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
# The script is not a standard commercial product offered by Ixia Keysight and #
# have     																	   #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia Keysight and/or by the user and/or by a third party)] shall at  #
# all times 																   #
# remain the property of Ixia Keysight.                                        #
#                                                                              #
# Ixia Keysight does not warrant (i) that the functions contained in the script#
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND Ixia Keysight#
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL Ixia Keysight BE LIABLE FOR ANY DAMAGES RESULTING FROM OR  #
# ARISING   																   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF Ixia Keysight HAS BEEN ADVISED OF THE          #
# POSSIBILITY OF  SUCH DAMAGES IN ADVANCE.                                     #
# Ixia Keysight will not be required to provide any software maintenance or    #
# support services of any kind (e.g. any error corrections) in connection with #
# script or any part thereof. The user acknowledges that although Ixia Keysight# 
# may     																	   #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia Keysight to  #
# provide any additional maintenance or support services.                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    Script  will create following:                                            #
#    1. Create PPPoX Client and server                                         #
#    2. Modify various parameters:											   #
#		Enable MRRU Negotiation												   #
#		Multilink MRRU size													   #
#		ML-PPP Endpoint Discriminator Option								   #
#		Endpoint discriminator class_ip_address                                #
#		Internet Protocol Address                                              #
#		MAC address                                                            #
#	 3. Start 
#	 4. Stop                                                          	       #	   					                            
#                                                                              #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.39.65.1
    set ixTclPort   8009
    set ports       {{10.39.64.117 2 9} {10.39.64.117 2 10}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.50

puts "Creating a new config"
ixNet exec newConfig

puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vport1 [lindex $vPorts 0]
set vport2 [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

after 5000

puts "*****************************************************"
puts "Create  topology with PPPoX client and PPPoX Client, "
puts "*****************************************************"
puts "Adding 2 topologies"
ixNet add 	[ixNet getRoot] topology -vports $vport1
ixNet add 	[ixNet getRoot] topology -vports $vport2
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 				[lindex $topologies 0]
set topo2 				[lindex $topologies 1]

puts "Adding 2 device groups, one for the client, \
	  multiplier is set to 1 and one for the server, multiplier is set to 1"
ixNet add $topo1 deviceGroup -multiplier 10
ixNet add $topo2 deviceGroup -multiplier 1
ixNet commit

set t1dev1 				[ixNet getList $topo1 deviceGroup]
set t2dev1 				[ixNet getList $topo2 deviceGroup]

# naming the topologies and the device groups
ixNet setAttr $topo1  -name "PPP Topology-1"
ixNet setAttr $topo2  -name "PPP Topology-2"
ixNet setAttr $t1dev1 -name "Clients"
ixNet setAttr $t2dev1 -name "Servers"
ixNet commit

puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet commit
set mac1 				[ixNet getList $t1dev1 ethernet]
set mac2 				[ixNet getList $t2dev1 ethernet]


puts "Adding PPP Server and Client stack"
set ppp_client 			[ixNet add $mac1 pppoxclient]
set ppp_server 			[ixNet add $mac2 pppoxserver]
ixNet commit

puts "Setting PPP Server Sessions Count to 1"
ixNet setA $ppp_server -sessionsCount 10

set root 				[ixNet getRoot]
set topo 				[ixNet getL $root topology ]
set device_group 		[ixNet getL [lindex $topo 0] deviceGroup]
set eth 				[ixNet getL $device_group ethernet]
set pppox_client 		[ixNet getL $eth pppoxclient]
set device_group_server [ixNet getL [lindex $topo 1] deviceGroup]
set eth_server 			[ixNet getL $device_group_server ethernet]
set pppox_server 		[ixNet getL $eth_server pppoxserver]


puts "*****************************************************"
puts "Set values to ML-PPP Parameters for PPPoX Client     "
puts "*****************************************************"

puts "1. Configure ML-PPP with ML-PPP Endpoint discriminator option as True"
set end_point_negotiation [ixNet getAttribute $pppox_client -endpointDiscNegotiation]
set end_point_negotiation_val [ixNet add $end_point_negotiation "singleValue"]
ixNet setMultiAttribute $end_point_negotiation_val \
	-value true
ixNet commit


puts "2. Configure ML-PPP with Enable MRRU Negotiation as true"
set mrru_negotiation 	 [ixNet getAttribute $pppox_client -mrruNegotiation]
set mrru_negotiation_val [ixNet add $mrru_negotiation "singleValue"]
ixNet setMultiAttribute $mrru_negotiation_val \
	-value true
ixNet commit

puts "3. Configure ML-PPP with MAC address"
set mlpp_mac_address 	 [ixNet getAttribute $pppox_client -mlpppMACAddress]
set mlpp_mac_address_val [ixNet add $mlpp_mac_address "counter"]
ixNet setMultiAttribute $mlpp_mac_address_val \
	-step 00:00:00:00:00:01 \
	-start 11:23:01:10:22:21 \
	-direction increment
ixNet commit

puts "4. Configure ML-PPP with IP address"
set mlppp_ip_address  	 [ixNet getAttribute $pppox_client -mlpppIPAddress]
set mlppp_ip_address_val [ixNet add $mlppp_ip_address "counter"]
ixNet setMultiAttribute $mlppp_ip_address_val \
	-step 0.0.0.1 \
	-start 12.2.3.4 \
	-direction increment
ixNet commit

puts "5. Configure ML-PPP with End point discriminator class"
# Different End point discriminator class values are:
#a. ipaddress
#b. nullclass
#c. macaddress

set end_point_disc 		[ixNet getAttribute $pppox_client -endpointDiscriminatorClass]
set end_point_disc_val 	[ixNet add $end_point_disc "singleValue"]
ixNet setMultiAttribute $end_point_disc_val \
	-value macaddress
ixNet commit


puts "6. Configure ML-PPP with MRRU size"
set mrru 	 			 [ixNet getAttribute $pppox_client -mrru]
set mrru_val 			 [ixNet add $mrru "singleValue"]
ixNet setMultiAttribute $mrru_val \
	-value 1487
ixNet commit



puts "*****************************************************"
puts "Set values to ML-PPP Parameters for PPPoX Server     "
puts "*****************************************************"

puts "1. Configure PPPoX Server  ML-PPP with ML-PPP Endpoint discriminator option as True"
set end_point_negotiation [ixNet getAttribute $pppox_server -endpointDiscNegotiation]
set end_point_negotiation_val [ixNet add $end_point_negotiation "singleValue"]
ixNet setMultiAttribute $end_point_negotiation_val \
	-value true
ixNet commit

puts "2. Configure PPPoX Server  ML-PPP with Enable MRRU Negotiation as true"
set mrru_negotiation 	 [ixNet getAttribute $pppox_server -mrruNegotiation]
set mrru_negotiation_val [ixNet add $mrru_negotiation "singleValue"]
ixNet setMultiAttribute $mrru_negotiation_val \
	-value true
ixNet commit

puts "3. Configure PPPoX Server  ML-PPP with MAC address"
set mlpp_mac_address 	 [ixNet getAttribute $pppox_server -mlpppMACAddress]
set mlpp_mac_address_val [ixNet add $mlpp_mac_address "counter"]
ixNet setMultiAttribute $mlpp_mac_address_val \
	-step 00:00:00:00:00:01 \
	-start 21:23:01:10:22:21 \
	-direction increment
ixNet commit

puts "4. Configure PPPoX Server  ML-PPP with IP address"
set mlppp_ip_address 	 [ixNet getAttribute $pppox_server -mlpppIPAddress]
set mlppp_ip_address_val [ixNet add $mlppp_ip_address "counter"]
ixNet setMultiAttribute $mlppp_ip_address_val \
	-step 0.0.0.1 \
	-start 14.2.3.4 \
	-direction increment
ixNet commit

puts "5. Configure  PPPoX Server  ML-PPP with End point discriminator class"
# Different End point discriminator class values are:
#a. ipaddress
#b. nullclass
#c. macaddress

set end_point_disc 	   	[ixNet getAttribute $pppox_server -endpointDiscriminatorClass]
set end_point_disc_val  [ixNet add $end_point_disc "singleValue"]
ixNet setMultiAttribute $end_point_disc_val \
	-value ipaddress
ixNet commit


puts "6. Configure PPPoX Server  ML-PPP with MRRU size"
set mrru 				[ixNet getAttribute $pppox_server -mrru]
set mrru_val [ixNet add $mrru "singleValue"]
ixNet setMultiAttribute $mrru_val \
	-value 1412
ixNet commit

puts "Starting PPP Server"
ixNet exec start $pppox_server
puts "Wait 5 sec"
after 5000

puts "Starting PPP Clients"
ixNet exec start $pppox_client

puts "Wait 60 seconds"
after 60000

puts "Stopping the clients"
ixNet exec stop $t1dev1
after 5000
puts "Stopping the servers"
ixNet exec stop $t2dev1
after 10000

puts "Unassigning ports..."
ixTclNet::UnassignPorts
puts "Done... Ports are unassigned..."
puts ""

puts "Cleaning up IxNetwork..."
ixNet exec newConfig
ixNet disconnect

puts "Done... IxNetwork session is closed..."
puts ""
puts "!!! TEST DONE !!!"

return 0





