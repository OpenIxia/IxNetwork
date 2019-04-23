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

RestPy Doc:
    https://www.openixia.com/userGuides/restPyDoc

Usage:
   # Defaults to Windows
   - Enter: python <script>

   # Connect to Windows Connection Manager
   - Enter: python <script> connection_manager <apiServerIp> 443

   # Connect to Linux API server
   - Enter: python <script> linux <apiServerIp> 443
"""

import json, sys, os, traceback

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

# The IP address for your Ixia license server(s) in a list.
licenseServerIp = ['192.168.70.3']
# subscription, perpetual or mixed
licenseMode = 'subscription'
# tier1, tier2, tier3, tier3-10g
licenseTier = 'tier3'

# For linux and windowsConnectionMgr only. Set to True to leave the session alive for debugging.
debugMode = False

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True

# A list of chassis to use
ixChassisIpList = ['192.168.70.128']
portList = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 2, 1]]

jsonConfigFile = 'bgp_ngpf_8.50.json'

try:
    testPlatform = TestPlatform(apiServerIp, apiServerPort, platform=osPlatform, log_file_name='restpy.log')

    # Console output verbosity: None|request|'request response'
    testPlatform.Trace = 'request_response'

    testPlatform.Authenticate(username, password)
    session = testPlatform.Sessions.add()
    ixNetwork = session.Ixnetwork
    ixNetwork.NewConfig()

    ixNetwork.info('\nLoading JSON config file: {0}'.format(jsonConfigFile))
    ixNetwork.ResourceManager.ImportConfigFile(Files(jsonConfigFile, local_file=True), Arg3=True)

    ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
    ixNetwork.Globals.Licensing.Mode = licenseMode
    ixNetwork.Globals.Licensing.Tier = licenseTier

    # Assign ports
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

    if debugMode == False:
        # For Linux and connection_manager only
            session.remove()

except Exception as errMsg:
    print('\n%s' % traceback.format_exc())
    if debugMode == False and 'session' in locals():
        session.remove()




