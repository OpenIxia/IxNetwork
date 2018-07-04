import re, time
from IxNetRestApi import IxNetRestApiException

class Traffic(object):
    def __init__(self, ixnObj=None):
        self.ixnObj = ixnObj

    def setMainObject(self, mainObject):
        # For Python Robot Framework support
        self.ixnObj = mainObject
        
    def configTrafficItem(self, mode=None, obj=None, trafficItem=None, endpoints=None, configElements=None):
        """
        Description
            Create or modify a Traffic Item.

            When creating a new Traffic Item, this API will return 3 object handles:
                 trafficItemObj, endpointSetObjList and configElementObjList

            NOTE:
                Each Traffic Item could create multiple endpoints and for each endpoint.
                you could provide a list of configElements for each endpoint.
                The endpoints and configElements must be in a list.

                - Each endpointSet allows you to configure the highLevelStream, which overrides configElements.
                - If you set bi-directional to True, then there will be two highLevelStreams that you could configure.
                - Including highLevelStream is optional.  Set highLevelStream to None to use configElements.

        Parameters
            mode: craete|modify

            obj: For "mode=modify" only. Provide the object to modify: trafficItemObj|configElementObj|endpointObj

            trafficItem: Traffic Item kwargs.

            endpoints: [list]: A list: [{name: sources:[], destionations:[], highLevelStreams: None, (add more endpoints)... ]
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

            trackBy: [list]: trackingenabled0, ethernetIiSourceaddress0, ethernetIiDestinationaddress0, ethernetIiPfcQueue0,
                             vlanVlanId0, vlanVlanUserPriority0, ipv4SourceIp0, sourceDestValuePair0, sourceDestEndpointPair0,
                             ipv4Precedence0, ipv4SourceIp0, flowGroup0, frameSize0 

        ConfigElement Parameters
            transmissionType:
               - continuous|fixedFrameCount
               - custom (for burstPacketCount)
            frameCount: (For continuous and fixedFrameCount traffic)
            burstPacketCount: (For bursty traffic)
            frameSize: The packet size.
            frameRate: The rate to transmit packets
            frameRateType: bitsPerSecond|framesPerSecond|interPacketGap|percentLineRate
            portDistribution: applyRateToAll|splitRateEvenly.  Default=applyRateToAll
            streamDistribution: splitRateEvenly|applyRateToAll. Default=splitRateEvently
            trackBy: <list>: Some options: flowGroup0, vlanVlanId0, ethernetIiDestinationaddress0, ethernetIiSourceaddress0,
                             sourcePort0, sourceDestPortPair0, ipv4DestIp0, ipv4SourceIp0, ipv4Precedence0,
                             ethernetIiPfcQueue0, frameSize0

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
            To modify:
                trafficObj.configTrafficItem(mode='modify',
                                             obj='/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/configElement/1', 
                                             configElements={'transmissionType': 'continuous'})

                trafficObj.configTrafficItem(mode='modify',
                                             obj='/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1',
                                             trafficItem={'trackBy': ['frameSize0', 'ipv4SourceIp0']})

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

                               endpoints = [{'name':'Flow-Group-1',
                                             'sources': [topologyObj1],
                                             'destinations': [topologyObj2],
                                             'highLevelStreamElements': None}],

                               configElements = [{'transmissionType': 'fixedFrameCount',
                                                  'frameCount': 50000,
                                                  'frameRate': 88,
                                                  'frameRateType': 'percentLineRate',
                                                  'frameSize': 128,
                                                  'portDistribution': 'applyRateToAll',
                                                  'streamDistribution': 'splitRateEvenly'
                                                  }]
            )

            To create a new Traffic Item and configure the highLevelStream:

            trafficObj.configTrafficItem(mode='create',
                                         trafficItem = {'name':'Topo3 to Topo4',
                                                       'trafficType':'ipv4',
                                                       'biDirectional':True,
                                                       'srcDestMesh':'one-to-one',
                                                       'routeMesh':'oneToOne',
                                                       'allowSelfDestined':False,
                                                       'trackBy': ['flowGroup0', 'vlanVlanId0']},
                                         endpoints = [{'name':'Flow-Group-1',
                                                        'sources': [topologyObj1],
                                                        'destinations': [topologyObj2],
                                                        'highLevelStreamElements': [
                                                           {
                                                               'transmissionType': 'fixedFrameCount',
                                                               'frameCount': 10000,
                                                               'frameRate': 18,
                                                               'frameRateType': 'percentLineRate',
                                                               'frameSize': 128}, 
                                                           {
                                                               'transmissionType': 'fixedFrameCount',
                                                               'frameCount': 20000,
                                                               'frameRate': 28,
                                                               'frameRateType': 'percentLineRate',
                                                               'frameSize': 228}
                                                         ]
                                                     }],
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

        # Don't configure config elements if user is configuring highLevelStreams
        isHighLevelStreamTrue = False

        # Create a new Traffic Item
        if mode == 'create' and trafficItem != None:
            if 'trackBy' in trafficItem:
                trackBy = trafficItem['trackBy']
                del trafficItem['trackBy']

            self.ixnObj.logInfo('configTrafficItem: %s : %s' % (trafficItemUrl, trafficItem), timestamp=False)
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

            # endpoints = [{'name':'Flow-Group-1', 'sources': [topologyObj1], 'destinations': [topologyObj2], 'highLevelStreamElements': None}]
            for endPoint in endpoints:
                endpointSrcDst = {}
                # {'name':'Flow-Group-1', 'sources': [topologyObj1], 'destinations': [topologyObj2]}
                #eachEndPoint = endPoint[0]
                if 'name' in endPoint:
                    endpointSrcDst['name'] = endPoint['name']
                endpointSrcDst['sources'] = endPoint['sources']
                endpointSrcDst['destinations'] = endPoint['destinations']
                self.ixnObj.logInfo('Config Traffic Item Endpoints', timestamp=False)
                response = self.ixnObj.post(self.ixnObj.httpHeader+trafficItemObj+'/endpointSet', data=endpointSrcDst)

                if 'highLevelStreamElements' in endPoint:
                    highLevelStream = endPoint['highLevelStreamElements']
                    # JSON doesn't support None.  In case user passed in {} instead of None.
                    if highLevelStream == {}:
                        highLevelStream = None
                else:
                    highLevelStream = None

                # Get the RETURNED endpointSet/# object
                endpointSetObj = response.json()['links'][0]['href']
                response = self.ixnObj.get(self.ixnObj.httpHeader+endpointSetObj)

                # This endpontSet ID is used for getting the corresponding Config Element ID
                # in case there are multiple endpoint sets created.
                endpointSetId = response.json()['id']
                endpointSetObjList.append(endpointSetObj)

                # An endpoint flow group could have two highLevelStream if bi-directional is enabled.x
                if highLevelStream != None:
                    isHighLevelStreamTrue = True
                    configElementObjList = None ;# Don't configure config elements if user is configuring highLevelStreams
                    streamNum = 1
                    for eachHighLevelStream in highLevelStream:
                        self.configConfigElements(self.ixnObj.httpHeader+trafficItemObj+'/highLevelStream/'+str(streamNum), eachHighLevelStream)
                        streamNum += 1

        if mode == 'modify' and endpoints != None:
            endpointSrcDst = {}
            if 'name' in endpoints:
                endpointSrcDst['name'] = endpoints['name']
            if 'sources' in endpoints:
                endpointSrcDst['sources'] = endpoints['sources']
            if 'destinations' in endpoints:
                endpointSrcDst['destinations'] = endpoints['destinations']

            endpointSetObj = obj
            self.ixnObj.patch(self.ixnObj.httpHeader+endpointSetObj, data=endpointSrcDst)

        if isHighLevelStreamTrue == False and configElements != None:
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
            self.ixnObj.logInfo('Config Traffic Item statistic trackings', timestamp=False)
            self.ixnObj.patch(self.ixnObj.httpHeader+trafficItemObj+'/tracking', data={'trackBy': trackBy})

        # API server needs some time to complete processing the highlevel stream configuration before entering regenerate.
        if mode == 'create' and trafficItem != None:
            return [trafficItemObj, endpointSetObjList, configElementObjList]

    def configConfigElements(self, configElementObj, configElements):
        """
        Description
           Configure Traffic Item Config Elements. This function will collect all the ReST API's attributes
           and execute a PATCH in one single command instead of sending a a PATCH for each attribute.
           This avoids dependency breakage because some APIs require the type to be configured first.

           This function also handles high level stream configurations since the attributes are the same. 
           Pass in the highLevelStream obj for the parameter configElementObj

        Parameters
           configElementObj: <str:obj>: The config element object:
                             Ex: /api/v1/sessions/{1}/ixnetwork/traffic/trafficItem/{1}/configElement/{1}
                             highLevelStream obj Ex: /api/v1/sessions/{1}/ixnetwork/traffic/trafficItem/{1}/highLevelStream/{1}
        
           configElements: <dict>: This could also be highLevelStream elements.  
                           configElements = {'transmissionType': 'fixedFrameCount',
                                              'frameCount': 50000,
                                              'frameRate': 88,
                                              'frameRateType': 'percentLineRate',
                                              'frameSize': 128,
                                              'portDistribution': 'applyRateToAll',
                                              'streamDistribution': 'splitRateEvenly'
                                            }
           transmissionType:   fixedFrameCount|continuous
           frameRateType:      percentLineRate|framesPerSecond
           portDistribution:   applyRateToAll|splitRateEvenly. Default=applyRateToAll
           streamDistribution: splitRateEvenly|applyRateToAll. Default=splitRateEvently
        """
        transmissionControlData = {}
        for item in ['transmissionType', 'bursePacketCount', 'frameCount', 'duration']:
            if item in configElements.keys() :
                # These attributes are int type
                if item in ['bursePacketCount', 'frameCount', 'duration']: 
                    transmissionControlData.update({item: int(configElements[item])})

                if item == 'transmissionType':
                    transmissionControlData.update({'type': str(configElements[item])})

        if transmissionControlData != {}:
            self.ixnObj.patch(configElementObj+'/transmissionControl', data=transmissionControlData)

        frameRateData = {}
        for item in ['frameRateType', 'frameRate']:
            if item in configElements.keys() :
                if item == 'frameRateType': 
                    frameRateData.update({'type': str(configElements[item])})

                if item == 'frameRate': 
                    frameRateData.update({'rate': float(configElements[item])})

        if frameRateData != {}:
            self.ixnObj.patch(configElementObj+'/frameRate', data=frameRateData)

        if 'frameSize' in configElements:
            self.ixnObj.patch(configElementObj+'/frameSize', data={'fixedSize': int(configElements['frameSize'])})

        frameRateDistribution = {}
        for item in ['portDistribution', 'streamDistribution']:
            if item in configElements.keys() :
                if item == 'portDistribution': 
                    frameRateDistribution.update({'portDistribution': configElements[item]})

                if item == 'streamDistribution': 
                    frameRateDistribution.update({'streamDistribution': configElements[item]})

        if frameRateDistribution != {}:
            self.ixnObj.patch(configElementObj+'/frameRateDistribution', data=frameRateDistribution)
        

    def getConfigElementObj(self, trafficItemObj=None, trafficItemName=None, endpointSetName=None):
        """
        Description
           Get the config element object handle.

           Use case #1: trafficItemName + endpointSetName
           Use case #2: trafficItemObj + endpointSetName

           Use case #3: trafficItemName only (Will assume there is only one configElement object which will be returned)
           Use case #4: trafficItemObj only  (Will assume there is only one configElement object which will be returned)

        Parameters
             
           trafficItemObj: <str obj>: The Traffic Item object.
           trafficItemName: <str>: The Traffic Item name.
           endpointSetName: <str>: The Traffic Item's EndpointSet name.

           How this works:
               - Users could create multiple EndpointSets within a Traffic Item.
               - Each EndpointSet has a unique object ID by default.
               - For each EndpointSet is created, a config element object is also created.
               - Each config element object handle is associated with an EndpointSet ID.
               - To be able to get the right config element object handle, we need to query
                 for the EndpointSet that you need for modifying.
               - Another terminology for EndpointSet is FlowGroup.
               - If you have multiple EndpointSets, you should give each EndpointSet a name
                 to make querying possible.
               - Otherwise, this function will assume there is only one EndpointSet created which will be returned.

        Usage examples:
           trafficObj.getConfigElementObj(trafficItemName='Raw MPLS/UDP', endpointSetName='EndpointSet-2')

           trafficObj.getConfigElementObj(trafficItemName='Raw MPLS/UDP', endpointSetName=None)

           trafficObj.getConfigElementObj(trafficItemObj='/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1', 
                                          trafficItemName=None, endpointSetName=None)

           trafficObj.getConfigElementObj(trafficItemObj='/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1', 
                                          trafficItemName=None, endpointSetName='EndpointSet-2')

        Return
           configElement: /api/v1/sessions/{id}/ixnetwork/traffic/trafficItem/{id}/configElement/{id}
        """
        if trafficItemObj:
            trafficItemName = self.getTrafficItemName(trafficItemObj)

        if trafficItemName:
            if endpointSetName:
                queryData = {'from': '/traffic',
                             'nodes': [{'node': 'trafficItem', 'properties': ['name'],
                                        'where': [{'property': 'name', 'regex': trafficItemName}]},
                                       {'node': 'endpointSet', 'properties': ['name'],
                                        'where': [{'property': 'name', 'regex': endpointSetName}]},
                      ]}

            if endpointSetName == None:
                queryData = {'from': '/traffic',
                             'nodes': [{'node': 'trafficItem', 'properties': ['name'],
                                        'where': [{'property': 'name', 'regex': trafficItemName}]},
                                       {'node': 'endpointSet', 'properties': [],
                                        'where': []},
                      ]}

            queryResponse = self.ixnObj.query(data=queryData)

            trafficItemList = queryResponse.json()['result'][0]['trafficItem']
            if trafficItemList == []:
                raise IxNetRestApiException('\nError: No traffic item name found: {0}'.format(trafficItemName))

            endpointSetList = queryResponse.json()['result'][0]['trafficItem'][0]['endpointSet']
            if endpointSetList == []:
                raise IxNetRestApiException('\nError: No endpointSet name: {0} found in Traffic Item name: {1}'.format(
                    endpointSetName, trafficItemName))

            endpointSetObj = queryResponse.json()['result'][0]['trafficItem'][0]['endpointSet'][0]['href']
            endpointSetId = endpointSetObj.split('/')[-1]

            # With the traffic item name and endpointSetId, get the Traffic Item's config element object handle.
            queryData = {'from': '/traffic',
                         'nodes': [{'node': 'trafficItem', 'properties': ['name'],
                                    'where': [{'property': 'name', 'regex': trafficItemName}]},
                                   {'node': 'configElement', 'properties': ['endpointSetId'],
                                    'where': [{'property': 'endpointSetId', 'regex': endpointSetId}]}
                  ]}

            queryResponse = self.ixnObj.query(data=queryData)
            configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
            print(configElementObj)
            return configElementObj

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
            self.ixnObj.logInfo('%s: %s' % (eachProtocol['id'], eachProtocol['displayName']), timestamp=False)

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
        self.ixnObj.logInfo('\n', timestamp=False)
        for (index, eachHeader) in enumerate(response.json()):
            self.ixnObj.logInfo('%s: %s' % (str(index+1), eachHeader['displayName']), timestamp=False)

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
            self.ixnObj.logInfo('{0}: {1}'.format(index+1, eachHeader['displayName']), timestamp=False)

        # Get a list of all the protocol templates:
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/traffic/protocolTemplate?skip=0&take=end')

        protocolTemplateId = None
        for eachProtocol in response.json()['data']:
            if bool(re.match('^%s$' % protocolStackNameToAdd, eachProtocol['displayName'].strip(), re.I)):
                # /api/v1/sessions/1/traffic/protocolTemplate/30
                protocolTemplateId =  eachProtocol['links'][0]['href']

        if protocolTemplateId == None:
            raise IxNetRestApiException('No such protocolTemplate name found: {0}'.format(protocolStackNameToAdd))
        self.ixnObj.logInfo('protocolTemplateId: %s' % protocolTemplateId, timestamp=False)
        data = {'arg1': arg1, 'arg2': protocolTemplateId}
        response = self.ixnObj.post(self.ixnObj.httpHeader+configElementObj+'/stack/operations/%s' % action, data=data)

        self.ixnObj.waitForComplete(response, self.ixnObj.httpHeader+configElementObj+'/stack/operations/appendprotocol/'+response.json()['id'])

        # /api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/configElement/1/stack/4
        self.ixnObj.logInfo('addTrafficItemPacketStack: Returning: %s' % response.json()['result'], timestamp=False)
        return response.json()['result']

    def getTrafficItemPktHeaderStackObj(self, configElementObj=None, trafficItemName=None, packetHeaderName=None):
        """
        Description
           Get the Traffic Item packet header stack object.
           You could either pass in a configElement object or the Traffic Item name.
           
        Parameters
           configElementObj: <str>: Optional: The configElement object.
                             Example: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/configElement/1

           trafficItemName: <str>: Optional: The Traffic Item name.

           packetHeaderName: <str>: Mandatory: The packet header name.
                             Example: ethernet, mpls, ipv4, ...

        Return
           The stack object
        """
        #if configElementObj != None:
        #    response = self.ixnObj.get(self.ixnObj.httpHeader+configElementObj+'/stack')

        if configElementObj == None:
            # Expect user to pass in the Traffic Item name if user did not pass in a configElement object.
            queryData = {'from': '/traffic',
                         'nodes': [{'node': 'trafficItem', 'properties': ['name'],
                                    'where': [{'property': 'name', 'regex': trafficItemName}]}]}

            queryResponse = self.ixnObj.query(data=queryData)

            if queryResponse.json()['result'][0]['trafficItem'] == []:
                raise IxNetRestApiException('\nNo such Traffic Item name found: %s' % trafficItemName)
                
            trafficItemObj = queryResponse.json()['result'][0]['trafficItem'][0]['href']
            configElementObj = trafficItemObj+'/configElement/1'
        
        response = self.ixnObj.get(self.ixnObj.httpHeader+configElementObj+'/stack')

        print('\n--- packetHeaderName:', packetHeaderName)

        for eachStack in response.json():
            self.ixnObj.logInfo('\nstack: {0}: {1}'.format(eachStack, eachStack['stackTypeId']), timestamp=False)
            if bool(re.match(packetHeaderName, eachStack['stackTypeId'], re.I)):
                stackObj = eachStack['links'][0]['href']
                break
        else:
            raise IxNetRestApiException('\nError: No such stack name found: %s' % stackName)

        return stackObj

    def showTrafficItemStackLink(self, configElementObj):
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
        self.ixnObj.logInfo('\n', timestamp=False)
        for eachStackLink in response.json():
            if eachStackLink['linkedTo'] != 'null':
                self.ixnObj.logInfo(eachStackLink['linkedTo'], timestamp=False)
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
        self.ixnObj.logInfo('\n', timestamp=False)
        for (index, eachHeader) in enumerate(response.json()):
            self.ixnObj.logInfo('{0}: {1}'.format(index+1, eachHeader['displayName']), timestamp=False)
            if stackId == index+1:
                self.ixnObj.logInfo('\tReturning: %s' % self.ixnObj.httpHeader+eachHeader['links'][0]['href'], timestamp=False)
                return eachHeader['links'][0]['href']

    def modifyTrafficItemPacketHeader(self, configElementObj, packetHeaderName, fieldName, values):
        """
        Description
           Modify any Traffic Item packet header.  You will need to use the IxNetwor API browser
           to understand the packetHeaderName, fieldName and data to modify.

           Since a Traffic Item could contain many endpointSet (Flow Groups), a Traffic Item could 
           have multiple configElement objects.  A configElementObj is the object handle for an 
           endpointSet.  You have to get the configElement object first.  To get the ConfigElement
           object, you call getConfigElementObj().  

           self.getConfigElementObj(self, trafficItemObj=None, trafficItemName=None, endpointSetName=None):
           Use case #1: trafficItemName + endpointSetName
           Use case #2: trafficItemObj + endpointSetName
           Use case #3: trafficItemName only (Will assume there is only one configElement object which will be returned)
           Use case #4: trafficItemObj only  (Will assume there is only one configElement object which will be returned)

        Parameters
           configElementObj: <str|obj>: The Traffic Item's Config Element object handle.
           packetHeaderName: <str>: The packet header name. You could get the list of names from the 
                                    IxNetwork API browser under trafficItem/{id}/configElement/{id}/stack.
           fieldName: <str>: The packet header field name. View API browser under:
                             trafficItem/{id}/configElement/{id}/stack/{id}/field
           values: <dict>: Any amount of attributes from the /stack/{id}/field/{id} to modify.

        Example:  For IP Precedence TOS 
           packetHeaderName='ipv4'
           fieldName='Precedence'
           values={'fieldValue': '011 Flash'}
        """
        # /api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/configElement/1/stack/6
        stackIdObj = self.getTrafficItemPktHeaderStackObj(configElementObj=configElementObj,
                                                          packetHeaderName=packetHeaderName)
        
        self.configPacketHeaderField(stackIdObj, fieldName, values)

    def modifyTrafficItemIpPriorityTos(self, trafficItemObj=None, trafficItemName=None, endpointSetName=None,
                                       packetHeaderName='ipv4', fieldName='Precedence', values=None):
        """
        Description
           Modify a Traffic Item Flow group IP Priority TOS fields.

        Parameters
           value: <dict>: {'fieldValue': '000 Routine'|'001 Priority'|'010 Immediate'|'011 Flash'|'100 Flash Override'
                           '101 CRITIC/ECP'|'110 Internetwork Control'}
        
           trafficItemObj: <str|obj>: The Traffic Item object handle.
           trafficItemName: <str|obj>: The Traffic Item name.
           endpointSetName: <str|obj>: The endpointSet name (Flow-Group).

           Option #1: trafficItemName + endpointSetName
           Option #2: trafficItemObj + endpointSetName
           Option #3: trafficItemName only (Will assume there is only one configElement object)
           Option #4: trafficItemObj only  (Will assume there is only one configElement object)

        Requirement
           Call self.getConfigElementObj() to get the config element object first.

        Example
           trafficObj.modifyTrafficItemIpPriorityTos(trafficItemName='Raw MPLS/UDP', values={'fieldValue': '001 Priority'})
        """
        configElementObj = self.getConfigElementObj(trafficItemObj=trafficItemObj, trafficItemName=trafficItemName,
                                                    endpointSetName=endpointSetName)

        self.modifyTrafficItemPacketHeader(configElementObj, packetHeaderName=packetHeaderName,
                                           fieldName=fieldName, values=values)

    def modifyTrafficItemDestMacAddress(self, trafficItemObj=None, trafficItemName=None, endpointSetName=None, values=None):
        """
        Description
           Modify a Traffic Item Flow group IP Priority TOS fields.

        Parameters
           value: <'str'|dict>: 
                  If str: The mac address address
                  If dict: Any or all the properties and the values:

                          {'valueType': 'increment',
                           'startValue': destMacAddress,
                           'stepValue': '00:00:00:00:00:00',
                           'countValue': 1,
                           'auto': False}
           
           trafficItemObj: <str|obj>: The Traffic Item object handle.
           trafficItemName: <str|obj>: The Traffic Item name.
           endpointSetName: <str|obj>: The endpointSet name (Flow-Group).

           Option #1: trafficItemName + endpointSetName
           Option #2: trafficItemObj + endpointSetName
           Option #3: trafficItemName only (Will assume there is only one configElement object)
           Option #4: trafficItemObj only  (Will assume there is only one configElement object)

        Requirement
           Call self.getConfigElementObj() to get the config element object first.

        Example
           trafficObj.modifyTrafficItemDestMacAddress(trafficItemName='Raw MPLS/UDP', values='00:01:01:02:00:01')
        """
        
        if type(values) == str:
            values = {'valueType': 'increment',
                      'startValue': values,
                      'stepValue': '00:00:00:00:00:00',
                      'countValue': 1,
                      'auto': False}

        configElementObj = self.getConfigElementObj(trafficItemObj=trafficItemObj, trafficItemName=trafficItemName,
                                                    endpointSetName=endpointSetName)

        self.modifyTrafficItemPacketHeader(configElementObj, packetHeaderName='ethernet',
                                           fieldName='Destination MAC Address', values=values)

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
        self.ixnObj.logInfo('showPacketHeaderFieldNames: %s' % stackObj+'/field', timestamp=False)
        response = self.ixnObj.get(self.ixnObj.httpHeader+stackObj+'/field')
        for eachField in  response.json():
            id = eachField['id']
            fieldName = eachField['displayName']
            self.ixnObj.logInfo('\t{0}: {1}'.format(id, fieldName), timestamp=False)

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
            In order to know the field names to modify, use showPacketHeaderFieldNames() to display the names:

        stackIdObj: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/{id}/configElement/{id}/stack/{id}

        fieldName: The field name in the packet header to modify.
                   Example. In a MPLS packet header, the fields would be "Label value", "MPLS Exp", etc.

                   Note: Use showPacketHeaderFieldNames(stackObj) API to dispaly your options.

        data: Example:
             data={'valueType': 'valueList', 'valueList': ['1001', '1002'], auto': False}
             data={'valueType': 'increment', 'startValue': '1.1.1.1', 'stepValue': '0.0.0.1', 'countValue': 2}
             data={'valueType': 'increment', 'startValue': '00:01:01:01:00:01', 'stepValue': '00:00:00:00:00:01'}
             data={'valueType': 'increment', 'startValue': 1001, 'stepValue': 1, 'countValue': 2, 'auto': False}
        
        Example: To modify MPLS field:
            packetHeaderObj = trafficObj.getTrafficItemPktHeaderStackObj(trafficItemName='Raw MPLS/UDP', packetHeaderName='mpls')
            trafficObj.configPacketHeaderField(packetHeaderObj,
                                               fieldName='MPLS Exp',
                                               data={'valueType': 'increment',
                                               'startValue': '4',
                                               'stepValue': '1',
                                               'countValue': 1,
                                               'auto': False})
        """
        fieldId = None
        # Get the field ID object by the user defined fieldName
        response = self.ixnObj.get(self.ixnObj.httpHeader+stackIdObj+'/field')
        for eachFieldId in response.json():
            if bool(re.match(fieldName, eachFieldId['displayName'], re.I)):
                fieldId = eachFieldId['id']

        if fieldId == None:
            raise IxNetRestApiException('Failed to located your provided fieldName:', fieldName)

        self.ixnObj.logInfo('configPacketHeaderFieldId:  fieldIdObj: %s' % stackIdObj+'/field/'+str(fieldId), timestamp=False)
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
        self.ixnObj.logInfo('Creating new statview for egress stats...')
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/statistics/view',
                             data={'caption': egressStatViewName,
                                   'treeViewNodeName': 'Egress Custom Views',
                                   'type': 'layer23TrafficFlow',
                                   'visible': True})

        egressStatView = response.json()['links'][0]['href']
        self.ixnObj.logInfo('egressStatView Object: %s' % egressStatView)
        # /api/v1/sessions/1/ixnetwork/statistics/view/12

        self.ixnObj.logInfo('Creating layer23TrafficFlowFilter')
        # Dynamically get the PortFilterId
        response = self.ixnObj.get(self.ixnObj.httpHeader+egressStatView+'/availablePortFilter')
        portFilterId = []
        for eachPortFilterId in response.json():
            #192.168.70.10/Card2/Port1
            self.ixnObj.logInfo('\tAvailable PortFilterId: %s' % eachPortFilterId['name'], timestamp=False)
            if eachPortFilterId['name'] == egressTrackingPort:
                self.ixnObj.logInfo('\tLocated egressTrackingPort: %s' % egressTrackingPort, timestamp=False)
                portFilterId.append(eachPortFilterId['links'][0]['href'])
                break
        if portFilterId == []:
            raise IxNetRestApiException('No port filter ID found')
        self.ixnObj.logInfo('PortFilterId: %s' % portFilterId)

        # Dynamically get the Traffic Item Filter ID
        response = self.ixnObj.get(self.ixnObj.httpHeader+egressStatView+'/availableTrafficItemFilter')
        availableTrafficItemFilterId = []
        for eachTrafficItemFilterId in response.json():
            if eachTrafficItemFilterId['name'] == trafficItemName:
                availableTrafficItemFilterId.append(eachTrafficItemFilterId['links'][0]['href'])
                break
        if availableTrafficItemFilterId == []:
            raise IxNetRestApiException('No traffic item filter ID found.')

        self.ixnObj.logInfo('availableTrafficItemFilterId: %s' % availableTrafficItemFilterId, timestamp=False)
        # /api/v1/sessions/1/ixnetwork/statistics/view/12
        self.ixnObj.logInfo('egressStatView: %s' % egressStatView, timestamp=False)
        layer23TrafficFlowFilter = self.ixnObj.httpHeader+egressStatView+'/layer23TrafficFlowFilter'
        self.ixnObj.logInfo('layer23TrafficFlowFilter: %s' % layer23TrafficFlowFilter, timestamp=False)
        response = self.ixnObj.patch(layer23TrafficFlowFilter,
                              data={'egressLatencyBinDisplayOption': 'showEgressRows',
                                    'trafficItemFilterId': availableTrafficItemFilterId[0],
                                    'portFilterIds': portFilterId,
                                    'trafficItemFilterIds': availableTrafficItemFilterId})

        # Get the egress tracking filter
        egressTrackingFilter = None
        ingressTrackingFilter = None
        response = self.ixnObj.get(self.ixnObj.httpHeader+egressStatView+'/availableTrackingFilter')
        self.ixnObj.logInfo('Available tracking filters for both ingress and egress...', timestamp=False)
        for eachTrackingFilter in response.json():
            self.ixnObj.logInfo('\tFilter Name: {0}: {1}'.format(eachTrackingFilter['id'], eachTrackingFilter['name']), timestamp=False)
            if bool(re.match('Custom: *\([0-9]+ bits at offset [0-9]+\)', eachTrackingFilter['name'])):
                egressTrackingFilter = eachTrackingFilter['links'][0]['href']

            if ingressTrackingFilterName is not None:
                if eachTrackingFilter['name'] == ingressTrackingFilterName:
                    ingressTrackingFilter = eachTrackingFilter['links'][0]['href']

        if egressTrackingFilter is None:
            raise IxNetRestApiException('Failed to locate your defined custom offsets: {0}'.format(egressTrackingOffsetFilter))

        # /api/v1/sessions/1/ixnetwork/statistics/view/23/availableTrackingFilter/3
        self.ixnObj.logInfo('Located egressTrackingFilter: %s' % egressTrackingFilter, timestamp=False)
        enumerationFilter = layer23TrafficFlowFilter+'/enumerationFilter'
        response = self.ixnObj.post(enumerationFilter,
                             data={'sortDirection': 'ascending',
                                   'trackingFilterId': egressTrackingFilter})

        if ingressTrackingFilterName is not None:
            self.ixnObj.logInfo('Located ingressTrackingFilter: %s' % egressTrackingFilter, timestamp=False)
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
            self.ixnObj.logInfo('\tEnabling egress stat counter: %s' % eachStatCounterName, timestamp=False)
            self.ixnObj.patch(self.ixnObj.httpHeader+eachStatCounterObject, data={'enabled': True})

        self.ixnObj.patch(self.ixnObj.httpHeader+egressStatView, data={'enabled': True})
        self.ixnObj.logInfo('createEgressCustomStatView: Done')

        return egressStatView

    def enableTrafficItem(self, trafficItemNumber):
        url = self.ixnObj.sessionUrl+'/traffic/trafficItem/%s' % str(trafficItemNumber)
        response = self.ixnObj.patch(url, data={"enabled": "true"})

    def disableTrafficItem(self, trafficItemNumber):
        url = self.ixnObj.sessionUrl+'/traffic/trafficItem/%s' % str(trafficItemNumber)
        response = self.ixnObj.patch(url, data={"enabled": "false"})

    def enableAllTrafficItems(self, mode=True):
        """
        Description
           Enable or Disable all Traffic Items.
         
        Parameter
           mode: True|False
                 True: Enable all Traffic Items
                 False: Disable all Traffic Items
        """
        queryData = {'from': '/traffic',
                     'nodes': [{'node': 'trafficItem', 'properties': [], 'where': []}]}
        queryResponse = self.ixnObj.query(data=queryData)
        for trafficItem in queryResponse.json()['result'][0]['trafficItem']:
            self.ixnObj.patch(self.ixnObj.httpHeader + trafficItem['href'], data={'enabled': mode})

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

    def checkTrafficState(self, expectedState=['stopped'], timeout=45, ignoreException=False):
        """
        Description
            Check the traffic state for the expected state.
            This is best used to verify that traffic has started before calling getting stats.

        Traffic states are:
            startedWaitingForStats, startedWaitingForStreams, started, stopped,
            stoppedWaitingForStats, txStopWatchExpected, locked, unapplied

        Parameters
            expectedState: <str>:  Input a list of expected traffic state.
                            Example: ['started', startedWaitingForStats'] <-- This will wait until stats has arrived.

            timeout: <int>: The amount of seconds you want to wait for the expected traffic state.
                      Defaults to 45 seconds.
                      In a situation where you have more than 10 pages of stats, you will
                      need to increase the timeout time.

            ignoreException: <bool>: If True, return 1 as failed, and don't raise an Exception.

        Return
            1: If failed.
        """
        if type(expectedState) != list:
            expectedState.split(' ')

        self.ixnObj.logInfo('checkTrafficState: Expecting state: {0}\n'.format(expectedState))
        for counter in range(1,timeout+1):
            response = self.ixnObj.get(self.ixnObj.sessionUrl+'/traffic', silentMode=True)
            currentTrafficState = response.json()['state']
            if currentTrafficState == 'unapplied':
                self.ixnObj.logWarning('\nCheckTrafficState: Traffic is UNAPPLIED')
                self.ixnObj.applyTraffic()

            self.ixnObj.logInfo('\ncheckTrafficState: {trafficState}: Expecting: {expectedStates}.'.format(trafficState=currentTrafficState,
                                                                                                           expectedStates=expectedState),
                                timestamp=False)
            self.ixnObj.logInfo('\tWaited {counter}/{timeout} seconds'.format(counter=counter, timeout=timeout), timestamp=False)
            
            if counter < timeout and currentTrafficState not in expectedState:
                time.sleep(1)
                continue

            if counter < timeout and currentTrafficState in expectedState:
                time.sleep(8)
                self.ixnObj.logInfo('checkTrafficState: Done\n')
                return 0
        
        if ignoreException == False:
            raise IxNetRestApiException('checkTrafficState: Traffic state did not reach the expected state(s): %s' % expectedState)
        else:
            return 1

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

    def getAllTrafficItemObjects(self, getEnabledTrafficItemsOnly=False):
        """
        Description
            Get all the Traffic Item objects.
        
        Parameter
            getEnabledTrafficItemOnly: <bool>
        Return
            A list of Traffic Items
        """
        trafficItemObjList = []
        response = self.ixnObj.get(self.ixnObj.sessionUrl + '/traffic/trafficItem')
        for eachTrafficItem in response.json():
            if getEnabledTrafficItemsOnly == True:
                if eachTrafficItem['enabled'] == True:
                    trafficItemObjList.append(eachTrafficItem['links'][0]['href'])
            else:
                trafficItemObjList.append(eachTrafficItem['links'][0]['href'])

        return trafficItemObjList

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
        self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/traffic/operations/apply/'+response.json()['id'])

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
        self.ixnObj.logInfo('Regenerating traffic items: %s' % trafficItemList)
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def startTraffic(self, regenerateTraffic=True, applyTraffic=True, blocking=False):
        """
        Description
            Start traffic and verify traffic is started.
            This function will also give you the option to regenerate and apply traffic.

        Parameter
            regenerateTraffic: <bool>
                          
            applyTraffic: <bool> 
                          In a situation like packet capturing, you cannot apply traffic after
                          starting packet capture because this will stop packet capturing. 
                          You need to set applyTraffic to False in this case.

            blocking: <bool> If True, API server doesn't return until it has
                             started traffic and ready for stats.  Unblocking is the opposite.

        Syntax
            For blocking state:
               POST:  /api/v1/sessions/{id}/ixnetwork/traffic/operations/startstatelesstrafficblocking'
               DATA:  {arg1: ['/api/v1/sessions/{id}/ixnetwork/traffic/trafficItem/{id}' ...]}

            For non blocking state:
               POST: /api/v1/sessions/1/ixnetwork/traffic/operations/start
               DATA: {arg1: '/api/v1/sessions/{id}/ixnetwork/traffic'}

        Requirements:
            For non blocking state only:

               # You need to check the traffic state before getting stats.
               # Note: Use the configElementObj returned by configTrafficItem()
               if trafficObj.getTransmissionType(configElementObj) == "fixedFrameCount":
                   trafficObj.checkTrafficState(expectedState=['stopped', 'stoppedWaitingForStats'], timeout=45)

               if trafficObj.getTransmissionType(configElementObj) == "continuous":
                   trafficObj.checkTrafficState(expectedState=['started', 'startedWaitingForStats'], timeout=45)
        """
        if regenerateTraffic:
            self.regenerateTrafficItems()

        if applyTraffic:
            self.applyTraffic()

        if blocking == False:
            url = self.ixnObj.sessionUrl+'/traffic/operations/start'
            response = self.ixnObj.post(url, data={'arg1': self.ixnObj.sessionUrl+'/traffic'})
            self.ixnObj.waitForComplete(response, url + '/' + response.json()['id'], timeout=120)

        # Server will go into blocking state until it is ready to accept the next api command.
        if blocking == True:
            enabledTrafficItemList = self.getAllTrafficItemObjects(getEnabledTrafficItemsOnly=True)
            url = self.ixnObj.sessionUrl+'/traffic/trafficItem/operations/startstatelesstrafficblocking'
            response = self.ixnObj.post(url, data={'arg1': enabledTrafficItemList})
            self.ixnObj.waitForComplete(response, url + '/' + response.json()['id'], timeout=120)

    def stopTraffic(self, blocking=False):
        """
        Description
            Stop traffic and verify traffic has stopped.

        Parameters
           blocking: <bool>: True=Synchronous mode. Server will not accept APIs until the process is complete.

        Syntax
            For blocking state:
               POST: /api/v1/sessions/{id}/ixnetwork/traffic/operations/stopstatelesstrafficblocking
               DATA:  {arg1: ['/api/v1/sessions/{id}/ixnetwork/traffic/trafficItem/{id}' ...]}

            For non blocking state:
               POST: /api/v1/sessions/{id}/ixnetwork/traffic/operations/stop
               DATA: {'arg1': '/api/v1/sessions/{id}/ixnetwork/traffic'}
        """
        if blocking == True:
            #queryData = {"from": "/traffic",
            #    "nodes": [{"node": "trafficItem", "properties": ["enabled"], "where": [{"property": "enabled", "regex": "True"}]}]}

            #queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
            #enabledTrafficItemHrefList = [trafficItem['href'] for trafficItem in queryResponse.json()['result'][0]['trafficItem']]

            enabledTrafficItemList = self.getAllTrafficItemObjects(getEnabledTrafficItemsOnly=True)
            url = self.ixnObj.sessionUrl+'/traffic/operations/stopstatelesstrafficblocking'
            response = self.ixnObj.post(url, data={'arg1': enabledTrafficItemList})
            self.ixnObj.waitForComplete(response, url + '/' + response.json()['id'], timeout=120)

        if blocking == False:
            self.ixnObj.logInfo('stopTraffic: %s' % self.ixnObj.sessionUrl+'/traffic/operations/stop')
            url = self.ixnObj.sessionUrl+'/traffic/operations/stop'            
            response = self.ixnObj.post(url, data={'arg1': self.ixnObj.apiSessionId + '/traffic'})
            self.ixnObj.waitForComplete(response, url + '/' + response.json()['id'], timeout=120)

        self.checkTrafficState(expectedState=['stopped'])
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
            self.ixnObj.logInfo('TrafficItem: {0}\n\tName: {1}  Enabled: {2}  State: {3}'.format(ti['id'], ti['name'], ti['enabled'], ti['state']), timestamp=False)
            self.ixnObj.logInfo('\tTrafficType: {0}  BiDirectional: {1}'.format(ti['trafficType'], ti['biDirectional']), timestamp=False)
            for tracking in ti['tracking']:
                self.ixnObj.logInfo('\tTrackings: {0}'.format(tracking['trackBy']), timestamp=False)

            for endpointSet, cElement in zip(ti['endpointSet'], ti['configElement']):
                self.ixnObj.logInfo('\tEndpointSetId: {0}  EndpointSetName: {1}'.format(endpointSet['id'], endpointSet['name']), timestamp=False)
                srcList = []
                for src in endpointSet['sources']:
                    srcList.append(src.split('/ixnetwork')[1])
                dstList = []
                for dest in endpointSet['destinations']:
                    dstList.append(dest.split('/ixnetwork')[1])
                self.ixnObj.logInfo('\t    Sources: {0}'.format(srcList), timestamp=False)
                self.ixnObj.logInfo('\t    Destinations: {0}'.format(dstList), timestamp=False)
                self.ixnObj.logInfo('\t    FrameType: {0}  FrameSize: {1}'.format(cElement['frameSize']['type'], cElement['frameSize']['fixedSize']), timestamp=False)
                self.ixnObj.logInfo('\t    TranmissionType: {0}  FrameCount: {1}  BurstPacketCount: {2}'.format(cElement['transmissionControl']['type'],
                                                                                                cElement['transmissionControl']['frameCount'],
                                                                                                cElement['transmissionControl']['burstPacketCount']), timestamp=False)
                self.ixnObj.logInfo('\t    FrameRateType: {0}  FrameRate: {1}'.format(cElement['frameRate']['type'], cElement['frameRate']['rate']), timestamp=False)
            self.ixnObj.logInfo('\n', end='', timestamp=False)

    def setFrameSize(self, trafficItemName, **kwargs):
        """
        Description
            Modify the frame size.

        Parameters
            type: <str>:  fixed|increment|presetDistribution|quadGaussian|random|weightedPairs
        
            trafficItemName: <str>: The name of the Traffic Item..

        Example:
            trafficObj.setFrameSize('Topo1 to Topo2', type='fxied', fixedSize=128)
            trafficObj.setFrameSize('Topo1 to Topo2', type='increment', incrementFrom=68, incrementStep=2, incrementTo=1200)
        """
        queryData = {'from': '/traffic',
                    'nodes': [{'node': 'trafficItem', 'properties': ['name'], 'where': [{'property': 'name', 'regex': trafficItemName}]},
                              {'node': 'configElement', 'properties': [], 'where': []}]}
        queryResponse = self.ixnObj.query(data=queryData)
        if queryResponse.json()['result'][0]['trafficItem'] == []:
            raise IxNetRestApiException('\nNo such Traffic Item name found: %s' % trafficItemName)

        configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
        self.ixnObj.patch(self.ixnObj.httpHeader+configElementObj+'/frameSize', data=kwargs)

    def configFramePayload(self, configElementObj, payloadType='custom', customRepeat=True, customPattern=None):
        """
        Description
            Configure the frame payload.

        Parameters
            payloadType: <str>: Options:
                           custom, decrementByte, decrementWord, incrementByte, incrementWord, random
            customRepeat: <bool>
            customPattern: <str>: Enter a custom payload pattern
        """
        data = {'type': payloadType, 'customRepeat': customRepeat, 'customPattern': customPattern}
        self.ixnObj.patch(self.ixnObj.httpHeader+configElementObj+'/framePayload', data=data)

    def enableMinFrameSize(self, enable=True):
        """
        Description
           Enable the global traffic option to allow smaller frame size.

        Parameter
           enable: <bool>: True to enable it.
        """
        self.ixnObj.patch(self.ixnObj.sessionUrl+'/traffic', data={'enableMinFrameSize': enable})

    def suspendTrafficItem(self, trafficItemObj, suspend=True):
        """
        Description
           Suspend the Traffic Item from sending traffic.
        
        Parameter
           trafficItemObj: <str>: The Traffic Item object.
           suspend: <bool>: True=suspend traffic.
        
        Syntax
           PATCH: /api/v1/sessions/{id}/ixnetwork/traffic/trafficItem/{id}
           DATA:  {'suspend': True}
        """
        self.ixnObj.patch(self.ixnObj.httpHeader+trafficItemObj, data={'suspend': suspend})



