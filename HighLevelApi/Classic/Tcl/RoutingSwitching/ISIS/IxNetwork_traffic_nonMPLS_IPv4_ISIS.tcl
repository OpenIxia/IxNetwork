################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Matei-Eugen Vasile $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    4-30-2007 Matei-Eugen Vasile
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
#    This sample creates a DUT setup.
#                                                                              #
#    It uses two Ixia ports.                                                   #
#                                                                              #
#          -----           -----          ------                               #
#         | IX  |---------| DUT |--------|  IX  |                              #
#          -----     |     -----     |    ------                               #
#                    |               |                                         #
#       Ixia port 1  |  Cisco 7200   |    Ixia port 2                          #
#                                                                              #
#    DUT runs IPv4 IS-IS                                                       #
#    IX runs IPv4 IS-IS                                                        #
#                                                                              #
################################################################################

################################################################################
# DUT config:                                                                  #
################################################################################
# conf t
# !
# interface FastEthernet5/0
#  ip address 21.0.0.1 255.255.255.0
#  ip router isis 400
#  no shutdown
# !
# interface FastEthernet6/0
#  ip address 22.0.0.1 255.255.255.0
#  ip router isis 400
#  no shutdown
# !
# router isis 400
#  net 49.0000.0001.0001.0000.0000.0001.00
#  is-type level-1
#  metric-style transition
# !
# end
################################################################################

proc script_increment_ipv4_address {ip_addr ip_addr_step} {
    set addr_words [split $ip_addr .]
    set step_words [split $ip_addr_step .]
    set index 3
    set result [list]
    set carry 0
    while {$index >= 0} {
        scan [lindex $addr_words $index] "%u" addr_word
        scan [lindex $step_words $index] "%u" step_word
        set value [expr $addr_word + $step_word + $carry]
        set carry [expr $value / 0xFF]
        set value [expr $value % 0xFF]
        lappend result $value
        incr index -1
    }
    set new_addr [format "%u" [lindex $result 3]]
    for {set i 2} {$i >= 0} {incr i -1} {
        append new_addr ".[format "%u" [lindex $result $i]]"
    }
    return $new_addr
}

package require Ixia

set test_name               [info script]

set chassisIP               10.205.19.96
set port_list               [list 2/3 2/4]

set port_count              [llength $port_list]

set local_ip_address        21.0.0.2
set local_ip_address_step   1.0.0.0
set gateway_ip_address      21.0.0.1
set gateway_ip_address_step 1.0.0.0

set route_range_ip_address  100.10.0.0
set route_range_step        0.10.0.0

################################################################################
# Connect to the chassis, reset to factory defaults and take ownership         #
################################################################################
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                         \
        -reset                                                              \
        -device     $chassisIP                                              \
        -port_list  $port_list                                              \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
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

################################################################################
# Initialize ports                                                             #
################################################################################
set intf_status [::ixia::interface_config                                       \
        -port_handle            "$port_0 $port_1"                               \
        -autonegotiation        1                                               \
        -speed                  ether1000                                       \
        -transmit_mode          advanced                                        \
        ]
if {[keylget intf_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget intf_status log]"
}

################################################################################
# Configure an IS-IS emulated router on each port                              #
################################################################################
set isis_router_handle_list [list]
set local_ip_address_temp   $local_ip_address
set gateway_ip_address_temp $gateway_ip_address
for {set i 0} {$i < $port_count} {incr i} {
    set isis_router_status [::ixia::emulation_isis_config                     \
            -mode                   create                                  \
            -reset                                                          \
            -port_handle            [subst $[subst port_$i]]                \
            -ip_version             4                                       \
            -system_id              "00 00 00 00 0$i 00"                    \
            -intf_ip_addr           $local_ip_address_temp                  \
            -gateway_ip_addr        $gateway_ip_address_temp                \
            -intf_ip_prefix_length  24                                      \
            -count                  1                                       \
            -routing_level          L1                                      \
            -loopback_ip_addr_count 0                                       \
            ]
    if {[keylget isis_router_status status] != $::SUCCESS} {
        return "FAIL - [keylget isis_router_status log]"
    }
    lappend isis_router_handle_list [keylget isis_router_status handle]

    set local_ip_address_temp [script_increment_ipv4_address                \
            $local_ip_address_temp $local_ip_address_step                   \
            ]
    set gateway_ip_address_temp [script_increment_ipv4_address              \
            $gateway_ip_address_temp $gateway_ip_address_step               \
            ]
}

################################################################################
#  For each IS-IS router, configure a route range                              #
################################################################################
set route_range_ip_address_temp   $route_range_ip_address
for {set i 0} {$i < $port_count} {incr i} {
    set isis_router_handle [lindex $isis_router_handle_list $i]
    set route_config_status [::ixia::emulation_isis_topology_route_config     \
            -mode                   create                                  \
            -handle                 $isis_router_handle                     \
            -type                   stub                                    \
            -ip_version             4                                       \
            -stub_ip_start          $route_range_ip_address_temp            \
            -stub_ip_step           0.0.8.0                                 \
            -stub_ip_pfx_len        24                                      \
            -stub_count             5                                       \
            -stub_metric            22                                      \
            ]
    if {[keylget route_config_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget route_config_status log]"
    }

    set route_range_ip_address_temp [script_increment_ipv4_address          \
            $route_range_ip_address_temp $route_range_step                  \
            ]
}

################################################################################
# Start IS-IS                                                                  #
################################################################################
for {set i 0} {$i < $port_count} {incr i} {
    set isis_router_handle [lindex $isis_router_handle_list $i]
    set isis_emulation_status [::ixia::emulation_isis_control                 \
            -handle             $isis_router_handle                         \
            -mode               start                                       \
            ]
    if {[keylget isis_emulation_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget isis_emulation_status log]"
    }
}

################################################################################
# Wait for the routes to be learned                                            #
################################################################################
after 30000

################################################################################
# Delete all the streams first                                                 #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action             reset                                           \
        -traffic_generator  ixnetwork                                       \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Generate traffic from the router on the first port to the one on the second  #
################################################################################
set traffic_status [::ixia::traffic_config                                  \
        -mode                   create                                      \
        -traffic_generator      ixnetwork                                   \
        -transmit_mode          continuous                                  \
        -name                   "IPv4_IS-IS_Traffic"                        \
        -src_dest_mesh          fully                                       \
        -route_mesh             one_to_one                                  \
        -circuit_type           none                                        \
        -circuit_endpoint_type  ipv4                                        \
        -emulation_src_handle   [lindex $isis_router_handle_list 0]         \
        -emulation_dst_handle   [lindex $isis_router_handle_list 1]         \
        -track_by               endpoint_pair                               \
        -stream_packing         one_stream_per_endpoint_pair                \
        -pkts_per_burst         2                                           \
        -rate_percent           4.5                                         \
        -enforce_min_gap        9                                           \
        -tx_delay               10                                          \
        -inter_frame_gap        8                                           \
        -inter_burst_gap        11                                          \
        -inter_stream_gap       12                                          \
        -length_mode            fixed                                       \
        -frame_size             512                                         \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Start the traffic                                                            #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# The traffic must flow!                                                       #
################################################################################
after 5000

################################################################################
# Stop the traffic                                                             #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Wait for the traffic to stop                                                 #
################################################################################
after 15000

################################################################################
# Gather and display traffic statistics                                        #
################################################################################
set aggregated_traffic_status [::ixia::traffic_stats                        \
        -mode                   aggregate                                   \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget aggregated_traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggregated_traffic_status log]"
}
set aggregated_traffic_results [list                                        \
        "Scheduled Frames Tx."          aggregate.tx.scheduled_pkt_count    \
        "Scheduled Frames Tx. Rate"     aggregate.tx.scheduled_pkt_rate     \
        "Line Speed"                    aggregate.tx.line_speed             \
        "Frames Tx."                    aggregate.tx.pkt_count              \
        "Total Frames Tx."              aggregate.tx.total_pkts             \
        "Frames Tx. Rate"               aggregate.tx.pkt_rate               \
        "Frames Tx. Rate"               aggregate.tx.total_pkt_rate         \
        "Bytes Tx."                     aggregate.tx.pkt_byte_count         \
        "Bytes Tx. Rate"                aggregate.tx.pkt_byte_rate          \
        "Tx. Rate (bps)"                aggregate.tx.pkt_bit_rate           \
        "Tx. Rate (Kbps)"               aggregate.tx.pkt_kbit_rate          \
        "Tx. Rate (Mbps)"               aggregate.tx.pkt_mbit_rate          \
        "Bytes Rx."                     aggregate.rx.pkt_byte_count         \
        "Bytes Rx. Rate"                aggregate.rx.pkt_byte_rate          \
        "Rx. Rate (bps)"                aggregate.rx.pkt_bit_rate           \
        "Rx. Rate (Kbps)"               aggregate.rx.pkt_kbit_rate          \
        "Rx. Rate (Mbps)"               aggregate.rx.pkt_mbit_rate          \
        "Data Integrity Frames Rx."     aggregate.rx.data_int_frames_count  \
        "Data Integrity Errors"         aggregate.rx.data_int_errors_count  \
        "Collisions"                    aggregate.rx.collisions_count       \
        "Valid Frames Rx."              aggregate.rx.pkt_count              \
        "Valid Frames Rx. Rate"         aggregate.rx.pkt_rate               \
        ]
for {set i 0} {$i < $port_count} {incr i} {
    puts "Port [subst $[subst port_$i]]:"
    puts "\tAggregated statistics:"
    foreach {name key} $aggregated_traffic_results {
        puts "\t\t$name: [keylget aggregated_traffic_status\
                [subst $[subst port_$i]].$key]"
    }
}

set stream_traffic_status [::ixia::traffic_stats                            \
        -mode                   stream                                      \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget stream_traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget stream_traffic_status log]"
}
set stream_tx_results [list                                                 \
        "Tx Frames"                     total_pkts                          \
        "Tx Frame Rate"                 total_pkt_rate                      \
        ]
set stream_rx_results [list                                                 \
        "Rx Frames"                     total_pkts                          \
        "Frames Delta"                  loss_pkts                           \
        "Rx Frame Rate"                 total_pkt_rate                      \
        "Loss %"                        loss_percent                        \
        "Rx Bytes"                      total_pkts_bytes                    \
        "Rx Rate (Bps)"                 total_pkt_byte_rate                 \
        "Rx Rate (bps)"                 total_pkt_bit_rate                  \
        "Rx Rate (Kbps)"                total_pkt_kbit_rate                 \
        "Rx Rate (Mbps)"                total_pkt_mbit_rate                 \
        "Avg Latency (ns)"              avg_delay                           \
        "Min Latency (ns)"              min_delay                           \
        "Max Latency (ns)"              max_delay                           \
        "First Timestamp"               first_tstamp                        \
        "Last Timestamp"                last_tstamp                         \
        ]
for {set i 0} {$i < $port_count} {incr i} {
    puts "Port [subst $[subst port_$i]]:"
    set streams [keylget stream_traffic_status \
            [subst $[subst port_$i]].stream]
    foreach stream [keylkeys streams] {
        set stream_key [keylget stream_traffic_status \
                [subst $[subst port_$i]].stream.$stream]
        foreach dir [keylkeys stream_key] {
            puts "\tStream $stream - $dir:"
            foreach {name key} [subst $[subst stream_${dir}_results]] {
                puts "\t\t$name: [keylget stream_traffic_status\
                        [subst $[subst port_$i]].stream.$stream.$dir.$key]"
            }
        }
    }
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
