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

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#------------------------------------------------------------------------------
# Name                    : test.10.1_RSVPlRateControl.tcl
#
# Purpose                 : Automate RSBP PORT Rate Control Functionality
#
# Configuration Procedure : 1. Configure RSVP-TE P2P through Wizard.
#                         : 2. Enable 1 Neighbor Pair with 5 Tunnel Head
#                         :    Range and Tail Ranges.
#                         : 3. Configure 10000 LSPs per Neighbor Pair.
#                         : 4. Configure Max LSP Initiations per sec=5
# Verification steps      : 1. Enable the packet capture and run the protocol.
#                         : 2. Verify the Expected Results step.
#                         : 3. Disable/Enable the Neighbor pair and again
#                              observe in capture.
#                         : 4. Verify the Expected Results step.
#
# Expected Results        : 1. After the protocol is started, stop the packet
#                         :    capture after 15 secs.
#                         :    Verify that the initial Path Messages send
#                         :    follow the Rate Control configured,
#                         :    i.e. 1 Path per sec. Verify the stat field
#                         :     "Rate Control Blocked LSP Setup".
#                         : 2. After Neighbor Pair is disabled/enabled, stop
#                         :    the packet capture after 15 secs.
#                         :    Verify that the initial Path Messages send
#                         :    follow the Rate Control configured, i.e.
#                         :    1 Path per sec. Verify the stat field
#                         :    "Rate Control Blocked LSP Setup".
# Config Format           :    ixncfg used
#------------------------------------------------------------------------------
proc Action {portData1 portData2} {
    source $::pwd/rateControlUtils.tcl

    # initialize return value
    set FAILED 1
    set PASSED 0

    # Get real card1/port1 from portData
    set chassisIp1 [getChassisIp $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    # Get real card2/port2 from portData
    set chassisIp2 [getChassisIp $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    # Hostname, where IxNetwork TCL-Server client runs
    set tclPublisherVersion "5.50"
    set hostName [lindex [getHostName $portData1] 0]
    set connection_Result [connectToClient $portData1 $portData2 \
                                           $tclPublisherVersion]

    log "Connection Result: $connection_Result"
    if {[string equal $connection_Result "::ixNet::OK"] != 1} {
        log "connection to client unsuccessful"
        return $FAILED
    }
    log "connectToClient Successful"

    # clean up all the existing configurations from client
    log "cleaning up the client"
    #ixNetCleanUp
    after 2000

    # load config files
    set configFileName config.[getTestId].ixncfg
    if  {[ixNet exec loadConfig [ixNet readFrom $::pwd/$configFileName]] \
         != "::ixNet::OK"} {
        log "Loading IxNetwork config file : Failed "
        #ixNetCleanUp
        return $FAILED
    }
    log "Loading IxNetwork config file : Passed"

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2]]

    # Assign real ports to virtual ports
    log "getting virtual ports ...."
    set vPorts  [ixNet getList [ixNet getRoot] vport]
    set vPort1  [lindex $vPorts 0]
    set vPort2  [lindex $vPorts 1]
    log "Virtual ports are = $vPorts"

    # Assign virtual ports to real ports
    log "Assign virtual ports to real ports ..."
    set force true
    set status  [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    log "Assigned: $status"
    if {[string equal [lindex $status 0]  $vPort1] != 1 || \
        [string equal [lindex $status 1]  $vPort2] != 1} {
        #ixNetCleanUp
        return $FAILED
    }
    ixTclNet::CheckLinkState $vPorts doneList
    after 2000

    # Enable & Start Capture
    log "Enable & Start Capture..."
    if {[enableCaptureMode $vPorts] == 1} {
        log "Failed to enable capture..."
        #ixNetCleanUp
        return $FAILED
    }

    puts "Starting the capture ..."
    ixNet exec startCapture

    puts "Capture started successfully !!!"
    after 5000

    # Start Protocols
    log "Starting protocol rsvp ..."
    if {([ixNet exec start $vPort1/protocols/rsvp] != "::ixNet::OK")} {
        log "Failed to start protocol rsvp on port1 ..."
        #ixNetCleanUp
        return $FAILED
    }

    after 5000

    if {([ixNet exec start $vPort2/protocols/rsvp] != "::ixNet::OK")} {
        log "Failed to start protocol rsvp on port2 ..."
        #ixNetCleanUp
        return $FAILED
    }
    log "Starting protocol ospf ..."

    if {([ixNet exec start $vPort1/protocols/ospf] != "::ixNet::OK") || \
        ([ixNet exec start $vPort2/protocols/ospf] != "::ixNet::OK")} {
        log "Failed to start protocol ospf ..."
        #ixNetCleanUp
        return $FAILED
    }

    log "Protocol started. Waiting for 120 Sec for protocol Sessions to be up.."
    after 120000

    # Stop Capture
    ixNet exec stopCapture

    # Verify Stats
    log "Verifying rsvp  protocol stats ..."
    set rsvpStatsListPort1 {"Egress LSPs Up" 1}

    set portList1 [list [list $chassisIp1 $card1 $port1]]
    if {[checkAllProtocolStats $portList1 "RSVP Aggregated Statistics" \
             $rsvpStatsListPort1]} {
        log "Did not get the expected rsvp protocol stats value..."
        #ixNetCleanUp
        return $FAILED
    }

    set rsvpStatsListPort2 {"Ingress LSPs Configured"        1 \
                            "Ingress LSPs Up"                1 \
                            "Rate Control Blocked LSP Setup" 1}

    set portList2 [list [list $chassisIp2 $card2 $port2]]
    if {[checkAllProtocolStats $portList2  "RSVP Aggregated Statistics" \
             $rsvpStatsListPort2]} {
        log "Did not get the expected rsvp protocol stats value..."
        #ixNetCleanUp
        return $FAILED
    }
    log "Got expected rsvp protocol stats values..."

    # Verify rsvp LSP's in captured packet
    log "Checking for rsvp  in Captured Pkt..."
    set lspMatchFieldList {38 39 "10 01"}

    set rateList [subst {5 1}]
    set expectedPktCount [expr 5 * 5]

    if {[checkRateControlThroughCapture $chassisIp1 $card1 $port1 \
         $lspMatchFieldList $expectedPktCount $rateList] == 1} {
        log "1 rsvp LSP Rate is not per configuration !!!"
        #ixNetCleanUp
        return $FAILED
    }

    # Enable the packet capture
    ixNet exec startCapture

    # Disable/Enable the neighborPair simultaneously.
    log "Disabling the neighborPair."

    foreach vPort $vPorts {
        set proto $vPort/protocols/rsvp
        set  neighborPair [ixNet getList $proto neighborPair]
        if {[setAndCheckAttributeValue $neighborPair \
            "enabled" {"false" y}] == 1} {
            log "Failed to disable neighborPair!!!"
            #ixNetCleanUp
            return $FAILED
        }

    }
    log "Waiting for 30 Sec..."
    after 30000

    log "Enabling the neighborPair."
    foreach vPort $vPorts {
        set proto $vPort/protocols/rsvp
        set  neighborPair [ixNet getList $proto neighborPair]
        if {[setAndCheckAttributeValue $neighborPair \
            "enabled" {"true" y}] == 1} {
            log "Failed to enable neighborPair!!!"
            #ixNetCleanUp
            return $FAILED
        }
    }
    log "Protocol started. Waiting for 30 Sec for protocol Sessions to be up"
    after 30000

    # Stop Capture
    ixNet exec stopCapture


    # Verify Stats
    log "Verifying rsvp  protocol stats ..."
    set rsvpStatsListPort1 {"Egress LSPs Up" 1}

    set portList1 [list [list $chassisIp1 $card1 $port1]]
    if {[checkAllProtocolStats $portList1 "RSVP Aggregated Statistics" \
              $rsvpStatsListPort1]} {
        log "Did not get the expected rsvp protocol stats value..."
        #ixNetCleanUp
        return $FAILED
    }

    set rsvpStatsListPort2 {"Ingress LSPs Configured"        1 \
                            "Ingress LSPs Up"                1 \
                            "Rate Control Blocked LSP Setup" 1}

    set portList2 [list [list $chassisIp2 $card2 $port2]]
    if {[checkAllProtocolStats $portList2 "RSVP Aggregated Statistics" \
              $rsvpStatsListPort2 $tclPublisherVersion]} {
        log "Did not get the expected rsvp protocol stats value..."
        #ixNetCleanUp
        return $FAILED
    }
    log "Got expected rsvp protocol stats values..."

    # Stop Protocols
    log "Stopping protocol rsvp ..."
    if {([ixNet exec stop $vPort1/protocols/rsvp] != "::ixNet::OK") || \
        ([ixNet exec stop $vPort2/protocols/rsvp] != "::ixNet::OK")} {
        log "Failed to stop protocol rsvp ..."
        #ixNetCleanUp
        return $FAILED
    }

    log "Stopping protocol ospf ..."
    if {([ixNet exec stop $vPort1/protocols/ospf] != "::ixNet::OK") || \
        ([ixNet exec stop $vPort2/protocols/ospf] != "::ixNet::OK")} {
        log "Failed to stop protocol ospf ..."
        #ixNetCleanUp
        return $FAILED
    }

    # Verify rsvp LSP's in captured packet
    log "Checking for rsvp in Captured Pkt..."
    if {[checkRateControlThroughCapture $chassisIp1 $card1 $port1 \
             $lspMatchFieldList $expectedPktCount $rateList] == 1} {
        log "2 rsvp LSP Rate is not per configuration!!!"
        #ixNetCleanUp
        return $FAILED
    }

    # Cleanup
    #ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action