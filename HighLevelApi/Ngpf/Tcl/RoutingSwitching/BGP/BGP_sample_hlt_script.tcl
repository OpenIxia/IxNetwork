################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    02/01/2015 - Rudra Dutta - created sample                                 #
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
#    This script intends to demonstrate how to use NGPF BGP API.               #
#                                                                              #
#    1. It will create 2 BGP topologies, each having an ipv4 network           #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. A loopback device group(DG) behind network   # 
#       group is needed to support applib traffic.                             #
#    2. Start BGP protocol.                                                    #
#    3. Retrieve protocol statistics.                                          #
#    4. Enable IPv4 Learned Information on the fly                             #
#    5. Retrieve protocol learned information                                  #
#    6. Configure L2-L3 traffic.                                               #
#    7. Configure application traffic.                                         #
#    8. Start the L2-L3 traffic.                                               #
#   9. Start the application traffic.                                          #
#   10. Retrieve Appilcation traffic stats.                                    #
#   11. Retrieve L2-L3 traffic stats.                                          #
#   12. Stop L2-L3 traffic.                                                    #
#   13. Stop Application traffic.                                              #
#   14. Stop all protocols.                                                    #
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
# Connection to the chassis, IxNetwork Tcl Server                              #
################################################################################
set chassis_ip        {10.205.28.170}
set tcl_server        10.205.28.170
set port_list         {1/7 1/8}
set ixNetwork_client  "10.205.28.41:8981"
set test_name         [info script]

# Connecting to chassis and client
puts "Connecting to Chassis and Client"
set connect_status [::ixiangpf::connect         \
    -reset                   1                  \
    -device                  $chassis_ip        \
    -port_list               $port_list         \
    -ixnetwork_tcl_server    $ixNetwork_client  \
    -tcl_server              $tcl_server        \
]

if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}
puts "Connection to Chassis Successful"

# Retrieving port handles, for later use
set port1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]

################################################################################
# Creating Topology and Device Group                                           #
################################################################################

# Creating a Topology on First Port
puts "Adding Topology 1 on Port 1"  
set topology_1_status [::ixiangpf::topology_config  \
    -topology_name      {BGP Topology 1}            \
    -port_handle        $port1                      \
]
if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_1_status log]"
    return 0
}
set topology_1_handle [keylget topology_1_status topology_handle]

# Creating a device group in topology 
puts "Creating device group 1 in topology 1"  
set device_group_1_status [::ixiangpf::topology_config  \
    -topology_handle              $topology_1_handle    \
    -device_group_name            {Device Group 1}      \
    -device_group_multiplier      1                     \
    -device_group_enabled         1                     \
]
if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_1_status log]"
    return 0
}
set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

# Creating a Topology on Second Port
puts "Adding Topology 2 on Port 2"
set topology_2_status [::ixiangpf::topology_config  \
    -topology_name      {BGP Topology 2}            \
    -port_handle        $port2                      \
]
if {[keylget topology_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_2_status log]"
    return 0
}
set topology_2_handle [keylget topology_2_status topology_handle]

# Creating a Device Group in Topology
puts "Creating Device Group 2 in Topology 2"
set device_group_3_status [::ixiangpf::topology_config  \
    -topology_handle              $topology_2_handle    \
    -device_group_name            {Device Group 2}      \
    -device_group_multiplier      1                     \
    -device_group_enabled         1                     \
]
if {[keylget device_group_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_3_status log]"
    return 0
}
set deviceGroup_3_handle [keylget device_group_3_status device_group_handle]

################################################################################
#  Configure protocol interfaces                                               #
################################################################################

# Creating Ethernet Stack for the First Device Group 
puts "Creating Ethernet Stack for the First Device Group on Port 1"
set ethernet_1_status [::ixiangpf::interface_config      \
    -protocol_name                {Ethernet 1}           \
    -protocol_handle              $deviceGroup_1_handle  \
    -mtu                          1500                   \
    -src_mac_addr                 18.03.73.c7.6c.b1      \
    -src_mac_addr_step            00.00.00.00.00.00      \
]
if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_1_status log]"
    return 0
}
set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]

# Creating Ethernet Stack for the First Device Group
puts "Creating Ethernet for the First Device Group on Port 2"
set ethernet_2_status [::ixiangpf::interface_config      \
    -protocol_name                {Ethernet 2}           \
    -protocol_handle              $deviceGroup_3_handle  \
    -mtu                          1500                   \
    -src_mac_addr                 18.03.73.c7.6c.01      \
    -src_mac_addr_step            00.00.00.00.00.00      \
]
if {[keylget ethernet_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_2_status log]"
    return 0
}
set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]

# Creating IPv4 Stack for the First Device Group
puts "Creating IPv4 Stack for First Device Group on Port 1"
set ipv4_1_status [::ixiangpf::interface_config            \
    -protocol_name                     {IPv4 1}            \
    -protocol_handle                   $ethernet_1_handle  \
    -ipv4_resolve_gateway              1                   \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01   \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00   \
    -gateway                           20.20.20.1          \
    -gateway_step                      0.0.0.0             \
    -intf_ip_addr                      20.20.20.2          \
    -intf_ip_addr_step                 0.0.0.0             \
    -netmask                           255.255.255.0       \
]
if {[keylget ipv4_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_1_status log]"
    return 0
}
set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]

# Creating IPv4 Stack for the first Device Group 
puts "Creating IPv4 Stack for the First Device Group on Port 2"
set ipv4_2_status [::ixiangpf::interface_config            \
    -protocol_name                     {IPv4 2}            \
    -protocol_handle                   $ethernet_2_handle  \
    -ipv4_resolve_gateway              1                   \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01   \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00   \
    -gateway                           20.20.20.2          \
    -gateway_step                      0.0.0.0             \
    -intf_ip_addr                      20.20.20.1          \
    -intf_ip_addr_step                 0.0.0.0             \
    -netmask                           255.255.255.0       \
]
if {[keylget ipv4_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_2_status log]"
    return 0
}
set ipv4_2_handle [keylget ipv4_2_status ipv4_handle]

################################################################################
# Other protocol configurations                                                # 
################################################################################

# This will create BGP Stack on top of IPv4 stack

# Creating BGP Stack on top of IPv4 Stack on Port 1 
puts "Creating BGP Stack on top of IPv4 Stack in Topology 1"
set bgp_ipv4_peer_1_status [::ixiangpf::emulation_bgp_config  \
    -mode                                    enable           \
    -active                                  1                \
    -handle                                  $ipv4_1_handle   \
    -remote_ip_addr                          20.20.20.1       \
]
if {[keylget bgp_ipv4_peer_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_ipv4_peer_1_status log]"
    return 0
}
set bgpIpv4Peer_1_handle [keylget bgp_ipv4_peer_1_status bgp_handle]

# Creating BGP Stack on top of IPv4 Stack on Port 2
puts "Creating BGP Stack on top of IPv4 Stack in Topology 2"
set bgp_ipv4_peer_2_status [::ixiangpf::emulation_bgp_config  \
    -mode                                    enable           \
    -active                                  1                \
    -handle                                  $ipv4_2_handle   \
    -remote_ip_addr                          20.20.20.2       \
]
if {[keylget bgp_ipv4_peer_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bgp_ipv4_peer_2_status log]"
    return 0
}
set bgpIpv4Peer_2_handle [keylget bgp_ipv4_peer_2_status bgp_handle]

# Creating Network Group behind First Device Group in Topology 1 Port 1
puts "Creating Network Group behind First Device Group in Topology 1"
set network_group_1_status [::ixiangpf::network_group_config     \
    -protocol_handle                      $deviceGroup_1_handle  \
    -protocol_name                        BGP_1_Network_Group1   \
    -multiplier                           1                      \
    -enable_device                        1                      \
    -connected_to_handle                  $ethernet_1_handle     \
    -type                                 ipv4-prefix            \
    -ipv4_prefix_network_address          200.1.0.0		         \
    -ipv4_prefix_length                   24                     \
    -ipv4_prefix_number_of_addresses      1                      \
]
if {[keylget network_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_1_status log]"
    return 0
}
set networkGroup_1_handle [keylget network_group_1_status network_group_handle]
set ipv4PrefixPools_1_handle [keylget network_group_1_status ipv4_prefix_pools_handle]

# Creating Second Device Group behind Network Group in Topology 1 Port 1
puts "Creating Second Device Group behind Network Group in Topology 1"	
set device_group_2_status [::ixiangpf::topology_config    \
    -device_group_name            {Device Group 4}        \
    -device_group_multiplier      1                       \
    -device_group_enabled         1                       \
    -device_group_handle          $networkGroup_1_handle  \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_2_status log]"
    return 0
}
set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]

# Adding IPv4 Loopback Interface in Second Device Group in Topology 1 Port 1
puts "Adding IPv4 Loopback Interface in Second Device Group in Topology 1"    
set ipv4_loopback_1_status [::ixiangpf::interface_config  \
    -protocol_name            {IPv4 Loopback 2}           \
    -protocol_handle          $deviceGroup_2_handle       \
    -enable_loopback          1                           \
    -connected_to_handle      $networkGroup_1_handle      \
    -intf_ip_addr             200.1.0.0			  \
    -netmask                  255.255.255.255             \
]
if {[keylget ipv4_loopback_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_loopback_1_status log]"
    return 0
}

# Creating Network Group behind First Device Group in Topology 2 Port 2
puts "Creating Network Group behind First Device Group in Topology 2"
set network_group_3_status [::ixiangpf::network_group_config     \
    -protocol_handle                      $deviceGroup_3_handle  \
    -protocol_name                        BGP_2_Network_Group1   \
    -multiplier                           1                      \
    -enable_device                        1                      \
    -connected_to_handle                  $ethernet_2_handle     \
    -type                                 ipv4-prefix            \
    -ipv4_prefix_network_address          201.1.0.0		 \
    -ipv4_prefix_length                   24                     \
    -ipv4_prefix_number_of_addresses      1                      \
]
if {[keylget network_group_3_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_3_status log]"
    return 0
}
set networkGroup_3_handle [keylget network_group_3_status network_group_handle]
set ipv4PrefixPools_3_handle [keylget network_group_3_status ipv4_prefix_pools_handle]
	
# Creating Second Device Group behind Network Group in Topology 2 Port 2
puts "Creating Second Device Group behind Network Group in Topology 2"
set device_group_4_status [::ixiangpf::topology_config    \
    -device_group_name            {Device Group 3}        \
    -device_group_multiplier      1                       \
    -device_group_enabled         1                       \
    -device_group_handle          $networkGroup_3_handle  \
]
if {[keylget device_group_4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_4_status log]"
    return 0
}
set deviceGroup_4_handle [keylget device_group_4_status device_group_handle]
	
# Adding IPv4 Loopback Interface in Second Device Group in Topology 2 Port 2
puts "Adding IPv4 Loopback Interface in Second Device Group in Topology 2"
set ipv4_loopback_2_status [::ixiangpf::interface_config  \
    -protocol_name            {IPv4 Loopback 1}           \
    -protocol_handle          $deviceGroup_4_handle       \
    -enable_loopback          1                           \
    -connected_to_handle      $networkGroup_3_handle      \
    -intf_ip_addr             201.1.0.0			  \
    -netmask                  255.255.255.255             \
]

puts "Waiting 5 seconds before starting protocol"
after 5000
  
############################################################################
#  Start BGP protocol                                                      #
############################################################################
puts "Starting BGP on topology1" 
set protocol_status [::ixiangpf::emulation_bgp_control \
    -handle $topology_1_handle\
    -mode start]
if {[keylget protocol_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_status log]"
    return 0
}  

puts "Starting BGP on topology2" 
set protocol_status [::ixiangpf::emulation_bgp_control \
    -handle $topology_2_handle\
    -mode start]
if {[keylget protocol_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_status log]"
    return 0
}

puts "Waiting for 45 seconds"
after 45000

############################################################################
# Retrieve protocol statistics                                             # 
############################################################################
puts "Fetching BGP aggregated statistics on port 1"
set aggregate_stats [::ixiangpf::emulation_bgp_info \
    -handle $bgpIpv4Peer_1_handle \
    -mode "stats"]
if {[keylget aggregate_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget aggregate_stats log]"
    return 0
}
foreach stat $aggregate_stats {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}
puts "Fetching BGP aggregated statistics on port 2"
set aggregate_stats [::ixiangpf::emulation_bgp_info \
    -handle $bgpIpv4Peer_2_handle \
    -mode "stats"]
if {[keylget aggregate_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget aggregate_stats log]"
    return 0
}
foreach stat $aggregate_stats {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}


############################################################################
# Enabling BGP Learned Information on the fly                              #
############################################################################
puts "Enabling IPv4 Unicast Learned Information for BGP Router"
set protocol_status [::ixiangpf::emulation_bgp_config    \
    -handle   $bgpIpv4Peer_1_handle \
    -mode   modify                     \
    -ipv4_filter_unicast_nlri      1]
if {[keylget protocol_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_status log]"
    return 0
}

puts "Enabling IPv4 Unicast Learned Information for BGP Router"
set protocol_status [::ixiangpf::emulation_bgp_config    \
    -handle   $bgpIpv4Peer_2_handle \
    -mode   modify                     \
    -ipv4_filter_unicast_nlri      1] 
if {[keylget protocol_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_status log]"
    return 0
}

############################################################################
# Applying changes one the fly                                             #    
############################################################################
puts "Applying changes on the fly"     
set status [::ixiangpf::test_control -action apply_on_the_fly_changes]
if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

puts "Waiting for 10 seconds"
after 10000
    
############################################################################
# Retrieve protocol learned info                                           #
############################################################################
puts "Fetching BGP aggregated learned info on port 1"
set learned_info [::ixiangpf::emulation_bgp_info                                  \
    -handle $bgpIpv4Peer_1_handle \
    -mode "learned_info"
]
if {[keylget learned_info status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget learned_info log]"
    return 0
}
foreach info $learned_info {
    puts "=================================================================="
    puts "$info"
    puts "=================================================================="
}
  
puts "Fetching BGP aggregated learned info on port 2"
set learned_info [::ixiangpf::emulation_bgp_info                                  \
    -handle $bgpIpv4Peer_2_handle \
    -mode "learned_info"
]
if {[keylget learned_info status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget learned_info log]"
    return 0
}
foreach info $learned_info {
    puts "=================================================================="
    puts "$info"
    puts "=================================================================="
}

after 5000

############################################################################ 
# Configure L2-L3 Traffic                                                  #
# 1. Endpoints : Source->IPv4 Prefix Pool, Destination->IPv4 Prefix Pool   #
# 2. Type      : IPv4 Traffic                                              #
# 3. Flow Group: None                                                      #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : Source-Destination Endpoint Pair                          #	
############################################################################ 
puts "Configuring L2-L3 traffic"
set _result_ [::ixiangpf::traffic_config                                                                    \
    -mode                                     create                                                  \
    -traffic_generator                        ixnetwork_540                                           \
    -endpointset_count                        1                                                       \
    -emulation_src_handle                     $networkGroup_1_handle                                  \
    -emulation_dst_handle                     $networkGroup_3_handle                                  \
    -track_by                                 {sourceDestEndpointPair0 trackingenabled0}              \
    -rate_pps                                 1000                                                    \
    -frame_size                               512                                                     \
]
if {[keylget _result_ status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget _result_ log]"
    return 0
}

############################################################################
# Configure Application Traffic                                            #
############################################################################
puts "Configure Application Traffic"
# Creating the Application Traffic Profiles
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
  
# Creating the Traffic Item  
set traffic_item_1_status [::ixiangpf::traffic_l47_config           \
    -mode                        create                             \
    -name                        {Traffic Item 2}                   \
    -circuit_endpoint_type       ipv4_application_traffic           \
    -emulation_src_handle        $networkGroup_1_handle             \
    -emulation_dst_handle        $networkGroup_3_handle             \
    -objective_type              users                              \
    -objective_value             100                                \
    -objective_distribution      apply_full_objective_to_each_port  \
    -enable_per_ip_stats         0                                  \
    -flows                       $flowList
]
if {[keylget traffic_item_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_item_1_status log]"
    return 0
}

############################################################################
#  Start L2-L3 traffic configured earlier                                  #
############################################################################
puts "Running Traffic..."
set r [::ixiangpf::traffic_control \
    -action            run           \
    -traffic_generator ixnetwork_540 \
    -type              {l23 l47}           \
]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "Let the traffic run for 60 seconds ..."
after 60000

############################################################################
# Retrieve Appilcation traffic stats                                       #                                   
# Retrieve L2-L3 traffic stats                                             #
############################################################################
set r [::ixiangpf::traffic_stats          \
    -mode all                         \
    -traffic_generator ixnetwork_540  \
    -measure_mode mixed               \
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
# Stop application traffic started earlier                                 #
############################################################################
puts "Stopping Traffic..."
set r [::ixiangpf::traffic_control \
    -action stop \
    -traffic_generator ixnetwork_540 \
    -type {l23 l47} 
]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
   
############################################################################
# Stop all protocols                                                       #
############################################################################
puts "Stopping all protocol(s) ..."
set r [::ixia::test_control -action stop_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "!!!!! TEST ENDS !!!!!"
return 1
