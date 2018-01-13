import re, time
from IxNetRestApi import IxNetRestApiException

class Traffic(object):
    def __init__(self, ixnObj):
        self.ixnObj = ixnObj

    def configTrafficItem(self, mode=None, obj=None, trafficItem=None, endpoints=None, configElements=None):
        """
        Description
            Create or modify a Traffic Item.

            When creating a new Traffic Item, this API will return 3 object handles:
                 trafficItemObj, endpointSetObjList and configElementObjList

            NOTE:
                Each Traffic Item could create multiple endpoints and for each endpoint,
                you could provide a list of configElements for each endpoint.
                The endpoints and configElements must be in a list.

                - Each endpointSet allows you to configure the highLevelStream, which overrides configElements.
                - If you set bi-directional to True, then there will be two highLevelStreams that you could configure.
                - Including highLevelStream is optional.  Set highLevelStream to None to use configElements.

        Parameters
            mode: craete|modify

            obj: For mode=modify only.  Select the object to modify: trafficItemObj|configElementObj|endpointObj

            trafficItem: Traffic Item kwargs.

            endpoints: [list]: A list of two items: [ ( {endpoints}, {highLevelStreams: [(),()]} ), (add more endpoints)... ]
                               Scroll down to see example.

            configElements: [list]: Config Element kwargs.
                                    Each item in this list is aligned to the sequential order of your endpoint list.

        If mode is create:
            The required parameters are: mode, trafficItem, endpoints and configElements

        If mode is modify:
            The required parameters are: mode, obj, and one of the objects to modify (trafficIemObj, endpointObj or configElementObj).
            
            You need to provide the right object handle.

               To modify trafficItem:
                  Ex: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/<id>

               To modify endpointSet:
                  Ex: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/endpointSet/<id>

               To modify configElements = configElement object handlex
                  Ex: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/configElement/<id>

               Look at sample script l2l3RestNgpy.py

        Traffic Item Parameters
            trafficType options:
               raw, ipv4, ipv4, ethernetVlan, frameRelay, atm, fcoe, fc, hdlc, ppp

            srcDestMesh:
               Defaults to one-to-one
               Options: manyToMany or fullMesh

            routeMesh:
               fullMesh or oneToOne

            allowSelfDestined: True or False

        ConfigElement Parameters
            transmissionType:
               - continuous, fixedFrameCount
               - custom (for burstPacketCount)
            frameCount: (For continuous and fixedFrameCount traffic)
            burstPacketCount: (For bursty traffic)

            frameRate: The rate to transmit packets
            frameRateType: percentLineRate or framesPerSecond
            trackBy: put in a list:

        For bursty packet count,
              transmissionType = 'custom',
              burstPacketCount = 50000,

        Endpoints Parameters
            A list of topology, deviceGroup or protocol objects
                sources: Object in a list.
                destinations: Object in a lsit.

            Example:
               ['/api/v1/sessions/1/ixnetwork/topology/8']
               or a list ['.../topology/1', '.../topology/3']
               ['.../topology/1/deviceGroup/1', '.../topology/2/deviceGroup/1/ethernet/1/ipv4/1']


        USAGE EXAMPLE:
            To create new Traffic Item:

            configTrafficItem(mode='create',
                              trafficItem = {
                                  'name':'Topo1 to Topo2',
                                  'trafficType':'ipv4',
                                  'biDirectional':True,
                                  'srcDestMesh':'one-to-one',
                                  'routeMesh':'oneToOne',
                                  'allowSelfDestined':False,
                                  'trackBy': ['flowGroup0', 'vlanVlanId0']},
                               endpoints = [({'name':'Flow-Group-1',
                                              'sources': [topologyObj1],
                                              'destinations': [topologyObj2]},
                                             {'highLevelStreamElements': None})],
                               configElements = [{'transmissionType': 'fixedFrameCount',
                                                  'frameCount': 50000,
                                                  'frameRate': 88,
                                                  'frameRateType': 'percentLineRate',
                                                  'frameSize': 128}])

            To create a new Traffic Item and configure the highLevelStream:

            trafficObj.configTrafficItem(mode='create',
                                         trafficItem = {'name':'Topo3 to Topo4',
                                                       'trafficType':'ipv4',
                                                       'biDirectional':True,
                                                       'srcDestMesh':'one-to-one',
                                                       'routeMesh':'oneToOne',
                                                       'allowSelfDestined':False,
                                                       'trackBy': ['flowGroup0', 'vlanVlanId0']},
                                         endpoints = [({'name':'Flow-Group-1',
                                                        'sources': [topologyObj1],
                                                        'destinations': [topologyObj2]},
                                                       {'highLevelStreamElements': [
                                                           ({
                                                               'transmissionType': 'fixedFrameCount',
                                                               'frameCount': 10000,
                                                               'frameRate': 18,
                                                               'frameRateType': 'percentLineRate',
                                                               'frameSize': 128}), 
                                                           ({
                                                               'transmissionType': 'fixedFrameCount',
                                                               'frameCount': 20000,
                                                               'frameRate': 28,
                                                               'frameRateType': 'percentLineRate',
                                                               'frameSize': 228})
                                                       ]
                                                    })],
                                         configElements = None)
    

        Return: trafficItemObj, endpointSetObjList, configElementObjList
        """
        if mode == 'create':
            trafficItemUrl = self.ixnObj.sessionUrl+'/traffic/trafficItem'
        if mode == 'modify' and obj is None:
            raise IxNetRestApiException('Modifying Traffic Item requires a Traffic Item object')
        if mode == 'create' and trafficItem is None:
            raise IxNetRestApiException('Creating Traffic Item requires trafficItem kwargs')
        if mode == None:
            raise IxNetRestApiException('configTrafficItem Error: Must include mode: config or modify')

        # Create a new Traffic Item
        if mode == 'create' and trafficItem != None:
            if 'trackBy' in trafficItem:
                trackBy = trafficItem['trackBy']
                del trafficItem['trackBy']

            self.ixnObj.logInfo('\nconfigTrafficItem: %s : %s' % (trafficItemUrl, trafficItem))
            response = self.ixnObj.post(trafficItemUrl, data=trafficItem)
            trafficItemObj = response.json()['links'][0]['href']

        if mode == 'modify' and trafficItem != None:
            trafficItemObj = obj
            if 'trackBy' in trafficItem:
                trackBy = trafficItem['trackBy']
                del trafficItem['trackBy']
            self.ixnObj.patch(self.ixnObj.httpHeader+trafficItemObj, data=trafficItem)

        # Create Endpoints
        if mode == 'create' and endpoints != None:
            if type(endpoints) != list:
                raise IxNetRestApiException('configTrafficItem error: Provide endpoints in a list')

            endpointSetObjList = []
            if 'trafficItemObj' not in locals():
                # Expect the user to pass in the endpoint object handle correctly and parse
                # out the traffic item object handle.
                trafficItemObj = self.ixnObj.sessionUrl.split('/endpointSet')[0]

            for endPoint in endpoints:
                eachEndPoint = endPoint[0]
                highLevelStream = endPoint[1]['highLevelStreamElements']
                response = self.ixnObj.post(self.ixnObj.httpHeader+trafficItemObj+'/endpointSet', data=eachEndPoint)

                # Get the RETURNED endpointSet/# object
                endpointSetObj = response.json()['links'][0]['href']
                response = self.ixnObj.get(self.ixnObj.httpHeader+endpointSetObj)

                # This endpontSet ID is used for getting the corresponding Config Element ID
                # in case there are multiple endpoint sets created.
                endpointSetId = response.json()['id']
                endpointSetObjList.append(endpointSetObj)

                # An endpoint flow group could have two highLevelStream if bi-directional is enabled.x
                if highLevelStream != None:
                    streamNum = 1
                    for eachHighLevelStream in highLevelStream:
                        self.configHighLevelStream(self.ixnObj.httpHeader+trafficItemObj+'/highLevelStream/'+str(streamNum), eachHighLevelStream)
                        streamNum += 1

        if mode == 'modify' and endpoints != None:
            endpointSetObj = obj
            self.ixnObj.patch(self.ixnObj.httpHeader+endpointSetObj, data=endpoints)

        if configElements is not None:
            if mode == 'create' and type(configElements) != list:
                raise IxNetRestApiException('configTrafficItem error: Provide configElements in a list')

            if mode == 'modify':
                configElementObj = obj
                self.configConfigElements(self.ixnObj.httpHeader+configElementObj, configElements)

            if mode == 'create':
                endpointResponse = self.ixnObj.get(self.ixnObj.httpHeader+trafficItemObj+'/endpointSet')

                index = 0
                configElementCounter = 1
                configElementObjList = []
                for eachEndpoint in endpointResponse.json():
                    configElementObj = trafficItemObj+'/configElement/'+str(configElementCounter)
                    configElementObjList.append(configElementObj)
                    self.configConfigElements(self.ixnObj.httpHeader+configElementObj, configElements[index])
                    if len(endpointSetObjList) == len(configElements):
                        index += 1
                    configElementCounter += 1

        if configElements is None:
            configElementObjList = []

        # Cannot configure tracking until endpoints are created. This is why
        # tracking config is at the end here.
        if mode in ['create', 'modify'] and 'trackBy' in locals():
            self.ixnObj.patch(self.ixnObj.httpHeader+trafficItemObj+'/tracking', data={'trackBy': trackBy})

        if mode == 'create' and trafficItem != None:
            return [trafficItemObj, endpointSetObjList, configElementObjList]

    def configConfigElements(self, configElementObj, configElements):
        if 'transmissionType' in configElements:
            self.ixnObj.patch(configElementObj+'/transmissionControl', data={'type': configElements['transmissionType']})

        if 'burstPacketCount' in configElements:
            self.ixnObj.patch(configElementObj+'/transmissionControl', data={'burstPacketCount': int(configElements['burstPacketCount'])})

        if 'frameCount' in configElements:
            self.ixnObj.patch(configElementObj+'/transmissionControl', data={'frameCount': int(configElements['frameCount'])})

        if 'duration' in configElements:
            self.ixnObj.patch(configElementObj+'/transmissionControl', data={'duration': int(configElements['duration'])})

        if 'frameRate' in configElements:
            self.ixnObj.patch(configElementObj+'/frameRate', data={'rate': int(configElements['frameRate'])})

        if 'frameRateType' in configElements:
            self.ixnObj.patch(configElementObj+'/frameRate', data={'type': configElements['frameRateType']})

        if 'frameSize' in configElements:
            self.ixnObj.patch(configElementObj+'/frameSize', data={'fixedSize': int(configElements['frameSize'])})

    def configHighLevelStream(self, highLevelStreamObj, flowGroupElements):
        if 'transmissionType' in flowGroupElements:
            self.ixnObj.patch(highLevelStreamObj+'/transmissionControl', data={'type': flowGroupElements['transmissionType']})

        if 'burstPacketCount' in flowGroupElements:
            self.ixnObj.patch(highLevelStreamObj+'/transmissionControl', data={'burstPacketCount': int(flowGroupElements['burstPacketCount'])})

        if 'frameCount' in flowGroupElements:
            self.ixnObj.patch(highLevelStreamObj+'/transmissionControl', data={'frameCount': int(flowGroupElements['frameCount'])})

        if 'duration' in flowGroupElements:
            self.ixnObj.patch(highLevelStreamObj+'/transmissionControl', data={'duration': int(flowGroupElements['duration'])})

        if 'frameRate' in flowGroupElements:
            self.ixnObj.patch(highLevelStreamObj+'/frameRate', data={'rate': int(flowGroupElements['frameRate'])})

        if 'frameRateType' in flowGroupElements:
            self.ixnObj.patch(highLevelStreamObj+'/frameRate', data={'type': flowGroupElements['frameRateType']})

        if 'frameSize' in flowGroupElements:
            self.ixnObj.patch(highLevelStreamObj+'/frameSize', data={'fixedSize': int(flowGroupElements['frameSize'])})

    def getTransmissionType(self, configElement):
        # configElement: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/configElement/1
        # Returns: fixedFrameCount, continuous

        response = self.ixnObj.get(self.ixnObj.httpHeader+configElement+'/transmissionControl')
        return response.json()['type']

    def configTrafficLatency(self, enabled=True, mode='storeForward'):
        # enabled = True|False
        # mode    = storeForward|cutThrough|forwardDelay|mef
        self.ixnObj.patch(self.ixnObj.sessionUrl+'/traffic/statistics/latency', data={'enabled':enabled, 'mode':mode})

    def showProtocolTemplates(self, configElementObj):
        """
        Description
           To show all the protocol template options. Mainly used for adding a protocol header
           to Traffic Item packets.

        Parameters
           configElementObj: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/{id}/configElement/{id}
        """
        # Get a list of all the protocol templates:
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/traffic/protocolTemplate?skip=0&take=end')
        for eachProtocol in response.json()['data']:
            self.ixnObj.logInfo('%s: %s' % (eachProtocol['id'], eachProtocol['displayName']))

    def showTrafficItemPacketStack(self, configElementObj):
        """
        Description
           Display a list of the current packet stack in a Traffic Item

           1: Ethernet II
           2: VLAN
           3: IPv4
           4: UDP
           5: Frame Check Sequence CRC-32

        Parameters
           configElementObj: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/{id}/configElement/{id}
       """
        print()
        response = self.ixnObj.get(self.ixnObj.httpHeader+configElementObj+'/stack')
        for (index, eachHeader) in enumerate(response.json()):
            self.ixnObj.logInfo('%s: %s' % (str(index+1), eachHeader['displayName']))

    def addTrafficItemPacketStack(self, configElementObj, protocolStackNameToAdd, stackNumber, action='append'):
        """
        Description
           To either append or insert a protocol stack to an existing packet.

           You must know the exact name of the protocolTemplate to add by calling
           showProtocolTemplates() API and get the exact name  as a value for the parameter protocolStackNameToAdd.

           You must also know where to add the new packet header stack.  Use showTrafficItemPacketStack() to see
           your current stack numbers.

           This API returns the protocol stack object handle so you could use it to config its settings.

         Parameters
           configElementObj: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/{id}/configElement/{id}

           action:
               append: To add after the specified stackNumber
               insert: To add before the specified stackNumber

           protocolStackNameToAdd: The name of the protocol stack to add.  To get a list of options,
                                   use API showProtocolTemplates().
                                   Some common ones: MPLS, IPv4, TCP, UDP, VLAN, IGMPv1, IGMPv2, DHCP, VXLAN

           stackNumber: The stack number to append or insert into.
                        Use showTrafficItemPacketStack() to view the packet header stack in order to know
                        which stack number to insert your new stack before or after the stack number.

        Example:
            addTrafficItemPacketStack(configElement, protocolStackNameToAdd='UDP',
                                      stackNumber=3, action='append', apiKey=apiKey, verifySslCert=False

        Returns:
            /api/v1/sessions/1/ixnetwork/traffic/trafficItem/{id}/configElement/{id}/stack/{id}
        """
        if action == 'append':
            action = 'appendprotocol'
        if action == 'insert':
            action = 'insertprotocol'

        # /api/v1/sessions/1
        match = re.match('http.*(/api.*sessions/[0-9]).*', self.ixnObj.sessionUrl)
        if match:
            apiHeader = match.group(1)

        # /api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/configElement/1
        arg1 = configElementObj+'/stack/' + str(stackNumber)

        # Display a list of the current packet stack
        response = self.ixnObj.get(self.ixnObj.httpHeader+configElementObj+'/stack')
        for (index, eachHeader) in enumerate(response.json()):
            self.ixnObj.logInfo('{0}: {1}'.format(index+1, eachHeader['displayName']))

        # Get a list of all the protocol templates:
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/traffic/protocolTemplate?skip=0&take=end')

        protocolTemplateId = None
        for eachProtocol in response.json()['data']:
            if bool(re.match('^%s$' % protocolStackNameToAdd, eachProtocol['displayName'].strip(), re.I)):
                # /api/v1/sessions/1/traffic/protocolTemplate/30
                protocolTemplateId =  eachProtocol['links'][0]['href']

        if protocolTemplateId == None:
            raise IxNetRestApiException('No such protocolTemplate name found: {0}'.format(protocolStackNameToAdd))
        self.ixnObj.logInfo('\nprotocolTemplateId: %s' % protocolTemplateId)
        data = {'arg1': arg1, 'arg2': protocolTemplateId}
        response = self.ixnObj.post(self.ixnObj.httpHeader+configElementObj+'/stack/operations/%s' % action, data=data)

        if self.ixnObj.waitForComplete(response, self.ixnObj.httpHeader+configElementObj+'/stack/operations/appendprotocol/'+response.json()['id']) == 1:
            raise IxNetRestApiException

        # /api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/configElement/1/stack/4
        self.ixnObj.logInfo('\naddTrafficItemPacketStack: Returning: %s' % response.json()['result'])
        return response.json()['result']

    def showTrafficItemStackLinks(self, configElementObj):
        # Return a list of configured Traffic Item packet header in sequential order.
        #   1: Ethernet II
        #   2: MPLS
        #   3: MPLS
        #   4: MPLS
        #   5: MPLS
        #   6: IPv4
        #   7: UDP
        #   8: Frame Check Sequence CRC-32

        stackList = []
        response = self.ixnObj.get(self.ixnObj.httpHeader+configElementObj+'/stackLink')
        self.ixnObj.logInfo('\n')
        for eachStackLink in response.json():
            if eachStackLink['linkedTo'] != 'null':
                self.ixnObj.logInfo(eachStackLink['linkedTo'])
                stackList.append(eachStackLink['linkedTo'])
        return stackList

    def getPacketHeaderStackIdObj(self, configElementObj, stackId):
        """
        Desciption
           This API should be called after calling showTrafficItemPacketStack(configElementObj) in
           order to know the stack ID number to use.  Such as ...
            Stack1: Ethernet II
            Stack2: MPLS
            Stack3: MPLS
            Stack4: MPLS
            Stack5: MPLS
            Stack6: IPv4
            Stack7: UDP
            Stack8: Frame Check Sequence CRC-32

        Parameters
           configElementObj: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/{id}/configElement/{id}
           stackId: In this example, IPv4 stack ID is 6.

         Return stack ID object: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/{id}/configElement/{id}/stack/{id}
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader+configElementObj+'/stack')
        for (index, eachHeader) in enumerate(response.json()):
            self.ixnObj.logInfo('{0}: {1}'.format(index+1, eachHeader['displayName']))
            if stackId == index+1:
                self.ixnObj.logInfo('\tReturning: %s' % self.ixnObj.httpHeader+eachHeader['links'][0]['href'])
                return eachHeader['links'][0]['href']

    def modifyTrafficItemDestMacAddress(self, trafficItemName, destMacAddress):
        trafficItemObj = self.getTrafficItemObjByName(trafficItemName)
        response = self.ixnObj.get(self.ixnObj.httpHeader+trafficItemObj)
        if response.json()['trafficType'] != 'raw':
            raise IxNetRestApiException('Traffic Item is not Raw type. Cannot modify Traffic Item: %s' % trafficItemName)

        configElementObj = trafficItemObj+'/configElement/1'
        stackObj = self.getPacketHeaderStackIdObj(configElementObj, stackId=1)
        self.configPacketHeaderField(stackObj,
                                     fieldName='Destination MAC Address',
                                     data={'valueType': 'increment',
                                           'startValue': destMacAddress,
                                           'stepValue': '00:00:00:00:00:00',
                                           'countValue': 1,
                                           'auto': False})
        
    def showPacketHeaderFieldNames(self, stackObj):
        """
        Description
           Get all the packet header field names.

        Parameters
           stackObj = /api/v1/sessions/1/ixnetwork/traffic/trafficItem/{id}/configElement/{id}/stack/{id}

        Example for Ethernet stack field names
           1: Destination MAC Address
           2: Source MAC Address
           3: Ethernet-Type
           4: PFC Queue
        """
        self.ixnObj.logInfo('\ngetPacketHeaderFieldNames: %s' % stackObj+'/field')
        response = self.ixnObj.get(self.ixnObj.httpHeader+stackObj+'/field')
        for eachField in  response.json():
            id = eachField['id']
            fieldName = eachField['displayName']
            self.ixnObj.logInfo('\t{0}: {1}'.format(id, fieldName))

    def convertTrafficItemToRaw(self, trafficItemName):
        """
        Description

        Parameter
        """
        trafficItemObj = self.getTrafficItemObjByName(trafficItemName)
        if trafficItemObj == 0:
            raise IxNetRestApiException('\nNo such Traffic Item name: %s' % trafficItemName)
        self.ixnObj.post(self.ixnObj.sessionUrl+'/traffic/trafficItem/operations/converttoraw', data={'arg1': trafficItemObj})

    def configPacketHeaderField(self, stackIdObj, fieldName, data):
        """
        Desciption
            Configure raw packets in a Traffic Item.
            In order to know the field names to modify, use getPacketHeaderFieldNames() to display the names:

        stackIdObj: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/{id}/configElement/{id}/stack/{id}
        fieldName: The name of the field name in the packet header stack to modify.
                   You could use getPacketHeaderFieldNames(stackObj) API to dispaly your options
        data: Example:
             data={'valueType': 'valueList', 'valueList': ['1001', '1002'], auto': False}
             data={'valueType': 'increment', 'startValue': '1.1.1.1', 'stepValue': '0.0.0.1', 'countValue': 2}
             data={'valueType': 'increment', 'startValue': '00:01:01:01:00:01', 'stepValue': '00:00:00:00:00:01'}
             data={'valueType': 'increment', 'startValue': 1001, 'stepValue': 1, 'countValue': 2, 'auto': False}
        """
        fieldId = None
        # Get the field ID object by the user defined fieldName
        response = self.ixnObj.get(self.ixnObj.httpHeader+stackIdObj+'/field')
        for eachFieldId in response.json():
            if bool(re.match(fieldName, eachFieldId['displayName'], re.I)):
                fieldId = eachFieldId['id']

        if fieldId == None:
            raise IxNetRestApiException('Failed to located your provided fieldName:', fieldName)

        self.ixnObj.logInfo('\nconfigPacketHeaderFieldId:  fieldIdObj: %s' % stackIdObj+'/field/'+str(fieldId))
        response = self.ixnObj.patch(self.ixnObj.httpHeader+stackIdObj+'/field/'+str(fieldId), data=data)

    def configEgressCustomTracking(self, trafficItemObj, offsetBits, widthBits):
        """
        Description
           Configuring custom egress tracking. User must know the offset and the bits width to track.
           In most use cases, packets ingressing the DUT gets modified by the DUT and to track the
           correctness of the DUT's packet modification, use this API to verify the receiving port's packet
           offset and bit width.
        """
        # Safety check: Apply traffic or else configuring egress tracking won't work.
        self.applyTraffic()
        self.ixnObj.patch(self.ixnObj.httpHeader+trafficItemObj+'/tracking/egress',
                   data={'encapsulation': 'Any: Use Custom Settings',
                         'customOffsetBits': offsetBits,
                         'customWidthBits': widthBits
                     })
        self.ixnObj.patch(self.ixnObj.httpHeader+trafficItemObj, data={'egressEnabled': True})
        self.regenerateTrafficItems()
        self.applyTraffic()

    def createEgressStatView(self, trafficItemObj, egressTrackingPort, offsetBit, bitWidth,
                             egressStatViewName='EgressStatView', ingressTrackingFilterName=None):
        """
        Description
           Create egress statistic view for egress stats.

        """
        egressTrackingOffsetFilter = 'Custom: ({0}bits at offset {1})'.format(int(bitWidth), int(offsetBit))
        trafficItemName = self.getTrafficItemName(trafficItemObj)

        # Get EgressStats
        # Create Egress Stats
        self.ixnObj.logInfo('\nCreating new statview for egress stats...')
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/statistics/view',
                             data={'caption': egressStatViewName,
                                   'treeViewNodeName': 'Egress Custom Views',
                                   'type': 'layer23TrafficFlow',
                                   'visible': True})

        egressStatView = response.json()['links'][0]['href']
        self.ixnObj.logInfo('\negressStatView Object: %s' % egressStatView)
        # /api/v1/sessions/1/ixnetwork/statistics/view/12

        self.ixnObj.logInfo('\nCreating layer23TrafficFlowFilter')
        # Dynamically get the PortFilterId
        response = self.ixnObj.get(self.ixnObj.httpHeader+egressStatView+'/availablePortFilter')
        portFilterId = []
        for eachPortFilterId in response.json():
            #192.168.70.10/Card2/Port1
            self.ixnObj.logInfo('\tAvailable PortFilterId: %s' % eachPortFilterId['name'])
            if eachPortFilterId['name'] == egressTrackingPort:
                self.ixnObj.logInfo('\tLocated egressTrackingPort: %s' % egressTrackingPort)
                portFilterId.append(eachPortFilterId['links'][0]['href'])
                break
        if portFilterId == []:
            raise IxNetRestApiException('No port filter ID found')
        self.ixnObj.logInfo('\nPortFilterId: %s' % portFilterId)

        # Dynamically get the Traffic Item Filter ID
        response = self.ixnObj.get(self.ixnObj.httpHeader+egressStatView+'/availableTrafficItemFilter')
        availableTrafficItemFilterId = []
        for eachTrafficItemFilterId in response.json():
            if eachTrafficItemFilterId['name'] == trafficItemName:
                availableTrafficItemFilterId.append(eachTrafficItemFilterId['links'][0]['href'])
                break
        if availableTrafficItemFilterId == []:
            raise IxNetRestApiException('No traffic item filter ID found.')

        self.ixnObj.logInfo('\navailableTrafficItemFilterId: %s' % availableTrafficItemFilterId)
        # /api/v1/sessions/1/ixnetwork/statistics/view/12
        self.ixnObj.logInfo('\negressStatView: %s' % egressStatView)
        layer23TrafficFlowFilter = self.ixnObj.httpHeader+egressStatView+'/layer23TrafficFlowFilter'
        self.ixnObj.logInfo('\nlayer23TrafficFlowFilter: %s' % layer23TrafficFlowFilter)
        response = self.ixnObj.patch(layer23TrafficFlowFilter,
                              data={'egressLatencyBinDisplayOption': 'showEgressRows',
                                    'trafficItemFilterId': availableTrafficItemFilterId[0],
                                    'portFilterIds': portFilterId,
                                    'trafficItemFilterIds': availableTrafficItemFilterId})

        # Get the egress tracking filter
        egressTrackingFilter = None
        ingressTrackingFilter = None
        response = self.ixnObj.get(self.ixnObj.httpHeader+egressStatView+'/availableTrackingFilter')
        self.ixnObj.logInfo('\nAvailable tracking filters for both ingress and egress...')
        for eachTrackingFilter in response.json():
            self.ixnObj.logInfo('\tFilter Name: {0}: {1}'.format(eachTrackingFilter['id'], eachTrackingFilter['name']))
            if bool(re.match('Custom: *\([0-9]+ bits at offset [0-9]+\)', eachTrackingFilter['name'])):
                egressTrackingFilter = eachTrackingFilter['links'][0]['href']

            if ingressTrackingFilterName is not None:
                if eachTrackingFilter['name'] == ingressTrackingFilterName:
                    ingressTrackingFilter = eachTrackingFilter['links'][0]['href']

        if egressTrackingFilter is None:
            raise IxNetRestApiException('Failed to locate your defined custom offsets: {0}'.format(egressTrackingOffsetFilter))

        # /api/v1/sessions/1/ixnetwork/statistics/view/23/availableTrackingFilter/3
        self.ixnObj.logInfo('\nLocated egressTrackingFilter: %s' % egressTrackingFilter)
        enumerationFilter = layer23TrafficFlowFilter+'/enumerationFilter'
        response = self.ixnObj.post(enumerationFilter,
                             data={'sortDirection': 'ascending',
                                   'trackingFilterId': egressTrackingFilter})

        if ingressTrackingFilterName is not None:
            self.ixnObj.logInfo('\nLocated ingressTrackingFilter: %s' % egressTrackingFilter)
            response = self.ixnObj.post(enumerationFilter,
                                 data={'sortDirection': 'ascending',
                                       'trackingFilterId': ingressTrackingFilter})

        # Must enable one or more egress statistic counters in order to enable the
        # egress tracking stat view object next.
        #   Enabling: ::ixNet::OBJ-/statistics/view:"EgressStats"/statistic:"Tx Frames"
        #   Enabling: ::ixNet::OBJ-/statistics/view:"EgressStats"/statistic:"Rx Frames"
        #   Enabling: ::ixNet::OBJ-/statistics/view:"EgressStats"/statistic:"Frames Delta"
        #   Enabling: ::ixNet::OBJ-/statistics/view:"EgressStats"/statistic:"Loss %"
        response = self.ixnObj.get(self.ixnObj.httpHeader+egressStatView+'/statistic')
        for eachEgressStatCounter in response.json():
            eachStatCounterObject = eachEgressStatCounter['links'][0]['href']
            eachStatCounterName = eachEgressStatCounter['caption']
            self.ixnObj.logInfo('\tEnabling egress stat counter: %s' % eachStatCounterName)
            self.ixnObj.patch(self.ixnObj.httpHeader+eachStatCounterObject, data={'enabled': True})

        self.ixnObj.patch(self.ixnObj.httpHeader+egressStatView, data={'enabled': True})
        self.ixnObj.logInfo('\ncreateEgressCustomStatView: Done')

        return egressStatView

    def enableTrafficItem(self, trafficItemNumber):
        url = self.ixnObj.sessionUrl+'/traffic/trafficItem/%s' % str(trafficItemNumber)
        response = self.ixnObj.patch(url, data={"enabled": "true"})

    def disableTrafficItem(self, trafficItemNumber):
        url = self.ixnObj.sessionUrl+'/traffic/trafficItem/%s' % str(trafficItemNumber)
        response = self.ixnObj.patch(url, data={"enabled": "false"})

    def isTrafficItemNameExists(self, trafficItemName):
        """
        Description
           Verify if the Traffic Item name exists in the configuration.

        Parameter
           trafficItemName: The Traffic Item name to verify
        """
        trafficItemNameExists = False
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/traffic/trafficItem')
        for eachTrafficItem in response.json():
            if eachTrafficItem['name'] == trafficItemName:
                return True
        return False

    def enablePacketLossDuration(self):
        self.ixnObj.patch(self.ixnObj.sessionUrl+'/traffic/statistics/packetLossDuration', data={'enabled': 'true'})

    def disablePacketLossDuration(self):
        self.ixnObj.patch(self.ixnObj.sessionUrl+'/traffic/statistics/packetLossDuration', data={'enabled': 'false'})

    def checkTrafficState(self, expectedState=['stopped'], timeout=45):
        """
        Description
            Check the traffic state for the expected state.
            This is best used to verify that traffic has started before calling getting stats.

        Traffic states are:
            startedWaitingForStats, startedWaitingForStreams, started, stopped,
            stoppedWaitingForStats, txStopWatchExpected, locked, unapplied

        Parameters
            expectedState = Input a list of expected traffic state.
                            Example: ['started', startedWaitingForStats'] <-- This will wait until stats has arrived.

            timeout = The amount of seconds you want to wait for the expected traffic state.
                      Defaults to 45 seconds.
                      In a situation where you have more than 10 pages of stats, you will
                      need to increase the timeout time.
        """
        if type(expectedState) != list:
            expectedState.split(' ')

        self.ixnObj.logInfo('\nExpecting traffic state: {0}\n'.format(expectedState))
        for counter in range(1,timeout+1):
            response = self.ixnObj.get(self.ixnObj.sessionUrl+'/traffic', silentMode=True)
            currentTrafficState = response.json()['state']
            self.ixnObj.logInfo('checkTrafficState: {trafficState}: Waited {counter}/{timeout} seconds'.format(
                trafficState=currentTrafficState,
                counter=counter,
                timeout=timeout))
            if counter < timeout and currentTrafficState not in expectedState:
                time.sleep(1)
                continue
            if counter < timeout and currentTrafficState in expectedState:
                time.sleep(8)
                self.ixnObj.logInfo('\ncheckTrafficState: Done\n')
                return 0

        raise IxNetRestApiException('checkTrafficState: Traffic state did not reach the expected state(s):', expectedState)

    def getRawTrafficItemSrcIp(self, trafficItemName):
        """
        Description
            Get the Raw Traffic Item source IP address. Mainly to look up each Device Group
            IPv4 that has the source IP address to get the gateway IP address.

        Parameter
            trafficItemName: The Raw Traffic Item name
        """
        trafficItemObj = self.getTrafficItemObjByName(trafficItemName)
        queryData = {
                    "from": trafficItemObj+"/configElement/1",
                    "nodes": [{"node": "stack", "properties": ["*"], "where": [{"property": "stackTypeId", "regex": "ipv4"}]},
                              {"node": "field", "properties": ["*"], "where": [{"property": "fieldTypeId", "regex": "ipv4.header.srcIp"}]}]
                    }
        queryResponse = self.ixnObj.query(data=queryData)
        sourceIp = queryResponse.json()['result'][0]['stack'][1]['field'][26]['fieldValue']
        return sourceIp

    def getTrafficItemType(self, trafficItemName):
        """
        Description
            Get the Traffic Item traffic type by the Traffic Item name.

        Parameter
            trafficItemName: The Traffic Item name

        Return
            The traffic type
        """
        queryData = {'from': '/traffic',
                    'nodes': [{'node': 'trafficItem', 'properties': ['name', 'trafficType'], 'where': [{'property': 'name', 'regex': trafficItemName}]},
                    ]}
        queryResponse = self.ixnObj.query(data=queryData)
        if queryResponse.json()['result'][0]['trafficItem'] == []:
            raise IxNetRestApiException('getTrafficItemType: No such Traffic Item Name found: %s' % trafficItemName)
        return (queryResponse.json()['result'][0]['trafficItem'][0]['trafficType'])

    def enableTrafficItemByName(self, trafficItemName, enable=True):
        """
        Description
            Enable or Disable a Traffic Item by its name.

        Parameter
            trafficItemName: The exact spelling of the Traffic Item name.
            enable: True | False
                    True: Enable Traffic Item
                    False: Disable Traffic Item
        """
        trafficItemObj = self.getTrafficItemObjByName(trafficItemName)
        if trafficItemObj == 0:
            raise IxNetRestApiException('No such Traffic Item name: %s' % trafficItemName)
        self.ixnObj.patch(self.ixnObj.httpHeader+trafficItemObj, data={"enabled": enable})

    def getTrafficItemName(self, trafficItemObj):
        """
        Description
            Get the Traffic Item name by its object.

        Parameter
            trafficItemObj: The Traffic Item object.
                            /api/v1/sessions/1/ixnetwork/traffic/trafficItem/1
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader+trafficItemObj)
        return response.json()['name']

    def getAllTrafficItemNames(self):
        """
        Description
            Return all of the Traffic Item names.
        """
        trafficItemUrl = self.ixnObj.sessionUrl+'/traffic/trafficItem'
        response = self.ixnObj.get(trafficItemUrl)
        trafficItemNameList = []
        for eachTrafficItemId in response.json():
            trafficItemNameList.append(eachTrafficItemId['name'])
        return trafficItemNameList

    def getTrafficItemObjByName(self, trafficItemName):
        """
        Description
            Get the Traffic Item object by the Traffic Item name.

        Parameter
            trafficItemName: Name of the Traffic Item.

        Return
            0: No Traffic Item name found. Return 0.
            traffic item object:  /api/v1/sessions/1/ixnetwork/traffic/trafficItem/2
        """
        queryData = {'from': '/traffic',
                    'nodes': [{'node': 'trafficItem', 'properties': ['name'], 'where': [{"property": "name", "regex": trafficItemName}]}
                    ]}
        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
        try:
            return queryResponse.json()['result'][0]['trafficItem'][0]['href']
        except:
            return 0

    def applyTraffic(self):
        """
        Description
            Apply the configured traffic.
        """
        restApiHeader = '/api'+self.ixnObj.sessionUrl.split('/api')[1]
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/traffic/operations/apply', data={'arg1': restApiHeader+'/traffic'})
        if self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/traffic/operations/apply/'+response.json()['id']) == 1:
            raise IxNetRestApiException

    def regenerateTrafficItems(self, trafficItemList='all'):
        """
        Description
            Performs regenerate on Traffic Items.

        Parameter
            trafficItemList: 'all' will automatically regenerate from all Traffic Items.
                             Or provide a list of Traffic Items.
                             ['/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1', ...]
        """
        if trafficItemList == 'all':
            response = self.ixnObj.get(self.ixnObj.sessionUrl + "/traffic/trafficItem")
            trafficItemList = ["%s" % (str(i["links"][0]["href"])) for i in response.json()]
        else:
            if type(trafficItemList) != list:
                trafficItemList = trafficItemList.split(' ')

        url = self.ixnObj.sessionUrl+"/traffic/trafficItem/operations/generate"
        data = {"arg1": trafficItemList}
        self.ixnObj.logInfo('\nRegenerating traffic items: %s' % trafficItemList)
        response = self.ixnObj.post(url, data=data)
        if self.ixnObj.waitForComplete(response, url+'/'+response.json()['id']) == 1:
            raise IxNetRestApiException

    def startTraffic(self, blocking=False):
        """
        Description
            Start traffic and verify traffic is started.

        Parameter
            blocking: True|False: Blocking doesn't return until the server has
                      started traffic and ready for stats.  Unblocking is the opposite.

        Syntax
            POST: http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/traffic/operations/start
                  data={arg1: http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/traffic}
        """
        self.applyTraffic()
        self.ixnObj.logInfo('\nstartTraffic: %s' % self.ixnObj.sessionUrl+'/traffic/operations/start')

        if blocking == False:
            self.ixnObj.post(self.ixnObj.sessionUrl+'/traffic/operations/start', data={'arg1': self.ixnObj.sessionUrl+'/traffic'})
            self.checkTrafficState(expectedState=['started', 'startedWaitingForStats'], timeout=45)

        if blocking == True:
            queryData = {"from": "/traffic",
                "nodes": [{"node": "trafficItem", "properties": ["enabled"], "where": [{"property": "enabled", "regex": "true"}]}]}
            queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
            enabledTrafficItemHrefList = [trafficItem['href'] for trafficItem in queryResponse.json()['result'][0]['trafficItem']]
            self.ixnObj.post(self.ixnObj.sessionUrl+'/traffic/operations/startstatelesstrafficblocking', data={'arg1': enabledTrafficItemHrefList})
            # Wait a few seconds before calling getStats() or else viewObj is not created.
            time.sleep(5)
        self.ixnObj.logInfo('startTraffic: Successfully started')

    def stopTraffic(self):
        """
        Description
            Stop traffic and verify traffic has stopped.

        Syntax
            POST: http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/traffic/operations/stop
                  data={arg1: http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/traffic}
        """
        self.ixnObj.logInfo('\nstopTraffic: %s' % self.ixnObj.sessionUrl+'/traffic/operations/stop')
        self.ixnObj.post(self.ixnObj.sessionUrl+'/traffic/operations/stop', data={'arg1': self.ixnObj.sessionUrl+'/traffic'})
        self.checkTrafficState(expectedState=['stopped', 'stoppedWaitingForStats'])
        time.sleep(3)

    def showTrafficItems(self):
        """
        Description
            Show All Traffic Item details.
        """
        queryData = {'from': '/traffic',
                    'nodes': [{'node': 'trafficItem',    'properties': ['name', 'enabled', 'state', 'biDirectional', 'trafficType', 'warning', 'errors'], 'where': []},
                                {'node': 'endpointSet',   'properties': ['name', 'sources', 'destinations'], 'where': []},
                                {'node': 'configElement', 'properties': ['name', 'endpointSetId', ], 'where': []},
                                {'node': 'frameSize',     'properties': ['type', 'fixedSize'], 'where': []},
                                {'node': 'framePayload',     'properties': ['type', 'customRepeat'], 'where': []},
                                {'node': 'frameRate',     'properties': ['type', 'rate'], 'where': []},
                                {'node': 'frameRateDistribution', 'properties': ['streamDistribution', 'portDistribution'], 'where': []},
                                {'node': 'transmissionControl', 'properties': ['type', 'frameCount', 'burstPacketCount'], 'where': []},
                                {'node': 'tracking',      'properties': ['trackBy'], 'where': []},
                            ]
                    }

        queryResponse = self.ixnObj.query(data=queryData)
        self.ixnObj.logInfo('\n', end='')
        for ti in queryResponse.json()['result'][0]['trafficItem']:
            self.ixnObj.logInfo('TrafficItem: {0}\n\tName: {1}  Enabled: {2}  State: {3}'.format(ti['id'], ti['name'], ti['enabled'], ti['state']))
            self.ixnObj.logInfo('\tTrafficType: {0}  BiDirectional: {1}'.format(ti['trafficType'], ti['biDirectional']))
            for tracking in ti['tracking']:
                self.ixnObj.logInfo('\tTrackings: {0}'.format(tracking['trackBy']))

            for endpointSet, cElement in zip(ti['endpointSet'], ti['configElement']):
                self.ixnObj.logInfo('\n\tEndpointSetId: {0}  EndpointSetName: {1}'.format(endpointSet['id'], endpointSet['name']))
                srcList = []
                for src in endpointSet['sources']:
                    srcList.append(src.split('/ixnetwork')[1])
                dstList = []
                for dest in endpointSet['destinations']:
                    dstList.append(dest.split('/ixnetwork')[1])
                self.ixnObj.logInfo('\t    Sources: {0}'.format(srcList))
                self.ixnObj.logInfo('\t    Destinations: {0}'.format(dstList))
                self.ixnObj.logInfo('\t    FrameType: {0}  FrameSize: {1}'.format(cElement['frameSize']['type'], cElement['frameSize']['fixedSize']))
                self.ixnObj.logInfo('\t    TranmissionType: {0}  FrameCount: {1}  BurstPacketCount: {2}'.format(cElement['transmissionControl']['type'],
                                                                                                cElement['transmissionControl']['frameCount'],
                                                                                                cElement['transmissionControl']['burstPacketCount']))
                self.ixnObj.logInfo('\t    FrameRateType: {0}  FrameRate: {1}'.format(cElement['frameRate']['type'], cElement['frameRate']['rate']))
            self.ixnObj.logInfo('\n', end='')

    def setFrameSize(self, trafficItemName, frameSize):
        """
        Description
            Modify the frame size.

            param: trafficItemName: The name of the Traffic Item.
            param: frameSize: (int): The frame size to set.
        """
        queryData = {'from': '/traffic',
                    'nodes': [{'node': 'trafficItem', 'properties': ['name'], 'where': [{'property': 'name', 'regex': trafficItemName}]},
                              {'node': 'configElement', 'properties': [], 'where': []}]}
        queryResponse = self.ixnObj.query(data=queryData)
        if queryResponse.json()['result'][0]['trafficItem'] == []:
            raise IxNetRestApiException('\nNo such Traffic Item name found: %s' % trafficItemName)
        configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
        self.configTrafficItem(mode='modify', obj=configElementObj, configElements={'frameSize': frameSize})

    def configFramePayload(self, configElementObj, payloadType='custom', customRepeat=True, customPattern=None):
        """
        Description
            Configure the frame payload.

        Parameters
            payloadType: Options:
                           custom, decrementByte, decrementWord, incrementByte, incrementWord, random
            customRepeat: True|False
            customPattern: Enter a custom payload pattern
        """
        data = {'type': payloadType, 'customRepeat': customRepeat, 'customPattern': customPattern}
        self.ixnObj.patch(self.ixnObj.httpHeader+configElementObj+'/framePayload', data=data)






