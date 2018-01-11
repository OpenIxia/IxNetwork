#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    03/12/2015 - Subhradip Pramanik - created sample                          #
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
#    This script intends to demonstrate how to use NGPF EVPN VXLAN API          #
#    About Topology:                                                            #
#        It will create 2 BGP EVPN-VXLAN topologies, each having OSPFv2         #
#    configured in connected Device Group .BGP EVPN VXLAN configured in chained # 
#    device group along with Mac pools connected behind the chained             # 
#    Device Group.                                                              #
#         Script Flow:                                                          #
#        Step 1. Configuration of protocols.                                    #
#    Configuration flow of the script is as follow:                             #
#             i.      Adding OSPF router.                                       #
#             ii.     Adding Network Topology(NT).                              #
#             iii.    Adding chain DG.                                          #
#             iv.     Adding BGP over loopback.                                 #
#             v.      Adding EVPN VXLAN over BGP                                #
#             vi.     Adding MAC Cloud with associated IPv4 Addresses           #
#        Step 2. Start of protocol                                              #
#        Step 3. Protocol Stat display                                          #
#        Step 4. Learned Info display                                           #
#        Step 5. On The Fly(OTF) change of protocol parameter.                  #
#        Step 6. Again Learned Info display to see OTF changes take place       #
#        Step 7. Configuration L2-L3 Traffic                                    #
#        Step 8. Apply and Start of L2-L3 traffic.                              #
#        Step 9. Diplay of L2-L3  traffic Stats.                                #
#        Step 10.Stop of L2-L3 traffic.                                         #
#        Step 11.Stop of all protocols.                                         #
#################################################################################
# Ixia Software Used to develop the script:                                     #
#    IxOS      8.00 EA                                                          #
#    IxNetwork 8.00 EA                                                          #
#                                                                               #
#################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.216.104.58
    set ixTclPort   8999
    set ports       {{10.216.108.82 2 15} { 10.216.108.82 2 16}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Disconnecting if any already connected"
ixNet disconnect $::ixia::ixTclServer

puts "Connect to IxNetwork Tcl server"
set version [ixNet getVersion]
scan [split $version "."] "%d %d" major minor
set version "$major.$minor"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version $version\
    setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

#################################################################################
# Step 1> protocol configuration section
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
# Creating topology and device group
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
ixNet setAttr $topo1  -name "EVPN_VXLAN Topology 1"
ixNet setAttr $topo2  -name "EVPN_VXLAN Topology 2"

set t1dev1 [lindex $t1devices 0]
set t2dev1 [lindex $t2devices 0]
ixNet setAttr $t1dev1 -name "Label Switch Router 1"
ixNet setAttr $t2dev1 -name "Label Switch Router 2"
ixNet commit
puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $t1dev1 -multiplier 1
ixNet setAttr $t2dev1 -multiplier 1
ixNet commit
#  Adding ethernet stack and configuring MAC
puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet commit

set mac1 [ixNet getList $t1dev1 ethernet]
set mac2 [ixNet getList $t2dev1 ethernet]

puts "Configuring the mac addresses"
ixNet setMultiAttr [ixNet getAttr $mac1 -mac]/counter\
        -direction  increment                        \
        -start      {22:01:01:01:01:01}              \
        -step       {00:00:00:00:00:01}

ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\
        -value      {44:01:01:01:01:01}
ixNet commit
#  Adding IPv4 stack and configuring  IP Address
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
ixNet setAttr $mvAdd1/singleValue -value "51.51.51.2"
ixNet setAttr $mvAdd2/singleValue -value "51.51.51.1"
ixNet setAttr $mvGw1/singleValue  -value "51.51.51.1"
ixNet setAttr $mvGw2/singleValue  -value "51.51.51.2"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 26
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 26

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit
#  Adding OSPF and configuring it
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

# Adding Network Topology behind Device Group
puts "Adding the Network Topology"
ixNet exec createDefaultStack $t1devices networkTopology
ixNet exec createDefaultStack $t2devices networkTopology

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

ixNet setAttr $networkGroup1 -name "Network Topology 1"
ixNet setAttr $networkGroup2 -name "Network Topology 2"
ixNet commit

set netTopo1 [ixNet getList $networkGroup1 networkTopology]
set netTopo2 [ixNet getList $networkGroup2 networkTopology]

puts "Adding Chained DG behind Network Topology in Topoloy 1"
set chainedDg1 [ixNet add $networkGroup1 deviceGroup]
ixNet commit
set chainedDg1 [lindex [ixNet remapIds $chainedDg1] 0]
ixNet setMultiAttribute $chainedDg1\
    -multiplier 1                  \
        -name {Edge Router 1}
ixNet commit
set loopback1 [ixNet add $chainedDg1 "ipv4Loopback"]
ixNet setMultiAttribute $loopback1\
    -stackedLayers [list]         \
    -name {IPv4 Loopback 2}
ixNet commit
puts "Adding Chained DG behind Network Topology in Topoloy 2"
set chainedDg2 [ixNet add $networkGroup2 deviceGroup]
ixNet setMultiAttribute $chainedDg2\
    -multiplier 1                  \
        -name {Edge Router 2}
ixNet commit
set chainedDg2 [lindex [ixNet remapIds $chainedDg2] 0]

set loopback2 [ixNet add $chainedDg2 "ipv4Loopback"]
ixNet setMultiAttribute $loopback2\
    -stackedLayers [list]         \
    -name {IPv4 Loopback 1}
ixNet commit

puts "Changing IP Address for IPv4 loopback in Chained DG"
set addressSet1 [ixNet getAttribute $loopback1 -address]
ixNet setMultiAttribute $addressSet1\
    -clearOverlays false            \
    -pattern counter
ixNet commit

set addressSet1 [ixNet add $addressSet1 "counter"]
ixNet setMultiAttribute $addressSet1\
    -step 0.0.0.1                   \
    -start 2.1.1.1                  \
    -direction increment
ixNet commit

set addressSet2 [ixNet getAttribute $loopback2 -address]
ixNet setMultiAttribute $addressSet2\
    -clearOverlays false            \
    -pattern counter
ixNet commit

set addressSet2 [ixNet add $addressSet2 "counter"]
ixNet setMultiAttribute $addressSet2\
    -step 0.0.0.1                   \
    -start 3.1.1.1                  \
    -direction increment
ixNet commit

puts "Creating  Connector in betwwen Network Toplogy and Chained DG for Topology1"
set connector1 [ixNet add $loopback1 "connector"]
ixNet setMultiAttribute $connector1\
    -connectedTo $networkGroup1/networkTopology/simRouter:1
ixNet commit
set connector1 [lindex [ixNet remapIds $connector1] 0]
puts "Creating  Connector in betwwen Network Toplogy and Chained DG for Topology1"
set connector2 [ixNet add $loopback2 "connector"]
ixNet setMultiAttribute $connector2\
    -connectedTo $networkGroup2/networkTopology/simRouter:1
ixNet commit
set connector1 [lindex [ixNet remapIds $connector2] 0]

puts "Adding BGPv4 over IP4 loopback in chained DG"
ixNet add $loopback1 bgpIpv4Peer
ixNet add $loopback2 bgpIpv4Peer
ixNet commit
set bgpIpv4Peer1 [ixNet getList $loopback1 bgpIpv4Peer]
set bgpIpv4Peer2 [ixNet getList $loopback2 bgpIpv4Peer]


puts "Setting DUT IP in BGPv4 Peer"
ixNet setAttr [ixNet getAttr $bgpIpv4Peer1 -dutIp]/singleValue\
        -value      {3.1.1.1}
ixNet commit

ixNet setMultiAttr [ixNet getAttr $bgpIpv4Peer2 -dutIp]/counter\
        -direction  increment       \
        -start      {2.1.1.1}       \
        -step       {0.0.0.1}
ixNet commit

puts "Enabling Learned Route Filters for EVPN VXLAN in BGP4 Peer"
ixNet setAttr [ixNet getAttr $bgpIpv4Peer1 -filterEvpn]/singleValue\
        -value      {1}
ixNet commit

ixNet setAttr [ixNet getAttr $bgpIpv4Peer2 -filterEvpn]/singleValue\
        -value      {1}
ixNet commit

puts "Configuring Router's MAC Addresses for EVPN VXLAN in BGP4 Peer"
ixNet setMultiAttr [ixNet getAttr $bgpIpv4Peer1 -routersMacOrIrbMacAddress]/counter\
        -direction  increment                        \
        -start      {aa:aa:aa:aa:aa:aa}              \
        -step       {00:00:00:00:00:01}
ixNet commit

ixNet setAttr [ixNet getAttr $bgpIpv4Peer2 -routersMacOrIrbMacAddress]/singleValue\
        -value      {cc:cc:cc:cc:cc:cc}
ixNet commit


puts "Changing Router Id of Network Topology to Loopback Address of Chained Device Group under Edge Router 1"
set simRouter1 [ixNet getList $netTopo1 simRouter]
set simRouterId1 [ixNet getAt $simRouter1 -routerId]

ixNet setMultiAttribute $simRouterId1        \
                        -clearOverlays false \
                        -pattern counter
ixNet commit
ixNet setMultiAttribute $simRouterId1/counter \
                        -step 0.0.0.1         \
                        -start 2.1.1.1        \
                        -direction increment
ixNet commit
set simRouterId1 [lindex [ixNet remapIds $simRouterId1] 0]
puts "Changing Router Id of Network Topology to Loopback Address of Chained Device Group under Edge Router 2"
set simRouter2 [ixNet getList $netTopo2 simRouter]
set simRouterId2 [ixNet getAt $simRouter2 -routerId]

ixNet setMultiAttribute $simRouterId2        \
                        -clearOverlays false \
                        -pattern counter
ixNet commit
ixNet setMultiAttribute $simRouterId2/counter \
                        -step 0.0.0.1         \
                        -start 3.1.1.1        \
                        -direction increment
ixNet commit
set simRouterId2 [lindex [ixNet remapIds $simRouterId2] 0]



puts "Adding EVPN VXLAN over BGPv4 in chained DG"
ixNet add $bgpIpv4Peer1 bgpIPv4EvpnVXLAN
ixNet add $bgpIpv4Peer2 bgpIPv4EvpnVXLAN
ixNet commit
set bgpIPv4EvpnVXLAN1 [ixNet getList $bgpIpv4Peer1 bgpIPv4EvpnVXLAN]
set bgpIPv4EvpnVXLAN2 [ixNet getList $bgpIpv4Peer2 bgpIPv4EvpnVXLAN]
set bgpIPv4EvpnVXLAN1 [lindex [ixNet remapIds $bgpIPv4EvpnVXLAN1] 0]
set bgpIPv4EvpnVXLAN2 [lindex [ixNet remapIds $bgpIPv4EvpnVXLAN2] 0]

puts "Changing Import Route Target AS No."
set bgpImportRouteTargetList1 [ixNet getList  $bgpIPv4EvpnVXLAN1 bgpImportRouteTargetList]
set bgpImportRouteTargetList2 [ixNet getList  $bgpIPv4EvpnVXLAN2 bgpImportRouteTargetList]
ixNet setMultiAttribute [ixNet getAttr $bgpImportRouteTargetList1 -targetAsNumber]/counter \
                        -step 0                            \
                        -start 200                         \
                        -direction increment
ixNet commit

ixNet setMultiAttribute [ixNet getAttr $bgpImportRouteTargetList2 -targetAsNumber]/counter \
                        -step 0                            \
                        -start 200                         \
                        -direction increment
ixNet commit


puts "Changing Export Route Target AS No."
set bgpExportRouteTargetList1 [ixNet getList  $bgpIPv4EvpnVXLAN1 bgpExportRouteTargetList]
set bgpExportRouteTargetList2 [ixNet getList  $bgpIPv4EvpnVXLAN2 bgpExportRouteTargetList]
ixNet setMultiAttribute [ixNet getAttr $bgpExportRouteTargetList1 -targetAsNumber]/counter \
                        -step 0                            \
                        -start 200                         \
                        -direction increment
ixNet commit

ixNet setMultiAttribute [ixNet getAttr $bgpExportRouteTargetList2 -targetAsNumber]/counter \
                        -step 0                            \
                        -start 200                         \
                        -direction increment
ixNet commit

puts "Adding Mac Pools behind EVPN VXLAN  DG"
ixNet exec createDefaultStack $chainedDg1 macPools
ixNet exec createDefaultStack $chainedDg2 macPools

set networkGroup3 [lindex [ixNet getList $chainedDg1 networkGroup] 0]
set networkGroup4 [lindex [ixNet getList $chainedDg2 networkGroup] 0]

ixNet setAttr $networkGroup3 -name "MAC_Pool_1"
ixNet setAttr $networkGroup4 -name "MAC_Pool_2"
ixNet setAttr $networkGroup3 -multiplier "1"
ixNet setAttr $networkGroup4 -multiplier "1"
set mac3 [ixNet getList $networkGroup3 macPools]
set mac4 [ixNet getList $networkGroup4 macPools]

puts "Configuring IPv4 Addresses associated with CMAC Addresses"
ixNet add $mac3 ipv4PrefixPools
ixNet add $mac4 ipv4PrefixPools
ixNet commit
set ipv4PrefixPools1 [ixNet getList $mac3 ipv4PrefixPools]
set ipv4PrefixPools2 [ixNet getList $mac4 ipv4PrefixPools]

puts "Configuring MAC Addresses in CMAC Ranges"

puts "Changing no. of CMAC Addresses"
ixNet setA $mac3 -numberOfAddresses 1
ixNet commit

ixNet setA $mac4 -numberOfAddresses 1
ixNet commit



puts "Changing MAC Addresses of CMAC Ranges"
ixNet setMultiAttr [ixNet getAttr $mac3 -mac]/counter\
        -direction  increment                        \
        -start      {66:66:66:66:66:66}              \
        -step       {00:00:00:00:00:01}
ixNet commit

ixNet setAttr [ixNet getAttr $mac4 -mac]/singleValue\
        -value      {88:88:88:88:88:88}
ixNet commit

puts "Enabling using of VLAN  in CMAC Ranges"
ixNet setAttr $mac3 -useVlans true
ixNet commit

ixNet setAttr $mac4 -useVlans true
ixNet commit

puts "Configuring CMAC Vlan properties"
set cMacvlan1 [ixNet getList $mac3 vlan]
set cMacvlan2 [ixNet getList $mac4 vlan]
puts "Configuring VLAN Ids"
ixNet setAttr [ixNet getAttr $cMacvlan1 -vlanId]/counter\
        -direction  increment                           \
        -start      {501}                               \
        -step       {1}
ixNet commit

ixNet setAttr [ixNet getAttr $cMacvlan2 -vlanId]/counter\
        -direction  increment                           \
        -start      {501}                               \
        -step       {1}
ixNet commit

puts "Configuring VLAN Priorities"
ixNet setAttr [ixNet getAttr $cMacvlan1 -priority]/singleValue\
        -value      {7}
ixNet commit

puts "Configuring VLAN Priorities"
ixNet setAttr [ixNet getAttr $cMacvlan2 -priority]/singleValue\
        -value      {7}
ixNet commit

puts "Changing VNI related Parameters under CMAC Properties"
set cMacProperties1 [ixNet getList $mac3 cMacProperties]
set cMacProperties2 [ixNet getList $mac4 cMacProperties]
puts "Changing 1st Label(L2VNI)"
ixNet setMultiAttribute [ixNet getAtt $cMacProperties1 -firstLabelStart]/counter \
                        -step 10                                                 \
                        -start 1001                                              \
                        -direction increment
ixNet commit

ixNet setMultiAttribute [ixNet getAtt $cMacProperties2 -firstLabelStart]/counter \
                        -step 10                                                 \
                        -start 1001                                              \
                        -direction increment
ixNet commit


puts "Changing 2nd Label(L3VNI)"
ixNet setMultiAttribute [ixNet getAtt $cMacProperties1 -secondLabelStart]/counter \
                        -step 10                                                  \
                        -start 2001                                               \
                        -direction increment
ixNet commit

ixNet setMultiAttribute [ixNet getAtt $cMacProperties2 -secondLabelStart]/counter \
                        -step 10                                                  \
                        -start 2001                                               \
                        -direction increment
ixNet commit

puts "Changing Increment Modes across all VNIs"
ixNet setAttr [ixNet getAtt $cMacProperties1 -labelMode]/singleValue -value "increment"
ixNet commit
ixNet setAttr [ixNet getAtt $cMacProperties2 -labelMode]/singleValue -value "increment"
ixNet commit

puts "Changing VNI step"
ixNet setMultiAttribute [ixNet getAtt $cMacProperties1 -labelStep]/counter \
                        -step 0                                            \
                        -start 1                                           \
                        -direction increment
ixNet commit                       
ixNet setMultiAttribute [ixNet getAtt $cMacProperties2 -labelStep]/counter \
                        -step 0                                            \
                        -start 1                                           \
                        -direction increment
ixNet commit

################################################################################
# 2. Start of protocol.
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000
################################################################################
# 3. Retrieve protocol statistics.
################################################################################
puts "Verifying all the stats\n"
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
puts "************************************************************"

###############################################################################
# 4. Retrieve protocol learned info
###############################################################################

puts "Fetching EVPN  Learned Info"
ixNet exec getEVPNLearnedInfo $bgpIpv4Peer1 

after 5000
set learnedInfoList [ixNet getList $bgpIpv4Peer1 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]
set EvpnMacLInfo [lindex $linfoList 0] 
set EvpnMulticastLInfo [lindex $linfoList 1] 
set EvpnESLInfo [lindex $linfoList 2] 
set EvpnEthernetADLInfo [lindex $linfoList 3] 

puts "EVPN learned info"
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
puts "Changing Host IP Address Value associated with CMAC in Topology 2"
ixNet setAttr [ixNet getAtt $ipv4PrefixPools2 -networkAddress]/singleValue -value "203.101.1.1"
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
        puts "$::errorInfo"
}
after 20000
###############################################################################
# 6. Retrieve protocol learned info to show On The Fly changes
###############################################################################

puts "Fetching EVPN  Learned Info"
ixNet exec getEVPNLearnedInfo $bgpIpv4Peer1 

after 5000
set learnedInfoList [ixNet getList $bgpIpv4Peer1 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]
set EvpnMacLInfo [lindex $linfoList 0] 

puts "EVPN learned info"
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
# 7. Configure L2-L3 traffic 
################################################################################
puts "Congfiguring L2-L3 Traffic Item"
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {Traffic Item 1}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv4
ixNet commit
after 5000
set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]

ixNet setMultiAttribute $endpointSet1\
    -name                  "EndpointSet-1"  \
    -multicastDestinations [list]           \
    -scalableSources       [list]           \
    -multicastReceivers    [list]           \
    -scalableDestinations  [list]           \
    -ngpfFilters           [list]           \
    -trafficGroups         [list]           \
    -sources               $ipv4PrefixPools1\
    -destinations          $ipv4PrefixPools2    
ixNet commit

ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy        [list mplsFlowDescriptor0 sourceDestEndpointPair0 ethernetIiWithoutFcsSourceaddress0 vxlanVni0 ipv4SourceIp1 ethernetIiWithoutFcsDestinationaddress0 ipv4DestIp1 trackingenabled0]\
    -fieldWidth     thirtyTwoBits                                                                                                                                                                     \
    -protocolOffset Root.0                                                                                                                                                                            \
    -values         [list]
ixNet commit
after 10000
###############################################################################
# 8. Apply and start L2/L3 traffic
###############################################################################
puts "Applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "Starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic
after 10000
###############################################################################
# 9. Retrieve L2/L3 traffic item statistics
###############################################################################
puts "Verifying all the L2-L3 traffic stats\n"
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
after 5000
puts "***************************************************"

################################################################################
# 10. Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 11. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
