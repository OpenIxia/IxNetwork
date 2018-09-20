"""Demonstrates creating a traffic item that uses ipv4 endpoints.

"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform

# connect to a test platform, create a session and get the root IxNetwork object
test_platform = TestPlatform('127.0.0.1', rest_port=11009)
test_platform.Trace = 'none'
sessions = test_platform.Sessions.find(Id=1)
ixnetwork = sessions.Ixnetwork

# clear the configuration
ixnetwork.NewConfig()

# create 2 ipv4 endpoints
ipv4_1 = ixnetwork.Topology.add(Vports=ixnetwork.Vport.add()).DeviceGroup.add().Ethernet.add().Ipv4.add(Name='Ipv4 West')
ipv4_2 = ixnetwork.Topology.add(Vports=ixnetwork.Vport.add()).DeviceGroup.add().Ethernet.add().Ipv4.add(Name='Ipv4 East')

# create an ipv4 traffic item
traffic_item = ixnetwork.Traffic.TrafficItem.add(Name='Ipv4 Traffic Item Sample', TrafficType='ipv4', TrafficItemType='l2L3')

# create an endpoint set using the ipv4 objects
endpoint_set = traffic_item.EndpointSet.add(Sources=ipv4_1, Destinations=ipv4_2)
assert (len(endpoint_set.Sources) == 1)
assert (len(endpoint_set.Destinations) == 1)
assert (len(traffic_item.ConfigElement.find().Stack.find(StackTypeId='ipv4')) == 1)
