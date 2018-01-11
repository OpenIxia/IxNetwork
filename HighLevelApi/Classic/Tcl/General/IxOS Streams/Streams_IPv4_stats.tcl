################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Karim $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    4-25-2003 Karim
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
#    This sample creates three IPv4 streams on a port,  starts the streams     #
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
set ipV4_port_list    "2/3            2/4"
set ipV4_ixia_list    "1.1.1.2        1.1.1.1"
set ipV4_gateway_list "1.1.1.1        1.1.1.2"
set ipV4_netmask_list "255.255.255.0  255.255.255.0"
set ipV4_mac_list     "0000.debb.0001 0000.debb.0002"
set ipV4_version_list "4                 4"
set ipV4_autoneg_list "1                 1"
set ipV4_duplex_list  "full              full"
set ipV4_speed_list   "ether100       ether100"

#################################################################################
#                                START TEST                                     #
#################################################################################

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
# Delete all the streams first
set traffic_status [::ixia::traffic_config \
        -mode        reset               \
        -port_handle $port_handle        ]

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
        -port_handle     $port_one              \
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
set traffic_start_status [::ixia::traffic_control    \
        -port_handle $port_one                  \
        -action      sync_run                        ]
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

# Get rateStats on the RX port - per stream
set rx_stream_stats [::ixia::traffic_stats \
        -port_handle $port_two           \
        -mode        streams             \
        -stream      [lindex $stream_index_list 0]]
if {[keylget rx_stream_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rx_stream_stats log]"
}

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

puts "\n******************* RUNNING COUNT STATS **********************"
puts "\t\t$port_one\t\t$port_two"
puts "\t\t-----\t\t-----"

post_stats $port_handle "Elapsed Time"   $aggregate_stats \
        aggregate.tx.elapsed_time
post_stats $port_handle "Packets Tx"     $aggregate_stats aggregate.tx.pkt_count
post_stats $port_handle "Raw Packets Tx" $aggregate_stats \
        aggregate.tx.raw_pkt_count
post_stats $port_handle "Bytes Tx"       $aggregate_stats \
        aggregate.tx.pkt_byte_count
post_stats $port_handle "Bits Tx"        $aggregate_stats \
        aggregate.tx.pkt_bit_count
post_stats $port_handle "Packets Rx"     $aggregate_stats aggregate.rx.pkt_count
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
post_stats $port_handle "RX PCKTS TOS0"  $aggregate_stats aggregate.rx.qos0_count
post_stats $port_handle "RX PCKTS TOS1"  $aggregate_stats aggregate.rx.qos1_count
post_stats $port_handle "RX PCKTS TOS2"  $aggregate_stats aggregate.rx.qos2_count
post_stats $port_handle "RX PCKTS TOS3"  $aggregate_stats aggregate.rx.qos3_count
post_stats $port_handle "RX PCKTS TOS4"  $aggregate_stats aggregate.rx.qos4_count
post_stats $port_handle "RX PCKTS TOS5"  $aggregate_stats aggregate.rx.qos5_count
post_stats $port_handle "RX PCKTS TOS6"  $aggregate_stats aggregate.rx.qos6_count
post_stats $port_handle "RX PCKTS TOS7"  $aggregate_stats aggregate.rx.qos7_count
puts "******************************************************\n"

puts "\n******************* RUNNING RATE STATS ***********************"
puts "\t\t$port_one\t\t$port_two"
puts "\t\t-----\t\t-----"
post_stats $port_handle "Packets Tx"     $aggregate_stats aggregate.tx.pkt_rate
post_stats $port_handle "Raw Packets Tx" $aggregate_stats \
        aggregate.tx.raw_pkt_rate
post_stats $port_handle "Bytes Tx"       $aggregate_stats \
        aggregate.tx.pkt_byte_rate
post_stats $port_handle "Bits Tx"        $aggregate_stats \
        aggregate.tx.pkt_bit_rate
post_stats $port_handle "Packets Rx"     $aggregate_stats aggregate.rx.pkt_rate
post_stats $port_handle "Raw Packets Rx" $aggregate_stats \
        aggregate.rx.raw_pkt_rate
post_stats $port_handle "Collisions"     $aggregate_stats \
        aggregate.rx.collisions_rate
post_stats $port_handle "Dribble Errors" $aggregate_stats \
        aggregate.rx.dribble_errors_rate
post_stats $port_handle "CRCs"           $aggregate_stats \
        aggregate.rx.crc_errors_rate
post_stats $port_handle "Oversizes"      $aggregate_stats \
        aggregate.rx.oversize_rate
post_stats $port_handle "Undersizes"     $aggregate_stats \
        aggregate.rx.undersize_rate
post_stats $port_handle "RX PCKTS TOS0"  $aggregate_stats aggregate.rx.qos0_rate
post_stats $port_handle "RX PCKTS TOS1"  $aggregate_stats aggregate.rx.qos1_rate
post_stats $port_handle "RX PCKTS TOS2"  $aggregate_stats aggregate.rx.qos2_rate
post_stats $port_handle "RX PCKTS TOS3"  $aggregate_stats aggregate.rx.qos3_rate
post_stats $port_handle "RX PCKTS TOS4"  $aggregate_stats aggregate.rx.qos4_rate
post_stats $port_handle "RX PCKTS TOS5"  $aggregate_stats aggregate.rx.qos5_rate
post_stats $port_handle "RX PCKTS TOS6"  $aggregate_stats aggregate.rx.qos6_rate
post_stats $port_handle "RX PCKTS TOS7"  $aggregate_stats aggregate.rx.qos7_rate
puts "******************************************************"

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

puts "\n\t\t########################"
puts "\t\t#  STATIC STATS        #"
puts "\t\t########################"
puts "\n******************* FINAL COUNT STATS **********************"
puts "\t\t$port_one\t\t$port_two"
puts "\t\t-----\t\t-----"

post_stats $port_handle "Elapsed Time"   $aggregate_stats \
        aggregate.tx.elapsed_time
post_stats $port_handle "Packets Tx"     $aggregate_stats aggregate.tx.pkt_count
post_stats $port_handle "Raw Packets Tx" $aggregate_stats \
        aggregate.tx.raw_pkt_count
post_stats $port_handle "Bytes Tx"       $aggregate_stats \
        aggregate.tx.pkt_byte_count
post_stats $port_handle "Bits Tx"        $aggregate_stats \
        aggregate.tx.pkt_bit_count
post_stats $port_handle "Packets Rx"     $aggregate_stats aggregate.rx.pkt_count
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
post_stats $port_handle "RX PCKTS TOS0"  $aggregate_stats aggregate.rx.qos0_count
post_stats $port_handle "RX PCKTS TOS1"  $aggregate_stats aggregate.rx.qos1_count
post_stats $port_handle "RX PCKTS TOS2"  $aggregate_stats aggregate.rx.qos2_count
post_stats $port_handle "RX PCKTS TOS3"  $aggregate_stats aggregate.rx.qos3_count
post_stats $port_handle "RX PCKTS TOS4"  $aggregate_stats aggregate.rx.qos4_count
post_stats $port_handle "RX PCKTS TOS5"  $aggregate_stats aggregate.rx.qos5_count
post_stats $port_handle "RX PCKTS TOS6"  $aggregate_stats aggregate.rx.qos6_count
post_stats $port_handle "RX PCKTS TOS7"  $aggregate_stats aggregate.rx.qos7_count
puts "******************************************************\n"

puts "\n******************* FINAL RATE STATS ***********************"
puts "\t\t$port_one\t\t$port_two"
puts "\t\t-----\t\t-----"
post_stats $port_handle "Packets Tx"     $aggregate_stats aggregate.tx.pkt_rate
post_stats $port_handle "Raw Packets Tx" $aggregate_stats \
        aggregate.tx.raw_pkt_rate
post_stats $port_handle "Bytes Tx"       $aggregate_stats \
        aggregate.tx.pkt_byte_rate
post_stats $port_handle "Bits Tx"        $aggregate_stats \
        aggregate.tx.pkt_bit_rate
post_stats $port_handle "Packets Rx"     $aggregate_stats aggregate.rx.pkt_rate
post_stats $port_handle "Raw Packets Rx" $aggregate_stats \
        aggregate.rx.raw_pkt_rate
post_stats $port_handle "Collisions"     $aggregate_stats \
        aggregate.rx.collisions_rate
post_stats $port_handle "Dribble Errors" $aggregate_stats \
        aggregate.rx.dribble_errors_rate
post_stats $port_handle "CRCs"           $aggregate_stats \
        aggregate.rx.crc_errors_rate
post_stats $port_handle "Oversizes"      $aggregate_stats \
        aggregate.rx.oversize_rate
post_stats $port_handle "Undersizes"     $aggregate_stats \
        aggregate.rx.undersize_rate
post_stats $port_handle "RX PCKTS TOS0"  $aggregate_stats aggregate.rx.qos0_rate
post_stats $port_handle "RX PCKTS TOS1"  $aggregate_stats aggregate.rx.qos1_rate
post_stats $port_handle "RX PCKTS TOS2"  $aggregate_stats aggregate.rx.qos2_rate
post_stats $port_handle "RX PCKTS TOS3"  $aggregate_stats aggregate.rx.qos3_rate
post_stats $port_handle "RX PCKTS TOS4"  $aggregate_stats aggregate.rx.qos4_rate
post_stats $port_handle "RX PCKTS TOS5"  $aggregate_stats aggregate.rx.qos5_rate
post_stats $port_handle "RX PCKTS TOS6"  $aggregate_stats aggregate.rx.qos6_rate
post_stats $port_handle "RX PCKTS TOS7"  $aggregate_stats aggregate.rx.qos7_rate
puts "******************************************************"

foreach stream $stream_index_list {
    # Get Stats on the RX port - per stream
    set rx_stream_stats [::ixia::traffic_stats \
            -port_handle $port_two            \
            -mode        streams             \
            -stream      $stream             ]

    puts "\n********** PER-STREAM RATE STATS - STREAM $stream**********"
    puts "\t\t$port_two"
    puts "\t\t-----"
    post_stats $port_two "Packets Rx"    $rx_stream_stats rx.total_pkts         \
            $stream
    post_stats $port_two "Bytes Rx"      $rx_stream_stats rx.total_pkt_bytes    \
            $stream
    post_stats $port_two "Bits Rate"     $rx_stream_stats rx.total_pkt_bit_rate \
            $stream
    post_stats $port_two "Line Rate"     $rx_stream_stats \
            rx.line_rate_percentage  $stream
    post_stats $port_two "Average Delay" $rx_stream_stats rx.avg_delay          \
            $stream
    post_stats $port_two "Min. Delay"    $rx_stream_stats rx.min_delay          \
            $stream
    post_stats $port_two "Max. Delay"    $rx_stream_stats rx.max_delay          \
            $stream
    puts "******************************************************\n"
}

# Clean up the connection
set cleanup_status [::ixia::cleanup_session \
        -port_handle $port_handle         ]
if {[keylget cleanup_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget cleanup_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
