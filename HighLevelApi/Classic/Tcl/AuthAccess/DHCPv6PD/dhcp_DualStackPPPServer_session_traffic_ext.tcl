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
#   This sample configures Dual Stack PPP server and sessions                  #
#  	 and sends traffic and validates stats							           #
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

################################################################################
# END - Interface configuration - L1
################################################################################

################################################################################
# START - PPPoX configuration - Access Port
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    Call to ::ixia::pppox_config using all parameters.                        #
#    Use this call as a starting point for specific PPPoX configurations.      #
#                                                                              #
################################################################################

set var_list {
    mode handle num_sessions port_handle protocol port_role attempt_rate disconnect_rate
    max_outstanding addr_count_per_vci addr_count_per_vpi encap mac_addr mac_addr_step
    pvc_incr_mode vci vci_count vci_step vlan_id vlan_id_count vlan_id_outer
    vlan_id_outer_count vlan_id_outer_step vlan_id_step vlan_user_priority
    vpi vpi_count vpi_step qinq_incr_mode
    ac_name ac_select_list ac_select_mode max_padi_req max_padr_req padi_req_timeout
    padr_req_timeout redial redial_max redial_timeout service_name service_type
    domain_group_map config_req_timeout echo_req echo_req_interval echo_rsp max_configure_req
    max_terminate_req local_magic term_req_timeout ip_cp ipcp_req_timeout
    ipv6_pool_addr_prefix_len ipv6_pool_prefix ipv6_pool_prefix_len max_ipcp_req
    ppp_local_ip ppp_local_ip_step ppp_local_iid ppp_peer_ip ppp_peer_ip_step ppp_peer_iid
    auth_mode auth_req_timeout max_auth_req password password_wildcard username
    username_wildcard wildcard_pound_end wildcard_pound_start wildcard_question_end
    wildcard_question_start actual_rate_downstream actual_rate_upstream agent_circuit_id
    agent_remote_id data_link enable_client_signal_iwf enable_client_signal_loop_char
    enable_client_signal_loop_encap enable_client_signal_loop_id enable_server_signal_iwf
    enable_server_signal_loop_char enable_server_signal_loop_encap
    enable_server_signal_loop_id intermediate_agent intermediate_agent_encap1
    intermediate_agent_encap2 ch ca po
}

set pppox_session_count 5

########################################
# GENERAL                              #
########################################
set mode                                  add                           ;# CHOICES add remove modify; DEFAULT add
set handle                                pppox_handle                  ;# Handle of PPPox session to modify
set num_sessions                          $pppox_session_count          ;# RANGE 1-32000; MANDATORY
foreach {ch ca po}                        [split $port_0 /] {}
set protocol                              pppoe                         ;# CHOICES pppoa pppoeoa pppoe; MANDATORY
set port_role                             access                        ;# CHOICES access network; DEFAULT access


########################################
# GLOBAL SETTINGS                      #
########################################
set attempt_rate                          100                           ;# RANGE  1-300   DEFAULT 100
set disconnect_rate                       100                           ;# RANGE  1-300   DEFAULT 100
set max_outstanding                       1000                          ;# RANGE 1-1000   DEFAULT 1000


########################################
# BASIC                                #
########################################
set addr_count_per_vci                    1                             ;# RANGE 1-65535  DEFAULT 1
set addr_count_per_vpi                    1                             ;# RANGE 1-65535  DEFAULT 1
set encap                                 ethernet_ii                   ;# CHOICES vc_mux llcsnap ethernet_ii ethernet_ii_vlan ethernet_ii_qinq llcsnap_nofcs; MANDATORY
set mac_addr                              00:0b:0c:0a:00:01       ;# MAC            DEFAULT 00:$ch$ch:$ca$ca:$po$po:$cfgNo$cfgNo:01
set mac_addr_step                         00:00:00:00:00:01             ;# MAC            DEFAULT 00:00:00:00:00:01
set pvc_incr_mode                         vci                           ;# CHOICES vpi vci both  DEFAULT vci
set vci                                   32                            ;# RANGE 1-65535  DEFAULT 32
set vci_count                             1                             ;# RANGE 1-256    DEFAULT 1
set vci_step                              1                             ;# RANGE 1-65534  DEFAULT 1
set vlan_id                               1                             ;# RANGE 1-4094   DEFAULT 1
set vlan_id_count                         4094                          ;# RANGE 1-4094   DEFAULT 4094
set vlan_id_outer                         1                             ;# RANGE 1-4094   DEFAULT 1
set vlan_id_outer_count                   4094                          ;# RANGE 1-4094   DEFAULT 4094
set vlan_id_outer_step                    1                             ;# RANGE 1-4094   DEFAULT 1
set vlan_id_step                          1                             ;# RANGE 1-4094   DEFAULT 1
set vlan_user_priority                    0                             ;# RANGE 0-7      DEFAULT 0
set vpi                                   0                             ;# RANGE 0-255    DEFAULT 0
set vpi_count                             1                             ;# RANGE 1-256    DEFAULT 1
set vpi_step                              1                             ;# RANGE 1-255    DEFAULT 1
set qinq_incr_mode                        both                          ;# CHOICES inner outer both  DEFAULT both


########################################
# PPPoX                                #
########################################
set ac_name                               ""                            ;# ANY                   DEFAULT ""
set ac_select_list                        ""                            ;# KEYLIST               DEFAULT ""
set ac_select_mode                        first_responding              ;# CHOICES first_responding ac_mac ac_name service_name      DEFAULT first_responding
set max_padi_req                          10                            ;# RANGE 1-65535         DEFAULT 10
set max_padr_req                          10                            ;# RANGE 1-65535         DEFAULT 10
# set padi_include_tag                      0                             ;# CHOICES 0 1
# set pado_include_tag                      0                             ;# CHOICES 0 1
# set padr_include_tag                      0                             ;# CHOICES 0 1
# set pads_include_tag                      0                             ;# CHOICES 0 1
set padi_req_timeout                      6                             ;# RANGE 1-65535         DEFAULT 5
set padr_req_timeout                      6                             ;# RANGE 1-65535         DEFAULT 5
set redial                                1                             ;# CHOICES 0 1           DEFAULT 1
set redial_max                            25                            ;# RANGE 1-255           DEFAULT 20
set redial_timeout                        15                            ;# RANGE 1-65535         DEFAULT 10
set service_name                          ""                            ;# ANY                   DEFAULT ""
set service_type                          any                           ;# CHOICES any name      DEFAULT any


########################################
# DOMAIN GROUP                         #
########################################
set domain_group_map                      ""                            ;# ANY                   DEFAULT ""


########################################
# LCP                                  #
########################################
set config_req_timeout                    6                             ;# RANGE  1-65535        DEFAULT 5
set echo_req                              1                             ;# RANGE 0-1             DEFAULT 0
set echo_req_interval                     70                            ;# RANGE 1-3600          DEFAULT 60
set echo_rsp                              1                             ;# RANGE 0-1             DEFAULT 1
set max_configure_req                     15                            ;# RANGE 1-255           DEFAULT 10
set max_terminate_req                     15                            ;# RANGE 1-65535         DEFAULT 10
set local_magic                           1                             ;# RANGE 0-1             DEFAULT 1
set term_req_timeout                      6                             ;# RANGE 1-65535         DEFAULT 5


########################################
# NCP                                  #
########################################
set ip_cp                                 ipv6_cp                       ;# CHOICES ipv4_cp ipv6_cp   DEFAULT ipv4_cp
set ipcp_req_timeout                      6                             ;# RANGE 1-65535    DEFAULT 5
set ipv6_pool_addr_prefix_len             64                            ;# NUMERIC          DEFAULT 64
set ipv6_pool_prefix                      ::                            ;# ANY              DEFAULT ::
set ipv6_pool_prefix_len                  48                            ;# NUMERIC          DEFAULT 48
set max_ipcp_req                          10                            ;# RANGE 1-255      DEFAULT 10
set ppp_local_ip                          1.1.1.100                     ;# IPV4             DEFAULT 1.1.1.1
set ppp_local_ip_step                     0.0.0.1                       ;# IPV4             DEFAULT 0.0.0.1
set ppp_local_iid                         {00 11 22 33 44 55 66 00}     ;# ANY              DEFAULT {00 00 00 00 00 00 00 00}
set ppp_peer_ip                           1.1.1.1                       ;# IPV4             DEFAULT 1.1.1.1
set ppp_peer_ip_step                      0.0.0.1                       ;# IPV4             DEFAULT 0.0.0.1
set ppp_peer_iid                          {00 77 88 99 aa bb cc 00}     ;# ANY              DEFAULT {00 00 00 00 00 00 00 00}


########################################
# AUTHENTICATION                       #
########################################
set auth_mode                             none                          ;# CHOICES none pap chap pap_or_chap     DEFAULT none
set auth_req_timeout                      6                             ;# RANGE  1-65535    DEFAULT 5
set max_auth_req                          15                            ;# RANGE 1-65535     DEFAULT 10
set password                              ""                            ;# ANY               DEFAULT ""
set password_wildcard                     0                             ;# RANGE 0-1         DEFAULT 0
set username                              ""                            ;# ANY               DEFAULT ""
set username_wildcard                     0                             ;# RANGE 0-1         DEFAULT 0
set wildcard_pound_end                    0                             ;# RANGE 0-65535     DEFAULT 0
set wildcard_pound_start                  0                             ;# RANGE 0-65535     DEFAULT 0
set wildcard_question_end                 0                             ;# RANGE 0-65535     DEFAULT 0
set wildcard_question_start               0                             ;# RANGE 0-65535     DEFAULT 0


########################################
# INTERMEDIATE AGENT                   #
########################################
set actual_rate_downstream                10                             ;# RANGE   1-65535  DEFAULT 10
set actual_rate_upstream                  10                             ;# RANGE   1-65535  DEFAULT 10
set agent_circuit_id                      ""                             ;# ANY              DEFAULT ""
set agent_remote_id                       ""                             ;# ANY              DEFAULT ""
set data_link                             ethernet                       ;# CHOICES atm_aal5 ethernet    DEFAULT ethernet
set enable_client_signal_iwf              0                              ;# CHOICES 0 1      DEFAULT 0    
set enable_client_signal_loop_char        0                              ;# CHOICES 0 1      DEFAULT 0
set enable_client_signal_loop_encap       0                              ;# CHOICES 0 1      DEFAULT 0
set enable_client_signal_loop_id          0                              ;# CHOICES 0 1      DEFAULT 0
set enable_server_signal_iwf              0                              ;# CHOICES 0 1      DEFAULT 0
set enable_server_signal_loop_char        0                              ;# CHOICES 0 1      DEFAULT 0
set enable_server_signal_loop_encap       0                              ;# CHOICES 0 1      DEFAULT 0
set enable_server_signal_loop_id          0                              ;# CHOICES 0 1      DEFAULT 0
# set intermediate_agent                    0                              ;# CHOICES 0 1      DEFAULT 0
set intermediate_agent_encap1             untagged_eth                   ;# CHOICES na untagged_eth single_tagged_eth        DEFAULT untagged_eth
set intermediate_agent_encap2             na                             ;# CHOICES na pppoa_llc pppoa_null ipoa_llc ipoa_null eth_aal5_llc_fcs eth_aal5_llc_no_fcs eth_aal5_null_fcs eth_aal5_null_no_fcs       DEFAULT na


########################################
# Start PPPoX Call                     #
########################################
set config_status [::ixia::pppox_config                                        \
		-mode                               $mode                              \
		-handle                             $handle                            \
		-num_sessions                       $num_sessions                      \
		-port_handle                        $port_0                            \
		-protocol                           $protocol                          \
		-port_role                          $port_role                         \
		-attempt_rate                       $attempt_rate                      \
		-disconnect_rate                    $disconnect_rate                   \
		-max_outstanding                    $max_outstanding                   \
		-addr_count_per_vci                 $addr_count_per_vci                \
		-addr_count_per_vpi                 $addr_count_per_vpi                \
		-encap                              $encap                             \
		-mac_addr                           $mac_addr                          \
		-mac_addr_step                      $mac_addr_step                     \
		-pvc_incr_mode                      $pvc_incr_mode                     \
		-vci                                $vci                               \
		-vci_count                          $vci_count                         \
		-vci_step                           $vci_step                          \
		-vlan_id                            $vlan_id                           \
		-vlan_id_count                      $vlan_id_count                     \
		-vlan_id_outer                      $vlan_id_outer                     \
		-vlan_id_outer_count                $vlan_id_outer_count               \
		-vlan_id_outer_step                 $vlan_id_outer_step                \
		-vlan_id_step                       $vlan_id_step                      \
		-vlan_user_priority                 $vlan_user_priority                \
		-vpi                                $vpi                               \
		-vpi_count                          $vpi_count                         \
		-vpi_step                           $vpi_step                          \
		-qinq_incr_mode                     $qinq_incr_mode                    \
		-ac_name                            $ac_name                           \
		-ac_select_list                     $ac_select_list                    \
		-ac_select_mode                     $ac_select_mode                    \
		-max_padi_req                       $max_padi_req                      \
		-max_padr_req                       $max_padr_req                      \
		-padi_req_timeout                   $padi_req_timeout                  \
		-padr_req_timeout                   $padr_req_timeout                  \
		-redial                             $redial                            \
		-redial_max                         $redial_max                        \
		-redial_timeout                     $redial_timeout                    \
		-service_name                       $service_name                      \
		-service_type                       $service_type                      \
		-domain_group_map                   $domain_group_map                  \
		-config_req_timeout                 $config_req_timeout                \
		-echo_req                           $echo_req                          \
		-echo_req_interval                  $echo_req_interval                 \
		-echo_rsp                           $echo_rsp                          \
		-max_configure_req                  $max_configure_req                 \
		-max_terminate_req                  $max_terminate_req                 \
		-local_magic                        $local_magic                       \
		-term_req_timeout                   $term_req_timeout                  \
		-ip_cp                              $ip_cp                             \
		-ipcp_req_timeout                   $ipcp_req_timeout                  \
		-ipv6_pool_addr_prefix_len          $ipv6_pool_addr_prefix_len         \
		-ipv6_pool_prefix                   $ipv6_pool_prefix                  \
		-ipv6_pool_prefix_len               $ipv6_pool_prefix_len              \
		-max_ipcp_req                       $max_ipcp_req                      \
		-ppp_local_ip                       $ppp_local_ip                      \
		-ppp_local_ip_step                  $ppp_local_ip_step                 \
		-ppp_local_iid                      $ppp_local_iid                     \
		-ppp_peer_ip                        $ppp_peer_ip                       \
		-ppp_peer_ip_step                   $ppp_peer_ip_step                  \
		-ppp_peer_iid                       $ppp_peer_iid                      \
		-auth_mode                          $auth_mode                         \
		-auth_req_timeout                   $auth_req_timeout                  \
		-max_auth_req                       $max_auth_req                      \
		-password                           $password                          \
		-password_wildcard                  $password_wildcard                 \
		-username                           $username                          \
		-username_wildcard                  $username_wildcard                 \
		-wildcard_pound_end                 $wildcard_pound_end                \
		-wildcard_pound_start               $wildcard_pound_start              \
		-wildcard_question_end              $wildcard_question_end             \
		-wildcard_question_start            $wildcard_question_start           \
		-actual_rate_downstream             $actual_rate_downstream            \
		-actual_rate_upstream               $actual_rate_upstream              \
		-agent_circuit_id                   $agent_circuit_id                  \
		-agent_remote_id                    $agent_remote_id                   \
		-data_link                          $data_link                         \
		-enable_client_signal_iwf           $enable_client_signal_iwf          \
		-enable_client_signal_loop_char     $enable_client_signal_loop_char    \
		-enable_client_signal_loop_encap    $enable_client_signal_loop_encap   \
		-enable_client_signal_loop_id       $enable_client_signal_loop_id      \
		-enable_server_signal_iwf           $enable_server_signal_iwf          \
		-enable_server_signal_loop_char     $enable_server_signal_loop_char    \
		-enable_server_signal_loop_encap    $enable_server_signal_loop_encap   \
		-enable_server_signal_loop_id       $enable_server_signal_loop_id      \
		-intermediate_agent_encap1          $intermediate_agent_encap1         \
		-intermediate_agent_encap2          $intermediate_agent_encap2         \
	]
if {[keylget config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget config_status log]"
    return 0
}

set pppox_handle_0 [keylget config_status handle]
puts "Ixia pppox_handle is $pppox_handle_0 "

foreach item $var_list { catch {unset item}}

########################################
# End PPPoX Call                       #
########################################
set dhcp6_client_range_duid_type                   duid_llt
set dhcp6_client_range_duid_enterprise_id          10
set dhcp6_client_range_duid_vendor_id              10
set dhcp6_client_range_duid_vendor_id_increment    1
set dhcp6_client_range_use_vendor_class_id         1
set dhcp6_client_range_ia_id                       10
set dhcp6_client_range_ia_t1                       302400
set dhcp6_client_range_ia_t2                       483840
set dhcp6_client_range_param_request_list          [list 2 7 23 24]
set dhcp6_client_range_renew_timer                 0
set dhcp6_pgdata_max_outstanding_releases             500
set dhcp6_pgdata_max_outstanding_requests             20
set dhcp6_pgdata_override_global_setup_rate           0
set dhcp6_pgdata_override_global_teardown_rate        0
set dhcp6_pgdata_setup_rate_increment                 0
set dhcp6_pgdata_setup_rate_initial                   10
set dhcp6_pgdata_setup_rate_max                       10
set dhcp6_pgdata_teardown_rate_increment              50
set dhcp6_pgdata_teardown_rate_initial                50
set dhcp6_pgdata_teardown_rate_max                    500
set dhcp6_global_echo_ia_info                         0
set dhcp6_global_max_outstanding_releases             500
set dhcp6_global_max_outstanding_requests             20
set dhcp6_global_reb_max_rt                           500
set dhcp6_global_reb_timeout                          10
set dhcp6_global_rel_max_rc                           5
set dhcp6_global_rel_timeout                          1
set dhcp6_global_ren_max_rt                           600
set dhcp6_global_ren_timeout                          10
set dhcp6_global_req_max_rc                           10
set dhcp6_global_req_max_rt                           30
set dhcp6_global_req_timeout                          1
set dhcp6_global_sol_max_rc                           3
set dhcp6_global_sol_max_rt                           120
set dhcp6_global_sol_timeout                          4
set dhcp6_global_setup_rate_increment                 0
set dhcp6_global_setup_rate_initial                   10
set dhcp6_global_setup_rate_max                       10
set dhcp6_global_teardown_rate_increment              50
set dhcp6_global_teardown_rate_initial                50
set dhcp6_global_teardown_rate_max                    500
set dhcp6_global_wait_for_completion                  0
set hosts_range_count                                 2
set hosts_range_ip_prefix                             96
set hosts_range_subnet_count                          2
set hosts_range_first_eui                             00:00:00:00:00:00:11:11
set hosts_range_eui_increment                         00:00:00:00:00:00:00:01

set dsppp_status_client [::ixia::dhcp_client_extension_config													\
        -handle													$pppox_handle_0                                 \
        -dhcp6_client_range_duid_type							$dhcp6_client_range_duid_type                   \
        -dhcp6_client_range_duid_enterprise_id					$dhcp6_client_range_duid_enterprise_id          \
        -dhcp6_client_range_duid_vendor_id						$dhcp6_client_range_duid_vendor_id              \
        -dhcp6_client_range_duid_vendor_id_increment			$dhcp6_client_range_duid_vendor_id_increment    \
        -dhcp6_client_range_param_request_list					$dhcp6_client_range_param_request_list          \
        -dhcp6_client_range_use_vendor_class_id					$dhcp6_client_range_use_vendor_class_id         \
        -dhcp6_pgdata_max_outstanding_requests					$dhcp6_pgdata_max_outstanding_requests			\
        -dhcp6_pgdata_override_global_setup_rate				$dhcp6_pgdata_override_global_setup_rate		\
        -dhcp6_pgdata_setup_rate_increment						$dhcp6_pgdata_setup_rate_increment				\
        -dhcp6_pgdata_setup_rate_initial						$dhcp6_pgdata_setup_rate_initial				\
        -dhcp6_pgdata_setup_rate_max							$dhcp6_pgdata_setup_rate_max					\
        -dhcp6_global_max_outstanding_requests					$dhcp6_global_max_outstanding_requests			\
        -dhcp6_global_setup_rate_increment						$dhcp6_global_setup_rate_increment				\
        -dhcp6_global_setup_rate_initial						$dhcp6_global_setup_rate_initial				\
        -dhcp6_global_setup_rate_max							$dhcp6_global_setup_rate_max					]
		
if {[keylget dsppp_status_client status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dsppp_status_client log]"
    return 0
}

set dsppp_handle_client [keylget dsppp_status_client handle]

################################################################################
# END - PPPoX configuration - Access Port
################################################################################

################################################################################
# START - PPPoX configuration - Network Port
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    Call to ::ixia::pppox_config using all parameters.                        #
#    Use this call as a starting point for specific PPPoX configurations.      #
#                                                                              #
################################################################################

set var_list {
      mode handle num_sessions port_handle protocol port_role attempt_rate disconnect_rate
      max_outstanding addr_count_per_vci addr_count_per_vpi encap mac_addr mac_addr_step
      pvc_incr_mode vci vci_count vci_step vlan_id vlan_id_count vlan_id_outer
      vlan_id_outer_count vlan_id_outer_step vlan_id_step vlan_user_priority
      vpi vpi_count vpi_step qinq_incr_mode
      ac_name ac_select_list ac_select_mode max_padi_req max_padr_req padi_req_timeout
      padr_req_timeout redial redial_max redial_timeout service_name service_type
      domain_group_map config_req_timeout echo_req echo_req_interval echo_rsp max_configure_req
      max_terminate_req local_magic term_req_timeout ip_cp ipcp_req_timeout
      ipv6_pool_addr_prefix_len ipv6_pool_prefix ipv6_pool_prefix_len max_ipcp_req
      ppp_local_ip ppp_local_ip_step ppp_local_iid ppp_peer_ip ppp_peer_ip_step ppp_peer_iid
      auth_mode auth_req_timeout max_auth_req password password_wildcard username
      username_wildcard wildcard_pound_end wildcard_pound_start wildcard_question_end
      wildcard_question_start actual_rate_downstream actual_rate_upstream agent_circuit_id
      agent_remote_id data_link enable_client_signal_iwf enable_client_signal_loop_char
      enable_client_signal_loop_encap enable_client_signal_loop_id enable_server_signal_iwf
      enable_server_signal_loop_char enable_server_signal_loop_encap
      enable_server_signal_loop_id intermediate_agent intermediate_agent_encap1
      intermediate_agent_encap2 ch ca po
}

########################################
# GENERAL                              #
########################################
set mode                                  add                           ;# CHOICES add remove modify; DEFAULT add
set handle                                pppox_handle                  ;# Handle of PPPox session to modify
set num_sessions                          $pppox_session_count          ;# RANGE 1-32000; MANDATORY
foreach {ch ca po}                        [split $port_1 /] {}
set protocol                              pppoe                         ;# CHOICES pppoa pppoeoa pppoe; MANDATORY
set port_role                             network                       ;# CHOICES access network; DEFAULT access


########################################
# GLOBAL SETTINGS                      #
########################################
set attempt_rate                          100                           ;# RANGE  1-300   DEFAULT 100
set disconnect_rate                       100                           ;# RANGE  1-300   DEFAULT 100
set max_outstanding                       1000                          ;# RANGE 1-1000   DEFAULT 1000


########################################
# BASIC                                #
########################################
set addr_count_per_vci                    1                             ;# RANGE 1-65535  DEFAULT 1
set addr_count_per_vpi                    1                             ;# RANGE 1-65535  DEFAULT 1
set encap                                 ethernet_ii                   ;# CHOICES vc_mux llcsnap ethernet_ii ethernet_ii_vlan ethernet_ii_qinq llcsnap_nofcs; MANDATORY
set mac_addr                              00:01:04:0a:00:01       ;# MAC            DEFAULT 00:$ch$ch:$ca$ca:$po$po:$cfgNo$cfgNo:01
set mac_addr_step                         00:00:00:00:00:01             ;# MAC            DEFAULT 00:00:00:00:00:01
set pvc_incr_mode                         vci                           ;# CHOICES vpi vci both  DEFAULT vci
set vci                                   32                            ;# RANGE 1-65535  DEFAULT 32
set vci_count                             1                             ;# RANGE 1-256    DEFAULT 1
set vci_step                              1                             ;# RANGE 1-65534  DEFAULT 1
set vlan_id                               1                             ;# RANGE 1-4094   DEFAULT 1
set vlan_id_count                         4094                          ;# RANGE 1-4094   DEFAULT 4094
set vlan_id_outer                         1                             ;# RANGE 1-4094   DEFAULT 1
set vlan_id_outer_count                   4094                          ;# RANGE 1-4094   DEFAULT 4094
set vlan_id_outer_step                    1                             ;# RANGE 1-4094   DEFAULT 1
set vlan_id_step                          1                             ;# RANGE 1-4094   DEFAULT 1
set vlan_user_priority                    0                             ;# RANGE 0-7      DEFAULT 0
set vpi                                   0                             ;# RANGE 0-255    DEFAULT 0
set vpi_count                             1                             ;# RANGE 1-256    DEFAULT 1
set vpi_step                              1                             ;# RANGE 1-255    DEFAULT 1
set qinq_incr_mode                        both                          ;# CHOICES inner outer both  DEFAULT both


########################################
# PPPoX                                #
########################################
set ac_name                               ""                            ;# ANY                   DEFAULT ""
set ac_select_list                        ""                            ;# KEYLIST               DEFAULT ""
set ac_select_mode                        first_responding              ;# CHOICES first_responding ac_mac ac_name service_name      DEFAULT first_responding
set max_padi_req                          10                            ;# RANGE 1-65535         DEFAULT 10
set max_padr_req                          10                            ;# RANGE 1-65535         DEFAULT 10
# set padi_include_tag                      0                             ;# CHOICES 0 1
# set pado_include_tag                      0                             ;# CHOICES 0 1
# set padr_include_tag                      0                             ;# CHOICES 0 1
# set pads_include_tag                      0                             ;# CHOICES 0 1
set padi_req_timeout                      5                             ;# RANGE 1-65535         DEFAULT 5
set padr_req_timeout                      5                             ;# RANGE 1-65535         DEFAULT 5
set redial                                1                             ;# CHOICES 0 1           DEFAULT 1
set redial_max                            20                            ;# RANGE 1-255           DEFAULT 20
set redial_timeout                        10                            ;# RANGE 1-65535         DEFAULT 10
set service_name                          ""                            ;# ANY                   DEFAULT ""
set service_type                          any                           ;# CHOICES any name      DEFAULT any


########################################
# DOMAIN GROUP                         #
########################################
set domain_group_map                      ""                            ;# ANY                   DEFAULT ""


########################################
# LCP                                  #
########################################
set config_req_timeout                    5                             ;# RANGE  1-65535        DEFAULT 5
set echo_req                              0                             ;# RANGE 0-1             DEFAULT 0
set echo_req_interval                     60                            ;# RANGE 1-3600          DEFAULT 60
set echo_rsp                              1                             ;# RANGE 0-1             DEFAULT 1
set max_configure_req                     10                            ;# RANGE 1-255           DEFAULT 10
set max_terminate_req                     10                            ;# RANGE 1-65535         DEFAULT 10
set local_magic                           1                             ;# RANGE 0-1             DEFAULT 1
set term_req_timeout                      5                             ;# RANGE 1-65535         DEFAULT 5


########################################
# NCP                                  #
########################################
set ip_cp                                 ipv6_cp                       ;# CHOICES ipv4_cp ipv6_cp   DEFAULT ipv4_cp
set ipcp_req_timeout                      5                             ;# RANGE 1-65535    DEFAULT 5
set ipv6_pool_addr_prefix_len             64                            ;# NUMERIC          DEFAULT 64
set ipv6_pool_prefix                      0002:0003:0002:0000::         ;# ANY              DEFAULT ::
set ipv6_pool_prefix_len                  48                            ;# NUMERIC          DEFAULT 48
set max_ipcp_req                          10                            ;# RANGE 1-255      DEFAULT 10
set ppp_local_ip                          1.1.1.1                       ;# IPV4             DEFAULT 1.1.1.1
set ppp_local_ip_step                     0.0.0.1                       ;# IPV4             DEFAULT 0.0.0.1
set ppp_local_iid                         "00 02 03 02 00 00 00 01"     ;# ANY              DEFAULT {00 00 00 00 00 00 00 00}
set ppp_peer_ip                           1.1.1.100                     ;# IPV4             DEFAULT 1.1.1.1
set ppp_peer_ip_step                      0.0.0.1                       ;# IPV4             DEFAULT 0.0.0.1
set ppp_peer_iid                          "00 02 03 02 00 10 00 01"     ;# ANY              DEFAULT {00 00 00 00 00 00 00 00}


########################################
# AUTHENTICATION                       #
########################################
set auth_mode                             none                          ;# CHOICES none pap chap pap_or_chap     DEFAULT none
set auth_req_timeout                      5                             ;# RANGE  1-65535    DEFAULT 5
set max_auth_req                          10                            ;# RANGE 1-65535     DEFAULT 10
set password                              ""                            ;# ANY               DEFAULT ""
set password_wildcard                     0                             ;# RANGE 0-1         DEFAULT 0
set username                              ""                            ;# ANY               DEFAULT ""
set username_wildcard                     0                             ;# RANGE 0-1         DEFAULT 0
set wildcard_pound_end                    0                             ;# RANGE 0-65535     DEFAULT 0
set wildcard_pound_start                  0                             ;# RANGE 0-65535     DEFAULT 0
set wildcard_question_end                 0                             ;# RANGE 0-65535     DEFAULT 0
set wildcard_question_start               0                             ;# RANGE 0-65535     DEFAULT 0


########################################
# INTERMEDIATE AGENT                   #
########################################
set actual_rate_downstream                10                             ;# RANGE   1-65535  DEFAULT 10
set actual_rate_upstream                  10                             ;# RANGE   1-65535  DEFAULT 10
set agent_circuit_id                      ""                             ;# ANY              DEFAULT ""
set agent_remote_id                       ""                             ;# ANY              DEFAULT ""
set data_link                             ethernet                       ;# CHOICES atm_aal5 ethernet    DEFAULT ethernet
set enable_client_signal_iwf              0                              ;# CHOICES 0 1      DEFAULT 0    
set enable_client_signal_loop_char        0                              ;# CHOICES 0 1      DEFAULT 0
set enable_client_signal_loop_encap       0                              ;# CHOICES 0 1      DEFAULT 0
set enable_client_signal_loop_id          0                              ;# CHOICES 0 1      DEFAULT 0
set enable_server_signal_iwf              0                              ;# CHOICES 0 1      DEFAULT 0
set enable_server_signal_loop_char        0                              ;# CHOICES 0 1      DEFAULT 0
set enable_server_signal_loop_encap       0                              ;# CHOICES 0 1      DEFAULT 0
set enable_server_signal_loop_id          0                              ;# CHOICES 0 1      DEFAULT 0
# set intermediate_agent                    0                              ;# CHOICES 0 1      DEFAULT 0
set intermediate_agent_encap1             untagged_eth                   ;# CHOICES na untagged_eth single_tagged_eth        DEFAULT untagged_eth
set intermediate_agent_encap2             na                             ;# CHOICES na pppoa_llc pppoa_null ipoa_llc ipoa_null eth_aal5_llc_fcs eth_aal5_llc_no_fcs eth_aal5_null_fcs eth_aal5_null_no_fcs       DEFAULT na


########################################
# Start PPPoX Call                     #
########################################
set config_status [::ixia::pppox_config                                        \
		-mode                               $mode                              \
		-handle                             $handle                            \
		-num_sessions                       $num_sessions                      \
		-port_handle                        $port_1                            \
		-protocol                           $protocol                          \
		-port_role                          $port_role                         \
		-attempt_rate                       $attempt_rate                      \
		-disconnect_rate                    $disconnect_rate                   \
		-max_outstanding                    $max_outstanding                   \
		-addr_count_per_vci                 $addr_count_per_vci                \
		-addr_count_per_vpi                 $addr_count_per_vpi                \
		-encap                              $encap                             \
		-mac_addr                           $mac_addr                          \
		-mac_addr_step                      $mac_addr_step                     \
		-pvc_incr_mode                      $pvc_incr_mode                     \
		-vci                                $vci                               \
		-vci_count                          $vci_count                         \
		-vci_step                           $vci_step                          \
		-vlan_id                            $vlan_id                           \
		-vlan_id_count                      $vlan_id_count                     \
		-vlan_id_outer                      $vlan_id_outer                     \
		-vlan_id_outer_count                $vlan_id_outer_count               \
		-vlan_id_outer_step                 $vlan_id_outer_step                \
		-vlan_id_step                       $vlan_id_step                      \
		-vlan_user_priority                 $vlan_user_priority                \
		-vpi                                $vpi                               \
		-vpi_count                          $vpi_count                         \
		-vpi_step                           $vpi_step                          \
		-qinq_incr_mode                     $qinq_incr_mode                    \
		-ac_name                            $ac_name                           \
		-ac_select_list                     $ac_select_list                    \
		-ac_select_mode                     $ac_select_mode                    \
		-max_padi_req                       $max_padi_req                      \
		-max_padr_req                       $max_padr_req                      \
		-padi_req_timeout                   $padi_req_timeout                  \
		-padr_req_timeout                   $padr_req_timeout                  \
		-redial                             $redial                            \
		-redial_max                         $redial_max                        \
		-redial_timeout                     $redial_timeout                    \
		-service_name                       $service_name                      \
		-service_type                       $service_type                      \
		-domain_group_map                   $domain_group_map                  \
		-config_req_timeout                 $config_req_timeout                \
		-echo_req                           $echo_req                          \
		-echo_req_interval                  $echo_req_interval                 \
		-echo_rsp                           $echo_rsp                          \
		-max_configure_req                  $max_configure_req                 \
		-max_terminate_req                  $max_terminate_req                 \
		-local_magic                        $local_magic                       \
		-term_req_timeout                   $term_req_timeout                  \
		-ip_cp                              $ip_cp                             \
		-ipcp_req_timeout                   $ipcp_req_timeout                  \
		-ipv6_pool_addr_prefix_len          $ipv6_pool_addr_prefix_len         \
		-ipv6_pool_prefix                   $ipv6_pool_prefix                  \
		-ipv6_pool_prefix_len               $ipv6_pool_prefix_len              \
		-max_ipcp_req                       $max_ipcp_req                      \
		-ppp_local_ip                       $ppp_local_ip                      \
		-ppp_local_ip_step                  $ppp_local_ip_step                 \
		-ppp_local_iid                      $ppp_local_iid                     \
		-ppp_peer_ip                        $ppp_peer_ip                       \
		-ppp_peer_ip_step                   $ppp_peer_ip_step                  \
		-ppp_peer_iid                       $ppp_peer_iid                      \
		-auth_mode                          $auth_mode                         \
		-auth_req_timeout                   $auth_req_timeout                  \
		-max_auth_req                       $max_auth_req                      \
		-password                           $password                          \
		-password_wildcard                  $password_wildcard                 \
		-username                           $username                          \
		-username_wildcard                  $username_wildcard                 \
		-wildcard_pound_end                 $wildcard_pound_end                \
		-wildcard_pound_start               $wildcard_pound_start              \
		-wildcard_question_end              $wildcard_question_end             \
		-wildcard_question_start            $wildcard_question_start           \
		-actual_rate_downstream             $actual_rate_downstream            \
		-actual_rate_upstream               $actual_rate_upstream              \
		-agent_circuit_id                   $agent_circuit_id                  \
		-agent_remote_id                    $agent_remote_id                   \
		-data_link                          $data_link                         \
		-enable_client_signal_iwf           $enable_client_signal_iwf          \
		-enable_client_signal_loop_char     $enable_client_signal_loop_char    \
		-enable_client_signal_loop_encap    $enable_client_signal_loop_encap   \
		-enable_client_signal_loop_id       $enable_client_signal_loop_id      \
		-enable_server_signal_iwf           $enable_server_signal_iwf          \
		-enable_server_signal_loop_char     $enable_server_signal_loop_char    \
		-enable_server_signal_loop_encap    $enable_server_signal_loop_encap   \
		-enable_server_signal_loop_id       $enable_server_signal_loop_id      \
		-intermediate_agent_encap1          $intermediate_agent_encap1         \
		-intermediate_agent_encap2          $intermediate_agent_encap2         \
	]
if {[keylget config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget config_status log]"
    return 0
}

set pppox_handle_1 [keylget config_status handle]
puts "Ixia pppox_handle is $pppox_handle_1 "

foreach item $var_list { catch {unset item}}

########################################
# End PPPoX Call                       #
########################################
set hosts_range_ip_prefix_addr                       3201::
set hosts_range_ip_outer_prefix                      64
set dhcp6_server_range_start_pool_address            2201::
set dhcp6_server_range_subnet_prefix                 64
set dhcp6_server_range_first_dns_server              20:0:2::2
set dhcp6_server_range_second_dns_server             20:0:2::3
set dhcp6_server_range_dns_domain_search_list        ixia.com
set lease_time_max                                   864000
set lease_time                                       86400
set ipv6_pool_prefix								 aa::
set ipv6_pool_prefix_len							 48

set dsppp_status_server [::ixia::dhcp_server_extension_config											\
        -handle											$pppox_handle_1									\
        -dhcp6_server_range_start_pool_address          $dhcp6_server_range_start_pool_address          \
        -dhcp6_server_range_subnet_prefix               $dhcp6_server_range_subnet_prefix               \
        -dhcp6_server_range_first_dns_server            $dhcp6_server_range_first_dns_server            \
        -dhcp6_server_range_second_dns_server           $dhcp6_server_range_second_dns_server           \
        -dhcp6_server_range_dns_domain_search_list      $dhcp6_server_range_dns_domain_search_list      \
        -dhcp6_pgdata_max_outstanding_releases			$dhcp6_pgdata_max_outstanding_releases			\
        -dhcp6_pgdata_max_outstanding_requests			$dhcp6_pgdata_max_outstanding_requests			\
        -dhcp6_pgdata_override_global_setup_rate		$dhcp6_pgdata_override_global_setup_rate		\
        -dhcp6_pgdata_override_global_teardown_rate		$dhcp6_pgdata_override_global_teardown_rate		\
        -dhcp6_pgdata_setup_rate_increment				$dhcp6_pgdata_setup_rate_increment				\
        -dhcp6_pgdata_setup_rate_initial				$dhcp6_pgdata_setup_rate_initial				\
        -dhcp6_pgdata_setup_rate_max					$dhcp6_pgdata_setup_rate_max					\
        -dhcp6_pgdata_teardown_rate_increment			$dhcp6_pgdata_teardown_rate_increment			\
        -dhcp6_pgdata_teardown_rate_initial				$dhcp6_pgdata_teardown_rate_initial				\
        -dhcp6_pgdata_teardown_rate_max					$dhcp6_pgdata_teardown_rate_max					]
		
if {[keylget dsppp_status_server status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dsppp_status_server log]"
    return 0
}
set dsppp_handle_server [keylget dsppp_status_server handle]

################################################################################
# END - PPPoX configuration - Network Port
################################################################################


########################################
# Start PPP                            #
########################################
set control_status [::ixia::pppox_control \
        -handle     $pppox_handle_1       \
        -action     connect               ]
if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    return 0
}

########################################
# Start PPP                            #
########################################
set control_status [::ixia::pppox_control \
        -handle     $pppox_handle_0       \
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
    set aggr_status [::ixia::pppox_stats      \
            -port_handle $port_0              \
            -mode        aggregate            ]
    if {[keylget aggr_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget aggr_status log]"
        return 0
    }
    
    incr retries -1
    
    set sess_num       [keylget aggr_status $port_0.aggregate.num_sessions]
    set sess_count_up  [keylget aggr_status $port_0.aggregate.connected]
    set sess_min_setup [keylget aggr_status $port_0.aggregate.min_setup_time]
    set sess_max_setup [keylget aggr_status $port_0.aggregate.max_setup_time]
    set sess_avg_setup [keylget aggr_status $port_0.aggregate.avg_setup_time]
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
set aggr_status [::ixia::pppox_stats      \
        -port_handle $port_0              \
        -mode        aggregate            ]
if {[keylget aggr_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget aggr_status log]"
    return 0
}
foreach key [keylkeys aggr_status $port_0.aggregate] {
    if {$key != "status"} {
        puts "[format %-40s $key]: [keylget aggr_status $port_0.aggregate.$key]"
    }
}

########################################################
## Statistics
########################################################
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
after 5000
set dhcp_stats_status1 [::ixia::dhcp_extension_stats    \
        -mode           aggregate                       \
        -port_handle    $port_handle                    \
    ]
if {[keylget dhcp_stats_status1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dhcp_stats_status1 log]"
    return 0
}
puts "Aggregate stats: $dhcp_stats_status1"
puts [keylprint dhcp_stats_status1]

if {[keylget dhcp_stats_status1 $port_0.aggregate.dhcpv6_sessions_succeeded] != 5} {
	puts "FAIL - $test_name - only [keylget dhcp_stats_status1 $port_0.aggregate.dhcpv6_sessions_succeeded] from 5 "
	return 0}

after 2000

set dhcp_stats_status2 [::ixia::dhcp_extension_stats                        \
        -mode           session                                             \
        -handle    [list $dsppp_handle_server $dsppp_handle_client]         \
    ]
if {[keylget dhcp_stats_status2 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dhcp_stats_status2 log]"
    return 0
}

puts "Session stats: $dhcp_stats_status2"
puts [keylprint dhcp_stats_status2]

for {set i 0} {$i < 5} {incr i} {
    if {[keylget dhcp_stats_status2 session.client.$port_0/$i.dhcpv6_replies_received] != 1 } {
        puts "not all clients received addresses"
        return 0   
    }
}

after 20000
#########################################
#  Configure and start traffic          #
#########################################

set traffic_status [::ixia::traffic_config         \
        -mode                 reset                \
        -port_handle          $port_handle         ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

#l2tp handles used because ixnet doesn't support extention handles

set track_by                endpoint_pair
set circuit_endpoint_type   ipv6
set traffic_status [::ixia::traffic_config				\
        -mode                  create					\
        -traffic_generator     ixnetwork_540			\
        -bidirectional         0						\
        -emulation_dst_handle  $pppox_handle_1			\
        -emulation_src_handle  $pppox_handle_0			\
        -track_by              $track_by				\
        -circuit_endpoint_type $circuit_endpoint_type	]
		
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}
#########################################
#  Start traffic                        #
#########################################
set control_status [::ixia::traffic_control \
        -port_handle $port_handle           \
        -action      run                    ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}

after 12000

#########################################
#  Stop traffic                         #
#########################################
set control_status [::ixia::traffic_control \
        -port_handle $port_handle			\
        -action      stop                   ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}

#########################################
#  Retrieve aggregate traffic stats     #
#########################################
set aggregated_traffic_status [::ixia::traffic_stats -port_handle $port_handle]
if {[keylget aggregated_traffic_status status] == $::FAILURE} {
    return "FAIL - $test_name - [keylget aggregated_traffic_status log]"
}
puts [keylprint aggregated_traffic_status]

########################################
# Check Frames Tx = Frames Rx          #
########################################
set traffic_percentage 1

if {[keylget aggregated_traffic_status $port_0.aggregate.tx.pkt_count] == 0} {
    puts "FAIL - $test_name - There are no packets sent out from port $port_0."
    return 0
}
if {[expr $traffic_percentage * [keylget aggregated_traffic_status $port_0.aggregate.tx.pkt_count]] > \
        [keylget aggregated_traffic_status $port_1.aggregate.rx.pkt_count]} {
    puts "FAIL - $test_name - Invalid number of packets received on port \
            $port_1 ([keylget aggregated_traffic_status $port_1.aggregate.rx.pkt_count]).\
            The number of packets sent from port $port_0 are\
            [keylget aggregated_traffic_status $port_0.aggregate.tx.pkt_count]."
    return 0
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
