"""
LAG-Port-with-LACP-MACsec-MKA-sample.py:
    Tested with 8 back-2-back Test ports. 4 ports in a LAG. back-2-back LAG scenario
    - Connect to the API server
    - Assign ports:
            - If variable forceTakePortOwnership is True, take over the ports if they're owned by another user.
            - If variable forceTakePortOwnership if False, abort test.
    - Configure LAG port and configure the LACP, MACsec and MKA properties
    - Configure two Topology Groups: IPv4
    - Configure a Traffic Item
    - Start all protocols
    - Verify all protocols
    - Start traffic
    - Get Traffic Item
    - Get Flow Statistics stats
    - Perform control and data plane switchover
    - Get stats and validate stats
Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux
Requirements:
   - Minimum IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install ixnetwork_restpy (minimum version is 20220224.10.33)
RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy/#/
Usage:
   - Enter: python <script>
"""

import sys, os, time, traceback

from ixnetwork_restpy import *

# API Server
apiServerIp = '10.39.35.42'

# Chassis, card, Port
ixChassisIpList = ['10.36.5.138']
physicalPortList = [[ixChassisIpList[0], 1,13], [ixChassisIpList[0], 1,14], [ixChassisIpList[0], 1,15], [ixChassisIpList[0], 1,16],[ixChassisIpList[0], 1,17], [ixChassisIpList[0], 1,18],[ixChassisIpList[0], 1,19], [ixChassisIpList[0], 1,20]]

# Define Chassis and Physical ports

chassis_ip = '10.36.5.138'
physicalPorts = [
    dict(Arg1=chassis_ip, Arg2=1, Arg3=13),
    dict(Arg1=chassis_ip, Arg2=1, Arg3=14),
    dict(Arg1=chassis_ip, Arg2=1, Arg3=15),
    dict(Arg1=chassis_ip, Arg2=1, Arg3=16),
    dict(Arg1=chassis_ip, Arg2=1, Arg3=17),
    dict(Arg1=chassis_ip, Arg2=1, Arg3=18),
    dict(Arg1=chassis_ip, Arg2=1, Arg3=19),
    dict(Arg1=chassis_ip, Arg2=1, Arg3=20)
]


# For Linux API server only
username = 'admin'
password = 'admin'

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = False

# Forcefully take port ownership even if the physical Ports are owned by other users.
forceTakePortOwnership = True

try:
    # LogLevel: none, info, warning, request, request_response, all
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=None, UserName='admin', Password='admin', 
                               SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel='all', LogFilename='restpy.log')

    ixNetwork = session.Ixnetwork

    #  LAG configuration START

    ########################################################################################
    # Add a LAG - lag1 with 4 vports & configure MKA properties 
    ########################################################################################
    
    # Add 4 vports
    lag1_portSet = ixNetwork.Vport.add().add().add().add()
    #print(vports_1)
    lag1 = ixNetwork.Lag.add(Name='Lag-1', Vports=lag1_portSet)
    
    # Add Ethernet layer on LAG ProtocolStack
    lag1_ethernet = lag1.ProtocolStack.add().Ethernet.add()

    # Add LACP as the LAG protocol over LAG Ethernet
    lag1_lacp = lag1_ethernet.Lagportlacp.add()
    
    # Configure lag1 -LACP Actor System ID, Actor System priority and Actor key
    lag1_lacp.ActorSystemId.Single("aabbcc112233") 
    lag1_lacp.ActorSystemPriority.Single(100)
    lag1_lacp.ActorKey.Single(100) 

    # Configure lag1-LACP  LACPDU periodic Interval = fast (value = 1 sec) & LACPDU Timeout = Short (value = 3 sec)
    lag1_lacp.LacpduPeriodicTimeInterval.Single("fast") 
    lag1_lacp.LacpduTimeout.Single("short")   

    # Add LAG L23 protocols - MACsec, MKA over LAG Ethernet
    lag1_macsec = lag1_ethernet.Macsec.add()
    lag1_mka = lag1_ethernet.Mka.add()

    # Configure lag1-MKA properties

    # Set MKA-lag1 Rekey Mode and Rekey Behaviour
    lag1_mka.RekeyMode = "timerBased" 
    lag1_mka.RekeyBehaviour = "rekeyContinuous" 

    #periodic rekey at every 30 sec interval
    lag1_mka.PeriodicRekeyInterval = 30 

    # Set MKA Key derivation function = AES-CMAC-128  for all ports in lag1 
    lag1_mka.KeyDerivationFunction.Single("aescmac128") 
    # Set Cipher suite = GCM-AES-XPN-128 in MKA Key Server Attributes for all ports in lag1 
    lag1_mka.CipherSuite.Single("aesxpn128") 

    # Set MKA Key Server Priority = 11 for all ports in lag1 , so that these ports act as Key Server
    lag1_mka.KeyServerPriority.Single("11") 

    # Set MKPDU Hello interval - 2 sec (default)
    lag1_mka.MkaHelloTime.Single(2000) 
    # Configure different MKA - Starting Distribute AN for all ports in lag1 
    lag1_mka.StartingDistributedAN.Increment(start_value=0, step_value=1) 
    
    # Configure CAK, CKN values in MKA - PSK Chain , samme vales for all ports in lag1
    lag1_mka.CakCache.CakName.Single("11112222") 
    lag1_mka.CakCache.CakValue128.Single("00000000000000000000000011112222") 

    
    ########################################################################################
    # Add another LAG - lag2 with 4 vports & configure MKA properties 
    ########################################################################################
    
    # Add 4 vports
    lag2_portSet = ixNetwork.Vport.add().add().add().add()
    #print(vports_1)
    lag2 = ixNetwork.Lag.add(Name='Lag-2', Vports=lag2_portSet)
    
    # Add Ethernet layer on LAG ProtocolStack
    lag2_ethernet = lag2.ProtocolStack.add().Ethernet.add()

    # Add LACP as the LAG protocol over LAG Ethernet
    lag2_lacp = lag2_ethernet.Lagportlacp.add()

    # Configure lag2-LACP Actor System ID, Actor System priority and Actor key
    lag2_lacp.ActorSystemId.Single("ddeeff445566") 
    lag2_lacp.ActorSystemPriority.Single(100)
    lag2_lacp.ActorKey.Single(100) 

    # Configure lag2-LACP  LACPDU periodic Interval = fast (value = 1 sec) & LACPDU Timeout = Short (value = 3 sec)
    lag2_lacp.LacpduPeriodicTimeInterval.Single("fast") 
    lag2_lacp.LacpduTimeout.Single("short") 

    # Add LAG L23 protocols - MACsec, MKA over LAG Ethernet
    lag2_macsec = lag2_ethernet.Macsec.add()
    lag2_mka = lag2_ethernet.Mka.add()
    
    # Configure lag2-MKA properties

    # Set MKA Key derivation function = AES-CMAC-128  for all ports in lag1 
    lag2_mka.KeyDerivationFunction.Single("aescmac128") 
    # Set Cipher suite = GCM-AES-XPN-128 in MKA Key Server Attributes for all ports in lag1 
    lag2_mka.CipherSuite.Single("aesxpn128") 

    # Set MKPDU Hello interval - 2 sec (default)
    lag2_mka.MkaHelloTime.Single(2000) 
    # Configure different MKA - Starting Distribute AN for all ports in lag1 
    lag2_mka.StartingDistributedAN.Increment(start_value=0, step_value=1)  

    # Configure CAK, CKN values in MKA - PSK Chain , samme vales for all ports in lag2
    lag2_mka.CakCache.CakName.Single("11112222") 
    lag2_mka.CakCache.CakValue128.Single("00000000000000000000000011112222") 
    
    # LACP, MACsec, MKA is configured - LAG configuration END

    # Topology Configuration - START

    ########################################################################################
    # Create Topology - Topology-LAg-1 with 20 IpV4 devices and assign lag2 to the topology
    ########################################################################################
    ixNetwork.info('Creating Topology-1')
    topology1 = ixNetwork.Topology.add(Name='Topology-LAG-1', Ports=lag1)
    topology1_deviceGroup1 = topology1.DeviceGroup.add(Name='DG1', Multiplier='20')
    topology1_ethernet1 = topology1_deviceGroup1.Ethernet.add()
    #topology1_ethernet1.Mac.Increment(start_value='00:01:01:01:00:01', step_value='00:00:00:00:00:01')
    topology1_ethernet1.EnableVlans.Single(True)

    ixNetwork.info('Configuring vlanID')
    vlanObj = topology1_ethernet1.Vlan.find()[0].VlanId.Increment(start_value=101, step_value=1)

    ixNetwork.info('Configuring IPv4')
    topology1_ethernet1_ipv4 = topology1_ethernet1.Ipv4.add()
    topology1_ethernet1_ipv4.Address.Increment(start_value='20.1.1.1', step_value='0.0.1.0')
    topology1_ethernet1_ipv4.GatewayIp.Increment(start_value='20.1.1.2', step_value='0.0.1.0')


    ########################################################################################
    # Create Topology - Topology-LAg-2 with 20 IpV4 devices and assign lag2 to the topology
    ########################################################################################
    ixNetwork.info('Creating Topology-2')
    topology2 = ixNetwork.Topology.add(Name='Topology-LAG-2', Ports=lag2)
    topology2_deviceGroup1 = topology2.DeviceGroup.add(Name='DG2', Multiplier='20')
    topology2_ethernet1 = topology2_deviceGroup1.Ethernet.add()
    #topology2_ethernet1.Mac.Increment(start_value='00:01:01:01:00:01', step_value='00:00:00:00:00:01')
    topology2_ethernet1.EnableVlans.Single(True)

    ixNetwork.info('Configuring vlanID')
    vlanObj = topology2_ethernet1.Vlan.find()[0].VlanId.Increment(start_value=101, step_value=1)

    ixNetwork.info('Configuring IPv4')
    topology2_ethernet1_ipv4 = topology2_ethernet1.Ipv4.add()
    topology2_ethernet1_ipv4.Address.Increment(start_value='20.1.1.2', step_value='0.0.1.0')
    topology2_ethernet1_ipv4.GatewayIp.Increment(start_value='20.1.1.1', step_value='0.0.1.0')

    # Topology Configuration - END

    ########################################################################################
    # Assign Physical Ports to Vports
    ########################################################################################
    vportSet = ixNetwork.Vport.find()
    conf_assist = session.ConfigAssistant()
    config = conf_assist.config
    config.info('Committing the config changes')
    errs = conf_assist.commit()
    if len(errs) > 0:
        raise Exception('configAssistant commit errors -  %s' % str(errs))
    config.AssignPorts(physicalPorts, [], vportSet, True)
 

    ixNetwork.StartAllProtocols(Arg1='sync')
    
    # Verify Statistics
    ixNetwork.info('Verify Protocol Summary Statictics\n')
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
    ixNetwork.info(protocolSummary)  
    
    ixNetwork.info('Verify MACsec Per Port Statictics\n')
    macsecPerPort = session.StatViewAssistant('MACsec Per Port')
    macsecPerPort.CheckCondition('Bad Packet Rx', macsecPerPort.EQUAL, 0)
    macsecPerPort.CheckCondition('Invalid ICV Discarded', macsecPerPort.EQUAL, 0)
    ixNetwork.info(macsecPerPort)

    ixNetwork.info('Create Traffic Item')
    trafficItem = ixNetwork.Traffic.TrafficItem.add(Name='Encrypted IPv4 Traffic', BiDirectional=False, TrafficType='ipv4')

    ixNetwork.info('Add traffic flow endpoint set' )
    trafficItem.EndpointSet.add(Sources=topology1, Destinations=topology2)

    # Note: A Traffic Item could have multiple EndpointSets (Flow groups).
    #       Therefore, ConfigElement is a list.
    ixNetwork.info('Configuring config elements')
    configElement = trafficItem.ConfigElement.find()[0]
    configElement.FrameRate.update(Type='percentLineRate', Rate=50)
    configElement.FrameRateDistribution.PortDistribution = 'splitRateEvenly'
    configElement.FrameSize.FixedSize = 1500
    trafficItem.Tracking.find()[0].TrackBy = ['flowGroup0']
    
    trafficItem.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.StartStatelessTrafficBlocking()

    time.sleep(30)
    # Flow Statistics
    flowStatistics = session.StatViewAssistant('Flow Statistics')

    ixNetwork.info('{}\n'.format(flowStatistics))

    for rowNumber,flowStat in enumerate(flowStatistics.Rows):
        ixNetwork.info('\n\nSTATS: {}\n\n'.format(flowStat))
        ixNetwork.info('\nRow:{}  TxPort:{}  RxPort:{}  TxFrames:{}  RxFrames:{}  Loss% :{}\n'.format(
        rowNumber, flowStat['Tx Port'], flowStat['Rx Port'],
        flowStat['Tx Frames'], flowStat['Rx Frames'], flowStat['Loss %']))

    # Get the LACP nde
    Lag_lacp = ixNetwork \
	.Lag.find() \
	.ProtocolStack.find() \
	.Ethernet.find() \
	.Lagportlacp.find()

    lacp_lag1 = Lag_lacp[0]
    #lacp_lag2 = Lag_lacp[1]

    # Disable LACP Synchronization FLAG in lag1-port1 - to simulate control and data plane switchover
    lacp_lag1.SynchronizationFlag.Overlay(1, "false")
    # Apply changes on-the-fly
    ixNetwork.Globals.find().Topology.find().ApplyOnTheFly()

    time.sleep(30)

    # Verify Statistics  
    ixNetwork.info('Verify MACsec Per Port Statictics\n')
    macsecPerPort = session.StatViewAssistant('MACsec Per Port')
    macsecPerPort.CheckCondition('Bad Packet Rx', macsecPerPort.EQUAL, 0)
    macsecPerPort.CheckCondition('Invalid ICV Discarded', macsecPerPort.EQUAL, 0)
    ixNetwork.info(macsecPerPort) 

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
