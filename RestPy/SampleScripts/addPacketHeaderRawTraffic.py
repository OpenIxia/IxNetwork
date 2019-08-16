"""
addPacketHeaderRawTraffic.py:

   Tested with two back-2-back Ixia ports

   - Connect to the API server
   - Connect to chassis
   - Configure license server IP
   - Assign ports:
        - If variable forceTakePortOwnership is True, take over the ports if they're owned by another user.
        - If variable forceTakePortOwnership if False, abort test.
   - Configure a Raw Traffic Item
   - Configure Ethernet packet header
   - Add packet headers: MPLS and IPv4
   - Start traffic
   - Get Traffic Item
   - Get Flow Statistics stats

Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements
   - Minimum IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install ixnetwork_restpy

RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy

Usage:
   # Defaults to Windows
   - Enter: python <script>

   # Connect to Windows Connection Manager
   - Enter: python <script> connection_manager <apiServerIp> 443

   # Connect to Linux API server
   - Enter: python <script> linux <apiServerIp> 443
"""

import sys, os, re, traceback

# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant

# Set defaults
# Options: windows|connection_manager|linux
osPlatform = 'windows' 

apiServerIp = '192.168.70.3'

# For Linux API server only
username = 'admin'
password = 'admin'

# Allow passing in some params/values from the CLI to replace the defaults
if len(sys.argv) > 1:
    apiServerPort = sys.argv[1]

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

try:
    testPlatform = TestPlatform(apiServerIp, log_file_name='restpy.log')

    # Console output verbosity: None|request|'request response'
    testPlatform.Trace = 'request_response'

    testPlatform.Authenticate(username, password)
    session = testPlatform.Sessions.add()

    ixNetwork = session.Ixnetwork
    ixNetwork.NewConfig()

    ixNetwork.info('Configuring license server')
    ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
    ixNetwork.Globals.Licensing.Mode = licenseMode
    ixNetwork.Globals.Licensing.Tier = licenseTier

    # Create vport for RAW Traffic Item source/dest endpoints
    vport1 = ixNetwork.Vport.add(Name='Port1')
    vport2 = ixNetwork.Vport.add(Name='Port2')

    # Assign ports
    testPorts = []
    vportList = [vport.href for vport in ixNetwork.Vport.find()]
    for port in portList:
        testPorts.append(dict(Arg1=port[0], Arg2=port[1], Arg3=port[2]))

    ixNetwork.AssignPorts(testPorts, [], vportList, forceTakePortOwnership)

    ixNetwork.info('Create Traffic Item')
    trafficItem = ixNetwork.Traffic.TrafficItem.add(Name='RAW MPLS',
                                                    BiDirectional=False,
                                                    TrafficType='raw',
                                                    TrafficItemType='l2L3'
                                                )

    ixNetwork.info('Add flow group')
    trafficItem.EndpointSet.add(Sources=vport1.Protocols.find(), Destinations=vport2.Protocols.find())

    # Note: A Traffic Item could have multiple EndpointSets (Flow groups). 
    #       Therefore, ConfigElement is a list.
    ixNetwork.info('Configuring config elements')
    configElement = trafficItem.ConfigElement.find()[0]
    configElement.FrameRate.update(Type='percentLineRate', Rate=50)
    configElement.TransmissionControl.update(Type='fixedFrameCount', FrameCount=10000)

    #trafficItem.ConfigElement.find()[0].FrameRate.Rate = 28
    #trafficItem.ConfigElement.find()[0].FrameRate.Type = 'framesPerSecond'
    #trafficItem.ConfigElement.find()[0].TransmissionControl.FrameCount = 10000
    #trafficItem.ConfigElement.find()[0].TransmissionControl.Type = 'fixedFrameCount'

    configElement.FrameRateDistribution.PortDistribution = 'splitRateEvenly'
    configElement.FrameSize.FixedSize = 128
    trafficItem.Tracking.find()[0].TrackBy = ['flowGroup0']

    # Show a list of current configured packet headers in the first Traffic Item and first EndpointSet.
    ethernetStackObj = ixNetwork.Traffic.TrafficItem.find()[0].ConfigElement.find()[0].Stack.find(DisplayName='Ethernet II')

    # Uncomment this to show a list of all the available protocol templates (packet headers)
    #for protocolHeader in ixNetwork.Traffic.ProtocolTemplate():
    #    ixNetwork.info('\n', protocolHeader.DisplayName)

    # NOTE: If you are using virtual ports (IxVM), you must use the Destination MAC address of 
    #       the IxVM port from your virtual host (ESX-i host or KVM)
    ixNetwork.info('Configuring Ethernet packet header')
    ethernetDstField = ethernetStackObj.Field.find(DisplayName='Destination MAC Address')
    ethernetDstField.ValueType = 'increment'
    ethernetDstField.StartValue = "00:0c:29:76:b4:39"
    ethernetDstField.StepValue = "00:00:00:00:00:00"
    ethernetDstField.CountValue = 1

    ethernetSrcField = ethernetStackObj.Field.find(DisplayName='Source MAC Address')
    ethernetSrcField.ValueType = 'increment'
    ethernetSrcField.StartValue = "00:01:01:01:00:01"
    ethernetSrcField.StepValue = "00:00:00:00:00:01"
    ethernetSrcField.CountValue = 1

    # 1> Get the MPLS protocol template from the ProtocolTemplate list.
    mplsProtocolTemplate = ixNetwork.Traffic.ProtocolTemplate.find(DisplayName='^MPLS$')

    # 2> Append the MPLS protocol object created above after the Ethernet header stack.
    ethernetStackObj.Append(Arg2=mplsProtocolTemplate)
    
    # 3> Get the new MPLS packet header stack to use it for appending an IPv4 stack after it.
    # Look for the MPLS packet header object and stack ID.
    mplsStackObj = ixNetwork.Traffic.TrafficItem.find()[0].ConfigElement.find()[0].Stack.find(DisplayName='^MPLS$')

    # 4> In order to modify the MPLS fields, get the mpls field object
    mplsFieldObj = ixNetwork.Traffic.TrafficItem.find()[0].ConfigElement.find()[0].Stack.find(DisplayName='^MPLS$').Field.find()

    # 5> Configure the mpls packet header
    mplsFieldObj.ValueType = 'increment'
    mplsFieldObj.StartValue = "16"
    mplsFieldObj.StepValue = "1"
    mplsFieldObj.CountValue = 2

    # Add IPv4 packet header after the MPLS packet header stack
    # 1> Get the protocol template for IPv4
    ipv4ProtocolTemplate = ixNetwork.Traffic.ProtocolTemplate.find(DisplayName='IPv4')

    # 2> Append the IPv4 protocol header after the MPLS header.
    mplsStackObj.Append(Arg2=ipv4ProtocolTemplate)

    # 3> Get the new IPv4 packet header stack to use it for appending any protocol after IP layer such as 
    #    UDP/TCP.
    # Look for the IPv4 packet header object.
    ipv4StackObj = ixNetwork.Traffic.TrafficItem.find()[0].ConfigElement.find()[0].Stack.find(DisplayName='IPv4')

    # 4> Configure the mpls packet header
    ipv4SrcFieldObj = ipv4StackObj.Field.find(DisplayName='Source Address')
    ipv4SrcFieldObj.ValueType = 'increment'
    ipv4SrcFieldObj.StartValue = "1.1.1.1"
    ipv4SrcFieldObj.StepValue = "0.0.0.1"
    ipv4SrcFieldObj.CountValue = 1

    ipv4DstFieldObj = ipv4StackObj.Field.find(DisplayName='Destination Address')
    ipv4DstFieldObj.ValueType = 'increment'
    ipv4DstFieldObj.StartValue = "1.1.1.2"
    ipv4DstFieldObj.StepValue = "0.0.0.1"
    ipv4DstFieldObj.CountValue = 1

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

    trafficItemStatistics = StatViewAssistant(ixNetwork, 'Traffic Item Statistics')
    ixNetwork.info('{}\n'.format(trafficItemStatistics))
    
    # Get the statistic values
    txFrames = trafficItemStatistics.Rows[0]['Tx Frames']
    rxFrames = trafficItemStatistics.Rows[0]['Rx Frames']
    ixNetwork.info('Traffic Item Stats:\n\tTxFrames: {}  RxFrames: {}\n'.format(txFrames, rxFrames))

    if debugMode == False:
        # For Linux and connection_manager only
        session.remove()

except Exception as errMsg:
    print('\n%s' % traceback.format_exc())

    if debugMode == False and 'session' in locals():
        session.remove()
