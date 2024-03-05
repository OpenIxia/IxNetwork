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
#    This script intends to demonstrate how to use NGPF BGP API                #
#    It will create 2 BGP topologies, it will start the emulation and          #
#    than it will retrieve and display few statistics                          #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.43.12
    set ixTclPort   8239
    set ports       {{10.39.50.123 1 7} { 10.39.50.123 1 8}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.40\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# protocol configuration section                                               #
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
ixNet setAttr $mvAdd1/singleValue -value "20::2"
ixNet setAttr $mvAdd2/singleValue -value "20::1"
ixNet setAttr $mvGw1/singleValue  -value "20::1"
ixNet setAttr $mvGw2/singleValue  -value "20::2"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 64
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 64

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

puts "Adding BGP over IPv6 stack"
ixNet add $ip1 bgpIpv6Peer
ixNet add $ip2 bgpIpv6Peer
ixNet commit

set bgp1 [ixNet getList $ip1 bgpIpv6Peer]
set bgp2 [ixNet getList $ip2 bgpIpv6Peer]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "BGP Topology 1"
ixNet setAttr $topo2  -name "BGP Topology 2"

ixNet setAttr $t1dev1 -name "SR-TE Policy Controller"
ixNet setAttr $t2dev1 -name "Head/Tail End Router"
ixNet commit

puts "Setting IPs in BGP DUT IP tab"
ixNet setAttr [ixNet getAttr $bgp1 -dutIp]/singleValue -value "20::1"
ixNet setAttr [ixNet getAttr $bgp2 -dutIp]/singleValue -value "20::2"
ixNet commit

puts "Enabling IPv6 SRTE Policy"
set cap1 [ixNet getAttr $bgp1 -capabilitySRTEPoliciesV6]
set cap2 [ixNet getAttr $bgp2 -capabilitySRTEPoliciesV6]
set sv1 [ixNet getList $cap1 singleValue]
set sv2 [ixNet getList $cap2 singleValue]
ixNet setAttr $sv1 -value true
ixNet setAttr $sv2 -value true
ixNet commit

puts "Enabling IPv6 SR TE Policy Learned Info filter"
set filter1 [ixNet getAttr $bgp1 -filterSRTEPoliciesV6]
set filter2 [ixNet getAttr $bgp2 -filterSRTEPoliciesV6]
set sv1 [ixNet getList $filter1 singleValue]
set sv2 [ixNet getList $filter2 singleValue]
ixNet setAttr $sv1 -value true
ixNet setAttr $sv2 -value true
ixNet commit

puts "**************************************************"
puts "Configuring Controller"
puts "**************************************************"

puts "Setting Number of polisies"
ixNet setAttr $bgp1 -numberSRTEPolicies 1
ixNet commit

puts "Setting Policy Type"
ixNet setAttr [ixNet getAttribute $bgp1/bgpSRTEPoliciesListV6 -policyType]/singleValue -value "ipv6"
ixNet setAttr [ixNet getAttribute $bgp2/bgpSRTEPoliciesListV6 -policyType]/singleValue -value "ipv6"
ixNet commit

puts "Setting IPv6 End Point value"
ixNet setAttr [ixNet getAttribute $bgp1/bgpSRTEPoliciesListV6 -endPointV6]/singleValue -value "30::1"
ixNet commit

puts "Setting color value"
ixNet setAttr [ixNet getAttribute $bgp1/bgpSRTEPoliciesListV6 -policyColor]/singleValue -value "200"
ixNet commit

puts "Setting Number of Segmnet Lists"
ixNet setAttr $bgp1/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6 -numberOfSegmentListV6 2
ixNet commit

puts "Enabling Binding SID"
ixNet setAttr [ixNet getAttribute $bgp1/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6 -enBindingTLV]/singleValue -value "true"
ixNet commit

puts "Setting Binding SID Type"
ixNet setAttr [ixNet getAttribute $bgp1/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6 -bindingSIDType]/singleValue -value "ipv6sid"
ixNet commit

puts "Setting SID value"
ixNet setAttr [ixNet getAttribute $bgp1/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6 -IPv6SID]/singleValue -value "9999::1"
ixNet commit

puts "Setting Number of Segments"
ixNet setAttr $bgp1/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6 -numberOfSegmentsV6 3
ixNet commit

puts "Setting Segment Type"
ixNet setAttr [ixNet getAttribute $bgp1/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6 -segmentType]/singleValue -value "ipv6sid"
ixNet commit

puts "Setting lable value for -IPv6 SID Only- Segment Type"
ixNet setAttr [ixNet getAttribute $bgp1/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6 -ipv6SID]/singleValue -value "abcd:0:0:0:0:0:0:1"
ixNet commit

puts "Adding the NetworkGroup with Routers at back of it"
set prefixpool1  [ixNet exec createDefaultStack $t2devices ipv6PrefixPools]
set networkGroup1 [lindex [ixNet getList $t2devices networkGroup] 0]
ixNet setAttr $networkGroup1 -name "Endpoint Prefix Advertising color"

set ip6pool [ixNet getList $networkGroup1 ipv6PrefixPools]
set bgpV6IPRouteProperty [ixNet getList $ip6pool bgpV6IPRouteProperty]
puts "Setting Network Address"
ixNet setAttr [ixNet getAttr $ip6pool -networkAddress]/singleValue -value "30::1"

puts "Enabling Extended Community"
ixNet setAttr [ixNet getAttribute $bgpV6IPRouteProperty -enableExtendedCommunity]/singleValue -value "true"

puts "Setting Extended Community Type"
ixNet setAttr [ixNet getAttribute $bgpV6IPRouteProperty/bgpExtendedCommunitiesList:1 -type]/singleValue -value "opaque"

puts "Setting Extended Community Sub-Type"
ixNet setAttr [ixNet getAttribute $bgpV6IPRouteProperty/bgpExtendedCommunitiesList:1 -subType]/singleValue -value "color"

puts "Setting Color Value"
ixNet setAttr [ixNet getAttribute $bgpV6IPRouteProperty/bgpExtendedCommunitiesList:1 -colorValue]/singleValue -value "200"
ixNet commit

################################################################################
# Start protocol and check statistics                                          #
################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000
puts "Verifying all the stats\n"
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

puts "Verifying BGP Peer related stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"BGP+ Peer Per Port"/page}
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
# On the fly section                                                           #  
################################################################################
puts "Changing the SID Value on the Fly"
ixNet setAttr [ixNet getAttribute $bgp1/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6 -ipv6SID]/singleValue -value "3333:0:0:0:0:0:0:1"
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology
if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
	puts "$::errorInfo"
}
after 10000

###############################################################################
# print learned info                                                          #
###############################################################################
ixNet exec getbgpSrTeLearnedInfoLearnedInfo $bgp2 1
after 5000

puts "Print Bgp Ipv6 SR-TE Learned Info"
set learnedInfoList [ixNet getList $bgp2 learnedInfo]
set learnedInfo [lindex $learnedInfoList end]
set table [lindex [ixNet getList $learnedInfo table] 1]
set learnedInfoColumnsList [ixNet getAttr $table -columns]
set learnedInfoValuesList [ixNet getAttr $table -values]
puts "***************************************************"
puts $learnedInfoColumnsList 
puts "***************************************************"

puts "***************************************************"
foreach v $learnedInfoValuesList {
    puts $v
}
puts "***************************************************"
after 15000

puts "Stopping all protocols"
ixNet exec stopAllProtocols
puts "*********************************************************************END*************************************************************************"
