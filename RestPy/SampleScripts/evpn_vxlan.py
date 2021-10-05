"""
evpnvxlan.py:
   It will create 2 BGP EVPN-VXLAN topologies, each having OSPFv2         
   configured in connected Device Group .BGP EVPN VXLAN configured in chained  
   device group along with Mac pools connected behind the chained             
   Device Group.

   Tested with two back-2-back IxNetwork ports
   - Connect to the API server
   - Configure license server IP
   - Assign ports
   - Physical topology:                            Port1 ----- Port2
   - Configure two Topology Groups
   - We will add an OSPF Router, with a Network Topology, dg chained to it 
     with BGP over loopback. Further add EVPN VXLAN over BGP and add MAC 
     cloud associated with the IP Addresses.
   - Start all protocols
   - Verify all protocols
   - Verify learned Info
   - Change a parameter OTF
   - Verify learned info again
   - Configure L2-3 Traffic
   - Apply and Start traffic
   - Get/Show Flow Statistics stats
   - Stop L2-3 Traffic
   - Stop Protocols
   
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

# For Linux API server and Windows Connection Mgr only.
#    debugMode=True:  Leave the session opened for debugging.
#    debugMode=False: Remove the session when the script is done.
debugMode = False

try:
    # LogLevel: none, info, warning, request, request_response, all
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=None, UserName='admin', Password='admin', 
                               SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel="all", LogFilename='restpy.log')

    ixNetwork = session.Ixnetwork
    ixNetwork.info('Assign ports')
    portMap = session.PortMapAssistant()
    vport = dict()
    for index,port in enumerate(portList):
        portName = 'Port_{}'.format(index+1)
        vport[portName] = portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=portName)

    portMap.Connect(forceTakePortOwnership)
    
    ixNetwork.info("Creating Topology")
    topology1 = ixNetwork.Topology.add(Name="EVPN VXLAN Topology 1", Ports=vport['Port_1'])
    
    ixNetwork.info("Adding Device Group")
    dg1 = topology1.DeviceGroup.add(Name='Label Switch Router 1', Multiplier=1)

    ixNetwork.info("Adding Ethernet/MAC endpoints")
    mac1 = dg1.Ethernet.add()
    mac1.Mac.Increment(start_value="22:01:01:01:01:01", step_value="00:00:00:00:00:01")
  
    ixNetwork.info("Addding Ipv4")
    ip1 = mac1.Ipv4.add()
    ip1.Address.Single("51.51.51.2")
    ip1.GatewayIp.Single("51.51.51.1")
    ip1.Prefix.Single(26)
    ip1.ResolveGateway.Single(True)

    ixNetwork.info("Adding OSPF")
    ospf1 = ip1.Ospfv2.add()

    ixNetwork.info("Setting Network type to point-to-point")
    ospf1.NetworkType.Single("pointtopoint")
    
    ixNetwork.info("Disabling the Discard learned Info")
    dg1.Ospfv2Router.find().DiscardLearnedLsa.Single(True)
    
    ixNetwork.info("Adding Network Group")
    networkGroup1 = dg1.NetworkGroup.add(Name="Network Topology 1")
    netTopo1= networkGroup1.NetworkTopology.add()

    ixNetwork.info("Add IPv4 loopback for EVPN VXLAN Leaf Ranges")
    chainedDg1 = networkGroup1.DeviceGroup.add(Name="Edge Router 1", Multiplier=1)
    loopback1 = chainedDg1.Ipv4Loopback.add(StackedLayers=[], Name = "IPv4 Loopback 2")
    addressSet1 = loopback1.Address
    addressSet1.Increment(start_value = "2.1.1.1", step_value ="0.1.0.0") 

    ixNetwork.info('Adding BGPv4 over IPv4 loopback in chained DG')
    bgpIpv4Peer1 = loopback1.BgpIpv4Peer.add()
    bgpIpv4Peer1.DutIp.Single("3.1.1.1")
    
    ixNetwork.info("Enabling Learned Route Filters for EVPN VXLAN in BGP4 Peer")
    bgpIpv4Peer1.FilterEvpn.Single("1")
    
    ixNetwork.info("Configuring Router\'s MAC Addresses for EVPN VXLAN in BGP4 Peer")
    bgpIpv4Peer1.RoutersMacOrIrbMacAddress.Increment(start_value = "aa:aa:aa:aa:aa:aa", step_value = "00:00:00:00:00:01")
    
    ixNetwork.info("Changing Router Id of Network Topology to Loopback Address of Chained Device Group under Edge Router 1")
    simRouter1 = netTopo1.SimRouter.find()[0] 
    simRouter1.RouterId.Increment(start_value = "2.1.1.1", step_value = "0.0.0.1")
    
    ixNetwork.info("Adding EVPN VXLAN over BGPv4 in chained DG")
    bgpIPv4EvpnVXLAN1 = bgpIpv4Peer1.BgpIPv4EvpnVXLAN.add()
    
    ixNetwork.info("Disabling Import RT List same as Export RT List")
    bgpIPv4EvpnVXLAN1.ImportRtListSameAsExportRtList = 'false'
    
    ixNetwork.info("Changing Import Route Target AS No.")
    bgpImportRouteTargetList1 = bgpIPv4EvpnVXLAN1.BgpImportRouteTargetList.find()[0]  
    bgpImportRouteTargetList1.TargetAsNumber.Increment(start_value = "200", step_value = "0")
    bgpExportRouteTargetList1 = bgpIPv4EvpnVXLAN1.BgpExportRouteTargetList.find()[0]
    bgpExportRouteTargetList1.TargetAsNumber.Increment(start_value=200, step_value = "0")
   
    ixNetwork.info("Adding Mac Pools beinhd EVPN VXLAn DG")
    networkGroup1 = chainedDg1.NetworkGroup.add(Name="MAC_Pool_1", Multiplier=1)   
    mac3 = networkGroup1.MacPools.add()
    
    ixNetwork.info("Configuring Ipv4 Adresses associated with CMAC addresses")
    ipv4PrefixPools1 = mac3.Ipv4PrefixPools.add()
    mac3.NumberOfAddresses = "1"
    mac3.Mac.Increment(start_value="66:66:66:66:66:66", step_value="00:00:00:00:00:01")

    ixNetwork.info("Enabling using of VLAN in CMAC Ranges")
    mac3.UseVlans = "true"
    cMacvlan1 = mac3.Vlan.find()[0]
    
    ixNetwork.info("Configuring VLAN ID")
    cMacvlan1.VlanId.Increment(start_value = '501', step_value = '1')
    
    ixNetwork.info("Configuring VLAN Priority")
    cMacvlan1.Priority.Single("7")

    ixNetwork.info("Changing VNI related Parameters under CMAC Properties")
    cMacProperties1 = mac3.CMacProperties.find()[0]

    ixNetwork.info("Changing 1st Label(L2VNI)")
    cMacProperties1.FirstLabelStart.Increment(start_value = "1001", step_value = "10")

    ixNetwork.info("Changing 2nd Label(L3VNI)")
    cMacProperties1.SecondLabelStart.Increment(start_value = "2001", step_value = "10")

    ixNetwork.info("Changing Increment Modes across all VNIs")
    cMacProperties1.LabelMode.Single("increment")
    

    ixNetwork.info("Changing VNI step")
    cMacProperties1.LabelStep.Increment(start_value = "1", step_value = "0")

    ixNetwork.info("Creating Topology")
    topology2 = ixNetwork.Topology.add(Name="EVPN VXLAN Topology 2", Ports=vport['Port_2'])

    ixNetwork.info("Adding Device Group")
    dg2 = topology2.DeviceGroup.add(Name='Label Switch Router 2', Multiplier=1)

    ixNetwork.info("Adding Ethernet/MAC endpoints")
    mac2 = dg2.Ethernet.add()
    mac2.Mac.Single("44:01:01:01:01:01")

    ixNetwork.info("Addding Ipv4")
    ip2 = mac2.Ipv4.add()
    ip2.Address.Single("51.51.51.1")
    ip2.GatewayIp.Single("51.51.51.2")
    ip2.Prefix.Single(26)
    ip2.ResolveGateway.Single(True)

    ixNetwork.info("Adding OSPF")
    ospf2 = ip2.Ospfv2.add()

    ixNetwork.info("Setting Network type to point-to-point")
    ospf2.NetworkType.Single("pointtopoint")

    ixNetwork.info("Disabling the Discard learned Info")
    dg2.Ospfv2Router.find().DiscardLearnedLsa.Single(True)

    ixNetwork.info("Adding Network Group")
    networkGroup2 = dg2.NetworkGroup.add(Name="Network topology 2")
    netTopo2= networkGroup2.NetworkTopology.add()

    ixNetwork.info("Add IPv4 loopback for EVPN VXLAN Leaf Ranges")
    chainedDg2 = networkGroup2.DeviceGroup.add(Name="Edge Router 2", Multiplier=1)
    loopback2 = chainedDg2.Ipv4Loopback.add(StackedLayers=[], Name = "IPv4 Loopback 1")
    addressSet2 = loopback2.Address
    addressSet2.Increment(start_value = "3.1.1.1", step_value ="0.0.0.1")

    ixNetwork.info('Adding BGPv4 over IPv4 loopback in chained DG')
    bgpIpv4Peer2 = loopback2.BgpIpv4Peer.add()
    bgpIpv4Peer2.DutIp.Increment(start_value = "2.1.1.1", step_value = "0.0.0.1")

    ixNetwork.info("Enabling Learned Route Filters for EVPN VXLAN in BGP4 Peer")
    bgpIpv4Peer2.FilterEvpn.Single("1")

    ixNetwork.info("Configuring Router\'s MAC Addresses for EVPN VXLAN in BGP4 Peer")
    bgpIpv4Peer2.RoutersMacOrIrbMacAddress.Single("cc:cc:cc:cc:cc:cc")

    ixNetwork.info("Changing Router Id of Network Topology to Loopback Address of Chained Device Group under Edge Router 1")
    simRouter2 = netTopo2.SimRouter.find()[0]
    simRouter2.RouterId.Increment(start_value = "3.1.1.1", step_value = "0.0.0.1")

    ixNetwork.info("Adding EVPN VXLAN over BGPv4 in chained DG")
    bgpIPv4EvpnVXLAN2 = bgpIpv4Peer2.BgpIPv4EvpnVXLAN.add()

    ixNetwork.info("Disabling Import RT List same as Export RT List")
    bgpIPv4EvpnVXLAN2.ImportRtListSameAsExportRtList = 'false'

    ixNetwork.info("Changing Import Route Target AS No.")
    bgpImportRouteTargetList2 = bgpIPv4EvpnVXLAN2.BgpImportRouteTargetList.find()[0]
    bgpImportRouteTargetList2.TargetAsNumber.Increment(start_value = "200", step_value = "0")
    bgpExportRouteTargetList2 = bgpIPv4EvpnVXLAN2.BgpExportRouteTargetList.find()[0]
    bgpExportRouteTargetList2.TargetAsNumber.Increment(start_value=200, step_value = "0")

    ixNetwork.info("Adding Mac Pools beinhd EVPN VXLAN DG")
    networkGroup2 = chainedDg2.NetworkGroup.add(Name="MAC_Pool_2", Multiplier=1)
    mac4 = networkGroup2.MacPools.add()

    ixNetwork.info("Configuring Ipv4 Adresses associated with CMAC addresses")
    ipv4PrefixPools2 = mac4.Ipv4PrefixPools.add()
    mac4.NumberOfAddresses = "1"
    mac4.Mac.Single("88:88:88:88:88:88")

    ixNetwork.info("Enabling using of VLAN in CMAC Ranges")
    mac4.UseVlans = "true"
    cMacvlan2 = mac4.Vlan.find()[0]

    ixNetwork.info("Configuring VLAN ID")
    cMacvlan2.VlanId.Increment(start_value = '501', step_value = '1')

    ixNetwork.info("Configuring VLAN Priority")
    cMacvlan2.Priority.Single("7")

    ixNetwork.info("Changing VNI related Parameters under CMAC Properties")
    cMacProperties2 = mac4.CMacProperties.find()[0]

    ixNetwork.info("Changing 1st Label(L2VNI)")
    cMacProperties2.FirstLabelStart.Increment(start_value = "1001", step_value = "10")

    ixNetwork.info("Changing 2nd Label(L3VNI)")
    cMacProperties2.SecondLabelStart.Increment(start_value = "2001", step_value = "10")

    ixNetwork.info("Changing Increment Modes across all VNIs")
    cMacProperties2.LabelMode.Single("increment")

    ixNetwork.info("Changing VNI step")
    cMacProperties2.LabelStep.Increment(start_value = "1", step_value = "0")

    ixNetwork.info("Starting protocols and waiting 60 seconds for protcols to come up")
    ixNetwork.StartAllProtocols()

    ixNetwork.info('Verify protocol sessions\n')
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.GREATER_THAN_OR_EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
    ixNetwork.info(protocolSummary)

    ixNetwork.info("Displaying EVPN-VXLAN Learned Info")
    bgpIpv4Peer1.GetEVPNLearnedInfo("1")

    learnedInfo = bgpIpv4Peer1.LearnedInfo.find()[0].Table.find()[0]

    for table in learnedInfo:
        print("Table Type "+str(table.Type))
        print("Columns "+str(table.Columns))
        values = table.Values
        for value in values:
            for word in values:
                print(word)

    ixNetwork.info("Chaning Host Ip Address Value associated with CMAC in Topology 2")
    ipv4PrefixPools2.NetworkAddress.Single("203.101.1.1")

    ixNetwork.Globals.Topology.ApplyOnTheFly()
    time.sleep(5)

    ixNetwork.info("Printing updated EVPN VXLAN Learned Info")

    bgpIpv4Peer1.GetEVPNLearnedInfo("1")

    learnedInfo = bgpIpv4Peer1.LearnedInfo.find()[0].Table.find()[0]

    for table in learnedInfo:
        print("Table Type "+str(table.Type))
        print("Columns "+str(table.Columns))
        values = table.Values
        for value in values:
            for word in values:
                print(word)

    ixNetwork.info("Configuring L2-L3 Traffic Item")
    trafficItem1 = ixNetwork.Traffic.TrafficItem.add(Name="EVPN VXLAN Traffic 1",
    RoundRobinPacketOrdering="false", TrafficType="ipv4")

    endpointSet1 = trafficItem1.EndpointSet.add(Name="EndpointSet-1", MulticastDestinations=[],
    ScalableSources=[],MulticastReceivers=[],ScalableDestinations=[],NgpfFilters=[],
    TrafficGroups=[],Sources=ipv4PrefixPools1,Destinations=ipv4PrefixPools2)

    trafficItem1.Tracking.find().TrackBy= ["sourceDestEndpointPair0","ethernetIiWithoutFcsSourceaddress0","vxlanVni0","ethernetIiWithoutFcsDestinationaddress0","ipv4DestIp0","trackingenabled0","mplsFlowDescriptor0"]

    trafficItem1.Tracking.find().FieldWidth="thirtyTwoBits"
    trafficItem1.Tracking.find().ProtocolOffset="Root.0"

    ixNetwork.info("applying and starting L2/L3 traffic")
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()

    ixNetwork.info("Traffic runs for 20 seconds")
    time.sleep(20)

    ixNetwork.info("Verifying all the L2-L3 traffic stats")

    flowStatistics = session.StatViewAssistant('Flow Statistics')
    flowStatistics.AddRowFilter('Traffic Item', flowStatistics.REGEX, '^EVPN.*')
    flowStatistics.AddRowFilter('VXLAN:VNI', flowStatistics.EQUAL, "2001")
    

    ixNetwork.info('{}\n'.format(flowStatistics))

    ixNetwork.info("Stopping L2/3 traffic")
    ixNetwork.Traffic.Stop()

    ixNetwork.info("Stopping Protocols")
    ixNetwork.StopAllProtocols()

    ixNetwork.info("Test Script Ends")

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

