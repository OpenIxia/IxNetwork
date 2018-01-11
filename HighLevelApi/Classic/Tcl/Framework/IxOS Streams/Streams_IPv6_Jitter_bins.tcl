################################################################################
# Version 1.0    $Revision: 1 $
# $Author: L.Raicea $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    11-14-2005 L.Raicea    - Added the jitter bin stats.
#    14-02-2008 R.Antonescu - Added router solicitation check 
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
#    This sample creates two IPv6 VLAN streams, starts the streams and         #
#    displays jitter statistics.                                               #
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
set connect_status [::ixia::connect       \
        -reset                            \
        -device      $chassisIP           \
        -port_list   $port_list           \
        -username    ixiaApiUser          \
        -break_locks 1                    \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
}

set port_0 [keylget connect_status \
        port_handle.$chassisIP.[lindex $port_list 0]]
set port_1 [keylget connect_status \
        port_handle.$chassisIP.[lindex $port_list 1]]
set port_handle [list $port_0 $port_1]

################################################################################
# Set IPv6 parameters
################################################################################
set ipV6_ixia_list    "1::1           1::2"
set ipV6_mac_list     "0000.debb.0001 0000.debb.0002"
set ipV6_version_list "4              4"
set ipV6_autoneg_list "1              1"
set ipV6_duplex_list  "auto           auto"
set ipV6_speed_list   "auto           auto"
set ipV6_sgn_list     "64             64"
set ipV6_pgid_list    "68             68"

################################################################################
# Configure interface in the test
################################################################################
set interface_status [::ixia::interface_config  \
        -port_handle      $port_handle          \
        -ipv6_intf_addr   $ipV6_ixia_list       \
        -autonegotiation  $ipV6_autoneg_list    \
        -duplex           $ipV6_duplex_list     \
        -src_mac_addr     $ipV6_mac_list        \
        -speed            $ipV6_speed_list      \
        -signature_offset $ipV6_sgn_list        \
        -pgid_offset      $ipV6_pgid_list       \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

set vlan_number       1
set number_of_pgids   $vlan_number
set stream_index_list ""
################################################################################
# Add first stream on TX port
################################################################################
set traffic_status  [::ixia::traffic_config        \
        -mode                      create          \
        -port_handle               $port_0         \
        -l3_protocol               ipv6            \
        -ipv6_src_addr             1::1            \
        -ipv6_src_mode             increment       \
        -ipv6_src_step             0::1000:0:0:0   \
        -ipv6_src_count            $vlan_number    \
        -ipv6_dst_addr             2::1            \
        -ipv6_dst_mode             increment       \
        -ipv6_dst_step             0::1000:0:0:0   \
        -ipv6_dst_count            $vlan_number    \
        -l3_length                 78              \
        -rate_percent              50              \
        -mac_dst_mode              discovery       \
        -vlan_id_mode              increment       \
        -vlan_id                   100             \
        -vlan_id_count             $vlan_number    \
        -vlan_id_step              2               \
        -signature_offset          64              \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

set stream_id_list [keylget traffic_status stream_id]
################################################################################
# Add second stream on TX port
################################################################################
set traffic_status  [::ixia::traffic_config        \
        -mode                      create          \
        -port_handle               $port_0         \
        -l3_protocol               ipv6            \
        -ipv6_src_addr             3::1            \
        -ipv6_src_mode             increment       \
        -ipv6_src_step             0::1000:0:0:0   \
        -ipv6_src_count            $vlan_number    \
        -ipv6_dst_addr             4::1            \
        -ipv6_dst_mode             increment       \
        -ipv6_dst_step             0::1000:0:0:0   \
        -ipv6_dst_count            $vlan_number    \
        -l3_length                 78              \
        -rate_percent              50              \
        -mac_dst_mode              discovery       \
        -vlan_id_mode              increment       \
        -vlan_id                   100             \
        -vlan_id_count             $vlan_number    \
        -vlan_id_step              2               \
        -signature_offset          64              \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return
}

################################################################################
# Send router solicitation if ports are connected to a DUT
################################################################################
if {0} {
    set interface_status [::ixia::interface_config  \
            -port_handle     $port_0                \
            -arp_send_req    1                      \
            ]
    if {[keylget interface_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget interface_status log]"
        return
    }
    if {[catch {set failed_arp [keylget interface_status \
            $port_0.router_solicitation_success]}] || $failed_arp == 0} {
        set returnLog "FAIL - $test_name - arp send request failed. "
        if {![catch {set intf_list [keylget interface_status \
                $port_0.arp_ipv6_interfaces_failed]}]} {
            append returnLog "Router Solicitation failed on interfaces: $intf_list."
        }
        puts $returnLog
        return
    }
}

lappend stream_id_list [keylget traffic_status stream_id]
set number_of_streams  [llength $stream_id_list]
set number_of_bins     3

################################################################################
# Clear stats before sending traffic
################################################################################
set clear_stats_status [::ixia::traffic_control \
        -port_handle    $port_handle            \
        -action         clear_stats             \
        -jitter_bins    $number_of_bins         \
        -jitter_values  2 3.45 ]
if {[keylget clear_stats_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget clear_stats_status log]"
    return
}
################################################################################
# Start traffic on port
################################################################################
set traffic_control_status [::ixia::traffic_control \
        -port_handle $port_0                        \
        -action      run                            \
        ]
if {[keylget traffic_control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_control_status log]"
    return
}

# Sleep n seconds for traffic to run
ixia_sleep 5000
################################################################################
# Stop traffic on port
################################################################################
set traffic_control_status [::ixia::traffic_control \
        -port_handle $port_0                        \
        -action      stop                           \
        ]
if {[keylget traffic_control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_control_status log]"
    return
}

# Sleep n seconds for traffic to run
ixia_sleep 1000

################################################################################
# Get traffic statistics for all the PGIDs
################################################################################
set pgid_statistics_list [::ixia::traffic_stats \
        -port_handle     $port_1                \
        -mode            streams                \
        ]
if {[keylget pgid_statistics_list status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pgid_statistics_list log]"
    return
}
################################################################################
# Format the statistics
################################################################################
puts  "\n"
puts  "+---------------------------------------------------------------+"
puts  "+                       Statistic Results                       +"
puts  "+---------------------------------------------------------------+"
puts  "+ Time                   : [clock format [clock seconds]]"
puts  "+ Number of Streams      : $number_of_streams"
puts  "+ Number of Jitter Bins  : $number_of_bins"
puts  "+ Note                   : Jitter values are in nsec"
puts  "+---------------------------------------------------------------+"
puts  [format "%8s  %8s  %15s  %15s  %8s  %8s  %8s" \
        Stream Bin# FirstTS LastTS MaxJ MinJ TotalPackets]

 
for {set s_index 0} {$s_index < $number_of_streams} {incr s_index} { 
    set s_id [lindex $stream_id_list $s_index]
    for {set l 1} {$l <= $number_of_bins} {incr l} {
        puts  [format "%8d  %8d  %15.1f  %15.1f  %8.1f  %8.1f  %8d" \
                $s_id   $l                                          \
                [keylget pgid_statistics_list \
                $port_1.stream.$s_id.rx.jitter_bin.$l.first_tstamp] \
                [keylget pgid_statistics_list \
                $port_1.stream.$s_id.rx.jitter_bin.$l.last_tstamp]  \
                [keylget pgid_statistics_list \
                $port_1.stream.$s_id.rx.jitter_bin.$l.max]          \
                [keylget pgid_statistics_list \
                $port_1.stream.$s_id.rx.jitter_bin.$l.min]          \
                [keylget pgid_statistics_list \
                $port_1.stream.$s_id.rx.jitter_bin.$l.total_pkts]   \
                [keylget pgid_statistics_list ]]
    }
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return
