"""
loadConfigFile.py:

   Tested with two back-2-back Ixia ports

   - Connect to the API server
   - Configure license server IP
   - Loads a saved .ixncfg config file that is in the same local directory: bgp_ngpf_8.30.ixncfg
   - Configure license server IP
   - Optional: Assign ports or use the ports that are in the saved config file.
   - Start all protocols
   - Verify all protocols
   - Modify the config by using JSON XPath.
   - Start traffic 
   - Get Traffic Item
   - Get Flow Statistics stats

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

Usage:
   # Defaults to Windows
   - Enter: python <script>

   # Connect to Windows Connection Manager
   - Enter: python <script> windowsConnectionMgr

   # Connect to Linux API server
   - Enter: python <script> linux

"""

import json, sys, os

# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.files import Files

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
    # Command line input: windows or linux
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

# The IP address for your Ixia license server(s) in a list.
licenseServerIp = ['192.168.70.3']
# subscription, perpetual or mixed
licenseMode = 'subscription'

# For linux and windowsConnectionMgr only. Set to False to leave the session alive for debugging.
deleteSessionWhenDone = True

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True

# A list of chassis to use
ixChassisIpList = ['192.168.70.128']
portList = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 1, 2]]

configFile = 'bgp_ngpf_8.30.ixncfg'

# The traffic item name to get stats from for this sample script
trafficItemName = 'Topo-BGP'

try:
    testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, platform=platform, log_file_name='restpy.log')

    # Console output verbosity: None|request|request_response
    testPlatform.Trace = 'request_response'

    if osPlatform == 'linux':
        testPlatform.Authenticate(username, password)

    session = testPlatform.Sessions.add()
    ixNetwork = session.Ixnetwork

    # Instantiate the helper class objects
    statObj = Statistics(ixNetwork)
    portObj = Ports(ixNetwork)

    if osPlatform == 'windows':
        ixNetwork.NewConfig()

    ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
    ixNetwork.Globals.Licensing.Mode = licenseMode

    print('\nLoading config file: {0}'.format(configFile))
    ixNetwork.LoadConfig(Files(configFile, local_file=True))

    print('\nAssigning ports/Rebooting ports')
    # Assigning ports after loading a saved config is optional because you could use the ports that
    # are saved in the config file. Optionally, reassign ports to use other chassis/ports on different testbeds.
    # getVportList=True because vports are already configured in the config file.
    portObj.assignPorts(portList, forceTakePortOwnership, getVportList=True)

    # Example: How to modify a loaded config using JSON's exported config XPATH
    data = json.dumps([{"xpath": "/topology[1]", "name": 'Topo-BGP-1'}])
    ixNetwork.ResourceManager.ImportConfig(Arg2=data, Arg3=False)

    ixNetwork.StartAllProtocols(Arg1='sync')
    statObj.verifyAllProtocolSessions()

    # Get the Traffic Item name for getting Traffic Item statistics.
    trafficItem = ixNetwork.Traffic.TrafficItem.find()[0]

    trafficItem.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()

    stats = statObj.getTrafficItemStats()
    
    # Get the statistic values
    txFrames = stats[trafficItem.Name]['Tx Frames']
    rxFrames = stats[trafficItem.Name]['Rx Frames']
    print('\nTraffic Item Stats:\n\tTxFrames: {}  RxFrames: {}\n'.format(txFrames, rxFrames))

    # This example is for getting Flow Statistics.
    flowStats = statObj.getFlowStatistics()

    for row, statValues in flowStats.items():
        txFrames = statValues['Tx Frames']
        rxFrames = statValues['Rx Frames']
        print('Flow Statistics: Row:{} TxFrames: {}  RxFrames: {}\n'.format(row, txFrames, rxFrames))

    if deleteSessionWhenDone:
        # For Linux and WindowsConnectionMgr only
        if osPlatform in ['linux', 'windowsConnectionMgr']:
            session.remove()

except Exception as errMsg:
    print('\nrestPy.Exception:', errMsg)
    if deleteSessionWhenDone and 'session' in locals():
        if osPlatform in ['linux', 'windowsConnectionMgr']:
            session.remove()





