#!/usr/bin/tclsh

# This NGPF script will:
#
#   - Create igmp host joining three igmp groups.
#   - Create a querier port.
#   - Get and verifies all igmp reports sent by the DUT to the querier.
#   - Traffic Item has example on:
#        - Sending to all_multicast_ranges.
#        - Send to selective igmp group ranges.
#

package req Ixia
source /home/hgee/Dropbox/MyIxiaWork/IxNet_tclApi.tcl

set ixiaChassisIp 10.219.116.72
set ixNetworkTclServerIp 192.168.70.127
set portList {1/1 1/2}
set userName hgee
set port1 1/1/1
set port2 1/1/2

puts "Rebooting ports $portList ..."
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
#    
set deviceGroup1(topo1,-topology_handle) $topology1(portHandle)
set deviceGroup1(topo1,-device_group_multiplier) 3
set deviceGroup1(topo1,-device_group_name) "IGMP Host"
set deviceGroup1(topo1,-device_group_enabled) 1
#set deviceGroup1(topo1,protocolName) "Ethernet"

set deviceGroup2(topo2,-topology_handle) $topology2(portHandle)
set deviceGroup2(topo2,-device_group_multiplier) 3
set deviceGroup2(topo2,-device_group_name) "IGMP Querier"
set deviceGroup2(topo2,-device_group_enabled) 1
#set deviceGroup2(topo2,protocolName) "Ethernet"

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
			   -counter_start 10.10.10.2 \
			   -overlay_value 10.10.10.2,10.10.10.3,10.10.10.4 \
			   -overlay_value_step 10.10.10.2,10.10.10.3,10.10.10.4 \
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
				-counter_start 10.10.10.5 \
				-counter_step 0.0.1.0 \
				-nest_step 0.1.0.0 \
				-nest_enabled 1 \
				-overlay_value 10.10.10.5,10.10.10.6,10.10.10.7 \
				-overlay_value_step 10.10.10.5,10.10.10.6,10.10.10.7 \
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
			   -counter_start 10.10.10.5 \
			   -overlay_value 10.10.10.5,10.10.10.6,10.10.10.7 \
			   -overlay_value_step 10.10.10.5,10.10.10.6,10.10.10.7 \
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
				-counter_start 10.10.10.2 \
				-counter_step 0.0.1.0 \
				-nest_step 0.1.0.0 \
				-nest_enabled 1 \
				-overlay_value 10.10.10.2,10.10.10.3,10.10.10.4 \
				-overlay_value_step 10.10.10.2,10.10.10.3,10.10.10.4 \
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

# Create IGMP Host
set igmpHostHandleStatus [::ixiangpf::emulation_igmp_config \
			-handle $topo1Dg1Ipv4 \
			-mode create \
			-name IGMP_HOST \
			-ip_router_alert 1 \
			-max_response_control 0 \
			-group_query 1 \
			-unsolicited_response_mode 0 \
			-igmp_version v3 \
			-join_leave_multiplier 1 \
			-general_query 1 \
			-unsolicited_report_interval 120 \
			]
puts "\nigmpHosthandle: [KeylPrint igmpHostHandleStatus]\n"
set igmpHostHandle [keylget igmpHostHandleStatus igmp_host_handle]

# Create the IGMP Host Groups to join
set igmpHostGroupAddrStatus [::ixiangpf::multivalue_config \
				   -pattern single_value \
				   -nest_owner $topology1(portHandle) \
				   -nest_enabled 0 \
				   -single_value 228.0.0.1 \
				   -overlay_value_step 228.0.0.1,229.0.0.1,230.0.0.1 \
				   -overlay_value 228.0.0.1,229.0.0.1,230.0.0.1 \
				   -overlay_index 1,2,3 \
				  ]
    
puts "\ngroupAddrMultiValue: [KeylPrint igmpHostGroupAddrStatus]\n"
set igmpHostGroupAddr [keylget igmpHostGroupAddrStatus multivalue_handle]


# Make the IGMP Host group active
set igmpHostGroupActiveStatus [::ixiangpf::multivalue_config \
			      -pattern single_value \
			      -overlay_value 1,1,1 \
			      -overlay_index 1,2,3 \
			      -overlay_value_step 1,1,1 \
			      -single_value 0 \
			     ]
puts "\ngroupAddrActiveMultiValue2: [KeylPrint igmpHostGroupActiveStatus]\n"
set igmpHostGroupActive [keylget igmpHostGroupActiveStatus multivalue_handle]

# Make it all happen here
set igmpGroupConfig [::ixiangpf::emulation_multicast_group_config \
			 -mode create \
			 -active $igmpHostGroupActive \
			 -num_groups 1 \
			 -ip_addr_start $igmpHostGroupAddr \
			 -ip_addr_step 1.0.0.0 \
			 ]
puts "\nigmpGroupConfig: [KeylPrint igmpGroupConfig]\n"
# /igmpMcastIPv4GroupList:HLAPI0
set igmpGroupAddrHandle [keylget igmpGroupConfig multicast_group_handle]


# Configure the IGMP Host Source Groups
set sourceGroupAddressesStatus [::ixiangpf::multivalue_config \
			     -pattern single_value \
			     -nest_owner $topology1(portHandle) \
			     -nest_enabled 0 \
			     -single_value 1.0.0.1 \
			     -overlay_value 10.10.10.2,10.10.10.3,10.10.10.4 \
			     -overlay_value_step 10.10.10.2,10.10.10.3,10.10.10.4 \
			     -overlay_index 1,2,3 \
			   ]
puts "\nsource Group addresses: [KeylPrint sourceGroupAddressesStatus]\n"
set sourceGroupAddresses [keylget sourceGroupAddressesStatus multivalue_handle]

set sourceGroupAddrActiveStatus [::ixiangpf::multivalue_config \
			      -pattern single_value \
			      -overlay_value 1,1,1 \
			      -overlay_index 1,2,3 \
			      -overlay_value_step 1,1,1 \
			      -single_value 0 \
			     ]
puts "\nsourceGroupAddrActiveStatus: [KeylPrint sourceGroupAddrActiveStatus]\n"
set sourceGroupActive [keylget sourceGroupAddrActiveStatus multivalue_handle]


# Make it all happen here
set srcGroupAddrHandleStatus [::ixiangpf::emulation_multicast_source_config \
				     -mode create \
				     -ip_addr_start $sourceGroupAddresses \
				     -ip_addr_step 1.0.0.0 \
				     -num_sources 1 \
				     -active $sourceGroupActive \
				     ]
puts "\nsourceGroupAddrHandleStatus: [KeylPrint srcGroupAddrHandleStatus]\n"

set igmpSrcGroupAddrHandle [keylget srcGroupAddrHandleStatus multicast_source_handle]


set igmpHostEmulationStatus [::ixiangpf::emulation_igmp_group_config \
				 -mode create \
				 -group_pool_handle  $igmpGroupAddrHandle \
				 -session_handle     $igmpHostHandle \
				 -source_pool_handle $igmpSrcGroupAddrHandle \
				]
puts "\nigmpHostEmulationStatus::  [KeylPrint igmpHostEmulationStatus]\n"


set igmpQuerierStatus [::ixiangpf::emulation_igmp_querier_config \
			   -handle $topo2Dg1Ipv4 \
			   -mode create \
			   -ip_router_alert 1\
			   -support_older_version_querier 1 \
			   -name IGMP_Querier \
			   -specific_query_response_interval 1000 \
			   -general_query_response_interval 1000 \
			   -robustness_variable 2 \
			   -startup_query_count 2 \
			   -igmp_version v2 \
			   -discard_learned_info 0 \
			   -support_older_version_host 1 \
			   -active 1 \
			   -query_interval 125 \
			   -specific_query_transmission_count 2 \
			   -support_election 1 \
			   ]
puts "\nigmpQuerierStatus:: [KeylPrint igmpQuerierStatus]\n"
set igmpQuerierHandle [keylget igmpQuerierStatus igmp_querier_handle]
# igmpQuerierStatus:: status: 1
#igmp_querier_handle: /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1
#igmp_querier_handles: /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:1 /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:2 /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:	

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

if {[VerifyProtocolSessionStatusUpNgpfHlt $igmpQuerierHandle] == 1} {
    exit
}

#puts "Starting igmp host and querier ..."
#StartIgmpEmulationNgpfHlt "$igmpHostHandle $igmpQuerierHandle"

set querierLearnedInfo [GetIgmpQuerierLearnedInfoNgpfHlt $igmpQuerierHandle]

puts "\nQuerier Learned Info:\n\n[KeylPrint querierLearnedInfo]\n"


# Retrieve IGMP querier stats
puts "Retrieve aggregate stats"
set querierAggregatedStats [GetIgmpQuerierAggregatedStatsNgpfHlt $igmpQuerierHandle]

puts "\nQuerierAggregatedStats:\n[KeylPrint querierAggregatedStats]\n"

# Querier Aggregated Stats: /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1 = {aggregate {{status started} {sessions_total 1} {sessions_up 1} {sessions_down 0} {sessions_notstarted 0}}}


#Querier Learned Info: /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:1 = {learned_info {{{"IGMP Querier" "1/1/2" "Interface-IP - 100.1.0.1"} {{id {"IGMP Querier" "1/1/2" "Interface-IP - 100.1.0.1"}} {{Querier Working Version} {v2 v2 v2 v2 v2}} {{Elected Querier Address} {100.1.0.1 100.1.0.1 100.1.0.1 100.1.0.1 100.1.0.1}} {{Group Address} {228.0.0.2 228.0.0.1 228.0.0.4 228.0.0.3 228.0.0.5}} {{Group Timer (sec)} {259 259 259 259 259}} {{Filter Mode} {N/A N/A N/A N/A N/A}} {{Compatibility Mode} {v2 v2 v2 v2 v2}} {{Compatibility Timer (sec)} {0 0 0 0 0}} {{Source Address} {removePacket[N/A] removePacket[N/A] removePacket[N/A] removePacket[N/A] removePacket[N/A]}} {{Source Timer (sec)} {0 0 0 0 0}}}}}}	


# This is example on how to select the receiving multicast group
# Note: 
#    - The amount of 'none' needs to be same amount of igmp host groups for -emulation_multicast_dst_handle_type
# -emulation_multicast_dst_handle [list [list 228.0.0.1/0.0.0.0/1 229.0.0.1/0.0.0.0/0 230.0.0.1/0.0.0.0/1]]
# -emulation_multicast_dst_handle_type [list [list none none none]]
#
# This is example on how to send to all multicast groups
# -emulation_multicast_dst_handle [list [list all_multicast_ranges]]
# -emulation_multicast_dst_handle_type [list none]

set trafficItem1 [::ixia::traffic_config \
		      -mode create \
		      -endpointset_count 1 \
		      -circuit_endpoint_type ipv4 \
		      -emulation_src_handle $deviceGroup(topo1,groupHandle) \
		      -emulation_dst_handle [list [list]] \
		      -emulation_multicast_dst_handle [list [list 228.0.0.1/0.0.0.0/1 229.0.0.1/0.0.0.0/0 230.0.0.1/0.0.0.0/1]] \
		      -emulation_multicast_dst_handle_type [list [list none none none]] \
		      -track_by  "trackingenabled0 flowGroup0" \
		      -name "IgmpHostAndQuerier" \
		      -bidirectional 0 \
		      -rate_percent 10 \
		      -pkts_per_burst 10000 \
		      -transmit_mode single_burst \
		      -frame_size 100 \
		      -allow_self_destined 1 \
		     ]

puts "\nTrafficItemStatus:\n[KeylPrint trafficItem1]\n"

# IMPORTANT NOTES
#   If there is only one endpoint, then only one [list] inside a list.
#     -emulation_src_handle [list [list]] or {{}}
#     -emulation_dst_handle [list [list]] or {{}}
#   If there are three endpoints, then 3 [list[ inside a list.
#     [list [list][list][list]] or { {} {} {} }
# 
# As for the array keys. Each endpoint uses the same key name
#

# /topology:1/deviceGroup:1/ethernet:1/ipv4:1
set srcPortHandle(EndpointSet-1) $deviceGroup(topo1,groupHandle)
set srcPortStart(EndpointSet-1)  1
set srcPortCount(EndpointSet-1)  1
set srcIntStart(EndpointSet-1)   3
set srcIntCount(EndpointSet-1)   1

# /topology:2/deviceGroup:1/ethernet:1/ipv4:1
set dstPortHandle(EndpointSet-1) $deviceGroup(topo2,groupHandle)
set dstPortStart(EndpointSet-1)  1
set dstPortCount(EndpointSet-1)  1
set dstIntStart(EndpointSet-1)   2 ;# Selecting ip host start at 1.1.1.7
set dstIntCount(EndpointSet-1)   2 ;# Ending at ip host 1.1.1.8 because the count = 2

RegenerateTrafficItems
StartTrafficHlt
after 10000

set stats [GetStats]

puts "\n[KeylPrint stats]"

ixNet disconnect
exit


# More samples ...

##############################################################################
#                    Stop IGMP hosts and queriers                            #
##############################################################################

puts "Stopping host and querier. Wait for 60 sec then."
StopIgmpEmulationNgpfHlt "$igmpHostHandle $igmpQuerierHandle"

##############################################################################
#                           Delete host                                      #
##############################################################################

set igmp_status [::ixiangpf::emulation_igmp_config          \
        -mode                  delete                       \
        -handle	               $igmpHostHandle           \
]

##############################################################################
#                           Delete querier                                   #
##############################################################################
set igmp_status [::ixiangpf::emulation_igmp_querier_config      \
        -mode                  delete                           \
        -handle	               $igmpQuerierHandle            \
]

set test_name IGMP_host_querier_operations_with_mcast_groups
return "SUCCESS - $test_name - [clock format [clock seconds]]"
