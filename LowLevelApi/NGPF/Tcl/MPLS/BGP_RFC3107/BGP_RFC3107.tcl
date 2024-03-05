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
#    This script intends to demonstrate how to use NGPF BGP RFC 3107 TCL APIs   #
#    About Topology:                                                            #
#       The scenario consists of two BGP peers.                                 #
#       Each of them capable of carrying Label information for the attached     #
#       advertising Route Range. Unidirectional Traffic is created in between   #
#       the peers.                                                              #
#         Script Flow:                                                          #
#        Step 1. Creation of 2 BGP topologies with RFC3107 IPv4 MPLS Capability #
#        Step 2. Start of protocol                                              #
#        Step 3. Protocol Stat display                                          #
#        Step 4. Learned Info display                                           #
#        Step 5. Configuration L2-L3 Traffic                                    #
#        Step 6. Apply and Start of L2-L3 traffic                               #
#        Step 7. Display of L2-L3  traffic Stats                                #
#        Step 8.Stop of L2-L3 traffic                                           #
#        Step 9.Stop of all protocols                                           #
#################################################################################


# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.216.104.58
    set ixTclPort   8239
    set ports       {{10.216.108.82 7 15} { 10.216.108.82 7 16}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Disconnecting if any already connected"
ixNet disconnect $::ixia::ixTclServer

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.10\
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
ixNet setAttr $topo1  -name "BGP Topology 1"
ixNet setAttr $topo2  -name "BGP Topology 2"

set t1dev1 [lindex $t1devices 0]
set t2dev1 [lindex $t2devices 0]
ixNet setAttr $t1dev1 -name "BGP Router 1"
ixNet setAttr $t2dev1 -name "BGP Router 2"
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
        -start      {22:22:22:22:22:22}              \
        -step       {00:00:00:00:01:00}

ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\
        -value      {44:44:44:44:44:44}
ixNet commit

puts "Adding IPv4 stack and configuring  IP Address"
ixNet add $mac1 ipv4
ixNet add $mac2 ipv4
ixNet commit

set ip1 [ixNet getList $mac1 ipv4]
set ip2 [ixNet getList $mac2 ipv4]

set mvAdd1 [ixNet getAttr $ip1 -address]
set mvAdd2 [ixNet getAttr $ip2 -address]
set mvGw1  [ixNet getAttr $ip1 -gatewayIp]
set mvGw2  [ixNet getAttr $ip2 -gatewayIp]

puts "Configuring ipv4 addresses"
ixNet setAttr $mvAdd1/singleValue -value "50.50.50.2"
ixNet setAttr $mvAdd2/singleValue -value "50.50.50.1"
ixNet setAttr $mvGw1/singleValue  -value "50.50.50.1"
ixNet setAttr $mvGw2/singleValue  -value "50.50.50.2"

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

puts "Adding BGP over IPv4 stack"
ixNet add $ip1 bgpIpv4Peer
ixNet add $ip2 bgpIpv4Peer
ixNet commit

set bgp1 [ixNet getList $ip1 bgpIpv4Peer]
set bgp2 [ixNet getList $ip2 bgpIpv4Peer]

puts "Enabling BGP 3107 advertising capability in BGP Peer"
ixNet setMultiAttribute $bgp1 -ipv4MplsCapability true 
ixNet commit

ixNet setMultiAttribute $bgp2 -ipv4MplsCapability true 
ixNet commit

puts "Setting IPs in BGP DUT IP tab"
ixNet setAttr [ixNet getAttr $bgp1 -dutIp]/singleValue -value "50.50.50.1"
ixNet setAttr [ixNet getAttr $bgp2 -dutIp]/singleValue -value "50.50.50.2"
ixNet commit

puts "Adding NetworkGroup behind BGP DG"
ixNet exec createDefaultStack $t1devices ipv4PrefixPools
ixNet exec createDefaultStack $t2devices ipv4PrefixPools

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

puts "Configuring the number of addresses"
set ipv4PrefixPools1 [ixNet getList $networkGroup1 ipv4PrefixPools]
ixNet setMultiAttribute $ipv4PrefixPools1 -numberOfAddresses 5 
ixNet commit
set ipv4PrefixPools1 [lindex [ixNet remapIds $ipv4PrefixPools1] 0]
		
set ipv4PrefixPools2 [ixNet getList $networkGroup2 ipv4PrefixPools]
ixNet setMultiAttribute $ipv4PrefixPools2 -numberOfAddresses 5
ixNet commit
set ipv4PrefixPools2 [lindex [ixNet remapIds $ipv4PrefixPools2] 0]

puts "Enabling BGP 3107 in BGP IP Route Ranges"
set bgpIPRouteProp1 [ixNet add $ipv4PrefixPools1 "bgpIPRouteProperty"]
ixNet setMultiAttribute $bgpIPRouteProp1 -advertiseAsBgp3107 true 
ixNet commit
set bgpIPRouteProp1 [lindex [ixNet remapIds $bgpIPRouteProp1] 0]

set bgpIPRouteProp2 [ixNet add $ipv4PrefixPools2 "bgpIPRouteProperty"]
ixNet setMultiAttribute $bgpIPRouteProp2 -advertiseAsBgp3107 true 	
ixNet commit
set bgpIPRouteProp2 [lindex [ixNet remapIds $bgpIPRouteProp2] 0]

puts "Editing Label values in BGP IP Route Ranges"
set labelStrt_1 [ixNet getAttribute $bgpIPRouteProp1 -labelStart]
ixNet setMultiAttribute $labelStrt_1 -clearOverlays false
ixNet commit

set sv1 [ixNet add $labelStrt_1 "singleValue"]
ixNet setMultiAttribute $sv1 -value 1006
ixNet commit

set labelStrt_2 [ixNet getAttribute $bgpIPRouteProp2 -labelStart]
ixNet setMultiAttribute $labelStrt_2 -clearOverlays false
ixNet commit

set sv2 [ixNet add $labelStrt_2 "singleValue"]
ixNet setMultiAttribute $sv2 -value 2006
ixNet commit

puts "Enabling IPv4 MPLS Learned Information for BGP Routers"
ixNet setAttr [ixNet getAttr $bgp1 -filterIpV4Mpls]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp2 -filterIpV4Mpls]/singleValue -value true
ixNet commit
		
puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $networkGroup1 -multiplier 5
ixNet setAttr $networkGroup2 -multiplier 5
ixNet commit

################################################################################
# Step 2> Start of protocol.
################################################################################
puts "Starting protocols and waiting for 45 seconds for protocols to come up"
ixNet exec startAllProtocols
after 45000

################################################################################
# Step 3> Retrieve protocol statistics.
################################################################################
puts "Verifying all the statistics\n"
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
# Step 4> Retrieve protocol learned info
###############################################################################
ixNet exec getIPv4MplsLearnedInfo $bgp1 1
after 5000
set linfo_1 [ixNet getList $bgp1 learnedInfo]
set values_1 [ixNet getAttribute $linfo_1 -values]
puts "BGP learned info"
puts "***************************************************"
foreach v1 $values_1 {
    puts $v1
}
puts "***************************************************"

################################################################################
# Step 5> Configure L2-L3 traffic.
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
	-sources               $source\
	-destinations          $destination\	
ixNet commit

ixNet setMultiAttribute $trafficItem1/tracking -trackBy \
    [list sourceDestEndpointPair0 mplsFlowDescriptor0 trackingenabled0 mplsMplsLabelValue0 ipv4DestIp0 ipv4SourceIp0]
ixNet commit

###############################################################################
# Step 6> Apply and start L2/L3 traffic.
###############################################################################
puts "applying traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000
puts "starting traffic"
ixNet exec start [ixNet getRoot]/traffic

puts "let traffic run for 120 second"
after 12000
###############################################################################
# Step 7> Retrieve L2/L3 traffic item statistics.
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
# Step 8> Stop L2/L3 traffic.
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# Step 9> Stop all protocols.
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"