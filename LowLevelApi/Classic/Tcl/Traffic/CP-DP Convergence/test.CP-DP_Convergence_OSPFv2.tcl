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
# FILE          :test.4.3.CP_EventTS_OSPFv2.tcl
#
# PURPOSE       :To Verify CP Event Time stamps,Event Name for OSPFv2 RRs by
#                Disabling/Enabling OSPFv2 Route Ranges.
#
# STEPS          : 1. Load config and assign ports
#                  2. Start OSPFv2.
#                  3. Generate,Apply and Start Traffic.
#                  4. Creating and Verifying Drill down view of Traffic stats
#                     Taking Drill down by Destination Endpoint)
#                  5. Disabling OSPFv2 Route Range on RX port.
#                  6. Verifying CP/DP stats.
#                  7. Clearing and verifying CP/DP stats.
#                  8. Enabling OSPFv2 Route Range on RX port.
#                  9. Verifying CP/DP stats.
#                  10.Stopping Traffic and protocol.
# STATUS         :NEW
#------------------------------------------------------------------------------

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

proc Action {portData1 portData2} {
    global endEventName
    global startEventName
    source $::pwd/CP-DPUtils.tcl
    #---------------------------------------------------------------------------
    # initialize return values and other variables
    #---------------------------------------------------------------------------
    set PASSED 0
    set FAILED 1
    #---------------------------------------------------------------------------
    # get port info 1
    #---------------------------------------------------------------------------
    set chassisIp1 [getChassisIp  $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    #---------------------------------------------------------------------------
    # get port info 2
    #---------------------------------------------------------------------------
    set chassisIp2 [getChassisIp  $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    #---------------------------------------------------------------------------
    # Connecting to client
    #---------------------------------------------------------------------------
    set connection_Result [connectToClient $portData1 $portData2 5.40]
    log "Connection Result: $connection_Result"
    if {[string equal $connection_Result "::ixNet::OK"] != 1} {
        log "connection to client unsuccessfill"
        return $FAILED
    }
    log "connectToClient Successful"

    #---------------------------------------------------------------------------
    # clean up all the existing configurations from client
    #---------------------------------------------------------------------------
    log "cleaning up the client"
    ixNetCleanUp

    #---------------------------------------------------------------------------
    # load the ixncfg config file
    #---------------------------------------------------------------------------
    set configFileName config.[getTestId].ixncfg
    if {[catch {ixNet exec loadConfig [ixNet readFrom $::pwd/$configFileName]} \
         errorMsg]} {
       log "Error in loading Config file: $errorMsg"
       ixNetCleanUp
       return $FAILED
    }

    #---------------------------------------------------------------------------
    # get the virtual port list and real port list
    #---------------------------------------------------------------------------
    log "getting virtual ports ...."
    set vPorts [ixNet getList [ixNet getRoot] vport]

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
        [list $chassisIp2 $card2 $port2] ]

    #---------------------------------------------------------------------------
    # Assign virtual ports to real ports
    #---------------------------------------------------------------------------
    log "Assign virtual ports to real ports ..."
    set force true
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    log "Assigned: $status"
    ixTclNet::CheckLinkState $vPorts doneList

    #---------------------------------------------------------------------------
    # Check if the ports are assigned if un assigned re-assign them
    #---------------------------------------------------------------------------
    after 5000
    ifUnassignedConnectAgain

    #---------------------------------------------------------------------------
    # Starting OSPF on port1 and port2
    #---------------------------------------------------------------------------
    catch {ixNet exec start ::ixNet::OBJ-/vport:1/protocols/ospf} result1
    catch {ixNet exec start ::ixNet::OBJ-/vport:2/protocols/ospf} result2
    if {$result1 != "::ixNet::OK" || $result2 != "::ixNet::OK"} {
       log "FAILED : Starting Protocol"
       ixNetCleanUp
       return $FAILED
    }
    log "SUCCESS : Protocol started on all ports"
    log "Waiting for 30 seconds for protocol session to come UP"
    after 30000

    #---------------------------------------------------------------------------
    # Verifying protocol stats
    #---------------------------------------------------------------------------
    set OSPFStatsList {"Sess. Configured" 1 \
                       "Full State Count" 1 \
                       "Full Nbrs." 1}
    if {[checkAllProtocolStats  $realPortsList "OSPF Aggregated Statistics" \
        $OSPFStatsList]} {
       log "Failure: Did not get the expected value for the all OSPF stats"
       ixNetCleanUp
       return $FAILED
    }

    #---------------------------------------------------------------------------
    # generte the traffic
    #---------------------------------------------------------------------------
    set traffic [ixNet getRoot]/traffic
    if {[generateApplyTraffic]} {
       log "Failed to Generate and Apply traffic"
       ixNetCleanUp
       return $FAILED
    }
    log "Traffic applyed successfully"
    #---------------------------------------------------------------------------
    # start the traffic
    #---------------------------------------------------------------------------
    if {[startTraffic $traffic] == 1} {
        log "Failed to start the traffic"
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic started successfully"

    #---------------------------------------------------------------------------
    # wait for desired amount of time
    #---------------------------------------------------------------------------
    set waitTime 15000
    log "wait for $waitTime ms"
    after $waitTime
    set DestinationIPList {{25.25.25.1} {26.26.26.1} {27.27.27.1}}
    set TrafficItemName "Traffic Item 1"
    set caption "FirstLevelDrilldown"
    if {[DesignAndVerifyCPDrillDownStats $TrafficItemName $chassisIp2 \
         Card$card2 Port$port2 $DestinationIPList]} {
        log "FAILED : Design and Verification of Dril down view"
        ixNetCleanUp
        return $FAILED
    }
    log "Disabling OSPFv2 Route Range on port2"

    set count 1
    while {$count < 4} {
        set routerange($count) [subst \
        {::ixNet::OBJ-/vport:2/protocols/ospf/router:1/routeRange:$count}]
        log "$routerange($count)"
        if {[setAndCheckAttributeValue $routerange($count) "enabled" \
           {"false" y}] == 1} {
           log "FAILURE :Disabling OSPFV2 Route Range$count failed"
           ixNetStopTrafficAndCleanup $traffic
           return $FAILED
       }
       incr count
    }

    log "SUCCESS :Disabled OSPFV2 Route Range"
    log "Waiting for 10 seconds after Disabling OSPFV2 Route Range"
    after 10000

    #-----------------------------------------------------------------------------------
    # Verifying CP stats
    #-----------------------------------------------------------------------------------

    set EndTSFlow3 [verifyCpStats $caption $DestinationIPList \
       3000000000 ospfDisableRR EndTSLastFlow]

    if {$EndTSFlow3 == 1} {
        log "FAILED : Verifiying CP stats after Disabling OSPFv2 RR"
        ixNetStopTrafficAndCleanup $traffic
        return $FAILED
    } else {
        log "SUCCESS : Verifiying CP stats after Disabling OSPFv2 RR"
    }


    #------------------------------------------------------------------------------------
    # Verification of CP stats after clearing CP-DP stats
    #------------------------------------------------------------------------------------

    if {[ClearAndVerifyCpDpStats $caption 3] == 0} {
        log "SUCCESS : Clearing and Verifying CP DP stats"
    } else {
        log "FAILED : Clearing and Verifying CP DP stats"
        ixNetStopTrafficAndCleanup $traffic
        return $FAILED
    }

   log "Enabling OSPFv2 Route Range on port2"


    set count 1
    while {$count < 4} {
        set routerange($count) [subst \
        {::ixNet::OBJ-/vport:2/protocols/ospf/router:1/routeRange:$count}]
        log "$routerange($count)"
        if {[setAndCheckAttributeValue $routerange($count) "enabled" \
           {"true" y}] == 1} {
           log "FAILURE :Enabling OSPFV2 Route Range$count failed"
           ixNetStopTrafficAndCleanup $traffic
           return $FAILED
        }
        incr count
    }
    log "SUCCESS :Enabled OSPFV2 Route Range"
    log "Waiting for 10 seconds"
    after 10000
    log "Checking  Flow Statistics for CP specific stats"

    #-----------------------------------------------------------------------------------
    # Verifying CP stats
    #-----------------------------------------------------------------------------------
    set startTSFlow1 [verifyCpStats $caption $DestinationIPList 3000000000 \
       ospfEnableRR StartTSFirstFlow]
    if {$startTSFlow1 == 1} {
       log "FAILED : Verifiying CP stats after Enabling OSPFv2 RR"
       ixNetStopTrafficAndCleanup $traffic
       return $FAILED
    } else {
       log "SUCCESS : Verifiying CP stats after Enabling OSPFv2 RR"
    }

    log "Verifying CP START TS of Flow1 for Enable Event and End TS of \
         Flow3 for Disable Event"
    log "CP START TS of Flow1 for Enable Event :: $startTSFlow1"
    log "End TS of Flow3 for Disable Event :: $EndTSFlow3"

    if {$startTSFlow1 > $EndTSFlow3} {
       log "CP START TS of Flow1 for Enable Event is greater than End TS \
           of Flow3 for Disable Event"
    } else {
       log "CP START TS of Flow1 for Enable Event is less than End TS of \
           Flow3 for Disable Event"
       ixNetStopTrafficAndCleanup $traffic
       return $FAILED
    }
    log "SUCCESS : Verification of CP specific Statistics is successful"

    #---------------------------------------------------------------------------
    # Stop the porotocl and traffic
    #---------------------------------------------------------------------------
    log "stopping protocol"
    ixNet exec stop ::ixNet::OBJ-/vport:1/protocols/ospf
    ixNet exec stop ::ixNet::OBJ-/vport:2/protocols/ospf
    if {[ixNetStopTrafficAndCleanup $traffic] == 0} {
     log "Traffic was stopped succesfully"
        return $PASSED
    } else {
    log "Stopping traffic failed"
        return $FAILED
    }
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action

