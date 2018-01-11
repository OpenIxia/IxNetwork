################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Daria Badea
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-13-2014 
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
#	 The script configures 2 VXLAN stacks and 2 emulated IPv4 VMs stacks       #
#	 Dynamics: Start/stop protocols and get stats.							   #
#    Traffic config, traffic control and traffic stats.						   #
#																			   #
# Module:                                                                      #
#    The sample was tested on an FlexFE LM	                        		   #
#                                                                              #
################################################################################

set port1 						9/1
set port2 						9/9
set test_name                   [info script]
set chassis_ip                  10.205.15.184
set ixnetwork_tcl_server        localhost
set port_list                   [list $port1 $port2]
set username                    user1

set PASSED 0
set FAILED 1

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - $retCode"
    return $FAILED
}

# #############################################################################
# 							CONNECT AND PORT HANDLES
# #############################################################################

set connect_status [::ixiangpf::connect \
        -reset                  1 \
        -device                 $chassis_ip \
        -username               $username \
        -port_list              $port_list \
        -ixnetwork_tcl_server   $ixnetwork_tcl_server \
        -tcl_server             $chassis_ip \
        -break_locks            1 \
        -connect_timeout        180 \
    ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - [keylget connect_status log]"
    return $FAILED
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}

set i 0
puts "Ixia port handles are:"
foreach port $port_handle {
    set port_$i $port
    puts $port
    set interface_handles_$port ""
    incr i
}

# #############################################################################
# 								VXLAN 1 CONFIG
# #############################################################################

# CREATE TOPOLOGY 1

set topology_1_status [::ixiangpf::topology_config					\
        -topology_name      {Topology 1}                            \
        -port_handle        $port_0								    \
    ]
if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_1_status log]"
    return $FAILED
}

set topology_1_handle [keylget topology_1_status topology_handle]

# CREATE DEVICE GROUP 1

set device_group_1_status [::ixiangpf::topology_config      \
		-topology_handle              $topology_1_handle        \
		-device_group_multiplier      3                         \
		-device_group_enabled         1                         \
]
if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_1_status log]"
    return $FAILED
}

set device_1_handle	[keylget device_group_1_status device_group_handle]

# CREATE ETHERNET STACK 1

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
    puts "FAIL - $multivalue_1_status"
	return $FAILED
}
set multivalue_1_handle [keylget multivalue_1_status multivalue_handle]

set ethernet_1_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 1}               \
    -protocol_handle              $device_1_handle           \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_1_handle       \
    -vlan                         1                          \
    -vlan_id                      101                        \
    -vlan_id_step                 1                          \
    -vlan_id_count                1                          \
    -vlan_tpid                    0x8100                     \
]
if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "FAIL - $ethernet_1_status"
	return $FAILED
}
set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]

# CREATE VXLAN STACK 1

set vxlan_1_status [::ixiangpf::emulation_vxlan_config                          \
        -create_ig								1								\
        -enable_resolve_gateway					1								\
        -enable_static_info						0								\
        -gateway								100.0.0.100						\
        -gateway_step							0.0.0.1							\
        -handle									$ethernet_1_handle				\
        -ig_enable_resolve_gateway				1								\
        -ig_gateway								70.0.0.100						\
        -ig_gateway_step						0.0.0.1							\
        -ig_intf_ip_addr						70.0.0.1						\
        -ig_intf_ip_addr_step					0.0.0.1							\
        -ig_intf_ip_prefix_length				16								\
        -ig_mac_address_init					00:11:22:33:00:00				\
        -ig_mac_address_step					00:00:00:00:00:11				\
        -ig_mac_mtu								1453							\
        -ig_manual_gateway_mac					00:00:00:00:00:12				\
        -ig_manual_gateway_mac_step				00:00:00:00:00:01				\
        -ig_vlan_id								300,400							\
        -ig_vlan_id_step						1,1								\
        -ig_vlan_user_priority					1,2								\
        -intf_ip_addr							100.0.0.1						\
        -intf_ip_addr_step						0.0.0.1							\
        -intf_ip_prefix_length					16								\
        -ipv4_multicast							225.1.1.1						\
        -mac_mtu								1336							\
        -manual_gateway_mac						00:00:00:00:00:12				\
        -manual_gateway_mac_step				00:00:00:00:00:01				\
        -mode									create							\
        -ip_to_vxlan_multiplier					1								\
        -remote_info_active						1							\
        -remote_vm_static_ipv4					70.0.0.100						\
        -remote_vm_static_mac					00:66:22:33:00:00				\
        -remote_vtep_ipv4						100.0.0.100						\
        -sessions_per_vxlan						2								\
        -static_info_count						1								\
        -vni									2233							\
		]
if {[keylget vxlan_1_status status] != $::SUCCESS} {
    puts "FAIL - [keylget vxlan_1_status log]"
    return $FAILED
}

set vxlan_1_handle [keylget vxlan_1_status vxlan_handle]

set vxlan_globals_status [::ixiangpf::emulation_vxlan_config        \
		-handle						/globals						\
        -outer_ip_dest_mode	        multicast						\
]
if {[keylget vxlan_globals_status status] != $::SUCCESS} {
    puts "FAIL - [keylget vxlan_globals_status log]"
    return $FAILED
}

# #############################################################################
# 								VTEP 2 CONFIG
# #############################################################################

# CREATE TOPOLOGY 2

set topology_2_status [::ixiangpf::topology_config					\
        -topology_name      {Topology 2}                            \
        -port_handle        $port_1								    \
    ]
if {[keylget topology_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_2_status log]"
    return $FAILED
}

set topology_2_handle [keylget topology_2_status topology_handle]

# CREATE DEVICE GROUP 2

set device_group_2_status [::ixiangpf::topology_config      \
		-topology_handle              $topology_2_handle        \
		-device_group_multiplier      3                         \
		-device_group_enabled         1                         \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_2_status log]"
    return $FAILED
}

set device_2_handle	[keylget device_group_2_status device_group_handle]

# CREATE ETHERNET STACK 2

set multivalue_2_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          00.22.01.00.00.01       \
    -counter_step           00.00.00.00.00.01       \
    -counter_direction      increment               \
    -nest_step              00.00.01.00.00.00       \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_2_status status] != $::SUCCESS} {
    puts "FAIL - $multivalue_2_status"
	return $FAILED
}
set multivalue_2_handle [keylget multivalue_2_status multivalue_handle]

set ethernet_1_status [::ixiangpf::interface_config \
    -protocol_name                {Ethernet 1}               \
    -protocol_handle              $device_2_handle           \
    -mtu                          1500                       \
    -src_mac_addr                 $multivalue_2_handle       \
    -vlan                         1                          \
    -vlan_id                      101                        \
    -vlan_id_step                 1                          \
    -vlan_id_count                1                          \
    -vlan_tpid                    0x8100                     \
]
if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "FAIL - $ethernet_1_status"
	return $FAILED
}
set ethernet_2_handle [keylget ethernet_1_status ethernet_handle]

# CREATE IPv4 STACK 2

set multivalue_2_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          100.0.0.100              \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget multivalue_2_status status] != $::SUCCESS} {
    puts "FAIL - $multivalue_2_status"
	return $FAILED
}
set multivalue_2_handle [keylget multivalue_2_status multivalue_handle]

set gw_multivalue_1_status [::ixiangpf::multivalue_config \
    -pattern                counter                 \
    -counter_start          100.0.0.1              \
    -counter_step           0.0.0.1                 \
    -counter_direction      increment               \
    -nest_step              0.1.0.0                 \
    -nest_owner             $topology_2_handle      \
    -nest_enabled           1                       \
]
if {[keylget gw_multivalue_1_status status] != $::SUCCESS} {
    puts "FAIL - $gw_multivalue_1_status"
	return $FAILED
}
set gw_multivalue_1_handle [keylget gw_multivalue_1_status multivalue_handle]

set ipv4_1_status [::ixiangpf::interface_config \
    -protocol_name                {IPv4 1}                  \
    -protocol_handle              $ethernet_2_handle        \
    -ipv4_resolve_gateway         1                         \
    -ipv4_manual_gateway_mac      00.00.00.00.00.01         \
    -gateway                      $gw_multivalue_1_handle   \
    -intf_ip_addr                 $multivalue_2_handle      \
	-netmask					  255.255.0.0				\
]
if {[keylget ipv4_1_status status] != $::SUCCESS} {
    puts "FAIL - $ipv4_1_status"
	return $FAILED
}
set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]

# CREATE VXLAN STACK 2

set vxlan_2_status [::ixiangpf::emulation_vxlan_config                               	\
        -create_ig								1								\
        -enable_resolve_gateway					1								\
        -enable_static_info						0								\
        -handle									$ipv4_1_handle					\
        -ig_enable_resolve_gateway				1								\
        -ig_gateway								70.0.0.1						\
        -ig_gateway_step						0.0.0.1							\
        -ig_intf_ip_addr						70.0.0.100						\
        -ig_intf_ip_addr_step					0.0.0.1							\
        -ig_intf_ip_prefix_length				16								\
        -ig_mac_address_init					00:66:22:33:00:00				\
        -ig_mac_address_step					00:00:00:00:00:11				\
        -ig_mac_mtu								1453							\
        -ig_manual_gateway_mac					00:00:00:00:00:12				\
        -ig_manual_gateway_mac_step				00:00:00:00:00:01				\
        -ig_vlan_id								300,400							\
        -ig_vlan_id_step						1,1								\
        -ig_vlan_user_priority					1,2								\
        -ipv4_multicast							225.1.1.1						\
        -mac_mtu								1336							\
        -manual_gateway_mac						00:00:00:00:00:12				\
        -manual_gateway_mac_step				00:00:00:00:00:01				\
        -mode									create							\
        -ip_to_vxlan_multiplier					1								\
        -remote_info_active						1							\
        -remote_vm_static_ipv4					70.0.0.1						\
        -remote_vm_static_mac					00:11:22:33:00:00				\
        -remote_vtep_ipv4						100.0.0.1						\
        -sessions_per_vxlan						2								\
        -static_info_count						1								\
        -vni									2233							\
		]
if {[keylget vxlan_2_status status] != $::SUCCESS} {
    puts "FAIL - [keylget vxlan_2_status log]"
    return $FAILED
}

set vxlan_2_handle [keylget vxlan_2_status vxlan_handle]

# #############################################################################
# 								START VXLAN
# #############################################################################

set control_status_1 [::ixiangpf::emulation_vxlan_control \
        -handle      	  $vxlan_1_handle                    \
        -action           start                      \
        ]
if {[keylget control_status_1 status] != $::SUCCESS} {
    puts "FAIL - [keylget control_status_1 log]"
    return $FAILED
}

set control_status_2 [::ixiangpf::emulation_vxlan_control \
        -handle      	  $vxlan_2_handle           \
        -action           start                     \
        ]
if {[keylget control_status_2 status] != $::SUCCESS} {
    puts "FAIL - [keylget control_status_2 log]"
    return $FAILED
}

while {[lindex [ixNet getA $vxlan_1_handle -stateCounts] 3]!="3" || [lindex [ixNet getA $vxlan_2_handle -stateCounts] 3]!="3"} {
	after 1000
	puts "Waiting for VXLAN to go up..."
}
puts "VXLAN stacks are up!"

set inner_ip_1_status [::ixiangpf::test_control \
        -action             start_protocol  \
        -handle             [keylget vxlan_1_status ig_ipv4_handle] \
        ]
if {[keylget inner_ip_1_status status] != $::SUCCESS} {
    puts "FAIL - [keylget inner_ip_1_status log]"
    return $FAILED
}

after 3000

set inner_ip_2_status [::ixiangpf::test_control \
        -action             start_protocol  \
        -handle             [keylget vxlan_2_status ig_ipv4_handle] \
        ]
if {[keylget inner_ip_2_status status] != $::SUCCESS} {
    puts "FAIL - [keylget inner_ip_2_status log]"
    return $FAILED
}

while {[lindex [ixNet getA [keylget vxlan_1_status ig_ipv4_handle] -stateCounts] 3]!="6" || [lindex [ixNet getA [keylget vxlan_2_status ig_ipv4_handle] -stateCounts] 3]!="6"} {
	after 1000
	puts "Waiting for inner IP to go up..."
}
puts "IP stacks are up!"

after 3000

# #############################################################################
# 								TRAFFIC CONFIG
# #############################################################################

set src_ip_endpoint			[keylget vxlan_1_status ig_ipv4_handle]
set dest_ip_endpoint		[keylget vxlan_2_status ig_ipv4_handle]

set rate_start_value        10
set frame_size_start        512

set traffic_status [::ixiangpf::traffic_config        											\
        -traffic_generator 							ixnetwork_540          					\
        -mode                						create               					\
		-circuit_endpoint_type          			ipv4                    				\
		-bidirectional								0										\
		-track_by                       			[list dest_ip source_ip]				\
		-name                   					"MULTICAST_IPv4"						\
        -emulation_src_handle   					$src_ip_endpoint					  	\
        -emulation_dst_handle   					$dest_ip_endpoint						\
        -src_dest_mesh                  			one_to_one                 				\
		-route_mesh									one_to_one								\
		-rate_percent                   			$rate_start_value       				\
        -frame_size                     			$frame_size_start       				\
		-l2_encap 									ethernet_ii								\
		-l3_protocol 								ipv4									\
		]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - [keylget traffic_status log]"
    return $FAILED
}

set traffic_status [::ixiangpf::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - [keylget traffic_status log]"
    return $FAILED
}

after 10000

set flow_traffic_status [::ixiangpf::traffic_stats                        \
        -mode                   flow                                        \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status log]"
    return $FAILED
}

set flow_results [list                                                      \
		"Source address" 				tracking.2.tracking_value			\
		"Destination address"			tracking.3.tracking_value			\
        "Tx Port"                       tx.port                             \
        "Rx Port"                       rx.port                             \
        "Tx Frames"                     tx.total_pkts                       \
        "Tx Frame Rate"                 tx.total_pkt_rate                   \
        "Rx Frames"                     rx.total_pkts                       \
        "Frames Delta"                  rx.loss_pkts                        \
        "Rx Frame Rate"                 rx.total_pkt_rate                   \
        "Loss %"                        rx.loss_percent                     \
        "Rx Bytes"                      rx.total_pkts_bytes                 \
        "Rx Rate (Bps)"                 rx.total_pkt_byte_rate              \
        "Rx Rate (bps)"                 rx.total_pkt_bit_rate               \
        "Rx Rate (Kbps)"                rx.total_pkt_kbit_rate              \
        "Rx Rate (Mbps)"                rx.total_pkt_mbit_rate              \
        "Avg Latency (ns)"              rx.avg_delay                        \
        "Min Latency (ns)"              rx.min_delay                        \
        "Max Latency (ns)"              rx.max_delay                        \
        "First Timestamp"               rx.first_tstamp                     \
        "Last Timestamp"                rx.last_tstamp                      \
        ]
		
set flows [keylget flow_traffic_status flow]
foreach flow [keylkeys flows] {
    set flow_key [keylget flow_traffic_status flow.$flow]
    puts "\tFlow $flow"
    foreach {name key} [subst $[subst flow_results]] {
        puts "\t\t$name: [keylget flow_traffic_status flow.$flow.$key]"
    }
}
foreach flow [keylkeys flows] {
    if {[keylget flow_traffic_status flow.$flow.tracking.2.tracking_value]!="100.0.0.1" && [keylget flow_traffic_status flow.$flow.tracking.2.tracking_value]!="100.0.0.2" && [keylget flow_traffic_status flow.$flow.tracking.2.tracking_value]!="100.0.0.3"} {
		puts "ERROR - IP source address is not correct for flow $flow!"
		incr cfgErrors
	}
    if {[keylget flow_traffic_status flow.$flow.tracking.3.tracking_value]!="225.1.1.1"} {
		puts "ERROR - IP destination address is not correct for flow $flow!"
		incr cfgErrors
	}
	set pkts_tx [keylget flow_traffic_status flow.$flow.tx.total_pkts]
	set pkts_rx [keylget flow_traffic_status flow.$flow.rx.total_pkts]
	if {$pkts_rx < [expr 0.8 * $pkts_tx]} {
		puts "ERROR - Packets loss detected for flow $flow!"
		incr cfgErrors
	}
}

set traffic_status [::ixiangpf::traffic_control                                 \
        -action                 stop                                         \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - [keylget traffic_status log]"
    return $FAILED
}

# #############################################################################
# 								STOP VXLAN
# #############################################################################

set control_status_0 [::ixiangpf::emulation_vxlan_control \
        -handle      	  $vxlan_1_handle                    \
        -action           stop                      \
        ]
if {[keylget control_status_0 status] != $::SUCCESS} {
    puts "FAIL - [keylget control_status_0 log]"
    return $FAILED
}

set control_status_1 [::ixiangpf::emulation_vxlan_control \
        -handle      	  $vxlan_2_handle              \
        -action           stop                     \
        ]
if {[keylget control_status_1 status] != $::SUCCESS} {
    puts "FAIL - [keylget control_status_1 log]"
    return $FAILED
}

while {[lindex [ixNet getA $vxlan_1_handle -stateCounts] 1]!="3" || [lindex [ixNet getA $vxlan_2_handle -stateCounts] 1]!="3"} {
	after 1000
	puts "Waiting for VXLAN to stop..."
}
puts "VXLAN stacks are stopped!"

after 3000

set cleanup [::ixiangpf::cleanup_session -reset]
if {[keylget cleanup status] != $::SUCCESS} {
	puts "FAIL - [keylget cleanup log]"
	return $FAILED
}

if {$cfgErrors > 0} {
	puts "FAIL - check configuration errors!"
	return $FAILED
}

puts "Done... IxNetwork session is closed..."
puts ""
puts "!!! PASSED !!!"
return $PASSED