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
   - IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install -U --no-cache-dir ixnetwork_restpy
   - https://github.com/OpenIxia/IxNetwork/RestApi/Python/Restpy/Modules:
         - Statistics.py and PortMgmt.py 

Script development API doc:
   - The doc is located in your Python installation /site-packages/ixnetwork_restpy/index.html
   - On a web browser, enter: file:///<full_path_to_ixnetwork_restpy>/index.html
"""

from __future__ import absolute_import, print_function
import sys, re

# The main client module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform

# Modules containing helper functions
sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules'))))
from StatisticsMgmt import Statistics
from PortMgmt import Ports

if len(sys.argv) > 1:
    # Command line input: windows or linux
    osPlatform = sys.argv[1]
else:
    # Defaulting to windows
    osPlatform = 'windows'

# Are you using IxNetwork Connection Manager in a Windows server 2012/2016?
isWindowsConnectionMgr = False

# Change API server values to use your setup
if osPlatform == 'windows':
    apiServerIp = '192.168.70.3'
    apiServerPort = 11009

# Change API server values to use your setup
if osPlatform == 'linux':
    apiServerIp = '192.168.70.121'
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
ixChassisIpList = ['192.168.70.120']
portList = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 1, 2]]

try:
    testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, platform=osPlatform)

    # Console output verbosity: None|request|request_response
    testPlatform.Trace = 'request_response'

    if osPlatform == 'linux':
        testPlatform.Authenticate(username, password)

    if isWindowsConnectionMgr or osPlatform == 'linux':
        session = testPlatform.Sessions.add()

    if osPlatform == 'windows':
        # Windows support only one session. Id is always equal 1.
        session = testPlatform.Sessions.find(Id=1)

    # ixNetwork is the root object to the IxNetwork API hierarchical tree.
    ixNetwork = session.Ixnetwork

    # Instantiate the helper class objects
    statObj = Statistics(ixNetwork)
    portObj = Ports(ixNetwork)

    '''
    if osPlatform == 'windows':
        ixNetwork.NewConfig()    

    print('\nConfiguring license server')
    '''
    if forceTakePortOwnership == True:
        # To configure the license server IP, must release the ports first.
        portObj.releasePorts(portList)
        ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
        ixNetwork.Globals.Licensing.Mode = licenseMode
    '''

    ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
    ixNetwork.Globals.Licensing.Mode = licenseMode
    portObj.assignPorts(portList, forceTakePortOwnership)
    '''

    # Get vport for RAW Traffic Item source/dest endpoints
    vportList = [vport.href+'/protocols' for vport in ixNetwork.Vport.find()]
    vport1 = vportList[0]
    vport2 = vportList[1]

    print('\nCreate Traffic Item')
    trafficItem = ixNetwork.Traffic.TrafficItem.add(Name='RAW MPLS',
                                                    BiDirectional=False,
                                                    TrafficType='raw'
                                                )
    
    print('\tAdd flow group')
    trafficItem.EndpointSet.add(Sources=[vport1], Destinations=[vport2])

    # Note: A Traffic Item could have multiple EndpointSets (Flow groups). 
    #       Therefore, ConfigElement is a list.
    print('\tConfiguring config elements')
    trafficItem.ConfigElement.find()[0].FrameRate.Rate = 28
    trafficItem.ConfigElement.find()[0].FrameRate.Type = 'framesPerSecond'
    trafficItem.ConfigElement.find()[0].TransmissionControl.FrameCount = 10000
    trafficItem.ConfigElement.find()[0].TransmissionControl.Type = 'fixedFrameCount'
    trafficItem.ConfigElement.find()[0].FrameRateDistribution.PortDistribution = 'splitRateEvenly'
    trafficItem.ConfigElement.find()[0].FrameSize.FixedSize = 128
    trafficItem.Tracking.find()[0].TrackBy = ['flowGroup0']

    # Show a list of current configured packet headers in the first Traffic Item and first EndpointSet.
    packetHeaderStacks = ixNetwork.Traffic.TrafficItem.find()[0].ConfigElement.find()[0].Stack.find()

    # Uncomment this to show a list of all the available protocol templates (packet headers)
    #for protocolHeader in ixNetwork.Traffic.ProtocolTemplate():
    #    print('\n', protocolHeader.DisplayName)

    # Look for the Ethernet packet header stack ID.
    # Note: The packetHeader stack number needs to be one based. Hence index+1.
    for index,stack in enumerate(packetHeaderStacks):
        if stack.DisplayName == 'Ethernet II':
            ethernetStackObj = stack
            break

    print('\nConfiguring Ethernet packet header')
    for field in ethernetStackObj.Field.find():
        if field.DisplayName == 'Destination MAC Address':
            field.ValueType = 'increment'
            field.StartValue = "00:0c:29:84:37:16"
            field.StepValue = "00:00:00:00:00:00"
            field.CountValue = 1

        if field.DisplayName == 'Source MAC Address':
            field.ValueType = 'increment'
            field.StartValue = "00:01:01:01:00:01"
            field.StepValue = "00:00:00:00:00:01"
            field.CountValue = 1

    print('\n--- Configuring MPLS 1 ----\n')
    # Add MPLS packet header after the Ethernet packet header stack
    # 1> Get the protocol index that you want to append or insert.
    for index,protocolHeader in enumerate(ixNetwork.Traffic.ProtocolTemplate.find()):
        if bool(re.match('mpls', protocolHeader.DisplayName, re.I)):
            mplsProtocolTemplateIndex = index
            break

    print('\n--- Configuring MPLS 2 ----\n')
    # 2> Yank out the MPLS protocol template from the ProtocolTemplate list.
    mplsProtocolTemplate = ixNetwork.Traffic.ProtocolTemplate.find()[mplsProtocolTemplateIndex]

    print('\n--- Configuring MPLS 3 ----\n')
    print('\n--- ethStackObj:', ethernetStackObj)
    print('\n---- dir:', dir(ethernetStackObj))
    print('\n---- mplsProtocolTemplate:', mplsProtocolTemplate)
    # 3> Append the MPLS protocol header after the Ethernet header.
    ethernetStackObj.Append(Arg2=mplsProtocolTemplate)
    
    print('\n--- Configuring MPLS 4 ----\n')
    # 4> Get the new MPLS packet header stack
    # Look for the MPLS packet header object and stack ID.
    # Note: The packetHeader stack number needs to be one based. Hence index+1.
    for index,stack in enumerate(ixNetwork.Traffic.TrafficItem.find()[0].ConfigElement.find()[0].Stack.find()):
        if stack.DisplayName == 'MPLS':
            mplsStackObj = stack
            break

    print('\n--- Configuring MPLS 5 ----\n')
    # 5> Configure the mpls packet header
    for field in mplsStackObj.Field.find():
        if field.DisplayName == 'Label Value':
            field.ValueType = 'increment'
            field.StartValue = "16"
            field.StepValue = "1"
            field.CountValue = 2

    print('\n--- Configuring MPLS 6 ----\n')
    # Add IPv4 packet header after the MPLS packet header stack
    # 1> Get the protocol index that you want to append or insert.
    for index,protocolHeader in enumerate(ixNetwork.Traffic.ProtocolTemplate.find()):
        if bool(re.match('ipv4', protocolHeader.DisplayName, re.I)):
            ipv4ProtocolTemplateIndex = index
            break

    print('\n--- Configuring MPLS 7 ----\n')
    # 2> Yank out the IPv4 protocol template from the ProtocolTemplate list.
    ipv4ProtocolTemplate = ixNetwork.Traffic.ProtocolTemplate.find()[ipv4ProtocolTemplateIndex]

    print('\n--- Configuring MPLS 8 ----\n')
    # 3> Append the protocol header after the Ethernet header.
    mplsStackObj.Append(Arg2=ipv4ProtocolTemplate)
    
    print('\n--- Configuring MPLS 9 ----\n')
    # 4> Get the new mpls packet header stack
    # Look for the MPLS packet header object and stack ID.
    # Note: The packetHeader stack number needs to be one based. Hence index+1.
    for index, stack in enumerate(ixNetwork.Traffic.TrafficItem.find()[0].ConfigElement.find()[0].Stack.find()):
        if bool(re.match('IPv4', stack.DisplayName, re.I)):
            ipv4StackObj = stack
            break

    print('\n--- Configuring MPLS 10 ----\n')
    # 5> Configure the mpls packet header
    for field in ipv4StackObj.Field.find():
        if field.DisplayName == 'Source Address':
            field.ValueType = 'increment'
            field.StartValue = "1.1.1.1"
            field.StepValue = "0.0.0.1"
            field.CountValue = 1

        if field.DisplayName == 'Destination Address':
            field.ValueType = 'increment'
            field.StartValue = "1.1.1.2"
            field.StepValue = "0.0.0.1"
            field.CountValue = 1

    trafficItem.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()

    # Get the Traffic Item name for getting Traffic Item statistics.
    trafficItemName = trafficItem.Name

    # Get and show the Traffic Item column caption names and stat values
    columnCaptions= statObj.getStatViewResults(statViewName='Traffic Item Statistics', getColumnCaptions=True)
    trafficItemStats = statObj.getStatViewResults(statViewName='Traffic Item Statistics', rowValuesLabel=trafficItemName)
    txFramesIndex = columnCaptions.index('Tx Frames')
    rxFramesIndex = columnCaptions.index('Rx Frames')
    print('\nTraffic Item Stats:\n\tTxFrames: {0}  RxFrames: {1}'.format(trafficItemStats[txFramesIndex],
                                                                         trafficItemStats[rxFramesIndex]))
    
    # Get and show the Flow Statistics column caption names and stat values
    columnCaptions =   statObj.getStatViewResults(statViewName='Flow Statistics', getColumnCaptions=True)
    flowStats = statObj.getFlowStatistics()
    print('\n', columnCaptions)
    for statValues in flowStats:
        print('\n{0}'.format(statValues))
    print()

    if deleteSessionWhenDone:
        # For Linux and WindowsConnectionMgr only
        if osPlatform == 'linux' or isWindowsConnectionMgr:
            session.remove()

except Exception as errMsg:
    print('\nrestPy.Exception:', errMsg)
    if deleteSessionWhenDone and 'session' in locals():
        if osPlatform == 'linux' or isWindowsConnectionMgr:
            session.remove()
