"""
manageSessions.py

   Connect to a Linux API server
      - View or delete open sessions

Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements
   - IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install -U --no-cache-dir ixnetwork_restpy

Script development API doc:
   - The doc is located in your Python installation site-packages/ixnetwork_restpy/docs/index.html
   - On a web browser:
         - If installed in Windows: enter: file://c:/<path_to_ixnetwork_restpy>/docs/index.html
         - If installed in Linux: enter: file:///<path_to_ixnetwork_restpy>/docs/index.html
"""

import os, sys
# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform

osPlatform = 'linux'

if len(sys.argv) > 1:
    # Command line input: windows, windowsConnectionMgr or linux
    osPlatform = sys.argv[1]

# Change API server values to use your setup
if osPlatform == 'windowsConnectionMgr':
    platform = 'windows'
    apiServerIp = '192.168.70.3'
    apiServerPort = 11009

# Change API server values to use your setup
if osPlatform == 'linux':
    platform = 'linux'
    apiServerIp = '192.168.70.12'
    apiServerPort = 443
    username = 'admin'
    password = 'admin'

try:
    testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, platform=platform)

    # Display debug loggings
    testPlatform.Trace = 'request_response'
    
    # authenticate with username and password
    testPlatform.Authenticate('admin', 'admin')

    # Show all open sessions
    for session in testPlatform.Sessions.find():
        print(session)

    # Delete a particular session ID
    #testPlatform.Sessions.find(Id=11).remove()
    
    testPlatform.Sessions.find(Id=1).remove()

except Exception as errMsg:
    print('\nrestPy.Exception:', errMsg)
