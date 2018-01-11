################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    01/19/2015 - Deepak Kumar Singh - created sample                          #
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
#    This script intends to demonstrate how to use NGPF OSPFv3 API.            #
#                                                                              #
#    1. It will create two OSPFv3 topologies.                                  #
#    2. Configure Network Topologies in each topologies.                       #
#    3. Configure Loopback Device Groups in each topologies.                   #
#    4. Start all protocols.                                                   #
#    5. Retrieve protocol statistics.                                          #
#    6. Configure L2-L3 & Applib traffic items.                                #
#    7. Start the L2-L3 & Applib traffics.                                     #
#    8. Retrieve L2-L3 traffic stats.                                          #
#    9. Make on the fly changes of Inter-Area Prefix attributes                #
#   10. Retrieve protocol statistics.                                          #
#   11. Stop L2-L3 traffic.                                                    #
#   12. Stop all protocols.                                                    #
#                                                                              #
# Ixia Software:                                                               #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
#                                                                              #
################################################################################

# ###############################################################################
# Utilities
# ###############################################################################
if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

# End Utilities #################################################################

# ###############################################################################
# Connection to the chassis, IxNetwork Tcl Server                               #
# ###############################################################################
set chassis_ip        {10.205.28.170}
set tcl_server        10.205.28.170
set port_list         {1/7 1/8}
set ixNetwork_client  "10.205.28.41:8981"
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
after 2000

# Retrieving port handles, for later use
set port1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]

# ###############################################################################
# Creating topology and device group                                            #
# ###############################################################################
# Creating a topology on first port
puts "Adding topology 1 on port 1" 
set topology_1_status [::ixiangpf::topology_config \
    -topology_name      {OSPFv3 Topology 1}        \
    -port_handle        $port1                     \
]
if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_1_status log]"
    return 0
}
set topology_1_handle [keylget topology_1_status topology_handle]

# Creating a device group in topology 
puts "Creating device group 1 in topology 1"    
set device_group_1_status [::ixiangpf::topology_config       \
    -topology_handle              $topology_1_handle         \
    -device_group_name            {OSPFv3 Router 1}          \
    -device_group_multiplier      1                          \
    -device_group_enabled         1                          \
]

if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_1_status log]"
    return 0
}
set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

# Creating a topology on second port
puts "Adding topology 2 on port 2"
set topology_2_status [::ixiangpf::topology_config \
    -topology_name      {OSPFv3 Topology 2}        \
    -port_handle        $port2                     \
]
if {[keylget topology_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_2_status log]"
    return 0
}
set topology_2_handle [keylget topology_2_status topology_handle]

# Creating a device group in topology
puts "Creating device group 2 in topology 2"
set device_group_2_status [::ixiangpf::topology_config       \
    -topology_handle              $topology_2_handle         \
    -device_group_name            {OSPFv3 Router 2}          \
    -device_group_multiplier      1                          \
    -device_group_enabled         1                          \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_2_status log]"
    return 0
}
set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]
after 2000

# ###############################################################################
#  Configure protocol interfaces                                                #
# ###############################################################################
# Creating ethernet stack for the first Device Group 
puts "Creating ethernet stack for the first Device Group"
set ethernet_1_status [::ixiangpf::interface_config          \
    -protocol_name                {Ethernet 1}               \
    -protocol_handle              $deviceGroup_1_handle      \
    -src_mac_addr                 18.03.73.c7.6c.b1          \
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
    -src_mac_addr                 18.03.73.c7.6c.01          \
]
if {[keylget ethernet_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_2_status log]"
    return 0
}
set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]

# Creating IPv6 Stack on top of Ethernet Stack for the first Device Group                                 
puts "Creating IPv6 Stack on top of Ethernet Stack for the first Device Group"
set ipv6_1_status [::ixiangpf::interface_config \
    -protocol_name                     {IPv6 1}                \
    -protocol_handle                   $ethernet_1_handle      \
    -ipv6_gateway                      2000:0:0:1:0:0:0:2      \
    -ipv6_intf_addr                    2000:0:0:1:0:0:0:1      \
]
if {[keylget ipv6_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv6_1_status log]"
    return 0
}
set ipv6_1_handle [keylget ipv6_1_status ipv6_handle]

# Creating IPv6 Stack on top of Ethernet Stack for the second Device Group 
puts "Creating IPv6 2 stack on ethernet 2 stack for the second Device Group"
set ipv6_2_status [::ixiangpf::interface_config \
    -protocol_name                     {IPv6 2}                \
    -protocol_handle                   $ethernet_2_handle      \
    -ipv6_gateway                      2000:0:0:1:0:0:0:1      \
    -ipv6_intf_addr                    2000:0:0:1:0:0:0:2      \
]
if {[keylget ipv6_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv6_2_status log]"
    return 0
}
set ipv6_2_handle [keylget ipv6_2_status ipv6_handle]
after 2000

# ###############################################################################
# Configure OSPFv3 protocol                                                     # 
# ###############################################################################
# Creating OSPFv3 Stack on top of IPv6 Stack for the first Device Group
puts "Creating OSPFv3 Stack on top of IPv6 1 stack"
set ospfv3_1_status [::ixiangpf::emulation_ospf_config \
    -handle                                                    $ipv6_1_handle            \
    -protocol_name                                             {OSPFv3-IF 1}             \
    -area_id_type                                              area_id_as_number         \
    -router_interface_active                                   1                         \
    -router_active                                             1                         \
    -lsa_discard_mode                                          0                         \
    -network_type                                              ptop                      \
    -mode                                                      create                    \
    -session_type                                              ospfv3                    \
]
if {[keylget ospfv3_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospfv3_1_status log]"
    return 0
}
set ospfv3_1_handle [keylget ospfv3_1_status ospfv3_handle]

# Creating OSPFv3 Stack on top of IPv6 Stack for the second Device Group
puts "Creating OSPFv3 Stack on top of IPv6 2 stack"
set ospfv3_2_status [::ixiangpf::emulation_ospf_config \
    -handle                                                    $ipv6_2_handle            \
    -protocol_name                                             {OSPFv3-IF 2}             \
    -area_id_type                                              area_id_as_number         \
    -router_interface_active                                   1                         \
    -router_active                                             1                         \
    -lsa_discard_mode                                          0                         \
    -network_type                                              ptop                      \
    -mode                                                      create                    \
    -session_type                                              ospfv3                    \
]
if {[keylget ospfv3_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospfv3_2_status log]"
    return 0
}
set ospfv3_2_handle [keylget ospfv3_2_status ospfv3_handle]
after 2000

# ###############################################################################
# Configure Network Topology & Loopback Device Groups                           # 
# ###############################################################################
# Creating Tree Network Topology in Topology 1
puts "Creating Tree Network Topology in Topology 1"
set network_group_1_status [::ixiangpf::network_group_config \
    -protocol_handle                   $deviceGroup_1_handle        \
    -protocol_name                     {OSPFv3 Network Group 1}     \
    -enable_device                     1                            \
    -type                              tree                         \
]
if {[keylget network_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_1_status log]"
    return 0
}
set networkGroup_1_handle [keylget network_group_1_status network_group_handle]
set simRouter_1_handle [keylget network_group_1_status simulated_router_handle]
set interAreaPrefix_1_handle [keylget network_group_1_status v3_inter_area_prefix_handle]

puts "Creating Loopback Device Group in Topology 1"
set device_group_3_status [::ixiangpf::topology_config \
    -device_group_name            {Applib Endpoint 1}         \
    -device_group_multiplier      7                           \
    -device_group_enabled         1                           \
    -device_group_handle          $networkGroup_1_handle      \
]
if {[keylget device_group_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_3_status log]"
    return 0
}
set deviceGroup_3_handle [keylget device_group_3_status device_group_handle] 

set multivalue_1_status [::ixiangpf::multivalue_config \
    -pattern                counter                                                              \
    -counter_start          3000:0:1:1:0:0:0:0                                                   \
    -counter_step           0:0:0:1:0:0:0:0                                                      \
    -counter_direction      increment                                                            \
    -nest_step              0:0:0:0:0:0:0:1,0:0:0:0:0:0:0:1,0:0:0:1:0:0:0:0                      \
    -nest_owner             $networkGroup_1_handle,$deviceGroup_1_handle,$topology_1_handle      \
    -nest_enabled           0,0,1                                                                \
]
if {[keylget multivalue_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_1_status log]"
    return 0
}
set multivalue_1_handle [keylget multivalue_1_status multivalue_handle]

set ipv6_loopback_1_status [::ixiangpf::interface_config \
    -protocol_name            {IPv6 Loopback 1}          \
    -protocol_handle          $deviceGroup_3_handle      \
    -enable_loopback          1                          \
    -connected_to_handle      $simRouter_1_handle        \
    -ipv6_intf_addr           $multivalue_1_handle       \
]

# Creating Tree Network Topology in Topology 2
puts "Creating Tree Network Topology in Topology 2"
set network_group_2_status [::ixiangpf::network_group_config \
    -protocol_handle                   $deviceGroup_2_handle        \
    -protocol_name                     {OSPFv3 Network Group 2}     \
    -enable_device                     1                            \
    -type                              tree                         \
]
if {[keylget network_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_2_status log]"
    return 0
}
set networkGroup_2_handle [keylget network_group_2_status network_group_handle]
set simRouter_2_handle [keylget network_group_2_status simulated_router_handle]
set interAreaPrefix_2_handle [keylget network_group_2_status v3_inter_area_prefix_handle]

puts "Creating Loopback Device Group in Topology 2"
set device_group_4_status [::ixiangpf::topology_config \
    -device_group_name            {Applib Endpoint 2}         \
    -device_group_multiplier      7                           \
    -device_group_enabled         1                           \
    -device_group_handle          $networkGroup_2_handle      \
]
if {[keylget device_group_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_4_status log]"
    return 0
}
set deviceGroup_4_handle [keylget device_group_4_status device_group_handle]

set multivalue_2_status [::ixiangpf::multivalue_config \
    -pattern                counter                                                              \
    -counter_start          3000:5:1:1:0:0:0:0                                                   \
    -counter_step           0:0:0:1:0:0:0:0                                                      \
    -counter_direction      increment                                                            \
    -nest_step              0:0:0:0:0:0:0:1,0:0:0:0:0:0:0:1,0:0:0:1:0:0:0:0                      \
    -nest_owner             $networkGroup_2_handle,$deviceGroup_2_handle,$topology_2_handle      \
    -nest_enabled           0,0,1                                                                \
]
if {[keylget multivalue_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_2_status log]"
    return 0
}
set multivalue_2_handle [keylget multivalue_2_status multivalue_handle]

set ipv6_loopback_2_status [::ixiangpf::interface_config \
    -protocol_name            {IPv6 Loopback 2}          \
    -protocol_handle          $deviceGroup_4_handle      \
    -enable_loopback          1                          \
    -connected_to_handle      $simRouter_2_handle        \
    -ipv6_intf_addr           $multivalue_2_handle       \
]
after 2000
  
# ###########################################################################
# Start all protocols                                                       #
# ###########################################################################
puts "Starting all protocols"
set protocol_start_status [::ixiangpf::test_control -action start_all_protocols]
if {[keylget protocol_start_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_start_status log]"
    return 0
}

puts "Waiting for 30 seconds for OSPFv3 sessions to come up ..."
after 30000

# ###############################################################################
# Making on the fly changes for Inter-Area Prefix Network Address in            #
# both Network Topologies                                                       #
# ###############################################################################
# Modifying Inter-Area Prefix Network Address in Network Topology 1
puts "Modifying Inter-Area Prefix Network Address in Network Topology 1"
set multivalue_3_status [::ixiangpf::multivalue_config \
    -pattern                counter                                       \
    -counter_start          3000:0:1:1:0:0:0:0                            \
    -counter_step           0:0:0:1:0:0:0:0                               \
    -counter_direction      increment                                     \
    -nest_step              0:0:0:0:0:0:0:1,0:0:1:0:0:0:0:0               \
    -nest_owner             $deviceGroup_1_handle,$topology_1_handle      \
    -nest_enabled           0,1                                           \
]
if {[keylget multivalue_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_3_status log]"
    return 0
}
set multivalue_3_handle [keylget multivalue_3_status multivalue_handle] 

set network_group_3_status [::ixiangpf::emulation_ospf_network_group_config \
    -handle                                      $networkGroup_1_handle      \
    -mode                                        modify                      \
    -inter_area_prefix_active                    1                           \
    -inter_area_prefix_network_address           $multivalue_3_handle       \
]
if {[keylget network_group_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_3_status log]"
    return 0
}

# Modifying Inter-Area Prefix Network Address in Network Topology 2
puts "Modifying Inter-Area Prefix Network Address in Network Topology 2"
set multivalue_4_status [::ixiangpf::multivalue_config \
    -pattern                counter                                       \
    -counter_start          3000:5:1:1:0:0:0:0                            \
    -counter_step           0:0:0:1:0:0:0:0                               \
    -counter_direction      increment                                     \
    -nest_step              0:0:0:0:0:0:0:1,0:0:1:0:0:0:0:0               \
    -nest_owner             $deviceGroup_2_handle,$topology_2_handle      \
    -nest_enabled           0,1                                           \
]
if {[keylget multivalue_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_4_status log]"
    return 0
}
set multivalue_4_handle [keylget multivalue_4_status multivalue_handle] 

set network_group_4_status [::ixiangpf::emulation_ospf_network_group_config \
    -handle                                      $networkGroup_2_handle      \
    -mode                                        modify                      \
    -inter_area_prefix_active                    1                           \
    -inter_area_prefix_network_address           $multivalue_4_handle       \
]
if {[keylget network_group_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_4_status log]"
    return 0
}
after 2000

# ###############################################################################
# Applying changes one the fly                                                  #
# ###############################################################################
puts "Applying changes on the fly ..."
set applyChanges [::ixiangpf::test_control \
   -action apply_on_the_fly_changes]
if {[keylget applyChanges status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget applyChanges log]"
    return 0
}

puts "Waiting for 15 seconds after applying change on the fly ..."
after 15000

# ###########################################################################
# Retrieve protocol statistics                                              #
# ###########################################################################
puts "Fetching OSPFv3 statistics ..."
set ospfv3Stat [::ixiangpf::emulation_ospf_info\
    -handle $ospfv3_1_handle \
    -session_type ospfv3 \
    -mode aggregate_stats]
if {[keylget ospfv3Stat status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospfv3Stat log]"
    return 0
}
foreach stat $ospfv3Stat {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}
after 2000

# ########################################################################### 
# Configure L2-3 & L4-7 traffic                                             #
# 1. Endpoints : Source->IPv6, Destination->IPv6                            #
# 2. Type      : Unicast IPv6 traffic                                       #
# 3. Flow Group: On IPv6 Destination Address                                #
# 4. Rate      : 2000 pps                                                   #
# 5. Frame Size: 500 bytes                                                  #
# 6. Tracking  : Source Destination EndpointPair                            #
# ###########################################################################
# Configuring L2-L3 traffic item
puts "Configuring L2-L3 traffic"
set traffic_item_1_status [::ixiangpf::traffic_config  \
    -mode                                       create                                     \
    -traffic_generator                          ixnetwork_540                              \
    -endpointset_count                          1                                          \
    -emulation_src_handle                       $interAreaPrefix_1_handle                  \
    -emulation_dst_handle                       $interAreaPrefix_2_handle                  \
    -name                                       Traffic_Item_1                             \
    -circuit_endpoint_type                      ipv6                                       \
    -rate_pps                                   2000                                       \
    -frame_size                                 500                                        \
    -track_by                                   {sourceDestEndpointPair0 trackingenabled0} \
]
if {[keylget traffic_item_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_item_1_status log]"
    return 0
}

# Configure traffic for Layer 4-7 AppLibrary Profile
puts "Configure L4-7 AppLibrary traffic profile"
set traffic_item_2_status [::ixiangpf::traffic_l47_config \
    -mode                        create                               \
    -name                        {Traffic Item 2}                     \
    -circuit_endpoint_type       ipv6_application_traffic             \
    -emulation_src_handle        $networkGroup_1_handle               \
    -emulation_dst_handle        $networkGroup_2_handle               \
    -objective_type              users                                \
    -objective_value             100                                  \
    -objective_distribution      apply_full_objective_to_each_port    \
    -enable_per_ip_stats         0                                    \
    -flows                       {Bandwidth_BitTorrent_File_Download Bandwidth_eDonkey Bandwidth_HTTP Bandwidth_IMAPv4 Bandwidth_POP3 Bandwidth_Radius Bandwidth_Raw Bandwidth_Telnet Bandwidth_uTorrent_DHT_File_Download BBC_iPlayer BBC_iPlayer_Radio BGP_IGP_Open_Advertise_Routes BGP_IGP_Withdraw_Routes Bing_Search BitTorrent_Ares_v217_File_Download BitTorrent_BitComet_v126_File_Download BitTorrent_Blizzard_File_Download BitTorrent_Cisco_EMIX BitTorrent_Enterprise BitTorrent_File_Download BitTorrent_LimeWire_v5516_File_Download BitTorrent_RMIX_5M}      \
]
if {[keylget traffic_item_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_item_2_status log]"
    return 0
}
after 2000

# ###########################################################################
#  Start Traffic configured earlier                                         #
# ###########################################################################
puts "Running Traffic ..."
set traffic_start_status [::ixiangpf::traffic_control       \
    -action            run           \
    -traffic_generator ixnetwork_540 \
    -type              {l23 l47}     \
]
if {[keylget traffic_start_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_start_status log]"
    return 0
}
puts "Let the traffic run for 30 seconds ..."
after 30000
   
# ###########################################################################
# Retrieve Traffic stats                                                    #
# ###########################################################################
puts "Retrieving traffic stats ..."
set trafficStats [::ixiangpf::traffic_stats \
    -mode all                           \
    -traffic_generator ixnetwork_540    \
    -measure_mode mixed                 \
]
if {[keylget trafficStats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget trafficStats log]"
    return 0
}

foreach stat $trafficStats {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}
after 2000
     
# ###############################################################################
# Stop Traffic started earlier                                                  #    
# ###############################################################################
puts "Stopping Traffic ..."
set traffic_stop_status [::ixiangpf::traffic_control \
    -action stop \
    -traffic_generator ixnetwork_540 \
    -type {l23 l47} \
]
if {[keylget traffic_stop_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_stop_status log]"
    return 0
}
after 2000
   
# ###############################################################################
# Stop all protocols                                                            #
# ###############################################################################
puts "Stopping all protocols ..."
set protocol_stop_status [::ixiangpf::test_control -action stop_all_protocols]
if {[keylget protocol_stop_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_stop_status log]"
    return 0
}
after 2000

puts "!!! Test Script Ends !!!"           
return 1     
