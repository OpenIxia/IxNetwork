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
# File Name  :test.RsvpGRModel.tcl
# Purpose    :Test Basic RSVP GR protocols with IxNetwork
#
################################################################################
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl


#Test case Starts
proc Action {portData1 portData2} {
    # initialize return value
    set FAILED 1
    set PASSED 0
    source $::pwd/statUtils.tcl
    source $::pwd/utils.rsvp.tcl
    # for packet capture you need to include this package
    if {[catch {package req IxTclHal}]} {
       puts "Error in including package IxTclHal"
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

    puts "load scriptgen file"

    if {[catch {source "$::pwd/config.rsvp-grModel.tcl"} error] } {
        puts "Error in sourcing the cnfig file "
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
                            [list $chassisIp2 $card2 $port2]]

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

    #Set Capture Attributes
    ixNet setAttr $vPort1/capture -hardwareEnabled true
    ixNet setAttr $vPort1/capture -softwareEnabled true
    ixNet setAttr $vPort2/capture -hardwareEnabled true
    ixNet setAttr $vPort2/capture -softwareEnabled true
    ixNet commit

    puts "Starting the capture"
    ixNet exec startCapture

    puts "Starting Protocols"

    ixNet exec start $vPort2/protocols/rsvp
    after 2000
    ixNet exec start $vPort1/protocols/rsvp

    puts "Waiting for LSPs to come up"
    after 10000

    #get rsvp
    set rsvp2 $vPort2/protocols/rsvp
    set rsvp1 $vPort1/protocols/rsvp

    #start protocol
    ixNet exec start $rsvp2
    ixNet exec start $rsvp1

    puts "Waiting for the neighbor adjacency to be established \
          and the stats to come up"
    after 15000


    set portList1 [list [list $chassisIp1 $card1 $port1]]
    set portList2 [list [list $chassisIp2 $card2 $port2]]


    for {set i 0} {$i<5} {incr i} {
        set neighborPair_($i) [lindex [ixNet getList $rsvp2 neighborPair] $i]
    }

    #--------------------------------Checking The Statistics-------------------
    set completeStats1 {"RSVP-TE Aggregated Peer Graceful-Restarts"       0 \
                        "RSVP-TE Aggregated Paths with Recovery-Label Tx" 0 }


    if {[checkAllRSVPStats_DefaultView $portList1 $completeStats1]} {
        puts "Failure: Did not get the expected value for the all stats"
        ixNetCleanUp
        return $FAILED
    }
    puts "Success: Got expected values for all the stats"

    set completeStats2 {"RSVP-TE Aggregated Own Graceful-Restarts"        0 \
                        "RSVP-TE Aggregated Paths with Recovery-Label Rx" 0}

    if {[checkAllRSVPStats_DefaultView $portList2 $completeStats2]} {
        puts "Failure: Did not get the expected value for the all stats"
        ixNetCleanUp
        return $FAILED
    }
    #---------------------------------------------------------------------------


    #Restart all the neighbors on the egress side
    for {set i 0} {$i<5} {incr i} {
        ixNet exec restartNeighbor $neighborPair_($i)
    }
    puts "Waiting for the label to be recovered"
    after 45000

    #--------------------------------After restart Checking The Statistics-----
    set completeStats1 {"RSVP-TE Aggregated Peer Graceful-Restarts"       5 \
                        "RSVP-TE Aggregated Paths with Recovery-Label Tx" 5 }


    if {[checkAllRSVPStats_DefaultView $portList1 $completeStats1]} {
        puts "Failure: Did not get the expected value for the all stats"
        ixNetCleanUp
       return $FAILED
    }
    puts "Success: Got expected values for all the stats"

    set completeStats2 {"RSVP-TE Aggregated Own Graceful-Restarts"        5 \
                        "RSVP-TE Aggregated Paths with Recovery-Label Rx" 5}

    if {[checkAllRSVPStats_DefaultView $portList2 $completeStats2]} {
        puts "Failure: Did not get the expected value for the all stats"
        ixNetCleanUp
       return $FAILED
    }
    #---------------------------------------------------------------------------

    puts "Going to check the Assigned Label info for the router \
          that have been restarted"
    set checkAssignedLabelInfo1 {reservationState "recovered" }
    puts "Retrieving Learned Info from the Restarting Router"
    for {set i 0} {$i<5} {incr i} {
        if {[getAssignedLabelInfo  $neighborPair_($i) \
                 $checkAssignedLabelInfo1] == 1} {
            puts "All requested Infos are not available in Assigned \
                  Label Learned Info List"
            ixNetCleanUp
            return $FAILED
        }
    }

    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action


