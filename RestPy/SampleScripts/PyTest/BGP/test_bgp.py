"""
PyTest sample to show how to use PyTest fixtures to connect to IxNetwork API server,
run traffic and get stats.

This sample script requires passing in a config file on the CLI.

Requirements:
    - ConfigFiles/qaSetup.yml
    - BGP folder with bgp.py script

Usage:
   pytest -v -s -x --configFile ConfigFiles/qaSetup.yml BGP

"""
import sys, os, traceback
import pytest

runTraffic = True

class BGP(): 
    def test_setup_ixia(self, connectIxNetwork, ixNetworkSessionObj, ixNetworkObj, middleware):
        """
        Configure IxNetwork BGP NGPF.
        
        connectIxNetwork <fixture>: Connects to IxNetwork API server
        ixNetworkSessioinObj <object>: RestPy session object
        ixNetworkObj <object>: RestPy IxNetwork object
        """
        # IxNetwork config params are passed into this script from pytest fixtures middleware
        print('\n--- middleware:', middleware.params)
        
        forceTakePortOwnership = middleware.params['forceTakePortOwnership']
            
        try:
            portList = middleware.params['portList']

            ixNetworkObj.info('Assign ports')
            portMap = ixNetworkSessionObj.PortMapAssistant()
            vport = dict()
            # Eliminated vmone chassis.  There will be no chassis to retrieve from the sandbox.
            # Just use range to create 2 vports.
            for index,port in enumerate(portList):
                # for index in range(0,2):
                portName = 'Port_{}'.format(index+1)
                vport[portName] = portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=portName)
                #vport[portName] = ixNetworkObj.Vport.add(Name=portName)

            if runTraffic:
                portMap.Connect(forceTakePortOwnership)
            
            ixNetworkObj.info('Creating Topology Group 1')
            topology1 = ixNetworkObj.Topology.add(Name='Topo1', Ports=vport['Port_1'])
            deviceGroup1 = topology1.DeviceGroup.add(Name='DG1', Multiplier='3')
            ethernet1 = deviceGroup1.Ethernet.add(Name='Eth1')
            ethernet1.Mac.Increment(start_value='00:01:01:01:00:01', step_value='00:00:00:00:00:01')
            ethernet1.EnableVlans.Single(True)

            ixNetworkObj.info('Configuring vlanID')
            vlanObj = ethernet1.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)

            ixNetworkObj.info('Configuring IPv4')
            ipv4 = ethernet1.Ipv4.add(Name='Ipv4')
            ipv4.Address.Increment(start_value='1.1.1.1', step_value='0.0.0.1')
            ipv4.GatewayIp.Increment(start_value='1.1.1.4', step_value='0.0.0.0')

            ixNetworkObj.info('Configuring BgpIpv4Peer 1')
            bgp1 = ipv4.BgpIpv4Peer.add(Name='Bgp1')
            bgp1.DutIp.Increment(start_value='1.1.1.4', step_value='0.0.0.1')
            bgp1.Type.Single('external')
            bgp1.LocalAs2Bytes.Increment(start_value=101, step_value=0)

            ixNetworkObj.info('Configuring Network Group 1')
            networkGroup1 = deviceGroup1.NetworkGroup.add(Name='BGP-Routes1', Multiplier='100')
            ipv4PrefixPool = networkGroup1.Ipv4PrefixPools.add(NumberOfAddresses='1')
            ipv4PrefixPool.NetworkAddress.Increment(start_value='10.10.0.1', step_value='0.0.0.1')
            ipv4PrefixPool.PrefixLength.Single(32)

            ixNetworkObj.info('Creating Topology Group 2')
            topology2 = ixNetworkObj.Topology.add(Name='Topo2', Ports=vport['Port_2'])
            deviceGroup2 = topology2.DeviceGroup.add(Name='DG2', Multiplier='3')

            ethernet2 = deviceGroup2.Ethernet.add(Name='Eth2')
            ethernet2.Mac.Increment(start_value='00:01:01:02:00:01', step_value='00:00:00:00:00:01')
            ethernet2.EnableVlans.Single(True)

            ixNetworkObj.info('Configuring vlanID')
            vlanObj = ethernet2.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)

            ixNetworkObj.info('Configuring IPv4 2')
            ipv4 = ethernet2.Ipv4.add(Name='Ipv4-2')
            ipv4.Address.Increment(start_value='1.1.1.4', step_value='0.0.0.1')
            ipv4.GatewayIp.Increment(start_value='1.1.1.1', step_value='0.0.0.0')
        
            ixNetworkObj.info('Configuring BgpIpv4Peer 2')
            bgp2 = ipv4.BgpIpv4Peer.add(Name='Bgp2')
            bgp2.DutIp.Increment(start_value='1.1.1.1', step_value='0.0.0.1')
            bgp2.Type.Single('external')
            bgp2.LocalAs2Bytes.Increment(start_value=102, step_value=0)

            ixNetworkObj.info('Configuring Network Group 2')
            networkGroup2 = deviceGroup2.NetworkGroup.add(Name='BGP-Routes2', Multiplier='100')
            ipv4PrefixPool = networkGroup2.Ipv4PrefixPools.add(NumberOfAddresses='1')
            ipv4PrefixPool.NetworkAddress.Increment(start_value='20.20.0.1', step_value='0.0.0.1')
            ipv4PrefixPool.PrefixLength.Single(32)
            
            if runTraffic:
                ixNetworkObj.StartAllProtocols(Arg1='sync')

                ixNetworkObj.info('Verify protocol sessions\n')
                protocolSummary = ixNetworkSessionObj.StatViewAssistant('Protocols Summary')
                protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.EQUAL, 0)
                protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
                ixNetworkObj.info(protocolSummary)

            ixNetworkObj.info('Create Traffic Item')
            trafficItem = ixNetworkObj.Traffic.TrafficItem.add(Name='BGP Traffic', BiDirectional=False, TrafficType='ipv4')
            
            ixNetworkObj.info('Add endpoint flow group')
            trafficItem.EndpointSet.add(Sources=topology1, Destinations=topology2)

            # Note: A Traffic Item could have multiple EndpointSets (Flow groups).
            #       Therefore, ConfigElement is a list.
            ixNetworkObj.info('Configuring config elements')
            configElement = trafficItem.ConfigElement.find()[0]
            configElement.FrameRate.update(Type='percentLineRate', Rate=50)
            configElement.FrameRateDistribution.PortDistribution = 'splitRateEvenly'
            configElement.FrameSize.FixedSize = 128
            trafficItem.Tracking.find()[0].TrackBy = ['flowGroup0']

            if runTraffic:
                trafficItem.Generate()
                ixNetworkObj.Traffic.Apply()
                ixNetworkObj.Traffic.StartStatelessTrafficBlocking()

                flowStatistics = ixNetworkSessionObj.StatViewAssistant('Flow Statistics')
                ixNetworkObj.info('{}\n'.format(flowStatistics))

                for rowNumber,flowStat in enumerate(flowStatistics.Rows):
                    ixNetworkObj.info('\n\nSTATS: {}\n\n'.format(flowStat))
                    ixNetworkObj.info('\nRow:{}  TxPort:{}  RxPort:{}  TxFrames:{}  RxFrames:{}\n'.format(
                        rowNumber, flowStat['Tx Port'], flowStat['Rx Port'],
                        flowStat['Tx Frames'], flowStat['Rx Frames']))
                    
                ixNetworkObj.Traffic.StopStatelessTrafficBlocking()
                ixNetworkObj.StopAllProtocols(Arg1='sync')
                
                if middleware.params['debugMode'] == False:
                    for vport in ixNetworkObj.Vport.find():
                        vport.ReleasePort()
                        
                    # For linux and connection_manager only
                    if ixNetworkSessionObj.TestPlatform.Platform != 'windows':
                        ixNetworkSessionObj.Session.remove()
                
                if flowStatistics.Rows[0]['Tx Frames'] != flowStatistics.Rows[0]['Rx Frames']:
                    pytest.fail(f'\nFailed: Tx Frames: {flowStatistics.Rows[0]["Tx Frames"]}   Rx Frames: {flowStatistics.Rows[1]["Rx Frames"]}')
                    
        except Exception as errMsg:
            if middleware.params['debugMode'] == False:
                if ixNetworkSessionObj.TestPlatform.Platform != 'windows':
                    ixNetworkSessionObj.Session.remove()
                    
            pytest.fail('\n{}'.format(traceback.format_exc(None, errMsg)))

        
    def test_bgp(self, ixNetworkSessionObj, ixNetworkObj):
        """
        Start BGP traffic for testing.  Get stats for passed/failed result.
        
        sandboxConfigs <dict object>: A dict object containing toka controller/sandbox data
        ixNetworkSessioinObj <object>: RestPy session object
        ixNetworkObj <objecet>: RestPy IxNetwork object
        """
        ixNetworkObj.info('Starting test_bgp ...')
        
        '''
        try:
            if runTraffic:
                trafficItem.Generate()
                ixNetworkObj.Traffic.Apply()
                ixNetworkObj.Traffic.StartStatelessTrafficBlocking()

                flowStatistics = ixNetworkSessionObj.StatViewAssistant('Flow Statistics')
                ixNetworkObj.info('{}\n'.format(flowStatistics))

                for rowNumber,flowStat in enumerate(flowStatistics.Rows):
                    ixNetworkObj.info('\n\nSTATS: {}\n\n'.format(flowStat))
                    ixNetworkObj.info('\nRow:{}  TxPort:{}  RxPort:{}  TxFrames:{}  RxFrames:{}\n'.format(
                        rowNumber, flowStat['Tx Port'], flowStat['Rx Port'],
                        flowStat['Tx Frames'], flowStat['Rx Frames']))

                ixNetworkObj.Traffic.StopStatelessTrafficBlocking()
                ixNetworkObj.StartAllProtocols(Arg1='sync')
                
                if sandboxConfigs['debugMode'] == False:
                    for vport in ixNetworkObj.Vport.find():
                        vport.ReleasePort()
                        
                    # For linux and connection_manager only
                    if ixNetworkSessionObj.TestPlatform.Platform != 'windows':
                        ixNetworkSessionObj.Session.remove()
                        
        except Exception as errMsg:
            if sandboxConfigs['debugMode'] == False:
                if ixNetworkSessionObj.TestPlatform.Platform != 'windows':
                    ixNetworkSessionObj.Session.remove()
                    
            pytest.fail('\n{}'.format(traceback.format_exc(None, errMsg)))
        '''
        
    def test_teardown_ixia(self):
        assert True
