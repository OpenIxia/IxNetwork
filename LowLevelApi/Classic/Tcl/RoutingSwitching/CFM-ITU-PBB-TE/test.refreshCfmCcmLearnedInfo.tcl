#-------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
#           CFM CCM Packet Learned Info verification
#
# SCRIPT-GEN USED : No
# IXNCFG USED     : config.refreshCfmCcmLearnedInfo.ixncfg
#                   Configure 1 bridge 2 MEP/MIP 1 Mdlevel with 1 QinQ Vlan
#                   Check CFM CCM Learnt Info
#
# Sequence of events being carried out by the script
#   1) Load the config file
#   2) Start CFM protocol & Wait for some time
#   3) Set filter, Refresh & Verify CCM Learned info with no Defect
#   4) Disable the MEP in bridge2
#   5) Set filter, Refresh & Verify CCM Learned info with Defect
#   6) Enable the MEP in bridge2
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
    if  {[ixNet exec loadConfig [ixNet readFrom "$::pwd/config.refreshCfmCcmLearnedInfo.ixncfg"]] != "::ixNet::OK"} {
        puts "Error in sourcing the file config.refreshCfmCcmLearnedInfo.ixncfg"
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

    # Start CFM
    puts "Starting the CFM protocols...."
    ixNet exec start $vPort1/protocols/cfm
    ixNet exec start $vPort2/protocols/cfm

    puts "Waiting for 30 seconds....."
    after 30000

    # Get the bridges
    set cfmbridge1 [lindex [ixNet getList $vPort1/protocols/cfm bridge] 0]
    set cfmbridge2 [lindex [ixNet getList $vPort2/protocols/cfm bridge] 0]

    puts "verify CCM Learned info ... "
    set filter {userMdLevel 0
                userSvlan allVlanId \
                userCvlan allVlanId}
    set checkInLearntInfoList {{"VLANID 1 TPID 0x8100 Priority 0" \
                        "VLANID 11 TPID 0x8100 Priority 1" 0 "00:00:00:00:00:02" \
                        2 false false false false false false false 0 false \
                        "1 sec" 2 "Ixia-0" 4 "Ixiacom-0"}}
    puts "Searching in CCM no Defect Database . . ."
    if {[checkCfmCcmLearnedInfo $cfmbridge1 $filter $checkInLearntInfoList] == 1} {
        puts "All requested Infos are not available in CFM CCM Database"
        ixNetCleanUp
        return $FAILED
    }

    set filter {userMdLevel 1}
    set checkInLearntInfoList {{"VLANID 1 TPID 0x8100 Priority 0" \
                        "VLANID 22 TPID 0x8100 Priority 2" 1 "00:00:00:00:00:04" \
                        4 false false false false false false false 0 false \
                        "1 sec" 2 "Ixia-0" 4 "Ixiacom-1"}}
    puts "Searching in CCM no Defect Database . . ."
    if {[checkCfmCcmLearnedInfo $cfmbridge1 $filter $checkInLearntInfoList] == 1} {
        puts "All requested Infos are not available in CFM CCM Database"
        ixNetCleanUp
        return $FAILED
    }

    # Disable the MEP in bridge2 with MD level 1
    puts "Disable the MEP in bridge2 with MD level 1 Mac Address 00:00:00:00:00:04"
    set mpList [ixNet getList $cfmbridge2 mp]
    foreach mp $mpList {
        if {[checkAttributeValue $mp {macAddress "00:00:00:00:00:04"}] == 0} {
            if {[setAndCheckAttributeValue $mp "enabled" {"False" y}] == 1} {
                puts "Falied to disable MP with Mac Address 00:00:00:00:00:04"
            }
        }
    }

    after 2000

    set filter {userMdLevel 1}
    set checkInLearntInfoList {{"VLANID 1 TPID 0x8100 Priority 0" \
                    "VLANID 22 TPID 0x8100 Priority 2" 1 "00:00:00:00:00:04" \
                    4 false true true false false false true 0 false "1 sec" \
                    2 "Ixia-0" 4 "Ixiacom-1"}}
    puts "Searching in CCM Defect Database . . ."
    if {[checkCfmCcmLearnedInfo $cfmbridge1 $filter $checkInLearntInfoList] == 1} {
        puts "All requested Infos are not available in CFM CCM Database"
        ixNetCleanUp
        return $FAILED
    }

    # Enable the MEP in bridge2 with MD level 1
    puts "Enable the MEP in bridge2 with MD level 1 Mac Address 00:00:00:00:00:04"
    set mpList [ixNet getList $cfmbridge2 mp]
    foreach mp $mpList {
        if {[checkAttributeValue $mp {macAddress "00:00:00:00:00:04"}] == 0} {
            if {[setAndCheckAttributeValue $mp "enabled" {"True" y}] == 1} {
                puts "Falied to disable MP with Mac Address 00:00:00:00:00:04"
            }
        }
    }

    after 2000

    set filter {userMdLevel 1}
    set checkInLearntInfoList {{"VLANID 1 TPID 0x8100 Priority 0" \
                        "VLANID 22 TPID 0x8100 Priority 2" 1 "00:00:00:00:00:04" \
                        4 false false false false false false false 0 false "1 sec" \
                        2 "Ixia-0" 4 "Ixiacom-1"}}
    puts "Searching in CCM Database . . ."
    if {[checkCfmCcmLearnedInfo $cfmbridge1 $filter $checkInLearntInfoList] == 1} {
        puts "All requested Infos are not available in CFM CCM Database"
        ixNetCleanUp
        return $FAILED
    }
    puts "Stoping CFM/PBT ... "
    ixNet exec stop $vPort1/protocols/cfm
    ixNet exec stop $vPort2/protocols/cfm

    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
