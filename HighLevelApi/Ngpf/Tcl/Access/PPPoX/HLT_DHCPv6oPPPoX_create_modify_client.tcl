################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Gina Dobrescu, Dragos Cotoc
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    03-18-2014 Daria Badea
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
# The script does the following operations:                                    #
#        - creates  topology with DHCP over PPPoX client                       #
#        - modifies DHCPv6 over PPPoX Client global parameters,                #
#          using  "::ixiangpf::emulation_dhcp_group_config"                    #
#          and "::ixiangpf::pppox_config" functions.  						   #
# Module:                                                                      #
#    The sample was tested on a 10GE LSM XM3 module.                           #
#                                                                              #
################################################################################

set PASSED 0
set FAILED 1

set port1 						8/4
set port2 						8/6
set test_name                   [info script]
set chassis_ip                  10.205.15.62
set ixnetwork_tcl_server        localhost
set port_list                   [list $port1 $port2]

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return $FAILED
}

set connect_status [::ixiangpf::connect                         \
    -reset                    1                                  \
    -device                 $chassis_ip                         \
    -port_list              $port_list                          \
    -ixnetwork_tcl_server   $ixnetwork_tcl_server               \
]

ixNet setSessionParameter setAttribute loose
ixNet commit

set port_1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port_2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]
set port_handle [list $port_1 $port_2] 

puts "Connected..."    

# ######################## Topology 1 ############################
set topology_1_status [::ixiangpf::topology_config     \
        -topology_name      {Topology 1}            \
        -port_handle        $port_1                  \
    ]
if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $topology_1_status"
    return $FAILED
}
set topology_1_handle [keylget topology_1_status topology_handle]

# ############################ DG 1 #############################

set device_group_1_status [::ixiangpf::topology_config \
        -topology_handle              $topology_1_handle      \
        -device_group_name            {Device Group 1}        \
        -device_group_multiplier      4                       \
        -device_group_enabled         1                       \
    ]
if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $device_group_1_status"
    return $FAILED
}
set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

set multivalue_1_status [::ixiangpf::multivalue_config             \
        -pattern                counter                         \
        -counter_start          00.15.01.00.00.01               \
        -counter_step           00.00.00.00.00.01               \
        -counter_direction      increment                       \
        -nest_step              00.00.01.00.00.00               \
        -nest_owner             $topology_1_handle              \
        -nest_enabled           0                               \
    ]
if {[keylget multivalue_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $multivalue_1_status"
    return $FAILED
}
set multivalue_1_handle [keylget multivalue_1_status multivalue_handle]    

# ########################### ETHERNET 1 ###########################
 
 set ethernet_1_status [::ixiangpf::interface_config \
        -protocol_name                {Ethernet 1}               \
        -protocol_handle              $deviceGroup_1_handle      \
        -mtu                          1500                       \
        -src_mac_addr                 $multivalue_1_handle       \
        -vlan                         0                          \
        -vlan_id                      1                          \
        -vlan_id_step                 0                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
        -use_vpn_parameters           0                          \
        -site_id                      0                          \
    ]
    
if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $ethernet_1_status"
    return $FAILED
}
set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]

# ########################### PPPoX Client ###########################    
 set pppoxclient_1_status [::ixiangpf::pppox_config \
        -port_role                            access                  \
        -handle                               $ethernet_1_handle      \
        -protocol_name                        {PPPoX Client 1}        \
        -unlimited_redial_attempts            0                       \
        -enable_mru_negotiation               0                       \
        -desired_mru_rate                     1492                    \
        -max_payload                          1700                    \
        -enable_max_payload                   0                       \
        -client_ipv6_ncp_configuration        learned                 \
        -client_ipv4_ncp_configuration        learned                 \
        -lcp_enable_accm                      0                       \
        -lcp_accm                             ffffffff                \
        -ac_select_mode                       ac_name                 \
        -ac_match_name                        ixia                    \
        -auth_req_timeout                     10                      \
        -config_req_timeout                   10                      \
        -echo_req                             0                       \
        -echo_rsp                             1                       \
        -ip_cp                                ipv6_cp                 \
        -ipcp_req_timeout                     10                      \
        -max_auth_req                         20                      \
        -max_padi_req                         5                       \
        -max_padr_req                         5                       \
        -max_terminate_req                    3                       \
        -padi_req_timeout                     10                      \
        -padr_req_timeout                     10                      \
        -password                             ixia                    \
        -chap_secret                          secret                  \
        -username                             ixia                    \
        -chap_name                            user                    \
        -mode                                 add                     \
        -auth_mode                            pap                     \
        -echo_req_interval                    10                      \
        -max_configure_req                    3                       \
        -max_ipcp_req                         3                       \
        -actual_rate_downstream               10                      \
        -actual_rate_upstream                 10                      \
        -data_link                            ethernet                \
        -enable_domain_group_map              0                       \
        -enable_client_signal_iwf             0                       \
        -enable_client_signal_loop_char       0                       \
        -enable_client_signal_loop_encap      0                       \
        -enable_client_signal_loop_id         0                       \
        -intermediate_agent_encap1            untagged_eth            \
        -intermediate_agent_encap2            na                      \
        -ppp_local_iid                        0:11:11:11:0:0:0:1      \
        -ppp_local_ip                         1.1.1.1                 \
        -redial                               0                       \
        -redial_max                           20                      \
        -redial_timeout                       10                      \
        -service_type                         any                     \
        -client_dns_options                   disable_extension       \
        -client_dns_primary_address           8.8.8.8                 \
        -client_dns_secondary_address         9.9.9.9                 \
        -client_netmask_options               disable_extension       \
        -client_netmask                       255.0.0.0               \
        -client_wins_options                  disable_extension       \
        -client_wins_primary_address          8.8.8.8                 \
        -client_wins_secondary_address        9.9.9.9                 \
    ]
if {[keylget pppoxclient_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $pppoxclient_1_status"
    return $FAILED
}
set pppoxclient_1_handle [keylget pppoxclient_1_status pppox_client_handle]

# #################### Setting DHCPv6 multivalues ###################
set multivalue_2_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          10                      \
    -counter_step           1                       \
    -counter_direction      increment               \
    -nest_step              0                       \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_2_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $multivalue_2_status"
    return $FAILED
}
set multivalue_2_handle [keylget multivalue_2_status multivalue_handle]

set multivalue_3_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          10                      \
    -counter_step           0                       \
    -counter_direction      increment               \
    -nest_step              1                       \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_3_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $multivalue_3_status"
    return $FAILED
}
set multivalue_3_handle [keylget multivalue_3_status multivalue_handle]
    
# ########################### DHCPv6 Client ###########################    

set dhcpv6client_1_status [::ixiangpf::emulation_dhcp_group_config \
        -dhcp6_range_duid_enterprise_id      $multivalue_2_handle       \
        -dhcp6_range_duid_type               duid_llt                   \
        -dhcp6_range_duid_vendor_id          $multivalue_3_handle       \
        -dhcp6_range_ia_id                   10                         \
        -dhcp6_range_ia_t1                   302400                     \
        -dhcp6_range_ia_t2                   483840                     \
        -dhcp6_range_ia_type                 iata                       \
        -dhcp_range_ip_type                  ipv6                       \
        -dhcp_range_renew_timer              0                          \
        -handle                              $pppoxclient_1_handle      \
        -use_rapid_commit                    0                          \
        -protocol_name                       {DHCPv6 Client 1}          \
        -enable_stateless                    1                          \
        -dhcp6_use_pd_global_address         0                          \
    ]
if {[keylget dhcpv6client_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $dhcpv6client_1_status"
    return $FAILED
}
set dhcpv6client_1_handle [keylget dhcpv6client_1_status dhcpv6client_handle]
    

# ########### Modifying DHCPv6 over PPPoX Client ##################### 

puts ""
puts "Modifying DHCPv6 over PPPoX Client global parameters..."
sleep 10



# ##################### Modifying DHCPv6 global parameters #################
set dhcpv6client_1_status [::ixiangpf::emulation_dhcp_config          \
        -mode                                  modify                     \
        -handle                              $dhcpv6client_1_handle  \
        -dhcp6_echo_ia_info                     1                         \
        -renew_on_link_up                     1                         \
        -skip_release_on_stop                 1                         \
        -msg_timeout                         6                         \
        -dhcp6_sol_max_rc                     6                         \
        -dhcp6_sol_max_rt                     89                         \
        -dhcp6_req_timeout                     2                         \
        -dhcp6_rel_timeout                     7                         \
        -dhcp6_reb_timeout                     11                         \
        -dhcp6_ren_max_rt                     670                     \
        -dhcp6_ren_timeout                     9                         \
        -dhcp6_req_max_rc                     6                         \
        -dhcp6_req_max_rt                     29                         \
        -dhcp6_reb_max_rt                     660                     \
        -dhcp6_sol_timeout                     7                         \
        -dhcp6_rel_max_rc                     6                         \
        -dhcp6_info_req_timeout                 8                         \
        -dhcp6_info_req_max_rt                 125                       \
        -dhcp6_info_req_max_rc                 6                         \
        -request_rate                         25                         \
        -interval_start                         1005                     \
        -outstanding_releases_count             406                     \
        -outstanding_session_count             407                     \
        -interval_stop                         206                     \
        -release_rate                         160                     \
        -enable_lifetime                     1                         \
        -min_lifetime                         2                         \
        -max_lifetime                         12                         \
        -enable_restart                         1                         \
        -max_restarts                         14                         \
        -unlimited_restarts                     1                         \
]        

if {[keylget dhcpv6client_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $dhcpv6client_1_status"
    return $FAILED
}

set pppoxclient_1_status [::ixiangpf::pppox_config                 \
    -port_role                                access                   \
    -handle                                 $pppoxclient_1_handle  \
    -mode                                    modify                   \
    -echo_req                                1                       \
    -ra_timeout                                7                       \
    -echo_req_interval                        850                       \
    -enable_session_lifetime                   1                       \
    -enable_session_lifetime_restart        1                       \
    -max_session_lifetime_restarts          6                       \
    -min_lifetime                             5                       \
    -max_lifetime                            8                       \
    -unlimited_session_lifetime_restarts     1                       \
    -attempt_enabled                        1                       \
    -attempt_rate                            250                       \
    -attempt_max_outstanding                450                       \
    -disconnect_max_outstanding             456                       \
    -attempt_interval                         850                       \
    -actual_rate_downstream                    402                       \
    -disconnect_interval                    708                       \
    -disconnect_rate                        240                       \
]

if {[keylget pppoxclient_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $pppoxclient_1_status"
    return $FAILED
}

puts ""
puts "!!! TEST PASSED !!!"
return $PASSED    



