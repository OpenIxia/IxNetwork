################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    01/19/2015 - Rupam Paul   - created sample                                #
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
#    This script intends to demonstrate how to use NGPF PIM API.               #
#                                                                              #
#    1. It will create 2 PIM topologies and Ipv4 Prefix Pool under             #
#       the network group(NG)                                                  #
#    2. Start the pim protocol.                                                #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Modify the Rangetype from "*G" to "SG" in the First and Second PIM     #
#       router.And apply changes On The Fly (OTF)                              #
#    6. Retrieve protocol learned info again and notice the difference with    #
#       previouly retrieved learned info.                                      #
#    7. Configure L2-L3 traffic.                                               #
#    8. Start the L2-L3 traffic.                                               #
#    9. Retrieve L2-L3 traffic stats                                           #
#   10. Stop L2-L3 traffic.                                                    #
#   11. Stop all protocols.                                                    #
#                                                                              #
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
# Connection to the chassis, IxNetwork Tcl Server                    	       #
################################################################################

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

# Retrieving port handles, for later use
set port1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]


################################################################################
# Creating topology and device group                                           #
################################################################################

# Creating a topology on first port
puts "Adding topology 1 on port 1" 
set topology_1_status [::ixiangpf::topology_config\
    -topology_name      {PIM Topology 1}          \
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
    -device_group_name            {Device Group 1}        \
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
    -topology_name      {PIM Topology 2}           \
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
    -device_group_name            {Device Group 2}     \
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

# This will Create PIMv4 Stack on top of IPv4 Stack of Topology1

puts "Creating PIMv4 Stack on top of IPv4 1 stack"
set pim_v4_interface_1_status [::ixiangpf::emulation_pim_config   \
    -mode                           create                    \
    -handle                         $ipv4_1_handle            \
	-ip_version                     4                         \
    ]
if {[keylget pim_v4_interface_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_interface_1_status log]"
    return 0
}

set pimv4Interface_1_handle [keylget pim_v4_interface_1_status pim_v4_interface_handle]

#Creating Multicast Group address

puts "Creating Multicast Group address"
set pim_v4_join_prune_list_2_status [::ixiangpf::emulation_multicast_group_config \
    -mode               create                  \
    -ip_addr_start      226.0.0.0               \
    -num_groups         1                       \
]
puts "pim_v4_join_prune_list_2_status = $pim_v4_join_prune_list_2_status"
if {[keylget pim_v4_join_prune_list_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_join_prune_list_2_status log]"
	return 0
}
	
set pimv4JoinPruneList_1_handle_group [keylget pim_v4_join_prune_list_2_status multicast_group_handle]
        
#Creating Multicast Source address

puts "Creating Multicast Source address"
set pim_v4_join_prune_list_3_status [::ixiangpf::emulation_multicast_source_config \
    -mode               create               \
    -ip_addr_start      0.0.0.1              \
	-num_sources        1                    \
    ]
if {[keylget pim_v4_join_prune_list_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_join_prune_list_3_status log]"
	return 0
}
		
set pimv4JoinPruneList_1_handle_source [keylget pim_v4_join_prune_list_3_status multicast_source_handle]
	
#Creating PIM Join-Prune List
puts "Creating Join Prune List"
	
set pim_v4_join_prune_list_4_status [::ixiangpf::emulation_pim_group_config \
    -mode                               create                                   \
    -session_handle                     $pimv4Interface_1_handle                 \
    -group_pool_handle                  $pimv4JoinPruneList_1_handle_group       \
    -source_pool_handle                 $pimv4JoinPruneList_1_handle_source      \
    -rp_ip_addr                         60.60.60.1                               \
    -group_pool_mode                    send                                     \
    -join_prune_aggregation_factor      1                                        \
    -flap_interval                      60                                       \
    -register_stop_trigger_count        10                                       \
    -source_group_mapping               fully_meshed                             \
    -switch_over_interval               5                                        \
    -group_range_type                   startogroup                              \
    -enable_flap_info                   false                                    \
    -prune_source_address               0.0.0.0                                  \
    -prune_source_mask_width            32                                       \
    -prune_source_address_count         0                                        \
    -join_prune_group_mask_width        32                                       \
    -join_prune_source_mask_width       32                                       \
    ]
if {[keylget pim_v4_join_prune_list_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_join_prune_list_4_status log]"
}
			
set pimv4JoinPruneList_1_handle [keylget pim_v4_join_prune_list_4_status pim_v4_join_prune_handle]
#Creating Multicast Group address

puts "Creating Multicast Group address"       
set pim_v4_sources_list_2_status [::ixiangpf::emulation_multicast_group_config \
    -mode               create                  \
    -ip_addr_start      225.0.0.0               \
	-num_groups         1                       \
        ]
if {[keylget pim_v4_sources_list_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_sources_list_2_status log]"
}
	
set pimv4SourcesList_1_handle_group [keylget pim_v4_sources_list_2_status multicast_group_handle]
  
#Creating Multicast Source address

puts "Creating Multicast Source address"  
set pim_v4_sources_list_3_status [::ixiangpf::emulation_multicast_source_config \
    -mode               create                  \
    -ip_addr_start      0.0.0.1                 \
	-num_sources        1                       \
     ]
if {[keylget pim_v4_sources_list_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_sources_list_3_status log]"
}
	
set pimv4SourcesList_1_handle_source [keylget pim_v4_sources_list_3_status multicast_source_handle]
	
#Creating PIM Source List
 
puts "Creating PIM Source List"
        
set pim_v4_sources_list_4_status [::ixiangpf::emulation_pim_group_config \
    -mode                               create                                 \
    -session_handle                     $pimv4Interface_1_handle               \
    -group_pool_handle                  $pimv4SourcesList_1_handle_group       \
    -source_pool_handle                 $pimv4SourcesList_1_handle_source      \
    -rp_ip_addr                         0.0.0.0                                \
    -group_pool_mode                    register                               \
    -register_tx_iteration_gap          30000                                  \
    -register_udp_destination_port      3000                                   \
    -register_udp_source_port           3000                                   \
    -switch_over_interval               0                                      \
    -send_null_register                 0                                      \
    -discard_sg_join_states             true                                   \
    -multicast_data_length              64                                     \
    -supression_time                    60                                     \
    -register_probe_time                5                                      \
    ]
if {[keylget pim_v4_sources_list_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_sources_list_4_status log]"
}
	
set pimv4SourcesList_1_handle [keylget pim_v4_sources_list_4_status pim_v4_source_handle]
    
#Creating Group Address for Candidate RP 

puts "Creating Group Address for Candidate RP"    
set pim_v4_candidate_r_ps_list_1_status [::ixiangpf::emulation_multicast_group_config \
    -mode               create         \
    -ip_addr_start      225.0.0.0      \
	-num_groups         1              \
     ]
if {[keylget pim_v4_candidate_r_ps_list_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_candidate_r_ps_list_1_status]"
}
	
set pimv4CandidateRPsList_1_handle [keylget pim_v4_candidate_r_ps_list_1_status multicast_group_handle]
	
#Creating PIM Candidate RP List
  
puts "Creating PIM Candidate RP List"
         
set pim_v4_candidate_r_ps_list_2_status [::ixiangpf::emulation_pim_group_config \
    -mode                       create                               \
    -session_handle             $pimv4Interface_1_handle             \
    -group_pool_handle          $pimv4CandidateRPsList_1_handle      \
    -adv_hold_time              150                                  \
    -back_off_interval          3                                    \
    -crp_ip_addr                0.0.0.1                              \
    -group_pool_mode            candidate_rp                         \
    -periodic_adv_interval      60                                   \
    -pri_change_interval        60                                   \
    -pri_type                   same                                 \
    -pri_value                  180                                  \
    -router_count               1                                    \
    -source_group_mapping       fully_meshed                         \
    -trigger_crp_msg_count      3                                    \
    -crp_group_mask_len         32                                   \
    ]
if {[keylget pim_v4_candidate_r_ps_list_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_candidate_r_ps_list_2_status log]"
}
	
set pimv4CandidateRPsList_1_handle [keylget pim_v4_candidate_r_ps_list_2_status pim_v4_candidate_rp_handle]
	
# Creating and Adding IPv6-prefix pool under Network Group1

puts "Creating ipv4 prefix network address"
set multivalue_3_status [::ixiangpf::multivalue_config \
    -pattern                counter                                       \
    -counter_start          200.1.0.0                                     \
    -counter_step           0.1.0.0                                       \
    -counter_direction      increment                                     \
    -nest_step              0.0.0.1,0.1.0.0                               \
    -nest_owner             $deviceGroup_1_handle,$topology_1_handle      \
    -nest_enabled           0,1                                           \
    ]
if {[keylget multivalue_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_3_status log]"
}
	
set multivalue_3_handle [keylget multivalue_3_status multivalue_handle]

puts "Creating and Adding IPv4-prefix pool under Network Group1"   
set network_group_1_status [::ixiangpf::network_group_config \
    -protocol_handle                      $deviceGroup_1_handle      \
    -protocol_name                        {Network Group 1}          \
    -multiplier                           1                          \
    -enable_device                        1                          \
    -connected_to_handle                  $ethernet_1_handle         \
    -type                                 ipv4-prefix                \
    -ipv4_prefix_network_address          $multivalue_3_handle       \
    -ipv4_prefix_length                   24                         \
    -ipv4_prefix_number_of_addresses      1                          \
    ]
if {[keylget network_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_1_status log]"
}
	
set networkGroup_1_handle [keylget network_group_1_status network_group_handle]
set ipv4PrefixPools_1_handle [keylget network_group_1_status ipv4_prefix_pools_handle]
	
# This will Create PIMv6 Stack on top of IPv6 Stack of Topology1

puts "Creating PIMv4 Stack on top of IPv4 Stack of Topology2"
set pim_v4_interface_2_status [::ixiangpf::emulation_pim_config \
    -mode                           create                      \
    -handle                         $ipv4_2_handle              \
    -ip_version                     4                           \
    ]
	
if {[keylget pim_v4_interface_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_interface_2_status log]"
}
	
set pimv4Interface_2_handle [keylget pim_v4_interface_2_status pim_v4_interface_handle]
     
#Creating Multicast Group address

puts "Creating Multicast Group address"	 
set pim_v4_join_prune_list_6_status [::ixiangpf::emulation_multicast_group_config \
    -mode               create                  \
    -ip_addr_start      226.0.0.0               \
    -num_groups         1                       \
    ]
if {[keylget pim_v4_join_prune_list_6_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_join_prune_list_6_status log]"
}
	
set pimv4JoinPruneList_5_handle_group [keylget pim_v4_join_prune_list_6_status multicast_group_handle]
	
#Creating Multicast Source address

puts "Creating Multicast Source address"   
set pim_v4_join_prune_list_7_status [::ixiangpf::emulation_multicast_source_config \
    -mode               create                  \
    -ip_addr_start      0.0.0.1                 \
    -num_sources        1                       \
    ]
if {[keylget pim_v4_join_prune_list_7_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_join_prune_list_7_status log]"
}
	
set pimv4JoinPruneList_5_handle_source [keylget pim_v4_join_prune_list_7_status multicast_source_handle]
	
#Creating PIM Join Prune List

puts "Creating PIM Join Prune List"
        
set pim_v4_join_prune_list_8_status [::ixiangpf::emulation_pim_group_config \
    -mode                               create                                   \
    -session_handle                     $pimv4Interface_2_handle                 \
    -group_pool_handle                  $pimv4JoinPruneList_5_handle_group       \
    -source_pool_handle                 $pimv4JoinPruneList_5_handle_source      \
    -rp_ip_addr                         60.60.60.1                               \
    -group_pool_mode                    send                                     \
    -join_prune_aggregation_factor      1                                        \
    -flap_interval                      60                                       \
    -register_stop_trigger_count        10                                       \
    -source_group_mapping               fully_meshed                             \
    -switch_over_interval               5                                        \
    -group_range_type                   startogroup                              \
    -enable_flap_info                   false                                    \
    -prune_source_address               0.0.0.0                                  \
    -prune_source_mask_width            32                                       \
    -prune_source_address_count         0                                        \
    -join_prune_group_mask_width        32                                       \
    -join_prune_source_mask_width       32                                       \
    ]
if {[keylget pim_v4_join_prune_list_8_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_join_prune_list_8_status log]"
}
	
set pimv4JoinPruneList_5_handle [keylget pim_v4_join_prune_list_8_status pim_v4_join_prune_handle]
#Creating Group address for Join-Prune list 

puts "Creating Group address for Join-Prune list"    
set pim_v4_sources_list_6_status [::ixiangpf::emulation_multicast_group_config \
    -mode               create                  \
    -ip_addr_start      225.0.0.0               \
    -num_groups         1                       \
    ]
if {[keylget pim_v4_sources_list_6_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_sources_list_6_status log]"
}
	
set pimv4SourcesList_5_handle_group [keylget pim_v4_sources_list_6_status multicast_group_handle]
    
#Creating Source address for Join-Prune list 

puts "Creating Source address for Join-Prune list"	
set pim_v4_sources_list_7_status [::ixiangpf::emulation_multicast_source_config \
    -mode               create                  \
    -ip_addr_start      0.0.0.1                 \
    -num_sources        1                       \
    -active             1                       \
    ]
if {[keylget pim_v4_sources_list_7_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_sources_list_7_status log]"
}
	
set pimv4SourcesList_5_handle_source [keylget pim_v4_sources_list_7_status multicast_source_handle]
	
#Creating PIM Source List
 
puts "Creating PIM Source List"  
set pim_v4_sources_list_8_status [::ixiangpf::emulation_pim_group_config       \
    -mode                               create                                 \
    -session_handle                     $pimv4Interface_2_handle               \
    -group_pool_handle                  $pimv4SourcesList_5_handle_group       \
    -source_pool_handle                 $pimv4SourcesList_5_handle_source      \
    -rp_ip_addr                         0.0.0.0                                \
    -group_pool_mode                    register                               \
    -register_tx_iteration_gap          30000                                  \
    -register_udp_destination_port      3000                                   \
    -register_udp_source_port           3000                                   \
    -switch_over_interval               0                                      \
    -send_null_register                 0                                      \
    -discard_sg_join_states             true                                   \
    -multicast_data_length              64                                     \
    -supression_time                    60                                     \
    -register_probe_time                5                                      \
    ]
if {[keylget pim_v4_sources_list_8_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_sources_list_8_status log]"
}
	
set pimv4SourcesList_5_handle [keylget pim_v4_sources_list_8_status pim_v4_source_handle]
   
#Creating Group Address for Candidate RP

puts "Creating Group Address for Candidate RP"   
set pim_v4_candidate_r_ps_list_3_status [::ixiangpf::emulation_multicast_group_config \
    -mode               create                  \
    -ip_addr_start      225.0.0.0               \
    -num_groups         1                       \
    -active             1                       \
    ]
if {[keylget pim_v4_candidate_r_ps_list_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_candidate_r_ps_list_3_status log]"
}
	
set pimv4CandidateRPsList_3_handle [keylget pim_v4_candidate_r_ps_list_3_status multicast_group_handle]
	
#Creating PIM Candidate RP List      
 
puts "Creating PIM Candidate RP List"      
set pim_v4_candidate_r_ps_list_4_status [::ixiangpf::emulation_pim_group_config \
    -mode                       create                               \
    -session_handle             $pimv4Interface_2_handle             \
    -group_pool_handle          $pimv4CandidateRPsList_3_handle      \
    -adv_hold_time              150                                  \
    -back_off_interval          3                                    \
    -crp_ip_addr                0.0.0.1                              \
    -group_pool_mode            candidate_rp                         \
    -periodic_adv_interval      60                                   \
    -pri_change_interval        60                                   \
    -pri_type                   same                                 \
    -pri_value                  190                                  \
    -router_count               1                                    \
    -source_group_mapping       fully_meshed                         \
    -trigger_crp_msg_count      3                                    \
    -crp_group_mask_len         32                                   \
    ]
if {[keylget pim_v4_candidate_r_ps_list_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pim_v4_candidate_r_ps_list_4_status log]"
}
	
set pimv4CandidateRPsList_3_handle [keylget pim_v4_candidate_r_ps_list_4_status pim_v4_candidate_rp_handle]
	
# Creating and Adding IPv6-prefix pool under Network Group2

puts "Creating ipv4 prefix network address"
set multivalue_6_status [::ixiangpf::multivalue_config                    \
    -pattern                counter                                       \
    -counter_start          201.1.0.0                                     \
    -counter_step           0.1.0.0                                       \
    -counter_direction      increment                                     \
    -nest_step              0.0.0.1,0.1.0.0                               \
    -nest_owner             $deviceGroup_2_handle,$topology_2_handle      \
    -nest_enabled           0,1                                           \
    ]
if {[keylget multivalue_6_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_6_status log]"
}
	
set multivalue_6_handle [keylget multivalue_6_status multivalue_handle]

puts "Creating and Adding IPv4-prefix pool under Network Group2"    
set network_group_2_status [::ixiangpf::network_group_config \
    -protocol_handle                      $deviceGroup_2_handle      \
    -protocol_name                        {Network Group 2}          \
    -multiplier                           1                          \
    -enable_device                        1                          \
    -connected_to_handle                  $ethernet_2_handle         \
    -type                                 ipv4-prefix                \
    -ipv4_prefix_network_address          $multivalue_6_handle       \
    -ipv4_prefix_length                   24                         \
    -ipv4_prefix_number_of_addresses      1                          \
    ]
if {[keylget network_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_2_status log]"
}
	
set networkGroup_2_handle [keylget network_group_2_status network_group_handle]
set ipv4PrefixPools_2_handle [keylget network_group_2_status ipv4_prefix_pools_handle]
	
############################################################################
# Start PIM protocol                                                       #
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
# Retrieve protocol statistics                                             # 
############################################################################
puts {fetching pimv4 aggregated statistics}
set aggregate_stats [::ixiangpf::emulation_pim_info                                \
    -handle $pimv4Interface_1_handle                                               \
    -mode aggregate]
	
if {[keylget aggregate_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget aggregate_stats log]"
}

puts $aggregate_stats
	
############################################################################
# Retrieve protocol learned info                                           #
############################################################################
puts {Fetching pim learned info}
set learned_info [::ixiangpf::emulation_pim_info                                   \
    -handle $pimv4Interface_1_handle                                               \
    -mode learned_crp]
	
if {[keylget learned_info status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget learned_info log]"
}

puts $learned_info
	
############################################################################
# Modifying the GroupRange Type from *G to SG and Enabling Bootstrap       #
############################################################################

#Modifying the GroupRange Type from *G to SG for Topology1
puts {Modifying the GroupRange Type from *G to SG for Topology1} 
set m1 [::ixiangpf::emulation_pim_group_config                                     \
    -handle            $pimv4JoinPruneList_1_handle                                \
    -mode              modify                                                      \
    -group_range_type  sourcetogroup]
		
if {[keylget m1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget m1 log]"
}

#Modifying the GroupRange Type from *G to SG for Topology2		
puts {Modifying the GroupRange Type from *G to SG for Topology2} 
set m2 [::ixiangpf::emulation_pim_group_config                                     \
    -handle            $pimv4JoinPruneList_5_handle                                \
    -mode              modify                                                      \
    -group_range_type  sourcetogroup]
	
if {[keylget m2 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget m2 log]"
}

#Enabling Bootstrap for Topology1   	
puts {Enabling Bootstrap for Topology1} 
set m3 [::ixiangpf::emulation_pim_config                                           \
    -handle            $pimv4Interface_1_handle                                    \
    -mode              modify                                                      \
    -ip_version                     4                                              \
    -bootstrap_enable               1]
if {[keylget m3 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget m3 log]"
}

#Enabling Bootstrap and Modifying Priority for Topology2
puts {Enabling Bootstrap and Modifying Priority for Topology2} 
set m4 [::ixiangpf::emulation_pim_config                                           \
    -handle            $pimv4Interface_2_handle                                    \
    -mode              modify                                                      \
    -ip_version                     4                                              \
    -bootstrap_enable               1                                              \
	-bootstrap_priority             74]
if {[keylget m4 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget m4 log]"
}

#Applying changes on the fly		
puts "Applying changes on the fly"
set applyChanges [::ixiangpf::test_control \
   -handle $pimv4Interface_1_handle        \
   -action apply_on_the_fly_changes]
if {[keylget applyChanges status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget applyChanges log]"
    return 0
}

puts {Waiting for 60 seconds}
after 60000
	
############################################################################
# Retrieve protocol learned info again after RangeType modification        #
############################################################################
puts {Fetching pim learned info again after modifying bsr priority}
set learned_info [::ixiangpf::emulation_pim_info                                   \
    -handle $pimv4Interface_1_handle                                               \
    -mode learned_crp]

if {[keylget learned_info status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget learned_info log]"
}

puts $learned_info
	
############################################################################ 
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv4, Destination->Multicast group                #
# 2. Type      : Multicast IPv4 traffic                                    #
# 3. Flow Group: On IPv4 Destination Address                               #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : IPv4 Destination Address                                  #	
############################################################################
puts "Configuring L2-L3 traffic"
set _result_ [::ixiangpf::traffic_config                                                    \
    -mode                                       create                                  \
    -traffic_generator                          ixnetwork_540                           \
    -endpointset_count                          1                                       \
    -emulation_src_handle                       $ipv4PrefixPools_1_handle               \
    -emulation_dst_handle                       $ipv4PrefixPools_2_handle               \
    -name                                       Traffic_Item_1                          \
    -circuit_endpoint_type                      ipv4                                    \
    -transmit_distribution                      ipv4DestIp0                             \
    -rate_pps                                   1000                                    \
    -frame_size                                 512                                     \
    -track_by                                   {trackingenabled0 ipv4DestIp0}          \
]
if {[keylget _result_ status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result_ log]"
    return 0
}

############################################################################
#  Start L2-L3 traffic configured earlier                                  #
############################################################################
puts "Running Traffic..."
set r [::ixiangpf::traffic_control       \
    -action run                      \
    -traffic_generator ixnetwork_540 \
    -type l23                        \
]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "Let the traffic run for 20 seconds ..."
after 20000
	
	   
############################################################################                                 
# Retrieve L2-L3 traffic stats                                             #  
############################################################################
puts "Retrieving L2-L3 traffic stats" 
set r [::ixiangpf::traffic_stats        \
    -mode all                       \
    -traffic_generator ixnetwork_540\
    -measure_mode mixed             \
    ]

if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts $r
  
############################################################################
# Stop L2-L3 traffic started earlier                                       #
############################################################################
puts "Stopping Traffic..."
set r [::ixiangpf::traffic_control       \
    -action stop                     \
    -traffic_generator ixnetwork_540 \
    -type {l23 l47} ]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
}
   
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
	
	
