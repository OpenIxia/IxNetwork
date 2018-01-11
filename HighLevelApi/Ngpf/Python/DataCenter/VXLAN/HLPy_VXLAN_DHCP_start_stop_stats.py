################################################################################
# Version 1.0    $Revision: 1 $
# $Author: tbadea
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    04-09-2014 Daria Badea
#
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
# This script configures a scenario with 2 topologies:		                   #
#        - Topology 1 with VXLAN and DHCP Client							   #
#        - Topology 2 with VXLAN and DHCP Server				    		   #
# The script does:										                       #
#    	 - start/stop protocol												   #
#		 - collect and display VXLAN/DHCP statistics						   #
#																			   #
# Module:                                                                      #
#    The sample was tested on a FlexAP10G16S			                       #
#                                                                              #
################################################################################

import sys, os
import time, re

# Append paths to python APIs

# sys.path.append('/path/to/hltapi/library/common/ixiangpf/python') 
# sys.path.append('/path/to/ixnetwork/api/python')

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError

ixiatcl = IxiaTcl()
ixiahlt = IxiaHlt(ixiatcl)
ixiangpf = IxiaNgpf(ixiahlt)

try:
	ixnHLT_errorHandler('', {})
except (NameError,):
	def ixnHLT_errorHandler(cmd, retval):
		global ixiatcl
		err = ixiatcl.tcl_error_info()
		log = retval['log']
		additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
		raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)

def printDict(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    if type(obj) == dict:
        print >> output, '%s' % ((nested_level) * spacing)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                printDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % ((nested_level + 1) * spacing, k, v)
        print >> output, '%s' % (nested_level * spacing)
    elif type(obj) == list:
        print >> output, '%s[' % ((nested_level) * spacing)
        for v in obj:
            if hasattr(v, '__iter__'):
                printDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % ((nested_level) * spacing)
    else:
        print >> output, '%s%s' % (nested_level * spacing, obj)


chassis_ip              = '10.205.15.184'
ixnetwork_tcl_server    = 'localhost'
port_list               = '9/1 9/9'

# #############################################################################
# 								CONNECT AND PORT HANDLES
# #############################################################################

print('\n\nConnect to IxNetwork Tcl Server and get port handles...\n\n')

connect_status = ixiangpf.connect(
	reset                  = 1,
    device                 = chassis_ip,
	port_list              = port_list,
	ixnetwork_tcl_server   = ixnetwork_tcl_server,
	tcl_server             = chassis_ip,
)
if connect_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('connect', connect_status)

port_handle = connect_status['vport_list']
port_0 = port_handle.split(' ')[0]
port_1 = port_handle.split(' ')[1]

# #############################################################################
# 								VTEP 1 CONFIG
# #############################################################################

# CREATE TOPOLOGY 1

print('\n\nConfigure VXLAN stack 1 ...\n\n')

topology_1_status =ixiangpf.topology_config(
    topology_name = 'Topology 1',
    port_handle = port_0,
)
if topology_1_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('topology_config', topology_1_status)

topology_1_handle = topology_1_status['topology_handle']

# CREATE DEVICE GROUP 1

device_group_1_status = ixiangpf.topology_config(
    topology_handle          =    topology_1_handle,
	device_group_name        =   'VTEP 1',
	device_group_multiplier  =    '3',
	device_group_enabled     =    '1',
)
if device_group_1_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('topology_config', device_group_1_status)

device_1_handle	= device_group_1_status['device_group_handle']

# CREATE ETHERNET STACK FOR VXLAN 1

multivalue_1_status = ixiangpf.multivalue_config(
    pattern              =  'counter',
    counter_start        =  '00.11.01.00.00.01',
    counter_step         =  '00.00.00.00.00.01',
    counter_direction    =  'increment',
    nest_step            =  '00.00.01.00.00.00',
    nest_owner           =  topology_1_handle,
    nest_enabled         =  '1',
)
if multivalue_1_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('multivalue_config', multivalue_1_status)

multivalue_1_handle = multivalue_1_status['multivalue_handle']

ethernet_1_status = ixiangpf.interface_config(
    protocol_name           =     'Ethernet 1',
    protocol_handle         =     device_1_handle,
    mtu                     =     '1500',
    src_mac_addr            =     multivalue_1_handle,
    vlan                    =     '1',
    vlan_id                 =     '101',
    vlan_id_step            =     '1',
    vlan_id_count           =     '1',
    vlan_tpid               =     '0x8100',
    vlan_user_priority      =     '0',
    vlan_user_priority_step =     '0',
    use_vpn_parameters      =     '0',
    site_id                 =     '0',
)
if ethernet_1_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('interface_config', ethernet_1_status)

ethernet_1_handle = ethernet_1_status['ethernet_handle']

vxlan_1_status = ixiangpf.emulation_vxlan_config(
		 mode						=	'create',
		 handle					    =	ethernet_1_handle,
         intf_ip_addr				=	'23.0.0.1',
         intf_ip_addr_step			=	'0.0.0.1',
         ip_num_sessions            =   '2',
         intf_ip_prefix_length		=	'24',
         gateway					=	'23.0.0.100',
         gateway_step				=	'0.0.0.1',
         enable_resolve_gateway	    =	'1',
         vni						=	'600',
		 create_ig					=	'0',
         ipv4_multicast			    =	'225.3.0.9',
		 sessions_per_vxlan		    =	'1',
         ip_to_vxlan_multiplier	    =   '1',
)
if vxlan_1_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_vxlan_config', vxlan_1_status)


vxlan_1_handle = vxlan_1_status['vxlan_handle']

# #############################################################################
# 								VTEP 2 CONFIG
# #############################################################################

# CREATE TOPOLOGY 2

print('\n\nConfigure VXLAN stack 2 ...\n\n')

topology_2_status = ixiangpf.topology_config(
    topology_name      = 'Topology 2',
    port_handle        = port_1
)
if topology_2_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('topology_config', topology_2_status)

topology_2_handle = topology_2_status['topology_handle']

# CREATE DEVICE GROUP 2

device_group_2_status = ixiangpf.topology_config(
	topology_handle          =    topology_2_handle,
	device_group_name        =    'VTEP 2',
	device_group_multiplier  =    '3',
	device_group_enabled     =    '1',
)
if device_group_2_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('topology_config', device_group_2_status)

device_2_handle	= device_group_2_status ['device_group_handle']

# CREATE ETHERNET STACK FOR VXLAN 2

multivalue_2_status = ixiangpf.multivalue_config(
    pattern              =  'counter',
    counter_start        =  '00.24.01.00.00.01',
    counter_step         =  '00.00.00.00.00.01',
    counter_direction    =  'increment',
    nest_step            =  '00.00.01.00.00.00',
    nest_owner           =  topology_2_handle,
    nest_enabled         =  '1',
)
if multivalue_2_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('multivalue_config', multivalue_2_status)

multivalue_2_handle = multivalue_2_status ['multivalue_handle']

ethernet_2_status = ixiangpf.interface_config(
    protocol_name           =     'Ethernet 2'               ,
    protocol_handle         =     device_2_handle           ,
    mtu                     =     '1500'                       ,
    src_mac_addr            =     multivalue_2_handle       ,
    vlan                    =     '1'                          ,
    vlan_id                 =     '101'                        ,
    vlan_id_step            =     '1'                          ,
    vlan_id_count           =     '1'                          ,
    vlan_tpid               =     '0x8100'                    ,
    vlan_user_priority      =     '0'                          ,
    vlan_user_priority_step =     '0'                          ,
    use_vpn_parameters      =     '0'                          ,
    site_id                 =     '0'                          ,
)
if ethernet_2_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('interface_config', ethernet_2_status)

ethernet_2_handle = ethernet_2_status ['ethernet_handle']

# CREATE IPv4 STACK FOR VXLAN 2

multivalue_2_status = ixiangpf.multivalue_config(
    pattern              =  'counter'                 ,
    counter_start        =  '23.0.0.100'              ,
    counter_step         =  '0.0.0.1'                 ,
    counter_direction    =  'increment'               ,
    nest_step            =  '0.1.0.0'                 ,
    nest_owner           =  topology_1_handle      ,
    nest_enabled         =  '1'                       ,
)
if multivalue_2_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('multivalue_config', multivalue_2_status)

multivalue_2_handle = multivalue_2_status ['multivalue_handle']

gw_multivalue_1_status = ixiangpf.multivalue_config(
    pattern              =  'counter'                 ,
    counter_start        =  '23.0.0.1'              ,
    counter_step         =  '0.0.0.1'                 ,
    counter_direction    =  'increment'               ,
    nest_step            =  '0.1.0.0'                 ,
    nest_owner           =  topology_1_handle      ,
    nest_enabled         =  '1'                       ,
)
if gw_multivalue_1_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('multivalue_config', gw_multivalue_1_status)

gw_multivalue_1_handle = gw_multivalue_1_status ['multivalue_handle']

ipv4_2_status = ixiangpf.interface_config(
    protocol_name           =     'IPv4 2'                  ,
    protocol_handle         =     ethernet_2_handle        ,
    ipv4_resolve_gateway    =     '1'                         ,
    gateway                 =     gw_multivalue_1_handle   ,
    intf_ip_addr            =     multivalue_2_handle      ,
    netmask                 =     '255.255.255.0'             ,
)
if ipv4_2_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('interface_config', ipv4_2_status)

ipv4_2_handle = ipv4_2_status ['ipv4_handle']

vxlan_2_status = ixiangpf.emulation_vxlan_config(
	 mode							=		'create'							,
	 handle							=	ipv4_2_handle					,
     intf_ip_prefix_length			=		'24'								,
     vni							=		'600'								,
	 create_ig						=		'1'								,
     ipv4_multicast					=	'225.3.0.9'						,
     ip_to_vxlan_multiplier			=	'1'								,
     ig_intf_ip_addr			    =     '80.0.0.100'			            ,
     ig_intf_ip_addr_step		    =        '1.0.0.0'			                ,
     ig_intf_ip_prefix_length	    =			'16'								,
	 ig_mac_address_init			=		'00:67:22:33:00:00'				,
     ig_mac_address_step			=		'00:00:00:00:00:11'				,
	 ig_gateway						=	'80.0.0.101'						,
     ig_gateway_step				=		'1.0.0.0'							,
	 ig_enable_resolve_gateway		=		'0'								,
	 sessions_per_vxlan				=	'1'								,
)
if vxlan_2_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_vxlan_config', vxlan_2_status)

inner_ipv4_2_handle = vxlan_2_status['ig_ipv4_handle']
vxlan_2_handle      = vxlan_2_status['vxlan_handle']

# #############################################################################
# 								 DHCPv4 SERVER
# #############################################################################

multivalue_pool = ixiangpf.multivalue_config(
    pattern           =     'counter'                 ,
    counter_start     =     '80.0.0.1'		       ,
    counter_step      =     '1.0.0.0'			       ,
    counter_direction =     'increment'               ,
    nest_step         =     '1.0.0.0'				       ,
    nest_owner        =     topology_2_handle      ,
    nest_enabled      =     '1'                       ,
)
if multivalue_pool['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('multivalue_config', multivalue_pool)

multivalue_pool_handle = multivalue_pool['multivalue_handle']

multivalue_prefix = ixiangpf.multivalue_config(
    pattern            =    'counter'                 ,
	counter_start		=	'16'					,
	counter_step		=	'0'					,
	counter_direction	=	'increment'					,
	nest_step			=	'0'			,
    nest_owner          =   topology_2_handle      ,
    nest_enabled        =   '1'                       ,
)
if multivalue_prefix['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('multivalue_config', multivalue_prefix)

multivalue_prefix_handle = multivalue_prefix['multivalue_handle']

dhcp_server_config_status1 = ixiangpf.emulation_dhcp_server_config(
        mode                              =          'create'                                  ,
		handle						      =			 inner_ipv4_2_handle  					,
		lease_time						  =			 '84600'							,
		ipaddress_count					  =		     '100'		                          ,
		ipaddress_pool					  =			 multivalue_pool_handle                         ,
		ipaddress_pool_prefix_length 	  =			 multivalue_prefix_handle                            ,
        ip_version                        =          '4'                                       ,
)
if dhcp_server_config_status1['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_dhcp_server_config', dhcp_server_config_status1)

dhcp_server_handle = dhcp_server_config_status1['dhcpv4server_handle']


# #############################################################################
# 								 DHCPv4 CLIENT
# #############################################################################

device_group_chained_status_1 = ixiangpf.topology_config(
		device_group_multiplier   =   '5'                         ,
		device_group_handle       =   device_1_handle      ,
)
if device_group_chained_status_1['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('topology_config', device_group_chained_status_1)

chained_dg_1_handle = device_group_chained_status_1['device_group_handle']

dhcp_status = ixiangpf.emulation_dhcp_group_config(
		handle						=	chained_dg_1_handle    ,
		dhcp_range_ip_type			=	'ipv4'						 ,
		dhcp_range_renew_timer		=	'2'							 ,
		use_rapid_commit			=	'0'							 ,
)
if dhcp_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_dhcp_group_config', dhcp_status)

dhcp_client_handle = dhcp_status['dhcpv4client_handle']

# #############################################################################
# 								START PROTOCOLS
# #############################################################################

print('\n\nStart VXLAN ...\n\n')

control_status_1 = ixiangpf.emulation_vxlan_control(
    handle     = 	  vxlan_1_handle                    ,
    action     =      'start'                      ,
)
if control_status_1['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_vxlan_control', control_status_1)

control_status_2 = ixiangpf.emulation_vxlan_control(
    handle      =	  vxlan_2_handle              ,
    action      =  'start'                     ,
)
if control_status_2['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_vxlan_control', control_status_2)

print ('\n\nStart DHCP server...\n\n')

control_status = ixiangpf.emulation_dhcp_server_control(
	dhcp_handle 	=		dhcp_server_handle 		,
	action 			=	'collect'								,
)
if control_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_dhcp_server_control', control_status)

print('\n\nStart DHCP clients...\n\n')

control_status = ixiangpf.emulation_dhcp_control(
	handle 		=		dhcp_client_handle ,
	action 		=		'bind'							,
)
if control_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_dhcp_control', control_status)

time.sleep(20)

# #############################################################################
# 								STATISTICS
# #############################################################################

# CLIENT

vxlan_stats_2 = ixiangpf.emulation_vxlan_stats(
    port_handle 		=	port_0                                   ,
    mode 				=    'aggregate_stats'                                                 ,
    execution_timeout  =    '30'                                              ,
)
if vxlan_stats_2['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_vxlan_stats', vxlan_stats_2)

dhcp_client_stats = ixiangpf.emulation_dhcp_stats(
    port_handle  = port_0,
	mode  = 'aggregate_stats',
    execution_timeout  = '30',
)
if dhcp_client_stats['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_dhcp_stats', dhcp_client_stats)

# SERVER

vxlan_stats_1 = ixiangpf.emulation_vxlan_stats(
    port_handle 	=		port_1                                   ,
	mode 			=	'aggregate_stats'                                                ,
    execution_timeout = '30'                                              ,
)
if vxlan_stats_1['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_vxlan_stats', vxlan_stats_1)

dhcp_server_stats = ixiangpf.emulation_dhcp_server_stats(
    port_handle = port_1,
	action = 'collect',
    execution_timeout = '30',
)
if dhcp_server_stats['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_dhcp_server_stats', dhcp_server_stats)

time.sleep(3)

print('\n\nVXLAN aggregate stats port 1:\n')
printDict(vxlan_stats_2)

print('\n\nVXLAN aggregate stats port 2:\n')
printDict(vxlan_stats_1)

print('\n\nDHCP Client aggregate stats:\n')
printDict(dhcp_client_stats)

print('\n\nDHCP Server aggregate stats:\n')
printDict(dhcp_server_stats)

if dhcp_client_stats[port_0]['aggregate']['success_percentage'] != '100':
    raise IxiaError(IxiaError.COMMAND_FAIL, 'Not all DHCP sessions are up!')

if dhcp_server_stats['aggregate'][port_1]['sessions_up'] != '3':
    raise IxiaError(IxiaError.COMMAND_FAIL, 'Not all DHCP Server sessions are up!')

# #############################################################################
# 								STOP PROTOCOLS
# #############################################################################

print('\n\nStop VXLAN ...\n\n')

control_status_1 = ixiangpf.emulation_vxlan_control(
    handle     = 	  vxlan_1_handle                    ,
    action     =      'stop'                      ,
)
if control_status_1['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_vxlan_control', control_status_1)

control_status_2 = ixiangpf.emulation_vxlan_control(
    handle      =	  vxlan_2_handle              ,
    action      =  'stop'                     ,
)
if control_status_2['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('emulation_vxlan_control', control_status_2)

# #############################################################################
# 								CLEANUP SESSION
# #############################################################################

cleanup_status = ixiangpf.cleanup_session(reset='1')
if cleanup_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('cleanup_session', cleanup_status)

print('\n\nIxNetwork session is closed...\n\n')
print('!!! TEST is PASSED !!!')


