################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Enache Adrian $
#
#    Copyright © 1997 - 2011 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#
# Description:
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
###############################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample configures 1 port and an OSPF-TE configuration on it          #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10/100/1000 STX4-256MB module.                 #
#                                                                              #
################################################################################

set env(IXIA_VERSION) HLTSET105
package require Ixia

#set ixia::debug 3
set test_name [info script]

set chassisIP sylvester
set port_list {2/3 2/4}

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                 \
        -reset                                      \
        -device                 $chassisIP          \
        -port_list              $port_list          \
        -username               ixiaApiUser         \
        -ixnetwork_tcl_server   localhost           \
        -tcl_server             $chassisIP          ]
        
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle1 [keylget connect_status port_handle.$chassisIP.[lindex $port_list 0]]
set port_handle2 [keylget connect_status port_handle.$chassisIP.[lindex $port_list 1]]

########################################
# Configure interfaces in the test     #
########################################
set interface_status [::ixia::interface_config \
        -mode config                         \
        -port_handle     $port_handle1       \
        -autonegotiation 1                   \
        -duplex          full                \
        -speed           ether1000           ]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

##################################
# Configure OSPFv2 neighbor      #
##################################

set ospf_neighbor_status [::ixia::emulation_ospf_config \
        -port_handle                $port_handle1    \
        -reset                                       \
        -session_type               ospfv2           \
        -mode                       create           \
        -count                      1                \
        -intf_ip_addr               100.1.1.1        \
        -neighbor_intf_ip_addr      100.1.1.2        \
        ]

if {[keylget ospf_neighbor_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ospf_neighbor_status log]"
}

# Extract the OSPF router handle
set ospf_router_handle [keylget ospf_neighbor_status handle]

#################################
# ospf - SETTINGS               #
#################################
set area_id                             1.0.0.0                ;# IP DEFAULT 0.0.0.0
set bfd_registration                    1                      ;# CHOICES 0 1 DEFAULT 0
set dead_interval                       40                     ;# RANGE 0-65535 DEFAULT 40
set enable_advertise                    1                      ;# CHOICES 0 1
set enable_advertise_loopback           1                      ;# CHOICES 0 1 DEFAULT 0
set external_number_of_prefix           1                      ;# RANGE 1-16000000
set external_prefix_length              24                     ;# RANGE 0-128 DEFAULT 24 | 64
set external_prefix_metric              1                      ;# RANGE 0-16777215
set external_prefix_start               2.0.0.0                ;# IP DEFAULT 0.0.0.0 | 0::0
set external_prefix_step                1                      ;# RANGE 0-2147483647 DEFAULT 1 | IP
set external_prefix_type                1                      ;# CHOICES 1 2
set grid_col                            2                      ;# RANGE 0-10000
set grid_connect                        {2 2}                  ;# NUMERIC
set grid_link_type                      ptop_unnumbered         ;# CHOICES broadcast ptop_unnumbered ptop_numbered DEFAULT ptop_numbered
set grid_prefix_length                  24                     ;# RANGE 0-128 DEFAULT 24 | 64
set grid_prefix_start                   3.0.0.0                ;# IP DEFAULT 0.0.0.0 | 0::0
set grid_prefix_step                    0.0.0.1                ;# IP DEFAULT 0.0.0.1 | 0::1
set grid_router_id                      4.0.0.0                ;# IP
set grid_router_id_step                 0.0.0.2                ;# IP
set grid_row                            3                      ;# RANGE 0-10000
set grid_te                             1                      ;# CHOICES 0 1
set handle                              $ospf_router_handle    ;# ANY
set hello_interval                      10                     ;# RANGE 0-65535 DEFAULT 10
set interface_ip_address                5.0.0.1                ;# IP
set interface_ip_mask                   255.255.0.0            ;# IP
set interface_metric                    20                     ;# RANGE 0-65535 DEFAULT 10
set interface_ip_options                22                     ;#
set link_te                             1                      ;# CHOICES 0 1 DEFAULT 0
set link_te_metric                      30                     ;# RANGE 0-65535 DEFAULT 10
set link_te_max_bw                      11.0                   ;# DECIMAL DEFAULT 0
set link_te_max_resv_bw                 25.0                   ;# DECIMAL DEFAULT 0
set link_te_unresv_bw_priority0         36.0                   ;# DECIMAL DEFAULT 0
set link_te_unresv_bw_priority1         49.0                   ;# DECIMAL DEFAULT 0
set link_te_unresv_bw_priority2         50.0                   ;# DECIMAL DEFAULT 0
set link_te_unresv_bw_priority3         6.24                   ;# DECIMAL DEFAULT 0
set link_te_unresv_bw_priority4         70.0                   ;# DECIMAL DEFAULT 0
set link_te_unresv_bw_priority5         80.0                   ;# DECIMAL DEFAULT 0
set link_te_unresv_bw_priority6         90.0                   ;# DECIMAL DEFAULT 0
set link_te_unresv_bw_priority7         100.0                  ;# DECIMAL DEFAULT 0
set link_type                           ppp                    ;# CHOICES external-capable ppp stub
set mode                                create                 ;# CHOICES create modify delete
set neighbor_router_id                  6.0.0.1                ;# IPV4
set neighbor_router_prefix_length       16                     ;# RANGE 0-32
set net_ip                              6.1.0.1                ;# IP
set net_prefix_length                   24                     ;# RANGE 1-128 DEFAULT 24 | 64
set router_abr                          1                      ;# CHOICES 0 1
set router_asbr                         1                      ;# CHOICES 0 1
set router_id                           7.0.0.1                ;# IP DEFAULT 0.0.0.0
set router_te                           1                      ;# CHOICES 0 1
set router_virtual_link_endpt           1                      ;# CHOICES 0 1
set router_wcr                          1                      ;# CHOICES 0 1
set summary_number_of_prefix            1                      ;# RANGE 1-16000000
set summary_prefix_length               24                     ;# RANGE 0-128 DEFAULT 24 | 64
set summary_prefix_metric               20                     ;# RANGE 0-16777215
set summary_prefix_start                8.0.0.0                ;# IP DEFAULT 0.0.0.0 | 0::0
set summary_prefix_step                 0.0.0.3                ;# RANGE 0-2147483647 DEFAULT 1 | IP
set type                                grid                   ;# CHOICES router grid network summary_routes ext_routes

################################################################################
# Start ospf Call
################################################################################
set ospf_config_status [::ixia::emulation_ospf_topology_route_config              \
        -area_id                             $area_id                             \
        -bfd_registration                    $bfd_registration                    \
        -dead_interval                       $dead_interval                       \
        -enable_advertise                    $enable_advertise                    \
        -enable_advertise_loopback           $enable_advertise_loopback           \
        -external_number_of_prefix           $external_number_of_prefix           \
        -external_prefix_length              $external_prefix_length              \
        -external_prefix_metric              $external_prefix_metric              \
        -external_prefix_start               $external_prefix_start               \
        -external_prefix_step                $external_prefix_step                \
        -external_prefix_type                $external_prefix_type                \
        -grid_col                            $grid_col                            \
        -grid_link_type                      $grid_link_type                      \
        -grid_prefix_length                  $grid_prefix_length                  \
        -grid_prefix_start                   $grid_prefix_start                   \
        -grid_prefix_step                    $grid_prefix_step                    \
        -grid_router_id                      $grid_router_id                      \
        -grid_router_id_step                 $grid_router_id_step                 \
        -grid_row                            $grid_row                            \
        -grid_te                             $grid_te                             \
        -handle                              $handle                              \
        -hello_interval                      $hello_interval                      \
        -interface_ip_address                $interface_ip_address                \
        -interface_ip_mask                   $interface_ip_mask                   \
        -interface_ip_options                $interface_ip_options                \
        -interface_metric                    $interface_metric                    \
        -link_te                             $link_te                             \
        -link_te_metric                      $link_te_metric                      \
        -link_te_max_bw                      $link_te_max_bw                      \
        -link_te_max_resv_bw                 $link_te_max_resv_bw                 \
        -link_te_unresv_bw_priority0         $link_te_unresv_bw_priority0         \
        -link_te_unresv_bw_priority1         $link_te_unresv_bw_priority1         \
        -link_te_unresv_bw_priority2         $link_te_unresv_bw_priority2         \
        -link_te_unresv_bw_priority3         $link_te_unresv_bw_priority3         \
        -link_te_unresv_bw_priority4         $link_te_unresv_bw_priority4         \
        -link_te_unresv_bw_priority5         $link_te_unresv_bw_priority5         \
        -link_te_unresv_bw_priority6         $link_te_unresv_bw_priority6         \
        -link_te_unresv_bw_priority7         $link_te_unresv_bw_priority7         \
        -link_type                           $link_type                           \
        -mode                                $mode                                \
        -neighbor_router_id                  $neighbor_router_id                  \
        -neighbor_router_prefix_length       $neighbor_router_prefix_length       \
        -net_ip                              $net_ip                              \
        -net_prefix_length                   $net_prefix_length                   \
        -router_abr                          $router_abr                          \
        -router_asbr                         $router_asbr                         \
        -router_id                           $router_id                           \
        -router_te                           $router_te                           \
        -router_virtual_link_endpt           $router_virtual_link_endpt           \
        -router_wcr                          $router_wcr                          \
        -summary_number_of_prefix            $summary_number_of_prefix            \
        -summary_prefix_length               $summary_prefix_length               \
        -summary_prefix_metric               $summary_prefix_metric               \
        -summary_prefix_start                $summary_prefix_start                \
        -summary_prefix_step                 $summary_prefix_step                 \
        -type                                $type                                ]

if {[keylget ospf_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospf_config_status log]"
    return
}
set ospf_route_handles [keylget ospf_config_status elem_handle]

puts "Ixia ospf handles are: "
foreach ospf_handle $ospf_route_handles {
    puts $ospf_handle
}

puts "SUCCESS - [info script] - [clock format [clock seconds]]"
return 1