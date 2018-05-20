# PLEASE READ DISCLAIMER
#
#    This class demonstrates sample IxNetwork REST API usage for
#    demo and reference purpose only.
#    It is subject to change for updates without warning.

import re, time
from IxNetRestApi import IxNetRestApiException

# 8.40 updates:
#    sessionStatus uses ?includes=sessionStatus and then response.json()['sessionStatus']
#       - verifyProtocolSessionsNgpf 
#       - verifyAllProtocolSessionsInternal
#       - getNgpfGatewayIpMacAddress (resolvedGatewayMac rquires ?includes=resolvedGatewayMac)
#       - showTopologies
#       - verifyArp
#
#    bgpIpv4Peer/1: LocalIpv4Ver2 for localIpAddress is removed.
#

class Protocol(object):
    def __init__(self, ixnObj=None, portMgmtObj=None):
        """
        Parameters
        ixnObj: <str>: The main connection object.
        portMgmtObj: <str>: Optional. It's deprecated. Leaving it here for backward compatibility
        """
        self.ixnObj = ixnObj
        self.configuredProtocols = []

        from IxNetRestApiPortMgmt import PortMgmt
        self.portMgmtObj = PortMgmt(self.ixnObj)

        from IxNetRestApiStatistics import Statistics
        self.statObj = Statistics(self.ixnObj)

    def setMainObject(self, mainObject):
        """
        Description
           For Python Robot Framework support
        
        Parameter
           mainObject: <str>: The connect object.
        """
        self.ixnObj = mainObject
        self.portMgmtObj.setMainObject(mainObject)
        self.statObj.setMainObject(mainObject)

    def getSelfObject(self):
        """
        Description
           For Python Robot Framework support.
           Get the Connect object.
        """
        return self

    def createTopologyNgpf(self, portList, topologyName=None):
        """
        Description
            Create a new Topology and assign ports to it.

        Parameters
            portList: <list>: format = [[(str(chassisIp), str(slotNumber), str(portNumber)] ]
                      Example 1: [ ['192.168.70.10', '1', '1'] ]
                      Example 2: [ ['192.168.70.10', '1', '1'], ['192.168.70.10', '2', '1'] ]

            topologyName: <str>: Give a name to the Topology Group.

        Syntax
            POST: /api/v1/sessions/{id}/ixnetwork/topology

        Return
            /api/v1/sessions/{id}/topology/{id}
        """
        url = self.ixnObj.sessionUrl+'/topology'
        vportList = self.portMgmtObj.getVports(portList)
        if len(vportList) != len(portList):
            raise IxNetRestApiException('createTopologyNgpf: There is not enough vports created to match the number of ports.')

        topologyData = {'vports': vportList}
        if topologyName != None:
            topologyData['name'] = topologyName

        self.ixnObj.logInfo('\nCreate new Topology Group')
        response = self.ixnObj.post(url, data=topologyData)
        topologyObj = response.json()['links'][0]['href']
        return topologyObj

    def createDeviceGroupNgpf(self, topologyObj, multiplier=1, deviceGroupName=None):
        """
        Description
            Create a new Device Group.

        Parameters
            topologyObj: <str>: A Topology object: /api/v1/sessions/1/ixnetwork/topology/{id}
            multiplier: <int>: The amount of host to create (In integer).
            deviceGroupName: <str>: Optional: Device Group name.

        Syntax
            POST: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup

        Returns:
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}
        """
        url = self.ixnObj.httpHeader+topologyObj+'/deviceGroup'
        deviceGroupData = {'multiplier': int(multiplier)}
        if deviceGroupName != None:
            deviceGroupData['name'] = deviceGroupName

        self.ixnObj.logInfo('\nCreate new Device Group')
        response = self.ixnObj.post(url, data=deviceGroupData)
        deviceGroupObj = response.json()['links'][0]['href']
        return deviceGroupObj

    def createLacpNgpf(self, ethernetObj, **kwargs):
        """
        Description
            Create new LACP group.

        Parameter
            ethernetObj: <str>:The Ethernet stack object to create the LACP.
                               Example: '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1

            administrativeKey: <int>: Default=1
            actorSystemId: <str>: Default='00 00 00 00 00 01'.
            actorSystemPriority: <int>: Default=1
            actorKey: <int>: Default=1
            actorPortNumber: <int>: Default=1
            actorPortPriority: <int>: Default=1

        Syntax
            POST: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/lacp
            PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/lacp/{id}

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/lacp/{id}
        """
        response = self.ixnObj.post(self.ixnObj.httpHeader+ethernetObj+'/lacp')
        lacpObj = response.json()['links'][0]['href']
        self.configuredProtocols.append(lacpObj)
        
        self.ixnObj.logInfo('\nCreate new LACP NGPF')
        lacpResponse = self.ixnObj.get(self.ixnObj.httpHeader+lacpObj)

        lacpAttributes = ['administrativeKey', 'actorSystemId', 'actorSystemPriority', 'actorKey', 'actorPortNumber', 'actorPortPriority']

        for lacpAttribute in lacpAttributes:
            if lacpAttribute in kwargs:
                multiValue = lacpResponse.json()[lacpAttribute]
                self.ixnObj.logInfo('\nConfiguring LACP attribute: %s' % lacpAttribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': kwargs[lacpAttribute]})

        return lacpObj

    def createEthernetNgpf(self, obj, **kwargs):
        """
        Description
            Create or modify NGPF Ethernet.
            To create a new Ethernet stack in NGPF, pass in the device group object.
            To modify an existing Ethernet stack in NGPF, pass in the Ethernet object.

        Parameters
            obj: <str>: Device Group obj: '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/2'
                        Ethernet obj: '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1'

            name|ethernetName: <str>:  Ethernet name.
            macAddress: <dict>: By default, IxNetwork will generate unique Mac Addresses.
                               {'start': '00:01:02:00:00:01', 'direction': 'increment', 'step': '00:00:00:00:00:01'}
                               Note: step: '00:00:00:00:00:00' means don't increment.

            macAddressPortStep:<str>: disable|00:00:00:01:00:00
                                      Incrementing the Mac address on each port based on your input.
                                      '00:00:00:00:00:01' means to increment the last byte on each port.

            vlanId: <dict>: Example: {'start': 103, 'direction': 'increment', 'step': 1}
            vlanPriority: <dict>:  Example: {'start': 2, 'direction': 'increment', 'step': 1}
            mtu: <dict>: Example: {'start': 1300, 'direction': 'increment', 'step': 1})

         Syntax
             POST:  /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet
             PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}

         Example:
             createEthernetNgpf(deviceGroupObj1,
                                ethernetName='Eth1',
                                macAddress={'start': '00:01:01:00:00:01',
                                            'direction': 'increment',
                                            'step': '00:00:00:00:00:01'},
                                macAddressPortStep='00:00:00:00:01:00',
                                vlanId={'start': 128, 'direction': 'increment', 'step':0},
                                vlanPriority={'start': 7, 'direction': 'increment', 'step': 0},
                                mtu={'start': 1400, 'direction': 'increment', 'step': 0},                                
                                )
        """
        createNewEthernetObj = True

        # To create a new Ethernet object
        if 'ethernet' not in obj:
            url = self.ixnObj.httpHeader+obj + '/ethernet'
            self.ixnObj.logInfo('\nCreate new Ethernet on NGPF')
            response = self.ixnObj.post(url)
            ethernetObj = response.json()['links'][0]['href']

        # To modify 
        if 'ethernet' in obj:
            ethernetObj = obj
            createNewEthernetObj = False

        ethObjResponse = self.ixnObj.get(self.ixnObj.httpHeader+ethernetObj)

        if 'ethernetName' in kwargs or 'name' in kwargs:
            if 'ethernetName' in kwargs:
                # This is to handle backward compatibility. This attribute should not be created. 
                # Should be using 'name'.
                name = kwargs['ethernetName']
            if 'name' in kwargs:
                name = kwargs['name']
                self.ixnObj.logInfo('\nConfigure MAC address name')
            self.ixnObj.patch(self.ixnObj.httpHeader+ethernetObj, data={'name': name})

        if 'macAddress' in kwargs:
            multivalue = ethObjResponse.json()['mac']
            self.ixnObj.logInfo('\nConfigure MAC address. Attribute for multivalueId = jsonResponse["mac"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['macAddress'])

            # Config Mac Address Port Step
            self.ixnObj.logInfo('\nConfigure MAC address port step')
            portStepMultivalue = self.ixnObj.httpHeader + multivalue+'/nest/1'
            if 'macAddressPortStep' in kwargs:
                if kwargs['macAddressPortStep'] != 'disabled':
                    self.ixnObj.patch(portStepMultivalue, data={'step': kwargs['macAddressPortStep']})
                if kwargs['macAddressPortStep'] == 'disabled':
                    self.ixnObj.patch(portStepMultivalue, data={'enabled': False})

        if 'vlanId' in kwargs and kwargs['vlanId'] != None:
            # Enable VLAN
            if createNewEthernetObj == True:
                multivalue = ethObjResponse.json()['enableVlans']
                self.ixnObj.logInfo('\nEnabling VLAN ID.  Attribute for multivalueId = jsonResponse["enablevlans"]')
                self.configMultivalue(multivalue, 'singleValue', data={'value': True})
                
            # CREATE vlan object (Creating vlanID always /vlan/1 and then do a get for 'vlanId')
            vlanIdObj = self.ixnObj.httpHeader+ethernetObj+'/vlan/1'
            vlanIdResponse = self.ixnObj.get(vlanIdObj)
            multivalue = vlanIdResponse.json()['vlanId']

            # CONFIG VLAN ID
            self.ixnObj.logInfo('\nConfigure VLAN ID. Attribute for multivalueId = jsonResponse["vlanId"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['vlanId'])

        # CONFIG VLAN PRIORITY
        if 'vlanPriority' in kwargs and kwargs['vlanPriority'] != None:
            multivalue = vlanIdResponse.json()['priority']
            self.ixnObj.logInfo('\nConfigure VLAN ID priority. Attribute for multivalue = jsonResponse["priority"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['vlanPriority'])

        if 'mtu' in kwargs and kwargs['mtu'] != None:
            multivalue = ethObjResponse.json()['mtu']
            self.ixnObj.logInfo('\nConfigure MTU. Attribute for multivalueId = jsonResponse["mtu"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['mtu'])
            
        return ethernetObj

    def configIsIsL3Ngpf(self, obj, **data):
        """
        Description
            Create or modify ISISL3

        Parameters
            ethernetObj: '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1'
            data: The ISISL3 attributes.  You could view all the attributes from the IxNetwork API browser.

        Syntax
            POST:  /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/isisL3
            PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/isisL3/{id}

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/isisL3/{id}
        """
        createNewIsIsObj = True

        if 'isis' in obj:
            # To modify ISIS
            isisObj = obj
            createNewIsIsObj = False
        else:
            # To create a new ISIS object
            url = self.ixnObj.httpHeader+obj + '/isisL3'
            self.ixnObj.logInfo('\nCreating new ISIS in NGPF')
            response = self.ixnObj.post(url, data=data)
            isisObj = response.json()['links'][0]['href']
            
        response = self.ixnObj.get(self.ixnObj.httpHeader+isisObj)
        self.configuredProtocols.append(isisObj)
        return isisObj

    def getDeviceGroupIsIsL3RouterObj(self, deviceGroupObj):
        """ 
        Description
           Get and return the Device Group's ISIS L3 Router object.
          
        Parameter
           deviceGroupObj: <str:obj>: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{1}

        Return
           IsIsL3Router obj: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/isisL3Router/{id}
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader + deviceGroupObj + '/isisL3Router')
        return response.json()[0]['links'][0]['href']

    def configIsIsL3RouterNgpf(self, isisL3RouterObj, **data):
        """
        Description
           Configure ISIS L3 Router

        Parameter
           isisL3RouterObj: <str:obj>: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/isisL3Router/{id}

           **data: <dict>:  Get attributes from the IxNetwork API browser.
        """
        self.ixnObj.patch(self.ixnObj.httpHeader + isisL3RouterObj, data=data)

    def createIpv4Ngpf(self, obj, **kwargs):
        """
        Description
            Create or modify NGPF IPv4.
            To create a new IPv4 stack in NGPF, pass in the Ethernet object.
            To modify an existing IPv4 stack in NGPF, pass in the IPv4 object.

        Parameters
            obj: <str>: Ethernet obj: '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1'
                        IPv4 obj: '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1'

            ipv4Address: <dict>: {'start': '100.1.1.100', 'direction': 'increment', 'step': '0.0.0.1'},
            ipv4AddressPortStep: <str>|<dict>:  disable|0.0.0.1 
                                 Incrementing the IP address on each port based on your input.
                                 0.0.0.1 means to increment the last octet on each port.

            gateway: <dict>: {'start': '100.1.1.1', 'direction': 'increment', 'step': '0.0.0.1'},
            gatewayPortStep:  <str>|<dict>:  disable|0.0.0.1 
                              Incrementing the IP address on each port based on your input.
                              0.0.0.1 means to increment the last octet on each port.

            prefix: <int>:  Example: 24
            rsolveGateway: <bool>

        Syntax
            POST:  /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4
            PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}

        Example:
             ipv4Obj1 = createIpv4Ngpf(ethernetObj1,
                                       ipv4Address={'start': '100.1.1.1', 'direction': 'increment', 'step': '0.0.0.1'},
                                       ipv4AddressPortStep='disabled',
                                       gateway={'start': '100.1.1.100', 'direction': 'increment', 'step': '0.0.0.0'},
                                       gatewayPortStep='disabled',
                                       prefix=24,
                                       resolveGateway=True)

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}
        """
        createNewIpv4Obj = True

        if 'ipv4' in obj:
            # To modify IPv4
            ipv4Obj = obj
            createNewIpv4Obj = False
        else:
            # To create a new IPv4 object
            ipv4Url = self.ixnObj.httpHeader+obj+'/ipv4'
            self.ixnObj.logInfo('\nCreating new IPv4 in NGPF')
            response = self.ixnObj.post(ipv4Url)
            ipv4Obj = response.json()['links'][0]['href']

        ipv4Response = self.ixnObj.get(self.ixnObj.httpHeader+ipv4Obj)

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+ipv4Obj, data={'name': kwargs['name']})

        # Config IPv4 address
        if 'ipv4Address' in kwargs:
            multivalue = ipv4Response.json()['address']
            self.ixnObj.logInfo('\nConfiguring IPv4 address. Attribute for multivalueId = jsonResponse["address"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['ipv4Address'])

        # Config IPv4 port step
        # disabled|0.0.0.1
        if 'ipv4AddressPortStep' in kwargs:
            portStepMultivalue = self.ixnObj.httpHeader+multivalue+'/nest/1'
            self.ixnObj.logInfo('\nConfigure IPv4 address port step')
            if kwargs['ipv4AddressPortStep'] != 'disabled':
                self.ixnObj.patch(portStepMultivalue, data={'step': kwargs['ipv4AddressPortStep']})
            if kwargs['ipv4AddressPortStep'] == 'disabled':
                self.ixnObj.patch(portStepMultivalue, data={'enabled': False})

        # Config Gateway
        if 'gateway' in kwargs:
            multivalue = ipv4Response.json()['gatewayIp']
            self.ixnObj.logInfo('\nConfigure IPv4 gateway. Attribute for multivalueId = jsonResponse["gatewayIp"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['gateway'])

        # Config Gateway port step
        if 'gatewayPortStep' in kwargs:
            portStepMultivalue = self.ixnObj.httpHeader+multivalue+'/nest/1'
            self.ixnObj.logInfo('\nConfigure IPv4 gateway port step')
            if kwargs['gatewayPortStep'] != 'disabled':
                self.ixnObj.patch(portStepMultivalue, data={'step': kwargs['gatewayPortStep']})
            if kwargs['gatewayPortStep'] == 'disabled':
                self.ixnObj.patch(portStepMultivalue, data={'enabled': False})

        # Config resolve gateway
        if 'resolveGateway' in kwargs:
            multivalue = ipv4Response.json()['resolveGateway']
            self.ixnObj.logInfo('\nConfigure IPv4 gateway to resolve gateway. Attribute for multivalueId = jsonResponse["resolveGateway"]')
            self.configMultivalue(multivalue, 'singleValue', data={'value': kwargs['resolveGateway']})

        if 'prefix' in kwargs:
            multivalue = ipv4Response.json()['prefix']
            self.ixnObj.logInfo('\nConfigure IPv4 prefix. Attribute for multivalueId = jsonResponse["prefix"]')
            self.configMultivalue(multivalue, 'singleValue', data={'value': kwargs['prefix']})

        if createNewIpv4Obj == True:
            self.configuredProtocols.append(ipv4Obj)

        return ipv4Obj

    def configDhcpClientV4(self, obj, **kwargs):
        """
        Description
            Create or modify DHCP V4 Client in NGPF.
            To create a new DCHP v4 Client stack in NGPF, pass in the Ethernet object.
            To modify an existing DHCP V4 Client stack in NGPF, pass in the dhcpv4client object.

        Parameters
            obj: <str>: To create new DHCP obj: Ethernet example: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1
            obj: <str>: To Modify DHCP client: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/dhcpv4client/1

            dhcp4Broadcast: <bool>
            multiplier: <int>: The amount of DHCP clients to create.
            dhcp4ServerAddress: <str>: The DHCP server IP address.
            dhcp4UseFirstServer: <bool>: Default=True
            dhcp4GatewayMac: <str>: Gateway mac address in the format of 00:00:00:00:00:00
            useRapdCommit: <bool>: Default=False
            renewTimer: <int>: Default=0
    
        Syntax
            POST:  /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/dhcpv4client
            PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/dhcpv4client/{id}

        Example:
            dhcpClientObj = protocolObj.configV4DhcpClient(ethernetObj1,
                                                           dhcp4Broadcast=True,
                                                           multiplier = 10,
                                                           dhcp4ServerAddress='1.1.1.11',
                                                           dhcp4UseFirstServer=True,
                                                           dhcp4GatewayMac='00:00:00:00:00:00',
                                                           useRapdCommit=False,
                                                           renewTimer=0)

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/dhcpv4client/{id}
        """
        # To create new DHCP object
        if 'dhcp' not in obj:
            dhcpUrl = self.ixnObj.httpHeader+obj+'/dhcpv4client'
            self.ixnObj.logInfo('\nCreate new DHCP client V4')
            response = self.ixnObj.post(dhcpUrl)
            # /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/dhcpv4client/1
            dhcpObj = response.json()['links'][0]['href']

        # To modify DHCP
        if 'dhcp' in obj:
            dhcpObj = obj

        dhcpObjResponse = self.ixnObj.get(self.ixnObj.httpHeader+dhcpObj)

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+dhcpObj, data={'name': kwargs['name']})

        # All of these DHCP attributes configures multivalue singleValue. So just loop them to do the same thing.
        dhcpAttributes = ['dhcp4Broadcast', 'dhcp4UseFirstServer', 'dhcp4ServerAddress', 'dhcp4GatewayMac', 'dhcp4GatewayAddress'
                          'useRapidCommit', 'dhcp4GatewayMac', 'renewTimer']

        for dhcpAttribute in dhcpAttributes:
            if dhcpAttribute in kwargs:
                multiValue = dhcpObjResponse.json()[dhcpAttribute]
                self.ixnObj.logInfo('\nConfiguring DHCP Client attribute: %s' % dhcpAttribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': kwargs[dhcpAttribute]})

        self.configuredProtocols.append(dhcpObj)
        return dhcpObj

    def configDhcpServerV4(self, obj, **kwargs):
        """
        Description
            Create or modify DHCP v4 Server in NGPF.
            To create a new DCHP v4 server stack in NGPF, pass in the IPv4 object.
            To modify an existing DHCP V4 server stack in NGPF, pass in the dhcpv4server object.

        Parameters
            obj: <str>: To create new DHCP: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1
            obj: <str>: To modify DHCP server: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/dhcpv4server/1

            useRapidCommit: <bool>: Default=False
            multiplier: <int>: Default-1
            subnetAddrAssign: <bool>: Default=False
            defaultLeaseTime: <int>: Default=86400
            echoRelayInfo: <bool>: Default=True
            ipAddress: <str>: The DHCP server IP address.
            ipAddressIncrement: <str>: format='0.0.0.1'
            ipDns1: <str>: Default='0.0.0.0'
            ipDns2: <str>: Default=='0.0.0.0'
            ipGateway: <str>: The DHCP server gateway IP address.
            ipPrefix: <int>: The DHCP server IP address prefix. Ex: 16.
            poolSize: <int>: The DHCP server pool size.

        Syntax
            POST:  /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/dhcpv4server
            PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/dhcpv4server/{id}

        Example:
            protocolObj.configV4DhcpServer('/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4/1',
                                           name='DHCP-Server-1',
                                           multiplier='1',
                                           useRapidCommit=False,
                                           subnetAddrAssign=False,
                                           defaultLeaseTime=86400,
                                           echoRelayInfo=True,
                                           ipAddress='1.1.1.1',
                                           ipAddressIncrement='0.0.0.1',
                                           ipDns1='0.0.0.0',
                                           ipDns2='0.0.0.0',
                                           ipGateway='1.1.1.11',
                                           ipPrefix=24,
                                           poolSize=10)

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/dhcpv4server/{id}
        """
        # To create new DHCP serverobject
        if 'dhcp' not in obj:
            dhcpUrl = self.ixnObj.httpHeader+obj+'/dhcpv4server'
            self.ixnObj.logInfo('\nCreate new DHCP server v4')
            response = self.ixnObj.post(dhcpUrl)
            # /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/dhcpv4server/1
            dhcpObj = response.json()['links'][0]['href']

        # To modify DHCP server
        if 'dhcp' in obj:
            dhcpObj = obj

        dhcpObjResponse = self.ixnObj.get(self.ixnObj.httpHeader+dhcpObj)

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+dhcpObj, data={'name': kwargs['name']})

        # All of these DHCP attributes configures multivalue singleValue. So just loop them to do the same thing.
        dhcpServerAttributes = ['useRapidCommit', 'subnetAddrAssign']

        for dhcpAttribute in dhcpServerAttributes:
            if dhcpAttribute in kwargs:
                multiValue = dhcpObjResponse.json()[dhcpAttribute]
                self.ixnObj.logInfo('\nConfiguring DHCP Server attribute: %s' % dhcpAttribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': kwargs[dhcpAttribute]})

        if 'multiplier' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+dhcpObj, data={'multiplier': kwargs['multiplier']})

        dhcpServerSessionObjResponse = self.ixnObj.get(self.ixnObj.httpHeader+dhcpObj+'/dhcp4ServerSessions')
        dhcpServerSessionAttributes = ['defaultLeaseTime', 'echoRelayInfo', 'ipAddress', 'ipAddressIncrement',
                                       'ipDns1', 'ipDns2', 'ipGateway', 'ipPrefix', 'poolSize']

        for dhcpAttribute in dhcpServerSessionAttributes:
            if dhcpAttribute in kwargs:
                multiValue = dhcpServerSessionObjResponse.json()[dhcpAttribute]
                self.ixnObj.logInfo('\nConfiguring DHCP Server session attribute: %s' % dhcpAttribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': kwargs[dhcpAttribute]})

        #self.configuredProtocols.append(dhcpObj)
        return dhcpObj

    def configOspf(self, obj, **kwargs):
        """
        Description
            Create or modify OSPF.

        Parameters
            IPv4 object handle example:
            obj: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1

            OSPF object handle example:
            obj: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/ospfv2/1

        Syntax
            POST:  /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/ospfv2
            PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/ospfv2/{id}

        Example:
            ospfObj1 = configOspf(ipv4Obj,
                          name = 'ospf_1',
                          areaId = '0',
                          neighborIp = '1.1.1.2',
                          helloInterval = '10',
                          areaIdIp = '0.0.0.0',
                          networkType = 'pointtomultipoint',
                          deadInterval = '40')

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/ospfv2/{id}
        """
        # To create new OSPF object
        if 'ospf' not in obj:
            ospfUrl = self.ixnObj.httpHeader+obj+'/ospfv2'
            self.ixnObj.logInfo('\nCreate new OSPFv2 in NGPF')
            response = self.ixnObj.post(ospfUrl)
            # /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/ospfv2/1
            ospfObj = response.json()['links'][0]['href']

        # To modify OSPF
        if 'ospf' in obj:
            ospfObj = obj

        ospfObjResponse = self.ixnObj.get(self.ixnObj.httpHeader+ospfObj)

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+ospfObj, data={'name': kwargs['name']})

        # All of these BGP attributes configures multivalue singleValue. So just loop them to do the same thing.
        ospfAttributes = ['areaId', 'neighborIp', 'helloInterval', 'areadIdIp', 'networkType', 'deadInterval']

        for ospfAttribute in ospfAttributes:
            if ospfAttribute in kwargs:
                multiValue = ospfObjResponse.json()[ospfAttribute]
                self.ixnObj.logInfo('\nConfiguring OSPF attribute: %s' % ospfAttribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': kwargs[ospfAttribute]})

        self.configuredProtocols.append(ospfObj)
        return ospfObj

    def configBgp(self, obj, **kwargs):
        """
        Description
            Create or modify BGP.  If creating a new BGP header, provide an IPv4 object handle.
            If modifying a BGP, provide the BGP object handle.

        Parameters
            obj: <str>: Either an IPv4 object or a BGP object.
                 IPv4 object example: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1
                 BGP object example: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1

            kwargs: BGP configuration attributes. The attributes could be obtained from the IxNetwork API browser.

        Syntax
            POST:  /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/bgpIpv4Peer
            PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/bgpIpv4Peer/{id}

        Example:
            configBgp(ipv4Obj,
                  name = 'bgp_1',
                  enableBgp = True,
                  holdTimer = 90,
                  dutIp={'start': '1.1.1.2', 'direction': 'increment', 'step': '0.0.0.0'},
                  localAs2Bytes=101,
                  enableGracefulRestart = False,
                  restartTime = 45,
                  type = 'internal',
                  enableBgpIdSameasRouterId = True,
                  staleTime = 0,
                  flap = ['false', 'false', 'false', 'false']

            # flap = true or false.  Provide a list of total true or false according to the total amount of host IP interfaces.

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/bgpIpv4Peer/{id}
        """
        # To create a new BGP stack using IPv4 object.
        if 'bgp' not in obj:
            bgpUrl = self.ixnObj.httpHeader+obj+'/bgpIpv4Peer'
            self.ixnObj.logInfo('\nCreate new BGP in NGPF')
            response = self.ixnObj.post(bgpUrl)
            # /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1
            bgpObj = response.json()['links'][0]['href']

        # To modify BGP by providing a BGP object handle.
        if 'bgp' in obj:
            bgpObj = obj

        bgpObjResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpObj)

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+bgpObj, data={'name': kwargs['name']})

        if 'enableBgp' in kwargs and kwargs['enableBgp'] == True:
            multiValue = bgpObjResponse.json()['enableBgpId']
            self.ixnObj.logInfo('\nEnabling BGP protocol. Attribut for multivalue = enableBgpId')
            self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': True})

        if 'dutIp' in kwargs:
            multiValue = bgpObjResponse.json()['dutIp']
            self.ixnObj.logInfo('\nConfigure BGP DUT IP. Attribut for multivalue = dutIp')
            self.configMultivalue(multiValue, 'counter', data=kwargs['dutIp'])

        # All of these BGP attributes configures multivalue singleValue. So just loop them to do the same thing.
        # Note: Don't include flap.  Call flapBgp instead because the uptime and downtime needs to be configured.
        bgpAttributes = ['localAs2Bytes', 'localAs4Bytes', 'enable4ByteAs', 'enableGracefulRestart', 'restartTime', 'type',
                         'staleTime', 'holdTimer', 'enableBgpIdSameasRouterId']

        for bgpAttribute in bgpAttributes:
            if bgpAttribute in kwargs:
                multiValue = bgpObjResponse.json()[bgpAttribute]
                self.ixnObj.logInfo('\nConfiguring BGP multivalue attribute: %s' % bgpAttribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': kwargs[bgpAttribute]})
            
        self.configuredProtocols.append(bgpObj)
        return bgpObj

    def configIgmpHost(self, ipObj, **kwargs):
        """
        Description
            Create or modify IGMP host.
            Provide an IPv4|IPv6 obj to create a new IGMP host object.
            Provide an IGMP host object to modify.

        Parameters
            ipObj: <str:obj>: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1
            igmpObj: <str:obj>: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmp/1

        Syntax
            POST:  /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/igmp
            PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/igmp/{id}
        
        Example:

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/igmp/{id}
        """
        # To create new IGMP object
        if 'igmp' not in obj:
            igmpUrl = self.ixnObj.httpHeader+obj+'/igmp'
            self.ixnObj.logInfo('\nCreate new IGMP V4 host')
            response = self.ixnObj.post(igmpUrl)
            # /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmp/1
            igmpObj = response.json()['links'][0]['href']

        # To modify OSPF
        if 'igmp' in obj:
            igmpObj = obj

        igmpObjResponse = self.ixnObj.get(self.ixnObj.httpHeader+igmpObj)

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+igmpObj, data={'name': kwargs['name']})

        # All of these BGP attributes configures multivalue singleValue. So just loop them to do the same thing.
        igmpAttributes = ['areaId', 'neighborIp', 'helloInterval', 'areadIdIp', 'networkType', 'deadInterval']

        for igmpAttribute in igmpAttributes:
            if igmpAttribute in kwargs:
                multiValue = igmpObjResponse.json()[igmpAttribute]
                self.ixnObj.logInfo('\nConfiguring IGMP host attribute: %s' % igmpAttribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': kwargs[igmpAttribute]})

        self.configuredProtocols.append(igmpObj)
        return igmpObj

    def configMpls(self, ethernetObj, **kwargs):
        """
        Description
            Create or modify static MPLS.  

        Parameters
            ethernetObj: <str>: The Ethernet object handle.
                         Example: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1

        Syntax
            POST:  /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/mpls
            PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/mpls/{id}

        Example:
            mplsObj1 = protocolObj.configMpls(ethernetObj1,
                                      name = 'mpls-1',
                                      destMac = {'start': '00:01:02:00:00:01', 'direction': 'increment', 'step': '00:00:00:00:00:01'},
                                      exp = {'start': 0, 'direction': 'increment', 'step': 1},
                                      ttl = {'start': 16, 'direction': 'increment', 'step': 1},
                                      rxLabelValue = {'start': 288, 'direction': 'increment', 'step': 1},
                                      txLabelValue = {'start': 888, 'direction': 'increment', 'step': 1})

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/mpls/{id}
        """
        # To create a new MPLS
        if 'mpls' not in ethernetObj:
            mplsUrl = self.ixnObj.httpHeader+ethernetObj+'/mpls'
            self.ixnObj.logInfo('\nCreate new MPLS protocol in NGPF')
            response = self.ixnObj.post(mplsUrl)
            mplsObj = response.json()['links'][0]['href']

        # To modify MPLS
        if 'mpls' in ethernetObj:
            mplsObj = ethernetObj

        self.ixnObj.logInfo('\nGET ATTRIBUTE MULTIVALUE IDs')
        mplsResponse = self.ixnObj.get(self.ixnObj.httpHeader+mplsObj)

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+mplsObj, data={'name': kwargs['name']})

        # All of these mpls attributes configures multivalue counter. So just loop them to do the same thing.
        mplsAttributes = ['rxLabelValue', 'txLabelValue', 'destMac', 'cos', 'ttl']

        for mplsAttribute in mplsAttributes:
            if mplsAttribute in kwargs:
                multiValue = mplsResponse.json()[mplsAttribute]
                self.ixnObj.logInfo('\nConfiguring MPLS attribute: %s' % mplsAttribute)
                self.configMultivalue(multiValue, 'counter', data=kwargs[mplsAttribute])
                
        self.configuredProtocols.append(mplsObj)
        return mplsObj

    def configVxlanNgpf(self, obj, **kwargs):
        """
        Description
            Create or modify a VXLAN.  If creating a new VXLAN header, provide an IPv4 object handle.
            If creating a new VxLAN object, provide an IPv4 object handle.
            If modifying a VXLAN header, provide the VXLAN object handle.
            
        Parameters
               obj: <str>: IPv4 Obj example: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1
                           VxLAN Obj example: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/vxlan/1

        Syntax
            POST:  /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/vxlan
            PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/vxlan/{id}

        Example:
            createVxlanNgpf(ipv4Object='/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1',
                            vtepName='vtep_1',
                            vtepVni={'start':2008, 'step':2, 'direction':'increment'},
                            vtepIpv4Multicast={'start':'225.8.0.1', 'step':'0.0.0.1', 'direction':'increment'})

            start = The starting value
            step  = 0 means don't increment or decrement.
                    For IP step = 0.0.0.1.  Increment on the last octet.
                                  0.0.1.0.  Increment on the third octet.
            direction = increment or decrement the starting value.

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/vxlan/{id}
        """
        if 'vxlan' not in obj:
            self.ixnObj.logInfo('\nCreate new VxLAN in NGPF')
            response = self.ixnObj.post(self.ixnObj.httpHeader+obj+'/vxlan')
            vxlanId = response.json()['links'][0]['href']
            self.ixnObj.logInfo('\ncreateVxlanNgpf: %s' % vxlanId)

        if 'vxlan' in obj:
            vxlanId = obj

        # Get VxLAN metadatas
        vxlanResponse = self.ixnObj.get(self.ixnObj.httpHeader+vxlanId)

        for key,value in kwargs.items():
            if key == 'vtepName':
                self.ixnObj.patch(self.ixnObj.httpHeader+vxlanId, data={'name': value})

            if key == 'vtepVni':
                multivalue = vxlanResponse.json()['vni']
                self.ixnObj.logInfo('\nConfiguring VxLAN attribute: %s: %s' % (key, value))
                data={'start':kwargs['vtepVni']['start'], 'step':kwargs['vtepVni']['step'], 'direction':kwargs['vtepVni']['direction']}
                self.configMultivalue(multivalue, 'counter', data=data)

            if key == 'vtepIpv4Multicast':
                self.ixnObj.logInfo('\nConfiguring VxLAN IPv4 multicast')
                multivalue = vxlanResponse.json()['ipv4_multicast']
                data={'start':kwargs['vtepIpv4Multicast']['start'], 'step':kwargs['vtepIpv4Multicast']['step'], 
                      'direction':kwargs['vtepIpv4Multicast']['direction']}
                self.configMultivalue(multivalue, 'counter', data=data)

        self.configuredProtocols.append(vxlanId)
        return vxlanId

    def configRsvpTeLsps(self, ipv4Obj):
        """
        Description
            Create new RSVP-TE LSPS Tunnel. A RSVP-TE interface is created automatically if there 
            is no RSVR-TE configured.

        Parameter
            ipv4Obj: <str>: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1

        Syntax
            POST: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/rsvpteLsps

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/rsvrteLsps/{id}
        """
        self.ixnObj.logInfo('\nCreating new RSVP TE LSPS')
        response = self.ixnObj.post(self.ixnObj.httpHeader+ipv4Obj+'/rsvpteLsps')
        return response.json()['links'][0]['href']
        
    def deleteRsvpTeLsps(self, rsvpTunnelObj):
        """
        Description
            Delete a RSVP-TE tunnel.
            Note: Deleting the last tunnel will also delete the RSVR-TE Interface.

        Parameter
            rsvrTunnelObj: <str>: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/rsvpteLsps/12

        Syntax
            DELETE: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/rsvpteLsps/{id}
        """
        self.ixnObj.delete(self.ixnObj.httpHeader+rsvpTunnelObj)

    def configNetworkGroup(self, **kwargs):
        """
        Description
            Create or modify a Network Group for network advertisement.

        Parameters
            deviceGroupObj: <str>: Optional: Device Group obj. For creating a new Network Group.
                            /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1

        Syntax
            POST: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/networkGroup
            POST: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/networkGroup/{id}/ipv4PrefixPools

        Example:
               Device Group object sample: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1
               configNetworkGroup(create=deviceGroupObj
                                  name='networkGroup1',
                                  multiplier = 100,
                                  networkAddress = {'start': '160.1.0.0', 'step': '0.0.0.1', 'direction': 'increment'},
                                  prefixLength = 24)

            To modify a Network Group:
               configNetworkGroup(modify=networkGroupObj,
                                  name='networkGroup-ospf',
                                  multiplier = 500,
                                  networkAddress = {'start': '200.1.0.0', 'step': '0.0.0.1', 'direction': 'increment'},
                                  prefixLength = 32)

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/networkGroup/{id}/ipv4PrefixPools/{id}
        """
        if 'create' not in kwargs and 'modify' not in kwargs:
            raise IxNetRestApiException('configNetworkGroup requires either a create or modify parameter.')

        if 'create' in kwargs:
            deviceGroupObj = kwargs['create']
            self.ixnObj.logInfo('\nCreating new Network Group')
            response = self.ixnObj.post(self.ixnObj.httpHeader+deviceGroupObj+'/networkGroup')
            networkGroupObj = response.json()['links'][0]['href']

        if 'modify' in kwargs:
            networkGroupObj = kwargs['modify']

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+networkGroupObj, data={'name': kwargs['name']})

        if 'multiplier' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+networkGroupObj, data={'multiplier': kwargs['multiplier']})

        if 'create' in kwargs:
            self.ixnObj.logInfo('\nCreate new Network Group IPv4 Prefix Pools')
            response = self.ixnObj.post(self.ixnObj.httpHeader+networkGroupObj+'/ipv4PrefixPools')
            ipv4PrefixObj = self.ixnObj.httpHeader + response.json()['links'][0]['href']
        else:
            ipv4PrefixObj = self.ixnObj.httpHeader+networkGroupObj+'/ipv4PrefixPools/1'

        # prefixPoolId = /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/networkGroup/3/ipv4PrefixPools/1
        response = self.ixnObj.get(ipv4PrefixObj)
        self.ixnObj.logInfo('\nConfig Network Group advertising routes')
        multivalue = response.json()['networkAddress']
        data={'start': kwargs['networkAddress']['start'],
              'step': kwargs['networkAddress']['step'],
              'direction': kwargs['networkAddress']['direction']}
        self.ixnObj.configMultivalue(multivalue, 'counter', data)

        if 'prefixLength' in kwargs:
            self.ixnObj.logInfo('\nConfig Network Group prefix pool length')
            response = self.ixnObj.get(ipv4PrefixObj)
            multivalue = response.json()['prefixLength']
            data={'value': kwargs['prefixLength']}
            self.ixnObj.configMultivalue(multivalue, 'singleValue', data)

        return ipv4PrefixObj

    def configMultivalue(self, multivalueUrl, multivalueType, data):
        """
        Description
           Configure multivalues.

        Parameters
           multivalueUrl: <str>: The multivalue: /api/v1/sessions/{1}/ixnetwork/multivalue/1
           multivalueType: <str>: counter|singleValue|valueList
           data: <dict>: singleValue: data={'value': '1.1.1.1'})
                             valueList:   data needs to be in a [list]:  data={'values': [list]}
                             counter:     data={'start': value, 'direction': increment|decrement, 'step': value}

        Syntax
            PATCH: /api/v1/sessions/{id}/ixnetwork/multivalue/{id}/singleValue
            PATCH: /api/v1/sessions/{id}/ixnetwork/multivalue/{id}/counter
            PATCH: /api/v1/sessions/{id}/ixnetwork/multivalue/{id}/valueList
        """
        if multivalueType == 'counter':
            # Examples: macAddress = {'start': '00:01:01:00:00:01', 'direction': 'increment', 'step': '00:00:00:00:00:01'}
            #          data=macAddress)
            self.ixnObj.patch(self.ixnObj.httpHeader+multivalueUrl+'/counter', data=data)

        if multivalueType == 'singleValue':
            # data={'value': value}
            self.ixnObj.patch(self.ixnObj.httpHeader+multivalueUrl+'/singleValue', data=data)

        if multivalueType == 'valueList':
            # data={'values': ['item1', 'item2']}
            self.ixnObj.patch(self.ixnObj.httpHeader+multivalueUrl+'/valueList', data=data)

    def getMultivalueValues(self, multivalueObj, silentMode=False):
        """
        Description
           Get the multivalue values.

        Parameters
           multivalueObj: <str>: The multivalue object: /api/v1/sessions/{1}/ixnetwork/multivalue/208
           silentMode: <bool>: True=Display the GET and status code. False=Don't display.
        
        Syntax
            /api/v1/sessions/{id}/ixnetwork/multivalue/{id}?includes=count

        Requirements
           self.ixnObj.waitForComplete()

        Returns
           The multivalue values
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader+multivalueObj+'?includes=count', silentMode=silentMode)
        count = response.json()['count']
        if silentMode == False:
            self.ixnObj.logInfo('\ngetMultivalueValues: {0} Count={1}'.format(multivalueObj, count))
        data = {'arg1': multivalueObj,
                'arg2': 0,
                'arg3': count
                }
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/multivalue/operations/getValues', data=data, silentMode=silentMode)
        self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/operations/multivalue/getValues'+response.json()['id'])
        return response.json()['result']

    def verifyProtocolSessionsUp(self, protocolViewName='BGP Peer Per Port', timeout=60):
        """
        Description
            Verify all specified protocols sessions for UP.

        Parameter
            protocolViewName: <str>: The protocol view name. Get this name from API browser or in IxNetwork GUI statistic tabs.
        
            timeout: <int>: The timeout value to declare as failed. Default = 60 seconds.

        protocolViewName options:
            'DHCPV4 Client Per Port'
            'DHCPV4 Server Per Port'
            'ISIS-L3 RTR Per Port'
            'BGP Peer Per Port'
            'OSPFv2-RTR Per Port'
        """
        totalSessionsDetectedUp = 0
        totalSessionsDetectedDown = 0
        totalPortsUpFlag = 0

        for counter in range(1,timeout+1):
            stats = self.statObj.getStats(viewName=protocolViewName, displayStats=False)
            totalPorts = len(stats.keys()) ;# Length stats.keys() represents total ports.
            self.ixnObj.logInfo('\nProtocolName: {0}'.format(protocolViewName))
            for session in stats.keys():
                sessionsUp = int(stats[session]['Sessions Up'])
                totalSessions = int(stats[session]['Sessions Total'])
                totalSessionsNotStarted = int(stats[session]['Sessions Not Started'])
                totalExpectedSessionsUp = totalSessions - totalSessionsNotStarted

                self.ixnObj.logInfo('\n\tPortName: {0}\n\t   TotalSessionsUp: {1}\n\t   ExpectedTotalSessionsup: {2}'.format(
                    stats[session]['Port'], sessionsUp, totalExpectedSessionsUp))

                if counter < timeout and sessionsUp != totalExpectedSessionsUp:
                    self.ixnObj.logInfo('\t   Session is still down')

                if counter < timeout and sessionsUp == totalExpectedSessionsUp:
                    totalPortsUpFlag += 1
                    if totalPortsUpFlag == totalPorts:
                        self.ixnObj.logInfo('\n\tAll sessions are up!')
                        return

            if counter == timeout and sessionsUp != totalExpectedSessionsUp:
                raise IxNetRestApiException('\nSessions failed to come up')

            self.ixnObj.logInfo('\n\tWait {0}/{1} seconds'.format(counter, timeout))
            print()
            time.sleep(1)

    def startAllOspfv2(self):
        """
        Description
            Start all OSPFv2.
        """
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': []},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',    'properties': [], 'where': []},
                              {'node': 'ipv4',        'properties': [], 'where': []},
                              {'node': 'ospfv2',      'properties': [], 'where': []}]
                    }
        queryResponse = self.ixnObj.query(data=queryData)
        for topologyObj in queryResponse.json()['result'][0]['topology']:
            for deviceGroupObj in topologyObj['deviceGroup']:
                if deviceGroupObj['ethernet'][0]['ipv4'][0]['ospfv2'] != []:
                    for ospfObj in deviceGroupObj['ethernet'][0]['ipv4'][0]['ospfv2']:
                        data = {'arg1': [ospfObj['href']]}
                        self.ixnObj.post(self.ixnObj.httpHeader+ospfObj['href']+'/operations/start', data=data)

    def startAllRsvpTeIf(self):
        """
        Description
            Start all RSVP-TE Interface.
        """
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': []},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',    'properties': [], 'where': []},
                              {'node': 'ipv4',        'properties': [], 'where': []},
                              {'node': 'rsvpteIf',    'properties': [], 'where': []}]
                    }
        queryResponse = self.ixnObj.query(data=queryData)
        for topologyObj in queryResponse.json()['result'][0]['topology']:
            for deviceGroupObj in topologyObj['deviceGroup']:
                if deviceGroupObj['ethernet'][0]['ipv4'][0]['rsvpteIf'] != []:
                    for rsvpTeIfObj in deviceGroupObj['ethernet'][0]['ipv4'][0]['rsvpteIf']:
                        data = {'arg1': [rsvpTeIfObj['href']]}
                        self.ixnObj.post(self.ixnObj.httpHeader+rsvpTeIfObj['href']+'/operations/start', data=data)

    def startAllRsvpTeLsps(self):
        """
        Description
            Start all RSVP-TE LSPS (Tunnels).
        """
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': []},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',    'properties': [], 'where': []},
                              {'node': 'ipv4',        'properties': [], 'where': []},
                              {'node': 'rsvpteLsps',    'properties': [], 'where': []}]
                    }
        queryResponse = self.ixnObj.query(data=queryData)
        for topologyObj in queryResponse.json()['result'][0]['topology']:
            for deviceGroupObj in topologyObj['deviceGroup']:
                if deviceGroupObj['ethernet'][0]['ipv4'][0]['rsvpteLsps'] != []:
                    for rsvpTeLspsObj in deviceGroupObj['ethernet'][0]['ipv4'][0]['rsvpteLsps']:
                        data = {'arg1': [rsvpTeLspsObj['href']]}
                        self.ixnObj.post(self.ixnObj.httpHeader+rsvpTeLspsObj['href']+'/operations/start', data=data)

    def verifyDeviceGroupStatus(self):
        queryData = {'from': '/',
                        'nodes': [{'node': 'topology', 'properties': [], 'where': []},
                                  {'node': 'deviceGroup', 'properties': ['href', 'enabled'], 'where': []},
                                  {'node': 'deviceGroup', 'properties': ['href', 'enabled'], 'where': []}]
                    }

        queryResponse = self.ixnObj.query(data=queryData)

        deviceGroupTimeout = 60
        for topology in queryResponse.json()['result'][0]['topology']:
            for deviceGroup in topology['deviceGroup']:
                deviceGroupObj = deviceGroup['href']
                response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroupObj, silentMode=False)
                # Verify if the Device Group is enabled. If not, don't go further.
                enabledMultivalue = response.json()['enabled']
                # touched
                enabled = self.ixnObj.getMultivalueValues(enabledMultivalue, silentMode=False)
                if enabled[0] == 'true':
                    for counter in range(1,deviceGroupTimeout+1):
                        response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroupObj, silentMode=False)
                        deviceGroupStatus = response.json()['status']
                        self.ixnObj.logInfo('\n%s' % deviceGroupObj)
                        self.ixnObj.logInfo('\tStatus: %s' % deviceGroupStatus)
                        if counter < deviceGroupTimeout and deviceGroupStatus != 'started':
                            self.ixnObj.logInfo('\tWaiting %d/%d seconds ...' % (counter, deviceGroupTimeout))
                            time.sleep(1)
                        if counter < deviceGroupTimeout and deviceGroupStatus == 'started':
                            break
                        if counter == deviceGroupTimeout and deviceGroupStatus != 'started':
                            raise IxNetRestApiException('\nDevice Group failed to start up')
                    
                    # Inner Device Group
                    if deviceGroup['deviceGroup'] != []:
                        innerDeviceGroupObj = deviceGroup['deviceGroup'][0]['href']
                        for counter in range(1,deviceGroupTimeout):
                            response = self.ixnObj.get(self.ixnObj.httpHeader+innerDeviceGroupObj, silentMode=True)
                            innerDeviceGroupStatus = response.json()['status']
                            self.ixnObj.logInfo('\n\tInnerDeviceGroup: %s' % innerDeviceGroupObj)
                            self.ixnObj.logInfo('\t   Status: %s' % innerDeviceGroupStatus)
                            if counter < deviceGroupTimeout and innerDeviceGroupStatus != 'started':
                                self.ixnObj.logInfo('\tWait %d/%d' % (counter, deviceGroupTimeout))
                                time.sleep(1)
                            if counter < deviceGroupTimeout and innerDeviceGroupStatus == 'started':
                                break
                            if counter == deviceGroupTimeout and innerDeviceGroupStatus != 'started':
                                raise IxNetRestApiException('\nInner Device Group failed to start up')
        print()

    def startAllProtocols(self):
        """
        Description
            Start all protocols in NGPF and verify all Device Groups are started.

        Syntax
            POST: /api/v1/sessions/{id}/ixnetwork/operations/startallprotocols
        """
        url = self.ixnObj.sessionUrl+'/operations/startallprotocols'
        response = self.ixnObj.post(url)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])
        self.verifyDeviceGroupStatus()

    def stopAllProtocols(self):
        """
        Description
            Stop all protocols in NGPF

        Syntax
            POST: /api/v1/sessions/{id}/ixnetwork/operations/stopallprotocols
        """
        url = self.ixnObj.sessionUrl+'/operations/stopallprotocols'
        response = self.ixnObj.post(url, data={'arg1': 'sync'})
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def startProtocol(self, protocolObj):
        """
        Description
            Start the specified protocol by its object handle.

        Parameters
            protocolObj: <str|obj>: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1
        
        Syntax
            POST: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1/operations/start
            DATA: {['arg1': [/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1']}
        """
        url = self.ixnObj.httpHeader+protocolObj+'/operations/start'
        response = self.ixnObj.post(url, data={'arg1': [protocolObj]})
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def stopProtocol(self, protocolObj):
        """
        Description
            Stop the specified protocol by its object handle.

        Parameters
            protocolObj: <str|obj>: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1

        Syntax
            POST: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1/operations/stop
            DATA: {['arg1': [/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1']}
        """
        url = self.ixnObj.httpHeader+protocolObj+'/operations/stop'
        response = self.ixnObj.post(url, data={'arg1': [protocolObj]})
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def startTopology(self, topologyObjList='all'):
        """
        Description
            Start a Topology Group and all of its protocol stacks.

        Parameters
            topologyObjList: <str>|<list>: 'all' or a list of Topology Group href.
                             Ex: ['/api/v1/sessions/1/ixnetwork/topology/1']
        """
        if topologyObjList == 'all':
            queryData = {'from': '/',
                         'nodes': [{'node': 'topology', 'properties': ['href'], 'where': []}]
                        }

           # QUERY FOR THE BGP HOST ATTRIBITE OBJECTS
            queryResponse = self.ixnObj.query(data=queryData)
            try:
                topologyList = queryResponse.json()['result'][0]['topology']
            except IndexError:
                raise IxNetRestApiException('\nNo Topology Group objects  found')

            topologyObjList = [topology['href'] for topology in topologyList]

        url = self.ixnObj.sessionUrl+'/topology/operations/start'
        response = self.ixnObj.post(url, data={'arg1': topologyObjList})
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])
        self.verifyDeviceGroupStatus()

    def stopTopology(self, topologyObjList='all'):
        """
        Description
            Stop the running Topology and all protocol sessions.

        Parameters
            topologyObjList: <list>: A list of Topology Group href.
                             Ex: ['/api/v1/sessions/1/ixnetwork/topology/1']
        """
        if topologyObjList == 'all':
            queryData = {'from': '/',
                         'nodes': [{'node': 'topology', 'properties': ['href'], 'where': []}]
                        }

           # QUERY FOR THE BGP HOST ATTRIBITE OBJECTS
            queryResponse = self.ixnObj.query(data=queryData)
            try:
                topologyList = queryResponse.json()['result'][0]['topology']
            except IndexError:
                raise IxNetRestApiException('\nNo Topology Group objects  found')

            topologyObjList = [topology['href'] for topology in topologyList]

        self.ixnObj.post(self.ixnObj.sessionUrl+'/topology/operations/stop', data={'arg1': topologyObjList})
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def startStopDeviceGroup(self, deviceGroupObjList='all', action='start'):
        """
        Description
            Start a Topology Group and all of its protocol stacks.

        Parameters
            topologyObjList: <str>|<list>: 'all' or a list of Topology Group href.
                             Ex: ['/api/v1/sessions/1/ixnetwork/topology/1']
        """
        if deviceGroupObjList == 'all':
            queryData = {'from': '/',
                         'nodes': [{'node': 'topology', 'properties': [], 'where': []},
                                   {'node': 'deviceGroup', 'properties': ['href'], 'where': []}]
                        }

            queryResponse = self.ixnObj.query(data=queryData)
            try:
                topologyGroupList = queryResponse.json()['result'][0]['topology']
            except IndexError:
                raise IxNetRestApiException('\nNo Device  Group objects  found')

            deviceGroupObjList = []
            for dg in topologyGroupList:
                for dgHref in  dg['deviceGroup']:
                    url = self.ixnObj.sessionUrl+'/topology/deviceGroup/operations/%s' % action
                    response = self.ixnObj.post(url, data={'arg1': dgHref['href'].split(' ')})
                    self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])
                    time.sleep(3)

    def verifyProtocolSessionsNgpf(self, protocolObjList=None, timeout=90):
        """
        Description
            Either verify the user specified protocol list to verify for session UP or verify
            the default object's self.configuredProtocols list that accumulates the emulation protocol object
            when it was configured.
            When verifying IPv4, this API will verify ARP failures and return you a list of IP interfaces
            that failed ARP.

        Parameters
            protocolObjList: <list>: A list of protocol objects.  Default = None.  The class will automatically verify all
                                     of the configured protocols.
                         Ex: ['/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1',
                              '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1',
                              '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1',
                              '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/ospfv2/1',]

            timeout: <int>: Total wait time for all the protocols in the provided list to come up.

        Syntaxes
            GET:  http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1
            RESPONSE:  [u'notStarted', u'notStarted', u'notStarted', u'notStarted', u'notStarted', u'notStarted']
            GET:  http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1
            RESPONSE:  [u'up', u'up', u'up', u'up', u'up', u'up', u'up', u'up']
            GET:  http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1
        """
        timerStop = timeout
        if protocolObjList is None:
            protocolObjList = self.configuredProtocols

        for eachProtocol in protocolObjList:
            # notStarted, up or down
            protocolName =  eachProtocol.split('/')[-2]
            for timer in range(1,timerStop+1):
                sessionStatus = self.getSessionStatus(eachProtocol)
                # ['up']
                response = self.ixnObj.get(self.ixnObj.httpHeader+eachProtocol, silentMode=True)
                # Started
                protocolSessionStatus = response.json()['status']

                self.ixnObj.logInfo('\nVerifyProtocolSessions: %s\n' % eachProtocol)
                print('\tprotocolSessionStatus:', protocolSessionStatus)
                print('\tsessionStatusResponse:', sessionStatus)
                if timer < timerStop:
                    if protocolSessionStatus != 'started':
                        self.ixnObj.logInfo('\tWait %s/%s seconds' % (timer, timerStop))
                        time.sleep(1)
                        continue

                    # Started
                    if 'up' not in sessionStatus:
                        self.ixnObj.logInfo('\tProtocol session is down: Wait %s/%s seconds' % (timer, timerStop))
                        time.sleep(1)
                        continue

                    if 'up' in sessionStatus:
                        self.ixnObj.logInfo('\tProtocol sessions are all up: {0}'.format(protocolName))
                        break

                if timer == timerStop:
                    if 'notStarted' in protocolSessionStatus:
                        raise IxNetRestApiException('\tverifyProtocolSessions: {0} session failed to start'.format(protocolName))
                        
                    if protocolSessionStatus == 'started' and 'down' in sessionStatus:
                        # Show ARP failures
                        if protocolName == 'ipv4':
                            ipInterfaceIndexList = []
                            index = 0
                            for eachSessionStatus in sessionStatus:
                                self.ixnObj.logInfo('eachSessionStatus index: {0} {1}'.format(eachSessionStatus, index))
                                if eachSessionStatus == 'down':
                                    ipInterfaceIndexList.append(index)
                                index += 1

                            ipMultivalue = response.json()['address']
                            ipAddressList = self.ixnObj.getMultivalueValues(ipMultivalue, silentMode=True)
                            self.ixnObj.logInfo('\nARP failed on IP interface:')
                            for eachIpIndex in ipInterfaceIndexList:
                                self.ixnObj.logInfo('\t{0}'.format(ipAddressList[eachIpIndex]))
                        else:
                            self.ixnObj.logInfo('\tverifyProtocolSessions: {0} session failed'.format(protocolName))

                        raise IxNetRestApiException('Verify protocol sessions failed: {0}'.format(protocolName))

    def verifyAllProtocolSessionsInternal(self, protocol, timeout=120, silentMode=True):
        """
        Description
            Verify protocol sessions for UP state.
            Initially created for verifyAllProtocolSessionsNgpf(), but this API will also work
            by passing in a protocol object.

        Parameters
           protocol: <str>: The protocol object to verify the session state.
           timeout: <int>: The timeout value for declaring as failed. Default = 120 seconds.
           silentMode: <bool>: True to not display less on the terminal.  False for debugging purpose.
        """
        sessionDownList = ['down', 'notStarted']
        startCounter = 1
        response = self.ixnObj.get(self.ixnObj.httpHeader+protocol, silentMode=silentMode)
        protocolActiveMultivalue = response.json()['active']
        response = self.ixnObj.getMultivalueValues(protocolActiveMultivalue, silentMode=silentMode)
        self.ixnObj.logInfo('\n%s' % protocol)
        self.ixnObj.logInfo('\tProtocol is enabled: %s' % response[0])
        if response[0] == 'false':
            return

        for timer in range(startCounter, timeout+1):
            currentStatus = self.getSessionStatus(protocol)
            self.ixnObj.logInfo('\n%s' % protocol)
            self.ixnObj.logInfo('\tTotal sessions: %d' % len(currentStatus))
            totalDownSessions = 0
            for eachStatus in currentStatus:
                if eachStatus != 'up':
                    totalDownSessions += 1
            self.ixnObj.logInfo('\tTotal sessions Down: %d' % totalDownSessions)

            if timer < timeout and [element for element in sessionDownList if element in currentStatus] == []:
                self.ixnObj.logInfo('\tProtocol sessions are all up')
                startCounter = timer
                break
            if timer < timeout and [element for element in sessionDownList if element in currentStatus] != []:
                self.ixnObj.logInfo('\tWait %d/%d seconds' % (timer, timeout))
                time.sleep(1)
                continue
            if timer == timeout and [element for element in sessionDownList if element in currentStatus] != []:
                raise IxNetRestApiException

    def verifyAllProtocolSessionsNgpf(self, timeout=120, silentMode=True):
        """
        Description
            Loop through each Topology Group and its enabled Device Groups and verify
            all the created and activated protocols for session up.
            Applies to Ethernet, IPv4 and IPv6.

        Parameters
           timeout: <int>: The timeout value for declaring as failed. Default = 120 seconds.
           silentMode: <bool>: True to not display less on the terminal.  False for debugging purpose.            
        """
        l2ProtocolList = ['isisL3', 'lacp', 'mpls']
        l3ProtocolList = ['ancp', 'bfdv4Interface', 'bgpIpv4Peer', 'bgpIpv6Peer', 'dhcpv4relayAgent', 'dhcpv6relayAgent',
                          'geneve', 'greoipv4', 'greoipv6', 'igmpHost', 'igmpQuerier',
                          'lac', 'ldpBasicRouter', 'ldpBasicRouterV6', 'ldpConnectedInterface', 'ldpv6ConnectedInterface',
                          'ldpTargetedRouter', 'ldpTargetedRouterV6', 'lns', 'mldHost', 'mldQuerier', 'ptp', 'ipv6sr',
                          'openFlowController', 'openFlowSwitch', 'ospfv2', 'ospfv3', 'ovsdbcontroller', 'ovsdbserver',
                          'pcc', 'pce', 'pcepBackupPCEs', 'pimV4Interface', 'pimV6Interface', 'ptp', 'rsvpteIf',
                          'rsvpteLsps', 'tag', 'vxlan']

        queryData = {'from': '/',
                        'nodes': [{'node': 'topology', 'properties': [], 'where': []},
                                  {'node': 'deviceGroup', 'properties': ['href'], 'where': []}]
                    }
        queryResponse = self.ixnObj.query(data=queryData)
        try:
            topologyGroupList = queryResponse.json()['result'][0]['topology']
        except IndexError:
            raise IxNetRestApiException('\nNo Device Group objects  found')

        deviceGroupObjList = []
        for topology in topologyGroupList:
            for deviceGroup in topology['deviceGroup']:
                deviceGroup = deviceGroup['href']
                response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroup)
                # Verify if the Device Group is enabled. If not, don't go further.
                enabledMultivalue = response.json()['enabled']
                response = self.ixnObj.getMultivalueValues(enabledMultivalue, silentMode=True)
                self.ixnObj.logInfo('\nDeviceGroup is enabled: %s'% response)
                if response[0] == 'false':
                    continue

                response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroup+'/ethernet', silentMode=silentMode)
                match = re.match('/api/v[0-9]+/sessions/[0-9]+/ixnetwork(.*)', deviceGroup)
                queryData = {'from': match.group(1),
                             'nodes': [{'node': 'ethernet', 'properties': [], 'where': []}]
                            }
                queryResponse = self.ixnObj.query(data=queryData)
                ethernetIds = queryResponse.json()['result'][0]['ethernet']
                ethernetList = [ethernet['href'] for ethernet in ethernetIds]

                for ethernet in ethernetList:
                    # Verify Layer2 first
                    for protocol in l2ProtocolList:
                        response = self.ixnObj.get(self.ixnObj.httpHeader+ethernet+'/'+protocol, silentMode=silentMode, ignoreError=True)
                        if response.json() == [] or 'errors' in response.json():
                            continue
                        currentProtocolList = ['%s/%s/%s' % (ethernet, protocol, str(i["id"])) for i in response.json()]
                        for currentProtocol in currentProtocolList:
                            if 'isis' in currentProtocol:
                                response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroup+'/isisL3Router', silentMode=silentMode)
                            self.verifyAllProtocolSessionsInternal(currentProtocol)

                    response = self.ixnObj.get(self.ixnObj.httpHeader+ethernet+'/ipv4', silentMode=silentMode)
                    ipv4List = ['%s/%s/%s' % (ethernet, 'ipv4', str(i["id"])) for i in response.json()]
                    response = self.ixnObj.get(self.ixnObj.httpHeader+ethernet+'/ipv6', silentMode=silentMode)
                    ipv6List = ['%s/%s/%s' % (ethernet, 'ipv6', str(i["id"])) for i in response.json()]
                    for layer3Ip in ipv4List+ipv6List:
                        for protocol in l3ProtocolList:
                            response = self.ixnObj.get(self.ixnObj.httpHeader+layer3Ip+'/'+protocol, silentMode=silentMode, ignoreError=True)
                            if response.json() == [] or 'errors' in response.json():
                                continue
                            currentProtocolList = ['%s/%s/%s' % (layer3Ip, protocol, str(i["id"])) for i in response.json()]
                            for currentProtocol in currentProtocolList:
                                self.verifyAllProtocolSessionsInternal(currentProtocol, silentMode=silentMode)

    def getIpObjectsByTopologyObject(self, topologyObj, ipType='ipv4'):
        """
        Description
           Get all the Topology's IPv4 or IPv6 objects based on the specified topology object.

        Parameters
           ipType = ipv4 or ipv6
        """
        ipObjList = []
        deviceGroupResponse = self.ixnObj.get(topologyObj+'/deviceGroup')
        deviceGroupList = ['%s/%s/%s' % (topologyObj, 'deviceGroup', str(i["id"])) for i in deviceGroupResponse.json()]
        for deviceGroup in deviceGroupList:
            response = self.ixnObj.get(deviceGroup+'/ethernet')
            ethernetList = ['%s/%s/%s' % (deviceGroup, 'ethernet', str(i["id"])) for i in response.json()]
            for ethernet in ethernetList:
                response = self.ixnObj.get(ethernet+'/{0}'.format(ipType))
                ipObjList = ['%s/%s/%s' % (ethernet, 'ipv4', str(i["id"])) for i in response.json()]
        return ipObjList

    def getAllTopologyList(self):
        """
        Description
           If Topology exists: Returns a list of created Topologies.

        Return
           If no Topology exists: Returns []
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/topology')
        topologyList = ['%s/%s/%s' % (self.ixnObj.sessionUrl, 'topology', str(i["id"])) for i in response.json()]
        return topologyList

    def clearAllTopologyVports(self):
        response = self.ixnObj.get(self.ixnObj.sessionUrl + "/topology")
        topologyList = ["%s%s" % (self.ixnObj.httpHeader, str(i["links"][0]["href"])) for i in response.json()]
        for topology in topologyList:
            self.ixnObj.patch(topology, data={"vports": []})

    def modifyTopologyPortsNgpf(self, topologyObj, portList, topologyName=None):
        """
        Description
           Add/remove Topology ports.

        Parameters
           topologyObj: <str>: The Topology Group object.
           portList: <list>: A list of all the ports that you want for the Topology even if the port exists in
                             the Topology.

           topologyName: <st>: The Topology Group name to modify.
           
        Requirements:
            1> You must have already connected all the required ports for your configuration. Otherwise,
               adding additional port(s) that doesn't exists in your configuration's assigned port list
               will not work.

            2> This API requires getVports()

        Examples
           topologyObj = '/api/v1/sessions/1/ixnetwork/topology/1'

           portList format = [(str(chassisIp), str(slotNumber), str(portNumber))]
               Example 1: [ ['192.168.70.10', '1', '1'] ]
               Example 2: [ ['192.168.70.10', '1', '1'], ['192.168.70.10', '2', '1'] ]
        """
        vportList = self.portMgmtObj.getVports(portList)
        if len(vportList) != len(portList):
            raise IxNetRestApiException('modifyTopologyPortsNgpf: There is not enough vports created to match the number of ports.')
        self.ixnObj.logInfo('\nvportList: %s' % vportList)
        topologyData = {'vports': vportList}
        response = self.ixnObj.patch(self.ixnObj.httpHeader+topologyObj, data=topologyData)

    def getTopologyPorts(self, topologyObj):
        """
        Description
            Get all the configured ports in the Topology.

        Parameter
            topologyObj: <str>: /api/v1/sessions/1/ixnetwork/topology/1

        Returns
            A list of ports: [('192.168.70.10', '1', '1') ('192.168.70.10', '1', '2')]
        """
        topologyResponse = self.ixnObj.get(self.ixnObj.httpHeader+topologyObj)
        vportList = topologyResponse.json()['vports']
        if vportList == []:
            self.ixnObj.logError('No vport is created')
            return 1
        self.ixnObj.logInfo('vportList: %s' % vportList)
        portList = []
        for vport in vportList:
            response = self.ixnObj.get(self.ixnObj.httpHeader+vport)
            # 192.168.70.10:1:1
            currentPort = response.json()['assignedTo']
            chassisIp = currentPort.split(':')[0]
            card = currentPort.split(':')[1]
            port = currentPort.split(':')[2]
            portList.append((chassisIp, card, port))
        return portList

    def sendArpNgpf(self, ipv4ObjList):
        """
        Description
            Send ARP out of all the IPv4 objects that you provide in a list.

        ipv4ObjList: <str>:  Provide a list of one or more IPv4 object handles to send arp.
                      Ex: ["/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1"]
        """
        if type(ipv4ObjList) != list:
            raise IxNetRestApiException('sendArpNgpf error: The parameter ipv4ObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl+'/topology/deviceGroup/ethernet/ipv4/operations/sendarp'
        data = {'arg1': ipv4ObjList}
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def sendPing(self, srcIpList=None, destIp=None):
        """
        Description
            Send PING from the the list of srcIp to destIp.  This function will query for the IPv4
            object that has the srcIp address.

        Parameters
            srcIpList: <list>: The srcIp addresses in a list.  Could be 1 or more src IP addresses, but must
                       be in a list.  This API will look up the IPv4 object that has the srcIp.
            destIp: <str>: The destination IP to ping.

        Returns
            Success: 1 requests sent, 1 replies received.
            Failed: Ping: 1.1.1.1 -> 1.1.1.10 failed - timeout
            0: Returns 0 if no src IP address found in the srcIpList.
        """
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': []},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',    'properties': [], 'where': []},
                              {'node': 'ipv4',        'properties': ['address', 'count'], 'where': []}]
                    }
        url = self.ixnObj.sessionUrl+'/topology/deviceGroup/ethernet/ipv4/operations/sendping'
        queryResponse = self.ixnObj.query(data=queryData)
        srcIpIndexList = []
        noSrcIpIndexFound = []
        for topology in queryResponse.json()['result'][0]['topology']:
            for ipv4 in topology['deviceGroup'][0]['ethernet'][0]['ipv4']:
                ipv4Obj = ipv4['href']
                ipv4Count = ipv4['count']
                ipv4AddressMultivalue = ipv4['address']
                ipv4AddressList = self.ixnObj.getMultivalueValues(ipv4AddressMultivalue)
                url = self.ixnObj.httpHeader+ipv4Obj+'/operations/sendping'
                for eachSrcIp in srcIpList:
                    # Don't error out if eachSrcIp is not found in the ipv4AddressList because
                    # it may not be in the current for loop topology.
                    try:
                        srcIpIndex = ipv4AddressList.index(eachSrcIp)
                        srcIpIndexList.append(srcIpIndex+1)
                    except:
                        noSrcIpIndexFound.append(eachSrcIp)
                        pass
                if srcIpIndexList != []:
                    data = {'arg1': ipv4Obj, 'arg2': destIp, 'arg3': srcIpIndexList}
                    response = self.ixnObj.post(url, data=data)
                    self.ixnObj.waitForComplete(response, url+response.json()['id'])
                    self.ixnObj.logInfo(response.json()['result'][0]['arg3'])
                    if noSrcIpIndexFound != []:
                        self.ixnObj.logError('No srcIp address found in configuration: {0}'.format(noSrcIpIndexFound))
                    return response.json()['result'][0]['arg3']

                # Reset these variable to empty list.
                srcIpIndexList = []
                noSrcIpIndexFound = []
        if srcIpIndexList == []:
            raise IxNetRestApiException('No srcIp addresses found in configuration: {0}'.format(srcIpList))

    def verifyNgpfProtocolStarted(self, protocolObj, timeout=30):
        """
        Description
           Verify if NGPF protocol started.

        Parameter
           protocolObj: <str>: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1
           timeout: <int>: The timeout value. Default=30 seconds.
        """
        for counter in range(1,timeout+1):
            sessionStatus = self.getSessionStatus(protocolObj)
            self.ixnObj.logInfo('\n%s' % protocolObj)
            self.ixnObj.logInfo('\tSessionStatus: %s' % sessionStatus)
            if counter < timeout and 'notStarted' in sessionStatus:
                self.ixnObj.logInfo('\tWait %d/%d seconds' % (counter, timeout))
                time.sleep(1)

            if counter == timeout and 'notStarted' in sessionStatus:
                raise IxNetRestApiException('Protocol sessions failed to start')

            if counter < timeout and 'notStarted' not in sessionStatus:
                self.ixnObj.logInfo('\tProtocol sessions all started')
                return

    def deviceGroupProtocolStackNgpf(self, deviceGroupObj, ipType, arpTimeout=60, silentMode=True):
        """
        Description
            This API is an internal API for VerifyArpNgpf.
            It's created because each deviceGroup has IPv4/IPv6 and
            a deviceGroup could have inner deviceGroup that has IPv4/IPv6.
            Therefore, you can loop device groups.

        Parameters
            deviceGroupObj: <str>: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1
            ipType: <str>: ipv4|ipv6
            arpTimeout:  <int>: Timeout value. Default=60 seconds.

        Requires
            self.verifyNgpfProtocolStarted()
        """
        unresolvedArpList = []
        response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroupObj+'/ethernet', silentMode=silentMode)
        ethernetObjList = ['%s/%s/%s' % (deviceGroupObj, 'ethernet', str(i["id"])) for i in response.json()]
        for ethernetObj in ethernetObjList:
            response = self.ixnObj.get(self.ixnObj.httpHeader+ethernetObj+'/'+ipType, ignoreError=True, silentMode=silentMode)
            if response.status_code != 200:
                self.ixnObj.logInfo('deviceGroupProtocolStackNgpf: %s' % response.text)
                raise IxNetRestApiException(response.text)
            ipProtocolList = ['%s/%s/%s' % (ethernetObj, ipType, str(i["id"])) for i in response.json()]

            for ipProtocol in ipProtocolList:
                # match.group(1): /topology/1/deviceGroup/1/deviceGroup/1/ethernet/1/ipv4/1
                match = re.match('.*(/topology.*)', ipProtocol)
                # sessionStatus could be: down, up, notStarted
                self.verifyNgpfProtocolStarted(ipProtocol)
                self.ixnObj.logInfo('')

                for counter in range(1,arpTimeout+1):
                    sessionStatus = self.getSessionStatus(ipProtocol)
                    self.ixnObj.logInfo('\tARP SessionStatus: %s' % sessionStatus)
                    if counter < arpTimeout and 'down' in sessionStatus:
                        self.ixnObj.logInfo('\tARP is not resolved yet. Wait %d/%d' % (counter, arpTimeout))
                        time.sleep(1)
                        continue
                    if counter < arpTimeout and 'down' not in sessionStatus:
                        break
                    if counter == arpTimeout and 'down' in sessionStatus:
                        #raise IxNetRestApiException('\nARP is not getting resolved')
                        # Let it flow down to get the unresolved ARPs
                        pass

                protocolResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipProtocol+'?includes=resolvedGatewayMac',
                                                   ignoreError=True, silentMode=silentMode)
                resolvedGatewayMac = protocolResponse.json()['resolvedGatewayMac']

                # sessionStatus: ['up', 'up']
                # resolvedGatewayMac ['00:0c:29:8d:d8:35', '00:0c:29:8d:d8:35']

                # Only care for unresolved ARPs.
                # resolvedGatewayMac: 00:01:01:01:00:01 00:01:01:01:00:02 removePacket[Unresolved]
                # Search each mac to see if they're resolved or not.
                for index in range(0, len(resolvedGatewayMac)):
                    if (bool(re.search('.*Unresolved.*', resolvedGatewayMac[index]))):
                        multivalue = protocolResponse.json()['address']
                        multivalueResponse = self.ixnObj.getMultivalueValues(multivalue, silentMode=silentMode)
                        # Get the IP Address of the unresolved mac address
                        srcIpAddrNotResolved = multivalueResponse[index]
                        gatewayMultivalue = protocolResponse.json()['gatewayIp']
                        response = self.ixnObj.getMultivalueValues(gatewayMultivalue, silentMode=silentMode)
                        gatewayIp = response[index]
                        self.ixnObj.logInfo('\tFailed to resolve ARP: srcIp:{0} gateway:{1}'.format(srcIpAddrNotResolved, gatewayIp))
                        unresolvedArpList.append((srcIpAddrNotResolved, gatewayIp))

        if unresolvedArpList == []:
            self.ixnObj.logInfo('\tARP is resolved')
            return 0
        else:
            return unresolvedArpList

    def verifyArp(self, ipType='ipv4', silentMode=True):
        """
        Description
            Verify for ARP resolvement on every enabled Device Group including inner Device Groups.

            How it works:
               Each device group has a list of $sessionStatus: up, down or notStarted.
               If the deviceGroup has sessionStatus as "up", then ARP will be verified.
               It also has a list of $resolvedGatewayMac: MacAddress or removePacket[Unresolved]
               These two $sessionStatus and $resolvedGatewayMac lists are aligned.
               If lindex 0 on $sessionSatus is up, then $resolvedGatewayMac on index 0 expects
               to have a mac address.  Not removePacket[Unresolved].
               If not, then arp is not resolved.

        Requires
           self.deviceGroupProtocolStacksNgpf() 
           self.verifyNgpfProtocolStarted()

        Parameter
            ipType:  ipv4 or ipv6
            silentMode: <bool>: True to show less display on the terminal. False for debugging purposes.
        """
        self.ixnObj.logInfo('\nVerify ARP: %s' % ipType)
        unresolvedArpList = []
        startFlag = 0
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': [], 'where': []},
                              {'node': 'deviceGroup', 'properties': [], 'where': []}
                    ]}
        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
        for topology in queryResponse.json()['result'][0]['topology']:
            for deviceGroup in topology['deviceGroup']:
                deviceGroupObj = deviceGroup['href']

                response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroupObj, silentMode=silentMode)
                # Verify if the Device Group is enabled. If not, don't go further.
                enabledMultivalue = response.json()['enabled']
                response = self.ixnObj.getMultivalueValues(enabledMultivalue, silentMode=silentMode)
                if response[0] == 'false':
                    continue

                timeout = 30
                for counter in range(1,timeout+1):
                    response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroupObj, silentMode=silentMode)
                    deviceGroupStatus = response.json()['status']
                    self.ixnObj.logInfo('\n%s' % deviceGroupObj)
                    if deviceGroupStatus == 'notStarted':
                        raise IxNetRestApiException('\nDevice Group is not started.')

                    if counter < timeout and deviceGroupStatus == 'starting':
                        self.ixnObj.logInfo('\tWait %d/%d' % (counter, timeout))
                        time.sleep(1)
                        continue
                    if counter < timeout and deviceGroupStatus in ['started', 'mixed']:
                        break
                    if counter == timeout and deviceGroupStatus not in ['started', 'mixed']:
                        raise IxNetRestApiException('\nDevice Group failed to come up')

                if deviceGroupStatus in ['started', 'mixed']:
                    startFlag = 1
                    arpResult = self.deviceGroupProtocolStackNgpf(deviceGroupObj, ipType, silentMode=silentMode)
                    if arpResult != 0:
                        unresolvedArpList = unresolvedArpList + arpResult

                    response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroupObj+'/deviceGroup', silentMode=silentMode)
                    if response.status_code == 200 and response.json() != []:
                        innerDeviceGroupObj = response.json()[0]['links'][0]['href']
                        self.ixnObj.logInfo('\n%s' % self.ixnObj.httpHeader+innerDeviceGroupObj)
                        response = self.ixnObj.get(self.ixnObj.httpHeader+innerDeviceGroupObj, silentMode=silentMode)
                        deviceGroupStatus1 = response.json()['status']
                        self.ixnObj.logInfo('\tdeviceGroup Status: %s' % deviceGroupStatus1)

                        if deviceGroupStatus == 'started':
                            arpResult = self.deviceGroupProtocolStackNgpf(innerDeviceGroupObj, ipType, silentMode=silentMode)
                            if arpResult != 0:
                                unresolvedArpList = unresolvedArpList + arpResult

        if unresolvedArpList == [] and startFlag == 1:
            return 0
        if unresolvedArpList == [] and startFlag == 0:
            return 1
        if unresolvedArpList != [] and startFlag == 1:
            print()
            raise IxNetRestApiException

    def getNgpfGatewayIpMacAddress(self, gatewayIp):
        """
        Description
            Get the NGPF gateway IP Mac Address. The IPv4
            session status must be UP.

        Parameter
            gatewayIp: <str>: The gateway IP address.

        Return:
            - 0: No Gateway IP address found.
            - removePacket[Unresolved]
            - The Gateway IP's Mac Address.
        """
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': [], 'where': []},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',  'properties': [], 'where': []},
                              {'node': 'ipv4',  'properties': ['gatewayIp'], 'where': []}
                    ]}
        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
        for topology in queryResponse.json()['result'][0]['topology']:
            for deviceGroup in topology['deviceGroup']:
                try:
                    # Getting in here means IPv4 session status is UP.
                    ipv4Href = deviceGroup['ethernet'][0]['ipv4'][0]['href']
                    ipv4SessionStatus = self.getSessionStatus(ipv4Href)
                    gatewayIpMultivalue = deviceGroup['ethernet'][0]['ipv4'][0]['gatewayIp']
                    self.ixnObj.logInfo('\n\t%s' % ipv4Href)
                    self.ixnObj.logInfo('\tIPv4 sessionStatus: %s' % ipv4SessionStatus)
                    self.ixnObj.logInfo('\tGatewayIpMultivalue: %s' % gatewayIpMultivalue)
                    response = self.ixnObj.getMultivalueValues(gatewayIpMultivalue)
                    valueList = response
                    
                    self.ixnObj.logInfo('gateway IP: %s' % valueList)
                    if gatewayIp in valueList:
                        gatewayIpIndex = valueList.index(gatewayIp)
                        self.ixnObj.logInfo('\nFound gateway: %s ; Index:%s' % (gatewayIp, gatewayIpIndex))

                        queryData = {'from': deviceGroup['ethernet'][0]['href'],
                                    'nodes': [{'node': 'ipv4',  'properties': ['gatewayIp', 'resolvedGatewayMac'], 'where': []}
                                    ]}
                        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
                        response = self.ixnObj.get(self.ixnObj.httpHeader+ipv4Href+'?includes=resolvedGatewayMac')
                        gatewayMacAddress = response.json()['resolvedGatewayMac']
                        self.ixnObj.logInfo('\ngatewayIpMacAddress: %s' % gatewayMacAddress)
                        if 'Unresolved' in gatewayMacAddress:
                            raise IxNetRestApiException('Gateway Mac Address is unresolved.')
                        return gatewayMacAddress[0]
                        
                except:
                    pass
        return 0


    def getDeviceGroupSrcIpGatewayIp(self, srcIpAddress):
        """
        Description
            Search each Topology's Device Group for the provided srcIpAddress.
            If found, get the gateway IP address.

        Parameter
           srcIpAddress: <str>: The source IP address.

        Returns
            0: Failed. No srcIpAddress found in any Device Group.
            Gateway IP address
        """
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': [], 'where': []},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',  'properties': [], 'where': []},
                              {'node': 'ipv4',  'properties': ['address', 'gatewayIp'], 'where': []},
                              ]}

        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
        for topology in queryResponse.json()['result'][0]['topology']:
            for deviceGroup in topology['deviceGroup']:
                try:
                    srcIpMultivalue = deviceGroup['ethernet'][0]['ipv4'][0]['address']
                    gatewayIpMultivalue = deviceGroup['ethernet'][0]['ipv4'][0]['gatewayIp']
                    response = self.ixnObj.getMultivalueValues(srcIpMultivalue)
                    srcIp = response[0]
                    if srcIpAddress == srcIp:
                        self.ixnObj.logInfo('\nFound srcIpAddress: %s. Getting Gatway IP address ...' % srcIpAddress)
                        response = self.ixnObj.getMultivalueValues(gatewayIpMultivalue)
                        gatewayIp = response[0]
                        self.ixnObj.logInfo('\nGateway IP address: %s' % gatewayIp)
                        return gatewayIp
                except:
                    pass
        return 0

    def getDeviceGroupObjBySrcIp(self, srcIpAddress):
        """
        Description
            Search each Topology's Device Group for the srcIpAddress.
            If found, return the Device Group object.
            Mainly used for Traffic Item source/destination endpoints.

            if srcIpAddress is IPv6, the format must match what is shown
            in the GUI or API server.  Please verify how the configured 
            IPv6 format looks like on either the GUI or API server when you
            are testing your script during development.

        Parameter
           srcIpAddress: <str>: The source IP address.

        Returns
            0: Failed. No srcIpAddress found in any Device Group.
            deviceGroup Object: The Device Group object
        """
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': [], 'where': []},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',  'properties': [], 'where': []},
                              {'node': 'ipv4',  'properties': ['address'], 'where': []},
                              {'node': 'ipv6',  'properties': ['address'], 'where': []}
                              ]}

        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
        for topology in queryResponse.json()['result'][0]['topology']:
            for deviceGroup in topology['deviceGroup']:
                for ethernet in deviceGroup['ethernet']:
                    try:
                        if bool(re.match(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', srcIpAddress)):
                            srcIpMultivalue = ethernet['ipv4'][0]['address']
                        else:
                            # IPv6 format: ['2000:0:0:1:0:0:0:2', '2000:0:0:2:0:0:0:2', '2000:0:0:3:0:0:0:2', '2000:0:0:4:0:0:0:2']
                            srcIpMultivalue = ethernet['ipv6'][0]['address']

                        response = self.ixnObj.getMultivalueValues(srcIpMultivalue)
                        if srcIpAddress in response:
                            self.ixnObj.logInfo('\nFound srcIpAddress: %s' % srcIpAddress)
                            return deviceGroup['href']
                    except:
                        pass
        return 0

    def getNetworkGroupObjByIp(self, ipAddress):
        """
        Description
            Search each Device Group's Network Group for the ipAddress.
            If found, return the Network Group object.
            Mainly used for Traffic Item source/destination endpoints.

            The ipAddress cannot be a range. It has to be an actual IP address
            within the range.

        Parameter
           ipAddress: <str>: The network group IP address.

        Returns
            0: Failed. No ipAddress found in any NetworkGroup.
            network group Object: The Network Group object.
        """
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': [], 'where': []},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'networkGroup',  'properties': [], 'where': []},
                              {'node': 'ipv4PrefixPools',  'properties': ['networkAddress'], 'where': []},
                              {'node': 'ipv6PrefixPools',  'properties': ['networkAddress'], 'where': []}
                              ]}

        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)

        if '.' in ipAddress:
            prefixPoolType = 'ipv4PrefixPools'
        if ':' in ipAddress:
            prefixPoolType = 'ipv6PrefixPools'

        for topology in queryResponse.json()['result'][0]['topology']:
            for deviceGroup in topology['deviceGroup']:
                for networkGroup in deviceGroup['networkGroup']:
                    for prefixPool in networkGroup[prefixPoolType]:
                        prefixPoolRangeMultivalue = prefixPool['networkAddress']
                        response = self.ixnObj.getMultivalueValues(prefixPoolRangeMultivalue)
                        if ipAddress in response:
                            return networkGroup['href']

        return 0

    def getIpAddrIndexNumber(self, ipAddress):
        """
        Description
            Get the index ID of the IP address.

        Parameter
            ipAddress: <str>: The IP address to search for its index .
        """
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': [], 'where': []},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',  'properties': [], 'where': []},
                              {'node': 'ipv4',  'properties': ['address'], 'where': []},
                              {'node': 'ipv6',  'properties': ['address'], 'where': []},
                              ]}

        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
        if '.' in ipAddress:
            multivalue = queryResponse.json()['result'][0]['topology']
        if ':' in ipAddress:
            multivalue = queryResponse.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv6'][0]['address']

        response = self.ixnObj.get(self.ixnObj.httpHeader+multivalue)
        valueList = response.json()['values']
        index = response.json()['values'].index(ipAddress)
        return index

    def getIpv4ObjByPortName(self, portName=None):
        """
        Description
            Get the IPv4 object by the port name.

        Parameter
            portName: <str>: Optional: The name of the port.  Default=None.
        """
        # Step 1 of 3: Get the Vport by the portName.
        queryData = {'from': '/',
                    'nodes': [{'node': 'vport', 'properties': ['name'], 'where': [{'property': 'name', 'regex': portName}]}]}

        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
        if queryResponse.json()['result'][0]['vport'] == []:
            raise IxNetRestApiException('\nNo such vport name: %s\n' % portName)

        # /api/v1/sessions/1/ixnetwork/vport/2
        vport = queryResponse.json()['result'][0]['vport'][0]['href']
        self.ixnObj.logInfo(vport)

        # Step 2 of 3: Query the API tree for the IPv4 object
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['vports'], 'where': []},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',  'properties': [], 'where': []},
                              {'node': 'ipv4',  'properties': [], 'where': []},
                              ]}

        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)

        # Step 3 of 3: Loop through each Topology looking for the vport.
        #              If found, get its IPv4 object
        for topology in queryResponse.json()['result'][0]['topology']:
            if vport in topology['vports']:
                # Get the IPv4 object: /api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4/1
                ipv4Obj = topology['deviceGroup'][0]['ethernet'][0]['ipv4'][0]['href']
                return ipv4Obj

    def activateIgmpHostSession(self, portName=None, ipAddress=None, activate=True):
        """
        Description
            Active or deactivate the IGMP host session ID by the portName and IPv4 host address.

        Parameters:
            portName: <str>: The name of the port in which this API will search in all the Topology Groups.
            ipAddress: <str>: Within the Topology Group, the IPv4 address for the IGMP host.
            activate: <bool>: To activate or not to activate.
        """
        # Get the IPv4 address index.  This index position is the same index position for the IGMP host sessionID.
        # Will use this variable to change the value of the IGMP host object's active valueList.
        ipv4AddressIndex = self.getIpAddrIndexNumber(ipAddress)

        # Get the IPv4 object by the port name. This will search through all the Topology Groups for the portName.
        ipv4Obj = self.getIpv4ObjByPortName(portName=portName)

        # With the ipv4Obj, get the IGMP host object's "active" multivalue so we could modify the active valueList.
        queryData = {'from': ipv4Obj,
                    'nodes': [{'node': 'igmpHost', 'properties': ['active'], 'where': []}]}

        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
        if queryResponse.json()['result'][0]['igmpHost'] == []:
            raise IxNetRestApiException('\nNo IGMP HOST found\n')

        igmpHostActiveMultivalue = queryResponse.json()['result'][0]['igmpHost'][0]['active']

        response = self.ixnObj.get(self.ixnObj.httpHeader+igmpHostActiveMultivalue)
        valueList = response.json()['values']
        # Using the ipv4 address index, activate the IGMP session ID which is the same index position.
        valueList[ipv4AddressIndex] = activate
        self.ixnObj.configMultivalue(igmpHostActiveMultivalue, multivalueType='valueList', data={'values': valueList})

    def enableDeviceGroup(self, deviceGroupObj=None, enable=True):
        """
        Description
            Enable or disable a Device Group by the object handle.  A Device Group could contain many interfaces.
            This API will enable or disable all the interfaces.

        Parameters
            deviceGroupObj: The Device Group object handle: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1

            enable: True|False
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader + deviceGroupObj)
        enabledMultivalue = response.json()['enabled']
        self.ixnObj.configMultivalue(enabledMultivalue, multivalueType='singleValue', data={'value': enable})

    def getRouteRangeAddressProtocolAndPort(self, routeRangeAddress):
        """
        Description
            Using the specified route range address, return the associated protocol and port.

        Parameter
            routeRangeAddress: The route range address.

        Returns
            [portList, protocolList] ->  (['192.168.70.11:2:1'], ['ospf', 'isisL3'])
        """
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['vports'], 'where': []},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'networkGroup',  'properties': [], 'where': []},
                              {'node': 'ipv4PrefixPools',  'properties': ['networkAddress'], 'where': []},
                              {'node': 'bgpIPRouteProperty',  'properties': [], 'where': []},
                              {'node': 'ospfRouteProperty',  'properties': [], 'where': []},
                              {'node': 'isisL3RouteProperty',  'properties': ['active'], 'where': []},
                              {'node': 'ldpFECProperty',  'properties': ['active'], 'where': []}
                          ]}
        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
        discoveryFlag = 0
        protocolList = []
        portList = []
        for topology in queryResponse.json()['result'][0]['topology']:
            portList = self.ixnObj.getPhysicalPortFromVport(topology['vports'])
            for networkGroup in topology['deviceGroup'][0]['networkGroup']:
                for ipv4PrefixPool in networkGroup['ipv4PrefixPools']:
                    networkAddressList = self.ixnObj.getMultivalueValues(ipv4PrefixPool['networkAddress'])
                    if routeRangeAddress in networkAddressList:
                        if ipv4PrefixPool['bgpIPRouteProperty'] != []:
                            protocolList.append('bgp')
                        if ipv4PrefixPool['ospfRouteProperty'] != []:
                            protocolList.append('ospf')
                        if ipv4PrefixPool['isisL3RouteProperty'] != []:
                            protocolList.append('isisL3')
                        if ipv4PrefixPool['ldpFECProperty'] != []:
                            protocolList.append('ldp')

        return portList,protocolList

    def activateRouterIdProtocol(self, routerId, protocol=None, activate=True):
        """
        Description
            Activate the protocols based on the RouterId.
            This API will disabled all Device Groups within a Topology Group and enable only the
            Device Group that has the specified router ID in it.

        Parameter
            routerId: The router Id address to enable|disable
            activate: True|False. The protocol to activate|disactivate.
            protocol: The protocol to activate.
                      Current choices: bgpIpv4Peer, bgpIpv6Peer, igmpHost, igmpQuerier,
                                       mldHost, mldQuerier, pimV6Interface, ospfv2, ospfv3, isisL3
        """
        if type(routerId) is list:
            routerId = routerId[0]
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': [], 'where': []},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'routerData',  'properties': ['routerId'], 'where': []},
                              {'node': 'ethernet',  'properties': [], 'where': []},
                              {'node': 'ipv4',  'properties': [], 'where': []},
                              {'node': 'ipv6',  'properties': [], 'where': []},
                              {'node': protocol,  'properties': ['active'], 'where': []}
                          ]}

        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)

        # Get the Device Group object that contains the RouterId
        # and search for configured protocols.
        protocolList = []
        foundRouterIdFlag = 0
        for topology in queryResponse.json()['result'][0]['topology']:
            for deviceGroup in topology['deviceGroup']:
                deviceGroupHref = deviceGroup['href']
                routerIdMultivalue = deviceGroup['routerData'][0]['routerId']
                routerIdList = self.ixnObj.getMultivalueValues(routerIdMultivalue, silentMode=True)
                self.ixnObj.logInfo('\nactivateRouterIdProtocols: Querying DeviceGroup for routerId %s: %s' % (routerId, protocol))
                self.ixnObj.logInfo('routerIdList: {0}'.format(routerIdList))
                # response: ["192.0.0.1", "192.0.0.2", "192.0.0.3", "192.0.0.4","192.1.0.1"]
                if routerId in routerIdList:
                    foundRouterIdFlag = 1
                    self.ixnObj.logInfo('\nFound routerId %s' %  routerId)
                    routerIdIndex = routerIdList.index(routerId)
                    self.ixnObj.logInfo('routerId index: %s' % routerIdIndex)

                    if protocol == 'isisL3' and deviceGroup['ethernet'][0]['isisL3'] != []:
                        protocolList.append(deviceGroup['ethernet'][0]['isisL3'][0]['active'])

                    if deviceGroup['ethernet'][0]['ipv4'] != []:
                        if protocol == 'igmpHost' and deviceGroup['ethernet'][0]['ipv4'][0]['igmpHost'] != []:
                            protocolList.append(deviceGroup['ethernet'][0]['ipv4'][0]['igmpHost'][0]['active'])
                        if protocol == 'igmpQuerier' and deviceGroup['ethernet'][0]['ipv4'][0]['igmpQuerier'] != []:
                            protocolList.append(deviceGroup['ethernet'][0]['ipv4'][0]['igmpQuerier'][0]['active'])
                        if protocol == 'bgpIpv4Peer' and deviceGroup['ethernet'][0]['ipv4'][0]['bgpIpv4Peer'] != []:
                            protocolList.append(deviceGroup['ethernet'][0]['ipv4'][0]['bgpIpv4Peer'][0]['active'])
                        if protocol == 'ospfv2' and deviceGroup['ethernet'][0]['ipv4'][0]['ospfv2'] != []:
                            protocolList.append(deviceGroup['ethernet'][0]['ipv4'][0]['ospfv2'][0]['active'])

                    if deviceGroup['ethernet'][0]['ipv6'] != []:
                        if protocol == 'pimV6Interface' and deviceGroup['ethernet'][0]['ipv6'][0]['pimV6Interface'] != []:
                            protocolList.append(deviceGroup['ethernet'][0]['ipv6'][0]['pimV6Interface'][0]['active'])
                        if protocol == 'bgpIpv6Peer' and deviceGroup['ethernet'][0]['ipv6'][0]['bgpIpv6Peer'] != []:
                            protocolList.append(deviceGroup['ethernet'][0]['ipv6'][0]['bgpIpv6Peer'][0]['active'])
                        if protocol == 'ospfv3' and deviceGroup['ethernet'][0]['ipv6'][0]['ospfv3'] != []:
                            protocolList.append(deviceGroup['ethernet'][0]['ipv6'][0]['ospfv3'][0]['active'])
                        if protocol == 'mldHost' and deviceGroup['ethernet'][0]['ipv6'][0]['mldHost'] != []:
                            protocolList.append(deviceGroup['ethernet'][0]['ipv6'][0]['mldHost'][0]['active'])
                        if protocol == 'mldQuerier' and deviceGroup['ethernet'][0]['ipv6'][0]['mldQuerier'] != []:
                            protocolList.append(deviceGroup['ethernet'][0]['ipv6'][0]['mldQuerier'][0]['active'])

                    for protocolActiveMultivalue in protocolList:
                        try:
                            protocolActiveList = self.ixnObj.getMultivalueValues(protocolActiveMultivalue)
                            self.ixnObj.logInfo('\ncurrentValueList: %s' % protocolActiveList)
                            protocolActiveList[routerIdIndex] = str(activate).lower()
                            self.ixnObj.logInfo('updatedValueList: %s' % protocolActiveList)
                            self.ixnObj.configMultivalue(protocolActiveMultivalue, multivalueType='valueList',
                                                  data={'values': protocolActiveList})
                        except:
                            pass
                    return

        if foundRouterIdFlag == 0:
            raise Exception ('\nNo RouterID found in any Device Group: %s' % routerId)

    def activateRouterIdRouteRanges(self, protocol=None, routeRangeAddressList=None, activate=True):
        """
        Description
            Activate the protocols based on the RouterId.

        Parameter
            protocol: The protocol to disable/enable route ranges.
                      Current choices: bgp, ospf, ldp, isis

            routeRangeAddress: A list of two lists grouped in a list:
                               For example: [[[list_of_routerID], [list_of_route_ranges]]]

            activate: True|False

        Examples:
            1> activateRouterIdRouteRanges(routeRangeAddressList=[[['all'], ['all']]], protocol='ospf', activate=True)

            2> activateRouterIdRouteRanges(routeRangeAddressList=[[['all'], ['202.13.0.0', '202.23.0.0', '203.5.0.0']]],
                                                                 protocol='isis', activate=False)

            3> activateRouterIdRouteRanges(routeRangeAddressList=[[['192.0.0.2', '192.0.0.3'], ['202.11.0.0', '202.21.0.0']],
                                                                 [['192.0.0.1'], ['all']]], protocol='ospf', activate=False)

            4> activateRouterIdRouteRanges(routeRangeAddressList=[[['192.0.0.1', '192.0.0.3'], ['202.3.0.0', '202.23.0.0']]],
                                                                 protocol='ospf', activate=False)
        """
        if protocol == 'bgp':  protocol = 'bgpIPRouteProperty'
        if protocol == 'ospf': protocol = 'ospfRouteProperty'
        if protocol == 'isis': protocol = 'isisL3RouteProperty'
        if protocol == 'ldp':  protocol = 'ldpFECProperty'

        # 1: Get all the Device Group objects with the user specified router IDs.
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': [], 'where': []},
                              {'node': 'deviceGroup', 'properties': ['multiplier'], 'where': []},
                              {'node': 'routerData',  'properties': ['routerId', 'count'], 'where': []}
                          ]}
        deviceGroupObjList = []
        allRouterIdList = []
        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
        for topology in queryResponse.json()['result'][0]['topology']:
            for deviceGroup in topology['deviceGroup']:
                deviceGroupObj = deviceGroup['href']
                deviceGroupMultiplier = deviceGroup['multiplier']
                routerIdMultivalue = deviceGroup['routerData'][0]['routerId']
                routerIdList = self.ixnObj.getMultivalueValues(routerIdMultivalue, silentMode=True)
                deviceGroupObjList.append((deviceGroupObj, deviceGroupMultiplier, routerIdList, routerIdMultivalue))

                for rId in routerIdList:
                    if rId not in allRouterIdList:
                        allRouterIdList.append(rId)

        # 2: For each Device Group, look for the protocol to enable|disable
        #    Enable|disable based on the specified routerId list
        for deviceGroup in deviceGroupObjList:
            deviceGroupObj = deviceGroup[0]
            deviceGroupMultiplier = deviceGroup[1]
            deviceGroupRouterIdList = deviceGroup[2]
            routerIdMultivalue = deviceGroup[3]

            self.ixnObj.logInfo('\nSearching Device Group: %s' % deviceGroupObj)
            queryData = {'from': deviceGroupObj,
                        'nodes': [{'node': 'networkGroup',  'properties': [], 'where': []},
                                  {'node': 'ipv4PrefixPools', 'properties': ['networkAddress', 'count'], 'where': []},
                                  {'node': protocol,  'properties': ['active'], 'where': []}
                                ]}
            queryResponse = self.ixnObj.query(data=queryData, silentMode=False)

            # Note: A device group could have multiple network groups.
            #       Loop through all configured network groups for the ipv4PrefixPools with the user specified protocol.
            for networkGroup in queryResponse.json()['result'][0]['networkGroup']:
                networkGroupObj = networkGroup['href']
                for ipv4Prefix in networkGroup['ipv4PrefixPools']:
                    if ipv4Prefix[protocol] != []:
                        ipv4PrefixPoolMultivalue = ipv4Prefix['networkAddress']
                        ipv4PrefixPool = self.ixnObj.getMultivalueValues(ipv4PrefixPoolMultivalue, silentMode=True)
                        protocolMultivalue = ipv4Prefix[protocol][0]['active']
                        protocolActiveList = self.ixnObj.getMultivalueValues(protocolMultivalue, silentMode=True)
                        totalCountForEachRouterId = ipv4Prefix['count'] // deviceGroupMultiplier
                        totalRouteRangeCount = ipv4Prefix['count']

                        # Create a dictionary containing routerID starting/ending indexes.
                        routerIdIndexes = {}
                        startingIndex = 0
                        endingIndex = totalCountForEachRouterId
                        for routerId in deviceGroupRouterIdList:
                            routerIdIndexes[routerId, 'startingIndex'] = {}
                            routerIdIndexes[routerId, 'endingIndex'] = {}
                            routerIdIndexes[routerId, 'startingIndex'] = startingIndex
                            routerIdIndexes[routerId, 'endingIndex'] = endingIndex
                            startingIndex += totalCountForEachRouterId
                            endingIndex += totalCountForEachRouterId

                        for key,value in routerIdIndexes.items():
                            print('', key, value)

                        self.ixnObj.logInfo('\nCurrent active list: %s' % protocolActiveList)
                        startingIndex = 0
                        endingIndex = totalCountForEachRouterId
                        for eachRouterId in deviceGroupRouterIdList:
                            print(eachRouterId)
                            for item in routeRangeAddressList:
                                currentUserDefinedRouterIdList = item[0]
                                currentUserDefinedRouteRangeList = item[1]

                                if 'all' not in currentUserDefinedRouterIdList:
                                    if eachRouterId not in currentUserDefinedRouterIdList:
                                        continue

                                if 'all' in currentUserDefinedRouteRangeList:
                                    for index in range(routerIdIndexes[eachRouterId,'startingIndex'], routerIdIndexes[eachRouterId,'endingIndex']):
                                        protocolActiveList[index] = activate

                                if 'all' not in currentUserDefinedRouteRangeList:
                                    for index in range(startingIndex, totalRouteRangeCount):
                                        currentIpv4PrefixPoolsIndex = ipv4PrefixPool[index]
                                        if ipv4PrefixPool[index] in currentUserDefinedRouteRangeList:
                                            protocolActiveList[index] = activate

                                self.ixnObj.logInfo('\nModifying: %s' % networkGroupObj)
                                self.ixnObj.configMultivalue(protocolMultivalue, multivalueType='valueList', data={'values': protocolActiveList})

    def modifyProtocolRoutes(self, **kwargs):
        """
        Description

        Parameters
            protocol:
            startingAddress:
            endingAddress:

        Example:
            configNetworkGroup(deviceGroupObj2,
                               name='networkGroup2',
                               multiplier = 100,
                               networkAddress = {'start': '180.1.0.0',
                                                 'step': '0.0.0.1',
                                                 'direction': 'increment'},
                               prefixLength = 24)
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+networkGroupPrefixPoolObj)
        print(response.json())
        prefixPoolAddressMultivalue = response.json()['networkAddress']
        print('modifyProtocolRoutes:', prefixPoolAddressMultivalue)
        #self.ixnObj.patch(self.ixnObj.httpHeader+/networkGroupObj, data=data)

        if 'networkGroupObj' not in kwargs:
            response = self.ixnObj.post(self.ixnObj.httpHeader+deviceGroupObj+'/networkGroup')
            networkGroupObj = response.json()['links'][0]['href']

        if 'networkGroupObj' in kwargs:
            networkGroupObj = kwargs['networkGroupObj']

        self.ixnObj.logInfo('\nconfigNetworkGroup: %s' % networkGroupObj)
        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+networkGroupObj, data={'name': kwargs['name']})

        if 'multiplier' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+networkGroupObj, data={'multiplier': kwargs['multiplier']})

        if 'networkAddress' in kwargs:
            response = self.ixnObj.post(self.ixnObj.httpHeader+networkGroupObj+'/ipv4PrefixPools')
            prefixPoolObj = self.ixnObj.httpHeader + response.json()['links'][0]['href']

            # prefixPoolId = /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/networkGroup/3/ipv4PrefixPools/1
            ipv4PrefixResponse = self.ixnObj.get(prefixPoolObj)

            if 'networkAddress' in kwargs:
                multiValue = ipv4PrefixResponse.json()['networkAddress']
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/counter",
                           data={'start': kwargs['networkAddress']['start'],
                                 'step': kwargs['networkAddress']['step'],
                                 'direction': kwargs['networkAddress']['direction']})

            if 'prefixLength' in kwargs:
                multiValue = ipv4PrefixResponse.json()['prefixLength']
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue",
                           data={'value': kwargs['prefixLength']})

        return prefixPoolObj


    def applyOnTheFly(self):
        """
         Description
            Apply configuration changes on the fly while Topology is running.
        """
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/globals/topology/operations/applyonthefly',
                             data={'arg1': '/api/v1/sessions/1/ixnetwork/globals/topology'})
        self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/globals/topology/operations/applyonthefly'+response.json()['id'])

    def getProtocolListByPort(self, port):
        """
        Description
            For IxNetwork Classic Framework only:
            Get all enabled protocolss by the specified port.

        Parameter
            port: (chassisIp, cardNumber, portNumber) -> ('10.10.10.1', '2', '8')
        """
        chassis = str(port[0])
        card = str(port[1])
        port = str(port[2])
        specifiedPort = (chassis, card, port)
        enabledProtocolList = []
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        vportList = ['%s/%s/%s' % (self.ixnObj.sessionUrl, 'vport', str(i["id"])) for i in response.json()]
        for vport in vportList:
            response = self.ixnObj.get(vport, 'assignedTo')
            # 10.219.117.101:1:5
            assignedTo = response.json()['assignedTo']
            currentChassisIp  = str(assignedTo.split(':')[0])
            currentCardNumber = str(assignedTo.split(':')[1])
            currentPortNumber = str(assignedTo.split(':')[2])
            currentPort = (currentChassisIp, currentCardNumber, currentPortNumber)
            if currentPort != specifiedPort:
                continue
            else:
                response = self.ixnObj.get(vport+'/protocols?links=true')
                if response.status_code == 200:
                     #print 'json', response.json()['links']
                    for protocol in response.json()['links']:
                        currentProtocol = protocol['href']
                        url = self.ixnObj.httpHeader+currentProtocol
                        response = self.ixnObj.get(url)
                        if 'enabled' in response.json() and response.json()['enabled'] == True:
                            # Exclude ARP object
                            if 'arp' not in currentProtocol:
                                enabledProtocolList.append(str(currentProtocol))

        return enabledProtocolList

    def getProtocolListByPortNgpf(self, port):
        """
        Description
            For IxNetwork NGPF only:
            This API will get all enabled protocolss by the specified port.

        Parameter
            port: [chassisIp, cardNumber, portNumber]
                  Example: ['10.10.10.1', '2', '8']

        Returns
            [] = If no protocol is configured.
            A list of configured protocols associated with the specified port.
                 Ex: ['/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/ospfv2',
                      '/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4/1/ospfv2']
        """
        chassis = str(port[0])
        card = str(port[1])
        port = str(port[2])
        specifiedPort = (chassis, card, port)
        enabledProtocolList = []
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/topology')
        topologyList = ['%s/%s/%s' % (self.ixnObj.sessionUrl, 'topology', str(i["id"])) for i in response.json()]
        for topology in topologyList:
            response = self.ixnObj.get(topology+'/deviceGroup')
            deviceGroupList = ['%s/%s/%s' % (topology, 'deviceGroup', str(i["id"])) for i in response.json()]
            for deviceGroup in deviceGroupList:
                response = self.ixnObj.get(deviceGroup+'/ethernet')
                ethernetList = ['%s/%s/%s' % (deviceGroup, 'ethernet', str(i["id"])) for i in response.json()]
                for ethernet in ethernetList:
                    response = self.ixnObj.get(ethernet+'/ipv4')
                    ipv4List = ['%s/%s/%s' % (ethernet, 'ipv4', str(i["id"])) for i in response.json()]
                    response = self.ixnObj.get(ethernet+'/ipv6')
                    ipv6List = ['%s/%s/%s' % (ethernet, 'ipv6', str(i["id"])) for i in response.json()]
                    for layer3Ip in ipv4List+ipv6List:
                        url = layer3Ip+'?links=true'
                        response = self.ixnObj.get(url)
                        for protocol in response.json()['links']:
                            currentProtocol = protocol['href']
                            print('\nProtocol URL:', currentProtocol)

                            if (bool(re.match('^/api/.*(ipv4|ipv6)/[0-9]+$', currentProtocol))):
                                continue
                            if (bool(re.match('^/api/.*(ipv4|ipv6)/[0-9]+/port$', currentProtocol))):
                                continue
                            url = self.ixnObj.httpHeader+currentProtocol
                            response = self.ixnObj.get(url)
                            if response.json() == []:
                                # The currentProtocol is not configured.
                                continue
                            else:
                                enabledProtocolList.append(str(currentProtocol))

        return enabledProtocolList

    def getPortsByProtocol(self, protocolName):
        """
        Description
            For IxNetwork Classic Framework only:
            Based on the specified protocol, return all ports associated withe the protocol.

        Parameter
           protocolName options:
              bfd, bgp, cfm, eigrp, elmi, igmp, isis, lacp, ldp, linkOam, lisp, mld,
              mplsOam, mplsTp, openFlow, ospf, ospfV3, pimsm, ping, rip, ripng, rsvp,
              static, stp

         Returns: [chassisIp, cardNumber, portNumber]
                  Example: [('10.219.117.101', '1', '1'), ('10.219.117.101', '1', '2')]

         Returns [] if no port is configured with the specified protocolName
        """
        portList = []
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        # ['http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/vport/1']
        vportList = ['%s/%s/%s' % (self.ixnObj.sessionUrl, 'vport', str(i["id"])) for i in response.json()]

        # Go through each port that has the protocol enabled.
        for vport in vportList:
            # http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/vport/1/protocols/ospf
            currentProtocol = vport+'/protocols/'+protocolName
            response = self.ixnObj.get(currentProtocol)
            if response.json()['enabled'] == True:
                # 10.219.117.101:1:5
                response = self.ixnObj.get(vport)
                assignedTo = response.json()['assignedTo']
                currentChassisIp  = str(assignedTo.split(':')[0])
                currentCardNumber = str(assignedTo.split(':')[1])
                currentPortNumber = str(assignedTo.split(':')[2])
                currentPort = (currentChassisIp, currentCardNumber, currentPortNumber)
                portList.append(currentPort)

        return portList

    def getPortsByProtocolNgpf(self, protocolName):
        """
        Description
            For IxNetwork NGPF only:
            Based on the specified protocol, return all ports associated with the protocol.

         Returns
            [chassisIp, cardNumber, portNumber]
            Example: [['10.219.117.101', '1', '1'], ['10.219.117.101', '1', '2']]

            Returns [] if no port is configured with the specified protocolName

         protocolName options:
            ['ancp',
            'bfdv4Interface',
            'bgpIpv4Peer',
            'bgpIpv6Peer',
            'dhcpv4relayAgent',
            'dhcpv6relayAgent',
            'dhcpv4server',
            'dhcpv6server',
            'geneve',
            'greoipv4',
            'greoipv6',
            'igmpHost',
            'igmpQuerier',
            'lac',
            'ldpBasicRouter',
            'ldpBasicRouterV6',
            'ldpConnectedInterface',
            'ldpv6ConnectedInterface',
            'ldpTargetedRouter',
            'ldpTargetedRouterV6',
            'lns',
            'mldHost',
            'mldQuerier',
            'ptp',
            'ipv6sr',
            'openFlowController',
            'openFlowSwitch',
            'ospfv2',
            'ospfv3',
            'ovsdbcontroller',
            'ovsdbserver',
            'pcc',
            'pce',
            'pcepBackupPCEs',
            'pimV4Interface',
            'pimV6Interface',
            'ptp',
            'rsvpteIf',
            'rsvpteLsps',
            'tag',
            'vxlan'
        """
        portList = []
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/topology')
        topologyList = ['%s/%s/%s' % (self.ixnObj.sessionUrl, 'topology', str(i["id"])) for i in response.json()]
        for topology in topologyList:
            response = self.ixnObj.get(topology+'/deviceGroup')
            deviceGroupList = ['%s/%s/%s' % (topology, 'deviceGroup', str(i["id"])) for i in response.json()]
            for deviceGroup in deviceGroupList:
                response = self.ixnObj.get(deviceGroup+'/ethernet')
                ethernetList = ['%s/%s/%s' % (deviceGroup, 'ethernet', str(i["id"])) for i in response.json()]
                for ethernet in ethernetList:
                    response = self.ixnObj.get(ethernet+'/ipv4')
                    ipv4List = ['%s/%s/%s' % (ethernet, 'ipv4', str(i["id"])) for i in response.json()]
                    response = self.ixnObj.get(ethernet+'/ipv6')
                    ipv6List = ['%s/%s/%s' % (ethernet, 'ipv6', str(i["id"])) for i in response.json()]
                    for layer3Ip in ipv4List+ipv6List:
                        url = layer3Ip+'/'+protocolName
                        print('\nProtocol URL:', url)
                        response = self.ixnObj.get(url)
                        if response.json() == []:
                            continue
                        response = self.ixnObj.get(topology)
                        vportList = response.json()['vports']
                        for vport in vportList:
                            response = self.ixnObj.get(self.ixnObj.httpHeader+vport)
                            assignedTo = response.json()['assignedTo']
                            currentChassisIp  = str(assignedTo.split(':')[0])
                            currentCardNumber = str(assignedTo.split(':')[1])
                            currentPortNumber = str(assignedTo.split(':')[2])
                            currentPort = [currentChassisIp, currentCardNumber, currentPortNumber]
                            portList.append(currentPort)
                            self.ixnObj.logInfo('\tFound port configured: %s' % currentPort)
        return portList

    def flapBgp(self, topologyName=None, bgpName=None, enable=True, ipInterfaceList='all', upTimeInSeconds=0, downTimeInSeconds=0):
        """
        Description
           Enable/Disable BGP flapping.

        Parameters
           topologyName: <str>: Mandatory: The Topolgy Group name where the BGP stack resides in.
           bgpName: <str>: Mandatory. The name of the BGP stack.
           enable: <bool>: To enable or disable BGP flapping.
           ipInterfaceList: <list>: A list of the local BGP IP interface to configure for flapping.
           upTimeInSeconds: <int>: The up time for BGP to remain up before flapping it down.
           downTimeInSeconds: <int>: The down time for BGP to remain down before flapping it back up.
        """
        bgpObject = None
        queryData = {'from': '/',
                     'nodes': [{'node': 'topology', 'properties': ['name'], 'where': [{'property': 'name', 'regex': topologyName}]},
                               {'node': 'deviceGroup', 'properties': [], 'where': []},
                               {'node': 'ethernet', 'properties': [], 'where': []},
                               {'node': 'ipv4', 'properties': [], 'where': []},
                               {'node': 'ipv6', 'properties': [], 'where': []},
                               {'node': 'bgpIpv4Peer', 'properties': ['name'], 'where': []},
                               {'node': 'bgpIpv6Peer', 'properties': ['name'], 'where': []}
                           ]}

        queryResponse = self.ixnObj.query(data=queryData)
        if queryResponse.json()['result'][0]['topology'][0]['name'] != topologyName:
            raise IxNetRestApiException('\nNo such Topology Group name found %s' % topologyName)
            
        try:
            discoveredBgpName = queryResponse.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv4'][0]['bgpIpv4Peer'][0]['name']
            if bgpName == discoveredBgpName:
                bgpObject = queryResponse.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv4'][0]['bgpIpv4Peer'][0]['href']
        except:
            discoveredBgpName = queryResponse.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv6'][0]['bgpIpv6Peer'][0]['name']
            if bgpName == discoveredBgpName:
                bgpObject = queryResponse.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv6'][0]['bgpIpv6Peer'][0]['href']
        
        if bgpObject == None:
            raise IxNetRestApiException('\nNo such bgp name found %s' % bgpName)
        
        self.flapBgpPeerNgpf(bgpObjHandle=bgpObject, enable=enable, flapList=ipInterfaceList,
                             uptime=upTimeInSeconds, downtime=downTimeInSeconds)

    def flapBgpPeerNgpf(self, bgpObjHandle, enable=True, flapList='all', uptime=0, downtime=0):
        """
        Description
           Enable or disable BGP flapping on either all or a list of IP interfaces.

        Parameters
            bgpObjHandle: The bgp object handle.
                         /api/v1/sessions/<int>/ixnetwork/topology/<int>/deviceGroup/<int>/ethernet/<int>/ipv4/<int>/bgpIpv4Peer/<int>
            enable: <bool>: Default = True
            flapList: 'all' or a list of IP addresses to enable/disable flapping.
                      [['10.10.10.1', '10.10.10.8', ...]
                      Default = 'all'
            uptime: <int>: In seconds. Defaults = 0
            downtime: <int>: In seconds. Defaults = 0

        Syntax
           POST = /api/v1/sessions/<int>/ixnetwork/topology/<int>/deviceGroup/<int>/ethernet/<int>/ipv4/<int>/bgpIpv4Peer/<int>
        """
        if flapList != 'all' and type(flapList) != list:
            ipRouteListToFlap = flapList.split(' ')

        response = self.ixnObj.get(self.ixnObj.httpHeader+bgpObjHandle)

        # Get the IP object from the bgpObjHandle
        match = re.match('(/api.*)/bgp', bgpObjHandle)
        ipObj = match.group(1)

        ipAddressList = self.getIpAddresses(ipObj)
        count = len(ipAddressList)

        # Recreate an index list based on user defined ip address to enable/disable
        indexToFlapList = []
        if flapList != 'all':
            for ipAddress in flapList:
                # A custom list of indexes to enable/disable flapping based on the IP address index number.
                indexToFlapList.append(ipAddressList.index(ipAddress))

        # Copy the same index list for uptime and downtime
        indexUptimeList = indexToFlapList
        indexDowntimeList = indexToFlapList
        response = self.ixnObj.get(self.ixnObj.httpHeader+bgpObjHandle)
        enableFlappingMultivalue = response.json()['flap']
        upTimeMultivalue = response.json()['uptimeInSec']
        downTimeMultivalue = response.json()['downtimeInSec']

        flappingResponse = self.ixnObj.getMultivalueValues(enableFlappingMultivalue)
        uptimeResponse = self.ixnObj.getMultivalueValues(upTimeMultivalue)
        downtimeResponse = self.ixnObj.getMultivalueValues(downTimeMultivalue)

        # Flapping IP addresses
        flapOverlayList = []
        uptimeOverlayList = []
        downtimeOverlayList = []
        # Build a valueList of either "true" or "false"
        if flapList == 'all':
            for counter in range(0,count):
                if enable == True:
                    flapOverlayList.append("true")
                if enable == False:
                    flapOverlayList.append("false")
                uptimeOverlayList.append(str(uptime))
                downtimeOverlayList.append(str(downtime))

        if flapList != 'all':
            # ['true', 'true', 'true']
            currentFlappingValueList = flappingResponse
            # ['10', '10', '10']
            currentUptimeValueList   = uptimeResponse
            # ['20', '20', '20']
            currentDowntimeValueList = downtimeResponse

            indexCounter = 0
            for (eachFlapValue, eachUptimeValue, eachDowntimeValue) in zip(currentFlappingValueList, currentUptimeValueList,
                                                                           currentDowntimeValueList):
                # Leave the setting alone on this index position. User did not care to change this value.
                if indexCounter not in indexToFlapList:
                    flapOverlayList.append(eachFlapValue)
                    uptimeOverlayList.append(eachUptimeValue)
                    downtimeOverlayList.append(eachDowntimeValue)
                else:
                    # Change the value on this index position.
                    if enable == True:
                        flapOverlayList.append("true")
                    else:
                        flapOverlayList.append("false")

                    uptimeOverlayList.append(str(uptime))
                    downtimeOverlayList.append(str(downtime))
                indexCounter += 1

        self.ixnObj.patch(self.ixnObj.httpHeader + enableFlappingMultivalue+'/valueList', data={'values': flapOverlayList})
        self.ixnObj.patch(self.ixnObj.httpHeader + upTimeMultivalue+'/valueList', data={'values': uptimeOverlayList})
        self.ixnObj.patch(self.ixnObj.httpHeader + downTimeMultivalue+'/valueList', data={'values': downtimeOverlayList})

    def flapBgpRoutesNgpf(self, prefixPoolObj, enable=True, ipRouteListToFlap='all', uptime=0, downtime=0, ip='ipv4'):
        """
        Description
           This API will enable or disable flapping on either all or a list of BGP IP routes.
           If you are configuring routes to enable, you could also set the uptime and downtime in seconds.

        Parameters
            prefixPoolObj = The Network Group PrefixPool object that was returned by configNetworkGroup()
                            /api/v1/sessions/<int>/ixnetwork/topology/<int>/deviceGroup/<int>/networkGroup/<int>/ipv4PrefixPools/<int>
            enable: True or False
                - Default = True
            ipRouteListToFlap: 'all' or a list of IP route addresses to enable/disable.
                                 [['160.1.0.1', '160.1.0.2',...]
                - Default = 'all'
            upTime: In seconds.
                - Defaults = 0
            downTime: In seconds.
                - Defaults = 0
            ip: ipv4 or ipv6
                - Defaults = ipv4

        Syntax
           POST = For IPv4: http://{apiServerIp:port}/api/v1/sessions/<int>/ixnetwork/topology/<int>/deviceGroup/<int>/networkGroup/<int>/ipv4PrefixPools/<int>/bgpIPRouteProperty

                  For IPv6: http://{apiServerIp:port}/api/v1/sessions/<int>/ixnetwork/topology/<int>/deviceGroup/<int>/networkGroup/<int>/ipv4PrefixPools/<int>/bgpV6IPRouteProperty
        """

        if ipRouteListToFlap != 'all' and type(ipRouteListToFlap) != list:
            ipRouteListToFlap = ipRouteListToFlap.split(' ')

        # Get a list of configured IP route addresses
        response = self.ixnObj.get(self.ixnObj.httpHeader+prefixPoolObj)
        networkAddressList = response.json()['lastNetworkAddress']
        count = len(networkAddressList)

        # Recreate an index list based on user defined ip route to enable/disable
        indexToFlapList = []
        if ipRouteListToFlap != 'all':
            for ipRouteAddress in ipRouteListToFlap:
                # A custom list of indexes to enable/disable flapping based on the IP address index number.
                indexToFlapList.append(networkAddressList.index(ipRouteAddress))

        # Copy the same index list for uptime and downtime
        indexUptimeList = indexToFlapList
        indexDowntimeList = indexToFlapList

        if ip == 'ipv4':
            response = self.ixnObj.get(self.ixnObj.httpHeader+prefixPoolObj+'/bgpIPRouteProperty')
        if ip == 'ipv6':
            response = self.ixnObj.get(self.ixnObj.httpHeader+prefixPoolObj+'/bgpV6IPRouteProperty')

        enableFlappingMultivalue = response.json()[0]['enableFlapping']
        upTimeMultivalue = response.json()[0]['uptime']
        downTimeMultivalue = response.json()[0]['downtime']
        flappingResponse = self.ixnObj.getMultivalueValues(enableFlappingMultivalue)
        uptimeResponse = self.ixnObj.getMultivalueValues(upTimeMultivalue)
        downtimeResponse = self.ixnObj.getMultivalueValues(downTimeMultivalue)

        # Flapping IP addresses
        flapOverlayList = []
        uptimeOverlayList = []
        downtimeOverlayList = []
        # Build a valueList of either "true" or "false"
        if ipRouteListToFlap == 'all':
            for counter in range(0,count):
                if enable == True:
                    flapOverlayList.append("true")
                if enable == False:
                    flapOverlayList.append("false")
                uptimeOverlayList.append(str(uptime))
                downtimeOverlayList.append(str(downtime))

        if ipRouteListToFlap != 'all':
            currentFlappingValueList = flappingResponse[0]
            currentUptimeValueList   = uptimeResponse[0]
            currentDowntimeValueList = downtimeResponse[0]

            indexCounter = 0
            for (eachFlapValue, eachUptimeValue, eachDowntimeValue) in zip(currentFlappingValueList,
                                                                           currentUptimeValueList, currentDowntimeValueList):
                # Leave the setting alone on this index position. User did not care to change this value.
                if indexCounter not in indexToFlapList:
                    flapOverlayList.append(eachFlapValue)
                    uptimeOverlayList.append(eachUptimeValue)
                    downtimeOverlayList.append(eachDowntimeValue)
                else:
                    # Change the value on this index position.
                    if enable == True:
                        flapOverlayList.append("true")
                    else:
                        flapOverlayList.append("false")
                    uptimeOverlayList.append(str(uptime))
                    downtimeOverlayList.append(str(downtime))
                indexCounter += 1

        # /topology/[1]/deviceGroup
        self.ixnObj.patch(self.ixnObj.httpHeader + enableFlappingMultivalue+'/valueList', data={'values': flapOverlayList})
        self.ixnObj.patch(self.ixnObj.httpHeader + upTimeMultivalue+'/valueList', data={'values': uptimeOverlayList})
        self.ixnObj.patch(self.ixnObj.httpHeader + downTimeMultivalue+'/valueList', data={'values': downtimeOverlayList})

    def enableProtocolRouteRange(self, routerId, protocol, enable=False):
        """
        Description
            Enable or disable route range for protocols: ospf, bgp, isis, etc.

        Parameters
            routerId: all|List of routerId
            enable: True|False
        """
        deviceGroupObj = self.getDeviceGroupByRouterId(routerId)
        response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroupObj+'/routerData')
        routerIdMultivalue = response.json()[0]['routerId']
        routerIdList = self.ixnObj.getMultivalueValues(routerIdMultivalue)
        print(routerIdList)
        print(deviceGroupObj)


    def startStopIpv4Ngpf(self, ipv4ObjList, action='start'):
        """
        Description
           Start or stop IPv4 header.

        Parameters
            ipv4ObjList: Provide a list of one or more IPv4 object handles to start or stop.
                 Ex: ["/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1", ...]

            action: start or stop
        """
        if type(ipv4ObjList) != list:
            raise IxNetRestApiException('startStopIpv4Ngpf error: The parameter ipv4ObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl+'/topology/deviceGroup/ethernet/ipv4/operations/'+action
        data = {'arg1': ipv4ObjList}
        self.ixnObj.logInfo('\nstartStopIpv4Ngpf: {0}'.format(action))
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def startStopBgpNgpf(self, bgpObjList, action='start'):
        """
        Description
            Start or stop BGP protocol

        Parameters
            bgpObjList: Provide a list of one or more BGP object handles to start or stop.
                 Ex: ["/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1", ...]

            action: start or stop
        """
        if type(bgpObjList) != list:
            raise IxNetRestApiException('startStopBgpNgpf error: The parameter bgpObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl+'/topology/deviceGroup/ethernet/ipv4/bgpIpv4Peer/operations/'+action
        data = {'arg1': bgpObjList}
        self.ixnObj.logInfo('\nstartStopBgpNgpf: {0}'.format(action))
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def startStopOspfNgpf(self, ospfObjList, action='start'):
        """
        Description
            Start or stop OSPF protocol

        Parameters
            bgpObjList: Provide a list of one or more OSPF object handles to start or stop.
                 Ex: ["/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/ospfv2/1", ...]

            action: start or stop
        """
        if type(ospfObjList) != list:
            raise IxNetRestApiException('startStopOspfNgpf error: The parameter ospfObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl+'/topology/deviceGroup/ethernet/ipv4/ospfv2/operations/'+action
        data = {'arg1': ospfObjList}
        self.ixnObj.logInfo('\nstartStopOspfNgpf: {0}'.format(action))
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def startStopIgmpHostNgpf(self, igmpHostObjList, action='start'):
        """
        Description
            Start or stop IGMP Host protocol

        Parameters
            igmpHostObjList: Provide a list of one or more IGMP host object handles to start or stop.
                 Ex: ["/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1", ...]

        action: start or stop
        """
        if type(igmpHostObjList) != list:
            raise IxNetRestApiException('igmpHostObjNgpf error: The parameter igmpHostObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl+'/topology/deviceGroup/ethernet/ipv4/igmpHost/operations/'+action
        data = {'arg1': igmpHostObjList}
        self.ixnObj.logInfo('\nstartStopIgmpHostNgpf: {0}'.format(action))
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def startStopPimV4InterfaceNgpf(self, pimV4ObjList, action='start'):
        """
        Description
            Start or stop PIM IPv4 interface.

        Parameters
            pimV4ObjList: Provide a list of one or more PIMv4 object handles to start or stop.
                       Ex: ["/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/pimV4Interface/1", ...]

            action: start or stop
        """
        if type(pimV4ObjList) != list:
            raise IxNetRestApiException('startStopPimV4InterfaceNgpf error: The parameter pimv4ObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl+'/topology/deviceGroup/ethernet/ipv4/pimV4Interface/operations/'+action
        data = {'arg1': pimV4ObjList}
        self.ixnObj.logInfo('\nstartStopPimV4InterfaceNgpf: {0}'.format(action))
        self.ixnObj.logInfo('\t%s' % pimV4ObjList)
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def startStopMldHostNgpf(self, mldHostObjList, action='start'):
        """
        Description
            Start or stop MLD Host.  For IPv6 only.

        Parameters
            mldHostObjList: Provide a list of one or more mldHost object handles to start or stop.
                         Ex: ["/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1", ...]

            action: start or stop
        """
        if type(mldHostObjList) != list:
            raise IxNetRestApiException('startStopMldHostNgpf error: The parameter mldHostObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl+'/topology/deviceGroup/ethernet/ipv6/mldHost/operations/'+action
        data = {'arg1': mldHostObjList}
        self.ixnObj.logInfo('\nstartStopMldHostNgpf: {0}'.format(action))
        self.ixnObj.logInfo('\t%s' % mldHostObjList)
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def startStopIsisL3Ngpf(self, isisObjList, action='start'):
        """
        Description
            Start or stop ISIS protocol.

        Parameters
            isisObjList: Provide a list of one or more mldHost object handles to start or stop.
                      Ex: ["/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/isisL3/3", ...]

        action = start or stop
        """
        if type(isisObjList) != list:
            raise IxNetRestApiException('startStopIsisL3Ngpf error: The parameter isisObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl+'/topology/deviceGroup/ethernet/isisL3/operations/'+action
        data = {'arg1': isisObjList}
        self.ixnObj.logInfo('\nstartStopIsisL3Ngpf: {0}'.format(action))
        self.ixnObj.logInfo('\t%s' % isisObjList)
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def startStopLdpBasicRouterNgpf(self, ldpObjList, action='start'):
        """
        Description
            Start or stop LDP Basic Router protocol.

        Parameters
            isisObjList: Provide a list of one or more ldpBasicRouter object handles to start or stop.
                      Ex: ["/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ldpBasicRouter/3", ...]

        action = start or stop
        """
        if type(isisObjList) != list:
            raise IxNetRestApiException('startStopLdpBasicRouterNgpf error: The parameter ldpObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl+'/topology/deviceGroup/ldpBasicRouter/operations/'+action
        data = {'arg1': ldpObjList}
        self.ixnObj.logInfo('\nstartStopLdpBasicRouterNgpf: {0}'.format(action))
        self.ixnObj.logInfo('\t%s' % ldpObjList)
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def enableDisableIgmpGroupRangeNgpf(self, protocolSessionUrl, groupRangeList, action='disable'):
        """
         Description:
             To enable or disable specific multicast group range IP addresses by using overlay.

             1> Get a list of all the Multicast group range IP addresses.
             2> Get the multivalue list of ACTIVE STATE group ranges.
             3> Loop through the user list "groupRangeList" and look
                for the index position of the specified group range IP address.
             4> Using overlay to enable|disable the index value.

             Note: If an overlay is not created, then create one by:
                   - Creating a "ValueList" for overlay pattern.
                   - And add an Overlay.

        Parameters
            protocolSessionUrl: http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1
            groupRangeList: A list of multicast group range addresses to disable.
                                Example: ['225.0.0.1', '225.0.0.5']
            action: disable or enable

        """
        if action == 'disable':
            enableDisable = 'false'
        else:
            enableDisable = 'true'

        url = protocolSessionUrl+'/igmpMcastIPv4GroupList'
        response = self.ixnObj.get(url)
        # /api/v1/sessions/1/ixnetwork/multivalue/59

        # Get startMcastAddr multivalue to get a list of all the configured Group Range IP addresses.
        groupRangeAddressMultivalue = response.json()['startMcastAddr']
        # Get the active multivalue to do the overlay on top of.
        activeMultivalue = response.json()['active']

        # Getting the list of Group Range IP addresses.
        response = self.ixnObj.get(self.ixnObj.httpHeader+groupRangeAddressMultivalue)

        # groupRangeValues are multicast group ranges:
        # [u'225.0.0.1', u'225.0.0.2', u'225.0.0.3', u'225.0.0.4', u'225.0.0.5']
        groupRangeValues = response.json()['values']
        print('\nConfigured groupRangeValues:', groupRangeValues)

        listOfIndexesToDisable = []
        # Loop through user list of specified group ranges to disable.
        for groupRangeIp in groupRangeList:
            index = groupRangeValues.index(groupRangeIp)
            listOfIndexesToDisable.append(index)

        if listOfIndexesToDisable == []:
            raise IxNetRestApiException('disableIgmpGroupRangeNgpf Error: No multicast group range ip address found on your list')

        for index in listOfIndexesToDisable:
            currentOverlayUrl = self.ixnObj.httpHeader+activeMultivalue+'/overlay'
            # http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/multivalue/5/overlay
            # NOTE:  Index IS NOT zero based.
            self.ixnObj.logInfo('enableDisableIgmpGroupRangeNgpf: %s: %s' % (action, groupRangeValues[index]))
            response = self.ixnObj.post(currentOverlayUrl, data={'index': index+1, 'value': enableDisable})

    def enableDisableMldGroupNgpf(self, protocolSessionUrl, groupRangeList, action='disable'):
        """
         Description:
             For IPv6 only. To enable or disable specific multicast group range IP addresses by using
             overlay.

             1> Get a list of all the Multicast group range IP addresses.
             2> Get the multivalue list of ACTIVE STATE group ranges.
             3> Loop through the user list "groupRangeList" and look
                for the index position of the specified group range IP address.
             4> Using overlay to enable|disable the index value.

             Note: If an overlay is not created, then create one by:
                   - Creating a "ValueList" for overlay pattern.
                   - And add an Overlay.

        Parameters
            protocolSessionUrl: http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1
            groupRangeList: A list of multicast group range addresses to disable.
                                Example: ['ff03::1', 'ff03::2']
            action: disable or enable
        """
        if action == 'disable':
            enableDisable = 'false'
        else:
            enableDisable = 'true'

        url = protocolSessionUrl+'/mldMcastIPv6GroupList'
        response = self.ixnObj.get(url)
        # /api/v1/sessions/1/ixnetwork/multivalue/59

        # Get startMcastAddr multivalue to get a list of all the configured Group Range IP addresses.
        groupRangeAddressMultivalue = response.json()['startMcastAddr']
        # Get the active multivalue to do the overlay on top of.
        activeMultivalue = response.json()['active']

        # Getting the list of Group Range IP addresses.
        response = self.ixnObj.get(self.ixnObj.httpHeader+groupRangeAddressMultivalue)

        # groupRangeValues are multicast group ranges:
        # ['ff03::1', 'ff03::2']
        groupRangeValues = response.json()['values']
        self.ixnObj.logInfo('\nConfigured groupRangeValues: %s' % groupRangeValues)

        listOfIndexesToDisable = []
        # Loop through user list of specified group ranges to disable.
        for groupRangeIp in groupRangeList:
            index = groupRangeValues.index(groupRangeIp)
            listOfIndexesToDisable.append(index)

        if listOfIndexesToDisable == []:
            raise IxNetRestApiException('disableMldGroupNgpf Error: No multicast group range ip address found on your list')

        for index in listOfIndexesToDisable:
            currentOverlayUrl = self.ixnObj.httpHeader+activeMultivalue+'/overlay'
            # http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/multivalue/5/overlay
            # NOTE:  Index IS NOT zero based.
            self.ixnObj.logInfo('enableDisableMldGroupNgpf: %s: %s' % (action, groupRangeValues[index]))
            response = self.ixnObj.post(currentOverlayUrl, data={'index': index+1, 'value': enableDisable})

    def sendIgmpJoinLeaveNgpf(self, routerId=None, igmpHostUrl=None, multicastIpAddress=None, action='join'):
        """
        Description
            Send IGMP joins or leaves.

            A IGMP host object is acceptable.  If you don't know the IGMP host object, use Device Group RouterID.
            Since a Device Group could have many routerID, you could state one of them.

            If multicastIpAddress is 'all', this will send IGMP join on all multicast addresses.
            Else, provide a list of multicast IP addresses to send join.

        Parameters
            routerId: The Device Group Router ID address.
            igmpHostUrl: '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1'
            multicastIpAddress: 'all' or a list of multicast IP addresses to send join.
                                 Example: ['225.0.0.3', '225.0.0.4']
            action: join|leave
        """
        if action == 'join':
            action = 'igmpjoingroup'
        if action == 'leave':
            action = 'igmpleavegroup'

        # In case somebody passes in http://{ip:port}.  All this function needs is the Rest API.
        if igmpHostUrl:
            match = re.match('http://.*(/api.*)', igmpHostUrl)
            if match:
                igmpHostUrl = match.group(1)

        if routerId:
            deviceGroupObj = self.getDeviceGroupByRouterId(routerId=routerId)
            if deviceGroupObj == 0:
                raise IxNetRestApiException('No Device Group found for router ID: %s' % routerId)

            queryData = {'from': deviceGroupObj,
                        'nodes': [{'node': 'routerData', 'properties': [], 'where': []},
                                  {'node': 'ethernet', 'properties': [], 'where': []},
                                  {'node': 'ipv4', 'properties': [], 'where': []},
                                  {'node': 'igmpHost', 'properties': [], 'where': []},
                              ]}
            queryResponse = self.ixnObj.query(data=queryData)
            routerIdObj = queryResponse.json()['result'][0]['routerData'][0]['href']
            response = self.ixnObj.get(self.ixnObj.httpHeader+routerIdObj)
            routerIdMultivalue = response.json()['routerId']
            routerIdList = self.ixnObj.getMultivalueValues(routerIdMultivalue, silentMode=True)
            if routerId in routerIdList:
                igmpHostUrl = queryResponse.json()['result'][0]['ethernet'][0]['ipv4'][0]['igmpHost'][0]['href']

        # Based on the list of multicastIpAddress, get all their indexes.
        response = self.ixnObj.get(self.ixnObj.httpHeader+igmpHostUrl+'/igmpMcastIPv4GroupList')
        startMcastAddrMultivalue = response.json()['startMcastAddr']
        listOfConfiguredMcastIpAddresses = self.ixnObj.getMultivalueValues(startMcastAddrMultivalue)

        self.ixnObj.logInfo('\nsendIgmpJoinNgpf: List of configured Mcast IP addresses: %s' % listOfConfiguredMcastIpAddresses)
        if listOfConfiguredMcastIpAddresses == []:
            raise IxNetRestApiException('sendIgmpJoinNgpf: No Mcast IP address configured')

        if multicastIpAddress == 'all':
            listOfMcastAddresses = listOfConfiguredMcastIpAddresses
        else:
            listOfMcastAddresses = multicastIpAddress

        # Note: Index position is not zero based.
        indexListToSend = []
        for eachMcastAddress in listOfMcastAddresses:
            index = listOfConfiguredMcastIpAddresses.index(eachMcastAddress)
            indexListToSend.append(index+1)

        url = igmpHostUrl+'/igmpMcastIPv4GroupList/operations/%s' % action
        data = {'arg1': [igmpHostUrl+'/igmpMcastIPv4GroupList'], 'arg2': indexListToSend}
        self.ixnObj.logInfo('\nsendIgmpJoinNgpf: %s' % url)
        self.ixnObj.logInfo('\t%s' % multicastIpAddress)
        response = self.ixnObj.post(self.ixnObj.httpHeader+url, data=data)
        self.ixnObj.waitForComplete(response, url+response.json()['id'])

    def sendPimV4JoinLeaveNgpf(self, routerId=None, pimObj=None, multicastIpAddress=None, action='join'):
        """
        Description
            Send PIMv4 joins or leaves.

            A PIM host object is acceptable.  If you don't know the PIM host object, use Device Group RouterID.
            Since a Device Group could have many routerID, you could state one of them.

            If multicastIpAddress is 'all', this will send join on all multicast addresses.
            Else, provide a list of multicast IP addresses to send join|leave.

        NOTE:
           Current support:  Each IP host multicast group address must be unique. IP hosts could send the same
                             multicast group address, but this API only supports unique multicast group address.
  
        Parameters
            routerId: The Device Group Router ID address.
            pimObj: '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/pimV4Interface/1/pimV4JoinPruneList'
            multicastIpAddress: 'all' or a list of multicast IP addresses to send join.
                                 Example: ['225.0.0.3', '225.0.0.4']
            action: join|leave
        """
        # In case somebody passes in http://{ip:port}.  All this function needs is the Rest API.
        if pimObj:
            match = re.match('http://.*(/api.*)', pimObj)
            if match:
                pimObj = match.group(1)

        if routerId:
            deviceGroupObj = self.getDeviceGroupByRouterId(routerId=routerId)
            if deviceGroupObj == 0:
                raise IxNetRestApiException('No Device Group found for router ID: %s' % routerId)

            queryData = {'from': deviceGroupObj,
                        'nodes': [{'node': 'routerData', 'properties': [], 'where': []},
                                  {'node': 'ethernet', 'properties': [], 'where': []},
                                  {'node': 'ipv4', 'properties': [], 'where': []},
                                  {'node': 'pimV4Interface', 'properties': [], 'where': []}
                              ]}
            queryResponse = self.ixnObj.query(data=queryData)
            routerIdObj = queryResponse.json()['result'][0]['routerData'][0]['href']
            response = self.ixnObj.get(self.ixnObj.httpHeader+routerIdObj)
            routerIdMultivalue = response.json()['routerId']
            routerIdList = self.ixnObj.getMultivalueValues(routerIdMultivalue, silentMode=True)
            if routerId in routerIdList:
                pimObj = queryResponse.json()['result'][0]['ethernet'][0]['ipv4'][0]['pimV4Interface'][0]['href']

        # Based on the list of multicastIpAddress, get all their indexes.
        response = self.ixnObj.get(self.ixnObj.httpHeader+pimObj+'/pimV4JoinPruneList')

        startMcastAddrMultivalue = response.json()['groupV4Address']        
        listOfConfiguredMcastIpAddresses = self.ixnObj.getMultivalueValues(startMcastAddrMultivalue)

        self.ixnObj.logInfo('\nsendPimV4JoinNgpf: List of configured Mcast IP addresses: %s' % listOfConfiguredMcastIpAddresses)
        if listOfConfiguredMcastIpAddresses == []:
            raise IxNetRestApiException('sendPimV4JoinNgpf: No Mcast IP address configured')

        if multicastIpAddress == 'all':
            listOfMcastAddresses = listOfConfiguredMcastIpAddresses
        else:
            listOfMcastAddresses = multicastIpAddress

        # Note: Index position is not zero based.
        indexListToSend = []
        for eachMcastAddress in listOfMcastAddresses:
            index = listOfConfiguredMcastIpAddresses.index(eachMcastAddress)
            indexListToSend.append(index+1)

        url = pimObj+'/pimV4JoinPruneList/operations/%s' % action
        data = {'arg1': [pimObj+'/pimV4JoinPruneList'], 'arg2': indexListToSend}
        self.ixnObj.logInfo('\nsendPimv4JoinNgpf: %s' % url)
        self.ixnObj.logInfo('\t%s' % multicastIpAddress)
        response = self.ixnObj.post(self.ixnObj.httpHeader+url, data=data)
        self.ixnObj.waitForComplete(response, url+response.json()['id'])

    def sendMldJoinNgpf(self, mldObj, ipv6AddressList):
        """
        Description
            For IPv6 only.
            This API will take the MLD object and loop through all the configured ports
            looking for the specified ipv6Address to send a join.

        Parameter
            ipv6AddressList: 'all' or a list of IPv6 addresses that must be EXACTLY how it is configured on the GUI.
        """
        # Loop all port objects to get user specified IPv6 address to send the join.
        portObjectList = mldObj+'/mldMcastIPv6GroupList/port'
        response = self.ixnObj.get(portObjectList)

        for eachPortIdDetails in response.json():
            currentPortId = eachPortIdDetails['id']
            # For each ID, get the 'startMcastAddr' multivalue
            startMcastAddrMultivalue = eachPortIdDetails['startMcastAddr']

            # Go to the multivalue and get the 'values'
            response = self.ixnObj.get(self.ixnObj.httpHeader+startMcastAddrMultivalue)
            listOfConfiguredGroupIpAddresses = response.json()['values']
            if ipv6AddressList == 'all':
                listOfGroupAddresses = listOfConfiguredGroupIpAddresses
            else:
                listOfGroupAddresses = ipv6AddressList

            for eachSpecifiedIpv6Addr in listOfGroupAddresses:
                if eachSpecifiedIpv6Addr in listOfConfiguredGroupIpAddresses:
                    # if 'values' match ipv4Address, do a join on:
                    #      http://192.168.70.127.:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1/mldMcastIPv6GroupList/port/1/operations/mldjoingroup
                    #    arg1: port/1 object
                    url = mldObj+'/mldMcastIPv6GroupList/port/%s/operations/mldjoingroup' % currentPortId
                    portIdObj = mldObj+'/mldMcastIPv6GroupList/port/%s' % currentPortId
                    # portIdObj = http:/{apiServerIp:port}/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1/mldMcastIPv6GroupList/port/1
                    response = self.ixnObj.post(url, data={'arg1': [portIdObj]})
                    self.ixnObj.waitForComplete(response, url+response.json()['id'])

    def sendMldLeaveNgpf(self, mldObj, ipv6AddressList):
        """
        Description
            For IPv6 only.
            This API will take the mld sessionUrl object and loop through all the configured ports
            looking for the specified ipv6Address to send a leave.

        Parameters
            mldObj: http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1
            ipv6AddressList: 'all' or a list of IPv6 addresses that must be EXACTLY how it is configured on the GUI.
        """
        # Loop all port objects to get user specified IPv6 address to send the leave.
        portObjectList = mldObj+'/mldMcastIPv6GroupList/port'
        response = post.get(portObjectList)
        for eachPortIdDetails in response.json():
            currentPortId = eachPortIdDetails['id']
            # For each ID, get the 'startMcastAddr' multivalue
            startMcastAddrMultivalue = eachPortIdDetails['startMcastAddr']

            # Go to the multivalue and get the 'values'
            response = self.ixnObj.get(self.ixnObj.httpHeader+startMcastAddrMultivalue)
            listOfConfiguredGroupIpAddresses = response.json()['values']
            if ipv6AddressList == 'all':
                listOfGroupAddresses = listOfConfiguredGroupIpAddresses
            else:
                listOfGroupAddresses = ipv6AddressList

            for eachSpecifiedIpv6Addr in listOfGroupAddresses:
                if eachSpecifiedIpv6Addr in listOfConfiguredGroupIpAddresses:
                    # if 'values' match ipv4Address, do a join on:
                    #      http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1/mldMcastIPv6GroupList/port/1/operations/mldjoingroup
                    #    arg1: port/1 object
                    url = mldObj+'/mldMcastIPv6GroupList/port/%s/operations/mldleavegroup' % currentPortId
                    portIdObj = mldObj+'/mldMcastIPv6GroupList/port/%s' % currentPortId
                    # portIdObj = http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1/mldMcastIPv6GroupList/port/1
                    response = self.ixnObj.post(url, data={'arg1': [portIdObj]})
                    self.ixnObj.waitForComplete(response, url+response.json()['id'])

    def getSessionStatus(self, protocolObj):
        """
        Description
           Get the object's session status.

        Parameter
           protocolObj: (str): The protocol object.
                        /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1
        Returns
           Success: A list of up|down session status.
           Failed:  An empty list
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader+protocolObj+'?includes=sessionStatus', silentMode=True)
        return response.json()['sessionStatus']

    def getIpAddresses(self, ipObj):
        """
        Description
           Get the configured ipv4|ipv6 addresses in a list.
        
        Parameter
           ipObj: <str>: The IPv4|Ipv6 object: /api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4/1
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader+ipObj)
        multivalueObj = response.json()['address']
        response = self.ixnObj.getMultivalueValues(multivalueObj)
        return response

    def showTopologies(self):
        """
        Description
            Show the NGPF configuration: Topology Groups, Device Groups, Mac Addreseses, VLAN ID,
                                         IPv4, IPv6, protocol sessions.
        """
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',      'properties': ['name', 'status', 'vports'], 'where': []},
                                {'node': 'deviceGroup', 'properties': ['name', 'status'], 'where': []},
                                {'node': 'networkGroup','properties': ['name', 'multiplier'], 'where': []},
                                {'node': 'ethernet',    'properties': ['name', 'status', 'sessionStatus', 'enableVlans', 'mac'], 'where': []},
                                {'node': 'vlan',        'properties': ['name', 'vlanId', 'priority'], 'where': []},
                                {'node': 'ipv4',        'properties': ['name', 'status', 'sessionStatus', 'address', 'gatewayIp', 'prefix'], 'where': []},
                                {'node': 'ipv6',        'properties': ['name', 'status', 'sessionStatus', 'address', 'gatewayIp', 'prefix'], 'where': []},
                                {'node': 'bgpIpv4Peer', 'properties': ['name', 'status', 'sessionStatus', 'dutIp', 'type', 'localIpv4Ver2', 'localAs2Bytes',
                                                                        'holdTimer', 'flap', 'uptimeInSec', 'downtimeInSec'], 'where': []},
                                {'node': 'bgpIpv6Peer', 'properties': ['name', 'status', 'sessionStatus'], 'where': []},
                                {'node': 'ospfv2',      'properties': ['name', 'status', 'sessionStatus'], 'where': []},
                                {'node': 'ospfv3',      'properties': ['name', 'status', 'sessionStatus'], 'where': []},
                                {'node': 'igmpHost',    'properties': ['name', 'status', 'sessionStatus'], 'where': []},
                                {'node': 'igmpQuerier', 'properties': ['name', 'status', 'sessionStatus'], 'where': []},
                                {'node': 'vxlan',       'properties': ['name', 'status', 'sessionStatus'], 'where': []},
                            ]
                    }

        queryResponse = self.ixnObj.query(data=queryData)
        self.ixnObj.logInfo('\n')
        for topology in queryResponse.json()['result'][0]['topology']:
            self.ixnObj.logInfo('TopologyGroup: {0}   Name: {1}'.format(topology['id'], topology['name']))
            self.ixnObj.logInfo('    Status: {0}'.format(topology['status']))
            vportObjList = topology['vports']
            for vportObj in vportObjList:
                vportResponse = self.ixnObj.get(self.ixnObj.httpHeader+vportObj, silentMode=True)
                self.ixnObj.logInfo('    VportId: {0} Name: {1}  AssignedTo: {2}  State: {3}'.format(vportResponse.json()['id'],
                                                                                                vportResponse.json()['name'],
                                                                                                vportResponse.json()['assignedTo'],
                                                                                                vportResponse.json()['state']))
            self.ixnObj.logInfo('\n', end='')

            for deviceGroup in topology['deviceGroup']:
                self.ixnObj.logInfo('    DeviceGroup:{0}  Name:{1}'.format(deviceGroup['id'], deviceGroup['name']))
                self.ixnObj.logInfo('\tStatus: {0}'.format(deviceGroup['status']), end='\n\n')
                for ethernet in deviceGroup['ethernet']:
                    ethernetObj = ethernet['href']
                    ethernetSessionStatus = self.getSessionStatus(ethernetObj)
                    self.ixnObj.logInfo('\tEthernet:{0}  Name:{1}'.format(ethernet['id'], ethernet['name']))
                    self.ixnObj.logInfo('\t    Status: {0}'.format(ethernet['status']))
                    enableVlansResponse = self.ixnObj.get(self.ixnObj.httpHeader+ethernet['enableVlans'], silentMode=True)
                    enableVlansMultivalue = enableVlansResponse.json()['links'][0]['href']
                    enableVlansValues = self.ixnObj.getMultivalueValues(enableVlansMultivalue, silentMode=True)[0]
                    self.ixnObj.logInfo('\t    Vlan enabled: %s\n' % enableVlansValues)

                    if ethernet['ipv6'] == []:
                        ethernet['ipv6'].insert(0, None)

                    for mac,vlan,ipv4,ipv6 in zip(ethernet['mac'], ethernet['vlan'], ethernet['ipv4'], ethernet['ipv6']):
                        ipv4Obj = ipv4['href']
                        ipv4SessionStatus = self.getSessionStatus(ipv4Obj)
                        
                        self.ixnObj.logInfo('\tIPv4:{0} Status: {1}'.format(ipv4['id'], ipv4['status']))
                        macResponse = self.ixnObj.get(self.ixnObj.httpHeader+ethernet['mac'], silentMode=True)
                        macAddress = self.ixnObj.getMultivalueValues(macResponse.json()['links'][0]['href'], silentMode=True)

                        vlanResponse = self.ixnObj.get(self.ixnObj.httpHeader+vlan['vlanId'], silentMode=True)
                        vlanId = self.ixnObj.getMultivalueValues(vlanResponse.json()['links'][0]['href'], silentMode=True)

                        priorityResponse = self.ixnObj.get(self.ixnObj.httpHeader+vlan['priority'], silentMode=True)
                        vlanPriority = self.ixnObj.getMultivalueValues(priorityResponse.json()['links'][0]['href'],
                                                                       silentMode=True)

                        ipResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv4['address'], silentMode=True)
                        ipAddress = self.ixnObj.getMultivalueValues(ipResponse.json()['links'][0]['href'], silentMode=True)

                        gatewayResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv4['gatewayIp'], silentMode=True)
                        gateway = self.ixnObj.getMultivalueValues(gatewayResponse.json()['links'][0]['href'], silentMode=True)

                        prefixResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv4['prefix'], silentMode=True)
                        prefix = self.ixnObj.getMultivalueValues(prefixResponse.json()['links'][0]['href'], silentMode=True)

                        index = 1
                        self.ixnObj.logInfo('\t    {0:8} {1:14} {2:7} {3:9} {4:12} {5:16} {6:12} {7:7} {8:7}'.format('Index', 'MacAddress', 'VlanId', 'VlanPri', 'EthSession',
                                                                                                        'IPv4Address', 'Gateway', 'Prefix', 'Ipv4Session'))
                        self.ixnObj.logInfo('\t    {0}'.format('-'*104))
                        for mac,vlanId,vlanPriority,ethSession,ip,gateway,prefix,ipv4Session in zip(macAddress,
                                                                                                    vlanId,
                                                                                                    vlanPriority,
                                                                                                    ethernetSessionStatus,
                                                                                                    ipAddress,
                                                                                                    gateway,
                                                                                                    prefix,
                                                                                                    ipv4SessionStatus):
                            self.ixnObj.logInfo('\t    {0:^5} {1:18} {2:^6} {3:^9} {4:13} {5:<15} {6:<13} {7:6} {8:7}'.format(index, mac, vlanId, vlanPriority,
                                                                                                    ethSession, ip, gateway, prefix, ipv4Session))
                            index += 1

                        # IPv6
                        if None not in ethernet['ipv6']:
                            ipResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv6['address'], silentMode=True)
                            gatewayResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv6['gatewayIp'], silentMode=True)
                            prefixResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv6['prefix'], silentMode=True)
                            self.ixnObj.logInfo('\n\tIPv6:{0} Status: {1}'.format(ipv6['id'], ipv6['status']))
                            self.ixnObj.logInfo('\t    {0:8} {1:14} {2:7} {3:9} {4:12} {5:19} {6:18} {7:7} {8:7}'.format('Index', 'MacAddress', 'VlanId', 'VlanPri', 'EthSession',
                                                                                                            'IPv6Address', 'Gateway', 'Prefix', 'Ipv6Session'))
                            print('\t   ', '-'*113)
                            for mac,vlanId,vlanPriority,ethSession,ip,gateway,prefix,ipv4Session in zip(macResponse.json()['values'],
                                                                            vlanResponse.json()['values'],
                                                                            priorityResponse.json()['values'],
                                                                            ethernet['sessionStatus'],
                                                                            ipResponse.json()['values'], gatewayResponse.json()['values'],
                                                                            prefixResponse.json()['values'], ipv6['sessionStatus']):
                                self.ixnObj.logInfo('\t    {0:^5} {1:18} {2:^6} {3:^9} {4:13} {5:<15} {6:<13} {7:8} {8:7}'.format(index, mac, vlanId, vlanPriority,
                                                                                                        ethSession, ip, gateway, prefix, ipv4Session))
                                index += 1

                        self.ixnObj.logInfo('\n', end='')
                        if ipv4['bgpIpv4Peer'] != []:
                            for bgpIpv4Peer in ipv4['bgpIpv4Peer']:
                                bgpIpv4PeerHref = bgpIpv4Peer['href']
                                bgpIpv4PeerSessionStatus = self.getSessionStatus(bgpIpv4PeerHref)

                                self.ixnObj.logInfo('\tBGPIpv4Peer:{0}  Name:{1}'.format(bgpIpv4Peer['id'], bgpIpv4Peer['name'],
                                                                                         bgpIpv4Peer['status']))
                                dutIpResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['dutIp'], silentMode=True)
                                dutIp = self.ixnObj.getMultivalueValues(dutIpResponse.json()['links'][0]['href'], silentMode=True)

                                typeResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['type'], silentMode=True)
                                typeMultivalue = typeResponse.json()['links'][0]['href']
                                bgpType = self.ixnObj.getMultivalueValues(typeMultivalue, silentMode=True)

                                localAs2BytesResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['localAs2Bytes'],
                                                                        silentMode=True)
                                localAs2BytesMultivalue = localAs2BytesResponse.json()['links'][0]['href']
                                localAs2Bytes = self.ixnObj.getMultivalueValues(localAs2BytesMultivalue, silentMode=True)

                                flapResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['flap'], silentMode=True)
                                flap = self.ixnObj.getMultivalueValues(flapResponse.json()['links'][0]['href'], silentMode=True)

                                uptimeResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['uptimeInSec'],
                                                                 silentMode=True)
                                uptime = self.ixnObj.getMultivalueValues(uptimeResponse.json()['links'][0]['href'], silentMode=True)
                                downtimeResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['downtimeInSec'],
                                                                   silentMode=True)
                                downtime = self.ixnObj.getMultivalueValues(downtimeResponse.json()['links'][0]['href'],
                                                                           silentMode=True)
                                self.ixnObj.logInfo('\t    Type: {0}  localAs2Bytes: {1}'.format(bgpType[0],
                                                                                                 localAs2Bytes[0]))
                                self.ixnObj.logInfo('\t    Status: {0}'.format(bgpIpv4Peer['status']))
                                index = 1

                                for dutIp,bgpSession,flap,uptime,downtime in zip(dutIp,
                                                                                 bgpIpv4PeerSessionStatus,
                                                                                 flap,
                                                                                 uptime,
                                                                                 downtime):
                                    self.ixnObj.logInfo('\t\t{0}: DutIp:{1}  SessionStatus:{2}  Flap:{3}  upTime:{4}  downTime:{5}'.format(index, dutIp, bgpSession, flap, uptime, downtime))
                                    index += 1

                        for ospfv2 in ipv4['ospfv2']:
                            self.ixnObj.logInfo('\t    OSPFv2:{0}  Name:{1}'.format(ospfv2['id'], ospfv2['name'], ospfv2['status']))
                            self.ixnObj.logInfo('\t\tStatus: {0}'.format(ospfv2['status']), end='\n\n')

                        for igmpHost in ipv4['igmpHost']:
                            self.ixnObj.logInfo('\t    igmpHost:{0}  Name:{1}'.format(igmpHost['id'], igmpHost['name'], igmpHost['status']))
                            self.ixnObj.logInfo('\t\tStatus: {0}'.format(igmpHost['status']), end='\n\n')
                        for igmpQuerier in ipv4['igmpQuerier']:
                            self.ixnObj.logInfo('\t    igmpQuerier:{0}  Name:{1}'.format(igmpQuerier['id'], igmpQuerier['name'], igmpQuerier['status']))
                            self.ixnObj.logInfo('\t\tStatus: {0}'.format(igmpQuerier['status']), end='\n\n')
                        for vxlan in ipv4['vxlan']:
                            self.ixnObj.logInfo('\t    vxlan:{0}  Name:{1}'.format(vxlan['id'], vxlan['name'], vxlan['status']))
                            self.ixnObj.logInfo('\tStatus: {0}'.format(vxlan['status']), end='\n\n')

                for networkGroup in deviceGroup['networkGroup']:
                    self.ixnObj.logInfo('\n\tNetworkGroup:{0}  Name:{1}'.format(networkGroup['id'], networkGroup['name']))
                    self.ixnObj.logInfo('\t    Multiplier: {0}'.format(networkGroup['multiplier']))
                    response = self.ixnObj.get(self.ixnObj.httpHeader+networkGroup['href']+'/ipv4PrefixPools', silentMode=True)
                    prefixPoolHref = response.json()[0]['links'][0]['href']

                    response = self.ixnObj.get(self.ixnObj.httpHeader+response.json()[0]['networkAddress'], silentMode=True)
                    startingAddressMultivalue = response.json()['links'][0]['href']
                    startingAddress = self.ixnObj.getMultivalueValues(startingAddressMultivalue, silentMode=True)[0]
                    endingAddress = self.ixnObj.getMultivalueValues(startingAddressMultivalue, silentMode=True)[-1]
                                        
                    prefixPoolResponse = self.ixnObj.get(self.ixnObj.httpHeader+prefixPoolHref, silentMode=True)
                    self.ixnObj.logInfo('\t    StartingAddress:{0}  EndingAddress:{1}  Prefix:{2}'.format(startingAddress,
                                                                                                          endingAddress,
                                                                                                          response.json()['formatLength']))
                    if None not in ethernet['ipv6']:
                        for ipv6 in ethernet['ipv6']:
                            self.ixnObj.logInfo('\t    IPv6:{0}  Name:{1}'.format(ipv6['id'], ipv6['name']))
                            for bgpIpv6Peer in ipv6['bgpIpv6Peer']:
                                self.ixnObj.logInfo('\t    BGPIpv6Peer:{0}  Name:{1}'.format(bgpIpv6Peer['id'], bgpIpv6Peer['name']))
                            for ospfv3 in ipv6['ospfv3']:
                                self.ixnObj.logInfo('\t    OSPFv3:{0}  Name:{1}'.format(ospfv3['id'], ospfv3['name']))
                            for mldHost in ipv6['mldHost']:
                                self.ixnObj.logInfo('\t    mldHost:{0}  Name:{1}'.format(mldHost['id'], mldHost['name']))
                            for mldQuerier in ipv6['mldQuerier']:
                                self.ixnObj.logInfo('\t    mldQuerier:{0}  Name:{1}'.format(mldQuerier['id'], mldQuerier['name']))
            self.ixnObj.logInfo('\n\n')

    def showTopologies_backup(self):
        """
        Description
            Show the NGPF configuration: Topology Groups, Device Groups, Mac Addreseses, VLAN ID,
                                         IPv4, IPv6, protocol sessions.
        """
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',      'properties': ['name', 'status', 'vports'], 'where': []},
                                {'node': 'deviceGroup', 'properties': ['name', 'status'], 'where': []},
                                {'node': 'networkGroup','properties': ['name', 'multiplier'], 'where': []},
                                {'node': 'ethernet',    'properties': ['name', 'status', 'sessionStatus', 'enableVlans', 'mac'], 'where': []},
                                {'node': 'vlan',        'properties': ['name', 'vlanId', 'priority'], 'where': []},
                                {'node': 'ipv4',        'properties': ['name', 'status', 'sessionStatus', 'address', 'gatewayIp', 'prefix'], 'where': []},
                                {'node': 'ipv6',        'properties': ['name', 'status', 'sessionStatus', 'address', 'gatewayIp', 'prefix'], 'where': []},
                                {'node': 'bgpIpv4Peer', 'properties': ['name', 'status', 'sessionStatus', 'dutIp', 'type', 'localIpv4Ver2', 'localAs2Bytes',
                                                                        'holdTimer', 'flap', 'uptimeInSec', 'downtimeInSec'], 'where': []},
                                {'node': 'bgpIpv6Peer', 'properties': ['name', 'status', 'sessionStatus'], 'where': []},
                                {'node': 'ospfv2',      'properties': ['name', 'status', 'sessionStatus'], 'where': []},
                                {'node': 'ospfv3',      'properties': ['name', 'status', 'sessionStatus'], 'where': []},
                                {'node': 'igmpHost',    'properties': ['name', 'status', 'sessionStatus'], 'where': []},
                                {'node': 'igmpQuerier', 'properties': ['name', 'status', 'sessionStatus'], 'where': []},
                                {'node': 'vxlan',       'properties': ['name', 'status', 'sessionStatus'], 'where': []},
                            ]
                    }

        queryResponse = self.ixnObj.query(data=queryData)
        self.ixnObj.logInfo('\n')
        for topology in queryResponse.json()['result'][0]['topology']:
            self.ixnObj.logInfo('TopologyGroup: {0}   Name: {1}'.format(topology['id'], topology['name']))
            self.ixnObj.logInfo('    Status: {0}'.format(topology['status']))
            vportObjList = topology['vports']
            for vportObj in vportObjList:
                vportResponse = self.ixnObj.get(self.ixnObj.httpHeader+vportObj, silentMode=True)
                self.ixnObj.logInfo('    VportId: {0} Name: {1}  AssignedTo: {2}  State: {3}'.format(vportResponse.json()['id'],
                                                                                                vportResponse.json()['name'],
                                                                                                vportResponse.json()['assignedTo'],
                                                                                                vportResponse.json()['state']))
            self.ixnObj.logInfo('\n', end='')

            for deviceGroup in topology['deviceGroup']:
                self.ixnObj.logInfo('    DeviceGroup:{0}  Name:{1}'.format(deviceGroup['id'], deviceGroup['name']))
                self.ixnObj.logInfo('\tStatus: {0}'.format(deviceGroup['status']), end='\n\n')
                for ethernet in deviceGroup['ethernet']:
                    self.ixnObj.logInfo('\tEthernet:{0}  Name:{1}'.format(ethernet['id'], ethernet['name']))
                    self.ixnObj.logInfo('\t    Status: {0}'.format(ethernet['status']))
                    enableVlansResponse = self.ixnObj.get(self.ixnObj.httpHeader+ethernet['enableVlans'], silentMode=True)
                    enableVlansValues = enableVlansResponse.json()['values'][0] ;# true|false
                    self.ixnObj.logInfo('\t    Vlan enabled: %s\n' % enableVlansValues)

                    if ethernet['ipv6'] == []:
                        ethernet['ipv6'].insert(0, None)

                    for mac,vlan,ipv4,ipv6 in zip(ethernet['mac'], ethernet['vlan'], ethernet['ipv4'], ethernet['ipv6']):
                        self.ixnObj.logInfo('\tIPv4:{0} Status: {1}'.format(ipv4['id'], ipv4['status']))
                        macResponse = self.ixnObj.get(self.ixnObj.httpHeader+ethernet['mac'], silentMode=True)
                        vlanResponse = self.ixnObj.get(self.ixnObj.httpHeader+vlan['vlanId'], silentMode=True)
                        priorityResponse = self.ixnObj.get(self.ixnObj.httpHeader+vlan['priority'], silentMode=True)

                        ipResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv4['address'], silentMode=True)
                        gatewayResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv4['gatewayIp'], silentMode=True)
                        prefixResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv4['prefix'], silentMode=True)
                        index = 1
                        self.ixnObj.logInfo('\t    {0:8} {1:14} {2:7} {3:9} {4:12} {5:16} {6:12} {7:7} {8:7}'.format('Index', 'MacAddress', 'VlanId', 'VlanPri', 'EthSession',
                                                                                                        'IPv4Address', 'Gateway', 'Prefix', 'Ipv4Session'))
                        print('\t   ', '-'*104)
                        for mac,vlanId,vlanPriority,ethSession,ip,gateway,prefix,ipv4Session in zip(macResponse.json()['values'], vlanResponse.json()['values'],
                                                                        priorityResponse.json()['values'],
                                                                        ethernet['sessionStatus'],
                                                                        ipResponse.json()['values'], gatewayResponse.json()['values'],
                                                                        prefixResponse.json()['values'], ipv4['sessionStatus']):
                            self.ixnObj.logInfo('\t    {0:^5} {1:18} {2:^6} {3:^9} {4:13} {5:<15} {6:<13} {7:6} {8:7}'.format(index, mac, vlanId, vlanPriority,
                                                                                                    ethSession, ip, gateway, prefix, ipv4Session))
                            index += 1

                        # IPv6
                        if None not in ethernet['ipv6']:
                            ipResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv6['address'], silentMode=True)
                            gatewayResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv6['gatewayIp'], silentMode=True)
                            prefixResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv6['prefix'], silentMode=True)
                            self.ixnObj.logInfo('\n\tIPv6:{0} Status: {1}'.format(ipv6['id'], ipv6['status']))
                            self.ixnObj.logInfo('\t    {0:8} {1:14} {2:7} {3:9} {4:12} {5:19} {6:18} {7:7} {8:7}'.format('Index', 'MacAddress', 'VlanId', 'VlanPri', 'EthSession',
                                                                                                            'IPv6Address', 'Gateway', 'Prefix', 'Ipv6Session'))
                            print('\t   ', '-'*113)
                            for mac,vlanId,vlanPriority,ethSession,ip,gateway,prefix,ipv4Session in zip(macResponse.json()['values'],
                                                                            vlanResponse.json()['values'],
                                                                            priorityResponse.json()['values'],
                                                                            ethernet['sessionStatus'],
                                                                            ipResponse.json()['values'], gatewayResponse.json()['values'],
                                                                            prefixResponse.json()['values'], ipv6['sessionStatus']):
                                self.ixnObj.logInfo('\t    {0:^5} {1:18} {2:^6} {3:^9} {4:13} {5:<15} {6:<13} {7:8} {8:7}'.format(index, mac, vlanId, vlanPriority,
                                                                                                        ethSession, ip, gateway, prefix, ipv4Session))
                                index += 1

                        self.ixnObj.logInfo('\n', end='')
                        if ipv4['bgpIpv4Peer'] != []:
                            for bgpIpv4Peer in ipv4['bgpIpv4Peer']:
                                self.ixnObj.logInfo('\tBGPIpv4Peer:{0}  Name:{1}'.format(bgpIpv4Peer['id'], bgpIpv4Peer['name'], bgpIpv4Peer['status']))
                                dutIpResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['dutIp'], silentMode=True)
                                localIpAddresses = bgpIpv4Peer['localIpv4Ver2']
                                typeResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['type'], silentMode=True)
                                localAs2BytesResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['localAs2Bytes'], silentMode=True)
                                flapResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['flap'], silentMode=True)
                                uptimeResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['uptimeInSec'], silentMode=True)
                                downtimeResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['downtimeInSec'], silentMode=True)
                                self.ixnObj.logInfo('\t    Type: {0}  localAs2Bytes: {1}'.format(typeResponse.json()['values'][0], localAs2BytesResponse.json()['values'][0]))
                                self.ixnObj.logInfo('\t    Status: {0}'.format(bgpIpv4Peer['status']))
                                index = 1
                                for localIp,dutIp,bgpSession,flap,uptime,downtime in zip(localIpAddresses, dutIpResponse.json()['values'], bgpIpv4Peer['sessionStatus'],
                                                                                        flapResponse.json()['values'], uptimeResponse.json()['values'],
                                                                                        downtimeResponse.json()['values']):
                                    self.ixnObj.logInfo('\t\t{0}: LocalIp: {1}  DutIp: {2}  SessionStatus: {3}  Flap:{4}  upTime:{5} downTime:{6}'.format(index, localIp, dutIp, bgpSession,
                                                                                                                                            flap, uptime, downtime))
                                    index += 1

                        for ospfv2 in ipv4['ospfv2']:
                            self.ixnObj.logInfo('\t\tOSPFv2:{0}  Name:{1}'.format(ospfv2['id'], ospfv2['name'], ospfv2['status']))
                            self.ixnObj.logInfo('\t\t    Status: {0}'.format(ospfv2['status']), end='\n\n')
                        for igmpHost in ipv4['igmpHost']:
                            self.ixnObj.logInfo('\t\tigmpHost:{0}  Name:{1}'.format(igmpHost['id'], igmpHost['name'], igmpHost['status']))
                            self.ixnObj.logInfo('\t\t    Status: {0}'.format(igmpHost['status']), end='\n\n')
                        for igmpQuerier in ipv4['igmpQuerier']:
                            self.ixnObj.logInfo('\t\tigmpQuerier:{0}  Name:{1}'.format(igmpQuerier['id'], igmpQuerier['name'], igmpQuerier['status']))
                            self.ixnObj.logInfo('\t\t    Status: {0}'.format(igmpQuerier['status']), end='\n\n')
                        for vxlan in ipv4['vxlan']:
                            self.ixnObj.logInfo('\t\tvxlan:{0}  Name:{1}'.format(vxlan['id'], vxlan['name'], vxlan['status']))
                            self.ixnObj.logInfo('\t    Status: {0}'.format(vxlan['status']), end='\n\n')

                for networkGroup in deviceGroup['networkGroup']:
                    self.ixnObj.logInfo('\tNetworkGroup:{0}  Name:{1}'.format(networkGroup['id'], networkGroup['name']))
                    self.ixnObj.logInfo('\t    Multiplier:{0}'.format(networkGroup['multiplier']))
                    response = self.ixnObj.get(self.ixnObj.httpHeader+networkGroup['href']+'/ipv4PrefixPools', silentMode=True)
                    response = self.ixnObj.get(self.ixnObj.httpHeader+response.json()[0]['networkAddress'], silentMode=True)
                    self.ixnObj.logInfo('\t    StartingAddress:{0}  EndingAddress:{1}  Prefix:{2}'.format(response.json()['values'][0], response.json()['values'][-1],
                                                                                            response.json()['formatLength']))
                    if None not in ethernet['ipv6']:
                        for ipv6 in ethernet['ipv6']:
                            self.ixnObj.logInfo('\t    IPv6:{0}  Name:{1}'.format(ipv6['id'], ipv6['name']))
                            for bgpIpv6Peer in ipv6['bgpIpv6Peer']:
                                self.ixnObj.logInfo('\t    BGPIpv6Peer:{0}  Name:{1}'.format(bgpIpv6Peer['id'], bgpIpv6Peer['name']))
                            for ospfv3 in ipv6['ospfv3']:
                                self.ixnObj.logInfo('\t    OSPFv3:{0}  Name:{1}'.format(ospfv3['id'], ospfv3['name']))
                            for mldHost in ipv6['mldHost']:
                                self.ixnObj.logInfo('\t    mldHost:{0}  Name:{1}'.format(mldHost['id'], mldHost['name']))
                            for mldQuerier in ipv6['mldQuerier']:
                                self.ixnObj.logInfo('\t    mldQuerier:{0}  Name:{1}'.format(mldQuerier['id'], mldQuerier['name']))
            self.ixnObj.logInfo('\n\n')

    def getBgpObject(self, topologyName=None, bgpAttributeList=None):
        """
        Description
            Get the BGP object from the specified Topology Group name and return the specified attributes

        Parameters
            topologyName: The Topology Group name
            bgpAttributeList: The BGP attributes to get.


        Example:
            bgpAttributeMultivalue = restObj.getBgpObject(topologyName='Topo1', bgpAttributeList=['flap', 'uptimeInSec', 'downtimeInSec'])
            restObj.configMultivalue(bgpAttributeMultivalue['flap'],          multivalueType='valueList',   data={'values': ['true', 'true']})
            restObj.configMultivalue(bgpAttributeMultivalue['uptimeInSec'],   multivalueType='singleValue', data={'value': '60'})
            restObj.configMultivalue(bgpAttributeMultivalue['downtimeInSec'], multivalueType='singleValue', data={'value': '30'})
        """
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': [{'property': 'name', 'regex': topologyName}]},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',    'properties': [], 'where': []},
                              {'node': 'ipv4',        'properties': [], 'where': []},
                              {'node': 'bgpIpv4Peer', 'properties': bgpAttributeList, 'where': []}]
                    }
        queryResponse = self.ixnObj.query(data=queryData)
        try:
            bgpHostAttributes = queryResponse.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv4'][0]['bgpIpv4Peer'][0]
            return bgpHostAttributes
        except IndexError:
            raise IxNetRestApiException('\nVerify the topologyName and bgpAttributeList input: {0} / {1}\n'.format(topologyName, bgpAttributeList))

    def getDeviceGroupByRouterId(self, routerId):
        """
        Description
            Get the Device Group object based on the router ID.

        Parameter
            routerId: The  Device Group's router ID.

        Return
            The Device Group object
            0 if router ID is not found in any Device Group.
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/topology')
        for topology in response.json():
            topologyObj = topology['links'][0]['href']
            response = self.ixnObj.get(self.ixnObj.httpHeader+topologyObj+'/deviceGroup')
            for deviceGroup in response.json():
                deviceGroupObj = deviceGroup['links'][0]['href']
                response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroupObj+'/routerData')
                routeDataMultivalue = response.json()[0]['routerId']
                routerIdList = self.ixnObj.getMultivalueValues(routeDataMultivalue)
                if routerId in routerIdList:
                    return deviceGroupObj
        return 0

    def isRouterIdInDeviceGroupObj(self, routerId, deviceGroupObj):
        routerIdMultivalue = deviceGroup['routerData'][0]['routerId']
        routerIdList = self.ixnObj.getMultivalueValues(routerIdMultivalue, silentMode=True)

    def configBgpNumberOfAs(self, routerId, numberOfAs):
        """
        Description
            Set the total number of BGP AS # List.
            In the GUI, under NetworkGroup, BGP Route Range tab, bottom tab ASPathSegments, enter number of AS # Segments.

            NOTE! 
                Currently, this API will get the first Network Group object even if there are multiple
                Network Groups. Network Groups could be filtered by the name or by the first route range 
                address.  Haven't decided yet. Don't want to filter by name because in a situation 
                where customers are also using Spirent, Spirent doesn't go by name.

        Parameters
            routerId: The Device Group router ID
            numberOfAs: The total number of AS list to create.

        Requirements
            getDeviceGroupByRouterId()
        """
        deviceGroupObj = self.getDeviceGroupByRouterId(routerId=routerId)
        if deviceGroupObj == 0:
            raise IxNetRestApiException('No Device Group found for router ID: %s' % routerId)

        queryData = {'from': deviceGroupObj,
                    'nodes': [{'node': 'networkGroup',    'properties': [], 'where': []},
                              {'node': 'ipv4PrefixPools', 'properties': [], 'where': []},
                              {'node': 'bgpIPRouteProperty', 'properties': [], 'where': []},
                              {'node': 'bgpAsPathSegmentList', 'properties': [], 'where': []}
                          ]}
        queryResponse = self.ixnObj.query(data=queryData)
        try:
            bgpStack = queryResponse.json()['result'][0]['networkGroup'][0]['ipv4PrefixPools'][0]['bgpIPRouteProperty'][0]['bgpAsPathSegmentList']
        except:
            raise IxNetRestApiException('No object found in DeviceGroup object:  deviceGroup/networkGroup/ipv4PrefixPools/bgpIPRouteProperty/bgpAsPathSegmentList: %s' % deviceGroupObj)

        if bgpStack == []:
            return IxNetRestApiException('No ipv4PrefixPools bgpIPRouteProperty object found.')

        bgpRouteObj = bgpStack[0]['href']
        response = self.ixnObj.get(self.ixnObj.httpHeader+bgpRouteObj)
        asNumberInSegmentMultivalue = response.json()['numberOfAsNumberInSegment']
        self.ixnObj.patch(self.ixnObj.httpHeader+bgpRouteObj, data={'numberOfAsNumberInSegment': numberOfAs})

    def configBgpAsPathSegmentListNumber(self, routerId, asNumber, indexAndAsNumber):
        """
        Description
            Set BGP AS numbers in the route range. 
            If there are 5 AS# created under "Number of AS# In Segment-1", the asNumberList is
            the AS# that you want to modify for all route ranges (Device Group multiplier). 
            The indexAndAsNumber is the route range index and value: [3, 300].
            3 = the 2nd route range (zero based) and 300 is the value.

            NOTE! 
                Currently, this API will get the first Network Group object even if there are multiple
                Network Groups. Network Groups could be filtered by the name or by the first route range 
                address.  Haven't decided yet. Don't want to filter by name because in a situation 
                where customers are also using Spirent, Spirent doesn't go by name.

        Parameters
            routerId: The Device Group router ID where the BGP is configured.
            asListNumber: 1|2|3|...|6|..:  The AS# to modify.
                          (On GUI, click NetworkGroup, on bottom tab asPathSegment,
                           and on top tab, use the "Number of AS# In Segment-1" to set number of AS#1 or AS#2 or AS#3.)
            indexAndAsNumber: all|a list of indexes with as# -> [[1, 100], [3, 300], ...]

        Example:
            protocolObj.configBgpAsPathSegmentListNumber(routerid='195.0.0.2', 3, [[0,28], [3,298], [4, 828]])

        Requirements:
            getDeviceGroupByRouterId()
            getMultivalues()
            configMultivalues()
        """
        deviceGroupObj = self.getDeviceGroupByRouterId(routerId=routerId)
        if deviceGroupObj == 0:
            raise IxNetRestApiException('No Device Group found for router ID: %s' % routerId)

        queryData = {'from': deviceGroupObj,
                    'nodes': [{'node': 'networkGroup',    'properties': [], 'where': []},
                              {'node': 'ipv4PrefixPools', 'properties': [], 'where': []},
                              {'node': 'bgpIPRouteProperty', 'properties': [], 'where': []},
                              {'node': 'bgpAsPathSegmentList', 'properties': [], 'where': []},
                              {'node': 'bgpAsNumberList', 'properties': [], 'where': []}
                          ]}
        queryResponse = self.ixnObj.query(data=queryData)
        try:
            bgpStack = queryResponse.json()['result'][0]['networkGroup'][0]['ipv4PrefixPools'][0]['bgpIPRouteProperty'][0]['bgpAsPathSegmentList'][0]['bgpAsNumberList'][int(asNumber)-1]
        except:
            raise IxNetRestApiException('No object found in DeviceGroup object:  deviceGroup/networkGroup/ipv4PrefixPools/bgpIPRouteProperty/bgpAsPathSegmentList/bgpAsNumberlist: %s' % deviceGroupObj)

        if bgpStack == []:
            return IxNetRestApiException('No ipv4PrefixPools bgpIPRouteProperty object found.')

        bgpRouteObj = bgpStack['href']
        response = self.ixnObj.get(self.ixnObj.httpHeader+bgpRouteObj)
        asNumberMultivalue = response.json()['asNumber']
        asNumberValueList = self.ixnObj.getMultivalueValues(asNumberMultivalue)
        try:
            for eachIndexAsNumber in indexAndAsNumber:
                index = eachIndexAsNumber[0]
                asNumber = eachIndexAsNumber[1]
                asNumberValueList[index] = str(asNumber)
        except:
            raise IxNetRestApiException('The index that you indicated is out of range for the current AS list')
 
        self.ixnObj.logInfo('\nConfiguruing: %s' % bgpRouteObj)
        self.ixnObj.configMultivalue(asNumberMultivalue, 'valueList', {'values': asNumberValueList})

    def configBgpAsSetMode(self, routerId, asSetMode):
        """
        Description
            Configure BGP Route Range AS Path: AS # Set Mode. This API will change all
            indexes to the specified asSetMode
            Note: In GUI, under Route Range, BGP IP Route Range.

        Parameters
            asSetMode:
                Options: "dontincludelocalas",
                         "includelocalasasasseq",
                         "includelocalasasasset",
                         "includelocalasasasseqconfederation",
                         "includelocalasasassetconfederation",
                         "prependlocalastofirstsegment"
        """
        deviceGroupObj = self.getDeviceGroupByRouterId(routerId=routerId)
        if deviceGroupObj == 0:
            raise IxNetRestApiException('No Device Group found for router ID: %s' % routerId)

        queryData = {'from': deviceGroupObj,
                    'nodes': [{'node': 'networkGroup',    'properties': [], 'where': []},
                              {'node': 'ipv4PrefixPools', 'properties': [], 'where': []},
                              {'node': 'bgpIPRouteProperty', 'properties': [], 'where': []}]
                    }
        queryResponse = self.ixnObj.query(data=queryData)
        bgpStack = queryResponse.json()['result'][0]['networkGroup'][0]['ipv4PrefixPools'][0]['bgpIPRouteProperty']
        if bgpStack == []:
            return IxNetRestApiException('No ipv4PrefixPools bgpIPRouteProperty object found.')

        bgpRouteObj = bgpStack[0]['href']
        response = self.ixnObj.get(self.ixnObj.httpHeader+bgpRouteObj)        
        asSetModeMultivalue = response.json()['asSetMode']
        count = response.json()['count']
        newList = [asSetMode for counter in range(0,count)]
        self.ixnObj.configMultivalue(asSetModeMultivalue, 'valueList', {'values': newList})
