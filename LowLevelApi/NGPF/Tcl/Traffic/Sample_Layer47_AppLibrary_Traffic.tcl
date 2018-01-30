################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997  2015 by IXIA                                             #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    02/02/2015  Andrei Parvu - created sample                                 #
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
# omissions or errorfree.                                                      #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NONINFRINGEMENT.                                  #
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
# damages limitations  forth herein and will not obligate Ixia to provide      #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

#################################################################################
#                                                                              	#
# Description:                                                                 	#
#	The script below represents an end to end workflow for AppLibrary Traffic. 	#
#	Steps:																	   	#			
#	1. Chassis connection and TCL server connection							   	#	
#	2. Scenario configuration at layer 2-3									   	#	
#	3. Creation of Applibrary traffic										   	#	
#	4. Per connection parameters configuration 								   	#	
#	5. Traffic apply and start 												   	#
#	6. Statistics operations: drill down in a loop							   	#	
#	7. Test criteria evaluation													#
#	8. Stop traffic															   	#
#													  	 						#		
#################################################################################

puts "\n\n\n#######################################"
puts "Running AppLibrary Sample Workflow Script"
puts "#######################################\n\n\n"

#---------------------------------------------------------
# Setting global variables for the sample run
#---------------------------------------------------------

set chassisIP 				{"10.205.23.34"}						;# chassis IP 
set applicationVersion 		7.40									;# IxN version 
set tclPort 				8549									;# the TCL port on which the IxTcl Server is listening
set port1					{2 15} 									;# where values are: {<card> <port>}
set port2 					{2 16} 									;# where values are: {<card> <port>}				
set PFCriteria_Higher			{"Initiator Tx Rate (Mbps)" 40}		;# statistic from Application Traffic item Statistics view that has to be higher than given value
set PFCriteria_Lower			{"Flows Failed" 40}					;# statistic from Application Traffic item Statistics view that has to be lower than given value
#--------------------------------------------------------------------------------------
# Connecting to TCL Server, resetting the configuration and loading required packages
#--------------------------------------------------------------------------------------

package require IxTclNetwork
puts "Connecting to TCL Server..."
ixNet connect localhost -version $applicationVersion -port $tclPort
ixNet exec newConfig
after 10000
set root [ixNet getRoot]

#------------------------------------
# Adding chassis
#------------------------------------

puts "Adding chassis to the configuration"
set chassis1 [ixNet add $root/availableHardware chassis]
	set chassis1ID [ixNet remapIDs $chassis1]
	
ixNet setAttribute $chassis1ID -hostname $chassisIP
ixNet commit

#------------------------------------
# Adding 2 ports 
#------------------------------------

puts "Adding offline ports to the configuration"
set vport1 [ixNet add $root vport]
	ixNet commit
	set vport1ID [ixNet remapIDs $vport1]

set vport2 [ixNet add $root vport]
	ixNet commit
	set vport2ID [ixNet remapIDs $vport2]
	
ixNet commit

#-----------------------------------------
# Mapping virtual ports to chassis ports 
#-----------------------------------------

puts "Mapping offline ports to actual ports in chassis\n"
ixNet setAttribute $root/vport:1 -connectedTo /availableHardware/chassis:$chassisIP/card:[lindex $port1 0]/port:[lindex $port1 1]
ixNet setAttribute $root/vport:2 -connectedTo /availableHardware/chassis:$chassisIP/card:[lindex $port2 0]/port:[lindex $port2 1]

ixNet commit

#---------------------------------------------------
# Adding 1st topology, Device Group, Ethernet, IPv4 
#---------------------------------------------------

puts "Building first topology and building its stack"
set addedTopology_1 [ixNet add $root topology]
	ixNet commit
	set addedTopology_1ID [ixNet remapIDs $addedTopology_1]

set addedDG [ixNet add $addedTopology_1ID deviceGroup]
	ixNet commit
	set addedDGID [ixNet remapIDs $addedDG]
	
set addedPort [ixNet add $addedTopology_1ID port]
	ixNet commit
	set addedPortID [ixNet remapIDs $addedPort]

set addedEthernet [ixNet add $addedDGID ethernet]
	ixNet commit
	set addedEthernetID [ixNet remapIDs $addedEthernet]

set addedIPv4 [ixNet add $addedEthernetID ipv4]
	ixNet commit
	set addedIPv4ID [ixNet remapIDs $addedIPv4]

#------------------------------------
# Configure 1st topology
#------------------------------------

puts "Addressing the first topology\n"
ixNet setAttribute $addedTopology_1ID -vports $root/vport:1
	ixNet commit
	
set addressMV [ixNet getA $addedIPv4 -address]
ixNet setMultiAttribute $addressMV/counter \
	-direction increment \
	-start 201.1.0.1 \
	-step 0.0.0.1
ixNet commit

set prefixMV [ixNet getA $addedIPv4 -prefix]
ixNet setMultiAttribute $prefixMV/singleValue -value 16
ixNet commit

set gatewayMV [ixNet getA $addedIPv4 -gatewayIp]
ixNet setMultiAttribute $gatewayMV/counter \
	-direction increment \
	-start 201.1.1.1 \
	-step 0.0.0.1
ixNet commit

#------------------------------------
# Adding 2nd topology, DG, ethernet, IPv4 
#------------------------------------

puts "Building second topology and building its stack"

set addedTopology_2 [ixNet add $root topology]
	ixNet commit
	set addedTopology_2ID [ixNet remapIDs $addedTopology_2]

set addedDG [ixNet add $addedTopology_2ID deviceGroup]
	ixNet commit
	set addedDGID [ixNet remapIDs $addedDG]
	
set addedPort [ixNet add $addedTopology_2ID port]
	ixNet commit
	set addedPortID [ixNet remapIDs $addedPort]

set addedEthernet [ixNet add $addedDGID ethernet]
	ixNet commit
	set addedEthernetID [ixNet remapIDs $addedEthernet]

set addedIPv4 [ixNet add $addedEthernetID ipv4]
	ixNet commit
	set addedIPv4ID [ixNet remapIDs $addedIPv4]

#------------------------------------
# Configure 2nd topology
#------------------------------------

puts "Addressing the second topology\n"
ixNet setAttribute $addedTopology_2ID -vports $root/vport:2
	ixNet commit
	
set addressMV [ixNet getA $addedIPv4 -address]
ixNet setMultiAttribute $addressMV/counter \
	-direction increment \
	-start 201.1.1.1 \
	-step 0.0.0.1
ixNet commit

set prefixMV [ixNet getA $addedIPv4 -prefix]
ixNet setMultiAttribute $prefixMV/singleValue -value 16
ixNet commit

set gatewayMV [ixNet getA $addedIPv4 -gatewayIp]
ixNet setMultiAttribute $gatewayMV/counter \
	-direction increment \
	-start 201.1.0.1 \
	-step 0.0.0.1
ixNet commit

#-------------------------------------------
# Create traffic item and add flows
#-------------------------------------------

puts "Adding an AppLibrary traffic item and also adding flows"
set addedTI [ixNet add $root/traffic trafficItem -trafficType ipv4ApplicationTraffic -trafficItemType applicationLibrary]
ixNet commit
set addedTIID [ixNet remapIDs $addedTI]

set addedProfile [ixNet add $addedTIID appLibProfile]
ixNet commit
set addedProfileID [ixNet remapIDs $addedProfile]

ixNet exec addAppLibraryFlow $addedProfileID {Bandwidth_HTTP Echo_UDP Yahoo_Mail Bandwidth_IMAPv4}
ixNet commit

ixNet exec removeAppLibraryFlow $addedProfileID Yahoo_Mail 
ixNet commit

#-----------------------------------------------------
# Link the traffic item to the new topology set
#-----------------------------------------------------

puts "Adding endpoints to the AppLibrary Traffic Item"
set addedEndpointSet [ixNet add $addedTIID endpointSet]
ixNet commit
set addedEndpointSetID [ixNet remapIDs $addedEndpointSet]

ixNet setMultiAttribute $addedEndpointSetID \
	-sources $addedTopology_1ID \
	-destinations $addedTopology_2ID
ixNet commit

#----------------------------------------------------------
# Edit traffic item parameters for the added traffic item
#----------------------------------------------------------

puts "\nConfiguring AppLibrary Traffic Item Basic Settings"
ixNet setMultiAttribute $addedProfileID \
	-objectiveValue 133 \
	-objectiveType throughputMbps \
	-enablePerIPStats True \
	-objectiveDistribution applyFullObjectiveToEachPort 
ixNet commit

#----------------------------------------------------------
# Setting flow percentages
#----------------------------------------------------------

puts "Setting AppLibrary flow percentages"
ixNet setAttribute $root/traffic/trafficItem:1/appLibProfile:1/appLibFlow:"Bandwidth_HTTP" -percentage 10
ixNet setAttribute $root/traffic/trafficItem:1/appLibProfile:1/appLibFlow:"Echo_UDP" -percentage 80
ixNet setAttribute $root/traffic/trafficItem:1/appLibProfile:1/appLibFlow:"Bandwidth_IMAPv4" -percentage 10
ixNet commit

#----------------------------------------------------------
# Configuring connection parameters
#----------------------------------------------------------

puts "Configuring connection parameters"
ixNet setAttribute $root/traffic/trafficItem:1/appLibProfile:1/appLibFlow:"Bandwidth_HTTP"/connection:1/parameter:"serverPort"/number -value 8080
ixNet setAttribute $root/traffic/trafficItem:1/appLibProfile:1/appLibFlow:"Echo_UDP"/connection:1/parameter:"enableTOS"/bool -value True
ixNet setAttribute $root/traffic/trafficItem:1/appLibProfile:1/appLibFlow:"Echo_UDP"/connection:1/parameter:"tosValue"/hex -value 0x1
ixNet commit

#----------------------------------------------------------
# Starting up protocols
#----------------------------------------------------------

puts "\nStarting all protocols and waiting for all ranges to be up"
ixNet exec startAllProtocols
after 5000
puts "Protocols started"

#----------------------------------------------------------
# Apply and start traffic
#----------------------------------------------------------
puts "\nApplying and starting AppLibrary Traffic"
ixNet exec applyApplicationTraffic $root/traffic
after 15000
ixNet exec startApplicationTraffic $root/traffic
after 2000
puts "AppLibrary traffic started"

#----------------------------------------------------------
# Clearing Statistics for AppLibrary Traffic
#----------------------------------------------------------

puts "\nWaiting 10 seconds before clearing AppLibrary statistics ..."
after 10000
ixNet exec clearAppLibraryStats
puts "Statistics have been cleared"

#----------------------------------------------------------
# Drilling down per IP 
#----------------------------------------------------------

after 10000
puts "Drilling down to reveal per IP address flow activity"

set viewsList [ixNet getL $root/statistics view]
set target [lindex $viewsList [lsearch [ixNet getL $root/statistics view] {::ixNet::OBJ-/statistics/view:"Application Traffic Item Statistics"}]]

puts "Configuring drill down per IP addresses"
ixNet setA $target/drillDown	-targetRowIndex 0
ixNet commit
ixNet setA $target/drillDown	-targetDrillDownOption "Application Traffic:Per IPs"
ixNet commit
ixNet setA $target/drillDown	-targetRow "Traffic Item=Traffic Item"
ixNet commit

puts "Launching the drill down per IP addresses view\n"
ixNet exec doDrillDown $target/drillDown
after 3000

puts "Refreshing statistics five times in a row"
set viewsList [ixNet getL $root/statistics view]
set target [lindex $viewsList [lsearch [ixNet getL $root/statistics view] {::ixNet::OBJ-/statistics/view:"Application Traffic Drill Down"}]]
for {set i 0} {$i<5} {incr i} {
	ixNet exec refresh $target
	after 5000
	puts "Statistics refreshed..."
}

#----------------------------------------------------------
# Pass Fail Evaluation
#----------------------------------------------------------

# selecting the "Application Traffic Item Statistics view from all the views"
set viewsList [ixNet getL [ixNet getRoot]/statistics view]
set targetView [lindex $viewsList [lsearch [ixNet getL [ixNet getRoot]/statistics view] {::ixNet::OBJ-/statistics/view:"Application Traffic Item Statistics"}]]

# selecting the columns based on the configured criteria
set targetColumnForHigh [lsearch [ixNet getA $targetView/page -columnCaptions] [lindex $PFCriteria_Higher 0]]
set targetColumnForLow [lsearch [ixNet getA $targetView/page -columnCaptions] [lindex $PFCriteria_Lower 0]]

# measuring the selected statistic
set measuredHigher [lindex [lindex [lindex [ixNet getA $targetView/page -rowValues] 0] 0] $targetColumnForHigh] 
set measuredLower [lindex [lindex [lindex [ixNet getA $targetView/page -rowValues] 0] 0] $targetColumnForLow] 

# comparing with pass fail condition - second item in the PFCriteria list 
if {$measuredHigher > [lindex $PFCriteria_Higher 1] && $measuredLower < [lindex $PFCriteria_Lower 1]} {
	set testResult "Test run is PASSED"
} else {
	set testResult "Test run is FAILED: pass fail conditions - $PFCriteria_Higher and $PFCriteria_Lower - configured in the start of the script are not met"
}

#----------------------------------------------------------
# Stop traffic 
#----------------------------------------------------------

after 20000
puts "Stopping AppLibrary traffic"
ixNet exec stopApplicationTraffic $root/traffic


#----------------------------------------------------------
# Test END
#----------------------------------------------------------

puts "##################"
puts $testResult
puts "##################"













