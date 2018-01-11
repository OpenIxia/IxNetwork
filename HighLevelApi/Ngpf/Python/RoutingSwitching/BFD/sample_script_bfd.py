################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    11/05/2016 - Dhiraj Khandelwal  - created sample                                #
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
#    This script intends to demonstrate how to use NGPF BFD API.               #
#                                                                              #
#    1. It will create 2 BFD topologies, each having an ipv4 network           #
#       topology. A loopback device group(DG) behind network   				   # 
#       group is needed to support applib traffic.                             #
#    2. Start BFD protocol.                                                    #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve Learned info 					                               #
#    5. Perform Action Start/Stop interfaces 	                               #
#    6. Changes few attributes OTF                                             #
#    7. Stop all protocols.                                                    #
#                                                                              #
# Ixia Software:                                                               #
#    IxOS      8.01 EA                                                         #
#    IxNetwork 8.01 EA                                                         #
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
import IxNetwork

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
chassis_ip              = ['10.216.108.130']
tcl_server              = '10.216.108.130'
port_list               = [['12/3', '12/4']]
ixnetwork_tcl_server    = '10.216.108.86:8237';
ixnetwork_tcl_ip 		= '10.216.108.86'
cfgErrors               = 0
ixTclPort				= '8237'
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
ixNet = IxNetwork.IxNet()
ixNet.connect(ixnetwork_tcl_ip, '-port', ixTclPort, '-version', '8.01' )
################################################################################
# Configure Topology, Device Group                                             # 
################################################################################if 'py' not in dir():
	
status = ixiangpf.topology_config(
	topology_name      = """Topology 1""",
	port_handle        = ports[0],
)
if status['status'] != IxiaHlt.SUCCESS:
	ixerrorHandler('topology_config', status)

topology_1_handle = status['topology_handle']

status = ixiangpf.topology_config(
	topology_handle              = topology_1_handle,
	device_group_name            = """Device Group 1""",
	device_group_multiplier      = "3",
	device_group_enabled         = "1",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('topology_config', status)

deviceGroup_1_handle = status['device_group_handle']

status = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "00.11.01.00.00.01",
	counter_step           = "00.00.00.00.00.01",
	counter_direction      = "increment",
	nest_step              = '%s' % ("00.00.01.00.00.00"),
	nest_owner             = '%s' % (topology_1_handle),
	nest_enabled           = '%s' % ("1"),
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)

multivalue_1_handle = status['multivalue_handle']

###################################
##Configure Ethernet
###################################
status = ixiangpf.interface_config(
	protocol_name                = """Ethernet 1""",
	protocol_handle              = deviceGroup_1_handle,
	mtu                          = "1500",
	src_mac_addr                 = multivalue_1_handle,
	vlan                         = "1",
	vlan_id                      = '%s' % ("1"),
	vlan_id_step                 = '%s' % ("1"),
	vlan_id_count                = '%s' % ("1"),
	vlan_tpid                    = '%s' % ("0x8100"),
	vlan_user_priority           = '%s' % ("0"),
	vlan_user_priority_step      = '%s' % ("0"),
	use_vpn_parameters           = "0",
	site_id                      = "0",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', status)

ethernet_1_handle = status['ethernet_handle']

status = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "100.1.0.2",
	counter_step           = "0.0.1.0",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
	nest_owner             = '%s' % (topology_1_handle),
	nest_enabled           = '%s' % ("1"),
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)

multivalue_2_handle = status['multivalue_handle']

status = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "100.1.0.1",
	counter_step           = "0.0.1.0",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
	nest_owner             = '%s' % (topology_1_handle),
	nest_enabled           = '%s' % ("1"),
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)

multivalue_3_handle = status['multivalue_handle']

#####################################
#Configrue Ipv4
#####################################

status = ixiangpf.interface_config(
	protocol_name                     = """IPv4 1""",
	protocol_handle                   = ethernet_1_handle,
	ipv4_resolve_gateway              = "1",
	ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
	ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
	gateway                           = multivalue_3_handle,
	intf_ip_addr                      = multivalue_2_handle,
	netmask                           = "255.255.255.0",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', status)

ipv4_1_handle = status['ipv4_handle']

status = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "192.0.0.1",
	counter_step           = "0.0.0.1",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
	nest_owner             = '%s' % (topology_1_handle),
	nest_enabled           = '%s' % ("1"),
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)

multivalue_4_handle = status['multivalue_handle']

####################################################
##Configure BFD
####################################################

status = ixiangpf.emulation_bfd_config(
	count                           = "1",
	echo_rx_interval                = "0",
	echo_timeout                    = "1500",
	echo_tx_interval                = "0",
	control_plane_independent       = "0",
	enable_demand_mode              = "0",
	flap_tx_interval                = "0",
	handle                          = ipv4_1_handle,
	min_rx_interval                 = "1000",
	mode                            = "create",
	detect_multiplier               = "3",
	poll_interval                   = "0",
	router_id                       = multivalue_4_handle,
	tx_interval                     = "1000",
	configure_echo_source_ip        = "0",
	echo_source_ip4                 = "0.0.0.0",
	ip_diff_serv                    = "0",
	interface_active                = "1",
	interface_name                  = """BFDv4 IF 1""",
	router_active                   = "1",
	router_name                     = """BfdRouter 1""",
	session_count                   = "1",
	enable_auto_choose_source       = "1",
	enable_learned_remote_disc      = "1",
	ip_version                      = "4",
	session_discriminator           = "1",
	session_discriminator_step      = "0",
	remote_discriminator            = "1",
	remote_discriminator_step       = "0",
	source_ip_addr                  = "0.0.0.0",
	remote_ip_addr                  = "100.1.0.1",
	remote_ip_addr_step             = "0.0.1.0",
	hop_mode                        = "singlehop",
	session_active                  = "1",
	session_name                    = """BFDv4 Session 1""",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_bfd_config', status)

bfdv4Interface_1_handle = status['bfd_v4_interface_handle']

status = ixiangpf.topology_config(
	device_group_name            = """Device Group 3""",
	device_group_multiplier      = "1",
	device_group_enabled         = "1",
	device_group_handle          = deviceGroup_1_handle,
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('topology_config', status)

deviceGroup_2_handle = status['device_group_handle']

status = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "2.2.2.2",
	counter_step           = "0.0.0.1",
	counter_direction      = "increment",
	nest_step              = '%s,%s' % ("0.0.0.1", "0.1.0.0"),
	nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
	nest_enabled           = '%s,%s' % ("0", "1"),
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)

multivalue_5_handle = status['multivalue_handle']

#################################################
#Configuer IPv4 Loopback
#################################################

status = ixiangpf.interface_config(
	protocol_name            = """IPv4 Loopback 1""",
	protocol_handle          = deviceGroup_2_handle,
	enable_loopback          = "1",
	connected_to_handle      = ethernet_1_handle,
	intf_ip_addr             = multivalue_5_handle,
	netmask                  = "255.255.255.255",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', status)

# n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
# n The attribute: connectedVia with the value: {} is not supported by scriptgen.
ipv4Loopback_1_handle = status['ipv4_loopback_handle']

status = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "3.2.2.2",
	counter_step           = "0.0.0.1",
	counter_direction      = "increment",
	nest_step              = '%s,%s' % ("0.0.0.1", "0.0.0.1"),
	nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
	nest_enabled           = '%s,%s' % ("0", "0"),
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)

multivalue_6_handle = status['multivalue_handle']

status = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "194.0.0.1",
	counter_step           = "0.0.0.1",
	counter_direction      = "increment",
	nest_step              = '%s,%s' % ("0.0.0.1", "0.1.0.0"),
	nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
	nest_enabled           = '%s,%s' % ("0", "1"),
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)

multivalue_7_handle = status['multivalue_handle']

######################################
#Configure BFD
######################################

status = ixiangpf.emulation_bfd_config(
	count                           = "1",
	echo_rx_interval                = "0",
	echo_timeout                    = "1500",
	echo_tx_interval                = "0",
	control_plane_independent       = "0",
	enable_demand_mode              = "0",
	flap_tx_interval                = "0",
	handle                          = ipv4Loopback_1_handle,
	min_rx_interval                 = "1000",
	mode                            = "create",
	detect_multiplier               = "3",
	poll_interval                   = "0",
	router_id                       = multivalue_7_handle,
	tx_interval                     = "1000",
	configure_echo_source_ip        = "0",
	echo_source_ip4                 = "0.0.0.0",
	ip_diff_serv                    = "0",
	interface_active                = "1",
	interface_name                  = """BFDv4 IF 3""",
	router_active                   = "1",
	router_name                     = """BfdRouter 3""",
	session_count                   = "1",
	enable_auto_choose_source       = "1",
	enable_learned_remote_disc      = "1",
	ip_version                      = "4",
	session_discriminator           = "1",
	session_discriminator_step      = "0",
	remote_discriminator            = "1",
	remote_discriminator_step       = "0",
	source_ip_addr                  = multivalue_6_handle,
	remote_ip_addr                  = "3.2.2.2",
	remote_ip_addr_step             = "0.0.0.1",
	hop_mode                        = "multiplehop",
	session_active                  = "1",
	session_name                    = """BFDv4 Session 3""",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_bfd_config', status)

bfdv4Interface_2_handle = status['bfd_v4_interface_handle']

status = ixiangpf.topology_config(
	topology_name      = """Topology 2""",
	port_handle        = ports[1],
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('topology_config', status)

topology_2_handle = status['topology_handle']
#################################
#Configure Topology 2
#################################

status = ixiangpf.topology_config(
	topology_handle              = topology_2_handle,
	device_group_name            = """Device Group 2""",
	device_group_multiplier      = "3",
	device_group_enabled         = "1",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('topology_config', status)

deviceGroup_3_handle = status['device_group_handle']

status = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "00.12.01.00.00.01",
	counter_step           = "00.00.00.00.00.01",
	counter_direction      = "increment",
	nest_step              = '%s' % ("00.00.01.00.00.00"),
	nest_owner             = '%s' % (topology_2_handle),
	nest_enabled           = '%s' % ("1"),
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)

multivalue_8_handle = status['multivalue_handle']

status = ixiangpf.interface_config(
	protocol_name                = """Ethernet 2""",
	protocol_handle              = deviceGroup_3_handle,
	mtu                          = "1500",
	src_mac_addr                 = multivalue_8_handle,
	vlan                         = "1",
	vlan_id                      = '%s' % ("1"),
	vlan_id_step                 = '%s' % ("1"),
	vlan_id_count                = '%s' % ("1"),
	vlan_tpid                    = '%s' % ("0x8100"),
	vlan_user_priority           = '%s' % ("0"),
	vlan_user_priority_step      = '%s' % ("0"),
	use_vpn_parameters           = "0",
	site_id                      = "0",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', status)

ethernet_2_handle = status['ethernet_handle']

status = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "100.1.0.1",
	counter_step           = "0.0.1.0",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
	nest_owner             = '%s' % (topology_2_handle),
	nest_enabled           = '%s' % ("1"),
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)

multivalue_9_handle = status['multivalue_handle']

status = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "100.1.0.2",
	counter_step           = "0.0.1.0",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
	nest_owner             = '%s' % (topology_2_handle),
	nest_enabled           = '%s' % ("1"),
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)

multivalue_10_handle = status['multivalue_handle']

##########################################
#Configure IPv4
#########################################

status = ixiangpf.interface_config(
	protocol_name                     = """IPv4 2""",
	protocol_handle                   = ethernet_2_handle,
	ipv4_resolve_gateway              = "1",
	ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
	ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
	gateway                           = multivalue_10_handle,
	intf_ip_addr                      = multivalue_9_handle,
	netmask                           = "255.255.255.0",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', status)

ipv4_2_handle = status['ipv4_handle']

status = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "193.0.0.1",
	counter_step           = "0.0.0.1",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.1.0.0"),
	nest_owner             = '%s' % (topology_2_handle),
	nest_enabled           = '%s' % ("1"),
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)

multivalue_11_handle = status['multivalue_handle']

##############################################
#configure BFD
##############################################

status = ixiangpf.emulation_bfd_config(
	count                           = "1",
	echo_rx_interval                = "0",
	echo_timeout                    = "1500",
	echo_tx_interval                = "0",
	control_plane_independent       = "0",
	enable_demand_mode              = "0",
	flap_tx_interval                = "0",
	handle                          = ipv4_2_handle,
	min_rx_interval                 = "1000",
	mode                            = "create",
	detect_multiplier               = "3",
	poll_interval                   = "0",
	router_id                       = multivalue_11_handle,
	tx_interval                     = "1000",
	configure_echo_source_ip        = "0",
	echo_source_ip4                 = "0.0.0.0",
	ip_diff_serv                    = "0",
	interface_active                = "1",
	interface_name                  = """BFDv4 IF 2""",
	router_active                   = "1",
	router_name                     = """BfdRouter 2""",
	session_count                   = "1",
	enable_auto_choose_source       = "1",
	enable_learned_remote_disc      = "1",
	ip_version                      = "4",
	session_discriminator           = "1",
	session_discriminator_step      = "0",
	remote_discriminator            = "1",
	remote_discriminator_step       = "0",
	source_ip_addr                  = "0.0.0.0",
	remote_ip_addr                  = "100.1.0.2",
	remote_ip_addr_step             = "0.0.1.0",
	hop_mode                        = "singlehop",
	session_active                  = "1",
	session_name                    = """BFDv4 Session 2""",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_bfd_config', status)

bfdv4Interface_3_handle = status['bfd_v4_interface_handle']

status = ixiangpf.topology_config(
	device_group_name            = """Device Group 4""",
	device_group_multiplier      = "1",
	device_group_enabled         = "1",
	device_group_handle          = deviceGroup_3_handle,
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('topology_config', status)

deviceGroup_4_handle = status['device_group_handle']

status = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "3.2.2.2",
	counter_step           = "0.0.0.1",
	counter_direction      = "increment",
	nest_step              = '%s,%s' % ("0.0.0.1", "0.1.0.0"),
	nest_owner             = '%s,%s' % (deviceGroup_3_handle, topology_2_handle),
	nest_enabled           = '%s,%s' % ("0", "1"),
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)

multivalue_12_handle = status['multivalue_handle']

status = ixiangpf.interface_config(
	protocol_name            = """IPv4 Loopback 2""",
	protocol_handle          = deviceGroup_4_handle,
	enable_loopback          = "1",
	connected_to_handle      = ethernet_2_handle,
	intf_ip_addr             = multivalue_12_handle,
	netmask                  = "255.255.255.255",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', status)

ipv4Loopback_2_handle = status['ipv4_loopback_handle']

status = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "195.0.0.1",
	counter_step           = "0.0.0.1",
	counter_direction      = "increment",
	nest_step              = '%s,%s' % ("0.0.0.1", "0.1.0.0"),
	nest_owner             = '%s,%s' % (deviceGroup_3_handle, topology_2_handle),
	nest_enabled           = '%s,%s' % ("0", "1"),
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)

multivalue_13_handle = status['multivalue_handle']

################################################
##Configure BFD over loopback Interfaces
################################################

status = ixiangpf.emulation_bfd_config(
	count                           = "1",
	echo_rx_interval                = "0",
	echo_timeout                    = "1500",
	echo_tx_interval                = "0",
	control_plane_independent       = "0",
	enable_demand_mode              = "0",
	flap_tx_interval                = "0",
	handle                          = ipv4Loopback_2_handle,
	min_rx_interval                 = "1000",
	mode                            = "create",
	detect_multiplier               = "3",
	poll_interval                   = "0",
	router_id                       = multivalue_13_handle,
	tx_interval                     = "1000",
	configure_echo_source_ip        = "0",
	echo_source_ip4                 = "0.0.0.0",
	ip_diff_serv                    = "0",
	interface_active                = "1",
	interface_name                  = """BFDv4 IF 4""",
	router_active                   = "1",
	router_name                     = """BfdRouter 4""",
	session_count                   = "1",
	enable_auto_choose_source       = "1",
	enable_learned_remote_disc      = "1",
	ip_version                      = "4",
	session_discriminator           = "1",
	session_discriminator_step      = "0",
	remote_discriminator            = "1",
	remote_discriminator_step       = "0",
	source_ip_addr                  = "0.0.0.0",
	remote_ip_addr                  = "2.2.2.2",
	remote_ip_addr_step             = "0.0.0.1",
	hop_mode                        = "multiplehop",
	session_active                  = "1",
	session_name                    = """BFDv4 Session 4""",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_bfd_config', status)

bfdv4Interface_4_handle = status['bfd_v4_interface_handle']

status = ixiangpf.interface_config(
	protocol_handle                    = "/globals",
	arp_on_linkup                      = "0",
	single_arp_per_gateway             = "1",
	ipv4_send_arp_rate                 = "200",
	ipv4_send_arp_interval             = "1000",
	ipv4_send_arp_max_outstanding      = "400",
	ipv4_send_arp_scale_mode           = "port",
	ipv4_attempt_enabled               = "0",
	ipv4_attempt_rate                  = "200",
	ipv4_attempt_interval              = "1000",
	ipv4_attempt_scale_mode            = "port",
	ipv4_diconnect_enabled             = "0",
	ipv4_disconnect_rate               = "200",
	ipv4_disconnect_interval           = "1000",
	ipv4_disconnect_scale_mode         = "port",
	ipv4_re_send_arp_on_link_up        = "true",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', status)


status = ixiangpf.interface_config(
	protocol_handle                     = "/globals",
	ethernet_attempt_enabled            = "0",
	ethernet_attempt_rate               = "200",
	ethernet_attempt_interval           = "1000",
	ethernet_attempt_scale_mode         = "port",
	ethernet_diconnect_enabled          = "0",
	ethernet_disconnect_rate            = "200",
	ethernet_disconnect_interval        = "1000",
	ethernet_disconnect_scale_mode      = "port",
)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', status)


print('Waiting 60 seconds before starting protocol(s) ...')
time.sleep(60)
print('Starting all protocol(s) ...')

#########################################################
#Starting Protocols
#########################################################
status = ixiahlt.test_control(action='start_all_protocols')
# Check status
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('ixiahlt::traffic_control', status)
	print('Test case FAILED')
		
print("Waiting for 90 seconds")
time.sleep(60)

# -----------------------------------------------------------------------------------------------------------
# Checking Stats for both the ports
# ----------------------------------------------------------------------------------------------------------
handle_bfd_topology1 = '/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1'
handle_bfd_topology2 = '/topology:2/deviceGroup:1/ethernet:1/ipv4:1/bfdv4Interface:1'
handle_bfd_loop =  '/topology:1/deviceGroup:1/deviceGroup:1/ipv4Loopback:1/bfdv4Interface:1'
handle_bfd_loop1 =  '/topology:2/deviceGroup:1/deviceGroup:1/ipv4Loopback:1/bfdv4Interface:1'
otf = '::ixNet::OBJ-//globals/topology'


###########################################################
#Checking Aggregate Stats using emulation_bfd_info
###########################################################

print("Checking BFD Per Port Stats for Topology 1")
status = ixiangpf.emulation_bfd_info(
	handle = handle_bfd_topology1,
	mode   = 'aggregate',
	)

print status 
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)
	print('Test case FAILED')


sessions_configured = status[ports[0]]['aggregate']['sessions_configured']
sessions_configured_up = status[ports[0]]['aggregate']['sessions_configured_up']

if (sessions_configured != '6') or (sessions_configured_up != '6') :
	print ('Stats Mismatch...')
	print ('Session configured = '+sessions_configured+', Session up = '+sessions_configured_up)

print ('Got expected session stats: Session configured = '+sessions_configured+', Session up = '+sessions_configured_up)

print("Checking BFD Per Port Stats for Topology 2")
status = ixiangpf.emulation_bfd_info(
	handle = handle_bfd_topology2,
	mode   = 'aggregate',
	)
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', status)
	print('Test case FAILED')

sessions_configured = status[ports[1]]['aggregate']['sessions_configured']
sessions_configured_up = status[ports[1]]['aggregate']['sessions_configured_up']

if (sessions_configured != '6') or (sessions_configured_up != '6') :
	print ('Stats Mismatch...')
	print ('Session configured = '+sessions_configured+', Session up = '+sessions_configured_up)

print ('Got expected session stats: Session configured = '+sessions_configured+', Session up = '+sessions_configured_up)


######################################################################
#fetching and Verifying BFd learned info using emulation_bfd_info
######################################################################
print ("Checking Learned Info for Topology 1:item1")
status = ixiangpf.emulation_bfd_info (
	handle = handle_bfd_topology1,
	mode = 'learned_info' ,
	)

if status['status'] != IxiaHlt.SUCCESS:
            ErrorHandler('ixiahlt::traffic_control', status)
            print('Test case FAILED')

state = [status[handle_bfd_topology1]['bfd_learned_info']['peer_session_state']]
session_type = [status[handle_bfd_topology1]['bfd_learned_info']['session_type']]
session_used_by_protocol = [status[handle_bfd_topology1]['bfd_learned_info']['session_used_by_protocol']]
my_disc = [status[handle_bfd_topology1]['bfd_learned_info']['my_discriminator']]
my_ip = [status[handle_bfd_topology1]['bfd_learned_info']['my_ip_address']]
tx_interval = [status[handle_bfd_topology1]['bfd_learned_info']['recvd_tx_interval']]
multiplier = [status[handle_bfd_topology1]['bfd_learned_info']['recvd_multiplier']]
recvd_flags = [status[handle_bfd_topology1]['bfd_learned_info']['recvd_peer_flags']]

print status

####################################################################
#Performing Stop/Start BFD interface using emualtion_bfd_control
####################################################################

print('Performing Stop/Start on BFD interfaces and verifying stat')
status = ixiangpf.emulation_bfd_control (
	handle = handle_bfd_topology1,
	mode = 'stop'
	)

if status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('ixiahlt::traffic_control', status)
    print('Test case FAILED')
	
status = ixiangpf.emulation_bfd_control (
	handle = handle_bfd_topology1,
	mode = 'start'
	)

if status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('ixiahlt::traffic_control', status)
    print('Test case FAILED')
	
###############################################################################
#Changing bfd configuration using emulation_bfd_config and -mode as modify
###############################################################################
print('Changing Session discriminator and remote discriminator OTF, and verifing in Learned Info')
	
status = ixiangpf.emulation_bfd_config (
	handle = handle_bfd_topology1,
	mode = 'modify',
	ip_version = '4',
	session_discriminator = '20',
	remote_discriminator = '30',
	session_discriminator_step = '2',
	remote_discriminator_step = '3' )

if status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('ixiahlt::traffic_control', status)
    print('Test case FAILED')

ixNet.commit
ixNet.execute('applyOnTheFly', otf)


time.sleep(3)

status = ixiahlt.test_control(action='stop_all_protocols')

# Check status
if status['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('ixiahlt::traffic_control', status)
	print('Test case FAILED')

print 'TEST COMPLETED'



