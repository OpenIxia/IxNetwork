"""
connectToExistingConfig.py

   Connecting to an existing session.
      - For Windows, the default session ID=1.
      - For Windows Connection Mgr, session ID=?
      - For Linux, there are two ways to login:
          1> Login with username/password
          2> Use the API-Key instead.

          - Then provide the Session ID to connect into.

Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements
   - IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install -U --no-cache-dir ixnetwork_restpy

RestPy Doc:
    https://www.openixia.com/userGuides/restPyDoc
"""

import os, sys, time, traceback
# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.files import Files
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant

# Set defaults
# Options: windows|connection_manager|linux
osPlatform = 'windows' 

apiServerIp = '192.168.70.3'

# windows:11009. linux:443. connection_manager:443
apiServerPort = 11009

# For Linux API server only
username = 'admin'
password = 'admin'

# Allow passing in some params/values from the CLI to replace the defaults
if len(sys.argv) > 1:
    # Command line input:
    #   osPlatform: windows, connection_manager or linux
    osPlatform = sys.argv[1]
    apiServerIp = sys.argv[2]
    apiServerPort = sys.argv[3]    

try:
    testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, platform=osPlatform, log_file_name='restpy.log')
    # Console output verbosity: None|request|request_response
    testPlatform.Trace = 'request_response'

    if osPlatform == 'linux':
        # There are two ways to log into an existing linux session ID

        # 1> Provide the login account username and password
        testPlatform.Authenticate(username, password)
        session = testPlatform.Sessions.find(Id=4)

        # 2> Or use the API-Key instead. The API-Key could be retrieve from the Linux api server under 
        #    settings, My Account.
        #testPlatform.ApiKey = '604348999bc34d028043347f713e49ce'
        #session = testPlatform.Sessions.find(Id=4)

    if osPlatform in ['windows', 'connection_manager']:
        # Windows support only one session. Id is always equal 1.
        session = testPlatform.Sessions.find(Id=1)
    
    # ixNetwork is the root object to the IxNetwork API tree.
    ixNetwork = session.Ixnetwork


except Exception as errMsg:
    print('\nError: %s' % traceback.format_exc())
    print('\nrestPy.Exception:', errMsg)
