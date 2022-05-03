"""
bgpevpnvpws.py:
   This script intends to demonstrate how to use NGPF BGP EVPN-VPWS API.     
    About Topology:                                                           
       It will create 2 BGP EVPN-VPWS topologies, each having LDP configured  
       in connected Device Group .BGP EVPN-VPWS configured in chained device  
       group along with Mac pools connected behind the chained Device Group.   
    Script Flow:                                                                 
        Step 1. Configuration of protocols.                                   
                                                                              
    Configuration flow of the script is as follow:                            
       i.    Adding of Ethernet and IP within both topologies,                 
       ii.   Ading and configuration of OSPF and LDP router over IP           
       iii.  Adding of Route Range behind DG of each topology                 
       iv.   Configuring loopback address as Router ID                        
       v.    Adding of chain DG for both topologies, act as PE router         
       vi.   Adding of BGP over loopback address within chained DG in both    
               topologies                                                     
       vii.  Adding of EVPN-VPWS EVI over BGP within both topologies          
       viii. Adding of MAC cloud behind each EVPN-VPWS EVI                    
       ix.   Configuring VPWS Service Id and service Id along with label      
               value and No. of MAC pools                                     
                                                                              
    2. Start all protocol.                                                    
    3. Retrieve protocol statistics.                                          
    4. Retrieve protocol learned info.                                        
    5. Configure L2-L3 traffic.                                               
    6. Start the L2-L3 traffic.                                               
    7. Retrieve L2-L3 traffic stats.                                          
    8. Stop L2-L3 traffic.                                                    
    9. Stop all protocols.   
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

apiServerIp = '10.39.47.41'

ixChassisIpList = ['10.39.44.162']
portList = [[ixChassisIpList[0], 2,1], [ixChassisIpList[0], 2, 2]]

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
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=11219, UserName='admin', Password='admin', 
                               SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel="info", LogFilename='restpy.log')

    ixNetwork = session.Ixnetwork
    ixNetwork.info('Assign ports')
    portMap = session.PortMapAssistant()
    vport = dict()
    for index,port in enumerate(portList):
        portName = 'Port_{}'.format(index+1)
        vport[portName] = portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=portName)

    portMap.Connect(forceTakePortOwnership)
    
    ixNetwork.info("Creating Topology")
    topology1 = ixNetwork.Topology.add(Name="EVPN Topology 1", Ports=vport['Port_1'])

    ixNetwork.info("Adding Device Group")
    dg1 = topology1.DeviceGroup.add(Name='LDP Router 1', Multiplier=1)

    ixNetwork.info("Adding Ethernet/MAC endpoints")
    mac1 = dg1.Ethernet.add()

    mac1.Mac.Increment(start_value="22:01:01:01:01:01", step_value="00:00:00:00:00:01")

    ixNetwork.info("Addding Ipv4")
    ip1 = mac1.Ipv4.add()
    ip1.Address.Single("51.51.51.2")
    ip1.GatewayIp.Single("51.51.51.1")
    ip1.Prefix.Single(26)
    ip1.ResolveGateway.Single(True)

    ixNetwork.info("Adding LDP over IPv4 Stacks")
    ip1.LdpBasicRouter.add()

    ixNetwork.info("Adding NetworkGroup behing LDP dg")
    networkGroup1 = dg1.NetworkGroup.add(Name="LDP_1_Network_Group1", Multiplier=1)
    ldpPrefixPool1 = networkGroup1.Ipv4PrefixPools.add()\

    ixNetwork.info("Configuring LDP Prefixes")
    ldpPrefixPool1.NetworkAddress.Single("2.2.2.2")
    ldpPrefixPool1.PrefixLength.Single("32")
    
    ixNetwork.info("Adding IPv4 loopback in DeviceGroup behind NetworkGroup")
    chainedDG1 = networkGroup1.DeviceGroup.add(Multiplier=1, Name="Device Group 3")
    loopback1 = chainedDG1.Ipv4Loopback.add(StackedLayers=[], Name="IPv4 Loopback 1")
    addressSet1 = loopback1.Address
    addressSet1.Increment(start_value="2.2.2.2", step_value="0.0.0.1")

    ixNetwork.info("Adding BGP over IPv4 loopback Interfaces")
    bgp1 = loopback1.BgpIpv4Peer.add()

    ixNetwork.info("Setting IPs in BGP DUT IP tab")
    bgp1.DutIp.Single("3.2.2.2")

    ixNetwork.info("Enabling EVPN Learned Information for BGP Router")
    bgp1.FilterEvpn.Single("true")

    ixNetwork.info("Adding EVPN-VPWS EVi over BGP in both ports")
    evpnVpws1 = bgp1.BgpIPv4EvpnVpws.add()

    broadcastDomain1 = evpnVpws1.BroadcastDomainV4Vpws

    ixNetwork.info("Changing default values of Ethernet tag Id")    
    broadcastDomain1.EthernetTagId.Single("1000")

    ixNetwork.info("Changing default values of Remote Service Id")
    broadcastDomain1.RemoteServiceId.Single("2000")

    ixNetwork.info("Changing default values of AD Route Label")
    broadcastDomain1.AdRouteLabel.Single("5016")

    ixNetwork.info("Changing default values of No. of MAC Pools")
    broadcastDomain1.NoOfMacPools = 2

    ixNetwork.info("Adding Mac Pools behind EVPN VPWS")
    networkGroup3 = chainedDG1.NetworkGroup.add(Name="MAC_Pool_1", Multiplier=2)

    macPool1 = networkGroup3.MacPools.add()

    ixNetwork.info("Changing Default Values of MAC Addresses in MAC Pools")
    macPool1.Mac.Single("C0:11:01:00:00:05")

    ixNetwork.info("Creating Topology")
    topology2 = ixNetwork.Topology.add(Name="EVPN Topology 2", Ports=vport['Port_2'])

    ixNetwork.info("Adding Device Group")
    dg2 = topology2.DeviceGroup.add(Name='LDP Router 2', Multiplier=1)

    ixNetwork.info("Adding Ethernet/MAC endpoints")
    mac2 = dg2.Ethernet.add()
    mac2.Mac.Single("44:01:01:01:01:01")

    ixNetwork.info("Addding Ipv4")
    ip2 = mac2.Ipv4.add()
    ip2.Address.Single("51.51.51.1")
    ip2.GatewayIp.Single("51.51.51.2")
    ip2.Prefix.Single(26)
    ip2.ResolveGateway.Single(True)

    ixNetwork.info("Adding LDP over IPv4 Stacks")
    ip2.LdpBasicRouter.add()

    ixNetwork.info("Adding NetworkGroup behing LDP dg")
    networkGroup2 = dg2.NetworkGroup.add(Name="LDP_2_Network_Group1", Multiplier=1)
    ldpPrefixPool2 = networkGroup2.Ipv4PrefixPools.add()

    ixNetwork.info("Configuring LDP Prefixes")
    ldpPrefixPool2.NetworkAddress.Single("3.2.2.2")
    ldpPrefixPool2.PrefixLength.Single("32")

    ixNetwork.info("Adding IPv4 loopback in DeviceGroup behind NetworkGroup")
    chainedDG2 = networkGroup2.DeviceGroup.add(Multiplier=1, Name="Device Group 4")
    loopback2 = chainedDG2.Ipv4Loopback.add(StackedLayers=[], Name="IPv4 Loopback 2")
    addressSet2 = loopback2.Address
    addressSet2.Increment(start_value="3.2.2.2", step_value="0.0.0.1")

    ixNetwork.info("Adding BGP over IPv4 loopback Interfaces")
    bgp2 = loopback2.BgpIpv4Peer.add()

    ixNetwork.info("Setting IPs in BGP DUT IP tab")
    bgp2.DutIp.Single("2.2.2.2")

    ixNetwork.info("Enabling EVPN Learned Information for BGP Router")
    bgp2.FilterEvpn.Single("true")

    ixNetwork.info("Adding EVPN-VPWS EVi over BGP in both ports")
    evpnVpws2 = bgp2.BgpIPv4EvpnVpws.add()
    broadcastDomain2 = evpnVpws2.BroadcastDomainV4Vpws

    ixNetwork.info("Changing default values of Ethernet tag Id")    
    broadcastDomain2.EthernetTagId.Single("2000")

    ixNetwork.info("Changing default values of Remote Service Id")
    broadcastDomain2.RemoteServiceId.Single("1000")

    ixNetwork.info("Changing default values of AD Route Label")
    broadcastDomain2.AdRouteLabel.Single("7016")

    ixNetwork.info("Changing default values of No. of MAC Pools")
    broadcastDomain2.NoOfMacPools = 2

    ixNetwork.info("Adding Mac Pools behind EVPN VPWS")
    networkGroup4 = chainedDG2.NetworkGroup.add(Name="MAC_Pool_2", Multiplier=2)
    macPool2 = networkGroup4.MacPools.add()

    ixNetwork.info("Changing Default Values of MAC Addresses in MAC Pools")
    macPool2.Mac.Single("C0:12:01:00:00:05")

    ixNetwork.info("Starting protocols and waiting 60 seconds for protcols to come up")
    ixNetwork.StartAllProtocols()
    time.sleep(60)

    ixNetwork.info('Verify protocol sessions\n')
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    protocolSummary.AddRowFilter('Protocol Type', protocolSummary.REGEX, '(?i)^BGP?')
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.GREATER_THAN_OR_EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
    ixNetwork.info(protocolSummary)

    ixNetwork.info("Displaying EVPN-VXLAN Learned Info")
    bgp1.GetEVPNLearnedInfo("1")

    learnedInfo = bgp1.LearnedInfo.find()[0].Table.find()[0]

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
    TrafficGroups=[],Sources=ldpPrefixPool1,Destinations=ldpPrefixPool2)

    trafficItem1.Tracking.find().TrackBy= ["sourceDestEndpointPair0","ipv4DestIp0","trackingenabled0","mplsFlowDescriptor0"]

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
    flowStatistics.AddRowFilter('Loss %', flowStatistics.EQUAL, "0")
    

    ixNetwork.info('{}\n'.format(flowStatistics))

    ixNetwork.info("Stopping L2/3 traffic")
    ixNetwork.Traffic.Stop()

    ixNetwork.info("Stopping Protocols")
    ixNetwork.StopAllProtocols()

    ixNetwork.info("Test Script Ends")

except Exception as errMsg:
    # print('\n%s' % traceback.format_exc(None, errMsg))
    print(traceback.print_exception())
    if 'session' in locals():
        session.Session.remove()
