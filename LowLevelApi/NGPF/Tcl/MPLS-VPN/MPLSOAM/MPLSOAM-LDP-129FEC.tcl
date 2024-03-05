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
#   This script intends to demonstrate how to use NGPF LDPv6 Low Level TCL API #
#   with FEC129.               					                               #
#                                                                              #
#    1. Configuration of protocols as described in topology.                   #
#    2. Start all protocols.                                                   #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Change LDP PW/VPLS labels & apply change on the fly                    #
#    6. Retrieve protocol learned info again.                                  #
#    7. Configure L2-L3 traffic.                                               #
#    8. Start the L2-L3 traffic.                                               #
#   11. Retrieve L2-L3 traffic stats.                                          #
#   12. Stop L2-L3 traffic.                                                    #
#   13. Stop all protocols.                                                    #                                                                                
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.216.22.32
    set ixTclPort   8009
    set ports       {{10.216.100.12 2 1} { 10.216.100.12 2 5}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.30\
    –setAttribute strict

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
        -start      {00:11:01:00:00:01}              \
        -step       {00:00:00:00:00:01}

ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\
        -value      {00:12:01:00:00:01}
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

puts "Adding LDP connected interface over IP4 stacks"
ixNet add $ip1 ldpBasicRouter
ixNet add $ip2 ldpBasicRouter
ixNet commit

puts "Adding MPLSOAM over IP4 stacks"
ixNet add $ip1 mplsOam
ixNet add $ip2 mplsOam
ixNet commit

set ldp1 [ixNet getList $ip1 ldpBasicRouter]
set ldp2 [ixNet getList $ip2 ldpBasicRouter]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "LDPv4 FEC129 Topology 1"
ixNet setAttr $topo2  -name "LDPv4 FEC129 Topology 1"

ixNet setAttr $t1dev1 -name "P Router 1"
ixNet setAttr $t2dev1 -name "P Router 2"
ixNet commit

puts "Adding NetworkGroup behind LDPv4 dual stack DG"

ixNet add $t1dev1 networkGroup
ixNet add $t2dev1 networkGroup
ixNet commit


#ixNet exec createDefaultStack $t1devices ipv4PrefixPools
#ixNet exec createDefaultStack $t2devices ipv4PrefixPools

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

ixNet setAttr $networkGroup1 -name "LDP_1_Network_Group1"
ixNet setAttr $networkGroup2 -name "LDP_2_Network_Group1"
ixNet setAttr $networkGroup1 -multiplier "2"
ixNet setAttr $networkGroup2 -multiplier "2"
ixNet commit



puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "LDP Topology 1"
ixNet setAttr $topo2  -name "LDP Topology 2"

ixNet setAttr $t1dev1 -name "LDP Topology 1 Router"
ixNet setAttr $t2dev1 -name "LDP Topology 2 Router"
ixNet commit


puts "Adding IPv4 prefix pools in Network Groups"
ixNet add $networkGroup1 ipv4PrefixPools
ixNet add $networkGroup2 ipv4PrefixPools
ixNet commit

set ipv4PrefixPools1 [ixNet getList $networkGroup1 ipv4PrefixPools]
set ipv4PrefixPools2 [ixNet getList $networkGroup2 ipv4PrefixPools]

puts "Configuring network address and prefix length of IPv4 prefix pools"
set prefixLength1 [ixNet getAttribute $ipv4PrefixPools1 -prefixLength]
set prefixLength2 [ixNet getAttribute $ipv4PrefixPools2 -prefixLength]
ixNet setMultiAttribute $prefixLength1 \
    -clearOverlays false \
    -pattern singleValue
ixNet setMultiAttribute $prefixLength2 \
    -clearOverlays false \
    -pattern singleValue
ixNet commit
set singleValue1 [ixNet add $prefixLength1 "singleValue"]
set singleValue2 [ixNet add $prefixLength2 "singleValue"]
ixNet setMultiAttribute $singleValue1 -value 32
ixNet setMultiAttribute $singleValue2 -value 32
ixNet commit

set addressSet1 [ixNet getAttribute $ipv4PrefixPools1 -networkAddress]
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

set addressSet2 [ixNet getAttribute $ipv4PrefixPools2 -networkAddress]
ixNet setMultiAttribute $addressSet2\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet2 [ixNet add $addressSet2 "counter"]
ixNet setMultiAttribute $addressSet2\
    -step 0.0.0.1\
    -start 1.1.1.1\
    -direction increment
ixNet commit

puts "Changing fec label in DG2"
set ldpFEC2        [lindex [ixNet getList $ipv4PrefixPools2 ldpFECProperty] 0]
set activeMultivalue2 [ixNet getAttribute $ldpFEC2 -active]
ixNet setAttribute $activeMultivalue2/singleValue -value true
ixNet commit

set labelMultiValue2 [ixNet getAttribute $ldpFEC2 -labelValue]
ixNet setMultiAttribute $labelMultiValue2\
    -clearOverlays false\
    -pattern counter
ixNet commit
puts "Changing FEC lables"
set labelSet [ixNet add $labelMultiValue2 "counter"]
ixNet setMultiAttribute $labelSet\
    -step 1\
    -start 100\
    -direction increment
ixNet commit



puts "Adding Device Group behind Network Groups"
ixNet add $networkGroup1 deviceGroup
ixNet add $networkGroup2 deviceGroup
ixNet commit


set t1dev2 [lindex [ixNet getList $networkGroup1 deviceGroup] 0]
set t2dev2 [lindex [ixNet getList $networkGroup2 deviceGroup] 0]

puts "Configuring the multipliers"
ixNet setAttr $t1dev2 -multiplier 1
ixNet setAttr $t2dev2 -multiplier 1
ixNet commit

ixNet setAttr $t1dev2 -name "PE Router 1"
ixNet setAttr $t2dev2 -name "PE Router 2"
ixNet commit

puts "Adding loopback in second device group of both topologies"
ixNet add $t1dev2 ipv4Loopback
ixNet add $t2dev2 ipv4Loopback
ixNet commit

set ipv4Loopback1 [ixNet getList $t1dev2 ipv4Loopback]
set ipv4Loopback2 [ixNet getList $t2dev2 ipv4Loopback]

puts "Adding targeted LDPv4 router over these loopbacks"
ixNet add $ipv4Loopback1 ldpTargetedRouter
ixNet add $ipv4Loopback2 ldpTargetedRouter
ixNet commit

puts "Assigning ipv4 address on Loop Back Interface"
set addressSet1 [ixNet getAttribute $ipv4Loopback1 -address]
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

set addressSet2 [ixNet getAttribute $ipv4Loopback2 -address]
ixNet setMultiAttribute $addressSet2\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet2 [ixNet add $addressSet2 "counter"]
ixNet setMultiAttribute $addressSet2\
    -step 0.0.0.1\
    -start 1.1.1.1\
    -direction increment
ixNet commit

set ldpTargetedRouterV41 [ixNet getList $ipv4Loopback1 ldpTargetedRouter]
set ldpTargetedRouterV42 [ixNet getList $ipv4Loopback2 ldpTargetedRouter]

puts "Configuring DUT IP in LDPv4 targeted peers"
set iPAddress1 [ixNet getAttribute $ldpTargetedRouterV41/ldpTargetedPeer -iPAddress]
set iPAddress2 [ixNet getAttribute $ldpTargetedRouterV42/ldpTargetedPeer -iPAddress]
ixNet setMultiAttribute $iPAddress1 \
    -clearOverlays false \
    -pattern counter
ixNet setMultiAttribute $iPAddress2 \
    -clearOverlays false \
    -pattern counter
ixNet commit
set counter1 [ixNet add $iPAddress1 "counter"]
set counter2 [ixNet add $iPAddress2 "counter"]
ixNet setMultiAttribute $counter1 \
    -step 0.0.0.1 \
    -start 1.1.1.1 \
    -direction increment
ixNet setMultiAttribute $counter2 \
    -step 0.0.0.1 \
    -start 2.2.2.2 \
    -direction increment
ixNet commit


puts "Enabling router capabilities for MPLSOAM in Targated LDP RTR"
ixNet setMultiAttr [ixNet getAttr $ldpTargetedRouterV41 -enableBfdMplsLearnedLsp]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ldpTargetedRouterV42 -enableBfdMplsLearnedLsp]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ldpTargetedRouterV41 -enableLspPingLearnedLsp]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ldpTargetedRouterV42 -enableLspPingLearnedLsp]/singleValue -value true
ixNet commit


puts "Adding MPLSOAM over IP4 loopback stacks"
ixNet add $ipv4Loopback1 mplsOam
ixNet add $ipv4Loopback2 mplsOam
ixNet commit

set mplsoamloop1 [ixNet getList $ipv4Loopback1 mplsOam]
set mplsoamloop2 [ixNet getList $ipv4Loopback2 mplsOam]

puts "Enabling periodic ping on mplsOam"
ixNet setMultiAttr [ixNet getAttr $mplsoamloop1 -enablePeriodicPing]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $mplsoamloop2 -enablePeriodicPing]/singleValue -value true
ixNet commit

puts "Changing echo request interval to 5sec"
ixNet setMultiAttr [ixNet getAttr $mplsoamloop1 -echoRequestInterval]/singleValue -value 5000
ixNet setMultiAttr [ixNet getAttr $mplsoamloop2 -echoRequestInterval]/singleValue -value 5000
ixNet commit


puts "Adding LDP PW/VPLS over these targeted routers"

ixNet add $ldpTargetedRouterV41 ldpvplsbgpad
ixNet add $ldpTargetedRouterV42 ldpvplsbgpad
ixNet commit

set ldppwvpls1 [ixNet getList $ldpTargetedRouterV41 ldpvplsbgpad]
set ldppwvpls2 [ixNet getList $ldpTargetedRouterV42 ldpvplsbgpad]

puts "Enabling C-Bit in LDP PW/VPLS"
ixNet setMultiAttr [ixNet getAttr $ldppwvpls1 -cBitEnabled]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ldppwvpls2 -cBitEnabled]/singleValue -value true
ixNet commit

puts "Enabling cv negotiation in LDP PW/VPLS"
ixNet setMultiAttr [ixNet getAttr $ldppwvpls1 -enableCCCVNegotiation]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ldppwvpls2 -enableCCCVNegotiation]/singleValue -value true
ixNet commit

puts "Enabling Auto Peer ID in LDP PW/VPLS"
ixNet setAttr $ldppwvpls1 -autoPeerId true
ixNet setAttr $ldppwvpls2 -autoPeerId true
ixNet commit

set labelMultiValue1 [ixNet getAttribute $ldppwvpls1 -label]
ixNet setMultiAttribute $labelMultiValue1\
    -clearOverlays false\
    -pattern counter
ixNet commit

puts "Changing FEC lables in ldppwvpls1 "
set labelSet1 [ixNet add $labelMultiValue1 "counter"]
ixNet setMultiAttribute $labelSet1\
    -step 1\
    -start 300\
    -direction increment
ixNet commit

set labelMultiValue2 [ixNet getAttribute $ldppwvpls2 -label]
ixNet setMultiAttribute $labelMultiValue2\
    -clearOverlays false\
    -pattern counter
ixNet commit

puts "Changing FEC lables in ldppwvpls2 "
set labelSet2 [ixNet add $labelMultiValue2 "counter"]
ixNet setMultiAttribute $labelSet2\
    -step 1\
    -start 400\
    -direction increment
ixNet commit



puts "Adding BGP Peer over IP4 loopback stacks"

ixNet add $ipv4Loopback1 bgpIpv4Peer
ixNet add $ipv4Loopback2 bgpIpv4Peer
ixNet commit

set bgppeer1 [ixNet getList $ipv4Loopback1 bgpIpv4Peer]
set bgppeer2 [ixNet getList $ipv4Loopback2 bgpIpv4Peer]


puts "Assigning DUT IP address on BGP Peer 1"
set addressSet1 [ixNet getAttribute $bgppeer1 -dutIp]
ixNet setMultiAttribute $addressSet1\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet1 [ixNet add $addressSet1 "counter"]
ixNet setMultiAttribute $addressSet1\
    -step 0.0.0.1\
    -start 1.1.1.1\
    -direction increment
ixNet commit


puts "Assigning DUT IP address on BGP Peer 2"
set addressSet1 [ixNet getAttribute $bgppeer2 -dutIp]
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


puts "Adding LDP PW/VPLS over these BGP Peer"

ixNet add $bgppeer1 bgpIpv4AdL2Vpn
ixNet add $bgppeer2 bgpIpv4AdL2Vpn
ixNet commit

set bgpadvpls1 [ixNet getList $bgppeer1 bgpIpv4AdL2Vpn]
set bgpadvpls2 [ixNet getList $bgppeer2 bgpIpv4AdL2Vpn]

puts "Adding Network Group behind each PE routers"
ixNet add $t1dev2 networkGroup
ixNet add $t2dev2 networkGroup
ixNet commit

set networkGroup3 [lindex [ixNet getList $t1dev2 networkGroup] 0]
set networkGroup4 [lindex [ixNet getList $t2dev2 networkGroup] 0]

ixNet setAttr $networkGroup3 -name "MAC_POOL_1"
ixNet setAttr $networkGroup4 -name "MAC_POOL_2"
ixNet commit

puts "Adding MAC pools in Network Groups"
ixNet add $networkGroup3 macPools
ixNet add $networkGroup4 macPools
ixNet commit

set macPools3 [ixNet getList $networkGroup3 macPools]
set macPools4 [ixNet getList $networkGroup4 macPools]

puts "Enabling transport labels on ldp interface"
set root [ixNet getRoot]
set globals [ixNet getList $root globals]
set globalTopo [ixNet getList $globals topology]
set globalLdp [ixNet getList $globalTopo ldpBasicRouter]
ixNet setMultiAttr [ixNet getAttr $globalLdp -transportLabels]/singleValue -value true
ixNet commit

puts "All configuration is completed..Wait for 5 seconds..."
after 5000


################################################################################
# 2. Start LDP protocol and wait for 60 seconds
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
puts "Fetching MPLSOAM Basic Learned Info"
ixNet exec getAllLearnedInfo $mplsoamloop1 1
after 5000
set linfo [ixNet getList $mplsoamloop1 learnedInfo]
ixNet getAttr $linfo -columns
set values [ixNet getAttribute $linfo -values]

puts "***************************************************"
foreach v $values {
        puts $v
}
puts "***************************************************"

################################################################################
# Change the labels of LDPv4 PW/VPLS                                           #
################################################################################
puts "Changing labels of LDPv4 PW/VPLS Range"
set labelMultiValue2 [ixNet getAttribute $ldppwvpls2 -label]
ixNet setMultiAttribute $labelMultiValue2\
    -clearOverlays false\
    -pattern counter
ixNet commit
set labelSet2 [ixNet add $labelMultiValue2 "counter"]
ixNet setMultiAttribute $labelSet2\
    -step 1\
    -start 500\
    -direction increment
ixNet commit
after 2000


################################################################################
# Applying changes one the fly                                                 #
################################################################################
puts "Applying changes on the fly"
set globals [ixNet getRoot]/globals
set topology $globals/topology
ixNet exec applyOnTheFly $topology
after 10000


###############################################################################
# 6. Retrieve protocol learned info again and compare with
#    previouly retrieved learned info.  
###############################################################################
puts "Fetching MPLSOAM Basic Learned Info"
ixNet exec getAllLearnedInfo $mplsoamloop1 1
after 5000
set linfo [ixNet getList $mplsoamloop1 learnedInfo]
ixNet getAttr $linfo -columns
set values [ixNet getAttribute $linfo -values]

puts "***************************************************"
foreach v $values {
        puts $v
}
puts "***************************************************"



################################################################################
# 2. Stop protocol and wait for 15 seconds
################################################################################
puts "Stopping protocols and waiting for 15 seconds for protocols to come up"
ixNet exec stopAllProtocols
after 15000

puts "Changing Target Peer Count in LDP to 0"
ixNet setAttr $ldpTargetedRouterV41 -peerCount 0
ixNet setAttr $ldpTargetedRouterV42 -peerCount 0
ixNet commit


################################################################################
# 2. Start all protocol and wait for 60 seconds
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000


#################################################################################
# Configure L2-L3 traffic                                                       #
#################################################################################
puts "Congfiguring L2-L3 Traffic Item"
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {Traffic Item 1}           \
    -biDirectional true              \
    -roundRobinPacketOrdering false  \
    -trafficType ethernetVlan
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $networkGroup1]
set destination  [list $networkGroup2]

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
# Apply L2/L3 traffic                                                         #
###############################################################################
puts "Applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

###############################################################################
# Start L2/L3 traffic                                                         #
###############################################################################
puts "Starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

puts "Let traffic run for 60 seconds"
after 60000

###############################################################################
# Retrieve L2/L3 traffic item statistics                                      #
###############################################################################
puts "Retrieving all L2/L3 traffic stats"
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
# Stop L2/L3 traffic                                                            #
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# Stop all protocols                                                          #
################################################################################
puts "Stopping all protocols"
ixNet exec stopAllProtocols

puts "!!! Test Script Ends !!!"

