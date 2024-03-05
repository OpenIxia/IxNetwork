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

#####################################################################################################        
#                                                                                                   #
# Description:                                                                                      #
#    This script intends to demonstrate how to use Flex-Algo Over  ISIS-SRv6 Using TCL APIs.        #  
#                                                                                                   #
#    1. It will create 2 ISISL3 topologies with Flex Algorithm enabled, each having an ipv6 network #                    
#       topology and loopback devicegroup behind the network group(NG) with loopback interface.     #
#    2. Configure ISIS with SRv6.                                                                   #
#    3. Configure Flex-Algo related fields one by one.                                              #
#    4. Start protocols                                                                             #
#    5. Retrieve protocol statistics.                                                               #
#    6. Retrieve protocol learned info.                                                             #
#    7. Stop all protocols.                                                                         #                                                                                          
#####################################################################################################                     

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.50.121
    set ixTclPort   8017
    set ports       {{10.39.50.179 2 3} {10.39.50.179 2 4}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 9.10\
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

set isisL3Router1 [lindex [ixNet getList $t1dev1 isisL3Router] 0]
set isisL3Router2 [lindex [ixNet getList $t2dev1 isisL3Router] 0]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "Ingress"
ixNet setAttr $topo2  -name "Egress"

ixNet setAttr $t1dev1 -name "P1"
ixNet setAttr $t2dev1 -name "P2"
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

#Flex Algorithm related Configuration
puts "Setting Flex Algo Count"
ixNet setAttribute $isisL3Router1 -flexAlgoCount 4
ixNet setAttribute $isisL3Router2 -flexAlgoCount 4
ixNet commit

set isisFlexAlgorithmList1 [lindex [ixNet getList $isisL3Router1 isisFlexAlgorithmList] 0]
set isisFlexAlgorithmList2 [lindex [ixNet getList $isisL3Router2 isisFlexAlgorithmList] 0]

puts "Setting Metric Type"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList1 -metricType]/singleValue -value "1"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList2 -metricType]/singleValue -value "1"
ixNet commit

puts "Setting Calc Type"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList1 -calcType]/singleValue -value "2"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList2 -calcType]/singleValue -value "2"
ixNet commit

puts "Setting priority Type"
set priority [ixNet getAttribute $isisFlexAlgorithmList1 -priority]
ixNet setMultiAttribute $priority \
	-clearOverlays false
	ixNet commit
set prioritycounter [ixNet add $priority "counter"]
ixNet setMultiAttribute $prioritycounter \
	-step 1 \
	-start 100 \
	-direction increment
ixNet commit

puts "Setting enable Exclude Ag"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList1 -enableExcludeAg]/singleValue -value "true"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList2 -enableExcludeAg]/singleValue -value "true"
ixNet commit

puts "Setting Ext Ag Len"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList1 -excludeAgExtAgLen]/singleValue -value "2"
ixNet commit

puts "set Ext-ExcludeAG Value .."
set ExcludeAgExtAg [ixNet getAttribute $isisFlexAlgorithmList1 -excludeAgExtAg]
ixNet setMultiAttribute $ExcludeAgExtAg \
	-clearOverlays false
ixNet commit

set excludeAgExtAgcounter [ixNet add $ExcludeAgExtAg "counter"]
ixNet setMultiAttribute $excludeAgExtAgcounter \
	-step 01 \
	-start 00000000 \
	-direction increment
ixNet commit

set overlay1 [ixNet add $ExcludeAgExtAg "overlay"]
ixNet setMultiAttribute $overlay1 \
	-count 1 \
	-index 1 \
	-value 0000000000000005
ixNet commit

set overlay2 [ixNet add $ExcludeAgExtAg "overlay"]
ixNet setMultiAttribute $overlay2 \
	-count 1 \
	-index 2 \
	-value 0000000000000066
ixNet commit

set overlay3 [ixNet add $ExcludeAgExtAg "overlay"]
ixNet setMultiAttribute $overlay3 \
	-count 1 \
	-index 3 \
	-value 0000000000000077
ixNet commit

set overlay4 [ixNet add $ExcludeAgExtAg "overlay"]
ixNet setMultiAttribute $overlay4 \
	-count 1 \
	-index 4 \
	-value 0000000000000088
ixNet commit

puts "Setting enable Include Any Ag"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList1 -enableIncludeAnyAg]/singleValue -value "true"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList2 -enableIncludeAnyAg]/singleValue -value "true"
ixNet commit

puts "Setting Ext Ag Len"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList1 -includeAnyAgExtAgLen]/singleValue -value "1"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList2 -includeAnyAgExtAgLen]/singleValue -value "1"
ixNet commit

puts "Setting include AnyAgExt"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList1 -includeAnyAgExtAg]/singleValue -value "BB000001"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList2 -includeAnyAgExtAg]/singleValue -value "BB000001"
ixNet commit


puts "Setting enable Include All Ag"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList1 -enableIncludeAllAg]/singleValue -value "true"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList2 -enableIncludeAllAg]/singleValue -value "true"
ixNet commit

puts "Setting Ext Ag Len"
set IncludeAllAgExtAgLen [ixNet getAttribute $isisFlexAlgorithmList1 -includeAllAgExtAgLen]
ixNet setMultiAttribute $IncludeAllAgExtAgLen \
	-clearOverlays false
ixNet commit

set IncludeAllAgExtAgLencounter [ixNet add $IncludeAllAgExtAgLen "counter"]
ixNet setMultiAttribute $IncludeAllAgExtAgLencounter \
	-step 1 \
	-start 1 \
	-direction increment
ixNet commit

ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList2 -includeAllAgExtAgLen]/singleValue -value "1"
ixNet commit

puts "Setting include AllAgExt"
set IncludeAllAgExtAg [ixNet getAttribute $isisFlexAlgorithmList1 -includeAllAgExtAg]
ixNet setMultiAttribute $IncludeAllAgExtAg \
	-clearOverlays false
ixNet commit

set includeallAgExtAgcounter [ixNet add $IncludeAllAgExtAg "counter"]
ixNet setMultiAttribute $includeallAgExtAgcounter \
	-step 01 \
	-start 00000000 \
	-direction increment
ixNet commit

set overlay1 [ixNet add $IncludeAllAgExtAg "overlay"]
ixNet setMultiAttribute $overlay1 \
	-count 1 \
	-index 1 \
	-value 0000055
ixNet commit

set overlay2 [ixNet add $IncludeAllAgExtAg "overlay"]
ixNet setMultiAttribute $overlay2 \
	-count 1 \
	-index 2 \
	-value 0000000000000066
ixNet commit

set overlay3 [ixNet add $IncludeAllAgExtAg "overlay"]
ixNet setMultiAttribute $overlay3 \
	-count 1 \
	-index 3 \
	-value 000000000000000000000077
ixNet commit

set overlay4 [ixNet add $IncludeAllAgExtAg "overlay"]
ixNet setMultiAttribute $overlay4 \
	-count 1 \
	-index 4 \
	-value 00000000000000000000000000000088
ixNet commit

puts "Setting enableFadfTlv"
set EnableFadfTlv [ixNet getAttribute $isisFlexAlgorithmList1 -enableFadfTlv]
ixNet setMultiAttribute $EnableFadfTlv \
	-clearOverlays false
ixNet commit

set EnableFadfTlvalternate [ixNet add $EnableFadfTlv "alternate"]
ixNet setMultiAttribute $EnableFadfTlvalternate \
	-value true
ixNet commit

ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList2 -enableFadfTlv]/singleValue -value "true"
ixNet commit

puts "Setting FAD Len"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList1 -fadfLen]/singleValue -value "1"
ixNet commit

set fadfLen2 [ixNet getAttribute $isisFlexAlgorithmList2 -fadfLen]
ixNet setMultiAttribute $fadfLen2 \
	-clearOverlays false
ixNet commit

set fadflengthcounter [ixNet add $fadfLen2 "counter"]
ixNet setMultiAttribute $fadflengthcounter \
	-step 1 \
	-start 1 \
	-direction increment
ixNet commit

puts "Setting include mFlag"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList1 -mFlag]/singleValue -value "true"
ixNet commit

set mFlag2 [ixNet getAttribute $isisFlexAlgorithmList2 -mFlag]
ixNet setMultiAttribute $mFlag2 \
	-clearOverlays false
ixNet commit

set singleValue2 [ixNet add $mFlag2 "singleValue"]
ixNet setMultiAttribute $singleValue2 \
	-value true
ixNet commit

set mFlag2overlay [ixNet add $mFlag2 "overlay"]
ixNet setMultiAttribute $mFlag2overlay \
	-count 1 \
	-index 1 \
	-value false
ixNet commit

puts "Setting Reserved bits"
ixNet setAttr [ixNet getAttribute $isisFlexAlgorithmList1 -reservedBits]/singleValue -value "0xAB"
set reservedBits2 [ixNet getAttribute $isisFlexAlgorithmList2 -reservedBits]
ixNet setMultiAttribute $reservedBits2 \
	-clearOverlays false
ixNet commit

set reservedBits2counteroverlay1 [ixNet add $reservedBits2 "overlay"]
ixNet setMultiAttribute $reservedBits2counteroverlay1 \
	-count 1 \
	-index 3 \
	-value 00AB
ixNet commit

set reservedBits2counteroverlay2 [ixNet add $reservedBits2 "overlay"]
ixNet setMultiAttribute $reservedBits2counteroverlay2 \
	-count 1 \
	-index 4 \
	-value 0000AB
ixNet commit

################################################################################
# 2. Start ISISl3 protocol and wait for 60 seconds
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
# 4. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
