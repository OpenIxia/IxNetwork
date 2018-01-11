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
#   This sample configures BGP and BGP+ Peers over IPv4 and IPv6 stacks on 4   #
#   Device Groups in two topologies and retreives neighbors and settings stats #
# Module:                                                                      #
#   The sample was tested on a LM1000TXS4 module.                              #
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

puts "Connect to the chassis complete."

#########################################################################################################################
##                                                     Topology 1 Config                                               ##
#########################################################################################################################

set topology_1_handle [setup_topology "Topology 1" $port_1]

#########################################################################################################################
##                                                     Device Group 1 Config                                           ##
#########################################################################################################################

set device_group_1_status [::ixiangpf::topology_config      \
    -topology_handle              $topology_1_handle        \
    -device_group_name            {D1}                      \
    -device_group_multiplier      2                         \
    -device_group_enabled         1                         \
]
if {[keylget device_group_1_status status] != $::SUCCESS} {
    error $device_group_1_status
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
    -vlan                         1                          \
    -vlan_id                      101                        \
    -vlan_id_step                 1                          \
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
## IPv4 Config
############################################

set multivalue_2_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          20.20.20.1              \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_2_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_2_status"
}
set multivalue_2_handle [keylget multivalue_2_status multivalue_handle]

set gw_multivalue_1_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          20.20.20.3              \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget gw_multivalue_1_status status] != $::SUCCESS} {
    puts "[info script] $gw_multivalue_1_status"
}
set gw_multivalue_1_handle [keylget gw_multivalue_1_status multivalue_handle]

set ipv4_1_status [::ixiangpf::interface_config \
    -protocol_name                {IPv4 1}                  \
    -protocol_handle              $ethernet_1_handle        \
    -ipv4_resolve_gateway         1                         \
    -ipv4_manual_gateway_mac      00.00.00.00.00.01         \
    -gateway                      $gw_multivalue_1_handle   \
    -intf_ip_addr                 $multivalue_2_handle      \
    -netmask                      255.255.255.0             \
]
if {[keylget ipv4_1_status status] != $::SUCCESS} {
    puts "[info script] $ipv4_1_status"
}
set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]

############################################
## IPv6 Config
############################################

set multivalue_3_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          2000:0:0:0:0:0:0:1      \
    -counter_step           0:0:0:0:0:0:0:1         \
    -counter_direction      increment               \
    -nest_step              0:0:0:1:0:0:0:0         \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_3_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_3_status"
}
set multivalue_3_handle [keylget multivalue_3_status multivalue_handle]

set gw_multivalue_2_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          2000:0:0:0:0:0:0:3      \
    -counter_step           0:0:0:0:0:0:0:1         \
    -counter_direction      increment               \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget gw_multivalue_2_status status] != $::SUCCESS} {
    puts "[info script] $gw_multivalue_2_status"
}
set gw_multivalue_2_handle [keylget gw_multivalue_2_status multivalue_handle]

set ipv6_1_status [::ixiangpf::interface_config \
    -protocol_name                {IPv6 1}                  \
    -protocol_handle              $ethernet_1_handle        \
    -ipv6_resolve_gateway         1                         \
    -ipv6_manual_gateway_mac      00.00.00.00.00.01         \
    -ipv6_gateway                 $gw_multivalue_2_handle   \
    -ipv6_intf_addr               $multivalue_3_handle      \
    -ipv6_prefix_length           64                        \
]
if {[keylget ipv6_1_status status] != $::SUCCESS} {
    puts "[info script] $ipv6_1_status"
}
set ipv6_1_handle [keylget ipv6_1_status ipv6_handle]

############################################
## BGP Peer Config
############################################

set multivalue_nlri_status [::ixiangpf::multivalue_config \
    -pattern                single_value            \
    -single_value           1                       \
]
if {[keylget multivalue_nlri_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_nlri_status"
}
set multivalue_nlri_handle [keylget multivalue_nlri_status multivalue_handle]

set bgp_ipv4_peer_1_status [::ixiangpf::emulation_bgp_config \
    -mode                                    enable                     \
    -md5_enable                              0                          \
    -handle                                  $ipv4_1_handle             \
    -remote_ip_addr                          20.20.20.3                 \
    -remote_addr_step                        0.0.0.1                    \
    -enable_4_byte_as                        0                          \
    -local_as                                100                        \
    -update_interval                         0                          \
    -count                                   1                          \
    -hold_time                               90                         \
    -neighbor_type                           internal                   \
    -graceful_restart_enable                 0                          \
    -restart_time                            45                         \
    -stale_time                              0                          \
    -tcp_window_size                         8192                       \
    -local_router_id_enable                  1                          \
    -ipv4_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv4_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv4_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv4_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv4_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ipv6_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv6_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv6_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv6_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv6_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ttl_value                               64                         \
    -updates_per_iteration                   1                          \
    -bfd_registration                        0                          \
    -bfd_registration_mode                   multi_hop                  \
    -vpls_capability_nlri                    $multivalue_nlri_handle    \
    -vpls_filter_nlri                        $multivalue_nlri_handle    \
    -act_as_restarted                        0                          \
    -discard_ixia_generated_routes           0                          \
    -flap_down_time                          0                          \
    -local_router_id_type                    same                       \
    -enable_flap                             0                          \
    -send_ixia_signature_with_routes         0                          \
    -flap_up_time                            0                          \
    -next_hop_enable                         0                          \
    -next_hop_ip                             0.0.0.0                    \
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
set bgp_ipv6_peer_1_status [::ixiangpf::emulation_bgp_config \
    -mode                                    enable                     \
    -md5_enable                              0                          \
    -ip_version                              6                          \
    -handle                                  $ipv6_1_handle             \
    -remote_ipv6_addr                        2000:0:0:0:0:0:0:3         \
    -remote_addr_step                        0:0:0:0:0:0:0:1            \
    -enable_4_byte_as                        0                          \
    -local_as                                100                        \
    -update_interval                         0                          \
    -count                                   1                          \
    -hold_time                               90                         \
    -neighbor_type                           internal                   \
    -graceful_restart_enable                 0                          \
    -restart_time                            45                         \
    -stale_time                              0                          \
    -tcp_window_size                         8192                       \
    -local_router_id_enable                  1                          \
    -ipv4_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv4_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv4_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv4_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv4_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ipv6_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv6_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv6_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv6_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv6_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ttl_value                               64                         \
    -updates_per_iteration                   1                          \
    -bfd_registration                        0                          \
    -bfd_registration_mode                   multi_hop                  \
    -vpls_capability_nlri                    $multivalue_nlri_handle    \
    -vpls_filter_nlri                        $multivalue_nlri_handle    \
    -act_as_restarted                        0                          \
    -discard_ixia_generated_routes           0                          \
    -flap_down_time                          0                          \
    -local_router_id_type                    same                       \
    -enable_flap                             0                          \
    -send_ixia_signature_with_routes         0                          \
    -flap_up_time                            0                          \
    -next_hop_enable                         0                          \
    -next_hop_ip                             0.0.0.0                    \
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

set network_group_1_status [::ixiangpf::network_group_config      \
    -protocol_handle                   $deviceGroup_1_handle      \
    -connected_to_handle               $ethernet_1_handle         \
    -type                              ipv4-prefix                \
    -multiplier                        2                          \
    -enable_device                     1                          \
    -ipv4_prefix_network_address       200.1.0.0                  \
    -ipv4_prefix_network_address_step  0.1.0.0                    \
    -ipv4_prefix_length                24                         \
    -ipv4_prefix_number_of_addresses   2                          ]
    
if {[keylget network_group_1_status status] != $::SUCCESS} {
    puts "[info script] $network_group_1_status"
}
set networkGroup_1_handle [keylget network_group_1_status network_group_handle]

set network_group_2_status [::ixiangpf::network_group_config      \
    -protocol_handle                   $deviceGroup_1_handle      \
    -connected_to_handle               $ethernet_1_handle         \
    -type                              ipv6-prefix                \
    -multiplier                        2                          \
    -enable_device                     1                          \
    -ipv6_prefix_network_address       3000:0:1:1:0:0:0:0         \
    -ipv6_prefix_network_address_step  0:0:1:0:0:0:0:0            \
    -ipv6_prefix_length                64                         \
    -ipv6_prefix_number_of_addresses   2                          ]
    
if {[keylget network_group_2_status status] != $::SUCCESS} {
    puts "[info script] $network_group_2_status"
}
set networkGroup_2_handle [keylget network_group_2_status network_group_handle]

#########################################################################################################################
##                                                     Device Group 2 Config                                           ##
#########################################################################################################################

set device_group_2_status [::ixiangpf::topology_config      \
    -topology_handle              $topology_1_handle        \
    -device_group_name            {D2}                      \
    -device_group_multiplier      2                         \
    -device_group_enabled         1                         \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    error $device_group_2_status
}

set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]

############################################
## Ethernet Config
############################################

set multivalue_4_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.13.01.00.00.01       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_4_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_4_status"
}
set multivalue_4_handle [keylget multivalue_4_status multivalue_handle]

set ethernet_2_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 2}               \
    -protocol_handle              $deviceGroup_2_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_4_handle       \
    -vlan                         0                          \
    -vlan_id                      1                          \
    -vlan_id_step                 1                          \
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
## IPv4 Config
############################################

set multivalue_5_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          30.30.30.1              \
    -counter_step           0.0.1.0                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           0                       \
]
if {[keylget multivalue_5_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_5_status"
}
set multivalue_5_handle [keylget multivalue_5_status multivalue_handle]

set gw_multivalue_3_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          30.30.30.2              \
    -counter_step           0.0.1.0                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget gw_multivalue_3_status status] != $::SUCCESS} {
    puts "[info script] $gw_multivalue_3_status"
}
set gw_multivalue_3_handle [keylget gw_multivalue_3_status multivalue_handle]

set ipv4_2_status [::ixiangpf::interface_config \
    -protocol_name                {IPv4 2}                  \
    -protocol_handle              $ethernet_2_handle        \
    -ipv4_resolve_gateway         1                         \
    -ipv4_manual_gateway_mac      00.00.00.00.00.01         \
    -gateway                      $gw_multivalue_3_handle   \
    -intf_ip_addr                 $multivalue_5_handle      \
    -netmask                      255.255.255.0             \
]
if {[keylget ipv4_2_status status] != $::SUCCESS} {
    puts "[info script] $ipv4_2_status"
}
set ipv4_2_handle [keylget ipv4_2_status ipv4_handle]

############################################
## IPv6 Config
############################################

set multivalue_6_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          3000:0:0:1:0:0:0:1      \
    -counter_step           0:0:0:1:0:0:0:0         \
    -counter_direction      increment               \
    -nest_step              0:0:0:1:0:0:0:0         \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           0                       \
]
if {[keylget multivalue_6_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_6_status"
}
set multivalue_6_handle [keylget multivalue_6_status multivalue_handle]

set gw_multivalue_4_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          3000:0:0:1:0:0:0:2      \
    -counter_step           0:0:0:1:0:0:0:0         \
    -counter_direction      increment               \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget gw_multivalue_4_status status] != $::SUCCESS} {
    puts "[info script] $gw_multivalue_4_status"
}
set gw_multivalue_4_handle [keylget gw_multivalue_4_status multivalue_handle]

set ipv6_2_status [::ixiangpf::interface_config \
    -protocol_name                {IPv6 2}                  \
    -protocol_handle              $ethernet_2_handle        \
    -ipv6_resolve_gateway         1                         \
    -ipv6_manual_gateway_mac      00.00.00.00.00.01         \
    -ipv6_gateway                 $gw_multivalue_4_handle   \
    -ipv6_intf_addr               $multivalue_6_handle      \
    -ipv6_prefix_length           64                        \
]
if {[keylget ipv6_2_status status] != $::SUCCESS} {
    puts "[info script] $ipv6_2_status"
}
set ipv6_2_handle [keylget ipv6_2_status ipv6_handle]

############################################
## BGP Peer Config
############################################

set bgp_ipv4_peer_2_status [::ixiangpf::emulation_bgp_config \
    -mode                                    enable                     \
    -md5_enable                              0                          \
    -handle                                  $ipv4_2_handle             \
    -remote_ip_addr                          30.30.30.2                 \
    -remote_addr_step                        0.0.1.0                    \
    -enable_4_byte_as                        0                          \
    -local_as                                200                        \
    -update_interval                         0                          \
    -count                                   1                          \
    -hold_time                               90                         \
    -neighbor_type                           external                   \
    -graceful_restart_enable                 0                          \
    -restart_time                            45                         \
    -stale_time                              0                          \
    -tcp_window_size                         8192                       \
    -local_router_id_enable                  1                          \
    -ipv4_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv4_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv4_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv4_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv4_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ipv6_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv6_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv6_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv6_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv6_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ttl_value                               64                         \
    -updates_per_iteration                   1                          \
    -bfd_registration                        0                          \
    -bfd_registration_mode                   multi_hop                  \
    -vpls_capability_nlri                    $multivalue_nlri_handle    \
    -vpls_filter_nlri                        $multivalue_nlri_handle    \
    -act_as_restarted                        0                          \
    -discard_ixia_generated_routes           0                          \
    -flap_down_time                          0                          \
    -local_router_id_type                    same                       \
    -enable_flap                             0                          \
    -send_ixia_signature_with_routes         0                          \
    -flap_up_time                            0                          \
    -next_hop_enable                         0                          \
    -next_hop_ip                             0.0.0.0                    \
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

set bgp_ipv6_peer_2_status [::ixiangpf::emulation_bgp_config \
    -mode                                    enable                     \
    -md5_enable                              0                          \
    -ip_version                              6                          \
    -handle                                  $ipv6_2_handle             \
    -remote_ipv6_addr                        3000:0:0:1:0:0:0:2         \
    -remote_addr_step                        0:0:0:1:0:0:0:0            \
    -enable_4_byte_as                        0                          \
    -local_as                                200                        \
    -update_interval                         0                          \
    -count                                   1                          \
    -hold_time                               90                         \
    -neighbor_type                           external                   \
    -graceful_restart_enable                 0                          \
    -restart_time                            45                         \
    -stale_time                              0                          \
    -tcp_window_size                         8192                       \
    -local_router_id_enable                  1                          \
    -ipv4_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv4_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv4_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv4_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv4_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ipv6_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv6_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv6_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv6_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv6_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ttl_value                               64                         \
    -updates_per_iteration                   1                          \
    -bfd_registration                        0                          \
    -bfd_registration_mode                   multi_hop                  \
    -vpls_capability_nlri                    $multivalue_nlri_handle    \
    -vpls_filter_nlri                        $multivalue_nlri_handle    \
    -act_as_restarted                        0                          \
    -discard_ixia_generated_routes           0                          \
    -flap_down_time                          0                          \
    -local_router_id_type                    same                       \
    -enable_flap                             0                          \
    -send_ixia_signature_with_routes         0                          \
    -flap_up_time                            0                          \
    -next_hop_enable                         0                          \
    -next_hop_ip                             0.0.0.0                    \
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

set network_group_3_status [::ixiangpf::network_group_config      \
    -protocol_handle                   $deviceGroup_2_handle      \
    -connected_to_handle               $ethernet_2_handle         \
    -type                              ipv4-prefix                \
    -multiplier                        2                          \
    -enable_device                     1                          \
    -ipv4_prefix_network_address       202.1.0.0                  \
    -ipv4_prefix_network_address_step  0.1.0.0                    \
    -ipv4_prefix_length                24                         \
    -ipv4_prefix_number_of_addresses   2                          ]
    
if {[keylget network_group_3_status status] != $::SUCCESS} {
    puts "[info script] $network_group_3_status"
}
set networkGroup_3_handle [keylget network_group_3_status network_group_handle]

set network_group_4_status [::ixiangpf::network_group_config      \
    -protocol_handle                   $deviceGroup_2_handle      \
    -connected_to_handle               $ethernet_2_handle         \
    -type                              ipv6-prefix                \
    -multiplier                        2                          \
    -enable_device                     1                          \
    -ipv6_prefix_network_address       3000:2:1:1:0:0:0:0         \
    -ipv6_prefix_network_address_step  0:0:1:0:0:0:0:0            \
    -ipv6_prefix_length                64                         \
    -ipv6_prefix_number_of_addresses   2                          ]
    
if {[keylget network_group_4_status status] != $::SUCCESS} {
    puts "[info script] $network_group_4_status"
}
set networkGroup_4_handle [keylget network_group_4_status network_group_handle]

#########################################################################################################################
##                                                     Topology 2 Config                                               ##
#########################################################################################################################

set topology_2_handle [setup_topology "Topology 2" $port_2]

#########################################################################################################################
##                                                     Device Group 3 Config                                           ##
#########################################################################################################################

set device_group_3_status [::ixiangpf::topology_config      \
    -topology_handle              $topology_2_handle        \
    -device_group_name            {D3}                      \
    -device_group_multiplier      2                         \
    -device_group_enabled         1                         \
]
if {[keylget device_group_3_status status] != $::SUCCESS} {
    error $device_group_3_status
}

set deviceGroup_3_handle [keylget device_group_3_status device_group_handle]

############################################
## Ethernet Config
############################################

set multivalue_7_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.12.01.00.00.01       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_7_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_7_status"
}
set multivalue_7_handle [keylget multivalue_7_status multivalue_handle]

set ethernet_3_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 3}               \
    -protocol_handle              $deviceGroup_3_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_7_handle       \
    -vlan                         1                          \
    -vlan_id                      101                        \
    -vlan_id_step                 1                          \
    -vlan_id_count                1                          \
    -vlan_tpid                    0x8100                     \
    -vlan_user_priority           0                          \
    -vlan_user_priority_step      0                          \
    -use_vpn_parameters           0                          \
    -site_id                      0                          \
]
if {[keylget ethernet_3_status status] != $::SUCCESS} {
    puts "[info script] $ethernet_3_status"
}
set ethernet_3_handle [keylget ethernet_3_status ethernet_handle]

############################################
## IPv4 Config
############################################

set multivalue_8_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          20.20.20.3              \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_8_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_8_status"
}
set multivalue_8_handle [keylget multivalue_8_status multivalue_handle]

set gw_multivalue_5_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          20.20.20.1              \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget gw_multivalue_5_status status] != $::SUCCESS} {
    puts "[info script] $gw_multivalue_5_status"
}
set gw_multivalue_5_handle [keylget gw_multivalue_5_status multivalue_handle]

set ipv4_3_status [::ixiangpf::interface_config \
    -protocol_name                {IPv4 3}                  \
    -protocol_handle              $ethernet_3_handle        \
    -ipv4_resolve_gateway         1                         \
    -ipv4_manual_gateway_mac      00.00.00.00.00.01         \
    -gateway                      $gw_multivalue_5_handle   \
    -intf_ip_addr                 $multivalue_8_handle      \
    -netmask                      255.255.255.0             \
]
if {[keylget ipv4_3_status status] != $::SUCCESS} {
    puts "[info script] $ipv4_3_status"
}
set ipv4_3_handle [keylget ipv4_3_status ipv4_handle]

############################################
## IPv6 Config
############################################

set multivalue_9_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          2000:0:0:0:0:0:0:3      \
    -counter_step           0:0:0:0:0:0:0:1         \
    -counter_direction      increment               \
    -nest_step              0:0:0:1:0:0:0:0         \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_9_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_9_status"
}
set multivalue_9_handle [keylget multivalue_9_status multivalue_handle]

set gw_multivalue_6_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          2000:0:0:0:0:0:0:1      \
    -counter_step           0:0:0:0:0:0:0:1         \
    -counter_direction      increment               \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget gw_multivalue_6_status status] != $::SUCCESS} {
    puts "[info script] $gw_multivalue_6_status"
}
set gw_multivalue_6_handle [keylget gw_multivalue_6_status multivalue_handle]

set ipv6_3_status [::ixiangpf::interface_config \
    -protocol_name                {IPv6 3}                  \
    -protocol_handle              $ethernet_3_handle        \
    -ipv6_resolve_gateway         1                         \
    -ipv6_manual_gateway_mac      00.00.00.00.00.01         \
    -ipv6_gateway                 $gw_multivalue_6_handle   \
    -ipv6_intf_addr               $multivalue_9_handle      \
    -ipv6_prefix_length           64                        \
]
if {[keylget ipv6_3_status status] != $::SUCCESS} {
    puts "[info script] $ipv6_3_status"
}
set ipv6_3_handle [keylget ipv6_3_status ipv6_handle]

############################################
## BGP Peer Config
############################################

set bgp_ipv4_peer_3_status [::ixiangpf::emulation_bgp_config \
    -mode                                    enable                     \
    -md5_enable                              0                          \
    -handle                                  $ipv4_3_handle             \
    -remote_ip_addr                          20.20.20.1                 \
    -remote_addr_step                        0.0.0.1                    \
    -enable_4_byte_as                        0                          \
    -local_as                                100                        \
    -update_interval                         0                          \
    -count                                   1                          \
    -hold_time                               90                         \
    -neighbor_type                           internal                   \
    -graceful_restart_enable                 0                          \
    -restart_time                            45                         \
    -stale_time                              0                          \
    -tcp_window_size                         8192                       \
    -local_router_id_enable                  1                          \
    -ipv4_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv4_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv4_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv4_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv4_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ipv6_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv6_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv6_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv6_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv6_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ttl_value                               64                         \
    -updates_per_iteration                   1                          \
    -bfd_registration                        0                          \
    -bfd_registration_mode                   multi_hop                  \
    -vpls_capability_nlri                    $multivalue_nlri_handle    \
    -vpls_filter_nlri                        $multivalue_nlri_handle    \
    -act_as_restarted                        0                          \
    -discard_ixia_generated_routes           0                          \
    -flap_down_time                          0                          \
    -local_router_id_type                    same                       \
    -enable_flap                             0                          \
    -send_ixia_signature_with_routes         0                          \
    -flap_up_time                            0                          \
    -next_hop_enable                         0                          \
    -next_hop_ip                             0.0.0.0                    \
    -advertise_end_of_rib                    0                          \
    -configure_keepalive_timer               0                          \
    -keepalive_timer                         30                         \
]

if {[keylget bgp_ipv4_peer_3_status status] != $::SUCCESS} {
    puts "[info script] $bgp_ipv4_peer_3_status"
}
set bgpIpv4Peer_3_handle [keylget bgp_ipv4_peer_3_status bgp_handle]

############################################
## BGP+ Peer Config
############################################

set bgp_ipv6_peer_3_status [::ixiangpf::emulation_bgp_config \
    -mode                                    enable                     \
    -md5_enable                              0                          \
    -ip_version                              6                          \
    -handle                                  $ipv6_3_handle             \
    -remote_ipv6_addr                        2000:0:0:0:0:0:0:1         \
    -remote_addr_step                        0:0:0:0:0:0:0:1            \
    -enable_4_byte_as                        0                          \
    -local_as                                100                        \
    -update_interval                         0                          \
    -count                                   1                          \
    -hold_time                               90                         \
    -neighbor_type                           internal                   \
    -graceful_restart_enable                 0                          \
    -restart_time                            45                         \
    -stale_time                              0                          \
    -tcp_window_size                         8192                       \
    -local_router_id_enable                  1                          \
    -ipv4_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv4_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv4_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv4_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv4_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ipv6_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv6_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv6_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv6_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv6_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ttl_value                               64                         \
    -updates_per_iteration                   1                          \
    -bfd_registration                        0                          \
    -bfd_registration_mode                   multi_hop                  \
    -vpls_capability_nlri                    $multivalue_nlri_handle    \
    -vpls_filter_nlri                        $multivalue_nlri_handle    \
    -act_as_restarted                        0                          \
    -discard_ixia_generated_routes           0                          \
    -flap_down_time                          0                          \
    -local_router_id_type                    same                       \
    -enable_flap                             0                          \
    -send_ixia_signature_with_routes         0                          \
    -flap_up_time                            0                          \
    -next_hop_enable                         0                          \
    -next_hop_ip                             0.0.0.0                    \
    -advertise_end_of_rib                    0                          \
    -configure_keepalive_timer               0                          \
    -keepalive_timer                         30                         \
]

if {[keylget bgp_ipv6_peer_3_status status] != $::SUCCESS} {
    puts "[info script] $bgp_ipv6_peer_3_status"
}
set bgpIpv6Peer_3_handle [keylget bgp_ipv6_peer_3_status bgp_handle]

############################################
## Network Group Config
############################################

set network_group_5_status [::ixiangpf::network_group_config      \
    -protocol_handle                   $deviceGroup_3_handle      \
    -connected_to_handle               $ethernet_3_handle         \
    -type                              ipv4-prefix                \
    -multiplier                        2                          \
    -enable_device                     1                          \
    -ipv4_prefix_network_address       201.1.0.0                  \
    -ipv4_prefix_network_address_step  0.1.0.0                    \
    -ipv4_prefix_length                24                         \
    -ipv4_prefix_number_of_addresses   2                          ]
    
if {[keylget network_group_5_status status] != $::SUCCESS} {
    puts "[info script] $network_group_5_status"
}
set networkGroup_5_handle [keylget network_group_5_status network_group_handle]

set network_group_6_status [::ixiangpf::network_group_config      \
    -protocol_handle                   $deviceGroup_3_handle      \
    -connected_to_handle               $ethernet_3_handle         \
    -type                              ipv6-prefix                \
    -multiplier                        2                          \
    -enable_device                     1                          \
    -ipv6_prefix_network_address       3000:1:1:1:0:0:0:0         \
    -ipv6_prefix_network_address_step  0:0:1:0:0:0:0:0            \
    -ipv6_prefix_length                64                         \
    -ipv6_prefix_number_of_addresses   2                          ]
    
if {[keylget network_group_6_status status] != $::SUCCESS} {
    puts "[info script] $network_group_6_status"
}
set networkGroup_6_handle [keylget network_group_6_status network_group_handle]

#########################################################################################################################
##                                                     Device Group 4 Config                                           ##
#########################################################################################################################

set device_group_4_status [::ixiangpf::topology_config      \
    -topology_handle              $topology_2_handle        \
    -device_group_name            {D4}                      \
    -device_group_multiplier      2                         \
    -device_group_enabled         1                         \
]
if {[keylget device_group_4_status status] != $::SUCCESS} {
    error $device_group_4_status
}

set deviceGroup_4_handle [keylget device_group_4_status device_group_handle]

############################################
## Ethernet Config
############################################

set multivalue_10_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.14.01.00.00.01       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_10_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_10_status"
}
set multivalue_10_handle [keylget multivalue_10_status multivalue_handle]

set ethernet_4_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 4}               \
    -protocol_handle              $deviceGroup_4_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_10_handle      \
    -vlan                         0                          \
    -vlan_id                      1                          \
    -vlan_id_step                 1                          \
    -vlan_id_count                1                          \
    -vlan_tpid                    0x8100                     \
    -vlan_user_priority           0                          \
    -vlan_user_priority_step      0                          \
    -use_vpn_parameters           0                          \
    -site_id                      0                          \
]
if {[keylget ethernet_4_status status] != $::SUCCESS} {
    puts "[info script] $ethernet_4_status"
}
set ethernet_4_handle [keylget ethernet_4_status ethernet_handle]

############################################
## IPv4 Config
############################################

set multivalue_11_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          30.30.30.2              \
    -counter_step           0.0.1.0                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           0                       \
]
if {[keylget multivalue_11_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_11_status"
}
set multivalue_11_handle [keylget multivalue_11_status multivalue_handle]

set gw_multivalue_7_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          30.30.30.1              \
    -counter_step           0.0.1.0                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget gw_multivalue_7_status status] != $::SUCCESS} {
    puts "[info script] $gw_multivalue_7_status"
}
set gw_multivalue_7_handle [keylget gw_multivalue_7_status multivalue_handle]

set ipv4_4_status [::ixiangpf::interface_config \
    -protocol_name                {IPv4 4}                  \
    -protocol_handle              $ethernet_4_handle        \
    -ipv4_resolve_gateway         1                         \
    -ipv4_manual_gateway_mac      00.00.00.00.00.01         \
    -gateway                      $gw_multivalue_7_handle   \
    -intf_ip_addr                 $multivalue_11_handle     \
    -netmask                      255.255.255.0             \
]
if {[keylget ipv4_4_status status] != $::SUCCESS} {
    puts "[info script] $ipv4_4_status"
}
set ipv4_4_handle [keylget ipv4_4_status ipv4_handle]

############################################
## IPv6 Config
############################################

set multivalue_12_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          3000:0:0:1:0:0:0:2      \
    -counter_step           0:0:0:1:0:0:0:0         \
    -counter_direction      increment               \
    -nest_step              0:0:0:1:0:0:0:0         \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           0                       \
]
if {[keylget multivalue_12_status status] != $::SUCCESS} {
    puts "[info script] $multivalue_12_status"
}
set multivalue_12_handle [keylget multivalue_12_status multivalue_handle]

set gw_multivalue_8_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          3000:0:0:1:0:0:0:1      \
    -counter_step           0:0:0:1:0:0:0:0         \
    -counter_direction      increment               \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget gw_multivalue_8_status status] != $::SUCCESS} {
    puts "[info script] $gw_multivalue_8_status"
}
set gw_multivalue_8_handle [keylget gw_multivalue_8_status multivalue_handle]

set ipv6_4_status [::ixiangpf::interface_config \
    -protocol_name                {IPv6 4}                  \
    -protocol_handle              $ethernet_4_handle        \
    -ipv6_resolve_gateway         1                         \
    -ipv6_manual_gateway_mac      00.00.00.00.00.01         \
    -ipv6_gateway                 $gw_multivalue_8_handle   \
    -ipv6_intf_addr               $multivalue_12_handle     \
    -ipv6_prefix_length           64                        \
]
if {[keylget ipv6_4_status status] != $::SUCCESS} {
    puts "[info script] $ipv6_4_status"
}
set ipv6_4_handle [keylget ipv6_4_status ipv6_handle]

############################################
## BGP Peer Config
############################################

set bgp_ipv4_peer_4_status [::ixiangpf::emulation_bgp_config \
    -mode                                    enable                     \
    -md5_enable                              0                          \
    -handle                                  $ipv4_4_handle             \
    -remote_ip_addr                          30.30.30.1                 \
    -remote_addr_step                        0.0.1.0                    \
    -enable_4_byte_as                        0                          \
    -local_as                                300                        \
    -update_interval                         0                          \
    -count                                   1                          \
    -hold_time                               90                         \
    -neighbor_type                           external                   \
    -graceful_restart_enable                 0                          \
    -restart_time                            45                         \
    -stale_time                              0                          \
    -tcp_window_size                         8192                       \
    -local_router_id_enable                  1                          \
    -ipv4_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv4_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv4_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv4_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv4_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ipv6_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv6_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv6_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv6_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv6_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ttl_value                               64                         \
    -updates_per_iteration                   1                          \
    -bfd_registration                        0                          \
    -bfd_registration_mode                   multi_hop                  \
    -vpls_capability_nlri                    $multivalue_nlri_handle    \
    -vpls_filter_nlri                        $multivalue_nlri_handle    \
    -act_as_restarted                        0                          \
    -discard_ixia_generated_routes           0                          \
    -flap_down_time                          0                          \
    -local_router_id_type                    same                       \
    -enable_flap                             0                          \
    -send_ixia_signature_with_routes         0                          \
    -flap_up_time                            0                          \
    -next_hop_enable                         0                          \
    -next_hop_ip                             0.0.0.0                    \
    -advertise_end_of_rib                    0                          \
    -configure_keepalive_timer               0                          \
    -keepalive_timer                         30                         \
]

if {[keylget bgp_ipv4_peer_4_status status] != $::SUCCESS} {
    puts "[info script] $bgp_ipv4_peer_4_status"
}
set bgpIpv4Peer_4_handle [keylget bgp_ipv4_peer_4_status bgp_handle]

############################################
## BGP+ Peer Config
############################################

set bgp_ipv6_peer_4_status [::ixiangpf::emulation_bgp_config \
    -mode                                    enable                     \
    -md5_enable                              0                          \
    -ip_version                              6                          \
    -handle                                  $ipv6_4_handle             \
    -remote_ipv6_addr                        3000:0:0:1:0:0:0:1         \
    -remote_addr_step                        0:0:0:1:0:0:0:0            \
    -enable_4_byte_as                        0                          \
    -local_as                                300                        \
    -update_interval                         0                          \
    -count                                   1                          \
    -hold_time                               90                         \
    -neighbor_type                           external                   \
    -graceful_restart_enable                 0                          \
    -restart_time                            45                         \
    -stale_time                              0                          \
    -tcp_window_size                         8192                       \
    -local_router_id_enable                  1                          \
    -ipv4_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv4_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv4_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv4_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv4_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ipv6_capability_unicast_nlri            $multivalue_nlri_handle    \
    -ipv6_filter_unicast_nlri                $multivalue_nlri_handle    \
    -ipv6_capability_multicast_nlri          $multivalue_nlri_handle    \
    -ipv6_capability_mpls_nlri               $multivalue_nlri_handle    \
    -ipv6_capability_mpls_vpn_nlri           $multivalue_nlri_handle    \
    -ttl_value                               64                         \
    -updates_per_iteration                   1                          \
    -bfd_registration                        0                          \
    -bfd_registration_mode                   multi_hop                  \
    -vpls_capability_nlri                    $multivalue_nlri_handle    \
    -vpls_filter_nlri                        $multivalue_nlri_handle    \
    -act_as_restarted                        0                          \
    -discard_ixia_generated_routes           0                          \
    -flap_down_time                          0                          \
    -local_router_id_type                    same                       \
    -enable_flap                             0                          \
    -send_ixia_signature_with_routes         0                          \
    -flap_up_time                            0                          \
    -next_hop_enable                         0                          \
    -next_hop_ip                             0.0.0.0                    \
    -advertise_end_of_rib                    0                          \
    -configure_keepalive_timer               0                          \
    -keepalive_timer                         30                         \
]

if {[keylget bgp_ipv6_peer_4_status status] != $::SUCCESS} {
    puts "[info script] $bgp_ipv6_peer_4_status"
}
set bgpIpv6Peer_4_handle [keylget bgp_ipv6_peer_4_status bgp_handle]

############################################
## Network Group Config
############################################

set network_group_7_status [::ixiangpf::network_group_config      \
    -protocol_handle                   $deviceGroup_4_handle      \
    -connected_to_handle               $ethernet_4_handle         \
    -type                              ipv4-prefix                \
    -multiplier                        2                          \
    -enable_device                     1                          \
    -ipv4_prefix_network_address       203.1.0.0                  \
    -ipv4_prefix_network_address_step  0.1.0.0                    \
    -ipv4_prefix_length                24                         \
    -ipv4_prefix_number_of_addresses   2                          ]
    
if {[keylget network_group_7_status status] != $::SUCCESS} {
    puts "[info script] $network_group_7_status"
}
set networkGroup_7_handle [keylget network_group_7_status network_group_handle]

set network_group_8_status [::ixiangpf::network_group_config      \
    -protocol_handle                   $deviceGroup_4_handle      \
    -connected_to_handle               $ethernet_4_handle         \
    -type                              ipv6-prefix                \
    -multiplier                        2                          \
    -enable_device                     1                          \
    -ipv6_prefix_network_address       3000:3:1:1:0:0:0:0         \
    -ipv6_prefix_network_address_step  0:0:1:0:0:0:0:0            \
    -ipv6_prefix_length                64                         \
    -ipv6_prefix_number_of_addresses   2                          ]
    
if {[keylget network_group_8_status status] != $::SUCCESS} {
    puts "[info script] $network_group_8_status"
}
set networkGroup_8_handle [keylget network_group_8_status network_group_handle]

############################################
## Start Protocols
############################################

set protocol_start_status   [::ixia::test_control -action start_all_protocols]

if {[keylget protocol_start_status status] != $::SUCCESS} {
    puts "[info script] $protocol_start_status"
}

puts "Wait for 30 seconds"

after 30000

############################################
## Stats for BGP
############################################

set bgp_stats_1_status [::ixiangpf::emulation_bgp_info                  \
        -handle                          $bgpIpv4Peer_1_handle          \
        -mode                            neighbors                      ]
        
if {[keylget bgp_stats_1_status status] != $::SUCCESS} {
    puts "[info script] $bgp_stats_1_status"
}

set neighbour_list [list 20.20.20.3 20.20.20.4]

if {[keylget bgp_stats_1_status peers] != $neighbour_list} {
    puts "NeighBours retreived are not correct"
    incr cfgErrors
}

set bgp_stats_2_status [::ixiangpf::emulation_bgp_info                  \
        -handle                          $bgpIpv4Peer_2_handle          \
        -mode                            stats_per_device_group         ]
        
if {[keylget bgp_stats_2_status status] != $::SUCCESS} {
    puts "[info script] $bgp_stats_2_status"
}
        
if {[keylget bgp_stats_2_status D2.aggregate.status] != "started"} {
    puts "status info is not correct"
    incr cfgErrors
}

if {[keylget bgp_stats_2_status D2.aggregate.sessions_configured] != "2"} {
    puts "sessions_configured info is not correct"
    incr cfgErrors
}

if {[keylget bgp_stats_2_status D2.aggregate.sessions_established] != "2"} {
    puts "sessions_established info is not correct"
    incr cfgErrors
}

set bgp_stats_3_status [::ixiangpf::emulation_bgp_info                  \
        -handle                          $bgpIpv6Peer_1_handle          \
        -mode                            neighbors                      ]
        
if {[keylget bgp_stats_3_status status] != $::SUCCESS} {
    puts "[info script] $bgp_stats_3_status"
}
     
set neighbour_list [list 2000:0:0:0:0:0:0:3 2000:0:0:0:0:0:0:4]
     
if {[keylget bgp_stats_3_status peers] != $neighbour_list} {
    puts "NeighBours retreived are not correct"
    incr cfgErrors
}

set bgp_stats_4_status [::ixiangpf::emulation_bgp_info                  \
        -handle                          $bgpIpv6Peer_2_handle          \
        -mode                            stats_per_device_group         ]

if {[keylget bgp_stats_4_status status] != $::SUCCESS} {
    puts "[info script] $bgp_stats_4_status"
}

if {[keylget bgp_stats_4_status D2.aggregate.status] != "started"} {
    puts "status info is not correct"
    incr cfgErrors
}

if {[keylget bgp_stats_4_status D2.aggregate.sessions_configured] != "2"} {
    puts "sessions_configured info is not correct"
    incr cfgErrors
}

if {[keylget bgp_stats_4_status D2.aggregate.sessions_established] != "2"} {
    puts "sessions_established info is not correct"
    incr cfgErrors
}

set bgp_clear_stats_1_status [::ixiangpf::emulation_bgp_info    \
        -handle                          $bgpIpv4Peer_3_handle  \
        -mode                            clear_stats            ]

if {[keylget bgp_clear_stats_1_status status] != $::SUCCESS} {
    puts "[info script] $bgp_clear_stats_1_status"
}

after 5000

set bgp_clear_stats_1_status [::ixiangpf::emulation_bgp_info    \
        -handle                          $bgpIpv6Peer_3_handle  \
        -mode                            clear_stats            ]
       
if {[keylget bgp_clear_stats_1_status status] != $::SUCCESS} {
    puts "[info script] $bgp_clear_stats_1_status"
}

after 5000
############################################
## Stop Protocols
############################################

set protocol_stop_status   [::ixia::test_control -action stop_all_protocols]

if {[keylget protocol_stop_status status] != $::SUCCESS} {
    puts "[info script] $protocol_stop_status"
}

puts "Wait for 30 seconds"

after 30000

############################### SUCCESS or FAILURE #############################

if {$cfgErrors > 0} {
    puts "FAIL - $test_name  $cfgErrors Errors- [clock format [clock seconds]]"
    return 0

} else {
    puts "SUCCESS - $test_name - [clock format [clock seconds]]"
    return 1
}
