################################################################################
# Version 1.0    $Revision: 1 $
# $Author:  $
#
#    Copyright © 1997 - 2009 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    
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
#    This sample creates BGP peers and routes, and sends traffic over it       #
#    using ixnetwork traffic_generator.                                        #
#                                                                              #
#    It uses two Ixia ports. BGP peers and routes are configured on both       #
#    ports.  Streams are generated using ixnetwork traffic_generator           #
#    Traffic statistics are collected for each flow.                           #
#                                                                              #
################################################################################

################################################################################
# DUT config:                                                                  #
# configure terminal                                                           #
# ! 
# interface GigabitEthernet5/3.2
#  encapsulation dot1Q 2
#  ip address 192.1.1.1 255.255.255.0
#  no cdp enable
# !
# interface GigabitEthernet5/3.3
#  encapsulation dot1Q 3
#  ip address 192.1.2.1 255.255.255.0
#  no cdp enable
# !
# interface GigabitEthernet5/3.4
#  encapsulation dot1Q 4
#  ip address 192.1.3.1 255.255.255.0
#  no cdp enable
# !
# interface GigabitEthernet5/3.5
#  encapsulation dot1Q 5
#  ip address 192.1.4.1 255.255.255.0
#  no cdp enable
# !
# interface GigabitEthernet5/3.6
#  encapsulation dot1Q 6
#  ip address 192.1.5.1 255.255.255.0
#  no cdp enable
# !
# interface GigabitEthernet5/3.7
#  encapsulation dot1Q 7
#  ip address 192.1.6.1 255.255.255.0
#  no cdp enable
# !
# interface GigabitEthernet5/3.8
#  encapsulation dot1Q 8
#  ip address 192.1.7.1 255.255.255.0
#  no cdp enable
# !
# interface GigabitEthernet5/3.9
#  encapsulation dot1Q 9
#  ip address 192.1.8.1 255.255.255.0
#  no cdp enable
# !
# interface GigabitEthernet5/3.10
#  encapsulation dot1Q 10
#  ip address 192.1.9.1 255.255.255.0
#  no cdp enable
# !
# interface GigabitEthernet5/3.11
#  encapsulation dot1Q 11
#  ip address 192.1.10.1 255.255.255.0
#  no cdp enable
# interface GigabitEthernet 5/4.2002
# Encapsulation dot1q 2002
# ip address 193.1.1.1 255.255.255.0
# no shut
# !
# interface GigabitEthernet 5/4.2003
# Encapsulation dot1q 2003
# ip address 193.1.2.1 255.255.255.0
# no shut
# !
# interface GigabitEthernet 5/4.2004
# Encapsulation dot1q 2004
# ip address 193.1.3.1 255.255.255.0
# no shut
# !
# interface GigabitEthernet 5/4.2005
# Encapsulation dot1q 2005
# ip address 193.1.4.1 255.255.255.0
# no shut
# !
# interface GigabitEthernet 5/4.2006
# Encapsulation dot1q 2006
# ip address 193.1.5.1 255.255.255.0
# no shut
# !
# interface GigabitEthernet 5/4.2007
# Encapsulation dot1q 2007
# ip address 193.1.6.1 255.255.255.0
# no shut
# !
# interface GigabitEthernet 5/4.2008
# Encapsulation dot1q 2008
# ip address 193.1.7.1 255.255.255.0
# no shut
# !
# interface GigabitEthernet 5/4.2009
# Encapsulation dot1q 2009
# ip address 193.1.8.1 255.255.255.0
# no shut
# !
# interface GigabitEthernet 5/4.2010
# Encapsulation dot1q 2010
# ip address 193.1.9.1 255.255.255.0
# no shut
# !
# interface GigabitEthernet 5/4.2011
# Encapsulation dot1q 2011
# ip address 193.1.10.1 255.255.255.0
# no shut
# !
# Router bgp 65001
# Neighbor 192.1.1.2 remote-as 200
# Neighbor 192.1.2.2 remote-as 201
# Neighbor 192.1.3.2 remote-as 202
# Neighbor 192.1.4.2 remote-as 203
# Neighbor 192.1.5.2 remote-as 204
# Neighbor 192.1.6.2 remote-as 205
# Neighbor 192.1.7.2 remote-as 206
# Neighbor 192.1.8.2 remote-as 207
# Neighbor 192.1.9.2 remote-as 208
# Neighbor 192.1.10.2 remote-as 209
# Neighbor 193.1.1.2 remote-as 200
# Neighbor 193.1.2.2 remote-as 201
# Neighbor 193.1.3.2 remote-as 202
# Neighbor 193.1.4.2 remote-as 203
# Neighbor 193.1.5.2 remote-as 204
# Neighbor 193.1.6.2 remote-as 205
# Neighbor 193.1.7.2 remote-as 206
# Neighbor 193.1.8.2 remote-as 207
# Neighbor 193.1.9.2 remote-as 208
# Neighbor 193.1.10.2 remote-as 209
################################################################################
proc increment_ipv4_address_script {ip_addr ip_addr_step} {
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
set test_name bgp_config

set chassis_ip sylvester

### points to where ixNetwork Tcl Server is running
set network_tcl_server_ip localhost

### points to where Ixia Tcl Server is running - only when using UNIX clients
set tcl_server_ip         sylvester

set port_list             [list 1/3 1/4]
set num_of_bgp_neighbors  10
set num_of_prefix         1
set prefix_ce1            55.0.0.1
set prefix_ce2            70.0.0.1


#################################################################################
# Connects to the IxNetwork Tcl Server, Tcl Server, and the chassis.  
# Takes ownership of the ports.  
# Notes: 
# IxNetwork Tcl Server must be running on a client PC; 
# Tcl Server must be running on a client PC;
#################################################################################
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                  \
        -reset                                       \
        -device               $chassis_ip            \
        -ixnetwork_tcl_server $network_tcl_server_ip \
        -tcl_server           $tcl_server_ip         \
        -port_list            $port_list             \
        -break_locks          1                      \
        -username             ixiaApiUser            \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle_list [::ixia::get_port_list_from_connect \
        $connect_status $chassis_ip $port_list]

set port_0 [lindex $port_handle_list 0]
set port_1 [lindex $port_handle_list 1]


################################################################################
# Configure layer 1 port settings (speed)
################################################################################
set speed                       auto              ;# CHOICES ether10 ether100 ether1000 auto DEFAULT ether100 (for 10/100/1000 Ethernet cards)
set autonegotiation             1                 ;# CHOICES 0 1 DEFAULT 1
set duplex                      auto              ;# CHOICES half full auto DEFAULT full
set phy_mode                    copper            ;# CHOICES copper fiber DEFAULT copper

set interface_status [::ixia::interface_config  \
        -port_handle      $port_handle_list     \
        -autonegotiation  $autonegotiation      \
        -speed            $speed                \
        -duplex           $duplex               \
        -phy_mode         $phy_mode             \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Configure multiple BGP Peers with count option
################################################################################
set bgp_config_status [::ixia::emulation_bgp_config     \
        -port_handle        $port_0                     \
        -mode               reset                       \
        -ip_version         4                           \
        -local_ip_addr      192.1.1.2                   \
        -remote_ip_addr     192.1.1.1                   \
        -local_addr_step    0.0.1.0                     \
        -remote_addr_step   0.0.1.0                     \
        -vlan_id            2                           \
        -vlan_id_step       1                           \
        -count              $num_of_bgp_neighbors       \
        -neighbor_type      external                    \
        -local_as           200                         \
        -local_as_step      1                           \
        -local_as_mode      increment                   \
        ]
if {[keylget bgp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - $port_0 BGP neighbors configuration failed. -\
            [keylget bgp_config_status log]"
}
set ce_bgp_neighbor_handle_list [keylget bgp_config_status handles]
 

foreach bgp_neighbor_handle $ce_bgp_neighbor_handle_list {
    ############################################################################
    # Configure BGP routes on each BGP peer
    ############################################################################
    set bgp_route_config_status [::ixia::emulation_bgp_route_config \
            -mode                  add                     \
            -handle                $bgp_neighbor_handle    \
            -prefix                $prefix_ce1             \
            -prefix_step           1                       \
            -netmask               255.255.255.0           \
            -num_routes            $num_of_prefix          \
            -ip_version            4                       \
            -origin_route_enable   1                       \
            -origin                igp                     \
            ]
    if {[keylget bgp_route_config_status status] != $::SUCCESS} {
        return "FAIL - $test_name - $port_0 BGP routes configuration failed. -\
                [keylget bgp_route_config_status log]"
    }
    set prefix_ce1 [increment_ipv4_address_script $prefix_ce1 0.1.0.0]
}

################################################################################
# Configure multiple BGP Peers and BGP routes on the second Ixia port
################################################################################
set bgp_config_status [::ixia::emulation_bgp_config  \
        -port_handle         $port_1                 \
        -mode                reset                   \
        -ip_version          4                       \
        -local_ip_addr       193.1.1.2               \
        -remote_ip_addr      193.1.1.1               \
        -local_addr_step     0.0.1.0                 \
        -remote_addr_step    0.0.1.0                 \
        -vlan_id             2002                    \
        -vlan_id_step        1                       \
        -count               $num_of_bgp_neighbors   \
        -neighbor_type       external                \
        -local_as            200                     \
        -local_as_step       1                       \
        -local_as_mode       increment               \
        ]
if {[keylget bgp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - $port_1 BGP neighbors configuration failed. -\
            [keylget bgp_config_status log]"
}
set pe_bgp_neighbor_handle_list [keylget bgp_config_status handles]

 
foreach bgp_neighbor_handle $pe_bgp_neighbor_handle_list {
    set bgp_route_config_status [::ixia::emulation_bgp_route_config \
            -mode                   add                             \
            -handle                 $bgp_neighbor_handle            \
            -prefix                 $prefix_ce2                     \
            -prefix_step            1                               \
            -netmask                255.255.255.0                   \
            -num_routes             $num_of_prefix                  \
            -ip_version             4                               \
            -origin_route_enable    1                               \
            -origin                 igp                             \
            ]
    if {[keylget bgp_config_status status] != $::SUCCESS} {
        return "FAIL - $test_name - $port_1 BGP neighbors configuration failed. -\
                [keylget bgp_config_status log]"
    }
    set prefix_ce2 [increment_ipv4_address_script $prefix_ce2 0.1.0.0]
    
}
################################################################################
# Start the BGP sessions
################################################################################
set bgp_control_status [::ixia::emulation_bgp_control   \
        -port_handle    $port_0                         \
        -mode           start                           \
        ]
if {[keylget bgp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - $port_0 - Failed to start BGP CE emulation. -\
            [keylget bgp_config_status log]"
}

set bgp_control_status [::ixia::emulation_bgp_control   \
        -port_handle    $port_1                         \
        -mode           start                           \
        ]
if {[keylget bgp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - $port_1 - Failed to start BGP PE emulation. -\
            [keylget bgp_config_status log]"
}


################################################################################
# Wait for the BGP sessions to establish on first port. 
# Any BGP peer handle configured for the port can be provided to -handle 
# parameter in order to retrive the BGP session' stats for the port.
################################################################################
set bgp_sessions_established 0
set retries                  10
while {($bgp_sessions_established < $num_of_bgp_neighbors) && ($retries >= 0)} {
    # For IxTclNetwork, this command returns per port stats, 
    # evenif a neighbor handle is specified
    set bgp_aggregate_status [ixia::emulation_bgp_info           \
            -handle      [lindex $ce_bgp_neighbor_handle_list 0] \
            -mode        stats                                   \
            ]
    if {[keylget bgp_aggregate_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget bgp_aggregate_status log]"
    }
    puts "Retrieving aggregate BGP stats, number of retries left: $retries ..."
    update idletasks
    if {![catch {keylget bgp_aggregate_status sessions_established}]} {
        set bgp_sessions_established \
                [keylget bgp_aggregate_status sessions_established]
    }
    incr retries -1
    if {$bgp_sessions_established < $num_of_bgp_neighbors} {
        after 1000
    }
}
if {$bgp_sessions_established < $num_of_bgp_neighbors} {
    return "FAIL - $test_name - Not all BGP sessions have been established."
}
puts "There are $bgp_sessions_established BGP sessions established on $port_0 ..."
update idletasks


################################################################################
# Wait for the BGP sessions to establish on second port.
# Any BGP peer handle configured for the port can be provided to -handle 
# parameter in order to retrive the BGP session' stats for the port.
################################################################################
set bgp_sessions_established 0
set retries                  10
while {($bgp_sessions_established < $num_of_bgp_neighbors) && ($retries >= 0)} {
    # For IxTclNetwork, this command returns per port stats, 
    # evenif a neighbor handle is specified
    set bgp_aggregate_status [ixia::emulation_bgp_info           \
            -handle      [lindex $pe_bgp_neighbor_handle_list 0] \
            -mode        stats                                   \
            ]
    if {[keylget bgp_aggregate_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget bgp_aggregate_status log]"
    }
    puts "Retrieving aggregate BGP stats, number of retries left: $retries ..."
    update idletasks
    if {![catch {keylget bgp_aggregate_status sessions_established}]} {
        set bgp_sessions_established \
                [keylget bgp_aggregate_status sessions_established]
    }
    incr retries -1
    if {$bgp_sessions_established < $num_of_bgp_neighbors} {
        after 1000
    }
}
if {$bgp_sessions_established < $num_of_bgp_neighbors} {
    return "FAIL - $test_name - Not all BGP sessions have been established."
}
puts "There are $bgp_sessions_established BGP sessions established on $port_1 ..."
update idletasks

################################################################################
# Use ixnetwork traffic generator to configure traffic from bgp routes on 
# the first port to the bgp routes on the second port. 
# The traffic flow is tracked by source/destination endpoint pair.
################################################################################
set traffic_status [::ixia::traffic_config                              \
        -mode                   create                                  \
        -traffic_generator      ixnetwork                               \
        -transmit_mode          continuous                              \
        -name                   "IPv4_TRAFFIC"                          \
        -src_dest_mesh          one_to_one                              \
        -route_mesh             one_to_one                              \
        -circuit_type           none                                    \
        -circuit_endpoint_type  ipv4                                    \
        -emulation_src_handle   $ce_bgp_neighbor_handle_list            \
        -emulation_dst_handle   $pe_bgp_neighbor_handle_list            \
        -track_by               endpoint_pair                           \
        -stream_packing         one_stream_per_endpoint_pair            \
        -rate_percent           10                                      \
        -tx_delay               10                                      \
        -length_mode            fixed                                   \
        -frame_size             512                                     \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Start the traffic 
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Wait for 10 seconds for the traffic to flow!
################################################################################
after 10000


################################################################################
# Stop the traffic 
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Wait for the traffic to stop - necessary for next step (stats retrieval)
################################################################################
after 15000


################################################################################
# Gather and display aggregate statistics
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
        "Valid Frames Rx."              aggregate.rx.pkt_count              \
        "Valid Frames Rx. Rate"         aggregate.rx.pkt_rate               \
        ]


for {set i 0} {$i < 2} {incr i} {
    puts "Port [subst $[subst port_$i]]:"
    puts "\tAggregated statistics:"
    foreach {name key} $aggregated_traffic_results {
        puts "\t\t[format %30s $name]: [keylget aggregated_traffic_status\
            [subst $[subst port_$i]].$key]"
    }
}


################################################################################
# Gather and display per flow statistics
################################################################################
set flow_traffic_status [::ixia::traffic_stats                            \
        -mode                   flow                                      \
        -traffic_generator      ixnetwork                                 \
        ]
if {[keylget flow_traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget flow_traffic_status log]"
}

set flow_tx_results [list \
        "Tx Port"                       port                              \
        "Tx Frames"                     total_pkts                        \
        "Tx Frame Rate"                 total_pkt_rate                    \
        ]
set flow_rx_results [list                                                 \
        "Rx Port"                       port                              \
        "Rx Frames"                     total_pkts                        \
        "Rx Loss Packets"               loss_pkts                         \
        "Rx Loss Percent"               loss_percent                      \
        "Rx Frame Rate"                 total_pkt_rate                    \
        "Rx Bytes"                      total_pkts_bytes                  \
        "Rx Rate (Bps)"                 total_pkt_byte_rate               \
        "Rx Rate (bps)"                 total_pkt_bit_rate                \
        "Rx Rate (Kbps)"                total_pkt_kbit_rate               \
        "Rx Rate (Mbps)"                total_pkt_mbit_rate               \
        "Avg Latency (ns)"              avg_delay                         \
        "Min Latency (ns)"              min_delay                         \
        "Max Latency (ns)"              max_delay                         \
        "First Timestamp"               first_tstamp                      \
        "Last Timestamp"                last_tstamp                       \
        ]



for {set i 1} {$i <= $num_of_bgp_neighbors} {incr i} {
    set flow_i [keylget flow_traffic_status flow.$i]
    puts "flow: $i  PGID: [keylget flow_i pgid_value] Name: [keylget flow_i flow_name]"
    foreach dir "tx rx" {
        puts "\t $dir:"
        foreach {name key} [subst $[subst flow_${dir}_results]] {
            puts "\t\t$name: [keylget flow_traffic_status flow.$i.$dir.$key]"
        }
    }    
    puts ""
}

################################################################################
# Clean up the session:
# Disconnects from  IxNetwork Tcl server, Tcl server, and Chassis. 
# Clears the ownership from a list of ports.
################################################################################
set cleanup_status [::ixia::cleanup_session -port_handle $port_handle_list -reset ]
if {[keylget cleanup_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget cleanup_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"