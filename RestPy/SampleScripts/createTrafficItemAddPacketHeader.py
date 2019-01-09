"""
createTrafficItemAddPacketHeader.py

Description
   - Load a saved config file.
   - Create 3 Traffic Items. Each Traffic Item with custom packet header added.
        - Traffic Item: GRE
        - Traffic Item: UDP
        - Traffic Item: TCP

Requirements
   - IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install -U --no-cache-dir ixnetwork_restpy
   - Helper functions: https://github.com/OpenIxia/IxNetwork/RestApi/Python/Restpy/Modules:
                       - Statistics.py and PortMgmt.py

Script development API doc:
   - The doc is located in your Python installation site-packages/ixnetwork_restpy/docs/index.html
   - On a web browser:
         - If installed in Windows: enter: file://c:/<path_to_ixnetwork_restpy>/docs/index.html
         - If installed in Linux: enter: file:///<path_to_ixnetwork_restpy>/docs/index.html
"""

import os, sys
from pprint import pprint

# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.files import Files

# Import modules containing helper functions
sys.path.append(os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules')))
from StatisticsMgmt import Statistics
from PortMgmt import Ports

# Change values to use your setup
platform = 'windows'
apiServerIp = '192.168.70.3'
apiServerPort = 11009
configFile = 'bgp_ngpf_8.30.ixncfg'

licenseServerIp = ['192.168.70.3']
# subscription, perpetual or mixed
licenseMode = 'subscription'

forceTakePortOwnership = True

# A list of chassis to use
ixChassisIpList = ['192.168.70.128']
portList = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 1, 2]]

try:

    def createNewTrafficItem(trafficItemName, packetHeaderToAdd=None, appendToStack=None):
        trafficItemObj = ixNetwork.Traffic.TrafficItem.add(Name=trafficItemName, BiDirectional=False, TrafficType='ipv4')

        print('\tAdd endpoint flow group')
        # Get the topology objects
        topology1 = ixNetwork.Topology.find(Name='Topo1')
        topology2 = ixNetwork.Topology.find(Name='Topo2')

        # Create a flow group by adding src/dst endpoints
        trafficItemObj.EndpointSet.add(Sources=topology1, Destinations=topology2)           

        configElement = trafficItemObj.ConfigElement.find()[0]
        configElement.FrameRate.Rate = 28
        configElement.FrameRate.Type = 'framesPerSecond'
        configElement.TransmissionControl.FrameCount = 10000
        configElement.TransmissionControl.Type = 'fixedFrameCount'
        configElement.FrameSize.FixedSize = 128
        trafficItemObj.Tracking.find()[0].TrackBy = ['flowGroup0']

        # Do the followings to add packet headers on the new traffic item

        # Show a list of all the available protocol templates (packet headers)
        for protocolHeader in ixNetwork.Traffic.ProtocolTemplate.find():
            print('\n', protocolHeader)

        # 1> Get the <new packet header> protocol template from the ProtocolTemplate list.
        packetHeaderProtocolTemplate = ixNetwork.Traffic.ProtocolTemplate.find(DisplayName=packetHeaderToAdd)
        print('\ngreProtocolTemplate:', packetHeaderProtocolTemplate)

        # 2> Append the <new packet header> object after the specified packet header stack.
        appendToStackObj = trafficItemObj.ConfigElement.find()[0].Stack.find(DisplayName=appendToStack)
        print('\nappendToStackObj:', appendToStackObj)
        appendToStackObj.Append(Arg2=packetHeaderProtocolTemplate)

        # 3> Get the new packet header stack to use it for appending an IPv4 stack after it.
        # Look for the packet header object and stack ID.
        packetHeaderStackObj = configElement.Stack.find(DisplayName=packetHeaderToAdd)
        
        # 4> In order to modify the fields, get the field object
        packetHeaderFieldObj = packetHeaderStackObj.Field.find()
        print('\ngreFieldObj:', packetHeaderFieldObj)
        
        # 5> Save the above configuration to the base config file.
        #ixNetwork.SaveConfig(Files('baseConfig.ixncfg', local_file=True))

        return trafficItemObj, packetHeaderFieldObj


    # Connect
    testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, platform=platform)
    testPlatform.Trace = 'request_response'    
    session = testPlatform.Sessions.find(Id=1)
    ixNetwork = session.Ixnetwork

    # Instantiate the helper class objects
    statObj = Statistics(ixNetwork)
    portObj = Ports(ixNetwork)

    ixNetwork.NewConfig()
    ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
    ixNetwork.Globals.Licensing.Mode = licenseMode
    ixNetwork.LoadConfig(Files(configFile, local_file=True))

    # Optional: Assign ports.
    vportList = [vport.href for vport in ixNetwork.Vport.find()]
    testPorts = [dict(Arg1=port[0], Arg2=port[1], Arg3=port[2]) for port in portList]
    ixNetwork.AssignPorts(testPorts, [], vportList, forceTakePortOwnership )
        
    ixNetwork.StartAllProtocols(Arg1='sync')
    statObj.verifyAllProtocolSessions()

    # Create a Traffic Item with GRE packet header
    greTrafficItemObj, greFieldObj = createNewTrafficItem(trafficItemName='GRE', packetHeaderToAdd='^GRE', appendToStack='IPv4')
    greTrafficItemObj.Enable = False
    greFieldObj.singleValue = 3

    # Create a Traffic Item with UDP packet header
    udpTrafficItemObj, udpFieldObj = createNewTrafficItem(trafficItemName='BGP', packetHeaderToAdd='^UDP', appendToStack='IPv4')
    udpTrafficItemObj.Enable = False
    udpFieldObj.find(DisplayName='UDP-Source-Port').Auto = False
    udpFieldObj.find(DisplayName='UDP-Source-Port').SingleValue = 1000
    udpFieldObj.find(DisplayName='UDP-Dest-Port').Auto = False
    udpFieldObj.find(DisplayName='UDP-Dest-Port').SingleValue = 1001

    # Create a Traffic Item with TCP packet header
    tcpTrafficItemObj, tcpFieldObj = createNewTrafficItem(trafficItemName='OSPF', packetHeaderToAdd='TCP', appendToStack='IPv4')
    tcpTrafficItemObj.Enable = False
    tcpFieldObj.find(DisplayName='TCP-Source-Port').Auto = False
    tcpFieldObj.find(DisplayName='TCP-Source-Port').SingleValue = 1002
    tcpFieldObj.find(DisplayName='TCP-Dest-Port').Auto = False
    tcpFieldObj.find(DisplayName='TCP-Dest-Port').SingleValue = 1003

    for trafficItem in ixNetwork.Traffic.TrafficItem.find():
        trafficItem.Generate()

    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()
    
    stats = statObj.getTrafficItemStats()
    # Get the statistic values
    txFrames = stats[trafficItem.Name]['Tx Frames']
    rxFrames = stats[trafficItem.Name]['Rx Frames']
    print('\nTraffic Item Stats:\n\tTxFrames: {}  RxFrames: {}\n'.format(txFrames, rxFrames))

    # This example is for getting Flow Statistics.
    flowStats = statObj.getFlowStatistics()

    pprint(flowStats)
    for row, statValues in flowStats.items():
        txFrames = statValues['Tx Frames']
        rxFrames = statValues['Rx Frames']
        print('Flow Statistics: Row:{} TxFrames: {}  RxFrames: {}\n'.format(row, txFrames, rxFrames))


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

except Exception as errMsg:
    print('\nrestPy.Exception:', errMsg)
