################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright 1997 - 2015 by IXIA                                             #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    15/01/2015 - Poulomi Chatterjee - created sample                          #
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
#    This script intends to demonstrate how to use NGPF ISISL3 API.            #
#                                                                              #
#    1. It will create 2 ISISL3 topologies, each having an ipv4 & ipv6 network #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. A loopback device group(DG) behind network   # 
#       group is needed to support applib traffic.                             #
#    2. Start ISISL3 protocol.                                                 #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Configure L2-L3 traffic (IPv4 & IPv6).                                 #
#    6. Configure application traffic for IPv4/IPv6 Profile. [global variable  #
#       "traffic_mode" selects the profile to be configured.                   #
#       Options are: 1(for IPv4) & 2(for IPv6)                                 # 
#       Note: IPv4 & IPv6 both could not be configured in same endpoint set.   #
#    7. Start L2-L3 traffic.                                                   #
#    8. Start application traffic.                                             #
#    9. Retrieve Appilcation traffic stats.                                    #
#   10. Retrieve L2-L3 traffic stats.                                          #
#   11. Stop L2-L3 traffic.                                                    #
#   12. Stop Application traffic.                                              #
#   13. Stop all protocols.                                                    #
# Ixia Software:                                                               #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
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
# Connection to the chassis, IxNetwork Tcl Server                              #
################################################################################
set chassis_ip        {10.205.28.170}
set tcl_server        10.205.28.170
set port_list         {1/7 1/8}
set ixNetwork_client  "10.205.28.41:8981"
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
    -topology_name      {ISIS Topology 1}          \
    -port_handle        "$port1"      \
]
if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_1_status log]"
}
set topology_1_handle [keylget topology_1_status topology_handle]

# Creating a device group in topology
puts "Creating device group 1 in topology 1\n"
set device_group_1_status [::ixiangpf::topology_config \
    -topology_handle              $topology_1_handle      \
    -device_group_name            {ISIS Device Group 1}   \
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
    -topology_name      {ISIS Topology 2}          \
    -port_handle        "$port2"      \
] 
if {[keylget topology_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_2_status log]"
    return 0
}
set topology_2_handle [keylget topology_2_status topology_handle]

# Creating a device group in topology
puts "Creating device group 2 in topology 2\n"
set device_group_4_status [::ixiangpf::topology_config \
    -topology_handle              $topology_2_handle      \
    -device_group_name            {ISIS Device Group 2}   \
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

# Creating ethernet stack in device group
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

# Creating ethernet stack in device group
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
# Other protocol configurations                                                # 
################################################################################

################################################################################
# Creating  ISIS Stack on top of ethernet stack                                #
# Descrtiption of protocol arguments : discard_lsp: enables learning LSPs      #
#                                      intf_type: sets interface type          #
#                                      routing_level: sets routing level       #
#                                      system_id: sets system id               #   
#                                      protocol_name: sets prtoocol name       # 
#                                      active: activates ISIS router           #
#                                      if_active: activates router interface   #
################################################################################ 
puts "Creating ISIS Stack on top of ethernet 1 stack\n"
set isis_l3_1_status [::ixiangpf::emulation_isis_config \
    -mode                                 create                    \
    -handle                               $ethernet_1_handle        \
    -discard_lsp                          0                         \
    -intf_type                            ptop                      \
    -routing_level                        L2                        \
    -system_id                            64:01:00:01:00:00         \
    -protocol_name                        {ISIS-L3 IF 1}            \
    -level2_dead_interval                 30                        \
    -active                               1                         \
    -if_active                            1                         \
]

if {[keylget isis_l3_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_l3_1_status log]"
    return 0
}
set isisL3_1_handle [keylget isis_l3_1_status isis_l3_handle]


# Creating ISIS Network Group in port 1
puts "Creating ISIS IPv4 Network group in port 1\n"    
set network_group_1_status [::ixiangpf::network_group_config \
    -protocol_handle                      $deviceGroup_1_handle       \
    -protocol_name                        {ISIS Network Group 1}      \
    -enable_device                        1                           \
    -connected_to_handle                  $ethernet_1_handle          \
    -type                                 ipv4-prefix                 \
]
if {[keylget network_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget  network_group_1_status log]"
}

set networkGroup_1_handle [keylget network_group_1_status network_group_handle]
set ipv4PrefixPools_1_handle [keylget network_group_1_status ipv4_prefix_pools_handle]

     
set network_group_2_status [::ixiangpf::emulation_isis_network_group_config \
    -handle                  $networkGroup_1_handle      \
    -mode                    modify                      \
    -stub_router_origin      stub                        \
]
if {[keylget network_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_2_status log]"
    return 0
}
    
set device_group_2_status [::ixiangpf::topology_config \
    -device_group_name            {Device Group 3}            \
    -device_group_multiplier      1                           \
    -device_group_enabled         1                           \
    -device_group_handle          $networkGroup_1_handle      \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
     puts "FAIL - $test_name - [keylget device_group_2_status log]"
}

set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]

# Creating ipv4 Loopback interface for applib traffic   
puts "Adding ipv4 loopback1 for applib traffic\n"
set ipv4_loopback_1_status [::ixiangpf::interface_config \
    -protocol_name            {IPv4 Loopback 1}           \
    -protocol_handle          $deviceGroup_2_handle       \
    -enable_loopback          1                           \
    -intf_ip_addr             2.2.2.2                     \
    -connected_to_handle      $networkGroup_1_handle      \
]
if {[keylget ipv4_loopback_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_loopback_1_status log]"
    return 0
}
set ipv4Loopback_1_handle [keylget ipv4_loopback_1_status ipv4_loopback_handle]
 
# Creating ISIS Network group 3 for ipv6 ranges    
puts "Creating ISIS Network group 3 for ipv6 ranges\n"   
set network_group_3_status [::ixiangpf::network_group_config \
    -protocol_handle                      $deviceGroup_1_handle       \
    -protocol_name                        {ISIS Network Group 3}      \
    -connected_to_handle                  $ethernet_1_handle          \
    -type                                 ipv6-prefix                 \
]
if {[keylget network_group_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_3_status log]"
    return 0
}
set networkGroup_3_handle [keylget network_group_3_status network_group_handle]
set ipv6PrefixPools_1_handle [keylget network_group_3_status ipv6_prefix_pools_handle]
    
set network_group_4_status [::ixiangpf::emulation_isis_network_group_config \
    -handle                      $networkGroup_3_handle      \
    -mode                        modify                      \
]
if {[keylget network_group_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_4_status log]"
    return 0
}
    
set device_group_3_status [::ixiangpf::topology_config \
    -device_group_name            {Device Group 6}            \
    -device_group_multiplier      1                           \
    -device_group_enabled         1                           \
    -device_group_handle          $networkGroup_3_handle      \
]
if {[keylget device_group_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_3_status log]"
    return 0
}
set deviceGroup_3_handle [keylget device_group_3_status device_group_handle]


#Creating ipv6 loopback 1 interface for applib traffic    
puts "Adding ipv6 loopback1 for applib traffic\n"
set ipv6_loopback_1_status [::ixiangpf::interface_config \
    -protocol_name            {IPv6 Loopback 2}          \
    -protocol_handle          $deviceGroup_3_handle      \
    -enable_loopback          1                          \
    -connected_to_handle      $networkGroup_3_handle     \
    -ipv6_intf_addr           2222:0:1:0:0:0:0:1         \
]
if {[keylget ipv6_loopback_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv6_loopback_1_status log]"
    retutn 0
}
set ipv6Loopback_1_handle [keylget ipv6_loopback_1_status ipv6_loopback_handle]
   
################################################################################
# Creating  ISIS Stack on top of ethernet stack                                #
# Descrtiption of protocol arguments : discard_lsp: enables learning LSPs      #
#                                      intf_type: sets interface type          #
#                                      routing_level: sets routing level       #
#                                      system_id: sets system id               #
#                                      protocol_name: sets prtoocol name       #
#                                      active: activates ISIS router           #
#                                      if_active: activates router interface   #
################################################################################
puts "Creating ISIS Stack on top of Ethernet 2 stack\n"
set isis_l3_2_status [::ixiangpf::emulation_isis_config \
    -mode                                 create                     \
    -handle                               $ethernet_2_handle         \
    -discard_lsp                          0                          \
    -intf_type                            ptop                       \
    -routing_level                        L2                         \
    -system_id                            65:01:00:01:00:00          \
    -protocol_name                        {ISIS-L3 IF 2}             \
    -active                               1                          \
    -if_active                            1                          \
]

if {[keylget isis_l3_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_l3_2_status log]"
    return 0
}
set isisL3_2_handle [keylget isis_l3_2_status isis_l3_handle]

# Creating IPv4 Prefix Ranges
puts "Creating ISIS IPv4 Prefix Ranges\n"    
set network_group_5_status [::ixiangpf::network_group_config \
    -protocol_handle                      $deviceGroup_4_handle       \
    -protocol_name                        {ISIS Network Group 2}      \
    -multiplier                           1                           \
    -enable_device                        1                           \
    -connected_to_handle                  $ethernet_2_handle          \
    -type                                 ipv4-prefix                 \
]
if {[keylget network_group_5_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_5_status log]"
    return 0
}
set networkGroup_5_handle [keylget network_group_5_status network_group_handle]
set ipv4PrefixPools_3_handle [keylget network_group_5_status ipv4_prefix_pools_handle]
   
set network_group_6_status [::ixiangpf::emulation_isis_network_group_config \
    -handle                  $networkGroup_5_handle      \
    -mode                    modify                      \
]
if {[keylget network_group_6_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_6_status log]"
    return 0
}
    
# Creating a device group in topology for loopback interface
puts "Creating device group 2 in topology 2 for loopback interface\n"    
set device_group_5_status [::ixiangpf::topology_config \
    -device_group_name            {Device Group 4}            \
    -device_group_multiplier      1                           \
    -device_group_enabled         1                           \
    -device_group_handle          $networkGroup_5_handle      \
]
if {[keylget device_group_5_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_5_status log]"
    return 0
}
set deviceGroup_5_handle [keylget device_group_5_status device_group_handle]

#Creating ipv4 loopback 2 for applib traffic    
puts "Adding ipv4 loopback2 for applib traffic\n"
set ipv4_loopback_2_status [::ixiangpf::interface_config  \
    -protocol_name            {IPv4 Loopback 2}           \
    -protocol_handle          $deviceGroup_5_handle       \
    -enable_loopback          1                           \
    -connected_to_handle      $networkGroup_5_handle      \
    -intf_ip_addr             3.2.2.2                     \
]
if {[keylget ipv4_loopback_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_loopback_2_status log]"
    return 0
}
set ipv4Loopback_2_handle [keylget ipv4_loopback_2_status ipv4_loopback_handle]

# Creating ISIS Prefix ranges
puts "Creating ISIS IPv6 Prefix ranges\n"    
set network_group_7_status [::ixiangpf::network_group_config \
    -protocol_handle                      $deviceGroup_4_handle       \
    -protocol_name                        {ISIS Network Group 4}      \
    -connected_to_handle                  $ethernet_2_handle          \
    -type                                 ipv6-prefix                 \
]
if {[keylget network_group_7_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_7_status log]"
    return 0
}
set networkGroup_7_handle [keylget network_group_7_status network_group_handle]
set ipv6PrefixPools_3_handle [keylget network_group_7_status ipv6_prefix_pools_handle]
    
set network_group_8_status [::ixiangpf::emulation_isis_network_group_config \
        -handle                      $networkGroup_7_handle      \
        -mode                        modify                      \
]
if {[keylget network_group_8_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_8_status log]"
    return 0
}
  
# Creating a device group in topology for loopback interface
puts "Creating device group 2 in topology 2 for loopback interface\n"
set device_group_6_status [::ixiangpf::topology_config \
    -device_group_name            {Device Group 5}            \
    -device_group_multiplier      1                           \
    -device_group_enabled         1                           \
    -device_group_handle          $networkGroup_7_handle      \
]
if {[keylget device_group_6_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_6_status log]"
    return 0
}
set deviceGroup_6_handle [keylget device_group_6_status device_group_handle]

#Creating ipv6 loopback 2 for applib traffic    
puts "Adding ipv6 loopback2 for applib traffic\n"
set ipv6_loopback_2_status [::ixiangpf::interface_config  \
    -protocol_name            {IPv6 Loopback 1}           \
    -protocol_handle          $deviceGroup_6_handle       \
    -enable_loopback          1                           \
    -connected_to_handle      $networkGroup_7_handle      \
    -ipv6_multiplier          1                           \
    -ipv6_intf_addr           2222:0:0:0:0:0:0:1          \
]

if {[keylget ipv6_loopback_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv6_loopback_2_status log]"
    return 0
}
set ipv6Loopback_2_handle [keylget ipv6_loopback_2_status ipv6_loopback_handle]
    
puts "Waiting 5 seconds before starting protocol(s) ...\n"
after 5000

############################################################################
# Start ISIS protocol                                                      #
############################################################################

puts "Starting all protocol(s) ...\n"
set r [::ixiangpf::test_control -action start_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}

puts "Waiting for 120 seconds\n"
after 30000

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
puts "Fetching ISISL3 aggregated statistics\n"
set isisL3_stats [::ixiangpf::emulation_isis_info \
   -handle $isisL3_1_handle\
   -mode "stats"
]

if {[keylget isisL3_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isisL3_stats log]"
    return 0
}
foreach stat $isisL3_stats {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}

############################################################################
# Retrieve protocol learned info                                           #
############################################################################
puts "Fetching ISISL3 aggregated learned info\n"
set learned_info [::ixiangpf::emulation_isis_info \
   -handle $isisL3_1_handle\
   -mode "learned_info"]

if {[keylget learned_info status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget learned_info log]"
    return 0
}
foreach stat $learned_info {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}

############################################################################
# Configure L2-L3 traffic                                                  #
############################################################################
puts "Configure L2-L3 traffic\n"
# Configure L2-L3 IPv4 Traffic

puts "Configuring L2-L3 IPv4 Traffic item ...\n"
set _result_ [::ixiangpf::traffic_config \
    -mode                                     create                          \
    -traffic_generator                        ixnetwork_540                   \
    -endpointset_count                        1                               \
    -emulation_src_handle                     [list $ipv4PrefixPools_1_handle]\
    -emulation_dst_handle                     [list $ipv4PrefixPools_3_handle]\
    -name                                     Traffic_Item_1                  \
    -circuit_endpoint_type                    ipv4                            \
    -transmit_distribution                    ipv4DestIp0                     \
    -rate_pps                                 1000                            \
    -frame_size                               512                             \
    -track_by                                 {trackingenabled0 sourceDestEndpointPair0}
]

if {[keylget _result_ status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result_ log]"
    return 0
}

puts "traffic $_result_"
puts "Configured L2-L3 IPv4 traffic item!!!\n"

# Configure L2-L3 IPv6 Traffic 

puts "\n Configuring L2-L3 IPv6 Traffic item ...\n"
set _result2_ [::ixiangpf::traffic_config \
    -mode                                     create                          \
    -traffic_generator                        ixnetwork_540                   \
    -endpointset_count                        1                               \
    -emulation_src_handle                     [list $ipv6PrefixPools_1_handle]\
    -emulation_dst_handle                     [list $ipv6PrefixPools_3_handle]\
    -name                                     Traffic_Item_2                  \
    -circuit_endpoint_type                    ipv6                            \
    -transmit_distribution                    ipv6DestIp0                     \
    -rate_pps                                 1000                            \
    -frame_size                               512                             \
    -track_by                                 {trackingenabled0 sourceDestEndpointPair0}
]
if {[keylget _result2_ status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result2_ log]"
    return 0
}

puts "traffic $_result2_"

puts "\n Configured L2-L3 IPv6 traffic item!!!"

################################################################################
# Configure_L4_L7_IPv4 traffic                                                 #
################################################################################
# Set applib traffic mode 
puts "\nSet applib traffic mode in variable traffic_mode, for IPv4: 1, IPv6: 2"
set traffic_mode "1"
if {$traffic_mode == 1} {
    # Configure L4-L7 IPv4 applib profiles
    puts "\n Traffic mode is set to: 1"
    puts "\n Configuring L4-L7 IPv4 traffic item ..."
    set flowList [list\
          Bandwidth_BitTorrent_File_Download               \
          Bandwidth_eDonkey Bandwidth_HTTP Bandwidth_IMAPv4\
          Bandwidth_POP3 Bandwidth_Radius Bandwidth_Raw    \
          Bandwidth_Telnet                                 \
          Bandwidth_uTorrent_DHT_File_Download             \
          BBC_iPlayer BBC_iPlayer_Radio                    \
          BGP_IGP_Open_Advertise_Routes                    \
          BGP_IGP_Withdraw_Routes                          \
          Bing_Search                                      \
          BitTorrent_Ares_v217_File_Download               \
          BitTorrent_BitComet_v126_File_Download           \
          BitTorrent_Blizzard_File_Download                \
          BitTorrent_Cisco_EMIX BitTorrent_Enterprise      \
          BitTorrent_File_Download                         \
          BitTorrent_LimeWire_v5516_File_Download BitTorrent_RMIX_5M
    ]
  
  
     set traffic_item_1_status [::ixiangpf::traffic_l47_config        \
        -mode                        create                           \
        -name                        {Traffic Item 3}                 \
        -circuit_endpoint_type       ipv4_application_traffic         \
        -emulation_src_handle        $networkGroup_1_handle           \
        -emulation_dst_handle        $networkGroup_5_handle           \
        -objective_type              users                            \
        -objective_value             100                              \
        -objective_distribution      apply_full_objective_to_each_port\
        -enable_per_ip_stats         0                                \
        -flows                       $flowList
    ]

    if {[keylget traffic_item_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget traffic_item_1_status log]"
        return 0
    }
    puts "\nConfigured L4-L7 IPv4 traffic item!!!"

} elseif {$traffic_mode == 2} {

    # Configure L4-L7 IPv6 applib profiles
    puts "\nTraffic mode is set to: 2"
    puts "\nConfiguring L4-L7 IPv6 traffic item ..."
    set flowList [list\
          Bandwidth_BitTorrent_File_Download               \
          Bandwidth_eDonkey Bandwidth_HTTP Bandwidth_IMAPv4\
          Bandwidth_POP3 Bandwidth_Radius Bandwidth_Raw    \
          Bandwidth_Telnet                                 \
          Bandwidth_uTorrent_DHT_File_Download             \
          BBC_iPlayer BBC_iPlayer_Radio                    \
          BGP_IGP_Open_Advertise_Routes                    \
          BGP_IGP_Withdraw_Routes                          \
          Bing_Search                                      \
          BitTorrent_Ares_v217_File_Download               \
          BitTorrent_BitComet_v126_File_Download           \
          BitTorrent_Blizzard_File_Download                \
          BitTorrent_Cisco_EMIX BitTorrent_Enterprise      \
          BitTorrent_File_Download                         \
          BitTorrent_LimeWire_v5516_File_Download BitTorrent_RMIX_5M
    ]
  
  
     set traffic_item_1_status [::ixiangpf::traffic_l47_config        \
        -mode                        create                           \
        -name                        {Traffic Item 4}                 \
        -circuit_endpoint_type       ipv6_application_traffic         \
        -emulation_src_handle        $networkGroup_3_handle           \
        -emulation_dst_handle        $networkGroup_7_handle           \
        -objective_type              users                            \
        -objective_value             100                              \
        -objective_distribution      apply_full_objective_to_each_port\
        -enable_per_ip_stats         0                                \
        -flows                       $flowList
    ]

    if {[keylget traffic_item_1_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget traffic_item_1_status log]"
        return 0
    }
    puts "\nConfigured L4-L7 IPv6 traffic item!!!"
}
############################################################################
#  Start L2-L3 traffic configured earlier                                  #
############################################################################
puts "\n Running L2-L3 Traffic..."
set r [::ixiangpf::traffic_control \
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
#  Start L4-L7 traffic configured earlier                                  #
############################################################################
puts "\n Running L4-L7 Traffic..."
set r [::ixiangpf::traffic_control \
    -action run \
    -traffic_generator ixnetwork_540 \
    -type l47 \
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
set r [::ixiangpf::traffic_stats        \
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
set r [::ixiangpf::traffic_control \
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
# Stop L4-L7 traffic started earlier                                       #
############################################################################
puts "Stopping L4-L7 Traffic..."
set r [::ixiangpf::traffic_control \
    -action stop \
    -traffic_generator ixnetwork_540 \
    -type l47\
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
set r [::ixiangpf::test_control -action stop_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "!!! Test Script Ends !!!"
return 1

