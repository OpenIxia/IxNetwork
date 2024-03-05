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
#    This script intends to demonstrate how to use NGPF BGP API to configure   #
#     H-L3vpn Scenario.                                                        #
#                                                                              #
#    1. It will create a BGP topology with OSPF, RSVP-TE and Targeted LDP      #
#       configured in Area Border Router.                                      #
#    2. In Provider Edge Router configuration  BGP Peer is configured.         #
#    3. BGP VRF is configured on top of BGP Peer.                              # 
#    4. IPv4 & IPv6 Prefix Pools are added behind BGP VRF.                     # 
#    5. IPv4 and IPv6 addresses  are configured in IPv4 and IPv6 Prefix Pools. #
#    6. Label values are configured in V4 & V6 Prefix Pools.                   #
#    3. Only one side configuration is provided.                               #
#    4. Traffic configuration will be similar to L3VPN scenario.               #
################################################################################

# Script Starts
puts "!!!Hl3VPN Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.216.108.113
    set ixTclPort   8650
    set ports       {{10.216.108.82 7 11} { 10.216.108.82 7  12}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.20\
    setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Configure H-L3VPN topology as per the description give above
################################################################################ 
puts "Adding vport"
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]

puts "Adding topology"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]

puts "Adding device groups"
ixNet add $topo1 deviceGroup
ixNet commit

set t1devices [ixNet getList $topo1 deviceGroup]

set t1dev1 [lindex $t1devices 0]

puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $t1dev1 -multiplier 1
ixNet commit

puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet commit

set mac1 [ixNet getList $t1dev1 ethernet]

puts "Configuring the mac addresses"
ixNet setMultiAttr [ixNet getAttr $mac1 -mac]/counter\
        -direction  increment                        \
        -start      {18:03:73:C7:6C:B1}              \
        -step       {00:00:00:00:00:01}

ixNet commit

# puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet]"

puts "Add ipv4"
ixNet add $mac1 ipv4
ixNet commit

set ip1 [ixNet getList $mac1 ipv4]

set mvAdd1 [ixNet getAttr $ip1 -address]
set mvGw1  [ixNet getAttr $ip1 -gatewayIp]

puts "configuring ipv4 addresses"
ixNet setAttr $mvAdd1/singleValue -value "20.20.20.2"
ixNet setAttr $mvGw1/singleValue  -value "20.20.20.1"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet commit

# puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4]"

puts "Adding OSPF over IP4 stacks"
ixNet add $ip1 ospfv2
ixNet commit

set ospf1 [ixNet getList $ip1 ospfv2]

puts "Adding NetworkGroup behind Area Border Router DG"
ixNet exec createDefaultStack $t1devices ipv4PrefixPools

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]

ixNet setAttr $networkGroup1 -name "Network_Group"
ixNet setAttr $networkGroup1 -multiplier "1"

puts "Adding IPv4 Loobcak in first Device Group"
set loopback1 [ixNet add $t1dev1 ipv4Loopback]
ixNet commit

puts "Adding Targeted LDP over IPv4 Loopback"
ixNet add $loopback1 ldpTargetedRouter
ixNet commit

puts "Adding RSVP-TE over same IPv4 Loopback"
ixNet add $loopback1 rsvpteLsps
ixNet commit

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "Hl3VPN_Topology"

ixNet setAttr $t1dev1 -name "Area Border Router"
ixNet commit

# puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp]"

puts "Configuring LDP prefixes"
set LdpPrefixPool1 [ixNet getList $networkGroup1 ipv4PrefixPools]
ixNet setAttr [ixNet getAttr $LdpPrefixPool1 -networkAddress]/singleValue -value 2.2.2.2
ixNet commit

# Add chanined DG behind NetworkGroup
puts "Add chanined DG behind NetworkGroup"
set chainedDg1 [ixNet add $networkGroup1 deviceGroup]
ixNet setMultiAttribute $chainedDg1\
    -multiplier 10\
    -name {Provider Edge Router}
ixNet commit
set chainedDg1 [lindex [ixNet remapIds $chainedDg1] 0]

# Add ipv4 loopback in Chained DG 
puts "Adding ipv4 loopback in Chained DG"
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

# Adding BGP over IPv4 loopback interface
puts "Adding BGP over IPv4 loopback interface"
ixNet add $loopback1 bgpIpv4Peer
ixNet commit

set bgp [lindex [ixNet getList $loopback1 bgpIpv4Peer] 0]

puts "Setting IPs in BGP DUT IP tab"
ixNet setAttr [ixNet getAttr $bgp -dutIp]/singleValue -value "3.2.2.2"
ixNet commit

puts "Enabling L3VPN Learned Information filters in BGP Router"
ixNet setAttr [ixNet getAttr $bgp -filterIpV4MplsVpn]/singleValue -value true
ixNet setAttr [ixNet getAttr $bgp -filterIpV6MplsVpn]/singleValue -value true
ixNet commit

# Adding VRF over BGP Peer
puts "Adding VRF over BGP Peer"
ixNet add $bgp bgpVrf
ixNet commit

set bgpVrf [ixNet getList $bgp bgpVrf]

# Adding IPv4 Address Pool behind bgpVrf 
puts "Adding IPv4 Address Pools behind bgpVrf"
set networkGroup3 [ixNet add $chainedDg1 networkGroup]
ixNet commit
set ipv4PrefixPool [ixNet add $networkGroup3 ipv4PrefixPools]
ixNet commit
ixNet setAttr $networkGroup3 -multiplier "1"
ixNet commit

puts "Changing default values of IPv4 prefixes"
ixNet setAttr [ixNet getAttr $ipv4PrefixPool -networkAddress]/singleValue -value "203.1.0.0"
ixNet commit

# Changing Label value in IPv4 Prefix Pool 
puts "Changing Label value in IPv4 Prefix Pool"
set v4RouteProperty [ixNet getList $ipv4PrefixPool bgpL3VpnRouteProperty]
set multiValue [ixNet getAttr $v4RouteProperty -labelStart]
ixNet setMultiAttr $multiValue -clearOverlay false
set count [ixNet add $multiValue counter]
ixNet setMultiAttr $count  -step 10 -start 4000 -direction increment
ixNet commit

# Adding IPv6 Address Pool behind bgpVrf
puts "Adding IPv6 Address Pools behind bgpVrf"
set networkGroup4 [ixNet add $chainedDg1 networkGroup]
ixNet commit
set ipv6PrefixPool [ixNet add $networkGroup4 ipv6PrefixPools]
ixNet commit
ixNet setAttr $networkGroup4 -multiplier "1"
ixNet commit

# Changing default values of IPv6 prefixes
puts "Changing default values of IPv6 prefixes"
ixNet setAttr [ixNet getAttr $ipv6PrefixPool -networkAddress]/singleValue -value "2000:1:1:1:0:0:0:0"
ixNet commit

# Changing Label value in IPv6 Prefix Pool
puts "Changing Label value in IPv6 Prefix Pool"
set v6RouteProperty [ixNet getList $ipv6PrefixPool bgpV6L3VpnRouteProperty]
set multiValue [ixNet getAttr $v6RouteProperty -labelStart]
ixNet setMultiAttr $multiValue -clearOverlay false
set count [ixNet add $multiValue counter]
ixNet setMultiAttr $count  -step 10 -start 5000 -direction increment
ixNet commit

puts "!!! Scenario confiugrd Successfully!!!\n";
puts "!!! Test Script Ends !!!"
