#!/bin/sh
# the next line restarts using tclsh \
exec tclsh "$0" "$@"

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
#    This script intends to demonstrate how to use NS and Ping                 #
#    it will configure 2 topologyes with IPv6 and than it will send ping       #
#    and NS in between diferent ip adresses.                                   #
# Module:                                                                      #
#    The sample was tested on 2 back-to-back XMVDC16 ports                     #
################################################################################

puts "Load ixNetwork Tcl API package"
package require IxTclNetwork

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.200.115.201                          ;# IP Address of the IxNetwork Tcl Server
    set ixTclPort   8018                                    ;# Port number of the IxNetwork Tcl Server
    set ports       {{10.200.113.3 2 1} {10.200.113.3 2 2}} ;# Chassis-Slot port details {{ChassisIP Slot Port}...}
}

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.0 –setAttribute strict

puts "Create a new config"
ixNet exec newConfig

puts "Add 2 vport"
ixNet add [ixNet getRoot] vport -name testVport1
ixNet add [ixNet getRoot] vport -name testVport2
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vport1 [lindex $vPorts 0]
set vport2 [lindex $vPorts 1]

puts "Add 2 Topologies"
ixNet add [ixNet getRoot] topology -name testTpg1
ixNet add [ixNet getRoot] topology -name testTpg2
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology] 
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

puts "Add 2 device groups with multipliers (number of sessions) as 5"
ixNet add $topo1 deviceGroup -name testDg1 -multiplier 5
ixNet add $topo2 deviceGroup -name testDg2 -multiplier 5
ixNet commit

set dev1 [ixNet getList $topo1 deviceGroup]
set dev2 [ixNet getList $topo2 deviceGroup]

puts "Add MAC"
ixNet add $dev1 ethernet -name testEth1
ixNet add $dev2 ethernet -name testEth2
ixNet commit
set mac1 [ixNet getList $dev1 ethernet]
set mac2 [ixNet getList $dev2 ethernet]

puts "Add IPv6"
ixNet add $mac1 ipv6 -name testIP1
ixNet add $mac2 ipv6 -name testIP2
ixNet commit
set ip1 [ixNet getList $mac1 ipv6]
set ip2 [ixNet getList $mac2 ipv6]
set ip1Items [ixNet getList $ip1/port:1 item]
set ip2Items [ixNet getList $ip2/port:1 item]


puts "Add vports to topologies"
set tPort1 [lindex [ixNet getList $topo1 port] 0]
set tPort2 [lindex [ixNet getList $topo2 port] 0]
ixNet setAttr $topo1 -vports $vport1
ixNet setAttr $topo2 -vports $vport2
ixNet commit


puts "Setting multi values for ipv6 addresses"
set ip1Multi [ixNet getAttr $ip1 -address]
set ip2Multi [ixNet getAttr $ip2 -address]
set ip1MultiGw [ixNet getAttr $ip1 -gatewayIp]
set ip2MultiGw [ixNet getAttr $ip2 -gatewayIp]

ixNet  setMultiAttr $ip1Multi/counter -start 2001:0:0:1:0:0:0:1 -step 0:0:0:0:0:0:0:2 -direction increment
ixNet  setMultiAttr $ip2Multi/counter -start 2001:0:0:1:0:0:0:2 -step 0:0:0:0:0:0:0:2 -direction increment
ixNet  setMultiAttr $ip1MultiGw/counter -start 2001:0:0:1:0:0:0:2 -step 0:0:0:0:0:0:0:2 -direction increment
ixNet  setMultiAttr $ip2MultiGw/counter -start 2001:0:0:1:0:0:0:1 -step 0:0:0:0:0:0:0:2 -direction increment
ixNet  setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet  setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

set ip1Item1_IP [ixNet getAtt [lindex $ip1Items 0] -address]
set ip1Item1_GW [ixNet getAtt [lindex $ip1Items 0] -gatewayIp]
set ip2Item1_IP [ixNet getAtt [lindex $ip2Items 0] -address]
set ip2Item1_GW [ixNet getAtt [lindex $ip2Items 0] -gatewayIp]

puts "Assigning the ports"
::ixTclNet::AssignPorts $::ixia::ports {} $vPorts force

puts "Starting protocols"
ixNet exec startAllProtocols
after 10000

puts "Ping IP1/Item1 Gateway from IP1/Item1"
puts [ixNet exec sendPing [lindex $ip1Items 0] $ip1Item1_GW]

puts "Ping IP2/Item1 from IP1/Item1"
puts [ixNet exec sendPing [lindex $ip1Items 0] $ip2Item1_IP]

puts "Ping IP2/Item1 from all IP1 Items"
puts [ixNet exec sendPing $ip1 $ip2Item1_IP]

puts "Ping a non-existing Item from IP1/Item1"
puts [ixNet exec sendPing [lindex $ip1Items 0] 2220:0:0:1:0:0:0:1]
after 3000

puts "Send Ns from IP1 Item 1"
puts [ixNet exec sendNs [lindex $ip1Items 0]]
after 1000

puts "Send Ns from all IP1 items"
puts [ixNet exec sendNs $ip1]

puts "Send Ns from IP1/Item 1 to IP2/Item 1 IP address"
puts [ixNet exec sendNsManual [lindex $ip1Items 0] $ip2Item1_IP]

puts "Send Ns from IP1/Item 1 to a non-existing IP address"
puts [ixNet exec sendNsManual [lindex $ip1Items 0] 2220:0:0:1:0:0:0:1]

puts "TEST END"

puts ""
puts ""
puts "For more info please refer to the user manual or the built-in help"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6/item"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6/item]"
