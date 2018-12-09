#!/usr/local/python3.7.0/bin/python3.7

# Ansible doc style
DOCUMENTATION = '''
---
module: bgpNgpf

description:
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

author: Hubert Gee
'''

from ansible.module_utils.basic import AnsibleModule

import os, sys, traceback, logging

# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform

# This sample script uses helper functions from the ../../RestPy/Modules directory: StatisticsMgmt.py and PortMgmt.py
# Since sys.path.append() doesn't work in a an Ansible custom module, these two helper modules are 
# copied to the ../Playbook/RestPyHelperModules directory, relative path from this file.
from RestPyHelperModules.StatisticsMgmt import Statistics
from RestPyHelperModules.PortMgmt import Ports

def main():
    logging.basicConfig(filename='../ansible.log', level=logging.DEBUG)

    # Define the available arguments/parameters that a user can pass to this module.
    params = {
        'osPlatform':             {'type':'str', 'required':False, 'default':'windows',
                                   'choices':['windows', 'windowsConnectionMgr', 'linux']},
        'forceTakePortOwnership': {'type':'bool', 'required':False, 'default':True},
        'deleteSessionWhenDone':  {'type':'bool', 'required':False, 'default':True},
        'portList':               {'type':'list', 'required':True, 'default':None},
        'apiServerIp':            {'type':'str', 'required':True, 'default':None},
        'apiServerIpPort':        {'type':'int', 'required':False, 'default':11009},
        'linuxUsername':          {'type':'str', 'required':False, 'default':'admin', 'no_log':False},
        'linuxPassword':          {'type':'str', 'required':False, 'default':'admin', 'no_log':False},
        'licenseServerIp':        {'type':'list', 'required':True, 'default':None},
        'licenseMode':            {'type':'str', 'required':True, 'default':None},
        'restPyLog':              {'type':'str', 'required':False, 'default':'restpy.log'},

        'port1Name':              {'type':'str', 'required':False, 'default':'Port1'},
        'port2Name':              {'type':'str', 'required':False, 'default':'Port2'},

        'topologyGroup1Name':     {'type':'str', 'required':False, 'default':'Topo1'},
        'topologyGroup1Ports':    {'type':'list', 'required':True, 'default':None},
        'topologyGroup2Name':     {'type':'str', 'required':False, 'default':'Topo2'},
        'topologyGroup2Ports':    {'type':'list', 'required':True, 'default':None},
        'deviceGroup1Name':       {'type':'str', 'required':False, 'default':None},
        'deviceGroup1Multiplier': {'type':'int', 'required':False, 'default':1},
        'deviceGroup2Name':       {'type':'str', 'required':False, 'default':None},
        'deviceGroup2Multiplier': {'type':'int', 'required':False, 'default':1},

	'ethernet1Name':         {'type':'str', 'required':False, 'default':None},
	'ethernet1MacAddress':   {'type':'str', 'required':False, 'default':None},
	'ethernet1MacStep':      {'type':'str', 'required':False, 'default':'00:00:00:00:00:00'},
	'ethernet1MacPortStep':  {'type':'str', 'required':True, 'default':None},
        'ethernet1VlanEnabled':  {'type':'bool', 'required':False, 'default':False},
	'ethernet1VlanId':       {'type':'int', 'required':True, 'default':None},
	'ethernet1VlanIdStep':   {'type':'int', 'required':True, 'default':None},

	'ethernet2Name':         {'type':'str', 'required':False, 'default':None},
	'ethernet2MacAddress':   {'type':'str', 'required':False, 'default':None},
	'ethernet2MacStep':      {'type':'str', 'required':False, 'default':'00:00:00:00:00:00'},
	'ethernet2MacPortStep':  {'type':'str', 'required':False, 'default':None},
        'ethernet2VlanEnabled':  {'type':'bool', 'required':False, 'default':False},
	'ethernet2VlanId':       {'type':'int', 'required':True, 'default':None},
	'ethernet2VlanIdStep':   {'type':'str', 'required':True, 'default':None},

	'ipv41Name':             {'type':'str', 'required':False, 'default':'IPv4-1'},
	'ipv41Address':          {'type':'str', 'required':True, 'default':None},
	'ipv41AddressStep':      {'type':'str', 'required':True, 'default':None},
	'ipv41AddressPortStep':  {'type':'str', 'required':True, 'default':None},
	'ipv41Gateway':          {'type':'str', 'required':True, 'default':None},
	'ipv41GatewayStep':      {'type':'str', 'required':True, 'default':None},
	'ipv41GatewayPortStep':  {'type':'str', 'required':True, 'default':None},
	'ipv41AddressPrefix':    {'type':'int', 'required':True, 'default':None},
	'ipv41ResolveGateway':   {'type':'bool', 'required':False, 'default':True},

	'ipv42Name':             {'type':'str', 'required':False, 'default':'IPv4-2'},
	'ipv42Address':          {'type':'str', 'required':True, 'default':None},
	'ipv42AddressStep':      {'type':'str', 'required':True, 'default':None},
	'ipv42AddressPortStep':  {'type':'str', 'required':True, 'default':None},
	'ipv42Gateway':          {'type':'str', 'required':True, 'default':None},
	'ipv42GatewayStep':      {'type':'str', 'required':True, 'default':None},
	'ipv42GatewayPortStep':  {'type':'str', 'required':True, 'default':None},
	'ipv42AddressPrefix':    {'type':'int', 'required':True, 'default':None},
	'ipv42ResolveGateway':   {'type':'bool', 'required':False, 'default':True},

	'bgp1Name':              {'type':'str', 'required':True, 'default':None},
	'bgp1HoldTimer':         {'type':'int', 'required':True, 'default':None},
	'bgp1DutIp':             {'type':'str', 'required':True, 'default':None},
	'bgp1DutIpStep':         {'type':'str', 'required':True, 'default':None},
	'bgp1LocalAsBytes':      {'type':'int', 'required':True, 'default':None},
	'bgp1LocalAsBytesStep':      {'type':'int', 'required':False, 'default':0},
	'bgp1Type':                  {'type':'str', 'required':True, 'default':None},

	'bgp2Name':                  {'type':'str', 'required':True, 'default':None},
	'bgp2HoldTimer':             {'type':'str', 'required':True, 'default':None},
	'bgp2DutIp':                 {'type':'str', 'required':True, 'default':None},
	'bgp2DutIpStep':             {'type':'str', 'required':True, 'default':None},
	'bgp2LocalAsBytes':          {'type':'int', 'required':True, 'default':None},
	'bgp2LocalAsBytesStep':      {'type':'int', 'required':False, 'default':0},
	'bgp2Type':                  {'type':'str', 'required':True, 'default':None},

        'networkGroup1Name':        {'type':'str', 'required':True, 'default':None}, 
	'networkGroup1Multiplier':  {'type':'int', 'required':False, 'default':100},
	'networkGroup1NumberOfAddresses':  {'type':'int', 'required':False, 'default':100},
	'networkGroup1Address':     {'type':'str', 'required':True, 'default':None},
	'networkGroup1AddressStep': {'type':'str', 'required':True, 'default':None},
	'networkGroup1PrefixLength':{'type':'int', 'required':True, 'default':None},

        'networkGroup2Name':        {'type':'str', 'required':True, 'default':None}, 
	'networkGroup2Multiplier':  {'type':'int', 'required':False, 'default':100},
	'networkGroup2NumberOfAddresses':  {'type':'int', 'required':False, 'default':100},
	'networkGroup2Address':     {'type':'str', 'required':True, 'default':None},
	'networkGroup2AddressStep': {'type':'str', 'required':True, 'default':None},
	'networkGroup2PrefixLength':{'type':'int', 'required':True, 'default':None},

        'trafficItemName':        {'type':'str', 'required':True, 'default':None},
	'trafficItemType':        {'type':'str', 'required':False, 'default':'ipv4',
                                   'choices':['raw', 'ipv4', 'ethernetVlan', 'frameRelay', 'atm', 'fcoe', 'fc', 'hdlc', 'ppp']},
	'trafficItemBiDirection': {'type':'bool', 'required':False, 'default':False},
	'portDistribution':       {'type':'str', 'required':False, 'default':'splitRateEvenly',
                                   'choices':['splitRateEvenly', 'applyRateToAll']},
	'trafficItemTrackBy':     {'type':'list', 'required':False, 'default': ['flowGroup0'],
                                   'choices':['vlanVlanId0', 'trackingenabled0', 'ethernetIiDestinationaddress0', 'ethernetIiSourceaddress0',
                                   'sourcePort0', 'sourceDestPortPair0', 'ipv4DestIp0', 'ipv4SourceIp0', 'ipv4Precedence0',
                                              'ethernetIiPfcQueue0', 'frameSize0', 'flowGroup0']},
	'endpointName':     {'type':'str', 'required':True, 'default':None},
	'transmissionType': {'type':'str', 'required':False, 'default':'fixedFrameCount',
                             'choices':['continuous', 'fixedFrameCount', 'fixedDuration']},
	'frameCount':       {'type':'int', 'required':False, 'default':50000},
	'frameRate':        {'type':'int', 'required':False, 'default':100},
	'frameRateType':    {'type':'str', 'required':False, 'default':'percentLineRate',
                             'choices':['percentLineRate', 'bitsPerSecond', 'framesPerSecond', 'interPacketGap']},
	'frameSize':        {'type':'int', 'required':False, 'default':64},
    }

    module = AnsibleModule(argument_spec=params, supports_check_mode=False)

    if module.params['osPlatform'] not in ['windows', 'windowsConnectionMgr', 'linux']:
        raise Exception("\nError: %s is not a known option. Choices are windows, windowsConnectionMgr or linux." % module.params['osPlatform'])
        
    if module.params['osPlatform'] == 'windowsConnectionMgr':
        osPlatform = 'windows'
    else:
        osPlatform = module.params['osPlatform']

    try:
        testPlatform = TestPlatform(ip_address=module.params['apiServerIp'],
                                    rest_port=module.params['apiServerIpPort'],
                                    platform=osPlatform,
                                    log_file_name=module.params['restPyLog'])

        # Console output verbosity: None|request|'request response'
        testPlatform.Trace = 'request_response'

        if osPlatform == 'linux':
            testPlatform.Authenticate(module.params['linuxUsername'], module.params['linuxPassword'])

        session = testPlatform.Sessions.add()
        ixNetwork = session.Ixnetwork

        # Instantiate some helper class objects
        statObj = Statistics(ixNetwork)
        portObj = Ports(ixNetwork)

        if osPlatform == 'windows':
            ixNetwork.NewConfig()

        ixNetwork.Globals.Licensing.LicensingServers = module.params['licenseServerIp']
        ixNetwork.Globals.Licensing.Mode = module.params['licenseMode']

        # Create vports and name them so you could get the vports by the name when creating Topology.
        vport1 = ixNetwork.Vport.add(Name=module.params['port1Name'])
        vport2 = ixNetwork.Vport.add(Name=module.params['port2Name'])

        # getVportList=True because you already created vports.
        # If you did not create vports, then assignPorts will create them and name them with default names.
        portObj.assignPorts(module.params['portList'], module.params['forceTakePortOwnership'], getVportList=True)

        topology1 = ixNetwork.Topology.add(Name=module.params['topologyGroup1Name'], Ports=vport1)
        deviceGroup1 = topology1.DeviceGroup.add(Name=module.params['deviceGroup1Name'], Multiplier=module.params['deviceGroup1Multiplier'])
        ethernet1 = deviceGroup1.Ethernet.add(Name=module.params['ethernet1Name'])
        ethernet1.Mac.Increment(start_value=module.params['ethernet1MacAddress'], step_value=module.params['ethernet1MacStep'])
        ethernet1.EnableVlans.Single(module.params['ethernet1VlanEnabled'])

        vlanObj = ethernet1.Vlan.find()[0].VlanId.Increment(start_value=module.params['ethernet1VlanId'],
                                                            step_value=module.params['ethernet1VlanIdStep'])

        ipv4 = ethernet1.Ipv4.add(Name=module.params['ipv41Name'])
        ipv4.Address.Increment(start_value=module.params['ipv41Address'], step_value=module.params['ipv41AddressStep'])
        ipv4.GatewayIp.Increment(start_value=module.params['ipv41Gateway'], step_value=module.params['ipv41GatewayStep'])

        bgp1 = ipv4.BgpIpv4Peer.add(Name=module.params['bgp1Name'])
        bgp1.DutIp.Increment(start_value=module.params['bgp1DutIp'], step_value=module.params['bgp1DutIpStep'])
        bgp1.Type.Single(module.params['bgp1Type'])
        bgp1.LocalAs2Bytes.Increment(start_value=module.params['bgp1LocalAsBytes'], step_value=module.params['bgp1LocalAsBytesStep'])

        networkGroup1 = deviceGroup1.NetworkGroup.add(Name=module.params['networkGroup1Name'], Multiplier=module.params['networkGroup1Multiplier'])
        ipv4PrefixPool = networkGroup1.Ipv4PrefixPools.add(NumberOfAddresses=module.params['networkGroup1NumberOfAddresses'])
        ipv4PrefixPool.NetworkAddress.Increment(start_value=module.params['networkGroup1Address'],
                                                step_value=module.params['networkGroup1AddressStep'])
        ipv4PrefixPool.PrefixLength.Single(module.params['networkGroup1PrefixLength'])


        topology2 = ixNetwork.Topology.add(Name=module.params['topologyGroup2Name'], Ports=vport2)
        deviceGroup2 = topology2.DeviceGroup.add(Name=module.params['deviceGroup2Name'], Multiplier=module.params['deviceGroup2Multiplier'])
        ethernet2 = deviceGroup2.Ethernet.add(Name=module.params['ethernet2Name'])
        ethernet2.Mac.Increment(start_value=module.params['ethernet2MacAddress'], step_value=module.params['ethernet2MacStep'])
        ethernet2.EnableVlans.Single(module.params['ethernet2VlanEnabled'])

        vlanObj = ethernet2.Vlan.find()[0].VlanId.Increment(start_value=module.params['ethernet2VlanId'],
                                                            step_value=module.params['ethernet2VlanIdStep'])

        ipv4 = ethernet2.Ipv4.add(Name=module.params['ipv42Name'])
        ipv4.Address.Increment(start_value=module.params['ipv42Address'], step_value=module.params['ipv42AddressStep'])
        ipv4.GatewayIp.Increment(start_value=module.params['ipv42Gateway'], step_value=module.params['ipv42GatewayStep'])

        bgp2 = ipv4.BgpIpv4Peer.add(Name=module.params['bgp2Name'])
        bgp2.DutIp.Increment(start_value=module.params['bgp2DutIp'], step_value=module.params['bgp2DutIpStep'])
        bgp2.Type.Single(module.params['bgp2Type'])
        bgp2.LocalAs2Bytes.Increment(start_value=module.params['bgp2LocalAsBytes'], step_value=module.params['bgp2LocalAsBytesStep'])

        networkGroup2 = deviceGroup2.NetworkGroup.add(Name=module.params['networkGroup2Name'], Multiplier=module.params['networkGroup2Multiplier'])
        ipv4PrefixPool = networkGroup2.Ipv4PrefixPools.add(NumberOfAddresses=module.params['networkGroup2NumberOfAddresses'])
        ipv4PrefixPool.NetworkAddress.Increment(start_value=module.params['networkGroup2Address'],
                                                step_value=module.params['networkGroup2AddressStep'])
        ipv4PrefixPool.PrefixLength.Single(module.params['networkGroup2PrefixLength'])

        ixNetwork.StartAllProtocols(Arg1='sync')
        statObj.verifyAllProtocolSessions()

        trafficItem = ixNetwork.Traffic.TrafficItem.add(Name=module.params['trafficItemName'],
                                                        BiDirectional=module.params['trafficItemBiDirection'],
                                                        TrafficType=module.params['trafficItemType'])

        trafficItem.EndpointSet.add(Sources=topology1, Destinations=topology2)

        # Note: A Traffic Item could have multiple EndpointSets (Flow groups).
        #       Therefore, ConfigElement is a list.
        configElement = trafficItem.ConfigElement.find()[0]
        configElement.FrameRate.Rate = module.params['frameRate']
        configElement.FrameRate.Type = module.params['frameRateType']
        configElement.TransmissionControl.FrameCount = module.params['frameCount']
        configElement.TransmissionControl.Type = module.params['transmissionType']
        configElement.FrameRateDistribution.PortDistribution = module.params['portDistribution']
        configElement.FrameSize.FixedSize = module.params['frameSize']
        trafficItem.Tracking.find()[0].TrackBy = module.params['trafficItemTrackBy']

        trafficItem.Generate()
        ixNetwork.Traffic.Apply()
        ixNetwork.Traffic.Start()

        stats = statObj.getTrafficItemStats()

        # Get the statistic values with the indexes.
        txFrames = stats[trafficItem.Name]['Tx Frames']
        rxFrames = stats[trafficItem.Name]['Rx Frames']

        if rxFrames != txFrames:
            module.fail_json(msg='txFrames={}  rxFrames={}'.format(txFrames, rxFrames))

        # This example is for getting Flow Statistics.
        stats = statObj.getFlowStatistics()

        for row, statValues in stats.items():
            txFrames = statValues['Tx Frames']
            rxFrames = statValues['Rx Frames']

            if txFrames != rxFrames:
                module.fail_json(msg="FlowStatictics failed: {} != {}".format(txFrames, rxFrames))

        if module.params['deleteSessionWhenDone']:
            if osPlatform in ['linux', 'windowsConnectionMgr']:
                session.remove()

        module.exit_json(changed=True, BGP_Configuration='Passed')

    except Exception as errMsg:
        #module.fail_json(msg=errMsg, **result)
        module.fail_json(msg=errMsg)
        module.fail_json(changed=True, meta=traceback.format_exc())

        loging.ERROR('\nRestPy.Exception: {}'.format(errMsg))
        if module.params['deleteSessionWhenDone'] and 'session' in locals():
            if osPlatform in ['linux', 'windowsConnectionMgr']:
                session.remove()

if __name__ == '__main__':
    main()
