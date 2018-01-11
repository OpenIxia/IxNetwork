################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    01/19/2015 - Sumeer Kumar - created sample                                #
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
#    This script intends to demonstrate how to use NGPF IGMP HLT API.          #
#                                                                              #
#    1. It will create twp topologies, one having two IGMP Hosts and other     #
#       having one IGMP Querier.                                               #
#    2. Start IGMP protocol.                                                   #
#    3. Retreive protocol statistics.                                          #
#    4. Retrieve learned info.                                                 #
#    5. Configure L2-L3 traffic.                                               #
#    6. Start L2/L3 protocol.                                                  #
#    7. Retreive  L2/L3 protocol statistics.                                   #
#    8. Make Making on the fly changes for IGMP Group and Source Ranges.       #         
#    9. Make Making on the fly changes for IGMP Querier.                       #
#   10. Retreive protocol statistics.                                          #                             
#   11. Stop protocol and L2/L3 traffic.                                       #
#   12. Stop all protocols.                                                    #                
#                                                                              #
#Ixia Software:                                                                #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
#                                                                              #
################################################################################

################################################################################
# Utilities
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
set topology_1_status [::ixiangpf::topology_config \
    -topology_name      {IGMP Host Topology}       \
    -port_handle        $port1                     \
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
    -device_group_name            {IGMP Host Device Group}\
    -device_group_multiplier      2                       \
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
    -topology_name      {IGMP Querier Topology}    \
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
    -device_group_name            {IGMP Querier Device Group}\
    -device_group_multiplier      1                          \
    -device_group_enabled         1                          \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_2_status log]"
    return 0
}
set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]

################################################################################
#  Configure protocol interfaces                                               #
################################################################################

# Creating multivalue for ethernet
puts "Creating multivalue pattern for ethernet"
set multivalue_1_status [::ixiangpf::multivalue_config \
    -pattern                counter                    \
    -counter_start          18.03.73.c7.6c.b1          \
    -counter_step           00.00.00.00.00.01          \
    -counter_direction      increment                  \
    -nest_step              00.00.01.00.00.00          \
    -nest_owner             $topology_1_handle         \
    -nest_enabled           1                          \
]
if {[keylget multivalue_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_1_status log]"
    return 0
}
set multivalue_1_handle [keylget multivalue_1_status multivalue_handle]

# Creating ethernet stack for the first Device Group 
puts "Creating ethernet stack for the first Device Group"
set ethernet_1_status [::ixiangpf::interface_config     \
    -protocol_name                {Ethernet 1}          \
    -protocol_handle              $deviceGroup_1_handle \
    -mtu                          1500                  \
    -src_mac_addr                 $multivalue_1_handle  \
]
if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_1_status log]"
    return 0
}
set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]

# Creating ethernet stack for the second Device Group
puts "Creating ethernet for the second Device Group"
set ethernet_2_status [::ixiangpf::interface_config     \
    -protocol_name                {Ethernet 2}          \
    -protocol_handle              $deviceGroup_2_handle \
    -mtu                          1500                  \
    -src_mac_addr                 18.03.73.c7.6c.01     \
    -src_mac_addr_step            00.00.00.00.00.00     \
]
if {[keylget ethernet_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_2_status log]"
    return 0
}
set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]

# Creating multivalue for IPv4                                 
puts "Creating multivalue pattern for IPv4"    
set multivalue_2_status [::ixiangpf::multivalue_config \
    -pattern                counter                    \
    -counter_start          20.20.20.2                 \
    -counter_step           0.0.0.1                    \
    -counter_direction      increment                  \
    -nest_step              0.1.0.0                    \
    -nest_owner             $topology_1_handle         \
    -nest_enabled           1                          \
]
if {[keylget multivalue_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_2_status log]"
    return 0
}
set multivalue_2_handle [keylget multivalue_2_status multivalue_handle]

# Creating IPv4 Stack on top of Ethernet Stack for the first Device Group                                 
puts "Creating IPv4 Stack on top of Ethernet Stack for the first Device Group"
set ipv4_1_status [::ixiangpf::interface_config                  \
    -protocol_name                     {IPv4 1}                  \
    -protocol_handle                   $ethernet_1_handle        \
    -ipv4_resolve_gateway              1                         \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01         \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00         \
    -gateway                           20.20.20.1                \
    -gateway_step                      0.0.0.0                   \
    -intf_ip_addr                      $multivalue_2_handle      \
    -netmask                           255.255.255.0             \
]
if {[keylget ipv4_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_1_status log]"
    return 0
}
set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]

# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group 
puts "Creating IPv4 2 stack on ethernet 2 stack for the second Device Group"
set ipv4_2_status [::ixiangpf::interface_config                \
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

# This will create IGMP v3 Host Stack with IPTV disabled on top of IPv4 stack

# Creating IGMP Host Stack on top of IPv4 stack
puts "Creating IGMP Host Stack on top of IPv4 stack in first topology"    
set igmp_host_1_status [::ixiangpf::emulation_igmp_config \
    -handle                               $ipv4_1_handle  \
    -protocol_name                        {IGMP Host}     \
    -mode                                 create          \
    -filter_mode                          include         \
    -igmp_version                         v3 		  \
]
if {[keylget igmp_host_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_host_1_status log]"
    return 0    
}
set igmpHost_1_handle [keylget igmp_host_1_status igmp_host_handle]

# Creating multivalue for group address
puts "Creating multivalue pattern for IGMP Host group address"
set multivalue_3_status [::ixiangpf::multivalue_config \
    -pattern                counter                    \
    -counter_start          226.0.0.1                  \
    -counter_step           1.0.0.0                    \
    -counter_direction      increment                  \
    -nest_step              0.1.0.0                    \
    -nest_owner             $topology_1_handle         \
    -nest_enabled           1                          \
]
if {[keylget multivalue_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget multivalue_3_status log]"
    return 0
}
set multivalue_3_handle [keylget multivalue_3_status multivalue_handle]

# Creating IGMP Group Ranges 
puts "Creating IGMP Group Ranges"
set igmp_mcast_i_pv4_group_list_1_status [::ixiangpf::emulation_multicast_group_config \
    -mode               create               \
    -ip_addr_start      $multivalue_3_handle \
    -ip_addr_step       0.0.0.1              \
    -num_groups         1                    \
    -active             1                    \
]
if {[keylget igmp_mcast_i_pv4_group_list_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_mcast_i_pv4_group_list_1_status log]"
    return 0
}
set igmpMcastIPv4GroupList_1_handle [keylget igmp_mcast_i_pv4_group_list_1_status multicast_group_handle]

# Creating IGMP Source Ranges
puts "Creating IGMP Source Ranges"
set igmp_ucast_i_pv4_source_list_1_status [::ixiangpf::emulation_multicast_source_config \
    -mode               create     \
    -ip_addr_start      20.20.20.1 \
    -ip_addr_step       0.0.0.1    \
    -num_sources        1          \
    -active             1          \
]
if {[keylget igmp_ucast_i_pv4_source_list_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_ucast_i_pv4_source_list_1_status log]"
    return 0
}
set igmpUcastIPv4SourceList_1_handle [keylget igmp_ucast_i_pv4_source_list_1_status multicast_source_handle]
    
# Creating IGMP Group and Source Ranges in IGMP Host stack
puts "Creating IGMP Group and Source Ranges in IGMP Host stack"
set igmp_host_1_status [::ixiangpf::emulation_igmp_group_config \
    -mode                    create                                 \
    -g_filter_mode           include                                \
    -group_pool_handle       $igmpMcastIPv4GroupList_1_handle       \
    -no_of_grp_ranges        1                                      \
    -no_of_src_ranges        1                                      \
    -session_handle          $igmpHost_1_handle                     \
    -source_pool_handle      $igmpUcastIPv4SourceList_1_handle      \
]
if {[keylget igmp_host_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_host_1_status log]"
    return 0
}
set igmpGroup_1_handle [keylget igmp_host_1_status igmp_group_handle]

# This will create IGMP v3 Querier Stack on top of IPv4 stack

# Creating IGMP Querier Stack on top of IPv4 stack
puts "Creating IGMP Querier Stack on top of IPv4 stack in second topology"
set igmp_querier_1_status [::ixiangpf::emulation_igmp_querier_config \
    -mode                                   create                   \
    -active                                 1                        \
    -discard_learned_info                   0                        \
    -general_query_response_interval        11000                    \
    -handle                                 $ipv4_2_handle           \
    -igmp_version                           v3                       \
    -query_interval                         140                      \
    -name                                   {IGMP Querier}           \
]
if {[keylget igmp_querier_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_querier_1_status log]"
    return 0    
}
set igmpQuerier_1_handle [keylget igmp_querier_1_status igmp_querier_handle]
    
puts "Waiting 5 seconds before starting protocol(s) ..."
after 5000
  
############################################################################
# Start IGMP protocol                                                      #
############################################################################
puts "Starting IGMP Host on topology1"
set protocol_status [::ixiangpf::emulation_igmp_control \
    -mode start                                         \
    -handle $igmpHost_1_handle                          \
]
if {[keylget protocol_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_status log]"
    return 0
}    

puts "Starting IGMP Querier on topology2"
set protocol_status [::ixiangpf::emulation_igmp_control \
    -mode start                                         \
    -handle $igmpQuerier_1_handle                       \
]
if {[keylget protocol_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_status log]"
    return 0
}

puts "Waiting for 30 seconds"
after 30000
    
############################################################################
# Retrieve protocol statistics                                             # 
############################################################################
puts "Fetching IGMP Host aggregated statistics"
set igmpHostStat [::ixiangpf::emulation_igmp_info \
    -handle $deviceGroup_1_handle                 \
    -type host                                    \
    -mode aggregate                               \
]
if {[keylget igmpHostStat status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmpHostStat log]"
    return 0
}
foreach stat $igmpHostStat {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}

puts "Fetching IGMP Querier aggregated statistics"
set igmpQuerierStat [::ixiangpf::emulation_igmp_info \
    -handle $deviceGroup_2_handle                    \
    -type querier                                    \
    -mode aggregate                                  \
]
if {[keylget igmpQuerierStat status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmpQuerierStat log]"
    return 0
}
foreach stat $igmpQuerierStat {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}

############################################################################
# Retrieve Learned Info                                                    #
############################################################################
puts "Fetching IGMP Querier LearnedInfo"
set igmpLearnedInfo [::ixiangpf::emulation_igmp_info \
    -handle $igmpQuerier_1_handle                    \
    -type querier                                    \
    -mode learned_info                               \
]
if {[keylget igmpLearnedInfo status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmpLearnedInfo log]"
    return 0
}
foreach info $igmpLearnedInfo {
    puts "=================================================================="
    puts "$info"
    puts "=================================================================="
}

############################################################################ 
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv4, Destination->Multicast group                #
# 2. Type      : Multicast IPv4 traffic                                    #
# 3. Flow Group: Source Destination Endpoint Pair                          #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : Source Destination Endpoint Pair                          #	
############################################################################
puts "Configuring L2-L3 traffic" 
set _result_ [::ixiangpf::traffic_config                                                                                    \
    -mode                                       create                                                                  \
    -traffic_generator                          ixnetwork_540                                                           \
    -endpointset_count                          1                                                                       \
    -emulation_src_handle                       $topology_2_handle                                                      \
    -emulation_dst_handle                       [list]                                                                  \
    -emulation_multicast_dst_handle             [list 226.0.0.1/0.0.0.0/1 227.0.0.1/0.0.0.0/1]                          \
    -emulation_multicast_dst_handle_type        [list none none]                                                        \
    -emulation_multicast_rcvr_handle            [list $igmpMcastIPv4GroupList_1_handle $igmpMcastIPv4GroupList_1_handle]\
    -emulation_multicast_rcvr_port_index        [list 0 0]                                                              \
    -emulation_multicast_rcvr_host_index        [list 0 1]                                                              \
    -emulation_multicast_rcvr_mcast_index       [list 0 0]                                                              \
    -name                                       Traffic_Item_1                                                          \
    -circuit_endpoint_type                      ipv4                                                                    \
    -transmit_distribution                      srcDestEndpointPair0                                                    \
    -rate_pps                                   1000                                                                    \
    -frame_size                                 512                                                                     \
    -track_by                                   {trackingenabled0 sourceDestEndpointPair0}                              \
]
if {[keylget _result_ status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result_ log]"
    return 0
}

############################################################################
#  Start L2-L3 traffic configured earlier                                  #
############################################################################
puts "Running Traffic..."
set r [::ixiangpf::traffic_control \
    -action run \
    -traffic_generator ixnetwork_540 \
    -type l23 \
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
foreach stat $r {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}
    
############################################################################
# Sending leave using igmp host group handle                               #
############################################################################
puts "Sending leave using igmp host group handle"
set sendLeaveGlobally [::ixiangpf::emulation_igmp_control \
    -mode leave                              \
    -group_member_handle $igmpGroup_1_handle \
]    
if {[keylget sendLeaveGlobally status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget sendLeaveGlobally log]"
    return 0
}
after 2000
 
############################################################################
# Sending join using igmp host group handle                                #
############################################################################
puts "Sending join using igmp host group handle"
set sendJoinGlobally [::ixiangpf::emulation_igmp_control \
    -mode join                               \
    -group_member_handle $igmpGroup_1_handle \
]
if {[keylget sendJoinGlobally status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget sendJoinGlobally log]"
    return 0
}
after 2000
    
################################################################################
# Making on the fly changes for IGMP Group and Source Ranges                   # 
################################################################################
puts "Making on the fly chnages for IGMP Group Ranges"
set igmp_mcast_i_pv4_group_list_1_status [::ixiangpf::emulation_multicast_group_config \
    -mode               modify                           \
    -handle	 	$igmpMcastIPv4GroupList_1_handle \
    -ip_addr_start      230.1.1.1                        \
    -ip_addr_step       0.0.0.2                          \
    -num_groups         2                                \
    -active             1                                \
]
if {[keylget igmp_mcast_i_pv4_group_list_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_mcast_i_pv4_group_list_1_status log]"
    return 0
}

puts "Making on the fly chnages for IGMP Source Ranges"
set igmp_ucast_i_pv4_source_list_1_status [::ixiangpf::emulation_multicast_source_config \
    -mode               modify                            \
    -handle 	        $igmpUcastIPv4SourceList_1_handle \
    -ip_addr_start      30.30.30.1                        \
    -ip_addr_step       0.0.0.1                           \
    -num_sources        5                                 \
    -active             1                                 \
]
if {[keylget igmp_ucast_i_pv4_source_list_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_ucast_i_pv4_source_list_1_status log]"
    return 0
}

puts "Making on the fly chnages for IGMP Group and Source Ranges in IGMP Host stack"
set igmp_host_1_status [::ixiangpf::emulation_igmp_group_config \
    -mode                    modify                                 \
    -handle                  $igmpHost_1_handle 	            \
    -group_pool_handle       $igmpMcastIPv4GroupList_1_handle       \
    -g_filter_mode           exclude                                \
    -no_of_grp_ranges        1                                      \
    -no_of_src_ranges        1                                      \
    -session_handle          $igmpHost_1_handle                     \
    -source_pool_handle      $igmpUcastIPv4SourceList_1_handle      \
]
if {[keylget igmp_host_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_host_1_status log]"
    return 0
}
after 5000

############################################################################
# Making on the fly changes for IGMP Querier                               #
############################################################################
puts "Making on the fly changes for IGMP Querier"
set igmp_querier_1_status [::ixiangpf::emulation_igmp_querier_config  \
    -mode                                   modify                    \
    -handle 			 	    $igmpQuerier_1_handle     \
    -general_query_response_interval        240		              \
    -ip_router_alert                        0                         \
    -robustness_variable                    5                         \
    -startup_query_count                    5                         \
    -query_interval                         180		              \
]
if {[keylget igmp_querier_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_querier_1_status log]"
    return 0
}
after 2000

############################################################################
# Applying changes one the fly                                             #    
############################################################################
puts "Applying changes on the fly"
set applyChanges [::ixiangpf::test_control \
   -handle $ipv4_1_handle \
   -action apply_on_the_fly_changes]
if {[keylget applyChanges status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget applyChanges log]"
    return 0
}
after 5000

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
puts "Fetching IGMP Host aggregated statistics"
set igmpHostStat [::ixiangpf::emulation_igmp_info \
    -handle $deviceGroup_1_handle \
    -type host \
    -mode aggregate]
if {[keylget igmpHostStat status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmpHostStat log]"
    return 0
}
foreach stat $igmpHostStat {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}

puts "Fetching IGMP Querier aggregated statistics"
set igmpQuerierStat [::ixiangpf::emulation_igmp_info \
    -handle $deviceGroup_2_handle \
    -type querier \
    -mode aggregate]
if {[keylget igmpQuerierStat status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmpQuerierStat log]"
    return 0
}
foreach stat $igmpQuerierStat {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}

############################################################################
# Stop L2-L3 traffic started earlier                                       #
############################################################################
puts "Stopping Traffic..."
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
# Stop all protocols                                                       #
############################################################################
puts "Stopping all protocol(s) ..."
set r [::ixiangpf::test_control -action stop_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
after 2000

puts "!!! Test Script Ends !!!"
return 1
