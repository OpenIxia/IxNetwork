"""A simple script that demonstrates how to get started with ixnetwork_restpy scripting.

"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform


# connect to a windows test platform using the default api server rest port
test_platform = TestPlatform('127.0.0.1', rest_port=11009, platform='windows')

# use the default session and get the root node of the hierarhcy
ixnetwork = test_platform.Sessions.find().Ixnetwork

vports = ixnetwork.Vport.find()
vport1 = vports[0]
print(vport1)
vport2 = vports[1]
print(vport2)
ixnetwork.info('end of index test')
vport_list = list(vports)
ixnetwork.info('end of list test')
print(vport_list)
ixnetwork.info('end of tests')
# # clear any configuration that may be present
# ixnetwork.NewConfig()

# # add a virtual port
# vport = ixnetwork.Vport.add(Name='Abstract Test Port 1')

# # add 10 ipv4 devices
# ipv4_devices = ixnetwork.Topology.add(Ports=vport).DeviceGroup.add(Multiplier=10).Ethernet.add().Ipv4.add()
