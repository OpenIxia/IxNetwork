
################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LBose $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-17-2013 LBose - Initial Version
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
#    This sample configures two ports in IxNetwork, configures a traffic item  #
#    and modify the traffic item for repeatable and non-repeatable random macs.#
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

# Declare the Chassis IP address and the Ports that will be used
set chassis_ip 10.206.27.55
set tcl_server 10.206.27.55
set port_list {10/1 10/2}
set ixnetwork_tcl_server 10.206.26.196

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                     \
        -reset                  1                       \
        -device                 $chassis_ip             \
        -port_list              $port_list              \
        -ixnetwork_tcl_server   $ixnetwork_tcl_server   \
        -tcl_server             $tcl_server             \
    ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
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
puts "End connecting to chassis ..."
update idletasks

puts "Configure interfaces ..."

################################################################################
# Configure Protocol Interfaces on both ports                                  #
################################################################################
set interface_status [::ixia::interface_config  \
    -mode                   config              \
    -port_handle            $port_0             \
    -tx_gap_control_mode    average             \
    -transmit_mode          advanced            \
    -port_rx_mode           packet_group        \
    -data_integrity         1                   \
    -intf_mode              ethernet            \
    -speed                  ether1000           \
    -duplex                 full                \
    -autonegotiation        1                   \
    -phy_mode               copper              \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set interface_status [::ixia::interface_config  \
    -mode                   config              \
    -port_handle            $port_1             \
    -tx_gap_control_mode    average             \
    -transmit_mode          advanced            \
    -port_rx_mode           packet_group        \
    -data_integrity         1                   \
    -intf_mode              ethernet            \
    -speed                  ether1000           \
    -duplex                 full                \
    -autonegotiation        1                   \
    -phy_mode               copper              \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Configure Traffic on ports                                                   #
################################################################################

puts "Reset traffic ..."
set traffic_reset [::ixia::traffic_control          \
    -action                      reset              \
    -traffic_generator           ixnetwork_540      \
    -latency_bins                enabled            \
    -latency_control             store_and_forward  \
]
if {[keylget traffic_reset status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_reset log]"
}

puts "Configure traffic ..."
set traffic_status [::ixia::traffic_config                      \
    -mode                                       create          \
    -traffic_generator                          ixnetwork_540   \
    -endpointset_count                          1               \
    -emulation_src_handle                       $port_0         \
    -emulation_dst_handle                       $port_1         \
    -global_dest_mac_retry_count                1               \
    -global_dest_mac_retry_delay                5               \
    -enable_data_integrity                      1               \
    -global_enable_dest_mac_retry               1               \
    -global_enable_min_frame_size               0               \
    -global_enable_staggered_transmit           0               \
    -global_enable_stream_ordering              0               \
    -global_stream_control                      continuous      \
    -global_stream_control_iterations           1               \
    -global_large_error_threshhold              2               \
    -global_enable_mac_change_on_fly            0               \
    -global_max_traffic_generation_queries      500             \
    -global_mpls_label_learning_timeout         30              \
    -global_refresh_learned_info_before_apply   0               \
    -global_use_tx_rx_sync                      1               \
    -global_wait_time                           1               \
    -global_display_mpls_current_label_value    0               \
    -frame_sequencing                           disable         \
    -frame_sequencing_mode                      rx_threshold    \
    -src_dest_mesh                              one_to_one      \
    -route_mesh                                 one_to_one      \
    -bidirectional                              0               \
    -allow_self_destined                        0               \
    -enable_dynamic_mpls_labels                 0               \
    -hosts_per_net                              1               \
    -name                                       Traffic_Item_1  \
    -source_filter                              all             \
    -destination_filter                         all             \
    -merge_destinations                         0               \
    -circuit_type                               raw             \
    -pending_operations_timeout                 30              \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

set current_config_element [keylget traffic_status traffic_item]
set eth_stack [lindex [keylget traffic_status $current_config_element.headers] 0]

return

set traffic_status [::ixia::traffic_config                      \
    -mode                               modify                  \
    -traffic_generator                  ixnetwork_540           \
    -stream_id                          $current_config_element \
    -preamble_size_mode                 auto                    \
    -preamble_custom_size               8                       \
    -data_pattern                       {}                      \
    -data_pattern_mode                  incr_byte               \
    -enforce_min_gap                    0                       \
    -rate_percent                       10                      \
    -frame_rate_distribution_port       apply_to_all            \
    -frame_rate_distribution_stream     split_evenly            \
    -frame_size                         64                      \
    -length_mode                        fixed                   \
    -tx_mode                            advanced                \
    -transmit_mode                      continuous              \
    -pkts_per_burst                     1                       \
    -tx_delay                           0                       \
    -tx_delay_unit                      bytes                   \
    -number_of_packets_per_stream       1                       \
    -loop_count                         1                       \
    -min_gap_bytes                      12                      \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

set dst_seed_hlt  7
set dst_bits_hlt  00:00:00:00:00:40
set dst_mask_hlt  ff:ff:ff:ff:ff:35
set dst_count_hlt 8
set src_seed_hlt  5
set src_bits_hlt  00:00:00:00:00:10
set src_mask_hlt  ff:ff:ff:ff:ff:25
set src_count_hlt 6
puts "Set repeatable random mac ..."
################################################################################
# Configure Traffic Item with repeatbale random mac                            #
################################################################################
set mac_cfg_config [::ixia::traffic_config      \
    -mode               modify                  \
    -traffic_generator  ixnetwork_540           \
    -stream_id          $eth_stack              \
    -l2_encap           ethernet_ii             \
    -mac_dst_mode       repeatable_random       \
    -mac_dst            $dst_bits_hlt           \
    -mac_dst_count      $dst_count_hlt          \
    -mac_dst_seed       $dst_seed_hlt           \
    -mac_dst_mask       $dst_mask_hlt           \
    -mac_dst_tracking   0                       \
    -mac_src_mode       repeatable_random       \
    -mac_src            $src_bits_hlt           \
    -mac_src_count      $src_count_hlt          \
    -mac_src_seed       $src_seed_hlt           \
    -mac_src_mask       $src_mask_hlt           \
    -mac_src_tracking   0                       \
    -track_by           none                    \
    -egress_tracking    none                    \
]
if {[keylget mac_cfg_config status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget mac_cfg_config log]"
}

puts "Set non repeatable random mac ..."
################################################################################
# Configure Traffic Item with non-repeatbale random mac                        #
################################################################################
set mac_cfg_config [::ixia::traffic_config      \
    -mode               modify                  \
    -traffic_generator  ixnetwork_540           \
    -stream_id          $eth_stack              \
    -l2_encap           ethernet_ii             \
    -mac_dst_mode       random                  \
    -mac_src_mode       random                  \
]
if {[keylget mac_cfg_config status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget mac_cfg_config log]"
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1