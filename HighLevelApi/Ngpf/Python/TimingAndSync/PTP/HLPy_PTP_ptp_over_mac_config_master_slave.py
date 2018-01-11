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
#        - Topology 1 with PTP over MAC - Master							   #
#        - Topology 2 with PTP over MAC - Slave 							   #
# The script does:										                       #
#    	 - start/stop protocol												   #
#		 - collect and display PTP aggregate statistics						   #
#																			   #
# Module:                                                                      #
#    The sample was tested on a 10GE LSM XM3 module.                           #
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
# 								PTP MASTER CONFIG
# #############################################################################

# CREATE TOPOLOGY 1

print('\n\nConfigure PTP Master ...\n\n')

topology_1_status =ixiangpf.topology_config(
    topology_name = 'PTP Master Topology',
    port_handle = port_0,
)
if topology_1_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('topology_config', topology_1_status)

topology_1_handle = topology_1_status['topology_handle']

# CREATE DEVICE GROUP 1

device_group_1_status = ixiangpf.topology_config(
    topology_handle          =    topology_1_handle,
	device_group_name        =   'PTP MAster 1',
	device_group_multiplier  =    '3',
	device_group_enabled     =    '1',
)
if device_group_1_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('topology_config', device_group_1_status)

device_1_handle	= device_group_1_status['device_group_handle']

# CREATE ETHERNET STACK FOR PTP 1

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

# CREATE PTP STACK

ptp_over_mac_status = ixiangpf.ptp_over_mac_config(
		parent_handle						=		ethernet_1_handle ,
		profile								= 		"ieee1588" ,
		role								= 		"master" ,
		mode                                =      "create" ,
		name                                =      "PTP Master" ,
		port_number                         =     	"6323" ,
		communication_mode                  = 		"multicast" ,
		domain                              = 		"123" ,
		priority1                           = 		"10" ,
		priority2                           = 		"100" ,
)
if ptp_over_mac_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('ptp_over_mac_config', ptp_over_mac_status)

ptp_master = ptp_over_mac_status['ptp_handle']

# #############################################################################
# 								PTP SLAVE CONFIG
# #############################################################################

# CREATE TOPOLOGY 2

print('\n\nConfigure PTP Slave ...\n\n')

topology_2_status = ixiangpf.topology_config(
    topology_name      = 'PTP Slave Topology',
    port_handle        = port_1
)
if topology_2_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('topology_config', topology_2_status)

topology_2_handle = topology_2_status['topology_handle']

# CREATE DEVICE GROUP 2

device_group_2_status = ixiangpf.topology_config(
	topology_handle          =    topology_2_handle,
	device_group_name        =    'PTP Slave 1',
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

# CREATE PTP STACK

ptp_over_mac_status = ixiangpf.ptp_over_mac_config(
		parent_handle						=		ethernet_2_handle ,
		profile								= 		"ieee1588" ,
		role								= 		"slave" ,
		mode                                =      "create" ,
		name                                =      "PTP Slave" ,
		port_number                         =     	"6323" ,
		communication_mode                  = 		"multicast" ,
		domain                              = 		"123" ,
		priority1                           = 		"10" ,
		priority2                           = 		"100" ,
)
if ptp_over_mac_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('ptp_over_mac_config', ptp_over_mac_status)

ptp_slave = ptp_over_mac_status['ptp_handle']

# #############################################################################
# 								START PTP
# #############################################################################

start_master = ixiangpf.ptp_over_mac_control(
		action		=		'start'	,
		handle		=		ptp_master	,
)
if start_master['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('ptp_over_mac_control', start_master)

time.sleep(5)

start_slave = ixiangpf.ptp_over_mac_control(
		action		=		'connect'	,
		handle		=		ptp_slave	,
)
if start_slave['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('ptp_over_mac_control', start_slave)

time.sleep(20)

# #############################################################################
# 								PTP STATS
# #############################################################################

ptp_aggregate_stats = ixiangpf.ptp_over_mac_stats(
		mode			=		'aggregate'		,
		port_handle		=		port_0	,
)
if ptp_aggregate_stats['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('ptp_over_mac_stats', ptp_aggregate_stats)

print('\n\nPTP aggregate stats port 1:\n')
printDict(ptp_aggregate_stats)

ptp_aggregate_stats = ixiangpf.ptp_over_mac_stats(
		mode			=		'aggregate'		,
		port_handle		=		port_1	,
)
if ptp_aggregate_stats['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('ptp_over_mac_stats', ptp_aggregate_stats)

print('\n\nPTP aggregate stats port 2:\n')
printDict(ptp_aggregate_stats)

# #############################################################################
# 								STOP PTP
# #############################################################################

stop_slave = ixiangpf.ptp_over_mac_control (
		action		=		'stop'	,
		handle		=		ptp_slave	,
)
if stop_slave['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('ptp_over_mac_control', stop_slave)

time.sleep(5)

stop_master = ixiangpf.ptp_over_mac_control (
		action		=		'disconnect'	,
		handle		=		ptp_master	,
)
if stop_master['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('ptp_over_mac_control', stop_master)

time.sleep(5)

# #############################################################################
# 								CLEANUP SESSION
# #############################################################################

cleanup_status = ixiangpf.cleanup_session(reset='1')
if cleanup_status['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('cleanup_session', cleanup_status)

print('\n\nIxNetwork session is closed...\n\n')
print('!!! TEST is PASSED !!!')

