"""
loadConfigFile.py:

   Tested with two back-2-back Ixia ports

   - Connect to the API server
   - Load a saved config file
   - Optional: Assign ports or use the ports that are in the saved config file.
   - Start all protocols
   - Verify all protocols
   - Start traffic 
   - Get Traffic Item
   - Get Flow Statistics stats

Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements
   - Minimum IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install ixnetwork_restpy (minimum version 1.0.51)

RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy/#/

Usage:
   - Enter: python <script>
"""

import json, sys, os, traceback

# Import the RestPy module
from ixnetwork_restpy import SessionAssistant, Files
#from ixnetwork_restpy import *

apiServerIp = '192.168.70.3'

# A list of chassis to use
ixChassisIpList = ['192.168.70.128']
portList = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 2, 1]]

# For Linux API server only
username = 'admin'
password = 'admin'

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = False

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True

configFile = 'bgp_ngpf_8.30.ixncfg'

try:
    # LogLevel: none, info, warning, request, request_response, all
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=None, UserName='admin', Password='admin', 
                               SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel='all', LogFilename='restpy.log')

    ixNetwork = session.Ixnetwork

    ixNetwork.info('Loading config file: {0}'.format(configFile))
    ixNetwork.LoadConfig(Files(configFile, local_file=True))
   
    # Assign ports. Map physical ports to the configured vports.
    portMap = session.PortMapAssistant()
    vport = dict()
    for index,port in enumerate(portList):
        # For the port name, get the loaded configuration's port name
        portName = ixNetwork.Vport.find()[index].Name
        portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=portName)
        
    portMap.Connect(forceTakePortOwnership)

    ixNetwork.StartAllProtocols(Arg1='sync')

    ixNetwork.info('Verify protocol sessions\n')
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
    ixNetwork.info(protocolSummary)

    # Get the Traffic Item name for getting Traffic Item statistics.
    trafficItem = ixNetwork.Traffic.TrafficItem.find()[0]

    trafficItem.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.StartStatelessTrafficBlocking()

    trafficItemStatistics = session.StatViewAssistant('Traffic Item Statistics')

    # StatViewAssistant could also filter by REGEX, LESS_THAN, GREATER_THAN, EQUAL. 
    # Examples:
    #    trafficItemStatistics.AddRowFilter('Port Name', trafficItemStatistics.REGEX, '^Port 1$')
    #    trafficItemStatistics.AddRowFilter('Tx Frames', trafficItemStatistics.GREATER_THAN, "5000")

    ixNetwork.info('{}\n'.format(trafficItemStatistics))

    # Get the statistic values
    txFrames = trafficItemStatistics.Rows['Tx Frames']
    rxFrames = trafficItemStatistics.Rows['Rx Frames']
    ixNetwork.info('\nTraffic Item Stats:\n\tTxFrames: {}  RxFrames: {}\n'.format(txFrames, rxFrames))

    ixNetwork.Traffic.StopStatelessTrafficBlocking()

    if debugMode == False:
        # For Linux and Windows Connection Manager only
        if session.TestPlatform.Platform != 'windows':
            session.Session.remove()

except Exception as errMsg:
    print('\n%s' % traceback.format_exc())
    if debugMode == False and 'session' in locals():
        if session.TestPlatform.Platform != 'windows':
            session.Session.remove()





