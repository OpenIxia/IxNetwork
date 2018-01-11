#!/usr/local/bin/tclsh
#------------------------------------------------------------------------------
# Name           : test.9.1.9_SVAPI_nestedDrilldown.tcl
# Author         : Jayasri Dhar
# Purpose        : 5.40 SV API Verification
# Topology       : Create a configuration with 1-2 traffic items with Egress tracking.
#                  Emulate Egress-Ingress stats
# Verification   : 1. Check stats from TI Agregated view
#                  2. Emulate 1st Level Drilldown
#                  3. Emulate 2nd Level Drilldown
#                  4. Emulate 3rd Level Drilldown
# Config Format  : ixncfg used
#------------------------------------------------------------------------------

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

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
    if  {[ixNet exec loadConfig [ixNet readFrom $::pwd/$configFileName]] != \
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
    set status      [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    log "Assigned: $status"
    if {[string equal [lindex $status 0]  $vPort1] != 1 || \
        [string equal [lindex $status 1]  $vPort2] != 1} {
        ixNetCleanUp
        return $FAILED
    }
    ixTclNet::CheckLinkState $vPorts doneList
    after 5000

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

    # Traffic Stop
    if {[stopTraffic $traffic] == 1} {
        log "Failed to stop traffic"
        ixNetCleanUp
        return $FAILED
    }


    # Check stats from TI Agregated view
    # Checking from Default 'Traffic Item Statistics' View
    log "Check Traffic Item Statistics..."
    if {[checkAllTrafficStats "Traffic Item Statistics"] == 1} {
        log "Not able to retrieve statistics values for Traffic Item Statistics"
        ixNetCleanUp
        return $FAILED
    }

    # Emulating Egress Tracking
    set caption "EgressTracking"
    set egressTracking "Ethernet:Outer VLAN Priority (3 bits) at offset 112"
    set usrFilterSetList [subst {{trafficItemFilterId {{name "TrafficItem_EgressTracking"}}} \
                                     {portFilterIds {{name "$chassisIp2/Card$card2/Port$port2"}}}}]
    set addFilterList [subst {{enumerationFilter { \
                        {trackingFilterId "$egressTracking" sortDirection "ascending"}}}}]
    set usrStatsList {"Tx Frames" "Rx Frames" "Loss %"}
    set fv {egressLatencyBinDisplayOption showEgressRows}

    # Design View
    if {[designL23TrafficFlowStatisticView $caption $fv $usrFilterSetList $addFilterList $usrStatsList] == 1} {
        log "Not able to emulate $caption Statistics View..."
        ixNetCleanUp
        return $FAILED
    }
    log "$caption Statistics View Successfully Emulated..."

    # Verify view creation as per user specification
    set usrSpecLists {{columnCaptions {{Rx Frames} {Tx Frames} {Loss %} \
                            {Tx Port} {Rx Port} {Egress Tracking}}} \
                    {matchRowValues {{{Ethernet:Outer VLAN Priority (3 bits) at offset 112} 0 1 2 3 4 5 6 7}}}}
    log "Verify designed Stats View as per user specification..."
    if {[verifyDesignedStatisticView $caption $usrSpecLists] == 1} {
        log "Not able to emulate $caption Statistics View as per user spec."
        ixNetCleanUp
        return $FAILED
    }

    #verify stats
    log "Check Traffic Egress Statistics in created SV..."
    set matchBucketList {{2 629407 15} {5 629407 15}}
    if {[checkEgressViewStats $caption 15 $matchBucketList] == 1} {
        log "Not able to retrieve statistics values for Traffic Item Statistics"
        ixNetCleanUp
        return $FAILED
    }

    log "Stoping the Protocols ... "
    ixNet exec stopAllProtocols
    after 4000

    # Cleanup
    ixNetCleanUp
    return $PASSED
}

#------------------------------------------------------------------------------#
# Execute the Action procedure defined above                                   #
#------------------------------------------------------------------------------#
Execute_Action
