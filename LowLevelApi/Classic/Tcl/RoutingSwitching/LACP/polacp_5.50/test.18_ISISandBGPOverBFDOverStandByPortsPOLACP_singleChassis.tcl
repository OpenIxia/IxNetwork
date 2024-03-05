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

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#-------------------------------------------------------------------------------
# Name       : test.18_ISISandBGPOverBFDOverStandByPortsPOLACP_singleChassis.tcl
# Purpose        : To Verify ISIS and BGP protocol over BFD over Stand By ports
# Topology       : 8 ports on single chassis.Having PoLACP configuration such
#                  that each LAG has 4 member ports.
# Verification   : Verify ISIS and BGP stats when Ports are made Stand_By.
#
# Config Format  : ixncfg used
#-------------------------------------------------------------------------------

package req IxTclNetwork

proc Action {testPortConnElement} {
    source [pwd]/LACP_Utils.tcl
    
    # initialize return value
    set FAILED 1
    set PASSED 0

    set numClient 0
    set numCLientList {}
    foreach portDataList $testPortConnElement {
        incr numClient

        log "Get real card/port from portDataList $portDataList"
        set index 0
        foreach portData $portDataList {
            log "portData $portData"
            incr index
            set [subst chassisIp$index]  [lindex $portData 0]
            set [subst card$index]       [lindex $portData 1]
            set [subst port$index]       [lindex $portData 2]
            set [subst hostNameIs$index] [lindex $portData 3]
        }

        set [subst hostName$numClient] [subst $[subst hostNameIs$index]]
        lappend numCLientList [subst $[subst hostName$numClient]]
        puts "[subst hostName$numClient] [subst $[subst hostNameIs$index]]"
        set numPorts $index

        # Hostname, where IxNetwork TCL-Server client runs
        log "connecting to Client [subst $[subst hostName$numClient]] ..."
        set tclPublisherVersion "5.40"
        set client [lindex [split [subst $[subst hostName$numClient]] :] 0]
        set port   [lindex [split [subst $[subst hostName$numClient]] :] 1]
        set connection_Result [ixNet connect $client -port $port -version 5.50]
        log "Connection Result: $connection_Result"

        if {[string equal $connection_Result "::ixNet::OK"] != 1} {
            log "connection to client unsuccessful"
            return $FAILED
        }
        log "connectToSpecClient Successful"

        # clean up all the existing configurations from client
        log "cleaning up the client"
        ixNetCleanUp
        after 2000

        # load config files
        set configFileName \
        config.18_ISISandBGPOverBFDOverStandByPortsPOLACP_singleChassis.ixncfg

        if  {[ixNet exec loadConfig [ixNet readFrom [pwd]/$configFileName]] !=\
            "::ixNet::OK"} {
            log "Loading IxNetwork config file : Failed "

            return $FAILED
        }
        log "Loading IxNetwork config file : Passed"

        # getting the real port list
        set realPortsList {}
        for {set index 1} {$index <= $numPorts} {incr index} {
            set realPorts [list [subst $[subst chassisIp$index]] \
                  [subst $[subst card$index]] [subst $[subst port$index]]]
            lappend realPortsList $realPorts
        }
        set [subst realPortsList$numClient] $realPortsList
        log "realPortsList [subst $[subst realPortsList$numClient]]"

        # Get virtual ports
        log "getting virtual ports ...."
        set vPorts      [ixNet getList [ixNet getRoot] vport]
        for {set index 1} {$index <= $numPorts} {incr index} {
            set [subst vPort$index]  [lindex $vPorts [expr $index -1]]
        }
        log "Virtual ports are = $vPorts"

        # Assign real ports to virtual ports
        log "Assign virtual ports to real ports ..."
        set force true
        set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
        log "Assigned: $status"
        for {set index 1} {$index <= $numPorts} {incr index} {
            if {[string equal [lindex $status [expr $index -1]]  \
                [subst $[subst vPort$index]]] != 1} {

                return $FAILED
            }
        }
        ixTclNet::CheckLinkState $vPorts doneList
        after 2000

        log "Starting protocol LACP..."
        for {set index 1} {$index <= $numPorts} {incr index} {
            if {[ixNet exec start [subst $[subst vPort$index]]/protocols/lacp] \
                != "::ixNet::OK"} {
                log "Failed to start protocol LACP..."

                return $FAILED
            }
        }
    } ;#foreach portDataList $testPortConnElement

    # Start Protocols
    # Wait for some time LAG formation
    after 30000

    set tclPublisherVersion "5.40"

    # Verify learned info which initially should have 2 user-defined and
    # operational LAGs.
    # All the ports should show aggregation status as Aggregated.
    # All Ports should show other member count 1 and other member
    # details as its pair connected port.


    # Verify stats of all the ports sholuld show Configured Members
    # and UP members as 2.
    log  "Verifying LACP stats ..."
    set LacpStatsList {"Link State"            "UP" \
                       "Total LAG Member Ports"   2 \
                       "LAG Member Ports UP"      2}

    set portList $realPortsList

    if {[checkAllProtocolStats $portList   \
              "LACP Aggregated Statistics" \
               $LacpStatsList]} {
        log  "Did not get the expected LACP stats value..."

        return $FAILED
    }
    log "Got expected LACP stats values..."

    log "Verifying LACP learnt infos..."
    set checkLearntInfoList {\
            {actorSyncFlag                                    \
            partnerSyncFlag                                   \
            enabledAggregation                                \
            actorLinkAggregationStatus                        \
            partnerLinkAggregationStatus                      \
            otherLagMemberCount }                             \
            {{inSync inSync true aggregatable aggregatable 1}}}

    for {set index 0} {$index <= 3} {incr index} {
        set lacp [subst [lindex \
            [ixNet getList [ixNet getRoot] vport] $index]]]/protocols/lacp

        if {[verifyLacpLearnedInfo $lacp $checkLearntInfoList]} {
            log "Did not get the expected LACP learnt infos..."
            # ixNetCleanUpAllClients $numCLientList $tclPublisherVersion
            return $FAILED
        }
        log "Got expected LACP learnt infos..."
    }

    log "Starting BFD Protocol..."
    for {set index 1} {$index <= 2} {incr index} {
        log "Starting BFD on  [subst $[subst vPort$index]]"
        if {[ixNet exec start [subst $[subst vPort$index]]/protocols/bfd] \
            != "::ixNet::OK"} {
            log "Failed to start protocol BFD ..."

            return $FAILED
        }
    }

    for {set index 5} {$index <= 6} {incr index} {
        log "Starting BFD on  [subst $[subst vPort$index]]"
        if {[ixNet exec start [subst $[subst vPort$index]]/protocols/bfd] \
            != "::ixNet::OK"} {
            log "Failed to start protocol BFD ..."

            return $FAILED
        }
    }
    log "BFD Started successfully"


    log "Waiting for 10 seconds to get BFD UP"
    after 10000

    # Verify learned info which initially should have 2 user-defined and
    # operational LAGs. All the ports should show aggregation status as
    # Aggregated. Port1/3/5 should show other member count 2 and other
    # member details as each other, similarly port2/4/6 should show
    # other member count as 2 and other member details as each other.

    # Verify stats of all the ports sholuld show Configured Members
    # and UP members as 3.
    set BfdStatsList {"Routers Configured" 1 \
                      "Routers Running"    1}

    log "Verifying BFD stats ..."
    set portLists $realPortsList

    for {set index 0} {$index <= 1} {incr index} {
        set portList [list [subst [lindex $portLists $index]]]
        if {[checkAllProtocolStats $portList
                  "BFD Aggregated Statistics" \
                   $BfdStatsLisl]} {
            log "Did not get the expected BFD stats value..."
            return $FAILED
        }
    }

    for {set index 4} {$index <= 5} {incr index} {
        set portList [list [subst [lindex $portLists $index]]]
        if {[checkAllProtocolStats $portList
                  "BFD Aggregated Statistics" \
                  $BfdStatsList]} {
            log "Did not get the expected BFD stats value..."
            return $FAILED
        }
    }

    log "Got expected BFD stats values..."

    #starting ISIS and BGP
    # Starting ISIS
    for {set index 1} {$index <= 2} {incr index} {
        log "Starting ISIS on  [subst $[subst vPort$index]]"
        if {[ixNet exec start [subst $[subst vPort$index]]/protocols/isis] !=\
            "::ixNet::OK"} {
            log "Failed to start protocol ISIS ..."

            return $FAILED
        }
    }
    log "ISIS Started successfully"
    # Starting BGP
    for {set index 5} {$index <= 6} {incr index} {
        log "Starting BGP on  [subst $[subst vPort$index]]"
        if {[ixNet exec start [subst $[subst vPort$index]]/protocols/bgp] !=\
            "::ixNet::OK"} {
            log "Failed to start protocol BFD ..."

            return $FAILED
        }
    }
    log "BGP Started successfully"

    log "Waiting for 60 seconds for ISIS and BGP to get UP"
    after 60000
    set BgpStatsList {"Sess. Configured"   1 \
                      "Sess. Up"           1 \
                      "Session Flap Count" 0}

    set IsisStatsList {"L2 Sess. Configured"   1 \
                       "L2 Sess. Up"           1 \
                       "L2 Full State Count"   1 \
                       "L2 Neighbors"          1 \
                       "L2 Session Flap Count" 0}

    #Verifying BGP and ISIS protocol stats
    #set portLists $realPortsList
    log "Verifying ISIS protocol stats"
    for {set index 0} {$index <= 1} {incr index} {
         set portList [list [subst [lindex $portLists $index]]]
         if {[checkAllProtocolStats $portList \
                   "ISIS Aggregated Statistics" \
                    $IsisStatsList]} {
            log "Did not get the expected ISIS stats value..."

            return $FAILED
         }
    }
    log "Got expected ISIS stats values..."

    log "Verifying BGP protocol stats"
    for {set index 4} {$index <= 5} {incr index} {
         set portList [list [subst [lindex $portLists $index]]]
         if {[checkAllProtocolStats $portList \
                   "BGP Aggregated Statistics" \
                    $BgpStatsList]} {
            log "Did not get the expected BGP stats value..."
            return $FAILED
         }
    }
    log "Got expected BGP stats values..."

    #Disabling Sync flag on port1 and port5
    log "Disabling Sync flag on port1 and port5"
    set p1 [lindex [ixNet getList [ixNet getRoot] vport] 0]
    set p5 [lindex [ixNet getList [ixNet getRoot] vport] 4]

    set lacp1 $p1/protocols/lacp
    set lacp5 $p5/protocols/lacp

    set link1 [lindex [ixNet getList $lacp1 link] 0]
    set link5 [lindex [ixNet getList $lacp5 link] 0]

    if {[setAndCheckAttributeValue $link1 "syncFlag" {"disable" y }] == 1} {
        ixNetCleanUpAllClients $numCLientList $tclPublisherVersion
        return $FAILED
    }

    log "Send Update Status.."

    if {[string first "::ixNet::OK" [ixNet exec sendUpdate $lacp1]] == -1} {
        log "Send Update Status unsuccessful !!!"
        #ixNetCleanUp $numCLientList $tclPublisherVersion
        return $FAILED
    }

    if {[setAndCheckAttributeValue $link5 "syncFlag" {"disable" y }] == 1} {
        ixNetCleanUpAllClients $numCLientList $tclPublisherVersion
        return $FAILED
    }

    log "Send Update Status.."

    if {[string first "::ixNet::OK" [ixNet exec sendUpdate $lacp5]] == -1} {
        log "Send Update Status unsuccessful !!!"
        #ixNetCleanUp $numCLientList $tclPublisherVersion
        return $FAILED
    }

    log "Waiting for 60 Sec "
    after 60000

    # Once the port is made standby learned info should show aggregation
    # status of port1, port2,port5 and port6 as "Not Aggregated".
    # Other member count and details should not change for any ports.
    # Also user-defined and operational LAG count should not change.

    log "Verifying LACP learnt infos..."
    set checkLearntInfoList1             \
          {{actorSyncFlag                \
            partnerSyncFlag              \
            enabledAggregation           \
            actorLinkAggregationStatus   \
            partnerLinkAggregationStatus \
            otherLagMemberCount }        \
          {{outOfSync inSync false aggregatable aggregatable 1}}}

    set checkLearntInfoList2             \
          {{actorSyncFlag                \
            partnerSyncFlag              \
            enabledAggregation           \
            actorLinkAggregationStatus   \
            partnerLinkAggregationStatus \
            otherLagMemberCount }        \
          {{inSync outOfSync false aggregatable aggregatable 1}}}

    for {set index 0} {$index <= 7} {incr index} {
        set lacp [subst [lindex [ixNet getList \
            [ixNet getRoot] vport] $index]]]/protocols/lacp

        if {$index == 0 || $index == 4} {

             if {[verifyLacpLearnedInfo $lacp $checkLearntInfoList1]} {
                log "Did not get the expected LACP learnt infos for \
                    [subst $[subst vPort$index]]..."
                return $FAILED
             }
             log "Got expected LACP learnt infos for \
                  [subst $[subst vPort[expr $index+1]]]"

         } else {

            if {$index == 1 || $index == 5} {
                if {[verifyLacpLearnedInfo $lacp $checkLearntInfoList2]} {
                    log "Did not get the expected LACP learnt infos for \
                        [subst $[subst vPort[expr $index+1]]]"
                    return $FAILED
                }
                log "Got expected LACP learnt infos for \
                     [subst $[subst vPort[expr $index+1]]]"
            } else {
                if {[verifyLacpLearnedInfo $lacp $checkLearntInfoList]} {
                    log "Did not get the expected LACP learnt infos for \
                        [subst $[subst vPort[expr $index+1]]]"
                    return $FAILED
                }
                log "Got expected LACP learnt infos for \
                    [subst $[subst vPort[expr $index+1]]]"
            }

        }
    }

    set LacpStatsList1 {"Link State"          "UP" \
                        "Total LAG Member Ports" 2 \
                        "LAG Member Ports UP"    1}

    set LacpStatsList2 {"Link State"            "DOWN" \
                        "Total LAG Member Ports"     2 \
                        "LAG Member Ports UP"        1}

    log "Verifying LACP stats ..."
    for {set index 0} {$index <= 7} {incr index} {

        set portList [list [subst [lindex $portLists $index]]]
        if {$index ==0 || $index ==1 || $index ==4 || $index ==5} {
            if {[checkAllProtocolStats $portList \
                      "LACP Aggregated Statistics" \
                       $LacpStatsList2 1 $tclPublisherVersion]} {
                log "Did not get the expected LACP stats value..."
                # ixNetCleanUpAllClients $numCLientList $tclPublisherVersion
                return $FAILED
            }
        } else {
             if {[checkAllProtocolStats $portList \
                      "LACP Aggregated Statistics" \
                       $LacpStatsList1 1 $tclPublisherVersion]} {
                log "Did not get the expected LACP stats value..."
                # ixNetCleanUpAllClients $numCLientList $tclPublisherVersion
                return $FAILED
            }
        }

    }
    log "Got expected LACP stats values..."


    # Verifying BGP and ISIS protocol stats after Making port1
    # and port5 as STANDBY
    log "Verifying ISIS protocol stats"
    for {set index 0} {$index <= 1} {incr index} {
         set portList [list [subst [lindex $portLists $index]]]
         if {[checkAllProtocolStats \
                  $portList \
                  "ISIS Aggregated Statistics" \
                   $IsisStatsList]} {
            log "Did not get the expected ISIS stats value..."

            return $FAILED
         }
    }
    log "Got expected ISIS stats values..."
    log "Verifying BGP protocol stats"

    for {set index 4} {$index <= 5} {incr index} {
         set portList [list [subst [lindex $portLists $index]]]
         if {[checkAllProtocolStats \
                   $portList \
                   "BGP Aggregated Statistics" \
                    $BgpStatsList]} {
            log "Did not get the expected BGP stats value..."

            return $FAILED
         }
    }
    log "Got expected BGP stats values..."


    # Once LAG has formed and all the ports are showing aggregation
    # status as Aggregated,
    # uncheck the sync flag of port 3 such that it becomes STANDBY.

    # Once the port is made standby learned info should show aggregation
    # status of port3 and 4
    # "Not Aggregated". Other member cound and details should
    # not change for any ports.
    # Also user-defined and operational LAG count should not change.

    # Verify stats of all the ports sholuld now show Configured
    # Members as 3 and UP members as 2.

    # Cleanup

    return $PASSED
}


set testPortConnElement {{{xm12-3 11 3 loopback:8009} \
                          {xm12-3 11 4 loopback:8009} \
                          {xm12-3 11 5 loopback:8009} \
                          {xm12-3 11 6 loopback:8009} \
                          {xm12-3 11 7 loopback:8009} \
                          {xm12-3 11 8 loopback:8009} \
                          {xm12-3 11 9 loopback:8009} \
                          {xm12-3 11 10 loopback:8009}}}

Action $testPortConnElement