################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Stefan Popi $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10-29-2013 Stefan Popi
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
#    This sample configures a scenario with 2 L2TP Access                      #
#    Concentrators and 2 L2TP Network Servers.                                 #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10GE LSM XM3 module.                           #
#                                                                              #
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

set test_name [info script]

set chassis_ip           ixro-hlt-xm2-01
set tcl_server           ixro-hlt-xm2-01
set ixnetwork_tcl_server localhost
set port_list            [list 1/5 1/6]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect                     \
        -reset                                          \
        -device                 $chassis_ip             \
        -port_list              $port_list              \
        -ixnetwork_tcl_server   $ixnetwork_tcl_server   \
        -tcl_server             $tcl_server             \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port_2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]
set port_handle [list $port_1 $port_2] 



set topology_1_status [::ixiangpf::topology_config          \
    -topology_name      {Topology 1}                        \
    -port_handle        $port_1                             \
]
if {[keylget topology_1_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget topology_1_status log]"
}
set topology_1_handle [keylget topology_1_status topology_handle]

set device_group_1_status [::ixiangpf::topology_config \
    -topology_handle              $topology_1_handle      \
    -device_group_name            {Device Group 1}        \
    -device_group_multiplier      3                       \
    -device_group_enabled         1                       \
]
if {[keylget device_group_1_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget device_group_1_status log]"
}
set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

set multivalue_1_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.11.01.00.00.01       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_1_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_1_status log]"
}
set multivalue_1_handle [keylget multivalue_1_status multivalue_handle]

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
    return "FAIL - $test_name - [keylget ethernet_1_status log]"
}
set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]

set multivalue_2_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          100.1.0.1               \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_2_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_2_status log]"
}
set multivalue_2_handle [keylget multivalue_2_status multivalue_handle]

set ipv4_1_status [::ixiangpf::interface_config \
    -protocol_name                     {IPv4 1}                  \
    -protocol_handle                   $ethernet_1_handle        \
    -ipv4_resolve_gateway              1                         \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01         \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00         \
    -gateway                           0.0.0.0                   \
    -gateway_step                      0.0.0.0                   \
    -intf_ip_addr                      $multivalue_2_handle      \
    -netmask                           255.255.255.0             \
]
if {[keylget ipv4_1_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ipv4_1_status log]"
}
set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]

set multivalue_3_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          100.1.0.100             \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_3_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_3_status log]"
}
set multivalue_3_handle [keylget multivalue_3_status multivalue_handle]

set lac_1_status [::ixiangpf::l2tp_config \
    -l2tp_dst_addr           $multivalue_3_handle                \
    -mode                    lac                                 \
    -handle                  $ipv4_1_handle                      \
    -num_tunnels             1                                   \
    -protocol_name           {L2TP Access Concentrator 1}        \
    -action                  create                              \
    -avp_hide                0                                   \
    -ctrl_chksum             1                                   \
    -ctrl_retries            30                                  \
    -data_chksum             0                                   \
    -hello_interval          60                                  \
    -hello_req               0                                   \
    -hostname                ixia                                \
    -init_ctrl_timeout       2                                   \
    -length_bit              0                                   \
    -max_ctrl_timeout        8                                   \
    -offset_bit              0                                   \
    -offset_byte             0                                   \
    -offset_len              0                                   \
    -redial                  0                                   \
    -redial_max              20                                  \
    -redial_timeout          10                                  \
    -rws                     10                                  \
    -secret                  ixia                                \
    -sequence_bit            0                                   \
    -tun_auth                tunnel_authentication_disabled      \
    -udp_dst_port            1701                                \
    -udp_src_port            1701                                \
    -bearer_capability       both                                \
    -bearer_type             analog                              \
    -framing_capability      sync                                \
]
if {[keylget lac_1_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget lac_1_status log]"
}
set lac_1_handle [keylget lac_1_status lac_handle]

set device_group_2_status [::ixiangpf::topology_config \
    -device_group_name            {Device Group 2}           \
    -device_group_multiplier      2                          \
    -device_group_enabled         1                          \
    -device_group_handle          $deviceGroup_1_handle      \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget device_group_2_status log]"
}
set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]

set multivalue_4_status [::ixiangpf::multivalue_config \
    -pattern                counter                                       \
    -counter_start          00.12.01.00.00.01                             \
    -counter_step           00.00.00.00.00.01                             \
    -counter_direction      increment                                     \
    -nest_step              00.00.00.00.00.01,00.00.01.00.00.00           \
    -nest_owner             $deviceGroup_1_handle,$topology_1_handle      \
    -nest_enabled           0,1                                           \
]
if {[keylget multivalue_4_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_4_status log]"
}
set multivalue_4_handle [keylget multivalue_4_status multivalue_handle]

set ethernet_2_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 2}               \
    -protocol_handle              $deviceGroup_2_handle      \
    -connected_to_handle          $ethernet_1_handle         \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_4_handle       \
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
if {[keylget ethernet_2_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ethernet_2_status log]"
}
set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]

set pppoxclient_1_status [::ixiangpf::pppox_config \
    -port_role                            access                  \
    -handle                               $ethernet_2_handle      \
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
    -ac_select_mode                       first_responding        \
    -auth_req_timeout                     10                      \
    -config_req_timeout                   10                      \
    -echo_req                             0                       \
    -echo_rsp                             1                       \
    -ip_cp                                ipv4_cp                 \
    -ipcp_req_timeout                     10                      \
    -max_auth_req                         20                      \
    -max_padi_req                         5                       \
    -max_padr_req                         5                       \
    -max_terminate_req                    3                       \
    -padi_req_timeout                     10                      \
    -padr_req_timeout                     10                      \
    -password                             password                \
    -chap_secret                          secret                  \
    -username                             user                    \
    -chap_name                            user                    \
    -mode                                 add                     \
    -auth_mode                            none                    \
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
    -redial                               1                       \
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
    -lcp_max_failure                      5                       \
]
if {[keylget pppoxclient_1_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pppoxclient_1_status log]"
}
set pppoxclient_1_handle [keylget pppoxclient_1_status pppox_client_handle]

set device_group_3_status [::ixiangpf::topology_config \
    -topology_handle              $topology_1_handle      \
    -device_group_name            {Device Group 4}        \
    -device_group_multiplier      10                      \
    -device_group_enabled         1                       \
]
if {[keylget device_group_3_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget device_group_3_status log]"
}
set deviceGroup_3_handle [keylget device_group_3_status device_group_handle]

set multivalue_5_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.14.01.00.00.01       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_5_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_5_status log]"
}
set multivalue_5_handle [keylget multivalue_5_status multivalue_handle]

set ethernet_3_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 4}               \
    -protocol_handle              $deviceGroup_3_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_5_handle       \
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
if {[keylget ethernet_3_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ethernet_3_status log]"
}
set ethernet_3_handle [keylget ethernet_3_status ethernet_handle]

set multivalue_6_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          102.1.0.1               \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_1_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_6_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_6_status log]"
}
set multivalue_6_handle [keylget multivalue_6_status multivalue_handle]

set ipv4_2_status [::ixiangpf::interface_config \
    -protocol_name                     {IPv4 3}                  \
    -protocol_handle                   $ethernet_3_handle        \
    -ipv4_resolve_gateway              1                         \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01         \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00         \
    -gateway                           0.0.0.0                   \
    -gateway_step                      0.0.0.0                   \
    -intf_ip_addr                      $multivalue_6_handle      \
    -netmask                           255.255.255.0             \
]
if {[keylget ipv4_2_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ipv4_2_status log]"
}
set ipv4_2_handle [keylget ipv4_2_status ipv4_handle]

set multivalue_7_status [::ixiangpf::multivalue_config \
    -pattern           custom                  \
    -nest_step         0.1.0.0                 \
    -nest_owner        $topology_1_handle      \
    -nest_enabled      1                       \
]
if {[keylget multivalue_7_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_7_status log]"
}
set multivalue_7_handle [keylget multivalue_7_status multivalue_handle]

set custom_1_status [::ixiangpf::multivalue_config \
    -multivalue_handle      $multivalue_7_handle      \
    -custom_start           102.1.0.100               \
    -custom_step            0.0.0.0                   \
]
if {[keylget custom_1_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget custom_1_status log]"
}
set custom_1_handle [keylget custom_1_status custom_handle]

set increment_1_status [::ixiangpf::multivalue_config \
    -custom_handle               $custom_1_handle      \
    -custom_increment_value      0.0.0.1               \
    -custom_increment_count      50                    \
]
if {[keylget increment_1_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget increment_1_status log]"
}
set increment_1_handle [keylget increment_1_status increment_handle]

set lac_2_status [::ixiangpf::l2tp_config \
    -l2tp_dst_addr           $multivalue_7_handle                \
    -mode                    lac                                 \
    -handle                  $ipv4_2_handle                      \
    -num_tunnels             5                                   \
    -protocol_name           {L2TP Access Concentrator 2}        \
    -action                  create                              \
    -avp_hide                0                                   \
    -ctrl_chksum             1                                   \
    -ctrl_retries            30                                  \
    -data_chksum             0                                   \
    -hello_interval          60                                  \
    -hello_req               0                                   \
    -hostname                ixia                                \
    -init_ctrl_timeout       2                                   \
    -length_bit              0                                   \
    -max_ctrl_timeout        8                                   \
    -offset_bit              0                                   \
    -offset_byte             0                                   \
    -offset_len              0                                   \
    -redial                  0                                   \
    -redial_max              20                                  \
    -redial_timeout          10                                  \
    -rws                     10                                  \
    -secret                  ixia                                \
    -sequence_bit            0                                   \
    -tun_auth                tunnel_authentication_disabled      \
    -udp_dst_port            1701                                \
    -udp_src_port            1701                                \
    -bearer_capability       both                                \
    -bearer_type             analog                              \
    -framing_capability      sync                                \
]
if {[keylget lac_2_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget lac_2_status log]"
}
set lac_2_handle [keylget lac_2_status lac_handle]

set device_group_4_status [::ixiangpf::topology_config \
    -device_group_name            {Device Group 5}           \
    -device_group_multiplier      1                          \
    -device_group_enabled         1                          \
    -device_group_handle          $deviceGroup_3_handle      \
]
if {[keylget device_group_4_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget device_group_4_status log]"
}
set deviceGroup_4_handle [keylget device_group_4_status device_group_handle]

set multivalue_8_status [::ixiangpf::multivalue_config \
    -pattern                counter                                       \
    -counter_start          00.15.01.00.00.01                             \
    -counter_step           00.00.00.00.00.01                             \
    -counter_direction      increment                                     \
    -nest_step              00.00.00.00.00.01,00.00.01.00.00.00           \
    -nest_owner             $deviceGroup_3_handle,$topology_1_handle      \
    -nest_enabled           0,1                                           \
]
if {[keylget multivalue_8_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_8_status log]"
}
set multivalue_8_handle [keylget multivalue_8_status multivalue_handle]

set ethernet_4_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 5}               \
    -protocol_handle              $deviceGroup_4_handle      \
    -connected_to_handle          $ethernet_3_handle         \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_8_handle       \
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
if {[keylget ethernet_4_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ethernet_4_status log]"
}
set ethernet_4_handle [keylget ethernet_4_status ethernet_handle]

set pppoxclient_2_status [::ixiangpf::pppox_config \
    -port_role                            access                  \
    -handle                               $ethernet_4_handle      \
    -protocol_name                        {PPPoX Client 2}        \
    -unlimited_redial_attempts            0                       \
    -enable_mru_negotiation               0                       \
    -desired_mru_rate                     1492                    \
    -max_payload                          1700                    \
    -enable_max_payload                   0                       \
    -client_ipv6_ncp_configuration        learned                 \
    -client_ipv4_ncp_configuration        learned                 \
    -lcp_enable_accm                      0                       \
    -lcp_accm                             ffffffff                \
    -ac_select_mode                       first_responding        \
    -auth_req_timeout                     10                      \
    -config_req_timeout                   10                      \
    -echo_req                             0                       \
    -echo_rsp                             1                       \
    -ip_cp                                ipv4_cp                 \
    -ipcp_req_timeout                     10                      \
    -max_auth_req                         20                      \
    -max_padi_req                         5                       \
    -max_padr_req                         5                       \
    -max_terminate_req                    3                       \
    -padi_req_timeout                     10                      \
    -padr_req_timeout                     10                      \
    -password                             password                \
    -chap_secret                          secret                  \
    -username                             user                    \
    -chap_name                            user                    \
    -mode                                 add                     \
    -auth_mode                            none                    \
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
    -redial                               1                       \
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
    -lcp_max_failure                      5                       \
]
if {[keylget pppoxclient_2_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pppoxclient_2_status log]"
}
set pppoxclient_2_handle [keylget pppoxclient_2_status pppox_client_handle]

set topology_2_status [::ixiangpf::topology_config          \
    -topology_name      {Topology 2}                        \
    -port_handle        $port_2                             \
]
if {[keylget topology_2_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget topology_2_status log]"
}
set topology_2_handle [keylget topology_2_status topology_handle]

set device_group_5_status [::ixiangpf::topology_config \
    -topology_handle              $topology_2_handle      \
    -device_group_name            {Device Group 3}        \
    -device_group_multiplier      5                       \
    -device_group_enabled         1                       \
]
if {[keylget device_group_5_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget device_group_5_status log]"
}
set deviceGroup_5_handle [keylget device_group_5_status device_group_handle]

set multivalue_9_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.13.01.00.00.01       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_9_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_9_status log]"
}
set multivalue_9_handle [keylget multivalue_9_status multivalue_handle]

set ethernet_5_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 3}               \
    -protocol_handle              $deviceGroup_5_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_9_handle       \
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
if {[keylget ethernet_5_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ethernet_5_status log]"
}
set ethernet_5_handle [keylget ethernet_5_status ethernet_handle]

set multivalue_10_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          100.1.0.100             \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_10_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_10_status log]"
}
set multivalue_10_handle [keylget multivalue_10_status multivalue_handle]

set ipv4_3_status [::ixiangpf::interface_config \
    -protocol_name                     {IPv4 2}                   \
    -protocol_handle                   $ethernet_5_handle         \
    -ipv4_resolve_gateway              1                          \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01          \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00          \
    -gateway                           0.0.0.0                    \
    -gateway_step                      0.0.0.0                    \
    -intf_ip_addr                      $multivalue_10_handle      \
    -netmask                           255.255.255.0              \
]
if {[keylget ipv4_3_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ipv4_3_status log]"
}
set ipv4_3_handle [keylget ipv4_3_status ipv4_handle]

set lns_1_status [::ixiangpf::l2tp_config \
    -mode                    lns                                 \
    -handle                  $ipv4_3_handle                      \
    -protocol_name           {L2TP Network Server 1}             \
    -action                  create                              \
    -avp_hide                0                                   \
    -ctrl_chksum             1                                   \
    -ctrl_retries            30                                  \
    -data_chksum             0                                   \
    -hello_interval          60                                  \
    -hello_req               0                                   \
    -hostname                ixia                                \
    -init_ctrl_timeout       2                                   \
    -length_bit              0                                   \
    -max_ctrl_timeout        8                                   \
    -no_call_timeout         5                                   \
    -offset_bit              0                                   \
    -offset_byte             0                                   \
    -offset_len              0                                   \
    -rws                     10                                  \
    -secret                  ixia                                \
    -sequence_bit            0                                   \
    -tun_auth                tunnel_authentication_disabled      \
    -udp_dst_port            1701                                \
    -udp_src_port            1701                                \
    -bearer_capability       both                                \
    -bearer_type             analog                              \
    -framing_capability      sync                                \
    -lns_host_name           ixia                                \
]
if {[keylget lns_1_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget lns_1_status log]"
}
set lns_1_handle [keylget lns_1_status lns_handle]

set multivalue_11_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          2.2.2.2                 \
    -counter_step           0.0.1.0                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_11_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_11_status log]"
}
set multivalue_11_handle [keylget multivalue_11_status multivalue_handle]

set multivalue_12_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          1:1:1:0:0:0:0:0         \
    -counter_step           0:0:1:0:0:0:0:0         \
    -counter_direction      increment               \
    -nest_step              0:1:0:0:0:0:0:0         \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_12_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_12_status log]"
}
set multivalue_12_handle [keylget multivalue_12_status multivalue_handle]

set multivalue_13_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          0:11:22:11:0:0:0:1      \
    -counter_step           0:0:0:1:0:0:0:0         \
    -counter_direction      increment               \
    -nest_step              0:0:1:0:0:0:0:0         \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_13_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_13_status log]"
}
set multivalue_13_handle [keylget multivalue_13_status multivalue_handle]

set pppoxserver_1_status [::ixiangpf::pppox_config \
    -port_role                            network                    \
    -handle                               $lns_1_handle              \
    -protocol_name                        {PPPoX Server 1}           \
    -enable_mru_negotiation               0                          \
    -desired_mru_rate                     1492                       \
    -enable_max_payload                   0                          \
    -server_ipv6_ncp_configuration        clientmay                  \
    -server_ipv4_ncp_configuration        clientmay                  \
    -lcp_enable_accm                      0                          \
    -lcp_accm                             ffffffff                   \
    -num_sessions                         2                          \
    -auth_req_timeout                     10                         \
    -config_req_timeout                   10                         \
    -echo_req                             0                          \
    -echo_rsp                             1                          \
    -ip_cp                                ipv4_cp                    \
    -ipcp_req_timeout                     10                         \
    -max_auth_req                         20                         \
    -max_terminate_req                    3                          \
    -password                             password                   \
    -chap_secret                          secret                     \
    -username                             user                       \
    -chap_name                            user                       \
    -mode                                 add                        \
    -auth_mode                            none                       \
    -echo_req_interval                    10                         \
    -max_configure_req                    3                          \
    -max_ipcp_req                         3                          \
    -ac_name                              ixia                       \
    -enable_domain_group_map              0                          \
    -enable_server_signal_iwf             0                          \
    -enable_server_signal_loop_char       0                          \
    -enable_server_signal_loop_encap      0                          \
    -enable_server_signal_loop_id         0                          \
    -ipv6_pool_prefix_len                 48                         \
    -ipv6_pool_prefix                     $multivalue_12_handle      \
    -ipv6_pool_addr_prefix_len            64                         \
    -ppp_local_iid                        $multivalue_13_handle      \
    -ppp_local_ip                         $multivalue_11_handle      \
    -ppp_local_ip_step                    0.0.0.1                    \
    -ppp_local_iid_step                   1                          \
    -ppp_peer_iid                         0:11:11:11:0:0:0:1         \
    -ppp_peer_iid_step                    1                          \
    -ppp_peer_ip                          1.1.1.1                    \
    -ppp_peer_ip_step                     0.0.0.1                    \
    -send_dns_options                     0                          \
    -dns_server_list                      2001:0:0:0:0:0:0:1         \
    -server_dns_options                   disable_extension          \
    -server_dns_primary_address           10.10.10.10                \
    -server_dns_secondary_address         11.11.11.11                \
    -server_netmask_options               disable_extension          \
    -server_netmask                       255.255.255.0              \
    -server_wins_options                  disable_extension          \
    -server_wins_primary_address          10.10.10.10                \
    -server_wins_secondary_address        11.11.11.11                \
    -accept_any_auth_value                0                          \
    -lcp_max_failure                      5                          \
]
if {[keylget pppoxserver_1_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pppoxserver_1_status log]"
}
set pppoxserver_1_handle [keylget pppoxserver_1_status pppox_server_handle]
set pppoxServerSessions_1_handle [keylget pppoxserver_1_status pppox_server_sessions_handle]

set device_group_6_status [::ixiangpf::topology_config \
    -topology_handle              $topology_2_handle      \
    -device_group_name            {Device Group 6}        \
    -device_group_multiplier      50                      \
    -device_group_enabled         1                       \
]
if {[keylget device_group_6_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget device_group_6_status log]"
}
set deviceGroup_6_handle [keylget device_group_6_status device_group_handle]

set multivalue_14_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.16.01.00.00.01       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_14_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_14_status log]"
}
set multivalue_14_handle [keylget multivalue_14_status multivalue_handle]

set ethernet_6_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 6}               \
    -protocol_handle              $deviceGroup_6_handle      \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_14_handle      \
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
if {[keylget ethernet_6_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ethernet_6_status log]"
}
set ethernet_6_handle [keylget ethernet_6_status ethernet_handle]

set multivalue_15_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          102.1.0.100             \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_15_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_15_status log]"
}
set multivalue_15_handle [keylget multivalue_15_status multivalue_handle]

set ipv4_4_status [::ixiangpf::interface_config \
    -protocol_name                     {IPv4 4}                   \
    -protocol_handle                   $ethernet_6_handle         \
    -ipv4_resolve_gateway              1                          \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01          \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00          \
    -gateway                           0.0.0.0                    \
    -gateway_step                      0.0.0.0                    \
    -intf_ip_addr                      $multivalue_15_handle      \
    -netmask                           255.255.255.0              \
]
if {[keylget ipv4_4_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget ipv4_4_status log]"
}
set ipv4_4_handle [keylget ipv4_4_status ipv4_handle]

set lns_2_status [::ixiangpf::l2tp_config \
    -mode                    lns                                 \
    -handle                  $ipv4_4_handle                      \
    -protocol_name           {L2TP Network Server 2}             \
    -action                  create                              \
    -avp_hide                0                                   \
    -ctrl_chksum             1                                   \
    -ctrl_retries            30                                  \
    -data_chksum             0                                   \
    -hello_interval          60                                  \
    -hello_req               0                                   \
    -hostname                ixia                                \
    -init_ctrl_timeout       2                                   \
    -length_bit              0                                   \
    -max_ctrl_timeout        8                                   \
    -no_call_timeout         5                                   \
    -offset_bit              0                                   \
    -offset_byte             0                                   \
    -offset_len              0                                   \
    -rws                     10                                  \
    -secret                  ixia                                \
    -sequence_bit            0                                   \
    -tun_auth                tunnel_authentication_disabled      \
    -udp_dst_port            1701                                \
    -udp_src_port            1701                                \
    -bearer_capability       both                                \
    -bearer_type             analog                              \
    -framing_capability      sync                                \
    -lns_host_name           ixia                                \
]
if {[keylget lns_2_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget lns_2_status log]"
}
set lns_2_handle [keylget lns_2_status lns_handle]

set multivalue_16_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          3.2.2.2                 \
    -counter_step           0.0.1.0                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_16_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_16_status log]"
}
set multivalue_16_handle [keylget multivalue_16_status multivalue_handle]

set multivalue_17_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          2:1:1:0:0:0:0:0         \
    -counter_step           0:0:1:0:0:0:0:0         \
    -counter_direction      increment               \
    -nest_step              0:1:0:0:0:0:0:0         \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_17_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_17_status log]"
}
set multivalue_17_handle [keylget multivalue_17_status multivalue_handle]

set multivalue_18_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          0:12:22:11:0:0:0:1      \
    -counter_step           0:0:0:1:0:0:0:0         \
    -counter_direction      increment               \
    -nest_step              0:0:1:0:0:0:0:0         \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_18_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget multivalue_18_status log]"
}
set multivalue_18_handle [keylget multivalue_18_status multivalue_handle]

set pppoxserver_2_status [::ixiangpf::pppox_config \
    -port_role                            network                    \
    -handle                               $lns_2_handle              \
    -protocol_name                        {PPPoX Server 2}           \
    -enable_mru_negotiation               0                          \
    -desired_mru_rate                     1492                       \
    -enable_max_payload                   0                          \
    -server_ipv6_ncp_configuration        clientmay                  \
    -server_ipv4_ncp_configuration        clientmay                  \
    -lcp_enable_accm                      0                          \
    -lcp_accm                             ffffffff                   \
    -num_sessions                         20                         \
    -auth_req_timeout                     10                         \
    -config_req_timeout                   10                         \
    -echo_req                             0                          \
    -echo_rsp                             1                          \
    -ip_cp                                ipv4_cp                    \
    -ipcp_req_timeout                     10                         \
    -max_auth_req                         20                         \
    -max_terminate_req                    3                          \
    -password                             password                   \
    -chap_secret                          secret                     \
    -username                             user                       \
    -chap_name                            user                       \
    -mode                                 add                        \
    -auth_mode                            none                       \
    -echo_req_interval                    10                         \
    -max_configure_req                    3                          \
    -max_ipcp_req                         3                          \
    -ac_name                              ixia                       \
    -enable_domain_group_map              0                          \
    -enable_server_signal_iwf             0                          \
    -enable_server_signal_loop_char       0                          \
    -enable_server_signal_loop_encap      0                          \
    -enable_server_signal_loop_id         0                          \
    -ipv6_pool_prefix_len                 48                         \
    -ipv6_pool_prefix                     $multivalue_17_handle      \
    -ipv6_pool_addr_prefix_len            64                         \
    -ppp_local_iid                        $multivalue_18_handle      \
    -ppp_local_ip                         $multivalue_16_handle      \
    -ppp_local_ip_step                    0.0.0.1                    \
    -ppp_local_iid_step                   1                          \
    -ppp_peer_iid                         0:11:11:11:0:0:0:1         \
    -ppp_peer_iid_step                    1                          \
    -ppp_peer_ip                          1.1.1.1                    \
    -ppp_peer_ip_step                     0.0.0.1                    \
    -send_dns_options                     0                          \
    -dns_server_list                      2001:0:0:0:0:0:0:1         \
    -server_dns_options                   disable_extension          \
    -server_dns_primary_address           10.10.10.10                \
    -server_dns_secondary_address         11.11.11.11                \
    -server_netmask_options               disable_extension          \
    -server_netmask                       255.255.255.0              \
    -server_wins_options                  disable_extension          \
    -server_wins_primary_address          10.10.10.10                \
    -server_wins_secondary_address        11.11.11.11                \
    -accept_any_auth_value                0                          \
    -lcp_max_failure                      5                          \
]
if {[keylget pppoxserver_2_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pppoxserver_2_status log]"
}
set pppoxserver_2_handle [keylget pppoxserver_2_status pppox_server_handle]
set pppoxServerSessions_2_handle [keylget pppoxserver_2_status pppox_server_sessions_handle]
    
puts "waiting for ports to become available ..."
after 5000

puts "Starting protocols ..."
set control_res [::ixia::test_control -action start_all_protocols]
if {[keylget control_res status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_res log]"
}

after 15000         
puts "Getting statistics per port..."
set l2tp_port_stats [::ixiangpf::l2tp_stats -port_handle $port_handle -mode aggregate]
if {[keylget l2tp_port_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget l2tp_port_stats log]"
}
        
puts "Stopping protocols ..."
set control_res [::ixia::test_control -action stop_all_protocols]
if {[keylget control_res status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_res log]"
}

puts "SUCCESS - [clock format [clock seconds] -format {%D %X}]"
return 1