"""Demonstrates creating a traffic item that uses scalable sources and igmp multicast receivers.

"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform

# connect to a test platform, create a session and get the root IxNetwork object
test_platform = TestPlatform('127.0.0.1', rest_port=11009)
test_platform.Trace = 'request_response'
sessions = test_platform.Sessions.find(Id=1)
ixnetwork = sessions.Ixnetwork

# clear the configuration
ixnetwork.NewConfig()

# create 2 igmp endpoints
ipv4_1 = ixnetwork.Topology.add(Vports=ixnetwork.Vport.add()).DeviceGroup.add().Ethernet.add().Ipv4.add()
igmp_host = ipv4_1.IgmpHost.add(Name='Igmp Host')
ipv4_2 = ixnetwork.Topology.add(Vports=ixnetwork.Vport.add().add().add()).DeviceGroup.add().Ethernet.add().Ipv4.add()
igmp_querier = ipv4_2.IgmpQuerier.add(Name='Igmp Querier')

# create a scalable sources object to be used in creating traffic
# arg1=ngpfObjectReference arg2=1 based port index, arg3=portCount, arg4=startingDeviceIndex, arg5=deviceCount
scalable_sources = [
	{
		'arg1': ipv4_2.href,
		'arg2': 1,
		'arg3': 3,
		'arg4': 1,
		'arg5': 2
	},
	{
		'arg1': ipv4_2.href,
		'arg2': 1,
		'arg3': 3,
		'arg4': 9,
		'arg5': 2
	}
]
# create a multicast receiver object to be used in creating traffic
# arg1=IgmpMcastIPv4GroupList.href, arg2=0 based port index, arg3=0 based host index, arg4=0 based group or prune/join index
multicast_receivers = [
	{
		'arg1': igmp_host.IgmpMcastIPv4GroupList.href,
		'arg2': 0,
		'arg3': 3,
		'arg4': 0
	},
	{
		'arg1': igmp_host.IgmpMcastIPv4GroupList.href,
		'arg2': 0,
		'arg3': 4,
		'arg4': 0
	},
	{
		'arg1': igmp_host.IgmpMcastIPv4GroupList.href,
		'arg2': 0,
		'arg3': 6,
		'arg4': 0
	},
	{
		'arg1': igmp_host.IgmpMcastIPv4GroupList.href,
		'arg2': 0,
		'arg3': 9,
		'arg4': 0
	}	
]

# create a traffic item using the scalable sources and multicast receivers
traffic_item = ixnetwork.Traffic.TrafficItem.add(Name='Ipv4 Traffic Item Sample', TrafficType='ipv4', TrafficItemType='l2L3')
endpoint_set = traffic_item.EndpointSet.add(ScalableSources=scalable_sources, MulticastReceivers=multicast_receivers)
assert (len(endpoint_set.MulticastReceivers) == 4)
assert (len(endpoint_set.ScalableSources) == 2)
assert (len(traffic_item.ConfigElement.find().Stack.find(StackTypeId='ipv4')) == 1)
