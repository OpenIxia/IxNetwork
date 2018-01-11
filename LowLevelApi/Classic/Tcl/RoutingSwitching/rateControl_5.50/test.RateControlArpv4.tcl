source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#------------------------------------------------------------------------------
# Name          : test.ARPRateControl_MaxRequestsPerSec.tcl
# Purpose       : Verifying ARP Rate Control: Max Requests Per Sec
# Test Setup    :
# Code Flow     : 1. Load config and assign real ports
#                 2. Set ARP Rate Control Parameters
#                 3. Clear Neighbor Table
#                 4. Start Capture at 1st port
#                 5. Send ARP from 2nd port and wait for sometime
#                 6. Stop Capture
#                 7. Verify ARP Rate
#                 8. Clean IXIA Ports
# Topoputsy      : B2B
# ixncfg used   : Yes (config.ARPRateControl_MaxRequestsPerSec.ixncfg)
# Scriptgen used: No
#------------------------------------------------------------------------------

###############################################################################
# PROCEDURE  : sendArp
# PURPOSE    : send ARP in loop for each interfaces
# PARAMETERS : vportList
# RETURN     : BOOL)    - 0 for Pass ~ 1 for Fail
###############################################################################
proc sendArp {vportList} {
    set isError 1
    foreach vport $vportList {
        set interfaceList [ixNet getList $vport interface]
        foreach interface $interfaceList {
            if {[ixNet exec sendArp $interface] != "::ixNet::OK"} {
                puts "Not able to send ARP for the Port: \
                     $vport Interface: $interface !!!"
                return $isError
            }
            puts "Send ARP successfully for the Port: \
                  $vport Interface: $interface !!!"
        }
    }

    set isError 0
    return $isError
}


proc configureIxNetworkGui {} {
    # get Root object
    set root [ixNet getRoot]

    # Add virual port1
    set vport1 [ixNet add $root vport]
    ixNet commit
    set vport1  [lindex [ixNet remapIds $vport1] 0]

    # Add virual port2
    set vport2 [ixNet add $root vport]
    ixNet commit
    set vport2  [lindex [ixNet remapIds $vport2] 0]

    # add 50 connected interface on virtual port 1
    for {set i 1} {$i <= 50} {incr i} {

        # add interface
        set intf [ixNet add $vport1 interface]
        ixNet setAttr $intf -enabled true
        ixNet commit
        set intf [lindex [ixNet remapIds $intf] 0]

        # add ip address on in the interface
        set ipAddress "1.1.1.$i"
        set gateway   "1.1.2.$i"
        set maskWidth 16

        set ipv4 [ixNet add $intf ipv4]
        ixNet setAttr $ipv4 -ip $ipAddress
        ixNet setAttr $ipv4 -gateway $gateway
        ixNet setAttr $ipv4 -maskWidth $maskWidth
        ixNet commit
    }

    # add 50 connected interface on virtual port 2
    for {set i 1} {$i <= 50} {incr i} {

        # add interface
        set intf [ixNet add $vport2 interface]
        ixNet setAttr $intf -enabled true
        ixNet commit
        set intf [lindex [ixNet remapIds $intf] 0]

        # add ip address on in the interface
        set ipAddress "1.1.2.$i"
        set gateway   "1.1.1.$i"
        set maskWidth 16

        set ipv4 [ixNet add $intf ipv4]
        ixNet setAttr $ipv4 -ip $ipAddress
        ixNet setAttr $ipv4 -gateway $gateway
        ixNet setAttr $ipv4 -maskWidth $maskWidth
        ixNet commit
    }

    # enable arp and ping on virtual port1
    set arp1  $vport1/protocols/arp
    set ping1 $vport1/protocols/ping

    ixNet setAttr $arp1 -enabled true
    ixNet setAttr $ping1 -enabled true
    ixNet commit

    # enable arp and ping on virtual port1
    set arp2  $vport2/protocols/arp
    set ping2 $vport2/protocols/ping

    ixNet setAttr $arp2 -enabled true
    ixNet setAttr $ping2 -enabled true
    ixNet commit

    # set global interface options
    set globalInterfaceOption $root/globals/interfaces
    ixNet setAttr $globalInterfaceOption -arpOnLinkup False
    ixNet setAttr $globalInterfaceOption -nsOnLinkup False
    ixNet setAttr $globalInterfaceOption -sendSingleArpPerGateway True
    ixNet setAttr $globalInterfaceOption -sendSingleNsPerGateway True
    ixNet commit

    # set rate control parameters port1
    set rateControlP1 $vport1/rateControlParameters
    ixNet setAttr $rateControlP1 -maxRequestsPerBurst 5
    ixNet setAttr $rateControlP1 -maxRequestsPerSec 10
    ixNet setAttr $rateControlP1 -minRetryInterval 10
    ixNet setAttr $rateControlP1 -retryCount 3
    ixNet setAttr $rateControlP1 -sendInBursts False
    ixNet commit

    # set rate control parameters port2
    set rateControlP2 $vport2/rateControlParameters
    ixNet setAttr $rateControlP2 -maxRequestsPerBurst 5
    ixNet setAttr $rateControlP2 -maxRequestsPerSec 10
    ixNet setAttr $rateControlP2 -minRetryInterval 10
    ixNet setAttr $rateControlP2 -retryCount 3
    ixNet setAttr $rateControlP2 -sendInBursts False
    ixNet commit
}

proc Action {portData1 portData2} {
    # Initialize return value
    source $::pwd/rateControlUtils.tcl

    set FAILED 1
    set PASSED 0

    # Get IXIA Ports Info
    set chassisIp1 [getChassisIp $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    set chassisIp2 [getChassisIp $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    ## Hostname, where IxNetwork TCL-Server client runs
    set hostName [lindex [getHostName $portData1] 0]

    # Version Number (IxNetwork Major version No i.e. 5.50)
    set version "5.50"

    # connect to client
    if {[ixNet connect $hostName -version 5.50] != "::ixNet::OK"} {
        puts "Test case failed unable to connect to IxNetwork"
        return $FAILED
    }

    # clean up config
    ixNet exec newConfig

    # Load the Test Config
    configureIxNetworkGui

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2]]

    # get root object
    set root [ixNet getRoot]

    # Assign real ports to virtual ports
    puts "getting virtual ports ...."
    set vPorts [ixNet getList $root vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]

    # enable NS on Link Up option
    set globals $root/globals
    set interfaces $globals/interfaces
    ixNet setAttr $interfaces -nsOnLinkup true
    ixNet commit

    # Assign virtual ports to real ports
    puts "Assign virtual ports to real ports ..."
    if {[catch {ixTclNet::AssignPorts $realPortsList {} $vPorts}]} {
        puts "Error in assigning ports"
        ixNet exec newConfig
        return $FAILED
    }

    # Clear Neighbor Table
    if {[ixNet exec clearNeighborTable $vPort1] != "::ixNet::OK-{kBool,true}" || \
        [ixNet exec clearNeighborTable $vPort2] != "::ixNet::OK-{kBool,true}"} {
        puts "Failed to Clear Neighbor Table !!!"
        ixNet exec newConfig
        return $FAILED
    }
    puts "Clear Neighbor Table successfully !!!"
    after 5000

    # Enable Capture Mode
    puts "Enabling Capture Mode ..."
    if {[enableCaptureMode $vPort1] == 1} {
        puts "Failed to enable Capture Mode !!!"
        ixNet exec newConfig
        return $FAILED
    }
    puts "Capture Mode enabled successfully !!!"
    after 5000

    # Start Capture
    puts "Starting the capture ..."
    if {[ixNet exec startCapture] != "::ixNet::OK"} {
        puts "Failed to start packet capture !!!"
        ixNet exec newConfig
        return $FAILED
    }
    puts "Capture started successfully !!!"
    after 5000

    # Transmit ARP
    puts "Sending ARP for all the interfaces ..."
    if {[sendArp $vPort2] == 1} {
        puts "Not able to send ARP for all interfaces !!!"
        ixNet exec newConfig
        return $FAILED
    }
    puts "ARP sent successfully for all the interfaces !!!"

    puts "Waiting for 15 sec ..."
    after 15000

    # Stop Capture
    puts "Stopping the capture ..."
    if {[ixNet exec stopCapture] != "::ixNet::OK"} {
        puts "Failed to stop packet capture !!!"
        ixNet exec newConfig
        return $FAILED
    }
    puts "Capture stopped successfully !!!"
    after 5000

    # ARP Rate Control Verification
    puts "Verifying ARP Rate at Port1 ..."
    set matchFieldList {0  5  "FF FF FF FF FF FF"\
                        12 13 "08 06"}

    set expPktCount 50
    set rateList {10 1}
    if {[checkRateControlThroughCapture $chassisIp1 \
                                        $card1 \
                                        $port1 \
                                        $matchFieldList \
                                        $expPktCount \
                                        $rateList] == 1} {
        error "xxx"
        puts "ARP Rate is not correct at Port1 !!!"
        ixNet exec newConfig
        return $FAILED
    }
    puts "ARP rate is correct at Port1 !!!"

    # End Test Execution
    puts "ARP Rate Control is working fine in IxNetwork !!!"
    puts "Test execution Ends !!!"

    # Cleanup
    ixNet exec newConfig
    return $PASSED
}


#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
