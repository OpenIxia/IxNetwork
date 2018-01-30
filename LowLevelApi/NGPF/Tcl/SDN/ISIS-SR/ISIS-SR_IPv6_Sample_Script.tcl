#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           # 
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    11/17/2016 - Rupam Paul - created sample                                  #
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
#    This script intends to demonstrate how to use NGPF IPv6 SR Low Level      #
#    TCL API.                                                                  #
#                                                                              #
#    1. It will create 2 ISIS topologies, topology2 will have                  #
#       IPv6 prefix pool & Simulated Topology.                                 #
#    2. Enable SR and SR IPv6 in ISIS Emulated Router.                         #
#    3. Set IPv6 Node Prefix & IPv6 Adj-Sid.                                   #
#    4. Enable Segment Routing in Simulated Router and                         #
#       Set IPv6 Node Prefix & IPv6 Adj-Sid in Simulated Router.               #  
#    5. Start protocol.                                                        #
#    6. Retrieve protocol statistics.                                          #
#    7. Retrieve protocol learned info in Port1.                               #
#    8. On the fly disable Adj-Sid in Simulated Interface.                     #
#    9. Retrieve protocol learned info in Port1 after On the Fly change.       #
#    10. Stop all protocols.                                                   #
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
    set ports       {{10.216.108.99 11  3} { 10.216.108.99  11  4}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.00\
   -setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
#  Protocol configuration section. Configure ISIS as per the description
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
puts "Add ipv6"
ixNet add $mac1 ipv6
ixNet add $mac2 ipv6
ixNet commit

set ip1 [ixNet getList $mac1 ipv6]
set ip2 [ixNet getList $mac2 ipv6]

set mvAdd1 [ixNet getAttr $ip1 -address]
set mvAdd2 [ixNet getAttr $ip2 -address]
set mvGw1  [ixNet getAttr $ip1 -gatewayIp]
set mvGw2  [ixNet getAttr $ip2 -gatewayIp]

puts "Configuring ipv6 addresses"
ixNet setAttr $mvAdd1/singleValue -value "2000::1"
ixNet setAttr $mvAdd2/singleValue -value "2000::101"
ixNet setAttr $mvGw1/singleValue  -value "2000::101"
ixNet setAttr $mvGw2/singleValue  -value "2000::1"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 64
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 64

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

# Disable Discard Learned LSP
puts "Disabling the Discard Learned Info CheckBox"

set isisL3RouterDiscardLearnedLSP1 [ ixNet getAttr [ixNet getList [ixNet getList $topo1 deviceGroup] isisL3Router] -discardLSPs]
set isisL3RouterDiscardLearnedLSP2 [ ixNet getAttr [ixNet getList [ixNet getList $topo2 deviceGroup] isisL3Router] -discardLSPs]

ixNet setAttr $isisL3RouterDiscardLearnedLSP1 -pattern singleValue -clearOverlays False
ixNet setAttr $isisL3RouterDiscardLearnedLSP1/singleValue -value False
ixNet setAttr $isisL3RouterDiscardLearnedLSP2 -pattern singleValue -clearOverlays False
ixNet setAttr $isisL3RouterDiscardLearnedLSP2/singleValue -value False


################################################################################
# Enabling Segment Routing in Emulated Router
################################################################################
puts "Enabling Segment Routing for ISIS"
ixNet setAttr $isisL3Router1 -enableSR true

ixNet setAttr $isisL3Router2 -enableSR true
ixNet commit

################################################################################
# Enabling SR-IPv6 Flag under Segnment Routing Tab in ISIS-L3 RTR
################################################################################
puts "Enabling SR-IPv6 Flag under Segment Routing Tab"

set sr_ipv6_flag1 [ixNet getAttr $isisL3Router1 -ipv6Srh]
ixNet setAttr $sr_ipv6_flag1/singleValue -value True
ixNet commit

set sr_ipv6_flag2 [ixNet getAttr $isisL3Router2 -ipv6Srh]
ixNet setAttr $sr_ipv6_flag2/singleValue -value True
ixNet commit


################################################################################
# Setting IPv6 Node Prefix Address
################################################################################
puts "Setting IPv6 Node Prefix Address"

set ipv6_node_prefix_add1 [ixNet getAttr $isisL3Router1 -ipv6NodePrefix]
ixNet setAttr $ipv6_node_prefix_add1/singleValue -value 3000::1
ixNet commit

set ipv6_node_prefix_add2 [ixNet getAttr $isisL3Router2 -ipv6NodePrefix]
ixNet setAttr $ipv6_node_prefix_add2/singleValue -value 4000::101
ixNet commit

################################################################################
# Enabling Adj-Sid under Segnment Routing Tab in ISIS-L3 IF
################################################################################

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

puts "Set IPv6 Adj-SID value in first Emulated Router"
set ipv6SidValue1 [ixNet getAttr $isisL3_1 -ipv6SidValue]
set svAdjSID1 [ixNet add $ipv6SidValue1 singleValue]
ixNet setAttr $svAdjSID1 -value 5000::1
ixNet commit

puts "Set IPv6 Adj-SID value in second Emulated Router"
set ipv6SidValue2 [ixNet getAttr $isisL3_2 -ipv6SidValue]
set svAdjSID2 [ixNet add $ipv6SidValue2 singleValue]
ixNet setAttr $svAdjSID2 -value 6000::1
ixNet commit

puts "Adding Network Group behind ISIS Device Group2"
ixNet exec createDefaultStack $t2devices networkTopology
after 5000
set networkGroup1 [lindex [ixNet getList $t2devices networkGroup] 0]
set networkGroup2 [lindex [ixNet add $t2devices networkGroup] 0]

ixNet setAttr $networkGroup1 -name "ISIS_Network_Group1"
ixNet commit

puts "Adding IPv6 Prefix Pool behind ISIS Device Group2"
set ipv6PrefixPools [lindex [ixNet add $networkGroup2 ipv6PrefixPools] 0]
after 2000
ixNet commit
ixNet setA $networkGroup2 -multiplier 1
ixNet commit

ixNet setAttr $networkGroup2 -name "ISIS_IPv6_Prefix_Pools"
ixNet commit

puts "Enabling Advertise IPv6 SID under IPv6 PrefixPool"
set isisL3RouteProperty [ixNet add $ipv6PrefixPools isisL3RouteProperty]
set ipv6Srh [ixNet getAttr $isisL3RouteProperty -ipv6Srh]
set svipv6Srh [ixNet add $ipv6Srh singleValue]
ixNet setAttr $svipv6Srh -value True
ixNet commit


################################################################################
# Enabling Segment Routing in simulated router
################################################################################
puts "Enabling Segment Routing in Simulated Routers on Network Group behind Device Group2"
set networkTopo1 [ixNet getList $networkGroup1 networkTopology]
set simRouter1 [ixNet getList $networkTopo1 simRouter]
set isisPseudoRouter1 [ixNet getList $simRouter1 isisL3PseudoRouter]
ixNet setAttribute $isisPseudoRouter1 -enableSR true
ixNet commit

puts "Enabling SR-IPv6 Flag in Simulated Routers on Network Group behind Device Group2"

set sr_ipv6_flag1 [ixNet getAttr $isisPseudoRouter1 -ipv6Srh]
ixNet setAttr $sr_ipv6_flag1/singleValue -value True
ixNet commit

puts "Setting IPv6 Node Prefix Address in Simulated Routers on Network Group behind Device Group2"

set ipv6_node_prefix_add1 [ixNet getAttr $isisPseudoRouter1 -ipv6NodePrefix]
set svSID2 [ixNet add $ipv6_node_prefix_add1 singleValue]
ixNet setAttr $svSID2 -value 7000::1
ixNet commit

puts "Enabling Adj-Sid in Simulated Interface on Network Group behind Device Group2"
set networkTopo1 [ixNet getList $networkGroup1 networkTopology]
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

puts "Fetching ISIS SR IPv6 Prefix Learned Info in Port 1"
ixNet exec getLearnedInfo $isisL3_1 
after 5000
set learnedInfoList [ixNet getList $isisL3_1 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]
set IPv6SrLInfo [lindex $linfoList 2]

puts "***************************************************"
foreach table $IPv6SrLInfo {
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

puts "Fetching ISIS SR IPv6 Adjacency Learned Info in Port 1"
ixNet exec getLearnedInfo $isisL3_1 
after 5000
set IPv6SrAdjLInfo [lindex $linfoList 3]

puts "***************************************************"
foreach table $IPv6SrAdjLInfo {
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
# Setting on the fly change of IPv6 Node Prefix Address in Simulated Router
################################################################################
puts "Setting on the fly change of IPv6 Node Prefix Address in Simulated Router"
set enableAdjSID1 [ixNet getAttr $isisL3_1 -enableAdjSID]
set svAdjSID1 [ixNet add $enableAdjSID1 singleValue]
ixNet setAttr $svAdjSID1 -value false
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
    puts "$::errorInfo"
}
after 5000

###############################################################################
# Retrieve protocol learned info
###############################################################################

puts "Fetching ISIS SR IPv6 Adjacency Learned Info in Port 1"
ixNet exec getLearnedInfo $isisL3_1 
after 5000
set IPv6SrAdjLInfo [lindex $linfoList 3]

puts "***************************************************"
foreach table $IPv6SrAdjLInfo {
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
# Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"

