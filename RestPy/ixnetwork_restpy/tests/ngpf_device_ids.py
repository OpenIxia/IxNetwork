"""Demonstrates some best practices for specifying device ids when executing ngpf operations

"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform


# connect to a test platform, create a session and get the root IxNetwork object
test_platform = TestPlatform('127.0.0.1', rest_port=11009)
test_platform.Trace = 'request_response'
sessions = test_platform.Sessions.find(Id=1)
ixnetwork = sessions.Ixnetwork
ixnetwork.NewConfig()

# create a b2b ngpf scenario
vport_1 = ixnetwork.Vport.add().add().add()
vport_2 = ixnetwork.Vport.add()
topologies = ixnetwork.Topology.add(Vports=vport_1).add(Vports=vport_2)
ipv4_1 = topologies[0].DeviceGroup.add().Ethernet.add().Ipv4.add()
igmp_host = ipv4_1.IgmpHost.add()
ipv4_2 = topologies[1].DeviceGroup.add().Ethernet.add().Ipv4.add()
igmp_querier = ipv4_2.IgmpQuerier.add()

# get device ids for two specific ip addresses
ipv4_device_ids = ipv4_1.get_device_ids(Address='^(%s|%s)' % (ipv4_1.Address.Values[6], ipv4_1.Address.Values[24]))
assert(len(ipv4_device_ids) == 2)

# get device ids on two specific ports
port_device_ids = ipv4_1.get_device_ids(PortNames='^(%s|%s)$' % (vport_1[0].Name, vport_1[2].Name))
assert(len(port_device_ids) == 20)

# get device ids for igmp v2 hosts on a specific port
v2_device_ids = igmp_host.get_device_ids(PortNames='(?i)^%s$' % (vport_1[1].Name), VersionType='(?i)version2')
assert(len(v2_device_ids) == 10)

ipv4_1.Start(ipv4_device_ids)
igmp_host.IgmpMcastIPv4GroupList.Join(v2_device_ids)




