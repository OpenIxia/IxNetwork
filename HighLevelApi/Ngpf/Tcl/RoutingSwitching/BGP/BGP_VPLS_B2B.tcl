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
#    This sample configures BGP L3VPN on both ports                            #
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

set port_list {2/5 2/6}
set vport_name_list {{{{10GE LAN - 001}} {{10GE LAN - 002}}}}
set aggregation_mode {{not_supported not_supported}}
set aggregation_resource_mode {{normal normal}}


################################################################################
# START - Connect to the chassis
################################################################################
set ret [::ixiangpf::connect                                \
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

proc keylprint {var_ref} {
    upvar 1 $var_ref var
    set level [expr [info level] - 1]
    foreach key [keylkeys var] {
        set indent [string repeat "    " $level]
        puts -nonewline $indent 
        if {[catch {keylkeys var $key} catch_rval] || [llength $catch_rval] == 0} {
            puts "$key: [keylget var $key]"
            continue
        } else {
            puts $key
            puts "$indent[string repeat "-" [string length $key]]"
        }
        set rec_key [keylget var $key]
        keylprint rec_key
        puts ""
    }
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
proc create_devicegroup_linked {networkgroup name} {
    set device_group_status [::ixiangpf::topology_config \
        -device_group_name            $name             \
        -device_group_multiplier      1                 \
        -device_group_enabled         1                 \
        -device_group_handle          $networkgroup     \
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
proc create_ipv4_loopback {topology devicegroup networkgroup ip_address name} {
    set mv_intf_ip_addr_status [::ixiangpf::multivalue_config \
        -pattern                counter                                 \
        -counter_start          $ip_address                             \
        -counter_step           0.0.0.1                                 \
        -counter_direction      increment                               \
        -nest_step              0.0.0.1,0.0.0.1,0.1.0.0                 \
        -nest_owner             $networkgroup,$devicegroup,$topology    \
        -nest_enabled           0,0,1                                   \
    ]
    if {[keylget mv_intf_ip_addr_status status] != $::SUCCESS} {
        error $mv_intf_ip_addr_status
    }
    set mv_intf_ip_addr [keylget mv_intf_ip_addr_status multivalue_handle]
    
    set ipv4_loopback_status [::ixiangpf::interface_config \
        -protocol_name            $name             \
        -protocol_handle          $devicegroup      \
        -enable_loopback          1                 \
        -connected_to_handle      $networkgroup     \
        -intf_ip_addr             $mv_intf_ip_addr  \
        -netmask                  255.255.255.255   \
    ]
    if {[keylget ipv4_loopback_status status] != $::SUCCESS} {
        error $ipv4_loopback_status
    }
    return [keylget ipv4_loopback_status ipv4_loopback_handle]
}
proc create_ldp {topology ipv4 lsr_id} {
    set ldp_status [::ixiangpf::emulation_ldp_config \
        -handle                     $ipv4           \
        -mode                       create          \
        -recovery_time              120000          \
        -reconnect_time             120000          \
        -keepalive_interval         15              \
        -keepalive_holdtime         45              \
        -graceful_restart_enable    0               \
        -interface_active           1               \
        -hello_interval             5               \
        -hello_hold_time            15              \
        -label_space                0               \
        -label_adv                  unsolicited     \
        -auth_mode                  null            \
        -lsr_id                     $lsr_id
    ]
    if {[keylget ldp_status status] != $::SUCCESS} {
        error $ldp_status
    }
}
proc create_ospf {topology ipv4 ip_address name} {
    set mv_router_id_status [::ixiangpf::multivalue_config \
        -pattern                counter         \
        -counter_start          $ip_address     \
        -counter_step           0.0.0.1         \
        -counter_direction      increment       \
        -nest_step              0.1.0.0         \
        -nest_owner             $topology       \
        -nest_enabled           1               \
    ]
    if {[keylget mv_router_id_status status] != $::SUCCESS} {
        error $mv_router_id_status
    }
    set mv_router_id [keylget mv_router_id_status multivalue_handle]
    
    set ospfv2_status [::ixiangpf::emulation_ospf_config \
        -handle                                                    $ipv4            \
        -mode                                                      create           \
        -protocol_name                                             $name            \
        -area_id                                                   0.0.0.0          \
        -area_id_as_number                                         0                \
        -area_id_type                                              number           \
        -authentication_mode                                       null             \
        -dead_interval                                             40               \
        -demand_circuit                                            0                \
        -graceful_restart_enable                                   0                \
        -hello_interval                                            10               \
        -router_interface_active                                   1                \
        -enable_fast_hello                                         0                \
        -hello_multiplier                                          2                \
        -max_mtu                                                   1500             \
        -router_active                                             1                \
        -router_asbr                                               0                \
        -do_not_generate_router_lsa                                0                \
        -router_abr                                                0                \
        -inter_flood_lsupdate_burst_gap                            33               \
        -lsa_refresh_time                                          1800             \
        -lsa_retransmit_time                                       5                \
        -max_ls_updates_per_burst                                  1                \
        -oob_resync_breakout                                       0                \
        -interface_cost                                            10               \
        -lsa_discard_mode                                          1                \
        -md5_key_id                                                1                \
        -network_type                                              ptop             \
        -neighbor_router_id                                        0.0.0.0          \
        -type_of_service_routing                                   0                \
        -external_capabilities                                     1                \
        -multicast_capability                                      0                \
        -nssa_capability                                           0                \
        -external_attribute                                        0                \
        -opaque_lsa_forwarded                                      0                \
        -unused                                                    0                \
        -router_id                                                 $mv_router_id    \
        -router_priority                                           2                \
        -te_enable                                                 0                \
        -te_max_bw                                                 0                \
        -te_max_resv_bw                                            0                \
        -te_unresv_bw_priority0                                    0                \
        -te_unresv_bw_priority1                                    0                \
        -te_unresv_bw_priority2                                    0                \
        -te_unresv_bw_priority3                                    0                \
        -te_unresv_bw_priority4                                    0                \
        -te_unresv_bw_priority5                                    0                \
        -te_unresv_bw_priority6                                    0                \
        -te_unresv_bw_priority7                                    0                \
        -te_metric                                                 0                \
        -te_admin_group                                            0                \
        -validate_received_mtu                                     1                \
        -graceful_restart_helper_mode_enable                       0                \
        -strict_lsa_checking                                       1                \
        -support_reason_sw_restart                                 1                \
        -support_reason_sw_reload_or_upgrade                       1                \
        -support_reason_switch_to_redundant_processor_control      1                \
        -support_reason_unknown                                    1                \
    ]
    if {[keylget ospfv2_status status] != $::SUCCESS} {
        error $ospfv2_status
    }
    return [keylget ospfv2_status ospfv2_handle]
}
proc create_ospf_ldp_network_group {topology devicegroup ethernet ospf ip_address name} {
    set mv_ipv4_prefix_network_address_status [::ixiangpf::multivalue_config \
        -pattern                counter                     \
        -counter_start          $ip_address                 \
        -counter_step           0.0.0.1                     \
        -counter_direction      increment                   \
        -nest_step              0.0.0.1,0.1.0.0             \
        -nest_owner             $devicegroup,$topology      \
        -nest_enabled           0,1                         \
    ]
    if {[keylget mv_ipv4_prefix_network_address_status status] != $::SUCCESS} {
        error $mv_ipv4_prefix_network_address_status
    }
    set mv_ipv4_prefix_network_address [keylget mv_ipv4_prefix_network_address_status multivalue_handle]
    
    set mv_ipv4_prefix_length_status [::ixiangpf::multivalue_config \
        -pattern                counter                     \
        -counter_start          32                          \
        -counter_step           0                           \
        -counter_direction      decrement                   \
        -nest_step              1,1                         \
        -nest_owner             $devicegroup,$topology      \
        -nest_enabled           0,0                         \
    ]
    if {[keylget mv_ipv4_prefix_length_status status] != $::SUCCESS} {
        error $mv_ipv4_prefix_length_status
    }
    set mv_ipv4_prefix_length [keylget mv_ipv4_prefix_length_status multivalue_handle]
    
    set network_group_status [::ixiangpf::emulation_ospf_network_group_config \
        -handle                               $ospf                             \
        -type                                 ipv4-prefix                       \
        -protocol_name                        $name                             \
        -multiplier                           1                                 \
        -enable_device                        1                                 \
        -connected_to_handle                  $ethernet                         \
        -ipv4_prefix_network_address          $mv_ipv4_prefix_network_address   \
        -ipv4_prefix_length                   $mv_ipv4_prefix_length            \
        -ipv4_prefix_number_of_addresses      1                                 \
        -ipv4_prefix_metric                   0                                 \
        -ipv4_prefix_active                   1                                 \
        -ipv4_prefix_allow_propagate          0                                 \
        -ipv4_prefix_route_origin             another_area                      \
    ]
    if {[keylget network_group_status status] != $::SUCCESS} {
        error $network_group_status
    }
    return [keylget network_group_status network_group_handle]
}
proc create_bgp {topology devicegroup networkgroup ipv4loopback remote_ip local_ip} {
    set mv_remote_ip_addr_status [::ixiangpf::multivalue_config \
        -pattern                counter                                 \
        -counter_start          $remote_ip                              \
        -counter_step           255.255.255.255                         \
        -counter_direction      decrement                               \
        -nest_step              0.0.0.1,0.0.0.1,0.0.0.1                 \
        -nest_owner             $networkgroup,$devicegroup,$topology    \
        -nest_enabled           0,0,0                                   \
    ]
    if {[keylget mv_remote_ip_addr_status status] != $::SUCCESS} {
        error $mv_remote_ip_addr_status
    }
    set mv_remote_ip_addr [keylget mv_remote_ip_addr_status multivalue_handle]
    
    set mv_local_router_id_status [::ixiangpf::multivalue_config \
        -pattern                counter                                 \
        -counter_start          $local_ip                               \
        -counter_step           0.0.0.1                                 \
        -counter_direction      increment                               \
        -nest_step              0.0.0.1,0.0.0.1,0.1.0.0                 \
        -nest_owner             $networkgroup,$devicegroup,$topology    \
        -nest_enabled           0,0,1                                   \
    ]
    if {[keylget mv_local_router_id_status status] != $::SUCCESS} {
        error $mv_local_router_id_status
    }
    set mv_local_router_id [keylget mv_local_router_id_status multivalue_handle]
    
    set bgp_ipv4_peer_status [::ixiangpf::emulation_bgp_config \
        -mode                                    enable                 \
        -md5_enable                              0                      \
        -handle                                  $ipv4loopback          \
        -remote_ip_addr                          $mv_remote_ip_addr     \
        -enable_4_byte_as                        0                      \
        -local_as                                0                      \
        -update_interval                         0                      \
        -count                                   1                      \
        -local_router_id                         $mv_local_router_id    \
        -hold_time                               90                     \
        -neighbor_type                           internal               \
        -graceful_restart_enable                 0                      \
        -restart_time                            45                     \
        -stale_time                              0                      \
        -tcp_window_size                         8192                   \
        -local_router_id_enable                  1                      \
        -ipv4_capability_mdt_nlri                1                      \
        -ipv4_capability_unicast_nlri            1                      \
        -ipv4_filter_unicast_nlri                1                      \
        -ipv4_capability_multicast_nlri          1                      \
        -ipv4_filter_multicast_nlri              1                      \
        -ipv4_capability_mpls_nlri               1                      \
        -ipv4_filter_mpls_nlri                   1                      \
        -ipv4_capability_mpls_vpn_nlri           1                      \
        -ipv4_filter_mpls_vpn_nlri               1                      \
        -ipv4_capability_multicast_vpn_nlri      1                      \
        -ipv4_filter_multicast_vpn_nlri          1                      \
        -ipv6_capability_unicast_nlri            1                      \
        -ipv6_filter_unicast_nlri                1                      \
        -ipv6_capability_multicast_nlri          1                      \
        -ipv6_filter_multicast_nlri              1                      \
        -ipv6_capability_mpls_nlri               1                      \
        -ipv6_filter_mpls_nlri                   1                      \
        -ipv6_capability_mpls_vpn_nlri           1                      \
        -ipv6_filter_mpls_vpn_nlri               1                      \
        -ipv6_capability_multicast_vpn_nlri      1                      \
        -ipv6_filter_multicast_vpn_nlri          1                      \
        -vpls_capability_nlri                    1                      \
        -vpls_filter_nlri                        1                      \
        -ttl_value                               64                     \
        -updates_per_iteration                   1                      \
        -bfd_registration                        0                      \
        -bfd_registration_mode                   multi_hop              \
        -act_as_restarted                        0                      \
        -discard_ixia_generated_routes           0                      \
        -flap_down_time                          0                      \
        -local_router_id_type                    same                   \
        -enable_flap                             0                      \
        -send_ixia_signature_with_routes         0                      \
        -flap_up_time                            0                      \
        -next_hop_enable                         0                      \
        -next_hop_ip                             0.0.0.0                \
        -advertise_end_of_rib                    0                      \
        -configure_keepalive_timer               0                      \
        -keepalive_timer                         30                     \
    ]
    if {[keylget bgp_ipv4_peer_status status] != $::SUCCESS} {
        error $bgp_ipv4_peer_status
    }
    return [list \
        [keylget bgp_ipv4_peer_status bgp_handle] \
        [keylget bgp_ipv4_peer_status handles] \
    ]
}
proc create_bgp_vpls {topology devicegroup networkgroup bgp_peer name} {
    set mv_rd_assign_value_status [::ixiangpf::multivalue_config \
        -pattern                counter                                 \
        -counter_start          1                                       \
        -counter_step           1                                       \
        -counter_direction      increment                               \
        -nest_step              1,1,0                                   \
        -nest_owner             $networkgroup,$devicegroup,$topology    \
        -nest_enabled           0,0,1                                   \
    ]
    if {[keylget mv_rd_assign_value_status status] != $::SUCCESS} {
        error $mv_rd_assign_value_status
    }
    set mv_rd_assign_value [keylget mv_rd_assign_value_status multivalue_handle]
    
    set mv_target_assign_status [::ixiangpf::multivalue_config \
        -pattern                counter                                 \
        -counter_start          1                                       \
        -counter_step           1                                       \
        -counter_direction      increment                               \
        -nest_step              1,1,0                                   \
        -nest_owner             $networkgroup,$devicegroup,$topology    \
        -nest_enabled           0,0,1                                   \
    ]
	if {[keylget mv_target_assign_status status] != $::SUCCESS} {
        error $mv_target_assign_status
    }
    set mv_target_assign [keylget mv_target_assign_status multivalue_handle]
	# set mv_l2_status [::ixiangpf::multivalue_config \
        # -pattern                counter                          \
		# -counter_start			a0.11.01.00.00.01					\
        # -counter_step           1                                       \
        # -counter_direction      increment                               \
		# -nest_step              0,0,0                                   \
        # -nest_owner             $networkgroup,$devicegroup,$topology    \
        # -nest_enabled           0,0,0                                   \
        # ]
    # if {[keylget mv_l2_status status] != $::SUCCESS} {
        # error $mv_l2_status
    # }
	# puts "...... [::ixia::keylprint mv_l2_status]"
    # set mv_l2 [keylget mv_l2_status multivalue_handle]
    #puts "mv_l2 = $mv_l2"
    set bgp_ipv4_l2_site_status [::ixiangpf::emulation_bgp_route_config \
        -handle                       $bgp_peer             \
        -mode                         add                   \
        -protocol_name                $name                 \
        -active                       1                     \
        -max_route_ranges             1                     \
        -num_sites                    1                     \
        -cluster_list_enable          0                     \
        -cluster_list                 0.0.0.0               \
        -vpls_nlri                    1                     \
        -rd_admin_value               100                   \
        -rd_assign_value              $mv_rd_assign_value   \
        -control_word_enable          0                     \
        -seq_delivery_enable          0                     \
        -mtu                          1500                  \
        -site_id                      1                     \
        -target                       100                   \
        -target_assign                $mv_target_assign     \
        -rd_type                      0                     \
        -target_type                  as                    \
        -advertise_label_block        1                     \
        -num_labels                   1000                  \
        -num_labels_type              single_value          \
        -label_block_offset           0                     \
        -label_block_offset_type      single_value          \
        -label_value                  16                    \
        -label_value_type             single_value          \
        ]
    if {[keylget bgp_ipv4_l2_site_status status] != $::SUCCESS} {
        error $bgp_ipv4_l2_site_status
    }
}

############################################
## configure bgp vpls device group on first port
############################################
set topology_1_handle [create_topology $ph_0 {Topology 1}]
set deviceGroup_1_handle [create_devicegroup $topology_1_handle {Device Group 1}]
set ethernet_1_handle [create_ethernet $topology_1_handle $deviceGroup_1_handle {Ethernet 1}]
set ipv4_1_handle [create_ipv4 \
    $topology_1_handle $ethernet_1_handle   \
    {IPv4 1}                                \
    100.1.0.2                               \
    100.1.0.1                               \
]
create_ldp $topology_1_handle $ipv4_1_handle 1.1.1.1
set ospfv2_1_handle [create_ospf \
    $topology_1_handle $ipv4_1_handle   \
    192.0.0.1                           \
    {OSPFv2-IF 1}                       \
]
set networkGroup_1_handle [create_ospf_ldp_network_group \
    $topology_1_handle $deviceGroup_1_handle $ethernet_1_handle $ospfv2_1_handle    \
    2.2.2.2                                                                         \
    {Network Group 1}                                                               \
]
set deviceGroup_2_handle [create_devicegroup_linked $networkGroup_1_handle {Device Group 4}]
set ipv4Loopback_1_handle [create_ipv4_loopback \
    $topology_1_handle $deviceGroup_2_handle $networkGroup_1_handle \
    2.2.2.2                                                         \
    {IPv4 Loopback 1}                                               \
]
set bgpIpv4Peer_1_list [create_bgp \
    $topology_1_handle $deviceGroup_2_handle $networkGroup_1_handle $ipv4Loopback_1_handle  \
    3.3.3.3                                                                                 \
    192.0.0.1                                                                               \
]
set bgpIpv4Peer_1_handle [lindex $bgpIpv4Peer_1_list 0]
set bgpIpv4Peer_1_items [lindex $bgpIpv4Peer_1_list 1]
create_bgp_vpls \
    $topology_1_handle $deviceGroup_2_handle $networkGroup_1_handle $bgpIpv4Peer_1_handle   \
    {BGP VPLS L2Site 2}

############################################
## configure bgp vpls device group on second port
############################################
set topology_2_handle [create_topology $ph_1 {Topology 2}]
set deviceGroup_3_handle [create_devicegroup $topology_2_handle {Device Group 2}]
set ethernet_2_handle [create_ethernet $topology_2_handle $deviceGroup_3_handle {Ethernet 2}]
set ipv4_2_handle [create_ipv4 \
    $topology_2_handle $ethernet_2_handle   \
    {IPv4 2}                                \
    100.1.0.1                               \
    100.1.0.2                               \
]
create_ldp $topology_2_handle $ipv4_2_handle 1.1.1.2
set ospfv2_2_handle [create_ospf \
    $topology_2_handle $ipv4_2_handle   \
    194.0.0.1                           \
    {OSPFv2-IF 2}                       \
]
set networkGroup_2_handle [create_ospf_ldp_network_group \
    $topology_2_handle $deviceGroup_3_handle $ethernet_2_handle $ospfv2_2_handle    \
    3.3.3.3                                                                         \
    {Network Group 2}                                                               \
]
set deviceGroup_4_handle [create_devicegroup_linked $networkGroup_2_handle {Device Group 4}]
set ipv4Loopback_2_handle [create_ipv4_loopback \
    $topology_2_handle $deviceGroup_4_handle $networkGroup_2_handle \
    3.3.3.3                                                         \
    {IPv4 Loopback 2}                                               \
]
set bgpIpv4Peer_2_list [create_bgp \
    $topology_2_handle $deviceGroup_4_handle $networkGroup_2_handle $ipv4Loopback_2_handle  \
    2.2.2.2                                                                                 \
    194.0.0.1                                                                               \
]
set bgpIpv4Peer_2_handle [lindex $bgpIpv4Peer_2_list 0]
set bgpIpv4Peer_2_items [lindex $bgpIpv4Peer_2_list 1]
create_bgp_vpls \
    $topology_2_handle $deviceGroup_4_handle $networkGroup_2_handle $bgpIpv4Peer_2_handle   \
    {BGP VPLS L2Site 2}

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
    set vpls_routes [keylget learned_info_1 $bgp_item.learned_info.vpls_routes]
    puts "$bgp_item vpls routes:"
    keylprint vpls_routes
}

set learned_info_2 [::ixiangpf::emulation_bgp_info   \
    -mode learned_info                  \
    -handle $bgpIpv4Peer_2_handle       \
]
if {[keylget learned_info_2 status] != $::SUCCESS} {
    error $learned_info_2
}
foreach bgp_item $bgpIpv4Peer_2_items {
    set vpls_routes [keylget learned_info_2 $bgp_item.learned_info.vpls_routes]
    puts "$bgp_item vpls routes:"
    keylprint vpls_routes
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
