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

set pppox_session_count     10

# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect         \
        -reset                              \
        -ixnetwork_tcl_server   localhost   \
        -device                 $chassisIP  \
        -port_list              $port_list  \
        -username               cnicutar    ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_array [keylget connect_status port_handle.$chassisIP]

set port0 [keylget port_array [lindex $port_list 0]]
set port1 [keylget port_array [lindex $port_list 1]]

set interface_status [::ixia::interface_config                          \
    -mode                               config                          \
    -port_handle                        $port0                          \
    -data_integrity                     1                               \
    -intf_mode                          ethernet                        \
    -speed                              auto                            \
    -transmit_mode                      advanced                        \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

#################################################################################
# START - PPPoX configuration - Access Port                                     #
#################################################################################

set config_status [::ixia::pppox_config                                 \
    -mode                               add                             \
    -handle                             pppox_handle                    \
    -num_sessions                       $pppox_session_count            \
    -port_handle                        $port0                          \
    -protocol                           pppoe                           \
    -port_role                          access                          \
    -attempt_rate                       100                             \
    -disconnect_rate                    100                             \
    -max_outstanding                    1000                            \
    -addr_count_per_vci                 1                               \
    -addr_count_per_vpi                 1                               \
    -encap                              ethernet_ii                     \
    -mac_addr                           00:00:01:03:01:01               \
    -mac_addr_step                      00:00:00:00:00:01               \
    -pvc_incr_mode                      vci                             \
    -vci                                32                              \
    -vci_count                          1                               \
    -vci_step                           1                               \
    -vlan_id                            1                               \
    -vlan_id_count                      4094                            \
    -vlan_id_outer                      1                               \
    -vlan_id_outer_count                4094                            \
    -vlan_id_outer_step                 1                               \
    -vlan_id_step                       1                               \
    -vlan_user_priority                 0                               \
    -vpi                                0                               \
    -vpi_count                          1                               \
    -vpi_step                           1                               \
    -qinq_incr_mode                     both                            \
    -ac_name                            ""                              \
    -ac_select_list                     ""                              \
    -ac_select_mode                     first_responding                \
    -max_padi_req                       10                              \
    -max_padr_req                       10                              \
    -padi_req_timeout                   6                               \
    -padr_req_timeout                   6                               \
    -redial                             1                               \
    -redial_max                         25                              \
    -redial_timeout                     15                              \
    -service_name                       ""                              \
    -service_type                       any                             \
    -domain_group_map                   ""                              \
    -config_req_timeout                 6                               \
    -echo_req                           1                               \
    -echo_req_interval                  70                              \
    -echo_rsp                           1                               \
    -max_configure_req                  15                              \
    -max_terminate_req                  15                              \
    -local_magic                        1                               \
    -term_req_timeout                   6                               \
    -ip_cp                              ipv6_cp                         \
    -ipcp_req_timeout                   6                               \
    -ipv6_pool_addr_prefix_len          64                              \
    -ipv6_pool_prefix                   ::                              \
    -ipv6_pool_prefix_len               48                              \
    -max_ipcp_req                       10                              \
    -ppp_local_ip                       1.1.1.100                       \
    -ppp_local_ip_step                  0.0.0.1                         \
    -ppp_local_iid                      {00 11 22 33 44 55 66 00}       \
    -ppp_peer_ip                        1.1.1.1                         \
    -ppp_peer_ip_step                   0.0.0.1                         \
    -ppp_peer_iid                       {00 77 88 99 aa bb cc 00}       \
    -auth_mode                          none                            \
    -max_auth_req                       15                              \
    -auth_req_timeout                   6                               \
    -password                           ""                              \
    -password_wildcard                  0                               \
    -username                           ""                              \
    -username_wildcard                  0                               \
    -wildcard_pound_end                 0                               \
    -wildcard_pound_start               0                               \
    -wildcard_question_end              0                               \
    -wildcard_question_start            0                               \
    -actual_rate_downstream             10                              \
    -actual_rate_upstream               10                              \
    -agent_circuit_id                   ""                              \
    -agent_remote_id                    ""                              \
    -data_link                          ethernet                        \
    -enable_client_signal_iwf           0                               \
    -enable_client_signal_loop_char     0                               \
    -enable_client_signal_loop_encap    0                               \
    -enable_client_signal_loop_id       0                               \
    -enable_server_signal_iwf           0                               \
    -enable_server_signal_loop_char     0                               \
    -enable_server_signal_loop_encap    0                               \
    -enable_server_signal_loop_id       0                               \
    -intermediate_agent_encap1          untagged_eth                    \
    -intermediate_agent_encap2          na                              \
]
if {[keylget config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget config_status log]"
    return 0
}

set pppox_handle_0 [keylget config_status handle]

#################################################################################
# END - PPPoX configuration - Access Port                                       #
#################################################################################

set interface_status [::ixia::interface_config                          \
    -mode                               config                          \
    -port_handle                        $port1                          \
    -data_integrity                     1                               \
    -intf_mode                          ethernet                        \
    -speed                              auto                            \
    -transmit_mode                      advanced                        \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

#################################################################################
# START - PPPoX configuration - Network Port                                    #
#################################################################################


set config_status [::ixia::pppox_config                                 \
    -mode                               add                             \
    -handle                             pppox_handle                    \
    -num_sessions                       $pppox_session_count            \
    -port_handle                        $port1                          \
    -protocol                           pppoe                           \
    -port_role                          network                         \
    -attempt_rate                       100                             \
    -disconnect_rate                    100                             \
    -max_outstanding                    1000                            \
    -addr_count_per_vci                 1                               \
    -addr_count_per_vpi                 1                               \
    -encap                              ethernet_ii                     \
    -mac_addr                           00:00:01:03:02:01               \
    -mac_addr_step                      00:00:00:00:00:01               \
    -pvc_incr_mode                      vci                             \
    -vci                                32                              \
    -vci_count                          1                               \
    -vci_step                           1                               \
    -vlan_id                            1                               \
    -vlan_id_count                      4094                            \
    -vlan_id_outer                      1                               \
    -vlan_id_outer_count                4094                            \
    -vlan_id_outer_step                 1                               \
    -vlan_id_step                       1                               \
    -vlan_user_priority                 0                               \
    -vpi                                0                               \
    -vpi_count                          1                               \
    -vpi_step                           1                               \
    -qinq_incr_mode                     both                            \
    -ac_name                            ""                              \
    -ac_select_list                     ""                              \
    -ac_select_mode                     first_responding                \
    -max_padi_req                       10                              \
    -max_padr_req                       10                              \
    -padi_req_timeout                   5                               \
    -padr_req_timeout                   5                               \
    -redial                             1                               \
    -redial_max                         20                              \
    -redial_timeout                     10                              \
    -service_name                       ""                              \
    -service_type                       any                             \
    -domain_group_map                   ""                              \
    -config_req_timeout                 5                               \
    -echo_req                           0                               \
    -echo_req_interval                  60                              \
    -echo_rsp                           1                               \
    -max_configure_req                  10                              \
    -max_terminate_req                  10                              \
    -local_magic                        1                               \
    -term_req_timeout                   5                               \
    -ip_cp                              ipv6_cp                         \
    -ipcp_req_timeout                   5                               \
    -ipv6_pool_addr_prefix_len          64                              \
    -ipv6_pool_prefix                   0002:0003:0002:0000::           \
    -ipv6_pool_prefix_len               48                              \
    -max_ipcp_req                       10                              \
    -ppp_local_ip                       1.1.1.1                         \
    -ppp_local_ip_step                  0.0.0.1                         \
    -ppp_local_iid                      "00 02 03 02 00 00 00 01"       \
    -ppp_peer_ip                        1.1.1.100                       \
    -ppp_peer_ip_step                   0.0.0.1                         \
    -ppp_peer_iid                       "00 02 03 02 00 10 00 01"       \
    -auth_mode                          none                            \
    -auth_req_timeout                   5                               \
    -max_auth_req                       10                              \
    -password                           ""                              \
    -password_wildcard                  0                               \
    -username                           ""                              \
    -username_wildcard                  0                               \
    -wildcard_pound_end                 0                               \
    -wildcard_pound_start               0                               \
    -wildcard_question_end              0                               \
    -wildcard_question_start            0                               \
    -actual_rate_downstream             10                              \
    -actual_rate_upstream               10                              \
    -agent_circuit_id                   ""                              \
    -agent_remote_id                    ""                              \
    -data_link                          ethernet                        \
    -enable_client_signal_iwf           0                               \
    -enable_client_signal_loop_char     0                               \
    -enable_client_signal_loop_encap    0                               \
    -enable_client_signal_loop_id       0                               \
    -enable_server_signal_iwf           0                               \
    -enable_server_signal_loop_char     0                               \
    -enable_server_signal_loop_encap    0                               \
    -enable_server_signal_loop_id       0                               \
    -intermediate_agent_encap1          untagged_eth                    \
    -intermediate_agent_encap2          na                              \
]
if {[keylget config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget config_status log]"
    return 0
}
set pppox_handle_1 [keylget config_status handle]

#################################################################################
# END - PPPoX configuration - Network Port                                      #
#################################################################################


########################################
# Start PPP                            #
########################################
set control_status [::ixia::pppox_control   \
        -handle     $pppox_handle_1         \
        -action     connect               ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}

########################################
# Start PPP                            #
########################################
set control_status [::ixia::pppox_control   \
        -handle     $pppox_handle_0         \
        -action     connect               ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}

after 10000

########################################
# Aggregate Stats                      #
########################################
# CHECK if all sessions are up
set retries       100
set sess_count_up 0
while {($sess_count_up < $pppox_session_count) && $retries} {
    set aggr_status [::ixia::pppox_stats    \
            -port_handle $port0             \
            -mode        aggregate            ]
    if {[keylget aggr_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget aggr_status log]"
        return 0
    }
    
    incr retries -1
    
    set sess_num       [keylget aggr_status $port0.aggregate.num_sessions]
    set sess_count_up  [keylget aggr_status $port0.aggregate.connected]
    set sess_min_setup [keylget aggr_status $port0.aggregate.min_setup_time]
    set sess_max_setup [keylget aggr_status $port0.aggregate.max_setup_time]
    set sess_avg_setup [keylget aggr_status $port0.aggregate.avg_setup_time]
    puts "PPPoX Aggregate Stats - retries left $retries ... "
    puts "        Number of sessions           = $sess_num "
    puts "        Number of connected sessions = $sess_count_up "
    puts "        Minimum Setup Time (ms)      = $sess_min_setup "
    puts "        Maximum Setup Time (ms)      = $sess_max_setup "
    puts "        Average Setup Time (ms)      = $sess_avg_setup "
    update idletasks
}
if {$sess_count_up != $pppox_session_count} {
    puts "FAIL - $test_name - Not all PPPoX sessions are up."
    return 0
}

########################################
# Print Aggregate Stats                #
########################################
puts [string repeat "#" 80]
puts "Aggregate stats:"
puts [string repeat "#" 80]
set aggr_status [::ixia::pppox_stats        \
        -port_handle $port0                 \
        -mode        aggregate            ]
if {[keylget aggr_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget aggr_status log]"
    return 0
}
foreach key [keylkeys aggr_status $port0.aggregate] {
    if {$key != "status"} {
        puts "[format %-40s $key]: [keylget aggr_status $port0.aggregate.$key]"
    }
}

after 10000
#################################################################################
# Retrieve per session stats                                                    #
#################################################################################

array set stats_array_per_session {
        interface_id
    "Interface Identifier"
        range_id
    "Range Identifier"
        pppoe_state
    "PPP State"
        close_mode
    "PPP Close Mode"
}
puts [string repeat "#" 80]
puts "Per session stats:"
puts [string repeat "#" 80]
puts ""

set sess_status [::ixia::pppox_stats      \
        -handle      $pppox_handle_1      \
        -mode        session              ]
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
        if {[string first "ipv6_addr" $key_2] >= 0} {
            # Validate ip addresses...
            set matched [regexp {([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9.]+)$} $current_value matched_str ip1 ip2 ip3 ip4]
            if {$matched} {
                lappend ok_log $current_value
            } else {
                set all_ok 0
                set ok_log "IPv6 address not matched: $current_value !"
            }
        }
    }
}
################################################################################


########################################
# Stop PPP                             #
########################################
set control_status [::ixia::pppox_control \
        -handle     $pppox_handle_0       \
        -action     disconnect            ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}

########################################
# Stop PPP                             #
########################################
set control_status [::ixia::pppox_control       \
        -handle         $pppox_handle_1         \
        -action         disconnect
        ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}

########################################
# Cleanup                              #
########################################
set cleanup_status [::ixia::cleanup_session     \
        -port_handle     $port0           \
        -reset                                  \
        ]
if {[keylget cleanup_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget cleanup_status log]"
    return 0
}
