source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#-------------------------------------------------------------------------------
# Name          : test.SampleScript_MVPN_P2MP.tcl
# Author        : Deepak Kumar Singh
# Purpose       : Sample Script for MVPN-P2MP
# Test Setup    :
# Code Flow     : 1. Configure IXIA and DUT Ports
#                 2. Start Protocols and wait for sometime
#                 3. Verify various Protocol Stats
#                 4. Verify various BGP Learned Infos
#                 5. Apply/Start Traffic and wait for sometime
#                 6. Verify various Traffic Stats
#                 7. Stop Traffic
#                 8. Stop Protocols
#                 9. Clean IXIA and DUT Ports
# Topology      : B2B
# ixncfg used   : Yes (config.SampleScript_MVPN_P2MP.ixncfg)
# Scriptgen used: No
#-------------------------------------------------------------------------------

proc configureIxNetworkGui {} {
    set isError  [catch {ixNet exec loadConfig [ixNet readFrom \
                        $::pwd/config.SampleScript_MVPN_P2MP.ixncfg]} errmsg]
    if {$isError} {
        puts "$errmsg"
    }
}


# Main Action Proc
proc Action {portData1 portData2} {
    source $::pwd/MVPN-NewDraftUtils.tcl

    set FAILED 1
    set PASSED 0

    # get port info 1
    set chassisIp1 [getChassisIp $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    # get port info 2
    set chassisIp2 [getChassisIp  $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    # Hostname, where IxNetwork TCL-Server client runs
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

    # Configure IxNetwork GUI
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
    }

    # Check if the ports are assigned; if un-assigned re-assign them
    if {[ifUnassignedConnectAgain] == 1} {
        puts "Not able to re-assign the ports !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Ports are in assigned state !!!"
    after 5000

    # Check Ports Link Status
    puts "Checking Port Link Status ..."
    if {[ixTclNet::CheckLinkState $vPorts doneList]} {
        puts "Ports Link is down !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Ports Link is Up !!!"

    # Start Test Execution
    puts "Test execution Starts !!!"

    # Start Protocols
    puts "Starting Protocols ..."
    if {[ixNet exec startAllProtocols] != "::ixNet::OK"} {
        puts "Failed to start Protocols !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Protocols started successfully !!!"

    puts "Waiting for 30 sec ..."
    after 30000

    # Verify Protocol Statistics
    puts "Verifying Protocol Stats ..."

    set BGPStatsList {"Sess. Configured" 1 \
                      "Sess. Up"         1}

    set OSPFStatsList {"Sess. Configured" 1 \
                       "Full Nbrs."       1}

    set RSVPPort1StatsList {"Ingress LSPs Configured"    4 \
                            "Ingress LSPs Up"            4 \
                            "Ingress SubLSPs Configured" 3 \
                            "Ingress SubLSPs Up"         3 \
                            "Egress LSPs Up"             1}

    set RSVPPort2StatsList {"Ingress LSPs Configured" 1 \
                            "Ingress LSPs Up"         1 \
                            "Egress LSPs Up"          4 \
                            "Egress SubLSPs Up"       3}

    set BGPPortList [list [list $chassisIp1 $card1 $port1] \
                          [list $chassisIp2 $card2 $port2]]


    set OSPFPortList [list [list $chassisIp1 $card1 $port1] \
                           [list $chassisIp2 $card2 $port2]]


    set RSVPPort1PortList [list [list $chassisIp1 $card1 $port1]]
    set RSVPPort2PortList [list [list $chassisIp2 $card2 $port2]]

    # Check BGP Aggregated Statistics
    puts "Verifying BGP Aggregated Statistics ..."
    if {[checkAllProtocolStats $BGPPortList "BGP Aggregated Statistics" \
        $BGPStatsList]} {
        puts "Did not get the expected value for the all BGP stats !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected values for BGP stats !!!"
    after 5000

    # Check OSPF Aggregated Statistics
    puts "Verifying OSPF Aggregated Statistics ..."
    if {[checkAllProtocolStats $OSPFPortList "OSPF Aggregated Statistics" \
        $OSPFStatsList]} {
        puts "Did not get the expected value for the all OSPF stats !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected values for OSPF stats !!!"
    after 5000

    # Check RSVP Aggregated Statistics
    puts "Verifying RSVP Aggregated Statistics at Port 1 ..."
    if {[checkAllProtocolStats $RSVPPort1PortList "RSVP Aggregated Statistics" \
        $RSVPPort1StatsList]} {
        puts "Did not get the expected value for the all RSVP stats at Port 1"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected values for RSVP stats at Port 1 !!!"
    after 5000

    puts "Verifying RSVP Aggregated Statistics at Port 2 ..."
    if {[checkAllProtocolStats $RSVPPort2PortList "RSVP Aggregated Statistics" \
        $RSVPPort2StatsList]} {
        puts "Did not get the expected value for the all RSVP stats at Port 2"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected values for RSVP stats at Port 2 !!!"
    after 5000

    # Switch To S-PMSI
    puts "Switching To S-PMSI ..."
    set protocols $vPort1/protocols
    set bgp $protocols/bgp
    set neighborRangeList [ixNet getList $bgp neighborRange]
    if {[switchToSpmsi $neighborRangeList] == 1} {
        puts "Failed to Switch To S-PMSI !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Successfully Switch To S-PMSI !!!"
    after 5000

    # Verify BGP Learned Info for Port1
    set neighborRange1 [lindex $neighborRangeList 0]

    # Verify BGP IPv4 Multicast VPN Learned Info for Port 1
    puts "Verifying BGP IPv4 Multicast VPN Learned Info:I-PMSI AD for Port 1"
    set checkLearntInfoList {ipv4MulticastVpn \
             {routeType neighbor originatingRouter routeDistinguisher} \
             {{"I-PMSI A-D" "2.2.2.2" "2.3.2.2" "100:1"}}}

    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv4 Multicast\
              VPN Learned Info:I-PMSI AD for Port 1 !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected BGP IPv4 Multicast VPN Learned Info:I-PMSI AD for Port 1"
    after 5000

    puts "Verifying BGP IPv4 Multicast VPN Learned Info:Leaf AD for Port 1"
    set checkLearntInfoList {ipv4MulticastVpn \
             {routeType neighbor originatingRouter routeKeyOriginatingRouter \
              routeKeyRouteDistinguisher routeKeySourceAddress \
              routeKeyGroupAddress} \
             {{"Leaf A-D" "2.2.2.2" "2.3.2.2" "2.2.2.2" "100:1" \
               "100.0.0.1" "225.0.0.1"}}}

    if {[checkBGPLearnedInfo $neighborRange1 \
        $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv4 Multicast VPN \
              Learned Info:Leaf AD for Port 1 !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected BGP IPv4 Multicast VPN Learned Info:Leaf AD for Port 1"
    after 5000

    puts "Verifying BGP IPv4 Multicast VPN Learned Info:C-Multicast for Port 1"
    set checkLearntInfoList {ipv4MulticastVpn \
             {routeType neighbor routeDistinguisher sourceAs \
              sourceAddress groupAddress} \
             {{"C-Multicast" "2.2.2.2" "100:1" 100 "100.0.0.1" "225.0.0.1"}}}

    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv4 Multicast \
              VPN Learned Info:C-Multicast for Port 1 !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected BGP IPv4 Multicast VPN Learned Info:C-Multicast for Port 1"
    after 5000

    # Verify BGP IPv6 Multicast VPN Learned Info for Port 1
    puts "Verifying BGP IPv6 Multicast VPN Learned Info:I-PMSI AD for Port 1"
    set checkLearntInfoList {ipv6MulticastVpn \
             {routeType neighbor originatingRouter routeDistinguisher} \
             {{"I-PMSI A-D" "2.2.2.2" "2.3.2.2" "100:1"}}}

    if {[checkBGPLearnedInfo $neighborRange1 \
         $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv6 Multicast VPN Learned \
             Info:I-PMSI AD for Port 1 !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected BGP IPv6 Multicast VPN Learned Info:I-PMSI AD for Port 1"
    after 5000

    puts "Verifying BGP IPv6 Multicast VPN Learned Info:Leaf AD for Port 1"
    set checkLearntInfoList {ipv6MulticastVpn \
             {routeType neighbor originatingRouter routeKeyOriginatingRouter \
              routeKeyRouteDistinguisher routeKeySourceAddress \
              routeKeyGroupAddress} \
              {{"Leaf A-D" "2.2.2.2" "2.3.2.2" "2.2.2.2" "100:1" \
                "FEC0:0:0:0:0:0:0:1" "FF15:0:0:0:0:0:0:0"}}}

    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv6 Multicast \
             VPN Learned Info:Leaf AD for Port 1"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected BGP IPv6 Multicast VPN Learned Info:Leaf AD for Port"
    after 5000

    puts "Verifying BGP IPv6 Multicast VPN Learned Info:C-Multicast for Port 1"
    set checkLearntInfoList {ipv6MulticastVpn \
             {routeType neighbor routeDistinguisher sourceAs \
              sourceAddress groupAddress} \
              {{"C-Multicast" "2.2.2.2" "100:1" 100 "FEC0:0:0:0:0:0:0:1" \
                "FF15:0:0:0:0:0:0:0"}}}

    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv6 Multicast VPN \
              Learned Info:C-Multicast for Port 1"
        return $FAILED
    }
    puts "Got expected BGP IPv6 Multicast \
          VPN Learned Info:C-Multicast for Port 1"
    after 5000

    ##### Verify BGP Learned Info for Port 2 #####
    set protocols $vPort2/protocols
    set bgp $protocols/bgp
    set neighborRangeList [ixNet getList $bgp neighborRange]
    set neighborRange1 [lindex $neighborRangeList 0]

    # Verify BGP IPv4 VPN Learned Info for Port 2
    puts "Verifying BGP IPv4 VPN Learned Info for Port 2 ..."
    set checkLearntInfoList {ipv4vpn \
                            {neighbor routeDistinguisher ipPrefix nextHop} \
                            {{"2.3.2.2" "100:1" "100.0.0.1" "2.2.2.2"}}}

    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv4 VPN Learned Info for Port 2"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected BGP IPv4 VPN Learned Info for Port 2 !!!"
    after 5000

    # Verify BGP IPv6 VPN Learned Info for Port 2
    puts "Verifying BGP IPv6 VPN Learned Info for Port 2 ..."
    set checkLearntInfoList {ipv6vpn \
             {neighbor routeDistinguisher ipPrefix nextHop} \
             {{"2.3.2.2" "100:1" "FEC0:0:0:0:0:0:0:1" \
               "0:0:0:0:0:FFFF:202:202"}}}

    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv6 VPN Learned Info for Port 2"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected BGP IPv6 VPN Learned Info for Port 2 !!!"
    after 5000

    # Verify BGP IPv4 Multicast VPN Learned Info for Port 2
    puts "Verifying BGP IPv4 Multicast VPN Learned Info:I-PMSI AD for Port 2"
    set checkLearntInfoList {ipv4MulticastVpn \
             {routeType neighbor originatingRouter routeDistinguisher \
              tunnelType rsvpP2mpExtendedTunnelId rsvpP2mpTunnelId \
              rsvpP2mpId upstreamLabel} \
             {{"I-PMSI A-D" "2.3.2.2" "2.2.2.2" "100:1" 1 "2.2.2.2" 1 1 0}}}

    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv4 Multicast VPN \
              Learned Info:I-PMSI AD for Port 2 !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected BGP IPv4 Multicast VPN Learned Info:I-PMSI AD for Port 2"
    after 5000

    puts "Verifying BGP IPv4 Multicast VPN Learned Info:S-PMSI AD for Port 2"
    set checkLearntInfoList {ipv4MulticastVpn \
             {routeType neighbor originatingRouter routeDistinguisher \
              sourceAddress groupAddress tunnelType rsvpP2mpExtendedTunnelId \
              rsvpP2mpTunnelId rsvpP2mpId upstreamLabel} \
             {{"S-PMSI A-D" "2.3.2.2" "2.2.2.2" "100:1" "100.0.0.1" \
               "225.0.0.1" 1 "2.2.2.2" 2 2 0}}}

    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv4 Multicast VPN \
             Learned Info:S-PMSI AD for Port 2"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected BGP IPv4 Multicast VPN Learned Info:S-PMSI AD for Port 2"
    after 5000

    puts "Verifying BGP IPv4 Multicast VPN Learned Info:Source \
          Active AD for Port 2"
    set checkLearntInfoList {ipv4MulticastVpn \
             {routeType neighbor routeDistinguisher sourceAddress groupAddress} \
             {{"Source Active A-D" "2.3.2.2" "100:1" "100.0.0.1" "225.0.0.1"}}}

    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv4 Multicast VPN Learned \
             Info:Source Active AD for Port 2"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected BGP IPv4 Multicast VPN Learned Info:Source \
          Active AD for Port 2"
    after 5000

    # Verify BGP IPv6 Multicast VPN Learned Info for Port 2
    puts "Verifying BGP IPv6 Multicast VPN Learned Info:I-PMSI AD for Port 2 ..."
    set checkLearntInfoList {ipv6MulticastVpn \
             {routeType neighbor originatingRouter routeDistinguisher \
              tunnelType rsvpP2mpExtendedTunnelId rsvpP2mpTunnelId \
              rsvpP2mpId upstreamLabel} \
              {{"I-PMSI A-D" "2.3.2.2" "2.2.2.2" "100:1" 1 "2.2.2.2" 1 1 0}}}

    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv6 Multicast \
              VPN Learned Info:I-PMSI AD for Port 2"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected BGP IPv6 Multicast VPN Learned Info:I-PMSI AD for Port"
    after 5000

    puts "Verifying BGP IPv6 Multicast VPN Learned Info:S-PMSI AD for Port 2"
    set checkLearntInfoList {ipv6MulticastVpn \
             {routeType neighbor originatingRouter routeDistinguisher \
              sourceAddress groupAddress tunnelType rsvpP2mpExtendedTunnelId \
              rsvpP2mpTunnelId rsvpP2mpId} \
             {{"S-PMSI A-D" "2.3.2.2" "2.2.2.2" "100:1" "FEC0:0:0:0:0:0:0:1"\
               "FF15:0:0:0:0:0:0:0" 1 "2.2.2.2" 3 3}}}

    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv6 Multicast VPN Learned \
              Info:S-PMSI AD for Port 2 !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected BGP IPv6 Multicast VPN Learned \
          Info:S-PMSI AD for Port 2"
    after 5000

    puts "Verifying BGP IPv6 Multicast VPN Learned Info:Source \
          Active AD for Port 2"
    set checkLearntInfoList {ipv6MulticastVpn \
             {routeType neighbor routeDistinguisher \
              sourceAddress groupAddress} \
             {{"Source Active A-D" "2.3.2.2" "100:1" \
               "FEC0:0:0:0:0:0:0:1" "FF15:0:0:0:0:0:0:0"}}}

    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        puts "Did not get the expected BGP IPv6 Multicast VPN Learned \
             Info:Source Active AD for Port 2"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Got expected BGP IPv6 Multicast VPN Learned \
          Info:Source Active AD for Port 2"
    after 5000


    # Apply Traffic
    puts "Generating and Applying Traffic ..."
    set traffic [ixNet getRoot]/traffic
    if {[generateApplyTraffic] == 1} {
        puts "Failed to apply traffic !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Traffic applied successfully !!!"
    after 5000

    # Start Traffic
    puts "Starting Traffic ..."
    if {[startTraffic $traffic] == 1} {
        puts "Failed to start Traffic"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Traffic started successfully !!!"

    puts "Waiting for 1 min for the traffic to flow ..."
    after 60000

    #Verify Traffic Statistics
    set tolerance 1

    # Check Data Plane Port Statistics
    puts "Verifying Data Plane Port Statistics ..."
    set txPortList [subst {{[ixNet getAttr $vPort1 -name]}}]
    set rxPortList [subst {{[ixNet getAttr $vPort2 -name]}}]
    if {[checkAllPortTrafficStats "Data Plane Port Statistics" \
        $txPortList $rxPortList $tolerance] == 1} {
        puts "Not able to retrieve statistics values for Data plane traffic"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Data Plane Port Statistics is correct !!!"
    after 5000

    # Check Traffic Item Statistics
    puts "Verifying Traffic Item Statistics ..."
    if {[checkAllTrafficStats "Traffic Item Statistics" $tolerance] == 1} {
        puts "Not able to retrieve statistics values for \
             Traffic Item Statistics"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Traffic Item Statistics is correct !!!"
    after 5000

    # Check Flow Statistics
    puts "Verifying Flow Statistics ..."
    if {[checkAllTrafficStats "Flow Statistics" $tolerance] == 1} {
        puts "Not able to retrieve statistics values for Flow Statistics"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Flow Statistics is correct !!!"
    after 5000

    # Stop Traffic
    puts "Stopping Traffic ..."
    if {[stopTraffic $traffic] == 1} {
        puts "Failed to stop traffic"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Traffic stopped successfully !!!"
    after 5000

    # Stop Protocols
    puts "Stopping Protocols ..."
    if {[ixNet exec stopAllProtocols] != "::ixNet::OK"} {
        puts "Failed to stop Protocols !!!"
        #ixNetCleanUp
        return $FAILED
    }
    puts "Protocols stopped successfully !!!"
    after 5000

    # End Test Execution
    puts "MVPN New Draft: New TCL APIs are working fine !!!"
    puts "Test execution Ends !!!"

    # Cleanup
    #ixNetCleanUp
    return $PASSED
}


#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
