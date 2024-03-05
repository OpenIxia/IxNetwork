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
#    than it will retrieve and display few statistics and modify the FLOW-SPEC #
#    field through HLT.                                                        #
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

set chassis_ip        {10.39.50.123}
set tcl_server        10.39.50.121
set port_list         {1/7 1/8}
set ixNetwork_client  "10.39.50.121:8119"
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
    -topology_name      {BGP Topology 1}          \
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
    -device_group_name            {BGP Topology 1 Router} \
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
    -topology_name      {BGP Topology 2}           \
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
    -device_group_name            {BGP Topology 2 Router} \
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

# Creating IPv4 Stack on top of Ethernet Stack for the first Device Group                                 
puts "Creating IPv4 Stack on top of Ethernet Stack for the first Device Group"
set ipv4_1_status [::ixiangpf::interface_config          \
    -protocol_name                     {IPv4 1}          \
    -protocol_handle                   $ethernet_1_handle\
    -ipv4_resolve_gateway              1                 \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01 \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00 \
    -gateway                           200.200.200.10        \
    -gateway_step                      0.0.0.0           \
    -intf_ip_addr                      200.200.200.20        \
    -intf_ip_addr_step                 0.0.0.0           \
    -netmask                           255.255.255.0     \
    ]
if {[keylget ipv4_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_1_status log]"
    return 0
}
set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]

# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group 
puts "Creating IPv4 2 stack on ethernet 2 stack for the second Device Group"
set ipv4_2_status [::ixiangpf::interface_config \
    -protocol_name                     {IPv4 2}                \
    -protocol_handle                   $ethernet_2_handle      \
    -ipv4_resolve_gateway              1                       \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01       \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00       \
    -gateway                           200.200.200.20              \
    -gateway_step                      0.0.0.0                 \
    -intf_ip_addr                      200.200.200.10              \
    -intf_ip_addr_step                 0.0.0.0                 \
    -netmask                           255.255.255.0           \
    ]
if {[keylget ipv4_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_2_status log]"
    return 0
}
set ipv4_2_handle [keylget ipv4_2_status ipv4_handle]


################################################################################
# Other protocol configurations                                                # 
################################################################################

# This will Create BGP Stack on top of IPv4 Stack of Topology1 & Topology2

puts "Creating BGP Stack on top of IPv4 1 stack on Topology 1 !!!!!!!!!!"
set bgp_v4_interface_1_status [::ixiangpf::emulation_bgp_config \
    -mode                                         enable                                        \
    -active                                       1                                             \
    -md5_enable                                   0                                             \
    -md5_key                                      {}                                            \
    -handle                                       $ipv4_1_handle                                \
    -ip_version                                   4                                             \
    -remote_ip_addr                               200.200.200.10                                \
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
    -ipv6_filter_unicast_nlri                     0                                             \
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
    -routers_mac_or_irb_mac_address               00:01:01:00:00:01                             \
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
    -capability_ipv6_unicast_flowSpec             0                                             \
    -filter_ipv6_unicast_flowSpec                 0                                             \
    -always_include_tunnel_enc_ext_community      false                                         \
    -ip_vrf_to_ip_vrf_type                        interfacefullWithUnnumberedCorefacingIRB      \
    -irb_interface_label                          16                                            \
    -irb_ipv4_address                             10.0.1.1                                      \
 ]
if {[keylget bgp_v4_interface_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_v4_interface_1_status log]"
    return 0
}

set bgpInterface_1_handle [keylget bgp_v4_interface_1_status bgp_handle]
# This will create BGP IPv4 Flow-Spec on top of BGP Stack @PEER2 SIDE
puts "Enabling BGP FLOW-Spec and with configure Flow-spec on top BGP Stack of Topology1 !!!!!!!"
set bgp_flow_spec_ranges_list_v4_1_status [::ixiangpf::emulation_bgp_flow_spec_config \
    -mode                                               enable                      \
    -fs_mode                                            fsv4                        \
    -handle                                             $bgpInterface_1_handle      \
    -no_of_flowSpecRangeV4                              1                           \
    -active                                             1                           \
    -flowSpecName                                       {BGP Flow Spec 11-100}      \
    -fsv4_enableDestPrefix                              1                           \
    -fsv4_destPrefix                                    1.1.0.1                     \
    -fsv4_destPrefixLength                              24                          \
    -fsv4_enableSrcPrefix                               1                           \
    -fsv4_srcPrefix                                     1.0.1.1                     \
    -fsv4_srcPrefixLength                               24                          \
    -fsv4_ipProto                                       123                         \
    -portMatch                                          345                         \
    -destPortMatch                                      567                         \
    -srcPortMatch                                       789                         \
    -icmpTypeMatch                                      100||200                    \
    -icmpCodeMatch                                      100||150-200&&>250          \
    -tcpFlagsMatch                                      (cwr)                       \
    -ipPacketMatch                                      >=1 && <=56 || 50 || !60000 \
    -dscpMatch                                          25                          \
    -fsv4_fragmentMatch                                 (lf)                        \
    -enable_traffic_rate                                1                           \
    -trafficRate                                        1000                        \
    -enable_trafficAction                               1                           \
    -terminalAction                                     1                           \
    -trafficActionSample                                1                           \
    -enable_redirect                                    1                           \
    -redirect_ext_communities_type                      rdIPv4                      \
    -as_2_bytes                                         1                           \
    -as_4_bytes                                         1                           \
    -fsv4_ipv4                                          1.1.1.1                     \
    -assigned_number_2_octets                           200                         \
    -assigned_number_4_octets                           100                         \
    -Cbit                                               1                           \
    -nextHop                                            1.1.1.1                     \
    -enable_trafficMarking                              1                           \
    -dscp                                               20                          \
    -enable_next_hop                                    1                           \
    -set_next_hop                                       manually                    \
    -set_next_hop_ip_type                               ipv4                        \
    -ipv4_next_hop                                      100.100.100.10              \
    -ipv6_next_hop                                      0:0:0:0:0:0:0:0             \
    -enable_origin                                      1                           \
    -origin                                             igp                         \
    -enable_local_preference                            1                           \
    -local_preference                                   200                         \
    -enable_multi_exit_discriminator                    1                           \
    -multi_exit_discriminator                           1234                        \
    -enable_atomic_aggregate                            1                           \
    -enable_aggregator_id                               1                           \
    -aggregator_id                                      4.4.4.4                     \
    -aggregator_as                                      10                          \
    -enable_originator_id                               1                           \
    -originator_id                                      3.3.3.3                     \
    -enable_community                                   1                           \
    -number_of_communities                              1                           \
    -community_type                                     no_export                   \
    -community_as_number                                123                         \
    -community_last_two_octets                          1234                        \
    -enable_ext_community                               1                           \
    -number_of_ext_communities                          1                           \
    -ext_communities_type                               admin_as_two_octet          \
    -ext_communities_subtype                            route_target                \
    -ext_community_as_number                            1                           \
    -ext_community_target_assigned_number_4_octets      100                         \
    -ext_community_ip                                   1.1.1.1                     \
    -ext_community_as_4_bytes                           1                           \
    -ext_community_target_assigned_number_2_octets      200                         \
    -ext_community_opaque_data                          ff                          \
    -ext_community_colorCObits                          00                          \
    -ext_community_colorReservedBits                    1                           \
    -ext_community_colorValue                           100                         \
    -ext_community_linkBandwidth                        1000                        \
    -enable_override_peer_as_set_mode                   1                           \
    -as_path_set_mode                                   include_as_seq              \
    -enable_as_path_segments                            1                           \
    -no_of_as_path_segments                             1                           \
    -enable_as_path_segment                             1                           \
    -as_path_segment_type                               as_set                      \
    -number_of_as_number_in_segment                     1                           \
    -as_path_segment_enable_as_number                   1                           \
    -as_path_segment_as_number                          1                           \
    -enable_cluster                                     1                           \
    -no_of_clusters                                     1                           \
    -cluster_id                                         1.1.1.1                     \
]
    
if {[keylget bgp_flow_spec_ranges_list_v4_1_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $bgp_flow_spec_ranges_list_v4_1_status
}
set bgpFlowSpecRangesListV4_1_handle [keylget bgp_flow_spec_ranges_list_v4_1_status bgp_flowSpecV4_handle]

puts "Creating BGP Stack on top of IPv4 1 stack on Topology 2!!!!!!!!!!!"
set bgp_v4_interface_2_status [::ixiangpf::emulation_bgp_config   \
    -mode                                         enable                                        \
    -active                                       1                                             \
    -md5_enable                                   0                                             \
    -md5_key                                      {}                                            \
    -handle                                       $ipv4_2_handle                                \
    -ip_version                                   4                                             \
    -remote_ip_addr                               200.200.200.20                                \
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
    -ipv6_filter_unicast_nlri                     0                                             \
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
    -routers_mac_or_irb_mac_address               00:01:02:00:00:01                             \
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
    -capability_ipv6_unicast_flowSpec             0                                             \
    -filter_ipv6_unicast_flowSpec                 0                                             \
    -always_include_tunnel_enc_ext_community      false                                         \
    -ip_vrf_to_ip_vrf_type                        interfacefullWithUnnumberedCorefacingIRB      \
    -irb_interface_label                          16                                            \
    -irb_ipv4_address                             11.0.1.1                                      \
]
	
if {[keylget bgp_v4_interface_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_v4_interface_2_status log]"
    return 0
}

set bgpInterface_2_handle [keylget bgp_v4_interface_2_status bgp_handle]
# This will create BGP IPv4 Flow-Spec on top of BGP Stack @PEER2 SIDE
set bgp_flow_spec_ranges_list_v4_2_status [::ixiangpf::emulation_bgp_flow_spec_config \
    -mode                                               enable                      \
    -fs_mode                                            fsv4                        \
    -handle                                             $bgpInterface_2_handle      \
    -no_of_flowSpecRangeV4                              1                           \
    -active                                             1                           \
    -flowSpecName                                       {BGP Flow Spec 11-100}      \
    -fsv4_enableDestPrefix                              1                           \
    -fsv4_destPrefix                                    200.1.0.0                   \
    -fsv4_destPrefixLength                              24                          \
    -fsv4_enableSrcPrefix                               1                           \
    -fsv4_srcPrefix                                     1.0.1.1                     \
    -fsv4_srcPrefixLength                               24                          \
    -fsv4_ipProto                                       234                         \
    -portMatch                                          456                         \
    -destPortMatch                                      678                         \
    -srcPortMatch                                       890                         \
    -icmpTypeMatch                                      >100||<200                  \
    -icmpCodeMatch                                      10||15-20&&>25              \
    -tcpFlagsMatch                                      (not)(cwr|syn)              \
    -ipPacketMatch                                      >=1 && <=56 || 50 || !102       \
    -dscpMatch                                          50                          \
    -fsv4_fragmentMatch                                 (ff)                        \
    -enable_traffic_rate                                1                           \
    -trafficRate                                        1000                        \
    -enable_trafficAction                               1                           \
    -terminalAction                                     1                           \
    -trafficActionSample                                1                           \
    -enable_redirect                                    1                           \
    -redirect_ext_communities_type                      rdIPv4                      \
    -as_2_bytes                                         1                           \
    -as_4_bytes                                         1                           \
    -fsv4_ipv4                                          1.1.1.1                     \
    -assigned_number_2_octets                           300                         \
    -assigned_number_4_octets                           200                         \
    -Cbit                                               1                           \
    -nextHop                                            1.1.1.1                     \
    -enable_trafficMarking                              1                           \
    -dscp                                               10                          \
    -enable_next_hop                                    1                           \
    -set_next_hop                                       sameaslocalip               \
    -set_next_hop_ip_type                               ipv4                        \
    -ipv4_next_hop                                      0.0.0.0                     \
    -ipv6_next_hop                                      0:0:0:0:0:0:0:0             \
    -enable_origin                                      1                           \
    -origin                                             igp                         \
    -enable_local_preference                            1                           \
    -local_preference                                   100                         \
    -enable_multi_exit_discriminator                    1                           \
    -multi_exit_discriminator                           100                         \
    -enable_atomic_aggregate                            1                           \
    -enable_aggregator_id                               1                           \
    -aggregator_id                                      5.5.5.5                     \
    -aggregator_as                                      100                         \
    -enable_originator_id                               1                           \
    -originator_id                                      6.6.6.6                     \
    -enable_community                                   1                           \
    -number_of_communities                              1                           \
    -community_type                                     no_export                   \
    -community_as_number                                1000                        \
    -community_last_two_octets                          1000                        \
    -enable_ext_community                               1                           \
    -number_of_ext_communities                          1                           \
    -ext_communities_type                               admin_as_two_octet          \
    -ext_communities_subtype                            route_target                \
    -ext_community_as_number                            1                           \
    -ext_community_target_assigned_number_4_octets      100                         \
    -ext_community_ip                                   1.1.1.1                     \
    -ext_community_as_4_bytes                           1                           \
    -ext_community_target_assigned_number_2_octets      200                         \
    -ext_community_opaque_data                          ab                          \
    -ext_community_colorCObits                          01                          \
    -ext_community_colorReservedBits                    1                           \
    -ext_community_colorValue                           200                         \
    -ext_community_linkBandwidth                        2000                        \
    -enable_override_peer_as_set_mode                   1                           \
    -as_path_set_mode                                   include_as_seq              \
    -enable_as_path_segments                            1                           \
    -no_of_as_path_segments                             1                           \
    -enable_as_path_segment                             1                           \
    -as_path_segment_type                               as_set                      \
    -number_of_as_number_in_segment                     1                           \
    -as_path_segment_enable_as_number                   1                           \
    -as_path_segment_as_number                          1                           \
    -enable_cluster                                     1                           \
    -no_of_clusters                                     1                           \
    -cluster_id                                         2.2.2.2                     \
]
if {[keylget bgp_flow_spec_ranges_list_v4_2_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $bgp_flow_spec_ranges_list_v4_2_status
}
set bgpFlowSpecRangesListV4_2_handle [keylget bgp_flow_spec_ranges_list_v4_2_status bgp_flowSpecV4_handle]

puts "After 5 secs Modify the value of Flow-Spec fields of BGP IPv4 Flow SPec Range of BGP PEER1"
after 5000

puts "Modify the value of Flow-Spec fields of BGP IPv4 FLOW SPEC RANGE of BGP PEER1"
set bgp_flow_spec_ranges_list_v4_1_status [::ixiangpf::emulation_bgp_flow_spec_config \
    -mode                                               modify                      \
    -fs_mode                                            fsv4                        \
    -handle                                             $bgpFlowSpecRangesListV4_1_handle      \
    -no_of_flowSpecRangeV4                              1                           \
    -active                                             1                           \
    -flowSpecName                                       {BGP Flow Spec 11-100}      \
    -fsv4_enableDestPrefix                              1                           \
    -fsv4_destPrefix                                    10.10.10.10                 \
    -fsv4_destPrefixLength                              16                          \
    -fsv4_enableSrcPrefix                               1                           \
    -fsv4_srcPrefix                                     10.10.10.100                \
    -fsv4_srcPrefixLength                               16                          \
    -fsv4_ipProto                                       150                         \
    -portMatch                                          543                         \
    -destPortMatch                                      765                         \
    -srcPortMatch                                       987                         \
    -icmpTypeMatch                                      10||20                      \
    -icmpCodeMatch                                      10||15-20&&>25              \
    -tcpFlagsMatch                                      (syn)                       \
    -ipPacketMatch                                      >=10 && <=9 || 5 || !6000   \
    -dscpMatch                                          15                          \
    -fsv4_fragmentMatch                                 (ff)                        \
    -enable_traffic_rate                                1                           \
    -trafficRate                                        10000                       \
    -enable_trafficAction                               1                           \
    -terminalAction                                     1                           \
    -trafficActionSample                                1                           \
    -enable_redirect                                    1                           \
    -redirect_ext_communities_type                      rdIPv4                      \
    -as_2_bytes                                         1                           \
    -as_4_bytes                                         1                           \
    -fsv4_ipv4                                          10.10.100.100               \
    -assigned_number_2_octets                           500                         \
    -assigned_number_4_octets                           1000                        \
    -Cbit                                               1                           \
    -nextHop                                            5.5.5.5                     \
    -enable_trafficMarking                              1                           \
    -dscp                                               15                          \
    -enable_next_hop                                    1                           \
    -set_next_hop                                       manually                    \
    -set_next_hop_ip_type                               ipv4                        \
    -ipv4_next_hop                                      200.200.200.20              \
    -ipv6_next_hop                                      10:10:10:10:10:10:10:10     \
    -enable_origin                                      1                           \
    -origin                                             igp                         \
    -enable_local_preference                            1                           \
    -local_preference                                   800                         \
    -enable_multi_exit_discriminator                    1                           \
    -multi_exit_discriminator                           4321                        \
    -enable_atomic_aggregate                            1                           \
    -enable_aggregator_id                               1                           \
    -aggregator_id                                      40.40.40.40                 \
    -aggregator_as                                      10                          \
    -enable_originator_id                               1                           \
    -originator_id                                      30.30.30.30                 \
    -enable_community                                   1                           \
    -number_of_communities                              1                           \
    -community_type                                     no_export                   \
    -community_as_number                                321                         \
    -community_last_two_octets                          4321                        \
    -enable_ext_community                               1                           \
    -number_of_ext_communities                          1                           \
    -ext_communities_type                               admin_as_two_octet          \
    -ext_communities_subtype                            route_target                \
    -ext_community_as_number                            1                           \
    -ext_community_target_assigned_number_4_octets      1000                        \
    -ext_community_ip                                   100.100.100.100             \
    -ext_community_as_4_bytes                           1                           \
    -ext_community_target_assigned_number_2_octets      800                         \
    -ext_community_opaque_data                          ab                          \
    -ext_community_colorCObits                          11                          \
    -ext_community_colorReservedBits                    1                           \
    -ext_community_colorValue                           400                         \
    -ext_community_linkBandwidth                        4000                        \
    -enable_override_peer_as_set_mode                   1                           \
    -as_path_set_mode                                   include_as_seq              \
    -enable_as_path_segments                            1                           \
    -no_of_as_path_segments                             1                           \
    -enable_as_path_segment                             1                           \
    -as_path_segment_type                               as_set                      \
    -number_of_as_number_in_segment                     1                           \
    -as_path_segment_enable_as_number                   1                           \
    -as_path_segment_as_number                          1                           \
    -enable_cluster                                     1                           \
    -no_of_clusters                                     1                           \
    -cluster_id                                         100.100.100.100             \
]

if {[keylget bgp_flow_spec_ranges_list_v4_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_flow_spec_ranges_list_v4_1_status log]"
    return 0
}
puts "After 5 secs Modify the value of Flow-Spec fields of BGP IPv4 Flow SPec Range of BGP PEER2!!!"
after 5000

puts "Modify the value of Flow-Spec fields of BGP IPv4 FLOW SPEC RANGE of BGP PEER2!!!!!!!!!!!!!!"
set bgp_flow_spec_ranges_list_v4_2_status [::ixiangpf::emulation_bgp_flow_spec_config \
    -mode                                               modify                      \
    -fs_mode                                            fsv4                        \
    -handle                                             $bgpFlowSpecRangesListV4_2_handle      \
    -no_of_flowSpecRangeV4                              1                           \
    -active                                             1                           \
    -flowSpecName                                       {BGP Flow Spec 11-100}      \
    -fsv4_enableDestPrefix                              1                           \
    -fsv4_destPrefix                                    20.20.20.20                 \
    -fsv4_destPrefixLength                              16                          \
    -fsv4_enableSrcPrefix                               1                           \
    -fsv4_srcPrefix                                     100.155.155.155             \
    -fsv4_srcPrefixLength                               24                          \
    -fsv4_ipProto                                       222                         \
    -portMatch                                          654                         \
    -destPortMatch                                      876                         \
    -srcPortMatch                                       1089                         \
    -icmpTypeMatch                                      >10||<20                  \
    -icmpCodeMatch                                      10||15-200&&>250              \
    -tcpFlagsMatch                                      (not)(cwr|fin)              \
    -ipPacketMatch                                      >=1 && <=56 || 50 || !102       \
    -dscpMatch                                          50                          \
    -fsv4_fragmentMatch                                 (ff)                        \
    -enable_traffic_rate                                1                           \
    -trafficRate                                        1000                        \
    -enable_trafficAction                               1                           \
    -terminalAction                                     1                           \
    -trafficActionSample                                1                           \
    -enable_redirect                                    1                           \
    -redirect_ext_communities_type                      rdIPv4                      \
    -as_2_bytes                                         1                           \
    -as_4_bytes                                         1                           \
    -fsv4_ipv4                                          11.11.11.111                \
    -assigned_number_2_octets                           3000                         \
    -assigned_number_4_octets                           2000                         \
    -Cbit                                               1                           \
    -nextHop                                            10.11.12.13                     \
    -enable_trafficMarking                              1                           \
    -dscp                                               10                          \
    -enable_next_hop                                    1                           \
    -set_next_hop                                       sameaslocalip               \
    -set_next_hop_ip_type                               ipv4                        \
    -ipv4_next_hop                                      0.0.0.0                     \
    -ipv6_next_hop                                      aaaa::BBBB:ac:0             \
    -enable_origin                                      1                           \
    -origin                                             igp                         \
    -enable_local_preference                            1                           \
    -local_preference                                   155                         \
    -enable_multi_exit_discriminator                    1                           \
    -multi_exit_discriminator                           100                         \
    -enable_atomic_aggregate                            1                           \
    -enable_aggregator_id                               1                           \
    -aggregator_id                                      50.5.55.55                  \
    -aggregator_as                                      100                         \
    -enable_originator_id                               1                           \
    -originator_id                                      6.6.6.6                     \
    -enable_community                                   1                           \
    -number_of_communities                              1                           \
    -community_type                                     no_export                   \
    -community_as_number                                1000                        \
    -community_last_two_octets                          1000                        \
    -enable_ext_community                               1                           \
    -number_of_ext_communities                          1                           \
    -ext_communities_type                               admin_as_two_octet          \
    -ext_communities_subtype                            route_target                \
    -ext_community_as_number                            1                           \
    -ext_community_target_assigned_number_4_octets      100                         \
    -ext_community_ip                                   1.1.1.1                     \
    -ext_community_as_4_bytes                           1                           \
    -ext_community_target_assigned_number_2_octets      200                         \
    -ext_community_opaque_data                          ab                          \
    -ext_community_colorCObits                          01                          \
    -ext_community_colorReservedBits                    1                           \
    -ext_community_colorValue                           200                         \
    -ext_community_linkBandwidth                        2000                        \
    -enable_override_peer_as_set_mode                   1                           \
    -as_path_set_mode                                   include_as_seq              \
    -enable_as_path_segments                            1                           \
    -no_of_as_path_segments                             1                           \
    -enable_as_path_segment                             1                           \
    -as_path_segment_type                               as_set                      \
    -number_of_as_number_in_segment                     1                           \
    -as_path_segment_enable_as_number                   1                           \
    -as_path_segment_as_number                          1                           \
    -enable_cluster                                     1                           \
    -no_of_clusters                                     1                           \
    -cluster_id                                         2.2.2.2                     \
]
if {[keylget bgp_flow_spec_ranges_list_v4_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_flow_spec_ranges_list_v4_2_status log]"
    return 0
}
############################################################################
# Start BGP protocol                                                       #
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
puts {Fetching BGP aggregated statistics}
set aggregate_stats [::ixiangpf::emulation_bgp_info                                \
    -handle $bgpInterface_1_handle                                                 \
    -mode stats_per_device_group]
	
if {[keylget aggregate_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget aggregate_stats log]"
}

puts $aggregate_stats
	
############################################################################
# Retrieve protocol learned info                                           #
############################################################################
puts {Fetching BGP learned info}
set learned_info [::ixiangpf::emulation_bgp_info                                   \
    -handle $bgpInterface_1_handle                                                 \
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
