#!/usr/bin/tclsh
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
#    than it will retrieve and display few statistics and Modify the Flow-Spec #
#    fileds.                                                                   #
#                                                                              #
################################################################################

################################################################################
# Utilities                                                                    #
################################################################################
if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

# End Utilities ################################################################

################################################################################
# Connection to the chassis, IxNetwork Tcl Server                    	       #
################################################################################

set chassis_ip        {10.39.50.122}
set tcl_server        10.39.43.12
set port_list         {1/7 1/8}
set ixNetwork_client  "10.39.43.12:8009"
set test_name         [info script]

# Connecting to chassis and client
puts "Connecting to chassis and client..."
set connect_status [::ixiangpf::connect       \
    -reset                   1                \
    -device                  $chassis_ip      \
    -port_list               $port_list       \
    -ixnetwork_tcl_server    $ixNetwork_client\
    -tcl_server              $tcl_server      \
]

if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}
puts "End connecting to chassis ..."

# Retrieving port handles, for later use
set port1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]

################################################################################
# Creating topology and device group                                           #
################################################################################

# Creating a topology on first port
puts "Adding topology 1 on port 1" 
set topology_1_status [::ixiangpf::topology_config\
    -topology_name      {BGP6 Topology 1}          \
    -port_handle        $port1                    \
]
if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_1_status log]"
    return 0
}
set topology_1_handle [keylget topology_1_status topology_handle]

# Creating a device group in topology 
puts "Creating device group 1 in topology 1"    
set device_group_1_status [::ixiangpf::topology_config    \
    -topology_handle              $topology_1_handle      \
    -device_group_name            {BGP6 Topology 1 Router} \
    -device_group_multiplier      1                       \
    -device_group_enabled         1                       \
]

if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_1_status log]"
    return 0
}
set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

# Creating a topology on second port
puts "Adding topology 2 on port 2"
set topology_2_status [::ixiangpf::topology_config \
    -topology_name      {BGP6 Topology 2}           \
    -port_handle        $port2                     \
]
if {[keylget topology_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_2_status log]"
    return 0
}
set topology_2_handle [keylget topology_2_status topology_handle]

# Creating a device group in topology
puts "Creating device group 2 in topology 2"
set device_group_2_status [::ixiangpf::topology_config \
    -topology_handle              $topology_2_handle   \
    -device_group_name            {BGP6 Topology 2 Router} \
    -device_group_multiplier      1                    \
    -device_group_enabled         1                    \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_2_status log]"
    return 0
}
set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]

################################################################################
#  Configure protocol interfaces                                               #
################################################################################

# Creating ethernet stack for the first Device Group 
puts "Creating ethernet stack for the first Device Group"
set ethernet_1_status [::ixiangpf::interface_config          \
    -protocol_name                {Ethernet 1}               \
    -protocol_handle              $deviceGroup_1_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 18.03.73.c7.6c.b1          \
    -src_mac_addr_step            00.00.00.00.00.00          \
]
if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_1_status log]"
    return 0
}
set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]

# Creating ethernet stack for the second Device Group
puts "Creating ethernet for the second Device Group"
set ethernet_2_status [::ixiangpf::interface_config          \
    -protocol_name                {Ethernet 2}               \
    -protocol_handle              $deviceGroup_2_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 18.03.73.c7.6c.01          \
    -src_mac_addr_step            00.00.00.00.00.00          \
]
if {[keylget ethernet_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_2_status log]"
    return 0
}
set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]

# Creating IPv6 Stack on top of Ethernet Stack for the first Device Group                                 
puts "Creating IPv6 Stack on top of Ethernet Stack for the first Device Group"
set ipv6_1_status [::ixiangpf::interface_config \
    -protocol_name                     {IPv6 1}                \
    -protocol_handle                   $ethernet_1_handle      \
    -ipv6_multiplier                   1                       \
    -ipv6_resolve_gateway              1                       \
    -ipv6_manual_gateway_mac           00.00.00.00.00.01       \
    -ipv6_manual_gateway_mac_step      00.00.00.00.00.00       \
    -ipv6_gateway                      2000:0:0:1:0:0:0:1      \
    -ipv6_gateway_step                 ::0                     \
    -ipv6_intf_addr                    2000:0:0:1:0:0:0:2      \
    -ipv6_intf_addr_step               ::0                     \
    -ipv6_prefix_length                64                      \
    ]
if {[keylget ipv6_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv6_1_status log]"
    return 0
}
set ipv6_1_handle [keylget ipv6_1_status ipv6_handle]

# Creating IPv6 Stack on top of Ethernet Stack for the second Device Group 
puts "Creating IPv6 2 stack on ethernet 2 stack for the second Device Group"
set ipv6_2_status [::ixiangpf::interface_config \
    -protocol_name                     {IPv6 2}                \
    -protocol_handle                   $ethernet_2_handle      \
    -ipv6_multiplier                   1                       \
    -ipv6_resolve_gateway              1                       \
    -ipv6_manual_gateway_mac           00.00.00.00.00.01       \
    -ipv6_manual_gateway_mac_step      00.00.00.00.00.00       \
    -ipv6_gateway                      2000:0:0:1:0:0:0:2      \
    -ipv6_gateway_step                 ::0                     \
    -ipv6_intf_addr                    2000:0:0:1:0:0:0:1      \
    -ipv6_intf_addr_step               ::0                     \
    -ipv6_prefix_length                64                      \
]
if {[keylget ipv6_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv6_2_status log]"
    return 0
}
set ipv6_2_handle [keylget ipv6_2_status ipv6_handle]


################################################################################
# Other protocol configurations                                                # 
################################################################################

# This will Create BGP6 Stack on top of IPv6 Stack of Topology1 & Topology2

puts "Creating BGP6 Stack on top of IPv6 stack on Topology 1 !!!!!!!!!!"
set bgp_v6_interface_1_status [::ixiangpf::emulation_bgp_config \
    -mode                                         enable                                        \
    -active                                       1                                             \
    -md5_enable                                   0                                             \
    -md5_key                                      Ixia                                          \
    -handle                                       $ipv6_1_handle                                \
    -ip_version                                   6                                             \
    -remote_ipv6_addr                             2000:0:0:1:0:0:0:1                            \
    -next_hop_enable                              0                                             \
    -next_hop_ip                                  0.0.0.0                                       \
    -enable_4_byte_as                             0                                             \
    -local_as                                     0                                             \
    -local_as4                                    0                                             \
    -update_interval                              0                                             \
    -count                                        1                                             \
    -local_router_id                              192.0.0.1                                     \
    -local_router_id_step                         0.0.0.0                                       \
    -hold_time                                    90                                            \
    -neighbor_type                                internal                                      \
    -graceful_restart_enable                      0                                             \
    -restart_time                                 45                                            \
    -stale_time                                   0                                             \
    -tcp_window_size                              8192                                          \
    -local_router_id_enable                       1                                             \
    -ipv4_capability_mdt_nlri                     0                                             \
    -ipv4_capability_unicast_nlri                 1                                             \
    -ipv4_filter_unicast_nlri                     1                                             \
    -ipv4_capability_multicast_nlri               1                                             \
    -ipv4_filter_multicast_nlri                   0                                             \
    -ipv4_capability_mpls_nlri                    1                                             \
    -ipv4_filter_mpls_nlri                        0                                             \
    -ipv4_capability_mpls_vpn_nlri                1                                             \
    -ipv4_filter_mpls_vpn_nlri                    0                                             \
    -ipv6_capability_unicast_nlri                 1                                             \
    -ipv6_filter_unicast_nlri                     1                                             \
    -ipv6_capability_multicast_nlri               1                                             \
    -ipv6_filter_multicast_nlri                   0                                             \
    -ipv6_capability_mpls_nlri                    1                                             \
    -ipv6_filter_mpls_nlri                        0                                             \
    -ipv6_capability_mpls_vpn_nlri                1                                             \
    -ipv6_filter_mpls_vpn_nlri                    0                                             \
    -capability_route_refresh                     1                                             \
    -capability_route_constraint                  0                                             \
    -ttl_value                                    64                                            \
    -updates_per_iteration                        1                                             \
    -bfd_registration                             0                                             \
    -bfd_registration_mode                        multi_hop                                     \
    -vpls_capability_nlri                         1                                             \
    -vpls_filter_nlri                             0                                             \
    -act_as_restarted                             0                                             \
    -discard_ixia_generated_routes                0                                             \
    -flap_down_time                               0                                             \
    -local_router_id_type                         same                                          \
    -enable_flap                                  0                                             \
    -send_ixia_signature_with_routes              0                                             \
    -flap_up_time                                 0                                             \
    -ipv4_capability_multicast_vpn_nlri           0                                             \
    -ipv4_filter_multicast_vpn_nlri               0                                             \
    -ipv6_capability_multicast_vpn_nlri           0                                             \
    -ipv6_filter_multicast_vpn_nlri               0                                             \
    -advertise_end_of_rib                         0                                             \
    -configure_keepalive_timer                    0                                             \
    -keepalive_timer                              30                                            \
    -as_path_set_mode                             no_include                                    \
    -router_id                                    192.0.0.1                                     \
    -filter_link_state                            0                                             \
    -capability_linkstate_nonvpn                  0                                             \
    -bgp_ls_id                                    0                                             \
    -instance_id                                  0                                             \
    -number_of_communities                        1                                             \
    -enable_community                             0                                             \
    -number_of_ext_communities                    1                                             \
    -enable_ext_community                         0                                             \
    -enable_override_peer_as_set_mode             0                                             \
    -bgp_ls_as_set_mode                           include_as_seq                                \
    -number_of_as_path_segments                   1                                             \
    -enable_as_path_segments                      1                                             \
    -number_of_clusters                           1                                             \
    -enable_cluster                               0                                             \
    -ethernet_segments_count                      0                                             \
    -filter_evpn                                  0                                             \
    -evpn                                         0                                             \
    -operational_model                            symmetric                                     \
    -routers_mac_or_irb_mac_address               00:01:03:00:00:01                             \
    -capability_ipv4_unicast_add_path             0                                             \
    -capability_ipv6_unicast_add_path             0                                             \
    -ipv4_mpls_add_path_mode                      both                                          \
    -ipv6_mpls_add_path_mode                      both                                          \
    -ipv4_unicast_add_path_mode                   both                                          \
    -ipv6_unicast_add_path_mode                   both                                          \
    -ipv4_mpls_capability                         0                                             \
    -ipv6_mpls_capability                         0                                             \
    -capability_ipv4_mpls_add_path                0                                             \
    -capability_ipv6_mpls_add_path                0                                             \
    -custom_sid_type                              40                                            \
    -srgb_count                                   1                                             \
    -start_sid                                    16000                                         \
    -sid_count                                    8000                                          \
    -ipv4_multiple_mpls_labels_capability         0                                             \
    -ipv6_multiple_mpls_labels_capability         0                                             \
    -mpls_labels_count_for_ipv4_mpls_route        1                                             \
    -mpls_labels_count_for_ipv6_mpls_route        1                                             \
    -noOfUserDefinedAfiSafi                       0                                             \
    -capability_ipv4_unicast_flowSpec             1                                             \
    -filter_ipv4_unicast_flowSpec                 1                                             \
    -capability_ipv6_unicast_flowSpec             1                                             \
    -filter_ipv6_unicast_flowSpec                 1                                             \
    -always_include_tunnel_enc_ext_community      false                                         \
    -ip_vrf_to_ip_vrf_type                        interfacefullWithUnnumberedCorefacingIRB      \
    -irb_interface_label                          16                                            \
    -irb_ipv6_address                             10:0:0:0:0:0:0:1                              \
    ]
if {[keylget bgp_v6_interface_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_v6_interface_1_status log]"
    return 0
}

set bgp_v6_Interface_1_handle [keylget bgp_v6_interface_1_status bgp_handle]

puts "Enabling BGP6 FLOW-Spec and with configure Flow-spec on top BGP6 Stack of Topology1 !!!!!!!"
set bgp_flow_spec_ranges_list_v6_1_status [::ixiangpf::emulation_bgp_flow_spec_config \
    -mode                                               enable                     \
    -fs_mode                                            fsv6                       \
    -handle                                             $bgp_v6_Interface_1_handle      \
    -no_of_flowSpecRangeV6                              1                          \
    -active                                             1                          \
    -flowSpecName                                       {BGP Flow Spec 11-1}       \
    -fsv6_enableDestPrefix                              1                          \
    -fsv6_destPrefix                                    1:0:0:0:0:0:1:1            \
    -fsv6_destPrefixLength                              64                         \
    -fsv6_destPrefixOffset                              34                         \
    -fsv6_enableSrcPrefix                               1                          \
    -fsv6_srcPrefix                                     1:1:0:0:0:0:0:1            \
    -fsv6_srcPrefixLength                               80                         \
    -fsv6_srcPrefixOffset                               48                         \
    -fsv6_nextHeader                                    120                        \
    -portMatch                                          10                         \
    -destPortMatch                                      40                         \
    -srcPortMatch                                       50                         \
    -icmpTypeMatch                                      80                         \
    -icmpCodeMatch                                      90                         \
    -tcpFlagsMatch                                      (cwr)                      \
    -ipPacketMatch                                      110                        \
    -dscpMatch                                          10                         \
    -fsv6_fragmentMatch                                 (lf)                       \
    -fsv6_flowLabel                                     40                         \
    -enable_traffic_rate                                1                          \
    -trafficRate                                        1000                       \
    -enable_trafficAction                               1                          \
    -terminalAction                                     1                          \
    -trafficActionSample                                1                          \
    -enable_redirect                                    1                          \
    -redirect_ext_communities_type                      rdIPv4                     \
    -as_2_bytes                                         100                        \
    -as_4_bytes                                         400                        \
    -fsv6_ipv6                                          1:1:0:0:0:0:0:1            \
    -assigned_number_2_octets                           500                        \
    -assigned_number_4_octets                           800                        \
    -Cbit                                               1                          \
    -nextHop                                            1.1.1.1                    \
    -enable_trafficMarking                              1                          \
    -dscp                                               10                         \
    -fsv6_enable_redirectIPv6                           1                          \
    -fsv6_redirectIPv6                                  1:1:0:0:0:0:0:1            \
    -enable_next_hop                                    1                          \
    -set_next_hop                                       sameaslocalip              \
    -set_next_hop_ip_type                               ipv4                       \
    -ipv4_next_hop                                      10.10.10.10                \
    -ipv6_next_hop                                      a:0:0:0:0:0:0:b            \
    -enable_origin                                      1                          \
    -origin                                             igp                        \
    -enable_local_preference                            1                          \
    -local_preference                                   100                        \
    -enable_multi_exit_discriminator                    1                          \
    -multi_exit_discriminator                           300                        \
    -enable_atomic_aggregate                            1                          \
    -enable_aggregator_id                               1                          \
    -aggregator_id                                      2.2.2.2                    \
    -aggregator_as                                      200                        \
    -enable_originator_id                               1                          \
    -originator_id                                      6.6.6.6                    \
    -enable_community                                   1                          \
    -number_of_communities                              1                          \
    -community_type                                     no_export                  \
    -community_as_number                                123                        \
    -community_last_two_octets                          234                        \
    -enable_ext_community                               1                          \
    -number_of_ext_communities                          1                          \
    -ext_communities_type                               admin_as_two_octet         \
    -ext_communities_subtype                            route_target               \
    -ext_community_as_number                            123                        \
    -ext_community_target_assigned_number_4_octets      1                          \
    -ext_community_ip                                   1.1.1.1                    \
    -ext_community_as_4_bytes                           1                          \
    -ext_community_target_assigned_number_2_octets      1                          \
    -ext_community_opaque_data                          aa                         \
    -ext_community_colorCObits                          00                         \
    -ext_community_colorReservedBits                    123                        \
    -ext_community_colorValue                           1234                       \
    -ext_community_linkBandwidth                        1000                       \
    -enable_override_peer_as_set_mode                   1                          \
    -as_path_set_mode                                   include_as_seq             \
    -enable_as_path_segments                            1                          \
    -no_of_as_path_segments                             1                          \
    -enable_as_path_segment                             1                          \
    -as_path_segment_type                               as_set                     \
    -number_of_as_number_in_segment                     1                          \
    -as_path_segment_enable_as_number                   1                          \
    -as_path_segment_as_number                          100                        \
    -enable_cluster                                     1                          \
    -no_of_clusters                                     1                          \
    -cluster_id                                         1.2.3.4                    \
]
if {[keylget bgp_flow_spec_ranges_list_v6_1_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $bgp_flow_spec_ranges_list_v6_1_status
}
set bgpFlowSpecRangesListV6_1_handle [keylget bgp_flow_spec_ranges_list_v6_1_status bgp_flowSpecV6_handle]

puts "Creating BGP6 Stack on top of IPv6 stack on Topology2 !!!!!!!!!!"
set bgp_v6_interface_2_status [::ixiangpf::emulation_bgp_config \
    -mode                                         enable                                        \
    -active                                       1                                             \
    -md5_enable                                   0                                             \
    -md5_key                                      Ixia                                          \
    -handle                                       $ipv6_2_handle                                \
    -ip_version                                   6                                             \
    -remote_ipv6_addr                             2000:0:0:1:0:0:0:2                            \
    -next_hop_enable                              0                                             \
    -next_hop_ip                                  0.0.0.0                                       \
    -enable_4_byte_as                             0                                             \
    -local_as                                     0                                             \
    -local_as4                                    0                                             \
    -update_interval                              0                                             \
    -count                                        1                                             \
    -local_router_id                              193.0.0.1                                     \
    -local_router_id_step                         0.0.0.0                                       \
    -hold_time                                    90                                            \
    -neighbor_type                                internal                                      \
    -graceful_restart_enable                      0                                             \
    -restart_time                                 45                                            \
    -stale_time                                   0                                             \
    -tcp_window_size                              8192                                          \
    -local_router_id_enable                       1                                             \
    -ipv4_capability_mdt_nlri                     0                                             \
    -ipv4_capability_unicast_nlri                 1                                             \
    -ipv4_filter_unicast_nlri                     1                                             \
    -ipv4_capability_multicast_nlri               1                                             \
    -ipv4_filter_multicast_nlri                   0                                             \
    -ipv4_capability_mpls_nlri                    1                                             \
    -ipv4_filter_mpls_nlri                        0                                             \
    -ipv4_capability_mpls_vpn_nlri                1                                             \
    -ipv4_filter_mpls_vpn_nlri                    0                                             \
    -ipv6_capability_unicast_nlri                 1                                             \
    -ipv6_filter_unicast_nlri                     1                                             \
    -ipv6_capability_multicast_nlri               1                                             \
    -ipv6_filter_multicast_nlri                   0                                             \
    -ipv6_capability_mpls_nlri                    1                                             \
    -ipv6_filter_mpls_nlri                        0                                             \
    -ipv6_capability_mpls_vpn_nlri                1                                             \
    -ipv6_filter_mpls_vpn_nlri                    0                                             \
    -capability_route_refresh                     1                                             \
    -capability_route_constraint                  0                                             \
    -ttl_value                                    64                                            \
    -updates_per_iteration                        1                                             \
    -bfd_registration                             0                                             \
    -bfd_registration_mode                        multi_hop                                     \
    -vpls_capability_nlri                         1                                             \
    -vpls_filter_nlri                             0                                             \
    -act_as_restarted                             0                                             \
    -discard_ixia_generated_routes                0                                             \
    -flap_down_time                               0                                             \
    -local_router_id_type                         same                                          \
    -enable_flap                                  0                                             \
    -send_ixia_signature_with_routes              0                                             \
    -flap_up_time                                 0                                             \
    -ipv4_capability_multicast_vpn_nlri           0                                             \
    -ipv4_filter_multicast_vpn_nlri               0                                             \
    -ipv6_capability_multicast_vpn_nlri           0                                             \
    -ipv6_filter_multicast_vpn_nlri               0                                             \
    -advertise_end_of_rib                         0                                             \
    -configure_keepalive_timer                    0                                             \
    -keepalive_timer                              30                                            \
    -as_path_set_mode                             no_include                                    \
    -router_id                                    193.0.0.1                                     \
    -filter_link_state                            0                                             \
    -capability_linkstate_nonvpn                  0                                             \
    -bgp_ls_id                                    0                                             \
    -instance_id                                  0                                             \
    -number_of_communities                        1                                             \
    -enable_community                             0                                             \
    -number_of_ext_communities                    1                                             \
    -enable_ext_community                         0                                             \
    -enable_override_peer_as_set_mode             0                                             \
    -bgp_ls_as_set_mode                           include_as_seq                                \
    -number_of_as_path_segments                   1                                             \
    -enable_as_path_segments                      1                                             \
    -number_of_clusters                           1                                             \
    -enable_cluster                               0                                             \
    -ethernet_segments_count                      0                                             \
    -filter_evpn                                  0                                             \
    -evpn                                         0                                             \
    -operational_model                            symmetric                                     \
    -routers_mac_or_irb_mac_address               00:01:04:00:00:01                             \
    -capability_ipv4_unicast_add_path             0                                             \
    -capability_ipv6_unicast_add_path             0                                             \
    -ipv4_mpls_add_path_mode                      both                                          \
    -ipv6_mpls_add_path_mode                      both                                          \
    -ipv4_unicast_add_path_mode                   both                                          \
    -ipv6_unicast_add_path_mode                   both                                          \
    -ipv4_mpls_capability                         0                                             \
    -ipv6_mpls_capability                         0                                             \
    -capability_ipv4_mpls_add_path                0                                             \
    -capability_ipv6_mpls_add_path                0                                             \
    -custom_sid_type                              40                                            \
    -srgb_count                                   1                                             \
    -start_sid                                    16000                                         \
    -sid_count                                    8000                                          \
    -ipv4_multiple_mpls_labels_capability         0                                             \
    -ipv6_multiple_mpls_labels_capability         0                                             \
    -mpls_labels_count_for_ipv4_mpls_route        1                                             \
    -mpls_labels_count_for_ipv6_mpls_route        1                                             \
    -noOfUserDefinedAfiSafi                       0                                             \
    -capability_ipv4_unicast_flowSpec             1                                             \
    -filter_ipv4_unicast_flowSpec                 1                                             \
    -capability_ipv6_unicast_flowSpec             1                                             \
    -filter_ipv6_unicast_flowSpec                 1                                             \
    -always_include_tunnel_enc_ext_community      false                                         \
    -ip_vrf_to_ip_vrf_type                        interfacefullWithUnnumberedCorefacingIRB      \
    -irb_interface_label                          16                                            \
    -irb_ipv6_address                             10:0:0:0:0:0:0:1                              \
]

if {[keylget bgp_v6_interface_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_v6_interface_2_status log]"
    return 0
}

set bgp_v6_Interface_2_handle [keylget bgp_v6_interface_2_status bgp_handle]

puts "Enabling BGP6 FLOW-Spec and with configure Flow-spec on top BGP6 Stack of Topology2 !!!!!!!"
set bgp_flow_spec_ranges_list_v6_2_status [::ixiangpf::emulation_bgp_flow_spec_config \
    -mode                                               enable                     \
    -fs_mode                                            fsv6                       \
    -handle                                             $bgp_v6_Interface_2_handle      \
    -no_of_flowSpecRangeV6                              1                          \
    -active                                             1                          \
    -flowSpecName                                       {BGP Flow Spec 11-1}       \
    -fsv6_enableDestPrefix                              1                          \
    -fsv6_destPrefix                                    1:0:0:0:0:0:1:1            \
    -fsv6_destPrefixLength                              64                         \
    -fsv6_destPrefixOffset                              34                         \
    -fsv6_enableSrcPrefix                               1                          \
    -fsv6_srcPrefix                                     1:1:0:0:0:0:0:1            \
    -fsv6_srcPrefixLength                               96                         \
    -fsv6_srcPrefixOffset                               64                         \
    -fsv6_nextHeader                                    120                        \
    -portMatch                                          20                         \
    -destPortMatch                                      30                         \
    -srcPortMatch                                       60                         \
    -icmpTypeMatch                                      70                         \
    -icmpCodeMatch                                      100                        \
    -tcpFlagsMatch                                      (fin)                      \
    -ipPacketMatch                                      120                        \
    -dscpMatch                                          20                         \
    -fsv6_fragmentMatch                                 (ff)                       \
    -fsv6_flowLabel                                     30                         \
    -enable_traffic_rate                                1                          \
    -trafficRate                                        2000                       \
    -enable_trafficAction                               1                          \
    -terminalAction                                     1                          \
    -trafficActionSample                                1                          \
    -enable_redirect                                    1                          \
    -redirect_ext_communities_type                      rdIPv4                     \
    -as_2_bytes                                         200                        \
    -as_4_bytes                                         300                        \
    -fsv6_ipv6                                          1:1:0:0:0:0:0:1            \
    -assigned_number_2_octets                           600                        \
    -assigned_number_4_octets                           700                        \
    -Cbit                                               1                          \
    -nextHop                                            1.1.1.1                    \
    -enable_trafficMarking                              1                          \
    -dscp                                               20                         \
    -fsv6_enable_redirectIPv6                           1                          \
    -fsv6_redirectIPv6                                  1:1:0:0:0:0:0:1            \
    -enable_next_hop                                    1                          \
    -set_next_hop                                       manually                   \
    -set_next_hop_ip_type                               ipv6                       \
    -ipv4_next_hop                                      11.11.11.11                \
    -ipv6_next_hop                                      c:0:0:0:0:0:0:d            \
    -enable_origin                                      1                          \
    -origin                                             igp                        \
    -enable_local_preference                            1                          \
    -local_preference                                   200                        \
    -enable_multi_exit_discriminator                    1                          \
    -multi_exit_discriminator                           400                        \
    -enable_atomic_aggregate                            1                          \
    -enable_aggregator_id                               1                          \
    -aggregator_id                                      3.3.3.3                    \
    -aggregator_as                                      300                        \
    -enable_originator_id                               1                          \
    -originator_id                                      7.7.7.7                    \
    -enable_community                                   1                          \
    -number_of_communities                              1                          \
    -community_type                                     no_export                  \
    -community_as_number                                321                        \
    -community_last_two_octets                          432                        \
    -enable_ext_community                               1                          \
    -number_of_ext_communities                          1                          \
    -ext_communities_type                               admin_as_two_octet         \
    -ext_communities_subtype                            route_target               \
    -ext_community_as_number                            1                          \
    -ext_community_target_assigned_number_4_octets      1                          \
    -ext_community_ip                                   1.1.1.1                    \
    -ext_community_as_4_bytes                           1                          \
    -ext_community_target_assigned_number_2_octets      1                          \
    -ext_community_opaque_data                          bb                         \
    -ext_community_colorCObits                          00                         \
    -ext_community_colorReservedBits                    214                        \
    -ext_community_colorValue                           567                        \
    -ext_community_linkBandwidth                        2000                       \
    -enable_override_peer_as_set_mode                   1                          \
    -as_path_set_mode                                   include_as_seq             \
    -enable_as_path_segments                            1                          \
    -no_of_as_path_segments                             1                          \
    -enable_as_path_segment                             1                          \
    -as_path_segment_type                               as_set                     \
    -number_of_as_number_in_segment                     1                          \
    -as_path_segment_enable_as_number                   1                          \
    -as_path_segment_as_number                          200                        \
    -enable_cluster                                     1                          \
    -no_of_clusters                                     1                          \
    -cluster_id                                         5.6.7.8                    \
]

if {[keylget bgp_flow_spec_ranges_list_v6_2_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $bgp_flow_spec_ranges_list_v6_2_status
}
set bgpFlowSpecRangesListV6_2_handle [keylget bgp_flow_spec_ranges_list_v6_2_status bgp_flowSpecV6_handle]

puts "After 5 secs Modify the value of Flow-Spec fields of BGP6 IPv6 Flow SPec Range of BGP PEER1"
after 5000

puts "Modify the value of Flow-Spec fields of BGP6 IPv6 FLOW SPEC RANGE of BGP PEER1"
set bgp_flow_spec_ranges_list_v6_1_status [::ixiangpf::emulation_bgp_flow_spec_config \
    -mode                                               enable                     \
    -fs_mode                                            fsv6                       \
    -handle                                             $bgpFlowSpecRangesListV6_1_handle      \
    -no_of_flowSpecRangeV6                              1                          \
    -active                                             1                          \
    -flowSpecName                                       {BGP Flow Spec 11-1}       \
    -fsv6_enableDestPrefix                              1                          \
    -fsv6_destPrefix                                    10:a:a:b:c:d:1a:1b            \
    -fsv6_destPrefixLength                              84                         \
    -fsv6_destPrefixOffset                              64                         \
    -fsv6_enableSrcPrefix                               1                          \
    -fsv6_srcPrefix                                     a1:b1:c:d:e:f:23:1            \
    -fsv6_srcPrefixLength                               100                         \
    -fsv6_srcPrefixOffset                               84                         \
    -fsv6_nextHeader                                    150                        \
    -portMatch                                          20                         \
    -destPortMatch                                      400                         \
    -srcPortMatch                                       500                         \
    -icmpTypeMatch                                      100                         \
    -icmpCodeMatch                                      100                         \
    -tcpFlagsMatch                                      (syn)                      \
    -ipPacketMatch                                      1010                        \
    -dscpMatch                                          20                         \
    -fsv6_fragmentMatch                                 (ff)                       \
    -fsv6_flowLabel                                     50                         \
    -enable_traffic_rate                                1                          \
    -trafficRate                                        5000                       \
    -enable_trafficAction                               1                          \
    -terminalAction                                     1                          \
    -trafficActionSample                                1                          \
    -enable_redirect                                    1                          \
    -redirect_ext_communities_type                      rdIPv4                     \
    -as_2_bytes                                         1000                        \
    -as_4_bytes                                         4000                        \
    -fsv6_ipv6                                          15:16:70:80:90:10:70:81            \
    -assigned_number_2_octets                           5000                        \
    -assigned_number_4_octets                           5800                        \
    -Cbit                                               1                          \
    -nextHop                                            15.15.15.15                    \
    -enable_trafficMarking                              1                          \
    -dscp                                               20                         \
    -fsv6_enable_redirectIPv6                           1                          \
    -fsv6_redirectIPv6                                  1a:1b:0c:d01:e05:067:078:ab1            \
    -enable_next_hop                                    1                          \
    -set_next_hop                                       sameaslocalip              \
    -set_next_hop_ip_type                               ipv4                       \
    -ipv4_next_hop                                      150.105.150.105                \
    -ipv6_next_hop                                      a:c:0:d:0:e:0:b            \
    -enable_origin                                      1                          \
    -origin                                             igp                        \
    -enable_local_preference                            1                          \
    -local_preference                                   1000                        \
    -enable_multi_exit_discriminator                    1                          \
    -multi_exit_discriminator                           3000                        \
    -enable_atomic_aggregate                            1                          \
    -enable_aggregator_id                               1                          \
    -aggregator_id                                      25.25.25.25                    \
    -aggregator_as                                      205                        \
    -enable_originator_id                               1                          \
    -originator_id                                      69.69.69.69                    \
    -enable_community                                   1                          \
    -number_of_communities                              1                          \
    -community_type                                     no_export                  \
    -community_as_number                                123                        \
    -community_last_two_octets                          234                        \
    -enable_ext_community                               1                          \
    -number_of_ext_communities                          1                          \
    -ext_communities_type                               admin_as_two_octet         \
    -ext_communities_subtype                            route_target               \
    -ext_community_as_number                            1203                        \
    -ext_community_target_assigned_number_4_octets      1                          \
    -ext_community_ip                                   17.17.17.17                    \
    -ext_community_as_4_bytes                           198                          \
    -ext_community_target_assigned_number_2_octets      189                          \
    -ext_community_opaque_data                          ef                         \
    -ext_community_colorCObits                          11                         \
    -ext_community_colorReservedBits                    1203                        \
    -ext_community_colorValue                           124                       \
    -ext_community_linkBandwidth                        9000                       \
    -enable_override_peer_as_set_mode                   1                          \
    -as_path_set_mode                                   include_as_seq             \
    -enable_as_path_segments                            1                          \
    -no_of_as_path_segments                             1                          \
    -enable_as_path_segment                             1                          \
    -as_path_segment_type                               as_set                     \
    -number_of_as_number_in_segment                     1                          \
    -as_path_segment_enable_as_number                   1                          \
    -as_path_segment_as_number                          1500                        \
    -enable_cluster                                     1                          \
    -no_of_clusters                                     1                          \
    -cluster_id                                         19.29.39.49                    \
]

if {[keylget bgp_flow_spec_ranges_list_v6_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_flow_spec_ranges_list_v6_1_status log]"
    return 0
}
puts "After 5 secs Modify the value of Flow-Spec fields of BGP6 IPv6 Flow SPec Range of BGP6 PEER2!!!"
after 5000

puts "Modify the value of Flow-Spec fields of BGP6 IPv6 FLOW SPEC RANGE of BGP6 PEER2!!!!!!!!!!!!!!"
set bgp_flow_spec_ranges_list_v6_2_status [::ixiangpf::emulation_bgp_flow_spec_config \
    -mode                                               enable                     \
    -fs_mode                                            fsv6                       \
    -handle                                             $bgp_v6_Interface_2_handle      \
    -no_of_flowSpecRangeV6                              1                          \
    -active                                             1                          \
    -flowSpecName                                       {BGP Flow Spec 11-1}       \
    -fsv6_enableDestPrefix                              1                          \
    -fsv6_destPrefix                                    1a:20:30:40:50:60:a1:b1            \
    -fsv6_destPrefixLength                              64                         \
    -fsv6_destPrefixOffset                              34                         \
    -fsv6_enableSrcPrefix                               1                          \
    -fsv6_srcPrefix                                     1a:1b:0c:0e:0d:0f:0:a1            \
    -fsv6_srcPrefixLength                               96                         \
    -fsv6_srcPrefixOffset                               64                         \
    -fsv6_nextHeader                                    120                        \
    -portMatch                                          200                         \
    -destPortMatch                                      330                         \
    -srcPortMatch                                       460                         \
    -icmpTypeMatch                                      255                         \
    -icmpCodeMatch                                      200                        \
    -tcpFlagsMatch                                      (syn)                      \
    -ipPacketMatch                                      120                        \
    -dscpMatch                                          15                         \
    -fsv6_fragmentMatch                                 (lf)                       \
    -fsv6_flowLabel                                     30                         \
    -enable_traffic_rate                                1                          \
    -trafficRate                                        2000                       \
    -enable_trafficAction                               1                          \
    -terminalAction                                     1                          \
    -trafficActionSample                                1                          \
    -enable_redirect                                    1                          \
    -redirect_ext_communities_type                      rdIPv4                     \
    -as_2_bytes                                         234                        \
    -as_4_bytes                                         321                        \
    -fsv6_ipv6                                          1a:1b:0c:0d:0e:0f:05:1            \
    -assigned_number_2_octets                           656                        \
    -assigned_number_4_octets                           734                        \
    -Cbit                                               1                          \
    -nextHop                                            15.16.17.18                    \
    -enable_trafficMarking                              1                          \
    -dscp                                               15                         \
    -fsv6_enable_redirectIPv6                           1                          \
    -fsv6_redirectIPv6                                  1a:1b:0c:0d:0e:0f:01:1            \
    -enable_next_hop                                    1                          \
    -set_next_hop                                       manually                   \
    -set_next_hop_ip_type                               ipv6                       \
    -ipv4_next_hop                                      11.11.11.11                \
    -ipv6_next_hop                                      c:a0:e0:f0:b0:c0:120:d            \
    -enable_origin                                      1                          \
    -origin                                             igp                        \
    -enable_local_preference                            1                          \
    -local_preference                                   256                        \
    -enable_multi_exit_discriminator                    1                          \
    -multi_exit_discriminator                           478                        \
    -enable_atomic_aggregate                            1                          \
    -enable_aggregator_id                               1                          \
    -aggregator_id                                      34.35.36.37                    \
    -aggregator_as                                      365                        \
    -enable_originator_id                               1                          \
    -originator_id                                      71.72.73.75                    \
    -enable_community                                   1                          \
    -number_of_communities                              1                          \
    -community_type                                     no_export                  \
    -community_as_number                                123                        \
    -community_last_two_octets                          234                        \
    -enable_ext_community                               1                          \
    -number_of_ext_communities                          1                          \
    -ext_communities_type                               admin_as_two_octet         \
    -ext_communities_subtype                            route_target               \
    -ext_community_as_number                            1                          \
    -ext_community_target_assigned_number_4_octets      1                          \
    -ext_community_ip                                   18.19.17.16                    \
    -ext_community_as_4_bytes                           1                          \
    -ext_community_target_assigned_number_2_octets      1                          \
    -ext_community_opaque_data                          ef                         \
    -ext_community_colorCObits                          10                         \
    -ext_community_colorReservedBits                    489                        \
    -ext_community_colorValue                           987                        \
    -ext_community_linkBandwidth                        2045                       \
    -enable_override_peer_as_set_mode                   1                          \
    -as_path_set_mode                                   include_as_seq             \
    -enable_as_path_segments                            1                          \
    -no_of_as_path_segments                             1                          \
    -enable_as_path_segment                             1                          \
    -as_path_segment_type                               as_set                     \
    -number_of_as_number_in_segment                     1                          \
    -as_path_segment_enable_as_number                   1                          \
    -as_path_segment_as_number                          256                        \
    -enable_cluster                                     1                          \
    -no_of_clusters                                     1                          \
    -cluster_id                                         55.66.77.88                    \
]
if {[keylget bgp_flow_spec_ranges_list_v6_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_flow_spec_ranges_list_v6_2_status log]"
    return 0
}
############################################################################
# Start BGP6 protocol                                                       #
############################################################################
	
puts "Waiting 5 seconds before starting protocol(s) ..."
    after 5000
	
puts {Starting all protocol(s) ...}
set r [::ixiangpf::test_control -action start_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
}

puts {Waiting for 60 seconds}
    after 60000
	
############################################################################
# Retrieve protocol statistics                                             # 
############################################################################
puts {Fetching BGP6 aggregated statistics}
set aggregate_stats [::ixiangpf::emulation_bgp_info                                \
    -handle $bgp_v6_Interface_1_handle                                                 \
    -mode stats_per_device_group]
	
if {[keylget aggregate_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget aggregate_stats log]"
}

puts $aggregate_stats
	
############################################################################
# Retrieve protocol learned info                                           #
############################################################################
puts {Fetching BGP6 learned info}
set learned_info [::ixiangpf::emulation_bgp_info                                   \
    -handle $bgp_v6_Interface_1_handle                                                 \
    -mode learned_info]
	
if {[keylget learned_info status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget learned_info log]"
}

puts $learned_info

############################################################################
# Stop all protocols                                                       #
############################################################################
puts {Stopping all protocol(s) ...}
set r [::ixiangpf::test_control -action stop_all_protocols]
    if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
}
	
puts "!!! Test Script Ends !!!"
return 1
