#!/opt/ActiveTcl-8.5/bin/tclsh

#                   ---------------------------
#                   |                         |
#                   |                         |
#   1.1.1.1---------|1.1.1.254       2.2.2.254|-------2.2.2.1 (non-ospf host)
#    ospf           |  ospf                   |
#                   |                         |
#                   ---------------------------
#   Advertising Route:
#     10.10.10.0
# 
#  Sending traffic from 10.10.10.0 to 2.2.2.1
#

package req Ixia
#source ~/MyIxiaWork/HLT/ixiaHltLib.tcl
#source ~/MyIxiaWork/Insieme_Saravana/pythonScripts/ixpy-0.0.9/ixpy/ixiaHltLib.tcl

set ixNetworkTclServerIp 10.219.117.103
set ixiaChassisIp 10.219.117.101
set portList "1/1 1/2"
set port1 1/1/1
set port2 1/1/2
set userName hgee

proc ConnectToIxia { connectParams {platform legacy} } {
    puts "ConnectToIxia: Please wait 40 seconds ..."
    set connectStatus [eval ::ixia::connect $connectParams]

    if {[keylget connectStatus status] != $::SUCCESS} {
	puts "\nEror ConnectToIxia: $connectStatus\n"
	return 1
    } else {
	return $connectStatus
    }
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

proc PortConfigProtocolInt { port portConfigParams } {
    upvar $portConfigParams params

    puts "\nPortConfigProtocolInt: $port"
    foreach {properties values} [array get params $port,*] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    set interfaceConfigStatus [eval ::ixia::interface_config $paramList]

    if {[keylget interfaceConfigStatus status] != $::SUCCESS} {
	puts "\nError PortConfigProtocolInt:\n$interfaceConfigStatus\n"
	return 1
    }

    # interface object = ::ixNet::OBJ-/vport:1/interface:1
    set interfaceHandle [keylget interfaceConfigStatus interface_handle]

    return $interfaceHandle
}

proc CreateTrafficItem { trafficItemParams } {
    upvar $trafficItemParams params

    # For non-full-mesh:        -src_dest_mesh one_to_one
    # For full-mesh:            -src_dest_mesh fully
    # For continuous traffic:   -transmit_mode continuous
    # For single burst traffic: -transmit single_burst -number_of_packets-per_stream 50000

    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "\nCreateTrafficItem"
    set trafficItemStatus [eval ::ixia::traffic_config $paramList]

    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError CreateTrafficItem: $trafficItemStatus\n"
	return 1
    }

    return $trafficItemStatus
}

proc StartAllProtocolsHlt { {platform legacy} } {
    # platform: legacy or ngpf

    if {$platform == "legacy"} {
	set params "::ixia::test_control -action start_all_protocols"
    } 

    if {$platform == "ngpf"} {
	set params "::ixiangpf::test_control -action start_all_protocols"
    } 

    puts "\nStartAllProtocolsHlt: $platform"
    set startProtocolStatus [eval $params]
    if {[keylget startProtocolStatus status] != $::SUCCESS} {
	puts "\nError StartAllProtocolsHlt:  $startProtocolStatus\n"
	return 1
    }

    return 0
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


proc SendArpOnProtocolInt { ports } {
    # This API will send ARP out of all the ports in -port_handle.
    # Only for Protocol Interface configuration.
    # Returns the Arp results.

    set arpStatus [::ixia::interface_config -mode modify -port_handle $ports -arp_send_req 1 -arp_req_retries 3]
    puts "\nSendArpOnProtocolInt: $arpStatus"

    return $arpStatus
}

set portConfig(1/1/1,-port_handle) $port1
set portConfig(1/1/1,-mode) config
set portConfig(1/1/1,-intf_ip_addr) 1.1.1.1
set portConfig(1/1/1,-intf_ip_addr_step) 0.0.0.1
set portConfig(1/1/1,-connected_count) 10 
set portConfig(1/1/1,-netmask) 255.255.255.0
set portConfig(1/1/1,-gateway) 1.1.1.11
set portConfig(1/1/1,-gateway_step) 0.0.0.1
set portConfig(1/1/1,-src_mac_addr) 00:01:01:01:00:01
set portConfig(1/1/1,-src_mac_addr_step) 0000.0000.0001
set portConfig(1/1/1,-vlan) 1
set portConfig(1/1/1,-vlan_id) 103
set portConfig(1/1/1,-vlan_id_step) 1
set portConfig(1/1/1,-vlan_id_count) 10
set portConfig(1/1/1,-arp_on_linkup) 1
set portConfig(1/1/1,-single_arp_per_gateway) 1
set portConfig(1/1/1,-single_ns_per_gateway) 1
set portConfig(1/1/1,-l23_config_type) protocol_interface

set portConfig(1/1/2,-port_handle) $port2
set portConfig(1/1/2,-mode) config
set portConfig(1/1/2,-intf_ip_addr) 1.1.1.11
set portConfig(1/1/2,-intf_ip_addr_step) 0.0.0.1
set portConfig(1/1/2,-connected_count) 10 
set portConfig(1/1/2,-netmask) 255.255.255.0
set portConfig(1/1/2,-gateway) 1.1.1.1
set portConfig(1/1/2,-gateway_step) 0.0.0.1
set portConfig(1/1/2,-src_mac_addr) 00:01:01:02:00:01
set portConfig(1/1/2,-src_mac_addr_step) 0000.0000.0001
set portConfig(1/1/2,-vlan) 1
set portConfig(1/1/2,-vlan_id) 103
set portConfig(1/1/2,-vlan_id_step) 1
set portConfig(1/1/2,-vlan_id_count) 10
set portConfig(1/1/2,-arp_on_linkup) 1
set portConfig(1/1/2,-single_arp_per_gateway) 1
set portConfig(1/1/2,-single_ns_per_gateway) 1
set portConfig(1/1/2,-l23_config_type) protocol_interface

# Uncomment this for generating a debug file only
#EnableHltDebug

puts "Rebooting ports $portList ..."
ConnectToIxia "-reset 1 -device $ixiaChassisIp -port_list $portList -ixnetwork_tcl_server $ixNetworkTclServerIp -tcl_server $ixiaChassisIp -username $userName"

foreach port $portList {
    set port 1/$port
    set endpoint($port) [PortConfigProtocolInt $port ::portConfig]
}

# These objects are used for Traffic Item endpoints
# endpoint(1/1/1) = ::ixNet::OBJ-/vport:1/interface:1
# endpoint(1/1/2) = ::ixNet::OBJ-/vport:2/interface:1

# Use this as src port handle in Traffic Item src endpoint
# OspfStatus = {handle ::ixNet::OBJ-/vport:1/protocols/ospf/router:1}
puts "\nConfiguring OSPF on $port1 ..."
set ospfStatus [::ixia::emulation_ospf_config  \
		    -mode create \
		    -port_handle $port1 \
		    -router_id 1.1.1.1 \
		    -graceful_restart_enable 0 \
		    -lsa_discard_mode 1 \
		    -session_type ospfv2 \
		    -area_id 0.0.0.0 \
		    -area_type external-capable \
		    -dead_interval 40 \
		    -hello_interval 10 \
		    -interface_cost 10 \
		    -authentication_mode null \
		    -mtu 1500 \
		    -neighbor_router_id 0.0.0.0 \
		    -network_type ptop \
		    -option_bits 2 \
		    -router_priority 2 \
		    -te_enable 0 \
		    -bfd_registration 0 \
		    -intf_ip_addr 1.1.1.1 \
		    -intf_prefix_length 24 \
		    -neighbor_intf_ip_addr 1.1.1.11 \
		    -vlan 1 \
		    -vlan_id 103 \
		    -vlan_user_priority 0 \
		    -mac_address_init 0000.edbd.787f \
		   ]

if {[keylget ospfStatus status] != $::SUCCESS} {
    puts "\nError: Ospf failed on $endpoint(1/1/1)"
}

set ospfPortHandle($port1,router1) [keylget ospfStatus handle]

# This is to create ospf route range/ospf advertisements
# ospfRouteRangeStatus = {elem_handle ::ixNet::OBJ-/vport:1/protocols/ospf/router:1/routeRange:1}
puts "\nConfiguring OSPF routes ..."
set ospfRouteRangeStatus [::ixia::emulation_ospf_topology_route_config  \
		  -mode create \
		  -handle $ospfPortHandle($port1,router1) \
		  -count 7 \
		  -summary_prefix_start 10.10.10.1 \
		  -summary_prefix_length 24 \
		  -summary_number_of_prefix 7 \
		  -type summary_routes \
		  -summary_route_type another_area \
		  -summary_prefix_metric 0 \
		 ]

if {[keylget ospfRouteRangeStatus status] != $::SUCCESS} {
    puts "\nError: Failed to configure ospf route range"
}

# Since the -count is 7, I get 7 routeRange under routeRange:1
# These are the src endpoints.
# ospfRouteRangeStatus: {elem_handle {::ixNet::OBJ-/vport:1/protocols/ospf/router:1/routeRange:1 ::ixNet::OBJ-/vport:1/protocols/ospf/router:1/routeRange:2 ::ixNet::OBJ-/vport:1/protocols/ospf/router:1/routeRange:3 ::ixNet::OBJ-/vport:1/protocols/ospf/router:1/routeRange:4 ::ixNet::OBJ-/vport:1/protocols/ospf/router:1/routeRange:5 ::ixNet::OBJ-/vport:1/protocols/ospf/router:1/routeRange:6 ::ixNet::OBJ-/vport:1/protocols/ospf/router:1/routeRange:7}} {status 1}

puts "\nospfRouteRangeStatus: $ospfRouteRangeStatus"


puts "\nConfiguring OSPF on $port2 ..."
set ospfStatus [::ixia::emulation_ospf_config  \
		    -mode create \
		    -port_handle $port2 \
		    -router_id 1.1.1.11 \
		    -graceful_restart_enable 0 \
		    -lsa_discard_mode 1 \
		    -session_type ospfv2 \
		    -area_id 0.0.0.0 \
		    -area_type external-capable \
		    -dead_interval 40 \
		    -hello_interval 10 \
		    -interface_cost 10 \
		    -authentication_mode null \
		    -mtu 1500 \
		    -neighbor_router_id 0.0.0.0 \
		    -network_type ptop \
		    -option_bits 2 \
		    -router_priority 2 \
		    -te_enable 0 \
		    -bfd_registration 0 \
		    -intf_ip_addr 1.1.1.11 \
		    -intf_prefix_length 24 \
		    -neighbor_intf_ip_addr 1.1.1.1 \
		    -vlan 1 \
		    -vlan_id 103 \
		    -vlan_user_priority 0 \
		    -mac_address_init 0000.edbd.787f \
		   ]

if {[keylget ospfStatus status] != $::SUCCESS} {
    puts "\nError: Ospf failed on $endpoint(1/1/2)"
}

set ospfPortHandle($port2,router1) [keylget ospfStatus handle]

# This is to create ospf route range/ospf advertisements
# ospfRouteRangeStatus = {elem_handle ::ixNet::OBJ-/vport:1/protocols/ospf/router:1/routeRange:1}
puts "\nConfiguring OSPF routes ..."
set ospfRouteRangeStatus [::ixia::emulation_ospf_topology_route_config  \
		  -mode create \
		  -handle $ospfPortHandle($port2,router1) \
		  -count 7 \
		  -summary_prefix_start 20.20.20.1 \
		  -summary_prefix_length 24 \
		  -summary_number_of_prefix 7 \
		  -type summary_routes \
		  -summary_route_type another_area \
		  -summary_prefix_metric 0 \
		 ]

if {[keylget ospfRouteRangeStatus status] != $::SUCCESS} {
    puts "\nError: Failed to configure ospf route range"
}

set trafficItem1(-mode) create
set trafficItem1(-name) Traffic_Item_1
set trafficItem1(-emulation_src_handle) [list $ospfPortHandle($port1,router1)]
set trafficItem1(-emulation_dst_handle) [list $endpoint($port2)]
set trafficItem1(-src_dest_mesh) one_to_one
set trafficItem1(-route_mesh) one_to_one
set trafficItem1(-bidirectional) 0
set trafficItem1(-circuit_endpoint_type) ipv4
set trafficItem1(-rate_percent) 100
set trafficItem1(-frame_size) 100
set trafficItem1(-transmit_mode) single_burst
set trafficItem1(-pkts_per_burst) 50000
set trafficItem1(-frame_rate_distribution_port) apply_to_all ;# split_evenly | apply_to_all
set trafficItem1(-frame_rate_distribution_stream) apply_to_all ;# split_evenly | apply_to_all
#set trafficItem1(-track_by) {trackingenabled0} ;# Use this if you are not tracking anyting
set trafficItem1(-ip_src_tracking) 1
set trafficItem1(-mac_src_tracking) 1

# -mac_dst_tracking 1
# I am excluding -mac_dst_tracking ingress tracking
# because I can only track four items.

set trafficItem1Objects [CreateTrafficItem ::trafficItem1]

StartAllProtocolsHlt

# ----->  At this point, you must verify on the DUT
#         for ospf neighbors and advertised routes
#         before starting traffic
# REMOVE THIS hardcoded timeout 
puts "\nWaiting for 45 seconds for ospf routes to converge on the DUT"
after 45000

puts "\nSending ARP on all ports ..."
# arpStatus: {1/1/1 {{arp_request_success 1}}} {1/1/2 {{arp_request_success 1}}} {status 1}
SendArpOnProtocolInt "$port1 $port2"
StartTrafficHlt

set flowStats [::ixia::traffic_stats \
		   -mode flow \
	      ]
if {[keylget flowStats status] != $::SUCCESS} {
    puts "Failed to get statistics"
    exit
}

puts \n[KeylPrint flowStats]\n
