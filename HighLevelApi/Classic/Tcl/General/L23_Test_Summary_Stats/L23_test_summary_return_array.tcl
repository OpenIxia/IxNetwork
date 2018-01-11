#################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    04-11-2013 Mchakravarthy - created sample
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
#    This sample connects to IxNetwork Tcl Server and configures IPV4 traffic. #
#    The stats is calculated using mode l23_test_summary and return_method     #
#    array                                                                     #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################
################################################################################
# Loaading Ixia package                                                        #
################################################################################

# Loading Ixia package

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}
################################################################################
# General script variables
################################################################################
set chassis_ip              {10.206.27.55}
set port_list               [list 8/1 8/2]
set tcl_server              localhost
set ixnetwork_tcl_server    localhost
set ::test_name             [info script]

################################################################################
# Procedures used in the test                                                  #
################################################################################

proc CheckFailure {handle} {
    upvar $handle local_handle
    if {[keylget local_handle status] != $::SUCCESS} { 
             puts "FAIL - $::test_name - [keylget local_handle log]"
             catch {::ixia::cleanup_session}
             uplevel 1 { return 0 }
    }
}

proc keylprint {listvalues {indentationLevel 0} {indentString "    "}} {
    set x 30
    foreach key [keylkeys listvalues] {
        set value [keylget listvalues $key]
        set heading [string repeat $indentString $indentationLevel]
        try_eval {
            set subkeys [keylkeys listvalues $key]
            set sublistvalues [keylget listvalues $key]
            puts "$heading$key:"
            keylprint $sublistvalues [expr {$indentationLevel + 1}] $indentString
        } {
            set y [expr $x - [string length $heading] - [string length $key]]
            puts  "$heading$key[string repeat "." $y]: [string repeat " " \
                    [expr 15 -[string length $value]]]$value"
        }
    }
}

################################################################################
# START - Connect to the chassis
################################################################################

# Connecting and getting the port handles
set connect_status  [ixia::connect                                          \
                        -reset                                              \
                        -ixnetwork_tcl_server $ixnetwork_tcl_server         \
                        -tcl_server $tcl_server                             \
                        -device $chassis_ip                                 \
                        -port_list $port_list                               \
                    ]
CheckFailure connect_status
set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} temp_port]} {
        lappend port_handle $temp_port
    }
}
set port_src_handle [lindex $port_handle 0]
set port_dst_handle [lindex $port_handle 1]
puts "Ixia port handles are $port_handle ..."
puts "End connecting to chassis ..."
################################################################################
# END - Connect to the chassis
################################################################################

################################################################################
# START - Interface configuration - Port src
################################################################################
puts "Start interface configuration for Port:$port_src_handle"

set _result_    [::ixia::interface_config                                       \
                        -mode                           config                  \
                        -port_handle                    $port_src_handle        \
                        -vlan                           0                       \
                        -l23_config_type                protocol_interface      \
                        -mtu                            1500                    \
                        -gateway                        20.0.0.1                \
                        -intf_ip_addr                   20.0.0.2                \
                        -netmask                        255.255.255.0           \
                        -src_mac_addr                   0000.0107.4232          \
                        -arp_on_linkup                  0                       \
                        -ns_on_linkup                   0                       \
                        -single_arp_per_gateway         1                       \
                        -single_ns_per_gateway          1                       \
                        -check_opposite_ip_version      0                       \
                ]
CheckFailure _result_ 

puts "End interface configuration for Port:$port_src_handle"

################################################################################
# START - Interface configuration - Port dst
################################################################################

puts "Start interface configuration for Port:$port_dst_handle"

set _result_    [::ixia::interface_config -mode config                          \
                        -port_handle                    $port_dst_handle        \
                        -vlan                           0                       \
                        -l23_config_type                protocol_interface      \
                        -mtu                            1500                    \
                        -gateway                        20.0.0.2                \
                        -intf_ip_addr                   20.0.0.1                \
                        -netmask                        255.255.255.0           \
                        -check_opposite_ip_version      0                       \
                        -src_mac_addr                   0000.0107.4233          \
                        -arp_on_linkup                  0                       \
                        -ns_on_linkup                   0                       \
                        -single_arp_per_gateway         1                       \
                        -single_ns_per_gateway          1                       \
                ]
CheckFailure _result_ 

puts "End interface configuration for Port:$port_dst_handle"

################################################################################
# Delete all the streams first
################################################################################

set traffic_status  [::ixia::traffic_control                                      \
                            -action                         reset                 \
                            -traffic_generator              ixnetwork_540         \
                            -cpdp_convergence_enable        0                     \
                            -delay_variation_enable         0                     \
                            -packet_loss_duration_enable    0                     \
                            -latency_bins                   3                     \
                            -latency_values                 {1.5 3 6.8}           \
                            -latency_control                store_and_forward     \
                    ]
CheckFailure traffic_status

################################################################################
# Configure the IPv4 Traffic and run
################################################################################
puts "Configure Traffic..." 
set ti_src ::ixNet::OBJ-/vport:1/protocols
set ti_dst ::ixNet::OBJ-/vport:2/protocols

set traffic_result  [::ixia::traffic_config                                     \
                    -mode                                       create          \
                    -endpointset_count                          1               \
                    -traffic_generator                          ixnetwork_540   \
                    -emulation_src_handle                       $ti_src         \
                    -emulation_dst_handle                       $ti_dst         \
                    -global_dest_mac_retry_count                1               \
                    -global_dest_mac_retry_delay                5               \
                    -global_refresh_learned_info_before_apply   0               \
                    -enable_data_integrity                      1               \
                    -global_enable_dest_mac_retry               1               \
                    -hosts_per_net                              1               \
                    -global_enable_min_frame_size               0               \
                    -global_enable_staggered_transmit           0               \
                    -global_enable_stream_ordering              0               \
                    -global_stream_control                      continuous      \
                    -global_stream_control_iterations           1               \
                    -global_large_error_threshhold              2               \
                    -global_enable_mac_change_on_fly            0               \
                    -global_mpls_label_learning_timeout         30              \
                    -global_max_traffic_generation_queries      500             \
                    -global_use_tx_rx_sync                      1               \
                    -global_wait_time                           1               \
                    -global_display_mpls_current_label_value    0               \
                    -frame_sequencing                           disable         \
                    -frame_sequencing_mode                      rx_threshold    \
                    -bidirectional                              0               \
                    -src_dest_mesh                              one_to_one      \
                    -route_mesh                                 one_to_one      \
                    -allow_self_destined                        0               \
                    -enable_dynamic_mpls_labels                 0               \
                    -name                                       Traffic_Item_1  \
                    -source_filter                              all             \
                    -destination_filter                         all             \
                    -merge_destinations                         1               \
                    -circuit_endpoint_type                      ipv4            \
                    -egress_tracking                            none            \
                    -ip_dst_tracking                            1               \
                    ]
CheckFailure traffic_result
set current_config_element [keylget traffic_result traffic_item]
set stack_handle [lindex [keylget traffic_result $current_config_element.headers] 0]

puts "Running Traffic..."
set run_traffic [::ixia::traffic_control -action run -instantaneous_stats_enable 1 ]
CheckFailure run_traffic
after 30000

################################################################################
# Getting statistics                                                           #
################################################################################

set stats [::ixia::traffic_stats -mode l23_test_summary -return_method array]
CheckFailure stats
keylprint $stats

################################################################################
# Stopping traffic and cleaning up                                             #
################################################################################

puts "Stopping Traffic..."
set stop_traffic [::ixia::traffic_control -action stop]

puts "Disconnecting from IxNetwork and cleaning up..."
set cleanup [::ixia::cleanup_session -reset]

################################################################################
#   If everything executed sucessfully until here then test is pass.           #
################################################################################

puts "SUCCESS - $::test_name - [clock format [clock seconds]]"
return 1


