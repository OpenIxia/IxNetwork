import time
from IxNetRestApi import IxNetRestApiException

class PortMgmt(object):
    def __init__(self, ixnObj):
        self.ixnObj = ixnObj

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

    def connectIxChassis(self, chassisIp):
        """
        Description
           Connect to an Ixia chassis.
           This needs to be done prior to assigning ports for testing.

        Syntax
           /api/v1/sessions/1/ixnetwork/availableHardware/chassis

        Parameter
           chassisIp: The chassis IP address.
        """
        url = self.ixnObj.sessionUrl+'/availableHardware/chassis'
        data = {'hostname': chassisIp}
        response = self.ixnObj.post(url, data=data)
        chassisIdObj = response.json()['links'][0]['href']
        # Chassis states: down, polling, ready
        for timer in range(1,61):
            response = self.ixnObj.get(self.ixnObj.httpHeader + chassisIdObj, silentMode=True)
            currentStatus = response.json()['state']
            self.ixnObj.logInfo('connectIxChassis {0}: Status: {1}'.format(chassisIp, currentStatus))
            if currentStatus != 'ready' and timer < 60:
                time.sleep(1)
            if currentStatus != 'ready' and timer == 60:
                raise IxNetRestApiException('connectIxChassis: Connecting to chassis {0} failed'.format(chassisIp))
            if currentStatus == 'ready' and timer < 60:
                break

        # http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/availableHardware/chassis/1
        return self.ixnObj.httpHeader + chassisIdObj

    def disconnectIxChassis(self, chassisIp):
        """
        Description
            Disconnect the chassis (both hardware or virtualChassis).

        Syntax
            http://{apiServerIp:11009}/api/v1/sessions/1/ixnetwork/availableHardware/chassis/<id>

        Parameter
            chassisIp: The chassis IP address.
        """
        url = self.ixnObj.sessionUrl+'/availableHardware/chassis'
        response = self.ixnObj.get(url)
        for eachChassisId in response.json():
            if eachChassisId['hostname'] == chassisIp:
                chassisIdUrl = eachChassisId['links'][0]['href']
                self.ixnObj.logInfo('\ndisconnectIxChassis: %s' % chassisIdUrl)
                response = self.ixnObj.delete(self.ixnObj.httpHeader+chassisIdUrl)

    def createVports(self, portList=None, rawTrafficVportStyle=False):
        """
        Description
           This API creates virtual ports based on a portList.

         portList:  Pass in a list of ports in the format of ixChassisIp, slotNumber, portNumber
           portList = [[ixChassisIp, '1', '1'],
                       [ixChassisIp, '2', '1']]

         rawTrafficVportStyle = For raw Traffic Item src/dest endpoints, vports must be in format:
                                /api/v1/sessions1/vport/{id}/protocols

         Next step is to call assignPort.

         Return: A list of vports
        """
        createdVportList = []
        for index in range(0, len(portList)):
            response = self.ixnObj.post(self.ixnObj.sessionUrl+'/vport')
            vportObj = response.json()['links'][0]['href']
            self.ixnObj.logInfo('\ncreateVports: %s' % vportObj)
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

        self.ixnObj.logInfo('\ncreateVports: %s' % createdVportList)
        return createdVportList

    def getVportObjectByName(self, portName):
        """
        Description:
           Get the vport object by the specified port name.
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

        vportObj: "http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/vport/1"
        """
        response = self.ixnObj.get(vportObj)
        return response.json()['name']

    def linkUpDown(self, port, action='down'):
        """
        Description
            Flap a port up or down.

        Parameters
            port: [ixChassisIp, str(card), str(port)] -> ['10.10.10.1', '1', '3']

        action
            up|down
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
            portList: [[str(chassisIp), str(slotNumber), str(portNumber)]]
                      Example 1: [[ixChassisIp, '1', '1']]
                      Example 2: [[ixChassisIp, '1', '1'], [ixChassisIp, '2', '1']]

        Returns
             Vports in a list: ['/api/v1/sessions/1/ixnetwork/vport/1', /api/v1/sessions/1/ixnetwork/vport/2']
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        vportList = []

        for vportAttributes in response.json():
            #print(vportAttributes, end='\n')
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
            portList.append(assignedTo)
        return portList

    def assignPorts(self, portList, createVports=False, rawTraffic=False):
        """
        Description
            Assuming that you already connected to an ixia chassis and ports are available for usage.
            Use this API to assign physical ports to the virtual ports.

        Parameters
            portList: [ [ixChassisIp, '1','1'], [ixChassisIp, '1','2'] ]

            createVports: To automatically create virtual ports prior to assigning ports.
                          This must be set to True if you are building a configuration from scratch.

            rawTraffic: True|False.  If traffic config is raw, then vport needs to be /vport/{id}/protocols

        Syntaxes
            POST: http://{apiServerIp:port}/api/v1/sessions/{id}/ixnetwork/operations/assignports
                  data={arg1: [{arg1: ixChassisIp, arg2: 1, arg3: 1}, {arg1: ixChassisIp, arg2: 1, arg3: 2}],
                        arg2: [],
                        arg3: [http://{apiServerIp:port}/api/v1/sessions/{1}/ixnetwork/vport/1,
                               http://{apiServerIp:port}/api/v1/sessions/{1}/ixnetwork/vport/2],
                        arg4: true}
                  headers={'content-type': 'application/json'}
            GET:  http://{apiServerIp:port}/api/v1/sessions/{id}/ixnetwork/operations/assignports/1
                  data={}
                  headers={}
            Expecting:   RESPONSE:  SUCCESS
        """
        if createVports:
            self.createVports(portList)
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        preamble = self.ixnObj.sessionUrl.split('/api')[1]
        #vportList = ["%s/vport/%s" % (self.ixnObj.sessionUrl, str(i["id"])) for i in response.json()]
        vportList = ["/api%s/vport/%s" % (preamble, str(i["id"])) for i in response.json()]
        if len(vportList) != len(portList):
            raise IxNetRestApiException('assignPorts: The amount of configured virtual ports:{0} is not equal to the amount of  portList:{1}'.format(len(vportList), len(portList)))

        data = {"arg1": [], "arg2": [], "arg3": vportList, "arg4": "true"}
        [data["arg1"].append({"arg1":str(chassis), "arg2":str(card), "arg3":str(port)}) for chassis,card,port in portList]
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/operations/assignports', data=data)
        if self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/operations/assignports/'+response.json()['id'], timeout=120) == 1:
            raise IxNetRestApiException('assignPorts: Ports not coming up:', portList)
        if rawTraffic:
            vportProtocolList = []
            for vport in vportList:
                vportProtocolList.append(vport+'/protocols')
            return vportProtocolList
        else:
            return vportList

    def unassignPorts(self, deleteVirtualPorts=False):
        """
        Description
            Unassign all virtual ports from the configuration.

        Parameters
            deleteVirtualPorts: True|False
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
        if self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/vport/operations/unassignports/'+response.json()['id'], timeout=120) == 1:
            raise IxNetRestApiException

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
            if self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'], timeout=120) == 1:
                raise IxNetRestApiException

    def releasePorts(self, portList):
        """
        Description
            Release the specified ports in portList.

        Parameter
            portList: A list of ports to release in format of...
                      [[ixChassisIp, str(cardNum), str(portNum)], ...]
        """
        for port in portList:
            vport = self.getVports([port])
            if vport == []:
                continue
            url = self.ixnObj.httpHeader+vport[0]+'/operations/releaseport'
            response = self.ixnObj.post(url, data={'arg1': vport})
            if response.json()['state'] == 'SUCCESS': continue
            if response.json()['id'] != '':
                if self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'], timeout=120) == 1:
                    raise IxNetRestApiException('releasePorts failed')

    def clearPortOwnership(self, portList):
        """
            Description
                Clear port ownership on the portList

            Parameters
                portList: [[chassisIp, cardId, portId]]
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/availableHardware/chassis')
        for eachChassis in response.json():
            chassisIp = eachChassis['ip']
            chassisHref = eachChassis['links'][0]['href']

            for userPort in portList:
                userChassisIp = userPort[0]
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
            portList: [[ixChassisIp, str(cardNumber), str(portNumber)]]

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

    def arePortsAvailable(self, portList, raiseException=True):
        """
        Description: Verify if any of the portList is owned.

        Parameter:
           portList: Example: [ ['192.168.70.11', '1', '1'], ['192.168.70.11', '2', '1'] ]

        Return:
            - List of ports that are currently owned
            - 0: If portList are available
        """
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
                queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
                queryResponse.json()['result'][0]['chassis'][0]['ip']
                queryResponse.json()['result'][0]['chassis'][0]['card'][0]['id']
                queryResponse.json()['result'][0]['chassis'][0]['card'][0]['port'][0]['portId']
            except:
                raise IxNetRestApiException('\nNot found:', chassisIp, cardId, portId)

            self.ixnObj.logInfo('\nPort currently owned by: %s' % queryResponse.json()['result'][0]['chassis'][0]['card'][0]['port'][0]['owner'])
            if queryResponse.json()['result'][0]['chassis'][0]['card'][0]['port'][0]['owner'] != '':
                self.ixnObj.logInfo('Port is still owned: {0}/cardId:{1}/portId:{2}'.format(chassisIp, cardId, portId))
                portOwnedList.append([chassisIp, cardId, portId])

        self.ixnObj.logInfo('\nPorts are still owned: %s' % portOwnedList)

        if portOwnedList != []:
            if raiseException:
                raise IxNetRestApiException
            else:
                return portOwnedList
        return 0

    def verifyPortState(self, timeout=70):
        #timer = timeout
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        vportList = ["%s/vport/%s" % (self.ixnObj.sessionUrl, str(i["id"])) for i in response.json()]
        for eachVport in vportList:
            for counter in range(1,timeout+1):
                response = self.ixnObj.get(eachVport, silentMode=True)
                self.ixnObj.logInfo('\nPort: %s' % response.json()['assignedTo'])
                self.ixnObj.logInfo('\tVerifyPortState: %s\n\tWaiting %s/%s seconds' % (response.json()['state'], counter, timeout))
                if counter < timeout and response.json()['state'] in ['down', 'busy']:
                    time.sleep(1)
                    continue
                if counter < timeout and response.json()['state'] == 'up':
                    break
                if counter == timeout and response.json()['state'] == 'down':
                    # Failed
                    raise IxNetRestApiException('Port failed to come up')

