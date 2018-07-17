
# PLEASE READ DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# REQUIREMENTS
#    - Python modules: requests
#
# DESCRIPTION
#    A dynamic sample script that...
# 
#        - Read a parameter file that is in a Python dictionary data structure.
#        - Testing with two back-to-back Ixia ports.
#        - This script is scalable.  Meaning you could create n number of Topology Groups and Traffic Items.
#        - The dictionary parameter file model reflects the IxNework API tree structure.
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

import sys, traceback

sys.path.insert(0, '../../Modules')
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiTraffic import Traffic
from IxNetRestApiProtocol import Protocol
from IxNetRestApiStatistics import Statistics

osPlatform = 'windows'
parameters = sys.argv[1:]
argIndex = 0
while argIndex < len(parameters):
    currentArg = parameters[argIndex]

    if bool(re.match(currentArg, '-osPlatform', re.I)):
        osPlatform = parameters[argIndex + 1]
        if osPlatform not in ['windows', 'windowsConnectionMgr', 'linux']:
            raise IxNetRestApiException("\nError: %s is not a known option. Choices are 'windows' or 'linux'." % osPlatform)
        argIndex += 2

    elif bool(re.match(currentArg, '-paramFile', re.I)):
        paramFile = parameters[argIndex + 1]
        if '.py' in paramFile:
            paramFile = paramFile.split('.')[0]
        argIndex += 2

    elif bool(re.match(currentArg, 'help', re.I)):
        print('\nconfigIxNetwork Parameters')
        print('----------------------------')
        print('\t-osPlatform: defaults to windows. Options: windows|windowsConnectionMgr|linux')
        print('\t-paramFile: The Python dictionary module file to input')
        print()
        sys.exit()
    else:
        raise IxNetRestApiException('\nNo such parameter: %s' % currentArg)

if 'paramFile' not in locals():
    sys.exit('\nError: You need to include -paramFile <file>\n')

if os.path.exists(paramFile+'.py') is False:
    raise IxNetRestApiException("JSON param file doesn't exists: %s" % paramFile)

param = __import__(paramFile).params

def configDeviceGroupProtocolStack(deviceGroupObj, deviceGroupData):
    for ethernet in deviceGroupData['ethernet']:
        ethernetObj = protocolObj.createEthernetNgpf(
            deviceGroupObj,
            ethernetName = ethernet['name'],
            macAddress = {'start': ethernet['macAddress']['start'],
                          'direction': ethernet['macAddress']['direction'],
                          'step': ethernet['macAddress']['step']
                      },
            macAddressPortStep = ethernet['macAddressPortStep'],
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
                    ipv4AddressPortStep = ipv4['ipv4AddressPortStep'],
                    gateway = {'start': ipv4['gateway']['start'],
                               'direction': ipv4['gateway']['direction'],
                               'step': ipv4['gateway']['step']},
                    gatewayPortStep = ipv4['gatewayPortStep'],
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

        if 'networkGroup' in deviceGroupData:
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
    if osPlatform == 'linux':
        mainObj = Connect(apiServerIp=param['linuxApiServerIp'],
                          serverIpPort=param['linuxServerIpPort'],
                          username=param['usename'],
                          password=param['password'],
                          deleteSessionAfterTest=param['deleteSessionAfterTest'],
                          verifySslCert=param['verifySslCert'],
                          serverOs=osPlatform
                          )

    if osPlatform in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp=param['windowsApiServerIp'],
                          serverIpPort=param['windowsServerIpPort'],
                          serverOs=osPlatform,
                          deleteSessionAfterTest=param['deleteSessionAfterTest']
                          )

    #---------- Preference Settings End --------------

    portObj = PortMgmt(mainObj)
    portObj.connectIxChassis(param['ixChassisIp'])

    if portObj.arePortsAvailable(param['portList'], raiseException=False) != 0:
        if param['forceTakePortOwnership'] == True:
            portObj.releasePorts(param['portList'])
            portObj.clearPortOwnership(param['portList'])
        else:
            raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')

    mainObj.newBlankConfig()

    # If the license is activated on the chassis's license server, this variable should be True.
    # Otherwise, if the license is in a remote server or remote chassis, this variable should be False.
    # Configuring license requires releasing all ports even for ports that is not used for this test.
    if param['configLicense'] == True:
        portObj.releaseAllPorts()
        mainObj.configLicenseServerDetails(param['licenseServerIp'], param['licenseModel'], param['licenseTier'])

    # Set createVports = True if building config from scratch.
    portObj.assignPorts(param['portList'])
    protocolObj = Protocol(mainObj)

    for topologyGroup in param['topology']:
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
    #endpointList = []
    #match = re.match('http.*(/api.*ixnetwork)', mainObj.sessionUrl)
    #sessionHeader = match.group(1)

    for trafficItem in param['trafficItem']:
        '''
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
        '''

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

    trafficObj.startTraffic(regenerateTraffic=True, applyTraffic=True)

    # Check the traffic state to assure traffic has stopped before checking for stats.
    if trafficObj.getTransmissionType(configElementObj) in ["fixedFrameCount", "fixedDuration"]:
        trafficObj.checkTrafficState(expectedState=['stopped'], timeout=45)

    if trafficObj.getTransmissionType(configElementObj) in ["continuous"]:
        trafficObj.checkTrafficState(expectedState=['started'], timeout=45)

    statObj = Statistics(mainObj)
    stats = statObj.getStats(viewName='Flow Statistics')

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

    if param['releasePortsWhenDone'] == True:
        portObj.releasePorts(portList)

    if osPlatform == 'linux':
        mainObj.linuxServerStopAndDeleteSession()

    if osPlatform == 'windowsConnectionMgr':
        mainObj.deleteSession()

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    if param['enableDebugTracing']:
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())
    print('\nException Error! %s\n' % errMsg)
    if 'mainObj' in locals() and osPlatform == 'linux':
        if param['deleteSessionAfterTest']:
            mainObj.linuxServerStopAndDeleteSession()
    if 'mainObj' in locals() and osPlatform in ['windows', 'windowsConnectionMgr']:
        if param['releasePortsWhenDone'] and param['forceTakePortOwnership']:
            portObj.releasePorts(portList)
        if osPlatform == 'windowsConnectionMgr':
            if param['deleteSessionAfterTest']:
                mainObj.deleteSession()
