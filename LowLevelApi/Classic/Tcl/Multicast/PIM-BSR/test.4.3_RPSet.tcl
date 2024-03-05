#!/usr/local/bin/tclsh
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

################################################################################
#File Name : test.4.3_RPSet.tcl
#Purpose   :
#Test Case : Configure 1 PIM router with BSR enabled on 1st port without any
#            C-RP range attached to it. Configure 1 PIM router on 2nd port without
#            BSR enabled and attach 2 C-RP ranges to 2nd port with same groups,
#            different  RPs with different priority. Start PIM protocol.
#Expected Result: Verify that lower priority C-RP is elected.
#Topology : B2B
#ScriptGen : No
################################################################################
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

proc Action {portData1 portData2} {

        # initialize return value
        set FAILED 1
        set PASSED 0

        # Source CFM common utility files
        source $::pwd/pimbsrUtils.tcl

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
        if  {[ixNet exec loadConfig [ixNet readFrom "$::pwd/config.4.3_RPSet.ixncfg"]] != "::ixNet::OK"} {
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

    # Starting the Test Execution
    puts "Starting PIM Protocol Operation..."
    ixNet exec start $vPort1/protocols/pimsm
    ixNet exec start $vPort2/protocols/pimsm

    puts "Waiting for RP learning..."
    after 30000

    set p2Rtr1 [ixNet getList $vPort2/protocols/pimsm router]
    set p2Iface1 [ixNet getList $p2Rtr1 interface]

    puts "Check for Elected BSR..."
    set checkBSRLearntInfoList {bsrAddress "1.1.1.1"   \
                                priority 64            \
                                ourBsrState "notStarted"}

    if {[getBSRInfo $p2Iface1 $checkBSRLearntInfoList] == 1} {
        puts "Elected BSR is Wrong!!"
        ixNetCleanUp
        return $FAILED
    }

    puts "Check for RP-set..."
    set checkRPLearntInfoList {groupAddress "226.1.1.1" \
                                crpAddress "10.1.1.1"   \
                                priority 192            }
    if {[getRPInfo $p2Iface1 $checkRPLearntInfoList] == 1} {
        puts "RP-set in IxNetwork is Wrong!!"
        ixNetCleanUp
        return $FAILED
    }

    puts "Decreasing 2nd CRP Range priority from default 192 to 150.. Disable/Enable"
    set p2crp2 [lindex [ixNet getList $p2Iface1 crpRange] 1]
    if {[setAndCheckAttributeValue $p2crp2 "priorityValue" { 150 y }] == 1} {
        ixNetCleanUp
        return $FAILED
    }
    if {[setAndCheckAttributeValue $p2crp2 "enabled" { "False" y }] == 1} {
        ixNetCleanUp
        return $FAILED
    }

    if {[setAndCheckAttributeValue $p2crp2 "enabled" { "True" y }] == 1} {
        ixNetCleanUp
        return $FAILED
    }

    puts "Waiting for RP learning..."
    after 30000

    set checkBSRLearntInfoList {bsrAddress "1.1.1.1"   \
                                priority 64            \
                                ourBsrState "notStarted"}

    puts "Check for Elected BSR..."
    if {[getBSRInfo $p2Iface1 $checkBSRLearntInfoList] == 1} {
        puts "Elected BSR is Wrong!!"
        ixNetCleanUp
        return $FAILED
    }

    puts "Check for RP-set in IxNetwork..."
    set checkRPLearntInfoList {groupAddress "226.1.1.1"  \
                                   crpAddress "20.1.1.1" \
                                   priority 150          }
    if {[getRPInfo $p2Iface1 $checkRPLearntInfoList] == 1} {
       puts "RP-set in IxNetwork is Wrong!!"
       ixNetCleanUp
       return $FAILED
    }

    puts "Increasing 2nd CRP Range priority from 150 to 200.. Disable/Enable"
    if {[setAndCheckAttributeValue $p2crp2 "priorityValue" { 200 y }] == 1} {
        ixNetCleanUp
        return $FAILED
    }
    if {[setAndCheckAttributeValue $p2crp2 "enabled" { "False" y }] == 1} {
        ixNetCleanUp
        return $FAILED
    }

    if {[setAndCheckAttributeValue $p2crp2 "enabled" { "True" y }] == 1} {
        ixNetCleanUp
        return $FAILED
    }

    puts "Waiting for RP learning..."
    after 30000

    set checkBSRLearntInfoList {bsrAddress "1.1.1.1" \
                                priority 64 \
                                ourBsrState "notStarted" }
    puts "Check for Elected BSR..."
    if {[getBSRInfo $p2Iface1 $checkBSRLearntInfoList] == 1} {
        puts "Elected BSR is Wrong!!"
        ixNetCleanUp
        return $FAILED
    }

    puts "Check for RP-set in IxNetwork..."
    set checkRPLearntInfoList {groupAddress "226.1.1.1" \
                                crpAddress "10.1.1.1" \
                                priority 192 }
    if {[getRPInfo $p2Iface1 $checkRPLearntInfoList] == 1} {
        puts "RP-set in IxNetwork is Wrong!!"
        ixNetCleanUp
        return $FAILED
    }

    puts "Always the lower priority C-RP is getting elected..."
    ixNetCleanUp
    return $PASSED

}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
