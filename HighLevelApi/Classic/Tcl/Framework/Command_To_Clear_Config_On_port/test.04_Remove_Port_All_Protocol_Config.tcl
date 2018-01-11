#################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    02-20-2013 Mchakravarthy - created sample
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
#    This sample configures Port Interfaces, OSPF protocol and traffic on the  #
#    port and remove all the protocol config on the port                       #
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

################################################################################
# START - Connect to the chassis
################################################################################
puts "Starting - $test_name - [clock format [clock seconds]]"
puts "Start connecting to chassis ..."

set chassis_ip                  10.205.16.54
set port_list                   [list 2/5 2/6]
set break_locks                 1
set tcl_server                  127.0.0.1
set ixnetwork_tcl_server        127.0.0.1
set port_count                  2

set connect_status [::ixia::connect                                            \
            -reset                                                             \
            -device               $chassis_ip                                  \
            -port_list            $port_list                                   \
            -break_locks          $break_locks                                 \
            -tcl_server           $tcl_server                                  \
            -ixnetwork_tcl_server $ixnetwork_tcl_server                        \
            -interactive          1                                            \
            ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_handle [list]

foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}

set i 0
puts "Ixia port handles are:"
foreach port $port_handle {
    set port_$i $port
    puts $port    
    incr i
}

puts "End connecting to chassis ..."


################################################################################
# END - Connect to the chassis
################################################################################

################################################################################
# START - Interface configuration - Port 0
################################################################################
puts "Start interface configuration for Port:$port_0"

set interface_status_0 [::ixia::interface_config         \
        -port_handle                $port_0              \
        -l23_config_type            protocol_interface   \
        -ipv6_intf_addr             2000:0:0:0:1:0:0:1   \
        -ipv6_gateway               2000:0:0:0:1:0:0:2   \
        -vlan                       1                    \
        -vlan_id                    50,51                \
        -ipv6_prefix_length         64                   \
        -arp_on_linkup              1                    \
        -ns_on_linkup               1                    \
        -single_arp_per_gateway     1                    \
        -single_ns_per_gateway      1                    \
        -autonegotiation            1                    \
        -duplex                     auto                 \
        -speed                      auto                 \
        -intf_mode                  ethernet             ]
if {[keylget interface_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status_0 log]"
    return 0
}

set interface_handle_0 [keylget interface_status_0 interface_handle]
puts "interface_handle_0 $interface_handle_0"
puts "End interface configuration for Port:$port_0"

################################################################################
# START - Interface configuration - Port 1
################################################################################

puts "Start interface configuration for Port:$port_1"

set interface_status_1 [::ixia::interface_config      \
        -port_handle            $port_1               \
        -l23_config_type        protocol_interface    \
        -ipv6_intf_addr         2000:0:0:0:1:0:0:2    \
        -ipv6_gateway           2000:0:0:0:1:0:0:1    \
        -ipv6_prefix_length     64                    \
        -vlan                   1                     \
        -vlan_id                50,51                 \
        -arp_on_linkup          1                     \
        -ns_on_linkup           1                     \
        -single_arp_per_gateway 1                     \
        -single_ns_per_gateway  1                     \
        -autonegotiation        1                     \
        -duplex                 auto                  \
        -speed                  auto                  \
        -intf_mode              ethernet              ]
        
if {[keylget interface_status_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status_1 log]"
    return 0
}

set interface_handle_1 [keylget interface_status_1 interface_handle]
puts "Interface Handle: $interface_handle_1"
puts "End interface configuration for Port:$port_1"
################################################################################
# BGP Configuration
################################################################################

set bgp_router_status_1    [::ixia::emulation_bgp_config                 \
        -mode                           reset                            \
        -port_handle                    $port_0                          \
        -netmask                        24                               \
        -ip_version                     4                                \
        -retry_time                     120                              \
        -retries                        0                                \
        -local_as_mode                  fixed                            \
        -bfd_registration_mode          multi_hop                        \
        -local_router_id                2.2.2.2                          \
        -remote_loopback_ip_addr        1.1.1.1                          \
        -remote_ip_addr                 20.20.20.2                       \
        -bfd_registration               0                                \
        -local_router_id_enable         1                                \
        -hold_time                      90                               \
        -ipv4_mpls_nlri                 1                                \
        -ipv4_mpls_vpn_nlri             1                                \
        -ipv4_multicast_nlri            1                                \
        -ipv4_unicast_nlri              1                                \
        -ipv6_mpls_nlri                 1                                \
        -ipv6_mpls_vpn_nlri             1                                \
        -ipv6_multicast_nlri            1                                \
        -ipv6_unicast_nlri              1                                \
        -local_as                       100                              \
        -local_loopback_ip_addr         2.2.2.2                          \
        -local_ip_addr                  20.20.20.1                       \
        -next_hop_ip                    0.0.0.0                          \
        -updates_per_iteration          1                                \
        -restart_time                   45                               \
        -staggered_start_time           0                                \
        -stale_time                     0                                \
        -tcp_window_size                8192                             \
        -neighbor_type                  internal                         \
        -update_interval                0                                \
        -vpls                           disabled                         ]
        
#Check status
if {[keylget bgp_router_status_1 status] != $::SUCCESS}   {
    puts "FAIL - $test_name - [keylget bgp_router_status_1 log]"
return 0
}

set bgp_handles_1 [keylget bgp_router_status_1 handles]



set bgp_routes_status_1    [::ixia::emulation_bgp_route_config              \
        -mode                            add                                \
        -handle                          $bgp_handles_1                     \
        -num_sites                       1                                  \
        -as_path                         {}                                 \
        -label_value                     16                                 \
        -label_incr_mode                 rd                                 \
        -label_step                      1                                  \
        -import_target_type              as                                 \
        -import_target                   100                                \
        -import_target_assign            1                                  \
        -target_type                     as                                 \
        -target                          100                                \
        -target_assign                   1                                  \
        -rd_admin_value                  100                                \
        -rd_assign_value                 1                                  \
        -rd_type                         0                                  \
        -next_hop_enable                 1                                  \
        -origin_route_enable             1                                  \
        -enable_traditional_nlri         1                                  \
        -ipv4_mpls_vpn_nlri              1                                  \
        -ipv6_mpls_vpn_nlri              1                                  \
        -packing_from                    0                                  \
        -prefix_from                     24                                 \
        -ip_version                      4                                  \
        -prefix_step                     1                                  \
        -local_pref                      0                                  \
        -prefix                          22.22.1.0                          \
        -next_hop                        0.0.0.0                            \
        -next_hop_mode                   increment                          \
        -next_hop_set_mode               same                               \
        -num_routes                      50                                 \
        -origin                          igp                                \
        -originator_id                   0.0.0.0                            \
        -packing_to                      0                                  \
        -prefix_to                       24                                 ]
        
#Check status
if {[keylget bgp_routes_status_1 status] != $::SUCCESS}   {
    puts "FAIL - $test_name - [keylget bgp_routes_status_1 log]"
return 0
}

set vpn_sources [keylget bgp_routes_status_1 bgp_routes]



set bgp_router_status_2    [::ixia::emulation_bgp_config                 \
        -mode                           reset                            \
        -port_handle                    $port_1                          \
        -netmask                        24                               \
        -ip_version                     4                                \
        -retry_time                     120                              \
        -retries                        0                                \
        -local_as_mode                 fixed                             \
        -bfd_registration_mode         multi_hop                         \
        -local_router_id               1.1.1.1                           \
        -remote_loopback_ip_addr       2.2.2.2                           \
        -remote_ip_addr                20.20.20.1                        \
        -bfd_registration              0                                 \
        -local_router_id_enable        1                                 \
        -hold_time                     90                                \
        -ipv4_mpls_nlri                1                                 \
        -ipv4_mpls_vpn_nlri            1                                 \
        -ipv4_multicast_nlri           1                                 \
        -ipv4_unicast_nlri             1                                 \
        -ipv6_mpls_nlri                1                                 \
        -ipv6_mpls_vpn_nlri            1                                 \
        -ipv6_multicast_nlri           1                                 \
        -ipv6_unicast_nlri             1                                 \
        -local_as                      100                               \
        -local_loopback_ip_addr        1.1.1.1                           \
        -local_ip_addr                 20.20.20.2                        \
        -next_hop_ip                   0.0.0.0                           \
        -updates_per_iteration         1                                 \
        -restart_time                  45                                \
        -staggered_start_time          0                                 \
        -stale_time                    0                                 \
        -tcp_window_size               8192                              \
        -neighbor_type                 internal                          \
        -update_interval               0                                 \
        -vpls                          disabled                          ]
        
#Check status
if {[keylget bgp_router_status_2 status] != $::SUCCESS}   {
    puts "FAIL - $test_name - [keylget bgp_router_status_2 log]"
return 0
}

set bgp_handles_2 [keylget bgp_router_status_2 handles]



set bgp_routes_status_2    [::ixia::emulation_bgp_route_config             \
        -mode                           add                                \
        -handle                         $bgp_handles_2                     \
        -num_sites                      1                                  \
        -as_path                        {}                                 \
        -label_value                    16                                 \
        -label_incr_mode                rd                                 \
        -label_step                     1                                  \
        -import_target_type             as                                 \
        -import_target                  100                                \
        -import_target_assign           1                                  \
        -target_type                    as                                 \
        -target                         100                                \
        -target_assign                  1                                  \
        -rd_admin_value                 100                                \
        -rd_assign_value                1                                  \
        -rd_type                        0                                  \
        -next_hop_enable                1                                  \
        -origin_route_enable            1                                  \
        -enable_traditional_nlri        1                                  \
        -ipv4_mpls_vpn_nlri             1                                  \
        -ipv6_mpls_vpn_nlri             1                                  \
        -packing_from                   0                                  \
        -prefix_from                    24                                 \
        -ip_version                     4                                  \
        -prefix_step                    1                                  \
        -local_pref                     0                                  \
        -prefix                         32.22.1.0                          \
        -next_hop                       0.0.0.0                            \
        -next_hop_mode                  increment                          \
        -next_hop_set_mode              same                               \
        -num_routes                     50                                 \
        -origin                         igp                                \
        -originator_id                  0.0.0.0                            \
        -packing_to                     0                                  \
        -prefix_to                      24                                 ]
        
#Check status
if {[keylget bgp_routes_status_2 status] != $::SUCCESS}   {
    puts "FAIL - $test_name - [keylget bgp_routes_status_2 log]"
    return 0
}

set vpn_destinations [keylget bgp_routes_status_2 bgp_routes]


################################################################################
# Configure an IS-IS emulated router on each port                              #
################################################################################
set isis_router_handle_list [list]
set local_ip_address_temp   [list 20.20.20.1 20.20.20.2]
set gateway_ip_address_temp [list 20.20.20.2 20.20.20.1]
for {set i 0} {$i < $port_count} {incr i} {
    set isis_router_status [::ixia::emulation_isis_config                   \
            -mode                   create                                  \
            -reset                                                          \
            -port_handle            [subst $[subst port_$i]]                \
            -ip_version             4                                       \
            -system_id              "00 00 00 00 0$i 00"                    \
            -intf_ip_addr           [lindex $local_ip_address_temp $i]      \
            -gateway_ip_addr        [lindex $gateway_ip_address_temp $i]    \
            -intf_ip_prefix_length  24                                      \
            -count                  1                                       \
            -routing_level          L1L2                                    \
            -loopback_ip_addr_count 0                                       \
            ]
    if {[keylget isis_router_status status] != $::SUCCESS} {
        return "FAIL - [keylget isis_router_status log]"
    }
    lappend isis_router_handle_list [keylget isis_router_status handle]
}

################################################################################
#  For each IS-IS router, configure a route range                              #
################################################################################
set route_range_ip_address_temp   [list 100.10.0.0 100.20.0.0]
set route_range_list [list ]
for {set i 0} {$i < $port_count} {incr i} {
    set isis_router_handle [lindex $isis_router_handle_list $i]
    set route_config_status [::ixia::emulation_isis_topology_route_config        \
            -mode                   create                                       \
            -handle                 $isis_router_handle                          \
            -type                   stub                                         \
            -ip_version             4                                            \
            -stub_ip_start          [lindex $route_range_ip_address_temp $i]     \
            -stub_ip_step           0.0.8.0                                      \
            -stub_ip_pfx_len        24                                           \
            -stub_count             2                                            \
            -stub_metric            22                                           \
            ]
    if {[keylget route_config_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget route_config_status log]"
    }
    set route_ranges [lindex [lindex [keylget route_config_status elem_handle] 0] 1]
    lappend route_range_list [lindex $route_ranges 0] [lindex $route_ranges 1]
  
}

################################################################################
# RSVP Configuration - Port 0
################################################################################

set rsvp_router_status_1 [::ixia::emulation_rsvp_config                   \
        -mode                               create                        \
        -port_handle                        $port_0                       \
        -count                              1                             \
        -ip_version                         4                             \
        -egress_label_mode                  exnull                        \
        -record_route                       1                             \
        -resv_state_refresh_timeout         30000                         \
        -resv_confirm                       0                             \
        -resv_state_timeout_count           3                             \
        -path_state_refresh_timeout         30000                         \
        -path_state_timeout_count           3                             \
        -enable_bgp_over_lsp                1                             \
        -actual_restart_time                15000                         \
        -neighbor_intf_ip_addr              11.1.1.2                      \
        -graceful_restart                   0                             \
        -hello_msgs                         0                             \
        -intf_prefix_length                 24                            \
        -vlan                               0                             \
        -vlan_id                            1                             \
        -vlan_user_priority                 0                             \
        -graceful_restart_start_time        30000                         \
        -graceful_restart_up_time           30000                         \
        -hello_interval                     5                             \
        -hello_retry_count                  3                             \
        -max_label_value                    100000                        \
        -min_label_value                    1000                          \
        -graceful_restarts_count            0                             \
        -intf_ip_addr                       11.1.1.1                      \
        -graceful_restart_recovery_time     30000                         \
        -refresh_reduction                  0                             \
        -graceful_restart_restart_time      30000                         \
        -srefresh_interval                  30000                         ]
    
#Check status
if {[keylget rsvp_router_status_1 status] != $::SUCCESS}   {
    puts "FAIL - $test_name - [keylget rsvp_router_status_1 log]"
    return 0
}

set rsvp_router_handle_1 [keylget rsvp_router_status_1 handles]

set rsvp_tunnel_status_1 [::ixia::emulation_rsvp_tunnel_config            \
        -mode                                create                       \
        -handle                              $rsvp_router_handle_1        \
        -count                               1                            \
        -egress_leaf_range_count             1                            \
        -egress_leaf_ip_count                1                            \
        -ingress_bandwidth                   0                            \
        -session_attr_bw_protect             0                            \
        -fast_reroute                        0                            \
        -session_attr_resource_affinities    0                            \
        -session_attr_ra_exclude_any         0                            \
        -fast_reroute_bandwidth              0                            \
        -avoid_node_id                       {}                           \
        -plr_id                              {}                           \
        -fast_reroute_exclude_any            0                            \
        -facility_backup                     0                            \
        -fast_reroute_holding_priority       7                            \
        -fast_reroute_hop_limit              3                            \
        -fast_reroute_include_all            0                            \
        -fast_reroute_include_any            0                            \
        -one_to_one_backup                   0                            \
        -send_detour                         0                            \
        -fast_reroute_setup_priority         7                            \
        -session_attr_hold_priority          7                            \
        -session_attr_ra_include_all         0                            \
        -session_attr_ra_include_any         0                            \
        -ingress_ip_addr                     2.2.2.2                      \
        -session_attr_label_record           0                            \
        -session_attr_local_protect          1                            \
        -lsp_id_count                        1                            \
        -lsp_id_start                        1                            \
        -sender_tspec_max_pkt_size           0                            \
        -sender_tspec_min_policed_size       0                            \
        -session_attr_node_protect           0                            \
        -sender_tspec_peak_data_rate         0                            \
        -session_attr_se_style               1                            \
        -session_attr_setup_priority         7                            \
        -sender_tspec_token_bkt_rate         0                            \
        -sender_tspec_token_bkt_size         0                            \
        -ero                                 0                            \
        -rro                                 0                            \
        -tunnel_id_count                     1                            \
        -tunnel_id_start                     1                            \
        -rsvp_behavior                       rsvpIngress                  \
        -emulation_type                      rsvpte                       \
        -egress_ip_addr                      1.1.1.1                      \
        -enable_append_connected_ip          1                            \
        -enable_prepend_tunnel_head_ip       1                            \
        -enable_prepend_tunnel_leaf_ip       1                            \
        -enable_send_as_rro                  1                            \
        -enable_send_as_srro                 0                            ]
        
#Check status
if {[keylget rsvp_tunnel_status_1 status] != $::SUCCESS}   {
    puts "FAIL - $test_name - [keylget rsvp_tunnel_status_1 log]"
    return 0
}

set rsvp_tunnel_status_2 [::ixia::emulation_rsvp_tunnel_config            \
        -mode                                create                       \
        -handle                              $rsvp_router_handle_1        \
        -count                               1                            \
        -egress_leaf_range_count             1                            \
        -egress_leaf_ip_count                1                            \
        -ingress_bandwidth                   0                            \
        -egress_behavior                     always_use_configured_style  \
        -reservation_style                   se                           \
        -rsvp_behavior                       rsvpEgress                   \
        -emulation_type                      rsvpte                       \
        -egress_ip_addr                      2.2.2.2                      \
        -enable_append_connected_ip          1                            \
        -enable_prepend_tunnel_head_ip       1                            \
        -enable_prepend_tunnel_leaf_ip       1                            \
        -enable_send_as_rro                  1                            \
        -enable_send_as_srro                 0                            ]
        
#Check status
if {[keylget rsvp_tunnel_status_2 status] != $::SUCCESS}   {
    puts "FAIL - $test_name - [keylget rsvp_tunnel_status_2 log]"
    return 0
}


################################################################################
# RSVP Configuration - Port 1
################################################################################

set rsvp_router_status_2 [::ixia::emulation_rsvp_config                  \
        -mode                               create                       \
        -port_handle                        $port_1                      \
        -count                              1                            \
        -ip_version                         4                            \
        -egress_label_mode                  exnull                       \
        -record_route                       1                            \
        -resv_state_refresh_timeout         30000                        \
        -resv_confirm                       0                            \
        -resv_state_timeout_count           3                            \
        -path_state_refresh_timeout         30000                        \
        -path_state_timeout_count           3                            \
        -enable_bgp_over_lsp                1                            \
        -actual_restart_time                15000                        \
        -neighbor_intf_ip_addr              11.1.1.1                     \
        -graceful_restart                   0                            \
        -hello_msgs                         0                            \
        -intf_prefix_length                 24                           \
        -vlan                               0                            \
        -vlan_id                            1                            \
        -vlan_user_priority                 0                            \
        -graceful_restart_start_time        30000                        \
        -graceful_restart_up_time           30000                        \
        -hello_interval                     5                            \
        -hello_retry_count                  3                            \
        -max_label_value                    100000                       \
        -min_label_value                    1000                         \
        -graceful_restarts_count            0                            \
        -intf_ip_addr                       11.1.1.2                     \
        -graceful_restart_recovery_time     30000                        \
        -refresh_reduction                  0                            \
        -graceful_restart_restart_time      30000                        \
        -srefresh_interval                  30000                        ]
    
#Check status
if {[keylget rsvp_router_status_2 status] != $::SUCCESS}   {
    puts "FAIL - $test_name - [keylget rsvp_router_status_2 log]"
    return 0
}

set rsvp_router_handle_2 [keylget rsvp_router_status_2 handles]

set rsvp_tunnel_status_3 [::ixia::emulation_rsvp_tunnel_config            \
        -mode                                create                       \
        -handle                              $rsvp_router_handle_2        \
        -count                               1                            \
        -egress_leaf_range_count             1                            \
        -egress_leaf_ip_count                1                            \
        -ingress_bandwidth                   0                            \
        -session_attr_bw_protect             0                            \
        -fast_reroute                        0                            \
        -session_attr_resource_affinities    0                            \
        -session_attr_ra_exclude_any         0                            \
        -fast_reroute_bandwidth              0                            \
        -avoid_node_id                       {}                           \
        -plr_id                              {}                           \
        -fast_reroute_exclude_any            0                            \
        -facility_backup                     0                            \
        -fast_reroute_holding_priority       7                            \
        -fast_reroute_hop_limit              3                            \
        -fast_reroute_include_all            0                            \
        -fast_reroute_include_any            0                            \
        -one_to_one_backup                   0                            \
        -send_detour                         0                            \
        -fast_reroute_setup_priority         7                            \
        -session_attr_hold_priority          7                            \
        -session_attr_ra_include_all         0                            \
        -session_attr_ra_include_any         0                            \
        -ingress_ip_addr                     1.1.1.1                      \
        -session_attr_label_record           0                            \
        -session_attr_local_protect          1                            \
        -lsp_id_count                        1                            \
        -lsp_id_start                        1                            \
        -sender_tspec_max_pkt_size           0                            \
        -sender_tspec_min_policed_size       0                            \
        -session_attr_node_protect           0                            \
        -sender_tspec_peak_data_rate         0                            \
        -session_attr_se_style               1                            \
        -session_attr_setup_priority         7                            \
        -sender_tspec_token_bkt_rate         0                            \
        -sender_tspec_token_bkt_size         0                            \
        -ero                                 0                            \
        -rro                                 0                            \
        -tunnel_id_count                     1                            \
        -tunnel_id_start                     1                            \
        -rsvp_behavior                       rsvpIngress                  \
        -emulation_type                      rsvpte                       \
        -egress_ip_addr                      2.2.2.2                      \
        -enable_append_connected_ip          1                            \
        -enable_prepend_tunnel_head_ip       1                            \
        -enable_prepend_tunnel_leaf_ip       1                            \
        -enable_send_as_rro                  1                            \
        -enable_send_as_srro                 0                            ]
        
#Check status
if {[keylget rsvp_tunnel_status_3 status] != $::SUCCESS}   {
    puts "FAIL - $test_name - [keylget rsvp_tunnel_status_3 log]"
    return 0
}

set rsvp_tunnel_status_4 [::ixia::emulation_rsvp_tunnel_config            \
        -mode                                create                       \
        -handle                              $rsvp_router_handle_2        \
        -count                               1                            \
        -egress_leaf_range_count             1                            \
        -egress_leaf_ip_count                1                            \
        -ingress_bandwidth                   0                            \
        -egress_behavior                     always_use_configured_style  \
        -reservation_style                   se                           \
        -rsvp_behavior                       rsvpEgress                   \
        -emulation_type                      rsvpte                       \
        -egress_ip_addr                      1.1.1.1                      \
        -enable_append_connected_ip          1                            \
        -enable_prepend_tunnel_head_ip       1                            \
        -enable_prepend_tunnel_leaf_ip       1                            \
        -enable_send_as_rro                  1                            \
        -enable_send_as_srro                 0                            ]
        
#Check status
if {[keylget rsvp_tunnel_status_4 status] != $::SUCCESS}   {
    puts "FAIL - $test_name - [keylget rsvp_tunnel_status_4 log]"
    return 0
}

################################################################################
# Start BGP on both ports                                                      #
################################################################################
set bgp_emulation_status [::ixia::emulation_bgp_control                     \
        -port_handle        $port_0                                         \
        -mode               start                                           \
        ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_emulation_status log]"
    return 0
}

set bgp_emulation_status [::ixia::emulation_bgp_control                     \
        -port_handle        $port_1                                         \
        -mode               start                                           \
        ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_emulation_status log]"
    return 0
}

after 1000

################################################################################
# Start IS-IS                                                                  #
################################################################################
for {set i 0} {$i < $port_count} {incr i} {
    set isis_router_handle [lindex $isis_router_handle_list $i]
    set isis_emulation_status [::ixia::emulation_isis_control                    \
            -handle             $isis_router_handle                              \
            -mode               start                                            \
            ]
    if {[keylget isis_emulation_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget isis_emulation_status log]"
    }
}


################################################################################
# Start RSVP on both ports                                                     #
################################################################################
set rsvp_emulation_status [::ixia::emulation_rsvp_control                    \
        -port_handle        $port_0                                          \
        -mode               start                                            \
        ]
if {[keylget rsvp_emulation_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget rsvp_emulation_status log]"
    return 0
}

set rsvp_emulation_status [::ixia::emulation_rsvp_control                    \
        -port_handle        $port_1                                          \
        -mode               start                                            \
        ]
if {[keylget rsvp_emulation_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget rsvp_emulation_status log]"
    return 0
}

for {set i 0} {$i < 20} {incr i} {

set rsvp_stats_handle_1 [::ixia::emulation_rsvp_info                        \
        -mode                       stats                                   \
        -port_handle                $port_1                                 \
        -handle                     [keylget rsvp_router_status_1 handles]  ]

if {[keylget rsvp_stats_handle_1 status] != $SUCCESS} {
    errMsg "FAIL - $test_name - [keylget rsvp_stats_handle_1 log]"
    return 0
}

#puts "lsp_count : [keylget rsvp_stats_handle_1 lsp_count]"
#puts "num_lsp_setup : [keylget rsvp_stats_handle_1 num_lsp_setup]"
#puts "peer_count : [keylget rsvp_stats_handle_1 peer_count]"
#puts "status : [keylget rsvp_stats_handle_1 status]"
set total_lsp_count [keylget rsvp_stats_handle_1 total_lsp_count]
puts "total_lsp_count : $total_lsp_count"


if {$total_lsp_count == 2 } {
    break
}
set rsvp_stats_handle_2 [::ixia::emulation_rsvp_info                        \
        -mode                       stats                                   \
        -port_handle                $port_1                                 \
        -handle                     [keylget rsvp_router_status_2 handles]  ]

if {[keylget rsvp_stats_handle_2 status] != $SUCCESS} {
    errMsg "FAIL - $test_name - [keylget rsvp_stats_handle_2 log]"
    return 0
}

set total_lsp_count [keylget rsvp_stats_handle_2 total_lsp_count]
puts "total_lsp_count : $total_lsp_count"

if {$total_lsp_count == 2 } {
    break
}
after 1000
}

################################################################################
# Wait for the routes to be learned                                            #
################################################################################
after 30000

################################################################################
# Delete all the streams first
################################################################################
set traffic_status [::ixia::traffic_config \
        -mode        reset                 \
        -port_handle $port_handle          \
        -traffic_generator ixnetwork_540   ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

################################################################################
# Configure the IPv4 Traffic - 1
################################################################################

set rate_start_value        50
set frame_size_start        512


set src_handle [lindex $route_range_list 0]
puts "SRC: $src_handle"
set dst_handle [lindex $route_range_list 2]
puts "DST: $dst_handle"
set traffic_status_1 [::ixia::traffic_config                                    \
            -traffic_generator                   ixnetwork_540                  \
            -circuit_endpoint_type               ipv4                           \
            -mode                                create                         \
            -emulation_src_handle                $src_handle                    \
            -emulation_dst_handle                $dst_handle                    \
            -name                                "Flow_Traffic"                 \
            -src_dest_mesh                       one_to_one                     \
            -route_mesh                          one_to_one                     \
            -rate_percent                        $rate_start_value              \
            -frame_size                          $frame_size_start              \
            -l3_protocol                         ipv4                           \
            -latency_bins_enable                 1                              \
            -latency_bins                        2                              \
            -latency_values                      {0}                            \
            -track_by                            src_mac                        \
            -frame_sequencing                    enable                         \
            -frame_sequencing_mode               rx_threshold                   \
            -egress_tracking                     outer_vlan_id_4                ]

if {[keylget traffic_status_1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status_1 log]"
}


################################################################################
# Port Set Factory Defaults
################################################################################

set reset_result [::ixia::reset_port                    \
        -mode               remove_protocol             \
        -port_handle        [list $port_0]              \
        -protocol           all                         ]
        
if {[keylget reset_result status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget reset_result log]"
    return 0
}

############################### SUCCESS or FAILURE #############################

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1

################################################################################


