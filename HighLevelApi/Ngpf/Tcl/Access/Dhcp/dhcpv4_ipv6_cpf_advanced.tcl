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
-topology_name              "DHCPv4 Client"                     \
-port_handle                $port_1                             \
-device_group_multiplier     10                                 \
-device_group_name          "Advance conf"                      \
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

 set topology_status [::ixiangpf::topology_config 	\
-topology_name            	"DHCPv4 Server"                     \
-port_handle               	$port_2    	                        \
-device_group_multiplier 	 	3		                        \
]
puts "Configured topology 2"
if {[keylget topology_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_status log]"
    return 0
}
set deviceGroup_second_handle [keylget topology_status device_group_handle]
set top_handle [keylget topology_status topology_handle]
set top_2 [keylget topology_status topology_handle]

################### Configure  IPv6 #####################################

puts "Configure Ipv6"

set interface_status [::ixiangpf::interface_config 	    \
            -protocol_handle  $deviceGroup_second_handle            \
            -port_handle  $port_2                                   \
            -src_mac_addr       	0000.0005.0001		            \
            -connector_type		routed				                \
            -ipv6_intf_addr		    3000::3000:0001                 \
            -ipv6_intf_addr_step    ::1000                          \
            -ipv6_resolve_gateway   0                               \
]

if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}

set ipv6_hand   [keylget interface_status ipv6_handle]

################################################################################
#                          Configure dhcp_client and server                    #
################################################################################
puts "Configure client"
 set dhcp_status [::ixiangpf::emulation_dhcp_group_config \
	 -handle 				$deviceGroup_first_handle                \
     -num_sessions          7                                        \
	 -protocol_name 				dhcp_florin                      \
	 -mac_addr  0000.0000.ffff                                        \
	 -mac_addr_step				00.00.00.00.00.02	                  \
	 -use_rapid_commit 0                                              \
	 -enable_stateless 0                                              \
     -vlan_id						100			                      \
     -vlan_id_step           4                                        \
     -dhcp4_broadcast    1                                            \
     -dhcp_range_use_first_server 1                                   \
     -dhcp_range_renew_timer 20                                       \
     -dhcp_range_ip_type             ipv4                             \
     -mac_mtu                               1500                      \
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

puts "Configure server"

set dhcp_status [::ixiangpf::emulation_dhcp_server_config   \
		-handle						$deviceGroup_second_handle           \
		-lease_time                 86400                               \
		-ipaddress_count			10		                            \
		-ipaddress_pool				100.1.0.2                           \
		-ipaddress_pool_step		0.1.0.0                             \
		-ipaddress_pool_prefix_length 	16                              \
		-protocol_name				"Dhcpv4_Server"                     \
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

puts "Configuring dhcpv6 server"

set dhcp_status [::ixiangpf::emulation_dhcp_server_config \
		-handle						$ipv6_hand                        \
        -ip_version					6			                      \
        -dhcp6_ia_type				iata			                  \
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

set dhcpv6_server [keylget dhcp_status dhcpv6server_handle]

set dhcp_status [::ixiangpf::emulation_dhcp_server_config \
		-handle						$dhcpv6_server                    \
		-mode 						modify						      \
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
	]	
	
if {[keylget dhcp_status status] != $::SUCCESS} {
     puts "FAIL - $test_name - [keylget dhcp_status log]"
     return 0
 }
 
 
 
 puts "Configure dhcpv6 client" 

set dhcp_status [::ixiangpf::emulation_dhcp_group_config \
		-handle						$deviceGroup_first_handle         \
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
     puts "FAIL - $test_name - [keylget dhcp_status log]"
     return 0
 }
 
set dhcpv6_client [keylget dhcp_status dhcpv6client_handle]
 

################################################################################
#                Modify dhcpv4  server and dhcpv6 client                       #
################################################################################

set dhcp_status [::ixiangpf::emulation_dhcp_server_config 	            \
		-handle					$dhcp_server                            \
        -mode                   modify                                  \
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
    
if {[keylget dhcp_status status] != $::SUCCESS} {
   puts "Error [keylget dhcp_status log]"
   incr cfgErrors
}


set dhcp_status [::ixiangpf::emulation_dhcp_group_config \
		-handle						$dhcpv6_client                   \
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
#                          test control dhcp_client and server                 #
################################################################################

puts "Start dhcp server..."

    ################### DHCPv4######################
set control_status [::ixiangpf::emulation_dhcp_server_control  \
	-dhcp_handle 			$dhcp_server 		\
	-action collect								\
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

    ################### DHCPv6######################
    
    set control_status [::ixiangpf::emulation_dhcp_server_control  \
	-dhcp_handle 			$dhcpv6_server 		\
	-action collect								\
    ]
    if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
    }

puts "Start dhcp clients..."
    ################### DHCPv4######################
set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcp_client\
	-action bind						\
]

if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

    ################### DHCPv6######################

set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcpv6_client\
	-action bind						\
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

after 15000

 ################################## Another operation ###############################

puts "Reset dhcp_server"
    ################### DHCPv4######################
set control_status [::ixiangpf::emulation_dhcp_server_control  \
	-dhcp_handle 			$dhcp_server 		                            \
	-action 	reset								                        \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

    ################### DHCPv6######################
    
    set control_status [::ixiangpf::emulation_dhcp_server_control  \
	-dhcp_handle 			$dhcpv6_server 		                            \
	-action 	reset								                        \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}


puts "Renew dhcp clients..."
    ################### DHCPv4######################
set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcp_client                            \
	-action renew						                            \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

    ################### DHCPv6######################

    set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcpv6_client                              \
	-action renew						                                \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}


after 15000
 ################################## Another operation ###############################

puts "Renew dhcp_server"
    ################### DHCPv4######################
set control_status [::ixiangpf::emulation_dhcp_server_control  \
	-dhcp_handle 			$dhcp_server 		                            \
	-action     renew								                        \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}
    ################### DHCPv6######################
set control_status [::ixiangpf::emulation_dhcp_server_control  \
	-dhcp_handle 			$dhcpv6_server 		                            \
	-action     renew								                        \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}
    ################### DHCPv4######################
puts "Rebind  dhcp clients..."
set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcp_client                            \
	-action rebind						                    \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

    ################### DHCPv6######################
    
set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcpv6_client                            \
	-action rebind						                    \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}
after 15000

    ################################# Another operation ###############################

puts "Restart down dhcp_server"

    ################### DHCPv4######################
set control_status [::ixiangpf::emulation_dhcp_server_control  \
	-dhcp_handle 			$dhcp_server 		                            \
	-action   restart_down								                    \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}
    ################### DHCPv6######################
    set control_status [::ixiangpf::emulation_dhcp_server_control  \
	-dhcp_handle 			$dhcpv6_server 		                            \
	-action   restart_down								                    \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

puts "Restart down dhcp clients..."
    ################### DHCPv4######################
set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcp_client                            \
	-action restart_down						                    \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

    ################### DHCPv6######################
set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcpv6_client                            \
	-action restart_down						                    \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}
after 15000

    ################################# Another operation ###############################
puts "Send_ping dhcp clients..."

    ################### DHCPv4######################
set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcp_client                            \
	-action send_ping						                        \
    -ping_destination       192.168.1.1                             \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

    ################### DHCPv6######################
    set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcpv6_client                            \
	-action send_ping						                        \
    -ping_destination       192.168.1.1                             \
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}
after 15000

puts "Release dhcp clients..."
    ################### DHCPv4######################
set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcp_client\
	-action release						\
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

    ################### DHCPv6######################
set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcpv6_client\
	-action release						\
]
if {[keylget control_status status] != $::SUCCESS} {
    puts "Error [keylget control_status log]"
    incr cfgErrors
}

after 6000
###############################################################################
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

set control_status [::ixiangpf::emulation_dhcp_server_control  \
	-dhcp_handle 			$dhcpv6_server 		                           \
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
puts "Stoppimg client...."

 set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcp_client                             \
	-action abort						                             \
]

if {[keylget control_status status] != $::SUCCESS} {
     puts "Error [keylget control_status log]"
    incr cfgErrors
}

 set control_status [::ixiangpf::emulation_dhcp_control  \
	-handle 				$dhcpv6_client                           \
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








