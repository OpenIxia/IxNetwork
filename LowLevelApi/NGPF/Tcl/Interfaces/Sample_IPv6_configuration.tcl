################################################################################
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
#    This sample configures 10 IPv6 sessions on each of the two ports          # 
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
# Adding IPv6 protocol to configuration
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

puts "Add ipv6 stacks to Ethernets"
ixNet add $mac1 ipv6
ixNet add $mac2 ipv6
ixNet commit

set ipv6_1 [lindex [ixNet getList $mac1 ipv6] 0]
set ipv6_2 [lindex [ixNet getList $mac2 ipv6] 0]

puts "Setting multi values for ipv6 addresses"
ixNet setMultiAttr [ixNet getAttr $ipv6_1 -address]/counter -start 2200:0:0:0:0:0:0:1 -step 0:0:0:1:0:0:0:0
ixNet setMultiAttr [ixNet getAttr $ipv6_1 -gatewayIp]/counter -start 2200:0:0:0:0:0:0:2 -step 0:0:0:1:0:0:0:0
ixNet setMultiAttr [ixNet getAttr $ipv6_1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ipv6_1 -prefix]/singleValue -value 64
ixNet setMultiAttr [ixNet getAttr $ipv6_2 -address]/counter -start 2200:0:0:0:0:0:0:2 -step 0:0:0:1:0:0:0:0
ixNet setMultiAttr [ixNet getAttr $ipv6_2 -gatewayIp]/counter -start 2200:0:0:0:0:0:0:1 -step 0:0:0:1:0:0:0:0
ixNet setMultiAttr [ixNet getAttr $ipv6_2 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ipv6_2 -prefix]/singleValue -value 64
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