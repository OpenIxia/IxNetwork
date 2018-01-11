#!/bin/sh
# the next line restarts using tclsh \
exec tclsh "$0" "$@"

################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2012 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    10/16/2012 - Nagendra Prasath - created sample                            #
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
#    This script intends to demonstrate how to use per session controls        #
#    It will create 2 topologyes with ethernet and IPv6 stacks and than it     #
#    will do actions and retrieve status at session level                      #
# Module:                                                                      #
#    The sample was tested on 2 back-to-back XMVDC16 ports                     #
# Software:                                                                    #
#    OS        Linux Fedora Core 12 (32 bit)                                   #
#    IxOS      6.40 EA (6.40.900.4)                                            #
#    IxNetwork 7.0  EA (7.0.801.20)                                            #
#                                                                              #
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

puts "Add 2 Topologies and attach respective vports to it"
ixNet add [ixNet getRoot] topology -name testTpg1 -vports $vport1
ixNet add [ixNet getRoot] topology -name testTpg2 -vports $vport2
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

puts "Add IPv4"
ixNet add $mac1 ipv4 -name testIP1
ixNet add $mac2 ipv4 -name testIP2
ixNet commit

set ip1 [ixNet getList $mac1 ipv4]
set ip2 [ixNet getList $mac2 ipv4]
set ip1Items [ixNet getList $ip1 item]
set ip2Items [ixNet getList $ip2 item]
set ip1item1 [lindex $ip1Items 0]

puts "Setting multi values for ipv4 addresses"
set ip1MultivalueAddr [ixNet getAttr $ip1 -address]
ixNet setMultiAttr $ip1MultivalueAddr/counter       \
    -direction      increment                       \
    -start          22.1.1.1                        \
    -step           0.0.0.2
    
set ip2MultivalueAddr [ixNet getAttr $ip2 -address]    
ixNet setMultiAttr $ip2MultivalueAddr/counter       \
    -direction      increment                       \
    -start          22.1.1.2                        \
    -step           0.0.0.2
    
set ip1MultivalueGw [ixNet getAttr $ip1 -gatewayIp]
ixNet setMultiAttr $ip1MultivalueGw/counter         \
    -direction      increment                       \
    -start          22.1.1.2                        \
    -step           0.0.0.2
    
set ip2MultivalueGw [ixNet getAttr $ip2 -gatewayIp]
ixNet setMultiAttr $ip2MultivalueGw/counter         \
    -direction      increment                       \
    -start          22.1.1.1                        \
    -step           0.0.0.2 
    
ixNet setAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit

set ip1Item1_IP [ixNet getAtt [lindex $ip1Items 0] -address]
set ip2Item1_IP [ixNet getAtt [lindex $ip2Items 0] -address]

puts "Assigning the ports"
::ixTclNet::AssignPorts $::ixia::ports {} $vPorts force

puts "Starting protocols"
ixNet exec startAllProtocols
after 10000

puts "Display address of Item1/IP1"
puts [ixNet getAtt $ip1item1 -address]
puts " "

puts "Display gatewayIp of Item1/IP1"
puts [ixNet getAtt $ip1item1 -gatewayIp]
puts " "

puts "Display resolveGateway of Item1/IP1"
puts [ixNet getAtt $ip1item1 -resolveGateway]
puts " "

puts "Display manualGatewayMac of Item1/IP1"
puts [ixNet getAtt $ip1item1 -manualGatewayMac]
puts " "

puts "Display prefix of Item1/IP1"
puts [ixNet getAtt $ip1item1 -prefix]
puts " "

puts "Abort Item1/IP1 and show its session state"
puts "Session States of items before Abort"
puts [ixNet getAtt $ip1 -sessionStatus]
puts "excuting the abort command"
ixNet exec abort $ip1item1
after 2000
puts "Session States of items after Abort"
puts [ixNet getAtt $ip1 -sessionStatus]
puts " "

puts "Retry Item1/IP1 and show its session state"
puts "Session States of items before Retry"
puts [ixNet getAtt $ip1 -sessionStatus]
puts "restarting $ip1item1"
ixNet exec restartDown $ip1item1
after 2000
puts "Session States of items after Retry"
puts [ixNet getAtt $ip1 -sessionStatus]
puts " "

puts "Stop Item1/IP1 and show its session state"
puts "Session States of items before Stop"
puts [ixNet getAtt $ip1 -sessionStatus]
puts "Stoping $ip1item1"
puts [ixNet exec stop $ip1item1]
after 2000
puts "Session States of items after Stop"
puts [ixNet getAtt $ip1 -sessionStatus]
puts " "

puts "Start Item1/IP1 and show its session state"
puts "Session States of items before Start"
puts [ixNet getAtt $ip1 -sessionStatus]
puts "Starting $ip1item1"
puts [ixNet exec start $ip1item1]
after 2000
puts "Session States of items after Start"
puts [ixNet getAtt $ip1 -sessionStatus]
puts " "

puts "Ping IP2/Item1 from IP1/Item1"
puts [ixNet exec sendPing $ip1item1 $ip2Item1_IP]
puts " "

puts "Send Arp from IP1/Item 1 to IP2/Item 1"
puts [ixNet exec sendArpManual $ip1item1 $ip2Item1_IP]
puts " "

puts "TEST END"

puts ""
puts ""
puts "For more info please refer to the user manual or the built-in help"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/item"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/item]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6/item"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6/item]"

