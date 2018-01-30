#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    01/12/2015 - Poulomi Chatterjee - created sample                          #
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

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF BGP PBB EVPN API.      #
#                                                                              #
#    1. It will create 2 BGP PBB EVPN topologies, each having LDP configured in#
#        connected Device Group .BGP EVPN configured in chained device group   #
#        along with Mac pools connected behind the chained Device Group.       # 
#    2. Start all protocol.                                                    #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Configure L2-L3 traffic.                                               #
#    6. Start the L2-L3 traffic.                                               #
#    7. Retrieve L2-L3 traffic stats.                                          #
#    8. Stop L2-L3 traffic.                                                    #
#    9. Stopallprotocols.                                                      #                                                                                
# Ixia Software:                                                               #
#    IxOS      8.00 EA                                                         #
#    IxNetwork 8.00 EA                                                         #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.216.104.58
    set ixTclPort   8350
    set ports       {{10.216.108.82 2  7} { 10.216.108.82 2  8}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.00\
    -setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure LDP as per the description
#    give above
################################################################################ 
puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]
set vportRx [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force
after 10000
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
        -start      {18:03:73:C7:6C:B1}              \
        -step       {00:00:00:00:00:01}

ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\
        -value      {18:03:73:C7:6C:01}
ixNet commit

# puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet]"

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
ixNet setAttr $mvAdd1/singleValue -value "20.20.20.2"
ixNet setAttr $mvAdd2/singleValue -value "20.20.20.1"
ixNet setAttr $mvGw1/singleValue  -value "20.20.20.1"
ixNet setAttr $mvGw2/singleValue  -value "20.20.20.2"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

# puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4]"

puts "Adding LDP over IP4 stacks"
ixNet add $ip1 ldpBasicRouter
ixNet add $ip2 ldpBasicRouter
ixNet commit

set ldp1 [ixNet getList $ip1 ldpBasicRouter]
set ldp2 [ixNet getList $ip2 ldpBasicRouter]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "PBB EVPN Topology 1"
ixNet setAttr $topo2  -name "PBB EVPN Topology 2"

ixNet setAttr $t1dev1 -name "LDP Router1"
ixNet setAttr $t2dev1 -name "LDP Router2"
ixNet commit

# puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp]"

puts "Adding NetworkGroup behind ldp DG"
ixNet exec createDefaultStack $t1devices ipv4PrefixPools
ixNet exec createDefaultStack $t2devices ipv4PrefixPools

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

ixNet setAttr $networkGroup1 -name "LDP_1_Network_Group"
ixNet setAttr $networkGroup2 -name "LDP_2_Network_Group"
ixNet setAttr $networkGroup1 -multiplier "1"
ixNet setAttr $networkGroup2 -multiplier "1"

set LdpPrefixPool1 [ixNet getList $networkGroup1 ipv4PrefixPools]
set LdpPrefixPool2 [ixNet getList $networkGroup2 ipv4PrefixPools]

puts "Configuring LDP prefixes"
ixNet setAttr [ixNet getAttr $LdpPrefixPool1 -networkAddress]/singleValue -value 2.2.2.2
ixNet setAttr [ixNet getAttr $LdpPrefixPool2 -networkAddress]/singleValue -value 3.2.2.2
ixNet commit

# Add ipv4 loopback1 behind LDP Topology 1
puts "Adding ipv4 loopback1"
set chainedDg1 [ixNet add $networkGroup1 deviceGroup]
ixNet setMultiAttribute $chainedDg1\
    -multiplier 1\
    -name {Device Group 3}
ixNet commit
set chainedDg1 [lindex [ixNet remapIds $chainedDg1] 0]

set loopback1 [ixNet add $chainedDg1 "ipv4Loopback"]
ixNet setMultiAttribute $loopback1\
    -stackedLayers [list]\
    -name {IPv4 Loopback 1}
ixNet commit

set connector1 [ixNet add $loopback1 "connector"]
ixNet setMultiAttribute $connector1\
    -connectedTo $networkGroup1/ipv4PrefixPools:1
ixNet commit
set connector1 [lindex [ixNet remapIds $connector1] 0]

set addressSet1 [ixNet getAttribute $loopback1 -address]
ixNet setMultiAttribute $addressSet1\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet1 [ixNet add $addressSet1 "counter"]
ixNet setMultiAttribute $addressSet1\
    -step 0.0.0.1\
    -start 2.2.2.2\
    -direction increment
ixNet commit
set addressSet1 [lindex [ixNet remapIds $addressSet1] 0]

# Add ipv4 loopback2 behind LDP Topology 2
puts "Adding ipv4 loopback2"
set chainedDg2 [ixNet add $networkGroup2 deviceGroup]
ixNet setMultiAttribute $chainedDg2\
    -multiplier 1\
    -name {Device Group 4}
ixNet commit
set chainedDg2 [lindex [ixNet remapIds $chainedDg2] 0]

set loopback2 [ixNet add $chainedDg2 "ipv4Loopback"]
ixNet setMultiAttribute $loopback2\
    -stackedLayers [list]\
    -name {IPv4 Loopback 2}
ixNet commit

set connector2 [ixNet add $loopback2 "connector"]
ixNet setMultiAttribute $connector2\
    -connectedTo $networkGroup2/ipv4PrefixPools:1
ixNet commit
set connector1 [lindex [ixNet remapIds $connector2] 0]

set addressSet2 [ixNet getAttribute $loopback2 -address]
ixNet setMultiAttribute $addressSet2\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet2 [ixNet add $addressSet2 "counter"]
ixNet setMultiAttribute $addressSet2\
    -step 0.0.0.1\
    -start 3.2.2.2\
    -direction increment
ixNet commit
set addressSet2 [lindex [ixNet remapIds $addressSet2] 0]


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

puts "Enabling EVPN Learned Information for BGP Router"
ixNet setAttr [ixNet getAttr $bgp1 -filterEvpn]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp2 -filterEvpn]/singleValue -value true
ixNet commit

puts "Adding PBB EVPN over BGP in both ports"
ixNet add $bgp1 bgpIPv4EvpnPbb
ixNet add $bgp2 bgpIPv4EvpnPbb
ixNet commit

set EvpnPbb1 [ixNet getList $bgp1 bgpIPv4EvpnPbb]
set EvpnPbb2 [ixNet getList $bgp2 bgpIPv4EvpnPbb]

puts "Configuring ESI value in both ports"
set ethernetSegment1 [ixNet getList $bgp1 bgpEthernetSegmentV4]
set ethernetSegment2 [ixNet getList $bgp2 bgpEthernetSegmentV4]
ixNet setAttr [ixNet getAttr $ethernetSegment1 -esiValue]/singleValue -value "1"
ixNet setAttr [ixNet getAttr $ethernetSegment2 -esiValue]/singleValue -value "1"

puts "Configuring B-MAC Prefix value in both ports"
ixNet setAttr [ixNet getAttr $ethernetSegment1 -bMacPrefix]/singleValue -value "B0:11:01:00:00:03"
ixNet setAttr [ixNet getAttr $ethernetSegment2 -bMacPrefix]/singleValue -value "B0:12:01:00:00:03"


puts "Adding Mac Pools behind PBB EVPN DG"
ixNet exec createDefaultStack $chainedDg1 macPools
ixNet exec createDefaultStack $chainedDg2 macPools

set networkGroup3 [lindex [ixNet getList $chainedDg1 networkGroup] 0]
set networkGroup4 [lindex [ixNet getList $chainedDg2 networkGroup] 0]

ixNet setAttr $networkGroup3 -name "MAC_Pool_1"
ixNet setAttr $networkGroup4 -name "MAC_Pool_2"
ixNet setAttr $networkGroup3 -multiplier "1"
ixNet setAttr $networkGroup4 -multiplier "1"

puts "Changing default values of MAC Addresses in MAC Pools"
set macPool1 [ixNet getList $networkGroup3 macPools]
set macPool2 [ixNet getList $networkGroup4 macPools]
ixNet setAttr [ixNet getAttr $macPool1 -mac]/singleValue -value "A0:11:01:00:00:03"
ixNet setAttr [ixNet getAttr $macPool2 -mac]/singleValue -value "A0:12:01:00:00:03"

ixNet commit

################################################################################
# 2. Start protocols and wait for 60 seconds
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
# 4. Retrieve protocol learned info
###############################################################################

puts "Fetching EVPN Learned Info"
ixNet exec getEVPNLearnedInfo $bgp1 

after 5000
set learnedInfoList [ixNet getList $bgp1 learnedInfo]
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
# 5. Configure L2-L3 traffic 
################################################################################
puts "Congfiguring L2-L3 Traffic Item"
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {Traffic Item 1}           \
    -roundRobinPacketOrdering false  \
    -trafficType ethernetVlan
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $networkGroup3/macPools:1]
set destination  [list $networkGroup4/macPools:1]

ixNet setMultiAttribute $endpointSet1\
    -name                  "EndpointSet-1"\
    -multicastDestinations [list]\
    -scalableSources       [list]\
    -multicastReceivers    [list]\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               $source\
    -destinations          $destination    
ixNet commit

ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy        [list mplsFlowDescriptor0 trackingenabled0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]
ixNet commit

###############################################################################
# 6. Apply and start L2/L3 traffic
###############################################################################
puts "applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

###############################################################################
# 7. Retrieve L2/L3 traffic item statistics
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
puts "***************************************************"

################################################################################
# 8. Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 9. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
