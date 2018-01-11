################################################################################
# Version 1.0    $Revision: 1 $
#
#
#    Copyright © 1997 - 2010 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    2/9 - C. Nicutar - created sample
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
#     This script configures two back-to-back Ixia ports and creates           #
#     10 BGP neighbors for each port, runs traffic and retrieves statistics.   #
#     In this case, we demonstrate how user defined stats (-uds_port_filter,   #
#     -uds_traffic_item_filter etc) are retrieved.                             #
# Module:                                                                      #
#    The sample was tested on an STXS4 module.                                 #
#                                                                              #
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

set test_name [info script]

set chassisIP sylvester
set port_list [list 2/3 2/4]


set num_of_bgp_neighbors  10
set num_of_prefix         1
set prefix_ce1            55.0.0.1
set prefix_ce2            70.0.0.1


# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
        -reset                                  \
        -ixnetwork_tcl_server   localhost       \
        -device                 $chassisIP      \
        -port_list              $port_list      \
        -username               ixiaApiUser     ]

if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_array [keylget connect_status port_handle.$chassisIP]

set port_0 [keylget port_array [lindex $port_list 0]]
set port_1 [keylget port_array [lindex $port_list 1]]

set interface_status1 [::ixia::interface_config \
        -port_handle        $port_0          \
        -intf_ip_addr       192.168.1.1      \
        -gateway            192.168.1.2      \
        -netmask            255.255.255.0    \
        -autonegotiation    1                \
        -duplex             auto             \
        -speed              auto             \
        -intf_mode          ethernet         ]
if {[keylget interface_status1 status] != $::SUCCESS} {
	puts "FAIL - $test_name - [keylget interface_status log]"
	return 0
}


set interface_status1 [::ixia::interface_config \
        -port_handle        $port_0          \
        -intf_ip_addr       192.168.1.2      \
        -gateway            192.168.1.1      \
        -netmask            255.255.255.0    \
        -autonegotiation    1                \
        -duplex             auto             \
        -speed              auto             \
        -intf_mode          ethernet         ]
if {[keylget interface_status1 status] != $::SUCCESS} {
	puts "FAIL - $test_name - [keylget interface_status log]"
	return 0
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
        -neighbor_type      internal                    \
        -local_as           200                         \
        -local_as_step      1                           \
        -local_as_mode      increment                   \
        ]
if {[keylget bgp_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - $port_0 BGP neighbors configuration failed. -\
            [keylget bgp_config_status log]"
    return 0
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
        puts "FAIL - $test_name - $port_0 BGP routes configuration failed. -\
                [keylget bgp_route_config_status log]"
        return 0
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
        -local_ip_addr       192.1.1.1               \
        -remote_ip_addr      192.1.1.2               \
        -local_addr_step     0.0.1.0                 \
        -remote_addr_step    0.0.1.0                 \
        -vlan_id             2                       \
        -vlan_id_step        1                       \
        -count               $num_of_bgp_neighbors   \
        -neighbor_type       internal                \
        -local_as            200                     \
        -local_as_step       1                       \
        -local_as_mode       increment               \
        ]
if {[keylget bgp_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - $port_1 BGP neighbors configuration failed. -\
            [keylget bgp_config_status log]"
    return 0
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
        puts "FAIL - $test_name - $port_1 BGP neighbors configuration failed. -\
                [keylget bgp_config_status log]"
        return 0
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
    puts "FAIL - $test_name - $port_0 - Failed to start BGP CE emulation. -\
            [keylget bgp_config_status log]"
    return 0
}

set bgp_control_status [::ixia::emulation_bgp_control   \
        -port_handle    $port_1                         \
        -mode           start                           \
        ]
if {[keylget bgp_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - $port_1 - Failed to start BGP PE emulation. -\
            [keylget bgp_config_status log]"
    return 0
}


################################################################################
# Wait for the BGP sessions to establish on first port.
# Any BGP peer handle configured for the port can be provided to -handle
# parameter in order to retrive the BGP session' stats for the port.
################################################################################

# this sleep is in leiu of the sats code working
puts "Waiting for 10 seconds... (first port)"
update idletasks
after 10000
puts "Done."
update idletasks


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
        puts "FAIL - $test_name - [keylget bgp_aggregate_status log]"
        return 0
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
    puts "FAIL - $test_name - Not all BGP sessions have been established."
    return 0
}
puts "There are $bgp_sessions_established BGP sessions established on $port_0 ..."



################################################################################
# Wait for the BGP sessions to establish on second port.
# Any BGP peer handle configured for the port can be provided to -handle
# parameter in order to retrive the BGP session' stats for the port.
################################################################################

puts "Waiting for 10 seconds... (second port)"
update idletasks
after 10000
puts "Done."
update idletasks

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
        puts "FAIL - $test_name - [keylget bgp_aggregate_status log]"
        return 0
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

puts "There are $bgp_sessions_established BGP sessions established on $port_1 ..."

if {$bgp_sessions_established < $num_of_bgp_neighbors} {
    puts "FAIL - $test_name - Not all BGP sessions have been established."
    return 0
}


################################################################################
# Use ixnetwork traffic generator to configure traffic from bgp routes on
# the first port to the bgp routes on the second port.
#
################################################################################
set traffic_status [::ixia::traffic_config                              \
        -mode                   reset                                   \
        -traffic_generator      ixnetwork_540                           \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}
puts "Reset traffic ..."
update idletasks


set traffic_status [::ixia::traffic_config                              \
        -mode                   create                                  \
        -traffic_generator      ixnetwork_540                           \
        -transmit_mode          continuous                              \
        -name                   "IPv4_TRAFFIC"                          \
        -src_dest_mesh          one_to_one                              \
        -route_mesh             one_to_one                              \
        -circuit_type           none                                    \
        -circuit_endpoint_type  ipv4                                    \
        -emulation_src_handle   $ce_bgp_neighbor_handle_list            \
        -emulation_dst_handle   $pe_bgp_neighbor_handle_list            \
        -track_by               [list endpoint_pair source_ip inner_vlan]\
        -stream_packing         one_stream_per_endpoint_pair            \
        -rate_percent           10                                      \
        -tx_delay               10                                      \
        -transmit_distribution  [list endpoint_pair frame_size]         \
        -length_mode            distribution                            \
        -frame_size_distribution imix_tcp                               \
        -egress_tracking        tos_precedence                          \
        -latency_bins_enable    1                                       \
        -latency_bins           16                                      \
        -latency_values         [list 0.02 0.04 0.06 0.08 0.1  0.12 0.14\
                                      0.16 0.18 0.2  0.5  0.52 1 2 3   ]\
        -ip_precedence          [list 0 2 3 7]                          \
        -ip_precedence_mode     list                                    \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}
puts "Configured traffic ..."
update idletasks

################################################################################
# Start the traffic
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork_540                               \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

puts "Started traffic ..."
update idletasks

# return pause
after 30000


################################################################################
# Collect stats without filters
################################################################################
set traffic_stats_status_1 [::ixia::traffic_stats                           \
        -traffic_generator      ixnetwork_540                               \
        -mode                   user_defined_stats                          \
        -uds_type               l23_traffic_flow                            \
        -uds_action             get_stats                                   \
        ]
if {[keylget traffic_stats_status_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_stats_status_1 log]"
    return 0
}
foreach row_key [keylkeys traffic_stats_status_1] {
    if {![string is integer $row_key]} {continue}
    puts        "ROW: $row_key"

    foreach stat_key [keylkeys traffic_stats_status_1 $row_key] {
        switch -- $stat_key {
            "Tx Frames" {
                set tx_frames $stat_key
            }
            "Rx Frames" {
                set rx_frames $stat_key
            }
        }
        puts        "[format %50s $stat_key]: [keylget traffic_stats_status_1 $row_key.$stat_key]"
    }
}

if {[keylget traffic_stats_status_1 1.$rx_frames] == 0 || [keylget traffic_stats_status_1 1.$tx_frames] == 0} {
    puts "No frames sent or received. TX: [keylget traffic_stats_status_1 1.$tx_frames]; RX: [keylget traffic_stats_status_1 1.$rx_frames]"

}

if {[keylget traffic_stats_status_1 1.$rx_frames] < [expr [keylget traffic_stats_status_1 1.$tx_frames] * 0.95]} {
    puts "Frame loss detected. TX: [keylget traffic_stats_status_1 1.$tx_frames]; RX: [keylget traffic_stats_status_1 1.$rx_frames]"

}

puts        "Completed stats retrieval without filtering ..."

update idletasks

################################################################################
# Collect stats with port and traffic item filters
################################################################################
set traffic_filters_status [::ixia::traffic_stats                           \
        -traffic_generator      ixnetwork_540                               \
        -mode                   user_defined_stats                          \
        -uds_type               l23_traffic_flow                            \
        -uds_action             get_available_port_filters                  \
        ]
if {[keylget traffic_filters_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_filters_status log]"
    return 0
}
set port_filters_list [lindex [keylget traffic_filters_status filters] 0]

set traffic_filters_status [::ixia::traffic_stats                           \
        -traffic_generator      ixnetwork_540                               \
        -mode                   user_defined_stats                          \
        -uds_type               l23_traffic_flow                            \
        -uds_action             get_available_traffic_item_filters          \
        ]
if {[keylget traffic_filters_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_filters_status log]"
    return 0
}
set ti_filters_list [keylget traffic_filters_status filters]

foreach port_filter $port_filters_list {
    foreach ti_filter $ti_filters_list {
        puts        "PORT FILTER: $port_filter; TI filter: $ti_filter"

        set traffic_stats_status_2 [::ixia::traffic_stats                            \
                -traffic_generator       ixnetwork_540                               \
                -mode                    user_defined_stats                          \
                -uds_type                l23_traffic_flow                            \
                -uds_action              get_stats                                   \
                -uds_port_filter         $port_filter                                \
                -uds_traffic_item_filter $ti_filter                                  \
                ]
        if {[keylget traffic_stats_status_2 status] != $::SUCCESS} {
            puts "FAIL - $test_name - [keylget traffic_stats_status_2 log]"
            return 0
        }

        foreach row_key [keylkeys traffic_stats_status_2] {
            if {![string is integer $row_key]} {continue}
            puts "ROW: $row_key"

            foreach stat_key [keylkeys traffic_stats_status_2 $row_key] {
                switch -- $stat_key {
                    "Tx Frames" {
                        set tx_frames $row_key.$stat_key
                    }
                    "Rx Frames" {
                        set rx_frames $row_key.$stat_key
                    }
                }
                puts "[format %50s $stat_key]: [keylget traffic_stats_status_2 $row_key.$stat_key]"
            }

            if {[keylget traffic_stats_status_2 $rx_frames] == 0 || [keylget traffic_stats_status_2 $tx_frames] == 0} {
                puts "No frames sent or received. TX: [keylget traffic_stats_status_2 $tx_frames]; RX: [keylget traffic_stats_status_2 $rx_frames]"
            }

            if {[keylget traffic_stats_status_2 $rx_frames] < [expr [keylget traffic_stats_status_2 $tx_frames] * 0.95]} {
                puts "Frame loss detected. TX: [keylget traffic_stats_status_2 $tx_frames]; RX: [keylget traffic_stats_status_2  $rx_frames]"
            }

        }
    }
}
puts        "Completed stats retrieval with port and traffic item filtering ..."

update idletasks

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
