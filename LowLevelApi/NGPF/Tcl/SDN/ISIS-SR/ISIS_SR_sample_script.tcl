#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           # 
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    08/01/2016 - Poulomi Chatterjee - created sample                          #
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
#    This script intends to demonstrate how to use NGPF ISIS SR TCL API.       #
#                                                                              #
#    1. It will create 2 ISIS topologies, topology1 will have a simulated      #
#        topology and topology2 will have IPv4 & IPv6 prefix pool.             #
#    2. Enable Segment Routing in ISIS Emulated Router.                        #
#    3. Set SRGB range and SID Count for Emulated Router.                      #
#    4. Enable Segment Routing in Simulated Router.                            #  
#    5. Start protocol.                                                        #
#    6. Retrieve protocol statistics.                                          #
#    7. Retrieve protocol learned info in Port1.                               #
#    8. Retrieve protocol learned info in Port2.                               #
#    9. On the fly change SID IndexLabel value for IPv4 & IPv6 PrefixPools.    #
#    10. On the fly Change SID Index Label in IPv4 & IPv6 PseudoNode Routes in #
#         Simulated Topology.                                                  #
#    11. Retrieve protocol learned info in Port1 after On the Fly change.      #
#    12. Change IPv4 & V6 PseudoNode Routes addresses in Simulated Topology    # 
#    13. Retrieve protocol learned info in Port2 after On the Fly change.      #
#    14. Configuring ISIS L2-L3 Traffic Item				       #
#    15. Verifying all the L2-L3 traffic stats                                 #
#    16. Stop L2-L3 traffic.                                                   #
#    17. Stop all protocols.                                                   #
#                                                                              #
# Ixia Softwares:                                                              #
#    IxOS      8.00 EA                                                         #
#    IxNetwork 8.00 EA                                                         #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your set-up
namespace eval ::ixia {
    set ixTclServer 10.216.108.34
    set ixTclPort   8377
    set ports       {{10.216.108.77 1  15} { 10.216.108.77  1  16}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.00\
   -setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure ISIS as per the description
#  give above
################################################################################ 
# Adding Virtual ports
puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]
set vportRx [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

# Adding topologies
puts "Adding 2 topologies"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet add [ixNet getRoot] topology -vports $vportRx
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

# Adding Device Groups
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

# Adding Ethernet
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

# Adding IPv4
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

#puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4"
#puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4]"

# Adding ISIS over Ethernet stack
puts "Adding ISIS over Ethernet stacks"
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

set isisL3Router1_1 [ixNet getList $t1dev1 isisL3Router]
set isisL3Router2_1 [ixNet getList $t2dev1 isisL3Router]

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


################################################################################
# 2.Enabling Segment Routing in Emulated Router
################################################################################
puts "Enabling Segment Routing for ISIS"
ixNet setAttr $isisL3Router1 -enableSR true

ixNet setAttr $isisL3Router2 -enableSR true
ixNet commit

################################################################################
# 3.Setting SRGB range and SID Count for Emulated Router
################################################################################
puts "Setting SRGB range pool for first Emulated Router"

set isisSRGBRangeSubObjectsList1 [ixNet getList $isisL3Router1 isisSRGBRangeSubObjectsList]
set startSIDLabel1 [ixNet getA $isisSRGBRangeSubObjectsList1 -startSIDLabel]
set svsrgb1 [ixNet getList $startSIDLabel1 singleValue]
ixNet setAtt $svsrgb1 -value 15000
ixNet commit

puts "Setting SID count for first Emulated Router "
set sidCount1 [ixNet getA $isisSRGBRangeSubObjectsList1 -sIDCount]
set sidcountsv [ixNet getList $sidCount1 singleValue]
ixNet setA $sidcountsv -value 100
ixNet commit

puts "Setting SRGB range pool for second Emulated Router"
set isisSRGBRangeSubObjectsList2 [ixNet getList $isisL3Router1 isisSRGBRangeSubObjectsList]
set startSIDLabel1 [ixNet getA $isisSRGBRangeSubObjectsList1 -startSIDLabel]
set svsrgb1 [ixNet getList $startSIDLabel1 singleValue]
ixNet setAtt $svsrgb1 -value 10000
ixNet commit

puts "Setting SID count for second Emulated Router"
set sidCount2 [ixNet getA $isisSRGBRangeSubObjectsList2 -sIDCount]
set sidcountsv [ixNet getList $sidCount2 singleValue]
ixNet setA $sidcountsv -value 100
ixNet commit

puts "Enabling Adj-SID in first Emulated Router"
set enableAdjSID1 [ixNet getAttr $isisL3_1 -enableAdjSID]
set svAdjSID1 [ixNet add $enableAdjSID1 singleValue]
ixNet setAttr $svAdjSID1 -value true
ixNet commit

puts "Enabling Adj-SID in second Emulated Router"
set enableAdjSID2 [ixNet getAttr $isisL3_2 -enableAdjSID]
set svAdjSID2 [ixNet add $enableAdjSID2 singleValue]
ixNet setAttr $svAdjSID2 -value true
ixNet commit

puts "Setting Adj-SID value in first Emulated Router"
set adjSID1 [ixNet getAttr $isisL3_1 -adjSID]
set counteradjSID1 [ixNet add $adjSID1 counter]
ixNet setMultiAttribute $counteradjSID1 \
-step 1 \
-start 9001 \
-direction increment
ixNet commit

puts "Setting Adj-SID value in second Emulated Router"
set adjSID2 [ixNet getAttr $isisL3_2 -adjSID]
set counteradjSID2 [ixNet add $adjSID2 counter]
ixNet setMultiAttribute $counteradjSID2 \
-step 1 \
-start 9002 \
-direction increment
ixNet commit

#Adding Network Group behind ISIS Device Group1
#Adding Prefix Pool behind ISIS Device Group2

puts "Adding Network Group behind ISIS Device Group1"
ixNet exec createDefaultStack $t1devices networkTopology
after 5000
set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet add $t2devices networkGroup] 0]
set networkGroup3 [lindex [ixNet add $t2devices networkGroup] 0]
#set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]
ixNet setAttr $networkGroup1 -name "ISIS_Network_Group1"
ixNet commit

puts "Adding IPv4 Prefix Pool behind ISIS Device Group2"
set ipv4PrefixPools [lindex [ixNet add $networkGroup2 ipv4PrefixPools] 0]
after 2000
ixNet commit
ixNet setA $networkGroup2 -multiplier 7
ixNet commit

ixNet setAttr $networkGroup2 -name "ISIS_IPv4_Prefix_Pools"
ixNet commit

puts "Adding IPv6 Prefix Pool behind ISIS Device Group2"
set ipv6PrefixPools [lindex [ixNet add $networkGroup3 ipv6PrefixPools] 0]
after 2000
ixNet commit
ixNet setA $networkGroup3 -multiplier 5
ixNet commit

ixNet setAttr $networkGroup3 -name "ISIS_IPv6_Prefix_Pools"
ixNet commit

set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]
set networkGroup3 [lindex [ixNet getList $t2devices networkGroup] 1]
set ipv4PrefixPools [ixNet getList  $networkGroup2 ipv4PrefixPools]
set ipv6PrefixPools [ixNet getList  $networkGroup3 ipv6PrefixPools]

################################################################################
# 4.Enabling Segment Routing in simulated router
################################################################################
puts "Enabling Segment Routing in Simulated Routers on Network Group behind Device Group1"
set networkTopo1 [ixNet getList $networkGroup1 networkTopology]
set simRouter1 [ixNet getList $networkTopo1 simRouter]
set isisPseudoRouter1 [ixNet getList $simRouter1 isisL3PseudoRouter]
ixNet setAttribute $isisPseudoRouter1 -enableSR true
ixNet commit

################################################################################
# 5. Start ISIS protocol and wait for 60 seconds
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
puts "***************************************************\n"

###############################################################################
# 7. Retrieve protocol learned info in Port 1
###############################################################################

puts "Fetching ISIS IPv4 & IPv6 Learned Info in Port 1"
ixNet exec getLearnedInfo $isisL3_1 
after 5000
set learnedInfoList [ixNet getList $isisL3_1 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]
set IPv4Info [lindex $linfoList 0]
set IPv6LInfo [lindex $linfoList 1]

puts "***************************************************"
foreach table $linfoList {
    set type [ixNet getAttr $table -type]
    puts "$type :"
    puts "***************************************************"
    set column [ixNet getAttr $table -columns]
    puts "$column"
    set values [ixNet getAttr $table -values]
    puts "$values\n"
    puts "***************************************************"
}
puts "***************************************************"

###############################################################################
# 8. Retrieve protocol learned info in Port 2
###############################################################################

puts "Fetching ISIS IPv4 & IPv6 Learned Info in Port 2"
ixNet exec getLearnedInfo $isisL3_2
after 5000
set learnedInfoList [ixNet getList $isisL3_2 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]
set IPv4Info [lindex $linfoList 0]
set IPv6LInfo [lindex $linfoList 1]

puts "***************************************************"
foreach table $linfoList {
    set type [ixNet getAttr $table -type]
    puts "$type :"
    puts "***************************************************"
    set column [ixNet getAttr $table -columns]
    puts "$column"
    set values [ixNet getAttr $table -values]
    puts "$values\n"
    puts "***************************************************"
}
puts "***************************************************"


################################################################################
# 9. Setting on the fly change sidIndexLabel value for ipv4 & ipv6 PrefixPools
################################################################################
puts "Setting on the fly change sidIndexLabel value for ipv4 & ipv6 PrefixPools in Port2"
set isisRouteProperty1 [ixNet getList $ipv4PrefixPools isisL3RouteProperty]
set sidIndexLabel1 [ixNet getAttr $isisRouteProperty1 -sIDIndexLabel]
set sidIndexLabelcounter1 [ixNet add $sidIndexLabel1 counter]
ixNet setMultiAttr $sidIndexLabelcounter1 \
-step 7 \
 -start 15 \
 -direction increment
ixNet commit

set isisRouteProperty2 [ixNet getList $ipv6PrefixPools isisL3RouteProperty]
set sidIndexLabel2 [ixNet getAttr $isisRouteProperty2 -sIDIndexLabel]
set sidIndexLabelcounter2 [ixNet add $sidIndexLabel2 counter]
ixNet setMultiAttr $sidIndexLabelcounter2 \
 -step 2 \
 -start 50 \
 -direction increment
ixNet commit


set globals [ixNet getRoot]/globals
set topology $globals/topology
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
    puts "$::errorInfo"
}
after 5000

###############################################################################
# 10. Retrieve protocol learned info
###############################################################################
puts "Fetching ISIS Learned Info in Port 1 After OTF"
ixNet exec getLearnedInfo $isisL3_1
after 5000
set learnedInfoList [ixNet getList $isisL3_1 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]
set IPv4Info [lindex $linfoList 0]
set IPv6LInfo [lindex $linfoList 1]

puts "***************************************************"
foreach table $linfoList {
    set type [ixNet getAttr $table -type]
    puts "$type :"
    puts "***************************************************"
    set column [ixNet getAttr $table -columns]
    puts "$column"
    set values [ixNet getAttr $table -values]
    puts "$values\n"
    puts "***************************************************"
}
puts "***************************************************"

################################################################################
# 11. Changing SID Index Label in IPv4 & v6 PseudoNode Routes in Simulated Topology 1
#      and active the routes
################################################################################
puts "Changing SID Index Label in IPv4 & IPv6 PseudoNode Routes in Simulated Topology 1 in Port1"
set IPv4PseudoNodeRoutes [ixNet getList $isisPseudoRouter1 IPv4PseudoNodeRoutes]
ixNet setAttr [ixNet getAttr $IPv4PseudoNodeRoutes -sIDIndexLabel]/singleValue -value "7"
puts "Activate IPv4 PseudoNode Routes in Simulated Topology 1 in Port1"
ixNet setAttr [ixNet getAttr $IPv4PseudoNodeRoutes -active]/singleValue -value "true"

set IPv6PseudoNodeRoutes [ixNet getList $isisPseudoRouter1 IPv6PseudoNodeRoutes]
ixNet setAttr [ixNet getAttr $IPv6PseudoNodeRoutes -sIDIndexLabel]/singleValue -value "10"
puts "Activate IPv6 PseudoNode Routes in Simulated Topology 1 in Port1"
ixNet setAttr [ixNet getAttr $IPv6PseudoNodeRoutes -active]/singleValue -value "true"
ixNet commit

if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
    puts "$::errorInfo"
}
after 5000

################################################################################
# 12. Changing IPv4 & IPv6 PseudoNode Routes in Simulated Topology  from 
#      default addresses. And apply changes On The Fly (OTF).
################################################################################
puts "Changing IPv4 Addresses in IPv4 PseudoNode Routes in Simulated Topology 1"
ixNet setMultiAttr [ixNet getAttr $IPv4PseudoNodeRoutes -networkAddress]/singleValue -value "251.1.1.1" 
puts "Changing IPv6 Addresses in IPv6 PseudoNode Routes in Simulated Topology 1"
ixNet setMultiAttr [ixNet getAttr $IPv6PseudoNodeRoutes -networkAddress]/singleValue -value "3222:0:1:1:0:0:0:1"

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
# 13. Retrieve protocol learned info again and compare with
#    previously retrieved learned info.  
###############################################################################
puts "Fetching ISIS Leanred Info in Port2 after the change"
ixNet exec getLearnedInfo $isisL3_2
after 5000
set learnedInfoList [ixNet getList $isisL3_2 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]
set IPv4Info [lindex $linfoList 0]
set IPv6LInfo [lindex $linfoList 1]

puts "***************************************************"
foreach table $linfoList {
    set type [ixNet getAttr $table -type]
    puts "$type :"
    puts "***************************************************"
    set column [ixNet getAttr $table -columns]
    puts "$column"
    set values [ixNet getAttr $table -values]
    puts "$values\n"
    puts "***************************************************"
}
puts "***************************************************"
################################################################################
# 14. Configure L2-L3 traffic 
################################################################################
puts "Configuring  L2-L3 IPv4 Traffic Item # 1"

puts "Configuring traffic item 1 with endpoints src :isisPseudoNodeRoutes & dst :ipv4PrefixPools "

set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {IPv4_MPLS_Traffic_Item_1}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv4
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $networkGroup1/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv4PseudoNodeRoutes:1]
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

puts "Configuring  L2-L3 IPv4 Traffic Item # 2"
puts "Configuring traffic item 2 with endpoints src :isisRouterDG1 & dst :isisRouterDG2"

set trafficItem2 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem2\
    -name {IPv4_MPLS_Traffic_Item_2}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv4
ixNet commit

set trafficItem2 [lindex [ixNet remapIds $trafficItem2] 0]
set endpointSet2 [ixNet add $trafficItem2 "endpointSet"]

set source       [list $t1devices/isisL3Router:1]
set destination  [list $t2devices/isisL3Router:1]
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


puts "Configuring  L2-L3 IPv6 Traffic Item # 3"
puts "Configuring traffic item 3 with endpoints src :isisIPv6PseudoNodeRoutes & dst :ipv6PrefixPools "

set trafficItem3 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem3\
    -name {IPv6_MPLS_Traffic_Item_1}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv6
ixNet commit

set trafficItem3 [lindex [ixNet remapIds $trafficItem3] 0]
set endpointSet3 [ixNet add $trafficItem3 "endpointSet"]
set source       [list $networkGroup1/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1]
set destination  [list $ipv6PrefixPools ]

ixNet setMultiAttribute $endpointSet3\
    -name                  "EndpointSet-3"\
    -multicastDestinations [list]\
    -scalableSources       [list]\
    -multicastReceivers    [list]\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               $source\
    -destinations          $destination
ixNet commit

ixNet setMultiAttribute $trafficItem3/configElement:1/transmissionDistribution \
    -distributions [list ipv6SourceIp0 ]

ixNet commit

ixNet setMultiAttribute $trafficItem3/tracking\
    -trackBy        [list sourceDestValuePair0 trackingenabled0 mplsMplsLabelValue0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]\

ixNet commit

###############################################################################
# 15. Apply and start L2/L3 traffic
###############################################################################
puts "Applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "Starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

###############################################################################
# 16. Retrieve L2/L3 traffic item statistics
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
# 17. Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 18. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"

