#!/usr/local/bin/tclsh
#------------------------------------------------------------------------------
# Name           : test.9.1.15_SVAPI_layer23TrafficFlowDetective.tcl
# Author         : Jayasri Dhar
# Purpose        :
# Topology       : Create a configuration with 3-4 traffic items with multiple tracking.
#                  For example 1st traffic item track by SRC and Dst IP,
#                  2 nd one on SRC iP, Qos etc.Apply and Start traffic.
# Verification   : 1. Emulate All  flow based on selected stat/Best Performer
#                  2. Emulate All Live flow based on selected stat/Best Performer
#                  3. Emulate All dead flow based on selected stat/Best Performer
#                  4. Check no dead flow before stopping traffic
#                  5. Check no live flow after stoping traffic
#                  6. Check All Flow coming even after traffic stop
#
# Config Format  : ixncfg used
#------------------------------------------------------------------------------

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

# 9.1.15 Test Case Coverage
set ::TestPart0 0
set ::TestPart1 1
set ::TestPart2 1 ;
set ::TestPart3 0 ; #BUG506769
set ::TestPart4 1 ;
set ::TestPart5 1 ;
set ::TestPart6 1 ;

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
    if  {[ixNet exec loadConfig [ixNet readFrom \
         $::pwd/$configFileName]] != "::ixNet::OK"} {
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
    set status      [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    log "Assigned: $status"
    if {[string equal [lindex $status 0]  $vPort1] != 1 || \
        [string equal [lindex $status 1]  $vPort2] != 1} {
        ixNetCleanUp
        return $FAILED
    }
    ixTclNet::CheckLinkState $vPorts doneList

    # Start Protocol
    log "Stoping the Protocols ... "
    ixNet exec startAllProtocols

    log "Waiting for 20 Sec before verifying protocol stats.."
    after 20000

if {($::TestPart0 == 1)} {
    # Check for Protocol Session UP
    log "Verify protocol stats.."
    set completeStats { "Sess. Configured" 1 \
                        "Full State Count" 1 \
                        "Full Nbrs." 1}
    if {[checkAllProtocolStats $realPortsList "OSPF" $completeStats]} {
        log "Failure: Did not get the expected value for the all stats"
        ixNetCleanUp
        return $FAILED
    }
    log "Control Plane UP and Runing ..."
}


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

    # Start setting filters for TCL SV creation
    set trafficItem "Traffic Item 1"
    set usrFilterSetList [subst {{trafficItemFilterId {{name "$trafficItem"}}} \
                                     {portFilterIds {All}}}]
    set usrFilterSetList [subst {{trafficItemFilterId {{name "Traffic Item 1"}}} \
                          {portFilterIds {{name "$chassisIp2/Card$card2/Port$port2"}}}}]
    set usrStatsList {"Tx Frames" "Rx Frames" "Loss %"}

if {($::TestPart1 == 1)} {
    set caption "FlowdetectiveView_AllFlows"
    set fdConfigList {deadFlowsThreshold 5 \
                      flowFilterType allFlows}
    set addFilterList [subst {{allFlowsFilter { \
                        {sortByStatisticId "TotalFrames" numberOfResults "10" sortingCondition "bestPerformers"}}}}]


    if {[designL23TrafficFlowDetectiveStatisticView $caption $fdConfigList $usrFilterSetList \
                            $addFilterList $usrStatsList] == 1} {
        log "Not able to emulate $caption Statistics View"
        ixNetCleanUp
        return $FAILED
    }
    log "$caption Statistics View Successfully Emulated..."

    # Verify view creation as per user specification
    set matchRowValues {}
    set matchRowValues [linsert $matchRowValues 1 [string repeat  {{Traffic Item 1} } 10]]
    set usrSpecLists [subst {{columnCaptions {{Rx Frames} {Tx Frames} {Loss %} \
                                {Tx Port} {Rx Port} {Traffic Item} {Source/Dest Endpoint Pair}}} \
                        {matchRowValues $matchRowValues}}]
    log "Verify designed Stats View as per user specification..."
    if {[verifyDesignedStatisticView $caption $usrSpecLists] == 1} {
        log "Not able to emulate $caption Statistics View as per user spec."
        ixNetCleanUp
        return $FAILED
    }

    log "Check Flow Statistics for $caption ..."
    if {[checkAllTrafficStats $caption ] == 1} {
        log "Not able to retrieve statistics values from $caption"
        ixNetCleanUp
        return $FAILED
    }
}

if {($::TestPart2 == 1)} {
    set caption "FlowdetectiveView_LiveFlows"
    set fdConfigList {deadFlowsThreshold 5 \
                      flowFilterType liveFlows}
    set addFilterList [subst {{liveFlowsFilter { \
                        {sortByStatisticId "TotalFrames" numberOfResults "5" sortingCondition "bestPerformers"}}}}]

    if {[designL23TrafficFlowDetectiveStatisticView $caption $fdConfigList $usrFilterSetList \
                            $addFilterList $usrStatsList] == 1} {
        log "Not able to emulate $caption Statistics View"
        ixNetCleanUp
        return $FAILED
    }
    log "$caption Statistics View Successfully Emulated..."

    # Verify view creation as per user specification
    set matchRowValues {}
    set matchRowValues [linsert $matchRowValues 1 [string repeat  {{Traffic Item 1} } 5]]
    set usrSpecLists [subst {{columnCaptions {{Rx Frames} {Tx Frames} {Loss %} \
                                {Tx Port} {Rx Port} {Traffic Item} {Source/Dest Endpoint Pair}}} \
                        {matchRowValues $matchRowValues}}]
    log "Verify designed Stats View as per user specification..."
    if {[verifyDesignedStatisticView $caption $usrSpecLists] == 1} {
        log "Not able to emulate $caption Statistics View as per user spec."
        ixNetCleanUp
        return $FAILED
    }

    log "Check Flow Statistics for $caption ..."
    if {[checkAllTrafficStats $caption ] == 1} {
        log "Not able to retrieve statistics values from $caption"
        ixNetCleanUp
        return $FAILED
    }
}
    # Traffic Stop
    if {[stopTraffic $traffic] == 1} {
        log "Failed to stop traffic"
        ixNetCleanUp
        return $FAILED
    }

    log "Wait for 10 Sec after stoping traffic..."
    after 10000

if {($::TestPart3 == 1)} {
    set caption "FlowdetectiveView_DeadFlows"
    set fdConfigList {deadFlowsThreshold 1 \
                      flowFilterType deadFlows}
    set addFilterList [subst {{deadFlowsFilter { \
                        {numberOfResults "15" sortingCondition "descending"}}}}]

    if {[designL23TrafficFlowDetectiveStatisticView $caption $fdConfigList $usrFilterSetList \
                            $addFilterList $usrStatsList] == 1} {
        log "Not able to emulate $caption Statistics View"
        ixNetCleanUp
        return $FAILED
    }
    log "$caption Statistics View Successfully Emulated..."

    # Verify view creation as per user specification
    set matchRowValues {}
    set matchRowValues [linsert $matchRowValues 1 [string repeat  {{Traffic Item 1} } 15]]
    set usrSpecLists [subst {{columnCaptions {{Rx Frames} {Tx Frames} {Loss %} \
                                {Tx Port} {Rx Port} {Traffic Item} {Source/Dest Endpoint Pair}}} \
                        {matchRowValues $matchRowValues}}]
    log "Verify designed Stats View as per user specification..."
    if {[verifyDesignedStatisticView $caption $usrSpecLists] == 1} {
        log "Not able to emulate $caption Statistics View as per user spec."
        ixNetCleanUp
        return $FAILED
    }

    log "Check Flow Statistics for $caption ..."
    if {[checkAllTrafficStats $caption ] == 1} {
        log "Not able to retrieve statistics values from $caption"
        ixNetCleanUp
        return $FAILED
    }
}

    log "Stoping Protocols on both the ports.."
    ixNet exec stopAllProtocols
    after 2000

    # Cleanup
    ixNetCleanUp
    return $PASSED
}


#------------------------------------------------------------------------------#
# Execute the Action procedure defined above                                   #
#------------------------------------------------------------------------------#
Execute_Action
