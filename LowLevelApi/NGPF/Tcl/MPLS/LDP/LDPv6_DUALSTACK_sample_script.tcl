#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
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
#    with dual stack router.                                                   #
#                                                                              #
# About Topology:                                                              #
#     On each port, it will create one topology of LDP dual stack router.      #
#     In each topology, there will be one device group and a network group.    #
#     The device group will simulate as a LDP dual stack router having LDP and #
#     LDPv6 interface over IPv4 and IPv6 stack respectively and a basic LDP    #
#     dual stack router connected to both IPv4 and IPv6 interface. The         #
#     transport connection preference in LDP router is set to IPv6.            #
#     The network groups consists of both IPv4 and IPv6 prefix pools.          #
#     Traffic is configured in between IPv6 prefix pools as end points.        #       
#                                                                              #
# Script Flow:                                                                 #
#    1. Configuration of protocols as described in topology.                   #
#    2. Start the LDP protocol.                                                #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Change LDP FEC labels & apply change on the fly                        #
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
    –setAttribute strict

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

puts "Adding IPv4 over Ethernet stack for both device groups"
ixNet add $mac1 ipv4
ixNet add $mac2 ipv4

puts "Adding IPv6 over Ethernet stack for both device groups"
ixNet add $mac1 ipv6
ixNet add $mac2 ipv6
ixNet commit

set ipv41 [ixNet getList $mac1 ipv4]
set ipv42 [ixNet getList $mac2 ipv4]

set ipv61 [ixNet getList $mac1 ipv6]
set ipv62 [ixNet getList $mac2 ipv6]

set mvAddv41 [ixNet getAttr $ipv41 -address]
set mvAddv42 [ixNet getAttr $ipv42 -address]
set mvAddv61 [ixNet getAttr $ipv61 -address]
set mvAddv62 [ixNet getAttr $ipv62 -address]

set mvGwv41  [ixNet getAttr $ipv41 -gatewayIp]
set mvGwv42  [ixNet getAttr $ipv42 -gatewayIp]
set mvGwv61  [ixNet getAttr $ipv61 -gatewayIp]
set mvGwv62  [ixNet getAttr $ipv62 -gatewayIp]


puts "Configuring IPv4 addresses for both device groups"
ixNet setAttr $mvAddv41/singleValue -value "100.1.0.2"
ixNet setAttr $mvAddv42/singleValue -value "100.1.0.1"
ixNet setAttr $mvGwv41/singleValue  -value "100.1.0.1"
ixNet setAttr $mvGwv42/singleValue  -value "100.1.0.2"

puts "Configuring IPv6 addresses for both device groups"
ixNet setAttr $mvAddv61/singleValue -value "2000:0:0:1:0:0:0:2"
ixNet setAttr $mvAddv62/singleValue -value "2000:0:0:1:0:0:0:1"
ixNet setAttr $mvGwv61/singleValue  -value "2000:0:0:1:0:0:0:1"
ixNet setAttr $mvGwv62/singleValue  -value "2000:0:0:1:0:0:0:2"


puts "Configuring IPv4 prefix for both device groups"
ixNet setAttr [ixNet getAttr $ipv41 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ipv42 -prefix]/singleValue -value 24

puts "Configuring IPv6 prefix for both device groups"
ixNet setAttr [ixNet getAttr $ipv61 -prefix]/singleValue -value 64
ixNet setAttr [ixNet getAttr $ipv62 -prefix]/singleValue -value 64

ixNet setMultiAttr [ixNet getAttr $ipv41 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ipv42 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ipv61 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ipv62 -resolveGateway]/singleValue -value true
ixNet commit

puts "Adding LDP Connected Interface over IPv4 stack"
ixNet add $ipv41 ldpConnectedInterface
ixNet add $ipv42 ldpConnectedInterface
ixNet commit

set ldpIf1 [ixNet getList $ipv41 ldpConnectedInterface]
set ldpIf2 [ixNet getList $ipv42 ldpConnectedInterface]

puts "Adding LDPv6 Connected Interface over IPv6 stack"
ixNet add $ipv61 ldpv6ConnectedInterface
ixNet add $ipv62 ldpv6ConnectedInterface
ixNet commit

set ldpv6If1 [ixNet getList $ipv61 ldpv6ConnectedInterface]
set ldpv6If2 [ixNet getList $ipv62 ldpv6ConnectedInterface]

puts "Adding LDPv6 dual stack router in both device groups"
ixNet add $t1dev1 ldpBasicRouterV6
ixNet add $t2dev1 ldpBasicRouterV6
ixNet commit

set ldpv6DualStackRouter1 [ixNet getList $t1dev1 ldpBasicRouterV6]
set ldpv6DualStackRouter2 [ixNet getList $t2dev1 ldpBasicRouterV6]

ixNet setAttribute $ipv41 -stackedLayers [list $ldpv6DualStackRouter1]
ixNet setAttribute $ipv61 -stackedLayers [list $ldpv6DualStackRouter1]

ixNet setAttribute $ipv42 -stackedLayers [list $ldpv6DualStackRouter2]
ixNet setAttribute $ipv62 -stackedLayers [list $ldpv6DualStackRouter2]
ixNet commit

puts "Setting IPv6 as transport connection preference"
set sessionPreference1 [ixNet getAttr $ldpv6DualStackRouter1 -sessionPreference]
set sessionPreference2 [ixNet getAttr $ldpv6DualStackRouter2 -sessionPreference]
set singleValue1 [ixNet getList $sessionPreference1 singleValue]
set singleValue2 [ixNet getList $sessionPreference2 singleValue]
ixNet setAttr $singleValue1 -value ipv6
ixNet setAttr $singleValue2 -value ipv6
ixNet commit

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "LDPv6 Topology 1"
ixNet setAttr $topo2  -name "LDPv6 Topology 2"

ixNet setAttr $t1dev1 -name "LDP Dual Stack Router 1"
ixNet setAttr $t2dev1 -name "LDP Dual Stack Router 2"
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

puts "Adding IPv4 and Ipv6 prefix pools in Network Groups"
ixNet add $networkGroup1 ipv6PrefixPools
ixNet add $networkGroup1 ipv4PrefixPools
ixNet add $networkGroup2 ipv6PrefixPools
ixNet add $networkGroup2 ipv4PrefixPools
ixNet commit

set ipv6PrefixPools1 [ixNet getList $networkGroup1 ipv6PrefixPools]
set ipv4PrefixPools1 [ixNet getList $networkGroup1 ipv4PrefixPools]
set ipv6PrefixPools2 [ixNet getList $networkGroup2 ipv6PrefixPools]
set ipv4PrefixPools2 [ixNet getList $networkGroup2 ipv4PrefixPools]

puts "Changing count of network group address"
ixNet setMultiAttribute $ipv6PrefixPools1 -numberOfAddresses 5
ixNet setMultiAttribute $ipv4PrefixPools1 -numberOfAddresses 5
ixNet setMultiAttribute $ipv6PrefixPools2 -numberOfAddresses 5
ixNet setMultiAttribute $ipv4PrefixPools2 -numberOfAddresses 5
ixNet commit

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
puts "Fetching LDPv6 Basic Learned Info"
ixNet exec getIPv4FECLearnedInfo $ldpv6DualStackRouter1
ixNet exec getIPv6FECLearnedInfo $ldpv6DualStackRouter1
after 5000
set linfoList [ixNet getList $ldpv6DualStackRouter1 learnedInfo]
puts "***************************************************"
puts "[ixNet getAttr $linfoList -columns]"
for {set i 0} {$i < 2} {incr i} {
    set linfo [lindex $linfoList $i]
    set values [ixNet getAttribute $linfo -values]
    puts "***************************************************"
    foreach v $values {
        puts $v
    }
}    
puts "***************************************************"

################################################################################
# Change the labels of FEC elements                                            #
################################################################################
puts "Changing Labels of LDP and LDPv6 FEC Range on second Network Group"
set ldpFEC2 [lindex [ixNet getList $ipv4PrefixPools2 ldpFECProperty] 0]
set ldpv6FEC2 [lindex [ixNet getList $ipv6PrefixPools2 ldpIpv6FECProperty] 0]

set labelV4MultiValue2 [ixNet getAttribute $ldpFEC2 -labelValue]
set labelV6MultiValue2 [ixNet getAttribute $ldpv6FEC2 -labelValue]
ixNet setMultiAttribute $labelV4MultiValue2\
    -clearOverlays false\
    -pattern counter
ixNet commit
set labelSetV4 [ixNet add $labelV4MultiValue2 "counter"]
ixNet setMultiAttribute $labelSetV4\
    -step 5\
    -start 30\
    -direction increment

ixNet setMultiAttribute $labelV6MultiValue2\
    -clearOverlays false\
    -pattern counter
ixNet commit
set labelSetV6 [ixNet add $labelV6MultiValue2 "counter"]
ixNet setMultiAttribute $labelSetV6\
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
puts "Fetching LDPv6 Basic Learned Info again after changing labels on the fly"
ixNet exec getIPv4FECLearnedInfo $ldpv6DualStackRouter1
ixNet exec getIPv6FECLearnedInfo $ldpv6DualStackRouter1
after 5000
set linfoList [ixNet getList $ldpv6DualStackRouter1 learnedInfo]
puts "***************************************************"
puts "[ixNet getAttr $linfoList -columns]"
for {set i 0} {$i < 2} {incr i} {
    set linfo [lindex $linfoList $i]
    set values [ixNet getAttribute $linfo -values]
    puts "***************************************************"
    foreach v $values {
        puts $v
    }
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
    -trafficType ipv6
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $networkGroup1/ipv6PrefixPools:1]
set destination  [list $networkGroup2/ipv6PrefixPools:1]


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
