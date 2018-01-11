
# PLEASE READ DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# REQUIREMENTS
#    - Python2.7
#    - Python modules: requests
#
# DESCRIPTION
#    This sample script demonstrates:
#        - REST API configurations using two back-to-back Ixia ports.
#        - Connecting to Windows IxNetwork API server or Linux API server.
#
#        - Configure two IPv4 Topology Groups
#        - Start protocols
#        - Verify ARP
#        - Create a Traffic Item
#        - Apply Traffic
#        - Start Traffic
#        - Get stats
#
# USAGE
#    python <script>.py windows
#    python <script>.py linux

import sys, traceback

sys.path.insert(0, '../Modules/Main')
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiTraffic import Traffic
from IxNetRestApiProtocol import Protocol
from IxNetRestApiStatistics import Statistics

# Default the API server to either windows or linux.
connectToApiServer = 'windows'

if len(sys.argv) > 1:
    if sys.argv[1] not in ['windows', 'windowsConnectionMgr', 'linux']:
        sys.exit("\nError: %s is not a known option. Choices are 'windows', 'windowsConnectionMgr or 'linux'." % sys.argv[1])
    connectToApiServer = sys.argv[1]

try:
    #---------- Preference Settings --------------

    forceTakePortOwnership = True
    releasePortsWhenDone = False
    enableDebugTracing = True
    deleteSessionAfterTest = True ;# For Windows Connection Mgr and Linux API server only
    licenseServerIp = '192.168.70.3'
    licenseModel = 'subscription'
    licenseTier = 'tier3'

    ixChassisIp = '192.168.70.11'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'],
                [ixChassisIp, '2', '1']]

    if connectToApiServer == 'linux':
        mainObj = Connect(apiServerIp='192.168.70.108',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs=connectToApiServer)
        
    if connectToApiServer in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='192.168.70.3',
                          serverIpPort='11009',
                          serverOs=connectToApiServer,
                          deleteSessionAfterTest=deleteSessionAfterTest)
        
    #---------- Preference Settings End --------------

    portObj = PortMgmt(mainObj)
    portObj.connectIxChassis(ixChassisIp)

    if portObj.arePortsAvailable(portList, raiseException=False) != 0:
        if forceTakePortOwnership == True:
            portObj.releasePorts(portList)
            portObj.clearPortOwnership(portList)
        else:
            raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')

    # Uncomment this to configure license server.
    # Configuring license requires releasing all ports even for ports that is not used for this test.
    portObj.releaseAllPorts()
    mainObj.configLicenseServerDetails([licenseServerIp], licenseModel, licenseTier)

    mainObj.newBlankConfig()

    # Set createVports True if building config from scratch.
    portObj.assignPorts(portList, createVports=True)

    protocolObj = Protocol(mainObj, portObj)
    topologyObj1 = protocolObj.createTopologyNgpf(portList=[portList[0]],
                                                  topologyName='Topo1')
    
    deviceGroupObj1 = protocolObj.createDeviceGroupNgpf(topologyObj1,
                                                        multiplier=1,
                                                        deviceGroupName='DG1')
    
    topologyObj2 = protocolObj.createTopologyNgpf(portList=[portList[1]],
                                                  topologyName='Topo2')
    
    deviceGroupObj2 = protocolObj.createDeviceGroupNgpf(topologyObj2,
                                                        multiplier=1,
                                                        deviceGroupName='DG2')
    
    ethernetObj1 = protocolObj.createEthernetNgpf(deviceGroupObj1,
                                                  ethernetName='MyEth1',
                                                  macAddress={'start': '00:01:01:00:00:01',
                                                              'direction': 'increment',
                                                              'step': '00:00:00:00:00:01'},
                                                  macAddressPortStep='disabled',
                                                  vlanId=100)
    
    ethernetObj2 = protocolObj.createEthernetNgpf(deviceGroupObj2,
                                                  ethernetName='MyEth2',
                                                  macAddress={'start': '00:01:02:00:00:01',
                                                              'direction': 'increment',
                                                              'step': '00:00:00:00:00:01'},
                                                  macAddressPortStep='disabled',
                                                  vlanId=100)
    
    ipv4Obj1 = protocolObj.createIpv4Ngpf(ethernetObj1,
                                          ipv4Address={'start': '100.1.1.1',
                                                       'direction': 'increment',
                                                       'step': '0.0.0.1'},
                                          ipv4AddressPortStep='disabled',
                                          gateway={'start': '100.1.3.1',
                                                   'direction': 'increment',
                                                   'step': '0.0.0.1'},
                                          gatewayPortStep='disabled',
                                          prefix=16,
                                          resolveGateway=True)
    
    ipv4Obj2 = protocolObj.createIpv4Ngpf(ethernetObj2,
                                          ipv4Address={'start': '100.1.3.1',
                                                       'direction': 'increment',
                                                       'step': '0.0.0.1'},
                                          ipv4AddressPortStep='disabled',
                                          gateway={'start': '100.1.1.1',
                                                   'direction': 'increment',
                                                   'step': '0.0.0.1'},
                                          gatewayPortStep='disabled',
                                          prefix=16,
                                          resolveGateway=True)
    
    vxlanObj1 = protocolObj.configVxlanNgpf(ipv4Obj1,
                                            vtepName='vtep_1',
                                            vtepVni={'start':1008,
                                                     'step':2,
                                                     'direction':'increment'},
                                            vtepIpv4Multicast={'start':'225.8.0.1',
                                                               'step':'0.0.0.1',
                                                               'direction':'increment'})
    
    
    vxlanObj2 = protocolObj.configVxlanNgpf(ipv4Obj2,
                                            vtepName='vtep_2',
                                            vtepVni={'start':1008,
                                                     'step':2,
                                                     'direction':'increment'},
                                            vtepIpv4Multicast={'start':'225.8.0.1',
                                                               'step':'0.0.0.1',
                                                               'direction':'increment'})
    
    vxlanDeviceGroupObj1 = protocolObj.createDeviceGroupNgpf(deviceGroupObj1,
                                                             multiplier=3, deviceGroupName='vxlanHost1')
    
    vxlanEthernetObj1 = protocolObj.createEthernetNgpf(vxlanDeviceGroupObj1,
                                                       ethernetName='VxLan1-Eth1',
                                                       macAddress={'start': '00:01:11:00:00:01',
                                                                   'direction': 'increment',
                                                                   'step': '00:00:00:00:00:01'},
                                                       vlanId='101')
    
    vxlanIpv4Obj1 = protocolObj.createIpv4Ngpf(vxlanEthernetObj1,
                                               ipv4Address={'start': '10.1.1.1',
                                                            'step': '0.0.0.0',
                                                            'direction': 'increment'},
                                               gateway={'start': '10.1.3.1',
                                                        'step': '0.0.0.0',
                                                        'direction': 'increment'},
                                               prefix=16,
                                               resolveGateway=True)
    
    vxlanDeviceGroupObj2 = protocolObj.createDeviceGroupNgpf(deviceGroupObj2, multiplier=3, deviceGroupName='vxlanHost2')
    
    vxlanEthernetObj2 = protocolObj.createEthernetNgpf(vxlanDeviceGroupObj2,
                                                       ethernetName='VxLan1-Eth1',
                                                       macAddress={'start': '00:01:22:00:00:01',
                                                                   'direction': 'increment',
                                                                   'step': '00:00:00:00:00:01'},
                                                       vlanId='101')
    
    vxlanIpv4Obj2 = protocolObj.createIpv4Ngpf(vxlanEthernetObj2,
                                               ipv4Address={'start': '10.1.3.1',
                                                            'step': '0.0.0.0',
                                                            'direction': 'increment'},
                                               gateway={'start': '10.1.1.1',
                                                        'step': '0.0.0.0',
                                                        'direction': 'increment'},
                                               prefix=16,
                                               resolveGateway=True)
    
    protocolObj.startAllProtocols()
    protocolObj.verifyProtocolSessionsNgpf()
    
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
            'trackBy': ['flowGroup0']},
        endpoints = [({'name':'Flow-Group-1',
                       'sources': [vxlanIpv4Obj1],
                       'destinations': [vxlanIpv4Obj2]},
                      {'highLevelStreamElements': None})],
        configElements = [{'transmissionType': 'fixedFrameCount',
                           'frameCount': 50000,
                           'frameRate': 88,
                           'frameRateType': 'percentLineRate',
                           'frameSize': 128}])
    
    trafficItemObj   = trafficStatus[0]
    endpointObj      = trafficStatus[1][0]
    configElementObj = trafficStatus[2][0]

    trafficObj.regenerateTrafficItems()
    trafficObj.startTraffic()

    # Check the traffic state to assure traffic has indeed stopped before checking for stats.
    if trafficObj.getTransmissionType(configElementObj) == "fixedFrameCount":
        trafficObj.checkTrafficState(expectedState=['stopped', 'stoppedWaitingForStats'], timeout=140)

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

    if connectToApiServer == 'linux':
        mainObj.linuxServerStopAndDeleteSession()

    if connectToApiServer == 'windowsConnectionMgr':
        mainObj.deleteSession()

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    if enableDebugTracing:
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())
    print('\nException Error! %s\n' % errMsg)
    if 'mainObj' in locals() and connectToApiServer == 'linux':
        mainObj.linuxServerStopAndDeleteSession()
    if 'mainObj' in locals() and connectToApiServer in ['windows', 'windowsConnectionMgr']:
        if releasePortsWhenDone and forceTakePortOwnership:
            portObj.releasePorts(portList)
        if connectToApiServer == 'windowsConnectionMgr':
            mainObj.deleteSession()
