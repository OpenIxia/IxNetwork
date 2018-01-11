#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    09/06/2016 - Sumit - created sample                                 #
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
#    This script demonstrates usage NGPF BGP API for BGP-SR                    #
#	 Script uses two back-to-back Ixia ports to demonstrate the protocol       #
#                                                                              #
#    1. It will create 2 BGP-SR topologies, each having an ipv4 Prefix pool    #
#    2. Start the ospfv2 protocol.                                             #
#    3. Retrieve protocol statistics.                                          #
#    4. Enable the IPv4 MPLS Learned Info. filter on the fly.                  #
#    5. Retrieve protocol learned info.                                        #
#    6. Configure L2-L3 traffic.                                               #
#    7. Start the L2-L3 traffic.                                               #
#    8. Retrieve L2-L3 traffic stats.                                          #
#    9. Stop L2-L3 traffic.                                                    #
#   10. Stop all protocols.                                                    #
#                                                                              # 
# Ixia Software:                                                               #
#    IxOS      8.10 EA                                                         #
#    IxNetwork 8.10 EA                                                         #
#                                                                              #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.216.108.113
    set ixTclPort   5555
    set ports       {{xg12-regr 1 5} { xg12-regr 1 6}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.10 -setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# protocol configuration section                                               #
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
        -start      {44:22:33:00:00:A1}              \
        -step       {00:00:00:00:00:01}

ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\
        -value      {44:22:33:00:00:B1}
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
ixNet setAttr $mvAdd1/singleValue -value "20.20.20.2"
ixNet setAttr $mvAdd2/singleValue -value "20.20.20.1"
ixNet setAttr $mvGw1/singleValue  -value "20.20.20.1"
ixNet setAttr $mvGw2/singleValue  -value "20.20.20.2"

#set mask
ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

#enable resolve gateway
ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

puts "Add BGP over IP4 stack"
ixNet add $ip1 bgpIpv4Peer
ixNet add $ip2 bgpIpv4Peer
ixNet commit

set bgp1 [ixNet getList $ip1 bgpIpv4Peer]
set bgp2 [ixNet getList $ip2 bgpIpv4Peer]

puts "Rename the topologies and the device groups"
ixNet setAttr $topo1  -name "BGP-SR Topology 1"
ixNet setAttr $topo2  -name "BGP-SR Topology 2"

ixNet setAttr $t1dev1 -name "BGP-SR Topology 1 Router"
ixNet setAttr $t2dev1 -name "BGP-SR Topology 2 Router"
ixNet commit

puts "Set IPs in BGP DUT IP field"
ixNet setAttr [ixNet getAttr $bgp1 -dutIp]/singleValue -value "20.20.20.1"
ixNet setAttr [ixNet getAttr $bgp2 -dutIp]/singleValue -value "20.20.20.2"
ixNet commit

#Configure BGP-SR related fields in BGP router

# Enable Capabilities in BGP Routers - IPv4 MPLS & IPv6 MPLS
ixNet setAttribute $bgp1 -ipv4MplsCapability true
ixNet setAttribute $bgp1 -ipv6MplsCapability true
ixNet setAttribute $bgp2 -ipv4MplsCapability true
ixNet setAttribute $bgp2 -ipv6MplsCapability true
ixNet commit

# Configure SRGB - SID start count and SID range on BGP-SR Topology 1 Router
set bgp1srgb [lindex [ixNet getList $bgp1 bgpSRGBRangeSubObjectsList] 0]
set bgp1sIDCountMultiValue [ixNet getAttribute $bgp1srgb -sIDCount]
set bgp1startSIDMultivalue [ixNet getAttribute $bgp1srgb -startSID]
ixNet setMultiAttribute $bgp1sIDCountMultiValue/singleValue -value "6000"
ixNet setMultiAttribute $bgp1startSIDMultivalue/singleValue -value "25000"
ixNet commit

puts "Add IPv4 Prefix pool behind BGP Routers"
ixNet exec createDefaultStack $t1devices ipv4PrefixPools
ixNet exec createDefaultStack $t2devices ipv4PrefixPools

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

ixNet setAttr $networkGroup1 -name "BGP_1_IP_Prefix_pool"
ixNet setAttr $networkGroup2 -name "BGP_2_IP_Prefix_pool"
ixNet commit

puts "Configure BGP-SR related fields in IPv4 Prefix Pool behind BGP-SR Topology 1 Router"
set networkGroup1ipv4PrefixPools [lindex [ixNet getList $networkGroup1 ipv4PrefixPools] 0]
set ipv4PrefixPoolBgpIPRouteProperty [lindex [ixNet getList $networkGroup1ipv4PrefixPools bgpIPRouteProperty] 0]

set networkAddressStartMultivalue [ixNet getAttribute $networkGroup1ipv4PrefixPools -networkAddress]
ixNet setMultiAttribute $networkAddressStartMultivalue/singleValue -value "5.1.1.1"
ixNet setAttribute $networkGroup1ipv4PrefixPools -numberOfAddresses "5"
ixNet commit

ixNet setAttribute $ipv4PrefixPoolBgpIPRouteProperty -advertiseAsBgp3107Sr true
set segmentIdMultivalue [ixNet getAttribute $ipv4PrefixPoolBgpIPRouteProperty -segmentId]
ixNet setMultiAttribute $segmentIdMultivalue/singleValue -value "101"
ixNet commit

################################################################################
# Start protocol and check statistics                                          #
################################################################################
puts "Start All Protocols and wait for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000
puts "Display Protocol summary stats\n"
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

################################################################################
# On the fly enable MPLS Learned info filter                                   #  
################################################################################
puts "Enabling IPv4 MPLS Learned Information for BGP Router"
ixNet setAttr [ixNet getAttr $bgp1 -filterIpV4Mpls]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp2 -filterIpV4Mpls]/singleValue -value true
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
ixNet exec applyOnTheFly $topology
after 30000

###############################################################################
# print learned info                                                          #
###############################################################################
ixNet exec getIPv4MplsLearnedInfo $bgp2 1
after 5000
set linfo [ixNet getList $bgp2 learnedInfo]
set values [ixNet getAttribute $linfo -values]
puts "BGP learned info"
puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"


################################################################################
# L2/L3 Traffic configuration/apply/start section                              #
################################################################################
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {BGP-SR-Traffic Item}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv4
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set destination  [list $networkGroup1/ipv4PrefixPools:1]
set source  [list $networkGroup2/ipv4PrefixPools:1]

ixNet setMultiAttribute $endpointSet1\
    -name                  "EndpointSet-1"\
	-multicastDestinations [list]\
	-scalableSources       [list]\
	-multicastReceivers    [list]\
	-scalableDestinations  [list]\
	-ngpfFilters           [list]\
	-trafficGroups         [list]\
	-sources               $source\
	-destinations          $destination\	
ixNet commit

ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy [list mplsFlowDescriptor0 trackingenabled0 mplsMplsLabelValue0] \
	-values [list ] \
	-fieldWidth thirtyTwoBits \
	-protocolOffset Root.0
	
ixNet commit

###############################################################################
# apply start traffic                                                         #
###############################################################################
puts "Applying Traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 10000

puts "Start Traffic"
ixNet exec start [ixNet getRoot]/traffic
ixNet exec startStatefulTraffic [ixNet getRoot]/traffic
puts "Let traffic run for 30 seconds"
after 30000

###############################################################################
# Retrieve L2/L3 traffic item Flow statistics
###############################################################################
puts "Display all  L2-L3 traffic flow stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Flow Statistics"/page}
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


puts "Stop Traffic"
ixNet exec stop [ixNet getRoot]/traffic
ixNet exec stopStatefulTraffic [ixNet getRoot]/traffic
after 5000

puts "Stop All Protocols"
ixNet exec stopAllProtocols
puts "Sample Script Ends"

