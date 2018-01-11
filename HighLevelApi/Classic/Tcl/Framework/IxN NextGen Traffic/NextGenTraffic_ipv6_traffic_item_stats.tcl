################################################################################
# Version 1.0    $Revision: 1 $
# $Author: cnicutar $
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
#    using ixnetwork_540 traffic_generator and tracking by qos.                #
#                                                                              #
#    It uses two Ixia ports. BGP peers and routes are configured on both       #
#    ports.  Streams are generated using ixnetwork traffic_generator           #
#    Traffic statistics are collected for each flow.                           #
#    Flow rates are updated while the traffic is running with mode             #
#    dynamic update.
#                                                                              #
################################################################################

package require Ixia
set test_name [info script]

set chassisIP sylvester
set port_list [list 7/1 7/2]


set intf_num_per_port 10


# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
        -reset                                  \
        -ixnetwork_tcl_server   localhost       \
        -device                 $chassisIP      \
        -port_list              $port_list      \
        -username               ixiaApiUser     \
]

if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}


proc print_flow_stats {flow_traffic_status} {
    set flow_results [list                                                  \
        "Tx Frames"                     tx.total_pkts                       \
        "Rx Frames"                     rx.total_pkts                       \
        "Tx pkt_rate"                   tx.total_pkt_rate                   \
        "Loss %"                        rx.loss_percent                     \
    ]

    set flows [keylget flow_traffic_status flow]
    foreach flow [keylkeys flows] {
        set flow_key [keylget flow_traffic_status flow.$flow]
        puts "\tFlow $flow"
        foreach {name key} [subst $[subst flow_results]] {
            puts "\t\t$name: [keylget flow_traffic_status flow.$flow.$key]"
        }
    }
}


set port_array [keylget connect_status port_handle.$chassisIP]

set port_0 [keylget port_array [lindex $port_list 0]]
set port_1 [keylget port_array [lindex $port_list 1]]

set port_handle {}

set ipv6_addr_start "2001::0"
set ipv6_addr_list {}

for {set i 0} {$i<$intf_num_per_port} {incr i} {
    lappend ipv6_addr_list [::ixia::increment_ipv6_address_hltapi $ipv6_addr_start "0::1"] \
    [::ixia::increment_ipv6_address_hltapi $ipv6_addr_start "0::${intf_num_per_port}"] \
    
    lappend port_handle $port_0 $port_1
    
    set ipv6_addr_start [::ixia::increment_ipv6_address_hltapi $ipv6_addr_start "0::1"]
}


set interface_status [::ixia::interface_config      \
        -port_handle            $port_handle        \
        -ipv6_intf_addr         $ipv6_addr_list     \
        -ipv6_prefix_length     64                  \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set port_0_interfaces {}
set port_1_interfaces {}

foreach {int1 int2} [keylget interface_status interface_handle] {
    lappend port_0_interfaces $int1
    lappend port_1_interfaces $int2
}


set rate_start_value        10
set rate_increment_step     30
set dynamic_count    3

set frame_size_start        48
set frame_size_step         16



set traffic_status  [::ixia::traffic_config                             \
        -traffic_generator              ixnetwork_540                   \
        -mode                           create                          \
        -circuit_endpoint_type          ipv6                            \
        -emulation_src_handle           $port_0_interfaces              \
        -emulation_dst_handle           $port_1_interfaces              \
        -src_dest_mesh                  fully                           \
        -rate_percent                   $rate_start_value               \
        -track_by                       ipv6_source_ip                  \
        -frame_size                     $frame_size_start               \
]

if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}
set stream_id [keylget traffic_status traffic_item]

puts "Running traffic with rate_percent : ${rate_start_value}%"

set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

after 10000

set flow_traffic_status  [::ixia::traffic_stats               \
        -traffic_generator              ixnetwork_540    \
        -mode                           flow             \
]
if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status log]"
    return 0
}

print_flow_stats $flow_traffic_status
update idletasks

for {set i 0} {$i<$dynamic_count} {incr i} {
    set rate_start_value [expr $rate_start_value + $rate_increment_step]
    set frame_size_start [expr $frame_size_start + $frame_size_step]

    puts "Changing traffic rate_percent to ${rate_start_value}%"
    set traffic_status  [::ixia::traffic_config                             \
            -traffic_generator              ixnetwork_540                   \
            -mode                           dynamic_update                  \
            -rate_percent                   $rate_start_value               \
            -stream_id                      $stream_id                      \
            -frame_size                     $frame_size_start               \
    ]
    if {[keylget traffic_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget traffic_status log]"
        return 0
    }
    
    after 10000
    
    set flow_traffic_status  [::ixia::traffic_stats      \
        -traffic_generator              ixnetwork_540    \
        -mode                           flow             \
    ]
    print_flow_stats $flow_traffic_status
    update idletasks    
}


set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1