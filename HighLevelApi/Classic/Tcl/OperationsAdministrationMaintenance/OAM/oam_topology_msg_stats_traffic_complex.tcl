################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mircea Hasegan $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    03-19-2009 Mircea Hasegan
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
#    This sample creates a BACK-TO-BACK setup using the IxNetwork              #
#    implementation of Ethernet OAM.                                           #
#                                                                              #
#    It configures two Ethernet OAM Bridges, one on each Ixia port.            #
#    Each OAM Bridge two MD Levels 4 and 7.                                    #
#    MD Level 4 will have 5 MEPs.                                              #
#    MD Level 7 will have 10 MEPs.                                             #
#    Loopback messages are configured on MD Level 4 of each bridge.            #
#    Linktrace messages are configured on MD Level 7 of each bridge.           #
#    Traffic is configured for each MD Level.                                  #
#    OAM is started and statistics are gathered.                               #
#    Traffic is started and statistics are gathered.                           #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 2/3 2/4]


# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                 \
        -reset                                      \
        -ixnetwork_tcl_server       localhost       \
        -device                     $chassisIP      \
        -port_list                  $port_list      \
        -username  ixiaApiUser      ]
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

puts "Ixia port handles are $port_handle "

set interface_status [::ixia::interface_config \
        -port_handle      $port_0              \
        -mode             config               \
        -speed            auto                 \
        -duplex           auto                 \
        -phy_mode         copper               \
        -autonegotiation  1                    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
    
}

set interface_status [::ixia::interface_config \
        -port_handle      $port_1              \
        -mode             config               \
        -speed            auto                 \
        -duplex           auto                 \
        -phy_mode         copper               \
        -autonegotiation  1                    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
    
}

puts "\nReset OAM topologies on ports $port_0 and $port_1"

#
# Reset any OAM topology that may exist on port_0
#
set oam_topology_status [::ixia::emulation_oam_config_topology                  \
         -mode                        reset                                     \
         -port_handle                 $port_0                                   \
    ]
if {[keylget oam_topology_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget oam_topology_status log]"
    
}

#
# Reset any OAM topology that may exist on port_1
#
set oam_topology_status [::ixia::emulation_oam_config_topology                  \
         -mode                        reset                                     \
         -port_handle                 $port_1                                   \
    ]
if {[keylget oam_topology_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget oam_topology_status log]"
    
}

puts "\nConfigure OAM Topology on port $port_0 MD Level 4"

#
# Configure OAM Topology on first port: 5 MEPs on MD Level 4.
# Traffic endpoint handles will be returned as keyed list.
#
set t0 [::ixia::emulation_oam_config_topology \
        -mode create                          \
        -port_handle            $port_0       \
        -count                  1             \
        -md_level               4             \
        -md_name                dom4          \
        -short_ma_name_format   char_str      \
        -continuity_check                     \
        -vlan_id                100           \
        -short_ma_name_value    "?"           \
        -short_ma_name_wildcard 1             \
        -short_ma_name_length   1             \
        -short_ma_name_wc_start 3             \
        -mep_count              5             \
        -mep_id                 105           \
        -mip_count              0             \
        -mac_local_incr_mode    increment     \
        -mep_id_incr_mode       increment     \
    ]
if {[keylget t0 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget t0 log]"
    
}
set topo_h_p0_0     [keylget t0 handle         ]
set traffic_ep_p0_0 [keylget t0 traffic_handles]

puts "Topology handle is $topo_h_p0_0"

puts "\nConfigure OAM Topology on port $port_0 MD Level 7"
#
# Configure OAM Topology on first port: 10 MEPs on MD Level 7.
# Traffic endpoint handles will be returned as array.
#
set t1 [::ixia::emulation_oam_config_topology   \
        -mode                   create          \
        -port_handle            $port_0         \
        -count                  1               \
        -md_level               7               \
        -md_name                dom7            \
        -short_ma_name_format   char_str        \
        -continuity_check                       \
        -vlan_id                115             \
        -short_ma_name_value    "?"             \
        -short_ma_name_wildcard 1               \
        -short_ma_name_length   1               \
        -short_ma_name_wc_start 8               \
        -mep_count              10              \
        -mep_id                 115             \
        -mip_count              0               \
        -mac_local_incr_mode    increment       \
        -mep_id_incr_mode       increment       \
        -return_method          array           \
    ]
if {[keylget t1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget t1 log]"
    
}
set topo_h_p0_1     [keylget t1 handle]

puts "Topology handle is $topo_h_p0_1"

set array_name [keylget t1 traffic_handles_array]
foreach idx [array names $array_name] {
    lappend traffic_ep_p0_1 [set [subst $array_name]($idx)]
}

puts "\nConfigure OAM Topology on port $port_1 MD Level 4"

#
# Configure OAM Topology on second port: 5 MEPs on MD Level 4.
# Traffic endpoint handles will be returned as keyed list.
#
set t2 [::ixia::emulation_oam_config_topology \
        -mode create                          \
        -port_handle            $port_1       \
        -count                  1             \
        -md_level               4             \
        -md_name                dom4          \
        -short_ma_name_format   char_str      \
        -continuity_check                     \
        -vlan_id                100           \
        -short_ma_name_value    "?"           \
        -short_ma_name_wildcard 1             \
        -short_ma_name_length   1             \
        -short_ma_name_wc_start 3             \
        -mep_count              5             \
        -mep_id                 205           \
        -mip_count              0             \
        -mac_local_incr_mode    increment     \
        -mep_id_incr_mode       increment     \
    ]
if {[keylget t2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget t2 log]"
    
}
set topo_h_p1_0     [keylget t2 handle         ]
puts "Topology handle is $topo_h_p1_0"
set traffic_ep_p1_0 [keylget t2 traffic_handles]

puts "\nConfigure OAM Topology on port $port_1 MD Level 7"

#
# Configure OAM Topology on second port: 10 MEPs on MD Level 7.
# Traffic endpoint handles will be returned as array.
#
set t3 [::ixia::emulation_oam_config_topology   \
        -mode                   create          \
        -port_handle            $port_1         \
        -count                  1               \
        -md_level               7               \
        -md_name                dom7            \
        -short_ma_name_format   char_str        \
        -continuity_check                       \
        -vlan_id                115             \
        -short_ma_name_value    "?"             \
        -short_ma_name_wildcard 1               \
        -short_ma_name_length   1               \
        -short_ma_name_wc_start 8               \
        -mep_count              10              \
        -mep_id                 215             \
        -mip_count              0               \
        -mac_local_incr_mode    increment       \
        -mep_id_incr_mode       increment       \
        -return_method          array           ]
if {[keylget t3 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget t3 log]"
    
}
set topo_h_p1_1     [keylget t3 handle]
puts "Topology handle is $topo_h_p1_1"
set array_name [keylget t3 traffic_handles_array]
foreach idx [array names $array_name] {
    lappend traffic_ep_p1_1 [set [subst $array_name]($idx)]
}

puts "\nReset OAM Messages on ports $port_0 and $port_1"
#
# Reset OAM messages on port_0
#
set oam_msg_status [::ixia::emulation_oam_config_msg   \
         -mode                        reset            \
         -port_handle                 $port_0          \
    ]
if {[keylget oam_msg_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget oam_msg_status log]"
    
}

#
# Reset OAM message on port_1
#
set oam_msg_status [::ixia::emulation_oam_config_msg    \
         -mode                        reset             \
         -port_handle                 $port_1           \
    ]
if {[keylget oam_msg_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget oam_msg_status log]"
    
}

puts "\nConfigure Loopback messages on MD Level 4 port $port_0"
#
# Configure OAM Loopback messages on all MEPs from the first port on MD Level 4
# Return a message handle for each message configured (-handle_granularity per_message)
#
set msg_status [::ixia::emulation_oam_config_msg      \
        -mode                   create                \
        -port_handle            $port_0               \
        -md_level               4                     \
        -msg_type               loopback              \
        -msg_timeout            13000                 \
        -mac_remote_incr_mode   list                  \
        -mac_remote_list        "all"                 \
        -renew_test_msgs                              \
        -renew_period           30000                 \
        -handle_granularity     per_message           \
    ]
if {[keylget msg_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget msg_status log]"
}
set msg_h_p0_0 [keylget msg_status handle]
puts "Message handles are $msg_h_p0_0"

puts "\nConfigure Loopback messages on MD Level 7 port $port_0"
#
# Configure OAM Linktrace messages on all MEPs from the first port on MD Level 7
# Return a message handle all messages configured (-handle_granularity per_group)
#
set msg_status [::ixia::emulation_oam_config_msg      \
        -mode                   create                \
        -port_handle            $port_0               \
        -md_level               7                     \
        -msg_type               linktrace             \
        -msg_timeout            13000                 \
        -mac_remote_incr_mode   list                  \
        -mac_remote_list        "all"                 \
        -renew_test_msgs                              \
        -renew_period           30000                 \
        -handle_granularity     per_group             \
    ]
if {[keylget msg_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget msg_status log]"
}
set msg_h_p0_1 [keylget msg_status handle]
puts "Group message handle is msg_h_p0_1"

puts "\nConfigure Loopback messages on MD Level 4 port $port_1"
#
# Configure OAM Loopback messages on all MEPs from the second port on MD Level 4
# Return a message handle for each message configured (-handle_granularity per_message)
#
set msg_status [::ixia::emulation_oam_config_msg      \
        -mode                   create                \
        -port_handle            $port_1               \
        -md_level               4                     \
        -msg_type               loopback              \
        -msg_timeout            13000                 \
        -mac_remote_incr_mode   list                  \
        -mac_remote_list        "all"                 \
        -renew_test_msgs                              \
        -renew_period           30000                 \
        -handle_granularity     per_message           \
    ]
if {[keylget msg_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget msg_status log]"
}
set msg_h_p1_0 [keylget msg_status handle]
puts "Message handles are $msg_h_p1_0"

puts "\nConfigure Loopback messages on MD Level 7 port $port_1"
#
# Configure OAM Linktrace messages on all MEPs from the second port on MD Level 7
# Return a message handle all messages configured (-handle_granularity per_group)
#
set msg_status [::ixia::emulation_oam_config_msg      \
        -mode                   create                \
        -port_handle            $port_1               \
        -md_level               7                     \
        -msg_type               linktrace             \
        -msg_timeout            13000                 \
        -mac_remote_incr_mode   list                  \
        -mac_remote_list        "all"                 \
        -renew_test_msgs                              \
        -renew_period           30000                 \
        -handle_granularity     per_group             \
    ]
if {[keylget msg_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget msg_status log]"
}
set msg_h_p1_1 [keylget msg_status handle]
puts "Group message handle is msg_h_p1_1"

puts "\nStart OAM Emulation"
#
# Start OAM
#
set ctrl_status [::ixia::emulation_oam_control        \
        -action start                                 \
        -port_handle [list $port_0 $port_1]           \
    ]
if {[keylget ctrl_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ctrl_status log]"
}

after 30000

#
# Get OAM Topology Session statistics for the topology handles on MD Level 4 (both ports).
# Return the statistics in keyed list.
#
set ret_list [::ixia::emulation_oam_info                     \
        -mode               session                          \
        -action             get_topology_stats               \
        -handle             [list $topo_h_p0_0 $topo_h_p1_0] \
    ]
if {[keylget ret_list status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ret_list log]"
}

foreach top_handle [list $topo_h_p0_0 $topo_h_p1_0] {
    puts "\nStatistics for Topology handle $top_handle"
    if {[catch {keylkeys ret_list $top_handle.md_level}]} {
        return "FAIL - $test_name - Topology Sesssion statistics are not available for\
                topology handle $top_handle"
    }
    foreach md_level [keylkeys ret_list $top_handle.md_level] {
        puts "\tMD Level $md_level"
        foreach mac_addr [keylkeys ret_list $top_handle.md_level.$md_level.mac] {
            puts "\t\tMAC Address $mac_addr"
            foreach key [keylkeys ret_list $top_handle.md_level.$md_level.mac.$mac_addr] {
                puts [format {%-24s%-26s%s} "" "$key " [keylget ret_list $top_handle.md_level.$md_level.mac.$mac_addr.$key]]
            }
        }
    }
}

#
# Get OAM Topology Session statistics for the topology handles on MD Level 7 (both ports).
# Return the statistics in array.
#
set ret_list [::ixia::emulation_oam_info                     \
        -mode               session                          \
        -action             get_topology_stats               \
        -handle             [list $topo_h_p0_1 $topo_h_p1_1] \
        -return_method      array                            \
    ]
if {[keylget ret_list status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ret_list log]"
}

set array_name [keylget ret_list handle]

foreach top_handle [list $topo_h_p0_1 $topo_h_p1_1] {
    
    puts "\nStatistics for Topology handle $top_handle"
    puts "\tMD Level 7"
    
    set mac_addr_list ""
    
    foreach mac_arr_idx [array names $array_name $topo_h_p0_1.md_level.7.mac*] {
        if {[regexp "($topo_h_p0_1\.md_level\.7\.mac\.)(\[:0-9a-fA-F\]+)(.*)$" $mac_arr_idx \
                dummy0 dummy1 mac_addr dummy2]} {
        
            if {[lsearch $mac_addr_list $mac_addr] == -1} {
                lappend mac_addr_list $mac_addr
            }
        
        }
    }
    
    foreach unique_mac_addr $mac_addr_list {
        puts "\t\tMAC Address $mac_addr"
        foreach key_idx [array names $array_name $topo_h_p0_1.md_level.7.mac.$unique_mac_addr.*] {

            if {[regexp "($topo_h_p0_1\.md_level\.7\.mac\.$unique_mac_addr\.)(.*)$" $key_idx \
                    dummy0 dummy1 key_name dummy2]} {
             
                set key_value [set [subst $array_name]($key_idx)]
                puts [format {%-24s%-26s%s} "" $key_name $key_value]
            
            }
        }
    }
}


#
# Get OAM Message Session statistics for the group message handles configured on MD Level 7 (both ports)
# Return the statistics in keyed list.
#

set ret_list [::ixia::emulation_oam_info        \
        -mode session                           \
        -action get_message_stats               \
        -handle [list $msg_h_p0_1 $msg_h_p1_1]  \
    ]
if {[keylget ret_list status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ret_list log]"
}

foreach msg_handle [list $msg_h_p0_1 $msg_h_p1_1] {
    puts "\nStatistics for Message handle $msg_handle - "
    foreach msg_type [keylkeys ret_list $msg_handle] {
        puts "\t$msg_type"
        foreach stat_key [keylkeys ret_list $msg_handle.$msg_type] {
            puts [format {%-16s%-36s%-s} "" $stat_key [keylget ret_list $msg_handle.$msg_type.$stat_key]]
        }
    }
}

#
# Get OAM Message Session statistics for the per_message message handles configured on MD Level 4
# Use one message handle from the first port and one from the second port
# Return the statistics in array.
#
set msg_list [list [lindex $msg_h_p0_0 0] [lindex $msg_h_p1_0 0]]
set ret_list [::ixia::emulation_oam_info \
        -mode           session          \
        -action         get_message_stats\
        -handle         $msg_list        \
        -return_method  array            \
    ]
if {[keylget ret_list status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ret_list log]"
}

set array_name [keylget ret_list handle]

foreach msg_handle $msg_list {
    puts "\nStatistics for Message handle $msg_handle - loopback"
    foreach idx [array names $array_name $msg_handle.loopback*] {
        if {[regexp "($msg_handle\.loopback\.)(.*)$" $idx dummy0 dummy1 key_name]} {
            set key_value [set [subst $array_name]($idx)]
            puts [format {%-16s%-36s%-s} "" $key_name $key_value]
        }
    }
}


puts "\nConfigure traffic on MD Level 4 for the first two MEPs on each port"
#
# Configure traffic on MD Level 4 from the first two MEPs on the first port
# to the first two MEPs on the second port
#
set traffic_status [::ixia::traffic_config         \
        -mode                        create        \
        -traffic_generator           ixnetwork     \
        -bidirectional               0             \
        -emulation_dst_handle        [lrange $traffic_ep_p1_0 0 1]       \
        -emulation_src_handle        [lrange $traffic_ep_p0_0 0 1]       \
        -circuit_endpoint_type       ethernet_vlan  \
        -circuit_type                none           \
        -track_by                    endpoint_pair  \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

puts "\nConfigure traffic on MD Level 7 for the first two MEPs on each port"
#
# Configure traffic on MD Level 7 from the first two MEPs on the first port
# to the first two MEPs on the second port
#
set traffic_status [::ixia::traffic_config         \
        -mode                        create        \
        -traffic_generator           ixnetwork     \
        -bidirectional               0             \
        -emulation_dst_handle        [lrange $traffic_ep_p1_1 0 1]       \
        -emulation_src_handle        [lrange $traffic_ep_p0_1 0 1]       \
        -circuit_endpoint_type       ethernet_vlan  \
        -circuit_type                none           \
        -track_by                    endpoint_pair  \
    ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Start the traffic                                                            #
################################################################################
puts "\nStart OAM Traffic"
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

puts "\nGet traffic statistics"
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
foreach port $port_handle {
    puts "Port $port:"
    set streams [keylget stream_traffic_status \
            $port.stream]
    foreach stream [keylkeys streams] {
        set stream_key [keylget stream_traffic_status \
                $port.stream.$stream]
        foreach dir [keylkeys stream_key] {
            puts "\tStream $stream - $dir:"
            foreach {name key} [subst $[subst stream_${dir}_results]] {
                puts "\t\t$name: [keylget stream_traffic_status\
                        $port.stream.$stream.$dir.$key]"
            }
        }
    }
}

puts "\nStop OAM Traffic"
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

puts "\nStop OAM Emulation"
#
# Stop OAM
#
set ctrl_status [::ixia::emulation_oam_control        \
        -action      stop                             \
        -port_handle [list $port_0 $port_1]           \
    ]
if {[keylget ctrl_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ctrl_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
