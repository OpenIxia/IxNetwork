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

puts "Connected..."

 ####################### Create Topologies ###################################

set topology_status [::ixiangpf::topology_config    \
-topology_name              "DHCPv4 Client"                     \
-port_handle                $port_1                             \
-device_group_multiplier     10                                 \
]
puts "Configured topology 1"

if {[keylget topology_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_status log]"
    return 0
}

set deviceGroup_first_handle [keylget topology_status device_group_handle]
set top_1 [keylget topology_status topology_handle]



 ########################### Topology 2 ###################################

 set topology_status [::ixiangpf::topology_config 	\
-topology_name            	"DHCPv4 Server"                     \
-port_handle               	$port_2    	                        \
-device_group_multiplier 	 	1		                        \
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
#                          Configure dhcp_client and server                    #
################################################################################
 
 ############## configure dhcp client ##############################

set dhcp_status [::ixiangpf::emulation_dhcp_group_config  \
	 -handle        $deviceGroup_first_handle                         \
	 -protocol_name 				"Dhcp_client"                     \
	 -mac_addr  0000.0000.ffff                                        \
	 -mac_addr_step				00.00.00.00.00.02	                  \
	 -use_rapid_commit 0                                              \
	 -enable_stateless 0                                              \
     -num_sessions       30                                           \
     -vlan_id						100			                      \
     -vlan_id_step					20			                      \
     -vlan_user_priority				2			                  \
     -dhcp4_broadcast    1                                            \
     -dhcp_range_use_first_server 1                                   \
     -dhcp_range_renew_timer 20                                       \
     -dhcp_range_ip_type             ipv4                             \
     -vendor_id                          any                          \
 ]

 if {[keylget dhcp_status status] != $::SUCCESS} {
     puts "FAIL - $test_name - [keylget dhcp_status log]"
     return 0
 }
 
set dhcp_client [keylget dhcp_status dhcpv4client_handle]
 
 ############## verify keys###############

 set keys [list dhcpv4client_handle handle]

foreach l $keys {
        set i 0
        foreach ll [keylkeys dhcp_status] {
                if {[string equal $l $ll]==1} {
                            incr i
                      }
          }
          set d1 [llength $keys]
          set ll [keylkeys dhcp_status] 
          set d2 [llength $ll]
          if {$i==0 || $d1!=$d2-1} {
                incr cfgErrors
                puts "key $l is not returned"
                }
}

set dhcp_status [::ixiangpf::emulation_dhcp_config       \
	-handle 				$dhcp_client                             \
	-mode					modify	                                 \
	-release_rate				65	                                 \
	-msg_timeout				5	                                 \
	-request_rate				7	                                 \
	-retry_count				2	                                 \
	-interval_stop				5	                                 \
	-interval_start				6	                                 \
	-min_lifetime				10	                                 \
	-max_restarts				20	                                 \
	-max_lifetime				30	                                 \
	-enable_restart				1	                                 \
	-enable_lifetime			0	                                 \
    -client_port                    119                              \
    -skip_release_on_stop           1                                \
    -renew_on_link_up               1                                \
]

	if {[keylget dhcp_status status] != $::SUCCESS} {
    puts "Error [keylget dhcp_status log]"
    incr cfgErrors
}


############## configure dhcp server ##############################
 
  
set dhcp_status [::ixiangpf::emulation_dhcp_server_config 	            \
		-handle					$deviceGroup_second_handle              \
		-count					5			                            \
		-lease_time                86400                                \
		-ipaddress_count			10			                        \
		-ip_dns1				10.10.10.10		                        \
		-ip_dns1_step				0.0.0.1			                    \
		-ip_dns2				20.20.20.20		                        \
		-ip_dns2_step				0.0.1.0			                    \
		-ipaddress_pool				20.20.100.100	                    \
		-ipaddress_pool_step			0.0.0.1			                \
		-ipaddress_pool_prefix_length 		12			                \
		-ipaddress_pool_prefix_step		1			                    \
		-dhcp_offer_router_address		20.20.200.200	                \
		-dhcp_offer_router_address_step 	0.0.0.1			            \
		-ip_address				5.5.5.5			                        \
		-ip_step				0.0.0.1			                        \
		-ip_gateway				6.6.6.6			                        \
		-ip_gateway_step			0.0.0.1			                    \
		-ip_prefix_length			12			                        \
		-ip_prefix_step				1			                        \
		-local_mac                       0000.0001.0001                 \
       	-local_mac_outer_step          0000.0001.0000                   \
		-local_mtu				800			                            \
		-vlan_id					100			                        \
		-vlan_id_step				10			                        \
		-protocol_name			"DHCP4 Server modify"                   \
		-use_rapid_commit			1			                        \
		-pool_address_increment		30.30.30.30		                    \
		-pool_address_increment_step 		0.0.0.2			            \
		-ping_timeout				10			                        \
		-ping_check				1			                            \
        -echo_relay_info            1                                   \
		-enable_resolve_gateway		0								  	\
		-manual_gateway_mac		    00bd.2340.0000					  	\
		-manual_gateway_mac_step 	0000.0000.0001					  	\
	]

   ############## verify keys###############
   
set keys [list dhcpv4server_handle handle]
if {[keylget dhcp_status status] != $::SUCCESS} {
     puts "FAIL - $test_name - [keylget dhcp_status log]"
     return 0
 }
 
foreach l $keys {
        set i 0
        foreach ll [keylkeys dhcp_status] {
                if {[string equal $l $ll]==1} {
                            incr i
                      }
          }
          set d1 [llength $keys]
          set ll [keylkeys dhcp_status] 
          set d2 [llength $ll]
          if {$i==0 || $d1!=$d2-1} {
                incr cfgErrors
                puts "key $l is not returned"
                }
}

set dhcp_server [keylget dhcp_status dhcpv4server_handle]

################################################################################
#                          Modify dhcp_client and server                       #
################################################################################

set dhcp_status [::ixiangpf::emulation_dhcp_server_config \
		-handle						$dhcp_server    \
        -mode       modify                          \
		-lease_time                 86400           \
		-ipaddress_count			10		        \
		-ipaddress_pool				100.1.0.2       \
		-ipaddress_pool_step		0.1.0.0         \
		-ipaddress_pool_prefix_length 	16          \
		-protocol_name				"Dhcpv4_Server" \
	]

 if {[keylget dhcp_status status] != $::SUCCESS} {
     puts "FAIL - $test_name - [keylget dhcp_status log]"
     return 0
 }

  set dhcp_status [::ixiangpf::emulation_dhcp_group_config           \
	 -handle 				$dhcp_client                                         \
	 -mode					modify	                                             \
	 ]

 if {[keylget dhcp_status status] != $::SUCCESS} {
     puts "FAIL - $test_name - [keylget dhcp_status log]"
     return 0
 }
 

################################################################################
#                          start dhcp_client and server                        #
################################################################################
puts "Starting dhcp server...."
set control_status [::ixiangpf::emulation_dhcp_server_control  \
	-dhcp_handle 			$dhcp_server 		                           \
	-action collect								                           \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}
puts "Starting dhcp client...."
set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcp_client                            \
	-action bind						                            \
]

if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

after 30000

################################################################################
#                       Retrieve statistics                                    #
################################################################################
puts "Retrieve statistics" 
set dhcp_stats_0 [::ixiangpf::emulation_dhcp_server_stats      \
        -port_handle   $port_2	                                           \
		-action 	collect				                                   \
        -execution_timeout 60                                              \
	]
    
  if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "Error [keylget dhcp_stats_0 log]"
    incr cfgErrors
}
 
set dhcp_stats_0 [::ixiangpf::emulation_dhcp_server_stats      \
	-dhcp_handle   $dhcp_server	                                           \
	-action 	collect				                                       \
    -execution_timeout 60                                                  \
]

 if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "Error [keylget dhcp_stats_0 log]"
    incr cfgErrors
}

set dhcp_stats_0 [::ixiangpf::emulation_dhcp_stats      \
        -port_handle   $port_1	                                    \
		-mode          aggregate_stats					            \
		-dhcp_version	dhcp4				                        \
        -execution_timeout 60                                       \
	]

if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "Error [keylget dhcp_stats_0 log]"
    incr cfgErrors
}
	
set dhcp_stats_0 [::ixiangpf::emulation_dhcp_stats      \
	-handle   $dhcp_client	                                        \
	-mode          aggregate_stats					                \
	-dhcp_version	dhcp4				                            \
    -execution_timeout 60                                           \
]

 if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "Error [keylget dhcp_stats_0 log]"
    incr cfgErrors
}

set dhcp_stats_0 [::ixiangpf::emulation_dhcp_stats      \
        -handle   $dhcp_client	                                    \
		-mode          session					                    \
		-dhcp_version	dhcp4				                        \
        -execution_timeout 60                                       \
	]

 if {[keylget dhcp_stats_0 status] != $::SUCCESS} {
    puts "Error [keylget dhcp_stats_0 log]"
    incr cfgErrors
}


################################################################################
#                       Stop protocols                                         #
################################################################################
 ############ stop server ################

puts "Stopping server...."

set control_status [::ixiangpf::emulation_dhcp_server_control  \
	-dhcp_handle 			$dhcp_server 		                           \
	-action abort								                           \
]
if {[keylget control_status status] != $::SUCCESS} {
     puts "Error [keylget control_status log]"
    incr cfgErrors
}
 ############ stop all protocol on port 1#####################
set stop_item_status [::ixiangpf::test_control          \
	-action	 stop_protocol		                                    \
	-handle	 $deviceGroup_second_handle                              \
 ]
if {[keylget stop_item_status status] != $::SUCCESS} {
     puts "Error [keylget stop_item_status log]"
    incr cfgErrors
}
 
 
 ################ stop client ################################### 
puts "Stopping client...."

 set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcp_client                             \
	-action abort						                             \
]

if {[keylget control_status status] != $::SUCCESS} {
     puts "Error [keylget control_status log]"
    incr cfgErrors
}

set stop_item_status [::ixiangpf::test_control          \
	-action	 stop_protocol		                                    \
	-handle	 $deviceGroup_first_handle                             \
 ]
 
if {[keylget stop_item_status status] != $::SUCCESS} {
     puts "Error [keylget stop_item_status log]"
    incr cfgErrors
}

################################################################################
#                       delete topology                                        #
################################################################################
 
 after 10000
 ######### delete dhcp client ###########################
puts "Deleting dhcp server topology..."

set dhcp_status [::ixiangpf::emulation_dhcp_server_config   \
	-handle 				$dhcp_server                                \
	-mode					reset	                                    \
]
	if {[keylget dhcp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dhcp_status log]"
    return 0
}

 ########### delete dhcp server ############################
puts "Deleting dhcp client topology..."
 
set dhcp_status [::ixiangpf::emulation_dhcp_group_config  \
	-handle 				$dhcp_client                               \
	-mode					reset	                                   \
]

if {[keylget dhcp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dhcp_status log]"
    return 0
} 

############## delete both topology ###################################

set topology_status [::ixiangpf::topology_config    \
-mode                       destroy                             \
-topology_name              "DHCPv4 Client"                     \
-topology_handle             $top_1                             \
-device_group_multiplier     10                                 \
-device_group_enabled        0                                  \
-device_group_handle         $deviceGroup_first_handle          \
]

if {[keylget topology_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_status log]"
    return 0
}


set topology_status [::ixiangpf::topology_config    \
-mode                       destroy                             \
-topology_name              "DHCPv4 Server"                     \
-topology_handle             $top_2                             \
-device_group_multiplier     10                                 \
-device_group_enabled        0                                  \
-device_group_handle         $deviceGroup_second_handle         \
]
if {[keylget topology_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_status log]"
    return 0
}

if {$cfgErrors != 0} {
    puts "FAIL - $test_name - Not all operation was finished with success"
    return 0
} 

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1