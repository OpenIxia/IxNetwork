#!/usr/bin/tclsh

package require Ixia

set test_name [info script]
set chassisIP 10.205.4.35
set ixNetworkTclServerIp 10.205.1.42
set userName hgee
set port_list [list 1/1 1/2]

proc KeylPrint {keylist {space ""}} {
    upvar $keylist kl
    set result ""
    foreach key [keylkeys kl] {
	set value [keylget kl $key]
	if {[catch {keylkeys value}]} {
	    append result "$space$key: $value\n"
	} else {
	    set newspace "$space "
	    append result "$space$key:\n[KeylPrint value $newspace]"
	}
    }
    return $result
}

set connectStatus [::ixia::connect \
		       -reset \
		       -device $chassisIP \
		       -port_list $port_list \
		       -username $userName \
		       -tcl_server $chassisIP \
		       -ixnetwork_tcl_server $ixNetworkTclServerIp \
		       ]

if {[keylget connectStatus status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connectStatus log]"
}

set port_array [keylget connectStatus port_handle.$chassisIP]

set port_0 [keylget port_array [lindex $port_list 0]]
set port_1 [keylget port_array [lindex $port_list 1]]


#set ::ixia::debug 1
#set ::ixia::debug_file_name ixiaHltDebugLog.txt
set ::ixia::logHltapiCommandsFlag 1
#set ::ixia::logHltapiCommandsFileName ixiaHltCommandsLog.txt

set interface_status1 [::ixia::interface_config \
			   -port_handle        $port_0          \
			   -intf_ip_addr       172.16.31.1      \
			   -gateway            172.16.31.2      \
			   -netmask            255.255.255.0    \
			   -op_mode            normal           \
			   -vlan               $true            \
			   -vlan_id            100              \
			   -vlan_user_priority 7                \
			  ]
if {[keylget interface_status1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
set intf_h0 [keylget interface_status1 interface_handle]

set interfaceStatus2 [::ixia::interface_config \
			  -port_handle        $port_1          \
			  -intf_ip_addr       172.16.31.2      \
			  -gateway            172.16.31.1      \
			  -netmask            255.255.255.0    \
			  -op_mode            normal           \
			  -vlan               $true            \
			  -vlan_id            100              \
			  -vlan_user_priority 7                \
			 ]
if {[keylget interfaceStatus2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interfaceStatus2 log]"
}

set intf_h1 [keylget interfaceStatus2 interface_handle]

set trafficStatus1 [::ixia::traffic_config         \
			-circuit_endpoint_type  ipv4            \
			-mode                   create          \
			-emulation_src_handle   $intf_h0        \
			-emulation_dst_handle   $intf_h1        \
			-l3_protocol            ipv4            \
			-qos_type_ixn           custom          \
			-qos_value_ixn          5               \
			-qos_value_ixn_mode     incr            \
			-qos_value_ixn_step     2               \
			-qos_value_ixn_count    2               \
			-qos_value_ixn_tracking 1               \
			-track_by "flowGroup0 ethernet_ii_pfc_queue" \
		   ]

if {[keylget trafficStatus1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget trafficStatus1 log]"
}

set trafficStatus2 [::ixia::traffic_config         \
			-circuit_endpoint_type  ipv4            \
			-mode                   create          \
			-emulation_src_handle   $intf_h0        \
			-emulation_dst_handle   $intf_h1        \
			-l3_protocol            ipv4            \
			-qos_type_ixn           tos             \
			-ip_precedence          {0 3}           \
			-ip_precedence_mode     list            \
			-ip_precedence_tracking 1               \
			-track_by "flowGroup0 ipv4_precedence" \
		       ]

if {[keylget trafficStatus2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget trafficStatus2 log]"
}


set trafficStatus3 [::ixia::traffic_config         \
			-circuit_endpoint_type  ipv4            \
			-mode                   create          \
			-emulation_src_handle   $intf_h0        \
			-emulation_dst_handle   $intf_h1        \
			-l3_protocol            ipv4            \
			-qos_type_ixn           dscp            \
			-qos_value_ixn          dscp_default    \
			-ip_dscp                60              \
			-ip_dscp_mode           decr            \
			-ip_dscp_count          3               \
			-ip_dscp_step           10              \
			-ip_dscp_tracking       1               \
			-track_by "flowGroup0 default_phb" \
		   ]

if {[keylget trafficStatus3 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget trafficStatus3 log]"
}

set trafficStatus4 [::ixia::traffic_config         \
			-circuit_endpoint_type  ipv4            \
			-mode                   create          \
			-emulation_src_handle   $intf_h0        \
			-emulation_dst_handle   $intf_h1        \
			-l3_protocol            ipv4            \
			-qos_type_ixn           dscp            \
			-qos_value_ixn          {af_class1_low_precedence af_class2_high_precedence} \
			-qos_value_ixn_mode     list            \
			-qos_value_ixn_tracking 1               \
			-track_by "flowGroup0 assured_forwarding_phb" \
		       ]

if {[keylget trafficStatus4 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget trafficStatus4 log]"
}


set trafficStatus5 [::ixia::traffic_config         \
			-circuit_endpoint_type  ipv4            \
			-mode                   create          \
			-emulation_src_handle   $intf_h0        \
			-emulation_dst_handle   $intf_h1        \
			-l3_protocol            ipv4            \
			-qos_type_ixn           dscp            \
			-qos_value_ixn          {cs_precedence1  cs_precedence2} \
			-qos_value_ixn_mode     list            \
			-qos_value_ixn_tracking 1               \
			-track_by "flowGroup0 class_selector_phb" \
		       ]

if {[keylget trafficStatus5 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget trafficStatus5 log]"
}

set item [keylget trafficStatus5 traffic_item]

set trafficStatus [::ixia::traffic_control \
		       -action run \
		       -traffic_generator ixnetwork \
		      ]
if {[keylget trafficStatus status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget trafficStatus log]"
    return 0
}

after 5000


################################################################################
# Stop the traffic                                                             #
################################################################################
set traffic_status [::ixia::traffic_control \
			-action stop \
			-traffic_generator ixnetwork \
		       ]

if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

set flow_traffic_status [::ixia::traffic_stats \
			     -mode flow \
			     -traffic_generator ixnetwork \
			    ]
if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status log]"
    return 0
}

puts [KeylPrint flow_traffic_status]

################################################################################
# Wait for the traffic to stop                                                 #
################################################################################
after 30000

set flow_results [list                                                      \
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
    puts "\tFlow $flow: [keylget flow_traffic_status flow.$flow.flow_name]"
    foreach {name key} [subst $[subst flow_results]] {
        puts "\t\t$name: [keylget flow_traffic_status flow.$flow.$key]"
    }
}
