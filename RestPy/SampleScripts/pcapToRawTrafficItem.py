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
   - Python 2.7 and 3+
   - tcp.pcap file (Included in the same local directory).
   - pip install scapy
   - pip install requests
   - pip install -U --no-cache-dir ixnetwork_restpy
   - Helper functions: https://github.com/OpenIxia/IxNetwork/RestApi/Python/Restpy/Modules:
                       - Statistics.py and PortMgmt.py

Script development API doc:
   - The doc is located in your Python installation site-packages/ixnetwork_restpy/docs/index.html
   - On a web browser:
         - If installed in Windows: enter: file://c:/<path_to_ixnetwork_restpy>/docs/index.html
         - If installed in Linux: enter: file:///<path_to_ixnetwork_restpy>/docs/index.html

Usage:
   # Defaults to Windows
   - Enter: python <script>

   # Connect to Windows Connection Manager
   - Enter: python <script> windowsConnectionMgr

   # Connect to Linux API server
   - Enter: python <script> linux

"""

import sys, os, re

from scapy.all import *

# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform

# If you got RestPy by doing a git clone instead of using pip, uncomment this line so
# your system knows where the RestPy modules are located.
#sys.path.append(os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', '')))

# This sample script uses helper functions from https://github.com/OpenIxia/IxNetwork/tree/master/RestPy/Modules
# If you did a git clone, add this path to use the helper modules: StatisticsMgmt.py and PortMgmt.py
# Otherwise, you could store these helper functions any where on your filesystem and set their path by using sys.path.append('your path')
sys.path.append(os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules')))

# Import modules containing helper functions
from StatisticsMgmt import Statistics
from PortMgmt import Ports

# Defaulting to windows
osPlatform = 'windows'

if len(sys.argv) > 1:
    # Command line input: windows, windowsConnectionMgr or linux
    osPlatform = sys.argv[1]

# Change API server values to use your setup
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

# The IP address for your Ixia license server(s) in a list.
licenseServerIp = ['192.168.70.3']
# subscription, perpetual or mixed
licenseMode = 'subscription'

# For linux and windowsConnectionMgr only. Set to False to leave the session alive for debugging.
deleteSessionWhenDone = True

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True

# A list of chassis to use
ixChassisIpList = ['192.168.70.128']
portList = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 1, 2]]

pcapFile = 'tcp.pcap'

try:
    testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, platform=platform, log_file_name='restpy.log')

    # Console output verbosity: None|request|request_response
    testPlatform.Trace = 'request_response'

    if osPlatform == 'linux':
        testPlatform.Authenticate(username, password)

    session = testPlatform.Sessions.add()
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

    # This will get the last packet header from the tcp.pcap file.
    for index, packet in enumerate(PcapReader(pcapFile)):
        print('\nPacket: {}:\n'.format(index, packet.show()))
        try:
            ethSrcAddr = packet[Ether].src
            ethDstAddr = packet[Ether].dst
            ipSrcAddr  = packet[IP].src
            ipDstAddr  = packet[IP].dst
            tcpSrcPort = packet[TCP].sport
            tcpDstPort = packet[TCP].dport
            
            print('ethSrc: {} ethDst: {}'.format(ethSrc, ethDst))
            print('ipSrc: {} ipDst: {}'.format(ipSrc, ipDst))
            print('tcpSrcPort: {} tcpDstPort: {}'.format(tcpSrcPort, tcpDstPort))
        except:
            pass

    print('\nCreate Traffic Item')
    trafficItem = ixNetwork.Traffic.TrafficItem.add(Name='RAW TCP',
                                                    BiDirectional=False,
                                                    TrafficType='raw',
                                                    TrafficItemType='l2L3'
                                                )

    print('\tAdd flow group')
    trafficItem.EndpointSet.add(Sources=vport1.Protocols.find(), Destinations=vport2.Protocols.find())

    # Note: A Traffic Item could have multiple EndpointSets (Flow groups). 
    #       Therefore, ConfigElement is a list.
    print('\tConfiguring config elements')
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
    #    print('\n', protocolHeader.DisplayName)

    # NOTE: If you are using virtual ports (IxVM), you must use the Destination MAC address of 
    #       the IxVM port from your virtual host (ESX-i host or KVM)
    print('\nConfiguring Ethernet packet header')
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

    if deleteSessionWhenDone:
        # For Linux and WindowsConnectionMgr only
        if osPlatform in ['linux', 'windowsConnectionMgr']:
            session.remove()

except Exception as errMsg:
    print('\nrestPy.Exception:', errMsg)
    if deleteSessionWhenDone and 'session' in locals():
        if osPlatform in ['linux', 'windowsConnectionMgr']:
            session.remove()
