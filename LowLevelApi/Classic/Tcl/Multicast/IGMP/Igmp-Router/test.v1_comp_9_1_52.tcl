#!/usr/local/bin/tclsh

################################################################################
#File Name  :test.v1_comp_9_1_52.tcl
#Author     :Suvendu M
#Purpose    :To check v3 Block messages are ignored in v1 compatibility mode
#Initial Config :
# p0 ---> v3Router0
#    |--> v1Host -> g1
# p1-|
#    |--> v3Host with gqResponseMode set to false -> g1 include s1,s2
# Status : NEW
################################################################################
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

proc Action {portData1 portData2} {
    global topoputsyGlobals igmpGlobals
    puts "P1 =$portData1 P2 = $portData2"

    # initialize return value
    set PASSED 0
    set FAILED 1

    set isError [catch { source $::pwd/igmpRouterGlobals.tcl
                         source $::pwd/igmpRouterUtils.tcl } errorMsg]

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
    if {[catch {source "$::pwd/config.v1_comp_9_1_52.tcl"} error] } {
        puts "Error in sourcing the file ./config.v1_comp_9_1_52.tcl"
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
    puts "Starting Protocols"
    set vPort1 [lindex [ixNet getList [ixNet getRoot] vport] 0]
    set vPort2 [lindex [ixNet getList [ixNet getRoot] vport] 1]

    ixNet exec start $vPort1/protocols/igmp
    ixNet exec start $vPort2/protocols/igmp

    #retrieving the igmp router
    set p0Router1 [ixNet getList [lindex $vPorts 0]/protocols/igmp querier]
    #Retrieving Learned Info fromt the Router
    set lInfo [lindex [retrieveLearnedInfoDetailsByGroup \
              $p0Router1 $igmpGlobals(g1)] 0]
    if {$lInfo != ""} {
        if {[getParamFromLearnedInfo $lInfo "grpMode"] == $igmpGlobals(ex) && \
            [getParamFromLearnedInfo $lInfo "srcAddr"] == $igmpGlobals(s0) && \
            [getParamFromLearnedInfo $lInfo "compMode"] == $igmpGlobals(v1)} {
            puts  "SUCCESS : Learned Info updated with group <$igmpGlobals(g1)> \
                  with comp mode as v1 and filter mode as exclude(NULL)"
        } else {
            puts "FAILURE : Entry for g1 is not as expected : <$lInfo>"
            ixNetCleanUp
            return $FAILED
        }
    } else {
        puts "FAILURE : Waited for more than QI interval, \
              Learned info not found --failed!!"
        ixNetCleanUp
        return $FAILED
    }

    # Disable the v1 host so that it doesnot respond to any general query received
    # when we are waiting for LMQT expiry.This is to ensure that the router has
    # really ignored the block message and he has not deleted the entry and not
    # relearned by any v1 query sent in between
    set p1Host1 [lindex [ixNet getList [lindex $vPorts 1]/protocols/igmp host] 0]
    if {[ixNet setAttr $p1Host1 -enabled false] != "::ixNet::OK"} {
        puts "FAILURE : Could not disable the v1 host on port <$p1Host1>"
        IxNetCleanUp
        return $FAILED
    } else {
        ixNet commit
    }

    #Disable the group range in the v3 host so that it sends a block message
    set p1Host2 [lindex [ixNet getList [lindex $vPorts 1]/protocols/igmp host] 1]
    set grList [ixNet getList $p1Host2 group]
    set searchFlag 0
    foreach grp $grList {
        if {[regexp $igmpGlobals(g1) [ixNet getAttr $grp -groupFrom]]} {
            puts "Disabling grouprange <$igmpGlobals(g1)> in <$p1Host2>"
            if {[ixNet setAttr $grp -enabled false] == "::ixNet::OK"} {
                puts "grouprange <$igmpGlobals(g1)> in <$p1Host2> disabled successfully"
                ixNet commit
                set searchFlag 1
            } else {
                puts "FAILURE : Could not disable group range"
                IxNetCleanUp
                return $FAILED
            }
        }
    }

    if {!$searchFlag} {
        puts "FAILURE : Could not find grouprange <$igmpGlobals(g1)> in <$p1Host2>"
        IxNetCleanUp
        return $FAILED
    }

    puts "Wait for LMQT time to ensure that Router is not deleting the group after LMQT expiry"
    puts "Sleeping for LMQT(<$igmpGlobals(lmqt)>sec) ...."
    sleep $igmpGlobals(lmqt)
    #Retrieving Learned Info from the Router
    set lInfo [lindex [retrieveLearnedInfoDetailsByGroup $p0Router1 $igmpGlobals(g1)] 0]
    if {$lInfo != ""} {
        if {[getParamFromLearnedInfo $lInfo "grpMode"] == $igmpGlobals(ex) && \
            [getParamFromLearnedInfo $lInfo "srcAddr"] == $igmpGlobals(s0) && \
            [getParamFromLearnedInfo $lInfo "compMode"] == $igmpGlobals(v1)} {
            puts  "Learned Info contains group <$igmpGlobals(g1)>, \
                   Group not deleted as expected"

            puts  "SUCCESS: While in v1 compatibility mode reports \
                   with block sources are ignored"
        } else {
            puts  "Group <$igmpGlobals(g1)> not present in Learned \
                   Info Database"
            puts  "FAILURE : While in v1 compatibility mode reports \
                   with block sources are not being ignored"
            ixNetCleanUp
            return $FAILED
        }
    } else {
        puts "FAILURE : Waited for more than QI interval, Learned info not found --failed!!"
        ixNetCleanUp
        return $FAILED
    }

    set portList [list [list $chassisIp1 $card1 $port1]]
    set statToCheck {"IGMPv2 Group specific Query Tx" 0 \
                     "IGMPv3 Group Specific Query Tx" 0}
    #Check the stats
    set grpSrcQ  [checkAllIGMPStats $portList $statToCheck ]
    if {!$grpSrcQ} {
        puts "SUCCESS : No group specific queries sent by the router"
    } else {
        puts "FAILURE : Group specific queries sent by the router"
        puts "FAILURE : It should not have sent as it is supposed to ignor the block msg"
        ixNetCleanUp
        return $FAILED
    }


    # Enable the v1 host again
    set p1Host1 [lindex [ixNet getList [lindex $vPorts 1]/protocols/igmp host] 0]
    if {[ixNet setAttr $p1Host1 -enabled true] != "::ixNet::OK"} {
        puts "FAILURE : Could not enable the v1 host on port <$p1Host1>"
        IxNetCleanUp
        return $FAILED
    } else {
        ixNet commit
    }

    puts "Now Check that To_Ex messages are also ignored in v1 compatibility mode"
    #Change the group mode to exclude in the v3 host so that it sends a To_Ex message
    set p1Host2 [lindex [ixNet getList [lindex $vPorts 1]/protocols/igmp host] 1]
    set grList [ixNet getList $p1Host2 group]
    set searchFlag 0
    foreach grp $grList {
        if {[regexp $igmpGlobals(g1) [ixNet getAttr $grp -groupFrom]]} {
            set searchFlag 1
            puts "Enabling grouprange <$igmpGlobals(g1)> in <$p1Host2>"
            if {[ixNet setAttr $grp -enabled true] == "::ixNet::OK"} {
                puts "grouprange <$igmpGlobals(g1)> in <$p1Host2> enabled successfully"
                ixNet commit
            } else {
                puts "FAILURE : Could not enable group range"
                IxNetCleanUp
                return $FAILED
            }
            sleep 2
            puts "Changing mode of grouprange <$igmpGlobals(g1)> to exclude"
            if {[ixNet setAttr $grp -sourceMode exclude] == "::ixNet::OK"} {
                puts "Mode of <$igmpGlobals(g1)> in <$p1Host2> changed to exclude successfully"
                ixNet commit
            } else {
                puts "FAILURE : Could not change mode to exclude"
                IxNetCleanUp
                return $FAILED
            }
            sleep 2
            puts "Updating the sources of grouprange <$igmpGlobals(g1)> so that it sends a To_Ex report"
            if {[ixNet setAttr $grp -updateRequired true] == "::ixNet::OK"} {
                puts "source list updated"
                ixNet commit
            } else {
                puts "FAILURE : Could not update sourcelist"
                IxNetCleanUp
                return $FAILED
            }
        }
    }

    if {!$searchFlag} {
        puts "FAILURE : Could not find grouprange <$igmpGlobals(g1)> in <$p1Host2>"
        IxNetCleanUp
        return $FAILED
    }

    puts "Wait for LMQT time to ensure that Router is not deleting the group after LMQT expiry"
    puts "Sleeping for LMQT(<$igmpGlobals(lmqt)>sec) ...."
    sleep $igmpGlobals(lmqt)
    #Retrieving Learned Info from the Router
    set lInfo [lindex [retrieveLearnedInfoDetailsByGroup $p0Router1 $igmpGlobals(g1)] 0]
    if {$lInfo != ""} {
        if {[getParamFromLearnedInfo $lInfo "grpMode"] == $igmpGlobals(ex) && \
            [getParamFromLearnedInfo $lInfo "srcAddr"] == $igmpGlobals(s0) && \
            [getParamFromLearnedInfo $lInfo "compMode"] == $igmpGlobals(v1)} {
            puts  "Learned Info contains group <$igmpGlobals(g1)>, Group not deleted as expected"
            puts  "SUCCESS: While in v1 compatibility mode reports with block sources are ignored"
        } else {
            puts  "Group <$igmpGlobals(g1)> not present in Learned Info Database"
            puts  "FAILURE : While in v1 compatibility mode reports with block sources are not being ignored"
            ixNetCleanUp
            return $FAILED
        }
    } else {
        puts "FAILURE : Waited for more than QI interval, Learned info not found --failed!!"
        ixNetCleanUp
        return $FAILED
    }

    #Check the stats
    set grpSrcQ  [checkAllIGMPStats $portList $statToCheck ]
    if {!$grpSrcQ} {
        puts "SUCCESS : No group specific queries sent by the router"
    } else {
        puts "FAILURE : Group specific queries sent by the router"
        puts "FAILURE : It should not have sent as it is supposed to ignor the block msg"
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

