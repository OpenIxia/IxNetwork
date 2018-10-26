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
   - The doc is located in your Python installation site-packages/ixnetwork_restpy/docs/index.html
   - On a web browser:
         - If installed in Windows: enter: file://c:/<path_to_ixnetwork_restpy>/docs/index.html
         - If installed in Linux: enter: file:///<path_to_ixnetwork_restpy>/docs/index.html
"""

from __future__ import absolute_import, print_function
import os, sys

# Adding some relevant paths if you are not installing RestPy by Pip.
sys.path.append(os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', '')))
sys.path.append(os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules')))

# Import the main client module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform

# Import modules containing helper functions
from StatisticsMgmt import Statistics
from PortMgmt import Ports

if len(sys.argv) > 1:
    # Command line input: windows or linux
    osPlatform = sys.argv[1]
else:
    # Default to windows
    osPlatform = 'windows'

# Are you using IxNetwork Connection Manager in a Windows server 2012/2016?
isWindowsConnectionMgr = False

if osPlatform == 'windows':
    platform = 'windows'
    apiServerIp = '192.168.70.3'
    apiServerPort = 11009

if osPlatform == 'linux':
    platform = 'linux'
    apiServerIp = '192.168.70.9'
    apiServerPort = 443
    username = 'admin'
    password = 'password'

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

    ipv4 = ixNetwork.Topology.find(Name='Topo1').DeviceGroup.find(Name='DG1').Ethernet.find(Name='Eth1').Ipv4.find(Name='Ipv4')
    print(ipv4)
    #ipv4.SendArp(2)

except Exception as errMsg:
    print('\nrestPy.Exception:', errMsg)
