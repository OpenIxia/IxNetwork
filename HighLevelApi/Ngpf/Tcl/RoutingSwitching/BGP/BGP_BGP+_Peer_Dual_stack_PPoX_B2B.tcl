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
#    This sample configures BGP and BGP+ Peers over PPoX Client and Server     #
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


proc setup_topology {name port_handle} {
    set topology_status [::ixiangpf::topology_config \
        -topology_name      $name             \
        -port_handle        $port_handle      \
    ]
    if {[keylget topology_status status] != $::SUCCESS} {
        error $topology_status
    }
    return [keylget topology_status topology_handle]
}

################################################################################
# START - Connect to the chassis
################################################################################
puts "Starting - $test_name - [clock format [clock seconds]]"
puts "Start connecting to chassis ..."
set chassis_ip              10.216.108.123
set port_list               [list 2/5 2/6]
set break_locks             1
set tcl_server              10.216.108.123
set ixnetwork_tcl_server    10.216.108.49:8500
set port_count              2
set cfgErrors               0

set rval [ixia::connect                             \
    -reset                                          \
    -device                 $chassis_ip             \
    -port_list              $port_list              \
    -ixnetwork_tcl_server   $ixnetwork_tcl_server   \
    -tcl_server             $tcl_server             \
]
if {[keylget rval status] != $::SUCCESS} {
    error "connect failed: [keylget rval log]"
}

set port_1 [keylget rval port_handle.$chassis_ip.[lindex $port_list 0]]
set port_2 [keylget rval port_handle.$chassis_ip.[lindex $port_list 1]]

set port_list [list $port_1 $port_2]

#########################################################################################################################
##                                                     Topology 1 Config                                               ##
#########################################################################################################################

set topology_1_handle [setup_topology "Topology 1" $port_1]

#########################################################################################################################
##                                                     Device Group 1 Config                                           ##
#########################################################################################################################

set device_group_1_status [::ixiangpf::topology_config \
    -topology_handle              $topology_1_handle      \
    -device_group_name            {Device Group 1}        \
    -device_group_multiplier      1                       \
    -device_group_enabled         1                       \
]
if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "[info script] $device_group_1_status"
}
set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

############################################
## Ethernet Config
############################################

set multivalue_1_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.11.01.00.00.01       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_1_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_1_status"
}
set multivalue_1_handle [keylget multivalue_1_status multivalue_handle]

set ethernet_1_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 1}               \
    -protocol_handle              $deviceGroup_1_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_1_handle       \
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
if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "[info script] $ethernet_1_status"
}
set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]

############################################
## PPoX Server Config
############################################

set multivalue_2_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          1                       \
    -counter_step           0                       \
    -counter_direction      increment               \
    -nest_step              1                       \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           0                       \
]
if {[keylget multivalue_2_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_2_status"
}
set multivalue_2_handle [keylget multivalue_2_status multivalue_handle]

set multivalue_3_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          1.1.1.2                 \
    -counter_step           0.0.1.0                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_3_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_3_status"
}
set multivalue_3_handle [keylget multivalue_3_status multivalue_handle]

set multivalue_4_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          1.1.1.1                 \
    -counter_step           0.0.1.0                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_4_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_4_status"
}
set multivalue_4_handle [keylget multivalue_4_status multivalue_handle]

set multivalue_5_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          11:0:0:0:0:0:0:11       \
    -counter_step           0:0:1:0:0:0:0:0         \
    -counter_direction      increment               \
    -nest_step              0:1:0:0:0:0:0:0         \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_5_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_5_status"
}
set multivalue_5_handle [keylget multivalue_5_status multivalue_handle]

set multivalue_6_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          11:0:0:0:0:0:0:11       \
    -counter_step           0:0:0:1:0:0:0:0         \
    -counter_direction      increment               \
    -nest_step              0:0:1:0:0:0:0:0         \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_6_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_6_status"
}
set multivalue_6_handle [keylget multivalue_6_status multivalue_handle]

set multivalue_7_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          11:0:0:0:0:0:0:1        \
    -counter_step           0:0:0:1:0:0:0:0         \
    -counter_direction      increment               \
    -nest_step              0:0:1:0:0:0:0:0         \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_7_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_7_status"
}
set multivalue_7_handle [keylget multivalue_7_status multivalue_handle]

set multivalue_8_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          2001:0:0:0:0:0:0:1      \
    -counter_step           0:0:0:1:0:0:0:0         \
    -counter_direction      increment               \
    -nest_step              0:0:1:0:0:0:0:0         \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_8_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_8_status"
}
set multivalue_8_handle [keylget multivalue_8_status multivalue_handle]

set pppoxserver_1_status [::ixiangpf::pppox_config \
    -port_role                            network                   \
    -handle                               $ethernet_1_handle        \
    -protocol_name                        {PPPoX Server 1}          \
    -enable_mru_negotiation               0                         \
    -desired_mru_rate                     1492                      \
    -enable_max_payload                   0                         \
    -server_ipv6_ncp_configuration        clientmay                 \
    -server_ipv4_ncp_configuration        clientmay                 \
    -lcp_enable_accm                      0                         \
    -lcp_accm                             ffffffff                  \
    -num_sessions                         1                         \
    -auth_req_timeout                     10                        \
    -config_req_timeout                   10                        \
    -echo_req                             $multivalue_2_handle      \
    -echo_rsp                             1                         \
    -ip_cp                                dual_stack                \
    -ipcp_req_timeout                     10                        \
    -max_auth_req                         20                        \
    -max_terminate_req                    3                         \
    -password                             password                  \
    -chap_secret                          secret                    \
    -username                             user                      \
    -chap_name                            user                      \
    -mode                                 add                       \
    -auth_mode                            none                      \
    -echo_req_interval                    10                        \
    -max_configure_req                    3                         \
    -max_ipcp_req                         3                         \
    -ac_name                              ixia                      \
    -enable_domain_group_map              0                         \
    -enable_server_signal_iwf             0                         \
    -enable_server_signal_loop_char       0                         \
    -enable_server_signal_loop_encap      0                         \
    -enable_server_signal_loop_id         0                         \
    -ipv6_pool_prefix_len                 48                        \
    -ipv6_pool_prefix                     $multivalue_5_handle      \
    -ipv6_pool_addr_prefix_len            64                        \
    -ppp_local_iid                        $multivalue_7_handle      \
    -ppp_local_ip                         $multivalue_4_handle      \
    -ppp_local_ip_step                    0.0.0.1                   \
    -ppp_peer_iid                         $multivalue_6_handle      \
    -ppp_peer_ip                          $multivalue_3_handle      \
    -send_dns_options                     0                         \
    -dns_server_list                      $multivalue_8_handle      \
    -server_dns_options                   disable_extension         \
    -server_dns_primary_address           10.10.10.10               \
    -server_dns_secondary_address         11.11.11.11               \
    -server_netmask_options               disable_extension         \
    -server_netmask                       255.255.255.0             \
    -server_wins_options                  disable_extension         \
    -server_wins_primary_address          10.10.10.10               \
    -server_wins_secondary_address        11.11.11.11               \
    -accept_any_auth_value                0                         \
]
if {[keylget pppoxserver_1_status status] != $::SUCCESS} {
    puts "[info script] $pppoxserver_1_status"
}
set pppoxserver_1_handle [keylget pppoxserver_1_status pppox_server_handle]

############################################
## BGP Peer Config
############################################

set multivalue_9_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          192.0.0.1               \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_9_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_9_status"
}
set multivalue_9_handle [keylget multivalue_9_status multivalue_handle]

set multivalue_10_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          1                       \
    -counter_step           0                       \
    -counter_direction      increment               \
    -nest_step              1                       \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           0                       \
]
if {[keylget multivalue_10_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_10_status"
}
set multivalue_10_handle [keylget multivalue_10_status multivalue_handle]

set bgp_ipv4_peer_1_status [::ixiangpf::emulation_bgp_config \
    -mode                                    enable                     \
    -md5_enable                              0                          \
    -handle                                  $pppoxserver_1_handle      \
    -remote_ip_addr                          1.1.1.2                    \
    -remote_addr_step                        0.0.0.0                    \
    -enable_4_byte_as                        0                          \
    -local_as                                1                          \
    -update_interval                         0                          \
    -count                                   1                          \
    -local_router_id                         $multivalue_9_handle       \
    -hold_time                               90                         \
    -neighbor_type                           external                   \
    -graceful_restart_enable                 0                          \
    -restart_time                            45                         \
    -stale_time                              0                          \
    -tcp_window_size                         8192                       \
    -local_router_id_enable                  1                          \
    -ipv4_capability_mdt_nlri                0                          \
    -ipv4_capability_unicast_nlri            1                          \
    -ipv4_filter_unicast_nlri                $multivalue_10_handle      \
    -ipv4_capability_multicast_nlri          1                          \
    -ipv4_filter_multicast_nlri              0                          \
    -ipv4_capability_mpls_nlri               1                          \
    -ipv4_filter_mpls_nlri                   0                          \
    -ipv4_capability_mpls_vpn_nlri           1                          \
    -ipv4_filter_mpls_vpn_nlri               0                          \
    -ipv6_capability_unicast_nlri            1                          \
    -ipv6_filter_unicast_nlri                0                          \
    -ipv6_capability_multicast_nlri          1                          \
    -ipv6_filter_multicast_nlri              0                          \
    -ipv6_capability_mpls_nlri               1                          \
    -ipv6_filter_mpls_nlri                   0                          \
    -ipv6_capability_mpls_vpn_nlri           1                          \
    -ipv6_filter_mpls_vpn_nlri               0                          \
    -ttl_value                               64                         \
    -updates_per_iteration                   1                          \
    -bfd_registration                        0                          \
    -bfd_registration_mode                   multi_hop                  \
    -vpls_capability_nlri                    1                          \
    -vpls_filter_nlri                        0                          \
    -act_as_restarted                        0                          \
    -discard_ixia_generated_routes           0                          \
    -flap_down_time                          0                          \
    -local_router_id_type                    same                       \
    -enable_flap                             0                          \
    -send_ixia_signature_with_routes         0                          \
    -flap_up_time                            0                          \
    -next_hop_enable                         0                          \
    -next_hop_ip                             0.0.0.0                    \
    -ipv4_capability_multicast_vpn_nlri      0                          \
    -ipv4_filter_multicast_vpn_nlri          0                          \
    -ipv6_capability_multicast_vpn_nlri      0                          \
    -ipv6_filter_multicast_vpn_nlri          0                          \
    -advertise_end_of_rib                    0                          \
    -configure_keepalive_timer               0                          \
    -keepalive_timer                         30                         \
]

if {[keylget bgp_ipv4_peer_1_status status] != $::SUCCESS} {
    puts "[info script] $bgp_ipv4_peer_1_status"
}
set bgpIpv4Peer_1_handle [keylget bgp_ipv4_peer_1_status bgp_handle]

############################################
## BGP+ Peer Config
############################################

set multivalue_11_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          192.0.0.1               \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_11_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_11_status"
}
set multivalue_11_handle [keylget multivalue_11_status multivalue_handle]

set multivalue_12_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          1                       \
    -counter_step           0                       \
    -counter_direction      increment               \
    -nest_step              1                       \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           0                       \
]
if {[keylget multivalue_12_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_12_status"
}
set multivalue_12_handle [keylget multivalue_12_status multivalue_handle]

set bgp_ipv6_peer_1_status [::ixiangpf::emulation_bgp_config \
    -mode                                    enable                     \
    -md5_enable                              0                          \
    -ip_version                              6                          \
    -handle                                  $pppoxserver_1_handle      \
    -remote_ipv6_addr                        11:0:0:0:11:1111:0:1      \
    -remote_addr_step                        0:0:0:0:0:0:0:0            \
    -enable_4_byte_as                        0                          \
    -local_as                                3                          \
    -update_interval                         0                          \
    -count                                   1                          \
    -local_router_id                         $multivalue_11_handle      \
    -hold_time                               90                         \
    -neighbor_type                           external                   \
    -graceful_restart_enable                 0                          \
    -restart_time                            45                         \
    -stale_time                              0                          \
    -tcp_window_size                         8192                       \
    -local_router_id_enable                  1                          \
    -ipv4_capability_mdt_nlri                0                          \
    -ipv4_capability_unicast_nlri            1                          \
    -ipv4_filter_unicast_nlri                0                          \
    -ipv4_capability_multicast_nlri          1                          \
    -ipv4_filter_multicast_nlri              0                          \
    -ipv4_capability_mpls_nlri               1                          \
    -ipv4_filter_mpls_nlri                   0                          \
    -ipv4_capability_mpls_vpn_nlri           1                          \
    -ipv4_filter_mpls_vpn_nlri               0                          \
    -ipv6_capability_unicast_nlri            1                          \
    -ipv6_filter_unicast_nlri                $multivalue_12_handle      \
    -ipv6_capability_multicast_nlri          1                          \
    -ipv6_filter_multicast_nlri              0                          \
    -ipv6_capability_mpls_nlri               1                          \
    -ipv6_filter_mpls_nlri                   0                          \
    -ipv6_capability_mpls_vpn_nlri           1                          \
    -ipv6_filter_mpls_vpn_nlri               0                          \
    -ttl_value                               64                         \
    -updates_per_iteration                   1                          \
    -bfd_registration                        0                          \
    -bfd_registration_mode                   multi_hop                  \
    -vpls_capability_nlri                    1                          \
    -vpls_filter_nlri                        0                          \
    -act_as_restarted                        0                          \
    -discard_ixia_generated_routes           0                          \
    -flap_down_time                          0                          \
    -local_router_id_type                    same                       \
    -enable_flap                             0                          \
    -send_ixia_signature_with_routes         0                          \
    -flap_up_time                            0                          \
    -next_hop_enable                         0                          \
    -next_hop_ip                             0.0.0.0                    \
    -ipv4_capability_multicast_vpn_nlri      0                          \
    -ipv4_filter_multicast_vpn_nlri          0                          \
    -ipv6_capability_multicast_vpn_nlri      0                          \
    -ipv6_filter_multicast_vpn_nlri          0                          \
    -advertise_end_of_rib                    0                          \
    -configure_keepalive_timer               0                          \
    -keepalive_timer                         30                         \
]

if {[keylget bgp_ipv6_peer_1_status status] != $::SUCCESS} {
    puts "[info script] $bgp_ipv6_peer_1_status"
}
set bgpIpv6Peer_1_handle [keylget bgp_ipv6_peer_1_status bgp_handle]

############################################
## Network Group Config
############################################

set multivalue_13_status [::ixiangpf::multivalue_config \
    -pattern                counter                                       \
    -counter_start          3000:0:1:1:0:0:0:0                            \
    -counter_step           0:0:0:1:0:0:0:0                               \
    -counter_direction      increment                                     \
    -nest_step              0:0:0:0:0:0:0:1,0:0:1:0:0:0:0:0               \
    -nest_owner             $deviceGroup_1_handle,$topology_1_handle      \
    -nest_enabled           0,1                                           \
]
if {[keylget multivalue_13_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_13_status"
}
set multivalue_13_handle [keylget multivalue_13_status multivalue_handle]

set network_group_1_status [::ixiangpf::network_group_config \
    -protocol_handle                      $deviceGroup_1_handle      \
    -connected_to_handle                  $pppoxserver_1_handle      \
    -type                                 ipv6-prefix                \
    -multiplier                           1                          \
    -enable_device                        1                          \
    -ipv6_prefix_network_address          $multivalue_13_handle      \
    -ipv6_prefix_length                   64                         \
    -ipv6_prefix_number_of_addresses      1                          \
]
if {[keylget network_group_1_status status] != $::SUCCESS} {
    puts "[info script] $network_group_1_status"
}
set networkGroup_1_handle [keylget network_group_1_status network_group_handle]
set ixnHLT(HANDLE,//topology:<1>/deviceGroup:<1>/networkGroup:<1>) $networkGroup_1_handle

set multivalue_14_status [::ixiangpf::multivalue_config \
    -pattern                counter                                       \
    -counter_start          200.1.0.0                                     \
    -counter_step           0.1.0.0                                       \
    -counter_direction      increment                                     \
    -nest_step              0.0.0.1,0.1.0.0                               \
    -nest_owner             $deviceGroup_1_handle,$topology_1_handle      \
    -nest_enabled           0,1                                           \
]
if {[keylget multivalue_14_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_14_status"
}
set multivalue_14_handle [keylget multivalue_14_status multivalue_handle]

set network_group_2_status [::ixiangpf::network_group_config \
    -protocol_handle                      $deviceGroup_1_handle      \
    -connected_to_handle                  $pppoxserver_1_handle      \
    -type                                 ipv4-prefix                \
    -multiplier                           1                          \
    -enable_device                        1                          \
    -ipv4_prefix_network_address          $multivalue_14_handle      \
    -ipv4_prefix_length                   24                         \
    -ipv4_prefix_number_of_addresses      1                          \
]
if {[keylget network_group_2_status status] != $::SUCCESS} {
    puts "[info script] $network_group_2_status"
}
set networkGroup_2_handle [keylget network_group_2_status network_group_handle]

#########################################################################################################################
##                                                     Topology 2 Config                                               ##
#########################################################################################################################

set topology_2_handle [setup_topology "Topology 2" $port_2]

#########################################################################################################################
##                                                     Device Group 2 Config                                           ##
#########################################################################################################################
set device_group_2_status [::ixiangpf::topology_config \
    -topology_handle              $topology_2_handle      \
    -device_group_name            {Device Group 2}        \
    -device_group_multiplier      1                       \
    -device_group_enabled         1                       \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    puts "[info script] $device_group_2_status"
}
set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]

############################################
## Ethernet Config
############################################

set multivalue_15_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.12.01.00.00.01       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_15_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_15_status"
}
set multivalue_15_handle [keylget multivalue_15_status multivalue_handle]

set ethernet_2_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 2}               \
    -protocol_handle              $deviceGroup_2_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_15_handle      \
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
if {[keylget ethernet_2_status status] != $::SUCCESS} {
    puts "[info script] $ethernet_2_status"
}
set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]

############################################
## PPoX Client Config
############################################

set multivalue_16_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          1                       \
    -counter_step           0                       \
    -counter_direction      increment               \
    -nest_step              1                       \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           0                       \
]
if {[keylget multivalue_16_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_16_status"
}
set multivalue_16_handle [keylget multivalue_16_status multivalue_handle]

set pppoxclient_1_status [::ixiangpf::pppox_config \
    -port_role                            access                     \
    -handle                               $ethernet_2_handle         \
    -protocol_name                        {PPPoX Client 1}           \
    -unlimited_redial_attempts            0                          \
    -enable_mru_negotiation               0                          \
    -desired_mru_rate                     1492                       \
    -max_payload                          1700                       \
    -enable_max_payload                   0                          \
    -client_ipv6_ncp_configuration        learned                    \
    -client_ipv4_ncp_configuration        learned                    \
    -lcp_enable_accm                      0                          \
    -lcp_accm                             ffffffff                   \
    -ac_select_mode                       first_responding           \
    -auth_req_timeout                     10                         \
    -config_req_timeout                   10                         \
    -echo_req                             $multivalue_16_handle      \
    -echo_rsp                             1                          \
    -ip_cp                                dual_stack                 \
    -ipcp_req_timeout                     10                         \
    -max_auth_req                         20                         \
    -max_padi_req                         5                          \
    -max_padr_req                         5                          \
    -max_terminate_req                    3                          \
    -padi_req_timeout                     10                         \
    -padr_req_timeout                     10                         \
    -password                             password                   \
    -chap_secret                          secret                     \
    -username                             user                       \
    -chap_name                            user                       \
    -mode                                 add                        \
    -auth_mode                            none                       \
    -echo_req_interval                    10                         \
    -max_configure_req                    3                          \
    -max_ipcp_req                         3                          \
    -actual_rate_downstream               10                         \
    -actual_rate_upstream                 10                         \
    -data_link                            ethernet                   \
    -enable_domain_group_map              0                          \
    -enable_client_signal_iwf             0                          \
    -enable_client_signal_loop_char       0                          \
    -enable_client_signal_loop_encap      0                          \
    -enable_client_signal_loop_id         0                          \
    -intermediate_agent_encap1            untagged_eth               \
    -intermediate_agent_encap2            na                         \
    -ppp_local_iid                        0:11:11:11:0:0:0:1         \
    -ppp_local_ip                         1.1.1.1                    \
    -redial                               0                          \
    -redial_max                           20                         \
    -redial_timeout                       10                         \
    -service_type                         any                        \
    -client_dns_options                   disable_extension          \
    -client_dns_primary_address           8.8.8.8                    \
    -client_dns_secondary_address         9.9.9.9                    \
    -client_netmask_options               disable_extension          \
    -client_netmask                       255.0.0.0                  \
    -client_wins_options                  disable_extension          \
    -client_wins_primary_address          8.8.8.8                    \
    -client_wins_secondary_address        9.9.9.9                    \
]
if {[keylget pppoxclient_1_status status] != $::SUCCESS} {
    puts "[info script] $pppoxclient_1_status"
}
set pppoxclient_1_handle [keylget pppoxclient_1_status pppox_client_handle]

############################################
## BGP Peer Config
############################################

set multivalue_17_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          193.0.0.1               \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_17_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_17_status"
}
set multivalue_17_handle [keylget multivalue_17_status multivalue_handle]

set multivalue_18_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          1                       \
    -counter_step           0                       \
    -counter_direction      increment               \
    -nest_step              1                       \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           0                       \
]
if {[keylget multivalue_18_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_18_status"
}
set multivalue_18_handle [keylget multivalue_18_status multivalue_handle]

set bgp_ipv4_peer_2_status [::ixiangpf::emulation_bgp_config \
    -mode                                    enable                     \
    -md5_enable                              0                          \
    -handle                                  $pppoxclient_1_handle      \
    -remote_ip_addr                          1.1.1.1                    \
    -remote_addr_step                        0.0.0.0                    \
    -enable_4_byte_as                        0                          \
    -local_as                                2                          \
    -update_interval                         0                          \
    -count                                   1                          \
    -local_router_id                         $multivalue_17_handle      \
    -hold_time                               90                         \
    -neighbor_type                           external                   \
    -graceful_restart_enable                 0                          \
    -restart_time                            45                         \
    -stale_time                              0                          \
    -tcp_window_size                         8192                       \
    -local_router_id_enable                  1                          \
    -ipv4_capability_mdt_nlri                0                          \
    -ipv4_capability_unicast_nlri            1                          \
    -ipv4_filter_unicast_nlri                $multivalue_18_handle      \
    -ipv4_capability_multicast_nlri          1                          \
    -ipv4_filter_multicast_nlri              0                          \
    -ipv4_capability_mpls_nlri               1                          \
    -ipv4_filter_mpls_nlri                   0                          \
    -ipv4_capability_mpls_vpn_nlri           1                          \
    -ipv4_filter_mpls_vpn_nlri               0                          \
    -ipv6_capability_unicast_nlri            1                          \
    -ipv6_filter_unicast_nlri                0                          \
    -ipv6_capability_multicast_nlri          1                          \
    -ipv6_filter_multicast_nlri              0                          \
    -ipv6_capability_mpls_nlri               1                          \
    -ipv6_filter_mpls_nlri                   0                          \
    -ipv6_capability_mpls_vpn_nlri           1                          \
    -ipv6_filter_mpls_vpn_nlri               0                          \
    -ttl_value                               64                         \
    -updates_per_iteration                   1                          \
    -bfd_registration                        0                          \
    -bfd_registration_mode                   multi_hop                  \
    -vpls_capability_nlri                    1                          \
    -vpls_filter_nlri                        0                          \
    -act_as_restarted                        0                          \
    -discard_ixia_generated_routes           0                          \
    -flap_down_time                          0                          \
    -local_router_id_type                    same                       \
    -enable_flap                             0                          \
    -send_ixia_signature_with_routes         0                          \
    -flap_up_time                            0                          \
    -next_hop_enable                         0                          \
    -next_hop_ip                             0.0.0.0                    \
    -ipv4_capability_multicast_vpn_nlri      0                          \
    -ipv4_filter_multicast_vpn_nlri          0                          \
    -ipv6_capability_multicast_vpn_nlri      0                          \
    -ipv6_filter_multicast_vpn_nlri          0                          \
    -advertise_end_of_rib                    0                          \
    -configure_keepalive_timer               0                          \
    -keepalive_timer                         30                         \
]

if {[keylget bgp_ipv4_peer_2_status status] != $::SUCCESS} {
    puts "[info script] $bgp_ipv4_peer_2_status"
}
set bgpIpv4Peer_2_handle [keylget bgp_ipv4_peer_2_status bgp_handle]

############################################
## BGP+ Peer Config
############################################

set multivalue_19_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          193.0.0.1               \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_19_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_19_status"
}
set multivalue_19_handle [keylget multivalue_19_status multivalue_handle]

set multivalue_20_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          1                       \
    -counter_step           0                       \
    -counter_direction      increment               \
    -nest_step              1                       \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           0                       \
]
if {[keylget multivalue_20_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_20_status"
}
set multivalue_20_handle [keylget multivalue_20_status multivalue_handle]

set bgp_ipv6_peer_2_status [::ixiangpf::emulation_bgp_config \
    -mode                                    enable                     \
    -md5_enable                              0                          \
    -ip_version                              6                          \
    -handle                                  $pppoxclient_1_handle      \
    -remote_ipv6_addr                        11:0:0:0:11:2211:0:1        \
    -remote_addr_step                        0:0:0:0:0:0:0:0            \
    -enable_4_byte_as                        0                          \
    -local_as                                4                          \
    -update_interval                         0                          \
    -count                                   1                          \
    -local_router_id                         $multivalue_19_handle      \
    -hold_time                               90                         \
    -neighbor_type                           external                   \
    -graceful_restart_enable                 0                          \
    -restart_time                            45                         \
    -stale_time                              0                          \
    -tcp_window_size                         8192                       \
    -local_router_id_enable                  1                          \
    -ipv4_capability_mdt_nlri                0                          \
    -ipv4_capability_unicast_nlri            1                          \
    -ipv4_filter_unicast_nlri                0                          \
    -ipv4_capability_multicast_nlri          1                          \
    -ipv4_filter_multicast_nlri              0                          \
    -ipv4_capability_mpls_nlri               1                          \
    -ipv4_filter_mpls_nlri                   0                          \
    -ipv4_capability_mpls_vpn_nlri           1                          \
    -ipv4_filter_mpls_vpn_nlri               0                          \
    -ipv6_capability_unicast_nlri            1                          \
    -ipv6_filter_unicast_nlri                $multivalue_20_handle      \
    -ipv6_capability_multicast_nlri          1                          \
    -ipv6_filter_multicast_nlri              0                          \
    -ipv6_capability_mpls_nlri               1                          \
    -ipv6_filter_mpls_nlri                   0                          \
    -ipv6_capability_mpls_vpn_nlri           1                          \
    -ipv6_filter_mpls_vpn_nlri               0                          \
    -ttl_value                               64                         \
    -updates_per_iteration                   1                          \
    -bfd_registration                        0                          \
    -bfd_registration_mode                   multi_hop                  \
    -vpls_capability_nlri                    1                          \
    -vpls_filter_nlri                        0                          \
    -act_as_restarted                        0                          \
    -discard_ixia_generated_routes           0                          \
    -flap_down_time                          0                          \
    -local_router_id_type                    same                       \
    -enable_flap                             0                          \
    -send_ixia_signature_with_routes         0                          \
    -flap_up_time                            0                          \
    -next_hop_enable                         0                          \
    -next_hop_ip                             0.0.0.0                    \
    -ipv4_capability_multicast_vpn_nlri      0                          \
    -ipv4_filter_multicast_vpn_nlri          0                          \
    -ipv6_capability_multicast_vpn_nlri      0                          \
    -ipv6_filter_multicast_vpn_nlri          0                          \
    -advertise_end_of_rib                    0                          \
    -configure_keepalive_timer               0                          \
    -keepalive_timer                         30                         \
]

if {[keylget bgp_ipv6_peer_2_status status] != $::SUCCESS} {
    puts "[info script] $bgp_ipv6_peer_2_status"
}
set bgpIpv6Peer_2_handle [keylget bgp_ipv6_peer_2_status bgp_handle]

############################################
## Network Group Config
############################################

set multivalue_21_status [::ixiangpf::multivalue_config \
    -pattern                counter                                       \
    -counter_start          3000:1:1:1:0:0:0:0                            \
    -counter_step           0:0:0:1:0:0:0:0                               \
    -counter_direction      increment                                     \
    -nest_step              0:0:0:0:0:0:0:1,0:0:1:0:0:0:0:0               \
    -nest_owner             $deviceGroup_2_handle,$topology_2_handle      \
    -nest_enabled           0,1                                           \
]
if {[keylget multivalue_21_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_21_status"
}
set multivalue_21_handle [keylget multivalue_21_status multivalue_handle]

set network_group_3_status [::ixiangpf::network_group_config \
    -protocol_handle                      $deviceGroup_2_handle      \
    -connected_to_handle                  $pppoxclient_1_handle      \
    -type                                 ipv6-prefix                \
    -multiplier                           1                          \
    -enable_device                        1                          \
    -ipv6_prefix_network_address          $multivalue_21_handle      \
    -ipv6_prefix_length                   64                         \
    -ipv6_prefix_number_of_addresses      1                          \
]
if {[keylget network_group_3_status status] != $::SUCCESS} {
    puts "[info script] $network_group_3_status"
}
set networkGroup_3_handle [keylget network_group_3_status network_group_handle]

set multivalue_22_status [::ixiangpf::multivalue_config \
    -pattern                counter                                       \
    -counter_start          201.1.0.0                                     \
    -counter_step           0.1.0.0                                       \
    -counter_direction      increment                                     \
    -nest_step              0.0.0.1,0.1.0.0                               \
    -nest_owner             $deviceGroup_2_handle,$topology_2_handle      \
    -nest_enabled           0,1                                           \
]
if {[keylget multivalue_22_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_22_status"
}
set multivalue_22_handle [keylget multivalue_22_status multivalue_handle]

set network_group_4_status [::ixiangpf::network_group_config \
    -protocol_handle                      $deviceGroup_2_handle      \
    -connected_to_handle                  $pppoxclient_1_handle      \
    -type                                 ipv4-prefix                \
    -multiplier                           1                          \
    -enable_device                        1                          \
    -ipv4_prefix_network_address          $multivalue_22_handle      \
    -ipv4_prefix_length                   24                         \
    -ipv4_prefix_number_of_addresses      1                          \
]
if {[keylget network_group_4_status status] != $::SUCCESS} {
    puts "[info script] $network_group_4_status"
}
set networkGroup_4_handle [keylget network_group_4_status network_group_handle]

############################################
## Globals Config
############################################

set bgp_ipv4_peer_3_status [::ixiangpf::emulation_bgp_config \
    -mode        enable        \
    -handle      /globals      \
]

if {[keylget bgp_ipv4_peer_3_status status] != $::SUCCESS} {
    puts "[info script] $bgp_ipv4_peer_3_status"
}

set bgp_ipv6_peer_3_status [::ixiangpf::emulation_bgp_config \
    -mode        enable        \
    -handle      /globals      \
]

if {[keylget bgp_ipv6_peer_3_status status] != $::SUCCESS} {
    puts "[info script] $bgp_ipv6_peer_3_status"
}

set ethernet_3_status [::ixiangpf::interface_config \
    -protocol_handle                     /globals      \
    -ethernet_attempt_enabled            0             \
    -ethernet_attempt_rate               200           \
    -ethernet_attempt_interval           1000          \
    -ethernet_attempt_scale_mode         port          \
    -ethernet_diconnect_enabled          0             \
    -ethernet_disconnect_rate            200           \
    -ethernet_disconnect_interval        1000          \
    -ethernet_disconnect_scale_mode      port          \
]
if {[keylget ethernet_3_status status] != $::SUCCESS} {
    puts "[info script] $ethernet_3_status"
}

set multivalue_23_status [::ixiangpf::multivalue_config \
    -pattern                counter        \
    -counter_start          1              \
    -counter_step           0              \
    -counter_direction      increment      \
]
if {[keylget multivalue_23_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_23_status"
}
set multivalue_23_handle [keylget multivalue_23_status multivalue_handle]

set multivalue_24_status [::ixiangpf::multivalue_config \
    -pattern                distributed      \
    -distributed_value      1                \
]
if {[keylget multivalue_24_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_24_status"
}
set multivalue_24_handle [keylget multivalue_24_status multivalue_handle]

set multivalue_25_status [::ixiangpf::multivalue_config \
    -pattern                distributed      \
    -distributed_value      10               \
]
if {[keylget multivalue_25_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_25_status"
}
set multivalue_25_handle [keylget multivalue_25_status multivalue_handle]

set multivalue_26_status [::ixiangpf::multivalue_config \
    -pattern                distributed      \
    -distributed_value      10               \
]
if {[keylget multivalue_26_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_26_status"
}
set multivalue_26_handle [keylget multivalue_26_status multivalue_handle]

set pppoxclient_2_status [::ixiangpf::pppox_config \
    -port_role                                access                     \
    -handle                                   /globals                   \
    -mode                                     add                        \
    -ipv6_global_address_mode                 icmpv6                     \
    -ra_timeout                               30                         \
    -create_interfaces                        $multivalue_23_handle      \
    -attempt_rate                             200                        \
    -attempt_max_outstanding                  400                        \
    -attempt_interval                         1000                       \
    -attempt_enabled                          1                          \
    -attempt_scale_mode                       port                       \
    -disconnect_rate                          200                        \
    -disconnect_max_outstanding               400                        \
    -disconnect_interval                      1000                       \
    -disconnect_enabled                       1                          \
    -disconnect_scale_mode                    port                       \
    -enable_session_lifetime                  0                          \
    -min_lifetime                             $multivalue_24_handle      \
    -max_lifetime                             $multivalue_25_handle      \
    -enable_session_lifetime_restart          0                          \
    -max_session_lifetime_restarts            $multivalue_26_handle      \
    -unlimited_session_lifetime_restarts      0                          \
]
if {[keylget pppoxclient_2_status status] != $::SUCCESS} {
    puts "[info script] $pppoxclient_2_status"
}

############################################
## Start Protocols
############################################

set bgp_start_1_status [::ixiangpf::emulation_bgp_control           \
        -handle                          $bgpIpv4Peer_1_handle      \
        -mode                            start                      ]
        
if {[keylget bgp_start_1_status status] != $::SUCCESS} {
    puts "[info script] $bgp_start_1_status"
}
        
set bgp_start_2_status [::ixiangpf::emulation_bgp_control           \
        -handle                          $bgpIpv4Peer_2_handle      \
        -mode                            start                      ]
        
if {[keylget bgp_start_2_status status] != $::SUCCESS} {
    puts "[info script] $bgp_start_2_status"
}
        
set bgp_start_3_status [::ixiangpf::emulation_bgp_control           \
        -handle                          $bgpIpv6Peer_1_handle      \
        -mode                            start                      ]
        
if {[keylget bgp_start_3_status status] != $::SUCCESS} {
    puts "[info script] $bgp_start_3_status"
}

set bgp_start_4_status [::ixiangpf::emulation_bgp_control           \
        -handle                          $bgpIpv6Peer_2_handle      \
        -mode                            start                      ]

if {[keylget bgp_start_4_status status] != $::SUCCESS} {
    puts "[info script] $bgp_start_4_status"
}

puts "Wait for 90 seconds"

after 90000

############################################
## Stats for BGP
############################################

set bgp_stats_1_status [::ixiangpf::emulation_bgp_info                  \
        -handle                          $bgpIpv4Peer_1_handle          \
        -mode                            stats                          ]
        
if {[keylget bgp_stats_1_status status] != $::SUCCESS} {
    puts "[info script] $bgp_stats_1_status"
}
        
if {[keylget bgp_stats_1_status $port_1.aggregate.status] != "started"} {
    puts "status info is not correct"
    incr cfgErrors
}

if {[keylget bgp_stats_1_status $port_1.aggregate.sessions_configured] != "1"} {
    puts "sessions_configured info is not correct"
    incr cfgErrors
}

if {[keylget bgp_stats_1_status $port_1.aggregate.sessions_established] != "1"} {
    puts "sessions_established info is not correct"
    incr cfgErrors
}

set bgp_stats_2_status [::ixiangpf::emulation_bgp_info                  \
        -handle                          $bgpIpv4Peer_2_handle          \
        -mode                            stats                          ]
        
if {[keylget bgp_stats_2_status status] != $::SUCCESS} {
    puts "[info script] $bgp_stats_2_status"
}
        
if {[keylget bgp_stats_2_status $port_2.aggregate.status] != "started"} {
    puts "status info is not correct"
    incr cfgErrors
}

if {[keylget bgp_stats_2_status $port_2.aggregate.sessions_configured] != "1"} {
    puts "sessions_configured info is not correct"
    incr cfgErrors
}

if {[keylget bgp_stats_2_status $port_2.aggregate.sessions_established] != "1"} {
    puts "sessions_established info is not correct"
    incr cfgErrors
}

set bgp_stats_3_status [::ixiangpf::emulation_bgp_info                  \
        -handle                          $bgpIpv6Peer_1_handle          \
        -mode                            stats                          ]
      
if {[keylget bgp_stats_3_status status] != $::SUCCESS} {
    puts "[info script] $bgp_stats_3_status"
}

if {[keylget bgp_stats_3_status $port_1.aggregate.status] != "started"} {
    puts "status info is not correct"
    incr cfgErrors
}

if {[keylget bgp_stats_3_status $port_1.aggregate.sessions_configured] != "1"} {
    puts "sessions_configured info is not correct"
    incr cfgErrors
}

if {[keylget bgp_stats_3_status $port_1.aggregate.sessions_established] != "1"} {
    puts "sessions_established info is not correct"
    incr cfgErrors
}


set bgp_stats_4_status [::ixiangpf::emulation_bgp_info                  \
        -handle                          $bgpIpv6Peer_2_handle          \
        -mode                            stats                          ]

if {[keylget bgp_stats_4_status status] != $::SUCCESS} {
    puts "[info script] $bgp_stats_4_status"
}

if {[keylget bgp_stats_4_status $port_2.aggregate.status] != "started"} {
    puts "status info is not correct"
    incr cfgErrors
}

if {[keylget bgp_stats_4_status $port_2.aggregate.sessions_configured] != "1"} {
    puts "sessions_configured info is not correct"
    incr cfgErrors
}

if {[keylget bgp_stats_4_status $port_2.aggregate.sessions_established] != "1"} {
    puts "sessions_established info is not correct"
    incr cfgErrors
}

set bgp_session_1_status [::ixiangpf::emulation_bgp_info        \
        -handle                          $bgpIpv4Peer_1_handle  \
        -mode                            session                ]

if {[keylget bgp_session_1_status status] != $::SUCCESS} {
    puts "[info script] $bgp_session_1_status"
}

set handle [keylget bgp_ipv4_peer_1_status handles]

if {[keylget bgp_session_1_status $handle.session.session_status] != "Up"} {
    puts "session_status info is not correct"
    incr cfgErrors
}

if {[keylget bgp_session_1_status $handle.session.fsm_state] != "Established"} {
    puts "fsm_state info is not correct"
    incr cfgErrors
}

set bgp_session_2_status [::ixiangpf::emulation_bgp_info        \
        -handle                          $bgpIpv6Peer_1_handle  \
        -mode                            session                ]
       
if {[keylget bgp_session_2_status status] != $::SUCCESS} {
    puts "[info script] $bgp_session_2_status"
}

set handle [keylget bgp_ipv6_peer_1_status handles]

if {[keylget bgp_session_2_status $handle.session.session_status] != "Up"} {
    puts "session_status info is not correct"
    incr cfgErrors
}

if {[keylget bgp_session_2_status $handle.session.fsm_state] != "Established"} {
    puts "fsm_state info is not correct"
    incr cfgErrors
}
############################################
## Stop Protocols
############################################

set bgp_start_1_status [::ixiangpf::emulation_bgp_control           \
        -handle                          $bgpIpv4Peer_1_handle      \
        -mode                            stop                       ]
        
set bgp_start_2_status [::ixiangpf::emulation_bgp_control           \
        -handle                          $bgpIpv4Peer_2_handle      \
        -mode                            stop                       ]
        
set bgp_start_3_status [::ixiangpf::emulation_bgp_control           \
        -handle                          $bgpIpv6Peer_1_handle      \
        -mode                            stop                       ]

set bgp_start_4_status [::ixiangpf::emulation_bgp_control           \
        -handle                          $bgpIpv6Peer_2_handle      \
        -mode                            stop                       ]

puts "Wait for 45 seconds"

after 30000

############################### SUCCESS or FAILURE #############################

if {$cfgErrors > 0} {
    puts "FAIL - $test_name  $cfgErrors Errors- [clock format [clock seconds]]"
    return 0
} else {
    puts "SUCCESS - $test_name - [clock format [clock seconds]]"
    return 1
}
