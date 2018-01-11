#################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mario Dicu $
#
#    Copyright © 1997 - 2015 by IXIA
#    All Rights Reserved.
#
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample configures 10 VXLAN sessions on each of the two ports         # 
#                                                                              #
################################################################################

namespace eval ::py {
     set ixTclServer 10.212.111.211
     set ixTclPort   8009
     set ports       {{10.212.111.180 3 1} {10.212.111.180 4 1}}
}

################################################################################
# Source the IxNet library
################################################################################

package req IxTclNetwork

################################################################################
# Connect to IxNet client
################################################################################

ixNet connect $::py::ixTclServer -port $::py::ixTclPort -version 7.40

################################################################################
# Cleaning up IxNetwork
################################################################################

puts "Cleaning up IxNetwork..."
ixNet exec newConfig

################################################################################
# Adding ports to configuration
################################################################################

puts "Adding ports to configuration"
set root [ixNet getRoot]
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit
set vPorts [ixNet getList [ixNet getRoot] vport]
set vport1 [lindex $vPorts 0]
set vport2 [lindex $vPorts 1]

################################################################################
# Adding VXLAN Protocol
################################################################################
puts "Add topologies"
ixNet add [ixNet getRoot] topology
ixNet add [ixNet getRoot] topology
ixNet commit

set topo1 [lindex [ixNet getList [ixNet getRoot] topology] 0]
set topo2 [lindex [ixNet getList [ixNet getRoot] topology] 1]

puts "Add ports to topologies"
ixNet setA $topo1 -vports $vport1
ixNet setA $topo2 -vports $vport2
ixNet commit

puts "Add device groups to topologies"
ixNet add $topo1 deviceGroup
ixNet add $topo2 deviceGroup
ixNet commit

set dg1 [ixNet getList $topo1 deviceGroup]
set dg2 [ixNet getList $topo2 deviceGroup]

puts "Add Ethernet stacks to device groups"
ixNet add $dg1 ethernet
ixNet add $dg2 ethernet
ixNet commit

set mac1 [ixNet getList $dg1 ethernet]
set mac2 [ixNet getList $dg2 ethernet]

puts "Add ipv4 stacks to Ethernets"
ixNet add $mac1 ipv4
ixNet add $mac2 ipv4
ixNet commit

set ipv4_1 [ixNet getList $mac1 ipv4]
set ipv4_2 [ixNet getList $mac2 ipv4]

puts "Setting multi values for ipv4 addresses"
ixNet setMultiAttribute [ixNet getAttribute $ipv4_1 -address]/counter -start 22.1.1.1 -step 0.0.1.0
ixNet setMultiAttribute [ixNet getAttribute $ipv4_1 -gatewayIp]/counter -start 22.1.1.2 -step 0.0.1.0
ixNet setMultiAttribute [ixNet getAttribute $ipv4_1 -resolveGateway]/singleValue -value true
ixNet setMultiAttribute [ixNet getAttribute $ipv4_2 -address]/counter -start 22.1.1.2 -step 0.0.1.0
ixNet setMultiAttribute [ixNet getAttribute $ipv4_2 -gatewayIp]/counter -start 22.1.1.1 -step 0.0.1.0
ixNet setMultiAttribute [ixNet getAttribute $ipv4_2 -resolveGateway]/singleValue -value true
ixNet commit

puts "Add VXLAN stacks to IPv4"
ixNet add $ipv4_1 vxlan
ixNet add $ipv4_2 vxlan
ixNet commit

set vxlan_1 [lindex [ixNet getList $ipv4_1 vxlan] 0]
set vxlan_2 [lindex [ixNet getList $ipv4_2 vxlan] 0]

ixNet setMultiAttribute [ixNet getAttribute $vxlan_1 -vni]/counter -start 1100 -step 1
ixNet setMultiAttribute [ixNet getAttribute $vxlan_1 -ipv4_multicast]/counter -start 225.0.0.1 -step 1.0.0.0
ixNet setMultiAttribute [ixNet getAttribute $vxlan_2 -vni]/counter -start 1100 -step 1
ixNet setMultiAttribute [ixNet getAttribute $vxlan_2 -ipv4_multicast]/counter -start 225.0.0.1 -step 1.0.0.0

puts "Add Inner Device Groups to the Outer Device Groups"
ixNet add $dg1 deviceGroup
ixNet add $dg2 deviceGroup
ixNet commit

set dg3 [lindex [ixNet getList $dg1 deviceGroup] 0]
set dg4 [lindex [ixNet getList $dg2 deviceGroup] 0]

puts "Add Ethernet stacks to the inner device groups"
ixNet add $dg3 ethernet
ixNet add $dg4 ethernet
ixNet commit

set mac3 [lindex [ixNet getList $dg3 ethernet] 0]
set mac4 [lindex [ixNet getList $dg4 ethernet] 0]

puts "Add a connector between the Ethernet and VXLAN"
ixNet add $mac3 connector
ixNet add $mac4 connector
ixNet commit

set connector1 [ixNet getList $mac3 connector]
set connector2 [ixNet getList $mac4 connector]

ixNet setAttribute $connector1 -connectedTo $vxlan_1
ixNet setAttribute $connector2 -connectedTo $vxlan_2
ixNet commit

puts "Add IPv4 stacks to inner Ethernets"
ixNet add $mac3 ipv4
ixNet add $mac4 ipv4
ixNet commit

set ipv4_3 [lindex [ixNet getList $mac3 ipv4] 0]
set ipv4_4 [lindex [ixNet getList $mac4 ipv4] 0]

puts "Setting multi values for inner IPv4 addresses"
ixNet setMultiAttribute [ixNet getAttribute $ipv4_3 -address]/counter -start 5.1.1.1 -step 0.0.1.0
ixNet setMultiAttribute [ixNet getAttribute $ipv4_3 -gatewayIp]/counter -start 5.1.1.2 -step 0.0.1.0
ixNet setMultiAttribute [ixNet getAttribute $ipv4_3 -resolveGateway]/singleValue -value true
ixNet setMultiAttribute [ixNet getAttribute $ipv4_4 -address]/counter -start 5.1.1.2 -step 0.0.1.0
ixNet setMultiAttribute [ixNet getAttribute $ipv4_4 -gatewayIp]/counter -start 5.1.1.1 -step 0.0.1.0
ixNet setMultiAttribute [ixNet getAttribute $ipv4_4 -resolveGateway]/singleValue -value true
ixNet commit

################################################################################
# Assign ports 
################################################################################
set vPorts [ixNet getList [ixNet getRoot] vport]
puts "Assigning ports to $vPorts"
::ixTclNet::AssignPorts $py::ports {} $vPorts force

################################################################################
# Start All Protocols
################################################################################
puts "Starting All Protocols"
ixNet exec startAllProtocols
puts "Sleep 30sec for protocols to start"
after 30000
