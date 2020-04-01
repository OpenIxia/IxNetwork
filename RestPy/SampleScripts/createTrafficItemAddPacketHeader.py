"""
createTrafficItemAddPacketHeader.py

Description
   Configure custom packet headers in raw Traffic Item. 
  
   - Create a Raw Traffic Items. 
   - Example to show how to add packet header: Ethernet, PFC queue, PFC pause 802.1QBB, VLAN, IPv4 + DSCP, UDP, TCP and ICMP  
   - Enable tracking to track the packet headers in Flow Statistics

Requirements
   - Minimum IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install ixnetwork_restpy (minimum version 1.0.51)

RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy

Usage:
   - Enter: python <script>
"""

import os, sys, traceback
from pprint import pprint

# Import the RestPy module
from ixnetwork_restpy import SessionAssistant

apiServerIp = '192.168.70.3'

# A list of chassis to use instead of the ones in the loaded config file
ixChassisIpList = ['192.168.70.128']
portList = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 2, 1]]

# For Linux API server only
username = 'admin'
password = 'admin'

# For linux and windowsConnectionMgr only. Set to True to leave the session alive for debugging.
debugMode = False

forceTakePortOwnership = True


try:
    def createPacketHeader(trafficItemObj, packetHeaderToAdd=None, appendToStack=None): 
        configElement = trafficItemObj.ConfigElement.find()[0]

        # Do the followings to add packet headers on the new traffic item

        # Uncomment this to show a list of all the available protocol templates to create (packet headers)
        #for protocolHeader in ixNetwork.Traffic.ProtocolTemplate.find():
        #    ixNetwork.info('Protocol header: -- {} --'.format(protocolHeader.DisplayName))

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


    # LogLevel: none, info, warning, request, request_response, all
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=None, UserName='admin', Password='admin', 
                               SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel='all', LogFilename='restpy.log')

    ixNetwork = session.Ixnetwork

    # Assign ports
    portMap = session.PortMapAssistant()
    vport = dict()
    for index,port in enumerate(portList):
        portName = 'Port_{}'.format(index+1) 
        vport[portName] = portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=portName)

    portMap.Connect(forceTakePortOwnership)

    ixNetwork.info('Create a raw traffic item')
    rawTrafficItemObj = ixNetwork.Traffic.TrafficItem.add(Name='Raw packet', BiDirectional=False, TrafficType='raw')

    ixNetwork.info('Add source and destination endpoints')
    rawTrafficItemObj.EndpointSet.add(Sources=vport['Port_1'].Protocols.find(), Destinations=vport['Port_2'].Protocols.find())

    configElement = rawTrafficItemObj.ConfigElement.find()[0]
    configElement.FrameRate.update(Type='percentLineRate', Rate=50)
    configElement.TransmissionControl.update(Type='fixedFrameCount', FrameCount=10000)
    configElement.FrameSize.FixedSize = 128
  
    # The Ethernet packet header doesn't need to be created.
    # It is there by default. Just do a find for the Ethernet stack object.
    ethernetStackObj = ixNetwork.Traffic.TrafficItem.find(Name='Raw packet').ConfigElement.find()[0].Stack.find(DisplayName='Ethernet II')

    # NOTE: If you are using virtual ports (IxVM), you must use the Destination MAC address of 
    #       the IxVM port from your virtual host (ESX-i host or KVM)
    ixNetwork.info('Configuring Ethernet packet header')
    ethernetDstField = ethernetStackObj.Field.find(DisplayName='Destination MAC Address')
    ethernetDstField.ValueType = 'increment'
    ethernetDstField.StartValue = "00:0c:29:3a:8a:3a"
    ethernetDstField.StepValue = "00:00:00:00:00:00"
    ethernetDstField.CountValue = 1

    ethernetSrcField = ethernetStackObj.Field.find(DisplayName='Source MAC Address')
    ethernetSrcField.ValueType = 'increment'
    ethernetSrcField.StartValue = "00:0c:29:86:ba:0e"
    ethernetSrcField.StepValue = "00:00:00:00:00:00"
    ethernetSrcField.CountValue = 1

    # VLAN
    vlanFieldObj = createPacketHeader(rawTrafficItemObj, packetHeaderToAdd='^VLAN', appendToStack='Ethernet II')
    vlanField = vlanFieldObj.find(DisplayName='VLAN Priority')
    vlanField.Auto = False
    vlanField.SingleValue = 3

    # PFC QUEUE
    pfcQueueObj = ethernetStackObj.Field.find(DisplayName='PFC Queue')
    pfcQueueObj.ValueType = 'valueList'
    pfcQueueObj.ValueList = [1, 3, 5, 7]

    # PFC PAUSE: PFC PAUSE (802.1Qbb)
    pauseFrameObj = createPacketHeader(rawTrafficItemObj, packetHeaderToAdd='^PFC PAUSE \(802.1Qbb\)', appendToStack='Ethernet II')
    pauseFrameField = pauseFrameObj.find(DisplayName='Control opcode')
    pauseFrameField.ValueType = 'singleValue'
    pauseFrameField.SingleValue = 103

    pauseFrameQueue0 = pauseFrameObj.find(DisplayName='PFC Queue 0')
    pauseFrameQueue0.ValueType = 'singleValue'
    pauseFrameQueue0.SingleValue = 'abcd'

    pauseFrameQueue1 = pauseFrameObj.find(DisplayName='PFC Queue 1')
    pauseFrameQueue2 = pauseFrameObj.find(DisplayName='PFC Queue 2')
    pauseFrameQueue3 = pauseFrameObj.find(DisplayName='PFC Queue 3')
    pauseFrameQueue4 = pauseFrameObj.find(DisplayName='PFC Queue 4')
    pauseFrameQueue5 = pauseFrameObj.find(DisplayName='PFC Queue 5')
    pauseFrameQueue6 = pauseFrameObj.find(DisplayName='PFC Queue 6')


    # IPv4
    ipv4FieldObj = createPacketHeader(rawTrafficItemObj, packetHeaderToAdd='IPv4', appendToStack='^VLAN')
    ipv4SrcField = ipv4FieldObj.find(DisplayName='Source Address')
    ipv4SrcField.ValueType = 'increment'
    ipv4SrcField.StartValue = '1.1.1.1'
    ipv4SrcField.StepValue = '0.0.0.1'
    ipv4SrcField.CountValue = 1

    # Example on how to create a custom list of ip addresses
    ipv4DstField = ipv4FieldObj.find(DisplayName='Destination Address')
    ipv4DstField.ValueType = 'valueList'
    ipv4DstField.ValueList = ['1.1.1.2', '1.1.1.3', '1.1.1.4', '1.1.1.5']    

    # DSCP configurations and references

    # For IPv4 TOS/Precedence:  Field/4
    #    000 Routine, 001 Priority, 010 Immediate, 011 Flash, 100 Flash Override,
    #    101 CRITIC/ECP, 110 Internetwork Control, 111 Network Control
    ipv4PrecedenceField = ipv4FieldObj.find(DisplayName='Precedence')
    ipv4PrecedenceField.ActiveFieldChoice = True
    ipv4PrecedenceField.FieldValue = '011 Flash'

    # For IPv4 Raw priority: Field/3
    #ipv4RawPriorityField = ipv4FieldObj.find(DisplayName='Raw priority')
    #ipv4RawPriorityField.ActiveFieldChoice = True
    #ipv4RawPriorityField.ValueType = 'increment'
    #ipv4RawPriorityField.StartValue = 3
    #ipv4RawPriorityField.StepValue = 1
    #ipv4RawPriorityField.CountValue = 9

    # For IPv4 Default PHB
    #   Field/10: Default PHB
    #   Field/12: Class selector PHB
    #   Field/14: Assured forwarding PHB
    #   Field/15: Expedited forwarding PHB
    #
    #   For Class selector, if singleValue: Goes by 8bits:
    #       Precedence 1 = 8
    #       Precedence 2 = 16
    #       Precedence 3 = 24
    #       Precedence 4 = 32
    #       Precedence 5 = 40
    #       Precedence 6 = 48
    #       Precedence 7 = 56
    #
    # DisplayName options: 
    #     'Default PHB' = Field/10 
    #     'Class selector PHB' = Field/12
    #     'Assured forwarding PHB" = Field/14
    #     'Expedited forwarding PHB" = Field/16 
    #ipv4DefaultPHBField = ipv4FieldObj.find(DisplayName='Class selector')
    ipv4DefaultPHBField = ipv4FieldObj.find(DisplayName='Default PHB')

    ipv4DefaultPHBField.ActiveFieldChoice = True
    ipv4DefaultPHBField.ValueType = 'singleVaoue' ;# singleValue, increment
    ipv4DefaultPHBField.SingleValue = 56
    # Below is for increment 
    #ipv4DefaultPHBField.StartValue = 3
    #ipv4DefaultPHBField.StepValue = 1
    #ipv4DefaultPHBField.CountValue = 9

    # Example to show appending UDP after the IPv4 header
    udpFieldObj = createPacketHeader(rawTrafficItemObj, packetHeaderToAdd='^UDP', appendToStack='IPv4')
    udpSrcField = udpFieldObj.find(DisplayName='UDP-Source-Port')
    udpSrcField.Auto = False
    udpSrcField.SingleValue = 1000

    udpDstField = udpFieldObj.find(DisplayName='UDP-Dest-Port')
    udpDstField.Auto = False
    udpDstField.SingleValue = 1001

    # Example to show appending TCP after the IPv4 header
    tcpFieldObj = createPacketHeader(rawTrafficItemObj, packetHeaderToAdd='^TCP', appendToStack='IPv4')
    tcpSrcField = tcpFieldObj.find(DisplayName='TCP-Source-Port')
    tcpSrcField.Auto = False
    tcpSrcField.ValueType = 'valueList'
    tcpSrcField.ValueList = ['1002', '1005', '1007']

    tcpDstField = tcpFieldObj.find(DisplayName='TCP-Dest-Port')
    tcpDstField.Auto = False
    tcpDstField.SingleValue = 1003

    # Example to show appending ICMP after the IPv4 header
    icmpFieldObj = createPacketHeader(rawTrafficItemObj, packetHeaderToAdd='ICMP Msg Type: 9', appendToStack='IPv4')


    # Optional: Enable tracking to track your packet headers:
    #    
    #    Other trackings: udpUdpSrcPrt0, udpUdpDstPrt0,tcpTcpSrcPrt0, tcpTcpDstPrt0, vlanVlanId0, vlanVlanUserPriority0
    #    On an IxNetwork GUI (Windows or Web UI), add traffic item trackings.
    #    Then go on the API browser to view the tracking fields.
    rawTrafficItemObj.Tracking.find().TrackBy = ['udpUdpSrcPrt0', 'udpUdpDstPrt0']

    if debugMode == False:
        # For Linux and WindowsConnectionMgr only
        session.Session.remove()

except Exception as errMsg:
    ixNetwork.debug('\n%s' % traceback.format_exc())
    if debugMode == False and 'session' in locals():
        session.Session.remove()


