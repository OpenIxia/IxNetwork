"""
bgpevpn.py:
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
   - We will add an OSPF and LDP Router, with a Network Topology, dg chained to it 
     with BGP over loopback. Further add EVPN VPWS EVI over BGP and add MAC 
     cloud associated with the IP Addresses.
   - Start all protocols
   - Verify all protocols
   - Verify learned Info
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
    
    ixNetwork.info("Creating Topology 1")
    topology1 = ixNetwork.Topology.add(Name="EVPN Topology 1", Ports=vport['Port_1'])

    ixNetwork.info("Adding DeviceGroup 1")
    dg1 = topology1.DeviceGroup.add(Name='LDP Router 1', Multiplier=1)

    ixNetwork.info("Adding Ethernet/AC Endpoints")
    mac1 = dg1.Ethernet.add()
    mac1.Mac.Increment(start_value="22:01:01:01:01:01", step_value="00:00:00:00:00:01")

    ixNetwork.info("Adding IPv4 on Ethernet")
    ip1 = mac1.Ipv4.add()
    ip1.Address.Single("51.51.51.2")
    ip1.GatewayIp.Single("51.51.51.1")
    ip1.Prefix.Single(26)
    ip1.ResolveGateway.Single(True)

    ixNetwork.info("Adding LDP Basic Router on Ipv4")
    ldp1 = ip1.LdpBasicRouter.add()

    ixNetwork.info("Adding Network Group begind Device Group 1")
    networkGroup1 = dg1.NetworkGroup.add(Name="Network Topology 1")
    netTopo1= networkGroup1.NetworkTopology.add()
    chainedDg1 = networkGroup1.DeviceGroup.add(Name="Edge Router 1", Multiplier=1)

    ixNetwork.info("Adding IPv4 Loopback for EVPN VXLAN Leaf Ranges")
    loopback1 = chainedDg1.Ipv4Loopback.add(StackedLayers=[], Name = "IPv4 Loopback 2")
    addressSet1 = loopback1.Address
    addressSet1.Increment(start_value = "2.2.2.2", step_value ="0.1.0.0")

    ixNetwork.info("Adding a BGPIpv4Peer on top of IPv4 loopback")
    bgp1 = loopback1.BgpIpv4Peer.add()

    ixNetwork.info("Setting DUT Ips in BGP")
    bgp1.DutIp.Single("3.2.2.2")

    ixNetwork.info("Enabling EVPN Learned Information for BGP Router")
    bgp1.FilterEvpn.Single("true")

    ixNetwork.info("Adding EVPN EVI over BGP")
    bgp1.BgpIPv4EvpnEvi.add()

    ixNetwork.info("Configuring ESI value")
    
    ethernetSegment1 = bgp1.BgpEthernetSegmentV4
    ethernetSegment1.EsiValue.Single("1")

    ixNetwork.info("Adding Mac Pools behind EVPN dg")
    networkGroup1 = chainedDg1.NetworkGroup.add(Name="MAC_Pool_1", Multiplier=1)
    mac3 = networkGroup1.MacPools.add()

    ixNetwork.info("Configuring Ipv4 Address assicayed with CMAC addresses")
    ipv4PrefixPools1 = mac3.Ipv4PrefixPools.add()
    
    mac3.Mac.Single("A0:11:01:00:00:03")

    ixNetwork.info("Changing default values of MAC Labels")
    cMAC1 = mac3.CMacProperties.find()[0]
    cMAC1.FirstLabelStart.Single("1000")

    ixNetwork.info("Changing default values of Ip Prefixes")
    ipv4PrefixPools1.NetworkAddress.Single("11.11.11.1")

    ixNetwork.info("Creating Topology 1")
    topology2 = ixNetwork.Topology.add(Name="EVPN Topology 2", Ports=vport['Port_2'])  

    ixNetwork.info("Adding DeviceGroup 1")
    dg2 = topology2.DeviceGroup.add(Name='LDP Router 2', Multiplier=1)  

    ixNetwork.info("Adding Ethernet/AC Endpoints")
    mac2 = dg2.Ethernet.add()   
    mac2.Mac.Single("44:01:01:01:01:01")

    ixNetwork.info("Adding IPv4 on Ethernet")
    ip2 = mac2.Ipv4.add()
    ip2.Address.Single("51.51.51.1")
    ip2.GatewayIp.Single("51.51.51.2")
    ip2.Prefix.Single(26)
    ip2.ResolveGateway.Single(True)
    ixNetwork.info("Adding ldp over IPv4 stacks")

    ixNetwork.info("Adding LDP Basic Router on Ipv4")
    ldp2 = ip2.LdpBasicRouter.add()
    
    ixNetwork.info("Adding Network Group begind Device Group 1")
    networkGroup2 = dg2.NetworkGroup.add(Name="Network topology 2")
    netTopo2= networkGroup2.NetworkTopology.add()    
    chainedDg2 = networkGroup2.DeviceGroup.add(Name="Edge Router 2", Multiplier=1)

    ixNetwork.info("Add IPv4 loopback for EVPN VXLAN Leaf Ranges")
    loopback2 = chainedDg2.Ipv4Loopback.add(StackedLayers=[], Name = "IPv4 Loopback 1")
    addressSet2 = loopback2.Address
    addressSet2.Increment(start_value = "3.2.2.2", step_value ="0.0.0.1")

    ixNetwork.info("Adding BGP over IPv4 loopback interfaces")
    bgp2 = loopback2.BgpIpv4Peer.add()

    ixNetwork.info("Setting IPs in BGP DUT IP tab")
    bgp2.DutIp.Single("2.2.2.2")

    ixNetwork.info("Enabling EVPN Learned Information for BGP Router")
    bgp2.FilterEvpn.Single("true")

    ixNetwork.info("Adding EVPN EVI over BGP in both ports")
    bgp2.BgpIPv4EvpnEvi.add()

    ixNetwork.info("Configuring ESI value in both ports")
    ethernetSegment2 = bgp2.BgpEthernetSegmentV4
    ethernetSegment2.EsiValue.Single("2")

    ixNetwork.info("Adding Mac Pools behind EVPN DG")
    networkGroup2 = chainedDg2.NetworkGroup.add(Name="MAC_Pool_2", Multiplier=1)
    mac4 = networkGroup2.MacPools.add()

    ixNetwork.info("Configuring Ipv4 Adresses associated with CMAC addresses")   
    ipv4PrefixPools2 = mac4.Ipv4PrefixPools.add() 
    
    mac4.Mac.Single("A0:12:01:00:00:03")

    ixNetwork.info("Changing default values of MAC Labels")
    cMAC2 = mac4.CMacProperties.find()[0]
    cMAC2.FirstLabelStart.Single("2000")

    ixNetwork.info("Changing Default values of IP Prefixes")
    ipv4PrefixPools2.NetworkAddress.Single("12.12.12.1")

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

    
    ixNetwork.info("Stopping Protocols")
    ixNetwork.StopAllProtocols()

    ixNetwork.info("Test Script Ends")

except Exception as errMsg:
    # print('\n%s' % traceback.format_exc(None, errMsg))
    print(traceback.print_exception())
    if 'session' in locals():
        session.Session.remove()



















