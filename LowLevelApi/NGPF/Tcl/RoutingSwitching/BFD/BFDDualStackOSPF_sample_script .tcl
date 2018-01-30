#Sourcing Ixia Library

package req Ixia

#performing connect to ixnetwork api server with chassis and port mentioned

set ixnetwork_api_server "localhost:8009"
set chassis_ip "10.216.100.216"
set port_list [list 1/3 1/4]

set connect [::ixiangpf::connect -ixnetwork_tcl_server $ixnetwork_api_server -device $chassis_ip -tcl_server $chassis_ip -port_list $port_list]

#fetching port handles
set port_handle1 [keylget connect port_handle.$chassis_ip.[lindex $port_list 0]]
set port_handle2 [keylget connect port_handle.$chassis_ip.[lindex $port_list 1]]

#configuration begins
#
######################################
#####Topology Config
######################################

    set topology_1_status [::ixiangpf::topology_config \
        -topology_name      {Topology 1}                            \
        -port_handle        $port_handle1      ]
    
    set topology_1_handle [keylget topology_1_status topology_handle]

    set device_group_1_status [::ixiangpf::topology_config \
        -topology_handle              $topology_1_handle      \
        -device_group_name            {Device Group 1}        \
        -device_group_multiplier      2                       \
        -device_group_enabled         1                       \
    ]
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
    set multivalue_1_handle [keylget multivalue_1_status multivalue_handle]

##########################################
##Ethernet config
##########################################

    set ethernet_1_status [::ixiangpf::interface_config \
        -protocol_name                {Ethernet 1}               \
        -protocol_handle              $deviceGroup_1_handle      \
        -mtu                          1500                       \
        -src_mac_addr                 $multivalue_1_handle       \
        -vlan                         1                          \
        -vlan_id                      1                          \
        -vlan_id_step                 1                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
        -use_vpn_parameters           0                          \
        -site_id                      0                          \
    ]
    set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]
    
    set multivalue_2_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          100.1.0.2               \
        -counter_step           0.0.1.0                 \
        -counter_direction      increment               \
        -nest_step              0.1.0.0                 \
        -nest_owner             $topology_1_handle      \
        -nest_enabled           1                       \
    ]
    set multivalue_2_handle [keylget multivalue_2_status multivalue_handle]
    
    set multivalue_3_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          100.1.0.1               \
        -counter_step           0.0.1.0                 \
        -counter_direction      increment               \
        -nest_step              0.1.0.0                 \
        -nest_owner             $topology_1_handle      \
        -nest_enabled           1                       \
    ]
    set multivalue_3_handle [keylget multivalue_3_status multivalue_handle]

###############################################
##IPv4 Config
###############################################

    set ipv4_1_status [::ixiangpf::interface_config \
        -protocol_name                     {IPv4 1}                  \
        -protocol_handle                   $ethernet_1_handle        \
        -ipv4_resolve_gateway              1                         \
        -ipv4_manual_gateway_mac           00.00.00.00.00.01         \
        -ipv4_manual_gateway_mac_step      00.00.00.00.00.00         \
        -gateway                           $multivalue_3_handle      \
        -intf_ip_addr                      $multivalue_2_handle      \
        -netmask                           255.255.255.0             \
    ]
    set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]
    set multivalue_4_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          192.0.0.1               \
        -counter_step           0.0.0.1                 \
        -counter_direction      increment               \
        -nest_step              0.1.0.0                 \
        -nest_owner             $topology_1_handle      \
        -nest_enabled           1                       \
    ]
    set multivalue_4_handle [keylget multivalue_4_status multivalue_handle]

##################################################
##Configuring BFDv4 with mode create    
##################################################

    set bfdv4_interface_1_status [::ixiangpf::emulation_bfd_config \
        -count                          1                         \
        -echo_rx_interval               0                         \
        -echo_timeout                   1500                      \
        -echo_tx_interval               0                         \
        -control_plane_independent      0                         \
        -enable_demand_mode             0                         \
        -flap_tx_interval               0                         \
        -handle                         $ipv4_1_handle            \
        -min_rx_interval                1000                      \
        -mode                           create                    \
        -detect_multiplier              3                         \
        -poll_interval                  0                         \
        -router_id                      $multivalue_4_handle      \
        -tx_interval                    1000                      \
        -configure_echo_source_ip       0                         \
        -echo_source_ip4                0.0.0.0                   \
        -ip_diff_serv                   0                         \
        -interface_active               1                         \
        -interface_name                 {BFDv4 IF 1}              \
        -router_active                  1                         \
        -router_name                    {BfdRouter 1}             \
        -session_count                  0                         \
        -ip_version                     4                         \
    ]
    set bfdv4Interface_1_handle [keylget bfdv4_interface_1_status bfd_v4_interface_handle]

######################################################
##Configuring OSFv2
######################################################
    set ospfv2_1_status [::ixiangpf::emulation_ospf_config \
        -handle                                                    $ipv4_1_handle            \
        -area_id                                                   0.0.0.0                   \
        -area_id_as_number                                         0                         \
        -area_id_type                                              number                    \
        -authentication_mode                                       null                      \
        -dead_interval                                             40                        \
        -demand_circuit                                            0                         \
        -graceful_restart_enable                                   0                         \
        -hello_interval                                            10                        \
        -router_interface_active                                   1                         \
        -enable_fast_hello                                         0                         \
        -hello_multiplier                                          2                         \
        -max_mtu                                                   1500                      \
        -protocol_name                                             {OSPFv2-IF 1}             \
        -router_active                                             1                         \
        -router_asbr                                               0                         \
        -do_not_generate_router_lsa                                0                         \
        -router_abr                                                0                         \
        -inter_flood_lsupdate_burst_gap                            33                        \
        -lsa_refresh_time                                          1800                      \
        -lsa_retransmit_time                                       5                         \
        -max_ls_updates_per_burst                                  1                         \
        -oob_resync_breakout                                       0                         \
        -interface_cost                                            10                        \
        -lsa_discard_mode                                          1                         \
        -md5_key_id                                                1                         \
        -network_type                                              ptop                      \
        -neighbor_router_id                                        0.0.0.0                   \
        -neighbor_router_id_step                                   0.0.0.0                   \
        -type_of_service_routing                                   0                         \
        -external_capabilities                                     1                         \
        -multicast_capability                                      0                         \
        -nssa_capability                                           0                         \
        -external_attribute                                        0                         \
        -opaque_lsa_forwarded                                      0                         \
        -unused                                                    0                         \
        -router_id                                                 $multivalue_4_handle      \
        -router_priority                                           2                         \
        -te_enable                                                 0                         \
        -te_max_bw                                                 125000000                 \
        -te_max_resv_bw                                            125000000                 \
        -te_unresv_bw_priority0                                    125000000                 \
        -te_unresv_bw_priority1                                    125000000                 \
        -te_unresv_bw_priority2                                    125000000                 \
        -te_unresv_bw_priority3                                    125000000                 \
        -te_unresv_bw_priority4                                    125000000                 \
        -te_unresv_bw_priority5                                    125000000                 \
        -te_unresv_bw_priority6                                    125000000                 \
        -te_unresv_bw_priority7                                    125000000                 \
        -te_metric                                                 0                         \
        -bfd_registration                                          1                         \
        -te_admin_group                                            0                         \
        -validate_received_mtu                                     1                         \
        -graceful_restart_helper_mode_enable                       0                         \
        -strict_lsa_checking                                       1                         \
        -support_reason_sw_restart                                 1                         \
        -support_reason_sw_reload_or_upgrade                       1                         \
        -support_reason_switch_to_redundant_processor_control      1                         \
        -support_reason_unknown                                    1                         \
        -mode                                                      create                    \
    ]
    set ospfv2_1_handle [keylget ospfv2_1_status ospfv2_handle]
    
    set multivalue_5_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          2000:0:0:1:0:0:0:2      \
        -counter_step           0:0:0:1:0:0:0:0         \
        -counter_direction      increment               \
        -nest_step              0:0:0:1:0:0:0:0         \
        -nest_owner             $topology_1_handle      \
        -nest_enabled           1                       \
    ]
    set multivalue_5_handle [keylget multivalue_5_status multivalue_handle]
    
    set multivalue_6_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          2000:0:0:1:0:0:0:1      \
        -counter_step           0:0:0:1:0:0:0:0         \
        -counter_direction      increment               \
        -nest_step              0:0:0:1:0:0:0:0         \
        -nest_owner             $topology_1_handle      \
        -nest_enabled           1                       \
    ]
    set multivalue_6_handle [keylget multivalue_6_status multivalue_handle]

##########################################################
##Configuring IPv6
##########################################################

    set ipv6_1_status [::ixiangpf::interface_config \
        -protocol_name                     {IPv6 1}                  \
        -protocol_handle                   $ethernet_1_handle        \
        -ipv6_multiplier                   1                         \
        -ipv6_resolve_gateway              1                         \
        -ipv6_manual_gateway_mac           00.00.00.00.00.01         \
        -ipv6_manual_gateway_mac_step      00.00.00.00.00.00         \
        -ipv6_gateway                      $multivalue_6_handle      \
        -ipv6_intf_addr                    $multivalue_5_handle      \
        -ipv6_prefix_length                64                        \
    ]
    set ipv6_1_handle [keylget ipv6_1_status ipv6_handle]

###########################################################
##Configuring BFDv6 using create    
###########################################################
 
    set bfdv6_interface_1_status [::ixiangpf::emulation_bfd_config \
        -count                          1                         \
        -echo_rx_interval               0                         \
        -echo_timeout                   1500                      \
        -echo_tx_interval               0                         \
        -control_plane_independent      0                         \
        -enable_demand_mode             0                         \
        -flap_tx_interval               0                         \
        -handle                         $ipv6_1_handle            \
        -min_rx_interval                1000                      \
        -mode                           create                    \
        -detect_multiplier              3                         \
        -poll_interval                  0                         \
        -router_id                      $multivalue_4_handle      \
        -tx_interval                    1000                      \
        -configure_echo_source_ip       0                         \
        -echo_source_ip6                0:0:0:0:0:0:0:0           \
        -ip_diff_serv                   0                         \
        -interface_active               1                         \
        -interface_name                 {BFDv6 IF 1}              \
        -router_active                  1                         \
        -router_name                    {BfdRouter 1}             \
        -session_count                  0                         \
        -ip_version                     6                         \
    ]
    set bfdv6Interface_1_handle [keylget bfdv6_interface_1_status bfd_v6_interface_handle]

###############################################################
##Configuring OSPFv3
###############################################################    
    set ospfv3_1_status [::ixiangpf::emulation_ospf_config \
        -handle                                                    $ipv6_1_handle            \
        -area_id                                                   0.0.0.0                   \
        -area_id_as_number                                         0                         \
        -area_id_type                                              area_id_as_number         \
        -dead_interval                                             40                        \
        -demand_circuit                                            0                         \
        -hello_interval                                            10                        \
        -router_interface_active                                   1                         \
        -enable_fast_hello                                         0                         \
        -hello_multiplier                                          2                         \
        -protocol_name                                             {OSPFv3-IF 1}             \
        -router_active                                             1                         \
        -router_asbr                                               0                         \
        -do_not_generate_router_lsa                                0                         \
        -router_abr                                                0                         \
        -lsa_refresh_time                                          1800                      \
        -lsa_retransmit_time                                       5                         \
        -instance_id                                               0                         \
        -lsa_discard_mode                                          1                         \
        -network_type                                              ptop                      \
        -external_capabilities                                     1                         \
        -nssa_capability                                           0                         \
        -router_id                                                 $multivalue_4_handle      \
        -router_priority                                           2                         \
        -bfd_registration                                          1                         \
        -graceful_restart_helper_mode_enable                       0                         \
        -strict_lsa_checking                                       1                         \
        -support_reason_sw_restart                                 1                         \
        -support_reason_sw_reload_or_upgrade                       1                         \
        -support_reason_switch_to_redundant_processor_control      1                         \
        -support_reason_unknown                                    0                         \
        -mode                                                      create                    \
        -session_type                                              ospfv3                    \
        -link_metric                                               10                        \
        -enable_ignore_db_desc_mtu                                 0                         \
        -router_bit                                                1                         \
        -v6                                                        1                         \
        -disable_auto_generate_link_lsa                            false                     \
        -ospfv3_lsa_flood_rate_control                             1000                      \
    ]
    set ospfv3_1_handle [keylget ospfv3_1_status ospfv3_handle]

##########################################################################
##Configuration repeats for the other half of ixia ports    
##########################################################################

    set topology_2_status [::ixiangpf::topology_config \
        -topology_name      {Topology 2}                            \
        -port_handle        $port_handle2      \
    ]
    set topology_2_handle [keylget topology_2_status topology_handle]
    
    set device_group_2_status [::ixiangpf::topology_config \
        -topology_handle              $topology_2_handle      \
        -device_group_name            {Device Group 2}        \
        -device_group_multiplier      2                       \
        -device_group_enabled         1                       \
    ]
    set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]
    
    set multivalue_7_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          00.12.01.00.00.01       \
        -counter_step           00.00.00.00.00.01       \
        -counter_direction      increment               \
        -nest_step              00.00.01.00.00.00       \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           1                       \
    ]
    set multivalue_7_handle [keylget multivalue_7_status multivalue_handle]
    
    set ethernet_2_status [::ixiangpf::interface_config \
        -protocol_name                {Ethernet 2}               \
        -protocol_handle              $deviceGroup_2_handle      \
        -mtu                          1500                       \
        -src_mac_addr                 $multivalue_7_handle       \
        -vlan                         1                          \
        -vlan_id                      1                          \
        -vlan_id_step                 1                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
        -use_vpn_parameters           0                          \
        -site_id                      0                          \
    ]
    set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]
    
    set multivalue_8_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          100.1.0.1               \
        -counter_step           0.0.1.0                 \
        -counter_direction      increment               \
        -nest_step              0.1.0.0                 \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           1                       \
    ]
    set multivalue_8_handle [keylget multivalue_8_status multivalue_handle]
    
    set multivalue_9_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          100.1.0.2               \
        -counter_step           0.0.1.0                 \
        -counter_direction      increment               \
        -nest_step              0.1.0.0                 \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           1                       \
    ]
    set multivalue_9_handle [keylget multivalue_9_status multivalue_handle]
    
    set ipv4_2_status [::ixiangpf::interface_config \
        -protocol_name                     {IPv4 2}                  \
        -protocol_handle                   $ethernet_2_handle        \
        -ipv4_resolve_gateway              1                         \
        -ipv4_manual_gateway_mac           00.00.00.00.00.01         \
        -ipv4_manual_gateway_mac_step      00.00.00.00.00.00         \
        -gateway                           $multivalue_9_handle      \
        -intf_ip_addr                      $multivalue_8_handle      \
        -netmask                           255.255.255.0             \
    ]
    set ipv4_2_handle [keylget ipv4_2_status ipv4_handle]
    
    set multivalue_10_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          193.0.0.1               \
        -counter_step           0.0.0.1                 \
        -counter_direction      increment               \
        -nest_step              0.1.0.0                 \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           1                       \
    ]
    set multivalue_10_handle [keylget multivalue_10_status multivalue_handle]
    
    set bfdv4_interface_2_status [::ixiangpf::emulation_bfd_config \
        -count                          1                          \
        -echo_rx_interval               0                          \
        -echo_timeout                   1500                       \
        -echo_tx_interval               0                          \
        -control_plane_independent      0                          \
        -enable_demand_mode             0                          \
        -flap_tx_interval               0                          \
        -handle                         $ipv4_2_handle             \
        -min_rx_interval                1000                       \
        -mode                           create                     \
        -detect_multiplier              3                          \
        -poll_interval                  0                          \
        -router_id                      $multivalue_10_handle      \
        -tx_interval                    1000                       \
        -configure_echo_source_ip       0                          \
        -echo_source_ip4                0.0.0.0                    \
        -ip_diff_serv                   0                          \
        -interface_active               1                          \
        -interface_name                 {BFDv4 IF 2}               \
        -router_active                  1                          \
        -router_name                    {BfdRouter 2}              \
        -session_count                  0                          \
        -ip_version                     4                          \
    ]
    set bfdv4Interface_2_handle [keylget bfdv4_interface_2_status bfd_v4_interface_handle]
    
    set ospfv2_2_status [::ixiangpf::emulation_ospf_config \
        -handle                                                    $ipv4_2_handle             \
        -area_id                                                   0.0.0.0                    \
        -area_id_as_number                                         0                          \
        -area_id_type                                              number                     \
        -authentication_mode                                       null                       \
        -dead_interval                                             40                         \
        -demand_circuit                                            0                          \
        -graceful_restart_enable                                   0                          \
        -hello_interval                                            10                         \
        -router_interface_active                                   1                          \
        -enable_fast_hello                                         0                          \
        -hello_multiplier                                          2                          \
        -max_mtu                                                   1500                       \
        -protocol_name                                             {OSPFv2-IF 2}              \
        -router_active                                             1                          \
        -router_asbr                                               0                          \
        -do_not_generate_router_lsa                                0                          \
        -router_abr                                                0                          \
        -inter_flood_lsupdate_burst_gap                            33                         \
        -lsa_refresh_time                                          1800                       \
        -lsa_retransmit_time                                       5                          \
        -max_ls_updates_per_burst                                  1                          \
        -oob_resync_breakout                                       0                          \
        -interface_cost                                            10                         \
        -lsa_discard_mode                                          1                          \
        -md5_key_id                                                1                          \
        -network_type                                              ptop                       \
        -neighbor_router_id                                        0.0.0.0                    \
        -neighbor_router_id_step                                   0.0.0.0                    \
        -type_of_service_routing                                   0                          \
        -external_capabilities                                     1                          \
        -multicast_capability                                      0                          \
        -nssa_capability                                           0                          \
        -external_attribute                                        0                          \
        -opaque_lsa_forwarded                                      0                          \
        -unused                                                    0                          \
        -router_id                                                 $multivalue_10_handle      \
        -router_priority                                           2                          \
        -te_enable                                                 0                          \
        -te_max_bw                                                 125000000                  \
        -te_max_resv_bw                                            125000000                  \
        -te_unresv_bw_priority0                                    125000000                  \
        -te_unresv_bw_priority1                                    125000000                  \
        -te_unresv_bw_priority2                                    125000000                  \
        -te_unresv_bw_priority3                                    125000000                  \
        -te_unresv_bw_priority4                                    125000000                  \
        -te_unresv_bw_priority5                                    125000000                  \
        -te_unresv_bw_priority6                                    125000000                  \
        -te_unresv_bw_priority7                                    125000000                  \
        -te_metric                                                 0                          \
        -bfd_registration                                          1                          \
        -te_admin_group                                            0                          \
        -validate_received_mtu                                     1                          \
        -graceful_restart_helper_mode_enable                       0                          \
        -strict_lsa_checking                                       1                          \
        -support_reason_sw_restart                                 1                          \
        -support_reason_sw_reload_or_upgrade                       1                          \
        -support_reason_switch_to_redundant_processor_control      1                          \
        -support_reason_unknown                                    1                          \
        -mode                                                      create                     \
    ]
    set ospfv2_2_handle [keylget ospfv2_2_status ospfv2_handle]
    
    set multivalue_11_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          2000:0:0:1:0:0:0:1      \
        -counter_step           0:0:0:1:0:0:0:0         \
        -counter_direction      increment               \
        -nest_step              0:0:0:1:0:0:0:0         \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           1                       \
    ]
    set multivalue_11_handle [keylget multivalue_11_status multivalue_handle]
    
    set multivalue_12_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          2000:0:0:1:0:0:0:2      \
        -counter_step           0:0:0:1:0:0:0:0         \
        -counter_direction      increment               \
        -nest_step              0:0:0:1:0:0:0:0         \
        -nest_owner             $topology_2_handle      \
        -nest_enabled           1                       \
    ]
    set multivalue_12_handle [keylget multivalue_12_status multivalue_handle]
    
    set ipv6_2_status [::ixiangpf::interface_config \
        -protocol_name                     {IPv6 2}                   \
        -protocol_handle                   $ethernet_2_handle         \
        -ipv6_multiplier                   1                          \
        -ipv6_resolve_gateway              1                          \
        -ipv6_manual_gateway_mac           00.00.00.00.00.01          \
        -ipv6_manual_gateway_mac_step      00.00.00.00.00.00          \
        -ipv6_gateway                      $multivalue_12_handle      \
        -ipv6_intf_addr                    $multivalue_11_handle      \
        -ipv6_prefix_length                64                         \
    ]
    set ipv6_2_handle [keylget ipv6_2_status ipv6_handle]
    
    set bfdv6_interface_2_status [::ixiangpf::emulation_bfd_config \
        -count                          1                          \
        -echo_rx_interval               0                          \
        -echo_timeout                   1500                       \
        -echo_tx_interval               0                          \
        -control_plane_independent      0                          \
        -enable_demand_mode             0                          \
        -flap_tx_interval               0                          \
        -handle                         $ipv6_2_handle             \
        -min_rx_interval                1000                       \
        -mode                           create                     \
        -detect_multiplier              3                          \
        -poll_interval                  0                          \
        -router_id                      $multivalue_10_handle      \
        -tx_interval                    1000                       \
        -configure_echo_source_ip       0                          \
        -echo_source_ip6                0:0:0:0:0:0:0:0            \
        -ip_diff_serv                   0                          \
        -interface_active               1                          \
        -interface_name                 {BFDv6 IF 2}               \
        -router_active                  1                          \
        -router_name                    {BfdRouter 2}              \
        -session_count                  0                          \
        -ip_version                     6                          \
    ]
    set bfdv6Interface_2_handle [keylget bfdv6_interface_2_status bfd_v6_interface_handle]
    
    set ospfv3_2_status [::ixiangpf::emulation_ospf_config \
        -handle                                                    $ipv6_2_handle             \
        -area_id                                                   0.0.0.0                    \
        -area_id_as_number                                         0                          \
        -area_id_type                                              area_id_as_number          \
        -dead_interval                                             40                         \
        -demand_circuit                                            0                          \
        -hello_interval                                            10                         \
        -router_interface_active                                   1                          \
        -enable_fast_hello                                         0                          \
        -hello_multiplier                                          2                          \
        -protocol_name                                             {OSPFv3-IF 2}              \
        -router_active                                             1                          \
        -router_asbr                                               0                          \
        -do_not_generate_router_lsa                                0                          \
        -router_abr                                                0                          \
        -lsa_refresh_time                                          1800                       \
        -lsa_retransmit_time                                       5                          \
        -instance_id                                               0                          \
        -lsa_discard_mode                                          1                          \
        -network_type                                              ptop                       \
        -external_capabilities                                     1                          \
        -nssa_capability                                           0                          \
        -router_id                                                 $multivalue_10_handle      \
        -router_priority                                           2                          \
        -bfd_registration                                          1                          \
        -graceful_restart_helper_mode_enable                       0                          \
        -strict_lsa_checking                                       1                          \
        -support_reason_sw_restart                                 1                          \
        -support_reason_sw_reload_or_upgrade                       1                          \
        -support_reason_switch_to_redundant_processor_control      1                          \
        -support_reason_unknown                                    0                          \
        -mode                                                      create                     \
        -session_type                                              ospfv3                     \
        -link_metric                                               10                         \
        -enable_ignore_db_desc_mtu                                 0                          \
        -router_bit                                                1                          \
        -v6                                                        1                          \
        -disable_auto_generate_link_lsa                            false                      \
        -ospfv3_lsa_flood_rate_control                             1000                       \
    ]
    set ospfv3_2_handle [keylget ospfv3_2_status ospfv3_handle]
    
    set ipv4_3_status [::ixiangpf::interface_config \
        -protocol_handle                    /globals      \
        -arp_on_linkup                      0             \
        -single_arp_per_gateway             1             \
        -ipv4_send_arp_rate                 200           \
        -ipv4_send_arp_interval             1000          \
        -ipv4_send_arp_max_outstanding      400           \
        -ipv4_send_arp_scale_mode           port          \
        -ipv4_attempt_enabled               0             \
        -ipv4_attempt_rate                  200           \
        -ipv4_attempt_interval              1000          \
        -ipv4_attempt_scale_mode            port          \
        -ipv4_diconnect_enabled             0             \
        -ipv4_disconnect_rate               200           \
        -ipv4_disconnect_interval           1000          \
        -ipv4_disconnect_scale_mode         port          \
        -ipv4_re_send_arp_on_link_up        true          \
    ]
    
    set ipv6_3_status [::ixiangpf::interface_config \
        -protocol_handle                   /globals      \
        -ns_on_linkup                      0             \
        -single_ns_per_gateway             1             \
        -ipv6_send_ns_rate                 200           \
        -ipv6_send_ns_interval             1000          \
        -ipv6_send_ns_max_outstanding      400           \
        -ipv6_send_ns_scale_mode           port          \
        -ipv6_attempt_enabled              0             \
        -ipv6_attempt_rate                 200           \
        -ipv6_attempt_interval             1000          \
        -ipv6_attempt_scale_mode           port          \
        -ipv6_diconnect_enabled            0             \
        -ipv6_disconnect_rate              200           \
        -ipv6_disconnect_interval          1000          \
        -ipv6_disconnect_scale_mode        port          \
        -ipv6_re_send_ns_on_link_up        true          \
    ]
    
    set ethernet_3_status [::ixiangpf::interface_config \
        -protocol_handle                     /globals      \
        -ethernet_attempt_enabled            0             \
        -ethernet_attempt_rate               200           \
        -ethernet_attempt_interval           1000          \
        -ethernet_attempt_scale_mode         port          \
        -ethernet_diconnect_enabled          0             \
        -ethernet_disconnect_rate            200           \
        -ethernet_disconnect_interval        1000          \
        -ethernet_disconnect_scale_mode      port          \
    ]
    
    set ospfv2_router_1_status [::ixiangpf::emulation_ospf_config \
        -handle                            /globals      \
        -enable_dr_bdr                     0             \
        -mode                              create        \
        -rate_control_interval             0             \
        -flood_lsupdates_per_interval      0             \
        -attempt_scale_mode                port          \
        -attempt_rate                      200           \
        -attempt_interval                  1000          \
        -attempt_enabled                   0             \
        -disconnect_scale_mode             port          \
        -disconnect_rate                   200           \
        -disconnect_interval               1000          \
        -disconnect_enabled                0             \
    ]
    set ospfv3_router_1_status [::ixiangpf::emulation_ospf_config \
        -handle             /globals      \
        -enable_dr_bdr      0             \
        -mode               create        \
        -session_type       ospfv3        \
    ]
   
##########################################Configuration Ends#################################




#############################################################
###Starting All Protocols
#############################################################

    ::ixia::test_control -action start_all_protocols
    #wait 60 seconds
    after 60000 
 
########################################################################################
#Fetching BFDv4 and BFDv6 stats, and will print number of autocreated session for each
########################################################################################
    
    set v4Stats [::ixiangpf::emulation_bfd_info \
    	-mode aggregate	\
	-handle $bfdv4Interface_1_handle ]

    set v6Stats [::ixiangpf::emulation_bfd_info \
	-mode aggregate \
    	-handle $bfdv6Interface_1_handle ]

    set port_1 {Ethernet - 001}
    puts $v4Stats
    set auto_created_v4 [keylget v4Stats $port_1.aggregate.sessions_auto_created]
    set auto_created_v6 [keylget v6Stats $port_1.aggregate.sessions_auto_created]

    puts "Auto Created session for BFDv4 : $auto_created_v4\nAuto Created session for BFDv6 : $auto_created_v6"

    after 10000

#######################################################################    
##Fetching Learned Info and displaying field Protocol_used_by
#######################################################################

    set v4Learned [::ixiangpf::emulation_bfd_info  \
    	-mode learned_info \
	-handle $bfdv4Interface_1_handle ]

    set v6Learned [::ixiangpf::emulation_bfd_info  \
    	-mode learned_info \
	-handle $bfdv6Interface_1_handle ]

    puts $v4Learned

    set prot_used_by_v4 [keylget v4Learned $bfdv4Interface_1_handle.bfd_learned_info.session_used_by_protocol] 
    set prot_used_by_v6 [keylget v6Learned $bfdv6Interface_1_handle.bfd_learned_info.session_used_by_protocol] 

    puts "Protocol Used by \nBFDv6 : $prot_used_by_v6 \nBFDv4 : $prot_used_by_v4"

##########################################################################
##Performing right click action set_admin_down/up
##########################################################################

    set return [::ixiangpf::emulation_bfd_control \
    	-mode set_admin_down \
	-handle $bfdv4Interface_1_handle \
	-protocol_name bfd ]

    after 10000

    set return [::ixiangpf::emulation_bfd_control \
    	-mode set_admin_up \
	-handle $bfdv4Interface_1_handle \
	-protocol_name bfd ]

    after 10000
#########################################################################
##Performing OTF for field tx_interval
#########################################################################

   set otf [ixNet getRoot]/globals/topology

   set return [::ixiangpf::emulation_bfd_config \
   	-mode modify  \
	-handle $bfdv4Interface_1_handle \
	-ip_version 4 \
	-tx_interval 3000 ]

   set return [::ixiangpf::emulation_bfd_config \
   	-mode modify  \
	-handle $bfdv6Interface_1_handle \
	-ip_version 6 \
	-tx_interval 3000 ]

   set return [::ixiangpf::emulation_bfd_config \
   	-mode modify  \
	-handle $bfdv4Interface_2_handle \
	-ip_version 4 \
	-tx_interval 3000 ]

   set return [::ixiangpf::emulation_bfd_config \
   	-mode modify  \
	-handle $bfdv6Interface_2_handle \
	-ip_version 6 \
	-tx_interval 3000 ]

   ixNet commit 
   ixNet exec applyOnTheFly $otf

########################################################################
##Performing Enable/Disable BFD Interfaces
########################################################################

   set return [::ixiangpf::emulation_bfd_config \
   	-mode disable \
	-handle $bfdv4Interface_1_handle \
	-ip_version 4]

   ixNet commit
   ixNet exec applyOnTheFly $otf

   after 20000
   set return [::ixiangpf::emulation_bfd_config \
   	-mode enable \
	-handle $bfdv6Interface_1_handle \
	-ip_version 6]

   ixNet commit
   ixNet exec applyOnTheFly $otf
   after 10000

########################################################################
##Stopping All protocols
########################################################################

   ::ixia::test_control -action stop_all_protocols
