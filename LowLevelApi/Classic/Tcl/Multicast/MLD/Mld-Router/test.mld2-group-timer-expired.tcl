#----------------------------------------------------------------------------
# TEST DESCRIPTION:
#    This test cases checks if group timer expires properly or not for mldv2
#    router; when the hosts does not sent any "done" or "block" report.
#
#    1) Configure mldv2 host on port 2 with one group no source in exclude
#       mode
#    2) Configure mldv2 router on port 1
#    3) Start mld Router
#    4) Then after 5 second start mld host
#    5) After 10 seconds check the learned info in the mld router
#    6) Then delete the mld host on the port 2
#    7) Keep checking the learned info in the interval of 10 seconds
#    8) Perform the above in the loop 10 time (confirm that group timer
#       is decrimenting)
#    9) At the end of the 10 iteration check the group timer value
#   10) Let the group timer value be X seconds
#   11) After (X + 1) seconds there should not be any learned info
#
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

#------------------------------------------------------------------------------
# PROCDURE     : getMldLearnedInfo
# PURPOSE      : To retrive the learned info object from mld querier.
# PARAMETERS   : The object referance of mld querier.
# RETURN VALUE : the list of learned object-ref.
#------------------------------------------------------------------------------
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
                 $mldRtr ... timeout"
            return ""
        }
    }

    set learntList [ixNet getList $mldRtr learnedGroupInfo]
    return $learntList
}


#------------------------------------------------------------------------------
# PROCEDURE : retriveLearnedGrp
# PURPOSE   : retriving the group timers from learned info for a given
#             group
#------------------------------------------------------------------------------
proc retriveLearnedGrp {learnedList {grp {}}} {

    set none {}
    if {[llength $learnedList] > 0} {
        foreach learntinfo $learnedList {
            set grpAddr [::ixNet getAttribute $learntinfo -groupAddress]
            if {$grpAddr == $grp} {
                set address [::ixNet getAttribute $learntinfo -groupAddress]
                set timer   [::ixNet getAttribute $learntinfo -groupTimer]
                set mode    [::ixNet getAttribute $learntinfo -filterMode]
                set sAddr   [::ixNet getAttribute $learntinfo -sourceAddress]
                set srcTmr  [::ixNet getAttribute $learntinfo -sourceTimer]
                puts "Group Address : $address"
                puts "Group Timer   : $timer"
                puts "group Mode    : $mode"
                puts "Source Addr   : $sAddr"
                puts "Source Timer  : $srcTmr"
                return $timer
            }
        }
    } else {
        return $none
    }
    return $none
}


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
    if {[catch {source "$::pwd/config.mld2-group-timer-expired.tcl"} error] } {
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
        return $FAILED
    }
    ixTclNet::CheckLinkState $vPorts doneList

    set root   [ixNet getRoot]
    set vport1 [lindex [ixNet getList $root vport] 0]
    set vport2 [lindex [ixNet getList $root vport] 1]

    set mld1        $vport1/protocols/mld
    set mldRtr      [lindex [ixNet getList $mld1 querier] 0]

    set mld2        $vport2/protocols/mld
    set mldHost1    [lindex [ixNet getList $mld2 host] 0]
    set mldHostGrp1 [lindex [ixNet getList $mldHost1 groupRange] 0]

    puts "Mldv1 querier started on port1"
    ixNet exec start $mld1

    puts "wait for 5 sec"
    after 5000

    puts "Mldv1 host started on port2"
    ixNet exec start $mld2

    puts "Wait for 10 second"
    after 10000

    puts "Check the learned info"
    set info [getMldLearnedInfo $mldRtr]
    set learnedGrpTimer1 [retriveLearnedGrp $info "FF03:0:0:0:0:0:0:14"]
    if {[llength $learnedGrpTimer1] == 0} {
        ixNetCleanUp
        return $FAILED
    }

    # starting packet capture
    # puts "Starting packet capture ..."
    # ixNet exec startCapture

    puts "Wait for 10 second"
    after 10000

    puts "Removing the MLD host"
    ixNet remove $mldHost1
    ixNet commit

    # retrive learned info in loop for 10 times
    set k 0
    set prevLearnedTimer $learnedGrpTimer1
    while {$k <= 10} {
        puts "Wait for 10 second"
        after 10000

        set info [getMldLearnedInfo $mldRtr]
        set learnedGrpTimer1 [retriveLearnedGrp $info "FF03:0:0:0:0:0:0:14"]

        if {[llength $learnedGrpTimer1] == 0} {
            puts "Group timer has expired .. break"
            break
        }

        if {$learnedGrpTimer1 > $prevLearnedTimer} {
            puts "Learned Timer refreshed un-expectedly!!! "
            ixNetCleanUp
            ixNet exec startCapture
            return $FAILED
        }

        set prevLearnedTimer $learnedGrpTimer1
        incr k
    }

    set waitTime [expr $prevLearnedTimer + 1]
    puts "Wait for $waitTime seconds for group timer to expire !!"
    after [expr $waitTime * 1000]

    # At this group timer should have expired.
    puts "Checking group timer again"
    set info [getMldLearnedInfo $mldRtr]
    set learnedGrpTimer1 [retriveLearnedGrp $info "FF03:0:0:0:0:0:0:14"]
    if {[llength $learnedGrpTimer1] != 0} {
        puts "group timer exists unexpectedly"
        ixNetCleanUp
        return $FAILED
    }

    puts "Stopping All protocols"
    ixNet exec stopAllProtocols

    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
