import time
from IxNetRestApi import IxNetRestApiException

class PortMgmt(object):
    def __init__(self, ixnObj=None):
        self.ixnObj = ixnObj

    def getSelfObject(self):
        # For Python Robot Framework support
        return self

    def setMainObject(self, mainObject):
        # For Python Robot Framework support
        self.ixnObj = mainObject

    def connectToVChassis(self, chassisIp):
        # Connects to the virtual chassis

        url = self.ixnObj.sessionUrl+'/operations/connecttochassis'
        data = {"arg1": chassisIp}

        response = self.ixnObj.post(url, data=data)
        if response == 1: return 1
        if response.json()['state'] == 'ERROR':
            self.ixnObj.logInfo('connectToVChassis error: %s' % response.json()['result'])
            return 1
        else:
            self.ixnObj.logInfo('connectToVChassis: Successfully connected to chassis: %s' % chassisIp)
            while response.json()["state"] == "IN_PROGRESS" or response.json()["state"] == "down":
                if timeout == 0:
                    break
                time.sleep(1)
                response = request.get(self.ixnObj.sessionUrl)
                state = response.json()["state"]
                self.ixnObj.logInfo("\t\t%s" % state)
                timeout = timeout - 1
            return 0

    def connectIxChassis(self, chassisIp, timeout=30):
        """
        Description
           Connect to an Ixia chassis.
           This needs to be done prior to assigning ports for testing.

        Parameter
           chassisIp: <str>|<list>: A string or a list of chassis IP addresses.
           timeout: <int>: Default=30 seconds. The amount of time to wait for the 
                           chassis to be in the ready state.

        Syntax
           /api/v1/sessions/{id}/ixnetwork/availableHardware/chassis

        """
        if isinstance(chassisIp, list) == False:
            chassisIp = chassisIp.split(' ')

        chassisObjList = []
        url = self.ixnObj.sessionUrl+'/availableHardware/chassis'
        for chassisIpAddress in chassisIp:
            data = {'hostname': chassisIpAddress}
            response = self.ixnObj.post(url, data=data)
            if type(response.json()) == list:
                # 8.50 json response is a list.
                chassisIdObj = response.json()[0]['links'][0]['href']
            else:
                chassisIdObj = response.json()['links'][0]['href']
 
            self.ixnObj.logInfo('\n', timestamp=False)
            # Chassis states: down, polling, ready
            for timer in range(1,timeout+1):
                response = self.ixnObj.get(self.ixnObj.httpHeader + chassisIdObj, silentMode=True)
                currentStatus = response.json()['state']
                self.ixnObj.logInfo('connectIxChassis {0}: Status: {1}. Wait {2}/{3} seconds'.format(
                    chassisIpAddress, currentStatus, timer, timeout), timestamp=False)
                if currentStatus != 'ready' and timer < timeout:
                    time.sleep(1)
                if currentStatus != 'ready' and timer == timeout:
                    raise IxNetRestApiException('connectIxChassis: Connecting to chassis {0} failed'.format(chassisIpAddress))
                if currentStatus == 'ready' and timer < timeout:
                    chassisObjList.append(chassisIdObj)
                    break

        # http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/availableHardware/chassis/1
        return chassisObjList

    def disconnectIxChassis(self, chassisIp):
        """
        Description
            Disconnect the chassis (both hardware or virtualChassis).

        Parameter
            chassisIp: <str>: The chassis IP address.

        Syntax
            /api/v1/sessions/{id}/ixnetwork/availableHardware/chassis/{id}
        """
        url = self.ixnObj.sessionUrl+'/availableHardware/chassis'
        response = self.ixnObj.get(url)
        for eachChassisId in response.json():
            if eachChassisId['hostname'] == chassisIp:
                chassisIdUrl = eachChassisId['links'][0]['href']
                self.ixnObj.logInfo('disconnectIxChassis: %s' % chassisIdUrl)
                response = self.ixnObj.delete(self.ixnObj.httpHeader+chassisIdUrl)

    def getChassisId(self, chassisIp):
        """
        Description
           Get the chassis ID based on the chassis IP address.
        
        Parameter
           chassisIp: <str>: The chassis IP address
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/availableHardware/chassis')
        for eachChassis in response.json():
            if eachChassis['ip'] == chassisIp:
                return eachChassis['id']

    def connectVportTo(self, portList):
        """
        Description
           This function assumes that a list of virtual ports are created.
           Connect the portList to the next vport that is not connected to any physical port.

        portList: <list>: A list of ports in a list: [[ixChassisIp, card, port]]
        """
        self.createVports(portList)
        vportObjectList = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        portListIndex = 0
        for vportObj in vportObjectList.json():
            print('\n', vportObj)
            connectedTo = vportObj['connectedTo']
            vportHref = vportObj['links'][0]['href']
            if connectedTo == 'null':
                # RW: 'connectedTo': '/api/v1/sessions/1/ixnetwork/availableHardware/chassis/1/card/1/port/1'
                # ReadOnly: 'assignedTo': '192.168.70.11:1:1'
                chassisIp = portList[portListIndex][0]
                cardNumber = portList[portListIndex][1]
                portNumber = portList[portListIndex][2]
                chassisId = self.getChassisId(chassisIp)
                self.ixnObj.patch(self.ixnObj.sessionUrl+'/availableHardware/chassis/'+str(chassisId)+'/card/'+str(cardNumber)+'/port/'+str(portNumber))
                data = '/api/v1/sessions/{0}/ixnetwork/availableHardware/chassis/{1}/card/{2}/port/{3}'.format(
                    self.ixnObj.sessionIdNumber, chassisId, cardNumber, portNumber)
                self.ixnObj.patch(self.ixnObj.httpHeader+vportHref, data={'connectedTo': data})
                if portListIndex < len(portList):
                    portListIndex += 1
                    continue
                else:
                    break

    def createVports(self, portList=None, rawTrafficVportStyle=False):
        """
        Description
           This API creates virtual ports based on a portList.
           Next step is to call assignPort.

        Parameters
            portList: <list>: Pass in a list of ports in the format of ixChassisIp, slotNumber, portNumber
                              portList = [[ixChassisIp, '1', '1'], [ixChassisIp, '2', '1']]

            rawTrafficVportStyle: <bool>: For raw Traffic Item src/dest endpoints, vports must be in format:
                               /api/v1/sessions1/vport/{id}/protocols

         Return
            A list of vports
        """
        createdVportList = []
        for index in range(0, len(portList)):
            self.ixnObj.logInfo('Creating a new virtual port')
            response = self.ixnObj.post(self.ixnObj.sessionUrl+'/vport')
            vportObj = response.json()['links'][0]['href']
            if rawTrafficVportStyle:
                createdVportList.append(vportObj+'/protocols')
            else:
                createdVportList.append(vportObj)
            if portList != None:
                response = self.ixnObj.get(self.ixnObj.httpHeader+vportObj)
                card = portList[index][1]
                port = portList[index][2]
                portNumber = str(card)+'/'+str(port)
                self.ixnObj.logInfo('\tName: %s' % portNumber)
                response = self.ixnObj.patch(self.ixnObj.httpHeader+vportObj, data={'name': portNumber})

        if createdVportList == []:
            raise IxNetRestApiException('No vports created')

        self.ixnObj.logInfo('createVports: %s' % createdVportList)
        return createdVportList

    def getVportObjectByName(self, portName):
        """
        Description:
           Get the vport object by the specified port name.

        Parameter
           portName: <str>: The name of the virtual port.
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        vportList = ["%s/vport/%s" % (self.ixnObj.sessionUrl, str(i["id"])) for i in response.json()]
        for vportObj in vportList:
            response = self.ixnObj.get(vportObj)
            if response.json()['name'] == portName:
                return vportObj
        return None

    def getVportName(self, vportObj):
        """
        Description
           Get the name of the vport by the specified vport object

        Parameter
            vportObj: <str>: /api/v1/sessions/1/ixnetwork/vport/1
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader+vportObj)
        return response.json()['name']

    def linkUpDown(self, port, action='down'):
        """
        Description
            Flap a port up or down.

        Parameters
            port: <list>: A list of ports in a list.  [[ixChassisIp, str(card), str(port)]] -> ['10.10.10.1', '1', '3']
            action: <str>: up|down
        """
        vport = self.ixnObj.getVports([port])[0]
        self.ixnObj.post(self.ixnObj.sessionUrl+'/vport/operations/linkUpDn', data={'arg1': [vport], 'arg2': action})

    def getAllVportList(self):
        """
        Description
            Returns a list of all the created virtual ports

        Returns
            List of vports: ['/api/v1/sessions/1/ixnetwork/vport/1', '/api/v1/sessions/1/ixnetwork/vport/2']
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        vportList = ['%s' % vport['links'][0]['href'] for vport in response.json()]
        return vportList

    def getVports(self, portList):
        """
        Description
            Get the vports for the portList

        Parameter
            portList: <list>: A list of ports in a list: [[str(chassisIp), str(slotNumber), str(portNumber)]]
                      Example 1: [[ixChassisIp, '1', '1']]
                      Example 2: [[ixChassisIp, '1', '1'], [ixChassisIp, '2', '1']]

        Returns
             Vports in a list: ['/api/v1/sessions/1/ixnetwork/vport/1', /api/v1/sessions/1/ixnetwork/vport/2']
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        vportList = []

        for vportAttributes in response.json():
            currentVportId = vportAttributes['links'][0]['href']
            # "assignedTo": "192.168.70.10:1:1
            assignedTo = vportAttributes['assignedTo']
            if assignedTo == '':
                continue

            chassisIp = assignedTo.split(':')[0]
            cardNum = assignedTo.split(':')[1]
            portNum = assignedTo.split(':')[2]
            port = [chassisIp, cardNum, portNum]

            if port in portList:
                # ['192.168.70.10', '1', '1']
                vport = vportAttributes['links'][0]['href']
                vportList.append(vport)

        # Returns:
        # ['/api/v1/sessions/1/ixnetwork/vport/1', /api/v1/sessions/1/ixnetwork/vport/2']
        return vportList

    def getPhysicalPortsFromCreatedVports(self):
        """
        Description
            Get all the ports that are configured.

        Return
            None or a list of ports in format: [['192.168.70.11', '1', '1'], ['192.168.70.11', '2', '1']]
        """
        portList = []
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        vportList = ['%s' % vport['links'][0]['href'] for vport in response.json()]

        for eachVport in vportList:
            response = self.ixnObj.get(self.ixnObj.httpHeader+eachVport)
            assignedTo = response.json()['assignedTo']
            # assignedTo: 192.168.70.11:2:1
            if assignedTo:
                chassis = assignedTo.split(':')[0]
                card = assignedTo.split(':')[1]
                port = assignedTo.split(':')[2]
                portList.append([chassis, card, port])
        return portList

    def getPhysicalPortFromVport(self, vportList):
        """
        Description
            Get the physical ports assigned to the vport objects.

        Parameter
            vportList: ['/api/v1/sessions/1/ixnetwork/vport/1']

        Returns
            A list of ports: ['192.168.70.11:1:1']
        """
        portList = []
        for eachVport in vportList:
            response = self.ixnObj.get(self.ixnObj.httpHeader+eachVport)
            assignedTo = response.json()['assignedTo']
            if assignedTo:
                portList.append(assignedTo)
        return portList

    def verifyPortConnectionStatus(self, vport=None):
        """
        Description
           Verify port connection status for errors such as License Failed, 
           Version Mismatch, Incompatible IxOS version, or any other error.
        """
        self.ixnObj.logInfo('verifyPortConnectionStatus')
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')

        for vport in response.json():
            connectionStatus = vport['connectionStatus']
            if 'Port Released' in connectionStatus:
                raise IxNetRestApiException(connectionStatus)

    def assignPorts(self, portList, createVports=False, rawTraffic=False, configPortName=True, timeout=120):
        """
        Description
            Assuming that you already connected to an ixia chassis and ports are available for usage.
            Use this API to assign physical ports to the virtual ports.

        Parameters
            portList: <list>: A list of ports in a list: [ [ixChassisIp, '1','1'], [ixChassisIp, '1','2'] ]

            createVports: <bool>: Optional:
                          If True: Create vports to the amount of portList.
                          If False: Automatically create vport on the server side. Optimized for port bootup performance. 

            rawTraffic: <bool>:  If traffic item is raw, then vport needs to be /vport/{id}/protocols
            resetPortCput: <bool>: Default=False. Some cards like the Novus 10GigLan requires a cpu reboot.
            timeout: <int>: Timeout for port up state. Default=90 seconds.

        Syntaxes
            POST: /api/v1/sessions/{id}/ixnetwork/operations/assignports
                  data={arg1: [{arg1: ixChassisIp, arg2: 1, arg3: 1}, {arg1: ixChassisIp, arg2: 1, arg3: 2}],
                        arg2: [],
                        arg3: ['/api/v1/sessions/{1}/ixnetwork/vport/1',
                               '/api/v1/sessions/{1}/ixnetwork/vport/2'],
                        arg4: true}  <-- True will clear port ownership
                  headers={'content-type': 'application/json'}

            GET:  /api/v1/sessions/{id}/ixnetwork/operations/assignports/1
                  data={}
                  headers={}
            Expecting:   RESPONSE:  SUCCESS
        """
        # Verify if the portList has duplicates.
        self.verifyForDuplicatePorts(portList)

        # Verify if there is existing vports. If yes, user either loaded a saved config file or 
        # the configuration already has vports.
        # If loading a saved config file and reassigning ports, assign ports to existing vports.
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')

        # If response.json() != [], means there are existing vports created already.
        if response.json() != []:
            mode = 'modify'
            preamble = self.ixnObj.sessionUrl.split('/api')[1]
            vportList = ["/api%s/vport/%s" % (preamble, str(i["id"])) for i in response.json()]
            if len(vportList) != len(portList):
                raise IxNetRestApiException('assignPorts: The amount of configured virtual ports:{0} is not equal to the amount of  portList:{1}'.format(len(vportList), len(portList)))

        else:
            if createVports == False:
                vportList = []

            if createVports:
                self.createVports(portList)
                response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
                preamble = self.ixnObj.sessionUrl.split('/api')[1]

                vportList = ["/api%s/vport/%s" % (preamble, str(i["id"])) for i in response.json()]
                if len(vportList) != len(portList):
                    raise IxNetRestApiException('assignPorts: The amount of configured virtual ports:{0} is not equal to the amount of  portList:{1}'.format(len(vportList), len(portList)))

        data = {"arg1": [], "arg2": [], "arg3": vportList, "arg4": 'true'}
        [data["arg1"].append({"arg1":str(chassis), "arg2":str(card), "arg3":str(port)}) for chassis,card,port in portList]
        url = self.ixnObj.sessionUrl+'/operations/assignports'
        response = self.ixnObj.post(url, data=data)
        response = self.ixnObj.waitForComplete(response, url + '/' + response.json()['id'], silentMode=False, timeout=timeout, ignoreException=True)

        if response.json()['state'] == 'EXCEPTION':
            # Some cards like the Novus 10gLan sometimes requires a cpu reboot.
            # To reboot the port cpu, the ports have to be assigned to a vport first.
            # So it has to be done at this spot.
            self.resetPortCpu(vportList=vportList, portList=portList)
            self.verifyPortState()
            
            raise IxNetRestApiException('assignPort Error: {}'.format(response.json()['message']))

        elif response.json()['state'] == 'IN_PROGRESS':
            raise IxNeRestApiException('assignPort Error: Port failed to boot up after 120 seconds')

        else:
            response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
            for vport in response.json():
                chassisIp = vport['assignedTo'].split(':')[0]
                slot = vport['assignedTo'].split(':')[1]
                port = vport['assignedTo'].split(':')[2]
                currentPort = [chassisIp, int(slot), int(port)]
                for chassis,card,port in portList:
                    currentPortList = [chassis, int(card), int(port)]
                    if set(currentPort) & set(currentPortList):
                        if 'License Failed' in vport['connectionStatus']:
                            raise IxNetRestApiException('Port License failed.')
                        if vport['connectionStatus'] == 'connectedLinkDown':
                            raise IxNetRestApiException('Port link connection is down: {0}'.format(vport['assignedTo']))

        if configPortName:
            # Name the vports
            for vportObj in self.getAllVportList():
                port = self.getPhysicalPortFromVport([vportObj])[0]
                chassisIp = port.split(':')[0]
                card = port.split(':')[1]
                port = port.split(':')[2]
                self.ixnObj.patch(self.ixnObj.httpHeader+vportObj, data={'name': card+'/'+port})

        if rawTraffic:
            vportProtocolList = []
            for vport in self.getAllVportList():
                vportProtocolList.append(vport+'/protocols')
            return vportProtocolList
        else:
            return vportList

    def unassignPorts(self, deleteVirtualPorts=False):
        """
        Description
            Unassign all virtual ports from the configuration.

        Parameters
            deleteVirtualPorts: <bool>:
                                True = Delete the virtual ports from the configuration.
                                False = Unassign the virtual ports from the configuration.

        Syntaxes
            POST:  http://{apiServerIp:port}/api/v1/sessions/{id}/ixnetwork/vport/operations/unassignports
                   data={arg1: [http://{apiServerIp:port}/api/v1/sessions/{id}/ixnetwork/vport/1,
                                http://{apiServerIp:port}/api/v1/sessions/{id}/ixnetwork/vport/2],
                         arg2: true|false}
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        vportList = ["%s/vport/%s" % (self.ixnObj.sessionUrl, str(i["id"])) for i in response.json()]
        url = self.ixnObj.sessionUrl+'/vport/operations/unassignports'
        response = self.ixnObj.post(url, data={'arg1': vportList, 'arg2': deleteVirtualPorts})
        self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/vport/operations/unassignports/'+response.json()['id'], timeout=120)

    def releaseAllPorts(self):
        """
        Description
            Release all the connected ports.
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        vportList = ["%s/vport/%s" % (self.ixnObj.sessionUrl, str(i["id"])) for i in response.json()]
        url = self.ixnObj.sessionUrl+'/vport/operations/releaseport'
        response = self.ixnObj.post(url, data={'arg1': vportList})
        if response.json()['state'] == 'SUCCESS': return 0
        if response.json()['id'] != '':
            self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'], timeout=120)
            
    def releasePorts(self, portList):
        """
        Description
            Release the specified ports in a list.

        Parameter
            portList: <list>: A list of ports in a list, to release in format of...
                      [[ixChassisIp, str(cardNum), str(portNum)], [], [] ...]
        """
        vportList = []
        for port in portList:
            vport = self.getVports([port])
            if vport == []:
                continue
            vportList.append(vport[0])

        url = self.ixnObj.sessionUrl+'/vport/operations/releaseport'
        response = self.ixnObj.post(url, data={'arg1': vportList})
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'], timeout=120)

    def resetPortCpu(self, vportList=None, portList=None, timeout=90):
        """
        Description
            Reset/Reboot ports CPU.
            Must call IxNetRestApi.py waitForComplete() afterwards to verify port state
        
        Parameter
            vportList: <list>: A list of one or more vports to reset.
        """
        url = self.ixnObj.sessionUrl+'/vport/operations/resetportcpu'
        if vportList == None:
            vportList = self.getVportFromPortList(portList)

        response = self.ixnObj.post(url, data={'arg1': vportList})
        self.ixnObj.waitForComplete(response, url + '/' +response.json()['id'], silentMode=False, timeout=timeout)

    def clearPortOwnership(self, portList):
        """
            Description
                Clear port ownership on the portList

            Parameters
                portList: <list>: A list of ports in a list: [[chassisIp, cardId, portId]]
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/availableHardware/chassis')
        for eachChassis in response.json():
            chassisIp = eachChassis['ip']
            chassisHref = eachChassis['links'][0]['href']

            for userPort in portList:
                userChassisIp = userPort[0]
                if userChassisIp != chassisIp:
                    continue
                userCardId = userPort[1]
                userPortId = userPort[2]
                url = self.ixnObj.httpHeader+chassisHref+'/card/'+str(userCardId)+'/port/'+str(userPortId)+'/operations/clearownership'
                data = {'arg1': [chassisHref+'/card/'+str(userCardId)+'/port/'+str(userPortId)]}
                self.ixnObj.post(url, data=data)

    def isPortConnected(self, portList):
        """
        Description
            Verify if the port is connected or released

        Parameters
            portList: <list>: A list of ports in a list:  [[ixChassisIp, str(cardNumber), str(portNumber)]]

        Return
            A list of 'connected' and 'released'.
        """
        returnValues = []
        for port in portList:
            vport = self.getVports([port])
            if vport == []:
                returnValues.append('released')
                continue
            response = self.ixnObj.get(self.ixnObj.httpHeader+vport[0])
            connectedStatus = response.json()['connectionStatus']
            print('\nisPortConnected:', port)
            if connectedStatus == 'Port Released':
                self.ixnObj.logInfo('\tFalse: %s' % connectedStatus)
                returnValues.append('released')
            else:
                self.ixnObj.logInfo('\tTrue: %s' % connectedStatus)
                returnValues.append('connected')
        return returnValues

    def verifyForDuplicatePorts(self, portList):
        """
        Description
           Verify if the portList has any duplicate ports.
           Raise an exception if true.
        """
        duplicatePorts = [x for n, x in enumerate(portList) if x in portList[:n]]
        if duplicatePorts:
            raise IxNetRestApiException('\nYour portList has duplicate ports {0}'.format(duplicatePorts))

    def arePortsAvailable(self, portList, raiseException=True):
        """
        Description:
           Verify if any of the portList is owned.

        Parameter: <list>: A list of ports in a list.
                   portList: [ ['192.168.70.11', '1', '1'], ['192.168.70.11', '2', '1'] ]

        raiseException: <bool>: To continue or not to continue if there is an error.

        Return:
            - List of ports that are currently owned
            - 0: If portList are available
        """
        # Verify if the portList has duplicates.
        self.verifyForDuplicatePorts(portList)

        self.ixnObj.logInfo('Verify if ports are currently owned')
        portOwnedList = []
        for port in portList:
            chassisIp = port[0]
            cardId = port[1]
            portId = port[2]
            try:
                queryData = {"from": "/availableHardware",
                                "nodes": [{"node": "chassis", "properties": ["ip"], "where": [{"property": "ip", "regex": chassisIp}]},
                                        {"node": "card", "properties": ["cardId"], "where": [{"property": "cardId", "regex": cardId}]},
                                        {"node": "port", "properties": ["portId", "owner"], "where": [{"property": "portId", "regex": portId}]}]}

                self.ixnObj.logInfo('Querying for %s/%s/%s' % (chassisIp, cardId, portId))
                queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
                queryResponse.json()['result'][0]['chassis'][0]['ip']
                queryResponse.json()['result'][0]['chassis'][0]['card'][0]['id']
                queryResponse.json()['result'][0]['chassis'][0]['card'][0]['port'][0]['portId']
            except:
                raise IxNetRestApiException('\nNot found: {0}:{1}:{2}'.format(chassisIp, cardId, portId))

            self.ixnObj.logInfo('Port currently owned by: %s' % queryResponse.json()['result'][0]['chassis'][0]['card'][0]['port'][0]['owner'])
            if queryResponse.json()['result'][0]['chassis'][0]['card'][0]['port'][0]['owner'] != '':
                self.ixnObj.logInfo('Port is still owned: {0}/cardId:{1}/portId:{2}'.format(chassisIp, cardId, portId))
                portOwnedList.append([chassisIp, cardId, portId])

        self.ixnObj.logInfo('Ports are still owned: %s' % portOwnedList)

        if portOwnedList != []:
            if raiseException:
                raise IxNetRestApiException('arePortsAvailable: Ports are still owned')
            else:
                return portOwnedList
        return 0

    def verifyPortState(self, timeout=70):
        """
        Description
            Verify port states for all the vports connected to physical ports.

        Parameter
            timeout: <int>: The timeout value to declare as failed. Default=70 seconds.
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        vportList = [metaDatas["links"][0]['href'] for metaDatas in response.json()]
        for eachVport in vportList:
            for counter in range(1,timeout+1):
                stateResponse = self.ixnObj.get(self.ixnObj.httpHeader+eachVport+'?includes=state,connectionStatus', silentMode=True)
                assignedToResponse = self.ixnObj.get(self.ixnObj.httpHeader+eachVport+'?includes=assignedTo', silentMode=True)

                if 'Port Released' in stateResponse.json()['connectionStatus']:
                    raise IxNetRestApiException(stateResponse.json()['connectionStatus'])

                if stateResponse.json()['state'] == 'unassigned':
                    self.ixnObj.logWarning('\nThe vport {0} is not assigned to a physical port. Skipping this vport verification.'.format(eachVport))
                    break

                self.ixnObj.logInfo('Port: %s' % assignedToResponse.json()['assignedTo'])
                self.ixnObj.logInfo('\tVerifyPortState: %s\n\tWaiting %s/%s seconds' % (stateResponse.json()['state'], counter, timeout), timestamp=False)
                if counter < timeout and stateResponse.json()['state'] in ['down', 'busy']:
                    time.sleep(1)
                    continue
                if counter < timeout and stateResponse.json()['state'] in ['up', 'connectedLinkUp']:
                    break
                if counter == timeout and stateResponse.json()['state'] == 'down':
                    # Failed
                    raise IxNetRestApiException('Port failed to come up')

    def getVportFromPortList(self, portList):
        """
        Description
           Get a list of vports from the specified portList.

        Parameter
           portList: <list>: Format: [[ixChassisIp, cardNumber1, portNumber1], [ixChassisIp, cardNumber1, portNumber2]]
    
        Return
           A list of vports.
           [] if vportList is empty.
        """
        vportList = []
        for eachPort in portList:
            chassisIp = eachPort[0]
            card = eachPort[1]
            portNum = eachPort[2]
            port = chassisIp+':'+card+':'+portNum
            # {'href': '/api/v1/sessions/1/ixnetwork/',
            # 'vport': [{'id': 2, 'href': '/api/v1/sessions/1/ixnetwork/vport/2', 'assignedTo': '10.10.10.8:1:2'}]}
            queryData = {"from": "/",
                         "nodes": [{"node": "vport", "properties": ["assignedTo"],
                                    "where": [{"property": "assignedTo", "regex": port}]
                                }]}
            
            queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
            vport = queryResponse.json()['result'][0]['vport']
            if vport == []:
                raise IxNetRestApiException('getVportFromPortList error: The port has no vport and not assigned. Check for port typo: {0}'.format(port))

            if vport:
                # Appending vportList: ['/api/v1/sessions/1/ixnetwork/vport/1', '/api/v1/sessions/1/ixnetwork/vport/2']
                vportList.append(vport[0]['href'])
        return vportList
                                
    def modifyPortMediaType(self, portList='all', mediaType='fiber'):
        """
        Description
           Modify the port media type: fiber, copper, SGMII

        Parameters
           portList: <'all'|list of ports>: 
                     <list>: Format: [[ixChassisIp, cardNumber1, portNumber1], [ixChassisIp, cardNumber1, portNumber2]]
                     Or if portList ='all', will modify all assigned ports to the specified mediaType.

           mediaType: <str>: copper, fiber or SGMII
        """
        self.ixnObj.logInfo('modifyPortMediaType: {0}'.format(mediaType))
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        if portList == 'all':
            #vportList = self.getAllVportList()
            portList = self.getPhysicalPortsFromCreatedVports()

        # vportList: ['/api/v1/sessions/1/ixnetwork/vport/1', '/api/v1/sessions/1/ixnetwork/vport/2']
        vportList = self.getVportFromPortList(portList)
        print('\n---- modifyPortMediaType vportList:', vportList)

        for vport in vportList:
            response = self.ixnObj.get(self.ixnObj.httpHeader+vport, silentMode=True)
            portType = response.json()['type']
            self.ixnObj.patch(self.ixnObj.httpHeader+vport+'/l1Config/'+portType, data={'media': mediaType})
