#!/usr/local/python2.7.6/bin/python2.7

import sys
import time

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError

ixia_tcl = IxiaTcl()
ixia_hlt = IxiaHlt(ixia_tcl)
ixia_ngpf = IxiaNgpf(ixia_hlt)
ixNet = ixia_ngpf.ixnet ;# For low level Python API commands

reset = '0'
username = 'hgee'
ixnetwork_tcl_server = '192.168.70.127'
port_list = '1/1 2/1'
tcl_server = '192.168.70.11'
device = '192.168.70.11'


def PrintDict(obj, nested_level=0, output=sys.stdout):
    """
    Print each dict key with indentions for readability.
    """

    spacing = '   '
    if type(obj) == dict:
        print >> output, '%s' % ((nested_level) * spacing)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                PrintDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % (
                    (nested_level + 1) * spacing, k, v)

        print >> output, '%s' % (nested_level * spacing)

    elif type(obj) == list:
        print >> output, '%s[' % ((nested_level) * spacing)
        for v in obj:
            if hasattr(v, '__iter__'):
                PrintDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % ((nested_level) * spacing)

    else:
        print >> output, '%s%s' % (nested_level * spacing, obj)



def ConnectHlPy(device='', reset=1, port_list='',
                ixnetwork_tcl_server='', tcl_server='',
                username='unknown'):

    print 'ConnectHlPy: Chassis:%s IxNetTclServer=%s' % (device, ixnetwork_tcl_server)
    connect_status = ixia_ngpf.connect(
        reset=reset,
        device=device,
        port_list=port_list,
        ixnetwork_tcl_server=ixnetwork_tcl_server,
        tcl_server=tcl_server,
        username=username
    )

    PrintDict(connect_status)

    if connect_status['status'] != '1':
        return 1
    else:
        return connect_status



def ConfigPortHlPy(mode='config',
                   port_handle='',
                   phy_mode='copper',
                   speed='ether1000',
                   autonegotiation='1',
                   duplex='full',
                   intf_mode='ethernet'):

    print '\nConfigPortHlPy:', port_handle, phy_mode
    status = ixia_hlt.interface_config(mode=mode,
                                       port_handle=port_handle,
                                       phy_mode=phy_mode,
                                       speed=speed,
                                       autonegotiation=autonegotiation,
                                       duplex=duplex,
                                       intf_mode=intf_mode
                                       )

    if status['status'] != '1':
        print '\nConfig_Port failed: %s\n' % status['log']
        sys.exit()

def ShowKwargs(**kwargs):
    for key, value in kwargs.iteritems():
        print '\t%s: %s' % (key, value)
    print '\n'

def CreateTopologyNgpfHlPy(topology_name='Topology', ports=''):
    ''' port_handle format = 12/1 '''

    print '\nCreateTopologyNgpfHlPy'
    status = ixia_ngpf.topology_config(
        topology_name=topology_name,
        port_handle=ports
    )

    if status['status'] != '1':
        return 1

    # /topology:1
    topology_handle = status['topology_handle']
    return topology_handle



def CreateDeviceGroupNgpfHlPy(topology_handle='',
                              device_group_name='',
                              multiplier=1,
                              enabled=1
                              ):

    print '\nCreateDeviceGroupNgpfHlPy'
    status = ixia_ngpf.topology_config(
        topology_handle=topology_handle,
        device_group_name=device_group_name,
        device_group_multiplier=multiplier,
        device_group_enabled=enabled
    )

    if status['status'] != '1':
        return 1

    # /topology:1/deviceGroup:1
    device_group_handle = status['device_group_handle']
    return device_group_handle

def CreateMultivalueNgpfHlPy(**kwargs):
    print '\nCreateMultivalueNgpfHlPy:'
    ShowKwargs(**kwargs)

    multivalue = ixia_ngpf.multivalue_config(**kwargs)
    if multivalue['status'] != '1':
        print '\nConfigMultivalueHlPy: Failed'
        return 1

    return multivalue['multivalue_handle']

def ConfigProtocolInterfaceNgpfHlPy(**kwargs):
    """ Usage:

     PortConfigProtocolIntNgpf(
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
    """

    print '\nConfigProtocolInterfaceNgpfHlPy:'
    ShowKwargs(**kwargs)

    status = ixia_ngpf.interface_config(**kwargs)
    if status['status'] != '1':
        return 1

    '''
     status: 1
     ethernet_handle: /topology:1/deviceGroup:1/ethernet:1
     ipv4_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1
     interface_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:1
                       /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:2
                       /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:3
                       /topology:1/deviceGroup:1/ethernet:1/item:1
                       /topology:1/deviceGroup:1/ethernet:1/item:2
                       /topology:1/deviceGroup:1/ethernet:1/item:3
     '''
    return status

def ConfigIgmpEmulationNgpfHlPy(**kwargs):
    print '\nConfigIgmpEmulationNgpfHlPy:'
    for key, value in kwargs.iteritems():
        print '\t%s: %s' % (key, value)

    status = ixia_ngpf.emulation_igmp_config(**kwargs)

    if status['status'] != '1':
        print '\nConfigIgmpEmulationNgpfHlPy failed: %s\n' % status['log']
        sys.exit()

    PrintDict(status)
    return status

def ConfigIgmpMulticastGroupNgpfHlPy(**kwargs):
    print '\nConfigIgmpMulticastGroupNgpfHlPy:'
    for key, value in kwargs.iteritems():
        print '\t%s: %s' % (key, value)

    status = ixia_ngpf.emulation_multicast_group_config(**kwargs)
    if status['status'] != '1':
        print '\nConfigIgmpGroupNgpfPy failed: %s\n' % status['log']
        sys.exit()

    PrintDict(status)
    return status

def ConfigIgmpGroupNgpfHlPy(**kwargs):
    print '\nConfigIgmpGroupNgpfHlPy:'
    for key, value in kwargs.iteritems():
        print '\t%s: %s' % (key, value)

    status = ixia_ngpf.emulation_igmp_group_config(**kwargs)
    if status['status'] != '1':
        print '\nConfigIgmpGroupNgpfHlPy failed: %s\n' % status['log']
        sys.exit()

    PrintDict(status)
    return status

def ConfigIgmpQuerierNgpfHlPy(**kwargs):
    print '\nConfigIgmpQuerierNgpfHlPy:'
    for key, value in kwargs.iteritems():
        print '\t%s: %s' % (key, value)

    status = ixia_ngpf.emulation_igmp_querier_config(**kwargs)
    if status['status'] != '1':
        print '\nConfigIgmpQuerierNgpfHlPy failed: %s\n' % status['log']
        sys.exit()

    # igmpQuerierStatus:: status: 1
    # igmp_querier_handle: /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1
    # igmp_querier_handles: /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:1
    #                       /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:2
    #                       /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:3

    PrintDict(status)
    return status

def ConfigIgmpSourceGroupNgpfHlPy(**kwargs):
    print '\nConfigIgmpSourceGroupNgpfHlPy:'
    for key, value in kwargs.iteritems():
        print '\t%s: %s' % (key, value)

    status = ixia_ngpf.emulation_multicast_source_config(**kwargs)
    if status['status'] != '1':
        print '\nConfigIgmpSourceGroupNgpfHlPy failed: %s\n' % status['log']
        sys.exit()

    PrintDict(status)
    # return status['multicast_source_handle']
    return status

def StartAllProtocolsNgpfHlPy():
    print '\nStartAllProtocolsNgpfHlPy'
    status = ixia_ngpf.test_control(action='start_all_protocols')
    if status['status'] != '1':
        print '\nStartAllProtocolsNgpfHlPy failed:', status['log']
        return 1

    time.sleep(5)
    return status

def VerifyProtocolSessionStatusUpNgpfHlPy(protocolHandleList, totalTime=60):
    '''
    protocolHandleList: One or more protocol handles in a list
                        to verify for sessions status 'UP'.

    Protocol handle example:
                     /topology:1/deviceGroup:1/ethernet:1/ipv4:1
                     /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1
    '''
    errorFlag = 0

    for eachProtocolSessionToVerify in protocolHandleList:
        for timer in range(1, totalTime + 1):
            sessionStatus = ixia_ngpf.protocol_info(
                handle=eachProtocolSessionToVerify,
                mode='aggregate'
            )

            currentSessionUp = sessionStatus[
                eachProtocolSessionToVerify]['aggregate']['sessions_up']
            totalSessions = sessionStatus[eachProtocolSessionToVerify][
                'aggregate']['sessions_total']

            print '\nVerifying protocol sessions', eachProtocolSessionToVerify
            print '\t%s/%s: CurrentSessionUp:%s   TotalSessions:%s\n' % (timer, totalTime, currentSessionUp, totalSessions)

            if timer < totalTime and currentSessionUp != totalSessions:
                time.sleep(1)
                continue

            if timer < totalTime and currentSessionUp == totalSessions:
                break

            if timer == totalTime and currentSessionUp != totalSessions:
                print '\nError: It has been %s seconds and total sessions are not all UP. ' % timer
                errorFlag = 1

    if errorFlag:
        sys.exit()

def ConfigTrafficItemNgpfHlPy(**kwargs):
    """ Usage:

    CreateTrafficItem(
    mode = 'create',
    name = 'Traffic_Item_1',
    emulation_src_handle = topology_1_handle,
    emulation_dst_handle = topology_2_handle,
    transmit_mode = 'continuous',
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
    """
    print '\nConfigTrafficItemNgpfHlPy:'
    ShowKwargs(**kwargs)

    status = ixia_ngpf.traffic_config(**kwargs)

    if status['status'] != '1':
        return 1

    '''
     status: 1
     stream_id: TI0-Traffic_Item_1
     log: 
     ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1:
     
     headers: ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ethernet-1"
              ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ipv4-2"
              ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"fcs-3"
     ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1:
     
     headers: ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"ethernet-1"
              ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"ipv4-2"
              ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"fcs-3"
     
     encapsulation_name: Ethernet.IPv4
     endpoint_set_id: 1
     stream_ids: ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1
     traffic_item: ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1
     '''

    return status

def StartTrafficNgpfHlPy():
    print '\nStartTrafficNgpfHlPy'
    status = ixia_ngpf.traffic_control(action='run')
    if status == 1:
        print '\nStartTrafficNgpfHlPy failed: ', status['log']
        return 1

    return status

def GetStatsNgpfHlPy(type_of_stats='flow'):
    print '\nGetStatsNgpfHlPy:', type_of_stats
    status = ixia_ngpf.traffic_stats(mode=type_of_stats)
    if status['status'] != '1':
        print '\nGetStatsNgpfHlPy failed: ', status['log']
        sys.exit()

    PrintDict(status)
    return status

ConnectHlPy(device='10.219.117.101',
            tcl_server='10.219.117.101',
            ixnetwork_tcl_server='10.219.117.103',
            port_list='1/1 1/2',
            reset='0',
            username='hgee',
            )

ConfigPortHlPy(mode='config',
               port_handle='1/1/1 1/1/2',
               phy_mode='copper')

topology_handle_1 = CreateTopologyNgpfHlPy(
    topology_name='Topology 1', ports='1/1/1')

device_group_handle_1 = CreateDeviceGroupNgpfHlPy(topology_handle=topology_handle_1,
                                                  device_group_name='IGMP Host',
                                                  multiplier='3')

src_mac_multivalue = CreateMultivalueNgpfHlPy(pattern='counter',
                                              counter_start='00:01:01:01:00:01',
                                              counter_step='00:00:00:00:00:01',
                                              counter_direction='increment',
                                              nest_step='00:00:00:00:00:01',
                                              nest_enabled=' 0',
                                              nest_owner=topology_handle_1)

ethernet_handle_1 = ConfigProtocolInterfaceNgpfHlPy(mode='config',
                                                    protocol_handle=device_group_handle_1,
                                                    src_mac_addr=src_mac_multivalue,
                                                    vlan_user_priority='3',
                                                    vlan_tpid='0x8100',
                                                    vlan_id='101',
                                                    vlan_id_step='0',
                                                    vlan='1',
                                                    mtu='1500')

ipv4_multivalue = CreateMultivalueNgpfHlPy(pattern='counter',
                                           counter_start='10.10.10.1',
                                           counter_step='0.0.0.1',
                                           counter_direction='increment',
                                           nest_step='0.0.0.1',
                                           nest_enabled='0',
                                           nest_owner=topology_handle_1)

ipv4_gateway_multivalue = CreateMultivalueNgpfHlPy(pattern='counter',
                                                   counter_start='10.10.10.4',
                                                   counter_step='0.0.0.1',
                                                   counter_direction='increment',
                                                   nest_step='0.0.0.1',
                                                   nest_enabled='0',
                                                   nest_owner=topology_handle_1)

ipv4_handle_1 = ConfigProtocolInterfaceNgpfHlPy(protocol_name='IPv4',
                                                intf_ip_addr=ipv4_multivalue,
                                                netmask='255.255.255.0',
                                                gateway=ipv4_gateway_multivalue,
                                                ipv4_resolve_gateway='1',
                                                arp_send_req='1',
                                                arp_req_retries='3',
                                                protocol_handle=ethernet_handle_1['ethernet_handle'])

igmp_host_handle_1 = ConfigIgmpEmulationNgpfHlPy(mode='create',
                                                 ip_router_alert='1',
                                                 name='IGMP_Host',
                                                 max_response_control='0',
                                                 join_leave_multiplier='1',
                                                 general_query='1',
                                                 group_query='1',
                                                 unsolicited_response_mode='0',
                                                 igmp_version='v2',
                                                 unsolicited_report_interval='120',
                                                 handle=ipv4_handle_1['ipv4_handle'])

igmp_multivalue = CreateMultivalueNgpfHlPy(single_value='228.1.1.1',
                                           overlay_value='228.0.0.1,229.0.0.1,230.0.0.1',
                                           overlay_value_step='228.0.0.1,229.0.0.1,230.0.0.1',
                                           overlay_index='1,2,3',
                                           overlay_index_step='0,0,0',
                                           overlay_count='1,1,1',
                                           nest_owner=topology_handle_1)

igmp_active_multivalue = CreateMultivalueNgpfHlPy(pattern='single_value',
                                                  overlay_value='1,1,1',
                                                  overlay_index='1,2,3',
                                                  overlay_value_step='1,1,1',
                                                  single_value='0')

multicast_group_handle_1 = ConfigIgmpMulticastGroupNgpfHlPy(mode='create',
                                                            num_groups='1',
                                                            ip_addr_step='1.0.0.0',
                                                            ip_addr_start=igmp_multivalue,
                                                            active=igmp_active_multivalue)

source_group = CreateMultivalueNgpfHlPy(counter_start='228.1.1.1',
                                        counter_step='0.0.0.0',
                                        counter_direction='increment',
                                        nest_step='0.0.0.1',
                                        nest_enabled='1',
                                        overlay_value='10.10.10.1,10.10.10.2',
                                        overlay_value_step='10.10.10.1,10.10.10.2',
                                        overlay_index='1,2',
                                        overlay_index_step='0,0',
                                        overlay_count='1,1',
                                        nest_owner=topology_handle_1)

igmp_source_group_handle_1 = ConfigIgmpSourceGroupNgpfHlPy(mode='create',
                                                           ip_addr_step='0.0.0.0',
                                                           num_sources='1',
                                                           active='1',
                                                           ip_addr_start=source_group)

igmp_group_handle_1 = ConfigIgmpGroupNgpfHlPy(mode='create',
                                              session_handle=igmp_host_handle_1[
                                                  'igmp_host_handle'],
                                              group_pool_handle=multicast_group_handle_1[
                                                  'multicast_group_handle'],
                                              source_pool_handle=igmp_source_group_handle_1['multicast_source_handle'])

topology_handle_2 = CreateTopologyNgpfHlPy(
    topology_name='Topology 2', ports='1/1/2')

device_group_handle_2 = CreateDeviceGroupNgpfHlPy(topology_handle=topology_handle_2,
                                                  device_group_name='IGMP Querier',
                                                  multiplier='3')

src_mac_multivalue = CreateMultivalueNgpfHlPy(pattern='counter',
                                              counter_start='00:01:01:02:00:01',
                                              counter_step='00:00:00:00:00:01',
                                              counter_direction='increment',
                                              nest_step='00:00:00:00:00:01',
                                              nest_enabled=' 0',
                                              nest_owner=topology_handle_2)

ethernet_handle_2 = ConfigProtocolInterfaceNgpfHlPy(mode='config',
                                                    protocol_handle=device_group_handle_2,
                                                    src_mac_addr=src_mac_multivalue,
                                                    vlan_user_priority='3',
                                                    vlan_tpid='0x8100',
                                                    vlan_id='101',
                                                    vlan_id_step='0',
                                                    vlan='1',
                                                    mtu='1500')

ipv4_multivalue = CreateMultivalueNgpfHlPy(pattern='counter',
                                           counter_start='10.10.10.4',
                                           counter_step='0.0.0.1',
                                           counter_direction='increment',
                                           nest_step='0.0.0.1',
                                           nest_enabled='0',
                                           nest_owner=topology_handle_2)

ipv4_gateway_multivalue = CreateMultivalueNgpfHlPy(pattern='counter',
                                                   counter_start='10.10.10.1',
                                                   counter_step='0.0.0.1',
                                                   counter_direction='increment',
                                                   nest_step='0.0.0.1',
                                                   nest_enabled='0',
                                                   nest_owner=topology_handle_2)

ipv4_handle_2 = ConfigProtocolInterfaceNgpfHlPy(netmask='255.255.255.0',
                                                protocol_name='IPv4-Kara',
                                                intf_ip_addr=ipv4_multivalue,
                                                gateway=ipv4_gateway_multivalue,
                                                ipv4_resolve_gateway='1',
                                                arp_send_req='1',
                                                arp_req_retries='3',
                                                protocol_handle=ethernet_handle_2['ethernet_handle'])

igmp_querier_handle_0 = ConfigIgmpQuerierNgpfHlPy(mode='create',
                                                  ip_router_alert='1',
                                                  support_older_version_querier='1',
                                                  name='IGMP_Querier',
                                                  specific_query_response_interval='1000',
                                                  general_query_response_interval='1000',
                                                  robustness_variable='2',
                                                  startup_query_count='2',
                                                  specific_query_transmission_count='2',
                                                  active='1',
                                                  query_interval='125',
                                                  support_older_version_host='1',
                                                  discard_learned_info='0',
                                                  support_election='1',
                                                  handle=ipv4_handle_2['ipv4_handle'])

StartAllProtocolsNgpfHlPy()

VerifyProtocolSessionStatusUpNgpfHlPy(['/topology:1/deviceGroup:1/ethernet:1/ipv4:1', igmp_host_handle_1[
                                      'igmp_host_handle'], '/topology:2/deviceGroup:1/ethernet:1/ipv4:1', igmp_querier_handle_0['igmp_querier_handle'], ])

traffic_item_1 = ConfigTrafficItemNgpfHlPy(mode='create',
                                           emulation_src_handle='/topology:1',
                                           name='Igmp_Traffic_1',
                                           rate_percent='100',
                                           pkts_per_burst='10000',
                                           transmit_mode='single_burst',
                                           circuit_endpoint_type='ipv4',
                                           frame_size='128',
                                           l3_protocol='ipv4',
                                           track_by='flowGroup0',
                                           emulation_dst_handle='/topology:2')

StartTrafficNgpfHlPy()
time.sleep(10)
GetStatsNgpfHlPy()

