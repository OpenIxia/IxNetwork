#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2013 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    21/06/2013 - Alexandra Apetroaei - created sample                         #
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
#   This script intends to demonstrate how to configure VxLAN with DHCPv6      #
#   Client and DHCPv6 Server. It configures one topology with one Device Group # 
#   with VxLAN and a chained Device Group with the DHCPv6 Client stack         #
#   and a corresponding topology containing one Device Group with VxLAN and a  #
#   chained Device Group with DHCPv6 Server stack.                             #
# Module:                                                                      #
#    The sample was tested on an FlexAP10G16S module.                          #
# Software:                                                                    #
#    IxOS      6.50 EA                                                         #
#    IxNetwork 7.11 EA                                                         #
#                                                                              #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer localhost
    set ixTclPort   8009
    set ports       {{10.205.15.253 1 7} {10.205.15.253 1 8}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.11

puts "Creating a new config"
ixNet exec newConfig

puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vport1 [lindex $vPorts 0]
set vport2 [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

# Rebooting the ports
foreach vp $vPorts {lappend jobs [ixNet -async exec resetPortCpuAndFactoryDefault $vp]}
foreach j $jobs {ixNet isSuccess $j}

after 5000

puts "Add 2 topologies"
ixNet add [ixNet getRoot] topology -vports $vport1
ixNet add [ixNet getRoot] topology -vports $vport2
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

puts "In each topology, add one Device Group and set the multiplier to 2."
ixNet add $topo1 deviceGroup -multiplier 2
ixNet add $topo2 deviceGroup -multiplier 2
ixNet commit

set topo1_DG1 [ixNet getList $topo1 deviceGroup]
set topo2_DG1 [ixNet getList $topo2 deviceGroup]

puts "Add a chained Device Group behind the previously added Device Groups and set the multiplier to 2."
ixNet add $topo1_DG1 deviceGroup -multiplier 2
ixNet add $topo2_DG1 deviceGroup -multiplier 2
ixNet commit

set topo1_chained_DG2 [ixNet getList $topo1_DG1 deviceGroup]
set topo2_chained_DG2 [ixNet getList $topo2_DG1 deviceGroup]

puts "Add ethernet/mac stack layer in each Device Group."
ixNet add $topo1_DG1 ethernet
ixNet add $topo2_DG1 ethernet
ixNet add $topo1_chained_DG2 ethernet
ixNet add $topo2_chained_DG2 ethernet
ixNet commit

set eth1 [ixNet getList $topo1_DG1 ethernet]
set eth2 [ixNet getList $topo2_DG1 ethernet]
set eth3 [ixNet getList $topo1_chained_DG2 ethernet]
set eth4 [ixNet getList $topo2_chained_DG2 ethernet]


puts "Create the VxLAN stack."
puts "First we need to add IP layer because VxLAN is stacked on it."
ixNet add $eth1 ipv4
ixNet add $eth2 ipv4
ixNet commit

set ip1 [ixNet getList $eth1 ipv4]
set ip2 [ixNet getList $eth2 ipv4]

puts "Add VxLAN on top of IPv4 stack."
ixNet add $ip1 vxlan
ixNet add $ip2 vxlan
ixNet commit

set vxlan_DG1 [ixNet getList $ip1 vxlan]
set vxlan_DG2 [ixNet getList $ip2 vxlan]

puts "Create the DHCP stacks in the chained Device Groups."
puts "Add DHCPv6 Client in one chained Device Group and IPv6 and DHCPv6 Server on the other chained Device Group."
ixNet add $eth3 dhcpv6client
ixNet add $eth4 ipv6
ixNet commit

set dhcpC [ixNet getList $eth3 dhcpv6client]
set ipv6S [ixNet getList $eth4 ipv6]
ixNet add $ipv6S dhcpv6server
ixNet commit

puts "Connect the ethernet layer from the chained Device Groups to the corresponding VxLAN stacks."
set connector1 [ixNet getList $eth3 connector]
ixNet setAttribute $connector1 -connectedTo $vxlan_DG1
ixNet commit

set connector2 [ixNet getList $eth4 connector]
ixNet setAttribute $connector2 -connectedTo $vxlan_DG2
ixNet commit


puts "Change the custom ratio between the IPv4 and VxLAN layers to 3."
ixNet setAttribute $vxlan_DG1 -multiplier 3
ixNet setAttribute $vxlan_DG2 -multiplier 3
ixNet commit

puts "Set the IP addresses and the Gateway IP addresses on the VxLAN DGs."
ixNet setMultiAttribute [ixNet getA $ip1 -address]/counter -direction increment -start 10.1.0.1 -step 0.0.0.1
ixNet setMultiAttribute [ixNet getA $ip2 -address]/counter -direction increment -start 10.1.0.100 -step 0.0.0.1

ixNet setMultiAttribute [ixNet getA $ip1 -gatewayIp]/counter -direction increment -start 10.1.0.100 -step 0.0.0.1
ixNet setMultiAttribute [ixNet getA $ip2 -gatewayIp]/counter -direction increment -start 10.1.0.1 -step 0.0.0.1
ixNet commit


puts "Set the VNIs on VxLAN."
ixNet setMultiAttribute [ixNet getA $vxlan_DG1 -vni]/counter -direction increment -start 700 -step 100
ixNet setMultiAttribute [ixNet getA $vxlan_DG2 -vni]/counter -direction increment -start 700 -step 100
ixNet commit


puts "Set the IPv4 Multicast Address on VxLAN."
ixNet setMultiAttribute [ixNet getA $vxlan_DG1 -ipv4_multicast]/counter -direction increment -start 226.0.0.1 -step 0.0.0.10
ixNet setMultiAttribute [ixNet getA $vxlan_DG2 -ipv4_multicast]/counter -direction increment -start 226.0.0.1 -step 0.0.0.10
ixNet commit


puts "Wait 5 sec"
after 5000

puts "Starting the VxLAN stacks."
ixNet exec start $vxlan_DG1
ixNet exec start $vxlan_DG2
puts "Wait 5 sec"
after 5000

puts "Starting DHCP Server chained Device Group."
ixNet exec start $topo2_chained_DG2
puts "Wait 5 sec"
after 5000

puts "Starting DHCP Client chained Device Group."
ixNet exec start $topo1_chained_DG2

puts "Wait 2 minutes"
after 120000


puts "Printing learned info for DHCPv6 Client"
foreach add [ixNet getA $dhcpC -discoveredPrefix] {
	puts $add
}
puts ""


puts "Stopping the clients"
ixNet exec stop $topo1_chained_DG2
after 5000
puts "Stopping the servers"
ixNet exec stop $topo2_chained_DG2
after 1000
puts "Stopping the VxLAN Device Groups."
ixNet exec stop $topo1_DG1
ixNet exec stop $topo2_DG1
after 10000


puts "Unassigning ports..."
ixTclNet::UnassignPorts
puts "Done... Ports are unassigned..."
puts ""

puts "Cleaning up IxNetwork..."
ixNet exec newConfig
ixNet disconnect

puts "Done... IxNetwork session is closed..."
puts ""
puts "!!! TEST DONE !!!"

return 0