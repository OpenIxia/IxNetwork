#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2013 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    21/06/2013 - Dragos Cotoc - created sample                                #
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
#  This script intends to demonstrate how to configure PPPv6 Server and Client #
#  with DHCPv6 Server and Client. It configures one topology with one Device   # 
#  Group with the DHCPv6 Server stack over the PPPv6 Server stack and a        #	
#  corresponding topology containing one Device Group with DHCPv6 Client stack # 
#  over PPPv6 Client stack.                                                    #
# Module:                                                                      #
#    The sample was tested on an 10GE LSM XM8S module.                         #
# Software:                                                                    #
#    IxOS      6.50 EA                                                         #
#    IxNetwork 7.11 EA                                                         #
#                                                                              #
################################################################################

# this variables values needs to be edited in order to match your setup
namespace eval ::ixia {
    set ixTclServer localhost
    set ixTclPort   8009
    set ports       {{10.205.15.88 2 1} {10.205.15.88 2 2}}
}

puts "Load ixNetwork Tcl API package."
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.11

puts "Creating a new config."
ixNet exec newConfig

puts "Adding 2 vports."
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vport1 [lindex $vPorts 0]
set vport2 [lindex $vPorts 1]

puts "Assigning the ports."
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

puts "Rebooting the ports."
foreach vp $vPorts {lappend jobs [ixNet -async exec resetPortCpuAndFactoryDefault $vp]}
foreach j $jobs {ixNet isSuccess $j}

puts "Wait 5 sec"
after 5000

puts "Add 2 topologies."
ixNet add [ixNet getRoot] topology -vports $vport1 -name {Server Topology}
ixNet add [ixNet getRoot] topology -vports $vport2 -name {Client Topology}
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topology1 [lindex $topologies 0]
set topology2 [lindex $topologies 1]

puts "In each topology, add one Device Group and set the multiplier to 10 in Device Group 2."
ixNet add $topology1 deviceGroup
ixNet add $topology2 deviceGroup -multiplier 10
ixNet commit

set deviceGroup1 [ixNet getList $topology1 deviceGroup]
set deviceGroup2 [ixNet getList $topology2 deviceGroup]

puts "Add ethernet/mac stack layer in each Device Group."
ixNet add $deviceGroup1 ethernet
ixNet add $deviceGroup2 ethernet
ixNet commit

set ethernet1 [ixNet getList $deviceGroup1 ethernet]
set ethernet2 [ixNet getList $deviceGroup2 ethernet]

puts "Create the DHCPv6oPPPv6 stack."
puts "First we need to add PPPv6 layer because DHCPv6 is stacked on it."
ixNet add $ethernet1 pppoxserver
ixNet add $ethernet2 pppoxclient
ixNet commit

set pppoxServer [ixNet getList $ethernet1 pppoxserver]
set pppoxClient [ixNet getList $ethernet2 pppoxclient]

puts "Setting the NCP Type on the PPP to IPv6."
set multiValueNCPTypeServer [ixNet getA $pppoxServer -ncpType]
set multiValueNCPTypeClient [ixNet getA $pppoxClient -ncpType]

set patternSingleValueServer [ixNet setA $multiValueNCPTypeServer -pattern singleValue]
set patternSingleValueClient [ixNet setA $multiValueNCPTypeServer -pattern singleValue]
ixNet commit

ixNet setMultiAttribute [ixNet getA $pppoxServer -ncpType]/singleValue -value ipv6
ixNet setMultiAttribute [ixNet getA $pppoxClient -ncpType]/singleValue -value ipv6
ixNet commit

puts "Setting the Number of Sessions per Device on the PPP Server to 10."
set sessionsCount [ixNet setA $pppoxServer -sessionsCount 10]
ixNet commit

puts "Add DHCPv6 on top of PPPv6 stack."
ixNet add $pppoxServer dhcpv6server
ixNet add $pppoxClient dhcpv6client
ixNet commit

set dhcpv6Server [ixNet getList $pppoxServer dhcpv6server]
set dhcpv6Client [ixNet getList $pppoxClient dhcpv6client]

puts "Wait 5 sec"
after 5000

puts "Starting the Server Topology."
ixNet exec start $topology1
puts "Wait 10 sec"
after 10000

puts "Starting the Client Topology."
ixNet exec start $topology2
puts "Wait 15 sec"
after 15000

puts "Printing learned info for DHCPv6 Client."
foreach add [ixNet getA $dhcpv6Client -discoveredPrefix] {
	puts $add
}
puts ""

puts "Printing learned info for PPPv6 Client."
foreach add [ixNet getA $pppoxClient -discoveredIpv6Addresses] {
	puts $add
}
puts ""

puts "Stopping the clients"
ixNet exec stop $topology2
after 10000

puts "Stopping the servers"
ixNet exec stop $topology1
after 1000

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

