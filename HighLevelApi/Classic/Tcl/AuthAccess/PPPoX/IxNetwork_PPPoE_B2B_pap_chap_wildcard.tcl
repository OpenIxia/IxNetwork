################################################################################
# Version 1.0    $Revision: 1 $
#
#    Copyright © 1997 - 2006 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    7-24-2007 : Mircea Hasegan
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
#    This sample configures a PPPoE tunnel with 20 sessions between the        #
#    SRC port and the DUT. Authentication with wildcards is used.              #
#    Traffic is sent over the tunnel. A few statistics are being retrieved.    #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module                             #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 3/1 3/2]
set sess_count 20
# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect              \
        -reset                                   \
        -ixnetwork_tcl_server   localhost        \
        -device                 $chassisIP       \
        -port_list              $port_list       ]
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

puts "Ixia port handles are $port_handle "

########################################
# Configure SRC interface in the test  #
########################################
set interface_status [::ixia::interface_config \
        -port_handle      $port_src_handle     \
        -mode             config               \
        -speed            ether100             \
        -phy_mode         copper               \
        -autonegotiation  1                    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}


########################################
# Configure DST interface  in the test #
########################################
set interface_status [::ixia::interface_config \
        -port_handle      $port_dst_handle     \
        -mode             config               \
        -speed            ether100             \
        -phy_mode         copper               \
        -autonegotiation  1                    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

#########################################
#  Configure sessions                   #
#########################################
set config_status [::ixia::pppox_config      \
        -mode             add                \
        -port_handle      $port_src_handle   \
        -protocol         pppoe              \
        -encap             ethernet_ii       \
        -num_sessions     $sess_count        \
        -port_role           access             \
        -disconnect_rate  10                 \
        -redial                 1                 \
        -redial_max          10                 \
        -redial_timeout      20                 \
        -ip_cp            ipv4_cp            \
        -auth_mode        pap_or_chap        \
        -username                    "ixia#?"\
        -password                    "pwd#?" \
        -username_wildcard           1         \
        -password_wildcard             1          \
        -wildcard_pound_start         1       \
        -wildcard_pound_end             20      \
        -wildcard_question_start     1         \
        -wildcard_question_end       2       \
        ]
if {[keylget config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget config_status log]"
}
set pppox_handle [keylget config_status handle]
puts "Ixia pppox_handle is $pppox_handle "

set config_status2 [::ixia::pppox_config     \
        -mode             add                \
        -port_handle      $port_dst_handle   \
        -protocol         pppoe              \
        -encap            ethernet_ii        \
        -num_sessions     $sess_count        \
        -port_role           network             \
        -ip_cp            ipv4_cp            \
        -ppp_local_ip     25.10.10.1         \
        -ppp_peer_ip      25.10.10.2         \
        -ppp_peer_ip_step 0.0.0.1            \
        -auth_mode        chap               \
        -username                    "ixia#?"\
        -password                    "pwd#?" \
        -username_wildcard           1         \
        -password_wildcard             1          \
        -wildcard_pound_start         1       \
        -wildcard_pound_end             20      \
        -wildcard_question_start     1         \
        -wildcard_question_end       2       \
        ]
if {[keylget config_status2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget config_status2 log]"
}
set pppox_handle2 [keylget config_status2 handle]
puts "Ixia pppox_handle2 is $pppox_handle2 "
#########################################
#  Connect sessions                     #
#########################################
set control_status2 [::ixia::pppox_control \
        -handle     $pppox_handle2         \
        -action     connect               ]
if {[keylget control_status2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status2 log]"
}

set control_status [::ixia::pppox_control \
        -handle     $pppox_handle         \
        -action     connect               ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}

#########################################
#  Retrieve aggregate session stats     #
#########################################
set aggr_status [::ixia::pppox_stats \
        -port_handle $port_src_handle\
        -mode   aggregate            ]
if {[keylget aggr_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggr_status log]"
}

set sess_num       [keylget aggr_status ${port_src_handle}.aggregate.num_sessions]
set sess_count_up  [keylget aggr_status ${port_src_handle}.aggregate.connected]
set sess_min_setup [keylget aggr_status ${port_src_handle}.aggregate.min_setup_time]
set sess_max_setup [keylget aggr_status ${port_src_handle}.aggregate.max_setup_time]
set sess_avg_setup [keylget aggr_status ${port_src_handle}.aggregate.avg_setup_time]
set sess_num       [keylget aggr_status ${port_src_handle}.aggregate.num_sessions]
set chap_auth_fail_tx  [keylget aggr_status ${port_src_handle}.aggregate.chap_auth_fail_tx]
set chap_auth_succ_tx [keylget aggr_status ${port_src_handle}.aggregate.chap_auth_succ_tx]
set chap_auth_rsp_rx [keylget aggr_status ${port_src_handle}.aggregate.chap_auth_rsp_rx]
set chap_auth_chal_rx [keylget aggr_status ${port_src_handle}.aggregate.chap_auth_chal_rx]
set chap_auth_fail_rx       [keylget aggr_status ${port_src_handle}.aggregate.chap_auth_fail_rx]
set chap_auth_succ_rx  [keylget aggr_status ${port_src_handle}.aggregate.chap_auth_succ_rx]
set chap_auth_rsp_tx [keylget aggr_status ${port_src_handle}.aggregate.chap_auth_rsp_tx]
set chap_auth_chal_tx [keylget aggr_status ${port_src_handle}.aggregate.chap_auth_chal_tx]
set pap_auth_ack_rx [keylget aggr_status ${port_src_handle}.aggregate.pap_auth_ack_rx]
set pap_auth_nak_tx       [keylget aggr_status ${port_src_handle}.aggregate.pap_auth_nak_tx]
set pap_auth_req_rx  [keylget aggr_status ${port_src_handle}.aggregate.pap_auth_req_rx]
set pap_auth_ack_tx [keylget aggr_status ${port_src_handle}.aggregate.pap_auth_ack_tx]
set pap_auth_nak_rx [keylget aggr_status ${port_src_handle}.aggregate.pap_auth_nak_rx]
set pap_auth_req_tx [keylget aggr_status ${port_src_handle}.aggregate.pap_auth_req_tx]

puts "Ixia Test Results ... "
puts "        Number of sessions           = $sess_num "
puts "        Number of connected sessions = $sess_count_up "
puts "        Minimum Setup Time (ms)      = $sess_min_setup "
puts "        Maximum Setup Time (ms)      = $sess_max_setup "
puts "        Average Setup Time (ms)      = $sess_avg_setup "
puts ""
puts "        Chap Auth Fail TX            = $chap_auth_fail_tx "
puts "        Chap Auth Fail RX            = $chap_auth_fail_rx "
puts "        Chap Auth Succ TX            = $chap_auth_succ_tx "
puts "        Chap Auth Succ RX            = $chap_auth_succ_rx "
puts "        Chap Auth Rsp TX             = $chap_auth_rsp_tx "
puts "        Chap Auth RSP RX             = $chap_auth_rsp_rx "
puts "        Chap Auth Chal TX            = $chap_auth_chal_tx "
puts "        Chap Auth Chal RX            = $chap_auth_chal_rx "
puts ""
puts "        Pap Auth Ack TX              = $pap_auth_ack_tx "
puts "        Pap Auth Ack RX              = $pap_auth_ack_rx "
puts "        Pap Auth NAck TX             = $pap_auth_nak_tx "
puts "        Pap Auth NAck RX             = $pap_auth_nak_rx "
puts "        Pap Auth Req TX              = $pap_auth_req_tx "
puts "        Pap Auth Req RX              = $pap_auth_req_rx "

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
        -emulation_dst_handle $pppox_handle2    \
        -emulation_src_handle $pppox_handle     \
        -track_by             endpoint_pair     ]
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
after 20000

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

#########################################
#  Disconnect sessions                  #
#########################################

set control_status [::ixia::pppox_control \
        -handle     $pppox_handle         \
        -action     disconnect            ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}
set control_status [::ixia::pppox_control \
        -handle     $pppox_handle2        \
        -action     disconnect            ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}

set cleanup_status [::ixia::cleanup_session -port_handle $port_handle]
if {[keylget cleanup_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget cleanup_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"

