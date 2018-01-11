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
#    This sample configures 10 Ethernet sessions on each of the two ports,     # 
#    adds a traffic Item that uses Ethernet endpoints, sends traffic and       #
#    checks the loss using the statistics                                      #
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
# Configuring Ethernet
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

################################################################################
# Configure Ethernet Traffic
################################################################################
puts ''
puts "Creating Traffic for Eth"

ixNet add [ixNet getRoot]/traffic trafficItem
ixNet commit
set ti1 [lindex [ixNet getList [ixNet getRoot]/traffic trafficItem] 0]
ixNet setMultiAttribute $ti1                \
        -name                 "Traffic Eth" \
        -trafficType          ethernetVlan  \
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
ixNet setAttribute $ti1 -trafficType ethernetVlan
ixNet commit
ixNet add $ti1 endpointSet              \
        -sources             $mac1      \
        -destinations        $mac2      \
        -name                "ep-set1"  \
        -sourceFilter        {}         \
        -destinationFilter   {}
ixNet commit
ixNet setMultiAttribute $ti1/configElement:1/frameSize \
        -type        fixed                             \
        -fixedSize   128
ixNet setMultiAttrs $ti1/configElement:1/frameRate   \
        -type       percentLineRate                         \
        -rate       10                                      \

ixNet setMultiAttrs $ti1/configElement:1/transmissionControl \
    -duration               1                                   \
    -iterationCount         1                                   \
    -startDelayUnits        bytes                               \
    -minGapBytes            12                                  \
    -frameCount             10000                               \
    -type                   fixedFrameCount                     \
    -interBurstGapUnits     nanoseconds                         \
    -interBurstGap          0                                   \
    -enableInterBurstGap    False                               \
    -interStreamGap         0                                   \
    -repeatBurst            1                                   \
    -enableInterStreamGap   False                               \
    -startDelay             0                                   \
    -burstPacketCount       1

ixNet setMultiAttribute $ti1/tracking -trackBy {{sourceDestValuePair0}}
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
# Generate, apply and start traffic
################################################################################
ixNet exec generate $ti1
ixNet exec apply [ixNet getRoot]/traffic
ixNet exec start [ixNet getRoot]/traffic
puts "Sleep 30sec to send all traffic"
after 30000

################################################################################
# Checking Stats to see if traffic was sent OK
################################################################################
puts "Checking Stats to check if traffic was sent OK"
puts "Getting the object for view Traffic Item Statistics"
set viewName "Traffic Item Statistics"
set views [ixNet getList [ixNet getRoot]/statistics view]
set viewObj ""
set editedViewName "::ixNet::OBJ-/statistics/view:\"$viewName\""
foreach view $views {
    if {$editedViewName == $view} {
         set viewObj $view
         break
    }
}
puts "Getting the Tx/Rx Frames values"
set txFrames [ixNet execute getColumnValues $viewObj "Tx Frames"]
set rxFrames [ixNet execute getColumnValues $viewObj "Rx Frames"]
foreach txStat $txFrames rxStat $rxFrames {
    set txStatProcessed [lindex [split [lindex [split $txStat {"kString,"}] end] {"\}"}] 0]
    set rxStatProcessed [lindex [split [lindex [split $rxStat {"kString,"}] end] {"\}"}] 0]
    if {$txStatProcessed != $rxStatProcessed} {
        puts "Rx Frames $rxStatProcessed != Tx Frames $txStatProcessed"
        puts "Fail the test"
    } else {
        puts "No loss found: Rx Frames $rxStatProcessed = Tx Frames $txStatProcessed"
    }
}