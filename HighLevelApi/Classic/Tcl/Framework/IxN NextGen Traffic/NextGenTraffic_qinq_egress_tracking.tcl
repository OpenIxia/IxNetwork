################################################################################
# Version 1.0    $Revision: 1 $
# $Author: cnicutar $
#
#    Copyright © 1997 - 2009 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10-29-2009 cnicutar
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
#    This script creates two interfaces each with stacked vlans and runs       # 
#    ipv4 traffic (-l3_protocol ipv4) between them (egress_) tracking by       #
#    outer_vlan_priority                                                       #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on an STXS4 module.                                 #
#                                                                              #
################################################################################
package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 2/3 2/4]


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
        -port_handle         $port_0          \
        -intf_ip_addr        172.16.31.1      \
        -gateway             172.16.31.2      \
        -netmask             255.255.255.0    \
        -autonegotiation     1                \
        -op_mode             normal           \
        -vlan                $true            \
        -vlan_id             10,20            \
        -vlan_user_priority  7,5              \
        -duplex              auto             \
        -speed               auto             \
        -intf_mode           ethernet         ]
if {[keylget interface_status1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status1 log]"
}

set interface_status2 [::ixia::interface_config \
        -port_handle         $port_1          \
        -intf_ip_addr        172.16.31.2      \
        -gateway             172.16.31.1      \
        -netmask             255.255.255.0    \
        -autonegotiation     1                \
        -op_mode             normal           \
        -vlan                $true            \
        -vlan_id             10,20            \
        -vlan_user_priority  7,5              \
        -duplex              auto             \
        -speed               auto             \
        -intf_mode           ethernet         ]

if {[keylget interface_status2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status2 log]"
}

set traffic_status [::ixia::traffic_config                  \
        -traffic_generator          ixnetwork_540           \
        -mode                       create                  \
        -ethernet_value_tracking    0                       \
        -port_handle                $port_0                 \
        -port_handle2               $port_1                 \
        -vlan                       enable                  \
        -vlan_id                    {10 20}                 \
        -vlan_user_priority         {5 6}                   \
        -vlan_user_priority_mode    {incr incr}             \
        -vlan_user_priority_count   {6 2}                   \
        -vlan_user_priority_step    {1 4}                   \
        -egress_tracking            outer_vlan_priority     \
        -track_by                   dest_endpoint           \
]

if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"

}

# puts stderr $traffic_status

set traffic_item [keylget traffic_status traffic_item]
set traffic_item_obj [keylget traffic_status $traffic_item]
set headers_obj [keylget traffic_item_obj headers]

set inner_vlan_header [lindex $headers_obj 2]

set traffic_status [::ixia::traffic_config      \
    -mode                   append_header       \
    -l3_protocol            ipv4                \
    -traffic_generator      ixnetwork_540       \
    -stream_id              $inner_vlan_header  \
    -ip_src_addr            172.16.31.1         \
    -ip_dst_addr            172.16.31.2         \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

after 10000


################################################################################
# Stop the traffic                                                             #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork_540                               \
]

if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}



################################################################################
# Wait for the traffic to stop                                                 #
################################################################################
after 10000

set flow_traffic_status [::ixia::traffic_stats                       \
        -mode                   egress_by_flow                              \
        -traffic_generator      ixnetwork_540                               \
        -port_handle            $port_1                                     \
]

if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status log]"
    return 0
}

puts "Finished retrieving stats per flow ..."
update idletasks
set flow_results [list                                                  \
            "Rx Frames"                     rx.total_pkts               \
            "Rx Frame Rate"                 rx.total_pkt_rate           \
            "Rx Bytes"                      rx.total_pkts_bytes         \
            "Rx Rate (Bps)"                 rx.total_pkt_byte_rate      \
            "Rx Rate (bps)"                 rx.total_pkt_bit_rate       \
            "Rx Rate (Kbps)"                rx.total_pkt_kbit_rate      \
            "Rx Rate (Mbps)"                rx.total_pkt_mbit_rate      \
            "Cut-Through Avg Latency (ns)"  rx.avg_delay                \
            "Cut-Through Min Latency (ns)"  rx.min_delay                \
            "Cut-Through Max Latency (ns)"  rx.max_delay                \
            "First TimeStamp"               rx.first_tstamp             \
            "Last TimeStamp"                rx.last_tstamp              \
        ]
puts " ----- EGRESS BY FLOW -----"

set flow 1
while {![catch {set flow_key [keylget flow_traffic_status $port_0.egress.$flow]}]} {
    puts "\tFlow $flow - [keylget flow_traffic_status $port_0.egress.$flow.flow_name] - [keylget flow_traffic_status $port_0.egress.$flow.flow_print]"
    foreach {name key} [subst $[subst flow_results]] {
        puts "\t\t$name: [keylget flow_traffic_status $port_0.egress.$flow.$key]"
    }
    incr flow
}

puts " ----- Flows = [expr $flow - 1] -----"


set flow_traffic_status_port [::ixia::traffic_stats                       \
        -mode                   egress_by_port                              \
        -traffic_generator      ixnetwork_540                               \
        -port_handle            $port_1                                     \
]

if {[keylget flow_traffic_status_port status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status_port log]"
    return 0
}

puts "Finished retrieving stats per flow ..."
update idletasks

set flow_results [list                                                  \
            "Rx Frames"                     rx.total_pkts               \
            "Rx Frame Rate"                 rx.total_pkt_rate           \
            "Rx Bytes"                      rx.total_pkts_bytes         \
            "Rx Rate (Bps)"                 rx.total_pkt_byte_rate      \
            "Rx Rate (bps)"                 rx.total_pkt_bit_rate       \
            "Rx Rate (Kbps)"                rx.total_pkt_kbit_rate      \
            "Rx Rate (Mbps)"                rx.total_pkt_mbit_rate      \
            "Cut-Through Avg Latency (ns)"  rx.avg_delay                \
            "Cut-Through Min Latency (ns)"  rx.min_delay                \
            "Cut-Through Max Latency (ns)"  rx.max_delay                \
            "First TimeStamp"               rx.first_tstamp             \
            "Last TimeStamp"                rx.last_tstamp              \
        ]


puts " ----- EGRESS BY PORT -----"

set flow 1

while {![catch {set flow_key [keylget flow_traffic_status_port $port_0.egress.$flow]}]} {
    puts "\tFlow $flow - [keylget flow_traffic_status_port $port_0.egress.$flow.flow_name]"
    foreach {name key} [subst $[subst flow_results]] {
        puts "\t\t$name: [keylget flow_traffic_status_port $port_0.egress.$flow.$key]"
    }
    incr flow
}

puts " ----- Flows = [expr $flow - 1] -----"

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1