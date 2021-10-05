"""
ldppwvpls.py:
    Within toplogy both Provider Edge(PE) and Provider(P) Routers are created.
    created.P router is emulated in the front Device Group(DG), which consists of both 
    OSPF as routing protocol as well as Basic LDP sessions for Transport Label         
    Distribution Protocol. The chained DG act as PE Router, where LDP Extended Martini 
    is configured for VPN Label distibution protocol.Bidirectional L2-L3 Traffic is    
    configured in between two CE cloud is created.                                     
     Script Flow:			                                                         
     1. Configuration of protocols.	                                                 
         Configuration flow of the script is as follow:                                  
 		i.    Adding of OSPF router.			        	                         
 		ii.   Adding of Network Cloud.      				                         
 		iii.  Adding of chain DG.					                                 
 		iv.   Adding of LDP(basic session) on Front DG 		                         
 		v.    Adding of LDP Extended Martini(Targeted sess.) over chained DG.        
 		vi.   Adding of LDP PW/VPLS Tunnel over LDP Extended Martini.	             
    2. Start the ldp protocol.                                                      
    3. Retrieve protocol statistics.                                         	    
    4. Retrieve protocol learned info.                                              
    5. Disbale/Enable the ldp FECs and change label & apply change on the fly       
    6. Retrieve protocol learned info again and notice the difference with          
       previouly retrieved learned info.                                            
    7. Configure L2-L3 traffic.                                                     
    8. Start the L2-L3 traffic.                                                     
    9. Retrieve L2-L3 traffic stats.                                                
   10. Stop L2-L3 traffic.                                                          
   11. Stop all protocols.   
    
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
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=None, UserName=username,
                               Password=password, SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel='all', LogFilename='restpy.log')

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
    ip1.Address.Single("51.51.51.1")
    ip1.GatewayIp.Single("51.51.51.2")
    ip1.Prefix.Single(26)
    ip1.ResolveGateway.Single(True)

    ixNetwork.info("Adding LDP over IPv4 stacks")
    ldp1 = ip1.LdpBasicRouter.add()

    ixNetwork.info("Adding OSPFv2 over Ipv4 Stack")
    ospf1= ip1.Ospfv2.add()

    ixNetwork.info("making the NetworkType to point to point")
    networkTypeMultivalue = ospf1.NetworkType
    networkTypeMultivalue.Single("pointtopoint")

    ixNetwork.info("Adding Network Group behind ldp")
    networkGroup1 = dg1.NetworkGroup.add(Name="LDP_1 Network Group", Multiplier = "10")

    ixNetwork.info("Adding ipv4 prefix pools on Network Topology")
    ipv4PrefixPools1 = networkGroup1.Ipv4PrefixPools.add()

    ixNetwork.info("Changing Prefix Length for ipv4 prefix pools")
    ipv4PrefixPools1.PrefixLength.Single("32")

    ixNetwork.info("Updating Network Address of ipv4 prefix pools")
    ipv4PrefixPools1.NetworkAddress.Increment(start_value = "200.1.0.1", step_value = "0.0.0.1")

    ixNetwork.info("Adding ipv4 loopback for configuring PE Routers above it")
    chainedDg1 = networkGroup1.DeviceGroup.add(Name = "Device group 3", Multiplier= 1)
    loopback1 = chainedDg1.Ipv4Loopback.add(Name = "Ipv4 Lopback 1", StackedLayers = [])

    addressSet3 = loopback1.Address
    addressSet3.Increment(start_value = "200.1.0.1", step_value = "0.0.0.1")

    ixNetwork.info("Add LDP Targeted Router")
    ldpTargeted1 = loopback1.LdpTargetedRouter.add()
    ldpTargetedPeer1 = ldpTargeted1.LdpTargetedPeer
    addressSet5 = ldpTargetedPeer1.IPAddress
    addressSet5.Increment(start_value = "201.1.0.1", step_value = "0.0.0.1")

    ixNetwork.info("Add LFp FEC129 on top of LDP targeted router")
    ldpPwVpls1 = ldpTargeted1.Ldppwvpls.add()
    peerId1 = ldpPwVpls1.PeerId
    peerId1.Increment(start_value = "201.1.0.1", step_value = "0.0.0.1")

    ixNetwork.info("Adding Mac Cloud Behind LDP PWs")
    networkGroup3 = chainedDg1.NetworkGroup.add()
    macPools1  = networkGroup3.MacPools.add(Name = "CE MAC Cloud 1")

    ixNetwork.info("Creating Topology 2")
    topology2 = ixNetwork.Topology.add(Name="EVPN Topology 2", Ports=vport['Port_2'])

    ixNetwork.info("Adding DeviceGroup 2")
    dg2 = topology2.DeviceGroup.add(Name='LDP Router 2', Multiplier=1)

    ixNetwork.info("Adding Ethernet/AC Endpoints")
    mac2 = dg2.Ethernet.add()
    mac2.Mac.Increment(start_value="22:01:01:01:01:01", step_value="00:00:00:00:00:01")

    ixNetwork.info("Adding IPv4 on Ethernet")
    ip2 = mac2.Ipv4.add()
    ip2.Address.Single("51.51.51.2")
    ip2.GatewayIp.Single("51.51.51.1")
    ip2.Prefix.Single(26)
    ip2.ResolveGateway.Single(True)

    ixNetwork.info("Adding LDP over IPv4 stacks")
    ldp2 = ip2.LdpBasicRouter.add()

    ixNetwork.info("Adding OSPFv2 over Ipv4 Stack")
    ospf2= ip2.Ospfv2.add()

    ixNetwork.info("making the NetworkType to point to point")
    networkTypeMultivalue = ospf2.NetworkType
    networkTypeMultivalue.Single("pointtopoint")

    ixNetwork.info("Adding Network Group behind ldp")
    networkGroup2 = dg2.NetworkGroup.add(Name="LDP_1 Network Group", Multiplier = "10")

    ixNetwork.info("Adding ipv4 prefix pools on Network Topology")
    ipv4PrefixPools2 = networkGroup2.Ipv4PrefixPools.add()

    ixNetwork.info("Changing Prefix Length for ipv4 prefix pools")
    ipv4PrefixPools2.PrefixLength.Single("32")

    ixNetwork.info("Updating Network Address of ipv4 prefix pools")
    ipv4PrefixPools2.NetworkAddress.Increment(start_value = "201.1.0.1", step_value = "0.0.0.1")

    ixNetwork.info("Adding ipv4 loopback for configuring PE Routers above it")
    chainedDg2 = networkGroup2.DeviceGroup.add(Name = "Device group 4", Multiplier= 1)
    loopback2 = chainedDg2.Ipv4Loopback.add(Name = "Ipv4 Loopback 2", StackedLayers = [])

    addressSet3 = loopback2.Address
    addressSet3.Increment(start_value = "201.1.0.1", step_value = "0.0.0.1")

    ixNetwork.info("Add LDP Targeted Router")
    ldpTargeted2 = loopback2.LdpTargetedRouter.add()
    ldpTargetedPeer2 = ldpTargeted2.LdpTargetedPeer
    addressSet5 = ldpTargetedPeer2.IPAddress
    addressSet5.Increment(start_value = "200.1.0.1", step_value = "0.0.0.1")

    ixNetwork.info("Add LFp FEC129 on top of LDP targeted router")
    ldpPwVpls2 = ldpTargeted2.Ldppwvpls.add()
    peerId2 = ldpPwVpls2.PeerId
    peerId2.Increment(start_value = "200.1.0.1", step_value = "0.0.0.1")

    ixNetwork.info("Adding Mac Cloud Behind LDP PWs")
    networkGroup4 = chainedDg2.NetworkGroup.add()
    macPools2  = networkGroup4.MacPools.add(Name = "CE MAC Cloud 1")

    ixNetwork.info("Starting protocols and waiting 60 seconds for protcols to come up")
    ixNetwork.StartAllProtocols()

    ixNetwork.info('Verify protocol sessions\n')
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    #protocolSummary.AddRowFilter('Protocol Type', protocolSummary.REGEX, '(?i)^BGP?')
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.GREATER_THAN_OR_EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
    ixNetwork.info(protocolSummary)

    ixNetwork.info("Fetching LDP Basic Learned Info")
    ldp1.GetIPv4FECLearnedInfo("1")
    time.sleep(5)

    linfo1 = ldp1.LearnedInfo.find()[0]
    values1 = linfo1.Values

    for v in values1:
        print(v)
    
    ixNetwork.info("Fetching FEC 128 Learned Info")
    ldpTargeted2.GetFEC128LearnedInfo("1")
    
    linfo2 = ldpTargeted2.LearnedInfo.find()[0]
    values2 = linfo2.Values

    for v in values2:
        print(v)

    ixNetwork.info("Changing FEC Labels on the fly")
    feclabel1 = ldpPwVpls1.Label
    feclabel1.Increment(start_value = "5001", step_value = "100" )

    ixNetwork.info("Applying n the fly")
    ixNetwork.Globals.Topology.ApplyOnTheFly()

    time.sleep(15)

    ixNetwork.info("Fetching FEC 128 Learned Info, it must be \
        updated after previous OTF change")
    ldpTargeted2.GetFEC128LearnedInfo("1")
    
    linfo2 = ldpTargeted2.LearnedInfo.find()[0]
    values2 = linfo2.Values

    for v in values2:
        print(v)
    
    ixNetwork.info("Stopping Protocols")
    ixNetwork.StopAllProtocols()

    if debugMode == False:
        for vport in ixNetwork.Vport.find():
            vport.ReleasePort()
            
        # For linux and connection_manager only
        if session.TestPlatform.Platform != 'windows':
            session.Session.remove()

except Exception as errMsg:
    print('\n%s' % traceback.format_exc(None, errMsg))
    if 'session' in locals():
        session.Session.remove()


    
    



    




      


