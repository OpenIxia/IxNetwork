
# PLEASE READ DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# REQUIREMENTS
#    - Python 2.7.11 or Python 3+
#    - request.py module
#    - readline.py module
#
# DESCRIPTION
#    This script assumes that you already imported ixVM chassis
#    and ixVM line cards on either a VMWare ESX Host or KVM Host.
#
#    This script will add or remove vChassis and vLMs on a specified
#    IxNetwork API server using ReST APIs.
#    This script operates in two modes:
#       1> Interactive mode: Will ask you all the necessary questions to add
#          the vChassis and vLMs on your IxNetwork API server.
#
#       2> Non-Interactive mode: Will not ask you any questions. 
#          Requires you to fill out the ixvmParams.py file.
#
#    NOTE:
#       For adding: This script will check for residual hypervisors and cards.
#                   Remove all before adding. Otherwise, adding new cardID will fail.
#
# USAGE
#
#     Non-Interactive mode: This script will read all the parameters/values from ixvmParams.py and do it.
#                           You must have the ixvmParams.py file in the same path as ixVmChassisBuilder.py
#         Enter: python ixVmChassisBuilder.py add|remove
#
#     Interactive mode: Ask questions. 
#         Enter: python ixVmChassisBuilder.py
#
# Version 2: Automate adding interfaces through VMWare and Openstack using APIs.

from __future__ import absolute_import, print_function
import os, sys, re, requests, json, time, traceback, platform, readline
from requests.exceptions import ConnectionError
from requests.packages.urllib3.connection import HTTPConnection

class IxNetRestApiException(Exception): pass

class IxVmChassisBuilder(object):
    def __init__(self, serverIp=None, serverPort=None):
        self.sessionUrl = None
        self.sessionId = None
        self.httpHeader = None
        self.jsonHeader = {"content-type": "application/json"}
        self.getSessionUrl(serverIp, serverPort)

    def get(self, restApi, data={}, stream=False, silentMode=False, ignoreError=False):
        """
        Description
           A HTTP GET function to send REST APIs.
        
        Parameters
           restApi: The REST API URL.
           data: The data payload for the URL.
           silentMode: True or False.  To display URL, data and header info.
           ignoreError: True or False.  If False, the response will be returned.
        """
        if silentMode is False:
            print('\nGET:', restApi)
            print('HEADERS:', self.jsonHeader)

        try:
            response = requests.get(restApi, headers=self.jsonHeader)

            if silentMode is False:
                print('STATUS CODE:', response.status_code)
            if not re.match('2[0-9][0-9]', str(response.status_code)):
                if ignoreError == False:
                    raise IxNetRestApiException('http GET error:{0}\n'.format(response.text))
            return response

        except requests.exceptions.RequestException as errMsg:
            raise IxNetRestApiException('http GET error: {0}\n'.format(errMsg))

    def post(self, restApi, data={}, headers=None, silentMode=False, ignoreError=False):
        """
        Description
           A HTTP POST function to mainly used to create or start operations.
        
        Parameters
           restApi: The REST API URL.
           data: The data payload for the URL.
           headers: The special header to use for the URL.
           silentMode: True or False.  To display URL, data and header info.
           noDataJsonDumps: True or False. If True, use json dumps. Else, accept the data as-is. 
           ignoreError: True or False.  If False, the response will be returned. No exception will be raised.
        """

        if headers != None:
            originalJsonHeader = self.jsonHeader
            self.jsonHeader = headers

        data = json.dumps(data)

        print('\nPOST:', restApi)
        if silentMode == False:
            print('DATA:', data)
            print('HEADERS:', self.jsonHeader)

        try:
            response = requests.post(restApi, data=data, headers=self.jsonHeader)
            # 200 or 201
            if silentMode == False:
                print('STATUS CODE:', response.status_code)
            if not re.match('2[0-9][0-9]', str(response.status_code)):
                if ignoreError == False:
                    raise IxNetRestApiException('http POST error: {0}\n'.format(response.text))

            return response
        except requests.exceptions.RequestException as errMsg:
            raise IxNetRestApiException('http POST error: {0}\n'.format(errMsg))

    def patch(self, restApi, data={}, silentMode=False):
        """
        Description
           A HTTP PATCH function to modify configurations.
        
        Parameters
           restApi: The REST API URL.
           data: The data payload for the URL.
           silentMode: True or False.  To display URL, data and header info.
        """

        if silentMode == False:
            print('\nPATCH:', restApi)
            print('DATA:', data)
            print('HEADERS:', self.jsonHeader)
        try:
            response = requests.patch(restApi, data=json.dumps(data), headers=self.jsonHeader)
            if silentMode == False:
                print('STATUS CODE:', response.status_code)
            if not re.match('2[0-9][0-9]', str(response.status_code)):
                print('\nPatch error:')
                raise IxNetRestApiException('http PATCH error: {0}\n'.format(response.text))
            return response
        except requests.exceptions.RequestException as errMsg:
            raise IxNetRestApiException('http PATCH error: {0}\n'.format(errMsg))

    def delete(self, restApi, data={}, headers=None):
        """
        Description
           A HTTP DELETE function to delete the session.
           For Linux API server only.
        
        Parameters
           restApi: The REST API URL.
           data: The data payload for the URL.
           headers: The header to use for the URL.
        """

        if headers != None:
            self.jsonHeader = headers

        print('\nDELETE:', restApi)
        print('DATA:', data)
        print('HEADERS:', self.jsonHeader)
        try:
            response = requests.delete(restApi, data=json.dumps(data), headers=self.jsonHeader)
            print('STATUS CODE:', response.status_code)
            if not re.match('2[0-9][0-9]', str(response.status_code)):
                raise IxNetRestApiException('http DELETE error: {0}\n'.format(response.text))
            return response
        except requests.exceptions.RequestException as errMsg:
            raise IxNetRestApiException('http DELETE error: {0}\n'.format(errMsg))

    def getSessionUrl(self, ixNetRestServerIp, ixNetRestServerPort=11009):
        """
        Description
            Connect to a Windows IxNetwork API Server to create a session URL.
            http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork
        
         ixNetRestServerIp: The IxNetwork API Server IP address.
         ixNetRestServerPort: Provide a port number to connect to your non Linux API Server.
                              On a Linux API Server, a socket port is not needed. State "None".
        """
        url = 'http://{0}:{1}/api/v1/sessions'.format(ixNetRestServerIp, ixNetRestServerPort)
        serverAndPort = ixNetRestServerIp+':'+str(ixNetRestServerPort)
        response = self.get(url)
        sessionId = response.json()[0]['id']
        self.sessionUrl = 'http://{apiServer}:{port}/api/v1/sessions/{id}/ixnetwork'.format(apiServer=ixNetRestServerIp, 
                                                                                            port=ixNetRestServerPort,
                                                                                            id=sessionId)
        # http://192.168.70.127:11009
        self.httpHeader = self.sessionUrl.split('/api')[0]
        # http://192.168.70.127:11009/api/v1/sessions/1
        self.sessionId = self.sessionUrl.split('/ixnetwork')[0]
        return self.sessionUrl

    def showErrorMessage(self):
        """
        Description
            Show all the error messages from IxNetwork.

        Syntax
            GET: http://{apiServerIp:11009}/api/v1/sessions/{id}/globals/appErrors/error
        """
        errorList = []
        print('\nShowErrorMessages:')
        response = self.get(self.sessionUrl+'/globals/appErrors/error')
        for errorId in response.json():
            if errorId['errorLevel'] in ['Error', 'kWarning']:
                print('%s: MessageType: %s\n\t%s' % (errorId['lastModified'], errorId['errorLevel'], errorId['description']))
                errorList.append(errorId['description'])
            print()

    def ixVmCreateHypervisor(self, enabled='true', serverIp='', 
                             hypervisorType='vmware', userLoginName='admin', userPassword='admin'):
        """
        Description
            Create a hypervisor.

        Syntax
            http://{apiServerIp:11009}/api/v1/sessions/1/ixnetwork/availableHardware/virtualChassis

        Parameters
           enabled: true or false.
           serverIp: The vChassis IP address.
           hypervisorType:  vmware or qemu.
           userLoginName: Default = admin
           userPassword:  Default = admin
        """
        vChassisObj = self.sessionUrl+'/availableHardware/virtualChassis'
        url = self.sessionUrl+'/availableHardware/virtualChassis/hypervisor'
        data = {'enabled': enabled, 
                'serverIp': serverIp,
                'type': hypervisorType,
                'user': userLoginName,
                'password': userPassword
            }
        response = self.post(url, data=data, ignoreError=True)
        if response.status_code != 201:
            errorMsg = response.json()['errors'][0]['detail']
            if errorMsg == 'Hypervisor already added.':
                response = self.get(url)
                existingHypervisor = response.json()[0]['links'][0]['href']
                print('ixVmCreateHypervisor: Hypervisor already added. Returning:', existingHypervisor)
                return existingHypervisor
            else:
                raise IxNetRestApiException('ixVmCreateHypervisor failed:', errorMsg)
        else:
            # http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/availableHardware/virtualChassis/hypervisor/1
            hypervisorObj = response.json()['links'][0]['href']
            return hypervisorObj

    def ixVmAddCardIdPortId(self, cardIdPortIdList):
        """
        Description
           A wrapper API to call ixVmConfigCardId and ixVmConfigPortId.

        Parameter
            cardIdPortIdList: A list of virtual Card and virtual port parameters.

               Example:
               ixvmCardPortList = [{'cardId': 1, 'portId': 1, 'mgmtIp': '192.168.70.12', 'interface': 'eth1',
                                   'promiscuousMode': False, 'mtu': '1500', 'keepAlive': '300', 'portName': 'myPort1'},

                                   {'cardId': 2, 'portId': 1, 'mgmtIp': '192.168.70.13', 'interface': 'eth1',
                                     'promiscuousMode': False, 'mtu': '1500', 'keepAlive': '300', 'portName': 'myPort2'}
                                  ]

        """

        mandatoryCardIdParams = ['mgmtIp']

        for eachList in cardIdPortIdList:
            for eachMandatoryParam in mandatoryCardIdParams:
                if eachMandatoryParam not in eachList:
                    raise IxNetRestApiException('Missing mandatory param for ixVm cardId: {0}\n\n{1}'.format(eachMandatoryParam, eachList))

        autoGenPortNameNumber = 1
        for eachList in cardIdPortIdList:
            # cardId config
            mgmtIp = eachList['mgmtIp']

            if 'cardName' not in eachList:
                cardName = 'card'+str(autoGenPortNameNumber)
            else:
                cardName = eachList['cardName']

            if 'keepAlive' in eachList:
                keepAlive = eachList['keepAlive']
            else:
                keepAlive = '300'

            # portId config
            if 'portName' in eachList:
                portName = eachList['portName']
            else:
                portName = 'port'+str(autoGenPortNameNumber)

            if 'promiscuousMode' in eachList:
                promiscuousMode = eachList['promiscuousMode']
            else:
                promiscuousMode = 'false'

            if 'mtu' in eachList:
                mtu = eachList['mtu']
            else:
                mtu = '1500'

            cardObj = self.ixVmConfigCardId(cardName=cardName, mgmtIp=mgmtIp, keepAlive=keepAlive)
            if cardObj != 1:
                # /api/v1/sessions/1/ixnetwork/availableHardware/virtualChassis/ixVmCard/1
                cardPortObj = self.ixVmConfigPortId(cardObj, portName=portName, promiscuousMode=promiscuousMode, mtu=mtu)
            cardId = cardObj.split('/')[-1]
            self.ixVmConnectCardById(cardId)

        for eachCard in self.ixVmGetListCardId():
            print('\tCreated:', eachCard)

    def ixVmConfigCardId(self, cardName=None, mgmtIp='', keepAlive=300):
        """
        Description
           Add/Configure a virtual line card.

        Syntax
           http://{apiServerIp:11009}/availableHardware/virtualChassis/ixVmCard

        Parameters
           cardId:   The cardId.  Must begin with 1 and in sequential order.
           cardName: Optional: Specify a name for the card.
           mgmtIp:   The virtual line card's management IP address.
           keepAlive: Integer in seconds
        """
        url = self.sessionUrl+'/availableHardware/virtualChassis/ixVmCard'
        nextCardId = self.ixVmGetLastCardId()+1
        data = {"cardId": str(nextCardId),
                "managementIp": str(mgmtIp),
                "keepAliveTimeout": int(keepAlive)
                }
        response = self.post(url, data=data, ignoreError=True)
        if response.status_code == 400:
            print()
            # Another card with IP 192.168.70.130 already exists on slot 1 on the chassis 192.168.70.10.
            # Commit operation failed on /availableHardware/virtualChassis/ixVmCard:L100
            for error in response.json()['errors']:
                print('\t', error['detail'])

            print('\nREMOVING existing cardID:', mgmtIp)
            self.ixVmRemoveCardId(mgmtIp)

            print('\nRETRY creating cardID:', mgmtIp)
            response = self.patch(url, data=data)
            if response.status_code == 400:
                print()
                # Another card with IP 192.168.70.130 already exists on slot 1 on the chassis 192.168.70.10.
                # Commit operation failed on /availableHardware/virtualChassis/ixVmCard:L100
                for error in response.json()['errors']:
                    print('\t', error['detail'])

            #raise IxNetRestApiException
        
        if cardName is not None:
            self.patch(url, data={'cardName': cardName})

        ixVmCardObj = response.json()['links'][0]['href']
        return ixVmCardObj

    def ixVmConfigPortId(self, cardUrl, portName=None, promiscuousMode='false', mtu='1500'):
        """
        Description
            Add/Configure a virtual port to the cardId.
        
        Parameters
            cardUrl:    The cardId object: /api/v1/sessions/1/ixnetwork/availableHardware/virtualChassis/ixVmCard/1
            interface:  eth1|eth2|eth3 ...
            portId:     Optional: The portId. Must begin with 1. Warning! You will have a misconfiguration if you don't begin with ID 1.
            portName:   Optional: Specify the name of the virtual port.
            promiscuousMode: true|false
            mtu:        Optional: The MTU frame size.
        """
        url = self.httpHeader+cardUrl+'/ixVmPort'
        portId = self.ixVmGetLastPortId(cardUrl)
        interface = 'eth'+str(portId)
        data = {'interface': interface,
                'portId': str(portId),
                'promiscMode': str(promiscuousMode),
                'mtu': str(mtu),
                }
        response = self.post(url, data=data)
        # /api/v1/sessions/1/ixnetwork/availableHardware/virtualChassis/ixVmCard/2/ixVmPort/1
        if portName is not None:
            self.patch(url, data={'portName': portName})

        return response.json()['links'][0]['href']

    def ixVmConnectCardById(self, cardId):
        url = self.httpHeader+'/api/v1/sessions/1/ixnetwork/operations/connectcardbyid'
        response = self.post(url, data={'arg1': cardId})
        print('\nconnectCardById:', response.json())
        self.waitForComplete(response, url+'/'+response.json()['id'])

    def ixVmGetListCardId(self):
        url = self.sessionUrl+'/availableHardware/virtualChassis/ixVmCard'
        response = self.get(url)
        cardIdList = []
        if response.status_code == 200:
            cardIdList = [item['links'][0]['href'] for item in response.json()]
            return cardIdList

    def ixVmGetLastCardId(self):
        return len(self.ixVmGetListCardId())

    def ixVmGetLastPortId(self, cardIdObj):
        response = self.get(self.httpHeader+cardIdObj+'/ixVmPort')
        portId = 1
        for eachPortId in response.json():
            portId = eachPortId['portId']
        return portId

    def ixVmClearPortOwnershipByCardId(self, cardId):
        """ 
        Description
           Clear ownership on all virtual ports from the provided IxVM cardId.

        Syntax
            http://{apiServerIp:11009}/api/v1/sessions/1/ixnetwork/operations/clearcardownershipbyid"
            data={'arg1': str(cardId)}

         Returns 0 if success
         Returns 1 if failed
        """
        url = self.sessionUrl+'/operations/clearcardownershipbyid'
        data = {"arg1": str(cardId)}
        response = self.post(url, data=data)
        if response.status_code == 202:
            state = response.json()['state']
            result = response.json()['result']
            # state: SUCCESS, ERROR
            # result: Selected card does not exist
            if state == 'ERROR' and result == 'Selected card does not exist':
                return 0 ;# Good
            if state == 'ERROR' and result != 'Selected card does not exist':
                return 1
            if state == 'SUCCESS':
                return 0
        else:
            return 1

    def ixVmRemoveCardId(self, managementIp):
        """
        Description
           Remove individual virtual line cards.
           1> Clear port ownership
           2> Remove cardId

        Syntax
           http://{apiServerIp:11009}/api/v1/sessions/1/ixnetwork/availableHardware/virtualChassis/ixVmCard/1

        Parameter
           managementIp: The IP address of the IxVM card.
        
        """
        response = self.get(self.sessionUrl+'/availableHardware/virtualChassis/ixVmCard')
        for eachVmCard in response.json():
            if eachVmCard['managementIp'] == managementIp:
                url = eachVmCard['links'][0]['href']
                cardIdNumber = eachVmCard['cardId']
                self.ixVmClearPortOwnershipByCardId(cardIdNumber)
                print('\nixVmRemoveCardId:', managementIp)
                self.delete(self.httpHeader+url)

    def ixVmRemoveAllCardId(self):
        """
        Description
            1> Clear port ownership
            2> Disconnect each card IDs.
            3> Remove the card IDs.

        Syntax
            To get a list of all virtual line cards:
                http://{apiServerIp:11009/availableHardware/virtualChassis/ixVmCard

            To disconnect virtual line cards:
                http://{apiServerIp:11009/operations/disconnectcardbyid 
                data={'arg1': str(cardId)}
        """
        url = self.sessionUrl+'/availableHardware/virtualChassis/ixVmCard'
        response = self.get(url)
        cardIdList = [item['links'][0]['href'] for item in response.json()]
        for eachCard in cardIdList:
            # /api/v1/sessions/1/ixnetwork/availableHardware/virtualChassis/ixVmCard/5        
            response = self.get(self.httpHeader+eachCard)
            print('\nixVmRemoveAllCardIds response:', response.json())
            if response.status_code == 200:
                cardIdNumber = response.json()['cardId']
                # Must clear port ownership first. This will disconnect the card/port
                self.ixVmClearPortOwnershipByCardId(cardIdNumber)

                print('Disconnecting cardId:', cardIdNumber)
                disconnectUrl = self.sessionUrl+'/operations/disconnectcardbyid'
                data = {"arg1": str(cardIdNumber)}
                response = self.post(disconnectUrl, data=data)
                if self.waitForComplete(response, disconnectUrl+'/'+response.json()['id']) == 1:
                    raise IxNetRestApiException

            response = self.delete(self.httpHeader+eachCard)

        existingCardList = self.ixVmGetListCardId()
        if len(existingCardList) > 0:
            for eachCard in existingCardList:
                IxNetRestApiException('\tCard still exist:', eachCard)

    def ixVmDeleteHypervisor(self, serverIp='all'):
        response = self.get(self.sessionUrl+'/availableHardware/virtualChassis/hypervisor')
        for hypervisor in response.json():
            currentHrefObject = hypervisor['links'][0]['href']
            currentServerIp = hypervisor['serverIp']
            print('\nixVmDeleteHypervisor: discovered:', currentServerIp)
            print('ixVmDeleteHypervisor hrefObject:', currentHrefObject)
            if serverIp == 'all':
                self.delete(self.httpHeader+currentHrefObject)
            if serverIp == currentServerIp:
                self.delete(self.httpHeader+currentHrefObject)

    def ixVmDeleteVirtualChassis(self, vChassisIp):
        """
        Description
           Delete the virtual chassis.

        Syntax
            http://{apiServerIp:11009}/api/v1/sessions/1/ixnetwork/availableHardware/virtualChassis/hypervisor/1

        Parameter
           vChassisIp: 'all' or the virtual chassis IP.
        """
        response = self.get(self.sessionUrl+'/availableHardware/virtualChassis/hypervisor')
        for eachHypervisor in response.json():
            if vChassisIp == 'all':
                response = self.get(self.httpHeader+eachHypervisor['links'][0]['href'])
                print('\nixVmDeleteVirtualChassis response:', response.json())
                self.delete(self.httpHeader+eachHypervisor['links'][0]['href'])

            if eachHypervisor['serverIp'] == vChassisIp:
                self.delete(self.httpHeader+eachHypervisor['links'][0]['href'])

    def removeAllSuper(self):
        print('\n-------- Before adding: Removing all residual hypervisors and cards ---------')
        self.ixVmRemoveAllCardId()
        self.ixVmDeleteHypervisor(serverIp='all')
        self.ixVmDeleteVirtualChassis('all')
        print('\n------------ Removing all residual hypervisors and cards done ---------')

    def connectIxChassis(self, chassisIp):
        """
        Description
           Connect to chassis.
           This needs to be done prior to assigning ports for testing.

        Syntax
           /api/v1/sessions/1/ixnetwork/availableHardware/chassis

        Parameter
           chassisIp: The chassis IP address.
        """ 
        url = self.sessionUrl+'/availableHardware/chassis'
        data = {'hostname': chassisIp}
        response = self.post(url, data=data)

        # /api/v1/sessions/1/ixnetwork/availableHardware/chassis/1
        chassisIdObj = response.json()['links'][0]['href']
        # Chassis states: down, polling, ready
        for timer in range(1,11):
            response = self.get(self.httpHeader + chassisIdObj, silentMode=True)
            currentStatus = response.json()['state']
            print('connectIxChassis {0}: Status: {1}'.format(chassisIp, currentStatus))
            if currentStatus != 'ready' and timer < 10:
                time.sleep(1)
            if currentStatus != 'ready' and timer == 10:
                raise IxNetRestApiException('connectIxChassis: Connecting to chassis {0} failed'.format(chassisIp))
            if currentStatus == 'ready' and timer < 10:
                break

        return chassisIdObj

    def connectToVChassis(self, chassisIp):
        self.connectIxChassis(chassisIp)

        # Connects to the virtual chassis
        url = self.sessionUrl+'/operations/connecttochassis'
        data = {"arg1": chassisIp}
        response = self.post(url, data=data)
        if self.waitForComplete(response, url+'/'+response.json()['id']) == 1:
            raise IxNetRestApiException

    def disconnectIxChassis(self, chassisIp):
        """
        Description
            Disconnect the chassis (both hardware or virtualChassis).

        Syntax
            http://{apiServerIp:11009}/api/v1/sessions/1/ixnetwork/availableHardware/chassis/<id>

        Parameter
            chassisIp: 'all' or the chassis IP address.
        """
        url = self.sessionUrl+'/availableHardware/chassis'
        response = self.get(url)
        for eachChassisId in response.json():
            if chassisIp == 'all':
                chassisIdUrl = eachChassisId['links'][0]['href']
                response = self.get(self.httpHeader+chassisIdUrl)
                print('\ndisconnectIxChassis all:', chassisIdUrl)
                print('\tIP address:', response.json()['ip'])
                response = self.delete(self.httpHeader+chassisIdUrl)
                
            if eachChassisId['hostname'] == chassisIp:
                chassisIdUrl = eachChassisId['links'][0]['href']
                print('\ndisconnectIxChassis', chassisIdUrl)
                print('\tIP address:', response.json()['ip'])
                response = self.delete(self.httpHeader+chassisIdUrl)

    def refreshHardware(self, chassisObj):
        """
        Description
            Refresh the chassis

        Syntax
            http://{apiServerIp:11009}/availableHardware/chassis/operations/refreshinfo

        Parameter
            chassisObj:  The chassis object
                         Ex: '/api/v1/sessions/1/ixnetwork/availableHardware/chassis/1'
        """
        response = self.post(self.sessionUrl+'/availableHardware/chassis/operations/refreshinfo', data={'arg1': [chassisObj]})
        if self.waitForComplete(response, self.sessionUrl+'/availableHardware/chassis/operations/refreshinfo') == 1:
            raise IxNetRestApiException

    def ixVmRediscoverAppliances(self):
        """
        Description
            Assuming that the virtual load module appliances (VM) are already created.
            Now you want to add them. This is step 1 of 2.
            Next step is to add them as useable ports.

        Returns
            Returns XML data format
        """
        url = self.sessionUrl+'/operations/rediscoverappliances'
        response = self.post(url)
        # XML format
        print('\n-- rediscover:', response.json())
        if self.waitForComplete(response, url+'/'+response.json()['id']) == 1:
            raise IxNetRestApiException

    def ixVmRebuildChassisTopology(self, ixNetworkVersion):
        """
        Description
            Remove all connected IxVM CardId/PortIds

        Parameter
            ixNetworkVersion: The version of IxNetwork.  Ex: 8.20

        Syntax
            POST: http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/operations/rebuildchassistopology
            arg1: IxNetwork version that should be used to filter appliances.
            arg2: Flag that enables reconfiguration on the same slots for the previous cards. (true|false)
            arg3: Promiscuous Mode (true|false)
        """
        url = self.sessionUrl+'/operations/rebuildchassistopology'
        data = {"arg1": str(ixNetworkVersion), "arg2": "false", "arg3": "false"}
        response = self.post(url, data=data)
        if self.waitForComplete(response, url+'/'+response.json()['id']) == 1:
            raise IxNetRestApiException
            # Returns a list of discovered machines in XML format.

    def waitForComplete(self, response='', url='',  silentMode=True, timeout=90):
        """
        Description
            Wait for an operation progress to complete.
        
        Parameters
            response: The POST action response.  Generally, after an /operations action.
                      Such as /operations/startallprotocols, /operations/assignports
            silentMode: True or False. If True, display info messages.
            timeout: The time allowed to wait for success completion in seconds.
        """
        print ('\nwaitForComplete...')
        if response.json() == []:
            raise IxNetRestApiException('waitForComplete: response is empty.')
        if 'errors' in response.json():
            print(response.json()["errors"][0])
            return 1
        print("\tState:",response.json()["state"])
        if response.json()['state'] == "SUCCESS":
            return 0
        if response.json()['state'] == "ERROR":
            self.showErrorMessage()
            return 1
        if response.json()['state'] == "EXCEPTION":
            print(response.text)
            return 1

        while True:
            if response.json()["state"] == "IN_PROGRESS" or response.json()["state"] == "down":
                if timeout == 0:
                    return 1
                time.sleep(1)
                response = self.get(url, silentMode=silentMode)
                state = response.json()["state"]
                if timeout > 0 and state == 'SUCCESS':
                    print("\tState: {0}".format(state))
                    break
                elif timeout > 0 and state == 'ERROR':
                    self.showErrorMessage()
                    return 1
                elif timeout > 0 and state == 'EXCEPTION':
                    print(response.text)
                    return 1
                elif timeout == 0 and state != 'SUCCESS':
                    return 1
                else:
                    print("\tState: {0} {1} seconds remaining".format(state, timeout))
                    timeout = timeout-1
                    continue

def completer(text, state):
    options = [x for x in commands if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None

def getInput(question):
    if platform.python_version().startswith('3'):
        userInput = input('%s ' % question)
    if platform.python_version().startswith('2'):
        userInput = raw_input('%s ' % question)

    return userInput

def askQuestion(question, defaultValue=None, expectedPattern=None):
    # This Method makes the script bomb proof.
    # It expects a correct value pattern and it will continue to ask you the
    # same question if you did not answer correctly.

    while True:
        response = getInput('\n'+question)
        # If there is no default value and no user response, ask again.
        # Expecting a value.
        if not response and defaultValue == None:
            continue
        if response and expectedPattern and bool(re.match(expectedPattern, response, re.I)) == False:
            print('\n\tError: You entered:', response)
            print('\tError: Expecting pattern:', expectedPattern)
            continue
        # User responded. Expecting a certain pattern and if ok, return the user input.
        if response and expectedPattern and bool(re.match(expectedPattern, response, re.I)) == True:
            return response
        # User responded. Any input is ok. No verification required.
        if response and expectedPattern == None:
            return response
        # No response and no default value, ask again
        if not response and defaultValue == None:            
            continue
        # No resposne, return the default value as the value.
        if not response and defaultValue:
            return defaultValue

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

vmMgmtCardListToRemove = 'all' 

#apiServerIp = '192.168.70.127'
#apiServerIpPort = '11009'
#restObj = IxVmChassisBuilder(serverIp=apiServerIp, serverPort=apiServerIpPort)
#restObj.ixVmDeleteHypervisor()
#sys.exit()

if len(sys.argv) == 1:
    # Ask questions. Not reading ixvmParams.py file.
    #    python ixvmChassisBuilder.py
    #ixvmCardPortList = 'interactive'
    mode = 'interactive'

if len(sys.argv) > 1:
    # Read the ixvnParams.py file
    #    python ixvmChassisBuilder.py add|remove
    if os.path.exists('ixvmParams.py') == False:
        errMsg = '\nError: For non-interactive mode, you must have the ixvmParams.py file on the same path as ixvmChassisBuilder.py.'
        errMsg = errMsg+'\n\tThe parameters file ixvmParams.py is not found.\n\n'
        sys.exit(errMsg)
    from ixvmParams import *
    #ixvmCardPortList = 'nonInteractive'
    mode = 'nonInteractive'

    if sys.argv[1] not in ['add', 'remove']:
        sys.exit('\nError: For interactive mode, you must specified add or remove: ./ixVmChassisBuilder.py add|remove ixVmParams.py')

    action = sys.argv[1]


if mode == 'interactive':
    try:
        apiServerIp = askQuestion('What is the IxNetwork API server IP?', defaultValue=None,
                                  expectedPattern='[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
        apiServerIpPort = askQuestion('What is the IxNetwork API server IP Port? (11009)', defaultValue='11009',
                                      expectedPattern='[0-9]+')

        # Connect to the IxNetwork API server. Only continue if it is successful.
        try:
            restObj = IxVmChassisBuilder(serverIp=apiServerIp, serverPort=apiServerIpPort)
        except IxNetRestApiException as errMsg:
            sys.exit('\nFailed to connect to:{0}:{1}\n'.format(apiServerIp, apiServerIpPort))

        print('\nSuccessfully connected to:{0}:{1}'.format(apiServerIp, apiServerIpPort))

        addOrRemoveCards = askQuestion('Do you want to add or remove IxVM appliances?\n\t(1=add, 2=remove, Default=1)',
                                       defaultValue='1', expectedPattern='1|2')

        # ADD
        if addOrRemoveCards == '1':
            action = 'add'
            hypervisorInput = askQuestion('Which hypervisor:\n\n\t(1) vmware\n\t(2) qemu\n\nPlease select (Default=1):',
                                          defaultValue='1', expectedPattern='1|2')
            if not hypervisorInput:
                hypervisorType == 'vmware'
            if hypervisorInput == '1':
                hypervisorType = 'vmware'
            if hypervisorInput == '2':
                hypervisorType = 'qemu'

            vChassisIp = askQuestion('What is the virtual chassis IP? ', expectedPattern='[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
            username = askQuestion('What is the virtual chassis username? (default=admin) ', defaultValue='admin',
                                   expectedPattern=None)
            password = askQuestion('What is the virtual chassis username password? (default=admin) ',
                                   defaultValue='admin', expectedPattern=None)

            totalIxVmCards = askQuestion('How many IxVM cards do you want to add? ', defaultValue=None, expectedPattern='[0-9]+')
            question = '\nDo you want to accept the following default settings for the IxVM cards?'
            question = question+'\n\n\tpromiscuousMode = False\n\tmtu = 1500\n\tkeepAlive = 300'
            question = question+'\n\nEnter 1 for Yes\nEnter 2 for No\nDefault = 1'
            question = question+'\n\nMake your selection: '
            ixVmCardDefaultSetting = askQuestion(question, defaultValue='1', expectedPattern='1|2')

            print()
            ixvmCardPortList = []
            for cardNumber in range(1,int(totalIxVmCards)+1):
                mgmtIp = askQuestion('What is the management IP address of card{0}?'.format(cardNumber),
                                     expectedPattern='[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
                if ixVmCardDefaultSetting == '1':
                    ixvmCardPortList.insert(len(ixvmCardPortList), {'mgmtIp': mgmtIp, 'promiscuousMode': False,
                                                                    'mtu': '1500', 'keepAlive': '300'})

                if ixVmCardDefaultSetting == '2':
                    promiscuousMode = askQuestion('Promiscuous mode for card{0}? (1=true, 2=false, default=1) '.format(cardNumber),
                                                  defaultValue='1', expectedPattern='1|2')
                    if promiscuousMode == '1':
                        promiscuousMode = True
                    if promiscuousMode == '2':
                        promiscuousMode = False
                    mtu = askQuestion('MTU for card{0}? (default=1500) '.format(cardNumber))
                    keepAlive = askQuestion('Keep Alive for card{0}? (Default=300)) '.format(cardNumber),
                                            defaultValue='300', expectedPattern='[0-9]+')

                    ixvmCardPortList.insert(len(ixvmCardPortList), {'mgmtIp': mgmtIp, 'promiscuousMode': promiscuousMode,
                                                                    'mtu': mtu, 'keepAlive': keepAlive})

        # REMOVE
        elif addOrRemoveCards == '2':
            action = 'remove'
            removeVChassis = True
            removeVChassisInput = askQuestion('Do you want to remove all discovered vChassis or specify a vChassis?\n(1=All, 2=Specify, 3=DoNotRemove, Default=1) ', defaultValue='1', expectedPattern='1|2|3')
            if removeVChassisInput == '1':
                vChassisIp = 'all'
            if removeVChassisInput == '2':
                vChassisIp = askQuestion('What is the virtual chassis IP? ', expectedPattern='[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
            if removeVChassisInput == '3':
                removeVChassis = False

            removeCardsInput = askQuestion('Do you want to remove all the vm cards? (1=Yes, 2=No, Default=1) ',
                                           defaultValue='1', expectedPattern='1|2')

            '''
            removeHypervisorInput = askQuestion('Do you want to remove all hypervisors? (1=Yes, 2=No, Default=1) ',
                                           defaultValue='1', expectedPattern='1|2')

            if not removeHypervisorInput:
                removeHypervisor = 'all'
            if removeHypervisorInput == '1':
                removeHypervisor = 'all'
            if removeHypervisorInput == '2':
                removeHypervisor = askQuestion('What is the hypervisor IP address that you want to remove? ',
                                               expectedPattern='[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
            '''

            vmMgmtCardListToRemove = []
            if removeCardsInput == '1':
                vmMgmtCardListToRemove = 'all'
            if removeCardsInput == '2':
                totalCardsToRemove = askQuestion('How many vm cards do you want to remove? ', expectedPattern='[0-9]+')
                for cardNumber in range(1,int(totalCardsToRemove)+1):
                    mgmtIp = askQuestion('What is the mgmt IP for card{0} to remove? '.format(cardNumber),
                                         expectedPattern='[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
                    vmMgmtCardListToRemove.append(mgmtIp)

        else:
            sys.exit('\nUnknown choice:', addOrRemoveCards)

    except KeyboardInterrupt:
        sys.exit('\nAborted\n')

try:
    restObj = IxVmChassisBuilder(serverIp=apiServerIp, serverPort=apiServerIpPort)

    if action == 'add':
        # First, clean up all residual hypervisors and cards in case there is any. 
        # Otherwise, creating new cardID will fail.
        restObj.removeAllSuper()
        restObj.connectToVChassis(vChassisIp)
        restObj.ixVmCreateHypervisor(enabled='true', serverIp=vChassisIp, hypervisorType=hypervisorType,
                                     userLoginName=username, userPassword=password)
        restObj.ixVmAddCardIdPortId(ixvmCardPortList)

    if action == 'remove':
        if vmMgmtCardListToRemove == 'all':
            restObj.ixVmRemoveAllCardId()
        else:
            for ixVmCardMgmt in vmMgmtCardListToRemove:
                restObj.ixVmRemoveCardId(ixVmCardMgmt)

        restObj.ixVmDeleteHypervisor(serverIp=vChassisIp)
        restObj.disconnectIxChassis(vChassisIp)

        # Delete the virtual chassis
        if removeVChassis:
            restObj.ixVmDeleteVirtualChassis(vChassisIp)

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    print('\n%s' % traceback.format_exc())
    print('\nException Error:', errMsg)
