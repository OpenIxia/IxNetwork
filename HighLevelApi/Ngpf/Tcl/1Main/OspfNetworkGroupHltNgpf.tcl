#!/usr/bin/tclsh

# This OSPF NGPF script will:
#
#   - Create two topologies
#   - Each topology has one ospf interface and network groups
#     to advertise ospf routes
#   - Traffic Item endpoints are ospf routes to ospf routes.


package req Ixia
source IxNet_tclApi.tcl

set ixiaChassisIp 10.219.116.72
set ixNetworkTclServerIp 192.168.70.127
set portList {1/1 1/2}
set userName hgee
set port1 1/1/1
set port2 1/1/2

puts "Rebooting ports $portList ..."
#set connectStatus [ConnectToIxiaNgpf "-reset -device $ixiaChassisIp -port_list $portList -ixnetwork_tcl_server $ixNetworkTclServerIp -tcl_server $ixiaChassisIp -username $userName"]

set connect(-reset) 1
set connect(-device) $ixiaChassisIp
set connect(-port_list) $portList
set connect(-ixnetwork_tcl_server) $ixNetworkTclServerIp
set connect(-tcl_server) $ixiaChassisIp
set connect(-username) $userName
set connectStatus [ConnectToIxiaNgpfHlt connect]
if {$connectStatus == 1} {
    exit
}

# 1> Create new Topology Group
set topology1(-topology_name)  "IGMP Host"
set topology1(-port_handle) [list [list $port1]]

set topology2(-topology_name)  "IGMP Querier"
set topology2(-port_handle) [list [list $port2]]

set topology1Keys [CreateNewTopologyNgpfHlt ::topology1]
set topology2Keys [CreateNewTopologyNgpfHlt ::topology2]

set topology1(portHandle) [keylget topology1Keys topology_handle]
set topology2(portHandle) [keylget topology2Keys topology_handle]

# 2> Create Device Group(s) to a Topology Group
set deviceGroup1(topo1,-topology_handle) $topology1(portHandle)
set deviceGroup1(topo1,-device_group_multiplier) 3
set deviceGroup1(topo1,-device_group_name) "Ospf Host"
set deviceGroup1(topo1,-device_group_enabled) 1
set deviceGroup1(topo1,protocolName) "Ethernet"

set deviceGroup2(topo2,-topology_handle) $topology2(portHandle)
set deviceGroup2(topo2,-device_group_multiplier) 3
set deviceGroup2(topo2,-device_group_name) "Ospf Querier"
set deviceGroup2(topo2,-device_group_enabled) 1
set deviceGroup2(topo2,protocolName) "Ethernet"

set topo1DeviceGroup1Keys [CreateNewDeviceGroupNgpfHlt deviceGroup1]
set topo2DeviceGroup2Keys [CreateNewDeviceGroupNgpfHlt deviceGroup2]

puts "\n[KeylPrint topo1DeviceGroup1Keys]\n"

set deviceGroup(topo1,groupHandle) [keylget topo1DeviceGroup1Keys device_group_handle]
set deviceGroup(topo2,groupHandle) [keylget topo2DeviceGroup2Keys device_group_handle]

# Mac Address
set topo1MacAddrStatus [::ixiangpf::multivalue_config \
		      -pattern counter \
		      -nest_owner $topology1(portHandle) \
		      -counter_direction increment \
		      -counter_start 00:01:01:01:00:01 \
		      -counter_step 00.00.00.00.00.01 \
		      -nest_step 00.00.01.00.00.00 \
		      -nest_enabled 1 \
		     ]
set topo1MacAddrObj [keylget topo1MacAddrStatus multivalue_handle]

puts "\n--- topo1MacAddr: $topo1MacAddrObj ---\n"

set topo1VlanStatus [::ixiangpf::multivalue_config \
		   -pattern single_value \
		   -single_value 100 \
		   -nest_owner $topology1(portHandle) \
		   -nest_enabled 0 \
		   -nest_step 1 \
		  ]
set topo1VlanObj [keylget topo1VlanStatus multivalue_handle]
puts "\n--- topo1Vlan: $topo1VlanObj ---\n"

set portConfig1(-mtu)                     1500
set portConfig1(-protocol_handle)         $deviceGroup(topo1,groupHandle)
set portConfig1(-protocol_name)           "Ethernet"
set portConfig1(-src_mac_addr)            $topo1MacAddrObj
set portConfig1(-vlan)                    1 ;# To enable vlan, use 1
set portConfig1(-vlan_id)                 $topo1VlanObj
set portConfig1(-vlan_user_priority)      0
set portConfig1(-vlan_id_count)           1
set portConfig1(-vlan_id_step)            1
set portConfig1(-vlan_tpid)               0x8100
set portConfig1(-vlan_user_priority_step) 0

set ethernetObj [PortConfigProtocolIntNgpfHlt portConfig1]
set topo1Dg1EthernetHandle [keylget ethernetObj ethernet_handle]

puts "\n[KeylPrint ethernetObj]\n"
puts "\n--- topo1Dg1EthernetHandle: $topo1Dg1EthernetHandle ---\n"
# ethernet_handle: /topology:1/deviceGroup:1/ethernet:1
#interface_handle: /topology:1/deviceGroup:1/ethernet:1/item:1 /topology:1/deviceGroup:1/ethernet:1/item:2 /topology:1/deviceGroup:1/ethernet:1/item:3



set topo1IpAddrStatus [::ixiangpf::multivalue_config \
			   -pattern counter \
			   -nest_owner $topology1(portHandle) \
			   -counter_direction increment \
			   -counter_step 0.0.0.1 \
			   -nest_step 0.1.0.0 \
			   -nest_enabled 1 \
			   -counter_start 10.10.10.1 \
			   -overlay_value 10.10.10.1,10.10.10.2,10.10.10.3 \
			   -overlay_value_step 10.10.10.1,10.10.10.2,10.10.10.3 \
			   -overlay_index 1,2,3 \
			   -overlay_index_step 0,0,0 \
			   -overlay_count 1,1,1 \
			  ]
set topo1IpAddrObj [keylget topo1IpAddrStatus multivalue_handle]
puts "\n--- topo1IpAddr: $topo1IpAddrObj ---\n"

set topo1GatewayAddrStatus [::ixiangpf::multivalue_config \
				-pattern counter \
				-nest_owner $topology1(portHandle) \
				-counter_direction increment \
				-counter_start 10.10.10.4 \
				-counter_step 0.0.1.0 \
				-nest_step 0.1.0.0 \
				-nest_enabled 1 \
				-overlay_value 10.10.10.4,10.10.10.5,10.10.10.6 \
				-overlay_value_step 10.10.10.4,10.10.10.5,10.10.10.6 \
				-overlay_index 1,2,3 \
				-overlay_index_step 0,0,0 \
				-overlay_count 1,1,1 \
			   ]
set topo1GatewayAddrObj [keylget topo1GatewayAddrStatus multivalue_handle]
puts "\n---- topo1GatewayAddr: $topo1GatewayAddrObj ---\n"

set portConfig1a(-gateway)                 $topo1GatewayAddrObj
set portConfig1a(-intf_ip_addr)            $topo1IpAddrObj
set portConfig1a(-netmask)                 255.255.255.0
set portConfig1a(-protocol_handle)         $topo1Dg1EthernetHandle
set portConfig1a(-protocol_name)           "IPv4"

set ipv4Obj [PortConfigProtocolIntNgpfHlt portConfig1a]
puts "\n[KeylPrint ipv4Obj]\n"

set topo1Dg1Ipv4 [keylget ipv4Obj ipv4_handle]

# ipv4_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1
#interface_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:1 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:2 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:3

# topology 2 device group 1
# Mac Address
set topo2MacAddrStatus [::ixiangpf::multivalue_config \
			    -pattern counter \
			    -nest_owner $topology2(portHandle) \
			    -counter_direction increment \
			    -counter_start 00:01:01:02:00:01 \
			    -counter_step 00.00.00.00.00.01 \
			    -nest_step 00.00.01.00.00.00 \
			    -nest_enabled 1 \
			   ]
set topo2MacAddrObj [keylget topo2MacAddrStatus multivalue_handle]

puts "\n--- topo2MacAddr: $topo2MacAddrObj ---\n"

set topo2VlanStatus [::ixiangpf::multivalue_config \
			 -pattern single_value \
			 -single_value 100 \
			 -nest_owner $topology2(portHandle) \
			 -nest_enabled 0 \
			 -nest_step 1 \
			]
set topo2VlanObj [keylget topo2VlanStatus multivalue_handle]
puts "\n--- topo2Vlan: $topo2VlanObj ---\n"

set portConfig2(-mtu)                     1500
set portConfig2(-protocol_handle)         $deviceGroup(topo2,groupHandle)
set portConfig2(-protocol_name)           "Ethernet"
set portConfig2(-src_mac_addr)            $topo2MacAddrObj
set portConfig2(-vlan)                    1;# To enable vlan, use 1
set portConfig2(-vlan_id)                 $topo2VlanObj
set portConfig2(-vlan_user_priority)      0
set portConfig2(-vlan_id_count)           1
set portConfig2(-vlan_id_step)            1
set portConfig2(-vlan_tpid)               0x8100
set portConfig2(-vlan_user_priority_step) 0

set ethernetObj [PortConfigProtocolIntNgpfHlt portConfig2]
set topo2Dg1EthernetHandle [keylget ethernetObj ethernet_handle]

puts "\n[KeylPrint ethernetObj]\n"
puts "\n--- topo2Dg1EthernetHandle: $topo2Dg1EthernetHandle ---\n"
# ethernet_handle: /topology:1/deviceGroup:1/ethernet:1
#interface_handle: /topology:1/deviceGroup:1/ethernet:1/item:1 /topology:1/deviceGroup:1/ethernet:1/item:2 /topology:1/deviceGroup:1/ethernet:1/item:3


set topo2IpAddrStatus [::ixiangpf::multivalue_config \
			   -pattern counter \
			   -nest_owner $topology2(portHandle) \
			   -counter_direction increment \
			   -counter_step 0.0.0.1 \
			   -nest_step 0.1.0.0 \
			   -nest_enabled 1 \
			   -counter_start 10.10.10.4 \
			   -overlay_value 10.10.10.4,10.10.10.5,10.10.10.6 \
			   -overlay_value_step 10.10.10.4,10.10.10.5,10.10.10.6 \
			   -overlay_index 1,2,3 \
			   -overlay_index_step 0,0,0 \
			   -overlay_count 1,1,1 \
		      ]
set topo2IpAddrObj [keylget topo2IpAddrStatus multivalue_handle]
puts "\n--- topo2IpAddr: $topo2IpAddrObj ---\n"

set topo2GatewayAddrStatus [::ixiangpf::multivalue_config \
				-pattern counter \
				-nest_owner $topology2(portHandle) \
				-counter_direction increment \
				-counter_start 10.10.10.1 \
				-counter_step 0.0.1.0 \
				-nest_step 0.1.0.0 \
				-nest_enabled 1 \
				-overlay_value 10.10.10.1,10.10.10.2,10.10.10.3 \
				-overlay_value_step 10.10.10.1,10.10.10.2,10.10.10.3 \
				-overlay_index 1,2,3 \
				-overlay_index_step 0,0,0 \
				-overlay_count 1,1,1 \
			       ]
set topo2GatewayAddrObj [keylget topo2GatewayAddrStatus multivalue_handle]
puts "\n---- topo2GatewayAddr: $topo2GatewayAddrObj ---\n"



set portConfig2a(-gateway)                 $topo2GatewayAddrObj
set portConfig2a(-intf_ip_addr)            $topo2IpAddrObj
set portConfig2a(-netmask)                 255.255.255.0
set portConfig2a(-protocol_handle)         $topo2Dg1EthernetHandle
set portConfig2a(-protocol_name)           "IPv4"

set ipv4Obj [PortConfigProtocolIntNgpfHlt portConfig2a]
puts "\n[KeylPrint ipv4Obj]\n"

set topo2Dg1Ipv4 [keylget ipv4Obj ipv4_handle]
# ipv4_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1
#interface_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:1 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:2 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:3

puts "\n---- topo1Dg1Ipv4: $topo1Dg1Ipv4 ----\n"

# ConfigNgpfMultiValueHlt
set ospfRouterIdActive [::ixiangpf::multivalue_config \
			 -pattern single_value \
			 -single_value 1 \
			]

set ospfRouterIdActive [keylget ospfRouterIdActive multivalue_handle]

# ConfigNgpfMultiValueHlt
set ospfRouterId [::ixiangpf::multivalue_config \
		  -pattern  counter \
		  -counter_start 10.10.10.1 \
		  -counter_step  0.0.0.1 \
		  -counter_direction increment \
		  -nest_step  0.1.0.0 \
		  -nest_owner $topology1(portHandle) \
		  -nest_enabled 0 \
		  -overlay_value 10.10.10.1 \
		  -overlay_value_step  10.10.10.1 \
		  -overlay_index 1 \
		  -overlay_index_step 0 \
		  -overlay_count 1 \
		 ]

set ospfRouterId [keylget ospfRouterId multivalue_handle]	      
puts "\n----- ospf routerId: $ospfRouterId ----\n"

set ospfTopo1(-mode) create
set ospfTopo1(-protocol_name) ospf-10.10.10.1
set ospfTopo1(-handle) $topo1Dg1Ipv4
set ospfTopo1(-router_id) $ospfRouterId
set ospfTopo1(-router_interface_active) $ospfRouterIdActive
set ospfTopo1(-router_active) 1
set ospfTopo1(-network_type) broadcast
set ospfTopo1(-hello_interval) 10
set ospfTopo1(-dead_interval) 40
set ospfTopo1(-interface_cost) 10
set ospfTopo1(-graceful_restart_enable) 0
set ospfTopo1(-neighbor_router_id) 0.0.0.0
set ospfTopo1(-router_priority) 2
set ospfTopo1(-enable_fast_hello) 0
set ospfTopo1(-max_mtu) 1500
set ospfTopo1(-area_id) 0.0.0.0
set ospfTopo1(-area_id_type) ip
set ospfTopo1(-lsa_retransmit_time) 5
set ospfTopo1(-lsa_discard_mode) 0

# ::ixiangpf::emulation_ospf_config
set ospfTopo1Keys [ConfigOspfEmulationNgpfHlt ospfTopo1]
set ospfTopo1Handle [keylget ospfTopo1Keys ospfv2_handle]
puts "\nospfTopo1Handle: $ospfTopo1Handle\n"

# ospfTopo1Handle: {status 1} {ospfv2_handle /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1} {handle {/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1/item:1 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1/item:2 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1/item:3}}

# ConfigNgpfMultiValueHlt
set ospfDrActive [::ixiangpf::multivalue_config \
		      -pattern single_value \
		      -single_value 1 \
		     ]
set ospfDrActive [keylget ospfDrActive multivalue_handle]

set ospfDrTopo1(-mode) create
set ospfDrTopo1(-enable_dr_bdr) $ospfDrActive
set ospfDrTopo1(-handle) /globals

# ::ixiangpf::emulation_ospf_config
set ospfDesignatedRouter [ConfigOspfEmulationNgpfHlt ospfDrTopo1]

set ospfRouteRanges [::ixiangpf::multivalue_config \
			 -pattern counter \
			 -counter_start 188.10.10.1 \
			 -counter_step 0.0.1.0 \
			 -counter_direction increment \
			 -nest_step 0.0.0.1,0.1.0.0 \
			 -nest_owner $topology1(portHandle) \
			 -nest_enabled 1 \
			]
set ospfRouteRanges [keylget ospfRouteRanges multivalue_handle]

set ospfNetworkGroupTopo1(-protocol_handle) $deviceGroup(topo1,groupHandle)
set ospfNetworkGroupTopo1(-connected_to_handle) $topo1Dg1EthernetHandle
# 'prefix': ['200.2.0.0/24', '201.2.0.0/24']
set ospfNetworkGroupTopo1(-type) ipv4-prefix
set ospfNetworkGroupTopo1(-enable_device) 1
set ospfNetworkGroupTopo1(-protocol_name) "OspfRoutes:188.10.10.0"
set ospfNetworkGroupTopo1(-ipv4_prefix_length) 24
# 100, 88
set ospfNetworkGroupTopo1(-ipv4_prefix_number_of_addresses) 100
set ospfNetworkGroupTopo1(-ipv4_prefix_network_address) $ospfRouteRanges
set ospfNetworkGroupTopo1(-multiplier) 1
# 'routeOrigin': ['nssa', 'another_area'],

# ::ixiangpf::network_group_config
# This is used as source/destination endpoints
set ospfNetworkGroupTopo1Keys [ConfigNetworkGroupNgpfHlt ospfNetworkGroupTopo1]

## This is used as source/destination endpoints
# /topology:1/deviceGroup:1/networkGroup:1
set ospfNetworkGroupTopo1Handle [keylget ospfNetworkGroupTopo1Keys network_group_handle]
#set ospfNetworkGroupTopo1Endpoints [keylget ospfNetworkGroupTopo1Keys ipv4_prefix_pools_handle]
 
puts "\n---- ospfNetworkGroupTopo1Handle: $ospfNetworkGroupTopo1Handle ----\n"
# ospfNetworkGroupTopo1Handle: {status 1} {network_group_handle /topology:1/deviceGroup:1/networkGroup:1} {ipv4_prefix_pools_handle /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1}

set ospfNssaRouteOrigin [::ixiangpf::multivalue_config \
			 -pattern single_value \
			 -single_value nssa\
			 -overlay_value nssa \
			 -overlay_value_step nssa \
			 -overlay_index 1 \
			 -overlay_index_step 0 \
			 -overlay_count 0 \
			]

set ospfNssaRouteOrigin [keylget ospfNssaRouteOrigin multivalue_handle]

set ospfNssa(-handle) $ospfNetworkGroupTopo1Handle
set ospfNssa(-mode) modify
set ospfNssa(-ipv4_prefix_metric) 0
set ospfNssa(-ipv4_prefix_active) 1
set ospfNssa(-ipv4_prefix_allow_propagate) 0
set ospfNssa(-ipv4_prefix_route_origin) $ospfNssaRouteOrigin 

# ::ixiangpf::emulation_ospf_network_group_config
set ospfNssaHandle [ConfigOspfNetworkGroupNgpfHlt ospfNssa]

# ospfNssaHandle: {status 1} {network_group_handle /topology:1/deviceGroup:1/networkGroup:1} {ipv4_prefix_pools_handle /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1} {ipv4_prefix_interface_handle /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/ospfRouteProperty:1}
puts "\nospfNssaHandle: $ospfNssaHandle\n"

# /topology:1/deviceGroup:1/networkGroup:1
set ospfNssaHandle [keylget ospfNssaHandle network_group_handle]
puts "\nospfNssaHandle: $ospfNssaHandle\n"

#-------- Topology 2 Ospf ---------

# ConfigNgpfMultiValueHlt
set ospfRouterIdActive2 [::ixiangpf::multivalue_config \
			 -pattern single_value \
			 -single_value 1 \
			]

set ospfRouterIdActive2 [keylget ospfRouterIdActive2 multivalue_handle]

# ConfigNgpfMultiValueHlt
set ospfRouterId2 [::ixiangpf::multivalue_config \
		  -pattern  counter \
		  -counter_start 10.10.10.4 \
		  -counter_step  0.0.0.1 \
		  -counter_direction increment \
		  -nest_step  0.1.0.0 \
		  -nest_owner $topology2(portHandle) \
		  -nest_enabled 0 \
		  -overlay_value 10.10.10.4 \
		  -overlay_value_step  10.10.10.4 \
		  -overlay_index 1 \
		  -overlay_index_step 0 \
		  -overlay_count 1 \
		 ]

set ospfRouterId2 [keylget ospfRouterId2 multivalue_handle]	      
puts "\n----- ospf routerId: $ospfRouterId ----\n"

set ospfTopo2(-mode) create
set ospfTopo2(-protocol_name) ospf-10.10.10.4
set ospfTopo2(-handle) $topo2Dg1Ipv4
set ospfTopo2(-router_id) $ospfRouterId2
set ospfTopo2(-router_interface_active) $ospfRouterIdActive2
set ospfTopo2(-router_active) 1
set ospfTopo2(-network_type) broadcast
set ospfTopo2(-hello_interval) 10
set ospfTopo2(-dead_interval) 40
set ospfTopo2(-interface_cost) 10
set ospfTopo2(-graceful_restart_enable) 0
set ospfTopo2(-neighbor_router_id) 0.0.0.0
set ospfTopo2(-router_priority) 2
set ospfTopo2(-enable_fast_hello) 0
set ospfTopo2(-max_mtu) 1500
set ospfTopo2(-area_id) 0.0.0.0
set ospfTopo2(-area_id_type) ip
set ospfTopo2(-lsa_retransmit_time) 5
set ospfTopo2(-lsa_discard_mode) 0

# ::ixiangpf::emulation_ospf_config
set ospfTopo2Keys [ConfigOspfEmulationNgpfHlt ospfTopo2]
set ospfTopo2Handle [keylget ospfTopo2Keys ospfv2_handle]
puts "\nospfTopo2Handle: $ospfTopo2Handle\n"

# ospfTopo2Handle: {status 1} {ospfv2_handle /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1} {handle {/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1/item:1 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1/item:2 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1/item:3}}

# ConfigNgpfMultiValueHlt
set ospfDrActive2 [::ixiangpf::multivalue_config \
		      -pattern single_value \
		      -single_value 1 \
		     ]
set ospfDrActive2 [keylget ospfDrActive2 multivalue_handle]

set ospfDrTopo2(-mode) create
set ospfDrTopo2(-enable_dr_bdr) $ospfDrActive2
set ospfDrTopo2(-handle) /globals

# ::ixiangpf::emulation_ospf_config
set ospfDesignatedRouter2 [ConfigOspfEmulationNgpfHlt ospfDrTopo2]

set ospfRouteRanges2 [::ixiangpf::multivalue_config \
			 -pattern counter \
			 -counter_start 208.10.10.1 \
			 -counter_step 0.0.1.0 \
			 -counter_direction increment \
			 -nest_step 0.0.0.1,0.1.0.0 \
			 -nest_owner $topology2(portHandle) \
			 -nest_enabled 1 \
			]
set ospfRouteRanges2 [keylget ospfRouteRanges2 multivalue_handle]

set ospfNetworkGroupTopo2(-protocol_handle) $deviceGroup(topo2,groupHandle)
set ospfNetworkGroupTopo2(-connected_to_handle) $topo2Dg1EthernetHandle
set ospfNetworkGroupTopo2(-type) ipv4-prefix
set ospfNetworkGroupTopo2(-enable_device) 1
set ospfNetworkGroupTopo2(-protocol_name) "OspfRoutes:288.10.10.0"
set ospfNetworkGroupTopo2(-ipv4_prefix_length) 24
set ospfNetworkGroupTopo2(-ipv4_prefix_number_of_addresses) 100
set ospfNetworkGroupTopo2(-ipv4_prefix_network_address) $ospfRouteRanges2
set ospfNetworkGroupTopo2(-multiplier) 1
# 'routeOrigin': ['nssa', 'another_area'],

# ::ixiangpf::network_group_config
# This is used as source/destination endpoints
set ospfNetworkGroupTopo2Keys [ConfigNetworkGroupNgpfHlt ospfNetworkGroupTopo2]

## This is used as source/destination endpoints
# /topology:1/deviceGroup:1/networkGroup:1
set ospfNetworkGroupTopo2Handle [keylget ospfNetworkGroupTopo2Keys network_group_handle]
#set ospfNetworkGroupTopo2Endpoints [keylget ospfNetworkGroupTopo2Keys ipv4_prefix_pools_handle]
 
puts "\n---- ospfNetworkGroupTopo2Handle: $ospfNetworkGroupTopo2Handle ----\n"
# ospfNetworkGroupTopo2Handle: {status 1} {network_group_handle /topology:1/deviceGroup:1/networkGroup:1} {ipv4_prefix_pools_handle /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1}

set ospfAnotherAreaRouteOrigin [::ixiangpf::multivalue_config \
			 -pattern single_value \
			 -single_value another_area \
			 -overlay_value another_area \
			 -overlay_value_step another_area \
			 -overlay_index 1 \
			 -overlay_index_step 0 \
			 -overlay_count 0 \
			]

set ospfAnotherAreaRouteOrigin [keylget ospfAnotherAreaRouteOrigin multivalue_handle]

set ospfAnotherArea(-handle) $ospfNetworkGroupTopo2Handle
set ospfAnotherArea(-mode) modify
set ospfAnotherArea(-ipv4_prefix_metric) 0
set ospfAnotherArea(-ipv4_prefix_active) 1
set ospfAnotherArea(-ipv4_prefix_allow_propagate) 0
set ospfAnotherArea(-ipv4_prefix_route_origin) $ospfAnotherAreaRouteOrigin

# ::ixiangpf::emulation_ospf_network_group_config
set ospfAnotherAreaHandle [ConfigOspfNetworkGroupNgpfHlt ospfAnotherArea]

# ospfAnotherAreaHandle: {status 1} {network_group_handle /topology:1/deviceGroup:1/networkGroup:1} {ipv4_prefix_pools_handle /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1} {ipv4_prefix_interface_handle /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/ospfRouteProperty:1}
puts "\nospfAnotherAreaHandle: $ospfAnotherAreaHandle\n"

# /topology:1/deviceGroup:1/networkGroup:1
set ospfAnotherAreaHandle [keylget ospfAnotherAreaHandle network_group_handle]
puts "\nospfAnotherAreaHandle: $ospfAnotherAreaHandle\n"

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

if {[VerifyProtocolSessionStatusUpNgpfHlt $ospfTopo1Handle] == 1} {
    exit
}

set ospfAggregatedStats [GetOspfAggregatedStatsNgpfHlt $ospfTopo1Handle]
puts "\nOspf Aggregated stats:\n[KeylPrint ospfAggregatedStats]\n"


set trafficItem1 [::ixia::traffic_config \
		      -mode create \
		      -endpointset_count 1 \
		      -circuit_endpoint_type ipv4 \
		      -emulation_src_handle [list $ospfNetworkGroupTopo1Handle] \
		      -emulation_dst_handle [list $ospfNetworkGroupTopo2Handle] \
		      -track_by  "trackingenabled0 sourceDestValuePair0" \
		      -name "ospf routes-to-routes" \
		      -bidirectional 0 \
		      -rate_percent 10 \
		      -pkts_per_burst 10000 \
		      -transmit_mode continuous \
		      -frame_size 100 \
		      -allow_self_destined 1 \
		     ]

puts "\nTrafficItemStatus:\n[KeylPrint trafficItem1]\n"

RegenerateTrafficItems
StartTrafficHlt
after 10000

#set stats [GetStatView]
set stats [GetStats]
puts "\n[KeylPrint stats]"

ixNet disconnect
