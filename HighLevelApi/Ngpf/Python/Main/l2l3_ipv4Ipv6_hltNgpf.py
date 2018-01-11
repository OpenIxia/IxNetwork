#!/usr/local/python2.7.6/bin/python2.7

# By: Hubert Gee
# 
# Create IPv4 and IPv6 dual stack port interfaces
# Create IPv4 Traffic Item
# Create IPv6 Traffic Item

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

'''
chassis_ip = '10.219.117.102'
ixnetwork_tcl_server = '10.219.117.103'
port_list = '1/1 1/2'
port_1 = '1/1/1'
port_2 = '1/1/2'
'''

chassis_ip = '1.1.1.7'
ixnetwork_tcl_server = '1.1.1.6'
port_list = '1/1 2/1'
port_1 = '1/1/1'
port_2 = '1/2/1'

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
    sys.exit()

print_dict(ethernet_status)

ethernet_handle = ethernet_status['ethernet_handle']
print '\n--- ethernet_handle:', ethernet_handle

ipv6_status = ixia_ngpf.interface_config(
    protocol_name = 'IPv6_1',
    protocol_handle = ethernet_handle,
    ipv6_resolve_gateway = '1',
    ipv6_intf_addr = '2000:0:1:0:0:0:0:1',
    ipv6_gateway = '2000:0:1:0:0:0:0:4',
    ipv6_prefix_length = '64',
    )
if ipv6_status['status'] != '1':
    print '\nError: Failed to configure IPv6_1', ipv6_status
    sys.exit()

print_dict(ipv6_status)

ethernet_status2 = ixia_ngpf.interface_config(
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
if ethernet_status2['status'] != '1':
    print '\nError: Failed to configure ethernet 2'
    sys.exit()

print_dict(ethernet_status2)

ethernet_handle2 = ethernet_status2['ethernet_handle']

ipv6_status2 = ixia_ngpf.interface_config(
    protocol_name = 'IPv6_2',
    protocol_handle = ethernet_handle2,
    ipv6_resolve_gateway = '1',
    ipv6_intf_addr = '2000:0:1:0:0:0:0:4',
    ipv6_gateway = '2000:0:1:0:0:0:0:1',
    ipv6_prefix_length = '64',
    )
if ipv6_status2['status'] != '1':
    print '\nError: Failed to configure IPv6_2', ipv6_status2
    sys.exit()

print_dict(ipv6_status2)

print '\nWait 10 seconds for configurations to set...\n'
time.sleep(10)

print '\nStarting IPv4 protocol ...'
start_protocol_status = ixia_ngpf.test_control(action = 'start_all_protocols')
if start_protocol_status['status'] != '1':
    print '\nError: Failed to start all protocols.\n'
    sys.exit()

print_dict(start_protocol_status)

print '\nWait 10 seconds for IPv4 protocols to come up...\n'
time.sleep(10)

traffic_status = ixia_ngpf.traffic_config(
    mode = 'create',
    name = 'Traffic_Item_1',
    emulation_src_handle = topology_1_handle,
    emulation_dst_handle = topology_2_handle,
    transmit_mode = 'single_burst',
    pkts_per_burst = '50000',
    frame_size = '256',
    rate_percent = '100',
    src_dest_mesh = 'one_to_one',
    route_mesh = 'one_to_one',
    bidirectional = '0',
    allow_self_destined = '0',
    circuit_endpoint_type = 'ipv4',
    track_by = 'flowGroup0 sourceDestValuePair0',
    l3_protocol = 'ipv4'
    )
if traffic_status['status'] != '1':
    print '\nError: Failed to configure Traffic Item 1.\n'
    print traffic_status
    sys.exit()

print_dict(traffic_status)


traffic_status = ixia_ngpf.traffic_config(
    mode = 'create',
    name = 'Traffic_Item_2',
    emulation_src_handle = topology_1_handle,
    emulation_dst_handle = topology_2_handle,
    transmit_mode = 'single_burst',
    pkts_per_burst = '50000',
    frame_size = '256',
    rate_percent = '100',
    src_dest_mesh = 'one_to_one',
    route_mesh = 'one_to_one',
    bidirectional = '0',
    allow_self_destined = '0',
    circuit_endpoint_type = 'ipv6',
    track_by = 'flowGroup0 sourceDestValuePair0',
    l3_protocol = 'ipv6'
    )
if traffic_status['status'] != '1':
    print '\nError: Failed to configure Traffic Item 2.\n'
    print traffic_status
    sys.exit()

print_dict(traffic_status)

time.sleep(10)

traffic_control_status = ixia_ngpf.traffic_control(action = 'run')

if traffic_control_status['status'] != '1':
    print '\nError: Failed to start traffic.\n'
    print traffic_control
    sys.exit()

print_dict(traffic_control_status)

time.sleep(10)


print '\ngetList: ', ixNet.getList(ixNet.getRoot()+'traffic', 'trafficItem')

traffic_stats = ixia_ngpf.traffic_stats(
    mode = 'flow'
    )

if traffic_stats['status'] != '1':
    print '\nError: Failed to get traffic flow stats.\n'
    print traffic_stats
    sys.exit()

print_dict(traffic_stats)

sys.exit()
