"""
createTrafficItemAddPacketHeader.py

Description
   This sample script loads a saved config file and allows you to add traffic items.
   This script demonstrates how to create two different types of traffic items (RAW and IPv4)
   and creating packet headers for each traffic item.

   RAW traffic item means not using NGPF protocol emulations. Build every packet header in the
   traffic item starting at the Ethernet stack.
   Use vport as source/dst endpoints in the traffic item.

   IPv4traffic item  means to use configured NGPF protocols (Ethernet, VLAN, IPv4, other).
   And use the Topology Group as endpoints in the traffic item.

   - There are two reuseable functions in this script: createTrafficItem() and createPacketHeader()
  
   - You could create as many traffic items as you need and for each traffic item, you could create as little or as many
     packet headers you need.


  What this script does:

   - Load a saved config file.

   - Create 1 Raw Traffic Items. Each Traffic Item with custom packet header added.
        - Packet header: Ethernet, VLAN, IPv4, UDP, TCP and ICMP  

   - Start all protools
   - Verify all protocols
   - Run traffic
   - Get stats

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

import os, sys, traceback
from pprint import pprint

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

configFile = 'bgp_ngpf_8.30.ixncfg'

licenseServerIp = ['192.168.70.3']
# subscription, perpetual or mixed
licenseMode = 'subscription'
# tier1, tier2, tier3, tier3-10g
licenseTier = 'tier3'

# For linux and windowsConnectionMgr only. Set to True to leave the session alive for debugging.
debugMode = False

forceTakePortOwnership = True

# A list of chassis to use instead of the ones in the loaded config file
ixChassisIpList = ['192.168.70.128']
portList = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 2, 1]]

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
    testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, platform=osPlatform, log_file_name='restpy.log')

    # Console output verbosity: None|request|'request response'
    testPlatform.Trace = 'request_response'

    testPlatform.Authenticate(username, password)
    session = testPlatform.Sessions.add()

    ixNetwork = session.Ixnetwork
    ixNetwork.NewConfig()

    ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
    ixNetwork.Globals.Licensing.Mode = licenseMode
    ixNetwork.Globals.Licensing.Tier = licenseTier

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

    rawTrafficItemObj = createTrafficItem(trafficItemName = 'Raw Samples',
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

    vlanFieldObj = createPacketHeader(rawTrafficItemObj, packetHeaderToAdd='^VLAN', appendToStack='Ethernet II')
    vlanField = vlanFieldObj.find(DisplayName='VLAN Priority')
    vlanField.Auto = False
    vlanField.SingleValue = 3

    ipv4FieldObj = createPacketHeader(rawTrafficItemObj, packetHeaderToAdd='IPv4', appendToStack='^VLAN')
    ipv4SrcField = ipv4FieldObj.find(DisplayName='Source Address')
    ipv4SrcField.ValueType = 'increment'
    ipv4SrcField.StartValue = '1.1.1.1'
    ipv4SrcField.StepValue = '0.0.0.1'
    ipv4SrcField.CountValue = 1

    ipv4DstField = ipv4FieldObj.find(DisplayName='Destination Address')
    ipv4DstField.ValueType = 'increment'
    ipv4DstField.StartValue = '1.1.1.2'
    ipv4DstField.StepValue = '0.0.0.1'
    ipv4DstField.CountValue = 1

    # 000 Routine, 001 Priority, 010 Immediate, 011 Flash, 100 Flash Override,
    # 101 CRITIC/ECP, 110 Internetwork Control, 111 Network Control
    ipv4PrecedenceField = ipv4FieldObj.find(DisplayName='Precedence')
    ipv4PrecedenceField.ActiveFieldChoice = True
    ipv4PrecedenceField.FieldValue = '011 Flash'

    udpFieldObj = createPacketHeader(rawTrafficItemObj, packetHeaderToAdd='^UDP', appendToStack='IPv4')
    udpSrcField = udpFieldObj.find(DisplayName='UDP-Source-Port')
    udpSrcField.Auto = False
    udpSrcField.SingleValue = 1000

    udpDstField = udpFieldObj.find(DisplayName='UDP-Dest-Port')
    udpDstField.Auto = False
    udpDstField.SingleValue = 1001

    tcpFieldObj = createPacketHeader(rawTrafficItemObj, packetHeaderToAdd='^TCP', appendToStack='UDP')
    tcpSrcField = tcpFieldObj.find(DisplayName='TCP-Source-Port')
    tcpSrcField.Auto = False
    tcpSrcField.SingleValue = 1002

    tcpDstField = tcpFieldObj.find(DisplayName='TCP-Dest-Port')
    tcpDstField.Auto = False
    tcpDstField.SingleValue = 1003

    icmpFieldObj = createPacketHeader(rawTrafficItemObj, packetHeaderToAdd='ICMP Msg Type: 9', appendToStack='^TCP')

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

    if debugMode == False:
        # For Linux and WindowsConnectionMgr only
        session.remove()

except Exception as errMsg:
    ixNetwork.debug('\n%s' % traceback.format_exc())
    if debugMode == False and 'session' in locals():
        session.remove()


