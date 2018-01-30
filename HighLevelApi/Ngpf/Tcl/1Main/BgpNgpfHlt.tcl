#!/usr/bin/tclsh

package req Ixia
#source ~/MyIxiaWork/NGPF/HLT/ixiaHltLib.tcl
#source ~/Dropbox/MyIxiaWork/IxNet_tclApi.tcl

set chassisIp 10.219.116.72
set ixNetServerIp 192.168.70.127
set portList {1/1 1/2}
set port_list {1/1 1/2}
set userName hgee
set port1 1/1/1
set port2 1/1/2

proc connect { ixNetServerIp  chassisIp portList } {
    set result [::ixiangpf::connect  \
		 -reset 1 \
		 -device $chassisIp \
		 -port_list $portList \
		 -ixnetwork_tcl_server $ixNetServerIp \
		 -tcl_server $chassisIp \
		]
    if {[keylget result status] != $::SUCCESS} {
	puts "\nConnect Error: $result"
    }
}

proc create_topology {portList name} {
    set topology_1_status [::ixiangpf::topology_config \
        -topology_name      $name   \
        -port_handle        $portList     \
    ]
    if {[keylget topology_1_status status] != $::SUCCESS} {
        error $topology_1_status
    }
    return [keylget topology_1_status topology_handle]    
}
proc create_devicegroup {topology name} {
    set device_group_status [::ixiangpf::topology_config \
        -topology_handle              $topology            \
        -device_group_name            $name                \
        -device_group_multiplier      1                    \
        -device_group_enabled         1                    \
    ]
    if {[keylget device_group_status status] != $::SUCCESS} {
        puts "\nError: $device_group_status"
    }
    return [keylget device_group_status device_group_handle]    
}
proc create_ethernet {topology devicegroup name} {
    set mv_src_mac_addr_status [::ixiangpf::multivalue_config \
        -pattern                counter                 \
        -counter_start          00.11.01.00.00.01       \
        -counter_step           00.00.00.00.00.01       \
        -counter_direction      increment               \
        -nest_step              00.00.01.00.00.00       \
        -nest_owner             $topology               \
        -nest_enabled           1                       \
    ]
    if {[keylget mv_src_mac_addr_status status] != $::SUCCESS} {
        puts "\nError: $mv_src_mac_addr_status"
    }
    set mv_src_mac_addr [keylget mv_src_mac_addr_status multivalue_handle]

    set ethernet_status [::ixiangpf::interface_config \
        -protocol_name                $name                      \
        -protocol_handle              $devicegroup               \
        -mtu                          1500                       \
        -src_mac_addr                 $mv_src_mac_addr           \
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
    if {[keylget ethernet_status status] != $::SUCCESS} {
        puts "\nError: $ethernet_status"
    }
    return [keylget ethernet_status ethernet_handle]
}
proc create_ipv4 {topology ethernet name ip_address gw_address} {
    set mv_intf_ip_addr_status [::ixiangpf::multivalue_config \
        -pattern                counter         \
        -counter_start          $ip_address     \
        -counter_step           0.0.1.0         \
        -counter_direction      increment       \
        -nest_step              0.1.0.0         \
        -nest_owner             $topology       \
        -nest_enabled           1               \
    ]
    if {[keylget mv_intf_ip_addr_status status] != $::SUCCESS} {
        puts "\nError: $mv_intf_ip_addr_status"
    }
    set mv_intf_ip_addr [keylget mv_intf_ip_addr_status multivalue_handle]

    set mv_gateway_status [::ixiangpf::multivalue_config \
        -pattern                counter         \
        -counter_start          $gw_address     \
        -counter_step           0.0.1.0         \
        -counter_direction      increment       \
        -nest_step              0.0.0.1         \
        -nest_owner             $topology       \
        -nest_enabled           0               \
    ]
    if {[keylget mv_gateway_status status] != $::SUCCESS} {
        puts "\nError: $mv_gateway_status"
    }
    set mv_gateway [keylget mv_gateway_status multivalue_handle]

    set ipv4_status [::ixiangpf::interface_config \
        -protocol_name                $name                 \
        -protocol_handle              $ethernet             \
        -ipv4_resolve_gateway         1                     \
        -ipv4_manual_gateway_mac      00.00.00.00.00.01     \
        -gateway                      $mv_gateway           \
        -intf_ip_addr                 $mv_intf_ip_addr      \
        -netmask                      255.255.255.0         \
    ]
    if {[keylget ipv4_status status] != $::SUCCESS} {
        puts "\nError: $ipv4_status"
    }
    return [keylget ipv4_status ipv4_handle]
}
proc create_bgp {topology ipv4 remote_ip local_ip} {
    set mv_remote_ip_addr_status [::ixiangpf::multivalue_config \
        -pattern                counter         \
        -counter_start          $remote_ip      \
        -counter_step           0.0.0.0         \
        -counter_direction      decrement       \
        -nest_step              0.0.0.1         \
        -nest_owner             $topology       \
        -nest_enabled           0               \
    ]
    puts "\ncreate_bgp: $mv_remote_ip_addr_status"

    if {[keylget mv_remote_ip_addr_status status] != $::SUCCESS} {
        puts "\nError: $mv_remote_ip_addr_status"
    }

    set mv_remote_ip_addr [keylget mv_remote_ip_addr_status multivalue_handle]
    puts "\nremoteIpAddr: $mv_remote_ip_addr"

    set mv_local_router_id_status [::ixiangpf::multivalue_config \
        -pattern                counter         \
        -counter_start          $local_ip       \
        -counter_step           0.0.1.0         \
        -counter_direction      increment       \
        -nest_step              0.1.0.0         \
        -nest_owner             $topology       \
        -nest_enabled           1               \
    ]
    if {[keylget mv_local_router_id_status status] != $::SUCCESS} {
        puts "\nError: $mv_local_router_id_status"
    }
    set mv_local_router_id [keylget mv_local_router_id_status multivalue_handle]

    set bgp_ipv4_peer_1_status [::ixiangpf::emulation_bgp_config \
        -mode                                    enable                    \
        -md5_enable                              0                         \
        -handle                                  $ipv4                     \
        -remote_ip_addr                          $mv_remote_ip_addr        \
        -enable_4_byte_as                        0                         \
        -local_as                                0                         \
        -update_interval                         0                         \
        -count                                   1                         \
        -local_router_id                         $mv_local_router_id       \
        -hold_time                               90                        \
        -neighbor_type                           internal                  \
        -graceful_restart_enable                 0                         \
        -restart_time                            45                        \
        -stale_time                              0                         \
        -tcp_window_size                         8192                      \
        -local_router_id_enable                  1                         \
        -ttl_value                               64                        \
        -updates_per_iteration                   1                         \
        -bfd_registration                        0                         \
        -bfd_registration_mode                   multi_hop                 \
        -act_as_restarted                        0                         \
        -discard_ixia_generated_routes           0                         \
        -flap_down_time                          0                         \
        -local_router_id_type                    same                      \
        -enable_flap                             0                         \
        -send_ixia_signature_with_routes         0                         \
        -flap_up_time                            0                         \
        -advertise_end_of_rib                    0                         \
        -configure_keepalive_timer               0                         \
        -keepalive_timer                         30                        \
    ]
    if {[keylget bgp_ipv4_peer_1_status status] != $::SUCCESS} {
        puts "\nError: $bgp_ipv4_peer_1_status"
    }
    puts "\nbgp_ipv4_peer status: $bgp_ipv4_peer_1_status"

    # bgp_ipv4_peer status: {status 1} {bgp_handle /topology:1/deviceGroup:1/ethernet:1/ipv4:1/bgpIpv4Peer:1}
    return [list [keylget bgp_ipv4_peer_1_status bgp_handle]]
}

proc create_bgp_ipv4_routes {topology devicegroup bgp_peer starting_address} {
    set mv_prefix_status [::ixiangpf::multivalue_config \
        -pattern                counter                     \
        -counter_start          $starting_address           \
        -counter_step           255.255.255.255             \
        -counter_direction      decrement                   \
        -nest_step              0.0.0.1,0.0.0.1             \
        -nest_owner             $devicegroup,$topology      \
        -nest_enabled           0,0                         \
    ]
    if {[keylget mv_prefix_status status] != $::SUCCESS} {
        puts "\nError: $mv_prefix_status"
    }
    set mv_prefix [keylget mv_prefix_status multivalue_handle]

    set mv_ext_communities_assigned_two_bytes_status [::ixiangpf::multivalue_config \
        -pattern                counter                     \
        -counter_start          1                           \
        -counter_step           1                           \
        -counter_direction      increment                   \
        -nest_step              1,0                         \
        -nest_owner             $devicegroup,$topology      \
        -nest_enabled           0,1                         \
    ]
    if {[keylget mv_ext_communities_assigned_two_bytes_status status] != $::SUCCESS} {
        puts "\nError: $mv_ext_communities_assigned_two_bytes_status"
    }
    set mv_ext_communities_assigned_two_bytes [keylget mv_ext_communities_assigned_two_bytes_status multivalue_handle]

    set mv_ext_communities_assigned_four_bytes_status [::ixiangpf::multivalue_config \
        -pattern                counter                     \
        -counter_start          1                           \
        -counter_step           1                           \
        -counter_direction      increment                   \
        -nest_step              1,0                         \
        -nest_owner             $devicegroup,$topology      \
        -nest_enabled           0,1                         \
    ]
    if {[keylget mv_ext_communities_assigned_four_bytes_status status] != $::SUCCESS} {
        puts "\nError: $mv_ext_communities_assigned_four_bytes_status"
    }
    set mv_ext_communities_assigned_four_bytes [keylget mv_ext_communities_assigned_four_bytes_status multivalue_handle]

    set network_group_status [::ixiangpf::emulation_bgp_route_config \
        -handle                                   $bgp_peer                                 \
        -mode                                     add                                       \
        -active                                   1                                         \
        -ipv4_unicast_nlri                        1                                         \
        -max_route_ranges                         5                                         \
        -ip_version                               4                                         \
        -prefix                                   $mv_prefix                                \
        -num_routes                               1                                         \
        -prefix_from                              24                                        \
        -advertise_nexthop_as_v4                  0                                         \
        -aggregator_as                            0                                         \
        -aggregator_id                            0.0.0.0                                   \
        -aggregator_id_mode                       increment                                 \
        -as_path_set_mode                         include_as_seq                            \
        -flap_delay                               0                                         \
        -flap_down_time                           0                                         \
        -enable_aggregator                        0                                         \
        -enable_as_path                           1                                         \
        -atomic_aggregate                         0                                         \
        -cluster_list_enable                      0                                         \
        -communities_enable                       1                                         \
        -ext_communities_enable                   1                                         \
        -enable_route_flap                        0                                         \
        -enable_local_pref                        1                                         \
        -enable_med                               0                                         \
        -next_hop_enable                          1                                         \
        -origin_route_enable                      1                                         \
        -originator_id_enable                     0                                         \
        -partial_route_flap_from_route_index      0                                         \
        -partial_route_flap_to_route_index        0                                         \
        -next_hop_ipv4                            0.0.0.0                                   \
        -next_hop_ipv6                            0:0:0:0:0:0:0:0                           \
        -local_pref                               0                                         \
        -multi_exit_disc                          0                                         \
        -next_hop_mode                            fixed                                     \
        -next_hop_ip_version                      4                                         \
        -next_hop_set_mode                        same                                      \
        -origin                                   igp                                       \
        -originator_id                            0.0.0.0                                   \
        -packing_from                             0                                         \
        -packing_to                               0                                         \
        -enable_partial_route_flap                0                                         \
        -flap_up_time                             0                                         \
        -enable_traditional_nlri                  1                                         \
        -communities_as_number                    0                                         \
        -communities_last_two_octets              0                                         \
        -ext_communities_as_two_bytes             1                                         \
        -ext_communities_as_four_bytes            1                                         \
        -ext_communities_assigned_two_bytes       $mv_ext_communities_assigned_two_bytes    \
        -ext_communities_assigned_four_bytes      $mv_ext_communities_assigned_four_bytes   \
        -ext_communities_ip                       1.1.1.1                                   \
        -ext_communities_opaque_data              0                                         \
        -as_path_segment_numbers                  [list [list 1]]                           \
    ]
    if {[keylget network_group_status status] != $::SUCCESS} {
        puts "\nError: $network_group_status"
    }
}

proc VerifyProtocolSessionStatusUpNgpfHlt { protocolHandle {totalTime 60}} {
    # protocolHandle: Ethernet handle, IPv4 handle, OSPF handle, etc
    #    IPv4 handle sample: /topology:1/deviceGroup:1/ethernet:1/ipv4:1
    #    OSPF handle sample: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1
   
    for {set timer 1} {$timer <= $totalTime} {incr timer} {
	set sessionStatus [ixiangpf::protocol_info \
			              -handle $protocolHandle \
			              -mode "aggregate" \
			       ]
	set currentSessionUp [keylget sessionStatus $protocolHandle.aggregate.sessions_up]
	set totalSessions    [keylget sessionStatus $protocolHandle.aggregate.sessions_total]
	
	puts "\n$protocolHandle"
	puts "\t$timer/$totalTime\secs: CurrentSessionUp:$currentSessionUp   TotalSessions:$totalSessions"
	
	if {$timer < $totalTime && $currentSessionUp != $totalSessions} {
	        after 1000
	        continue
	}
	if {$timer < $totalTime && $currentSessionUp == $totalSessions} {
	        return 0
	}
	if {$timer == $totalTime && $currentSessionUp != $totalSessions} {
	        puts "\nError: It has been $timer seconds and total sessions are not all UP"
	        return 1
	}
    }
}

proc CreateTrafficItemHlt { trafficItemParams } {
    upvar $trafficItemParams params

    # For non-full-mesh:        -src_dest_mesh one_to_one
    # For full-mesh:            -src_dest_mesh fully
    # For continuous traffic:   -transmit_mode continuous
    # For single burst traffic: -transmit single_burst -number_of_packets-per_stream 50000

    # How to use this from a script:
    #     set trafficItem1(-mode) create 
    #     set trafficItem1(-endpointset_count) 1
    #     set trafficItem1(-emulation_src_handle) $topology1(portHandle)
    #     set trafficItem1(-emulation_dst_handle) $topology2(portHandle)
    #     set trafficItem1(-src_dest_mesh) one_to_one
    #     set trafficItem1(-route_mesh) one_to_one
    #     set trafficItem1(-bidirectional) 0
    #     set trafficItem1(-allow_self_destined) 0
    #     set trafficItem1(-name) Traffic_Item_1
    #     set trafficItem1(-circuit_endpoint_type) ipv4
    #     set trafficItem1(-track_by) {trackingenabled0 sourceDestValuePair0}
    #     set trafficItem1(-l3_protocol) ipv4
    #
    #     set trafficItem1Objects [CreateTrafficItemHlt ::trafficItem1]

    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "\nCreateTrafficItemHlt: $paramList\n"
    set trafficItemStatus [eval ::ixia::traffic_config $paramList]

    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError CreateTrafficItem: $trafficItemStatus\n"
	return 1
    }

    return $trafficItemStatus
}

proc StartTrafficHlt {} {
    puts "\nStartTrafficHlt ..."
    set startTrafficStatus [::ixia::traffic_control \
				-action run \
			       ]
    if {[keylget startTrafficStatus status] != $::SUCCESS} {
	puts "\nError StartTrafficHlt: $startTrafficStatus\n"
	return 1
    } 

    # By including VerifyTrafficState, it will wait up to 15 seconds until
    # traffic is started before returning.
    VerifyTrafficState
    return 0
}

proc StopTrafficHlt {} {
    puts "\nStopTrafficHlt ..."
    set stopTrafficStatus [::ixia::traffic_control \
			       -action stop \
			      ]
    if {[keylget stopTrafficStatus status] != $::SUCCESS} {
	puts "\nError StopTrafficHlt: $stopTrafficStatus\n"
	return 1
    } 
    after 5000
    return 0
}

proc CheckTrafficState {} {
    # This API is mainly used by VerifyTrafficState.
    # Users can also use this in their scripts to check traffic state.

    # startedWaitingForStats, startedWaitingForStreams, started, stopped, stoppedWaitingForStats, txStopWatchExpected, locked, unapplied

    set currentTrafficState [ixNet getAttribute [ixNet getRoot]/traffic -state]

    switch -exact -- $currentTrafficState {
	::ixNet::OK {
	    return notRunning
	}
	stopped {
	    return stopped
	}
	started {
	    return started
	}
	locked {
	    return locked
	}
	unapplied {
	    return unapplied
	}
	startedWaitingForStreams {
	    return startedWaitingForStreams
	}
	startedWaitingForStats {
	    return startedWaitingForStats
	}
	stoppedWaitingForStats {
	    return stoppedWaitingForStats
	}
	default {
	    return $currentTrafficState
	    puts "\nError CheckTrafficState: Traffic state is currently: $currentTrafficState\n"
	    return 1
	}
    }
}

proc VerifyTrafficState {} {
    set startCounter 1
    set stopCounter 15
    for {set start $startCounter} {$start <= $stopCounter} {incr start} {
	set trafficState [CheckTrafficState]

	# Basically, if traffic state is unapplied or lock, then failed.
	if {$start == $stopCounter} {
	    if {$trafficState != "started" || $trafficState != "startedWaitingForStats" \
		    || $trafficState != "stoppedWaitingForStats" || $trafficState != "stopped"} {
		puts "VerifyTrafficState Error: Traffic failed to start"
		return 1
	    }
	}
	
	if {$trafficState == "started"} {
	    puts "VerifyTrafficState: Traffic Started"
	    break
	}

	if {$trafficState == "stopped"} {
	    puts "VerifyTrafficState: Traffic stopped"
	    break
	}

	if {$trafficState == "startedWaitingForStats" || $trafficState == "stoppedWaitingForStats"} {
	    puts "VerifyTrafficState: Traffic started. Waiting for stats to complete"
	    break
	}

	if {$start < $stopCounter} {
	    if {$trafficState != "started" || $trafficState != "startedWaitingForStats" \
		    || $trafficState != "stoppedWaitingForStats" || $trafficStats != "stopped"} {
		puts "VerifyTrafficState: Current state = $trafficState. Waiting $start/$stopCounter ..."
		after 1000
	    }
	}
    }
}

proc GetStats {{viewName "Flow Statistics"}} {
    # viewName options (Not case sensitive):
    #    NOTE: Not all statistics are listed here.
    #          You could get the statistic viewName directly from the IxNetwork GUI in the statistics.
    #
    #    'Port Statistics'
    #    'Tx-Rx Frame Rate Statistics'
    #    'Port CPU Statistics'
    #    'Global Protocol Statistics'
    #    'Protocols Summary'
    #    'Port Summary'
    #    'OSPFv2-RTR Drill Down'
    #    'OSPFv2-RTR Per Port'
    #    'IPv4 Drill Down'
    #    'L2-L3 Test Summary Statistics'
    #    'Flow Statistics'
    #    'Traffic Item Statistics'
    #    'IGMP Host Drill Down'
    #    'IGMP Host Per Port'
    #    'IPv6 Drill Down'
    #    'MLD Host Drill Down'
    #    'MLD Host Per Port'
    #    'PIMv6 IF Drill Down'
    #    'PIMv6 IF Per Port'

    set root [ixNet getRoot]
    set viewList [ixNet getList $root/statistics view]    
    set statViewIndex [lsearch -nocase -regexp $viewList $viewName]
    set view [lindex $viewList $statViewIndex]
    puts "\nview: $view"
    # Flow Statistics
    set caption [ixNet getAttribute $view -caption]

    ixNet setAttribute $view -enabled true
    ixNet commit

    set columnList [ixNet getAttribute ${view}/page -columnCaptions]
    puts "\n$columnList\n"
    
    set startTime 1
    set stopTime 30
    while {$startTime < $stopTime} {
	set totalPages [ixNet getAttribute $view/page -totalPages]
	if {[regexp -nocase "null" $totalPages]} {
	        puts "\nGetStatView: Getting total pages for $view is not ready. $startTime/$stopTime"
	        after 2000
	} else {
	        break
	}
    }
    puts "\ntotal Pages: $totalPages"

    # Iterrate through each page 
    set row 0
    for {set currentPage 1} {$currentPage <= $totalPages} {incr currentPage} {
	puts "\nGetStatView: Getting statistics on page: $currentPage/$totalPages. Please wait ..."

	catch {ixNet setAttribute $view/page -currentPage $currentPage} errMsg
	if {$errMsg != "::ixNet::OK"} {
	        puts "\nGetStatView: Failed to get statistic for current page.\n"
	        return 1
	}
	ixNet commit
	
	# Wait for statistics to populate on current page
	set whileLoopStopCounter 0
	while {[ixNet getAttribute $view/page -isReady] != "true"} {
	    if {$whileLoopStopCounter == "5"} {
		puts "\nGetStatView: Could not get stats"
		return 1
	    }
	    if {$whileLoopStopCounter < 5} {
		puts "\nGetStatView: Not ready yet.  Waiting $whileLoopStopCounter/5 seconds ..."
		after 1000
	    }
	        incr whileLoopStopCounter
	}
	
	set pageList [ixNet getAttribute $view/page -rowValues] ;# first list of all rows in the page
	set totalFlowStatistics [llength $pageList]

	# totalPageList == The total amount of flow statistics
	for {set pageListIndex 0} {$pageListIndex <= $totalFlowStatistics} {incr pageListIndex} {
	    set rowList [lindex $pageList $pageListIndex] ;# second list of 1 ingress and x egress rows

	    for {set rowIndex 0} {$rowIndex < [llength $rowList]} {incr rowIndex} {
		# Increment the row number
		incr row

		# cellList: 1/1/1 1/1/2 TI0-Flow_1 1.1.1.1-1.1.2.1 4000 4000 0 0 0 0 256000 0 0 0 0 0 0 0 0 0 0 0 00:00:00.684 00:00:00.700
		set cellList [lindex $rowList $rowIndex] ;# third list of cell values
		
		#puts "\n--- cellList $pageListIndex: $cellList ---\n"
		puts "  $row:"
		for {set index 0} {$index <[llength $cellList]} {incr index} {
		    keylset getStats flow.$row.[join [lindex $columnList $index] _] [lindex $cellList $index] 
		    puts "\t[lindex $columnList $index]: [lindex $cellList $index]"
		}
	    }
	}
    }  
    ixNet setAttribute $view -enabled false
    ixNet commit

    return $getStats
}

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

connect $ixNetServerIp $chassisIp $portList

set topology_1_handle [create_topology $port1 "BGP Topo1"]

set deviceGroup_1_handle [create_devicegroup $topology_1_handle "BGP DG1"]

set ethernet_1_handle [create_ethernet $topology_1_handle $deviceGroup_1_handle {Ethernet 1}]

set ipv4_1_handle [create_ipv4 \
    $topology_1_handle $ethernet_1_handle   \
    {IPv4 1}                                \
    100.1.0.1                               \
    100.1.0.2                               \
]

set bgpIpv4Peer_1_list [create_bgp          \
    $topology_1_handle $ipv4_1_handle       \
    100.1.0.2                               \
    100.1.0.1                               \
]
set bgpIpv4Peer_1_handle [lindex $bgpIpv4Peer_1_list 0]

create_bgp_ipv4_routes $topology_1_handle $deviceGroup_1_handle $bgpIpv4Peer_1_handle 0.1.0.0

set topology_2_handle [create_topology $port2 "BGP Topo2"]

set deviceGroup_2_handle [create_devicegroup $topology_2_handle "BGP DG2"]

set ethernet_2_handle [create_ethernet $topology_2_handle $deviceGroup_2_handle {Ethernet 2}]

set ipv4_2_handle [create_ipv4 \
    $topology_2_handle $ethernet_2_handle   \
    {IPv4 2}                                \
    100.1.0.2                               \
    100.1.0.1                               \
]

set bgpIpv4Peer_2_list [create_bgp          \
    $topology_2_handle $ipv4_2_handle       \
    100.1.0.1                               \
    100.1.0.2                               \
]
set bgpIpv4Peer_2_handle [lindex $bgpIpv4Peer_2_list 0]

create_bgp_ipv4_routes $topology_2_handle $deviceGroup_2_handle $bgpIpv4Peer_2_handle 0.100.0.0

set ret [::ixiangpf::test_control -action start_all_protocols]
if {[keylget ret status] != $::SUCCESS} {
    puts "\nError: $ret"
}

# Verify ARP
set port1ArpStatus [::ixiangpf::interface_config -port_handle $port1 -arp_send_req 1 -arp_req_retries 3]
set port2ArpStatus [::ixiangpf::interface_config -port_handle $port2 -arp_send_req 1 -arp_req_retries 3]

puts "\nport1ArpStatus: $port1ArpStatus"
if {[keylget port1ArpStatus status] != 1} {
    puts "\n$port1 ARP failed"
    exit
}

puts "\nport2ArpStatus: $port2ArpStatus"
if {[keylget port2ArpStatus status] != 1} {
    puts "\n$port2 ARP failed"
    exit
}

if {[VerifyProtocolSessionStatusUpNgpfHlt $bgpIpv4Peer_1_handle] == 1} {
    exit
}

set trafficItem1(-mode) create 
set trafficItem1(-name) Traffic_Item_1
set trafficItem1(-endpointset_count) 1
set trafficItem1(-emulation_src_handle) $topology_1_handle
set trafficItem1(-emulation_dst_handle) $topology_2_handle
set trafficItem1(-src_dest_mesh) one_to_one
set trafficItem1(-route_mesh) one_to_one
set trafficItem1(-bidirectional) 0
set trafficItem1(-rate_percent) 10
set trafficItem1(-pkts_per_burst) 10000
set trafficItem1(-transmit_mode) continuous
set trafficItem1(-frame_size) 100
set trafficItem1(-allow_self_destined) 0
set trafficItem1(-circuit_endpoint_type) ipv4 ;# To send only L2 traffic, use ethernet_vlan
set trafficItem1(-track_by) {trackingenabled0 sourceDestValuePair0}
set trafficItem1(-l3_protocol) ipv4

set trafficItemObj [CreateTrafficItemHlt trafficItem1]

StartTrafficHlt
set stats [GetStats]
puts "[KeylPrint stats]"
puts "\n--- [keylget stats flow.1.Tx_Frames] ---"


