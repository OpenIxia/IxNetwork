#/usr/bin/tclsh

################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/17/2014 - Deepak Kumar Singh - created sample                          #
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
#    This script intends to demonstrate how to use NGPF OSPFv3 TCL APIs.       #
#                                                                              #
#    1. It will create 2 OSPFv3 topologies, each having an ipv6 network        #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. A loopback device group(DG) behind network   # 
#       group is needed to support applib traffic.                             #
#    2. Start the ospfv3 protocol.                                             #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Enable the OSPFv3 Simulated Inter Area Prefix, which                   #
#       was disabled by default and apply change on the fly.                   #
#    6. Retrieve protocol learned info again and notice the difference with    #
#       previouly retrieved learned info.                                      #
#    7. Configure L2-L3 traffic.                                               #
#    8. Configure application traffic.                                         #
#    9. Start the L2-L3 traffic.                                               #
#   10. Start the application traffic.                                         #
#   11. Retrieve Appilcation traffic stats.                                    #
#   12. Retrieve L2-L3 traffic stats.                                          #
#   13. Stop L2-L3 traffic.                                                    #
#   14. Stop Application traffic.                                              #
#   15. Stop all protocols.                                                    #                                                                                          
# Ixia Softwares:                                                              #
#    IxOS      6.80 EB (6.80.1101.116)                                         #
#    IxNetwork 7.40 EB (7.40.929.3)                                            #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.205.28.84
    set ixTclPort   8345
    set ports       {{10.205.28.35 1 9} { 10.205.28.35 1 10}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.40\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure OSPFv3 as per the description
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

puts "configuring ipv6 addresses"
ixNet setAttr $mvAdd1/singleValue -value "2000:0:0:1:0:0:0:1"
ixNet setAttr $mvAdd2/singleValue -value "2000:0:0:1:0:0:0:2"
ixNet setAttr $mvGw1/singleValue  -value "2000:0:0:1:0:0:0:2"
ixNet setAttr $mvGw2/singleValue  -value "2000:0:0:1:0:0:0:1"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 64
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 64

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6]"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6]"

puts "Adding OSPFv3 over IPv6 stacks"
ixNet add $ip1 ospfv3
ixNet add $ip2 ospfv3
ixNet commit

set ospf1 [ixNet getList $ip1 ospfv3]
set ospf2 [ixNet getList $ip2 ospfv3]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "OSPFv3 Topology 1"
ixNet setAttr $topo2  -name "OSPFv3 Topology 2"

ixNet setAttr $t1dev1 -name "OSPFv3 Topology 1 Router"
ixNet setAttr $t2dev1 -name "OSPFv3 Topology 2 Router"
ixNet commit

puts "Making the NetworkType to Point to Point in the first OSPFv3 router"
set networkTypeMultiValue1 [ixNet getAttr $ospf1 -networkType]
ixNet setAttr $networkTypeMultiValue1 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue1/singleValue -value pointtopoint

puts "Making the NetworkType to Point to Point in the Second OSPFv3 router"
set networkTypeMultiValue2 [ixNet getAttr $ospf2 -networkType]
ixNet setAttr $networkTypeMultiValue2 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue2/singleValue -value pointtopoint

puts "Disabling the Discard Learned Info CheckBox"

set ospfv3RouterDiscardLearnedLSA1\
    [ixNet getAttr [lindex [ixNet getList $t1devices ospfv3Router] 0] -discardLearnedLsa]

set ospfv3RouterDiscardLearnedLSA2\
    [ixNet getAttr [lindex [ixNet getList $t2devices ospfv3Router] 0] -discardLearnedLsa]

ixNet setAttr $ospfv3RouterDiscardLearnedLSA1 -pattern singleValue -clearOverlays False
ixNet setAttr $ospfv3RouterDiscardLearnedLSA1/singleValue -value False
ixNet setAttr $ospfv3RouterDiscardLearnedLSA2 -pattern singleValue -clearOverlays False
ixNet setAttr $ospfv3RouterDiscardLearnedLSA2/singleValue -value False

# puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6/ospfv3"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6/ospfv3]"

puts "Adding NetworkGroup behind OSPFv3 DG"
ixNet exec createDefaultStack $t1devices networkTopology
ixNet exec createDefaultStack $t2devices networkTopology

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

ixNet setAttr $networkGroup1 -name "OSPFv3_1_Network_Group1"
ixNet setAttr $networkGroup2 -name "OSPFv3_2_Network_Group1"
ixNet commit

# Add ipv6 loopback1 for applib traffic
puts "Adding ipv6 loopback1 for applib traffic"
set chainedDg1 [ixNet add $networkGroup1 deviceGroup]
ixNet setMultiAttribute $chainedDg1\
    -multiplier 7\
    -name {Device Group 4}
ixNet commit
set chainedDg1 [lindex [ixNet remapIds $chainedDg1] 0]

set loopback1 [ixNet add $chainedDg1 "ipv6Loopback"]
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
    -step 0:0:0:1:0:0:0:0\
    -start 3000:0:1:1:0:0:0:0\
    -direction increment
ixNet commit
set addressSet1 [lindex [ixNet remapIds $addressSet1] 0]

# Add ipv6 loopback2 for applib traffic
puts "Adding ipv6 loopback2 for applib traffic"
set chainedDg2 [ixNet add $networkGroup2 deviceGroup]
ixNet setMultiAttribute $chainedDg2\
    -multiplier 7\
    -name {Device Group 3}
ixNet commit
set chainedDg2 [lindex [ixNet remapIds $chainedDg2] 0]

set loopback2 [ixNet add $chainedDg2 "ipv6Loopback"]
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
    -step 0:0:0:1:0:0:0:0\
    -start 3000:5:1:1:0:0:0:0\
    -direction increment
ixNet commit
set addressSet2 [lindex [ixNet remapIds $addressSet2] 0]

################################################################################
# 2. Start OSPFv3 protocol and wait for 60 seconds
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
puts "Fetching OSPFv3 Basic Learned Info"
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
# 5. Enable the Ospfv3 Inter Area Prefix Simulated Routes, which
#    was disabled by default. And apply changes On The Fly (OTF).
################################################################################
puts "Enabling Inter Area Prefix Simulated Routes"
set netTopology1      [lindex [ixNet getList $networkGroup1 networkTopology] 0]
set simRouter1        [lindex [ixNet getList $netTopology1 simRouter] 0]
set ospfv3PseudoRouter1 [lindex [ixNet getList $simRouter1 ospfv3PseudoRouter] 0]
set interAreaPrefix1    [lindex [ixNet getList $ospfv3PseudoRouter1 interAreaPrefix] 0]
set activeMultivalue1 [ixNet getAttr $interAreaPrefix1 -active]
ixNet setAttribute $activeMultivalue1/singleValue -value true
ixNet commit

set netTopology2      [lindex [ixNet getList $networkGroup2 networkTopology] 0]
set simRouter2        [lindex [ixNet getList $netTopology2 simRouter] 0]
set ospfv3PseudoRouter2 [lindex [ixNet getList $simRouter2 ospfv3PseudoRouter] 0]
set interAreaPrefix2         [lindex [ixNet getList $ospfv3PseudoRouter2 interAreaPrefix] 0]
set activeMultivalue2 [ixNet getAttr $interAreaPrefix2 -active]
ixNet setAttribute $activeMultivalue2/singleValue -value true
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
# 6. Retrieve protocol learned info again and compare with
#    previouly retrieved learned info.  
###############################################################################
puts "Fetching OSPFv3 learned info after enabling OSPFv3 Inter Area Prefix Simulated Routes"
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
# 7. Configure L2-L3 traffic 
################################################################################
puts "Congfiguring L2-L3 Traffic Item"
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {Traffic Item 1}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv6
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $networkGroup1/networkTopology/simRouter:1/ospfv3PseudoRouter:1/interAreaPrefix:1]
set destination  [list $networkGroup2/networkTopology/simRouter:1/ospfv3PseudoRouter:1/interAreaPrefix:1]

ixNet setMultiAttribute $endpointSet1\
    -name                  "EndpointSet-1"\
    -multicastDestinations [list]\
    -scalableSources       [list]\
    -multicastReceivers    [list]\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               $source\
    -destinations          $destination\    
ixNet commit

ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy        [list sourceDestEndpointPair0 trackingenabled0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]\
ixNet commit

################################################################################
# 8. Configure Application traffic
################################################################################
puts "Configuring Applib traffic"
set trafficItem2 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem2  \
    -name {Traffic Item 2}             \
    -trafficItemType applicationLibrary\
    -roundRobinPacketOrdering false    \
    -trafficType ipv6ApplicationTraffic
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

# puts "ixNet help [ixNet getRoot]/traffic"
# puts "[ixNet help [ixNet getRoot]/traffic]"

###############################################################################
# 9. Apply and start L2/L3 traffic
###############################################################################
puts "applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

###############################################################################
# 10. Apply and start applib traffic
###############################################################################
puts "applying applib traffic"
ixNet exec applyStatefulTraffic  [ixNet getRoot]/traffic
after 5000

puts "starting applib traffic"
ixNet exec startStatefulTraffic [ixNet getRoot]/traffic
puts "Let traffic run for 1 minute"
after 60000

###############################################################################
# 11. Retrieve Applib traffic item statistics
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
# 12. Retrieve L2/L3 traffic item statistics
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
# 13. Stop applib traffic
#################################################################################
puts "Stopping applib traffic"
ixNet exec stopStatefulTraffic [ixNet getRoot]/traffic
after 5000

################################################################################
# 14. Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 15. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
