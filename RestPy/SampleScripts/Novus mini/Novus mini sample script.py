"""
Novusmini IxNetwork REST PY - API sample
Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux
Requirements:
   - Minimum IxNetwork 9.32EA
   - Python 2.7 and 3+
   - pip install requests
   - pip install ixnetwork_restpy (minimum version is 1.1.10)
RestPy Doc:
    https://openixia.github.io/ixnetwork_restpy/#/overview
    https://github.com/OpenIxia/ixnetwork_restpy
Usage:
   - Enter: python <script>
"""

import sys, os, time, traceback

from ixnetwork_restpy import *

# API Server - IP of the Novusmini Box
apiServerIp = '10.39.50.69'

# Define Chassis and Physical ports
ixChassisIpList = ['localchassis']
physicalPorts = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 1, 2]]

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = True

# Forcefully take port ownership even if the physical Ports are owned by other users.
forceTakePortOwnership = True

try:
    # LogLevel: none, info, warning, request, request_response, all
    # Connect to the IxNetwork session
    # NOTE : UrlPrefix="ixnetwork-mw" is a mandatory argument to pe passed to SessionAssistant to connect to the IxNetwork Session in Novusmini.
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=80, SessionName=None, SessionId=None, ApiKey=None, ClearConfig=True, UrlPrefix="ixnetwork-mw", LogLevel='info', LogFilename='restpy.log')
    ixNetwork = session.Ixnetwork

    ########################################################################################
    # Assign Ports 
    ########################################################################################
    vport = dict()
    portMap = session.PortMapAssistant()
    #vportSet = ixNetwork.Vport.find()
    for index,port in enumerate(physicalPorts):
        portName = 'Port_{}'.format(index+1)
        #vport[portName] = portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=vportSet[index].Name)
        vport[portName] = portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=portName)
        #print(vport[portName])

    #portMap.Connect(forceTakePortOwnership, LinkUpTimeout=90 )
    portMap.Connect(forceTakePortOwnership)

    vportSet = ixNetwork.Vport.find()
    vport1,vport2 = vportSet[0] , vportSet[1]

    ########################################################################################
    #  Topology configuration START
    ########################################################################################
  
    # Add Topology - 'Topology-Tx' on vport1. Add a Device Group and configure Ethernet and IPv4 stacks 
    ixNetwork.info('Create Topology-Tx')
    topology1 = ixNetwork.Topology.add(Name='Topology-Tx', Ports=vport1)
    topology1_deviceGroup1 = topology1.DeviceGroup.add(Name='DeviceGroup1-Tx', Multiplier='10')
    topology1_ethernet1 = topology1_deviceGroup1.Ethernet.add()
    topology1_ethernet1.Mac.Increment(start_value='00:11:01:01:00:01', step_value='00:00:00:00:00:01')
    
    ixNetwork.info('Enable Ethernet-VLAN and Configure vlan-ID')
    topology1_ethernet1.EnableVlans.Single(True)
    topology1_ethernet1_vlanValue = topology1_ethernet1.Vlan.find()[0].VlanId.Increment(start_value=101, step_value=1)
    
    topology1_ipv41 = topology1_deviceGroup1.Ethernet.find().Ipv4.add()
    topology1_ipv41.Address.Increment(start_value="100.1.0.2", step_value="0.0.1.0") 
    topology1_ipv41.GatewayIp.Increment(start_value="100.1.0.1", step_value="0.0.1.0") 
    topology1_ipv41.Prefix.Single(24) 
    topology1_ipv41.ResolveGateway.Single(True)

    # Topology-Tx configuration END

    # Add Topology - 'Topology-Rx' on vport2. Add a Device Group and configure Ethernet and IPv4 stacks 
    ixNetwork.info('Create Topology-Rx')
    topology2 = ixNetwork.Topology.add(Name='Topology-Rx', Ports=vport2)
    topology2_deviceGroup1 = topology2.DeviceGroup.add(Name='DeviceGroup1-Rx', Multiplier='10')
    topology2_ethernet1 = topology2_deviceGroup1.Ethernet.add()
    topology2_ethernet1.Mac.Increment(start_value='00:12:01:01:00:01', step_value='00:00:00:00:00:01')
    
    ixNetwork.info('Enable Ethernet-VLAN and Configure vlan-ID')
    topology2_ethernet1.EnableVlans.Single(True)
    topology2_ethernet1_vlanValue = topology2_ethernet1.Vlan.find()[0].VlanId.Increment(start_value=101, step_value=1)
    
    topology2_ipv41 = topology2_deviceGroup1.Ethernet.find().Ipv4.add()
    topology2_ipv41.Address.Increment(start_value="100.1.0.1", step_value="0.0.1.0") 
    topology2_ipv41.GatewayIp.Increment(start_value="100.1.0.2", step_value="0.0.1.0") 
    topology2_ipv41.Prefix.Single(24) 
    topology2_ipv41.ResolveGateway.Single(True)
    
    # Topology-Rx configuration END
  
    ########################################################################################
    #  Topology configuration END
    ########################################################################################  

    time.sleep(10)
    
    # Start All Protocols
    ixNetwork.StartAllProtocols(Arg1='sync')
    time.sleep(10)
    
 
    # Verify Protocol Summary Statistics
    ixNetwork.info('Validate and print Protocol Summary Statictics')
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    protocolSummary.CheckCondition('Sessions Up', protocolSummary.EQUAL, 20)
    protocolSummary.CheckCondition('Sessions Total', protocolSummary.EQUAL, 20)
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)

    ixNetwork.info(protocolSummary)  
    
    time.sleep(10)

    # Create a Traffic Item with Endpoints= Topology-Tx & Topology-Rx , Frame size = Fixed 1500B , Rate = 50% Line rate, Flow Tracking = Traffic Item, Source/Destination Value pair.   
    ixNetwork.info('Create a Traffic Item from Topology-Tx to Topology-Rx')
    trafficItem = ixNetwork.Traffic.TrafficItem.add(Name='IPv4 Traffic', BiDirectional=False, TrafficType='ipv4')

    ixNetwork.info('Add traffic flow endpoint set' )
    trafficItem.EndpointSet.add(Sources=topology1, Destinations=topology2)

    ixNetwork.info('Configuring config elements')
    configElement = trafficItem.ConfigElement.find()[0]
    configElement.FrameRate.update(Type='percentLineRate', Rate=50)
    configElement.FrameRateDistribution.PortDistribution = 'splitRateEvenly'
    configElement.FrameSize.FixedSize = 1500

    # Add Ingress flow tracking
    tracking = trafficItem.find().Tracking.find()
    tracking.TrackBy = ["trackingenabled0", "sourceDestValuePair0"] 
    #trafficItem.Tracking.TrackBy = ["trackingenabled0", "sourceDestValuePair0"] 
    
    # Generate , Apply and Start Traffic 
    ixNetwork.info("Generate , Apply and Start Traffic ")
    trafficItem.Generate()
    ixNetwork.Traffic.Apply()
    time.sleep(10)
    ixNetwork.Traffic.StartStatelessTrafficBlocking()
    
    # Let the traffic run for 30 secs
    time.sleep(30)
    
    # Flow Statictics
    
    #Find the Flow Statistics view and set page size
    flowStatView = ixNetwork.Statistics.find().View.find(Caption="Flow Statistics")
    flowStatViewPage = flowStatView.Page
    flowStatViewPage.PageSize = 50
    time.sleep(5)
    flowStatistics = session.StatViewAssistant('Flow Statistics')
    # Note : Various Filters can be added to retrieve a specifis row from Statview
    #flowStatistics.AddRowFilter('Rx Frames', flowStatistics.GREATER_THAN_OR_EQUAL, 100)
    #flowStatistics.AddRowFilter('PGID', flowStatistics.EQUAL, 0)
    #ixNetwork.info('{}\n'.format(flowStatistics))
    ixNetwork.info("\n\n Print Flow Statistics \n\n")
    for rowNumber,flowStat in enumerate(flowStatistics.Rows):
        #Print values from those flow stat rows which are active e.g. Tx Frames > 0  , Rx Frames > 0 , Tx Port != ""  
        if (int(flowStat['Tx Frames'])) > 0 :
            ixNetwork.info('\nRow : {}  \nSource/Destination Value Pair : {} \nTxPort : {}  \nRxPort : {}  \nTxFrames : {}  \nRxFrames : {}  \nLoss% : {}\n'.format(rowNumber, flowStat['Source/Dest Value Pair'], flowStat['Tx Port'], flowStat['Rx Port'],
                flowStat['Tx Frames'], flowStat['Rx Frames'], flowStat['Loss %']))
    
    #ixNetwork.info('\n\nSTATS: {}\n\n'.format(flowStat))

    # Stop Traffic and All Protocols
    ixNetwork.Traffic.StopStatelessTrafficBlocking()
    ixNetwork.StopAllProtocols(Arg1='sync')

    # Test END

    if debugMode == False:
        for vport in ixNetwork.Vport.find():
            vport.ReleasePort()
            
        # For linux and connection_manager only
        #if session.TestPlatform.Platform != 'windows':
        #    session.Session.remove()

except Exception as errMsg:
    print('\n%s' % traceback.format_exc(None, errMsg))
    if debugMode == False and 'session' in locals():
        if session.TestPlatform.Platform != 'windows':
            session.Session.remove()


