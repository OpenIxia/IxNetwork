#!/usr/local/bin/tclsh
#------------------------------------------------------------------------------
# Name           : test.9.1.13_SVAPI_LatencyBinView.tcl
# Author         : Jayasri Dhar
# Purpose        : 5.40 SV API Verification
# Topology       : Create a configuration with 3-4 traffic items with latency
#                  bin tracking.
# Verification   : Verify SV for emulated Latency Bin Stats
# Config Format  : ixncfg used
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

proc Action {portData1 portData2} {

    # initialize return value
    set FAILED 1
    set PASSED 0

    # Get real card1/port1 from portData
    set chassisIp1 [getChassisIp $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    # Get real card2/port2 from portData
    set chassisIp2 [getChassisIp $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

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

    log "Waiting for 10 Sec.."
    after 10000

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
        log "Not able to values for Traffic Item Statistics"
        ixNetCleanUp
        return $FAILED
    }

    # Emulating Latency Bin
    set caption "LatencyBin"
    set usrFilterSetList \
        [subst {{trafficItemFilterId {{name "Traffic-Item-1"}}} \
                {portFilterIds {{name "$chassisIp2/Card$card2/Port$port2"}}}}]

    set fv {egressLatencyBinDisplayOption showLatencyBinStats}

    set usrStatsList {{Cut-Through Min Latency (ns) per Bin}   \
                      {Cut-Through Max Latency (ns) per Bin}   \
                        {Cut-Through Avg Latency (ns) per Bin} \
                        {Rx Frames per Bin}                    \
                        {Rx Frame Rate per Bin}                \
                        {First TimeStamp per Bin}              \
                        {Last TimeStamp per Bin}               \
                        {kRxFdFramesDelta per Bin}             \
                        {kRxFdTimestampDelta per Bin}          \
                        {Rx Bytes per Bin}                     \
                        {Rx Rate (Bps) per Bin}                \
                        {kRxFdBytesDelta per Bin}}

    # Design View
    if {[designL23TrafficFlowStatisticView $caption          \
                                           $fv               \
                                           $usrFilterSetList \
                                           {}                \
                                           $usrStatsList] == 1} {
        log "Not able to emulate $caption Statistics View..."
        ixNetCleanUp
        return $FAILED
    }
    log "$caption Statistics View Successfully Emulated..."

    # Verify view creation as per user specification
    set usrSpecLists {{columnCaptions {{Tx Port} {Rx Port} {Traffic Item} \
                {Cut-Through Min Latency (ns) per Bin : 0us - 1us} \
                {Cut-Through Min Latency (ns) per Bin : 1us - 1.42us} \
                {Cut-Through Min Latency (ns) per Bin : 1.42us - 2us} \
                {Cut-Through Min Latency (ns) per Bin : 2us - 2.82us} \
                {Cut-Through Min Latency (ns) per Bin : 2.82us - 4us} \
                {Cut-Through Min Latency (ns) per Bin : 4us - 5.66us} \
                {Cut-Through Min Latency (ns) per Bin : 5.66us - 8us} \
                {Cut-Through Min Latency (ns) per Bin : 8us - maxus} \
                {Cut-Through Max Latency (ns) per Bin : 0us - 1us} \
                {Cut-Through Max Latency (ns) per Bin : 1us - 1.42us} \
                {Cut-Through Max Latency (ns) per Bin : 1.42us - 2us} \
                {Cut-Through Max Latency (ns) per Bin : 2us - 2.82us} \
                {Cut-Through Max Latency (ns) per Bin : 2.82us - 4us} \
                {Cut-Through Max Latency (ns) per Bin : 4us - 5.66us} \
                {Cut-Through Max Latency (ns) per Bin : 5.66us - 8us} \
                {Cut-Through Max Latency (ns) per Bin : 8us - maxus} \
                {Cut-Through Avg Latency (ns) per Bin : 0us - 1us} \
                {Cut-Through Avg Latency (ns) per Bin : 1us - 1.42us} \
                {Cut-Through Avg Latency (ns) per Bin : 1.42us - 2us} \
                {Cut-Through Avg Latency (ns) per Bin : 2us - 2.82us} \
                {Cut-Through Avg Latency (ns) per Bin : 2.82us - 4us} \
                {Cut-Through Avg Latency (ns) per Bin : 4us - 5.66us} \
                {Cut-Through Avg Latency (ns) per Bin : 5.66us - 8us} \
                {Cut-Through Avg Latency (ns) per Bin : 8us - maxus} \
                {Rx Frames per Bin : 0us - 1us} \
                {Rx Frames per Bin : 1us - 1.42us} \
                {Rx Frames per Bin : 1.42us - 2us} \
                {Rx Frames per Bin : 2us - 2.82us} \
                {Rx Frames per Bin : 2.82us - 4us} \
                {Rx Frames per Bin : 4us - 5.66us} \
                {Rx Frames per Bin : 5.66us - 8us} \
                {Rx Frames per Bin : 8us - maxus} \
                {Rx Frame Rate per Bin : 0us - 1us} \
                {Rx Frame Rate per Bin : 1us - 1.42us} \
                {Rx Frame Rate per Bin : 1.42us - 2us} \
                {Rx Frame Rate per Bin : 2us - 2.82us} \
                {Rx Frame Rate per Bin : 2.82us - 4us} \
                {Rx Frame Rate per Bin : 4us - 5.66us} \
                {Rx Frame Rate per Bin : 5.66us - 8us} \
                {Rx Frame Rate per Bin : 8us - maxus} \
                {First TimeStamp per Bin : 0us - 1us} \
                {First TimeStamp per Bin : 1us - 1.42us} \
                {First TimeStamp per Bin : 1.42us - 2us} \
                {First TimeStamp per Bin : 2us - 2.82us} \
                {First TimeStamp per Bin : 2.82us - 4us} \
                {First TimeStamp per Bin : 4us - 5.66us} \
                {First TimeStamp per Bin : 5.66us - 8us} \
                {First TimeStamp per Bin : 8us - maxus} \
                {Last TimeStamp per Bin : 0us - 1us} \
                {Last TimeStamp per Bin : 1us - 1.42us} \
                {Last TimeStamp per Bin : 1.42us - 2us} \
                {Last TimeStamp per Bin : 2us - 2.82us} \
                {Last TimeStamp per Bin : 2.82us - 4us} \
                {Last TimeStamp per Bin : 4us - 5.66us} \
                {Last TimeStamp per Bin : 5.66us - 8us} \
                {Last TimeStamp per Bin : 8us - maxus} \
                {Rx Bytes per Bin : 0us - 1us} \
                {Rx Bytes per Bin : 1us - 1.42us} \
                {Rx Bytes per Bin : 1.42us - 2us} \
                {Rx Bytes per Bin : 2us - 2.82us} \
                {Rx Bytes per Bin : 2.82us - 4us} \
                {Rx Bytes per Bin : 4us - 5.66us} \
                {Rx Bytes per Bin : 5.66us - 8us} \
                {Rx Bytes per Bin : 8us - maxus} \
                {Rx Rate (Bps) per Bin : 0us - 1us} \
                {Rx Rate (Bps) per Bin : 1us - 1.42us} \
                {Rx Rate (Bps) per Bin : 1.42us - 2us} \
                {Rx Rate (Bps) per Bin : 2us - 2.82us} \
                {Rx Rate (Bps) per Bin : 2.82us - 4us} \
                {Rx Rate (Bps) per Bin : 4us - 5.66us} \
                {Rx Rate (Bps) per Bin : 5.66us - 8us} \
                {Rx Rate (Bps) per Bin : 8us - maxus}}} \
                {matchRowValues {{Traffic-Item-1}}}}

    log "Verify designed Stats View as per user specification..."
    if {[verifyDesignedStatisticView $caption $usrSpecLists] == 1} {
        log "Not able to emulate $caption Statistics View as per user spec."
        ixNetCleanUp
        return $FAILED
    }

    log "Check Traffic Statistics in created SV..."
    if {[checkAllStats $caption {{"Rx Frames per Bin : 0us - 1us" "447124" "15"}}] == 1} {
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
