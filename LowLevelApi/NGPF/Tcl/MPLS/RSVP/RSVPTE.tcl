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
#    This script intends to demonstrate how to use NGPF RSVPTE API              #
#    About Topology:                                                            #
#       Within topology both Label Switch Router(LSR) and Label Edge Router(LER)#
#    are created. LSR is emulated in the front Device Group(DG), which consists #
#    of both OSPF as routing protocol as well as RSVPTE-IF for Label            # 
#    Distribution Protocol. The chained DG act as LER, where RSVP-TE LSPs are   #
#    configured. Unidirectional L2-L3 Traffic from Ingress to Egress is created.#
#         Script Flow:                                                          #
#        Step 1. Configuration of protocols.                                    #
#    Configuration flow of the script is as follow:                             #
#             i.      Adding of OSPF router                                     #
#             ii.     Adding of Network Topology(NT)                            #
#             iii.    Enabling of TE(Traffic Engineering)                       #
#             iv.     Adding of chain DG                                        #
#             v.      Adding of RSVPTE-IF                                       #
#             vi.     Adding of RSVP-TE LSPs within chain DG                    #
#        Step 2. Start of protocol                                              #
#        Step 3. Protocol Stat display                                          #
#        Step 4. Learned Info display                                           #
#        Step 5. On The Fly(OTF) change of protocol parameter.                  #
#        Step 6. Again Learned Info display to see OTF changes take place       #
#        Step 7. Configuration L2-L3 Traffic                                    #
#        Step 8. Apply and Start of L2-L3 traffic                               #
#        Step 9. Display of L2-L3  traffic Stats                                #
#        Step 10.Stop of L2-L3 traffic                                          #
#        Step 11.Stop of all protocols                                          #
#################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.216.108.49
    set ixTclPort   8999
    set ports       {{10.216.102.209 1 3} { 10.216.102.209 1 4}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Disconnecting if any already connected"
ixNet disconnect $::ixia::ixTclServer

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.40\
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
ixNet setAttr $topo1  -name "RSVPTE Topology 1"
ixNet setAttr $topo2  -name "RSVPTE Topology 2"

set t1dev1 [lindex $t1devices 0]
set t2dev1 [lindex $t2devices 0]
ixNet setAttr $t1dev1 -name "Label Switch Router 1"
ixNet setAttr $t2dev1 -name "Label Switch Router 2"
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
#  Adding IPv4 stack and configuring  IP Address
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
ixNet setAttr $mvAdd1/singleValue -value "50.50.50.2"
ixNet setAttr $mvAdd2/singleValue -value "50.50.50.1"
ixNet setAttr $mvGw1/singleValue  -value "50.50.50.1"
ixNet setAttr $mvGw2/singleValue  -value "50.50.50.2"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 26
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 26

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit
#  Adding OSPF and configuring it
puts "Adding OSPFv2 over IP4 stack"
ixNet add $ip1 ospfv2
ixNet add $ip2 ospfv2
ixNet commit
set ospf1 [ixNet getList $ip1 ospfv2]
set ospf2 [ixNet getList $ip2 ospfv2]
puts "Making the NetworkType to Point to Point in the first OSPF router"
set networkTypeMultiValue1 [ixNet getAttr $ospf1 -networkType]
ixNet setAttr $networkTypeMultiValue1 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue1/singleValue -value pointtopoint
ixNet commit

puts "Making the NetworkType to Point to Point in the Second OSPF router"
set networkTypeMultiValue2 [ixNet getAttr $ospf2 -networkType]
ixNet setAttr $networkTypeMultiValue2 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue2/singleValue -value pointtopoint
ixNet commit

puts "Disabling the Discard Learned Info CheckBox"
set ospfv2RouterDiscardLearnedLSA1\
    [ixNet getAttr [lindex [ixNet getList $t1devices ospfv2Router] 0] -discardLearnedLsa]
set ospfv2RouterDiscardLearnedLSA2\
    [ixNet getAttr [lindex [ixNet getList $t2devices ospfv2Router] 0] -discardLearnedLsa]

ixNet setAttr $ospfv2RouterDiscardLearnedLSA1 -pattern singleValue -clearOverlays False
ixNet setAttr $ospfv2RouterDiscardLearnedLSA1/singleValue -value False
ixNet setAttr $ospfv2RouterDiscardLearnedLSA2 -pattern singleValue -clearOverlays False
ixNet setAttr $ospfv2RouterDiscardLearnedLSA2/singleValue -value False

# Adding Network Topology behind Device Group
puts "Adding the Network Topology"
ixNet exec createDefaultStack $t1devices networkTopology
ixNet exec createDefaultStack $t2devices networkTopology

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

ixNet setAttr $networkGroup1 -name "Network Topology 1"
ixNet setAttr $networkGroup2 -name "Network Topology 2"
ixNet commit

set netTopo1 [ixNet getList $networkGroup1 networkTopology]
set netTopo2 [ixNet getList $networkGroup2 networkTopology]

# Configuring Traffic Engineering
puts "Enabling Traffic Engineering in Network Topology 1"
set simInterface1 [ixNet getList $netTopo1 simInterface]
set simInterfaceIPv4Config1 [ixNet getList $simInterface1 simInterfaceIPv4Config]

set ospfPseudoInterface1 [ixNet getList $simInterfaceIPv4Config1 ospfPseudoInterface]

set ospfPseudoInterface1_teEnable [ixNet getAttribute $ospfPseudoInterface1 -enable]
ixNet setMultiAttribute $ospfPseudoInterface1_teEnable \
                        -clearOverlays false           \
                        -pattern singleValue
ixNet commit
ixNet setMultiAttribute $ospfPseudoInterface1_teEnable/singleValue -value true
ixNet commit

puts "Enabling Traffic Engineering in Network Topology 2"
set simInterface2 [ixNet getList $netTopo2 simInterface]
set simInterfaceIPv4Config2 [ixNet getList $simInterface2 simInterfaceIPv4Config]
set ospfPseudoInterface2 [ixNet getList $simInterfaceIPv4Config2 ospfPseudoInterface]
set ospfPseudoInterface2_teEnable [ixNet getAttribute $ospfPseudoInterface2 -enable]
ixNet setMultiAttribute $ospfPseudoInterface2_teEnable \
                        -clearOverlays false           \
                        -pattern singleValue
ixNet commit
ixNet setMultiAttribute $ospfPseudoInterface2_teEnable/singleValue -value true
ixNet commit        
# Adding Chained Device Group Behind front Device Group for IPv4 loopback
puts "Adding Chained DG behind Network Topology in Topoloy 1"
set chainedDg1 [ixNet add $networkGroup1 deviceGroup]
ixNet commit
set chainedDg1 [lindex [ixNet remapIds $chainedDg1] 0]
ixNet setMultiAttribute $chainedDg1\
    -multiplier 1                  \
        -name {Edge Router 1}
ixNet commit
set loopback1 [ixNet add $chainedDg1 "ipv4Loopback"]
ixNet setMultiAttribute $loopback1\
    -stackedLayers [list]         \
    -name {IPv4 Loopback 2}
ixNet commit
puts "Adding Chained DG behind Network Topology in Topoloy 2"
set chainedDg2 [ixNet add $networkGroup2 deviceGroup]
ixNet setMultiAttribute $chainedDg2\
    -multiplier 1                  \
        -name {Edge Router 2}
ixNet commit
set chainedDg2 [lindex [ixNet remapIds $chainedDg2] 0]

set loopback2 [ixNet add $chainedDg2 "ipv4Loopback"]
ixNet setMultiAttribute $loopback2\
    -stackedLayers [list]         \
    -name {IPv4 Loopback 1}
ixNet commit
puts "Creating  Connector in betwwen Network Toplogy and Chained DG for Topology1"
set connector1 [ixNet add $loopback1 "connector"]
ixNet setMultiAttribute $connector1\
    -connectedTo $networkGroup1/networkTopology/simRouter:1
ixNet commit
set connector1 [lindex [ixNet remapIds $connector1] 0]
puts "Creating  Connector in betwwen Network Toplogy and Chained DG for Topology1"
set connector2 [ixNet add $loopback2 "connector"]
ixNet setMultiAttribute $connector2\
    -connectedTo $networkGroup2/networkTopology/simRouter:1
ixNet commit
set connector1 [lindex [ixNet remapIds $connector2] 0]

puts "Adding RSVPTE over IP4 stack"
ixNet add $ip1 rsvpteIf
ixNet add $ip2 rsvpteIf
ixNet commit
set rsvpte1 [ixNet getList $ip1 rsvpteIf]
set rsvpte2 [ixNet getList $ip2 rsvpteIf]
puts "Changing Label Value for first RSVPTE router to single value"
set labelSpaceStartMultValue1 [ixNet getAttr $rsvpte1 -labelSpaceStart]
ixNet setAttr $labelSpaceStartMultValue1 -pattern singleValue -clearOverlays False
ixNet setAttr $labelSpaceStartMultValue1/singleValue -value 5001
ixNet commit
puts "Changing Label Value for second RSVPTE router to increment mode"
ixNet setMultiAttr [ixNet getAttr $rsvpte2 -labelSpaceStart]/counter\
        -direction  increment         \
        -start      7001              \
        -step       1
ixNet commit
puts "Changing Label Space End for first RSVPTE router to single value"
set labelSpaceEndMultValue1 [ixNet getAttr $rsvpte1 -labelSpaceEnd]
ixNet setAttr $labelSpaceEndMultValue1 -pattern singleValue -clearOverlays False
ixNet setAttr $labelSpaceEndMultValue1/singleValue -value 50000
ixNet commit

puts "Changing Label Space End for second RSVPTE router to increment mode"
ixNet setMultiAttr [ixNet getAttr $rsvpte2 -labelSpaceEnd]/counter\
        -direction  increment          \
        -start      60000              \
        -step       1
ixNet commit

puts "add ipv4 loopback1 for Label Edge Router"
set addressSet1 [ixNet getAttribute $loopback1 -address]
ixNet setMultiAttribute $addressSet1\
    -clearOverlays false            \
    -pattern counter
ixNet commit

set addressSet1 [ixNet add $addressSet1 "counter"]
ixNet setMultiAttribute $addressSet1\
    -step 0.0.0.1                   \
    -start 2.2.2.2                  \
    -direction increment
ixNet commit
set addressSet1 [lindex [ixNet remapIds $addressSet1] 0]
set addressSet2 [ixNet getAttribute $loopback2 -address]
ixNet setMultiAttribute $addressSet2\
    -clearOverlays false            \
    -pattern counter
ixNet commit

set addressSet1 [ixNet add $addressSet2 "counter"]
ixNet setMultiAttribute $addressSet1\
    -step 0.0.0.1                   \
    -start 3.3.3.3                  \
    -direction increment
ixNet commit
set addressSet1 [lindex [ixNet remapIds $addressSet2] 0]


puts "Adding RSVPTE router over 'IPv4 Loopback 1'"
set rsvpteLsps1 [ixNet add $loopback1 rsvpteLsps]
ixNet commit
set rsvpteLsps1 [lindex [ixNet remapIds $rsvpteLsps1] 0]

puts "Adding RSVPTE router over 'IPv4 Loopback 2'"
set rsvpteLsps2 [ixNet add $loopback2 rsvpteLsps]
ixNet commit
set rsvpteLsps2 [lindex [ixNet remapIds $rsvpteLsps2] 0]
puts "Assigning 'Remote IP' to RSVPTE LSPs under Topology 1"
set rsvpP2PIngressLsps1 [ixNet getList $rsvpteLsps1 rsvpP2PIngressLsps]
set remoteIp4Rsvp1 [ixNet getAttribute $rsvpP2PIngressLsps1 -remoteIp]
ixNet setMultiAttribute $remoteIp4Rsvp1\
    -clearOverlays false               \
    -pattern counter
ixNet commit
ixNet setMultiAttribute $remoteIp4Rsvp1/counter\
    -step 0.0.0.1                              \
    -start 3.3.3.3                             \
    -direction increment
ixNet commit

puts "Assigning 'Remote IP' to RSVPTE LSPs under Topology 2"
set rsvpP2PIngressLsps2 [ixNet getList $rsvpteLsps2 rsvpP2PIngressLsps]
set remoteIp4Rsvp2 [ixNet getAttribute $rsvpP2PIngressLsps2 -remoteIp]
ixNet setMultiAttribute $remoteIp4Rsvp2\
    -clearOverlays false               \
    -pattern counter
ixNet commit
ixNet setMultiAttribute $remoteIp4Rsvp2/counter\
    -step 0.0.0.1                              \
    -start 2.2.2.2                             \
    -direction increment
ixNet commit

puts "Changing Router Id of Network Topology to Loopback Address of Chained Device Group under Edge Router 1"
set simRouter1 [ixNet getList $netTopo1 simRouter]
set simRouterId1 [ixNet getAt $simRouter1 -routerId]

ixNet setMultiAttribute $simRouterId1        \
                        -clearOverlays false \
                        -pattern counter
ixNet commit
ixNet setMultiAttribute $simRouterId1/counter \
                        -step 0.0.0.1         \
                        -start 2.2.2.2        \
                        -direction increment
ixNet commit
set simRouterId1 [lindex [ixNet remapIds $simRouterId1] 0]
puts "Changing Router Id of Network Topology to Loopback Address of Chained Device Group under Edge Router 2"
set simRouter2 [ixNet getList $netTopo2 simRouter]
set simRouterId2 [ixNet getAt $simRouter2 -routerId]

ixNet setMultiAttribute $simRouterId2        \
                        -clearOverlays false \
                        -pattern counter
ixNet commit
ixNet setMultiAttribute $simRouterId2/counter \
                        -step 0.0.0.1         \
                        -start 3.3.3.3        \
                        -direction increment
ixNet commit
set simRouterId2 [lindex [ixNet remapIds $simRouterId2] 0]

################################################################################
# Step 2> Start of protocol.
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000
################################################################################
# Step 3> Retrieve protocol statistics.
################################################################################
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
puts "************************************************************"

###############################################################################
# Step 4> Retrieve protocol learned info
###############################################################################
ixNet exec getLearnedInfo $rsvpte1 1
after 5000
set linfo [ixNet getList $rsvpte1 learnedInfo]
set values [ixNet getAttribute $linfo -values]
puts "RSVPTE2 learned info"
puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"

################################################################################
# Step 5> Apply changes on the fly.
################################################################################
puts "Changing Label Value for first RSVPTE router to single value in Topology 1"
set labelSpaceStartMultValue1 [ixNet getAttr $rsvpte1 -labelSpaceStart]
ixNet setAttr $labelSpaceStartMultValue1 -pattern singleValue -clearOverlays False
ixNet setAttr $labelSpaceStartMultValue1/singleValue -value 8000
ixNet commit

puts "Changing Label Value for first RSVPTE router to single value in Topology 2"
set labelSpaceStartMultValue2 [ixNet getAttr $rsvpte2 -labelSpaceStart]
ixNet setAttr $labelSpaceStartMultValue2 -pattern singleValue -clearOverlays False
ixNet setAttr $labelSpaceStartMultValue2/singleValue -value 9000
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
        puts "$::errorInfo"
}
after 5000

################################################################################
# Step 6> Retrieve protocol learned info again and compare with.
################################################################################
ixNet exec getLearnedInfo $rsvpte1 1
after 5000
set linfo [ixNet getList $rsvpte1 learnedInfo]
set values [ixNet getAttribute $linfo -values]
puts "RSVPTE2 learned info"
puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"

################################################################################
# Step 7> Configure L2-L3 traffic.
################################################################################
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1  \
    -name {RSVPTE Traffic 1}           \
    -roundRobinPacketOrdering false    \
    -trafficType ipv4
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $rsvpteLsps1/rsvpP2PIngressLsps]
set destination  [list $rsvpteLsps2/rsvpP2PEgressLsps]

ixNet setMultiAttribute $endpointSet1           \
        -name                  "EndpointSet-1"  \
        -multicastDestinations [list]           \
        -scalableSources       [list]           \
        -multicastReceivers    [list]           \
        -scalableDestinations  [list]           \
        -ngpfFilters           [list]           \
        -trafficGroups         [list]           \
        -sources               $source          \
        -destinations          $destination        
ixNet commit
set endpointSet1 [lindex [ixNet remapIds $endpointSet1] 0]
ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy        [list sourceDestEndpointPair0 trackingenabled0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]
ixNet commit

###############################################################################
# Step 8> Apply and start L2/L3 traffic.
###############################################################################
puts "applying traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000
puts "starting traffic"
ixNet exec start [ixNet getRoot]/traffic

puts "let traffic run for 120 second"
after 12000
###############################################################################
# Step 9> Retrieve L2/L3 traffic item statistics.
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

#################################################################################
# Step 10> Stop L2/L3 traffic.
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# Step 11> Stop all protocols.
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
