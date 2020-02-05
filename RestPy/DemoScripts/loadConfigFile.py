"""
loadConfigFile.py:

   Tested with two back-2-back Ixia ports

   - Connect to the API server
   - Configure license server IP
   - Load a saved config file
   - Configure license server IP
   - Optional: Assign ports or use the ports that are in the saved config file.
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
   - pip install ixnetwork_restpy

RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy

Usage:
   - Enter: python <script>
"""

import json, sys, os, traceback

# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.files import Files
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant
from ixnetwork_restpy.assistants.ports.portmapassistant import PortMapAssistant

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = False

try:
    testPlatform = TestPlatform(ip_address='192.168.70.3', log_file_name='restpy.log')

    # Console output verbosity: none|info|warning|request|request_response|all
    testPlatform.Trace = 'info'

    testPlatform.Authenticate('admin', 'admin')
    session = testPlatform.Sessions.add()
    ixNetwork = session.Ixnetwork

    ixNetwork.info('Preparing new blank config')
    ixNetwork.NewConfig()

    ixNetwork.info('Loading config file: bgp_ngpf_8.30.ixncfg')
    ixNetwork.LoadConfig(Files('bgp_ngpf_8.30.ixncfg', local_file=True))

    # Assign ports. Map physical ports to the configured vports.
    portMap = PortMapAssistant(ixNetwork)
    # For the portName, get it from the loaded configuration
    portMap.Map(IpAddress='192.168.70.128', CardId=1, PortId=1, Name=ixNetwork.Vport.find()[0].Name)
    portMap.Map(IpAddress='192.168.70.128', CardId=2, PortId=1, Name=ixNetwork.Vport.find()[1].Name)
    portMap.Connect(ForceOwnership=True)

    ixNetwork.info('Starting NGPF protocols')
    ixNetwork.StartAllProtocols(Arg1='sync')

    ixNetwork.info('Verify protocol sessions')
    protocolsSummary = StatViewAssistant(ixNetwork, 'Protocols Summary')
    protocolsSummary.CheckCondition('Sessions Not Started', StatViewAssistant.EQUAL, 0)
    protocolsSummary.CheckCondition('Sessions Down', StatViewAssistant.EQUAL, 0)

    # Get the Traffic Item name for getting Traffic Item statistics.
    trafficItem = ixNetwork.Traffic.TrafficItem.find()[0]

    trafficItem.Generate()
    ixNetwork.info('Applying traffic')
    ixNetwork.Traffic.Apply()
    ixNetwork.info('Starting traffic')
    ixNetwork.Traffic.StartStatelessTrafficBlocking()

    # StatViewAssistant could also filter by regex, LESS_THAN, GREATER_THAN, EQUAL. 
    # Examples:
    #    flowStatistics.AddRowFilter('Port Name', StatViewAssistant.REGEX, '^Port 1$')
    #    flowStatistics.AddRowFilter('Tx Frames', StatViewAssistant.LESS_THAN, 50000)

    trafficItemStatistics = StatViewAssistant(ixNetwork, 'Traffic Item Statistics')
    ixNetwork.info('{}\n'.format(trafficItemStatistics))
    
    # Get the statistic values
    txFrames = trafficItemStatistics.Rows[0]['Tx Frames']
    rxFrames = trafficItemStatistics.Rows[0]['Rx Frames']
    ixNetwork.info('\nTraffic Item Stats:\n\tTxFrames: {}  RxFrames: {}\n'.format(txFrames, rxFrames))

    ixNetwork.info('Stopping traffic')
    ixNetwork.Traffic.StopStatelessTrafficBlocking()

    if debugMode == False:
        # For Linux and Windows Connection Manager only
        session.remove()

except Exception as errMsg:
    print('\n%s' % traceback.format_exc())
    if debugMode and 'session' in locals():
        session.remove()





