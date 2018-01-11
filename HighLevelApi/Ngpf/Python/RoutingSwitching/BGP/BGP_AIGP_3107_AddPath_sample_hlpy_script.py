################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    06/10/2016 - Debarati Chakraborty  - created sample                       #
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
#    This script intends to demonstrate how to use NGPF BGP RFC 3107, Add-Path,#
#    AIGP APIs                                                                 #
#    About Topology:                                                           #
#       The scenario consists of two BGP peers.                                #
#       Each of them capable of carrying Label information for the attached    #
#       advertising Route Range. Unidirectional Traffic is created in between  #
#       the peers.                                                             #
#         Script Flow:                                                         #
#        Step 1. Creation of 2 BGP topologies with RFC3107 IPv4 MPLS, AIGP,    #
#                Add-Path Capabilities                                         #
#        Step 2. Start of protocol                                             #
#        Step 3. Protocol Stat display                                         #
#        Step 4. Learned Info display                                          #
#        Step 5. Configuration L2-L3 Traffic                                   #
#        Step 6. Apply and Start of L2-L3 traffic                              #
#        Step 7. Display of L2-L3  traffic Stats                               #
#        Step 8.Stop of L2-L3 traffic                                          #
#        Step 9.Stop of all protocols                                          #
# Ixia Software:                                                               #
#    IxOS      8.10-EA                                                         #
#    IxNetwork 8.10-EA-Update(3)                                               #
################################################################################
#                                                                              #
################################################################################

################################################################################
# Utils                                                                        #	
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

################################################################################
# Connection to the chassis, IxNetwork Tcl Server                              #
################################################################################
chassis_ip              = ['10.216.108.46']
tcl_server              = '10.216.25.8'
port_list               = [['1/3', '1/4']]
ixnetwork_tcl_server    = '10.216.25.8:8239';
cfgErrors               = 0

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
print(connect_result)

#Retrieving the port handles, in a list
ports = connect_result['vport_list'].split()

############################################################################################
# Configuring Topology, Device Group, Protocol Interfaces and other protocol configuration #
############################################################################################
# Creating a topology on first port
print "Adding topology 1 on port 1"
_result_ = ixiangpf.topology_config(
	topology_name      = """Topology 1""",
	port_handle        = ports[0],
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('topology_config', _result_)

topology_1_handle = _result_['topology_handle']

# Creating a device group in topology 
print "Creating device group 1 in topology 1" 
_result_ = ixiangpf.topology_config(
	topology_handle              = topology_1_handle,
	device_group_name            = """BGP_1 Device Group 1""",
	device_group_multiplier      = "1",
	device_group_enabled         = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('topology_config', _result_)

deviceGroup_1_handle = _result_['device_group_handle']
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "00.11.01.00.00.01",
	counter_step           = "00.00.00.00.00.01",
	counter_direction      = "increment",
	nest_step              = '%s' % ("00.00.01.00.00.00"),
	nest_owner             = '%s' % (topology_1_handle),
	nest_enabled           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)
	
multivalue_1_handle = _result_['multivalue_handle']

# Creating ethernet stack for the first Device Group 
print "Creating ethernet stack for the first Device Group"
_result_ = ixiangpf.interface_config(
	protocol_name                = """Ethernet 1""",
	protocol_handle              = deviceGroup_1_handle,
	mtu                          = "1500",
	src_mac_addr                 = multivalue_1_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', _result_)
	
ethernet_1_handle = _result_['ethernet_handle']

_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "100.1.0.2",
	counter_step           = "0.0.1.0",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
    nest_owner             = '%s' % (topology_1_handle),
	nest_enabled           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_2_handle = _result_['multivalue_handle']
	
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "100.1.0.1",
	counter_step           = "0.0.1.0",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
	nest_owner             = '%s' % (topology_1_handle),
	nest_enabled           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_3_handle = _result_['multivalue_handle']

# Creating IPv4 Stack on top of Ethernet Stack for the first Device Group                                 
print "Creating IPv4 Stack on top of Ethernet Stack for the first Device Group\n";	
_result_ = ixiangpf.interface_config(
	protocol_name                     = """IPv4 1""",
	protocol_handle                   = ethernet_1_handle,
	ipv4_resolve_gateway              = "1",
	ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
	ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
	gateway                           = multivalue_3_handle,
	intf_ip_addr                      = multivalue_2_handle,
	netmask                           = "255.255.255.0",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', _result_)
	
ipv4_1_handle = _result_['ipv4_handle']

_result_ = ixiangpf.multivalue_config(
	pattern                 = "single_value",
	single_value            = "0.0.0.0",
	nest_step               = '%s' % ("0.0.0.1"),
	nest_owner              = '%s' % (topology_1_handle),
	nest_enabled            = '%s' % ("0"),
	overlay_value           = '%s' % ("100.1.0.1"),
	overlay_value_step      = '%s' % ("100.1.0.1"),
	overlay_index           = '%s' % ("1"),
	overlay_index_step      = '%s' % ("0"),
	overlay_count           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_4_handle = _result_['multivalue_handle']

_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "192.0.0.1",
	counter_step           = "0.0.0.1",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
	nest_owner             = '%s' % (topology_1_handle),
	nest_enabled           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_5_handle = _result_['multivalue_handle']
	
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "00:01:01:00:00:01",
	counter_step           = "00:00:00:00:00:01",
	counter_direction      = "increment",
	nest_step              = '%s' % ("00:00:01:00:00:00"),
	nest_owner             = '%s' % (topology_1_handle),
	nest_enabled           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_6_handle = _result_['multivalue_handle']
	
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "192.0.0.1",
	counter_step           = "0.0.0.1",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
	nest_owner             = '%s' % (topology_1_handle),
	nest_enabled           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)
	
multivalue_7_handle = _result_['multivalue_handle']

# Creating BGP Stack on top of IPv4 stack
print "Creating BGP Stack on top of IPv4 stack in first topology on port 1"  
_result_ = ixiangpf.emulation_bgp_config(
	mode                                    = "enable",
	active                                  = "1",
	md5_enable                              = "0",
	handle                                  = ipv4_1_handle,
	ip_version                              = "4",
	remote_ip_addr                          = multivalue_4_handle,
	ipv4_capability_unicast_nlri            = "1",
	ipv4_filter_unicast_nlri                = "0",
	ipv4_filter_multicast_nlri              = "1",
	ipv4_capability_mpls_nlri               = "1",
	ipv4_filter_mpls_nlri                   = "1",
	ipv4_capability_mpls_vpn_nlri           = "1",
	ipv6_capability_unicast_nlri            = "1",
	ipv6_filter_unicast_nlri                = "1",
	ipv6_filter_multicast_nlri              = "1",
	ipv6_capability_mpls_nlri               = "1",
	ipv6_filter_mpls_nlri                   = "1",
	ipv6_capability_mpls_vpn_nlri           = "1",
	ipv4_mpls_add_path_mode                 = "sendonly",
	ipv6_mpls_add_path_mode                 = "sendonly",
	ipv4_unicast_add_path_mode              = "sendonly",
	ipv6_unicast_add_path_mode              = "sendonly",
	ipv4_mpls_capability                    = "1",
	capability_ipv4_mpls_add_path           = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_bgp_config', _result_)

bgpIpv4Peer_1_handle = _result_['bgp_handle']

# Creating multivalue for network group
print "Creating multivalue pattern for BGP network group on Port 1"			
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "205.1.0.1",
	counter_step           = "0.0.0.0",
	counter_direction      = "increment",
	nest_step              = '%s,%s' % ("0.0.0.1", "0.1.0.0"),
	nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
	nest_enabled           = '%s,%s' % ("0", "1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)
	
multivalue_8_handle = _result_['multivalue_handle']

# Creating BGP Network Group 
print "Creating BGP Network Group on Port 1"		
_result_ = ixiangpf.network_group_config(
	protocol_handle                      = deviceGroup_1_handle,
	protocol_name                        = """Network Group 1""",
	multiplier                           = "5",
	enable_device                        = "1",
	connected_to_handle                  = ethernet_1_handle,
	type                                 = "ipv4-prefix",
	ipv4_prefix_network_address          = multivalue_8_handle,
	ipv4_prefix_length                   = "24",
	ipv4_prefix_number_of_addresses      = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('network_group_config', _result_)
	
ipv4PrefixPools_1_handle = _result_['ipv4_prefix_pools_handle']
networkGroup_1_handle = _result_['network_group_handle']

# Creating multivalue for network group
print "Creating multivalue pattern for BGP network group on Port 1"		
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "1096",
	counter_step           = "10",
	counter_direction      = "increment",
	nest_step              = '%s,%s' % ("1", "1"),
	nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
	nest_enabled           = '%s,%s' % ("0", "0"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)
	
multivalue_9_handle = _result_['multivalue_handle']

_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "1111",
	counter_step           = "100",
	counter_direction      = "decrement",
	nest_step              = '%s,%s' % ("1", "0"),
	nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
	nest_enabled           = '%s,%s' % ("0", "1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)
	
multivalue_10_handle = _result_['multivalue_handle']
	
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "1048575",
	counter_step           = "10",
	counter_direction      = "decrement",
	nest_step              = '%s,%s' % ("1", "1"),
	nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
	nest_enabled           = '%s,%s' % ("0", "0"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)
	
multivalue_11_handle = _result_['multivalue_handle']

_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "1",
	counter_step           = "1",
	counter_direction      = "increment",
	nest_step              = '%s,%s' % ("1", "0"),
	nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
	nest_enabled           = '%s,%s' % ("0", "1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)
	
multivalue_12_handle = _result_['multivalue_handle']
	
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "1",
	counter_step           = "1",
	counter_direction      = "increment",
	nest_step              = '%s,%s' % ("1", "0"),
	nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
	nest_enabled           = '%s,%s' % ("0", "1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)
	
multivalue_13_handle = _result_['multivalue_handle']
	
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "0",
    counter_step           = "10",
	counter_direction      = "increment",
	nest_step              = '%s,%s' % ("1", "1"),
	nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
	nest_enabled           = '%s,%s' % ("0", "0"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_14_handle = _result_['multivalue_handle']
	
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "0",
	counter_step           = "1",
	counter_direction      = "decrement",
	nest_step              = '%s,%s' % ("1", "1"),
	nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
	nest_enabled           = '%s,%s' % ("0", "0"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_15_handle = _result_['multivalue_handle']

# Creating BGP Network Group
print "Creating BGP Network Group on Port 1\n";	
_result_ = ixiangpf.emulation_bgp_route_config(
	handle                                   = networkGroup_1_handle,
	mode                                     = "create",
	protocol_route_name                      = """BGP IP Route Range 1""",
	active                                   = "1",
	ipv4_unicast_nlri                        = "1",
	max_route_ranges                         = "5",
	ip_version                               = "4",
	prefix                                   = multivalue_8_handle,
	label_step                               = "1",
	label_start                              = multivalue_9_handle,
	enable_add_path                          = "1",
	add_path_id                              = multivalue_10_handle,
	advertise_as_bgp_3107                    = "1",
	label_end                                = multivalue_11_handle,
	enable_aigp                              = "1",
	no_of_tlvs                               = "2",
	aigp_type                                = ["aigptlv", "aigptlv"],
	aigp_value                               = [multivalue_14_handle, multivalue_15_handle],
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_bgp_route_config', _result_)

# Creating a topology on second port
print "Adding topology 2 on port 2"
	
_result_ = ixiangpf.topology_config(
	topology_name      = """Topology 2""",
	port_handle        = ports[1],
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('topology_config', _result_)

topology_2_handle = _result_['topology_handle']

# Creating a device group in topology 
print "Creating device group 2 in topology 2" 
_result_ = ixiangpf.topology_config(
	topology_handle              = topology_2_handle,
	device_group_name            = """BGP_2_Device Group 2""",
	device_group_multiplier      = "1",
	device_group_enabled         = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('topology_config', _result_)

deviceGroup_2_handle = _result_['device_group_handle']

_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "00.12.01.00.00.01",
	counter_step           = "00.00.00.00.00.01",
	counter_direction      = "increment",
	nest_step              = '%s' % ("00.00.01.00.00.00"),
	nest_owner             = '%s' % (topology_2_handle),
	nest_enabled           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_16_handle = _result_['multivalue_handle']

# Creating ethernet stack for the second Device Group 
print "Creating ethernet stack for the second Device Group"	
_result_ = ixiangpf.interface_config(
	protocol_name                = """Ethernet 2""",
	protocol_handle              = deviceGroup_2_handle,
	mtu                          = "1500",
	src_mac_addr                 = multivalue_16_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', _result_)
	
ethernet_2_handle = _result_['ethernet_handle']
	
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "100.1.0.1",
	counter_step           = "0.0.1.0",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
	nest_owner             = '%s' % (topology_2_handle),
	nest_enabled           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_17_handle = _result_['multivalue_handle']

_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "100.1.0.2",
	counter_step           = "0.0.1.0",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
	nest_owner             = '%s' % (topology_2_handle),
	nest_enabled           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)
	
multivalue_18_handle = _result_['multivalue_handle']

# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group                                 
print "Creating IPv4 Stack on top of Ethernet Stack for the second Device Group\n";
_result_ = ixiangpf.interface_config(
	protocol_name                     = """IPv4 2""",
	protocol_handle                   = ethernet_2_handle,
	ipv4_resolve_gateway              = "1",
	ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
	ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
	gateway                           = multivalue_18_handle,
	intf_ip_addr                      = multivalue_17_handle,
	netmask                           = "255.255.255.0",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', _result_)

ipv4_2_handle = _result_['ipv4_handle']
	
_result_ = ixiangpf.multivalue_config(
	pattern                 = "single_value",
    single_value            = "0.0.0.0",
	nest_step               = '%s' % ("0.0.0.1"),
	nest_owner              = '%s' % (topology_2_handle),
	nest_enabled            = '%s' % ("0"),
	overlay_value           = '%s' % ("100.1.0.2"),
	overlay_value_step      = '%s' % ("100.1.0.2"),
	overlay_index           = '%s' % ("1"),
	overlay_index_step      = '%s' % ("0"),
	overlay_count           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_19_handle = _result_['multivalue_handle']

_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "193.0.0.1",
	counter_step           = "0.0.0.1",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
	nest_owner             = '%s' % (topology_2_handle),
	nest_enabled           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_20_handle = _result_['multivalue_handle']

_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "00:01:02:00:00:01",
	counter_step           = "00:00:00:00:00:01",
	counter_direction      = "increment",
	nest_step              = '%s' % ("00:00:01:00:00:00"),
	nest_owner             = '%s' % (topology_2_handle),
	nest_enabled           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_21_handle = _result_['multivalue_handle']

_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "193.0.0.1",
	counter_step           = "0.0.0.1",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
	nest_owner             = '%s' % (topology_2_handle),
	nest_enabled           = '%s' % ("1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)
	
multivalue_22_handle = _result_['multivalue_handle']

# Creating BGP Stack on top of IPv4 stack
print "Creating BGP Stack on top of IPv4 stack in second topology on port 2"  
_result_ = ixiangpf.emulation_bgp_config(
	mode                                    = "enable",
	active                                  = "1",
	md5_enable                              = "0",
	handle                                  = ipv4_2_handle,
	ip_version                              = "4",
	remote_ip_addr                          = multivalue_19_handle,
    ipv4_capability_unicast_nlri            = "1",
	ipv4_filter_unicast_nlri                = "0",
	ipv4_filter_multicast_nlri              = "1",
	ipv4_capability_mpls_nlri               = "1",
	ipv4_filter_mpls_nlri                   = "1",
	ipv4_capability_mpls_vpn_nlri           = "1",
	ipv6_capability_unicast_nlri            = "1",
	ipv6_filter_unicast_nlri                = "1",
	ipv6_filter_multicast_nlri              = "1",
    ipv6_capability_mpls_nlri               = "1",
	ipv6_filter_mpls_nlri                   = "1",
	ipv6_capability_mpls_vpn_nlri           = "1",
	ipv4_mpls_add_path_mode                 = "receiveonly",
	ipv6_mpls_add_path_mode                 = "receiveonly",
	ipv4_unicast_add_path_mode              = "receiveonly",
	ipv6_unicast_add_path_mode              = "receiveonly",
	ipv4_mpls_capability                    = "1",
	capability_ipv4_mpls_add_path           = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_bgp_config', _result_)
	
bgpIpv4Peer_2_handle = _result_['bgp_handle']

# Creating multivalue for network group
print "Creating multivalue pattern for BGP network group on Port 2"			
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "206.1.0.1",
	counter_step           = "0.0.0.0",
	counter_direction      = "increment",
	nest_step              = '%s,%s' % ("0.0.0.1", "0.1.0.0"),
	nest_owner             = '%s,%s' % (deviceGroup_2_handle, topology_2_handle),
	nest_enabled           = '%s,%s' % ("0", "1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_23_handle = _result_['multivalue_handle']

# Creating BGP Network Group 
print "Creating BGP Network Group on Port 1"	
_result_ = ixiangpf.network_group_config(
	protocol_handle                      = deviceGroup_2_handle,
	protocol_name                        = """Network Group 2""",
	multiplier                           = "5",
	enable_device                        = "1",
	connected_to_handle                  = ethernet_2_handle,
	type                                 = "ipv4-prefix",
	ipv4_prefix_network_address          = multivalue_23_handle,
	ipv4_prefix_length                   = "24",
	ipv4_prefix_number_of_addresses      = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('network_group_config', _result_)

ipv4PrefixPools_2_handle = _result_['ipv4_prefix_pools_handle']
networkGroup_3_handle = _result_['network_group_handle']

# Creating multivalue for network group
print "Creating multivalue pattern for BGP network group on Port 2"			
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "1234",
	counter_step           = "1",
    counter_direction      = "increment",
	nest_step              = '%s,%s' % ("1", "0"),
	nest_owner             = '%s,%s' % (deviceGroup_2_handle, topology_2_handle),
	nest_enabled           = '%s,%s' % ("0", "1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_24_handle = _result_['multivalue_handle']

_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
    counter_start          = "1",
	counter_step           = "1",
	counter_direction      = "increment",
	nest_step              = '%s,%s' % ("1", "0"),
	nest_owner             = '%s,%s' % (deviceGroup_2_handle, topology_2_handle),
	nest_enabled           = '%s,%s' % ("0", "1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_25_handle = _result_['multivalue_handle']

_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "1",
	counter_step           = "1",
	counter_direction      = "increment",
	nest_step              = '%s,%s' % ("1", "0"),
	nest_owner             = '%s,%s' % (deviceGroup_2_handle, topology_2_handle),
	nest_enabled           = '%s,%s' % ("0", "1"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)
	
multivalue_26_handle = _result_['multivalue_handle']

# Creating BGP Network Group
print "Creating BGP Network Group on Port 2\n";		
_result_ = ixiangpf.emulation_bgp_route_config(
	handle                                   = networkGroup_3_handle,
	mode                                     = "create",
	protocol_route_name                      = """BGP IP Route Range 2""",
	active                                   = "1",
	ipv4_unicast_nlri                        = "1",
	max_route_ranges                         = "5",
	ip_version                               = "4",
	prefix                                   = multivalue_23_handle,
	label_step                               = "1",
	label_start                              = "16",
	enable_add_path                          = "1",
	add_path_id                              = multivalue_24_handle,
	advertise_as_bgp_3107                    = "1",
	label_end                                = "1048575",
	enable_aigp                              = "0",
	no_of_tlvs                               = "1",
	aigp_type                                = ["aigptlv"],
	aigp_value                               = ["0"],
)
		
print "Waiting 05 seconds before starting protocol(s) ..."
time.sleep(5)

############################################################################
# Start BGP protocol                                                       #
############################################################################    
_result_ = ixiangpf.test_control(action='start_all_protocols')
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', _result_)

print "Waiting for 45 seconds"
time.sleep(45)

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
print "Fetching BGP aggregated statistics on Port1"               
protostats = ixiangpf.emulation_bgp_info(\
    handle = bgpIpv4Peer_1_handle,
    mode   = 'stats')
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_bgp_info', protostats)

pprint(protostats)

print "Fetching BGP aggregated statistics on Port2"               
protostats = ixiangpf.emulation_bgp_info(\
    handle = bgpIpv4Peer_2_handle,
    mode   = 'stats')
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_bgp_info', protostats)

pprint(protostats)

############################################################################
# Enable IPv4 Learned Information Filter on the Fly                        #
############################################################################
print "Enabling IPv4 Unicast Learned Info Filter on Port1"
bgp_1_status = ixiangpf.emulation_bgp_config (
    handle                               = bgpIpv4Peer_1_handle,
    mode                                 = 'modify',
    ipv4_filter_unicast_nlri             = '1',
)
if bgp_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_bgp_config', bgp_1_status)

print "Enabling IPv4 Unicast Learned Info Filter on Port2"
bgp_1_status = ixiangpf.emulation_bgp_config (
    handle                               = bgpIpv4Peer_2_handle,
    mode                                 = 'modify',
    ipv4_filter_unicast_nlri             = '1',
)
if bgp_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_bgp_config', bgp_1_status)
	
################################################################################
# Applying changes one the fly                                                 #
################################################################################
print "Applying changes on the fly"
applyChanges = ixiangpf.test_control(
    handle = ipv4_1_handle,
    action = 'apply_on_the_fly_changes',)
if applyChanges['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', applyChanges)

time.sleep(10)
	
############################################################################
# Retrieve Learned Info                                                    #
############################################################################
print "Fetching IPv4 MPLS LearnedInfo on Port1"
bgpLearnedInfo = ixiangpf.emulation_bgp_info(\
    handle = bgpIpv4Peer_1_handle,
    mode   = 'learned_info');
if bgpLearnedInfo['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_bgp_info', bgpLearnedInfo)

pprint(bgpLearnedInfo)

print "Fetching IPv4 MPLS LearnedInfo on Port2"
bgpLearnedInfo = ixiangpf.emulation_bgp_info(\
    handle = bgpIpv4Peer_2_handle,
    mode   = 'learned_info');
if bgpLearnedInfo['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_bgp_info', bgpLearnedInfo)

pprint(bgpLearnedInfo)

############################################################################ 
# Configure L2-L3 traffic                                                  #
############################################################################
print "Configure L2-L3 traffic"
_result_ = ixiangpf.traffic_config(
    mode='create',
    traffic_generator='ixnetwork_540',
    endpointset_count=1,
    emulation_src_handle=networkGroup_3_handle,
    emulation_dst_handle=networkGroup_1_handle,
    track_by='sourceDestEndpointPair0 trackingenabled0',
    rate_pps=1000,
    frame_size=512,
)	
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_config', _result_)

############################################################################
#  Start L2-L3 & L4-L7 traffic configured earlier                          #
############################################################################
print "Running Traffic"
_result_ = ixiangpf.traffic_control(
    action='run',
    traffic_generator='ixnetwork_540',
    type=['l23']
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

print "Let the traffic run for 60 seconds"
time.sleep(60)

############################################################################
# Retrieve L2-L3 traffic stats                                     #
############################################################################
print "Retrieving L2-L3 traffic stats"
protostats = ixiangpf.traffic_stats(
    mode 				= 'all',
    traffic_generator 		        = 'ixnetwork_540',
    measure_mode 			= 'mixed')
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_stats', protostats)

pprint(protostats)

############################################################################
# Stop L2-L3 traffic started earlier                                       #
############################################################################
print "Stopping Traffic"
_result_ = ixiangpf.traffic_control(
    action='stop',
    traffic_generator='ixnetwork_540',
    type=['l23']
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

time.sleep(2)

############################################################################
# Stop all protocols                                                       #
############################################################################
print "Stopping all protocols"
_result_ = ixiangpf.test_control(action='stop_all_protocols')
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', _result_)

time.sleep(2)                  

print "!!! Test Script Ends !!!"
