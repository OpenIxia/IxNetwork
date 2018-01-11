################################################################################
# Version 1.0    $Revision: 2 $
# $Author: Lavinia Raicea $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    13/6-2005 Lavinia Raicea
#
# Description:
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
#    This sample creates three IPv4 streams on a port, starts the streams      #
#    and displays statistics about them.                                       #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET26.                                      #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester

########
# IpV4 #
########
set ipV4_port_list    "2/1              2/2"
set ipV4_ixia_list    "1.1.1.2          1.1.1.1"
set ipV4_gateway_list "1.1.1.1          1.1.1.2"
set ipV4_netmask_list "255.255.255.0    255.255.255.0"
set ipV4_mac_list     "0000.debb.0001   0000.debb.0002"
set ipV4_version_list "4                4"
set ipV4_autoneg_list "1                1"
set ipV4_duplex_list  "full             full"
set ipV4_speed_list   "ether100         ether100"

#################################################################################
#                                START TEST                                     #
#################################################################################
# Procedures for printing stats
proc post_stats {port_handle label key_list stat_key {stream ""}} {
    puts -nonewline [format "%-16s" $label]
    
    foreach port $port_handle {
        if {$stream != ""} {
            set key $port.stream.$stream.$stat_key
        } else {
            set key $port.$stat_key
        }
        
        puts -nonewline "[format "%-16s" [keylget key_list $key]]"
    }
    puts ""
}

proc print_stats {title port_handle stat_mode key_list {stat_mode_add ""}} {
    set tx_rx_modes {tx rx}
    set aggregate_list [list \
            elapsed_time pkt_count pkt_byte_count pkt_rate pkt_bit_rate \
            datagram_byte_count  datagram_bit_rate  line_bandwidth \
            substream_count  substream_error_count   filter_count \
            total_pkts  total_pkt_bytes  good_pkts  good_pkt_bytes \
            good_datagram_bytes total_pkt_rate good_pkt_rate \
            good_pkt_bit_rate good_datagram_bit_rate line_rate_percentage \
            tcp_pkts tcp_ratio tcp_checksum_errors \
            udp_pkts udp_ratio udp_checksum_errors  icmp_pkts icmp_ratio \
            ip_pkts ip_checksum_errors ip_fragment_detected \
            avg_datagram_length min_datagram_length max_datagram_length \
            avg_pkt_length min_pkt_length max_pkt_length \
            uds1_count uds2_count pkt_bit_count \
            collisions_count collisions_rate crc_errors_count crc_errors_rate \
            dribble_errors_count dribble_errors_rate \
            oversize_count oversize_rate pkt_byte_rate uds1_rate uds2_rate    \
            undersize_count undersize_rate vlan_pkts_count vlan_pkts_rate     \
            qos0_count qos1_count qos2_count qos3_count qos4_count qos5_count \
            qos6_count qos7_count data_int_frames_count data_int_errors_count \
            ]
    
    set stream_list [list \
            elapsed_time encap all.ipv4_present all.ipv6_present     \
            all.tcp_present all.udp_present all.maxtag_present       \
            total_pkts total_pkt_bytes good_pkts good_pkt_bytes      \
            good_datagram_bytes total_pkt_rate total_pkt_bit_rate    \
            good_pkt_rate good_pkt_bit_rate good_datagram_bit_rate   \
            line_rate_percentage phy_crc_errors bad_encaps_errors    \
            bad_encaps_ratio mtu_errors ip_checksum_errors           \
            avg_pkt_length min_pkt_length max_pkt_length             \
            avg_delay min_delay max_delay lost_pkts misinserted_pkts \
            out_of_sequence_pkts lost_pkt_ratio misinserted_pkt_rate \
            out_of_sequence_pkt_ratio prbs_bit_error_rate            \
            prbs_bit_errors test_block_errors good_pkts              \
            ]
    set stat_list "${stat_mode}_list"
    if {$stat_mode_add != ""} {
        set stat_mode "${stat_mode}.${stat_mode_add}"
    }
    set table ""
    set table [append table                                \
            "\n" [format "%-105s" $title]  "\n"            \
            [format "%-105s" [string repeat "*" 105]] "\n" \
            [format "%-21s" "Stat"] "\t"]
    foreach port $port_handle {
        set table [append table [format "%-36s" "Port $port"] "\t"]
    }
    set table [append table "\n" [format "%-21s" " "] "\t"]
    foreach port $port_handle {
        set table [append table            \
                [format "%-16s" "Tx"] "\t" \
                [format "%-16s" "Rx"] "\t" ]
    }
    set table [append table "\n"]
    foreach stat [set $stat_list] {
        set line ""
        set line [append line [format "%-21s" $stat] "\t"]
        set line_content ""
        set stats_array ""
        foreach port $port_handle {
            foreach tx_rx_mode $tx_rx_modes {
                if {[regsub "^all." $stat "" stat_ignore] == 1} {
                    regsub "^all." $stat "" stat
                    set key $port.$stat_mode.$stat
                } else  {
                    set key $port.$stat_mode.$tx_rx_mode.$stat
                }
                if {[catch {keylget key_list $key}]} {
                    set stat_value "-"
                } elseif {([string first "not supported" \
                            [keylget key_list $key]] != -1) || \
                            ([keylget key_list $key] == "") } {
                    set stat_value "-"
                } else  {
                    set stat_value [keylget key_list $key]
                }
                set stats_array [append stats_array $stat_value]
                set line_content [append line_content \
                        [format "%-16s" $stat_value] "\t"]
            }
        }
        if {$stats_array != [string repeat "-" [expr \
                    [llength $port_handle] * [llength $tx_rx_modes] ]]} {
            set table [append table $line $line_content "\n"]
        }
    }
    return $table
}

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect  \
        -reset                     \
        -device    $chassisIP      \
        -port_list $ipV4_port_list \
        -username  ixiaApiUser     ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_one [keylget connect_status \
        port_handle.$chassisIP.[lindex $ipV4_port_list 0]]
set port_two [keylget connect_status \
        port_handle.$chassisIP.[lindex $ipV4_port_list 1]]

set port_handle [list $port_one $port_two]

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    $ipV4_ixia_list     \
        -gateway         $ipV4_gateway_list  \
        -netmask         $ipV4_netmask_list  \
        -autonegotiation $ipV4_autoneg_list  \
        -duplex          $ipV4_duplex_list   \
        -src_mac_addr    $ipV4_mac_list      \
        -speed           $ipV4_speed_list    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

########################################
# Stream configuration                 #
# IPv4                                 #
########################################
# Delete all the streams from the first port
set traffic_status [::ixia::traffic_config \
        -mode        reset               \
        -port_handle $port_one           \
        ]

# Delete all the streams from the second port
set traffic_status [::ixia::traffic_config \
        -mode        reset               \
        -port_handle $port_two           \
        ]

set stream_index_list ""

# Configure first stream on the IpV4 port
set traffic_status [::ixia::traffic_config         \
        -mode         create                     \
        -port_handle  $port_one                  \
        -l3_protocol  ipv4                       \
        -ip_src_addr  [lindex $ipV4_ixia_list 0] \
        -ip_dst_addr  [lindex $ipV4_ixia_list 1] \
        -l3_length    46                         \
        -rate_percent 50                         \
        -mac_dst_mode discovery                  \
        -mac_src      [lindex $ipV4_mac_list 0]  ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

lappend stream_index_list [keylget traffic_status stream_id]

# Configure second stream on the IpV4 port
set traffic_status [::ixia::traffic_config         \
        -mode         create                     \
        -port_handle  $port_one                  \
        -l3_protocol  ipv4                       \
        -ip_src_addr  [lindex $ipV4_ixia_list 0] \
        -ip_dst_addr  [lindex $ipV4_ixia_list 1] \
        -l3_length    54                         \
        -rate_percent 50                         \
        -mac_dst_mode discovery                  \
        -mac_src      [lindex $ipV4_mac_list 0]  ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

lappend stream_index_list [keylget traffic_status stream_id]

# Configure third stream on the IpV4 port
set traffic_status [::ixia::traffic_config         \
        -mode         create                     \
        -port_handle  $port_one                  \
        -l3_protocol  ipv4                       \
        -ip_src_addr  [lindex $ipV4_ixia_list 0] \
        -ip_dst_addr  [lindex $ipV4_ixia_list 1] \
        -l3_length    65                         \
        -rate_percent 50                         \
        -mac_dst_mode discovery                  \
        -mac_src      [lindex $ipV4_mac_list 0]  ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

lappend stream_index_list [keylget traffic_status stream_id]

set interface_status [::ixia::interface_config  \
        -port_handle     $port_one           \
        -arp_send_req    1                      ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
if {[catch {set failed_arp [keylget interface_status \
        $port_one.arp_request_success]}] || $failed_arp == 0} {
    set returnLog "FAIL - $test_name arp send request failed. "
    if {![catch {set intf_list [keylget interface_status \
            $port_one.arp_ipv4_interfaces_failed]}]} {
        append returnLog "ARP failed on interfaces: $intf_list."
    }
    return $returnLog
}

########################################
# Traffic control                      #
########################################

# Clear stats before sending traffic
set clear_stats_status [::ixia::traffic_control \
        -port_handle $port_handle             \
        -action      clear_stats              ]
if {[keylget clear_stats_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget clear_stats_status log]"
}

# Start the traffic on TX port
set traffic_start_status [::ixia::traffic_control \
        -port_handle $port_one                  \
        -action      run                        ]
if {[keylget traffic_start_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_start_status log]"
}

# Sleep 5 seconds
ixia_sleep 5000

###############################################################################
#   Retrieve stats while running
###############################################################################

# Get aggregrate stats for all ports
set aggregate_stats [::ixia::traffic_stats -port_handle $port_handle]
if {[keylget aggregate_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggregate_stats log]"
}

# Get TX - RX stats - per stream
set stream_stats [::ixia::traffic_stats    \
        -port_handle $port_handle        \
        -mode        stream              ]
if {[keylget stream_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget stream_stats log]"
}


puts [print_stats \
        "******************** RUNNING STATS *********************" \
        $port_handle aggregate $aggregate_stats ]
        
foreach stream $stream_index_list {
    puts [print_stats \
            "******************** RUNNING TX-RX STATS PER-STREAM $stream " \
            $port_handle stream $stream_stats $stream]
}
ixia_sleep 8000

# Stop traffic on the TX port
set traffic_stop_status [::ixia::traffic_control \
    -port_handle $port_one                 \
    -action      stop                      ]
if {[keylget traffic_stop_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_stop_status log]"
}

###############################################################################
#   Retrieve stats after stopped
###############################################################################
# Get aggregrate stats for all ports
set aggregate_stats [::ixia::traffic_stats -port_handle $port_handle]
if {[keylget aggregate_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggregate_stats log]"
}

puts [print_stats \
        "******************** STATIC STATS *********************" \
        $port_handle aggregate $aggregate_stats ]

foreach stream $stream_index_list {
    # Get Stats on the RX port - per stream
    set rx_stream_stats [::ixia::traffic_stats \
            -port_handle $port_handle           \
            -mode        stream              \
            -streams     $stream             ]

    puts [print_stats \
            "********** PER-STREAM RX STATS - STREAM $stream**********" \
            $port_handle stream $rx_stream_stats $stream]
}

# Clean up the connection
set cleanup_status [::ixia::cleanup_session \
        -port_handle $port_handle         ]
if {[keylget cleanup_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget cleanup_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
