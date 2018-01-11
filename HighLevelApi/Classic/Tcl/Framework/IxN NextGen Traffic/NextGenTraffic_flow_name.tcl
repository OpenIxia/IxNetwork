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
# This script creates a traffic item and runs traffic between 2 ports. It      #
# prints flow stats and explains the meaning of the "flow_name" field          #
# Module:                                                                      #
#    The sample was tested on an STXS4 module.                                 #
#                                                                              #
################################################################################

package require Ixia

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
        set flow_name [keylget flow_traffic_status flow.$flow.flow_name]
        puts "\tFlow #$flow $flow_name"
        foreach {name key} [subst $[subst flow_results]] {
            puts "\t\t$name: [keylget flow_traffic_status flow.$flow.$key]"
        }
        puts "\t\tTraffic Item: [lindex $flow_name 1]"
        puts "\t\tIP Precedence : [lindex $flow_name 2]"
        puts "\t\tSource IP: [lindex $flow_name 3]"
        puts "\t\tDestination IP: [lindex $flow_name 4]"
    }
}

set test_name [info script]

set chassisIP sylvester
set port_list [list 7/1 7/2]


# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect            \
        -reset                                 \
        -ixnetwork_tcl_server   localhost      \
        -device                 $chassisIP     \
        -port_list              $port_list     \
        -username               ixiaApiUser    ]

if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_array [keylget connect_status port_handle.$chassisIP]

set port_0 [keylget port_array [lindex $port_list 0]]
set port_1 [keylget port_array [lindex $port_list 1]]


set interface_status1 [::ixia::interface_config \
        -port_handle         $port_0          \
        -intf_ip_addr        200.16.31.1      \
        -gateway             200.16.31.2      \
        -netmask             255.255.255.0    \
        -autonegotiation     1                \
        -op_mode             normal           \
        -duplex              auto             \
        -speed               auto             \
        -intf_mode           ethernet         ]
if {[keylget interface_status1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status1 log]"
}

set interface_status2 [::ixia::interface_config \
        -port_handle         $port_1          \
        -intf_ip_addr        200.16.31.2      \
        -gateway             200.16.31.1      \
        -netmask             255.255.255.0    \
        -autonegotiation     1                \
        -op_mode             normal           \
        -duplex              auto             \
        -speed               auto             \
        -intf_mode           ethernet         ]

if {[keylget interface_status2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status2 log]"
}


set traffic_status [::ixia::traffic_config                              \
        -traffic_generator          ixnetwork_540                       \
        -mode                       create                              \
        -ethernet_value_tracking    0                                   \
        -port_handle                $port_0                             \
        -port_handle2               $port_1                             \
        -ip_src_addr                {200.16.31.1 10.0.0.1}              \
        -ip_dst_addr                {200.16.31.2 10.0.0.2 10.0.0.3}     \
        -ip_src_mode                list                                \
        -ip_dst_mode                list                                \
        -ip_precedence              3                                   \
        -ip_precedence_mode         incr                                \
        -ip_precedence_count        3                                   \
        -ip_precedence_step         1                                   \
        -track_by                   {source_ip dest_ip ipv4_precedence} \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
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
set flow_traffic_status [::ixia::traffic_stats            \
        -mode                   flow                      \
        -traffic_generator      ixnetwork_540             \
        ]
if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status log]"
    return 0
}

after 1000

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


print_flow_stats $flow_traffic_status

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1