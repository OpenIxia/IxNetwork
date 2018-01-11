#!/opt/ActiveTcl-8.5/bin/tclsh

package req Ixia

set ixiaChassisIp 10.219.117.11
set ixNetworkTclServerIp 10.219.16.219
set userName hgee
set portList [list 8/3 8/4]
set port1 1/8/3
set port2 1/8/4


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

proc CreateTopologyNgpf { topologyParams } {
    upvar $topologyParams params

    puts "\nCreateTopologyNgpf ..."
    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "\nCreateTopology paramList: $paramList"

    set topologyStatus [eval ::ixiangpf::topology_config $paramList]

    if {[keylget topologyStatus status] != $::SUCCESS} {
	puts "\nError CreateTopologyNgpf: $topologyStatus"
	return 1
    }
    
    return [keylget topologyStatus topology_handle]
}

proc CreateDeviceGroupNgpf { deviceGroupParams } { 
    upvar $deviceGroupParams params

    puts "\nCreateDeviceGroupNgpf"
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
	puts "\nError CreateDeviceGroupNgpf: $topoDeviceGroupStatus"
	return 1
    } 

    return [keylget topoDeviceGroupStatus device_group_handle]
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
	puts "\nError PortConfigProtocolIntNgpf:\n$interfaceConfigStatus\n"
	return 1
    }

    # keylget interfaceConfigStatus:
    #    ethernet_handle: /topology:2/deviceGroup:2/ethernet:1
    #    ipv4_handle: /topology:2/deviceGroup:2/ethernet:1/ipv4:1
    #    interface_handle: /topology:2/deviceGroup:2/ethernet:1/ipv4:1/item:1
    # interface object = ::ixNet::OBJ-/vport:1/interface:1

    return $interfaceConfigStatus
}

proc ConfigVxlanEmulationNgpfHlt { configParams {returnHandle returnHandle} } {
    upvar $configParams params

    foreach {properties values} [array get params *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }

    puts "\nConfigVxlanEmulationNgpfHlt: $paramList ..."
    set status [eval ::ixiangpf::emulation_vxlan_config $paramList]
    
    if {[keylget status status] != $::SUCCESS} {
	puts "\nError ConfigVxlanEmulationNgpfHlt:\n$status\n"
	return 1
    }

    # keylget interfaceConfigStatus:
    #    ethernet_handle: /topology:2/deviceGroup:2/ethernet:1
    #    ipv4_handle: /topology:2/deviceGroup:2/ethernet:1/ipv4:1
    #    interface_handle: /topology:2/deviceGroup:2/ethernet:1/ipv4:1/item:1
    # interface object = ::ixNet::OBJ-/vport:1/interface:1

    if {$returnHandle == "returnHandle"} {
	return [keylget status vxlan_handle]
    }
}

proc ConfigMultiValueNgpfHlt { multiValueParams } {
    upvar $multiValueParams param

    foreach {properties values} [array get param *] {
	set property [lindex [split $properties ,] end]
	append paramList "$property $values "
    }
    
    puts "\nConfigMultiValueNgpfHlt"
    set multiValueStatus [eval ::ixiangpf::multivalue_config $paramList]

    if {[keylget multiValueStatus status] != $::SUCCESS} {
	puts "\nError ConfigMultiValueNgpfHlt: $multiValueStatus\n"
	return 1
    }

    return [keylget multiValueStatus multivalue_handle]
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

proc StartTrafficHlt {} {
    puts "\nStartTrafficHlt ..."
    set startTrafficStatus [::ixia::traffic_control \
				-action run \
			       ]
    if {[keylget startTrafficStatus status] != $::SUCCESS} {
	puts "\nError StartTrafficHlt: $startTrafficStatus\n"
	return 1
    } 

    after 10000
    # By including VerifyTrafficState, it will wait up to 15 seconds until
    # traffic is started before returning.
    #VerifyTrafficState
    return 0
}

puts "Rebooting ports $portList ..."
set connectStatus [eval ::ixia::connect \
		       -reset \
		       -device $ixiaChassisIp \
		       -port_list $portList \
		       -ixnetwork_tcl_server $ixNetworkTclServerIp \
		       -tcl_server $ixiaChassisIp \
		       -username $userName \
		      ]
if {[keylget connectStatus status] != $::SUCCESS} {
    puts "\nEror ConnectToIxia: $connectStatus\n"
    exit
}

# 1> Create new Topology Group
set topology1(-topology_name)  "IPv4 Topology Tx-1"
set topology1(-port_handle) "$port1"

set topology2(-topology_name)  "IPv4 Topology Rx-1"
set topology2(-port_handle) "$port2"

set topology1(portHandle) [CreateTopologyNgpf ::topology1]
set topology2(portHandle) [CreateTopologyNgpf ::topology2]

set deviceGroup1(-topology_handle) $topology1(portHandle)
set deviceGroup1(-device_group_multiplier) 2
set deviceGroup1(-device_group_name) "Ipv4 Tx"
set deviceGroup1(-device_group_enabled) 1

set deviceGroup2(-topology_handle) $topology2(portHandle)
set deviceGroup2(-device_group_multiplier) 2
set deviceGroup2(-device_group_name) "Ipv4 Tx-2"
set deviceGroup2(-device_group_enabled) 1

set deviceGroupHandle(topo1,dg1) [CreateDeviceGroupNgpf ::deviceGroup1]
set deviceGroupHandle(topo2,dg1) [CreateDeviceGroupNgpf ::deviceGroup2]

set ethernet_1(-mode)                    config
set ethernet_1(-protocol_handle)         $deviceGroupHandle(topo1,dg1)
set ethernet_1(-mtu)                     1500 
set ethernet_1(-src_mac_addr)            00:01:01:01:00:01
set ethernet_1(-src_mac_addr_step)       00:00:00:00:00:01
set ethernet_1(-vlan)                    0 ;# To enable vlan, use 1
set ethernet_1(-vlan_id)                 100
set ethernet_1(-vlan_user_priority)      3
set ethernet_1(-vlan_id_count)           5
set ethernet_1(-vlan_id_step)            1
set ethernet_1(-vlan_user_priority_step) 0

set status [PortConfigProtocolIntNgpf ::ethernet_1]
set ethernetHandle(topo1,dg1) [keylget status ethernet_handle]

set multivalue1(-pattern) counter
set multivalue1(-counter_start) 1.1.1.1
set multivalue1(-counter_step) 0.0.1.0
set multivalue1(-counter_direction) increment
set multivalue1(-nest_enabled) 0
set multivalue1(-nest_step) 0.0.0.1
set multivalue1(-nest_owner) $topology1(portHandle)

set multivalue(topo1,dg1,ip) [ConfigMultiValueNgpfHlt multivalue1]

set multivalue2(-pattern) counter
set multivalue2(-counter_start) 1.1.1.10
set multivalue2(-counter_step) 0.0.1.0
set multivalue2(-counter_direction) increment
set multivalue2(-nest_enabled) 0
set multivalue2(-nest_step) 0.0.0.1
set multivalue2(-nest_owner) $topology1(portHandle)

set multivalue(topo1,dg1,gateway) [ConfigMultiValueNgpfHlt multivalue2]

set ipv4_1(-protocol_handle)         $ethernetHandle(topo1,dg1)
set ipv4_1(-ipv4_resolve_gateway)    1
set ipv4_1(-intf_ip_addr)            $multivalue(topo1,dg1,ip)
set ipv4_1(-gateway)                 $multivalue(topo1,dg1,gateway)
set ipv4_1(-netmask)                 255.255.255.0
#set ipv4_1(-arp_send_req) 1
set ipv4_1(-ipv4_resolve_gateway)    1

set status [PortConfigProtocolIntNgpf ::ipv4_1]
set ipv4Handle(topo1,dg1) [keylget status ipv4_handle]

set ethernet_2(-mode)                    config
set ethernet_2(-protocol_handle)         $deviceGroupHandle(topo2,dg1)       
set ethernet_2(-mtu)                     1500 
set ethernet_2(-src_mac_addr)            00:01:01:02:00:01
set ethernet_2(-src_mac_addr_step)       00:00:00:00:00:01
set ethernet_2(-vlan)                    0 ;# To enable vlan, use 1
set ethernet_2(-vlan_id)                 100
set ethernet_2(-vlan_user_priority)      3
set ethernet_2(-vlan_id_count)           5
set ethernet_2(-vlan_id_step)            1
set ethernet_2(-vlan_user_priority_step) 0

set status [PortConfigProtocolIntNgpf ::ethernet_2]
set ethernetHandle(topo2,dg1) [keylget status ethernet_handle]

set multivalue3(-pattern) counter
set multivalue3(-counter_start) 1.1.1.10
set multivalue3(-counter_step) 0.0.1.0
set multivalue3(-counter_direction) increment
set multivalue3(-nest_enabled) 0
set multivalue3(-nest_step) 0.0.0.1
set multivalue3(-nest_owner) $topology2(portHandle)

set multivalue(topo2,dg1,ip) [ConfigMultiValueNgpfHlt multivalue3]

set multivalue4(-pattern) counter
set multivalue4(-counter_start) 1.1.1.1
set multivalue4(-counter_step) 0.0.1.0
set multivalue4(-counter_direction) increment
set multivalue4(-nest_enabled) 0
set multivalue4(-nest_step) 0.0.0.1
set multivalue4(-nest_owner) $topology2(portHandle)

set multivalue(topo2,dg1,gateway) [ConfigMultiValueNgpfHlt multivalue4]

set ipv4_2(-protocol_handle)         $ethernetHandle(topo2,dg1)
set ipv4_2(-intf_ip_addr)            $multivalue(topo2,dg1,ip)
set ipv4_2(-gateway)                 $multivalue(topo2,dg1,gateway)
set ipv4_2(-netmask)                 255.255.255.0
#set ipv4_2(-arp_send_req)            1
set ipv4_2(-ipv4_resolve_gateway)    1

set status [PortConfigProtocolIntNgpf ::ipv4_2]
set ipv4Handle(topo2,dg1) [keylget status ipv4_handle]


# VNI - topology 1
set multivalue5(-pattern) counter
set multivalue5(-counter_start) 1000
set multivalue5(-counter_step) 1
set multivalue5(-counter_direction) increment
set multivalue5(-nest_step) 1
set multivalue5(-nest_enabled) 0
set multivalue5(-nest_owner) $topology1(portHandle)

set multivalue(topo1,dg1,vni) [ConfigMultiValueNgpfHlt multivalue5]

# VxLAN multicast
set multivalue6(-pattern) counter
set multivalue6(-counter_start) 225.1.1.1
set multivalue6(-counter_step) 0.0.0.1
set multivalue6(-counter_direction) increment
set multivalue6(-nest_step) 0.0.0.1
set multivalue6(-nest_enabled) 0
set multivalue6(-nest_owner) $topology1(portHandle)

set multivalue(topo1,dg1,multicast) [ConfigMultiValueNgpfHlt multivalue6]

# VxLAN Remote static Mac
set multivalue10(-pattern) counter
set multivalue10(-counter_start) 00:00:00:00:00:00
set multivalue10(-counter_step)  00:00:00:00:00:00
set multivalue10(-counter_direction) increment
set multivalue10(-nest_step)         00:00:00:00:00:00
set multivalue10(-nest_enabled)      0
set multivalue10(-nest_owner) $topology2(portHandle)

set multivalue(topo1,dg1,remoteStaticMac) [ConfigMultiValueNgpfHlt multivalue10]

set vxlan1(-handle)               $ipv4Handle(topo1,dg1)
set vxlan1(-protocol_name)        "VxLan_1"
set vxlan1(-vni)                  $multivalue(topo1,dg1,vni)
set vxlan1(-ipv4_multicast)       $multivalue(topo1,dg1,multicast)
set vxlan1(-remote_vm_static_mac) $multivalue(topo1,dg1,remoteStaticMac)
set vxlan1(-remote_vtep_ipv4)     0.0.0.0
set vxlan1(-ip_to_vxlan_multiplier) 1

set vxlanHandle(topo1,dg1) [ConfigVxlanEmulationNgpfHlt vxlan1]
 

# VNI - topology 2
set multivalue7(-pattern) counter
set multivalue7(-counter_start) 1000
set multivalue7(-counter_step) 1
set multivalue7(-counter_direction) increment
set multivalue7(-nest_step) 1
set multivalue7(-nest_enabled) 0
set multivalue7(-nest_owner) $topology2(portHandle)

set multivalue(topo2,dg1,vni) [ConfigMultiValueNgpfHlt multivalue7]

# VxLAN multicast
set multivalue8(-pattern) counter
set multivalue8(-counter_start) 225.1.1.1
set multivalue8(-counter_step) 0.0.0.1
set multivalue8(-counter_direction) increment
set multivalue8(-nest_step) 0.0.0.1
set multivalue8(-nest_enabled) 0
set multivalue8(-nest_owner) $topology2(portHandle)

set multivalue(topo2,dg1,multicast) [ConfigMultiValueNgpfHlt multivalue8]

# VxLAN Remote static Mac
set multivalue9(-pattern) counter
set multivalue9(-counter_start) 00:00:00:00:00:00
set multivalue9(-counter_step)  00:00:00:00:00:00
set multivalue9(-counter_direction) increment
set multivalue9(-nest_step)         00:00:00:00:00:00
set multivalue9(-nest_enabled)      0
set multivalue9(-nest_owner) $topology2(portHandle)

set multivalue(topo2,dg1,remoteStaticMac) [ConfigMultiValueNgpfHlt multivalue9]

set vxlan2(-handle)               $ipv4Handle(topo2,dg1)
set vxlan2(-protocol_name)        "VxLan_1"
set vxlan2(-vni)                  $multivalue(topo2,dg1,vni)
set vxlan2(-ipv4_multicast)       $multivalue(topo2,dg1,multicast)
set vxlan2(-remote_vm_static_mac) $multivalue(topo2,dg1,remoteStaticMac)
set vxlan2(-remote_vtep_ipv4)     0.0.0.0
set vxlan2(-remote_info_active)   1
set vxlan2(-ip_to_vxlan_multiplier) 1

set vxlanHandle(topo2,dg1) [ConfigVxlanEmulationNgpfHlt vxlan2]

puts "\n---- vxlanHandle(topo2,dg1): $vxlanHandle(topo2,dg1) -----\n"

#--------- VM Hosts behind VxLAN -----------#

set deviceGroup3(-topology_handle) $deviceGroupHandle(topo1,dg1)
set deviceGroup3(-device_group_multiplier) 3
set deviceGroup3(-device_group_name) "Ipv4 Tx"
set deviceGroup3(-device_group_enabled) 1

set deviceGroup4(-topology_handle) $deviceGroupHandle(topo2,dg1)
set deviceGroup4(-device_group_multiplier) 3
set deviceGroup4(-device_group_name) "Ipv4 Tx-2"
set deviceGroup4(-device_group_enabled) 1

set deviceGroupHandle(topo1,dg3,vxlan) [CreateDeviceGroupNgpf ::deviceGroup3]
set deviceGroupHandle(topo2,dg4,vxlan) [CreateDeviceGroupNgpf ::deviceGroup4]

puts "\ndeviceGroupHandle(topo1,dg3,vxlan): $deviceGroupHandle(topo1,dg3,vxlan)" 
puts "\ndeviceGroupHandle(topo2,dg4,vxlan): $deviceGroupHandle(topo2,dg4,vxlan)\n" 


# VM Host1 - Src Mac
set multivalue9(-pattern) counter
set multivalue9(-counter_start) 00:11:11:11:00:01
set multivalue9(-counter_step)  00:00:00:00:00:01
set multivalue9(-counter_direction) increment
set multivalue9(-nest_step)         00.00.00.00.00.00,00.00.00.00.00.00
set multivalue9(-nest_enabled)      0,0
#set multivalue9(-nest_owner)        $deviceGroupHandle(topo1,dg1),$topology1(portHandle)
set multivalue9(-nest_owner)        $deviceGroupHandle(topo1,dg3,vxlan),$topology1(portHandle)

set multivalue(topo1,dg3,vxlan,srcMac) [ConfigMultiValueNgpfHlt multivalue9]

puts "\n----- deviceGroupHandle(topo1,dg3,vxlan): $deviceGroupHandle(topo1,dg3,vxlan) ---"

set ethernet_3(-mode)                    config
set ethernet_3(-protocol_handle)         $deviceGroupHandle(topo1,dg3,vxlan)
set ethernet_3(-connected_to_handle)     $vxlanHandle(topo1,dg1)     
set ethernet_3(-mtu)                     1500 
set ethernet_3(-src_mac_addr)            $multivalue(topo1,dg3,vxlan,srcMac)
set ethernet_3(-vlan)                    0 ;# To enable vlan, use 1
set ethernet_3(-vlan_id)                 100
set ethernet_3(-vlan_user_priority)      3
set ethernet_3(-vlan_id_count)           5
set ethernet_3(-vlan_id_step)            1
set ethernet_3(-vlan_tpid)               0x8100
set ethernet_3(-vlan_user_priority_step) 0

set status [PortConfigProtocolIntNgpf ::ethernet_3]
set ethernetVxlanHandle(topo1,dg3) [keylget status ethernet_handle]
puts "\n----ethernetVxlan handle: $ethernetVxlanHandle(topo1,dg3) ------\n"

set multivalue11(-pattern) counter
set multivalue11(-counter_start) 10.1.1.1
set multivalue11(-counter_step) 0.0.1.0
set multivalue11(-counter_direction) increment
set multivalue11(-nest_step) 0.0.0.0,0.0.0.0
#set multivalue11(-nest_owner) $deviceGroupHandle(topo1,dg1),$topology1(portHandle)
set multivalue11(-nest_owner) $deviceGroupHandle(topo1,dg3,vxlan),$topology1(portHandle)
set multivalue11(-nest_enabled) 0,0

set multivalue(topo1,dg3,ip) [ConfigMultiValueNgpfHlt multivalue11]

set multivalue12(-pattern) counter
set multivalue12(-counter_start) 10.1.1.10
set multivalue12(-counter_step) 0.0.1.0
set multivalue12(-counter_direction) increment
set multivalue12(-nest_step) 0.0.0.0,0.0.0.0
set multivalue12(-nest_owner) $topology1(portHandle),$deviceGroupHandle(topo1,dg3,vxlan)
set multivalue12(-nest_enabled) 0,0

set multivalue(topo1,dg3,gateway) [ConfigMultiValueNgpfHlt multivalue12]

set ipv4_3(-protocol_handle)         $ethernetVxlanHandle(topo1,dg3)
set ipv4_3(-intf_ip_addr)            $multivalue(topo1,dg3,ip)
set ipv4_3(-gateway)                 $multivalue(topo1,dg3,gateway)
set ipv4_3(-netmask)                 255.255.255.0
#set ipv4_3(-arp_send_req) 1
set ipv4_3(-ipv4_resolve_gateway)    1

set status [PortConfigProtocolIntNgpf ::ipv4_3]
set ipv4VxlanHandle(topo1,dg3) [keylget status ipv4_handle]

# ipv4VxlanHandle(topo1,dg3)
# /topology:1/deviceGroup:1/deviceGroup:1/ethernet:1/ipv4:1


# VM Host2 - Src Mac
set multivalue14(-pattern) counter
set multivalue14(-counter_start)     00:22:22:22:00:01
set multivalue14(-counter_step)      00:00:00:00:00:01
set multivalue14(-counter_direction) increment
set multivalue14(-nest_step)         00.00.00.00.00.00,00.00.00.00.00.00
set multivalue14(-nest_enabled)      0,0
#set multivalue14(-nest_owner)        $deviceGroupHandle(topo2,dg1),$topology2(portHandle)
set multivalue14(-nest_owner)        $topology2(portHandle),$deviceGroupHandle(topo2,dg4,vxlan)

set multivalue(topo2,dg4,vxlan,srcMac) [ConfigMultiValueNgpfHlt multivalue14]


# deviceGroupHandle(topo2,dg4,vxlan)
# /topology:2/deviceGroup:1/deviceGroup:1

set ethernet_4(-mode)                    config
set ethernet_4(-protocol_handle)         $deviceGroupHandle(topo2,dg4,vxlan)
set ethernet_4(-connected_to_handle)     $vxlanHandle(topo2,dg1)
set ethernet_4(-mtu)                     1500 
set ethernet_4(-src_mac_addr)            $multivalue(topo2,dg4,vxlan,srcMac)
set ethernet_4(-vlan)                    0 ;# To enable vlan, use 1
set ethernet_4(-vlan_id)                 100
set ethernet_4(-vlan_user_priority)      3
set ethernet_4(-vlan_id_count)           5
set ethernet_4(-vlan_id_step)            1
set ethernet_4(-vlan_user_priority_step) 0

set status [PortConfigProtocolIntNgpf ::ethernet_4]
set ethernetVxlanHandle(topo2,dg4) [keylget status ethernet_handle]
# /topology:2/deviceGroup:1/deviceGroup:1/ethernet:1

# VM Host2 - ip
set multivalue13(-pattern) counter
set multivalue13(-counter_start) 10.1.1.10
set multivalue13(-counter_step) 0.0.1.0
set multivalue13(-counter_direction) increment
set multivalue13(-nest_enabled) 1,1
set multivalue13(-nest_step) 0.0.1.0,0.0.1.0
set multivalue13(-nest_owner) $topology2(portHandle),$deviceGroupHandle(topo2,dg4,vxlan)

set multivalue(topo2,dg4,ip) [ConfigMultiValueNgpfHlt multivalue13]

# VM Host2 - gateway
set multivalue14(-pattern) counter
set multivalue14(-counter_start) 10.1.1.1
set multivalue14(-counter_step) 0.0.1.0
set multivalue14(-counter_direction) increment
set multivalue14(-nest_enabled) 1,1
set multivalue14(-nest_step) 0.0.1.0,0.0.1.0
set multivalue14(-nest_owner) $topology2(portHandle),$deviceGroupHandle(topo2,dg4,vxlan)

set multivalue(topo2,dg4,gateway) [ConfigMultiValueNgpfHlt multivalue14]

set ipv4_4(-protocol_handle)         $ethernetVxlanHandle(topo2,dg4)
set ipv4_4(-intf_ip_addr)            $multivalue(topo2,dg4,ip)
set ipv4_4(-gateway)                 $multivalue(topo2,dg4,gateway)
set ipv4_4(-netmask)                 255.255.255.0
#set ipv4_4(-arp_send_req)            1
set ipv4_4(-ipv4_resolve_gateway)    1

set status [PortConfigProtocolIntNgpf ::ipv4_4]
set ipv4VxlanHandle(topo2,dg4) [keylget status ipv4_handle]

# /topology:2/deviceGroup:1/deviceGroup:1/ethernet:1/ipv4:1


StartAllProtocolsHlt ngpf
after 10000


set trafficItem1(-mode) create 
set trafficItem1(-endpointset_count) 1
set trafficItem1(-emulation_src_handle) $ipv4VxlanHandle(topo1,dg3)
set trafficItem1(-emulation_dst_handle) $ipv4VxlanHandle(topo2,dg4)
set trafficItem1(-src_dest_mesh) one_to_one
set trafficItem1(-route_mesh) one_to_one
set trafficItem1(-bidirectional) 1
set trafficItem1(-allow_self_destined) 0
set trafficItem1(-name) Traffic_Item_1
set trafficItem1(-circuit_endpoint_type) ipv4
set trafficItem1(-track_by) {trackingenabled0 sourceDestValuePair0}
set trafficItem1(-l3_protocol) ipv4

set trafficItem1Keys [CreateTrafficItem trafficItem1]
puts \n[KeylPrint trafficItem1Keys]\n

StartTrafficHlt

set stats [::ixiangpf::traffic_stats -mode flow]

puts "\n[KeylPrint stats]\n"


