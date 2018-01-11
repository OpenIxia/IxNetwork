################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright 1997 - 2016 by IXIA                                             #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/08/2016 - Poulomi Chatterjee - created sample                          #
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
#    This script intends to demonstrate how to use NGPF RSVPTE P2P HLT API.    #
#                                                                              #
# 1. It will create 2 RSVP-TE P2P topologies.                                  #
#     - Configure P2P Ingress LSPs in Topology 1.                              #
#     - Configure P2P Egress LSPs in Topology 2.                               #
# 2. Start all protocol.                                                       #
# 3. Retrieve protocol statistics.                                             #
# 4. Retrieve protocol learned info.                                           #
# 5. On The Fly deactivate/activate LSPs.                                      #
# 6. Configure L2-L3 traffic.                                                  #
# 7. Start the L2-L3 traffic.                                                  #
# 8. Retrieve L2-L3 traffic stats.                                             #
# 9. Stop L2-L3 traffic.                                                       #
# 10. Stop allprotocols.                                                       #
#                                                                              #
# Ixia Software:                                                               #
#    IxOS      8.10-EA                                                         #
#    IxNetwork 8.10-EA-Update(2)                                               #
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
set ixNetwork_client  "10.216.108.14:2666"
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
    -topology_name      {RSVP-TE P2P Topology 1}   \
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
    -device_group_name            {Device Group 1}        \
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
    -topology_name      {RSVP-TE P2P Topology 2}   \
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
    -device_group_name            {Device Group 2}     \
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

###################################################################################
# Configure RSVP Topologies in both ports as described in Description Section     #
#  above.                                                                         #
################################################################################### 

#---------------------------------------------------------------------------------#
# Configuring RSVPTE protocols in Topology 1                                      #
#---------------------------------------------------------------------------------#
#Creating RSVP-IF on top of ipv4 1 stack
puts "Creating RSVP-IF on top of ipv4 1 stack\n"
set rsvpte_if_1_status [::ixiangpf::emulation_rsvp_config \
    -mode                                         create                    \
    -handle                                       $ipv4_1_handle            \
    -using_gateway_ip                             1                         \
    -dut_ip                                       100.1.0.1                 \
    -label_space_start                            2000                      \
    -label_space_end                              300000                    \
    -hello_interval                               10000                     \
    -hello_timeout_multiplier                     3                         \
    -rsvp_neighbor_active                         1                         \
]
if {[keylget rsvpte_if_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget rsvpte_if_1_status log]"
    return 0
}
set rsvpteIf_1_handle [keylget rsvpte_if_1_status rsvp_if_handle] 

#Adding Network Group behind first DG
puts "Adding Network Group behind first DG"

set network_group_1_status [::ixiangpf::network_group_config \
    -protocol_handle                       $deviceGroup_1_handle      \
    -protocol_name                         {Network Group 1}          \
    -multiplier                            1                          \
    -enable_device                         1                          \
    -connected_to_handle                   $ethernet_1_handle         \
    -type                                  ipv4-prefix                \
    -ipv4_prefix_network_address           4.4.4.1                    \
    -ipv4_prefix_network_address_step      0.0.0.0                    \
    -ipv4_prefix_length                    32                         \
    -ipv4_prefix_multiplier                1                          \
]
if {[keylget network_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_1_status log]"
    return 0
}
set networkGroup_1_handle [keylget network_group_1_status network_group_handle]

# Adding second Device Group behind Network Group
puts "Adding second Device Group behind Network Group"
set device_group_2_status [::ixiangpf::topology_config \
    -device_group_name            {RSVP 1}                    \
    -device_group_multiplier      1                           \
    -device_group_enabled         1                           \
    -device_group_handle          $networkGroup_1_handle      \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_2_status log]"
    return 0
}
set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]
    
    
# Adding ipv4 loopback in Second Device Group
puts "Adding ipv4 loopback in Second Device Group"
set ipv4_loopback_1_status [::ixiangpf::interface_config \
    -protocol_name            {IPv4 Loopback 1}           \
    -protocol_handle          $deviceGroup_2_handle       \
    -enable_loopback          1                           \
    -connected_to_handle      $networkGroup_1_handle      \
    -intf_ip_addr             4.4.4.1                     \
    -netmask                  255.255.255.255             \
]
if {[keylget ipv4_loopback_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_loopback_1_status log]"
    return 0
}
set ipv4Loopback_1_handle [keylget ipv4_loopback_1_status ipv4_loopback_handle]

# Adding RSVPTE LSPs over ipv4 Loopback
puts "Adding RSVPTE LSPs over ipv4 Loopback"
set rsvpte_lsps_1_status [::ixiangpf::emulation_rsvp_tunnel_config \
    -mode                        create                      \
    -handle                      $ipv4Loopback_1_handle      \
    -p2p_ingress_lsps_count      2                           \
    -enable_p2p_egress           0                           \
    -lsp_active                  true                        \
]

if {[keylget rsvpte_lsps_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget rsvpte_lsps_1_status log]"
    return 0
}
set rsvpteLsps_1_handle [keylget rsvpte_lsps_1_status rsvpte_lsp_handle]

# Configure RSVPTE LSP parameters in ingress side
puts "Configure RSVPTE LSP parameters in ingress side"

set multivalue_6_status [::ixiangpf::multivalue_config \
    -pattern                counter                                                              \
    -counter_start          5.5.5.1                                                              \
    -counter_step           0.0.3.0                                                              \
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

set multivalue_7_status [::ixiangpf::multivalue_config \
    -pattern                counter                                                              \
    -counter_start          1                                                                    \
    -counter_step           1                                                                    \
    -counter_direction      increment                                                            \
    -nest_step              1,1,0                                                                \
    -nest_owner             $networkGroup_1_handle,$deviceGroup_1_handle,$topology_1_handle      \
    -nest_enabled           0,0,1                                                                \
]
if {[keylget multivalue_7_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_6_status log]"
    return 0
}
set multivalue_7_handle [keylget multivalue_7_status multivalue_handle]

set rsvp_p2p_ingress_lsps_1_status [::ixiangpf::emulation_rsvp_tunnel_config \
    -mode                                       create                       \
    -handle                                     $rsvpteLsps_1_handle         \
    -rsvp_p2p_ingress_enable                    1                            \
    -remote_ip                                  $multivalue_6_handle         \
    -tunnel_id                                  $multivalue_7_handle         \
    -lsp_id                                     101                          \
    -backup_lsp_id                              5000                         \
    -enable_path_re_optimization                true                         \
    -enable_periodic_re_evaluation_request      true                         \
    -p2p_ingress_active                         true                         \
]
if {[keylget rsvp_p2p_ingress_lsps_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget rsvp_p2p_ingress_lsps_1_status log]"
    return 0
}
set rsvpP2PIngressLsps_1_handle [keylget rsvp_p2p_ingress_lsps_1_status rsvpte_p2p_ingress_handle]

puts "Ingress Side topology Configuration complete in port 1..."

#---------------------------------------------------------------------------------#
# Configuring RSVPTE protocols in Topology 2                                      #
#---------------------------------------------------------------------------------#
set multivalue_48_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          101.1.0.1               \
    -counter_step           0.0.1.0                 \
    -counter_direction      increment               \
    -nest_step              0.0.0.1                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           0                       \
]
if {[keylget multivalue_48_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_48_status log]"
    return 0
}
set multivalue_48_handle [keylget multivalue_48_status multivalue_handle]
    

#Creating RSVP-IF on top of ipv4 2 stack
puts "Creating RSVP-IF on top of ipv4 2 stack\n"
set rsvpte_if_2_status [::ixiangpf::emulation_rsvp_config \
    -mode                                         create                     \
    -handle                                       $ipv4_2_handle             \
    -using_gateway_ip                             1                          \
    -dut_ip                                       $multivalue_48_handle      \
    -label_space_start                            1500                       \
    -label_space_end                              10000                      \
    -rsvp_neighbor_active                         1                          \
]
if {[keylget rsvpte_if_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget rsvpte_if_2_status log]"
    return 0
}
set rsvpteIf_2_handle [keylget rsvpte_if_2_status rsvp_if_handle]

#Adding IPv4 Prefix Pools behind first Device Group
puts "Adding IPv4 Prefix Pools behind first Device Group"
set network_group_6_status [::ixiangpf::network_group_config \
    -protocol_handle                       $deviceGroup_4_handle      \
    -protocol_name                         {Network Group 2}          \
    -multiplier                            2                          \
    -enable_device                         1                          \
    -connected_to_handle                   $ethernet_2_handle         \
    -type                                  ipv4-prefix                \
    -ipv4_prefix_network_address           5.5.5.1                    \
    -ipv4_prefix_network_address_step      0.0.3.0                    \
    -ipv4_prefix_length                    32                         \
    -ipv4_prefix_multiplier                1                          \
]
if {[keylget network_group_6_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_6_status log]"
    return 0
}
set networkGroup_6_handle [keylget network_group_6_status network_group_handle]


# Add DG2 behind IPv4 Prefix Pool
puts "Add DG2 behind IPv4 Prefix Pool"
set device_group_5_status [::ixiangpf::topology_config \
    -device_group_name            {Device Group 4}            \
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
     -counter_start          5.5.5.1                                                              \
     -counter_step           0.0.3.0                                                              \
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

# Adding RSVP LSPs over ipv4 Loopback
puts "Adding RSVP LSPs over ipv4 Loopback\n"
set rsvpte_lsps_2_status [::ixiangpf::emulation_rsvp_tunnel_config \
    -mode                        create                      \
    -handle                      $ipv4Loopback_2_handle      \
    -p2p_ingress_lsps_count      0                           \
    -enable_p2p_egress           1                           \
    -lsp_active                  true                        \
]
if {[keylget rsvpte_lsps_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget rsvpte_lsps_2_status log]"
    return 0
}
set rsvpteLsps_2_handle [keylget rsvpte_lsps_2_status rsvpte_lsp_handle]

# Configure RSVPTE LSP parameters in egress side
puts "Configure RSVPTE LSP parameters in egress side"
set multivalue_33_status [::ixiangpf::multivalue_config \
     -pattern                counter                                                              \
     -counter_start          2001                                                                 \
     -counter_step           1                                                                    \
     -counter_direction      increment                                                            \
]
if {[keylget multivalue_33_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_33_status log]"
    return 0
}
set multivalue_33_handle [keylget multivalue_33_status multivalue_handle]

set rsvp_p2p_egress_lsps_1_status [::ixiangpf::emulation_rsvp_tunnel_config \
    -mode                                     create                      \
    -handle                                   $rsvpteLsps_2_handle        \
    -rsvp_p2p_egress_enable                   1                           \
    -enable_fixed_label_for_reservations      true                        \
    -label_value                              $multivalue_33_handle       \
    -reservation_style                        se                          \
    -reflect_rro                              true                        \
    -egress_active                            true                        \
]
if {[keylget rsvp_p2p_egress_lsps_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget rsvp_p2p_egress_lsps_1_status log]"
    return 0
}
set rsvpP2PEgressLsps_1_handle [keylget rsvp_p2p_egress_lsps_1_status rsvpte_p2p_egress_handle]

puts "Egress Side topology Configuration complete in port 2..."

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
puts "Fetching RSVP statistics\n"
# Check Stats using RSVP Router handle
puts {Check Stats using RSVP Router handle ...}
set rsvp_stats [::ixiangpf::emulation_rsvp_info \
    -handle $rsvpteIf_2_handle                  \
    -mode stats]
if {[keylget rsvp_stats status] != $::SUCCESS} {
    puts "FAILED"
    return $::FAILED
}
foreach stat $rsvp_stats {
    puts "=================================================================="
    puts "$stat\n"
    puts "=================================================================="
}

############################################################################
# Retrieve protocol learned info                                           #
############################################################################
puts "Fetching RSVPTE P2P learned info\n"
# Check Learned Info 
puts {Check Learned Info using RSVP-IF2 handle ...\n}
set rsvp_linfo [::ixiangpf::emulation_rsvp_info \
    -handle $rsvpteIf_2_handle             \
    -mode learned_info]

if {[keylget rsvp_linfo status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget rsvp_linfo log]"
    return $::FAILED
}
foreach info $rsvp_linfo {
    puts "=================================================================="
    puts "$info\n"
    puts "=================================================================="
}
set linfo [keylget rsvp_linfo /topology:2/deviceGroup:1/ethernet:1/ipv4:1/rsvpteIf:1]
set rsvp_linfo [keylget linfo learned_info]
set assigned [keylget rsvp_linfo assigned]

puts {Check Learned Info using RSVP-IF1 handle ...\n}
set rsvp_linfo [::ixiangpf::emulation_rsvp_info \
    -handle $rsvpteIf_1_handle             \
    -mode learned_info]

if {[keylget rsvp_linfo status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget rsvp_linfo log]"
    return $::FAILED
}
foreach info $rsvp_linfo {
    puts "=================================================================="
    puts "$info\n"
    puts "=================================================================="
}
set linfo [keylget rsvp_linfo /topology:1/deviceGroup:1/ethernet:1/ipv4:1/rsvpteIf:1]
set rsvp_linfo [keylget linfo learned_info]
set received [keylget rsvp_linfo received]


puts "====Assigned Learned Info ========================================"
puts "$assigned"
puts "=================================================================="
puts "====Received Learned Info ========================================"
puts "$received"
puts "=================================================================="
############################################################################
# On The Fly Deactivate/Activate LSPs 
############################################################################
puts "On The Fly Deactivate Egress Lsps"
set deactivate_lsp [::ixiangpf::emulation_rsvp_tunnel_config \
    -handle /topology:2/deviceGroup:1/networkGroup:1/deviceGroup:1/ipv4Loopback:1/rsvpteLsps:1/rsvpP2PEgressLsps\
    -mode disable]

if {[keylget deactivate_lsp status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget deactivate_lsp log]"
    return 0
}

puts "Apply On The Fly changes"
set applyChanges [::ixiangpf::test_control -action apply_on_the_fly_changes]
if {[keylget applyChanges status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result_ log]"
    return 0 
}
after 5000

puts "On The Fly Activate Egress Lsps"
set activate_lsp [::ixiangpf::emulation_rsvp_tunnel_config \
    -handle /topology:2/deviceGroup:1/networkGroup:1/deviceGroup:1/ipv4Loopback:1/rsvpteLsps:1/rsvpP2PEgressLsps\
    -mode enable]

if {[keylget activate_lsp status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget activate_lsp log]"
    return 0
}

puts "Apply On The Fly changes"
set applyChanges [::ixiangpf::test_control -action apply_on_the_fly_changes]
if {[keylget applyChanges status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result_ log]"
    return 0
}
after 10000
############################################################################
# Configure L2-L3 traffic                                                  #
############################################################################
puts "Configure L2-L3 traffic\n"
# Configure L2-L3 IPv4 Traffic
puts {Configuring traffic for traffic item: //traffic/trafficItem:<1>}

puts "Configuring L2-L3 IPv4 Traffic item ...\n"
set _result_ [::ixia::traffic_config \
    -mode                                     create                               \
    -traffic_generator                        ixnetwork_540                        \
    -endpointset_count                        1                                    \
    -emulation_src_handle                     [list $rsvpP2PIngressLsps_1_handle]  \
    -emulation_dst_handle                     [list $rsvpP2PEgressLsps_1_handle]   \
    -name                                     RSVP-P2P-Traffic                     \
    -circuit_endpoint_type                    ipv4                                 \
    -rate_pps                                 1000                                 \
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

