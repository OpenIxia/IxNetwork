#!/usr/local/bin/tclsh
################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

#------------------------------------------------------------------------------
# Name           : test.9.1.11_SVAPI_FlowFilteringReuseView.tcl
# Purpose        : 5.40 SV API Verification
# Topology       : Create a configuration with 3-4 traffic items with multiple tracking.
# Verification   : 1. Check stats from TI Agregated view
#                  2. one sorting option selected
#                  3. two sorting option selected reuse view
# Config Format  : ixncfg used
#------------------------------------------------------------------------------

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

# 9.1.11 Test Case Coverage
set ::TestPart0 1 ; # Control plane stats varification
set ::TestPart1 1 ; # Check stats from TI Agregated view
set ::TestPart2 1 ; #
set ::TestPart3 1 ; #

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
    if  {[ixNet exec loadConfig [ixNet readFrom $::pwd/$configFileName]] \
        != "::ixNet::OK"} {
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
    log "Starting the Protocols ... "
    ixNet exec startAllProtocols

    log "Waiting for 20 Sec before verifying protocol stats.."
    after 20000


    # Check for Protocol Session UP
    log "Verify protocol stats.."
    set completeStats { "IPv4 Routers Configured" 1 \
                        "IPv4 Routers Running" 1}
    if {[checkAllProtocolStats $realPortsList \
        "EIGRP Aggregated Statistics" $completeStats]} {
        log "Failure: Did not get the expected value for the all stats"
        ixNetCleanUp
        return $FAILED
    }
    log "Control Plane UP and Runing ..."



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

    set caption "ViewPerSortingOptionReuse"

    # Traffic Item "ingressTrackingRaw1" having 3 different
    # tracking in one traffic item and
    # Emulating 1st level drill down
    set ingressTracking "Source/Dest Value Pair"

    set usrFilterSetList [subst {{trafficItemFilterId {{name "ingressTrackingRaw1"}}}\
        {portFilterIds {{name "$chassisIp2/Card$card2/Port$port2"}}}}]

    set addFilterList [subst {{enumerationFilter { \
        {trackingFilterId "Source/Dest Value Pair" sortDirection "ascending"}}}}]

    set usrStatsList {"Tx Frames" "Rx Frames" "Loss %"}

    # Design View
    if {[designL23TrafficFlowStatisticView $caption {} $usrFilterSetList \
        $addFilterList $usrStatsList] == 1} {
        log "Not able to emulate $caption Statistics View..."
        ixNetCleanUp
        return $FAILED
    }
    log "$caption Statistics View Successfully Emulated..."

    # Verify view creation as per user specification
    set usrSpecLists {{columnCaptions {{Rx Frames} {Tx Frames} {Loss %} \
                      {Rx Port} {Source/Dest Value Pair}}} \
                    {matchRowValues {{4.1.1.1-4.1.6.1} \
                            {4.1.2.1-4.1.7.1} {4.1.3.1-4.1.8.1} \
                            {4.1.4.1-4.1.9.1} {4.1.5.1-4.1.10.1}}}}
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

    # Traffic Item "ingressTrackingRaw1" having 3 different tracking in one traffic item and
    # Emulating 2nd level drill down :: First by  Source/Dest Value Pair -> IPv4 :Precedence
    set ingressTracking "IPv4 :Precedence"
    set usrFilterSetList [subst {{trafficItemFilterId {{name "ingressTrackingRaw1"}}}\
                                     {portFilterIds {{name "$chassisIp2/Card$card2/Port$port2"}}}}]
    set addFilterList [subst {{enumerationFilter { \
            {trackingFilterId "IPv4 :Precedence" sortDirection "ascending"} \
            {trackingFilterId "Source/Dest Value Pair" sortDirection "ascending"}}}}]
    set usrStatsList {"Tx Frames" "Rx Frames" "Loss %"}

    # Design View
    if {[designL23TrafficFlowStatisticView $caption {} $usrFilterSetList \
        $addFilterList $usrStatsList {} 1] == 1} {
        log "Not able to emulate $caption Statistics View..."
        ixNetCleanUp
        return $FAILED
    }
    log "$caption Statistics View Successfully Emulated..."

    # Verify view creation as per user specification
    set usrSpecLists {{columnCaptions {{Rx Frames} {Tx Frames} {Loss %} \
                            {Rx Port} {IPv4 :Precedence} {Source/Dest Value Pair}}} \
                      {matchRowValues {{0} {1} {2} {3} {4} {5} {6}}} \
                      {matchRowValues {{4.1.1.1-4.1.6.1} {4.1.1.1-4.1.6.1} {4.1.2.1-4.1.7.1} \
                            {4.1.2.1-4.1.7.1} {4.1.3.1-4.1.8.1} \
                            {4.1.4.1-4.1.9.1} {4.1.5.1-4.1.10.1}}}}
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
