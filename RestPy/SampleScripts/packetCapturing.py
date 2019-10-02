"""
packetCapturing.py

   - Connecting to an existing session with traffic preconfigured to send at continuous mode.
   - User settings:
        - captureControlPlane: True|False
        - captureDataPlane: True|False
        - Get the vport object for packet capturing

   - Start continuous traffic
   - Configure vport (capturing port) to user settings
   - Start capturing
   - Wait for minimum 30 seconds
   - Stop capturing
   - Stop traffic
   - Get captured packets on Wireshark:
       - There could be over 7000 packets.
       - User must set the for loop with the starting packet value and ending packet value to inspect.


Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements
   - IxNetwork 8.50
   - Python 2.7 and 3+

RestPy installation
   - pip install requests
   - pip install -U --no-cache-dir ixnetwork_restpy

RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy
"""

import os, sys, time, traceback
# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.files import Files
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant

apiServerIp = '192.168.70.3'

# windows|connection_manager|linux
osPlatform = 'windows'

# For Linux API server only
username = 'admin'
password = 'admin'

try:
    testPlatform = TestPlatform(apiServerIp, log_file_name='restpy.log')

    # Console output verbosity: 'none'|request|request_response
    testPlatform.Trace = 'none'

    if osPlatform == 'linux':
        testPlatform.Authenticate(username, password)
        session = testPlatform.Sessions.find(Id=1)

    if osPlatform in ['windows', 'connection_manager']:
        # Windows support only one session. Id is always equal 1.
        session = testPlatform.Sessions.find(Id=1)

    # ixNetwork is the root object to the IxNetwork API tree.
    ixNetwork = session.Ixnetwork

    captureControlPlane = True
    captureDataPlane = True

    # Get the packet capturing vport
    vport = ixNetwork.Vport.find()[1]
    vport.RxMode = 'captureAndMeasure'

    # -softwareEnabled == Control Plane
    # -hardwareEnabled == Data Plane
    ixNetwork.info('\nConfigure capture')
    vport.Capture.SoftwareEnabled = captureControlPlane
    vport.Capture.HardwareEnabled = captureDataPlane

    ixNetwork.info('CloseAllTabs')
    ixNetwork.CloseAllTabs()

    if captureDataPlane:
        ixNetwork.info('Apply traffic')
        ixNetwork.Traffic.Apply()

        # Note:  Start traffic must be called before calling start capture.
        #        If you call them the other way around, then the started capture will be stopped by calling startTraffic().
        ixNetwork.info('Start traffic')
        ixNetwork.Traffic.Start()

    ixNetwork.info('Start Capture')
    ixNetwork.StartCapture()

    # It is safer to let data traffic and control plane run for 30 seconds minimum.
    # For control plane, some protocols are set at 10 seconds interval, some are set at 30+ seconds.
    # Set the sleep time accordingly.
    ixNetwork.info('Wait 30 seconds')
    time.sleep(30)

    ixNetwork.info('Stop capture')
    ixNetwork.StopCapture()

    if captureDataPlane:
        ixNetwork.info('Stop traffic')
        ixNetwork.Traffic.Stop()


    if captureDataPlane:
        ixNetwork.info('Total data packets captured: {}'.format(vport.Capture.DataPacketCounter))

        # There could be thousands of packets captured.  State the amount of packets to 
        # inspect with a starting value and an ending value.
        for packetNumber in range(1, 2):
            try:
                # Note: GetPacketFromDataCapture() will create the packet header fields
                vport.Capture.CurrentPacket.GetPacketFromDataCapture(Arg2=packetNumber)
                packetHeaderStacks = vport.Capture.CurrentPacket.Stack.find()
            except Exception as errMsg:
                print('\nError: {}'.format(errMsg))
                continue

            for packetHeader in packetHeaderStacks.find():
                print('\nPacketHeaderName: {}'.format(packetHeader.DisplayName))
                for field in packetHeader.Field.find():
                    print('\t{}: {}'.format(field.DisplayName, field.FieldValue)) 

                    # Do your parsing and logics here using the packetHeader and field.FieldValue


    if captureControlPlane:
        ixNetwork.info('Total control packets captured: {}'.format(vport.Capture.ControlPacketCounter))

        # There could be thousands of packets captured.  State the amount of packets to 
        # inspect with a starting value and an ending value.
        for packetNumber in range(1, 2):

            try:
                # Note: GetPacketFromDataCapture() will create the packet header fields
                vport.Capture.CurrentPacket.GetPacketFromControlCapture(Arg2=packetNumber)
                packetHeaderStacks = vport.Capture.CurrentPacket.Stack.find()
            except Exception as errMsg:
                print('\nError: {}'.format(errMsg))
                continue

            for packetHeader in packetHeaderStacks.find():
                print('\nPacketHeaderName: {}'.format(packetHeader.DisplayName))
                for field in packetHeader.Field.find():
                    print('\t{}: {}'.format(field.DisplayName, field.FieldValue)) 

                    # Do your parsing and logics here using the packetHeader and field.FieldValue


    '''
    Example on wireshark output:

    PacketHeaderName: Frame
        Interface id: 0
        WTAP_ENCAP: 1
        Arrival Time: Dec 31, 1969 16:00:07.056489960 Pacific Standard Time
        Time shift for this packet: 0.000000000
        Epoch Time: 7.056489960
        Time delta from previous captured frame: 0.000005600
        Time delta from previous displayed frame: 0.000005600
        Time since reference or first frame: 0.000005600
        Frame Number: 2
        Frame length on the wire: 128
        Frame length stored into the capture file: 128
        Frame is marked: False
        Frame is ignored: False
        Protocols in frame: eth:vlan:ip:data

    PacketHeaderName: Ethernet
        Destination: 00:0c:29:3a:38:3a
        Address: 00:0c:29:3a:38:3a
        LG bit: False
        IG bit: False
        Source: 00:0c:29:86:ba:0e
        Address: 00:0c:29:86:ba:0e
        LG bit: False
        IG bit: False
        Type: 33024

    PacketHeaderName: 802.1Q Virtual LAN
        Priority: 0
        CFI: 0
        ID: 103
        Type: 2048
        Trailer: 5613399f

    PacketHeaderName: Internet Protocol
        Version: 4
        Header Length: 20
        Differentiated Services field: 0
        Differentiated Services Codepoint: 0
        Explicit Congestion Notification: 0
        Type of Service: 0
        Precedence: 0
        Delay: False
        Throughput: False
        Reliability: False
        Cost: False
        MBZ: False
        Total Length: 106
        Identification: 0
        Flags: 0
        Reserved bit: False
        Don't fragment: False
        More fragments: False
        Fragment offset: 0
        Time to live: 64
        Protocol: 61
        Header checksum: 23558
        Good: True
        Bad: False
        Source: 10.10.0.26
        Source or Destination Address: 10.10.0.26
        Source Host: 10.10.0.26
        Source or Destination Host: 10.10.0.26
        Destination: 20.20.0.26
        Source or Destination Address: 20.20.0.26
        Destination Host: 20.20.0.26
        Source or Destination Host: 20.20.0.26
        Source GeoIP: Unknown: 
        Destination GeoIP: Unknown: 

    PacketHeaderName: Data
        Data: eb57d6e9b7a240dc497869600000000010111213150365a518191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f30313233...
        Length: 86
    '''
        

except Exception as errMsg:
    print('\nError: %s' % traceback.format_exc())
    print('\nrestPy.Exception:', errMsg)
