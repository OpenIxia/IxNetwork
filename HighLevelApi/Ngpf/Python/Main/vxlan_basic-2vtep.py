#!/opt/Python-2.7.6/bin/python2.7

# Description:
#
#   VxLAN script with two Ixia ports connected back-2-back
#   as VTEP peers.  Behind each VTEP are VM hosts.
#  
#   The current configuration includes vlan on the VM hosts,
#   but not enabled. To enabled vlan, set parameter 'vlan= '1'
# 
#

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

reset = '1'
username = 'hgee'
ixnetwork_tcl_server = '10.219.16.219'
port_list = '8/3 8/4'
tcl_server = '10.219.117.11'
ixia_chassis = '10.219.117.11'
port_1 = '1/8/3'
port_2 = '1/8/4'

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


def Connect(device='',
            port_list='',
            ixnetwork_tcl_server='',
            tcl_server='',
            username='',
            reset=1):

    ixia_ngpf.ixiahlt.ixiatcl._eval("set ::ixia::logHltapiCommandsFlag 1")
    ixia_ngpf.ixiahlt.ixiatcl._eval(
        "set ::ixia::logHltapiCommandsFileName ixiaHltDebug.txt")

    status = ixia_ngpf.connect(reset=reset, device=device, port_list=port_list,
                               ixnetwork_tcl_server=ixnetwork_tcl_server,
                               tcl_server=device, username=username)

    if status['status'] != '1':
        print '\nConnect failed: %s\n' % status['log']
    else:
        print '\nConnect success: %s' % ixnetwork_tcl_server

    return status


def Create_Topology(topology_name='', ports=''):
    status = ixia_ngpf.topology_config(topology_name=topology_name,
                                       port_handle=ports)

    if status['status'] != '1':
        print '\nCreate_Topology failed: %s\n' % status['log']
        sys.exit()

    PrintDict(status)
    return status['topology_handle']



def Create_Device_Group(topology_handle='',
                        name='',
                        multiplier=''):

    status = ixia_ngpf.topology_config(topology_handle=topology_handle,
                                       device_group_name=name,
                                       device_group_multiplier=multiplier,
                                       device_group_enabled='1')

    if status['status'] != '1':
        print '\nCreateDeviceGroup failed: %s\n' % status['log']
        sys.exit()

    # /topology:1/deviceGroup:1
    PrintDict(status)
    device_group_handle = status['device_group_handle']
    return device_group_handle


def Create_Multivalue(**kwargs):
    params = 'ixia_ngpf.multivalue_config('

    for key, value in kwargs.iteritems():
        if value:
            params = params + key + '=' + '\'' + value + '\'' + ',' + '\n'

    params = params[:-1] + ')'

    print '\nCreateMultivalue: %s\n' % params
    status = eval(params)

    if status['status'] != '1':
        print '\nCreateDeviceGroup failed: %s\n' % status['log']
        sys.exit()

    multivalue_handle = status['multivalue_handle']
    PrintDict(status)
    return multivalue_handle


def Config_Protocol_Interface(**kwargs):
    params = 'ixia_ngpf.interface_config( '

    for key, value in kwargs.iteritems():
        params = params + key + '=' + '\'' + value + '\'' + ','

    params = params[:-1] + ')'

    print '\nConfigProtocolInterface: %s\n' % params
    status = eval(params)

    if status['status'] != '1':
        print '\nConfigProtocolInterface failed: %s\n' % status['log']
        sys.exit()

    # status:
    #    ethernet_handle: /topology:1/deviceGroup:1/ethernet:1
    #    ipv4_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1
    # interface_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:1
    # /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:2
    # /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:3
    # /topology:1/deviceGroup:1/ethernet:1/item:1
    # /topology:1/deviceGroup:1/ethernet:1/item:2
    # /topology:1/deviceGroup:1/ethernet:1/item:3
    PrintDict(status)
    return status


def ConfigVxlanEmulation(get_handle='yes', **kwargs):
    params = 'ixia_ngpf.emulation_vxlan_config('

    for key, value in kwargs.iteritems():
        params = params + key + '=' + '\'' + value + '\'' + ','

    params = params[:-1] + ')'

    print '\nConfigVxlanEmulation: %s\n' % params
    status = eval(params)

    if status['status'] != '1':
        print '\nConfigVxlanEmulation failed: %s\n' % status['log']
        sys.exit()

    PrintDict(status)
    if get_handle == 'yes':
        return status['vxlan_handle']


def Start_All_Protocols_Ngpf_Hlt():
    status = ixia_ngpf.test_control(action='start_all_protocols')

    if status['status'] != '1':
        print '\nStart_All_Protocols failed:', status['log']
        sys.exit()

    time.sleep(5)
    print '\nStart_All_Protocols: Successfully started'


def Config_Traffic_Item(**kwargs):
    params = 'ixia_ngpf.traffic_config( '

    for key, value in kwargs.iteritems():
        params = params + key + '=' + '\'' + value + '\'' + ','

    params = params[:-1] + ')'

    print '\nConfig_Traffic_Item: %s\n' % params
    status = eval(params)

    if status['status'] != '1':
        print '\nConfig_Traffic_Item failed: %s\n' % status['log']
        sys.exit()

    return status


def Start_Traffic_Ngpf_Hlt():
    status = ixia_ngpf.traffic_control(action='run')

    if status['status'] != '1':
        print '\nStart_Traffic_Ngpf failed: ', status['log']
        sys.exit()

    time.sleep(10)
    print '\nStart_Traffic_Ngpf_Hlt: Successfully started'


def Get_Stats_Ngpf_Hlt(type_of_stats='flow'):
    status = ixia_ngpf.traffic_stats(mode=type_of_stats)

    if status['status'] != '1':
        print '\nGet_Stats_Flow failed: ', status['log']
        sys.exit()

    PrintDict(status)


Connect(device=ixia_chassis,
        tcl_server=ixia_chassis,
        ixnetwork_tcl_server=ixnetwork_tcl_server,
        port_list=port_list,
        reset=reset,
        username=username)

topology_handle_1 = Create_Topology(topology_name='Topology 1', ports=port_1)

device_group_handle_1 = Create_Device_Group(topology_handle=topology_handle_1,
                                            name='VxLAN-1',
                                            multiplier='2')

multivalue = Create_Multivalue(pattern            = "counter",
                               counter_start      = "00.11.01.00.00.01",
                               counter_step       = "00.00.00.00.00.01",
                               counter_direction  = "increment",
                               nest_step          = "00.00.01.00.00.00",
                               nest_owner         = topology_handle_1,
                               nest_enabled       = "1")
                               

ethernet_vxlan_handle_1 = Config_Protocol_Interface(protocol_name   = "{Ethernet 1}",
                                                    protocol_handle = device_group_handle_1,
                                                    mtu             = "1500",
                                                    src_mac_addr    = multivalue,
                                                    vlan            = "0",
                                                    vlan_id         = "1",
                                                    vlan_id_step    = "1",
                                                    vlan_id_count   = "1",
                                                    vlan_tpid       = "0x8100",
                                                    vlan_user_priority = "0")

ethernet_vxlan_handle_1 = ethernet_vxlan_handle_1['ethernet_handle']

multivalue_ip = Create_Multivalue(pattern         = "counter",
                                  counter_start      = "1.1.1.1",
                                  counter_step       = "0.0.0.1",
                                  counter_direction  = "increment",
                                  nest_step          = "0.1.0.0",
                                  nest_owner         = topology_handle_1,
                                  nest_enabled       = "0")

multivalue_gateway = Create_Multivalue(pattern           = "counter",
                                       counter_start     = "1.1.1.10",
                                       counter_step      = "0.0.0.0",
                                       counter_direction = "increment",
                                       nest_step         = "0.1.0.0",
                                       nest_owner        = topology_handle_1,
                                       nest_enabled      = "0")
                                       
ipv4_vxlan_handle_1 = Config_Protocol_Interface(protocol_name                 = "{IPv4 1}",
                                                protocol_handle               = ethernet_vxlan_handle_1,
                                                ipv4_resolve_gateway          = "1",
                                                gateway                       = multivalue_gateway,
                                                intf_ip_addr                  = multivalue_ip,
                                                netmask                       = "255.255.255.0")
                                          

ipv4_vxlan_handle_1 = ipv4_vxlan_handle_1['ipv4_handle']
print '\nipv4_vxlan_handle_1:', ipv4_vxlan_handle_1

multivalue_vni = Create_Multivalue(pattern            = "counter",
                                   counter_start      = "1000",
                                   counter_step       = "1",
                                   counter_direction  = "increment",
                                   nest_step          = "1",
                                   nest_owner         = topology_handle_1,
                                   nest_enabled       = "0")

multivalue_multicast = Create_Multivalue(pattern            = "counter",
                                         counter_start      = "225.1.1.1",
                                         counter_step       = "0.0.0.1",
                                         counter_direction  = "increment",
                                         nest_step          = "0.0.0.1",
                                         nest_owner         = topology_handle_1,
                                         nest_enabled       = "0")
                                         

multivalue_static_mac = Create_Multivalue(pattern           = "counter",
                                         counter_start      = "00:00:00:00:00:00",
                                         counter_step       = "00:00:00:00:00:00",
                                         counter_direction  = "increment",
                                         nest_step          = "00:00:00:00:00:00",
                                         nest_owner         = topology_handle_1,
                                         nest_enabled       = "1")

    
vxlan_handle_1 = ConfigVxlanEmulation(handle                  = ipv4_vxlan_handle_1,
                                      protocol_name           = "{VXLAN 1}",
                                      vni                     = multivalue_vni,
                                      ipv4_multicast          = multivalue_multicast,
                                      enable_static_info      = "0",
                                      static_info_count       = "1",
                                      remote_vtep_ipv4        = "0.0.0.0",
                                      remote_vm_static_mac    = multivalue_static_mac,
                                      remote_vm_static_ipv4   = "0.0.0.0",
                                      remote_info_active      = "1",
                                      ip_to_vxlan_multiplier  = "1")

print '\nvxlan_handle_1:', vxlan_handle_1

device_group_handle_vxlan = Create_Device_Group(topology_handle = device_group_handle_1,
                                                name = 'VLAN-1',
                                                multiplier = '3')


multivalue_mac = Create_Multivalue(pattern           = "counter",
                                   counter_start     = "00.12.01.00.00.01",
                                   counter_step      = "00.00.00.00.00.01",
                                   counter_direction = "increment",
                                   nest_step         = "00.00.00.00.00.01,00.00.01.00.00.00",
                                   nest_owner        = '%s,%s' % (device_group_handle_1, topology_handle_1),
                                   nest_enabled      = "0,1")
                                                

ethernet_handle_1 = Config_Protocol_Interface(protocol_name           = "{Vlan}",
                                              protocol_handle         = device_group_handle_vxlan,
                                              connected_to_handle     = vxlan_handle_1,
                                              mtu                     = "1500",
                                              src_mac_addr            = multivalue_mac,
                                              vlan                    = "0",
                                              vlan_id                 = "1",
                                              vlan_id_step            = "0",
                                              vlan_id_count           = "1",
                                              vlan_tpid               = "0x8100",
                                              vlan_user_priority      = "0",
                                              vlan_user_priority_step = "0",
                                              use_vpn_parameters      = "0",
                                              site_id                 = "0")

# /topology:1/deviceGroup:1/deviceGroup:1/ethernet:1
ethernet_handle_1 = ethernet_handle_1['ethernet_handle']
print '\nethernet_handle_1:', ethernet_handle_1

multivalue_ipv4 = Create_Multivalue(pattern           = "counter",
                                    counter_start     = "10.1.1.1",
                                    counter_step      = "0.0.1.0",
                                    counter_direction = "increment",
                                    nest_step         = "0.0.0.1,0.1.0.0",
                                    nest_owner        = '%s,%s' % (device_group_handle_1, topology_handle_1),
                                    nest_enabled      = "0,1")

multivalue_gateway = Create_Multivalue(pattern           = "counter",
                                       counter_start     = "10.1.1.10",
                                       counter_step      = "0.0.1.0",
                                       counter_direction = "increment",
                                       nest_step         = "0.0.0.1,0.1.0.0",
                                       nest_owner        = '%s,%s' % (device_group_handle_1, topology_handle_1),
                                       nest_enabled      = "0,1")
                                       
ipv4_handle_1 = Config_Protocol_Interface(protocol_name        = "{IPv4 2}",
                                          protocol_handle      = ethernet_handle_1,
                                          ipv4_resolve_gateway = "1",
                                          gateway              = multivalue_gateway,
                                          intf_ip_addr         = multivalue_ipv4,
                                          netmask              = "255.255.255.0")

# Use this handle for Traffic Item endpoint
# /topology:1/deviceGroup:1/deviceGroup:1/ethernet:1/ipv4:1
ipv4_handle_1 = ipv4_handle_1['ipv4_handle']

#-------------- Topology 2 ----------------"

topology_handle_2 = Create_Topology(topology_name='Topology 2', ports=port_2)

device_group_handle_2 = Create_Device_Group(topology_handle=topology_handle_2,
                                            name='VxLAN-2',
                                            multiplier='2')

multivalue = Create_Multivalue(pattern            = "counter",
                               counter_start      = "00.22.01.00.00.01",
                               counter_step       = "00.00.00.00.00.01",
                               counter_direction  = "increment",
                               nest_step          = "00.00.01.00.00.00",
                               nest_owner         = topology_handle_2,
                               nest_enabled       = "0")
                               

ethernet_vxlan_handle_2 = Config_Protocol_Interface(protocol_name   = "{Ethernet 1}",
                                                    protocol_handle = device_group_handle_2,
                                                    mtu             = "1500",
                                                    src_mac_addr    = multivalue,
                                                    vlan            = "0",
                                                    vlan_id         = "1",
                                                    vlan_id_step    = "1",
                                                    vlan_id_count   = "1",
                                                    vlan_tpid       = "0x8100",
                                                    vlan_user_priority = "0")

ethernet_vxlan_handle_2 = ethernet_vxlan_handle_2['ethernet_handle']

multivalue_ip = Create_Multivalue(pattern         = "counter",
                               counter_start      = "1.1.1.10",
                               counter_step       = "0.0.0.1",
                               counter_direction  = "increment",
                               nest_step          = "0.1.0.0",
                               nest_owner         = topology_handle_2,
                               nest_enabled       = "0")

multivalue_gateway = Create_Multivalue(pattern           = "counter",
                                       counter_start     = "1.1.1.1",
                                       counter_step      = "0.0.0.0",
                                       counter_direction = "increment",
                                       nest_step         = "0.1.0.0",
                                       nest_owner        = topology_handle_2,
                                       nest_enabled      = "0")
                                       
ipv4_vxlan_handle_2 = Config_Protocol_Interface(protocol_name                = "{IPv4 2}",
                                                protocol_handle               = ethernet_vxlan_handle_2,
                                                ipv4_resolve_gateway          = "1",
                                                gateway                       = multivalue_gateway,
                                                intf_ip_addr                  = multivalue_ip,
                                                netmask                       = "255.255.255.0")


ipv4_vxlan_handle_2 = ipv4_vxlan_handle_2['ipv4_handle']

print '\nipv4_vxlan_handle_2:', ipv4_vxlan_handle_2

multivalue_vni = Create_Multivalue(pattern              = "counter",
                                     counter_start      = "1000",
                                     counter_step       = "1",
                                     counter_direction  = "increment",
                                     nest_step          = "1",
                                     nest_owner         = topology_handle_2,
                                     nest_enabled       = "0")

multivalue_multicast = Create_Multivalue(pattern            = "counter",
                                         counter_start      = "225.1.1.1",
                                         counter_step       = "0.0.0.1",
                                         counter_direction  = "increment",
                                         nest_step          = "0.0.0.1",
                                         nest_owner         = topology_handle_2,
                                         nest_enabled       = "0")
                                         

multivalue_static_mac = Create_Multivalue(pattern           = "counter",
                                         counter_start      = "00:00:00:00:00:00",
                                         counter_step       = "00:00:00:00:00:00",
                                         counter_direction  = "increment",
                                         nest_step          = "00:00:00:00:00:00",
                                         nest_owner         = topology_handle_2,
                                         nest_enabled       = "0")

    
vxlan_handle_2 = ConfigVxlanEmulation(handle                  = ipv4_vxlan_handle_2,
                                      protocol_name           = "{VXLAN 1}",
                                      vni                     = multivalue_vni,
                                      ipv4_multicast          = multivalue_multicast,
                                      enable_static_info      = "0",
                                      static_info_count       = "1",
                                      remote_vtep_ipv4        = "0.0.0.0",
                                      remote_vm_static_mac    = multivalue_static_mac,
                                      remote_vm_static_ipv4   = "0.0.0.0",
                                      remote_info_active      = "1",
                                      ip_to_vxlan_multiplier  = "1")


device_group_vxlan_handle_2 = Create_Device_Group(topology_handle = device_group_handle_2,
                                                name = 'VLAN-1',
                                                multiplier = '3')


multivalue_mac = Create_Multivalue(pattern           = "counter",
                                   counter_start     = "00.14.01.00.00.01",
                                   counter_step      = "00.00.00.00.00.01",
                                   counter_direction = "increment",
                                   nest_step         = "00.00.00.00.00.01,00.00.01.00.00.00",
                                   nest_owner        = '%s,%s' % (device_group_handle_2, topology_handle_2),
                                   nest_enabled      = "0,1")
                                                

ethernet_handle_2 = Config_Protocol_Interface(protocol_name           = "{Vlan}",
                                              protocol_handle         = device_group_vxlan_handle_2,
                                              connected_to_handle     = vxlan_handle_2,
                                              mtu                     = "1500",
                                              src_mac_addr            = multivalue_mac,
                                              vlan                    = "0",
                                              vlan_id                 = "1",
                                              vlan_id_step            = "0",
                                              vlan_id_count           = "1",
                                              vlan_tpid               = "0x8100",
                                              vlan_user_priority      = "0",
                                              vlan_user_priority_step = "0",
                                              use_vpn_parameters      = "0",
                                              site_id                 = "0")

# /topology:2/deviceGroup:1/deviceGroup:1/ethernet:1
ethernet_handle_2 = ethernet_handle_2['ethernet_handle']

multivalue_ipv4 = Create_Multivalue(pattern           = "counter",
                                    counter_start     = "10.1.1.10",
                                    counter_step      = "0.0.1.0",
                                    counter_direction = "increment",
                                    nest_step         = "0.0.0.1,0.1.0.0",
                                    nest_owner        = '%s,%s' % (device_group_handle_2, topology_handle_2),
                                    nest_enabled      = "0,1")

multivalue_gateway = Create_Multivalue(pattern           = "counter",
                                       counter_start     = "10.1.1.1",
                                       counter_step      = "0.0.1.0",
                                       counter_direction = "increment",
                                       nest_step         = "0.0.0.1,0.1.0.0",
                                       nest_owner        = '%s,%s' % (device_group_handle_2, topology_handle_2),
                                       nest_enabled      = "0,1")

# /topology:2/deviceGroup:1/deviceGroup:1/ethernet:1  
ipv4_handle_2 = Config_Protocol_Interface(protocol_name        = "{IPv4 2}",
                                          protocol_handle      = ethernet_handle_2,
                                          ipv4_resolve_gateway = "1",
                                          gateway              = multivalue_gateway,
                                          intf_ip_addr         = multivalue_ipv4,
                                          netmask              = "255.255.255.0")

# Use this handle for Traffic Item endpoint
# /topology:2/deviceGroup:1/deviceGroup:1/ethernet:1/ipv4:1
ipv4_handle_2 = ipv4_handle_2['ipv4_handle']

global_status = ixia_ngpf.emulation_vxlan_config(get_handle                 = 'no',
                                                 mode                       = "create",
                                                 handle                     = "/globals",
                                                 start_rate_enabled         = "0",
                                                 start_rate                 = "200",
                                                 start_rate_interval        = "1000",
                                                 start_rate_scale_mode      = "port",
                                                 stop_rate_enabled          = "0",
                                                 stop_rate                  = "200",
                                                 stop_rate_interval         = "1000",
                                                 stop_rate_scale_mode       = "port",
                                                 udp_dest                   = "4789",
                                                 igmp_mode                  = "igmpv3",
                                                 outer_ip_dest_mode         = "unicast")
    
Start_All_Protocols_Ngpf_Hlt()
time.sleep(10)

traffic_item = Config_Traffic_Item(mode='create',
                                   name='Traffic_Item_VxLAN',
                                   endpointset_count='1',
                                   circuit_endpoint_type='ipv4',
                                   emulation_src_handle=ipv4_handle_1,
                                   emulation_dst_handle=ipv4_handle_2,
                                   emulation_multicast_dst_handle='',
                                   emulation_multicast_dst_handle_type='',
                                   src_dest_mesh='one_to_one',
                                   route_mesh='one_to_one',
                                   bidirectional='1',
                                   frame_size='128',
                                   transmit_mode='single_burst',
                                   pkts_per_burst='10000',
                                   rate_percent='100',
                                   track_by='sourceDestValuePair0',
                                   allow_self_destined='0')
                                   

Start_Traffic_Ngpf_Hlt()

Get_Stats_Ngpf_Hlt()
