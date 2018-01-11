#################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    08-15-2013 Mchakravarthy - created sample
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
#    This sample configures device groups containing BGP with IPv4 and IPv6 routers on both ports     #
#    and retreives session stats                                               #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################


if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

################################################################################
# General script variables
################################################################################
set test_name                                   [info script]


set chassis 10.216.108.123
set ixnetwork_tcl_server 10.216.108.49:8500

set port_list {2/3 2/4}
set vport_name_list {{{{10GE LAN - 001}} {{10GE LAN - 002}}}}
set aggregation_mode {{not_supported not_supported}}
set aggregation_resource_mode {{normal normal}}


################################################################################
# START - Connect to the chassis
################################################################################

set ret [::ixiangpf::connect                           \
    -reset 1                                                \
    -device $chassis                                        \
    -aggregation_mode $aggregation_mode                     \
    -aggregation_resource_mode $aggregation_resource_mode   \
    -port_list $port_list                                   \
    -ixnetwork_tcl_server $ixnetwork_tcl_server             \
    -tcl_server $chassis                                    \
]
if {[keylget ret status] != $::SUCCESS} {
    error $ret
}

set i -1
set ch_vport_list [list]
foreach {port} $port_list {
    if {[catch {keylget ret port_handle.$chassis.$port} port_handle]} {
        error "connection status: $ret: $port_handle"
    }
    set ph_[incr i] $port_handle
    lappend ch_vport_list $port_handle
}

set vpinfo_rval [::ixia::vport_info     \
    -mode set_info                      \
    -port_list $ch_vport_list           \
    -port_name_list $vport_name_list    \
]
if {[keylget vpinfo_rval status] != $::SUCCESS} {
    error $vpinfo_rval
}

proc create_topology {ph name} {
    set topology_1_status [::ixiangpf::topology_config \
        -topology_name      $name   \
        -port_handle        $ph     \
    ]
    if {[keylget topology_1_status status] != $::SUCCESS} {
        error $topology_1_status
    }
    return [keylget topology_1_status topology_handle]    
}
proc create_devicegroup {topology name} {
    set device_group_status [::ixiangpf::topology_config \
        -topology_handle              $topology            \
        -device_group_name            $name                \
        -device_group_multiplier      1                    \
        -device_group_enabled         1                    \
    ]
    if {[keylget device_group_status status] != $::SUCCESS} {
        error $device_group_status
    }
    return [keylget device_group_status device_group_handle]    
}
proc create_ethernet {topology devicegroup name} {
    set mv_src_mac_addr_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          00.11.01.00.00.01       \
        -counter_step           00.00.00.00.00.01       \
        -counter_direction      increment               \
        -nest_step              00.00.01.00.00.00       \
        -nest_owner             $topology               \
        -nest_enabled           1                       \
    ]
    if {[keylget mv_src_mac_addr_status status] != $::SUCCESS} {
        error $mv_src_mac_addr_status
    }
    set mv_src_mac_addr [keylget mv_src_mac_addr_status multivalue_handle]

    set ethernet_status [::ixiangpf::interface_config \
        -protocol_name                $name                      \
        -protocol_handle              $devicegroup               \
        -mtu                          1500                       \
        -src_mac_addr                 $mv_src_mac_addr           \
        -vlan                         0                          \
        -vlan_id                      1                          \
        -vlan_id_step                 0                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
        -use_vpn_parameters           0                          \
        -site_id                      0                          \
    ]
    if {[keylget ethernet_status status] != $::SUCCESS} {
        error $ethernet_status
    }
    return [keylget ethernet_status ethernet_handle]
}
proc create_ipv4 {topology ethernet name ip_address gw_address} {
    set mv_intf_ip_addr_status [::ixiangpf::multivalue_config \
        -pattern                counter         \
        -counter_start          $ip_address     \
        -counter_step           0.0.1.0         \
        -counter_direction      increment       \
        -nest_step              0.1.0.0         \
        -nest_owner             $topology       \
        -nest_enabled           1               \
    ]
    if {[keylget mv_intf_ip_addr_status status] != $::SUCCESS} {
        error $mv_intf_ip_addr_status
    }
    set mv_intf_ip_addr [keylget mv_intf_ip_addr_status multivalue_handle]

    set mv_gateway_status [::ixiangpf::multivalue_config \
        -pattern                counter         \
        -counter_start          $gw_address     \
        -counter_step           0.0.1.0         \
        -counter_direction      increment       \
        -nest_step              0.0.0.1         \
        -nest_owner             $topology       \
        -nest_enabled           0               \
    ]
    if {[keylget mv_gateway_status status] != $::SUCCESS} {
        error $mv_gateway_status
    }
    set mv_gateway [keylget mv_gateway_status multivalue_handle]

    set ipv4_status [::ixiangpf::interface_config \
        -protocol_name                $name                 \
        -protocol_handle              $ethernet             \
        -ipv4_resolve_gateway         1                     \
        -ipv4_manual_gateway_mac      00.00.00.00.00.01     \
        -gateway                      $mv_gateway           \
        -intf_ip_addr                 $mv_intf_ip_addr      \
        -netmask                      255.255.255.0         \
    ]
    if {[keylget ipv4_status status] != $::SUCCESS} {
        error $ipv4_status
    }
    return [keylget ipv4_status ipv4_handle]
}
proc create_bgp {topology ipv4 remote_ip local_ip} {
    set mv_remote_ip_addr_status [::ixiangpf::multivalue_config \
        -pattern                counter         \
        -counter_start          $remote_ip      \
        -counter_step           0.0.0.0         \
        -counter_direction      decrement       \
        -nest_step              0.0.0.1         \
        -nest_owner             $topology       \
        -nest_enabled           0               \
    ]
    if {[keylget mv_remote_ip_addr_status status] != $::SUCCESS} {
        error $mv_remote_ip_addr_status
    }
    set mv_remote_ip_addr [keylget mv_remote_ip_addr_status multivalue_handle]

    set mv_local_router_id_status [::ixiangpf::multivalue_config \
        -pattern                counter         \
        -counter_start          $local_ip       \
        -counter_step           0.0.1.0         \
        -counter_direction      increment       \
        -nest_step              0.1.0.0         \
        -nest_owner             $topology       \
        -nest_enabled           1               \
    ]
    if {[keylget mv_local_router_id_status status] != $::SUCCESS} {
        error $mv_local_router_id_status
    }
    set mv_local_router_id [keylget mv_local_router_id_status multivalue_handle]

    set bgp_ipv4_peer_1_status [::ixiangpf::emulation_bgp_config \
        -mode                                    enable                    \
        -md5_enable                              0                         \
        -handle                                  $ipv4                     \
        -remote_ip_addr                          $mv_remote_ip_addr        \
        -enable_4_byte_as                        0                         \
        -local_as                                0                         \
        -update_interval                         0                         \
        -count                                   1                         \
        -local_router_id                         $mv_local_router_id       \
        -hold_time                               90                        \
        -neighbor_type                           internal                  \
        -graceful_restart_enable                 0                         \
        -restart_time                            45                        \
        -stale_time                              0                         \
        -tcp_window_size                         8192                      \
        -local_router_id_enable                  1                         \
        -ipv4_capability_mdt_nlri                0                         \
        -ipv4_capability_unicast_nlri            1                         \
        -ipv4_filter_unicast_nlri                1                         \
        -ipv4_capability_multicast_nlri          1                         \
        -ipv4_filter_multicast_nlri              0                         \
        -ipv4_capability_mpls_nlri               1                         \
        -ipv4_filter_mpls_nlri                   0                         \
        -ipv4_capability_mpls_vpn_nlri           1                         \
        -ipv4_filter_mpls_vpn_nlri               0                         \
        -ipv4_capability_multicast_vpn_nlri      0                         \
        -ipv4_filter_multicast_vpn_nlri          0                         \
        -ipv6_capability_unicast_nlri            1                         \
        -ipv6_filter_unicast_nlri                1                         \
        -ipv6_capability_multicast_nlri          1                         \
        -ipv6_filter_multicast_nlri              0                         \
        -ipv6_capability_mpls_nlri               1                         \
        -ipv6_filter_mpls_nlri                   0                         \
        -ipv6_capability_mpls_vpn_nlri           1                         \
        -ipv6_filter_mpls_vpn_nlri               0                         \
        -ipv6_capability_multicast_vpn_nlri      0                         \
        -ipv6_filter_multicast_vpn_nlri          0                         \
        -ttl_value                               64                        \
        -updates_per_iteration                   1                         \
        -bfd_registration                        0                         \
        -bfd_registration_mode                   multi_hop                 \
        -vpls_capability_nlri                    1                         \
        -vpls_filter_nlri                        0                         \
        -act_as_restarted                        0                         \
        -discard_ixia_generated_routes           0                         \
        -flap_down_time                          0                         \
        -local_router_id_type                    same                      \
        -enable_flap                             0                         \
        -send_ixia_signature_with_routes         0                         \
        -flap_up_time                            0                         \
        -next_hop_enable                         0                         \
        -next_hop_ip                             0.0.0.0                   \
        -advertise_end_of_rib                    0                         \
        -configure_keepalive_timer               0                         \
        -keepalive_timer                         30                        \
    ]
    puts "----------------------------"
    puts "$bgp_ipv4_peer_1_status"
    puts "----------------------------"

    if {[keylget bgp_ipv4_peer_1_status status] != $::SUCCESS} {
        error $bgp_ipv4_peer_1_status
    }
    return [list \
        [keylget bgp_ipv4_peer_1_status bgp_handle] \
        [keylget bgp_ipv4_peer_1_status handles]     \
    ]
}
proc create_bgp_ipv4_routes {topology devicegroup bgp_peer} {
    set mv_prefix_status [::ixiangpf::multivalue_config \
        -pattern                counter                     \
        -counter_start          0.1.0.0                     \
        -counter_step           255.255.255.255             \
        -counter_direction      decrement                   \
        -nest_step              0.0.0.1,0.0.0.1             \
        -nest_owner             $devicegroup,$topology      \
        -nest_enabled           0,0                         \
    ]
    if {[keylget mv_prefix_status status] != $::SUCCESS} {
        error $mv_prefix_status
    }
    set mv_prefix [keylget mv_prefix_status multivalue_handle]

    set mv_ext_communities_assigned_two_bytes_status [::ixiangpf::multivalue_config \
        -pattern                counter                     \
        -counter_start          1                           \
        -counter_step           1                           \
        -counter_direction      increment                   \
        -nest_step              1,0                         \
        -nest_owner             $devicegroup,$topology      \
        -nest_enabled           0,1                         \
    ]
    if {[keylget mv_ext_communities_assigned_two_bytes_status status] != $::SUCCESS} {
        error $mv_ext_communities_assigned_two_bytes_status
    }
    set mv_ext_communities_assigned_two_bytes [keylget mv_ext_communities_assigned_two_bytes_status multivalue_handle]

    set mv_ext_communities_assigned_four_bytes_status [::ixiangpf::multivalue_config \
        -pattern                counter                     \
        -counter_start          1                           \
        -counter_step           1                           \
        -counter_direction      increment                   \
        -nest_step              1,0                         \
        -nest_owner             $devicegroup,$topology      \
        -nest_enabled           0,1                         \
    ]
    if {[keylget mv_ext_communities_assigned_four_bytes_status status] != $::SUCCESS} {
        error $mv_ext_communities_assigned_four_bytes_status
    }
    set mv_ext_communities_assigned_four_bytes [keylget mv_ext_communities_assigned_four_bytes_status multivalue_handle]

    set network_group_status [::ixiangpf::emulation_bgp_route_config \
        -handle                                   $bgp_peer                                 \
        -mode                                     add                                       \
        -active                                   1                                         \
        -ipv4_unicast_nlri                        1                                         \
        -max_route_ranges                         5                                         \
        -ip_version                               4                                         \
        -prefix                                   $mv_prefix                                \
        -num_routes                               1                                         \
        -prefix_from                              24                                        \
        -advertise_nexthop_as_v4                  0                                         \
        -aggregator_as                            0                                         \
        -aggregator_id                            0.0.0.0                                   \
        -aggregator_id_mode                       increment                                 \
        -as_path_set_mode                         include_as_seq                            \
        -flap_delay                               0                                         \
        -flap_down_time                           0                                         \
        -enable_aggregator                        0                                         \
        -enable_as_path                           1                                         \
        -atomic_aggregate                         0                                         \
        -cluster_list_enable                      0                                         \
        -communities_enable                       1                                         \
        -ext_communities_enable                   1                                         \
        -enable_route_flap                        0                                         \
        -enable_local_pref                        1                                         \
        -enable_med                               0                                         \
        -next_hop_enable                          1                                         \
        -origin_route_enable                      1                                         \
        -originator_id_enable                     0                                         \
        -partial_route_flap_from_route_index      0                                         \
        -partial_route_flap_to_route_index        0                                         \
        -next_hop_ipv4                            0.0.0.0                                   \
        -next_hop_ipv6                            0:0:0:0:0:0:0:0                           \
        -local_pref                               0                                         \
        -multi_exit_disc                          0                                         \
        -next_hop_mode                            fixed                                     \
        -next_hop_ip_version                      4                                         \
        -next_hop_set_mode                        same                                      \
        -origin                                   igp                                       \
        -originator_id                            0.0.0.0                                   \
        -packing_from                             0                                         \
        -packing_to                               0                                         \
        -enable_partial_route_flap                0                                         \
        -flap_up_time                             0                                         \
        -enable_traditional_nlri                  1                                         \
        -communities_as_number                    0                                         \
        -communities_last_two_octets              0                                         \
        -ext_communities_as_two_bytes             1                                         \
        -ext_communities_as_four_bytes            1                                         \
        -ext_communities_assigned_two_bytes       $mv_ext_communities_assigned_two_bytes    \
        -ext_communities_assigned_four_bytes      $mv_ext_communities_assigned_four_bytes   \
        -ext_communities_ip                       1.1.1.1                                   \
        -ext_communities_opaque_data              0                                         \
        -as_path_segment_numbers                  [list [list 1]]                           \
    ]
    if {[keylget network_group_status status] != $::SUCCESS} {
        error $network_group_status
    }
}
proc create_bgp_ipv6_routes {topology devicegroup bgp_peer} {
    set mv_prefix_status [::ixiangpf::multivalue_config \
        -pattern                counter                             \
        -counter_start          0:1:0:0:0:0:0:0                     \
        -counter_step           ffff:0:0:0:0:0:0:0                  \
        -counter_direction      decrement                           \
        -nest_step              0:0:0:0:0:0:0:1,0:0:0:0:0:0:0:1     \
        -nest_owner             $devicegroup,$topology              \
        -nest_enabled           0,0                                 \
    ]
    if {[keylget mv_prefix_status status] != $::SUCCESS} {
        error $mv_prefix_status
    }
    set mv_prefix [keylget mv_prefix_status multivalue_handle]
    
    set mv_ext_communities_assigned_two_bytes_status [::ixiangpf::multivalue_config \
        -pattern                counter                     \
        -counter_start          1                           \
        -counter_step           1                           \
        -counter_direction      increment                   \
        -nest_step              1,0                         \
        -nest_owner             $devicegroup,$topology      \
        -nest_enabled           0,1                         \
    ]
    if {[keylget mv_ext_communities_assigned_two_bytes_status status] != $::SUCCESS} {
        error $mv_ext_communities_assigned_two_bytes_status
    }
    set mv_ext_communities_assigned_two_bytes [keylget mv_ext_communities_assigned_two_bytes_status multivalue_handle]
    
    set mv_ext_communities_assigned_four_bytes_status [::ixiangpf::multivalue_config \
        -pattern                counter                     \
        -counter_start          1                           \
        -counter_step           1                           \
        -counter_direction      increment                   \
        -nest_step              1,0                         \
        -nest_owner             $devicegroup,$topology      \
        -nest_enabled           0,1                         \
    ]
    if {[keylget mv_ext_communities_assigned_four_bytes_status status] != $::SUCCESS} {
        error $mv_ext_communities_assigned_four_bytes_status
    }
    set mv_ext_communities_assigned_four_bytes [keylget mv_ext_communities_assigned_four_bytes_status multivalue_handle]
    
    set mv_as_path_segment_numbers_2_1_status [::ixiangpf::multivalue_config \
        -pattern                counter                     \
        -counter_start          3                           \
        -counter_step           1                           \
        -counter_direction      increment                   \
        -nest_step              1,1                         \
        -nest_owner             $devicegroup,$topology      \
        -nest_enabled           0,0                         \
    ]
    if {[keylget mv_as_path_segment_numbers_2_1_status status] != $::SUCCESS} {
        error $mv_as_path_segment_numbers_2_1_status
    }
    set mv_as_path_segment_numbers_2_1 [keylget mv_as_path_segment_numbers_2_1_status multivalue_handle]
    
    set network_group_status [::ixiangpf::emulation_bgp_route_config \
        -handle                                   $bgp_peer                                                     \
        -mode                                     add                                                           \
        -active                                   1                                                             \
        -ipv6_unicast_nlri                        1                                                             \
        -max_route_ranges                         5                                                             \
        -ip_version                               6                                                             \
        -prefix                                   $mv_prefix                                                    \
        -num_routes                               1                                                             \
        -prefix_from                              64                                                            \
        -advertise_nexthop_as_v4                  0                                                             \
        -aggregator_as                            0                                                             \
        -aggregator_id                            0.0.0.0                                                       \
        -aggregator_id_mode                       increment                                                     \
        -as_path_set_mode                         include_as_seq                                                \
        -flap_delay                               0                                                             \
        -flap_down_time                           0                                                             \
        -enable_aggregator                        0                                                             \
        -enable_as_path                           1                                                             \
        -atomic_aggregate                         0                                                             \
        -cluster_list_enable                      0                                                             \
        -communities_enable                       0                                                             \
        -ext_communities_enable                   0                                                             \
        -enable_route_flap                        0                                                             \
        -enable_local_pref                        1                                                             \
        -enable_med                               0                                                             \
        -next_hop_enable                          1                                                             \
        -origin_route_enable                      1                                                             \
        -originator_id_enable                     0                                                             \
        -partial_route_flap_from_route_index      0                                                             \
        -partial_route_flap_to_route_index        0                                                             \
        -next_hop_ipv4                            0.0.0.0                                                       \
        -next_hop_ipv6                            0:0:0:0:0:0:0:0                                               \
        -local_pref                               0                                                             \
        -multi_exit_disc                          0                                                             \
        -next_hop_mode                            fixed                                                         \
        -next_hop_ip_version                      4                                                             \
        -next_hop_set_mode                        same                                                          \
        -origin                                   igp                                                           \
        -originator_id                            0.0.0.0                                                       \
        -packing_from                             0                                                             \
        -packing_to                               0                                                             \
        -enable_partial_route_flap                0                                                             \
        -flap_up_time                             0                                                             \
        -enable_traditional_nlri                  1                                                             \
        -communities_as_number                    0                                                             \
        -communities_last_two_octets              0                                                             \
        -ext_communities_as_two_bytes             1                                                             \
        -ext_communities_as_four_bytes            1                                                             \
        -ext_communities_assigned_two_bytes       $mv_ext_communities_assigned_two_bytes                        \
        -ext_communities_assigned_four_bytes      $mv_ext_communities_assigned_four_bytes                       \
        -ext_communities_ip                       1.1.1.1                                                       \
        -ext_communities_opaque_data              0                                                             \
        -as_path_segment_numbers                  [list [list 1 2] [list $mv_as_path_segment_numbers_2_1 2 1]]  \
        -as_path_segment_type                     [list as_set as_seq]                                          \
    ]
    if {[keylget network_group_status status] != $::SUCCESS} {
        error $network_group_status
    }
}

############################################
## configure bgp device group on first port 
## with ipv4 routes
############################################
set topology_1_handle [create_topology $ph_0 {BGP w/Random v4 Prefix/Length}]
set deviceGroup_1_handle [create_devicegroup $topology_1_handle {BGP Router 1}]
set ethernet_1_handle [create_ethernet $topology_1_handle $deviceGroup_1_handle {Ethernet 1}]
set ipv4_1_handle [create_ipv4 \
    $topology_1_handle $ethernet_1_handle   \
    {IPv4 1}                                \
    100.1.0.1                               \
    100.1.0.2                               \
]
set bgpIpv4Peer_1_list [create_bgp          \
    $topology_1_handle $ipv4_1_handle       \
    100.1.0.2                               \
    100.1.0.1                               \
]
set bgpIpv4Peer_1_handle [lindex $bgpIpv4Peer_1_list 0]
set bgpIpv4Peer_1_items [lindex $bgpIpv4Peer_1_list 1]
create_bgp_ipv4_routes $topology_1_handle $deviceGroup_1_handle $bgpIpv4Peer_1_handle

############################################
## configure bgp device group on second port
## with ipv6 routes
############################################
set topology_2_handle [create_topology $ph_1 {BGP w/Random v6 Prefix/Length}]
set deviceGroup_2_handle [create_devicegroup $topology_2_handle {BGP Router 2}]
set ethernet_2_handle [create_ethernet $topology_2_handle $deviceGroup_2_handle {Ethernet 2}]
set ipv4_2_handle [create_ipv4 \
    $topology_2_handle $ethernet_2_handle   \
    {IPv4 2}                                \
    100.1.0.2                               \
    100.1.0.1                               \
]
set bgpIpv4Peer_2_list [create_bgp          \
    $topology_2_handle $ipv4_2_handle       \
    100.1.0.1                               \
    100.1.0.2                               \
]
set bgpIpv4Peer_2_handle [lindex $bgpIpv4Peer_2_list 0]
set bgpIpv4Peer_2_items [lindex $bgpIpv4Peer_2_list 1]
create_bgp_ipv6_routes $topology_2_handle $deviceGroup_2_handle $bgpIpv4Peer_2_handle

############################################
## start all protocols
############################################
set ret [::ixiangpf::test_control -action start_all_protocols]
if {[keylget ret status] != $::SUCCESS} {
    error $ret
}
after 30000

############################################
## get learned routes
############################################
set learned_info_1 [::ixiangpf::emulation_bgp_info   \
    -mode learned_info                  \
    -handle $bgpIpv4Peer_1_handle       \
]
if {[keylget learned_info_1 status] != $::SUCCESS} {
    error $learned_info_1
}
foreach bgp_item $bgpIpv4Peer_1_items {
    set ip_prefixes [keylget learned_info_1 $bgp_item.learned_info.ipv6_prefixes]
    puts "IPv6 prefixes for BGP session $bgp_item: \n $ip_prefixes"
}

set learned_info_2 [::ixiangpf::emulation_bgp_info   \
    -mode learned_info                  \
    -handle $bgpIpv4Peer_2_handle       \
]
if {[keylget learned_info_2 status] != $::SUCCESS} {
    error $learned_info_2
}
foreach bgp_item $bgpIpv4Peer_2_items {
    set ip_prefixes [keylget learned_info_2 $bgp_item.learned_info.ipv4_prefixes]
    puts "IPv4 prefixes for BGP session $bgp_item: \n $ip_prefixes"
}

############################################
## stop all protocols
############################################
set ret [::ixiangpf::test_control -action stop_all_protocols]
if {[keylget ret status] != $::SUCCESS} {
    error $ret
}


puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1

