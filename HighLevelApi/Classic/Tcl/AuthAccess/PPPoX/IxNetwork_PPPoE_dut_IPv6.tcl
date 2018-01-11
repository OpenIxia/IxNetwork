#################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mircea Hasegan $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    08-15-2007 MHasegan
#
#################################################################################

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
#    This sample configures a PPPoE tunnel with 5 sessions between the         #
#    SRC port and the DUT.                                                     #
#    Traffic is sent over the tunnel and the DUT sends                         #
#    it to the DST port. After that a few statistics are being retrieved.      #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#                                                                              #
################################################################################

################################################################################
# DUT configuration:
#
# aaa new-model
# aaa authentication ppp default local
# aaa session-id common
#
#  username cisco password 0 cisco
#  ipv6 unicast-routing
#  ipv6 cef
#
#  bba-group pppoe groupIPv6
#   virtual-template 100
#
#  interface gigabitEthernet 0/2
#   no ip address
#   duplex full
#   pppoe enable group groupIPv6
#   ipv6 enable
#   no shutdown
#
#  interface gigabitEthernet 0/3
#   no ip address
#   no ip route-cache cef
#   no ip route-cache
#   no ip mroute-cache
#   duplex full
#   ipv6 address 2002:5678:5678::1/64
#   ipv6 enable
#   no shutdown
#
#  interface Virtual-Template100
#   no ip address
#   ipv6 enable
#   no ipv6 nd suppress-ra
#   peer default ipv6 pool poolIPv6
#   ppp max-bad-auth 10
#   ppp mtu adaptive
#   ppp authentication chap pap
#
#  ipv6 local pool poolIPv6 2001:1234:1234::/48 64
#
################################################################################

package require Ixia

set test_name  [info script]
set chassisIP  sylvester
set port_list  [list 3/3 3/4]
set sess_count 5

# Connect to the chassis, reset to factory defaults and take ownership
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
set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
            temp_port]} {
        lappend port_handle $temp_port
    }
}
set port_src_handle [lindex $port_handle 0]
set port_dst_handle [lindex $port_handle 1]

################################################################################
# Configure SRC interface in the test  
################################################################################
set interface_status [::ixia::interface_config \
        -port_handle      $port_src_handle     \
        -mode             config               \
        -autonegotiation  1                    \
        -phy_mode         copper               \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Configure DST interface in the test
################################################################################
set interface_status [::ixia::interface_config \
        -mode               config             \
        -autonegotiation    1                  \
        -phy_mode           copper             \
        -port_handle        $port_dst_handle   \
        -ipv6_intf_addr     2002:5678:5678::2  \
        -ipv6_prefix_length 64                 \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set int_handle [keylget interface_status interface_handle]
################################################################################
# Configure PPPoE sessions
################################################################################
set config_status [::ixia::pppox_config             \
        -mode                   add                 \
        -port_handle            $port_src_handle    \
        -protocol               pppoe               \
        -encap                  ethernet_ii         \
        -num_sessions           $sess_count         \
        -port_role              access              \
        -disconnect_rate        10                  \
        -redial                 1                   \
        -redial_max             10                  \
        -redial_timeout         20                  \
        -ip_cp                  ipv6_cp             \
        -auth_mode              chap                \
        -password               cisco               \
        -username               cisco               \
        ]
if {[keylget config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget config_status log]"
}
set pppox_handle [keylget config_status handle]
puts "Ixia pppox_handle is $pppox_handle ..."

################################################################################
#  Connect PPPoE sessions
################################################################################
set control_status [::ixia::pppox_control \
        -handle     $pppox_handle         \
        -action     connect               ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}

#########################################
#  Retrieve aggregate session stats     #
#########################################
after 10000
set aggr_status [::ixia::pppox_stats \
        -port_handle $port_src_handle        \
        -mode   aggregate            ]
if {[keylget aggr_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggr_status log]"
}

set sess_num       [keylget aggr_status ${port_src_handle}.aggregate.num_sessions]
set sess_count_up  [keylget aggr_status ${port_src_handle}.aggregate.connected]
set sess_min_setup [keylget aggr_status ${port_src_handle}.aggregate.min_setup_time]
set sess_max_setup [keylget aggr_status ${port_src_handle}.aggregate.max_setup_time]
set sess_avg_setup [keylget aggr_status ${port_src_handle}.aggregate.avg_setup_time]
puts "Ixia Test Results ... "
puts "        Number of sessions           = $sess_num "
puts "        Number of connected sessions = $sess_count_up "
puts "        Minimum Setup Time (ms)      = $sess_min_setup "
puts "        Maximum Setup Time (ms)      = $sess_max_setup "
puts "        Average Setup Time (ms)      = $sess_avg_setup "

################################################################################
# Delete all the streams first                                                 #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action             reset                                           \
        -traffic_generator  ixnetwork                                       \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

#########################################
#  Configure traffic                    #
#########################################
set traffic_status [::ixia::traffic_config      \
        -mode                 create            \
        -traffic_generator    ixnetwork         \
        -bidirectional        1                 \
        -emulation_dst_handle $int_handle       \
        -emulation_src_handle $pppox_handle     \
        -track_by             endpoint_pair     \
        -circuit_endpoint_type ipv6             ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Start the traffic                                                            #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# The traffic must flow!                                                       #
################################################################################
after 5000

################################################################################
# Stop the traffic                                                             #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

################################################################################
# Wait for the traffic to stop                                                 #
################################################################################
after 15000

################################################################################
# Gather and display traffic statistics                                        #
################################################################################
set aggregated_traffic_status [::ixia::traffic_stats                        \
        -mode                   aggregate                                   \
        -traffic_generator      ixnetwork                                   \
        ]
if {[keylget aggregated_traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggregated_traffic_status log]"
}
set aggregated_traffic_results [list                                        \
        "Scheduled Frames Tx."          aggregate.tx.scheduled_pkt_count    \
        "Scheduled Frames Tx. Rate"     aggregate.tx.scheduled_pkt_rate     \
        "Line Speed"                    aggregate.tx.line_speed             \
        "Frames Tx."                    aggregate.tx.pkt_count              \
        "Total Frames Tx."              aggregate.tx.total_pkts             \
        "Frames Tx. Rate"               aggregate.tx.pkt_rate               \
        "Frames Tx. Rate"               aggregate.tx.total_pkt_rate         \
        "Bytes Tx."                     aggregate.tx.pkt_byte_count         \
        "Bytes Tx. Rate"                aggregate.tx.pkt_byte_rate          \
        "Tx. Rate (bps)"                aggregate.tx.pkt_bit_rate           \
        "Tx. Rate (Kbps)"               aggregate.tx.pkt_kbit_rate          \
        "Tx. Rate (Mbps)"               aggregate.tx.pkt_mbit_rate          \
        "Bytes Rx."                     aggregate.rx.pkt_byte_count         \
        "Bytes Rx. Rate"                aggregate.rx.pkt_byte_rate          \
        "Rx. Rate (bps)"                aggregate.rx.pkt_bit_rate           \
        "Rx. Rate (Kbps)"               aggregate.rx.pkt_kbit_rate          \
        "Rx. Rate (Mbps)"               aggregate.rx.pkt_mbit_rate          \
        "Data Integrity Frames Rx."     aggregate.rx.data_int_frames_count  \
        "Data Integrity Errors"         aggregate.rx.data_int_errors_count  \
        "Collisions"                    aggregate.rx.collisions_count       \
        "Valid Frames Rx."              aggregate.rx.pkt_count              \
        "Valid Frames Rx. Rate"         aggregate.rx.pkt_rate               \
        ]
foreach port $port_handle {
    puts "Port $port:"
    puts "\tAggregated statistics:"
    foreach {name key} $aggregated_traffic_results {
        puts "\t\t$name: [keylget aggregated_traffic_status\
                $port.$key]"
    }
}


################################################################################
# Disconnect sessions
################################################################################

set control_status [::ixia::pppox_control \
        -handle     $pppox_handle         \
        -action     disconnect            \
        ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}

set control_status [::ixia::cleanup_session -port_handle $port_handle]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
