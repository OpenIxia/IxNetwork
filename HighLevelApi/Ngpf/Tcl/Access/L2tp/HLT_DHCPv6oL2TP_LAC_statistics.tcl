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
# This script configures a scenario with 2 topologies:		                   #
#        - Topology 1 with DHCPv6 Client behind L2TP Access Concentrator       #
#        - Topology 2 With DHCPv6 Server over L2TP Network Server			   #
# The script does the following operations for LAC:                            #
#    	 - creates topologies and retrive specific DHCP over PPP  			   #
#  		   statistics and protocol info.   									   #
#																			   #
# Module:                                                                      #
#    The sample was tested on a 10GE LSM XM3 module.                           #
#                                                                              #
################################################################################

set PASSED 0
set FAILED 1

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return $FAILED
}

set port1 						1/7
set port2 						1/8
set test_name                   [info script]
set chassis_ip                  10.205.15.75
set ixnetwork_tcl_server        localhost
set port_list                   [list $port1 $port2]


set connect_status [::ixiangpf::connect                         \
    -reset         1                                             \
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
puts ""
puts "Creating topology..."

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
sleep 5
puts ""
puts "Creating DG 1..."

set device_group_1_status [::ixiangpf::topology_config \
        -topology_handle              $topology_1_handle      \
        -device_group_name            {Device Group 1}        \
        -device_group_multiplier      10                       \
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

sleep 5
puts ""
puts "Creating Ethernet 1 layer..."

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


    
# ################## L2TP Access Concentrator ###############    

puts "Adding L2TP Access Concentrator..."

set tunnel_count        1
set sessions_per_tunnel 10

set mv_custom_distribution [::ixiangpf::multivalue_config \
        -mode                   create           \
        -pattern                string           \
        -string_pattern         User{Inc:1}_Pwd{Inc:100}               \
    ]
if {[keylget mv_custom_distribution status] != $::SUCCESS} {
    puts "FAIL - [info script] - $mv_custom_distribution"
    return $FAILED
}
set mv_cd_handle [keylget mv_custom_distribution multivalue_handle]

set l2tp_LAC_status [::ixiangpf::l2tp_config                                \
		-mode                               lac                             \
		-handle                             $ethernet_1_handle              \
		-action                             create                          \
		-sessions_per_tunnel                $sessions_per_tunnel            \
		-num_tunnels                        $tunnel_count                   \
		-l2tp_dst_addr                      12.70.1.1                       \
		-l2tp_dst_step                      0.0.0.1                         \
		-l2tp_src_gw                		0.0.0.0                			\
		-l2tp_src_prefix_len            	16                    			\
		-l2tp_src_addr                      12.70.0.1                       \
		-l2tp_src_count                     $tunnel_count                   \
		-l2tp_src_step                      0.0.0.1                         \
		-domain_group_map                   $mv_cd_handle                   \
		-enable_term_req_timeout            0                               \
        -sequence_bit                                                       \
        -offset_bit                                                         \
        -length_bit                                                         \
        -tun_auth                                                           \
        -redial                                                             \
        -data_chksum                                                        \
        -ctrl_chksum                                                        \
        -hello_req                                                          \
        -avp_hide                                                           \
        -offset_byte                        89                              \
        -udp_src_port                       1600                            \
        -udp_dst_port                       1800                            \
        -redial_timeout                     13                              \
        -rws                                15                              \
        -offset_len                         16                              \
        -max_ctrl_timeout                   9                               \
        -redial_max                         2048                            \
		-hostname                           "ixia_dut"                      \
        -secret                             "ixia_secret"                   \
        -hostname_wc                        1                               \
        -secret_wc                          1                               \
        -wildcard_bang_start                1                               \
        -wildcard_bang_end                  $sessions_per_tunnel            \
        -wildcard_dollar_start              1                               \
        -wildcard_dollar_end                $tunnel_count                   \
        -username                           "ixia_#_?"                      \
        -password                           "pwd_#_?"                       \
        -username_wc                        1                               \
        -password_wc                        1                               \
        -wildcard_pound_start               1                               \
        -wildcard_pound_end                 $tunnel_count                   \
        -wildcard_question_start            1                               \
        -wildcard_question_end              $sessions_per_tunnel            \
        -init_ctrl_timeout                  6                               \
        -hello_interval                     101                             \
        -framing_capability                 async                           \
        -ctrl_retries                       11                              \
        -bearer_type                        digital                         \
        -bearer_capability                  digital                         \
        -enable_mru_negotiation             1                               \
        -desired_mru_rate                   1501                            \
        -lcp_enable_accm                    1                               \
        -lcp_accm                           1501                            \
        -max_auth_req                       15                              \
        -auth_req_timeout                   7                               \
        -auth_mode                          pap_or_chap                     \
        -chap_name                          ixia_chap_name                  \
        -chap_secret                        ixia_chap_secret                \
        -client_dns_options                 request_primary_and_secondary   \
		-ppp_client_ip                      3.3.3.3                         \
        -ppp_client_step                    0.0.0.2                         \
        -ppp_client_iid                     00:44:44:44:00:00:00:01         \
        -client_ipv4_ncp_configuration      request                         \
        -client_netmask                     255.255.0.0                     \
        -client_netmask_options             request_specific_netmask        \
        -client_ipv6_ncp_configuration      request                         \
        -client_wins_options                request_primaryandsecondary_wins\
        -client_wins_primary_address        88.88.88.88                     \
        -client_wins_secondary_address      99.99.99.99                     \
        -enable_domain_groups               1                               \
        -echo_req                           1                               \
        -echo_req_interval                  9                               \
        -echo_rsp                           1                               \
        -max_configure_req                  8                               \
        -max_terminate_req                  6                               \
        -config_req_timeout                 25                              \
        -protocol_name                      "Ixia LAC"                      \
        -max_ipcp_req                       12                              \
        -ipcp_req_timeout                   13                              \
        -ip_cp                              dual_stack                      \
        -client_primary_dns_address         5.5.5.5                         \
        -client_secondary_dns_address       6.6.6.6                         \
    ]

if {[keylget l2tp_LAC_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $l2tp_LAC_status"
    return $FAILED
}

set l2tp_LAC_handle [keylget l2tp_LAC_status lac_handle]

set pppoxclient_handle [keylget l2tp_LAC_status pppox_client_handle]


    
# ########################### DHCPv6 Client ###########################    

puts ""
puts "Adding DHCPv6 Client 1 layer..."

set dhcp_config_for_lac [::ixiangpf::emulation_dhcp_group_config    \
		-handle                      	$pppoxclient_handle         \
		-mode                    		create        \
		-dhcp_range_ip_type             ipv6        \
		-dhcp6_range_duid_enterprise_id 15        \
		-dhcp6_range_duid_type          duid_en        \
		-dhcp6_range_duid_vendor_id     20        \
		-dhcp6_range_duid_vendor_id_increment    2        \
		-dhcp_range_renew_timer         10        \
		-dhcp6_use_pd_global_address    1        \
		-protocol_name                	"Ixia DHCPv6"    \
		-dhcp6_range_ia_type        	iana_iapd        \
		-dhcp6_range_ia_t2            	40000        \
		-dhcp6_range_ia_t1            	30000        \
		-dhcp6_range_ia_id_increment    2        \
		-dhcp6_range_ia_id            	20        \
]

if {[keylget dhcp_config_for_lac status] != $::SUCCESS} {
    puts "FAIL - [info script] - $dhcp_config_for_lac"
    return $FAILED
}
set dhcpclient_1_handle [keylget dhcp_config_for_lac dhcpv6client_handle]



set topology_2_status [::ixiangpf::topology_config     \
        -topology_name      {Topology 2}            \
        -port_handle        $port_2          \
]
if {[keylget topology_2_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $topology_2_status"
    return $FAILED
}
set topology_2_handle [keylget topology_2_status topology_handle]


puts ""
puts "Creating DG 3..."

set device_group_3_status [::ixiangpf::topology_config \
        -topology_handle              $topology_2_handle      \
        -device_group_name            {Device Group 3}        \
        -device_group_multiplier      10                       \
        -device_group_enabled         1                       \
    ]
if {[keylget device_group_3_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $device_group_3_status"
    return $FAILED
}
set deviceGroup_3_handle [keylget device_group_3_status device_group_handle]


set tunnel_count        5
set sessions_per_tunnel 50

set l2tp_LNS_status [::ixiangpf::l2tp_config                                \
        -mode                               lns                             \
        -handle                             $deviceGroup_3_handle           \
		-protocol_name                {L2TP Network Server}        \
        -action                             create                          \
        -num_tunnels                        $tunnel_count                   \
        -sessions_per_tunnel                $sessions_per_tunnel            \
        -l2tp_src_addr                      12.70.1.1                       \
        -l2tp_src_count                     $tunnel_count                   \
		-l2tp_src_gw                  0.0.0.0                \
        -l2tp_src_step                      0.0.0.1                         \
		-l2tp_src_prefix_len            16                    \
        -enable_term_req_timeout            0                               \
        -username                           ixia_lns_user                   \
        -password                           ixia_lns_pass                   \
        -chap_name                          ixia_chap_name                  \
        -chap_secret                        ixia_chap_secret                \
        -enable_domain_groups               1                               \
        -domain_group_map                   $mv_cd_handle                   \
        -sequence_bit                                                       \
        -offset_bit                                                         \
        -length_bit                                                         \
        -tun_auth                                                           \
        -redial                                                             \
        -data_chksum                                                        \
        -ctrl_chksum                                                        \
        -hello_req                                                          \
        -avp_hide                                                           \
        -offset_byte                        89                              \
        -udp_src_port                       1800                            \
        -udp_dst_port                       1600                            \
        -redial_timeout                     13                              \
        -rws                                15                              \
        -offset_len                         16                              \
        -max_ctrl_timeout                   9                               \
        -redial_max                         2048                            \
        -secret                             ixia_secret                     \
        -hostname                           ixia_dut                        \
        -init_ctrl_timeout                  6                               \
        -hello_interval                     101                             \
        -framing_capability                 async                           \
        -ctrl_retries                       11                              \
        -bearer_type                        digital                         \
        -bearer_capability                  digital                         \
        -accept_any_auth_value              1                               \
        -max_auth_req                       121                             \
        -auth_req_timeout                   132                             \
        -auth_mode                          pap_or_chap                     \
        -ppp_client_iid                     00:55:55:55:00:00:00:01         \
        -ppp_client_iid_step                00:00:00:00:00:00:00:01         \
        -ppp_client_ip                      22.22.22.1                      \
        -ppp_client_step                    0.0.0.3                         \
        -dns_server_list                    100:0:0:1:0:0:0:0               \
        -echo_req_interval                  17                              \
        -send_dns_options                   1                               \
        -echo_req                           1                               \
        -echo_rsp                           1                               \
        -ipv6_pool_addr_prefix_len          90                              \
        -ipv6_pool_prefix                   1:1:1:1:1:1:1:1                 \
        -ipv6_pool_prefix_len               72                              \
        -lcp_accm                           234                             \
        -lcp_enable_accm                    1                               \
        -max_configure_req                  111                             \
        -max_terminate_req                  120                             \
        -config_req_timeout                 55                              \
        -enable_mru_negotiation             1                               \
        -desired_mru_rate                   1501                            \
        -max_ipcp_req                       14                              \
        -ipcp_req_timeout                   15                              \
        -ip_cp                              dual_stack                      \
        -ppp_server_iid                     00:66:66:66:00:00:00:01         \
        -ppp_server_ip                      45.45.45.1                      \
        -server_dns_options                 supply_primary_and_secondary    \
        -ppp_local_iid_step                 3                               \
        -ppp_local_ip_step                  0.0.15.15                       \
        -server_ipv4_ncp_configuration      clientmay                       \
        -server_netmask                     255.255.255.128                 \
        -server_netmask_options             supply_netmask                  \
        -server_primary_dns_address         12.12.12.1                      \
        -server_secondary_dns_address       13.13.13.1                      \
        -server_ipv6_ncp_configuration      clientmay                       \
        -server_wins_options                supply_primary_and_secondary    \
        -server_wins_primary_address        21.21.21.1                      \
        -server_wins_secondary_address      31.31.31.1                      \
    ]

set pppoxserver_handle [keylget l2tp_LNS_status pppox_server_handle]



set dhcp_server_config_for_lns [::ixiangpf::emulation_dhcp_server_config    \
		-handle                             $pppoxserver_handle            \
		-mode                    create                \
        -dhcp6_ia_type                      iana_iapd                \
        -ip_dns1                            11:0:0:0:0:0:0:1            \
        -ip_dns2                            22:0:0:0:0:0:0:1            \
        -ip_version                         6                    \
        -ipaddress_count                    1                    \
        -ipaddress_pool                     5:a::1                \
        -ipaddress_pool_prefix_length       64                    \
        -lease_time                         86400                \
        -protocol_name                      {Ixia DHCPv6 Server}        \
        -use_rapid_commit                   0                    \
        -pool_address_increment             0:0:0:0:0:0:0:1            \
        -start_pool_prefix                  55:aa::                \
        -pool_prefix_increment              1:0:0:0:0:0:0:0            \
        -pool_prefix_size                   1                    \
        -prefix_length                      64                    \
        -custom_renew_time                  34560                              \
        -custom_rebind_time                 55296                              \
        -use_custom_times                   1                                  \
]

if {[keylget dhcp_server_config_for_lns status] != $::SUCCESS} {
    puts "FAIL - [info script] - $dhcp_server_config_for_lns"
    return $FAILED
}

set dhcp_server_handle [keylget dhcp_server_config_for_lns dhcpv6server_handle]


puts ""
puts "Starting protocols ..."
puts ""    



set test_control [::ixiangpf::test_control    \
    -action start_all_protocols        \
    ]

sleep 10



# ###################### DHCPv6 over PPPoX Client Statistics #####################
puts ""
puts "Retriving statistics..."
puts ""

puts "DHCP Statistics..."
puts ""

set dhcp_stats_0 [::ixiangpf::emulation_dhcp_stats      \
        -port_handle   $port_1                            \
		-mode          aggregate_stats                \
		-dhcp_version    dhcp6                    \
        -execution_timeout 300                           \
    ]

if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "FAIL - [info script] - $dhcp_stats_0"
    return $FAILED
}
    
set dhcp_stats_0 [::ixiangpf::emulation_dhcp_stats      \
		-handle   $dhcpclient_1_handle                    \
		-mode          aggregate_stats                \
		-dhcp_version    dhcp6                    \
		-execution_timeout 300                               \
]

 if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "FAIL - [info script] - $dhcp_stats_0"
    return $FAILED
}

set dhcp_stats_0 [::ixiangpf::emulation_dhcp_stats  \
        -handle   $dhcpclient_1_handle                \
        -mode          session            \
        -dhcp_version    dhcp6            \
        -execution_timeout 300                       \
    ]

if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "FAIL - [info script] - $dhcp_stats_0"
    return $FAILED
}


puts ""
puts "LAC Statistics..."

set l2tp_stats2 [::ixiangpf::l2tp_stats          \
        -port_handle   $port_1            \
		-mode     aggregate            \
        -execution_timeout 300                   \
    ]


if {[keylget l2tp_stats2 status] != $::SUCCESS} {
    puts "FAIL - [info script] - $l2tp_stats2"
    return $FAILED
}


set l2tp_stats1 [::ixiangpf::l2tp_stats          \
		-mode              tunnel        \
		-handle          $l2tp_LAC_handle    \
        -execution_timeout   300                   \
    ]

if {[keylget l2tp_stats1 status] != $::SUCCESS} {
    puts "FAIL - [info script] - $l2tp_stats1"
    return $FAILED
}



puts ""
puts "Verifying session info for DHCPv6 over PPPoX Client..."
puts ""
set ppp_client_session_info1 [::ixiangpf::protocol_info     \
    -handle              $pppoxclient_handle        \
    -mode                handles            \
]    

sleep 5

set ppp_client_session_info2 [::ixiangpf::protocol_info     \
    -handle              $pppoxclient_handle        \
    -mode                aggregate        \
]

sleep 5

set dhcp_client_session_info1 [::ixiangpf::protocol_info     \
    -handle              $dhcpclient_1_handle        \
    -mode                handles            \
]            

sleep 5

set dhcp_client_session_info2 [::ixiangpf::protocol_info     \
    -handle              $dhcpclient_1_handle        \
    -mode                aggregate        \
]            



puts ""
puts "Stopping protocols ..."
puts ""    


set test_control [::ixiangpf::test_control    \
    -action stop_all_protocols        \
    ]

sleep 10    

puts ""
puts "Clear topologies..."
sleep 5


set topology_1_status [::ixiangpf::topology_config     \
		-mode               destroy                     \
        -port_handle        $port_1              \
		-topology_handle    $topology_1_handle            \
]
if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $topology_1_status"
    return $FAILED
}


set topology_2_status [::ixiangpf::topology_config     \
		-mode               destroy                     \
        -port_handle        $port_2              \
		-topology_handle    $topology_2_handle            \
  ]
if {[keylget topology_2_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $topology_2_status"
    return $FAILED
}
  
puts ""
puts "!!! TEST PASSED !!!"
return $PASSED    

