"""Demonstrates an approach for clearing ownership on vports that are connected 
by using the Vport.ConnectedTo reference and obtaining the Port object which has the ClearOwnership method

"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform


# connect to a test platform, create a session and get the root IxNetwork object
test_platform = TestPlatform('127.0.0.1', rest_port=11009)
test_platform.Trace = 'request_response'
sessions = test_platform.Sessions.find(Id=1)
ixnetwork = sessions.Ixnetwork
ixnetwork.NewConfig()

# add a chassis
chassis = ixnetwork.AvailableHardware.Chassis.add(Hostname='10.36.74.17')

# add abstract ports and connect them to chassis ports
card = chassis.Card.find(CardId=1)
for port in card.Port.find():
	ixnetwork.Vport.add(ConnectedTo=port)

# clear the ownership on the port using a reference returned by the Vport.ConnectedTo property
for vport in ixnetwork.Vport.find():
	port = sessions.GetObjectFromHref(vport.ConnectedTo)
	if port is not None:
		port.ClearOwnership()


