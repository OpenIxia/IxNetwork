"""
Evpn_NGPF.py:
   Tested with two back-2-back Ixia ports and put variables for the VTEP scale (L2/L3 VNI, number of VTEPs, ETC)
   - Connect to the API server
   - Assign ports:
        - If variable forceTakePortOwnership is True, take over the ports if they're owned by another user.
        - If variable forceTakePortOwnership if False, abort test.
   - Configure two Topology Groups: IPv4/BGP/EVPN
   - Configure Network Group for each topology
   - Configure a Traffic Item
   - Start all protocols
   - Verify all protocols
   - Start traffic
   - Get Traffic Item
   - Get Flow Statistics stats
Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux
Requirements:
   - Minimum IxNetwork 8.52
   - Python 2.7 and 3+
   - pip install requests
   - pip install ixnetwork_restpy
RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy/#/
Usage:
   - Enter: python <script>
"""


import sys, os, time, traceback

from ixnetwork_restpy import SessionAssistant

apiServerIp = '192.168.186.131'

ixChassisIpList = ['192.168.186.129']
portList = [[ixChassisIpList[0], 1,1], [ixChassisIpList[0], 2, 1]]

# For Linux API server only
username = 'admin'
password = 'admin'


# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = True

forceTakePortOwnership = True


vtep_multiplier = '64'

l2_label_start_value = '1001'
l3_label_start_value = '1001001'

# evi_count has to be evenly divisable by l3_rt_count for the script to work.
evi_count = '128'
l3_rt_count = 8

l3_rt_repeat_value = (int(evi_count) / l3_rt_count)

try:
    # LogLevel: none, info, warning, request, request_response, all
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=None, UserName=username, Password=password,
                               SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel='info', LogFilename='restpy.log')

    ixNetwork = session.Ixnetwork
    
    ixNetwork.info('Assign ports')
    portMap = session.PortMapAssistant()
    vport = dict()
    for index,port in enumerate(portList):
        portName = 'Port_{}'.format(index+1)
        vport[portName] = portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=portName)

    portMap.Connect(forceTakePortOwnership)

    ixNetwork.info('Creating Topology Group 1')
    topology1 = ixNetwork.Topology.add(Name='Topo1', Ports=vport['Port_1'])
    deviceGroup1 = topology1.DeviceGroup.add(Name='DG1', Multiplier=vtep_multiplier)
    ethernet1 = deviceGroup1.Ethernet.add(Name='Eth1')
    ethernet1.Mac.Increment(start_value='00:01:01:01:00:01', step_value='00:00:00:00:00:01')
    # ethernet1.EnableVlans.Single(True)
    # ixNetwork.info('Configuring vlanID')
    # vlanObj = ethernet1.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)

    ixNetwork.info('Configuring IPv4')
    ipv4 = ethernet1.Ipv4.add(Name='Ipv4')
    ipv4.Address.Increment(start_value='10.1.1.1', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='10.1.2.1', step_value='0.0.0.1')

    ixNetwork.info('Configuring BgpIpv4Peer 1')
    bgp1 = ipv4.BgpIpv4Peer.add(Name='Bgp1')
    bgp1.DutIp.Increment(start_value='10.1.2.1', step_value='0.0.0.1')
    bgp1.Type.Single('internal')
    bgp1.LocalAs2Bytes.Increment(start_value=101, step_value=0)
    bgp1.AdvertiseEvpnRoutesForOtherVtep = 'True' 
    bgp1.FilterEvpn.Single(True)

    ixNetwork.info('Configuring EVPN 1')
    evpn1 = bgp1.BgpIPv4EvpnVXLAN.add(Name= 'EVPN_VXLAN_1')
    bgp1.BgpEthernetSegmentV4.EvisCount = evi_count
    bgp1.BgpEthernetSegmentV4.VtepIpv4Address.Increment(start_value='10.1.1.1', step_value='0.0.0.1')
    evpn1.NumBroadcastDomainV4 = '1' 
    evpn1.RdEvi.Custom(start_value='1', step_value='0',increments=[('1', l3_rt_count, [('0', l3_rt_repeat_value , [])])])
    evpn1.BgpL3VNIExportRouteTargetList.find()[0].TargetAssignedNumber.Custom(start_value=l3_label_start_value, step_value='0',increments=[('1', l3_rt_count, [('0', l3_rt_repeat_value , [])])])
    evpn1.BgpExportRouteTargetList.find()[0].TargetAssignedNumber.Custom(start_value=l2_label_start_value, step_value='0',increments=[('1', evi_count, [])])

    ixNetwork.info('Configuring Network Group 1')
    networkGroup1 = deviceGroup1.NetworkGroup.add(Name='BGP-Routes1', Multiplier='1')
    macPool = networkGroup1.MacPools.add(NumberOfAddresses='1')
    CMacProperties = macPool.CMacProperties.add()
    connectorMac= macPool.Connector.find()
    connectorMac.ConnectedTo='/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1/bgpIPv4EvpnVXLAN/1'
    ipv4PrefixPool = macPool.Ipv4PrefixPools.add(NumberOfAddresses='1')
    ipv4PrefixPool.NetworkAddress.Increment(start_value='20.20.0.1', step_value='0.0.1.0')
    ipv4PrefixPool.PrefixLength.Single(16)
    macPool.CMacProperties.find()[0].FirstLabelStart.Custom(start_value=l2_label_start_value, step_value='0',increments=[('1', evi_count, [])])
    macPool.CMacProperties.find()[0].EnableSecondLabel.Single (True)
    macPool.CMacProperties.find()[0].SecondLabelStart.Custom(start_value=l3_label_start_value, step_value='0',increments=[('1', l3_rt_count, [('0', l3_rt_repeat_value , [])])])
    macPool.CMacProperties.find()[0].AdvertiseIpv4Address.Single (True)
    macPool.CMacProperties.find()[0].Ipv4AddressPrefixLength.Single(32)

    ixNetwork.info('Creating Topology Group 2')
    topology2 = ixNetwork.Topology.add(Name='Topo2', Ports=vport['Port_2'])
    deviceGroup2 = topology2.DeviceGroup.add(Name='DG2', Multiplier=vtep_multiplier)

    ethernet2 = deviceGroup2.Ethernet.add(Name='Eth2')
    ethernet2.Mac.Increment(start_value='00:01:01:02:00:01', step_value='00:00:00:00:00:01')
    # ethernet2.EnableVlans.Single(True)
    # ixNetwork.info('Configuring vlanID')
    # vlanObj = ethernet2.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)

    ixNetwork.info('Configuring IPv4 2')
    ipv4 = ethernet2.Ipv4.add(Name='Ipv4-2')
    ipv4.Address.Increment(start_value='10.1.2.1', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='10.1.1.1', step_value='0.0.0.1')

    ixNetwork.info('Configuring BgpIpv4Peer 2')
    bgp2 = ipv4.BgpIpv4Peer.add(Name='Bgp2')
    bgp2.DutIp.Increment(start_value='10.1.1.1', step_value='0.0.0.1')
    bgp2.Type.Single('internal')
    bgp2.LocalAs2Bytes.Increment(start_value=101, step_value=0)
    bgp2.AdvertiseEvpnRoutesForOtherVtep = 'True' 
    bgp2.FilterEvpn.Single(True)

    ixNetwork.info('Configuring EVPN 2')
    evpn2 = bgp2.BgpIPv4EvpnVXLAN.add(Name= 'EVPN_VXLAN_2')
    bgp2.BgpEthernetSegmentV4.EvisCount = evi_count
    bgp2.BgpEthernetSegmentV4.VtepIpv4Address.Increment(start_value='10.1.2.1', step_value='0.0.0.1')
    evpn2.NumBroadcastDomainV4 = '1' 
    evpn2.RdEvi.Custom(start_value='1', step_value='0',increments=[('1', l3_rt_count, [('0', l3_rt_repeat_value , [])])])
    evpn2.BgpL3VNIExportRouteTargetList.find()[0].TargetAssignedNumber.Custom(start_value=l3_label_start_value, step_value='0',increments=[('1', l3_rt_count, [('0', l3_rt_repeat_value , [])])])
    evpn2.BgpExportRouteTargetList.find()[0].TargetAssignedNumber.Custom(start_value=l2_label_start_value, step_value='0',increments=[('1', evi_count, [])])

    ixNetwork.info('Configuring Network Group 2')
    networkGroup2=deviceGroup2.NetworkGroup.add(Name='BGP-Routes-2', Multiplier='1')
    macPool2 = networkGroup2.MacPools.add(NumberOfAddresses='1')
    CMacProperties2 = macPool2.CMacProperties.add()
    connectorMac2= macPool2.Connector.find()
    connectorMac2.ConnectedTo='/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1/bgpIPv4EvpnVXLAN/1'

    ipv4PrefixPool = macPool2.Ipv4PrefixPools.add(NumberOfAddresses='1')
    ipv4PrefixPool.NetworkAddress.Increment(start_value='20.20.0.2', step_value='0.0.1.0')
    ipv4PrefixPool.PrefixLength.Single(16)
    macPool2.CMacProperties.find()[0].FirstLabelStart.Custom(start_value=l2_label_start_value, step_value='0',increments=[('1', evi_count, [])])
    macPool2.CMacProperties.find()[0].EnableSecondLabel.Single (True)
    macPool2.CMacProperties.find()[0].SecondLabelStart.Custom(start_value=l3_label_start_value, step_value='0',increments=[('1', l3_rt_count, [('0', l3_rt_repeat_value , [])])])
    macPool2.CMacProperties.find()[0].AdvertiseIpv4Address.Single (True)
    macPool2.CMacProperties.find()[0].Ipv4AddressPrefixLength.Single(32)


    ixNetwork.StartAllProtocols(Arg1='sync')

    ixNetwork.info('Verify protocol sessions\n')
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
    ixNetwork.info(protocolSummary)

    ixNetwork.info('Create Traffic Item')
    trafficItem = ixNetwork.Traffic.TrafficItem.add(Name='Traffic Item 1', BiDirectional=False, TrafficType='ipv4')

    ixNetwork.info('Add endpoint flow group')
    trafficItem.EndpointSet.add(Sources=topology1, Destinations=topology2)

    ixNetwork.info('Configuring config elements')
    configElement = trafficItem.ConfigElement.find()[0]
    configElement.FrameRate.update(Type='percentLineRate', Rate=50)
    configElement.FrameRateDistribution.PortDistribution = 'splitRateEvenly'
    configElement.FrameSize.FixedSize = 128
    trafficItem.Tracking.find()[0].TrackBy = ['flowGroup0']

    trafficItem.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.StartStatelessTrafficBlocking()

    flowStatistics = session.StatViewAssistant('Flow Statistics')

    ixNetwork.info('{}\n'.format(flowStatistics))

    for rowNumber,flowStat in enumerate(flowStatistics.Rows):
        ixNetwork.info('\n\nSTATS: {}\n\n'.format(flowStat))
        ixNetwork.info('\nRow:{}  TxPort:{}  RxPort:{}  TxFrames:{}  RxFrames:{}\n'.format(
            rowNumber, flowStat['Tx Port'], flowStat['Rx Port'],
            flowStat['Tx Frames'], flowStat['Rx Frames']))

    ixNetwork.Traffic.StopStatelessTrafficBlocking()

    if debugMode == False:
        # For linux and connection_manager only
        for vport in ixNetwork.Vport.find():
            vport.ReleasePort()
        session.Session.remove()
        print ('Releasing ports and Removing Session')        

except Exception as errMsg:
    print('\n%s' % traceback.format_exc(None, errMsg))
    if debugMode == False and 'session' in locals():
        session.Session.remove()