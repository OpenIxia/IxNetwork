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
    puts "Eror - $test_name - [keylget connect_status log]"
    return 0
}

set port_1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port_2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]
set port_handle [list $port_1 $port_2] 

    #################### Create Topologies ###################################
    ########################### Topology 1 ###################################
set topology_status [::ixiangpf::topology_config    \
-topology_name              "PPPoX Client"                     \
-port_handle                $port_1                             \
-device_group_multiplier     10                                 \
-device_group_name          "Basic conf"                        \
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

 set topology_status [::ixiangpf::topology_config    \
-topology_name              "PPPoX Server"                      \
-port_handle                $port_2                              \
-device_group_multiplier     2                                   \
-device_group_name          "Basic conf"                         \
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
#                          Create ethernet handles                             #
################################################################################

set ethernet_1_status [::ixiangpf::interface_config \
	-protocol_handle              $deviceGroup_first_handle      \
	-vlan_id                      1                              \
	-vlan_user_priority           0                              \
	-vlan                         0                              \
	-vlan_user_priority_step      0                              \
	-protocol_name                "ETH 0"                        \
	-src_mac_addr                 00.11.01.00.00.01              \
	-vlan_tpid                    0x8100                         \
	-vlan_id_step                 0                              \
	-mtu                          1500                           \
	-vlan_id_count                1                              \
]

if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_1_status log]"
    return 0
}
set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]

set ethernet_2_status [::ixiangpf::interface_config \
	-protocol_handle              $deviceGroup_second_handle    \
	-vlan_id                      1                          \
	-vlan_user_priority           0                          \
	-vlan                         0                          \
	-vlan_user_priority_step      0                          \
	-protocol_name                "ETH 2"                    \
	-src_mac_addr                 00.12.01.00.00.01          \
	-vlan_tpid                    0x8100                     \
	-vlan_id_step                 0                          \
	-mtu                          1500                       \
	-vlan_id_count                1                          \
]

if {[keylget ethernet_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_2_status log]"
    return 0
}

set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]

################################################################################
#                   Create PPPoX client and server                             #
################################################################################
puts "Create PPPoX Server"

set pppoxserver_1_status [::ixiangpf::pppox_config \
        -port_role                            network                   \
        -handle                               $ethernet_2_handle        \
        -mode                                 add                       \
		-ip_cp                                ipv4_cp                   \
		-auth_req_timeout                     20                        \
		-ac_name                              ixia                      \
		-ppp_peer_ip_step                     0.0.0.1                   \
		-ppp_local_ip                         6.6.6.6                   \
        -ppp_local_ip_step                    0.0.0.1                   \
		-ppp_peer_ip                          1.1.1.1                   \
		-max_ipcp_req                         3                         \
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

puts "Create PPPoX Client "

set pppoxclient_1_status [::ixiangpf::pppox_config 			\
        -port_role                            access                    \
        -handle                               $ethernet_1_handle        \
        -mode                                 add                       \
		-ip_cp                                ipv4_cp                   \
		-redial_max                           200                       \
		-padr_req_timeout                     100                       \
		-auth_req_timeout                     20                        \
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

set pppoxserver_control [::ixiangpf::pppox_control 			\
        -action                            connect                   	\
        -handle                               $pppox_server_handle      \
    ]
if {[keylget pppoxserver_control status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pppoxserver_control log]"
    return 0
}


set pppoxclient_control [::ixiangpf::pppox_control 		\
	-action                            connect                   	\
	-handle                               $pppox_client_handle      \
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
        -port_handle   $port_2							\
		-mode 	aggregate								\
		-source client 									\
        -execution_timeout 30                           \
	]

    if {[keylget ppp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ppp_stats log]"
    incr cfgErrors
}
  
  
set ppp_stats [::ixiangpf::pppox_stats      \
        -port_handle   $port_1							\
		-mode 	aggregate								\
		-source server 									\
        -execution_timeout 30                           \
	]

    if {[keylget ppp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ppp_stats log]"
    incr cfgErrors
}


set ppp_stats [::ixiangpf::pppox_stats      \
        -handle  $pppox_client_handle					\
		-mode 	aggregate								\
        -execution_timeout 60                           \
	]

    if {[keylget ppp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ppp_stats log]"
    incr cfgErrors
}


set ppp_stats [::ixiangpf::pppox_stats      \
        -handle  $pppox_server_handle 					\
		-mode 	aggregate								\
        -execution_timeout 60                          	\
	]

    if {[keylget ppp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ppp_stats log]"
    incr cfgErrors
}


set ppp_stats [::ixiangpf::pppox_stats      \
        -handle  $pppox_client_handle					\
		-mode 	session									\
        -execution_timeout 60                           \
	]
	
    if {[keylget ppp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ppp_stats log]"
    incr cfgErrors
}


set ppp_stats [::ixiangpf::pppox_stats              \
        -handle  $pppox_server_handle	                        \
		-mode 	session				                            \
        -execution_timeout 60                                   \
	]

if {[keylget ppp_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ppp_stats log]"
    incr cfgErrors
}


################################################################################
#                       Stop protocol                                          #
################################################################################

set pppoxserver_control [::ixiangpf::pppox_control 			\
        -action                            disconnect                   \
        -handle                               $pppox_server_handle      \
    ]

if {[keylget pppoxserver_control status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget pppoxserver_control log]"
    incr cfgErrors
}
    
set pppoxclient_control [::ixiangpf::pppox_control 		\
	-action                            disconnect                   \
	-handle                               $pppox_client_handle      \
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



