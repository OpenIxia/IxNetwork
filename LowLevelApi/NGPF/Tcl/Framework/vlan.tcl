#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2012 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    09/07/2012 - Mircea Dan Gheorghe - created sample                         #
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
#    This script intends to demonstrate how to use next gen protocols          #
#    It will create 2 topologyes with ethernet and vlan stacks and than it     #
#    will create and send traffic over them                                    #
# Module:                                                                      #
#    The sample was tested on 2 back-to-back XMVDC16 ports                     #
# Software:                                                                    #
#    OS        Linux Fedora Core 12 (32 bit)                                   #
#    IxOS      6.40 EA (6.40.900.4)                                            #
#    IxNetwork 7.0  EA (7.0.801.20)                                            #
#                                                                              #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.200.115.201                          ;# IP Address of the IxNetwork Tcl Server
    set ixTclPort   8018                                    ;# Port number of the IxNetwork Tcl Server
    set ports       {{10.200.113.3 2 1} {10.200.113.3 2 2}} ;# Chassis-Slot port details {{ChassisIP Slot Port}...}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.0 –setAttribute strict

puts "Create a new config"
ixNet exec newConfig

puts "Add 2 vport"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]
set vportRx [lindex $vPorts 1]

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
ixNet setAttr $t1dev1 -multiplier 5
ixNet setAttr $t2dev1 -multiplier 1
ixNet commit

puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet commit

set mac1 [ixNet getList $t1dev1 ethernet]
set mac2 [ixNet getList $t2dev1 ethernet]

puts "Enabled vlan"
ixNet setAttr $mac1 -vlanCount 1
ixNet setAttr $mac2 -vlanCount 1
ixNet setAttr $mac1 -useVlans true
ixNet setAttr $mac2 -useVlans true
ixNet commit

set vlan1 [ixNet getList $mac1 vlan]
set vlan2 [ixNet getList $mac2 vlan]

puts "Configuring the mac addresses"
ixNet setMultiAttr [ixNet getAttr $mac1 -mac]/counter   \
        -direction  increment                           \
        -start      {18:03:73:C7:6C:B1}                 \
        -step       {00:00:00:00:00:01}
ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue    \
        -value      {18:03:73:C7:6C:01}
ixNet commit

puts "Configure the vlan value"
ixNet setAttr [ixNet getAttr $vlan1 -vlanId]/singleValue -value 180
ixNet setAttr [ixNet getAttr $vlan2 -vlanId]/singleValue -value 180
ixNet commit

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1 -name  "Send Topology"
ixNet setAttr $topo2 -name  "Receive Topology"
ixNet setAttr $t1dev1 -name "Send Device"
ixNet setAttr $t2dev1 -name "Receive Device"
ixNet commit

puts "Creating a traffic item in between the ethernet/mac endpoints"
ixNet add [ixNet getRoot]/traffic trafficItem         \
    -name                     {Ethernet L2 with vlan} \
    -allowSelfDestined        False                   \
    -trafficItemType          l2L3                    \
    -mergeDestinations        False                   \
    -egressEnabled            False                   \
    -srcDestMesh              oneToOne                \
    -enabled                  True                    \
    -routeMesh                oneToOne                \
    -transmitMode             interleaved             \
    -biDirectional            False                   \
    -trafficType              {ethernetVlan}          \
    -hostsPerNetwork          1
ixNet commit

set trItem [ixNet getList [ixNet getRoot]/traffic trafficItem]

ixNet add $trItem endpointSet   \
    -sources            $mac1   \
    -destinations       $mac2   \
    -name               {eps1}  \
    -sourceFilter       {}      \
    -destinationFilter  {}
ixNet commit

ixNet setMultiAttrs $trItem/configElement:1/frameSize   \
    -type       fixed                                   \
    -fixedSize  128

ixNet setMultiAttrs $trItem/configElement:1/frameRate   \
    -type       percentLineRate                         \
    -rate       10                                      \

ixNet setMultiAttrs $trItem/configElement:1/transmissionControl \
    -duration               1                                   \
    -iterationCount         1                                   \
    -startDelayUnits        bytes                               \
    -minGapBytes            12                                  \
    -frameCount             1                                   \
    -type                   fixedIterationCount                 \
    -interBurstGapUnits     nanoseconds                         \
    -interBurstGap          0                                   \
    -enableInterBurstGap    False                               \
    -interStreamGap         0                                   \
    -repeatBurst            1                                   \
    -enableInterStreamGap   False                               \
    -startDelay             0                                   \
    -burstPacketCount       1
ixNet commit

ixNet setMultiAttrs $trItem/tracking                            \
    -trackBy {{sourceDestValuePair0} {ethernetIiEtherType0}}
ixNet commit

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

puts "Starting protocols"
ixNet exec startAllProtocols

puts "TEST END"

puts " "
puts " "
puts "For more info please refer to the user manual or the built-in help"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology"
puts "[ixNet help ::ixNet::OBJ-/topology]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet]"
puts " "
puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/vlan"
puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/vlan]"
