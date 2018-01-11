#-------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
#   Check PBT CCM Functionality
#
# SCRIPT-GEN USED : No
# IXNCFG USED     : config.refreshPbtCcmLearnedInfo.ixncfg
#                   Configure 1 Bridge ,  8 Trunk on both the ports .
#                   First four trunk are in MD level4 and
#                   second four are in MD level5
#                   Every  trunks are in different MA , CCI 1sec
#                   Diffrent BVLAN  ID .
#                   1. Check the CCM Functionality
#                   2. Disable/Enable the Trunks check the CCM learned info
#
#
# Sequence of events being carried out by the script
#   1) Load the config file
#   2) Start CFM protocol & Wait for some time
#   3) Set filter, Refresh & Verify CCM Learned info with no Defect
#   4) Disable the Trunk
#   5) Set filter, Refresh & Verify CCM Learned info with Defect
#   6) Enable the Trunk
#   7) Set filter, Refresh & Verify CCM Learned info with no Defect
#   8) Stop CFM protocol
#
#-------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

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

    # Source CFM common utility files
    source $::pwd/cfmCommonUtils.tcl

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

    # Now we configure the first Ixia port
    puts "loading ixncfg file ..."
    # load config files
    if  {[ixNet exec loadConfig [ixNet readFrom "$::pwd/config.refreshPbtCcmLearnedInfo.ixncfg" ]] != "::ixNet::OK"} {
        puts "Error in sourcing the file config.refreshPbtCcmLearnedInfo.ixncfg"
        return $FAILED
    }

    # get the virtual port list
    puts "getting virtual ports ...."
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]
    puts "Virtual ports are = $vPorts"

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
        [list $chassisIp2 $card2 $port2] ]
    puts "realPortsList = $realPortsList"

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

    puts "Waiting for 30 sec before starting ..."
    after 30000

    # Get CFM/PBT
    set pbt1 $vPort1/protocols/cfm
    set pbt2 $vPort2/protocols/cfm

    puts "Starting CFM/PBT ... "
    ixNet exec start $pbt1
    ixNet exec start $pbt2

    puts "Waiting for 30 seconds....."
    after 30000

    # PBT Bridge
    set pbt1Bridge [lindex [ixNet getList $pbt1 bridge] 0]
    set pbt2Bridge [lindex [ixNet getList $pbt2 bridge] 0]

    # Check & Verify PBT CCM LearntInfo in noDefectDatabase
    set checkInLearntInfoList_all {}
    for {set i 1; set lastbyte 17} {$i <= 4} {incr i; incr lastbyte} {
        lappend checkInLearntInfoList_all [subst {"B-VLANID $i TPID 0x8100 Priority 0" \
            "00:00:0a:00:00:[format %0.2x $lastbyte]" "00:00:0a:00:00:[format %0.2x $i]" 2 "network-$i" \
            [expr 10 + $i] $i 4 4 "Ixiacom-0" false false false false false 0 "1 Sec" 0 0 0 0}]
    }
    for {set i 5; set lastbyte 21} {$i <= 6} {incr i; incr lastbyte} {
        lappend checkInLearntInfoList_all [subst {"B-VLANID $i TPID 0x8100 Priority 0" \
            "00:00:0a:00:00:[format %0.2x $lastbyte]" "00:00:0a:00:00:[format %0.2x $i]" 2 "network-$i" \
            [expr 10 + $i] $i 5 4 "Ixiacom-0" false false false false false 0 "1 Sec" 0 0 0 0}]
    }

    if {[checkCfmPbtCcmLearnedInfo $pbt1Bridge $checkInLearntInfoList_all] == 1} {
        puts "All requested Infos are not available in PBT CCM no Defect Database"
        ixNetCleanUp
        return $FAILED
    }

    # Disable one trunk in port1 & check learnt Info for bridge containing it pair in port2
    set en_disen "False"
    set trunkSpec {mepId 1 \
                   srcMacAddress "00:00:0A:00:00:01" \
                   dstMacAddress "00:00:0A:00:00:11"}
    puts "Disabling Trunk with specification: \n $trunkSpec"
    if {[enableDisablePbtTrunk $pbt1Bridge $en_disen $trunkSpec] == 1} {
        puts "Failed to find & disable trunk with expected specification"
        ixNetCleanUp
        return $FAILED
    }

    puts "Waiting for 5 seconds....."
    after 5000

    # Disabled Trunk Info will come in CCM DefectDatabase
    set checkInLearntInfoList_dis {{"B-VLANID 1 TPID 0x8100 Priority 0" \
        "00:00:0a:00:00:01" "00:00:0a:00:00:11" 2 "network-1" \
        1 11 4 4 "Ixiacom-0" false false false false true 0 "1 Sec" 0 0 0 1}}

    if {[checkCfmPbtCcmLearnedInfo $pbt2Bridge $checkInLearntInfoList_dis] == 1} {
        puts "All requested Infos are not available in PBT CCM Defect Database"
        ixNetCleanUp
        return $FAILED
    }

    after 2000

    # Re-enabled Trunk & check CCM no DefectDatabase
    set en_disen "True"
    set trunkSpec {mepId 1 \
                   srcMacAddress "00:00:0A:00:00:01" \
                   dstMacAddress "00:00:0A:00:00:11"}
    puts "Disabling Trunk with specification: \n $trunkSpec"
    if {[enableDisablePbtTrunk $pbt1Bridge $en_disen $trunkSpec] == 1} {
        puts "Failed to find & enable trunk with expected specification"
        ixNetCleanUp
        return $FAILED
    }

    puts "Waiting for 5 seconds....."
    after 5000

    if {[checkCfmPbtCcmLearnedInfo $pbt1Bridge $checkInLearntInfoList_all] == 1} {
        puts "All requested Infos are not available in PBT CCM Defect Database"
        ixNetCleanUp
        return $FAILED
    }

    puts "Stoping CFM/PBT ... "
    ixNet exec stop $pbt1
    ixNet exec stop $pbt2

    ixNetCleanUp
    return $PASSED

}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
