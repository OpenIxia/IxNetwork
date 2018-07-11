
# PLEASE READ DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# REQUIREMENTS
#    - Python modules: requests and napalm
#    
# DESCRIPTION
#    This sample script demonstrates:
#        - Using ReST API to load a saved BGP configurations.
#        - Ixia ports connecting to a virtual DUT.
#        - Full reference guide could be found in ../../Automation Getting Started.docx
# 
#    Supports Windows, Windows Connection Mgr and Linux API server.
#
# USAGE
#    python <script>.py windows
#    python <script>.py linux

import sys, traceback, pprint, napalm

sys.path.insert(0, '../Modules')
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiProtocol import Protocol
from IxNetRestApiTraffic import Traffic
from IxNetRestApiStatistics import Statistics

# Default the API server to either windows or linux.
osPlatform = 'windows'

# For accepting command line parameters: windows or linux
if len(sys.argv) > 1:
    if sys.argv[1] not in ['windows', 'windowsConnectionMgr', 'linux']:
        sys.exit("\nError: %s is not a known option. Choices are 'windows', 'windowsConnectionMgr or 'linux'." % sys.argv[1])
    osPlatform = sys.argv[1]

try:
    #---------- Preference Settings --------------
    forceTakePortOwnership = True
    releasePortsWhenDone = False
    enableDebugTracing = False
    deleteSessionAfterTest = True

    configLicense = True
    licenseServerIp = '10.36.79.226'
    licenseModel = 'subscription'
    licenseTier = 'tier3'

    configFile = 'C:\\IxiaAutomation\\RestApi\\Python\\SampleScripts\\bgp_dut_8.50.ixncfg'
    dutConfigFile = 'C:\\IxiaAutomation\\RestApi\\Python\\SampleScripts\\bgp_eos.cfg'

    ixChassisIp = '10.36.79.186'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'],
                [ixChassisIp, '1', '2']]

    if osPlatform == 'linux':
        mainObj = Connect(apiServerIp='192.168.70.108',
                          serverIpPort='443',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs='linux')

    if osPlatform in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='10.36.79.226',
                          serverIpPort='11009',
                          serverOs=osPlatform,
                          deleteSessionAfterTest=deleteSessionAfterTest)

    #---------- Preference Settings End --------------

    portObj = PortMgmt(mainObj)
    portObj.connectIxChassis(ixChassisIp)
    '''
    if portObj.arePortsAvailable(portList, raiseException=False) != 0:
        if forceTakePortOwnership == True:
            portObj.releasePorts(portList)
            portObj.clearPortOwnership(portList)
        else:
            raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')
    '''
    if configLicense == True:
        portObj.releaseAllPorts()
        mainObj.configLicenseServerDetails([licenseServerIp], licenseModel, licenseTier)

    fileMgmtObj = FileMgmt(mainObj)
    fileMgmtObj.loadConfigFile(configFile)

    portObj.assignPorts(portList)
    portObj.verifyPortState()

    #---------- load DUT configurations --------------    
    driver = napalm.get_network_driver('eos')
    device = driver(hostname='10.36.79.66', username='winscp',
                    password='winscp', optional_args={'port': 443})
    
    mainObj.logInfo('Opening ...')
    device.open()
    mainObj.logInfo('Loading replacement candidate ...')
    device.load_replace_candidate(filename=dutConfigFile)
    device.commit_config()
    device.close()
    mainObj.logInfo('Done.')

   #---------- Continue test --------------  
    protocolObj = Protocol(mainObj)
    protocolObj.startAllProtocols()
    protocolObj.verifyArp(ipType='ipv4')
    protocolObj.verifyProtocolSessionsUp(protocolViewName='BGP Peer Per Port', timeout=120)

    #---------- get DUT BGP peers --------------  
    dutBGPPeers = device.get_bgp_neighbors()
    pp = pprint.PrettyPrinter(indent=2)
    mainObj.logInfo("\nBGP Peers details in DUT\n")
    pp.pprint(dutBGPPeers)

    trafficObj = Traffic(mainObj)
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

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    if enableDebugTracing:
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())
    print('\nException Error! %s\n' % errMsg)
    if 'mainObj' in locals() and osPlatform == 'linux':
        if deleteSessionAfterTest:
            mainObj.linuxServerStopAndDeleteSession()
    if 'mainObj' in locals() and osPlatform in ['windows', 'windowsConnectionMgr']:
        if releasePortsWhenDone and forceTakePortOwnership:
            portObj.releasePorts(portList)
        if osPlatform == 'windowsConnectionMgr':
            if deleteSessionAfterTest:
                mainObj.deleteSession()
