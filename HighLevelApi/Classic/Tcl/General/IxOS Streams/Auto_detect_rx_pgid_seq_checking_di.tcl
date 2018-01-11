################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2006 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    06-06-2006 LRaicea
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
#    This sample configures 2 ports with the auto detect instrumentation       #
#    feature and then creates a stream on each port.                           #
#    Bidirectional traffic is run and stats are being retrieved.               #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET26.                                      #
#                                                                              #
################################################################################
package require Ixia

set test_name [info script]
set chassisIP sylvester

################################################################################
# Interface configuration settings
################################################################################
set port_list           "3/1                         3/2"
set ixia_list           "1.1.1.1                     1.1.1.2"
set gateway_list        "1.1.1.2                     1.1.1.1"
set netmask_list        "255.255.255.0               255.255.255.0"
set mac_list            "0000.debb.0001              0000.debb.0002"
set autoneg_list        "1                              1"
set duplex_list         "full                           full"
set speed_list          "ether100                    ether100"
set port_rx_list        "auto_detect_instrumentation auto_detect_instrumentation"
set seq_checking_list   "1                           1"
set data_integrity_list "1                           1"
set signature_list      {
    {AA BB AA BB AA BB AA BB AA BB AA BB}
    {CC DD CC DD CC DD CC DD CC DD CC DD}
}
set signature_start_list "2                          2"

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect  \
        -reset                     \
        -device    $chassisIP      \
        -port_list $port_list \
        -username  ixiaApiUser     ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_one [keylget connect_status \
        port_handle.$chassisIP.[lindex $port_list 0]]
set port_two [keylget connect_status \
        port_handle.$chassisIP.[lindex $port_list 1]]

set port_handle [list $port_one $port_two]


################################################################################
# Configure interface in the test IPv4
################################################################################
set interface_status [::ixia::interface_config            \
        -port_handle            $port_handle            \
        -intf_ip_addr           $ixia_list              \
        -gateway                $gateway_list           \
        -netmask                $netmask_list           \
        -autonegotiation        $autoneg_list           \
        -duplex                 $duplex_list            \
        -src_mac_addr           $mac_list               \
        -speed                  $speed_list             \
        -port_rx_mode           $port_rx_list           \
        -signature              $signature_list         \
        -signature_start_offset $signature_start_list   \
        -sequence_checking      $seq_checking_list      \
        -data_integrity         $data_integrity_list    ]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Delete all the streams first
################################################################################
set traffic_status [::ixia::traffic_config \
        -mode        reset               \
        -port_handle $port_handle        ]

set stream_index_list ""

################################################################################
# Configure first stream on the IpV4 port
################################################################################
set traffic_status [::ixia::traffic_config         \
        -mode         create                     \
        -port_handle  $port_one                  \
        -l3_protocol  ipv4                       \
        -ip_src_addr  [lindex $ixia_list 0]      \
        -ip_dst_addr  [lindex $ixia_list 1]      \
        -l3_length    64                         \
        -rate_percent 50                         \
        -mac_dst_mode discovery                  \
        -mac_src      [lindex $mac_list 0]       \
        -enable_auto_detect_instrumentation  1   \
        -signature    [lindex $signature_list 1] \
        -frame_sequencing enable                 \
        -enable_data_integrity 1                 \
        -integrity_signature EE.AA               ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

lappend stream_index_list [keylget traffic_status stream_id]

################################################################################
# Configure second stream on the IpV4 port
################################################################################
set traffic_status [::ixia::traffic_config         \
        -mode         create                     \
        -port_handle  $port_two                  \
        -l3_protocol  ipv4                       \
        -ip_src_addr  [lindex $ixia_list 1]      \
        -ip_dst_addr  [lindex $ixia_list 0]      \
        -l3_length    64                         \
        -rate_percent 50                         \
        -mac_dst_mode discovery                  \
        -mac_src      [lindex $mac_list 1]       \
        -enable_auto_detect_instrumentation  1   \
        -signature    [lindex $signature_list 0] \
        -frame_sequencing enable                 \
        -enable_data_integrity 1                 \
        -integrity_signature EE.BB               ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

lappend stream_index_list [keylget traffic_status stream_id]

set interface_status [::ixia::interface_config  \
        -port_handle     $port_handle           \
        -arp_send_req    1                      ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

foreach port $port_handle {
    if {[catch {set failed_arp [keylget interface_status \
            $port.arp_request_success]}] || $failed_arp == 0} {
        set returnLog "FAIL - $test_name arp send request failed. "
        if {![catch {set intf_list [keylget \
            interface_status $port.arp_ipv4_interfaces_failed]}]} {
            append returnLog "ARP failed on interfaces: $intf_list."
        }
        return $returnLog
    }
}

################################################################################
# Clear stats before sending traffic
################################################################################
set clear_stats_status [::ixia::traffic_control \
        -port_handle $port_handle             \
        -action      clear_stats              ]
if {[keylget clear_stats_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget clear_stats_status log]"
}

################################################################################
# Start the traffic
################################################################################
set traffic_start_status [::ixia::traffic_control    \
        -port_handle $port_handle               \
        -action      run                        ]
if {[keylget traffic_start_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_start_status log]"
}

# Wait 15 seconds
after 15000

proc post_stats {port_handle label key_list stat_key {stream ""}} {
    puts -nonewline [format "%-32s" $label]

    foreach port $port_handle {
        if {$stream != ""} {
            set key $port.stream.$stream.$stat_key
        } else {
            set key $port.$stat_key
        }
        if {[catch {keylget key_list $key}]} {
            puts -nonewline "[format "%-16s" N/A]"
        } else  {
            puts -nonewline "[format "%-16s" [keylget key_list $key]]"
        }
        
    }
    puts ""
}


################################################################################
# Stop traffic on the TX port
################################################################################
set traffic_stop_status [::ixia::traffic_control \
        -port_handle $port_handle              \
        -action      stop                      ]
if {[keylget traffic_stop_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_stop_status log]"
}

###############################################################################
# Get aggregrate stats for all ports
###############################################################################
set aggregate_stats [::ixia::traffic_stats -port_handle $port_handle]
if {[keylget aggregate_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggregate_stats log]"
}

puts "\n\t\t########################"
puts "\t\t#  STATIC STATS        #"
puts "\t\t########################"
puts "\n******************* FINAL COUNT STATS **********************"
puts "\t\t\t\t$port_one\t\t$port_two"
puts "\t\t\t\t-----\t\t-----"

post_stats $port_handle "Elapsed Time"   $aggregate_stats \
        aggregate.tx.elapsed_time

post_stats $port_handle "Packets Tx"     $aggregate_stats \
        aggregate.tx.pkt_count

post_stats $port_handle "Raw Packets Tx" $aggregate_stats \
        aggregate.tx.raw_pkt_count

post_stats $port_handle "Bytes Tx"       $aggregate_stats \
        aggregate.tx.pkt_byte_count

post_stats $port_handle "Bits Tx"        $aggregate_stats \
        aggregate.tx.pkt_bit_count

post_stats $port_handle "Packets Rx"     $aggregate_stats \
        aggregate.rx.pkt_count

post_stats $port_handle "Raw Packets Rx" $aggregate_stats \
        aggregate.rx.raw_pkt_count

post_stats $port_handle "Collisions"     $aggregate_stats \
        aggregate.rx.collisions_count

post_stats $port_handle "Dribble Errors" $aggregate_stats \
        aggregate.rx.dribble_errors_count

post_stats $port_handle "CRCs"           $aggregate_stats \
        aggregate.rx.crc_errors_count

post_stats $port_handle "Oversizes"      $aggregate_stats \
        aggregate.rx.oversize_count

post_stats $port_handle "Undersizes"     $aggregate_stats \
        aggregate.rx.undersize_count

post_stats $port_handle "Data Integrity Frames" $aggregate_stats \
        aggregate.rx.data_int_frames_count

post_stats $port_handle "Data Integrity Error"  $aggregate_stats \
        aggregate.rx.data_int_errors_count

post_stats $port_handle "Sequence Frames"  $aggregate_stats \
        aggregate.rx.sequence_frames_count

post_stats $port_handle "Sequence Error"   $aggregate_stats \
        aggregate.rx.sequence_errors_count

puts "******************************************************\n"

################################################################################
# Get per stream stats
################################################################################
set rx_stream_stats [::ixia::traffic_stats \
        -port_handle $port_handle        \
        -mode        streams             \
        -streams     $stream_index_list     ]

foreach {stream} $stream_index_list {
    puts "\n********** PER-STREAM STATS - STREAM $stream**********"
    
    puts [format "%-15s %-15s %-15s" [string repeat " " 15] \
            $port_one $port_two]
    
    puts [format "%-15s %-15s %-15s" [string repeat " " 15] \
            [string repeat "-" 5] [string repeat "-" 5]]
    
    post_stats $port_handle "Packets Tx"    $rx_stream_stats tx.total_pkts         \
            $stream
    
    post_stats $port_handle "Time Tx"       $rx_stream_stats tx.elapsed_time         \
            $stream
    
    post_stats $port_handle "Packets Rx"    $rx_stream_stats rx.total_pkts           \
            $stream
    
    post_stats $port_handle "Bytes Rx"      $rx_stream_stats rx.total_pkt_bytes      \
            $stream
    
    post_stats $port_handle "Bits Rate"     $rx_stream_stats rx.total_pkt_bit_rate   \
            $stream
    
    post_stats $port_handle "Line Rate"     $rx_stream_stats rx.line_rate_percentage \
            $stream
    
    post_stats $port_handle "Average Delay" $rx_stream_stats rx.avg_delay            \
            $stream
    
    post_stats $port_handle "Min. Delay"    $rx_stream_stats rx.min_delay            \
            $stream
    
    post_stats $port_handle "Max. Delay"    $rx_stream_stats rx.max_delay            \
            $stream
    
    puts "******************************************************\n"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
