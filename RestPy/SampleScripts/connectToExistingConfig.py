"""
connectToExistingConfig.py

   Connecting to an existing session.
      - For Windows, the default session ID=1.
      - For Windows Connection Mgr, session ID=?
      - For Linux, you need to:
          - Login
          - Include your API-Key
          - Session ID

Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements
   - IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install -U --no-cache-dir ixnetwork_restpy
   - Helper functions: https://github.com/OpenIxia/IxNetwork/RestApi/Python/Restpy/Modules:
                       - Statistics.py and PortMgmt.py

Script development API doc:
   - The doc is located in your Python installation site-packages/ixnetwork_restpy/docs/index.html
   - On a web browser:
         - If installed in Windows: enter: file://c:/<path_to_ixnetwork_restpy>/docs/index.html
         - If installed in Linux: enter: file:///<path_to_ixnetwork_restpy>/docs/index.html
"""

import os, sys
# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform

# If you got RestPy by doing a git clone instead of using pip, uncomment this line so
# your system knows where the RestPy modules are located.
#sys.path.append(os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', '')))

# This sample script uses helper functions from https://github.com/OpenIxia/IxNetwork/tree/master/RestPy/Modules
# If you did a git clone, add this path to use the helper modules: StatisticsMgmt.py and PortMgmt.py
# Otherwise, you could store these helper functions any where on your filesystem and set their path by using sys.path.append('your path')
sys.path.append(os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules')))

# Import modules containing helper functions
from StatisticsMgmt import Statistics
from PortMgmt import Ports

# Defaulting to windows
osPlatform = 'windows'

if len(sys.argv) > 1:
    # Command line input: windows, windowsConnectionMgr or linux
    osPlatform = sys.argv[1]

# Change API server values to use your setup
if osPlatform in ['windows', 'windowsConnectionMgr']:
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

    # Console output verbosity: None|request|request_response
    testPlatform.Trace = 'request_response'

    if osPlatform == 'linux':
        testPlatform.Authenticate(username, password)
        ixNetwork.ApiKey = '9277fc8fe92047f6a126f54481ba07fc'
        session = ixNetwork.Sessions(Id=8)
        ixNetwork = session.Ixnetwork

    if osPlatform == 'windows':
        # Windows support only one session. Id is always equal 1.
        session = testPlatform.Sessions.find(Id=1)
    
    # ixNetwork is the root object to the IxNetwork API tree.
    ixNetwork = session.Ixnetwork

    # Instantiate the helper class objects
    statObj = Statistics(ixNetwork)
    portObj = Ports(ixNetwork)


except Exception as errMsg:
    print('\nrestPy.Exception:', errMsg)
