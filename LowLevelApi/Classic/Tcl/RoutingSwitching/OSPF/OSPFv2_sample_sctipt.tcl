#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    19/01/2015 - Sumit Deb - created sample                                #
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
# Ixia does not gurantee (i) that the functions contained in the script will   #
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
#    This script intends to demonstrate how to use NGPF OSPFv2 API.            #
#                                                                              #
#    1. Create 2 interfaces with OSPFv2 enabled, each having 1 OSPFv2          #
#       router with 10 route-ranges per router with first 5 enabled			   #
#    2. Start the ospfv2 protocol.                                             #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Enable remaining route-ranges on each OSPFv2 router                    #
#    6. Disable and enable router interfaces to reflect changes                # 
#    7. Retrieve protocol learned info.                                        #                                     
#    8. Configure L2-L3 traffic.                                               #
#    9. Start the L2-L3 traffic.                                               #
#    10. Retrieve L2-L3 traffic stats.                                         #
#    11. Stop L2-L3 traffic.                                                   #
#    12. Stop all protocols.                                                   #       #                                                                              #              
# Ixia Softwares:                                                              #
#    IxOS      6.80 EA (6.80.1100.7)                                           #
#    IxNetwork 7.40 EA (7.40.929.15)                                           #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.205.27.23
    set ixTclPort   8009
    set ports       {{ixin-asd-2 2 1} {ixin-asd-2 2 2}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.40\
    –setAttribute strict

puts "Create a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure OSPFv2 as per the description
#    give above
################################################################################ 
puts "Add 2 virtual ports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vPort1 [lindex $vPorts 0]
set vPort2 [lindex $vPorts 1]

puts "Assign the real ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

################################################################################
# setting ipv4 interfaces
################################################################################
puts "Set ipv4 interfaces" 
set interface1 [ixNet add $vPort1 interface]
set ipv41 [ixNet add $interface1 ipv4]
set interface2 [ixNet add $vPort2 interface]
set ipv42 [ixNet add $interface2 ipv4]
ixNet commit

################################################################################
# enabling protocol interface
################################################################################
puts "Enable protocol interface"
ixNet setAttribute $interface1 -enabled true
ixNet setAttribute $interface2 -enabled true
ixNet commit

################################################################################
# configuring ip and gateway on each interface
################################################################################
puts "Add IP address, Gateway and Mask on Protocol Interface 1"
ixNet setAttribute $ipv41 -ip 20.20.20.2
ixNet setAttribute $ipv41 -maskWidth 24
ixNet setAttribute $ipv41 -gateway 20.20.20.1
ixNet commit
puts "Add IP address, Gateway and Mask on Protocol Interface 1"
ixNet setAttribute $ipv42 -ip 20.20.20.1
ixNet setAttribute $ipv42 -maskWidth 24
ixNet setAttribute $ipv42 -gateway 20.20.20.2
ixNet commit

################################################################################
# Enable OSPFv2 on ports
################################################################################
# Enable ospf from protocol management
ixNet setAttribute $vPort1/protocols/ospf -enabled true
ixNet setAttribute $vPort2/protocols/ospf -enabled true
ixNet commit

################################################################################
# Configure OSPFv2 routers on ports
################################################################################
set router1 [ixNet add $vPort1/protocols/ospf router]
ixNet setAttribute $router1 -enabled true
ixNet setAttribute $router1 -routerId 1.1.1.1
ixNet setAttribute $router1 -discardLearnedLsa false
ixNet commit

set router2 [ixNet add $vPort2/protocols/ospf router]
ixNet setAttribute $router2 -enabled true
ixNet setAttribute $router2 -routerId 2.2.2.2
ixNet setAttribute $router2 -discardLearnedLsa false
ixNet commit

################################################################################
# Configure interfaces on OSPFv2 routers 
################################################################################
set router1Interface [ixNet add $router1 interface]
ixNet setAttribute $router1Interface -connectedToDut true
ixNet setAttribute $router1Interface -protocolInterface $interface1
ixNet setAttribute $router1Interface -enabled true
ixNet setAttribute $router1Interface -networkType pointToPoint
ixNet commit

set router2Interface [ixNet add $router2 interface]
ixNet setAttribute $router2Interface -connectedToDut true
ixNet setAttribute $router2Interface -protocolInterface $interface2
ixNet setAttribute $router2Interface -enabled true
ixNet setAttribute $router2Interface -networkType pointToPoint
ixNet commit

#######################################################################################
# Configure 10 route range on each OSPFv2 router , enable only the first 5 route ranges
#######################################################################################
for {set count 1} {$count <= 10} {incr count} {
	set router1routeRange [ixNet add $router1 routeRange]
	if {$count <= 5} {
		ixNet setAttribute $router1routeRange -enabled true
		ixNet setAttribute $router1routeRange -origin externalType1
	}
	ixNet setAttribute $router1routeRange -networkNumber 55.55.55.$count
	ixNet commit

	set router2routeRange [ixNet add $router2 routeRange]
	if {$count <= 5} {
		ixNet setAttribute $router2routeRange -enabled true
		ixNet setAttribute $router2routeRange -origin externalType1
	}
	ixNet setAttribute $router2routeRange -networkNumber 66.66.66.$count
	ixNet commit
}

################################################################################
# 2. Start OSPFv2 protocol and wait for 60 seconds
################################################################################
puts "Start OSPFv2 and wait for 60 seconds for protocol to come up"
ixNet exec startAllProtocols
after 30000

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
puts "Fetch all OSPF Aggregated Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"OSPF Aggregated Statistics"/page}
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
###############################################################################
# 4. Retrieve protocol learned info
###############################################################################
puts "Retrieve protocol learned info"
ixNet exec refreshLearnedInfo $router1Interface
ixNet exec refreshLearnedInfo $router2Interface
set waitPeriod 0
set isRefreshedInterface1 false
set isRefreshedInterface2 false
while {$isRefreshedInterface1 != true && $isRefreshedInterface2 != true } {
	set isRefreshedInterface1 [ixNet getAttr $router1Interface -isLearnedInfoRefreshed]
	set isRefreshedInterface2 [ixNet getAttr $router2Interface -isLearnedInfoRefreshed]
	after 1000
	incr waitPeriod
	if {$waitPeriod > 60} {
		puts "Could not retrieve learnt info on ports"
	}
}

set listLSA1 [ixNet getList $router1Interface learnedLsa]
set listLSA2 [ixNet getList $router2Interface learnedLsa]
set count 1

puts "LSA retrieved on port 1"
foreach item $listLSA1 {
	puts "LSA : $count"
	puts "***************************************************"

	set linkStateID [ixNet getAttribute $item -linkStateId]
	set advRouterID [ixNet getAttribute $item -advRouterId]
	set lsaType [ixNet getAttribute $item -lsaType]
	set seqNumber [ixNet getAttribute $item -seqNumber]
	set age [ixNet getAttribute $item -age]

	puts "linkStateID \t:\t $linkStateID"
	puts "advRouterID \t:\t $advRouterID"
	puts "lsaType     \t:\t $lsaType"
	puts "seqNumber   \t:\t $seqNumber"
	puts "age         \t:\t $age"
	puts ""
	incr count
}
puts "LSA retrieved on port 2"
set count 1
foreach item $listLSA2 {
	puts "LSA : $count"
	puts "***************************************************"

	set linkStateID [ixNet getAttribute $item -linkStateId]
	set advRouterID [ixNet getAttribute $item -advRouterId]
	set lsaType [ixNet getAttribute $item -lsaType]
	set seqNumber [ixNet getAttribute $item -seqNumber]
	set age [ixNet getAttribute $item -age]

	puts "linkStateID \t:\t $linkStateID"
	puts "advRouterID \t:\t $advRouterID"
	puts "lsaType     \t:\t $lsaType"
	puts "seqNumber   \t:\t $seqNumber"
	puts "age         \t:\t $age"
	puts ""
	incr count
}

puts "***************************************************"


################################################################################
# 5. Enable all route ranges on each OSPFv2 router
################################################################################
puts "Enable all available route ranges on each OSPFv2 router"
set router1routeRangeList [ixNet getList $router1 routeRange]
set router2routeRangeList [ixNet getList $router2 routeRange]

foreach routeRange $router1routeRangeList {
   ixNet setAttribute $routeRange -enabled true
}
ixNet commit

foreach routeRange $router2routeRangeList {
   ixNet setAttribute $routeRange -enabled true
}
ixNet commit

#####################################################################################
# 6. Disable / Enable interfaces on each OSPFv2 router for new routes to be available
#####################################################################################
puts "Disable / Enable interfaces on each OSPFv2 router for new routes to be available"
set router1InterfaceList [ixNet getList $router1 interface]
set router2InterfaceList [ixNet getList $router2 interface]
foreach interface $router1InterfaceList {
   ixNet setAttribute $interface -enabled false
   ixNet commit
   ixNet setAttribute $interface -enabled true
}
ixNet commit

foreach interface $router2InterfaceList {
   ixNet setAttribute $interface -enabled false
   ixNet commit
   ixNet setAttribute $interface -enabled true
}
ixNet commit

###############################################################################
# 7. Retrieve protocol learned info , wait till 60 sec for table to be refreshed
###############################################################################
after 10000
puts "Retrieve protocol learned info"
ixNet exec refreshLearnedInfo $router1Interface
ixNet exec refreshLearnedInfo $router2Interface
set waitPeriod 0
set isRefreshedInterface1 false
set isRefreshedInterface2 false
while {$isRefreshedInterface1 != true && $isRefreshedInterface2 != true } {
	set isRefreshedInterface1 [ixNet getAttr $router1Interface -isLearnedInfoRefreshed]
	set isRefreshedInterface2 [ixNet getAttr $router2Interface -isLearnedInfoRefreshed]
	after 1000
	incr waitPeriod
	if {$waitPeriod > 60} {
		puts "Could not retrieve learnt info on ports"
	}
}

set listLSA1 [ixNet getList $router1Interface learnedLsa]
set listLSA2 [ixNet getList $router2Interface learnedLsa]
set count 1

puts "LSA retrieved on port 1"
foreach item $listLSA1 {
	puts "LSA : $count"
	puts "***************************************************"

	set linkStateID [ixNet getAttribute $item -linkStateId]
	set advRouterID [ixNet getAttribute $item -advRouterId]
	set lsaType [ixNet getAttribute $item -lsaType]
	set seqNumber [ixNet getAttribute $item -seqNumber]
	set age [ixNet getAttribute $item -age]

	puts "linkStateID \t:\t $linkStateID"
	puts "advRouterID \t:\t $advRouterID"
	puts "lsaType     \t:\t $lsaType"
	puts "seqNumber   \t:\t $seqNumber"
	puts "age         \t:\t $age"
	puts ""
	incr count
}
puts "LSA retrieved on port 2"
set count 1
foreach item $listLSA2 {
	puts "LSA : $count"
	puts "***************************************************"

	set linkStateID [ixNet getAttribute $item -linkStateId]
	set advRouterID [ixNet getAttribute $item -advRouterId]
	set lsaType [ixNet getAttribute $item -lsaType]
	set seqNumber [ixNet getAttribute $item -seqNumber]
	set age [ixNet getAttribute $item -age]

	puts "linkStateID \t:\t $linkStateID"
	puts "advRouterID \t:\t $advRouterID"
	puts "lsaType     \t:\t $lsaType"
	puts "seqNumber   \t:\t $seqNumber"
	puts "age         \t:\t $age"
	puts ""
	incr count
}

puts "***************************************************"

###############################################################################
# 8. Configure L2-L3 traffic 
###############################################################################
puts "Congfiguring L2-L3 Traffic Item"
set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {Traffic Item OSPF}           \
    -roundRobinPacketOrdering false  \
    -trafficType ipv4
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $vPort1/protocols/ospf]
set destination  [list $vPort2/protocols/ospf]

ixNet setMultiAttribute $endpointSet1\
    -name                  "EndpointSet-1"\
    -multicastDestinations [list]\
    -scalableSources       [list]\
    -multicastReceivers    [list]\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               $source\
    -destinations          $destination\    
ixNet commit

ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy        [list sourceDestEndpointPair0 trackingenabled0]
ixNet commit

###############################################################################
# 9. Apply and start L2/L3 traffic
###############################################################################
puts "Applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "Starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

puts "Let traffic run for 1 minute"
after 60000

###############################################################################
# 10. Retrieve L2/L3 traffic item statistics
###############################################################################
puts "Verifying all the L2-L3 traffic stats\n"
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
puts "***************************************************"

################################################################################
# 11. Stop L2/L3 traffic
################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 12. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
