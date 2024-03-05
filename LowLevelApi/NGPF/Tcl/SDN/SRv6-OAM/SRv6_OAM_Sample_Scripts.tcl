#/usr/bin/tclsh

################################################################################
#                                                                              #
#    Copyright 1997 - 2021 by Keysight                                         #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################

####################################################################################    
#                                                                                  #
#                                LEGAL  NOTICE:                                    #
#                                ==============                                    #
# The following code and documentation (hereinafter "the script") is an            #
# example script for demonstration purposes only.                                  #
# The script is not a standard commercial product offered by Keysight and have     #
# been developed and is being provided for use only as indicated herein. The       #
# script [and all modifications enhancements and updates thereto (whether          #
# made by Keysight and/or by the user and/or by a third party)] shall at all times #
# remain the property of Keysight.                                                 #
#                                                                                  #
# Keysight does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without              #
# omissions or error-free.                                                         #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND Keysight         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE                  #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR     #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                     #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE     #
# USER.                                                                            #
# IN NO EVENT SHALL Keysight BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF         #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR              #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR                  #
# CONSEQUENTIAL DAMAGES EVEN IF Keysight HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                         #
# Keysight will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the         #
# script or any part thereof. The user acknowledges that although Keysight may     #
# from time to time and in its sole discretion provide maintenance or support      #
# services for the script any such services are subject to the warranty and        #
# damages limitations set forth herein and will not obligate Keysight to provide   #
# any additional maintenance or support services.                                  #
#                                                                                  #
####################################################################################   

##########################################################################################################              
#                                                                                                        #
# Description:                                                                                           #
#    This script intends to demonstrate how to use SRv6 OAM (Ping/TraceRoute)in L3vpn Over SRv6 TCL APIs #
#                                                                                                        #
#    1. It will create 2 ISISL3 topologies, each having an ipv6 network                                  #
#       topology and loopback device group behind the network group(NG) with                             # 
#       loopback interface on it. L3vpn configure behind IPv6 Loopback.                                  #
#       IPv4 NG configured begind L3vpn DG.                           								     # 
#    2. Start the protocol.                                                                              #
#    3. Retrieve protocol statistics.                                                                    #
#    4. Send Ping Request to VPN SID.                                                                    #
#    5. Retrieve Ping Learned information.                                                               #
#    6. Send Ping Request to VPN SID.                                                                    #
#    7. Retrieve Traceroute Learned information.                                                         #
#    8. Stop all protocols.                                                                              #                                                                                          
##########################################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::Keysight {
    set ixTclServer 10.39.43.12
    set ixTclPort   8023
    set ports       {{10.39.50.200 1 5} {10.39.50.200 1 6}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::Keysight::ixTclServer -port $::Keysight::ixTclPort -version 8.50\
    �setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure ISISL3/BGP+ as per the description
#    give above
################################################################################ 
set Root [ixNet getRoot]
puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]
set vportRx [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $Keysight::ports {} $vPorts force

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

set t1dev1 [lindex $t1devices 0]
set t2dev1 [lindex $t2devices 0]

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
        -start      {00:11:01:00:00:01}              \
        -step       {00:00:00:00:00:01}

ixNet setMultiAttr [ixNet getAttr $mac2 -mac]/counter\
        -direction  increment                        \
        -start      {00:12:01:00:00:01}              \
        -step       {00:00:00:00:00:01}
ixNet commit

puts "Add ipv6"
ixNet add $mac1 ipv6
ixNet add $mac2 ipv6
ixNet commit

set ip1 [ixNet getList $mac1 ipv6]
set ip2 [ixNet getList $mac2 ipv6]

set mvAdd1 [ixNet getAttr $ip1 -address]
set mvAdd2 [ixNet getAttr $ip2 -address]
set mvGw1  [ixNet getAttr $ip1 -gatewayIp]
set mvGw2  [ixNet getAttr $ip2 -gatewayIp]

puts "configuring ipv6 addresses"
ixNet setAttr $mvAdd1/singleValue -value "2000:0:0:1:0:0:0:1"
ixNet setAttr $mvAdd2/singleValue -value "2000:0:0:1:0:0:0:2"
ixNet setAttr $mvGw1/singleValue  -value "2000:0:0:1:0:0:0:2"
ixNet setAttr $mvGw2/singleValue  -value "2000:0:0:1:0:0:0:1"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 64
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 64

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit
puts "Adding isisL3 over IPv6 stacks"
ixNet add $mac1 isisL3
ixNet add $mac2 isisL3
ixNet commit

set isisL3_1 [ixNet getList $mac1 isisL3]
set isisL3_2 [ixNet getList $mac2 isisL3]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "isisL3 Topology 1"
ixNet setAttr $topo2  -name "isisL3 Topology 2"

ixNet setAttr $t1dev1 -name "isisL3 Topology 1 Router"
ixNet setAttr $t2dev1 -name "isisL3 Topology 2 Router"
ixNet commit

#Change the property of ISIS-L3
puts "Change the Property of ISIS-L3"
set Network_Type_1 [ixNet getAttribute $isisL3_1 -networkType]
ixNet setMultiAttribute $Network_Type_1 -clearOverlays false
ixNet commit
set singleValue_1 [ixNet add $Network_Type_1 "singleValue"]
ixNet setMultiAttribute $singleValue_1 -value pointpoint
ixNet commit
set Network_Type_1 [ixNet getAttribute $isisL3_2 -networkType]
ixNet setMultiAttribute $Network_Type_1 -clearOverlays false
ixNet commit
set singleValue_1 [ixNet add $Network_Type_1 "singleValue"]
ixNet setMultiAttribute $singleValue_1 -value pointpoint
ixNet commit

#Change the value of -enableIPv6SID
puts "Change the value enableIPv6SID"
set enableIPv6SID_1 [ixNet getAttribute $isisL3_1 -enableIPv6SID]
ixNet setMultiAttribute $enableIPv6SID_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $enableIPv6SID_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set enableIPv6SID_1 [ixNet getAttribute $isisL3_2 -enableIPv6SID]
ixNet setMultiAttribute $enableIPv6SID_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $enableIPv6SID_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit


#Enable the ipv6Srh means Enable SR-IPv6
puts "Enabling the ipv6Srh means Enable SR-IPv6"
set ipv6Srh_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -ipv6Srh]
ixNet setMultiAttribute $ipv6Srh_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $ipv6Srh_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set ipv6Srh_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -ipv6Srh]
ixNet setMultiAttribute $ipv6Srh_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $ipv6Srh_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit

#Configure Locator in isisL3Router in topology 2 
puts "Configure Locator in isisL3Router in topology 2"
set locator_1 [ixNet getAttribute $t2dev1/isisL3Router:1/isisSRv6LocatorEntryList -locator]
ixNet setMultiAttribute $locator_1 \
	-clearOverlays false

ixNet commit
set counter [ixNet add $locator_1 "counter"]
ixNet setMultiAttribute $counter \
	-step 0:0:0:1:0:0:0:0 \
	-start 5001:0:0:1:0:0:0:0 \
	-direction increment
ixNet commit

#Configure End SID in isisL3Router in topology 2 
puts "Configure End SID in isisL3Router in topology 2"
set EndSid [ixNet getAttribute $t2dev1/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList -sid]
ixNet setMultiAttribute $EndSid \
	-clearOverlays false
ixNet commit

set counter [ixNet add $EndSid "counter"]
ixNet setMultiAttribute $counter \
	-step 0:0:0:0:1:0:0:0 \
	-start 5001:0:0:1:10:0:0:0 \
	-direction increment
ixNet commit
		
#Create Network Group At PEER1 Side
set IPv6_LoopBack [ixNet add $t1dev1 "networkGroup"]
ixNet setMultiAttribute $IPv6_LoopBack \
	-name "IPv6_LoopBack_Address"
ixNet commit
set IPv6_LoopBack [lindex [ixNet remapIds $IPv6_LoopBack] 0]
set ipv6PrefixPools [ixNet add $IPv6_LoopBack "ipv6PrefixPools"]
ixNet setMultiAttribute $ipv6PrefixPools \
	-addrStepSupported true \
	-name "Basic\ IPv6\ Addresses\ 1"
ixNet commit
set ipv6PrefixPools [lindex [ixNet remapIds $ipv6PrefixPools] 0]
set Connector [ixNet add $ipv6PrefixPools "connector"]
ixNet setMultiAttribute $Connector \
	-connectedTo $mac1
ixNet commit
set networkAddress [ixNet getAttribute $ipv6PrefixPools -networkAddress]
ixNet setMultiAttribute $networkAddress -clearOverlays false
ixNet commit
set counter_networkAddress [ixNet add $networkAddress "counter"]
ixNet setMultiAttribute $counter_networkAddress \
	-step ::0.0.0.1 \
	-start 1111::1 \
	-direction increment
ixNet commit

#Create Network Group At PEER2 Side
set networkGroup_P2 [ixNet add $t2dev1 "networkGroup"]
ixNet setMultiAttribute $networkGroup_P2 \
	-name "Routers"
ixNet commit
set networkGroup_P2 [lindex [ixNet remapIds $networkGroup_P2] 0]
set Network_Topology [ixNet add $networkGroup_P2 "networkTopology"]
ixNet commit
set Network_Topology [lindex [ixNet remapIds $Network_Topology] 0]
set netTopologyLinear [ixNet add $Network_Topology "netTopologyLinear"]
ixNet commit
set netTopologyLinear [lindex [ixNet remapIds $netTopologyLinear] 0]
ixNet setMultiAttribute $netTopologyLinear \
	-nodes 4
ixNet commit

#Enable the field of "Enable SR-IPv6"
set ipv6Srh [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1 -ipv6Srh]
ixNet setMultiAttribute $ipv6Srh -clearOverlays false
ixNet commit
set singleValue [ixNet add $ipv6Srh "singleValue"]
ixNet setMultiAttribute $singleValue -value true
ixNet commit
#Change the Network Address of ISIS Simulated IPv6 Node Routers of Simulated Bridge
set networkAddress [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1 -networkAddress]
ixNet setMultiAttribute $networkAddress -clearOverlays false
ixNet commit
set singleValue [ixNet add $networkAddress "singleValue"]
ixNet setMultiAttribute $singleValue -value 2222::1
ixNet commit
set singleValue [lindex [ixNet remapIds $singleValue] 0]
ixNet setMultiAttribute $networkAddress/nest:1 -enabled false \
	-step ::0.0.0.1
ixNet setMultiAttribute $networkAddress/nest:2 \
	-enabled false \
	-step ::0.0.0.1
ixNet commit
set active [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1 -active]
ixNet setMultiAttribute $active -clearOverlays false
ixNet commit
set singleValue [ixNet add $active "singleValue"]
ixNet setMultiAttribute $singleValue -value true
ixNet commit

#Configure locator in isisL3PseudoRouter in topology 2 
puts "Configure locator in isisL3PseudoRouter in topology 2"
set locator [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1/isisPseudoSRv6LocatorEntryList -locator]
ixNet setMultiAttribute $locator \
	-clearOverlays false

ixNet commit
set counter [ixNet add $locator "counter"]
ixNet setMultiAttribute $counter \
	-step 0:0:0:1:0:0:0:0 \
	-start 5001:0:0:2:0:0:0:0 \
	-direction increment
ixNet commit

#Configure End SID in isisL3PseudoRouter in topology 2 
puts "Configure End SID in isisL3PseudoRouter in topology 2"		
set sid [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1/isisPseudoSRv6LocatorEntryList/isisPseudoSRv6EndSIDList -sid]
ixNet setMultiAttribute $sid \
	-clearOverlays false

ixNet commit
set counter [ixNet add $sid "counter"]
ixNet setMultiAttribute $counter \
	-step 0:0:0:1:0:0:0:0 \
	-start 5001:0:0:2:10:0:0:0 \
	-direction increment
ixNet commit
		
#Add Device Group Behind IPv6 Network Group
set deviceGroup_bgp [ixNet add $IPv6_LoopBack "deviceGroup"]
ixNet setMultiAttribute $deviceGroup_bgp \
	-multiplier 1 \
	-name "BGP_L3vpn_1"
ixNet commit
set deviceGroup_bgp [lindex [ixNet remapIds $deviceGroup_bgp] 0]
set enable [ixNet getAttribute $deviceGroup_bgp -enabled]
ixNet setMultiAttribute $enable \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $enable "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set singleValue [lindex [ixNet remapIds $singleValue] 0]

set ipv6Loopback [ixNet add $deviceGroup_bgp "ipv6Loopback"]
ixNet setMultiAttribute $ipv6Loopback \
	-stackedLayers [list ] \
	-name "IPv6\ Loopback\ 2"
ixNet commit
set ipv6Loopback [lindex [ixNet remapIds $ipv6Loopback] 0]

set Connector [ixNet add $ipv6Loopback "connector"]
ixNet setMultiAttribute $Connector \
	-connectedTo $ipv6PrefixPools
ixNet commit
set Connector [lindex [ixNet remapIds $Connector] 0]
set prefix [ixNet getAttribute $ipv6Loopback -prefix]
ixNet setMultiAttribute $prefix \
	-clearOverlays false
ixNet commit
set Single_Value [ixNet add $prefix "singleValue"]
ixNet setMultiAttribute $Single_Value \
	-value 128
ixNet commit        
set address [ixNet getAttribute $ipv6Loopback -address]
ixNet setMultiAttribute $address \
	-clearOverlays false
ixNet commit
set Counter [ixNet add $address "counter"]
ixNet setMultiAttribute $Counter \
	-step ::0.0.0.1 \
	-start 1111::1 \
	-direction increment
ixNet commit

set bgpIpv6Peer_1 [ixNet add $ipv6Loopback "bgpIpv6Peer"]
ixNet setMultiAttribute $bgpIpv6Peer_1 \
	-enSRv6DataPlane true \
	-stackedLayers [list ] \
	-name "BGP+\ Peer\ 2"
ixNet commit

set dutIp [ixNet getAttribute $bgpIpv6Peer_1 -dutIp]
ixNet setMultiAttribute $dutIp \
	-clearOverlays false
ixNet commit
set counter [ixNet add $dutIp "counter"]
ixNet setMultiAttribute $counter \
	-step ::0.0.0.1 \
	-start 2222::1 \
	-direction increment
ixNet commit
set counter [lindex [ixNet remapIds $counter] 0]
set filterIpV4MplsVpn [ixNet getAttribute $bgpIpv6Peer_1 -filterIpV4MplsVpn]
ixNet setMultiAttribute $filterIpV4MplsVpn -clearOverlays false
ixNet commit

set capabilityNHEncodingCapabilities [ixNet getAttribute $bgpIpv6Peer_1 -capabilityNHEncodingCapabilities]
ixNet setMultiAttribute $capabilityNHEncodingCapabilities -clearOverlays false
ixNet commit
set singleValue [ixNet add $capabilityNHEncodingCapabilities "singleValue"]
ixNet setMultiAttribute $singleValue -value true
ixNet commit

#Adding BGPVRF on top of BGP+
set bgpV6Vrf_1 [ixNet add $bgpIpv6Peer_1 "bgpV6Vrf"]
ixNet setMultiAttribute $bgpV6Vrf_1 \
	-multiplier 4 \
	-stackedLayers [list ] \
	-name "BGP+\ VRF\ 2"
ixNet commit
set bgpV6Vrf_1 [lindex [ixNet remapIds $bgpV6Vrf_1] 0]
set targetAsNumber [ixNet getAttribute $bgpV6Vrf_1/bgpExportRouteTargetList:1 -targetAsNumber]
ixNet setMultiAttribute $targetAsNumber \
	-clearOverlays false
ixNet commit
set counter [ixNet add $targetAsNumber "counter"]
ixNet setMultiAttribute $counter \
	-step 1 \
	-start 100 \
	-direction increment
ixNet commit
#Adding Network Group Behind BGP+
set networkGroup [ixNet add $deviceGroup_bgp "networkGroup"]
ixNet setMultiAttribute $networkGroup \
	-name "IPv4_VPN_Route"
ixNet commit
set networkGroup [lindex [ixNet remapIds $networkGroup] 0]
set networkGroup_1 [ixNet getAttribute $networkGroup -enabled]
ixNet setMultiAttribute $networkGroup_1 \
	-clearOverlays false
ixNet commit
set networkGroup_1 [ixNet add $networkGroup_1 "singleValue"]
ixNet setMultiAttribute $networkGroup_1 \
	-value true
ixNet commit
set networkGroup_1 [lindex [ixNet remapIds $networkGroup_1] 0]
set ipv4PrefixPools [ixNet add $networkGroup "ipv4PrefixPools"]
ixNet setMultiAttribute $ipv4PrefixPools \
	-addrStepSupported true \
	-name "Basic\ IPv4\ Addresses\ 2"
ixNet commit
set ipv4PrefixPools [lindex [ixNet remapIds $ipv4PrefixPools] 0]
set connector [ixNet add $ipv4PrefixPools "connector"]
ixNet setMultiAttribute $connector \
	-connectedTo $bgpV6Vrf_1
ixNet commit
set networkAddress [ixNet getAttribute $ipv4PrefixPools -networkAddress]
ixNet setMultiAttribute $networkAddress \
	-clearOverlays false

ixNet commit
set counter [ixNet add $networkAddress "counter"]
ixNet setMultiAttribute $counter \
	-step 0.1.0.0 \
	-start 1.1.1.1 \
	-direction increment
ixNet commit
set bgpV6L3VpnRouteProperty [lindex [ixNet getList $ipv4PrefixPools bgpV6L3VpnRouteProperty] 0]
set labelStep [ixNet getAttribute $bgpV6L3VpnRouteProperty -labelStep]
ixNet setMultiAttribute $labelStep \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $labelStep "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value 1
ixNet commit
set enableSrv6Sid [ixNet getAttribute $bgpV6L3VpnRouteProperty -enableSrv6Sid]
ixNet setMultiAttribute $enableSrv6Sid \
	-clearOverlays false

ixNet commit
set singleValue [ixNet add $enableSrv6Sid "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set srv6SidLoc [ixNet getAttribute $bgpV6L3VpnRouteProperty -srv6SidLoc]
ixNet setMultiAttribute $srv6SidLoc -clearOverlays false
ixNet commit
set counter [ixNet add $srv6SidLoc "counter"]
ixNet setMultiAttribute $counter \
	-step ::1 \
	-start 5000:0:0:1::d100 \
	-direction increment
ixNet commit
#Configure BGP/BGP-vrf at PEER2 side
set deviceGroup_P2 [ixNet add $networkGroup_P2 "deviceGroup"]
ixNet setMultiAttribute $deviceGroup_P2 \
	-multiplier 1 \
	-name "BGP_L3vpn_2"
ixNet commit
set deviceGroup_P2 [lindex [ixNet remapIds $deviceGroup_P2] 0]
set ipv6Loopback_P2 [ixNet add $deviceGroup_P2 "ipv6Loopback"]
ixNet setMultiAttribute $ipv6Loopback_P2 \
	-stackedLayers [list ] \
	-name "IPv6\ Loopback\ 1"
ixNet commit
set ipv6Loopback_P2 [lindex [ixNet remapIds $ipv6Loopback_P2] 0]
set connector [ixNet add $ipv6Loopback_P2 "connector"]
ixNet commit
set address [ixNet getAttribute $ipv6Loopback_P2 -address]
ixNet setMultiAttribute $address \
	-clearOverlays false

ixNet commit
set counter [ixNet add $address "counter"]
ixNet setMultiAttribute $counter \
	-step ::0.0.0.1 \
	-start 2222::1 \
	-direction increment
ixNet commit
set bgpIpv6Peer_p2 [ixNet add $ipv6Loopback_P2 "bgpIpv6Peer"]
ixNet setMultiAttribute $bgpIpv6Peer_p2 \
	-stackedLayers [list ] \
	-name "BGP+\ Peer\ 1"
ixNet commit
set bgpIpv6Peer_p2 [lindex [ixNet remapIds $bgpIpv6Peer_p2] 0]
set dutIp [ixNet getAttribute $bgpIpv6Peer_p2 -dutIp]
ixNet setMultiAttribute $dutIp \
	-clearOverlays false
ixNet commit

set counter [ixNet add $dutIp "counter"]
ixNet setMultiAttribute $counter \
	-step ::0.0.0.1 \
	-start 1111::1 \
	-direction increment
ixNet commit

set filterIpV4MplsVpn_2 [ixNet getAttribute $bgpIpv6Peer_p2 -filterIpV4MplsVpn]
ixNet setMultiAttribute $filterIpV4MplsVpn_2 -clearOverlays false
ixNet commit
set singleValue [ixNet add $filterIpV4MplsVpn_2 "singleValue"]
ixNet setMultiAttribute $singleValue -value true
ixNet commit

set capabilityNHEncodingCapabilities_2 [ixNet getAttribute $bgpIpv6Peer_p2 -capabilityNHEncodingCapabilities]
ixNet setMultiAttribute $capabilityNHEncodingCapabilities_2 -clearOverlays false
ixNet commit
set singleValue [ixNet add $capabilityNHEncodingCapabilities_2 "singleValue"]
ixNet setMultiAttribute $singleValue -value true
ixNet commit
#Adding BGPVRF on top of BGP+ @Peer2 side
set bgpV6Vrf_2 [ixNet add $bgpIpv6Peer_p2 "bgpV6Vrf"]
ixNet setMultiAttribute $bgpV6Vrf_2 \
	-multiplier 4 \
	-stackedLayers [list ] \
	-name "BGP+\ VRF\ 2"
ixNet commit
set bgpV6Vrf_2 [lindex [ixNet remapIds $bgpV6Vrf_2] 0]
set targetAsNumber [ixNet getAttribute $bgpV6Vrf_2/bgpExportRouteTargetList:1 -targetAsNumber]
ixNet setMultiAttribute $targetAsNumber \
	-clearOverlays false
ixNet commit
set counter [ixNet add $targetAsNumber "counter"]
ixNet setMultiAttribute $counter \
	-step 1 \
	-start 100 \
	-direction increment
ixNet commit
#Adding Network Group Behind BGP+ AT PEER2 Side
set networkGroup_P2 [ixNet add $deviceGroup_P2 "networkGroup"]
ixNet setMultiAttribute $networkGroup_P2 \
	-name "IPv4_VPN_Route_2"
ixNet commit
set networkGroup_P2 [lindex [ixNet remapIds $networkGroup_P2] 0]
set networkGroup_2 [ixNet getAttribute $networkGroup_P2 -enabled]
ixNet setMultiAttribute $networkGroup_2 \
	-clearOverlays false
ixNet commit
set networkGroup_2 [ixNet add $networkGroup_2 "singleValue"]
ixNet setMultiAttribute $networkGroup_2 \
ixNet setMultiAttribute $networkGroup_2 \
	-value true
ixNet commit
set networkGroup_1 [lindex [ixNet remapIds $networkGroup_2] 0]
set ipv4PrefixPools_P2 [ixNet add $networkGroup_P2 "ipv4PrefixPools"]
ixNet setMultiAttribute $ipv4PrefixPools_P2 \
	-addrStepSupported true \
	-name "Basic\ IPv4\ Addresses\ 2"
ixNet commit
set ipv4PrefixPools_P2 [lindex [ixNet remapIds $ipv4PrefixPools_P2] 0]
set connector_P2 [ixNet add $ipv4PrefixPools_P2 "connector"]
ixNet setMultiAttribute $connector_P2 \
	-connectedTo $bgpV6Vrf_2
ixNet commit
set networkAddress_P2 [ixNet getAttribute $ipv4PrefixPools_P2 -networkAddress]
ixNet setMultiAttribute $networkAddress_P2 \
	-clearOverlays false
ixNet commit
set counter [ixNet add $networkAddress_P2 "counter"]
ixNet setMultiAttribute $counter \
	-step 0.1.0.0 \
	-start 2.2.2.2 \
	-direction increment
ixNet commit
set bgpV6L3VpnRouteProperty_P2 [lindex [ixNet getList $ipv4PrefixPools_P2 bgpV6L3VpnRouteProperty] 0]
set labelStep [ixNet getAttribute $bgpV6L3VpnRouteProperty_P2 -labelStep]
ixNet setMultiAttribute $labelStep \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $labelStep "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value 1
ixNet commit
set enableSrv6Sid [ixNet getAttribute $bgpV6L3VpnRouteProperty_P2 -enableSrv6Sid]
ixNet setMultiAttribute $enableSrv6Sid \
	-clearOverlays false

ixNet commit
set singleValue [ixNet add $enableSrv6Sid "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set srv6SidLoc [ixNet getAttribute $bgpV6L3VpnRouteProperty_P2 -srv6SidLoc]
ixNet setMultiAttribute $srv6SidLoc -clearOverlays false
ixNet commit
set counter [ixNet add $srv6SidLoc "counter"]
ixNet setMultiAttribute $counter \
	-step ::1 \
	-start 5001:0:0:5::d100 \
	-direction increment
ixNet commit

puts "\nSRv6 OAM Related Configuration begins here !!!"
#Enable srv6OAMService in ISIS-L3 Router present in Topology 1 and Topology 2
puts "Enable srv6OAMService in ISIS-L3 Router present in Topology 1 and Topology 2"

#Change the value of -srv6OAMService
puts "Change the value srv6OAMService"
set srv6OAMService_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -srv6OAMService]
ixNet setMultiAttribute $srv6OAMService_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $srv6OAMService_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit

set srv6OAMService_2 [ixNet getAttribute $t2dev1/isisL3Router:1 -srv6OAMService]
ixNet setMultiAttribute $srv6OAMService_2 -clearOverlays false
ixNet commit
set single_value_2 [ixNet add $srv6OAMService_2 "singleValue"]
ixNet setMultiAttribute $single_value_2 -value true
ixNet commit

#Enable srv6OAMService in isisL3PseudoRouter in Topology 2
puts "Enable srv6OAMService in isisL3PseudoRouter in Topology 2"
set srv6OAMService [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1 -srv6OAMService]
ixNet setMultiAttribute $srv6OAMService -clearOverlays false
ixNet commit

set singleValue [ixNet add $srv6OAMService "singleValue"]
ixNet setMultiAttribute $singleValue -value true
ixNet commit

#Enable srv6OAMService in BGP+ Peer in Topology 1 and Topology 2
puts "Enable srv6OAMService in BGP+ Peer in Topology 1 and Topology 2"
ixNet setMultiAttribute $bgpIpv6Peer_1 -enableSRv6OAMService true
ixNet commit

ixNet setAttribute $bgpIpv6Peer_p2 -enableSRv6OAMService true 
ixNet commit

puts "Adding srv6Oam over IPv6 stacks"
ixNet add $ip1 srv6Oam
ixNet add $ip2 srv6Oam
ixNet commit

set srv6Oam1 [ixNet getList $ip1 srv6Oam]
set srv6Oam2 [ixNet getList $ip2 srv6Oam]

#Configure the value of numPingTraceRouteDest
puts "Configure the value numPingTraceRouteDest"
ixNet setAttribute $srv6Oam1 -numPingTraceRouteDest 1
ixNet commit

#Configure the value for field tracerouteDstPort (destination Port to be used traceroute operation)
puts "Configure the value for field tracerouteDstPort (destination Port to be used traceroute operation)"
ixNet setAttribute $srv6Oam1 -tracerouteDstPort 33435
ixNet setAttribute $srv6Oam2 -tracerouteDstPort 33435
ixNet commit

#Configure the value for field locatorBlkLen (Useful while processing compressed sid in srh)
puts "Configure the value for field locatorBlkLen (Useful while processing compressed sid in srh)"
set locatorBlkLen [ixNet getAttribute $srv6Oam2 -locatorBlkLen]
set singleValue [ixNet add $locatorBlkLen "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value 48bit
ixNet commit


set srv6OamDestination [ixNet getList $srv6Oam1 srv6OamDestination]
#Configure the value for field srv6DestAddress (Destination address)
puts "Configure the value for field srv6DestAddress (Destination address)"
set srv6DestAddress [ixNet getAttribute $srv6OamDestination -srv6DestAddress]
set singleValue [ixNet add $srv6DestAddress "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value 5001:0:0:5:0:0:0:d100
ixNet commit


set srv6DstName [ixNet getAttribute $srv6OamDestination -srv6DstName]
ixNet setMultiAttribute $srv6DstName \
	-clearOverlays false

ixNet commit
set string [ixNet add $srv6DstName "string"]
ixNet setMultiAttribute $string \
	-pattern "VPN SID DA-\{Inc:1,1\}"
ixNet commit

#Configure the value for field numSegments (Number of segments)
puts "Configure the value for field numSegments (Number of segments)"
ixNet setAttribute $srv6OamDestination -numSegments 5
ixNet commit

#Configure the value for field srv6DestAddress (Destination address)
puts "Configure the value for field srv6DestAddress (Destination address)"
set srv6DestAddress [ixNet getAttribute $srv6OamDestination -srv6DestAddress]
set singleValue [ixNet add $srv6DestAddress "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value 5001:0:0:5:0:0:0:d100
ixNet commit

#Configure the value for field txCfgSrcAddrFlag (Enable Configure source address)
puts "Configure the value for field txCfgSrcAddrFlag (Destination address)"
set txCfgSrcAddrFlag [ixNet getAttribute $srv6OamDestination -txCfgSrcAddrFlag]
set singleValue [ixNet add $txCfgSrcAddrFlag "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit

#Configure the value for field txSrcAddr (source address to be used for ping/Traceroute request)
puts "Configure the value for field txSrcAddr (Destination address)"
set txSrcAddr [ixNet getAttribute $srv6OamDestination -txSrcAddr]
set singleValue [ixNet add $txSrcAddr "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value 1111:0:0:0:0:0:0:1
ixNet commit

#Configure the value for field payloadLen
puts "Configure the value for field payloadLen"
set payloadLen [ixNet getAttribute $srv6OamDestination -payloadLen]
set singleValue [ixNet add $payloadLen "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value 32
ixNet commit

#Configure the value for field maxTtlForTR (TTl for Traceroute)
puts "Configure the value for field maxTtlForTR (TTl for Traceroute)"
set maxTtlForTR [ixNet getAttribute $srv6OamDestination -maxTtlForTR]
set singleValue [ixNet add $maxTtlForTR "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value 60
ixNet commit

#Configure the value for field ttl (TTL for Ping)
puts "Configure the value for field ttl (TTL for Ping)"
set ttl [ixNet getAttribute $srv6OamDestination -ttl]
set singleValue [ixNet add $ttl "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value 250
ixNet commit

#Configure the value for field oFlag 
puts "Configure the value for field oFlag"
set oFlag [ixNet getAttribute $srv6OamDestination -oFlag]
set singleValue [ixNet add $oFlag "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit


set srv6oamSegmentNode [ixNet getList $srv6OamDestination  srv6oamSegmentNode]
#Configure the value for field segmentAddress 
puts "Configure the value for field segmentAddress"
set segmentAddress [ixNet getAttribute $srv6oamSegmentNode -segmentAddress]
set counter [ixNet add $segmentAddress "counter"]
ixNet setMultiAttribute $counter \
	-step 0:0:0:1:0:0:0:0 \
	-start 5001:0:0:1:10:0:0:0 \
	-direction increment
ixNet commit

#Configure the value for field gSIDEnableFlag 
puts "Configure the value for field gSIDEnableFlag"
set gSIDEnableFlag [ixNet getAttribute $srv6oamSegmentNode -gSIDEnableFlag]
set singleValue [ixNet add $gSIDEnableFlag "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit

#Configure the value for field locatorBlkLen 
puts "Configure the value for field locatorBlkLen"
set locatorBlkLen [ixNet getAttribute $srv6oamSegmentNode -locatorBlkLen]
set singleValue [ixNet add $locatorBlkLen "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value 48
ixNet commit



################################################################################
# 2. Start ISISl3/BGP+ protocol and wait for 60 seconds
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
puts "Fetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Protocols Summary"/page}
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
# Step 4> Trigger Ping Request
###############################################################################
puts "Sending Ping Request for VPN SID"
ixNet exec sendPingRequest $srv6OamDestination 1
after 30000
###############################################################################
# Step 5> Retrieve Ping learned info
###############################################################################

set linfo [ixNet getList $srv6Oam1 learnedInfo]
set values [ixNet getAttribute $linfo -values]
puts "Ping learned info"
puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"


###############################################################################
# Step 6> clear learned info
###############################################################################
ixNet exec clearAllLearnedInfo $srv6OamDestination 1

###############################################################################
# Step 7> Trigger TraceRoute Request
###############################################################################
puts "Sending TraceRoute Request for VPN SID"
ixNet exec sendTraceRouteRequest $srv6OamDestination 1
after 60000
###############################################################################
# Step 8> Retrieve TraceRoute learned info
###############################################################################

set linfo [ixNet getList $srv6Oam1 learnedInfo]
set values [ixNet getAttribute $linfo -values]
puts "TraceRoute learned info"
puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"



#################################################################################
## 9. Stop all protocols
#################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
