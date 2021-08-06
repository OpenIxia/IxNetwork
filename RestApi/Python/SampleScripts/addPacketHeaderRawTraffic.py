#

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
#    - Configure a raw Traffic Item
#    - Add packet headers and configure its attributes:
#          Ethernet II
#          MPLS
#          MPLS
#          MPLS
#          MPLS
#          IPv4
#          UDP
#    - Apply Traffic
#    - Start Traffic
#    - Get stats
#
# Note:
#
#    For NGPF, Traffic Item traffic type has to be Ethernet/LAN. IPv4 trafifc type is not RAW.
#    No need to create DG, if you create RAW, just source and dest are ports.
#    If you use VM ports to do back to back, you probably will not see traffic. Use a physical ports instead.
#

import re, sys, os, traceback

# These  modules are one level above.
sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules'))))
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiTraffic import Traffic
from IxNetRestApiStatistics import Statistics

# Default the API server to either windows or linux.
osPlatform = 'linux'

try:
    #---------- Preference Settings --------------
    forceTakePortOwnership = True
    releasePortsWhenDone = False
    enableDebugTracing = True
    deleteSessionAfterTest = True ;# For Windows Connection Mgr and Linux API server only

    licenseServerIp = '172.16.101.3'
    licenseModel = 'subscription'

    ixChassisIp = '172.16.102.5'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'],
                [ixChassisIp, '1', '2']]

    if osPlatform == 'linux':
        mainObj = Connect(apiServerIp='172.16.102.2',
                          serverIpPort='443',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs=osPlatform,
                          traceLevel='all',
                          generateLogFile='ixiaDebug.log'
                      )

    if osPlatform in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='172.16.101.3',
                          serverIpPort='11009',
                          serverOs=osPlatform,
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          generateLogFile='ixiaDebug.log',
                          traceLevel='all'
                      )

    #---------- Preference Settings End --------------

    # Only need to blank the config for Windows because osPlatforms such as Linux and
    # Windows Connection Mgr supports multiple sessions and a new session always come up as a blank config.
    if osPlatform == 'windows':
        mainObj.newBlankConfig()

    mainObj.configLicenseServerDetails([licenseServerIp], licenseModel)

    # Set createVports = True if building config from scratch.
    portObj = PortMgmt(mainObj)
    vportList = portObj.assignPorts(portList, forceTakePortOwnership, createVports=True, rawTraffic=True, timeout=120)
    portObj.verifyPortState()

    # For all parameter options, please go to the API configTrafficItem
    # mode = create or modify
    trafficObj = Traffic(mainObj)
    trafficStatus = trafficObj.configTrafficItem(mode='create',
                                                 trafficItem = {
                                                     'name':'Raw MPLS/UDP',
                                                     'trafficType':'raw',
                                                     'trackBy': ['flowGroup0']
                                                 },
                                                 endpoints = [{'name':'Flow-Group-1',
                                                               'sources': [vportList[0]],
                                                               'destinations': [vportList[1]]
                                                           }],
                                                 configElements = [{'transmissionType': 'fixedFrameCount',
                                                                    'frameCount': 50000,
                                                                    'frameRate': 88,
                                                                    'frameRateType': 'percentLineRate',
                                                                    'frameSize': 128}])
    
    trafficItem1Obj  = trafficStatus[0]
    endpointObj      = trafficStatus[1][0]
    configElementObj = trafficStatus[2][0]

    # This will show you all the available protocol header options to create
    trafficObj.showProtocolTemplates(configElementObj)
    
    # Show the configured packet headers in sequential order to get the stack ID.
    trafficObj.showTrafficItemPacketStack(configElementObj)
    # 1: Ethernet II
    # 2: MPLS
    # 3: MPLS
    # 4: MPLS
    # 5: MPLS
    # 6: IPv4
    # 7: UDP

    stackObj = trafficObj.getPacketHeaderStackIdObj(configElementObj, stackId=1)
    # Show a list of field names in order to know which field to configure the mac addresses.
    trafficObj.showPacketHeaderFieldNames(stackObj)
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Destination MAC Address',
                                       data={'valueType': 'increment',
                                             'startValue': '00:0c:29:76:b4:39',
                                             'stepValue': '00:00:00:00:00:01',
                                             'countValue': 1})
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Source MAC Address',
                                       data={'valueType': 'increment',
                                             'startValue': '00:0c:29:aa:86:e0',
                                             'stepValue': '00:00:00:00:00:01',
                                             'countValue': 1})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='MPLS', stackNumber=1, action='append')
    # Just an example to show a list of field names in order to know which field to configure the IP addresses.
    trafficObj.showPacketHeaderFieldNames(stackObj)
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Label Value',
                                       data={'valueType': 'increment',
                                             'startValue': '16',
                                             'stepValue': '1',
                                             'countValue': 2,
                                             'auto': False})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='MPLS', stackNumber=2, action='append')
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Label Value',
                                       data={'valueType': 'increment',
                                             'startValue': '16',
                                             'stepValue': '1',
                                             'countValue': 2,
                                             'auto': False})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='MPLS', stackNumber=3, action='append')
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Label Value',
                                       data={'valueType': 'increment',
                                             'startValue': '16',
                                             'stepValue': '1',
                                             'countValue': 2,
                                             'auto': False})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='MPLS', stackNumber=4, action='append')
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Label Value',
                                       data={'valueType': 'increment',
                                             'startValue': '16',
                                             'stepValue': '1',
                                             'countValue': 2,
                                             'auto': False})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='IPv4',
                                                    stackNumber=5, action='append')
    #stackObj = getPacketHeaderStackIdObj(configElementObjList[0], stackId=6)
    # Show a list of field names in order to know which field to configure the IP addresses.
    trafficObj.showPacketHeaderFieldNames(stackObj)
    trafficObj.configPacketHeaderField(stackObj,
                                    fieldName='Source Address',
                                       data={'valueType': 'increment',
                                             'startValue': '1.1.1.1',
                                             'stepValue': '0.0.0.1',
                                             'countValue': 1})
    
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Destination Address',
                                       data={'valueType': 'increment',
                                             'startValue': '1.1.1.2',
                                             'stepValue': '0.0.0.1',
                                             'countValue': 1})

    # Example for IP Priority = DSCP/Diff-Serv
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Class selector PHB',
                                       data={'activeFieldChoice': True})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='UDP',
                                                    stackNumber=6, action='append')
    #stackObj = getPacketHeaderStackIdObj(configElementObjList[0], stackId=7)
    # Show a list of field names in order to know which field to configure the UDP src/dst ports.
    trafficObj.showPacketHeaderFieldNames(stackObj)
    # 1: UDP-Source-Port
    # 2: UDP-Dest-Port
    # 3: UDP-Length
    # 4: UDP-Checksum
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='UDP-Source-Port',
                                       data={'valueType': 'increment',
                                             'startValue': 1001,
                                             'stepValue': 1,
                                             'countValue': 2,
                                             'auto': False
                                         })
    
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='UDP-Dest-Port',
                                       data={'valueType': 'increment',
                                            'startValue': 1008,
                                             'stepValue': 1,
                                             'countValue': 2,
                                             'auto': False
                                         })
    
    trafficObj.showTrafficItemPacketStack(configElementObj)
    trafficObj.startTraffic(regenerateTraffic=True, applyTraffic=True)

    # Check the traffic state before getting stats.
    #    Use one of the below APIs based on what you expect the traffic state should be before calling stats.
    #    If you expect traffic to be stopped such as in fixedFrameCount and fixedDuration
    #    or do you expect traffic to be started such as in continuous mode
    trafficObj.checkTrafficState(expectedState=['stopped'], timeout=45)
    #trafficObj.checkTrafficState(expectedState=['started], timeout=45)

    statObj = Statistics(mainObj)
    stats = statObj.getStats(viewName='Flow Statistics')

    print('\n{txPort:10} {rxPort:10} {txFrames:15} {rxFrames:15} {frameLoss:10}'.format(
        txPort='txPort', txFrames='txFrames', rxPort='rxPort', rxFrames='rxFrames', frameLoss='frameLoss'))
    print('-'*90)

    for flowGroup,values in stats.items():
        txPort = values['Tx Port']
        rxPort = values['Rx Port']
        txFrames = values['Tx Frames']
        rxFrames = values['Rx Frames']
        frameLoss = values['Frames Delta']

        print('{txPort:10} {rxPort:10} {txFrames:15} {rxFrames:15} {frameLoss:10} '.format(
            txPort=txPort, rxPort=rxPort, txFrames=txFrames, rxFrames=rxFrames, frameLoss=frameLoss))

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
