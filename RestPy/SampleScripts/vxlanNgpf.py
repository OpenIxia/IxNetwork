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

RestPy Doc:
    https://www.openixia.com/userGuides/restPyDoc

Usage:
   # Defaults to Windows
   - Enter: python <script>

   # Connect to Windows Connection Manager
   - Enter: python <script> connection_manager <apiServerIp> <apiServerPort>

   # Connect to Linux API server
   - Enter: python <script> linux <apiServerIp> <apiServerPort>

"""

import sys, os, time, traceback

# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant

# Set defaults
osPlatform = 'windows'
apiServerIp = '192.168.70.3'
apiServerPort = 11009
username = 'admin'
password = 'admin'

# Allow passing in some params/values from the CLI to replace the defaults
if len(sys.argv) > 1:
    # Command line input:
    #   osPlatform: windows, connection_manager or linux
    osPlatform = sys.argv[1]
    apiServerIp = sys.argv[2]
    apiServerPort = sys.argv[3]

# The IP address for your Ixia license server(s) in a list.
licenseServerIp = ['192.168.70.3']
# subscription, perpetual or mixed
licenseMode = 'subscription'
# tier1, tier2, tier3, tier3-10g
licenseTier = 'tier3'

# For linux and windowsConnectionMgr only. Set to False to leave the session alive for debugging.
debugMode = True

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True

# A list of chassis to use
ixChassisIpList = ['192.168.70.128']
portList = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 2, 1]]

try:
    testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, platform=osPlatform, log_file_name='restpy.log')

    # Console output verbosity: None|request|'request response'
    testPlatform.Trace = 'request_response'

    testPlatform.Authenticate(username, password)
    session = testPlatform.Sessions.add()

    ixNetwork = session.Ixnetwork
    ixNetwork.NewConfig()

    ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
    ixNetwork.Globals.Licensing.Mode = licenseMode

    # Create vports and name them so you could use .find() to filter vports by the name.
    vport1 = ixNetwork.Vport.add(Name='Port1')
    vport2 = ixNetwork.Vport.add(Name='Port2')

    # Assign ports
    testPorts = []
    vportList = [vport.href for vport in ixNetwork.Vport.find()]
    for port in portList:
        testPorts.append(dict(Arg1=port[0], Arg2=port[1], Arg3=port[2]))

    ixNetwork.AssignPorts(testPorts, [], vportList, forceTakePortOwnership)

    ixNetwork.info('Creating Topology Group 1')
    topology1 = ixNetwork.Topology.add(Name='Topo1', Ports=vport1)
    deviceGroup1 = topology1.DeviceGroup.add(Name='DG1', Multiplier='1')

    ethernet1 = deviceGroup1.Ethernet.add(Name='Eth1')
    ethernet1.Mac.Increment(start_value='00:01:01:01:00:01', step_value='00:00:00:00:00:01')
    ethernet1.EnableVlans.Single(True)

    ixNetwork.info('\tConfiguring vlanID')
    vlanObj = ethernet1.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)

    ixNetwork.info('Configuring IPv4')
    ipv4 = ethernet1.Ipv4.add(Name='Ipv4-1')
    ipv4.Address.Increment(start_value='100.1.1.1', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='100.1.3.1', step_value='0.0.0.1')
    ipv4.Prefix.Single(16)

    ixNetwork.info('Configuring VxLAN')
    vxlan1 = ipv4.Vxlan.add(Name='VxLAN-1')
    vxlan1.Vni.Increment(start_value=1008, step_value=2)
    vxlan1.Ipv4_multicast.Increment(start_value='225.8.0.1', step_value='0.0.0.1')

    ixNetwork.info('Create Device Group for VxLAN')
    vxlanDeviceGroup1 = deviceGroup1.DeviceGroup.add(Name='VxLAN-DG', Multiplier=1)

    ixNetwork.info('Create Ethernet for VxLAN')
    vxlanEthernet1 = vxlanDeviceGroup1.Ethernet.add(Name='VxLAN-Ethernet')
    vxlanEthernet1.Mac.Increment(start_value='00:01:11:00:00:001', step_value='00:00:00:00:00:01')
    vxlanEthernet1.EnableVlans.Single(True)

    vxlanEthernet1.Vlan.find()[0].VlanId.Increment(start_value=101, step_value=0)

    ixNetwork.info('Create IPv4 for VxLAN')
    vxlanIpv4 = vxlanEthernet1.Ipv4.add(Name='VxLAN-IPv4')
    vxlanIpv4.Address.Increment(start_value='10.1.1.1', step_value='0.0.0.0')
    vxlanIpv4.GatewayIp.Increment(start_value='10.1.3.1', step_value='0.0.0.0')
    vxlanIpv4.Prefix.Single(16)
    vxlanIpv4.ResolveGateway.Single(True)

    ixNetwork.info('Creating Topology Group 2')
    # assignPorts() has created a list of vports based on the amount of your portList.
    topology2 = ixNetwork.Topology.add(Name='Topo2', Ports=vport2)
    deviceGroup2 = topology2.DeviceGroup.add(Name='MyDG2', Multiplier='1')

    ethernet2 = deviceGroup2.Ethernet.add(Name='Eth2')
    ethernet2.Mac.Increment(start_value='00:01:01:02:00:01', step_value='00:00:00:00:00:01')
    ethernet2.EnableVlans.Single(True)

    ixNetwork.info('Configuring vlanID')
    vlanObj = ethernet2.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)

    ixNetwork.info('Configuring IPv4')
    ipv4 = ethernet2.Ipv4.add(Name='Ipv4-2')
    ipv4.Address.Increment(start_value='100.1.3.1', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='100.1.1.1', step_value='0.0.0.1')
    ipv4.Prefix.Single(24)

    ixNetwork.info('Configuring VxLAN')
    vxlan2 = ipv4.Vxlan.add(Name='VxLAN-2')
    vxlan2.Vni.Increment(start_value=1008, step_value=1)
    vxlan2.Ipv4_multicast.Increment(start_value='225.8.0.1', step_value='0.0.0.0')

    ixNetwork.info('Create Device Group for VxLAN')
    vxlanDeviceGroup2 = deviceGroup2.DeviceGroup.add(Name='VxLAN-DG', Multiplier=1)

    ixNetwork.info('Create Ethernet for VxLAN')
    vxlanEthernet2 = vxlanDeviceGroup2.Ethernet.add(Name='VxLAN-Ethernet')
    vxlanEthernet2.Mac.Increment(start_value='00:01:22:00:00:001', step_value='00:00:00:00:00:01')
    vxlanEthernet2.EnableVlans.Single(True)

    vxlanEthernet2.Vlan.find()[0].VlanId.Increment(start_value=101, step_value=0)

    ixNetwork.info('Create IPv4 for VxLAN')
    vxlanIpv4 = vxlanEthernet2.Ipv4.add(Name='VxLAN-IPv4-2')
    vxlanIpv4.Address.Increment(start_value='10.1.3.1', step_value='0.0.0.0')
    vxlanIpv4.GatewayIp.Increment(start_value='10.1.1.1', step_value='0.0.0.0')
    vxlanIpv4.Prefix.Single(16)
    vxlanIpv4.ResolveGateway.Single(True)

    ixNetwork.StartAllProtocols(Arg1='sync')

    ixNetwork.info('Verify protocol sessions')
    protocolsSummary = StatViewAssistant(ixNetwork, 'Protocols Summary')
    protocolsSummary.CheckCondition('Sessions Not Started', StatViewAssistant.EQUAL, 0)
    protocolsSummary.CheckCondition('Sessions Down', StatViewAssistant.EQUAL, 0)
    ixNetwork.info(protocolsSummary)

    ixNetwork.info('Create Traffic Item')
    trafficItem = ixNetwork.Traffic.TrafficItem.add(Name='VxLAN traffic', BiDirectional=False, TrafficType='ipv4')

    ixNetwork.info('Add flow group')
    trafficItem.EndpointSet.add(Sources=topology1, Destinations=topology2)

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

    trafficItem.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()

    # StatViewAssistant could also filter by regex, LESS_THAN, GREATER_THAN, EQUAL. 
    # Examples:
    #    flowStatistics.AddRowFilter('Port Name', StatViewAssistant.REGEX, '^Port 1$')
    #    flowStatistics.AddRowFilter('Tx Frames', StatViewAssistant.LESS_THAN, 50000)

    flowStatistics = StatViewAssistant(ixNetwork, 'Flow Statistics')
    ixNetwork.info('{}\n'.format(flowStatistics))

    for rowNumber,flowStat in enumerate(flowStatistics.Rows):
        ixNetwork.info('\n\nSTATS: {}\n\n'.format(flowStat))
        ixNetwork.info('\nRow:{}  TxPort:{}  RxPort:{}  TxFrames:{}  RxFrames:{}\n'.format(
            rowNumber, flowStat['Tx Port'], flowStat['Rx Port'],
            flowStat['Tx Frames'], flowStat['Rx Frames']))

    if debugMode:
        # For Linux and WindowsConnectionMgr only
        session.remove()

except Exception as errMsg:
    ixNetwork.debug('\n%s' % traceback.format_exc())
    if debugMode and 'session' in locals():
        session.remove()



