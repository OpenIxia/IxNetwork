#!/usr/local/python3.4.6/bin/python3.4

# DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# DESCRIPTION
#
#    Configures custom egress tracking on a receiving port.
#    This sample shows how to create one ingress tracking and one egress tracking
#    so the configuration tries not to run out of the maximum 22 bits of resource.
#
#    This script supports both IxNetwork API server and Linux API server connection.
#
#    - Configure two IPv4 Topology Groups
#    - Start protocols
#    - Create Traffic Item
#    - Regenerate All Traffic Items
#    - Apply Traffic
#    - Configures egress tracking
#    - Create egress tracking stat view
#    - Start Traffic
#    - Get stats
#    - Option to remove the egress stat view
#
# To include an ingress tracking field:
#    When you create your Traffic Item, this is when you select your ingress trackings.
#    The ingress trackings becomes an option for you to select as part of the egress tracking 
#    stats as shown below.  
#
# Available tracking filters for both ingress and egress...
#        ID: 1  VLAN:VLAN-ID (Ingress tracking)
#        ID: 2  Flow Group  (Ingress tracking)
#        ID: 3  Custom: (4 bits at offset 116)  <-- Egress tracking
# 
# Sample egress stats:
#
# Row: 1
#        Rx Port: 2/1
#        VLAN:VLAN-ID: 103  <-- Ingress tracking the vlanID
#        Egress Tracking: Custom: (4 bits at offset 116)
#        Tx Frames: 100000
#        Rx Frames: 100000
#        Frames Delta: 0
#        Loss %: 0
#        Tx Frame Rate: 0
#        Rx Frame Rate: 0
#        Tx L1 Rate (bps): 0
#        Rx L1 Rate (bps): 0
#        Rx Bytes: 12800000
#        Tx Rate (Bps): 0
#        Rx Rate (Bps): 0
#        Tx Rate (bps): 0
#        Rx Rate (bps): 0
#        Tx Rate (Kbps): 0
#        Rx Rate (Kbps): 0
#        Tx Rate (Mbps): 0
#        Rx Rate (Mbps): 0
#        Store-Forward Avg Latency (ns): 556418835
#        Store-Forward Min Latency (ns): 9840
#        Store-Forward Max Latency (ns): 1213352620
#        First TimeStamp: 00:00:01.002
#        Last TimeStamp: 00:00:02.510


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

#--------------- Egress tracking variable settings -----------------
# STEP 1:
#    This variable is optional for you to name your egress stat view.
#    Defaults to EgressStatView
egressStatViewName = 'EgressStats'

# STEP 2:
#    Create this variable's value in this string's format.
egressTrackingPort = '192.168.70.10/Card2/Port1'
offsetBit = 116
bitWidth = 4

# STEP 3:
# This variable is optional to include an ingress tracking field. Set to None if you don't want to
# track ingressing packets.  
# This ingress tracking filter name will be selectable only if you include it in the Traffic Item's
# trackby parameter at the time of creating the Traffic Item.
# How to know and get the filter name?  
#     - Include the tracking on Traffic Item first.
#     - Then run this script with this variable set to None since you don't know the filter name yet.
#     - On your terminal, you will see a list of tracking filter names like shown below:
#
#        ID: 1  VLAN:VLAN-ID  <-- For this example, going to track ingressing vlanID. 
#        ID: 2  Flow Group  
#        ID: 3  Custom: (4 bits at offset 116)  <-- This is your custom egress tracking filter name. 
ingressTrackingFilterName = 'VLAN:VLAN-ID'
#ingressTrackingFilterName = None

# STEP 4:
# Sometime you might not want to remove the created egress stat view so you could debug.
removeAllTclStatViews = True

#--------------- Egress tracking variable settings ends ----------

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
                                                     vlanId={'start': 103,
                                                             'direction': 'increment',
                                                             'step':0},
                                                     apiKey=apiKey, verifySslCert=verifySslCert)

    ethernetObj2 = IxN_RestApiPy3.createEthernetNgpf(deviceGroupObj2,
                                                     ethernetName='MyEth2',
                                                     macAddress={'start': '00:01:02:00:00:01',
                                                                 'direction': 'increment',
                                                                 'step': '00:00:00:00:00:01'},
                                                     vlanId={'start': 103,
                                                             'direction': 'increment',
                                                             'step':0},
                                                     macAddressPortStep='disabled',
                                                     apiKey=apiKey, verifySslCert=verifySslCert)
    
    ipv4Obj1 = IxN_RestApiPy3.createIpv4Ngpf(ethernetObj1,
                                             ipv4Address={'start': '1.1.1.1',
                                                          'direction': 'increment',
                                                          'step': '0.0.0.1'},
                                             ipv4AddressPortStep='disabled',
                                             gateway={'start': '1.1.1.2',
                                                      'direction': 'increment',
                                                      'step': '0.0.0.0'},
                                             gatewayPortStep='disabled',
                                             prefix=24,
                                             resolveGateway=True, apiKey=apiKey, verifySslCert=verifySslCert)

    ipv4Obj2 = IxN_RestApiPy3.createIpv4Ngpf(ethernetObj2,
                                             ipv4Address={'start': '1.1.1.2',
                                                          'direction': 'increment',
                                                          'step': '0.0.0.1'},
                                             ipv4AddressPortStep='disabled',
                                             gateway={'start': '1.1.1.1',
                                                      'direction':'increment',
                                                      'step': '0.0.0.0'},
                                             gatewayPortStep='disabled',
                                             prefix=24,
                                             resolveGateway=True, apiKey=apiKey, verifySslCert=verifySslCert)

    IxN_RestApiPy3.startAllProtocols(sessionUrl, apiKey=apiKey, verifySslCert=verifySslCert)

    IxN_RestApiPy3.verifyProtocolSessionsNgpf([ipv4Obj1, ipv4Obj2], apiKey=apiKey, verifySslCert=verifySslCert)

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
                                                         'trackBy': ['flowGroup0', 'vlanVlanId0', 'sourceDestValuePair0']},
                                                     endpoints = [{'name':'Flow-Group-1',
                                                                   'sources': [topologyObj1],
                                                                   'destinations': [topologyObj2]}],
                                                     configElements = [{'transmissionType': 'fixedFrameCount',
                                                                        'frameCount': 100000,
                                                                        'frameRate': 88,
                                                                        'frameRateType': 'percentLineRate',
                                                                        'frameSize': 128}])
    
    trafficItemObj      = trafficStatus[0]
    endpointObjList      = trafficStatus[1]
    configElementObjList = trafficStatus[2]
     
    IxN_RestApiPy3.regenerateTrafficItems(sessionUrl, apiKey=apiKey, verifySslCert=verifySslCert)

    IxN_RestApiPy3.applyTraffic(sessionUrl, apiKey=apiKey, verifySslCert=verifySslCert)

    IxN_RestApiPy3.configEgressCustomTracking(trafficItemObj, offsetBit, bitWidth,
                                              apiKey=apiKey, verifySslCert=verifySslCert)

    IxN_RestApiPy3.createEgressStatView(trafficItemObj, egressTrackingPort, offsetBit, bitWidth,
                                        egressStatViewName, ingressTrackingFilterName,
                                        apiKey=apiKey, verifySslCert=verifySslCert)

    IxN_RestApiPy3.startTraffic(sessionUrl, apiKey=apiKey, verifySslCert=verifySslCert)

    IxN_RestApiPy3.checkTrafficState(sessionUrl,
                                     expectedState=['started'],
                                     apiKey=apiKey, verifySslCert=verifySslCert)

    # If you're sending a large number of packets, you need to set timeout to a larger number. 
    IxN_RestApiPy3.checkTrafficState(sessionUrl, expectedState=['stopped'],
                                        timeout=45, apiKey=apiKey, verifySslCert=verifySslCert)

    #time.sleep(10)
    stats = IxN_RestApiPy3.getStats(sessionUrl, viewName=egressStatViewName, apiKey=apiKey,
                                    verifySslCert=verifySslCert)

    if removeAllTclStatViews:
        IxN_RestApiPy3.removeAllTclViews(sessionUrl, apiKey=apiKey, verifySslCert=verifySslCert)

    print('{0:10} {1:15} {2:15}'.format(
        'rxPort', 'txFrames', 'rxFrames'))
    print('-'*90)

    for flowGroup,values in stats.items():
        rxPort = values['Rx Port']
        txFrames = values['Tx Frames']
        rxFrames = values['Rx Frames']
        frameLoss = values['Frames Delta']

        print('{rxPort:10} {txFrames:15} {rxFrames:15}'.format(
            rxPort=rxPort, txFrames=txFrames, rxFrames=rxFrames))

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



