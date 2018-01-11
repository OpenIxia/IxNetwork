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
#    This sample creates an IPv4 stream with increasing frame length.          #
#    It configures buffer triggers and filters to capture only frames within a #
#    a small length range.                                                     #
#    Starts the capture, then starts the streams, collects statistics and      #  
#    returns the capture buffer in a csv file.                                 #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LSM XMVDC16NG module.                          #
#                                                                              #
################################################################################


from pprint import pprint
import os, sys
import time
import pdb

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

try:
	ErrorHandler('', {})
except (NameError,):
	def ErrorHandler(cmd, retval):
		global ixiatcl
		err = ixiatcl.tcl_error_info()
		log = retval['log']
		additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
		raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)


dirname, filename = os.path.split(os.path.abspath(__file__))
chassis_ip = "ixro-hlt-xm2-09"
tcl_server = "ixro-hlt-xm2-09"
ixnetwork_tcl_server = 'localhost'
port_list = ['2/1','2/2']
cfgErrors = 0

print "Printing connection variables ... "
print "test_name = %s" % filename
print 'chassis_ip =  %s' % chassis_ip
print "tcl_server = %s " % tcl_server
print "ixnetwork_tcl_server = %s" % ixnetwork_tcl_server
print "port_list = %s " % port_list
print "dirname = %s " % dirname


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
 
ports = connect_result['vport_list'].split()
rx_port = ports[0]
tx_port = ports[1]

ipV4_ixia_list    =['1.1.1.2', '1.1.1.1']
ipV4_gateway_list =['1.1.1.1', '1.1.1.2']
ipV4_netmask_list =['255.255.255.0', '255.255.255.0']
ipV4_mac_list     =['0000.debb.0001', '0000.debb.0002']
ipV4_version_list =[4, 4]
ipV4_autoneg_list =[1, 1]
ipV4_duplex_list  =['full', 'full']
ipV4_speed_list   =['ether100', 'ether100']
ipV4_port_rx_mode =['capture', 'capture']


########################################
# Configure the IPv4 interfaces        #
########################################

interface_status = ixiangpf.interface_config(
        port_handle     = ports,
        intf_ip_addr    = ipV4_ixia_list,
        gateway         = ipV4_gateway_list,
        netmask         = ipV4_netmask_list,
        autonegotiation = ipV4_autoneg_list,
        duplex          = ipV4_duplex_list,
        src_mac_addr    = ipV4_mac_list,
        speed           = ipV4_speed_list,
        port_rx_mode    = ipV4_port_rx_mode,
    )
    
if interface_status['status'] != '1':
    ErrorHandler('interface_config', interface_status)
    
 
##################################
#  Configure streams on TX port  #
##################################

pkts_per_burst_1=1000
ipv4_handles = interface_status['ipv4_handle'].split()
ti_src = ipv4_handles[0]
ti_dst = ipv4_handles[1]
   
traffic_status = ixiangpf.traffic_config(
    mode                                       = 'create',
    traffic_generator                          = 'ixnetwork_540',
    endpointset_count                          = 1,
    emulation_src_handle                       = ti_src,
    emulation_dst_handle                       = ti_dst,
    global_dest_mac_retry_count                = 1,
    global_dest_mac_retry_delay                = 5,
    enable_data_integrity                      = 1               ,
    global_enable_dest_mac_retry               = 1               ,
    global_enable_min_frame_size               = 0               ,
    global_enable_staggered_transmit           = 0               ,
    global_enable_stream_ordering              = 0               ,
    global_stream_control                      = 'continuous'      ,
    global_stream_control_iterations           = 1               ,
    global_large_error_threshhold              = 2               ,
    global_enable_mac_change_on_fly            = 0               ,
    global_max_traffic_generation_queries      = 500             ,
    global_mpls_label_learning_timeout         = 30              ,
    global_refresh_learned_info_before_apply   = 0               ,
    global_use_tx_rx_sync                      = 1               ,
    global_wait_time                           = 1               ,
    global_display_mpls_current_label_value    = 0               ,
    frame_sequencing                           = 'disable'         ,
    frame_sequencing_mode                      = 'rx_threshold'    ,
    src_dest_mesh                              = 'one_to_one'      ,
    route_mesh                                 = 'one_to_one'      ,
    bidirectional                              = 0               ,
    allow_self_destined                        = 0               ,
    enable_dynamic_mpls_labels                 = 0               ,
    hosts_per_net                              = 1               ,
    name                                       = 'Traffic_Item_1'  ,
    source_filter                              = 'all'             ,
    destination_filter                         = 'all'             ,
    merge_destinations                         = 1               ,
    circuit_endpoint_type                      = 'ipv4'            ,
    egress_tracking                            = 'none'            ,
    )
if traffic_status['status'] != '1':
    ErrorHandler('traffic_config', traffic_status) 
    
traffic_item = traffic_status['traffic_item']

interface_status = ixiangpf.interface_config(
        port_handle     = tx_port,
        arp_send_req    = 1,
    )

if interface_status['status'] != '1':
    ErrorHandler('interface_config', interface_status) 
    

time.sleep(10)

interface_status = ixiangpf.interface_config(
        port_handle     = rx_port,
        arp_send_req    = 1,
    )

if interface_status['status'] != '1':
    ErrorHandler('interface_config', interface_status) 
    
# Clear stats before sending traffic
clear_stats_status = ixiangpf.traffic_control(
        port_handle    = ports,
        action         = 'clear_stats',
    )

if clear_stats_status['status'] != '1':
    ErrorHandler('traffic_control', clear_stats_status)

time.sleep(5)

####################################
#  Configure triggers and filters  #
####################################

config_status = ixiangpf.packet_config_buffers(
    port_handle   = tx_port,
    capture_mode = 'trigger',
    )

if config_status['status'] != '1':
    ErrorHandler('packet_config_buffers', config_status) 

config_status = ixiangpf.packet_config_filter(
        port_handle = tx_port,
    )
if config_status['status'] != '1':
    ErrorHandler('packet_config_filter', config_status) 


uds1_size_from = 62
uds1_size_to = 67

uds2_size_from = 68
uds2_size_to = 1020

config_status = ixiangpf.packet_config_triggers(
    port_handle                    = tx_port,
    capture_trigger                = 1,
    capture_trigger_framesize      = 1 ,
    capture_trigger_framesize_from = uds1_size_from,
    capture_trigger_framesize_to   = uds1_size_to,
    capture_filter                 = 1,
    capture_filter_framesize       = 1,
    capture_filter_framesize_from  = uds1_size_from,
    capture_filter_framesize_to    = uds1_size_to,
    uds1                           = 1,
    uds1_framesize                 = 1,
    uds1_framesize_from            = uds1_size_from,
    uds1_framesize_to              = uds1_size_to,
    uds2                           = 1,
    uds2_framesize                 = 1,
    uds2_framesize_from            = uds2_size_from,
    uds2_framesize_to              = uds2_size_to,
    )

if config_status['status'] != '1':
    ErrorHandler('packet_config_triggers', config_status) 

time.sleep(5)

#########################
# Start capture on port #
#########################

print "Starting capture ..."

start_status = ixiangpf.packet_control(
        port_handle = tx_port,
        action      = 'start',
        packet_type = 'data',
    )
if start_status['status'] != '1':
    ErrorHandler('packet_control', start_status) 

time.sleep(10)

print "Capturing ..."

#########################
# Start traffic on port #
#########################

traffic_control_status = ixiangpf.traffic_control(
        handle      = traffic_item,
        action      = 'run',
    )
if traffic_control_status['status'] != '1':
    ErrorHandler('traffic_control', traffic_control_status) 

time.sleep(10)

#########################
# Stop traffic on port  #
#########################

print "Stopping traffic ..."
traffic_control_status = ixiangpf.traffic_control(
        handle      = traffic_item,
        action      = 'stop',
    )
if traffic_control_status['status'] != '1':
    ErrorHandler('traffic_control', traffic_control_status) 
    

print "Traffic stopped"

time.sleep(20)

#########################
# Stop capture on port  #
#########################

print "Stopping capture..."

stop_status = ixiangpf.packet_control(
        port_handle = tx_port,
        action      = 'stop',
    )

if stop_status['status'] != '1':
    ErrorHandler('packet_control', stop_status) 

time.sleep(15)

#############################################
# Get capture and statistics to csv         #
#############################################

stats_status = ixiangpf.packet_stats(
        port_handle = tx_port,
        format      = 'csv',
        stop        = 1,
        dirname     = dirname,
    )
if stats_status['status'] != '1':
    ErrorHandler('packet_stats', stats_status) 

print "SUCCESS!"