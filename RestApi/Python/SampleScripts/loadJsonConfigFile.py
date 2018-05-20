
# PLEASE READ DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# REQUIREMENTS
#    - Python2.7 - 3.6
#    - Python modules: requests
#
# DESCRIPTION
#    A sample script to:
#        - Read a saved JSON config file into an JSON object..
#        - Load the configuration:  Import the JSON config object to IxNetwork.
#        - Modify just the BGP configuration fragments.
#          Two ways to do this:
#             1> Using the XPATH.
#             2> Using the JSON config object in Dict format.
#        - Start all protocols.
#        - Verify protocol sessions including ARP.
#        - Start traffic.
#        - Get stats.


import json, sys

sys.path.insert(0, '../Modules')
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiProtocol import Protocol
from IxNetRestApiTraffic import Traffic
from IxNetRestApiStatistics import Statistics

# Default the API server to either windows or linux.
osPlatform = 'windows'

# Optional: Command line parameters: windows or linux
if len(sys.argv) > 1:
    if sys.argv[1] not in ['windows', 'windowsConnectionMgr', 'linux']:
        sys.exit("\nError: %s is not a known option. Choices are 'windows', 'windowsConnectionMgr or 'linux'." % sys.argv[1])
    osPlatform = sys.argv[1]

try:
    #---------- Preference Settings --------------

    forceTakePortOwnership = True
    releasePortsWhenDone = False
    enableDebugTracing = True
    deleteSessionAfterTest = True
    jsonConfigFile = 'bgp.json'

    licenseIsInChassis = False
    licenseServerIp = '192.168.70.3'
    licenseModel = 'subscription'
    licenseTier = 'tier3'

    ixChassisIp = '192.168.70.11'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'],
                [ixChassisIp, '2', '1']]

    if osPlatform == 'linux':
        mainObj = Connect(apiServerIp='192.168.70.108',
                          serverIpPort='443',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs='linux')

    if osPlatform in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='192.168.70.3',
                          serverIpPort='11009',
                          serverOs=osPlatform,
                          deleteSessionAfterTest=deleteSessionAfterTest)

    #---------- Preference Settings End --------------

    portObj = PortMgmt(mainObj)
    portObj.connectIxChassis(ixChassisIp)

    if portObj.arePortsAvailable(portList, raiseException=False) != 0:
        if forceTakePortOwnership == True:
            portObj.releasePorts(portList)
            portObj.clearPortOwnership(portList)
        else:
            raise IxNetRestApiException('\nPorts are owned by another user and forceTakePortOwnership is set to False. Exiting test.')

    # If the license is activated on the chassis's license server, this variable should be True.
    # Otherwise, if the license is in a remote server or remote chassis, this variable should be False.
    # Configuring license requires releasing all ports even for ports that is not used for this test.
    if licenseIsInChassis == False:
        portObj.releaseAllPorts()
        mainObj.configLicenseServerDetails([licenseServerIp], licenseModel, licenseTier)

    fileMgmtObj = FileMgmt(mainObj)
    jsonData = fileMgmtObj.jsonReadConfig(jsonConfigFile)

    fileMgmtObj.importJsonConfigFile(jsonConfigFile, option='newConfig')
    fileMgmtObj.jsonAssignPorts(jsonData, portList, timeout=300)
    portObj.verifyPortState()

    # Example: How to modify
    #    Mofify the BGP configuration using JSON XPATH. XPATH are obtained from a JSON exported config file.
    #       1> Export the JSON configuration to a file.
    #       2> Get the XPATH to where you want to modify the configuraiton.
    #       3> Import the modified JSON to IxNetwork
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
    protocolObj.verifyArp(ipType='ipv4')
    protocolObj.verifyProtocolSessionsUp(protocolViewName='BGP Peer Per Port', timeout=120)

    trafficObj = Traffic(mainObj)
    trafficObj.startTraffic(regenerateTraffic=True, applyTraffic=True)

    # Check the traffic state before getting stats.
    #    Use one of the below APIs based on what you expect the traffic state should be before calling stats.
    #    If you expect traffic to be stopped such as for fixedFrameCount and fixedDuration
    #    or do you expect traffic to be started such as in continuous mode.
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




