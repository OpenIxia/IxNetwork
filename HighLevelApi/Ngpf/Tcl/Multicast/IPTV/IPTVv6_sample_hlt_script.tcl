################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    01/15/2015 - Sumeer Kumar - created sample                                #
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
#    This script intends to demonstrate how to use NGPF IPTVv6 API.            #
#                                                                              #
#    1. It will create one MLD Host topology and one IPv6 topology.            #
#    2. Configure IPTV on MLD host.                                            #
#    3. Start all protocols.                                                   #
#    4. Retrieve protocol statistics.                                          #
#    5. Configure L2-L3 traffic.                                               #
#    6. Start the L2-L3 traffic.                                               #
#    7. Stat IPTV.                                                             #  
#    8. Retrieve L2-L3 traffic stats.                                          #
#    9. Make on the fly changes of IPTV attributes                             #	
#   10. Retrieve protocol statistics.                                          #
#   11. Stop IPTV.                                                             #
#   12. Stop L2-L3 traffic.                                                    #
#   13. Stop all protocols.                                                    #
#                                                                              #
# Ixia Software:                                                               #
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
set topology_1_status [::ixiangpf::topology_config\
    -topology_name      {MLD Topology 1}         \
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
    -topology_name      {IPv6 Topology 2}          \
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

# Creating IPv6 Stack on top of Ethernet Stack for the first Device Group                                 
puts "Creating IPv6 Stack on top of Ethernet Stack for the first Device Group"
set ipv6_1_status [::ixiangpf::interface_config \
    -protocol_name                     {IPv6 1}                \
    -protocol_handle                   $ethernet_1_handle      \
    -ipv6_multiplier                   1                       \
    -ipv6_resolve_gateway              1                       \
    -ipv6_manual_gateway_mac           00.00.00.00.00.01       \
    -ipv6_manual_gateway_mac_step      00.00.00.00.00.00       \
    -ipv6_gateway                      20:0:0:0:0:0:0:1        \
    -ipv6_gateway_step                 ::0                     \
    -ipv6_intf_addr                    20:0:0:0:0:0:0:2        \
    -ipv6_intf_addr_step               ::0                     \
    -ipv6_prefix_length                64                      \
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
    -ipv6_multiplier                   1                       \
    -ipv6_resolve_gateway              1                       \
    -ipv6_manual_gateway_mac           00.00.00.00.00.01       \
    -ipv6_manual_gateway_mac_step      00.00.00.00.00.00       \
    -ipv6_gateway                      20:0:0:0:0:0:0:2        \
    -ipv6_gateway_step                 ::0                     \
    -ipv6_intf_addr                    20:0:0:0:0:0:0:1        \
    -ipv6_intf_addr_step               ::0                     \
    -ipv6_prefix_length                64                      \
]
if {[keylget ipv6_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv6_2_status log]"
    return 0
}
set ipv6_2_handle [keylget ipv6_2_status ipv6_handle]

################################################################################
# Other protocol configurations                                                # 
################################################################################

# This will create MLD v2 Host Stack with IPTV enabled on top of IPv6 stack having zap behavior as zap and view, zapping type as multicast to leave and zap direction as down.

puts "Creating MLD Host Stack on top of IPv6 1 stack"
set mld_host_1_status [::ixiangpf::emulation_mld_config       \
    -mode                                 create              \
    -handle                               $ipv6_1_handle      \
    -mld_version                          v2                  \
    -name                                 {MLD Host 1}        \
    -enable_iptv                          1                   \
    -iptv_name                            {IPTV 1}            \
    -stb_leave_join_delay                 3000                \
    -join_latency_threshold               10000               \
    -leave_latency_threshold              10000               \
    -zap_behavior                         zapandview          \
    -zap_direction                        down                \
    -zap_interval_type                    multicasttoleave    \
    -zap_interval                         10000               \
    -num_channel_changes_before_view      1                   \
    -view_duration                        10000               \
    -log_failure_timestamps               0                   \
]
if {[keylget mld_host_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget mld_host_1_status log]"
    return 0
}
set mldHost_1_handle [keylget mld_host_1_status mld_host_handle]
set mld_host_iptv_handle [keylget mld_host_1_status mld_host_iptv_handle]

# Creating MLD Group Ranges 
puts "Creating MLD Group Ranges"    
set mld_mcast_i_pv6_group_list_1_status [::ixiangpf::emulation_multicast_group_config \
    -mode               create             \
    -ip_addr_start      ff0a:0:0:0:0:0:0:1 \
    -ip_addr_step       0:0:0:0:0:0:0:0    \
    -num_groups         1                  \
    -active             1                  \
]
if {[keylget mld_mcast_i_pv6_group_list_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget mld_mcast_i_pv6_group_list_1_status log]"
    return 0
}
set mldMcastIPv6GroupList_1_handle [keylget mld_mcast_i_pv6_group_list_1_status multicast_group_handle]
    
# Creating MLD Source Ranges
puts "Creating MLD Source Ranges"
set mld_ucast_i_pv6_source_list_1_status [::ixiangpf::emulation_multicast_source_config \
    -mode               create           \
    -ip_addr_start      20:0:0:0:0:0:0:1 \
    -ip_addr_step       0:0:0:0:0:0:0:0  \
    -num_sources        1                \
    -active             1                \
]
if {[keylget mld_ucast_i_pv6_source_list_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget mld_ucast_i_pv6_source_list_1_status log]"
    return 0
}
set mldUcastIPv6SourceList_1_handle [keylget mld_ucast_i_pv6_source_list_1_status multicast_source_handle]
   
# Creating MLD Group and Source Ranges in MLD Host stack
puts "Creating MLD Group and Source Ranges in MLD Host stack"
set mld_host_1_status [::ixiangpf::emulation_mld_group_config \
    -mode                    create                           \
    -g_filter_mode           include                          \
    -group_pool_handle       $mldMcastIPv6GroupList_1_handle  \
    -no_of_grp_ranges        1                                \
    -no_of_src_ranges        1                                \
    -session_handle          $mldHost_1_handle                \
    -source_pool_handle      $mldUcastIPv6SourceList_1_handle \
]
if {[keylget mld_host_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget mld_host_1_status log]"
    return 0
}

# Configuring inter stb delay and rate control for MLD Host global settings
puts "Configuring inter stb delay and rate control for MLD host"    
set mld_host_2_status [::ixiangpf::emulation_mld_config \
    -mode                          create        \
    -handle                        /globals      \
    -global_settings_enable        1             \
    -no_of_reports_per_second      500           \
    -interval_in_ms                1000          \
    -inter_stb_start_delay         1000          \
]
if {[keylget mld_host_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget mld_host_2_status log]"
    return 0
}

puts "Waiting 5 seconds before starting protocol(s) ..."
after 5000
  
############################################################################
# Start MLD protocol                                                       #
############################################################################
puts "Starting MLD on topology1"
set protocol_status [::ixiangpf::emulation_mld_control \
    -mode start \
    -handle $mldHost_1_handle]
if {[keylget protocol_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_status log]"
    return 0
}
    
puts "Starting IPv6 on topology2"
set protocol_status [::ixiangpf::test_control \
    -handle $ipv6_2_handle \
    -action start_protocol]
if {[keylget protocol_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_status log]"
    return 0
}

puts "Waiting for 30 seconds"
after 30000

############################################################################
# Retrieve protocol statistics                                             #
############################################################################
puts "Fetching MLD aggregated statistics"
set mldHostStat [::ixiangpf::emulation_mld_info \
    -handle $deviceGroup_1_handle \
    -type host \
    -mode aggregate]
if {[keylget mldHostStat status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget mldHostStat log]"
    return 0
}
foreach stat $mldHostStat {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}

############################################################################ 
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv6, Destination->Multicast group                #
# 2. Type      : Multicast IPv6 traffic                                    #
# 3. Flow Group: On IPv6 Destination Address                               #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : IPv6 Destination Address                                  #	
############################################################################
puts "Configuring L2-L3 traffic"
set _result_ [::ixiangpf::traffic_config                                                    \
    -mode                                       create                                  \
    -traffic_generator                          ixnetwork_540                           \
    -endpointset_count                          1                                       \
    -emulation_src_handle                       $ipv6_2_handle                          \
    -emulation_dst_handle                       $mldMcastIPv6GroupList_1_handle         \
    -emulation_multicast_dst_handle             ff0a:0:0:0:0:0:0:1/0:0:0:0:0:0:0:0/1    \
    -emulation_multicast_dst_handle_type        none                                    \
    -emulation_multicast_rcvr_handle            $mldMcastIPv6GroupList_1_handle         \
    -emulation_multicast_rcvr_port_index        0                                       \
    -emulation_multicast_rcvr_host_index        0                                       \
    -emulation_multicast_rcvr_mcast_index       0                                       \
    -name                                       Traffic_Item_1                          \
    -circuit_endpoint_type                      ipv6                                    \
    -transmit_distribution                      ipv6DestIp0                             \
    -rate_pps                                   1000                                    \
    -frame_size                                 512                                     \
    -track_by                                   {trackingenabled0 ipv6DestIp0}          \
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
    -action            run           \
    -traffic_generator ixnetwork_540 \
    -type              l23           \
]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "Let the traffic run for 20 seconds ..."
after 20000
   
############################################################################
# Starting IPTV                                                            #
############################################################################
puts "Starting IPTV..."
set startIPTVGlobal [::ixiangpf::emulation_mld_control \
    -handle $mld_host_iptv_handle\
    -mode   start]
if {[keylget startIPTVGlobal status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget startIPTVGlobal log]"
    return 0
}
after 10000   

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
  
################################################################################
# Making on the fly changes for zapDirection, zapIntervalType, zapInterval,    #
# numChannelChangesBeforeView and viewDuration in IPTV tab of MLD host         #
################################################################################
puts "Making on the fly chnages for zapDirection, zapIntervalType, zapInterval,\
    numChannelChangesBeforeView and viewDuration"
set mld_host_1_status [::ixiangpf::emulation_mld_config       \
    -handle                               $mldHost_1_handle   \
    -mode                                 modify              \
    -zap_direction                        up                  \
    -zap_interval_type                    leavetoleave        \
    -zap_interval                         30000               \
    -num_channel_changes_before_view      4                   \
    -view_duration                        40000               \
]
if {[keylget mld_host_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget mld_host_1_status log]"
    return 0
}

################################################################################
# Applying changes one the fly                                                 #
################################################################################
puts "Applying changes on the fly"
set applyChanges [::ixiangpf::test_control \
   -handle $ipv6_1_handle \
   -action apply_on_the_fly_changes]
if {[keylget applyChanges status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget applyChanges log]"
    return 0
}
after 5000
     
################################################################################
# Retrieve protocol statistics after doing on the fly changes                  #
################################################################################

puts "Fetching MLD aggregated statistics"
set mldHostStat [::ixiangpf::emulation_mld_info \
        -handle $deviceGroup_1_handle\
        -type host \
        -mode aggregate]
if {[keylget mldHostStat status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget mldHostStat log]"
    return 0
}
foreach stat $mldHostStat {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}

################################################################################
# Stopping IPTV                                                                #
################################################################################
puts "Stopping IPTV..."
set stopIPTVGlobal [::ixiangpf::emulation_mld_control \
    -handle $mld_host_iptv_handle\
    -mode   stop]
if {[keylget stopIPTVGlobal status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget stopIPTVGlobal log]"
    return 0
}
after 2000

################################################################################
# Stop L2-L3 traffic started earlier                                           #	
################################################################################
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
   
################################################################################
# Stop all protocols                                                           #
################################################################################
puts "Stopping all protocol(s) ..."
set r [::ixiangpf::test_control -action stop_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "!!! Test Script Ends !!!"           
return 1     
