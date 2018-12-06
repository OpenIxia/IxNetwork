"""Demonstrates creating a raw traffic item over vport endpoints.

"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform

# connect to a test platform, create a session and get the root IxNetwork object
test_platform = TestPlatform('127.0.0.1', rest_port=11009, platform='windows')
test_platform.Trace = 'request_response'
sessions = test_platform.Sessions.find(Id=1)
ixnetwork = sessions.Ixnetwork

# clear the configuration
ixnetwork.NewConfig()

# create two vport objects
vport_1 = ixnetwork.Vport.add()
vport_2 = ixnetwork.Vport.add()

# create a raw traffic item
traffic_item = ixnetwork.Traffic.TrafficItem.add(Name='Raw Traffic Item Sample', TrafficType='raw', TrafficItemType='l2L3')

# raw traffic endpoints must be Vport.Protocols objects
# create an endpoint set using the Vport.Protocols objects
endpoint_set = traffic_item.EndpointSet.add(Sources=vport_1.Protocols.find(), Destinations=vport_2.Protocols.find())
assert (len(endpoint_set.Sources) == 1)
assert (len(endpoint_set.Destinations) == 1)
