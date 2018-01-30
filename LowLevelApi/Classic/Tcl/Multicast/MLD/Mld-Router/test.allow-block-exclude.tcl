#!/usr/local/bin/tclsh

#---------------------------------------------------------------------------
# This script automates 2 test cases
#
#
# let set A = 2001::1, 2001::2 2001::3 2001::4
# let set B = 2001::3, 2001::4 2001::5 2001::6
# Configure a host with group G with source address set A and
# mode exclude on port 2. Configure a MLDv2 router on port 1.
# Start MLDv2 router on port1. Start host on port2.
# Check learned info on port1
#
#
# let set A = 2001::1, 2001::2 2001::3 2001::4
# let set B = 2001::3, 2001::4 2001::5 2001::6
# Configure a host with group G with source address set A and
# mode exclude on port 2. Configure a MLDv2 router on port 1.
# Start MLDv2 router on port1. Start host on port2.
# Check learned info on port1.
# Wait for 10 seconds
# Change the source address of group G on port 2 with address set B
# Update the changed info.
#
#---------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

#----------------------------------------------------------------------------
# PROCDURE     : getMldLearnedInfo
# PURPOSE      : To retrive the learned info object from mld querier.
# PARAMETERS   : The object referance of mld querier.
# RETURN VALUE : the list of learned object-ref.
#----------------------------------------------------------------------------
proc getMldLearnedInfo {mldRtr} {
    set isComplete false
    set count 0

    # Request LearnedInfo
    if {[catch {set retVal [ixNet exec refreshLearnedInfo $mldRtr]} error]} {
        puts "Error in retriving learned info: $error"
        return ""
    }

    while {$isComplete != true} {
        flush stdout
        set isComplete [ixNet getAttr $mldRtr -isRefreshComplete]
        puts "isComplete = $isComplete"
        after 1000
        incr count

        if {$count > 10} {
            puts "Could not retrieve learnt info on \
                 $protocolName querier : $protocolName Router, ... timeout"
            return ""
        }
    }

    set learntList [ixNet getList $mldRtr learnedGroupInfo]
    return $learntList
}


#--------------------------------------------------------------------------
# PROCEDURE : printLearnedInfo
# PURPOSE   : retriving the group timers from learned info for a given
#             group
#--------------------------------------------------------------------------
proc printLearnedInfo {learnedList} {
    set none {}
    if {[llength $learnedList] > 0} {
        foreach learntinfo $learnedList {
            puts "Group Addr :: [::ixNet getAttribute \
                 $learntinfo -groupAddress]"

            puts "Group Timer:: [::ixNet getAttribute \
                 $learntinfo -groupTimer]"

            puts "Group Mode :: [::ixNet getAttribute \
                 $learntinfo -filterMode]"

            puts "Src Addr   :: [::ixNet getAttribute \
                 $learntinfo -sourceAddress]"

            puts "Src Timer  :: [::ixNet getAttribute \
                 $learntinfo -sourceTimer]"
        }
    } else {
        return $none
    }
    return $none
}


#--------------------------------------------------------------------------
# PROCEDURE : retriveLearnedGrpSrc
# PURPOSE   : retriving the group timers from learned info for a given
#             group and source
#--------------------------------------------------------------------------
proc retriveLearnedGrpSrc {learnedList grp src} {

    set none {}
    if {[llength $learnedList] > 0} {
        foreach learntinfo $learnedList {
            set grpAddr [::ixNet getAttribute $learntinfo -groupAddress]
            if {$grpAddr == $grp} {
                set grpAddr    [::ixNet getAttribute  \
                               $learntinfo -groupAddress]

                set grpTimer   [::ixNet getAttribute  \
                               $learntinfo -groupTimer]

                set grpMode    [::ixNet getAttribute  \
                               $learntinfo -filterMode]

                set sourceAddr [::ixNet getAttribute  \
                               $learntinfo -sourceAddress]

                set srcTimer   [::ixNet getAttribute  \
                               $learntinfo -sourceTimer]
                if {$sourceAddr == $src} {
                    puts "$learntinfo"
                    return $learntinfo
                }
            } ;# end if ($grpAddr == $grp)
        } ;# end foreach
    } else {
        return $none
    }
    return $none
}


#----------------------------------------------------------------------------
# PROCEDURE : verifyCapture
# PURPOSE   : To capture a specific pattern or packet from capture buffer
#             and to find the number of occurences.
#----------------------------------------------------------------------------
proc verifyCapture {ch card port pattern {expCnt 1}} {

     puts "Initilizing thorugh IxTclHal...."
     ixInitialize $ch

     puts "Getting port-2"
     port get 1 $card $port

     puts "Getting the ownership details..."
     set putsinName [port cget -owner]

     puts "Logging in using the $putsinName"
     ixLogin $putsinName

     captureBuffer get 1 $card $port
     puts "Checking the number of captured packets.."
     set numRxPackets [captureBuffer cget -numFrames]
     puts "Total number of packets are $numRxPackets"

     captureBuffer get 1 $card $port 1 $numRxPackets
     set cnt 0

     for {set i 1} {$i <= $numRxPackets} {incr i} {
         captureBuffer getframe $i
         set capFrame [captureBuffer cget -frame]
         if {[regexp -nocase "$pattern" $capFrame match]} {
             incr cnt
         } else {
             # puts "not matching :- $capFrame"
         }
     }
     return $cnt
}


proc Action {portData1 portData2} {
    set PASSED 0
    set FAILED 1

   # initialize return value
    set FAILED 1
    set PASSED 0

    # get port info 1
    set chassisIp1 [lindex $portData1 0]
    set card1      [lindex $portData1 1]
    set port1      [lindex $portData1 2]
    set client1    [lindex $portData1 3]
    set tcpPort1   [lindex $portData1 4]

    # get port info 2
    set chassisIp2 [lindex $portData2 0]
    set card2      [lindex $portData2 1]
    set port2      [lindex $portData2 2]
    set client2    [lindex $portData2 3]
    set tcpPort2   [lindex $portData2 4]

    if {$client1 == $client2} {
       set status ""
       puts "Connecting to client $client1"
       if {[catch {set status [ixNet connect $client1 -port \
           $tcpPort1]} error]} {
           puts "Unable to connect to ixNetwork"
           return $FAILED
       }

       if {[string equal $status "::ixNet::OK"] != 1} {
           puts "connection to client unsuccessful"
           return $FAILED
       }

    } else {

       puts "Try to use the same client"
       return $FAILED
    }

    # clean up all the existing configurations from client
    puts "cleaning up the client"
    ixNetCleanUp
    puts "Executing from [pwd]"

    # Now we configure the first Ixia port
    puts "Now we configure the first Ixia port from the script-gen file"
    if {[catch {source "$::pwd/config.allow-block-exclude.tcl"} error] } {
       puts "Error in sourcing the file ./config.allow-block-exclude.tcl"
       puts "$error"
       return $FAILED
    }

    # get the virtual port list
    puts "getting virtual ports ...."
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]
    puts "Virtual ports are = $vPorts"

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1]\
       [list $chassisIp2 $card2 $port2] ]

    # Assign virtual ports to real ports
    puts "Assign virtual ports to real ports ..."
    set force true
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    ixNet commit
    puts "Assigned: $status"

    if {[string equal [lindex $status 0] $vPort1] != 1 || \
       [string equal [lindex $status 1] $vPort2] != 1} {
       ixNetCleanUp
       return $flag
    }
    ixTclNet::CheckLinkState $vPorts doneList

    # Get MLD querier
    set root   [ixNet getRoot]
    set vport1 [lindex [ixNet getList $root vport] 0]
    set mld1   $vport1/protocols/mld
    set mldRtr [lindex [ixNet getList $mld1 querier] 0]

    # Get MLD  host
    set vport2 [lindex [ixNet getList $root vport] 1]
    set mld2 $vport2/protocols/mld

    # get MLD group range
    set mldHost1 [lindex [ixNet getList $mld2 host] 0]
    set mldHost1Grp1 [lindex [ixNet getList $mldHost1 groupRange] 0]

    # get MLD sources
    set mldHost1Grp1Src(1) [lindex [ixNet getList $mldHost1Grp1  sourceRange] 0]
    set mldHost1Grp1Src(2) [lindex [ixNet getList $mldHost1Grp1  sourceRange] 1]
    set mldHost1Grp1Src(3) [lindex [ixNet getList $mldHost1Grp1  sourceRange] 2]
    set mldHost1Grp1Src(4) [lindex [ixNet getList $mldHost1Grp1  sourceRange] 3]

    # Enable packet capture
    ixNet setAttribute $vport1/capture -softwareEnabled true
    ixNet setAttribute $vport1/capture -hardwareEnabled true
    ixNet setAttribute $vport2/capture -softwareEnabled true
    ixNet setAttribute $vport2/capture -hardwareEnabled true
    ixNet commit

    puts "Mldv1 querier started on port1"
    ixNet exec start $mld1

    puts "wait for 5 sec"
    after 5000

    puts "Mldv1 host started on port2"
    ixNet exec start $mld2

    puts "Wait for 10 sec Necessery"
    after 10000

    set learnedInfo [getMldLearnedInfo $mldRtr]
    printLearnedInfo $learnedInfo

    #---------------------------------------------------------------------------
    # Source timer for the sources 2001:0:0:0:0:0:0:1 to 2001:0:0:0:0:0:0:4
    # should be set to 0
    # group timer value should be 130
    #---------------------------------------------------------------------------
    puts "for the group source 2001::1 2001::2 2001::3 2001::4 "
    foreach i {1 2 3 4} {
         set learnedInfoTemp [retriveLearnedGrpSrc $learnedInfo  \
             "FF03:0:0:0:0:0:0:14"  "2001:0:0:0:0:0:0:$i"]

         if {[llength $learnedInfoTemp] == 0} {
             puts "No learned info retrived !!"
             ixNetCleanUp
             return $FAILED
         }

         set grpMode  [ixNet getAttr $learnedInfoTemp -filterMode]
         set srcTimer [ixNet getAttr $learnedInfoTemp -sourceTimer]

         if {$grpMode != "exclude"} {
             puts "group mode did not matched for 2001:0:0:0:0:0:0:$i"
             puts "Expected exclude got $grpMode"
             ixNetCleanUp
             return $FAILED
         }

         # source timer should be set to 130 consider 5 sec tolerance
         if {$srcTimer != 0} {
             puts "source timer for 2001:0:0:0:0:0:0:$i is not set properly"
             puts "Expected at least >= 115 got $srcTimer"
             ixNetCleanUp
             return $FAILED
         }

         set groupTimer [ixNet getAttr $learnedInfoTemp -groupTimer]
         if {$groupTimer < 120} {
             puts "source timer for 2001:0:0:0:0:0:0:$i is not set properly"
             ixNetCleanUp
             return $FAILED
         }
    }

    # now change the groups
    puts "Changing sources"
    set ctr 1
    foreach val {3 4 5 6} {
        ixNet setAttr $mldHost1Grp1Src($ctr) -ipFrom "2001:0:0:0:0:0:0:$val"
        ixNet commit
        incr ctr
    }

    puts "Updating sources"
    ixNet exec updateSource $mldHost1Grp1

    puts "wait for 5 sec"
    after 5000

    set learnedInfo [getMldLearnedInfo $mldRtr]
    printLearnedInfo $learnedInfo

    #---------------------------------------------------------------------------
    # Source timer for the sources 2001:0:0:0:0:0:0:1 and 2001:0:0:0:0:0:0:2
    # should be set to 135
    #---------------------------------------------------------------------------
    puts "Retriving source timer for 2001:0:0:0:0:0:0:1 ..."
    set learnedInfoTemp [retriveLearnedGrpSrc $learnedInfo  \
                        "FF03:0:0:0:0:0:0:14" "2001:0:0:0:0:0:0:1"]

    if {[llength $learnedInfoTemp] == 0} {
        puts "No learned info retrived !!"
        ixNetCleanUp
        return $FAILED
    }

    puts "source Timer of the deleted group will be set to 130 sec"
    set sourceTimer [::ixNet getAttribute $learnedInfoTemp -sourceTimer]

    # Source timer should be set to 135 sec. Over and above that consider
    # some tolerance such as delay for retriving learned info, other
    # processiong delays. Lets wait for something greater than 120
    if {($sourceTimer < 120) || ($sourceTimer > 135)} {
        puts "source timer for the src/group 2001:0:0:0:0:0:0:1/ \
            FF03:0:0:0:0:0:0:14 is not set properly"
        ixNetcleanUp
        return $FAILED
    }
    puts "Source timer check for source 2001:0:0:0:0:0:0:1 passed"

    puts "Retriving source timer for 2001:0:0:0:0:0:0:1 ..."
    set learnedInfoTemp [retriveLearnedGrpSrc $learnedInfo  \
                        "FF03:0:0:0:0:0:0:14" "2001:0:0:0:0:0:0:2"]

    if {[llength $learnedInfoTemp] == 0} {
        puts "No learned info retrived !!"
        ixNetCleanUp
        return $FAILED
    }

    puts "source Timer of the deleted group will be set to 130 sec"
    set sourceTimer [::ixNet getAttribute $learnedInfoTemp -sourceTimer]

    # Source timer should be set to 135 sec. Over and above that consider
    # some tolerance such as delay for retriving learned info, other
    # processiong delays. Lets wait for something greater than 120
    if {($sourceTimer < 120) || ($sourceTimer > 135)} {
        puts "source timer for the src/group 2001:0:0:0:0:0:0:2/\
            FF03:0:0:0:0:0:0:14 is not set properly"
        ixNetcleanUp
        return $FAILED
    }
    puts "Source timer check for source 2001:0:0:0:0:0:0:2 passed"

    #--------------------------------------------------------------------------
    # Source timer for the sources 2001:0:0:0:0:0:0:3 and 2001:0:0:0:0:0:0:4
    # should remain unchanged and should be 0
    #--------------------------------------------------------------------------
    puts "There shall be sources 2001::3 2001::4 will remain unchanged (0)"
    foreach i {3 4} {
         set learnedInfoTemp [retriveLearnedGrpSrc $learnedInfo  \
             "FF03:0:0:0:0:0:0:14"  "2001:0:0:0:0:0:0:$i"]

         if {[llength $learnedInfoTemp] == 0} {
             puts "No learned info retrived !!"
             ixNetCleanUp
             return $FAILED
         }

         set grpMode  [ixNet getAttr $learnedInfoTemp -filterMode]
         set srcTimer [ixNet getAttr $learnedInfoTemp -sourceTimer]

         if {$grpMode != "exclude"} {
             puts "group mode did not matched for 2001:0:0:0:0:0:0:$i"
             puts "Expected exclude got $grpMode"
             ixNetCleanUp
             return $FAILED
         }

         # source timer for the groups 2001::3 and 2001::4 should be set to 0
         if {$srcTimer != 0} {
             puts "source timer for 2001:0:0:0:0:0:0:$i is not set properly"
             puts "Expected 0 got $srcTimer"
             ixNetCleanUp
             return $FAILED
         }
    }
    puts "Source timer check for source 2001:0:0:0:0:0:0:3  \
          2001:0:0:0:0:0:0:4 passed"

    #---------------------------------------------------------------------------
    # Source timer for the sources 2001:0:0:0:0:0:0:5 and 2001:0:0:0:0:0:0:6
    # should and should be set to 20
    #---------------------------------------------------------------------------
    puts "source timer of  2001:0:0:0:0:0:0:5 and 2001:0:0:0:0:0:0:6 will be \
         set to 20"

    foreach i {5 6} {
         set learnedInfoTemp [retriveLearnedGrpSrc $learnedInfo  \
             "FF03:0:0:0:0:0:0:14"  "2001:0:0:0:0:0:0:$i"]

         if {[llength $learnedInfoTemp] == 0} {
             puts "No learned info retrived !!"
             ixNetCleanUp
             return $FAILED
         }

         set grpMode  [ixNet getAttr $learnedInfoTemp -filterMode]
         set srcTimer [ixNet getAttr $learnedInfoTemp -sourceTimer]

         if {$grpMode != "exclude"} {
             puts "group mode did not matched for 2001:0:0:0:0:0:0:$i"
             puts "Expected exclude got $grpMode"
             ixNetCleanUp
             return $FAILED
         }

         # source timer should be set to 20 consider some tolerance
         # due to other processing delays
         if {($srcTimer < 10) || ($srcTimer > 20)} {
             puts "source timer for 2001:0:0:0:0:0:0:$i is not set properly"
             puts "Expected at least >= 10 got $srcTimer"
             ixNetCleanUp
             return $FAILED
         }
    }
    puts "Source timer check for source 2001:0:0:0:0:0:0:5  \
          2001:0:0:0:0:0:0:6 passed"

    # waiting for hard-coaded 20 sec because. Specific query response interval
    # == 5 sec and specific query transmission count = 4. So 4 * 5 = 20 sec
    # is the max wait time for source timer to expire for 2001::1 and 2001::2
    puts "Wait for 25 sec for  2001:0:0:0:0:0:0:5 and 2001:0:0:0:0:0:0:6 for \
         source timer to be 0"
    after 25000

    set learnedInfo [getMldLearnedInfo $mldRtr]
    printLearnedInfo $learnedInfo

    #---------------------------------------------------------------------------
    # Source timer for the all the sources except 2001::1 and 2002::2
    # should and should be set 0
    #---------------------------------------------------------------------------
    foreach i {3 4 5 6} {
         set learnedInfoTemp [retriveLearnedGrpSrc $learnedInfo  \
             "FF03:0:0:0:0:0:0:14"  "2001:0:0:0:0:0:0:$i"]
         set grpMode  [ixNet getAttr $learnedInfoTemp -filterMode]
         set srcTimer [ixNet getAttr $learnedInfoTemp -sourceTimer]

         if {[llength $learnedInfoTemp] == 0} {
             puts "No learned info retrived !!"
             ixNetCleanUp
             return $FAILED
         }

         if {$grpMode != "exclude"} {
             puts "group mode did not matched for 2001:0:0:0:0:0:0:$i"
             puts "Expected exclude got $grpMode"
             ixNetCleanUp
             return $FAILED
         }

         # source timer should be set to 0
         if {$srcTimer != 0} {
             puts "source timer for 2001:0:0:0:0:0:0:$i is not set properly"
             puts "Expected 0 got $srcTimer"
             ixNetCleanUp
             return $FAILED
         }
    }
    puts "Source timer check for 2001:0:0:0:0:0:0:3 to 2001:0:0:0:0:0:0:6 passed"

    #---------------------------------------------------------------------------
    # Source timer for the sources except 2001::1 and 2002::2 will be a
    # non zero value
    #---------------------------------------------------------------------------
    foreach i {1 2} {
         set learnedInfoTemp [retriveLearnedGrpSrc $learnedInfo  \
             "FF03:0:0:0:0:0:0:14"  "2001:0:0:0:0:0:0:$i"]

         if {[llength $learnedInfoTemp] == 0} {
             puts "No learned info retrived !!"
             ixNetCleanUp
             return $FAILED
         }

         set grpMode  [ixNet getAttr $learnedInfoTemp -filterMode]
         set srcTimer [ixNet getAttr $learnedInfoTemp -sourceTimer]

         if {$grpMode != "exclude"} {
             puts "group mode did not matched for 2001:0:0:0:0:0:0:$i"
             puts "Expected exclude got $grpMode"
             ixNetCleanUp
             return $FAILED
         }

         # source timer should be greater than 90 (considering other processing
         # delays and tolerance
         if {$srcTimer < 90} {
             puts "source timer for 2001:0:0:0:0:0:0:$i is not set properly"
             puts "Expected > 90 got $srcTimer"
             ixNetCleanUp
             return $FAILED
         }
    }
    puts "Source timer check for 2001:0:0:0:0:0:0:1 and 2001:0:0:0:0:0:0:2 passed"


    puts "Now wait for a generic querry/report conversation to happen"
    after 90000

    set learnedInfo [getMldLearnedInfo $mldRtr]
    printLearnedInfo $learnedInfo

    #---------------------------------------------------------------------------
    # Source timer for the all the sources 2001::3 to 2002::6
    # should and should be set 0
    #---------------------------------------------------------------------------
    puts "All other sources should be there 2001::3 2001::4 2001::5 2001::6"
    foreach i {3 4 5 6} {
         set learnedInfoTemp [retriveLearnedGrpSrc $learnedInfo  \
             "FF03:0:0:0:0:0:0:14"  "2001:0:0:0:0:0:0:$i"]

         if {[llength $learnedInfoTemp] == 0} {
             puts "No learned info retrived !!"
             ixNetCleanUp
             return $FAILED
         }

         set grpMode  [ixNet getAttr $learnedInfoTemp -filterMode]
         set srcTimer [ixNet getAttr $learnedInfoTemp -sourceTimer]

         if {$grpMode != "exclude"} {
             puts "group mode did not matched for 2001:0:0:0:0:0:0:$i"
             puts "Expected include got $grpMode"
             ixNetCleanUp
             return $FAILED
         }

         # considering the tolerance source timer should be set to 0
         if {$srcTimer != 0} {
             puts "source timer for 2001:0:0:0:0:0:0:$i is not set properly"
             puts "Expected 0 got $srcTimer"
             ixNetCleanUp
             return $FAILED
         }
    }

    #---------------------------------------------------------------------------
    # Group 2001::1 to 2001::2 should not be there
    #---------------------------------------------------------------------------
    foreach i {1 2} {
         set learnedInfoTemp [retriveLearnedGrpSrc $learnedInfo  \
             "FF03:0:0:0:0:0:0:14"  "2001:0:0:0:0:0:0:$i"]

         if {[llength $learnedInfoTemp] != 0} {
             puts "source timer for 2001:0:0:0:0:0:0:$i should not be there"
             ixNetCleanUp
             return $FAILED
         }
    }

    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action

