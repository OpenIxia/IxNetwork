#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    15/02/2015 - Rupam Paul - created sample                                  #
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
#    This script intends to demonstrate how to use NGPF SR-IPv6-SRH Traffic    #
#    Using Low Level TCL API                                                   #
#   1.It will create 1 IPv6 SR Ext Stack in topology1 and in topology2 will    #
#     contain only ipv6 stack.                                                 #
#	2.Configure the multipliers for IPv6 SR Ext                                #
#	3.Set values of 'Segment List Max Index[n]'                                #
#	4.Disable the checkbox 'Use This Device As Ingress' for the 2nd Tunnel     #
#     in 1st device of IPv6 SR Ext.                                            #
#	5.Set values to 'Segment Left' field for the 2nd tunnel of device 1        #
#	6.Disable the checkbox 'Enable Segment 4' for the 1st Tunnel in 1st        #
#	  device of IPv6 SR Ext                                                    #
#	7.Create IPv6 PrefixPool behind both topologies                            #
#	8.Start All protocol                                                       #
#	9.Create TrafficItem between NetworkGroup1 to NetworkGroup2                #
#  10.Apply and Start Traffic                                                  #
#  11.Print Traffic Flow Statistics                                            #
#  12.Stop Traffic                                                             #
#  13.Stop Protocols	                                                       #
#                                                                              #
# Ixia Software:                                                               #
#    IxOS      8.20 EA                                                         #
#    IxNetwork 8.20 EA                                                         #
#                                                                              #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.216.104.58
    set ixTclPort   5555
    set ports       {{10.216.108.130 12 3} { 10.216.108.130 12 4}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.20\
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
ixNet setAttr $mvAdd1/singleValue -value "2000:0:0:1:0:0:0:1"
ixNet setAttr $mvAdd2/singleValue -value "2000:0:0:1:0:0:0:101"
ixNet setAttr $mvGw1/singleValue  -value "2000:0:0:1:0:0:0:101"
ixNet setAttr $mvGw2/singleValue  -value "2000:0:0:1:0:0:0:1"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 64
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 64

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

puts "Adding IPv6 SR Ext stack over IPv6 stack for Device Group 1"
ixNet add $ip1 ipv6sr
ixNet commit
set ipv6sr [ixNet getList $ip1 ipv6sr]

puts "Configuring the multipliers for IPv6 SR Ext"
ixNet setAttr $ipv6sr -multiplier 2
ixNet commit

puts "Set values to Segment List Max Index"
ixNet setAttr $ipv6sr -numberSegments 5
ixNet commit

puts "Disabling the checkbox 'Use This Device As Ingress' for the 2nd Tunnel in 1st device of IPv6 SR Ext"
set mv [ixNet getAttr $ipv6sr -useAsIngress]
set overlay [ixNet add $mv "overlay"]        
ixNet setMultiA $overlay \
-count 1 \
-index 2 \
-indexStep 0 \
-valueStep false \
-value false
ixNet commit

puts "Setting values to 'Segment Left' field for the 2nd tunnel of device 1"
set segmentsLeft [ixNet getAttr $ipv6sr -segmentsLeft]
set overlay [ixNet add $segmentsLeft "overlay"]        
ixNet setMultiA $overlay \
-count 1 \
-index 2 \
-indexStep 0 \
-valueStep 3 \
-value 3
ixNet commit


puts "Disabling the checkbox 'Enable Segment 4' for the 1st Tunnel in 1st device of IPv6 SR Ext"
set IPv6SegmentsList [ixNet getList $ipv6sr IPv6SegmentsList]
set enableSegment4 [lindex $IPv6SegmentsList 3]
set sIDEnable [ixNet getAttr $enableSegment4 -sIDEnable]
set overlay [ixNet add $sIDEnable "overlay"]        
ixNet setMultiA $overlay \
-count 1 \
-index 1 \
-indexStep 0 \
-valueStep false \
-value false
ixNet commit

puts "Adding the NetworkGroup with Routers at back of it"
ixNet exec createDefaultStack $t1devices ipv6PrefixPools
ixNet exec createDefaultStack $t2devices ipv6PrefixPools

set networkGroup1 [lindex [ixNet getList $t1devices networkGroup] 0]
set networkGroup2 [lindex [ixNet getList $t2devices networkGroup] 0]

################################################################################
# Start protocol                                                               #
################################################################################

puts "Starting protocols and waiting for 45 seconds for protocols to come up"
ixNet exec startAllProtocols
after 45000

################################################################################
# 14. Configure L2-L3 traffic 
################################################################################

puts "Configuring  L2-L3 IPv6 Traffic Item # "
puts "Configuring traffic item with endpoints src ::ipv6PrefixPools & dst :ipv6PrefixPools "

set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {IPv6_Traffic_Item_1}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv6
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 endpointSet]
set source       [list $networkGroup1/ipv6PrefixPools:1]
set destination  [list $networkGroup2/ipv6PrefixPools:1]

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
    -trackBy        [list sourceDestValuePair0 trackingenabled0 smFlowDescriptor0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]\

ixNet commit

###############################################################################
# 15. Apply and start L2/L3 traffic
###############################################################################
puts "Applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "Starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic
after 10000

###############################################################################
# 16. Retrieve L2/L3 traffic Flow statistics
###############################################################################
puts "Verifying all the L2-L3 traffic flow stats\n"
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
# 17. Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 18. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"