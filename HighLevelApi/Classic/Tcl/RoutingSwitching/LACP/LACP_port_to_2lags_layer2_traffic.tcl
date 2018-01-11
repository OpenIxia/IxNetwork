################################################################################
# Version 1.1    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    12-05-2008 LRaicea - created sample
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
#    This sample creates two LAGs using four Ixia ports.                       #
#    Layer 2 traffic is sent from a fifth port to the 2 LAGs                   #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET42.                                      #
#                                                                              #
################################################################################

################################################################################
# DUT configuration layer 2:
#
# conf t
# default interface range GigabitEthernet 1/0/3-10
# no interface Port-channel 3
# no interface Port-channel 5
# no interface Port-channel 7
# no interface Port-channel 9
# 
# #LACP aggregator interface configuration
# interface Port-channel3
#  switchport
#  no ip address
# !
# #LACP port 1
# interface GigabitEthernet1/0/3
#  switchport
#  no ip address
#  channel-group 3 mode active
#  channel-protocol lacp
# !
# 
# #LACP port 2
# interface GigabitEthernet1/0/4
#  switchport
#  no ip address
#  channel-group 3 mode active
#  channel-protocol lacp
# !
# #LACP aggregator interface configuration
# interface Port-channel5
#  switchport
#  no ip address
# !
# #LACP port 3
# interface GigabitEthernet1/0/5
#  switchport
#  no ip address
#  channel-group 5 mode active
#  channel-protocol lacp
# !
# 
# #LACP port 4
# interface GigabitEthernet1/0/6
#  switchport
#  no ip address
#  channel-group 5 mode active
#  channel-protocol lacp
# !
# #Non LACP port
# interface GigabitEthernet1/0/7
#  switchport
#  no ip address
# 
# port-channel load-balance src-mac
# 
# mac address-table static 0013.0101.0284 vlan 1 interface port-channel 3
# mac address-table static 0013.0103.0284 vlan 1 interface port-channel 5
#
################################################################################

set env(IXIA_VERSION) HLTSET42
package require Ixia

################################################################################
# General script variables
################################################################################
set test_name               [info script]
set num_pgids               10

################################################################################
# START - Connect to the chassis
################################################################################
puts "Start connecting to chassis ..."
update idletasks

set chassis_ip              sylvester
set port_list               [list 1/1 1/3 1/2 1/4 1/5]
set break_locks             1
set username                ixiaApiUser

set connect_status [::ixia::connect                                        \
        -reset                                                             \
        -device               $chassis_ip                                  \
        -port_list            $port_list                                   \
        -break_locks          $break_locks                                 \
        -username             $username                                    \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
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
    
    # Initialize per port variables
    set interface_handles_$port ""
    
    incr i
}

puts "End connecting to chassis ..."
update idletasks
################################################################################
# END - Connect to the chassis
################################################################################

################################################################################
# START - Interface configuration - L1
################################################################################
puts "Start L1 interface configuration ..."
update idletasks

set interface_status [::ixia::interface_config                                  \
        -port_handle                 $port_handle                               \
        -mode                        config                                     \
        -intf_mode                   ethernet                                   \
        -autonegotiation             1                                          \
        -speed                       auto                                       \
        -duplex                      auto                                       \
        -phy_mode                    copper                                     \
        -transmit_mode               advanced                                   \
        -port_rx_mode                auto_detect_instrumentation                \
        -signature                   {87 73 67 49 42 87 11 80 08 71 18 05}      \
        -signature_mask              {00 00 00 00 00 00 00 00 00 00 00 00}      \
        -signature_offset            48                                         \
        -signature_start_offset      14                                         \
        -pgid_offset                 52                                         \
        -pgid_mode                   custom                                     \
        -pgid_split1_mask            0xFFFFFFFF                                 \
        -pgid_split1_offset          52                                         \
        -pgid_split1_width           4                                          \
        -pgid_split2_mask            0xFFFFFFFF                                 \
        -pgid_split2_offset          52                                         \
        -pgid_split2_width           4                                          \
        -pgid_split3_mask            0xFFFFFFFF                                 \
        -pgid_split3_offset          52                                         \
        -pgid_split3_width           4                                          \
        -sequence_num_offset         44                                         \
        -integrity_signature         08.71.18.00                                \
        -integrity_signature_offset  40                                         \
        -qos_stats                   1                                          \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

puts "End L1 interface configuration ..."
update idletasks
################################################################################
# END - Interface configuration - L1
################################################################################################################################################################

################################################################################
# START - LACP configuration
################################################################################
puts "Start LACP configuration ..."
update idletasks

set lacp_port_handle                      [lrange $port_handle 0 [expr [llength $port_handle] - 2]]

################################################################################
# Start LACP Call
################################################################################
set lacp_link_config_status [::ixia::emulation_lacp_link_config                 \
        -mode                                  create                           \
        -reset                                                                  \
        -lag_count                             2                                \
        -port_handle                           $lacp_port_handle                \
        -actor_key                             3                                \
        -actor_key_step                        2                                \
        -actor_port_num_step                   0                                \
        -actor_port_pri_step                   0                                \
        -actor_system_id                       0013.0101.0284                   \
        -actor_system_id_step                  0000.0002.0000                   \
        -actor_system_pri_step                 0                                \
        -auto_pick_port_mac                    0                                \
        -port_mac                              0013.0101.0284                   \
        -port_mac_step                         0000.0002.0000                   \
        ]
if {[keylget lacp_link_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp_link_config_status log]"
    return
}
set lacp_link_handles [keylget lacp_link_config_status handle]
puts "Ixia LACP handles are: "
update idletasks
foreach lacp_link_handle $lacp_link_handles {
    puts $lacp_link_handle
    update idletasks
}
################################################################################
# End LACP Call
################################################################################

puts "End LACP configuration ..."
update idletasks
################################################################################
# END - LACP configuration
################################################################################

################################################################################
# LACP - Protocol start
################################################################################
set lacp_control_status [::ixia::emulation_lacp_control                           \
        -mode            start                                                    \
        -port_handle     [lrange $port_handle 0 [expr [llength $port_handle] - 2]]\
        ]
if {[keylget lacp_control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp_control_status log]"
    return
}
puts "Starting LACP protocol ..."
update idletasks
# Wait for links to be aggregated
after 30000

################################################################################
# LACP - Gather learned info
################################################################################
set lacp_agg_links 0
set retries        20
puts "Retrieving LACP learned info ..."
update idletasks
while {($lacp_agg_links < [expr [llength $port_handle] - 1]) && $retries} {
    set lacp_info_status [::ixia::emulation_lacp_info                                 \
            -mode            learned_info                                             \
            -port_handle     [lrange $port_handle 0 [expr [llength $port_handle] - 2]]\
            ]
    if {[keylget lacp_info_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget lacp_info_status log]"
        return
    }
    set lacp_agg_links 0
    foreach port [lrange $port_handle 0 [expr [llength $port_handle] - 2]] {
        if {![catch {keylget lacp_info_status $port.actor_link_aggregation_status} retStat]} {
            if {$retStat == 1} {
                incr lacp_agg_links
            }
        }
    }
    incr retries -1
    puts "LACP aggregated links - $lacp_agg_links ..."
}
foreach port [lrange $port_handle 0 [expr [llength $port_handle] - 2]] {
    puts "Port $port - Learned info ..."
    puts [string repeat "-" 80]
    foreach key [keylkeys lacp_info_status $port] {
        if {![catch {keylget lacp_info_status $port.$key} retStat]} {
            puts [format "%30s %s" $key $retStat]
        }
    }
}
if {$lacp_agg_links < [expr [llength $port_handle] - 1]} {
    puts "FAIL - $test_name - Not all LACP links have been aggregated."
    return
}

################################################################################
# LACP - Gather configuration info
################################################################################
puts "Retrieving LACP configuration info ..."
update idletasks
set lacp_cfg_info [::ixia::emulation_lacp_info                                 \
        -mode            configuration                                         \
        ]
if {[keylget lacp_cfg_info status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp_cfg_info log]"
    return
}
################################################################################
# TRAFFIC - Reset all streams
################################################################################
set traffic_status [::ixia::traffic_control                                    \
        -action             reset                                              \
        -port_handle        $port_handle                                       \
        -traffic_generator  ixos                                               \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

################################################################################
# START - TRAFFIC configuration
################################################################################
puts "Start traffic configuration ..."
update idletasks

set traffic_index 0
foreach lag_id_i [keylkeys lacp_cfg_info lag] {
    set system_id_i    [keylget lacp_cfg_info lag.$lag_id_i.actor_system_id]
    incr traffic_index

    ################################################################################
    # TRAFFIC - Configuration
    ################################################################################
    set traffic_config_status [::ixia::traffic_config                           \
            -mode                                create                         \
            -port_handle                         [lindex $port_handle end]      \
            -number_of_packets_per_stream        100                            \
            -number_of_packets_tx                100                            \
            -rate_bps                            3500000                        \
            -data_pattern                        1                              \
            -data_pattern_mode                   incr_byte                      \
            -length_mode                         fixed                          \
            -frame_size                          512                            \
            -ethernet_type                       ethernetII                     \
            -ethernet_value                      0xFFFF                         \
            -mac_dst                             $system_id_i                   \
            -mac_dst2                            0000.0000.0000                 \
            -mac_dst_mode                        fixed                          \
            -mac_src                             00cc.00dd.0001                 \
            -mac_src2                            0000.0000.0000                 \
            -mac_src_count                       10                             \
            -mac_src_mode                        increment                      \
            -mac_src_step                        0000.0000.0001                 \
            -enable_auto_detect_instrumentation  1                              \
            -enable_udf1                         1                              \
            -udf1_mode                           counter                        \
            -udf1_offset                         26                             \
            -udf1_counter_type                   32                             \
            -udf1_counter_up_down                up                             \
            -udf1_counter_init_value             ${traffic_index}0              \
            -udf1_counter_repeat_count           $num_pgids                     \
            -udf1_counter_step                   1                              \
            -udf1_value_list                     {10 20 30 40}                  \
            -udf1_counter_mode                   count                          \
            -udf1_inner_repeat_value             1                              \
            -udf1_inner_repeat_count             1                              \
            -udf1_inner_step                     1                              \
        ]
    if {[keylget traffic_config_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget traffic_config_status log]"
        return
    }
}
puts "End traffic configuration ..."
update idletasks

################################################################################
# END - TRAFFIC configuration
################################################################################

################################################################################
# TRAFFIC - Clear statistics
#         - This is absolutely necessary for starting PGID stats retrieval
################################################################################
set traffic_status [::ixia::traffic_control                                    \
        -action             clear_stats                                        \
        -port_handle        $port_handle                                       \
        -traffic_generator  ixos                                               \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

################################################################################
# TRAFFIC - Start the traffic 
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 sync_run                                    \
        -port_handle            [lindex $port_handle end]                   \
        -traffic_generator      ixos                                        \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

################################################################################
# The traffic must flow!
################################################################################
puts "Transmitting for 15 seconds ..."
after 15000

################################################################################
# Stop the traffic 
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -port_handle            [lindex $port_handle end]                   \
        -traffic_generator      ixos                                        \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}
# Wait for the traffic to stop 
after 30000

################################################################################
# Gather traffic statistics 
################################################################################
set pgid_list ""
set traffic_index 0
foreach lag_id_i [keylkeys lacp_cfg_info lag] {
    incr traffic_index
    for {set j 0} {$j < $num_pgids} {incr j} {
        lappend pgid_list ${traffic_index}$j
    }
}
set aggregate_stats [::ixia::traffic_stats                                     \
        -port_handle       $port_handle                                        \
        -mode              aggregate                                           \
        -packet_group_id   $pgid_list                                          \
        ]
if {[keylget aggregate_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget aggregate_stats log]"
    return
}
################################################################################
# Display aggregated traffic statistics 
################################################################################
set aggregated_traffic_stats [list                                             \
        "Frames Tx."                    aggregate.tx.pkt_count                 \
        "Frames Tx. Rate"               aggregate.tx.pkt_rate                  \
        "Raw Frames Tx."                aggregate.tx.raw_pkt_count             \
        "Raw Frames Tx. Rate"           aggregate.tx.raw_pkt_rate              \
        "Bytes Tx."                     aggregate.tx.pkt_byte_count            \
        "Bytes Tx. Rate"                aggregate.tx.pkt_byte_rate             \
        "Tx. Rate (bps)"                aggregate.tx.pkt_bit_rate              \
        "Frames Rx."                    aggregate.rx.pkt_count                 \
        "Frames Rx. Rate"               aggregate.rx.pkt_rate                  \
        "Raw Frames Rx."                aggregate.rx.raw_pkt_count             \
        "Raw Frames Rx. Rate"           aggregate.rx.raw_pkt_rate              \
        ]


puts "Aggregated Statistics:"
puts -nonewline [format "%20s" [string repeat " " 20]]
foreach port $port_handle {
    puts -nonewline [format "%20s" $port]
}
puts ""
puts [string repeat "-" [expr 20 + [llength $port_handle] * 20]]

foreach {name key} $aggregated_traffic_stats {
    puts -nonewline [format "%20s" $name]
    foreach port $port_handle {
        if {![catch {keylget aggregate_stats $port.$key} retStat]} {
            puts -nonewline [format "%20s" $retStat]
        } else {
            puts -nonewline [format "%20s" NA]
        }
    }
    puts ""
}
################################################################################
# Display PGID traffic statistics 
################################################################################
set pgid_traffic_stats [list                                                   \
        "Frames Rx."                    pgid.rx.pkt_count                      \
        "Min Latency"                   pgid.rx.min_latency                    \
        "Max Latency"                   pgid.rx.max_latency                    \
        "Avg Latency"                   pgid.rx.avg_latency                    \
        ]
puts "\n\nPGID Statistics:"
set pgid_ports ""
foreach lag_id_i [keylkeys lacp_cfg_info lag] {
    set pgid_ports [concat $pgid_ports [keylget lacp_cfg_info lag.$lag_id_i.ports]]
}
puts -nonewline [format "%20s" [string repeat " " 20]]
foreach port $pgid_ports {
    puts -nonewline [format "%20s" $port]
}
puts ""
puts [string repeat "-" [expr 20 + [llength $pgid_ports] * 20]]

set frames_tx [keylget aggregate_stats [lindex $port_handle end].aggregate.tx.pkt_count]
set frames_rx 0
foreach {pgid} $pgid_list {
    puts "PGID $pgid:"
    foreach {name key} $pgid_traffic_stats {    
        puts -nonewline [format "%20s" $name]
        foreach port $pgid_ports {
            if {![catch {keylget aggregate_stats $port.$key.$pgid} retStat]} {
                puts -nonewline [format "%20s" $retStat]
                if {$key == "pgid.rx.pkt_count"} {
                    incr frames_rx $retStat
                }
            } else {
                puts -nonewline [format "%20s" NA]
            }
        }
        puts ""
    }
}
puts "Total Rx: $frames_rx, Total Tx: $frames_tx"
if {($frames_rx > [expr $frames_tx + ($frames_tx / [llength $pgid_list]) * 0.1])} {
    puts "FAIL - $test_name - Too many frames have been received. Rx: $frames_rx, Tx: $frames_tx"
    return
}
if {($frames_rx < [expr $frames_tx - ($frames_tx / [llength $pgid_list]) * 0.1])} {
    puts "FAIL - $test_name - Not all frames have been received. Rx: $frames_rx, Tx: $frames_tx"
    return
}
################################################################################
# LACP - Protocol stop
################################################################################
set lacp_control_status [::ixia::emulation_lacp_control                        \
        -mode            stop                                                  \
        -port_handle     [lrange $port_handle 0 [expr [llength $port_handle] - 2]]\
        ]
if {[keylget lacp_control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp_control_status log]"
    return
}
puts "Stopping LACP protocol ..."
update idletasks

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return
