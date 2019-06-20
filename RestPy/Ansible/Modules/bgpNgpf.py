# Ansible doc style
DOCUMENTATION = '''
---
module: bgpNgpf

Requirements:
  - IxNetwork 8.50 minimum
  - python requests module

Description:
  Configure two BGP topology groups in IxNetwork NGPF with one tx port and one rx port.

notes:
  - Connect to an API server.
  - Configure license server IP.
  - Assign ports.
  - If variable forceTakePortOwnership is True, take over the ports if they're owned by another user.
  - If variable forceTakePortOwnership if False, abort test.
  - Configure two Topology Groups - IPv4/BGP.
  - Configure Network Group for each topology for route advertising.
  - Configure a Traffic Item.
  - Start all protocols.
  - Verify all protocols.
  - Start traffic.
  - Get Traffic Item.
  - Get Flow Statistics stats.

'''

from ansible.module_utils.basic import AnsibleModule

import os, sys, traceback, logging

# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant

def main():
    logging.basicConfig(filename='../ansible.log', level=logging.DEBUG)

    # Define the available arguments/parameters that a user can pass to this module.
    params = {
        'apiServerIp':            {'type':'str', 'required':True, 'default':None},
        'apiServerIpPort':        {'type':'int', 'required':False, 'default':11009},
        'username':               {'type':'str', 'required':False, 'default':'admin', 'no_log':False},
        'password':               {'type':'str', 'required':False, 'default':'admin', 'no_log':False},
        'licenseServerIp':        {'type':'list', 'required':True, 'default':None},
        'licenseMode':            {'type':'str', 'required':True, 'default':None},
        'licenseTier':            {'type':'str', 'required':False, 'default':'tier3'},
        'portList':               {'type':'list', 'required':True, 'default':None},
        'forceTakePortOwnership': {'type':'bool', 'required':False, 'default':True},
        'debugMode':              {'type':'str', 'required':False, 'default':False},
    }

    result = dict(changed=False, message='')
    module = AnsibleModule(argument_spec=params, supports_check_mode=True)

    if module.check_mode:
        module.exit_json(**result)

    module.params['name'] = 'Custom Ansible module for NGPF BGP configuration'

    try:

        testPlatform = TestPlatform(ip_address=module.params['apiServerIp'],
                                    rest_port=module.params['apiServerIpPort'],
                                    log_file_name='restpy.log')

        # Console output verbosity: None|request|'request response'
        testPlatform.Trace = 'request_response'

        testPlatform.Authenticate(module.params['username'], module.params['password'])
        session = testPlatform.Sessions.add()
        ixNetwork = session.Ixnetwork
    
        ixNetwork.NewConfig()

        ixNetwork.Globals.Licensing.LicensingServers = module.params['licenseServerIp']
        ixNetwork.Globals.Licensing.Mode = module.params['licenseMode']
        ixNetwork.Globals.Licensing.Tier =  module.params['licenseTier']

        # Create vports and name them so you could get the vports by the name when creating Topology.
        vport1 = ixNetwork.Vport.add(Name='Port1')
        vport2 = ixNetwork.Vport.add(Name='Port2')

        # Assign ports
        testPorts = []
        vportList = [vport.href for vport in ixNetwork.Vport.find()]
        for port in module.params['portList']:
            testPorts.append(dict(Arg1=port[0], Arg2=port[1], Arg3=port[2]))
            
        ixNetwork.AssignPorts(testPorts, [], vportList, module.params['forceTakePortOwnership'])

        ixNetwork.info('Creating Topology Group 1')
        topology1 = ixNetwork.Topology.add(Name='Topology 1', Ports=vport1)
        deviceGroup1 = topology1.DeviceGroup.add(Name='DG1', Multiplier='1')
        ethernet1 = deviceGroup1.Ethernet.add(Name='Eth1')
        ethernet1.Mac.Increment(start_value='00:01:01:01:00:01', step_value='00:00:00:00:00:01')
        ethernet1.EnableVlans.Single(True)
        
        ixNetwork.info('Configuring vlanID')
        vlanObj = ethernet1.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)
        
        ixNetwork.info('Configuring IPv4')
        ipv4 = ethernet1.Ipv4.add(Name='Ipv4')
        ipv4.Address.Increment(start_value='1.1.1.1', step_value='0.0.0.1')
        ipv4.GatewayIp.Increment(start_value='1.1.1.2', step_value='0.0.0.0')
        
        ixNetwork.info('Configuring BgpIpv4Peer 1')
        bgp1 = ipv4.BgpIpv4Peer.add(Name='Bgp1')
        bgp1.DutIp.Increment(start_value='1.1.1.2', step_value='0.0.0.0')
        bgp1.Type.Single('internal')
        bgp1.LocalAs2Bytes.Increment(start_value=101, step_value=0)
        
        ixNetwork.info('Configuring Network Group 1')
        networkGroup1 = deviceGroup1.NetworkGroup.add(Name='BGP-Routes1', Multiplier='100')
        ipv4PrefixPool = networkGroup1.Ipv4PrefixPools.add(NumberOfAddresses='1')
        ipv4PrefixPool.NetworkAddress.Increment(start_value='10.10.0.1', step_value='0.0.0.1')
        ipv4PrefixPool.PrefixLength.Single(32)        
        
        topology2 = ixNetwork.Topology.add(Name='Topology 2', Ports=vport2)
        deviceGroup2 = topology2.DeviceGroup.add(Name='DG2', Multiplier='1')
        
        ethernet2 = deviceGroup2.Ethernet.add(Name='Eth2')
        ethernet2.Mac.Increment(start_value='00:01:01:02:00:01', step_value='00:00:00:00:00:01')
        ethernet2.EnableVlans.Single(True)
        
        ixNetwork.info('Configuring vlanID')
        vlanObj = ethernet2.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)
        
        ixNetwork.info('Configuring IPv4 2')
        ipv4 = ethernet2.Ipv4.add(Name='Ipv4-2')
        ipv4.Address.Increment(start_value='1.1.1.2', step_value='0.0.0.1')
        ipv4.GatewayIp.Increment(start_value='1.1.1.1', step_value='0.0.0.0')
        
        ixNetwork.info('Configuring BgpIpv4Peer 2')
        bgp2 = ipv4.BgpIpv4Peer.add(Name='Bgp2')
        bgp2.DutIp.Increment(start_value='1.1.1.1', step_value='0.0.0.0')
        bgp2.Type.Single('internal')
        bgp2.LocalAs2Bytes.Increment(start_value=101, step_value=0)
        
        ixNetwork.info('Configuring Network Group 2')
        networkGroup2 = deviceGroup2.NetworkGroup.add(Name='BGP-Routes2', Multiplier='100')
        ipv4PrefixPool = networkGroup2.Ipv4PrefixPools.add(NumberOfAddresses='1')
        ipv4PrefixPool.NetworkAddress.Increment(start_value='20.20.0.1', step_value='0.0.0.1')
        ipv4PrefixPool.PrefixLength.Single(32)
        
        ixNetwork.StartAllProtocols(Arg1='sync')
        
        ixNetwork.info('Verify protocol sessions\n')
        protocolsSummary = StatViewAssistant(ixNetwork, 'Protocols Summary')
        protocolsSummary.CheckCondition('Sessions Not Started', StatViewAssistant.EQUAL, 0)
        protocolsSummary.CheckCondition('Sessions Down', StatViewAssistant.EQUAL, 0)
        ixNetwork.info(protocolsSummary)
        
        ixNetwork.info('Create Traffic Item')
        trafficItem = ixNetwork.Traffic.TrafficItem.add(Name='BGP Traffic', BiDirectional=False, TrafficType='ipv4')
        
        ixNetwork.info('Add endpoint flow group')
        trafficItem.EndpointSet.add(Sources=topology1, Destinations=topology2)
        
        # Note: A Traffic Item could have multiple EndpointSets (Flow groups).
        #       Therefore, ConfigElement is a list.
        ixNetwork.info('Configuring config elements')
        configElement = trafficItem.ConfigElement.find()[0]
        configElement.FrameRate.Rate = 28
        configElement.FrameRate.Type = 'framesPerSecond'
        configElement.TransmissionControl.FrameCount = 10000
        configElement.TransmissionControl.Type = 'fixedFrameCount'
        configElement.FrameRateDistribution.PortDistribution = 'splitRateEvenly'
        configElement.FrameSize.FixedSize = 128
        trafficItem.Tracking.find()[0].TrackBy = ['flowGroup0']
        
        trafficItem.Generate()
        ixNetwork.Traffic.Apply()
        ixNetwork.Traffic.Start()

        # StatViewAssistant could also filter by REGEX, LESS_THAN, GREATER_THAN, EQUAL. 
        # Examples:
        #    flowStatistics.AddRowFilter('Port Name', StatViewAssistant.REGEX, '^Port 1$')
        #    flowStatistics.AddRowFilter('Tx Frames', StatViewAssistant.LESS_THAN, 50000)
        
        flowStatistics = StatViewAssistant(ixNetwork, 'Flow Statistics')
        ixNetwork.info('{}\n'.format(flowStatistics))
        
        for rowNumber,flowStat in enumerate(flowStatistics.Rows):
            ixNetwork.info('\n\nSTATS: {}\n\n'.format(flowStat))
            ixNetwork.info('\nRow:{}  TxPort:{}  RxPort:{}  TxFrames:{}  RxFrames:{}\n'.format(
                rowNumber, flowStat['Tx Port'], flowStat['Rx Port'],
                flowStat['Tx Frames'], flowStat['Rx Frames']))

        flowStatistics = StatViewAssistant(ixNetwork, 'Traffic Item Statistics')
        ixNetwork.info('{}\n'.format(flowStatistics))

        if module.params['debugMode'] == False:
            # For linux and connection_manager only
            session.remove()

        result['result'] = 'Passed'
        module.exit_json(**result)

    except Exception as errMsg:
        module.fail_json(result='Failed', msg=errMsg)

        if module.params['debugMode'] == False and 'session' in locals():
            session.remove()

if __name__ == '__main__':
   main()
 

