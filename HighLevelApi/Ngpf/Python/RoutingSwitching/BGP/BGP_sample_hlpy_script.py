################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    06/01/2015 - Rudra Dutta  - created sample                                #
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
#    This script intends to demonstrate how to use NGPF BGP API.               #
#                                                                              #
#    1. It will create 2 BGP topologies, each having an ipv4 network           #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. A loopback device group(DG) behind network   # 
#       group is needed to support applib traffic.                             #
#    2. Start BGP protocol.                                                    #
#    3. Retrieve protocol statistics.                                          #
#    4. Enable IPv4 Learned Information on the fly                             #
#    5. Retrieve protocol learned information                                  #
#    6. Configure L2-L3 traffic.                                               #
#    7. Configure application traffic.                                         #
#    8. Start the L2-L3 traffic.                                               #
#   9. Start the application traffic.                                          #
#   10. Retrieve Appilcation traffic stats.                                    #
#   11. Retrieve L2-L3 traffic stats.                                          #
#   12. Stop L2-L3 traffic.                                                    #
#   13. Stop Application traffic.                                              #
#   14. Stop all protocols.                                                    #
#                                                                              #
# Ixia Software:                                                               #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
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
    topology_name      = """BGP_1 Topology""",
    port_handle        = ports[0],
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
topology_1_handle = _result_['topology_handle']

# Creating a device group in topology 
print "Creating device group 1 in topology 1" 
_result_ = ixiangpf.topology_config(
    topology_handle              = topology_1_handle,
    device_group_name            = """BGP_1 Device Group""",
    device_group_multiplier      = "1",
    device_group_enabled         = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
deviceGroup_1_handle = _result_['device_group_handle']

# Creating a topology on second port
print "Adding topology 2 on port 2"
_result_ = ixiangpf.topology_config(
    topology_name      = """BGP_2 Topology""",
    port_handle        = ports[1],
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)

topology_2_handle = _result_['topology_handle']

# Creating a device group in topology
print "Creating device group 2 in topology 2"
_result_ = ixiangpf.topology_config(
    topology_handle              = topology_2_handle,
    device_group_name            = """BGP_2 Device Group""",
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
    gateway_step                      = "0.0.0.0",
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
    gateway_step                      = "0.0.0.0",
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

# This will create BGP Stack on top of IPv4 stack

# Creating BGP Stack on top of IPv4 stack
print "Creating BGP Stack on top of IPv4 stack in first topology on port 1"     
_result_ = ixiangpf.emulation_bgp_config(
    mode                                    = "enable",
    active                                  = "1",
    handle                                  = ipv4_1_handle,
    remote_ip_addr                          = "20.20.20.1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_bgp_config', _result_)

bgpIpv4Peer_1_handle = _result_['bgp_handle']

print "Creating BGP Stack on top of IPv4 stack in first topology on port 2"
_result_ = ixiangpf.emulation_bgp_config(
    mode                                    = "enable",
    active                                  = "1",
    handle                                  = ipv4_2_handle,
    remote_ip_addr                          = "20.20.20.2",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_bgp_config', _result_)

bgpIpv4Peer_2_handle = _result_['bgp_handle']

# Creating multivalue for network group
print "Creating multivalue pattern for BGP network group on Port 1"
_result_ = ixiangpf.multivalue_config(
    pattern                = "counter",
    counter_start          = "200.1.0.0",
    counter_step           = "0.1.0.0",
    counter_direction      = "increment",
    nest_step              = "0.0.0.1,0.1.0.0",
    nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
    nest_enabled           = "0,1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', _result_)

multivalue_4_handle = _result_['multivalue_handle']

# Creating BGP Network Group 
print "Creating BGP Network Group on Port 1"
_result_ = ixiangpf.network_group_config(
    protocol_handle                      = deviceGroup_1_handle,
    protocol_name                        = "BGP_1_Network_Group1",
    multiplier                           = "1",
    enable_device                        = "1",
    connected_to_handle                  = ethernet_1_handle,
    type                                 = "ipv4-prefix",
    ipv4_prefix_network_address          = multivalue_4_handle,
    ipv4_prefix_length                   = "24",
    ipv4_prefix_number_of_addresses      = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('network_group_config', _result_)

networkGroup_1_handle = _result_['network_group_handle']
ipv4PrefixPools_1_handle = _result_['ipv4_prefix_pools_handle']

# Creating multivalue for network group
print "Creating multivalue pattern for BGP network group on Port 2"
_result_ = ixiangpf.multivalue_config(
    pattern                = "counter",
    counter_start          = "201.1.0.0",
    counter_step           = "0.1.0.0",
    counter_direction      = "increment",
    nest_step              = "0.0.0.1,0.1.0.0",
    nest_owner             = '%s,%s' % (deviceGroup_2_handle, topology_2_handle),
    nest_enabled           = "0,1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', _result_)

multivalue_10_handle = _result_['multivalue_handle']

# Creating BGP Network Group
print "Creating BGP Network Group on Port 2"
_result_ = ixiangpf.network_group_config(
    protocol_handle                      = deviceGroup_2_handle,
    protocol_name                        = "BGP_2_Network_Group1",
    multiplier                           = "1",
    enable_device                        = "1",
    connected_to_handle                  = ethernet_2_handle,
    type                                 = "ipv4-prefix",
    ipv4_prefix_network_address          = multivalue_10_handle,
    ipv4_prefix_length                   = "24",
    ipv4_prefix_number_of_addresses      = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('network_group_config', _result_)

networkGroup_3_handle = _result_['network_group_handle']
ipv4PrefixPools_3_handle = _result_['ipv4_prefix_pools_handle']

# Creating multivalue for IPv4 Loopback
print "Creating multivalue for IPv4 Loopback"
_result_ = ixiangpf.topology_config(
    device_group_name            = """Device Group 3""",
    device_group_multiplier      = "1",
    device_group_enabled         = "1",
    device_group_handle          = networkGroup_1_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('topology_config', _result_)
	
deviceGroup_3_handle = _result_['device_group_handle']

# Creating multivalue pattern for IPv4 Loopback
print "Creating multivalue pattern for IPv4 Loopback on Port 1"
_result_ = ixiangpf.multivalue_config(
    pattern                = "counter",
    counter_start          = "200.1.0.0",
    counter_step           = "0.1.0.0",
    counter_direction      = "increment",
    nest_step              = "0.0.0.1,0.0.0.1,0.1.0.0",
    nest_owner             = '%s,%s,%s' % (networkGroup_1_handle, deviceGroup_1_handle, topology_1_handle),
    nest_enabled           = "0,0,1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', _result_)

multivalue_7_handle = _result_['multivalue_handle']

# Creating IPv4 Loopback
print "Creating IPv4 Loopback on Port 1"
_result_ = ixiangpf.interface_config(
    protocol_name            = """IPv4 Loopback 1""",
    protocol_handle          = deviceGroup_3_handle,
    enable_loopback          = "1",
    connected_to_handle      = networkGroup_1_handle,
    intf_ip_addr             = multivalue_7_handle,
    netmask                  = "255.255.255.255",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)

ipv4Loopback_1_handle = _result_['ipv4_loopback_handle']


# Creating multivalue for IPv4 Loopback
print "Creating multivalue for IPv4 Loopback"
_result_ = ixiangpf.topology_config(
    device_group_name            = """Device Group 4""",
    device_group_multiplier      = "1",
    device_group_enabled         = "1",
    device_group_handle          = networkGroup_3_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('topology_config', _result_)

deviceGroup_4_handle = _result_['device_group_handle']

# Creating multivalue pattern for IPv4 Loopback
print "Creating multivalue pattern for IPv4 Loopback on Port 2"
_result_ = ixiangpf.multivalue_config(
    pattern                = "counter",
    counter_start          = "201.1.0.0",
    counter_step           = "0.1.0.0",
    counter_direction      = "increment",
    nest_step              = "0.0.0.1,0.0.0.1,0.1.0.0",
    nest_owner             = '%s,%s,%s' % (networkGroup_3_handle, deviceGroup_3_handle, topology_2_handle),
    nest_enabled           = "0,0,1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', _result_)

multivalue_13_handle = _result_['multivalue_handle']

# Creating IPv4 Loopback
print "Creating IPv4 Loopback on Port 2"
_result_ = ixiangpf.interface_config(
    protocol_name            = """IPv4 Loopback 2""",
    protocol_handle          = deviceGroup_4_handle,
    enable_loopback          = "1",
    connected_to_handle      = networkGroup_3_handle,
    intf_ip_addr             = multivalue_13_handle,
    netmask                  = "255.255.255.255",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)

ipv4Loopback_2_handle = _result_['ipv4_loopback_handle']

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
print "Fetching BGP LearnedInfo on Port1"
bgpLearnedInfo = ixiangpf.emulation_bgp_info(\
    handle = bgpIpv4Peer_1_handle,
    mode   = 'learned_info');
if bgpLearnedInfo['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_bgp_info', bgpLearnedInfo)

pprint(bgpLearnedInfo)

print "Fetching BGP LearnedInfo on Port2"
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
    emulation_src_handle=networkGroup_1_handle,
    emulation_dst_handle=networkGroup_3_handle,
    track_by='sourceDestEndpointPair0 trackingenabled0',
    rate_pps=1000,
    frame_size=512,
)	
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_config', _result_)

############################################################################ 
# Configure L4-L7 traffic                                                  #
############################################################################
print "Configure L4-L7 traffic"
_result_ = ixiangpf.traffic_l47_config(
    mode                        = "create",
    name                        = """Traffic Item 2""",
    circuit_endpoint_type       = "ipv4_application_traffic",
    emulation_src_handle        = ipv4Loopback_1_handle,
    emulation_dst_handle        = ipv4Loopback_2_handle,
    objective_type              = "users",
    objective_value             = "100",
    objective_distribution      = "apply_full_objective_to_each_port",
    enable_per_ip_stats         = "0",
    flows                       = """Bandwidth_BitTorrent_File_Download Bandwidth_eDonkey Bandwidth_HTTP Bandwidth_IMAPv4 Bandwidth_POP3 Bandwidth_Radius Bandwidth_Raw Bandwidth_Telnet Bandwidth_uTorrent_DHT_File_Download BBC_iPlayer BBC_iPlayer_Radio BGP_IGP_Open_Advertise_Routes BGP_IGP_Withdraw_Routes Bing_Search BitTorrent_Ares_v217_File_Download BitTorrent_BitComet_v126_File_Download BitTorrent_Blizzard_File_Download BitTorrent_Cisco_EMIX BitTorrent_Enterprise BitTorrent_File_Download BitTorrent_LimeWire_v5516_File_Download BitTorrent_RMIX_5M""",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_l47_config', _result_)

############################################################################
#  Start L2-L3 & L4-L7 traffic configured earlier                          #
############################################################################
print "Running Traffic"
_result_ = ixiangpf.traffic_control(
    action='run',
    traffic_generator='ixnetwork_540',
    type=['l23','l47']
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

print "Let the traffic run for 60 seconds"
time.sleep(60)

############################################################################
# Retrieve L2-L3 & L4-L7 traffic stats                                     #
############################################################################
print "Retrieving L2-L3 & L4-L7 traffic stats"
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
    type=['l23','l47']
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
