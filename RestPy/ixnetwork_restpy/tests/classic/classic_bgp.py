"""Demonstrates adding a bgp neighbor range to a virtual port.

"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform


# connect to a test platform, create a session and get the root IxNetwork object
test_platform = TestPlatform('127.0.0.1', rest_port=11009)
test_platform.Trace = 'none'
sessions = test_platform.Sessions.find(Id=1)
ixnetwork = sessions.Ixnetwork

# clear the configuration
ixnetwork.NewConfig()

# add a virtual port and get the interface object
vport = ixnetwork.Vport.add(Name='Test Port 1')

# add an interface
interface = vport.Interface.add(Enabled=True)
ipv4 = interface.Ipv4.add(Ip='1.1.1.1', Gateway='1.1.2.1')

# enable bgp
bgp = vport.Protocols.find().Bgp
bgp.Enabled = True

# add a bgp neighbor range
neighbor_range = bgp.NeighborRange.add(Interfaces=interface, Enabled=True, EnableBgpId=True)

# verify the neighbor range has been added on the server
assert(len(neighbor_range.find()) == 1)
