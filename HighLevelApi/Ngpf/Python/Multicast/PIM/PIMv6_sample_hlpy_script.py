################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    01/19/2015 - Rupam Paul   - created sample                                #
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
#    This script intends to demonstrate how to use NGPF PIM API.               #
#                                                                              #
#    1. It will create 2 PIM topologies and Ipv6 Prefix Pool under             #
#       the network group(NG)                                                  #
#    2. Start the pim protocol.                                                #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Modify the Range type from "*G" to "SG" in the First and Second PIM    #
#       router.And apply changes On The Fly (OTF)                              #
#    6. Retrieve protocol learned info again and notice the difference with    #
#       previously retrieved learned info.                                     #
#    7. Configure L2-L3 traffic.                                               #
#    8. Start the L2-L3 traffic.                                               #
#    9. Retrieve L2-L3 traffic stats                                           #
#   10. Stop L2-L3 traffic.                                                    #
#   11. Stop all protocols.                                                    #
#                                                                              #
# Ixia Software:                                                               #
#    IxOS      6.80  EA                                                        #
#    IxNetwork 7.40  EA                                                        #
#                                                                              #
################################################################################

################################################################################
# Utilities                                                                    #
################################################################################

# Libraries to be included
# package require Ixia
# Other procedures used in the script, that do not use HL API configuration/control procedures

from pprint import pprint
import sys, os
import time, re

# Append paths to python APIs (Linux and Windows)

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

# End Utilities ################################################################

################################################################################
# Connection to the chassis, IxNetwork Tcl Server                              #
################################################################################
chassis_ip              = ['10.205.28.170']
tcl_server              = '10.205.28.170'
port_list               = [['1/7', '1/8']]
ixnetwork_tcl_server    = '10.205.28.41:8981';
cfgErrors 		= 0

print "Printing connection variables ... "
print 'chassis_ip =  %s' % chassis_ip
print "tcl_server = %s " % tcl_server
print "ixnetwork_tcl_server = %s" % ixnetwork_tcl_server
print "port_list = %s " % port_list

print "Connecting to chassis and client"
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

#Retrieving the port handles, in a list
ports = connect_result['vport_list'].split()


################################################################################
# Creating topology and device group                                           #
################################################################################

# Creating a topology on first port
print "Adding topology 1 on port 1" 
_result_ = ixiangpf.topology_config(
    topology_name      = """PIMv6 Topology 1""",
    port_handle        = ports[0],
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
topology_1_handle = _result_['topology_handle']

# Creating a device group in topology 
print "Creating device group 1 in topology 1"    
_result_ = ixiangpf.topology_config(
    topology_handle              = topology_1_handle,
    device_group_name            = """Device Group 1""",
    device_group_multiplier      = "1",
    device_group_enabled         = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
deviceGroup_1_handle = _result_['device_group_handle']

# Creating a topology on second port
print "Adding topology 2 on port 2"
_result_ = ixiangpf.topology_config(
    topology_name      = """PIMv6 Topology 2""",
    port_handle        = ports[1],
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)

topology_2_handle = _result_['topology_handle']

# Creating a device group in topology
print "Creating device group 2 in topology 2"
_result_ = ixiangpf.topology_config(
    topology_handle              = topology_2_handle,
    device_group_name            = """Device Group 2""",
    device_group_multiplier      = "1",
    device_group_enabled         = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)

deviceGroup_2_handle = _result_['device_group_handle']

################################################################################
#  Configure protocol interfaces                                               #
################################################################################

# Creating ethernet stack for the first Device Group 
print "Creating ethernet stack for the first Device Group"
_result_ = ixiangpf.interface_config(
    protocol_name                = """Ethernet 1""",
    protocol_handle              = deviceGroup_1_handle,
    mtu                          = "1500",
    src_mac_addr                 = "18.03.73.c7.6c.b1",
    src_mac_addr_step            = "00.00.00.00.00.00",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)
    
ethernet_1_handle = _result_['ethernet_handle']

# Creating ethernet stack for the second Device Group
print "Creating ethernet for the second Device Group"
_result_ = ixiangpf.interface_config(
    protocol_name                = """Ethernet 2""",
    protocol_handle              = deviceGroup_2_handle,
    mtu                          = "1500",
    src_mac_addr                 = "18.03.73.c7.6c.01",
    src_mac_addr_step            = "00.00.00.00.00.00",
 )
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)

ethernet_2_handle = _result_['ethernet_handle']

# Creating IPv6 Stack on top of Ethernet Stack for the first Device Group                                 
print "Creating IPv6 Stack on top of Ethernet Stack for the first Device Group"
_result_ = ixiangpf.interface_config(
    protocol_name                = """IPv6 1""",
    protocol_handle              = ethernet_1_handle,
    ipv6_multiplier              = "1",
    ipv6_resolve_gateway         = "1",
    ipv6_manual_gateway_mac      = "00.00.00.00.00.01",
    ipv6_manual_gateway_mac_step = "00.00.00.00.00.00",
    ipv6_gateway                 = "2000:0:0:0:0:0:0:1",
    ipv6_gateway_step            = "::0",
    ipv6_intf_addr               = "2000:0:0:0:0:0:0:2",
    ipv6_intf_addr_step          = "::0",
    ipv6_prefix_length           = "64",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)
    
ipv6_1_handle = _result_['ipv6_handle']

# Creating IPv6 Stack on top of Ethernet Stack for the second Device Group 
print "Creating IPv6 2 stack on ethernet 2 stack for the second Device Group"
_result_ = ixiangpf.interface_config(
    protocol_name                = """IPv6 2""",
    protocol_handle              = ethernet_2_handle,
    ipv6_multiplier              = "1",
    ipv6_resolve_gateway         = "1",
    ipv6_manual_gateway_mac      = "00.00.00.00.00.01",
    ipv6_manual_gateway_mac_step = "00.00.00.00.00.00",
    ipv6_gateway                 = "2000:0:0:0:0:0:0:2",
    ipv6_gateway_step            = "::0",
    ipv6_intf_addr               = "2000:0:0:0:0:0:0:1",
    ipv6_intf_addr_step          = "::0",
    ipv6_prefix_length           = "64",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)

ipv6_2_handle = _result_['ipv6_handle']


################################################################################
# Other protocol configurations                                                # 
################################################################################

# This will Create PIMv6 Stack on top of IPv6 Stack of Topology1

print "Creating PIMv6 Stack on top of IPv6 1 stack"
_result_ = ixiangpf.emulation_pim_config(
    mode                           = "create",
	handle                         = ipv6_1_handle,
	ip_version                     = "6",
	)
		
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_pim_config', _result_)
	
pimV6Interface_1_handle = _result_['pim_v6_interface_handle']

#Creating Multicast Group address

print "Creating Multicast Group address"
_result_ = ixiangpf.emulation_multicast_group_config(
	mode               = "create",
	ip_addr_start      = "ff15:0:0:0:0:0:0:1",
	num_groups         = "1",
	active             = "1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_group_config', _result_)
	
pimV6JoinPruneList_1_handle_group = _result_['multicast_group_handle']
        
#Creating Multicast Source address

print "Creating Multicast Source address"	
_result_ = ixiangpf.emulation_multicast_source_config(
	mode               = "create",
	ip_addr_start      = "4:0:0:0:0:0:0:1",
	num_sources        = "1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_source_config', _result_)
	
pimV6JoinPruneList_1_handle_source = _result_['multicast_source_handle']
	
#Creating PIM Join-Prune List
print "Creating Join Prune List"	
_result_ = ixiangpf.emulation_pim_group_config(
	mode                               = "create",
	session_handle                     = pimV6Interface_1_handle,
	group_pool_handle                  = pimV6JoinPruneList_1_handle_group,
	source_pool_handle                 = pimV6JoinPruneList_1_handle_source,
	rp_ip_addr                         = "3000:0:0:0:0:0:0:1",
	group_pool_mode                    = "send",
	join_prune_aggregation_factor      = "1",
	flap_interval                      = "60",
	register_stop_trigger_count        = "10",
	source_group_mapping               = "fully_meshed",
	switch_over_interval               = "5",
	group_range_type                   = "startogroup",
	enable_flap_info                   = "false",
	prune_source_address               = "0:0:0:0:0:0:0:0",
	prune_source_mask_width            = "32",
	prune_source_address_count         = "0",
	join_prune_group_mask_width        = "32",
	join_prune_source_mask_width       = "32",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_pim_group_config', _result_)
	
pimV6JoinPruneList_1_handle = _result_['pim_v6_join_prune_handle']
 
#Creating Multicast Group address

print "Creating Multicast Group address" 
_result_ = ixiangpf.emulation_multicast_group_config(
	mode               = "create",
	ip_addr_start      = "ff15:0:0:0:0:0:0:0",
	num_groups         = "1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_pim_group_config', _result_)
	
pimV6SourcesList_1_handle_group = _result_['multicast_group_handle']
 
#Creating Multicast Source address

print "Creating Multicast Source address" 
_result_ = ixiangpf.emulation_multicast_source_config(
	mode               = "create",
	ip_addr_start      = "fec0:0:0:0:0:0:0:1",
	num_sources        = "1",
	active             = "1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_pim_group_config', _result_)
	
pimV6SourcesList_1_handle_source = _result_['multicast_source_handle']
	
#Creating PIM Source List
 
print "Creating PIM Source List"  
_result_ = ixiangpf.emulation_pim_group_config(
	mode                               = "create",
	session_handle                     = pimV6Interface_1_handle,
	group_pool_handle                  = pimV6SourcesList_1_handle_group,
	source_pool_handle                 = pimV6SourcesList_1_handle_source,
	rp_ip_addr                         = "0:0:0:0:0:0:0:0",
	group_pool_mode                    = "register",
	register_tx_iteration_gap          = "30000",
	register_udp_destination_port      = "3000",
	register_udp_source_port           = "3000",
	switch_over_interval               = "0",
	send_null_register                 = "0",
	discard_sg_join_states             = "true",
	multicast_data_length              = "64",
	supression_time                    = "60",
	register_probe_time                = "5",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_pim_group_config', _result_)
	
pimV6SourcesList_1_handle = _result_['pim_v6_source_handle']
  
#Creating Group Address for Candidate RP 

print "Creating Group Address for Candidate RP" 
_result_ = ixiangpf.emulation_multicast_group_config(
	mode               = "create",
	ip_addr_start      = "ff15:0:0:0:0:0:0:1",
	num_groups         = "1",
	active             = "1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_group_config', _result_)
	
pimV6CandidateRPsList_1_handle = _result_['multicast_group_handle']
	
#Creating PIM Candidate RP List
  
print "Creating PIM Candidate RP List"  
_result_ = ixiangpf.emulation_pim_group_config(
	mode                       = "create",
	session_handle             = pimV6Interface_1_handle,
	group_pool_handle          = pimV6CandidateRPsList_1_handle,
	adv_hold_time              = "150",
	back_off_interval          = "3",
	crp_ip_addr                = "fec0:0:0:0:0:0:0:1",
	group_pool_mode            = "candidate_rp",
	periodic_adv_interval      = "60",
	pri_change_interval        = "60",
	pri_type                   = "same",
	pri_value                  = "180",
	router_count               = "1",
	source_group_mapping       = "fully_meshed",
	trigger_crp_msg_count      = "3",
	crp_group_mask_len         = "32",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_pim_group_config', _result_)
	
pimV6CandidateRPsList_1_handle = _result_['pim_v6_candidate_rp_handle']
	
#Creating and Adding IPv6-prefix pool under Network Group1

print "Creating ipv6 prefix network address"
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "3000:0:1:1:0:0:0:0",
	counter_step           = "0:0:0:1:0:0:0:0",
	counter_direction      = "increment",
	nest_step              = "0:0:0:0:0:0:0:1,0:0:1:0:0:0:0:0",
	nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
	nest_enabled           = "0,1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', _result_)
	
multivalue_2_handle = _result_['multivalue_handle']

print "Creating and Adding IPv6-prefix pool under Network Group1"	
_result_ = ixiangpf.network_group_config(
	protocol_handle                      = deviceGroup_1_handle,
	protocol_name                        = """Network Group 1""",
	multiplier                           = "1",
	enable_device                        = "1",
	connected_to_handle                  = ethernet_1_handle,
	type                                 = "ipv6-prefix",
	ipv6_prefix_network_address          = multivalue_2_handle,
	ipv6_prefix_length                   = "24",
	ipv6_prefix_number_of_addresses      = "1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('network_group_config', _result_)
	
networkGroup_1_handle = _result_['network_group_handle']
ipv6PrefixPools_1_handle = _result_['ipv6_prefix_pools_handle']
		        
         
# This will Create PIMv6 Stack on top of IPv6 Stack of Topology1

print "Creating PIMv6 Stack on top of IPv6 Stack of Topology2"	 
_result_ = ixiangpf.emulation_pim_config(
	mode                           = "create",
	handle                         = ipv6_2_handle,
	ip_version                     = "6",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_pim_config', _result_)
	
pimV6Interface_2_handle = _result_['pim_v6_interface_handle']
 
#Creating Multicast Group address

print "Creating Multicast Group address" 
_result_ = ixiangpf.emulation_multicast_group_config(
	mode               = "create",
	ip_addr_start      = "ff16:0:0:0:0:0:0:1",
	num_groups         = "1",
	active             = "1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_group_config', _result_)
	
pimV6JoinPruneList_5_handle_group = _result_['multicast_group_handle']
	
#Creating Multicast Source address

print "Creating Multicast Source address"       
_result_ = ixiangpf.emulation_multicast_source_config(
	mode               = "create",
	ip_addr_start      = "fec0:0:0:0:0:0:0:1",
	num_sources        = "1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_source_config', _result_)
	
pimV6JoinPruneList_5_handle_source = _result_['multicast_source_handle']
	
#Creating PIM Join Prune List

print "Creating PIM Join Prune List"       
_result_ = ixiangpf.emulation_pim_group_config(
	mode                               = "create",
	session_handle                     = pimV6Interface_2_handle,
	group_pool_handle                  = pimV6JoinPruneList_5_handle_group,
	source_pool_handle                 = pimV6JoinPruneList_5_handle_source,
	rp_ip_addr                         = "3000:0:0:0:0:0:0:1",
	group_pool_mode                    = "send",
	join_prune_aggregation_factor      = "1",
	flap_interval                      = "60",
	register_stop_trigger_count        = "10",
	source_group_mapping               = "fully_meshed",
	switch_over_interval               = "5",
	group_range_type                   = "startogroup",
	enable_flap_info                   = "false",
	prune_source_address               = "0:0:0:0:0:0:0:0",
	prune_source_mask_width            = "32",
	prune_source_address_count         = "0",
	join_prune_group_mask_width        = "32",
	join_prune_source_mask_width       = "32",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_pim_group_config', _result_)
	
pimV6JoinPruneList_2_handle = _result_['pim_v6_join_prune_handle']

#Creating Group address for Join-Prune list 

print "Creating Group address for Join-Prune list"       
_result_ = ixiangpf.emulation_multicast_group_config(
	mode               = "create",
	ip_addr_start      = "ff15:0:0:0:0:0:0:0",
	num_groups         = "1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_group_config', _result_)
	
pimV6SourcesList_5_handle_group = _result_['multicast_group_handle']

#Creating Source address for Join-Prune list 

print "Creating Source address for Join-Prune list"         
_result_ = ixiangpf.emulation_multicast_source_config(
	mode               = "create",
	ip_addr_start      = "fec0:0:0:0:0:0:0:1",
	num_sources        = "1",
	active             = "1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_source_config', _result_)
	
pimV6SourcesList_5_handle_source = _result_['multicast_source_handle']
	
#Creating PIM Source List
 
print "Creating PIM Source List" 
_result_ = ixiangpf.emulation_pim_group_config(
	mode                               = "create",
	session_handle                     = pimV6Interface_2_handle,
	group_pool_handle                  = pimV6SourcesList_5_handle_group,
	source_pool_handle                 = pimV6SourcesList_5_handle_source,
	rp_ip_addr                         = "0:0:0:0:0:0:0:0",
	group_pool_mode                    = "register",
	register_tx_iteration_gap          = "30000",
	register_udp_destination_port      = "3000",
	register_udp_source_port           = "3000",
	switch_over_interval               = "0",
	send_null_register                 = "0",
	discard_sg_join_states             = "true",
	multicast_data_length              = "64",
	supression_time                    = "60",
	register_probe_time                = "5",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_pim_group_config', _result_)
	
pimV6SourcesList_5_handle = _result_['pim_v6_source_handle']

#Creating Group Address for Candidate RP

print "Creating Group Address for Candidate RP"
_result_ = ixiangpf.emulation_multicast_group_config(
	mode               = "create",
	ip_addr_start      = "ff15:0:0:0:0:0:0:0",
	num_groups         = "1",
	active             = "1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_group_config', _result_)
	
pimV6CandidateRPsList_3_handle = _result_['multicast_group_handle']
	
#Creating PIM Candidate RP List      
 
print "Creating PIM Candidate RP List" 
_result_ = ixiangpf.emulation_pim_group_config(
	mode                       = "create",
	session_handle             = pimV6Interface_2_handle,
	group_pool_handle          = pimV6CandidateRPsList_3_handle,
	adv_hold_time              = "150",
	back_off_interval          = "3",
	crp_ip_addr                = "fec0:0:0:0:0:0:0:1",
	group_pool_mode            = "candidate_rp",
	periodic_adv_interval      = "60",
	pri_change_interval        = "60",
	pri_type                   = "same",
	pri_value                  = "190",
	router_count               = "1",
	source_group_mapping       = "fully_meshed",
	trigger_crp_msg_count      = "3",
	crp_group_mask_len         = "32",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_pim_group_config', _result_)
	
pimV6CandidateRPsList_3_handle = _result_['pim_v6_candidate_rp_handle']
	
# Creating and Adding IPv6-prefix pool under Network Group2

print "Creating ipv6 prefix network address"
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "3000:1:1:1:0:0:0:0",
	counter_step           = "0:0:0:1:0:0:0:0",
	counter_direction      = "increment",
	nest_step              = "0:0:0:0:0:0:0:1,0:0:1:0:0:0:0:0",
	nest_owner             = '%s,%s' % (deviceGroup_2_handle, topology_2_handle),
	nest_enabled           = "0,1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', _result_)
	
multivalue_4_handle = _result_['multivalue_handle']
 
print "Creating and Adding IPv6-prefix pool under Network Group2" 
_result_ = ixiangpf.network_group_config(
	protocol_handle                      = deviceGroup_2_handle,
	protocol_name                        = """Network Group 2""",
	multiplier                           = "1",
	enable_device                        = "1",
	connected_to_handle                  = ethernet_2_handle,
	type                                 = "ipv6-prefix",
	ipv6_prefix_network_address          = multivalue_4_handle,
	ipv6_prefix_length                   = "24",
	ipv6_prefix_number_of_addresses      = "1",
	)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('network_group_config', _result_)
	
networkGroup_2_handle = _result_['network_group_handle']
ipv6PrefixPools_2_handle = _result_['ipv6_prefix_pools_handle']
	
############################################################################
# Start PIM protocol                                                       #
############################################################################
	
print "Waiting 5 seconds before starting protocol(s) ..."
time.sleep(5)
	
print "Starting all protocol(s) ..."

_result_ = ixiangpf.test_control(action='start_all_protocols')

# Check status
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', protostats)
	
print "Waiting for 60 Seconds"
time.sleep(60)
	
############################################################################
# Retrieve protocol statistics                                             # 
############################################################################
print "fetching pimv6 aggregated statistics"
protostats = ixiangpf.emulation_pim_info(\
    handle = pimV6Interface_2_handle,
    mode   = 'aggregate',
    )

if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_pim_info', protostats)

pprint(protostats)
    
    	
############################################################################
# Retrieve protocol learned info                                           #
############################################################################
print "Fetching pim learned info"
protostats = ixiangpf.emulation_pim_info(\
    handle = pimV6Interface_1_handle,                                               
    mode   = 'learned_crp',
	)

if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_pim_info', protostats)

pprint(protostats)

  
	
############################################################################
# Modifying the GroupRange Type from *G to SG and Enabling Bootstrap       #
############################################################################

#Modifying the GroupRange Type from *G to SG for Topology1
print "Modifying the GroupRange Type from *G to SG for Topology1" 

_result_ = ixiangpf.emulation_pim_group_config(                                     
    handle            = pimV6JoinPruneList_1_handle,                                
    mode              = 'modify',                                                     
    group_range_type  = 'sourcetogroup',
	)
		
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_pim_group_config',_result_)

#Modifying the GroupRange Type from *G to SG for Topology2
print "Modifying the GroupRange Type from *G to SG for Topology2"
 
_result_ = ixiangpf.emulation_pim_group_config(                                     
    handle            = pimV6JoinPruneList_2_handle,                                
    mode              = 'modify',                                                      
    group_range_type  = 'sourcetogroup',
	)
	
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_pim_group_config', _result_)

#Enabling Bootstrap for Topology1    	
print "Enabling Bootstrap for Topology1"

_result_ = ixiangpf.emulation_pim_config(
    handle            = pimV6Interface_1_handle,                                    
    mode              = 'modify',
    ip_version        = '6',                                                      
    bootstrap_enable  =  '1',
	)
		
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_pim_config', _result_)
	
#Enabling Bootstrap and Modifying Priority for Topology2
print "Enabling Bootstrap and Modifying Priority for Topology2"

_result_ = ixiangpf.emulation_pim_config(\
    handle            = pimV6Interface_2_handle,                                    
    mode              = 'modify',
    ip_version        = '6',                                                      
    bootstrap_enable  = '1',                                              
	bootstrap_priority = '74',
	)
		
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_pim_config', _result_)
		
#Applying changes on the fly		
print "Applying changes on the fly"

applyChanges = ixiangpf.test_control(
   handle = pimV6Interface_1_handle,
   action = 'apply_on_the_fly_changes',
)
time.sleep(5)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('test_control', _result_)

#Applying changes on the fly
print "Applying changes on the fly"
applyChanges = ixiangpf.test_control(
   handle = pimV6Interface_2_handle,
   action = 'apply_on_the_fly_changes',
)
time.sleep(5)
if _result_['status'] != IxiaHlt.SUCCESS:
        ErrorHandler('test_control', _result_)
    
print "Waiting for 60 seconds"
time.sleep(60)
	
############################################################################
# Retrieve protocol learned info again after RangeType modification        #
############################################################################
print "Fetching pim learned info"
protostats = ixiangpf.emulation_pim_info(\
    handle = pimV6Interface_1_handle,                                               
    mode   = 'learned_crp',
	)

if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_pim_info', protostats)

pprint(protostats)
 	
############################################################################ 
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv6, Destination->Multicast group                #
# 2. Type      : Multicast IPv6 traffic                                    #
# 3. Flow Group: On IPv6 Destination Address                               #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : IPv6 Destination Address                                  #	
############################################################################

print "Configuring L2-L3 traffic"
_result_ = ixiangpf.traffic_config(
    mode                                        = 'create',
    traffic_generator                           = 'ixnetwork_540',
    endpointset_count                           = 1,
    emulation_src_handle                        = ipv6PrefixPools_1_handle,
    emulation_dst_handle                        = ipv6PrefixPools_2_handle,
    name                                        = 'Traffic_Item_1',
    circuit_endpoint_type                       = 'ipv6',
    transmit_distribution                       = 'ipv6DestIp0',                             
    rate_pps                                    = 1000,                                    
    frame_size                                  = 512,
    track_by                                    = 'trackingenabled0 ipv6DestIp0'
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_config', _result_)
	
	
############################################################################
#  Start L2-L3 traffic configured earlier                                  #
############################################################################
print "Running Traffic..."
_result_ = ixiangpf.traffic_control(
    action            = 'run',
    traffic_generator = 'ixnetwork_540',
    type              = 'l23',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

print "Let the traffic run for 20 seconds ..."
time.sleep(20)
	
	   
############################################################################                                 
# Retrieve L2-L3 traffic stats                                             #
############################################################################
print "Retrieving L2-L3 traffic stats"
trafficStats = ixiangpf.traffic_stats(
    mode              = 'all',
    traffic_generator = 'ixnetwork_540',
    measure_mode      = 'mixed',
)
if trafficStats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_stats', trafficStats)

pprint(trafficStats)
  
############################################################################
# Stop L2-L3 traffic started earlier                                       #
############################################################################
print "Stopping Traffic..."

_result_ = ixiangpf.traffic_control(
    action='stop',
    traffic_generator='ixnetwork_540',
    type='l23',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

time.sleep(5)
   
############################################################################
# Stop all protocols                                                       #
############################################################################
print "Stopping all protocol(s) ..."
stop = ixiangpf.test_control(action='stop_all_protocols')
if stop['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', stop)	

time.sleep(2)
       
print "!!! Test Script Ends !!!"
	
	
