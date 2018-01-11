################################################################################
# Version 1.0    $Revision: 1 $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10-10-2006 dstanciu
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
#    This sample configures an IPv4 stream with packet group id and extracts   #
#    statistics including first and last timestamp.                            #
#    This sample requires a DUT.                                               #
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

set ipV4_ixia_list    "12.1.1.2          12.2.1.2"
set ipV4_gateway_list "12.1.1.1          12.2.1.1"
set ipV4_netmask_list "255.255.255.0     255.255.255.0"
set ipV4_mac_list     "0000.debb.0001    0000.debb.0002"
set ipV4_version_list "4                 4"
set ipV4_autoneg_list "1                 1"
set ipV4_duplex_list  "auto              auto"
set ipV4_speed_list   "auto              auto"
set ipV4_mode         "wide_packet_group wide_packet_group"
set ipV4_arp_list     "1                 1"
# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_list       \
        -username  ixiaApiUser      ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle_tx [keylget connect_status \
        port_handle.$chassisIP.[lindex $port_list 0]]
set port_handle_rx [keylget connect_status \
        port_handle.$chassisIP.[lindex $port_list 1]]
set port_handle [list $port_handle_tx $port_handle_rx]

################################################################################
# Configure interface in the test
################################################################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    $ipV4_ixia_list     \
        -gateway         $ipV4_gateway_list  \
        -netmask         $ipV4_netmask_list  \
        -autonegotiation $ipV4_autoneg_list  \
        -duplex          $ipV4_duplex_list   \
        -src_mac_addr    $ipV4_mac_list      \
        -speed           $ipV4_speed_list    \
        -port_rx_mode    $ipV4_mode          \
        -arp_send_req    $ipV4_arp_list      ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
################################################################################
# Delete all the streams first
################################################################################
set traffic_status [::ixia::traffic_config \
        -mode        reset                 \
        -port_handle $port_handle_tx       ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}
set traffic_status [::ixia::traffic_config \
        -mode        reset                 \
        -port_handle $port_handle_rx       ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}
################################################################################
# Configure the stream
################################################################################
set number_of_pgids 1
set traffic_status [::ixia::traffic_config \
        -mode         create               \
        -port_handle  $port_handle_tx      \
        -l3_protocol  ipv4                 \
        -ip_src_addr  12.1.1.2             \
        -ip_dst_addr  12.2.1.2             \
        -l3_length    57                   \
        -rate_percent 50                   \
        -mac_dst_mode discovery            \
        -mac_src      0000.0005.0001       \
        -enable_pgid  1                    \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

# This should be uncommented when using a valid gateway for the interface
# configured above through the interface_config call.
if {0} {
    set interface_status [::ixia::interface_config  \
            -port_handle     $port_handle_tx        \
            -arp_send_req    1                      ]
    if {[keylget interface_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget interface_status log]"
    }
    if {[catch {set failed_arp [keylget interface_status \
            $port_handle_tx.arp_request_success]}] || $failed_arp == 0} {
        set returnLog "FAIL - $test_name - ARP send request failed. "
        if {![catch {set intf_list [keylget interface_status $port_handle_tx.arp_ipv4_interfaces_failed]}]} {
            append returnLog "ARP failed on interfaces: $intf_list."
        }
        return $returnLog
    }
}
################################################################################
# Clear statistics
################################################################################
set clear_stats_status [::ixia::traffic_control \
        -port_handle    $port_handle          \
        -action         clear_stats           ]
if {[keylget clear_stats_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget clear_stats_status log]"
}

puts "Sending..."
################################################################################
# Start traffic
################################################################################
set traffic_control_status [::ixia::traffic_control \
        -port_handle $port_handle_tx              \
        -action      run                          ]
if {[keylget traffic_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_control_status log]"
}

# Sleep n seconds for traffic to run
after 5000

puts "Stop."
################################################################################
# Stop traffic
################################################################################
set traffic_control_status [::ixia::traffic_control \
        -port_handle $port_handle_tx              \
        -action      stop                         ]
if {[keylget traffic_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_control_status log]"
}

################################################################################
# Retrieve statistics
################################################################################
set pgid_statistics_list [::ixia::traffic_stats \
        -port_handle     $port_handle           \
        -packet_group_id $number_of_pgids       \
        ]
if {[keylget pgid_statistics_list status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pgid_statistics_list log]"
}
################################################################################
# Format the statistics
################################################################################
puts  "\n"
puts  "+---------------------------------------------------------------+"
puts  "+                       Statistic Results                       +"
puts  "+---------------------------------------------------------------+"
puts  [format "%8s %10s %20s %20s" \
        PGID    Port    FirstTimeStamp LastTimeStamp]
for {set pgid_index 1} {$pgid_index <= $number_of_pgids} {incr pgid_index} {
    puts  [format "%8d %10s %20.0f %20.0f" $pgid_index $port_handle_rx [keylget pgid_statistics_list \
        $port_handle_rx.pgid.$pgid_index.first_timestamp] \
        [keylget pgid_statistics_list \
        $port_handle_rx.pgid.$pgid_index.last_timestamp]]

}
###############################################################################
# Retrieve statistics after stopped
###############################################################################
# Get aggregrate stats for all ports
set aggregate_stats [::ixia::traffic_stats -port_handle $port_handle]
if {[keylget aggregate_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggregate_stats log]"
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

puts "\n\t\t########################"
puts "\t\t#  STATIC STATS        #"
puts "\t\t########################"
puts "\n******************* FINAL COUNT STATS **********************"
puts "\t\t$port_handle_tx\t\t$port_handle_rx"
puts "\t\t-----\t\t-----"

post_stats $port_handle "Elapsed Time"   $aggregate_stats \
        aggregate.tx.elapsed_time
post_stats $port_handle "Packets Tx"     $aggregate_stats aggregate.tx.pkt_count
post_stats $port_handle "Raw Packets Tx" $aggregate_stats \
        aggregate.tx.raw_pkt_count
post_stats $port_handle "Bytes Tx"       $aggregate_stats \
        aggregate.tx.pkt_byte_count
post_stats $port_handle "Packets Rx"     $aggregate_stats aggregate.rx.pkt_count
post_stats $port_handle "Raw Packets Rx" $aggregate_stats \
        aggregate.rx.raw_pkt_count
post_stats $port_handle "Collisions"     $aggregate_stats \
        aggregate.rx.collisions_count

set cleanup_status [::ixia::cleanup_session ]

if {[keylget cleanup_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget cleanup_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
