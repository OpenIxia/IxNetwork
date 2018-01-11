################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    16/08/2016 - Poulomi Chatterjee - created sample                          #
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
#    This script intends to demonstrate how to use NGPF RSVPTE P2P HLPy API.   #
#                                                                              #
# 1. It will create 2 RSVP-TE P2P topologies.                                  #
#      - Configure P2P Ingress LSPs in Topology 1.                             #
#      - Configure P2P Egress LSPs in Topology 2.                              #
# 2. Start all protocol.                                                       #
# 3. Retrieve protocol statistics.                                             #
# 4. Retrieve protocol learned info.                                           #
# 5. On The Fly deactivate/activate LSPs.                                      #
# 6. Configure L2-L3 traffic.                                                  #
# 7. Start the L2-L3 traffic.                                                  #
# 8. Retrieve L2-L3 traffic stats.                                             #
# 9. Stop L2-L3 traffic.                                                       #
# 10. Stop allprotocols.                                                       #
#                                                                              #
# Ixia Software:                                                               #
#    IxOS      8.10-EA                                                         #
#    IxNetwork 8.10-EA-Update(2)                                               #
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
chassis_ip              = ['10.216.108.82']
tcl_server              = '10.216.108.82'
port_list               = [['7/7', '7/8']]
ixnetwork_tcl_server    = '10.216.108.14:2666';
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
        topology_name      = """RSVP-TE P2P Topology 1""",
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
        topology_name      = """RSVP-TE P2P Topology 2""",
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
# Configure RSVP Topologies in both ports as described in Description Section  #
#  above.                                                                      #
################################################################################

################################################################################
# Configuring RSVPTE protocols in Topology 1                                   #
################################################################################

#Creating RSVP-IF on top of ipv4 1 stack
print "Creating RSVP-IF on top of ipv4 1 stack\n"
_result_ = ixiangpf.emulation_rsvp_config(
	mode                                         = "create",
	handle                                       = ipv4_1_handle,
	using_gateway_ip                             = "1",
	dut_ip                                       = "20.20.20.1",
	label_space_start                            = "2000",
	label_space_end                              = "300000",
	enable_refresh_reduction                     = "0",
	summary_refresh_interval                     = "30000",
	enable_bundle_message_sending                = "0",
	enable_hello_extension                       = "0",
	hello_interval                               = "10000",
	hello_timeout_multiplier                     = "3",
	enable_graceful_restart_helper_mode          = "0",
	enable_graceful_restart_restarting_mode      = "0",
	advertised_restart_time                      = "30000",
	actual_restart_time                          = "15000",
	recovery_time                                = "30000",
	number_of_restarts                           = "0",
	restart_start_time                           = "30000",
	restart_up_time                              = "30000",
	enable_bfd_registration                      = "0",
	rsvp_neighbor_active                         = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_rsvp_config', _result_)

rsvpteIf_1_handle = _result_['rsvp_if_handle']

#Adding Network Group behind first DG
print "Adding Network Group behind first DG\n"
_result_ = ixiangpf.network_group_config(
	protocol_handle                       = deviceGroup_1_handle,
	protocol_name                         = """Network Group 1""",
	multiplier                            = "1",
	enable_device                         = "1",
	connected_to_handle                   = ethernet_1_handle,
	type                                  = "ipv4-prefix",
	ipv4_prefix_network_address           = "4.4.4.1",
	ipv4_prefix_network_address_step      = "0.0.0.0",
	ipv4_prefix_length                    = "32",
	ipv4_prefix_number_of_addresses       = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('network_group_config', _result_)
	
ipv4PrefixPools_1_handle = _result_['ipv4_prefix_pools_handle']
networkGroup_1_handle = _result_['network_group_handle']

# Adding second Device Group behind Network Group
print "Adding second Device Group behind Network Group\n"
_result_ = ixiangpf.topology_config(
	device_group_name            = """RSVP 1""",
	device_group_multiplier      = "1",
	device_group_enabled         = "1",
	device_group_handle          = networkGroup_1_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('topology_config', _result_)
deviceGroup_2_handle = _result_['device_group_handle']
    
# Adding ipv4 loopback in Second Device Group
print "Adding ipv4 loopback in Second Device Group\n"
_result_ = ixiangpf.interface_config(
	protocol_name            = """IPv4 Loopback 1""",
	protocol_handle          = deviceGroup_2_handle,
	enable_loopback          = "1",
	connected_to_handle      = networkGroup_1_handle,
	intf_ip_addr             = "4.4.4.1",
	intf_ip_addr_step        = "0.0.0.1",
	netmask                  = "255.255.255.255",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', _result_)
ipv4Loopback_1_handle = _result_['ipv4_loopback_handle']

# Adding RSVPTE LSPs over ipv4 Loopback
print "Adding RSVPTE LSPs over ipv4 Loopback\n"
_result_ = ixiangpf.emulation_rsvp_tunnel_config(
	mode                        = "create",
	handle                      = ipv4Loopback_1_handle,
	p2p_ingress_lsps_count      = "2",
	enable_p2p_egress           = "0",
	lsp_active                  = "true",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_rsvp_tunnel_config', _result_)
	
rsvpteLsps_1_handle = _result_['rsvpte_lsp_handle']

# Configure RSVPTE LSP parameters in ingress side
print "Configure RSVPTE LSP parameters in ingress side\n"
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "5.5.5.1",
	counter_step           = "0.0.3.0",
	counter_direction      = "increment",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_1_handle = _result_['multivalue_handle']


_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "1",
	counter_step           = "1",
	counter_direction      = "increment",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)
multivalue_2_handle = _result_['multivalue_handle']

_result_ = ixiangpf.emulation_rsvp_tunnel_config(
	mode                                       = "create",
	handle                                     = rsvpteLsps_1_handle,
	rsvp_p2p_ingress_enable                    = "1",
	remote_ip                                  = [multivalue_1_handle],
	tunnel_id                                  = [multivalue_2_handle],
	lsp_id                                     = ["101"],
	using_headend_ip                           = ["true"],
	backup_lsp_id                              = ["5000"],
	enable_path_re_optimization                = ["true"],
	p2p_ingress_active                         = ["true"],
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_rsvp_tunnel_config', _result_)

rsvpP2PIngressLsps_1_handle = _result_['rsvpte_p2p_ingress_handle']
print "Ingress Side topology Configuration complete in port 1...\n"

##############################################################################
# Configuring RSVPTE protocols in Topology 2                                 #
##############################################################################

#Creating RSVP-IF on top of ipv4 2 stack
print "Creating RSVP-IF on top of ipv4 2 stack\n"

_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "101.1.0.1",
	counter_step           = "0.0.1.0",
	counter_direction      = "increment",
	nest_step              = '%s' % ("0.0.0.1"),
	nest_owner             = '%s' % (topology_2_handle),
	nest_enabled           = '%s' % ("0"),
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_5_handle = _result_['multivalue_handle']

_result_ = ixiangpf.emulation_rsvp_config(
	mode                                         = "create",
	handle                                       = ipv4_2_handle,
	using_gateway_ip                             = "1",
	dut_ip                                       = multivalue_5_handle,
	label_space_start                            = "1500",
	rsvp_neighbor_active                         = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_rsvp_config', _result_)

rsvpteIf_2_handle = _result_['rsvp_if_handle']

#Adding IPv4 Prefix Pools behind first DG
print "Adding IPv4 Prefix Pools behind first DG\n"
_result_ = ixiangpf.network_group_config(
	protocol_handle                       = deviceGroup_4_handle,
	protocol_name                         = """Network Group 2""",
	multiplier                            = "2",
	enable_device                         = "1",
	connected_to_handle                   = ethernet_2_handle,
	type                                  = "ipv4-prefix",
	ipv4_prefix_network_address           = "5.5.5.1",
	ipv4_prefix_network_address_step      = "0.0.3.0",
	ipv4_prefix_length                    = "32",
	ipv4_prefix_number_of_addresses       = "1",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('network_group_config', _result_)

ipv4PrefixPools_2_handle = _result_['ipv4_prefix_pools_handle']
networkGroup_2_handle = _result_['network_group_handle']

# Add DG2 behind IPv4 Prefix Pool
print "Add DG2 behind IPv4 Prefix Pool\n"
_result_ = ixiangpf.topology_config(
	device_group_name            = """Device Group 4""",
	device_group_multiplier      = "1",
	device_group_enabled         = "1",
	device_group_handle          = networkGroup_2_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('topology_config', _result_)

deviceGroup_5_handle = _result_['device_group_handle']

# Add ipv4 loopback in DG2
print "Add ipv4 loopback in DG2\n"
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "5.5.5.1",
	counter_step           = "0.0.3.0",
	counter_direction      = "increment",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_6_handle = _result_['multivalue_handle']
_result_ = ixiangpf.interface_config(
	protocol_name            = """IPv4 Loopback 2""",
	protocol_handle          = deviceGroup_5_handle,
	enable_loopback          = "1",
	connected_to_handle      = networkGroup_2_handle,
	intf_ip_addr             = multivalue_6_handle,
	netmask                  = "255.255.255.255",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('interface_config', _result_)

ipv4Loopback_2_handle = _result_['ipv4_loopback_handle']

# Adding RSVP LSPs over ipv4 Loopback
print "Adding RSVP LSPs over ipv4 Loopback\n"
_result_ = ixiangpf.emulation_rsvp_tunnel_config(
	mode                        = "create",
	handle                      = ipv4Loopback_2_handle,
	p2p_ingress_lsps_count      = "0",
	enable_p2p_egress           = "1",
	lsp_active                  = "true",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_rsvp_tunnel_config', _result_)

rsvpteLsps_2_handle = _result_['rsvpte_lsp_handle']

# Configure RSVPTE LSP parameters in egress side
print "Configure RSVPTE LSP parameters in egress side\n";
_result_ = ixiangpf.multivalue_config(
	pattern                = "counter",
	counter_start          = "2001",
	counter_step           = "1",
	counter_direction      = "increment",
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('multivalue_config', _result_)

multivalue_7_handle = _result_['multivalue_handle']

_result_ = ixiangpf.emulation_rsvp_tunnel_config(
	mode                                     = "create",
	handle                                   = rsvpteLsps_2_handle,
	rsvp_p2p_egress_enable                   = "1",
	egress_refresh_interval                  = ["30000"],
	egress_timeout_multiplier                = ["3"],
	send_reservation_confirmation            = ["false"],
	enable_fixed_label_for_reservations      = ["true"],
	label_value                              = [multivalue_7_handle],
	reservation_style                        = ["se"],
	reflect_rro                              = ["true"],
	egress_number_of_rro_sub_objects         = ["0"],
	egress_active                            = ["true"],
)
if _result_['status'] != IxiaHlt.SUCCESS:
	ErrorHandler('emulation_rsvp_tunnel_config', _result_)

rsvpP2PEgressLsps_1_handle = _result_['rsvpte_p2p_egress_handle']

print "Egress Side topology Configuration complete in port 2...\n"

############################################################################
# Start All protocols                                                      #
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
print ('Fetching RSVP aggregated statistics')               
protostats = ixiangpf.emulation_rsvp_info(\
        handle = rsvpteIf_2_handle,
        mode   = 'stats')
if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_rsvp_info', protostats)

#pprint(protostats)
print(protostats)

############################################################################
# Retrieve protocol learned info                                           #
############################################################################

print "Fetching RSVP-TE P2P learned info\n"
# Check Learned Info in port1 
print "Check Learned Info in Port1 ...\n"
linfostatus = ixiangpf.emulation_rsvp_info(
        handle = rsvpteIf_2_handle,
        mode   = 'learned_info')
if linfostatus['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_rsvp_info', linfostatus)

print('Fetched Linfo successfully...')

assignedLinfo= linfostatus['/topology:2/deviceGroup:1/ethernet:1/ipv4:1/rsvpteIf:1']['learned_info']['assigned']
print("----------------RSVP-TE P2P assigned learned info -----------------------")
print(assignedLinfo)
print("-------------------------------------------------------------------------")	

linfostatus2 = ixiangpf.emulation_rsvp_info(
        handle = rsvpteIf_1_handle,
        mode   = 'learned_info')
if linfostatus2['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_rsvp_info', linfostatus2)

print('Fetched Linfo successfully...')

receivedLinfo= linfostatus2['/topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteIf:1']['learned_info']['received']
print("----------------RSVP-TE P2P received learned info -----------------------")
print(receivedLinfo)
print("-------------------------------------------------------------------------")

############################################################################
# On The Fly Deactivate/Activate LSPs
############################################################################
print "On The Fly Deactivate/Activate LSPs"
deactivate_lsp = ixiangpf.emulation_rsvp_tunnel_config (
   handle    = '/topology:2/deviceGroup:1/networkGroup:1/deviceGroup:1/ipv4Loopback:1/rsvpteLsps:1/rsvpP2PEgressLsps',
   mode      = 'disable')

if deactivate_lsp['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_rsvp_tunnel_config', deactivate_lsp)

print "Apply On The Fly changes\n";
applyChanges = ixiangpf.test_control (
   action = 'apply_on_the_fly_changes')

time.sleep(10)

print "On The Fly Activate Egress Lsps";
activate_lsp= ixiangpf.emulation_rsvp_tunnel_config (
   handle    = '/topology:2/deviceGroup:1/networkGroup:1/deviceGroup:1/ipv4Loopback:1/rsvpteLsps:1/rsvpP2PEgressLsps',
   mode      = 'enable')

if activate_lsp['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_rsvp_tunnel_config', activate_lsp)

print "Apply On The Fly changes\n";
applyChanges = ixiangpf.test_control (
   action = 'apply_on_the_fly_changes')

time.sleep(30)

################################################################################
# Configure_L2_L3_IPv4 traffic                                                 #
################################################################################
print ('Configuring L2-L3 IPv4 traffic item ...')
# Check status
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

_result_ = ixiangpf.traffic_config(
        mode                               = 'create',
        traffic_generator                  = 'ixnetwork_540',
        endpointset_count                  = 1,
        emulation_src_handle               = [[rsvpP2PIngressLsps_1_handle]],
        emulation_dst_handle               = [[rsvpP2PEgressLsps_1_handle]],
        name                               = 'RSVP-P2P-Traffic',
        circuit_endpoint_type              = 'ipv4',
        rate_pps                           = '1000',
        track_by                           = 'trackingenabled0 mplsFlowDescriptor0',
)
    
config_elements = ixiatcl.convert_tcl_list(_result_['traffic_item'])
current_config_element = config_elements[0]
    
print ('Configured L2-L3 IPv4 traffic item!!!')

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

print ('Let the traffic run for 30 seconds ...')
time.sleep(30)

############################################################################
# Retrieve L2-L3 traffic stats                                             #
############################################################################
print ('Retrieving L2-L3 traffic stats')
trafficStats = ixiangpf.traffic_stats(
        mode                 = 'all',
        traffic_generator       = 'ixnetwork_540',
        measure_mode          = 'mixed'
)
if trafficStats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_stats', trafficStats)

print(trafficStats)

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

time.sleep(5)
    
############################################################################
# Stop all protocols                                                       #
############################################################################
print ('Stopping all protocol(s) ...')
stop = ixiangpf.test_control(action='stop_all_protocols')
                  
if stop['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', stop)

print ('!!! Test Script Ends !!!')
