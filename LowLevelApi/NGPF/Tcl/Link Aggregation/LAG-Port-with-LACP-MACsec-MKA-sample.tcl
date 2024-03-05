#!/usr/bin/tclsh
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

#################################################################################
#                                                                               #
# Description:                                                                  #
#    This script intends to demonstrate how to use NGPF LAG API.                #
#	 Script uses four ports for demonstration.                                  #
#                                                                               #
#    1. It will create 2 LAGs as RED-LAG & BLUE-LAG with LACP as LAG protocol,  #
#       and  MACsec and MKA as LAG L23 Protocol,each LAG having two member      #
#       ports. It with configure LACP, MKA and MACsec properties and add        # 
#       Topology over the LAG ports with IPv4 devices                           #
#    2. Start All Protocols                                                     #
#    3. Retrieve protocol statistics and LACP per port statistics.              #
#    4. Configure Traffic over the LAG Topologies                               #
#    5. Regenerate,Apply,Start traffic                                          #
#    6. Retrieve Traffic Flow Statistics                                        #
#	 7. Disable Synchronization flag on RED-LAG-port1 in RED-LAG.               # 
#	 8. Retrieve protocol statistics and Traffic Flow Statistics.               #
#	 9. Re-enable Synchronization flag on RED-LAG-port1 in RED-LAG.             # 
#	 10. Retrieve protocol statistics and Traffic Flow Statistics.              #
#	 11. Perform StopPDU on RED-LAG-port1 in RED-LAG.                           # 
#	 12. Retrieve LACP global learned info and Traffic Flow Statistics.         #
#	 13. Perform StartPDU on RED-LAG-port1 in RED-LAG.                          # 
#	 14. Retrieve LACP global learned info and Traffic Flow Statistics.         #
#	 15. Stop Traffic and Stop All protocols.                                   #
#################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"
#procedure to generate drill-down global learned info view for LACP
proc gererateLacpLearnedInfoView { viewName } {
variable currentStatView
	set viewCaption $viewName
	set protocol "LACP"
	set drillDownType "Global Learned Info"
    set root $root
	set statsViewList [ixNet getList $root/statistics view]
	
	# Add a StatsView
	set statistics $root/statistics
    set view [ixNet add $statistics view]
    ixNet setAttribute $view -caption $viewCaption
	ixNet setAttribute $view -type layer23NextGenProtocol
    ixNet setAttribute $view -visible true
	ixNet commit
	set view [ixNet remapIds $view]

	# Set Filters        
    set trackingFilter [ixNet add $view advancedCVFilters]
    ixNet setAttribute $trackingFilter -protocol $protocol
	ixNet commit
	#ixNet getAttr $trackingFilter -availableGroupingOptions        
	ixNet setAttribute $trackingFilter -grouping $drillDownType
	ixNet commit
	set layer23NextGenProtocolFilter $view/layer23NextGenProtocolFilter        
	ixNet setAttribute $layer23NextGenProtocolFilter -advancedCVFilter $trackingFilter
	ixNet commit

	# Enable Stats Columns to be displayed
	set statsList [ixNet getList $view statistic]
	foreach stat $statsList {
		ixNet setAttribute $stat -enabled true
	}
	ixNet commit

	# Enable Statsview
	ixNet setAttribute $view -enabled true
	ixNet commit
}
# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.50.238
    set ixTclPort   5555
    set ports       {{10.36.5.138 1 13} {10.36.5.138 1 14} {10.36.5.138 1 15} {10.36.5.138 1 16} {10.36.5.138 1 17} {10.36.5.138 1 18} {10.36.5.138 1 19} {10.36.5.138 1 20}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 9.20 -setAttributeibute strict

puts "Create a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure LACP as per the description     #
################################################################################ 
puts "Add 4 virtual ports"
set root [ixNet getRoot]
ixNet add $root vport
ixNet add $root vport
ixNet add $root vport
ixNet add $root vport
ixNet add $root vport
ixNet add $root vport
ixNet add $root vport
ixNet add $root vport
ixNet commit

set vPorts [ixNet getList $root vport]
set vportTx1 [lindex $vPorts 0]
set vportTx2 [lindex $vPorts 1]
set vportTx3 [lindex $vPorts 2]
set vportTx4 [lindex $vPorts 3]
set vportRx1 [lindex $vPorts 4]
set vportRx2 [lindex $vPorts 5]
set vportRx1 [lindex $vPorts 6]
set vportRx2 [lindex $vPorts 7]
set vportListLAG1 [list $vportTx1 $vportTx2 $vportTx3 $vportTx4]
set vportListLAG2 [list $vportRx1 $vportRx2 $vportRx3 $vportRx4]


puts "Assign physical ports to virtual ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

# ADD LAG-1 named RED-LAG
set lag1 [ixNet add $root lag]
ixNet commit
ixNet setMultiAttr $lag1 -name "RED-LAG" -vports $vportListLAG1
ixNet commit

# ADD LAG-2 named BLUE-LAG
set lag2 [ixNet add $root lag]
ixNet commit
ixNet setMultiAttr $lag2 -name "BLUE-LAG" -vports $vportListLAG2
ixNet commit


# Add LACP in RED-LAG
set lag1Stack [ixNet add $lag1 protocolStack]
ixNet setMultiAttribute $lag1Stack -name "LAG1-stack"
ixNet commit

# Add Ethernet Layer in RED-LAG
set lag1eth [ixNet add $lag1Stack "ethernet"]
ixNet setMultiAttribute $lag1eth -stackedLayers [list ] -name "Ethernet-RED-LAG"
ixNet commit
# Add LAG Protocol - LACP on top of LAG-ethernet in RED-LAG
set lag1lacp [ixNet add $lag1eth "lagportlacp"]
ixNet setMultiAttribute $lag1lacp -stackedLayers [list ] -name "LACP-RED-LAG"
ixNet commit

# Add LAG L23 Protocol - MACsec on top of LAG-ethernet in RED-LAG
set lag1macsec [ixNet add $lag1eth "macsec"]
ixNet commit

# Add LAG L23 Protocol - MKA on top of LAG-ethernet in RED-LAG
set lag1mka [ixNet add $lag1eth "mka"]
ixNet commit

# Add LACP in BLUE-LAG
set lag2Stack [ixNet add $lag2 protocolStack]
ixNet setMultiAttribute $lag2Stack -name "LAG2-stack"
ixNet commit
# Add Ethernet Layer in BLUE-LAG
set lag2eth [ixNet add $lag2Stack "ethernet"]
ixNet setMultiAttribute $lag1eth -stackedLayers [list ] -name "Ethernet-BLUE-LAG"
ixNet commit

# Add LAG Protocol - LACP on top of LAG-ethernet in BLUE-LAG
set lag2lacp [ixNet add $lag2eth "lagportlacp"]
ixNet setMultiAttribute $lag2lacp -stackedLayers [list ] -name "LACP-BLUE-LAG"
ixNet commit

# Add LAG L23 Protocol - MACsec on top of LAG-ethernet in BLUE-LAG
set lag2macsec [ixNet add $lag2eth "macsec"]
ixNet commit

# Add LAG L23 Protocol - MKA on top of LAG-ethernet in BLUE-LAG
set lag2mka [ixNet add $lag2eth "mka"]
ixNet commit

# configure LACP ActorSystemID and ActorKey to user defined values

puts "Configure LACP ActorSystemID and ActorKey to user defined values"
set RedLAGlacp [lindex $lag1lacp 0]
set BlueLAGlacp [lindex $lag2lacp 0]

set RedLAGlacpActKey [ixNet getAttribute $RedLAGlacp -actorKey]
set BlueLAGlacpActKey [ixNet getAttribute $BlueLAGlacp -actorKey]

set RedLAGlacpSysId [ixNet getAttribute $RedLAGlacp -actorSystemId]
set BlueLAGlacpSysId [ixNet getAttribute $BlueLAGlacp -actorSystemId]

ixNet setMultiAttr $RedLAGlacpActKey -pattern singleValue -clearOverlays False
ixNet setMultiAttr $BlueLAGlacpActKey -pattern singleValue -clearOverlays False
ixNet commit

ixNet setMultiAttr $RedLAGlacpSysId -pattern singleValue -clearOverlays False
ixNet setMultiAttr $BlueLAGlacpSysId -pattern singleValue -clearOverlays False
ixNet commit

ixNet setMultiAttribute $RedLAGlacpActKey/singleValue -value "6677"
ixNet setMultiAttribute $BlueLAGlacpActKey/singleValue -value "8899"
ixNet commit

ixNet setMultiAttribute $RedLAGlacpSysId/singleValue -value "016677"
ixNet setMultiAttribute $BlueLAGlacpSysId/singleValue -value "018899"
ixNet commit

# Configure RED-LAG - LACP - LACPDU periodic Interval = fast (value = 1 sec) & LACPDU Timeout = Short (value = 3 sec)
set RedLAGlacp_LacpduPeriodicTimeInterval [ixNet getA $RedLAGlacp -lacpduPeriodicTimeInterval]
ixNet setAttribute $RedLAGlacp_LacpduPeriodicTimeInterval/singleValue -value "fast"
ixNet commit
set RedLAGlacp_LacpduTimeout [ixNet getA $RedLAGlacp -lacpduTimeout]
ixNet setAttribute $RedLAGlacp_LacpduTimeout/singleValue -value "short"
ixNet commit

# Configure BLUE-LAG - LACP - LACPDU periodic Interval = fast (value = 1 sec) & LACPDU Timeout = Short (value = 3 sec)
set BlueLAGlacp_LacpduPeriodicTimeInterval [ixNet getA $BlueLAGlacp -lacpduPeriodicTimeInterval]
ixNet setAttribute $BlueLAGlacp_LacpduPeriodicTimeInterval/singleValue -value "fast"
ixNet commit
set BlueLAGlacp_LacpduTimeout [ixNet getA $BlueLAGlacp -lacpduTimeout]
ixNet setAttribute $BlueLAGlacp_LacpduTimeout/singleValue -value "short"
ixNet commit

# Configure MKA & MACsec properties in RED-LAG
# Set RED-LAG MKA Rekey Mode and Rekey Behaviour
ixNet setAttribute $lag1mka -rekeyMode "timerBased"
ixNet setAttribute $lag1mka -rekeyBehaviour "rekeyContinuous"
ixNet commit

# Set RED-LAG MKA periodic rekey at every 30 sec interval
ixNet setAttribute $lag1mka -periodicRekeyInterval 30
ixNet commit

# Set RED-LAG MKA Key derivation function = AES-CMAC-128  for all ports in RED-LAG 
set lag1mka_keyDerivationFunction [ ixNet getA $lag1mka -keyDerivationFunction]
ixNet setAttribute $lag1mka_keyDerivationFunction/singleValue -value "aescmac128"
ixNet commit

# Set Cipher suite = GCM-AES-XPN-128 in RED-LAG MKA Key Server Attributes for all ports in RED-LAG 
set lag1mka_cipherSuite [ ixNet getA $lag1mka -cipherSuite]
ixNet setAttribute $lag1mka_cipherSuite/singleValue -value "aesxpn128"
ixNet commit 

# Set MKA Key Server Priority = 11 for all ports in RED-LAG , so that these ports act as Key Server
set lag1mka_keyServerPriority [ ixNet getA $lag1mka -keyServerPriority]
ixNet setAttribute $lag1mka_keyServerPriority/singleValue -value 11
ixNet commit 

# Set RED-LAG - MKA MKPDU Hello interval - 2 sec (default)
set lag1mka_helloInterval [ ixNet getA $lag1mka -mkaHelloTime]
ixNet setAttribute $lag1mka_helloInterval/singleValue -value 2000
ixNet commit 

# Configure CAK, CKN values in MKA - PSK Chain , same vales for all ports in RED-LAG
set lag1mka_pskChain [ixNet getL $lag1mka cakCache]
set lag1mka_pskChain_cakName [ixNet getA $lag1mka_pskChain -cakName]
ixNet setAttribute $lag1mka_pskChain_cakName/singleValue -value "11112222"
ixNet commit

set lag1mka_pskChain_cakValue128 [ixNet getA $lag1mka_pskChain -cakValue128]
ixNet setAttribute $lag1mka_pskChain_cakValue128/singleValue -value "00000000000000000000000011112222"
ixNet commit

# Configure MKA & MACsec properties in BLUE-LAG
# Set BLUE-LAG MKA Key derivation function = AES-CMAC-128  for all ports in BLUE-LAG 
set lag2mka_keyDerivationFunction [ ixNet getA $lag2mka -keyDerivationFunction]
ixNet setAttribute $lag2mka_keyDerivationFunction/singleValue -value "aescmac128"
ixNet commit

# Set Cipher suite = GCM-AES-XPN-128 in BLUE-LAG MKA Key Server Attributes for all ports in BLUE-LAG 
set lag2mka_cipherSuite [ ixNet getA $lag2mka -cipherSuite]
ixNet setAttribute $lag2mka_cipherSuite/singleValue -value "aesxpn128"
ixNet commit 

# Set BLUE-LAG - MKA MKPDU Hello interval - 2 sec (default)
set lag2mka_helloInterval [ ixNet getA $lag2mka -mkaHelloTime]
ixNet setAttribute $lag2mka_helloInterval/singleValue -value 2000
ixNet commit 

# Configure CAK, CKN values in MKA - PSK Chain , same vales for all ports in BLUE-LAG
set lag2mka_pskChain [ixNet getL $lag2mka cakCache]
set lag2mka_pskChain_cakName [ixNet getA $lag2mka_pskChain -cakName]
ixNet setAttribute $lag2mka_pskChain_cakName/singleValue -value "11112222"
ixNet commit

set lag2mka_pskChain_cakValue128 [ixNet getA $lag2mka_pskChain -cakValue128]
ixNet setAttribute $lag2mka_pskChain_cakValue128/singleValue -value "00000000000000000000000011112222"
ixNet commit


# Configure Topology and Device Group with Protocol stack over LAG ports
################################################################################
# Add topology over RED-LAG
################################################################################
puts "Add Topology over RED-LAG"
set topology1 [ixNet add $root "topology"]
ixNet commit
set topology1 [lindex [ixNet remapIds $topology1] 0]
ixNet setAttribute $topology1 -name "Topology-RED-LAG"
ixNet setAttribute $topology1 -ports $lag1
ixNet commit
################################################################################
# Add Device Group in Topoloy 1
################################################################################
puts "Add Device Group in Topology-RED-LAG"
set device1 [ixNet add $topology1 "deviceGroup"]
ixNet commit
set device1 [lindex [ixNet remapIds $device1] 0]
ixNet setAttribute $device1 -name "DeviceGroup-RED-LAG"
ixNet setAttribute $device1 -multiplier "20"
ixNet commit
################################################################################
# Add Ethernet in Device Group 1
################################################################################
puts "Add Ethernet 1"
set ethernet1 [ixNet add $device1 "ethernet"]
ixNet commit
set ethernet1 [lindex [ixNet remapIds $ethernet1] 0]


################################################################################
# Add topology over BLUE-LAG
################################################################################
puts "Add topology over BLUE-LAG"
set topology2 [ixNet add $root "topology"]
ixNet commit
set topology2 [lindex [ixNet remapIds $topology2] 0]
ixNet setAttribute $topology2 -name "Topology-BLUE-LAG"
ixNet setAttribute $topology2 -ports $lag2
ixNet commit

################################################################################
# Add Device Group in Topoloy 2
################################################################################
puts "Add Device Group in Topology-BLUE-LAG"
set device2 [ixNet add $topology2 "deviceGroup"]
ixNet commit
set device2 [lindex [ixNet remapIds $device2] 0]
ixNet setAttribute $device2 -name "DeviceGroup-BLUE-LAG"
ixNet setAttribute $device2 -multiplier "20"
ixNet commit
################################################################################
# Add Ethernet in Device Group 2
################################################################################
puts "Add Ethernet 2"
set ethernet2 [ixNet add $device2 "ethernet"]
ixNet commit
set ethernet2 [lindex [ixNet remapIds $ethernet2] 0]


################################################################################
# Add IPv4 on top of Ethernet in Topology-RED-LAG & Topology-BLUE-LAG
################################################################################
puts "Add IPv4 on top of Ethernet in Topology-RED-LAG"
ixNet add $ethernet1 ipv4
ixNet add $ethernet2 ipv4
ixNet commit

set ip1 [ixNet getList $ethernet1 ipv4]
set ip2 [ixNet getList $ethernet2 ipv4]

set mvAdd1 [ixNet getAttribute $ip1 -address]
set mvAdd2 [ixNet getAttribute $ip2 -address]
set mvGw1  [ixNet getAttribute $ip1 -gatewayIp]
set mvGw2  [ixNet getAttribute $ip2 -gatewayIp]

puts "configuring ipv4 addresses and gateway"
ixNet setMultiAttribute $mvAdd1/counter -direction "increment" -start "20.20.1.1" -step "0.0.1.0"
ixNet setMultiAttribute $mvAdd2/counter -direction "increment" -start "20.20.2.1" -step "0.0.1.0"
ixNet setMultiAttribute $mvGw1/counter -direction "increment" -start "20.20.2.1" -step "0.0.1.0"
ixNet setMultiAttribute $mvGw2/counter -direction "increment" -start "20.20.1.1" -step "0.0.1.0"

ixNet commit

################################################################################
# Start All protocols and wait for 30 seconds                               #
################################################################################
puts "\nStarting All protocols and waiting for 30 seconds for sessions to come up"
ixNet exec startAllProtocols
after 30000

################################################################################
# 3. Retrieve protocol statistics and LACP per port statistics                 #
################################################################################
puts "\nFetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Protocols Summary"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
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
puts "\nFetching all LACP per-port statistics\n"
set viewPage {::ixNet::OBJ-/statistics/view:"LACP Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
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

################################################################################
# Create L3 Traffic over IPv4 end points from Device Group 1 to Device Group 2
# FrameSize - Icnrement - 128B to 1518B
# Framerate - 25% Line rate
# Flow tracking - IPv4 destination address
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
        -incrementFrom   128									\
		-incrementTo  1518
ixNet setMultiAttribute $trafficItem1/configElement:1/frameRate   \
        -rate       25                                    

ixNet setMultiAttribute $trafficItem1/tracking -trackBy ipv4DestIp0 
ixNet commit
after 5000

################################################################################
# Generate, apply and start traffic
################################################################################
ixNet exec generate $trafficItem1
ixNet exec apply [ixNet getRoot]/traffic
ixNet exec start [ixNet getRoot]/traffic
puts "Run traffic for 30 secs"
after 30000

###############################################################################
# Retrieve L2/L3 Flow statistics
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

puts "\nFetching all MACsec per-port statistics\n"
set viewPage {::ixNet::OBJ-/statistics/view:"MACsec Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
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

################################################################################
# Disable Synchronization flag on port1 in RED-LAG						#
################################################################################
puts "\n\nDisable Synchronization flag on port1 in RED-LAG"
set RedLAGlacpPort1 [lindex [ixNet getList $RedLAGlacp port] 0]
set RedLAGlacpPort1SyncFlag [ixNet getA $RedLAGlacpPort1 -synchronizationFlag]
ixNet setMultiAttr $RedLAGlacpPort1SyncFlag -pattern singleValue -clearOverlays false
ixNet commit
ixNet setMultiAttribute $RedLAGlacpPort1SyncFlag/singleValue -value false
ixNet commit

#Applying changes on the fly
set globals $root/globals
set topology $globals/topology
puts "Applying changes on the fly"
ixNet exec applyOnTheFly $topology

after 10000

################################################################################
# Retrieve protocol statistics and LACP per port statistics                 #
################################################################################
puts "\nFetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Protocols Summary"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
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
puts "\nFetching all LACP per-port statistics\n"
set viewPage {::ixNet::OBJ-/statistics/view:"LACP Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
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

puts "\nFetching all MACsec per-port statistics\n"
set viewPage {::ixNet::OBJ-/statistics/view:"MACsec Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
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

###############################################################################
# Retrieve L2/L3 Flow statistics
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

after 5000
################################################################################
# Re-enable Synchronization flag on port1 in RED-LAG               #
################################################################################
puts "\nRe-enable Synchronization flag on port1 in RED-LAG"
set RedLAGlacpPort1 [lindex [ixNet getList $RedLAGlacp port] 0]
set RedLAGlacpPort1SyncFlag [ixNet getA $RedLAGlacpPort1 -synchronizationFlag]
ixNet setMultiAttr $RedLAGlacpPort1SyncFlag -pattern singleValue -clearOverlays false
ixNet commit
ixNet setMultiAttribute $RedLAGlacpPort1SyncFlag/singleValue -value true
ixNet commit

#Applying changes on the fly
set globals $root/globals
set topology $globals/topology
puts "Applying changes on the fly"
ixNet exec applyOnTheFly $topology

after 5000

################################################################################
# Retrieve protocol statistics and LACP per port statistics                 #
################################################################################
puts "\nFetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Protocols Summary"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
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
puts "\nFetching all LACP per-port statistics\n"
set viewPage {::ixNet::OBJ-/statistics/view:"LACP Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
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

puts "\nFetching all MACsec per-port statistics\n"
set viewPage {::ixNet::OBJ-/statistics/view:"MACsec Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
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

###############################################################################
# Retrieve L2/L3 Flow statistics
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

after 5000

################################################################################
# Perform LACPDU stop on RED-LAG-LACP                                   #
################################################################################
puts "\n\nPerform LACPDU stop on RED-LAG-LACP Port1 "
set RedLAGlacpPort1 [lindex [ixNet getList $RedLAGlacp port] 0]
ixNet exec lacpStopPDU $RedLAGlacpPort1
after 10000

################################################################################
# Retrieve LACP global Learned Info                                         #
################################################################################
puts "\n\n Retrieve LACP global Learned Info"
set viewName "LACP-global-learned-Info-TCLview"
gererateLacpLearnedInfoView $viewName
ixNet exec refresh ::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"
after 10000
puts "\nFetching all Global Learned Info\n"
set viewPage {::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
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

after 5000

# Fetch MACsec Per Port Statistics - MACsec BAD Packet and Invalid ICV Discarded Packet counters can be analysed here
puts "\nFetching all MACsec per-port statistics\n"
set viewPage {::ixNet::OBJ-/statistics/view:"MACsec Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
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

################################################################################
# Perform LACPDU start on RED-LAG-LACP                                         # 
################################################################################
puts "\n\nPerform LACPDU start on RED-LAG-LACP-Port1 "
set RedLAGlacpPort1 [lindex [ixNet getList $RedLAGlacp port] 0]
ixNet exec lacpStartPDU $RedLAGlacpPort1
after 10000

################################################################################
# Retrieve LACP global Learned Info                                            #
################################################################################
ixNet exec refresh ::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"
after 10000
puts "\nFetching all Global Learned Info\n"
set viewPage {::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
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

after 5000
################################################################################
# 12. Stop all protocols                                                       #
################################################################################
puts "Stopping all protocols"
ixNet exec stopAllProtocols
puts "\n\n!!! Test Script Ends !!!"
