################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    20/01/2015 - Abhijit Dhar - created sample                                #
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
# This script intends to demonstrate how to use NGPF OSPFv2 API.               #
#                                                                              #
# About Topology:                                                              #
# This topology has two b2b connected device group, with each device group     #
# having a 1) OSPFv2 router and 2) a network group range. The network group    #
# range has a device group behind to simulate the applib traffic.              #
#                                                                              # 
# Script Flow:                                                                 #
#  1. Configure the topology as described above.                               #
#  2. Start the OSPFv2 protocol.                                               #
#  3. Retrieve protocol learned info.                                          #
#  4. Retrieve protocol statistics.                                            #
#  5. Disable OSPFv2 network group range                                       #
#  6. Retrieve protocol learned info again and notice the difference with      #
#     previously retrieved learned info.                                       #
#  7. Enable the network group range                                           #
#  8. Retrieve protocol learned info again.                                    #
#  9. Configure L2-L3 traffic.                                                 #
# 10. Configure application traffic.                                           #
# 11. Start the L2-L3 traffic.                                                 #
# 12. Start the application traffic.                                           #
# 13. Retrieve Application traffic stats.                                      #
# 14. Retrieve L2-L3 traffic stats.                                            #
# 15. Stop L2-L3 traffic.                                                      #
# 16. Stop Application traffic.                                                #
# 17. Stop all protocols.                                                      #
#                                                                              #
# Ixia Software :                                                              #
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

# Connecting to Chassis
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
# End Connecting to Chassis
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
    -topology_name      {OSPFv2-1}                \
    -port_handle        "$port1"                  \
]
if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_1_status log]"
    return 0
}
set topology_1_handle [keylget topology_1_status topology_handle]

# Creating a device group in topology 1
puts "Creating device group in first port"
set device_group_1_status [::ixiangpf::topology_config\
    -topology_handle              $topology_1_handle  \
    -device_group_name            {OSPFv2-Router1}    \
    -device_group_multiplier      1                   \
    -device_group_enabled         1                   \
]
if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_1_status log]"
    return 0
}
set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

# Creating a topology on 2nd port
puts "Adding topology 1 on port 1"
set topology_2_status [::ixiangpf::topology_config\
    -topology_name      {OSPFv2-2}                \
    -port_handle        "$port2"                  \
]
if {[keylget topology_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_2_status log]"
    return 0
}
set topology_2_handle [keylget topology_2_status topology_handle]

# Creating a device group in topology 2
puts "Creating device group in second port"
set device_group_2_status [::ixiangpf::topology_config\
    -topology_handle              $topology_2_handle  \
    -device_group_name            {OSPFv2-Router2}    \
    -device_group_multiplier      1                   \
    -device_group_enabled         1                   \
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
puts "Creating ethernet stack within Device Group 1"
set ethernet_1_status [::ixiangpf::interface_config    \
    -protocol_name                {Ethernet 1}         \
    -protocol_handle              $deviceGroup_1_handle\
    -mtu                          1500                 \
    -src_mac_addr                 18.03.73.c7.6c.b1    \
]

if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_1_status log]"
    return 0
}

set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]

# Creating ethernet stack for the second Device Group
puts "Creating ethernet stack within Device Group 2"
set ethernet_2_status [::ixiangpf::interface_config    \
    -protocol_name                {Ethernet 2}         \
    -protocol_handle              $deviceGroup_2_handle\
    -mtu                          1500                 \
    -src_mac_addr                 "18.03.73.c7.6c.01"  \
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
    -intf_ip_addr                      20.20.20.2        \
    -netmask                           255.255.255.0     \
    ]
if {[keylget ipv4_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_1_status log]"
    return 0
}
set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]

# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group                                 
puts "Creating IPv4 Stack on top of Ethernet Stack for the second Device Group"  
set ipv4_2_status [::ixiangpf::interface_config          \
    -protocol_name                     {IPv4 1}          \
    -protocol_handle                   $ethernet_2_handle\
    -ipv4_resolve_gateway              1                 \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01 \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00 \
    -gateway                           20.20.20.2        \
    -intf_ip_addr                      20.20.20.1        \
    -netmask                           255.255.255.0     \
    ]
if {[keylget ipv4_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_1_status log]"
    return 0
}
set ipv4_2_handle [keylget ipv4_2_status ipv4_handle]

################################################################################
# Other protocol configurations                                                # 
################################################################################
# This will create OSPFv2 on top of IP within Topology 1 
puts "Creating OSPFv2 on top of IPv4 1 stack"
set ospfv2_1_status [::ixiangpf::emulation_ospf_config\
    -handle                  $ipv4_1_handle           \
    -mode                    create                   \
    -network_type            ptop                     \
    -protocol_name           {OSPFv2-IF 1}            \
    -lsa_discard_mode        0                        \
    -router_id               193.0.0.1                \
    -router_interface_active 1                        \
    -router_active           1                        \
]
if {[keylget ospfv2_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospfv2_1_status log]"
    return 0
}
set ospfv2_handle1 [keylget ospfv2_1_status ospfv2_handle]

# Creating IPv4 prefix pool of Network for Network Cloud behind first
# Device Group  with "ipv4_prefix_network_address" = 201.1.0.1
puts "Creating IPv4 prefix pool behind first Device Group"
set network_group_1_status [::ixiangpf::network_group_config        \
    -protocol_handle                       $deviceGroup_1_handle\
    -protocol_name                         {Network Cloud 1}    \
    -multiplier                            1                    \
    -enable_device                         1                    \
    -connected_to_handle                   $ethernet_1_handle   \
    -type                                  ipv4-prefix          \
    -ipv4_prefix_network_address           201.1.0.1            \
    -ipv4_prefix_network_address_step      0.0.0.0              \
    -ipv4_prefix_length                    32                   \
    -ipv4_prefix_number_of_addresses       1                    \
]
if {[keylget network_group_1_status status] != $::SUCCESS} {
    puts "FAIL $test_name [keylget network_group_1_status log]"
    return 0
}
set networkGroup_1_handle    [keylget network_group_1_status network_group_handle]
set ipv4PrefixPools_1_handle [keylget network_group_1_status ipv4_prefix_pools_handle]

# Configure OSPFv2 group range for topology 1
puts "Configuring OSPFv2 group range for topology 1"
set ospfv2_network_group_1_status [::ixiangpf::emulation_ospf_network_group_config\
    -handle                           $networkGroup_1_handle                  \
    -mode                             modify                                  \
    -ipv4_prefix_active               1                                       \
    -ipv4_prefix_route_origin         another_area                            \
]
if {[keylget ospfv2_network_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name [keylget ospfv2_network_group_1_status log]"
    return 0
}

# This will create OSPFv2 on top of IP within Topology 2 
puts "Creating OSPFv2 on top of IPv4 2 stack"
set ospfv2_2_status [::ixiangpf::emulation_ospf_config\
    -handle                  $ipv4_2_handle           \
    -mode                    create                   \
    -network_type            ptop                     \
    -protocol_name           {OSPFv2-IF 2}            \
    -lsa_discard_mode        0                        \
    -router_id               194.0.0.1                \
    -router_interface_active 1                        \
    -router_active           1                        \
]

if {[keylget ospfv2_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospfv2_2_status log]"
    return 0
}
set ospfv2_handle2 [keylget ospfv2_2_status ospfv2_handle]

# Creating IPv4 prefix pool of Network for Network Cloud behind second\
# Device Group  with "ipv4_prefix_network_address" = 202.1.0.1
puts "Creating IPv4 prefix pool behind second Device Group" 
set network_group_2_status [::ixiangpf::network_group_config   \
    -protocol_handle                      $deviceGroup_2_handle\
    -protocol_name                        {Network Cloud 2}    \
    -multiplier                           1                    \
    -enable_device                        1                    \
    -connected_to_handle                  $ethernet_2_handle   \
    -type                                 ipv4-prefix          \
    -ipv4_prefix_network_address          202.1.0.1            \
    -ipv4_prefix_length                   32                   \
    -ipv4_prefix_number_of_addresses      1                    \
    ]
if {[keylget network_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_2_status log]"
    return 0
}
set networkGroup_2_handle    [keylget network_group_2_status network_group_handle]
set ipv4PrefixPools_2_handle [keylget network_group_2_status ipv4_prefix_pools_handle]

# Configure OSPFv2 group range for topology 2
puts "Configuring OSPFv2 group range for topology 1"
set ospfv2_network_group_2_status [::ixiangpf::emulation_ospf_network_group_config\
    -handle                           $networkGroup_2_handle                  \
    -mode                             modify                                  \
    -ipv4_prefix_active               1                                       \
    -ipv4_prefix_route_origin         another_area                            \
]
if {[keylget ospfv2_network_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name [keylget ospfv2_network_group_2_status log]"
    return 0
}

# Going to create Chained Device Group 3 behind Network Cloud 1 within Topology 1
# and renaming of that chained DG to "IPv4 Loopback 1"
puts "Going to create Chained DG 3 in Topology 1 behind Network Cloud 1 and renaming it"
set device_group_1_1_status [::ixiangpf::topology_config\
    -device_group_name            {IPv4 Loopback 1}     \
    -device_group_multiplier      1                     \
    -device_group_enabled         1                     \
    -device_group_handle          $networkGroup_1_handle\
]
if {[keylget device_group_1_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name [keylget device_group_1_1_status log]"
    return 0
}
set deviceGroup_1_1_handle [keylget device_group_1_1_status device_group_handle]

# Creating multivalue loopback adderress within chained DG in Topology 1
puts "Creating multivalue for loopback adderress within chained DG";
set multivalue1_1_status [::ixiangpf::multivalue_config                               \
    -pattern           counter                                                        \
    -counter_start     201.1.0.1                                                      \
    -counter_step      0.0.0.1                                                        \
    -counter_direction increment                                                      \
    -nest_step         0.0.0.1,0.0.0.1,0.1.0.0                                        \
    -nest_owner        $networkGroup_1_handle,$deviceGroup_1_handle,$topology_1_handle\
    -nest_enabled      0,0,1                                                          \
]
if {[keylget multivalue1_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue1_1_status log]"
    return 0
}
set multivalue_4_handle [keylget multivalue1_1_status multivalue_handle]

# Creating Loopback behind Chained DG
puts "Creating Loopback behind Chained DG"
set ipv4_loopback_1_status [::ixiangpf::interface_config\
    -protocol_name            {IPv4 Loopback 1}         \
    -protocol_handle          $deviceGroup_1_1_handle   \
    -enable_loopback          1                         \
    -connected_to_handle      $networkGroup_1_handle    \
    -intf_ip_addr             $multivalue_4_handle      \
    -netmask                  255.255.255.255           \
]
if {[keylget ipv4_loopback_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_loopback_1_status log]"
    return 0
}
set ipv4Loopback_1_handle [keylget ipv4_loopback_1_status ipv4_loopback_handle]

# Going to create Chained Device Group 4  behind Network Cloud 2 within Topology 2
# and renaming of that chained DG to "IPv4 Loopback 2"
puts "Going to create Chained DG 4 in Topology 2 behind Network Cloud 2 and renaming it"
set device_group_2_1_status [::ixiangpf::topology_config\
    -device_group_name            {IPv4 Loopback 2}     \
    -device_group_multiplier      1                     \
    -device_group_enabled         1                     \
    -device_group_handle          $networkGroup_2_handle\
]
if {[keylget device_group_2_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_2_1_status log]"
    return 0
}
set deviceGroup_2_1_handle [keylget device_group_2_1_status device_group_handle]

# Creating multivalue loopback adderress within chained DG in Topology 2
puts "Creating multivalue for loopback adderress within chained DG 4";
set multivalue2_1_status [::ixiangpf::multivalue_config                                    \
    -pattern                counter                                                        \
    -counter_start          202.1.0.1                                                      \
    -counter_step           0.0.0.1                                                        \
    -counter_direction      increment                                                      \
    -nest_step              0.0.0.1,0.0.0.1,0.1.0.0                                        \
    -nest_owner             $networkGroup_2_handle,$deviceGroup_2_handle,$topology_2_handle\
    -nest_enabled           0,0,1                                                          \
]
if {[keylget multivalue2_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue2_1_status log]"
    return 0
}
set multivalue_5_handle [keylget multivalue2_1_status multivalue_handle]

# Creating Loopback behind Chained Device Group 4 within Device Group
puts "Creating Loopback behind Chained DG 4"
set ipv4_loopback_2_status [::ixiangpf::interface_config\
    -protocol_name            {IPv4 Loopback 2}         \
    -protocol_handle          $deviceGroup_2_1_handle   \
    -enable_loopback          1                         \
    -connected_to_handle      $networkGroup_2_handle    \
    -intf_ip_addr             $multivalue_5_handle      \
    -netmask                  255.255.255.255           \
]
if {[keylget ipv4_loopback_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_loopback_2_status log]"
    return 0
}
set ipv4Loopback_2_handle [keylget ipv4_loopback_2_status\
    ipv4_loopback_handle]
# Configuration Block Ends Here    
puts "Waiting 5 seconds before starting protocol(s) ..."
after 5000

################################################################################
# Start all protocols                                                          #
################################################################################
puts "Starting all protocol(s) ..."
set r [::ixiangpf::test_control -action start_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "Waiting for 30 seconds"
after 30000

################################################################################
# Get OSPFv2 learned info                                                      #
################################################################################
puts "Fetching OSPFv2 learned info"
set learned_info [::ixiangpf::emulation_ospf_info\
    -handle $ospfv2_handle1                   \
    -mode learned_info]
if {[keylget learned_info status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget learned_info log]"
    return 0
}

puts "Printing OSPFv2 learned info"
puts "-------------------------------------------------------------------------"
puts "$learned_info"
puts "-------------------------------------------------------------------------"

################################################################################
# Get OSPFv2  stats                                                            #
################################################################################
puts "Fetching OSPFv2 stats"
set ospf_stats [::ixiangpf::emulation_ospf_info\
   -handle $ospfv2_handle1                 \
   -mode aggregate_stats                   \
]
if {[keylget ospf_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospf_stats log]"
    return 0
}
puts "Printing OSPFv2 stats"
puts "------------------------------------------------------------------------"
puts $ospf_stats
puts "------------------------------------------------------------------------"

################################################################################
# Disable the OSPFv2 group range                                               # 
################################################################################
puts "Disabling the OSPFv2 group-range on the topology 2"
set ospfv2_2_modify_status [::ixiangpf::emulation_ospf_network_group_config\
    -handle                 $networkGroup_2_handle                         \
    -mode                   modify                                         \
    -ipv4_prefix_active     0                                              \
]
if {[keylget ospfv2_2_modify_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospfv2_2_modify_status log]"
    return 0
}

################################################################################
# Applying changes one the fly                                                 #
################################################################################
puts "Applying changes on the fly"
set applyChanges [::ixiangpf::test_control\
   -action apply_on_the_fly_changes       \
]
if {[keylget applyChanges status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget applyChanges log]"
    return 0
}
after 5000

################################################################################
# Check learned info again after route disable                                 # 
################################################################################
puts "Waiting for 30 seconds"
after 30000

puts "Checking learned info after disabling OSPF router in topology 2"
set learned_info [::ixiangpf::emulation_ospf_info\
   -handle   $ospfv2_handle1                 \
   -mode     learned_info                    \
]

puts "-------------------------------------------------------------------------"
puts "$learned_info"
puts "-------------------------------------------------------------------------"

################################################################################
# Enabling the disabled OSPFv2 group range                                     #
################################################################################
puts "Disabling the OSPFv2 group-range on the topology 2"
set ospfv2_2_modify_status [::ixiangpf::emulation_ospf_network_group_config\
    -handle                 $networkGroup_2_handle                         \
    -mode                   modify                                         \
    -ipv4_prefix_active     1                                              \
]
if {[keylget ospfv2_2_modify_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospfv2_2_modify_status log]"
    return 0
}

################################################################################
# Applying changes one the fly                                                 #
################################################################################
puts "Applying changes on the fly"
set applyChanges [::ixiangpf::test_control\
   -action apply_on_the_fly_changes       \
]
if {[keylget applyChanges status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget applyChanges log]"
    return 0
}
after 5000

puts "Waiting for 30 seconds"
after 30000

###############################################################################
# Check learned info again after route enable                                 # 
###############################################################################
puts "Checking learned info after re-enabling OSPF router in topology 2"
set learned_info [::ixiangpf::emulation_ospf_info\
   -handle $ospfv2_handle1                   \
   -mode   learned_info                      \
]
if {[keylget learned_info status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget learned_info log]"
    return 0
}
puts "-------------------------------------------------------------------------"
puts "$learned_info"
puts "-------------------------------------------------------------------------"

################################################################################ 
# Configure L2-L3 traffic                                                      #
#    1. Endpoints : Source->IPv4, Destination->Multicast group                 #
#    2. Type      : Multicast IPv4 traffic                                     #
#    3. Flow Group: On IPv4 Destination Address                                #
#    4. Rate      : 100000 packets per second                                  #
#    5. Frame Size: 64 bytes                                                   #
#    6. Tracking  : IPv4 Source-Destination Address                            #
################################################################################
puts "Configuring L2-L3 data traffic"
set _result_ [::ixiangpf::traffic_config                              \
    -mode                   create                                    \
    -traffic_generator      ixnetwork_540                             \
    -endpointset_count      1                                         \
    -emulation_src_handle   $ipv4PrefixPools_1_handle                 \
    -emulation_dst_handle   $ipv4PrefixPools_2_handle                 \
    -frame_sequencing       disable                                   \
    -frame_sequencing_mode  rx_threshold                              \
    -name                   Traffic_Item_1                            \
    -circuit_endpoint_type  ipv4                                      \
    -rate_pps               100000                                    \
    -frame_size             64                                        \
    -mac_dst_mode           fixed                                     \
    -mac_src_mode           fixed                                     \
    -mac_src_tracking       1                                         \
    -track_by               {sourceDestEndpointPair0 trackingenabled0}\
]
if {[keylget _result_ status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result_ log]"
    return 0
}

################################################################################# 
# Configure L4-L7 Application traffic                                           #
#     1. Endpoints      : Source->IPv4 Loopback, Destination->IPv4 Loopback     #
#     2. Flow Group     : On IPv4 Destination Address                           #
#     3. objective value: 100                                                   #
#################################################################################
puts "Configuring L4-L7 App Lib traffic"
# L4-L7 applib profiles
set flowList [list                                            \
    Bandwidth_BitTorrent_File_Download                        \
    Bandwidth_eDonkey Bandwidth_HTTP Bandwidth_IMAPv4         \
    Bandwidth_POP3 Bandwidth_Radius Bandwidth_Raw             \
    Bandwidth_Telnet                                          \
    Bandwidth_uTorrent_DHT_File_Download                      \
    BBC_iPlayer BBC_iPlayer_Radio                             \
    BGP_IGP_Open_Advertise_Routes                             \
    BGP_IGP_Withdraw_Routes                                   \
    Bing_Search                                               \
    BitTorrent_Ares_v217_File_Download                        \
    BitTorrent_BitComet_v126_File_Download                    \
    BitTorrent_Blizzard_File_Download                         \
    BitTorrent_Cisco_EMIX BitTorrent_Enterprise               \
    BitTorrent_File_Download                                  \
    BitTorrent_LimeWire_v5516_File_Download BitTorrent_RMIX_5M\
]
  
set traffic_item_1_status [::ixiangpf::traffic_l47_config         \
    -mode                        create                           \
    -name                        {Traffic Item 2}                 \
    -circuit_endpoint_type       ipv4_application_traffic         \
    -emulation_src_handle        $ipv4Loopback_1_handle           \
    -emulation_dst_handle        $ipv4Loopback_2_handle           \
    -objective_type              users                            \
    -objective_value             100                              \
    -objective_distribution      apply_full_objective_to_each_port\
    -enable_per_ip_stats         1                                \
    -flows                       $flowList
]
if {[keylget traffic_item_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_item_1_status log]"
    return 0
}
################################################################################
# Start L2-L3 traffic configured earlier                                       #
# Start application traffic configured earlier                                 #
################################################################################
puts "Running Traffic..."
set r [::ixiangpf::traffic_control   \
    -action run                      \
    -traffic_generator ixnetwork_540 \
    -type {l23 l47}                  \
]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "Let the traffic run for 30 seconds ..."                
after 30000

################################################################################
# Retrieve Application traffic stats                                           # 
# Retrieve L2-L3 traffic stats                                                 # 
################################################################################
set r [::ixiangpf::traffic_stats    \
    -mode all                       \
    -traffic_generator ixnetwork_540\
    -measure_mode mixed             \
]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
foreach stat $r {
    puts "---------------------------------------------------------------------"
    puts "$stat"
    puts "---------------------------------------------------------------------"
}
################################################################################
# Stop L2-L3 traffic started earlier                                           #
# Stop application traffic started earlier                                     #
################################################################################
puts "Stopping Traffic..."
set r [::ixiangpf::traffic_control  \
    -action stop                    \
    -traffic_generator ixnetwork_540\
    -type {l23 l47} ]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}

###############################################################################
# Stop all protocols                                                          #
###############################################################################
puts "Stopping all protocol(s) ..."
set r [::ixiangpf::test_control -action stop_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "!!! Test Script Ends !!!"           
return 1
