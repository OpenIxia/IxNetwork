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
        'licenseTier':            {'type':'str', 'required':False, 'default':'tier3'}
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
            mainObj.configLicenseServerDetails([licenseServerIp], licenseModel, licenseTier)
            
        # Set createVports = True if building config from scratch.
        portObj.assignPorts(module.params['portList'])

        protocolObj = Protocol(mainObj)
        topologyObj1 = protocolObj.createTopologyNgpf(portList=[module.params['portList'][0]],
                                                      topologyName='Topo1')

        deviceGroupObj1 = protocolObj.createDeviceGroupNgpf(topologyObj1,
                                                            multiplier=1,
                                                            deviceGroupName='DG1')

        topologyObj2 = protocolObj.createTopologyNgpf(portList=[module.params['portList'][1]],
                                                      topologyName='Topo2')

        deviceGroupObj2 = protocolObj.createDeviceGroupNgpf(topologyObj2,
                                                            multiplier=1,
                                                            deviceGroupName='DG2')

        ethernetObj1 = protocolObj.configEthernetNgpf(deviceGroupObj1,
                                                      ethernetName='MyEth1',
                                                      macAddress={'start': '00:01:01:00:00:01',
                                                                  'direction': 'increment',
                                                                  'step': '00:00:00:00:00:01'},
                                                      macAddressPortStep='disabled',
                                                      vlanId={'start': 103,
                                                              'direction': 'increment',
                                                              'step':0})

        ethernetObj2 = protocolObj.configEthernetNgpf(deviceGroupObj2,
                                                      ethernetName='MyEth2',
                                                      macAddress={'start': '00:01:02:00:00:01',
                                                                  'direction': 'increment',
                                                                  'step': '00:00:00:00:00:01'},
                                                      macAddressPortStep='disabled',
                                                      vlanId={'start': 103,
                                                              'direction': 'increment',
                                                              'step':0})

        ipv4Obj1 = protocolObj.configIpv4Ngpf(ethernetObj1,
                                              ipv4Address={'start': '1.1.1.1',
                                                           'direction': 'increment',
                                                           'step': '0.0.0.1'},
                                              ipv4AddressPortStep='disabled',
                                              gateway={'start': '1.1.1.2',
                                                       'direction': 'increment',
                                                       'step': '0.0.0.0'},
                                              gatewayPortStep='disabled',
                                              prefix=24,
                                              resolveGateway=True)

        ipv4Obj2 = protocolObj.configIpv4Ngpf(ethernetObj2,
                                              ipv4Address={'start': '1.1.1.2',
                                                           'direction': 'increment',
                                                           'step': '0.0.0.1'},
                                              ipv4AddressPortStep='disabled',
                                              gateway={'start': '1.1.1.1',
                                                       'direction': 'increment',
                                                       'step': '0.0.0.0'},
                                              gatewayPortStep='disabled',
                                              prefix=24,
                                              resolveGateway=True)

        # flap = true or false.
        #    If there is only one host IP interface, then single value = True or False.
        #    If there are multiple host IP interfaces, then single value = a list ['true', 'false']
        #           Provide a list of total true or false according to the total amount of host IP interfaces.
        bgpObj1 = protocolObj.configBgp(ipv4Obj1,
                                        name = 'bgp_1',
                                        enableBgp = True,
                                        holdTimer = 90,
                                        dutIp={'start': '1.1.1.2',
                                               'direction': 'increment',
                                               'step': '0.0.0.0'},
                                        localAs2Bytes = 101,
                                        enableGracefulRestart = False,
                                        restartTime = 45,
                                        type = 'internal',
                                        enableBgpIdSameasRouterId = True)

        bgpObj2 = protocolObj.configBgp(ipv4Obj2,
                                        name = 'bgp_2',
                                        enableBgp = True,
                                        holdTimer = 90,
                                        dutIp={'start': '1.1.1.1',
                                               'direction': 'increment',
                                               'step': '0.0.0.0'},
                                        localAs2Bytes = 101,
                                        enableGracefulRestart = False,
                                        restartTime = 45,
                                        type = 'internal',
                                        enableBgpIdSameasRouterId = True)

        networkGroupObj1 = protocolObj.configNetworkGroup(create=deviceGroupObj1,
                                                          name='networkGroup1',
                                                          multiplier = 100,
                                                          networkAddress = {'start': '160.1.0.0',
                                                                            'step': '0.0.0.1',
                                                                            'direction': 'increment'},
                                                          prefixLength = 32)

        networkGroupObj2 = protocolObj.configNetworkGroup(create=deviceGroupObj2,
                                                      name='networkGroup2',
                                                      multiplier = 100,
                                                      networkAddress = {'start': '180.1.0.0',
                                                                        'step': '0.0.0.1',
                                                                        'direction': 'increment'},
                                                      prefixLength = 32)

        protocolObj.startAllProtocols()
        protocolObj.verifyProtocolSessionsNgpf()

        # For all parameter options, go to the API configTrafficItem.
        # mode = create or modify
        trafficObj = Traffic(mainObj)
        trafficStatus = trafficObj.configTrafficItem(
            mode='create',
            trafficItem = {
                'name':'Topo1 to Topo2',
                'trafficType':'ipv4',
                'biDirectional':True,
                'srcDestMesh':'one-to-one',
                'routeMesh':'oneToOne',
                'allowSelfDestined':False,
                'trackBy': ['flowGroup0', 'vlanVlanId0']},

            endpoints = [{'name':'Flow-Group-1',
                          'sources': [topologyObj1],
                          'destinations': [topologyObj2]
                         }],

            configElements = [{'transmissionType': 'fixedFrameCount',
                               'frameCount': 50000,
                               'frameRate': 88,
                               'frameRateType': 'percentLineRate',
                               'frameSize': 128}])

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
