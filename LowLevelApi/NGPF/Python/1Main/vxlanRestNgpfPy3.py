#!/usr/local/python3.4.6/bin/python3.4

# DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# VxLAN configuration
#    This script configures two back-to-back Ixia ports.
#    Supports both IxNetwork API server and Linux API server connection.
#
#    If you want to create 100 VxLANS:
#       - Set the variablt totalVni = 100.
#       - The first Device Group multiplier must be 100..
#       - This will create 100 VNIs.
#    
#    To create hosts behind the VTEP:
#       - You need to create a new Device Group attaching to the Device Group with the VxLAN stack.
# 
#       For example:
#          - Get the first Device Group object:
#              http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1
#          - Create a Device Group attaching to the corresponding Device Group with the VxLAN stack:
#              http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/deviceGroup/1
#          - Using the second Device Group for the hosts sending traffic behind the VxLAN stack.
#

import sys, requests, json, time, traceback
import IxN_RestApiPy3

# Which REST API server do you want to connect to: linux or windows
connectToApiServer = 'linux'

# Settings for Windows 
if connectToApiServer == 'windows':
    ixNetRestServerIp = '192.168.70.127'
    ixNetRestServerPort = '11009'

# Setitngs for Linux API Server
if connectToApiServer == 'linux':
    linuxServerIp = '192.168.70.137'
    username = 'admin'
    password = 'admin'
    deleteLinuxSessionWhenDone = True
    
    # Set to True if the Linux API Server is newly installed.
    # We need to set the license server settings once. 
    isLinuxApiServerNewlyInstalled = False
    
    licenseServerIp = '192.168.70.127'
    licenseMode = 'subscription' ;# IxVM uses subscription. Physical chassis uses perpetual.
    licenseTier = 'tier3'
    linuxServerUrl = 'https://%s' % linuxServerIp

ixChassisIp = '192.168.70.10'    
portList = [[ixChassisIp, '1', '1'],
            [ixChassisIp, '2', '1']]

# For connecting to Linux API server that supports SSL. Provide your SSL certificate here.
verifySslCert = False

totalVni = 100

try:
    # If connecting to Linux API server
    if connectToApiServer == 'linux':
        # This will disable all the SSL warnings on your terminal.
        requests.packages.urllib3.disable_warnings()

        returnList = IxN_RestApiPy3.connectToLinuxApiServer(linuxServerIp, username=username, password=password)
        sessionUrl, sessionId, apiKey = returnList

        if isLinuxApiServerNewlyInstalled:
            IxN_RestApiPy3.linuxServerConfigGlobalLicenseServer(linuxServerIp, licenseServerIp,
                                                                licenseMode, licenseTier,
                                                                apiKey, verifySslCert=verifySslCert)
        IxN_RestApiPy3.linuxServerConfigNewSessionLicense(sessionUrl, linuxServerIp, apiKey, verifySslCert=verifySslCert)

    # If connecting to Windows API server
    if connectToApiServer == 'windows':
        sessionUrl = IxN_RestApiPy3.getSessionUrl(ixNetRestServerIp, ixNetRestServerPort)
        apiKey=None
        sessionId = sessionUrl.split('/ixnetwork')[0]


    IxN_RestApiPy3.newBlankConfig(sessionUrl, apiKey=apiKey, verifySslCert=verifySslCert)
    IxN_RestApiPy3.connectIxChassis(sessionUrl,chassisIp=ixChassisIp, apiKey=apiKey, verifySslCert=verifySslCert)
    IxN_RestApiPy3.createVports(sessionUrl, portList, apiKey=apiKey, verifySslCert=verifySslCert)
    IxN_RestApiPy3.assignPorts(sessionUrl, portList, apiKey=apiKey, verifySslCert=verifySslCert)

    topologyObj1 = IxN_RestApiPy3.createTopologyNgpf(sessionUrl, portList=[portList[0]],
                                                     topologyName='MyTopo1',
                                                     apiKey=apiKey, verifySslCert=verifySslCert)

    deviceGroupObj1 = IxN_RestApiPy3.createDeviceGroupNgpf(topologyObj1, multiplier=totalVni,
                                                           deviceGroupName='myDG1',
                                                           apiKey=apiKey, verifySslCert=verifySslCert)

    topologyObj2 = IxN_RestApiPy3.createTopologyNgpf(sessionUrl, portList=[portList[1]],
                                                     topologyName='MyTopo2', apiKey=apiKey)

    deviceGroupObj2 = IxN_RestApiPy3.createDeviceGroupNgpf(topologyObj2, multiplier=totalVni,
                                                           deviceGroupName='myDG2',
                                                           apiKey=apiKey, verifySslCert=verifySslCert)

    ethernetObj1 = IxN_RestApiPy3.createEthernetNgpf(deviceGroupObj1,
                                                     ethernetName='MyEth1',
                                                     macAddress={'start': '00:01:01:00:00:01',
                                                                 'direction': 'increment',
                                                                 'step': '00:00:00:00:00:01'},
                                                     macAddressPortStep='disabled',
                                                     vlanId=100, apiKey=apiKey, verifySslCert=verifySslCert)
    
    ethernetObj2 = IxN_RestApiPy3.createEthernetNgpf(deviceGroupObj2,
                                                     ethernetName='MyEth2',
                                                     macAddress={'start': '00:01:02:00:00:01',
                                                                 'direction': 'increment',
                                                                 'step': '00:00:00:00:00:01'},
                                                     macAddressPortStep='disabled',
                                                     vlanId=100, apiKey=apiKey, verifySslCert=verifySslCert)

    ipv4Obj1 = IxN_RestApiPy3.createIpv4Ngpf(ethernetObj1,
                                             ipv4Address={'start': '100.1.1.1',
                                                          'direction': 'increment', 
                                                          'step': '0.0.0.1'},
                                             ipv4AddressPortStep='disabled',
                                             gateway={'start': '100.1.3.1',
                                                      'direction': 'increment',
                                                      'step': '0.0.0.1'},
                                             gatewayPortStep='disabled',
                                             prefix=16,
                                             resolveGateway=True, apiKey=apiKey, verifySslCert=verifySslCert)
    
    ipv4Obj2 = IxN_RestApiPy3.createIpv4Ngpf(ethernetObj2,
                                             ipv4Address={'start': '100.1.3.1',
                                                          'direction': 'increment',
                                                          'step': '0.0.0.1'},
                                             ipv4AddressPortStep='disabled',
                                             gateway={'start': '100.1.1.1',
                                                      'direction': 'increment',
                                                      'step': '0.0.0.1'},
                                             gatewayPortStep='disabled',
                                             prefix=16,
                                             resolveGateway=True, apiKey=apiKey, verifySslCert=verifySslCert)

    vxlanObj1 = IxN_RestApiPy3.createVxlanNgpf(ipv4Object=ipv4Obj1,
                                               vtepName='vtep_1',
                                               vtepVni={'start':1008,
                                                        'step':2,
                                                        'direction':'increment'},
                                               vtepIpv4Multicast={'start':'225.8.0.1',
                                                                  'step':'0.0.0.1',
                                                                  'direction':'increment'},
                                               apiKey=apiKey, verifySslCert=verifySslCert)

    vxlanObj2 = IxN_RestApiPy3.createVxlanNgpf(ipv4Object=ipv4Obj2,
                                               vtepName='vtep_1',
                                               vtepVni={'start':1008, 'step':2, 'direction':'increment'},
                                               vtepIpv4Multicast={'start':'225.8.0.1',
                                                                  'step':'0.0.0.1',
                                                                  'direction':'increment'},
                                               apiKey=apiKey, verifySslCert=verifySslCert)

    vxlanDeviceGroupObj1 = IxN_RestApiPy3.createDeviceGroupNgpf(deviceGroupObj1, multiplier=3,
                                                                deviceGroupName='vxlanHost1',
                                                                apiKey=apiKey, verifySslCert=verifySslCert)

    vxlanEthernetObj1 = IxN_RestApiPy3.createEthernetNgpf(vxlanDeviceGroupObj1,
                                                          ethernetName='VxLan1-Eth1',
                                                          macAddress={'start': '00:01:11:00:00:01',
                                                                      'direction': 'increment',
                                                                      'step': '00:00:00:00:00:01'},
                                                          vlanId='101', apiKey=apiKey,
                                                          verifySslCert=verifySslCert)
    
    vxlanIpv4Obj1 = IxN_RestApiPy3.createIpv4Ngpf(vxlanEthernetObj1,
                                                  ipv4Address={'start': '10.1.1.1',
                                                               'step': '0.0.0.0',
                                                               'direction': 'increment'},
                                                  gateway={'start': '10.1.3.1',
                                                           'step': '0.0.0.0',
                                                           'direction': 'increment'},
                                                  prefix=16,
                                                  resolveGateway=True,
                                                  apiKey=apiKey, verifySslCert=verifySslCert)
    
    vxlanDeviceGroupObj2 = IxN_RestApiPy3.createDeviceGroupNgpf(deviceGroupObj2, multiplier=3,
                                                                deviceGroupName='vxlanHost2',
                                                                apiKey=apiKey, verifySslCert=verifySslCert)

    vxlanEthernetObj2 = IxN_RestApiPy3.createEthernetNgpf(vxlanDeviceGroupObj2,
                                                          ethernetName='VxLan1-Eth1',
                                                          macAddress={'start': '00:01:22:00:00:01',
                                                                      'direction': 'increment',
                                                                      'step': '00:00:00:00:00:01'},
                                                          vlanId='101', apiKey=apiKey,
                                                          verifySslCert=verifySslCert)
    
    vxlanIpv4Obj2 = IxN_RestApiPy3.createIpv4Ngpf(vxlanEthernetObj2,
                                                  ipv4Address={'start': '10.1.3.1',
                                                               'step': '0.0.0.0',
                                                               'direction': 'increment'},
                                                  gateway={'start': '10.1.1.1',
                                                           'step': '0.0.0.0',
                                                           'direction': 'increment', },
                                                  prefix=16,
                                                  resolveGateway=True, apiKey=apiKey,
                                                  verifySslCert=verifySslCert)

    IxN_RestApiPy3.startAllProtocols(sessionUrl, apiKey=apiKey)

    IxN_RestApiPy3.verifyProtocolSessionsNgpf([ipv4Obj1, ipv4Obj2, vxlanObj1,
                                               vxlanObj2, vxlanIpv4Obj1, vxlanIpv4Obj2],
                                              apiKey=apiKey, verifySslCert=verifySslCert)

    # For all parameter options, please go to the API configTrafficItem
    # mode = create or modify
    trafficStatus = IxN_RestApiPy3.configTrafficItem(sessionUrl, apiKey=apiKey,
                                                     verifySslCert=verifySslCert,
                                                     mode='create',
                                                     trafficItem = {
                                                         'name':'Topo1 to Topo2',
                                                         'trafficType':'ipv4',
                                                         'biDirectional':True,
                                                         'srcDestMesh':'one-to-one',
                                                         'routeMesh':'oneToOne',
                                                         'allowSelfDestined':False,
                                                         'trackBy': ['flowGroup0']
                                                     },
                                                     endpoints = [{'name':'Flow-Group-1',
                                                                   'sources': [vxlanIpv4Obj1],
                                                                   'destinations': [vxlanIpv4Obj2]}],
                                                     configElements = [{'transmissionType': 'fixedFrameCount',
                                                                        'frameCount': 50000,
                                                                        'frameRate': 88,
                                                                        'frameRateType': 'percentLineRate',
                                                                        'frameSize': 128}])
    
    trafficItemObj       = trafficStatus[0]
    endpointObjList      = trafficStatus[1]
    configElementObjList = trafficStatus[2]

    IxN_RestApiPy3.regenerateTrafficItems(sessionUrl, apiKey=apiKey, verifySslCert=verifySslCert)

    IxN_RestApiPy3.applyTraffic(sessionUrl, apiKey=apiKey, verifySslCert=verifySslCert)

    IxN_RestApiPy3.startTraffic(sessionUrl, apiKey=apiKey, verifySslCert=verifySslCert)

    IxN_RestApiPy3.checkTrafficState(sessionUrl, expectedState=['started', 'startedWaitingForStats'],
                                     apiKey=apiKey, verifySslCert=verifySslCert)

    # If you're sending a large number of packets, you need to set timeout to a larger number. 
    IxN_RestApiPy3.checkTrafficState(sessionUrl, expectedState='stopped', timeout=45,
                                     apiKey=apiKey, verifySslCert=verifySslCert
)
    stats = IxN_RestApiPy3.getStats(sessionUrl, viewName='Flow Statistics', apiKey=apiKey,
                                    verifySslCert=verifySslCert)

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

        #if txFrames != rxFrames:
        #    print('\nFrame loss error:', int(txFrames) - int(rxFrames))

    if connectToApiServer == 'linux' and deleteLinuxSessionWhenDone == True:
        IxN_RestApiPy3.linuxServerStopAndDeleteSession(sessionId, apiKey=apiKey, verifySslCert=verifySslCert)

except IxN_RestApiPy3.IxNetRestUtilityException as errMsg:
    print('\nTest failed! {0}\n'.format(errMsg))
    if 'sessionId' in locals() and deleteLinuxSessionWhenDone == True:
        IxN_RestApiPy3.linuxServerStopAndDeleteSession(sessionId, apiKey=apiKey, verifySslCert=verifySslCert)

except Exception as errMsg:
    print('\nTest failed! {0}\n'.format(traceback.print_exc()))
    if 'sessionId' in locals() and deleteLinuxSessionWhenDone == True:
        IxN_RestApiPy3.linuxServerStopAndDeleteSession(sessionId, apiKey=apiKey, verifySslCert=verifySslCert)

except KeyboardInterrupt:
    print('\nAborting ...')
    if 'sessionId' in locals() and deleteLinuxSessionWhenDone == True:
        IxN_RestApiPy3.linuxServerStopAndDeleteSession(sessionId, apiKey=apiKey, verifySslCert=verifySslCert)

