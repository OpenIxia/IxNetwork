
# PLEASE READ DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# REQUIREMENTS
#    - Python modules: requests
#
# DESCRIPTION
#    This sample script demonstrates:
#        - Read a parameter file using JSON data structure.
#        - Testing with two back-to-back Ixia ports.
#        - This utility is scalable.  Meaning you could create n number of Topology Groups and Traffic Items.
#        - The JSON config file model reflects the IxNework API tree structure.
#        - Connecting to Windows IxNetwork API server or Linux API server.
#        - Written in Python3 and supports Python 2 
#        - Verify for sufficient amount of port licenses before testing.
#        - Verify port ownership.
#        - Configure two Topology Groups
#        - Start protocols
#        - Verify protocol sessions
#        - Create a Traffic Item
#        - Apply Traffic
#        - Start Traffic
#        - Get stats
#

import sys, json, traceback

sys.path.insert(0, '../../Modules')
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiTraffic import Traffic
from IxNetRestApiProtocol import Protocol
from IxNetRestApiStatistics import Statistics

parameters = sys.argv[1:]
argIndex = 0
while argIndex < len(parameters):
    currentArg = parameters[argIndex]

    if bool(re.match(currentArg, '-connectToApiServer', re.I)):
        connectToApiServer = parameters[argIndex + 1]
        if connectToApiServer not in ['windows', 'windowsConnectionMgr', 'linux']:
            raise IxNetRestApiException("\nError: %s is not a known option. Choices are 'windows' or 'linux'." % connectToApiServer)
        argIndex += 2

    elif bool(re.match(currentArg, '-paramFile', re.I)):
        paramFile = parameters[argIndex + 1]
        if os.path.exists(paramFile) is False:
            raise IxNetRestApiException("JSON param file doesn't exists: %s" % paramFile)
        argIndex += 2

    else:
        raise IxNetRestApiException('\nNo such parameter: %s' % currentArg)

if 'paramFile' not in locals():
    sys.exit('\nError: You need to include -paramFile <file>\n')

with open(paramFile.strip()) as inFile:
    jsonData = json.load(inFile)

def configDeviceGroupProtocolStack(deviceGroupObj, deviceGroupJsonData):
    for ethernet in deviceGroupJsonData['ethernet']:
        ethernetObj = protocolObj.createEthernetNgpf(
            deviceGroupObj,
            ethernetName = ethernet['name'],
            macAddress = {'start': ethernet['macAddress']['start'],
                          'direction': ethernet['macAddress']['direction'],
                          'step': ethernet['macAddress']['step']
                      },
            macAddressPortStep = ethernet['macAddress']['portStep'],
            vlanId = {'start': ethernet['vlanId']['start'],
                      'direction': ethernet['vlanId']['direction'],
                      'step': ethernet['vlanId']['step']
                })

        if 'ipv4'in ethernet:
            for ipv4 in ethernet['ipv4']:
                ipv4Obj = protocolObj.createIpv4Ngpf(
                    ethernetObj,
                    ipv4Address = {'start': ipv4['address']['start'],
                                   'direction': ipv4['address']['direction'],
                                   'step': ipv4['address']['step']},
                    ipv4AddressPortStep = ipv4['address']['portStep'],
                    gateway = {'start': ipv4['gateway']['start'],
                               'direction': ipv4['gateway']['direction'],
                               'step': ipv4['gateway']['step']},
                    gatewayPortStep = ipv4['gateway']['portStep'],
                    prefix = ipv4['prefix'])

                if 'bgp' in ipv4:
                    for bgp in ipv4['bgp']:
                        bgpObj = protocolObj.configBgp(ipv4Obj,
                                                       name = bgp['name'],
                                                       enableBgp = True,
                                                       dutIp = {'start': bgp['dutIp']['start'],
                                                                'direction': bgp['dutIp']['direction'],
                                                                'step': bgp['dutIp']['step']
                                                            },
                                                       localAs2Bytes = bgp['localAs2Bytes'],
                                                       type = bgp['type'])
                if 'ospf' in ipv4:
                    for ospf in ipv4['ospf']:
                        ospfObj = protocolObj.configOspf(ipv4Obj,
                                                         name = ospf['name'],
                                                         areaId = ospf['areaId'],
                                                         neighborIp =ospf['neighborIp'],
                                                         helloInterval = ospf['helloInterval'],
                                                         areaIdIp = ospf['areaIp'],
                                                         networkType = ospf['networkType'],
                                                         deadInterval = ospf['deadInterval'])

        if 'networkGroup' in deviceGroup:
            for networkGroup in deviceGroup['networkGroup']:
                networkGroupObj = protocolObj.configNetworkGroup(
                    create = deviceGroupObj,
                    name = networkGroup['name'],
                    multiplier = networkGroup['multiplier'],
                    networkAddress = {'start': networkGroup['routeRange']['start'],
                                      'step': networkGroup['routeRange']['step'],
                                      'direction': networkGroup['routeRange']['direction']
                                  },
                    prefixLength = networkGroup['prefix'])


try:
    if jsonData['connectToApiServer'] == 'linux':
        mainObj = Connect(apiServerIp=jsonData['apiServerIp'],
                          serverIpPort=jsonData['linuxServerIpPort'],
                          username=jsonData['usename'],
                          password=jsonData['password'],
                          deleteSessionAfterTest=jsonData['deleteSessionAfterTest'],
                          verifySslCert=jsonData['verifySslCert'],
                          serverOs=jsonData['connectToApiServer']
                          )

    if jsonData['connectToApiServer'] in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp=jsonData['apiServerIp'],
                          serverIpPort=jsonData['windowsServerIpPort'],
                          serverOs=jsonData['connectToApiServer'],
                          deleteSessionAfterTest=jsonData['deleteSessionAfterTest']
                          )

    #---------- Preference Settings End --------------

    portObj = PortMgmt(mainObj)
    portObj.connectIxChassis(jsonData['ixChassisIp'])

    if portObj.arePortsAvailable(jsonData['portList'], raiseException=False) != 0:
        if jsonData['forceTakePortOwnership'] == True:
            portObj.releasePorts(jsonData['portList'])
            portObj.clearPortOwnership(jsonData['portList'])
        else:
            raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')

    # Configuring license requires releasing all ports even for ports that is not used for this test.
    portObj.releaseAllPorts()
    mainObj.configLicenseServerDetails([jsonData['licenseServerIp']], jsonData['licenseModel'], jsonData['licenseTier'])

    mainObj.newBlankConfig()

    # Set createVports = True if building config from scratch.
    portObj.assignPorts(jsonData['portList'], createVports=True)
    protocolObj = Protocol(mainObj, portObj)

    for topologyGroup in jsonData['topology']:
        topologyObj = protocolObj.createTopologyNgpf(portList=topologyGroup['ports'],
                                                     topologyName=topologyGroup['name'])
        
        for deviceGroup in topologyGroup['deviceGroup']:
            deviceGroupObj = protocolObj.createDeviceGroupNgpf(topologyObj,
                                                               multiplier=deviceGroup['multiplier'],
                                                               deviceGroupName=deviceGroup['name'])

            configDeviceGroupProtocolStack(deviceGroupObj, deviceGroup)

            # Optional: Create a Device Group inside a Device Group.
            #           Example: VxLAN and LACP requirements
            if 'deviceGroup' in deviceGroup:
                for deviceGroupOuter in deviceGroup['deviceGroup']:
                    deviceGroupObj2 = protocolObj.createDeviceGroupNgpf(deviceGroupObj,
                                                                       multiplier=deviceGroupOuter['multiplier'],
                                                                       deviceGroupName=deviceGroupOuter['name'])

                    configDeviceGroupProtocolStack(deviceGroupObj2, deviceGroupOuter)

    protocolObj.startAllProtocols()
    protocolObj.verifyProtocolSessionsNgpf()

    # For all traffic parameter options, go to the API configTrafficItem.
    # mode = create or modify
    endpointList = []
    match = re.match('http.*(/api.*ixnetwork)', mainObj.sessionUrl)
    sessionHeader = match.group(1)

    for trafficItem in jsonData['trafficItem']:
        endpoints = {}
        endpoints['sources'] = []
        endpoints['destinations'] = []
        for endpoint in trafficItem['endpoints']:
            if 'name' in endpoint:
                endpoints['name'] = endpoint['name']
            for sources in endpoint['sources']:
                endpoints['sources'].append(sessionHeader + sources)
            for destinations in endpoint['destinations']:
                endpoints['destinations'].append(sessionHeader + destinations)
        endpointList.append(endpoints)

        trafficObj = Traffic(mainObj)
        trafficStatus = trafficObj.configTrafficItem(
            mode='create',            
            trafficItem = {
                'name': trafficItem['name'],
                'trafficType': trafficItem['trafficType'],
                'biDirectional': trafficItem['bidirectional'],
                'trackBy': trafficItem['trackBy']
            },
            endpoints = trafficItem['endpoints'],
            configElements = trafficItem['configElements']
        )

    configElementObj = trafficStatus[2][0]
    trafficObj.regenerateTrafficItems()
    trafficObj.startTraffic()

    # Check the traffic state to assure traffic has stopped before checking for stats.
    if trafficObj.getTransmissionType(configElementObj) == "fixedFrameCount":
        trafficObj.checkTrafficState(expectedState=['stopped', 'stoppedWaitingForStats'], timeout=45)

    statObj = Statistics(mainObj)
    stats = statObj.getStats(viewName='Flow Statistics', silentMode=False)

    # Example to show how to get specific stats from the stats dictionary that contains all the stats.
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

    if jsonData['releasePortsWhenDone'] == True:
        portObj.releasePorts(portList)

    if jsonData['connectToApiServer'] == 'linux':
        mainObj.linuxServerStopAndDeleteSession()

    if jsonData['connectToApiServer'] == 'windowsConnectionMgr':
        mainObj.deleteSession()

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    if jsonData['enableDebugTracing']:
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())
    print('\nException Error! %s\n' % errMsg)
    if 'mainObj' in locals() and jsonData['connectToApiServer'] == 'linux':
        if jsonData['deleteSessionAfterTest']:
            mainObj.linuxServerStopAndDeleteSession()
    if 'mainObj' in locals() and jsonData['connectToApiServer'] in ['windows', 'windowsConnectionMgr']:
        if jsonData['releasePortsWhenDone'] and jsonData['forceTakePortOwnership']:
            portObj.releasePorts(portList)
        if jsonData['connectToApiServer'] == 'windowsConnectionMgr':
            if jsonData['deleteSessionAfterTest']:
                mainObj.deleteSession()
