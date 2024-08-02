"""
rocev2.py:

   Four ports all-to-all full mesh 

   - Connect to the API server
   - Assign ports:
        - If variable forceTakePortOwnership is True, take over the ports if they're owned by another user.
        - If variable forceTakePortOwnership if False, abort test.
   - Configure four Topology Groups: IPv4/RoCEv2
   - Start all protocols
   - Verify all protocols
   - Start traffic
   - Get Traffic Item
   - Get RoCEv2 Flow Statistics stats

Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements:
   - Minimum IxNetwork 10.20.2403.2
   - Python 2.7 and 3+
   - pip install requests
   - pip install ixnetwork_restpy (minimum version 1.3.0)

RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy/#/

Usage:
   - Enter: python <script>
"""

import sys, os, time, traceback

from ixnetwork_restpy import *

apiServerIp = '192.168.28.15'

ixChassisIpList = ['10.36.75.23']
portList = [f'{ixChassisIpList[0]}/1', f'{ixChassisIpList[0]}/2', f'{ixChassisIpList[0]}/3', f'{ixChassisIpList[0]}/4']

# For Linux API server only
username = 'admin'
password = 'admin'

# Leave session opened at the end
debugMode = True

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True

try:
    # LogLevel: none, info, warning, request, request_response, all
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=None, UserName='admin', Password='admin', 
                               SessionName=None, SessionId=None, ApiKey=None,
                               ClearConfig=True, LogLevel='all', LogFilename='restpy.log')

    ixNetwork = session.Ixnetwork
   
    ixNetwork.info('Assign ports')
    portMap = session.PortMapAssistant()
    vport = dict()
    for index,port in enumerate(portList):
        portName = 'Port_{}'.format(index+1)
        vport[portName] = portMap.Map(Location=port)

    portMap.Connect(forceTakePortOwnership)
    rocev2PeerList = []

    ixNetwork.info('Creating Topology Group 1')
    topology1 = ixNetwork.Topology.add(Name='Topo1', Ports=vport['Port_1'])
    deviceGroup1 = topology1.DeviceGroup.add(Name='DG1', Multiplier='1')
    ethernet1 = deviceGroup1.Ethernet.add(Name='Eth1')
    ethernet1.Mac.Increment(start_value='00:01:01:01:00:01', step_value='00:00:00:00:00:01')
    ixNetwork.info('Configuring IPv4 1')
    ipv4 = ethernet1.Ipv4.add(Name='Ipv4')
    ipv4.Address.Increment(start_value='71.1.1.2', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='71.1.1.1', step_value='0.0.0.0')
    rocev2_1 = ipv4.Rocev2.add(Name=f'RoCEv2 1', QpCount=1)
    rocev2PeerList.append(rocev2_1)
                
    ixNetwork.info('Creating Topology Group 2')
    topology2 = ixNetwork.Topology.add(Name='Topo2', Ports=vport['Port_2'])
    deviceGroup2 = topology2.DeviceGroup.add(Name='DG2', Multiplier='1')
    ethernet2 = deviceGroup2.Ethernet.add(Name='Eth2')
    ethernet2.Mac.Increment(start_value='00:01:01:02:00:01', step_value='00:00:00:00:00:01')
    ixNetwork.info('Configuring IPv4 2')
    ipv4 = ethernet2.Ipv4.add(Name='Ipv4-2')
    ipv4.Address.Increment(start_value='71.2.1.2', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='71.2.1.1', step_value='0.0.0.0')
    rocev2_2 = ipv4.Rocev2.add(Name=f'RoCEv2 2', QpCount=1)
    rocev2PeerList.append(rocev2_2)
      
    ixNetwork.info('Creating Topology Group 3')
    topology2 = ixNetwork.Topology.add(Name='Topo3', Ports=vport['Port_3'])
    deviceGroup2 = topology2.DeviceGroup.add(Name='DG3', Multiplier='1')
    ethernet2 = deviceGroup2.Ethernet.add(Name='Eth3')
    ethernet2.Mac.Increment(start_value='00:01:01:02:00:01', step_value='00:00:00:00:00:01')
    ixNetwork.info('Configuring IPv4 3')
    ipv4 = ethernet2.Ipv4.add(Name='Ipv4-3')
    ipv4.Address.Increment(start_value='71.3.1.2', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='71.3.1.1', step_value='0.0.0.0')
    rocev2_3 = ipv4.Rocev2.add(Name=f'RoCEv2 3', QpCount=1)
    rocev2PeerList.append(rocev2_3)
        
    ixNetwork.info('Creating Topology Group 4')
    topology2 = ixNetwork.Topology.add(Name='Topo4', Ports=vport['Port_4'])
    deviceGroup2 = topology2.DeviceGroup.add(Name='DG4', Multiplier='1')
    ethernet2 = deviceGroup2.Ethernet.add(Name='Eth4')
    ethernet2.Mac.Increment(start_value='00:01:01:02:00:01', step_value='00:00:00:00:00:01')
    ixNetwork.info('Configuring IPv4 4')
    ipv4 = ethernet2.Ipv4.add(Name='Ipv4-4')
    ipv4.Address.Increment(start_value='71.4.1.2', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='71.4.1.1', step_value='0.0.0.0')
    rocev2_4 = ipv4.Rocev2.add(Name=f'RoCEv2 4', QpCount=1)
    rocev2PeerList.append(rocev2_4)
     
    topologyList = ixNetwork.Topology.find()
    for topology in topologyList:
        rocev2 = topology.DeviceGroup.find().Ethernet.find().Ipv4.find().Rocev2.find()
        for peer in rocev2PeerList:
            rocev2.AddDestinationPeers(peer)
            
    # Examples that show how to configure NGPF RoCEv2flow 1 settings
    qpNumber = 101
    for index, roceFlow in enumerate(rocev2_1.Flows.find()):
        roceFlow.Name = f"RoCE Flow Settings {index}"
        roceFlow.CustomizeQP = True
        roceFlow.BufferSize.Single(1024)
        roceFlow.BufferSizeRemote.Single(1024)
        roceFlow.BufferSizeUnit.Single("byte") 
        roceFlow.BufferSizeUnitRemote.Single("mb") 
        #rocFlow1.CustomQP.Single(101)
        roceFlow.CustomQP.ValueList([qpNumber])
        roceFlow.Dscp.Single(11) 
        roceFlow.DscpRemote.Single(0) 
        roceFlow.ExecuteCommands.Single("rdmawrite") 
        roceFlow.ExecuteCommandsRemote.Single("none") 
        roceFlow.UdpSourcePort.Increment(start_value=1001, step_value=1) 
        roceFlow.UdpSourcePortRemote.Increment(start_value=3001, step_value=1)
        qpNumber += 1
        
    ixNetwork.StartAllProtocols(Arg1='sync')

    ixNetwork.info('Verify protocol sessions\n')
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
    ixNetwork.info(protocolSummary)

    ixNetwork.info('Create RoCEv2 Traffic')
    ixNetwork.Traffic.AddRoCEv2FlowGroups()
    
    # Exmaples that show configuring all RoCEv2 Traffic stream settings
    for stream in ixNetwork.Traffic.RoceV2Traffic.RoceV2Stream.find():
        stream.Enabled = True
        stream.BurstCount = 1
        # continuous | fixed
        stream.Type = 'fixed'
    
    # Examples that shows configuring DCQCN settings on port config 1
    rocev2_1_dcqcn_params = ixNetwork.Traffic.RoceV2Traffic.RoceV2PortConfig.find()[0].RoceV2DcqcnParams
    rocev2_1_dcqcn_params.Enabled = True
    
    # Examples that shows configuring port config 1 settings
    for portConfig in ixNetwork.Traffic.RoceV2Traffic.RoceV2PortConfig.find():
        portConfig.InterBatchPeriodUnits = 'nanoseconds'
        portConfig.InterBatchPeriodValue = 1
        portConfig.TargetLineRateInPercent = 98
        portConfig.TxCtrlParam = 'targetLineRate'
      
    ixNetwork.Traffic.RoceV2Traffic.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()

    rocev2FlowStatistics = session.StatViewAssistant('RoCEv2 Flow Statistics')
    ixNetwork.info(f'{rocev2FlowStatistics}\n')

    for rowNumber,flowStat in enumerate(rocev2FlowStatistics.Rows):
        ixNetwork.info(f'\n\nSTATS: {flowStat}\n\n')
    
    for rowNumber,flowStat in enumerate(rocev2FlowStatistics.Rows):
        ixNetwork.info(f"\nRow:{rowNumber}  TxPort:{flowStat['Tx Port']}  RxPort:{flowStat['Rx Port']}  TxFrames:{flowStat['Data Frames Tx']}  RxFrames:{flowStat['Data Frames Rx']}\n")

    ixNetwork.Traffic.Stop()
    ixNetwork.StartAllProtocols(Arg1='sync')

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




