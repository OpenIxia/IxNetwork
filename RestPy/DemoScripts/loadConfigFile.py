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
   - pip install ixnetwork_restpy (minimum version 1.0.51)

RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy

Usage:
   - Enter: python <script>
"""

import json, sys, os, traceback

# Import the RestPy module
from ixnetwork_restpy import SessionAssistant, Files

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = False

try:
    # LogLevel: none, info, warning, request, request_response, all
    session = SessionAssistant(IpAddress='192.168.70.3', RestPort=None, UserName='admin', Password='admin', 
                               SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel='info', LogFilename='restpy.log')

    ixNetwork = session.Ixnetwork

    ixNetwork.info('Loading config file: bgp_ngpf_8.30.ixncfg')
    ixNetwork.LoadConfig(Files('bgp_ngpf_8.30.ixncfg', local_file=True))

    # Assign ports. Map physical ports to the configured vports.
    portMap = session.PortMapAssistant()
    # For the portName, get it from the loaded configuration
    portMap.Map(IpAddress='192.168.70.128', CardId=1, PortId=1, Name=ixNetwork.Vport.find()[0].Name)
    portMap.Map(IpAddress='192.168.70.128', CardId=2, PortId=1, Name=ixNetwork.Vport.find()[1].Name)
    portMap.Connect(ForceOwnership=True)

    ixNetwork.info('Starting NGPF protocols')
    ixNetwork.StartAllProtocols(Arg1='sync')

    ixNetwork.info('Verify protocol sessions')
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)

    # Get the Traffic Item name for getting Traffic Item statistics.
    trafficItem = ixNetwork.Traffic.TrafficItem.find()[0]

    trafficItem.Generate()

    ixNetwork.info('Applying traffic')
    ixNetwork.Traffic.Apply()

    ixNetwork.info('Starting traffic')
    ixNetwork.Traffic.StartStatelessTrafficBlocking()

    trafficItemStatistics = session.StatViewAssistant('Traffic Item Statistics')
    ixNetwork.info('{}\n'.format(trafficItemStatistics))
    
    # Get the statistic values
    txFrames = trafficItemStatistics.Rows[0]['Tx Frames']
    rxFrames = trafficItemStatistics.Rows[0]['Rx Frames']
    ixNetwork.info('\nTraffic Item Stats:\n\tTxFrames: {}  RxFrames: {}\n'.format(txFrames, rxFrames))

    ixNetwork.info('Stopping traffic')
    ixNetwork.Traffic.StopStatelessTrafficBlocking()

    if debugMode == False:
        # For Linux and Windows Connection Manager only
        session.Session.remove()

except Exception as errMsg:
    print('\n%s' % traceback.format_exc())
    if debugMode and 'session' in locals():
        session.Session.remove()





