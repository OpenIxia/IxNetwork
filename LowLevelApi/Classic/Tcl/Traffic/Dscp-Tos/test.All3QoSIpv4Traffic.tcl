source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl


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

    # Source Traffic common utility files
    source $::pwd/trafficUtil.tcl

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
    if  {[catch {source "$::pwd/config.All3QoSIpv4Traffic.tcl"} err]} {
        puts $err
        puts "Loading Scriptgen config file config.All3QoSIpv4Traffic.tcl "
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

    #Enabling Capture on ports
    ixNet setAttribute $vPort2 -rxMode capture
    ixNet setAttribute $vPort2/capture -hardwareEnabled true
    ixNet commit

    # capture cleanup
    if {[catch {ixNet exec closeAllTabs} err] == 1} {
        puts "Failed to close existing analyser tabs "
    }
    after 2000

    # Traffic Start
    if [generateApplyTraffic] {
        puts "Failed to start traffic"
        ixNetCleanUp
        return $FAILED
    }
    puts "Traffic applied successfully"

    #Start the capture
    puts "Start Capturing packets"
    if { [catch {ixNet exec startCapture} err] } {
        puts "Start Capture failed"
        ixNetCleanUp
        return $FAILED
    }
    after 2000

    if [startTraffic] {
        puts "Failed to start the traffic"
        ixNetCleanUp
        return $FAILED
    }
    puts "Traffic started successfully"

    #Wait for Traffic to be sent for 1 iteration
    puts "Waiting 30 Sec for Traffic to be sent ..."
    after 30000

    # Traffic Stop
    if [stopTraffic] {
        puts "Failed to stop traffic"
        ixNetCleanUp
        return $FAILED
    }
    puts "Traffic stopped successfully"

    # Stop the capture
    puts "Stopping the capture"
    if { [catch {ixNet exec stopCapture} err] } {
        puts "Capture stop failed"
    }
    after 2000

    # Check for Configured TOS in captured packet
    foreach {type tos} { Precedence-0 "00" \
                         Precedence-1 "20" \
                         Precedence-2 "40" \
                         Precedence-3 "60" \
                         Precedence-4 "80" \
                         Precedence-5 "A0" \
                         Precedence-6 "C0" \
                         Precedence-7 "E0" \
                         Default    "00" \
                         AF11       "28" \
                         AF12       "30" \
                         AF13       "38" \
                         AF21       "48" \
                         AF22       "50" \
                         AF23       "58" \
                         AF31       "68" \
                         AF32       "70" \
                         AF33       "78" \
                         AF41       "88" \
                         AF42       "90" \
                         AF43       "98" \
                         EF         "B8" \
                         CS1        "20" \
                         CS2        "40" \
                         CS3        "60" \
                         CS4        "80" \
                         CS5        "A0" \
                         CS6        "C0" \
                         CS7        "E0"} {
        set matchFieldList [subst {15   15   "$tos"}]
        if {[verifyCapturedPackets $chassisIp2 $card2 $port2 $matchFieldList] == 1} {
            puts "Expected field value match not found in capture buffer"
            ixNetCleanUp
            return $FAILED
        }
        puts "$type Packet received with TOS : $tos"
    }

    ixNetCleanUp
    return $PASSED

}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
