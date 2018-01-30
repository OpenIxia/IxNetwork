source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#------------------------------------------------------------------------------
# Name          : test.3.2_BGP-AD-LDP-SIG_Functionality.tcl
# Purpose       : Verifying BGP-AD-LDP-SIG Functionality
# Test Setup    : Configure BGP AD LDP SIG VPLS with OSPF/RSVP-TE 1 P, 1 PE per
#                 P, 1 VPLS per PE router, set VSI ID with "IP" option and VC
#                 Type VLAN. Enable packet capture. Send interleaved stream of
#                 increment byte payload traffic between PE.
# Code Flow     : 1. Configure IXIA Ports
#                 2. Start Protocols and wait for sometime
#                 3. Verify Protocol Stats/Protocol Learned Info
#                 4. Start Traffic and wait for sometime
#                 5. Verify various Traffic Stats
#                 6. Stop Traffic/Protocols
#                 7. Clean IXIA Ports
# Topology      : B2B
# ixncfg used   : Yes (config.3.2_BGP-AD-LDP-SIG_Functionality.ixncfg)
# Scriptgen used: No
#------------------------------------------------------------------------------

proc configureIxNetworkGui {} {
    set configFileName "config.3.2_BGP-AD-LDP-SIG_Functionality.ixncfg"
    set isError [catch {ixNet exec loadConfig \
        [ixNet readFrom $::pwd/$configFileName]} errMsg]
    puts "Error in configuring GUI"
}

# Main Action Proc
proc Action {portData1 portData2} {
    source $::pwd/BGP-AD-LDP-SigUtils.tcl

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

    # Start Test Execution
    log "Test execution Starts !!!"

    # Start Protocols
    log "Starting Protocols ..."
    if {[ixNet exec startAllProtocols] != "::ixNet::OK"} {
        log "Failed to start Protocols !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Protocols started successfully !!!"

    log "Waiting for 30 sec for the Control Plane to get established ..."
    after 30000

    # Verify Protocol Statistics
    log "Verifying Protocol Stats ..."

    set BGPStatsList {"Sess. Configured" 16 \
                      "Sess. Up"         16}

    set LDPStatsList {"Basic Sess. Up"           4 \
                      "Targeted Sess. Up"       16 \
                      "Operational State Count" 20 \
                      "Established LSP Ingress" 80 \
                      "Established LSP Egress"  80}

    set OSPFStatsList {"Sess. Configured" 4 \
                       "Full Nbrs."       4}

    set portList [list [list $chassisIp1 $card1 $port1] \
                       [list $chassisIp2 $card2 $port2]]

    # Check BGP Aggregated Statistics
    log "Verifying BGP Aggregated Statistics ..."
    if {[checkAllProtocolStats $portList "BGP Aggregated Statistics" \
         $BGPStatsList]} {
        log "Did not get the expected value for BGP stats !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected values for BGP stats !!!"
    after 5000

    # Check LDP Aggregated Statistics
    log "Verifying LDP Aggregated Statistics ..."
    if {[checkAllProtocolStats $portList "LDP Aggregated Statistics" \
        $LDPStatsList]} {
        log "Did not get the expected value for LDP Stats !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected values for LDP Stats !!!"
    after 5000

    # Check OSPF Aggregated Statistics
    log "Verifying OSPF Aggregated Statistics ..."
    if {[checkAllProtocolStats $portList "OSPF Aggregated Statistics" \
        $OSPFStatsList]} {
        log "Did not get the expected value for OSPF stats !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected values for OSPF stats !!!"
    after 5000

    # Verify BGP: AD VPLS Learned Info
    # Verify BGP: AD VPLS Learned Info at Port1
    log "Verifying BGP: AD VPLS Learned Info at Port1 ..."
    set protocols $vPort1/protocols
    set bgp $protocols/bgp
    set neighborRangeList [ixNet getList $bgp neighborRange]

    # Verify BGP: AD VPLS Learned Info at Port1: Neighbor1
    log "Verifying BGP: AD VPLS Learned Info at Port1: Neighbor1 ..."
    set neighborRange1 [lindex $neighborRangeList 0]
    set checkLearntInfoList {adVpls \
                            {neighborAddress remoteVplsId supportedLocally remotePeAddress remoteVsiId routeDistinguisher routeTarget nextHopAddress} \
                            {{"2.2.2.2" "100:2" "True" "1.1.1.1" "500" "100:2" "100:2" "1.1.1.1"} \
                             {"2.2.2.2" "100:1" "True" "1.1.1.1" "500" "100:1" "100:1" "1.1.1.1"} \
                             {"2.2.2.2" "100:3" "True" "1.1.1.1" "500" "100:3" "100:3" "1.1.1.1"} \
                             {"2.2.2.2" "100:4" "True" "1.1.1.1" "500" "100:4" "100:4" "1.1.1.1"}}}
    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        log "Did not get expected BGP: AD VPLS Learned Info at Port1: Neighbor1 !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected BGP: AD VPLS Learned Info at Port1: Neighbor1 !!!"
    after 5000

    # Verify BGP: AD VPLS Learned Info at Port1: Neighbor16
    log "Verifying BGP: AD VPLS Learned Info at Port1: Neighbor16 ..."
    set neighborRange16 [lindex $neighborRangeList 15]
    set checkLearntInfoList {adVpls \
                            {neighborAddress remoteVplsId supportedLocally remotePeAddress remoteVsiId routeDistinguisher routeTarget nextHopAddress} \
                            {{"2.2.2.17" "100:2" "True" "1.1.1.16" "515" "100:2" "100:2" "1.1.1.16"} \
                             {"2.2.2.17" "100:1" "True" "1.1.1.16" "515" "100:1" "100:1" "1.1.1.16"} \
                             {"2.2.2.17" "100:3" "True" "1.1.1.16" "515" "100:3" "100:3" "1.1.1.16"} \
                             {"2.2.2.17" "100:4" "True" "1.1.1.16" "515" "100:4" "100:4" "1.1.1.16"}}}
    if {[checkBGPLearnedInfo $neighborRange16 $checkLearntInfoList] == 1} {
        log "Did not get expected BGP: AD VPLS Learned Info at Port1: Neighbor16 !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected BGP: AD VPLS Learned Info at Port1: Neighbor16 !!!"
    after 5000

    # Verify BGP: AD VPLS Learned Info at Port2
    log "Verifying BGP: AD VPLS Learned Info at Port2 ..."
    set protocols $vPort2/protocols
    set bgp $protocols/bgp
    set neighborRangeList [ixNet getList $bgp neighborRange]

    # Verify BGP: AD VPLS Learned Info at Port2: Neighbor1
    log "Verifying BGP: AD VPLS Learned Info at Port2: Neighbor1 ..."
    set neighborRange1 [lindex $neighborRangeList 0]
    set checkLearntInfoList {adVpls \
                            {neighborAddress remoteVplsId supportedLocally remotePeAddress remoteVsiId routeDistinguisher routeTarget nextHopAddress} \
                            {{"1.1.1.1" "100:2" "True" "2.2.2.2" "500" "100:2" "100:2" "2.2.2.2"} \
                             {"1.1.1.1" "100:1" "True" "2.2.2.2" "500" "100:1" "100:1" "2.2.2.2"} \
                             {"1.1.1.1" "100:3" "True" "2.2.2.2" "500" "100:3" "100:3" "2.2.2.2"} \
                             {"1.1.1.1" "100:4" "True" "2.2.2.2" "500" "100:4" "100:4" "2.2.2.2"}}}
    if {[checkBGPLearnedInfo $neighborRange1 $checkLearntInfoList] == 1} {
        log "Did not get expected BGP: AD VPLS Learned Info at Port2: Neighbor1 !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected BGP: AD VPLS Learned Info at Port2: Neighbor1 !!!"
    after 5000

    # Verify BGP: AD VPLS Learned Info at Port2: Neighbor16
    log "Verifying BGP: AD VPLS Learned Info at Port2: Neighbor16 ..."
    set neighborRange16 [lindex $neighborRangeList 15]
    set checkLearntInfoList {adVpls \
                            {neighborAddress remoteVplsId supportedLocally remotePeAddress remoteVsiId routeDistinguisher routeTarget nextHopAddress} \
                            {{"1.1.1.16" "100:2" "True" "2.2.2.17" "515" "100:2" "100:2" "2.2.2.17"} \
                             {"1.1.1.16" "100:2" "True" "2.2.2.17" "515" "100:2" "100:2" "2.2.2.17"} \
                             {"1.1.1.16" "100:2" "True" "2.2.2.17" "515" "100:2" "100:2" "2.2.2.17"} \
                             {"1.1.1.16" "100:2" "True" "2.2.2.17" "515" "100:2" "100:2" "2.2.2.17"}}}
    if {[checkBGPLearnedInfo $neighborRange16 $checkLearntInfoList] == 1} {
        log "Did not get expected BGP: AD VPLS Learned Info at Port2: Neighbor16 !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected BGP: AD VPLS Learned Info at Port2: Neighbor16 !!!"
    after 5000

    ##### Verify LDP: BGP AD VPLS Labels Learned Info #####
    # Verify LDP: BGP AD VPLS Labels Learned Info at Port1
    log "Verifying LDP: BGP AD VPLS Labels Learned Info at Port1 ..."
    set protocols $vPort1/protocols
    set ldp $protocols/ldp
    set routerList [ixNet getList $ldp router]

    # Verify LDP: BGP AD VPLS Labels Learned Info at Port1: Router2
    log "Verifying LDP: BGP AD VPLS Labels Learned Info at Port1: Router2 ..."
    set router2 [lindex $routerList 1]
    set checkLearntInfoList {{peerAddress vplsId sourceAii targetAii groupId label pwState localPwSubState remotePwSubState cBit mtu} \
                            {{"1.1.1.1" "100:1" "500" "500" "1" "16" "True" "0" "0" "False" "1500"} \
                             {"1.1.1.1" "100:2" "500" "500" "1" "17" "True" "0" "0" "False" "1500"} \
                             {"1.1.1.1" "100:3" "500" "500" "1" "18" "True" "0" "0" "False" "1500"} \
                             {"1.1.1.1" "100:4" "500" "500" "1" "19" "True" "0" "0" "False" "1500"}}}
    if {[checkLDP_BgpAdVplsLearnedInfo $router2 $checkLearntInfoList] == 1} {
        log "Did not get LDP: BGP AD VPLS Labels Learned Info at Port1: Router2 !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected LDP: BGP AD VPLS Labels Learned Info at Port1: Router2 !!!"
    after 5000

    # Verify LDP: BGP AD VPLS Labels Learned Info at Port1: Router20
    log "Verifying LDP: BGP AD VPLS Labels Learned Info at Port1: Router20 ..."
    set router20 [lindex $routerList 19]
    set checkLearntInfoList {{peerAddress vplsId sourceAii targetAii groupId label pwState localPwSubState remotePwSubState cBit mtu} \
                            {{"1.1.1.16" "100:1" "515" "515" "1" "16" "True" "0" "0" "False" "1500"} \
                             {"1.1.1.16" "100:2" "515" "515" "1" "17" "True" "0" "0" "False" "1500"} \
                             {"1.1.1.16" "100:3" "515" "515" "1" "18" "True" "0" "0" "False" "1500"} \
                             {"1.1.1.16" "100:4" "515" "515" "1" "19" "True" "0" "0" "False" "1500"}}}

    if {[checkLDP_BgpAdVplsLearnedInfo $router20 $checkLearntInfoList] == 1} {
        log "Did not get LDP: BGP AD VPLS Labels Learned Info at Port1: Router20 !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected LDP: BGP AD VPLS Labels Learned Info at Port1: Router20 !!!"
    after 5000

    # Verify LDP: BGP AD VPLS Labels Learned Info at Port2
    log "Verifying LDP: BGP AD VPLS Labels Learned Info at Port2 ..."
    set protocols $vPort2/protocols
    set ldp $protocols/ldp
    set routerList [ixNet getList $ldp router]

    # Verify LDP: BGP AD VPLS Labels Learned Info at Port2: Router2
    log "Verifying LDP: BGP AD VPLS Labels Learned Info at Port2: Router2 ..."
    set router2 [lindex $routerList 1]
    set checkLearntInfoList {{peerAddress vplsId sourceAii targetAii groupId label pwState localPwSubState remotePwSubState cBit mtu} \
                            {{"2.2.2.2" "100:1" "500" "500" "1" "16" "True" "0" "0" "False" "1500"} \
                             {"2.2.2.2" "100:2" "500" "500" "1" "17" "True" "0" "0" "False" "1500"} \
                             {"2.2.2.2" "100:3" "500" "500" "1" "18" "True" "0" "0" "False" "1500"} \
                             {"2.2.2.2" "100:4" "500" "500" "1" "19" "True" "0" "0" "False" "1500"}}}

    if {[checkLDP_BgpAdVplsLearnedInfo $router2 $checkLearntInfoList] == 1} {
        log "Did not get LDP: BGP AD VPLS Labels Learned Info at Port2: Router2 !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected LDP: BGP AD VPLS Labels Learned Info at Port2: Router2 !!!"
    after 5000

    # Verify LDP: BGP AD VPLS Labels Learned Info at Port2: Router20
    log "Verifying LDP: BGP AD VPLS Labels Learned Info at Port2: Router20 ..."
    set router20 [lindex $routerList 19]
    set checkLearntInfoList {{peerAddress vplsId sourceAii targetAii groupId label pwState localPwSubState remotePwSubState cBit mtu} \
                            {{"2.2.2.17" "100:1" "515" "515" "1" "16" "True" "0" "0" "False" "1500"} \
                             {"2.2.2.17" "100:2" "515" "515" "1" "17" "True" "0" "0" "False" "1500"} \
                             {"2.2.2.17" "100:3" "515" "515" "1" "18" "True" "0" "0" "False" "1500"} \
                             {"2.2.2.17" "100:4" "515" "515" "1" "19" "True" "0" "0" "False" "1500"}}}
    if {[checkLDP_BgpAdVplsLearnedInfo $router20 $checkLearntInfoList] == 1} {
        log "Did not get LDP: BGP AD VPLS Labels Learned Info at Port2: Router20 !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Got expected LDP: BGP AD VPLS Labels Learned Info at Port2: Router20 !!!"
    after 5000

    # Apply Traffic
    log "Generating and Applying Traffic ..."
    set traffic [ixNet getRoot]/traffic
    if {[generateApplyTraffic] == 1} {
        log "Failed to apply traffic !!!"
        clearAll $testDutConnElements
        return $FAILED
    }
    log "Traffic applied successfully !!!"
    after 5000

    # Start Traffic
    log "Starting Traffic ..."
    set traffic [ixNet getRoot]/traffic
    if {[startTraffic $traffic] == 1} {
        log "Failed to start Traffic !!!"
        clearAll $testDutConnElements
        return $FAILED
    }
    log "Traffic started successfully !!!"

    log "Waiting for 1 min ..."
    after 60000

    # Verify Traffic Statistics
    set tolerance 1
    # Check Data Plane Port Statistics
    log "Verifying Data Plane Port Statistics ..."
    set txPortList \
    [subst {{[ixNet getAttr $vPort1 -name]} {[ixNet getAttr $vPort2 -name]}}]

    set rxPortList \
    [subst {{[ixNet getAttr $vPort1 -name]} {[ixNet getAttr $vPort2 -name]}}]

    if {[checkAllPortTrafficStats "Data Plane Port Statistics" \
         $txPortList $rxPortList $tolerance] == 1} {
        log "Not able to retrieve statistics values for Data plane traffic"
        clearAll $testDutConnElements
        return $FAILED
    }
    log "Data Plane Port Statistics is correct !!!"
    after 5000

    # Check Traffic Item Statistics
    log "Verifying Traffic Item Statistics ..."
    if {[checkAllTrafficStats "Traffic Item Statistics" $tolerance] == 1} {
        log "Not able to retrieve statistics values for Traffic Item Statistics"
        clearAll $testDutConnElements
        return $FAILED
    }
    log "Traffic Item Statistics is correct !!!"
    after 5000

    # Check Flow Statistics
    log "Verifying Flow Statistics ..."
    if {[checkAllTrafficStats "Flow Statistics" $tolerance] == 1} {
        log "Not able to retrieve statistics values for Flow Statistics"
        clearAll $testDutConnElements
        return $FAILED
    }
    log "Flow Statistics is correct !!!"
    after 5000

    # Stop Traffic
    log "Stopping Traffic ..."
    if {[stopTraffic $traffic] == 1} {
        log "Failed to stop traffic"
        clearAll $testDutConnElements
        return $FAILED
    }
    log "Traffic stopped successfully !!!"
    after 5000

    # Stop Protocols
    log "Stopping Protocols ..."
    if {[ixNet exec stopAllProtocols] != "::ixNet::OK"} {
        log "Failed to stop Protocols !!!"
        ixNetCleanUp
        return $FAILED
    }
    log "Protocols stopped successfully !!!"
    after 5000

    # End Test Execution
    log "BGP-AD-LDP-SIG Functionality is working fine in IxNetwork !!!"
    log "Test execution Ends !!!"

    # Cleanup
    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
