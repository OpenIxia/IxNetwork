
# PLEASE READ DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# REQUIREMENTS
#    - Python2.7/3.4
#    - Python modules: requests
#
# DESCRIPTION
#    This sample script demonstrates:
#        - REST API configurations using two back-to-back Ixia ports.
#        - Connecting to Windows IxNetwork API server or Linux API server.

#    Configures custom egress tracking on a receiving port.
#
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

import sys, traceback

sys.path.insert(0, '../Modules/Main')
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiProtocol import Protocol
from IxNetRestApiTraffic import Traffic
from IxNetRestApiStatistics import Statistics
 
# Default the API server to either windows or linux.
connectToApiServer = 'windows'

if len(sys.argv) > 1:
    if sys.argv[1] not in ['windows', 'linux']:
        sys.exit("\nError: %s is not a known option. Choices are 'windows' or 'linux'." % sys.argv[1])
    connectToApiServer = sys.argv[1]

#--------------- Egress tracking variable settings -----------------
# STEP 1:
#    This variable is optional for you to name your egress stat view.
#    Defaults to EgressStatView
egressStatViewName = 'EgressStats'

# STEP 2:
#    Modify this variable's value using your chassisIp,card#/port# in this string's format.
egressTrackingPort = '192.168.70.11/Card2/Port1'
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
    #mainObj.releaseAllPorts()
    #mainObj.configLicenseServerDetails([licenseServerIp], licenseModel, licenseTier)

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
                                                  vlanId={'start': 103,
                                                          'direction': 'increment',
                                                          'step':0})
    
    ethernetObj2 = protocolObj.createEthernetNgpf(deviceGroupObj2,
                                                  ethernetName='MyEth2',
                                                  macAddress={'start': '00:01:02:00:00:01',
                                                              'direction': 'increment',
                                                              'step': '00:00:00:00:00:01'},
                                                  vlanId={'start': 103,
                                                          'direction': 'increment',
                                                          'step':0},
                                                  macAddressPortStep='disabled')

    ipv4Obj1 = protocolObj.createIpv4Ngpf(ethernetObj1,
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
    
    ipv4Obj2 = protocolObj.createIpv4Ngpf(ethernetObj2,
                                          ipv4Address={'start': '1.1.1.2',
                                                       'direction': 'increment',
                                                       'step': '0.0.0.1'},
                                          ipv4AddressPortStep='disabled',
                                          gateway={'start': '1.1.1.1',
                                                   'direction':'increment',
                                                   'step': '0.0.0.0'},
                                          gatewayPortStep='disabled',
                                          prefix=24,
                                          resolveGateway=True)
    
    protocolObj.startAllProtocols()
    protocolObj.verifyProtocolSessionsNgpf()
    
    # For all parameter options, please go to the API configTrafficItem
    # mode = create or modify
    trafficObj = Traffic(mainObj)
    trafficStatus = trafficObj.configTrafficItem(mode='create',
                                                 trafficItem = {
                                                     'name':'Topo1 to Topo2',
                                                     'trafficType':'ipv4',
                                                     'biDirectional':True,
                                                     'srcDestMesh':'one-to-one',
                                                     'routeMesh':'oneToOne',
                                                     'allowSelfDestined':False,
                                                     'trackBy': ['flowGroup0', 'vlanVlanId0', 'sourceDestValuePair0']},
                                                 endpoints = [({'name':'Flow-Group-1',
                                                                'sources': [topologyObj1],
                                                                'destinations': [topologyObj2]},
                                                               {'highLevelStreamElements': None})],
                                                 configElements = [{'transmissionType': 'fixedFrameCount',
                                                                    'frameCount': 100000,
                                                                    'frameRate': 88,
                                                                    'frameRateType': 'percentLineRate',
                                                                    'frameSize': 128}])
    
    trafficItemObj   = trafficStatus[0]
    endpointObj      = trafficStatus[1][0]
    configElementObj = trafficStatus[2][0]
    
    trafficObj.regenerateTrafficItems()
    trafficObj.applyTraffic()
    trafficObj.configEgressCustomTracking(trafficItemObj, offsetBit, bitWidth)
    statview = trafficObj.createEgressStatView(trafficItemObj, egressTrackingPort, offsetBit, bitWidth,
                                    egressStatViewName, ingressTrackingFilterName)
    
    trafficObj.startTraffic()
    
    print('\n****************** 7')
    response = mainObj.get(mainObj.httpHeader+statview)
    print(response.json())

    # Check the traffic state to assure traffic has indeed stopped before checking for stats.
    if trafficObj.getTransmissionType(configElementObj) == "fixedFrameCount":
        trafficObj.checkTrafficState(expectedState=['stopped', 'stoppedWaitingForStats'], timeout=45)
    
    statObj = Statistics(mainObj)
    stats = statObj.getStats(viewName=egressStatViewName)
        
    #if removeAllTclStatViews:
    #    mainObj.removeAllTclViews()
    
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
    if 'mainObj' in locals() and connectToApiServer == 'windows':
        if releasePortsWhenDone and forceTakePortOwnership:
            portObj.releasePorts(portList)
