""" Demonstrates IxNetwork API server session configuration options on a linux platform
"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform


# setup the connection information for a windows gui test platform that has a default session of 1
test_platform=TestPlatform('10.36.78.53', platform='linux')
test_platform.Trace = 'request_response'
test_platform.Authenticate('admin', 'admin')

# get a list of sessions
for session in test_platform.Sessions.find():
	print(session)

# add a session
sessions = test_platform.Sessions.add()
session_id = sessions.Id
print(sessions)

# remove the session
sessions.remove()
assert (len(sessions) == 0)

# attempt to get the removed session
sessions = test_platform.Sessions.find(session_id)
assert(len(sessions) == 0)
