"""
loadJsonConfigFile.py:

   Tested with two back-2-back Ixia ports

   - Connect to the API server
   - Configure license server IP
   - Loads a saved .json config file that is in the same local directory: bgp.json
   - Configure license server IP
   - Optional: Assign ports or use the ports that are in the saved config file.
   - Demonstrate how to use XPATH to modify any part of the configuration.
   - Start all protocols
   - Verify all protocols
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

import json, sys, os, traceback

# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.files import Files
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant

# If you installed RestPy by doing a git clone instead of using pip, uncomment this line so
# your system knows where the RestPy modules are located.
#sys.path.append(os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', '')))

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

jsonConfigFile = 'bgp.json'

try:
    testPlatform = TestPlatform(apiServerIp, apiServerPort, platform=platform, log_file_name='restpy.log')

    # Console output verbosity: None|request|request_response
    testPlatform.Trace = 'request_response'

    if osPlatform == 'linux':
        testPlatform.Authenticate(username, password)

    if osPlatform in ['linux', 'windowsConnectionMgr']:
        session = testPlatform.Sessions.add()

    if osPlatform == 'windows':
        session = testPlatform.Sessions.find(Id=1)

    # ixNetwork is the root object to the IxNetwork API hierarchical tree.
    ixNetwork = session.Ixnetwork

    if osPlatform == 'windows':
        ixNetwork.NewConfig()

    ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
    ixNetwork.Globals.Licensing.Mode = licenseMode

    ixNetwork.info('\nLoading JSON config file: {0}'.format(jsonConfigFile))
    ixNetwork.ResourceManager.ImportConfigFile(Files(jsonConfigFile, local_file=True), Arg3=True)

    # Assigning ports after loading a saved config is optional because you could use the ports that
    # are saved in the config file. Optionally, reassign ports to use other chassis/ports on different testbeds.
    # getVportList=True because vports are already configured in the config file.
    testPorts = []
    vportList = [vport.href for vport in ixNetwork.Vport.find()]
    for port in portList:
        testPorts.append(dict(Arg1=port[0], Arg2=port[1], Arg3=port[2]))

    ixNetwork.AssignPorts(testPorts, [], vportList, forceTakePortOwnership)

    # Example: How to modify a loaded json config using XPATH
    # Arg3:  True=To create a new config. False=To modify an existing config.
    data = json.dumps([{"xpath": "/traffic/trafficItem[1]", "name": 'Modified Traffic'}])
    ixNetwork.ResourceManager.ImportConfig(Arg2=data, Arg3=False)

    ixNetwork.StartAllProtocols(Arg1='sync')

    ixNetwork.info('Verify protocol sessions\n')
    protocolsSummary = StatViewAssistant(ixNetwork, 'Protocols Summary')
    protocolsSummary.CheckCondition('Sessions Not Started', StatViewAssistant.EQUAL, 0)
    protocolsSummary.CheckCondition('Sessions Down', StatViewAssistant.EQUAL, 0)
    ixNetwork.info(protocolsSummary)

    # Get the Traffic Item name for getting Traffic Item statistics.
    trafficItem = ixNetwork.Traffic.TrafficItem.find()[0]

    trafficItem.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()

    # StatViewAssistant could also filter by REGEX, LESS_THAN, GREATER_THAN, EQUAL. 
    # Examples:
    #    flowStatistics.AddRowFilter('Port Name', StatViewAssistant.REGEX, '^Port 1$')
    #    flowStatistics.AddRowFilter('Tx Frames', StatViewAssistant.LESS_THAN, 50000)

    flowStatistics = StatViewAssistant(ixNetwork, 'Flow Statistics')
    ixNetwork.info('{}\n'.format(flowStatistics))

    for rowNumber,flowStat in enumerate(flowStatistics.Rows):
        ixNetwork.info('\n\nSTATS: {}\n\n'.format(flowStat))
        ixNetwork.info('\nRow:{}  TxPort:{}  RxPort:{}  TxFrames:{}  RxFrames:{}\n'.format(
            rowNumber, flowStat['Tx Port'], flowStat['Rx Port'],
            flowStat['Tx Frames'], flowStat['Rx Frames']))

    if deleteSessionWhenDone:
        # For Linux and WindowsConnectionMgr only
        if osPlatform in ['linux', 'windowsConnectionMgr']:
            session.remove()

except Exception as errMsg:
    ixNetwork.debug('\n%s' % traceback.format_exc())
    if deleteSessionWhenDone and 'session' in locals():
        if osPlatform in ['linux', 'windowsConnectionMgr']:
            session.remove()




