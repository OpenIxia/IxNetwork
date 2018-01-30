#!/usr/local/python3.4.6/bin/python3.4

# DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
# 
# DESCRIPTION
#    This sample script uses two back-to-back Ixia ports.
#    to configure OSPF with advertising network routes.
#
#    This script supports both IxNetwork API server and Linux API server connection.
#
#    - Configure two IPv4 Topology Groups
#    - Configure OSPF and network advertising routes.
#    - Start protocols
#    - Verify protocol sessions
#    - Create Traffic Item
#    - Apply Traffic
#    - Start Traffic
#    - Get stats   
#

import requests, json, sys, os, time, traceback
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

    topologyObj1 = IxN_RestApiPy3.createTopologyNgpf(sessionUrl, 
                                                     portList=[portList[0]],
                                                     topologyName='MyTopo1',
                                                     apiKey=apiKey, verifySslCert=verifySslCert)

    deviceGroupObj1 = IxN_RestApiPy3.createDeviceGroupNgpf(topologyObj1,
                                                           multiplier=1,
                                                           deviceGroupName='myDG1',
                                                           apiKey=apiKey, verifySslCert=verifySslCert)

    topologyObj2 = IxN_RestApiPy3.createTopologyNgpf(sessionUrl,
                                                     portList=[portList[1]],
                                                     topologyName='MyTopo2',
                                                     apiKey=apiKey, verifySslCert=verifySslCert)

    deviceGroupObj2 = IxN_RestApiPy3.createDeviceGroupNgpf(topologyObj2,
                                                           multiplier=1,
                                                           deviceGroupName='myDG2',
                                                           apiKey=apiKey, verifySslCert=verifySslCert)

    ethernetObj1 = IxN_RestApiPy3.createEthernetNgpf(deviceGroupObj1,
                                                     ethernetName='MyEth1',
                                                     macAddress={'start': '00:01:01:00:00:01',
                                                                 'direction': 'increment',
                                                                 'step': '00:00:00:00:00:01'},
                                                     macAddressPortStep='disabled',
                                                     apiKey=apiKey, verifySslCert=verifySslCert)

    ethernetObj2 = IxN_RestApiPy3.createEthernetNgpf(deviceGroupObj2,
                                                     ethernetName='MyEth2',
                                                     macAddress={'start': '00:01:02:00:00:01',
                                                                 'direction': 'increment',
                                                                 'step': '00:00:00:00:00:01'},
                                                     macAddressPortStep='disabled',
                                                     apiKey=apiKey, verifySslCert=verifySslCert)
    
    ipv4Obj1 = IxN_RestApiPy3.createIpv4Ngpf(ethernetObj1,
                                             ipv4Address={'start': '1.1.1.1',
                                                          'direction': 'increment',
                                                          'step': '0.0.0.1'},
                                             ipv4AddressPortStep='disabled',
                                             gateway={'start': '1.1.1.2',
                                                      'direction':'increment',
                                                      'step': '0.0.0.0'},
                                             gatewayPortStep='disabled',
                                             prefix=24,
                                             resolveGateway=True,
                                             apiKey=apiKey, verifySslCert=verifySslCert)

    ipv4Obj2 = IxN_RestApiPy3.createIpv4Ngpf(ethernetObj2,
                                             ipv4Address={'start': '1.1.1.2',
                                                          'direction': 'increment',
                                                          'step': '0.0.0.1'},
                                             ipv4AddressPortStep='disabled',
                                             gateway={'start': '1.1.1.1',
                                                      'direction': 'increment',
                                                      'step': '0.0.0.0'},
                                             gatewayPortStep='disabled',
                                             prefix=24,
                                             resolveGateway=True,
                                             apiKey=apiKey, verifySslCert=verifySslCert)
        
    ospfObj1 = IxN_RestApiPy3.configOspf(ipv4Obj1,
                                         apiKey = apiKey,
                                         verifySslCert = False,
                                         name = 'ospf_1',
                                         areaId = '0',
                                         neighborIp = '1.1.1.2',
                                         helloInterval = '10',
                                         areaIdIp = '0.0.0.0',
                                         networkType = 'pointtomultipoint',
                                         deadInterval = '40')

    ospfObj2 = IxN_RestApiPy3.configOspf(ipv4Obj2,
                                         apiKey = apiKey,
                                         verifySslCert = False,
                                         name = 'ospf_2',
                                         areaId = '0',
                                         neighborIp = '1.1.1.1',
                                         helloInterval = '10',
                                         areaIdIp = '0.0.0.0',
                                         networkType = 'pointtomultipoint',
                                         deadInterval = '40')

    networkGroupObj1 = IxN_RestApiPy3.configNetworkGroup(deviceGroupObj1,
                                                         name='networkGroup1',
                                                         multiplier = 100,
                                                         networkAddress = {'start': '160.1.0.0',
                                                                           'step': '0.0.0.1',
                                                                           'direction': 'increment'},
                                                         prefixLength = 24,
                                                         apiKey=apiKey, verifySslCert=verifySslCert)
    
    networkGroupObj2 = IxN_RestApiPy3.configNetworkGroup(deviceGroupObj2,
                                                         name='networkGroup2',
                                                         multiplier = 100,
                                                         networkAddress = {'start': '180.1.0.0',
                                                                           'step': '0.0.0.1',
                                                                           'direction': 'increment'},
                                                         prefixLength = 24,
                                                         apiKey=apiKey, verifySslCert=verifySslCert)

    IxN_RestApiPy3.startAllProtocols(sessionUrl, apiKey=apiKey, verifySslCert=verifySslCert)

    IxN_RestApiPy3.verifyProtocolSessionsNgpf([ipv4Obj1, ipv4Obj2, ospfObj1, ospfObj2],
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
                                                                   'sources': [topologyObj1],
                                                                   'destinations': [topologyObj2]}],
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
                                     apiKey=apiKey)

    # If you're sending a large number of packets, you need to set timeout to a larger number. 
    IxN_RestApiPy3.checkTrafficState(sessionUrl, expectedState=['stopped'], timeout=45,
                                     apiKey=apiKey, verifySslCert=verifySslCert)

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
