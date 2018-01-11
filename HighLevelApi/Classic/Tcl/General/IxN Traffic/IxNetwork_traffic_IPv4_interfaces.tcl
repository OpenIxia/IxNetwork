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

set chassisIP               10.205.19.96
set port_list               [list 2/1 2/2]

set port_count              [llength $port_list]

################################################################################
# Connect to the chassis, reset to factory defaults and take ownership         #
################################################################################
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                         \
        -reset                                                              \
        -ixnetwork_tcl_server   localhost                                   \
        -device                 $chassisIP                                  \
        -port_list              $port_list                                  \
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
# Configure interfaces                                                         #
################################################################################
set intf_status [::ixia::interface_config                                   \
        -port_handle        [list $port_0           $port_1]                \
        -intf_ip_addr       [list 20.0.0.1          20.0.0.2]               \
        -gateway            [list 20.0.0.2          20.0.0.1]               \
        -netmask            [list 255.255.255.0     255.255.255.0]          \
        -src_mac_addr       [list 0cb0.0012.0001    0cb0.0012.0002]         \
        -autonegotiation    1                                               \
        -speed              ether1000                                       \
        -transmit_mode      advanced                                        \
        ]
if {[keylget intf_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget intf_status log]"
}
set interface_handles [keylget intf_status interface_handle]

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
        -name                   "IPv4_Traffic"                              \
        -src_dest_mesh          fully                                       \
        -route_mesh             one_to_one                                  \
        -circuit_type           none                                        \
        -circuit_endpoint_type  ipv4                                        \
        -emulation_src_handle   [lindex $interface_handles 0]               \
        -emulation_dst_handle   [lindex $interface_handles 1]               \
        -track_by               endpoint_pair                               \
        -stream_packing         one_stream_per_endpoint_pair                \
        -pkts_per_burst         2                                           \
        -rate_percent           4.5                                         \
        -enforce_min_gap        9                                           \
        -tx_delay               10                                          \
        -inter_frame_gap        8                                           \
        -inter_burst_gap        11                                          \
        -inter_stream_gap       12                                          \
        -length_mode            increment                                   \
        -frame_size_max         512                                         \
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
