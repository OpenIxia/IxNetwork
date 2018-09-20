"""Demonstrates some best practices for using resource manager to import and export the configuration as json

"""

import json
from ixnetwork_restpy.testplatform.testplatform import TestPlatform

# connect to a test platform, create a session and get the root IxNetwork object
test_platform = TestPlatform('127.0.0.1', rest_port=11009)
test_platform.Trace = 'none'
sessions = test_platform.Sessions.find(Id=1)
ixnetwork = sessions.Ixnetwork

# create two virtual ports by importing them as json
vports = [
    {
        'xpath': '/vport[1]',
        'name': 'vport 1'
    },
    {
        'xpath': '/vport[2]',
        'name': 'vport 2'
    }
]
ixnetwork.ResourceManager.ImportConfig(json.dumps(vports), True)
assert(len(ixnetwork.Vport.find()) == 2)

# export the entire configuration as a string
config = ixnetwork.ResourceManager.ExportConfig(['/descendant-or-self::*'], False, 'json')

# import the entire configuration
ixnetwork.ResourceManager.ImportConfig(config, True)
assert(len(ixnetwork.Vport.find()) == 2)
