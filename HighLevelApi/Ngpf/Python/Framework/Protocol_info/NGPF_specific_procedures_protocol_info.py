################################################################################
# Version 1.0    $Revision: 1 $
# $Author: rcsutak
#
#    Copyright ? 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    11-14-2014 Ruxandra Csutak
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
#        - Topology 1 with Ethernet and IPv4 stacks							   #
#        - Topology 2 with Ethernet and IPv4 stacks 						   #
# The script does:										                       #
#    	 - start/stop protocol												   #
#		 - collect and display IPv4 and Ethernet statistics					   #	
#		 - uses protocol_info to retrieve stats regarding each protocol		   #
#																			   #
# Module:                                                                      #
#    The sample was tested on a 1GE LSM XMVDC16NG module.                      #
#                                                                              #
################################################################################

from pprint import pprint
import os, sys
import time

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
	ErrorHandler('', {})
except (NameError,):
	def ErrorHandler(cmd, retval):
		global ixiatcl
		err = ixiatcl.tcl_error_info()
		log = retval['log']
		additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
		raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)

        

chassis_ip = "ixro-hlt-xm2-09"
tcl_server = "ixro-hlt-xm2-09"
ixnetwork_tcl_server = 'localhost'
port_list = ['2/1', '2/2']
cfgErrors = 0

print "Printing connection variables ... "
print 'chassis_ip =  %s' % chassis_ip
print "tcl_server = %s " % tcl_server
print "ixnetwork_tcl_server = %s" % ixnetwork_tcl_server
print "port_list = %s " % port_list



##########################################
##  CONNECT AND PRINT CONNECTION RESULT ##
##########################################

connect_result = ixiangpf.connect(
        ixnetwork_tcl_server = ixnetwork_tcl_server,
        tcl_server = tcl_server,
        device = chassis_ip,
        port_list = port_list,
        break_locks = 1,
        reset = 1,
    )

if connect_result['status'] != '1':
    ErrorHandler('connect', connect_result)
    
print " Printing connection result"
pprint(connect_result)
 
ports = connect_result['vport_list'].split()


############################################################
##  CREATING FIRST TOPOLOGY WITH ETHERNET AND IPV4 STACKS ##
############################################################

topology_1 = ixiangpf.topology_config(
	topology_name      = "{Topology 1}",
	port_handle        = ports[0],
)
if topology_1['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', topology_1)
	
topology_1_handle = topology_1['topology_handle']
	
deviceGroup_1 = ixiangpf.topology_config(
	topology_handle              = topology_1_handle,
	device_group_name            = "{Device Group 1}",
	device_group_multiplier      = "10",
	device_group_enabled         = "1",
)
if deviceGroup_1['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', deviceGroup_1)

deviceGroup_1_handle = deviceGroup_1['device_group_handle']
	
    
mv1 = ixiangpf.multivalue_config(
    pattern                = "counter",
    counter_start          = "00.11.01.00.00.01",
    counter_step           = "00.00.00.00.00.01",
    counter_direction      = "increment",
    nest_step              = "00.00.01.00.00.00",
    nest_owner             = topology_1_handle,
    nest_enabled           = "1",
)
if mv1['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv1)

multivalue_1_handle = mv1['multivalue_handle']

mv2 = ixiangpf.multivalue_config(
    pattern           = "custom",
    nest_step         = "1",
    nest_owner        = topology_1_handle,
    nest_enabled      = "0",
)
if mv2['status'] != IxiaHlt.SUCCESS:
       ErrorHandler('multivalue_config', mv2)

multivalue_2_handle = mv2['multivalue_handle']

mv3 = ixiangpf.multivalue_config(
    multivalue_handle      = multivalue_2_handle,
    custom_start           = "1",
    custom_step            = "1",
)
if mv3['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv3)

custom_1_handle = mv3['custom_handle']

mv4 = ixiangpf.multivalue_config(
    custom_handle               = custom_1_handle,
    custom_increment_value      = "0",
    custom_increment_count      = "3",
)
if mv4['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv4)

increment_1_handle = mv4['increment_handle']

interface_1 = ixiangpf.interface_config(
    protocol_name                = "{Ethernet 1}",
    protocol_handle              = deviceGroup_1_handle,
    mtu                          = "1500",
    src_mac_addr                 = multivalue_1_handle,
    vlan                         = "1",
    vlan_id                      = multivalue_2_handle,
    vlan_id_step                 = "0",
    vlan_id_count                = "1",
    vlan_tpid                    = "0x8100",
    vlan_user_priority           = "0",
    vlan_user_priority_step      = "0",
    use_vpn_parameters           = "0",
    site_id                      = "0",
)
if interface_1['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', interface_1)

ethernet_1_handle = interface_1['ethernet_handle']


mv5 = ixiangpf.multivalue_config(
    pattern           = "custom",
    nest_step         = "0.1.0.0",
    nest_owner        = topology_1_handle,
    nest_enabled      = "1",
)
if mv5['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv5)

multivalue_3_handle = mv5['multivalue_handle']

mv6 = ixiangpf.multivalue_config(
    multivalue_handle      = multivalue_3_handle,
    custom_start           = "100.1.0.2",
    custom_step            = "0.0.1.0",
)
if mv6['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv6)

custom_2_handle = mv6['custom_handle']

mv7 = ixiangpf.multivalue_config(
    custom_handle               = custom_2_handle,
    custom_increment_value      = "0.0.0.1",
    custom_increment_count      = "3",
)
if mv7['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv7)

increment_2_handle = mv7['increment_handle']

mv8 = ixiangpf.multivalue_config(
    pattern                 = "custom",
    nest_step               = "0.0.0.1",
    nest_owner              = topology_1_handle,
    nest_enabled            = "0",
    overlay_value           = "100.1.3.1",
    overlay_value_step      = "100.1.3.1",
    overlay_index           = "10",
    overlay_index_step      = "0",
    overlay_count           = "1",
)
if mv8['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv8)

multivalue_4_handle = mv8['multivalue_handle']

mv9 = ixiangpf.multivalue_config(
    multivalue_handle      = multivalue_4_handle,
    custom_start           = "100.1.0.5",
    custom_step            = "0.0.1.0",
)
if mv9['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv9)

custom_3_handle = mv9['custom_handle']

mv10 = ixiangpf.multivalue_config(
    custom_handle               = custom_3_handle,
    custom_increment_value      = "0.0.0.0",
    custom_increment_count      = "3",
)
if mv10['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv10)

increment_3_handle = mv10['increment_handle']

interface_2 = ixiangpf.interface_config(
    protocol_name                     = "{IPv4 1}",
    protocol_handle                   = ethernet_1_handle,
    ipv4_resolve_gateway              = "1",
    ipv4_manual_gateway_mac           = "00.00.00.00.02.01",
    ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
    gateway                           = multivalue_4_handle,
    intf_ip_addr                      = multivalue_3_handle,
    netmask                           = "255.255.255.0",
)
if interface_2['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', interface_2)


ipv4_1_handle = interface_2['ipv4_handle']

#############################################################
##  CREATING SECOND TOPOLOGY WITH ETHERNET AND IPV4 STACKS ##
#############################################################

topology_2 = ixiangpf.topology_config(
    topology_name      = "{Topology 2}",
    port_handle        = ports[1],
)
if topology_2['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', topology_2)

topology_2_handle = topology_2['topology_handle']

deviceGroup_2 = ixiangpf.topology_config(
    topology_handle              = topology_2_handle,
    device_group_name            = "{Device Group 2}",
    device_group_multiplier      = "10",
    device_group_enabled         = "1",
)
if deviceGroup_2['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', deviceGroup_2)

deviceGroup_2_handle = deviceGroup_2['device_group_handle']


mv11 = ixiangpf.multivalue_config(
    pattern                = "counter",
    counter_start          = "00.12.01.00.00.01",
    counter_step           = "00.00.00.00.00.01",
    counter_direction      = "increment",
    nest_step              = "00.00.01.00.00.00",
    nest_owner             = topology_2_handle,
    nest_enabled           = "1",
)
if mv11['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv11)

multivalue_5_handle = mv11['multivalue_handle']

mv12 = ixiangpf.multivalue_config(
    pattern           = "custom",
    nest_step         = "1",
    nest_owner        = topology_2_handle,
    nest_enabled      = "0",
)
if mv12['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv12)

multivalue_6_handle = mv12['multivalue_handle']

mv13 = ixiangpf.multivalue_config(
    multivalue_handle      = multivalue_6_handle,
    custom_start           = "1",
    custom_step            = "1",
)
if mv13['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv13)

custom_4_handle = mv13['custom_handle']

mv14 = ixiangpf.multivalue_config(
    custom_handle               = custom_4_handle,
    custom_increment_value      = "0",
    custom_increment_count      = "3",
)
if mv14['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv14)

increment_4_handle = mv14['increment_handle']

interface_3 = ixiangpf.interface_config(
    protocol_name                = "{Ethernet 2}",
    protocol_handle              = deviceGroup_2_handle,
    mtu                          = "1500",
    src_mac_addr                 = multivalue_5_handle,
    vlan                         = "1",
    vlan_id                      = multivalue_6_handle,
    vlan_id_step                 = "0",
    vlan_id_count                = "1",
    vlan_tpid                    = "0x8100",
    vlan_user_priority           = "0",
    vlan_user_priority_step      = "0",
    use_vpn_parameters           = "0",
    site_id                      = "0",
)
if interface_3['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', interface_3)

ethernet_2_handle = interface_3['ethernet_handle']

mv15 = ixiangpf.multivalue_config(
    pattern                 = "custom",
    nest_step               = "0.1.0.0",
    nest_owner              = topology_2_handle,
    nest_enabled            = "1",
    overlay_value           = "100.1.3.1",
    overlay_value_step      = "100.1.3.1",
    overlay_index           = "10",
    overlay_index_step      = "0",
    overlay_count           = "1",
)
if mv15['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv15)

multivalue_7_handle = mv15['multivalue_handle']

mv16 = ixiangpf.multivalue_config(
    multivalue_handle      = multivalue_7_handle,
    custom_start           = "100.1.0.5",
    custom_step            = "0.0.1.0",
)
if mv16['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv16)

custom_5_handle = mv16['custom_handle']

mv17 = ixiangpf.multivalue_config(
    custom_handle               = custom_5_handle,
    custom_increment_value      = "0.0.0.1",
    custom_increment_count      = "3",
)
if mv17['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv17)

increment_5_handle = mv17['increment_handle']

mv18 = ixiangpf.multivalue_config(
    pattern           = "custom",
    nest_step         = "0.1.0.0",
    nest_owner        = topology_2_handle,
    nest_enabled      = "1",
)
if mv18['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv18)

multivalue_8_handle = mv18['multivalue_handle']

mv19 = ixiangpf.multivalue_config(
    multivalue_handle      = multivalue_8_handle,
    custom_start           = "100.1.0.2",
    custom_step            = "0.0.1.0",
)
if mv19['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv19)

custom_6_handle = mv19['custom_handle']

mv20 = ixiangpf.multivalue_config(
    custom_handle               = custom_6_handle,
    custom_increment_value      = "0.0.0.0",
    custom_increment_count      = "3",
)
if mv20['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', m20)

increment_6_handle = mv20['increment_handle']

interface_4 = ixiangpf.interface_config(
    protocol_name                     = "{IPv4 2}",
    protocol_handle                   = ethernet_2_handle,
    ipv4_resolve_gateway              = "1",
    ipv4_manual_gateway_mac           = "00.00.00.00.01.01",
    ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
    gateway                           = multivalue_8_handle,
    intf_ip_addr                      = multivalue_7_handle,
    netmask                           = "255.255.255.0",
)
if interface_4['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', interface_4)

ipv4_2_handle = interface_4['ipv4_handle']


#############################
##  STARTING ALL PROTOCOLS ##
#############################

print "\nStarting all protocols ... "    
start = ixiangpf.test_control(action='start_all_protocols')

if start['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', start)

print "\nSleeping for 30 seconds ... "	
time.sleep(30)

#############################
##  STOPPING ALL PROTOCOLS ##
#############################

print "\nStopping all protocols ... "
stop = ixiangpf.test_control(action='stop_all_protocols')

if stop['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', stop)	


####################################
##  RETRIEVE AND PRINT STATISTICS ##
####################################
    
print "\n====>Gather and print ethernet and ipv4 protocol_info stats (mode = aggregate) ...\n\n"    

eth_1_info = ixiangpf.protocol_info(
    handle = ethernet_1_handle,
    mode = 'aggregate',
)

if eth_1_info['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('protocol_info', eth_1_info)

print "\n====>Ethernet info (port 0) ... \n"
pprint(eth_1_info)
     
eth_2_info = ixiangpf.protocol_info(
    handle = ethernet_2_handle,
    mode = 'aggregate',
)

if eth_2_info['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('protocol_info', eth_2_info)

print "\n====>Ethernet info (port 1) ... \n"
pprint(eth_2_info)
    

ipv4_1_info = ixiangpf.protocol_info(
    handle = ipv4_1_handle,
    mode = 'aggregate',
)

if ipv4_1_info['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('protocol_info', ipv4_1_info)
    
print "\n====>IPv4 info (port 0) ... \n"
pprint(ipv4_1_info)
    
ipv4_2_info = ixiangpf.protocol_info(
    handle = ipv4_2_handle,
    mode = 'aggregate',
)

if ipv4_2_info['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('protocol_info', ipv4_2_info)
    
print "\n====>IPv4 info (port 1) ... \n"
pprint(ipv4_2_info)


print "\n====>Gather and print ethernet and ipv4 protocol_info stats (mode = handles) ...\n\n"   
    
eth_3_info = ixiangpf.protocol_info(
    handle = ethernet_1_handle,
    mode = 'handles',
)

if eth_3_info['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('protocol_info', eth_3_info)
    
print "\n====>Ethernet info (port 0) ... \n"
pprint(eth_3_info)
     
eth_4_info = ixiangpf.protocol_info(
    handle = ethernet_2_handle,
    mode = 'handles',
)

if eth_4_info['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('protocol_info', eth_4_info)

print "\n====>Ethernet info (port 1) ... \n"
pprint(eth_4_info)
    

ipv4_3_info = ixiangpf.protocol_info(
    handle = ipv4_1_handle,
    mode = 'handles',
)

if ipv4_3_info['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('protocol_info', ipv4_3_info)
    
print "\n====>IPv4 info (port 0) ... \n"
pprint(ipv4_3_info)
    
ipv4_4_info = ixiangpf.protocol_info(
    handle = ipv4_2_handle,
    mode = 'handles',
)

if ipv4_4_info['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('protocol_info', ipv4_4_info)
    
print "\n====>IPv4 info (port 1) ... \n"
pprint(ipv4_4_info)

print "\n\nScript ended SUCCESSFULLY!"
