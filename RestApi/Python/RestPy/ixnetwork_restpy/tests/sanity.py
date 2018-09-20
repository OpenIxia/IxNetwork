"""Sanity script that exercises all major points in the IxNetwork REST API
- sessions
- properties returning objects
- methods returning objects
- tracing
- authentication
- file transfer
- execs
- multivalues
- multivalue steps
"""
import sys
import os
import json
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.errors import IxNetworkError
from ixnetwork_restpy.files import Files

sessions = None

try:
    # test_platform = TestPlatform('10.36.78.53', platform='linux')
    test_platform = TestPlatform('127.0.0.1', rest_port=11009, platform='windows')
    test_platform.Trace = 'none'
    test_platform.Authenticate('admin', 'admin')
    print(test_platform)

    sessions = test_platform.Sessions.add()
    print(sessions)

    ixnetwork = sessions.Ixnetwork
    print(ixnetwork)

    views = ixnetwork.Statistics.View.find()
    print(views)

    try:
        ixnetwork.LoadConfig('c:/temp/ipv4_traffic.ixncfg')
        assert ('Type checking failed')
    except TypeError as e:
        print(e)
    ixnetwork.LoadConfig(Files('c:/users/anbalogh/downloads/ipv4_traffic.ixncfg', local_file=True))

    print(ixnetwork.Globals)
    print(ixnetwork.AvailableHardware)
    print(ixnetwork.Traffic)
    print(ixnetwork.Statistics)
    print(ixnetwork.ResourceManager)

    assert(len(ixnetwork.Vport.find()) == 0)
    assert(len(ixnetwork.Topology.find()) == 0)
    assert(len(ixnetwork.AvailableHardware.Chassis.find()) == 0)
    assert(len(ixnetwork.Statistics.View.find()) == 0)
    assert(len(ixnetwork.Traffic.TrafficItem.find()) == 0)

    vport_name = 'Abstract Port 1'
    vports = ixnetwork.Vport.add(Name=vport_name, Type='pos')
    assert (vports.Type == 'pos')
    assert (vports.Name == vport_name)
    vports.Type = 'ethernet'
    assert (vports.Type == 'ethernet')
    vports.refresh()
    vports.add(Name='Abstract Port 2')
    vports.add(Name='Abstract Port 3')
    assert(len(vports) == 3)
    vports.remove()
    assert(len(vports) == 0)

    # create 2 ports
    vports.add().add()

    # create a raw traffic item
    traffic_item = ixnetwork.Traffic.TrafficItem.add(Name='Raw Traffic Item Test', TrafficType='raw', TrafficItemType='l2L3')
    protocols = vports.Protocols
    assert (len(protocols) == 2)
    protocols.refresh()
    assert (len(protocols) == 2)
    endpoint_set = traffic_item.EndpointSet.add(Sources=protocols)
    assert (len(endpoint_set.Sources) == 2)
    mpls_protocol_template = ixnetwork.Traffic.ProtocolTemplate.find(StackTypeId='^mpls$')
    ethernet_stack = traffic_item.ConfigElement.find()[0].Stack.find(StackTypeId='^ethernet$')
    append_result = ethernet_stack.Append(mpls_protocol_template)

    # create a topology
    topology = ixnetwork.Topology.add(Name='Topology 1', Ports=vports)
    assert(len(topology) == 1)

    # create a device group
    device_group = topology.DeviceGroup.add(Name='Device 1', Multiplier='7')
    assert(len(device_group) == 1)
    device_group.Enabled.Alternate('False')
    assert (device_group.Enabled == 'Alt: False')
    
    # create and print ethernet information
    ethernet = device_group.Ethernet.add()
    assert(len(ethernet) == 1)

    # get multivalue information
    # # outputs format, count, possible patterns etc
    print(ethernet.Mac.Info)

    # multivalue steps
    steps = ethernet.Mac.Steps()
    for step in steps:
        print(step)
        step.Enabled = False
        step.refresh()
        assert (step.Enabled is False)
        
    # update multivalue on server immediately
    ethernet.Mac.Decrement(start_value='00:00:de:ad:be:ef', step_value='00:00:fa:ce:fa:ce')
    assert (ethernet.Mac == 'Dec: 00:00:de:ad:be:ef, 00:00:fa:ce:fa:ce')
    ethernet.Mac.Increment(start_value='00:00:fa:ce:fa:ce', step_value='00:00:de:ad:be:ef')
    assert (ethernet.Mac == 'Inc: 00:00:fa:ce:fa:ce, 00:00:de:ad:be:ef')
    ethernet.Mac.Random()
    assert (ethernet.Mac == 'Rand')
    ethernet.Mac.RandomRange()
    assert (ethernet.Mac.Pattern.startswith('Randr:'))
    ethernet.Mac.RandomMask()
    assert (ethernet.Mac.Pattern.startswith('Randb:'))
    ethernet.Mac.Distributed(algorithm='autoEven', mode='perPort', values=[('00:00:fa:ce:fa:ce', 60), ('0:00:de:ad:be:ef', 40)])
    assert (ethernet.Mac.Pattern.startswith('Dist:'))
    ethernet.Mac.ValueList(values=['00:00:fa:ce:fa:ce', '00:00:de:ad:be:ef'])
    assert (ethernet.Mac.Pattern.startswith('List:'))
    ethernet.Mac.Custom(start_value='00:00:fa:ce:fa:ce', step_value='00:00:de:ad:be:ef', increments=[('00:00:ab:ab:ab:ab', 6, [('00:00:01:01:01:01', 2, None)])])
    assert (ethernet.Mac.Pattern.startswith('Custom:'))
    print(ethernet.Mac.Values)
    
    ipv4 = ethernet.Ipv4.add(Name='Ipv4 1')
    print(ipv4)
    ipv4.Address.Increment(start_value='1.1.1.1', step_value='0.1.1.1')
    assert(ipv4.Address == 'Inc: 1.1.1.1, 0.1.1.1')
    
    bgp4 = ipv4.BgpIpv4Peer.add(Name='Bgp 1')
    bgp4.Md5Key.String('my-md5-key-{Dec: 1,1}')
    print(bgp4)

    # release all vports
    ixnetwork.Vport.find().ReleasePort()

    # add bgp6 in one line
    bgp6 = topology.DeviceGroup.add(Name='Device 2').Ethernet.add().Ipv6.add().BgpIpv6Peer.add()
    print(bgp6)

    # add one quick flow group per vport
    vports = ixnetwork.Vport.find()
    vports.AddQuickFlowGroups(1)
    
    # number of quick flow groups should equal the number of vports
    traffic_items = ixnetwork.Traffic.TrafficItem.find()
    high_level_streams = traffic_items.HighLevelStream.find()

    # errors = ixnetwork.Globals.AppErrors()[0].Error(Name='JSON Import Errors')
    # for instance in errors[0].Instance():
    # 	print(instance)

    # chassis = ixnetwork.AvailableHardware.add_Chassis(Hostname='10.36.24.55')
except IxNetworkError as e:
    print(e)

if sessions is not None:
    sessions.remove()


