################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LBose $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-27-2013 LBose - Initial Version
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
#    This sample script creates the ISIS outside link with IPv4 Addresses      #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#                                                                              #
################################################################################

package require Ixia

################################################################################
# General script variables
################################################################################
set test_name           [info script]
set port_names          [list test_port_1 test_port_2]

################################################################################
# START - Connect to the chassis                                               #
################################################################################
puts "Start connecting to chassis .. - $test_name - [clock format [clock seconds]]"
set chassis_ip              10.206.27.55
set port_list               [list 10/1 10/2]
set break_locks             1
set tcl_server              10.206.27.55
set ixnetwork_tcl_server    192.168.4.6

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                         \
        -reset                                                              \
        -device               $chassis_ip                                   \
        -port_list            $port_list                                    \
        -break_locks          $break_locks                                  \
        -tcl_server           $tcl_server                                   \
        -ixnetwork_tcl_server $ixnetwork_tcl_server                         \
        -interactive          1                                             \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port}      \
                temp_port]} {
        lappend port_handle $temp_port
    }
}

set i 0
puts "Ixia port handles are:"
foreach port $port_handle {
    set port_$i $port
    puts $port    
    incr i
}

set vport_info_status   [::ixia::vport_info     \
        -mode               set_info            \
        -port_list          $port_handle        \
        -port_name_list     $port_names         ]
    
if {[keylget vport_info_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget vport_info_status log]"
}
puts "End connecting to chassis ..."

################################################################################
# END - Connect to the chassis                                                 #
################################################################################


################################################################################
# START - Interface configuration - L1                                         #
################################################################################
puts "Start interface configuration L1 ..."
##########################################
# Configure interface in the test (IPv4) #
##########################################
set interface_status [ixia::interface_config    \
        -port_handle     $port_handle           \
        -autonegotiation 1                      \
        -speed           auto                   \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}

################################################################################
#                    Configure the first IS-IS L1L2 router                     #
################################################################################
puts "Configuring ISIS on Port0.."
set isis_router_status [ixia::emulation_isis_config     \
        -mode                           create          \
        -reset                                          \
        -port_handle                    $port_0         \
        -intf_ip_addr                   22.1.1.2        \
        -gateway_ip_addr                22.1.1.1        \
        -intf_ip_prefix_length          24              \
        -mac_address_init               0000.0000.0001  \
        -count                          1               \
        -wide_metrics                   1               \
        -discard_lsp                    1               \
        -attach_bit                     1               \
        -partition_repair               1               \
        -overloaded                     1               \
        -lsp_refresh_interval           888             \
        -lsp_life_time                  777             \
        -max_packet_size                1492            \
        -intf_metric                    0               \
        -routing_level                  L1L2            \
        ]
if {[keylget isis_router_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_router_status log]"
    return 0
}

set router_handle1 [keylget isis_router_status handle]

################################################################################
#           Add a Grid Network Ranges for the first IS-IS router               #
################################################################################
set ip_version                          4
set grid_start_system_id                000000000011
set grid_system_id_step                 000000000001
set grid_row                            1
set grid_col                            1
set grid_stub_per_router                10
set grid_router_id                      192.168.1.1
set grid_router_id_step                 0.1.0.0
set grid_ip_start                       192.20.20.1
set grid_ip_pfx_len                     24
set grid_ip_step                        0.0.1.0
set grid_connect                        "1 1"
set grid_link_type                      ptop
set grid_router_metric                  10
set grid_router_up_down_bit             0
set grid_router_origin                  external
set grid_user_wide_metric               0
set grid_ol_ip_and_prefix               list [10.0.0.1/24,10.0.0.2/24 \
                                            11.0.0.1/24,11.0.0.2/24]
set grid_ol_connection_row              {1 1}
set grid_ol_connection_col              {1 1}
set grid_ol_linked_rid                  [list 1 2]
set grid_ol_metric                      [list 1 2]
set grid_ol_admin_group                 [list 1 2]
set grid_ol_max_bw                      [list 10 11]
set grid_ol_max_resv_bw                 [list 12 13]
set grid_ol_unresv_bw_priority0         [list 14 15]
set grid_ol_unresv_bw_priority1         [list 16 17]
set grid_ol_unresv_bw_priority2         [list 18 19]
set grid_ol_unresv_bw_priority3         [list 20 21]
set grid_ol_unresv_bw_priority4         [list 22 23]
set grid_ol_unresv_bw_priority5         [list 24 25]
set grid_ol_unresv_bw_priority6         [list 26 27]
set grid_ol_unresv_bw_priority7         [list 28 29]
set isis_router_networkRange_handle_list    ""

set route_config_status_0 [ixia::emulation_isis_topology_route_config       \
        -mode                           create                              \
        -handle                         $router_handle1                     \
        -type                           grid                                \
        -ip_version                     $ip_version                         \
        -grid_outside_link              1                                   \
        -grid_ol_connection_row         $grid_ol_connection_row             \
        -grid_ol_connection_col         $grid_ol_connection_col             \
        -grid_ol_linked_rid             $grid_ol_linked_rid                 \
        -grid_ol_admin_group            $grid_ol_admin_group                \
        -grid_ol_ip_and_prefix          $grid_ol_ip_and_prefix              \
        -grid_ol_metric                 $grid_ol_metric                     \
        -grid_ol_max_bw                 $grid_ol_max_bw                     \
        -grid_ol_max_resv_bw            $grid_ol_max_resv_bw                \
        -grid_ol_unresv_bw_priority0    $grid_ol_unresv_bw_priority0        \
        -grid_ol_unresv_bw_priority1    $grid_ol_unresv_bw_priority1        \
        -grid_ol_unresv_bw_priority2    $grid_ol_unresv_bw_priority2        \
        -grid_ol_unresv_bw_priority3    $grid_ol_unresv_bw_priority3        \
        -grid_ol_unresv_bw_priority4    $grid_ol_unresv_bw_priority4        \
        -grid_ol_unresv_bw_priority5    $grid_ol_unresv_bw_priority5        \
        -grid_ol_unresv_bw_priority6    $grid_ol_unresv_bw_priority6        \
        -grid_ol_unresv_bw_priority7    $grid_ol_unresv_bw_priority7        \
        -grid_start_system_id           $grid_start_system_id               \
        -grid_system_id_step            $grid_system_id_step                \
        -grid_row                       $grid_row                           \
        -grid_col                       $grid_col                           \
        -grid_stub_per_router           $grid_stub_per_router               \
        -grid_router_id                 $grid_router_id                     \
        -grid_router_id_step            $grid_router_id_step                \
        -grid_ip_start                  $grid_ip_start                      \
        -grid_ip_pfx_len                $grid_ip_pfx_len                    \
        -grid_ip_step                   $grid_ip_step                       \
        -grid_connect                   $grid_connect                       \
        -grid_link_type                 $grid_link_type                     \
        -grid_router_metric             $grid_router_metric                 \
        -grid_router_up_down_bit        $grid_router_up_down_bit            \
        -grid_router_origin             $grid_router_origin                 \
        -grid_user_wide_metric          $grid_user_wide_metric              ]

    if {[keylget route_config_status_0 status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget route_config_status_0 log]"
        return 0
    }

################################################################################
#                   Configure the second IS-IS L1L2 router                     #
################################################################################
puts "Configuring ISIS on Port1.."
set isis_router_status [ixia::emulation_isis_config     \
        -mode                           create          \
        -reset                                          \
        -port_handle                    $port_1         \
        -intf_ip_addr                   22.1.1.1        \
        -gateway_ip_addr                22.1.1.2        \
        -intf_ip_prefix_length          24              \
        -mac_address_init               0000.0000.0002  \
        -count                          1               \
        -wide_metrics                   1               \
        -discard_lsp                    1               \
        -attach_bit                     1               \
        -partition_repair               1               \
        -overloaded                     1               \
        -lsp_refresh_interval           888             \
        -lsp_life_time                  777             \
        -max_packet_size                1492            \
        -intf_metric                    0               \
        -routing_level                  L1L2            \
        ]
if {[keylget isis_router_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_router_status log]"
    return 0
}

set router_handle2 [keylget isis_router_status handle]

################################################################################
#           Add a Grid Network Ranges for the second IS-IS router              #
################################################################################

set ip_version                     4
set grid_start_system_id           0000000011
set grid_system_id_step            000000000001
set grid_row                       2
set grid_col                       2
set grid_stub_per_router           10
set grid_router_id                 193.168.1.1
set grid_router_id_step            0.1.0.0
set grid_ip_start                  193.20.20.1
set grid_ip_pfx_len                24
set grid_ip_step                   0.0.1.0
set grid_connect                   "2 2"
set grid_link_type                 ptop
set grid_router_metric             10
set grid_router_up_down_bit        0
set grid_router_origin             external
set grid_user_wide_metric          0
set grid_ol_ip_and_prefix          [list 12.0.0.1/24,12.0.0.2/24 \
                                         13.0.0.1/24,13.0.0.2/24]
set grid_ol_connection_row         {1 1}
set grid_ol_connection_col         {1 1}
set grid_ol_linked_rid             [list 255 256]
set grid_ol_metric                 [list 355 356]
set grid_ol_admin_group            [list 455 456]
set grid_ol_max_bw                 [list 555 556]
set grid_ol_max_resv_bw            [list 655 656]
set grid_ol_unresv_bw_priority0    [list 755 756]
set grid_ol_unresv_bw_priority1    [list 855 856]
set grid_ol_unresv_bw_priority2    [list 955 956]
set grid_ol_unresv_bw_priority3    [list 1055 1056]
set grid_ol_unresv_bw_priority4    [list 1165 1156]
set grid_ol_unresv_bw_priority5    [list 1175 1176]
set grid_ol_unresv_bw_priority6    [list 1185 1186]
set grid_ol_unresv_bw_priority7    [list 1195 1196]
set isis_router_networkRange_handle_list ""

set route_config_status_1 [ixia::emulation_isis_topology_route_config       \
        -mode                           create                              \
        -handle                         $router_handle2                     \
        -type                           grid                                \
        -ip_version                     $ip_version                         \
        -grid_outside_link              1                                   \
        -grid_ol_connection_row         $grid_ol_connection_row             \
        -grid_ol_connection_col         $grid_ol_connection_col             \
        -grid_ol_linked_rid             $grid_ol_linked_rid                 \
        -grid_ol_admin_group            $grid_ol_admin_group                \
        -grid_ol_ip_and_prefix          $grid_ol_ip_and_prefix              \
        -grid_ol_metric                 $grid_ol_metric                     \
        -grid_ol_max_bw                 $grid_ol_max_bw                     \
        -grid_ol_max_resv_bw            $grid_ol_max_resv_bw                \
        -grid_ol_unresv_bw_priority0    $grid_ol_unresv_bw_priority0        \
        -grid_ol_unresv_bw_priority1    $grid_ol_unresv_bw_priority1        \
        -grid_ol_unresv_bw_priority2    $grid_ol_unresv_bw_priority2        \
        -grid_ol_unresv_bw_priority3    $grid_ol_unresv_bw_priority3        \
        -grid_ol_unresv_bw_priority4    $grid_ol_unresv_bw_priority4        \
        -grid_ol_unresv_bw_priority5    $grid_ol_unresv_bw_priority5        \
        -grid_ol_unresv_bw_priority6    $grid_ol_unresv_bw_priority6        \
        -grid_ol_unresv_bw_priority7    $grid_ol_unresv_bw_priority7        \
        -grid_start_system_id           $grid_start_system_id               \
        -grid_system_id_step            $grid_system_id_step                \
        -grid_row                       $grid_row                           \
        -grid_col                       $grid_col                           \
        -grid_stub_per_router           $grid_stub_per_router               \
        -grid_router_id                 $grid_router_id                     \
        -grid_router_id_step            $grid_router_id_step                \
        -grid_ip_start                  $grid_ip_start                      \
        -grid_ip_pfx_len                $grid_ip_pfx_len                    \
        -grid_ip_step                   $grid_ip_step                       \
        -grid_connect                   $grid_connect                       \
        -grid_link_type                 $grid_link_type                     \
        -grid_router_metric             $grid_router_metric                 \
        -grid_router_up_down_bit        $grid_router_up_down_bit            \
        -grid_router_origin             $grid_router_origin                 \
        -grid_user_wide_metric          $grid_user_wide_metric              ]

    if {[keylget route_config_status_1 status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget route_config_status_1 log]"
        return 0
    }

################################################################################
#                           Start the IS-IS protocol emulation                 #
################################################################################
set isis_emulation_status [ixia::emulation_isis_control         \
        -port_handle    $port_0                                 \
        -mode           start                                   ]
if {[keylget isis_emulation_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_emulation_status log]"
    return 0
}

set isis_emulation_status [ixia::emulation_isis_control         \
        -port_handle $port_1                                    \
        -mode        start                                      ]
if {[keylget isis_emulation_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_emulation_status log]"
    return 0
}
after 10000
puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1