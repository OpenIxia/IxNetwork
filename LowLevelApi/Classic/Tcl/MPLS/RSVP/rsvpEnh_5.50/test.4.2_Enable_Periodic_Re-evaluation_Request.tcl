source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#------------------------------------------------------------------------------
# Name                      : test.4.2_Enable_Periodic_Re-evaluation_Request.tcl
# Author                    : Sanchari Roy
# Purpose                   : Automate RSBP Enable_Periodic_Re-evaluation_Request_Functionality
#
# Configuration Procedure   : 1> Configure RSVP-TE through Wizard.
#                           : 2> Configure one Neighbor Pair per port with 2 Tunnel Endpoints per
#                           : Neighbor Pair.
#                           : 3> Enable the checkbox "Enable Path Re-optimization" and "Enable Periodic
#                           : Re-evaluation Request".
#                           : 4> Configure "Re-evaluation Request Interval" = 20 secs and "Refresh Interval" = 30 secs in port1.
#                           : 5> Enable packet capture in both Control and Data mode
#                           : 6> At first start RSVP-TE protocol in Egress port and then in Ingress port.
# Verification steps        : 1> Verify the control capture of both ports.
#                           : 2> Check for the normal Path Message and the Path Message with Re-evaluation
#                           : Request flag set.
# Expected Results          : 1> The normal Path Message should be send only once.
#                           : 2> From next time onwards Path Message with Re-evaluation request flag set
#                           : should be send with the interval of "Re-evaluation Request Interval" configured
#                           : and no normal Path Message should be send.
# Config Format             : ixncfg used
#------------------------------------------------------------------------------

proc configureIxNetworkGui  {} {
    set configFileName \
        "config.4.2_Enable_Periodic_Re-evaluation_Request.ixncfg"

    set isError [catch {\
        [ixNet exec loadConfig [ixNet readFrom $::pwd/$configFileName]]} \
        errMsg]

    if {$isError} {
        puts "unable to read config file"
    }
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

    # enable NS on Link Up option
    set globals $root/globals
    set interfaces $globals/interfaces
    ixNet setAttr $interfaces -nsOnLinkup true
    ixNet commit

    # Assign virtual ports to real ports
    puts "Assign virtual ports to real ports ..."
    if {[catch {ixTclNet::AssignPorts $realPortsList {} $vPorts}]} {
        puts "Error in assigning ports"
        ixNet exec newConfig
    }

    # Enable & Start Capture
    log "Enable & Start Capture on both ports..."
    if {[enableCaptureMode $vPorts] == 1} {
        log "Failed to enable capture..."
        ixNetCleanUp
        return $FAILED
    }

    ixNet exec startCapture

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
        log "Failed to start protocol ospf in both ports..."
        ixNetCleanUp
        return $FAILED
    }

    log "Protocol started. Waiting for 120 Sec for protocol Sessions to be up"
    after 120000

    # Verify Stats
    log "Verifying rsvp  protocol stats on both ports..."


    set rsvpStatsListPort1 {"Ingress LSPs Configured" 1 \
                            "Ingress LSPs Up"         1}


    set portList1 [list [list $chassisIp1 $card1 $port1]]
    if {[checkAllProtocolStats            \
             $portList1                   \
             "RSVP Aggregated Statistics" \
             $rsvpStatsListPort1]} {

        log "Did not get the expected rsvp protocol stats value on port1..."
        ixNetCleanUp
        return $FAILED
    }

    set rsvpStatsListPort2 {"Egress LSPs Up" 1}

    set portList2 [list [list $chassisIp2 $card2 $port2]]
    if {[checkAllProtocolStats             \
              $portList2                   \
              "RSVP Aggregated Statistics" \
              $rsvpStatsListPort2]} {
        log "Did not get the expected rsvp protocol stats value on port2..."
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected rsvp protocol stats values on both ports..."

    log "Wait for 30 second"
    after 30000

    # Stop Capture
    log "Stopping Capture on both ports..."
    ixNet exec stopCapture

    log "Now check for normal Path Message in capture in port2"

    set packetsToVerify1 {96 96 "05"}

    log "chassisIp2 = $chassisIp2, card2 = $card2 port2 = $port2"
    if {[verifyCapturedPackets $chassisIp2 $card2 $port2 $packetsToVerify1] \
         == 1} {
        log "Expected normal Path Message in not found in capture--failed!!"
        return 1
    }
    log "Found normal Path Message in capture in port2"

    ##Path Message with Re-evaluation request flag set should be send with
    ##the interval of "Re-evaluation Request Interval" configured

    log "Now check for Path Message with Re-evaluation request flag"

    set matchFieldList {96 96 "25"}

    set rateList [subst {1 20}]
    set expectedPktCount [expr 1 * 3]

    if {[checkInterBurstGapThroughCapture \
              $chassisIp2                 \
              $card2                      \
              $port2                      \
              $matchFieldList             \
              $expectedPktCount           \
              $rateList 1] == 1} {
        log "Expected Path Message with Re-evaluation request \
             flag in not found in capture--failed!!"
        ixNetCleanUp
        return $FAILED
    }

    log "Path Message with Re-evaluation request flag set is \
         be send with Re-evaluation Request Interval"

    # Stop Protocols
    log "Stopping protocol rsvp on both ports..."
    if {([ixNet exec stop $vPort1/protocols/rsvp] != "::ixNet::OK") || \
        ([ixNet exec stop $vPort2/protocols/rsvp] != "::ixNet::OK")} {
        log "Failed to stop protocol rsvp on both ports..."
        ixNetCleanUp
        return $FAILED
    }

    log "Stopping protocol OSPF on both ports..."
    if {([ixNet exec stop $vPort1/protocols/ospf] != "::ixNet::OK") || \
        ([ixNet exec stop $vPort2/protocols/ospf] != "::ixNet::OK")} {
        log "Failed to stop protocol ospf on both ports ..."
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
