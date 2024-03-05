#/usr/bin/tclsh

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

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use L3vpn Over SRv6 TCL APIs.   #
#                                                                              #
#    1. It will create 2 ISISL3 topologies, each having an ipv6 network        #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. L3vpn configure behind IPv6 Loopback.        #
#       IPv4 NG  configured begind L3vpn DG which is used to generate traffic. # 
#    2. Start the ISISL3 protocol.                                             #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Start the L2-L3 traffic.                                               #
#    6. Retrieve L2-L3 traffic stats.                                          #
#    7. Stop L2-L3 traffic.                                                    #
#    8. Stop all protocols.                                                    #                                                                                          
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.43.12
    set ixTclPort   8009
    set ports       {{10.39.50.122 1 1} {10.39.50.122 1 2}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.50\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure ISISL3/BGP+ as per the description
#    give above
################################################################################ 
set Root [ixNet getRoot]
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
        -start      {00:11:01:00:00:01}              \
        -step       {00:00:00:00:00:01}

ixNet setMultiAttr [ixNet getAttr $mac2 -mac]/counter\
        -direction  increment                        \
        -start      {00:12:01:00:00:01}              \
        -step       {00:00:00:00:00:01}
ixNet commit

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
puts "Adding isisL3 over IPv6 stacks"
ixNet add $mac1 isisL3
ixNet add $mac2 isisL3
ixNet commit

set isisL3_1 [ixNet getList $mac1 isisL3]
set isisL3_2 [ixNet getList $mac2 isisL3]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "isisL3 Topology 1"
ixNet setAttr $topo2  -name "isisL3 Topology 2"

ixNet setAttr $t1dev1 -name "isisL3 Topology 1 Router"
ixNet setAttr $t2dev1 -name "isisL3 Topology 2 Router"
ixNet commit

#Change the property of ISIS-L3
puts "Change the Property of ISIS-L3"
set Network_Type_1 [ixNet getAttribute $isisL3_1 -networkType]
ixNet setMultiAttribute $Network_Type_1 -clearOverlays false
ixNet commit
set singleValue_1 [ixNet add $Network_Type_1 "singleValue"]
ixNet setMultiAttribute $singleValue_1 -value pointpoint
ixNet commit
set Network_Type_1 [ixNet getAttribute $isisL3_2 -networkType]
ixNet setMultiAttribute $Network_Type_1 -clearOverlays false
ixNet commit
set singleValue_1 [ixNet add $Network_Type_1 "singleValue"]
ixNet setMultiAttribute $singleValue_1 -value pointpoint
ixNet commit
#Change the value of fFlag
puts "Change the value F Flag"
set f_Flag_1 [ixNet getAttribute $isisL3_1 -fFlag]
ixNet setMultiAttribute $f_Flag_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $f_Flag_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set f_Flag_1 [ixNet getAttribute $isisL3_2 -fFlag]
ixNet setMultiAttribute $f_Flag_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $f_Flag_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Change the value of -enableIPv6SID
puts "Change the value enableIPv6SID"
set enableIPv6SID_1 [ixNet getAttribute $isisL3_1 -enableIPv6SID]
ixNet setMultiAttribute $enableIPv6SID_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $enableIPv6SID_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set enableIPv6SID_1 [ixNet getAttribute $isisL3_2 -enableIPv6SID]
ixNet setMultiAttribute $enableIPv6SID_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $enableIPv6SID_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Change the value of -ipv6SidValue
puts "Change the value ipv6SidValue"
set ipv6SidValue_1 [ixNet getAttribute $isisL3_1 -ipv6SidValue]
ixNet setMultiAttribute $ipv6SidValue_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $ipv6SidValue_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 3333::1
ixNet commit
set ipv6SidValue_1 [ixNet getAttribute $isisL3_2 -ipv6SidValue]
ixNet setMultiAttribute $ipv6SidValue_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $ipv6SidValue_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 4444::1
ixNet commit
#Change the value of -srv6SidFlags
puts "Change the value srv6SidFlags"
set srv6SidFlags_1 [ixNet getAttribute $isisL3_1 -srv6SidFlags]
ixNet setMultiAttribute $srv6SidFlags_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $srv6SidFlags_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value cd
ixNet commit
set srv6SidFlags_1 [ixNet getAttribute $isisL3_2 -srv6SidFlags]
ixNet setMultiAttribute $srv6SidFlags_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $srv6SidFlags_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value ef
ixNet commit
#Change the value of discardLSPs
puts "Change the value discardLSPs"
set discardLSPs_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -discardLSPs]
ixNet setMultiAttribute $discardLSPs_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $discardLSPs_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value false
ixNet commit
set discardLSPs_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -discardLSPs]
ixNet setMultiAttribute $discardLSPs_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $discardLSPs_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value false
ixNet commit
#Enable of enableWideMetric
puts "Enable the enableWideMetric"
set enableWideMetric_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -enableWideMetric]
ixNet setMultiAttribute $enableWideMetric_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $enableWideMetric_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set enableWideMetric_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -enableWideMetric]
ixNet setMultiAttribute $enableWideMetric_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $enableWideMetric_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable Segment Routing
puts "Enable Segment routing"
ixNet setMultiAttribute $t1dev1/isisL3Router:1 \
	-enableSR true \
	-name "ISIS-L3\ RTR\ 1"
ixNet commit
ixNet setMultiAttribute $t2dev1/isisL3Router:1 \
	-enableSR true \
	-name "ISIS-L3\ RTR\ 1"
ixNet commit
#Enable the DBit
puts "Enable the sBit"
set dBit_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -dBit]
ixNet setMultiAttribute $dBit_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $dBit_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set dBit_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -dBit]
ixNet setMultiAttribute $dBit_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $dBit_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the SBit
puts "Enabling the SBit"
set sBit_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -sBit]
ixNet setMultiAttribute $sBit_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $sBit_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set sBit_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -sBit]
ixNet setMultiAttribute $sBit_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $sBit_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the ipv6Flag
puts "Enabling the ipv6Flag"
set ipv6Flag_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -ipv6Flag]
ixNet setMultiAttribute $ipv6Flag_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $ipv6Flag_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value false
ixNet commit
set ipv6Flag_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -ipv6Flag]
ixNet setMultiAttribute $ipv6Flag_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $ipv6Flag_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value false
ixNet commit
#Enable the ipv4Flag
puts "Enabling the ipv4Flag"
set ipv4Flag_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -ipv4Flag]
ixNet setMultiAttribute $ipv4Flag_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $ipv4Flag_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value false
ixNet commit
set ipv4Flag_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -ipv4Flag]
ixNet setMultiAttribute $ipv4Flag_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $ipv4Flag_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value false
ixNet commit
#Enable the configureSIDIndexLabel
puts "Enabling the configureSIDIndexLabel"
set configureSIDIndexLabel_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -configureSIDIndexLabel]
ixNet setMultiAttribute $configureSIDIndexLabel_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $configureSIDIndexLabel_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value false
ixNet commit
set configureSIDIndexLabel_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -configureSIDIndexLabel]
ixNet setMultiAttribute $configureSIDIndexLabel_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $configureSIDIndexLabel_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value false
ixNet commit
#Enable the ipv6Srh means Enable SR-IPv6
puts "Enabling the ipv6Srh means Enable SR-IPv6"
set ipv6Srh_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -ipv6Srh]
ixNet setMultiAttribute $ipv6Srh_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $ipv6Srh_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set ipv6Srh_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -ipv6Srh]
ixNet setMultiAttribute $ipv6Srh_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $ipv6Srh_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the oFlagOfSRv6CapTlv
puts "Enabling the oFlagOfSRv6CapTlv"
set oFlagOfSRv6CapTlv_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -oFlagOfSRv6CapTlv]
ixNet setMultiAttribute $oFlagOfSRv6CapTlv_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $oFlagOfSRv6CapTlv_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set oFlagOfSRv6CapTlv_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -oFlagOfSRv6CapTlv]
ixNet setMultiAttribute $oFlagOfSRv6CapTlv_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $oFlagOfSRv6CapTlv_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the eFlagOfSRv6CapTlv
puts "Enabling the eFlagOfSRv6CapTlv"
set eFlagOfSRv6CapTlv_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -eFlagOfSRv6CapTlv]
ixNet setMultiAttribute $eFlagOfSRv6CapTlv_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $eFlagOfSRv6CapTlv_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set eFlagOfSRv6CapTlv_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -eFlagOfSRv6CapTlv]
ixNet setMultiAttribute $eFlagOfSRv6CapTlv_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $eFlagOfSRv6CapTlv_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the sBitForSRv6Cap
puts "Enabling the sBitForSRv6Cap"
set sBitForSRv6Cap_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -sBitForSRv6Cap]
ixNet setMultiAttribute $sBitForSRv6Cap_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $sBitForSRv6Cap_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set sBitForSRv6Cap_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -sBitForSRv6Cap]
ixNet setMultiAttribute $sBitForSRv6Cap_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $sBitForSRv6Cap_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the dBitForSRv6Cap
puts "Enabling the dBitForSRv6Cap"
set dBitForSRv6Cap_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -dBitForSRv6Cap]
ixNet setMultiAttribute $dBitForSRv6Cap_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $dBitForSRv6Cap_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set dBitForSRv6Cap_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -dBitForSRv6Cap]
ixNet setMultiAttribute $dBitForSRv6Cap_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $dBitForSRv6Cap_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the reservedInsideSRv6CapFlag
puts "Enabling the reservedInsideSRv6CapFlag"
set reservedInsideSRv6CapFlag_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -reservedInsideSRv6CapFlag]
ixNet setMultiAttribute $reservedInsideSRv6CapFlag_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $reservedInsideSRv6CapFlag_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 3fff
ixNet commit
set reservedInsideSRv6CapFlag_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -reservedInsideSRv6CapFlag]
ixNet setMultiAttribute $reservedInsideSRv6CapFlag_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $reservedInsideSRv6CapFlag_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 2fff
ixNet commit
#Enable the includeMaximumEndDSrhTLV
puts "Enabling the includeMaximumEndDSrhTLV"
set includeMaximumEndDSrhTLV_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -includeMaximumEndDSrhTLV]
ixNet setMultiAttribute $includeMaximumEndDSrhTLV_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $includeMaximumEndDSrhTLV_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set includeMaximumEndDSrhTLV_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -includeMaximumEndDSrhTLV]
ixNet setMultiAttribute $includeMaximumEndDSrhTLV_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $includeMaximumEndDSrhTLV_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the includeMaximumEndPopSrhTLV
puts "Enabling the includeMaximumEndPopSrhTLV"
set includeMaximumEndPopSrhTLV_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -includeMaximumEndPopSrhTLV]
ixNet setMultiAttribute $includeMaximumEndPopSrhTLV_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $includeMaximumEndPopSrhTLV_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set includeMaximumEndPopSrhTLV_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -includeMaximumEndPopSrhTLV]
ixNet setMultiAttribute $includeMaximumEndPopSrhTLV_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $includeMaximumEndPopSrhTLV_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the includeMaximumSLTLV
puts "Enabling the includeMaximumSLTLV"
set includeMaximumSLTLV_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -includeMaximumSLTLV]
ixNet setMultiAttribute $includeMaximumSLTLV_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $includeMaximumSLTLV_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set includeMaximumSLTLV_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -includeMaximumSLTLV]
ixNet setMultiAttribute $includeMaximumSLTLV_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $includeMaximumSLTLV_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the includeMaximumTEncapSrhTLV
puts "Enabling the includeMaximumTEncapSrhTLV"
set includeMaximumTEncapSrhTLV_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -includeMaximumTEncapSrhTLV]
ixNet setMultiAttribute $includeMaximumTEncapSrhTLV_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $includeMaximumTEncapSrhTLV_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set includeMaximumTEncapSrhTLV_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -includeMaximumTEncapSrhTLV]
ixNet setMultiAttribute $includeMaximumTEncapSrhTLV_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $includeMaximumTEncapSrhTLV_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the includeMaximumTInsertSrhTLV
puts "Enabling the includeMaximumTInsertSrhTLV"
set includeMaximumTInsertSrhTLV_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -includeMaximumTInsertSrhTLV]
ixNet setMultiAttribute $includeMaximumTInsertSrhTLV_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $includeMaximumTInsertSrhTLV_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set includeMaximumTInsertSrhTLV_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -includeMaximumTInsertSrhTLV]
ixNet setMultiAttribute $includeMaximumTInsertSrhTLV_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $includeMaximumTInsertSrhTLV_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the dBitForSRv6Cap
puts "Enabling the dBitForSRv6Cap"
set dBitInsideSRv6SidTLV_1 [ixNet getAttribute $t1dev1/isisL3Router:1 -dBitInsideSRv6SidTLV]
ixNet setMultiAttribute $dBitInsideSRv6SidTLV_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $dBitInsideSRv6SidTLV_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set dBitInsideSRv6SidTLV_1 [ixNet getAttribute $t2dev1/isisL3Router:1 -dBitInsideSRv6SidTLV]
ixNet setMultiAttribute $dBitInsideSRv6SidTLV_1 -clearOverlays false
ixNet commit
set single_value_1 [ixNet add $dBitInsideSRv6SidTLV_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Create Network Group At PEER1 Side
set IPv6_LoopBack [ixNet add $t1dev1 "networkGroup"]
ixNet setMultiAttribute $IPv6_LoopBack \
	-name "IPv6_LoopBack_Address"
ixNet commit
set IPv6_LoopBack [lindex [ixNet remapIds $IPv6_LoopBack] 0]
set ipv6PrefixPools [ixNet add $IPv6_LoopBack "ipv6PrefixPools"]
ixNet setMultiAttribute $ipv6PrefixPools \
	-addrStepSupported true \
	-name "Basic\ IPv6\ Addresses\ 1"
ixNet commit
set ipv6PrefixPools [lindex [ixNet remapIds $ipv6PrefixPools] 0]
set Connector [ixNet add $ipv6PrefixPools "connector"]
ixNet setMultiAttribute $Connector \
	-connectedTo $mac1
ixNet commit
set networkAddress [ixNet getAttribute $ipv6PrefixPools -networkAddress]
ixNet setMultiAttribute $networkAddress -clearOverlays false
ixNet commit
set counter_networkAddress [ixNet add $networkAddress "counter"]
ixNet setMultiAttribute $counter_networkAddress \
	-step ::0.0.0.1 \
	-start 1111::1 \
	-direction increment
ixNet commit
#Create Network Group At PEER2 Side
set networkGroup_P2 [ixNet add $t2dev1 "networkGroup"]
ixNet setMultiAttribute $networkGroup_P2 \
	-name "Routers"
ixNet commit
set networkGroup_P2 [lindex [ixNet remapIds $networkGroup_P2] 0]
set Network_Topology [ixNet add $networkGroup_P2 "networkTopology"]
ixNet commit
set Network_Topology [lindex [ixNet remapIds $Network_Topology] 0]
set netTopologyCustom [ixNet add $Network_Topology "netTopologyCustom"]
ixNet commit
set netTopologyCustom [lindex [ixNet remapIds $netTopologyCustom] 0]
ixNet setMultiAttribute $netTopologyCustom/linkTable \
	-fromNodeIndex [list 5 5 1 1 6 6 2 2 9 9 9 9] \
	-toNodeIndex [list 3 7 0 3 4 8 0 4 1 5 2 6]
ixNet setMultiAttribute $Network_Topology/simInterface:1 \
	-name "Simulated\ Interfaces\ 1"
ixNet setMultiAttribute $Network_Topology/simInterface:1/simInterfaceIPv4Config:1 \
	-name "Simulated\ Link\ IPv4\ Address\ 1"
ixNet commit
#Enable the F Flag of SR-MPLS of Network Topology
set fFlag_1 [ixNet getAttribute $Network_Topology/simInterface:1/isisL3PseudoInterface:1 -fFlag]
ixNet setMultiAttribute $fFlag_1 -clearOverlays false
ixNet commit
set Single_Value_1 [ixNet add $fFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit
#Enable the enableWideMetric of SR-MPLS of Simulated Interfaces of Network Topology
set enableWideMetric [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1 -enableWideMetric]
ixNet setMultiAttribute $enableWideMetric -clearOverlays false
ixNet commit
set Single_Value_1 [ixNet add $enableWideMetric "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit
#Enable the enableSR/IPv4/IPv6/configureSIDIndexLabel of Simulated Bridge of Network Topology
ixNet setMultiAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1 -enableSR true
ixNet commit
set ipv4Flag [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1 -ipv4Flag]
ixNet setMultiAttribute $ipv4Flag -clearOverlays false
ixNet commit
set Single_Value_1 [ixNet add $ipv4Flag "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value false
ixNet commit
set ipv6Flag [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1 -ipv6Flag]
ixNet setMultiAttribute $ipv6Flag -clearOverlays false
ixNet commit
set Single_Value_1 [ixNet add $ipv6Flag "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value false
ixNet commit
set configureSIDIndexLabel [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1 -configureSIDIndexLabel]
ixNet setMultiAttribute $configureSIDIndexLabel -clearOverlays false
ixNet commit
set Single_Value_1 [ixNet add $configureSIDIndexLabel "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value false
ixNet commit
#The value set for the IPv6 Node SID
set ipv6NodePrefix [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1 -ipv6NodePrefix]
ixNet setMultiAttribute $ipv6NodePrefix	-clearOverlays false
ixNet commit
set counter [ixNet add $ipv6NodePrefix "counter"]
ixNet setMultiAttribute $counter \
	-step 1:: \
	-start 7001::1 \
	-direction increment
ixNet commit
#Enable the filed of "Enable SR-IPv6"
set ipv6Srh [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1 -ipv6Srh]
ixNet setMultiAttribute $ipv6Srh -clearOverlays false
ixNet commit
set singleValue [ixNet add $ipv6Srh "singleValue"]
ixNet setMultiAttribute $singleValue -value true
ixNet commit
#Change the Network Address of ISIS Simulated IPv6 Node Routers of Simulated Bridge
set networkAddress [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1 -networkAddress]
ixNet setMultiAttribute $networkAddress -clearOverlays false
ixNet commit
set singleValue [ixNet add $networkAddress "singleValue"]
ixNet setMultiAttribute $singleValue -value 2222::1
ixNet commit
set singleValue [lindex [ixNet remapIds $singleValue] 0]
ixNet setMultiAttribute $networkAddress/nest:1 -enabled false \
	-step ::0.0.0.1
ixNet setMultiAttribute $networkAddress/nest:2 \
	-enabled false \
	-step ::0.0.0.1
ixNet commit
set active [ixNet getAttribute $Network_Topology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1 -active]
ixNet setMultiAttribute $active -clearOverlays false
ixNet commit
set singleValue [ixNet add $active "singleValue"]
ixNet setMultiAttribute $singleValue -value false
ixNet commit
set overlay [ixNet add $active "overlay"]
ixNet setMultiAttribute $overlay \
	-count 1 \
	-index 5 \
	-indexStep 0 \
	-valueStep true \
	-value true
ixNet commit
set overlay [lindex [ixNet remapIds $overlay] 0]
set overlay_1 [ixNet add $active "overlay"]
ixNet setMultiAttribute $overlay_1 \
	-count 1 \
	-index 9 \
	-indexStep 0 \
	-valueStep true \
	-value true
ixNet commit
#Add Device Group Behind IPv6 Network Group
set deviceGroup_bgp [ixNet add $IPv6_LoopBack "deviceGroup"]
ixNet setMultiAttribute $deviceGroup_bgp \
	-multiplier 1 \
	-name "BGP_L3vpn_1"
ixNet commit
set deviceGroup_bgp [lindex [ixNet remapIds $deviceGroup_bgp] 0]
set enable [ixNet getAttribute $deviceGroup_bgp -enabled]
ixNet setMultiAttribute $enable \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $enable "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set singleValue [lindex [ixNet remapIds $singleValue] 0]

set ipv6Loopback [ixNet add $deviceGroup_bgp "ipv6Loopback"]
ixNet setMultiAttribute $ipv6Loopback \
	-stackedLayers [list ] \
	-name "IPv6\ Loopback\ 2"
ixNet commit
set ipv6Loopback [lindex [ixNet remapIds $ipv6Loopback] 0]

set Connector [ixNet add $ipv6Loopback "connector"]
ixNet setMultiAttribute $Connector \
	-connectedTo $ipv6PrefixPools
ixNet commit
set Connector [lindex [ixNet remapIds $Connector] 0]
set prefix [ixNet getAttribute $ipv6Loopback -prefix]
ixNet setMultiAttribute $prefix \
	-clearOverlays false
ixNet commit
set Single_Value [ixNet add $prefix "singleValue"]
ixNet setMultiAttribute $Single_Value \
	-value 128
ixNet commit        
set address [ixNet getAttribute $ipv6Loopback -address]
ixNet setMultiAttribute $address \
	-clearOverlays false
ixNet commit
set Counter [ixNet add $address "counter"]
ixNet setMultiAttribute $Counter \
	-step ::0.0.0.1 \
	-start 1111::1 \
	-direction increment
ixNet commit
set bgpIpv6Peer_1 [ixNet add $ipv6Loopback "bgpIpv6Peer"]
ixNet setMultiAttribute $bgpIpv6Peer_1 \
	-numberSRTEPolicies 2 \
	-enSRv6DataPlane true \
	-stackedLayers [list ] \
	-name "BGP+\ Peer\ 2"
ixNet commit
set bgpIpv6Peer_1 [lindex [ixNet remapIds $bgpIpv6Peer_1] 0]
set dutIp [ixNet getAttribute $bgpIpv6Peer_1 -dutIp]
ixNet setMultiAttribute $dutIp \
	-clearOverlays false
ixNet commit
set counter [ixNet add $dutIp "counter"]
ixNet setMultiAttribute $counter \
	-step ::0.0.0.1 \
	-start 2222::1 \
	-direction increment
ixNet commit
set counter [lindex [ixNet remapIds $counter] 0]
set filterSRTEPoliciesV6 [ixNet getAttribute $bgpIpv6Peer_1 -filterSRTEPoliciesV6]
ixNet setMultiAttribute $filterSRTEPoliciesV6 \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $filterSRTEPoliciesV6 "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set filterSRTEPoliciesV4 [ixNet getAttribute $bgpIpv6Peer_1 -filterSRTEPoliciesV4]
ixNet setMultiAttribute $filterSRTEPoliciesV4 \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $filterSRTEPoliciesV4 "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set filterIpV4MplsVpn [ixNet getAttribute $bgpIpv6Peer_1 -filterIpV4MplsVpn]
ixNet setMultiAttribute $filterIpV4MplsVpn -clearOverlays false
ixNet commit
set singleValue [ixNet add $filterIpV4MplsVpn "singleValue"]
ixNet setMultiAttribute $singleValue -value true
ixNet commit
set capabilitySRTEPoliciesV4 [ixNet getAttribute $bgpIpv6Peer_1 -capabilitySRTEPoliciesV4]
ixNet setMultiAttribute $capabilitySRTEPoliciesV4 \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $capabilitySRTEPoliciesV4 "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set capabilitySRTEPoliciesV6 [ixNet getAttribute $bgpIpv6Peer_1 -capabilitySRTEPoliciesV6]
ixNet setMultiAttribute $capabilitySRTEPoliciesV6 \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $capabilitySRTEPoliciesV6 "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set capabilityNHEncodingCapabilities [ixNet getAttribute $bgpIpv6Peer_1 -capabilityNHEncodingCapabilities]
ixNet setMultiAttribute $capabilityNHEncodingCapabilities -clearOverlays false
ixNet commit
set singleValue [ixNet add $capabilityNHEncodingCapabilities "singleValue"]
ixNet setMultiAttribute $singleValue -value true
ixNet commit
#Configuring the SRTE Policy Properties
puts "Configuring the SRTE Policy Properties: BGP SRTE Policy Tab"
set policyType [ixNet getAttribute $bgpIpv6Peer_1/bgpSRTEPoliciesListV6 -policyType]
ixNet setMultiAttribute $policyType \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $policyType "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value ipv6
ixNet commit
set endPointV6 [ixNet getAttribute $bgpIpv6Peer_1/bgpSRTEPoliciesListV6 -endPointV6]
ixNet setMultiAttribute $endPointV6 -clearOverlays false
ixNet commit
set singleValue [ixNet add $endPointV6 "singleValue"]
ixNet setMultiAttribute $singleValue -value 2222::1
ixNet commit
ixNet setMultiAttribute $bgpIpv6Peer_1/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6 \
	-numberOfSegmentsV6 6
ixNet commit
#set singleValue [ixNet add $numberOfActiveSegments "singleValue"]
#ixNet setMultiAttribute $singleValue \
	-value 6
#ixNet commit
set segmentType [ixNet getAttribute $bgpIpv6Peer_1/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6 -segmentType]
ixNet setMultiAttribute $segmentType \
	-clearOverlays false

ixNet commit
set singleValue [ixNet add $segmentType "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value ipv6sid
ixNet commit
set ipv6SID [ixNet getAttribute $bgpIpv6Peer_1/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6 -ipv6SID]
ixNet setMultiAttribute $ipv6SID \
	-clearOverlays false

ixNet commit
set singleValue [ixNet add $ipv6SID "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value 6666::1
ixNet commit
set singleValue [lindex [ixNet remapIds $singleValue] 0]

ixNet setMultiAttribute $ipv6SID/nest:1 \
	-enabled false \
	-step ::0.0.0.1

ixNet setMultiAttribute $ipv6SID/nest:2 \
	-enabled false \
	-step ::0.0.0.1

ixNet setMultiAttribute $ipv6SID/nest:3 \
	-enabled false \
	-step ::0.0.0.1

ixNet commit
set overlay [ixNet add $ipv6SID "overlay"]
ixNet setMultiAttribute $overlay \
	-count 1 \
	-index 2 \
	-indexStep 0 \
	-valueStep 7001::1 \
	-value 7001::1
ixNet commit
set overlay [lindex [ixNet remapIds $overlay] 0]

set overlay [ixNet add $ipv6SID "overlay"]
ixNet setMultiAttribute $overlay \
	-count 1 \
	-index 3 \
	-indexStep 0 \
	-valueStep 7003::1 \
	-value 7003::1
ixNet commit
set overlay [lindex [ixNet remapIds $overlay] 0]

set overlay [ixNet add $ipv6SID "overlay"]
ixNet setMultiAttribute $overlay \
	-count 1 \
	-index 4 \
	-indexStep 0 \
	-valueStep 7004::1 \
	-value 7004::1
ixNet commit
set overlay [lindex [ixNet remapIds $overlay] 0]

set overlay [ixNet add $ipv6SID "overlay"]
ixNet setMultiAttribute $overlay \
	-count 1 \
	-index 5 \
	-indexStep 0 \
	-valueStep 7007::1 \
	-value 7007::1
ixNet commit
set overlay [lindex [ixNet remapIds $overlay] 0]

set overlay [ixNet add $ipv6SID "overlay"]
ixNet setMultiAttribute $overlay \
	-count 1 \
	-index 6 \
	-indexStep 0 \
	-valueStep 7009::1 \
	-value 7009::1
ixNet commit
set overlay [lindex [ixNet remapIds $overlay] 0]

set overlay [ixNet add $ipv6SID "overlay"]
ixNet setMultiAttribute $overlay \
	-count 1 \
	-index 8 \
	-indexStep 0 \
	-valueStep 7002::1 \
	-value 7002::1
ixNet commit
set overlay [lindex [ixNet remapIds $overlay] 0]

set overlay [ixNet add $ipv6SID "overlay"]
ixNet setMultiAttribute $overlay \
	-count 1 \
	-index 9 \
	-indexStep 0 \
	-valueStep 7006::1 \
	-value 7006::1
ixNet commit
set overlay [lindex [ixNet remapIds $overlay] 0]

set overlay [ixNet add $ipv6SID "overlay"]
ixNet setMultiAttribute $overlay \
	-count 1 \
	-index 10 \
	-indexStep 0 \
	-valueStep 7008::1 \
	-value 7008::1
ixNet commit
set overlay [lindex [ixNet remapIds $overlay] 0]

set overlay [ixNet add $ipv6SID "overlay"]
ixNet setMultiAttribute $overlay \
	-count 1 \
	-index 11 \
	-indexStep 0 \
	-valueStep 7004::1 \
	-value 7004::1
ixNet commit
set overlay [lindex [ixNet remapIds $overlay] 0]

set overlay [ixNet add $ipv6SID "overlay"]
ixNet setMultiAttribute $overlay \
	-count 1 \
	-index 12 \
	-indexStep 0 \
	-valueStep 7005::1 \
	-value 7005::1
ixNet commit
#Adding BGPVRF on top of BGP+
set bgpV6Vrf_1 [ixNet add $bgpIpv6Peer_1 "bgpV6Vrf"]
ixNet setMultiAttribute $bgpV6Vrf_1 \
	-multiplier 4 \
	-stackedLayers [list ] \
	-name "BGP+\ VRF\ 2"
ixNet commit
set bgpV6Vrf_1 [lindex [ixNet remapIds $bgpV6Vrf_1] 0]
set targetAsNumber [ixNet getAttribute $bgpV6Vrf_1/bgpExportRouteTargetList:1 -targetAsNumber]
ixNet setMultiAttribute $targetAsNumber \
	-clearOverlays false
ixNet commit
set counter [ixNet add $targetAsNumber "counter"]
ixNet setMultiAttribute $counter \
	-step 1 \
	-start 100 \
	-direction increment
ixNet commit
#Adding Network Group Behind BGP+
set networkGroup [ixNet add $deviceGroup_bgp "networkGroup"]
ixNet setMultiAttribute $networkGroup \
	-name "IPv4_VPN_Rote"
ixNet commit
set networkGroup [lindex [ixNet remapIds $networkGroup] 0]
set networkGroup_1 [ixNet getAttribute $networkGroup -enabled]
ixNet setMultiAttribute $networkGroup_1 \
	-clearOverlays false
ixNet commit
set networkGroup_1 [ixNet add $networkGroup_1 "singleValue"]
ixNet setMultiAttribute $networkGroup_1 \
	-value true
ixNet commit
set networkGroup_1 [lindex [ixNet remapIds $networkGroup_1] 0]
set ipv4PrefixPools [ixNet add $networkGroup "ipv4PrefixPools"]
ixNet setMultiAttribute $ipv4PrefixPools \
	-addrStepSupported true \
	-name "Basic\ IPv4\ Addresses\ 2"
ixNet commit
set ipv4PrefixPools [lindex [ixNet remapIds $ipv4PrefixPools] 0]
set connector [ixNet add $ipv4PrefixPools "connector"]
ixNet setMultiAttribute $connector \
	-connectedTo $bgpV6Vrf_1
ixNet commit
set networkAddress [ixNet getAttribute $ipv4PrefixPools -networkAddress]
ixNet setMultiAttribute $networkAddress \
	-clearOverlays false

ixNet commit
set counter [ixNet add $networkAddress "counter"]
ixNet setMultiAttribute $counter \
	-step 0.1.0.0 \
	-start 1.1.1.1 \
	-direction increment
ixNet commit
set bgpV6L3VpnRouteProperty [lindex [ixNet getList $ipv4PrefixPools bgpV6L3VpnRouteProperty] 0]
set labelStep [ixNet getAttribute $bgpV6L3VpnRouteProperty -labelStep]
ixNet setMultiAttribute $labelStep \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $labelStep "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value 1
ixNet commit
set enableSrv6Sid [ixNet getAttribute $bgpV6L3VpnRouteProperty -enableSrv6Sid]
ixNet setMultiAttribute $enableSrv6Sid \
	-clearOverlays false

ixNet commit
set singleValue [ixNet add $enableSrv6Sid "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set srv6SidLoc [ixNet getAttribute $bgpV6L3VpnRouteProperty -srv6SidLoc]
ixNet setMultiAttribute $srv6SidLoc -clearOverlays false
ixNet commit
set counter [ixNet add $srv6SidLoc "counter"]
ixNet setMultiAttribute $counter \
	-step 1:: \
	-start a1::d100 \
	-direction increment
ixNet commit
#Configure BGP/BGP-vrf at PEER2 side
set deviceGroup_P2 [ixNet add $networkGroup_P2 "deviceGroup"]
ixNet setMultiAttribute $deviceGroup_P2 \
	-multiplier 1 \
	-name "BGP_L3vpn_2"
ixNet commit
set deviceGroup_P2 [lindex [ixNet remapIds $deviceGroup_P2] 0]
set ipv6Loopback_P2 [ixNet add $deviceGroup_P2 "ipv6Loopback"]
ixNet setMultiAttribute $ipv6Loopback_P2 \
	-stackedLayers [list ] \
	-name "IPv6\ Loopback\ 1"
ixNet commit
set ipv6Loopback_P2 [lindex [ixNet remapIds $ipv6Loopback_P2] 0]
set connector [ixNet add $ipv6Loopback_P2 "connector"]
ixNet commit
set address [ixNet getAttribute $ipv6Loopback_P2 -address]
ixNet setMultiAttribute $address \
	-clearOverlays false

ixNet commit
set counter [ixNet add $address "counter"]
ixNet setMultiAttribute $counter \
	-step ::0.0.0.1 \
	-start 2222::1 \
	-direction increment
ixNet commit
set bgpIpv6Peer_p2 [ixNet add $ipv6Loopback_P2 "bgpIpv6Peer"]
ixNet setMultiAttribute $bgpIpv6Peer_p2 \
	-stackedLayers [list ] \
	-name "BGP+\ Peer\ 1"
ixNet commit
set bgpIpv6Peer_p2 [lindex [ixNet remapIds $bgpIpv6Peer_p2] 0]
set dutIp [ixNet getAttribute $bgpIpv6Peer_p2 -dutIp]
ixNet setMultiAttribute $dutIp \
	-clearOverlays false

ixNet commit
set counter [ixNet add $dutIp "counter"]
ixNet setMultiAttribute $counter \
	-step ::0.0.0.1 \
	-start 1111::1 \
	-direction increment
ixNet commit
set filterSRTEPoliciesV6 [ixNet getAttribute $bgpIpv6Peer_p2 -filterSRTEPoliciesV6]
ixNet setMultiAttribute $filterSRTEPoliciesV6 \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $filterSRTEPoliciesV6 "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set filterSRTEPoliciesV4 [ixNet getAttribute $bgpIpv6Peer_p2 -filterSRTEPoliciesV4]
ixNet setMultiAttribute $filterSRTEPoliciesV4 \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $filterSRTEPoliciesV4 "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set filterIpV4MplsVpn_2 [ixNet getAttribute $bgpIpv6Peer_p2 -filterIpV4MplsVpn]
ixNet setMultiAttribute $filterIpV4MplsVpn_2 -clearOverlays false
ixNet commit
set singleValue [ixNet add $filterIpV4MplsVpn_2 "singleValue"]
ixNet setMultiAttribute $singleValue -value true
ixNet commit
set capabilitySRTEPoliciesV4 [ixNet getAttribute $bgpIpv6Peer_p2 -capabilitySRTEPoliciesV4]
ixNet setMultiAttribute $capabilitySRTEPoliciesV4 \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $capabilitySRTEPoliciesV4 "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set capabilitySRTEPoliciesV6 [ixNet getAttribute $bgpIpv6Peer_p2 -capabilitySRTEPoliciesV6]
ixNet setMultiAttribute $capabilitySRTEPoliciesV6 \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $capabilitySRTEPoliciesV6 "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set capabilityNHEncodingCapabilities_2 [ixNet getAttribute $bgpIpv6Peer_p2 -capabilityNHEncodingCapabilities]
ixNet setMultiAttribute $capabilityNHEncodingCapabilities_2 -clearOverlays false
ixNet commit
set singleValue [ixNet add $capabilityNHEncodingCapabilities_2 "singleValue"]
ixNet setMultiAttribute $singleValue -value true
ixNet commit
#Adding BGPVRF on top of BGP+ @Peer2 side
set bgpV6Vrf_2 [ixNet add $bgpIpv6Peer_p2 "bgpV6Vrf"]
ixNet setMultiAttribute $bgpV6Vrf_2 \
	-multiplier 4 \
	-stackedLayers [list ] \
	-name "BGP+\ VRF\ 2"
ixNet commit
set bgpV6Vrf_2 [lindex [ixNet remapIds $bgpV6Vrf_2] 0]
set targetAsNumber [ixNet getAttribute $bgpV6Vrf_2/bgpExportRouteTargetList:1 -targetAsNumber]
ixNet setMultiAttribute $targetAsNumber \
	-clearOverlays false
ixNet commit
set counter [ixNet add $targetAsNumber "counter"]
ixNet setMultiAttribute $counter \
	-step 1 \
	-start 100 \
	-direction increment
ixNet commit
#Adding Network Group Behind BGP+ AT PEER2 Side
set networkGroup_P2 [ixNet add $deviceGroup_P2 "networkGroup"]
ixNet setMultiAttribute $networkGroup_P2 \
	-name "IPv4_VPN_Rote_2"
ixNet commit
set networkGroup_P2 [lindex [ixNet remapIds $networkGroup_P2] 0]
set networkGroup_2 [ixNet getAttribute $networkGroup_P2 -enabled]
ixNet setMultiAttribute $networkGroup_2 \
	-clearOverlays false
ixNet commit
set networkGroup_2 [ixNet add $networkGroup_2 "singleValue"]
ixNet setMultiAttribute $networkGroup_2 \
	-value true
ixNet commit
set networkGroup_1 [lindex [ixNet remapIds $networkGroup_2] 0]
set ipv4PrefixPools_P2 [ixNet add $networkGroup_P2 "ipv4PrefixPools"]
ixNet setMultiAttribute $ipv4PrefixPools_P2 \
	-addrStepSupported true \
	-name "Basic\ IPv4\ Addresses\ 2"
ixNet commit
set ipv4PrefixPools_P2 [lindex [ixNet remapIds $ipv4PrefixPools_P2] 0]
set connector_P2 [ixNet add $ipv4PrefixPools_P2 "connector"]
ixNet setMultiAttribute $connector_P2 \
	-connectedTo $bgpV6Vrf_2
ixNet commit
set networkAddress_P2 [ixNet getAttribute $ipv4PrefixPools_P2 -networkAddress]
ixNet setMultiAttribute $networkAddress_P2 \
	-clearOverlays false
ixNet commit
set counter [ixNet add $networkAddress_P2 "counter"]
ixNet setMultiAttribute $counter \
	-step 0.1.0.0 \
	-start 2.2.2.2 \
	-direction increment
ixNet commit
set bgpV6L3VpnRouteProperty_P2 [lindex [ixNet getList $ipv4PrefixPools_P2 bgpV6L3VpnRouteProperty] 0]
set labelStep [ixNet getAttribute $bgpV6L3VpnRouteProperty_P2 -labelStep]
ixNet setMultiAttribute $labelStep \
	-clearOverlays false
ixNet commit
set singleValue [ixNet add $labelStep "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value 1
ixNet commit
set enableSrv6Sid [ixNet getAttribute $bgpV6L3VpnRouteProperty_P2 -enableSrv6Sid]
ixNet setMultiAttribute $enableSrv6Sid \
	-clearOverlays false

ixNet commit
set singleValue [ixNet add $enableSrv6Sid "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set srv6SidLoc [ixNet getAttribute $bgpV6L3VpnRouteProperty_P2 -srv6SidLoc]
ixNet setMultiAttribute $srv6SidLoc -clearOverlays false
ixNet commit
set counter [ixNet add $srv6SidLoc "counter"]
ixNet setMultiAttribute $counter \
	-step ::1 \
	-start a1::d100 \
	-direction increment
ixNet commit
set enableExtendedCommunity [ixNet getAttribute $bgpV6L3VpnRouteProperty_P2 -enableExtendedCommunity]
ixNet setMultiAttribute $enableExtendedCommunity \
	-clearOverlays false

ixNet commit
set singleValue [ixNet add $enableExtendedCommunity "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value true
ixNet commit
set colorValue [ixNet getAttribute $bgpV6L3VpnRouteProperty_P2/bgpExtendedCommunitiesList:1 -colorValue]
ixNet setMultiAttribute $colorValue \
	-clearOverlays false

ixNet commit
set counter [ixNet add $colorValue "counter"]
ixNet setMultiAttribute $counter \
	-step 1 \
	-start 100 \
	-direction increment
ixNet commit
set subType [ixNet getAttribute $bgpV6L3VpnRouteProperty_P2/bgpExtendedCommunitiesList:1 -subType]
ixNet setMultiAttribute $subType \
	-clearOverlays false

ixNet commit
set singleValue [ixNet add $subType "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value color
ixNet commit

set type [ixNet getAttribute $bgpV6L3VpnRouteProperty_P2/bgpExtendedCommunitiesList:1 -type]
ixNet setMultiAttribute $type \
	-clearOverlays false

ixNet commit
set singleValue [ixNet add $type "singleValue"]
ixNet setMultiAttribute $singleValue \
	-value opaque
ixNet commit

################################################################################
# 2. Start ISISl3/BGP+ protocol and wait for 60 seconds
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

################################################################################
# 4. Configure L2-L3 traffic 
################################################################################
puts "Congfiguring L2-L3 Traffic Item"
set statistic_1 [ixNet add $Root/globals/testInspector "statistic"]
ixNet commit
set statistic_1 [lindex [ixNet remapIds $statistic_1] 0]

set statistic_2 [ixNet add $Root/globals/testInspector "statistic"]
ixNet commit
set statistic_2 [lindex [ixNet remapIds $statistic_2] 0]

set statistic_3 [ixNet add $Root/globals/testInspector "statistic"]
ixNet commit
set statistic_3 [lindex [ixNet remapIds $statistic_3] 0]

set statistic_4 [ixNet add $Root/globals/testInspector "statistic"]
ixNet commit
set statistic_4 [lindex [ixNet remapIds $statistic_4] 0]

set statistic_5 [ixNet add $Root/globals/testInspector "statistic"]
ixNet commit
set statistic_5 [lindex [ixNet remapIds $statistic_5] 0]

set statistic_6 [ixNet add $Root/globals/testInspector "statistic"]
ixNet setMultiAttribute $statistic_6 \
	-value 1
ixNet commit
set statistic_6 [lindex [ixNet remapIds $statistic_6] 0]

set statistic_7 [ixNet add $Root/globals/testInspector "statistic"]
ixNet commit
set statistic_7 [lindex [ixNet remapIds $statistic_7] 0]

set statistic_8 [ixNet add $Root/globals/testInspector "statistic"]
ixNet setMultiAttribute $statistic_8 \
	-value 3
ixNet commit
set statistic_8 [lindex [ixNet remapIds $statistic_8] 0]
ixNet setMultiAttribute $Root/globals/interfaces \
	-arpOnLinkup true \
	-nsOnLinkup true \
	-sendSingleArpPerGateway true \
	-sendSingleNsPerGateway true

ixNet commit
ixNet setMultiAttribute $Root/traffic \
	-cycleTimeUnitForScheduledStart milliseconds \
	-refreshLearnedInfoBeforeApply true \
	-detectMisdirectedOnAllPorts false \
	-useRfc5952 true \
	-cycleOffsetForScheduledStart 0 \
	-cycleOffsetUnitForScheduledStart nanoseconds \
	-enableEgressOnlyTracking false \
	-cycleTimeForScheduledStart 1 \
	-enableLagFlowBalancing true \
	-peakLoadingReplicationCount 1

ixNet setMultiAttribute $Root/traffic/statistics/misdirectedPerFlow \
	-enabled false

ixNet setMultiAttribute $Root/traffic/statistics/multipleJoinLeaveLatency \
	-enabled false

ixNet setMultiAttribute $Root/traffic/statistics/oneTimeJoinLeaveLatency \
	-enabled false

ixNet commit
set trafficItem [ixNet add $Root/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem \
	-name Top1-To-Top2 \
	-multicastForwardingMode replication \
	-useControlPlaneRate true \
	-useControlPlaneFrameSize true \
	-roundRobinPacketOrdering false \
	-numVlansForMulticastReplication 1 \
	-trafficType ipv4
ixNet commit
set trafficItem [lindex [ixNet remapIds $trafficItem] 0]

set endpointSet [ixNet add $trafficItem "endpointSet"]
ixNet setMultiAttribute $endpointSet \
	-multicastDestinations [list ] \
	-destinations [list $deviceGroup_P2] \
	-scalableSources [list ] \
	-multicastReceivers [list ] \
	-scalableDestinations [list ] \
	-ngpfFilters [list ] \
	-trafficGroups [list ] \
	-sources [list $topo1] \
	-name EndpointSet-1
ixNet commit
set endpointSet [lindex [ixNet remapIds $endpointSet] 0]

set egressTracking [ixNet add $trafficItem "egressTracking"]
ixNet commit
set egressTracking [lindex [ixNet remapIds $egressTracking] 0]


ixNet setMultiAttribute $trafficItem/tracking \
	-trackBy [list ipv4SourceIp0 trackingenabled0] \
	-values [list ] \
	-fieldWidth thirtyTwoBits \
	-protocolOffset Root.0

ixNet setMultiAttribute $trafficItem/tracking/latencyBin \
	-binLimits [list 1 1.42 2 2.82 4 5.66 8 2147483647]

ixNet commit

###############################################################################
# 5. Apply and start L2/L3 traffic
###############################################################################
puts "applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 60000

###############################################################################
# 6. Retrieve L2/L3 traffic item statistics
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
# 7. Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 8. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
