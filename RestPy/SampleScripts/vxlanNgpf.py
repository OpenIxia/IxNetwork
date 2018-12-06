"""
vxlanNgpf.py:

   Tested with two back-2-back Ixia ports

   - Connect to the API server
   - Configure license server IP
   - Assign ports:
        - If variable forceTakePortOwnership is True, take over the ports if they're owned by another user.
        - If variable forceTakePortOwnership if False, abort test.
   - Configure two Topology Groups: vxLAN/IPv4
   - Configure a Traffic Item
   - Start all protocols
   - Verify all protocols
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

import sys, os

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

    ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
    ixNetwork.Globals.Licensing.Mode = licenseMode

    # Create vports and name them so you could get the vports by the name when creating Topology.
    vport1 = ixNetwork.Vport.add(Name='Port1')
    vport2 = ixNetwork.Vport.add(Name='Port2')

    portObj.assignPorts(portList, forceTakePortOwnership, getVportList=True)

    print('\nCreating Topology Group 1')
    # assignPorts() has created a list of vports based on the amount of your portList.
    topology1 = ixNetwork.Topology.add(Name='Topo1', Ports=vport1)
    deviceGroup1 = topology1.DeviceGroup.add(Name='DG1', Multiplier='1')

    ethernet1 = deviceGroup1.Ethernet.add(Name='Eth1')
    ethernet1.Mac.Increment(start_value='00:01:01:01:00:01', step_value='00:00:00:00:00:01')
    ethernet1.EnableVlans.Single(True)

    print('\tConfiguring vlanID')
    vlanObj = ethernet1.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)

    print('\tConfiguring IPv4')
    ipv4 = ethernet1.Ipv4.add(Name='Ipv4-1')
    ipv4.Address.Increment(start_value='100.1.1.1', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='100.1.3.1', step_value='0.0.0.1')
    ipv4.Prefix.Single(16)

    print('\tConfiguring VxLAN')
    vxlan1 = ipv4.Vxlan.add(Name='VxLAN-1')
    vxlan1.Vni.Increment(start_value=1008, step_value=2)
    vxlan1.Ipv4_multicast.Increment(start_value='225.8.0.1', step_value='0.0.0.1')

    print('Create Device Group for VxLAN')
    vxlanDeviceGroup1 = deviceGroup1.DeviceGroup.add(Name='VxLAN-DG', Multiplier=1)

    print('Create Ethernet for VxLAN')
    vxlanEthernet1 = vxlanDeviceGroup1.Ethernet.add(Name='VxLAN-Ethernet')
    vxlanEthernet1.Mac.Increment(start_value='00:01:11:00:00:001', step_value='00:00:00:00:00:01')
    vxlanEthernet1.EnableVlans.Single(True)

    vxlanEthernet1.Vlan.find()[0].VlanId.Increment(start_value=101, step_value=0)

    print('Create IPv4 for VxLAN')
    vxlanIpv4 = vxlanEthernet1.Ipv4.add(Name='VxLAN-IPv4')
    vxlanIpv4.Address.Increment(start_value='10.1.1.1', step_value='0.0.0.0')
    vxlanIpv4.GatewayIp.Increment(start_value='10.1.3.1', step_value='0.0.0.0')
    vxlanIpv4.Prefix.Single(16)
    vxlanIpv4.ResolveGateway.Single(True)

    print('\nCreating Topology Group 2')
    # assignPorts() has created a list of vports based on the amount of your portList.
    topology2 = ixNetwork.Topology.add(Name='Topo2', Ports=vport2)
    deviceGroup2 = topology2.DeviceGroup.add(Name='MyDG2', Multiplier='1')

    ethernet2 = deviceGroup2.Ethernet.add(Name='Eth2')
    ethernet2.Mac.Increment(start_value='00:01:01:02:00:01', step_value='00:00:00:00:00:01')
    ethernet2.EnableVlans.Single(True)

    print('\tConfiguring vlanID')
    vlanObj = ethernet2.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)

    print('\tConfiguring IPv4')
    ipv4 = ethernet2.Ipv4.add(Name='Ipv4-2')
    ipv4.Address.Increment(start_value='100.1.3.1', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='100.1.1.1', step_value='0.0.0.1')
    ipv4.Prefix.Single(24)

    print('\tConfiguring VxLAN')
    vxlan2 = ipv4.Vxlan.add(Name='VxLAN-2')
    vxlan2.Vni.Increment(start_value=1008, step_value=1)
    vxlan2.Ipv4_multicast.Increment(start_value='225.8.0.1', step_value='0.0.0.0')

    print('Create Device Group for VxLAN')
    vxlanDeviceGroup2 = deviceGroup2.DeviceGroup.add(Name='VxLAN-DG', Multiplier=1)

    print('Create Ethernet for VxLAN')
    vxlanEthernet2 = vxlanDeviceGroup2.Ethernet.add(Name='VxLAN-Ethernet')
    vxlanEthernet2.Mac.Increment(start_value='00:01:22:00:00:001', step_value='00:00:00:00:00:01')
    vxlanEthernet2.EnableVlans.Single(True)

    vxlanEthernet2.Vlan.find()[0].VlanId.Increment(start_value=101, step_value=0)

    print('Create IPv4 for VxLAN')
    vxlanIpv4 = vxlanEthernet2.Ipv4.add(Name='VxLAN-IPv4-2')
    vxlanIpv4.Address.Increment(start_value='10.1.3.1', step_value='0.0.0.0')
    vxlanIpv4.GatewayIp.Increment(start_value='10.1.1.1', step_value='0.0.0.0')
    vxlanIpv4.Prefix.Single(16)
    vxlanIpv4.ResolveGateway.Single(True)

    ixNetwork.StartAllProtocols(Arg1='sync')
    statObj.verifyAllProtocolSessions()

    print('\nCreate Traffic Item')
    trafficItem = ixNetwork.Traffic.TrafficItem.add(Name='VxLAN traffic', BiDirectional=False, TrafficType='ipv4')

    print('\tAdd flow group')
    trafficItem.EndpointSet.add(Sources=topology1, Destinations=topology2)

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

    trafficItem.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()

    # Get the Traffic Item name for getting Traffic Item statistics.
    trafficItemName = trafficItem.Name

    # Get and show the Traffic Item column caption names and stat values
    columnNames      = statObj.getStatViewResults(statViewName='Traffic Item Statistics', getColumnCaptions=True)
    trafficItemStats = statObj.getStatViewResults(statViewName='Traffic Item Statistics', rowValuesLabel=trafficItemName)

    # The columnNames variable contains all the stat counter names.
    # Get the index position of the stat counter that you want.
    # The index is aligned with trafficItemStats that contains the statistic values.
    txFramesIndex = columnNames.index('Tx Frames')
    rxFramesIndex = columnNames.index('Rx Frames')

    # Get the statistic values with the indexes.
    txFrames = trafficItemStats[txFramesIndex]
    rxFrames = trafficItemStats[rxFramesIndex]

    print('\nTraffic Item Stats:\n\tTxFrames: {0}  RxFrames: {1}\n'.format(txFrames, rxFrames))

    # This example is for getting Flow Statistics.
    columnCaptions =   statObj.getStatViewResults(statViewName='Flow Statistics', getColumnCaptions=True)
    flowStats = statObj.getFlowStatistics()
    print('\n', columnCaptions)
    for statValues in flowStats:
        print('\n{0}'.format(statValues))
    print()

    if deleteSessionWhenDone:
        # For Linux and WindowsConnectionMgr only
        if osPlatform in ['linux', 'windowsConnectionMgr']:
            session.remove()

except Exception as errMsg:
    print('\nrestPy.Exception:', errMsg)
    if deleteSessionWhenDone and 'session' in locals():
        if osPlatform in ['linux', 'windowsConnectionMgr']:
            session.remove()



