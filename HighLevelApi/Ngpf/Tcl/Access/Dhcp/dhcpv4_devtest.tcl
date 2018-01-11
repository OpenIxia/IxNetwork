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

set topology_status [::ixiangpf::topology_config \
-topology_name				"T1"			\
-port_handle				$port_1			\
-device_group_multiplier	5				\
]
puts "Configured topology 1"

if {[keylget topology_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_status log]"
    return 0
}

set deviceGroup_first_handle [keylget topology_status device_group_handle]

set topology_status [::ixiangpf::topology_config \
-topology_name				"T2"			\
-port_handle				$port_2			\
-device_group_multiplier	5				\
]

puts "Configured topology 2"
if {[keylget topology_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_status log]"
    return 0
}

set deviceGroup_second_handle [keylget topology_status device_group_handle]

################################################################################
#                          Configure dhcp_client and server                    #
################################################################################

 ########################### Dhcp4 client #######################################

set dhcp_status [::ixiangpf::emulation_dhcp_group_config \
		-handle							$deviceGroup_first_handle    \
		-dhcp_range_ip_type				ipv4						 \
		-dhcp_range_renew_timer			2							 \
		-use_rapid_commit				0							 \
		-protocol_name					"Dhcpv4 Client 78"		     \
]

set dhcp_client [keylget dhcp_status dhcpv4client_handle]

if {[keylget dhcp_status status] != $::SUCCESS} {
     puts "FAIL - $test_name - [keylget dhcp_status log]"
     return 0
 }

#
 ########################### Dhcp4 server #######################################
#
set dhcp_status [::ixiangpf::emulation_dhcp_server_config \
		-handle						$deviceGroup_second_handle        \
		-lease_time                 86400                             \
		-ipaddress_count			10		                          \
		-ipaddress_pool				100.1.0.2                         \
		-ipaddress_pool_step		0.1.0.0                           \
		-ipaddress_pool_prefix_length 	16                            \
		-protocol_name				"Dhcpv4 Server"                   \
	]


set dhcp_server [keylget dhcp_status dhcpv4server_handle]

if {[keylget dhcp_status status] != $::SUCCESS} {
     puts "FAIL - $test_name - [keylget dhcp_status log]"
     return 0
 }

################################################################################
#                          start dhcp_client and server                        #
################################################################################

puts "Start dhcp server..."

set control_status [::ixiangpf::emulation_dhcp_server_control  \
	-dhcp_handle 			$dhcp_server 		\
	-action collect								\
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

puts "Start dhcp clients..."
set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcp_client\
	-action bind						\
]

if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

after 30000

################################################################################
#                       Retrieve statistics                                    #
################################################################################
puts "Retrive statistics"

set dhcp_stats_0 [::ixiangpf::emulation_dhcp_server_stats      \
        -port_handle   $port_2	                                           \
		-action 	collect				                                   \
        -execution_timeout 30                                              \
	]
    
  if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "Error [keylget dhcp_stats_0 log]"
    incr cfgErrors
}
 
set dhcp_stats_0 [::ixiangpf::emulation_dhcp_server_stats      \
	-dhcp_handle   $dhcp_server	                                           \
	-action 	collect				                                       \
    -execution_timeout 30                                                  \
]

 if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "Error [keylget dhcp_stats_0 log]"
    incr cfgErrors
}

set dhcp_stats_0 [::ixiangpf::emulation_dhcp_stats      \
        -port_handle   $port_1	                                    \
		-mode          aggregate_stats					            \
		-dhcp_version	dhcp4				                        \
        -execution_timeout 30                                       ]

if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "Error [keylget dhcp_stats_0 log]"
    incr cfgErrors
}
	
set dhcp_stats_0 [::ixiangpf::emulation_dhcp_stats      \
	-handle   $dhcp_client	                                        \
	-mode          aggregate_stats					                \
	-dhcp_version	dhcp4				                            \
    -execution_timeout 30                                           ]

 if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "Error [keylget dhcp_stats_0 log]"
    incr cfgErrors
}

set dhcp_stats_0 [::ixiangpf::emulation_dhcp_stats      \
        -handle   $dhcp_client	                                    \
		-mode          session					                    \
		-dhcp_version	dhcp4				                        \
        -execution_timeout 30                                       ]

 if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "Error [keylget dhcp_stats_0 log]"
    incr cfgErrors
}
 
################################################################################
#                       Stop protocols                                         #
################################################################################

puts "Stopping Server..."
set control_status [::ixiangpf::emulation_dhcp_server_control  \
	-dhcp_handle 		$dhcp_server 		                               \
	-action reset							                               \
]
if {[keylget control_status status] != $::SUCCESS} {
     puts "Error [keylget control_status log]"
    incr cfgErrors
}

puts "Stopping Client...."
set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 			$dhcp_client                                \
	-action release					                                \
]

if {[keylget control_status status] != $::SUCCESS} {
     puts "Error [keylget control_status log]"
    incr cfgErrors
}
puts "Stop all protocols..."
set control_status [::ixiangpf::test_control  \
	-action stop_all_protocols							  \
	
]

if {[keylget control_status status] != $::SUCCESS} {
     puts "Error [keylget control_status log]"
    incr cfgErrors
}

if {$cfgErrors != 0} {
    puts "FAIL - $test_name - Not all operation was finished with success"
    return 0
} 

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
