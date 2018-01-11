################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Matei-Eugen Vasile $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10-02-2007 Matei-Eugen Vasile
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
#    This sample creates a BACK-TO-BACK setup.                                 #
#                                                                              #
#    It configures two IPv4 Ethernet interfaces and generates traffic between  #
#    them.                                                                     #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################

package require Ixia

set test_name               [info script]

set chassisIP               10.205.19.230
set port_list               [list 2/3 2/4]

################################################################################
# Connect to the chassis, reset to factory defaults and take ownership         #
################################################################################
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                         \
        -reset                                                              \
        -ixnetwork_tcl_server   localhost                                   \
        -device                 $chassisIP                                  \
        -port_list  $           port_list                                   \
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
# Connection established                                                       #
################################################################################

proc script_increment_ipv6_address {ip_addr ip_addr_step} {
    set addr_words [split $ip_addr :]
    set step_words [split $ip_addr_step :]
    set index 7
    set result [list]
    set carry 0
    while {$index >= 0} {
        scan [lindex $addr_words $index] "%x" addr_word
        scan [lindex $step_words $index] "%x" step_word
        set value [expr $addr_word + $step_word + $carry]
        set carry [expr $value / 0xFFFF]
        set value [expr $value % 0xFFFF]
        lappend result $value
        incr index -1
    }
    set new_addr [format "%04x" [lindex $result 7]]
    for {set i 6} {$i >= 0} {incr i -1} {
        append new_addr ":[format "%04x" [lindex $result $i]]"
    }
    return $new_addr
}

proc script_expand_ipv6_address {ip_addr} {
    if {![regexp {(.*)::(.*)} $ip_addr {} before after]} {
        set ip_addr [split $ip_addr :]
        set new_addr "[format "%04x" 0x[lindex $ip_addr 0]]"
        for {set i 1} {$i < [llength $ip_addr]} {incr i} {
            append new_addr ":[format "%04x" 0x[lindex $ip_addr $i]]"
        }
    } else {
        set before [split $before :]
        set after [split $after :]
        set zeroes_length [expr 8 - [llength $before] - \
                [llength $after]]
        set new_addr ""
        if {[llength $before] > 0} {
            append new_addr "[format "%04x" 0x[lindex $before 0]]"
            for {set i 1} {$i < [llength $before]} {incr i} {
                append new_addr ":[format "%04x" 0x[lindex $before $i]]"
            }
        }
        if {$zeroes_length > 0} {
            if {[llength $before] > 0} {
                append new_addr ":0000"
            } else {
                append new_addr "0000"
            }
            for {set i 1} {$i < $zeroes_length} {incr i} {
                append new_addr ":0000"
            }
        }
        if {[llength $after] > 0} {
            for {set i 0} {$i < [llength $after]} {incr i} {
                append new_addr ":[format "%04x" 0x[lindex $after $i]]"
            }
        }
    }
    return $new_addr
}

set port_count              [llength $port_handle]

set intf_count              5
set host_count              3
set group_count             2

set src_ip_address          [script_expand_ipv6_address 2000::1]
set src_ip_address_step     [script_expand_ipv6_address 0:1::]

set host_ip_address         [script_expand_ipv6_address 3000::1]
set host_ip_address_step    [script_expand_ipv6_address 0:1::]

set group_range_ip_address  [script_expand_ipv6_address FF07::1]
set group_range_step        [script_expand_ipv6_address 0::1:0]
set group_range_host_step   [script_expand_ipv6_address 0::1]

################################################################################
# Initialize ports                                                             #
################################################################################
set intf_status [::ixia::interface_config                                   \
        -port_handle        $port_handle                                    \
        -autonegotiation    1                                               \
        ]
if {[keylget intf_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget intf_status log]"
}

################################################################################
# Configure the interfaces used as the traffic sources                         #
################################################################################
set src_intf_handle_list    [list]
set src_address_temp        $src_ip_address
for {set i 0} {$i < $intf_count} {incr i} {
    set intf_status [::ixia::interface_config                                 \
            -mode           config                                          \
            -port_handle    $port_0                                         \
            -ipv6_intf_addr $src_ip_address                                 \
            ]
    if {[keylget intf_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget $intf_status log]"
    }
    lappend src_intf_handle_list [keylget intf_status interface_handle]

    set src_address_temp [script_increment_ipv6_address                     \
            $src_address_temp $src_ip_address_step                          \
            ]
}

################################################################################
# Configure the MLD hosts                                                      #
################################################################################
set mld_host_status [::ixia::emulation_mld_config                             \
        -mode                        create                                 \
        -port_handle                 $port_1                                \
        -mld_version                 v1                                     \
        -count                       $host_count                            \
        -intf_ip_addr                $host_ip_address                       \
        -intf_ip_addr_step           $host_ip_address_step                  \
        -reset                                                              \
        ]
if {[keylget mld_host_status status] != $::SUCCESS} {
    return "FAIL - [keylget mld_host_status log]"
}
set mld_host_handle_list [keylget mld_host_status handle]

################################################################################
#  For each MLD host, configure a group ranges                                 #
################################################################################
set group_range_handle_list         [list]
set group_range_ip_address_temp     $group_range_ip_address
for {set i 0} {$i < $host_count} {incr i} {
    set mcast_group_status [::ixia::emulation_multicast_group_config        \
            -mode          create                                           \
            -num_groups    $group_count                                     \
            -ip_addr_start $group_range_ip_address_temp                     \
            -ip_addr_step  $group_range_step                                \
            ]
    if {[keylget mcast_group_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget mcast_group_status log]"
    }
    set mcast_group_handle [keylget mcast_group_status handle]

    set mld_host_handle [lindex $mld_host_handle_list $i]
    set mcast_group_status [::ixia::emulation_mld_group_config                \
            -mode              create                                       \
            -session_handle    $mld_host_handle                             \
            -group_pool_handle $mcast_group_handle                          \
            ]
    if {[keylget mcast_group_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget mcast_group_status log]"
    }
    lappend group_range_handle_list [keylget mcast_group_status handle]

    set group_range_ip_address_temp [script_increment_ipv6_address          \
            $group_range_ip_address_temp $group_range_host_step             \
            ]
}

################################################################################
# Start MLD                                                                    #
################################################################################
set mld_emulation_status [::ixia::emulation_mld_control                       \
        -port_handle        $port_1                                         \
        -mode               start                                           \
        ]
if {[keylget mld_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget mld_emulation_status log]"
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
        -name                   "IPv6_MLD_Traffic"                          \
        -src_dest_mesh          fully                                       \
        -route_mesh             fully                                       \
        -circuit_type           none                                        \
        -circuit_endpoint_type  ipv6                                        \
        -emulation_src_handle   $src_intf_handle_list                       \
        -emulation_dst_handle   $group_range_handle_list                    \
        -track_by               endpoint_pair                               \
        -stream_packing         one_stream_per_endpoint_pair                \
        -rate_percent           3                                           \
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
