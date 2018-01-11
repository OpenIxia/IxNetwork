#!/opt/ActiveTcl-8.5/bin/tclsh

package req Ixia

source ~/MyIxiaWork/NGPF/HLT/ixiaHltLib.tcl

set ixiaChassisIp 10.205.4.155
set ixNetworkTclServerIp 10.205.4.160
set userName hgee
set portList [list 1/3 1/4]
set port1 1/1/3
set port2 1/1/4


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
set deviceGroup1(topo1,-device_group_multiplier) 15000
set deviceGroup1(topo1,-device_group_name) "Ipv4 Tx-1"
set deviceGroup1(topo1,-device_group_enabled) 1
set deviceGroup1(topo1,protocolName) "Ethernet"

set deviceGroup2(topo2,-topology_handle) $topology2(portHandle)
set deviceGroup2(topo2,-device_group_multiplier) 15000
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

StartAllProtocolHlt
SendArpOnAllActiveIntNgpf

if {[VerifyArpNgpf] != 0}  {
    exit
}

RegenerateTrafficItems
StartTrafficHlt
after 15000

set stats [GetStatView]

puts "\n[KeylPrint stats]"
