
# PLEASE READ DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# REQUIREMENTS
#    - Python modules: requests
#
# DESCRIPTION
#    A sample utility script to:
#        - Read a saved JSON config file into an JSON object..
#        - Load the configuration:  Import the JSON config object to IxNetwork.
#        - Start all protocols.
#        - Verify protocol sessions including ARP.
#        - Start traffic.
#        - Get stats.
#

import json, sys

sys.path.insert(0, '../../Modules')
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiProtocol import Protocol
from IxNetRestApiTraffic import Traffic
from IxNetRestApiStatistics import Statistics

def help():
    print()
    print('Command line parameters:')
    print('------------------------')
    print('\t-jsonFile: The json config file to load')
    print('\t-windows:  Load config file in a Windows API server')
    print('\t-linux:    Load config file in a Linux API server')
    print('\t-windowsConnectionMgr: Load config file in a Windows Server running IxNetwork Connection Manager')
    print()


# Default the API server to either windows or linux.
connectToApiServer = 'windows'

parameters = sys.argv[1:]
argIndex = 0
while argIndex < len(parameters):
    currentArg = parameters[argIndex]
    if currentArg == '-windows':
        connectToApiServer = 'windows'
        argIndex += 1
    elif currentArg == '-linux':
        connectToApiServer = 'linux'
        argIndex += 1
    elif currentArg == '-windowsConnectionMgr':
        connectToApiServer = 'windowsConnectionMgr'
        argIndex += 1
    elif currentArg == '-jsonFile':
        jsonConfigFile = parameters[argIndex+1]
        argIndex += 2
    elif currentArg == 'help':
        help()
        sys.exit()
    else:
        sys.exit('\nNo such parameter: %s' % currentArg)

if os.path.isfile(jsonConfigFile) == False:
    raise IxNetRestApiException("JSON config file doesn't exists: %s" % jsonConfigFile)

with open(jsonConfigFile.strip()) as inFile:
    jsonData = json.load(inFile)

if connectToApiServer == 'linux':
    # Verify if mandatory parameters are included in the json config file.
    if 'linuxApiServerIp' not in jsonData:
        sys.exit('\nError: JSON config file is missing the linuxApiServerIp parameter/value\n')
    if 'linuxApiServerPort' not in jsonData:
        sys.exit('\nError: JSON config file is missing the linuxApiServerPort parameter/value\n')

try:
    #---------- Preference Settings --------------

    forceTakePortOwnership = jsonData['forceTakePortOwnership']
    releasePortsWhenDone = jsonData['releasePortsWhenDone']
    enableDebugTracing = jsonData['enableDebugTracing']
    deleteSessionAfterTest = jsonData['deleteSessionAfterTest']
    
    licenseServerIsInChassis = False
    licenseServerIp = jsonData['licenseServerIp']
    licenseModel = jsonData['licenseModel']
    licenseTier = jsonData['licenseTier']

    ixChassisIp = jsonData['availableHardware']['chassis'][0]['hostname']

    portList = []
    # Dynamically build the portList by reading the JSON config file searching for all the ports in it.
    for vport in jsonData['vport']:
        card = vport['connectedTo'].split('/')[-2]
        matchCard = re.match('card\[([0-9]+)]', card)
        port = vport['connectedTo'].split('/')[-1]
        matchPort = re.match('port\[([0-9]+)]', port)
        portList.append([ixChassisIp, matchCard.group(1), matchPort.group(1)]) 

    if connectToApiServer == 'linux':
        mainObj = Connect(apiServerIp = jsonData['linuxApiServerIp'],
                          serverIpPort = jsonData['linuxServerIpPort'],
                          username = jsonData['username'],
                          password = jsonData['password'],
                          deleteSessionAfterTest = jsonData['deleteSessionAfterTest'],
                          verifySslCert = False,
                          serverOs ='linux')

    if connectToApiServer in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp=jsonData['windowsApiServerIp'], serverIpPort=jsonData['windowsServerIpPort'], serverOs=connectToApiServer)

    #---------- Preference Settings End --------------
    fileMgmtObj = FileMgmt(mainObj)
    
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
    if licenseServerIsInChassis == False:
        portObj.releaseAllPorts()
        mainObj.configLicenseServerDetails([licenseServerIp], licenseModel, licenseTier)

    fileMgmtObj.importJsonConfigFile(jsonConfigFile, option='newConfig')
    fileMgmtObj.jsonAssignPorts(jsonData, portList, timeout=90)
    portObj.verifyPortState()

    protocolObj = Protocol(mainObj)
    protocolObj.startAllProtocols()
    protocolObj.verifyArp(ipType='ipv4')
    protocolObj.verifyAllProtocolSessionsNgpf(timeout=120)

    trafficObj = Traffic(mainObj)
    trafficObj.regenerateTrafficItems()
    trafficObj.startTraffic()

    # Uncomment this if traffic is fixed packet count because you want to assure that
    # the stats are completely stopped before getting stats
    #trafficObj.checkTrafficState(expectedState=['stopped', 'stoppedWaitingForStats'], timeout=45)

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
        if deleteSessionAfterTest:
            mainObj.linuxServerStopAndDeleteSession()
    if 'mainObj' in locals() and connectToApiServer in ['windows', 'windowsConnectionMgr']:
        if releasePortsWhenDone and forceTakePortOwnership:
            portObj.releasePorts(portList)
        if connectToApiServer == 'windowsConnectionMgr':
            if deleteSessionAfterTest:
                mainObj.deleteSession()




