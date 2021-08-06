
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
#        - Using ReST API to load a saved BGP configurations using two back-to-back Ixia ports.
#        - Supports Windows, Windows Connection Mgr and Linux API server.
#
#    - Connects to the chassis and verify port availability.
#    - Load a saved BGP config file.
#         If the config file is in the Windows API server filesystem, the configFile path format is c:\\path\\bgp.ixncfg
#         and set parameter localFile=False. Ex: fileMgmtObj.loadConfigFile(configFile, localFile=False)
#
#    - Optional: Reassign Ports
#    - Verify port states.
#    - Example to show how to modify BGP configurations.
#    - Start all protocols.
#    - Verify all protocol sessions.
#    - Apply Traffic
#    - Regenerate Traffic
#    - Start Traffic
#    - Get Stats
#

import re, sys, os, traceback

# These  modules are one level above.
sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules'))))
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiProtocol import Protocol
from IxNetRestApiTraffic import Traffic
from IxNetRestApiStatistics import Statistics

# API server options: windows, windowsConnectionMgr or linux.
# Linux default port for https only: 443
# Windows default port for both http|https: 11009
# Windows Connection Mgr. http:11009|htps:443
osPlatform = 'windows'
port = 11009

try:
    #---------- Preference Settings --------------
    forceTakePortOwnership = True
    releasePortsWhenDone = True
    deleteSessionAfterTest = True

    licenseServerIp = '172.16.101.3'
    licenseModel = 'subscription'
    licenseTier = 'tier3'

    currentDir = os.path.abspath(os.path.dirname(__file__))
    configFile = '{}/bgp_ngpf_8.30.ixncfg'.format(currentDir)

    ixChassisIp = '172.16.102.5'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'],
                [ixChassisIp, '1', '2']]

    if osPlatform == 'linux':
        mainObj = Connect(apiServerIp='172.16.102.2',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs=osPlatform,
                          sessionId=None,
                          traceLevel='all',
                          generateLogFile='ixiaDebug.log'
                      )

    # For windows: serverIpPort=11009
    # For windowsConnectionMgr, must state the following params: httpsSecured=<bool>. serverIpPort=443
    if osPlatform in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='172.16.101.3',
                          serverIpPort=port,
                          serverOs=osPlatform,
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          generateLogFile='ixiaDebug.log',
                          traceLevel='all',
                          httpsSecured=True
                      )

    #---------- Preference Settings End --------------

    portObj = PortMgmt(mainObj)
    portObj.connectIxChassis(ixChassisIp)

    if portObj.arePortsAvailable(portList, raiseException=False) != 0:
        if forceTakePortOwnership == True:
            portObj.releasePorts(portList)
            portObj.clearPortOwnership(portList)
        else:
            raise IxNetRestApiException('\nPorts are owned by another user and forceTakePortOwnership is set to False. Exiting test.')

    fileMgmtObj = FileMgmt(mainObj)    
    # localFile=True if config file is not located in the Windows c: drive.
    fileMgmtObj.loadConfigFile(configFile, localFile=True)
    
    portObj.releasePorts(portList)
    mainObj.configLicenseServerDetails([licenseServerIp], licenseModel, licenseTier)

    portObj = PortMgmt(mainObj)
    portObj.assignPorts(portList, forceTakePortOwnership)
    portObj.verifyPortState()
    
    protocolObj = Protocol(mainObj)

    # MODIFY BGP CONFIG:
    #    Step 1 of 2:  Get the BGP host object.
    #                  Filter the BGP host by it's Topology Group name.
    #                  State all the BGP attributes to modify in a list.
    bgpAttributeMultivalue = protocolObj.getBgpObject(topologyName='Topo1',
                                                      bgpAttributeList=['flap', 'uptimeInSec', 'downtimeInSec'])

    # Step 2 of 2: MODIFY THE BGP OBJECT ATTRIBUTES
    mainObj.configMultivalue(bgpAttributeMultivalue['flap'], multivalueType='valueList',
                             data={'values': ['true', 'true']})
    mainObj.configMultivalue(bgpAttributeMultivalue['uptimeInSec'],   multivalueType='singleValue', data={'value': '60'})
    mainObj.configMultivalue(bgpAttributeMultivalue['downtimeInSec'], multivalueType='singleValue', data={'value': '30'})

    protocolObj.startAllProtocols()
    protocolObj.verifyProtocolSessionsUp()

    trafficObj = Traffic(mainObj)
    trafficObj.startTraffic(regenerateTraffic=True, applyTraffic=True)

    # Check the traffic state before getting stats.
    #    Use one of the below APIs based on what you expect the traffic state should be before calling stats.
    #    If you expect traffic to be stopped such as in fixedFrameCount and fixedDuration
    #    or do you expect traffic to be started such as in continuous mode
    #trafficObj.checkTrafficState(expectedState=['stopped'], timeout=45)
    trafficObj.checkTrafficState(expectedState=['started'], timeout=45)

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
