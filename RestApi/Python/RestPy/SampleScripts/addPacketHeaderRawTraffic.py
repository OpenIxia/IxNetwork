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
import sys, os, re

# The main client module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform

# Modules containing helper functions from Github
# These  modules are one level above.
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

    if osPlatform == 'windows':
        ixNetwork.NewConfig()    

    print('\nConfiguring license server')
    ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
    ixNetwork.Globals.Licensing.Mode = licenseMode

    # Create vport for RAW Traffic Item source/dest endpoints
    vport1 = ixNetwork.Vport.add(Name='Port1')
    vport2 = ixNetwork.Vport.add(Name='Port2')

    # getVportList=True because you already created vports from above.
    # If you did not create vports, then assignPorts will create them and name them with default names.
    portObj.assignPorts(portList, forceTakePortOwnership, getVportList=True)

    print('\nCreate Traffic Item')
    trafficItem = ixNetwork.Traffic.TrafficItem.add(Name='RAW MPLS',
                                                    BiDirectional=False,
                                                    TrafficType='raw'
                                                )
    
    print('\tAdd flow group')
    trafficItem.EndpointSet.add(Sources=vport1.Protocols, Destinations=vport2.Protocols)

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
    ethernetStackObj = ixNetwork.Traffic.TrafficItem.find()[0].ConfigElement.find()[0].Stack.find(DisplayName='Ethernet II')

    # Uncomment this to show a list of all the available protocol templates (packet headers)
    #for protocolHeader in ixNetwork.Traffic.ProtocolTemplate():
    #    print('\n', protocolHeader.DisplayName)

    # NOTE: If you are using virtual ports (IxVM), you must use the Destination MAC address of 
    #       the IxVM port from your virtual host (ESX-i host or KVM)
    print('\nConfiguring Ethernet packet header')
    ethernetDstField = ethernetStackObj.Field.find(DisplayName='Destination MAC Address')
    ethernetDstField.ValueType = 'increment'
    ethernetDstField.StartValue = "00:0c:29:ce:41:32"
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

    # Get the Traffic Item name for getting Traffic Item statistics.
    trafficItemName = trafficItem.Name

    # Get the Traffic Item column caption names and stat values
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
