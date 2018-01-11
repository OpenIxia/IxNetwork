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
#    This script intends to demonstrate how to use NGPF IPTVv4 HLPy API.       #
#                                                                              #
#    1. It will create one IGMP Host topology and one IPv4 topology.           #
#    2. Configure IPTV on IGMP host.                                           #
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
    topology_name      = """IGMP Topology 1""",
    port_handle        = ports[0],
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
topology_1_handle = _result_['topology_handle']

# Creating a device group in topology 
print "Creating device group 1 in topology 1"    
_result_ = ixiangpf.topology_config(
    topology_handle              = topology_1_handle,
    device_group_name            = """IGMP HOST""",
    device_group_multiplier      = "1",
    device_group_enabled         = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
    
deviceGroup_1_handle = _result_['device_group_handle']

# Creating a topology on second port
print "Adding topology 2 on port 2"
_result_ = ixiangpf.topology_config(
    topology_name      = """IPv4 Topology 2""",
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

# This will create IGMP v3 Host Stack with IPTV enabled on top of IPv4 stack having zap behavior as zap and view, zapping type as multicast to leave and zap direction as down.

print "Creating IGMP Host Stack on top of IPv4 1 stack"
_result_ = ixiangpf.emulation_igmp_config(
    handle                               = ipv4_1_handle,
    protocol_name                        = """IGMP Host 1""",
    mode                                 = "create",
    filter_mode                          = "include",
    igmp_version                         = "v3",
    enable_iptv                          = "true",
    iptv_name                            = """IPTV 1""",
    stb_leave_join_delay                 = "3000",
    join_latency_threshold               = "10000",
    leave_latency_threshold              = "10000",
    zap_behavior                         = "zapandview",
    zap_direction                        = "down",
    zap_interval_type                    = "multicasttoleave",
    zap_interval                         = "10000",
    num_channel_changes_before_view      = "1",
    view_duration                        = "10000",
    log_failure_timestamps               = "0",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_config', _result_)
    
igmpHost_1_handle = _result_['igmp_host_handle']
igmp_host_iptv_handle = _result_['igmp_host_iptv_handle']
    
# Creating IGMP Group Ranges 
print "Creating IGMP Group Ranges"  
_result_ = ixiangpf.emulation_multicast_group_config(
    mode               = "create",
    ip_addr_start      = "226.0.0.1",
    ip_addr_step       = "0.0.0.1",
    num_groups         = "1",
    active             = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_group_config', _result_)
    
igmpMcastIPv4GroupList_1_handle = _result_['multicast_group_handle']

# Creating IGMP Source Ranges 
print "Creating IGMP Source Ranges"    
_result_ = ixiangpf.emulation_multicast_source_config(
    mode               = "create",
    ip_addr_start      = "10.10.10.1",
    ip_addr_step       = "0.0.0.0",
    num_sources        = "1",
    active             = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_multicast_source_config', _result_)
    
igmpUcastIPv4SourceList_1_handle = _result_['multicast_source_handle']
    
# Creating IGMP Group and Source Ranges in IGMP Host stack
print "Creating IGMP Group and Source Ranges in IGMP Host stack"
_result_ = ixiangpf.emulation_igmp_group_config(
    mode                    = "create",
    g_filter_mode           = "include",
    group_pool_handle       = igmpMcastIPv4GroupList_1_handle,
    no_of_grp_ranges        = "1",
    no_of_src_ranges        = "1",
    session_handle          = igmpHost_1_handle,
    source_pool_handle      = igmpUcastIPv4SourceList_1_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_group_config', _result_)

# Configuring inter stb delay and rate control for IGMP Host global settings
print "Configuring inter stb delay and rate control for IGMP host"    
_result_ = ixiangpf.emulation_igmp_config(
    handle                      = "/globals",
    mode                        = "create",
    global_settings_enable      = "1",
    inter_stb_start_delay       = "0",
    msg_count_per_interval      = "600",
    msg_interval                = "1000",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_config', _result_)
    
print "Waiting 5 seconds before starting protocol(s) ..."
time.sleep(5)

############################################################################
# Start IGMP protocol                                                      #
############################################################################    
print "Starting IGMP on topology1"
_result_ = ixiangpf.emulation_igmp_control(
    handle = igmpHost_1_handle,
    mode   = 'start',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_control', _result_)

print "Starting IPv4 on topology2"
_result_ = ixiangpf.test_control(
    handle = ipv4_2_handle,
    action = 'start_protocol',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', _result_)

print "Waiting for 30 seconds"
time.sleep(30)

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
print "Fetching IGMP aggregated statistics"
protostats = ixiangpf.emulation_igmp_info(\
    handle = deviceGroup_1_handle,
    type   = 'host',
    mode   = 'aggregate',
)
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_info', protostats)

pprint(protostats)

############################################################################ 
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv4, Destination->Multicast group                #
# 2. Type      : Multicast IPv4 traffic                                    #
# 3. Flow Group: On IPv4 Destination Address                               #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : IPv4 Destination Address                                  #	
############################################################################
print "Configuring L2-L3 traffic"
_result_ = ixiangpf.traffic_config(
    mode                                        = 'create',
    traffic_generator                           = 'ixnetwork_540',
    endpointset_count                           = 1,
    emulation_src_handle                        = ipv4_2_handle,
    emulation_dst_handle                        = igmpMcastIPv4GroupList_1_handle,
    emulation_multicast_dst_handle              = '226.0.0.1/0.0.0.0/1',
    emulation_multicast_dst_handle_type         = 'none',
    emulation_multicast_rcvr_handle             = igmpMcastIPv4GroupList_1_handle,
    emulation_multicast_rcvr_port_index         = 0,
    emulation_multicast_rcvr_host_index         = 0,
    emulation_multicast_rcvr_mcast_index        = 0,
    name                                        = 'TI0-Traffic_Item_1',
    circuit_endpoint_type                       = 'ipv4',
    transmit_distribution                       = 'ipv4DestIp0',                             
    rate_pps                                    = 1000,                                    
    frame_size                                  = 512,
    track_by                                    = 'trackingenabled0 ipv4DestIp0'
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
_result_ = ixiangpf.emulation_igmp_control(
    handle = igmp_host_iptv_handle,
    mode   = 'start',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_control', _result_)

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
# numChannelChangesBeforeView and viewDuration in IPTV tab of IGMP host    #
############################################################################
print "Making on the fly chnages for zapDirection, zapIntervalType, zapInterval,\
    numChannelChangesBeforeView and viewDuration"
igmp_host_1_status = ixiangpf.emulation_igmp_config (
    handle                               = igmpHost_1_handle,
    mode                                 = "modify",
    zap_direction                        = "up",
    zap_interval_type                    = "leavetoleave",
    zap_interval                         = "30000",
    num_channel_changes_before_view      = "4",
    view_duration                        = "40000",
)
if igmp_host_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_config', igmp_host_1_status)

################################################################################
# Applying changes one the fly
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
# Retrieve protocol statistics after doing on the fly changes              #
############################################################################
print "Fetching IGMP aggregated statistics"
protostats = ixiangpf.emulation_igmp_info(\
    handle = deviceGroup_1_handle,
    type   = 'host',
    mode   = 'aggregate',
)
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_info', protostats)

pprint(protostats)

############################################################################
# Stopping IPTV                                                            #
############################################################################
print "Stopping IPTV"
_result_ = ixiangpf.emulation_igmp_control(
    handle = igmp_host_iptv_handle,
    mode   = 'stop',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_control', _result_)

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
