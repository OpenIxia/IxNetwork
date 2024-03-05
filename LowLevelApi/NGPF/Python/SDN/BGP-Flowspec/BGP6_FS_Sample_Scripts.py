# -*- coding: utf-8 -*-
################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
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
#    This script intends to demonstrate how to use NGPF BGP API                #
#    It will create 2 BGP topologies, it will start the emulation and          #
#    than it will retrieve and display few statistics and modify the FLOW-SPEC #
#    field through HLT.                                                        #
################################################################################

################################################################################
# Utilities                                                                    #    
################################################################################
from pprint import pprint
import sys, os
import time, re

from ixiatcl   import IxiaTcl
from ixiahlt   import IxiaHlt
from ixiangpf  import IxiaNgpf
from ixiaerror import IxiaError

if os.name == 'nt':
    # If the Python version is greater than 3.4 call IxiaTcl with
    # the Tcl 8.6 path.
    # Example: tcl_dependencies = ['/path/to/tcl8.6'];
    # ixiatcl = IxiaTcl(tcl_autopath=tcl_dependencies)
    ixiatcl = IxiaTcl()
else:
    # unix dependencies this may change accoring to your system. This is
    # required to make following packages available to ixiatcl object.
    # 1. Tclx   --> mandatory
    # 2. msgcat --> mandatory
    # 3. mpexpr --> optional
    tcl_dependencies = [
         '/usr/local/lib/',
         '/usr/lib/',
         '/usr/share/tcl8.5',
         '/usr/lib/tcl8.5',
         '/usr/lib/tk8.5',
         '/usr/share/tk8.5',
    ]
    ixiatcl = IxiaTcl(tcl_autopath=tcl_dependencies)
# endif

ixiahlt  = IxiaHlt(ixiatcl)
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

###############################################################################
# Specify your chassis/card port and IxNetwork client here
###############################################################################
chassis_ip           = "10.39.50.122"
tcl_server           = "10.39.50.122"
ixnetwork_tcl_server = "10.39.43.12:8009"
port_list            = "1/7 1/8"
cfgErrors            = 0

print("Connecting to chassis and client")
connect_result = ixiangpf.connect(
      ixnetwork_tcl_server = ixnetwork_tcl_server,
      tcl_server           = tcl_server,
      device               = chassis_ip,
      port_list            = port_list,
      break_locks          = 1,
      reset                = 1,
)

if connect_result['status'] != '1':
    ErrorHandler('connect', connect_result)
    
#Retrieving the port handles, in a list
ports = connect_result['vport_list'].split()

################################################################################
# Creating topology and device group                                           #
################################################################################
# Creating a topology on first port
print("Adding topology 1 on port 1")
topology_1_status = ixiangpf.topology_config(
    topology_name      = """BGP6 Topology 1""",
    port_handle        = ports[0],
)
if topology_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config',topology_1_status)
    
topology_1_handle = topology_1_status['topology_handle']

# Creating a device group in BGP topology1 
print("Creating device group 1 in topology 1") 
device_group_1_status = ixiangpf.topology_config(
    topology_handle              = topology_1_handle,
    device_group_name            = """BGP6 Topology 1 Router""",
    device_group_multiplier      = "1",
    device_group_enabled         = "1",
)
if device_group_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', device_group_1_status)
    
deviceGroup_1_handle = device_group_1_status['device_group_handle']

# Creating a topology on second port
print("Adding topology 2 on port 2")
topology_2_status = ixiangpf.topology_config(
    topology_name      = """BGP6 Topology 2""",
    port_handle        = ports[1],
)
if topology_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', topology_2_status)
    
topology_2_handle = topology_2_status['topology_handle']

# Creating a device group in BGP topology2
print("Creating device group 2 in topology 2")
device_group_2_status = ixiangpf.topology_config(
    topology_handle              = topology_2_handle,
    device_group_name            = """BGP6 Topology 2 Router""",
    device_group_multiplier      = "1",
    device_group_enabled         = "1",
)
if device_group_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', device_group_2_status)
    
deviceGroup_2_handle = device_group_2_status['device_group_handle']

################################################################################
#  Configure protocol interfaces                                               #
################################################################################
# Creating Ethernet stack for the first Device Group 
print("Creating Ethernet stack for the first Device Group")
ethernet_1_status= ixiangpf.interface_config(
    protocol_name                = """Ethernet 1""",
    protocol_handle              = deviceGroup_1_handle,
    mtu                          = "1500",
    src_mac_addr                 = "18.03.73.c7.6c.b1",
    src_mac_addr_step            = "00.00.00.00.00.00",
    vlan                    	 = "0",
    vlan_id_count           	 = '%s' % ("0"),
    use_vpn_parameters      	 = "0",
    site_id                 	 = "0",
)
if ethernet_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ethernet_1_status)
    
ethernet_1_handle = ethernet_1_status['ethernet_handle']

# Creating Ethernet stack for the second Device Group
print("Creating Ethernet for the second Device Group")   
ethernet_2_status = ixiangpf.interface_config(
    protocol_name                = """Ethernet 2""",
    protocol_handle              = deviceGroup_2_handle,
    mtu                          = "1500",
    src_mac_addr                 = "18.03.73.c7.6c.01",
    src_mac_addr_step            = "00.00.00.00.00.00",
    vlan                    	 = "0",
    vlan_id_count            	 = '%s' % ("0"),
    use_vpn_parameters      	 = "0",
    site_id                 	 = "0",
)
if ethernet_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ethernet_2_status)

ethernet_2_handle = ethernet_2_status['ethernet_handle']

# Creating IPv6 Stack on top of Ethernet Stack for the first Device Group                                 
print("Creating IPv6 Stack on top of Ethernet 1 Stack for the first Device Group")
ipv6_1_status = ixiangpf.interface_config(
    protocol_name                     = """IPv6 1""",
    protocol_handle                   = ethernet_1_handle,
    ipv6_multiplier                   = "1",
    ipv6_resolve_gateway              = "1",
    ipv6_manual_gateway_mac           = "00.00.00.00.00.01",
    ipv6_manual_gateway_mac_step      = "00.00.00.00.00.00",
    ipv6_gateway                      = "2000:0:0:1:0:0:0:1",
    ipv6_gateway_step                 = "::0",
    ipv6_intf_addr                    = "2000:0:0:1:0:0:0:2",
    ipv6_intf_addr_step               = "::0",
    ipv6_prefix_length                = "64",
)
if ipv6_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ipv6_1_status)
    
ipv6_1_handle = ipv6_1_status['ipv6_handle']

# Creating IPv6 Stack on top of Ethernet 1 Stack for the second Device Group 
print("Creating IPv6 2 stack on Ethernet 2 stack for the second Device Group")
ipv6_2_status = ixiangpf.interface_config(
    protocol_name                     = """IPv6 2""",
    protocol_handle                   = ethernet_2_handle,
    ipv6_multiplier                   = "1",
    ipv6_resolve_gateway              = "1",
    ipv6_manual_gateway_mac           = "00.00.00.00.00.01",
    ipv6_manual_gateway_mac_step      = "00.00.00.00.00.00",
    ipv6_gateway                      = "2000:0:0:1:0:0:0:2",
    ipv6_gateway_step                 = "::0",
    ipv6_intf_addr                    = "2000:0:0:1:0:0:0:1",
    ipv6_intf_addr_step               = "::0",
    ipv6_prefix_length                = "64",
)
if ipv6_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ipv6_2_status)
    
ipv6_2_handle = ipv6_2_status['ipv6_handle']

################################################################################
# BGP6 protocol configurations On Top Of IPv6 Stack at Peer1 side                                             # 
################################################################################
# This will Create BGP6 Stack on top of IPv6 Stack of Topology1
print("Creating BGP6 Stack on top of IPv6 1 stack on Topology 1")     

bgp_v6_interface_1_status = ixiangpf.emulation_bgp_config(
    mode                                         = "enable",
    active                                       = "1",
    md5_enable                                   = "0",
    md5_key                                      = "Ixia",
    handle                                       = ipv6_1_handle,
    ip_version                                   = "6",
    remote_ipv6_addr                             = "2000:0:0:1:0:0:0:1",
    next_hop_enable                              = "0",
    next_hop_ip                                  = "0.0.0.0",
    enable_4_byte_as                             = "0",
    local_as                                     = "0",
    local_as4                                    = "0",
    update_interval                              = "0",
    count                                        = "1",
    local_router_id                              = "192.0.0.1",
    local_router_id_step                         = "0.0.0.0",
    hold_time                                    = "90",
    neighbor_type                                = "internal",
    graceful_restart_enable                      = "0",
    restart_time                                 = "45",
    stale_time                                   = "0",
    tcp_window_size                              = "8192",
    local_router_id_enable                       = "1",
    ipv4_capability_mdt_nlri                     = "0",
    ipv4_capability_unicast_nlri                 = "1",
    ipv4_filter_unicast_nlri                     = "1",
    ipv4_capability_multicast_nlri               = "1",
    ipv4_filter_multicast_nlri                   = "0",
    ipv4_capability_mpls_nlri                    = "1",
    ipv4_filter_mpls_nlri                        = "0",
    ipv4_capability_mpls_vpn_nlri                = "1",
    ipv4_filter_mpls_vpn_nlri                    = "0",
    ipv6_capability_unicast_nlri                 = "1",
    ipv6_filter_unicast_nlri                     = "1",
    ipv6_capability_multicast_nlri               = "1",
    ipv6_filter_multicast_nlri                   = "0",
    ipv6_capability_mpls_nlri                    = "1",
    ipv6_filter_mpls_nlri                        = "0",
    ipv6_capability_mpls_vpn_nlri                = "1",
    ipv6_filter_mpls_vpn_nlri                    = "0",
    capability_route_refresh                     = "1",
    capability_route_constraint                  = "0",
    ttl_value                                    = "64",
    updates_per_iteration                        = "1",
    bfd_registration                             = "0",
    bfd_registration_mode                        = "multi_hop",
    vpls_capability_nlri                         = "1",
    vpls_filter_nlri                             = "0",
    act_as_restarted                             = "0",
    discard_ixia_generated_routes                = "0",
    flap_down_time                               = "0",
    local_router_id_type                         = "same",
    enable_flap                                  = "0",
    send_ixia_signature_with_routes              = "0",
    flap_up_time                                 = "0",
    ipv4_capability_multicast_vpn_nlri           = "0",
    ipv4_filter_multicast_vpn_nlri               = "0",
    ipv6_capability_multicast_vpn_nlri           = "0",
    ipv6_filter_multicast_vpn_nlri               = "0",
    advertise_end_of_rib                         = "0",
    configure_keepalive_timer                    = "0",
    keepalive_timer                              = "30",
    as_path_set_mode                             = "no_include",
    router_id                                    = "192.0.0.1",
    filter_link_state                            = "0",
    capability_linkstate_nonvpn                  = "0",
    bgp_ls_id                                    = "0",
    instance_id                                  = "0",
    number_of_communities                        = "1",
    enable_community                             = "0",
    number_of_ext_communities                    = "1",
    enable_ext_community                         = "0",
    enable_override_peer_as_set_mode             = "0",
    bgp_ls_as_set_mode                           = "include_as_seq",
    number_of_as_path_segments                   = "1",
    enable_as_path_segments                      = "1",
    number_of_clusters                           = "1",
    enable_cluster                               = "0",
    ethernet_segments_count                      = "0",
    filter_evpn                                  = "0",
    evpn                                         = "0",
    operational_model                            = "symmetric",
    routers_mac_or_irb_mac_address               = "00:01:03:00:00:01",
    capability_ipv4_unicast_add_path             = "0",
    capability_ipv6_unicast_add_path             = "0",
    ipv4_mpls_add_path_mode                      = "both",
    ipv6_mpls_add_path_mode                      = "both",
    ipv4_unicast_add_path_mode                   = "both",
    ipv6_unicast_add_path_mode                   = "both",
    ipv4_mpls_capability                         = "0",
    ipv6_mpls_capability                         = "0",
    capability_ipv4_mpls_add_path                = "0",
    capability_ipv6_mpls_add_path                = "0",
    custom_sid_type                              = "40",
    srgb_count                                   = "1",
    start_sid                                    = ["16000"],
    sid_count                                    = ["8000"],
    ipv4_multiple_mpls_labels_capability         = "0",
    ipv6_multiple_mpls_labels_capability         = "0",
    mpls_labels_count_for_ipv4_mpls_route        = "1",
    mpls_labels_count_for_ipv6_mpls_route        = "1",
    noOfUserDefinedAfiSafi                       = "0",
    capability_ipv4_unicast_flowSpec             = "1",
    filter_ipv4_unicast_flowSpec                 = "1",
    capability_ipv6_unicast_flowSpec             = "1",
    filter_ipv6_unicast_flowSpec                 = "1",
    always_include_tunnel_enc_ext_community      = "false",
    ip_vrf_to_ip_vrf_type                        = "interfacefullWithUnnumberedCorefacingIRB",
    irb_interface_label                          = "16",
    irb_ipv6_address                             = "10:0:0:0:0:0:0:1",                    
)

if bgp_v6_interface_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_bgp_config', bgp_v6_interface_1_status)
    
bgpInterface_1_handle = bgp_v6_interface_1_status['bgp_handle']

################################################################################
# BGP FLOW SPEC configurations AT PEER1 Side on Top of BGP6 Stack                                               # 
################################################################################
# This will Create BGP IPv6 Flow spec on top of BGP6 Stack of Topology1
print("Creating BGP IPv6 Flow Spec on top of BGP6 stack on Topology 1")
bgpFlowSpecRangeList_v6_interface_1_status = ixiangpf.emulation_bgp_flow_spec_config(
    mode                                               = "enable",
    fs_mode                                            = "fsv6",
    handle                                             = bgpInterface_1_handle,
    no_of_flowSpecRangeV6                              = "1",
    active                                             = "1",
    flowSpecName                                       = """BGP Flow Spec 11-1""",
    fsv6_enableDestPrefix                              = "1",
    fsv6_destPrefix                                    = "1:0:0:0:0:0:1:1",
    fsv6_destPrefixLength                              = "64",
    fsv6_destPrefixOffset                              = "34",
    fsv6_enableSrcPrefix                               = "1",
    fsv6_srcPrefix                                     = "1:1:0:0:0:0:0:1",
    fsv6_srcPrefixLength                               = "80",
    fsv6_srcPrefixOffset                               = "48",
    fsv6_nextHeader                                    = "120",
    portMatch                                          = "10",
    destPortMatch                                      = "40",
    srcPortMatch                                       = "50",
    icmpTypeMatch                                      = "80",
    icmpCodeMatch                                      = "90",
    tcpFlagsMatch                                      = "(cwr)",
    ipPacketMatch                                      = "110",
    dscpMatch                                          = "10",
    fsv6_fragmentMatch                                 = "(lf)",
    fsv6_flowLabel                                     = "40",
    enable_traffic_rate                                = "1",
    trafficRate                                        = "1000",
    enable_trafficAction                               = "1",
    terminalAction                                     = "1",
    trafficActionSample                                = "1",
    enable_redirect                                    = "1",
    redirect_ext_communities_type                      = "rdIPv4",
    as_2_bytes                                         = "100",
    as_4_bytes                                         = "400",
    fsv6_ipv6                                          = "1:1:0:0:0:0:0:1",
    assigned_number_2_octets                           = "500",
    assigned_number_4_octets                           = "800",
    Cbit                                               = "1",
    nextHop                                            = "1.1.1.1",
    enable_trafficMarking                              = "1",
    dscp                                               = "10",
    fsv6_enable_redirectIPv6                           = "1",
    fsv6_redirectIPv6                                  = "1:1:0:0:0:0:0:1",
    enable_next_hop                                    = "1",
    set_next_hop                                       = "sameaslocalip",
    set_next_hop_ip_type                               = "ipv4",
    ipv4_next_hop                                      = "10.10.10.10",
    ipv6_next_hop                                      = "a:0:0:0:0:0:0:b",
    enable_origin                                      = "1",
    origin                                             = "igp",
    enable_local_preference                            = "1",
    local_preference                                   = "100",
    enable_multi_exit_discriminator                    = "1",
    multi_exit_discriminator                           = "300",
    enable_atomic_aggregate                            = "1",
    enable_aggregator_id                               = "1",
    aggregator_id                                      = "2.2.2.2",
    aggregator_as                                      = "200",
    enable_originator_id                               = "1",
    originator_id                                      = "6.6.6.6",
    enable_community                                   = "1",
    number_of_communities                              = "1",
    community_type                                     = ["no_export"],
    community_as_number                                = ["123"],
    community_last_two_octets                          = ["234"],
    enable_ext_community                               = "1",
    number_of_ext_communities                          = "1",
    ext_communities_type                               = ["admin_as_two_octet"],
    ext_communities_subtype                            = ["route_target"],
    ext_community_as_number                            = ["123"],
    ext_community_target_assigned_number_4_octets      = ["1"],
    ext_community_ip                                   = ["1.1.1.1"],
    ext_community_as_4_bytes                           = ["1"],
    ext_community_target_assigned_number_2_octets      = ["1"],
    ext_community_opaque_data                          = ["aa"],
    ext_community_colorCObits                          = ["00"],
    ext_community_colorReservedBits                    = ["123"],
    ext_community_colorValue                           = ["1234"],
    ext_community_linkBandwidth                        = ["1000"],
    enable_override_peer_as_set_mode                   = "1",
    as_path_set_mode                                   = "include_as_seq",
    enable_as_path_segments                            = "1",
    no_of_as_path_segments                             = "1",
    enable_as_path_segment                             = ["1"],
    as_path_segment_type                               = ["as_set"],
    number_of_as_number_in_segment                     = ["1"],
    as_path_segment_enable_as_number                   = ["1"],
    as_path_segment_as_number                          = ["100"],
    enable_cluster                                     = "1",
    no_of_clusters                                     = "1",
    cluster_id                                         = ["1.2.3.4"],
)
if bgpFlowSpecRangeList_v6_interface_1_status['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('emulation_bgp_flow_spec_config', bgpFlowSpecRangeList_v6_interface_1_status)

bgpFlowSpecRangesListV6_1_handle = bgpFlowSpecRangeList_v6_interface_1_status['bgp_flowSpecV6_handle']

################################################################################
# BGP protocol configurations On Top Of IPv6 Stack at Peer2 side                                             # 
################################################################################
# This will Create BGP6 Stack on top of IPv6 Stack of Topology2
print("Creating BGP6 Stack on top of IPv6 1 stack on Topology 2")
bgp_v6_interface_2_status = ixiangpf.emulation_bgp_config(
    mode                                         = "enable",
    active                                       = "1",
    md5_enable                                   = "0",
    md5_key                                      = "Ixia",
    handle                                       = ipv6_2_handle,
    ip_version                                   = "6",
    remote_ipv6_addr                             = "2000:0:0:1:0:0:0:2",
    next_hop_enable                              = "0",
    next_hop_ip                                  = "0.0.0.0",
    enable_4_byte_as                             = "0",
    local_as                                     = "0",
    local_as4                                    = "0",
    update_interval                              = "0",
    count                                        = "1",
    local_router_id                              = "193.0.0.1",
    local_router_id_step                         = "0.0.0.0",
    hold_time                                    = "90",
    neighbor_type                                = "internal",
    graceful_restart_enable                      = "0",
    restart_time                                 = "45",
    stale_time                                   = "0",
    tcp_window_size                              = "8192",
    local_router_id_enable                       = "1",
    ipv4_capability_mdt_nlri                     = "0",
    ipv4_capability_unicast_nlri                 = "1",
    ipv4_filter_unicast_nlri                     = "1",
    ipv4_capability_multicast_nlri               = "1",
    ipv4_filter_multicast_nlri                   = "0",
    ipv4_capability_mpls_nlri                    = "1",
    ipv4_filter_mpls_nlri                        = "0",
    ipv4_capability_mpls_vpn_nlri                = "1",
    ipv4_filter_mpls_vpn_nlri                    = "0",
    ipv6_capability_unicast_nlri                 = "1",
    ipv6_filter_unicast_nlri                     = "1",
    ipv6_capability_multicast_nlri               = "1",
    ipv6_filter_multicast_nlri                   = "0",
    ipv6_capability_mpls_nlri                    = "1",
    ipv6_filter_mpls_nlri                        = "0",
    ipv6_capability_mpls_vpn_nlri                = "1",
    ipv6_filter_mpls_vpn_nlri                    = "0",
    capability_route_refresh                     = "1",
    capability_route_constraint                  = "0",
    ttl_value                                    = "64",
    updates_per_iteration                        = "1",
    bfd_registration                             = "0",
    bfd_registration_mode                        = "multi_hop",
    vpls_capability_nlri                         = "1",
    vpls_filter_nlri                             = "0",
    act_as_restarted                             = "0",
    discard_ixia_generated_routes                = "0",
    flap_down_time                               = "0",
    local_router_id_type                         = "same",
    enable_flap                                  = "0",
    send_ixia_signature_with_routes              = "0",
    flap_up_time                                 = "0",
    ipv4_capability_multicast_vpn_nlri           = "0",
    ipv4_filter_multicast_vpn_nlri               = "0",
    ipv6_capability_multicast_vpn_nlri           = "0",
    ipv6_filter_multicast_vpn_nlri               = "0",
    advertise_end_of_rib                         = "0",
    configure_keepalive_timer                    = "0",
    keepalive_timer                              = "30",
    as_path_set_mode                             = "no_include",
    router_id                                    = "193.0.0.1",
    filter_link_state                            = "0",
    capability_linkstate_nonvpn                  = "0",
    bgp_ls_id                                    = "0",
    instance_id                                  = "0",
    number_of_communities                        = "1",
    enable_community                             = "0",
    number_of_ext_communities                    = "1",
    enable_ext_community                         = "0",
    enable_override_peer_as_set_mode             = "0",
    bgp_ls_as_set_mode                           = "include_as_seq",
    number_of_as_path_segments                   = "1",
    enable_as_path_segments                      = "1",
    number_of_clusters                           = "1",
    enable_cluster                               = "0",
    ethernet_segments_count                      = "0",
    filter_evpn                                  = "0",
    evpn                                         = "0",
    operational_model                            = "symmetric",
    routers_mac_or_irb_mac_address               = "00:01:04:00:00:01",
    capability_ipv4_unicast_add_path             = "0",
    capability_ipv6_unicast_add_path             = "0",
    ipv4_mpls_add_path_mode                      = "both",
    ipv6_mpls_add_path_mode                      = "both",
    ipv4_unicast_add_path_mode                   = "both",
    ipv6_unicast_add_path_mode                   = "both",
    ipv4_mpls_capability                         = "0",
    ipv6_mpls_capability                         = "0",
    capability_ipv4_mpls_add_path                = "0",
    capability_ipv6_mpls_add_path                = "0",
    custom_sid_type                              = "40",
    srgb_count                                   = "1",
    start_sid                                    = ["16000"],
    sid_count                                    = ["8000"],
    ipv4_multiple_mpls_labels_capability         = "0",
    ipv6_multiple_mpls_labels_capability         = "0",
    mpls_labels_count_for_ipv4_mpls_route        = "1",
    mpls_labels_count_for_ipv6_mpls_route        = "1",
    noOfUserDefinedAfiSafi                       = "0",
    capability_ipv4_unicast_flowSpec             = "1",
    filter_ipv4_unicast_flowSpec                 = "1",
    capability_ipv6_unicast_flowSpec             = "1",
    filter_ipv6_unicast_flowSpec                 = "1",
    always_include_tunnel_enc_ext_community      = "false",
    ip_vrf_to_ip_vrf_type                        = "interfacefullWithUnnumberedCorefacingIRB",
    irb_interface_label                          = "16",
    irb_ipv6_address                             = "10:0:0:0:0:0:0:1",
)

if bgp_v6_interface_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_bgp_config', bgp_v6_interface_2_status)
    
bgpInterface_2_handle = bgp_v6_interface_2_status['bgp_handle']

################################################################################
# BGP IPv6 FLOW SPEC configurations AT PEER1 Side on Top of BGP6 Stack                                               # 
################################################################################
# This will Create BGP IPv6 Flow spec on top of BGP6 Stack of Topology2
print("Creating BGP IPv6 Flow Spec on top of BGP6 stack on Topology 2")
bgpFlowSpecRangeList_v6_interface_2_status = ixiangpf.emulation_bgp_flow_spec_config(
    mode                                               = "enable",
    fs_mode                                            = "fsv6",
    handle                                             = bgpInterface_2_handle,
    no_of_flowSpecRangeV6                              = "1",
    active                                             = "1",
    flowSpecName                                       = """BGP Flow Spec 11-1""",
    fsv6_enableDestPrefix                              = "1",
    fsv6_destPrefix                                    = "1:0:0:0:0:0:1:1",
    fsv6_destPrefixLength                              = "64",
    fsv6_destPrefixOffset                              = "34",
    fsv6_enableSrcPrefix                               = "1",
    fsv6_srcPrefix                                     = "1:1:0:0:0:0:0:1",
    fsv6_srcPrefixLength                               = "96",
    fsv6_srcPrefixOffset                               = "64",
    fsv6_nextHeader                                    = "120",
    portMatch                                          = "20",
    destPortMatch                                      = "30",
    srcPortMatch                                       = "60",
    icmpTypeMatch                                      = "70",
    icmpCodeMatch                                      = "100",
    tcpFlagsMatch                                      = "(fin)",
    ipPacketMatch                                      = "120",
    dscpMatch                                          = "20",
    fsv6_fragmentMatch                                 = "(ff)",
    fsv6_flowLabel                                     = "30",
    enable_traffic_rate                                = "1",
    trafficRate                                        = "2000",
    enable_trafficAction                               = "1",
    terminalAction                                     = "1",
    trafficActionSample                                = "1",
    enable_redirect                                    = "1",
    redirect_ext_communities_type                      = "rdIPv4",
    as_2_bytes                                         = "200",
    as_4_bytes                                         = "300",
    fsv6_ipv6                                          = "1:1:0:0:0:0:0:1",
    assigned_number_2_octets                           = "600",
    assigned_number_4_octets                           = "700",
    Cbit                                               = "1",
    nextHop                                            = "1.1.1.1",
    enable_trafficMarking                              = "1",
    dscp                                               = "20",
    fsv6_enable_redirectIPv6                           = "1",
    fsv6_redirectIPv6                                  = "1:1:0:0:0:0:0:1",
    enable_next_hop                                    = "1",
    set_next_hop                                       = "manually",
    set_next_hop_ip_type                               = "ipv6",
    ipv4_next_hop                                      = "11.11.11.11",
    ipv6_next_hop                                      = "c:0:0:0:0:0:0:d",
    enable_origin                                      = "1",
    origin                                             = "igp",
    enable_local_preference                            = "1",
    local_preference                                   = "200",
    enable_multi_exit_discriminator                    = "1",
    multi_exit_discriminator                           = "400",
    enable_atomic_aggregate                            = "1",
    enable_aggregator_id                               = "1",
    aggregator_id                                      = "3.3.3.3",
    aggregator_as                                      = "300",
    enable_originator_id                               = "1",
    originator_id                                      = "7.7.7.7",
    enable_community                                   = "1",
    number_of_communities                              = "1",
    community_type                                     = ["no_export"],
    community_as_number                                = ["321"],
    community_last_two_octets                          = ["432"],
    enable_ext_community                               = "1",
    number_of_ext_communities                          = "1",
    ext_communities_type                               = ["admin_as_two_octet"],
    ext_communities_subtype                            = ["route_target"],
    ext_community_as_number                            = ["1"],
    ext_community_target_assigned_number_4_octets      = ["1"],
    ext_community_ip                                   = ["1.1.1.1"],
    ext_community_as_4_bytes                           = ["1"],
    ext_community_target_assigned_number_2_octets      = ["1"],
    ext_community_opaque_data                          = ["bb"],
    ext_community_colorCObits                          = ["00"],
    ext_community_colorReservedBits                    = ["214"],
    ext_community_colorValue                           = ["567"],
    ext_community_linkBandwidth                        = ["2000"],
    enable_override_peer_as_set_mode                   = "1",
    as_path_set_mode                                   = "include_as_seq",
    enable_as_path_segments                            = "1",
    no_of_as_path_segments                             = "1",
    enable_as_path_segment                             = ["1"],
    as_path_segment_type                               = ["as_set"],
    number_of_as_number_in_segment                     = ["1"],
    as_path_segment_enable_as_number                   = ["1"],
    as_path_segment_as_number                          = ["200"],
    enable_cluster                                     = "1",
    no_of_clusters                                     = "1",
    cluster_id                                         = ["5.6.7.8"],
)

if bgpFlowSpecRangeList_v6_interface_2_status['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('emulation_bgp_flow_spec_config', bgpFlowSpecRangeList_v6_interface_2_status)

bgpFlowSpecRangesListV6_2_handle = bgpFlowSpecRangeList_v6_interface_2_status['bgp_flowSpecV6_handle']  

#####################################################################################
#Modifying the value of Flow Spec Field of BGP6 PEER1 and PEER2
#####################################################################################
time.sleep(10)
print "wait for 10Sec"
print "After 5 secs Modify the value of Flow-Spec fields of BGP IPv6 Flow SPec Range of BGP6 PEER1"
time.sleep(5)

print "Modifying the value of Flow-Spec fields of BGP IPv6 FLOW SPEC RANGE of BGP6 PEER1"
bgpFlowSpecRangeList_v6_interface_1_status = ixiangpf.emulation_bgp_flow_spec_config(
    mode                                               = "modify",
    fs_mode                                            = "fsv6",
    handle                                             = bgpFlowSpecRangesListV6_1_handle,
    no_of_flowSpecRangeV6                              = "1",
    active                                             = "1",
    flowSpecName                                       = """BGP Flow Spec 11-1""",
    fsv6_enableDestPrefix                              = "1",
    fsv6_destPrefix                                    = "1a:b0:c0:d0:ef0:120:134:1",
    fsv6_destPrefixLength                              = "64",
    fsv6_destPrefixOffset                              = "34",
    fsv6_enableSrcPrefix                               = "1",
    fsv6_srcPrefix                                     = "123:145:0675:0876:0abc:0def:0:1",
    fsv6_srcPrefixLength                               = "80",
    fsv6_srcPrefixOffset                               = "48",
    fsv6_nextHeader                                    = "120",
    portMatch                                          = "10",
    destPortMatch                                      = "40",
    srcPortMatch                                       = "50",
    icmpTypeMatch                                      = "80",
    icmpCodeMatch                                      = "90",
    tcpFlagsMatch                                      = "(syn)",
    ipPacketMatch                                      = "110",
    dscpMatch                                          = "10",
    fsv6_fragmentMatch                                 = "(ff)",
    fsv6_flowLabel                                     = "40",
    enable_traffic_rate                                = "1",
    trafficRate                                        = "1000",
    enable_trafficAction                               = "1",
    terminalAction                                     = "1",
    trafficActionSample                                = "1",
    enable_redirect                                    = "1",
    redirect_ext_communities_type                      = "rdIPv4",
    as_2_bytes                                         = "100",
    as_4_bytes                                         = "400",
    fsv6_ipv6                                          = "1bc:1de:0f3:120:340:560:0:1",
    assigned_number_2_octets                           = "500",
    assigned_number_4_octets                           = "800",
    Cbit                                               = "1",
    nextHop                                            = "1.1.1.1",
    enable_trafficMarking                              = "1",
    dscp                                               = "10",
    fsv6_enable_redirectIPv6                           = "1",
    fsv6_redirectIPv6                                  = "1a:1b:0cd:0ef:230:450:670:1",
    enable_next_hop                                    = "1",
    set_next_hop                                       = "sameaslocalip",
    set_next_hop_ip_type                               = "ipv4",
    ipv4_next_hop                                      = "150.160.170.180",
    ipv6_next_hop                                      = "a:a:b:c:d:e:f:b",
    enable_origin                                      = "1",
    origin                                             = "igp",
    enable_local_preference                            = "1",
    local_preference                                   = "100",
    enable_multi_exit_discriminator                    = "1",
    multi_exit_discriminator                           = "300",
    enable_atomic_aggregate                            = "1",
    enable_aggregator_id                               = "1",
    aggregator_id                                      = "2.2.2.2",
    aggregator_as                                      = "200",
    enable_originator_id                               = "1",
    originator_id                                      = "66.67.68.69",
    enable_community                                   = "1",
    number_of_communities                              = "1",
    community_type                                     = ["no_export"],
    community_as_number                                = ["123"],
    community_last_two_octets                          = ["234"],
    enable_ext_community                               = "1",
    number_of_ext_communities                          = "1",
    ext_communities_type                               = ["admin_as_two_octet"],
    ext_communities_subtype                            = ["route_target"],
    ext_community_as_number                            = ["123"],
    ext_community_target_assigned_number_4_octets      = ["1"],
    ext_community_ip                                   = ["1.1.1.1"],
    ext_community_as_4_bytes                           = ["1"],
    ext_community_target_assigned_number_2_octets      = ["1"],
    ext_community_opaque_data                          = ["aa"],
    ext_community_colorCObits                          = ["00"],
    ext_community_colorReservedBits                    = ["123"],
    ext_community_colorValue                           = ["1234"],
    ext_community_linkBandwidth                        = ["1000"],
    enable_override_peer_as_set_mode                   = "1",
    as_path_set_mode                                   = "include_as_seq",
    enable_as_path_segments                            = "1",
    no_of_as_path_segments                             = "1",
    enable_as_path_segment                             = ["1"],
    as_path_segment_type                               = ["as_set"],
    number_of_as_number_in_segment                     = ["1"],
    as_path_segment_enable_as_number                   = ["1"],
    as_path_segment_as_number                          = ["100"],
    enable_cluster                                     = "1",
    no_of_clusters                                     = "1",
    cluster_id                                         = ["11.22.33.45"],
)
if bgpFlowSpecRangeList_v6_interface_1_status['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('emulation_bgp_flow_spec_config', bgpFlowSpecRangeList_v6_interface_1_status)

time.sleep(5)

print "After 5 secs Modify the value of Flow-Spec fields of BGP IPv6 Flow SPec Range of BGP6 PEER2"
time.sleep(5)

print "Modifying the value of Flow-Spec fields of BGP IPv6 FLOW SPEC RANGE of BGP6 PEER2"
bgpFlowSpecRangeList_v6_interface_2_status = ixiangpf.emulation_bgp_flow_spec_config(
    mode                                               = "modify",
    fs_mode                                            = "fsv6",
    handle                                             = bgpFlowSpecRangesListV6_2_handle,
    no_of_flowSpecRangeV6                              = "1",
    active                                             = "1",
    flowSpecName                                       = """BGP Flow Spec 11-1""",
    fsv6_enableDestPrefix                              = "1",
    fsv6_destPrefix                                    = "1:a0:b0:c0:d0:e0:1f:1",
    fsv6_destPrefixLength                              = "64",
    fsv6_destPrefixOffset                              = "34",
    fsv6_enableSrcPrefix                               = "1",
    fsv6_srcPrefix                                     = "1:1:a0:4540:560:5650:780:1",
    fsv6_srcPrefixLength                               = "96",
    fsv6_srcPrefixOffset                               = "64",
    fsv6_nextHeader                                    = "120",
    portMatch                                          = "20",
    destPortMatch                                      = "30",
    srcPortMatch                                       = "60",
    icmpTypeMatch                                      = "70",
    icmpCodeMatch                                      = "100",
    tcpFlagsMatch                                      = "(rst)",
    ipPacketMatch                                      = "120",
    dscpMatch                                          = "20",
    fsv6_fragmentMatch                                 = "(lf)",
    fsv6_flowLabel                                     = "30",
    enable_traffic_rate                                = "1",
    trafficRate                                        = "2220",
    enable_trafficAction                               = "1",
    terminalAction                                     = "1",
    trafficActionSample                                = "1",
    enable_redirect                                    = "1",
    redirect_ext_communities_type                      = "rdIPv4",
    as_2_bytes                                         = "200",
    as_4_bytes                                         = "300",
    fsv6_ipv6                                          = "1:1:0:0:0:0:0:1",
    assigned_number_2_octets                           = "600",
    assigned_number_4_octets                           = "700",
    Cbit                                               = "1",
    nextHop                                            = "13.14.15.17",
    enable_trafficMarking                              = "1",
    dscp                                               = "20",
    fsv6_enable_redirectIPv6                           = "1",
    fsv6_redirectIPv6                                  = "1:1:0a:0b:0c:0d:0e:1",
    enable_next_hop                                    = "1",
    set_next_hop                                       = "manually",
    set_next_hop_ip_type                               = "ipv6",
    ipv4_next_hop                                      = "11.11.11.11",
    ipv6_next_hop                                      = "c:0:0:0:0:0:0:d",
    enable_origin                                      = "1",
    origin                                             = "igp",
    enable_local_preference                            = "1",
    local_preference                                   = "200",
    enable_multi_exit_discriminator                    = "1",
    multi_exit_discriminator                           = "400",
    enable_atomic_aggregate                            = "1",
    enable_aggregator_id                               = "1",
    aggregator_id                                      = "3.3.3.3",
    aggregator_as                                      = "300",
    enable_originator_id                               = "1",
    originator_id                                      = "7.7.7.7",
    enable_community                                   = "1",
    number_of_communities                              = "1",
    community_type                                     = ["no_export"],
    community_as_number                                = ["321"],
    community_last_two_octets                          = ["432"],
    enable_ext_community                               = "1",
    number_of_ext_communities                          = "1",
    ext_communities_type                               = ["admin_as_two_octet"],
    ext_communities_subtype                            = ["route_target"],
    ext_community_as_number                            = ["1"],
    ext_community_target_assigned_number_4_octets      = ["1"],
    ext_community_ip                                   = ["1.1.1.1"],
    ext_community_as_4_bytes                           = ["1"],
    ext_community_target_assigned_number_2_octets      = ["1"],
    ext_community_opaque_data                          = ["bb"],
    ext_community_colorCObits                          = ["00"],
    ext_community_colorReservedBits                    = ["214"],
    ext_community_colorValue                           = ["567"],
    ext_community_linkBandwidth                        = ["2000"],
    enable_override_peer_as_set_mode                   = "1",
    as_path_set_mode                                   = "include_as_seq",
    enable_as_path_segments                            = "1",
    no_of_as_path_segments                             = "1",
    enable_as_path_segment                             = ["1"],
    as_path_segment_type                               = ["as_set"],
    number_of_as_number_in_segment                     = ["1"],
    as_path_segment_enable_as_number                   = ["1"],
    as_path_segment_as_number                          = ["200"],
    enable_cluster                                     = "1",
    no_of_clusters                                     = "1",
    cluster_id                                         = ["55.66.77.89"],
)
if bgpFlowSpecRangeList_v6_interface_2_status['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('emulation_bgp_flow_spec_config', bgpFlowSpecRangeList_v6_interface_2_status)
############################################################################
# Start BGP6 protocol                                                       #
############################################################################    
print("Waiting 5 seconds before starting protocol(s) ...")
time.sleep(5)
_result_ = ixiangpf.test_control(action='start_all_protocols')
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', _result_)
     

print("Waiting for 60 seconds")
time.sleep(60)

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
print("Fetching BGP aggregated statistics")               
protostats = ixiangpf.emulation_bgp_info(\
    handle = bgpInterface_1_handle,
    mode   = 'stats_per_device_group')

if protostats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_bgp_info', protostats)

pprint(protostats)

############################################################################
# Retrieve Learned Info                                                    #
############################################################################
print("Fetching BGP Learned Info")
learned_info = ixiangpf.emulation_bgp_info(\
    handle = bgpInterface_1_handle,
    mode   = 'learned_info');

if learned_info['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_bgp_info', learned_info)
    
pprint(learned_info)

############################################################################
# Stop all protocols                                                       #
############################################################################
print("Stopping all protocols")
_result_ = ixiangpf.test_control(action='stop_all_protocols')
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', _result_)
    
time.sleep(2)                  
print("!!! Test Script Ends !!!")
