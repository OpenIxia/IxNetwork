#/usr/bin/tclsh

################################################################################
#                                                                              #
#    Copyright 1997 - 2021 by Keysight                                         #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################

####################################################################################    
#                                                                                  #
#                                LEGAL  NOTICE:                                    #
#                                ==============                                    #
# The following code and documentation (hereinafter "the script") is an            #
# example script for demonstration purposes only.                                  #
# The script is not a standard commercial product offered by Keysight and have     #
# been developed and is being provided for use only as indicated herein. The       #
# script [and all modifications enhancements and updates thereto (whether          #
# made by Keysight and/or by the user and/or by a third party)] shall at all times #
# remain the property of Keysight.                                                 #
#                                                                                  #
# Keysight does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without              #
# omissions or error-free.                                                         #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND Keysight         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE                  #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR     #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                     #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE     #
# USER.                                                                            #
# IN NO EVENT SHALL Keysight BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF         #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR              #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR                  #
# CONSEQUENTIAL DAMAGES EVEN IF Keysight HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                         #
# Keysight will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the         #
# script or any part thereof. The user acknowledges that although Keysight may     #
# from time to time and in its sole discretion provide maintenance or support      #
# services for the script any such services are subject to the warranty and        #
# damages limitations set forth herein and will not obligate Keysight to provide   #
# any additional maintenance or support services.                                  #
#                                                                                  #
####################################################################################   

################################################################################################
#                                                                                              #
# Description:                                                                                 #
#    This script intends to demonstrate how to use OSPFv3 SRv6 TCL APIs.                       #
#                                                                                              #
#    1. This configuration template provides an example of basic OSPFv3 Segment Routing over   #
#       IPV6 data plane configuration in back-to-back scenerio for point-to-point network.     #
#       One port emulates 1 OSPFv3 router and other port emulates 1 OSPFv3 router with a       #
#       Linear topology having 2 nodes behind it.Each node of linear topology are configured   #
#		with SRV6, also emulated OSPFv3 router are SRv6 enabled and it will providee the Locator#
#		and SID.                                                                               #
#    2. Start the OSPFV3 protocol.                                                             #
#    3. Retrieve protocol statistics.                                                          #
#    4. Stop all protocols.                                                                    #                                                                                          
################################################################################################   

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::Keysight {
    set ixTclServer 10.39.43.12
    set ixTclPort   8012
    set ports       {{10.39.50.200 1 5} {10.39.50.200 1 6}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::Keysight::ixTclServer -port $::Keysight::ixTclPort -version 8.50\
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
::ixTclNet::AssignPorts $Keysight::ports {} $vPorts force

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
puts "Adding ospfv3Router over IPv6 stacks"
ixNet add $ip1 ospfv3
ixNet add $ip2 ospfv3
ixNet commit

set ospfv3Rtr_1 [ixNet getList $t1dev1 ospfv3Router]
set ospfv3Rtr_2 [ixNet getList $t2dev1 ospfv3Router]

set ospfv3_1 [ixNet getList $ip1 ospfv3]
set ospfv3_2 [ixNet getList $ip2 ospfv3]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "ospfv3 Topology 1"
ixNet setAttr $topo2  -name "ospfv3 Topology 2"

ixNet setAttr $t1dev1 -name "ospfv3 Topology 1 Router"
ixNet setAttr $t2dev1 -name "ospfv3 Topology 2 Router"
ixNet commit

#Change the property of OSPFv3 IF
puts "Change the Property of OSPFv3 IF"
set Network_Type_1 [ixNet getAttribute $ospfv3_1 -networkType]
set singleValue_1 [ixNet add $Network_Type_1 "singleValue"]
ixNet setMultiAttribute $singleValue_1 -value pointtopoint
ixNet commit
set Network_Type_1 [ixNet getAttribute $ospfv3_2 -networkType]
set singleValue_1 [ixNet add $Network_Type_1 "singleValue"]
ixNet setMultiAttribute $singleValue_1 -value pointtopoint
ixNet commit

#Change the value of -enableIPv6SID
puts "Change the value enableIPv6SID"
set enableIPv6SID_1 [ixNet getAttribute $ospfv3_1 -enableIPv6SID]
set single_value_1 [ixNet add $enableIPv6SID_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set enableIPv6SID_1 [ixNet getAttribute $ospfv3_2 -enableIPv6SID]
set single_value_1 [ixNet add $enableIPv6SID_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit


#Enable the ipv6Srh means Enable SR-IPv6
puts "Enabling the ipv6Srh means Enable SR-IPv6"
set ipv6Srh_1 [ixNet getAttribute $ospfv3Rtr_1 -ipv6Srh]
set single_value_1 [ixNet add $ipv6Srh_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set ipv6Srh_1 [ixNet getAttribute $ospfv3Rtr_2 -ipv6Srh]
set single_value_1 [ixNet add $ipv6Srh_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit

#Change the value flagOfSRv6Cap 
puts "Change the value flagOfSRv6Cap"
set flagOfSRv6Cap_1 [ixNet getAttribute $ospfv3Rtr_1 -flagOfSRv6Cap]
set single_value_1 [ixNet add $flagOfSRv6Cap_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 4000
ixNet commit
set flagOfSRv6Cap_1 [ixNet getAttribute $ospfv3Rtr_2 -flagOfSRv6Cap]
set single_value_1 [ixNet add $flagOfSRv6Cap_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 4000
ixNet commit

#Change the value reservedInsideSRv6Cap 
puts "Change the value reservedInsideSRv6Cap"
set reservedInsideSRv6Cap_1 [ixNet getAttribute $ospfv3Rtr_1 -reservedInsideSRv6Cap]
set single_value_1 [ixNet add $reservedInsideSRv6Cap_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 3fff
ixNet commit
set reservedInsideSRv6Cap_1 [ixNet getAttribute $ospfv3Rtr_2 -reservedInsideSRv6Cap]
set single_value_1 [ixNet add $reservedInsideSRv6Cap_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 3fff
ixNet commit

#Change the value sRv6NodePrefix 
puts "Change the value sRv6NodePrefix"
set sRv6NodePrefix_1 [ixNet getAttribute $ospfv3Rtr_1 -sRv6NodePrefix]
set single_value_1 [ixNet add $sRv6NodePrefix_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 2000:0:0:1:0:0:0:1
ixNet commit
set sRv6NodePrefix_1 [ixNet getAttribute $ospfv3Rtr_2 -sRv6NodePrefix]
set single_value_1 [ixNet add $sRv6NodePrefix_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 2000:0:0:1:0:0:0:2
ixNet commit

#Change the value srv6PrefixOptions 
puts "Change the value srv6PrefixOptions"
set srv6PrefixOptions_1 [ixNet getAttribute $ospfv3Rtr_1 -srv6PrefixOptions]
set single_value_1 [ixNet add $srv6PrefixOptions_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 128
ixNet commit
set srv6PrefixOptions_1 [ixNet getAttribute $ospfv3Rtr_2 -srv6PrefixOptions]
set single_value_1 [ixNet add $srv6PrefixOptions_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 128
ixNet commit


#Enable the advertiseNodeMsd
puts "Enabling the advertiseNodeMsd"
set advertiseNodeMsd_1 [ixNet getAttribute $ospfv3Rtr_1 -advertiseNodeMsd]
set single_value_1 [ixNet add $advertiseNodeMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set advertiseNodeMsd_1 [ixNet getAttribute $ospfv3Rtr_2 -advertiseNodeMsd]
set single_value_1 [ixNet add $advertiseNodeMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit

#Enable the includeMaxSlMsd
puts "Enabling the includeMaxSlMsd"
set includeMaxSlMsd_1 [ixNet getAttribute $ospfv3Rtr_1 -includeMaxSlMsd]
set single_value_1 [ixNet add $includeMaxSlMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set includeMaxSlMsd_1 [ixNet getAttribute $ospfv3Rtr_2 -includeMaxSlMsd]
set single_value_1 [ixNet add $includeMaxSlMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the includeMaximumEndPopMsd
puts "Enabling the includeMaximumEndPopMsd"
set includeMaximumEndPopMsd_1 [ixNet getAttribute $ospfv3Rtr_1 -includeMaximumEndPopMsd]
set single_value_1 [ixNet add $includeMaximumEndPopMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set includeMaximumEndPopMsd_1 [ixNet getAttribute $ospfv3Rtr_2 -includeMaximumEndPopMsd]
set single_value_1 [ixNet add $includeMaximumEndPopMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the includeMaximumHEncapMsd
puts "Enabling the includeMaximumHEncapMsd"
set includeMaximumHEncapMsd_1 [ixNet getAttribute $ospfv3Rtr_1 -includeMaximumHEncapMsd]
set single_value_1 [ixNet add $includeMaximumHEncapMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set includeMaximumHEncapMsd_1 [ixNet getAttribute $ospfv3Rtr_2 -includeMaximumHEncapMsd]
set single_value_1 [ixNet add $includeMaximumHEncapMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
#Enable the includeMaximumEndDMsd
puts "Enabling the includeMaximumEndDMsd"
set includeMaximumEndDMsd_1 [ixNet getAttribute $ospfv3Rtr_1 -includeMaximumEndDMsd]
set single_value_1 [ixNet add $includeMaximumEndDMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit
set includeMaximumEndDMsd_1 [ixNet getAttribute $ospfv3Rtr_2 -includeMaximumEndDMsd]
set single_value_1 [ixNet add $includeMaximumEndDMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit


#Change the value of maxSlMsd 
puts "Change the value of maxSlMsd"
set maxSlMsd_1 [ixNet getAttribute $ospfv3Rtr_1 -maxSlMsd]
set single_value_1 [ixNet add $maxSlMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 5
ixNet commit
set maxSlMsd_1 [ixNet getAttribute $ospfv3Rtr_2 -maxSlMsd]
set single_value_1 [ixNet add $maxSlMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 5
ixNet commit

#Change the value of maxEndPopMsd 
puts "Change the value of maxEndPopMsd"
set maxEndPopMsd_1 [ixNet getAttribute $ospfv3Rtr_1 -maxEndPopMsd]
set single_value_1 [ixNet add $maxEndPopMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 5
ixNet commit
set maxEndPopMsd_1 [ixNet getAttribute $ospfv3Rtr_2 -maxEndPopMsd]
set single_value_1 [ixNet add $maxEndPopMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 5
ixNet commit

#Change the value of maxHEncapsMsd 
puts "Change the value of maxHEncapsMsd"
set maxHEncapsMsd_1 [ixNet getAttribute $ospfv3Rtr_1 -maxHEncapsMsd]
set single_value_1 [ixNet add $maxHEncapsMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 5
ixNet commit
set maxHEncapsMsd_1 [ixNet getAttribute $ospfv3Rtr_2 -maxHEncapsMsd]
set single_value_1 [ixNet add $maxHEncapsMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 5
ixNet commit

#Change the value of maxEndDMsd 
puts "Change the value of maxEndDMsd"
set maxEndDMsd_1 [ixNet getAttribute $ospfv3Rtr_1 -maxEndDMsd]
set single_value_1 [ixNet add $maxEndDMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 5
ixNet commit
set maxEndDMsd_1 [ixNet getAttribute $ospfv3Rtr_2 -maxEndDMsd]
set single_value_1 [ixNet add $maxEndDMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 5
ixNet commit


#Change the value of locatorCount 
puts "Change the value of locatorCount"
ixNet setAttribute $ospfv3Rtr_1 -locatorCount 1
ixNet commit
ixNet setAttribute $ospfv3Rtr_2 -locatorCount 1
ixNet commit

#Change the value of metric 
puts "Change the value of metric"
set metric_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList -metric]
set single_value_1 [ixNet add $metric_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 1
ixNet commit
set metric_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList -metric]
set single_value_1 [ixNet add $metric_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 1
ixNet commit


#Change the value of algorithm 
puts "Change the value of algorithm"
set algorithm_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList -algorithm]
set single_value_1 [ixNet add $algorithm_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 1
ixNet commit
set algorithm_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList -algorithm]
set single_value_1 [ixNet add $algorithm_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 1
ixNet commit

#Enable the nBit
puts "Enable the nBit"
set nBit_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList -nBit]
set Single_Value_1 [ixNet add $nBit_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit
set nBit_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList -nBit]
set Single_Value_1 [ixNet add $nBit_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit

#Enable the aBit
puts "Enable the aBit"
set aBit_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList -aBit]
set Single_Value_1 [ixNet add $aBit_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit
set aBit_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList -aBit]
set Single_Value_1 [ixNet add $aBit_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit

#Change the value of reservedFlag"
puts "Change the value of reservedFlag"
set reservedFlag_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList -reservedFlag]
set Single_Value_1 [ixNet add $reservedFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 01
ixNet commit
set reservedFlag_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList -reservedFlag]
set Single_Value_1 [ixNet add $reservedFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 01
ixNet commit

#Change the value of locatorLength
puts "Change the value of locatorLength"
set locatorLength_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList -locatorLength]
set Single_Value_1 [ixNet add $locatorLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 64
ixNet commit
set locatorLength_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList -locatorLength]
set Single_Value_1 [ixNet add $locatorLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 64
ixNet commit

#Enable the advertiseLocatorAsPrefix
puts "Enable the advertiseLocatorAsPrefix"
set advertiseLocatorAsPrefix_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList -advertiseLocatorAsPrefix]
set Single_Value_1 [ixNet add $advertiseLocatorAsPrefix_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit
set advertiseLocatorAsPrefix_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList -advertiseLocatorAsPrefix]
set Single_Value_1 [ixNet add $advertiseLocatorAsPrefix_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit


#Change the value of locatorRouteType
puts "Change the value of locatorRouteType"
set locatorRouteType_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList -locatorRouteType]
set Single_Value_1 [ixNet add $locatorRouteType_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value intraarea
ixNet commit
set locatorRouteType_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList -locatorRouteType]
set Single_Value_1 [ixNet add $locatorRouteType_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value intraarea
ixNet commit

#Change the value of prefixMetric
puts "Change the value of prefixMetric"
set prefixMetric_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList -prefixMetric]
set Single_Value_1 [ixNet add $prefixMetric_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 64
ixNet commit
set prefixMetric_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList -prefixMetric]
set Single_Value_1 [ixNet add $prefixMetric_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 64
ixNet commit

#Change the value of sidCount 
puts "Change the value of sidCount"
ixNet setAttribute $ospfv3Rtr_1 -sidCount 1
ixNet commit
ixNet setAttribute $ospfv3Rtr_2 -sidCount 1
ixNet commit

#Change the value of flags
puts "Change the value of flags"
set flags_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -flags]
set Single_Value_1 [ixNet add $flags_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 01
ixNet commit
set flags_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -flags]
set Single_Value_1 [ixNet add $flags_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 01
ixNet commit

#Change the value of reserved
puts "Change the value of reserved"
set reserved_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -reserved]
set Single_Value_1 [ixNet add $reserved_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 02
ixNet commit
set reserved_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -reserved]
set Single_Value_1 [ixNet add $reserved_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 02
ixNet commit

#Change the value of endPointFunction
puts "Change the value of endPointFunction"
set endPointFunction_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -endPointFunction]
set Single_Value_1 [ixNet add $endPointFunction_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 5
ixNet commit
set endPointFunction_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -endPointFunction]
set Single_Value_1 [ixNet add $endPointFunction_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 5
ixNet commit

#Change the value of includeSRv6SIDStructureSubTlv
puts "Change the value of includeSRv6SIDStructureSubTlv"
set includeSRv6SIDStructureSubTlv_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -includeSRv6SIDStructureSubTlv]
set Single_Value_1 [ixNet add $includeSRv6SIDStructureSubTlv_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit
set includeSRv6SIDStructureSubTlv_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -includeSRv6SIDStructureSubTlv]
set Single_Value_1 [ixNet add $includeSRv6SIDStructureSubTlv_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit

#Change the value of locatorBlockLength
puts "Change the value of locatorBlockLength"
set locatorBlockLength_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -locatorBlockLength]
set Single_Value_1 [ixNet add $locatorBlockLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 40
ixNet commit
set locatorBlockLength_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -locatorBlockLength]
set Single_Value_1 [ixNet add $locatorBlockLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 40
ixNet commit

#Change the value of locatorNodeLength
puts "Change the value of locatorNodeLength"
set locatorNodeLength_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -locatorNodeLength]
set Single_Value_1 [ixNet add $locatorNodeLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 24
ixNet commit
set locatorNodeLength_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -locatorNodeLength]
set Single_Value_1 [ixNet add $locatorNodeLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 24
ixNet commit

#Change the value of functionLength
puts "Change the value of functionLength"
set functionLength_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -functionLength]
set Single_Value_1 [ixNet add $functionLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 16
ixNet commit
set functionLength_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -functionLength]
set Single_Value_1 [ixNet add $functionLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 16
ixNet commit
 
#Change the value of argumentLength
puts "Change the value of argumentLength"
set argumentLength_1 [ixNet getAttribute $ospfv3Rtr_1/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -argumentLength]
set Single_Value_1 [ixNet add $argumentLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 0
ixNet commit
set argumentLength_1 [ixNet getAttribute $ospfv3Rtr_2/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList -argumentLength]
set Single_Value_1 [ixNet add $argumentLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 0
ixNet commit

#Change the value of adjSidCount 
puts "Change the value of adjSidCount"
ixNet setAttribute $ospfv3Rtr_1 -adjSidCount 1
ixNet commit
ixNet setAttribute $ospfv3Rtr_2 -adjSidCount 1
ixNet commit

#Change the value of bFlag
puts "Change the value of bFlag"
set bFlag_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -bFlag]
set Single_Value_1 [ixNet add $bFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit
set bFlag_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -bFlag]
set Single_Value_1 [ixNet add $bFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit

#Change the value of sFlag
puts "Change the value of sFlag"
set sFlag_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -sFlag]
set Single_Value_1 [ixNet add $sFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit
set sFlag_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -sFlag]
set Single_Value_1 [ixNet add $sFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit

#Change the value of pFlag
puts "Change the value of pFlag"
set pFlag_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -pFlag]
set Single_Value_1 [ixNet add $pFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit
set pFlag_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -pFlag]
set Single_Value_1 [ixNet add $pFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit

#Change the value of reservedFlag
puts "Change the value of reservedFlag"
set reservedFlag_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -reservedFlag]
set Single_Value_1 [ixNet add $reservedFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 01
ixNet commit
set reservedFlag_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -reservedFlag]
set Single_Value_1 [ixNet add $reservedFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 01
ixNet commit

#Change the value of algorithm
puts "Change the value of algorithm"
set algorithm_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -algorithm]
set Single_Value_1 [ixNet add $algorithm_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 1
ixNet commit
set algorithm_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -algorithm]
set Single_Value_1 [ixNet add $algorithm_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 1
ixNet commit

#Change the value of weight
puts "Change the value of weight"
set weight_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -weight]
set Single_Value_1 [ixNet add $weight_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 100
ixNet commit
set weight_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -weight]
set Single_Value_1 [ixNet add $weight_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 100
ixNet commit

#Change the value of reserved1
puts "Change the value of reserved1"
set reserved1_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -reserved1]
set Single_Value_1 [ixNet add $reserved1_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 01
ixNet commit
set reserved1_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -reserved1]
set Single_Value_1 [ixNet add $reserved1_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 01
ixNet commit



#Change the value of reserved2
puts "Change the value of reserved2"
set reserved2_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -reserved2]
set Single_Value_1 [ixNet add $reserved2_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 0001
ixNet commit
set reserved2_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -reserved2]
set Single_Value_1 [ixNet add $reserved2_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 0001
ixNet commit

    
#Change the value of endPointFunction
puts "Change the value of endPointFunction"
set endPointFunction_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -endPointFunction]
set Single_Value_1 [ixNet add $endPointFunction_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 9
ixNet commit
set endPointFunction_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -endPointFunction]
set Single_Value_1 [ixNet add $endPointFunction_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 9
ixNet commit

#Change the value of includeSRv6SIDStructureSubTlv
puts "Change the value of includeSRv6SIDStructureSubTlv"
set includeSRv6SIDStructureSubTlv_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -includeSRv6SIDStructureSubTlv]
set Single_Value_1 [ixNet add $includeSRv6SIDStructureSubTlv_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit
set includeSRv6SIDStructureSubTlv_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -includeSRv6SIDStructureSubTlv]
set Single_Value_1 [ixNet add $includeSRv6SIDStructureSubTlv_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit

#Change the value of locatorBlockLength
puts "Change the value of locatorBlockLength"
set locatorBlockLength_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -locatorBlockLength]
set Single_Value_1 [ixNet add $locatorBlockLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 40
ixNet commit
set locatorBlockLength_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -locatorBlockLength]
set Single_Value_1 [ixNet add $locatorBlockLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 40
ixNet commit

#Change the value of locatorNodeLength
puts "Change the value of locatorNodeLength"
set locatorNodeLength_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -locatorNodeLength]
set Single_Value_1 [ixNet add $locatorNodeLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 24
ixNet commit
set locatorNodeLength_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -locatorNodeLength]
set Single_Value_1 [ixNet add $locatorNodeLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 24
ixNet commit

#Change the value of functionLength
puts "Change the value of functionLength"
set functionLength_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -functionLength]
set Single_Value_1 [ixNet add $functionLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 16
ixNet commit
set functionLength_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -functionLength]
set Single_Value_1 [ixNet add $functionLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 16
ixNet commit
 
#Change the value of argumentLength
puts "Change the value of argumentLength"
set argumentLength_1 [ixNet getAttribute $ospfv3_1/ospfv3SRv6AdjSIDList -argumentLength]
set Single_Value_1 [ixNet add $argumentLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 0
ixNet commit
set argumentLength_1 [ixNet getAttribute $ospfv3_2/ospfv3SRv6AdjSIDList -argumentLength]
set Single_Value_1 [ixNet add $argumentLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 0
ixNet commit
		
set networkGroup_P2 [ixNet add $t2dev1 "networkGroup"]
ixNet setMultiAttribute $networkGroup_P2 \
	-name "Routers"
ixNet commit
set networkGroup_P2 [lindex [ixNet remapIds $networkGroup_P2] 0]
set Network_Topology [ixNet add $networkGroup_P2 "networkTopology"]
ixNet commit
set Network_Topology [lindex [ixNet remapIds $Network_Topology] 0]
set netTopologyLinear [ixNet add $Network_Topology "netTopologyLinear"]
ixNet commit
set netTopologyLinear [lindex [ixNet remapIds $netTopologyLinear] 0]
ixNet setMultiAttribute $netTopologyLinear \
	-nodes 4
ixNet commit

#Enable the ipv6Srh means Enable SR-IPv6 ospfv3PseudoRouter
puts "Enabling the ipv6Srh means Enable SR-IPv6 ospfv3PseudoRouter"
set ipv6Srh_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -ipv6Srh]
set single_value_1 [ixNet add $ipv6Srh_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit


#Change the value flagOfSRv6Cap 
puts "Change the value flagOfSRv6Cap"
set flagOfSRv6Cap_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -flagOfSRv6Cap]
set single_value_1 [ixNet add $flagOfSRv6Cap_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 4000
ixNet commit


#Change the value reservedInsideSRv6Cap 
puts "Change the value reservedInsideSRv6Cap"
set reservedInsideSRv6Cap_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -reservedInsideSRv6Cap]
set single_value_1 [ixNet add $reservedInsideSRv6Cap_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 3fff
ixNet commit


#Change the value sRv6NodePrefix 
puts "Change the value sRv6NodePrefix"
set sRv6NodePrefix_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -sRv6NodePrefix]
set single_value_1 [ixNet add $sRv6NodePrefix_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 2000:0:0:1:0:0:0:1
ixNet commit


#Change the value srv6PrefixOptions 
puts "Change the value srv6PrefixOptions"
set srv6PrefixOptions_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -srv6PrefixOptions]
set single_value_1 [ixNet add $srv6PrefixOptions_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 128
ixNet commit



#Enable the advertiseNodeMsd
puts "Enabling the advertiseNodeMsd"
set advertiseNodeMsd_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -advertiseNodeMsd]
set single_value_1 [ixNet add $advertiseNodeMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit


#Enable the includeMaxSlMsd
puts "Enabling the includeMaxSlMsd"
set includeMaxSlMsd_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -includeMaxSlMsd]
set single_value_1 [ixNet add $includeMaxSlMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit

#Enable the includeMaximumEndPopMsd
puts "Enabling the includeMaximumEndPopMsd"
set includeMaximumEndPopMsd_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -includeMaximumEndPopMsd]
set single_value_1 [ixNet add $includeMaximumEndPopMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit

#Enable the includeMaximumHEncapsMsd
puts "Enabling the includeMaximumHEncapsMsd"
set includeMaximumHEncapsMsd_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -includeMaximumHEncapsMsd]
set single_value_1 [ixNet add $includeMaximumHEncapsMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit

#Enable the includeMaximumEndDMsd
puts "Enabling the includeMaximumEndDMsd"
set includeMaximumEndDMsd_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -includeMaximumEndDMsd]
set single_value_1 [ixNet add $includeMaximumEndDMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value true
ixNet commit

#Change the value of maxSlMsd 
puts "Change the value of maxSlMsd"
set maxSlMsd_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -maxSlMsd]
set single_value_1 [ixNet add $maxSlMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 5
ixNet commit


#Change the value of maxEndPopMsd 
puts "Change the value of maxEndPopMsd"
set maxEndPopMsd_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -maxEndPopMsd]
set single_value_1 [ixNet add $maxEndPopMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 5
ixNet commit


#Change the value of maxHEncapsMsd 
puts "Change the value of maxHEncapsMsd"
set maxHEncapsMsd_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -maxHEncapsMsd]
set single_value_1 [ixNet add $maxHEncapsMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 5
ixNet commit


#Change the value of maxEndDMsd 
puts "Change the value of maxEndDMsd"
set maxEndDMsd_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -maxEndDMsd]
set single_value_1 [ixNet add $maxEndDMsd_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 5
ixNet commit


#Change the value of locatorCount 
puts "Change the value of locatorCount"
ixNet setAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -locatorCount 1
ixNet commit
ixNet setAttribute $ospfv3Rtr_2 -locatorCount 1
ixNet commit

#Change the value of metric 
puts "Change the value of metric"
set metric_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList -metric]
set single_value_1 [ixNet add $metric_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 1
ixNet commit

#Change the value of algorithm 
puts "Change the value of algorithm"
set algorithm_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList -algorithm]
set single_value_1 [ixNet add $algorithm_1 "singleValue"]
ixNet setMultiAttribute $single_value_1 -value 1
ixNet commit

#Enable the nBit
puts "Enable the nBit"
set nBit_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList -nBit]
set Single_Value_1 [ixNet add $nBit_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit


#Enable the aBit
puts "Enable the aBit"
set aBit_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList -aBit]
set Single_Value_1 [ixNet add $aBit_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit


#Change the value of reservedFlag"
puts "Change the value of reservedFlag"
set reservedFlag_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList -reservedFlag]
set Single_Value_1 [ixNet add $reservedFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 01
ixNet commit


#Change the value of locatorLength
puts "Change the value of locatorLength"
set locatorLength_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList -locatorLength]
set Single_Value_1 [ixNet add $locatorLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 64
ixNet commit

#Enable the advertiseLocatorAsPrefix
puts "Enable the advertiseLocatorAsPrefix"
set advertiseLocatorAsPrefix_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList -advertiseLocatorAsPrefix]
set Single_Value_1 [ixNet add $advertiseLocatorAsPrefix_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit

#Change the value of locatorRouteType
puts "Change the value of locatorRouteType"
set locatorRouteType_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList -locatorRouteType]
set Single_Value_1 [ixNet add $locatorRouteType_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value intraarea
ixNet commit


#Change the value of prefixMetric
puts "Change the value of prefixMetric"
set prefixMetric_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList -prefixMetric]
set Single_Value_1 [ixNet add $prefixMetric_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 64
ixNet commit


#Change the value of sidCount 
puts "Change the value of sidCount"
ixNet setAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -sidCount 1
ixNet commit


#Change the value of flags
puts "Change the value of flags"
set flags_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList -flags]
set Single_Value_1 [ixNet add $flags_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 01
ixNet commit


#Change the value of reserved
puts "Change the value of reserved"
set reserved_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList -reserved]
set Single_Value_1 [ixNet add $reserved_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 02
ixNet commit


#Change the value of endPointFunction
puts "Change the value of endPointFunction"
set endPointFunction_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList -endPointFunction]
set Single_Value_1 [ixNet add $endPointFunction_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value endt_nopsp_nousp
ixNet commit


#Change the value of includeSRv6SIDStructureSubTlv
puts "Change the value of includeSRv6SIDStructureSubTlv"
set includeSRv6SIDStructureSubTlv_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList -includeSRv6SIDStructureSubTlv]
set Single_Value_1 [ixNet add $includeSRv6SIDStructureSubTlv_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit


#Change the value of locatorBlockLength
puts "Change the value of locatorBlockLength"
set locatorBlockLength_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList -locatorBlockLength]
set Single_Value_1 [ixNet add $locatorBlockLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 40
ixNet commit


#Change the value of locatorNodeLength
puts "Change the value of locatorNodeLength"
set locatorNodeLength_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList -locatorNodeLength]
set Single_Value_1 [ixNet add $locatorNodeLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 24
ixNet commit


#Change the value of functionLength
puts "Change the value of functionLength"
set functionLength_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList -functionLength]
set Single_Value_1 [ixNet add $functionLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 16
ixNet commit

 #Change the value of argumentLength
puts "Change the value of argumentLength"
set argumentLength_1 [ixNet getAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList -argumentLength]
set Single_Value_1 [ixNet add $argumentLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 0
ixNet commit

#Change the value of adjSidCount 
puts "Change the value of adjSidCount"
ixNet setAttribute $Network_Topology/simRouter:1/ospfv3PseudoRouter:1 -adjSidCount 1
ixNet commit

#Change the value of enableIPv6SID
puts "Change the value of enableIPv6SID"
set enableIPv6SID_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1 -enableIPv6SID]
set Single_Value_1 [ixNet add $enableIPv6SID_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit

#Change the value of bFlag
puts "Change the value of bFlag"
set bFlag_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -bFlag]
set Single_Value_1 [ixNet add $bFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit

#Change the value of sFlag
puts "Change the value of sFlag"
set sFlag_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -sFlag]
set Single_Value_1 [ixNet add $sFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit

#Change the value of pFlag
puts "Change the value of pFlag"
set pFlag_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -pFlag]
set Single_Value_1 [ixNet add $pFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit

#Change the value of reservedFlag
puts "Change the value of reservedFlag"
set reservedFlag_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -reservedFlag]
set Single_Value_1 [ixNet add $reservedFlag_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 01
ixNet commit


#Change the value of algorithm
puts "Change the value of algorithm"
set algorithm_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -algorithm]
set Single_Value_1 [ixNet add $algorithm_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 1
ixNet commit


#Change the value of weight
puts "Change the value of weight"
set weight_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -weight]
set Single_Value_1 [ixNet add $weight_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 100
ixNet commit


#Change the value of reserved1
puts "Change the value of reserved1"
set reserved1_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -reserved1]
set Single_Value_1 [ixNet add $reserved1_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 01
ixNet commit


#Change the value of reserved2
puts "Change the value of reserved2"
set reserved2_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -reserved2]
set Single_Value_1 [ixNet add $reserved2_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 0001
ixNet commit
    
#Change the value of endPointFunction
puts "Change the value of endPointFunction"
set endPointFunction_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -endPointFunction]
set Single_Value_1 [ixNet add $endPointFunction_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value endt_nopsp_nousp 
ixNet commit


#Change the value of includeSRv6SIDStructureSubTlv
puts "Change the value of includeSRv6SIDStructureSubTlv"
set includeSRv6SIDStructureSubTlv_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -includeSRv6SIDStructureSubTlv]
set Single_Value_1 [ixNet add $includeSRv6SIDStructureSubTlv_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value true
ixNet commit

#Change the value of locatorBlockLength
puts "Change the value of locatorBlockLength"
set locatorBlockLength_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -locatorBlockLength]
set Single_Value_1 [ixNet add $locatorBlockLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 40
ixNet commit

#Change the value of locatorNodeLength
puts "Change the value of locatorNodeLength"
set locatorNodeLength_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -locatorNodeLength]
set Single_Value_1 [ixNet add $locatorNodeLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 24
ixNet commit

#Change the value of functionLength
puts "Change the value of functionLength"
set functionLength_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -functionLength]
set Single_Value_1 [ixNet add $functionLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 16
ixNet commit
 
#Change the value of argumentLength
puts "Change the value of argumentLength"
set argumentLength_1 [ixNet getAttribute $Network_Topology/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList -argumentLength]
set Single_Value_1 [ixNet add $argumentLength_1 "singleValue"]
ixNet setMultiAttribute $Single_Value_1 -value 0
ixNet commit

################################################################################
# step 2> Start OSPFv3 protocol and wait for 60 seconds
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000

################################################################################
# step 3> Retrieve protocol statistics.
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


#################################################################################
## step 4> Stop all protocols
#################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
