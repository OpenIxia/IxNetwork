#!/usr/local/bin/tclsh

################################################################################
#File Name         : test.3.1_PktCRPAdv.tcl
#Author            : Deepak Kumar Singh
#Reviewer          : Jayasri Dhar
#Purpose           :
#Test Setup        : Configure on 1st port a C-RP range having 2 groups with /24
#                    mask and 2 RP addresses fully-meshed. Make 2nd port as E-BSR.
#Expected Result   : Capture packet and verify C-RP-Adv are unicast to E-BSR with
#                    source address as configured C-RP address. Verify C-RP-Adv
#                    format and group to RP mapping.
#Topology          : B2B
#ScriptGen         : No
################################################################################
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
    if  {[ixNet exec loadConfig [ixNet readFrom "$::pwd/config.3.1_PktCRPAdv.ixncfg"]] != "::ixNet::OK"} {
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


    #Starting the Test Execution

    # Capture cleanup
    if {[catch {ixNet exec closeAllTabs} err] == 1} {
        puts "Failed to close existing analyser tabs "
    }

    after 2000

    #Start the protocol
    puts "Starting Protocols"
    ixNet exec start $vPort1/protocols/pimsm
    ixNet exec start $vPort2/protocols/pimsm

    puts "Waiting for the BSM and C-RP Adv. packets to come..."
    after 30000

    #Start the capture
    #Capture is already enabled in the config file loaded
    puts "Capturing packets"
    catch {ixNet exec startCapture}

    after 15000
    #Stop capture
    puts "Stopping the capture"
    catch {ixNet exec stopCapture}

    #Check for the 1st CRP Advertisement on the 2nd port
    puts "Checking for the 1st CRP Adv in the capture"
    set pattern {26 34 "14 01 01 01 01 01 01 02 28" \
                      38 38 "02" \
                      39 39 "C0" \
                      40 41 "00 96" \
                      42 47 "01 00 14 01 01 01" \
                      48 55 "01 00 00 18 E2 01 01 00"
                      56 63 "01 00 00 18 E2 01 02 00"}
    set packet [verifyCapturedPackets $chassisIp2 $card2 $port2 $pattern]
    if {$packet == 1} {
        puts "Packets not found --failed!!"
        ixNetCleanUp
        return $FAILED
    }
    puts "1st CRP Adv packet found!!"

    #Check for the 2nd CRP Advertisement on the 2nd port
    puts "Checking for the 2nd CRP Adv in the capture"
    set pattern {26 34 "14 01 01 02 01 01 01 02 28" \
                      38 38 "02" \
                      39 39 "C0" \
                      40 41 "00 96" \
                      42 47 "01 00 14 01 01 02" \
                      48 55 "01 00 00 18 E2 01 01 00"
                      56 63 "01 00 00 18 E2 01 02 00"}
    set packet [verifyCapturedPackets $chassisIp2 $card2 $port2 $pattern]
    if {$packet == 1} {
        puts "Packets not found --failed!!"
        ixNetCleanUp
        return $FAILED
    }
    puts "2nd CRP Adv packet found!!"
    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
