
# PLEASE READ DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# REQUIREMENTS
#    - Python modules: requests
#
# SUPPORTS
#    - Python 2.7 and 3+
#    - IxNetwork API servers: Windows, WindowsConnectionMgr and Linux
#
# DESCRIPTION
#    This sample script demonstrates:
#        - REST API configurations using two back-to-back Ixia ports.
#        - Connecting to Windows IxNetwork API server or Linux API server.
#
#        - Verify for sufficient amount of port licenses before testing.
#        - Verify port ownership.
#        - Configure two IPv4 Topology Groups
#        - Start protocols
#        - Verify ARP
#        - Create a Traffic Item
#             - Selecting specific source and destionation IP addresses.
#
#        - Apply Traffic
#        - Start Traffic
#        - Get stats
#
# USAGE
#    python <script>.py windows
#    python <script>.py linux

import sys, os, traceback

sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules'))))
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiTraffic import Traffic
from IxNetRestApiProtocol import Protocol
from IxNetRestApiStatistics import Statistics

# Default the API server to either windows, windowsConnectionMgr or linux.
osPlatform = 'windows'

if len(sys.argv) > 1:
    if sys.argv[1] not in ['windows', 'windowsConnectionMgr', 'linux']:
        sys.exit("\nError: %s is not a known option. Choices are 'windows', 'windowsConnectionMgr or 'linux'." % sys.argv[1])
    osPlatform = sys.argv[1]

try:
    #---------- Preference Settings --------------
    forceTakePortOwnership = True
    releasePortsWhenDone = False
    enableDebugTracing = True
    deleteSessionAfterTest = False ;# For Windows Connection Mgr and Linux API server only

    licenseServerIp = '192.168.70.3'
    licenseModel = 'subscription'

    ixChassisIp = '192.168.70.128'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'],
                [ixChassisIp, '1', '2']]

    if osPlatform == 'linux':
        mainObj = Connect(apiServerIp='192.168.70.12',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs=osPlatform,
                          generateLogFile='ixiaDebug.log'
                      )
        
    if osPlatform in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='192.168.70.3',
                          serverIpPort='11009',
                          serverOs=osPlatform,
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          generateLogFile='ixiaDebug.log'
                      )
        
    #---------- Preference Settings End --------------

    # Only need to blank the config for Windows because osPlatforms such as Linux and
    # Windows Connection Mgr supports multiple sessions and a new session always come up as a blank config.
    if osPlatform == 'windows':
        mainObj.newBlankConfig() 

    mainObj.configLicenseServerDetails([licenseServerIp], licenseModel)

    portObj = PortMgmt(mainObj)
    portObj.assignPorts(portList, forceTakePortOwnership)

    protocolObj = Protocol(mainObj)
    topologyObj1 = protocolObj.createTopologyNgpf(portList=[portList[0]],
                                              topologyName='Topo1')

    deviceGroupObj1 = protocolObj.createDeviceGroupNgpf(topologyObj1,
                                                    multiplier=10,
                                                    deviceGroupName='DG1')

    topologyObj2 = protocolObj.createTopologyNgpf(portList=[portList[1]],
                                              topologyName='Topo2')

    deviceGroupObj2 = protocolObj.createDeviceGroupNgpf(topologyObj2,
                                                    multiplier=10,
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
                                          gateway={'start': '1.1.1.11',
                                                   'direction': 'increment',
                                                   'step': '0.0.0.0'},
                                          gatewayPortStep='disabled',
                                          prefix=24,
                                          resolveGateway=True)

    ipv4Obj2 = protocolObj.configIpv4Ngpf(ethernetObj2,
                                          ipv4Address={'start': '1.1.1.11',
                                                       'direction': 'increment',
                                                       'step': '0.0.0.1'},
                                          ipv4AddressPortStep='disabled',
                                          gateway={'start': '1.1.1.1',
                                                   'direction': 'increment',
                                                   'step': '0.0.0.0'},
                                          gatewayPortStep='disabled',
                                          prefix=24,
                                          resolveGateway=True)

    protocolObj.startAllProtocols()
    protocolObj.verifyProtocolSessionsUp()

    # To select specific source and destionation IP addresses:
    #     - Create a list of keyword args
    #       For example:
    #            scalableSources = [{"arg1": ipv4Obj1, "arg2": 1, "arg3": 1, "arg4": 2, "arg5": 1},
    #                               {"arg1": ipv4Obj1, "arg2": 1, "arg3": 1, "arg4": 5, "arg5": 1}],
    # 
    # arg1: The ipv4 object handle: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1
    # arg2: Base port index
    # arg3: Port count
    # arg4: Starting device index
    # arg5: Device count
    

    # For all parameter options, please go to the API configTrafficItem
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
                      'scalableSources': [{"arg1": ipv4Obj1, "arg2": 1, "arg3": 1, "arg4": 2, "arg5": 1},
                                          {"arg1": ipv4Obj1, "arg2": 1, "arg3": 1, "arg4": 5, "arg5": 1}],
                      'scalableDestinations': [{"arg1": ipv4Obj2, "arg2": 1, "arg3": 1, "arg4": 3, "arg5": 1},
                                               {"arg1": ipv4Obj2, "arg2": 1, "arg3": 1, "arg4": 6, "arg5": 1}]
                  }],
        configElements = [{'transmissionType': 'fixedFrameCount',
                           'frameCount': 50000,
                           'frameRate': 10,
                           'frameRateType': 'percentLineRate',
                           'frameSize': 128}])
    
    trafficItemObj   = trafficStatus[0]
    endpointObj      = trafficStatus[1][0]
    configElementObj = trafficStatus[2][0]

    trafficObj.startTraffic(regenerateTraffic=True, applyTraffic=True)

    # Check the traffic state before getting stats.
    #    Use one of the below APIs based on what you expect the traffic state should be before calling stats.
    #    If you expect traffic to be stopped such as in fixedFrameCount and fixedDuration
    #    or do you expect traffic to be started such as in continuous mode
    trafficObj.checkTrafficState(expectedState=['stopped'], timeout=45)
    #trafficObj.checkTrafficState(expectedState=['started], timeout=45)

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

    if releasePortsWhenDone == True:
        portObj.releasePorts(portList)

    if osPlatform == 'linux':
        mainObj.linuxServerStopAndDeleteSession()

    if osPlatform == 'windowsConnectionMgr':
        mainObj.deleteSession()

except (IxNetRestApiException, Exception, KeyboardInterrupt):
    if enableDebugTracing:
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())

    if 'mainObj' in locals() and osPlatform == 'linux':
        if deleteSessionAfterTest:
            mainObj.linuxServerStopAndDeleteSession()

    if 'mainObj' in locals() and osPlatform in ['windows', 'windowsConnectionMgr']:
        if releasePortsWhenDone and forceTakePortOwnership:
            portObj.releasePorts(portList)

        if osPlatform == 'windowsConnectionMgr':
            if deleteSessionAfterTest:
                mainObj.deleteSession()
