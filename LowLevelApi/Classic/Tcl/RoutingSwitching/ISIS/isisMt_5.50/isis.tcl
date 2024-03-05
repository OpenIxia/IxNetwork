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

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use Classic ISIS-L2/L3 API.     #
#                                                                              #
#    1. Create 2 interfaces with ISIS-L2/L3 enabled, each with 1 ISIS-L2/L3    #
#       router with 2 route-ranges behind one router with 2 routes per route   #
#	range						   	       	                                   #
#    2. Start ISIS L2/L3 protocol.                                             #
#    3. Retrieve ISIS L2/L3 protocol statistics			       	               #
#    4. Retrieve ISIS L2/L3 protocol learned info.                             #
#    5. Configure L2-L3 traffic.                                               #
#    6. Start the L2-L3 traffic.                                               #
#    7. Retrieve L2-L3 traffic stats.                                          #
#    8. Stop L2-L3 traffic.                                                    #
#    9. Stop all protocols.                                                    # 
################################################################################
puts "Load ixNetwork Tcl API package"
package req IxTclNetwork
################################################################################
# Test topology details
################################################################################
# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer  10.216.108.14
    set ixTclPort    8009
    set ports        {{10.216.108.96 10 5} {10.216.108.96 10 6}}
}
set version    7.51
################################################################################

################################################################################
#	1. Create 2 interfaces with ISIS-L2/L3 enabled, each with 1 ISIS-L2/L3 #
#       router with 2 route-ranges behind one router with 2 routes per route   #
#       range								       #
################################################################################

puts "Connecting to client $::ixia::ixTclServer "
ixNet connect $::ixia::ixTclServer -version $version -port $::ixia::ixTclPort

puts "Clenaing up the IxNetwork GUI"
ixNet exec newConfig

set r [ixNet getRoot]

################################################################################
# Configure vport1
################################################################################

puts "Add  virtual port vport1"
set vport1 [ixNet add $r vport] 
ixNet setMultiAttribute $vport1 -type ethernetvm -rxMode CaptureAndMeasure
ixNet commit
set vport1 [lindex [ixNet remapId $vport1] 0]

puts "Add  IPv4 interface for vport1"
set int1 [ixNet add $vport1 interface]
ixNet setMultiAttribute $int1 -enabled true
ixNet commit
set int1 [lindex [ixNet remapid $int1] 0]

puts "Assign interface IPv4 address for vport1 and set default gateway IPv4 address"
set ip1 [ixNet add $int1 ipv4]
ixNet setMultiAttribue $ip1 -gateway 1.1.1.2 -ip 1.1.1.1
ixNet commit
set ip1 [lindex [ixNet remapId $ip1] 0]

################################################################################
# Configure vport2
################################################################################

puts "Add  virtual port vport2"
set vport2 [ixNet add $r vport] 
ixNet setMultiAttribute $vport2 -type ethernetvm -rxMode CaptureAndMeasure
ixNet commit
set vport2 [lindex [ixNet remapId $vport2] 0]

puts "Add  IPv4 interface for vport2"
set int2 [ixNet add $vport2 interface]
ixNet setMultiAttribute $int2 -enabled true
ixNet commit
set int2 [lindex [ixNet remapid $int2] 0]

puts "Assign interface IPv4 address for vport2 and set default gateway IPv4 address"
set ip2 [ixNet add $int2 ipv4]
ixNet setMultiAttribute $ip2 -gateway 1.1.1.1 -ip 1.1.1.2
ixNet commit
set ip2 [lindex [ixNet remapId $ip2] 0]

puts "Wait for 5 seconds"
after 5000

set vportlist [list $vport1 $vport2]

puts "Assign the real ports"
::ixTclNet::AssignPorts $::ixia::ports {} $vportlist force

################################################################################
# Enable ISIS L2/L3 on ports
################################################################################

puts "Enablling ISIS L2/L3 on ports ..."
ixNet setMultiAttribute $vport1/protocols/isis -enabled true  
ixNet setMultiAttribute $vport2/protocols/isis -enabled true  
ixNet commit

################################################################################
# Configure ISIS L2/L3 routers on ports and set appropriate parameters
################################################################################

puts "Configure ISIS L2/L3 routers on ports and set appropriate parameters"
set router1 [ixNet add $vport1/protocols/isis router]
ixNet setMultiAttribute $router1\
	-enableDiscardLearnedLsps false\
	-enabled true\
	-capabilityRouterId 100.1.1.1\
	-systemId 64.00.00.00.00.01\
	-enableHelloPadding false\
	-enableMultiTopology false\
	-enableOverloaded false\
	-enableWideMetric true\
	-maxAreaAddresses 3\
	-teEnable false\
	-teEnable 100.1.1.1

ixNet commit
ixNet router1 [lindex [ixNet remapId $router1] 0]

set router2 [ixNet add $vport2/protocols/isis router]
ixNet setMultiAttribute $router2\
	-enableDiscardLearnedLsps false\
	-enabled true\
	-capabilityRouterId 200.1.1.1\
	-systemId 65.00.00.00.00.01\
	-enableHelloPadding false\
	-enableMultiTopology false\
	-enableOverloaded false\
	-enableWideMetric true\
	-maxAreaAddresses 3\
	-teEnable false\
	-teEnable 200.1.1.1
ixNet commit
ixNet router2 [lindex [ixNet remapId $router2] 0]

##################################################################################
# Configure 2 ISIS L2/L3 Route ranges 10.10.10.0/24 and 20.20.20.0/24 behind vport2
##################################################################################

puts "Configure 2 ISIS L2/L3 Route ranges 10.10.10.0/24 and 20.20.20.0/24 behind vport2"
set routeRange21 [ixNet add $router2 routeRange]
ixNet setMultiAttribute $routeRange21\
	-enabled true\
	-firstRoute 10.10.10.0\
	-numberOfRoutes 2\
	-routeOrigin false\
	-isRedistributed false\
	-maskWidth 24\
	-metric 10
ixNet commit
ixNet routeRange21 [lindex [ixNet remapId $routeRange21] 0]

set routeRange22 [ixNet add $router2 routeRange]
ixNet setMultiAttribute $routeRange22\
	-enabled true\
	-firstRoute 20.20.20.0\
	-numberOfRoutes 2\
	-routeOrigin false\
	-isRedistributed false\
	-maskWidth 24\
	-metric 10
ixNet commit
ixNet routeRange22 [lindex [ixNet remapId $routeRange22] 0]


##################################################################################
# Configure interfaces on ISIS L2/L3 routers
##################################################################################

puts "Configuring interfaces on ISIS L2/L3 routers ..."
set protInt1 [ixNet add $router1 interface]
ixNet setMultiAttribute $protInt1\
	-enabled true\
	-interfaceId $int1\
	-enableConnectedToDut true\
	-networkType pointToPoint
ixNet commit
set protInt1 [lindex [ixNet remapId $protInt1] 0]

set protInt2 [ixNet add $router2 interface]
ixNet setMultiAttribute $protInt2\
	-enabled true\
	-interfaceId $int2\
	-enableConnectedToDut true\
	-networkType pointToPoint
ixNet commit
set protInt2 [lindex [ixNet remapId $protInt2] 0]

################################################################################
#	2. Start ISIS L2/L3 protocol 					       #
################################################################################

puts "Starting ISIS L2/l3 protocols ..."
ixNet exec startAllProtocols

#Wait for sometime ...
puts "Waiting for 30 sec ..."
after 30000

################################################################################
#	3. Retrieve ISIS L2/L3 protocol statistics			       #
################################################################################

puts "Fetching ISIS Aggregated Stats .......\n"
set viewPage {::ixNet::OBJ-/statistics/view:"ISIS Aggregated Statistics"/page}

set protocolStatFetchPage [ixNet getAttr $viewPage -currentPage]
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
puts "***************************************************"
after 5000

################################################################################
#	4. Retrieve ISIS L2/L3 protocol learned info.                          #
################################################################################

# Fetch learned info on port 1 
ixNet exec refreshLearnedInformation $router1

# Wait for 3 sec 
puts "Waiting for 3 sec ..."
after 3000

#Check for Learned info on the Protocol interface behind ISIS router for vport1
puts "Checking learned info ..."
set learnedInfo1 [ixNet getList $router1 learnedInformation]
foreach entry $learnedInfo1 {
     set ipv4prefix [ixNet getList $entry ipv4Prefixes]
     puts "=============$ipv4prefix ================"
     foreach ipv4 $ipv4prefix {
        set ipaddr [ixNet getAttr $ipv4 -ipv4Prefix]
        set age [ixNet getAttr $ipv4 -age]
        set hostName [ixNet getAttr $ipv4 -hostName]
        set learnedVia [ixNet getAttr $ipv4 -learnedVia]
        set lspId [ixNet getAttr $ipv4 -lspId]
        set metric [ixNet getAttr $ipv4 -metric]
        set sequenceNumber [ixNet getAttr $ipv4 -sequenceNumber]
        puts "$ipv4"
        puts "ipaddr  == $ipaddr"
        puts "age == $age"
        puts "hostName == $hostName"
        puts "learnedVia == $learnedVia"
        puts "lspId == $lspId"
	puts "metric == $metric"
        puts "sequenceNumber == $sequenceNumber"
        puts "----------------------------------"
     }
}
puts "***************************************************"

#####################################################################
#	5.Configure L2-L3 traffic.				    #	
#####################################################################

set trafficItem1 [ixNet add [ixNet getRoot]/traffic trafficItem]
ixNet setMultiAttribute $trafficItem1\
      -name "Traffic item ISIS"      \
      -roundRobinPacketOrdering false\
      -trafficType ipv4

ixNet commit

set trafficItem1 [lindex [ixNet remapId $trafficItem1] 0]

set endpointSet1 [ixNet add $trafficItem1 endpointSet]
ixNet commit
set endpointSet1 [lindex [ixNet remapId $endpointSet1] 0]

set trafficSource [list $vport1/protocols]
ixNet commit
set trafficSource [lindex [ixNet remapId $trafficSource] 0]

set trafficDestination $routeRange21
ixNet commit
set trafficDestination [lindex [ixNet remapId $trafficDestination] 0]

ixNet setMultiAttribute $endpointSet1        \
      -name "Endpointset 1"                  \
      -sources [list $trafficSource]         \
      -destinations [list $trafficDestination]

ixNet setMultiAttribute $trafficItem1/tracking -trackBy [list sourceEndpoint0 destEndpoint0]

ixNet commit

puts "Applying L2/L3 traffic ......."
ixNet exec apply [ixNet getRoot]/traffic
after 2000

####################################################################
#	6. Start the L2-L3 traffic.				   #
####################################################################

puts "Starting L2/L3 traffic......."
ixNet exec start [ixNet getRoot]/traffic

# Delay of 20 seconds to get traffic stat 
after 20000

###################################################################
#	7. Retrieve L2-L3 traffic stats.                          #
###################################################################

puts "Fetching L2/L3 traffic Stats .......\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Flow Statistics"/page}
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

###################################################################
#	8. Stop L2-L3 traffic. 					  #
###################################################################

puts "Stopping L2/L3 traffic ......."
ixNet exec stop [ixNet getRoot]/traffic


###################################################################
#	9. Stop all protocols
###################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"





