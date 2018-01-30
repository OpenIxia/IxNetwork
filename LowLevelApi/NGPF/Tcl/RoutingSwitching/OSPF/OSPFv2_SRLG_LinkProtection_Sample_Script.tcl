#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2016 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    21/09/2016 - Mamud Hasan - created sample                                 #
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
#    This script intends to demonstrate how to use NGPF OSPFv2 SRLG and Link   #
#    Protection TCL API.                                                       #
#                                                                              #
#    1. It will create 2 OSPFv2 topologies. Topology-1 will have a Linear      #
#       simulated topology.                                                    #
#    2. Enable Traffic Engineering in OSPF Emulated Router                     # 
#    3. Enable Shared Risk Link Group(SRLG) in OSPF Emulated Router.           #
#    4. Set SRLG Count and Provide SRLG Value in OSPF Emulated Router.         #
#    5. Enable Link Protection in OSPF Emulated Router.                        #
#    6. Set Link Protection Type in OSPF Emulated Router.                      #
#    7. Enable Traffic Engineering in OSPF Simulated Router                    #
#    8. Enable Shared Risk Link Group(SRLG) in OSPF Simulated Router.          #
#    9. Set SRLG Count and Provide SRLG Value in OSPF Simulated Router.        #
#   10. Enable Link Protection in OSPF Simulated Router.                       #
#   11. Set Link Protection Type in OSPF Simulated Router.                     #
#   12. Start Protocol                                                         #
#   13. Retrieve protocol statistics                                           #
#   14. Retrieve protocol learned info.                                        #
#   15. Stop all protocols.                                                    #                                                                                          
#                                                                              #
# Ixia Softwares:                                                              #
#    IxOS      8.10 EA (8.10.1046.6)                                           #
#    IxNetwork 8.10 EA (8.10.1250.4)                                           #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.216.22.18
    set ixTclPort   8009
    set ports       {{10.216.100.216 1 5} { 10.216.100.216 1 6}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.10\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure OSPFv2 as per the description   #
#    give above                                                                #
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

puts "Adding OSPFv2 over IP4 stacks"
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
ixNet commit
# puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2]"

puts "Adding a Linear ST on OSPF Topology 1"
set networkGroup1 [ ixNet add $t1devices networkGroup ]
ixNet commit
set networkTopology1 [ixNet add $networkGroup1  networkTopology ]
ixNet commit
set lineartopo [ixNet add $networkTopology1 netTopologyLinear ]
ixNet commit

ixNet setAttr $networkGroup1 -name "OSPF Linear Topology 1"
ixNet commit

################################################################################
# 2. Enable Traffic Engineering in OSPF Emulated Router.                       #           
################################################################################
puts "Enabling TE in OSPF Topology 1 Router"
set ospf1TE [ixNet getList $ospf1 ospfTrafficEngineering]
set enTE1 [ixNet getAttribute $ospf1TE -enable]
set TE1_singleValue [ixNet getList $enTE1 singleValue]
ixNet setAttr $TE1_singleValue -value true
ixNet commit

puts "Enabling TE in OSPF Topology 2 Router"
set ospf2TE [ixNet getList $ospf2 ospfTrafficEngineering]
set enTE2 [ixNet getAttribute $ospf2TE -enable]
set TE2_singleValue [ixNet getList $enTE2 singleValue]
ixNet setAttr $TE2_singleValue -value true
ixNet commit

################################################################################
# 3. Enable Shared Risk Link Group(SRLG) in OSPF Emulated Router.              #           
################################################################################
puts "Enabling SRLG in OSPF Topology 1 Router"
set enSRLG1 [ixNet getAttribute $ospf1 -enableSRLG]
set SRLG1_singleValue [ixNet getList $enSRLG1 singleValue]
ixNet setAttr $SRLG1_singleValue -value True
ixNet commit

puts "Enabling SRLG in OSPF Topology 2 Router"
set enSRLG2 [ixNet getAttribute $ospf2 -enableSRLG]
set SRLG2_singleValue [ixNet getList $enSRLG2 singleValue]
ixNet setAttr $SRLG2_singleValue -value True
ixNet commit

################################################################################
# 4. Set SRLG Count and Provide SRLG Value in OSPF Emulated Router.            #           
################################################################################
puts "Setting SRLG Count 3 in OSPF Topology 1 Router"
ixNet setAttr  $ospf1 -srlgCount 3
ixNet commit

puts "Setting SRLG Value 14, 0 and 255 in OSPF Topology 1 Router"
set SRLG1_ValueList0 [lindex [ixNet getList  $ospf1 srlgValueList] 0]
set SRLG1_Value0 [ixNet getAttribute $SRLG1_ValueList0 -srlgValue]
set SRLG1_Value0_singleValue [ixNet getList $SRLG1_Value0 singleValue]
ixNet setAttr $SRLG1_Value0_singleValue -value 14
ixNet commit

set SRLG1_ValueList1 [lindex [ixNet getList  $ospf1 srlgValueList] 1]
set SRLG1_Value1 [ixNet getAttribute $SRLG1_ValueList1 -srlgValue]
set SRLG1_Value1_singleValue [ixNet getList $SRLG1_Value1 singleValue]
ixNet setAttr $SRLG1_Value1_singleValue -value 0
ixNet commit

set SRLG1_ValueList2 [lindex [ixNet getList  $ospf1 srlgValueList] 2]
set SRLG1_Value2 [ixNet getAttribute $SRLG1_ValueList2 -srlgValue]
set SRLG1_Value2_singleValue [ixNet getList $SRLG1_Value2 singleValue]
ixNet setAttr $SRLG1_Value2_singleValue -value 255
ixNet commit

puts "Setting SRLG Count 2 in OSPF Topology 2 Router"
ixNet setAttr  $ospf2 -srlgCount 2
ixNet commit

puts "Setting SRLG Value 12 and 13 in OSPF Topology 2 Router"
set SRLG2_ValueList0 [lindex [ixNet getList  $ospf2 srlgValueList] 0]
set SRLG2_Value0 [ixNet getAttribute $SRLG2_ValueList0 -srlgValue]
set SRLG2_Value0_singleValue [ixNet getList $SRLG2_Value0 singleValue]
ixNet setAttr $SRLG2_Value0_singleValue -value 12
ixNet commit

set SRLG2_ValueList1 [lindex [ixNet getList  $ospf2 srlgValueList] 1]
set SRLG2_Value1 [ixNet getAttribute $SRLG2_ValueList1 -srlgValue]
set SRLG2_Value1_singleValue [ixNet getList $SRLG2_Value1 singleValue]
ixNet setAttr $SRLG2_Value1_singleValue -value 13
ixNet commit

################################################################################
# 5. Enable Link Protection in OSPF Emulated Router.                           #           
################################################################################
puts "Enabling Link Protection in OSPF Topology 1 Router"
set enLinkProtection1 [ixNet getAttribute $ospf1 -enLinkProtection ]
set LinkProc1_singleValue [ixNet getList $enLinkProtection1 singleValue]
ixNet setAttr $LinkProc1_singleValue -value True
ixNet commit

puts "Enabling Link Protection in OSPF Topology 2 Router"
set enLinkProtection2 [ixNet getAttribute $ospf2 -enLinkProtection ]
set LinkProc2_singleValue [ixNet getList $enLinkProtection2 singleValue]
ixNet setAttr $LinkProc2_singleValue -value True
ixNet commit

################################################################################
# 6. Set Link Protection Type in OSPF Emulated Router.                         #           
################################################################################
puts "Enabling Extra Traffic Link Protection Type in OSPF Topology 1 Router"
set extTraf [ixNet getAttribute $ospf1 -extraTraffic]
set extTraf_singleValue [ixNet getList $extTraf singleValue]
ixNet setMulA $extTraf_singleValue -value True
ixNet commit

puts "Enabling Shared Link Protection Type in OSPF Topology 2 Router"
set sharedTraf [ixNet getAttribute $ospf2 -shared]
set sharedTraf_singleValue [ixNet getList $sharedTraf singleValue]
ixNet setMulA $sharedTraf_singleValue -value True
ixNet commit

################################################################################
# 7. Enable Traffic Engineering in OSPF Simulated Router.                      #           
################################################################################
puts "Enabling TE in OSPF Linear Topology"
set simInterface1 [lindex [ixNet getList $networkTopology1 simInterface] 0]
set simInterfaceIPv4Config1 [lindex [ixNet getList $simInterface1\
   simInterfaceIPv4Config] 0]
set ospfPseudoInterface1 [lindex [ixNet getList $simInterfaceIPv4Config1\
   ospfPseudoInterface] 0]
set LinearST_TE [ixNet getAttribute $ospfPseudoInterface1 -enable]
set TE1_singleValue [ixNet getList $LinearST_TE singleValue]
ixNet setAttr $TE1_singleValue -value true
ixNet commit   
   
################################################################################
# 8. Enable Shared Risk Link Group(SRLG) in OSPF Simulated Router.             #           
################################################################################
puts "Enabling SRLG in OSPF Linear Topology"
set enSRLG_ST [ixNet getAttribute $ospfPseudoInterface1 -enableSRLG]
set SRLGST_singleValue [ixNet getList $enSRLG_ST singleValue]
ixNet setAttr $SRLGST_singleValue -value True
ixNet commit

################################################################################
# 9. Set SRLG Count and Provide SRLG Value in OSPF Simulated Router.           #           
################################################################################
puts "Setting SRLG Count 2 in OSPF Linear Topology"
ixNet setAttr  $ospfPseudoInterface1 -srlgCount 2
ixNet commit

puts "Setting SRLG Value 18 and 255 in OSPF Linear Topology"
set SRLGST_ValueList0 [lindex [ixNet getList  $ospfPseudoInterface1 srlgValueList] 0]
set SRLGST_Value0 [ixNet getAttribute $SRLGST_ValueList0 -srlgValue]
set SRLGST_Value0_singleValue [ixNet getList $SRLGST_Value0 singleValue]
ixNet setAttr $SRLGST_Value0_singleValue -value 18
ixNet commit

set SRLGST_ValueList1 [lindex [ixNet getList  $ospfPseudoInterface1 srlgValueList] 1]
set SRLGST_Value1 [ixNet getAttribute $SRLGST_ValueList1 -srlgValue]
set SRLGST_Value1_singleValue [ixNet getList $SRLGST_Value1 singleValue]
ixNet setAttr $SRLGST_Value1_singleValue -value 255
ixNet commit

################################################################################
# 10. Enable Link Protection in OSPF Simulated Router.                         #           
################################################################################
puts "Enabling Link Protection in OSPF Linear Topology"
set enLinkProtectionST [ixNet getAttribute $ospfPseudoInterface1 -enLinkProtection ]
set LinkProcST_singleValue [ixNet getList $enLinkProtectionST singleValue]
ixNet setAttr $LinkProcST_singleValue -value True
ixNet commit

################################################################################
# 11. Set Link Protection Type in OSPF Simulated Router.                       #           
################################################################################
puts "Enabling Dedicated 1:1 Link Protection Type in OSPF Linear Topology"
set D_1to1_Traf [ixNet getAttribute $ospfPseudoInterface1 -dedicated1To1]
set D_1to1_singleValue [ixNet getList $D_1to1_Traf singleValue]
ixNet setMulA $D_1to1_singleValue -value True
ixNet commit

################################################################################
# 12. Start Protocol and wait for 60 seconds.                                  #           
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000

################################################################################
# 13. Retrieve protocol statistics.                                            #           
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

puts "Fetching OSPFv2 Per Port Stats\n"
set viewPage1 {::ixNet::OBJ-/statistics/view:"OSPFv2-RTR Per Port"/page}
set statcap1 [ixNet getAttr $viewPage1 -columnCaptions]
foreach statValList1 [ixNet getAttr $viewPage1 -rowValues] {
    foreach statVal $statValList1  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap1 $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

################################################################################
# 14. Retrieve protocol learned info.                                          #           
################################################################################
puts "Fetching OSPFv2 Basic Learned Info on OSPFv2 Topology 2 Router"
ixNet exec getBasicLearnedInfo $ospf2 1
after 5000
set linfo [ixNet getList $ospf2 learnedInfo]
set values [ixNet getAttribute $linfo -values]

puts "***************************************************"
foreach v $values {
   puts $v
}
puts "***************************************************"

puts "Fetching OSPFv2 Detailed Learned Info on OSPFv2 Topology 2 Router"
ixNet exec getDetailedLearnedInfo $ospf2 1
after 5000
set learnedInfoList [ixNet getList $ospf2 learnedInfo]
set learnedInfo [lindex $learnedInfoList end]
set OpaqueLSAtable [lindex [ixNet getList $learnedInfo table] 5]
set learnedInfoColumnsList [ixNet getAttr $OpaqueLSAtable -columns]
set learnedInfoValuesList [ixNet getAttr $OpaqueLSAtable -values]
puts "Show Opaque LSA Table information"
puts "***************************************************"
foreach valuelist $learnedInfoValuesList {
            set index 0
            foreach satIndv $valuelist {
            set col [lindex $learnedInfoColumnsList $index]
            puts [format "%*s:%*s" -30 $col -10 $satIndv]
            incr index
          }
  puts "***************************************************"
}

################################################################################
# 15. Stop all protocols.                                                      #           
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
