#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    04/09/2015 - Sumeer Kumar - created sample                                #
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
#    This script intends to demonstrate how to use NGPF LDPv6 Low Level TCL API#
#    with FEC128.                                                              #
#                                                                              #
# About Topology:                                                              #
#                                                                              #
#     On each port, it will create one topology of LDPv6 FEC 128.              #
#     In each topology, there will be two device groups and two network groups.#
#     First device group will simulate as a LDP basic P router and other as    #
#     LDPv6 targeted PE router with pseudo wire FEC 128 is configured.         #
#     After first device group, there is one network group in which IPv6 prefix#
#     pools is configured. The other network group has mac pools which is      #
#     simulated as CE router and also is used as traffic end point.            #
#                                                                              #
# Script Flow:                                                                 #
#    1. Configuration of protocols as described in topology.                   #
#    2. Start the LDP protocol.                                                #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Change LDP PW/VPLS labels & apply change on the fly                    #
#    6. Retrieve protocol learned info again.                                  #
#    7. Configure L2-L3 traffic.                                               #
#    8. Start the L2-L3 traffic.                                               #
#   11. Retrieve L2-L3 traffic stats.                                          #
#   12. Stop L2-L3 traffic.                                                    #
#   13. Stopallprotocols.                                                      #
#                                                                              #                                                                                
# Ixia Software:                                                               #
#    IxOS      6.90 EA                                                         #
#    IxNetwork 7.50 EA                                                         #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.205.28.41
    set ixTclPort   8981
    set ports       {{10.205.28.12 6 1} { 10.205.28.12 6 2}}
}

################################################################################
# Load required packages                                                       #
################################################################################
puts "Load IxNetwork Tcl API package"
package req IxTclNetwork

################################################################################
# Connect to IxNetwork TCL server                                              #
################################################################################
puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.40\
    setAttribute strict

################################################################################
# Clean GUI and create a new config                                            #
################################################################################
puts "Creating a new config"
ixNet exec newConfig


################################################################################
# Protocol configuration section                                               #
# Configure LDPv6 as per the description given above                           #
################################################################################ 
puts "Adding two virtual ports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]
set vportRx [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force
after 10000

puts "Adding two topologies"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet add [ixNet getRoot] topology -vports $vportRx
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

puts "Adding one device group in each topology"
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

puts "Adding Ethernet/MAC endpoints for the device groups"
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet commit

set mac1 [ixNet getList $t1dev1 ethernet]
set mac2 [ixNet getList $t2dev1 ethernet]

puts "Configuring the MAC addresses for the device groups"
ixNet setMultiAttr [ixNet getAttr $mac1 -mac]/counter\
    -direction  increment                        \
    -start      {00:11:01:00:00:01}              \
    -step       {00:00:00:00:00:01}

ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\
    -value      {00:12:01:00:00:01}
ixNet commit

puts "Adding IPv6 over Ethernet stack for both device groups"
ixNet add $mac1 ipv6
ixNet add $mac2 ipv6
ixNet commit

set ipv61 [ixNet getList $mac1 ipv6]
set ipv62 [ixNet getList $mac2 ipv6]

set mvAddv61 [ixNet getAttr $ipv61 -address]
set mvAddv62 [ixNet getAttr $ipv62 -address]

set mvGwv61  [ixNet getAttr $ipv61 -gatewayIp]
set mvGwv62  [ixNet getAttr $ipv62 -gatewayIp]


puts "Configuring IPv6 addresses for both device groups"
ixNet setAttr $mvAddv61/singleValue -value "2000:0:0:1:0:0:0:2"
ixNet setAttr $mvAddv62/singleValue -value "2000:0:0:1:0:0:0:1"
ixNet setAttr $mvGwv61/singleValue  -value "2000:0:0:1:0:0:0:1"
ixNet setAttr $mvGwv62/singleValue  -value "2000:0:0:1:0:0:0:2"


puts "Configuring IPv6 prefix for both device groups"
ixNet setAttr [ixNet getAttr $ipv61 -prefix]/singleValue -value 64
ixNet setAttr [ixNet getAttr $ipv62 -prefix]/singleValue -value 64

ixNet setMultiAttr [ixNet getAttr $ipv61 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ipv62 -resolveGateway]/singleValue -value true
ixNet commit

puts "Adding LDPv6 Connected Interface over IPv6 stack"
ixNet add $ipv61 ldpv6ConnectedInterface
ixNet add $ipv62 ldpv6ConnectedInterface
ixNet commit

set ldpv6If1 [ixNet getList $ipv61 ldpv6ConnectedInterface]
set ldpv6If2 [ixNet getList $ipv62 ldpv6ConnectedInterface]

puts "Adding LDPv6 basic router over IPv6 stack"
ixNet add $ipv61 ldpBasicRouterV6
ixNet add $ipv62 ldpBasicRouterV6
ixNet commit

set ldpBasicRouterV61 [ixNet getList $ipv61 ldpBasicRouterV6]
set ldpBasicRouterV62 [ixNet getList $ipv62 ldpBasicRouterV6]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "LDPv6 FEC128 Topology 1"
ixNet setAttr $topo2  -name "LDPv6 FEC128 Topology 2"

ixNet setAttr $t1dev1 -name "P Router 1"
ixNet setAttr $t2dev1 -name "P Router 2"
ixNet commit

puts "Adding Network Group behind LDPv6 dual stack DG"
ixNet add $t1dev1 networkGroup
ixNet add $t2dev1 networkGroup
ixNet commit

set networkGroup1 [lindex [ixNet getList $t1dev1 networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2dev1 networkGroup] 0]

ixNet setAttr $networkGroup1 -name "LDP_1_Network_Group1"
ixNet setAttr $networkGroup2 -name "LDP_2_Network_Group1"
ixNet setAttr $networkGroup1 -multiplier "1"
ixNet setAttr $networkGroup2 -multiplier "1"
ixNet commit

puts "Adding IPv6 prefix pools in Network Groups"
ixNet add $networkGroup1 ipv6PrefixPools
ixNet add $networkGroup2 ipv6PrefixPools
ixNet commit

set ipv6PrefixPools1 [ixNet getList $networkGroup1 ipv6PrefixPools]
set ipv6PrefixPools2 [ixNet getList $networkGroup2 ipv6PrefixPools]

puts "Configuring network address and prefix length of IPv6 prefix pools"
set prefixLength1 [ixNet getAttribute $ipv6PrefixPools1 -prefixLength]
set prefixLength2 [ixNet getAttribute $ipv6PrefixPools2 -prefixLength]
ixNet setMultiAttribute $prefixLength1 \
    -clearOverlays false \
    -pattern singleValue
ixNet setMultiAttribute $prefixLength2 \
    -clearOverlays false \
    -pattern singleValue
ixNet commit
set singleValue1 [ixNet add $prefixLength1 "singleValue"]
set singleValue2 [ixNet add $prefixLength2 "singleValue"]
ixNet setMultiAttribute $singleValue1 -value 128
ixNet setMultiAttribute $singleValue2 -value 128
ixNet commit

set networkAddress1 [ixNet getAttribute $ipv6PrefixPools1 -networkAddress]
set networkAddress2 [ixNet getAttribute $ipv6PrefixPools2 -networkAddress]
ixNet setMultiAttribute $networkAddress1 \
    -clearOverlays false \
    -pattern counter
ixNet setMultiAttribute $networkAddress2 \
    -clearOverlays false \
    -pattern counter
ixNet commit
set counter1 [ixNet add $networkAddress1 "counter"]
set counter2 [ixNet add $networkAddress2 "counter"]
ixNet setMultiAttribute $counter1 \
    -step 0:0:0:0:0:0:0:1 \
    -start 2222:0:0:0:0:0:0:1 \
    -direction increment
ixNet setMultiAttribute $counter2 \
    -step 0:0:0:0:0:0:0:1 \
    -start 2222:0:1:0:0:0:0:1 \
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
ixNet add $t1dev2 ipv6Loopback
ixNet add $t2dev2 ipv6Loopback
ixNet commit

set ipv6Loopback1 [ixNet getList $t1dev2 ipv6Loopback]
set ipv6Loopback2 [ixNet getList $t2dev2 ipv6Loopback]

puts "Adding targeted LDPv6 router over these loopbacks"
ixNet add $ipv6Loopback1 ldpTargetedRouterV6
ixNet add $ipv6Loopback2 ldpTargetedRouterV6
ixNet commit

set ldpTargetedRouterV61 [ixNet getList $ipv6Loopback1 ldpTargetedRouterV6]
set ldpTargetedRouterV62 [ixNet getList $ipv6Loopback2 ldpTargetedRouterV6]

puts "Configuring DUT IP in LDPv6 targeted peers"
set iPAddress1 [ixNet getAttribute $ldpTargetedRouterV61/ldpTargetedIpv6Peer -iPAddress]
set iPAddress2 [ixNet getAttribute $ldpTargetedRouterV62/ldpTargetedIpv6Peer -iPAddress]
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
    -step 0:0:0:0:0:0:0:1 \
    -start 2222:0:1:0:0:0:0:1 \
    -direction increment
ixNet setMultiAttribute $counter2 \
    -step 0:0:0:0:0:0:0:1 \
    -start 2222:0:0:0:0:0:0:1 \
    -direction increment
ixNet commit

puts "Adding LDP PW/VPLS over these targeted routers"
ixNet add $ldpTargetedRouterV61 ldppwvpls
ixNet add $ldpTargetedRouterV62 ldppwvpls
ixNet commit

set ldppwvpls1 [ixNet getList $ldpTargetedRouterV61 ldppwvpls]
set ldppwvpls2 [ixNet getList $ldpTargetedRouterV62 ldppwvpls]

puts "Enabling Auto Peer Address in LDP PW/VPLS"
ixNet setAttr $ldppwvpls1 -autoPeerId true
ixNet setAttr $ldppwvpls2 -autoPeerId true
ixNet commit

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

puts "All configuration is completed..Wait for 5 seconds..."
after 5000

################################################################################
# Start LDPv6 protocol and wait for 60 seconds                                 #  
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000

################################################################################
# Retrieve protocol statistics                                                 #
################################################################################
puts "Fetching LDP Per Port Stats"
set viewPage {::ixNet::OBJ-/statistics/view:"LDP Per Port"/page}
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

#################################################################################
# Retrieve protocol learned info                                                #
#################################################################################
puts "Fetching LDPv6 FEC128 Learned Info"
ixNet exec getFEC128LearnedInfo $ldpTargetedRouterV61
after 5000
set linfoList [ixNet getList $ldpTargetedRouterV61 learnedInfo]
puts "***************************************************"
puts "[ixNet getAttr $linfoList -columns]"
set linfo [lindex $linfoList 0]
set values [ixNet getAttribute $linfo -values]
puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"

################################################################################
# Change the labels of LDPv6 PW/VPLS                                           #
################################################################################
puts "Changing labels of LDPv6 PW/VPLS Range"
set label2 [ixNet getAttribute $ldppwvpls2 -label]
ixNet setMultiAttribute $label2\
    -clearOverlays false\
    -pattern counter
ixNet commit
set counter2 [ixNet add $label2 "counter"]
ixNet setMultiAttribute $counter2\
    -step 10\
    -start 60\
    -direction decrement
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

#################################################################################
# Retrieve protocol learned info again                                          #
#################################################################################
puts "Fetching LDPv6 FEC128 Learned Info again after changing labels on the fly"
ixNet exec getFEC128LearnedInfo $ldpTargetedRouterV61
after 5000
set linfoList [ixNet getList $ldpTargetedRouterV61 learnedInfo]
puts "***************************************************"
puts "[ixNet getAttr $linfoList -columns]"
set linfo [lindex $linfoList 0]
set values [ixNet getAttribute $linfo -values]
puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"

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
