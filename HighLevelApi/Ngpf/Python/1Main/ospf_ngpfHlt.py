#!/usr/local/python2.7.6/bin/python2.7

# By: Hubert Gee
# Sample script on Layer2/Layer3
#

import sys, os
import time, re

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError

ixia_tcl = IxiaTcl()
ixia_hlt = IxiaHlt(ixia_tcl)
ixia_ngpf = IxiaNgpf(ixia_hlt)
ixNet = ixia_ngpf.ixnet ;# For low level Python API commands


chassis_ip = '10.219.117.101'
ixnetwork_tcl_server = '10.219.117.103'
port_list = '1/1 1/2'
port_1 = '1/1/1'
port_2 = '1/1/2'

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


def CreateMultivalueNgpfHlPy(**kwargs):
    print '\nCreateMultivalueNgpfHlPy:', kwargs
    multivalue = ixia_ngpf.multivalue_config(**kwargs)
    print_dict(multivalue)
    if multivalue['status'] != '1':
        print '\nConfigMultivalueHlPy: Failed'
        return 0

    return multivalue['multivalue_handle']


def ConfigOspfEmulationNgpfHlPy(**kwargs):
    print '\nConfigOspfEmulationNgpfHlPy:', kwargs
    ospfEmulation = ixia_ngpf.emulation_ospf_config(**kwargs)
    print_dict(ospfEmulation)
    if ospfEmulation['status'] != '1':
        print '\nConfigOspfEmulationNgpfHlPy: Failed'
        return 0

    # status: 1
    # ospfv2_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1
    return ospfEmulation


def ConfigNetworkGroupNgpfHlPy(**kwargs):
    print '\nConfigNetworkGroupNgpfHlPy:', kwargs
    networkGroup = ixia_ngpf.network_group_config(**kwargs)

    print_dict(networkGroup)
    if networkGroup['status'] != '1':
        print '\nConfigNetworkGroupNgpfHlPy: Failed:'
        return 0

    # status: 1
    # ipv4_prefix_pools_handle: /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1
    # network_group_handle: /topology:1/deviceGroup:1/networkGroup:1
    return networkGroup


def ConfigOspfNetworkGroupNgpfHlPy(**kwargs):
    print '\nConfigOspfNetworkGroupNgpfHlPy:', kwargs
    ospfNetworkGroup = ixia_ngpf.emulation_ospf_network_group_config(**kwargs)
    print_dict(ospfNetworkGroup)
    if ospfNetworkGroup['status'] != '1':
        print '\nConfigOspfNetworkGroupNgpfHlPy: Failed'
        return 0

    # status: 1
    # ipv4_prefix_pools_handle: /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1
    # ipv4_prefix_interface_handle: /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/ospfRouteProperty:1
    # network_group_handle: /topology:1/deviceGroup:1/networkGroup:1
    return ospfNetworkGroup

def VerifyProtocolSessionStatusUpNgpfHlPy(protocolHandle, totalTime=60):
    for timer in range(1, totalTime+1):
        sessionStatus = ixia_ngpf.protocol_info(
            handle = protocolHandle,
            mode = 'aggregate'
            )

        currentSessionUp = sessionStatus[protocolHandle]['aggregate']['sessions_up']
        totalSessions = sessionStatus[protocolHandle]['aggregate']['sessions_total']

        print '\nVerifying protocol sessions:', protocolHandle
        print '\t%s/%s: CurrentSessionUp:%s   TotalSessions:%s\n' % (timer, totalTime, currentSessionUp, totalSessions)

        if timer < totalTime and currentSessionUp != totalSessions:
            time.sleep(1)
            continue
        
        if timer < totalTime and currentSessionUp == totalSessions:
            return 0

        if timer == totalTime and currentSessionUp != totalSessions:
            print '\nError: It has been %s seconds and total sessions are not all UP. ' % timer
            return 1


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
    gateway_step = '0.0.0.1',
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
    gateway_step = '0.0.0.1',
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

routerInteractiveMultivalue = CreateMultivalueNgpfHlPy(
    pattern = 'single_value',
    single_value = '1'
    )

print '\nrouterInteractiveMultivalue:', routerInteractiveMultivalue
# /multivalue:HLAPI0

ospfRouterIdTopo1Multivalue = CreateMultivalueNgpfHlPy(
    pattern = 'counter',
    counter_start = '1.1.1.1',
    counter_step = '0.0.0.1',
    counter_direction = 'increment',
    nest_step = '0.1.0.0',
    nest_owner = topology_1_handle,
    nest_enabled = '0',
    overlay_value = '1.1.1.1',
    overlay_value_step = '1.1.1.1',
    overlay_index = '1',
    overlay_index_step = '0',
    overlay_count = '1'
    )

print '\nospfRouterIdTopo1Multivalue !:', ospfRouterIdTopo1Multivalue
# /multivalue:HLAPI1

ospfRouterIdTopo2Multivalue = CreateMultivalueNgpfHlPy(
    pattern = 'counter',
    counter_start = '1.1.1.4',
    counter_step = '0.0.0.1',
    counter_direction = 'increment',
    nest_step = '0.1.0.0',
    nest_owner = topology_2_handle,
    nest_enabled = '0',
    overlay_value = '1.1.1.4',
    overlay_value_step = '1.1.1.4',
    overlay_index = '1',
    overlay_index_step = '0',
    overlay_count = '1'
    )

print '\nospfRouterIdTopo2Multivalue !!:', ospfRouterIdTopo2Multivalue
# /multivalue:HLAPI2

ospfEmulationTopo1 = ConfigOspfEmulationNgpfHlPy(
    mode = 'create',
    protocol_name = 'ospf-1',
    handle = topo1Ipv4Handle,
    router_id = ospfRouterIdTopo1Multivalue,
    router_id_step = '0.0.0.1',
    neighbor_router_id = '1.1.1.4',
    neighbor_router_id_step = '0.0.0.1',
    router_interface_active = routerInteractiveMultivalue,
    router_active = '1',
    network_type = 'broadcast',
    hello_interval = '10',
    dead_interval = '40',
    interface_cost = '10',
    graceful_restart_enable = '0',
    router_priority = '2',
    enable_fast_hello = '0',
    max_mtu = '1500',
    area_id = '0.0.0.0',
    area_id_type = 'ip',
    lsa_retransmit_time = '5',
    lsa_discard_mode = '0'
    )

ospfEmulationTopo1 = ospfEmulationTopo1['ospfv2_handle']
print '\nospf emulation topo1:', ospfEmulationTopo1
# /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1

ospfEmulationTopo2 = ConfigOspfEmulationNgpfHlPy(
    mode = 'create',
    protocol_name = 'ospf-2',
    handle = topo2Ipv4Handle,
    router_id = ospfRouterIdTopo2Multivalue,
    router_id_step = '0.0.0.1',
    neighbor_router_id = '1.1.1.1',
    neighbor_router_id_step = '0.0.0.1',
    router_interface_active = routerInteractiveMultivalue,
    router_active = '1',
    network_type = 'broadcast',
    hello_interval = '10',
    dead_interval = '40',
    interface_cost = '10',
    graceful_restart_enable = '0',
    router_priority = '2',
    enable_fast_hello = '0',
    max_mtu = '1500',
    area_id = '0.0.0.0',
    area_id_type = 'ip',
    lsa_retransmit_time = '5',
    lsa_discard_mode = '0'
    )

ospfEmulationTopo2 = ospfEmulationTopo2['ospfv2_handle']
print '\nospf emulation topo2:', ospfEmulationTopo2
# /topology:2/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1

designatedRouterTopo1Multivalue = CreateMultivalueNgpfHlPy(
    pattern = 'single_value',
    single_value = '1'
    )

designatedRouterTopo1 = ConfigOspfEmulationNgpfHlPy(
    mode = 'create',
    enable_dr_bdr = designatedRouterTopo1Multivalue,
    handle = '/globals'
)

print '\nDR topo1:', designatedRouterTopo1
# {'status': '1'}

designatedRouterTopo2Multivalue = CreateMultivalueNgpfHlPy(
    pattern = 'single_value',
    single_value = '1'
    )

designatedRouterTopo2 = ConfigOspfEmulationNgpfHlPy(
    mode = 'create',
    enable_dr_bdr = designatedRouterTopo2Multivalue,
    handle = '/globals'
)

print '\nDR topo2:', designatedRouterTopo2
# {'status': '1'}

topo1AdvertisingRoute = '100.1.1.1'
topo2AdvertisingRoute = '200.1.1.1'

routeRangeTopo1Multivalue = CreateMultivalueNgpfHlPy(
    pattern = 'counter',
    counter_start = topo1AdvertisingRoute,
    counter_step = '0.0.1.0',
    counter_direction = 'increment',
    nest_step = '0.0.0.1,0.1.0.0',
    nest_owner = topology_1_handle,
    nest_enabled = '1'
    )

print '\nrouteRangeTopo1Multivalue:', routeRangeTopo1Multivalue
# 

routeRangeTopo2Multivalue = CreateMultivalueNgpfHlPy(
    pattern = 'counter',
    counter_start = topo2AdvertisingRoute,
    counter_step = '0.0.1.0',
    counter_direction = 'increment',
    nest_step = '0.0.0.1,0.1.0.0',
    nest_owner = topology_2_handle,
    nest_enabled = '1'
    )
print '\nrouteRangeTopo1Multivalue:', routeRangeTopo1Multivalue
# 

topo1NetworkGroup = ConfigNetworkGroupNgpfHlPy(
    protocol_handle = device_group_1_handle,
    connected_to_handle = topo1EthernetHandle,
    type = 'ipv4-prefix',
    enable_device = '1',
    protocol_name = 'Routes=%s' % topo1AdvertisingRoute,
    ipv4_prefix_length = '24',
    ipv4_prefix_number_of_addresses = '80',
    ipv4_prefix_network_address = routeRangeTopo1Multivalue, 
    multiplier = '1'
    )

print '\ntopo1 network group:', topo1NetworkGroup

# /topology:1/deviceGroup:1/networkGroup:1
topo1NetworkGroupHandle = topo1NetworkGroup['network_group_handle']

# /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1
topo1NetworkGroupPrefixPool = topo1NetworkGroup['ipv4_prefix_pools_handle']

topo2NetworkGroup = ConfigNetworkGroupNgpfHlPy(
    protocol_handle = device_group_2_handle,
    connected_to_handle = topo2EthernetHandle,
    type = 'ipv4-prefix',
    enable_device = '1',
    protocol_name = 'Routes=%s' % topo2AdvertisingRoute,
    ipv4_prefix_length = '24',
    ipv4_prefix_number_of_addresses = '100',
    ipv4_prefix_network_address = routeRangeTopo2Multivalue, 
    multiplier = '1'
    )

print '\ntopo2 network group:', topo2NetworkGroup
topo2NetworkGroupHandle = topo2NetworkGroup['network_group_handle']
topo2NetworkGroupPrefixPool = topo2NetworkGroup['ipv4_prefix_pools_handle']

topo1RouteOriginMultivalue = CreateMultivalueNgpfHlPy(
    pattern = 'single_value',
    single_value = 'nssa',
    overlay_value =  'nssa',
    overlay_value_step = 'nssa',
    overlay_index = '2',
    overlay_index_step = '0',
    overlay_count = '0'
    )

topo2RouteOriginMultivalue = CreateMultivalueNgpfHlPy(
    pattern = 'single_value',
    single_value = 'another_area',
    overlay_value =  'another_area',
    overlay_value_step = 'another_area',
    overlay_index = '2',
    overlay_index_step = '0',
    overlay_count = '0'
    )

topo1OspfNetworkGroup = ConfigOspfNetworkGroupNgpfHlPy(
    handle = topo1NetworkGroupHandle,
    mode = 'modify',
    ipv4_prefix_metric = '0',
    ipv4_prefix_active = '1',
    ipv4_prefix_allow_propagate = '0',
    ipv4_prefix_route_origin = topo1RouteOriginMultivalue 
    )

print '\ntopo1 Ospf Network Group:', topo1OspfNetworkGroup

#   ipv4_prefix_pools_handle: /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1
#   ipv4_prefix_interface_handle: /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/ospfRouteProperty:1
#   network_group_handle: /topology:1/deviceGroup:1/networkGroup:1
topo1OspfNetworkGroupHandle = topo1OspfNetworkGroup['network_group_handle']
topo1OspfNetworkGroupIpv4PrefixPool = topo1OspfNetworkGroup['ipv4_prefix_pools_handle']
topo1OspfNetworkGroupipv4PrefixInterface = topo1OspfNetworkGroup['ipv4_prefix_interface_handle']

topo2OspfNetworkGroup = ConfigOspfNetworkGroupNgpfHlPy(
    handle = topo2NetworkGroupHandle,
    mode = 'modify',
    ipv4_prefix_metric = '0',
    ipv4_prefix_active = '1',
    ipv4_prefix_allow_propagate = '0',
    ipv4_prefix_route_origin = topo2RouteOriginMultivalue 
    )

print '\ntopo2 Ospf Network Group:', topo2OspfNetworkGroup
topo2OspfNetworkGroupHandle = topo2OspfNetworkGroup['network_group_handle']
topo2OspfNetworkGroupIpv4PrefixPool = topo2OspfNetworkGroup['ipv4_prefix_pools_handle']
topo2OspfNetworkGroupipv4PrefixInterface = topo2OspfNetworkGroup['ipv4_prefix_interface_handle']

print '\nStarting All protocols ...'
start_protocol_status = ixia_ngpf.test_control(action = 'start_all_protocols')
if start_protocol_status['status'] != '1':
    print '\nError: Failed to start all protocols.\n'
    sys.exit()

print_dict(start_protocol_status)

if VerifyProtocolSessionStatusUpNgpfHlPy(topo1Ipv4Handle) == 1:
    sys.exit()

if VerifyProtocolSessionStatusUpNgpfHlPy(ospfEmulationTopo1) == 1:
    sys.exit()

traffic_status = ixia_ngpf.traffic_config(
    mode = 'create',
    name = 'Traffic_Item_1',
    emulation_src_handle = topology_1_handle,
    emulation_dst_handle = topology_2_handle,
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

print_dict(traffic_status)

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


