#!/usr/local/bin/tclsh
#------------------------------------------------------------------------------
# Name           : test.3.1.1.1_interleavedFrameRateOnFly.tcl
# Purpose        : Verifying traffic item configuration for Raw Traffic
#
# Topology       :  Configure BGPv4 protocol back to back with 4 route ranges
#                   Configure Traffic in the following way:-
#
#                   TrafficItem1 = RR1 of port1 -> RR1 of port2 frame Rate
#                   Type = lineRate
#
#                   TrafficItem2 = RR2 of port1 -> RR1 of port2 frame Rate
#                   Type = PacketRate
#
#                   TrafficItem3 = RR3 of port1 -> RR1 of port2 frame Rate
#                   Type = BitRate Start the traffic:
#
#                   When mode = fixed, do the flollowing while the traffic is
#                   running Increase the
#
#                   LineRate on the fly and check the the increased rate in
#                   stat
# ixncfg used    : Yes
# Scriptgen used : No
#------------------------------------------------------------------------------

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

proc checkDetailTrafficConfiguration {trafficItemName rateType rateValue} {
    set error 1
    #Getting the Traffic Item object hierarchy details
    set traffic [ixNet getRoot]/traffic
    set trafficItemList [ixNet getList $traffic trafficItem]
    for {set index 0} {$index < [llength $trafficItemList]} {incr index} {

        set trafficItem [lindex $trafficItemList $index]

        if {[ixNet getAttr $trafficItem -name] == $trafficItemName} {
            set configElementList [ixNet getList $trafficItem configElement]
            set configElement [lindex $configElementList 0]
            set frameRate [ixNet getList $configElement frameRate]
            puts [ixNet help $frameRate]
            log "Checking Frame Rate parameters..."

            if {[checkAttributeValue $frameRate [subst {type $rateType \
                                                 rate $rateValue}]] == 1} {
                return $error
            }
            break
        }
    }
    set error 0
    return $error
}


proc changeRateOnTheFly {trafficItemName rateType rateValue} {
    set isError 1
    set traffic [ixNet getRoot]/traffic
    set trafficItemList [ixNet getList $traffic trafficItem]

    for {set index 0} {$index < [llength $trafficItemList]} {incr index} {
        set trafficItem [lindex $trafficItemList $index]
        if {[ixNet getAttr $trafficItem -name] == $trafficItemName} {

            set dr [lindex [ixNet getList $traffic dynamicRate] $index]

            if {[setAndCheckAttributeValue $dr "rateType" [subst \
                {$rateType "y"}]] == 1} {
                return $isError
            }

            if {[setAndCheckAttributeValue $dr "rate" [subst \
                {$rateValue "y"}]] == 1} {
                return $isError
            }
            break
        }
    }
    set isError 0
    return $isError
}


proc Action {portData1 portData2} {

    # initialize return value
    set FAILED 1
    set PASSED 0

    # Get real card1/port1 from portData
    set chassisIp1 [getChassisIp $portData1]
    set card1 [getCardNumber $portData1]
    set port1 [getPortNumber $portData1]

    # Get real card2/port2 from portData
    set chassisIp2 [getChassisIp $portData2]
    set card2 [getCardNumber $portData2]
    set port2 [getPortNumber $portData2]

    # Hostname, where IxNetwork TCL-Server client runs
    set hostName [lindex [getHostName $portData1] 0]
    set connection_Result [connectToClient $portData1 $portData2 "5.40"]
    log "Connection Result: $connection_Result"
    if {[string equal $connection_Result "::ixNet::OK"] != 1} {
        log "connection to client unsuccessful"
        return $FAILED
    }
    log "connectToClient Successful"

    # clean up all the existing configurations from client
    log "cleaning up the client"
    ixNetCleanUp

    after 2000

    # load config files
    set configFileName config.[getTestId].ixncfg
    if {[ixNet exec loadConfig [ixNet readFrom $::pwd/$configFileName]] != \
        "::ixNet::OK"} {
        log "Loading IxNetwork config file : Failed "
        ixNetCleanUp
        return $FAILED
    }
    log "Loading IxNetwork config file : Passed"

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2]]

    # Assign real ports to virtual ports
    log "getting virtual ports ...."
    set vPorts      [ixNet getList [ixNet getRoot] vport]
    set vPort1      [lindex $vPorts 0]
    set vPort2      [lindex $vPorts 1]
    log "Virtual ports are = $vPorts"

    # Assign virtual ports to real ports
    log "Assign virtual ports to real ports ..."
    set force true
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    log "Assigned: $status"
    if {[string equal [lindex $status 0]  $vPort1] != 1 || \
        [string equal [lindex $status 1]  $vPort2] != 1} {
        ixNetCleanUp
        return $FAILED
    }
    ixTclNet::CheckLinkState $vPorts doneList
    after 5000

    # Start All Protocols
    log "Starting Protocols....."
    if {[ixNet exec startAllProtocols] != "::ixNet::OK"} {
        log "Failed to start Protocols"
        ixNetCleanUp
        return $FAILED
    }
    log "Protocols started successfully !!!"

    log "Waiting for 10 Sec before verifying protocol stats.."
    after 10000
    log "Verify Protocol Stats ....."
    set StatsList {"Sess. Configured" 1 \
                   "Sess. Up" 1}

    if {[checkAllProtocolStats $realPortsList "BGP Aggregated Statistics" \
        $StatsList]} {
        log "Failure: Did not get the expected value for the all stats"
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected values for all stats..."

    # Traffic Apply and Start
    set traffic [ixNet getRoot]/traffic
    if [generateApplyTraffic] {
        log "Failed to start traffic"
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic applyed successfully"

    if {[startTraffic $traffic] == 1} {
        log "Failed to start the traffic"
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic started successfully"

    log "Waiting for 20 seconds..."
    after 20000

    # Check stats from TI Agregated view
    # Checking from Default 'Traffic Item Statistics' View
    log "Check Traffic Item Statistics..."
    if {[checkAllTrafficStats "Traffic Item Statistics"] == 1} {
        log "Not able to retrieve statistics values for Traffic Item Statistics"
        ixNetCleanUp
        return $FAILED
    }

    # Check Initial Traffic Rate configuration
    set initialConfigList {"Traffic Item 1" "percentLineRate" "1.0" \
                           "Traffic Item 2" "framesPerSecond" "100.0" \
                           "Traffic Item 3" "bitsPerSecond" "1000.0" }

    foreach {tiName rateType rateValue} $initialConfigList {
        log "Checking rate configuration ($rateType $rateValue) for $tiName ..."
        if {[checkDetailTrafficConfiguration $tiName $rateType \
            $rateValue] == 1} {
            log "Checking Rate configuration faiils .."
            ixNetCleanUp
            return $FAILED
        }
    }

    # Check stats
    set matchStatList {{"Tx Frame Rate" 14880 15} \
                       {"Tx Frame Rate" 100 15} \
                       {"Tx Frame Rate" 15 15}}

    foreach matchStatListPerRowList $matchStatList {
        if {[checkAllStats "Traffic Item Statistics" [list \
            $matchStatListPerRowList]] == 1} {
            log "Tx Frame Rate Stats not per expectation.."
            ixNetCleanUp
            return $FAILED
        }
    }

    # Change the Rate On the Fly
    set onTheFLyChangeList {"Traffic Item 1" "percentLineRate" "5.0" \
                            "Traffic Item 2" "framesPerSecond" "1000.0" \
                            "Traffic Item 3" "bitsPerSecond" "20000.0" }

    foreach {tiName rateType rateValue} $onTheFLyChangeList {
        log "Setting $rateType to $rateValue for $tiName ..."
        if {[changeRateOnTheFly $tiName $rateType $rateValue] == 1} {
            log "Change Rate On the Fly faiils .."
            ixNetCleanUp
            return $FAILED
        }
    }

    log "Waiting for 30 seconds..."
    after 30000

    # Check the change reflected in stats
    set matchStatList1 {{"Tx Frame Rate" 74404 15}\
                        {"Tx Frame Rate" 1000 15} \
                        {"Tx Frame Rate" 312 15}}

    foreach matchStatListPerRowList1 $matchStatList1 {
        if {[checkAllStats "Traffic Item Statistics" \
            [list $matchStatListPerRowList1]] == 1} {
            log "Tx Frame Rate Stats not per expectation.."
            ixNetCleanUp
            return $FAILED
        }
    }

    log "Stoping the Protocols ... "
    ixNet exec stopAllProtocols
    after 4000


    if {[stopTraffic $traffic] == 1} {
        log "Failed to stop the traffic"
        ixNetCleanUp
        return $FAILED
    }

    # Cleanup
    ixNetCleanUp
    return $PASSED
}


#------------------------------------------------------------------------------#
# Execute the Action procedure defined above                                   #
#------------------------------------------------------------------------------#
Execute_Action
