#-------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
#       PBT Loopback Functionality verification
#
# SCRIPT-GEN USED : No
# IXNCFG USED     : config.refreshPbtLbLearnedInfo.ixncfg
#                   Configure 1 Bridge ,
#                   8 Trunk on both the ports  with Different  MA Name ,
#                   same  MD Name , MD levels from  0 to 7 ,
#                   CCI 3.33ms ,10ms , 100ms , 1sec , 10 sec , 1 min , 10 min , 1sec
#                   diffrent B VLAN ID with diffrent TPID diffrent Priority
#                   check the LBM Functionality
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
    if  {[ixNet exec loadConfig [ixNet readFrom "$::pwd/config.refreshPbtLbLearnedInfo.ixncfg" ]] != "::ixNet::OK"} {
        puts "Error in sourcing the file config.refreshPbtLbLearnedInfo.ixncfg"
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

    # Check & Verify PBT LB LearntInfo
    set filter {userBvlan       vlanId \
            userBvlanId         105 \
            userBvlanPriority   4 \
            userBvlanTpId       0x8100 \
            userMdLevel         4 \
            userSrcMacAddress   "00:00:0a:00:00:05" \
            userDstMacAddress   "00:00:0a:00:00:15"}

    set checkInLearntInfoList {"B-VLANID 105 TPID 0x8100 Priority 4" \
                        4 "00:00:0a:00:00:05" "00:00:0a:00:00:15" true}

    if {[checkPbtLbLearnedInfo $pbt1Bridge $filter $checkInLearntInfoList] == 1} {
        puts "All requested Infos are not available in PBT LB Database"
        ixNetCleanUp
        return $FAILED
    }

    # Check & Verify PBT LB LearntInfo using MepId filter
    set filter {userBvlan         vlanId \
            userBvlanId           106 \
            userBvlanPriority     5 \
            userBvlanTpId         0x9100 \
            userMdLevel           5 \
            userSelectSrcMepById  true \
            userSrcMepId          6 \
            userSelectDstMepById  false \
            userDstMacAddress     "00:00:0a:00:00:16"}

    set checkInLearntInfoList {"B-VLANID 106 TPID 0x9100 Priority 5" \
                               5 "00:00:0a:00:00:06" "00:00:0a:00:00:16" true}

    if {[checkPbtLbLearnedInfo $pbt1Bridge $filter $checkInLearntInfoList] == 1} {
        puts "All requested Infos are not available in PBT LB Database"
        ixNetCleanUp
        return $FAILED
    }

    # Check for incorrect filter specification reachability fails
    set filter {userBvlan       vlanId \
            userBvlanId         106 \
            userBvlanPriority   5 \
            userBvlanTpId       0x8100 \
            userMdLevel         5 \
            userSelectSrcMepById  false \
            userSrcMacAddress   "00:00:0a:00:00:06" \
            userSelectDstMepById  false \
            userDstMacAddress   "00:00:0a:00:00:16"}

    set checkInLearntInfoList {"B-VLANID 106 TPID 0x8100 Priority 5" \
                               5 "00:00:0a:00:00:06" "00:00:0a:00:00:16" false}

    if {[checkPbtLbLearnedInfo $pbt1Bridge $filter $checkInLearntInfoList false 101] == 1} {
        puts "All requested Infos are not available in PBT LB Database"
        ixNetCleanUp
        return $FAILED
    }

    # Check for unconfigured Mep
    set filter {userBvlan       vlanId \
            userBvlanId         106 \
            userBvlanPriority   5 \
            userBvlanTpId       0x9100 \
            userMdLevel         5 \
            userSrcMacAddress   "00:00:0a:0b:00:06" \
            userDstMacAddress   "00:00:0a:00:00:16"}

    set checkInLearntInfoList {"B-VLANID 106 TPID 0x9100 Priority 5" \
                               5 "00:00:0a:0b:00:06" "00:00:0a:00:00:16" false}

    if {[checkPbtLbLearnedInfo $pbt1Bridge $filter $checkInLearntInfoList false 1975] == 1} {
        puts "All requested Infos are not available in PBT LB Database"
        ixNetCleanUp
        return $FAILED
    }

    # Check & Verify PBT LB LearntInfo by specifying broadcast dest MAC
    set filter1 {userBvlan       vlanId \
            userBvlanId         105 \
            userBvlanPriority   4 \
            userBvlanTpId       0x8100 \
            userMdLevel         4 \
            userSrcMacAddress   "00:00:0a:00:00:05" \
            userDstMacAddress   "FF:FF:FF:FF:FF:FF"}

    set filter2 {userBvlan       vlanId \
            userBvlanId         105 \
            userBvlanPriority   4 \
            userBvlanTpId       0x8100 \
            userMdLevel         4 \
            userSrcMacAddress   "00:00:0a:00:00:05" \
            userDstType         mepMacAll}

    set checkInLearntInfoList {"B-VLANID 105 TPID 0x8100 Priority 4" \
                        4 "00:00:0a:00:00:05" "00:00:0a:00:00:15" true}

    if {[checkPbtLbLearnedInfo $pbt1Bridge $filter1 $checkInLearntInfoList] == 1 &&
        [checkPbtLbLearnedInfo $pbt1Bridge $filter2 $checkInLearntInfoList] == 1}    {
        log "All requested Infos are not available in PBT LB Database"
        ixNetCleanUp
        return $flag
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
