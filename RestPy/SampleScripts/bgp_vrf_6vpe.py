"""
bgp_vrf_6vpe.py:

Tested with two back-2-back IxNetwork ports.
   - Connect to the API server
   - Assign ports
   - Physical topology:  Port1 ----- Port2
   - Configure two Topology Groups: IPv6/Routes-VRF1 ---- PE1 ---- P1----- P2 ---- PE2 ---- VRF2-IPv6/Routes
   - Between P1 and P2 when can set OSPF or ISIS to advertize PE's loopbacks
   - Singalling between PE Routers - RSVP-TE
   - Configure Network Group for each topology for IPv6 vpn route advertising
   - Start all protocols
   - Verify all protocols has up
   - Configure a Traffic Item from VRF1 to VRF2 - 1000 packets
   - Start traffic
   - Get/Show Traffic Item Statistics
   - Get/Show Flow Statistics stats
   
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
   
Error:
        10/04/2021 20:23:11 [WARNING] [Transmit Rate for IxVM] When IxVM ports are used, traffic transmit rate may be lower than expected due to underlying hardware or hypervisor capabilities. In this case, if the Flow Group Transmission Mode for the Traffic Item is configured as Fixed Packet Count, Fixed iteration or Fixed Duration, then the transmit duration for that Traffic Item might be increased.
        10/04/2021 20:23:11 [WARNING] [No Valid Packets] There are no packets to be applied to hardware. This happens when no packets were generated due to destination MACs or VPNs being invalid or unreachable
        10/04/2021 20:23:11 [ERROR] [No Flow Groups] Cannot apply traffic because there are no flow groups after removing failed destination MAC addresses.

   
"""

import sys, os, time, traceback

from ixnetwork_restpy import SessionAssistant

apiServerIp = '172.16.101.3'

ixChassisIpList = ['172.16.102.5']
portList = [[ixChassisIpList[0], 1,1], [ixChassisIpList[0], 1, 2]]

# For Linux API server only
username = 'admin'
password = 'admin'

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = False

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True

# igp between P-P either ospf or isis
igp ='ospf'

try:
    # LogLevel: none, info, warning, request, request_response, all
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=None, UserName='admin', Password='admin', 
                               SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel='all', LogFilename='restpy.log')

    ixNetwork = session.Ixnetwork

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

    ixNetwork.info('Configuring RSVP protocol on P Router 1')
    p1Rsvp = ipv4.RsvpteIf.add(Name='RSVPTE-IF_P1')

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

    ixNetwork.info('Configuring PE1 Router')

    pe1DevGroup1 = networkGroup1.DeviceGroup.add(Name='PE1', Multiplier='1')
    pe1LoopBackv4 = pe1DevGroup1.Ipv4Loopback.add(Name='PE1 loopback')
    pe1LoopBackv4.Address.Increment(start_value='1.1.1.1', step_value='0.0.0.1')

    # Rsvp TE Configuration on PE1 and RSVP TE P to P Tunnel Local and Remote
    pe1Rsvp = pe1LoopBackv4.RsvpteLsps.add(Name='RSVPTE_PE1')
    pe1Rsvp.RsvpP2PIngressLsps.RemoteIp.Increment(start_value='2.2.2.2', step_value='0.0.0.1')

    pe1Bgp = pe1LoopBackv4.BgpIpv4Peer.add(Name='BGP_PE1')
    pe1Bgp.update(EthernetSegmentsCountV4=2)
    pe1Bgp.DutIp.Increment(start_value='2.2.2.2', step_value='0.0.0.1')
    pe1Bgp.Type.Single('internal')
    pe1Bgp.LocalAs2Bytes.Increment(start_value=15169, step_value=0)
    pe1Bgp.BgpId.Increment(start_value='1.1.1.1', step_value='0.0.0.1')

    # Turning on of Leraned Info in order to create Traffic Item with learned source and destination

    pe1Bgp.FilterIpV4MplsVpn.Single(True)
    pe1Bgp.FilterIpV6MplsVpn.Single(True)

    pe1BgpVrf1 = pe1Bgp.BgpVrf.add(Name='PE1_BGP_VRF')

    # VPN Routes - IPv6 
    ixNetwork.info('Configuring IPv6 VPN Routes')
    routeRange1 = pe1DevGroup1.NetworkGroup.add(Multiplier='10' , Name='VRF_1')
    vrf1=routeRange1.Ipv6PrefixPools.add(NumberOfAddresses=5)
    vrf1.NetworkAddress.Increment(start_value='3ffe:1::1:100', step_value='0:0:0:1:0:0:0:0')

    # Modifying of IPv6 VPN Route Attributes
    ixNetwork.info('Modifying VPN v6 Route attributes :for Ex- Label')
    vrf1.BgpV6L3VpnRouteProperty.find().LabelStart.Increment(start_value='4000', step_value='50')


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

    ixNetwork.info('Configuring RSVP prrotocol on P Router 2')
    p2Rsvp=p2Ipv4.RsvpteIf.add(Name='RSVPTE-IF_P2')

    # Configuration of IGP in P Router

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

    ixNetwork.info('Configuring PE2 Router')

    pe2DevGroup1 = networkGroup2.DeviceGroup.add(Name='PE2', Multiplier='1')
    pe2LoopBackv4 = pe2DevGroup1.Ipv4Loopback.add(Name='PE2_loopback')
    pe2LoopBackv4.Address.Increment(start_value='2.2.2.2', step_value='0.0.0.1')

    # Rsvp TE Configuration ON PE2 and RSVP TE P to P Tunnel Local and Remote
    pe2Rsvp = pe2LoopBackv4.RsvpteLsps.add(Name='RSVPTE_PE2')
    pe2Rsvp.RsvpP2PIngressLsps.RemoteIp.Increment(start_value='1.1.1.1', step_value='0.0.0.1')

    pe2Bgp = pe2LoopBackv4.BgpIpv4Peer.add(Name='BGP_PE2')
    pe2Bgp.update(EthernetSegmentsCountV4=2)
    pe2Bgp.DutIp.Increment(start_value='1.1.1.1', step_value='0.0.0.1')
    pe2Bgp.Type.Single('internal')
    pe2Bgp.LocalAs2Bytes.Increment(start_value=15169, step_value=0)
    pe2Bgp.BgpId.Increment(start_value='2.2.2.2', step_value='0.0.0.1')


    # Turning on of Leraned Info in order to create Traffic Item with learned source and destination
    pe2Bgp.FilterIpV4MplsVpn.Single(True)
    pe2Bgp.FilterIpV6MplsVpn.Single(True)

    pe2BgpVrf1 = pe2Bgp.BgpVrf.add(Name='PE2_BGP_VRF')

    ixNetwork.info('Configuring IPv6 VPN Routes')
    routeRange2 = pe2DevGroup1.NetworkGroup.add(Multiplier='10' , Name='VRF_2')
    vrf2 = routeRange2.Ipv6PrefixPools.add(NumberOfAddresses=5)
    vrf2.NetworkAddress.Increment(start_value='3ffe:2::2:200', step_value='0:0:0:1:0:0:0:0')

    # Modifying of IPv6 VPN Route Attributes
    ixNetwork.info('Modifying VPN v6 Route attributes - for ex: Label')
    vrf2.BgpV6L3VpnRouteProperty.find().LabelStart.Increment(start_value='444', step_value='5')

    # Starting all protocol
    ixNetwork.StartAllProtocols(Arg1='sync')

    # Getting protocol stats
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.GREATER_THAN_OR_EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
    ixNetwork.info(protocolSummary)

    # Traffic Creation
    ixNetwork.info('IPv6 VPN Traffic Item from one VRF1 to another VRF2 ')
    trafficVrf1ToVrf2 = ixNetwork.Traffic.TrafficItem.add(Name='VRF1 to VRF2', BiDirectional=False, TrafficType='ipv6')

    ixNetwork.info('Traffic Item endpoint Source - VRF of PE1 and Destination - VRF of PE2')

    trafficVrf1ToVrf2.EndpointSet.add(Sources=vrf1 , Destinations=vrf2)
    configElement = trafficVrf1ToVrf2.ConfigElement.find()[0]

    configElement.FrameRate.update(Type='percentLineRate', Rate=50)
    configElement.TransmissionControl.update(Type='fixedFrameCount', FrameCount=1000)
    configElement.FrameRateDistribution.PortDistribution = 'splitRateEvenly'
    configElement.FrameSize.FixedSize = 120

    trafficVrf1ToVrf2.Tracking.find()[0].TrackBy = ['flowGroup0']

    trafficVrf1ToVrf2.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()

    # Traffic Statistics
    trafficItemStatistics = session.StatViewAssistant('Traffic Item Statistics')
    ixNetwork.info('{}\n'.format(trafficItemStatistics))

    ixNetwork.info('Stop traffic')
    ixNetwork.Traffic.StopStatelessTrafficBlocking()

    ixNetwork.StopAllProtocols(Arg1='sync')

    if debugMode == False:
        for vport in ixNetwork.Vport.find():
            vport.ReleasePort()
            
        # For linux and connection_manager only
        if session.TestPlatform.Platform != 'windows':
            session.Session.remove()
            
except Exception as errMsg:
    print('\n%s' % traceback.format_exc(None, errMsg))
    if debugMode == False and 'session' in locals():
        if session.TestPlatform.Platform != 'windows':
            session.Session.remove()
