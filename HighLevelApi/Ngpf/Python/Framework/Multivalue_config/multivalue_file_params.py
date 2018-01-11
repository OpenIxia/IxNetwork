################################################################################
# Version 1.0    $Revision: 1 $
# $Author: rcsutak
#
#    Copyright ? 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-14-2014 Ruxandra Csutak
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
#        - Topology 2 with Ethernet and IPv4 stacks                            # 
#        - uses the file pattern for multivalue_config procedure               #
# The script does:										                       #
#    	 - start/stop protocols												   #
#		 - collect and display IPv4 and Ethernet statistics 				   #
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

dirname, filename = os.path.split(os.path.abspath(__file__))
chassis_ip = "ixro-hlt-xm2-09"
tcl_server = "ixro-hlt-xm2-09"
ixnetwork_tcl_server = 'localhost'
port_list_str = "2/1 2/2"
port_list = port_list_str.split()
cfgErrors = 0
file_param = os.path.join(dirname, 'file_params.csv')

print "Printing connection variables ... "
print "test_name = %s" % filename
print 'chassis_ip =  %s' % chassis_ip
print "tcl_server = %s " % tcl_server
print "ixnetwork_tcl_server = %s" % ixnetwork_tcl_server
print "port_list = %s " % port_list
print "file_param = %s " % file_param


######################################
##  CONNECT WITHOUT SESSION RESUME  ##
######################################
connect_result = ixiangpf.connect(
        ixnetwork_tcl_server = ixnetwork_tcl_server,
        tcl_server = tcl_server,
        device = chassis_ip,
        port_list = port_list_str,
        break_locks = 1,
        reset = 1,
    )

if connect_result['status'] != '1':
    print "FAIL:"
    print connect_result['log']
    quit()
print " Printing connection result"
pprint(connect_result)
 

ports = connect_result['vport_list'].split()

top_1 = ixiangpf.topology_config(
	topology_name      = "{Topology 1}",
	port_handle        = ports[0],
)
if top_1['status'] != IxiaHlt.SUCCESS:
    print "FAIL:"
    print top_1['log']
    quit()    
	
topology_1_handle = top_1['topology_handle']
	
dg_1 = ixiangpf.topology_config(
	topology_handle              = topology_1_handle,
	device_group_name            = "{Device Group 1}",
	device_group_multiplier      = "10",
	device_group_enabled         = "1",
)
if dg_1['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % dg_1['log']
    quit()

deviceGroup_1_handle = dg_1['device_group_handle']
	
    
mv1 = ixiangpf.multivalue_config(
    pattern                = 'value_list',
    values_file            = file_param,
    values_file_type       = 'csv',
    values_file_column_index = 1,
    nest_owner             = topology_1_handle,
    nest_enabled           = '1',
)
if mv1['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv1['log']
    quit()

multivalue_1_handle = mv1['multivalue_handle']


mv2 = ixiangpf.multivalue_config(
    pattern           = "custom",
    nest_step         = "1",
    nest_owner        = topology_1_handle,
    nest_enabled      = "0",
)
if mv2['status'] != IxiaHlt.SUCCESS:
   print "FAIL: %sn" % mv2['log']
   quit()

multivalue_2_handle = mv2['multivalue_handle']

mv3 = ixiangpf.multivalue_config(
    multivalue_handle      = multivalue_2_handle,
    custom_start           = "1",
    custom_step            = "1",
)
if mv3['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv3['log']
    quit()

custom_1_handle = mv3['custom_handle']

mv4 = ixiangpf.multivalue_config(
    custom_handle               = custom_1_handle,
    custom_increment_value      = "0",
    custom_increment_count      = "3",
)
if mv4['status'] != IxiaHlt.SUCCESS:
   print "FAIL: %sn" % mv4['log']
   quit()

increment_1_handle = mv4['increment_handle']


mv_mtu = ixiangpf.multivalue_config(
    pattern                = 'value_list',
    values_file            = file_param,
    values_file_type       = 'csv',
    values_file_column_index = 0,
    nest_owner             = topology_1_handle,
    nest_enabled           = '1',
)

if mv_mtu['status'] != IxiaHlt.SUCCESS:
   print "FAIL: %sn" % mv_mtu['log']
   quit()

mtu_handle = mv_mtu['multivalue_handle']

intf1 = ixiangpf.interface_config(
    protocol_name                = "{Ethernet 1}",
    protocol_handle              = deviceGroup_1_handle,
    mtu                          = mtu_handle,
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
if intf1['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % intf1['log']
    quit()
ethernet_1_handle = intf1['ethernet_handle']

mv5 = ixiangpf.multivalue_config(
    pattern           = "custom",
    nest_step         = "0.1.0.0",
    nest_owner        = topology_1_handle,
    nest_enabled      = "1",
)
if mv5['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv5['log']
    quit()

multivalue_3_handle = mv5['multivalue_handle']

mv6 = ixiangpf.multivalue_config(
    multivalue_handle      = multivalue_3_handle,
    custom_start           = "100.1.0.2",
    custom_step            = "0.0.1.0",
)
if mv6['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv6['log']
    quit()

custom_2_handle = mv6['custom_handle']

mv7 = ixiangpf.multivalue_config(
    custom_handle               = custom_2_handle,
    custom_increment_value      = "0.0.0.1",
    custom_increment_count      = "3",
)
if mv7['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv7['log']
    quit()

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
    print "FAIL: %sn" % mv8['log']
    quit()

multivalue_4_handle = mv8['multivalue_handle']

mv9 = ixiangpf.multivalue_config(
    multivalue_handle      = multivalue_4_handle,
    custom_start           = "100.1.0.5",
    custom_step            = "0.0.1.0",
)
if mv9['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv9['log']
    quit()

custom_3_handle = mv9['custom_handle']

mv10 = ixiangpf.multivalue_config(
    custom_handle               = custom_3_handle,
    custom_increment_value      = "0.0.0.0",
    custom_increment_count      = "3",
)
if mv10['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv10['log']
    quit()

increment_3_handle = mv10['increment_handle']

intf2 = ixiangpf.interface_config(
    protocol_name                     = "{IPv4 1}",
    protocol_handle                   = ethernet_1_handle,
    ipv4_resolve_gateway              = "1",
    ipv4_manual_gateway_mac           = "00.00.00.00.02.01",
    ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
    gateway                           = multivalue_4_handle,
    intf_ip_addr                      = multivalue_3_handle,
    netmask                           = "255.255.255.0",
)
if intf2['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % intf2['log']
    quit()


ipv4_1_handle = intf2['ipv4_handle']


top_2 = ixiangpf.topology_config(
    topology_name      = "{Topology 2}",
    port_handle        = ports[1],
)
if top_2['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % top_2['log']
    quit()

topology_2_handle = top_2['topology_handle']

dg_2 = ixiangpf.topology_config(
    topology_handle              = topology_2_handle,
    device_group_name            = "{Device Group 2}",
    device_group_multiplier      = "10",
    device_group_enabled         = "1",
)
if dg_2['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % dg_2['log']
    quit()

deviceGroup_2_handle = dg_2['device_group_handle']


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
    print "FAIL: %sn" % mv11['log']
    quit()

multivalue_5_handle = mv11['multivalue_handle']

mv12 = ixiangpf.multivalue_config(
    pattern           = "custom",
    nest_step         = "1",
    nest_owner        = topology_2_handle,
    nest_enabled      = "0",
)
if mv12['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv12['log']
    quit()

multivalue_6_handle = mv12['multivalue_handle']

mv13 = ixiangpf.multivalue_config(
    multivalue_handle      = multivalue_6_handle,
    custom_start           = "1",
    custom_step            = "1",
)
if mv13['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv13['log']
    quit()

custom_4_handle = mv13['custom_handle']

mv14 = ixiangpf.multivalue_config(
    custom_handle               = custom_4_handle,
    custom_increment_value      = "0",
    custom_increment_count      = "3",
)
if mv14['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv14['log']
    quit()

increment_4_handle = mv14['increment_handle']

intf3 = ixiangpf.interface_config(
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
if intf3['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % intf3['log']
    quit()

ethernet_2_handle = intf3['ethernet_handle']

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
    print "FAIL: %sn" % mv15['log']
    quit()

multivalue_7_handle = mv15['multivalue_handle']

mv16 = ixiangpf.multivalue_config(
    multivalue_handle      = multivalue_7_handle,
    custom_start           = "100.1.0.5",
    custom_step            = "0.0.1.0",
)
if mv16['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv16['log']
    quit()

custom_5_handle = mv16['custom_handle']

mv17 = ixiangpf.multivalue_config(
    custom_handle               = custom_5_handle,
    custom_increment_value      = "0.0.0.1",
    custom_increment_count      = "3",
)
if mv17['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv17['log']
    quit()

increment_5_handle = mv17['increment_handle']

mv18 = ixiangpf.multivalue_config(
    pattern           = "custom",
    nest_step         = "0.1.0.0",
    nest_owner        = topology_2_handle,
    nest_enabled      = "1",
)
if mv18['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv18['log']
    quit()

multivalue_8_handle = mv18['multivalue_handle']

mv19 = ixiangpf.multivalue_config(
    multivalue_handle      = multivalue_8_handle,
    custom_start           = "100.1.0.2",
    custom_step            = "0.0.1.0",
)
if mv19['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv19['log']
    quit()

custom_6_handle = mv19['custom_handle']

mv20 = ixiangpf.multivalue_config(
    custom_handle               = custom_6_handle,
    custom_increment_value      = "0.0.0.0",
    custom_increment_count      = "3",
)
if mv20['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv20['log']
    quit()

increment_6_handle = mv20['increment_handle']

intf4 = ixiangpf.interface_config(
    protocol_name                     = "{IPv4 2}",
    protocol_handle                   = ethernet_2_handle,
    ipv4_resolve_gateway              = "1",
    ipv4_manual_gateway_mac           = "00.00.00.00.01.01",
    ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
    gateway                           = multivalue_8_handle,
    intf_ip_addr                      = multivalue_7_handle,
    netmask                           = "255.255.255.0",
)
if intf4['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % intf4['log']
    quit()

ipv4_2_handle = intf4['ipv4_handle']


intf5 = ixiangpf.interface_config(
    protocol_handle                    = "/globals",
    arp_on_linkup                      = "0",
    single_arp_per_gateway             = "1",
    ipv4_send_arp_rate                 = "200",
    ipv4_send_arp_interval             = "1000",
    ipv4_send_arp_max_outstanding      = "400",
    ipv4_send_arp_scale_mode           = "port",
    ipv4_attempt_enabled               = "0",
    ipv4_attempt_rate                  = "200",
    ipv4_attempt_interval              = "1000",
    ipv4_attempt_scale_mode            = "port",
    ipv4_diconnect_enabled             = "0",
    ipv4_disconnect_rate               = "200",
    ipv4_disconnect_interval           = "1000",
    ipv4_disconnect_scale_mode         = "port",
    ipv4_re_send_arp_on_link_up        = "true",
)
if intf5['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % intf5['log']
    quit()


intf6 = ixiangpf.interface_config(
    protocol_handle                     = "/globals",
    ethernet_attempt_enabled            = "0",
    ethernet_attempt_rate               = "200",
    ethernet_attempt_interval           = "1000",
    ethernet_attempt_scale_mode         = "port",
    ethernet_diconnect_enabled          = "0",
    ethernet_disconnect_rate            = "200",
    ethernet_disconnect_interval        = "1000",
    ethernet_disconnect_scale_mode      = "port",
)
if intf6['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % intf6['log']
    quit()
    
    
start = ixiangpf.test_control(action='start_all_protocols')

if start['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % start['log']
    quit()	

print "Sleeping for 30 seconds ... "	
time.sleep(30)

print "Stopping all protocols ... "
stop = ixiangpf.test_control(action='stop_all_protocols')

if stop['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % stop['log']
    quit()	

print "Gather and print ethernet and ipv4 protocol_info stats (mode = aggregate) ... "    
#eth info    
eth_1_info = ixiangpf.protocol_info(
    handle = ethernet_1_handle,
    mode = 'aggregate',
)

if eth_1_info['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % eth_1_info['log']
    quit()
    
print " Ethernet info (port 0) ... \n"
pprint(eth_1_info)
     
eth_2_info = ixiangpf.protocol_info(
    handle = ethernet_2_handle,
    mode = 'aggregate',
)

if eth_2_info['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % eth_2_info['log']
    quit()

print " Ethernet info (port 1) ... \n"
pprint(eth_2_info)
    
#ipv4 info

ipv4_1_info = ixiangpf.protocol_info(
    handle = ipv4_1_handle,
    mode = 'aggregate',
)

if ipv4_1_info['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % ipv4_1_info['log']
    quit()
    
print " IPv4 info (port 0) ... \n"
pprint(ipv4_1_info)
    
ipv4_2_info = ixiangpf.protocol_info(
    handle = ipv4_2_handle,
    mode = 'aggregate',
)

if ipv4_2_info['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % ipv4_2_info['log']
    quit()
    
print " IPv4 info (port 1) ... \n"
pprint(ipv4_2_info)

print "Gather and print ethernet and ipv4 protocol_info stats (mode = handles) ... "   
#eth info    
eth_3_info = ixiangpf.protocol_info(
    handle = ethernet_1_handle,
    mode = 'handles',
)

if eth_3_info['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % eth_3_info['log']
    quit()
    
print " Ethernet info (port 0) ... \n"
pprint(eth_3_info)
     
eth_4_info = ixiangpf.protocol_info(
    handle = ethernet_2_handle,
    mode = 'handles',
)

if eth_4_info['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % eth_4_info['log']
    quit()

print " Ethernet info (port 1) ... \n"
pprint(eth_4_info)
    
#ipv4 info

ipv4_3_info = ixiangpf.protocol_info(
    handle = ipv4_1_handle,
    mode = 'handles',
)

if ipv4_3_info['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % ipv4_3_info['log']
    quit()
    
print " IPv4 info (port 0) ... \n"
pprint(ipv4_3_info)
    
ipv4_4_info = ixiangpf.protocol_info(
    handle = ipv4_2_handle,
    mode = 'handles',
)

if ipv4_4_info['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % ipv4_4_info['log']
    quit()
    
print " IPv4 info (port 1) ... \n"
pprint(ipv4_4_info)

print "\n\nScript ended SUCCESSFULLY!"