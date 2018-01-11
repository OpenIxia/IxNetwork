################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    09/04/2015 - Abhijit Dhar - created sample                                #
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
#                                                                              #        
# This test script intends to describe capability of HLT scripts in the context#
# of ISIS-SR. It configures two ISIS router back to back. One of them has      #
# simulated topology (type linier) configured behind it. The script does       #
# the following operations.                                                    #  
# 1. Starts the routers.                                                       #
# 2. Starts the simulated topology (after waiting for a while).                #
# 3. Checks for learned info.                                                  # 
# 4. Execute disconnect from node operation on the simulated topology.         #
# 5. Checks for learned info.                                                  #
# 6. Execute reconnect from node operation on the simulated topology.          #
# 7. Checks for learned info.                                                  #
# 8. Stops simulated topology.                                                 #
# 9. Checks for learned info.                                                  #
#10. Stops the routers.                                                        #
#                                                                              #
# Ixia Software:                                                               #
#     IxOS : 6.90 EA                                                           #
#     IxNetwork : 7.50 EA                                                      # 
################################################################################
#-------------------------------------------------------------------------------
# include HLT package
#-------------------------------------------------------------------------------
package req Ixia

#-------------------------------------------------------------------------------
# set chassis card port info
#-------------------------------------------------------------------------------
set chassis   10.205.28.182
set client    10.205.28.41
set card1     1
set port1     3
set card2     1
set port2     4
set ixNetport 8074
set port_list [list $card1/$port1 $card2/$port2]
set test_name [info script]

#-------------------------------------------------------------------------------
# connect to ixnetwork
#-------------------------------------------------------------------------------
puts "Connecting to Ixnetwork"
set connect_status [::ixiangpf::connect     \
    -reset                1                 \
    -device               $chassis          \
    -port_list            $port_list        \
    -ixnetwork_tcl_server $client:$ixNetport\
    -tcl_server           $chassis          \
]

if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_handle [list]
foreach port $port_list {
    set temp_port [keylget connect_status port_handle.$chassis.$port]
    lappend port_handle $temp_port
}
set port_0 [lindex $port_handle 0]
set port_1 [lindex $port_handle 1]

#-------------------------------------------------------------------------------
# Add topology1
#-------------------------------------------------------------------------------
puts "Adding topology1"
set topology_1_status [::ixiangpf::topology_config\
    -topology_name    {Topology 1}                \
    -port_handle      $port_0                     \
]

if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_1_status log]"
    return 0
}

set topology_1_handle [keylget topology_1_status topology_handle]

#-------------------------------------------------------------------------------
# Add device group1
#-------------------------------------------------------------------------------
puts "Adding device group1"
set device_group_1_status [::ixiangpf::topology_config\
    -topology_handle              $topology_1_handle  \
    -device_group_name            {Device Group 1}    \
    -device_group_multiplier      1                   \
    -device_group_enabled         1                   \
]

if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_1_status log]"
    return 0
}

set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

#-------------------------------------------------------------------------------
# Add ethernet stack1
#-------------------------------------------------------------------------------
puts "Adding ethernet stack1"
set ethernet_1_status [::ixiangpf::interface_config\
        -protocol_name     {Ethernet 1}            \
        -protocol_handle   $deviceGroup_1_handle   \
        -mtu               1500                    \
        -src_mac_addr      00.11.01.00.00.01       \
        -src_mac_addr_step 00.00.00.00.00.00       \
        -vlan              1                       \
        -vlan_id           1                       \
]

if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_1_status log]"
    return 0
}

set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]

#-------------------------------------------------------------------------------
# Add ISIS router1
#-------------------------------------------------------------------------------
puts "Adding ISIS router1"
set isis_l3_1_status [::ixiangpf::emulation_isis_config\
        -handle               $ethernet_1_handle       \
        -mode                 create                   \
        -protocol_name        {ISIS-L3 IF 1}           \
        -intf_ip_addr         1.1.1.1                  \
        -gateway_ip_addr      1.1.1.2                  \
        -area_id              490001                   \
        -attach_bit           1                        \
        -discard_lsp          0                        \
        -intf_type            ptop                     \
        -routing_level        L2                       \
        -system_id            64:01:00:01:00:00        \
        -system_id_step       00:00:00:00:00:00        \
        -wide_metrics         1                        \
        -level2_dead_interval 30                       \
        -auto_adjust_mtu      1                        \
        -auto_adjust_area     1                        \
        -active               1                        \
        -if_active            1                        \
        -enable_sr            1                        \
        -node_prefix          1.1.1.1                  \
        -mask                 32                       \
        -start_sid_label      1600                     \
        -sid_count            100                      \
]

if {[keylget isis_l3_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_l3_1_status log]"
    return 0
}

set isisL3_1_handle [keylget isis_l3_1_status isis_l3_handle]

#--------------------------------------------------------------------------------
# Configure simulated topology1 type == linear
#--------------------------------------------------------------------------------
puts "Adding simulated topology1 linear"
set network_group_1_status [::ixiangpf::network_group_config\
    -protocol_handle             $deviceGroup_1_handle      \
    -protocol_name               {Network Group 1}          \
    -multiplier                  1                          \
    -enable_device               1                          \
    -type                        linear                     \
    -linear_nodes                1                          \
    -linear_link_multiplier      1                          \
]

if {[keylget network_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_group_1_status log]"
    return 0
}

set networkGroup_1_handle [keylget network_group_1_status network_group_handle]

#--------------------------------------------------------------------------------
# Configure ISIS and ISIS-SR related parameters in the simulated topology1
#--------------------------------------------------------------------------------
puts "Configuring ISIS route parameter in the simulated topology"
set network_isis_grp_status [::ixiangpf::emulation_isis_network_group_config\
    -handle                                           $networkGroup_1_handle\
    -mode                                             modify                \
    -connected_to_handle                              $ethernet_1_handle    \
    -router_system_id                                 a1:01:00:00:00:01     \
    -enable_wide_metric                               1                     \
    -node_active                                      1                     \
    -from_ip                                          1.0.0.1               \
    -to_ip                                            1.0.0.2               \
    -enable_ip                                        1                     \
    -subnet_prefix_length                             24                    \
    -to_node_active                                   1                     \
    -to_node_link_metric                              10                    \
    -from_node_active                                 1                     \
    -from_node_link_metric                            10                    \
    -sim_topo_active                                  1                     \
    -grid_router_active                               1                     \
    -grid_router_id                                   213.1.0.0             \
    -grid_router_ip_pfx_len                           16                    \
    -grid_stub_per_router                             1                     \
    -grid_router_route_step                           1                     \
    -grid_router_metric                               0                     \
    -grid_router_origin                               stub                  \
    -grid_router_up_down_bit                          0                     \
    -grid_node_step                                   56                    \
    -link_type                                        pttopt                \
    -si_enable_adj_sid                                1                     \
    -si_adj_sid                                       8001                  \
    -pseudo_node_enable_sr                            1                     \
    -pseudo_node_node_prefix                          11.11.11.11           \
    -pseudo_node_mask                                 32                    \
    -pseudo_node_rtrcap_id                            1.1.1.1               \
    -pseudo_node_d_bit                                0                     \
    -pseudo_node_sid_index_label                      16                    \
    -pseudo_node_algorithm                            0                     \
    -pseudo_node_srgb_range_count                     1                     \
    -pseudo_node_start_sid_label                      10                    \
    -pseudo_node_sid_count                            50                    \
    -pseudo_node_route_ipv4_configure_sid_index_label 1                     \
    -pseudo_node_route_ipv4_sid_index_label           16                    \
]

if {[keylget network_isis_grp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget network_isis_grp_status log]"
    return 0
}

set simtopo_1_handle [keylget network_isis_grp_status simulated_topology_handle]

#-------------------------------------------------------------------------------
# Add topology2
#-------------------------------------------------------------------------------
puts "Adding topology2"
set topology_2_status [::ixiangpf::topology_config\
    -topology_name    {Topology 2}                \
    -port_handle      $port_1                     \
]

if {[keylget topology_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_2_status log]"
    return 0
}

set topology_2_handle [keylget topology_2_status topology_handle]

#-------------------------------------------------------------------------------
# Add device group2
#-------------------------------------------------------------------------------
puts "Adding device group2"
set device_group_2_status [::ixiangpf::topology_config\
    -topology_handle              $topology_2_handle  \
    -device_group_name            {Device Group 2}    \
    -device_group_multiplier      1                   \
    -device_group_enabled         1                   \
]

if {[keylget device_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_2_status log]"
    return 0
}

set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]

#-------------------------------------------------------------------------------
# Add ethernet stack2
#-------------------------------------------------------------------------------
puts "Adding ethernet stack2"
set ethernet_2_status [::ixiangpf::interface_config\
    -protocol_name       {Ethernet 2}              \
    -protocol_handle     $deviceGroup_2_handle     \
    -mtu                 1500                      \
    -src_mac_addr        00.12.01.00.00.01         \
    -src_mac_addr_step   00.00.00.00.00.00         \
    -vlan                1                         \
    -vlan_id             1                         \
]

if {[keylget ethernet_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_2_status log]"
    return 0
}

set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]

#-------------------------------------------------------------------------------
# Add ISIS router2
#-------------------------------------------------------------------------------
puts "Adding ISIS router2"
set isis_l3_2_status [::ixiangpf::emulation_isis_config\
    -handle               $ethernet_2_handle           \
    -mode                 create                       \
    -protocol_name        {ISIS-L3 IF 2}               \
    -intf_ip_addr         1.1.1.2                      \
    -gateway_ip_addr      1.1.1.1                      \
    -area_id              500001                       \
    -attach_bit           1                            \
    -discard_lsp          0                            \
    -intf_type            ptop                         \
    -routing_level        L2                           \
    -system_id            65:01:00:01:00:00            \
    -system_id_step       00:00:00:00:00:00            \
    -wide_metrics         1                            \
    -level2_dead_interval 30                           \
    -auto_adjust_mtu      1                            \
    -auto_adjust_area     1                            \
    -active               1                            \
    -if_active            1                            \
    -enable_sr            1                            \
    -node_prefix          1.1.1.2                      \
    -mask                 32                           \
]

if {[keylget isis_l3_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_l3_2_status log]"
    return 0
}

set isisL3_2_handle [keylget isis_l3_2_status isis_l3_handle]

#-------------------------------------------------------------------------------
# Starting ISIS router1
#-------------------------------------------------------------------------------
puts "Starting ISIS router1"
set status [::ixiangpf::emulation_isis_control\
    -handle $isisL3_1_handle                  \
    -mode   "start"                           \
]

if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

after 1000

#-------------------------------------------------------------------------------
# Starting ISIS router2
#-------------------------------------------------------------------------------
puts "Starting ISIS router2"
set status [::ixiangpf::emulation_isis_control\
    -handle $isisL3_2_handle                  \
    -mode   "start"                           \
]

if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

after 1000

puts "Waiting for 120 seconds"
after 120000

#-------------------------------------------------------------------------------
# Fetching ISIS statistics
#-------------------------------------------------------------------------------
puts "Fetching statistics on ISIS router2"
set status [::ixiangpf::emulation_isis_info\
    -handle $isisL3_2_handle               \
    -mode   "stats"                        \
]

if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

#-------------------------------------------------------------------------------
# printing stat values
#-------------------------------------------------------------------------------
foreach stat $status {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}

#-------------------------------------------------------------------------------
# Starting simulated topology1
#-------------------------------------------------------------------------------
puts "Starting simulated topology1"
set status [::ixiangpf::emulation_isis_control\
    -handle $simtopo_1_handle                 \
    -mode   "start"                           \
]

if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

after 5000

#-------------------------------------------------------------------------------
# Fetching learned info
#-------------------------------------------------------------------------------
puts "fetching learned info on ISIS router2"
set status [::ixiangpf::emulation_isis_info\
    -handle $isisL3_2_handle               \
    -mode   "learned_info"                 \
]

if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

#-------------------------------------------------------------------------------
# printing learned info
#-------------------------------------------------------------------------------
foreach stat $status {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}

#------------------------------------------------------------------------------
# "Executing 'disconnect from node' operation on simulated topology1
#------------------------------------------------------------------------------
puts "Executing 'disconnect from node' operation on simulated topology1"
set sim_interface_hndl [keylget network_isis_grp_status from_node_handle]
set status [::ixiangpf::emulation_isis_control\
    -handle $sim_interface_hndl               \
    -mode   "disconnect"                      \
]

if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

after 5000

#-------------------------------------------------------------------------------
# Fetching learned info
#-------------------------------------------------------------------------------
puts "Fetching learned info on ISIS router2"
set status [::ixiangpf::emulation_isis_info\
    -handle $isisL3_2_handle               \
    -mode   "learned_info"                 \
]

if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

#-------------------------------------------------------------------------------
# printing learned info
#-------------------------------------------------------------------------------
foreach stat $status {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}
after 5000

#-------------------------------------------------------------------------------
# Executing 'reconnect from node' operation on simulated topology1
#-------------------------------------------------------------------------------
puts "Executing 'reconnect from node' operation on simulated topology1"
set status [::ixiangpf::emulation_isis_control\
    -handle $sim_interface_hndl               \
    -mode   "reconnect"                       \
]

if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

after 5000

#-------------------------------------------------------------------------------
# Fetching learned info
#-------------------------------------------------------------------------------
puts "Fetching learned info on ISIS router2"
set status [::ixiangpf::emulation_isis_info\
    -handle $isisL3_2_handle               \
    -mode   "learned_info"                 \
]

if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

#-------------------------------------------------------------------------------
# printing learned info
#-------------------------------------------------------------------------------
foreach stat $status {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}

#-------------------------------------------------------------------------------
# Stopping simulated topology1
#-------------------------------------------------------------------------------
puts "Stopping simulated topology1"
set status [::ixiangpf::emulation_isis_control\
    -handle $simtopo_1_handle                 \
    -mode   "stop"                            \
]

if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

after 5000

#-------------------------------------------------------------------------------
# Fetching learned info
#-------------------------------------------------------------------------------
puts "Fetching learned info on ISIS router2"
set status [::ixiangpf::emulation_isis_info\
    -handle $isisL3_2_handle               \
    -mode   "learned_info"                 \
]

if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

#-------------------------------------------------------------------------------
# printing learned info
#-------------------------------------------------------------------------------
foreach stat $status {
    puts "=================================================================="
    puts "$stat"
    puts "=================================================================="
}

#-------------------------------------------------------------------------------
# Stopping ISIS router1
#-------------------------------------------------------------------------------
puts "Stopping ISIS router1"
set status [::ixiangpf::emulation_isis_control\
    -handle $isisL3_1_handle                  \
    -mode   "start"                           \
]

if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

after 1000

#-------------------------------------------------------------------------------
# Stopping ISIS router2
#-------------------------------------------------------------------------------
puts "Stopping ISIS router2"
set status [::ixiangpf::emulation_isis_control\
    -handle $isisL3_2_handle                  \
    -mode   "start"                           \
]

if {[keylget status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget status log]"
    return 0
}

#-------------------------------------------------------------------------------
# Test Ends
#-------------------------------------------------------------------------------
puts "TEST FINISHED SUCCESSFULLY !"

return 1

