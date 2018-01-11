################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    15/01/2015 - Sumeer Kumar - created sample                                #
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
#    This script intends to demonstrate how to use NGPF IPTVv6 HLPy API.       #
#                                                                              #
#    1. It will create one MLD Host topology and one IPv6 topology.            #
#    2. Configure IPTV on MLD host.                                            #
#    3. Start all protocols.                                                   #
#    4. Retrieve protocol statistics.                                          #
#    5. Configure L2-L3 traffic.                                               #
#    6. Start the L2-L3 traffic.                                               #
#    7. Stat IPTV.                                                             #  
#    8. Retrieve L2-L3 traffic stats.                                          #
#    9. Make on the fly changes of IPTV attributes                             #	
#   10. Retrieve protocol statistics.                                          #
#   11. Stop IPTV.                                                             #
#   12. Stop L2-L3 traffic.                                                    #
#   13. Stop all protocols.                                                    #
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
port_list               = [['1/5', '1/6']]
ixnetwork_tcl_server    = '10.205.28.41:8982';
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
# Configure Topology, Device Group                                             # 
################################################################################

# Creating a topology on first port
print "Adding topology 1 on port 1" 
_result_ = ixiangpf.topology_config(
    topology_name      = """MLD Topology 1""",
    port_handle        = ports[0],
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
topology_1_handle = _result_['topology_handle']

# Creating a device group in topology 
print "Creating device group 1 in topology 1"    
_result_ = ixiangpf.topology_config(
    topology_handle              = topology_1_handle,
    device_group_name            = """MLD HOST""",
    device_group_multiplier      = "1",
    device_group_enabled         = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
deviceGroup_1_handle = _result_['device_group_handle']

# Creating a topology on second port
print "Adding topology 2 on port 2"
_result_ = ixiangpf.topology_config(
    topology_name      = """IPv6 Topology 2""",
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
    ipv6_gateway                 = "20:0:0:0:0:0:0:1",
    ipv6_gateway_step            = "::0",
    ipv6_intf_addr               = "20:0:0:0:0:0:0:2",
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
    ipv6_gateway                 = "20:0:0:0:0:0:0:2",
    ipv6_gateway_step            = "::0",
    ipv6_intf_addr               = "20:0:0:0:0:0:0:1",
    ipv6_intf_addr_step          = "::0",
    ipv6_prefix_length           = "64",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)

ipv6_2_handle = _result_['ipv6_handle']
 
################################################################################
# Other protocol configurations                                                # 
################################################################################

# This will create MLD v2 Host Stack with IPTV enabled on top of IPv6 stack having zap behavior as zap and view, zapping type as multicast to leave and zap direction as down.

print "Creating MLD Host Stack on top of IPv6 1 stack"
_result_ = ixiangpf.emulation_mld_config(
    mode                                = "create",
    handle                              = ipv6_1_handle,
    mld_version                         = "v2",
    name                                = """MLD Host 1""",
    enable_iptv                         = "1",
    iptv_name                           = """IPTV 1""",
    stb_leave_join_delay                = "3000",
    join_latency_threshold              = "10000",
    leave_latency_threshold             = "10000",
    zap_behavior                        = "zapandview",
    zap_direction                       = "down",
    zap_interval                        = "10000",
    num_channel_changes_before_view     = "1",
    view_duration                       = "10000",
    zap_interval_type                   = "multicasttoleave",
    log_failure_timestamps              = "0",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_config', _result_)
    
mldHost_1_handle = _result_['mld_host_handle']
mld_host_iptv_handle = _result_['mld_host_iptv_handle']
    
# Creating MLD Group Ranges 
print "Creating MLD Group Ranges"  
_result_ = ixiangpf.emulation_multicast_group_config(
    mode               = "create",
    ip_addr_start      = "ff0a:0:0:0:0:0:0:1",
    ip_addr_step       = "0:0:0:0:0:0:0:0",
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
    ip_addr_start      = "20:0:0:0:0:0:0:1",
    ip_addr_step       = "0:0:0:0:0:0:0:0",
    num_sources        = "1",
    active             = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_source_config', _result_)
    
mldUcastIPv6SourceList_1_handle = _result_['multicast_source_handle']
    
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

# Configuring inter stb delay and rate control for MLD Host global settings
print "Configuring inter stb delay and rate control for MLD host"
_result_ = ixiangpf.emulation_mld_config(
    mode                        = "create",
    handle                      = "/globals",
    global_settings_enable      = "1",
    no_of_reports_per_second    = "500",
    interval_in_ms              = "1000",
    inter_stb_start_delay       = "0",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_config', _result_)
    
print "Waiting 5 seconds before starting protocol(s) ..."
time.sleep(5)

############################################################################
# Start MLD protocol                                                       #
############################################################################    
print "Starting MLD on topology1"
_result_ = ixiangpf.emulation_mld_control(
    handle = mldHost_1_handle,
    mode   = 'start',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_control', _result_)

print "Starting IPv6 on topology2"
_result_ = ixiangpf.test_control(
    handle = ipv6_2_handle,
    action = 'start_protocol',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', _result_)

print "Waiting for 30 seconds"
time.sleep(30)

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
print "Fetching MLD aggregated statistics"
protostats = ixiangpf.emulation_mld_info(\
    handle = deviceGroup_1_handle,
    type   = 'host',
    mode   = 'aggregate',
)
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_info', protostats)

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
    emulation_src_handle                        = ipv6_2_handle,
    emulation_dst_handle                        = mldMcastIPv6GroupList_1_handle,
    emulation_multicast_dst_handle              = 'ff0a:0:0:0:0:0:0:1/0:0:0:0:0:0:0:0/1',
    emulation_multicast_dst_handle_type         = 'none',
    emulation_multicast_rcvr_handle             = mldMcastIPv6GroupList_1_handle,
    emulation_multicast_rcvr_port_index         = 0,
    emulation_multicast_rcvr_host_index         = 0,
    emulation_multicast_rcvr_mcast_index        = 0,
    name                                        = 'TI0-Traffic_Item_1',
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
    type              = 'l23'
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

print "Let the traffic run for 20 seconds ..."
time.sleep(20)

############################################################################
# Starting IPTV                                                            #
############################################################################
print "Starting IPTV..."
_result_ = ixiangpf.emulation_mld_control(
    handle = mld_host_iptv_handle,
    mode   = 'start',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_control', _result_)

time.sleep(10)

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
# Making on the fly changes for zapDirection, zapIntervalType, zapInterval,#    
# numChannelChangesBeforeView and viewDuration in IPTV tab of MLD host     #
############################################################################
print "Making on the fly chnages for zapDirection, zapIntervalType, zapInterval,\
    numChannelChangesBeforeView and viewDuration"
mld_host_1_status = ixiangpf.emulation_mld_config (
    handle                               = mldHost_1_handle,
    mode                                 = "modify",
    zap_direction                        = "up",
    zap_interval_type                    = "leavetoleave",
    zap_interval                         = "30000",
    num_channel_changes_before_view      = "4",
    view_duration                        = "40000",
)
if mld_host_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_config', mld_host_1_status)

################################################################################
# Applying changes one the fly
################################################################################
print "Applying changes on the fly"
applyChanges = ixiangpf.test_control(
   handle = ipv6_1_handle,
   action = 'apply_on_the_fly_changes',
)
time.sleep(5)
if applyChanges['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', applyChanges)

############################################################################
# Retrieve protocol statistics after doing on the fly changes              #
############################################################################
print "Fetching MLD aggregated statistics"
protostats = ixiangpf.emulation_mld_info(\
    handle = deviceGroup_1_handle,
    type   = 'host',
    mode   = 'aggregate',
)
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_info', protostats)

pprint(protostats)

############################################################################
# Stopping IPTV                                                            #
############################################################################
print "Stopping IPTV"
_result_ = ixiangpf.emulation_mld_control(
    handle = mld_host_iptv_handle,
    mode   = 'stop',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_mld_control', _result_)

time.sleep(2)

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
