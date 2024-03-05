#!/usr/bin/tclsh
#################################################################################                                                                             
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                               #
#################################################################################
#################################################################################
#                                                                               #
#                                LEGAL  NOTICE:                                 #
#                                ==============                                 #
# The following code and documentation (hereinafter "the script") is an         #
# example script for demonstration purposes only.                               #
# The script is not a standard commercial product offered by Ixia and have      #
# been developed and is being provided for use only as indicated herein. The    #
# script [and all modifications enhancements and updates thereto (whether       #
# made by Ixia and/or by the user and/or by a third party)] shall at all times  #
# remain the property of Ixia.                                                  #
#                                                                               #
# Ixia does not warrant (i) that the functions contained in the script will     #
# meet the users requirements or (ii) that the script will be without           #
# omissions or error-free.                                                      #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA          #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE               #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR  #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                  #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE  #
# USER.                                                                         #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING    #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF      #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR           #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR               #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF     #
# SUCH DAMAGES IN ADVANCE.                                                      #
# Ixia will not be required to provide any software maintenance or support      #
# services of any kind (e.g. any error corrections) in connection with the      #
# script or any part thereof. The user acknowledges that although Ixia may      #
# from time to time and in its sole discretion provide maintenance or support   #
# services for the script any such services are subject to the warranty and     #
# damages limitations set forth herein and will not obligate Ixia to provide    #
# any additional maintenance or support services.                               #
#                                                                               #
################################################################################
#################################################################################
#                                                                               #
# Description:                                                                  #
#    This script intends to demonstrate how to use NGPF API for NGMVPN-BIER     #
#    with underlay ISIS                                                         #
# About Topology:                                                               #
#    Within topology both Sender and Receiver PEs are configured, each behind   #
#    Ingress and Egress P routers respectively. PMSI tunnels used in topology   #
#    is BIER. Both I-PMSI and S-PMSI tunnels for IPv4 multicast streams are     #
#    configured. Multicast traffic soruce address are distributed by BGP as     #
#    MVPN routes (AFI:1,SAFI:129) with TYPE I-PMSI, S-PMSI & Leaf AD. ISIS is   #
#    being used as underlay & IGP for BIER emulation. It provides Label for     #
#    multicast stream as per PMSI tunnel configration based on BSL,SD & SI.     #
#    I-PMSI, S-PMSI Multicast L2-L3 Traffic from Sender to Receiver are         #
#    configured.                                                                #
# Script Flow:                                                                  #
#    Step 1. Configuration of protocols.                                        #
#    Configuration flow of the script is as follow:                             #
#        i.   Add ISIS router and enable BIER and configure BIER related        #
#             parameters.                                                       #
#        ii.  Add Network Topology(NT) and configure BIER related parameters.   #     
#        iii. Add chain DG behind both P routers                                #
#        iv.  Add loopback on chained DG, confiugre BGP on loopback.            #
#              add mVRF over BGP within chain DG.                               #
#        v.   Configure I-PMSI Tunnel as BIER related parameterfor mVRF at BFIR #
#              and BFER as well as  Traffic related parameters                  #
#        vi.  Add mVRF Route Range(IPv4) as Sender Site behind BFIR and as      #
#             Receiver Site behind BFER.                                        #
#        vii. Configuring S-PMSI Tunnel as BIER at Sender Site and configure    #
#             BIER realted parameter and Traffic related parameters as well.    #
#        Step 2. Start of protocol                                              #
#        Step 3. Retrieve protocol statistics                                   #
#        Step 4. S-PMSI Trigger                                                 #
#        Step 5. Retrieve IPv4 mVPN learned info                                #
#        Step 6. Configure L2-L3 IPv4 I-PMSI traffic.                           #
#        Step 7. Configure L2-L3 IPv4 S-PMSI traffic.                           #
#        Step 8. Apply and start L2/L3 traffic.                                 #
#        Step 9. Retrieve L2/L3 traffic item statistics.                        #
#        Step 10. Stop L2/L3 traffic.                                           #
#        Step 11. Stop all protocols.                                           #
#################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.40.148
    set ixTclPort   8239
    set ports       {{10.39.50.123 11 7} { 10.39.50.123 11 8}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Disconnecting if any already connected"
ixNet disconnect $::ixia::ixTclServer

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.50\
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

ixNet setAttr $topo1  -name "Ingress Topology : Sender"
ixNet setAttr $topo2  -name "Egress Topology: Receiver"

set t1dev1 [lindex $t1devices 0]
set t2dev1 [lindex $t2devices 0]
ixNet setAttr $t1dev1 -name "Sender P Router"
ixNet setAttr $t2dev1 -name "Receiver P Router"
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

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

puts "Adding ISIS over Ethernet stacks"
ixNet add $mac1 isisL3
ixNet add $mac2 isisL3
ixNet commit

set isisL3_1 [ixNet getList $mac1 isisL3]
set isisL3_2 [ixNet getList $mac2 isisL3]

set isisL3Router1_1 [ixNet getList $t1dev1 isisL3Router]
set isisL3Router2_1 [ixNet getList $t2dev1 isisL3Router]

puts "Making the NetworkType to Point to Point in the first ISIS router"
set networkTypeMultiValue1 [ixNet getAttr $isisL3_1 -networkType]
ixNet setAttr $networkTypeMultiValue1 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue1/singleValue -value pointpoint

puts "Making the NetworkType to Point to Point in the Second ISIS router"
set networkTypeMultiValue2 [ixNet getAttr $isisL3_2 -networkType]
ixNet setAttr $networkTypeMultiValue2 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue2/singleValue -value pointpoint

# Disable Discard Learned LSP
puts "Disabling the Discard Learned Info CheckBox"

set isisL3RouterDiscardLearnedLSP1 [ ixNet getAttr [ixNet getList [ixNet getList $topo1 deviceGroup] isisL3Router] -discardLSPs]
set isisL3RouterDiscardLearnedLSP2 [ ixNet getAttr [ixNet getList [ixNet getList $topo2 deviceGroup] isisL3Router] -discardLSPs]

ixNet setAttr $isisL3RouterDiscardLearnedLSP1 -pattern singleValue -clearOverlays False
ixNet setAttr $isisL3RouterDiscardLearnedLSP1/singleValue -value False
ixNet setAttr $isisL3RouterDiscardLearnedLSP2 -pattern singleValue -clearOverlays False
ixNet setAttr $isisL3RouterDiscardLearnedLSP2/singleValue -value False

# BIER related configuration
puts "Enabling BIER"
ixNet setAttr $isisL3Router1_1 -enableBIER 1
ixNet setAttr $isisL3Router2_1 -enableBIER 1

puts "Setting Node Prefix"
ixNet setAttr [ixNet getAttribute $isisL3Router1_1 -BIERNodePrefix]/singleValue -value "30.30.30.1"
ixNet setAttr [ixNet getAttribute $isisL3Router2_1 -BIERNodePrefix]/singleValue -value "60.60.60.1"
ixNet commit

puts "Setting Prefix Attribute Flag"
ixNet setAttr [ixNet getAttribute $isisL3Router1_1 -includePrefixAttrFlags]/singleValue -value "true"
ixNet setAttr [ixNet getAttribute $isisL3Router2_1 -includePrefixAttrFlags]/singleValue -value "true"
ixNet commit

puts "Setting R Flag"
ixNet setAttr [ixNet getAttribute $isisL3Router1_1 -bierRFlag]/singleValue -value "true"
ixNet setAttr [ixNet getAttribute $isisL3Router2_1 -bierRFlag]/singleValue -value "true"
ixNet commit

puts "Setting SubDomainId value"
ixNet setAttr [ixNet getAttribute $isisL3Router1_1/isisBierSubDomainList -subDomainId]/singleValue -value "41"
ixNet setAttr [ixNet getAttribute $isisL3Router2_1/isisBierSubDomainList -subDomainId]/singleValue -value "41"
ixNet commit

puts "Setting BFR Id value"
ixNet setAttr [ixNet getAttribute $isisL3Router1_1/isisBierSubDomainList -BFRId]/singleValue -value "141"
ixNet setAttr [ixNet getAttribute $isisL3Router2_1/isisBierSubDomainList -BFRId]/singleValue -value "142"
ixNet commit

set bitStringObj1 [lindex [ixNet getList $isisL3Router1_1/isisBierSubDomainList isisBierBSObjectList ] 0]
set bitStringObj2 [lindex [ixNet getList $isisL3Router2_1/isisBierSubDomainList isisBierBSObjectList ] 0]

puts "Setting Bit String Length"
ixNet setAttr [ixNet getAttribute $bitStringObj1 -BIERBitStringLength]/singleValue -value "4096bits"
ixNet setAttr [ixNet getAttribute $bitStringObj2 -BIERBitStringLength]/singleValue -value "4096bits"
ixNet commit

puts "Setting Label Range Size"
ixNet setAttr [ixNet getAttribute $bitStringObj1 -labelRangeSize]/singleValue -value "5"
ixNet setAttr [ixNet getAttribute $bitStringObj2 -labelRangeSize]/singleValue -value "5"
ixNet commit

puts "Setting Label Start value"
ixNet setAttr [ixNet getAttribute $bitStringObj1 -labelStart]/singleValue -value "444"
ixNet setAttr [ixNet getAttribute $bitStringObj2 -labelStart]/singleValue -value "44"
ixNet commit

puts "Adding Network Topology"
ixNet exec createDefaultStack $t1devices ipv4PrefixPools
ixNet exec createDefaultStack $t2devices ipv4PrefixPools

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

ixNet setAttr $networkGroup1 -name "NG1 For PE Loopback Address"
ixNet setAttr $networkGroup2 -name "NG2 For PE Loopback Address"
ixNet commit

set netTopo1 [ixNet getList $networkGroup1 ipv4PrefixPools]
set netTopo2 [ixNet getList $networkGroup2 ipv4PrefixPools]

ixNet setAttr $netTopo1 -numberOfAddresses 5
ixNet setAttr $netTopo2 -numberOfAddresses 5
ixNet commit

ixNet setAttr [ixNet getAttribute $netTopo1 -networkAddress]/singleValue -value "2.2.2.2"
ixNet setAttr [ixNet getAttribute $netTopo2 -networkAddress]/singleValue -value "3.2.2.2"
ixNet commit


ixNet setAttr [ixNet getAttribute $netTopo1 -prefixLength]/singleValue -value "32"
ixNet setAttr [ixNet getAttribute $netTopo2 -prefixLength]/singleValue -value "32"
ixNet commit

set isisL3RouteProperty1 [lindex [ixNet getList $netTopo1 isisL3RouteProperty] 0]
set isisL3RouteProperty2 [lindex [ixNet getList $netTopo2 isisL3RouteProperty] 0]

puts "Configuring BIER in network group"
puts "Setting Sub-domain Id"
ixNet setAttr [ixNet getAttribute $isisL3RouteProperty1 -subDomainId]/singleValue -value "41"
ixNet setAttr [ixNet getAttribute $isisL3RouteProperty2 -subDomainId]/singleValue -value "41"
ixNet commit

puts "Setting IPA"
ixNet setAttr [ixNet getAttribute $isisL3RouteProperty1 -IPA]/singleValue -value "49"
ixNet setAttr [ixNet getAttribute $isisL3RouteProperty2 -IPA]/singleValue -value "50"
ixNet commit

puts "Setting BFR Id"
ixNet setAttr [ixNet getAttribute $isisL3RouteProperty1 -BFRId]/singleValue -value "12"
ixNet setAttr [ixNet getAttribute $isisL3RouteProperty2 -BFRId]/singleValue -value "14"
ixNet commit

puts "Setting Bit String Length"
ixNet setAttr [ixNet getAttribute $isisL3RouteProperty1 -BIERBitStringLength]/singleValue -value "4096bits"
ixNet setAttr [ixNet getAttribute $isisL3RouteProperty2 -BIERBitStringLength]/singleValue -value "4096bits"
ixNet commit

puts "Setting Label Range Size"
ixNet setAttr [ixNet getAttribute $isisL3RouteProperty1 -labelRangeSize]/singleValue -value "5"
ixNet setAttr [ixNet getAttribute $isisL3RouteProperty2 -labelRangeSize]/singleValue -value "5"
ixNet commit

puts "Setting Label Range Start"
ixNet setAttr [ixNet getAttribute $isisL3RouteProperty1 -labelStart]/singleValue -value "1111"
ixNet setAttr [ixNet getAttribute $isisL3RouteProperty2 -labelStart]/singleValue -value "2222"
ixNet commit

puts "Adding Chained DG behind Network Topology in Ingress Topology"
set chainedDg1 [ixNet add $networkGroup1 deviceGroup]
ixNet commit
set chainedDg1 [lindex [ixNet remapIds $chainedDg1] 0]
ixNet setMultiAttribute $chainedDg1\
    -multiplier 5                  \
    -name {BFIR}
ixNet commit

set loopback1 [ixNet add $chainedDg1 "ipv4Loopback"]
ixNet setMultiAttribute $loopback1\
    -stackedLayers [list]         \
    -name {IPv4 Loopback 1}
ixNet commit

puts "Adding Chained DG behind Network Topology in Egress Topology"
set chainedDg2 [ixNet add $networkGroup2 deviceGroup]
ixNet setMultiAttribute $chainedDg2\
    -multiplier 5                  \
    -name {BFER}
ixNet commit
set chainedDg2 [lindex [ixNet remapIds $chainedDg2] 0]

set loopback2 [ixNet add $chainedDg2 "ipv4Loopback"]
ixNet setMultiAttribute $loopback2\
    -stackedLayers [list]         \
    -name {IPv4 Loopback 2}
ixNet commit

puts "Adding BGP over IPv4 loopback interfaces"
ixNet add $loopback1 bgpIpv4Peer
ixNet add $loopback2 bgpIpv4Peer
ixNet commit

set bgp1 [ixNet getList $loopback1 bgpIpv4Peer]
set bgp2 [ixNet getList $loopback2 bgpIpv4Peer]

puts "Setting IPs in BGP DUT IP tab"
set dutIp1 [ixNet getAttr $bgp1 -dutIp]
ixNet setMultiAttribute $dutIp1 -clearOverlays false  -pattern counter
ixNet commit
ixNet setMultiAttribute $dutIp1/counter\
    -step 0.0.0.1                              \
    -start 3.2.2.2                             \
    -direction increment
ixNet commit

set dutIp2 [ixNet getAttr $bgp2 -dutIp]
ixNet setMultiAttribute $dutIp2 -clearOverlays false  -pattern counter
ixNet commit
ixNet setMultiAttribute $dutIp2/counter\
    -step 0.0.0.1                              \
    -start 2.2.2.2                             \
    -direction increment
ixNet commit


puts "Enabling MVPN Capabilities for BGP Router"
ixNet setAttr [ixNet getAttr $bgp1 -capabilityIpV4MplsVpn]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp1 -capabilityIpV4Multicast]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp1 -capabilityIpV4MulticastVpn]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp1 -ipv4MulticastBgpMplsVpn]/singleValue -value true
ixNet commit

ixNet setAttr [ixNet getAttr $bgp2 -capabilityIpV4MplsVpn]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp2 -capabilityIpV4Multicast]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp2 -capabilityIpV4MulticastVpn]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp2 -ipv4MulticastBgpMplsVpn]/singleValue -value true
ixNet commit

puts "Enabling MVPN Learned Information for BGP Router"
ixNet setAttr [ixNet getAttr $bgp1 -filterIpV4Unicast]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp1 -filterIpV4MplsVpn]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp1 -filterIpv4MulticastBgpMplsVpn]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp1 -filterIpV4MulticastVpn]/singleValue -value true
ixNet commit

ixNet setAttr [ixNet getAttr $bgp2 -filterIpV4Unicast]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp2 -filterIpV4MplsVpn]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp2 -filterIpv4MulticastBgpMplsVpn]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp2 -filterIpV4MulticastVpn]/singleValue -value true
ixNet commit

puts "Adding mVRF over BGP on both ports"
ixNet add $bgp1 bgpIpv4MVrf
ixNet add $bgp2 bgpIpv4MVrf
ixNet commit

set mVRF1 [ixNet getList $bgp1 bgpIpv4MVrf]
set mVRF2 [ixNet getList $bgp2 bgpIpv4MVrf]

puts "Setting Tunnel Type as BIER for I-PMSI"
ixNet setAttr [ixNet getAttribute $mVRF1 -multicastTunnelType]/singleValue -value "tunneltypebier"
ixNet setAttr [ixNet getAttribute $mVRF2 -multicastTunnelType]/singleValue -value "tunneltypebier"
ixNet commit

puts "Assigning value for Up/DownStream Assigned Label for I-PMSI"
set upOrDownStreamAssignedLabel1 [ixNet getAttr $mVRF1 -upOrDownStreamAssignedLabel]
ixNet setMultiAttribute $upOrDownStreamAssignedLabel1 -clearOverlays false  -pattern counter
ixNet commit
ixNet setMultiAttribute $upOrDownStreamAssignedLabel1/counter\
    -step 1                              \
    -start 3333                             \
    -direction increment
ixNet commit

set upOrDownStreamAssignedLabel2 [ixNet getAttr $mVRF2 -upOrDownStreamAssignedLabel]
ixNet setMultiAttribute $upOrDownStreamAssignedLabel2 -clearOverlays false  -pattern counter
ixNet commit
ixNet setMultiAttribute $upOrDownStreamAssignedLabel2/counter\
    -step 1                              \
    -start 4444                             \
    -direction increment
ixNet commit

puts "Setting Sub-domain ID for I-PMSI"
ixNet setAttr [ixNet getAttribute $mVRF1 -BIERSubDomainId]/singleValue -value "41"
ixNet setAttr [ixNet getAttribute $mVRF2 -BIERSubDomainId]/singleValue -value "41"
ixNet commit

puts "Setting BFR ID for I-PMSI"
set bfrid1 [ixNet getAttribute $mVRF1 -BFRId]
ixNet setMultiAttribute $bfrid1 -clearOverlays false  -pattern counter
ixNet commit
ixNet setMultiAttribute $bfrid1/counter\
    -step 1                              \
    -start 33                             \
    -direction increment
ixNet commit

set bfrid2 [ixNet getAttribute $mVRF2 -BFRId]
ixNet setMultiAttribute $bfrid2 -clearOverlays false  -pattern counter
ixNet commit
ixNet setMultiAttribute $bfrid2/counter\
    -step 1                              \
    -start 44                             \
    -direction increment
ixNet commit

puts "Setting BFR IPv4 Prefix for I-PMSI"
set ipv4prefix1 [ixNet getAttribute $mVRF1 -BFRIpv4Prefix]
ixNet setMultiAttribute $ipv4prefix1 -clearOverlays false  -pattern counter
ixNet commit
ixNet setMultiAttribute $ipv4prefix1/counter\
    -step 0.0.0.1                              \
    -start 33.1.1.1                             \
    -direction increment
ixNet commit

set ipv4prefix2 [ixNet getAttribute $mVRF2 -BFRIpv4Prefix]
ixNet setMultiAttribute $ipv4prefix2 -clearOverlays false  -pattern counter
ixNet commit
ixNet setMultiAttribute $ipv4prefix2/counter\
    -step 0.0.0.1                              \
    -start 44.1.1.1                             \
    -direction increment
ixNet commit

puts "Setting Bit String Length for I-PMSI"
ixNet setAttr [ixNet getAttribute $mVRF1 -bierBitStringLength]/singleValue -value "4096bits"
ixNet setAttr [ixNet getAttribute $mVRF2 -bierBitStringLength]/singleValue -value "4096bits"
ixNet commit

puts "Setting Entropy for I-PMSI"
ixNet setAttr [ixNet getAttribute $mVRF1 -entropy]/singleValue -value "100"

puts "Setting OAM for I-PMSI"
ixNet setAttr [ixNet getAttribute $mVRF1 -oam]/singleValue -value "2"

puts "Setting DSCP for I-PMSI"
ixNet setAttr [ixNet getAttribute $mVRF1 -dscp]/singleValue -value "63"

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

puts "Adding IPv4 Prefix pools in Ingress Topology behind Sender PE router"
ixNet add $networkGroup3 ipv4PrefixPools
ixNet commit

puts "Adding IPv4 Prefix pools in Egress Topology behind Receiver PE router"
ixNet add $networkGroup4 ipv4PrefixPools
ixNet commit

puts "Disabling Sender site and enabling Receiver Site for both IPv4 in Egress Topology"
set ipv4PrefixPools3 [lindex [ixNet getList $networkGroup3 ipv4PrefixPools] 0]
set ipv4PrefixPools4 [lindex [ixNet getList $networkGroup4 ipv4PrefixPools] 0]
set bgpL3VpnRouteProperty4 [lindex [ixNet getList $ipv4PrefixPools4 bgpL3VpnRouteProperty] 0]
ixNet setAttr $bgpL3VpnRouteProperty4 -enableIpv4Sender False
ixNet setAttr $bgpL3VpnRouteProperty4 -enableIpv4Receiver True
ixNet commit

set bgpMVpnSenderSitesIpv4 [lindex [ixNet getList $ipv4PrefixPools3 bgpMVpnSenderSitesIpv4] 0]
set bgpMVpnReceiverSitesIpv4 [lindex [ixNet getList $ipv4PrefixPools4 bgpMVpnReceiverSitesIpv4] 0]

puts "Changing Group Address Count for IPv4 Cloud in Sender Site"
set mulValGCount [ixNet getAttr $bgpMVpnSenderSitesIpv4 -groupAddressCount]
ixNet setMultiAttribute $mulValGCount/singleValue -value 3
ixNet commit

puts "Changing Source Address Count for IPv4 Cloud in Sender Site"
set mulValSCount [ixNet getAttr $bgpMVpnSenderSitesIpv4 -sourceAddressCount]
ixNet setMultiAttribute $mulValSCount/singleValue -value 2
ixNet commit

puts "Changing Group Address for IPv4 Cloud in Sender Site"
set mulValGAdd [ixNet getAttr $bgpMVpnSenderSitesIpv4 -startGroupAddressIpv4]
ixNet setMultiAttribute $mulValGAdd -clearOverlays false -pattern counter
ixNet commit
ixNet setMultiAttribute $mulValGAdd/counter\
    -step 0.0.1.0                              \
    -start 234.161.1.1                             \
    -direction increment
ixNet commit

puts "Changing Source Address for IPv4 Cloud in Sender Site"
set mulValSAdd [ixNet getAttr $bgpMVpnSenderSitesIpv4 -startSourceAddressIpv4]
ixNet setMultiAttribute $mulValSAdd -clearOverlays false -pattern counter
ixNet commit
ixNet setMultiAttribute $mulValSAdd/counter\
    -step 0.0.1.0                              \
    -start 191.0.1.1                             \
    -direction increment
ixNet commit

puts "Changing Group Address Count for IPv4 Cloud in Receiver Site"
set mulValGCount [ixNet getAttr $bgpMVpnReceiverSitesIpv4 -groupAddressCount]
ixNet setMultiAttr $mulValGCount -pattern singleValue -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValGCount/singleValue -value 3
ixNet commit

puts "Changing Source Address Count for IPv4 Cloud in Receiver Site"
set mulValSCount [ixNet getAttr $bgpMVpnReceiverSitesIpv4 -sourceAddressCount]
ixNet setMultiAttr $mulValSCount -pattern singleValue -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValSCount/singleValue -value 2
ixNet commit

puts "Changing Group Address for IPv4 Cloud in Receiver Site"
set mulValGAdd [ixNet getAttr $bgpMVpnReceiverSitesIpv4 -startGroupAddressIpv4]
ixNet setMultiAttribute $mulValGAdd -clearOverlays false -pattern counter
ixNet commit
ixNet setMultiAttribute $mulValGAdd/counter\
    -step 0.0.1.0                              \
    -start 234.161.1.1                             \
    -direction increment
ixNet commit

puts "Changing Source Address for IPv4 Cloud in Receiver Site"
set mulValSAdd [ixNet getAttr $bgpMVpnReceiverSitesIpv4 -startSourceAddressIpv4]
ixNet setMultiAttribute $mulValSAdd -clearOverlays false -pattern counter
ixNet commit
ixNet setMultiAttribute $mulValSAdd/counter\
    -step 0.0.1.0                              \
    -start 191.0.1.1                             \
    -direction increment
ixNet commit

puts "Changing Prefix Length for IPv4 Address Pool in Sender Site"
set mulValPrefLenSndr [ixNet getAttr $ipv4PrefixPools3 -prefixLength]
ixNet setMultiAttr $mulValPrefLenSndr -pattern singleValue -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValPrefLenSndr/singleValue -value "32"
ixNet commit

puts "Changing Prefix Length for IPv4 Address Pool in Receiver Site"
set mulValPrefLenRcvr [ixNet getAttr $ipv4PrefixPools4 -prefixLength]
ixNet setMultiAttr $mulValPrefLenRcvr -pattern singleValue -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValPrefLenRcvr/singleValue -value "32"
ixNet commit

puts "Configuring S-PMSI on Sender Sites"
set bgpMVpnSenderSiteSpmsiV4 [lindex [ixNet getList $bgpMVpnSenderSitesIpv4 bgpMVpnSenderSiteSpmsiV4] 0]

puts "Setting Tunnel Type as BIER for S-PMSI"
ixNet setAttr [ixNet getAttribute $bgpMVpnSenderSiteSpmsiV4 -multicastTunnelType]/singleValue -value "tunneltypebier"
ixNet commit

puts "Setting Sub-domain Id for S-PMSI"
ixNet setAttr [ixNet getAttribute $bgpMVpnSenderSiteSpmsiV4 -BIERSubDomainId]/singleValue -value "41"
ixNet commit

puts "Setting BFR ID for S-PMSI"
set bfridSender [ixNet getAttribute $bgpMVpnSenderSiteSpmsiV4 -BFRId]
ixNet setMultiAttribute $bfridSender -clearOverlays false  -pattern counter
ixNet commit
ixNet setMultiAttribute $bfridSender/counter\
    -step 1                              \
    -start 200                             \
    -direction increment
ixNet commit

puts "Setting BFR IPv4 Prefix for S-PMSI at Sender Site (same as own loopback ip)"
set ipv4prefixSender [ixNet getAttribute $bgpMVpnSenderSiteSpmsiV4 -BFRIpv4Prefix]
ixNet setMultiAttribute $ipv4prefixSender -clearOverlays false  -pattern counter
ixNet commit
ixNet setMultiAttribute $ipv4prefixSender/counter\
    -step 0.0.0.1                              \
    -start 2.2.2.2                             \
    -direction increment
ixNet commit

puts "Assigning value for Up/DownStream Assigned Label for S-PMSI"
set upOrDownStreamAssignedLabel1 [ixNet getAttr $bgpMVpnSenderSiteSpmsiV4 -upstreamOrDownstreamAssignedLabel]
ixNet setMultiAttribute $upOrDownStreamAssignedLabel1 -clearOverlays false  -pattern counter
ixNet commit
ixNet setMultiAttribute $upOrDownStreamAssignedLabel1/counter\
    -step 1                              \
    -start 5555                             \
    -direction increment
ixNet commit


puts "Setting Bit String Length for S-PMSI"
ixNet setAttr [ixNet getAttribute $bgpMVpnSenderSiteSpmsiV4 -bierBitStringLength]/singleValue -value "4096bits"

puts "Setting Entropy for S-PMSI"
ixNet setAttr [ixNet getAttribute $bgpMVpnSenderSiteSpmsiV4 -entropy]/singleValue -value "999"

puts "Setting OAM for S-PMSI"
ixNet setAttr [ixNet getAttribute $bgpMVpnSenderSiteSpmsiV4 -oam]/singleValue -value "3"

puts "Setting DSCP for S-PMSI"
ixNet setAttr [ixNet getAttribute $bgpMVpnSenderSiteSpmsiV4 -dscp]/singleValue -value "50"

puts "Setting BFR ID for Receiver Site"
set bfridRcvr [ixNet getAttribute $bgpMVpnReceiverSitesIpv4 -BFRId]
ixNet setMultiAttribute $bfridRcvr -clearOverlays false  -pattern counter
ixNet commit
ixNet setMultiAttribute $bfridRcvr/counter\
    -step 1                              \
    -start 300                             \
    -direction increment
ixNet commit

puts "Setting BFR IPv4 Prefix for S-PMSI at Receiver Site (same as own loopback ip)"
set ipv4prefixSender [ixNet getAttribute $bgpMVpnReceiverSitesIpv4 -BFRIpv4Prefix]
ixNet setMultiAttribute $ipv4prefixSender -clearOverlays false  -pattern counter
ixNet commit
ixNet setMultiAttribute $ipv4prefixSender/counter\
    -step 0.0.0.1                              \
    -start 3.2.2.2                             \
    -direction increment
ixNet commit


################################################################################
# 2. Start protocols.
################################################################################
puts "Wait for 5 seconds before starting protocol"
after 5000
puts "Starting protocols and waiting for 2 min seconds for protocols to come up"
ixNet exec startAllProtocols
after 120000

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

################################################################################
# 4. S-PMSI Trigger
################################################################################
puts "Switching to S-PMSI for IPv4 Cloud from Sender Site"
ixNet exec switchToSpmsi $bgpMVpnSenderSitesIpv4

###############################################################################
# 5. Retrieve BGP MVPN learned info 
###############################################################################
puts "Fetching IPv4 mVPN Learned Info in Ingress topology"
ixNet exec getIpv4MvpnLearnedInfo $bgp1 1
after 5000
puts "IPv4 MVPN Learned Info at BFIR"
set learnedInfoList [ixNet getList $bgp1 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]

puts "mVPN learned info at BFIR"
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

puts "Fetching IPv4 mVPN Learned Info in Egress topology"
ixNet exec getIpv4MvpnLearnedInfo $bgp2 1
after 5000
puts "IPv4 MVPN Learned Info at BFER"
set learnedInfoList [ixNet getList $bgp2 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]

puts "mVPN learned info at BFIR"
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
# 6. Configure L2-L3 IPv4 I-PMSI traffic.
################################################################################
puts "Configuring L2-L3 IPv4 S-PMSI Traffic Item"
set ipmsiTrafficItem [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $ipmsiTrafficItem  \
    -name {NGMVPN I-PMSI Traffic}    \
    -multicastForwardingMode replication \
    -useControlPlaneRate true \
    -useControlPlaneFrameSize true \
    -roundRobinPacketOrdering false \
    -numVlansForMulticastReplication 1 \
    -trafficType ipv4
ixNet commit

set ipmsiTrafficItem [lindex [ixNet remapIds $ipmsiTrafficItem] 0]
set endpointSet [ixNet add $ipmsiTrafficItem "endpointSet"]
set source       [list $bgpMVpnSenderSitesIpv4]
set destination  [list $bgpMVpnReceiverSitesIpv4]
ixNet setMultiAttribute $endpointSet           \
    -name                  "EndpointSet-1"  \
    -multicastDestinations [list [list false none 234.161.1.1 0.0.0.1 3] [list false none 234.161.2.1 0.0.0.1 3] [list false none 234.161.3.1 0.0.0.1 3] [list false none 234.161.4.1 0.0.0.1 3] [list false none 234.161.5.1 0.0.0.1 3]] \
    -multicastReceivers $destination \
    -sources $source
ixNet commit

set endpointSet [lindex [ixNet remapIds $endpointSet] 0]

ixNet setMultiAttribute $ipmsiTrafficItem/configElement:1/frameSize -fixedSize 570
ixNet setMultiAttribute $ipmsiTrafficItem/configElement:1/frameRate -rate 1000 -type framesPerSecond
ixNet setMultiAttribute $ipmsiTrafficItem/configElement:1/frameRateDistribution -streamDistribution applyRateToAll

ixNet setMultiAttribute $ipmsiTrafficItem/tracking -trackBy \
    [list trackingenabled0 mplsMplsLabelValue0 mplsMplsLabelValue1 ipv4DestIp0 bierBsl0]
ixNet commit

################################################################################
# 7. Configure L2-L3 IPv4 S-PMSI traffic.
################################################################################
puts "Configuring L2-L3 IPv4 S-PMSI Traffic Item"
set SpmsiTrafficItem [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $SpmsiTrafficItem  \
    -name {NGMVPN S-PMSI Traffic}    \
    -multicastForwardingMode replication \
    -useControlPlaneRate true \
    -useControlPlaneFrameSize true \
    -roundRobinPacketOrdering false \
    -numVlansForMulticastReplication 1 \
    -trafficType ipv4
ixNet commit

set SpmsiTrafficItem [lindex [ixNet remapIds $SpmsiTrafficItem] 0]
set endpointSet [ixNet add $SpmsiTrafficItem "endpointSet"]
set source       [list $bgpMVpnSenderSiteSpmsiV4]
set destination  [list $bgpMVpnReceiverSitesIpv4]
ixNet setMultiAttribute $endpointSet           \
    -name                  "EndpointSet-1"  \
    -multicastDestinations [list [list false none 234.161.1.1 0.0.0.1 3] [list false none 234.161.2.1 0.0.0.1 3] [list false none 234.161.3.1 0.0.0.1 3] [list false none 234.161.4.1 0.0.0.1 3] [list false none 234.161.5.1 0.0.0.1 3]] \
    -multicastReceivers $destination \
    -sources $source
ixNet commit

set endpointSet [lindex [ixNet remapIds $endpointSet] 0]

ixNet setMultiAttribute $SpmsiTrafficItem/configElement:1/frameSize -fixedSize 570
ixNet setMultiAttribute $SpmsiTrafficItem/configElement:1/frameRate -rate 1000 -type framesPerSecond
ixNet setMultiAttribute $SpmsiTrafficItem/configElement:1/frameRateDistribution -streamDistribution applyRateToAll

ixNet setMultiAttribute $SpmsiTrafficItem/tracking -trackBy \
    [list trackingenabled0 mplsMplsLabelValue0 mplsMplsLabelValue1 ipv4DestIp0 bierBsl0]
ixNet commit

###############################################################################
#8. Apply and start L2/L3 traffic.
###############################################################################
puts "applying traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000
puts "starting traffic"
ixNet exec start [ixNet getRoot]/traffic
puts "let traffic run for 60 second"
after 60000

###############################################################################
# 9. Retrieve L2/L3 traffic item statistics.
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
# 10. Stop L2/L3 traffic.
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 11. Stop all protocols.
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
