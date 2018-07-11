"""
 PLEASE READ DISCLAIMER

    This is a sample script for demo and reference purpose only.
    It is subject to change for content updates without warning.

 REQUIREMENTS
    - Python modules: requests
    - IxNetwork 8.41+

 DESCRIPTION
    - Configures 3 NGPF Topology Groups with ISIS protocol, enabling BIER in ISIS and Network Groups.
    - Configures 3 RAW Traffic Items with packet headers: Ethernet, MPLS, BIER, IPv4 and UDP

        - Topology 1 = TxPort
            Device Group
              - IPv4
              - ISIS
                  name='ISIS-L3 RTR 2'
                   enableBIER=True
                   bierNFlag=True
                   bierRFlag=False
                   prefixAdvertisementType='ipv4'
                   includePrefixAttrFlags=True
                   distribution='up'

        - Topology 2 = RxPort
            Device Group 
              - IPv4
              - ISIS
                  name='ISIS-L3 RTR 2'
                   enableBIER=True
                   bierNFlag=True
                   bierRFlag=False
                   prefixAdvertisementType='ipv4'
                   includePrefixAttrFlags=True
                   distribution='up'
 
            Network Group
               IPv4PrefixPool/ISIS
                   BAR= 0
                   BFRId= 12
                   BFRIdStep= 1
                   BIERBitStringLength= '64bits'
                   labelStart= 1001
                   labelRangeSize= 1
                   nFlag= True
                   pFlag= False
                   rFlag= False
                   vFlag= False
                   redistribution= 'up'
                   routeOrigin= 'internal'
                   subDomainId= 0

        - Topology 3 = RxPort
            Device Group
              - IPv4
              - ISIS
                  name='ISIS-L3 RTR 3'
                   enableBIER=True
                   bierNFlag=True
                   bierRFlag=False
                   prefixAdvertisementType='ipv4'
                   includePrefixAttrFlags=True
                   distribution='up'

            Network Group
               IPv4PrefixPool/ISIS
                   BAR= 0,
                   BFRId= 12,
                   BFRIdStep= 1,
                   BIERBitStringLength= '64bits',
                   labelStart= 1001,
                   labelRangeSize= 1,
                   nFlag= True,
                   pFlag= False,
                   rFlag= False,
                   vFlag= False,
                   redistribution= 'up',
                   routeOrigin= 'internal',
                   subDomainId= 0
 
    - Create 3 Traffic Items
        - All Traffic items are RAW traffic items and have the same configurations.
         Raw packet header configurations:

           1: Ethernet II
           2: MPLS
                startLabel=1001
           3: BIER
                Nibble=5
                Ver=0
                BSL=64 Bits
                Entropy=0
                OAM=0
                Rsv=0
                DSCP=0
                Proto=IPv4 Packet
                BFIR-Id=1
           4: IPv4
           5: UDP
                Auto

    - Start protocols
    - Verify protocol sessions
    - Apply Traffic
    - Start Traffic
    - Get stats

 USAGE
    python <script>.py windows
    python <script>.py linux
"""

import sys, traceback

sys.path.insert(0, '../Modules')
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiTraffic import Traffic
from IxNetRestApiProtocol import Protocol
from IxNetRestApiStatistics import Statistics

# Default the API server to either windows or linux.
osPlatform = 'windows'

if len(sys.argv) > 1:
    if sys.argv[1] not in ['windows', 'windowsConnectionMgr', 'linux']:
        sys.exit("\nError: %s is not a known option. Choices are 'windows' or 'linux'." % sys.argv[1])
    osPlatform = sys.argv[1]

try:
    #---------- Preference Settings --------------

    forceTakePortOwnership = True
    releasePortsWhenDone = False
    enableDebugTracing = True
    deleteSessionAfterTest = True ;# For Windows Connection Mgr and Linux API server only

    # Set configLicense to False if:
    #    - You are using a Linux based XGS chassis and the licenses are activated in the chassis.
    #    - Or the license settings are configured in the Windows IxNetwork GUI in Preferences.
    # Set configLicense to True if:
    #    - You are using IxVM chassis/ports and OVA Linux API server and the licenses are not activated in the vm chassis.
    configLicense = True
    licenseServerIp = '192.168.70.3'
    licenseModel = 'subscription'
    licenseTier = 'tier3'

    ixChassisIp = '192.168.70.120'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'], [ixChassisIp, '1', '2'], [ixChassisIp, '1', '3']]

    if osPlatform == 'linux':
        mainObj = Connect(apiServerIp='192.168.70.108',
                          serverIpPort='443',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs=osPlatform
                          )

    if osPlatform in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='192.168.70.3',
                          serverIpPort='11009',
                          serverOs=osPlatform,
                          deleteSessionAfterTest=True
                          )

    #---------- Preference Settings End --------------

    portObj = PortMgmt(mainObj)
    portObj.connectIxChassis(ixChassisIp)

    if portObj.arePortsAvailable(portList, raiseException=False) != 0:
        if forceTakePortOwnership == True:
            portObj.releasePorts(portList)
        else:
            raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')

    mainObj.newBlankConfig()

    if configLicense == True:
        portObj.releaseAllPorts()
        mainObj.configLicenseServerDetails([licenseServerIp], licenseModel, licenseTier)

    vportList = portObj.assignPorts(portList, rawTraffic=True)

    protocolObj = Protocol(mainObj)
    topologyObj1 = protocolObj.createTopologyNgpf(portList=[portList[0]], topologyName='Ixia Test Port1 (Tx)')
    topologyObj2 = protocolObj.createTopologyNgpf(portList=[portList[1]], topologyName='Ixia Test Port2 (Rx)')
    topologyObj3 = protocolObj.createTopologyNgpf(portList=[portList[2]], topologyName='Ixia Test Port3 (Rx)')

    deviceGroupObj1 = protocolObj.createDeviceGroupNgpf(topologyObj1, multiplier=1, deviceGroupName='DG1')
    deviceGroupObj2 = protocolObj.createDeviceGroupNgpf(topologyObj2, multiplier=1, deviceGroupName='BFR 11')
    deviceGroupObj3 = protocolObj.createDeviceGroupNgpf(topologyObj3, multiplier=1, deviceGroupName='BFR 21')

    ethernetObj1 = protocolObj.configEthernetNgpf(deviceGroupObj1,
                                                  ethernetName='MyEth1',
                                                  macAddress={'start': '00:01:01:00:00:01',
                                                              'direction': 'increment',
                                                              'step': '00:00:00:00:00:01'},
                                                  macAddressPortStep='disabled',
                                                  vlanId=None)

    ethernetObj2 = protocolObj.configEthernetNgpf(deviceGroupObj2,
                                                  ethernetName='MyEth2',
                                                  macAddress={'start': '00:01:02:00:00:01',
                                                              'direction': 'increment',
                                                              'step': '00:00:00:00:00:01'},
                                                  macAddressPortStep='disabled',
                                                  vlanId=None)

    ethernetObj3 = protocolObj.configEthernetNgpf(deviceGroupObj3,
                                                  ethernetName='MyEth3',
                                                  macAddress={'start': '00:01:03:00:00:01',
                                                              'direction': 'increment',
                                                              'step': '00:00:00:00:00:01'},
                                                  macAddressPortStep='disabled',
                                                  vlanId=None)

    isisObj1 = protocolObj.configIsIsL3Ngpf(ethernetObj1, name='IsIsL3-1')

    # /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/isisL3Router/1
    isisL3RouterObj1 = protocolObj.getDeviceGroupIsIsL3RouterObj(deviceGroupObj=deviceGroupObj1)
    protocolObj.configIsIsL3RouterNgpf(isisL3RouterObj1,
                                       name='ISIS-L3 RTR 1',
                                       enableBIER=True,
                                       bierNFlag=True,
                                       bierRFlag=False,
                                       prefixAdvertisementType='ipv4',
                                       includePrefixAttrFlags=True,
                                       distribution='up')

    # /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/isisL3Router/1/isisBierSubDomainList
    protocolObj.configIsIsBierSubDomainListNgpf(isisL3RouterObj1, subDomainId=0, BAR=0)

    isisObj2 = protocolObj.configIsIsL3Ngpf(ethernetObj2, name='IsIsL3-2')
    isisL3RouterObj2 = protocolObj.getDeviceGroupIsIsL3RouterObj(deviceGroupObj=deviceGroupObj2)
    protocolObj.configIsIsL3RouterNgpf(isisL3RouterObj2,
                                       name='ISIS-L3 RTR 2',
                                       enableBIER=True,
                                       bierNFlag=True,
                                       bierRFlag=False,
                                       prefixAdvertisementType='ipv4',
                                       includePrefixAttrFlags=True,
                                       distribution='up')

    # /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/2/isisL3Router/1/isisBierSubDomainList
    protocolObj.configIsIsBierSubDomainListNgpf(isisL3RouterObj2, subDomainId=0, BAR=0)

    isisObj3 = protocolObj.configIsIsL3Ngpf(ethernetObj3, name='IsIsL3-3')
    isisL3RouterObj3 = protocolObj.getDeviceGroupIsIsL3RouterObj(deviceGroupObj=deviceGroupObj3)
    protocolObj.configIsIsL3RouterNgpf(isisL3RouterObj3,
                                       name='ISIS-L3 RTR 3',
                                       enableBIER=True,
                                       bierNFlag=True,
                                       bierRFlag=False,
                                       prefixAdvertisementType='ipv4',
                                       includePrefixAttrFlags=True,
                                       distribution='up')

    # /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/3/isisL3Router/1/isisBierSubDomainList
    protocolObj.configIsIsBierSubDomainListNgpf(isisL3RouterObj3, subDomainId=0, BAR=0)

    # 5.1.1.1, 5.1.1.101
    ipv4Obj1 = protocolObj.configIpv4Ngpf(ethernetObj1,
                                          ipv4Address={'start': '1.1.1.1',
                                                       'direction': 'increment',
                                                       'step': '0.0.0.1'},
                                          ipv4AddressPortStep='disabled',
                                          gateway={'start': '1.1.1.2',
                                                   'direction': 'increment',
                                                   'step': '0.0.0.0'},
                                          gatewayPortStep='disabled',
                                          prefix=24,
                                          resolveGateway=True)

    # 5.1.1.101, 5.1.1.1
    ipv4Obj2 = protocolObj.configIpv4Ngpf(ethernetObj2,
                                          ipv4Address={'start': '1.1.1.2',
                                                       'direction': 'increment',
                                                       'step': '0.0.0.1'},
                                          ipv4AddressPortStep='disabled',
                                          gateway={'start': '1.1.1.1',
                                                   'direction': 'increment',
                                                   'step': '0.0.0.0'},
                                          gatewayPortStep='disabled',
                                          prefix=24,
                                          resolveGateway=True)

    # 6.1.1.101, 6.1.1.1
    ipv4Obj3 = protocolObj.configIpv4Ngpf(ethernetObj3,
                                          ipv4Address={'start': '1.1.1.3',
                                                       'direction': 'increment',
                                                       'step': '0.0.0.1'},
                                          ipv4AddressPortStep='disabled',
                                          gateway={'start': '1.1.1.1',
                                                   'direction': 'increment',
                                                   'step': '0.0.0.0'},
                                          gatewayPortStep='disabled',
                                          prefix=24,
                                          resolveGateway=True)


    networkGroupObj1 = protocolObj.configNetworkGroup(create=deviceGroupObj2,
                                                      name='BFR 22',
                                                      multiplier = 1,
                                                      networkAddress = {'start': '2.1.1.22',
                                                                        'step': '0.0.0.1',
                                                                        'direction': 'increment'},
                                                      prefixLength = 32)

    protocolObj.configPrefixPoolsIsisL3RouteProperty(prefixPoolsObj=networkGroupObj1,
                                                     BAR= 0,
                                                     BFRId= 12,
                                                     BFRIdStep= 1,
                                                     BIERBitStringLength= '64bits',
                                                     labelStart= 1001,
                                                     labelRangeSize= 1,
                                                     nFlag= True,
                                                     pFlag= False,
                                                     rFlag= False,
                                                     vFlag= False,
                                                     redistribution= 'up',
                                                     routeOrigin= 'internal',
                                                     subDomainId= 0
                                                 )

    networkGroupObj2 = protocolObj.configNetworkGroup(create=deviceGroupObj3,
                                                  name='BFR 12',
                                                  multiplier = 1,
                                                  networkAddress = {'start': '2.1.1.12',
                                                                    'step': '0.0.0.1',
                                                                    'direction': 'increment'},
                                                  prefixLength = 32)

    protocolObj.configPrefixPoolsIsisL3RouteProperty(prefixPoolsObj=networkGroupObj2,
                                                     BAR= 0,
                                                     BFRId= 12,
                                                     BFRIdStep= 1,
                                                     BIERBitStringLength= '64bits',
                                                     labelStart= 1001,
                                                     labelRangeSize= 1,
                                                     nFlag= True,
                                                     pFlag= False,
                                                     rFlag= False,
                                                     vFlag= False,
                                                     redistribution= 'up',
                                                     routeOrigin= 'internal',
                                                     subDomainId= 0
                                                 )

    protocolObj.startAllProtocols()
    protocolObj.verifyAllProtocolSessionsNgpf()

    # For all parameter options, go to the API configTrafficItem.
    # mode = create or modify
    # Note: Check API configTrafficItem for options.
    trafficObj = Traffic(mainObj)
    trafficStatus = trafficObj.configTrafficItem(mode='create',
                                                 trafficItem = {
                                                     'name':'Stream_BFR_11',
                                                     'trafficType':'raw',
                                                     'trafficItemType': 'l2L3',
                                                     'biDirectional':False,
                                                     'trackBy': ['trackingenabled0']
                                                 },
                                                 endpoints = [{'name':'Flow-Group-1',
                                                               'sources': [vportList[0]],
                                                               'destinations': [vportList[1]]
                                                           }],
                                                 configElements = [{'transmissionType': 'continuous',
                                                                    'frameRate': 10000,
                                                                    'frameRateType': 'framesPerSecond',
                                                                    'frameSize': 512}])

    trafficItemObj   = trafficStatus[0]
    endpointObj      = trafficStatus[1][0]
    configElementObj = trafficStatus[2][0]

    # This will show you all the available protocol header options to create
    trafficObj.showProtocolTemplates(configElementObj)
    
    # Show the configured packet headers in sequential order to get the stack ID.
    trafficObj.showTrafficItemPacketStack(configElementObj)
    # 1: Ethernet II
    # 2: MPLS
    # 3: BIER
    # 4: IPv4
    # 5: UDP

    stackObj = trafficObj.getPacketHeaderStackIdObj(configElementObj, stackId=1)
    # Show a list of field names in order to know which field to configure the mac addresses.
    trafficObj.showPacketHeaderFieldNames(stackObj)
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Destination MAC Address',
                                       data={'valueType': 'increment',
                                             'startValue': '00:0c:29:84:37:16',
                                             'stepValue': '00:00:00:00:00:01',
                                             'countValue': 1})

    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Source MAC Address',
                                       data={'valueType': 'increment',
                                             'startValue': '00:0c:29:aa:86:e0',
                                             'stepValue': '00:00:00:00:00:01',
                                             'countValue': 1})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='MPLS', stackNumber=1,
                                                    action='append')
    # Just an example to show a list of field names in order to know which field to configure the IP addresses.
    #trafficObj.showPacketHeaderFieldNames(stackObj)
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Label Value',
                                       data={'valueType': 'increment',
                                             'startValue': '1001',
                                             'stepValue': '1',
                                             'countValue': 1,
                                             'auto': False})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='BIER', stackNumber=2,
                                                    action='append')
    # 5
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Nibble',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '5',
                                             'startValue': '5',
                                             'stepValue': '5',
                                             'countValue': 1,
                                             'auto': False})
    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Ver',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})

    # 64 Bits
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='BSL',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '1',
                                             'startValue': '3',
                                             'stepValue': '3',
                                             'countValue': 1,
                                             'auto': False})
    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Entropy',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})

    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='OAM',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})

    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Rsv',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})

    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='DSCP',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})
       
    # IPv4 Packet
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Proto',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '4',
                                             'startValue': '2',
                                             'stepValue': '2',
                                             'countValue': 1,
                                             'auto': False})
    
    # 1
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='BFIR-Id',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '1',
                                             'startValue': '1',
                                             'stepValue': '1',
                                             'countValue': 1,
                                             'auto': False})
    
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='IPv4', stackNumber=3,
                                                    action='append')
    #stackObj = getPacketHeaderStackIdObj(configElementObjList[0], stackId=6)
    # Show a list of field names in order to know which field to configure the IP addresses.
    trafficObj.showPacketHeaderFieldNames(stackObj)

    # src = 45.1.1.1
    trafficObj.configPacketHeaderField(stackObj,
                                    fieldName='Source Address',
                                       data={'valueType': 'increment',
                                             'startValue': '45.1.1.1',
                                             'stepValue': '0.0.0.1',
                                             'countValue': 1})
    
    # dst = 230.1.1.1
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Destination Address',
                                       data={'valueType': 'increment',
                                             'startValue': '230.1.1.1',
                                             'stepValue': '0.0.0.1',
                                             'countValue': 1})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='UDP', stackNumber=4,
                                                    action='append')
    #stackObj = getPacketHeaderStackIdObj(configElementObjList[0], stackId=7)
    # Show a list of field names in order to know which field to configure the UDP src/dst ports.
    trafficObj.showPacketHeaderFieldNames(stackObj)
    # 1: UDP-Source-Port
    # 2: UDP-Dest-Port
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='UDP-Source-Port',
                                       data={'auto': True})
    
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='UDP-Dest-Port',
                                       data={'auto': True})
    
    trafficObj.showTrafficItemPacketStack(configElementObj)


    # 2nd Traffic Item
    trafficObj = Traffic(mainObj)
    trafficStatus = trafficObj.configTrafficItem(mode='create',
                                                 trafficItem = {
                                                     'name':'Stream_BFR_11_12',
                                                     'trafficType':'raw',
                                                     'trafficItemType': 'l2L3',
                                                     'biDirectional':False,
                                                     'trackBy': ['trackingenabled0']
                                                 },
                                                 endpoints = [{'name':'Flow-Group-1',
                                                               'sources': [vportList[0]],
                                                               'destinations': [vportList[1]]
                                                           }],
                                                 configElements = [{'transmissionType': 'continuous',
                                                                    'frameRate': 10000,
                                                                    'frameRateType': 'framesPerSecond',
                                                                    'frameSize': 512}])

    trafficItemObj   = trafficStatus[0]
    endpointObj      = trafficStatus[1][0]
    configElementObj = trafficStatus[2][0]

    # This will show you all the available protocol header options to create
    #trafficObj.showProtocolTemplates(configElementObj)
    
    # Show the configured packet headers in sequential order to get the stack ID.
    trafficObj.showTrafficItemPacketStack(configElementObj)
    # 1: Ethernet II
    # 2: MPLS
    # 3: BIER
    # 4: IPv4
    # 5: UDP

    stackObj = trafficObj.getPacketHeaderStackIdObj(configElementObj, stackId=1)
    # Show a list of field names in order to know which field to configure the mac addresses.
    trafficObj.showPacketHeaderFieldNames(stackObj)
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Destination MAC Address',
                                       data={'valueType': 'increment',
                                             'startValue': '00:0c:29:84:37:16',
                                             'stepValue': '00:00:00:00:00:01',
                                             'countValue': 1})

    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Source MAC Address',
                                       data={'valueType': 'increment',
                                             'startValue': '00:0c:29:aa:86:e0',
                                             'stepValue': '00:00:00:00:00:01',
                                             'countValue': 1})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='MPLS', stackNumber=1,
                                                    action='append')
    # Just an example to show a list of field names in order to know which field to configure the IP addresses.
    trafficObj.showPacketHeaderFieldNames(stackObj)
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Label Value',
                                       data={'valueType': 'increment',
                                             'startValue': '1001',
                                             'stepValue': '1',
                                             'countValue': 1,
                                             'auto': False})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='BIER', stackNumber=2,
                                                    action='append')
    # 5
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Nibble',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '5',
                                             'startValue': '5',
                                             'stepValue': '5',
                                             'countValue': 1,
                                             'auto': False})
    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Ver',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})

    # 64 Bits
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='BSL',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '1',
                                             'startValue': '3',
                                             'stepValue': '3',
                                             'countValue': 1,
                                             'auto': False})
    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Entropy',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})

    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='OAM',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})

    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Rsv',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})

    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='DSCP',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})
       
    # IPv4 Packet
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Proto',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '4',
                                             'startValue': '2',
                                             'stepValue': '2',
                                             'countValue': 1,
                                             'auto': False})
    
    # 1
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='BFIR-Id',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '1',
                                             'startValue': '1',
                                             'stepValue': '1',
                                             'countValue': 1,
                                             'auto': False})
    
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='IPv4', stackNumber=3,
                                                    action='append')
    #stackObj = getPacketHeaderStackIdObj(configElementObjList[0], stackId=6)
    # Show a list of field names in order to know which field to configure the IP addresses.
    trafficObj.showPacketHeaderFieldNames(stackObj)

    # src = 45.1.1.1
    trafficObj.configPacketHeaderField(stackObj,
                                    fieldName='Source Address',
                                       data={'valueType': 'increment',
                                             'startValue': '45.1.1.1',
                                             'stepValue': '0.0.0.1',
                                             'countValue': 1})
    
    # dst = 230.1.1.1
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Destination Address',
                                       data={'valueType': 'increment',
                                             'startValue': '230.1.1.1',
                                             'stepValue': '0.0.0.1',
                                             'countValue': 1})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='UDP', stackNumber=4,
                                                    action='append')
    #stackObj = getPacketHeaderStackIdObj(configElementObjList[0], stackId=7)
    # Show a list of field names in order to know which field to configure the UDP src/dst ports.
    trafficObj.showPacketHeaderFieldNames(stackObj)
    # 1: UDP-Source-Port
    # 2: UDP-Dest-Port
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='UDP-Source-Port',
                                       data={'auto': True})
    
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='UDP-Dest-Port',
                                       data={'auto': True})
    
    trafficObj.showTrafficItemPacketStack(configElementObj)


    # 3rd Traffic Item
    trafficObj = Traffic(mainObj)
    trafficStatus = trafficObj.configTrafficItem(mode='create',
                                                 trafficItem = {
                                                     'name':'Stream_BFR_12_21',
                                                     'trafficType':'raw',
                                                     'trafficItemType': 'l2L3',
                                                     'biDirectional':False,
                                                     'trackBy': ['trackingenabled0']
                                                 },
                                                 endpoints = [{'name':'Flow-Group-1',
                                                               'sources': [vportList[0]],
                                                               'destinations': [vportList[1]]
                                                           }],
                                                 configElements = [{'transmissionType': 'continuous',
                                                                    'frameRate': 10000,
                                                                    'frameRateType': 'framesPerSecond',
                                                                    'frameSize': 512}])

    trafficItemObj   = trafficStatus[0]
    endpointObj      = trafficStatus[1][0]
    configElementObj = trafficStatus[2][0]

    # This will show you all the available protocol header options to create
    #trafficObj.showProtocolTemplates(configElementObj)
    
    # Show the configured packet headers in sequential order to get the stack ID.
    trafficObj.showTrafficItemPacketStack(configElementObj)
    # 1: Ethernet II
    # 2: MPLS
    # 3: BIER
    # 4: IPv4
    # 5: UDP

    stackObj = trafficObj.getPacketHeaderStackIdObj(configElementObj, stackId=1)
    # Show a list of field names in order to know which field to configure the mac addresses.
    trafficObj.showPacketHeaderFieldNames(stackObj)
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Destination MAC Address',
                                       data={'valueType': 'increment',
                                             'startValue': '00:0c:29:84:37:16',
                                             'stepValue': '00:00:00:00:00:01',
                                             'countValue': 1})

    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Source MAC Address',
                                       data={'valueType': 'increment',
                                             'startValue': '00:0c:29:aa:86:e0',
                                             'stepValue': '00:00:00:00:00:01',
                                             'countValue': 1})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='MPLS', stackNumber=1,
                                                    action='append')
    # Just an example to show a list of field names in order to know which field to configure the IP addresses.
    trafficObj.showPacketHeaderFieldNames(stackObj)
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Label Value',
                                       data={'valueType': 'increment',
                                             'startValue': '1001',
                                             'stepValue': '1',
                                             'countValue': 1,
                                             'auto': False})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='BIER', stackNumber=2,
                                                    action='append')
    # 5
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Nibble',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '5',
                                             'startValue': '5',
                                             'stepValue': '5',
                                             'countValue': 1,
                                             'auto': False})
    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Ver',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})

    # 64 Bits
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='BSL',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '1',
                                             'startValue': '3',
                                             'stepValue': '3',
                                             'countValue': 1,
                                             'auto': False})
    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Entropy',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})

    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='OAM',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})

    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Rsv',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})

    # 0
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='DSCP',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '0',
                                             'startValue': '0',
                                             'stepValue': '0',
                                             'countValue': 1,
                                             'auto': False})
       
    # IPv4 Packet
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Proto',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '4',
                                             'startValue': '2',
                                             'stepValue': '2',
                                             'countValue': 1,
                                             'auto': False})
    
    # 1
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='BFIR-Id',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '1',
                                             'startValue': '1',
                                             'stepValue': '1',
                                             'countValue': 1,
                                             'auto': False})
    
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='IPv4', stackNumber=3,
                                                    action='append')
    #stackObj = getPacketHeaderStackIdObj(configElementObjList[0], stackId=6)
    # Show a list of field names in order to know which field to configure the IP addresses.
    trafficObj.showPacketHeaderFieldNames(stackObj)

    # src = 45.1.1.1
    trafficObj.configPacketHeaderField(stackObj,
                                    fieldName='Source Address',
                                       data={'valueType': 'increment',
                                             'startValue': '45.1.1.1',
                                             'stepValue': '0.0.0.1',
                                             'countValue': 1})
    
    # dst = 230.1.1.1
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Destination Address',
                                       data={'valueType': 'increment',
                                             'startValue': '230.1.1.1',
                                             'stepValue': '0.0.0.1',
                                             'countValue': 1})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='UDP', stackNumber=4,
                                                    action='append')
    #stackObj = getPacketHeaderStackIdObj(configElementObjList[0], stackId=7)
    # Show a list of field names in order to know which field to configure the UDP src/dst ports.
    trafficObj.showPacketHeaderFieldNames(stackObj)
    # 1: UDP-Source-Port
    # 2: UDP-Dest-Port
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='UDP-Source-Port',
                                       data={'auto': True})
    
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='UDP-Dest-Port',
                                       data={'auto': True})
    
    trafficObj.showTrafficItemPacketStack(configElementObj)


    trafficObj.startTraffic(regenerateTraffic=True, applyTraffic=True)

    # Check the traffic state before getting stats.
    #    Use one of the below APIs based on what you expect the traffic state should be before calling stats.
    #    'stopped': If you expect traffic to be stopped such as for fixedFrameCount and fixedDuration.
    #    'started': If you expect traffic to be started such as in continuous mode.
    #trafficObj.checkTrafficState(expectedState=['stopped'], timeout=45)
    trafficObj.checkTrafficState(expectedState=['started'], timeout=45)

    statObj = Statistics(mainObj)
    stats = statObj.getStats(viewName='Traffic Item Statistics')

    '''
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
    '''

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
