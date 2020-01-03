"""
connectToExistingConfig.py

   Connecting to an existing session.

Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements
   - IxNetwork 8.50
   - Minimum RestPy version 1.0.33
   - Python 2.7 and 3+
   - pip install requests
   - pip install -U --no-cache-dir ixnetwork_restpy

RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy
"""

import os, sys, time, traceback
# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.files import Files
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant

apiServerIp = '192.168.70.12'

# windows|connection_manager|linux
osPlatform = 'linux'

# For Linux API server only
username = 'admin'
password = 'admin'

try:
    testPlatform = TestPlatform(apiServerIp, log_file_name='restpy.log')

    # Console output verbosity: 'none'|request|request_response
    testPlatform.Trace = 'request_response'

    if osPlatform == 'linux':
        # There are two ways to log into an existing linux session

        # 1> Provide the login account username and password
        testPlatform.Authenticate(username, password)

        # 2> Or use the API-Key instead. 
        # The API-Key could be retrieve from the Linux api server under settings, My Account.
        #testPlatform.ApiKey = '604348999bc34d028043347f713e49ce'

        # After logging in, there are two ways to connect to a specific session.
        session = testPlatform.Sessions.find(Id=2)
        #session = testPlatform.Sessions.find(Name='devTest')

    if osPlatform in ['windows', 'connection_manager']:
        # Windows support only one session. Id is always equal 1.
        session = testPlatform.Sessions.find(Id=1)

    # ixNetwork is the root object to the IxNetwork API tree.
    ixNetwork = session.Ixnetwork


except Exception as errMsg:
    print('\nError: %s' % traceback.format_exc())
    print('\nrestPy.Exception:', errMsg)
