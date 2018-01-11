################################################################################
# Version 1.0    $Revision: 1 $
# $Author: $
#
#    Copyright © 1997 - 2010 by IXIA
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
###############################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 10.205.16.65
set port_list [list 3/1 3/2]



# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
        -reset                                  \
        -ixnetwork_tcl_server   localhost       \
        -device                 $chassisIP      \
        -port_list              $port_list      \
        -username               cnicutar        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_array [keylget connect_status port_handle.$chassisIP]

set port0 [keylget port_array [lindex $port_list 0]]
set port1 [keylget port_array [lindex $port_list 1]]


set interface_status [::ixia::interface_config    \
    -mode               config                    \
    -port_handle        $port0                    \
    -data_integrity     1                         \
    -intf_mode          ethernet                  \
    -speed              auto                      \
    -transmit_mode      advanced                  \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}


set config_status [::ixia::l2tp_config                                           \
    -mode                           lac                                          \
    -num_tunnels                    3                                            \
    -port_handle                    $port0                                       \
    -attempt_rate                   100                                          \
    -disconnect_rate                200                                          \
    -enable_term_req_timeout        1                                            \
    -max_outstanding                200                                          \
    -max_terminate_req              10                                           \
    -terminate_req_timeout          5                                            \
    -l2_encap                       ethernet_ii                                  \
    -l2tp_dst_addr                  12.70.0.1                                    \
    -l2tp_dst_step                  0.0.0.0                                      \
    -src_mac_addr                   00.de.ad.be.ef.00                            \
    -bearer_capability              digital                                      \
    -bearer_type                    digital                                      \
    -ctrl_retries                   5                                            \
    -framing_capability             sync                                         \
    -hello_interval                 60                                           \
    -init_ctrl_timeout              2                                            \
    -max_ctrl_timeout               8                                            \
    -redial_max                     20                                           \
    -redial_timeout                 10                                           \
    -rws                            10                                           \
    -sess_distribution              next                                         \
    -sessions_per_tunnel            35                                           \
    -offset_byte                    0                                            \
    -offset_len                     0                                            \
    -udp_dst_port                   1701                                         \
    -udp_src_port                   1701                                         \
    -avp_rx_connect_speed           128                                          \
    -hostname                       dut                                          \
    -secret                         ixia                                         \
    -domain_group_map               {1 12.70.0.1 1 4} {{test 1 1 3 1 .org} {0}}  \
    -tun_distribution               domain_group                                 \
    -config_req_timeout             5                                            \
    -echo_req                       1                                            \
    -echo_req_interval              60                                           \
    -echo_rsp                       1                                            \
    -max_configure_req              10                                           \
    -ip_cp                          ipv4_cp                                      \
    -auth_mode                      chap                                         \
    -auth_req_timeout               5                                            \
    -max_auth_req                   10                                           \
    -password                       pass                                         \
    -username                       user                                         \
    -enable_magic                   0                                            \
    -l2tp_src_addr                  12.70.0.2                                    \
    -l2tp_src_count                 3                                            \
    -l2tp_src_gw                    0.0.0.0                                      \
    -l2tp_src_prefix_len            16                                           \
    -l2tp_src_step                  0.0.0.1                                      \
    -no_call_timeout                5                                            \
    -session_id_start               1                                            \
    -tunnel_id_start                1                                            \
    -tun_auth                       1                                            \
]
if {[keylget config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget config_status log]"
    return 0
}
set access_l2tp_handle [keylget config_status handle]
puts "Ixia access_l2tp_handle is $access_l2tp_handle "



set config_status [::ixia::l2tp_config                                              \
        -mode                           lns                                         \
        -num_tunnels                    3                                           \
        -port_handle                    $port1                                      \
        -attempt_rate                   100                                         \
        -disconnect_rate                200                                         \
        -enable_term_req_timeout        1                                           \
        -max_outstanding                200                                         \
        -max_terminate_req              10                                          \
        -terminate_req_timeout          5                                           \
        -l2_encap                       ethernet_ii                                 \
        -l2tp_dst_addr                  12.70.0.2                                   \
        -l2tp_dst_step                  0.0.0.0                                     \
        -src_mac_addr                   00.de.ad.be.ef.00                           \
        -bearer_capability              digital                                     \
        -bearer_type                    digital                                     \
        -ctrl_retries                   5                                           \
        -framing_capability             sync                                        \
        -hello_interval                 60                                          \
        -init_ctrl_timeout              2                                           \
        -max_ctrl_timeout               8                                           \
        -redial_max                     20                                          \
        -redial_timeout                 10                                          \
        -rws                            10                                          \
        -sess_distribution              next                                        \
        -sessions_per_tunnel            35                                          \
        -offset_byte                    0                                           \
        -offset_len                     0                                           \
        -udp_dst_port                   1701                                        \
        -udp_src_port                   1701                                        \
        -avp_rx_connect_speed           128                                         \
        -hostname                       dut                                         \
        -secret                         ixia                                        \
        -domain_group_map               {1 12.70.0.1 1 4} {{test 1 1 3 1 .org} {0}} \
        -tun_distribution               domain_group                                \
        -config_req_timeout             5                                           \
        -echo_req                       1                                           \
        -echo_req_interval              60                                          \
        -echo_rsp                       1                                           \
        -max_configure_req              10                                          \
        -ip_cp                          ipv4_cp                                     \
        -auth_mode                      chap                                        \
        -auth_req_timeout               5                                           \
        -max_auth_req                   10                                          \
        -password                       pass                                        \
        -username                       user                                        \
        -enable_magic                   0                                           \
        -l2tp_src_addr                  12.70.0.1                                   \
        -l2tp_src_count                 1                                           \
        -l2tp_src_gw                    0.0.0.0                                     \
        -l2tp_src_prefix_len            16                                          \
        -l2tp_src_step                  0.0.0.0                                     \
        -no_call_timeout                5                                           \
        -session_id_start               1                                           \
        -tunnel_id_start                1                                           \
        -tun_auth                       1                                           \
    ]
if {[keylget config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget config_status log]"
    return 0
}

after 5000
set network_l2tp_handle [keylget config_status handle]
puts "Ixia network_l2tp_handle is $network_l2tp_handle "


set control_status [::ixia::l2tp_control                                        \
        -handle     [list                                                       \
                            $network_l2tp_handle                                \
                            $access_l2tp_handle                                 \
                    ]                                                           \
        -action     connect                                                     \
        ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}


set traffic_status [::ixia::traffic_config                                      \
    -mode                                       create                          \
    -traffic_generator                          ixnetwork_540                   \
    -bidirectional                              1                               \
    -port_handle                                $port1                          \
    -emulation_dst_handle                       $access_l2tp_handle             \
    -emulation_src_handle                       $network_l2tp_handle            \
    -allow_self_destined                        0                               \
    -hosts_per_net                              1                               \
    -stream_packing                             optimal_packing                 \
    -transmit_mode                              continuous                      \
    -pkts_per_burst                             100                             \
    -rate_bps                                   100000                          \
    -rate_percent                               10                              \
    -rate_pps                                   100000                          \
    -inter_burst_gap                            64                              \
    -inter_frame_gap                            64                              \
    -inter_stream_gap                           64                              \
    -enforce_min_gap                            12                              \
    -tx_delay                                   0                               \
    -burst_loop_count                           1                               \
    -loop_count                                 1                               \
    -fcs                                        0                               \
    -fcs_type                                   no_CRC                          \
    -frame_size                                 256                             \
    -length_mode                                fixed                           \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}


after 10000

array set stats_array_per_session {
    interface_id
        "Interface Identifier"
    peer_call_id
        "Peer Call Id"
    tunnel_id
        "Tunnel Id"
    data_ns
        "Data NS"
    destination_port
        "Destination Port"
    source_port
        "Source Port"
    destination_ip
        "Destination IP"
    source_ip
        "Source IP"
    gateway_ip
        "Gateway IP"
    call_id
        "Call Id"
    peer_id
        "Peer Id"
    cookie_len
        "Cookie Length"
    cookie
        "Cookie"
    icrq_tx
        "ICRQ Tx"
    icrp_tx
        "ICRP Tx"
    iccn_tx
        "ICCN Tx"
    cdn_tx
        "CDN Tx"
    icrq_rx
        "ICRQ Rx"
    icrp_rx
        "ICRP Rx"
    iccn_rx
        "ICCN Rx"
    cdn_rx
        "CDN Rx"
    pppox_state
        "PPPoE state"
}
puts [string repeat "#" 80]
puts "Per session stats:"
puts [string repeat "#" 80]
puts ""
    
set sess_status [::ixia::l2tp_stats         \
        -port_handle    $port1              \
        -mode           session              ]
if {[keylget sess_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget sess_status log]"
    return 0
}

############################ CHECKING PER SESSION STATS ########################
set all_ok 1
set ok_log [list]
foreach key_1 [keylkeys sess_status session] {
    puts "Session $key_1"
    puts [string repeat "#" 40]
    set target_statistics [keylget sess_status session.$key_1]
    foreach key_2 [keylkeys target_statistics] {
        set current_value [keylget target_statistics $key_2]
        puts "[format %-40s $key_2]: $current_value"
        if {[string first "ip_addr" $key_2] >= 0} {
            # Validate ip addresses...
            set matched [regexp {([0-9]+).([0-9]+).([0-9]+).([0-9]+)$} $current_value matched_str ip1 ip2 ip3 ip4]
            if {$matched} {
                lappend ok_log $current_value
            } else {
                set all_ok 0
                set ok_log "IP address not matched: $current_value !"
            }
        }
    }
}
################################################################################

########################################
# Disconnect sessions                  #
########################################
set control_status [::ixia::l2tp_control                                        \
        -handle     [list                                                       \
                            $network_l2tp_handle                                \
                            $access_l2tp_handle                                 \
                    ]                                                           \
        -action     disconnect                                                  \
        ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}