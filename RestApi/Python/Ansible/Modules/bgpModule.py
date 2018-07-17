"""
Description
    A sample custom module for configuring BGP.

By: Hubert Gee

"""

import logging
from ansible.module_utils.basic import AnsibleModule

import sys, traceback

sys.path.insert(0, '../Modules')
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiTraffic import Traffic
from IxNetRestApiProtocol import Protocol
from IxNetRestApiStatistics import Statistics

def main():
    logging.basicConfig(filename='../ansible.log', level=logging.DEBUG)

    # Define the available arguments/parameters that a user can pass to this module.
    params = {
        'osPlatform':             {'type':'str', 'required':False, 'default':'windows',
                                   'choices':['windows', 'windowsConnectionMgr', 'linux']},
        'forceTakePortOwnership': {'type':'bool', 'required':False, 'default':True},
        'releasePortsWhenDone':   {'type':'bool', 'required':False, 'default':False},
        'enableDebugTracing':     {'type':'bool', 'required':False, 'default':True},
        'deleteSessionAfterTest': {'type':'bool', 'required':False, 'default':True},
        'ixChassisIp':            {'type':'str', 'required':True, 'default':None},
        'portList':               {'type':'list', 'required':True, 'default':None},
        'apiServerIp':            {'type':'str', 'required':True, 'default':None},
        'apiServerIpPort':        {'type':'int', 'required':False, 'default':11009},
        'configLicense':          {'type':'str', 'required':False, 'default':'True', 'no_log':False},
        'linuxUsername':          {'type':'str', 'required':False, 'default':'admin', 'no_log':False},
        'linuxPassword':          {'type':'str', 'required':False, 'default':'password', 'no_log':False},
        'licenseServerIp':        {'type':'str', 'required':True, 'default':None},
        'licenseMode':            {'type':'str', 'required':False, 'default':'subscription'},
        'licenseTier':            {'type':'str', 'required':False, 'default':'tier3'},

        'topologyGroup1Name':     {'type':'str', 'required':True, 'default':None},
        'topologyGroup1Ports':    {'type':'list', 'required':True, 'default':None},
        'topologyGroup2Name':     {'type':'str', 'required':True, 'default':None},
        'topologyGroup2Ports':    {'type':'list', 'required':True, 'default':None},
        'deviceGroup1Name':       {'type':'str', 'required':True, 'default':None},
        'deviceGroup1Multiplier': {'type':'int', 'required':False, 'default':1},
        'deviceGroup2Name':       {'type':'str', 'required':True, 'default':None},
        'deviceGroup2Multiplier': {'type':'int', 'required':False, 'default':1},

	'ethernet1Name':         {'type':'str', 'required':True, 'default':None},
	'ethernet1MacAddress':   {'type':'str', 'required':True, 'default':None},
	'ethernet1MacDirection': {'type':'str', 'required':True, 'default':None},
	'ethernet1MacStep':      {'type':'str', 'required':True, 'default':None},
	'ethernet1MacPortStep':  {'type':'str', 'required':True, 'default':None},
	'ethernet1VlanId':       {'type':'int', 'required':True, 'default':None},
	'ethernet1VlanIdDirection': {'type':'str', 'required':True, 'default':None},
	'ethernet1VlanIdStep':      {'type':'str', 'required':True, 'default':None},

	'ethernet2Name':         {'type':'str', 'required':True, 'default':None},
	'ethernet2MacAddress':   {'type':'str', 'required':True, 'default':None},
	'ethernet2MacDirection': {'type':'str', 'required':True, 'default':None},
	'ethernet2MacStep':      {'type':'str', 'required':True, 'default':None},
	'ethernet2MacPortStep':  {'type':'str', 'required':True, 'default':None},
	'ethernet2VlanId':       {'type':'int', 'required':True, 'default':None},
	'ethernet2VlanIdDirection': {'type':'str', 'required':True, 'default':None},
	'ethernet2VlanIdStep':      {'type':'str', 'required':True, 'default':None},

	'ipv41Address':          {'type':'str', 'required':True, 'default':None},
	'ipv41AddressDirection': {'type':'str', 'required':True, 'default':None},
	'ipv41AddressStep':      {'type':'str', 'required':True, 'default':None},
	'ipv41AddressPortStep':  {'type':'str', 'required':True, 'default':None},
	'ipv41Gateway':          {'type':'str', 'required':True, 'default':None},
	'ipv41GatewayDirection': {'type':'str', 'required':True, 'default':None},
	'ipv41GatewayStep':      {'type':'str', 'required':True, 'default':None},
	'ipv41GatewayPortStep':  {'type':'str', 'required':True, 'default':None},
	'ipv41AddressPrefix':    {'type':'str', 'required':True, 'default':None},
	'ipv41ResolveGateway':   {'type':'str', 'required':True, 'default':None},

	'ipv42Address':          {'type':'str', 'required':True, 'default':None},
	'ipv42AddressDirection': {'type':'str', 'required':True, 'default':None},
	'ipv42AddressStep':      {'type':'str', 'required':True, 'default':None},
	'ipv42AddressPortStep':  {'type':'str', 'required':True, 'default':None},
	'ipv42Gateway':          {'type':'str', 'required':True, 'default':None},
	'ipv42GatewayDirection': {'type':'str', 'required':True, 'default':None},
	'ipv42GatewayStep':      {'type':'str', 'required':True, 'default':None},
	'ipv42GatewayPortStep':  {'type':'str', 'required':True, 'default':None},
	'ipv42AddressPrefix':    {'type':'str', 'required':True, 'default':None},
	'ipv42ResolveGateway':   {'type':'str', 'required':True, 'default':None},

	'bgp1Name':      {'type':'str', 'required':True, 'default':None},
	'bgp1Enable':    {'type':'str', 'required':True, 'default':None}, 
	'bgp1HoldTimer': {'type':'str', 'required':True, 'default':None},
	'bgp1DutIp':     {'type':'str', 'required':True, 'default':None},
	'bgp1DutIpDirection': {'type':'str', 'required':True, 'default':None},
	'bgp1DutIpStep':      {'type':'str', 'required':True, 'default':None},
	'bgp1LocalAsBytes':   {'type':'str', 'required':True, 'default':None},
	'bgp1EnableGracefulRestart': {'type':'str', 'required':True, 'default':None},
	'bgp1RestartTime':           {'type':'str', 'required':True, 'default':None},
	'bgp1Type':                  {'type':'str', 'required':True, 'default':None},

	'bgp2Name':      {'type':'str', 'required':True, 'default':None},
	'bgp2Enable':    {'type':'str', 'required':True, 'default':None}, 
	'bgp2HoldTimer': {'type':'str', 'required':True, 'default':None},
	'bgp2DutIp':     {'type':'str', 'required':True, 'default':None},
	'bgp2DutIpDirection': {'type':'str', 'required':True, 'default':None},
	'bgp2DutIpStep':      {'type':'str', 'required':True, 'default':None},
	'bgp2LocalAsBytes':   {'type':'str', 'required':True, 'default':None},
	'bgp2EnableGracefulRestart': {'type':'str', 'required':True, 'default':None},
	'bgp2RestartTime':           {'type':'str', 'required':True, 'default':None},
	'bgp2Type':                  {'type':'str', 'required':True, 'default':None},

        'networkGroup1Name':        {'type':'str', 'required':True, 'default':None}, 
	'networkGroup1Multiplier':  {'type':'int', 'required':True, 'default':None},
	'networkGroup1Address':     {'type':'str', 'required':True, 'default':None},
	'networkGroup1AddressStep': {'type':'str', 'required':True, 'default':None},
	'networkGroup1AddressDirection': {'type':'str', 'required':True, 'default':None},
	'networkGroup1PrefixLength':     {'type':'int', 'required':True, 'default':None},

        'networkGroup2Name':        {'type':'str', 'required':True, 'default':None}, 
	'networkGroup2Multiplier':  {'type':'int', 'required':True, 'default':None},
	'networkGroup2Address':     {'type':'str', 'required':True, 'default':None},
	'networkGroup2AddressStep': {'type':'str', 'required':True, 'default':None},
	'networkGroup2AddressDirection': {'type':'str', 'required':True, 'default':None},
	'networkGroup2PrefixLength':     {'type':'int', 'required':True, 'default':None},

        'trafficItemName':        {'type':'str', 'required':True, 'default':None},
	'trafficItemType':        {'type':'str', 'required':True, 'default':None},
	'trafficItemBiDirection': {'type':'str', 'required':True, 'default':None},
	'trafficItemSrcDestMesh': {'type':'str', 'required':True, 'default':None},
	'trafficItemRouteMesh':   {'type':'str', 'required':True, 'default':None},
	'trafficItemAllowSelfDestined': {'type':'str', 'required':True, 'default':None},
	'trafficItemTrackBy':           {'type':'list', 'required':True, 'default':None},
	'endpointName':     {'type':'str', 'required':True, 'default':None},
	'transmissionType': {'type':'str', 'required':True, 'default':None},
	'frameCount':       {'type':'str', 'required':True, 'default':None},
	'frameRate':        {'type':'str', 'required':True, 'default':None},
	'frameRateType':    {'type':'str', 'required':True, 'default':None},
	'frameSize':        {'type':'str', 'required':True, 'default':None},
    }

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec = params,
        supports_check_mode = False
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    #if module.check_mode:
    #    return result

    module.params['name'] = 'Custom Ansible  module for BGP configuration'
    result['Result'] = 'Passed'

    # Default the API server to either windows or linux.
    osPlatform = module.params['osPlatform']

    if module.params['osPlatform'] not in ['windows', 'windowsConnectionMgr', 'linux']:
        raise IxNetRestApiException("\nError: %s is not a known option. Choices are 'windows' or 'linux'." % module.params['osPlatform'])
        
    try:
        #---------- Preference Settings --------------

        forceTakePortOwnership = module.params['forceTakePortOwnership']
        releasePortsWhenDone = module.params['releasePortsWhenDone']
        enableDebugTracing = module.params['enableDebugTracing']
        deleteSessionAfterTest = module.params['deleteSessionAfterTest'] ;# For Windows Connection Mgr and Linux API server only
              
        ixChassisIp = module.params['ixChassisIp']
        # [chassisIp, cardNumber, slotNumber]
        portList = module.params['portList']

        if module.params['osPlatform'] == 'linux':
              mainObj = Connect(apiServerIp = module.params['apiServerIp'],
                                serverIpPort = module.params['apiSeverIpPort'],
                                username = module.params['linuxUsername'],
                                password = module.params['linuxPassword'],
                                deleteSessionAfterTest = module.params['deleteSessionAfterTest'],
                                verifySslCert = False,
                                serverOs = module.params['osPlatform']
                            )
            
        if module.params['osPlatform'] in ['windows', 'windowsConnectionMgr']:
              mainObj = Connect(apiServerIp = module.params['apiServerIp'],
                                serverIpPort = module.params['apiServerIpPort'],
                                serverOs = module.params['osPlatform'],
                                deleteSessionAfterTest = module.params['deleteSessionAfterTest']
                            )

        #---------- Preference Settings End --------------

        portObj = PortMgmt(mainObj)
        portObj.connectIxChassis(module.params['ixChassisIp'])

        if portObj.arePortsAvailable(module.params['portList'], raiseException=False) != 0:
            if module.params['forceTakePortOwnership'] == True:
                portObj.releasePorts(module.params['portList'])
                portObj.clearPortOwnership(module.params['portList'])
            else:
                raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')

        mainObj.newBlankConfig()

        if module.params['configLicense'] == True:
            portObj.releaseAllPorts()
            mainObj.configLicenseServerDetails([module.params['licenseServerIp']],
                                               module.params['licenseMode'], module.params['licenseTier'])
            
        # Set createVports = True if building config from scratch.
        portObj.assignPorts(module.params['portList'])

        protocolObj = Protocol(mainObj)
        topologyObj1 = protocolObj.createTopologyNgpf(portList = [module.params['topologyGroup1Ports']],
                                                      topologyName = module.params['topologyGroup1Name'])

        deviceGroupObj1 = protocolObj.createDeviceGroupNgpf(topologyObj1,
                                                            multiplier=module.params['deviceGroup1Multiplier'],
                                                            deviceGroupName=module.params['deviceGroup1Name'])

        topologyObj2 = protocolObj.createTopologyNgpf(portList=[module.params['topologyGroup2Ports']],
                                                      topologyName=module.params['topologyGroup2Name'])

        deviceGroupObj2 = protocolObj.createDeviceGroupNgpf(topologyObj2,
                                                            multiplier=module.params['deviceGroup2Multiplier'],
                                                            deviceGroupName=module.params['deviceGroup2Name'])

        ethernetObj1 = protocolObj.configEthernetNgpf(deviceGroupObj1,
                                                      ethernetName=module.params['ethernet1Name'],
                                                      macAddress={'start': module.params['ethernet1MacAddress'],
                                                                  'direction': module.params['ethernet1MacDirection'],
                                                                  'step': module.params['ethernet1MacStep']},
                                                      macAddressPortStep=module.params['ethernet1MacPortStep'],
                                                      vlanId={'start': module.params['ethernet1VlanId'],
                                                              'direction': module.params['ethernet1VlanIdDirection'],
                                                              'step':module.params['ethernet1VlanIdStep']})

        ethernetObj2 = protocolObj.configEthernetNgpf(deviceGroupObj2,
                                                      ethernetName=module.params['ethernet2Name'],
                                                      macAddress={'start': module.params['ethernet2MacAddress'],
                                                                  'direction': module.params['ethernet2MacDirection'],
                                                                  'step': module.params['ethernet2MacStep']},
                                                      macAddressPortStep=module.params['ethernet2MacPortStep'],
                                                      vlanId={'start': module.params['ethernet2VlanId'],
                                                              'direction': module.params['ethernet2VlanIdDirection'],
                                                              'step': module.params['ethernet2VlanIdStep']})

        ipv4Obj1 = protocolObj.configIpv4Ngpf(ethernetObj1,
                                              ipv4Address={'start': module.params['ipv41Address'],
                                                           'direction': module.params['ipv41AddressDirection'],
                                                           'step': module.params['ipv41AddressStep']},
                                              ipv4AddressPortStep = module.params['ipv41AddressPortStep'],
                                              gateway={'start': module.params['ipv41Gateway'],
                                                       'direction': module.params['ipv41GatewayDirection'],
                                                       'step': module.params['ipv41GatewayStep']},
                                              gatewayPortStep = module.params['ipv41GatewayPortStep'],
                                              prefix = module.params['ipv41AddressPrefix'],
                                              resolveGateway = module.params['ipv41ResolveGateway'])

        ipv4Obj2 = protocolObj.configIpv4Ngpf(ethernetObj2,
                                              ipv4Address={'start': module.params['ipv42Address'],
                                                           'direction': module.params['ipv42AddressDirection'],
                                                           'step': module.params['ipv42AddressStep']},
                                              ipv4AddressPortStep = module.params['ipv42AddressPortStep'],
                                              gateway={'start': module.params['ipv42Gateway'],
                                                       'direction': module.params['ipv42GatewayDirection'],
                                                       'step': module.params['ipv42GatewayStep']},
                                              gatewayPortStep = module.params['ipv42GatewayPortStep'],
                                              prefix = module.params['ipv42AddressPrefix'],
                                              resolveGateway = module.params['ipv42ResolveGateway'])

        # flap = true or false.
        #    If there is only one host IP interface, then single value = True or False.
        #    If there are multiple host IP interfaces, then single value = a list ['true', 'false']
        #           Provide a list of total true or false according to the total amount of host IP interfaces.
        bgpObj1 = protocolObj.configBgp(ipv4Obj1,
                                        name = module.params['bgp1Name'],
                                        enableBgp = module.params['bgp1Enable'],
                                        holdTimer = module.params['bgp1HoldTimer'],
                                        dutIp={'start': module.params['bgp1DutIp'],
                                               'direction': module.params['bgp1DutIpDirection'],
                                               'step': module.params['bgp1DutIpStep']},
                                        localAs2Bytes = module.params['bgp1LocalAsBytes'],
                                        enableGracefulRestart = module.params['bgp1EnableGracefulRestart'],
                                        restartTime = module.params['bgp1RestartTime'],
                                        type = module.params['bgp1Type'])

        bgpObj2 = protocolObj.configBgp(ipv4Obj2,
                                        name = module.params['bgp2Name'],
                                        enableBgp = module.params['bgp2Enable'],
                                        holdTimer = module.params['bgp2HoldTimer'],
                                        dutIp={'start': module.params['bgp2DutIp'],
                                               'direction': module.params['bgp2DutIpDirection'],
                                               'step': module.params['bgp2DutIpStep']},
                                        localAs2Bytes = module.params['bgp2LocalAsBytes'],
                                        enableGracefulRestart = module.params['bgp2EnableGracefulRestart'],
                                        restartTime = module.params['bgp2RestartTime'],
                                        type = module.params['bgp2Type'])

        networkGroupObj1 = protocolObj.configNetworkGroup(create=deviceGroupObj1,
                                                          name=module.params['networkGroup1Name'],
                                                          multiplier = module.params['networkGroup1Multiplier'],
                                                          networkAddress = {'start': module.params['networkGroup1Address'],
                                                                            'step': module.params['networkGroup1AddressStep'],
                                                                            'direction': module.params['networkGroup1AddressDirection']},
                                                          prefixLength = module.params['networkGroup1PrefixLength'])

        networkGroupObj2 = protocolObj.configNetworkGroup(create=deviceGroupObj2,
                                                          name=module.params['networkGroup2Name'],
                                                          multiplier = module.params['networkGroup2Multiplier'],
                                                          networkAddress = {'start': module.params['networkGroup2Address'],
                                                                            'step': module.params['networkGroup2AddressStep'],
                                                                            'direction': module.params['networkGroup2AddressDirection']},
                                                          prefixLength = module.params['networkGroup2PrefixLength'])

        protocolObj.startAllProtocols()
        protocolObj.verifyProtocolSessionsNgpf()

        # For all parameter options, go to the API configTrafficItem.
        # mode = create or modify
        trafficObj = Traffic(mainObj)
        trafficStatus = trafficObj.configTrafficItem(
            mode='create',
            trafficItem = {
                'name': module.params['trafficItemName'],
                'trafficType': module.params['trafficItemType'],
                'biDirectional': module.params['trafficItemBiDirection'],
                'srcDestMesh': module.params['trafficItemSrcDestMesh'],
                'routeMesh': module.params['trafficItemRouteMesh'],
                'allowSelfDestined': module.params['trafficItemAllowSelfDestined'],
                'trackBy': module.params['trafficItemTrackBy']},

            endpoints = [{'name': module.params['endpointName'],
                          'sources': [topologyObj1],
                          'destinations': [topologyObj2]
                         }],

            configElements = [{'transmissionType': module.params['transmissionType'],
                               'frameCount': module.params['frameCount'],
                               'frameRate': module.params['frameRate'],
                               'frameRateType': module.params['frameRateType'],
                               'frameSize': module.params['frameSize']}])

        trafficItemObj   = trafficStatus[0]
        endpointObj      = trafficStatus[1][0]
        configElementObj = trafficStatus[2][0]

        trafficObj.startTraffic(regenerateTraffic=True, applyTraffic=True)

        # Check the traffic state before getting stats.
        #    Use one of the below APIs based on what you expect the traffic state should be before calling stats.
        #    'stopped': If you expect traffic to be stopped such as for fixedFrameCount and fixedDuration.
        #    'started': If you expect traffic to be started such as in continuous mode.
        trafficObj.checkTrafficState(expectedState=['stopped'], timeout=45)
        #trafficObj.checkTrafficState(expectedState=['started'], timeout=45)
        
        statObj = Statistics(mainObj)
        stats = statObj.getStats(viewName='Flow Statistics')

        print('\n{txPort:10} {txFrames:15} {rxPort:10} {rxFrames:15} {frameLoss:10}'.format(
            txPort='txPort', txFrames='txFrames', rxPort='rxPort', rxFrames='rxFrames', frameLoss='frameLoss'))
        print('-'*90)

        for flowGroup,values in stats.items():
            txPort = values['Tx Port']
            rxPort = values['Rx Port']
            txFrames = values['Tx Frames']
            rxFrames = values['Rx Frames']
            frameLoss = values['Frames Delta']

            print('{txPort:10} {txFrames:15} {rxPort:10} {rxFrames:15} {frameLoss:10} '.format(
                txPort=txPort, txFrames=txFrames, rxPort=rxPort, rxFrames=rxFrames, frameLoss=frameLoss))

        if module.params['releasePortsWhenDone'] == True:
            portObj.releasePorts(module.params['portList'])

        if module.params['osPlatform'] == 'linux':
            mainObj.linuxServerStopAndDeleteSession()

        if module.params['osPlatform'] == 'windowsConnectionMgr':
            mainObj.deleteSession()

        # Tell Ansible test passed
        #result['changed'] = True
        #module.exit_json(changed=True, test='Passed')
        module.exit_json(BGP_Configuration='Passed')

    except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
        module.fail_json(msg=errMsg, **result)

        if module.params['enableDebugTracing']:
            if not bool(re.search('ConnectionError', traceback.format_exc())):
                logging.ERROR('\n%s' % traceback.format_exc())
                module.fail_json(changed=True, meta=traceback.format_exc())
                #exitArgs = {'module_stderr': traceback.format_exc()}
                #module.exit_json(**exitArgs)

        logging.ERROR('\nException Error! %s\n' % errMsg)
        if 'mainObj' in locals() and module.params['osPlatform'] == 'linux':
            mainObj.linuxServerStopAndDeleteSession()

        if 'mainObj' in locals() and module.params['osPlatform'] in ['windows', 'windowsConnectionMgr']:
            if releasePortsWhenDone and forceTakePortOwnership:
                portObj.releasePorts(module.params['portList'])
            if module.params['osPlatform'] == 'windowsConnectionMgr':
                mainObj.deleteSession()


if __name__ == '__main__':
    main()
