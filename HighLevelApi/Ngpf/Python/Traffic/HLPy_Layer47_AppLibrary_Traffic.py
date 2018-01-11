################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    01/20/2014 - Andrei Zamisnicu - created sample                            #
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
#   The script below walks through the workflow of an AppLibrary end to end    #	
#	test, using the below steps:											   #	
#		1. Connection to the chassis, IxNetwork Tcl Server 					   #
#		2. Topology configuration											   #
#		3. Configure trafficItem 1 for Layer 4-7 AppLibrary Profile			   #	
#		4. Configure trafficItem 2 for Layer 4-7 AppLibrary Profile			   #
#		5. Start protocols													   #	
#		6. Apply and run AppLibrary traffic									   #
#		7. Drill down per IP addresses during traffic run					   #
#		8. Stop Traffic.													   #	
#																			   #	
#                                                                              #
################################################################################

################################################################################
# Utils																		   #
################################################################################

# Libraries to be included
# package require Ixia
# Other procedures used in the script, that do not use HL API configuration/control procedures

from pprint import pprint
import os
import sys
import time

# Append paths to python APIs (Linux and Windows)

sys.path.append('C:/Program Files (x86)/Ixia/hltapi/4.97.0.2/TclScripts/lib/hltapi/library/common/ixiangpf/python')
sys.path.append('C:/Program Files (x86)/Ixia/IxNetwork/7.50.0.8EB/API/Python')

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError

ixiatcl = IxiaTcl()
ixiahlt = IxiaHlt(ixiatcl)
ixiangpf = IxiaNgpf(ixiahlt)


try:
	ErrorHandler('', {})
except (NameError,):
	def ErrorHandler(cmd, retval):
		global ixiatcl
		err = ixiatcl.tcl_error_info()
		log = retval['log']
		additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
		raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)

################################################################################
# Connection to the chassis, IxNetwork Tcl Server                 			   #
################################################################################

# This section should contain the connect procedure values (device ip, port list etc) and, of course, the connect procedure		

chassis_ip = '10.205.23.38'
tcl_server = '10.205.23.38'
ixnetwork_tcl_server = 'localhost:8449'
portsList = ['1/3','1/4','1/5','1/6']

connect_status = ixiangpf.connect(
    reset 				=			1,
    device				=			chassis_ip,
    port_list			=			portsList,
    ixnetwork_tcl_server=			ixnetwork_tcl_server,
    tcl_server			=			tcl_server,
)

if connect_status['status'] != '1':
    ErrorHandler('connect', connect_status)

port_handle = connect_status['vport_list']

ports = connect_status['vport_list'].split()

port_1 = port_handle.split(' ')[0]
port_2 = port_handle.split(' ')[1]
port_3 = port_handle.split(' ')[2]
port_4 = port_handle.split(' ')[3]

port_handle = ('port_1','port_2','port_3','port_4')


	
	
################################################################################
# Configure Topology 1, Device Group 1                                         #
################################################################################

topology_1_status = ixiangpf.topology_config(
        topology_name     = 'Topology 1',
        port_handle       = port_1,
    )
topology_1_handle = topology_1_status['topology_handle']

if topology_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', topology_1_status)

device_group_1_status = ixiangpf.topology_config(
        topology_handle			    = topology_1_handle,
        device_group_name			= 'Device Group 1',
        device_group_multiplier	    = "45",
        device_group_enabled		= "1",
    )
	
if device_group_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', device_group_1_status)
	
deviceGroup_1_handle = device_group_1_status['device_group_handle']


################################################################################
# Configure protocol interfaces for first topology                             #
################################################################################

multivalue_1_status = ixiangpf.multivalue_config(
        pattern                ="counter",
        counter_start          ="00.11.01.00.00.01",
        counter_step           ="00.00.00.00.00.01",
        counter_direction      ="increment",
        nest_step              ="00.00.01.00.00.00",
        nest_owner             =topology_1_handle,
        nest_enabled           ="1",
    )
	
if multivalue_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', multivalue_1_status)

multivalue_1_handle = multivalue_1_status ['multivalue_handle']


ethernet_1_status =ixiangpf.interface_config(
        protocol_name                ="Ethernet 1"               ,
        protocol_handle              =deviceGroup_1_handle      ,
        mtu                          ="1500"                       ,
        src_mac_addr                 =multivalue_1_handle       ,
        vlan                         ="0"                          ,
        vlan_id                      ="1"                          ,
        vlan_id_step                 ="0"                          ,
        vlan_id_count                ="1"                          ,
        vlan_tpid                    ="0x8100"                     ,
        vlan_user_priority           ="0"                          ,
        vlan_user_priority_step      ="0"                          ,
        use_vpn_parameters           ="0"                          ,
        site_id                      ="0"                          ,
    )
	
if ethernet_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ethernet_1_status)

ethernet_1_handle = ethernet_1_status['ethernet_handle']


multivalue_2_status = ixiangpf.multivalue_config(
        pattern                ="counter"                 ,
        counter_start          ="100.1.0.1"               ,
        counter_step           ="0.0.0.1"                 ,
        counter_direction      ="increment"               ,
        nest_step              ="0.1.0.0"                 ,
        nest_owner             =topology_1_handle      ,
        nest_enabled           ="1"                       ,
    )
	
if multivalue_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', multivalue_2_status)	

multivalue_2_handle = multivalue_2_status['multivalue_handle']


multivalue_3_status = ixiangpf.multivalue_config(
        pattern                ="counter"                 ,
        counter_start          ="101.1.0.1"               ,
        counter_step           ="255.255.255.255"         ,
        counter_direction      ="decrement"               ,
        nest_step              ="0.0.0.1"                 ,
        nest_owner             =topology_1_handle      ,
        nest_enabled           ="0"                       ,
    )
	
if multivalue_3_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', multivalue_3_status)	

multivalue_3_handle = multivalue_3_status['multivalue_handle']


ipv4_1_status = ixiangpf.interface_config(
        protocol_name                ="IPv4 1"                  ,
        protocol_handle              =ethernet_1_handle        ,
        ipv4_resolve_gateway         ="1"                         ,
        ipv4_manual_gateway_mac      ="00.00.00.00.00.01"         ,
        gateway                      =multivalue_3_handle      ,
        intf_ip_addr                 =multivalue_2_handle      ,
        netmask                      ="255.255.255.0"             ,
    )
	
if ipv4_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ipv4_1_status)	
	
ipv4_1_handle =ipv4_1_status['ipv4_handle']


################################################################################
# Configure Topology 2, Device Group 2                                         #
################################################################################

topology_2_status =ixiangpf.topology_config(
        topology_name      ="Topology 2"                            ,
        port_handle        =port_2							        ,
    )

if topology_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', topology_2_status)
	
topology_2_handle = topology_2_status['topology_handle']


device_group_2_status = ixiangpf.topology_config(
        topology_handle              =topology_2_handle      ,
        device_group_name            ="Device Group 2"        ,
        device_group_multiplier      ="45"	                  ,
        device_group_enabled         ="1"                       ,
    )

if device_group_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', device_group_2_status)

deviceGroup_2_handle = device_group_2_status['device_group_handle']

################################################################################
# Configure protocol interfaces for second topology                             #
################################################################################

multivalue_4_status =ixiangpf.multivalue_config(
        pattern               ="counter"                 ,
        counter_start         ="00.12.01.00.00.01"       ,
        counter_step          ="00.00.00.00.00.01"       ,
        counter_direction     ="increment"               ,
        nest_step             ="00.00.01.00.00.00"       ,
        nest_owner            =topology_2_handle      ,
        nest_enabled          ="1"                       ,
    )
	
if multivalue_4_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', multivalue_4_status)

multivalue_4_handle = multivalue_4_status['multivalue_handle']


ethernet_2_status = ixiangpf.interface_config(
        protocol_name                ="Ethernet 2"               ,
        protocol_handle              =deviceGroup_2_handle      ,
        mtu                          ="1500"                      ,
        src_mac_addr                 =multivalue_4_handle       ,
        vlan                         ="0"                          ,
        vlan_id                      ="1"                          ,
        vlan_id_step                 ="0"                          ,
        vlan_id_count                ="1"                          ,
        vlan_tpid                    ="0x8100"                     ,
        vlan_user_priority           ="0"                          ,
        vlan_user_priority_step      ="0"                          ,
        use_vpn_parameters           ="0"                          ,
        site_id                      ="0"                          ,
    )
if ethernet_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ethernet_2_status)
	
ethernet_2_handle=ethernet_2_status['ethernet_handle']


multivalue_5_status = ixiangpf.multivalue_config(
        pattern                ="counter"                 ,
        counter_start          ="101.1.0.1"               ,
        counter_step           ="0.0.0.1"                 ,
        counter_direction      ="increment"               ,
        nest_step              ="0.1.0.0"                 ,
        nest_owner             =topology_2_handle      ,
        nest_enabled           ="1"                       ,
    )
	
if multivalue_5_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', multivalue_5_status)
	
multivalue_5_handle = multivalue_5_status['multivalue_handle']


multivalue_6_status = ixiangpf.multivalue_config(
        pattern                ="counter"                 ,
        counter_start          ="100.1.0.1"               ,
        counter_step           ="255.255.255.255"         ,
        counter_direction      ="decrement"               ,
        nest_step              ="0.0.0.1"                 ,
        nest_owner             =topology_2_handle      ,
        nest_enabled           ="0"                       ,
    )	
if multivalue_6_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', multivalue_6_status)
	
multivalue_6_handle = multivalue_6_status['multivalue_handle']


ipv4_2_status = ixiangpf.interface_config(
        protocol_name                ="IPv4 2"                  ,
        protocol_handle              =ethernet_2_handle        ,
        ipv4_resolve_gateway         ="1"                         ,
        ipv4_manual_gateway_mac      ="00.00.00.00.00.01"         ,
        gateway                      =multivalue_6_handle      ,
        intf_ip_addr                 =multivalue_5_handle      ,
        netmask                      ="255.255.255.0"             ,
    )
	
if ipv4_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ipv4_2_status)

ipv4_2_handle = ipv4_2_status['ipv4_handle']



################################################################################
# Configure Topology 3, Device Group 3                                         #
################################################################################

topology_3_status = ixiangpf.topology_config(
        topology_name      ="Topology 3"                          ,
        port_handle        =port_3								  ,
    )	
	
if topology_3_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', topology_3_status)

topology_3_handle = topology_3_status['topology_handle']


device_group_3_status = ixiangpf.topology_config(
        topology_handle              =topology_3_handle      ,
        device_group_name            ="Device Group3"         ,
        device_group_multiplier      ="45"                      ,
        device_group_enabled         ="1"                       ,
    )
	
if device_group_3_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', device_group_3_status)
	
deviceGroup_3_handle = device_group_3_status['device_group_handle']

################################################################################
# Configure protocol interfaces for the third topology                         #
################################################################################

multivalue_7_status = ixiangpf.multivalue_config(
        pattern                ="counter"                 ,
        counter_start          ="00.13.01.00.00.01"       ,
        counter_step           ="00.00.00.00.00.01"       ,
        counter_direction      ="increment"               ,
        nest_step              ="00.00.01.00.00.00"       ,
        nest_owner             =topology_3_handle      ,
        nest_enabled           ="1"                       ,
    )
	
	
if multivalue_7_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', multivalue_7_status)

multivalue_7_handle = multivalue_7_status['multivalue_handle']


ethernet_3_status = ixiangpf.interface_config(
        protocol_name                ="Ethernet 3"               ,
        protocol_handle              =deviceGroup_3_handle      ,
        mtu                          ="1500"                       ,
        src_mac_addr                 =multivalue_7_handle       ,
        src_mac_addr_step            ="00.00.00.00.00.00"          ,
        vlan                         ="0"                          ,
        vlan_id                      ="1"                          ,
        vlan_id_step                 ="0"                          ,
        vlan_id_count                ="1"                          ,
        vlan_tpid                    ="0x8100"                     ,
        vlan_user_priority           ="0"                          ,
        vlan_user_priority_step      ="0"                          ,
        use_vpn_parameters           ="0"                          ,
        site_id                      ="0"                          ,
    )
	
if ethernet_3_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ethernet_3_status)
	
ethernet_3_handle = ethernet_3_status ['ethernet_handle']


multivalue_8_status = ixiangpf.multivalue_config (
        pattern                ="counter"                 ,
        counter_start          ="3000:0:0:1:0:0:0:2"      ,
        counter_step           ="0:0:0:1:0:0:0:0"         ,
        counter_direction      ="increment"               ,
        nest_step              ="0:0:0:1:0:0:0:0"         ,
        nest_owner             ="topology_3_handle"      ,
        nest_enabled           ="1"                       ,
    )
	
if multivalue_8_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', multivalue_8_status)

multivalue_8_handle = multivalue_8_status['multivalue_handle']

multivalue_9_status = ixiangpf.multivalue_config(
        pattern                ="counter"                 ,
        counter_start          ="3000:0:1:1:0:0:0:2"      ,
        counter_step           ="0:0:0:1:0:0:0:0"         ,
        counter_direction      ="increment"               ,
        nest_step              ="0:0:0:1:0:0:0:0"         ,
        nest_owner             =topology_3_handle      ,
        nest_enabled           ="1"                       ,
    )
	
if multivalue_9_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', multivalue_9_status)
	
multivalue_9_handle = multivalue_9_status["multivalue_handle"]


ipv6_3_status =ixiangpf.interface_config(
        protocol_name                     ="IPv6 3"                  ,
        protocol_handle                   =ethernet_3_handle        ,
        ipv6_multiplier                   ="1"                         ,
        ipv6_resolve_gateway              ="1"                         ,
        ipv6_manual_gateway_mac           ="00.00.00.00.00.01"         ,
        ipv6_manual_gateway_mac_step      ="00.00.00.00.00.00"         ,
        ipv6_gateway                      =multivalue_9_handle      ,
        ipv6_gateway_step                 ="::0"                       ,
        ipv6_intf_addr                    =multivalue_8_handle      ,
        ipv6_intf_addr_step               ="::0"                       ,
        ipv6_prefix_length                ="64"                        ,
    )	
if ipv6_3_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ipv6_3_status)
	
ipv6_3_handle = ipv6_3_status["ipv6_handle"]

################################################################################
# Configure Topology 4, Device Group 4                                         #
################################################################################

topology_4_status = ixiangpf.topology_config(
        topology_name      ="Topology 4"                          ,
        port_handle        =port_4								  ,
    )
	
if topology_4_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', topology_4_status)
	
topology_4_handle = topology_4_status["topology_handle"]


device_group_4_status=ixiangpf.topology_config(
        topology_handle              =topology_4_handle      ,
        device_group_name            ="Device Group4"         ,
        device_group_multiplier      ="45"                      ,
        device_group_enabled         ="1"                       ,
    )
if device_group_4_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', device_group_4_status)
	
deviceGroup_4_handle = device_group_4_status["device_group_handle"]

################################################################################
# Configure protocol interfaces for the fourth topology                        #
################################################################################

multivalue_10_status = ixiangpf.multivalue_config (
        pattern                ="counter"                 ,
        counter_start          ="00.14.01.00.00.01"       ,
        counter_step           ="00.00.00.00.00.01"       ,
        counter_direction      ="increment"               ,
        nest_step              ="00.00.01.00.00.00"       ,
        nest_owner             =topology_4_handle      ,
        nest_enabled           ="1"                       ,
    )

if multivalue_10_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', multivalue_10_status)

multivalue_10_handle = multivalue_10_status ["multivalue_handle"]

ethernet_4_status = ixiangpf.interface_config (
        protocol_name                ="Ethernet 4"               ,
        protocol_handle              =deviceGroup_4_handle      ,
        mtu                          ="1500"                       ,
        src_mac_addr                 =multivalue_10_handle      ,
        src_mac_addr_step            ="00.00.00.00.00.00"          ,
        vlan                         ="0"                          ,
        vlan_id                      ="1"                          ,
        vlan_id_step                 ="0"                          ,
        vlan_id_count                ="1"                          ,
        vlan_tpid                    ="0x8100"                     ,
        vlan_user_priority           ="0"                          ,
        vlan_user_priority_step      ="0"                         ,
        use_vpn_parameters           ="0"                          ,
        site_id                      ="0"                          ,
    )

	
if ethernet_4_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ethernet_4_status)

ethernet_4_handle = ethernet_4_status["ethernet_handle"]


multivalue_11_status = ixiangpf.multivalue_config(
        pattern                ="counter"                 ,
        counter_start          ="3000:0:1:1:0:0:0:2"      ,
        counter_step           ="0:0:0:1:0:0:0:0"         ,
        counter_direction      ="increment"               ,
        nest_step              ="0:0:0:1:0:0:0:0"         ,
        nest_owner             =topology_4_handle      ,
        nest_enabled           ="1"                       ,
    )

if multivalue_11_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', multivalue_11_status)

multivalue_11_handle = multivalue_11_status ["multivalue_handle"]


multivalue_12_status=ixiangpf.multivalue_config(
        pattern                ="counter"                 ,
        counter_start          ="3000:0:0:1:0:0:0:2"      ,
        counter_step           ="0:0:0:1:0:0:0:0"         ,
        counter_direction      ="increment"               ,
        nest_step              ="0:0:0:1:0:0:0:0"         ,
        nest_owner             =topology_4_handle      ,
        nest_enabled           ="1"                       ,
    )

if multivalue_12_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', multivalue_12_status)
	
multivalue_12_handle = multivalue_12_status["multivalue_handle"]


ipv6_4_status = ixiangpf.interface_config(
        protocol_name                     ="IPv6 4"                  ,
        protocol_handle                   =ethernet_4_handle        ,
        ipv6_multiplier                   ="1"                         ,
        ipv6_resolve_gateway              ="1"                         ,
        ipv6_manual_gateway_mac           ="00.00.00.00.00.01"         ,
        ipv6_manual_gateway_mac_step      ="00.00.00.00.00.00"         ,
        ipv6_gateway                      =multivalue_12_handle      ,
        ipv6_gateway_step                 ="::0"                       ,
        ipv6_intf_addr                    =multivalue_11_handle      ,
        ipv6_intf_addr_step               ="::0"                       ,
        ipv6_prefix_length                ="64"                        ,
    )
	
if ipv6_4_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ipv6_4_status)
	
ipv6_4_handle = ipv6_4_status ["ipv6_handle"]



####################################################
##Configure traffic for all configuration elements##

##########################################################
# Configure trafficItem 1 for Layer 47 AppLibrary Profile
##########################################################

flows1= (
"IRC_Login_Auth_Failure",
"IRC_Private_Chat",
"iSCSI_Read_and_Write",
"iTunes_Desktop_App_Store",
"iTunes_Mobile_App_Store",
"Jabber_Chat",
"Laposte_Webmail_1307",
"LinkedIn",
"Linkedin_1301",
"LPD",
)

traffic_item_1_status = ixiangpf.traffic_l47_config(
        mode                        ="create"																				  ,
        name                        ="Traffic_Item_1"																		  ,
        circuit_endpoint_type       ="ipv4_application_traffic"															  ,
        emulation_src_handle        =topology_1_handle																	  ,
        emulation_dst_handle        =topology_2_handle																	  ,
        objective_type              ="users"																				  ,
        objective_value             ="100"																				  ,
        objective_distribution      ="apply_full_objective_to_each_port"													  ,
        enable_per_ip_stats         ="1"																				  ,
        flows                       =flows1																			  ,
    )

if traffic_item_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', traffic_item_1_status)
	
##########################################################
# Configure trafficItem 2 for Layer 47 AppLibrary Profile
##########################################################

flows2 =(
"MAX_Bandwidth_HTTP",
"Microsoft_Update",
"MMS_MM1_WAP_HTTP",
"Modbus",
"MS_SQL_Create",
"MS_SQL_Delete",
"MS_SQL_Drop",
"MS_SQL_Insert",
"MS_SQL_Server",
"MS_SQL_Server_Advanced"
)


traffic_item_2_status =ixiangpf.traffic_l47_config(
        mode                        ="create"																				  ,
        name                        ="Traffic_Item_2"																		  ,
        circuit_endpoint_type       ="ipv6_application_traffic"															  ,
        emulation_src_handle        =topology_3_handle																	  ,
        emulation_dst_handle        =topology_4_handle																	  ,
        objective_type              ="users"																				  ,
        objective_value             ="100"																				  ,
        objective_distribution      ="apply_full_objective_to_each_port"													  ,
        enable_per_ip_stats         ="1"																					  ,
        flows                       =flows2																			  ,
    )

	
if traffic_item_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', traffic_item_2_status)
	




trafficItem_1_handle = traffic_item_1_status["traffic_l47_handle"]
responder_port_item1 = traffic_item_1_status[trafficItem_1_handle]["responder_ports"]
applib_handle_item1 = traffic_item_1_status[trafficItem_1_handle]["applib_profile"]
applib_flow_item1= traffic_item_1_status[trafficItem_1_handle][applib_handle_item1]["applib_flow"]

trafficItem_2_handle = traffic_item_2_status["traffic_l47_handle"]
responder_port_item2 = traffic_item_2_status[trafficItem_2_handle]["responder_ports"]
applib_handle_item2 = traffic_item_2_status[trafficItem_2_handle]["applib_profile"]
applib_flow_item2= traffic_item_2_status[trafficItem_2_handle][applib_handle_item2]["applib_flow"]


####################################################
# Start protocols
####################################################


start = ixiangpf.test_control(action='start_all_protocols')
if start['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', start)
time.sleep(10)


################################################################################
# Start traffic                                                                #
################################################################################

print "Running traffic"
run_traffic = ixiangpf.traffic_control(
        action				='run' 								,
        traffic_generator   ='ixnetwork_540' 						,
        type				='l47' 								,
    )

if run_traffic['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', run_traffic)

time.sleep(10)

drillDownSelectedOptions = (
	('L47_traffic_item_tcp','per_ports_per_initiator_flows','initiatorPorts'),
	('L47_flow_initiator_tcp','per_initiator_ports','initiatorPorts')
)

stats1= ixiangpf.traffic_stats(
					mode						="L47_traffic_item_tcp"			,
					drill_down_type				="per_ports_per_initiator_flows"	,
					drill_down_traffic_item		=trafficItem_1_handle			,
					drill_down_port				=port_1							,
					drill_down_flow				=flows1[0]				,
                )
time.sleep(10)

if stats1['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_stats', stats1)
	
stats2 = ixiangpf.traffic_stats(
					mode						="L47_flow_initiator_tcp"			,
					drill_down_type				="per_initiator_ports"				,
					drill_down_traffic_item		=trafficItem_2_handle			,
					drill_down_port				=port_3							,
					drill_down_flow				=flows2[1]				,
                )

if stats2['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_stats', stats2)

time.sleep(10)


####################################################
# Stop traffic
####################################################

print "Stopping traffic"
stop_traffic =ixiangpf.traffic_control(
        action				 ='stop' 								,
        traffic_generator    ='ixnetwork_540' 						,
        type			     ='l47' 								,
    )
if stop_traffic['status'] != IxiaHlt.SUCCESS:
   ErrorHandler('traffic_control', stop_traffic)
	
time.sleep(15)

####################################################
# Test END
####################################################

print "###################"
print"Test run is PASSED"
print "###################"


##################################################################################################################################################
##################################################################################################################################################





















