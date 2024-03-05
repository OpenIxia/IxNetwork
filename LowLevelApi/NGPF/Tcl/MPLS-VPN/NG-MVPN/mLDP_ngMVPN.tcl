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
#    This script intends to demonstrate how to use mLDP as P-tunnel in NGMVPN   #
#    through API.                                                               #
#    About Topology:                                                            #
#    Within topology both Sender and Receiver PEs are configured, each behind   #
#    Ingress and Egress P routers respectively. P2MP tunnels used in topology   #
#	 is mLDP-P2MP. Both I-PMSI and S-PMSI tunnels for IPv4 & Ipv6 multicast     #
#    streams are configured using mLDP-P2MP. Multicast traffic source address   #
#    are distributed by BGP as VPN routes(AFI:1,SAFI:128). Multicast L2-L3      #
#    Traffic from Seder to Receiver                                             #
# Script Flow:                                                                  #
#        Step 1. Configuration of protocols.                                    #
#    Configuration flow of the script is as follow:                             #
#         i.      Adding of OSPF router                                         #
#         ii.     Adding of Network Topology(NT)                                #
#         iii.    Enabling of TE(Traffic Engineering) and configuring loopback  #
#                         address as Router ID                                  #
#         iv.     Adding of mLDP LSPs within LDP RTR and mVRF over BGP over     #
#                  loopback within connected DG.                                #
#         v.     Configuring Parameters in mVRF at sender and Receiver PE       #
#         vi.    Adding Route Ranges(both IPv4 and v6) behind mVRF as Sender    #
#                 Router and Receiver Sites.                                    #
#         vii.   Configuring I-PMSI and S-PMSI Tunnel in Sender Sites for both  #
#                 IPv4/v6 ranges as per mLDP LSP.                               #
#        Step 2. Start of protocol                                              #
#        Step 3. Retrieve protocol statistics                                   #
#        Step 4. Retrieve IPv4 mVPN learned info                                #
#        Step 5. Apply changes on the fly                                       #
#        Step 6. S-PMSI Trigger                                                 #
#        Step 7. Retrieve protocol learned info after OTF                       #
#        Step 8. Configure L2-L3 IPv6 I-PMSI traffic.                           #
#        Step 9. Configure L2-L3 IPv4 S-PMSI traffic.                           #
#        Step 10. Apply and start L2/L3 traffic.                                #
#        Step 11. Retrieve L2/L3 traffic item statistics.                       #
#        Step 12. Stop L2/L3 traffic.                                           #
#        Step 13. Stop all protocols.                                           #
#################################################################################

# edit this variables values to match your setup

namespace eval ::ixia {
    set ixTclServer 10.39.50.134
    set ixTclPort   8819
    set ports       {{10.39.50.161 2 3} { 10.39.50.161 2 4}}
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

ixNet setAttr $topo1  -name "Ingress Topology"
ixNet setAttr $topo2  -name "Egress Topology"

set t1dev1 [lindex $t1devices 0]
set t2dev1 [lindex $t2devices 0]
ixNet setAttr $t1dev1 -name "Sender P router"
ixNet setAttr $t2dev1 -name "Receiver P router"
ixNet commit
puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $t1dev1 -multiplier 2
ixNet setAttr $t2dev1 -multiplier 2
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
        -step       {00:00:00:00:00:01}

ixNet setAttr [ixNet getAttr $mac2 -mac]/counter\
        -direction  increment                        \
        -start      {44:44:44:44:44:44}              \
        -step       {00:00:00:00:00:01} 
ixNet commit

puts "Enabling VLAN"
ixNet setMultiAttr [ixNet getAttr $mac1 -enableVlans]/singleValue\
        -value  true

ixNet setMultiAttr [ixNet getAttr $mac2 -enableVlans]/singleValue\
        -value  true
ixNet commit

puts "Configuring VLAN ID"
ixNet setMultiAttr [ixNet getAttr $mac1/vlan:1 -vlanId]/counter\
        -direction  increment                        \
        -start      {400}              \
        -step       {1}

ixNet setMultiAttr [ixNet getAttr $mac2/vlan:1 -vlanId]/counter\
        -direction  increment                        \
        -start      {400}              \
        -step       {1}
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
ixNet setMultiAttr $mvAdd1/counter\
        -direction  increment                        \
        -start      {50.50.50.2}              \
        -step       {0.1.0.0}

ixNet setMultiAttr $mvAdd2/counter\
        -direction  increment                        \
        -start      {50.50.50.20}              \
        -step       {0.1.0.0}

ixNet setMultiAttr $mvGw1/counter\
        -direction  increment                        \
        -start      {50.50.50.20}              \
        -step       {0.1.0.0}

ixNet setMultiAttr $mvGw2/counter\
        -direction  increment                        \
        -start      {50.50.50.2}              \
        -step       {0.1.0.0}

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

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
ixNet commit

puts "Adding Connected LDP-IF over IPv4 stack"
ixNet add $ip1 ldpConnectedInterface
ixNet add $ip2 ldpConnectedInterface
ixNet commit

puts "Adding Connected LDP-RTR over IPv4 stack"
ixNet add $ip1 ldpBasicRouter
ixNet add $ip2 ldpBasicRouter
ixNet commit

set ldp1 [ixNet getList $ip1 ldpBasicRouter]
set ldp2 [ixNet getList $ip2 ldpBasicRouter]

puts "Enabling P2MP Capability in the first LDP router"
set p2MpCapability1 [ixNet getAttr $ldp1 -enableP2MPCapability]
ixNet setAttr $p2MpCapability1 -pattern singleValue -clearOverlays False
ixNet setAttr $p2MpCapability1/singleValue -value true
ixNet commit

puts "Enabling P2MP Capability in the second LDP router"
set p2MpCapability2 [ixNet getAttr $ldp2 -enableP2MPCapability]
ixNet setMultiAttr $p2MpCapability2 -pattern singleValue -clearOverlays False
ixNet setMultiAttr $p2MpCapability2/singleValue -value true
ixNet commit

puts "Enabling Root ranges in the Sender P LDP router"
ixNet setMultiAttr $ldp1 -rootRangesCountV4 1
ixNet commit

puts "Enabling Root ranges in the Receiver P LDP router"
ixNet setMultiAttr $ldp2 -rootRangesCountV4 1
ixNet commit

puts "Enabling Leaf ranges in the Sender P LDP router"
ixNet setMultiAttr $ldp1 -leafRangesCountV4 1
ixNet commit

puts "Enabling Leaf ranges in the Receiver P LDP router"
ixNet setMultiAttr $ldp2 -leafRangesCountV4 1
ixNet commit

puts "Configuring mLDP Leaf range in Sender LDP router"
ixNet setMultiAttr $ldp1/ldpLeafRangeV4 -numberOfTLVs 3
ixNet commit

puts "Configuring mLDP Leaf range in Receiver LDP router"
ixNet setMultiAttr $ldp2/ldpLeafRangeV4 -numberOfTLVs 3
ixNet commit

puts "Activating mLDP Leaf range in Sender LDP router"
set active1 [ixNet getAttribute $ldp1/ldpLeafRangeV4 -active] 
ixNet setMultiAttr $active1/singleValue -value true
ixNet commit

puts "Changing Continuous Increment Opaque Value Across Root in mLDP Leaf range in Sender LDP router"
set contIncOpq1 [ixNet getAttribute $ldp1/ldpLeafRangeV4 -continuousIncrementOVAcrossRoot]
ixNet setMultiAttr $contIncOpq1/singleValue -value true
ixNet commit

puts "Changing Label Value Step in mLDP Leaf range in Sender LDP router"
set label1 [ixNet getAttribute $ldp1/ldpLeafRangeV4 -labelValueStep]
ixNet setMultiAttr $label1/singleValue -value 1
ixNet commit

puts "Changing Label Value Start in mLDP Leaf range in Sender LDP router"
set start1 [ixNet getAttribute $ldp1/ldpLeafRangeV4 -labelValueStart]
ixNet setMultiAttr $start1 -pattern counter -clearOverlays False
ixNet commit
ixNet setMultiAttr $start1/counter\
        -direction  increment       \
        -start      {12321}   \
        -step       {1}
ixNet commit

puts "Changing LSP count per root in mLDP Leaf range in Sender LDP router"
set lspCountPerRoot1 [ixNet getAttribute $ldp1/ldpLeafRangeV4 -lspCountPerRoot]
ixNet setMultiAttr $lspCountPerRoot1/singleValue -value 2
ixNet commit

puts "Changing Root Address Step in mLDP Leaf range in Sender LDP router"
set rootAddStep1 [ixNet getAttribute $ldp1/ldpLeafRangeV4 -rootAddressStep]
ixNet setMultiAttr $rootAddStep1/singleValue -value 0.0.0.1
ixNet commit

puts "Changing Root Address Count in mLDP Leaf range in Sender LDP router"
set rootAddCnt1 [ixNet getAttribute $ldp1/ldpLeafRangeV4 -rootAddressCount]
ixNet setMultiAttr $rootAddCnt1/singleValue -value 1
ixNet commit

puts "Changing Root Address in mLDP Leaf range in Sender LDP router"
set rootAdd1 [ixNet getAttribute $ldp1/ldpLeafRangeV4 -rootAddress]
ixNet setMultiAttr $rootAdd1 -pattern singleValue -clearOverlays False
ixNet commit
ixNet setMultiAttr $rootAdd1/singleValue\
        -value      {7.7.7.7}
ixNet commit

puts "Changing TLV1 name in mLDP Leaf range in Sender LDP router"
ixNet setMultiAttr $ldp1/ldpLeafRangeV4/ldpTLVList:1 -name "LDP Opaque TLV 1"
ixNet commit

puts "Deactivating TLV1 in mLDP Leaf range in Sender LDP router"
set active1 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:1 -active]
ixNet setMultiAttr $active1/singleValue -value false
ixNet commit

puts "Changing Type of TLV1 in mLDP Leaf range in Sender LDP router"
set type1 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:1 -type]
ixNet setMultiAttr $type1/singleValue -value 1
ixNet commit

puts "Changing Length of TLV1 in mLDP Leaf range in Sender LDP router"
set len1 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:1 -tlvLength]
ixNet setMultiAttr $len1/singleValue -value 4
ixNet commit

puts "Changing Value of TLV1 in mLDP Leaf range in Sender LDP router"
set val1 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:1 -value]
ixNet setMultiAttr $val1 -pattern counter -clearOverlays False
ixNet commit
ixNet setMultiAttr $val1/counter\
        -direction  increment       \
        -start      {00000001}   \
        -step       {01}
ixNet commit

puts "Changing Increment of TLV1 in mLDP Leaf range in Sender LDP router"
set inc1 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:1 -increment]
ixNet setMultiAttr $inc1/singleValue -value 00000001
ixNet commit

puts "Changing TLV2 name in mLDP Leaf range in Sender LDP router"
ixNet setMultiAttr $ldp1/ldpLeafRangeV4/ldpTLVList:2 -name "LDP Opaque TLV 2"
ixNet commit

puts "Activating TLV2 in mLDP Leaf range in Sender LDP router"
set active2 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:2 -active]
ixNet setMultiAttr $active2/singleValue -value true
ixNet commit

puts "Changing Type of TLV2 in mLDP Leaf range in Sender LDP router"
set type2 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:2 -type]
ixNet setMultiAttr $type2/singleValue -value 123
ixNet commit

puts "Changing Length of TLV2 in mLDP Leaf range in Sender LDP router"
set len2 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:2 -tlvLength]
ixNet setMultiAttr $len2/singleValue -value 5
ixNet commit

puts "Changing Value of TLV2 in mLDP Leaf range in Sender LDP router"
set val2 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:2 -value]
ixNet setMultiAttr $val2 -pattern counter -clearOverlays False
ixNet commit
ixNet setMultiAttr $val2/counter\
        -direction  increment       \
        -start      {000000A1}   \
        -step       {04}
ixNet commit

puts "Changing Increment of TLV2 in mLDP Leaf range in Sender LDP router"
set inc2 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:2 -increment]
ixNet setMultiAttr $inc2/singleValue -value 00000001
ixNet commit

puts "Changing TLV3 name in mLDP Leaf range in Sender LDP router"
ixNet setMultiAttr $ldp1/ldpLeafRangeV4/ldpTLVList:3 -name "LDP Opaque TLV 3"
ixNet commit

puts "Activating TLV3 in mLDP Leaf range in Sender LDP router"
set active3 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:3 -active]
ixNet setMultiAttr $active3/singleValue -value true
ixNet commit

puts "Changing Type of TLV3 in mLDP Leaf range in Sender LDP router"
set type3 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:3 -type]
ixNet setMultiAttr $type3/singleValue -value 1
ixNet commit

puts "Changing Length of TLV3 in mLDP Leaf range in Sender LDP router"
set len3 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:3 -tlvLength]
ixNet setMultiAttr $len3/singleValue -value 4
ixNet commit

puts "Changing Value of TLV3 in mLDP Leaf range in Sender LDP router"
set val3 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:3 -value]
ixNet setMultiAttr $val3 -pattern counter -clearOverlays False
ixNet commit
ixNet setMultiAttr $val3/singleValue\
        -value {00000001}
ixNet commit

puts "Changing Increment of TLV3 in mLDP Leaf range in Sender LDP router"
set inc3 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:3 -increment]
ixNet setMultiAttr $inc3/singleValue -value 00000001
ixNet commit

puts "Configuring mLDP Leaf range in Receiver LDP router"
puts "Activating mLDP Leaf range in Receiver LDP router"
set active22 [ixNet getAttribute $ldp2/ldpLeafRangeV4 -active]
ixNet setMultiAttr $active22/singleValue -value true
ixNet commit

puts "Changing Continuous Increment Opaque Value Across Root in mLDP Leaf range in Receiver LDP router"
set contIncOpq22 [ixNet getAttribute $ldp2/ldpLeafRangeV4 -continuousIncrementOVAcrossRoot]
ixNet setMultiAttr $contIncOpq22/singleValue -value true
ixNet commit

puts "Changing Label Value Step in mLDP Leaf range in Receiver LDP router"
set label22 [ixNet getAttribute $ldp2/ldpLeafRangeV4 -labelValueStep]
ixNet setMultiAttr $label22/singleValue -value 1
ixNet commit

puts "Changing Label Value Start in mLDP Leaf range in Receiver LDP router"
set start22 [ixNet getAttribute $ldp2/ldpLeafRangeV4 -labelValueStart]
ixNet setMultiAttr $start22 -pattern counter -clearOverlays False
ixNet commit
ixNet setMultiAttr $start22/counter\
        -direction  increment       \
        -start      {8916}   \
        -step       {100}
ixNet commit

puts "Changing LSP count per root in mLDP Leaf range in Receiver LDP router"
set lspCountPerRoot22 [ixNet getAttribute $ldp2/ldpLeafRangeV4 -lspCountPerRoot]
ixNet setMultiAttr $lspCountPerRoot22/singleValue -value 6
ixNet commit

puts "Changing Root Address Step in mLDP Leaf range in Receiver LDP router"
set rootAddStep22 [ixNet getAttribute $ldp2/ldpLeafRangeV4 -rootAddressStep]
ixNet setMultiAttr $rootAddStep22/singleValue -value 0.0.0.1
ixNet commit

puts "Changing Root Address Count in mLDP Leaf range in Receiver LDP router"
set rootAddCnt22 [ixNet getAttribute $ldp2/ldpLeafRangeV4 -rootAddressCount]
ixNet setMultiAttr $rootAddCnt22/singleValue -value 1
ixNet commit

puts "Changing Root Address in mLDP Leaf range in Receiver LDP router"
set rootAdd22 [ixNet getAttribute $ldp2/ldpLeafRangeV4 -rootAddress]
ixNet commit
ixNet setMultiAttr $rootAdd22 -pattern singleValue -clearOverlays False
ixNet commit
ixNet setMultiAttr $rootAdd22/singleValue\
        -value      {8.8.8.7}
ixNet commit

puts "Changing TLV1 name in mLDP Leaf range in Receiver LDP router"
ixNet setMultiAttr $ldp2/ldpLeafRangeV4/ldpTLVList:1 -name "LDP Opaque TLV 4"
ixNet commit

puts "Activating TLV1 in mLDP Leaf range in Receiver LDP router"
set active4 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:1 -active]
ixNet setMultiAttr $active4/singleValue -value true
ixNet commit

puts "Changing Type of TLV1 in mLDP Leaf range in Receiver LDP router"
set type4 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:1 -type]
ixNet setMultiAttr $type4/singleValue -value 111
ixNet commit

puts "Changing Length of TLV1 in mLDP Leaf range in Receiver LDP router"
set len4 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:1 -tlvLength]
ixNet setMultiAttr $len4 -pattern singleValue -clearOverlays False
ixNet setMultiAttr $len4/singleValue -value 33
ixNet commit

puts "Changing Value of TLV1 in mLDP Leaf range in Receiver LDP router"
set val4 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:1 -value]

ixNet setMultiAttr $val4 -pattern counter -clearOverlays False
ixNet commit
ixNet setMultiAttr $val4/counter\
        -direction  increment       \
        -start      {000000000000000000000000000000000000000000000000000000000000007651}   \
        -step       {04}
ixNet commit

puts "Changing Increment of TLV1 in mLDP Leaf range in Receiver LDP router"
set inc4 [ixNet getAttribute $ldp1/ldpLeafRangeV4/ldpTLVList:1 -increment]
ixNet setMultiAttr $inc4/singleValue -value 00000001
ixNet commit

puts "Changing TLV2 name in mLDP Leaf range in Receiver LDP router"
ixNet setMultiAttr $ldp2/ldpLeafRangeV4/ldpTLVList:2 -name "LDP Opaque TLV 5"
ixNet commit

puts "Activating TLV2 in mLDP Leaf range in Receiver LDP router"
set active5 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:2 -active]
ixNet setMultiAttr $active5/singleValue -value true
ixNet commit

puts "Changing Type of TLV2 in mLDP Leaf range in Receiver LDP router"
set type5 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:2 -type]
ixNet setMultiAttr $type5/singleValue -value 123
ixNet commit

puts "Changing Length of TLV2 in mLDP Leaf range in Receiver LDP router"
set len5 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:2 -tlvLength]
ixNet setMultiAttr $len5 -pattern singleValue -clearOverlays False
ixNet setMultiAttr $len5/singleValue -value 5
ixNet commit

puts "Changing Value of TLV2 in mLDP Leaf range in Receiver LDP router"
set val5 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:2 -value]
ixNet setMultiAttr $val5 -pattern counter -clearOverlays False
ixNet commit
ixNet setMultiAttr $val5/counter\
        -direction  increment       \
        -start      {00000000A1}    \
        -step       {04}
ixNet commit

puts "Changing Increment of TLV2 in mLDP Leaf range in Receiver LDP router"
set inc5 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:2 -increment]
ixNet setMultiAttr $inc5/singleValue -value 00000001
ixNet commit

puts "Changing TLV3 name in mLDP Leaf range in Receiver LDP router"
ixNet setMultiAttr $ldp2/ldpLeafRangeV4/ldpTLVList:3 -name "LDP Opaque TLV 6"
ixNet commit

puts "Activating TLV3 in mLDP Leaf range in Receiver LDP router"
set active6 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:3 -active]
ixNet setMultiAttr $active6/singleValue -value true
ixNet commit

puts "Changing Type of TLV3 in mLDP Leaf range in Receiver LDP router"
set type6 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:3 -type]
ixNet setMultiAttr $type6/singleValue -value 1
ixNet commit

puts "Changing Length of TLV3 in mLDP Leaf range in Receiver LDP router"
set len6 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:3 -tlvLength]
ixNet setMultiAttr $len6 -pattern singleValue -clearOverlays False
ixNet setMultiAttr $len6/singleValue -value 4
ixNet commit

puts "Changing Value of TLV3 in mLDP Leaf range in Receiver LDP router"
set val6 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:3 -value]
ixNet setMultiAttr $val6 -pattern counter -clearOverlays False
ixNet commit
ixNet setMultiAttr $val6/singleValue -value 00000001
ixNet commit

puts "Changing Increment of TLV3 in mLDP Leaf range in Receiver LDP router"
set inc6 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:3 -increment]
ixNet setMultiAttr $inc6/singleValue -value 00000001
ixNet commit

puts "Adding the Network Topology behind Ethernet for Sender P router"
ixNet exec createDefaultStack $t1devices networkTopology
set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set netTopo1 [ixNet getList $networkGroup1 networkTopology]
ixNet setAttr $networkGroup1 -name "Simulated Topology for Sender PE Address"
ixNet commit

puts "Adding the Network Topology behind Ethernet for Receiver P router"
ixNet exec createDefaultStack $t2devices networkTopology
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]
set netTopo2 [ixNet getList $networkGroup2 networkTopology]
ixNet setAttr $networkGroup2 -name "Simulated Topology for Receiver PE Address"
ixNet commit

puts "Enabling Traffic Engineering behind mVRF for Sender P router"
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

puts "Enabling Traffic Engineering behind mVRF for Receiver P router"
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

puts "Add IPv4 Loopback for PE"
set loopback1 [ixNet add $t1dev1 "ipv4Loopback"]
set loopback2 [ixNet add $t2dev1 "ipv4Loopback"]

puts "Changing the IPv4 Loopback name and address in Sender P router"
ixNet setMultiAttribute $loopback1 -name {IPv4 Loopback 1}
ixNet commit

ixNet setMultiAttribute $loopback2 -name {IPv4 Loopback 2}
ixNet commit

set lpbk_add1 [ixNet getAttribute $loopback1 -address]
ixNet setMultiAttribute $lpbk_add1 \
                       -clearOverlays false           \
                       -pattern singleValue
ixNet setMultiAttr $lpbk_add1 -pattern counter -clearOverlays False
ixNet commit
ixNet setMultiAttr $lpbk_add1/counter\
        -direction  increment                        \
        -start      {8.8.8.7}              \
        -step       {0.0.0.1}
ixNet commit

set lpbk_add2 [ixNet getAttribute $loopback2 -address]
ixNet setMultiAttribute $lpbk_add2 \
                       -clearOverlays false           \
                       -pattern singleValue
ixNet setMultiAttr $lpbk_add2 -pattern counter -clearOverlays False
ixNet commit
ixNet setMultiAttr $lpbk_add2/counter\
        -direction  increment                        \
        -start      {7.7.7.7}              \
        -step       {0.0.0.1}
ixNet commit

puts "Adding BGP over IPv4 loopback interfaces"
ixNet add $loopback1 bgpIpv4Peer
ixNet add $loopback2 bgpIpv4Peer
ixNet commit

set bgp1 [ixNet getList $loopback1 bgpIpv4Peer]
set bgp2 [ixNet getList $loopback2 bgpIpv4Peer]

puts "Setting IPs in BGP DUT IP tab"
set dutIp1 [ixNet getAttribute $bgp1 -dutIp]
ixNet setMultiAttr $dutIp1/counter\
        -direction  increment       \
        -step       {0.0.0.1}       \
        -start      {7.7.7.7}
ixNet commit

set dutIp2 [ixNet getAttribute $bgp2 -dutIp]
ixNet setMultiAttr $dutIp2/counter\
        -direction  increment       \
        -step       {0.0.0.1}       \
        -start      {8.8.8.7}
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

puts "Configuring mLDP P2MP as the Tunnel Type in Sender P router"
set tunnel_type1 [ixNet getAttribute $mVRF1 -multicastTunnelType]
ixNet setMultiAttribute $tunnel_type1/singleValue -value tunneltypemldpp2mp
ixNet commit

puts "Configuring mLDP P2MP as the Tunnel Type in Receiver P router"
set tunnel_type2 [ixNet getAttribute $mVRF2 -multicastTunnelType]
ixNet setMultiAttribute $tunnel_type2/singleValue -value tunneltypemldpp2mp
ixNet commit

puts "Configuring Root Address in Topology 1"
set rtAdd1 [ixNet getAttribute $mVRF1 -rootAddress]
ixNet setMultiAttribute $rtAdd1/singleValue -value 8.8.8.7
ixNet commit

puts "Enabling CheckBox for use of Up/DownStream Assigned Label for Ingress Topology"
set useUpOrDownStreamAssigneLabel1 [ixNet getAttr $mVRF1 -useUpOrDownStreamAssigneLabel]
ixNet setAttr $useUpOrDownStreamAssigneLabel1 -pattern singleValue -clearOverlays False
ixNet setAttr $useUpOrDownStreamAssigneLabel1/singleValue -value True
ixNet commit

puts "Assigning value for Up/DownStream Assigned Label for Ingress Topology"
set upOrDownStreamAssignedLabel1 [ixNet getAttr $mVRF1 -upOrDownStreamAssignedLabel]
ixNet setAttr $upOrDownStreamAssignedLabel1 -pattern counter -clearOverlays False
ixNet setMultiAttr $upOrDownStreamAssignedLabel1/counter\
        -direction  increment       \
        -step       {1}       \
        -start      {10001}
ixNet commit

puts "Configuring Root Address in Topology 2"
set rtAdd2 [ixNet getAttribute $mVRF2 -rootAddress]
ixNet setMultiAttribute $rtAdd2/singleValue -value 7.7.7.7
ixNet commit

puts "Enabling CheckBox for use of Up/DownStream Assigned Label for Egress Topology"
set useUpOrDownStreamAssigneLabel2 [ixNet getAttr $mVRF2 -useUpOrDownStreamAssigneLabel]
ixNet setAttr $useUpOrDownStreamAssigneLabel2 -pattern singleValue -clearOverlays False
ixNet setAttr $useUpOrDownStreamAssigneLabel2/singleValue -value True
ixNet commit

puts "Assigning value for Up/DownStream Assigned Label for Egress Topology"
set upOrDownStreamAssignedLabel2 [ixNet getAttr $mVRF2 -upOrDownStreamAssignedLabel]
ixNet setAttr $upOrDownStreamAssignedLabel2 -pattern counter -clearOverlays False
ixNet setMultiAttr $upOrDownStreamAssignedLabel2/counter\
        -direction  increment       \
        -step       {1}       \
        -start      {3116}
ixNet commit

puts "Configuring Opaque TLV Type for I-PMSI in Sender mVRF"
set opaque_type1 [ixNet getAttr $mVRF1/pnTLVList:1 -type]
ixNet setAttr $opaque_type1/singleValue -value "111"
ixNet commit

puts "Configuring Opaque TLV Length for I-PMSI in Sender mVRF"
set opaque_len1 [ixNet getAttr $mVRF1/pnTLVList:1 -tlvLength]
ixNet setAttr $opaque_len1/singleValue -value "33"
ixNet commit

puts "Configuring Opaque TLV Value for I-PMSI in Sender mVRF"
set opaque_val1 [ixNet getAttribute $mVRF1/pnTLVList:1 -value]
ixNet setMultiAttr $opaque_val1/counter\
        -direction  increment       \
        -step       {04}       \
        -start      {000000000000000000000000000000000000000000000000000000000000007651}
ixNet commit

puts "Configuring Opaque TLV Increment for I-PMSI in Sender mVRF"
set opaque_inc1 [ixNet getAttr $mVRF1/pnTLVList:1 -increment]
ixNet setAttr $opaque_inc1/singleValue -value "000000000000000000000000000000000000000000000000000000000000000001"
ixNet commit

puts "Configuring Opaque TLV Type for I-PMSI in Receiver mVRF"
set opaque_type2 [ixNet getAttr $mVRF2/pnTLVList:1 -type]
ixNet setAttr $opaque_type2/singleValue -value "123"
ixNet commit

puts "Configuring Opaque TLV Length for I-PMSI in Receiver mVRF"
set opaque_len2 [ixNet getAttr $mVRF2/pnTLVList:1 -tlvLength]
ixNet setAttr $opaque_len2/singleValue -value "5"
ixNet commit

puts "Configuring Opaque TLV Value for I-PMSI in Receiver mVRF"
set opaque_val2 [ixNet getAttribute $mVRF2/pnTLVList:1 -value]
ixNet setMultiAttr $opaque_val2/counter\
        -direction  increment       \
        -step       {04}       \
        -start      {00000000A1}
ixNet commit

puts "Configuring Opaque TLV Increment for I-PMSI in Receiver mVRF"
set opaque_inc2 [ixNet getAttr $mVRF1/pnTLVList:1 -increment]
ixNet setAttr $opaque_inc2/singleValue -value "0000000001"
ixNet commit

puts "Adding Network Group behind mVRF for Ingress Topology"
ixNet add $t1dev1 networkGroup
ixNet commit

set networkGroup1 [lindex [ixNet getList $t1dev1 networkGroup] 1]
ixNet setAttr $networkGroup1 -name  "IPv4 Sender Site-IPv6 Receiver Site"
ixNet commit

puts "Adding Network Group behind mVRF for Egress Topology"
ixNet add $t2dev1 networkGroup
ixNet commit

set networkGroup2 [lindex [ixNet getList $t2dev1 networkGroup] 1]
ixNet setAttr $networkGroup2 -name  "IPv4 Receiver Site-IPv6 Sender Site"
ixNet commit

puts "Adding IPv4/IPv6 Prefix pools in Ingress Topology"
ixNet add $networkGroup1 ipv4PrefixPools
ixNet commit

ixNet add $networkGroup1 ipv6PrefixPools
ixNet commit

puts "Adding IPv4/IPv6 Prefix pools in Egress Topology"
ixNet add $networkGroup2 ipv4PrefixPools
ixNet commit

ixNet add $networkGroup2 ipv6PrefixPools
ixNet commit

puts "Configuring the addresses in IPv4/IPv6 Prefix pools in IPv4 Sender Site-IPv6 Receiver Site"
set ipv4PrefixPools1 [lindex [ixNet getList $networkGroup1 ipv4PrefixPools] 0]
set ipv6PrefixPools1 [lindex [ixNet getList $networkGroup1 ipv6PrefixPools] 0]

puts "Changing Address for IPv4 Address Pool in Sender Site"
set nwAdd1 [ixNet getAttribute $ipv4PrefixPools1 -networkAddress]
ixNet setMultiAttr $nwAdd1/counter\
        -direction  increment       \
        -step       {0.1.0.0}       \
        -start      {200.1.0.1}
ixNet commit

puts "Changing Prefix Length for IPv4 Address Pool in Sender Site"
set mulValPrefLen1 [ixNet getAttr $ipv4PrefixPools1 -prefixLength]
ixNet setMultiAttr $mulValPrefLen1/singleValue -value "32"

puts "Changing Address Count for IPv4 Address Pool in Sender Site"
ixNet setAttr $ipv4PrefixPools1 -numberOfAddresses 3
ixNet commit

puts "Changing Address for IPv6 Address Pool in Sender Site"
set nwAdd2 [ixNet getAttribute $ipv6PrefixPools1 -networkAddress]
ixNet setMultiAttr $nwAdd2/counter\
        -direction  increment       \
        -step       {0:0:1:0:0:0:0:0}       \
        -start      {5001:1:0:0:0:0:0:1}
ixNet commit

puts "Changing Prefix Length for IPv6 Address Pool in Sender Site"
set mulValPrefLen2 [ixNet getAttr $ipv6PrefixPools1 -prefixLength]
ixNet setMultiAttr $mulValPrefLen2/singleValue -value "128"
ixNet commit

puts "Changing Address Count for IPv6 Address Pool in Sender Site"
ixNet setAttr $ipv6PrefixPools1 -numberOfAddresses 5
ixNet commit

puts "Changing label value for IPv4/IPv6 in IPv4 Sender Site-IPv6 Receiver Site"
set bgpL3VpnRouteProperty1 [lindex [ixNet getList $ipv4PrefixPools1 bgpL3VpnRouteProperty] 0]
set bgp6L3VpnRouteProperty1 [lindex [ixNet getList $ipv6PrefixPools1 bgpV6L3VpnRouteProperty] 0]

set label1 [ixNet getAttribute $bgpL3VpnRouteProperty1 -labelStart]
ixNet setMultiAttr $label1/counter\
        -direction  increment       \
        -step       {10}       \
        -start      {97710}
ixNet commit

set label2 [ixNet getAttribute $bgp6L3VpnRouteProperty1 -labelStart]
ixNet setMultiAttr $label2/counter\
        -direction  increment       \
        -step       {10}       \
        -start      {55410}
ixNet commit

puts "Disabling Receiver site and enabling Sender Site for IPv4 in Ingress Topology"
set bgpL3VpnRouteProperty1 [lindex [ixNet getList $ipv4PrefixPools1 bgpL3VpnRouteProperty] 0]
set bgp6L3VpnRouteProperty1 [lindex [ixNet getList $ipv6PrefixPools1 bgpV6L3VpnRouteProperty] 0]

ixNet setAttr $bgpL3VpnRouteProperty1 -enableIpv4Sender True
ixNet setAttr $bgpL3VpnRouteProperty1 -enableIpv4Receiver False
ixNet commit

puts "Disabling Sender site and enabling Receiver Site for IPv6 in Ingress Topology"
ixNet setAttr $bgp6L3VpnRouteProperty1 -enableIpv6Sender False
ixNet setAttr $bgp6L3VpnRouteProperty1 -enableIpv6Receiver True
ixNet commit

puts "Configuring the addresses in IPv4/IPv6 Prefix pools in IPv4 Receiver Site-IPv6 Sender Site"
set ipv4PrefixPools2 [lindex [ixNet getList $networkGroup2 ipv4PrefixPools] 0]
set ipv6PrefixPools2 [lindex [ixNet getList $networkGroup2 ipv6PrefixPools] 0]

puts "Changing Address for IPv4 Address Pool in Receiver Site"
set nwAdd3 [ixNet getAttribute $ipv4PrefixPools2 -networkAddress]
ixNet setMultiAttr $nwAdd3/counter\
        -direction  increment       \
        -step       {0.1.0.0}       \
        -start      {202.0.0.1}
ixNet commit

puts "Changing Prefix Length for IPv4 Address Pool in Receiver Site"
set mulValPrefLen3 [ixNet getAttr $ipv4PrefixPools2 -prefixLength]
ixNet setMultiAttr $mulValPrefLen3/singleValue -value "32"
ixNet commit

puts "Changing Address Count for IPv4 Address Pool in Receiver Site"
ixNet setAttr $ipv4PrefixPools1 -numberOfAddresses 3
ixNet commit

puts "Changing Address for IPv6 Address Pool in Receiver Site"
set nwAdd4 [ixNet getAttribute $ipv6PrefixPools2 -networkAddress]
ixNet setMultiAttr $nwAdd4/counter\
        -direction  increment       \
        -step       {0:0:1:0:0:0:0:0}       \
        -start      {3001:1:0:0:0:0:0:1}
ixNet commit

puts "Changing Prefix Length for IPv6 Address Pool in Receiver Site"
set mulValPrefLen4 [ixNet getAttr $ipv6PrefixPools2 -prefixLength]
ixNet setMultiAttr $mulValPrefLen4/singleValue -value "128"
ixNet commit

puts "Changing label value for IPv4/IPv6 in IPv4 Receiver Site-IPv6 Sender Site"
set bgpL3VpnRouteProperty2 [lindex [ixNet getList $ipv4PrefixPools2 bgpL3VpnRouteProperty] 0]
set bgp6L3VpnRouteProperty2 [lindex [ixNet getList $ipv6PrefixPools2 bgpV6L3VpnRouteProperty] 0]

set label11 [ixNet getAttribute $bgpL3VpnRouteProperty2 -labelStart]
ixNet setMultiAttr $label11/counter\
        -direction  increment       \
        -step       {10}       \
        -start      {87710}
ixNet commit

set label21 [ixNet getAttribute $bgp6L3VpnRouteProperty2 -labelStart]
ixNet setMultiAttr $label21/counter\
        -direction  increment       \
        -step       {10}       \
        -start      {2765}
ixNet commit

puts "Disabling Receiver site and enabling Sender Site for IPv6 in Egress Topology"
ixNet setAttr $bgp6L3VpnRouteProperty2 -enableIpv6Sender True
ixNet setAttr $bgp6L3VpnRouteProperty2 -enableIpv6Receiver False
ixNet commit

puts "Disabling Sender site and enabling Receiver Site for IPv4 in Egress Topology"
ixNet setAttr $bgpL3VpnRouteProperty2 -enableIpv4Sender False
ixNet setAttr $bgpL3VpnRouteProperty2 -enableIpv4Receiver True
ixNet commit

set bgpMVpnSenderSitesIpv4 [lindex [ixNet getList $ipv4PrefixPools1 bgpMVpnSenderSitesIpv4] 0]
set bgpMVpnSenderSitesIpv6 [lindex [ixNet getList $ipv6PrefixPools2 bgpMVpnSenderSitesIpv6] 0]
set bgpMVpnReceiverSitesIpv4 [lindex [ixNet getList $ipv4PrefixPools2 bgpMVpnReceiverSitesIpv4] 0]
set bgpMVpnReceiverSitesIpv6 [lindex [ixNet getList $ipv6PrefixPools1 bgpMVpnReceiverSitesIpv6] 0]

puts "Changing Group Address Count for IPv4 Cloud in Sender Site"
set mulValGCount [ixNet getAttr $bgpMVpnSenderSitesIpv4 -groupAddressCount]
ixNet setMultiAttr $mulValGCount -pattern singleValue -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValGCount/singleValue -value 4
ixNet commit

puts "Changing Source Address Count for IPv4 Cloud in Sender Site"
set mulValSCount [ixNet getAttr $bgpMVpnSenderSitesIpv4 -sourceAddressCount]
ixNet setMultiAttr $mulValSCount -pattern singleValue -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValSCount/singleValue -value 2
ixNet commit

puts "Changing Group Address for IPv4 Cloud in Sender Site"
set mulValGAdd [ixNet getAttr $bgpMVpnSenderSitesIpv4 -startGroupAddressIpv4]
ixNet setMultiAttr $mulValGAdd -pattern counter -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValGAdd/counter \
        -step "0.1.0.0" \
        -start "234.161.1.1" \
        -direction  increment
ixNet commit

puts "Changing Source Address for IPv4 Cloud in Sender Site"
set mulValSAdd [ixNet getAttr $bgpMVpnSenderSitesIpv4 -startSourceAddressIpv4]
ixNet setMultiAttr $mulValSAdd -pattern counter -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValSAdd/counter \
        -step "0.1.0.0" \
        -start "200.1.0.1" \
        -direction  increment
ixNet commit

puts "Changing Group Address Count for IPv4 Cloud in Receiver Site"
set mulValGCount [ixNet getAttr $bgpMVpnReceiverSitesIpv4 -groupAddressCount]
ixNet setMultiAttr $mulValGCount -pattern singleValue -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValGCount/singleValue -value 4
ixNet commit

puts "Changing Source Address Count for IPv4 Cloud in Receiver Site"
set mulValSCount [ixNet getAttr $bgpMVpnReceiverSitesIpv4 -sourceAddressCount]
ixNet setMultiAttr $mulValSCount -pattern singleValue -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValSCount/singleValue -value 2
ixNet commit

puts "Changing Group Address for IPv4 Cloud in Receiver Site"
set mulValGAdd [ixNet getAttr $bgpMVpnReceiverSitesIpv4 -startGroupAddressIpv4]
ixNet setMultiAttr $mulValGAdd -pattern counter -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValGAdd/counter \
        -step "0.1.0.0" \
        -start "234.161.1.1" \
        -direction  increment
ixNet commit

puts "Changing Source Address for IPv4 Cloud in Receiver Site"
set mulValSAdd [ixNet getAttr $bgpMVpnReceiverSitesIpv4 -startSourceOrCrpAddressIpv4]
ixNet setMultiAttr $mulValSAdd -pattern counter -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValSAdd/counter \
        -step "0.1.0.0" \
        -start "200.1.0.1" \
        -direction  increment
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

puts "Changing Source Group Mapping for IPv6 Cloud in Sender Site"
set mulValSGMap_1 [ixNet getAttr $bgpMVpnSenderSitesIpv6 -sourceGroupMapping]
ixNet setMultiAttr $mulValSGMap_1 -pattern singleValue -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValSGMap_1/singleValue -value onetoone
ixNet commit

puts "Changing Group Address for IPv6 Cloud in Sender Site"
set mulValGAdd_1 [ixNet getAttr $bgpMVpnSenderSitesIpv6 -startGroupAddressIpv6]
ixNet setMultiAttr $mulValGAdd_1 -pattern counter -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValGAdd_1/counter \
        -step "0:0:0:0:0:0:0:1" \
        -start "ff15:1:0:0:0:0:0:1" \
        -direction  increment
ixNet commit

puts "Changing Source Address for IPv6 Cloud in Sender Site"
set mulValSAdd [ixNet getAttr $bgpMVpnSenderSitesIpv6 -startSourceAddressIpv6]
ixNet setMultiAttr $mulValSAdd -pattern counter -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValSAdd/counter \
        -step "0:0:1:0:0:0:0:0" \
        -start "3000:1:1:1:0:0:0:0" \
        -direction  increment
ixNet commit

puts "Changing Group Address Count for IPv6 Cloud in Receiver Site"
set mulValGCount [ixNet getAttr $bgpMVpnReceiverSitesIpv6 -groupAddressCount]
ixNet setMultiAttr $mulValGCount -pattern singleValue -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValGCount/singleValue -value 5
ixNet commit

puts "Changing Source Group Mapping for IPv6 Cloud in Receiver Site"
set mulValSGMap_2 [ixNet getAttr $bgpMVpnReceiverSitesIpv6 -sourceGroupMapping]
ixNet setMultiAttr $mulValSGMap_2 -pattern singleValue -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValSGMap_2/singleValue -value onetoone
ixNet commit

puts "Changing Group Address for IPv6 Cloud in Receiver Site"
set mulValGAdd_2 [ixNet getAttr $bgpMVpnReceiverSitesIpv6 -startGroupAddressIpv6]
ixNet setMultiAttr $mulValGAdd_2 -pattern counter -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValGAdd_2/counter \
        -step "0:0:0:0:0:0:0:1" \
        -start "ff15:1:0:0:0:0:0:1" \
        -direction  increment
ixNet commit

puts "Changing Source Address for IPv6 Cloud in Sender Site"
set mulValSAdd_2 [ixNet getAttr $bgpMVpnReceiverSitesIpv6 -startSourceAddressIpv6]
ixNet setMultiAttr $mulValSAdd_2 -pattern counter -clearOverlays 0
ixNet commit
ixNet setMultiAttribute $mulValSAdd_2/counter \
        -step "0:0:1:0:0:0:0:0" \
        -start "3000:1:1:1:0:0:0:0" \
        -direction  increment
ixNet commit

puts "Changing Tunnel Type to mLDP for S-PMSI in IPv4 Address Pool in Sender Site"
set bgpMVpnSenderSiteSpmsiV4 [lindex [ixNet getList $bgpMVpnSenderSitesIpv4 bgpMVpnSenderSiteSpmsiV4] 0]
set mulValsPMSITunType [ixNet getAttr $bgpMVpnSenderSiteSpmsiV4 -multicastTunnelType]
ixNet setMultiAtt $mulValsPMSITunType/singleValue -value "tunneltypemldpp2mp"
ixNet commit

puts "Enabling Use Upstream/Downstream Assigned Label for S-PMSI in IPv4 Address Pool in Sender Sites"
set mulValUpAsLabEn [ixNet getAttr $bgpMVpnSenderSiteSpmsiV4 -useUpstreamOrDownstreamAssignedLabel]
ixNet setAttr $mulValUpAsLabEn -pattern singleValue -clearOverlays False
ixNet setAttr $mulValUpAsLabEn/singleValue -value True
ixNet commit

puts "Configuring the Upstream/Downstream Assigned Label for S-PMSI in IPv4 Address Pool in Sender Sites"
set mulValUpAsLabel [ixNet getAttr $bgpMVpnSenderSiteSpmsiV4 -upstreamOrDownstreamAssignedLabel]
ixNet setMultiAttr $mulValUpAsLabel/counter \
        -step "10" \
        -start "144" \
        -direction increment
ixNet commit

puts "Configuring Root Address for S-PMSI in IPv4 Address Pool in Sender Sites"
set mulValRootAdd [ixNet getAttribute $bgpMVpnSenderSiteSpmsiV4 -sPmsirootAddress]
ixNet setMultiAttribute $mulValRootAdd/counter \
        -step "0.0.0.1" \
        -start "8.8.8.7" \
        -direction increment
ixNet commit

puts "Changing Tunnel Count for S-PMSI in IPv4 Address Pool in Sender Site"
set mulValsPMSITunCnt [ixNet getAttr $bgpMVpnSenderSiteSpmsiV4 -sPmsiTunnelCount]
ixNet setAttr $mulValsPMSITunCnt -pattern singleValue -clearOverlays False
ixNet setAttr $mulValsPMSITunCnt/singleValue -value 3
ixNet commit

puts "Changing Type of TLV1 in S-PMSI mLDP Leaf range in IpV4 Sender Site"
set type_s1 [ixNet getAttr $bgpMVpnSenderSiteSpmsiV4/pnTLVList:1 -type]
ixNet setAttr $type_s1/singleValue -value "111"
ixNet commit

puts "Changing Length of TLV1 in S-PMSI mLDP Leaf range in IpV4 Sender Site"
set len_s1 [ixNet getAttr $bgpMVpnSenderSiteSpmsiV4/pnTLVList:1 -tlvLength]
ixNet setAttr $len_s1/singleValue -value "33"
ixNet commit

puts "Changing Value of TLV1 in S-PMSI mLDP Leaf range in IpV4 Sender Site"
set val_s1 [ixNet getAttribute $bgpMVpnSenderSiteSpmsiV4/pnTLVList:1 -value]
ixNet setMultiAttr $val_s1/counter\
        -direction  increment       \
        -step       {04}       \
        -start      {000000000000000000000000000000000000000000000000000000000000007653}
ixNet commit

puts "Changing Increment of TLV1 in S-PMSI mLDP Leaf range in IpV4 Sender Site"
set inc_s1 [ixNet getAttr $bgpMVpnSenderSiteSpmsiV4/pnTLVList:1 -increment]
ixNet setAttr $inc_s1/singleValue -value "000000000000000000000000000000000000000000000000000000000000000001"
ixNet commit

puts "Changing Tunnel Type to mLDP for S-PMSI in IPv6 Address Pool in Sender Site"
set bgpMVpnSenderSiteSpmsiV6 [lindex [ixNet getList $bgpMVpnSenderSitesIpv6 bgpMVpnSenderSiteSpmsiV6] 0]
set mulValsPMSIv6TunType [ixNet getAttr $bgpMVpnSenderSiteSpmsiV6 -multicastTunnelType]
ixNet setMultiAtt $mulValsPMSIv6TunType/singleValue -value "tunneltypemldpp2mp"
ixNet commit

puts "Enabling Use Upstream/Downstream Assigned Label for S-PMSI in IPv6 Address Pool in Sender Sites"
set mulValUpAsLabEn_S [ixNet getAttr $bgpMVpnSenderSiteSpmsiV6 -useUpstreamOrDownstreamAssignedLabel]
ixNet setAttr $mulValUpAsLabEn_S -pattern singleValue -clearOverlays False
ixNet setAttr $mulValUpAsLabEn_S/singleValue -value True
ixNet commit

puts "Configuring the Upstream/Downstream Assigned Label for S-PMSI in IPv6 Address Pool in Sender Sites"
set mulValUpAsLabel_S [ixNet getAttr $bgpMVpnSenderSiteSpmsiV6 -upstreamOrDownstreamAssignedLabel]
ixNet setMultiAttr $mulValUpAsLabel_S/counter \
        -step "10" \
        -start "14400" \
        -direction increment
ixNet commit

puts "Configuring Root Address for S-PMSI in IPv6 Address Pool in Sender Sites"
set mulValRootAddv6 [ixNet getAttribute $bgpMVpnSenderSiteSpmsiV6 -sPmsirootAddress]
ixNet setMultiAttribute $mulValRootAddv6/counter \
        -step "0.0.0.1" \
        -start "7.7.7.7" \
        -direction increment
ixNet commit

puts "Changing Tunnel Count for S-PMSI in IPv6 Address Pool in Sender Site"
set mulValsPMSITunCntv6 [ixNet getAttr $bgpMVpnSenderSiteSpmsiV6 -sPmsiTunnelCount]
ixNet setAttr $mulValsPMSITunCntv6 -pattern singleValue -clearOverlays False
ixNet setAttr $mulValsPMSITunCntv6/singleValue -value 3
ixNet commit

puts "Changing Type of TLV1 in S-PMSI mLDP Leaf range in IpV6 Sender Site"
set type_s2 [ixNet getAttr $bgpMVpnSenderSiteSpmsiV6/pnTLVList:1 -type]
ixNet setAttr $type_s2/singleValue -value "123"
ixNet commit

puts "Changing Length of TLV1 in S-PMSI mLDP Leaf range in IpV6 Sender Site"
set len_s2 [ixNet getAttr $bgpMVpnSenderSiteSpmsiV6/pnTLVList:1 -tlvLength]
ixNet setAttr $len_s2/singleValue -value "5"
ixNet commit

puts "Changing Value of TLV1 in S-PMSI mLDP Leaf range in IpV6 Sender Site"
set val_s2 [ixNet getAttribute $bgpMVpnSenderSiteSpmsiV6/pnTLVList:1 -value]
ixNet setMultiAttr $val_s2/singleValue\
        -value      {00000000A4}
ixNet commit

puts "Changing Increment of TLV1 in S-PMSI mLDP Leaf range in IpV6 Sender Site"
set inc_s2 [ixNet getAttr $bgpMVpnSenderSiteSpmsiV6/pnTLVList:1 -increment]
ixNet setAttr $inc_s2/singleValue -value "0000000001"
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
# 4. Retrieve IPv4/IPv6 mVPN learned info
###############################################################################

puts "Fetching IPv4 mVPN Learned Info at Receiver side PE Router"
ixNet exec getIpv4MvpnLearnedInfo $bgp2 1
after 5000
puts "IPv4 MVPN Learned Info at Receiver PE Router"
set learnedInfoList [ixNet getList $bgp2 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]

puts "IPv4 mVPN learned info"
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

puts "Fetching IPv6 mVPN Learned Info at Sender side PE Router"
ixNet exec getIpv6MvpnLearnedInfo $bgp1 1
after 5000
puts "IPv6 MVPN Learned Info at Sender PE Router"
set learnedInfoList [ixNet getList $bgp1 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]

puts "IPv6 mVPN learned info"
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
# 5. Apply changes on the fly.
################################################################################
puts "Changing Source Address Count for IPv6 Cloud in Receiver Site"
set mulValSCount [ixNet getAttr $bgpMVpnReceiverSitesIpv6 -sourceAddressCount]
ixNet setMultiAttr $mulValSCount/singleValue -value "4"
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
puts "Switching to S-PMSI for IPv4 Cloud from Sender Site"
ixNet exec switchToSpmsi $bgpMVpnSenderSitesIpv4 1
ixNet exec switchToSpmsi $bgpMVpnSenderSitesIpv4 2

###############################################################################
# 7. Retrieve protocol learned info after OTF
###############################################################################

puts "Fetching IPv4 mVPN Learned Info"
ixNet exec getIpv4MvpnLearnedInfo $bgp2 1
after 5000

puts "IPv6 MVPN Learned Info at Receiver PE Router"
set learnedInfoList [ixNet getList $bgp2 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]

puts "mVPN learned info at Receiver PE Router"
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
# 8. Configure L2-L3 IPv6 I-PMSI traffic.
################################################################################
puts "Configuring L2-L3 IPv6 I-PMSI Traffic Item"
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1  \
    -name {NGMVPN I-PMSI Traffic 1}    \
    -roundRobinPacketOrdering false    \
    -numVlansForMulticastReplication 1 \
    -trafficType ipv6 \
    -routeMesh fullMesh
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set destination  [list $bgpMVpnReceiverSitesIpv6]

ixNet setMultiAttribute $endpointSet1           \
        -name                  "EndpointSet-1"  \
        -multicastDestinations [list [list false none ff15:1:0:0:0:0:0:1 0:0:0:0:0:0:0:1 5]] \
	    -sources $bgpMVpnSenderSitesIpv6
ixNet commit

set endpointSet1 [lindex [ixNet remapIds $endpointSet1] 0]

ixNet setMultiAttribute $trafficItem1/tracking -trackBy \
    [list sourceDestEndpointPair0 mplsFlowDescriptor0 trackingenabled0 mplsMplsLabelValue0 ipv6DestIp0 ipv6SourceIp0]
ixNet commit	

################################################################################
# 9. Configure L2-L3 IPv4 S-PMSI traffic.
################################################################################
puts "Configuring L2-L3 IPv4 S-PMSI Traffic Item"
set trafficItem2 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem2  \
    -name {NGMVPN S-PMSI Traffic 2}    \
    -roundRobinPacketOrdering false    \
    -numVlansForMulticastReplication 1 \
    -trafficType ipv4 \

ixNet commit

set trafficItem2 [lindex [ixNet remapIds $trafficItem2] 0]
set endpointSet2 [ixNet add $trafficItem2 "endpointSet"]
set source       [list $bgpMVpnSenderSiteSpmsiV4]
set destination  [list $bgpMVpnReceiverSitesIpv4]
ixNet setMultiAttribute $endpointSet2           \
        -name                  "EndpointSet-1"  \
        -multicastDestinations [list [list false none 234.161.1.1 0.0.0.1 4] [list false none 234.162.1.1 0.0.0.1 4]] \
	    -sources $source
ixNet commit

set endpointSet2 [lindex [ixNet remapIds $endpointSet2] 0]

ixNet setMultiAttribute $trafficItem2/tracking -trackBy \
    [list sourceDestValuePair0 ipv4DestIp0 ipv4SourceIp0 trackingenabled0 mplsFlowDescriptor0]
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

