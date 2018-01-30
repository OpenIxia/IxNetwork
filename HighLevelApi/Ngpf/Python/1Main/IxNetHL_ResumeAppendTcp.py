#!/opt/Python-2.7.6/bin/python2.7

# Connect to an existing configuration.
# Append TCP header to the existing packet.
#
# 1> Must know the Traffic Item name for the keylget.
# 2> Get the Traffic Item handle.
# 3> Use the Traffic Item handle to get the IPv4 header handle as the stream_id.
# 4> Use the $stream_id to append TCP with src/dst ports.

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

chassis_ip = '10.219.117.102'
ixnetwork_tcl_server = '10.219.16.219'
tcl_server = chassis_ip
user_name = 'hgee'

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



# To Resume
connect_result = ixia_hlt.connect ( 
    ixnetwork_tcl_server = ixnetwork_tcl_server,
    tcl_server = tcl_server,
    username = user_name,
    break_locks = '1'
    ) 

print_dict(connect_result)

# MUST know the Traffic Item name!
# TI0-TrafficItem_1 is my Traffic Item name.

config_element = connect_result['TI0-TrafficItem_1']['traffic_config']['traffic_item']
print '\n', config_element

# Get the index position of the IPv4 header because we want to append TCP after it.
# ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ipv4-2"
ipv4PacketStack = connect_result['TI0-TrafficItem_1']['traffic_config'][config_element]['headers']
ipv4PacketStack = ipv4PacketStack.split()[2]
print '\nipv4PacketStack', ipv4PacketStack


traffic_status = ixia_hlt.traffic_config(
    mode = 'append_header',
    stream_id = ipv4PacketStack,
    l4_protocol = 'tcp',
    tcp_src_port = '1001 1003',
    tcp_dst_port = '1005 1007',
    tcp_src_port_mode = 'list',
    tcp_dst_port_mode = 'list'
    )

