import sys, traceback, time

sys.path.insert(0, '../Modules/Main')
from IxNetRestApi import *
from IxNetRestApiProtocol import Protocol
from IxNetRestApiTraffic import Traffic
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiStatistics import Statistics
from IxNetRestApiPacketCapture import PacketCapture

# Default the API server to either windows or linux.
connectToApiServer = 'windows'
deleteSessionAfterTest = True

if len(sys.argv) > 1 and sys.argv[1] not in ['windows', 'linux']:
    sys.exit("\nError: %s is not a known option. Choices are 'windows' or 'linux'." % sys.argv[1])
if len(sys.argv) > 1:
    connectToApiServer = sys.argv[1]

try:
    forceTakePortOwnership = True
    releasePortsWhenDone = False

    if connectToApiServer == 'linux':
        mainObj = Connect(apiServerIp='192.168.70.108',
                                serverIpPort='443',
                                username='admin',
                                password='admin',
                                deleteSessionAfterTest=deleteSessionAfterTest,
                                verifySslCert=False,
                                serverOs=connectToApiServer
                                )

    if connectToApiServer == 'windows':
        mainObj = Connect(apiServerIp='192.168.70.3', serverIpPort='11009')

    ixChassisIp = '192.168.70.11'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'],
                [ixChassisIp, '2', '2']]

    fileMgmtObj = FileMgmt(mainObj)
    fileMgmtObj.copyFileWindowsToLocalLinux('c:\\Results\\test', '.')
    sys.exit()

    protocolObj = Protocol(mainObj)
    #protocolObj.verifyProtocolSessionsNgpf(['/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1'])
    protocolObj.verifyArp()
    #protocolObj.getNgpfGatewayIpMacAddress('1.1.1.2')
    sys.exit()

    response = protocolObj.configRsvpTeLsps(ipv4Obj='/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1')
    #protocolObj.deleteRsvpTeLsps(rsvpTunnelObj='/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/rsvpteLsps/16')
    #protocolObj.startAllRsvpTeLsps()
    #protocolObj.startAllRsvpTeIf()
    sys.exit()

    trafficObj = Traffic(mainObj)
    topologyObj1 = '/api/v1/sessions/1/ixnetwork/topology/1'
    topologyObj2 = '/api/v1/sessions/1/ixnetwork/topology/2'


    trafficObj.configTrafficItem(mode='create',
                                 trafficItem = {'name':'Topo3 to Topo4',
                                                'trafficType':'ipv4',
                                                'biDirectional':True,
                                                'srcDestMesh':'one-to-one',
                                                'routeMesh':'oneToOne',
                                                'allowSelfDestined':False,
                                                'trackBy': ['flowGroup0', 'vlanVlanId0']},
                                 endpoints = [
                                     ({'name':'Flow-Group-1', 'sources': [topologyObj1], 'destinations': [topologyObj2]},
                                      {'highLevelStreamElements': (
                                          ({
                                              'transmissionType': 'fixedFrameCount',
                                              'frameCount': 10000,
                                              'frameRate': 18,
                                              'frameRateType': 'percentLineRate',
                                              'frameSize': 128
                                          }), 
                                          ({
                                              'transmissionType': 'fixedFrameCount',
                                              'frameCount': 20000,
                                              'frameRate': 28,
                                              'frameRateType': 'percentLineRate',
                                              'frameSize': 228
                                          })
                                      )}
                                  )],
                                 configElements = None)
    sys.exit()

    trafficStatus = trafficObj.configTrafficItem(mode='create',
                                                 trafficItem = {
                                                     'name':'Topo1 to Topo2',
                                                     'trafficType':'ipv4',
                                                     'biDirectional':True,
                                                     'srcDestMesh':'one-to-one',
                                                     'routeMesh':'oneToOne',
                                                     'allowSelfDestined':False,
                                                     'trackBy': ['flowGroup0', 'vlanVlanId0']
                                                 },
                                                 endpoints = [({'name':'Flow-Group-1',
                                                                'sources': [topologyObj1],
                                                                'destinations': [topologyObj2]}),
                                                          ],
                                                 configElements = [{'transmissionType': 'fixedFrameCount',
                                                                    'frameCount': 50000,
                                                                    'frameRate': 88,
                                                                    'frameRateType': 'percentLineRate',
                                                                    'frameSize': 128}])

    sys.exit()

    trafficItemName = 'Topo1 to Topo2'
    queryData = {'from': '/traffic',
                 'nodes': [{'node': 'trafficItem', 'properties': ['name'], 'where': [{'property': 'name', 'regex': trafficItemName}]},
                           {'node': 'configElement', 'properties': [], 'where': []}
                 ]}
    queryResponse = mainObj.query(data=queryData)
    configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
    print('\n--- ce:', configElementObj)
    sys.exit()

    trafficObj.configFramePayload('/traffic/trafficItem/1/configElement/1/framePayload', 'custom', False, 'abcdabcdedeadbeef')
    sys.exit()

    #protocolObj.sendPimV4JoinLeaveNgpf(routerId='192.0.0.3', multicastIpAddress='all', action='join')
    protocolObj.sendIgmpJoinLeaveNgpf(routerId='192.0.0.3', igmpHostUrl='http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1', multicastIpAddress='all', action='join')
    sys.exit()

    protocolObj.configBgpNumberOfAs(routerId='195.0.0.2', numberOfAs=4)
    sys.exit()

    response = protocolObj.configBgpAsPathSegmentListNumber('195.0.0.2', 3, [[0,28], [3,298], [4, 828]])
    sys.exit()

    protocolObj.configBgpAsSetMode(routerId='195.0.0.2', asSetMode="includelocalasasasseqconfederation")
    sys.exit()

    protocolObj = Protocol(mainObj)
    result = protocolObj.getRouteRangeAddressProtocolAndPort(routeRangeAddress='202.7.0.0')
    print('\nresult:', result)
    sys.exit()

    #protocolObj.activateRouterIdRouteRanges(routerId=['192.0.0.2'], routeRangeAddressList=None, protocol='ldp', activate=True)
    #protocolObj.activateRouterIdRouteRanges(routeRangeAddressList=[('192.0.0.2', ('202.11.0.0', '202.12.0.0')), ('192.0.0.3', 'all')],
    #                                                             protocol='ospf', activate=True)
    #sys.exit()

    # Works
    # protocolObj.activateRouterIdRouteRanges(routeRangeAddressList=[ [['192.0.0.2', '192.0.0.3'], ['202.11.0.0', '202.21.0.0']], [['192.0.0.1'], ['all']]  ],
    #                                                             protocol='ospf', activate=False)
    # sys.exit()

    # Works
    #protocolObj.activateRouterIdRouteRanges(routeRangeAddressList=[  [ ['192.0.0.1', '192.0.0.3'], ['202.3.0.0', '202.23.0.0']]],
    #                                                            protocol='ospf', activate=False)
    #sys.exit()

    # works
    # protocolObj.activateRouterIdRouteRanges(routeRangeAddressList=[  [ ['all'], ['202.13.0.0', '202.23.0.0', '203.5.0.0']]],
    #                                                           protocol='isis', activate=False)
    # sys.exit()

    # Works
    # protocolObj.activateRouterIdRouteRanges(routeRangeAddressList=[[['all'], ['all']]], protocol='ospf', activate=True)
    # sys.exit()

    mainObj.getStats(viewName='Flow Statistics')
    sys.exit()

    mainObj.activateRouterIdProtocol(routerId='194.0.0.3', protocol='ospf', activate=False)
    sys.exit()

    mainObj.activateProtocolRouteRange(routerId='192.0.0.2', protocol='ospf', activate=False)
    sys.exit()



    result = mainObj.sendPing(srcIpList=['1.1.1.3'], destIp='1.1.1.5')
    sys.exit()

    mainObj.activateRouterIdProtocol(routerId='192.3.0.8', activate=True, protocol='isisL3')
    sys.exit()

    result = mainObj.tgnStartTraffic(['BGP100_L4', 'BGP100_L4'])
    print('\n--- result:', result)
    sys.exit()

    mainObj.showTopologies()
    sys.exit()

    mainObj.verifyArp(ipType='ipv4')
    sys.exit()

    mainObj.verifyAllProtocolSessionsNgpf()
    sys.exit()

    mainObj.verifyProtocolSessionsUp('ISIS-L3 RTR Per Port')
    sys.exit()

    stats = mainObj.getStats(viewName='Traffic Item Statistics')

    mainObj.tgnStartTraffic('BGP100_L4')
    sys.exit()
    #mainObj.getMultivalueValues('/api/v1/sessions/1/ixnetwork/multivalue/277')
    #sys.exit()

    srcIp = mainObj.getRawTrafficItemSrcIp(['BGP100_L4'])
    print('\n--- srcIp:', srcIp)
    sys.exit()

    mainObj.getDeviceGroupSrcIpGatewayIp(srcIp)
    sys.exit()

    gatewayIpMacAddress = mainObj.getNgpfGatewayIpMacAddress(gatewayIp=srcIp)
    if gatewayIpMacAddress == 0 or 'Unresolved' in gatewayIpMacAddress:
        raise IxNetRestApiException('Gateway Mac is unresolved!')

    mainObj.modifyTrafficItemDestMacAddress('BGP100_L5', destMacAddress=gatewayIpMacAddress)
    mainObj.enableTrafficItemByName('BGP100_L5', enable=True)
    sys.exit()

    #r = mainObj.getMultivalueValues(multivalueObj='/api/v1/sessions/1/ixnetwork/multivalue/286', patternOffsetToGet=0, numberOfValuesToReturn=1)
    #print('++++', r)
    #sys.exit()

    #mainObj.verifyProtocolSessionsUp(protocolViewName='BGP Peer Per Port')
    #sys.exit()

    mainObj.verifyAllProtocolSessionsNgpf()
    sys.exit()

    srcIp = mainObj.getRawTrafficItemSrcIp('StaticRoute1_L5')
    print(srcIp)
    mainObj.getDeviceGroupSrcIpGatewayIp('10.3.0.2')
    sys.exit()

    #mainObj.activateRouterIdProtocols(routerId='192.4.0.4', activate=True, protocol='bgpIpv4Peer')


    # Export a configuration into a json config file
    #mainObj.exportJsonConfigFile(jsonFileName='jsonExportSample.json')

    # Export a configuration into a dictionary
    #jsonConfigDict = mainObj.exportJsonConfigToDict()
    #printDict(jsonConfigDict)

    # obj = mainObj.exportJsonConfig()
    #print('\n---', obj['traffic'])

    # packet capture
    # mainObj.packetCaptureConfigPortMode([ixChassisIp, '1', '15'], enableDataPlane=False, enableControlPlane=True)
    # mainObj.packetCaptureClearTabs()
    # mainObj.packetCaptureStart()
    # time.sleep(10)
    # mainObj.packetCaptureStop()

    #mainObj.startStopDeviceGroup(deviceGroupObjList='all', action='start')
    #mainObj.startStopDeviceGroup(deviceGroupObjList='all', action='stop')

    #portLicenseObj = verifyPortLicense.Connect(platform='chassis', licenseServerIp=ixChassisIp, username='admin', password='admin', licenseModel='VM-IXN-TIER3')
#    portLicenseObj = verifyPortLicense.Connect(platform='windows', licenseServerIp='192.168.70.127', username='hgee', password='!Flash128', licenseModel='VM-IXN-TIER3')

    #portLicenseObj = verifyPortLicense.Connect(platform='chassis', licenseServerIp='192.168.70.11', username='admin', password='admin', licenseModel='VM-IXN-TIER3')
#    portLicenseObj.areThereEnoughLicenses(2)
#    print('\n--- Available:', portLicenseObj.availablePortLicenses)

    # jsonConfigFile = '/home/hgee/Dropbox/MyIxiaWork/jsonConfigImportExport/bgpJsonOriginal.json'
    # jsonData = mainObj.jsonReadConfig(jsonConfigFile)
    # ixChassisIp = jsonData['availableHardware']['chassis'][0]['hostname']

    #status = mainObj.activateRouterIdProtocols('192.4.0.5', activate=True)

    #status = mainObj.getIndexIdByIpAddr('1.1.1.6')
    # ipv4Obj = mainObj.getIpv4ObjByPortName(portName='PE2-6/8')
    # mainObj.getIgmpHostObjByIpv4Obj(ipv4Obj)

    #mainObj.activateIgmpHostSession(portName='PE2-6/8', ipAddress='1.1.1.5', activate=True)


    # getStats() = 0:01:09.005277
    # takesnapshot() = 0:00:12.119357

    # stats = mainObj.getStats(viewName='Flow Statistics', silentMode=False)
    # for flowGroup,values in stats.items():
    #     print('\nFlow:', flowGroup)
    #     txPort = values['    for flowGroup,values in stats.items()

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    print('\nTest failed! {0}\n'.format(traceback.print_exc()))
    print(errMsg)
    if connectToApiServer == 'linux':
        mainObj.linuxServerStopAndDeleteSession()
