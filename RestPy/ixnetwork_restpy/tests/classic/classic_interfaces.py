"""Demonstrates adding interfaces to virtual ports.

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
interfaces = ixnetwork.Vport.add(Name='Test Port 1').Interface

# add 10 interfaces
for i in range(1, 11):
	interfaces.add(Description='Interface Demo %s' % i, Enabled=True)

# verify they have been added on the server
assert(len(interfaces.find()) == 10)
