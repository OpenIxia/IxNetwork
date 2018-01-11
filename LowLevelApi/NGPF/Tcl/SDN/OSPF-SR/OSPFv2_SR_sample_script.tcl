#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    03/12/2015 - Chandan Mishra - created sample                              #
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
#    This script intends to demonstrate how to use NGPF OSPFv2 API.            #
#                                                                              #
#    1. It will create 2 OSPFv2 topologies, each having an ipv4 network        #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. A loopback device group(DG) behind network   # 
#       group is needed to support applib traffic.                             #
#    2. Start the ospfv2 protocol.                                             #
#    3. Enabling Segment Routing in ospfv2                                     #
#    4. Retrieve protocol statistics.                                          #
#    5. Retrieve protocol learned info.                                        #
#    6. Enable the Ospfv2 simulated topologies External Route type1 for DG1,   #
#       which was disabled by default and apply change on the fly.             #
#    7. Enable Segment Routing in Simulated Router                             #
#    8.	Setting SRGB range and SID Count for Emulated Router                   #
#	 9.	Enabling Adj-SID in both emulated router                               #
#	10.	Setting Adj-SID value in both emulated router                          #
#	11.	Adding Network Group behind both OSPFv2 Device Groups                  #
#	12.	Enabling Segment Routing in simulated router                           #
#	13.	Starting protocols                                                     #
#	14.	Fetching all Protocol Summary Stats                                    #
#	15.	Setting on the fly change sidIndexLabel value for ipv4PrefixPools      #
#		and Simulated Router                                                   #
#	16.	Fetching OSPFv2 Basic Learned Info									   #
#	17.	Enabling External Type-1 Simulated Routes on Network Group behind 	   #
#		Device Group1														   #
#	18.	Fetching OSPFv2 on DG2 learned info after enabling ospf external       #
#		route type1															   #
#	19.	Configuring MPLS L2-L3 Traffic Item									   #
#	20.	Verifying all the L2-L3 traffic stats                                  #
#   21. Stop L2-L3 traffic.                                                    #
#   22. Stop Application traffic.                                              #
#   23. Stop all protocols.                                                    #
#                                                                  			   #                                                                                          
# 	Ixia Softwares:                                                            #
#    IxOS      8.00 EB (8.00.1201.21)                                          #
#    IxNetwork 8.00 EB (8.00.1206.6)                                           #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your set-up
namespace eval ::ixia {
    set ixTclServer 10.216.104.58
    set ixTclPort   8091
    set ports       {{10.216.108.129 1 3} { 10.216.108.129 1 4}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.00\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure OSPFv2 as per the description
#  give above
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

puts "Configuring ipv4 addresses"
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

puts "Adding OSPFv2 over IPv4 stacks"
ixNet add $ip1 ospfv2
ixNet add $ip2 ospfv2
ixNet commit

set ospf1 [ixNet getList $ip1 ospfv2]
set ospf2 [ixNet getList $ip2 ospfv2]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "OSPF Topology 1"
ixNet setAttr $topo2  -name "OSPF Topology 2"

ixNet setAttr $t1dev1 -name "OSPF Topology 1 Router"
ixNet setAttr $t2dev1 -name "OSPF Topology 2 Router"
ixNet commit

puts "Making the NetworkType to Point to Point in the first OSPF router"
set networkTypeMultiValue1 [ixNet getAttr $ospf1 -networkType]
ixNet setAttr $networkTypeMultiValue1 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue1/singleValue -value pointtopoint

puts "Making the NetworkType to Point to Point in the Second OSPF router"
set networkTypeMultiValue2 [ixNet getAttr $ospf2 -networkType]
ixNet setAttr $networkTypeMultiValue2 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue2/singleValue -value pointtopoint

puts "Disabling the Discard Learned Info CheckBox"

set ospfv2RouterDiscardLearnedLSA1\
    [ixNet getAttr [lindex [ixNet getList $t1devices ospfv2Router] 0] -discardLearnedLsa]

set ospfv2RouterDiscardLearnedLSA2\
    [ixNet getAttr [lindex [ixNet getList $t2devices ospfv2Router] 0] -discardLearnedLsa]

ixNet setAttr $ospfv2RouterDiscardLearnedLSA1 -pattern singleValue -clearOverlays False
ixNet setAttr $ospfv2RouterDiscardLearnedLSA1/singleValue -value False
ixNet setAttr $ospfv2RouterDiscardLearnedLSA2 -pattern singleValue -clearOverlays False
ixNet setAttr $ospfv2RouterDiscardLearnedLSA2/singleValue -value False

# puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2]"

################################################################################
# 2.Enabling Segment Routing in Emulated Router
################################################################################
puts "Enabling Segment Routing for OSPFv2"
set ospfv2Router1 [ixNet getList $t1devices ospfv2Router]
ixNet setAttr $ospfv2Router1 -enableSegmentRouting true

set ospfv2Router2 [ixNet getList $t2devices ospfv2Router]
ixNet setAttr $ospfv2Router2 -enableSegmentRouting true
ixNet commit

################################################################################
# 3.Setting SRGB range and SID Count for Emulated Router
################################################################################
puts "Setting SRGB range pool for first emulated router"

set ospfSRGBRangeSubObjectsList1 [ixNet getList $ospfv2Router1 ospfSRGBRangeSubObjectsList]
set startSIDLabel1 [ixNet getA $ospfSRGBRangeSubObjectsList1 -startSIDLabel]
set svsrgb1 [ixNet getList $startSIDLabel1 singleValue]
ixNet setAtt $svsrgb1 -value 4000

ixNet commit

puts "Setting SID count for first emulated router "
set sidCount1 [ixNet getA $ospfSRGBRangeSubObjectsList1 -sidCount]
set sidcountsv [ixNet getList $sidCount1 singleValue]
ixNet setA $sidcountsv -value 100
ixNet commit

puts "Setting SRGB range pool for second emulated router"
set ospfSRGBRangeSubObjectsList2 [ixNet getList $ospfv2Router2 ospfSRGBRangeSubObjectsList]

set startSIDLabel2 [ixNet getA $ospfSRGBRangeSubObjectsList2 -startSIDLabel]
set svsrgb2 [ixNet getList $startSIDLabel2 singleValue]
ixNet setAtt $svsrgb2 -value 5000

ixNet commit

puts "Setting SID count for second emulated router"
set sidCount2 [ixNet getA $ospfSRGBRangeSubObjectsList2 -sidCount]
set sidcountsv [ixNet getList $sidCount2 singleValue]
ixNet setA $sidcountsv -value 100
ixNet commit

puts "Enabling Adj-SID in first emulated router"
set enableAdjSID1 [ixNet getAttr $ospf1 -enableAdjSID]
set svAdjSID1 [ixNet add $enableAdjSID1 singleValue]
ixNet setAttr $svAdjSID1 -value true
ixNet commit

puts "Enabling Adj-SID in second emulated router"
set enableAdjSID2 [ixNet getAttr $ospf2 -enableAdjSID]
set svAdjSID2 [ixNet add $enableAdjSID2 singleValue]
ixNet setAttr $svAdjSID2 -value true
ixNet commit

puts "Setting Adj-SID value in first emulated router"
set adjSID1 [ixNet getAttr $ospf1 -adjSID]
set counteradjSID1 [ixNet add $adjSID1 counter]
ixNet setMultiAttribute $counteradjSID1 \
-step 1 \
-start 9001 \
-direction increment
ixNet commit

puts "Setting Adj-SID value in second emulated router"
set adjSID2 [ixNet getAttr $ospf2 -adjSID]
set counteradjSID2 [ixNet add $adjSID2 counter]
ixNet setMultiAttribute $counteradjSID2 \
-step 1 \
-start 9002 \
-direction increment
ixNet commit

puts "Adding Network Group behind OSPFv2 Device Group1"
ixNet exec createDefaultStack $t1devices networkTopology
after 5000
set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet add $t2devices networkGroup] 0]
puts "Adding Prefix Pool behind OSPFv2 Device Group2"
set ipv4PrefixPools [lindex [ixNet add $networkGroup2 ipv4PrefixPools] 0]
ixNet commit
ixNet setA $networkGroup2 -multiplier 7
ixNet commit

ixNet setAttr $networkGroup1 -name "OSPF_1_Network_Group1"
ixNet setAttr $networkGroup2 -name "OSPF_2_ipv4_Prefix_Pools"
ixNet commit

################################################################################
# 4.Enabling Segment Routing in simulated router
################################################################################
puts "Enabling Segment Routing in Simulated Routers on Network Group behind Device Group1"
set networkTopo1 [ixNet getList $networkGroup1 networkTopology]
set simRouter1 [ixNet getList $networkTopo1 simRouter]
set ospfPseudoRouter1 [ixNet getList $simRouter1 ospfPseudoRouter]
ixNet setA $ospfPseudoRouter1 -enableSegmentRouting true
ixNet commit

################################################################################
# 5. Start OSPFv2 protocol and wait for 60 seconds
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000

################################################################################
# 6. Retrieve protocol statistics.
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

################################################################################
# 7. Setting on the fly change sidIndexLabel value for ipv4PrefixPools
################################################################################
puts "Setting on the fly change sidIndexLabel value for ipv4PrefixPools from Index 10 "
set ospfRouteProperty1 [ixNet getList $ipv4PrefixPools ospfRouteProperty]
set sidIndexLabel1 [ixNet getAttr $ospfRouteProperty1 -sidIndexLabel]
set sidIndexLabelcounter1 [ixNet add $sidIndexLabel1 counter]
ixNet setMultiAttr $sidIndexLabelcounter1 \
-step 2 \
 -start 10 \
 -direction increment
ixNet commit
set globals [ixNet getRoot]/globals
set topology $globals/topology
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
    puts "$::errorInfo"
}
after 5000

################################################################################
# 8. Setting on the fly change sidIndexLabel value for Simulated Router
################################################################################
puts "Setting on the fly change sidIndexLabel value for Simulated Router from Index 11  "
set sidIndexLabel2 [ixNet getAttr $ospfPseudoRouter1 -sidIndexLabel]
set sidIndexLabelcounter1 [ixNet add $sidIndexLabel2 counter]
ixNet setMultiAttr $sidIndexLabelcounter1 \
-step 2 \
 -start 11 \
 -direction increment
ixNet commit

if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
    puts "$::errorInfo"
}
after 5000

###############################################################################
# 9. Retrieve protocol learned info
###############################################################################
puts "Fetching OSPFv2 Basic Learned Info"
ixNet exec getBasicLearnedInfo $ospf1 1
after 5000
set linfo [ixNet getList $ospf1 learnedInfo]
set values [ixNet getAttribute $linfo -values]

puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"

################################################################################
# 10. Enable the Ospfv2 simulated topology's External Route type1, which
#    was disabled by default. And apply changes On The Fly (OTF).
################################################################################
puts "Enabling External Type-1 Simulated Routes on Network Group behind Device Group1 to send SR routes for Simulated node routes"

set extRoute1         [lindex [ixNet getList $ospfPseudoRouter1 ospfPseudoRouterType1ExtRoutes] 0]
set activeMultivalue1 [ixNet getAttr $extRoute1 -active]
ixNet setAttribute $activeMultivalue1/singleValue -value true
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
puts "Applying changes on the fly"
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
    puts "$::errorInfo"
}
after 5000

###############################################################################
# 11. Retrieve protocol learned info again and compare with
#    previously retrieved learned info.  
###############################################################################
puts "Fetching OSPFv2 on DG2 learned info after enabling ospf external route type1"
ixNet exec getBasicLearnedInfo $ospf2 1
after 5000
set linfo [ixNet getList $ospf2 learnedInfo]
set values [ixNet getAttribute $linfo -values]
puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"


################################################################################
# 12. Configure L2-L3 traffic 
################################################################################
puts "Configuring MPLS L2-L3 Traffic Item"

puts "Configuring traffic item 1 with endpoints src :ospfPseudoRouterType1ExtRoutes & dst :ipv4PrefixPools "

set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {Traffic Item 1}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv4
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $networkGroup1/networkTopology/simRouter:1/ospfPseudoRouter:1/ospfPseudoRouterType1ExtRoutes:1]
set destination  [list $ipv4PrefixPools ]

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

ixNet setMultiAttribute $trafficItem1/configElement:1/transmissionDistribution \
    -distributions [list ipv4SourceIp0 ]
	
ixNet commit

ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy        [list sourceDestValuePair0 trackingenabled0 mplsMplsLabelValue0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]\
	
ixNet commit

puts "Configuring traffic item 2 with endpoints src :ospfv2RouterDG1 & dst :ospfv2RouterDG2 "

set trafficItem2 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem2\
    -name {Traffic Item 2}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv4
ixNet commit

set trafficItem2 [lindex [ixNet remapIds $trafficItem2] 0]
set endpointSet2 [ixNet add $trafficItem2 "endpointSet"]

set source       [list $t1devices/ospfv2Router:1]
set destination  [list $t2devices/ospfv2Router:1]
ixNet setMultiAttribute $endpointSet2\
    -name                  "EndpointSet-2"\
    -multicastDestinations [list]\
    -scalableSources       [list]\
    -multicastReceivers    [list]\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               $source\
    -destinations          $destination 
ixNet commit

ixNet setMultiAttribute $trafficItem2/configElement:1/transmissionDistribution \
    -distributions [list ipv4SourceIp0 ]
	
ixNet commit

ixNet setMultiAttribute $trafficItem2/tracking\
    -trackBy        [list sourceDestValuePair0 trackingenabled0 mplsMplsLabelValue0 mplsFlowDescriptor0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]\
	
ixNet commit

puts "Enabling option Display Dynamic Value when Tracking by Dynamic Flow Descriptor from Traffic Options in Global"
set traffic [ixNet getRoot]/traffic
ixNet setAttr $traffic -displayMplsCurrentLabelValue true
ixNet commit

###############################################################################
# 13. Apply and start L2/L3 traffic
###############################################################################
puts "Applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "Starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

###############################################################################
# 14. Retrieve L2/L3 traffic item statistics
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
# 15. Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 16. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"

