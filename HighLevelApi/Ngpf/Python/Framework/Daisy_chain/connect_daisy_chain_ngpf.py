#################################################################################
# Version 1    $Revision: 3 $
# $Author: RCsutak $
#
#    Copyright © 1997 - 2014 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    08-12-2014 RCsutak - created sample
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
#    This sample connects to a daisy chained topology and sets the chain	   # 
#    sequence and cable length for each slave, using the ixiangpf namespace.   #
# Module:                                                                      #
#    The sample was tested on a LSM XMVDC16NG module.                          #
#                                                                              #
################################################################################



from pprint import pprint
import os, sys
import time
import pdb

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
print dirname
print filename
logname = dirname + '\\log.log'

chassis_ip = ["ixro-hlt-xm2-02", "ixro-hlt-xm2-03","ixro-hlt-xm2-09"]
tcl_server = "localhost"
ixnetwork_tcl_server = 'localhost'
port_list = [['2/1'], ['2/3'], ['2/1']]
master_chassis = ['none',"ixro-hlt-xm2-02","ixro-hlt-xm2-02"]
chain_cables_length = [0,6,3]
chain_type = 'daisy'
chain_seq = [1,3,2]
cfgErrors = 0

print "Printing connection variables ... "
print "test_name = %s" % filename
print 'chassis_ip =  %s' % chassis_ip
print "tcl_server = %s " % tcl_server
print "ixnetwork_tcl_server = %s" % ixnetwork_tcl_server
print "port_list = %s " % port_list



######################################
##  CONNECT WITHOUT SESSION RESUME  ##
######################################
connect_result = ixiangpf.connect(
        ixnetwork_tcl_server = ixnetwork_tcl_server,
        tcl_server = tcl_server,
        device = chassis_ip,
        port_list = port_list,
        break_locks = 1,
        reset = 1,
        master_device = master_chassis,
        chain_sequence = chain_seq,
        chain_cables_length = chain_cables_length,
    )

if connect_result['status'] != '1':
    print "FAIL:"
    print connect_result['log']
    quit()
print " Printing connection result"
pprint(connect_result)

check_master = connect_result['connection']['chassis'][chassis_ip[0]]['is_master_chassis']
check_slave1 = connect_result['connection']['chassis'][chassis_ip[1]]['is_master_chassis']
check_slave2 = connect_result['connection']['chassis'][chassis_ip[2]]['is_master_chassis']
check_master_of_slave1 = connect_result['connection']['chassis'][chassis_ip[1]]['chassis_chain']['master_device']
check_master_of_slave2 = connect_result['connection']['chassis'][chassis_ip[2]]['chassis_chain']['master_device']
cable_length1 = connect_result['connection']['chassis'][chassis_ip[1]]['chassis_chain']['cable_length']
cable_length2 = connect_result['connection']['chassis'][chassis_ip[2]]['chassis_chain']['cable_length']


print "Master set is : %s\n" % check_master_of_slave1
if check_slave1 == '0':
	print "First slave is %s\n" % chassis_ip[1]
if check_slave2 == '0':
	print "Second slave is %s\n" % chassis_ip[2]
      
ports = connect_result['vport_list'].split()

top_1 = ixiangpf.topology_config(
	topology_name      = "{Topology 1}",
	port_handle        = ports[0],
)
if top_1['status'] != IxiaHlt.SUCCESS:
    print "FAIL:"
    print top_1['log']
    quit()    
	
top_1_handle = top_1['topology_handle']
	
dg_1 = ixiangpf.topology_config(
	topology_handle              = top_1_handle,
	device_group_name            = "{Device Group 1}",
	device_group_multiplier      = "10",
	device_group_enabled         = "1",
)
if dg_1['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % dg_1['log']
    quit()

dg_1_handle = dg_1['device_group_handle']
	
mv_1 = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "00.11.01.00.00.01",
	counter_step           = "00.00.00.00.00.01",
	counter_direction      = "increment",
	nest_step              = "00.00.01.00.00.00",
	nest_owner             = top_1_handle,
	nest_enabled           = "1",
)
if mv_1['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % dg_1['log']
    quit()
	
	
mv_1_handle = mv_1['multivalue_handle']
	
intf_dg1 = ixiangpf.interface_config(
	protocol_name                = "{Ethernet 1}",
	protocol_handle              = dg_1_handle,
	mtu                          = "1500",
	src_mac_addr                 = mv_1_handle,
	vlan                         = "0",
	vlan_id                      = "1",
	vlan_id_step                 = "0",
	vlan_id_count                = "1",
	vlan_tpid                    = "0x8100",
	vlan_user_priority           = "0",
	vlan_user_priority_step      = "0",
	use_vpn_parameters           = "0",
	site_id                      = "0",
)
if intf_dg1['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % intf_dg1['log']
    quit()
    
eth_1_handle = intf_dg1['ethernet_handle']

mv_2 = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "100.1.0.2",
	counter_step           = "0.0.1.0",
	counter_direction      = "increment",
	nest_step              = "0.1.0.0",
	nest_owner             = top_1_handle,
	nest_enabled           = "1",
)
if mv_2['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv_2['log']
    quit()
	
mv_2_handle = mv_2['multivalue_handle']
	
mv_3 = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "100.1.0.1",
	counter_step           = "0.0.1.0",
	counter_direction      = "increment",
	nest_step              = "0.1.0.0",
	nest_owner             = top_1_handle,
	nest_enabled           = "1",
)
if mv_3['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv_3['log']
    quit()

mv_3_handle = mv_3['multivalue_handle']
	
intf_dg1_2 = ixiangpf.interface_config(
	protocol_name                     = "{IPv4 1}",
	protocol_handle                   = eth_1_handle,
	ipv4_resolve_gateway              = "1",
	ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
	ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
	gateway                           = mv_3_handle,
	intf_ip_addr                      = mv_2_handle,
	netmask                           = "255.255.255.0",
)
if intf_dg1_2['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % intf_dg1_2['log']
    quit()

ipv4_1_handle = intf_dg1_2['ipv4_handle']

	
top_2 = ixiangpf.topology_config(
	topology_name      = "{Topology 2}",
	port_handle        = ports[1],
)
if top_2['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % top_2['log']
    quit()
	
top_2_handle = top_2['topology_handle']

	
dg_2 = ixiangpf.topology_config(
	topology_handle              = top_2_handle,
	device_group_name            = "{Device Group 2}",
	device_group_multiplier      = "10",
	device_group_enabled         = "1",
)
if dg_2['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % dg_2['log']
    quit()
	
dg_2_handle = dg_2['device_group_handle']
	
mv_4 = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "00.12.01.00.00.01",
	counter_step           = "00.00.00.00.00.01",
	counter_direction      = "increment",
	nest_step              = "00.00.01.00.00.00",
	nest_owner             = top_2_handle,
	nest_enabled           = "1",
)
if mv_4['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv_4['log']
    quit()
	
mv_4_handle = mv_4['multivalue_handle']
	
intf_dg2 = ixiangpf.interface_config(
	protocol_name                = "{Ethernet 2}",
	protocol_handle              = dg_2_handle,
	mtu                          = "1500",
	src_mac_addr                 = mv_4_handle,
	vlan                         = "0",
	vlan_id                      = "1",
	vlan_id_step                 = "0",
	vlan_id_count                = "1",
	vlan_tpid                    = "0x8100",
	vlan_user_priority           = "0",
	vlan_user_priority_step      = "0",
	use_vpn_parameters           = "0",
	site_id                      = "0",
)
if intf_dg2['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % intf_dg2['log']
    quit()

eth_2_handle = intf_dg2['ethernet_handle']

	
mv_5 = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "101.1.0.2",
	counter_step           = "0.0.1.0",
	counter_direction      = "increment",
	nest_step              = "0.1.0.0",
	nest_owner             = top_2_handle,
	nest_enabled           = "1",
)
if mv_5['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv_5['log']
    quit()
    
mv_5_handle = mv_5['multivalue_handle']
	
mv_6 = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "101.1.0.1",
	counter_step           = "0.0.1.0",
	counter_direction      = "increment",
	nest_step              = "0.1.0.0",
	nest_owner             = top_2_handle,
	nest_enabled           = "1",
)
if mv_6['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % mv_6['log']
    quit()
	
mv_6_handle = mv_6['multivalue_handle']
	
intf_dg2_2 = ixiangpf.interface_config(
	protocol_name                     = "{IPv4 2}",
	protocol_handle                   = eth_2_handle,
	ipv4_resolve_gateway              = "1",
	ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
	ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
	gateway                           = mv_6_handle,
	intf_ip_addr                      = mv_5_handle,
	netmask                           = "255.255.255.0",
)
if intf_dg2_2['status'] != IxiaHlt.SUCCESS:
    print "FAIL: %sn" % intf_dg2_2['log']
    quit()	
	
ipv4_2_handle = intf_dg2_2['ipv4_handle']

if cfgErrors > 0:
    print "FAIL - The script has a total of %d errors\n" % cfgErrors
else :
    print "SUCCESS -  The script has ended with no errors!\n"
	
	# _result_ = ixiangpf.interface_config(
		# protocol_handle                    = "/globals",
		# arp_on_linkup                      = "0",
		# single_arp_per_gateway             = "1",
		# ipv4_send_arp_rate                 = "200",
		# ipv4_send_arp_interval             = "1000",
		# ipv4_send_arp_max_outstanding      = "400",
		# ipv4_send_arp_scale_mode           = "port",
		# ipv4_attempt_enabled               = "0",
		# ipv4_attempt_rate                  = "200",
		# ipv4_attempt_interval              = "1000",
		# ipv4_attempt_scale_mode            = "port",
		# ipv4_diconnect_enabled             = "0",
		# ipv4_disconnect_rate               = "200",
		# ipv4_disconnect_interval           = "1000",
		# ipv4_disconnect_scale_mode         = "port",
		# ipv4_re_send_arp_on_link_up        = "true",
	# )
	# if _result_['status'] != IxiaHlt.SUCCESS:
		# ixnHLT_errorHandler('interface_config', _result_)
	
	
	# _result_ = ixiangpf.interface_config(
		# protocol_handle                     = "/globals",
		# ethernet_attempt_enabled            = "0",
		# ethernet_attempt_rate               = "200",
		# ethernet_attempt_interval           = "1000",
		# ethernet_attempt_scale_mode         = "port",
		# ethernet_diconnect_enabled          = "0",
		# ethernet_disconnect_rate            = "200",
		# ethernet_disconnect_interval        = "1000",
		# ethernet_disconnect_scale_mode      = "port",
	# )
	# if _result_['status'] != IxiaHlt.SUCCESS:
		# ixnHLT_errorHandler('interface_config', _result_)
	
