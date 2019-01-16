"""
createTrafficItemAddPacketHeader.py

Description
   This sample script loads a saved config file and allows you to add traffic items.
   This script demonstrates how to create two different types of traffic items (RAW and IPv4)
   and creating packet headers for each traffic item.

   RAW traffic item means not using NGPF protocol emulations. Build every packet header in the traffic item starting with Ethernet.
   Use vport as source/dst endpoints in the traffic item.

   IPv4traffic item  means to use configured NGPF protocols (Ethernet, VLAN, IPv4, other).
   And use the Topology Group as endpoints in the traffic item.

   - There are two reuseable functions in this script: createTrafficItem() and createPacketHeader()
  
   - You could create as many traffic items as you need and for each traffic item, you could create as little or as many
     packet headers you need.


  What this script does:

   - Load a saved config file.

   - Create 2 Traffic Items. Each Traffic Item with custom packet header added.

        Traffic Item #1:
           - Packet header: GRE

        Traffic Item #2 (RAW traffic item):
           - Packet header: Ethernet, VLAN, IPv4, UDP, GTPu, IPv4, TCP and ICMP  

   - Start all protools
   - Verify all protocols
   - Run traffic
   - Get stats

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
"""

import os, sys, traceback
from pprint import pprint

# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.files import Files
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant

# Defaulting to windows
osPlatform = 'windows'

# Change values to use your setup
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

configFile = 'bgp_ngpf_8.30.ixncfg'

licenseServerIp = ['192.168.70.3']
# subscription, perpetual or mixed
licenseMode = 'subscription'

# For linux and windowsConnectionMgr only. Set to False to leave the session alive for debugging.
deleteSessionWhenDone = True

forceTakePortOwnership = True

# A list of chassis to use instead of the ones in the loaded config file
ixChassisIpList = ['192.168.70.128']
portList = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 1, 2]]

try:

    def createTrafficItem(**kwargs):
        trafficItemObj = ixNetwork.Traffic.TrafficItem.add(Name=kwargs['trafficItemName'], BiDirectional=kwargs['biDirectional'],
                                                           TrafficType=kwargs['trafficType'])

        ixNetwork.info('Add endpoints')
        trafficItemObj.EndpointSet.add(Sources=kwargs['srcEndpoint'], Destinations=kwargs['dstEndpoint'])           

        configElement = trafficItemObj.ConfigElement.find()[0]
        configElement.FrameRate.Rate = kwargs['frameRate']
        configElement.FrameRate.Type = kwargs['frameRateType']
        configElement.TransmissionControl.FrameCount = kwargs['frameCount']
        configElement.TransmissionControl.Type = kwargs['transmissionControlType']
        configElement.FrameSize.FixedSize = kwargs['frameSize']
        trafficItemObj.Tracking.find()[0].TrackBy = kwargs['tracking']

        return trafficItemObj

    def createPacketHeader(trafficItemObj, packetHeaderToAdd=None, appendToStack=None): 
        configElement = trafficItemObj.ConfigElement.find()[0]

        # Do the followings to add packet headers on the new traffic item

        # Uncomment this to show a list of all the available protocol templates to create (packet headers)
        #for protocolHeader in ixNetwork.Traffic.ProtocolTemplate.find():
        #    ixNetwork.info('Protocol header: {}'.format(protocolHeader))

        # 1> Get the <new packet header> protocol template from the ProtocolTemplate list.
        packetHeaderProtocolTemplate = ixNetwork.Traffic.ProtocolTemplate.find(DisplayName=packetHeaderToAdd)
        ixNetwork.info('protocolTemplate: {}'.format(packetHeaderProtocolTemplate))

        # 2> Append the <new packet header> object after the specified packet header stack.
        appendToStackObj = configElement.Stack.find(DisplayName=appendToStack)
        ixNetwork.info('appendToStackObj: {}'.format(appendToStackObj))
        appendToStackObj.Append(Arg2=packetHeaderProtocolTemplate)

        # 3> Get the new packet header stack to use it for appending an IPv4 stack after it.
        # Look for the packet header object and stack ID.
        packetHeaderStackObj = configElement.Stack.find(DisplayName=packetHeaderToAdd)
        
        # 4> In order to modify the fields, get the field object
        packetHeaderFieldObj = packetHeaderStackObj.Field.find()
        ixNetwork.info('packetHeaderFieldObj: {}'.format(packetHeaderFieldObj))
        
        # 5> Save the above configuration to the base config file.
        #ixNetwork.SaveConfig(Files('baseConfig.ixncfg', local_file=True))

        return packetHeaderFieldObj


    # Connect
    testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, platform=platform, log_file_name='restpy.log')

    # Console output verbosity: None|request|'request response'
    testPlatform.Trace = 'request_response'    

    if osPlatform == 'linux':
        testPlatform.Authenticate(username, password)

    session = testPlatform.Sessions.add()
    ixNetwork = session.Ixnetwork

    if osPlatform == 'windows':
        ixNetwork.NewConfig()

    ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
    ixNetwork.Globals.Licensing.Mode = licenseMode

    ixNetwork.LoadConfig(Files(configFile, local_file=True))

    # Optional: Assign ports.
    testPorts = []
    vportList = [vport.href for vport in ixNetwork.Vport.find()]
    for port in portList:
        testPorts.append(dict(Arg1=port[0], Arg2=port[1], Arg3=port[2]))

    ixNetwork.AssignPorts(testPorts, [], vportList, forceTakePortOwnership)

    ixNetwork.StartAllProtocols(Arg1='sync')
 
    ixNetwork.info('Verify protocol sessions\n')
    protocolsSummary = StatViewAssistant(ixNetwork, 'Protocols Summary')
    protocolsSummary.CheckCondition('Sessions Not Started', StatViewAssistant.EQUAL, 0)
    protocolsSummary.CheckCondition('Sessions Down', StatViewAssistant.EQUAL, 0)
    ixNetwork.info(protocolsSummary)

    greTrafficItemObj = createTrafficItem(trafficItemName = 'GRE',
                                          biDirectional = False,
                                          trafficType = 'ipv4',
                                          frameRate = 28,
                                          frameSize = 64,
                                          frameRateType = 'framesPerSecond',
                                          frameCount = 10000,
                                          transmissionControlType = 'fixedFrameCount',
                                          tracking = ['flowGroup0'],
                                          srcEndpoint = ixNetwork.Topology.find(Name='Topo1'),
                                          dstEndpoint = ixNetwork.Topology.find(Name='Topo2')
                                      )

    # Enable/disable the traffic item
    greTrafficItemObj.Enabled = False    

    greFieldObj = createPacketHeader(greTrafficItemObj, packetHeaderToAdd='^GRE', appendToStack='IPv4')
    greFieldObj.singleValue = 3


    # Create GTPu traffic item
    gtpuTrafficItemObj = createTrafficItem(trafficItemName = 'GTPu',
                                          biDirectional = False,
                                          trafficType = 'raw',
                                          frameRate = 28,
                                          frameSize = 64,
                                          frameRateType = 'framesPerSecond',
                                          frameCount = 10000,
                                          transmissionControlType = 'fixedFrameCount',
                                          tracking = ['flowGroup0'],
                                          srcEndpoint = ixNetwork.Vport.find(Name='Port_1').Protocols.find(),
                                          dstEndpoint = ixNetwork.Vport.find(Name='Port_2').Protocols.find()
                                      )

    # Ethernet header doesn't need to be created.  It is there by default. Just do a find for the Ethernet stack object.
    ethernetStackObj = ixNetwork.Traffic.TrafficItem.find()[-1].ConfigElement.find()[0].Stack.find(DisplayName='Ethernet II')

    # NOTE: If you are using virtual ports (IxVM), you must use the Destination MAC address of 
    #       the IxVM port from your virtual host (ESX-i host or KVM)
    ixNetwork.info('Configuring Ethernet packet header')
    ethernetDstField = ethernetStackObj.Field.find(DisplayName='Destination MAC Address')
    ethernetDstField.ValueType = 'increment'
    ethernetDstField.StartValue = "00:0c:29:22:8f:2f"
    ethernetDstField.StepValue = "00:00:00:00:00:00"
    ethernetDstField.CountValue = 1

    ethernetSrcField = ethernetStackObj.Field.find(DisplayName='Source MAC Address')
    ethernetSrcField.ValueType = 'increment'
    ethernetSrcField.StartValue = "00:01:01:01:00:01"
    ethernetSrcField.StepValue = "00:00:00:00:00:01"
    ethernetSrcField.CountValue = 1

    vlanFieldObj = createPacketHeader(gtpuTrafficItemObj, packetHeaderToAdd='^VLAN', appendToStack='Ethernet II')
    vlanFieldObj.find(DisplayName='VLAN Priority').Auto = False
    vlanFieldObj.find(DisplayName='VLAN Priority').SingleValue = 3
    vlanFieldObj.find(DisplayName='VLAN-ID').Auto = False
    vlanFieldObj.find(DisplayName='VLAN-ID').SingleValue = 1008

    outerIpv4FieldObj = createPacketHeader(gtpuTrafficItemObj, packetHeaderToAdd='IPv4', appendToStack='^VLAN')
    outerIpv4FieldObj.find(DisplayName='Source Address').ValueType = 'increment'
    outerIpv4FieldObj.find(DisplayName='Source Address').StartValue = '1.1.1.1'
    outerIpv4FieldObj.find(DisplayName='Source Address').StepValue = '0.0.0.1'
    outerIpv4FieldObj.find(DisplayName='Source Address').CountValue = 1

    outerIpv4FieldObj.find(DisplayName='Destination Address').ValueType = 'increment'
    outerIpv4FieldObj.find(DisplayName='Destination Address').StartValue = '1.1.1.2'
    outerIpv4FieldObj.find(DisplayName='Destination Address').StepValue = '0.0.0.1'
    outerIpv4FieldObj.find(DisplayName='Destination Address').CountValue = 1

    udpFieldObj = createPacketHeader(gtpuTrafficItemObj, packetHeaderToAdd='^UDP', appendToStack='IPv4')
    udpFieldObj.find(DisplayName='UDP-Source-Port').Auto = False
    udpFieldObj.find(DisplayName='UDP-Source-Port').SingleValue = 1000
    udpFieldObj.find(DisplayName='UDP-Dest-Port').Auto = False
    udpFieldObj.find(DisplayName='UDP-Dest-Port').SingleValue = 1001

    gtpuFieldObj = createPacketHeader(gtpuTrafficItemObj, packetHeaderToAdd='GTPu', appendToStack='UDP')
    gtpuFieldObj.find(DisplayName='').Auto = False
    gtpuFieldObj.find(DisplayName='').SingleValue = 1002
    gtpuFieldObj.find(DisplayName='').Auto = False
    gtpuFieldObj.find(DisplayName='').SingleValue = 1003

    innerIpv4FieldObj = createPacketHeader(gtpuTrafficItemObj, packetHeaderToAdd='IPv4', appendToStack='^GTPu')
    innerIpv4FieldObj.find(DisplayName='Source Address').ValueType = 'increment'
    innerIpv4FieldObj.find(DisplayName='Source Address').StartValue = '10.1.1.1'
    innerIpv4FieldObj.find(DisplayName='Source Address').StepValue = '0.0.0.1'
    innerIpv4FieldObj.find(DisplayName='Source Address').CountValue = 1

    innerIpv4FieldObj.find(DisplayName='Destination Address').ValueType = 'increment'
    innerIpv4FieldObj.find(DisplayName='Destination Address').StartValue = '10.1.1.2'
    innerIpv4FieldObj.find(DisplayName='Destination Address').StepValue = '0.0.0.1'
    innerIpv4FieldObj.find(DisplayName='Destination Address').CountValue = 1

    tcpFieldObj = createPacketHeader(gtpuTrafficItemObj, packetHeaderToAdd='^TCP', appendToStack='IPv4')
    tcpFieldObj.find(DisplayName='TCP-Source-Port').Auto = False
    tcpFieldObj.find(DisplayName='TCP-Source-Port').SingleValue = 1002
    tcpFieldObj.find(DisplayName='TCP-Dest-Port').Auto = False
    tcpFieldObj.find(DisplayName='TCP-Dest-Port').SingleValue = 1003

    icmpFieldObj = createPacketHeader(gtpuTrafficItemObj, packetHeaderToAdd='ICMP Msg Type: 9', appendToStack='^TCP')
    #icmpFieldObj.find(DisplayName='ICMP-Source-Port').Auto = False
    #icmpFieldObj.find(DisplayName='ICMP-Source-Port').SingleValue = 1002
    #icmpFieldObj.find(DisplayName='ICMP-Dest-Port').Auto = False
    #icmpFieldObj.find(DisplayName='ICMP-Dest-Port').SingleValue = 1003

    for trafficItem in ixNetwork.Traffic.TrafficItem.find():
        trafficItem.Generate()

    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()
    
    # StatViewAssistant could also filter by REGEX, LESS_THAN, GREATER_THAN, EQUAL. 
    # Examples:
    #    flowStatistics.AddRowFilter('Port Name', StatViewAssistant.REGEX, '^Port 1$')
    #    flowStatistics.AddRowFilter('Tx Frames', StatViewAssistant.LESS_THAN, 50000)

    flowStatistics = StatViewAssistant(ixNetwork, 'Flow Statistics')

    #flowStatistics.AddRowFilter('Loss %', StatViewAssistant.GREATER_THAN, 0)

    for rowNumber,flowStat in enumerate(flowStatistics.Rows):
        ixNetwork.info('\n\nSTATS: {}\n\n'.format(flowStat))
        ixNetwork.info('\nRow:{}  TxPort:{}  RxPort:{}  TxFrames:{}  RxFrames:{}\n'.format(
            rowNumber, flowStat['Tx Port'], flowStat['Rx Port'],
            flowStat['Tx Frames'], flowStat['Rx Frames']))


    '''
     Field[13]: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/configElement/1/stack/4/field/14
        __id__: a3a92ed3-fb09-47ce-aaf9-f07529127752
        ActiveFieldChoice: True
        Auto: False
        CountValue: 1
        DefaultValue: 0
        DisplayName: No Sequence Number
        EnumValues: []
        FieldChoice: True
        FieldTypeId: gre.header.sequenceHolder.noSequenceNum
        FieldValue: 0
        FixedBits: 0
        FullMesh: False
        Length: 32
        Level: False
        MaxValue: 0
        MinValue: 0
        Name: no_sequence_num
        Offset: 32
        OffsetFromRoot: 336
        OnTheFlyMask: 0
        Optional: False
        OptionalEnabled: True
        RandomMask: 0
        RateVaried: False
        ReadOnly: False
        RequiresUdf: False
        Seed: 1
        SingleValue: 0
        StartValue: 0
        StepValue: 0
        SupportsNonRepeatableRandom: True
        SupportsOnTheFlyMask: True
        TrackingEnabled: False
        ValueFormat: hex
        ValueList: ['0']
        ValueType: singleValue
    '''

    if deleteSessionWhenDone:
        # For Linux and WindowsConnectionMgr only
        if osPlatform in ['linux', 'windowsConnectionMgr']:
            session.remove()

except Exception as errMsg:
    ixNetwork.debug('\n%s' % traceback.format_exc())
    if deleteSessionWhenDone and 'session' in locals():
        if osPlatform in ['linux', 'windowsConnectionMgr']:
            session.remove()


