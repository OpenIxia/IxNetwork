"""Demonstrates the best practice for connecting vport(s) to hardware test ports.

AssignPorts is currently the optimal method for connecting hardware test ports to vport(s).

The AssignPorts method on the test platform does the following:
	- adds chassis to /availableHardware using Arg1
	- creates abstract ports if the abstract port list (Arg3) cannot meet the number of Arg1 test ports
	- clears ownership of test ports if Arg4 is True
	- waits until port statistic view for all test ports are ready
	- returns a list of abstract test ports that have not been connected to test ports
"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform


# connect to a test platform, create a session and get the root IxNetwork object
test_platform = TestPlatform('127.0.0.1', rest_port=11009)
test_platform.Trace = 'request_response'
sessions = test_platform.Sessions.find(Id=1)
ixnetwork = sessions.Ixnetwork
ixnetwork.NewConfig()

# add abstract ports
vports = ixnetwork.Vport.find()
for i in range(2):
	vports.add(Name='Abstract Port %s' % i)
print(vports)

# connect the abstract ports to test ports
chassis_ip = '10.36.24.55'
test_ports = [
	dict(Arg1=chassis_ip, Arg2=1, Arg3=1),
	dict(Arg1=chassis_ip, Arg2=1, Arg3=2)
]
unconnected_ports = ixnetwork.AssignPorts(test_ports, [], vports, True)

