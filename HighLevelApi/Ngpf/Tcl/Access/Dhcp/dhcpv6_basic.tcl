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
-topology_name              "DHCPv6 Client"                     \
-port_handle                $port_1                             \
-device_group_multiplier     10                                 \
-device_group_name          "Basic conf2"                      \
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
-topology_name              "DHCPv6 Server"                     \
-port_handle                $port_2                             \
-device_group_multiplier     2                                 \
-device_group_name          "Basic conf"                      \
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

puts "Configure client"

set dhcp_status [::ixiangpf::emulation_dhcp_group_config            \
	 -handle 				$deviceGroup_second_handle                           \
	 -mode					create	                                             \
	 -dhcp_range_ip_type				ipv6                                     \
     -protocol_name      "Dhcpv6_Client"                                         \
	 ]

 if {[keylget dhcp_status status] != $::SUCCESS} {
     puts "FAIL - $test_name - [keylget dhcp_status log]"
     return 0
 }
 
set dhcp_client [keylget dhcp_status dhcpv6client_handle]
 
 ############## verify keys###############

 set keys [list dhcpv6client_handle handle]

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
puts "configure server"

set dhcp_status [::ixiangpf::emulation_dhcp_server_config   \
		-handle						$deviceGroup_first_handle          \
		-count						7			                        \
		-dhcp6_ia_type				iata			                    \
		-lease_time                 86400                               \
		-ip_version					6			                        \
        -protocol_name              "Dhcpv6_server"                     \
]


   ############## verify keys###############
   
set keys [list dhcpv6server_handle handle]
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
set dhcp_server [keylget dhcp_status dhcpv6server_handle]
 
 
################################################################################
#                          Modify dhcp_client and server                       #
################################################################################

######### Modify dhcp server #########################

puts "Modify dhcp server"

set dhcp_status [::ixiangpf::emulation_dhcp_server_config \
		-handle						$dhcp_server                      \
        -mode                       modify                            \
		-count						3			                      \
		-dhcp6_ia_type				iata			                  \
		-lease_time                 5400                              \
		-ip_version					6			                      \
		-ipaddress_count				10		                      \
		-ip_dns1					1110::100	                      \
		-ip_dns1_step				0:0:0:0:0:0:0:1		              \
		-ip_dns2					100::100                          \
		-ip_dns2_step				0:0:0:0:0:0:1:1		              \
		-ipaddress_pool				10::100                           \
		-ipaddress_pool_step		0:0:0:0:0:0:0:1                   \
		-ipaddress_pool_prefix_length 	12                            \
		-ipaddress_pool_prefix_step	1                                 \
		-ip_address					1000::100                         \
		-ip_step					0:0:0:0:0:0:0:0100                \
		-ip_gateway					1110::100                         \
		-ip_gateway_step			0:0:0:0:0:0:0:1                   \
        -ipv6_gateway               1110::101                         \
        -ipv6_gateway_step          ::1                               \
		-ip_prefix_length			12                                \
		-ip_prefix_step				3                                 \
        -local_mac_outer_step  		0000.0001.0000                    \
		-local_mtu					1500		                      \
		-protocol_name				"DHCPv6_server"                   \
		-use_rapid_commit			1                                 \
		-pool_address_increment		200:200:200::0                    \
		-pool_address_increment_step 0:0:0:0:0:0:0:2                  \
		-dns_domain					blabla	                          \
		-custom_rebind_time			240                               \
		-custom_renew_time			140                               \
		-use_custom_times			1                                 \
		-start_pool_prefix			100::20                           \
		-start_pool_prefix_step		0::2                              \
		-pool_prefix_increment_step	0::3                              \
		-pool_prefix_size			100                               \
		-prefix_length				24                                \
		-ping_timeout				10                                \
		-ping_check					1                                 \
		-pool_prefix_increment    	300:200:200::0   				  \
        -local_mac                  00bc.00ad.0003                    \
		-enable_resolve_gateway		0								  \
		-manual_gateway_mac		    00bd.2340.0000					  \
		-manual_gateway_mac_step 	0000.0000.0001					  \
	]
    
if {[keylget dhcp_status status] != $::SUCCESS} {
   puts "Error [keylget dhcp_status log]"
   incr cfgErrors
}

######### Modify dhcp client #########################


set dhcp_status [::ixiangpf::emulation_dhcp_group_config \
		-handle						$dhcp_client                     \
        -mode                       modify                           \
		-mac_addr					00:00:01:00:00:01                \
		-mac_addr_step				00.00.00.00.00.02                \
		-num_sessions				3                                \
		-mac_mtu						1800                         \
		-vlan_user_priority				2                            \
		-dhcp_range_ip_type				ipv6                         \
		-dhcp6_range_duid_enterprise_id			15                   \
		-dhcp6_range_duid_type					duid_en              \
		-dhcp6_range_duid_vendor_id				20                   \
		-dhcp6_range_duid_vendor_id_increment	2                    \
		-dhcp_range_renew_timer					10                   \
		-use_vendor_id							1                    \
		-dhcp6_use_pd_global_address			1                    \
		-protocol_name					dhcpv6client                 \
		-dhcp6_range_ia_type			iana_iapd                    \
		-dhcp6_range_ia_t2						40000                \
		-dhcp6_range_ia_t1						30000                \
		-dhcp6_range_ia_id_increment			2                    \
		-dhcp6_range_ia_id						20                   \
        -use_rapid_commit                        1                   \
	]
if {[keylget dhcp_status status] != $::SUCCESS} {
   puts "Error [keylget dhcp_status log]"
   incr cfgErrors
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
puts [::ixia::keylprint control_status]

puts "Starting dhcp client...."
set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcp_client                            \
	-action bind						                            \
]

if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

after 20000

################################################################################
#                       Stop protocols                                         #
################################################################################
 ############ stop server ################

puts "Stoppimg server...."

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
	-handle	 $deviceGroup_first_handle                              \
 ]
if {[keylget stop_item_status status] != $::SUCCESS} {
     puts "Error [keylget stop_item_status log]"
    incr cfgErrors
}
 
 
 ################ stop client ################################### 
puts "Stoppimg client...."

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
	-handle	 $deviceGroup_second_handle                             \
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
puts "Deleteing dhcp client topology..."
 set dhcp_status [::ixiangpf::emulation_dhcp_group_config  \
	-handle 				$dhcp_client                               \
	-mode					reset	                                   \
]
	if {[keylget dhcp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget dhcp_status log]"
    return 0
}

 ########### delete dhcp server ############################
puts "Deleteing dhcp server topology..."
 
set dhcp_status [::ixiangpf::emulation_dhcp_server_config   \
	-handle 				$dhcp_server                                \
	-mode					reset	                                    \
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