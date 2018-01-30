################################################################################
# File Name  : test.9.1.22_LACPLearntInfoForActor.tcl
# Author     : Darshan T
# Purpose    : This test case verify that all the information in learned info
#              regarding actor is proper or not. To verify this we have to check
#              all actor information in the learned info with configured one.
# Return     : 0 - PASS
#              1 - FAIL
################################################################################
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

proc Action {portData1 portData2} {

    source $::pwd/LACP_Utils.tcl

    # initialize return value
    set PASSED 0
    set FAILED 1
    global lacpGlobalParams

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
        if {[catch {set status [ixNet connect $client1 -port $tcpPort1]} error]} {
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

    set configFileName "config.9.1.22_LACPLearntInfoForActor.ixncfg"

    puts "Loading the config file......"
    if  {[ixNet exec loadConfig [ixNet readFrom $::pwd/$configFileName]] != \
         $lacpGlobalParams(ixNetOk)} {
        puts "Loading IxNetwork config file FAILED "
        ixNetCleanUp
        return $FAILED
    }

    puts "Configuration of the ports Successful"
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2]]

    puts "$realPortsList"

    # Assign virtual ports to real ports

    puts "Assign virtual ports to real ports ..."
    set root   [ixNet getRoot]
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts]

    puts "Assigned: $status"

    set vport1 [lindex $vPorts 0]
    set vport2 [lindex $vPorts 1]

    set proto $vport1/protocols
    set proto [ixNet getList $proto lacp]

    set proto1 $vport2/protocols
    set proto1 [ixNet getList $proto1 lacp]

    set linkList1 [ixNet getList $proto link]
    set link1     [lindex $linkList1 0]

    set link2 [ixNet getList $proto1 link]

    # Start LACP Protocol
    puts "Start LACP Protocol"


    if {[startLacpOnPorts $proto $proto1] ==1} {
       puts "Error In Starting LACP protocol"
       ixNetCleanUp
       return $FAILED
    }

    puts "Wait for $lacpGlobalParams(pktCaptureDurShort) sec...."
    after $lacpGlobalParams(pktCaptureDurShortInMilisec)

    # Checking Learn info for port1.
    puts "Checking for leaenrd info for actor on port1...."
    set getLearnedInfo [retrieveLacpLearnedInfoPerLink $proto]

     if {[getParamFromLearnedInfo $getLearnedInfo "actorCollectingFlag"] != [ixNet getAttr $link1 -collectingFlag]        \
        || [string tolower [getParamFromLearnedInfo $getLearnedInfo "actorDefaultedFlag"]] != "false"                     \
        || [getParamFromLearnedInfo $getLearnedInfo "actorDistributingFlag"] != [ixNet getAttr $link1 -distributingFlag]  \
        || [string tolower [getParamFromLearnedInfo $getLearnedInfo "actorExpiredFlag"]] != "false"                       \
        || [getParamFromLearnedInfo $getLearnedInfo "actorLacpActivity"] != [ixNet getAttr $link1 -lacpActivity]          \
        || [string tolower [getParamFromLearnedInfo $getLearnedInfo "actorLacpTimeout"]] != "long"                        \
        || [getParamFromLearnedInfo $getLearnedInfo "actorOperationalKey"] != [ixNet getAttr $link1 -actorKey]            \
        || [getParamFromLearnedInfo $getLearnedInfo "actorPortNumber"] != [ixNet getAttr $link1 -actorPortNumber]         \
        || [getParamFromLearnedInfo $getLearnedInfo "actorPortPriority"] != [ixNet getAttr $link1 -actorPortPriority]     \
        || [getParamFromLearnedInfo $getLearnedInfo "actorSystemId"] != [ixNet getAttr $link1 -actorSystemId]             \
        || [getParamFromLearnedInfo $getLearnedInfo "actorSystemPriority"] != [ixNet getAttr $link1 -actorSystemPriority] \
        || [string tolower [getParamFromLearnedInfo $getLearnedInfo "enabledAggregation"]] != "true"                      \
        || [string tolower [getParamFromLearnedInfo $getLearnedInfo "actorLinkAggregationStatus"]] != "aggregatable"      \
        || [string tolower [getParamFromLearnedInfo $getLearnedInfo "actorSyncFlag"]] != "insync"} {

            puts "Learned info for actor is not proper for port1...."
            ixNetCleanUp
            return $FAILED
    }

    puts "Verification of learned info for actor done succesfully for port1...."

    # Checking Learn info for port2.
    puts "Checking for leaenrd info for actor on port2...."

    set getLearnedInfo1 [retrieveLacpLearnedInfoPerLink $proto1]

    if {[getParamFromLearnedInfo $getLearnedInfo1 "actorCollectingFlag"] != [ixNet getAttr $link2 -collectingFlag]         \
        || [string tolower [getParamFromLearnedInfo $getLearnedInfo1 "actorDefaultedFlag"]] != "false"                     \
        || [getParamFromLearnedInfo $getLearnedInfo1 "actorDistributingFlag"] != [ixNet getAttr $link2 -distributingFlag]  \
        || [string tolower [getParamFromLearnedInfo $getLearnedInfo1 "actorExpiredFlag"]] != "false"                       \
        || [getParamFromLearnedInfo $getLearnedInfo1 "actorLacpActivity"] != [ixNet getAttr $link2 -lacpActivity]          \
        || [string tolower [getParamFromLearnedInfo $getLearnedInfo1 "actorLacpTimeout"]] != "long"                        \
        || [getParamFromLearnedInfo $getLearnedInfo1 "actorOperationalKey"] != [ixNet getAttr $link2 -actorKey]            \
        || [getParamFromLearnedInfo $getLearnedInfo1 "actorPortNumber"] != [ixNet getAttr $link2 -actorPortNumber]         \
        || [getParamFromLearnedInfo $getLearnedInfo1 "actorPortPriority"] != [ixNet getAttr $link2 -actorPortPriority]     \
        || [getParamFromLearnedInfo $getLearnedInfo1 "actorSystemId"] != [ixNet getAttr $link2 -actorSystemId]             \
        || [getParamFromLearnedInfo $getLearnedInfo1 "actorSystemPriority"] != [ixNet getAttr $link2 -actorSystemPriority] \
        || [string tolower [getParamFromLearnedInfo $getLearnedInfo1 "enabledAggregation"]] != "true"                      \
        || [string tolower [getParamFromLearnedInfo $getLearnedInfo1 "actorLinkAggregationStatus"]] != "aggregatable"      \
        || [string tolower [getParamFromLearnedInfo $getLearnedInfo1 "actorSyncFlag"]] != "insync"} {

            puts "Learned info for actor is not proper for port2...."
            ixNetCleanUp
            return $FAILED
    }
    puts "Verification of learned info for actor done succesfully for port2...."


    # Stop LACP Protocols
    puts "Stop LACP Protocol"
    if {[stopLacpOnPorts $proto $proto1] ==1} {

        puts "Error In Starting LACP protocol"
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
