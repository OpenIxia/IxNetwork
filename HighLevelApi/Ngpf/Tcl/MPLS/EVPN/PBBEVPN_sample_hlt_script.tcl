################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright 1997 - 2016 by IXIA                                             #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    15/06/2016 - Poulomi Chatterjee - created sample                          #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL NOTICE:                                 #
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
# meet the user’s requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT IS WITH THE  #
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
#    This script intends to demonstrate how to use NGPF PBB EVPN HLAPI.        #
#                                                                              #
# 1. It will create 2 PBB EVPN topologies in following way.                    #
#   - Configure LDP in each connected Device Group.                            #
#   - Configure OSPF in connected Devicr Group to Advertise Loopback Address   #
#       of BGP.                                                                #
#   - Configure Network Groups behind each Device Groups.                      #
#   - Add chained Device Group behind each Network Group, add IPv4 Loopback in #
#      these Device Groups.                                                    #
#   - Configure BGP Peer over IPv4 Loopback.                                   #
#   - Configure EVI(PBB) stack over BGP.                                       #
#   - Configure MAC Pools behing PBB EVPN Device Group.                        #
# 2. Start all protocol.                                                       #
# 3. Retrieve protocol statistics.                                             #
# 4. Retrieve protocol learned info.                                           #
# 5. Configure L2-L3 traffic.                                                  #
# 6. Start the L2-L3 traffic.                                                  #
# 7. Retrieve L2-L3 traffic stats.                                             #
# 8. Stop L2-L3 traffic.                                                       #
# 9. Stop allprotocols.                                                        #
#                                                                              #
# Ixia Software:                                                               #
#    IxOS      8.10-EB                                                         #
#    IxNetwork 8.10-EB                                                         #
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
# Connection to the chassis, IxNetwork Tcl Server                              #
################################################################################
set chassis_ip        {10.216.108.82}
set tcl_server        10.216.108.82
set port_list         {7/7 7/8}
set ixNetwork_client  "10.216.108.100:8005"
set test_name         [info script]

puts "Start Connecting to chassis ..."
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

# Creating a topology in first port
puts "Adding topology:1 in port 1\n" 
set topology_1_status [::ixiangpf::topology_config \
    -topology_name      {PBB-EVPN Topology 1}      \
    -port_handle        "$port1"      \
]
if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_1_status log]"
}
set topology_1_handle [keylget topology_1_status topology_handle]

# Creating  device group 1 in topology 1
puts "Creating device group 1 in topology 1\n"
set device_group_1_status [::ixiangpf::topology_config    \
    -topology_handle              $topology_1_handle      \
    -device_group_name            {Provider Router 1}     \
    -device_group_multiplier      1                       \
    -device_group_enabled         1                       \
]

if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_1_status log]"
    return 0
}

set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

# Creating a topology in second port
puts "Adding topology 2 in port 2\n"
set topology_2_status [::ixiangpf::topology_config \
    -topology_name      {PBB-EVPN Topology 2}      \
    -port_handle        "$port2"      \
] 
if {[keylget topology_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_2_status log]"
    return 0
}
set topology_2_handle [keylget topology_2_status topology_handle]

# Creating device group 2 in topology 2
puts "Creating device group 2 in topology 2\n"
set device_group_4_status [::ixiangpf::topology_config    \
    -topology_handle              $topology_2_handle      \
    -device_group_name            {Provider Router 2}     \
    -device_group_multiplier      1                       \
    -device_group_enabled         1                       \
]
if {[keylget device_group_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_4_status log]"
    retun 0
}
set deviceGroup_4_handle [keylget device_group_4_status device_group_handle]

################################################################################
#  Configure protocol interfaces                                               #
################################################################################

# Creating ethernet stack in device group 1
puts "Creating ethernet stack in first device group\n"
set ethernet_1_status [::ixiangpf::interface_config \
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

# Creating ethernet stack in device group 2
puts "Creating ethernet stack in second device group\n"
set ethernet_2_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 2}               \
    -protocol_handle              $deviceGroup_4_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 18.03.73.c7.6c.01          \
    -src_mac_addr_step            00.00.00.00.00.00          \
]
if {[keylget ethernet_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_2_status log]"
    return 0
}
set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]

# Creating IPv4 Stack on top of Ethernet Stack
puts "Creating IPv4  stack on first ethernet stack\n"    
set ipv4_1_status [::ixiangpf::interface_config \
    -protocol_name                     {IPv4 1}                \
    -protocol_handle                   $ethernet_1_handle      \
    -ipv4_resolve_gateway              1                       \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01       \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00       \
    -gateway                           20.20.20.1              \
    -gateway_step                      0.0.0.0                 \
    -intf_ip_addr                      20.20.20.2              \
    -intf_ip_addr_step                 0.0.0.0                 \
    -netmask                           255.255.255.0           \
]
if {[keylget ipv4_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_1_status log]"
    return 0
}
set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]

# Creating IPv4 Stack on top of Ethernet Stack
puts "Creating IPv4 stack on second ethernet stack\n"    
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
# Configure PBB EVPN Topologies in both ports as described in Description Sec- #
#  tion above.                                                                 #
################################################################################ 

#Creating LDP Stack on top of ipv4 1 stack
puts "Creating LDP Stack on top of ipv4 1 stack\n"
set ldp_basic_router_1_status [::ixiangpf::emulation_ldp_config \
    -handle                       $ipv4_1_handle            \
    -mode                         create                    \
    -label_adv                    unsolicited               \
    -lsr_id                       192.0.0.1                 \
    -interface_name               {LDP-IF 1}                \
    -interface_multiplier         1                         \
    -interface_active             1                         \
    -router_name                  {LDP 1}                   \
    -router_multiplier            1                         \
    -router_active                1                         \
]
 
if {[keylget ldp_basic_router_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ldp_basic_router_1_status log]"
    return 0
}
    
set ldp_connected_interface_1_status [::ixiangpf::emulation_ldp_config \
    -handle                    $ipv4_1_handle      \
    -mode                      create              \
    -label_adv                 unsolicited         \
    -interface_name            {LDP-IF 1}          \
    -interface_multiplier      1                   \
    -interface_active          1                   \
]
if {[keylget ldp_connected_interface_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ldp_basic_router_1_status log]"
    return 0
}
set ldpConnectedInterface_1_handle [keylget ldp_connected_interface_1_status ldp_connected_interface_handle]

#Creating OSPF Stack on top of ipv4 1 stack
puts "Creating OSPF Stack on top of ipv4 1 stack"
set ospfv2_1_status [::ixiangpf::emulation_ospf_config \
    -handle                                                    $ipv4_1_handle            \
    -area_id                                                   0.0.0.0                   \
    -area_id_as_number                                         0                         \
    -area_id_type                                              number                    \
    -router_interface_active                                   1                         \
    -protocol_name                                             {OSPFv2-IF 1}             \
    -router_active                                             1                         \
    -lsa_discard_mode                                          1                         \
    -network_type                                              ptop                      \
    -external_capabilities                                     1                         \
    -router_id                                                 192.0.0.1                 \
    -mode                                                      create                    \
]
if {[keylget ospfv2_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospfv2_1_status log]"
    return 0
}
set ospfv2_1_handle [keylget ospfv2_1_status ospfv2_handle]
  
#Adding IPv4 Prefix Pools behind first DG
puts "Adding IPv4 Prefix Pools behind first DG"

set network_group_1_status [::ixiangpf::network_group_config \
    -protocol_handle                       $deviceGroup_1_handle      \
    -protocol_name                         {Network Group 1}          \
    -multiplier                            1                          \
    -enable_device                         1                          \
    -connected_to_handle                   $ethernet_1_handle         \
    -type                                  ipv4-prefix                \
    -ipv4_prefix_network_address           2.2.2.2                    \
    -ipv4_prefix_network_address_step      0.0.0.0                    \
    -ipv4_prefix_length                    32                         \
    -ipv4_prefix_multiplier                1                          \
]
if {[keylget network_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_1_status log]"
    return 0
}
set networkGroup_1_handle [keylget network_group_1_status network_group_handle]

# Configuring OSPF Prefix Pool Parameters   
puts "Configuring OSPF Prefix Pool Parameters"
set network_group_2_status [::ixiangpf::emulation_ospf_network_group_config \
    -handle                           $networkGroup_1_handle      \
    -mode                             modify                      \
    -ipv4_prefix_metric               0                           \
    -ipv4_prefix_active               1                           \
    -ipv4_prefix_allow_propagate      0                           \
    -ipv4_prefix_route_origin         another_area                \
]
if {[keylget network_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_2_status log]"
    return 0
}
    
# Configuring LDP Prefix Pool Parameters   
puts "Configuring LDP Prefix Pool Parameters"
set network_group_3_status [::ixiangpf::emulation_ldp_route_config \
    -mode                   modify                      \
    -handle                 $networkGroup_1_handle      \
    -egress_label_mode      fixed                       \
    -fec_type               ipv4_prefix                 \
    -label_value_start      101        \
    -lsp_handle             $networkGroup_1_handle      \
    -fec_active             1                           \
    -fec_name               {LDP FEC Range 1}           \
] 
if {[keylget network_group_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_3_status log]"
    return 0
}

# Add DG2 behind IPv4 Prefix Pool
puts "Add DG2 behind IPv4 Prefix Pool"
set device_group_2_status [::ixiangpf::topology_config \
    -device_group_name            {PE 1}                      \
    -device_group_multiplier      1                           \
    -device_group_enabled         1                           \
    -device_group_handle          $networkGroup_1_handle      \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_2_status log]"
    return 0
}
set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]
    
set multivalue_6_status [::ixiangpf::multivalue_config \
    -pattern                counter                                                              \
    -counter_start          2.2.2.2                                                              \
    -counter_step           0.0.0.1                                                              \
    -counter_direction      increment                                                            \
    -nest_step              0.0.0.1,0.0.0.1,0.1.0.0                                              \
    -nest_owner             $networkGroup_1_handle,$deviceGroup_1_handle,$topology_1_handle      \
    -nest_enabled           0,0,1                                                                \
]
if {[keylget multivalue_6_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_6_status log]"
    return 0
}
set multivalue_6_handle [keylget multivalue_6_status multivalue_handle]
    
# Add ipv4 loopback in DG2
puts "Add ipv4 loopback in DG2"
set ipv4_loopback_1_status [::ixiangpf::interface_config \
    -protocol_name            {IPv4 Loopback 1}           \
    -protocol_handle          $deviceGroup_2_handle       \
    -enable_loopback          1                           \
    -connected_to_handle      $networkGroup_1_handle      \
    -intf_ip_addr             $multivalue_6_handle        \
    -netmask                  255.255.255.255             \
]
if {[keylget ipv4_loopback_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_loopback_1_status log]"
    return 0
}
set ipv4Loopback_1_handle [keylget ipv4_loopback_1_status ipv4_loopback_handle]

# Adding BGP peer over ipv4 Loopback
puts "Adding BGP peer over ipv4 Loopback"
set bgp_ipv4_peer_1_status [::ixiangpf::emulation_bgp_config \
    -mode                                               enable                      \
    -active                                             1                           \
    -handle                                             $ipv4Loopback_1_handle      \
    -ip_version                                         4                           \
    -local_as                                           100                         \
    -count                                              1                           \
    -local_router_id                                    2.2.2.2                     \
    -remote_loopback_ip_addr                            3.2.2.2                     \
    -neighbor_type                                      internal                    \
    -local_router_id_enable                             1                           \
    -local_router_id_type                               same                        \
    -ethernet_segments_count                            1                           \
    -filter_evpn                                        1                           \
    -evpn                                               1                           \
    -operational_model                                  symmetric                   \
]
if {[keylget bgp_ipv4_peer_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_ipv4_peer_1_status log]"
    return 0
}
set bgpIpv4Peer_1_handle [keylget bgp_ipv4_peer_1_status bgp_handle]

# Add EVI(PBB) stack on top of BGP
puts "Add EVI(PBB) stack on top of BGP"
set bgp_i_pv4_evpn_pbb_1_status [::ixiangpf::emulation_bgp_route_config \
    -handle      $bgpIpv4Peer_1_handle      \
    -mode        create                     \
    -pbb_evpn    1                          \
]
if {[keylget bgp_i_pv4_evpn_pbb_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_i_pv4_evpn_pbb_1_status log]"
    return 0
}
set bgpIPv4EvpnPbb_1_handle [keylget bgp_i_pv4_evpn_pbb_1_status evpn_evi]

# Configure BGP Ethernet Segment stack 
puts "Configure BGP Ethernet Segment stack"
set bgpEthernetSegmentV4_1_status [::ixiangpf::emulation_bgp_config \
    -mode                                               modify                        \
    -handle                                             $bgpIpv4Peer_1_handle         \
    -active_ethernet_segment                            1                             \
    -esi_type                                           type0                         \
    -esi_value                                          1                             \
    -esi_label                                          16                            \
    -advertise_inclusive_multicast_route                1                             \
    -b_mac_prefix                                       b0.11.01.00.00.03             \
    -b_mac_prefix_length                                48                            \
    -evis_count                                         1                             \
    -enable_next_hop                                    1                             \
    -set_next_hop                                       sameaslocalip                 \
    -set_next_hop_ip_type                               ipv4                          \
    -enable_origin                                      1                             \
    -origin                                             igp                           \
    -ethernet_segment_name                              {BGP Ethernet Segment 1}      \
]
if {[keylget bgpEthernetSegmentV4_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgpEthernetSegmentV4_1_status log]"
    return 0
}

# Configure EVI parameters
puts "Configure EVI parameters"
set bgpIPv4EvpnPbb_2_status_modify [::ixiangpf::emulation_bgp_route_config \
    -handle                                           $bgpIpv4Peer_1_handle             \
    -mode                                             modify                            \
    -active                                           1                                 \
    -origin                                           igp                               \
    -num_broadcast_domain                             1                                 \
    -auto_configure_rd_ip_address                     1                                 \
    -enable_next_hop                                  1                                 \
    -set_next_hop                                     sameaslocalip                     \
    -set_next_hop_ip_type                             ipv4                              \
    -b_mac_first_label                                16                                \
    -enable_b_mac_second_label                        0                                 \
    -b_mac_second_label                               16                                \
    -pbb_evpn                                         1                                 \
    -no_of_mac_pools                                  1                                 \
    -enable_broadcast_domain                          1                                 \
]
if {[keylget bgpIPv4EvpnPbb_2_status_modify status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgpIPv4EvpnPbb_2_status_modify log]"
    return 0
}
    
# Create MAC/IP Pool behind PE Router 1
puts "Create MAC/IP Pool behind PE Router 1"

set network_group_4_status [::ixiangpf::network_group_config \
    -protocol_handle                       $deviceGroup_2_handle         \
    -protocol_name                         MAC_IP_1                      \
    -multiplier                            1                             \
    -enable_device                         1                             \
    -connected_to_handle                   $bgpIPv4EvpnPbb_1_handle      \
    -type                                  mac-pools                     \
    -mac_pools_multiplier                  1                             \
    -mac_pools_prefix_length               48                            \
    -mac_pools_mac                         A0:11:01:00:00:03             \
]
if {[keylget network_group_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_4_status log]"
    return 0
}
set networkGroup_4_handle [keylget network_group_4_status network_group_handle]

puts "Configuration complete in port 1..."

###############################################################################
#Creating LDP Stack on top of ipv4 2 stack                                    #
###############################################################################
puts "Creating LDP Stack on top of ipv4 2 stack\n"

set ldp_basic_router_2_status [::ixiangpf::emulation_ldp_config \
    -handle                       $ipv4_2_handle             \
    -mode                         create                     \
    -label_adv                    unsolicited                \
    -lsr_id                       194.0.0.1                  \
    -label_space                  0                          \
    -hello_interval               5                          \
    -hello_hold_time              15                         \
    -keepalive_interval           15                         \
    -keepalive_holdtime           45                         \
    -auth_mode                    null                       \
    -bfd_registration             0                          \
    -graceful_restart_enable      0                          \
    -reconnect_time               120000                     \
    -recovery_time                120000                     \
    -interface_name               {LDP-IF 2}                 \
    -interface_multiplier         1                          \
    -interface_active             1                          \
    -router_name                  {LDP 2}                    \
    -router_multiplier            1                          \
    -router_active                1                          \
]
if {[keylget ldp_basic_router_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ldp_basic_router_2_status log]"
    return 0
}
    
set ldp_connected_interface_2_status [::ixiangpf::emulation_ldp_config \
    -handle                    $ipv4_2_handle      \
    -mode                      create              \
    -label_adv                 unsolicited         \
    -label_space               0                   \
    -hello_interval            5                   \
    -hello_hold_time           15                  \
    -auth_mode                 null                \
    -bfd_registration          0                   \
    -interface_name            {LDP-IF 2}          \
    -interface_multiplier      1                   \
    -interface_active          1                   \
]
if {[keylget ldp_connected_interface_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ldp_connected_interface_2_status log]"
    return 0
}
set ldpConnectedInterface_2_handle [keylget ldp_connected_interface_2_status ldp_connected_interface_handle]

#Creating OSPF Stack on top of ipv4 2 stack
puts "Creating OSPF Stack on top of ipv4 2 stack"
set ospfv2_2_status [::ixiangpf::emulation_ospf_config \
     -handle                                                    $ipv4_2_handle             \
     -protocol_name                                             {OSPFv2-IF 2}              \
     -router_active                                             1                          \
     -network_type                                              ptop                       \
     -router_id                                                 194.0.0.1                  \
     -mode                                                      create                     \
]
if {[keylget ospfv2_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospfv2_2_status log]"
    return 0
}
set ospfv2_2_handle [keylget ospfv2_2_status ospfv2_handle]

#Adding IPv4 Prefix Pools behind first DG
puts "Adding IPv4 Prefix Pools behind first DG"
set network_group_6_status [::ixiangpf::network_group_config \
    -protocol_handle                       $deviceGroup_4_handle      \
    -protocol_name                         {Network Group 2}          \
    -multiplier                            1                          \
    -enable_device                         1                          \
    -connected_to_handle                   $ethernet_2_handle         \
    -type                                  ipv4-prefix                \
    -ipv4_prefix_network_address           3.2.2.2                    \
    -ipv4_prefix_network_address_step      0.0.0.0                    \
    -ipv4_prefix_length                    32                         \
    -ipv4_prefix_multiplier                1                          \
]
if {[keylget network_group_6_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_6_status log]"
    return 0
}
set networkGroup_6_handle [keylget network_group_6_status network_group_handle]

# Configuring OSPF Prefix Pool Parameters
puts "Configuring OSPF Prefix Pool Parameters"
set network_group_7_status [::ixiangpf::emulation_ospf_network_group_config \
    -handle                           $networkGroup_6_handle      \
    -mode  	                           modify                      \
    -ipv4_prefix_metric               0                           \
    -ipv4_prefix_active               1                           \
    -ipv4_prefix_allow_propagate      0                           \
    -ipv4_prefix_route_origin         another_area                \
]
if {[keylget network_group_7_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_7_status log]"
    return 0
}
# Configuring LDP Prefix Pool Parameters
puts "Configuring LDP Prefix Pool Parameters"
set network_group_8_status [::ixiangpf::emulation_ldp_route_config \
    -mode                   modify                      \
    -handle                 $networkGroup_6_handle      \
    -egress_label_mode      fixed                       \
    -fec_type               ipv4_prefix                 \
    -label_value_start      201                         \
    -lsp_handle             $networkGroup_6_handle      \
    -packing_enable         0                           \
    -fec_active             1                           \
    -fec_name               {LDP FEC Range 2}           \
]
if {[keylget network_group_8_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_8_status log]"
    return 0
}

# Add DG2 behind IPv4 Prefix Pool
puts "Add DG2 behind IPv4 Prefix Pool"
set device_group_5_status [::ixiangpf::topology_config \
    -device_group_name            {PE 2}                      \
    -device_group_multiplier      1                           \
    -device_group_enabled         1                           \
    -device_group_handle          $networkGroup_6_handle      \
]
if {[keylget device_group_5_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_5_status log]"
    return 0
}
set deviceGroup_5_handle [keylget device_group_5_status device_group_handle]

set multivalue_32_status [::ixiangpf::multivalue_config \
     -pattern                counter                                                              \
     -counter_start          3.2.2.2                                                              \
     -counter_step           0.0.0.1                                                              \
     -counter_direction      increment                                                            \
     -nest_step              0.0.0.1,0.0.0.1,0.1.0.0                                              \
     -nest_owner             $networkGroup_6_handle,$deviceGroup_4_handle,$topology_2_handle      \
     -nest_enabled           0,0,1                                                                \
]
if {[keylget multivalue_32_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_32_status log]"
    return 0
}
set multivalue_32_handle [keylget multivalue_32_status multivalue_handle]

# Add ipv4 loopback in DG2
puts "Add ipv4 loopback in DG2"
set ipv4_loopback_2_status [::ixiangpf::interface_config \
    -protocol_name            {IPv4 Loopback 2}           \
    -protocol_handle          $deviceGroup_5_handle       \
    -enable_loopback          1                           \
    -connected_to_handle      $networkGroup_6_handle      \
    -intf_ip_addr             $multivalue_32_handle       \
    -netmask                  255.255.255.255             \
]
if {[keylget ipv4_loopback_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_loopback_2_status log]"
    return 0
}
set ipv4Loopback_2_handle [keylget ipv4_loopback_2_status ipv4_loopback_handle]

# Adding BGP peer over ipv4 Loopback
puts "Adding BGP peer over ipv4 Loopback"
set bgp_ipv4_peer_2_status [::ixiangpf::emulation_bgp_config \
    -mode                                               enable                      \
    -active                                             1                           \
    -handle                                             $ipv4Loopback_2_handle      \
    -ip_version                                         4                           \
    -local_as                                           100                         \
    -count                                              1                           \
    -local_router_id                                    3.2.2.2                     \
    -remote_loopback_ip_addr                            2.2.2.2                     \
    -neighbor_type                                      internal                    \
    -local_router_id_enable                             1                           \
    -local_router_id_type                               same                        \
    -ethernet_segments_count                            1                           \
    -filter_evpn                                        1                           \
    -evpn                                               1                           \
    -operational_model                                  symmetric                   \
]
if {[keylget bgp_ipv4_peer_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_ipv4_peer_2_status log]"
    return 0
}
set bgpIpv4Peer_2_handle [keylget bgp_ipv4_peer_2_status bgp_handle]

# Add EVI(PBB) stack on top of BGP
puts "Add EVI(PBB) stack on top of BGP"

set bgp_i_pv4_evpn_pbb_3_status [::ixiangpf::emulation_bgp_route_config \
    -handle      $bgpIpv4Peer_2_handle      \
    -mode        create                     \
    -pbb_evpn    1                          \
]
if {[keylget bgp_i_pv4_evpn_pbb_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_i_pv4_evpn_pbb_3_status log]"
    return 0
}
set bgpIPv4EvpnPbb_3_handle [keylget bgp_i_pv4_evpn_pbb_3_status evpn_evi]

# Configure BGP Ethernet Segment stack
puts "Configure BGP Ethernet Segment stack"
set bgpEthernetSegmentV4_2_status [::ixiangpf::emulation_bgp_config \
    -mode                                               modify                        \
    -handle                                             $bgpIpv4Peer_2_handle         \
    -active_ethernet_segment                            1                             \
    -esi_type                                           type0                         \
    -esi_value                                          2                             \
    -support_multihomed_es_auto_discovery               1                             \
    -evis_count                                         1                             \
    -b_mac_prefix                                       b0.12.01.00.00.03             \
    -b_mac_prefix_length                                48                            \
    -no_of_b_mac_mapped_ips                             0                             \
    -enable_next_hop                                    1                             \
    -set_next_hop                                       sameaslocalip                 \
    -set_next_hop_ip_type                               ipv4                          \
    -ethernet_segment_name                              {BGP Ethernet Segment 2}      \
]
if {[keylget bgpEthernetSegmentV4_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgpEthernetSegmentV4_2_status log]"
    return 0
}

# Configure EVI parameters
puts "Configure EVI parameters"
set bgpIPv4EvpnPbb_4_status_modify [::ixiangpf::emulation_bgp_route_config \
    -handle                                           $bgpIpv4Peer_2_handle             \
    -mode                                             modify                            \
    -active                                           1                                 \
    -pbb_evpn                                         1                                 \
    -no_of_mac_pools                                  1                                 \
    -enable_broadcast_domain                          1                                 \
    -b_mac_first_label                                16                                \
    -enable_b_mac_second_label                        0                                 \
    -b_mac_second_label                               16                                \
]
if {[keylget bgpIPv4EvpnPbb_4_status_modify status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgpIPv4EvpnPbb_4_status_modify log]"
    return 0
}

# Create MAC/IP Pool behind PE Router 2
puts "Create MAC/IP Pool behind PE Router 2"
set network_group_9_status [::ixiangpf::network_group_config \
    -protocol_handle                       $deviceGroup_5_handle         \
    -protocol_name                         MAC_IP_2                      \
    -multiplier                            1                             \
    -enable_device                         1                             \
    -connected_to_handle                   $bgpIPv4EvpnPbb_3_handle      \
    -type                                  mac-pools	                 \
    -mac_pools_multiplier                  1                             \
    -mac_pools_prefix_length               48                            \
    -mac_pools_mac                         A0:12:01:00:00:03             \
]
if {[keylget network_group_9_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_9_status log]"
    return 0
}
set networkGroup_9_handle [keylget network_group_9_status network_group_handle]

puts "Configuration complete in port 2..."

###########################################################################
# Start protocols                                                         #
############################################################################

puts "Starting all protocol(s) ...\n"
set r [::ixia::test_control -action start_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}

puts "Waiting for 120 seconds\n"
after 120000

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
puts "Fetching BGP statistics\n"
# Check Stats using BGP Router handle
puts {Check Stats using BGP Router handle ...}
set bgp_stats [::ixiangpf::emulation_bgp_info \
    -handle $bgpIpv4Peer_1_handle             \
    -mode stats]
if {[keylget bgp_stats status] != $::SUCCESS} {
    puts "FAILED"
    return $::FAILED
}
foreach stat $bgp_stats {
    puts "=================================================================="
    puts "$stat\n"
    puts "=================================================================="
}

############################################################################
# Retrieve protocol learned info                                           #
############################################################################
puts "Fetching EVPN  learned info\n"
# Check Learned Info for port 2 using BGP Router handle
puts {Check Learned Info using BGP Router handle ...\n}
set bgp_linfo [::ixiangpf::emulation_bgp_info \
    -handle $bgpIpv4Peer_1_handle             \
    -mode learned_info]

if {[keylget bgp_linfo status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_linfo log]"
    return $::FAILED
}
foreach info $bgp_linfo {
    puts "=================================================================="
    puts "$info\n"
    puts "=================================================================="
}
set linfo [keylget bgp_linfo /topology:1/deviceGroup:1/networkGroup:1/deviceGroup:1/ipv4Loopback:1/bgpIpv4Peer:1/item:1]
set evpn_linfo [keylget linfo learned_info]
foreach  table $evpn_linfo {
    puts "=================================================================="
    puts "$table"
    puts "=================================================================="
}
after 5000
############################################################################
# Configure L2-L3 traffic                                                  #
############################################################################
puts "Configure L2-L3 traffic\n"
# Configure L2-L3 IPv4 Traffic
puts {Configuring traffic for traffic item: //traffic/trafficItem:<1>}

puts "Configuring L2-L3 IPv4 Traffic item ...\n"
set _result_ [::ixia::traffic_config \
    -mode                                     create                          \
    -traffic_generator                        ixnetwork_540                   \
    -endpointset_count                        1                               \
    -emulation_src_handle                     [list $networkGroup_4_handle]   \
    -emulation_dst_handle                     [list $networkGroup_9_handle]   \
    -name                                     Traffic_Item_1                  \
    -circuit_endpoint_type                    ethernet_vlan                   \
    -rate_pps                                 100                             \
    -track_by                                 {trackingenabled0 mplsFlowDescriptor0}
]

if {[keylget _result_ status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result_ log]"
    return 0
}

puts "traffic $_result_"
puts "Configured L2-L3 IPv4 traffic item!!!\n"

############################################################################
#  Start L2-L3 traffic configured earlier                                  #
############################################################################
puts "\n Running L2-L3 Traffic..."
set r [::ixia::traffic_control \
    -action run \
    -traffic_generator ixnetwork_540 \
    -type l23  \
]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "\n Let the traffic run for 20 seconds ..."
after 20000
############################################################################
# Retrieve L2-L3 traffic stats                                             #
############################################################################
puts "Retrieving traffic stats"
set r [::ixia::traffic_stats        \
    -mode all                       \
    -traffic_generator ixnetwork_540\
    -measure_mode mixed             \
]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}

foreach stat $r {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}

############################################################################
# Stop L2-L3 traffic started earlier                                       #
############################################################################
puts "Stopping L2-L3 Traffic..."
set r [::ixia::traffic_control \
    -action stop \
    -traffic_generator ixnetwork_540 \
    -type l23 \
]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
after 5000

############################################################################
# Stop all protocols                                                       #
############################################################################
puts "Stopping all protocol(s) ..."
set r [::ixia::test_control -action stop_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "!!! Test Script Ends !!!"
return 1

