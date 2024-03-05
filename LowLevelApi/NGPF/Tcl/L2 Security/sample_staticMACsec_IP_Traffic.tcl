################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA                                             #
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
# Description: 
# 1. Configuring macsec Hardware Based IP Data Traffic.
# 2. Assign ports
# 3. Start all protocols
# 4. Create traffic Item
# 5. Start traffic
# 6. Stop traffic
# 7. Stop all protocols
################################################################################

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork
# Edit this variables values to match your setup
namespace eval ::ixia {
    set ports       {{10.39.50.226 1 5} {10.39.50.226 1 6}}
    set ixTclServer 10.39.50.102
    set ixTclPort   9890
}

################################################################################
# Connect to IxNet client
################################################################################
ixNet connect $ixia::ixTclServer -port  $ixia::ixTclPort -version "9.01"

################################################################################
# Cleaning up IxNetwork
################################################################################
puts "Cleaning up IxNetwork..."
ixNet execute newConfig
puts "Get IxNetwork root object"
set root [ixNet getRoot]
################################################################################
# Adding virtual ports
################################################################################
puts "Adding virtual port 1"
set vport1 [ixNet add $root vport]
ixNet commit
set vport1 [lindex [ixNet remapIds $vport1] 0]
ixNet setAttribute $vport1 -name "10GE LAN - 001"
ixNet commit
puts "Adding virtual port 2"
set vport2 [ixNet add $root vport]
ixNet commit
set vport2 [lindex [ixNet remapIds $vport2] 0]
ixNet setAttribute $vport2 -name "10GE LAN - 002"
ixNet commit
################################################################################
# Adding topology
################################################################################
puts "Adding topology 1"
set topology1 [ixNet add $root "topology"]
ixNet commit
set topology1 [lindex [ixNet remapIds $topology1] 0]
ixNet setAttribute $topology1 -name "Topology 1"
ixNet setAttribute $topology1 -vports $vport1
ixNet commit
################################################################################
# Adding device group
################################################################################
puts "Adding device group 1"
set device1 [ixNet add $topology1 "deviceGroup"]
ixNet commit
set device1 [lindex [ixNet remapIds $device1] 0]
ixNet setAttribute $device1 -name "Device Group 1"
ixNet setAttribute $device1 -multiplier "1"
ixNet commit
################################################################################
# Adding Ethernet layer
################################################################################
puts "Adding ethernet 1"
set ethernet1 [ixNet add $device1 "ethernet"]
ixNet commit
set ethernet1 [lindex [ixNet remapIds $ethernet1] 0]
set macMv [ixNet getAttribute $ethernet1 -mac]
ixNet add $macMv "counter"
ixNet setMultiAttribute $macMv/counter\
             -direction "increment"\
             -start     "00:11:01:00:00:01"\
             -step      "00:00:00:00:00:01"

ixNet commit

################################################################################
# Adding Static Macsec layer on Topology 1
################################################################################
puts "Adding Static MACsec 1"
set staticMacsec1 [ixNet add $ethernet1 "staticMacsec"]
ixNet commit
set staticMacsec1 [lindex [ixNet remapIds $staticMacsec1] 0]
set dutMacMv [ixNet getAttribute $staticMacsec1 -dutMac]
ixNet add $dutMacMv "counter"
ixNet setMultiAttribute $dutMacMv/counter\
             -direction "increment"\
             -start     "00:12:01:00:00:01"\
             -step      "00:00:00:00:00:01"

ixNet commit
set dutSciMacMv [ixNet getAttribute $staticMacsec1 -dutSciMac]
ixNet add $dutSciMacMv "counter"
ixNet setMultiAttribute $dutSciMacMv/counter\
             -direction "increment"\
             -start     "00:12:01:00:00:01"\
             -step      "00:00:00:00:00:01"

ixNet commit
set portIdMv [ixNet getAttribute $staticMacsec1 -portId]
ixNet add $portIdMv "counter"
ixNet setMultiAttribute $portIdMv/counter\
             -direction "increment"\
             -start     "10"\
             -step      "1"

ixNet commit
set dutSciPortIdMv [ixNet getAttribute $staticMacsec1 -dutSciPortId]
ixNet add $dutSciPortIdMv "counter"
ixNet setMultiAttribute $dutSciPortIdMv/counter\
             -direction "increment"\
             -start     "10"\
             -step      "1"

ixNet commit
################################################################################
# Adding topology
################################################################################
puts "Adding topology 2"
set topology2 [ixNet add $root "topology"]
ixNet commit
set topology2 [lindex [ixNet remapIds $topology2] 0]
ixNet setAttribute $topology2 -name "Topology 2"
ixNet setAttribute $topology2 -vports $vport2
ixNet commit
################################################################################
# Adding device group
################################################################################
puts "Adding device group 2"
set device2 [ixNet add $topology2 "deviceGroup"]
ixNet commit
set device2 [lindex [ixNet remapIds $device2] 0]
ixNet setAttribute $device2 -name "Device Group 2"
ixNet setAttribute $device2 -multiplier "1"
ixNet commit
################################################################################
# Adding ethernet layer
################################################################################
puts "Adding ethernet 2"
set ethernet2 [ixNet add $device2 "ethernet"]
ixNet commit
set ethernet2 [lindex [ixNet remapIds $ethernet2] 0]
set macMv [ixNet getAttribute $ethernet2 -mac]
ixNet add $macMv "counter"
ixNet setMultiAttribute $macMv/counter\
             -direction "increment"\
             -start     "00:12:01:00:00:01"\
             -step      "00:00:00:00:00:01"

ixNet commit
################################################################################
# Adding Static Macsec layer on Topology 2
################################################################################
puts "Adding Static MACsec 2"
set staticMacsec2 [ixNet add $ethernet2 "staticMacsec"]
ixNet commit
set staticMacsec2 [lindex [ixNet remapIds $staticMacsec2] 0]
set dutMacMv [ixNet getAttribute $staticMacsec2 -dutMac]
ixNet add $dutMacMv "counter"
ixNet setMultiAttribute $dutMacMv/counter\
             -direction "increment"\
             -start     "00:11:01:00:00:01"\
             -step      "00:00:00:00:00:01"

ixNet commit
set dutSciMacMv [ixNet getAttribute $staticMacsec2 -dutSciMac]
ixNet add $dutSciMacMv "counter"
ixNet setMultiAttribute $dutSciMacMv/counter\
             -direction "increment"\
             -start     "00:11:01:00:00:01"\
             -step      "00:00:00:00:00:01"

ixNet commit
set portIdMv [ixNet getAttribute $staticMacsec2 -portId]
ixNet add $portIdMv "counter"
ixNet setMultiAttribute $portIdMv/counter\
             -direction "increment"\
             -start     "10"\
             -step      "1"

ixNet commit
set dutSciPortIdMv [ixNet getAttribute $staticMacsec2 -dutSciPortId]
ixNet add $dutSciPortIdMv "counter"
ixNet setMultiAttribute $dutSciPortIdMv/counter\
             -direction "increment"\
             -start     "10"\
             -step      "1"

ixNet commit
################################################################################
# Creating Traffic for Creating Traffic from Static MACsec1 to Static MACsec2
################################################################################
puts "Creating Traffic from Static MACsec1 to Static MACsec2"

ixNet add [ixNet getRoot]/traffic trafficItem
ixNet commit
set ti1 [lindex [ixNet getList [ixNet getRoot]/traffic trafficItem] 0]
ixNet setMultiAttribute $ti1                			\
        -name                 "Static_Macsec_IP_Traffic"	\
        -trafficType          ipv4          			\
        -allowSelfDestined    False         			\
        -trafficItemType      l2L3          			\
        -mergeDestinations    True          			\
        -egressEnabled        False         			\
        -enabled              True          			\
        -routeMesh            fullMesh      			\
        -transmitMode         interleaved   			\
        -hostsPerNetwork      1
ixNet commit
ixNet setAttribute $ti1 -trafficType ipv4
ixNet commit
ixNet add $ti1 endpointSet              				\
        -sources             $staticMacsec1    		\
        -destinations        $staticMacsec2    				\
        -name                "Static_Macsec_IP_Traffic"  	\
        -sourceFilter        {}         				\
        -destinationFilter   {}
ixNet commit
ixNet setMultiAttribute $ti1/configElement:1/frameSize \
        -type        fixed                             \
        -fixedSize   128
ixNet setMultiAttrs $ti1/configElement:1/frameRate   \
        -type       packetsPerSecond                         \
        -rate       100                                     \

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

ixNet commit

################################################################################
# 2. Assign ports
################################################################################
puts "Assigning the ports"
set vPorts [ixNet getList $root "vport"]
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

puts "Starting all protocols"
################################################################################
# 3. Start all protocols
################################################################################
ixNet execute "startAllProtocols"
puts "Wait for 20 Seconds"
after 20000

################################################################################
# 5. Retrieve protocol statistics. (Static MACsec Per Port)          		   #
################################################################################
puts "Fetching all Static MACsec Per Port Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Static MACsec Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -40 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

################################################################################
# Generate, apply and start traffic
################################################################################
ixNet exec generate $ti1
ixNet exec apply [ixNet getRoot]/traffic
ixNet exec start [ixNet getRoot]/traffic
puts "Sleep 10sec to send all traffic"
after 10000

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

################################################################################
# Stop traffic
################################################################################
ixNet exec stop [ixNet getRoot]/traffic
puts "Sleep 10sec to send all traffic"
after 10000

################################################################################
# 6. Stop all protocols                                                        #
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"