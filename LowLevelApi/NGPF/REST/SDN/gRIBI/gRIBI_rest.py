"""
gRIBI-NGPF.py:
   Tested with two back-2-back Ixia ports...
   - Connect to the API server
   - Configure two Topology Groups:
     - Topology 1 : gRIBI Client
     - Topology 2: IPv4 (gRIBI Server will run on this port)
     - gRIBI server not inplemented in IxNetwork. Tested with mock gRIBI server.
   - Configure Network Groupin topology1. Configure gRIBI IPv4 entries in prefix pools.
   - Commit changes
   - Assign ports
   - Start all protocols
   - Verify all protocols
   - Verify Protocol statistics 
Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux
Requirements:
   - Minimum IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install ixnetwork_restpy (minimum version 1.0.51)
RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy
Usage:
   - Enter: python <script>
"""

import sys, os, time, traceback, json
from time import time
# Import the RestPy module
from ixnetwork_restpy import SessionAssistant

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = False

try:
    # LogLevel: none, info, warning, request, request_response, all

    session_assistant = SessionAssistant(IpAddress='10.66.47.72', RestPort='11961',
                                         LogLevel=SessionAssistant.LOGLEVEL_INFO, ClearConfig=True)


    start = time()
    conf_assist = session_assistant.ConfigAssistant()
    config = conf_assist.config

    config.info('creating vport 1')
    vport1 = config.Vport.add()[-1]

    config.info('Creating Topology Group 1')
    topology1 = config.Topology.add(Name='Topo1', Ports=vport1)[-1]

    config.info('Creating Device Group 1')
    deviceGroup1 = topology1.DeviceGroup.add(Name='DG1', Multiplier='1')

    config.info('Creating Ethernet stack 1')
    ethernet1 = deviceGroup1.Ethernet.add(Name='Eth1')
    ethernet1.Mac.Increment(start_value='00:01:01:01:00:01', step_value='00:00:00:00:00:01')

    config.info('Enabling Vlan on Topology 1')
    ethernet1.EnableVlans.Single(True)

    config.info('Configuring vlanID')
    vlanObj1 = ethernet1.Vlan.add()
    vlanObj1.VlanId.Increment(start_value=103, step_value=0)

    config.info('Configuring IPv4')
    ipv4 = ethernet1.Ipv4.add(Name='IPv4')
    ipv4.Address.Increment(start_value='51.1.1.2', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='51.1.1.1', step_value='0.0.0.0')

    config.info('Configuring gRPCClient 1')
    gRPCClient1 = ipv4.gRPCClient.add(Name='gRPCClient')
    conf_assist.commit()

    gRPCClient1.RemoteIp.Increment(start_value='51.1.1.1', step_value='0.0.0.0')
    gRPCClient1.Type.Single('internal')
    gRPCClient1.RemotePort.Increment(start_value=50001, step_value=0)
    conf_assist.commit()

    config.info('Configuring gRIBI Client 1')
    gRIBIClient1 = gRPCClient1.gRIBIClient.add(Name='gRIBIClient')
    gRIBIClient1.clientRedundancy.Pattern(value="singleprimary")
    gRIBIClient1.Type.Single('internal')
    gRIBIClient1.electionIdLow.Increment(start_value="2001", step_value='10')
    gRIBIClient1.electionIdHigh.Increment(start_value="1001", step_value='10')

    config.info('Configuring gRIBI Next Hop Group 1')
    gRIBINextHopGroup1 = gRIBIClient.gRIBINextHopGroup.add(Name='gRIBINextHopGroup', multiplier='5')
    #nHopGroupMulti1 = gRIBINextHopGroup1.multiplier(value=5)
    #gRIBINextHopGroup1.Type.Single('internal')
    gRIBINextHopGroup1.numberOfNextHops(value='3')
    gRIBINextHopGroup1.Type.Single('internal')
   

    config.info('Configuring Network Group 1')
    networkGroup1 = gRIBINextHopGroup.NetworkGroup.add(Name="IPv4 Entries", Multiplier='3')
    ipv4PrefixPool = networkGroup1.Ipv4PrefixPools.add(NumberOfAddresses='10')
    ipv4PrefixPool.NetworkAddress.Increment(start_value='201.10.0.1', step_value='0.0.0.1')
    ipv4PrefixPool.PrefixLength.Single(32)
   
    
    
    config.info('creating vport 2')
    vport2 = config.Vport.add()[-1]

    config.info('Creating Topology Group 2')
    topology2 = config.Topology.add(Name='Topo2', Ports=vport2)[-1]

    config.info('Creating Device Group 2')
    deviceGroup2 = topology2.DeviceGroup.add(Name='DG2', Multiplier='1')

    config.info('Creating Ethernet 2')
    ethernet2 = deviceGroup2.Ethernet.add(Name='Eth2')
    ethernet2.Mac.Increment(start_value='00:01:01:02:00:01', step_value='00:00:00:00:00:01')

    config.info('Enabling Vlan on Topology 2')
    ethernet2.EnableVlans.Single(True)

    config.info('Configuring vlanID')
    vlanObj2 = ethernet2.Vlan.add()
    vlanObj2.VlanId.Increment(start_value=103, step_value=0)

    config.info('Configuring IPv4 2')
    ipv4 = ethernet2.Ipv4.add(Name='Ipv4-2')
    ipv4.Address.Increment(start_value='51.1.1.1', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='51.1.1.2', step_value='0.0.0.0')


    # generally its always advisable to configure everything first and then commit and do operation when using
    # config assistant so that the script execution is fast as well as creating the configuration at once as you can
    # see in this script everything configured then committing then all operation like start protocols view statsistics.

    config.info('committing changes')
    errs = conf_assist.commit()
    if len(errs) > 0:
        raise Exception('json import has errors %s' % str(errs))

        chassis_ip = '10.39.50.126'
        test_ports = [
            dict(Arg1=chassis_ip, Arg2=1, Arg3=1),
            dict(Arg1=chassis_ip, Arg2=1, Arg3=2)
        ]

        config.info('Assigning Ports')
        config.AssignPorts(test_ports, [], config.Vport, True)

        config.info('Starting NGPF protocols')
        config.StartAllProtocols(Arg1='sync')

        
        protocolsSummary = StatViewAssistant(ixnetwork, 'Protocols Summary')        print(protocolsSummary)
        protocolsSummary.AddRowFilter('Protocol Type', protocolsSummary.REGEX, '(?i)^gRIBI?')
        config.info('Verify protocol sessions\n')
        protocolSummary = session_assistant.StatViewAssistant('Protocols Summary')
        protocolSummary.CheckCondition('Sessions Configured', protocolSummary.EQUAL, 0)
        protocolSummary.CheckCondition('Sessions Up', protocolSummary.EQUAL, 0)
        protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.EQUAL, 0)
        protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
        protocolSummary.CheckCondition('Sessions Flapped', protocolSummary.EQUAL, 0)


            if not debugMode:
                # For linux and connection_manager only
                session_assistant.Session.remove()

                config.info('Test Case Passed !!!!!!!')

except Exception as errMsg:
    print('\n%s' % traceback.format_exc(None, errMsg))
    if not debugMode and 'session' in locals():
        session_assistant.Session.remove()