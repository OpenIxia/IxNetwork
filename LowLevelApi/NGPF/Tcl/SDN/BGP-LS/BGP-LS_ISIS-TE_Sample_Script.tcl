#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           # 
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    11/24/2016 - Rupam Paul - created sample                                  #
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
#    This script intends to demonstrate how to use NGPF BGPLS &                #
#    ISIS TE SR Low Level TCL API.                                             #
#                                                                              #
#    1. It will create 2 BGP and 2 ISIS Topologies and 1 Network Group.        #
#    2. ISIS SR, TE and SR Algorithm is enabled on both Emulated and           #
#       Simulated Routers.                                                     #
#    3. BGP LS is Enabled                                                      #
#    4. Start All Protocols                                                    #
#    5. Check Protocol Stats                                                   #
#    6. Check BGPLS Learned Info	                                           #
#    7. Stop all protocols.                                                    #
#                                                                              #
# Ixia Softwares:                                                              #
#    IxOS      8.20 EA                                                         #
#    IxNetwork 8.20 EA                                                         #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your set-up
namespace eval ::ixia {
    set ixTclServer 10.216.104.58
    set ixTclPort   5555
    set ports       {{10.216.108.130 12  1} { 10.216.108.130  12  2}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.20\
   -setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# Protocol configuration section. Configure ISIS as per the description
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
# Traffic Engineering Configuration for ISIS Emulated Routers
################################################################################

puts "Enabling TE on Router1"
ixNet setAttr [ixNet getAttr $isisL3Router1_1 -enableTE]/singleValue -value true
ixNet commit

puts "Enabling TE on Router2"
ixNet setAttr [ixNet getAttr $isisL3Router2_1 -enableTE]/singleValue -value true
ixNet commit

puts "Enabling Metric Level for Traffic Engineering under ISISL3-IF in DG1"
set isisTrafficEngineering1 [ixNet getList $isisL3_1 isisTrafficEngineering]
ixNet setAttr [ixNet getAttr $isisTrafficEngineering1 -metricLevel]/singleValue -value "44"
ixNet commit

puts "Enabling Metric Level for Traffic Engineering under ISISL3-IF in DG2"
set isisTrafficEngineering2 [ixNet getList $isisL3_2 isisTrafficEngineering]
ixNet setAttr [ixNet getAttr $isisTrafficEngineering2 -metricLevel]/singleValue -value "55"
ixNet commit

puts "Setting Maximum Bandwidth Value for Traffic Engineering under ISISL3-IF in DG1"
ixNet setAttr [ixNet getAttr $isisTrafficEngineering1 -maxBandwidth]/singleValue -value "126000000"
ixNet commit

puts "Setting Maximum Bandwidth Value for Traffic Engineering under ISISL3-IF in DG2"
ixNet setAttr [ixNet getAttr $isisTrafficEngineering2 -maxBandwidth]/singleValue -value "127000000"
ixNet commit

puts "Setting Maximum Reservable Bandwidth Value for Traffic Engineering under ISISL3-IF in DG1"
ixNet setAttr [ixNet getAttr $isisTrafficEngineering1 -maxReservableBandwidth]/singleValue -value "128000000"
ixNet commit

puts "Setting Maximum Reservable Bandwidth Value for Traffic Engineering under ISISL3-IF in DG2"
ixNet setAttr [ixNet getAttr $isisTrafficEngineering2 -maxReservableBandwidth]/singleValue -value "129000000"
ixNet commit

puts "Setting Administrator Group Value for Traffic Engineering under ISISL3-IF in DG1"
ixNet setAttr [ixNet getAttr $isisTrafficEngineering1 -administratorGroup]/singleValue -value "22"
ixNet commit

puts "Setting Administrator Group Value for Traffic Engineering under ISISL3-IF in DG2"
ixNet setAttr [ixNet getAttr $isisTrafficEngineering2 -administratorGroup]/singleValue -value "33"
ixNet commit

################################################################################
# Enabling Segment Routing in Emulated Router
################################################################################
puts "Enabling Segment Routing for ISIS"
ixNet setAttr $isisL3Router1 -enableSR true

ixNet setAttr $isisL3Router2 -enableSR true
ixNet commit

################################################################################
# Setting SRGB range and SID Count for Emulated Router
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

################################################################################
# Enabling Segment Routing Algorithm in Emulated Router
################################################################################

puts "Enabling Segment Routing Algorithm in Emulated Router1"
set isisSRAlgorithmList [ixNet getList $isisL3Router1_1 isisSRAlgorithmList]
ixNet setAttr [ixNet getAttr $isisSRAlgorithmList -isisSrAlgorithm]/singleValue -value "30"
ixNet commit

puts "Enabling Segment Routing Algorithm in Emulated Router2"
set isisSRAlgorithmList [ixNet getList $isisL3Router1_1 isisSRAlgorithmList]
ixNet setAttr [ixNet getAttr $isisSRAlgorithmList -isisSrAlgorithm]/singleValue -value "60"
ixNet commit

################################################################################
# Adding BGP and Enabling BGPLS
################################################################################

puts "Adding BGP over IP4 stack"
ixNet add $ip1 bgpIpv4Peer
ixNet add $ip2 bgpIpv4Peer
ixNet commit

set bgp1 [ixNet getList $ip1 bgpIpv4Peer]
set bgp2 [ixNet getList $ip2 bgpIpv4Peer]

puts "Enabling BGPLS Capability"
set cap1 [ixNet getAttr $bgp1 -capabilityLinkStateNonVpn]
set cap2 [ixNet getAttr $bgp2 -capabilityLinkStateNonVpn]
set sv1 [ixNet getList $cap1 singleValue]
set sv2 [ixNet getList $cap2 singleValue]
ixNet setAttr $sv1 -value true
ixNet setAttr $sv2 -value true

puts "Enabling BGPLS Filter Link State"
set filter1 [ixNet getAttr $bgp1 -filterLinkState]
set filter2 [ixNet getAttr $bgp2 -filterLinkState]
set sv1 [ixNet getList $filter1 singleValue]
set sv2 [ixNet getList $filter2 singleValue]
ixNet setAttr $sv1 -value true
ixNet setAttr $sv2 -value true

puts "Setting IPs in BGP DUT IP tab"
ixNet setAttr [ixNet getAttr $bgp1 -dutIp]/singleValue -value "20.20.20.1"
ixNet setAttr [ixNet getAttr $bgp2 -dutIp]/singleValue -value "20.20.20.2"
ixNet commit

#Adding Network Group behind ISIS Device Group1
#Adding Prefix Pool behind ISIS Device Group2

puts "Adding Network Group behind ISIS Device Group1"
ixNet exec createDefaultStack $t1devices networkTopology
after 5000
set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
ixNet setAttr $networkGroup1 -name "ISIS_Network_Group1"
ixNet commit


################################################################################
# Enabling Segment Routing in simulated router
################################################################################
puts "Enabling Segment Routing in Simulated Routers on Network Group behind Device Group1"
set networkTopo1 [ixNet getList $networkGroup1 networkTopology]
set simRouter1 [ixNet getList $networkTopo1 simRouter]
set isisPseudoRouter1 [ixNet getList $simRouter1 isisL3PseudoRouter]
ixNet setAttribute $isisPseudoRouter1 -enableSR true
ixNet commit

puts "Set Value for SID/Index/Label"
ixNet setAttr [ixNet getAttr $isisPseudoRouter1 -sIDIndexLabel]/singleValue -value "100"
ixNet commit

puts "Set Value for Start SID/Label-1"
set isisSRGBRangeSubObjectsList [ixNet getList $isisPseudoRouter1 isisSRGBRangeSubObjectsList]
ixNet setMultiAttr [ixNet getAttr $isisSRGBRangeSubObjectsList -startSIDLabel]/counter\
        -direction  increment                        \
        -start      {116000}              \
        -step       {100}

ixNet commit

puts "Set Value for Start SID Count-1"
ixNet setAttr [ixNet getAttr $isisSRGBRangeSubObjectsList -sIDCount]/singleValue -value "9000"
ixNet commit


puts "Enabling Adj-Sid in Simulated Interface on Network Group behind Device Group2"
set simInterface1 [ixNet getList $networkTopo1 simInterface]
set isisL3PseudoInterface1 [ixNet getList $simInterface1 isisL3PseudoInterface]

set adj_sid [ixNet getAttr $isisL3PseudoInterface1 -enableAdjSID]
ixNet setAttr $adj_sid/singleValue -value True
ixNet commit

puts "Set IPv6 Adj-SID value for Simulated Interface"
set ipv6SidValue1 [ixNet getAttr $isisL3PseudoInterface1 -ipv6SidValue]
set svAdjSID2 [ixNet add $ipv6SidValue1 singleValue]
ixNet setAttr $svAdjSID2 -value 8000::1
ixNet commit

################################################################################
# Traffic Engineering Configuration for ISIS Simulated Routers
################################################################################

puts "Enabling TE on Simulated Router"
ixNet setAttr [ixNet getAttr $isisPseudoRouter1 -enable]/singleValue -value true
ixNet commit

puts "Enabling Metric Level for Traffic Engineering under ISISL3-IF in DG1"
ixNet setAttr [ixNet getAttr $isisL3PseudoInterface1 -metricLevel]/singleValue -value "67"
ixNet commit


puts "Setting Maximum Bandwidth Value for Traffic Engineering under ISISL3-IF in DG1"
ixNet setAttr [ixNet getAttr $isisL3PseudoInterface1 -maxBandwidth_Bps]/singleValue -value "136000000"
ixNet commit


puts "Setting Maximum Reservable Bandwidth Value for Traffic Engineering under ISISL3-IF in DG1"
ixNet setAttr [ixNet getAttr $isisL3PseudoInterface1 -maxReservableBandwidth_Bps]/singleValue -value "138000000"
ixNet commit

puts "Setting Administrator Group Value for Traffic Engineering under ISISL3-IF in DG1"
ixNet setAttr [ixNet getAttr $isisL3PseudoInterface1 -administratorGroup]/singleValue -value "77"
ixNet commit

################################################################################
# Start ISIS protocol and wait for 60 seconds
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
puts "***************************************************\n"

###############################################################################
# Retrieve protocol learned info in Port 1
###############################################################################

ixNet exec getLinkStateLearnedInfo $bgp2 1
after 5000

puts "Print BGP-LS Node/Link Learned Info"
set learnedInfoList [ixNet getList $bgp2 learnedInfo]
set learnedInfo [lindex $learnedInfoList end]
set table [lindex [ixNet getList $learnedInfo table] 0]
set learnedInfoColumnsList [ixNet getAttr $table -columns]
set learnedInfoValuesList [ixNet getAttr $table -values]
set row2 [lindex $learnedInfoValuesList 1]
puts "***************************************************"
foreach v $learnedInfoColumnsList {
    puts $v
}
puts "***************************************************"

puts "***************************************************"
foreach v $row2 {
    puts $v
}
puts "***************************************************"

puts "Print BGP-LS IPv4 Prefix Learned Info"
set learnedInfoList [ixNet getList $bgp2 learnedInfo]
set learnedInfo [lindex $learnedInfoList end]
set table [lindex [ixNet getList $learnedInfo table] 1]
set learnedInfoColumnsList [ixNet getAttr $table -columns]
set learnedInfoValuesList [ixNet getAttr $table -values]
set row2 [lindex $learnedInfoValuesList 1]
puts "***************************************************"
foreach v $learnedInfoColumnsList {
    puts $v
}
puts "***************************************************"

puts "***************************************************"
foreach v $row2 {
    puts $v
}
puts "***************************************************"

puts "Print BGP-LS IPv6 Prefix Learned Info"
set learnedInfoList [ixNet getList $bgp2 learnedInfo]
set learnedInfo [lindex $learnedInfoList end]
set table [lindex [ixNet getList $learnedInfo table] 2]
set learnedInfoColumnsList [ixNet getAttr $table -columns]
set learnedInfoValuesList [ixNet getAttr $table -values]
set row2 [lindex $learnedInfoValuesList 1]

puts "***************************************************"
foreach v $learnedInfoColumnsList {
    puts $v
}
puts "***************************************************"

puts "***************************************************"
foreach v $row2 {
    puts $v
}
puts "***************************************************"

################################################################################
#  Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"

