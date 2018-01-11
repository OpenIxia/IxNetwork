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
#    The script configures 5 traffic items with various qos parameters and     #
#    collects flow stats.                                                      #
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
        -port_handle        $port_0          \
        -intf_ip_addr       172.16.31.1      \
        -gateway            172.16.31.2      \
        -netmask            255.255.255.0    \
        -autonegotiation    1                \
        -op_mode            normal           \
        -vlan               $true            \
        -vlan_id            100              \
        -vlan_user_priority 7                \
        -duplex             auto             \
        -speed              auto             \
        -intf_mode          ethernet         ]
if {[keylget interface_status1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
set intf_h0 [keylget interface_status1 interface_handle]


set interface_status2 [::ixia::interface_config \
        -port_handle        $port_1          \
        -intf_ip_addr       172.16.31.2      \
        -gateway            172.16.31.1      \
        -netmask            255.255.255.0    \
        -autonegotiation    1                \
        -op_mode            normal           \
        -vlan               $true            \
        -vlan_id            100              \
        -vlan_user_priority 7                \
        -duplex             auto             \
        -speed              auto             \
        -intf_mode          ethernet         ]
if {[keylget interface_status2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status2 log]"
}

set intf_h1 [keylget interface_status2 interface_handle]


set traffic_status1 [::ixia::traffic_config         \
            -traffic_generator      ixnetwork_540   \
            -circuit_endpoint_type  ipv4            \
            -mode                   create          \
            -emulation_src_handle   $intf_h0        \
            -emulation_dst_handle   $intf_h1        \
            -l3_protocol            ipv4            \
            -qos_type_ixn           custom          \
            -qos_value_ixn          5               \
            -qos_value_ixn_mode     incr            \
            -qos_value_ixn_step     2               \
            -qos_value_ixn_count    2               \
            -qos_value_ixn_tracking 1               \
]

if {[keylget traffic_status1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status1 log]"
}

set traffic_status2 [::ixia::traffic_config         \
            -traffic_generator      ixnetwork_540   \
            -circuit_endpoint_type  ipv4            \
            -mode                   create          \
            -emulation_src_handle   $intf_h0        \
            -emulation_dst_handle   $intf_h1        \
            -l3_protocol            ipv4            \
            -qos_type_ixn           tos             \
            -ip_precedence          {0 3}           \
            -ip_precedence_mode     list            \
            -ip_precedence_tracking 1               \
]

if {[keylget traffic_status2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status2 log]"
}


set traffic_status3 [::ixia::traffic_config         \
            -traffic_generator      ixnetwork_540   \
            -circuit_endpoint_type  ipv4            \
            -mode                   create          \
            -emulation_src_handle   $intf_h0        \
            -emulation_dst_handle   $intf_h1        \
            -l3_protocol            ipv4            \
            -qos_type_ixn           dscp            \
            -qos_value_ixn          dscp_default    \
            -ip_dscp                60              \
            -ip_dscp_mode           decr            \
            -ip_dscp_count          3               \
            -ip_dscp_step           10              \
            -ip_dscp_tracking       1               \
]

if {[keylget traffic_status3 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status3 log]"
}

set traffic_status4 [::ixia::traffic_config         \
            -traffic_generator      ixnetwork_540   \
            -circuit_endpoint_type  ipv4            \
            -mode                   create          \
            -emulation_src_handle   $intf_h0        \
            -emulation_dst_handle   $intf_h1        \
            -l3_protocol            ipv4            \
            -qos_type_ixn           dscp            \
            -qos_value_ixn          {af_class1_low_precedence af_class2_high_precedence} \
            -qos_value_ixn_mode     list            \
            -qos_value_ixn_tracking 1               \
]

if {[keylget traffic_status4 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status4 log]"
}


set traffic_status5 [::ixia::traffic_config         \
            -traffic_generator      ixnetwork_540   \
            -circuit_endpoint_type  ipv4            \
            -mode                   create          \
            -emulation_src_handle   $intf_h0        \
            -emulation_dst_handle   $intf_h1        \
            -l3_protocol            ipv4            \
            -qos_type_ixn           dscp            \
            -qos_value_ixn          {cs_precedence1  cs_precedence2} \
            -qos_value_ixn_mode     list            \
            -qos_value_ixn_tracking 1               \
]

if {[keylget traffic_status5 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status5 log]"
}

set item [keylget traffic_status5 traffic_item]

set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}


after 10000



set flow_traffic_status [::ixia::traffic_stats                        \
        -mode                   flow                                        \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status log]"
    return 0
}


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
after 30000

set flow_results [list                                                      \
        "Tx Port"                       tx.port                             \
        "Rx Port"                       rx.port                             \
        "Tx Frames"                     tx.total_pkts                       \
        "Tx Frame Rate"                 tx.total_pkt_rate                   \
        "Rx Frames"                     rx.total_pkts                       \
        "Frames Delta"                  rx.loss_pkts                        \
        "Rx Frame Rate"                 rx.total_pkt_rate                   \
        "Loss %"                        rx.loss_percent                     \
        "Rx Bytes"                      rx.total_pkts_bytes                 \
        "Rx Rate (Bps)"                 rx.total_pkt_byte_rate              \
        "Rx Rate (bps)"                 rx.total_pkt_bit_rate               \
        "Rx Rate (Kbps)"                rx.total_pkt_kbit_rate              \
        "Rx Rate (Mbps)"                rx.total_pkt_mbit_rate              \
        "Avg Latency (ns)"              rx.avg_delay                        \
        "Min Latency (ns)"              rx.min_delay                        \
        "Max Latency (ns)"              rx.max_delay                        \
        "First Timestamp"               rx.first_tstamp                     \
        "Last Timestamp"                rx.last_tstamp                      \
        ]

set flows [keylget flow_traffic_status flow]
foreach flow [keylkeys flows] {
    set flow_key [keylget flow_traffic_status flow.$flow]
    puts "\tFlow $flow: [keylget flow_traffic_status flow.$flow.flow_name]"
    foreach {name key} [subst $[subst flow_results]] {
        puts "\t\t$name: [keylget flow_traffic_status flow.$flow.$key]"
    }
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
