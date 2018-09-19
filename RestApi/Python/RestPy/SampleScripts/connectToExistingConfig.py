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
   - https://github.com/OpenIxia/IxNetwork/RestApi/Python/Restpy/Modules:
         - Statistics.py and PortMgmt.py 

Script development API doc:
   - The doc is located in your Python installation site-packages/ixnetwork_restpy/index.html
   - On a web browser, enter: file:///<full_path_to_ixnetwork_restpy>/index.html
"""

from __future__ import absolute_import, print_function
import os, sys

from ixnetwork_restpy.testplatform.testplatform import TestPlatform

sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules'))))
from StatisticsMgmt import Statistics
from PortMgmt import Ports

osPlatform = 'windows'

if osPlatform == 'windows':
    apiServerIp = '192.168.70.3'
    apiServerPort = 11009

if osPlatform == 'linux':
    apiServerIp = '192.168.70.121'
    apiServerPort = 443
    username = 'admin'
    password = 'password'

licenseServerIp = ['192.168.70.3']
licenseMode = 'subscription'

ixChassisIp = '192.168.70.120'
portList = [[ixChassisIp, 1, 1], [ixChassisIp, 1, 2]]

try:
    testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, platform=osPlatform)

    # Console output verbosity: None|request|request_response
    testPlatform.Trace = 'request_response'

    if osPlatform == 'linux':
        testPlatform.Authenticate(username, password)
        # How to connect to an existing session ID
        ixNetwork.ApiKey = '9277fc8fe92047f6a126f54481ba07fc'
        session = ixNetwork.Sessions(Id=1)
        ixNetwork = session.Ixnetwork

    if osPlatform == 'windows':
        # Windows support only one session. Id is always equal 1.
        session = testPlatform.Sessions.find(Id=1)
    
    # ixNetwork is the root object to the IxNetwork API hierarchical tree.
    ixNetwork = session.Ixnetwork

    # Instantiate the helper class objects
    statObj = Statistics(ixNetwork)
    portObj = Ports(ixNetwork)

except Exception as errMsg:
    print('\nrestPy.Exception:', errMsg)
