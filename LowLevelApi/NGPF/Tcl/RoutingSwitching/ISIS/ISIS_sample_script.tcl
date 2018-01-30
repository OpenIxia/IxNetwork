#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/10/2014 - Poulomi Chatterjee - created sample                          #
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
#    This script intends to demonstrate how to use NGPF ISIS API.              #
#                                                                              #
#    1. It will create 2 ISIS topologies, each having an ipv4 and ipv6 network #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. A loopback device group(DG) behind network   # 
#       group is needed to support applib traffic.                             #
#    2. Start the ISIS protocol.                                               #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. i)Enable ISISL3 simulated topology's Simulated IPv4 & v6 Node Routes,  #
#        which was disabled by default and apply change on the fly.            #
#       ii) Stop ISIS Routers on the fly.                                      #
#       iii) Again Start ISIS Routers on the fly.                              #
#    6. Retrieve protocol learned info again and notice the difference with    #
#       previouly retrieved learned info.                                      #
#    7. Configure L2-L3 traffic.                                               #
#    8. Configure IPv4 application traffic.[application Traffic type is set    #
#       using variable "trafficType". "ipv4ApplicationTraffic" for ipv4 profile#
#       and "ipv6ApplicationTraffic" for ipv6 profile.                         #
#    9. Start the L2-L3 traffic.                                               #
#   10. Start the IPV4 application traffic.                                    #
#   11. Retrieve Appilcation traffic stats.                                    #
#   12. Retrieve L2-L3 traffic stats.                                          #
#   13. Stop L2-L3 traffic.                                                    #
#   14. Stop Application traffic.                                              #
#   15. Stop all protocols.                                                    #                                                                                          
# Ixia Softwares:                                                              #
#    IxOS      6.80 EB                                                         #
#    IxNetwork 7.40 EB                                                         #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.205.28.41
    set ixTclPort   8067
    set ports       {{10.205.28.170 1  5} { 10.205.28.170 1  6}}
}

# Variable named trafficType sets type of application traffic to be configured.
# "ipv4ApplicationTraffic" for ipv4 profile & "ipv6ApplicationTraffic" for ipv6 profile.
set trafficType "ipv6ApplicationTraffic"

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.40 -setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
#  Protocol configuration section. Configure ISIS as per the description
#  give above
################################################################################ 
# Adding Virtual ports 
puts "Adding 2 Vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]
set vportRx [lindex $vPorts 1]

puts "Assigning the Ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

# Adding topologies
puts "Adding 2 Topologies"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet add [ixNet getRoot] topology -vports $vportRx
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

# Adding Device Groups
puts "Adding 2 Device Groups"
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

# Adding Ethernet
puts "Adding Ethernet/mac endpoints"
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

puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet]"

# Adding ipv4
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
ixNet setAttr $mvAdd1/singleValue -value "11.1.1.1"
ixNet setAttr $mvAdd2/singleValue -value "11.1.1.2"
ixNet setAttr $mvGw1/singleValue  -value "11.1.1.2"
ixNet setAttr $mvGw2/singleValue  -value "11.1.1.1"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4]"

# Adding ISIS over Ethernet stack 
puts "Adding ISISL3 over Ethernet stacks"
ixNet add $mac1 isisL3
ixNet add $mac2 isisL3
ixNet commit

set isisL3_1 [ixNet getList $mac1 isisL3]
set isisL3_2 [ixNet getList $mac2 isisL3]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "ISIS Topology 1"
ixNet setAttr $topo2  -name "ISIS Topology 2"

ixNet setAttr $t1dev1 -name "ISIS Topology 1 Router"
ixNet setAttr $t2dev1 -name "ISIS Topology 2 Router"
ixNet commit

# Enable host name in ISIS routers
puts "Enabling Host name in Emulated ISIS Routers"
set isisL3Router1 [ixNet getList [ixNet getList $topo1 deviceGroup] isisL3Router]
set enableHostName1 [ixNet getAttr $isisL3Router1 -enableHostName]
ixNet setAttr $enableHostName1/singleValue -value True
ixNet commit
set configureHostName1 [ixNet getAttr $isisL3Router1 -hostName]
ixNet setAttr $configureHostName1/singleValue -value "isisL3Router1"
ixNet commit

set isisL3Router2 [ixNet getList [ixNet getList $topo2 deviceGroup] isisL3Router]
set enableHostName2 [ixNet getAttr $isisL3Router2 -enableHostName]
ixNet setAttr $enableHostName2/singleValue -value True
ixNet commit
set configureHostName2 [ixNet getAttr $isisL3Router2 -hostName]
ixNet setAttr $configureHostName2/singleValue -value "isisL3Router2"
ixNet commit

puts "Making the NetworkType to Point to Point in the first ISIS router"
set networkTypeMultiValue1 [ixNet getAttr $isisL3_1 -networkType]
ixNet setAttr $networkTypeMultiValue1 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue1/singleValue -value pointpoint

puts "Making the NetworkType to Point to Point in the Second ISIS router"
set networkTypeMultiValue2 [ixNet getAttr $isisL3_2 -networkType]
ixNet setAttr $networkTypeMultiValue2 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue2/singleValue -value pointpoint

# Disable Discard Learned LSP 
puts "Disabling the Discard Learned Info CheckBox"

set isisL3RouterDiscardLearnedLSP1 [ ixNet getAttr [ixNet getList [ixNet getList $topo1 deviceGroup] isisL3Router] -discardLSPs]
set isisL3RouterDiscardLearnedLSP2 [ ixNet getAttr [ixNet getList [ixNet getList $topo2 deviceGroup] isisL3Router] -discardLSPs]

ixNet setAttr $isisL3RouterDiscardLearnedLSP1 -pattern singleValue -clearOverlays False
ixNet setAttr $isisL3RouterDiscardLearnedLSP1/singleValue -value False
ixNet setAttr $isisL3RouterDiscardLearnedLSP2 -pattern singleValue -clearOverlays False
ixNet setAttr $isisL3RouterDiscardLearnedLSP2/singleValue -value False

# Adding Network group behind DeviceGroup
puts "Adding NetworkGroup behind ISIS DG"
ixNet exec createDefaultStack $t1devices networkTopology
ixNet exec createDefaultStack $t2devices networkTopology

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

ixNet setAttr $networkGroup1 -name "ISIS_1_Network_Group1"
ixNet setAttr $networkGroup2 -name "ISIS_2_Network_Group1"
ixNet commit

# Enabling Host name in Simulated ISIS Routers
puts "Enabling Host name in Simulated ISIS Routers"
set networkTopology1      [lindex [ixNet getList $networkGroup1 networkTopology] 0]
set isisL3SimulatedTopologyConfig1 [ixNet getList $networkTopology1 isisL3SimulatedTopologyConfig]
set enableHostName1 [ixNet getAttr $isisL3SimulatedTopologyConfig1 -enableHostName]
ixNet setAttr $enableHostName1/singleValue -value True
ixNet commit
set configureHostName1 [ixNet getAttr $isisL3SimulatedTopologyConfig1 -hostName]
ixNet setAttr $configureHostName1/singleValue -value "isisL3SimulatedRouter1"
ixNet commit

set networkTopology2      [lindex [ixNet getList $networkGroup2 networkTopology] 0]
set isisL3SimulatedTopologyConfig2 [ixNet getList $networkTopology2 isisL3SimulatedTopologyConfig]
set enableHostName2 [ixNet getAttr $isisL3SimulatedTopologyConfig2 -enableHostName]
ixNet setAttr $enableHostName2/singleValue -value True
ixNet commit
set configureHostName2 [ixNet getAttr $isisL3SimulatedTopologyConfig2 -hostName]
ixNet setAttr $configureHostName2/singleValue -value "isisL3SimulatedRouter2"
ixNet commit

# Add ipv4 loopback1 for applib traffic
puts "Adding ipv4 loopback1 for applib traffic"
set chainedDg1 [ixNet add $networkGroup1 deviceGroup]
ixNet setMultiAttribute $chainedDg1\
    -multiplier 7\
    -name {Device Group 4}
ixNet commit
set chainedDg1 [lindex [ixNet remapIds $chainedDg1] 0]

set loopback1 [ixNet add $chainedDg1 "ipv4Loopback"]
ixNet setMultiAttribute $loopback1\
    -stackedLayers [list]\
    -name {IPv4 Loopback 2}
ixNet commit

set connector1 [ixNet add $loopback1 "connector"]
ixNet setMultiAttribute $connector1\
    -connectedTo $networkGroup1/networkTopology/simRouter:1
ixNet commit
set connector1 [lindex [ixNet remapIds $connector1] 0]

set addressSet1 [ixNet getAttribute $loopback1 -address]
ixNet setMultiAttribute $addressSet1\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet1 [ixNet add $addressSet1 "counter"]
ixNet setMultiAttribute $addressSet1\
    -step 0.1.0.0\
    -start 201.1.0.0\
    -direction increment
ixNet commit
set addressSet1 [lindex [ixNet remapIds $addressSet1] 0]

# Add ipv4 loopback2 for applib traffic
puts "Adding ipv4 loopback2 for applib traffic"
set chainedDg2 [ixNet add $networkGroup2 deviceGroup]
ixNet setMultiAttribute $chainedDg2\
    -multiplier 7\
    -name {Device Group 3}
ixNet commit
set chainedDg2 [lindex [ixNet remapIds $chainedDg2] 0]

set loopback2 [ixNet add $chainedDg2 "ipv4Loopback"]
ixNet setMultiAttribute $loopback2\
    -stackedLayers [list]\
    -name {IPv4 Loopback 1}
ixNet commit

set connector2 [ixNet add $loopback2 "connector"]
ixNet setMultiAttribute $connector2\
    -connectedTo $networkGroup2/networkTopology/simRouter:1
ixNet commit
set connector1 [lindex [ixNet remapIds $connector2] 0]

set addressSet2 [ixNet getAttribute $loopback2 -address]
ixNet setMultiAttribute $addressSet2\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet2 [ixNet add $addressSet2 "counter"]
ixNet setMultiAttribute $addressSet2\
    -step 0.1.0.0\
    -start 206.1.0.0\
    -direction increment
ixNet commit
set addressSet2 [lindex [ixNet remapIds $addressSet2] 0]

# Add ipv6 loopback1 for applib traffic
puts "Adding ipv6 loopback1 for applib traffic"
set chainedDg3 [ixNet add $networkGroup1 deviceGroup]
ixNet setMultiAttribute $chainedDg3\
    -multiplier 7\
    -name {Device Group 6}
ixNet commit
set chainedDg3 [lindex [ixNet remapIds $chainedDg3] 0]

set loopback1 [ixNet add $chainedDg3 "ipv6Loopback"]
ixNet setMultiAttribute $loopback1\
    -stackedLayers [list]\
    -name {IPv6 Loopback 2}
ixNet commit

set connector1 [ixNet add $loopback1 "connector"]
ixNet setMultiAttribute $connector1\
    -connectedTo $networkGroup1/networkTopology/simRouter:1
ixNet commit
set connector1 [lindex [ixNet remapIds $connector1] 0]

set addressSet1 [ixNet getAttribute $loopback1 -address]
ixNet setMultiAttribute $addressSet1\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet1 [ixNet add $addressSet1 "counter"]
ixNet setMultiAttribute $addressSet1\
    -step ::1\
    -start 2010::1\
    -direction increment
ixNet commit
set addressSet1 [lindex [ixNet remapIds $addressSet1] 0]

# Add ipv6 loopback2 for applib traffic
puts "Adding ipv6 loopback2 for applib traffic"
set chainedDg4 [ixNet add $networkGroup2 deviceGroup]
ixNet setMultiAttribute $chainedDg4\
    -multiplier 7\
    -name {Device Group 5}
ixNet commit
set chainedDg4 [lindex [ixNet remapIds $chainedDg4] 0]

set loopback2 [ixNet add $chainedDg4 "ipv6Loopback"]
ixNet setMultiAttribute $loopback2\
    -stackedLayers [list]\
    -name {IPv6 Loopback 1}
ixNet commit

set connector2 [ixNet add $loopback2 "connector"]
ixNet setMultiAttribute $connector2\
    -connectedTo $networkGroup2/networkTopology/simRouter:1
ixNet commit
set connector1 [lindex [ixNet remapIds $connector2] 0]

set addressSet2 [ixNet getAttribute $loopback2 -address]
ixNet setMultiAttribute $addressSet2\
    -clearOverlays false\
    -pattern counter
ixNet commit
set addressSet2 [ixNet add $addressSet2 "counter"]
ixNet setMultiAttribute $addressSet2\
    -step ::1\
    -start 2060::1\
    -direction increment
ixNet commit
set addressSet2 [lindex [ixNet remapIds $addressSet2] 0]

################################################################################
# Start ISISL3 protocol and wait for 60 seconds
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000

################################################################################
# Retrieve protocol statistics.
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
# Retrieve protocol learned info
###############################################################################
puts "Fetching ISISL3 Basic Learned Info"
ixNet exec getLearnedInfo $isisL3_1 1
after 5000
set linfo [ixNet getList $isisL3_1 learnedInfo]
set values [ixNet getAttribute $linfo -values]

puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"


################################################################################
# Enable ISISL3 simulated topology's ISIS Simulated IPv4 & IPv6 Node Routes,
#  which was disabled by default. And apply changes On The Fly (OTF).
################################################################################
puts "Enabling IPv4  IPv6 Simulated Node Routes"

set simRouter1        [lindex [ixNet getList $networkTopology1 simRouter] 0]
set isisL3PseudoRouter1 [ixNet getList $simRouter1 isisL3PseudoRouter]
set ipv4PseudoNodeRoutes1 [ixNet getList $isisL3PseudoRouter1 IPv4PseudoNodeRoutes]
set ipv4PseudoNodeRouteMultivalue [ixNet getAttribute $ipv4PseudoNodeRoutes1 -active]
ixNet setAttribute $ipv4PseudoNodeRouteMultivalue/singleValue -value true
set ipv6PseudoNodeRoutes1 [ixNet getList $isisL3PseudoRouter1 IPv6PseudoNodeRoutes]
set ipv6PseudoNodeRouteMultivalue [ixNet getAttribute $ipv6PseudoNodeRoutes1 -active]
ixNet setAttribute $ipv6PseudoNodeRouteMultivalue/singleValue -value true
ixNet commit

set simRouter2        [lindex [ixNet getList $networkTopology2 simRouter] 0]
set isisL3PseudoRouter2 [ixNet getList $simRouter2 isisL3PseudoRouter]
set ipv4PseudoNodeRoutes2 [ixNet getList $isisL3PseudoRouter2 IPv4PseudoNodeRoutes]
set ipv4PseudoNodeRouteMultivalue [ixNet getAttribute $ipv4PseudoNodeRoutes2 -active]
ixNet setAttribute $ipv4PseudoNodeRouteMultivalue/singleValue -value true
set ipv6PseudoNodeRoutes2 [ixNet getList $isisL3PseudoRouter2 IPv6PseudoNodeRoutes]
set ipv6PseudoNodeRouteMultivalue [ixNet getAttribute $ipv6PseudoNodeRoutes2 -active]
ixNet setAttribute $ipv6PseudoNodeRouteMultivalue/singleValue -value true
ixNet commit

################################################################################
# Stop/Start ISIS Router on both ports and apply changes on-the-fly
################################################################################
puts "Stop ISIS Router on both ports and apply changes on-the-fly"
set isisL3RouterDeactivate1 [ ixNet getAttr [ixNet getList [ixNet getList $topo1 deviceGroup] isisL3Router] -active]
set isisL3RouterDeactivate2 [ ixNet getAttr [ixNet getList [ixNet getList $topo2 deviceGroup] isisL3Router] -active]

ixNet setAttr $isisL3RouterDeactivate1 -pattern singleValue -clearOverlays False
ixNet setAttr $isisL3RouterDeactivate1/singleValue -value False
ixNet setAttr $isisL3RouterDeactivate2 -pattern singleValue -clearOverlays False
ixNet setAttr $isisL3RouterDeactivate2/singleValue -value False
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
puts "Applying changes on the fly"
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
    puts "$::errorInfo"
}
puts "Wait for 30 seconds..."
after 30000

################################################################################
# Start ISIS Router on both ports and apply changes on-the-fly
################################################################################
puts "Start ISIS Router on both ports and apply changes on-the-fly"
set isisL3RouterActivate1 [ ixNet getAttr [ixNet getList [ixNet getList $topo1 deviceGroup] isisL3Router] -active]
set isisL3RouterActivate2 [ ixNet getAttr [ixNet getList [ixNet getList $topo2 deviceGroup] isisL3Router] -active]

ixNet setAttr $isisL3RouterDeactivate1 -pattern singleValue -clearOverlays True
ixNet setAttr $isisL3RouterDeactivate1/singleValue -value True
ixNet setAttr $isisL3RouterDeactivate2 -pattern singleValue -clearOverlays True
ixNet setAttr $isisL3RouterDeactivate2/singleValue -value True
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
puts "Applying changes on the fly"
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
    puts "$::errorInfo"
}
puts "Wait for 30 seconds..."
after 30000

###############################################################################
# Retrieve protocol learned info again and compare with
#  previouly retrieved learned info.  
###############################################################################
after 10000
puts "Fetching ISISL3 learned info after enabling IPv4 & IPv6 Node Routes\n"
ixNet exec getLearnedInfo $isisL3_2 1
after 5000
set linfo [ixNet getList $isisL3_2 learnedInfo]
set values [ixNet getAttribute $linfo -values]
puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"

puts "Fetching ISISL3 IPv6 Learned Info"
ixNet exec getLearnedInfo $isisL3_1 1
after 5000
set learnedInfoMV1 [ixNet getList $isisL3_1 learnedInfo]
foreach linfo $learnedInfoMV1 {
     set tables [ixNet getList $linfo table]
     set ipv6table [lindex $tables 1]
     set values [ixNet getAttr $ipv6table -values]
}

puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"

################################################################################
# Configure L2-L3 traffic 
################################################################################
#Configuring L2-L3 IPv4 Traffic Item"
puts "Configuring L2-L3 IPv4 Traffic Item\n"
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {Traffic Item 1}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv4
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source1       [list $networkGroup1/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv4PseudoNodeRoutes:1]
set destination1  [list $networkGroup2/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv4PseudoNodeRoutes:1]

ixNet setMultiAttribute $endpointSet1\
    -name                  "EndpointSet-1"\
    -multicastDestinations [list]\
    -scalableSources       [list]\
    -multicastReceivers    [list]\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               $source1\
    -destinations          $destination1\    
ixNet commit

ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy        [list sourceDestEndpointPair0 trackingenabled0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]

ixNet commit

# Configuring L2-L3 IPv6 Traffic Item
puts "Configuring L2-L3 IPv6 Traffic Item\n"
set trafficItem2 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem2\
    -name {Traffic Item 2}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv6
ixNet commit

set trafficItem2 [lindex [ixNet remapIds $trafficItem2] 0]
set endpointSet1 [ixNet add $trafficItem2 "endpointSet"]
set source2       [list $networkGroup1/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1]
set destination2  [list $networkGroup2/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1]

ixNet setMultiAttribute $endpointSet1\
    -name                  "EndpointSet-1"\
    -multicastDestinations [list]\
    -scalableSources       [list]\
    -multicastReceivers    [list]\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               $source2\
    -destinations          $destination2
ixNet commit

ixNet setMultiAttribute $trafficItem2/tracking\
    -trackBy        [list sourceDestEndpointPair0 trackingenabled0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]

ixNet commit

puts "Configured L2-L3 IPv4 & IPv6 Traffic Item\n"
################################################################################
# Configure Application traffic
################################################################################
# Configuring Applib traffic
puts "Configuring Applib traffic, type: trafficType"
set trafficItem2 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem2  \
    -name {Traffic Item 3}             \
    -trafficItemType applicationLibrary\
    -roundRobinPacketOrdering false    \
    -trafficType $trafficType
ixNet commit
set trafficItem2 [lindex [ixNet remapIds $trafficItem2] 0]

set endpointSet2 [ixNet add $trafficItem2 "endpointSet"]
set source_app [list [lindex [ixNet getList $t1dev1 networkGroup] 0]]
set destin_app [list [lindex [ixNet getList $t2dev1 networkGroup] 0]]

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

puts "ixNet help [ixNet getRoot]/traffic"

###############################################################################
# Apply and start L2/L3 traffic
###############################################################################
puts "Applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "Starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

###############################################################################
# Apply and start applib traffic
###############################################################################
puts "Applying IPv4 applib traffic"
ixNet exec applyStatefulTraffic  [ixNet getRoot]/traffic
after 5000

puts "Starting IPv4 applib traffic"
ixNet exec startStatefulTraffic [ixNet getRoot]/traffic
puts "Let traffic run for 1 minute"
after 60000

###############################################################################
# Retrieve Applib traffic item statistics
###############################################################################
puts "Verifying all the applib traffic stats\n"
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

###############################################################################
# Retrieve L2/L3 traffic item statistics
###############################################################################
puts "Verifying all the L2-L3 traffic stats\n"
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

################################################################################
# Stop applib traffic
#################################################################################
puts "Stopping applib traffic"
ixNet exec stopStatefulTraffic [ixNet getRoot]/traffic
after 5000

################################################################################
# Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
