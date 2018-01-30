#!/usr/local/bin/tclsh

#-----------------------------------------------------------------------------
# File Name  :test.older_host_comp_9_1_54.tcl
# Author     :Suvendu M
# Purpose    :To check older host present interval transition
# Initial Config :
#      p0 ---> v3Router0
#        |---> v2Host -> g1
#      p1|---> v2Host -> g1
#        |---> v3Host -> g1
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#------------------------------------------------------------------------------
# Standard package to include all IxNetwork APIs
#------------------------------------------------------------------------------

proc Action {portData1 portData2} {
    # initialize return value
    set FAILED 1
    set PASSED 0

    set isError [catch { source $::pwd/igmpRouterGlobals.tcl
                        source $::pwd/igmpRouterUtils.tcl} errorMsg]
    if {$isError} {
        puts "Error in sourcing the file $errorMsg"
        return $FAILED
    }

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
    if {[catch {source "$::pwd/config.older_host_comp_9_1_54.tcl"} error] } {
        puts "Error in sourcing the file ./config.older_host_comp_9_1_54.tcl"
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

    #Start the protocols
    set vPort1 [lindex [ixNet getList [ixNet getRoot] vport] 0]
    set vPort2 [lindex [ixNet getList [ixNet getRoot] vport] 1]
    puts "Starting Protocols"
    ixNet exec start $vPort1/protocols/igmp
    ixNet exec start $vPort2/protocols/igmp

    puts "Wait for 10 seconds before starting the protocols"
    after 10000

    #retrieving the igmp hostlist to enable the v1 and v2 hosts
    set p1Host0 [lindex [ixNet getList [lindex \
                $vPorts 1]/protocols/igmp host] 0]
    if {[ixNet setAttr $p1Host0 -enabled true] != "::ixNet::OK"} {
        puts "Failed to enable v1Host"
        ixNetCleanUp
        return $FAILED
    } else {
        puts "v1 Host enabled"
    }
    ixNet commit

    set enableTime [clock seconds]

    #retrieving the igmp querier
    puts "Check for v1 entry for group $igmpGlobals(g1) in the Querier"
    set p0Router1 [ixNet getList [lindex $vPorts 0]/protocols/igmp querier]

    #Retrieving Learned Info fromt the Router
    set lInfo [lindex [retrieveLearnedInfoDetailsByGroup $p0Router1 \
              $igmpGlobals(g1)] 0]
    if {$lInfo != ""} {
        if {[getParamFromLearnedInfo $lInfo "grpMode"] == $igmpGlobals(ex) && \
            [getParamFromLearnedInfo $lInfo "srcAddr"] == $igmpGlobals(s0) && \
            [getParamFromLearnedInfo $lInfo "compMode"] == $igmpGlobals(v1)} {
            set checkTime [clock seconds]
            set timeDiff [expr $checkTime-$enableTime]
            set initialV1CompTime [getParamFromLearnedInfo $lInfo "compTimer"]
            puts "Older Host Present Interval set to <$initialV1CompTime>"
            set startTime [clock seconds]
            # Check that the OHPI timer should run with value between
        } else {
            puts "FAILURE : Entry for g1 is not as expected : <$lInfo>"
            ixNetCleanUp
            return $FAILED
        }
    } else {
        puts "FAILURE : Waited for more than QI interval, Learned info \
            not found --failed!!"
        ixNetCleanUp
        return $FAILED
    }

    # Now disalbe v1 host and enable v2 Host
    set p1Host0 [lindex [ixNet getList [lindex $vPorts 1]/protocols/igmp \
                 host] 0]
    if {[ixNet setAttr $p1Host0 -enabled false] != "::ixNet::OK"} {
        puts "Failed to disable v1Host"
        ixNetCleanUp
        return $FAILED
    } else {
        puts "v1 Host disabled"
    }
    ixNet commit

    set p1Host1 [lindex [ixNet getList [lindex $vPorts 1]/protocols/igmp host] 1]
    if {[ixNet setAttr $p1Host1 -enabled true] != "::ixNet::OK"} {
        puts "Failed to enable v2Host"
        ixNetCleanUp
        return $FAILED
    } else {
        puts "v2 Host enabled"
    }
    ixNet commit

    # Now wait for Older Host Present timer expiry for the v1 host
    puts "Check after $igmpGlobals(qi1) interval what is the value of Comp. Timer"
    set checkOnce 1
    while (1) {
        sleep 1
        set curTime [clock seconds]
        if {$checkOnce && [expr $curTime-$startTime] > $igmpGlobals(qi1)} {
            set lInfo [lindex [retrieveLearnedInfoDetailsByGroup $p0Router1 \
                       $igmpGlobals(g1) $igmpGlobals(qi1)] 0]

            if {[getParamFromLearnedInfo $lInfo "compMode"] == $igmpGlobals(v1)} {
                set compTime [getParamFromLearnedInfo $lInfo "compTimer"]
                if {$compTime < $initialV1CompTime && $compTime > 0} {
                    puts "Compatibility Timer for v1 compatibility mode running."
                    set checkOnce 0
                } else {
                    puts "Compatibility timer value is not decrementing"
                    puts "Initially it was <$initialV1CompTime>, after \
                         $igmpGlobals(qi1) sec. it is <$compTime>"
                    ixNetCleanUp
                    return $FAILED
                }
            } else {
                puts "Compatibility mode has changed before Older \
                     Host Present Timer expiry"
                ixNetCleanUp
                return $FAILED
            }
        }
        if {[expr $curTime-$startTime] > $initialV1CompTime} {
            puts "Older Host Present Interval expired for v1"
            break
        }
    }


    # Now check that the entry present for g1 should have v2 compatibility mode
    # Retrieving Learned Info fromt the Router
    set lInfo [lindex [retrieveLearnedInfoDetailsByGroup $p0Router1 \
                      $igmpGlobals(g1) $igmpGlobals(qi1)] 0]
    if {$lInfo != ""} {
        if {[getParamFromLearnedInfo $lInfo "grpMode"] == $igmpGlobals(ex) && \
            [getParamFromLearnedInfo $lInfo "srcAddr"] == $igmpGlobals(s0) && \
            [getParamFromLearnedInfo $lInfo "compMode"] == $igmpGlobals(v2)} {

            puts  "Learned Info updated with group \
                   <$igmpGlobals(g1)> with comp mode as v2"
            set initialV2CompTime [getParamFromLearnedInfo $lInfo "compTimer"]
            puts "Older Host Present Interval set to <$initialV2CompTime>"

            if {$initialV2CompTime < $igmpGlobals(ohpi1) && $initialV2CompTime > 0} {
                puts  "Learned Info updated with group \
                       <$igmpGlobals(g1)> with comp mode as v2"
                puts "Older Host Present Interval running on <$initialV2CompTime>"
                set startTime [clock seconds]
            } else {
                puts "FAILURE : Older Host Present Interval for v2 not set properly"
                ixNetCleanUp
                return $FAILED
            }
        } else {
            puts "FAILURE : Entry for g1 is not as expected : <$lInfo>"
            ixNetCleanUp
            return $FAILED
        }
    } else {
        puts "FAILURE : Waited for more than QI interval, Learned info not found --failed!!"
        ixNetCleanUp
        return $FAILED
    }


    # Now disable the v2 Host so that it does not respond
    # to general queries any more and the Older Host Present Interval expires.
    # Also enable the v3 host so that it keeps sending v3 reports
    ixNet setAttr $p1Host1 -enabled false
    ixNet commit

    set p1Host2 [lindex [ixNet getList [lindex $vPorts 1]/protocols/igmp host] 2]
    ixNet setAttr $p1Host2 -enabled true
    ixNet commit

    puts "Check after $igmpGlobals(qi1) interval what is the value of Comp. Timer"
    # NOw wait for Older Host Present timer expiry for the v2 host
    set checkOnce 1
        while (1) {
        sleep 1
        set curTime [clock seconds]
        if {$checkOnce && [expr $curTime-$startTime] > $igmpGlobals(qi1)} {
            set lInfo [lindex [retrieveLearnedInfoDetailsByGroup $p0Router1 \
                      $igmpGlobals(g1) $igmpGlobals(qi1)] 0]

            if {[getParamFromLearnedInfo $lInfo "compMode"] == $igmpGlobals(v2)} {
                set compTime [getParamFromLearnedInfo $lInfo "compTimer"]
                if {$compTime < $initialV2CompTime && $compTime > 0} {
                    puts "Compatibility Timer for v2 compatibility mode running."
                    set checkOnce 0
                } else {
                    puts "Compatibility timer value is not decrementing"
                    puts "Initially it was <$initialV2CompTime>, after \
                         $igmpGlobals(qi1) sec. it is <$compTime>"
                    ixNetCleanUp
                    return $FAILED
                }
            } else {
                puts "Compatibility mode has changed before Older Host \
                     Present Timer expiry"
                ixNetCleanUp
                return $FAILED
            }
        }
        if {[expr $curTime-$startTime] > $initialV2CompTime} {
            puts "Older Host Present Interval expired for v2"
            break
        }
    }

    # Now check that the entry present for g1 should have v3 \
    # compatibility mode Retrieving Learned Info fromt the Router
    set lInfo [lindex [retrieveLearnedInfoDetailsByGroup $p0Router1 \
               $igmpGlobals(g1) $igmpGlobals(qi1)] 0]
    if {$lInfo != ""} {
        if {[getParamFromLearnedInfo $lInfo "grpMode"] == $igmpGlobals(ex) && \
            [getParamFromLearnedInfo $lInfo "srcAddr"] == $igmpGlobals(s0) && \
            [getParamFromLearnedInfo $lInfo "compMode"] == $igmpGlobals(v3)} {

            puts  "Learned Info updated with group <$igmpGlobals(g1)> \
                  with comp mode as v3"
            set v3CompTime [getParamFromLearnedInfo $lInfo "compTimer"]

            if {$v3CompTime != 0} {
                puts "FAILURE: Older Host Present Interval running for comp mode v3"
                ixNetCleanUp
                return $FAILED
            }
        } else {
            puts "FAILURE : Entry for g1 is not as expected : <$lInfo>"
            ixNetCleanUp
            return $FAILED
        }
    } else {
        puts "FAILURE : Waited for more than QI interval, Learned info not found --failed!!"
        ixNetCleanUp
        return $FAILED
    }
    ixNetCleanUp
    return $PASSED
}


#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
