#-------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
# To show how to start protocols and how to check learned info of a protocol.
# For this purpose we have used BGP and LDP
#
# Sequence of events being carried out by the script
#   1) Source the script gen file "ixNetScriptgenProc {}"
#   2) Start LDP protocol
#   3) Start OSPF protocol
#   4) Check LDP learned info
#   5) Disable the l2 interface
#   6) Check LDP learned info
#   7) Enable the l2 interface
#   8) Check LDP learned info
#
# SCRIPT-GEN USED : Yes
# IXNCFG USED     : No
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

#------------------------------------------------------------------------------------
# PROCEDURE    : GetLearntInfo
# PURPOSE      : Getting the LDP l2 learned info
# INPUT        : object referance to the interface on which learned info is required.
# OUTPUT       : the learned info
# RETURN VALUE : learned-info list.
#------------------------------------------------------------------------------------
proc GetLearntInfo {iface {learnedInfo {}}} {
    upvar learnedInfo learnedInfoLocal
    set a [ixNet exec refreshLearnedInfo $iface]
    set count 0

    set isComplete false
    while {$isComplete != true} {
        set isComplete [ixNet getAttr $iface -isLdpLearnedInfoRefreshed]
        puts "isComplete = $isComplete"
        after 1000
        incr count
        if {$count > 40} {
            puts "Could not retrieve learnt info on ldp \
                  interface:$iface,timeout"
            break
        }
    }

    set labelSpaceId 0
    set label 0
    set peer 0
    set vcType 0
    set groupId 0
    set vcId 0
    set pwState 0
    set cBit 0
    set mtu 0
    set maxAtmCell 0
    set cemPayloadBytes 0
    set cemOption 0
    set disCEAddress 0
    set description 0

    set listMartiny [::ixNet getList $iface learnedMartiniLabel]
    set count 0
    foreach item $listMartiny {
        incr count
        puts "IPv4 Learned Information : $count"
        puts "----------------------------------"
        set labelSpaceId    [ixNet getAtt $item -labelSpaceId]
        set label           [ixNet getAtt $item -label]
        set peer            [ixNet getAtt $item -peer]
        set vcType          [ixNet getAtt $item -vcType]
        set groupId         [ixNet getAtt $item -groupId]
        set vcId            [ixNet getAtt $item -vcId]
        set pwState         [ixNet getAtt $item -pwState]
        set cBit            [ixNet getAtt $item -cBit]
        set mtu             [ixNet getAtt $item -mtu]
        set maxAtmCell      [ixNet getAtt $item -maxAtmCell]
        set cemPayloadBytes [ixNet getAtt $item -cemPayloadBytes]
        set cemOption       [ixNet getAtt $item -cemOption]
        set disCEAddress    [ixNet getAtt $item -disCeAddress]
        set description     [ixNet getAtt $item -description]

        puts "labelSpaceId   :$labelSpaceId"
        puts "label          :$label"
        puts "peerIpAddress  :$peer"
        puts "vcType         :$vcType"
        puts "groupId        :$groupId"
        puts "vcId           :$vcId"
        puts "pwState        :$pwState"
        puts "cBit           :$cBit"
        puts "mtu            :$mtu"
        puts "maxAtmCell     :$maxAtmCell"
        puts "cemPayloadBytes:$cemPayloadBytes"
        puts "cemOption      :$cemOption"
        puts "disCEAddress   :$disCEAddress"
        puts "description    :$description"
    }

    set learnedInfoLocal [list $labelSpaceId $label $peer $vcType $groupId \
                               $vcId $pwState $cBit $mtu $maxAtmCell       \
                               $cemPayloadBytes $cemOption $disCEAddress   \
                               $description]

    # if count is 0 nothing is learned
    if {$count == 0} {set learnedInfoLocal {}}

    set learnedInfo $learnedInfoLocal
    return $learnedInfoLocal
}


#------------------------------------------------------------------------------
# PROCEDURE    : lcompare
# PURPOSE      : Procedure for comparing two lists a and b
# INPUT        : the two lists to be compared a = list1 and b = list2
# RETURN VALUE : 0 on success >0 if fails
#------------------------------------------------------------------------------
proc lcompare {a b} {
   set ctr 0
   foreach element $a {
       set val [lindex $b $ctr]
       if {[string equal $element $val] == 0} {
           incr ctr
           return $ctr
       }
       incr ctr
   }
   return 0
}


#------------------------------------------------------------------------------
# PROCEDURE    : Action
# PURPOSE      : Encapsulating all of your testing actions
# INPUT        : (1) [list $chassis1 $card1 $port1 $client1 $tcpPort1]
#                (2) [list $chassis2 $card2 $port2 $client2 $tcpPort2]
#                (3) home; (the current directory)
# RETURN VALUE : FAILED (1) or PASSED (0)
#------------------------------------------------------------------------------
proc Action {portData1 portData2} {
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
            puts "connection to client unsuccessfill"
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
    if {[catch {source "$::pwd/config.ethernet-l2-vpn-15.3.tcl"} error] } {
        puts "Error in sourcing the file ./config.ethernet-l2-vpn-15.3.tcl"
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

    puts "Waiting for 30 sec before starting protocols"
    after 30000
    # start Ldp
    ixNet exec start $vPort1/protocols/ldp
    ixNet exec start $vPort2/protocols/ldp

    # Start ospf2 on both the port 1 and port 2
    ixNet exec start $vPort1/protocols/ospf
    ixNet exec start $vPort2/protocols/ospf
    puts "Started OSPF on Port1 and Port2"

    puts "wait for 50 sec"
    after 50000

    # get ldp from protocol management
    set ldpProtocolMgmt1 "$vPort1/protocols/ldp"
    set ldpProtocolMgmt2 "$vPort2/protocols/ldp"

    # get Ldp router
    set ldpRouterList  [ixNet getList $ldpProtocolMgmt1 router]
    set ldpRouterList2 [ixNet getList $ldpProtocolMgmt2 router]

    # there must be two routers
    if {[llength $ldpRouterList] != 2 || [llength $ldpRouterList2] != 2} {
        puts "Configuration not loaded properly"
        ixNetCleanUp
        return $FAILED
    }

    # get the router 2 of port 1 and 2
    set ldpRouter  [lindex $ldpRouterList 1]
    set ldpRouter2 [lindex $ldpRouterList2 1]

    # get interface of Ldp router 2
    set ldpIntfList  [ixNet getList $ldpRouter interface]
    set ldpIntfList2 [ixNet getList $ldpRouter2 interface]

    # there must be 1 interface
    if {[llength $ldpIntfList] != 1 || [llength $ldpIntfList2] != 1} {
        puts "Configuration not loaded properly"
        set portsList [ixNet getList [::ixNet getRoot] vport]
        ixNetCleanUp
        return $FAILED
    }

    set intf  [lindex $ldpIntfList 0]
    set intf2 [lindex $ldpIntfList2 0]

    set timeOut 0
    while {$timeOut < 60} {
        set learnedInfo [GetLearntInfo $intf]
        incr timeOut
        if {[llength $learnedInfo] > 0} {
            break
        }
    }

    if {[llength $learnedInfo] == 0} {
        puts "No learned info found"
        ixNetCleanUp
        return $FAILED
    }
    puts "$learnedInfo"

    set expectedLearnedinfo {0 16 2.2.2.3 vlan 1 10 true \
                             false 1500 0 0 0 0.0.0.0 {}}

    if {[lcompare $expectedLearnedinfo $learnedInfo]} {
        puts "Learned info did not match"
        ixNetCleanUp
        return $FAILED
    }

    # get l2 interface
    set l2InterfaceList2 [ixNet getList $ldpRouter2 l2Interface]

    # there must be only one l2 interface
    if {[llength $l2InterfaceList2] != 1} {
        ixNetCleanUp
        return $FAILED
    }
    set l2Interface2 [lindex $l2InterfaceList2 0]
    puts "l2Interface $l2Interface2"

    # get l2 vc range
    set l2VcRangeList2 [ixNet getList $l2Interface2 l2VcRange]
    puts "L2VcRange: $l2VcRangeList2"

    # there must be one l2vc range
    if {[llength $l2VcRangeList2] != 1} {
        puts "Number of l2 vc range did not match"
        ixNetCleanUp
        return $FAILED
    }

    # get l2 vc range
    set l2Vcrange2 [lindex $l2VcRangeList2 0]

    # disable l2 Interface
    ixNet setAttr $l2Interface2 -enabled False
    ixNet commit

    puts "Wait for 60 sec"
    after 60000

    set timeOut 0
    while {$timeOut < 60} {
        set learnedInfo [GetLearntInfo $intf]
        incr timeOut
        if {[llength $learnedInfo] > 0} {
            break
        }
    }

    if {[llength $learnedInfo] != 0} {
        puts "Some learned info is there"
        ixNetCleanUp
        return $FAILED
    }
    puts "$learnedInfo"


    # enable l2 interface
    ixNet setAttr $l2Interface2 -enabled True
    ixNet commit

    puts "Wait for 50 sec"
    after 50000

    # check l2 learned info on port 1
    set timeOut 0
    while {$timeOut < 60} {
        set learnedInfo [GetLearntInfo $intf]
        incr timeOut
        if {[llength $learnedInfo] > 0} {
            break
        }
    }

    if {[llength $learnedInfo] == 0} {
        puts "No learned info found"
        ixNetCleanUp
        return $FAILED
    }
    puts "$learnedInfo"

    set expectedLearnedinfo {0 16 2.2.2.3 vlan 1 10 true \
                             false 1500 0 0 0 0.0.0.0 {}}

    if {[lcompare $expectedLearnedinfo $learnedInfo]} {
        ixNetCleanUp
        return $FAILED
    }

    # Needs to remove assigned ports after test
    ixNetCleanUp
    return $PASSED
}



#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
