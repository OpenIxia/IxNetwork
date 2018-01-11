################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    15/01/2015 - Poulomi Chatterjee - created sample                          #
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
#    This script intends to demonstrate how to use NGPF ISISL3 API.            #
#                                                                              #
#    1. It will create 2 ISISL3 topologies, each having an ipv4 & ipv6 network #
#       topology and loopback device group behind the network group(NG) with   #
#       loopback interface on it. A loopback device group(DG) behind network   #
#       group is needed to support applib traffic.                             #
#    2. Start the ISISL3 protocol.                                             #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Configure L2-L3 traffic (IPv4 & IPv6).                                 #
#    6. Configure application traffic for IPv4/IPv6 Profile. [global variable  #
#       "traffic_mode" selects the profile to be configured.                   #
#       Options are: 1(for IPv4) & 2(for IPv6)                                 #
#       Note: IPv4 & IPv6 both could not be configured in same endpoint set.   #
#    7. Start the L2-L3 traffic.                                               #
#    8. Start the application traffic.                                         #
#    9. Retrieve Appilcation traffic stats.                                    #
#   10. Retrieve L2-L3 traffic stats.                                          #
#   11. Stop L2-L3 traffic.                                                    #
#   12. Stop Application traffic.                                              #
#   13. Stop all protocols.                                                    #
# Ixia Software:                                                               #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
#                                                                              #
################################################################################

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
chassis_ip              = ['10.205.28.170']
tcl_server              = '10.205.28.170'
port_list               = [['1/7', '1/8']]
ixnetwork_tcl_server    = '10.205.28.41:8981';
cfgErrors               = 0

print "Printing connection variables ... "
print 'chassis_ip =  %s' % chassis_ip
print "tcl_server = %s " % tcl_server
print "ixnetwork_tcl_server = %s" % ixnetwork_tcl_server
print "port_list = %s " % port_list

print "Connect to chassis ..."
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

# Creating a topology in first port
print ('Adding topology:1 in port 1')    
_result_ = ixiangpf.topology_config(
        topology_name      = """ISIS Topology 1""",
        port_handle        = ports[0],
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
topology_1_handle = _result_['topology_handle']

# Creating a device group in topology
print "Creating device group 1 in topology 1\n"
_result_ = ixiangpf.topology_config(
        topology_handle              = topology_1_handle,
        device_group_name            = """Device Group 1""",
        device_group_multiplier      = "1",
        device_group_enabled         = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
deviceGroup_1_handle = _result_['device_group_handle']
    
# Creating a topology in second port
print "Adding topology 2 in port 2"    
_result_ = ixiangpf.topology_config(
        topology_name      = """ISIS Topology 2""",
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
    
deviceGroup_4_handle = _result_['device_group_handle']

################################################################################
#  Configure protocol interfaces                                               #
################################################################################

# Creating ethernet stack in device group
print "Creating ethernet stack in first device group"
_result_ = ixiangpf.interface_config(
        protocol_name                = """Ethernet 1""",
        protocol_handle              = deviceGroup_1_handle,
        mtu                          = "1500",
        src_mac_addr                 = "18.03.73.c7.6c.b2",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)
    
ethernet_1_handle = _result_['ethernet_handle']

# Creating ethernet stack in device group
print "Creating ethernet stack in second device group"
_result_ = ixiangpf.interface_config(
        protocol_name                = """Ethernet 2""",
        protocol_handle              = deviceGroup_4_handle,
        mtu                          = "1500",
        src_mac_addr                 = "18.03.73.c7.6c.b1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)

ethernet_2_handle = _result_['ethernet_handle']

    
# Creating IPv4 Stack on top of Ethernet Stack
print "Creating IPv4  stack on first ethernet stack"
_result_ = ixiangpf.interface_config(
        protocol_name                     = """IPv4 1""",
        protocol_handle                   = ethernet_1_handle,
        ipv4_resolve_gateway              = "1",
        ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
        ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
        gateway                           = "20.20.20.1",
        intf_ip_addr                      = "20.20.20.2",
        netmask                           = "255.255.255.0",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)
    
ipv4_1_handle = _result_['ipv4_handle']
    
# Creating IPv4 Stack on top of Ethernet Stack
print "Creating IPv4  stack on second ethernet stack"
_result_ = ixiangpf.interface_config(
        protocol_name                     = """IPv4 2""",
        protocol_handle                   = ethernet_2_handle,
        ipv4_resolve_gateway              = "1",
        ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
        ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
        gateway                           = "20.20.20.2",
        intf_ip_addr                      = "20.20.20.1",
        netmask                           = "255.255.255.0",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)

ipv4_2_handle = _result_['ipv4_handle']

################################################################################
# Other protocol configurations                                                #
################################################################################
################################################################################
# Creating  ISIS Stack on top of ethernet stack                                #
# Descrtiption of protocol arguments : discard_lsp: enables learning LSPs      #
#                                      intf_type: sets interface type          #
#                                      system_id: sets system id               #
#                                      protocol_name: sets prtoocol name       #
#                                      active: activates ISIS router           #
#                                      if_active: activates router interface   #
################################################################################
print "Creating ISIS Stack on top of ethernet 1 stack"
_result_ = ixiangpf.emulation_isis_config(
        mode                                 = "create",
        discard_lsp                          = "0",
        handle                               = ethernet_1_handle,
        intf_type                            = "ptop",
        routing_level                        = "L2",
        system_id                            = "64:01:00:01:00:00 ",
        protocol_name                        = """ISIS-L3 IF 1""",
        active                               = "1",
        if_active                            = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_isis_config', _result_)
    
isisL3_1_handle = _result_['isis_l3_handle']
    
# Creating ISIS Network Group in port 1
print "Creating ISIS IPv4 Network group in port 1"
_result_ = ixiangpf.network_group_config(
        protocol_handle                      = deviceGroup_1_handle,
        protocol_name                        = """ISIS Network Group 1""",
        enable_device                        = "1",
        connected_to_handle                  = ethernet_1_handle,
        type                                 = "ipv4-prefix",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('network_group_config', _result_)
    
networkGroup_1_handle = _result_['network_group_handle']
ipv4PrefixPools_1_handle = _result_['ipv4_prefix_pools_handle']
    
_result_ = ixiangpf.emulation_isis_network_group_config(
        handle                  = networkGroup_1_handle,
        mode                    = "modify",
        stub_router_origin      = "stub",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_isis_network_group_config', _result_)
    
    
_result_ = ixiangpf.topology_config(
        device_group_name            = """Device Group 3""",
        device_group_multiplier      = "1",
        device_group_enabled         = "1",
        device_group_handle          = networkGroup_1_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
deviceGroup_2_handle = _result_['device_group_handle']
    
# Creating ipv4 Loopback interface for applib traffic
print "Adding ipv4 loopback1 for applib traffic"    
_result_ = ixiangpf.interface_config(
        protocol_name            = """IPv4 Loopback 1""",
        protocol_handle          = deviceGroup_2_handle,
        enable_loopback          = "1",
        connected_to_handle      = networkGroup_1_handle,
        intf_ip_addr             = "4.4.4.4",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)
    
ipv4Loopback_1_handle = _result_['ipv4_loopback_handle']
    
# Creating ISIS Network group 3 for ipv6 ranges
print "Creating ISIS Network group 3 for ipv6 ranges"
_result_ = ixiangpf.network_group_config(
        protocol_handle                      = deviceGroup_1_handle,
        protocol_name                        = """ISIS Network Group 3""",
        connected_to_handle                  = ethernet_1_handle,
        type                                 = "ipv6-prefix",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('network_group_config', _result_)
    
networkGroup_3_handle = _result_['network_group_handle']
ipv6PrefixPools_1_handle = _result_['ipv6_prefix_pools_handle']
    
_result_ = ixiangpf.emulation_isis_network_group_config(
        handle                      = networkGroup_3_handle,
        mode                        = "modify",
        external_router_origin      = "stub",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_isis_network_group_config', _result_)
    
_result_ = ixiangpf.topology_config(
        device_group_name            = """Device Group 6""",
        device_group_multiplier      = "1",
        device_group_enabled         = "1",
        device_group_handle          = networkGroup_3_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
deviceGroup_3_handle = _result_['device_group_handle']
    
#Creating ipv6 loopback 1 interface for applib traffic
print "Adding ipv6 loopback1 for applib traffic"    
_result_ = ixiangpf.interface_config(
        protocol_name            = """IPv6 Loopback 2""",
        protocol_handle          = deviceGroup_3_handle,
        enable_loopback          = "1",
        connected_to_handle      = networkGroup_3_handle,
        ipv6_intf_addr           = "2222:0:1:0:0:0:0:1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)
    
ipv6Loopback_1_handle = _result_['ipv6_loopback_handle']
    
################################################################################
# Creating  ISIS Stack on top of ethernet stack                                #
# Descrtiption of protocol arguments : discard_lsp: enables learning LSPs      #
#                                      intf_type: sets interface type          #
#                                      system_id: sets system id               #
#                                      protocol_name: sets prtoocol name       #
#                                      active: activates ISIS router           #
#                                      if_active: activates router interface   #
################################################################################
print "Creating ISIS Stack on top of Ethernet 2 stack"
_result_ = ixiangpf.emulation_isis_config(
        mode                                 = "create",
        discard_lsp                          = "0",
        handle                               = ethernet_2_handle,
        intf_type                            = "ptop",
        routing_level                        = "L2",
        system_id                            = "65:01:00:01:00:00",
        protocol_name                        = """ISIS-L3 IF 2""",
        active                               = "1",
        if_active                            = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_isis_config', _result_)
isisL3_2_handle = _result_['isis_l3_handle']
    
# Creating IPv4 Prefix Ranges
print "Creating ISIS IPv4 Prefix Ranges"
_result_ = ixiangpf.network_group_config(
        protocol_handle                      = deviceGroup_4_handle,
        protocol_name                        = """ISIS Network Group 2""",
        multiplier                           = "1",
        enable_device                        = "1",
        connected_to_handle                  = ethernet_2_handle,
        type                                 = "ipv4-prefix",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('network_group_config', _result_)
    
networkGroup_5_handle = _result_['network_group_handle']
ipv4PrefixPools_3_handle = _result_['ipv4_prefix_pools_handle']
    
_result_ = ixiangpf.emulation_isis_network_group_config(
        handle                  = networkGroup_5_handle,
        mode                    = "modify",
        stub_router_origin      = "stub",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_isis_network_group_config', _result_)
    
# Creating a device group in topology for loopback interface
print "Creating device group 2 in topology 2 for loopback interface"
_result_ = ixiangpf.topology_config(
        device_group_name            = """Device Group 4""",
        device_group_multiplier      = "1",
        device_group_enabled         = "1",
        device_group_handle          = networkGroup_5_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
   
deviceGroup_5_handle = _result_['device_group_handle']
    
#Creating ipv4 loopback 2 for applib traffic
print "Adding ipv4 loopback2 for applib traffic"    
_result_ = ixiangpf.interface_config(
        protocol_name            = """IPv4 Loopback 2""",
        protocol_handle          = deviceGroup_5_handle,
        enable_loopback          = "1",
        connected_to_handle      = networkGroup_5_handle,
        intf_ip_addr             = "5.5.5.5",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)
    
ipv4Loopback_2_handle = _result_['ipv4_loopback_handle']
    
# Creating ISIS Prefix ranges
print "Creating ISIS IPv6 Prefix ranges"    
_result_ = ixiangpf.network_group_config(
        protocol_handle                      = deviceGroup_4_handle,
        protocol_name                        = """ISIS Network Group 4""",
        connected_to_handle                  = ethernet_2_handle,
        type                                 = "ipv6-prefix",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('network_group_config', _result_)
    
networkGroup_7_handle = _result_['network_group_handle']
ipv6PrefixPools_3_handle = _result_['ipv6_prefix_pools_handle']
    
_result_ = ixiangpf.emulation_isis_network_group_config(
        handle                      = networkGroup_7_handle,
        mode                        = "modify",
        external_router_origin      = "stub",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_isis_network_group_config', _result_)
    
# Creating a device group in topology for loopback interface
print "Creating device group 2 in topology 2 for loopback interface"
_result_ = ixiangpf.topology_config(
        device_group_name            = """Device Group 5""",
        device_group_multiplier      = "1",
        device_group_enabled         = "1",
        device_group_handle          = networkGroup_7_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
deviceGroup_6_handle = _result_['device_group_handle']
    
#Creating ipv6 loopback 2 for applib traffic
print "Adding ipv6 loopback2 for applib traffic"
_result_ = ixiangpf.interface_config(
        protocol_name            = """IPv6 Loopback 1""",
        protocol_handle          = deviceGroup_6_handle,
        enable_loopback          = "1",
        connected_to_handle      = networkGroup_7_handle,
        ipv6_multiplier          = "1",
        ipv6_intf_addr           = "2222:0:0:0:0:0:0:1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)
    
ipv6Loopback_2_handle = _result_['ipv6_loopback_handle']
    
print('Waiting 5 seconds before starting protocol(s) ...')
time.sleep(5)

############################################################################
# Start ISIS protocol                                                      #
############################################################################    
print ('Starting all protocol(s) ...')
	
_result_ = ixiangpf.test_control(action='start_all_protocols')
# Check status
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('ixiangpf.test_control', _result_)
time.sleep(60)

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
print ('Fetching ISIS aggregated statistics')               
protostats = ixiangpf.emulation_isis_info(\
        handle = isisL3_1_handle,
        mode   = 'stats')
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_info', protostats)

pprint(protostats)

################################################################################
# Configure_L2_L3_IPv4 traffic                                                 #
################################################################################
print ('Configuring L2-L3 IPv4 traffic item ...')
# Check status
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

_result_ = ixiangpf.traffic_config(
	    mode                    		    = 'create',
        traffic_generator            		= 'ixnetwork_540',
        endpointset_count            		= 1,
        emulation_src_handle            	= [[ipv4PrefixPools_1_handle]],
        emulation_dst_handle            	= [[ipv4PrefixPools_3_handle]],
        name                    		    = 'Traffic_Item_1',
        circuit_endpoint_type            	= 'ipv4',
        frame_size        	                = '512',
        rate_pps                            = '1000',
        track_by                            = 'trackingenabled0 ipv4DestIp0',
)
    
config_elements = ixiatcl.convert_tcl_list(_result_['traffic_item'])
current_config_element = config_elements[0]
    
print ('Configured L2-L3 IPv4 traffic item!!!')


################################################################################
# Configure_L2_L3_IPv6 traffic                                                 #
################################################################################
print ('Configuring L2-L3 IPv6 traffic item ...')
# Check status
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

_result_ = ixiangpf.traffic_config(
	    mode                    		    = 'create',
        traffic_generator            		= 'ixnetwork_540',
        endpointset_count            		= 1,
        emulation_src_handle            	= [[ipv6PrefixPools_1_handle]],
        emulation_dst_handle            	= [[ipv6PrefixPools_3_handle]],
        name                    		    = 'Traffic_Item_2',
        tag_filter                		    = [[]],
        merge_destinations            		= '1',
        circuit_endpoint_type            	= 'ipv6',
        pending_operations_timeout        	= '30'
)
    
config_elements = ixiatcl.convert_tcl_list(_result_['traffic_item'])
current_config_element = config_elements[0]
    
_result_ = ixiangpf.traffic_config(
        mode                 = 'modify',
        traffic_generator    = 'ixnetwork_540',
    	stream_id            = current_config_element,
        track_by             = 'trackingenabled0 ipv6DestIp0',
)

print ('Configured L2-L3 IPv6 traffic item!!!')

################################################################################
# Configure_L4_L7_IPv4                                                         #
################################################################################
# Set applib traffic mode
print "Set applib traffic mode in variable traffic_mode, for IPv4: 1, IPv6: 2"
traffic_mode = 1

if traffic_mode == 1:
    print "Traffic mode is set to : 1"
    print "Configuring L4-L7 IPv4 traffic item ..."
    # Configure_L4_L7_IPv4 applib profiles
    _result_ = ixiangpf.traffic_l47_config(
        mode                        = "create",
        name                        = """Traffic Item 3""",
        circuit_endpoint_type       = "ipv4_application_traffic",
        emulation_src_handle        = networkGroup_1_handle,
        emulation_dst_handle        = networkGroup_5_handle,
        objective_type              = "users",
        objective_value             = "100",
        objective_distribution      = "apply_full_objective_to_each_port",
        enable_per_ip_stats         = "0",
        flows                       = ["Bandwidth_BitTorrent_File_Download", "Bandwidth_eDonkey Bandwidth_HTTP Bandwidth_IMAPv4", "Bandwidth_Telnet","Bandwidth_uTorrent_DHT_File_Download", "BBC_iPlayer BBC_iPlayer_Radio", "BGP_IGP_Open_Advertise_Routes", "BGP_IGP_Withdraw_Routes", "Bing_Search", "BitTorrent_Ares_v217_File_Download", "BitTorrent_BitComet_v126_File_Download"],
    )

    if _result_['status'] != IxiaHlt.SUCCESS:
        ErrorHandler('traffic_l47_config', _result_)
	
    trafficItem_1_handle = _result_['traffic_l47_handle']

elif traffic_mode == 2:
    print "Traffic mode is set to : 2"
    print "Configuring L4-L7 IPv6 traffic item ..."
    # Configure_L4_L7_IPv6 applib profiles
    _result_ = ixiangpf.traffic_l47_config(
        mode                        = "create",
        name                        = """Traffic Item 4""",
        circuit_endpoint_type       = "ipv6_application_traffic",
        emulation_src_handle        = networkGroup_3_handle,
        emulation_dst_handle        = networkGroup_7_handle,
        objective_type              = "users",
        objective_value             = "100",
        objective_distribution      = "apply_full_objective_to_each_port",
        enable_per_ip_stats         = "0",
        flows                       = ["Bandwidth_BitTorrent_File_Download", "Bandwidth_eDonkey Bandwidth_HTTP Bandwidth_IMAPv4", "Bandwidth_Telnet","Bandwidth_uTorrent_DHT_File_Download", "BBC_iPlayer BBC_iPlayer_Radio", "BGP_IGP_Open_Advertise_Routes", "BGP_IGP_Withdraw_Routes", "Bing_Search", "BitTorrent_Ares_v217_File_Download", "BitTorrent_BitComet_v126_File_Download"],
    )

    if _result_['status'] != IxiaHlt.SUCCESS:
        ErrorHandler('traffic_l47_config', _result_)
	
    trafficItem_1_handle = _result_['traffic_l47_handle']
	
############################################################################
#  Start L2-L3 traffic configured earlier                                  #
############################################################################
print ('Running Traffic...')
_result_ = ixiangpf.traffic_control(
        action='run',
        traffic_generator='ixnetwork_540',
        type='l23'
)

if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

print ('Let the traffic run for 20 seconds ...')
time.sleep(20)

############################################################################
#  Start L4-L7 traffic configured earlier                                  #
############################################################################
print ('Running Traffic...')
_result_ = ixiangpf.traffic_control(
        action='run',
        traffic_generator='ixnetwork_540',
        type='l47'
)

if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

print ('Let the traffic run for 20 seconds ...')
time.sleep(20)

############################################################################
# Retrieve L2-L3, L4-L7 traffic stats                                      #
############################################################################
print ('Retrieving L2-L3 and L4-L7 traffic stats')
trafficStats = ixiangpf.traffic_stats(
    	mode 				    = 'all',
        traffic_generator 		= 'ixnetwork_540',
        measure_mode 			= 'mixed'
)
if trafficStats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_stats', trafficStats)

pprint(trafficStats)

############################################################################
# Stop L2-L3 traffic started earlier                                       #
############################################################################
print ('Stopping Traffic...')
_result_ = ixiangpf.traffic_control(
        action             ='stop',
        traffic_generator  ='ixnetwork_540',
        type               ='l23',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

time.sleep(2)
    
############################################################################
# Stop L4-L7 traffic started earlier                                       #
############################################################################
print ('Stopping Traffic...')
_result_ = ixiangpf.traffic_control(
        action='stop',
        traffic_generator='ixnetwork_540',
        type='l47',
)

if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

time.sleep(2)
############################################################################
# Stop all protocols                                                       #
############################################################################
print ('Stopping all protocol(s) ...')
stop = ixiangpf.test_control(action='stop_all_protocols')
                  
if stop['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', stop)

print ('!!! Test Script Ends !!!')

