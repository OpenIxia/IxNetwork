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

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF BGP API                #
#    It will create 2 BGP topologies, it will start the emulation and          #
#    than it will retrieve and display few statistics                          #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.205.25.97
    set ixTclPort   8009
    set ports       {{10.205.28.63 10 13} { 10.205.28.63 10 14}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.40\
    �setAttribute strict

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
        -start      {18:03:73:C7:6C:B1}              \
        -step       {00:00:00:00:00:01}

ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\
        -value      {18:03:73:C7:6C:01}
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

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

puts "Adding BGP over IP4 stack"
ixNet add $ip1 bgpIpv4Peer
ixNet add $ip2 bgpIpv4Peer
ixNet commit

set bgp1 [ixNet getList $ip1 bgpIpv4Peer]
set bgp2 [ixNet getList $ip2 bgpIpv4Peer]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "BGP Topology 1"
ixNet setAttr $topo2  -name "BGP Topology 2"

ixNet setAttr $t1dev1 -name "BGP Topology 1 Router"
ixNet setAttr $t2dev1 -name "BGP Topology 2 Router"
ixNet commit

puts "Setting IPs in BGP DUT IP tab"
ixNet setAttr [ixNet getAttr $bgp1 -dutIp]/singleValue -value "20.20.20.1"
ixNet setAttr [ixNet getAttr $bgp2 -dutIp]/singleValue -value "20.20.20.2"
ixNet commit

puts "Adding the NetworkGroup with Routers at back of it"
ixNet exec createDefaultStack $t1devices ipv4PrefixPools
ixNet exec createDefaultStack $t2devices ipv4PrefixPools

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

ixNet setAttr $networkGroup1 -name "BGP_1_Network_Group1"
ixNet setAttr $networkGroup2 -name "BGP_2_Network_Group1"
ixNet commit

################################################################################
# add ipv4 loopback1 for applib traffic                                        #
################################################################################
set chainedDg1 [ixNet add $networkGroup1 deviceGroup]
ixNet setMultiAttribute $chainedDg1\
    -multiplier 1\
	-name {Device Group 4}
ixNet commit
set chainedDg1 [lindex [ixNet remapIds $chainedDg1] 0]

set loopback1 [ixNet add $chainedDg1 "ipv4Loopback"]
ixNet setMultiAttribute $loopback1\
    -stackedLayers [list]\
    -name {IPv4 Loopback 2}
ixNet commit

set addressSet1 [ixNet getAttribute $loopback1 -address]
ixNet setMultiAttribute $addressSet1\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet1 [ixNet add $addressSet1 "counter"]
ixNet setMultiAttribute $addressSet1\
    -step 0.1.0.0\
    -start 200.1.0.0\
    -direction increment
ixNet commit
set addressSet1 [lindex [ixNet remapIds $addressSet1] 0]

################################################################################
# add ipv4 loopback2 for applib traffic                                        #
################################################################################
set chainedDg2 [ixNet add $networkGroup2 deviceGroup]
ixNet setMultiAttribute $chainedDg2\
    -multiplier 1\
	-name {Device Group 3}
ixNet commit
set chainedDg2 [lindex [ixNet remapIds $chainedDg2] 0]

set loopback2 [ixNet add $chainedDg2 "ipv4Loopback"]
ixNet setMultiAttribute $loopback2\
    -stackedLayers [list]\
    -name {IPv4 Loopback 1}
ixNet commit

set addressSet2 [ixNet getAttribute $loopback2 -address]
ixNet setMultiAttribute $addressSet2\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet1 [ixNet add $addressSet2 "counter"]
ixNet setMultiAttribute $addressSet1\
    -step 0.1.0.0\
    -start 201.1.0.0\
    -direction increment
ixNet commit
set addressSet1 [lindex [ixNet remapIds $addressSet2] 0]

################################################################################
# Start protocol and check statistics                                          #
################################################################################
puts "Starting protocols and waiting for 45 seconds for protocols to come up"
ixNet exec startAllProtocols
after 45000
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
puts "***************************************************"

################################################################################
# On the fly section                                                           #  
################################################################################
puts "Enabling IPv4 Unicast Learned Information for BGP Router"
ixNet setAttr [ixNet getAttr $bgp1 -filterIpV4Unicast]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp2 -filterIpV4Unicast]/singleValue -value true
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
	puts "$::errorInfo"
}
after 10000

###############################################################################
# print learned info                                                          #
###############################################################################
ixNet exec getIPv4LearnedInfo $bgp1 1
after 5000
set linfo [ixNet getList $bgp1 learnedInfo]
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
    -name {Traffic Item 1}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv4
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $networkGroup1/ipv4PrefixPools:1]
set destination  [list $networkGroup2/ipv4PrefixPools:1]

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
    -trackBy        [list sourceDestEndpointPair0 trackingenabled0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]\
ixNet commit

################################################################################
# add applibrary traffic item                                                  #
################################################################################
set trafficItem2 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem2  \
    -name {Traffic Item 2}             \
    -trafficItemType applicationLibrary\
    -roundRobinPacketOrdering false    \
    -trafficType ipv4ApplicationTraffic
ixNet commit
set trafficItem2 [lindex [ixNet remapIds $trafficItem2] 0]

set endpointSet2 [ixNet add $trafficItem2 "endpointSet"]
set source_app [list [lindex [ixNet getList $t1devices networkGroup] 0]]
set destin_app [list [lindex [ixNet getList $t2devices networkGroup] 0]]

ixNet setMultiAttribute $endpointSet2\
    -name                  "EndpointSet-2"\
	-multicastDestinations [list]     \
	-scalableSources       [list]     \
	-multicastReceivers    [list]     \
	-scalableDestinations  [list]     \
	-ngpfFilters           [list]     \
	-trafficGroups         [list]     \
	-sources               $source_app\
	-destinations          $destin_app\	
ixNet commit
set endpointSet2 [lindex [ixNet remapIds $endpointSet2] 0]

set appLibProfile [ixNet add $trafficItem2 "appLibProfile"]
set flows_configured  [list Bandwidth_BitTorrent_File_Download\
                            Bandwidth_eDonkey\
 							Bandwidth_HTTP\
							Bandwidth_IMAPv4\
							Bandwidth_POP3\
							Bandwidth_Radius\
							Bandwidth_Raw\
							Bandwidth_Telnet\
							Bandwidth_uTorrent_DHT_File_Download\
							BBC_iPlayer\
							BBC_iPlayer_Radio\
							BGP_IGP_Open_Advertise_Routes\
							BGP_IGP_Withdraw_Routes\
							Bing_Search\
							BitTorrent_Ares_v217_File_Download\
							BitTorrent_BitComet_v126_File_Download\
							BitTorrent_Blizzard_File_Download\
							BitTorrent_Cisco_EMIX\
							BitTorrent_Enterprise\
							BitTorrent_File_Download\
							BitTorrent_LimeWire_v5516_File_Download\
							BitTorrent_RMIX_5M]

ixNet setMultiAttribute $appLibProfile\
    -enablePerIPStats false \
    -objectiveDistribution applyFullObjectiveToEachPort \
    -configuredFlows $flows_configured
ixNet commit

set appLibProfile [lindex [ixNet remapIds $appLibProfile] 0]

###############################################################################
# apply start traffic                                                         #
###############################################################################
puts "applying traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000
ixNet exec applyStatefulTraffic  [ixNet getRoot]/traffic
after 5000

puts "starting traffic"
ixNet exec start [ixNet getRoot]/traffic
ixNet exec startStatefulTraffic [ixNet getRoot]/traffic
puts "let traffic run for 60 seconds"
after 60000

###############################################################################
# print traffic item statistics                                               #
###############################################################################
puts "Verifying all the application traffic stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Application Traffic Item Statistics"/page}
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

puts "Verifying all the application traffic stats\n"
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

puts " "
puts "For more info please refer to the user manual or the built-in help"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2]"
puts " "
puts "[ixNet help [ixNet getRoot]/traffic]"

puts "stopping traffic"
ixNet exec stop [ixNet getRoot]/traffic
ixNet exec stopStatefulTraffic [ixNet getRoot]/traffic
after 15000

puts "Stopping all protocols"
ixNet exec stopAllProtocols
puts "*********************************************************************END*************************************************************************"