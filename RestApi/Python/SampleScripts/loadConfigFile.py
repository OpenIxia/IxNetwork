
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
#        - Using ReST API to load a saved BGP configurations using two back-to-back Ixia ports.
#        - Supports Windows, Windows Connection Mgr and Linux API server.
#
#    - Connects to the chassis and verify port availability.
#    - Load a saved BGP config file.
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
# USAGE
#    python <script>.py windows
#    python <script>.py linux

import sys, traceback

sys.path.insert(0, '../Modules/Main')
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiProtocol import Protocol
from IxNetRestApiTraffic import Traffic
from IxNetRestApiStatistics import Statistics

# Default the API server to either windows or linux.
connectToApiServer = 'windows'

# For accepting command line parameters: windows or linux
if len(sys.argv) > 1:
    if sys.argv[1] not in ['windows', 'windowsConnectionMgr', 'linux']:
        sys.exit("\nError: %s is not a known option. Choices are 'windows', 'windowsConnectionMgr or 'linux'." % sys.argv[1])
    connectToApiServer = sys.argv[1]

try:
    #---------- Preference Settings --------------
    forceTakePortOwnership = True
    releasePortsWhenDone = False
    enableDebugTracing = False
    deleteSessionAfterTest = True
    licenseServerIp = '192.168.70.3'
    licenseModel = 'subscription'
    licenseTier = 'tier3'

    configFile = 'bgp_ngpf_8.30.ixncfg'

    ixChassisIp = '192.168.70.11'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'],
                [ixChassisIp, '2', '1']]

    if connectToApiServer == 'linux':
        mainObj = Connect(apiServerIp='192.168.70.108',
                                serverIpPort='443',
                                username='admin',
                                password='admin',
                                deleteSessionAfterTest=deleteSessionAfterTest,
                                verifySslCert=False,
                                serverOs='linux')

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

    fileMgmtObj = FileMgmt(mainObj)
    fileMgmtObj.loadConfigFile(configFile)
    portObj.assignPorts(portList)
    portObj.verifyPortState()

    protocolObj = Protocol(mainObj, portObj)

    # MODIFY BGP CONFIG:
    #    Step 1 of 2:  Get the BGP host object.
    #                  Filter the BGP host by it's Topology Group name.
    #                  State all the BGP attributes to modify in a list.
    bgpAttributeMultivalue = protocolObj.getBgpObject(topologyName='Topo1', bgpAttributeList=['flap', 'uptimeInSec', 'downtimeInSec'])

    # Step 2 of 2: MODIFY THE BGP OBJECT ATTRIBUTES
    mainObj.configMultivalue(bgpAttributeMultivalue['flap'],          multivalueType='valueList',   data={'values': ['true', 'true']})
    mainObj.configMultivalue(bgpAttributeMultivalue['uptimeInSec'],   multivalueType='singleValue', data={'value': '60'})
    mainObj.configMultivalue(bgpAttributeMultivalue['downtimeInSec'], multivalueType='singleValue', data={'value': '30'})

    protocolObj.startAllProtocols()
    protocolObj.verifyArp(ipType='ipv4')
    protocolObj.verifyAllProtocolSessionsNgpf(timeout=120)

    trafficObj = Traffic(mainObj)
    trafficObj.regenerateTrafficItems()
    trafficObj.applyTraffic()
    trafficObj.startTraffic()

    # Uncomment this if traffic is fixed packet count because you want to assure that
    # the stats are completely stopped before getting stats.
    #mainObj.checkTrafficState(expectedState=['stopped', 'stoppedWaitingForStats'], timeout=45)

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
    if 'mainObj' in locals() and connectToApiServer == 'windows':
        if releasePortsWhenDone and forceTakePortOwnership:
            portObj.releasePorts(portList)
        if connectToApiServer == 'windowsConnectionMgr':
            mainObj.deleteSession()
