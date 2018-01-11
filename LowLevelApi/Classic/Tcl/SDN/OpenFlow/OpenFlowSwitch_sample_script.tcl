#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2014 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/10/2014 - Alka pattnaik - created sample                               #
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
#This script includes a section to configure a basic OpenFlow Controller in a  #
#back-to-back Ixia port.                                                       #
#This part can be used to bring up OpenFlow channel in the absence of real DUT #                                                                              
#    1. It will create Openflow Switch .                                       #
#       The switch has hosts configured.                                       #
#    2. Start the openflow protocol.                                           #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Trigger Host to HoSt Ping.                                             #
#    11. Stop all protocols.                                                   #
#######################################################################################################
#The Host and switch Connection with Controller is demonstrated below.                                #
#                                                                                                     #
#                                           |----------|                                              #
#                    _______________________|Controller|________________________                      #
#                   |                       |----------|                         |                    #
#                   |                             |                              |                    #
#					|							  |                              |                    #
#|-------|       |-----------|               |----------|                |----------|       |-------| #
#| Host 1| ----- | Sw 1      |2 -------------| Sw 2     |--------------1 | Sw 3      |2-----| Host 2| #
#|-------|       |-----------|               |----------|                |----------|       |-------| #
#					|                           | 3                         4|  3|                    #
#					|                           |____________________________|   |                    #
#					|____________________________________________________________|                    #
#######################################################################################################
# Ixia Software:                                                               #
#    IxOS      6.80 EB (6.80.1101.116)                                         #
#    IxNetwork 7.40 EB (7.40.929.3)                                            #
#                                                                              #
################################################################################

					
# Script Starts
puts "!!! Test Script Starts !!!"

# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.205.25.71
    set ixTclPort   8009
    set ports       {{10.205.28.81 1 5} { 10.205.28.81 1 6}}
}
puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.40\
    setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure Openflow as per the description #
#   given above                                                                #
################################################################################ 
puts "Adding 2 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vPort1 [lindex $vPorts 0]
set vPort2 [lindex $vPorts 1]

puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force
after 10000

############################################
# 2.For Switch Side configuration.
#############################################
puts "adding Interface for switch"
set interface2 [ixNet add $vPort2 interface]
set interface3 [ixNet add $vPort2 interface]
set interface4 [ixNet add $vPort2 interface]

ixNet setAttribute $interface2 -description sw1_1
ixNet setAttribute $interface3 -description sw1_2
ixNet setAttribute $interface4 -description sw1_3

puts "adding ipv4 to interfaces"
set ipv4_2 [ixNet add $interface2 ipv4]
set ipv4_3 [ixNet add $interface3 ipv4]
set ipv4_4 [ixNet add $interface4 ipv4]
ixNet commit

puts "adding ip for Switch1"
ixNet setAttribute $ipv4_2 -ip 65.1.1.101
set switchIp1 [ixNet getAttribute $ipv4_2 -ip]
ixNet setAttribute $ipv4_2 -maskWidth 24
ixNet setAttribute $ipv4_2 -gateway 65.1.1.1
ixNet commit

puts "adding ip for Switch2"
ixNet setAttribute $ipv4_3 -ip 65.1.1.102
set switchIp2 [ixNet getAttribute $ipv4_3 -ip]
ixNet setAttribute $ipv4_3 -maskWidth 24
ixNet setAttribute $ipv4_3 -gateway 65.1.1.1
ixNet commit

puts "adding ip for Switch3"
ixNet setAttribute $ipv4_4 -ip 65.1.1.103
set switchIp3 [ixNet getAttribute $ipv4_4 -ip]
ixNet setAttribute $ipv4_4 -maskWidth 24
ixNet setAttribute $ipv4_4 -gateway 65.1.1.1
ixNet commit

puts "enabling protocol interface"

ixNet setAttribute $interface2 -enabled true
ixNet setAttribute $interface3 -enabled true
ixNet setAttribute $interface4 -enabled true
ixNet commit

#adding Openflow switch
set protocol2 [ixNet getList $vPort2 protocols]
set openflow2 [ixNet getList $protocol2 openFlow]
ixNet setA $openflow2 -enabled true
ixNet commit
set switch1 [ixNet add $openflow2 device]
set switch2 [ixNet add $openflow2 device]
set switch3 [ixNet add $openflow2 device]
ixNet commit
set switch1 [lindex [ixNet remapIds $switch1] 0]
set switch2 [lindex [ixNet remapIds $switch2] 0]
set switch3 [lindex [ixNet remapIds $switch3] 0]

ixNet setAttribute $switch1 -enabled true
ixNet setAttribute $switch1 -enableVersion131 true
set swInterface1 [ixNet add $switch1 interface]
ixNet commit
ixNet setAttribute $switch1 -deviceRole switch
ixNet setAttribute $swInterface1 -protocolInterfaces $interface2
ixNet setAttribute $swInterface1 -enabled true
ixNet commit

ixNet setAttribute $switch2 -enabled true
ixNet setAttribute $switch2 -enableVersion131 true
set swInterface2 [ixNet add $switch2 interface]
ixNet commit
ixNet setAttribute $switch2 -deviceRole switch
ixNet setAttribute $swInterface2 -protocolInterfaces $interface3
ixNet setAttribute $swInterface2 -enabled true
ixNet commit

ixNet setAttribute $switch3 -enabled true
ixNet setAttribute $switch3 -enableVersion131 true
set swInterface3 [ixNet add $switch3 interface]
ixNet commit
ixNet setAttribute $switch3 -deviceRole switch
ixNet setAttribute $swInterface3 -protocolInterfaces $interface4
ixNet setAttribute $swInterface3 -enabled true
ixNet commit

ixNet setAttribute $swInterface1 -enableMultipleLogicalSwitch true
ixNet setAttribute $swInterface2 -enableMultipleLogicalSwitch true
ixNet setAttribute $swInterface3 -enableMultipleLogicalSwitch true
ixNet commit
set Sw1 [ixNet getList $swInterface1 switch]
set Sw2 [ixNet getList $swInterface2 switch]
set Sw3 [ixNet getList $swInterface3 switch]
ixNet commit
#puts "ixNet help ::ixNet::OBJ-/vport:2/protocols/openFlow/device:2/interface:1/switch:1"
#puts "[ixNet help ::ixNet::OBJ-/vport:2/protocols/openFlow/device:2/interface:1/switch:1]"
ixNet setAttribute $Sw1 -enable true
ixNet setAttribute $Sw2 -enable true
ixNet setAttribute $Sw3 -enable true
ixNet commit
ixNet setAttribute $Sw1 -description sw1
ixNet setAttribute $Sw2 -description sw2
ixNet setAttribute $Sw3 -description sw3
ixNet commit
ixNet setAttribute $Sw1 -datapathId 101
ixNet setAttribute $Sw2 -datapathId 102
ixNet setAttribute $Sw3 -datapathId 103
ixNet commit
set swOfCh1 [ixNet getList $Sw1 switchOfChannel]
set swOfCh2 [ixNet getList $Sw2 switchOfChannel]
set swOfCh3 [ixNet getList $Sw3 switchOfChannel]

#puts "ixNet help ::ixNet::OBJ-/vport:2/protocols/openFlow/device:2/interface:1/switch:1/switchOfChannel:1"
#puts "[ixNet help ::ixNet::OBJ-/vport:2/protocols/openFlow/device:2/interface:1/switch:1/switchOfChannel:1]"
ixNet setAttribute $swOfCh1 -enabled true
ixNet setAttribute $swOfCh1 -remoteIp 65.1.1.1
ixNet setAttribute $swOfCh2 -enabled true
ixNet setAttribute $swOfCh2 -remoteIp 65.1.1.1
ixNet setAttribute $swOfCh3 -enabled true
ixNet setAttribute $swOfCh3 -remoteIp 65.1.1.1
ixNet commit
puts "configuring Switch ports and hosts"
set sw1Ports_1 [ixNet getList $Sw1 switchPorts]
ixNet commit
ixNet setMultiAttribute $sw1Ports_1 \
		-connectionType host \
		-enabled true \
		-ethernetAddress "startValue\ =\ 00:00:11:00:00:01,stepValue\ =\ 00:00:00:00:00:01,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
		-portName "startValue\ =\ port1,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
		-portNumber "startValue\ =\ 1,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" 
ixNet commit

set sw1Host_1 [ixNet add $sw1Ports_1 switchHostRanges]
ixNet commit
ixNet setMultiAttribute $sw1Host_1 \
			-enabled true \
			-hostMacAddress "startValue\ =\ 00:00:00:00:05:01,stepValue\ =\ 00:00:00:00:00:01,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
			-hostStaticIpv4Address "startValue\ =\ 75.1.1.1,stepValue\ =\ 0.0.0.1,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
			-hostVlanid "startValue\ =\ 201,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 65535,incrementMode\ =\ increment" \
			-numberOfHostsPerPort 1
ixNet commit

set sw1Ports_2 [ixNet add $Sw1 switchPorts]
ixNet commit
ixNet setMultiAttribute $sw1Ports_2 \
	    -connectionType internalSwitch \
		-enabled true \
		-ethernetAddress "startValue\ =\ 00:00:12:00:00:01,stepValue\ =\ 00:00:00:00:00:01,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
		-portName "startValue\ =\ port2,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
		-portNumber "startValue\ =\ 2,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
		-transmissionDelay 10
ixNet commit

set sw1Ports_3 [ixNet add $Sw1 switchPorts]
ixNet commit
ixNet setMultiAttribute $sw1Ports_3 \
	    -connectionType internalSwitch \
		-enabled true \
		-ethernetAddress "startValue\ =\ 00:00:00:00:00:01,stepValue\ =\ 00:00:00:00:00:01,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
		-portName "startValue\ =\ port3,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
		-portNumber "startValue\ =\ 3,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
		-transmissionDelay 10
ixNet commit


set sw2Ports_1 [ixNet getList $Sw2 switchPorts]
ixNet commit			
ixNet setMultiAttribute $sw2Ports_1 \
			-connectionType internalSwitch \
			-enabled true \
			-ethernetAddress "startValue\ =\ 00:00:15:00:00:01,stepValue\ =\ 00:00:00:00:00:01,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
			-portName "startValue\ =\ port1,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
			-portNumber "startValue\ =\ 1,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
			-remoteSwitch $Sw1\
			-remoteSwitchPort $sw1Ports_2 \
			-transmissionDelay 10
ixNet commit

set sw2Ports_2 [ixNet add $Sw2 switchPorts]
ixNet commit
		ixNet setMultiAttribute $sw2Ports_2 \
			-connectionType internalSwitch \
			-enabled true \
			-ethernetAddress "startValue\ =\ 00:00:16:00:00:01,stepValue\ =\ 00:00:00:00:00:01,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
			-portName "startValue\ =\ port2,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
			-portNumber "startValue\ =\ 2,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
			-transmissionDelay 10
ixNet commit

set sw2Ports_3 [ixNet add $Sw2 switchPorts]
ixNet commit
ixNet setMultiAttribute $sw2Ports_3 \
	    -connectionType internalSwitch \
		-enabled true \
		-ethernetAddress "startValue\ =\ 00:00:00:00:00:01,stepValue\ =\ 00:00:00:00:00:01,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
		-portName "startValue\ =\ port3,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
		-portNumber "startValue\ =\ 3,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
		-transmissionDelay 10
ixNet commit

set sw3Ports_1 [ixNet getList $Sw3 switchPorts]
ixNet commit
		ixNet setMultiAttribute $sw3Ports_1 \
			-connectionType internalSwitch \
		    -enabled true \
			-ethernetAddress "startValue\ =\ 00:00:19:00:00:01,stepValue\ =\ 00:00:00:00:00:01,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
			-portName "startValue\ =\ port1,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
			-portNumber "startValue\ =\ 1,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
			-remoteSwitch $Sw2 \
			-remoteSwitchPort $sw2Ports_2 \
			-transmissionDelay 10
ixNet commit

set sw3Ports_2 [ixNet add $Sw3 switchPorts]
ixNet commit
ixNet setMultiAttribute $sw3Ports_2 \
			-connectionType host \
			-enabled true \
			-ethernetAddress "startValue\ =\ 00:00:1a:00:00:01,stepValue\ =\ 00:00:00:00:00:01,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
			-portName "startValue\ =\ port2,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
			-portNumber "startValue\ =\ 2,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" 			
ixNet commit

set sw3Host_1 [ixNet add $sw3Ports_2 switchHostRanges]
ixNet commit
ixNet setMultiAttribute $sw3Host_1 \
			-enabled true \
			-hostMacAddress "startValue\ =\ 00:00:00:00:05:02,stepValue\ =\ 00:00:00:00:00:01,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
			-hostStaticIpv4Address "startValue\ =\ 75.1.1.2,stepValue\ =\ 0.0.0.1,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
			-hostVlanid "startValue\ =\ 301,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 65535,incrementMode\ =\ increment" \
			-numberOfHostsPerPort 1
ixNet commit

set sw3Ports_3 [ixNet add $Sw3 "switchPorts"]
ixNet commit
ixNet setMultiAttribute $sw3Ports_3 \
			-connectionType internalSwitch \
			-enabled true \
			-ethernetAddress "startValue\ =\ 00:00:00:00:00:01,stepValue\ =\ 00:00:00:00:00:01,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
			-portName "startValue\ =\ port3,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
			-portNumber "startValue\ =\ 3,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
			-remoteSwitch $Sw1 \
			-remoteSwitchPort $sw1Ports_3 \
			-transmissionDelay 10
ixNet commit

set sw3Ports_4 [ixNet add $Sw3 switchPorts]
ixNet commit
ixNet setMultiAttribute $sw3Ports_4 \
			-connectionType internalSwitch \
			-enabled true \
			-ethernetAddress "startValue\ =\ 00:00:00:00:00:01,stepValue\ =\ 00:00:00:00:00:01,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
			-portName "startValue\ =\ port4,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
			-portNumber "startValue\ =\ 4,stepValue\ =\ 1,repeatCount\ =\ 1,wrapCount\ =\ 4294967295,incrementMode\ =\ increment" \
			-remoteSwitch $Sw2 \
			-remoteSwitchPort $sw2Ports_3 \
			-transmissionDelay 10
ixNet commit

ixNet setMultiAttribute $sw1Ports_2 \
            -remoteSwitch $Sw2 \
			-remoteSwitchPort $sw2Ports_1 
	
ixNet setMultiAttribute $sw1Ports_3 \
            -remoteSwitch $Sw3 \
			-remoteSwitchPort $sw3Ports_3 

ixNet setMultiAttribute $sw2Ports_2 \
            -remoteSwitch $Sw3 \
			-remoteSwitchPort $sw3Ports_1
			
ixNet setMultiAttribute $sw2Ports_3 \
            -remoteSwitch $Sw3 \
			-remoteSwitchPort $sw3Ports_4 
ixNet commit 


########################################################################################
# 3. Controller Side Configuraion. Do not use this part if you are working on a switch.
#########################################################################################

#adding Interface
set interface1 [ixNet add $vPort1 interface]
set ipv41 [ixNet add $interface1 ipv4]
ixNet commit

#adding ip
ixNet setA $ipv41 -ip 65.1.1.1
ixNet setA $ipv41 -maskWidth 24
ixNet setA $ipv41 -gateway 65.1.1.101
ixNet commit

#enabling protocol interface
ixNet setA $interface1 -enabled true
ixNet commit

#adding Openflow
set protocol1 [ixNet getList $vPort1 protocols]
set openflow1 [ixNet getList $protocol1 openFlow]
ixNet setA $openflow1 -enabled true
ixNet commit
set controller [ixNet add $openflow1 device]
ixNet commit
set controller [lindex [ixNet remapIds $controller] 0]

ixNet setAttribute $controller -enabled true
ixNet setAttribute $controller -enableVersion131 true
set ofInterface [ixNet add $controller interface]
ixNet commit
ixNet setAttribute $ofInterface -protocolInterfaces $interface1
ixNet setAttribute $ofInterface -enabled true
ixNet commit
set ofch1 [ixNet add $ofInterface ofChannel]
set ofch2 [ixNet add $ofInterface ofChannel]
set ofch3 [ixNet add $ofInterface ofChannel]
ixNet commit
#puts "ixNet help ::ixNet::OBJ-/vport:1/protocols/openFlow/device:1/interface:1/ofChannel:1"
#puts "[ixNet help ::ixNet::OBJ-/vport:1/protocols/openFlow/device:1/interface:1/ofChannel:1]"
ixNet setAttribute $ofch1 -remoteIp $switchIp1
ixNet setAttribute $ofch1 -enabled true
ixNet commit
ixNet setAttribute $ofch2 -remoteIp $switchIp2
ixNet setAttribute $ofch2 -enabled true
ixNet commit
ixNet setAttribute $ofch3 -remoteIp $switchIp3
ixNet setAttribute $ofch3 -enabled true
ixNet commit

 
##########################################################
#adding tables and flow ranges 
set controllerTable1 [ixNet add $ofch1 controllerTables]
set controllerTable2 [ixNet add $ofch2 controllerTables]
set controllerTable3 [ixNet add $ofch3 controllerTables]
ixNet commit

ixNet setAttribute $controllerTable1 \
     -enabled true \
	 -tableId 0 
ixNet commit
ixNet setAttribute $controllerTable2 \
     -enabled true \
	 -tableId 0 
ixNet commit
ixNet setAttribute $controllerTable3 \
     -enabled true \
	 -tableId 0 
ixNet commit

#########################################################
#Adding flow ranges, Instructions and instruction actions
#########################################################
set ctrTableFlowRanges1 [ixNet add $controllerTable1 controllerTableFlowRanges]
set ctrTableFlowRanges2 [ixNet add $controllerTable1 controllerTableFlowRanges]
ixNet commit
#puts "ixNet help ::::ixNet::OBJ-/vport:1/protocols/openFlow/device:1/interface:1/ofChannel:1/controllerTables:1/controllerTableFlowRanges:1"
#puts "[ixNet help ::::ixNet::OBJ-/vport:1/protocols/openFlow/device:1/interface:1/ofChannel:1/controllerTables:1/controllerTableFlowRanges:1]"
ixNet setAttribute $ctrTableFlowRanges1 -enabled true 
ixNet setMultiAttribute $ctrTableFlowRanges1 \
     -ethernetDestination "startValue\ =\ 00:00:00:00:05:01,stepValue\ =\ 00:00:00:00:00:00,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment"  \
	 -ethernetSource "\"*\"" \
	 -ethernetSourceMask "FF\ FF\ FF\ FF\ FF\ FF\ " 
ixNet commit
ixNet setAttribute $ctrTableFlowRanges2 -enabled true 
ixNet setMultiAttribute $ctrTableFlowRanges2 \
     -ethernetDestination "startValue\ =\ 00:00:00:00:05:02,stepValue\ =\ 00:00:00:00:00:00,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
	 -ethernetSource "\"*\"" \
	 -ethernetSourceMask "FF\ FF\ FF\ FF\ FF\ FF\ " \
	 -vlanId "startValue\ =\ 4096,stepValue\ =\ 0,repeatCount\ =\ 1,wrapCount\ =\ 65535,incrementMode\ =\ increment" \
	 -vlanMatchType withVlanTag 
ixNet commit

set ctrTableFlowRanges3 [ixNet add $controllerTable2 controllerTableFlowRanges]
set ctrTableFlowRanges4 [ixNet add $controllerTable2 controllerTableFlowRanges]
ixNet commit
ixNet setAttribute $ctrTableFlowRanges3 -enabled true 
ixNet setMultiAttribute $ctrTableFlowRanges3 \
     -ethernetDestination "startValue\ =\ 00:00:00:00:05:01,stepValue\ =\ 00:00:00:00:00:00,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
	 -ethernetSource "\"*\"" \
	 -ethernetSourceMask "FF\ FF\ FF\ FF\ FF\ FF\ " 
ixNet commit
ixNet setAttribute $ctrTableFlowRanges4 -enabled true 
ixNet setMultiAttribute $ctrTableFlowRanges4 \
     -ethernetDestination "startValue\ =\ 00:00:00:00:05:02,stepValue\ =\ 00:00:00:00:00:00,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
	 -ethernetSource "\"*\"" \
	 -ethernetSourceMask "FF\ FF\ FF\ FF\ FF\ FF\ " 
ixNet commit

set ctrTableFlowRanges5 [ixNet add $controllerTable3 controllerTableFlowRanges]
set ctrTableFlowRanges6 [ixNet add $controllerTable3 controllerTableFlowRanges]
ixNet commit
ixNet setAttribute $ctrTableFlowRanges5 -enabled true 
ixNet setMultiAttribute $ctrTableFlowRanges5 \
     -ethernetDestination "startValue\ =\ 00:00:00:00:05:02,stepValue\ =\ 00:00:00:00:00:00,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
	 -ethernetSource "\"*\"" \
	 -ethernetSourceMask "FF\ FF\ FF\ FF\ FF\ FF\ " 
ixNet commit
ixNet setAttribute $ctrTableFlowRanges6 -enabled true 
ixNet setMultiAttribute $ctrTableFlowRanges6 \
     -ethernetDestination "startValue\ =\ 00:00:00:00:05:01,stepValue\ =\ 00:00:00:00:00:00,repeatCount\ =\ 1,wrapCount\ =\ 1000000,incrementMode\ =\ increment" \
	 -ethernetSource "\"*\"" \
	 -ethernetSourceMask "FF\ FF\ FF\ FF\ FF\ FF\ " \
	 -vlanMatchType specificVlanTag  
ixNet commit
ixNet setMultiAttribute $ctrTableFlowRanges6 \
     -vlanId "startValue\ =\ 301,stepValue\ =\ 0,repeatCount\ =\ 1,wrapCount\ =\ 65535,incrementMode\ =\ increment" \
     -vlanIdMask "FF\ FF\ " 
ixNet commit

#############################################
#Set up the instructins and instruction action
##############################################

set instruction1 [ixNet add $ctrTableFlowRanges1 instructions]
ixNet setMultiAttribute $instruction1 \
			-experimenterData {} \
			-instructionType applyActions \
			-metadataInHex 0 
ixNet commit

set instructionActions1_1 [ixNet add $instruction1 instructionActions]
ixNet setAttribute $instructionActions1_1 -actionType setVlanId
ixNet setAttribute $instructionActions1_1 -vlanId 201
ixNet commit
			
set instructionActions1_2 [ixNet add $instruction1 instructionActions]
ixNet setAttribute $instructionActions1_2 -actionType output
ixNet commit
ixNet setAttribute $instructionActions1_2 -outputPort 1
ixNet commit

set instruction2 [ixNet add $ctrTableFlowRanges2 instructions]
ixNet setMultiAttribute $instruction2 \
			-experimenterData {} \
			-instructionType applyActions \
			-metadataInHex 0 
ixNet commit

set instructionActions2_1 [ixNet add $instruction2 instructionActions]
ixNet setAttribute $instructionActions2_1 -actionType output
ixNet commit
ixNet setAttribute $instructionActions2_1 -outputPort 2
ixNet commit

set instruction3 [ixNet add $ctrTableFlowRanges3 instructions]
ixNet setMultiAttribute $instruction3 \
			-experimenterData {} \
			-instructionType applyActions \
			-metadataInHex 0 
ixNet commit

set instructionActions3_1 [ixNet add $instruction3 instructionActions]
ixNet setAttribute $instructionActions3_1 -actionType output
ixNet commit
ixNet setAttribute $instructionActions3_1 -outputPort 1
ixNet commit


set instruction4 [ixNet add $ctrTableFlowRanges4 instructions]
ixNet setMultiAttribute $instruction4 \
			-experimenterData {} \
			-instructionType applyActions \
			-metadataInHex 0 
ixNet commit
set instructionActions4_1 [ixNet add $instruction4 instructionActions]
ixNet setAttribute $instructionActions4_1 -actionType output
ixNet commit
ixNet setAttribute $instructionActions4_1 -outputPort 2
ixNet commit

set instruction5 [ixNet add $ctrTableFlowRanges5 instructions]
ixNet setMultiAttribute $instruction5 \
			-experimenterData {} \
			-instructionType applyActions \
			-metadataInHex 0 
ixNet commit

set instructionActions5_1 [ixNet add $instruction5 instructionActions]
ixNet setAttribute $instructionActions5_1 -actionType setVlanId
ixNet commit
ixNet setAttribute $instructionActions5_1 -vlanId 301
ixNet commit
set instructionActions5_2 [ixNet add $instruction5 instructionActions]
ixNet setAttribute $instructionActions5_2 -actionType output
ixNet commit
ixNet setAttribute $instructionActions5_2 -outputPort 2
ixNet commit

set instruction6 [ixNet add $ctrTableFlowRanges6 instructions]
ixNet setMultiAttribute $instruction6 \
			-experimenterData {} \
			-instructionType applyActions \
			-metadataInHex 0 
ixNet commit

set instructionActions6_1 [ixNet add $instruction6 instructionActions]
ixNet setAttribute $instructionActions6_1 -actionType output
ixNet commit
ixNet setAttribute $instructionActions6_1 -outputPort 1
ixNet commit

###################################################################################
# 4. Starting all protocols
###################################################################################
puts "starting all protocols and waiting 45 sec ..."
ixNet exec startAllProtocols
after 45000

################################################################################
# 5. Retrieve protocol aggregated statistics.
################################################################################
puts "Fetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"OpenFlow Switch Aggregated Statistics"/page}
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

puts "Fetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"OpenFlow Host Aggregated Statistics"/page}
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
###################################################################################
# 6. Get Switch Of channel Learned Info
#####################################################################################
puts "Fetching Openflow Channel Learned Info"
set learnedInfo_Switch ${vPort2}/protocols/openFlow/switchLearnedInformation
after 1000
#puts "ixNet help ::ixNet::OBJ-/vport:2/protocols/openFlow/switchLearnedInformation:1"
#puts "[ixNet help ::ixNet::OBJ-/vport:2/protocols/openFlow/switchLearnedInformation:1]"
ixNet exec refreshOfChannelLearnedInformation $learnedInfo_Switch
after 1000
ixNet exec clearRecordsForTrigger $learnedInfo_Switch
set ofChannelSwLearnedInfo [ixNet getList $learnedInfo_Switch ofChannelSwitchLearnedInfo]
after 2000
set ofChannelSw1_LearnedInfo [lindex $ofChannelSwLearnedInfo 0]
#set ofChannelSw2_LearnedInfo [lindex $ofChannelSwLearnedInfo 1]
#set ofChannelSw3_LearnedInfo [lindex $ofChannelSwLearnedInfo 2]
set localIp [ixNet getA $ofChannelSw1_LearnedInfo -localIp]
set version [ixNet getA $ofChannelSw1_LearnedInfo -negotiatedVersion]
set	remoteIp [ixNet getA $ofChannelSw1_LearnedInfo -remoteIp]
set dataPathId [ixNet getA $ofChannelSw1_LearnedInfo -dataPathId]
set numberOfPorts [ixNet getA $ofChannelSw1_LearnedInfo -numberOfPorts]
set sessionType  [ixNet getA $ofChannelSw1_LearnedInfo -sessionType]
puts "Got : localIp   dataPathId   version   remoteIp     sessionType   numberOfPorts "
puts "$localIp        $dataPathId  $version  $remoteIp    $sessionType	$numberOfPorts"

# Trigger the host LInfo
#####################################################################################
set hostLI [ixNet getList $openflow2 hostTopologyLearnedInformation]
set hostLItrigAttrib [ixNet getList $hostLI switchHostRangeLearnedInfoTriggerAttributes]

puts "Sending trigger for ping request from sw1Host1 to sw3Host1."
ixNet setAttr $hostLItrigAttrib -sourceHostList $sw1Host_1
ixNet setAttr $hostLItrigAttrib -destinationHostList $sw3Host_1
ixNet setAttr $hostLItrigAttrib -packetType ping
ixNet setAttr $hostLItrigAttrib -responseTimeout 5000
ixNet commit
ixNet exec refreshHostRangeLearnedInformation $hostLI
puts "Trigger sent .. waiting 15 sec"
after 15000

set hostLIhostRangeLIs [ixNet getList $hostLI switchHostRangeLearnedInfo]
set hostLInum [llength $hostLIhostRangeLIs]
puts "Received $hostLInum entries in host topology learned info."

set hostLIhostRangeLI [lindex $hostLIhostRangeLIs 0]
puts "Checking ping request for single path."
set dstMAC [ixNet getAttr $hostLIhostRangeLI -destinationHostMac]
set dstIP [ixNet getAttr $hostLIhostRangeLI -destinationHostIpv4Address ]
set srcMAC [ixNet getAttr $hostLIhostRangeLI -sourceHostMac]
set srcIP [ixNet getAttr $hostLIhostRangeLI -sourceHostIpv4Address]
set status [ixNet getAttr $hostLIhostRangeLI -status]
puts "Got : dstMAC    dstIP    srcMAC    srcIP    status"
puts "$dstMAC    $dstIP    $srcMAC    $srcIP    $status"

################################################################################
# 7. Stop all protocols
################################################################################
ixNet exec stopAllProtocols
puts "!!! Test Script Ends !!!"