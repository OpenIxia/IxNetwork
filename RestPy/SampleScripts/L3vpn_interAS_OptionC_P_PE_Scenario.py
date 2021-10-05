"""
L3vpn_interAS_OptionC_P_PE_Scenario.py:

This script intends to demonstrate how to use NGPF BGP API to configure
     L3vpn interAS OptionC Scenario.

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
"""

import sys, os, time, traceback

# Import the Restpy module
from ixnetwork_restpy import SessionAssistant

print('!!! L3VPN Option C Test Script Starts !!!')
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

try:
    # Connection to Windows API server
    print('Connecting to IxNetwork Client')
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=None, UserName=username,
                               Password=password, SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel='all', LogFilename='restpy.log')

    ixNetwork = session.Ixnetwork

    ixNetwork.info('cleaning up the old config file and creating an empty config')
    portMap = session.PortMapAssistant()
    vport = dict()

    ixNetwork.info('Assign test ports into IxNetwork')
    for index,port in enumerate(portList):
        portName = 'Port_{}'.format(index+1)
        vport[portName] = portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=portName)
        portMap.Connect(forceTakePortOwnership)

    ixNetwork.info('Adding Topology')
    topology1 = ixNetwork.Topology.add(Name='L3VPN_interAS_OptionC_Topology', Ports=vport['Port_1'])

    ixNetwork.info('Adding Device Group')
    p1Dg1 = topology1.DeviceGroup.add(Name='Provider Router', Multiplier='1')

    ixNetwork.info('Adding Ethernet/Mac Endpoints')
    ethernet1 = p1Dg1.Ethernet.add(Name='Ethernet 1')
    ixNetwork.info('Configuring the MAC Addresses')
    ethernet1.Mac.Increment(start_value='00:ca:ff:ee:00:01', step_value='00:00:00:00:00:01')
    ethernet1.EnableVlans.Single(False)

    ixNetwork.info('Add IPv4')
    ipv4 = ethernet1.Ipv4.add(Name='Ipv4 1')
    ixNetwork.info('Configuring IPv4 Interface')
    ipv4.Address.Increment(start_value='20.20.20.2', step_value='0.0.0.0')
    ipv4.GatewayIp.Increment(start_value='20.20.20.1', step_value='0.0.0.0')
    ipv4.Prefix.Single(24)

    ixNetwork.info('Adding OSPF over IPv4 Stack0')
    ixNetwork.info('Configuring Ospf Router on P Router 1')
    p1Ospf = ipv4.Ospfv2.add(Name='OSPFV2-IF1')

    ixNetwork.info('Configuring Ldp Over IPv4 Stack')
    p1ldp = ipv4.LdpBasicRouter.add(Name='LDP 1')

    ixNetwork.info('Adding NetworkGroup behind Provider Router DG')
    networkGroup1 = p1Dg1.NetworkGroup.add(Name='Network_Group', Multiplier='1')
    ipv4PrefixPool = networkGroup1.Ipv4PrefixPools.add(NumberOfAddresses='1')
    ixNetwork.info('Configuring LDP prefixes')
    ipv4PrefixPool.NetworkAddress.Increment(start_value='2.2.2.2', step_value='0.0.0.1')
    ipv4PrefixPool.PrefixLength.Single(32)

    ixNetwork.info('Add Chained DG behind LDP NetworkGroup')
    chainedDg1 = networkGroup1.DeviceGroup.add(Name='Device Group 3', Multiplier='1')
    pe1LoopBackv4 = chainedDg1.Ipv4Loopback.add(Name='IPv4 loopback 1')
    pe1LoopBackv4.Address.Increment(start_value='2.2.2.2', step_value='0.0.0.1')

    ixNetwork.info('Adding BGP over IPv4 loopback interfaces')
    eBgp = pe1LoopBackv4.BgpIpv4Peer.add(Name='Multihop eBGP Peer')
    eBgp.update(EthernetSegmentsCountV4=2)

    ixNetwork.info('Setting IPs in BGP DUT IP tab')
    eBgp.DutIp.Increment(start_value='3.2.2.2', step_value='0.0.0.1')

    ixNetwork.info('Changing bgp type to external')
    eBgp.Type.Single('external')

    ixNetwork.info('Adding another BGP Peer over same IPv4 loopback interface')
    iBgp = pe1LoopBackv4.BgpIpv4Peer.add(Name='iBGP Peer')

    ixNetwork.info('Setting IPs in iBGP DUT IP tab')
    iBgp.DutIp.Increment(start_value='4.2.2.2', step_value='0.0.0.1')

    ixNetwork.info('Changing bgp type to internal')
    iBgp.Type.Single('internal')

    ixNetwork.info('Enabling IPv4 MPLS Capability in iBGP Peer')
    iBgp.CapabilityIpV4Mpls.Single(True)

    ixNetwork.info('Enabling L3VPN Learned Information filters for BGP Router')
    eBgp.FilterIpV4Mpls.Single(True)
    eBgp.FilterIpV4MplsVpn.Single(True)
    iBgp.FilterIpV4Mpls.Single(True)
    iBgp.FilterIpV4MplsVpn.Single(True)

    ixNetwork.info('Adding VRF over eBGP Peer')
    eBgp.BgpVrf.add()

    ixNetwork.info('Adding IPv4 Address Pool behind bgpVrf with name VPN RouteRange(Src)')
    networkGroup3=chainedDg1.NetworkGroup.add(Multiplier='1',Name='VPN RouterRange(Src)')
    vrf1 = networkGroup3.Ipv4PrefixPools.add(NumberOfAddresses=1)
    ixNetwork.info('Changing default values of IP Prefixes in VPN RouteRange(Src)')
    vrf1.NetworkAddress.Increment(start_value='11.11.11.1' , step_value='0.0.0.1')

    ixNetwork.info('Adding another IPv4 Address Pool connected to iBGP Peer')
    networkGroup4=chainedDg1.NetworkGroup.add(Multiplier='1',Name='eBGP Lpbk Addr(MPLS RR)')
    vrf2 = networkGroup4.Ipv4PrefixPools.add(NumberOfAddresses=1)
    vrf2.NetworkAddress.Increment(start_value='2.2.2.2' , step_value='0.0.0.1')

    ixNetwork.info('Changing BGP Connector in 2nd Prefix Pool')
    connector=vrf2.Connector.find()
    connector.ConnectedTo=iBgp.href

    ixNetwork.info('Enabling IPv4 MPLS Capability in iBGP Prefix Pool')
    bgpIPRouteProperty = vrf2.BgpIPRouteProperty.find()
    bgpIPRouteProperty.AdvertiseAsBgp3107 = True

    ixNetwork.info('Changing label start value in iBGP Prefix Pool')
    vrf2.BgpIPRouteProperty.find().LabelStart.Increment(start_value='21',step_value='5')

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