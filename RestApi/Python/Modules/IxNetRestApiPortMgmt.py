import time
from IxNetRestApi import IxNetRestApiException


class PortMgmt(object):
    def __init__(self, ixnObj=None):
        self.ixnObj = ixnObj
        self.ixNetwork = ixnObj.ixNetwork

    def getSelfObject(self):
        # For Python Robot Framework support
        return self

    def setMainObject(self, mainObject):
        # For Python Robot Framework support
        self.ixnObj = mainObject

    def connectToVChassis(self, chassisIp):
        """
        Description
           Connect to an virtual chassis chassis.

        Parameter
           chassisIp: <str>: A string of chassis IP addresses.
        """
        counterStop = 45
        for counter in range(1, counterStop + 1):
            chassisStatus = self.ixNetwork.AvailableHardware.Chassis.add(Hostname=chassisIp)
            if chassisStatus.State != 'ready':
                self.ixnObj.logInfo('\nChassis {0} is not connected yet. Waiting {1}/{2} seconds'.
                                    format(chassisIp, counter, counterStop))
                time.sleep(1)

            if chassisStatus.State == 'ready':
                self.ixnObj.logInfo('\n{0}'.format(chassisStatus))
                return 0

            if counter == counterStop:
                raise Exception('\nFailed to connect to chassis: {0}'.format(chassisIp))

    def connectIxChassis(self, chassisIp, timeout=45, **kwargs):
        """
        Description
           Connect to an Ixia chassis.

        Parameter
           chassisIp: <str>|<list>: A string or a list of chassis IP addresses.
           timeout: <int>: Default=30 seconds. The amount of time to wait for the chassis to be
           in the ready state.

           kwargs: Any chassis attributes and values. For example, if two chassis are dasisy
           chained, include: chainTopology=None, masterChassis='10.10.10.1', sequenceId=1

        """
        if not isinstance(chassisIp, list):
            chassisIp = chassisIp.split(' ')

        chassisObjList = []
        for ixChassisIp in chassisIp:
            self.ixnObj.logInfo("Connecting to chassis {}".format(ixChassisIp))
            for counter in range(1, timeout + 1):

                chassisStatus = self.ixNetwork.AvailableHardware.Chassis.add(Hostname=ixChassisIp)
                if chassisStatus.State != 'ready':
                    self.ixnObj.logInfo('\nChassis {0} is not connected yet. Waiting {1}/{2} '
                                        'seconds'.format(ixChassisIp, counter, timeout))
                    time.sleep(1)

                if chassisStatus.State == 'ready':
                    self.ixnObj.logInfo('\n{0}'.format(chassisStatus))
                    chassisObjList.append(chassisStatus)
                    break

                if counter == timeout:
                    raise Exception('\nFailed to connect to chassis: {0}'.format(ixChassisIp[0]))

        return chassisObjList

    def disconnectIxChassis(self, chassisIp):
        """
        Description
            Disconnect the chassis (both hardware or virtualChassis).

        Parameter
            chassisIp: <str>: The chassis IP address.

        """
        self.ixnObj.logInfo("disconnecting from chassis {}".format(chassisIp))
        try:
            self.ixNetwork.AvailableHardware.Chassis.find(Hostname=chassisIp).remove()
        except Exception as err:
            self.ixnObj.logInfo('Errored : \n {}'.format(err))
            raise Exception("Failed disconnecting chassis {}".format(chassisIp))

    def getChassisId(self, chassisIp):
        """
         This parameter is used to get chassis Id from Chassis Ip for REST API
         For RESTpy we can ignore this
        """
        pass

    def connectVportTo(self, portList):
        """
        Description
           This function assumes that a list of virtual ports are created.
           Connect the portList to the next vport that is not connected to any physical port.

        portList: <list>: A list of ports in a list: [[ixChassisIp, card, port]]
        """
        self.createVports(portList)
        testPorts = []
        vportList = self.ixNetwork.Vport.find()
        for port in portList:
            testPorts.append(dict(Arg1=port[0], Arg2=port[1], Arg3=port[2]))

        self.ixnObj.logInfo('\nAssignPorts: {0}'.format(portList))
        try:
            self.ixNetwork.AssignPorts(testPorts, [], vportList, True)
        except Exception as err:
            self.ixnObj.logInfo('Errored : \n {}'.format(err))
            raise Exception("Failed to Assign ports {} ".format(portList))

    def createVports(self, portList=None, rawTrafficVportStyle=False):
        """
        Description
           This API creates virtual ports based on a portList.
           Next step is to call assignPort.

        Parameters
            portList: <list>: Pass in a list of ports in the format of
                                    ixChassisIp, slotNumber, portNumber
                                    portList = [[ixChassisIp, '1', '1'], [ixChassisIp, '2', '1']]

            rawTrafficVportStyle: This parameter is not useful in RESTpy ang Ignoring this
        """
        if portList is not None:
            createdVportList = []
            self.ixnObj.logInfo('\n Creating Vports for portList {}'.format(portList))
            for i in range(1, len(portList) + 1):
                createdVportList.append(self.ixNetwork.Vport.add())
            if createdVportList == []:
                raise Exception("Unable to create vports")
            return createdVportList
        else:
            raise Exception("Please pass the portlist")

    def getVportObjectByName(self, portName):
        """
        Description:
           Get the vport object by the specified port name.

        Parameter
           portName: <str>: The name of the virtual port.

        Return
           vport object : ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.vport.Vport object
        """

        self.ixnObj.logInfo("getting vport object for portname {}".format(portName))
        vport = self.ixNetwork.Vport.find(Name=portName)
        if vport:
            return vport
        else:
            raise Exception("Unable to find vportObj for portname {}".format(portName))

    def getVportName(self, vportObj):
        """
        Description
           Get the name of the vport by the specified vport object

        Parameter
            vportObj:
            <str>: ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.vport.Vport object

        Return
            vport Name

        Eg :
            Syntax :
                getVportName(vportObj)
            Return : Ethernet - VM - 001
        """
        self.ixnObj.logInfo("getting vport name for vportObj")
        return vportObj.Name

    def linkUpDown(self, port, action='down'):
        """
        Description
            Flap a port up or down.

        Parameters
            port: <list>: A list of ports in a list.
                 [[ixChassisIp, str(card), str(port)]] -> ['10.10.10.1', '1', '3']
            action: <str>: up|down
        """

        action = action.lower()
        self.ixnObj.logInfo("Link {} operation for ports {}".format(action, port))
        for eachPort in port:
            self.ixnObj.logInfo("\n Make port {} to {} state".format(":".join(eachPort), action))
            vport = self.ixNetwork.Vport.find(AssignedTo=":".join(eachPort))
            if vport:
                vport.LinkUpDn(action)

    def getAllVportList(self):
        """
        Description
            Returns a list of all the created virtual ports

        Returns
            List of vport Objects:
        [<ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.vport.Vport object at 0x04FB0E18>,
        <ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.vport.Vport object at 0x04FB0F80>]
        """
        self.ixnObj.logInfo("Get vports for all ports")
        vportList = self.ixNetwork.Vport.find()
        if not vportList:
            raise Exception("vport list is empty hence failing")
        return vportList

    def getVports(self, portList):
        """
        Description
            Get the vports for the portList

        Parameter
            portList: <list>: A list of ports in a list:
            [[str(chassisIp), str(slotNumber), str(portNumber)]]
                      Example 1: [[ixChassisIp, '1', '1']]
                      Example 2: [[ixChassisIp, '1', '1'], [ixChassisIp, '2', '1']]

        Returns
             Vports Objects in a list:
        [<ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.vport.Vport object at 0x04FB0E18>,
         <ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.vport.Vport object at 0x04FB0F80>]
        """
        vportList = []

        self.ixnObj.logInfo("get vport objects for portList {}".format(portList))
        for vport in self.ixnObj.ixNetwork.Vport.find():
            assignedTo = vport.AssignedTo
            if assignedTo == '':
                continue

            chassisIp = assignedTo.split(':')[0]
            cardNum = assignedTo.split(':')[1]
            portNum = assignedTo.split(':')[2]
            port = [chassisIp, cardNum, portNum]
            if port in portList:
                vportList.append(vport)
        return vportList

    def getPhysicalPortsFromCreatedVports(self):
        """
        Description
            Get all the ports that are configured.

        Return
            None or a list of ports in format:
                [['192.168.70.11', '1', '1'], ['192.168.70.11', '2', '1']]
        """
        self.ixnObj.logInfo("get physical port details from all vport objects ")
        portList = []
        for vport in self.ixnObj.ixNetwork.Vport.find():
            assignedTo = vport.AssignedTo
            if assignedTo == '':
                continue

            chassisIp = assignedTo.split(':')[0]
            cardNum = assignedTo.split(':')[1]
            portNum = assignedTo.split(':')[2]
            port = [chassisIp, cardNum, portNum]
            portList.append(port)

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

        self.ixnObj.logInfo("get physical port details from particular vport objects ")

        portList = []
        for vport in vportList:
            port = vport.AssignedTo
            if port:
                portList.append(port)
        return portList

    def verifyPortConnectionStatus(self, vport=None):
        """
        Description
           Verify port connection status for errors such as License Failed,
           Version Mismatch, Incompatible IxOS version, or any other error.
        """
        self.ixnObj.logInfo('verifyPortConnectionStatus raise exception if any port is not '
                            'connected to')
        if vport:
            if 'Port Released' in vport.ConnectionStatus:
                raise Exception(vport.ConnectionStatus)
        else:
            for vport in self.ixNetwork.Vport.find():
                if 'Port Released' in vport.ConnectionStatus:
                    raise Exception(vport.ConnectionStatus)

    def assignPorts(self, portList, forceTakePortOwnership=True, createVports=False,
                    rawTraffic=False, configPortName=True, timeout=900):
        """
        Description
            Assuming that you already connected to an ixia chassis and ports are available for
            usage. Use this API to assign physical ports to the virtual ports.

        Parameters
            portList: <list>: A list of ports in a list:
                 [ [ixChassisIp, '1','1'], [ixChassisIp, '1','2'] ]
            forceTakePortOwnership: <bool>: True = Forcefully take ownership of portList.

            createVports: <bool>: Optional:
                          If True: Create vports to the amount of portList.
                          If False: Automatically create vport on the server side.
                                    Optimized for port bootup performance.

            rawTraffic: <bool>:  Ignored in Restpy
            timeout: <int>: Ignored in Restpy
            configPortName : <bool>: Optional:
                          If True: Configure vportname based on card and port Id.
                          If False: Default vportname

        """
        if createVports:
            self.createVports(portList)
        testPorts = []
        vportList = [vport for vport in self.ixNetwork.Vport.find()]
        for port in portList:
            testPorts.append(dict(Arg1=port[0], Arg2=port[1], Arg3=port[2]))
        self.ixnObj.logInfo('\nAssignPorts: {0}'.format(portList))

        try:
            self.ixNetwork.AssignPorts(testPorts, [], vportList, forceTakePortOwnership)
        except Exception as err:
            self.ixnObj.logInfo('Errored : \n {}'.format(err))
            raise Exception("Failed to Assign ports {} ".format(portList))

        if configPortName:
            # Name the vports
            for vportObj in self.ixNetwork.Vport.find():
                port = vportObj.AssignedTo
                card = port.split(':')[1]
                port = port.split(':')[2]
                vportObj.Name = 'Port' + card + '_' + port
        if rawTraffic:
            vportProtocolList = []
            for vport in self.getAllVportList():
                vportProtocolList.append(vport.Protocols.find())
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
        """

        self.ixnObj.logInfo('Unassign all ports')
        for vport in self.ixNetwork.Vport.find():
            vport.UnassignPorts(Arg2=deleteVirtualPorts)

    def releaseAllPorts(self):
        """
        Description
            Release all the connected ports.
        """
        self.ixnObj.logInfo('Release all ports from configuration')
        for vport in self.ixNetwork.Vport.find():
            vport.ReleasePort()

    def releasePorts(self, portList):
        """
        Description
            Release the specified ports in a list.

        Parameter
            portList: <list>: A list of ports in a list, to release in format of...
                      [[ixChassisIp, str(cardNum), str(portNum)], [], [] ...]
        """
        self.ixnObj.logInfo('Release selected ports {} from configuration'.format(portList))
        vportList = self.getVports(portList)
        for vport in vportList:
            vport.ReleasePort()

    def resetPortCpu(self, vportList=None, portList=None, timeout=90):
        """
        Description
            Reset/Reboot ports CPU.
            Must call IxNetRestApi.py waitForComplete() afterwards to verify port state

        Parameter
            vportList: <list>: A list of one or more vports to reset.
        """

        self.ixnObj.logInfo('Reset all / selected ports from configuration')
        if vportList is None:
            vportList = self.getVportFromPortList(portList)

        for vport in vportList:
            vport.ResetPortCpu()

    def clearPortOwnership(self, portList):
        """
            Description
                Clear port ownership on the portList

            Parameters
                portList: <list>: A list of ports in a list: [[chassisIp, cardId, portId]]
        """
        self.ixnObj.logInfo('Clear port ownership for ports {}'.format(portList))
        for port in portList:
            ixChassisIp = port[0]
            cardId = port[1]
            portId = port[2]
            for chassisObj in self.ixNetwork.AvailableHardware.Chassis.find(Hostname=ixChassisIp):
                for cardObj in chassisObj.Card.find(CardId=cardId):
                    portObj = cardObj.Port.find(PortId=portId)
                    if portObj:
                        portObj.ClearOwnership()

    def isPortConnected(self, portList):
        """
        Description
            Verify if the port is connected or released

        Parameters
            portList: <list>: A list of ports in a list:
                        [[ixChassisIp, str(cardNumber), str(portNumber)]]

        Return
            A list of 'connected' and 'released'.
        """
        self.ixnObj.logInfo('Verify {} is connected or released '.format(portList))
        returnValues = []
        for port in portList:
            vport = self.getVports([port])
            if vport == []:
                returnValues.append('released')
                continue

            if 'Port Released' in vport.ConnectionStatus:
                returnValues.append('released')
            else:
                returnValues.append('connected')
        return returnValues

    def verifyForDuplicatePorts(self, portList):
        """
        Description
           Verify if the portList has any duplicate ports.
           Raise an exception if true.
        """
        duplicatePorts = [port for numberOfPorts, port in enumerate(portList) if port in
                          portList[:numberOfPorts]]
        if duplicatePorts:
            raise IxNetRestApiException('\nYour portList has duplicate ports {0}'.
                                        format(duplicatePorts))

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
            ixChassisIp = port[0]
            cardId = port[1]
            portId = port[2]
            for chassisObj in self.ixNetwork.AvailableHardware.Chassis.find(Hostname=ixChassisIp):
                for cardObj in chassisObj.Card.find(CardId=cardId):
                    portObj = cardObj.Port.find(PortId=portId)
                    if portObj:
                        if portObj.Owner != '':
                            self.ixnObj.logInfo(
                                '{0} is currently owned by: {1}'.format(port, portObj.Owner))
                            portOwnedList.append([ixChassisIp, cardId, portId])

        if portOwnedList != []:
            if raiseException:
                raise Exception('arePortsAvailable: Ports are still owned')
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

        vportList = [vport for vport in self.ixNetwork.Vport.find()]
        for vport in vportList:
            for counter in range(1, timeout + 1):
                if 'Port Released' in vport.ConnectionStatus:
                    raise Exception(vport.ConnectionStatus)
                if not vport.IsConnected:
                    self.ixnObj.logWarning('\nThe vport {0} is not assigned to a physical port. '
                                           'Skipping this vport verification.'.format(vport.href))
                    break
                if vport.ConnectionState in ['down', 'connecting']:
                    time.sleep(1)
                    continue
                if vport.ConnectionState in ['up', 'connectedLinkUp']:
                    break
                if counter == timeout and vport.ConnectionState in ['assignedInUseByOther',
                                                                    'assignedUnconnected',
                                                                    'connectedLinkDown']:
                    # Failed
                    raise IxNetRestApiException('Port failed to come up')

    def getVportFromPortList(self, portList):
        """
        Description
           Get a list of vports from the specified portList.

        Parameter
           portList: <list>: Format: [[ixChassisIp, cardNumber1, portNumber1],
                                      [ixChassisIp, cardNumber1, portNumber2]]

        Return
           A list of vports.
           [] if vportList is empty.
        """
        regexString = ''
        for port in portList:
            # Construct the regex string format = '(1.1.1.1:2:3)|(1.1.1.1:6:2)'
            regexString = \
                regexString + '(' + str(port[0]) + ':' + str(port[1]) + ':' + str(port[2]) + ')'
            if port != portList[-1]:
                regexString = regexString + '|'
        vports = [vport for vport in self.ixNetwork.Vport.find(AssignedTo=regexString)]
        if not vports:
            raise Exception("unable to find vports for ports {} ".format(portList))
        return vports

    def modifyPortMediaType(self, portList='all', mediaType='fiber'):
        """
        Description
           Modify the port media type: fiber, copper, SGMII

        Parameters
           portList: <'all'|list of ports>:
                     <list>: Format: [[ixChassisIp, str(cardNumber1), str(portNumber1])]...]
                     Or if portList ='all',
                                    will modify all assigned ports to the specified mediaType.

           mediaType: <str>: copper, fiber or SGMII
        """
        self.ixnObj.logInfo('modifyPortMediaType: {0}'.format(mediaType))
        if portList == 'all':
            vportList = self.getAllVportList()
        else:
            vportList = self.getVports(portList)

        for vport in vportList:
            cardType = vport.Type
            cardType = cardType[0].upper() + cardType[1:]
            cardObj = getattr(vport.L1Config, cardType)
            cardObj.Media = mediaType

    def modifyL1Config(self, configSettings, portList='all'):
        """
        Description
           Modify Layer 1 Configuration

        Parameters
           portList: <'all'|list of ports>:
                     <list>: Format: [[ixChassisIp, str(cardNumber1), str(portNumber1])]...]
                     Or if portList ='all', will modify all assigned ports to the specified
                                            configSettings.
                     Note:  all ports must be of the same type

           configSettings: <dict>: L1 Settings. The actual settings depend on the card type.
                           example for novusHundredGigLan card:
                           configSettings ={'enabledFlowControl': True,
                                            'flowControlDirectedAddress': '01 80 C2 00 00 00 CC',
                                            'txIgnoreRxLinkFaults': False,
                                            'laserOn': True,
                                            'ieeeL1Defaults': False,
                                            'enableAutoNegotiation': False,
                                            'linkTraining': False,
                                            'firecodeAdvertise': False,
                                            'firecodeRequest': False,
                                            'rsFecAdvertise': False,
                                            'rsFecRequest': False,
                                            'useANResults': False,
                                            'firecodeForceOn': True,
                                            'rsFecForceOn': False,
                                            'forceDisableFEC': False}
        """
        self.ixnObj.logInfo(
            'modifyL1Config: portList = {} configSettings = {}'.format(portList, configSettings))

        if portList == 'all':
            vportList = self.getAllVportList()
        else:
            vportList = self.getVports(portList)

        for vport in vportList:
            cardType = vport.Type
            cardType = cardType[0].upper() + cardType[1:]
            obj = getattr(vport.L1Config, cardType)
            for key, value in configSettings.items():
                key = key[0].upper() + key[1:]
                try:
                    setattr(obj, key, value)
                except Exception as err:
                    self.ixnObj.logInfo('Errored : \n {}'.format(err))
                    raise Exception("Failed setting value {} for {} in L1config".format(value, key))

    def configLoopbackPort(self, portList='all', enabled=True):
        """
        Description
           Configure port to loopback.

        Parameters
           portList: <'all'|list of ports>:
                     <list>: Format: [[ixChassisIp, str(cardNumber1), str(portNumber1])]...]
                     Or if portList ='all', will modify all assigned ports to the specified
                                            mediaType.

           enabled: <bool>: True=Enable port to loopback mode.
        """
        if portList == 'all':
            vportList = self.getAllVportList()
        else:
            vportList = self.getVports(portList)

        for vport in vportList:
            cardType = vport.Type
            cardType = cardType[0].upper() + cardType[1:]
            cardObj = getattr(vport.L1Config, cardType)
            cardObj.Loopback = enabled

    def setTxMode(self, vportList='all', txMode='interleaved', timeout=70):
        """
        Description
           set TxMode of the vports

        Parameter
           vportList: <list>: vports to set the transmitMode on.  Default = all
           txMode:    <str>: transmit mode setting -  can be either 'interleaved' or 'sequential'
           timeout:   <int>: the timeout value to declare as failed. Default=70 seconds.

        """
        if vportList == 'all':
            vportList = self.getAllVportList()
        for eachVport in vportList:
            eachVport.TxMode = txMode

    def configUdsRxFilters(self, portList='all', filterPalette=None, udsNum='1', udsArgs=None):
        """
        Description
           Configure rxFilters and User Defined Stats on a port

        Parameters
           portList: <'all'|list of ports>:
                     <list>: Format: [[ixChassisIp, str(cardNumber1), str(portNumber1])]...]
                     Or if portList ='all', will modify all assigned ports to the specified
                                            mediaType.

           filterPalette: Filter Palette kwargs.
           udsNum: <string>:  uds number
           udsArgs: uds kwargs.

        USAGE EXAMPLE:
           portMgmtObj.configUdsRxFilters(portList=[['10.113.9.219', '6', '1']],
                                          filterPalette={'pattern1':'01', 'pattern1Mask':'FC',
                                                         'pattern1Offset':'15',
                                                         'pattern1OffsetType':'fromStartOfFrame',
                                          udsNum=1
                                          udsArgs={'isEnabled':'true',
                                                    'patternSelector':'pattern1'})

           portMgmtObj.configUdsRxFilters(portList=[['10.113.9.219', '6', '1']],
                                          filterPalette={'pattern2':'03', 'pattern2Mask':'FC',
                                                         'pattern2Offset':'19',
                                                         'pattern2OffsetType':'fromStartOfFrame',
                                          udsNum=2
                                          udsArgs={'isEnabled':'true',
                                                    'patternSelector':'pattern2'})

        """
        self.ixnObj.logInfo('configUdsRxFilters: filterPalette={0}'.format(filterPalette))
        self.ixnObj.logInfo('\t\t uds={0} udsArgs={1}'.format(udsNum, udsArgs))
        if portList == 'all':
            vportList = self.getAllVportList()
        else:
            vportList = self.getVports(portList)

        for vport in vportList:
            filterObj = vport.L1Config.RxFilters.FilterPalette
            for key, value in filterPalette.items():
                key = key[0].upper() + key[1:]
                try:
                    setattr(filterObj, key, value)
                except Exception as err:
                    self.ixnObj.logInfo('Errored : \n {}'.format(err))
                    raise Exception(
                        "Failed setting value {} for {} in filterpallete ".format(value, key))

            for udsObj in vport.L1Config.RxFilters.Uds.find():
                if udsNum == udsObj.href.split("/")[-1]:
                    for key, value in udsArgs.items():
                        key = key[0].upper() + key[1:]
                        try:
                            setattr(udsObj, key, value)
                        except Exception as err:
                            self.ixnObj.logInfo('Errored : \n {}'.format(err))
                            raise Exception(
                                "Failed setting value {} for {} in uds".format(value, key))
