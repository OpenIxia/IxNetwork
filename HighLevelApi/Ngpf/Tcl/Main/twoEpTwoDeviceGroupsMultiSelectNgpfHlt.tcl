#!/opt/ActiveTcl-8.5/bin/tclsh

# Two topology groups, two device groups for each topology group
# Two endpoints and able to select which ip addresses.

package req Ixia

source ~/MyIxiaWork/IxNet_tclApi.tcl

set ixiaChassisIp 10.219.117.101
set ixNetworkTclServerIp 10.219.117.103
set userName hgee
set portList [list 1/1 1/2]
set port1 1/1/1
set port2 1/1/2

#EnableHltDebug

set connect(-reset) 1
set connect(-device) $ixiaChassisIp
set connect(-port_list) $portList
set connect(-ixnetwork_tcl_server) $ixNetworkTclServerIp
set connect(-tcl_server) $ixiaChassisIp
set connect(-username) $userName

set connectStatus [ConnectToIxiaNgpfHlt ::connect]
if {$connectStatus == 1} {
    exit
}

# 1> Create new Topology Group
set topology1(-topology_name)  "IPv4 Topology Tx-1"
set topology1(-port_handle) [list [list $port1]]

set topology2(-topology_name)  "IPv4 Topology Rx-1"
set topology2(-port_handle) [list [list $port2]]

set topology1Keys [CreateNewTopologyNgpfHlt ::topology1]
set topology2Keys [CreateNewTopologyNgpfHlt ::topology2]

set topology1(portHandle) [keylget topology1Keys topology_handle]
set topology2(portHandle) [keylget topology2Keys topology_handle]

# 2> Create Device Group(s) to a Topology Group
#    
set deviceGroup1(topo1,-topology_handle) $topology1(portHandle)
set deviceGroup1(topo1,-device_group_multiplier) 5
set deviceGroup1(topo1,-device_group_name) "Ipv4 Tx-1"
set deviceGroup1(topo1,-device_group_enabled) 1
set deviceGroup1(topo1,protocolName) "Ethernet"

set deviceGroup2(topo2,-topology_handle) $topology2(portHandle)
set deviceGroup2(topo2,-device_group_multiplier) 5
set deviceGroup2(topo2,-device_group_name) "Ipv4 Rx-1"
set deviceGroup2(topo2,-device_group_enabled) 1
set deviceGroup2(topo2,protocolName) "Ethernet"

set deviceGroup3(topo1,-topology_handle) $topology1(portHandle)
set deviceGroup3(topo1,-device_group_multiplier) 5
set deviceGroup3(topo1,-device_group_name) "Ipv4 Rx-2"
set deviceGroup3(topo1,-device_group_enabled) 1
set deviceGroup3(topo1,protocolName) "Ethernet"

set deviceGroup4(topo2,-topology_handle) $topology2(portHandle)
set deviceGroup4(topo2,-device_group_multiplier) 5
set deviceGroup4(topo2,-device_group_name) "Ipv4 Tx-2"
set deviceGroup4(topo2,-device_group_enabled) 1
set deviceGroup4(topo2,protocolName) "Ethernet"

set topo1DeviceGroup1Keys [CreateNewDeviceGroupNgpfHlt ::deviceGroup1]
set topo2DeviceGroup2Keys [CreateNewDeviceGroupNgpfHlt ::deviceGroup2]
set topo1DeviceGroup3Keys [CreateNewDeviceGroupNgpfHlt ::deviceGroup3]
set topo2DeviceGroup4Keys [CreateNewDeviceGroupNgpfHlt ::deviceGroup4]

set deviceGroup1(topo1,groupHandle) [keylget topo1DeviceGroup1Keys device_group_handle]
set deviceGroup2(topo2,groupHandle) [keylget topo2DeviceGroup2Keys device_group_handle]
set deviceGroup3(topo1,groupHandle) [keylget topo1DeviceGroup3Keys device_group_handle]
set deviceGroup4(topo2,groupHandle) [keylget topo2DeviceGroup4Keys device_group_handle]

set portConfig1(-mtu)                     1500
set portConfig1(-protocol_handle)         $deviceGroup1(topo1,groupHandle)
set portConfig1(-ipv4_resolve_gateway)    1
set portConfig1(-ipv4_manual_gateway_mac) 00.00.00.00.00.01
set portConfig1(-gateway)                 1.1.1.6
set portConfig1(-gateway_step)            0.0.0.0
set portConfig1(-intf_ip_addr)            1.1.1.1
set portConfig1(-intf_ip_addr_step)       0.0.0.1
set portConfig1(-netmask)                 255.255.255.0
set portConfig1(-src_mac_addr)            00:01:01:01:00:01
set portConfig1(-src_mac_addr_step)       00:00:00:00:00:01
set portConfig1(-vlan)                    0 ;# To enable vlan, use 1
set portConfig1(-vlan_id)                 100
set portConfig1(-vlan_user_priority)      3
set portConfig1(-vlan_id_count)           5
set portConfig1(-vlan_id_step)            1
set portConfig1(-vlan_user_priority_step) 0
set portConfig1(-arp_send_req) 1

set portConfig2(-mtu)                     1500 
set portConfig2(-protocol_handle)         $deviceGroup2(topo2,groupHandle)
set portConfig2(-ipv4_resolve_gateway)    1
set portConfig2(-ipv4_manual_gateway_mac) 00.00.00.00.00.01
set portConfig2(-gateway)                 1.1.1.1
set portConfig2(-gateway_step)            0.0.0.0
set portConfig2(-intf_ip_addr)            1.1.1.6
set portConfig2(-intf_ip_addr_step)       0.0.0.1
set portConfig2(-netmask)                 255.255.255.0
set portConfig2(-src_mac_addr)            00:01:01:02:00:01
set portConfig2(-src_mac_addr_step)       00:00:00:00:00:01
set portConfig2(-vlan)                    0 ;# To enable vlan, use 1
set portConfig2(-vlan_id)                 100
set portConfig2(-vlan_user_priority)      3
set portConfig2(-vlan_id_count)           5
set portConfig2(-vlan_id_step)            1
set portConfig2(-vlan_user_priority_step) 0
set portConfig2(-arp_send_req) 1

set portConfig3(-mtu)                     1500 
set portConfig3(-protocol_handle)         $deviceGroup3(topo1,groupHandle)
set portConfig3(-ipv4_resolve_gateway)    1
set portConfig3(-ipv4_manual_gateway_mac) 00.00.00.00.00.01
set portConfig3(-gateway)                 1.1.1.16
set portConfig3(-gateway_step)            0.0.0.0
set portConfig3(-intf_ip_addr)            1.1.1.11
set portConfig3(-intf_ip_addr_step)       0.0.0.1
set portConfig3(-netmask)                 255.255.255.0
set portConfig3(-src_mac_addr)            00:01:01:01:00:0b
set portConfig3(-src_mac_addr_step)       00:00:00:00:00:01
set portConfig3(-vlan)                    0 ;# To enable vlan, use 1
set portConfig3(-vlan_id)                 100
set portConfig3(-vlan_user_priority)      3
set portConfig3(-vlan_id_count)           5
set portConfig3(-vlan_id_step)            1
set portConfig3(-vlan_user_priority_step) 0
set portConfig3(-arp_send_req) 1

set portConfig4(-mtu)                     1500 
set portConfig4(-protocol_handle)         $deviceGroup4(topo2,groupHandle)
set portConfig4(-ipv4_resolve_gateway)    1
set portConfig4(-ipv4_manual_gateway_mac) 00.00.00.00.00.01
set portConfig4(-gateway)                 1.1.1.11
set portConfig4(-gateway_step)            0.0.0.0
set portConfig4(-intf_ip_addr)            1.1.1.16
set portConfig4(-intf_ip_addr_step)       0.0.0.1
set portConfig4(-netmask)                 255.255.255.0
set portConfig4(-src_mac_addr)            00:01:01:02:00:a0
set portConfig4(-src_mac_addr_step)       00:00:00:00:00:01
set portConfig4(-vlan)                    0 ;# To enable vlan, use 1
set portConfig4(-vlan_id)                 100
set portConfig4(-vlan_user_priority)      3
set portConfig4(-vlan_id_count)           5
set portConfig4(-vlan_id_step)            1
set portConfig4(-vlan_user_priority_step) 0
set portConfig4(-arp_send_req) 1

set deviceGroup1Topo1Keys [PortConfigProtocolIntNgpfHlt ::portConfig1]
set deviceGroup2Topo2Keys [PortConfigProtocolIntNgpfHlt ::portConfig2]
set deviceGroup3Topo1Keys [PortConfigProtocolIntNgpfHlt ::portConfig3]
set deviceGroup4Topo2Keys [PortConfigProtocolIntNgpfHlt ::portConfig4]

set deviceGroup1Topo1 [keylget deviceGroup1Topo1Keys ipv4_handle]
set deviceGroup2Topo2 [keylget deviceGroup2Topo2Keys ipv4_handle]
set deviceGroup3Topo1 [keylget deviceGroup3Topo1Keys ipv4_handle]
set deviceGroup4Topo2 [keylget deviceGroup4Topo2Keys ipv4_handle]

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
set srcPortHandle(EndpointSet-1) [list $deviceGroup1Topo1 $deviceGroup1Topo1 $deviceGroup1Topo1 $deviceGroup3Topo1 $deviceGroup3Topo1 $deviceGroup3Topo1]
set srcPortStart(EndpointSet-1)  [list 1 1 1 1 1 1]
set srcPortCount(EndpointSet-1)  [list 1 1 1 1 1 1]
set srcIntStart(EndpointSet-1)   [list 1 3 5 1 2 3]
set srcIntCount(EndpointSet-1)   [list 1 1 1 1 1 1]

# /topology:2/deviceGroup:1/ethernet:1/ipv4:1
set dstPortHandle(EndpointSet-1)  $deviceGroup2Topo2 
set dstPortStart(EndpointSet-1)   1
set dstPortCount(EndpointSet-1)   1
set dstIntStart(EndpointSet-1)    1
set dstIntCount(EndpointSet-1)    5

set srcPortHandle(EndpointSet-2) [list $deviceGroup1Topo1 $deviceGroup1Topo1 $deviceGroup1Topo1 $deviceGroup3Topo1 $deviceGroup3Topo1 $deviceGroup3Topo1]
set srcPortStart(EndpointSet-2)  [list 1 1 1 1 1 1]
set srcPortCount(EndpointSet-2)  [list 1 1 1 1 1 1]
set srcIntStart(EndpointSet-2)   [list 1 3 4 5 4 3]
set srcIntCount(EndpointSet-2)   [list 1 1 1 1 1 1]

# /topology:2/deviceGroup:2/ethernet:1/ipv4:1
set dstPortHandle(EndpointSet-2) [list $deviceGroup2Topo2 $deviceGroup2Topo2 $deviceGroup2Topo2 $deviceGroup4Topo2 $deviceGroup4Topo2 $deviceGroup4Topo2]
set dstPortStart(EndpointSet-2)  [list 1 1 1 1 1 1]
set dstPortCount(EndpointSet-2)  [list 1 1 1 1 1 1]
set dstIntStart(EndpointSet-2)   [list 2 3 4 3 4 1]
set dstIntCount(EndpointSet-2)   [list 1 1 1 1 1 1]

set trafficItem1(-mode) create 
set trafficItem1(-endpointset_count) 2
set trafficItem1(-emulation_src_handle) {  { {} {} }   }
set trafficItem1(-emulation_dst_handle) {  { {} {} }   }
set trafficItem1(-emulation_scalable_src_handle)     ::srcPortHandle
set trafficItem1(-emulation_scalable_src_port_start) ::srcPortStart
set trafficItem1(-emulation_scalable_src_port_count) ::srcPortCount
set trafficItem1(-emulation_scalable_src_intf_start) ::srcIntStart
set trafficItem1(-emulation_scalable_src_intf_count) ::srcIntCount

set trafficItem1(-emulation_scalable_dst_handle)     ::dstPortHandle
set trafficItem1(-emulation_scalable_dst_port_start) ::dstPortStart
set trafficItem1(-emulation_scalable_dst_port_count) ::dstPortCount
set trafficItem1(-emulation_scalable_dst_intf_start) ::dstIntStart
set trafficItem1(-emulation_scalable_dst_intf_count) ::dstIntCount

set trafficItem1(-src_dest_mesh) one_to_one
set trafficItem1(-route_mesh) one_to_one
set trafficItem1(-bidirectional) 0
set trafficItem1(-allow_self_destined) 0
set trafficItem1(-name) Traffic_Item_1
set trafficItem1(-circuit_endpoint_type) ipv4 ;# To send only L2 traffic, use ethernet_vlan
set trafficItem1(-track_by) {trackingenabled0 sourceDestValuePair0}
set trafficItem1(-l3_protocol) ipv4

StartAllProtocolsHlt
set trafficItem1Keys [CreateTrafficItemHlt ::trafficItem1]

if {[VerifyArpNgpf] != 0}  {
    exit
}

RegenerateTrafficItems
StartTrafficHlt
after 15000

set stats [GetStatView]

puts "\n[KeylPrint stats]"
