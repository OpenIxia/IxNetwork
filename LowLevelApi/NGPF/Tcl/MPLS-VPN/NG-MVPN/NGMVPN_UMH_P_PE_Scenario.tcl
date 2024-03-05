#!/usr/bin/tclsh

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



#################################################################################

#                                                                               #

# Description:                                                                  #

#    This script intends to demonstrate how to use NGPF RSVPTE P2MP API         #

#    About Topology:                                                            #

#       Within topology both Sender and Receiver PEs are configured, each behind# 

#    Ingress and Egress P routers respectively. P2MP tunnels used in topology is# 

#	 RSVPTE-P2MP. Both I-PMSI and S-PMSI tunnels for IPv4 & Ipv6 multicast  #

#    streams are configured using RSVPTE-P2MP. Multicast traffic soruce address #

#    are distributed by BGP as UMH routes(AFI:1,SAFI:129). Multicast L2-L3      #

#    Traffic from Seder to Receiver                                             #

# Script Flow:                                                                  #

#        Step 1. Configuration of protocols.                                    #

#    Configuration flow of the script is as follow:                             #

#         i.      Adding of OSPF router                                         #

#         ii.     Adding of Network Topology(NT)                                #

#         iii.    Enabling of TE(Traffic Engineering) and configuring loopback  #

#                         address as Router ID                                  #

#         iv.     Adding of chain DG for behind both Sender/Receiver PE Router  #

#         v.      Adding of RSVP-TE LSPs(both P2P adn P2MP) and mVRF over       #

#                     BGP within chain DG                                       #

#         vi.     Configuring Parameters in mVRF at sender PE Router            #

#         vii.    Adding mVRF Route Range(both IPv4 and v6) as Sender Site      #

#                     behind Sender PE Router and as Receiver Site behind       # 

#                     Receiver PE Router                                        #

#         viii.   Configuring S-PMSI Tunnel in Sender Site (both IPv4/v6 range) #

#        Step 2. Start of protocol                                              #

#        Step 3. Retrieve protocol statistics                                   #

#        Step 4. Retrieve IPv4 mVPN learned info                                #

#        Step 5. Apply changes on the fly                                       #

#        Step 6. S-PMSI Trigger                                                 #

#        Step 7. Retrieve protocol learned info after OTF                       #

#        Step 8. Configure L2-L3 IPv4 I-PMSI traffic.                           #

#        Step 9. Configure L2-L3 IPv6 S-PMSI traffic.                           #

#        Step 10. Apply and start L2/L3 traffic.                                #

#        Step 11. Retrieve L2/L3 traffic item statistics.                       #

#        Step 12. Stop L2/L3 traffic.                                           #

#        Step 13. Stop all protocols.                                           #

#################################################################################



# edit this variables values to match your setup

namespace eval ::ixia {

    set ixTclServer 10.216.25.13

    set ixTclPort   8990

    set ports       {{10.216.108.82 7 11} { 10.216.108.82 7 12}}

}



puts "Load ixNetwork Tcl API package"

package req IxTclNetwork



puts "Disconnecting if any already connected"

ixNet disconnect $::ixia::ixTclServer



puts "Connect to IxNetwork Tcl server"

ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.20\

    setAttribute strict



puts "Creating a new config"

ixNet exec newConfig



#################################################################################

# 1. Configuration of protocols

#################################################################################

puts "Adding 2 vports"

ixNet add [ixNet getRoot] vport

ixNet add [ixNet getRoot] vport

ixNet commit



set vPorts [ixNet getList [ixNet getRoot] vport]

set vportTx [lindex $vPorts 0]

set vportRx [lindex $vPorts 1]



puts "Assigning the ports"

::ixTclNet::AssignPorts $ixia::ports {} $vPorts force



puts "Adding 2 topologies"

ixNet add [ixNet getRoot] topology -vports $vportTx

ixNet add [ixNet getRoot] topology -vports $vportRx

ixNet commit



set topologies [ixNet getList [ixNet getRoot] topology]

set topo1 [lindex $topologies 0]

set topo2 [lindex $topologies 1]



puts "Adding 2 device groups"

ixNet add $topo1 deviceGroup

ixNet add $topo2 deviceGroup

ixNet commit



set t1devices [ixNet getList $topo1 deviceGroup]

set t2devices [ixNet getList $topo2 deviceGroup]



puts "Renaming the topologies and the device groups"



ixNet setAttr $topo1  -name "Ingress Topology"

ixNet setAttr $topo2  -name "Egress Topology"



set t1dev1 [lindex $t1devices 0]

set t2dev1 [lindex $t2devices 0]

ixNet setAttr $t1dev1 -name "Sender P router"

ixNet setAttr $t2dev1 -name "Receiver P router"

ixNet commit

puts "Configuring the multipliers (number of sessions)"

ixNet setAttr $t1dev1 -multiplier 1

ixNet setAttr $t2dev1 -multiplier 1

ixNet commit



puts "Adding ethernet/mac endpoints"

ixNet add $t1dev1 ethernet

ixNet add $t2dev1 ethernet

ixNet commit



set mac1 [ixNet getList $t1dev1 ethernet]

set mac2 [ixNet getList $t2dev1 ethernet]



puts "Configuring the mac addresses"

ixNet setMultiAttr [ixNet getAttr $mac1 -mac]/counter\

        -direction  increment                        \

        -start      {22:22:22:22:22:22}              \

        -step       {00:00:00:00:01:00}



ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\

        -value      {44:44:44:44:44:44}

ixNet commit



puts "Add ipv4"

ixNet add $mac1 ipv4

ixNet add $mac2 ipv4

ixNet commit



set ip1 [ixNet getList $mac1 ipv4]

set ip2 [ixNet getList $mac2 ipv4]



set mvAdd1 [ixNet getAttr $ip1 -address]

set mvAdd2 [ixNet getAttr $ip2 -address]

set mvGw1  [ixNet getAttr $ip1 -gatewayIp]

set mvGw2  [ixNet getAttr $ip2 -gatewayIp]



puts "configuring ipv4 addresses"

ixNet setAttr $mvAdd1/singleValue -value "50.50.50.2"

ixNet setAttr $mvAdd2/singleValue -value "50.50.50.1"

ixNet setAttr $mvGw1/singleValue  -value "50.50.50.1"

ixNet setAttr $mvGw2/singleValue  -value "50.50.50.2"



ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 26

ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 26



ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true

ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true

ixNet commit



puts "Adding OSPFv2 over IP4 stack"

ixNet add $ip1 ospfv2

ixNet add $ip2 ospfv2

ixNet commit

set ospf1 [ixNet getList $ip1 ospfv2]

set ospf2 [ixNet getList $ip2 ospfv2]

puts "Making the NetworkType to Point to Point in the first OSPF router"

set networkTypeMultiValue1 [ixNet getAttr $ospf1 -networkType]

ixNet setAttr $networkTypeMultiValue1 -pattern singleValue -clearOverlays False

ixNet setAttr $networkTypeMultiValue1/singleValue -value pointtopoint

ixNet commit



puts "Making the NetworkType to Point to Point in the Second OSPF router"

set networkTypeMultiValue2 [ixNet getAttr $ospf2 -networkType]

ixNet setAttr $networkTypeMultiValue2 -pattern singleValue -clearOverlays False

ixNet setAttr $networkTypeMultiValue2/singleValue -value pointtopoint

ixNet commit



puts "Disabling the Discard Learned Info CheckBox"

set ospfv2RouterDiscardLearnedLSA1\

    [ixNet getAttr [lindex [ixNet getList $t1devices ospfv2Router] 0] -discardLearnedLsa]

set ospfv2RouterDiscardLearnedLSA2\

    [ixNet getAttr [lindex [ixNet getList $t2devices ospfv2Router] 0] -discardLearnedLsa]



ixNet setAttr $ospfv2RouterDiscardLearnedLSA1 -pattern singleValue -clearOverlays False

ixNet setAttr $ospfv2RouterDiscardLearnedLSA1/singleValue -value False

ixNet setAttr $ospfv2RouterDiscardLearnedLSA2 -pattern singleValue -clearOverlays False

ixNet setAttr $ospfv2RouterDiscardLearnedLSA2/singleValue -value False





puts "Adding the Network Topology"



ixNet exec createDefaultStack $t1devices networkTopology

ixNet exec createDefaultStack $t2devices networkTopology



set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]

set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]





ixNet setAttr $networkGroup1 -name "Sender PE Loopback"

ixNet setAttr $networkGroup2 -name "Receiver PE Loopback"

ixNet commit



set netTopo1 [ixNet getList $networkGroup1 networkTopology]

set netTopo2 [ixNet getList $networkGroup2 networkTopology]



puts "Enabling Traffic Engineering in Network Ingress Topology"

set simInterface1 [ixNet getList $netTopo1 simInterface]

set simInterfaceIPv4Config1 [ixNet getList $simInterface1 simInterfaceIPv4Config]



set ospfPseudoInterface1 [ixNet getList $simInterfaceIPv4Config1 ospfPseudoInterface]



set ospfPseudoInterface1_teEnable [ixNet getAttribute $ospfPseudoInterface1 -enable]

ixNet setMultiAttribute $ospfPseudoInterface1_teEnable \

                        -clearOverlays false           \

                        -pattern singleValue

ixNet commit

ixNet setMultiAttribute $ospfPseudoInterface1_teEnable/singleValue -value true

ixNet commit



puts "Enabling Traffic Engineering in Network Egress Topology"

set simInterface2 [ixNet getList $netTopo2 simInterface]

set simInterfaceIPv4Config2 [ixNet getList $simInterface2 simInterfaceIPv4Config]

set ospfPseudoInterface2 [ixNet getList $simInterfaceIPv4Config2 ospfPseudoInterface]

set ospfPseudoInterface2_teEnable [ixNet getAttribute $ospfPseudoInterface2 -enable]

ixNet setMultiAttribute $ospfPseudoInterface2_teEnable \

                        -clearOverlays false           \

                        -pattern singleValue

ixNet commit

ixNet setMultiAttribute $ospfPseudoInterface2_teEnable/singleValue -value true

ixNet commit



puts "Adding Chained DG behind Network Topology in Ingress Topology"

set chainedDg1 [ixNet add $networkGroup1 deviceGroup]

ixNet commit

set chainedDg1 [lindex [ixNet remapIds $chainedDg1] 0]

ixNet setMultiAttribute $chainedDg1\

    -multiplier 1                  \

    -name {Sender PE Router}

ixNet commit

set loopback1 [ixNet add $chainedDg1 "ipv4Loopback"]

ixNet setMultiAttribute $loopback1\

    -stackedLayers [list]         \

    -name {IPv4 Loopback 1}

ixNet commit

puts "Adding Chained DG behind Network Topology in Egress Topology"

set chainedDg2 [ixNet add $networkGroup2 deviceGroup]

ixNet setMultiAttribute $chainedDg2\

    -multiplier 1                  \

    -name {Receiver PE Router}

ixNet commit

set chainedDg2 [lindex [ixNet remapIds $chainedDg2] 0]



set loopback2 [ixNet add $chainedDg2 "ipv4Loopback"]

ixNet setMultiAttribute $loopback2\

    -stackedLayers [list]         \

    -name {IPv4 Loopback 2}

ixNet commit



puts "Adding RSVPTE P2MP router over 'IPv4 Loopback 1'"

set rsvpteLsps1 [ixNet add $loopback1 rsvpteLsps]

ixNet setMultiAttribute $rsvpteLsps1 -ingressP2PLsps 1 \

		    -enableP2PEgress true     \

			-p2mpIngressLspCount 3    \

			-p2mpEgressTunnelCount 0  \

			-stackedLayers [list ]    \

			-name "RSVP-TE\ 1"

ixNet commit

set rsvpteLsps1 [lindex [ixNet remapIds $rsvpteLsps1] 0]



puts "Adding RSVPTE P2MP router over 'IPv4 Loopback 2'"

set rsvpteLsps2 [ixNet add $loopback2 rsvpteLsps]

ixNet setMultiAttribute $rsvpteLsps2 -ingressP2PLsps 1 \

			-enableP2PEgress true 		\

			-p2mpIngressLspCount 0 		\

			-p2mpEgressTunnelCount 3    \

			-stackedLayers [list ]      \

			-name "RSVP-TE\ 2"

ixNet commit

set rsvpteLsps2 [lindex [ixNet remapIds $rsvpteLsps2] 0]

puts "Changing P2MP ID config/Type for RSVP-P2MP to IP for P2MP Ingress LSPs to use with I-PMSI & S-PMSI tunnel config"



ixNet setAttribute $rsvpteLsps1/rsvpP2mpIngressLsps -typeP2mpId iP



set p2mpIdAsIp_ingress [ixNet getAttribute $rsvpteLsps1/rsvpP2mpIngressLsps -p2mpIdIp]

ixNet setMultiAttribute $p2mpIdAsIp_ingress\

    -clearOverlays false \

    -pattern counter

ixNet commit



ixNet setMultiAttr $p2mpIdAsIp_ingress/counter\

        -direction  increment                 \

        -start      11.11.11.1                \

        -step       0.0.0.1

ixNet commit



puts "Changing Tunnel Id for P2MP Ingress LSPs"

set tunnelId_ingress [ixNet getAttribute $rsvpteLsps1/rsvpP2mpIngressLsps -tunnelId]

ixNet setMultiAttribute $tunnelId_ingress\

    -clearOverlays false \

    -pattern counter

ixNet commit



ixNet setMultiAttr $tunnelId_ingress/counter\

        -direction  increment               \

        -start      1                       \

        -step       0

ixNet commit



puts "Changing P2MP ID config/Type for RSVP-P2MP to IP for P2MP Egress LSPs to use with I-PMSI & S-PMSI tunnel config"

ixNet setAttribute $rsvpteLsps2/rsvpP2mpEgressLsps -typeP2mpId iP

ixNet commit

puts "Configuring P2MP ID value as IP"

set p2mpIdAsIp_egress [ixNet getAttribute $rsvpteLsps2/rsvpP2mpEgressLsps -p2mpIdIp]

ixNet setMultiAttribute $p2mpIdAsIp_egress\

    -clearOverlays false                      \

    -pattern custom

ixNet commit

ixNet setMultiAttr $p2mpIdAsIp_egress/counter\

        -direction  increment                \

        -start      11.11.11.1               \

        -step       0.0.0.1

ixNet commit



puts "Editing Leaf IP in Ingress SubLSPs"

set leafIp [ixNet getAttribute $rsvpteLsps1/rsvpP2mpIngressLsps/rsvpP2mpIngressSubLsps -leafIp]

ixNet setMultiAttribute $leafIp \

	-clearOverlays false

ixNet commit

ixNet setAttr $leafIp/singleValue -value "3.2.2.2"

ixNet commit



puts "Assigning 'Remote IP' to RSVPTE P2P LSPs under Ingress Topology"

set rsvpP2PIngressLsps1 [ixNet getList $rsvpteLsps1 rsvpP2PIngressLsps]

set remoteIp4Rsvp1 [ixNet getAttribute $rsvpP2PIngressLsps1 -remoteIp]

ixNet setMultiAttribute $remoteIp4Rsvp1\

    -clearOverlays false               \

    -pattern counter

ixNet commit

ixNet setMultiAttribute $remoteIp4Rsvp1/counter\

    -step 0.0.0.1                              \

    -start 3.2.2.2                             \

    -direction increment

ixNet commit



puts "Assigning 'Remote IP' to RSVPTE P2P LSPs under Egress Topology"

set rsvpP2PIngressLsps2 [ixNet getList $rsvpteLsps2 rsvpP2PIngressLsps]

set remoteIp4Rsvp2 [ixNet getAttribute $rsvpP2PIngressLsps2 -remoteIp]

ixNet setMultiAttribute $remoteIp4Rsvp2\

    -clearOverlays false               \

    -pattern counter

ixNet commit

ixNet setMultiAttribute $remoteIp4Rsvp2/counter\

    -step 0.0.0.1                              \

    -start 2.2.2.2                             \

    -direction increment

ixNet commit



puts "Adding BGP over IPv4 loopback interfaces"

ixNet add $loopback1 bgpIpv4Peer

ixNet add $loopback2 bgpIpv4Peer

ixNet commit



set bgp1 [ixNet getList $loopback1 bgpIpv4Peer]

set bgp2 [ixNet getList $loopback2 bgpIpv4Peer]



puts "Setting IPs in BGP DUT IP tab"

ixNet setAttr [ixNet getAttr $bgp1 -dutIp]/singleValue -value "3.2.2.2"

ixNet setAttr [ixNet getAttr $bgp2 -dutIp]/singleValue -value "2.2.2.2"

ixNet commit



puts "Enabling MVPN Capabilities for BGP Router"

ixNet setAttr [ixNet getAttr $bgp1 -capabilityIpV4MplsVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp1 -capabilityIpV4Multicast]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp1 -capabilityIpV4MulticastVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp1 -ipv4MulticastBgpMplsVpn]/singleValue -value true



ixNet setAttr [ixNet getAttr $bgp1 -capabilityIpV6MplsVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp1 -capabilityIpV6Multicast]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp1 -capabilityIpV6MulticastVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp1 -ipv6MulticastBgpMplsVpn]/singleValue -value true



ixNet setAttr [ixNet getAttr $bgp2 -capabilityIpV4MplsVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp2 -capabilityIpV4Multicast]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp2 -capabilityIpV4MulticastVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp2 -ipv4MulticastBgpMplsVpn]/singleValue -value true



ixNet setAttr [ixNet getAttr $bgp2 -capabilityIpV6MplsVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp2 -capabilityIpV6Multicast]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp2 -capabilityIpV6MulticastVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp2 -ipv6MulticastBgpMplsVpn]/singleValue -value true

ixNet commit



puts "Enabling MVPN Learned Information for BGP Router"

ixNet setAttr [ixNet getAttr $bgp1 -filterIpV4Unicast]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp1 -filterIpV4MplsVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp1 -filterIpv4MulticastBgpMplsVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp1 -filterIpV4MulticastVpn]/singleValue -value true



ixNet setAttr [ixNet getAttr $bgp1 -filterIpV6Unicast]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp1 -filterIpV6MplsVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp1 -filterIpv6MulticastBgpMplsVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp1 -filterIpV6MulticastVpn]/singleValue -value true



ixNet setAttr [ixNet getAttr $bgp2 -filterIpV4Unicast]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp2 -filterIpV4MplsVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp2 -filterIpv4MulticastBgpMplsVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp2 -filterIpV4MulticastVpn]/singleValue -value true



ixNet setAttr [ixNet getAttr $bgp2 -filterIpV6Unicast]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp2 -filterIpV6MplsVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp2 -filterIpv6MulticastBgpMplsVpn]/singleValue -value true

ixNet setAttr [ixNet getAttr $bgp2 -filterIpV6MulticastVpn]/singleValue -value true

ixNet commit



puts "Adding mVRF over BGP in both ports"

ixNet add $bgp1 bgpIpv4MVrf

ixNet add $bgp2 bgpIpv4MVrf

ixNet commit



set mVRF1 [ixNet getList $bgp1 bgpIpv4MVrf]

set mVRF2 [ixNet getList $bgp2 bgpIpv4MVrf]



puts "Configuring RSVP P2MP ID value as IP in I-PMSI Tunnel in Egress Topology"

set p2mpIdAsIp_pmsi1 [ixNet getAttribute $mVRF1 -rsvpP2mpId]

ixNet setMultiAttribute $p2mpIdAsIp_pmsi1      \

    -clearOverlays false                      \

    -pattern custom

ixNet commit

ixNet setMultiAttr $p2mpIdAsIp_pmsi1/counter  \

        -direction  increment                \

        -start      11.11.11.1               \

        -step       0.0.0.0

ixNet commit



puts "Enabling  CheckBox for use of Up/DownStream Assigned Label for Ingress Topology"

set useUpOrDownStreamAssigneLabel1 [ixNet getAttr $mVRF1 -useUpOrDownStreamAssigneLabel]

ixNet setAttr $useUpOrDownStreamAssigneLabel1 -pattern singleValue -clearOverlays False

ixNet setAttr $useUpOrDownStreamAssigneLabel1/singleValue -value True



puts "Assigning value for Up/DownStream Assigned Label for Ingress Topology"

set upOrDownStreamAssignedLabel1 [ixNet getAttr $mVRF1 -upOrDownStreamAssignedLabel]

ixNet setAttr $upOrDownStreamAssignedLabel1/singleValue -value "10001"



puts "Adding Network Group behind mVRF for Ingress Topology"

ixNet add $chainedDg1 networkGroup

ixNet commit

set networkGroup3 [lindex [ixNet getList $chainedDg1 networkGroup] 0]

ixNet setAttr $networkGroup3 -name  "Sender\ Site"

ixNet commit



puts "Adding Network Group behind mVRF for Egress Topology"

ixNet add $chainedDg2 networkGroup

ixNet commit

set networkGroup4 [lindex [ixNet getList $chainedDg2 networkGroup] 0]

ixNet setAttr $networkGroup4 -name  "Receiver\ Site"

ixNet commit



puts "Adding IPv4/IPv6 Prefix pools in Ingress Topology behind Sender PE router"

ixNet add $networkGroup3 ipv4PrefixPools

ixNet commit

ixNet add $networkGroup3 ipv6PrefixPools

ixNet commit



puts "Adding IPv4/IPv6 Prefix pools in Egress Topology behind Receiver PE router"

ixNet add $networkGroup4 ipv4PrefixPools

ixNet commit

ixNet add $networkGroup4 ipv6PrefixPools

ixNet commit



puts "Disabling Sender site and enabling Receiver Site for both IPv4 in Egress Topology"

set ipv4PrefixPools4 [lindex [ixNet getList $networkGroup4 ipv4PrefixPools] 0]

set bgpL3VpnRouteProperty4 [lindex [ixNet getList $ipv4PrefixPools4 bgpL3VpnRouteProperty] 0]

ixNet setAttr $bgpL3VpnRouteProperty4 -enableIpv4Sender False

ixNet setAttr $bgpL3VpnRouteProperty4 -enableIpv4Receiver True

ixNet commit



puts "Disabling Sender site and enabling Receiver Site for both IPv6 in Egress Topology"

set ipv6PrefixPools4 [lindex [ixNet getList $networkGroup4 ipv6PrefixPools] 0]

set bgpV6L3VpnRouteProperty [lindex [ixNet getList $ipv6PrefixPools4 bgpV6L3VpnRouteProperty] 0]

ixNet setAttr $bgpV6L3VpnRouteProperty -enableIpv6Sender False

ixNet setAttr $bgpV6L3VpnRouteProperty -enableIpv6Receiver True

ixNet commit



puts "Enabling UMH Route check box in Sender Site"

set ipv4PrefixPools3 [lindex [ixNet getList $networkGroup3 ipv4PrefixPools] 0]

set ipv6PrefixPools3 [lindex [ixNet getList $networkGroup3 ipv6PrefixPools] 0]

set bgpL3VpnRouteProperty3 [lindex [ixNet getList $ipv4PrefixPools3 bgpL3VpnRouteProperty] 0]

set bgpV6L3VpnRouteProperty3 [lindex [ixNet getList $ipv6PrefixPools3 bgpV6L3VpnRouteProperty] 0]

ixNet setAttr $bgpL3VpnRouteProperty3 -useAsIpv4UmhRoutes True

ixNet setAttr $bgpV6L3VpnRouteProperty3 -useAsIpv6UmhRoutes True

ixNet commit



set bgpMVpnSenderSitesIpv4 [lindex [ixNet getList $ipv4PrefixPools3 bgpMVpnSenderSitesIpv4] 0]

set ipv6PrefixPools3 [lindex [ixNet getList $networkGroup3 ipv6PrefixPools] 0]

set bgpMVpnSenderSitesIpv6 [lindex [ixNet getList $ipv6PrefixPools3 bgpMVpnSenderSitesIpv6] 0]

set bgpMVpnReceiverSitesIpv4 [lindex [ixNet getList $ipv4PrefixPools4 bgpMVpnReceiverSitesIpv4] 0]

set bgpMVpnReceiverSitesIpv6 [lindex [ixNet getList $ipv6PrefixPools4 bgpMVpnReceiverSitesIpv6] 0]





puts "Changing Group Address Count for IPv4 Cloud in Sender Site"

set mulValGCount [ixNet getAttr $bgpMVpnSenderSitesIpv4 -groupAddressCount]

ixNet setMultiAttr $mulValGCount -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValGCount/singleValue -value 5

ixNet commit



puts "Changing Source Address Count for IPv4 Cloud in Sender Site"

set mulValSCount [ixNet getAttr $bgpMVpnSenderSitesIpv4 -sourceAddressCount]

ixNet setMultiAttr $mulValSCount -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValSCount/singleValue -value 3

ixNet commit



puts "Changing Group Address for IPv4 Cloud in Sender Site"

set mulValGAdd [ixNet getAttr $bgpMVpnSenderSitesIpv4 -startGroupAddressIpv4]

ixNet setMultiAttr $mulValGAdd -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValGAdd/singleValue -value "234.161.1.1"

ixNet commit



puts "Changing Source Address for IPv4 Cloud in Sender Site"

set mulValSAdd [ixNet getAttr $bgpMVpnSenderSitesIpv4 -startSourceAddressIpv4]

ixNet setMultiAttr $mulValSAdd -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValSAdd/singleValue -value "191.0.1.1"

ixNet commit



puts "Changing Group Address Count for IPv4 Cloud in Receiver Site"

set mulValGCount [ixNet getAttr $bgpMVpnReceiverSitesIpv4 -groupAddressCount]

ixNet setMultiAttr $mulValGCount -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValGCount/singleValue -value 5

ixNet commit



puts "Changing Source Address Count for IPv4 Cloud in Receiver Site"

set mulValSCount [ixNet getAttr $bgpMVpnReceiverSitesIpv4 -sourceAddressCount]

ixNet setMultiAttr $mulValSCount -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValSCount/singleValue -value 3

ixNet commit



puts "Changing Group Address for IPv4 Cloud in Receiver Site"

set mulValGAdd [ixNet getAttr $bgpMVpnReceiverSitesIpv4 -startGroupAddressIpv4]

ixNet setMultiAttr $mulValGAdd -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValGAdd/singleValue -value "234.161.1.1"

ixNet commit



puts "Changing Source Address for IPv4 Cloud in Receiver Site"

set mulValSAdd [ixNet getAttr $bgpMVpnReceiverSitesIpv4 -startSourceOrCrpAddressIpv4]

ixNet setMultiAttr $mulValSAdd -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValSAdd/singleValue -value "191.0.1.1"

ixNet commit



puts "Changing C-Multicast Route Type for IPv4 Cloud in Receiver Site"

set mulValCMRType [ixNet getAttr $bgpMVpnReceiverSitesIpv4 -cMulticastRouteType]

ixNet setMultiAttr $mulValCMRType -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValCMRType/singleValue -value "sharedtreejoin"

ixNet commit



puts "Changing Group Address Count for IPv6 Cloud in Sender Site"

set mulValGCount [ixNet getAttr $bgpMVpnSenderSitesIpv6 -groupAddressCount]

ixNet setMultiAttr $mulValGCount -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValGCount/singleValue -value 5

ixNet commit



puts "Changing source Group Mapping for IPv6 Cloud in Sender Site"

set mulValSGMap [ixNet getAttr $bgpMVpnSenderSitesIpv6 -sourceGroupMapping]

ixNet setMultiAttr $mulValSGMap -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValSGMap/singleValue -value onetoone

ixNet commit



puts "Changing Group Address for IPv6 Cloud in Sender Site"

set mulValGAdd [ixNet getAttr $bgpMVpnSenderSitesIpv6 -startGroupAddressIpv6]

ixNet setMultiAttr $mulValGAdd -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValGAdd/singleValue -value "ff15:1:0:0:0:0:0:1"

ixNet commit



puts "Changing Source Address for IPv6 Cloud in Sender Site"

set mulValSAdd [ixNet getAttr $bgpMVpnSenderSitesIpv6 -startSourceAddressIpv6]

ixNet setMultiAttr $mulValSAdd -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValSAdd/singleValue -value "5001:1:0:0:0:0:0:1"

ixNet commit



set bgpMVpnReceiverSitesIpv4 [lindex [ixNet getList $ipv4PrefixPools4 bgpMVpnReceiverSitesIpv4] 0]

set bgpMVpnReceiverSitesIpv6 [lindex [ixNet getList $ipv6PrefixPools4 bgpMVpnReceiverSitesIpv6] 0]



puts "Changing Group Address Count for IPv6 Cloud in Receiver Site"

set mulValGCount [ixNet getAttr $bgpMVpnReceiverSitesIpv6 -groupAddressCount]

ixNet setMultiAttr $mulValGCount -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValGCount/singleValue -value 5

ixNet commit



puts "Changing source Group Mapping for IPv6 Cloud in Receiver Site"

set mulValSGMap [ixNet getAttr $bgpMVpnReceiverSitesIpv6 -sourceGroupMapping]

ixNet setMultiAttr $mulValSGMap -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValSGMap/singleValue -value onetoone

ixNet commit



puts "Changing Group Address for IPv6 Cloud in Receiver Site"

set mulValGAdd [ixNet getAttr $bgpMVpnReceiverSitesIpv6 -startGroupAddressIpv6]

ixNet setMultiAttr $mulValGAdd -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValGAdd/singleValue -value "ff15:1:0:0:0:0:0:1"

ixNet commit



puts "Changing Source Address for IPv6 Cloud in Receiver Site"

set mulValSAdd [ixNet getAttr $bgpMVpnReceiverSitesIpv6 -startSourceOrCrpAddressIpv6]

ixNet setMultiAttr $mulValSAdd -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValSAdd/singleValue -value "5001:1:0:0:0:0:0:1"

ixNet commit



puts "Changing Address for IPv4 Address Pool in Sender Site"

set mulValIpAdd [ixNet getAttr $ipv4PrefixPools3 -networkAddress]

ixNet setMultiAttr $mulValIpAdd -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValIpAdd/singleValue -value "191.0.1.1"

ixNet commit



puts "Changing Prefix Length for IPv4 Address Pool in Sender Site"

set mulValPrefLen [ixNet getAttr $ipv4PrefixPools3 -prefixLength]

ixNet setMultiAttr $mulValPrefLen -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValPrefLen/singleValue -value "32"

ixNet commit



puts "Changing Address Count Address Pool in Sender Site"

ixNet setAttr $ipv4PrefixPools3 -numberOfAddresses 3

ixNet commit



puts "Changing Address for IPv6 Address Pool in Sender Site"

set mulValIpAdd [ixNet getAttr $ipv6PrefixPools3 -networkAddress]

ixNet setMultiAttr $mulValIpAdd -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValIpAdd/singleValue -value "5001:1:0:0:0:0:0:1"

ixNet commit



puts "Changing Prefix Length for IPv6 Address Pool in Sender Site"

set mulValPrefLen [ixNet getAttr $ipv6PrefixPools3 -prefixLength]

ixNet setMultiAttr $mulValPrefLen -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValPrefLen/singleValue -value "128"

ixNet commit



puts "Changing Address Count Address Pool in Sender Site"

ixNet setAttr $ipv6PrefixPools3 -numberOfAddresses 5

ixNet commit



puts "Configuring S-PMSI on Sender SItes"

set bgpMVpnSenderSiteSpmsiV4 [lindex [ixNet getList $bgpMVpnSenderSitesIpv4 bgpMVpnSenderSiteSpmsiV4] 0]



puts "Changing RSVP P2MP Id for S-PMSI in IPv4 Address Pool in Ingress Topology"

set mulValp2mpId [ixNet getAttr $bgpMVpnSenderSiteSpmsiV4 -sPmsiRsvpP2mpId]

ixNet setMultiAttr $mulValp2mpId -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValp2mpId/singleValue -value "11.11.11.2"

ixNet commit



puts "Changing RSVP TunnelId Step for S-PMSI in IPv4 Address Pool in Sender Site"

set mulValsPMSIRsvpTunId [ixNet getAttr $bgpMVpnSenderSiteSpmsiV4 -sPmsiRsvpTunnelIdStep]

ixNet setMultiAttr $mulValsPMSIRsvpTunId -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValsPMSIRsvpTunId/singleValue -value "0"

ixNet commit





puts "Changing RSVP Tunnel Count for S-PMSI in IPv4 Address Pool in Ingress Topology"

set mulValsPMSTidCnt [ixNet getAttr $bgpMVpnSenderSiteSpmsiV4 -sPmsiTunnelCount]

ixNet setMultiAttr $mulValsPMSTidCnt -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValsPMSTidCnt/singleValue -value "2"

ixNet commit



set bgpMVpnSenderSiteSpmsiV6 [lindex [ixNet getList $bgpMVpnSenderSitesIpv6 bgpMVpnSenderSiteSpmsiV6] 0]



puts "Changing RSVP P2MP Id for S-PMSI in IPv6 Address Pool in Sender Site"

set mulValp2mpId [ixNet getAttr $bgpMVpnSenderSiteSpmsiV6 -sPmsiRsvpP2mpId]

ixNet setMultiAttr $mulValp2mpId -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValp2mpId/singleValue -value "11.11.11.2"

ixNet commit



puts "Changing RSVP TunnelId Step for S-PMSI in IPv6 Address Pool  in Sender Site"

set mulValsPMSIRsvpTunId [ixNet getAttr $bgpMVpnSenderSiteSpmsiV6 -sPmsiRsvpTunnelIdStep]

ixNet setMultiAttr $mulValsPMSIRsvpTunId -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValsPMSIRsvpTunId/singleValue -value "0"

ixNet commit



puts "Changing RSVP Tunnel Count for S-PMSI in IPv6 Address Pool  in Sender Site"

set mulValsPMSTidCnt [ixNet getAttr $bgpMVpnSenderSiteSpmsiV6 -sPmsiTunnelCount]

ixNet setMultiAttr $mulValsPMSTidCnt -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValsPMSTidCnt/singleValue -value "2"

ixNet commit



################################################################################

# 2. Start protocols.

################################################################################

puts "Wait for 5 seconds before starting protocol"

after 5000

puts "Starting protocols and waiting for 60 seconds for protocols to come up"

ixNet exec startAllProtocols

after 60000



################################################################################

# 3. Retrieve protocol statistics.

################################################################################

puts "Fetching all BGP Peer Per Port\n"

set viewPage {::ixNet::OBJ-/statistics/view:"BGP Peer Per Port"/page}

set statcap [ixNet getAttr $viewPage -columnCaptions]

foreach statValList [ixNet getAttr $viewPage -rowValues] {

    foreach statVal $statValList  {

        puts "***************************************************"

        set index 0

        foreach satIndv $statVal {

            puts [format "%*s:%*s" -30 [lindex $statcap $index]\

                -10 $satIndv]

            incr index

        }

    }

}

puts "***************************************************"



###############################################################################

# 4. Retrieve IPv4 mVPN learned info

###############################################################################



puts "Fetching mVPN Learned Info"

ixNet exec getIpv4MvpnLearnedInfo $bgp1 1

after 5000

puts "IPv4 MVPN Learned Info at Sender PE Router"

set learnedInfoList [ixNet getList $bgp1 learnedInfo]

set linfoList [ixNet getList $learnedInfoList table]



puts "mVPN learned info"

puts "***************************************************"

foreach table $linfoList {

    set type [ixNet getAttr $table -type]

    puts "$type Routes:"

    puts "***************************************************"

    set column [ixNet getAttr $table -columns]

    puts "$column"

    set values [ixNet getAttr $table -values]

    puts "$values\n"

    puts "***************************************************"

}

puts "***************************************************"



puts "Fetching IPv6 UMH Learned Info at Receiver PE Router"

ixNet exec getIpv6UmhRoutesLearnedInfo $bgp2 1

after 5000

set learnedInfoList [ixNet getList $bgp2 learnedInfo]

set linfoTable [ixNet getList $learnedInfoList table]

puts "IPv6 UMH Learned Info at Receiver PE Router"

puts "***************************************************"

set type [ixNet getAttr $linfoTable -type]

puts "$type Routes:"

puts "***************************************************"

set column [ixNet getAttr $linfoTable -columns]

puts "$column"

set values [ixNet getAttr $linfoTable -values]

puts "$values\n"

puts "***************************************************"



################################################################################

# 5. Apply changes on the fly.

################################################################################

puts "Changing C-Multicast Route Type for IPv6 Cloud in Receiver Site"

set mulValCMRType [ixNet getAttr $bgpMVpnReceiverSitesIpv6 -cMulticastRouteType]

ixNet setMultiAttr $mulValCMRType -pattern singleValue -clearOverlays 0

ixNet commit

ixNet setMultiAttribute $mulValCMRType/singleValue -value "sharedtreejoin"

ixNet commit



set globals [ixNet getRoot]/globals

set topology $globals/topology

if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {

    puts "error in applying on the fly change"

        puts "$::errorInfo"

}

after 10000

################################################################################

# 6. S-PMSI Trigger

################################################################################

puts "Switching to S-PMSI for IPv6 Cloud from Sender Site"

ixNet exec switchToSpmsi $bgpMVpnSenderSitesIpv6 1



###############################################################################

# 7. Retrieve protocol learned info after OTF

###############################################################################



puts "Fetching IPv6 mVPN Learned Info"

ixNet exec getIpv6MvpnLearnedInfo $bgp1 1

after 5000

puts "IPv6 MVPN Learned Info at Sender PE Router"

set learnedInfoList [ixNet getList $bgp1 learnedInfo]

set linfoList [ixNet getList $learnedInfoList table]



puts "mVPN learned info at Sender PE Router"

puts "***************************************************"

foreach table $linfoList {

    set type [ixNet getAttr $table -type]

    puts "$type Routes:"

    puts "***************************************************"

    set column [ixNet getAttr $table -columns]

    puts "$column"

    set values [ixNet getAttr $table -values]

    puts "$values\n"

    puts "***************************************************"

}

puts "***************************************************"



################################################################################

# 8. Configure L2-L3 IPv4 I-PMSI traffic.

################################################################################

puts "Configuring L2-L3 IPv6 I-PMSI Traffic Item"

set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]

ixNet setMultiAttribute $trafficItem1  \

    -name {NGMVPN I-PMSI Traffic 1}    \

    -roundRobinPacketOrdering false    \

	-numVlansForMulticastReplication 1 \

    -trafficType ipv4 \

	-routeMesh fullMesh

ixNet commit



set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]

set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]

set source       [list $bgpMVpnSenderSitesIpv4]

set destination  [list $bgpMVpnReceiverSitesIpv4]



ixNet setMultiAttribute $endpointSet1           \

        -name                  "EndpointSet-1"  \

        -multicastDestinations [list [list false none 234.161.1.1 0.0.0.1 5]] \

		-multicastReceivers $destination \

		-sources $source

ixNet commit



set endpointSet1 [lindex [ixNet remapIds $endpointSet1] 0]



ixNet setMultiAttribute $trafficItem1/tracking -trackBy \

    [list sourceDestEndpointPair0 mplsFlowDescriptor0 trackingenabled0 mplsMplsLabelValue0 ipv4DestIp0 ipv4SourceIp0]

ixNet commit	



################################################################################

# 9. Configure L2-L3 IPv6 S-PMSI traffic.

################################################################################

puts "Configuring L2-L3 IPv6 S-PMSI Traffic Item"

set trafficItem2 [ixNet add [ixNet getRoot]/traffic "trafficItem"]

ixNet setMultiAttribute $trafficItem2  \

    -name {NGMVPN S-PMSI Traffic 2}    \

    -roundRobinPacketOrdering false    \

	-numVlansForMulticastReplication 1 \

    -trafficType ipv6 \



ixNet commit



set trafficItem2 [lindex [ixNet remapIds $trafficItem2] 0]

set endpointSet2 [ixNet add $trafficItem2 "endpointSet"]

set source       [list $bgpMVpnSenderSiteSpmsiV6]

set destination  [list $bgpMVpnReceiverSitesIpv6]

ixNet setMultiAttribute $endpointSet2           \

        -name                  "EndpointSet-1"  \

        -multicastDestinations [list [list false none ff15:1:0:0:0:0:0:1 0:0:0:0:0:0:0:1 5]] \

		-multicastReceivers $destination \

		-sources $source

ixNet commit



set endpointSet2 [lindex [ixNet remapIds $endpointSet2] 0]



ixNet setMultiAttribute $trafficItem2/tracking -trackBy \

    [list sourceDestValuePair0 ipv6DestIp0 ipv6SourceIp0 trackingenabled0 mplsFlowDescriptor0]

ixNet commit



###############################################################################

# 10. Apply and start L2/L3 traffic.

###############################################################################

puts "applying traffic"

ixNet exec apply [ixNet getRoot]/traffic

after 5000

puts "starting traffic"

ixNet exec start [ixNet getRoot]/traffic



puts "let traffic run for 60 second"

after 60000

###############################################################################

# 11. Retrieve L2/L3 traffic item statistics.

###############################################################################

puts "Verifying all the L2-L3 traffic statistics\n"

set viewPage {::ixNet::OBJ-/statistics/view:"Flow Statistics"/page}

set statcap [ixNet getAttr $viewPage -columnCaptions]

foreach statValList [ixNet getAttr $viewPage -rowValues] {

    foreach statVal $statValList  {

        puts "***************************************************"

        set index 0

        foreach satIndv $statVal {

            puts [format "%*s:%*s" -34 [lindex $statcap $index]\

                -10 $satIndv]

            incr index

        }

    }

}

puts "***************************************************"



#################################################################################

# 12. Stop L2/L3 traffic.

#################################################################################

puts "Stopping L2/L3 traffic"

ixNet exec stop [ixNet getRoot]/traffic

after 5000



################################################################################

# 13. Stop all protocols.

################################################################################

ixNet exec stopAllProtocols

puts "!!! Test Script Ends !!!"

