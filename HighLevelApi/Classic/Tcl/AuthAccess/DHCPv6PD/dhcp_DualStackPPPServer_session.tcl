################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-20-2007 Mchakravarthy - created sample
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
#   This sample configures DHCP over L2TP and validates the stats              #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

################################################################################
# General script variables
################################################################################
set test_name                                   [info script]
set cfgError									0
set chassis_ip									10.205.16.54
set port_list									[list 2/5 2/6]
set break_locks									1
set tcl_server									127.0.0.1
set ixnetwork_tcl_server						127.0.0.1
set port_count									2
set detailed_logging							0
################################################################################
# START - Connect to the chassis
################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect

puts "Starting - $test_name - [clock format [clock seconds]]"
puts "Start connecting to chassis ..."

set connect_status [::ixia::connect                                        	   \
            -reset                                                             \
            -device               $chassis_ip                                  \
            -port_list            $port_list                                   \
            -break_locks          $break_locks                                 \
            -tcl_server           $tcl_server                                  \
            -ixnetwork_tcl_server $ixnetwork_tcl_server                        \
            -interactive          1                                            \
            ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}

set i 0
puts "Ixia port handles are:"
foreach port $port_handle {
    set port_$i $port
    puts $port    
    incr i
}

puts "End interface configuration L1 ..."
update idletasks
################################################################################
# END - Connect to the chassis
################################################################################

################################################################################
# Configure DHCP Hosts Dual Stack PPP - Client                                 #
################################################################################
puts "Configure DHCP Hosts Dual Stack PPP ..."
update idletasks

proc keylprint {keylist {space ""}} {
    upvar $keylist kl
    set result ""

    foreach key [keylkeys kl] {
            set value [keylget kl $key]
            if {[catch {keylkeys value}]} {
                append result "$space$key: $value\n"
            } else {
                set newspace "$space "
                append result "$space$key:\n[keylprint value $newspace]"
            }
    }
    return $result
}

set var_list {mode protocol encap dhcpv6_hosts_enable mac_addr mac_addr_step 
        num_sessions vlan_id_outer address_per_vlan vlan_id_outer_step vlan_id_outer_count 
        vlan_user_priority vlan_id address_per_svlan vlan_id_step vlan_id_count 
        qinq_incr_mode redial redial_timeout redial_max padi_req_timeout 
        max_padi_req padr_req_timeout actual_rate_downstream actual_rate_upstream 
        auth_mode auth_req_timeout config_req_timeout data_link echo_req 
        echo_req_interval echo_rsp ip_cp ipcp_req_timeout ipv6_pool_addr_prefix_len 
        ipv6_pool_prefix ipv6_pool_prefix_len local_magic max_auth_req max_configure_req 
        max_ipcp_req max_padr_req max_terminate_req password ppp_local_iid ppp_local_ip 
        ppp_local_ip_step ppp_peer_iid ppp_peer_ip term_req_timeout username 
        hosts_range_count hosts_range_ip_prefix hosts_range_subnet_count hosts_range_first_eui 
        hosts_range_eui_increment dhcp6_pd_client_range_use_vendor_class_id 
        dhcp6_pd_client_range_duid_enterprise_id dhcp6_pd_client_range_duid_type 
        dhcp6_pd_client_range_duid_vendor_id dhcp6_pd_client_range_duid_vendor_id_increment 
        dhcp6_pd_client_range_ia_id dhcp6_pd_client_range_ia_id_increment dhcp6_pd_client_range_ia_t1 
        dhcp6_pd_client_range_ia_t2 dhcp6_pd_client_range_param_request_list dhcp6_pd_client_range_renew_timer 
        dhcp6_pd_client_range_vendor_class_id port_role attempt_rate max_outstanding disconnect_rate 
        ipv6_global_address_mode dhcp6_pgdata_override_global_setup_rate dhcp6_pgdata_override_global_teardown_rate
        dhcp6_global_echo_ia_info dhcp6_global_max_outstanding_releases dhcp6_global_max_outstanding_requests 
        dhcp6_global_reb_max_rt dhcp6_global_reb_timeout dhcp6_global_rel_max_rc dhcp6_global_rel_timeout 
        dhcp6_global_ren_max_rt dhcp6_global_ren_timeout dhcp6_global_req_max_rc dhcp6_global_req_max_rt 
        dhcp6_global_req_timeout dhcp6_global_setup_rate_increment dhcp6_global_setup_rate_initial 
        dhcp6_global_setup_rate_max dhcp6_global_sol_max_rc dhcp6_global_sol_max_rt 
        dhcp6_global_sol_timeout dhcp6_global_teardown_rate_increment dhcp6_global_teardown_rate_initial 
        dhcp6_global_teardown_rate_max dhcp6_global_wait_for_completion}

set dhcpv6pd_type                                     client
set mode                                              add
set protocol                                          pppoe
set encap                                             ethernet_ii
set dhcpv6_hosts_enable                               1
set mac_addr                                          0C:A3:B3:FE:00:00
set mac_addr_step                                     00:00:00:00:00:01
set num_sessions                                      1
set ip_cp                                             dual_stack
set hosts_range_count                                 1
set hosts_range_ip_prefix                             64
set hosts_range_subnet_count                          1
set hosts_range_first_eui                             00:00:00:00:00:00:11:11
set hosts_range_eui_increment                         00:00:00:00:00:00:00:01
set dhcp6_pd_client_range_duid_type                   duid_llt
set dhcp6_pd_client_range_duid_enterprise_id          10
set dhcp6_pd_client_range_duid_vendor_id              10
set dhcp6_pd_client_range_duid_vendor_id_increment    1
set dhcp6_pd_client_range_use_vendor_class_id         0
set dhcp6_pd_client_range_ia_id                       10
set dhcp6_pd_client_range_ia_t1                       302400
set dhcp6_pd_client_range_ia_t2                       483840
set dhcp6_pd_client_range_param_request_list          [list 2 7 23 24]
set dhcp6_pd_client_range_renew_timer                 0
set dhcp6_pgdata_max_outstanding_releases             100000
set dhcp6_pgdata_max_outstanding_requests             100000
set dhcp6_pgdata_override_global_setup_rate           1
set dhcp6_pgdata_override_global_teardown_rate        0
set dhcp6_pgdata_setup_rate_increment                 0
set dhcp6_pgdata_setup_rate_initial                   10
set dhcp6_pgdata_setup_rate_max                       10
set dhcp6_pgdata_teardown_rate_increment              100000
set dhcp6_pgdata_teardown_rate_initial                100000
set dhcp6_pgdata_teardown_rate_max                    100000
set dhcp6_global_echo_ia_info                         1
set dhcp6_global_max_outstanding_releases             1500
set dhcp6_global_max_outstanding_requests             120
set dhcp6_global_reb_max_rt                           600
set dhcp6_global_reb_timeout                          15
set dhcp6_global_rel_max_rc                           7
set dhcp6_global_rel_timeout                          2
set dhcp6_global_ren_max_rt                           650
set dhcp6_global_ren_timeout                          15
set dhcp6_global_req_max_rc                           25
set dhcp6_global_req_max_rt                           35
set dhcp6_global_req_timeout                          2
set dhcp6_global_sol_max_rc                           12
set dhcp6_global_sol_max_rt                           550
set dhcp6_global_sol_timeout                          3
set dhcp6_global_wait_for_completion                  1
set port_role                                         access
set ipv6_global_address_mode                          dhcpv6_pd
set padi_req_timeout                                  10
set max_padi_req                                      5
set padr_req_timeout                                  10
set max_padr_req                                      5
set term_req_timeout                                  15
set max_terminate_req                                 3 
set echo_req_interval                                 10
set echo_req                                          0 
set config_req_timeout                                10
set max_configure_req                                 3 
set ipcp_req_timeout                                  10
set max_ipcp_req                                      3 
set auth_req_timeout                                  10
set max_auth_req                                      20
set ppp_local_iid                                     00:11:11:11:00:00:00:01
set ppp_peer_iid                                      00:11:22:11:00:00:00:01
set ipv6_pool_prefix                                  1:1:1::

set dsppp_status_client [::ixia::pppox_config                                                                 \
        -port_handle                                       $port_0                                            \
        -mode                                              $mode                                              \
        -protocol                                          $protocol                                          \
        -encap                                             $encap                                             \
        -dhcpv6_hosts_enable                               $dhcpv6_hosts_enable                               \
        -dhcpv6pd_type                                     $dhcpv6pd_type                                     \
        -num_sessions                                      $num_sessions                                      \
        -ip_cp                                             $ip_cp                                             \
        -hosts_range_count                                 $hosts_range_count                                 \
        -hosts_range_eui_increment                         $hosts_range_eui_increment                         \
        -hosts_range_first_eui                             $hosts_range_first_eui                             \
        -hosts_range_ip_prefix                             $hosts_range_ip_prefix                             \
        -hosts_range_subnet_count                          $hosts_range_subnet_count                          \
        -port_role                                         $port_role                                         \
        -ppp_local_iid                                     $ppp_local_iid                                     \
        -ppp_peer_iid                                      $ppp_peer_iid                                      \
        -ipv6_pool_prefix                                  $ipv6_pool_prefix                                  \
        -ipv6_global_address_mode                          $ipv6_global_address_mode                          \
        -auth_req_timeout                                  $auth_req_timeout                                  \
        -config_req_timeout                                $config_req_timeout                                \
        -echo_req                                          $echo_req                                          \
        -echo_req_interval                                 $echo_req_interval                                 \
        -ipcp_req_timeout                                  $ipcp_req_timeout                                  \
        -max_auth_req                                      $max_auth_req                                      \
        -max_configure_req                                 $max_configure_req                                 \
        -max_ipcp_req                                      $max_ipcp_req                                      \
        -max_padi_req                                      $max_padi_req                                      \
        -max_padr_req                                      $max_padr_req                                      \
        -max_terminate_req                                 $max_terminate_req                                 \
        -padi_req_timeout                                  $padi_req_timeout                                  \
        -padr_req_timeout                                  $padr_req_timeout                                  \
        -term_req_timeout                                  $term_req_timeout                                  \
    ]
    
if {[keylget dsppp_status_client status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dsppp_status_client log]"
    return 0
}
set dsppp_handle_client [keylget dsppp_status_client handle]

################################################################################
# Configure DHCP Hosts Dual Stack PPP - Server                                 #
################################################################################

# set dhcp6_pd_server_range_first_dns_server              20:0:2:0:0:0:0:2
# set dhcp6_pd_server_range_second_dns_server             20:0:2:0:0:0:0:3
set dhcpv6pd_type                                       server
set hosts_range_ip_prefix_addr                          3001::
set hosts_range_ip_prefix                               96
set hosts_range_ip_outer_prefix                         64
set dhcp6_pd_server_range_start_pool_address            2001::
set dhcp6_pd_server_range_subnet_prefix                 48
set lease_time_max                                      864000
set lease_time                                          86400

set port_role                                         network

set dsppp_status_server [::ixia::pppox_config                                                                 \
        -port_handle                                       $port_1                                            \
        -mode                                              $mode                                              \
        -protocol                                          $protocol                                          \
        -encap                                             $encap                                             \
        -dhcpv6_hosts_enable                               $dhcpv6_hosts_enable                               \
        -dhcpv6pd_type                                     $dhcpv6pd_type                                     \
        -dhcp6_pd_server_range_start_pool_address          $dhcp6_pd_server_range_start_pool_address          \
        -dhcp6_pd_server_range_subnet_prefix               $dhcp6_pd_server_range_subnet_prefix               \
        -num_sessions                                      $num_sessions                                      \
        -ip_cp                                             $ip_cp                                             \
        -hosts_range_count                                 $hosts_range_count                                 \
        -hosts_range_ip_prefix                             $hosts_range_ip_prefix                             \
        -hosts_range_subnet_count                          $hosts_range_subnet_count                          \
        -hosts_range_first_eui                             $hosts_range_first_eui                             \
        -hosts_range_eui_increment                         $hosts_range_eui_increment                         \
        -hosts_range_ip_prefix_addr                        $hosts_range_ip_prefix_addr                        \
        -hosts_range_ip_outer_prefix                       $hosts_range_ip_outer_prefix                       \
        -port_role                                         $port_role                                         \
        -auth_req_timeout                                  $auth_req_timeout                                  \
        -config_req_timeout                                $config_req_timeout                                \
        -echo_req                                          $echo_req                                          \
        -echo_req_interval                                 $echo_req_interval                                 \
        -ipcp_req_timeout                                  $ipcp_req_timeout                                  \
        -max_auth_req                                      $max_auth_req                                      \
        -max_configure_req                                 $max_configure_req                                 \
        -max_ipcp_req                                      $max_ipcp_req                                      \
        -max_padi_req                                      $max_padi_req                                      \
        -max_padr_req                                      $max_padr_req                                      \
        -max_terminate_req                                 $max_terminate_req                                 \
        -padi_req_timeout                                  $padi_req_timeout                                  \
        -padr_req_timeout                                  $padr_req_timeout                                  \
        -term_req_timeout                                  $term_req_timeout                                  \
        -ppp_local_iid                                     $ppp_local_iid                                     \
        -ppp_peer_iid                                      $ppp_peer_iid                                      \
        -ipv6_pool_prefix                                  $ipv6_pool_prefix                                  \
        -ipv6_global_address_mode                          $ipv6_global_address_mode                          \
    ]
    
if {[keylget dsppp_status_server status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dsppp_status_server log]"
    return 0
}
set dsppp_handle_server [keylget dsppp_status_server handle]

after 20000
#########################################
#  Retrieve aggregate session stats     #
#########################################

set ppp_handles [list $dsppp_handle_client $dsppp_handle_server]
set connect_status [::ixia::pppox_control   \
        -action         connect             \
    ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set pppox_ppp_stats_status [::ixia::pppox_stats \
        -mode           session                 \
        -handle         $ppp_handles            \
    ]
if {[keylget pppox_ppp_stats_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pppox_ppp_stats_status log]"
    return 0
}
puts [keylprint pppox_ppp_stats_status]

set pppox_dhcpv6_stats_status [::ixia::pppox_stats  \
        -mode           session_dhcpv6pd            \
        -port_handle    $port_handle                \
    ]
if {[keylget pppox_dhcpv6_stats_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pppox_dhcpv6_stats_status log]"
    return 0
}
puts [keylprint pppox_dhcpv6_stats_status]

set pppox_host_stats_status [::ixia::pppox_stats    \
        -mode           session_dhcp_hosts          \
        -handle         $ppp_handles                \
    ]
if {[keylget pppox_host_stats_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pppox_host_stats_status log]"
    return 0
}
puts [keylprint pppox_host_stats_status]

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
