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
#    This sample configures 10 IPv4 sessions on each of the two ports,         # 
#    and performs the following traffic actions                                #
#    - Creating 2 Traffic Items for IPv4                                       #
#    - Add 2 new Endpoint sets to TI 1 IPv4                                    #
#    - Remove last configured Endpoint set from TI 1 IPv4                      #
#    - Disable TI 1 IPv4                                                       #
#    - Enable TI 1 IPv4                                                        #
#    - Duplicate TI 1 IPv4 3 times                                             #
#    - Remove a Traffic Item copy                                              #
#    - Adding Ingress Tracking for bot Traffic Items                           #
#    - Adding Egress Tracking for both Traffic Items                           #
#    - Adding Latency Bins Tracking for both Traffic Items                     #
#    - Generate Traffic                                                        #
#    - Apply Traffic                                                           #
#    - Start Traffic                                                           #
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
# Defining the create IPv4 Traffic Item function
################################################################################
proc createBasicIPv4TrafficItem { name sourceEP destEP } {
    puts "- creating traffic item: $name"
    ixNet add [ixNet getRoot]/traffic trafficItem
    ixNet commit
    set trafficItem [lindex [ixNet getList [ixNet getRoot]/traffic trafficItem] end]
    ixNet setMultiAttribute $trafficItem        \
            -name                 $name         \
            -trafficType          ipv4          \
            -allowSelfDestined    False         \
            -trafficItemType      l2L3          \
            -mergeDestinations    True          \
            -egressEnabled        False         \
            -srcDestMesh          manyToMany    \
            -enabled              True          \
            -routeMesh            fullMesh      \
            -transmitMode         interleaved   \
            -biDirectional        True          \
            -hostsPerNetwork      1
    ixNet commit
    ixNet setAttribute $trafficItem -trafficType ipv4
    ixNet commit
    ixNet add $trafficItem endpointSet      \
            -sources             $sourceEP  \
            -destinations        $destEP    \
            -name                "ep-set1"  \
            -sourceFilter        {}         \
            -destinationFilter   {}
    ixNet commit
    ixNet setMultiAttribute $trafficItem/configElement:1/frameSize  \
            -type        fixed                                      \
            -fixedSize   128
    ixNet setMultiAttrs $trafficItem/configElement:1/frameRate  \
            -type       percentLineRate                         \
            -rate       2                 
    ixNet setMultiAttrs $trafficItem/configElement:1/transmissionControl \
            -duration               1                                   \
            -iterationCount         1                                   \
            -startDelayUnits        bytes                               \
            -minGapBytes            12                                  \
            -frameCount             10000                               \
            -type                   continuous                          \
            -interBurstGapUnits     nanoseconds                         \
            -interBurstGap          0                                   \
            -enableInterBurstGap    False                               \
            -interStreamGap         0                                   \
            -repeatBurst            1                                   \
            -enableInterStreamGap   False                               \
            -startDelay             0                                   \
            -burstPacketCount       1
    ixNet commit
}

################################################################################
# Defining the Ingress Tracking for Traffic Item set function
################################################################################
proc setIngressTrackingForTI { ti trackingList} {
    set tiName [ixNet getAttribute $ti -name]
    puts "--- Traffic Item: $tiName setting ingress tracking $trackingList "
    ixNet setMultiAttribute $ti/tracking -trackBy $trackingList
    ixNet commit
}

################################################################################
# Defining the Egress Tracking for Traffic Item set function
################################################################################    
proc setFirstEgressTrackingForTI { ti stack field} {
    set tiName [ixNet getAttribute $ti -name]
    puts "--- Traffic Item: $tiName setting eggress tracking to field $field for stack $stack "
    ixNet setAttribute $ti -egressEnabled True
    set et [lindex [ixNet getList $ti egressTracking] 0]
    ixNet setAttribute $et -encapsulation "Any: Use Custom Settings"
    ixNet setAttribute $et -offset "CustomByField"
    ixNet commit
    set stackList [ixNet getList [lindex [ixNet getList $ti egressTracking] 0]/fieldOffset stack]
    foreach mstack $stackList {
        if {[lsearch -regexp -inline $mstack $stack]  != ""} {
            set fieldList [ixNet getList $mstack field]
            foreach mfield $fieldList {
                if {[lsearch -regexp -inline $mfield $field]  != "" } {
                    ixNet setAttribute $mfield -activeFieldChoice True
                    ixNet setAttribute $mfield -trackingEnabled True
                    ixNet setAttribute $mfield -valueType valueList
                    ixNet setAttribute $mfield -valueList {4 6}
                    ixNet commit
                    break
                }
            }
        }
    }
}

################################################################################
# Defining the Latency Bins for Traffic Item set function
################################################################################
proc setLatencyBinsTrackingForTI { ti binNo } {
    set tiName [ixNet getAttribute $ti -name]
    puts "--- Traffic Item: $tiName setting latency bins tracking $binNo"
    set latencyBin [lindex [ixNet getList $ti/tracking latencyBin] 0]
    ixNet setAttribute $latencyBin -enabled True
    ixNet setAttribute $latencyBin -numberOfBins $binNo
    ixNet commit
}

################################################################################
# Defining the Add EndpointSet function
################################################################################
proc addEndpointSet { trafficItem epName sourceEPs destEPs} {
    puts "- adding $epName endpoint set"
    ixNet add $trafficItem endpointSet      \
            -sources             $sourceEPs \
            -destinations        $destEPs   \
            -name                $epName    \
            -sourceFilter        {}         \
            -destinationFilter   {}
    ixNet commit
}

################################################################################
# Defining the Remove EndpointSet function
################################################################################
proc removeEndpointSet {trafficItem epName} {
    puts "- removing $epName endpoint set"
    set eps [ixNet getList $trafficItem endpointSet]
    foreach ep $eps {
        puts $ep
        set mName [ixNet getAttribute $ep -name]
        if { $mName == $epName } {
            ixNet remove $ep
            ixNet commit
            break
        }
    }

}

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
# Configure IPv4 Endpoints to configuration
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

################################################################################
# Create 2 IPv4 Traffic Items
################################################################################
puts "######################"
puts "## Traffic Samples ##"
puts "######################"
puts ''
puts "Creating 2 Traffic Items for IPv4"
createBasicIPv4TrafficItem "TI 1 IPv4" $ipv4_1 $ipv4_2
createBasicIPv4TrafficItem "TI 2 IPv4" $ipv4_2 $ipv4_1

set ti1 [lindex [ixNet getList [ixNet getRoot]/traffic trafficItem] 0]
set ti2 [lindex [ixNet getList [ixNet getRoot]/traffic trafficItem] 1]
puts "Add 2 new Endpoint sets to TI 1 IPv4"
addEndpointSet $ti1 "ep-set2" $ipv4_2 $ipv4_1
addEndpointSet $ti1 "ep-set3" $ipv4_2 $ipv4_1
puts "Remove last configured Endpoint set from TI 1 IPv4"
removeEndpointSet $ti1 "ep-set3"

################################################################################
# Performing the Traffic Actions Samples
################################################################################
puts "Traffic Actions Samples:"
puts "- Disable TI 1 IPv4"
ixNet setAttribute $ti1 -enabled False
ixNet commit
puts "- Enable TI 1 IPv4"
ixNet setAttribute $ti1 -enabled True
ixNet commit
puts "- Duplicate TI 1 IPv4 3 times"
ixNet execute duplicate $ti1 3
puts "- Remove a Traffic Item copy"
set ti_remove [lrange [ixNet getList [ixNet getRoot]/traffic trafficItem] 2 end]
ixNet remove $ti_remove
ixNet commit
puts "- Adding Ingress Tracking for bot Traffic Items"
set trackingList {sourceDestValuePair0}
setIngressTrackingForTI $ti1 $trackingList
setIngressTrackingForTI $ti2 $trackingList
puts "- Adding Egress Tracking for both Traffic Items"
setFirstEgressTrackingForTI $ti1 "ipv4" "ipv4.header.version-1"
setFirstEgressTrackingForTI $ti2 "ipv4" "ipv4.header.version-1"
puts "- Adding Latency Bins Tracking for both Traffic Items"
setLatencyBinsTrackingForTI $ti1 4
setLatencyBinsTrackingForTI $ti2 4
puts "- Generate Traffic"
ixNet execute generate {$ti1 $ti2}
puts "- Apply Traffic"
ixNet execute apply [ixNet getRoot]/traffic
puts "- Start Traffic"
ixNet execute start [ixNet getRoot]/traffic
puts "Sleep 30sec then stop traffic"
after 30000
puts "- Stop Traffic"
ixNet execute stop [ixNet getRoot]/traffic

################################################################################
# Stop All Protocols
################################################################################
puts "Stop All Protocols"
ixNet execute stopAllProtocols
puts "Sleep 30sec for protocols to stop"
after 30000

