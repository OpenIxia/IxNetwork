#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2016 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    05/05/2016 - Rupam Paul - created sample                                  #
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
#    than it will retrieve and display few statistics                          #
# Ixia Software:                                                              #
#    IxOS      8.10 EA                                                         #
#    IxNetwork 8.10 EA                                                         #
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

set chassis_ip        {10.216.108.99}
set tcl_server        10.216.108.99
set port_list         {7/1 7/2}
set ixNetwork_client  "10.216.104.58:5555"
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
    -gateway                           20.20.20.1        \
    -gateway_step                      0.0.0.0           \
    -intf_ip_addr                      20.20.20.2        \
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
    -gateway                           20.20.20.2              \
    -gateway_step                      0.0.0.0                 \
    -intf_ip_addr                      20.20.20.1              \
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

puts "Creating BGP Stack on top of IPv4 1 stack on Topology 1 and enabling BGP_LS on it"
set bgp_v4_interface_1_status [::ixiangpf::emulation_bgp_config   \
    -mode                                               create                     \
    -active                                             1                          \
    -md5_enable                                         0                          \
    -handle                                             $ipv4_1_handle             \
    -ip_version                                         4                          \
    -remote_ip_addr                                     20.20.20.1                 \
    -next_hop_enable                                    0                          \
    -next_hop_ip                                        0.0.0.0                    \
    -filter_link_state                                  1                          \
    -capability_linkstate_nonvpn                        1                          \
    -bgp_ls_id                                          300                        \
    -instance_id                                        400                        \
    -number_of_communities                              1                          \
    -enable_community                                   0                          \
    -community_type                                     no_export                  \
    -community_as_number                                0                          \
    -community_last_two_octets                          0                          \
    -number_of_ext_communities                          1                          \
    -enable_ext_community                               0                          \
    -ext_communities_type                               admin_as_two_octet         \
    -ext_communities_subtype                            route_target               \
    -ext_community_as_number                            1                          \
    -ext_community_as_4_bytes                           1                          \
    -ext_community_ip                                   1.1.1.1                    \
    -ext_community_opaque_data                          0                          \
    -enable_override_peer_as_set_mode                   0                          \
    -bgp_ls_as_set_mode                                 include_as_seq             \
    -number_of_as_path_segments                         1                          \
    -enable_as_path_segments                            1                          \
    -enable_as_path_segment                             1                          \
    -number_of_as_number_in_segment                     1                          \
    -as_path_segment_type                               as_set                     \
    -as_path_segment_enable_as_number                   1                          \
    -as_path_segment_as_number                          1                          \
    -number_of_clusters                                 1                          \
    -enable_cluster                                     0                          \
    -cluster_id                                         0.0.0.0                    \
    ]
if {[keylget bgp_v4_interface_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_v4_interface_1_status log]"
    return 0
}

set bgpInterface_1_handle [keylget bgp_v4_interface_1_status bgp_handle]



puts "Creating BGP Stack on top of IPv4 1 stack on Topology 2 and enabling BGP_LS on it"
set bgp_v4_interface_2_status [::ixiangpf::emulation_bgp_config   \
    -mode                                               create                     \
    -active                                             1                          \
    -md5_enable                                         0                          \
    -handle                                             $ipv4_2_handle             \
    -ip_version                                         4                          \
    -remote_ip_addr                                     20.20.20.2                 \
    -next_hop_enable                                    0                          \
    -next_hop_ip                                        0.0.0.0                    \
    -filter_link_state                                  1                          \
    -capability_linkstate_nonvpn                        1                          \
    -bgp_ls_id                                          300                        \
    -instance_id                                        400                        \
    -number_of_communities                              1                          \
    -enable_community                                   0                          \
    -community_type                                     no_export                  \
    -community_as_number                                0                          \
    -community_last_two_octets                          0                          \
    -number_of_ext_communities                          1                          \
    -enable_ext_community                               0                          \
    -ext_communities_type                               admin_as_two_octet         \
    -ext_communities_subtype                            route_target               \
    -ext_community_as_number                            1                          \
    -ext_community_as_4_bytes                           1                          \
    -ext_community_ip                                   1.1.1.1                    \
    -ext_community_opaque_data                          0                          \
    -enable_override_peer_as_set_mode                   0                          \
    -bgp_ls_as_set_mode                                 include_as_seq             \
    -number_of_as_path_segments                         1                          \
    -enable_as_path_segments                            1                          \
    -enable_as_path_segment                             1                          \
    -number_of_as_number_in_segment                     1                          \
    -as_path_segment_type                               as_set                     \
    -as_path_segment_enable_as_number                   1                          \
    -as_path_segment_as_number                          1                          \
    -number_of_clusters                                 1                          \
    -enable_cluster                                     0                          \
    -cluster_id                                         0.0.0.0                    \
    ]
	
if {[keylget bgp_v4_interface_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_v4_interface_2_status log]"
    return 0
}

set bgpInterface_2_handle [keylget bgp_v4_interface_2_status bgp_handle]

puts "Creating OSPFv2 Stack on top of IPv4 1 stack on Topology 1"
set ospfv2_1_status [::ixiangpf::emulation_ospf_config \
    -handle                                                    $ipv4_1_handle            \
    -area_id                                                   0.0.0.0                   \
    -area_id_as_number                                         0                         \
    -area_id_type                                              number                    \
    -authentication_mode                                       null                      \
    -dead_interval                                             40                        \
    -hello_interval                                            10                        \
    -router_interface_active                                   1                         \
    -enable_fast_hello                                         0                         \
    -hello_multiplier                                          2                         \
    -max_mtu                                                   1500                      \
    -protocol_name                                             {OSPFv2-IF 1}             \
    -router_active                                             1                         \
    -router_asbr                                               0                         \
    -do_not_generate_router_lsa                                0                         \
    -router_abr                                                0                         \
    -inter_flood_lsupdate_burst_gap                            33                        \
    -lsa_refresh_time                                          1800                      \
    -lsa_retransmit_time                                       5                         \
    -max_ls_updates_per_burst                                  1                         \
    -oob_resync_breakout                                       0                         \
    -interface_cost                                            10                        \
    -lsa_discard_mode                                          1                         \
    -md5_key_id                                                1                         \
    -network_type                                              ptop                      \
    -mode                                                      create                    \
    ]

if {[keylget ospfv2_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospfv2_1_status log]"
    return 0
}

puts "Creating OSPFv2 Stack on top of IPv4 1 stack on Topology 2"
set ospfv2_2_status [::ixiangpf::emulation_ospf_config \
        -handle                                                    $ipv4_2_handle            \
        -area_id                                                   0.0.0.0                   \
        -area_id_as_number                                         0                         \
        -area_id_type                                              number                    \
        -authentication_mode                                       null                      \
        -dead_interval                                             40                        \
        -hello_interval                                            10                        \
        -router_interface_active                                   1                         \
        -enable_fast_hello                                         0                         \
        -hello_multiplier                                          2                         \
        -max_mtu                                                   1500                      \
        -protocol_name                                             {OSPFv2-IF 1}             \
        -router_active                                             1                         \
        -router_asbr                                               0                         \
        -do_not_generate_router_lsa                                0                         \
        -router_abr                                                0                         \
        -inter_flood_lsupdate_burst_gap                            33                        \
        -lsa_refresh_time                                          1800                      \
        -lsa_retransmit_time                                       5                         \
        -max_ls_updates_per_burst                                  1                         \
        -oob_resync_breakout                                       0                         \
        -interface_cost                                            10                        \
        -lsa_discard_mode                                          1                         \
        -md5_key_id                                                1                         \
        -network_type                                              ptop                      \
        -mode                                                      create                    \
    ]

if {[keylget ospfv2_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospfv2_2_status log]"
    return 0
}

############################################
## Network Group Config
############################################

set network_group_1_status [::ixiangpf::network_group_config      \
    -protocol_handle                   $deviceGroup_2_handle      \
	-protocol_name                     {Direct/Static Routes}     \
    -connected_to_handle               $ethernet_2_handle         \
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
    -protocol_handle                   $deviceGroup_2_handle      \
	-protocol_name                     {IPv6 Prefix NLRI}         \
    -connected_to_handle               $ethernet_2_handle         \
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

set network_group_3_status [::ixiangpf::network_group_config      \
    -protocol_handle                   $deviceGroup_2_handle      \
	-protocol_name                     {IPv4 Prefix NLRI}         \
    -connected_to_handle               $ethernet_2_handle         \
    -type                              ipv4-prefix                \
    -multiplier                        2                          \
    -enable_device                     1                          \
    -ipv4_prefix_network_address       200.1.0.0                  \
    -ipv4_prefix_network_address_step  0.1.0.0                    \
    -ipv4_prefix_length                24                         \
    -ipv4_prefix_number_of_addresses   2                          ]
    
if {[keylget network_group_3_status status] != $::SUCCESS} {
    puts "[info script] $network_group_3_status"
}
set networkGroup_3_handle [keylget network_group_3_status network_group_handle]


set network_group_4_status [::ixiangpf::network_group_config      \
    -protocol_handle                   $deviceGroup_2_handle      \
    -protocol_name                     {Node/Link/Prefix NLRI}    \
    -multiplier                        1                          \
    -enable_device                     1                          \
    -type                              mesh                       \
    -mesh_number_of_nodes              3                          \
    -mesh_include_emulated_device      0                          \
    -mesh_link_multiplier              1                          \
    ]
    if {[keylget network_group_4_status status] != $::SUCCESS} {
        puts "[info script] $network_group_4_status"
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
# OTF changing the valye of BGPLS ID & Instance ID                         #
############################################################################
	
puts "Changing BGPLS ID and Instance ID On The Fly"
set bgp_v4_interface_2_status [::ixiangpf::emulation_bgp_config                    \
    -mode                                               modify                     \
    -active                                             1                          \
    -md5_enable                                         0                          \
    -handle                                             $bgpInterface_2_handle     \
    -ip_version                                         4                          \
    -bgp_ls_id                                          700                        \
    -instance_id                                        800                        \
    ]
	
if {[keylget bgp_v4_interface_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_v4_interface_2_status log]"
    return 0
}
	
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