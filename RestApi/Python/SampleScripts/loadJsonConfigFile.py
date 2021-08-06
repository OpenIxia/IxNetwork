
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
#    A sample script to:
#        - Load a saved JSON configuration file.
#        - Modify just the BGP configuration using XPATH's from the JSON config file.
#        - Start all protocols.
#        - Verify protocol sessions including ARP.
#        - Start traffic.
#        - Get stats.


import re, json, os, sys, traceback

# These  modules are one level above.
sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules'))))
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiProtocol import Protocol
from IxNetRestApiTraffic import Traffic
from IxNetRestApiStatistics import Statistics

# Default the API server to either windows or linux.
osPlatform = 'linux'

try:
    #---------- Preference Settings --------------

    forceTakePortOwnership = True
    releasePortsWhenDone = False
    deleteSessionAfterTest = True
    
    currentDir = os.path.abspath(os.path.dirname(__file__))
    jsonConfigFile = f'{currentDir}/bgp_ngpf_8.50.json'

    licenseServerIp = '172.16.101.3'
    licenseModel = 'subscription'
    licenseTier = 'tier3'

    ixChassisIp = '172.16.102.5'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'],
                [ixChassisIp, '1', '2']]

    # For Novus cards only:
    #     Novus cards support multiple media types. When assigning port, it will default to fiber.
    #     Use this variable to set your port media type correctly.
    modifyPortMediaType = None ;# None or copper|fiber|SGMII

    if osPlatform == 'linux':
        mainObj = Connect(apiServerIp='172.16.102.2',
                          serverIpPort='443',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs='linux',
                          generateLogFile='ixiaDebug.log',
                          traceLevel='all'
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

    portObj = PortMgmt(mainObj)
    portObj.connectIxChassis(ixChassisIp)

    if portObj.arePortsAvailable(portList, raiseException=False) != 0:
        if forceTakePortOwnership == True:
            portObj.releasePorts(portList)
            portObj.clearPortOwnership(portList)
        else:
            raise IxNetRestApiException('\nPorts are owned by another user and forceTakePortOwnership is set to False. Exiting test.')

    fileMgmtObj = FileMgmt(mainObj)
    fileMgmtObj.importJsonConfigFile(jsonConfigFile, option='newConfig')

    portObj.releasePorts(portList)
    mainObj.configLicenseServerDetails([licenseServerIp], licenseModel, licenseTier)

    # Set configPortName=False because loading a saved config file assumes ports already have configured names. Don't overwrite them.
    portObj.assignPorts(portList, forceTakePortOwnership, configPortName=False)

    if modifyPortMediaType:
        portObj.modifyPortMediaType(portList=portList, mediaType=modifyPortMediaType)
        portObj.verifyPortState()

    # Example: How to modify
    #    Mofify the BGP configuration using JSON XPATH. XPATH are obtained from a JSON exported config file.
    #       1> Export the JSON configuration to a file.
    #       2> Get the XPATH for what you want to modify the configuraiton.
    #       3> Import the modified JSON data object to IxNetwork.
    xpathObj = [{"xpath": "/multivalue[@source = '/topology[1]/deviceGroup[1]/ethernet[1]/ipv4[1]/bgpIpv4Peer[1] flap']/singleValue",
                 "value": "true"},
                {"xpath": "/multivalue[@source = '/topology[1]/deviceGroup[1]/ethernet[1]/ipv4[1]/bgpIpv4Peer[1] uptimeInSec']/singleValue",
                 "value": "28"},
                {"xpath": "/multivalue[@source = '/topology[1]/deviceGroup[1]/ethernet[1]/ipv4[1]/bgpIpv4Peer[1] downtimeInSec']/singleValue",
                 "value": "68"}
            ]

    fileMgmtObj.importJsonConfigObj(dataObj=xpathObj, option='modify')

    protocolObj = Protocol(mainObj)
    protocolObj.startAllProtocols()
    protocolObj.verifyProtocolSessionsUp()

    trafficObj = Traffic(mainObj)
    trafficObj.startTraffic(regenerateTraffic=True, applyTraffic=True)

    # Check the traffic state before getting stats.
    #    Use one of the below APIs based on what you expect the traffic state should be before calling stats.
    #    'stopped': If you expect traffic to be stopped such as for fixedFrameCount and fixedDuration.
    #    'started': If you expect traffic to be started such as in continuous mode.
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




