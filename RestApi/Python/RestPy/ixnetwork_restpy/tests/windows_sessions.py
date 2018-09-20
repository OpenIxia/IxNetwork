""" Demonstrates IxNetwork GUI session configuration options on a windows platform
"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform


# setup the connection information for a windows gui test platform that has a default session of 1
test_platform=TestPlatform('127.0.0.1', rest_port=11009, platform='windows')

# get a list of sessions
for session in test_platform.Sessions.find():
	print(session)

# add a session and remove the session
sessions = test_platform.Sessions.add()
print(sessions)
sessions.remove()

# get an invalid session
sessions = test_platform.Sessions.find(Id=6)
assert(len(sessions) == 0)

# get a valid session
sessions = test_platform.Sessions.find(Id=1)
assert(len(sessions) == 1)