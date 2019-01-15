""" Demonstrates IxNetwork API server session configuration options on a linux platform
"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform


# setup the connection information for a windows gui test platform that has a default session of 1
# platform='linux' forces the scheme to https
# if the default platform='windows' is used a ConnectionError will be raised
# as the Linux API Server does not redirect but closes the connection
test_platform=TestPlatform('10.36.74.17', platform='linux')
test_platform.Trace = 'request_response'

# authenticate with username and password
test_platform.Authenticate('admin', 'admin')
api_key = test_platform.ApiKey

# if username/password is not acceptable to the client due to the unencrypted password
# an api key can be specified instead
# the api key can be retrieved from the linux api server user settings and provided 
# to the TestPlatform.ApiKey property which will be used in subsequent server requests
test_platform.ApiKey = api_key

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
