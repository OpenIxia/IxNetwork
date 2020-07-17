"""
evpnNgpf.py:

   Tested with two back-2-back IxNetwork ports

   - Connect to the API server
   - Configure license server IP
   - Assign ports
   - Physical topology:                            Port1 ----- Port2
   - Configure two Topology Groups: Ce1 ---- Pe1 ---- P1 ----- P2 ---- Pe2 ---- Ce2
   - Between P1 and P2 when can set OSPF or ISIS to adv PE's loopbacks
   - Configure Network Group for each topology for route advertising
   - Start all protocols
   - Verify all protocols
   - Configure a Traffic Item from CE1 to CE2 - 100,000 packets
   - Start traffic
   - Get/Show Traffic Item
   - Get/Show Flow Statistics stats
   - Verify traffic Item pass when TX == 100,000 and RX traffic > 980,000

Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements:
   - IxNetwork 9.00
   - Python 2.7 and 3+
   - pip install requests
   - pip install ixnetwork_restpy (minimum version 1.0.51)

RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy

Usage:
   - Enter: python <script>

"""

import sys, re, time, traceback

# Import the RestPy module
from ixnetwork_restpy import SessionAssistant

apiServerIp = '192.168.70.3'

ixChassisIpList = ['192.168.70.128']
portList = [[ixChassisIpList[0], 1,1], [ixChassisIpList[0], 2, 1]]

# For Linux API server only
username = 'admin'
password = 'admin'

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = False

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True

#Test Variables
# ospf or isis
igp = 'isis'

# For Linux API server and Windows Connection Mgr only.
#    debugMode=True:  Leave the session opened for debugging.
#    debugMode=False: Remove the session when the script is done.
debugMode = False

try:
    # LogLevel: none, info, warning, request, request_response, all
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=None, UserName='admin', Password='admin', 
                               SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel='all', LogFilename='restpy.log')

    ixNetwork = session.Ixnetwork

    ixNetwork.info('Assign ports')
    portMap = session.PortMapAssistant()
    vport = dict()
    for index,port in enumerate(portList):
        portName = 'Port_{}'.format(index+1)
        vport[portName] = portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=portName)

    portMap.Connect(forceTakePortOwnership)

    ixNetwork.info('Creating Topology PE-1')
    topology1 = ixNetwork.Topology.add(Name='PE1 - Topo', Ports=vport['Port_1'])

    deviceGroup1 = topology1.DeviceGroup.add(Name='P1 - 100.1.0.1', Multiplier='1')
    ethernet1 = deviceGroup1.Ethernet.add(Name='Eth')
    ethernet1.Mac.Increment(start_value='00:ca:ff:ee:00:01', step_value='00:00:00:00:00:00')
    ethernet1.EnableVlans.Single(False)

    ixNetwork.info('Configuring P1 IPv4')
    ipv4 = ethernet1.Ipv4.add(Name='Ipv4')
    ipv4.Address.Increment(start_value='100.1.0.1', step_value='0.0.0.0')
    ipv4.GatewayIp.Increment(start_value='100.1.0.2', step_value='0.0.0.0')

    ixNetwork.info('Configuring Ldp')
    p1Ldp = ipv4.LdpBasicRouter.add(Name='ldp')

    if igp.lower() == 'ospf':
        ixNetwork.info('Configuring Ospf Router on P1')
        p1Ospf = ipv4.Ospfv2.add(Name='ospf-100.1.0.1')
        p1Ospf.NeighborIp.Increment(start_value='100.1.0.2', step_value='0.0.0.1')
        p1Ospf.NetworkType.Single('pointtopoint')

    elif igp.lower() == 'isis':
        ixNetwork.info('Configuring Isis Router on P1')
        p1Isis = ethernet1.IsisL3.add(Name='Isis P1 Router')
        p1Isis.NetworkType.Single('pointpoint')
        p1Isis.LevelType.Single('level2')
        isisl3router = deviceGroup1.IsisL3Router.find(Name='ISIS-L3 RTR.*')
        isisl3router.EnableWideMetric.Single(True)


    ixNetwork.info('Configuring PE1 Loopbackpool')
    networkGroup1 = deviceGroup1.NetworkGroup.add(Name='PE1-Loopbacks', Multiplier='1')
    ipv4PrefixPool = networkGroup1.Ipv4PrefixPools.add(NumberOfAddresses='2')
    ipv4PrefixPool.NetworkAddress.Increment(start_value='1.1.1.1', step_value='0.0.0.1')
    ipv4PrefixPool.PrefixLength.Single(32)

    pe1DevGroup1 = networkGroup1.DeviceGroup.add(Name='PE1-1.1.1.1/2', Multiplier='2')
    pe1LoopBackv4 = pe1DevGroup1.Ipv4Loopback.add(Name='loopback')
    pe1LoopBackv4.Address.Increment(start_value='1.1.1.1', step_value='0.0.0.1')

    pe1Bgp = pe1LoopBackv4.BgpIpv4Peer.add(Name='Pe1Bgp')
    pe1Bgp.update(EthernetSegmentsCountV4=2)
    pe1Bgp.DutIp.Increment(start_value='2.2.2.2', step_value='0.0.0.1')
    pe1Bgp.Type.Single('internal')
    pe1Bgp.LocalAs2Bytes.Increment(start_value=15169, step_value=0)
    pe1Bgp.BgpId.Increment(start_value='1.1.1.1', step_value='0.0.0.1')
    pe1Bgp.Evpn.Single(True)
    pe1Bgp.FilterEvpn.Single(True)

    pe1Evi = pe1Bgp.BgpIPv4EvpnEvi.add()
    pe1Evi.RdEvi.ValueList(['1','2'])

    ce1Pool = pe1DevGroup1.NetworkGroup.add(Name='CE1')
    ce1MacPool = ce1Pool.MacPools.add(Name='Customers')

    pe1Evi.EnableL3vniTargetList.Single(True)
    ce1V4Pool = ce1MacPool.Ipv4PrefixPools.add(Name='Customers')

    # Port 2 - PE2
    ixNetwork.info('Creating Topology PE-2')
    topology2 = ixNetwork.Topology.add(Name='PE2 - Topo', Ports=vport['Port_2'])

    deviceGroup2 = topology2.DeviceGroup.add(Name='P2 - 100.1.0.2', Multiplier='1')
    ethernet2 = deviceGroup2.Ethernet.add(Name='Eth')
    ethernet2.Mac.Increment(start_value='00:ca:ff:ee:02:01', step_value='00:00:00:00:00:00')
    ethernet2.EnableVlans.Single(False)

    ixNetwork.info('Configuring P2 IPv4')
    p2Ipv4 = ethernet2.Ipv4.add(Name='Ipv4')
    p2Ipv4.Address.Increment(start_value='100.1.0.2', step_value='0.0.0.0')
    p2Ipv4.GatewayIp.Increment(start_value='100.1.0.1', step_value='0.0.0.0')

    ixNetwork.info('Configuring Ldp')
    p2Ldp = p2Ipv4.LdpBasicRouter.add(Name='ldp')

    ixNetwork.info('Configuring Igp Router on P2')

    if igp.lower() == 'ospf':
        ixNetwork.info('Configuring Ospf Router on P2')
        p2Ospf = p2Ipv4.Ospfv2.add(Name='ospf-100.1.0.2')
        p2Ospf.NeighborIp.Increment(start_value='100.1.0.1', step_value='0.0.0.0')
        p2Ospf.NetworkType.Single('pointtopoint')

    elif igp.lower() == 'isis':
        ixNetwork.info('Configuring Isis Router on P2')
        p2Isis = ethernet2.IsisL3.add(Name='Isis P2 Router')
        p2Isis.NetworkType.Single('pointpoint')
        p2Isis.LevelType.Single('level2')
        p2Isisl3router = deviceGroup2.IsisL3Router.find(Name='ISIS-L3 RTR.*')
        p2Isisl3router.EnableWideMetric.Single(True)

    ixNetwork.info('Configuring PE2 Loopbackpool')
    p2NetworkGroup = deviceGroup2.NetworkGroup.add(Name='PE2-Loopbacks', Multiplier='1')
    p2Ipv4PrefixPool = p2NetworkGroup.Ipv4PrefixPools.add(NumberOfAddresses='2')
    p2Ipv4PrefixPool.NetworkAddress.Increment(start_value='2.2.2.2', step_value='0.0.0.1')
    p2Ipv4PrefixPool.PrefixLength.Single(32)

    pe2DevGroup1 = p2NetworkGroup.DeviceGroup.add(Name='PE2-2.2.2.2/3', Multiplier='2')
    pe2LoopBackv4 = pe2DevGroup1.Ipv4Loopback.add(Name='loopback')
    pe2LoopBackv4.Address.Increment(start_value='2.2.2.2', step_value='0.0.0.1')

    pe2Bgp = pe2LoopBackv4.BgpIpv4Peer.add(Name='Pe2Bgp')
    pe2Bgp.update(EthernetSegmentsCountV4=2)
    pe2Bgp.DutIp.Increment(start_value='1.1.1.1', step_value='0.0.0.1')
    pe2Bgp.Type.Single('internal')
    pe2Bgp.LocalAs2Bytes.Increment(start_value=15169, step_value=0)
    pe2Bgp.BgpId.Increment(start_value='2.2.2.2', step_value='0.0.0.1')
    pe2Bgp.Evpn.Single(True)
    pe2Bgp.FilterEvpn.Single(True)

    pe2Evi = pe2Bgp.BgpIPv4EvpnEvi.add()
    pe2Evi.RdEvi.ValueList(['1','2'])

    ce2Pool = pe2DevGroup1.NetworkGroup.add(Name='CE2')
    ce2MacPool = ce2Pool.MacPools.add(Name='Mac - Customers')

    pe2Evi.EnableL3vniTargetList.Single(True)
    ce2V4Pool = ce2MacPool.Ipv4PrefixPools.add(Name='L3 - Customers')

    ixNetwork.StartAllProtocols(Arg1='sync')

    ixNetwork.info('Verify protocol sessions\n')
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    protocolSummary.AddRowFilter('Protocol Type', protocolSummary.REGEX, '(?i)^BGP?')
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.GREATER_THAN_OR_EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
    ixNetwork.info(protocolSummary)

    ixNetwork.info('Create Traffic Item')
    traffCe1ToCe2 = ixNetwork.Traffic.TrafficItem.add(Name='CE1 to CE2 Traffic', BiDirectional=False, TrafficType='ipv4')
    ixNetwork.info('Add endpoint flow group')
    traffCe1ToCe2.EndpointSet.add(Sources=ce1V4Pool, Destinations=ce2V4Pool)
    configElement = traffCe1ToCe2.ConfigElement.find()[0]
    configElement.FrameRate.update(Type='percentLineRate', Rate=50)
    configElement.TransmissionControl.update(Type='fixedFrameCount', FrameCount=100000)
    configElement.FrameRateDistribution.PortDistribution = 'splitRateEvenly'
    configElement.FrameSize.FixedSize = 1280
    traffCe1ToCe2.Tracking.find()[0].TrackBy = ['trafficGroupId0']

    traffCe1ToCe2.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()

    trafficItemStatistics = session.StatViewAssistant('Traffic Item Statistics')
    ixNetwork.info('{}\n'.format(trafficItemStatistics))

    flowStatistics = session.StatViewAssistant('Flow Statistics')
    flowStatistics.AddRowFilter('Traffic Item', flowStatistics.REGEX, '^CE1.*')
    flowStatistics.AddRowFilter('Tx Frames', flowStatistics.EQUAL, 100000)
    flowStatistics.AddRowFilter('Rx Frames', flowStatistics.GREATER_THAN_OR_EQUAL, 98000)

    ixNetwork.info('{}\n'.format(flowStatistics))

    if debugMode == False:
        if 'session' in locals():
            session.Session.remove()

except Exception as errMsg:
    # print('\n%s' % traceback.format_exc(None, errMsg))
    print(traceback.print_exception())
    if 'session' in locals():
        session.Session.remove()

