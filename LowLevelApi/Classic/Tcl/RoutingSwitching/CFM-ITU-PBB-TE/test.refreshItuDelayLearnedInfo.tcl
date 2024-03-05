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

#-------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
#       To get ITU Delay Learnt info.
#
# SCRIPT-GEN USED : config.refreshItuDelayLearnedInfo.tcl
# IXNCFG USED     : No
#                   Configure 1 Bridge per port with 1 MEP per port with one
#                   link each on each port with VLAN  Keep the operation mode
#                   as CFM and the MD levels to be 0. MA name format Character
#                   Start the Protocol and send the DM and verify
#
# Sequence of events being carried out by the script
#   1) Load the config file
#   2) Start CFM protocol & Wait for some time
#   3) Set filter for retriving Delay Learnt Info
#   4) Refesh Delay Learnt Info
#   5) Verify Delay Learnt Info is retrieved
#   6) Stop CFM protocol
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
    puts "loading Scriptgen file ..."
    # load config files
    if  {[catch {source "$::pwd/config.refreshItuDelayLearnedInfo.tcl"} err]} {
        puts $err
        puts "Loading Scriptgen config file config.refreshItuDelayLearnedInfo.tcl "
        ixNetCleanUp
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

    puts "Starting CFM on both the ports.."
    ixNet exec start $vPort1/protocols/cfm
    ixNet exec start $vPort2/protocols/cfm
    puts "CFM protocols started"

    # Wait for Some time
    puts "Waiting for 10 seconds"
    after 10000

    set brobj [lindex [ixNet getList $vPort1/protocols/cfm bridge] 0]
    set filter {userDelayType               dm                  \
                userMdLevel                 0                   \
                userSelectSrcMepById        false               \
                userSrcMacAddress           00:00:00:00:00:01   \
                userSelectDstMepById        false               \
                userDstMacAddress           00:00:00:00:00:02   \
                userCvlan                   noVlanId            \
                userSvlan                   vlanId              \
                userSvlanTpId               0x8100              \
                userSvlanId                 1                   \
                userSvlanPriority           0                   }

    set checkInLearntInfoList {true -1 0 0}
    set try 0
    set isFound 0
    while {$try < 10 } {
        if {[checkItuDelayLearnedInfo $brobj $filter $checkInLearntInfoList] == 1} {
            puts "Try$try : Failed to retrieve requested delay information"
        } else {
           puts "Try$try : Retrieved requested delay information"
           set isFound 1
           break
       }
       after 2000
       incr try
    }
    if {$isFound == 0} {
        ixNetCleanUp
        return $FAILED
    }


    puts "Stoping CFM ... "
    ixNet exec stop $vPort1/protocols/cfm
    ixNet exec stop $vPort2/protocols/cfm
    after 2000

    ixNetCleanUp
    return $PASSED

}


#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
