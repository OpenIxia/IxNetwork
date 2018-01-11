#!/usr/local/bin/tclsh
#------------------------------------------------------------------------------
# Name           : test.9.1.2_SVAPI_layer23TrafficItem.tcl
# Author         : Jayasri Dhar
# Purpose        : 5.40 SV API verification
# Topology       : Create a configuration with 1 traffic items with default
#                   name.
# Verification   : Create TCL SV layer23TrafficItem
#                  1. Set all availableTrafficItemFilter
#                  2. Set one availableTrafficItemFilter
#                  2. Set multiple availableTrafficItemFilter
#                  Check for successful view creation
# Config Format  : ixncfg used
#------------------------------------------------------------------------------

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

# 9.1.2 Test Case Coverage
set ::TestPart1 1
set ::TestPart2 1
set ::TestPart3 1

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
    after 2000

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

    # Check default stats for sanity
    log "Check Traffic Item Statistics..."
    if {[checkAllTrafficStats "Traffic Item Statistics"] == 1} {
        log "Not able to retrieve statistics values for Traffic Item Statistics"
        ixNetCleanUp
        return $FAILED
    }


    if {[designL23TrafficItemStatisticView "AllTI-AllStats"] == 1} {
        log "Not able to emulate L23TrafficItem Statistics View"
        ixNetCleanUp
        return $FAILED
    }

    set usrSpecLists {{columnCaptions {{Traffic Item} \
                            {Cut-Through Min Latency (ns)} \
                            {Cut-Through Max Latency (ns)} \
                            {Cut-Through Avg Latency (ns)} \
                            {Rx Frames} {Rx Frame Rate} \
                            {First TimeStamp} {Last TimeStamp} \
                            {Tx Frames} {Frames Delta} {Loss %} \
                            {Tx Frame Rate}  \
                            {Rx Bytes} {Rx Rate (Bps)}}} \
                     {matchRowValues {{ingressTracking-1} \
                            {ingress Tracking 2} \
                            {ingressTracking-3}}}}

    log "Verify designed Stats View as per user specification..."
    if {[verifyDesignedStatisticView "AllTI-AllStats" $usrSpecLists] == 1} {
        log "Not able to emulate L23TrafficItem Statistics View as per user spec."
        ixNetCleanUp
        return $FAILED
    }

    log "Check Traffic Item Statistics in created SV..."
    if {[checkAllTrafficStats "AllTI-AllStats"] == 1} {
        log "Not able to retrieve statistics values for Traffic Item Statistics"
        ixNetCleanUp
        return $FAILED
    }


    set usrFilterSetList {{trafficItemFilterIds {{name "ingressTracking-3"}}}}
    set usrStatsList {"Tx Frames" "Rx Frames"}

    if {[designL23TrafficItemStatisticView "specifiedTI-selectedStats" \
                                    $usrFilterSetList $usrStatsList] == 1} {
        log "Not able to emulate L23TrafficItem Statistics View"
        ixNetCleanUp
        return $FAILED
    }

    set usrSpecLists {{columnCaptions {{Traffic Item} {Rx Frames} {Tx Frames}}} \
                     {matchRowValues {{ingressTracking-3}}}}

    log "Verify designed Stats View as per user specification..."
    if {[verifyDesignedStatisticView "specifiedTI-selectedStats" $usrSpecLists] == 1} {
        log "Not able to emulate L23TrafficItem Statistics View as per user spec."
        ixNetCleanUp
        return $FAILED
    }

    log "Check Traffic Item Statistics in created SV..."
    if {[checkAllTrafficStats "specifiedTI-selectedStats"] == 1} {
        log "Not able to retrieve statistics values for Traffic Item Statistics"
        ixNetCleanUp
        return $FAILED
    }


    set usrFilterSetList {{trafficItemFilterIds {{name "ingressTracking-1"} {name "ingress Tracking 2"}}}}
    set usrStatsList {"Tx Frames" "Rx Frames"}

    if {[designL23TrafficItemStatisticView "specified2TI-selectedStats" \
                                    $usrFilterSetList $usrStatsList] == 1} {
        log "Not able to emulate L23TrafficItem Statistics View"
        ixNetCleanUp
        return $FAILED
    }

    set usrSpecLists {{columnCaptions {{Traffic Item} {Rx Frames} {Tx Frames}}} \
                     {matchRowValues {{ingressTracking-1} {ingress Tracking 2}}}}

    log "Verify designed Stats View as per user specification..."
    if {[verifyDesignedStatisticView "specified2TI-selectedStats" $usrSpecLists] == 1} {
        log "Not able to emulate L23TrafficItem Statistics View as per user spec."
        ixNetCleanUp
        return $FAILED
    }

    log "Check Traffic Item Statistics in created SV..."
    if {[checkAllTrafficStats "specified2TI-selectedStats"] == 1} {
        log "Not able to retrieve statistics values for Traffic Item Statistics"
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
