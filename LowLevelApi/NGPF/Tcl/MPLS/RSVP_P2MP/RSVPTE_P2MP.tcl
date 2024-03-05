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
#    This script intends to demonstrate how to use NGPF RSVPTE P2MP API         #
#    About Topology:                                                            #
#       Within topology both Label Switch Router(LSR) and Label Edge Router(LER)#
#    are created. LSR is emulated in the front Device Group(DG), which consists #
#    of both OSPF as routing protocol as well as RSVPTE-IF for Label            # 
#    Distribution Protocol. The chained DG act as LER, where RSVP-TE P2MP LSPs  #
#    are configured. Unidirectional L2-L3 Traffic from Ingress to Egress is     #
#    created.                                                                   #
#         Script Flow:                                                          #
#        Step 1. Configuration of protocols.                                    #
#    Configuration flow of the script is as follow:                             #
#             i.      Adding of OSPF router                                     #
#             ii.     Adding of Network Topology(NT)                            #
#             iii.    Enabling of TE(Traffic Engineering)                       #
#             iv.     Adding of chain DG                                        #
#             v.      Adding of RSVP-TE LSPs within chain DG                    #
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
ixNet setAttr $topo1  -name "RSVPTE P2MP Topology 1"
ixNet setAttr $topo2  -name "RSVPTE P2MP Topology 2"

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

puts "Adding IPv4 stack and configuring  IP Address"
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

puts "Configuring ipv4 addresses"
ixNet setAttr $mvAdd1/singleValue -value "50.50.50.2"
ixNet setAttr $mvAdd2/singleValue -value "50.50.50.1"
ixNet setAttr $mvGw1/singleValue  -value "50.50.50.1"
ixNet setAttr $mvGw2/singleValue  -value "50.50.50.2"

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
puts "Adding IPv4 Address Pool in Topology1"
ixNet add $t1devices networkGroup
ixNet add $t2devices networkGroup
ixNet commit

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

ixNet add $networkGroup1 ipv4PrefixPools
ixNet commit

set ipv4PrefixPools1 [ixNet getList $networkGroup1 ipv4PrefixPools]
ixNet commit

puts "Adding Linear Tree in Topology2"
set netTopologyLinear [ixNet add [ixNet add $networkGroup2 networkTopology] netTopologyLinear]
set netTopologyLinear [lindex [ixNet remapIds $netTopologyLinear] 0]

ixNet commit
set networkTopology1 [ixNet getList $networkGroup2 networkTopology]
set networkTopology1 [lindex [ixNet remapIds $networkTopology1] 0]

ixNet setMultiAttribute $netTopologyLinear -nodes 5
ixNet commit

ixNet setMultiAttribute $networkTopology1/simInterface:1 \
	-name "Simulated\ Interfaces\ 1"

ixNet setMultiAttribute $networkTopology1/simInterface:1/simInterfaceIPv4Config:1 \
	-name "Simulated\ Link\ IPv4\ Address\ 1"

ixNet setMultiAttribute $networkTopology1/simInterface:1/simInterfaceIPv4Config:1/ospfPseudoInterface:1 \
	-name "OSPF\ Simulated\ Interface\ Configuration\ 1"

puts "Enabling Traffic Engineering"	
set TE_enabled [ixNet getAttribute $networkTopology1/simInterface:1/simInterfaceIPv4Config:1/ospfPseudoInterface:1 -enable]
ixNet setMultiAttribute $TE_enabled \
	-clearOverlays false
ixNet commit

set single_Value [ixNet add $TE_enabled "singleValue"]
ixNet setMultiAttribute $single_Value \
	-value true
ixNet commit

puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $networkGroup1 -multiplier 2
ixNet setAttr $networkGroup2 -multiplier 2
ixNet commit

# Adding Chained Device Group Behind front Device Group for IPv4 loopback
puts "Adding Chained DG behind Network Topology in Topology 1"
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
    -name {IPv4 Loopback 1}
ixNet commit
puts "Adding Chained DG behind Network Topology in Topology 2"
set chainedDg2 [ixNet add $networkGroup2 deviceGroup]
ixNet setMultiAttribute $chainedDg2\
    -multiplier 1                  \
        -name {Edge Router 2}
ixNet commit
set chainedDg2 [lindex [ixNet remapIds $chainedDg2] 0]

set loopback2 [ixNet add $chainedDg2 "ipv4Loopback"]
ixNet setMultiAttribute $loopback2\
    -stackedLayers [list]         \
    -name {IPv4 Loopback 2}
ixNet commit

puts "Adding RSVPTE P2MP router over 'IPv4 Loopback 1'"
set rsvpteLsps1 [ixNet add $loopback1 rsvpteLsps]
ixNet setMultiAttribute $rsvpteLsps1 -ingressP2PLsps 0 \
			-enableP2PEgress false \
			-p2mpIngressLspCount 1 \
			-p2mpEgressTunnelCount 0 \
			-stackedLayers [list ] \
			-name "RSVP-TE\ 1"
ixNet commit
set rsvpteLsps1 [lindex [ixNet remapIds $rsvpteLsps1] 0]

puts "Adding RSVPTE P2MP router over 'IPv4 Loopback 2'"
set rsvpteLsps2 [ixNet add $loopback2 rsvpteLsps]
ixNet setMultiAttribute $rsvpteLsps2 -ingressP2PLsps 0 \
			-enableP2PEgress false \
			-p2mpIngressLspCount 0 \
			-p2mpEgressTunnelCount 5 \
			-stackedLayers [list ] \
			-name "RSVP-TE\ 2"
ixNet commit
set rsvpteLsps2 [lindex [ixNet remapIds $rsvpteLsps2] 0]

puts "Editing P2MP ID in Ingress and Egress LSPs"
#Edit P2MP ID in Ingress and Egress LSPs
set p2mpIdAsNumber_ingress [ixNet getAttribute $rsvpteLsps1/rsvpP2mpIngressLsps -p2mpIdAsNumber]
ixNet setMultiAttribute $p2mpIdAsNumber_ingress\
    -clearOverlays false \
    -pattern counter
ixNet commit

ixNet setMultiAttr $p2mpIdAsNumber_ingress/counter\
        -direction  increment         \
        -start      1              \
        -step       1
ixNet commit

set p2mpIdAsNumber_egress [ixNet getAttribute $rsvpteLsps2/rsvpP2mpEgressLsps -p2mpIdAsNumber]
ixNet setMultiAttribute $p2mpIdAsNumber_egress\
    -clearOverlays false \
    -pattern custom
ixNet commit

set custom [ixNet add $p2mpIdAsNumber_egress "custom"]

ixNet setMultiAttr $custom\
        -step 0 \
		-start 1
		ixNet commit
set custom [lindex [ixNet remapIds $custom] 0]
		
set inc1 [ixNet add $custom "increment"]
ixNet setMultiAttribute $inc1 \
		-count 2 \
		-value 1
ixNet commit
set inc1 [lindex [ixNet remapIds $inc1] 0]
		
ixNet commit

puts "Editing P2MP Ingress SubLSPs counter"
#Edit Ingress SubLSPs counter 
ixNet setAttribute $rsvpteLsps1/rsvpP2mpIngressLsps -ingressP2mpSubLspRanges 5
ixNet commit

puts "Editing Leaf IP in Ingress SubLSPs"
#Edit Leaf IP in Ingress SubLSPs
set leafIp [ixNet getAttribute $rsvpteLsps1/rsvpP2mpIngressLsps/rsvpP2mpIngressSubLsps -leafIp]
ixNet setMultiAttribute $leafIp \
	-clearOverlays false
ixNet commit

set custom_leaf [ixNet add $leafIp "custom"]
ixNet setMultiAttribute $custom_leaf \
	-step 0.0.0.0 \
	-start 3.2.2.2
ixNet commit
set custom_leaf [lindex [ixNet remapIds $custom_leaf] 0]

set increment_leaf [ixNet add $custom_leaf "increment"]
ixNet setMultiAttribute $increment_leaf \
	-count 2 \
	-value 0.0.0.1
ixNet commit
set custom_leaf [lindex [ixNet remapIds $custom_leaf] 0]

################################################################################
# Step 2> Start of protocol.
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000
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
puts "************************************************************"

###############################################################################
# Step 4> Retrieve protocol learned info
###############################################################################
set rsvpteIf1 [ixNet getList $ip1 rsvpteIf]
set learnedInfoList1 [ixNet exec getLearnedInfo $rsvpteIf1]

after 5000
set linfo [ixNet getList $rsvpteIf1 learnedInfo]
set receivedLearnedInfoList [lindex $linfo 3]
set receivedLearnedInfo [lindex [ixNet getList $receivedLearnedInfoList table] 0]

set values1 [ixNet getAttribute $receivedLearnedInfo -values]

puts "RSVPTE P2MP Received learned info"
puts "***************************************************"
foreach v1 $values1 {
    puts $v1
}
puts "***************************************************"
set rsvpteIf2 [ixNet getList $ip2 rsvpteIf]
set learnedInfoList2 [ixNet exec getLearnedInfo $rsvpteIf2]

after 5000
set linfo2 [ixNet getList $rsvpteIf2 learnedInfo]
set assignedLearnedInfoList [lindex $linfo2 2]
set assignedLearnedInfo [lindex [ixNet getList $assignedLearnedInfoList table] 0]

set values2 [ixNet getAttribute $assignedLearnedInfo -values]

puts "RSVPTE P2MP Assigned learned info"
puts "***************************************************"
foreach v2 $values2 {
    puts $v2
}

################################################################################
# Step 5> Apply changes on the fly.
################################################################################
puts "Changing Label Value for first RSVPTE router to single value in Topology 1"
set labelSpaceStartMultValue1 [ixNet getAttr $rsvpteIf1 -labelSpaceStart]
ixNet setAttr $labelSpaceStartMultValue1 -pattern singleValue -clearOverlays False
ixNet setAttr $labelSpaceStartMultValue1/singleValue -value 8000
ixNet commit

puts "Changing Label Value for first RSVPTE router to single value in Topology 2"
set labelSpaceStartMultValue2 [ixNet getAttr $rsvpteIf2 -labelSpaceStart]
ixNet setAttr $labelSpaceStartMultValue2 -pattern singleValue -clearOverlays False
ixNet setAttr $labelSpaceStartMultValue2/singleValue -value 9000
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "Error in applying on the fly change"
        puts "$::errorInfo"
}
after 5000

################################################################################
# Step 6> Retrieve protocol learned info again and compare with.
################################################################################
set rsvpteIf1 [ixNet getList $ip1 rsvpteIf]
set learnedInfoList1 [ixNet exec getLearnedInfo $rsvpteIf1]

after 5000
set linfo [ixNet getList $rsvpteIf1 learnedInfo]
set receivedLearnedInfoList [lindex $linfo 3]
set receivedLearnedInfo [lindex [ixNet getList $receivedLearnedInfoList table] 0]

set values3 [ixNet getAttribute $receivedLearnedInfo -values]

puts "RSVPTE P2MP Received learned info after OTF changes"
puts "***************************************************"
foreach v3 $values3 {
    puts $v3
}
puts "***************************************************"
set rsvpteIf2 [ixNet getList $ip2 rsvpteIf]
set learnedInfoList2 [ixNet exec getLearnedInfo $rsvpteIf2]

after 5000
set linfo2 [ixNet getList $rsvpteIf2 learnedInfo]
set assignedLearnedInfoList [lindex $linfo2 2]
set assignedLearnedInfo [lindex [ixNet getList $assignedLearnedInfoList table] 0]

set values4 [ixNet getAttribute $assignedLearnedInfo -values]

puts "RSVPTE P2MP Assigned learned info after OTF changes"
puts "***************************************************"
foreach v4 $values4 {
    puts $v4
}

################################################################################
# Step 7> Configure L2-L3 traffic.
################################################################################
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1  \
    -name {RSVPTE P2MP Traffic 1}           \
    -roundRobinPacketOrdering false    \
	-numVlansForMulticastReplication 1 \
    -trafficType ipv4
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $rsvpteLsps1/rsvpP2mpIngressLsps]
set destination  [list $rsvpteLsps2/rsvpP2mpEgressLsps]

ixNet setMultiAttribute $endpointSet1           \
        -name                  "EndpointSet-1"  \
        -multicastDestinations [list [list false none 225.0.0.0 0.0.0.0 1]] \
		-multicastReceivers $destination \
		-sources $source
ixNet commit

set endpointSet1 [lindex [ixNet remapIds $endpointSet1] 0]

ixNet setMultiAttribute $trafficItem1/tracking -trackBy \
    [list sourceDestEndpointPair0 mplsFlowDescriptor0 trackingenabled0 mplsMplsLabelValue0 ipv4DestIp0 ipv4SourceIp0]
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