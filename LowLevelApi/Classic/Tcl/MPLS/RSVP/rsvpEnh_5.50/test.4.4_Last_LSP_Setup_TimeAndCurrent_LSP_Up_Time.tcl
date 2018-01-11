source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#------------------------------------------------------------------------------
# Name                      : test.4.4_Last_LSP_Setup_TimeAndCurrent_LSP_Up_Time.tcl
# Author                    : Sanchari Roy
# Purpose                   : Automate RSBP Last_LSP_Setup_TimeAndCurrent_LSP_Up_Time_functionality
#
# Configuration Procedure   : 1> Configure RSVP-TE through Wizard.
#                           : 2> Configure one Neighbor Pair per port with 2000 Tunnel Endpoints per Neighbor Pair.
#                           : 3> Enable the checkbox "Enable Path Re-optimization".
#                           : 4> Enable SREFRESH Message with default interval of 30 secs.
#                           : 5> At first start RSVP-TE protocol in Egress port and then in Ingress port.
#                           : 6> Check the values Last_LSP_Setup_TimeAndCurrent_LSP_Up_Time in learned info
#                           : 7> Disable/Enable the tunnelTailRange simultaneously.
#                           : 8> Check the values Last_LSP_Setup_TimeAndCurrent_LSP_Up_Time in learned info again
# Verification steps        : 1> Verify value of currentLspOrSubLspUpTime is greater than 1 after Disable/Enable the
#                           : tunnelTailRange simultaneously.
# Config Format             : ixncfg used
#------------------------------------------------------------------------------

proc configureIxNetworkGui  {} {
    set configFileName \
        "config.4.4_Last_LSP_Setup_TimeAndCurrent_LSP_Up_Time.ixncfg"

    set isError [catch {\
        [ixNet exec loadConfig [ixNet readFrom $::pwd/$configFileName]]} \
        errMsg]

    if {$isError} {
        puts "unable to read config file"
    }

}


##############################################################################
#PROC NAME  :getValueOfLearnedInfoAttributes
#ARGUMENT   :
#           :Name of the attribute of rsvpNeighborPair
#            whose value is required
#DESCRIPTION:Returns the value of the given attribute of rsvpNeighborPair
##############################################################################
proc getValueOfLearnedInfoAttributes  {attrName} {

    set vPorts      [ixNet getList [ixNet getRoot] vport]
    set vPort1      [lindex $vPorts 0]
    set rsvp $vPort1/protocols/rsvp
    set neighborPair [lindex [ixNet getList $rsvp neighborPair] 0]

    set ref [ixNet exec refreshReceivedLabelInfo $neighborPair]

    set count 0
    set isComplete false
    while {$isComplete != true} {
        set isComplete [ixNet getAttr $neighborPair -isLearnedInfoRefreshed]
        after 1000
        incr count
        if {$count > 50} {
            log "Failed to retrieve learned info"
            ixNetCleanUp
            return $FAILED
        }
    }
    set labelList1 [lindex [ixNet getList $neighborPair receivedLabel] 0]
    set val [ixNet getAttr $labelList1 -$attrName]


  return $val

}


proc Action {portData1 portData2} {
    source $::pwd/rateControlUtils.tcl

    set FAILED 1
    set PASSED 0

    # get port info 1
    set chassisIp1 [getChassisIp $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    # get port info 2
    set chassisIp2 [getChassisIp  $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    # Hostname, where IxNetwork TCL-Server client runs
    set hostName [lindex [getHostName $portData1] 0]

    # Version Number (IxNetwork Major version No i.e. 5.50)
    set version "5.50"

    # connect to client
    if {[ixNet connect $hostName -version 5.50] != "::ixNet::OK"} {
        puts "Test case failed unable to connect to IxNetwork"
        return $FAILED
    }

    # clean up config
    ixNet exec newConfig

    # Configure IxNetwork GUI
    configureIxNetworkGui

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2]]

    # get root object
    set root [ixNet getRoot]

    # Assign real ports to virtual ports
    puts "getting virtual ports ...."
    set vPorts [ixNet getList $root vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]

    # Assign virtual ports to real ports
    puts "Assign virtual ports to real ports ..."
    if {[catch {ixTclNet::AssignPorts $realPortsList {} $vPorts}]} {
        puts "Error in assigning ports"
        ixNet exec newConfig
    }

    # Start Protocols
    log "At first start RSVP-TE protocol in Egress port and \
         then in Ingress port"
    if {([ixNet exec start $vPort1/protocols/rsvp] != "::ixNet::OK")} {
        log "Failed to start protocol rsvp on port1 ..."
        ixNetCleanUp
        return $FAILED
    }

    after 5000

    if {([ixNet exec start $vPort2/protocols/rsvp] != "::ixNet::OK")} {
        log "Failed to start protocol rsvp on port2 ..."
        ixNetCleanUp
        return $FAILED
    }
    log "Starting protocol OSPF in both ports"
    if {([ixNet exec start $vPort1/protocols/ospf] != "::ixNet::OK") || \
        ([ixNet exec start $vPort2/protocols/ospf] != "::ixNet::OK")} {
        log "Failed to start protocol ospf on both ports ..."
        ixNetCleanUp
        return $FAILED
    }

    log "Protocol started. Waiting for 5 minutes for protocol \
         Sessions to be up"
    after 300000

    # Verify Stats
    log "Verifying rsvp  protocol stats on both ports..."

    set rsvpStatsListPort1 {"Ingress LSPs Configured" 2000 \
                            "Ingress LSPs Up"         2000}


    set portList1 [list [list $chassisIp1 $card1 $port1]]
    if {[checkAllProtocolStats            \
             $portList1                   \
             "RSVP Aggregated Statistics" \
             $rsvpStatsListPort1]} {
        log "Did not get the expected rsvp protocol stats value on port1"
        ixNetCleanUp
        return $FAILED
    }

    set rsvpStatsListPort2 {"Egress LSPs Up" 2000}

    set portList2 [list [list $chassisIp2 $card2 $port2]]
    if {[checkAllProtocolStats             \
              $portList2                   \
              "RSVP Aggregated Statistics" \
              $rsvpStatsListPort2]} {
        log "Did not get the expected rsvp protocol stats value on port2"
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected rsvp protocol stats values on both ports..."


    log "Wait for 30 second"
    after 30000

    log "Now check if value of both currentLspOrSubLspUpTime & \
         lspOrSubLspSetupTime greater than 1"


    set currentTmBeforeEnDis [getValueOfLearnedInfoAttributes \
                                  lspOrSubLspSetupTime]

    set lspOrSubLspSetupTime [getValueOfLearnedInfoAttributes \
                                  currentLspOrSubLspUpTime]

    if {$currentTmBeforeEnDis < 1} {
       log "Value of currentTmBeforeEnDis is currentTmBeforeEnDis,\
            should not < 1"
       ixNetCleanUp
       return $FAILED
    }
    if {$lspOrSubLspSetupTime < 1} {
       log "Value of lspOrSubLspSetupTime is \
            $lspOrSubLspSetupTime,should not < 1"
       ixNetCleanUp
       return $FAILED
    }

    log "Value of both currentLspOrSubLspUpTime & \
         lspOrSubLspSetupTime is greater than 1"

    # Disable/Enable the tunnelTailRange simultaneously.
    log "Disabling the tunnelTailRange."

    set proto $vPort1/protocols/rsvp
    set neighborPair [lindex [ixNet getList $proto neighborPair] 0]
    set destinationRange [ixNet getList $neighborPair destinationRange]

    for {set i 0} {$i <= 1999} {incr i 1} {

        set destRange       [lindex $destinationRange $i]
        if {[setAndCheckAttributeValue $destRange "enabled" {"false" y}] == 1} {
            log "Failed to enable tunnelTailRange!!!"
            ixNetCleanUp
            return $FAILED
        }
    }

    log "Waiting for 20 Sec..."
    after 20000

    log "Enabling the tunnelTailRange."

    set proto $vPort1/protocols/rsvp
    set neighborPair [lindex [ixNet getList $proto neighborPair] 0]
    set destinationRange [ixNet getList $neighborPair destinationRange]

    for {set i 0} {$i <= 1999} {incr i 1} {

        set destRange [lindex $destinationRange $i]
        if {[setAndCheckAttributeValue $destRange "enabled" \
            {"true" y}] == 1} {
            log "Failed to enable tunnelTailRange!!!"
            ixNetCleanUp
            return $FAILED
        }
    }

    log "Waiting for 5 Sec..."
    after 5000

    log "Verify value of currentLspOrSubLspUpTime is less after \
         Disable/Enable the tunnelTailRange simultaneously"

    set currentTmAfterEnDis [getValueOfLearnedInfoAttributes \
                                 lspOrSubLspSetupTime]

    set lspOrSubLspSetupTime [getValueOfLearnedInfoAttributes \
                                  currentLspOrSubLspUpTime]

    if {$currentTmAfterEnDis < 1} {
       log "Value of currentTmAfterEnDis is $currentTmAfterEnDis,\
            should not < 1"
       ixNetCleanUp
       return $FAILED
    }

    log "Verify value of lspOrSubLspSetupTime is greater than 1 after \
         Disable/Enable the tunnelTailRange simultaneously."

    if {$lspOrSubLspSetupTime < 1} {
       log "Value of lspOrSubLspSetupTime is $lspOrSubLspSetupTime, \
            should not less than 1"
       ixNetCleanUp
       return $FAILED
    }

    # Stop Protocols
    log "Stopping protocol rsvp on both ports..."
    if {([ixNet exec stop $vPort1/protocols/rsvp] != "::ixNet::OK") || \
        ([ixNet exec stop $vPort2/protocols/rsvp] != "::ixNet::OK")} {
        log "Failed to stop protocol rsvp on both ports..."
        ixNetCleanUp
        return $FAILED
    }

    log "Stopping protocol ospf on both ports..."
    if {([ixNet exec stop $vPort1/protocols/ospf] != "::ixNet::OK") || \
        ([ixNet exec stop $vPort2/protocols/ospf] != "::ixNet::OK")} {
        log "Failed to stop protocol ospf on both ports..."
        ixNetCleanUp
        return $FAILED
    }

    # Cleanup
    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
