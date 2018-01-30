#!/usr/local/bin/tclsh

################################################################################
# File Name  :test.RsvpGRModel.tcl
# Author     :Manodipto Ghose
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


