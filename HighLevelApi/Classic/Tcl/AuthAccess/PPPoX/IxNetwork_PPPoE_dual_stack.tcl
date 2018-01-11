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
set port_list [list 3/1]

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



################################################################################
# Configure DHCP Hosts Dual Stack PPP                                          #
################################################################################
puts "Configure DHCP Hosts Dual Stack PPP ..."
update idletasks

set dsppp_status [::ixia::pppox_config                                          \
    -mode                                           add                         \
    -port_handle                                    $port0                      \
    -protocol                                       pppoe                       \
    -encap                                          ethernet_ii_qinq            \
    -dhcpv6_hosts_enable                            1                           \
    -mac_addr                                       AA:BB:CC:F0:00:00           \
    -mac_addr_step                                  00:00:00:00:00:01           \
    -num_sessions                                   2                           \
    -vlan_id_outer                                  10                          \
    -address_per_vlan                               1                           \
    -vlan_id_outer_step                             2                           \
    -vlan_id_outer_count                            2                           \
    -vlan_user_priority                             1                           \
    -vlan_id                                        100                         \
    -address_per_svlan                              1                           \
    -vlan_id_step                                   3                           \
    -vlan_id_count                                  2                           \
    -qinq_incr_mode                                 both                        \
    -redial                                         1                           \
    -redial_timeout                                 10                          \
    -redial_max                                     20                          \
    -padi_req_timeout                               10                          \
    -max_padi_req                                   5                           \
    -padr_req_timeout                               10                          \
    -actual_rate_downstream                         10                          \
    -actual_rate_upstream                           10                          \
    -auth_mode                                      chap                        \
    -auth_req_timeout                               10                          \
    -config_req_timeout                             10                          \
    -data_link                                      ethernet                    \
    -echo_req                                       0                           \
    -echo_req_interval                              10                          \
    -echo_rsp                                       1                           \
    -ip_cp                                          dual_stack                  \
    -ipcp_req_timeout                               10                          \
    -ipv6_pool_addr_prefix_len                      64                          \
    -ipv6_pool_prefix                               1:1:1::                     \
    -ipv6_pool_prefix_len                           48                          \
    -local_magic                                    1                           \
    -max_auth_req                                   20                          \
    -max_configure_req                              3                           \
    -max_ipcp_req                                   3                           \
    -max_padr_req                                   5                           \
    -max_terminate_req                              3                           \
    -password                                       cisco                       \
    -ppp_local_iid                                  00:11:11:11:00:00:00:01     \
    -ppp_local_ip                                   1.1.1.1                     \
    -ppp_local_ip_step                              0.0.0.1                     \
    -ppp_peer_iid                                   00:11:22:11:00:00:00:01     \
    -ppp_peer_ip                                    2.2.2.2                     \
    -term_req_timeout                               15                          \
    -username                                       cisco                       \
    -hosts_range_count                              2                           \
    -hosts_range_ip_prefix                          96                          \
    -hosts_range_subnet_count                       2                           \
    -hosts_range_first_eui                          ff:00:00:00:00:00:11:11     \
    -hosts_range_eui_increment                      ff:00:00:00:00:00:00:01     \
    -dhcp6_pd_client_range_use_vendor_class_id      1                           \
    -dhcp6_pd_client_range_duid_enterprise_id       11                          \
    -dhcp6_pd_client_range_duid_type                duid_en                     \
    -dhcp6_pd_client_range_duid_vendor_id           12                          \
    -dhcp6_pd_client_range_duid_vendor_id_increment 1                           \
    -dhcp6_pd_client_range_ia_id                    13                          \
    -dhcp6_pd_client_range_ia_id_increment          1                           \
    -dhcp6_pd_client_range_ia_t1                    302300                      \
    -dhcp6_pd_client_range_ia_t2                    484840                      \
    -dhcp6_pd_client_range_param_request_list       [list 2 7 11 23 24]         \
    -dhcp6_pd_client_range_renew_timer              0                           \
    -dhcp6_pd_client_range_vendor_class_id          "HLTAPI DHCP Client"        \
    -port_role                                      access                      \
    -attempt_rate                                   300                         \
    -max_outstanding                                300                         \
    -disconnect_rate                                300                         \
    -ipv6_global_address_mode                       dhcpv6_pd                   \
    -dhcp6_pgdata_override_global_setup_rate        0                           \
    -dhcp6_pgdata_override_global_teardown_rate     0                           \
    -dhcp6_global_echo_ia_info                      0                           \
    -dhcp6_global_max_outstanding_releases          500                         \
    -dhcp6_global_max_outstanding_requests          20                          \
    -dhcp6_global_reb_max_rt                        600                         \
    -dhcp6_global_reb_timeout                       10                          \
    -dhcp6_global_rel_max_rc                        5                           \
    -dhcp6_global_rel_timeout                       1                           \
    -dhcp6_global_ren_max_rt                        600                         \
    -dhcp6_global_ren_timeout                       10                          \
    -dhcp6_global_req_max_rc                        10                          \
    -dhcp6_global_req_max_rt                        30                          \
    -dhcp6_global_req_timeout                       1                           \
    -dhcp6_global_setup_rate_increment              0                           \
    -dhcp6_global_setup_rate_initial                10                          \
    -dhcp6_global_setup_rate_max                    10                          \
    -dhcp6_global_sol_max_rc                        3                           \
    -dhcp6_global_sol_max_rt                        120                         \
    -dhcp6_global_sol_timeout                       4                           \
    -dhcp6_global_teardown_rate_increment           50                          \
    -dhcp6_global_teardown_rate_initial             50                          \
    -dhcp6_global_teardown_rate_max                 500                         \
    -dhcp6_global_wait_for_completion               1                           \
]
    
if {[keylget dsppp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dsppp_status log]"
    return 0
}

set dsppp_handle [keylget dsppp_status handle]


################################################################################
# Modify DHCP Hosts Dual Stack PPP                                             #
################################################################################
puts "Modify DHCP Hosts Dual Stack PPP   ..."
update idletasks

set dsppp_status [::ixia::pppox_config                                          \
    -mode                                           modify                      \
    -handle                                         $dsppp_handle               \
    -port_handle                                    $port0                      \
    -ip_cp                                          ipv6_cp                     \
    -dhcp6_pd_client_range_duid_vendor_id           22                          \
    -ipv6_global_address_mode                       icmpv6                      \
    -dhcp6_global_ren_max_rt                        655                         \
    -protocol                                       pppoe                       \
    -encap                                          ethernet_ii_qinq            \
    -num_sessions                                   2                           \
]    
if {[keylget dsppp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dsppp_status log]"
    return 0
}

################################################################################
# The next section is only relevant for a DUT setup                            #
################################################################################

# puts "\nStarting DSPPP Clients..."
# set control_status2 [::ixia::pppox_control \
#      -handle     $dsppp_handle             \
#      -action     connect               ]
# if {[keylget control_status2 status] != $::SUCCESS} {
#  return "FAIL - $test_name - [keylget control_status2 log]"
# }

# #########################################
# #  Retrieve aggregate session stats     #
# #########################################

# set aggr_status [::ixia::pppox_stats    \
#         -port_handle $port0             \
#         -mode   aggregate            ]
# if {[keylget aggr_status status] != $::SUCCESS} {
#     puts "FAIL - $test_name - [keylget aggr_status log]"
#     return 0
# }
# set sess_num       [keylget aggr_status $port0.aggregate.num_sessions]
# set sess_count_up  [keylget aggr_status $port0.aggregate.connected]
# 
# set dhcpv6pd_sess_num       [keylget aggr_status $port0.aggregate.dhcpv6pd_sessions_initiated]
# set dhcpv6pd_sess_count_up  [keylget aggr_status $port0.aggregate.dhcpv6pd_sessions_succeeded]
# 
# set dhcph_sess_num          [keylget aggr_status $port0.aggregate.dhcp_hosts_sessions_initiated]
# set dhcph_sess_count_up     [keylget aggr_status $port0.aggregate.dhcp_hosts_sessions_succeeded]
# 
# puts "        Number of PPPoE sessions                  = $sess_num"
# puts "        Number of PPPoE connected sessions        = $sess_count_up\n"
# puts "        Number of DHCPv6 PD sessions              = $dhcpv6pd_sess_num"      
# puts "        Number of DHCPv6 PD connected sessions    = $dhcpv6pd_sess_count_up\n"
# puts "        Number of DHCPv6 Hosts sessions           = $dhcph_sess_num"
# puts "        Number of DHCPv6 Hosts connected sessions = $dhcph_sess_count_up\n"


################################################################################
# Remove DHCP Hosts Dual Stack PPP                                             #
################################################################################
puts "Remove DHCP Hosts Dual Stack PPP   ..."
update idletasks

set dsppp_status [::ixia::pppox_config                                          \
        -mode                                           remove                  \
        -handle                                         $dsppp_handle           \
        -port_handle                                    $port0                  \
        -protocol                                       pppoe                   \
        -encap                                          ethernet_ii_qinq        \
        -num_sessions                                   2                       \
    ]
    
if {[keylget dsppp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dsppp_status log]"
    return 0
}

puts "Done Remove DHCP Hosts Dual Stack PPP   ..."


puts "SUCCESS - $test_name - [clock format [clock seconds]]"