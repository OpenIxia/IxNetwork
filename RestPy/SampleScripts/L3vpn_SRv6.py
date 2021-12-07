"""
L3vpn SRv6:

   This script intends to demonstrate how to use NGPF BGP API to configure

    1. It will create a BGP topology with LDP & OSPF configured in Provider
        Router.
    2. In Provider Edge Router configuration 2 BGP Peer are configured.
       - iBGP Peer
       - eBGP Peer to configure Multi Hop BGP session.
    3. Only one side configuration is provided.
    4. Traffic configuration will be similar to L3VPN scenario.

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
       raise BadRequestError(message, response.status_code)
       ixnetwork_restpy.errors.BadRequestError:  Error in L2/L3 Traffic Apply

        Current Server Errors/Warnings:
        10/04/2021 20:07:06 [WARNING] [No Flow Groups Created] The Traffic Item was not generated properly and no Flow Groups were created. Please regenerate the Traffic Item to see all the pending errors and fix them before Applying the Traffic
            
"""

import sys, os, time, traceback

# Import the Restpy module
from ixnetwork_restpy import SessionAssistant

apiServerIp = '10.39.34.74'

ixChassisIpList = ['10.39.44.162']
portList = [[ixChassisIpList[0], 2,1], [ixChassisIpList[0], 2, 2]]

# For Linux API server only
username = 'admin'
password = 'admin'

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = False

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True
 
try:
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=11339 ,SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel='all', LogFilename='restpy.log')

    ixNetwork = session.Ixnetwork

    portMap = session.PortMapAssistant()
    vport = dict()

    ixNetwork.info('Adding 2 Vports')
    for index,port in enumerate(portList):
        portName = 'Port_{}'.format(index+1)
        vport[portName] = portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=portName)
        portMap.Connect(forceTakePortOwnership)

    ixNetwork.info('Adding 2 Topologies')
    topology1 = ixNetwork.Topology.add(Name='Egress Topology: Sender', Ports=vport['Port_1'])
    topology2 = ixNetwork.Topology.add(Name='Ingress Topology: Receiver', Ports=vport['Port_2'])

    ixNetwork.info('Adding 2 Device Groups')
    t1device1 = topology1.DeviceGroup.add(Name='Sender PE Router', Multiplier='1')
    t2device1 = topology2.DeviceGroup.add(Name='Receiver PE Router', Multiplier='1')

    ixNetwork.info('Adding Ethernet/Mac Endpoints')
    ethernet1 = t1device1.Ethernet.add(Name='Ethernet 1')
    ixNetwork.info('Configuring the MAC Addresses')
    ethernet1.Mac.Increment(start_value='00:11:01:00:00:01', step_value='00:00:00:00:00:01')
    ethernet1.EnableVlans.Single(False)

    ethernet2 = t2device1.Ethernet.add(Name='Ethernet 1')
    ixNetwork.info('Configuring the MAC Addresses')
    ethernet2.Mac.Increment(start_value='00:12:01:00:00:01', step_value='00:00:00:00:00:01')
    ethernet2.EnableVlans.Single(False)

    ixNetwork.info('Add IPv6')
    ip1 = ethernet1.Ipv6.add(Name='Ipv6 1')
    ixNetwork.info('Configuring IPv6 addresses')
    ip1.Address.Increment(start_value='2000:0:0:1:0:0:0:1', step_value='0::1')
    ip1.GatewayIp.Increment(start_value='2000:0:0:1:0:0:0:2', step_value='0::1')
    ip1.Prefix.Single(64)

    ip2 = ethernet2.Ipv6.add(Name='Ipv6 2')
    ip2.Address.Increment(start_value='2000:0:0:1:0:0:0:2', step_value='0::1')
    ip2.GatewayIp.Increment(start_value='2000:0:0:1:0:0:0:1', step_value='0::1')
    ip2.Prefix.Single(64)

    ixNetwork.info('Adding ISIS-L3 Over IPv6 Stacks')
    isis1 = ethernet1.IsisL3.add()
    isis2 = ethernet2.IsisL3.add()

    ixNetwork.info('Renaming the Topologies and Device Groups')
    topology1.Name = 'isisL3 Topology 1'
    topology2.Name = 'isisL3 Topology 2'
    t1device1.Name = 'isisL3 Topology 1 Router'
    t2device1.Name = 'isisL3 Topology 2 Router'

    ixNetwork.info('Change the Property of ISIS-L3')
    isis1.NetworkType.Single('pointpoint')
    isis1.LevelType.Single('level2')
    isis1router = t1device1.IsisL3Router.find()
    isis1router.EnableWideMetric.Single(True)
    isis2.NetworkType.Single('pointpoint')
    isis2.LevelType.Single('level2')
    isis2router = t2device1.IsisL3Router.find()
    isis2router.EnableWideMetric.Single(True)

    ixNetwork.info('Change the value F Flag')
    isis1.FFlag.Single(True)
    isis2.FFlag.Single(True)

    ixNetwork.info('Change the Value enableIpv6SID')
    isis1.EnableIPv6SID.Single(True)
    isis2.EnableIPv6SID.Single(True)

    ixNetwork.info('Change the Value ipv6SidValue')
    isis1.Ipv6SidValue.Single('3333::1')
    isis2.Ipv6SidValue.Single('4444::1')

    ixNetwork.info('Change the value srv6SidFlags')
    isis1.Srv6SidFlags.Single('cd')
    isis2.Srv6SidFlags.Single('ef')

    ixNetwork.info('Change the value discardLSPs')
    isis1router.DiscardLSPs.Single(False)
    isis2router.DiscardLSPs.Single(False)

    ixNetwork.info('Enable Segment Routing')
    isis1.EnableSRLG.Single(True)
    isis2.EnableSRLG.Single(True)

    ixNetwork.info('Enable the S bit and D bit')
    isis1router.SBit.Single(True)
    isis2router.SBit.Single(True)
    isis1router.DBit.Single(True)
    isis2router.DBit.Single(True)

    ixNetwork.info('Enable the ipv4/ipv6 Flag')
    isis1router.Ipv4Flag.Single(True)
    isis2router.Ipv4Flag.Single(True)
    isis1router.Ipv6Flag.Single(True)
    isis2router.Ipv6Flag.Single(True)

    ixNetwork.info('Enabling the configureSIDIndexLabel')
    isis1router.ConfigureSIDIndexLabel.Single(True)
    isis2router.ConfigureSIDIndexLabel.Single(True)

    ixNetwork.info('Enabling the ipv6Srh means Enable SR-IPv6')
    isis1router.Ipv6Srh.Single(True)
    isis2router.Ipv6Srh.Single(True)

    ixNetwork.info('Enabling the oFlagOfSrv6CapTLV')
    isis1router.OFlagOfSRv6CapTlv.Single(True)
    isis2router.OFlagOfSRv6CapTlv.Single(True)

    ixNetwork.info('Enabling the eFlagOfSrv6CapTLV')
    isis1router.EFlagOfSRv6CapTlv.Single(True)
    isis2router.EFlagOfSRv6CapTlv.Single(True)

    ixNetwork.info('Enabling the sBitForSRv6Cap')
    isis1router.SBitForSRv6Cap.Single(True)
    isis2router.SBitForSRv6Cap.Single(True)

    ixNetwork.info('Enabling the dBitForSRv6Cap')
    isis1router.DBitForSRv6Cap.Single(True)
    isis2router.DBitForSRv6Cap.Single(True)

    ixNetwork.info('Enabling the reservedInsideSRv6CapFlag')
    isis1router.ReservedInsideSRv6CapFlag.Single('3fff')
    isis2router.ReservedInsideSRv6CapFlag.Single('2fff')

    ixNetwork.info('Enabling the includeMaximumEndDSrhTLV')
    isis1router.IncludeMaximumEndDSrhTLV.Single(True)
    isis2router.IncludeMaximumEndDSrhTLV.Single(True)

    ixNetwork.info('Enabling the includeMaximumEndPopTLV')
    isis1router.IncludeMaximumEndPopSrhTLV.Single(True)
    isis2router.IncludeMaximumEndPopSrhTLV.Single(True)

    ixNetwork.info('Enabling the includeMaximumSLVTLV')
    isis1router.IncludeMaximumSLTLV.Single(True)
    isis2router.IncludeMaximumSLTLV.Single(True)

    ixNetwork.info('Enabling the includeMaximumTEncapSrhTLV')
    isis1router.IncludeMaximumTEncapSrhTLV.Single(True)
    isis2router.IncludeMaximumTEncapSrhTLV.Single(True)

    ixNetwork.info('Enabling the includeMaximumTInsertSrhTLV')
    isis1router.IncludeMaximumTInsertSrhTLV.Single(True)
    isis2router.IncludeMaximumTInsertSrhTLV.Single(True)

    ixNetwork.info('Enabling the dBitForSRv6Cap')
    isis1router.DBitInsideSRv6SidTLV.Single(True)
    isis2router.DBitInsideSRv6SidTLV.Single(True)

    ixNetwork.info('Add Network Group')
    networkGroup1=t1device1.NetworkGroup.add(Name='IPv6_LoopBack_Address')
    ipv6PrefixPool = networkGroup1.Ipv6PrefixPools.add(NumberOfAddresses='1')
    ipv6PrefixPool.NetworkAddress.Increment(start_value='1111::1', step_value='0::1')
    ipv6PrefixPool.PrefixLength.Single(64)

    ixNetwork.info('Create Network Group At PEER2 Side')
    networkGroup2 = t2device1.NetworkGroup.add(Name='Routers')
    networkTopo1 = networkGroup2.NetworkTopology.add()

    simInterface = networkTopo1.SimInterface.find()
    simInterface.Name = 'Simulated Interfaces 1'

    netTopoCustom = networkTopo1.NetTopologyCustom.add(IncludeEntryPoint=None, LinkMultiplier=None)
    netTopoCustom.LinkTable.FromNodeIndex = ['5', '5', '1', '1', '6', '6', '2', '2', '9', '9', '9', '9']
    netTopoCustom.LinkTable.ToNodeIndex = ['3', '7', '0', '3', '4', '8', '0', '4', '1', '5', '2', '6']

    simIntIPv4 = simInterface.SimInterfaceIPv4Config.find()
    simIntIPv4.Name='Simulated Link IPv4 Address 1'

    ixNetwork.info('Enable the F Flag of SR-MPLS of Network Topology')
    fFlag1 = simInterface.IsisL3PseudoInterface.find()
    fFlag1.FFlag.Single(True)

    ixNetwork.info('Enable the WideMetric of SR-MPLS of Simulated Interfaces of Network Topology')
    simRouter = networkTopo1.SimRouter.find()
    simRouterIsisL3 = simRouter.IsisL3PseudoRouter.find()
    simRouterIsisL3.EnableWideMetric.Single(True)

    ixNetwork.info('Enable the enableSR/IPv4/IPv6/ConfigureSIDIndexLabel if Simulated Bridge of Network Topology')
    simRouterIsisL3.Ipv4Flag.Single(True)
    simRouterIsisL3.Ipv6Flag.Single(True)
    simRouterIsisL3.ConfigureSIDIndexLabel.Single(True)

    ixNetwork.info('The Value for the IPv6 Node SID')
    simRouterIsisL3.Ipv6NodePrefix.Increment(start_value='7001::1', step_value='1::')

    ixNetwork.info('Enable the Field of SR-IPv6')
    simRouterIsisL3.Ipv6Srh.Single(True)

    ixNetwork.info('Change the Network Address of ISIS Simulated IPv6 Node Routers of Simulated Bridge')
    simRouterIsisL3.IPv6PseudoNodeRoutes.find().NetworkAddress.Single('2222::1')

    ixNetwork.info('Add Device Group Behind IPv6 Network Group')
    deviceGroupBgp = networkGroup1.DeviceGroup.add(Name='BGP_L3vpn_1', Multiplier='1')
    ipv6Loopback = deviceGroupBgp.Ipv6Loopback.add(Name='IPv6 Loopback 1')

    ipv6Loopback.Address.Increment(start_value='1111::1', step_value='0::1')
    ipv6Loopback.Prefix.Single(128)

    bgpIpv6Peer1 = ipv6Loopback.BgpIpv6Peer.add(Name='BGP6Peer2')
    bgpIpv6Peer1.NumberSRTEPolicies = 2
    bgpIpv6Peer1.EnSRv6DataPlane=True
    bgpIpv6Peer1.StackedLayers=[]
    bgpIpv6Peer1.DutIp.Increment(start_value='2222::1', step_value='0::1')
    bgpIpv6Peer1.FilterSRTEPoliciesV4.Single(True)
    bgpIpv6Peer1.FilterSRTEPoliciesV6.Single(True)
    bgpIpv6Peer1.FilterIpV4MplsVpn.Single(True)
    bgpIpv6Peer1.CapabilitySRTEPoliciesV4.Single(True)
    bgpIpv6Peer1.CapabilitySRTEPoliciesV6.Single(True)
    bgpIpv6Peer1.CapabilityNHEncodingCapabilities.Single(True)

    ixNetwork.info('Configuring the SRTE Policy Properties: BGP SRTE Policy Tab')
    bgpIpv6Peer1.BgpSRTEPoliciesListV6.PolicyType.Single('ipv6')
    bgpIpv6Peer1.BgpSRTEPoliciesListV6.EndPointV6.Single('2222::1')
    #bgpIpv6Peer1.BgpSRTEPoliciesListV6.BgpSRTEPoliciesTunnelEncapsulationListV6.BgpSRTEPoliciesSegmentListV6.NumberOfSegmentsV6=6
    #bgpIpv6Peer1.BgpSRTEPoliciesListV6.BgpSRTEPoliciesTunnelEncapsulationListV6.BgpSRTEPoliciesSegmentListV6.BgpSRTEPoliciesSegmentsCollectionV6.SegmentType.Single('ipv6sid')
    #bgpIpv6Peer1.BgpSRTEPoliciesListV6.BgpSRTEPoliciesTunnelEncapsulationListV6.BgpSRTEPoliciesSegmentListV6.BgpSRTEPoliciesSegmentsCollectionV6.Ipv6SID.Single('6666::1')

    ixNetwork.info('Adding BGPVRF on top of BGPv6')
    bgpV6Vrf1=bgpIpv6Peer1.BgpV6Vrf.add(Name='BGP6VRF2', Multiplier=1)
    bgpExportRoute = bgpV6Vrf1.BgpExportRouteTargetList.find()
    bgpExportRoute.TargetAsNumber.Increment(start_value='100', step_value=1)

    ixNetwork.info('Adding Network Group Behind BGPv6')
    networkGroup = deviceGroupBgp.NetworkGroup.add(Name='IPv4_VPN_Route')
    ipv4PrefixPool = networkGroup.Ipv4PrefixPools.add(NumberOfAddresses=1)

    ipv4PrefixPool.NetworkAddress.Increment(start_value='1.1.1.1' , step_value='0.1.0.0')
    bgpV6L3VpnRoute = ipv4PrefixPool.BgpV6L3VpnRouteProperty.find()
    bgpV6L3VpnRoute.LabelStep.Single(1)
    bgpV6L3VpnRoute.EnableSrv6Sid.Single(True)
    bgpV6L3VpnRoute.Srv6SidLoc.Increment(start_value='a1::d100', step_value='1::1')

    ixNetwork.info('Configure BGP/BGP-Vrf at PEER2 Side')
    deviceGroupBgp2 = networkGroup2.DeviceGroup.add(Name='BGP_L3vpn_2',Multiplier=1)
    ipv6Loopback2 = deviceGroupBgp2.Ipv6Loopback.add(Name='IPv6Loopback1')
    ipv6Loopback2.Address.Increment(start_value='2222::1', step_value='0::1')

    ixNetwork.info('Adding BGPv6 Peer on top of IPv6Loopback')
    bgpIpv6Peer2 = ipv6Loopback2.BgpIpv6Peer.add(Name='BGP6Peer1')
    bgpIpv6Peer2.DutIp.Increment(start_value='1111::1', step_value='0::1')
    bgpIpv6Peer2.FilterSRTEPoliciesV4.Single(True)
    bgpIpv6Peer2.FilterSRTEPoliciesV6.Single(True)
    bgpIpv6Peer2.FilterIpV4MplsVpn.Single(True)
    bgpIpv6Peer2.CapabilitySRTEPoliciesV4.Single(True)
    bgpIpv6Peer2.CapabilitySRTEPoliciesV6.Single(True)
    bgpIpv6Peer2.CapabilityNHEncodingCapabilities.Single(True)

    ixNetwork.info('Adding BGP6VRF on top of BGP6 Peer2 Side')
    bgpV6Vrf2=bgpIpv6Peer2.BgpV6Vrf.add(Name='BGP6VRF1', Multiplier=1)
    bgpExportRoute = bgpV6Vrf2.BgpExportRouteTargetList.find()
    bgpExportRoute.TargetAsNumber.Increment(start_value='100', step_value=1)

    ixNetwork.info('Adding Network Group Behind BGP6 At Peer2 Side')
    networkGroupP2 = deviceGroupBgp2.NetworkGroup.add(Name='IPv4_VPN_Route_2')
    ipv4PrefixPoolP2 = networkGroupP2.Ipv4PrefixPools.add()

    ipv4PrefixPoolP2.NetworkAddress.Increment(start_value='2.2.2.2', step_value='0.1.0.0')
    bgpV6L3RoutePropertyP2 = ipv4PrefixPoolP2.BgpV6L3VpnRouteProperty.find()
    bgpV6L3RoutePropertyP2.LabelStep.Single(1)
    bgpV6L3RoutePropertyP2.EnableSrv6Sid.Single(True)
    bgpV6L3RoutePropertyP2.Srv6SidLoc.Increment(start_value='a1::d100', step_value='1::1')
    bgpV6L3RoutePropertyP2.EnableExtendedCommunity.Single(True)
    bgpv6ExtendedCommunities = bgpV6L3RoutePropertyP2.BgpExtendedCommunitiesList.find()
    bgpv6ExtendedCommunities.ColorValue.Increment(start_value=100, step_value=1)
    bgpv6ExtendedCommunities.SubType.Single('color')
    bgpv6ExtendedCommunities.Type.Single('opaque')

    ixNetwork.info('Starting Protocols and waiting for 20 seconds for protocols to come up')
    ixNetwork.StartAllProtocols(Arg1='sync')
    time.sleep(20)

    ixNetwork.info('Fetching all Protocol Summary Stats')
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.GREATER_THAN_OR_EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
    ixNetwork.info(protocolSummary)

    ixNetwork.info('Configuring L2-L3 Traffic Items')
    ixNetwork.Globals.Interfaces.ArpOnLinkup = True
    ixNetwork.Globals.Interfaces.NsOnLinkup = True
    ixNetwork.Globals.Interfaces.SendSingleArpPerGateway = True
    ixNetwork.Globals.Interfaces.SendSingleNsPerGateway = True

    ixNetwork.Traffic.CycleTimeUnitForScheduledStart = 'milliseconds'
    ixNetwork.Traffic.RefreshLearnedInfoBeforeApply = True
    ixNetwork.Traffic.DetectMisdirectedOnAllPorts = False
    ixNetwork.Traffic.UseRfc5952 = True
    ixNetwork.Traffic.CycleOffsetUnitForScheduledStart = 'nanoseconds'
    ixNetwork.Traffic.CycleTimeUnitForScheduledStart = 'nanoseconds'
    ixNetwork.Traffic.CycleTimeForScheduledStart = '1'
    ixNetwork.Traffic.EnableLagFlowBalancing = True
    ixNetwork.Traffic.PeakLoadingReplicationCount = '1'

    ixNetwork.Traffic.Statistics.MisdirectedPerFlow.Enabled = False
    ixNetwork.Traffic.Statistics.MultipleJoinLeaveLatency.Enabled = False
    ixNetwork.Traffic.Statistics.OneTimeJoinLeaveLatency.Enabled = False

    trafficTopo1ToTopo2 = ixNetwork.Traffic.TrafficItem.add(Name='Top1-To-Top2',MulticastForwardingMode='replication',
                        UseControlPlaneRate=True, UseControlPlaneFrameSize=True, RoundRobinPacketOrdering=False,
                        NumVlansForMulticastReplication='1', TrafficType='ipv4')

    trafficTopo1ToTopo2.EndpointSet.add(Name="EndpointSet-1", MulticastDestinations=[], ScalableSources=[],
                                        MulticastReceivers=[],ScalableDestinations=[],NgpfFilters=[], TrafficGroups=[],
                                        Sources=topology1, Destinations=deviceGroupBgp2)

    trafficTopo1ToTopo2.Tracking.find().TrackBy = ['ipv4SourceIp0', 'trackingenabled0']
    trafficTopo1ToTopo2.Tracking.find().FieldWidth = "thirtyTwoBits"
    trafficTopo1ToTopo2.Tracking.find().ProtocolOffset = "Root.0"
    trafficTopo1ToTopo2.Tracking.find().LatencyBin.BinLimits = ['1', '1.42', '2', '2.82', '4', '5.66',
                                                                '8', '2147483647']

    ixNetwork.info('applying and starting L2/L3 traffic')
    trafficTopo1ToTopo2.Generate()
    ixNetwork.Traffic.Apply()

    ixNetwork.Traffic.Start()
    ixNetwork.info("Traffic runs for 20 seconds")
    time.sleep(20)

    ixNetwork.info('Traffic Statistics')
    trafficItemStatistics = session.StatViewAssistant('Traffic Item Statistics')
    ixNetwork.info('{}\n'.format(trafficItemStatistics))
    flowStatistics = session.StatViewAssistant('Flow Statistics')
    ixNetwork.info('{}\n'.format(flowStatistics))

    ixNetwork.info('Stopping L2/L3 Traffic')
    ixNetwork.Traffic.Stop()
    #time.sleep(5)

    ixNetwork.info('Stopping Protocols')
    ixNetwork.StopAllProtocols()

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
