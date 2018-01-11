#!/usr/bin/tclsh

package req Ixia

set ixiaChassisIp 10.219.117.101
set ixNetworkTclServerIp 10.219.117.103
set portList "1/1 1/2"
set port1 1/1/1
set port2 1/1/2
set userName hgee

proc ConnectToIxiaNgpf { connectParams } {
    puts "Resetting Ixia ports. Please wait 40 seconds ..."
    set connectStatus [eval ::ixiangpf::connect $connectParams]

    if {[keylget connectStatus status] != $::SUCCESS} {
	puts "ConnectToIxiaNgpf failed: $connectStatus\n"
	return 1
    } else {
	return $connectStatus
    }
}

proc CreateNewTopologyNgpf { topologyParams } {
    upvar $topologyParams params

    puts "\nCreateNewTopologyNgpf ..."
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "\nCreateNewTopology paramList: $paramList"

    set topologyStatus [eval ::ixiangpf::topology_config $paramList]

    if {[keylget topologyStatus status] != $::SUCCESS} {
	puts "\nError CreateNewTopologyNgpf: $topologyStatus"
	return 1
    }
    
    return $topologyStatus
}

proc CreateNewTopoDeviceGroupNgpf { deviceGroupParams } { 
    upvar $deviceGroupParams params

    puts "\nCreateNewTopoDeviceGroupNgpf"
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	
	# Using regexp to parse out $property with a dash because only dashes 
	# in front of a parameter is a hlt parameter.
	if {[regexp -- "-" $property]} {
	    append paramList "$property $values "
	}
    }
    
    set topoDeviceGroupStatus [eval ::ixiangpf::topology_config $paramList]

    if {[keylget topoDeviceGroupStatus status] != $::SUCCESS} {
	puts "\nError CreateNewTopoDeviceGroupNgpf: $topoDeviceGroupStatus"
	return 1
    } 

    return $topoDeviceGroupStatus
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

proc PortConfigProtocolIntNgpf { portConfigParams } {
    upvar $portConfigParams params

    puts "\nPortConfigProtocolIntNgpf ..."
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    set interfaceConfigStatus [eval ::ixiangpf::interface_config $paramList]
    
    if {[keylget interfaceConfigStatus status] != $::SUCCESS} {
	puts "\nPortConfigProtocolIntNgpf error:\n$interfaceConfigStatus\n"
	return 1
    }

    # keylget interfaceConfigStatus:
    #    ethernet_handle: /topology:2/deviceGroup:2/ethernet:1
    #    ipv4_handle: /topology:2/deviceGroup:2/ethernet:1/ipv4:1
    #    interface_handle: /topology:2/deviceGroup:2/ethernet:1/ipv4:1/item:1
    # interface object = ::ixNet::OBJ-/vport:1/interface:1

    return $interfaceConfigStatus
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

    puts "\nCreateTrafficItem: $paramList\n"
    set trafficItemStatus [eval ::ixia::traffic_config $paramList]

    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError CreateTrafficItem: $trafficItemStatus\n"
	return 1
    }

    return $trafficItemStatus
}

proc StartAllProtocolsHlt {} {
    puts "\nStartAllProtocolsHlt"
    set startProtocolStatus [::ixiangpf::test_control -action start_all_protocols]
    if {[keylget startProtocolStatus status] != $::SUCCESS} {
	puts "\nStartAllProtocolsHlt error:  $startProtocolStatus\n"
	return 1
    }

    return 0
}

proc RegenerateTrafficItems { {trafficItemList all} } {
    # trafficItemList == one or more traffic item names in a list
    #                    DEFAULT is all

    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set trafficItemName [ixNet getAttribute $trafficItem -name]

	if {$trafficItemList != "all" && [lsearch $trafficItemList $trafficItemName] != -1} {
	    puts "\nRegenerateTrafficitem: $trafficItemName"
	    catch {ixNet exec generate $trafficItem} errMsg
	}
	if {$trafficItemList == "all"} {
	    puts "\nRegenerateTrafficItem: $trafficItemName"
	    catch {ixNet exec generate $trafficItem} errMsg
	}
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError RegenerateTrafficItem failed on $trafficItem : $errMsg\n"
	    return 1
	}
    }
    after 3000
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

proc StartTrafficHlt {} {
    puts "\nStartTrafficHlt ..."
    set startTrafficStatus [::ixiangpf::traffic_control \
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

proc GetStatsHlt {} {
    puts "\nGetStatsHlt ..."
    set flowStats [::ixia::traffic_stats \
		       -mode flow
		  ]
    if {[keylget flowStats status] != $::SUCCESS} {
	puts "\nGetStatsHlt: Failed to get statistics"
	exit
    }
    return $flowStats
}

#EnableHltDebug

set connectStatus [ConnectToIxiaNgpf "-reset -device $ixiaChassisIp -port_list $portList -ixnetwork_tcl_server $ixNetworkTclServerIp -tcl_server $ixiaChassisIp -username $userName"]
if {$connectStatus == 1} {
    exit
}

#set connectStatus [ConnectToIxiaNgpf "-ixnetwork_tcl_server $ixNetworkTclServerIp -tcl_server $ixiaChassisIp -username $userName -session_resume_keys 0"]

puts $connectStatus

# 1> Create new Topology Group
set topology1(-topology_name)  "IPv4 Topology Tx-1"
set topology1(-port_handle) [list [list $port1]]

set topology2(-topology_name)  "IPv4 Topology Rx-1"
set topology2(-port_handle) [list [list $port2]]

set topology1Status [CreateNewTopologyNgpf ::topology1]
set topology2Status [CreateNewTopologyNgpf ::topology2]

#puts [KeylPrint topology1Status]
#puts [KeylPrint topology2Status]

# /topology:1
# /topology:2

set topology1(portHandle) [keylget topology1Status topology_handle]
set topology2(portHandle) [keylget topology2Status topology_handle]

# 2> Create Device Group(s) to a Topology Group
#    
set deviceGroup1(topo1,-topology_handle) $topology1(portHandle)
set deviceGroup1(topo1,-device_group_multiplier) 10
set deviceGroup1(topo1,-device_group_name) "Ipv4 Tx-1"
set deviceGroup1(topo1,-device_group_enabled) 1
set deviceGroup1(topo1,protocolName) "Ethernet"

set deviceGroup2(topo2,-topology_handle) $topology2(portHandle)
set deviceGroup2(topo2,-device_group_multiplier) 10
set deviceGroup2(topo2,-device_group_name) "Ipv4 Rx-1"
set deviceGroup2(topo2,-device_group_enabled) 1
set deviceGroup2(topo2,protocolName) "Ethernet"

set topo1DeviceGroup1 [CreateNewTopoDeviceGroupNgpf ::deviceGroup1]
set topo2DeviceGroup2 [CreateNewTopoDeviceGroupNgpf ::deviceGroup2]

set deviceGroup1(topo1,groupHandle) [keylget topo1DeviceGroup1 device_group_handle]
set deviceGroup2(topo2,groupHandle) [keylget topo2DeviceGroup2 device_group_handle]

#puts "\ndeviceGroup1Handles: $deviceGroup1(topo1,groupHandle)"
#puts "\ndeviceGroup2Handles: $deviceGroup2(topo2,groupHandle)"
# /topology:1/deviceGroup:1
# /topology:2/deviceGroup:1

set portconfig1(-mode)                    config
set portConfig1(-mtu)                     1500
# set portConfig($port2,-port_handle)            1/1/3 ;# Use -port_handle if you want to create a custom list
set portConfig1(-protocol_handle)         $deviceGroup1(topo1,groupHandle)
set portConfig1(-ipv4_resolve_gateway)    1
set portConfig1(-ipv4_manual_gateway_mac) 00.00.00.00.00.01
set portConfig1(-gateway)                 1.1.10.1
set portConfig1(-gateway_step)            0.0.0.0
set portConfig1(-intf_ip_addr)            1.1.1.1
set portConfig1(-intf_ip_addr_step)       0.0.0.1
set portConfig1(-netmask)                 255.255.0.0
set portConfig1(-src_mac_addr)            00:01:01:01:00:01
set portConfig1(-src_mac_addr_step)       00:00:00:00:00:01
set portConfig1(-vlan)                    0 ;# To enable vlan, use 1
set portConfig1(-vlan_id)                 100
set portConfig1(-vlan_user_priority)      3
set portConfig1(-vlan_id_count)           5
set portConfig1(-vlan_id_step)            1
set portConfig1(-vlan_user_priority_step) 0

set portConfig2(-mode)                    config
set portConfig2(-mtu)                     1500 
# set portConfig(-port_handle)            1/1/4 ;# Use -port_handle if you want to create a custom list
set portConfig2(-protocol_handle)         $deviceGroup2(topo2,groupHandle)
set portConfig2(-ipv4_resolve_gateway)    1
set portConfig2(-ipv4_manual_gateway_mac) 00.00.00.00.00.01
set portConfig2(-gateway)                 1.1.1.1
set portConfig2(-gateway_step)            0.0.0.0
set portConfig2(-intf_ip_addr)            1.1.10.1
set portConfig2(-intf_ip_addr_step)       0.0.0.1
set portConfig2(-netmask)                 255.255.0.0
set portConfig2(-src_mac_addr)            00:01:01:02:00:01
set portConfig2(-src_mac_addr_step)       00:00:00:00:00:01
set portConfig2(-vlan)                    0 ;# To enable vlan, use 1
set portConfig2(-vlan_id)                 100
set portConfig2(-vlan_user_priority)      3
set portConfig2(-vlan_id_count)           5
set portConfig2(-vlan_id_step)            1
set portConfig2(-vlan_user_priority_step) 0

set deviceGroup1Topo1 [PortConfigProtocolIntNgpf ::portConfig1]
set deviceGroup2Topo1 [PortConfigProtocolIntNgpf ::portConfig2]

if 0 {
foreach port $portList {
    set port 1/$port
    # endpoint(1/1/3) = /topology:1/deviceGroup:2/ethernet:1/ipv4:1/item:1
    # endpoint(1/1/4) = /topology:2/deviceGroup:2/ethernet:1/ipv4:1/item:1
    set endpoint($port) [PortConfigProtocolIntNgpf $port ::portConfig]
}
}

#parray endpoint

# /topology:1/deviceGroup:1/ethernet:1/ipv4:1
#set topo1DeviceGroup1Ipv4Handle [keylget interfaceConfig1Status interface_handle]
#puts \n$topo1DeviceGroup1Ipv4Handle

#set topo2DeviceGroup2Ipv4Handle [keylget interfaceConfig2Status interface_handle]
#puts \n$topo2DeviceGroup2Ipv4Handle

# /topology:2/deviceGroup:1/ethernet:1/ipv4:1

# status: 1
# ethernet_handle: /topology:1/deviceGroup:1/ethernet:1
# ipv4_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1
# interface_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:1 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:2 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:3 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:4 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:5 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:6 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:7 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:8 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:9 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:10

set trafficItem1(-mode) create 
set trafficItem1(-endpointset_count) 1
set trafficItem1(-emulation_src_handle) $topology1(portHandle)
set trafficItem1(-emulation_dst_handle) $topology2(portHandle)
set trafficItem1(-src_dest_mesh) one_to_one
set trafficItem1(-route_mesh) one_to_one
set trafficItem1(-bidirectional) 0
set trafficItem1(-allow_self_destined) 0
set trafficItem1(-name) Traffic_Item_1
set trafficItem1(-circuit_endpoint_type) ipv4 ;# To send only L2 traffic, use ethernet_vlan
set trafficItem1(-track_by) {trackingenabled0 sourceDestValuePair0}
set trafficItem1(-l3_protocol) ipv4

StartAllProtocolsHlt
set trafficItem1Objects [CreateTrafficItem ::trafficItem1]

puts "\n$trafficItem1Objects"

# status: 1
# log: 
# ::ixNet::OBJ-/traffic/trafficItem:1 - {Not all the Packets could be Generated: One or more destination MACs or VPNs are invalid or unreachable and the packets configured to be sent to them were not created}.
# stream_id: TI0-Traffic_Item_1
# traffic_item: ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1
# ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1:
#  headers: ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ethernet-1" ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ipv4-2" ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"fcs-3"
#  stream_ids: ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1
#   ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1:
#  headers: ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"ethernet-1" ::ixNet::OBJ-/traffic/trafficItem:#1/highLevelStream:1/stack:"ipv4-2" ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"fcs-3"
# endpoint_set_id: 1
# encapsulation_name: Ethernet.IPv4

RegenerateTrafficItems
StartTrafficHlt
after 10000

set stats [GetStatsHlt]

puts "\n[KeylPrint stats]"
