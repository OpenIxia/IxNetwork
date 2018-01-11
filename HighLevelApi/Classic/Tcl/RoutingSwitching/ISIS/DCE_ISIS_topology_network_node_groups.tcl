################################################################################
# Version 1.0    $Revision: 1 $
# $Author: B. Danciu $
#
# $Workfile: DCE_ISIS_topology_multicast_ranges.tcl $
#
#    Copyright © 1997 - 2009 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    4-10-2009 create.
#
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample creates 3 DCE ISIS router bridges in Ixia back to back setup  #
# and adds a all types of network ranges on each bridge. Each bridge has a     #
# node mac group, node ipv4 group, node ipv6 group and outside link.           #
# Then it starts the router bridges and get protocol stats from port handles   #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module using HLTSET 48             #
#                                                                              #
################################################################################

set hltset "HLTSET48"
set env(IXIA_VERSION) $hltset

package require Ixia

set test_name [info script]

set chassisIP 10.205.19.121
set port_list [list 6/1 6/2]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                            \
        -reset                                                                 \
        -device                         $chassisIP                             \
        -port_list                      $port_list                             \
        -username                       ixiaApiUser                            \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
            temp_port]} {
        lappend port_handle $temp_port
    }
}
set port_0 [lindex $port_handle 0]
set port_1 [lindex $port_handle 1]

puts "Ixia port handles are: $port_0, $port_1 ..."
update idletasks

################################################################################
# Configure interface in the test
################################################################################
set interface_status [::ixia::interface_config                                 \
        -port_handle                    [list $port_0 $port_1]                 \
        -intf_mode                      ethernet                               \
        -autonegotiation                1                                      \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}
puts "Ixia port configuration returned: [keylget interface_status status] ..."
update idletasks

################################################################################
# Create protocol interface in the test
################################################################################
set interface_status [::ixia::interface_config                                 \
        -mode               modify                                             \
        -port_handle        [list $port_0           $port_0         $port_0]   \
        -intf_ip_addr       [list 21.1.1.1          22.1.1.1        23.1.1.1]  \
        -gateway            [list 21.1.1.2          22.1.1.2        23.1.1.2]  \
        -netmask            [list 255.255.255.0     255.255.255.0   255.255.255.0] \
        -ipv6_intf_addr     [list 21::1             22::1           23::1]         \
        -ipv6_prefix_length [list 64                64              64]            \
        -src_mac_addr       [list 0ab0.0021.0001    0ab0.0022.0002  0ab0.0023.0002]\
        ]
if {[keylget interface_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return  0
}
set interface_handle [keylget interface_status interface_handle]
set interface_0 [lindex $interface_handle 0]
set interface_1 [lindex $interface_handle 1]
set interface_2 [lindex $interface_handle 2]
puts "Ixia interface configuration returned: $interface_handle ..."
update idletasks
################################################################################
# Create protocol interface in the test
################################################################################
set interface_status [::ixia::interface_config                                 \
        -mode               modify                                             \
        -port_handle        [list $port_1           $port_1         $port_1]   \
        -intf_ip_addr       [list 21.1.1.2          22.1.1.2        23.1.1.2]  \
        -gateway            [list 21.1.1.1          22.1.1.1        23.1.1.1]  \
        -netmask            [list 255.255.255.0     255.255.255.0   255.255.255.0] \
        -ipv6_intf_addr     [list 21::2             22::2           23::2]         \
        -ipv6_prefix_length [list 64                64              64]            \
        -src_mac_addr       [list 0cd0.0021.0001    0cd0.0022.0002  0cd0.0023.0002]\
        ]
if {[keylget interface_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}
set interface_handle [keylget interface_status interface_handle]
set interface_3 [lindex $interface_handle 0]
set interface_4 [lindex $interface_handle 1]
set interface_5 [lindex $interface_handle 2]
puts "Ixia interface configuration returned: $interface_handle ..."
update idletasks
################################################################################
# Create DCE ISIS bridges
################################################################################
set isis_router_status [::ixia::emulation_isis_config                          \
        -mode                           create                                 \
        -reset                                                                 \
        -port_handle                    $port_0                                \
        -type                           dce_isis_draft_ward_l2_isis_04         \
        -intf_ip_addr                   21.1.1.1                               \
        -intf_ip_addr_step              1.0.0.0                                \
        -gateway_ip_addr                21.1.1.2                               \
        -gateway_ip_addr_step           1.0.0.0                                \
        -intf_ip_prefix_length          24                                     \
        -count                          3                                      \
        -wide_metrics                   0                                      \
        -discard_lsp                    0                                      \
        -attach_bit                     0                                      \
        ]
if {[keylget isis_router_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_router_status log]"
    return 0
}

#Get the list of ISIS router handle form the keye list returned
set isis_router_handle_list_0 [keylget isis_router_status handle]
set isis_router_handle_0 [lindex $isis_router_handle_list_0 0]
set isis_router_handle_1 [lindex $isis_router_handle_list_0 1]
set isis_router_handle_2 [lindex $isis_router_handle_list_0 2]
################################################################################
# Create DCE ISIS bridges
################################################################################
set isis_router_status [::ixia::emulation_isis_config                          \
        -mode                           create                                 \
        -reset                                                                 \
        -port_handle                    $port_1                                \
        -type                           dce_isis_draft_ward_l2_isis_04         \
        -interface_handle               [list $interface_3 $interface_4 $interface_5] \
        -count                          3                                      \
        -wide_metrics                   0                                      \
        -discard_lsp                    0                                      \
        -attach_bit                     0                                      \
        ]
if {[keylget isis_router_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_router_status log]"
    return 0
}
set isis_router_handle_list_1 [keylget isis_router_status handle]
set isis_router_handle_3 [lindex $isis_router_handle_list_1 0]
set isis_router_handle_4 [lindex $isis_router_handle_list_1 1]
set isis_router_handle_5 [lindex $isis_router_handle_list_1 1]

################################################################################
# Create DCE ISIS network ranges
################################################################################
# PORT 0
set i 1
set isis_network_handle_list_0 ""
foreach isis_router_handle $isis_router_handle_list_0 {
    set dce_bcast_root_pri                    10000                     ;# RANGE 0-65535 DEFAULT 65535
    set dce_bcast_root_pri_step               11                        ;# RANGE 0-65535 DEFAULT 0
    set dce_device_id                         12                        ;# RANGE 0-65535 DEFAULT 1
    set dce_device_id_step                    13                        ;# RANGE 0-65535 DEFAULT 1
    set dce_device_pri                        14                        ;# RANGE 0-255 DEFAULT 1
    set dce_ftag                              15                        ;# RANGE 0-65535 DEFAULT 1
    set dce_ftag_enable                       1                         ;# CHOICES 0 1 DEFAULT 0
    set dce_local_entry_point_column          2                         ;# RANGE 1-100000 DEFAULT 1
    set dce_local_entry_point_row             2                         ;# RANGE 1-100000 DEFAULT 1
    set dce_local_link_metric                 16                        ;# RANGE 0-63 DEFAULT 1
    set dce_local_num_columns                 2                         ;# RANGE 1-100000 DEFAULT 1
    set dce_local_num_rows                    2                         ;# RANGE 1-100000 DEFAULT 1
    set dce_num_mcast_destination_trees       17                        ;# RANGE 0-65535 DEFAULT 1
    set dce_system_id                         00.00.00.0A.0$i.00        ;#
    set dce_system_id_step                    00.00.00.00.00.18         ;#
    
    set net_config_status_$i [::ixia::emulation_isis_topology_route_config                \
            -mode                                  create                                 \
            -handle                                $isis_router_handle                    \
            -type                                  dce_network_range                      \
            -dce_bcast_root_pri                    $dce_bcast_root_pri                    \
            -dce_bcast_root_pri_step               $dce_bcast_root_pri_step               \
            -dce_device_id                         $dce_device_id                         \
            -dce_device_id_step                    $dce_device_id_step                    \
            -dce_device_pri                        $dce_device_pri                        \
            -dce_ftag                              $dce_ftag                              \
            -dce_ftag_enable                       $dce_ftag_enable                       \
            -dce_local_entry_point_column          $dce_local_entry_point_column          \
            -dce_local_entry_point_row             $dce_local_entry_point_row             \
            -dce_local_link_metric                 $dce_local_link_metric                 \
            -dce_local_num_columns                 $dce_local_num_columns                 \
            -dce_local_num_rows                    $dce_local_num_rows                    \
            -dce_num_mcast_destination_trees       $dce_num_mcast_destination_trees       \
            -dce_system_id                         $dce_system_id                         \
            -dce_system_id_step                    $dce_system_id_step                    \
            ]
    if {[keylget net_config_status_$i status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget net_config_status_$i log]"
    }
    set     isis_network_handle        [keylget net_config_status_$i elem_handle]
    lappend isis_network_handle_list_0 [keylget net_config_status_$i elem_handle]
    incr i
    
}

# PORT 1
set isis_network_handle_list_1 ""
foreach isis_router_handle $isis_router_handle_list_1 {
    set dce_bcast_root_pri                    20000                     ;# RANGE 0-65535 DEFAULT 65535
    set dce_bcast_root_pri_step               21                        ;# RANGE 0-65535 DEFAULT 0
    set dce_device_id                         22                        ;# RANGE 0-65535 DEFAULT 1
    set dce_device_id_step                    23                        ;# RANGE 0-65535 DEFAULT 1
    set dce_device_pri                        24                        ;# RANGE 0-255 DEFAULT 1
    set dce_ftag                              25                        ;# RANGE 0-65535 DEFAULT 1
    set dce_ftag_enable                       1                         ;# CHOICES 0 1 DEFAULT 0
    set dce_local_entry_point_column          2                         ;# RANGE 1-100000 DEFAULT 1
    set dce_local_entry_point_row             2                         ;# RANGE 1-100000 DEFAULT 1
    set dce_local_link_metric                 26                        ;# RANGE 0-63 DEFAULT 1
    set dce_local_num_columns                 2                         ;# RANGE 1-100000 DEFAULT 1
    set dce_local_num_rows                    2                         ;# RANGE 1-100000 DEFAULT 1
    set dce_num_mcast_destination_trees       27                        ;# RANGE 0-65535 DEFAULT 1
    set dce_system_id                         00.00.00.0B.0$i.00        ;#
    set dce_system_id_step                    00.00.00.00.00.28         ;#
    set net_config_status_$i [::ixia::emulation_isis_topology_route_config                \
            -mode                                  create                                 \
            -handle                                $isis_router_handle                    \
            -type                                  dce_network_range                      \
            -dce_bcast_root_pri                    $dce_bcast_root_pri                    \
            -dce_bcast_root_pri_step               $dce_bcast_root_pri_step               \
            -dce_device_id                         $dce_device_id                         \
            -dce_device_id_step                    $dce_device_id_step                    \
            -dce_device_pri                        $dce_device_pri                        \
            -dce_ftag                              $dce_ftag                              \
            -dce_ftag_enable                       $dce_ftag_enable                       \
            -dce_local_entry_point_column          $dce_local_entry_point_column          \
            -dce_local_entry_point_row             $dce_local_entry_point_row             \
            -dce_local_link_metric                 $dce_local_link_metric                 \
            -dce_local_num_columns                 $dce_local_num_columns                 \
            -dce_local_num_rows                    $dce_local_num_rows                    \
            -dce_num_mcast_destination_trees       $dce_num_mcast_destination_trees       \
            -dce_system_id                         $dce_system_id                         \
            -dce_system_id_step                    $dce_system_id_step                    \
            ]
    if {[keylget net_config_status_$i status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget net_config_status_$i log]"
        return 0
    }
    set isis_network_handle            [keylget net_config_status_$i elem_handle]
    lappend isis_network_handle_list_1 [keylget net_config_status_$i elem_handle]
    incr i 
}

################################################################################
# Create DCE ISIS Node Mac Groups
################################################################################
# PORT 0
set cfgErrors 0
set isis_dce_node_mac_group_handle_list_0 ""
set i 1
foreach isis_router_handle $isis_router_handle_list_0 isis_network_handle $isis_network_handle_list_0 {
    set dce_include_groups                    1                                    ;# CHOICES 0 1 DEFAULT 0
    set dce_inter_grp_ucast_step              0000.000$i.0000                      ;# MAC DEFAULT 0000.0000.0000
    set dce_intra_grp_ucast_step              0000.000$i.0000                      ;# MAC DEFAULT 0000.0000.0001
    set dce_mcast_addr_count                  1                                    ;# RANGE 1-4294967295 DEFAULT 1
    set dce_mcast_addr_node_step              0000.000$i.0100                      ;# MAC DEFAULT 0000.0000.0100
    set dce_mcast_addr_step                   0000.000$i.0001                      ;# MAC DEFAULT 0000.0000.0001
    set dce_mcast_start_addr                  0100.000$i.0000                      ;# MAC DEFAULT 0100.0000.0000
    set dce_src_grp_mapping                   manual_mapping                       ;# CHOICES fully_meshed one_to_one manual_mapping DEFAULT fully_meshed
    set dce_ucast_addr_node_step              0000.000$i.0100                      ;# MAC DEFAULT 0000.0000.0100
    set dce_ucast_sources_per_mcast_addr      $i                                   ;# RANGE 0-4294967295 DEFAULT 1
    set dce_ucast_src_addr                    0000.000$i.0000                      ;# MAC DEFAULT 0000.0000.0000
    set dce_vlan_id                           $i                                   ;# RANGE 0-4095 DEFAULT 1


    set dce_group_mac_range_config_status_$i [::ixia::emulation_isis_topology_route_config \
            -mode                                  create                                  \
            -handle                                $isis_network_handle                    \
            -type                                  dce_node_mac_group                      \
            -dce_include_groups                    $dce_include_groups                     \
            -dce_inter_grp_ucast_step              $dce_inter_grp_ucast_step               \
            -dce_intra_grp_ucast_step              $dce_intra_grp_ucast_step               \
            -dce_mcast_addr_count                  $dce_mcast_addr_count                   \
            -dce_mcast_addr_node_step              $dce_mcast_addr_node_step               \
            -dce_mcast_addr_step                   $dce_mcast_addr_step                    \
            -dce_mcast_start_addr                  $dce_mcast_start_addr                   \
            -dce_src_grp_mapping                   $dce_src_grp_mapping                    \
            -dce_ucast_addr_node_step              $dce_ucast_addr_node_step               \
            -dce_ucast_sources_per_mcast_addr      $dce_ucast_sources_per_mcast_addr       \
            -dce_ucast_src_addr                    $dce_ucast_src_addr                     \
            -dce_vlan_id                           $dce_vlan_id                            \
            ]
    
    if {[keylget dce_group_mac_range_config_status_$i status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget dce_group_mac_range_config_status_$i log]"
    }
    set     dce_mac_handle                        [keylget dce_group_mac_range_config_status_$i elem_handle]
    lappend isis_dce_node_mac_group_handle_list_0 [keylget dce_group_mac_range_config_status_$i elem_handle]
    incr i
}

# PORT 1

set isis_dce_node_mac_group_handle_list_1 ""
foreach isis_router_handle $isis_router_handle_list_1 isis_network_handle $isis_network_handle_list_1 {
    set dce_include_groups                    1                                    ;# CHOICES 0 1 DEFAULT 0
    set dce_inter_grp_ucast_step              0000.000$i.0000                      ;# MAC DEFAULT 0000.0000.0000
    set dce_intra_grp_ucast_step              0000.000$i.0000                      ;# MAC DEFAULT 0000.0000.0001
    set dce_mcast_addr_count                  1                                    ;# RANGE 1-4294967295 DEFAULT 1
    set dce_mcast_addr_node_step              0000.000$i.0100                      ;# MAC DEFAULT 0000.0000.0100
    set dce_mcast_addr_step                   0000.000$i.0001                      ;# MAC DEFAULT 0000.0000.0001
    set dce_mcast_start_addr                  0100.000$i.0000                      ;# MAC DEFAULT 0100.0000.0000
    set dce_src_grp_mapping                   manual_mapping                       ;# CHOICES fully_meshed one_to_one manual_mapping DEFAULT fully_meshed
    set dce_ucast_addr_node_step              0000.000$i.0100                      ;# MAC DEFAULT 0000.0000.0100
    set dce_ucast_sources_per_mcast_addr      $i                                   ;# RANGE 0-4294967295 DEFAULT 1
    set dce_ucast_src_addr                    0000.000$i.0000                      ;# MAC DEFAULT 0000.0000.0000
    set dce_vlan_id                           $i                                   ;# RANGE 0-4095 DEFAULT 1

    set dce_group_mac_range_config_status_$i [::ixia::emulation_isis_topology_route_config \
            -mode                                  create                                  \
            -handle                                $isis_network_handle                    \
            -type                                  dce_node_mac_group                      \
            -dce_include_groups                    $dce_include_groups                     \
            -dce_inter_grp_ucast_step              $dce_inter_grp_ucast_step               \
            -dce_intra_grp_ucast_step              $dce_intra_grp_ucast_step               \
            -dce_mcast_addr_count                  $dce_mcast_addr_count                   \
            -dce_mcast_addr_node_step              $dce_mcast_addr_node_step               \
            -dce_mcast_addr_step                   $dce_mcast_addr_step                    \
            -dce_mcast_start_addr                  $dce_mcast_start_addr                   \
            -dce_src_grp_mapping                   $dce_src_grp_mapping                    \
            -dce_ucast_addr_node_step              $dce_ucast_addr_node_step               \
            -dce_ucast_sources_per_mcast_addr      $dce_ucast_sources_per_mcast_addr       \
            -dce_ucast_src_addr                    $dce_ucast_src_addr                     \
            -dce_vlan_id                           $dce_vlan_id                            \
            ]
    
    if {[keylget dce_group_mac_range_config_status_$i status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget dce_group_mac_range_config_status_$i log]"
    }
    set     dce_mac_handle                        [keylget dce_group_mac_range_config_status_$i elem_handle]
    lappend isis_dce_node_mac_group_handle_list_1 [keylget dce_group_mac_range_config_status_$i elem_handle]
    incr i
}


################################################################################
# Create DCE ISIS Node IPv4 Groups
################################################################################

# PORT 0

set isis_dce_node_ipv4_group_handle_list_0 ""
set i 1
foreach isis_router_handle $isis_router_handle_list_0 isis_network_handle $isis_network_handle_list_0 {

    set dce_include_groups                    1                                    ;# CHOICES 0 1 DEFAULT 0
    set dce_inter_grp_ucast_step              0.$i.1.0                             ;# IPV4 DEFAULT 0.0.0.0
    set dce_intra_grp_ucast_step              0.0.$i.1                             ;# IPV4 DEFAULT 0.0.0.1
    set dce_mcast_addr_count                  1                                    ;# RANGE 1-4294967295 DEFAULT 1
    set dce_mcast_addr_node_step              0.$i.2.0                             ;# IPV4 DEFAULT 0.0.1.0
    set dce_mcast_addr_step                   0.0.$i.2                             ;# IPV4 DEFAULT 0.0.0.1
    set dce_mcast_start_addr                  224.0.$i.0                           ;# IPV4 DEFAULT 224.0.0.0
    set dce_src_grp_mapping                   manual_mapping                       ;# CHOICES fully_meshed one_to_one manual_mapping DEFAULT fully_meshed
    set dce_ucast_addr_node_step              0.$i.3.0                             ;# IPV4 DEFAULT 0.0.1.0
    set dce_ucast_sources_per_mcast_addr      1                                    ;# RANGE 0-4294967295 DEFAULT 1
    set dce_ucast_src_addr                    0.0.0.$i                             ;# IPV4 DEFAULT 0.0.0.0
    set dce_vlan_id                           1                                    ;# RANGE 0-4095 DEFAULT 1


    set dce_group_ipv4_range_config_status_$i [::ixia::emulation_isis_topology_route_config \
            -mode                                  create                                  \
            -handle                                $isis_network_handle                    \
            -type                                  dce_node_ipv4_group                     \
            -dce_include_groups                    $dce_include_groups                     \
            -dce_inter_grp_ucast_step              $dce_inter_grp_ucast_step               \
            -dce_intra_grp_ucast_step              $dce_intra_grp_ucast_step               \
            -dce_mcast_addr_count                  $dce_mcast_addr_count                   \
            -dce_mcast_addr_node_step              $dce_mcast_addr_node_step               \
            -dce_mcast_addr_step                   $dce_mcast_addr_step                    \
            -dce_mcast_start_addr                  $dce_mcast_start_addr                   \
            -dce_src_grp_mapping                   $dce_src_grp_mapping                    \
            -dce_ucast_addr_node_step              $dce_ucast_addr_node_step               \
            -dce_ucast_sources_per_mcast_addr      $dce_ucast_sources_per_mcast_addr       \
            -dce_ucast_src_addr                    $dce_ucast_src_addr                     \
            -dce_vlan_id                           $dce_vlan_id                            \
            ]
    
    if {[keylget dce_group_ipv4_range_config_status_$i status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget dce_group_ipv4_range_config_status_$i log]"
    }
    set     dce_ipv4_handle                        [keylget dce_group_ipv4_range_config_status_$i elem_handle]
    lappend isis_dce_node_ipv4_group_handle_list_0 [keylget dce_group_ipv4_range_config_status_$i elem_handle]
    incr i
}

# PORT 1

set isis_dce_node_ipv4_group_handle_list_1 ""
foreach isis_router_handle $isis_router_handle_list_1 isis_network_handle $isis_network_handle_list_1 {

    set dce_include_groups                    1                                    ;# CHOICES 0 1 DEFAULT 0
    set dce_inter_grp_ucast_step              0.$i.1.0                             ;# IPV4 DEFAULT 0.0.0.0
    set dce_intra_grp_ucast_step              0.0.$i.1                             ;# IPV4 DEFAULT 0.0.0.1
    set dce_mcast_addr_count                  1                                    ;# RANGE 1-4294967295 DEFAULT 1
    set dce_mcast_addr_node_step              0.$i.2.0                             ;# IPV4 DEFAULT 0.0.1.0
    set dce_mcast_addr_step                   0.0.$i.2                             ;# IPV4 DEFAULT 0.0.0.1
    set dce_mcast_start_addr                  224.0.$i.0                           ;# IPV4 DEFAULT 224.0.0.0
    set dce_src_grp_mapping                   manual_mapping                       ;# CHOICES fully_meshed one_to_one manual_mapping DEFAULT fully_meshed
    set dce_ucast_addr_node_step              0.$i.3.0                             ;# IPV4 DEFAULT 0.0.1.0
    set dce_ucast_sources_per_mcast_addr      1                                    ;# RANGE 0-4294967295 DEFAULT 1
    set dce_ucast_src_addr                    0.0.0.$i                             ;# IPV4 DEFAULT 0.0.0.0
    set dce_vlan_id                           1                                    ;# RANGE 0-4095 DEFAULT 1


    set dce_group_ipv4_range_config_status_$i [::ixia::emulation_isis_topology_route_config \
            -mode                                  create                                  \
            -handle                                $isis_network_handle                    \
            -type                                  dce_node_ipv4_group                     \
            -dce_include_groups                    $dce_include_groups                     \
            -dce_inter_grp_ucast_step              $dce_inter_grp_ucast_step               \
            -dce_intra_grp_ucast_step              $dce_intra_grp_ucast_step               \
            -dce_mcast_addr_count                  $dce_mcast_addr_count                   \
            -dce_mcast_addr_node_step              $dce_mcast_addr_node_step               \
            -dce_mcast_addr_step                   $dce_mcast_addr_step                    \
            -dce_mcast_start_addr                  $dce_mcast_start_addr                   \
            -dce_src_grp_mapping                   $dce_src_grp_mapping                    \
            -dce_ucast_addr_node_step              $dce_ucast_addr_node_step               \
            -dce_ucast_sources_per_mcast_addr      $dce_ucast_sources_per_mcast_addr       \
            -dce_ucast_src_addr                    $dce_ucast_src_addr                     \
            -dce_vlan_id                           $dce_vlan_id                            \
            ]
    
    if {[keylget dce_group_ipv4_range_config_status_$i status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget dce_group_ipv4_range_config_status_$i log]"
    }
    set     dce_ipv4_handle                        [keylget dce_group_ipv4_range_config_status_$i elem_handle]
    lappend isis_dce_node_ipv4_group_handle_list_1 [keylget dce_group_ipv4_range_config_status_$i elem_handle]
    incr i
}


################################################################################
# Create DCE ISIS Node IPv6 Groups
################################################################################

# PORT 0

set isis_dce_node_ipv6_group_handle_list_0 ""
set i 1
foreach isis_router_handle $isis_router_handle_list_0 isis_network_handle $isis_network_handle_list_0 {

    set dce_include_groups                    1                                    ;# CHOICES 0 1 DEFAULT 0
    set dce_inter_grp_ucast_step              0::$i:0                              ;# IPV6 DEFAULT 0::0
    set dce_intra_grp_ucast_step              0::$i:1                              ;# IPV6 DEFAULT 0::1
    set dce_mcast_addr_count                  1                                    ;# RANGE 1-4294967295 DEFAULT 1
    set dce_mcast_addr_node_step              0::$i:10                             ;# IPV6 DEFAULT 0::10
    set dce_mcast_addr_step                   0::$i:2                              ;# IPV6 DEFAULT 0::1
    set dce_mcast_start_addr                  FF03:0::$i:0                         ;# IPV6 DEFAULT FF03:0::0
    set dce_src_grp_mapping                   manual_mapping                       ;# CHOICES fully_meshed one_to_one manual_mapping DEFAULT fully_meshed
    set dce_ucast_addr_node_step              0::$i:20                             ;# IPV6 DEFAULT 0::10
    set dce_ucast_sources_per_mcast_addr      1                                    ;# RANGE 0-4294967295 DEFAULT 1
    set dce_ucast_src_addr                    0::$i:3                              ;# IPV6 DEFAULT 0::0
    set dce_vlan_id                           1                                    ;# RANGE 0-4095 DEFAULT 1


    set dce_group_ipv6_range_config_status_$i [::ixia::emulation_isis_topology_route_config \
            -mode                                  create                                  \
            -handle                                $isis_network_handle                    \
            -type                                  dce_node_ipv6_group                     \
            -dce_include_groups                    $dce_include_groups                     \
            -dce_inter_grp_ucast_step              $dce_inter_grp_ucast_step               \
            -dce_intra_grp_ucast_step              $dce_intra_grp_ucast_step               \
            -dce_mcast_addr_count                  $dce_mcast_addr_count                   \
            -dce_mcast_addr_node_step              $dce_mcast_addr_node_step               \
            -dce_mcast_addr_step                   $dce_mcast_addr_step                    \
            -dce_mcast_start_addr                  $dce_mcast_start_addr                   \
            -dce_src_grp_mapping                   $dce_src_grp_mapping                    \
            -dce_ucast_addr_node_step              $dce_ucast_addr_node_step               \
            -dce_ucast_sources_per_mcast_addr      $dce_ucast_sources_per_mcast_addr       \
            -dce_ucast_src_addr                    $dce_ucast_src_addr                     \
            -dce_vlan_id                           $dce_vlan_id                            \
            ]
    
    if {[keylget dce_group_ipv6_range_config_status_$i status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget dce_group_ipv6_range_config_status_$i log]"
    }
    set     dce_ipv6_handle                        [keylget dce_group_ipv6_range_config_status_$i elem_handle]
    lappend isis_dce_node_ipv6_group_handle_list_0 [keylget dce_group_ipv6_range_config_status_$i elem_handle]
    incr i
}


# PORT 1

set isis_dce_node_ipv6_group_handle_list_1 ""
foreach isis_router_handle $isis_router_handle_list_1 isis_network_handle $isis_network_handle_list_1 {

    set dce_include_groups                    1                                    ;# CHOICES 0 1 DEFAULT 0
    set dce_inter_grp_ucast_step              0::$i:0                              ;# IPV6 DEFAULT 0::0
    set dce_intra_grp_ucast_step              0::$i:1                              ;# IPV6 DEFAULT 0::1
    set dce_mcast_addr_count                  1                                    ;# RANGE 1-4294967295 DEFAULT 1
    set dce_mcast_addr_node_step              0::$i:10                             ;# IPV6 DEFAULT 0::10
    set dce_mcast_addr_step                   0::$i:2                              ;# IPV6 DEFAULT 0::1
    set dce_mcast_start_addr                  FF03:0::$i:0                         ;# IPV6 DEFAULT FF03:0::0
    set dce_src_grp_mapping                   manual_mapping                       ;# CHOICES fully_meshed one_to_one manual_mapping DEFAULT fully_meshed
    set dce_ucast_addr_node_step              0::$i:20                             ;# IPV6 DEFAULT 0::10
    set dce_ucast_sources_per_mcast_addr      1                                    ;# RANGE 0-4294967295 DEFAULT 1
    set dce_ucast_src_addr                    0::$i:3                              ;# IPV6 DEFAULT 0::0
    set dce_vlan_id                           1                                    ;# RANGE 0-4095 DEFAULT 1


    set dce_group_ipv6_range_config_status_$i [::ixia::emulation_isis_topology_route_config \
            -mode                                  create                                  \
            -handle                                $isis_network_handle                    \
            -type                                  dce_node_ipv6_group                     \
            -dce_include_groups                    $dce_include_groups                     \
            -dce_inter_grp_ucast_step              $dce_inter_grp_ucast_step               \
            -dce_intra_grp_ucast_step              $dce_intra_grp_ucast_step               \
            -dce_mcast_addr_count                  $dce_mcast_addr_count                   \
            -dce_mcast_addr_node_step              $dce_mcast_addr_node_step               \
            -dce_mcast_addr_step                   $dce_mcast_addr_step                    \
            -dce_mcast_start_addr                  $dce_mcast_start_addr                   \
            -dce_src_grp_mapping                   $dce_src_grp_mapping                    \
            -dce_ucast_addr_node_step              $dce_ucast_addr_node_step               \
            -dce_ucast_sources_per_mcast_addr      $dce_ucast_sources_per_mcast_addr       \
            -dce_ucast_src_addr                    $dce_ucast_src_addr                     \
            -dce_vlan_id                           $dce_vlan_id                            \
            ]
    
    if {[keylget dce_group_ipv6_range_config_status_$i status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget dce_group_ipv6_range_config_status_$i log]"
    }
    set     dce_ipv6_handle                        [keylget dce_group_ipv6_range_config_status_$i elem_handle]
    lappend isis_dce_node_ipv6_group_handle_list_1 [keylget dce_group_ipv6_range_config_status_$i elem_handle]
    incr i
}


################################################################################
# Create DCE ISIS Outside Link
################################################################################

# PORT 0

set isis_dce_outside_link_handle_list_0 ""
set i 1
foreach isis_router_handle $isis_router_handle_list_0 isis_network_handle $isis_network_handle_list_0 {

    set dce_connection_column                 2                                    ;# RANGE 1-100000 DEFAULT 1
    set dce_connection_row                    2                                    ;# RANGE 1-100000 DEFAULT 1
    set dce_linked_router_id                  00.00.00.00.0$i.00                   ;# HEX DEFAULT 00.00.00.00.00.00

    set dce_outside_link_config_status_$i [::ixia::emulation_isis_topology_route_config    \
            -mode                                  create                                  \
            -handle                                $isis_network_handle                    \
            -type                                  dce_outside_link                        \
            -dce_connection_column                 $dce_connection_column                  \
            -dce_connection_row                    $dce_connection_row                     \
            -dce_linked_router_id                  $dce_linked_router_id                   \
            ]
    
    if {[keylget dce_outside_link_config_status_$i status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget dce_outside_link_config_status_$i log]"
    }
    set     dce_outside_link_handle             [keylget dce_outside_link_config_status_$i elem_handle]
    lappend isis_dce_outside_link_handle_list_0 [keylget dce_outside_link_config_status_$i elem_handle]
    incr i
}

# PORT 1

set isis_dce_outside_link_handle_list_1 ""
foreach isis_router_handle $isis_router_handle_list_1 isis_network_handle $isis_network_handle_list_1 {

    set dce_connection_column                 $i                                   ;# RANGE 1-100000 DEFAULT 1
    set dce_connection_row                    $i                                   ;# RANGE 1-100000 DEFAULT 1
    set dce_linked_router_id                  00.00.00.00.0$i.00                   ;# HEX DEFAULT 00.00.00.00.00.00

    set dce_outside_link_config_status_$i [::ixia::emulation_isis_topology_route_config    \
            -mode                                  create                                  \
            -handle                                $isis_network_handle                    \
            -type                                  dce_outside_link                        \
            -dce_connection_column                 $dce_connection_column                  \
            -dce_connection_row                    $dce_connection_row                     \
            -dce_linked_router_id                  $dce_linked_router_id                   \
            ]
    
    if {[keylget dce_outside_link_config_status_$i status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget dce_outside_link_config_status_$i log]"
    }
    set     dce_outside_link_handle             [keylget dce_outside_link_config_status_$i elem_handle]
    lappend isis_dce_outside_link_handle_list_1 [keylget dce_outside_link_config_status_$i elem_handle]
    incr i
}

################################################################################
# Start protocol
################################################################################
set isis_info_handle_0 [::ixia::emulation_isis_control                         \
        -mode                               start                              \
        -port_handle                        [list $port_0 $port_1 ]            \
        ]

if {[keylget isis_info_handle_0 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_info_handle_0 log]"
}

# wait 30sec to start the protocol and learn stats
after 30000

##############################################
#SHOW STATS PROCEDURE - printing statistics  #
##############################################

proc show_stats var {
    set level [expr [info level] - 1]
    foreach key [keylkeys var] {
	if {$key == "status"} {continue}
	set indent [string repeat "    " $level] 
	puts -nonewline $indent 
	if {[catch {keylkeys var $key}]} {
	    puts "$key: [keylget var $key]"
	    continue
	} else {
	    puts $key
	    puts "$indent[string repeat "-" [string length $key]]"
	}
	show_stats [keylget var $key]
    }
}

################################################################################
# Retrieve protocol stats 
################################################################################
set isis_stats_0 [::ixia::emulation_isis_info                                  \
        -mode                               stats                              \
        -port_handle                        $port_0                            \
        ]

if {[keylget isis_stats_0 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_stats_0 log]"
}
puts "isis_stats_0 stats: -----------------------------------"
show_stats $isis_stats_0

set isis_stats_1 [::ixia::emulation_isis_info                                  \
        -mode                               stats                              \
        -port_handle                        $port_1                            \
        ]

if {[keylget isis_stats_1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_stats_1 log]"
}
puts "isis_stats_1 stats: -----------------------------------"
show_stats $isis_stats_1


puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
