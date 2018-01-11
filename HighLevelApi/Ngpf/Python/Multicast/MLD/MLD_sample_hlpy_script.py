################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    01/19/2015 - Sumeer Kumar - created sample                                #
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
#    This script intends to demonstrate how to use NGPF MLD HLPy API.          #
#                                                                              #
#    1. It will create two topologies, one having two MLD Hosts and other      #
#       having one MLD Querier.                                                #
#    2. Start MLD protocol.                                                    #
#    3. Retreive protocol statistics.                                          #
#    4. Retrieve learned info.                                                 #
#    5. Configure L2-L3 traffic.                                               #
#    6. Start L2/L3 protocol.                                                  #
#    7. Retreive  L2/L3 protocol statistics.                                   #
#    8. Make Making on the fly changes for MLD Group and Source Ranges         #
#    9. Make Making on the fly changes for MLD Querier                         #
#   10. Retreive protocol statistics.                                          #
#   11. Stop protocol and L2/L3 traffic.                                       #
#   12. Stop all protocols.                                                    #
#                                                                              #
#Ixia Software:                                                                #
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
port_list               = [['1/5', '1/6']]
ixnetwork_tcl_server    = '10.205.28.41:8982';
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
    topology_name      = """MLD Host Topology""",
    port_handle        = ports[0],
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
topology_1_handle = _result_['topology_handle']

# Creating a device group in topology 
print "Creating device group 1 in topology 1" 
_result_ = ixiangpf.topology_config(
    topology_handle              = topology_1_handle,
    device_group_name            = """MLD Host Device Group""",
    device_group_multiplier      = "2",
    device_group_enabled         = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
deviceGroup_1_handle = _result_['device_group_handle']

# Creating a topology on second port
print "Adding topology 2 on port 2"
_result_ = ixiangpf.topology_config(
    topology_name      = """MLD Querier Topology""",
    port_handle        = ports[1],
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)

topology_2_handle = _result_['topology_handle']

# Creating a device group in topology
print "Creating device group 2 in topology 2"
_result_ = ixiangpf.topology_config(
    topology_handle              = topology_2_handle,
    device_group_name            = """MLD Querier Device Group""",
    device_group_multiplier      = "1",
    device_group_enabled         = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)

deviceGroup_2_handle = _result_['device_group_handle']

################################################################################
#  Configure protocol interfaces                                               #
################################################################################

# Creating multivalue for ethernet
print "Creating multivalue pattern for ethernet"
_result_ = ixiangpf.multivalue_config(
    pattern                = "counter",
    counter_start          = "18.03.73.c7.6c.b1",
    counter_step           = "00.00.00.00.00.01",
    counter_direction      = "increment",
    nest_step              = "00.00.01.00.00.00",
    nest_owner             = topology_1_handle,
    nest_enabled           = "1",
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

# Creating multivalue for IPv6                                 
print "Creating multivalue pattern for IPv6"
_result_ = ixiangpf.multivalue_config(
    pattern                = "counter",
    counter_start          = "2001:0:0:1:0:0:0:2",
    counter_step           = "0:0:0:0:0:0:0:1",
    counter_direction      = "increment",
    nest_step              = "0:0:0:1:0:0:0:0",
    nest_owner             = topology_1_handle,
    nest_enabled           = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', _result_)
    
multivalue_2_handle = _result_['multivalue_handle']
    
# Creating IPv6 Stack on top of Ethernet Stack for the first Device Group                                 
print "Creating IPv6 Stack on top of Ethernet Stack for the first Device Group"
_result_ = ixiangpf.interface_config(
    protocol_name                     = """IPv6 1""",
    protocol_handle                   = ethernet_1_handle,
    ipv6_multiplier                   = "1",
    ipv6_resolve_gateway              = "1",
    ipv6_manual_gateway_mac           = "00.00.00.00.00.01",
    ipv6_manual_gateway_mac_step      = "00.00.00.00.00.00",
    ipv6_gateway                      = "2001:0:0:1:0:0:0:1",
    ipv6_gateway_step                 = "::0",
    ipv6_intf_addr                    = multivalue_2_handle,
    ipv6_prefix_length                = "64",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)
    
ipv6_1_handle = _result_['ipv6_handle']

# Creating IPv6 Stack on top of Ethernet Stack for the second Device Group 
print "Creating IPv6 2 stack on ethernet 2 stack for the second Device Group"
_result_ = ixiangpf.interface_config(
    protocol_name                     = """IPv6 2""",
    protocol_handle                   = ethernet_2_handle,
    ipv6_multiplier                   = "1",
    ipv6_resolve_gateway              = "1",
    ipv6_manual_gateway_mac           = "00.00.00.00.00.01",
    ipv6_manual_gateway_mac_step      = "00.00.00.00.00.00",
    ipv6_gateway                      = "2001:0:0:1:0:0:0:2",
    ipv6_gateway_step                 = "::0",
    ipv6_intf_addr                    = "2001:0:0:1:0:0:0:1",
    ipv6_intf_addr_step               = "::0",
    ipv6_prefix_length                = "64",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)

ipv6_2_handle = _result_['ipv6_handle']

################################################################################
# Other protocol configurations                                                # 
################################################################################

# This will create MLD v2 Host Stack with IPTV disabled on top of IPv6 stack

# Creating MLD Host Stack on top of IPv6 stack
print "Creating MLD Host Stack on top of IPv6 stack in first topology"     
_result_ = ixiangpf.emulation_mld_config(
    mode                                 = "create",
    handle                               = ipv6_1_handle,
    mld_version                          = "v2",
    name                                 = """MLD Host 1""",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_config', _result_)
    
mldHost_1_handle = _result_['mld_host_handle']

# Creating multivalue for group address
print "Creating multivalue pattern for MLD Host group address"
_result_ = ixiangpf.multivalue_config(
    pattern                = "counter",
    counter_start          = "ff0a:0:0:0:0:0:0:1",
    counter_step           = "1:0:0:0:0:0:0:0",
    counter_direction      = "increment",
    nest_step              = "0:0:0:1:0:0:0:0",
    nest_owner             = topology_1_handle,
    nest_enabled           = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', _result_)

multivalue_3_handle = _result_['multivalue_handle']

# Creating MLD Group Ranges 
print "Creating MLD Group Ranges" 
_result_ = ixiangpf.emulation_multicast_group_config(
    mode               = "create",
    ip_addr_start      = multivalue_3_handle,
    ip_addr_step       = "0:0:0:0:0:0:0:1",
    num_groups         = "1",
    active             = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_group_config', _result_)
    
mldMcastIPv6GroupList_1_handle = _result_['multicast_group_handle']

# Creating MLD Source Ranges
print "Creating MLD Source Ranges"    
_result_ = ixiangpf.emulation_multicast_source_config(
    mode               = "create",
    ip_addr_start      = "2001:0:0:1:0:0:0:1",
    ip_addr_step       = "0:0:0:0:0:0:0:1",
    num_sources        = "1",
    active             = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_source_config', _result_)
    
mldUcastIPv6SourceList_1_handle = _result_['multicast_source_handle']

# This will create MLD v2 Querier Stack on top of IPv6 stack
    
# Creating MLD Group and Source Ranges in MLD Host stack
print "Creating MLD Group and Source Ranges in MLD Host stack"
_result_ = ixiangpf.emulation_mld_group_config(
    mode                    = "create",
    g_filter_mode           = "include",
    group_pool_handle       = mldMcastIPv6GroupList_1_handle,
    no_of_grp_ranges        = "1",
    no_of_src_ranges        = "1",
    session_handle          = mldHost_1_handle,
    source_pool_handle      = mldUcastIPv6SourceList_1_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_group_config', _result_)

mldGroup_1_handle = _result_['mld_group_handle']

# This will create MLD v2 Querier Stack on top of IPv6 stack

# Creating MLD Querier Stack on top of IPv6 stack
print "Creating MLD Querier Stack on top of IPv6 stack in second topology"
_result_ = ixiangpf.emulation_mld_querier_config(
    mode                                   = "create",
    discard_learnt_info                    = "0",
    active                                 = "1",
    general_query_response_interval        = 11000,
    handle                                 = ipv6_2_handle,
    version                                = "version2",
    general_query_interval                 = 140,
    name                                   = """MLD Querier""",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_querier_config', _result_)
    
mldQuerier_1_handle = _result_['mld_querier_handle']
    
print "Waiting 05 seconds before starting protocol(s) ..."
time.sleep(5)

############################################################################
# Start MLD protocol                                                       #
############################################################################    
print "Starting MLD Host on topology1"
_result_ = ixiangpf.emulation_mld_control(
    handle = mldHost_1_handle,
    mode   = 'start',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_control', _result_)

print "Starting MLD Querier on topology2"
_result_ = ixiangpf.emulation_mld_control(
        handle = mldQuerier_1_handle,
        mode   = 'start',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_control', _result_)

print "Waiting for 30 seconds"
time.sleep(30)

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
print "Fetching MLD Host aggregated statistics"         
protostats = ixiangpf.emulation_mld_info(\
    handle = deviceGroup_1_handle,
    type   = 'host',
    mode   = 'aggregate',
)
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_info', protostats)

pprint(protostats)

print "Fetching MLD Querier aggregated statistics"
protostats = ixiangpf.emulation_mld_info(\
    handle = deviceGroup_2_handle,
    type   = 'querier',
    mode   = 'aggregate',
)
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_info', protostats)

pprint(protostats)

############################################################################
# Retrieve Learned Info                                                    #
############################################################################
print "Fetching MLD Querier LearnedInfo"
mldLearnedInfo = ixiangpf.emulation_mld_info(\
    handle = mldQuerier_1_handle,
    type   = 'querier',
    mode   = 'learned_info',
)
if mldLearnedInfo['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_info', mldLearnedInfo)

pprint(mldLearnedInfo)

############################################################################ 
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv6, Destination->Multicast group                #
# 2. Type      : Multicast IPv6 traffic                                    #
# 3. Flow Group: Source Destination Endpoint Pair                          #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : Source Destination Endpoint Pair                          #	
############################################################################
print "Configuring L2-L3 traffic"
_result_ = ixiangpf.traffic_config(
    mode                                        = 'create',
    traffic_generator                           = 'ixnetwork_540',
    endpointset_count                           = 1,
    emulation_src_handle                        = topology_2_handle,
    emulation_dst_handle                        = '',
    emulation_multicast_dst_handle              = ['ff0a:0:0:0:0:0:0:1/0:0:0:0:0:0:0:0/1', 'ff0b:0:0:0:0:0:0:1/0:0:0:0:0:0:0:0/1'],
    emulation_multicast_dst_handle_type         = ['none', 'none'],
    emulation_multicast_rcvr_handle             = [mldMcastIPv6GroupList_1_handle, mldMcastIPv6GroupList_1_handle],
    emulation_multicast_rcvr_port_index         = [0, 0],
    emulation_multicast_rcvr_host_index         = [0, 1],
    emulation_multicast_rcvr_mcast_index        = [0, 0],
    name                                        = 'TI0-Traffic_Item_1',
    circuit_endpoint_type                       = 'ipv6',
    transmit_distribution                       = 'srcDestEndpointPair0',                             
    rate_pps                                    = 1000,                                    
    frame_size                                  = 512,
    track_by                                    = 'trackingenabled0 sourceDestEndpointPair0'
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_config', _result_)

############################################################################
#  Start L2-L3 traffic configured earlier                                  #
############################################################################
print "Running Traffic..."
_result_ = ixiangpf.traffic_control(
    action='run',
    traffic_generator='ixnetwork_540',
    type='l23'
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
# Sending leave using MLD host group handle                                #
############################################################################
print "Sending leave using MLD host group handle"
sendLeaveGlobally = ixiangpf.emulation_mld_control(
    mode                = 'leave',
    group_member_handle = mldGroup_1_handle,
)
if sendLeaveGlobally['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_control', sendLeaveGlobally)

time.sleep(2)

############################################################################
# Sending join using MLD host group handle                                 #
############################################################################
print "Sending join using MLD host group handle"
sendJoinGlobally = ixiangpf.emulation_mld_control(
    mode                = 'join',
    group_member_handle = mldGroup_1_handle,
)
if sendJoinGlobally['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_control', sendJoinGlobally)

time.sleep(2)

############################################################################
# Making on the fly changes for MLD Group and Source Ranges                #
############################################################################
print "Making on the fly changes for MLD Group Ranges"
_result_ = ixiangpf.emulation_multicast_group_config (
    handle        = mldMcastIPv6GroupList_1_handle,
    mode          = 'modify',
    ip_addr_start = 'ffff:0:0:1:0:0:0:1',
    ip_addr_step  = '0:0:0:0:0:0:0:2',
    num_groups    = '2',
    active        = '1',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_group_config', _result_)

print "Making on the fly changes for MLD Source Ranges"
_result_ = ixiangpf.emulation_multicast_source_config (
    handle        = mldUcastIPv6SourceList_1_handle,
    mode          = 'modify',
    ip_addr_start = 'bbbb:0:0:1:0:0:0:1',
    ip_addr_step  = '0:0:0:0:0:0:0:1',
    num_sources   = '5',
    active        = '1',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_source_config', _result_)

print "Making on the fly chnages for MLD Group and Source Ranges in MLD Host stack"
_result_ = ixiangpf.emulation_mld_group_config (
    mode                    = 'modify',
    handle                  = mldHost_1_handle,
    g_filter_mode           = 'exclude',
    group_pool_handle       = mldMcastIPv6GroupList_1_handle,
    no_of_grp_ranges        = '1',
    no_of_src_ranges        = '1',
    session_handle          = mldHost_1_handle,
    source_pool_handle      = mldUcastIPv6SourceList_1_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_source_config', _result_)

time.sleep(5)
 
############################################################################
# Making on the fly changes for MLD Querier                                #
############################################################################
print "Making on the fly changes for MLD Querier"
_result_ = ixiangpf.emulation_mld_querier_config (
    mode                            = 'modify',
    handle                          = mldQuerier_1_handle,
    general_query_response_interval = '240',
    router_alert                    = '0',
    robustness_variable             = '5',
    startup_query_count             = '5',
    general_query_interval          = '180',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_source_config', _result_)

time.sleep(2)  

############################################################################
# Applying changes one the fly                                             #
############################################################################
print "Applying changes on the fly"
applyChanges = ixiangpf.test_control(
    handle = ipv6_1_handle,
    action = 'apply_on_the_fly_changes',
)
if applyChanges['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', applyChanges)

time.sleep(5)

############################################################################
# Retrieve protocol statistics  fter making on the fly changes             #
############################################################################
print "Fetching MLD Host aggregated statistics"
protostats = ixiangpf.emulation_mld_info(\
    handle = deviceGroup_1_handle,
    type   = 'host',
    mode   = 'aggregate',
)
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_info', protostats)

pprint(protostats)

print "Fetching MLD Querier aggregated statistics"
protostats = ixiangpf.emulation_mld_info(\
    handle = deviceGroup_2_handle,
    type   = 'querier',
    mode   = 'aggregate',
)
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_info', protostats)

pprint(protostats)

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

