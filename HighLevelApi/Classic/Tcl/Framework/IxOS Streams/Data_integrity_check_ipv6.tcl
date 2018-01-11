################################################################################
# Version 1.0    $Revision: 1 $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#       07-02-2008 MGithens   - created sample
#       14-02-2008 RAntonescu - Add router solicitation check 
#       21-02-2008 Lraicea    - Updated description
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
#    This sample configures tx and rx ports for data integrity checking.       #
#    The sample requires a DUT connected to the Ixia ports, that can respond   #
#    to the router solicitation.                                               #
#    The statistics for the data integrity frames and data integrity errors    #
#    are retrieved.                                                            #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET26.                                      #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 2/1 2/2]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect   \
        -reset                        \
        -device      $chassisIP       \
        -port_list   $port_list       \
        -username    ixiaApiUser      \
        -break_locks 1                \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
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
# Set IPv6 interface parameters
################################################################################
set ipV6_mac_list               "0000.debb.0001 0000.debb.0002"
set ipV6_autoneg_list           "1              1"
set ipV6_duplex_list            "auto           auto"
set ipV6_speed_list             "auto           auto"
set ipV6_ixia_list              "4000::1        5000::1"
set ipV6_prefix_len_ixia_list   "64             64"
set port_rx_mode_list           "capture        {packet_group  data_integrity}"
set data_integrity_list         "0              1"

################################################################################
# Configure interfaces in the test IPv6
################################################################################
set interface_status [::ixia::interface_config                  \
        -port_handle                $port_handle                \
        -ipv6_intf_addr             $ipV6_ixia_list             \
        -ipv6_prefix_length         $ipV6_prefix_len_ixia_list  \
        -autonegotiation            $ipV6_autoneg_list          \
        -duplex                     $ipV6_duplex_list           \
        -src_mac_addr               $ipV6_mac_list              \
        -port_rx_mode               $port_rx_mode_list          \
        -pgid_offset                62                          \
        -data_integrity             $data_integrity_list        \
        -signature                  11223344                    \
        -signature_offset           58                          \
        -integrity_signature        a1b1c1d1                    \
        -integrity_signature_offset 54                          \
        -qos_stats                  0                           \
        -speed                      $ipV6_speed_list            \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}
################################################################################
# Delete all the streams first
################################################################################
set traffic_status [::ixia::traffic_config \
        -mode        reset                 \
        -port_handle $port_0               \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

set stream_index_list [list]
################################################################################
# Configure stream 1 - the PGID offset is 4 bytes more than the signature offset
################################################################################
set traffic_status [::ixia::traffic_config          \
        -mode                       create          \
        -port_handle                $port_0         \
        -l3_protocol                ipv6            \
        -ipv6_src_addr              4000::1         \
        -ipv6_dst_addr              5000::1         \
        -l3_length                  100             \
        -rate_percent               50              \
        -mac_dst_mode               discovery       \
        -mac_src                    0000.0005.0001  \
        -enable_data_integrity      1               \
        -signature                  11223344        \
        -signature_offset           58              \
        -integrity_signature        a1b1c1d1        \
        -integrity_signature_offset 54              \
        ]

if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

lappend stream_index_list [keylget traffic_status stream_id]
################################################################################
# Send router solicitation if there is a router to respond
################################################################################
if {0} {
    set interface_status [::ixia::interface_config \
            -port_handle              $port_0      \
            -send_router_solicitation 1            ]
    if {[keylget interface_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget interface_status log]"
        return
    }
    
    if {[catch {set failed_arp [keylget interface_status \
            $port_0.router_solicitation_success]}] || $failed_arp == 0} {
        set returnLog "FAIL - $test_name - Router Solicitation send request failed. "
        if {![catch {set intf_list [keylget interface_status $port_0.arp_ipv6_interfaces_failed]}]} {
            append returnLog "Router Solicitation failed on interfaces: $intf_list."
        }
        puts $returnLog
        return
    }
}

################################################################################
# Clear stats before sending traffic
################################################################################
set clear_stats_status [::ixia::traffic_control \
        -port_handle $port_handle               \
        -action      clear_stats                \
        ]
if {[keylget clear_stats_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget clear_stats_status log]"
    return
}
################################################################################
# Start the traffic on TX port
################################################################################
set traffic_start_status [::ixia::traffic_control   \
        -port_handle $port_0                        \
        -action      run                            \
        ]
if {[keylget traffic_start_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_start_status log]"
    return
}

# Sleep 5 seconds
ixia_sleep 5000

################################################################################
# Stop the traffic on TX port
################################################################################
set traffic_stop_status [::ixia::traffic_control    \
        -port_handle $port_0                        \
        -action      stop                           \
        ]
if {[keylget traffic_stop_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_stop_status log]"
    return
}

###############################################################################
#   Retrieve stats after stopped
###############################################################################
# Get aggregrate stats for all ports
set aggregate_stats [::ixia::traffic_stats -port_handle $port_handle]
if {[keylget aggregate_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget aggregate_stats log]"
    return
}

proc post_stats {port_handle label key_list stat_key {stream ""}} {
    puts -nonewline [format "%-25s" $label]

    foreach port $port_handle {
        if {$stream != ""} {
            set key $port.stream.$stream.$stat_key
        } else {
            set key $port.$stat_key
        }

        puts -nonewline "[format "%-40s" [keylget key_list $key]]"
    }
    puts ""
}

puts "\n\n\n#################################### STATS #####################################"
puts "[format "%30s%40s" $port_0 $port_1]"
puts "[format "%30s%40s" ----- -----]"

post_stats $port_handle "Elapsed Time"          $aggregate_stats \
        aggregate.tx.elapsed_time
post_stats $port_handle "Packets Tx"            $aggregate_stats \
        aggregate.tx.pkt_count
post_stats $port_handle "Bytes Tx"              $aggregate_stats \
        aggregate.tx.pkt_byte_count
post_stats $port_handle "Packets Rx"            $aggregate_stats \
        aggregate.rx.pkt_count
post_stats $port_handle "Bytes Rx"              $aggregate_stats \
        aggregate.rx.pkt_byte_count
post_stats $port_handle "Data Integrity Frames" $aggregate_stats \
        aggregate.rx.data_int_frames_count
post_stats $port_handle "Data Integrity Error"  $aggregate_stats \
        aggregate.rx.data_int_errors_count


foreach stream $stream_index_list {
    # Get Stats on the RX port - per stream
    set rx_stream_stats [::ixia::traffic_stats  \
            -port_handle $port_1               \
            -mode        streams                \
            -stream      $stream                \
            ]

    if {[keylget rx_stream_stats status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget rx_stream_stats log]"
        return
    }
    puts "\n\n\n####################### PER-STREAM RATE STATS - STREAM $stream ########################"
    puts "[format "%30s" $port_0]"
    puts "[format "%30s" -----]"
    post_stats $port_1 "Packets Rx" $rx_stream_stats rx.total_pkts      $stream
    post_stats $port_1 "Bytes Rx"   $rx_stream_stats rx.total_pkt_bytes $stream
    puts "******************************************************\n"
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return
