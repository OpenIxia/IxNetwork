#!/usr/local/python2.7.6/bin/python2.7

# Description:
# 
#    A sample BGP script using high level APIs.
#      - Create two Topologies.
#      - Create BGP network advertising routes.
#      - Start all protocols.
#      - Verify ARP.
#      - Verify BGP sessions.
#      - Create Traffic Item.
#           - Endpoints = Network advertising routes from Topology1 to Topology2.
#      - Start traffic.
#      - Get stats.

import sys, os
import time, re
import pprint

#from SharedIxiaNgpf import *
import IxN_Api

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError

ixia_tcl = IxiaTcl()
ixia_hlt = IxiaHlt(ixia_tcl)
ixia_ngpf = IxiaNgpf(ixia_hlt)
ixNet = ixia_ngpf.ixnet ;# For low level Python API commands

chassis_ip = '192.168.70.10'
ixnetwork_tcl_server = '192.168.70.127'
port_list = '1/1 2/1'
port_1 = '1/1/1'
port_2 = '1/2/1'


def VerifyProtocolSessionStatusUpNgpfHlPy(protocolHandleList, totalTime=60):
    '''
    protocolHandleList: One or more protocol handles in a list
                        to verify for sessions status 'UP'.
    
    Protocol handle example:
                     /topology:1/deviceGroup:1/ethernet:1/ipv4:1
                     /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1
    '''
    for eachProtocolSessionToVerify in protocolHandleList:
        for timer in range(1, totalTime+1):
            sessionStatus = ixia_ngpf.protocol_info(
                handle = eachProtocolSessionToVerify,
                mode = 'aggregate'
                )

            currentSessionUp = sessionStatus[eachProtocolSessionToVerify]['aggregate']['sessions_up']
            totalSessions = sessionStatus[eachProtocolSessionToVerify]['aggregate']['sessions_total']

            print '\nVerifying protocol sessions', eachProtocolSessionToVerify
            print '\t%s/%s: CurrentSessionUp:%s   TotalSessions:%s\n' % (timer, totalTime, currentSessionUp, totalSessions)

            if timer < totalTime and currentSessionUp != totalSessions:
                time.sleep(1)
                continue

            if timer < totalTime and currentSessionUp == totalSessions:
                break

            if timer == totalTime and currentSessionUp != totalSessions:
                print '\nError: It has been %s seconds and total sessions are not all UP. ' % timer
                return 1

def print_dict(obj, nested_level=0, output=sys.stdout):
    """
    Print each dict key with indentions for readability.
    """
    spacing = '   '
    if type(obj) == dict:
        print >> output, '%s' % ((nested_level) * spacing)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                print_dict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % ((nested_level + 1) * spacing, k, v)

        print >> output, '%s' % (nested_level * spacing)
    elif type(obj) == list:
        print >> output, '%s[' % ((nested_level) * spacing)
        for v in obj:
            if hasattr(v, '__iter__'):
                print_dict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % ((nested_level) * spacing)
    else:
        print >> output, '%s%s' % (nested_level * spacing, obj)


def ConfigMultivalueNgpfHlt(**kwargs):
    print '\nConfigMultivalueNgpfHlt:', kwargs
    multivalue = ixia_ngpf.multivalue_config(**kwargs)
    print_dict(multivalue)
    if multivalue['status'] != '1':
        print '\nConfigMultivalueHlt: Failed'
        return 0

    return multivalue['multivalue_handle']


def ConfigBgpEmulationNgpfHlt(**kwargs):
    print '\nConfigBgpEmulationNgpfHlt:', kwargs
    bgpEmulation = ixia_ngpf.emulation_bgp_config(**kwargs)
    print_dict(bgpEmulation)
    if bgpEmulation['status'] != '1':
        print '\nConfigBgpEmulationNgpfHlt: Failed'
        return 0

    print "\nConfigBgpEmulationNgpfHlt status..."
    print_dict(bgpEmulation)
    # status: 1
    # ospfv2_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1
    return bgpEmulation


def ConfigNetworkGroupNgpfHlt(**kwargs):
    print '\nConfigNetworkGroupNgpfHlt:', kwargs
    networkGroup = ixia_ngpf.network_group_config(**kwargs)

    print_dict(networkGroup)
    if networkGroup['status'] != '1':
        print '\nConfigNetworkGroupNgpfHlt: Failed:'
        return 0

    # status: 1
    # ipv4_prefix_pools_handle: /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1
    # network_group_handle: /topology:1/deviceGroup:1/networkGroup:1
    return networkGroup

connect_status = ixia_ngpf.connect(
    reset = 1,
    device = chassis_ip,
    port_list = port_list,
    ixnetwork_tcl_server = ixnetwork_tcl_server,
    tcl_server = chassis_ip
    )
print_dict(connect_status)
if connect_status['status'] != '1':
    print '\nError: Failed to connect\n'

port_handle = connect_status['vport_list']

print '\nport handles', port_handle
print 'port1', port_1
print 'port2', port_2


topology_1_status = ixia_ngpf.topology_config(
    topology_name = 'Topology 1',
    port_handle = port_1
    )

if topology_1_status ['status'] != '1':
    print '\nError: Failed to create Topology\n'
    sys.exit()

# /topology:1
topology_1_handle = topology_1_status['topology_handle']


topology_2_status = ixia_ngpf.topology_config(
    topology_name = 'Topology 2',
    port_handle = port_2
    )

if topology_2_status ['status'] != '1':
    print '\nError: Failed to create Topology\n'
    sys.exit()

# /topology:2
topology_2_handle = topology_2_status['topology_handle']


device_group_1_status = ixia_ngpf.topology_config(
    topology_handle = topology_1_handle,
    device_group_name = 'Basic L3-1',
    device_group_multiplier = '3',
    device_group_enabled = '1'
    )

if device_group_1_status['status'] != '1':
    print '\nError: Failed to create Device Group\n'
    sys.exit()

# /topology:1/deviceGroup:1
device_group_1_handle = device_group_1_status['device_group_handle']


device_group_2_status = ixia_ngpf.topology_config(
    topology_handle = topology_2_handle,
    device_group_name = 'Basic L3-2',
    device_group_multiplier = '3',
    device_group_enabled = '1'
    )

if device_group_2_status['status'] != '1':
    print '\nError: Failed to create Device Group\n'
    sys.exit()

# /topology:1/deviceGroup:2
device_group_2_handle = device_group_2_status['device_group_handle']

ethernet_status = ixia_ngpf.interface_config(
    mode = 'config',
    protocol_handle = device_group_1_handle,
    mtu = '1500',
    src_mac_addr = '00:01:01:01:00:01',
    src_mac_addr_step = '00:00:00:00:00:01',
    intf_ip_addr = '1.1.1.1',
    intf_ip_addr_step = '0.0.0.1',
    netmask = '255.255.255.0',
    gateway = '1.1.1.4',
    gateway_step = '0.0.0.0',
    arp_send_req = '1',
    arp_req_retries = '3',
    ipv4_resolve_gateway = '1',
    vlan = '0',
    vlan_id = '101',
    vlan_id_step = '1',
    vlan_id_count = '1',
    vlan_user_priority = '0',
    vlan_user_priority_step = '0'
    )
if ethernet_status['status'] != '1':
    print '\nError: Failed to configure Device Group on port: ', port_1
    print '\n', ethernet_status
    sys.exit()

print_dict(ethernet_status)

topo1EthernetHandle = ethernet_status['ethernet_handle']
topo1Ipv4Handle = ethernet_status['ipv4_handle']
topo1InterfaceHandles = ethernet_status['interface_handle']

ethernet_status = ixia_ngpf.interface_config(
    mode = 'config',
    protocol_handle = device_group_2_handle,
    mtu = '1500',
    src_mac_addr = '00:01:01:02:00:01',
    src_mac_addr_step = '00:00:00:00:00:01',
    intf_ip_addr = '1.1.1.4',
    intf_ip_addr_step = '0.0.0.1',
    gateway = '1.1.1.1',
    gateway_step = '0.0.0.0',
    arp_send_req = '1',
    arp_req_retries = '3',
    ipv4_resolve_gateway = '1',
    vlan = '0',
    vlan_id = '101',
    vlan_id_step = '1',
    vlan_id_count = '1',
    vlan_user_priority = '0',
    vlan_user_priority_step = '0'
    )
if ethernet_status['status'] != '1':
    print '\nError: Failed to configure Device Group on port: ', port_2
    print '\n', ethernet_status
    sys.exit()

print_dict(ethernet_status)

topo2EthernetHandle = ethernet_status['ethernet_handle']
topo2Ipv4Handle = ethernet_status['ipv4_handle']
topo2InterfaceHandles = ethernet_status['interface_handle']


bgp1RemoteIpMultiValue = ConfigMultivalueNgpfHlt(
    pattern                 = "single_value",
    single_value            = "1.1.1.4",
    nest_step               = "0.0.0.1",
    nest_owner              = '%s' % (topology_1_handle),
    nest_enabled            = "0",
    overlay_value           = "1.1.1.4,1.1.1.5,1.1.1.6",
    overlay_value_step      = "1.1.1.4,1.1.1.5,1.1.1.6",
    overlay_index           = "1,2,3",
    overlay_index_step      = "0,0,0",
    )

bgp2RemoteIpMultiValue = ConfigMultivalueNgpfHlt(
    pattern                 = "single_value",
    single_value            = "1.1.1.1",
    nest_step               = "0.0.0.1",
    nest_owner              = '%s' % (topology_2_handle),
    nest_enabled            = "0",
    overlay_value           = "1.1.1.1,1.1.1.2,1.1.1.3",
    overlay_value_step      = "1.1.1.1,1.1.1.2,1.1.1.3",
    overlay_index           = "1,2,3",
    overlay_index_step      = "0,0,0",
    )

bgpIpv4PeerStatus = ConfigBgpEmulationNgpfHlt(
    mode = "enable",
    active = "1",
    handle = topo1Ipv4Handle,
    remote_ip_addr = bgp1RemoteIpMultiValue,
    )

bgpIpv4PeerHandle1 = bgpIpv4PeerStatus['bgp_handle']

bgpIpv4PeerStatus = ConfigBgpEmulationNgpfHlt(
    mode = "enable",
    active = "1",
    handle = topo2Ipv4Handle,
    remote_ip_addr = bgp2RemoteIpMultiValue,
    )

bgpIpv4PeerHandle2 = bgpIpv4PeerStatus['bgp_handle']

'''
bgpIpv4PeerHandle:
   status: 1
   handle: /topology:2/deviceGroup:1/ethernet:1/ipv4:1/bgpIpv4Peer:1/item:1
           /topology:2/deviceGroup:1/ethernet:1/ipv4:1/bgpIpv4Peer:1/item:2
           /topology:2/deviceGroup:1/ethernet:1/ipv4:1/bgpIpv4Peer:1/item:3
   bgp_handle: /topology:2/deviceGroup:1/ethernet:1/ipv4:1/bgpIpv4Peer:1
'''

bgp1NetworkGroupMultiValue = ConfigMultivalueNgpfHlt(
    pattern                = "counter",
    counter_start          = "200.1.0.0",
    counter_step           = "0.1.0.0",
    counter_direction      = "increment",
    nest_step              = "0.0.0.1,0.1.0.0",
    nest_owner             = '%s,%s' % (device_group_1_handle, topology_1_handle),
    nest_enabled           = "0,1",
)

bgp1NetworkGroup = ConfigNetworkGroupNgpfHlt(
    protocol_handle                      = device_group_1_handle,
    protocol_name                        = "BGP_1_Network_Group1",
    multiplier                           = "1",
    enable_device                        = "1",
    connected_to_handle                  = topo1EthernetHandle,
    type                                 = "ipv4-prefix",
    ipv4_prefix_network_address          = bgp1NetworkGroupMultiValue,
    ipv4_prefix_length                   = "24",
    ipv4_prefix_number_of_addresses      = "1",
)

networkGroup_1_handle = bgp1NetworkGroup['network_group_handle']
ipv4PrefixPools_1_handle = bgp1NetworkGroup['ipv4_prefix_pools_handle']

bgp2NetworkGroupMultiValue = ConfigMultivalueNgpfHlt(
    pattern                = "counter",
    counter_start          = "201.1.0.0",
    counter_step           = "0.1.0.0",
    counter_direction      = "increment",
    nest_step              = "0.0.0.1,0.1.0.0",
    nest_owner             = '%s,%s' % (device_group_2_handle, topology_2_handle),
    nest_enabled           = "0,1",
)

bgp2NetworkGroup = ConfigNetworkGroupNgpfHlt(
    protocol_handle                      = device_group_2_handle,
    protocol_name                        = "BGP_2_Network_Group1",
    multiplier                           = "1",
    enable_device                        = "1",
    connected_to_handle                  = topo2EthernetHandle,
    type                                 = "ipv4-prefix",
    ipv4_prefix_network_address          = bgp2NetworkGroupMultiValue,
    ipv4_prefix_length                   = "24",
    ipv4_prefix_number_of_addresses      = "1",
)

networkGroup_2_handle = bgp2NetworkGroup['network_group_handle']
ipv4PrefixPools_2_handle = bgp1NetworkGroup['ipv4_prefix_pools_handle']


'''
ConfigNetworkGroupNgpfHlt: {
   status: 1
   ipv4_prefix_pools_handle: /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1
   network_group_handle: /topology:1/deviceGroup:1/networkGroup:1
'''

_result_ = ixia_ngpf.test_control(action='start_all_protocols')
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', _result_)

# Verify ARP
if VerifyProtocolSessionStatusUpNgpfHlPy([topo1Ipv4Handle, topo2Ipv4Handle]) == 1:
    #print "Waiting for 45 seconds"
    #time.sleep(45)
    sys.exit()

print "Verifying BGP aggregated statistics on Port1"               
protostats = ixia_ngpf.emulation_bgp_info(\
    handle = bgpIpv4PeerHandle1,
    mode   = 'stats')
if protostats['status'] != IxiaHlt.SUCCESS:
    print '\nError:', print_dict(protostats)

print_dict(protostats)

print "Verifying BGP aggregated statistics on Port2"               
protostats = ixia_ngpf.emulation_bgp_info(\
    handle = bgpIpv4PeerHandle2,
    mode   = 'stats')
if protostats['status'] != IxiaHlt.SUCCESS:
    print '\nError:', print_dict(protostats)

print_dict(protostats)

time.sleep(3)
traffic_status = ixia_ngpf.traffic_config(
    mode = 'create',
    name = 'Traffic_Item_1',
    emulation_src_handle = networkGroup_1_handle,
    emulation_dst_handle = networkGroup_2_handle,
    transmit_mode = 'single_burst',
    pkts_per_burst = '50000',
    frame_size = '256',
    rate_percent = '10',
    src_dest_mesh = 'one_to_one',
    route_mesh = 'one_to_one',
    bidirectional = '0',
    allow_self_destined = '0',
    circuit_endpoint_type = 'ipv4',
    track_by = 'flowGroup0 sourceDestValuePair0',
    l3_protocol = 'ipv4'
    )

if traffic_status['status'] != '1':
    print '\nError: Failed to configure Traffic Item.\n'
    print traffic_status
    sys.exit()

print '\nWait 10 seconds for Traffic Item to set ...'
time.sleep(10)

print '\nStarting traffic ...'
traffic_control_status = ixia_ngpf.traffic_control(action = 'run')

if traffic_control_status['status'] != '1':
    print '\nError: Failed to start traffic.\n'
    print traffic_control
    sys.exit()

print_dict(traffic_control_status)

time.sleep(15)

print '\ngetList: ', ixNet.getList(ixNet.getRoot()+'traffic', 'trafficItem')

traffic_stats = ixia_ngpf.traffic_stats(mode = 'flow')

if traffic_stats['status'] != '1':
    print '\nError: Failed to get traffic flow stats.\n'
    print traffic_stats
    sys.exit()

print_dict(traffic_stats)

print '\nStopping All protocols ...'
ixia_ngpf.test_control(action = 'stop_all_protocols')
ixia_ngpf.cleanup_session(reset='0')
