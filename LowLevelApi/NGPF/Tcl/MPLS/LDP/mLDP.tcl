#!/usr/bin/tclsh
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
#    This script intends to demonstrate how to use NGPF mLDP API.              #
#                                                                              #
#    1. It will create 2 mLDP topologies: 1 Ingress with Root Range configured #
#       and another Egress with Leaf Range.                                    #
#    2. Configure Root Ranges with Source Endpoint.                            #
#    3. Configure Leaf Ranges with Multicast Destination Endpoint.             #
#    4. Start the ldp protocol.                                                #
#    5. Retrieve protocol statistics.                                          #
#    6. Retrieve protocol learned info.                                        #
#    7. Change label and LSP Count per Root & apply change on the fly          #
#    8. Retrieve protocol learned info again and notice the difference with    #
#       previouly retrieved learned info.                                      #
#    9. Configure IPv4 & IPv6 L2-L3 traffic.                                   #
#   10. Retrieve L2-L3 traffic stats.                                          #
#   11. Stop L2-L3 traffic.                                                    #
#   12. Stop all protocols.                                                    #                                                                                
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.50.155
    set ixTclPort   8332
    set ports       {{10.39.43.154 4 1} { 10.39.43.154 4 2}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.30\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure mLDP                            #
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

puts "Add IPv4"
ixNet add $mac1 ipv4
ixNet add $mac2 ipv4
ixNet commit

set ip1 [ixNet getList $mac1 ipv4]
set ip2 [ixNet getList $mac2 ipv4]

set mvAdd1 [ixNet getAttr $ip1 -address]
set mvAdd2 [ixNet getAttr $ip2 -address]
set mvGw1  [ixNet getAttr $ip1 -gatewayIp]
set mvGw2  [ixNet getAttr $ip2 -gatewayIp]

puts "configuring IPv4 addresses"
ixNet setAttr $mvAdd1/singleValue -value "20.20.20.2"
ixNet setAttr $mvAdd2/singleValue -value "20.20.20.1"
ixNet setAttr $mvGw1/singleValue  -value "20.20.20.1"
ixNet setAttr $mvGw2/singleValue  -value "20.20.20.2"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

puts "Adding mLDP over IPv4 stacks"
ixNet add $ip1 ldpBasicRouter
ixNet add $ip2 ldpBasicRouter
ixNet commit

set ldp1 [ixNet getList $ip1 ldpBasicRouter]
set ldp2 [ixNet getList $ip2 ldpBasicRouter]

puts "Enabling P2MP capability for mLDP"
set capability1 [ixNet getAttr $ldp1 -enableP2MPCapability]
set capability2 [ixNet getAttr $ldp2 -enableP2MPCapability]

ixNet setAttr $capability1/singleValue -value true
ixNet setAttr $capability2/singleValue -value true
ixNet commit

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "mLDP Topology 1:Ingress"
ixNet setAttr $topo2  -name "mLDP Topology 2:Egress"

ixNet setAttr $t1dev1 -name "mLDP Topology 1:Ingress Router"
ixNet setAttr $t2dev1 -name "mLDP Topology 2:Egress Router"
ixNet commit

puts "Configuring Root Ranges behind Topology 1"
ixNet setMultiAttribute $ldp1 -rootRangesCountV4 1
ixNet commit

puts "Configuring Leaf Ranges behind Topology 2"
ixNet setMultiAttribute $ldp2 -leafRangesCountV4 1
ixNet commit

puts "Changing Root Address in Root Ranges behind Topology 1"
set rootRange_rootAddrCount [ixNet getAttribute $ldp1/ldpRootRangeV4 -rootAddress]
ixNet setMultiAttribute $rootRange_rootAddrCount/counter -start 15.1.1.1
ixNet commit

puts "Changing Root Address in Leaf Ranges behind Topology 2"
set leafRange_rootAddrCount [ixNet getAttribute $ldp2/ldpLeafRangeV4 -rootAddress]
ixNet setMultiAttribute $leafRange_rootAddrCount/counter -start 15.1.1.1
ixNet commit

puts "Configuring 2 Opaque TLVs for Root Ranges"	
set rootRange_numberOfTLV [ixNet setAttribute $ldp1/ldpRootRangeV4 -numberOfTLVs 2]
ixNet commit
puts "Configuring 2 Opaque TLVs for Leaf Ranges"
set leafRange_numberOfTLV [ixNet setAttribute $ldp2/ldpLeafRangeV4 -numberOfTLVs 2]
ixNet commit

puts "Configuring 2nd Opaque TLV as Type:2 for Root Ranges"
set type_2_1 [ixNet getAttribute $ldp1/ldpRootRangeV4/ldpTLVList:2 -type]
ixNet setMultiAttribute $type_2_1/singleValue -value 2
ixNet commit
puts "Configuring 2nd Opaque TLV as Type:2 for Leaf Ranges"
set type_2_2 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:2 -type]
ixNet setMultiAttribute $type_2_2/singleValue -value 2
ixNet commit

puts "Changing 1st Opaque TLV Value for Root Ranges"
set value_2_1 [ixNet getAttribute $ldp1/ldpRootRangeV4/ldpTLVList:1 -value]
ixNet setMultiAttribute $value_2_1/singleValue -value 00000066
ixNet commit
puts "Changing 1st Opaque TLV Value for Leaf Ranges"
set value_2_2 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:1 -value]
ixNet setMultiAttribute $value_2_2/singleValue -value 00000066
ixNet commit

puts "Changing 2nd Opaque TLV Increment for Root Ranges"
set increment_2_1 [ixNet getAttribute $ldp1/ldpRootRangeV4/ldpTLVList:2 -increment]
ixNet setMultiAttribute $type_2_1/singleValue -value 0000000000000010
ixNet commit
puts "Changing 2nd Opaque TLV Increment for Leaf Ranges"
set increment_2_2 [ixNet getAttribute $ldp2/ldpLeafRangeV4/ldpTLVList:2 -increment]
ixNet setMultiAttribute $type_2_2/singleValue -value 0000000000000010
ixNet commit

puts "Changing IPv4 Group Addresses under Leaf Ranges behind Egress Router"
set groupAddressV4 [ixNet getAttribute $ldp2/ldpLeafRangeV4 -groupAddressV4]
ixNet setMultiAttribute $groupAddressV4/singleValue -value 225.0.1.1
ixNet commit

puts "Changing IPv6 Group Addresses under Leaf Ranges behind Egress Router"
set groupAddressV6 [ixNet getAttribute $ldp2/ldpLeafRangeV4 -groupAddressV6]
ixNet setMultiAttribute $groupAddressV6/singleValue -value ff15:0:1::
ixNet commit

puts "Changing IPv4 Source Addresses under Root Ranges behind Ingress Router"
set sourceAddressV4 [ixNet getAttribute $ldp1/ldpRootRangeV4 -sourceAddressV4]
ixNet setMultiAttribute $sourceAddressV4/singleValue -value 5.1.1.1
ixNet commit

puts "Changing IPv6 Source Addresses under Root Ranges behind Ingress Router"
set sourceAddressV6 [ixNet getAttribute $ldp1/ldpRootRangeV4 -sourceAddressV6]
ixNet setMultiAttribute $sourceAddressV6/singleValue -value 6001:1::1
ixNet commit

puts "Changing Group Addresses count under Leaf Ranges behind Egress Router"
set groupCountPerLsp [ixNet getAttribute $ldp2/ldpLeafRangeV4 -groupCountPerLsp]
ixNet setMultiAttribute $groupCountPerLsp/singleValue -value 5
ixNet commit

################################################################################
# 2. Start LDP protocol and wait for 60 seconds
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
puts "Fetching P2MP FEC Learned Info in Ingress Router on Topology 1"
ixNet exec getP2MPFECLearnedInfo $ldp1 1
after 5000
set linfo [ixNet getList $ldp1 learnedInfo]
ixNet getAttr $linfo -columns
set values [ixNet getAttribute $linfo -values]

puts "***************************************************"
foreach v $values {
        puts $v
}
puts "***************************************************"

################################################################################
# 5. Change the label, number of LSP Count And apply changes On The Fly (OTF). #
################################################################################

puts "Changing LSP Count per root On The Fly behind Egress Router on Topology 2"
set lsp2 [ixNet getAttribute $ldp2/ldpLeafRangeV4 -lspCountPerRoot]
ixNet setMultiAttribute $lsp2/singleValue -value 5

puts "Changing Label value  On The Fly behind Egress Router on Topology 2"
set label [ixNet getAttribute $ldp2/ldpLeafRangeV4 -labelValueStart]
ixNet setMultiAttribute $label/singleValue -value 666
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
puts "Fetching P2MP FEC Learned Info in Ingress Router on Topology 1"
ixNet exec getP2MPFECLearnedInfo $ldp1 1
after 5000
set linfo [ixNet getList $ldp1 learnedInfo]
set values [ixNet getAttribute $linfo -values]
puts "***************************************************"
foreach v $values {
    puts $v
}
puts "***************************************************"

################################################################################
# 7. Configure L2-L3 traffic 
################################################################################
puts "Configuring L2-L3 Traffic Item"
set ldp1 [lindex [ixNet remapIds $ldp1] 0]
set ldp2 [lindex [ixNet remapIds $ldp2] 0]

set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {IPv4 Traffic Item}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv4
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $ldp1/ldpRootRangeV4]

ixNet setMultiAttribute $endpointSet1\
    -name                  "EndpointSet-1"\
    -scalableSources       [list]\
    -multicastReceivers    [list [list $ldp2/ldpLeafRangeV4 0 0 0]]\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               $source\
    -destinations          [list]    
ixNet commit

ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy        [list sourceDestEndpointPair0 trackingenabled0 mplsMplsLabelValue0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]
ixNet commit

set trafficItem2 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem2\
    -name {IPv6 Traffic Item}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv6
ixNet commit

set trafficItem2 [lindex [ixNet remapIds $trafficItem2] 0]
set endpointSet2 [ixNet add $trafficItem2 "endpointSet"]

ixNet setMultiAttribute $endpointSet2\
    -name                  "EndpointSet-2"\
    -scalableSources       [list]\
    -multicastReceivers    [list [list $ldp2/ldpLeafRangeV6 0 0 0]]\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               $source\
    -destinations          [list]    
ixNet commit

ixNet setMultiAttribute $trafficItem2/tracking\
    -trackBy        [list sourceDestEndpointPair0 trackingenabled0 mplsMplsLabelValue0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]
ixNet commit

###############################################################################
# 8. Apply and start L2/L3 traffic
###############################################################################
puts "applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

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
            puts [format "%*s:%*s" -34 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

################################################################################
# 9. Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 10. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
