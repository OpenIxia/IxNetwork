"""
pcapToRawTrafficItem.py

   Tested with two back-2-back Ixia ports

   - Connect to the API server
   - Connect to chassis
   - Configure license server IP
   - Assign ports:
        - If variable forceTakePortOwnership is True, take over the ports if they're owned by another user.
        - If variable forceTakePortOwnership if False, abort test.
   - Configure a Raw Traffic Item
   - Read a PCAP file.
   - Add Traffic Item packet headers using PCAP packet header values.


Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements
   - IxNetwork 8.50
   - tcp.pcap file (Included in the same local directory).
   - pip install scapy
   - pip install requests
   - pip install -U --no-cache-dir ixnetwork_restpy

Usage:
   # Defaults to Windows
   - Enter: python <script>
"""

import sys, os, re, traceback

from scapy.all import *

# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant

# If you installed RestPy by doing a git clone instead of using pip, uncomment this line so
# your system knows where the RestPy modules are located.
#sys.path.append(os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', '')))

# Defaulting to windows
# Options: windows|connection_manager|linux
osPlatform = 'windows' 

apiServerIp = '192.168.70.3'

# For Linux API server only
username = 'admin'
password = 'admin'

# The IP address for your Ixia license server(s) in a list.
licenseServerIp = ['192.168.70.3']

# subscription, perpetual or mixed
licenseMode = 'subscription'

# For linux and windowsConnectionMgr only. Set to True to leave the session alive for debugging.
debugMode = False

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True

# A list of chassis to use
ixChassisIpList = ['192.168.70.128']
portList = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 2, 1]]

# The PCAP file to read
pcapFile = 'tcp.pcap'

try:
    testPlatform = TestPlatform(apiServerIp, log_file_name='restpy.log')

    # Console output verbosity: None|request|request_response
    testPlatform.Trace = 'request_response'

    testPlatform.Authenticate(username, password)
    session = testPlatform.Sessions.add()
    ixNetwork = session.Ixnetwork

    ixNetwork.NewConfig()    

    ixNetwork.info('\nConfiguring license server')
    ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
    ixNetwork.Globals.Licensing.Mode = licenseMode

    # Create vport for RAW Traffic Item source/dest endpoints
    vport1 = ixNetwork.Vport.add(Name='Port1')
    vport2 = ixNetwork.Vport.add(Name='Port2')

    # Assign ports
    testPorts = []
    vportList = [vport.href for vport in ixNetwork.Vport.find()]
    for port in portList:
        testPorts.append(dict(Arg1=port[0], Arg2=port[1], Arg3=port[2]))

    ixNetwork.AssignPorts(testPorts, [], vportList, forceTakePortOwnership)

    # This will get the last packet header from the tcp.pcap file.
    for index, packet in enumerate(PcapReader(pcapFile)):
        ixNetwork.info('\nPacket: {}:\n'.format(index, packet.show()))
        try:
            ethSrcAddr = packet[Ether].src
            ethDstAddr = packet[Ether].dst
            ipSrcAddr  = packet[IP].src
            ipDstAddr  = packet[IP].dst
            tcpSrcPort = packet[TCP].sport
            tcpDstPort = packet[TCP].dport
            
            ixNetwork.info('ethSrc: {} ethDst: {}'.format(ethSrc, ethDst))
            ixNetwork.info('ipSrc: {} ipDst: {}'.format(ipSrc, ipDst))
            ixNetwork.info('tcpSrcPort: {} tcpDstPort: {}'.format(tcpSrcPort, tcpDstPort))
        except:
            pass

    ixNetwork.info('Create Traffic Item')
    trafficItem = ixNetwork.Traffic.TrafficItem.add(Name='RAW TCP',
                                                    BiDirectional=False,
                                                    TrafficType='raw',
                                                    TrafficItemType='l2L3'
                                                )

    ixNetwork.info('Add flow group')
    trafficItem.EndpointSet.add(Sources=vport1.Protocols.find(), Destinations=vport2.Protocols.find())

    # Note: A Traffic Item could have multiple EndpointSets (Flow groups). 
    #       Therefore, ConfigElement is a list.
    ixNetwork.info('\tConfiguring config elements')
    configElement = trafficItem.ConfigElement.find()[0]
    configElement.FrameRate.Rate = 28
    configElement.FrameRate.Type = 'framesPerSecond'
    configElement.TransmissionControl.FrameCount = 10000
    configElement.TransmissionControl.Type = 'fixedFrameCount'
    configElement.FrameRateDistribution.PortDistribution = 'splitRateEvenly'
    configElement.FrameSize.FixedSize = 128
    trafficItem.Tracking.find()[0].TrackBy = ['flowGroup0']

    # Show a list of current configured packet headers in the first Traffic Item and first EndpointSet.
    ethernetStackObj = configElement.Stack.find(DisplayName='Ethernet II')

    # Uncomment this to show a list of all the available protocol templates (packet headers)
    #for protocolHeader in ixNetwork.Traffic.ProtocolTemplate():
    #    ixNetwork.info('\n', protocolHeader.DisplayName)

    # NOTE: If you are using virtual ports (IxVM), you must use the Destination MAC address of 
    #       the IxVM port from your virtual host (ESX-i host or KVM)
    ixNetwork.info('\nConfiguring Ethernet packet header')
    ethernetDstField = ethernetStackObj.Field.find(DisplayName='Destination MAC Address')
    ethernetDstField.ValueType = 'increment'
    ethernetDstField.StartValue = ethDstAddr
    ethernetDstField.StepValue = "00:00:00:00:00:00"
    ethernetDstField.CountValue = 1

    ethernetSrcField = ethernetStackObj.Field.find(DisplayName='Source MAC Address')
    ethernetSrcField.ValueType = 'increment'
    ethernetSrcField.StartValue = ethSrcAddr
    ethernetSrcField.StepValue = "00:00:00:00:00:01"
    ethernetSrcField.CountValue = 1

    # Add IPv4 packet header after the Ethernet stack
    # 1> Get the protocol template for IPv4
    ipv4ProtocolTemplate = ixNetwork.Traffic.ProtocolTemplate.find(DisplayName='IPv4')

    # 2> Append the IPv4 protocol header after the Ethernet stack.
    ethernetStackObj.Append(Arg2=ipv4ProtocolTemplate)

    # 3> Get the new IPv4 packet header stack to use it for appending any protocol after IP layer such as 
    #    UDP/TCP.
    # Look for the IPv4 packet header object.
    ipv4StackObj = configElement.Stack.find(DisplayName='IPv4')

    # 4> Configure the mpls packet header
    ipv4SrcFieldObj = ipv4StackObj.Field.find(DisplayName='Source Address')
    ipv4SrcFieldObj.ValueType = 'increment'
    ipv4SrcFieldObj.StartValue = ipSrcAddr
    ipv4SrcFieldObj.StepValue = "0.0.0.1"
    ipv4SrcFieldObj.CountValue = 1

    ipv4DstFieldObj = ipv4StackObj.Field.find(DisplayName='Destination Address')
    ipv4DstFieldObj.ValueType = 'increment'
    ipv4DstFieldObj.StartValue = ipDstAddr
    ipv4DstFieldObj.StepValue = "0.0.0.1"
    ipv4DstFieldObj.CountValue = 1

    # Add TCP packet header after the IPv4 packet header stack
    # 1> Get the protocol template for TCP
    tcpProtocolTemplate = ixNetwork.Traffic.ProtocolTemplate.find(DisplayName='TCP')

    # 2> Append the TCP protocol header after the IPv4 header.
    ipv4StackObj.Append(Arg2=tcpProtocolTemplate)

    tcpStackObj = configElement.Stack.find(DisplayName='TCP')

    tcpSrcPortFieldObj = tcpStackObj.Field.find(DisplayName='TCP-Source-Port')
    tcpSrcPortFieldObj.Auto = False
    tcpSrcPortFieldObj.SingleValue = tcpSrcPort

    tcpDstPortFieldObj = tcpStackObj.Field.find(DisplayName='TCP-Dest-Port')
    tcpDstPortFieldObj.Auto = False
    tcpDstPortFieldObj.SingleValue = tcpDstPort

    # This sample script does not expect traffic.
    # It is only demonstrating how to parse a pcap file and insert the values into a 
    # Traffic Item.

    if debugMode == False:
        # For Linux and WindowsConnectionMgr only
        session.remove()

except Exception as errMsg:
    ixNetwork.debug(traceback.format_exc())

    if debugMode == False and 'session' in locals():
        if osPlatform in ['linux', 'windowsConnectionMgr']:
            session.remove()
