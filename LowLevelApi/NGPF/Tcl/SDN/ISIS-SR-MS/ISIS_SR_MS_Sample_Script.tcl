#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2016 by IXIA                                           # 
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    23/06/2016 - Anit Ghosal - created sample                                 #
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
#    This script intends to demonstrate how to use NGPF ISIS SR MS TCL API.    #
#                                                                              #
#    1. It will create 2 ISIS topologies, topology1 will have a simulated      #
#       topology Linear behind Device Group1 and Mesh behind Device Group2.    #
#    2. Enable Segment Routing in ISIS Emulated Router.                        #
#    3. Set SRGB range and SID Count for Emulated Router.                      #
#    4. Set IPV4 and IPV6 Ranges for both router acts as Mapping Server(MS)    #
#         and accordingly IPV4 & IPV6 Node Routes in Simulated Topologies.     #
#    5. Start Protocol And Retrieve protocol statistics.                       #
#    6. Retrieve protocol learned info in Port1.                               #
#    7. Retrieve protocol learned info in Port2.                               #
#    8. On the fly change SID Index value for IPv4 MS Ranges in Device Group1. #
#    9. On the fly Change IPV6 prefix in MS range and accordingly IPV6 address #
#        count of Node Routes in  Mesh Simulated Topology behind Device Group2.#  
#    10.On the fly Change in IPV6 FEC prefix in MS  and accordingly IPV6       #
#       address of Node Routes in Mesh Simulated Topology behind Device Group2.#
#    11. Retrieve protocol learned info in both ports after On the Fly changes.#
#    12. Configuring ISIS L2-L3 IPv4 & IPv6 Traffic Item for MS prefix ranges. #
#    13. Verifying all the L2-L3 traffic stats                                 #
#    14. Stop L2-L3 traffic.                                                   #
#    15. Stop all protocols.                                                   #
#                                                                              #
# Ixia Softwares:                                                              #
#    IxOS      8.10 EA                                                         #
#    IxNetwork 8.10 EA                                                         #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your set-up
namespace eval ::ixia {
    set ixTclServer 10.216.108.27
    set ixTclPort   8009
    set ports       {{10.216.108.99 4  3} { 10.216.108.99  4  4}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.01\
   -setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure ISIS as per the description
#  give above
################################################################################ 
# Adding Virtual ports
puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]
set vportRx [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

# Adding topologies
puts "Adding 2 topologies"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet add [ixNet getRoot] topology -vports $vportRx
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

# Adding Device Groups
puts "Adding 2 device groups"
ixNet add $topo1 deviceGroup
ixNet add $topo2 deviceGroup
ixNet commit

set t1devices [ixNet getList $topo1 deviceGroup]
set t2devices [ixNet getList $topo2 deviceGroup]

set t1dev1 [lindex $t1devices 0]
set t2dev1 [lindex $t2devices 0]

puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $t1dev1 -multiplier 1
ixNet setAttr $t2dev1 -multiplier 1
ixNet commit

# Adding Ethernet
puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet commit

set mac1 [ixNet getList $t1dev1 ethernet]
set mac2 [ixNet getList $t2dev1 ethernet]

puts "Configuring the mac addresses"
ixNet setMultiAttr [ixNet getAttr $mac1 -mac]/counter\
        -direction  increment                        \
        -start      {18:03:73:C7:6C:B1}              \
        -step       {00:00:00:00:00:01}

ixNet setAttr [ixNet getAttr $mac2 -mac]/singleValue\
        -value      {18:03:73:C7:6C:01}
ixNet commit


# Adding IPv4
puts "Add ipv4 Stack"
ixNet add $mac1 ipv4
ixNet add $mac2 ipv4
ixNet commit

set ip1 [ixNet getList $mac1 ipv4]
set ip2 [ixNet getList $mac2 ipv4]

set mvAdd1 [ixNet getAttr $ip1 -address]
set mvAdd2 [ixNet getAttr $ip2 -address]
set mvGw1  [ixNet getAttr $ip1 -gatewayIp]
set mvGw2  [ixNet getAttr $ip2 -gatewayIp]

puts "Configuring ipv4 addresses"
ixNet setAttr $mvAdd1/singleValue -value "100.0.0.1"
ixNet setAttr $mvAdd2/singleValue -value "100.0.0.2"
ixNet setAttr $mvGw1/singleValue  -value "100.0.0.2"
ixNet setAttr $mvGw2/singleValue  -value "100.0.0.1"

ixNet setAttr [ixNet getAttr $ip1 -prefix]/singleValue -value 24
ixNet setAttr [ixNet getAttr $ip2 -prefix]/singleValue -value 24

ixNet setMultiAttr [ixNet getAttr $ip1 -resolveGateway]/singleValue -value true
ixNet setMultiAttr [ixNet getAttr $ip2 -resolveGateway]/singleValue -value true
ixNet commit



# Adding ISIS over Ethernet stack
puts "Adding ISIS over Ethernet stacks"
ixNet add $mac1 isisL3
ixNet add $mac2 isisL3
ixNet commit

set isisL3_1 [ixNet getList $mac1 isisL3]
set isisL3_2 [ixNet getList $mac2 isisL3]

puts "Renaming the topologies and the device groups"
ixNet setAttr $topo1  -name "ISIS Topology 1"
ixNet setAttr $topo2  -name "ISIS Topology 2"

ixNet setAttr $t1dev1 -name "ISIS Topology 1 Router"
ixNet setAttr $t2dev1 -name "ISIS Topology 2 Router"
ixNet commit

set isisL3Router1_1 [ixNet getList $t1dev1 isisL3Router]
set isisL3Router2_1 [ixNet getList $t2dev1 isisL3Router]

# Enable host name in ISIS routers
puts "Enabling Host name in Emulated ISIS Routers"
set isisL3Router1 [ixNet getList [ixNet getList $topo1 deviceGroup] isisL3Router]
set enableHostName1 [ixNet getAttr $isisL3Router1 -enableHostName]
ixNet setAttr $enableHostName1/singleValue -value True
ixNet commit
set configureHostName1 [ixNet getAttr $isisL3Router1 -hostName]
ixNet setAttr $configureHostName1/singleValue -value "isisL3Router1"
ixNet commit

set isisL3Router2 [ixNet getList [ixNet getList $topo2 deviceGroup] isisL3Router]
set enableHostName2 [ixNet getAttr $isisL3Router2 -enableHostName]
ixNet setAttr $enableHostName2/singleValue -value True
ixNet commit
set configureHostName2 [ixNet getAttr $isisL3Router2 -hostName]
ixNet setAttr $configureHostName2/singleValue -value "isisL3Router2"
ixNet commit

puts "Making the NetworkType to Point to Point in the ISIS router in Device Group1 "
set networkTypeMultiValue1 [ixNet getAttr $isisL3_1 -networkType]
ixNet setAttr $networkTypeMultiValue1 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue1/singleValue -value pointpoint

puts "Making the NetworkType to Point to Point in the ISIS router in Device Group2"
set networkTypeMultiValue2 [ixNet getAttr $isisL3_2 -networkType]
ixNet setAttr $networkTypeMultiValue2 -pattern singleValue -clearOverlays False
ixNet setAttr $networkTypeMultiValue2/singleValue -value pointpoint

# Disable Discard Learned LSP
puts "Disabling the Discard Learned Info CheckBox"

set isisL3RouterDiscardLearnedLSP1 [ ixNet getAttr [ixNet getList [ixNet getList $topo1 deviceGroup] isisL3Router] -discardLSPs]
set isisL3RouterDiscardLearnedLSP2 [ ixNet getAttr [ixNet getList [ixNet getList $topo2 deviceGroup] isisL3Router] -discardLSPs]

ixNet setAttr $isisL3RouterDiscardLearnedLSP1 -pattern singleValue -clearOverlays False
ixNet setAttr $isisL3RouterDiscardLearnedLSP1/singleValue -value False
ixNet setAttr $isisL3RouterDiscardLearnedLSP2 -pattern singleValue -clearOverlays False
ixNet setAttr $isisL3RouterDiscardLearnedLSP2/singleValue -value False

puts "Add Linear ST on the back of Device Group1 "
set networkGoup1 [ ixNet add $t1devices networkGroup ]
ixNet commit
set networkTopology1 [ixNet add $networkGoup1  networkTopology  ]
ixNet commit
set lineartopo [ixNet add $networkTopology1 netTopologyLinear ]
ixNet commit

puts "Add Mesh ST on the back of Device Group2 "
set networkGoup2 [ ixNet add $t2devices networkGroup ]
ixNet commit
set networkTopology2 [ixNet add $networkGoup2  networkTopology  ]
ixNet commit
set lineartopo2 [ixNet add $networkTopology2 netTopologyMesh ]
ixNet commit

#Setting Multiplier

ixNet setAttr $networkGoup1 -multiplier 3
ixNet commit

ixNet setAttr $networkGoup2 -multiplier 1
ixNet commit

ixNet setAttr $networkGoup1 -name "ISIS_Linear Topology 1 "
ixNet commit

ixNet setAttr $networkGoup2 -name "ISIS_Linear Topology 2"
ixNet commit

########################################################################################
# 2.Enabling Segment Routing in Emulated Router on Device Group 1 and Device Group 2 
########################################################################################
puts "Enabling Segment Routing for ISIS"
ixNet setAttr $isisL3Router1 -enableSR true

ixNet setAttr $isisL3Router2 -enableSR true
ixNet commit

################################################################################
# 3.Setting SRGB range and SID Count for Emulated Router
################################################################################
puts "Setting SRGB range pool for  Emulated Router in Device Group1"
puts "***************************************************"

set isisSRGBRangeSubObjectsList1 [ixNet getList $isisL3Router1 isisSRGBRangeSubObjectsList]
set startSIDLabel1 [ixNet getA $isisSRGBRangeSubObjectsList1 -startSIDLabel]
set svsrgb1 [ixNet getList $startSIDLabel1 singleValue]
ixNet setAtt $svsrgb1 -value 15000
ixNet commit

puts "Setting SID count for Emulated Router  Device Group 1"
set sidCount1 [ixNet getA $isisSRGBRangeSubObjectsList1 -sIDCount]
set sidcountsv [ixNet getList $sidCount1 singleValue]
ixNet setA $sidcountsv -value 100
ixNet commit

puts "Setting SRGB range pool for  Emulated Router Device Group2"
puts "***************************************************"
set isisSRGBRangeSubObjectsList2 [ixNet getList $isisL3Router2 isisSRGBRangeSubObjectsList]
set startSIDLabel1 [ixNet getA $isisSRGBRangeSubObjectsList2 -startSIDLabel]
set svsrgb1 [ixNet getList $startSIDLabel1 singleValue]
ixNet setAtt $svsrgb1 -value 10000
ixNet commit

puts "Setting SID count for  Emulated Router Device Group2"
set sidCount2 [ixNet getA $isisSRGBRangeSubObjectsList2 -sIDCount]
set sidcountsv [ixNet getList $sidCount2 singleValue]
ixNet setA $sidcountsv -value 100
ixNet commit

###########################################################################################################################################
# 4. Set IPV4 and IPV6 Ranges for both router acts as Mapping Server(MS)and accordingly IPV4 & IPV6 Node Routes in Simulated Topologies    
###########################################################################################################################################         
puts "Enabling IPV4  and IPV6 Node Routes Simulated Routers on Linear Network Group behind Device Group1"
puts "***************************************************"
set networkTopo1 [ixNet getList $networkGoup1 networkTopology]
set simRouter1 [ixNet getList $networkTopo1 simRouter]
set isisPseudoRouter1 [ixNet getList $simRouter1 isisL3PseudoRouter]
set ipv4noderoutes [ixNet getList $isisPseudoRouter1  IPv4PseudoNodeRoutes ]
set active [ixNet getAttr $ipv4noderoutes -active ]
set activesin [ixNet add $active singleValue ]
ixNet setAttr $activesin -value True
ixNet commit

set ipv6noderoutes [ixNet getList $isisPseudoRouter1  IPv6PseudoNodeRoutes ]
set active1 [ixNet getAttr $ipv6noderoutes -active ]
set activesin1 [ixNet add $active1 singleValue ]
ixNet setAttr $activesin1 -value True
ixNet commit

puts "Changing Prefix Length to 24 "

set prefixlen [ ixNet getAttr $ipv4noderoutes  -prefixLength  ]
set prefix [ixNet add $prefixlen singleValue ]
ixNet setAttr $prefix -value 24
ixNet commit

puts "Enabling IPV4  and IPV6 Node Routes Simulated Routers on Mesh Network Group behind Device Group2"
puts "***************************************************"
set networkTopo2 [ixNet getList $networkGoup2 networkTopology]
set simRouter2 [ixNet getList $networkTopo2 simRouter]
set isisPseudoRouter2 [ixNet getList $simRouter2 isisL3PseudoRouter]
set ipv4noderoutes2 [ixNet getList $isisPseudoRouter2  IPv4PseudoNodeRoutes ]
set active2 [ixNet getAttr $ipv4noderoutes2 -active ]
set activesin2 [ixNet add $active2 singleValue ]
ixNet setAttr $activesin2 -value True
ixNet commit

set ipv6noderoutes2 [ixNet getList $isisPseudoRouter2  IPv6PseudoNodeRoutes ]
set active12 [ixNet getAttr $ipv6noderoutes2 -active ]
set activesin12 [ixNet add $active12 singleValue ]
ixNet setAttr $activesin12 -value True
ixNet commit

puts "Changing Prefix Length to 24 "

set prefixlen2 [ ixNet getAttr $ipv4noderoutes2  -prefixLength  ]
set prefix2 [ixNet add $prefixlen2 singleValue ]
ixNet setAttr $prefix2 -value 24
ixNet commit

puts "Enabling Mapping Server on  Emulated Router in Device Group 1  and Setting No. of IPV4 and IPV6 Mapping Ranges"
puts "***************************************************"

set enablems1 [ixNet getAttribute $t1devices/isisL3Router:1 -enableMappingServer]
	
			
set single [ixNet add $enablems1 "singleValue"]
ixNet setMultiAttribute $single \
-value true
ixNet commit

ixNet setMultiAttribute $t1devices/isisL3Router:1 \
			-enableSR true \
			-numberOfMappingIPV4Ranges 3 \
			-numberOfMappingIPV6Ranges 3 \
			-name "ISIS-L3\ RTR\ 1"
			
ixNet commit 

puts "Enabling Mapping Server on  Emulated Router in Device Group 2  and Setting No. of IPV4 and IPV6 Mapping Ranges "
puts "***************************************************"

set enablems2 [ixNet getAttribute $t2devices/isisL3Router:1 -enableMappingServer]

set single [ixNet add $enablems2 "singleValue"]
ixNet setMultiAttribute $single \
-value true
ixNet commit

ixNet setMultiAttribute $t2devices/isisL3Router:1 \
			-enableSR true \
			-numberOfMappingIPV4Ranges 3 \
			-numberOfMappingIPV6Ranges 3 \
			-name "ISIS-L3\ RTR\ 1"
			
ixNet commit 		

puts "Setting Mapping Server IPV4 FEC Prefix ranges For Emulated Router1 in Device Group1"

set isisvmsppingserverv4 [ ixNet getList $isisL3Router1 isisMappingServerIPV4List ]
set fecprefix [ixNet getAttribute $isisvmsppingserverv4 -fECPrefix]
ixNet commit
		set counter [ixNet add $fecprefix "counter"]
		ixNet setMultiAttribute $counter \
			-step 0.1.0.0 \
			-start 201.1.0.0 \
			-direction increment
		ixNet commit

puts "Setting Mapping Server IPV6 FEC Prefix ranges For Emulated Router1 in Device Group1 "

set isisvmsppingserverv6 [ ixNet getList $isisL3Router1 isisMappingServerIPV6List ]
set fecprefix1 [ixNet getAttribute $isisvmsppingserverv6 -fECPrefix]
ixNet commit
set counter1 [ixNet add $fecprefix1 "counter"]
ixNet setMultiAttribute $counter1 \
			-step 0:0:0:1:0:0:0:0 \
			-start 3000:0:1:1:0:0:0:0 \
			-direction increment
ixNet commit

puts "Setting Mapping Server IPV4 FEC Prefix ranges For Emulated Router2 in Device Group2 "

set isisvmsppingserverv4 [ ixNet getList $isisL3Router2 isisMappingServerIPV4List ]
set fecprefix [ixNet getAttribute $isisvmsppingserverv4 -fECPrefix]
ixNet commit
		set counter [ixNet add $fecprefix "counter"]
		ixNet setMultiAttribute $counter \
			-step 0.1.0.0 \
			-start 202.1.0.0 \
			-direction increment
		ixNet commit

puts "Setting Mapping Server IPV6 FEC Prefix ranges For Emulated Router2 in Device Group2 "

set isisvmsppingserverv6 [ ixNet getList $isisL3Router2 isisMappingServerIPV6List ]
set fecprefix1 [ixNet getAttribute $isisvmsppingserverv6 -fECPrefix]
ixNet commit
set counter1 [ixNet add $fecprefix1 "counter"]
ixNet setMultiAttribute $counter1 \
			-step 0:0:0:1:0:0:0:0 \
			-start 3000:1:1:1:0:0:0:0 \
			-direction increment
ixNet commit

######################################################################################
# 5. Start ISIS protocol and wait for 60 seconds And  Retrieve protocol statistics.
######################################################################################
puts "Starting protocols and waiting for 60 seconds for protocols to come up"
ixNet exec startAllProtocols
after 60000

puts "Fetching all Protocol Summary Stats\n"
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
puts "***************************************************\n"

###############################################################################
# 6. Retrieve protocol learned info in Port 1
###############################################################################
puts "Fetching ISIS IPv4 & IPv6 Learned Info of Device Group1 Topology1 Emulated Router  for Proper Prefix-Label Binding in Port1 "
puts "***************************************************"
ixNet exec getLearnedInfo $isisL3_1 
after 5000
set learnedInfoList [ixNet getList $isisL3_1 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]
set IPv4Info [lindex $linfoList 0]
set IPv6LInfo [lindex $linfoList 1]

puts "***************************************************"
foreach table $linfoList {
    set type [ixNet getAttr $table -type]
    puts "$type :"
    puts "***************************************************"
    set column [ixNet getAttr $table -columns]
    puts "$column"
    set values [ixNet getAttr $table -values]
    puts "$values\n"
    puts "***************************************************"
}
puts "***************************************************"

###############################################################################
# 7. Retrieve protocol learned info in Port 2
###############################################################################
puts "Fetching ISIS IPv4 & IPv6 Learned Info of  Device Group2 Topology1 Emulated Router Proper Prefix-Label Binding in Port2 "
puts "***************************************************"
ixNet exec getLearnedInfo $isisL3_2
after 5000
set learnedInfoList [ixNet getList $isisL3_2 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]
set IPv4Info [lindex $linfoList 0]
set IPv6LInfo [lindex $linfoList 1]

puts "***************************************************"
foreach table $linfoList {
    set type [ixNet getAttr $table -type]
    puts "$type :"
    puts "***************************************************"
    set column [ixNet getAttr $table -columns]
    puts "$column"
    set values [ixNet getAttr $table -values]
    puts "$values\n"
    puts "***************************************************"
}
puts "***************************************************"

###############################################################################
# 8. OTF on SID value
###############################################################################
puts "OTF on Device Group1  in Topology1 IPV4 MS SID value "
puts "***************************************************"

set isisvmsppingserverv4 [ ixNet getList $isisL3Router1 isisMappingServerIPV4List ]
set newsid11 [ixNet getAttr $isisvmsppingserverv4 -startSIDLabel]
set overlay61 [ixNet add $newsid11 overlay]
ixNet setMultiAttribute $overlay61  -index 1  -value 10
ixNet commit


#######################################################################################################
# 9. OTF on  Address  Of Mapping Server  IPV6 and Simulated Topology  And Apply Changes
######################################################################################################
puts "OTF on Device Group 2 Topology 1 Address Field"
puts "\n"
set isisvmsppingserverv6 [ ixNet getList $isisL3Router2 isisMappingServerIPV6List ]
set fecprefix [ixNet getAttr $isisvmsppingserverv6 -fECPrefix]
set overlay10 [ixNet add $fecprefix overlay]
ixNet setMultiAttribute $overlay10 -count 1 -index 2   -value 3000:4:1:2:0:0:0:0
ixNet commit

set v6noderoutes [ixNet getAttr $ipv6noderoutes2 -networkAddress ]
set overlay [ixNet add $v6noderoutes  overlay ]
ixNet setAttr $overlay -count 1 -index 2   -value 3000:4:1:2:0:0:0:0
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology

if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
    puts "$::errorInfo"
}
after 5000

#######################################################################################################
# 10. OTF on Range  Of  Mapping Server  IPV6 and Simulated Topology  also And Apply Changes
######################################################################################################
puts "OTF on Device Group2 Topology2 IPV6 MS range and  also in ST "
puts "\n"

set range [ixNet getAttr $ipv6noderoutes2 -rangeSize ]
set overlay1 [ixNet add $range  overlay ]
ixNet setAttr $overlay1 -count 1 -index 1   -value 4
ixNet commit

set range1 [ixNet getAttr $isisvmsppingserverv6 -range ]
set overlay11 [ixNet add $range1  overlay ]
ixNet setAttr $overlay11 -count 1 -index 1   -value 4
ixNet commit

set globals [ixNet getRoot]/globals
set topology $globals/topology

if {[catch {ixNet exec applyOnTheFly $topology}] == 1} {
    puts "error in applying on the fly change"
    puts "$::errorInfo"
}
after 5000

###############################################################################
# 11 . Retrieve protocol learned info in Both Port 
###############################################################################
puts "Fetching ISIS IPv4 & IPv6 Learned Info of Device Group1 Topology1 Emulated Router  for Proper Prefix-Label Binding in Port1 "

ixNet exec getLearnedInfo $isisL3_1 
after 5000
set learnedInfoList [ixNet getList $isisL3_1 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]
set IPv4Info [lindex $linfoList 0]
set IPv6LInfo [lindex $linfoList 1]

puts "***************************************************"
foreach table $linfoList {
    set type [ixNet getAttr $table -type]
    puts "$type :"
    puts "***************************************************"
    set column [ixNet getAttr $table -columns]
    puts "$column"
    set values [ixNet getAttr $table -values]
    puts "$values\n"
    puts "***************************************************"
}
puts "***************************************************"

puts "Fetching ISIS IPv4 & IPv6 Learned Info in Device Group 2 Topology 1 Emulated Router  for Proper Prefix-Label Binding After OTF in Port 2 "
ixNet exec getLearnedInfo $isisL3_2
after 5000
set learnedInfoList [ixNet getList $isisL3_2 learnedInfo]
set linfoList [ixNet getList $learnedInfoList table]
set IPv4Info [lindex $linfoList 0]
set IPv6LInfo [lindex $linfoList 1]

puts "***************************************************"
foreach table $linfoList {
    set type [ixNet getAttr $table -type]
    puts "$type :"
    puts "***************************************************"
    set column [ixNet getAttr $table -columns]
    puts "$column"
    set values [ixNet getAttr $table -values]
    puts "$values\n"
    puts "***************************************************"
}
puts "***************************************************"

################################################################################
# 12. Configure L2-L3 traffic 
################################################################################
puts "Configuring  L2-L3 IPv4 Traffic Item # 1"
puts "***************************************************"

puts "Configuring traffic item 1 with endpoints src :isisPseudoNodeRoutes IPV4 & dst :isisPseudoNodeRoutes IPV4 "

set trafficItem1 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem1\
    -name {IPv4_MPLS_Traffic_Item_1}  \
	-biDirectional true \
	-useControlPlaneRate true \
	-useControlPlaneFrameSize true \
	-mergeDestinations false \
	-roundRobinPacketOrdering false \
	-numVlansForMulticastReplication 1 \
	-trafficType ipv4
ixNet commit

set trafficItem1 [lindex [ixNet remapIds $trafficItem1] 0]
set endpointSet1 [ixNet add $trafficItem1 "endpointSet"]
set source       [list $networkGoup1/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv4PseudoNodeRoutes:1]
set destination   [list $networkGoup2/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv4PseudoNodeRoutes:1]

ixNet setMultiAttribute $endpointSet1\
    -name                  "EndpointSet-1"\
    -multicastDestinations [list]\
    -scalableSources       [list]\
    -multicastReceivers    [list]\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               $source\
    -destinations          $destination
ixNet commit

ixNet setMultiAttribute $trafficItem1/configElement:1/transmissionDistribution \
    -distributions [list srcDestEndpointPair0 ]
	
ixNet commit

ixNet setMultiAttribute $trafficItem1/tracking\
    -trackBy        [list sourceDestValuePair0 trackingenabled0 mplsMplsLabelValue0 ipv4DestIp0 ipv4SourceIp0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]\
	
ixNet commit




puts "Configuring  L2-L3 IPv6 Traffic Item # 2"
puts "***************************************************"

puts "Configuring traffic item 2 with endpoints src :isisPseudoNodeRoutes IPV6 & dst :isisPseudoNodeRoutes IPV6 "

set trafficItem2 [ixNet add [ixNet getRoot]/traffic "trafficItem"]
ixNet setMultiAttribute $trafficItem2\
    -name {IPv6_MPLS_Traffic_Item_1}  \
	-biDirectional true \
	-useControlPlaneRate true \
	-useControlPlaneFrameSize true \
	-mergeDestinations false \
	-roundRobinPacketOrdering false \
	-numVlansForMulticastReplication 1 \
	-trafficType ipv6
ixNet commit

set trafficItem2 [lindex [ixNet remapIds $trafficItem2] 0]
set endpointSet2 [ixNet add $trafficItem2 "endpointSet"]
set source1      [list $networkGoup1/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1]
set destination1   [list $networkGoup2/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1]

ixNet setMultiAttribute $endpointSet2\
    -name                  "EndpointSet-2"\
    -multicastDestinations [list]\
    -scalableSources       [list]\
    -multicastReceivers    [list]\
    -scalableDestinations  [list]\
    -ngpfFilters           [list]\
    -trafficGroups         [list]\
    -sources               $source1\
    -destinations          $destination1
ixNet commit

ixNet setMultiAttribute $trafficItem2/configElement:1/transmissionDistribution \
    -distributions [list srcDestEndpointPair0 ]
	
ixNet commit

ixNet setMultiAttribute $trafficItem2/tracking\
    -trackBy        [list sourceDestValuePair0 trackingenabled0 mplsMplsLabelValue0 ipv6DestIp0 ipv6SourceIp0]\
    -fieldWidth     thirtyTwoBits\
    -protocolOffset Root.0\
    -values         [list]\
	
ixNet commit

##################################################################################
# 13. Apply and start L2/L3 traffic And  Retrieve L2/L3 traffic item statistics
##################################################################################
puts "Applying L2/L3 traffic"
ixNet exec apply [ixNet getRoot]/traffic
after 5000

puts "Starting L2/L3 traffic"
ixNet exec start [ixNet getRoot]/traffic

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
# 14. Stop L2/L3 traffic
#################################################################################
puts "Stopping L2/L3 traffic"
ixNet exec stop [ixNet getRoot]/traffic
after 5000

################################################################################
# 15. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"
puts "***************************************************"

