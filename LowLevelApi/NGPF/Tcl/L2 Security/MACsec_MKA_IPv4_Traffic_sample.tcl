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
# 1. Configue MKA and MACSec (HW based)
# 2. Create traffic Item
# 3. Assign ports
# 4. Start all protocols
# 5. Retrieve protocol statistics. (MACsec Per Port)
# 6. Start traffic
# 7. Stop traffic
# 8. Stop all protocols
################################################################################

puts "Load IxNetwork Tcl API package"
package req IxTclNetwork
# Edit this variables values to match user setup
namespace eval ::ixia {
    set ports       {{10.36.74.52 1 21} {10.36.74.52 1 25}}
    set ixTclServer 10.36.67.90
    set ixTclPort   8009
}

################################################################################
# Connect to IxNetwork client
################################################################################
ixNet connect $ixia::ixTclServer -port  $ixia::ixTclPort -version "9.15"

################################################################################
# Clean up IxNetwork
################################################################################
puts "Clean up IxNetwork GUI"
ixNet execute newConfig
puts "Get IxNetwork root object"
set root [ixNet getRoot]
################################################################################
# Add virtual ports
################################################################################
puts "Add virtual port 1"
set vport1 [ixNet add $root vport]
ixNet commit
set vport1 [lindex [ixNet remapIds $vport1] 0]
ixNet setAttribute $vport1 -name "10GE LAN - 001"
ixNet commit
puts "Add virtual port 2"
set vport2 [ixNet add $root vport]
ixNet commit
set vport2 [lindex [ixNet remapIds $vport2] 0]
ixNet setAttribute $vport2 -name "10GE LAN - 002"
ixNet commit

################################################################################
# Add topology
################################################################################
puts "Add Topology 1"
set topology1 [ixNet add $root "topology"]
ixNet commit
set topology1 [lindex [ixNet remapIds $topology1] 0]
ixNet setAttribute $topology1 -name "Topology 1"
ixNet setAttribute $topology1 -vports $vport1
ixNet commit
################################################################################
# Add Device Group in Topoloy 1
################################################################################
puts "Add Device Group 1"
set device1 [ixNet add $topology1 "deviceGroup"]
ixNet commit
set device1 [lindex [ixNet remapIds $device1] 0]
ixNet setAttribute $device1 -name "Device Group 1"
ixNet setAttribute $device1 -multiplier "10"
ixNet commit
################################################################################
# Add Ethernet in Device Group 1
################################################################################
puts "Add Ethernet 1"
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
# Add Macsec on top of Ethernet in Device Group 1
################################################################################
puts "Add MACsec in Device Group 1"
set macsec1 [ixNet add $ethernet1 "macsec"]
ixNet commit
set macsec1 [lindex [ixNet remapIds $macsec1] 0]

################################################################################
# Add MKA in Device Group 1
################################################################################
puts "Add MKA in Device Group 1"
set mka1 [ixNet add $ethernet1 "mka"]
ixNet commit
set mka1 [lindex [ixNet remapIds $mka1] 0]

################################################################################
# Set CipherSiute AES-XPN-128 for all devices in MKA 1
################################################################################
puts "Set CipherSiute AES-XPN-128 for all devices in MKA 1"
set cipherSuite1 [ixNet getAttribute $mka1 -cipherSuite]
set cipherSuite1 [lindex [ixNet remapIds $cipherSuite1] 0]
set cipherSuiteOverlay1 [ixNet add $cipherSuite1 overlay]
set cipherSuiteOverlay1 [lindex [ixNet remapIds $cipherSuiteOverlay1] 0]
for { set loop1 1 } { $loop1 <= 10 } { incr loop1 } {
	ixNet setAttribute $cipherSuiteOverlay1 -index $loop1 -count 1 -value aesxpn128
	ixNet commit
	after 1000
}

################################################################################
# Add topology
################################################################################
puts "Add Topology 2"
set topology2 [ixNet add $root "topology"]
ixNet commit
set topology2 [lindex [ixNet remapIds $topology2] 0]
ixNet setAttribute $topology2 -name "Topology 2"
ixNet setAttribute $topology2 -vports $vport2
ixNet commit

################################################################################
# Add Device Group in Topoloy 2
################################################################################
puts "Add Device Group in Topology 2"
set device2 [ixNet add $topology2 "deviceGroup"]
ixNet commit
set device2 [lindex [ixNet remapIds $device2] 0]
ixNet setAttribute $device2 -name "Device Group 2"
ixNet setAttribute $device2 -multiplier "10"
ixNet commit
################################################################################
# Add Ethernet in Device Group 2
################################################################################
puts "Add Ethernet 2"
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
# Add Macsec on top of Ethernet in Device Group 2
################################################################################
puts "Add MACsec in Device Group 2"
set macsec2 [ixNet add $ethernet2 "macsec"]
ixNet commit
set macsec2 [lindex [ixNet remapIds $macsec2] 0]
ixNet commit

################################################################################
# Add MKA in Device Group 2
################################################################################
puts "Add MKA in Device Group 2"
set mka2 [ixNet add $ethernet2 "mka"]
ixNet commit
set mka1 [lindex [ixNet remapIds $mka2] 0]

################################################################################
# Set CipherSiute AES-XPN-128 for all devices in MKA 2
################################################################################
puts "Set CipherSiute AES-XPN-128 for all devices in MKA 2"
set cipherSuite2 [ixNet getAttribute $mka2 -cipherSuite]
set cipherSuite2 [lindex [ixNet remapIds $cipherSuite2] 0]
set cipherSuiteOverlay2 [ixNet add $cipherSuite2 overlay]
set cipherSuiteOverlay2 [lindex [ixNet remapIds $cipherSuiteOverlay2] 0]
for { set loop1 1 } { $loop1 <= 10 } { incr loop1 } {
	ixNet setAttribute $cipherSuiteOverlay2 -index $loop1 -count 1 -value aesxpn128
	ixNet commit
	after 1000
}

################################################################################
# Add IPv4 on top of MACsec
################################################################################
puts "Add ipv4"
ixNet add $macsec1 ipv4
ixNet add $macsec2 ipv4
ixNet commit

set ip1 [ixNet getList $macsec1 ipv4]
set ip2 [ixNet getList $macsec2 ipv4]

set mvAdd1 [ixNet getAttribute $ip1 -address]
set mvAdd2 [ixNet getAttribute $ip2 -address]
set mvGw1  [ixNet getAttribute $ip1 -gatewayIp]
set mvGw2  [ixNet getAttribute $ip2 -gatewayIp]

puts "configuring ipv4 addresses"
ixNet setMultiAttribute $mvAdd1/counter -direction "increment" -start "20.20.1.1" -step "0.0.1.0"
ixNet setMultiAttribute $mvAdd2/counter -direction "increment" -start "20.20.2.1" -step "0.0.1.0"
ixNet setMultiAttribute $mvGw1/counter -direction "increment" -start "20.20.2.1" -step "0.0.1.0"
ixNet setMultiAttribute $mvGw2/counter -direction "increment" -start "20.20.1.1" -step "0.0.1.0"

ixNet setAttribute [ixNet getAttribute $ip1 -prefix]/singleValue -value 24
ixNet setAttribute [ixNet getAttribute $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttribute $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttribute $ip2 -resolveGateway]/singleValue -value true
ixNet commit

################################################################################
# 2. Create L3 Traffic over IPv4 end points from Device Group 1 to Device Group 2
################################################################################

puts "Create L3 Traffic over IPv4 end points from Device Group 1 to Device Group 2"

ixNet add [ixNet getRoot]/traffic trafficItem
ixNet commit
set trafficItem1 [lindex [ixNet getList [ixNet getRoot]/traffic trafficItem] 0]
ixNet setMultiAttribute $trafficItem1                			\
        -name                 "Macsec_IPv4_L3_Traffic"	\
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
ixNet setAttribute $trafficItem1 -trafficType ipv4
ixNet commit

ixNet add $trafficItem1 endpointSet              				\
        -sources             $ip1    		\
        -destinations        $ip2    				\
        -name                "Macsec_IPv4_L3_Traffic"  	\
        -sourceFilter        {}         				\
        -destinationFilter   {}
ixNet commit

ixNet setMultiAttribute $trafficItem1/configElement:1/frameSize \
        -type        increment                             \
        -incrementFrom   72									\
		-incrementTo  1518
ixNet setMultiAttribute $trafficItem1/configElement:1/frameRate   \
        -rate       100                                     

ixNet setMultiAttribute $trafficItem1/configElement:1/transmissionControl \
    -duration               1                                   \
    -iterationCount         1                                   \
    -startDelayUnits        bytes                               \
    -minGapBytes            12                                  \
    -frameCount             10000000000                         \
    -type                   fixedFrameCount                     \
    -interBurstGapUnits     nanoseconds                         \
    -interBurstGap          0                                   \
    -enableInterBurstGap    False                               \
    -interStreamGap         0                                   \
    -repeatBurst            1                                   \
    -enableInterStreamGap   False                               \
    -startDelay             0                                   \
    -burstPacketCount       1

ixNet setMultiAttribute $trafficItem1/tracking -trackBy ipv4DestIp0 
ixNet commit

################################################################################
# 3. Assign ports
################################################################################
puts "Assign real ports to both Topology"
set vPorts [ixNet getList $root "vport"]
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

################################################################################
# 4. Start all protocols
################################################################################
puts "Start all protocols"
ixNet execute "startAllProtocols"
puts "Wait for 30 Seconds"
after 30000

################################################################################
# 5. Retrieve protocol statistics. (MACsec Per Port)          		  		   #
################################################################################
puts "Fetch MACsec Per Port Statistics\n"
set viewPage {::ixNet::OBJ-/statistics/view:"MACsec Per Port"/page}
set statcap [ixNet getAttribute $viewPage -columnCaptions]
foreach statValList [ixNet getAttribute $viewPage -rowValues] {
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
# 6. Generate, apply and start traffic
################################################################################
ixNet exec generate $trafficItem1
ixNet exec apply [ixNet getRoot]/traffic
ixNet exec start [ixNet getRoot]/traffic
puts "Run traffic for 30 secs"
after 30000

###############################################################################
# 12. Retrieve L2/L3 Flow statistics
###############################################################################
puts "VRetrieve L2/L3 Flow statistics\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Flow Statistics"/page}
set statcap [ixNet getAttribute $viewPage -columnCaptions]
foreach statValList [ixNet getAttribute $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

################################################################################
# 7. Stop traffic
################################################################################
ixNet exec stop [ixNet getRoot]/traffic

################################################################################
# 8. Stop all protocols                                                        #
################################################################################
ixNet exec stopAllProtocols
puts "Test Script ends"