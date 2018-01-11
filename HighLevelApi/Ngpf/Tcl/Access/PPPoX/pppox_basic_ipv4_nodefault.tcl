#py> TOPOLOGY: 2p-1G
#py> TIMEOUT: 900

namespace eval ::cfg {}
set ::cfg::hltapi_p2no_hltset HLTSET142
set env(IXIA_VERSION) $::cfg::hltapi_p2no_hltset 

################################################################################
#                          Configure topology                                  #
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}
set test_name                   [info script]
set chassis_ip                  10.215.180.120
set tcl_server                  10.215.180.120
set ixnetwork_tcl_server        127.0.0.1:8009
set port_list                   [list 5/1 5/2]
set cfgErrors                   0

set connect_status [::ixiangpf::connect      \
        -reset                                           \
        -device                 $chassis_ip              \
        -port_list              $port_list               \
        -ixnetwork_tcl_server   $ixnetwork_tcl_server    \
        -tcl_server             $tcl_server              \
]

if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port_2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]
set port_handle [list $port_1 $port_2] 

 ####################### Create Topologies ###################################

set topology_status [::ixiangpf::topology_config    \
-topology_name              "PPPoX Client"                     \
-port_handle                $port_1                             \
-device_group_multiplier     10                                 \
-device_group_name          "Basic conf_client"                 \
-device_group_enabled       1                                   \
]
puts "Configured topology 1"

if {[keylget topology_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_status log]"
    return 0
}

set deviceGroup_first_handle [keylget topology_status device_group_handle]
set top_1 [keylget topology_status topology_handle]



 ########################### Topology 2 ###################################

 set topology_status [::ixiangpf::topology_config              \
-topology_name              "PPPoX Server"                     \
-port_handle                $port_2                            \
-device_group_multiplier     2                                 \
-device_group_name          "Basic conf_server"                \
]

puts "Configured topology 2"
if {[keylget topology_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_status log]"
    return 0
}
set deviceGroup_second_handle [keylget topology_status device_group_handle]
set top_handle [keylget topology_status topology_handle]
set top_2 [keylget topology_status topology_handle]

################################################################################
#                   Create PPPoX client and server                             #
################################################################################
puts "Create PPPoX Server"

set pppoxserver_1_status [::ixiangpf::pppox_config                      \
        -port_role                         network                      \
        -handle                            $deviceGroup_second_handle   \
        -mode                                 add                       \
        -protocol_name                      "PPPoX Server"              \
		-ip_cp                                ipv4_cp                   \
		-ac_name                              ixia                      \
        -ppp_peer_ip_step                     0.0.0.1                   \
		-ppp_local_ip                         2.2.1.1                   \
        -ppp_local_ip_step                    0.0.0.2                   \
		-ppp_peer_ip                          3.3.3.3                   \
        -ipv6_pool_prefix_len                  78                       \
        -ipv6_pool_prefix                   2000::30:20                 \
        -ipv6_pool_addr_prefix_len          79                          \
        -unlimited_redial_attempts            1                         \
        -enable_mru_negotiation               1                         \
        -desired_mru_rate                     1500                      \
        -max_payload                          3000                      \
        -enable_max_payload                   1                         \
        -num_sessions                         10                        \
        -ac_select_mode                     first_responding            \
        -ac_match_name                        ixia                      \
        -auth_req_timeout                      20                       \
        -config_req_timeout                    20                       \
        -echo_req                              1                        \
        -echo_rsp                              1                        \
        -ipcp_req_timeout                      20                       \
        -max_auth_req                                   15              \
        -max_padi_req                                   15              \
        -max_padr_req                                  15               \
        -max_terminate_req                             15               \
        -padi_req_timeout                              9                \
        -padr_req_timeout                               8               \
        -password                                       ixia            \
        -chap_secret                                    ixia            \
        -username                                       ixia            \
        -chap_name                                    ixia              \
        -vlan_id                                        30              \
        -vlan_id_count                                  2               \
        -vlan_id_step                                  10               \
        -vlan_user_priority                             6               \
        -auth_mode                                      pap_or_chap     \
        -echo_req_interval                              40              \
        -mac_addr                                       0000.0ffd.00ab  \
        -mac_addr_step                                  0000.1000.0000  \
        -max_configure_req                              74              \
        -max_ipcp_req                                   74              \
        -data_link                                    ethernet          \
        -enable_domain_group_map                        1               \
        -enable_server_signal_iwf                     0                 \
        -enable_server_signal_loop_char               1                 \
        -enable_server_signal_loop_encap               1                \
        -enable_server_signal_loop_id                 1                 \
         -redial                                        1               \
         -redial_max                                    253             \
         -redial_timeout                                56000           \
         -service_name                              "Florin conf"       \
         -service_type                                    any           \
         -server_wins_options              supply_primary_and_secondary \
         -server_wins_primary_address                    30.20.0.1      \
         -server_wins_secondary_address                  40.10.0.1      \
         -ra_timeout                                     3              \
         -create_interfaces                             1               \
         -attempt_rate                                   1000           \
         -attempt_max_outstanding                        1000           \
         -attempt_interval                               0              \
         -attempt_enabled                                1              \
         -enable_session_lifetime                         1             \
         -send_dns_options                                 1            \
         -server_dns_options               supply_primary_and_secondary \
         -server_dns_primary_address                     10.10.0.1      \
         -server_dns_secondary_address                   8.8.8.8        \
         -server_netmask_options                        supply_netmask  \
         -server_netmask                                 255.255.255.0  \
         -min_lifetime                                   20             \
         -max_lifetime                                   100000         \
         -enable_session_lifetime_restart                1              \
         -max_session_lifetime_restarts                  20             \
         -unlimited_session_lifetime_restarts            1              \
]

if {[keylget pppoxserver_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pppoxserver_1_status log]"
    return 0
}
set pppox_server_handle [keylget pppoxserver_1_status handle]

    ###################Verify keys#########################

set keys [list handles handle]
foreach l $keys {
        set i 0
        foreach ll [keylkeys pppoxserver_1_status] {
                if {[string equal $l $ll]==1} {
                            incr i
                      }
          }
          set d1 [llength $keys]
          set ll [keylkeys pppoxserver_1_status] 
          set d2 [llength $ll]
          if {$i==0 || $d1!=$d2-1} {
                incr cfgErrors
                puts "key $l is not returned"
                }
}


set pppoxclient_1_status [::ixiangpf::pppox_config           \
        -port_role                            access                     \
        -mode                                add                         \
        -handle                          $deviceGroup_first_handle       \
		-ip_cp                                ipv4_cp                    \
		-redial_max                           200                        \
		-padr_req_timeout                     100                        \
		-auth_req_timeout                     20                         \
        -num_sessions                         5                          \
        -enable_client_signal_iwf                       0                \
        -enable_client_signal_loop_char               1                  \
        -enable_client_signal_loop_encap              1                  \
        -enable_client_signal_loop_id                 1                  \
        -vlan_id                                        30               \
        -vlan_id_count                                  2                \
        -vlan_id_step                                  10                \
        -vlan_user_priority                             6                \
        -vlan_user_priority_step                        2                \
        -auth_mode                                      pap_or_chap      \
        -protocol_name                        "PPP server"               \
        -password                                       ixia             \
        -chap_secret                                    ixia             \
        -client_dns_options               request_primary_and_secondary  \
        -client_dns_primary_address                    10.10.10.30       \
        -client_dns_secondary_address                 172.168.3.1        \
        -client_netmask_options               request_specific_netmask   \
        -client_netmask                       128.0.0.0                  \
        -client_wins_options           request_primaryandsecondary_wins  \
        -client_wins_primary_address                    200.0.0.1        \
        -client_wins_secondary_address                  201.0.0.2        \
        -unlimited_redial_attempts            1                          \
]

if {[keylget pppoxclient_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pppoxclient_1_status log]"
    return 0
}

set pppox_client_handle [keylget pppoxclient_1_status handle]

    ###################Verify keys#########################

set keys [list handles handle]
foreach l $keys {
        set i 0
        foreach ll [keylkeys pppoxclient_1_status] {
                if {[string equal $l $ll]==1} {
                            incr i
                      }
          }
          set d1 [llength $keys]
          set ll [keylkeys pppoxclient_1_status] 
          set d2 [llength $ll]
          if {$i==0 || $d1!=$d2-1} {
                incr cfgErrors
                puts "key $l is not returned"
                }
}

################################################################################
#                          start protocols                                     #
################################################################################
puts "Start protocols"

set pppoxserver_control [::ixiangpf::pppox_control \
        -action                            connect                   \
        -handle                               $pppox_server_handle        \
    ]
if {[keylget pppoxserver_control status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pppoxserver_control log]"
    return 0
}


set pppoxclient_control [::ixiangpf::pppox_control \
	-action                            connect                   \
	-handle                               $pppox_client_handle        \
]

if {[keylget pppoxclient_control status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pppoxclient_control log]"
    return 0
}

after 60000

################################################################################
#                       Retrieve statistics                                    #
################################################################################
puts "Retrieve statistics"

set ppp_stats [::ixiangpf::pppox_stats      \
        -port_handle   $port_2	                        \
		-mode 	aggregate				                \
		-source client                                  \
        -execution_timeout 30                           \
	]

    if {[keylget ppp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ppp_stats log]"
    incr cfgErrors
}
    
set ppp_stats [::ixiangpf::pppox_stats      \
        -port_handle   $port_1	                        \
		-mode 	aggregate				                \
		-source server                                  \
        -execution_timeout 30                           \
	]

    if {[keylget ppp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ppp_stats log]"
    incr cfgErrors
}

set ppp_stats [::ixiangpf::pppox_stats      \
        -handle  $pppox_client_handle	                \
		-mode 	aggregate				                \
        -execution_timeout 60                           \
	]

    if {[keylget ppp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ppp_stats log]"
    incr cfgErrors
}

set ppp_stats [::ixiangpf::pppox_stats      \
        -handle  $pppox_server_handle 	                \
		-mode 	aggregate				                \
        -execution_timeout 60                          \
	]

    if {[keylget ppp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ppp_stats log]"
    incr cfgErrors
}
set ppp_stats [::ixiangpf::pppox_stats      \
        -handle  $pppox_client_handle	                \
		-mode 	session				                    \
        -execution_timeout 60                           \
	]
	
    if {[keylget ppp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ppp_stats log]"
    incr cfgErrors
}
set ppp_stats [::ixiangpf::pppox_stats      \
        -handle  $pppox_server_handle	                \
		-mode 	session				                    \
        -execution_timeout 60                          \
	]

if {[keylget ppp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ppp_stats log]"
    incr cfgErrors
}

################################################################################
#                       Stop protocol                                          #
################################################################################

set pppoxserver_control [::ixiangpf::pppox_control \
        -action                            disconnect                   \
        -handle                               $pppox_server_handle        \
    ]

if {[keylget pppoxserver_control status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pppoxserver_control log]"
    incr cfgErrors
}
    
set pppoxclient_control [::ixiangpf::pppox_control \
	-action                            disconnect                   \
	-handle                               $pppox_client_handle        \
]

if {[keylget pppoxclient_control status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pppoxclient_control log]"
    incr cfgErrors
}

set control_status [::ixiangpf::test_control  \
	-action stop_all_protocols							  \
]

if {[keylget control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status log]"
    incr cfgErrors
}

after 6000
################################################################################
#                       Remove protocol                                        #
################################################################################

puts "Remove PPPoX"
set remove [::ixiangpf::pppox_config \
        -port_role                            network                   \
        -handle                               $pppox_server_handle      \
        -mode                             remove                        \
]

if {[keylget remove status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget remove log]"
    incr cfgErrors
}

set remove [::ixiangpf::pppox_config                        \
        -port_role                            access                    \
        -handle                               $pppox_client_handle      \
        -mode                             remove                        \
]

if {[keylget remove status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget remove log]"
    incr cfgErrors
}

if {$cfgErrors != 0} {
    puts "FAIL - $test_name - Not all operation was finished with success"
    return 0
} 

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1

