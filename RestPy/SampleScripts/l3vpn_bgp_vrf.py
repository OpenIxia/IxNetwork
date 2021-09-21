"""
l3vpn_bgp_vrf.py:

Tested with two back-2-back IxNetwork ports.
   - Connect to the API server
   - Assign ports
   - Physical topology:  Port1 ----- Port2
   - Configure two Topology Groups: VRF1 ---- PE1 ---- P1----- P2 ---- PE2 ---- VRF2
   - Between P1 and P2 when can set OSPF or ISIS to advertize PE's loopbacks
   - Configure Network Group for each topology for vpn route advertising
   - Start all protocols
   - Verify all protocols has up
   - Configure a Traffic Item from VRF1 to VRF2 - 1000 packets
   - Start traffic
   - Get/Show Traffic Item
   - Get/Show Flow Statistics stats
   - Verify traffic Item pass when TX == 1000 and RX traffic > 980,000
   
Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux
Requirements:
   - Minimum IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install ixnetwork_restpy (minimum version 1.0.51)
RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy/#/
Usage:
   - Enter: python <script>
"""


import sys, os, time, traceback

from ixnetwork_restpy import SessionAssistant

apiServerIp = '10.39.33.143'

ixChassisIpList = ['10.39.33.143']
portList = [[ixChassisIpList[0], 1,1], [ixChassisIpList[0], 1, 2]]

# For Linux API server only
username = 'admin'
password = 'ixia123'

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = False

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True


try:
#Connection to Linux API Server
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=None, UserName=username, Password=password, SessionName=None, SessionId=None, ApiKey=None,
                                ClearConfig=True, LogLevel='all', LogFilename='restpy.log')

    # igp between P-P either ospf or isis
    igp ='ospf'

    ixNetwork = session.Ixnetwork
    
    ixNetwork.info('Assign test ports into IxNetwork')

    portMap = session.PortMapAssistant()
    vport = dict()

    for index,port in enumerate(portList):
        portName = 'Port_{}'.format(index+1)
        vport[portName] = portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=portName)
        portMap.Connect(forceTakePortOwnership)

    ixNetwork.info('Creating Topology - L3VPN Topology 1')

    topology1 = ixNetwork.Topology.add(Name='L3VPN Topology 1', Ports=vport['Port_1'])
    p1Dg1 = topology1.DeviceGroup.add(Name='P_Rorter_1', Multiplier='1')
    ethernet1 = p1Dg1.Ethernet.add(Name='Ethernet_P1')
    ethernet1.Mac.Increment(start_value='00:ca:ff:ee:00:01', step_value='00:00:00:00:00:00')
    ethernet1.EnableVlans.Single(False)

    ixNetwork.info('Configuring IPv4 Interface')
    ipv4 = ethernet1.Ipv4.add(Name='Ipv4_P1')
    ipv4.Address.Increment(start_value='100.1.0.1', step_value='0.0.0.0')
    ipv4.GatewayIp.Increment(start_value='100.1.0.2', step_value='0.0.0.0')

    ixNetwork.info('Configuring Ldp prrotocol on P Router 1')
    p1ldp = ipv4.LdpBasicRouter.add(Name='LDP_P1')

    if igp.lower() == 'ospf':
        ixNetwork.info('Configuring Ospf Router on P Router 1')
        p1Ospf = ipv4.Ospfv2.add(Name='IGP_OSPF_P1')
        p1Ospf.NeighborIp.Increment(start_value='100.1.0.2', step_value='0.0.0.1')
        p1Ospf.NetworkType.Single('pointtopoint')

    elif igp.lower() == 'isis':
        ixNetwork.info('Configuring Isis Router on P Router 1')
        p1Isis = ethernet1.IsisL3.add(Name='IGP_ISIS_P1')
        p1Isis.NetworkType.Single('pointpoint')
        p1Isis.LevelType.Single('level2')
        isisl3router = p1Dg1.IsisL3Router.find(Name='ISIS-L3 RTR.*')
        isisl3router.EnableWideMetric.Single(True)

    ixNetwork.info('Configuring P1-PE1 Nework')
    networkGroup1 = p1Dg1.NetworkGroup.add(Name='P1-PE1 Network', Multiplier='1')
    ipv4PrefixPool = networkGroup1.Ipv4PrefixPools.add(NumberOfAddresses='1')
    ipv4PrefixPool.NetworkAddress.Increment(start_value='1.1.1.1', step_value='0.0.0.1')
    ipv4PrefixPool.PrefixLength.Single(32)

    pe1DevGroup1 = networkGroup1.DeviceGroup.add(Name='PE1', Multiplier='1')
    pe1LoopBackv4 = pe1DevGroup1.Ipv4Loopback.add(Name='PE1 loopback')
    pe1LoopBackv4.Address.Increment(start_value='1.1.1.1', step_value='0.0.0.1')

    pe1Bgp = pe1LoopBackv4.BgpIpv4Peer.add(Name='BGP_PE1')
    pe1Bgp.update(EthernetSegmentsCountV4=2)
    pe1Bgp.DutIp.Increment(start_value='2.2.2.2', step_value='0.0.0.1')
    pe1Bgp.Type.Single('internal')
    pe1Bgp.LocalAs2Bytes.Increment(start_value=15169, step_value=0)
    pe1Bgp.BgpId.Increment(start_value='1.1.1.1', step_value='0.0.0.1')

    # Turning on of Leraned Info in order to create Traffic Item with learned source and destination

    pe1Bgp.FilterIpV4MplsVpn.Single(True)

    pe1BgpVrf1 = pe1Bgp.BgpVrf.add(Name='PE1_BGP_VRF')

    routeRange1 = pe1DevGroup1.NetworkGroup.add(Multiplier='1' , Name='VRF_1')
    vrf1 = routeRange1.Ipv4PrefixPools.add(NumberOfAddresses=5)
    vrf1.NetworkAddress.Increment(start_value='13.13.13.1' , step_value='0.0.0.1')
    vrf1.BgpL3VpnRouteProperty.find().LabelStart.Increment(start_value='4000',step_value='45')

    ixNetwork.info('Creating Topology - L3VPN Topology 2')
    topology2 = ixNetwork.Topology.add(Name='L3VPN Topology 2', Ports=vport['Port_2'])
    p2Dg1 = topology2.DeviceGroup.add(Name='P_Rorter_2', Multiplier='1')
    ethernet2 = p2Dg1.Ethernet.add(Name='Ethernet_P2')
    ethernet2.Mac.Increment(start_value='00:ca:ff:ff:00:01', step_value='00:00:00:00:00:00')
    ethernet2.EnableVlans.Single(False)

    ixNetwork.info('Configuring IPv4 Interface')
    p2Ipv4 = ethernet2.Ipv4.add(Name='Ipv4_P2')
    p2Ipv4.Address.Increment(start_value='100.1.0.2', step_value='0.0.0.0')
    p2Ipv4.GatewayIp.Increment(start_value='100.1.0.1', step_value='0.0.0.0')

    ixNetwork.info('Configuring Ldp prrotocol on P Router 2')
    p2ldp = p2Ipv4.LdpBasicRouter.add(Name='LDP_P2')

    if igp.lower() == 'ospf':
        ixNetwork.info('Configuring Ospf on P Router 2')
        p2Ospf = p2Ipv4.Ospfv2.add(Name='IGP_OSPF_P2')
        p2Ospf.NeighborIp.Increment(start_value='100.1.0.1', step_value='0.0.0.1')
        p2Ospf.NetworkType.Single('pointtopoint')

    elif igp.lower() == 'isis':
        ixNetwork.info('Configuring Isis Router on P2')
        p2Isis = ethernet2.IsisL3.add(Name='IGP_ISIS_P2')
        p2Isis.NetworkType.Single('pointpoint')
        p2Isis.LevelType.Single('level2')
        p2isisl3router = p2Dg1.IsisL3Router.find(Name='ISIS-L3 RTR.*')
        p2isisl3router.EnableWideMetric.Single(True)

    ixNetwork.info('Configuring P2-PE2 Network')
    networkGroup2 = p2Dg1.NetworkGroup.add(Name='P2-PE2 Network', Multiplier='1')
    p2ipv4PrefixPool = networkGroup2.Ipv4PrefixPools.add(NumberOfAddresses='1')
    p2ipv4PrefixPool.NetworkAddress.Increment(start_value='2.2.2.2', step_value='0.0.0.1')
    p2ipv4PrefixPool.PrefixLength.Single(32)

    pe2DevGroup1 = networkGroup2.DeviceGroup.add(Name='PE2', Multiplier='1')
    pe2LoopBackv4 = pe2DevGroup1.Ipv4Loopback.add(Name='PE2_loopback')
    pe2LoopBackv4.Address.Increment(start_value='2.2.2.2', step_value='0.0.0.1')

    pe2Bgp = pe2LoopBackv4.BgpIpv4Peer.add(Name='BGP_PE2')
    pe2Bgp.update(EthernetSegmentsCountV4=2)
    pe2Bgp.DutIp.Increment(start_value='1.1.1.1', step_value='0.0.0.1')
    pe2Bgp.Type.Single('internal')
    pe2Bgp.LocalAs2Bytes.Increment(start_value=15169, step_value=0)
    pe2Bgp.BgpId.Increment(start_value='2.2.2.2', step_value='0.0.0.1')

    # Turning on of Leraned Info in order to create Traffic Item with learned source and destination
    pe2Bgp.FilterIpV4MplsVpn.Single(True)

    pe2BgpVrf1 = pe2Bgp.BgpVrf.add(Name='PE2_BGP_VRF')

    routeRange2 = pe2DevGroup1.NetworkGroup.add(Multiplier='1' , Name='VRF_2')
    vrf2 = routeRange2.Ipv4PrefixPools.add(NumberOfAddresses='10')
    vrf2.NetworkAddress.Increment(start_value='23.23.23.1', step_value='0.0.0.1')

    # Modifying VPN Routes Lables
    vrf2.BgpL3VpnRouteProperty.find().LabelStart.Increment(start_value='444', step_value='5')

    # Starting all protocol
    ixNetwork.StartAllProtocols(Arg1='sync')

    # Getting protocol stats
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    protocolSummary.AddRowFilter('Protocol Type', protocolSummary.REGEX, '(?i)^BGP?')
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.GREATER_THAN_OR_EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
    ixNetwork.info(protocolSummary)

    # Traffic Creation
    ixNetwork.info('Traffic Item Creation between two VRF')
    trafficVrf1ToVrf2 = ixNetwork.Traffic.TrafficItem.add(Name='VRF1 to VRF2', BiDirectional=False, TrafficType='ipv4')

    ixNetwork.info('Traffic Item endpoint Source - VRF of PE1 and Destination - VRF of PE2')

    trafficVrf1ToVrf2.EndpointSet.add(Sources=vrf1 , Destinations=vrf2)
    configElement = trafficVrf1ToVrf2.ConfigElement.find()[0]

    configElement.FrameRate.update(Type='percentLineRate', Rate=50)
    configElement.TransmissionControl.update(Type='fixedFrameCount', FrameCount=1000)
    configElement.FrameRateDistribution.PortDistribution = 'splitRateEvenly'
    configElement.FrameSize.FixedSize = 120

    #Enable tracking of traffic
    trafficVrf1ToVrf2.Tracking.find()[0].TrackBy = ['flowGroup0']

    trafficVrf1ToVrf2.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()

    # Traffic Statistics
    trafficItemStatistics = session.StatViewAssistant('Traffic Item Statistics')
    ixNetwork.info('{}\n'.format(trafficItemStatistics))
    flowStatistics = session.StatViewAssistant('Flow Statistics')
    flowStatistics.AddRowFilter('Traffic Item', flowStatistics.REGEX, '^vrf1.*')
    flowStatistics.AddRowFilter('Tx Frames', flowStatistics.EQUAL, 1000)
    flowStatistics.AddRowFilter('Rx Frames', flowStatistics.GREATER_THAN_OR_EQUAL, 98000)

    ixNetwork.info('{}\n'.format(flowStatistics))

    ixNetwork.info('Stop traffic')
    ixNetwork.Traffic.StopStatelessTrafficBlocking()

    ixNetwork.info('Stop All Protocols')
    ixNetwork.StopAllProtocols(Arg1='sync')

except Exception as errMsg:
    print(traceback.print_exception())
    if 'session' in locals():
        session.Session.remove()

