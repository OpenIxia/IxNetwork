"""This sample demonstrates customizing a traffic item stack.

"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform

# connect to a test platform, create a session and get the root IxNetwork object
test_platform = TestPlatform('127.0.0.1', rest_port=11009)
test_platform.Trace = 'none'
sessions = test_platform.Sessions.find(Id=1)
ixnetwork = sessions.Ixnetwork

# clear the configuration
ixnetwork.NewConfig()

# create two vport objects
vport_1 = ixnetwork.Vport.add()
vport_2 = ixnetwork.Vport.add()

# create a raw traffic item
traffic_item = ixnetwork.Traffic.TrafficItem.add(Name='Raw Traffic Item Sample', TrafficType='raw', TrafficItemType='l2L3')
endpoint_set = traffic_item.EndpointSet.add(Sources=vport_1.Protocols, Destinations=vport_2.Protocols)

# append protocol templates to the traffic item
config_element = traffic_item.ConfigElement.find(EndpointSetId=1)
ethernet_stack = config_element.Stack.find(StackTypeId='^ethernet$')

# get the protocol templates to be appended
vlan_protocol_template = ixnetwork.Traffic.ProtocolTemplate.find(StackTypeId='^vlan$')
ipv4_protocol_template = ixnetwork.Traffic.ProtocolTemplate.find(StackTypeId='^ipv4$')
udp_protocol_template = ixnetwork.Traffic.ProtocolTemplate.find(StackTypeId='^udp$')

# append the protocol templates and get the newly appended stack object using the returned href
vlan_stack = config_element.Stack.read(ethernet_stack.AppendProtocol(vlan_protocol_template))
ipv4_stack = config_element.Stack.read(vlan_stack.AppendProtocol(ipv4_protocol_template))
udp_stack = config_element.Stack.read(ipv4_stack.AppendProtocol(udp_protocol_template))

