#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2012 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    11/07/2012 - Alexandru Branciog - created sample                         #
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
#   This script intends to demonstrate how to configure DHCPv4/v6 Client and   #
#   DHCPv4/v6 Server. It configures one topology with one DHCPv4 Client stack  #
#   and one DHCPv6 Client stack and a corresponding topology containing        #
#   DHCPv4/v6 Servers.                                                         #
# Module:                                                                      #
#    The sample was tested on an XMVDC16 module.                               #
# Software:                                                                    #
#    OS        Linux Fedora Core 12 (32 bit)                                   #
#    IxOS      6.40 EA (6.40.900.4)                                            #
#    IxNetwork 7.0  EA (7.0.801.20)                                            #
#                                                                              #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.205.15.67
    set ixTclPort   8102
    set ports       {{10.205.15.73 9 1} {10.205.15.73 9 2}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.0

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

puts "Adding 2 topologies"
ixNet add [ixNet getRoot] topology -vports $vport1
ixNet add [ixNet getRoot] topology -vports $vport2
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

puts "Adding 2 device groups, one for the client, multiplier is set to 15 and one for the server, multiplier is set to 1"
ixNet add $topo1 deviceGroup -multiplier 1
ixNet add $topo2 deviceGroup -multiplier 15
ixNet commit

set t1dev1 [ixNet getList $topo1 deviceGroup]
set t2dev1 [ixNet getList $topo2 deviceGroup]

# naming the topologies and the device groups
ixNet setAttr $topo1  -name "DHCP Topology-1"
ixNet setAttr $topo2  -name "DHCP Topology-2"
ixNet setAttr $t1dev1 -name "Servers"
ixNet setAttr $t2dev1 -name "Clients"
ixNet commit

puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet commit
foreach {mac1 mac2} [ixNet getList $t1dev1 ethernet] {}
set mac3 [ixNet getList $t2dev1 ethernet]

puts "Adding DHCPv4 Server and DHCPv6 Server stacks"
puts "First we need to add IP layer because DHCP server is stacked on it"
ixNet add $mac1 ipv4
ixNet add $mac2 ipv6
ixNet commit
set dhcpv4S [ixNet add [ixNet getList $mac1 ipv4] dhcpv4server]
set dhcpv6S [ixNet add [ixNet getList $mac2 ipv6] dhcpv6server]

puts "Adding DHCpv4 Client and DHCPv6 Client stacks"
ixNet add $mac3 dhcpv4client
ixNet add $mac3 dhcpv6client
ixNet commit

set dhcpv4S [ixNet remapIds $dhcpv4S]
set dhcpv6S [ixNet remapIds $dhcpv6S]

set dhcpv4C [ixNet getL $mac3 dhcpv4client]
set dhcpv6C [ixNet getL $mac3 dhcpv6client]

puts "Setting type to IATA for both v6 client and server"
ixNet setA [ixNet getA $dhcpv6S/dhcp6ServerSessions -iaType]/singleValue -value iata
ixNet setA [ixNet getA $dhcpv6C -dhcp6IaType]/singleValue -value iata

puts "Setting DHCPv6 Server Pool Count and Pool Prefix Count to 15"
ixNet setA [ixNet getA $dhcpv6S/dhcp6ServerSessions -poolSize]/singleValue -value 15
ixNet setA [ixNet getA $dhcpv6S/dhcp6ServerSessions -poolPrefixSize]/singleValue -value 15
puts "Setting DHCPv4 Server Pool Count to 15"
ixNet setA [ixNet getA $dhcpv4S/dhcp4ServerSessions -poolSize]/singleValue -value 15

puts "Setting Start Pool Address for DHCPv4/v6 Servers"
ixNet setA [ixNet getA $dhcpv6S/dhcp6ServerSessions -ipAddress]/counter -start 2000:0:0:1:0:0:1:1
ixNet setA [ixNet getA $dhcpv4S/dhcp4ServerSessions -ipAddress]/counter -start 100.1.1.1
ixNet commit

puts "Wait 5 sec"
after 5000

puts "Starting DHCP Servers"
ixNet exec start $dhcpv4S
ixNet exec start $dhcpv6S
puts "Wait 5 sec"
after 5000

puts "Starting DHCP Clients"
ixNet exec start $t2dev1

puts "Wait 2 minutes"
after 120000

puts "Printing learned info for DHCPv4 Client"
foreach add [ixNet getA $dhcpv4C -discoveredAddresses] {
	puts $add
}

puts "Printing learned info for DHCPv6 Client"
foreach add [ixNet getA $dhcpv6C -discoveredAddresses] {
	puts $add
}
	

puts "Stopping the clients"
ixNet exec stop $t2dev1
after 5000
puts "Stopping the servers"
ixNet exec stop $t1dev1
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