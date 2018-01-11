################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    22/01/2015 - Subhradip Pramanik - created sample                          #
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
#    This script intends to demonstrate how to use NGPF OSPFv2 API.            #
#                                                                              #
#    1. It will create 2 OSPFv2 topologies, each having an ipv4 network        #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. A loopback device group(DG) behind network   # 
#       group is needed to support applib traffic.                             #
#    2. Start the ospfv2 protocol.                                             #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Enable the Ospfv2 simulated topologies External Route type1, which     #
#       was disabled by default and apply change on the fly.                   #
#    6. Retrieve protocol learned info again and notice the difference with    #
#       previously retrieved learned info.                                     #
#    7. Configure L2-L3 traffic.                                               #
#    8. Start the L2-L3 traffic.                                               #
#    9. Retrieve L2-L3 traffic stats.                                          #
#   10. Stop L2-L3 traffic.                                                    #
#   11. Stop all protocols.                                                    #
# Ixia Software:                                                               #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
#                                                                              #
################################################################################

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
chassis_ip              = ['10.216.108.82']
tcl_server              = '10.216.108.82'
port_list               = [['8/3', '8/4']]
ixnetwork_tcl_server    = '10.216.108.49:8999';
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
pprint(connect_result)

#Retrieving the port handles, in a list
ports = connect_result['vport_list'].split()

################################################################################
# Configure Topology, Device Group                                             # 
################################################################################

# Creating a topology on first port
print "Adding topology 1 on port 1" 
_result_ = ixiangpf.topology_config(
    topology_name      = """ldp Topology 1""",
    port_handle        = ports[0],
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
topology_1_handle = _result_['topology_handle']

# Creating a device group in topology 
print "Creating device group 1 in topology 1"    
_result_ = ixiangpf.topology_config(
    topology_handle              = topology_1_handle,
    device_group_name            = """ldp Topology 1 Router""",
    device_group_multiplier      = "1",
    device_group_enabled         = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
deviceGroup_1_handle = _result_['device_group_handle']

# Creating a topology on second port
print "Adding topology 2 on port 2"
_result_ = ixiangpf.topology_config(
    topology_name      = """ldp Topology 2""",
    port_handle        = ports[1],
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)

topology_2_handle = _result_['topology_handle']

# Creating a device group in topology
print "Creating device group 2 in topology 2"
_result_ = ixiangpf.topology_config(
    topology_handle              = topology_2_handle,
    device_group_name            = """ldp Topology 2 Router""",
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

# Creating IPv4 Stack on top of Ethernet Stack for the first Device Group                                 
print "Creating IPv4 Stack on top of Ethernet Stack for the first Device Group"
_result_ = ixiangpf.interface_config(
    protocol_name                     = """IPv4 1""",
    protocol_handle                   = ethernet_1_handle,
    ipv4_resolve_gateway              = "1",
    ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
    ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
    gateway                           = "20.20.20.1",
    intf_ip_addr                      = "20.20.20.2",
    intf_ip_addr_step                 = "0.0.0.0",
    netmask                           = "255.255.255.0",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)
    
ipv4_1_handle = _result_['ipv4_handle']

# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group 
print "Creating IPv4 2 stack on ethernet 2 stack for the second Device Group"
_result_ = ixiangpf.interface_config(
    protocol_name                     = """IPv4 2""",
    protocol_handle                   = ethernet_2_handle,
    ipv4_resolve_gateway              = "1",
    ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
    ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
    gateway                           = "20.20.20.2",
    intf_ip_addr                      = "20.20.20.1",
    intf_ip_addr_step                 = "0.0.0.0",
    netmask                           = "255.255.255.0",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)

ipv4_2_handle = _result_['ipv4_handle']
 
################################################################################
# Other protocol configurations                                                # 
################################################################################
# Configuration of LDP Router and LDP Interface for the first Device Group with label space = 30, hello interval= 10, hold time = 45, keepalive interval = 30, keepalive holdtime =30
print "Creating LDP Router for 1st Device Group"
_result_ = ixiangpf.emulation_ldp_config(
    handle                       = ipv4_1_handle,
    mode                         = "create",
    lsr_id                       = "193.0.0.1",
    label_space                  = "30",
    hello_interval               = "10",
    hello_hold_time              = "30",
    keepalive_interval           = "30",
    keepalive_holdtime           = "45",
    interface_name               = """LDP-IF 1""",
    router_name                  = """LDP 1""",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_ldp_config', _result_)
ldpBasicRouter_1_handle = _result_['ldp_basic_router_handle']
# # Creating LDP Interface for first Device Group with label space = 30, hello interval= 10, hold time = 30
# print "Creating LDP Interface for 1st Device Group\n";    
# _result_ = ixiangpf.emulation_ldp_config(
    # handle                    = ipv4_1_handle,
    # mode                      = "create",
    # label_space               = "30",
    # hello_interval            = "10",
    # hello_hold_time           = "30",
    # interface_name            = """LDP-IF 1""",
# )
# if _result_['status'] != IxiaHlt.SUCCESS:
    # ErrorHandler('emulation_ldp_config', _result_)
# ldpConnectedInterface_1_handle = _result_['ldp_connected_interface_handle']    

# Configuration of LDP Router and LDP Interface for the second Device Group with label space = 30, hello interval= 10, hold time = 45, keepalive interval = 30, keepalive holdtime =30
print "Creating LDP Router for 2nd Device Group"
_result_ = ixiangpf.emulation_ldp_config(
    handle                       = ipv4_2_handle,
    mode                         = "create",
    lsr_id                       = "194.0.0.1",
    label_space                  = "30",
    hello_interval               = "10",
    hello_hold_time              = "30",
    keepalive_interval           = "30",
    keepalive_holdtime           = "45",
    interface_name               = """LDP-IF 2""",
    router_name                  = """LDP 2""",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_ldp_config', _result_)
ldpBasicRouter_2_handle = _result_['ldp_basic_router_handle']
# Creating LDP Interface for second Device Group with label space = 30, hello interval= 10, hold time = 30
# print "Creating LDP Interface for 2nd Device Group\n";        
# _result_ = ixiangpf.emulation_ldp_config(
    # handle                    = ipv4_1_handle,
    # mode                      = "create",
    # label_adv                 = "unsolicited",
    # label_space               = "30",
    # hello_interval            = "10",
    # hello_hold_time           = "30",
    # interface_name            = """LDP-IF 2""",
# )
# if _result_['status'] != IxiaHlt.SUCCESS:
    # ErrorHandler('emulation_ldp_config', _result_)
# ldpConnectedInterface_1_handle = _result_['ldp_connected_interface_handle']    
# Configuration of IPv4 Prefix which will used as FEC Range for the first Device Group with ipv4_prefix_network_address = "201.1.0.1
print "Creating multivalue for IPv4 prefix LDP_1_Network_Group"
_result_ = ixiangpf.network_group_config(
    protocol_handle                      = deviceGroup_1_handle,
    protocol_name                        = """Network Cloud 1""",
    multiplier                           = "1",
    enable_device                        = "1",
    connected_to_handle                  = ethernet_1_handle,
    type                                 = "ipv4-prefix",
    ipv4_prefix_network_address          = "201.1.0.1",
    ipv4_prefix_length                   = "32",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('network_group_config', _result_)
networkGroup_1_handle = _result_['network_group_handle']
ipv4PrefixPools_1_handle = _result_['ipv4_prefix_pools_handle']
# Configuration of IPv4 Prefix which will used as FEC Range for the second Device Group with ipv4_prefix_network_address = "202.1.0.1
print "Creating multivalue for IPv4 prefix LDP_2_Network_Group"
_result_ = ixiangpf.network_group_config(
    protocol_handle                      = deviceGroup_2_handle,
    protocol_name                        = """Network Cloud 2""",
    multiplier                           = "1",
    enable_device                        = "1",
    connected_to_handle                  = ethernet_2_handle,
    type                                 = "ipv4-prefix",
    ipv4_prefix_network_address          = "202.1.0.1",
    ipv4_prefix_length                   = "32",
)
if _result_['status'] != IxiaHlt.SUCCESS:
     ErrorHandler('network_group_config', _result_)
networkGroup_2_handle = _result_['network_group_handle']
ipv4PrefixPools_2_handle = _result_['ipv4_prefix_pools_handle']
# Modifying FEC Range Parameters with label_value_start="516"
print "Modifying LDP FEC Ranges info for LDP_1_Network_Group";
_result_ = ixiangpf.emulation_ldp_route_config(
    mode                        = "modify",
    handle                      = networkGroup_1_handle,
    fec_type                    = """ipv4_prefix""",
    label_value_start           = "516",
    label_value_start_step      = "1",
    lsp_handle                  = networkGroup_1_handle,
    fec_name                    = "{LDP FEC Range 1}",    
)
if _result_['status'] != IxiaHlt.SUCCESS:
     ErrorHandler('emulation_ldp_route_config', _result_)
fec_handle_1 = _result_['fecproperty_handle']
# Modifying FEC Range Parameters with label_value_start="216"
print "Modifying LDP FEC Ranges info for LDP_2_Network_Group";
_result_ = ixiangpf.emulation_ldp_route_config(
    mode                        = "modify",
    handle                      = networkGroup_2_handle,
    fec_type                    = """ipv4_prefix""",
    label_value_start           = "216",
    label_value_start_step      = "1",
    lsp_handle                  = networkGroup_2_handle,
    fec_name                    = "{LDP FEC Range 2}",    
)
if _result_['status'] != IxiaHlt.SUCCESS:
     ErrorHandler('emulation_ldp_route_config', _result_)
fec_handle_2 = _result_['fecproperty_handle']
# Creating multivalue for Device Group 3 for multiplier 10 
print "Creating multivalue for Device Group 3"
_result_ = ixiangpf.topology_config (
        device_group_name            = """Device Group 3""",
        device_group_multiplier      = "10",
        device_group_enabled         = "1",
        device_group_handle          = networkGroup_1_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
     ErrorHandler('topology_config', _result_)
deviceGroup_2_handle = _result_['device_group_handle']

# Creating of Chained Device Group for configuration of loopback behind first Device Group
print "Creating IPv4 loopback for configuring L4-L7 App Traffic for Topology 1"
_result_ = ixiangpf.interface_config (
    protocol_name            = """IPv4 Loopback 1""",
    protocol_handle          = deviceGroup_2_handle,
    enable_loopback          = "1",
    connected_to_handle      = networkGroup_1_handle,
    intf_ip_addr             = "201.1.0.0",
    netmask                  = "255.255.255.255",
)
if _result_['status'] != IxiaHlt.SUCCESS:
     ErrorHandler('interface_config', _result_)
ipv4Loopback_1_handle = _result_['ipv4_loopback_handle']

# Creating multivalue for Device Group 4 for multiplier 10 
print "Creating multivalue for Device Group 4"
_result_ = ixiangpf.topology_config (
        device_group_name            = """Device Group 4""",
        device_group_multiplier      = "10",
        device_group_enabled         = "1",
        device_group_handle          = networkGroup_2_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
     ErrorHandler('topology_config', _result_)
deviceGroup_3_handle = _result_['device_group_handle']

# Creating of Chained Device Group for configuration of loopback behind first Device Group
print "Creating IPv4 loopback for configuring L4-L7 App Traffic for Topology 2"
_result_ = ixiangpf.interface_config (
    protocol_name            = """IPv4 Loopback 2""",
    protocol_handle          = deviceGroup_3_handle,
    enable_loopback          = "1",
    connected_to_handle      = networkGroup_2_handle,
    intf_ip_addr             = "202.1.0.0",
    netmask                  = "255.255.255.255",
)
if _result_['status'] != IxiaHlt.SUCCESS:
     ErrorHandler('interface_config', _result_)
ipv4Loopback_2_handle = _result_['ipv4_loopback_handle']
print "Waiting 5 seconds before starting protocol(s) ..."
time.sleep(5)
############################################################################
# Start LDP protocol                                                       #
############################################################################    
print "Starting LDP on topology1"
ixiangpf.emulation_ldp_control(
    handle = topology_1_handle,
    mode   = 'start')
print "Starting LDP on topology2"
ixiangpf.test_control(
    handle = topology_2_handle,
    action = 'start_protocol',)
print "Waiting for 30 seconds"
time.sleep(60)
############################################################################
# Retrieve protocol statistics                                             #
############################################################################
print "Fetching LDP aggregated statistics"
protostats = ixiangpf.emulation_ldp_info(\
    handle = ldpBasicRouter_1_handle,
    mode   = 'stats',
)
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_ldp_info', protostats)

pprint(protostats)
############################################################################
# Retrieve protocol learned info                                           #
############################################################################
print "Fetching LDP  aggregated learned info for Topology 2"
learnedInfo = ixiangpf.emulation_ldp_info(\
    handle = ldpBasicRouter_2_handle,
    mode   = 'lsp_labels',
)
if learnedInfo['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_ldp_info', learnedInfo)

pprint(learnedInfo)

############################################################################
# Changing Label in both sides of FEC Ranges                               #
############################################################################
print "Changing Label value for Topology 2 LDP  FEC Ranges:";
network_group_4_status = ixiangpf.emulation_ldp_route_config (\
    mode                        = "modify",
    handle                      = fec_handle_2,
    label_value_start           = "5016",
    label_value_start_step      = "100",
    lsp_handle                  = fec_handle_2,
)
if network_group_4_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_ldp_config', network_group_4_status)
################################################################################
# Applying changes one the fly                                                 #
################################################################################
print "Applying changes on the fly"
applyChanges = ixiangpf.test_control(
   handle = ipv4_1_handle,
   action = 'apply_on_the_fly_changes',
)
time.sleep(5)
if applyChanges['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', applyChanges)
############################################################################
# Retrieve protocol learned info again and notice the difference with      #
# previously retrieved learned info.                                       #    
############################################################################
print "Fetching LDP  aggregated learned info for Topology 1"
learnedInfo = ixiangpf.emulation_ldp_info(\
    handle = ldpBasicRouter_1_handle,
    mode   = 'lsp_labels',
)
if learnedInfo['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_ldp_info', learnedInfo)

pprint(learnedInfo)
############################################################################
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv4 FEC Range, Destination->IPv4 FEC Range       #
# 2. Type      : Unicast IPv4 traffic                                      #
# 3. Flow Group: On IPv4 Destination Address                               #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : Source Destination EndPoint Set                           #
############################################################################
print "Configuring L2-L3 traffic"
_result_ = ixiangpf.traffic_config(
    mode                                    = 'create',
    traffic_generator                       = 'ixnetwork_540',
    endpointset_count                       = "1",
    emulation_src_handle                    = ipv4PrefixPools_1_handle,
    emulation_dst_handle                    = ipv4PrefixPools_2_handle,
    frame_sequencing                        = "disable",
    frame_sequencing_mode                   = "rx_threshold",
    name                                    = "Traffic_1_Item",
    circuit_endpoint_type                   = "ipv4",
    transmit_distribution                   = "ipv4DestIp0",                               
    rate_pps                                = "1000",                                      
    frame_size                              = "512",                                       
    track_by                                = "sourceDestEndpointPair0 trackingenabled0",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_config', _result_)

############################################################################
# Start L2-L3 traffic configured earlier                                   #
############################################################################
print "Running Traffic..."
_result_ = ixiangpf.traffic_control(
    action            = 'run',
    traffic_generator = 'ixnetwork_540',
    type              = 'l23'
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
