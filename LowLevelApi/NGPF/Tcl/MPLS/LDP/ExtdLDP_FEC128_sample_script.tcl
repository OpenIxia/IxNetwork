#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/10/2014 - Alka pattnaik - created sample                               #
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

######################################################################################
#                                                                                    #
# Description:                                                                       #
#    This script intends to demonstrate how to use NGPF LDP API.                     #
#                                                                                    #
# About Topology:							                                         #
#          Within toplogy both Provider Edge(PE) and Provider(P) Routers are created.#
# created.P router is emulated in the front Device Group(DG), which consists of both #
# OSPF as routing protocol as well as Basic LDP sessions for Transport Label         #
# Distribution Protocol. The chained DG act as PE Router, where LDP Extended Martini #
# is configured for VPN Label distibution protocol.Bidirectional L2-L3 Traffic is    #
# configured in between two CE cloud and L4-L7 AppLib Traffic are created            #
#	 Script Flow:			                                                         #
#	 1. Configuration of protocols.	                                                 #
#    Configuration flow of the script is as follow:                                  #
# 		i.    Adding of OSPF router.			        	                         #
# 		ii.   Adding of Network Cloud.      				                         #
# 		iii.  Adding of chain DG.					                                 #
# 		iv.   Adding of LDP(basic session) on Front DG 		                         #
# 		v.    Adding of LDP Extended Martini(Targeted sess.) over chained DG.        #
# 		vi.   Adding of LDP PW/VPLS Tunnel over LDP Extended Martini.	             #
#    2. Start the ldp protocol.                                                      #
#    3. Retrieve protocol statistics.                                         	     #
#    4. Retrieve protocol learned info.                                              #
#    5. Disbale/Enable the ldp FECs and change label & apply change on the fly       #
#    6. Retrieve protocol learned info again and notice the difference with          #
#       previouly retrieved learned info.                                            #
#    7. Configure L2-L3 traffic.                                                     #
#    8. Start the L2-L3 traffic.                                                     #
#    9. Retrieve L2-L3 traffic stats.                                                #
#   10. Stop L2-L3 traffic.                                                          #
#   11. Stop all protocols.                                                          #
# Ixia Software:                                                                     #
#    IxOS      6.80 EB (6.80.1101.116)                                               #
#    IxNetwork 7.40 EB (7.40.929.3)                                                  #
#                                                                                    #
######################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.216.108.49
    set ixTclPort   8999
    set ports       {{10.216.102.209 1 3} { 10.216.102.209 1 4}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.40\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Configuration of protocols as per above mentioned flow.
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
after 10000
puts "Adding 2 topologies"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet add [ixNet getRoot] topology -vports $vportRx
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "Topology for FEC128 1"
ixNet setAttr $topo2  -name "Topology for FEC128 2"

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

puts "configuring ipv4 addresses"
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
# **********************************************************************************
puts "Adding LDP over IP4 stacks"
ixNet add $ip1 ldpBasicRouter
ixNet add $ip2 ldpBasicRouter
ixNet commit

set ldp1 [ixNet getList $ip1 ldpBasicRouter]
set ldp2 [ixNet getList $ip2 ldpBasicRouter]

ixNet setAttr $t1dev1 -name "Provider Router 1"
ixNet setAttr $t2dev1 -name "Provider Router 2"
ixNet commit

# puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp]"
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
# **********************************************************************************

puts "Adding NetworkGroup behind ldp DG"
ixNet exec createDefaultStack $t1devices ipv4PrefixPools
ixNet exec createDefaultStack $t2devices ipv4PrefixPools

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

ixNet setAttr $networkGroup1 -name "Network Cloud 1"
ixNet setAttr $networkGroup2 -name "Network Cloud 2"
ixNet setAttr $networkGroup1 -multiplier "1"
ixNet setAttr $networkGroup2 -multiplier "1"
ixNet commit

#Change IP address and Prefix Of Network Group 
set ipV4PrefixPools1 [lindex [ixNet getList $networkGroup1 ipv4PrefixPools] 0]
set ipV4PrefixPools2 [lindex [ixNet getList $networkGroup2 ipv4PrefixPools] 0]
set prefixLength1 [ixNet getAttribute $ipV4PrefixPools1 -prefixLength]
set prefixLength2 [ixNet getAttribute $ipV4PrefixPools2 -prefixLength]

ixNet setMultiAttribute $prefixLength1\
    -clearOverlays false\
    -pattern singleValue
	
ixNet setMultiAttribute $prefixLength2\
    -clearOverlays false\
    -pattern singleValue
ixNet commit

set prefix1 [ixNet add $prefixLength1 "singleValue"]
set prefix2 [ixNet add $prefixLength2 "singleValue"]

ixNet setMultiAttribute $prefix1\
        -value 32
ixNet setMultiAttribute $prefix2\
        -value 32
ixNet commit
set addressSet1 [ixNet getAttribute $ipV4PrefixPools1 -networkAddress]
set addressSet2 [ixNet getAttribute $ipV4PrefixPools2 -networkAddress]
ixNet setMultiAttribute $addressSet1\
    -clearOverlays false\
    -pattern counter
ixNet setMultiAttribute $addressSet2\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet1 [ixNet add $addressSet1 "counter"]
set addressSet2 [ixNet add $addressSet2 "counter"]
ixNet setMultiAttribute $addressSet1\
    -step 0.0.0.1\
    -start 200.1.0.1\
    -direction increment
	
ixNet setMultiAttribute $addressSet2\
    -step 0.0.0.1\
    -start 201.1.0.1\
    -direction increment
ixNet commit

# Add ipv4 loopback1 for PE Router
puts "Adding ipv4 loopback1 for configuring PE Routers above it."
set chainedDg1 [ixNet add $networkGroup1 deviceGroup]
ixNet setMultiAttribute $chainedDg1\
    -multiplier 1\
    -name {Provider Edge Router 1}
ixNet commit
set chainedDg1 [lindex [ixNet remapIds $chainedDg1] 0]

set loopback1 [ixNet add $chainedDg1 "ipv4Loopback"]
ixNet setMultiAttribute $loopback1\
    -stackedLayers [list]\
    -name {IPv4 Loopback 1}
ixNet commit

set connector1 [ixNet add $loopback1 "connector"]
ixNet setMultiAttribute $connector1\
    -connectedTo $networkGroup1/ipv4PrefixPools:1
ixNet commit
set connector1 [lindex [ixNet remapIds $connector1] 0]

set addressSet3 [ixNet getAttribute $loopback1 -address]
ixNet setMultiAttribute $addressSet3\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet3 [ixNet add $addressSet3 "counter"]
ixNet setMultiAttribute $addressSet3\
    -step 0.0.0.1\
    -start 200.1.0.1\
    -direction increment
ixNet commit
set addressSet3 [lindex [ixNet remapIds $addressSet3] 0]

# Add ipv4 loopback2 for PE Router
puts "Adding ipv4 loopback2 for configuring PE Routers above it."
set chainedDg2 [ixNet add $networkGroup2 deviceGroup]
ixNet setMultiAttribute $chainedDg2\
    -multiplier 1\
    -name "Provider Edge Router 2"
ixNet commit
set chainedDg2 [lindex [ixNet remapIds $chainedDg2] 0]

set loopback2 [ixNet add $chainedDg2 "ipv4Loopback"]
ixNet setMultiAttribute $loopback2\
    -stackedLayers [list]\
    -name {IPv4 Loopback 2}
ixNet commit

set connector2 [ixNet add $loopback2 "connector"]
ixNet setMultiAttribute $connector2\
    -connectedTo $networkGroup2/ipv4PrefixPools:1
ixNet commit
set connector1 [lindex [ixNet remapIds $connector2] 0]

set addressSet4 [ixNet getAttribute $loopback2 -address]
ixNet setMultiAttribute $addressSet4\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet4 [ixNet add $addressSet4 "counter"]
ixNet setMultiAttribute $addressSet4\
    -step 0.0.0.1\
    -start 201.1.0.1\
    -direction increment
ixNet commit
set addressSet4 [lindex [ixNet remapIds $addressSet4] 0]


################################################################################
# 2. Add LDP targeted(Extended Martini) Router
################################################################################

ixNet add $loopback1 ldpTargetedRouter
ixNet add $loopback2 ldpTargetedRouter
ixNet commit

set ldpTargeted1 [ixNet getList $loopback1 ldpTargetedRouter]
set ldpTargeted2 [ixNet getList $loopback2 ldpTargetedRouter]
set ldpTargetedPeer1 [ixNet getList $ldpTargeted1 ldpTargetedPeer]
set ldpTargetedPeer2 [ixNet getList $ldpTargeted2 ldpTargetedPeer]
#puts "ixNet help ::ixNet::OBJ-/topology:2/deviceGroup:2/networkGroup:2/deviceGroup:1/ipv4Loopback:1/ldpTargetedRouter:1/ldpTargetedPeer"
#puts "[ixNet help ::ixNet::OBJ-/topology:2/deviceGroup:2/networkGroup:2/deviceGroup:1/ipv4Loopback:1/ldpTargetedRouter:1/ldpTargetedPeer]"

set addressSet5 [ixNet getAttribute $ldpTargetedPeer1 -iPAddress]
ixNet setMultiAttribute $addressSet5\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet5 [ixNet add $addressSet5 "counter"]
ixNet setMultiAttribute $addressSet5\
    -step 0.0.0.1\
    -start 201.1.0.1\
    -direction increment
ixNet commit

set addressSet6 [ixNet getAttribute $ldpTargetedPeer2 -iPAddress]
ixNet setMultiAttribute $addressSet6\
    -clearOverlays false\
    -pattern counter
ixNet commit

set addressSet6 [ixNet add $addressSet6 "counter"]
ixNet setMultiAttribute $addressSet6\
    -step 0.0.0.1\
    -start 200.1.0.1\
    -direction increment
ixNet commit

#Add LDP FEC128(PW/VPLS) on top of LDP targeted Router
set ldppwvpls1 [ixNet add $ldpTargeted1 "ldppwvpls"]
set ldppwvpls2 [ixNet add $ldpTargeted2 "ldppwvpls"]
ixNet commit

#puts "ixNet help ::ixNet::OBJ-/topology:1/deviceGroup:1/networkGroup:1/deviceGroup:1/ipv4Loopback:1/ldpTargetedRouter:1/ldppwvpls:1"
#puts ["ixNet help ::ixNet::OBJ-/topology:1/deviceGroup:1/networkGroup:1/deviceGroup:1/ipv4Loopback:1/ldpTargetedRouter:1/ldppwvpls:1]"
set ldppwvpls1 [lindex [ixNet remapIds $ldppwvpls1] 0]
set ldppwvpls2 [lindex [ixNet remapIds $ldppwvpls2] 0]

set peerId1 [ixNet getAttribute $ldppwvpls1 -peerId]
ixNet setMultiAttribute $peerId1\
    -clearOverlays false\
    -pattern counter
ixNet commit

set peerId1 [ixNet add $peerId1 "counter"]
ixNet setMultiAttribute $peerId1\
    -step 0.0.0.1\
    -start 201.1.0.1\
    -direction increment
ixNet commit
set peerId2 [ixNet getAttribute $ldppwvpls2 -peerId]
ixNet setMultiAttribute $peerId2\
    -clearOverlays false\
    -pattern counter
ixNet commit

set peerId2 [ixNet add $peerId2 "counter"]
ixNet setMultiAttribute $peerId2\
    -step 0.0.0.1\
    -start 200.1.0.1\
    -direction increment
ixNet commit

################################################################################
# 3. Add MAC Cloud behind LDP PWs
################################################################################
ixNet exec createDefaultStack $chainedDg1 macPools
ixNet exec createDefaultStack $chainedDg2 macPools
ixNet commit

set macPools1 [lindex [ixNet getList $chainedDg1 networkGroup] 0]
set macPools2 [lindex [ixNet getList $chainedDg2 networkGroup] 0]
puts "Renaming MAC Cloud"
ixNet setAttr $macPools1 -name "CE MAC Cloud 1"
ixNet setAttr $macPools2 -name "CE MAC Cloud 2"
ixNet commit
################################################################################
# 4. Start LDP protocol and wait for 60 seconds
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000

################################################################################
# 5. Retrieve protocol statistics.
################################################################################
puts "Fetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Protocols Summary"/page}
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

###############################################################################
# 6. Retrieve protocol learned info
###############################################################################
puts "Fetching LDP Basic Learned Info"
ixNet exec getIPv4FECLearnedInfo $ldp1 1
#ixNet exec getAllLearnedInfo $ldp1 
after 5000
set linfo1 [ixNet getList $ldp1 learnedInfo]
ixNet getAttr $linfo1 -columns
set values [ixNet getAttribute $linfo1 -values]

puts "Fetching FEC 128 Learned Info"
ixNet exec  getFEC128LearnedInfo $ldpTargeted2 1
set linfo2 [ixNet getList $ldpTargeted2 learnedInfo]
ixNet getAttr $linfo2 -columns
set values [ixNet getAttribute $linfo2 -values]

##########################################################################################
# 7. Change the labels of VPN Label in PW/VPLS element And apply changes On The Fly (OTF).
##########################################################################################
set feclabel1 [ixNet getAttribute $ldppwvpls1 -label]
ixNet setMultiAttribute $feclabel1\
    -clearOverlays false\
    -pattern counter
ixNet commit

set feclabel1 [ixNet add $feclabel1 "counter"]
ixNet setMultiAttribute $feclabel1\
    -step 100\
    -start 5001\
    -direction increment
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
# 8. Retrieve protocol learned info again and compare with
#    previouly retrieved learned info.  
###############################################################################

puts "Fetching FEC 128 Learned Info"
ixNet exec  getFEC128LearnedInfo $ldpTargeted2 1
set linfo2 [ixNet getList $ldpTargeted2 learnedInfo]
ixNet getAttr $linfo2 -columns
set values [ixNet getAttribute $linfo2 -values]
puts "***************************************************"

################################################################################
# 9. Configure L2-L3 traffic 
################################################################################
puts "Configuring L2-L3 Traffic Item"
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {Traffic Item 1}           \
    -roundRobinPacketOrdering false  \
    -trafficType ethernetVlan        \
	-biDirectional 1
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source [list $networkGroup1]
set destination [list $networkGroup2]


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
    -trackBy        [list sourceDestEndpointPair0 trackingenabled0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]
ixNet commit

# puts "ixNet help [ixNet getRoot]/traffic"
# puts "[ixNet help [ixNet getRoot]/traffic]"

###############################################################################
# 10. Apply and start L2/L3 traffic
###############################################################################
puts "applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

puts "Let traffic run for 1 minute"
after 60000

###############################################################################
# 11. Retrieve L2/L3 traffic item statistics
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

################################################################################
# 12. Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 13. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
