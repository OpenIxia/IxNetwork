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
#    This script intends to demonstrate how to use BGP Large Community         #
#  (RFC8092).								                                   #	
#    It will create 2 BGP topologies, add IPv4 prefix pools to them, enable    # 
#    Large Community in one of them,modify the Number of Large Communities,    #
#    and  will start the emulation .It will then retrieve and display Learned  #
#    info statistics.				                                           #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.50.121
    set ixTclPort   8019
    set ports       {{10.39.50.123 9 7} { 10.39.50.123 9 8}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.50\
    –setAttribute strict

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
set topology1 [lindex $topologies 0]
set topology2 [lindex $topologies 1]

puts "Adding 2 device groups"
ixNet add $topology1 deviceGroup
ixNet add $topology2 deviceGroup
ixNet commit

set deviceGroup_T1 [ixNet getList $topology1 deviceGroup]
set deviceGroup_T2 [ixNet getList $topology2 deviceGroup]

set deviceGroup_T1 [lindex $deviceGroup_T1 0]
set deviceGroup_T2 [lindex $deviceGroup_T2 0]

puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $deviceGroup_T1 -multiplier 1
ixNet setAttr $deviceGroup_T2 -multiplier 1
ixNet commit

puts "Adding ethernet/mac endpoints"
ixNet add $deviceGroup_T1 ethernet
ixNet add $deviceGroup_T2 ethernet
ixNet commit

set mac1 [ixNet getList $deviceGroup_T1 ethernet]
set mac2 [ixNet getList $deviceGroup_T2 ethernet]

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


puts "Enabling BGP IPv4 unicast Capability"
set cap1 [ixNet getAttr $bgp1 -capabilityIpV4Unicast]
set cap2 [ixNet getAttr $bgp2 -capabilityIpV4Unicast]
set sv1 [ixNet getList $cap1 singleValue]
set sv2 [ixNet getList $cap2 singleValue]
ixNet setAttr $sv1 -value true
ixNet setAttr $sv2 -value true
ixNet commit

puts "Enabling BGP Filter IPv4 Unicast"
set filter1 [ixNet getAttr $bgp1 -filterIpV4Unicast]
set filter2 [ixNet getAttr $bgp2 -filterIpV4Unicast]
set sv1 [ixNet getList $filter1 singleValue]
set sv2 [ixNet getList $filter2 singleValue]
ixNet setAttr $sv1 -value true
ixNet setAttr $sv2 -value true
ixNet commit

puts "Renaming the topologies and the device groups"
ixNet setAttr $topology1  -name "BGP Topology 1"
ixNet setAttr $topology2  -name "BGP Topology 2"

ixNet setAttr $deviceGroup_T1 -name "BGP Topology 1 Router"
ixNet setAttr $deviceGroup_T2 -name "BGP Topology 2 Router"
ixNet commit

puts "Setting IPs in BGP DUT IP tab"
ixNet setAttr [ixNet getAttr $bgp1 -dutIp]/singleValue -value "20.20.20.1"
ixNet setAttr [ixNet getAttr $bgp2 -dutIp]/singleValue -value "20.20.20.2"
ixNet commit

puts "Adding the NetworkGroup with Routers at back of it"
ixNet exec createDefaultStack $deviceGroup_T1 ipv4PrefixPools
ixNet exec createDefaultStack $deviceGroup_T2 ipv4PrefixPools

set networkGroup_T1 [lindex [ixNet getList $deviceGroup_T1 networkGroup] 0]
set networkGroup_T2 [lindex [ixNet getList $deviceGroup_T2 networkGroup] 0]

ixNet setAttr $networkGroup_T1 -name "BGP_1_Network_Group1"
ixNet setAttr $networkGroup_T2 -name "BGP_2_Network_Group1"
ixNet commit
set IPv4Pool_T1 [ixNet getList $networkGroup_T1 ipv4PrefixPools]
ixNet commit

after 5000 ; #Wait for the commit to take place.

set IPv4Pool_T2 [ixNet getList $networkGroup_T2 ipv4PrefixPools]
ixNet commit

after 5000;# Wait for the commit to take place.

#Persuing IPv4 Prefix Pool below
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
set bgpV4IPRoutePropertyPri_T1 [ixNet getList $IPv4Pool_T1 bgpIPRouteProperty]
set LargeComm_v4_T1 $bgpV4IPRoutePropertyPri_T1/bgpNonVPNRRLargeCommunitiesList

set EnableLargeComm_v4_T1 [ixNet getAttribute $bgpV4IPRoutePropertyPri_T1 -enableLargeCommunities]
set singleValue_v4_T1 [ixNet getList $EnableLargeComm_v4_T1 singleValue]
ixNet setAttribute $singleValue_v4_T1 -value true
ixNet commit
after 5000;# Wait for the commit to take place.

#puts "Modifying the Number of LargeCommunities\n"

ixNet setAttrib $bgpV4IPRoutePropertyPri_T1 -noOfLargeCommunities 3
ixNet commit
after 5000;# Wait for the commit to take place.

set LargeComm1_v4pool_T1 [lindex [ixNet getList $bgpV4IPRoutePropertyPri_T1 bgpNonVPNRRLargeCommunitiesList] 0]
set LargeComm2_v4pool_T1 [lindex [ixNet getList $bgpV4IPRoutePropertyPri_T1 bgpNonVPNRRLargeCommunitiesList] 1]
set LargeComm3_v4pool_T1 [lindex [ixNet getList $bgpV4IPRoutePropertyPri_T1 bgpNonVPNRRLargeCommunitiesList] 2]

set LargeComm2_v4Pool_T1_attr [ixNet getAttribute $LargeComm2_v4pool_T1 -largeCommunity]
ixNet commit
after 5000;# Wait for the commit to take place.

set LargeComm2_v4Pool_T1_attr_str [ixNet add $LargeComm2_v4Pool_T1_attr "string"]
ixNet setAttribute $LargeComm2_v4Pool_T1_attr_str -pattern "\{Inc:\ 85550,10\}:\{Dec:\ 100,10\}:70"
ixNet commit
after 5000;# Wait for the commit to take place.

# ---------------------------------------------------------------------------
# Starting Topology 
# ---------------------------------------------------------------------------    
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
###############################################################################
# print learned info                                                          #
###############################################################################
ixNet exec getIPv4LearnedInfo $bgp2 1
after 5000
set linfo [ixNet getList $bgp2 learnedInfo]
set values [ixNet getAttribute $linfo -values]
puts "BGP learned info"
puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"

puts "Stopping all protocols"
ixNet exec stopAllProtocols
puts "*********************************************************************END*************************************************************************"
