# PLEASE READ DISCLAIMER
#
#    This class demonstrates sample IxNetwork REST API usage for
#    demo and reference purpose only.
#    It is subject to change for updates without warning.
#
# Getting object handles:
#    getNgpfObjectHandleByName: Get the NGPF object handle by the NGPF component name.
#    getDeviceGroupByRouterId: Get the NGPF object handle by the Router ID.
#
#    ethernetObj = self.getNgpfObjectHandleByRouterId(routerId=routerId, ngpfEndpointObject='ethernet')
#
#    Get any NGPF object handle by host IP:
#       x = protocolObj.getProtocolListByHostIpNgpf('1.1.1.1')
#       objHandle = protocolObj.getProtocolObjFromHostIp(x, protocol='bgpIpv4Peer')
#
#    Get any NGPF object handle by either the physical port or by the vport name.
#       x = protocolObj.getProtocolListByPortNgpf(port=['192.168.70.120', '1', '1'])
#       x = protocolObj.getProtocolListByPortNgpf(portName='1/1')
#       objHandle = protocolObj.getProtocolObjFromProtocolList(x['deviceGroup'], 'bgpIpv4Peer')
#
#       Filter by the deviceGroupName if there are multiple device groups
#       x = protocolObj.getProtocolObjFromProtocolList(x['deviceGroup'], 'ethernet', deviceGroupName='DG2')
#
#    Get a NGPF object handle that is configured in a Device Group by the name.
#    x = protocolObj.getEndpointObjByDeviceGroupName('DG-2', 'bgpIpv4Peer')
#

import re, time
from .IxNetRestApi import IxNetRestApiException
from .IxNetRestApiPortMgmt import PortMgmt
from .IxNetRestApiStatistics import Statistics

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
           portMgmtObj: <str>: Optional. This is deprecated. Leaving it here for backward compatibility.
        """
        self.ixnObj = ixnObj
        self.configuredProtocols = []
        self.portMgmtObj = PortMgmt(self.ixnObj)
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

        self.ixnObj.logInfo('Create new Topology Group')
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

        self.ixnObj.logInfo('Create new Device Group')
        response = self.ixnObj.post(url, data=deviceGroupData)
        deviceGroupObj = response.json()['links'][0]['href']
        return deviceGroupObj

    def configLacpNgpf(self, ethernetObj, **kwargs):
        """
        Description
            Create new LACP group.

        Parameter
            ethernetObj: <str>: The Ethernet stack object to create the LACP.
                         Example: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1

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
        
        self.ixnObj.logInfo('Create new LACP NGPF')
        lacpResponse = self.ixnObj.get(self.ixnObj.httpHeader+lacpObj)

        lacpAttributes = ['administrativeKey', 'actorSystemId', 'actorSystemPriority', 'actorKey', 'actorPortNumber', 'actorPortPriority']

        data = {}
        for lacpAttribute in lacpAttributes:
            if lacpAttribute in kwargs:
                multiValue = lacpResponse.json()[lacpAttribute]
                self.ixnObj.logInfo('Configuring LACP attribute: %s' % lacpAttribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': kwargs[lacpAttribute]})
                data.update({'value': kwargs[lacpAttribute]})

        return lacpObj

    def createEthernetNgpf(self, obj=None, port=None, portName=None, ngpfEndpointName=None, **kwargs):
        """
        Description
           This API is for backward compatiblility.  Use self.configEthernetNgpf()
        """
        ethernetObj = self.configEthernetNgpf(obj=obj, port=port, portName=portName, ngpfEndpointName=ngpfEndpointName, **kwargs)
        return ethernetObj

    def configEthernetNgpf(self, obj=None, port=None, portName=None, ngpfEndpointName=None, **kwargs):
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
        if obj != None:
            if 'ethernet' not in obj:
                url = self.ixnObj.httpHeader+obj + '/ethernet'
                self.ixnObj.logInfo('Create new Ethernet on NGPF')
                response = self.ixnObj.post(url)
                ethernetObj = response.json()['links'][0]['href']

            # To modify 
            if 'ethernet' in obj:
                ethernetObj = obj
                createNewEthernetObj = False

        # To modify
        if ngpfEndpointName:
            ethernetObj = self.getNgpfObjectHandleByName(ngpfEndpointName=ngpfEndpointName, ngpfEndpointObject='ethernet')
            createNewEthernetObj = False

        # To modify
        if port:
            x = self.getProtocolListByPortNgpf(port=port)
            ethernetObj = self.getProtocolObjFromProtocolList(x['deviceGroup'], 'ethernet')[0]
            createNewEthernetObj = False

        # To modify
        if portName:
            x = self.getProtocolListByPortNgpf(portName=portName)
            ethernetObj = self.getProtocolObjFromProtocolList(x['deviceGroup'], 'ethernet')[0]
            createNewEthernetObj = False

        ethObjResponse = self.ixnObj.get(self.ixnObj.httpHeader+ethernetObj)

        if 'ethernetName' in kwargs or 'name' in kwargs:
            if 'ethernetName' in kwargs:
                # This is to handle backward compatibility. This attribute should not be created. 
                # Should be using 'name'.
                name = kwargs['ethernetName']
            if 'name' in kwargs:
                name = kwargs['name']
                self.ixnObj.logInfo('Configure MAC address name')
            self.ixnObj.patch(self.ixnObj.httpHeader+ethernetObj, data={'name': name})

        if 'multiplier' in kwargs:
            self.configDeviceGroupMultiplier(objectHandle=ethernetObj, multiplier=kwargs['multiplier'], applyOnTheFly=False)

        if 'macAddress' in kwargs:
            multivalue = ethObjResponse.json()['mac']
            self.ixnObj.logInfo('Configure MAC address. Attribute for multivalueId = jsonResponse["mac"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['macAddress'])

            # Config Mac Address Port Step
            if 'macAddressPortStep' in kwargs:
                self.ixnObj.logInfo('Configure MAC address port step')
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
                self.ixnObj.logInfo('Enabling VLAN ID.  Attribute for multivalueId = jsonResponse["enablevlans"]')
                self.configMultivalue(multivalue, 'singleValue', data={'value': True})
                
            # CREATE vlan object (Creating vlanID always /vlan/1 and then do a get for 'vlanId')
            vlanIdObj = self.ixnObj.httpHeader+ethernetObj+'/vlan/1'
            vlanIdResponse = self.ixnObj.get(vlanIdObj)
            multivalue = vlanIdResponse.json()['vlanId']

            # CONFIG VLAN ID
            self.ixnObj.logInfo('Configure VLAN ID. Attribute for multivalueId = jsonResponse["vlanId"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['vlanId'])

        # CONFIG VLAN PRIORITY
        if 'vlanPriority' in kwargs and kwargs['vlanPriority'] != None:
            multivalue = vlanIdResponse.json()['priority']
            self.ixnObj.logInfo('Configure VLAN ID priority. Attribute for multivalue = jsonResponse["priority"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['vlanPriority'])

        if 'mtu' in kwargs and kwargs['mtu'] != None:
            multivalue = ethObjResponse.json()['mtu']
            self.ixnObj.logInfo('Configure MTU. Attribute for multivalueId = jsonResponse["mtu"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['mtu'])
            
        return ethernetObj

    # Was configIsIsL3Ngpf
    def configIsIsL3Ngpf(self, obj, **data):
        """
        Description
            Create or modify ethernet/ISISL3

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
            response = self.ixnObj.post(url, data=data)
            isisObj = response.json()['links'][0]['href']
            
        response = self.ixnObj.get(self.ixnObj.httpHeader+isisObj)
        self.configuredProtocols.append(isisObj)
        return isisObj

    def getDeviceGroupIsIsL3RouterObj(self, deviceGroupObj):
        """ 
        Description
           Get and the Device Group's ISIS L3 Router object.
           Mainly used after configIsIsNgpf().
          
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
           Configure ISIS L3 Router.

        Parameter
           isisL3RouterObj: <str:obj>: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/isisL3Router/{id}

           data: <dict>:  Get attributes from the IxNetwork API browser.
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader + isisL3RouterObj)

        if 'enableBIER' in data:
            self.ixnObj.patch(self.ixnObj.httpHeader + isisL3RouterObj, data={'enableBIER': data['enableBIER']})

        # Note: Feel free to add additional parameters.
        for attribute in ['active', 'bierNFlag', 'bierRFlag']:
            if attribute in data:
                multivalue = response.json()[attribute]
                self.ixnObj.logInfo('Configuring ISIS BIER Subdomain multivalue attribute: %s' % attribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multivalue+"/singleValue", data={'value': data[attribute]})

    def configIsIsBierSubDomainListNgpf(self, isisL3RouterObj, **data):
        """
        Description
           Configure ISIS BIER Subdomain.

        Parameter
           isisL3RouterObj: <str:obj>: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/isisL3Router/{id}

           data: <dict>:  active, subDomainId, BAR
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader + isisL3RouterObj + '/isisBierSubDomainList')
        for attribute in ['active', 'subDomainId', 'BAR']:
            if attribute in data:
                multiValue = response.json()[attribute]
                self.ixnObj.logInfo('Configuring ISIS DIER Subdomain multivalue attribute: %s' % attribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': data[attribute]})

    def createIpv4Ngpf(self, obj=None, port=None, portName=None, ngpfEndpointName=None, **kwargs):
        """
        Description
           This API is for backward compatiblility.  Use self.configIpv4Ngpf()
        """
        ipv4Obj = self.configIpv4Ngpf(obj=obj, port=port, portName=portName, ngpfEndpointName=ngpfEndpointName, **kwargs)
        return ipv4Obj

    def configIpv4Ngpf(self, obj=None, port=None, portName=None, ngpfEndpointName=None, **kwargs):
        """
        Description
            Create or modify NGPF IPv4.
            To create a new IPv4 stack in NGPF, pass in the Ethernet object.
            If modifying, there are four options. 2-4 will query for the IP object handle.

               1> Provide the IPv4 object handle using the obj parameter.
               2> Set port: The physical port.
               3> Set portName: The vport port name.
               4> Set NGPF IP name that you configured.

        Parameters
            obj: <str>: None or Ethernet obj: '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1'
                                IPv4 obj: '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1'

            port: <list>: Format: [ixChassisIp, str(cardNumber), str(portNumber)]
            portName: <str>: The virtual port name.
            ngpfEndpointName: <str>: The name that you configured for the NGPF BGP.

            kwargs:
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

        Example to create a new IPv4 object:
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

        if obj != None:
            if 'ipv4' in obj:
                # To modify IPv4
                ipv4Obj = obj
                createNewIpv4Obj = False
            else:
                # To create a new IPv4 object
                ipv4Url = self.ixnObj.httpHeader+obj+'/ipv4'
                self.ixnObj.logInfo('Creating new IPv4 in NGPF')
                response = self.ixnObj.post(ipv4Url)
                ipv4Obj = response.json()['links'][0]['href']

        # To modify
        if ngpfEndpointName:
            ipv4Obj = self.getNgpfObjectHandleByName(ngpfEndpointName=ngpfEndpointName, ngpfEndpointObject='ipv4')
            createNewIpv4Obj = False

        # To modify
        if port:
            x = self.getProtocolListByPortNgpf(port=port)
            ipv4Obj = self.getProtocolObjFromProtocolList(x['deviceGroup'], 'ipv4')[0]
            createNewIpv4Obj = False

        # To modify
        if portName:
            x = self.getProtocolListByPortNgpf(portName=portName)
            ipv4Obj = self.getProtocolObjFromProtocolList(x['deviceGroup'], 'ipv4')[0]
            createNewIpv4Obj = False

        ipv4Response = self.ixnObj.get(self.ixnObj.httpHeader+ipv4Obj)

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+ipv4Obj, data={'name': kwargs['name']})

        if 'multiplier' in kwargs:
            self.configDeviceGroupMultiplier(objectHandle=ipv4Obj, multiplier=kwargs['multiplier'], applyOnTheFly=False)

        # Config IPv4 address
        if 'ipv4Address' in kwargs:
            multivalue = ipv4Response.json()['address']
            self.ixnObj.logInfo('Configuring IPv4 address. Attribute for multivalueId = jsonResponse["address"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['ipv4Address'])

        # Config IPv4 port step
        # disabled|0.0.0.1
        if 'ipv4AddressPortStep' in kwargs:
            portStepMultivalue = self.ixnObj.httpHeader+multivalue+'/nest/1'
            self.ixnObj.logInfo('Configure IPv4 address port step')
            if kwargs['ipv4AddressPortStep'] != 'disabled':
                self.ixnObj.patch(portStepMultivalue, data={'step': kwargs['ipv4AddressPortStep']})
            if kwargs['ipv4AddressPortStep'] == 'disabled':
                self.ixnObj.patch(portStepMultivalue, data={'enabled': False})

        # Config Gateway
        if 'gateway' in kwargs:
            multivalue = ipv4Response.json()['gatewayIp']
            self.ixnObj.logInfo('Configure IPv4 gateway. Attribute for multivalueId = jsonResponse["gatewayIp"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['gateway'])

        # Config Gateway port step
        if 'gatewayPortStep' in kwargs:
            portStepMultivalue = self.ixnObj.httpHeader+multivalue+'/nest/1'
            self.ixnObj.logInfo('Configure IPv4 gateway port step')
            if kwargs['gatewayPortStep'] != 'disabled':
                self.ixnObj.patch(portStepMultivalue, data={'step': kwargs['gatewayPortStep']})
            if kwargs['gatewayPortStep'] == 'disabled':
                self.ixnObj.patch(portStepMultivalue, data={'enabled': False})

        # Config resolve gateway
        if 'resolveGateway' in kwargs:
            multivalue = ipv4Response.json()['resolveGateway']
            self.ixnObj.logInfo('Configure IPv4 gateway to resolve gateway. Attribute for multivalueId = jsonResponse["resolveGateway"]')
            self.configMultivalue(multivalue, 'singleValue', data={'value': kwargs['resolveGateway']})

        if 'prefix' in kwargs:
            multivalue = ipv4Response.json()['prefix']
            self.ixnObj.logInfo('Configure IPv4 prefix. Attribute for multivalueId = jsonResponse["prefix"]')
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
            obj: <str>: To create new DHCP obj.
                 Example: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1

            obj: <str>: To Modify DHCP client.
                 Example: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/dhcpv4client/1

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
            self.ixnObj.logInfo('Create new DHCP client V4')
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
                self.ixnObj.logInfo('Configuring DHCP Client attribute: %s' % dhcpAttribute)
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
            self.ixnObj.logInfo('Create new DHCP server v4')
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
                self.ixnObj.logInfo('Configuring DHCP Server attribute: %s' % dhcpAttribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': kwargs[dhcpAttribute]})

        if 'multiplier' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+dhcpObj, data={'multiplier': kwargs['multiplier']})

        dhcpServerSessionObjResponse = self.ixnObj.get(self.ixnObj.httpHeader+dhcpObj+'/dhcp4ServerSessions')
        dhcpServerSessionAttributes = ['defaultLeaseTime', 'echoRelayInfo', 'ipAddress', 'ipAddressIncrement',
                                       'ipDns1', 'ipDns2', 'ipGateway', 'ipPrefix', 'poolSize']

        for dhcpAttribute in dhcpServerSessionAttributes:
            if dhcpAttribute in kwargs:
                multiValue = dhcpServerSessionObjResponse.json()[dhcpAttribute]
                self.ixnObj.logInfo('Configuring DHCP Server session attribute: %s' % dhcpAttribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': kwargs[dhcpAttribute]})

        #self.configuredProtocols.append(dhcpObj)
        return dhcpObj

    def configOspf(self, obj=None, routerId=None, port=None, portName=None, ngpfEndpointName=None, hostIp=None, **kwargs):
        """
        Description
            Create or modify OSPF. If creating a new OSPF, provide an IPv4 object handle.
            If modifying a OSPF, there are five options. 2-6 will query for the OSPF object handle.

               1> Provide the OSPF object handle using the obj parameter.
               2> Set routerId.
               3> Set port: The physical port.
               4> Set portName: The vport port name.
               5> Set NGPF OSPF name that you configured.
               6> Set hostIp: The src IP.

        Parameters
            IPv4 object handle example:
               obj: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1

            OSPF object handle example:
               obj: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/ospfv2/1

            routerId: <str>: The router ID IP address.
            port: <list>: Format: [ixChassisIp, str(cardNumber), str(portNumber)]
            portName: <str>: The virtual port name.
            ngpfEndpointName: <str>: The name that you configured for the NGPF endpoint.
            hostIp: <src>: The source IP address to query for the object.
            kwargs: OSPF configuration attributes. The attributes could be obtained from the IxNetwork API browser.

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
        if obj != None:
            if 'ospf' not in obj:
                ospfUrl = self.ixnObj.httpHeader+obj+'/ospfv2'
                self.ixnObj.logInfo('Create new OSPFv2 in NGPF')
                response = self.ixnObj.post(ospfUrl)
                # /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/ospfv2/1
                ospfObj = response.json()['links'][0]['href']

            # To modify OSPF
            if 'ospf' in obj:
                ospfObj = obj

        # To modify
        if ngpfEndpointName:
            ospfObj = self.getNgpfObjectHandleByName(ngpfEndpointName=ngpfEndpointName, ngpfEndpointObject='ospfv2')

        # To modify
        if port:
            x = self.getProtocolListByPortNgpf(port=port)
            ospfObj = self.getProtocolObjFromProtocolList(x['deviceGroup'], 'ospvv2')[0]

        # To modify
        if portName:
            x = self.getProtocolListByPortNgpf(portName=portName)
            ospfObj = self.getProtocolObjFromProtocolList(x['deviceGroup'], 'ospfv2')[0]

        # To modify
        if routerId:
            ospfObj = self.getNgpfObjectHandleByRouterId(routerId=routerId, ngpfEndpointObject='ospfv2')

        # To modify
        if hostIp:
            x = self.getProtocolListByHostIpNgpf(hostIp)
            ospfObj = self.getProtocolObjFromHostIp(x, protocol='ospfv2')

        ospfObjResponse = self.ixnObj.get(self.ixnObj.httpHeader+ospfObj)

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+ospfObj, data={'name': kwargs['name']})

        # All of these BGP attributes configures multivalue singleValue. So just loop them to do the same thing.
        ospfAttributes = ['areaId', 'neighborIp', 'helloInterval', 'areadIdIp', 'networkType', 'deadInterval']

        for ospfAttribute in ospfAttributes:
            if ospfAttribute in kwargs:
                multiValue = ospfObjResponse.json()[ospfAttribute]
                self.ixnObj.logInfo('Configuring OSPF attribute: %s' % ospfAttribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': kwargs[ospfAttribute]})

        self.configuredProtocols.append(ospfObj)
        return ospfObj

    def configBgp(self, obj=None, routerId=None, port=None, portName=None, ngpfEndpointName=None, hostIp=None, **kwargs):
        """
        Description
            Create or modify BGP.  If creating a new BGP, provide an IPv4 object handle.
            If modifying a BGP, there are five options. 2-6 will query for the BGP object handle.

               1> Provide the BGP object handle using the obj parameter.
               2> Set routerId.
               3> Set port: The physical port.
               4> Set portName: The vport port name.
               5> Set NGPF BGP name that you configured.
               6> Set hostIp: The src IP.

        Parameters
            obj: <str>: None or Either an IPv4 object or a BGP object.
               If creating new bgp object:
                  IPv4 object example: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1
               If modifying, you could provide the bgp object handle using the obj parameter:
                  BGP object example: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1
            
            routerId: <str>: The router ID IP address.
            port: <list>: Format: [ixChassisIp, str(cardNumber), str(portNumber)]
            portName: <str>: The virtual port name.
            ngpfEndpointName: <str>: The name that you configured for the NGPF endpoint.
            hostIp: <src>: The source IP address to query for the object.
            kwargs: BGP configuration attributes. The attributes could be obtained from the IxNetwork API browser.

        Syntax
            POST:  /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/bgpIpv4Peer
            PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/bgpIpv4Peer/{id}

        Example: Create a new bgp object...
            configBgp(ipv4Obj,
                  name = 'bgp_1',
                  enableBgp = True,
                  holdTimer = 90,
                  dutIp={'start': '1.1.1.2', 'direction': 'increment', 'step': '0.0.0.0'},
                  localAs2Bytes=101,
                  enableGracefulRestart = False,
                  restartTime = 45,
                  type = 'internal',
                  enableBgpIdSameasRouterId = True

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/bgpIpv4Peer/{id}
        """
        # To create a new BGP stack using IPv4 object.
        if obj != None:
            if 'bgp' not in obj:
                bgpUrl = self.ixnObj.httpHeader+obj+'/bgpIpv4Peer'
                self.ixnObj.logInfo('Create new BGP in NGPF')
                response = self.ixnObj.post(bgpUrl)
                # /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1
                bgpObj = response.json()['links'][0]['href']

            # To modify BGP by providing a BGP object handle.
            if 'bgp' in obj:
                bgpObj = obj

        # To modify
        if ngpfEndpointName:
            bgpObj = self.getNgpfObjectHandleByName(ngpfEndpointName=ngpfEndpointName, ngpfEndpointObject='bgpIpv4Peer')

        # To modify
        if port:
            x = self.getProtocolListByPortNgpf(port=port)
            bgpObj = self.getProtocolObjFromProtocolList(x['deviceGroup'], 'bgpIpv4Peer')[0]

        # To modify
        if portName:
            x = self.getProtocolListByPortNgpf(portName=portName)
            bgpObj = self.getProtocolObjFromProtocolList(x['deviceGroup'], 'bgpIpv4Peer')[0]

        # To modify
        if routerId:
            bgpObj = self.getNgpfObjectHandleByRouterId(routerId=routerId, ngpfEndpointObject='bgpIpv4Peer')

        # To modify
        if hostIp:
            x = self.getProtocolListByHostIpNgpf(hostIp)
            bgpObj = self.getProtocolObjFromHostIp(x, protocol='bgpIpv4Peer')

        bgpObjResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpObj)

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+bgpObj, data={'name': kwargs['name']})

        if 'enableBgp' in kwargs and kwargs['enableBgp'] == True:
            multiValue = bgpObjResponse.json()['enableBgpId']
            self.ixnObj.logInfo('Enabling BGP protocol. Attribut for multivalue = enableBgpId')
            self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': True})

        if 'dutIp' in kwargs:
            multiValue = bgpObjResponse.json()['dutIp']
            self.ixnObj.logInfo('Configure BGP DUT IP. Attribut for multivalue = dutIp')
            self.configMultivalue(multiValue, 'counter', data=kwargs['dutIp'])

        # All of these BGP attributes configures multivalue singleValue. So just loop them to do the same thing.
        # Note: Don't include flap.  Call flapBgp instead because the uptime and downtime needs to be configured.
        bgpAttributes = ['localAs2Bytes', 'localAs4Bytes', 'enable4ByteAs', 'enableGracefulRestart', 'restartTime', 'type',
                         'staleTime', 'holdTimer', 'enableBgpIdSameasRouterId']

        for bgpAttribute in bgpAttributes:
            if bgpAttribute in kwargs:
                multiValue = bgpObjResponse.json()[bgpAttribute]
                self.ixnObj.logInfo('Configuring BGP multivalue attribute: %s' % bgpAttribute)
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
            self.ixnObj.logInfo('Create new IGMP V4 host')
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
                self.ixnObj.logInfo('Configuring IGMP host attribute: %s' % igmpAttribute)
                self.ixnObj.patch(self.ixnObj.httpHeader+multiValue+"/singleValue", data={'value': kwargs[igmpAttribute]})

        self.configuredProtocols.append(igmpObj)
        return igmpObj

    def configMpls(self, ethernetObj, **kwargs):
        """
        Description
            Create or modify static MPLS.  

        Parameters
            ethernetObj: <str>: The Ethernet object handle.
                         Example: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}

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
            self.ixnObj.logInfo('Create new MPLS protocol in NGPF')
            response = self.ixnObj.post(mplsUrl)
            mplsObj = response.json()['links'][0]['href']

        # To modify MPLS
        if 'mpls' in ethernetObj:
            mplsObj = ethernetObj

        self.ixnObj.logInfo('GET ATTRIBUTE MULTIVALUE IDs')
        mplsResponse = self.ixnObj.get(self.ixnObj.httpHeader+mplsObj)

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+mplsObj, data={'name': kwargs['name']})

        # All of these mpls attributes configures multivalue counter. So just loop them to do the same thing.
        mplsAttributes = ['rxLabelValue', 'txLabelValue', 'destMac', 'cos', 'ttl']

        for mplsAttribute in mplsAttributes:
            if mplsAttribute in kwargs:
                multiValue = mplsResponse.json()[mplsAttribute]
                self.ixnObj.logInfo('Configuring MPLS attribute: %s' % mplsAttribute)
                self.configMultivalue(multiValue, 'counter', data=kwargs[mplsAttribute])
                
        self.configuredProtocols.append(mplsObj)
        return mplsObj

    def configVxlanNgpf(self, obj=None, routerId=None, port=None, portName=None, ngpfEndpointName=None, hostIp=None, **kwargs):
        """
        Description
            Create or modify a VXLAN.  If creating a new VXLAN header, provide an IPv4 object handle.
            If creating a new VxLAN object, provide an IPv4 object handle.
            If modifying a OSPF, there are five options. 2-6 will query for the OSPF object handle.

               1> Provide the OSPF object handle using the obj parameter.
               2> Set routerId.
               3> Set port: The physical port.
               4> Set portName: The vport port name.
               5> Set NGPF OSPF name that you configured.
               6> Set hostIp: The src IP.
            
        Parameters
               obj: <str>: IPv4 Obj example: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}
                           VxLAN Obj example: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/vxlan/{id}

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
        if obj != None:
            if 'vxlan' not in obj:
                self.ixnObj.logInfo('Create new VxLAN in NGPF')
                response = self.ixnObj.post(self.ixnObj.httpHeader+obj+'/vxlan')
                vxlanId = response.json()['links'][0]['href']
                self.ixnObj.logInfo('createVxlanNgpf: %s' % vxlanId)

            if 'vxlan' in obj:
                vxlanId = obj

        # To modify
        if ngpfEndpointName:
            vxlanId = self.getNgpfObjectHandleByName(ngpfEndpointName=ngpfEndpointName, ngpfEndpointObject='vxlan')

        # To modify
        if port:
            x = self.getProtocolListByPortNgpf(port=port)
            vxlanId = self.getProtocolObjFromProtocolList(x['deviceGroup'], 'vxlan')[0]

        # To modify
        if portName:
            x = self.getProtocolListByPortNgpf(portName=portName)
            vxlanId = self.getProtocolObjFromProtocolList(x['deviceGroup'], 'vxlan')[0]

        # To modify
        if routerId:
            vxlanId = self.getNgpfObjectHandleByRouterId(routerId=routerId, ngpfEndpointObject='vxlan')

        # To modify
        if hostIp:
            x = self.getProtocolListByHostIpNgpf(hostIp)
            vxlanId = self.getProtocolObjFromHostIp(x, protocol='vxlan')

        # Get VxLAN metadatas
        vxlanResponse = self.ixnObj.get(self.ixnObj.httpHeader+vxlanId)

        for key,value in kwargs.items():
            if key == 'vtepName':
                self.ixnObj.patch(self.ixnObj.httpHeader+vxlanId, data={'name': value})

            if key == 'vtepVni':
                multivalue = vxlanResponse.json()['vni']
                self.ixnObj.logInfo('Configuring VxLAN attribute: %s: %s' % (key, value))
                data={'start':kwargs['vtepVni']['start'], 'step':kwargs['vtepVni']['step'], 'direction':kwargs['vtepVni']['direction']}
                self.configMultivalue(multivalue, 'counter', data=data)

            if key == 'vtepIpv4Multicast':
                self.ixnObj.logInfo('Configuring VxLAN IPv4 multicast')
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
        self.ixnObj.logInfo('Creating new RSVP TE LSPS')
        response = self.ixnObj.post(self.ixnObj.httpHeader+ipv4Obj+'/rsvpteLsps')
        return response.json()['links'][0]['href']
        
    def deleteRsvpTeLsps(self, rsvpTunnelObj):
        """
        Description
            Delete a RSVP-TE tunnel.
            Note: Deleting the last tunnel will also delete the RSVR-TE Interface.

        Parameter
            rsvrTunnelObj: <str>: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/rsvpteLsps/{id}

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
            self.ixnObj.logInfo('Creating new Network Group')
            response = self.ixnObj.post(self.ixnObj.httpHeader+deviceGroupObj+'/networkGroup')
            networkGroupObj = response.json()['links'][0]['href']

        if 'modify' in kwargs:
            networkGroupObj = kwargs['modify']

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+networkGroupObj, data={'name': kwargs['name']})

        if 'multiplier' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+networkGroupObj, data={'multiplier': kwargs['multiplier']})

        if 'create' in kwargs:
            self.ixnObj.logInfo('Create new Network Group IPv4 Prefix Pools')
            response = self.ixnObj.post(self.ixnObj.httpHeader+networkGroupObj+'/ipv4PrefixPools')
            ipv4PrefixObj = response.json()['links'][0]['href']
        else:
            ipv4PrefixObj = networkGroupObj+'/ipv4PrefixPools/1'

        # prefixPoolId = /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/networkGroup/3/ipv4PrefixPools/1
        response = self.ixnObj.get(self.ixnObj.httpHeader + ipv4PrefixObj)
        self.ixnObj.logInfo('Config Network Group advertising routes')
        multivalue = response.json()['networkAddress']
        data={'start': kwargs['networkAddress']['start'],
              'step': kwargs['networkAddress']['step'],
              'direction': kwargs['networkAddress']['direction']}
        self.ixnObj.configMultivalue(multivalue, 'counter', data)

        if 'prefixLength' in kwargs:
            self.ixnObj.logInfo('Config Network Group prefix pool length')
            response = self.ixnObj.get(self.ixnObj.httpHeader + ipv4PrefixObj)
            multivalue = response.json()['prefixLength']
            data={'value': kwargs['prefixLength']}
            self.ixnObj.configMultivalue(multivalue, 'singleValue', data)

        return ipv4PrefixObj

    def configPrefixPoolsIsisL3RouteProperty(self, prefixPoolsObj, **data):
        """
        Description
            Configure Network Group Prefix Pools ISIS L3 Route properties.
            Supports both IPv4PrefixPools and IPv6PrefiPools.
            For more property and value references, use the IxNetwork API browser.

        Parameters
            prefixPoolsObj: <str>: Example:
                  /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/networkGroup/{id}/ipv4PrefixPools/{id}

            data: Properties: active, advIPv6Prefix, BAR, BFRId, BFRIdStep, BIERBitStingLength, eFlag, labelRangeSize,
                  labelStart, nFlag, pFlag, rFlag, vFlag, redistribution,  routeOrigin, subDomainId
        Syntax
            PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/networkGroup/{id}/ipv4PrefixPools/{id}
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader + prefixPoolsObj + '/isisL3RouteProperty/1')
        for attribute, value in data.items():
            multivalue = response.json()[attribute]
            self.ixnObj.logInfo('Configuring PrefixPools ISIS L3 Route Property multivalue attribute: %s' % attribute)
            self.ixnObj.patch(self.ixnObj.httpHeader+multivalue+"/singleValue", data={'value': data[attribute]})

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
           multivalueObj: <str>: The multivalue object: /api/v1/sessions/{1}/ixnetwork/multivalue/{id}
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
            self.ixnObj.logInfo('getMultivalueValues: {0} Count={1}'.format(multivalueObj, count))
        data = {'arg1': multivalueObj,
                'arg2': 0,
                'arg3': count
                }
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/multivalue/operations/getValues', data=data, silentMode=silentMode)
        self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/operations/multivalue/getValues'+response.json()['id'], silentMode=silentMode)
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
            self.ixnObj.logInfo('ProtocolName: {0}'.format(protocolViewName))
            for session in stats.keys():
                sessionsUp = int(stats[session]['Sessions Up'])
                totalSessions = int(stats[session]['Sessions Total'])
                totalSessionsNotStarted = int(stats[session]['Sessions Not Started'])
                totalExpectedSessionsUp = totalSessions - totalSessionsNotStarted

                self.ixnObj.logInfo('\n\tPortName: {0}\n\t   TotalSessionsUp: {1}\n\t   ExpectedTotalSessionsup: {2}'.format(
                    stats[session]['Port'], sessionsUp, totalExpectedSessionsUp), timestamp=False)

                if counter < timeout and sessionsUp != totalExpectedSessionsUp:
                    self.ixnObj.logInfo('\t   Session is still down', timestamp=False)

                if counter < timeout and sessionsUp == totalExpectedSessionsUp:
                    totalPortsUpFlag += 1
                    if totalPortsUpFlag == totalPorts:
                        self.ixnObj.logInfo('All sessions are up!')
                        return

            if counter == timeout and sessionsUp != totalExpectedSessionsUp:
                raise IxNetRestApiException('\nSessions failed to come up')

            self.ixnObj.logInfo('\n\tWait {0}/{1} seconds'.format(counter, timeout), timestamp=False)
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

        deviceGroupTimeout = 90
        for topology in queryResponse.json()['result'][0]['topology']:
            for deviceGroup in topology['deviceGroup']:
                deviceGroupObj = deviceGroup['href']
                response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroupObj, silentMode=False)
                # Verify if the Device Group is enabled. If not, don't go further.
                enabledMultivalue = response.json()['enabled']
                enabled = self.ixnObj.getMultivalueValues(enabledMultivalue, silentMode=False)
                if enabled[0] == 'true':
                    for counter in range(1,deviceGroupTimeout+1):
                        response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroupObj, silentMode=False)
                        deviceGroupStatus = response.json()['status']
                        self.ixnObj.logInfo('\t%s' % deviceGroupObj, timestamp=False)
                        self.ixnObj.logInfo('\t\tStatus: %s' % deviceGroupStatus, timestamp=False)
                        if counter < deviceGroupTimeout and deviceGroupStatus != 'started':
                            self.ixnObj.logInfo('\t\tWaiting %d/%d seconds ...' % (counter, deviceGroupTimeout), timestamp=False)
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
                            self.ixnObj.logInfo('\tInnerDeviceGroup: %s' % innerDeviceGroupObj, timestamp=False)
                            self.ixnObj.logInfo('\t   Status: %s' % innerDeviceGroupStatus, timestamp=False)
                            if counter < deviceGroupTimeout and innerDeviceGroupStatus != 'started':
                                self.ixnObj.logInfo('\tWait %d/%d' % (counter, deviceGroupTimeout), timestamp=False)
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
            protocolObj: <str|obj>: Ex: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1
        
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
            Start one or more Device Groups and all its protocols.

        Parameters
            deviceGroupObj: <str>|<list>: 'all' or a list of Device Group objects.
                             Ex: ['/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1']

            action: <str>: 'start'|'stop'
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
                    deviceGroupObjList.append(dgHref['href'])

        url = self.ixnObj.sessionUrl+'/topology/deviceGroup/operations/%s' % action
        response = self.ixnObj.post(url, data={'arg1': deviceGroupObjList})
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

                self.ixnObj.logInfo('\nVerifyProtocolSessions: %s\n' % eachProtocol, timestamp=False)
                self.ixnObj.logInfo('\tprotocolSessionStatus: %s' % protocolSessionStatus, timestamp=False)
                self.ixnObj.logInfo('\tsessionStatusResponse: %s' % sessionStatus, timestamp=False)
                if timer < timerStop:
                    if protocolSessionStatus != 'started':
                        self.ixnObj.logInfo('\tWait %s/%s seconds' % (timer, timerStop), timestamp=False)
                        time.sleep(1)
                        continue

                    # Started
                    if 'up' not in sessionStatus:
                        self.ixnObj.logInfo('\tProtocol session is down: Wait %s/%s seconds' % (timer, timerStop), timestamp=False)
                        time.sleep(1)
                        continue

                    if 'up' in sessionStatus:
                        self.ixnObj.logInfo('Protocol sessions are all up: {0}'.format(protocolName))
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
                                self.ixnObj.logInfo('eachSessionStatus index: {0} {1}'.format(eachSessionStatus, index), timestamp=False)
                                if eachSessionStatus == 'down':
                                    ipInterfaceIndexList.append(index)
                                index += 1

                            ipMultivalue = response.json()['address']
                            ipAddressList = self.ixnObj.getMultivalueValues(ipMultivalue, silentMode=True)
                            self.ixnObj.logWarning('ARP failed on IP interface:')
                            for eachIpIndex in ipInterfaceIndexList:
                                self.ixnObj.logInfo('\t{0}'.format(ipAddressList[eachIpIndex]), timestamp=False)
                        else:
                            self.ixnObj.logWarning('\tverifyProtocolSessions: {0} session failed'.format(protocolName))

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
        self.ixnObj.logInfo('\t%s' % protocol, timestamp=False)
        self.ixnObj.logInfo('\tProtocol is enabled: %s\n' % response[0], timestamp=False)
        if response[0] == 'false':
            return

        for timer in range(startCounter, timeout+1):
            currentStatus = self.getSessionStatus(protocol)
            self.ixnObj.logInfo('\n%s' % protocol, timestamp=False)
            self.ixnObj.logInfo('\tTotal sessions: %d' % len(currentStatus), timestamp=False)
            totalDownSessions = 0
            for eachStatus in currentStatus:
                if eachStatus != 'up':
                    totalDownSessions += 1
            self.ixnObj.logInfo('\tTotal sessions Down: %d' % totalDownSessions, timestamp=False)
            self.ixnObj.logInfo('\tCurrentStatus: %s' % currentStatus)

            if timer < timeout and [element for element in sessionDownList if element in currentStatus] == []:
                self.ixnObj.logInfo('Protocol sessions are all up')
                startCounter = timer
                break

            if timer < timeout and [element for element in sessionDownList if element in currentStatus] != []:
                self.ixnObj.logInfo('\tWait %d/%d seconds' % (timer, timeout), timestamp=False)
                time.sleep(1)
                continue

            if timer == timeout and [element for element in sessionDownList if element in currentStatus] != []:
                raise IxNetRestApiException('\nError: Protocols failed')

    def verifyAllProtocolSessionsNgpf(self, timeout=120, silentMode=False):
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
                response = self.ixnObj.getMultivalueValues(enabledMultivalue, silentMode=silentMode)

                self.ixnObj.logInfo('DeviceGroup is enabled: %s'% response)
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
                        response = self.ixnObj.get(self.ixnObj.httpHeader+ethernet+'/'+protocol, silentMode=True, ignoreError=True)
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
                            response = self.ixnObj.get(self.ixnObj.httpHeader+layer3Ip+'/'+protocol, silentMode=True, ignoreError=True)
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
        self.ixnObj.logInfo('vportList: %s' % vportList)
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
            self.ixnObj.logInfo('\n%s' % protocolObj, timestamp=False)
            self.ixnObj.logInfo('\tSessionStatus: %s' % sessionStatus, timestamp=False)
            if counter < timeout and 'notStarted' in sessionStatus:
                self.ixnObj.logInfo('\tWait %d/%d seconds' % (counter, timeout), timestamp=False)
                time.sleep(1)

            if counter == timeout and 'notStarted' in sessionStatus:
                raise IxNetRestApiException('Protocol sessions failed to start')

            if counter < timeout and 'notStarted' not in sessionStatus:
                self.ixnObj.logInfo('Protocol sessions all started')
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
                self.ixnObj.logInfo('\n', timestamp=False)

                for counter in range(1,arpTimeout+1):
                    sessionStatus = self.getSessionStatus(ipProtocol)
                    self.ixnObj.logInfo('\tARP SessionStatus: %s' % sessionStatus, timestamp=False)
                    if counter < arpTimeout and 'down' in sessionStatus:
                        self.ixnObj.logInfo('\tARP is not resolved yet. Wait %d/%d' % (counter, arpTimeout), timestamp=False)
                        time.sleep(1)
                        continue
                    if counter < arpTimeout and 'down' not in sessionStatus:
                        break
                    if counter == arpTimeout and 'down' in sessionStatus:
                        #raise IxNetRestApiException('\nARP is not getting resolved')
                        # Let it flow down to get the unresolved ARPs
                        pass

                protocolResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipProtocol+'?includes=resolvedGatewayMac,address,gatewayIp', ignoreError=True, silentMode=silentMode)

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
            self.ixnObj.logInfo('ARP is resolved')
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
        self.ixnObj.logInfo('Verify ARP: %s' % ipType)
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
                    #self.ixnObj.logInfo('%s' % deviceGroupObj, timestamp=False)
                    if deviceGroupStatus == 'notStarted':
                        raise IxNetRestApiException('\nDevice Group is not started.')

                    if counter < timeout and deviceGroupStatus == 'starting':
                        self.ixnObj.logInfo('\tWait %d/%d' % (counter, timeout), timestamp=False)
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
                        self.ixnObj.logInfo('%s' % self.ixnObj.httpHeader+innerDeviceGroupObj, timestamp=False)
                        response = self.ixnObj.get(self.ixnObj.httpHeader+innerDeviceGroupObj, silentMode=silentMode)
                        deviceGroupStatus1 = response.json()['status']
                        self.ixnObj.logInfo('\tdeviceGroup Status: %s' % deviceGroupStatus1, timestamp=False)

                        if deviceGroupStatus == 'started':
                            arpResult = self.deviceGroupProtocolStackNgpf(innerDeviceGroupObj, ipType, silentMode=silentMode)
                            if arpResult != 0:
                                unresolvedArpList = unresolvedArpList + arpResult

        if unresolvedArpList == [] and startFlag == 0:
            # Device group status is not started.
            raise IxNetRestApiException("\nError: Device Group is not started. It must've went down. Can't verify arp.")

        if unresolvedArpList != [] and startFlag == 1:
            # Device group status is started and there are arp unresolved.
            print()
            raise IxNetRestApiException('\nError: Unresolved ARP: {0}'.format(unresolvedArpList))

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
                    self.ixnObj.logInfo('\t%s' % ipv4Href)
                    self.ixnObj.logInfo('\tIPv4 sessionStatus: %s' % ipv4SessionStatus)
                    self.ixnObj.logInfo('\tGatewayIpMultivalue: %s' % gatewayIpMultivalue)
                    response = self.ixnObj.getMultivalueValues(gatewayIpMultivalue)
                    valueList = response
                    
                    self.ixnObj.logInfo('gateway IP: %s' % valueList)
                    if gatewayIp in valueList:
                        gatewayIpIndex = valueList.index(gatewayIp)
                        self.ixnObj.logInfo('Found gateway: %s ; Index:%s' % (gatewayIp, gatewayIpIndex))

                        queryData = {'from': deviceGroup['ethernet'][0]['href'],
                                    'nodes': [{'node': 'ipv4',  'properties': ['gatewayIp', 'resolvedGatewayMac'], 'where': []}
                                    ]}
                        queryResponse = self.ixnObj.query(data=queryData, silentMode=False)
                        response = self.ixnObj.get(self.ixnObj.httpHeader+ipv4Href+'?includes=resolvedGatewayMac')
                        gatewayMacAddress = response.json()['resolvedGatewayMac']
                        self.ixnObj.logInfo('gatewayIpMacAddress: %s' % gatewayMacAddress)
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
                        self.ixnObj.logInfo('Found srcIpAddress: %s. Getting Gatway IP address ...' % srcIpAddress)
                        response = self.ixnObj.getMultivalueValues(gatewayIpMultivalue)
                        gatewayIp = response[0]
                        self.ixnObj.logInfo('Gateway IP address: %s' % gatewayIp)
                        return gatewayIp
                except:
                    pass
        return 0

    def getDeviceGroupObjAndIpObjBySrcIp(self, srcIpAddress):
        """
        Description
            Search each Topology/Device Group for the srcIpAddress.
            If found, return the Device Group object and the IPv4|Ipv6 object.

            if srcIpAddress is IPv6, the format must match what is shown
            in the GUI or API server.  Please verify how the configured 
            IPv6 format looks like on either the IxNetwork API server when you
            are testing your script during development.

        Parameter
           srcIpAddress: <str>: The source IP address.

        Returns
            None: If no srcIpAddress is found.
            deviceGroup Object and IPv4|IPv6 object
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
                            ipObj = ethernet['ipv4'][0]['href']
                        else:
                            # IPv6 format: ['2000:0:0:1:0:0:0:2', '2000:0:0:2:0:0:0:2', '2000:0:0:3:0:0:0:2', '2000:0:0:4:0:0:0:2']
                            srcIpMultivalue = ethernet['ipv6'][0]['address']
                            ipObj = ethernet['ipv6'][0]['href']

                        response = self.ixnObj.getMultivalueValues(srcIpMultivalue)
                        if srcIpAddress in response:
                            self.ixnObj.logInfo('Found srcIpAddress: %s' % srcIpAddress)
                            return deviceGroup['href'],ipObj
                    except:
                        pass

    def getTopologyObjAndDeviceGroupObjByPortName(self, portName):
        """
        Description
            Search each Topology Group vport for the portName.
            If found, return the topology object and a list of 
            all its device groups.

        Parameter
            portName: <str>: The port name that you configured for the physical port.

        Returns
            None: If no portName found in any Topology Group.

            Topology object + Device Group list
            Ex: ['/api/v1/sessions/1/ixnetwork/topology/2', ['/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1']]
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl + '/topology')
        for eachTopology in response.json():
            topologyObj = eachTopology['links'][0]['href']
            vportList = eachTopology['ports']
            response = self.ixnObj.get(self.ixnObj.httpHeader + topologyObj + '/deviceGroup')

            deviceGroupList = []
            for eachDeviceGroup in response.json()[0]['links']:
                deviceGroupObj = eachDeviceGroup['href']
                deviceGroupList.append(deviceGroupObj)

            for eachVport in vportList:
                response = self.ixnObj.get(self.ixnObj.httpHeader+eachVport)
                vportName = response.json()['name']
                if portName == vportName:
                    return topologyObj, deviceGroupList

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
                self.ixnObj.logInfo('activateRouterIdProtocols: Querying DeviceGroup for routerId %s: %s' % (routerId, protocol))
                self.ixnObj.logInfo('routerIdList: {0}'.format(routerIdList))
                # response: ["192.0.0.1", "192.0.0.2", "192.0.0.3", "192.0.0.4","192.1.0.1"]
                if routerId in routerIdList:
                    foundRouterIdFlag = 1
                    self.ixnObj.logInfo('Found routerId %s' %  routerId)
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
                            self.ixnObj.logInfo('currentValueList: %s' % protocolActiveList)
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

            self.ixnObj.logInfo('Searching Device Group: %s' % deviceGroupObj)
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

                        self.ixnObj.logInfo('Current active list: %s' % protocolActiveList)
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

                                self.ixnObj.logInfo('Modifying: %s' % networkGroupObj)
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

        self.ixnObj.logInfo('configNetworkGroup: %s' % networkGroupObj)
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
            Apply NGPF configuration changes on the fly while Topology protocols are running.
        """
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/globals/topology/operations/applyonthefly',
                                    data={'arg1': '{0}/globals/topology'.format(self.ixnObj.sessionUrl)})
        self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/globals/topology/operations/applyonthefly'+response.json()['id'])

    def getProtocolListByPort(self, port):
        """
        Description
            For IxNetwork Classic Framework only:
            Get all enabled protocolss by the specified port.

        Parameter
            port: (chassisIp, cardNumber, portNumber) -> ('10.10.10.1', '2', '8')
        """
        self.ixnObj.logInfo('\ngetProtocolListByPort...')
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

    def getProtocolListByPortNgpf(self, port=None, portName=None):
        """
        Description
            Based on either the vport name or the physical port, get the Topology
            Group object and all the protocols in each Device Group within the same 
            Topology Group.

        Parameter
            port: [chassisIp, cardNumber, portNumber]
                  Example: ['10.10.10.1', '2', '8']

            portName: <str>: The virtual port name.

        Example usage:
            protocolObj = Protocol(mainObj)
            protocolList = protocolObj.getProtocolListByPortNgpf(port=['192.168.70.120', '1', '2'])

            Subsequently, you could call getObjectHandleFromProtocolList to get any protocol object handle:
            obj = protocolObj.getProtocolObjFromProtocolList(protocolList['deviceGroup'], 'bgpIpv4Peer')
        
        Returns
            {'topology':    '/api/v1/sessions/1/ixnetwork/topology/2',
             'deviceGroup': [['/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/2',
                              '/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/2/ethernet/1',
                              '/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/2/ethernet/1/ipv4/1',
                              '/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/2/ethernet/1/ipv4/1/bgpIpv4Peer'], 

                             ['/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/3',
                              '/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/3/ethernet/1',
                              '/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/3/ethernet/1/ipv4/1',
                              '/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/3/ethernet/1/ipv4/1/ospfv2']
                            ]}
        """
        self.ixnObj.logInfo('{0}...'.format('\ngetProtocolListByPortNgpf'), timestamp=False)
        if port:
            chassisIp = str(port[0])
            cardNum = str(port[1])
            portNum = str(port[2])
            specifiedPort = chassisIp+':'+cardNum+':'+portNum

        loopFlag = 0

        # Loop each Topology and search for matching port or portName
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/topology', silentMode=True)
        topologyList = ['%s/%s/%s' % (self.ixnObj.sessionUrl, 'topology', str(i["id"])) for i in response.json()]
        for topology in topologyList:
            response = self.ixnObj.get(topology, silentMode=True)
            topologyObj = response.json()['links'][0]['href']
            vportList = response.json()['vports']

            for eachVport in vportList:
                response = self.ixnObj.get(self.ixnObj.httpHeader+eachVport, silentMode=True)
                vportName = response.json()['name']

                if portName != None:
                    if portName != vportName:
                        continue
                    else:
                        loopFlag = 1
                        break
                
                if port != None:
                    # actualPort: ['192.168.70.3:1:2']
                    actualPort = self.portMgmtObj.getPhysicalPortFromVport([eachVport])[0]
                    if actualPort != specifiedPort:
                        continue
                    else:
                        loopFlag = 1
                        break

            if loopFlag == 0:
                # The port or portName is not found.
                continue

            enabledProtocolList = {'topology': topologyObj}
            response = self.ixnObj.get(topology+'/deviceGroup', silentMode=True)
            deviceGroupList = ['%s/%s/%s' % (topology, 'deviceGroup', str(i["id"])) for i in response.json()]

            deviceGroupObjects = []
            enabledProtocolList = {'topology': topologyObj, 'deviceGroup': []}
            for deviceGroup in deviceGroupList:
                deviceGroupObj = '/api' + deviceGroup.split('/api')[1]
                deviceGroupObjects.append(deviceGroupObj)

                response = self.ixnObj.get(deviceGroup+'/ethernet', silentMode=True)
                ethernetList = ['%s/%s/%s' % (deviceGroup, 'ethernet', str(i["id"])) for i in response.json()]
                for ethernet in ethernetList:
                    deviceGroupObjects.append('/api'+ethernet.split('/api')[1])
                    response = self.ixnObj.get(ethernet+'/ipv4', silentMode=True)
                    ipv4List = ['%s/%s/%s' % (ethernet, 'ipv4', str(i["id"])) for i in response.json()]
                    if ipv4List:
                        deviceGroupObjects.append('/api'+ipv4List[0].split('/api')[1])
                    response = self.ixnObj.get(ethernet+'/ipv6', silentMode=True)
                    ipv6List = ['%s/%s/%s' % (ethernet, 'ipv6', str(i["id"])) for i in response.json()]
                    if ipv6List:
                        deviceGroupObjects.append('/api'+ipv6List[0].split('/api')[1])
                    for layer3Ip in ipv4List+ipv6List:
                        url = layer3Ip+'?links=true'
                        response = self.ixnObj.get(url, silentMode=True)
                        for protocol in response.json()['links']:
                            currentProtocol = protocol['href']
                            if (bool(re.match('^/api/.*(ipv4|ipv6)/[0-9]+$', currentProtocol))):
                                continue
                            if (bool(re.match('^/api/.*(ipv4|ipv6)/[0-9]+/port$', currentProtocol))):
                                continue
                            url = self.ixnObj.httpHeader+currentProtocol
                            response = self.ixnObj.get(url, silentMode=True)
                            if response.json() == []:
                                # The currentProtocol is not configured.
                                continue
                            else:
                                response = self.ixnObj.get(url, silentMode=True)
                                currentProtocol =response.json()[0]['links'][0]['href']
                                deviceGroupObjects.append(currentProtocol)

                enabledProtocolList['deviceGroup'].insert(len(enabledProtocolList), deviceGroupObjects)
                deviceGroupObjects = []

            # Getting here means either the port or portName is found and the object is obtained.
            # Break and return the object handle.
            break

        if loopFlag == 0:
            if port != None:
                raise IxNetRestApiException('\nError: No port found: {0}'.format(port))
            if portName != None:
                raise IxNetRestApiException('\nError: No portName found: {0}'.format(portName))

        self.ixnObj.logInfo('\ngetProtocolListByPortNgpf: {0}'.format(str(enabledProtocolList)), timestamp=False)        
        return enabledProtocolList

    def getProtocolListByHostIpNgpf(self, hostIp):
        """
        Description
            Based on the host IP address, will return all the Topology/DeviceGroup and all
            it's protocols within the DeviceGroup.

        Parameter
            hostIp: <str>: The host IP address to search in all the topologies.

        Example usage:
            protocolObj = Protocol(mainObj)
            objectList = protocolObj.getProtocolListByHostIpNgpf('1.1.1.1')

            Subsequently, you could call getObjectHandleFromProtocolList to get any protocol object handle:
            obj = protocolObj.getProtocolObjFromProtocolList(protocolList['deviceGroup'], 'bgpIpv4Peer')
        
        Returns
           # This return example shows that the hostIp was found in one topology group and the hostIP
           # was found in two of the device groups within this topology group.

           [{'topology': '/api/v1/sessions/1/ixnetwork/topology/1',
             'deviceGroup': [['/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1',
                              '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1',
                              '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1',
                              '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1'],

                             ['/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/2',
                              '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/2/ethernet/1',
                              '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/2/ethernet/1/ipv4/1',
                              '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/2/ethernet/1/ipv4/1/ospfv2/1']
                            ]
            }]
        """
        self.ixnObj.logInfo('{0}...'.format('\ngetProtocolListByIpHostNgpf'), timestamp=False)
        container = []

        # Loop each Topology and search for matching port or portName
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/topology', silentMode=True)
        topologyList = ['%s/%s/%s' % (self.ixnObj.sessionUrl, 'topology', str(i["id"])) for i in response.json()]
        for topology in topologyList:
            response = self.ixnObj.get(topology, silentMode=True)
            topologyObj = response.json()['links'][0]['href']

            response = self.ixnObj.get(topology+'/deviceGroup', silentMode=True)
            deviceGroupList = ['%s/%s/%s' % (topology, 'deviceGroup', str(i["id"])) for i in response.json()]

            topologyDict = {}
            topology = []
            deviceGroupObjects = []
            isHostIpFound = False

            for deviceGroup in deviceGroupList:
                deviceGroupObj = '/api' + deviceGroup.split('/api')[1]

                response = self.ixnObj.get(deviceGroup+'/ethernet', silentMode=True)
                ethernetList = ['%s/%s/%s' % (deviceGroup, 'ethernet', str(i["id"])) for i in response.json()]
                for ethernet in ethernetList:
                    response = self.ixnObj.get(ethernet+'/ipv4', silentMode=True)
                    ipv4List = ['%s/%s/%s' % (ethernet, 'ipv4', str(i["id"])) for i in response.json()]
                    if ipv4List:
                        for ipv4Obj in ipv4List:
                            response = self.ixnObj.get(ipv4Obj)
                            multivalue = response.json()['address']
                            ipv4HostList = self.getMultivalueValues(multivalue)
                            if hostIp in ipv4HostList:
                                if 'topology' not in topologyDict:
                                    topologyDict = {'topology': topologyObj, 'deviceGroup': []}
                                deviceGroupObjects.append(deviceGroupObj)
                                deviceGroupObjects.append('/api'+ethernet.split('/api')[1])
                                deviceGroupObjects.append('/api'+ipv4List[0].split('/api')[1])
                                isHostIpFound = True

                    response = self.ixnObj.get(ethernet+'/ipv6', silentMode=True)
                    ipv6List = ['%s/%s/%s' % (ethernet, 'ipv6', str(i["id"])) for i in response.json()]
                    if ipv6List:
                        for ipv6Obj in ipv6List:
                            response = self.ixnObj.get(ipv6Obj)
                            multivalue = response.json()['address']
                            ipv6HostList = self.getMultivalueValues(multivalue)
                            if hostIp in ipv6HostList:
                                if 'topology' not in topologyDict:
                                    topologyDict = {'topology': topologyObj, 'deviceGroup': []}
                                deviceGroupObjects.append(deviceGroupObj)
                                deviceGroupObjects.append('/api'+ethernet.split('/api')[1])
                                deviceGroupObjects.append('/api'+ipv6List[0].split('/api')[1])
                                isHostIpFound = True

                    if isHostIpFound == False:
                        continue

                    for layer3Ip in ipv4List+ipv6List:
                        url = layer3Ip+'?links=true'
                        response = self.ixnObj.get(url, silentMode=True)
                        for protocol in response.json()['links']:
                            currentProtocol = protocol['href']                            
                            if (bool(re.match('^/api/.*(ipv4|ipv6)/[0-9]+$', currentProtocol))):
                                continue
                            if (bool(re.match('^/api/.*(ipv4|ipv6)/[0-9]+/port$', currentProtocol))):
                                continue

                            url = self.ixnObj.httpHeader+currentProtocol
                            response = self.ixnObj.get(url, silentMode=True)
                            if response.json() == []:
                                # The currentProtocol is not configured.
                                continue
                            else:
                                deviceGroupObjects.append(response.json()[0]['links'][0]['href'])

                if isHostIpFound:
                    topologyDict['deviceGroup'].insert(len(topologyDict['deviceGroup']), deviceGroupObjects)
                    deviceGroupObjects = []

            if isHostIpFound:
                container.append(topologyDict)

        return container

    def getEndpointObjByDeviceGroupName(self, deviceGroupName, endpointObj):
        """
        Description
            Based on the Device Group name, return the specified endpointObj object handle.
            The endpointObj is the NGPF endpoint: topology, deviceGroup, networkGroup, ethernet, ipv4|ipv6,
            bgpIpv4Peer, ospfv2, igmpHost, etc.  The exact endpoint name could be found in the
            IxNetwork API Browser.

        Parameter
            deviceGroupName: <str>: The Device Group name.
            endpointObj: <str>: The NGPF endpoint object handle to get.
            
        Example usage:
            # This example shows how to get the bgp object handle from the Device Group named DG-2.

            protocolObj = Protocol(mainObj)
            obj = protocolObj.getEndpointObjByDeviceGroupName('DG-2', 'bgpIpv4Peer')
            returns: ['/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer']

            obj = protocolObj.getEndpointObjByDeviceGroupName('DG-2', 'topology')
            returns: ['/api/v1/sessions/1/ixnetwork/topology/2']

        Returns
           []|The NGPF endpoint object handle(s) in a list.
        """
        self.ixnObj.logInfo('{0}...'.format('\ngetProtocolListByIpHostNgpf'), timestamp=False)

        # Loop each Topology and search for matching port or portName
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/topology', silentMode=False)
        topologyList = ['%s/%s/%s' % (self.ixnObj.sessionUrl, 'topology', str(i["id"])) for i in response.json()]
        for topology in topologyList:
            response = self.ixnObj.get(topology, silentMode=False)
            topologyObj = response.json()['links'][0]['href']

            response = self.ixnObj.get(topology+'/deviceGroup', silentMode=False)
            deviceGroupList = ['%s/%s/%s' % (topology, 'deviceGroup', str(i["id"])) for i in response.json()]

            for deviceGroup in deviceGroupList:
                deviceGroupObj = '/api' + deviceGroup.split('/api')[1]
                response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroupObj)
                if response.json()['name'] == deviceGroupName:
                    if endpointObj == 'topology':
                        return topologyObj

                    if endpointObj == 'deviceGroup':
                        return deviceGroupObj

                    response = self.ixnObj.get(deviceGroup+'/ethernet', silentMode=False)
                    ethernetList = ['%s/%s/%s' % (deviceGroup, 'ethernet', str(i["id"])) for i in response.json()]
                    if endpointObj == 'ethernet':
                        headlessEthernetList = []
                        for eachEthernetObj in ethernetList:
                            match = re.match('http.*(/api.*)', eachEthernetObj)
                            if match:
                                headlessEthernetList.append(match.group(1))
                        return headlessEthernetList

                    response = self.ixnObj.get(deviceGroup+'/networkGroup', silentMode=False)
                    networkGroupList = ['%s/%s/%s' % (deviceGroup, 'networkGroup', str(i["id"])) for i in response.json()]
                    if endpointObj == 'networkGroup':
                        headlessNetworkGroupList = []
                        for eachNetworkGroupObj in networkGroupList:
                            match = re.match('http.*(/api.*)', eachNetworkGroupObj)
                            if match:
                                headlessNetworkGroupList.append(match.group(1))
                        return headlessNetworkGroupList

                    for ethernet in ethernetList:
                        response = self.ixnObj.get(ethernet+'/ipv4', silentMode=False)
                        ipv4List = ['%s/%s/%s' % (ethernet, 'ipv4', str(i["id"])) for i in response.json()]
                        if endpointObj == 'ipv4':
                            headlessIpv4List = []
                            for obj in ipv4List:
                                match = re.match('http.*(/api.*)', obj)
                                if match:
                                    headlessIpv4List.append(match.group(1))
                            return headlessIpv4List

                        response = self.ixnObj.get(ethernet+'/ipv6', silentMode=False)
                        ipv6List = ['%s/%s/%s' % (ethernet, 'ipv6', str(i["id"])) for i in response.json()]
                        if endpointObj == 'ipv6':
                            headlessIpv6List = []
                            for obj in ipv6List:
                                match = re.match('http.*(/api.*)', obj)
                                if match:
                                    headlessIpv6List.append(match.group(1))
                            return headlessIpv6List

                        for layer3Ip in ipv4List+ipv6List:
                            url = layer3Ip+'?links=true'
                            response = self.ixnObj.get(url, silentMode=False)
                            for protocol in response.json()['links']:
                                currentProtocol = protocol['href']
                                if (bool(re.match('^/api/.*(ipv4|ipv6)/[0-9]+$', currentProtocol))):
                                    continue
                                if (bool(re.match('^/api/.*(ipv4|ipv6)/[0-9]+/port$', currentProtocol))):
                                    continue

                                url = self.ixnObj.httpHeader+currentProtocol
                                response = self.ixnObj.get(url, silentMode=False)
                                if response.json() == []:
                                    # The currentProtocol is not configured.
                                    continue
                                else:
                                    if (bool(re.search('.*%s' % endpointObj, currentProtocol))):
                                        return currentProtocol

    def getProtocolObjFromProtocolList(self, protocolList, protocol, deviceGroupName=None):
        """
        Description
           This is an internal API used after calling self.getProtocolListByPortNgpf().
           self.getProtocolListByPortNgpf() returns a dict containing a key called deviceGroup
           that contains all the device group protocols in a list.
        
           Use this API to get the protocol object handle by passing in the deviceGroup list and 
           specify the NGPF protocol endpoint name.

        Parameters
           protocolList: <list>: 
           protocol: <str>: The NGPF endpoint protocol name. View below:
           deviceGroupName: <str>: If there are multiple Device Groups within the Topology, filter
                            the Device Group by its name.
        
         NGPF endpoint protocol names:
            'ancp', 'bfdv4Interface', 'bgpIpv4Peer', 'bgpIpv6Peer', 'dhcpv4relayAgent', 'dhcpv6relayAgent',
            'dhcpv4server', 'dhcpv6server', 'geneve', 'greoipv4', 'greoipv6', 'igmpHost', 'igmpQuerier',
            'lac', 'ldpBasicRouter', 'ldpBasicRouterV6', 'ldpConnectedInterface', 'ldpv6ConnectedInterface',
            'ldpTargetedRouter', 'ldpTargetedRouterV6', 'lns', 'mldHost', 'mldQuerier', 'ptp',
            'ipv6sr', 'openFlowController', 'openFlowSwitch', 'ospfv2', 'ospfv3',  'ovsdbcontroller',
            'ovsdbserver', 'pcc', 'pce', 'pcepBackupPCEs', 'pimV4Interface', 'pimV6Interface', 'ptp',
            'rsvpteIf', 'rsvpteLsps', 'tag', 'vxlan'

        Example usage:
            protocolObj = Protocol(mainObj)
            protocolList = protocolObj.getProtocolListByPortNgpf(port=['192.168.70.120', '1', '2'])
            obj = protocolObj.getObjectHandleFromProtocolList(protocolList['deviceGroup'], 'bgpIpv4Peer')

            If you expect multiple Device Groups in your Topology, you could filter by the Device Group name:
            obj = protocolObj.getProtocolObjFromProtocolList(protocolList['deviceGroup'], 'ethernet', deviceGroupName='DG2')

        Returns
            The protocol object handle in a list. For example:
            ['/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/2/ethernet/1/ipv4/1/bgpIpv4Peer']
        """
        self.ixnObj.logInfo('\n{0}...'.format('\ngetProtocolObjFromProtocolList'), timestamp=False)
        objectHandle = []
        for protocols in protocolList:
            if protocol in ['deviceGroup', 'ethernet', 'ipv4', 'ipv6']:
                for endpointObj in protocols:
                    match = re.search(r'(/api/v1/sessions/[0-9]+/ixnetwork/topology/[0-9]+/deviceGroup/[0-9]+).*/%s/[0-9]+$' % protocol, endpointObj)
                    if match:
                        # A topology could have multiple Device Groups. Filter by the Device Group name.
                        if deviceGroupName:
                            deviceGroupObj = match.group(1)
                            response = self.ixnObj.get(self.ixnObj.httpHeader+deviceGroupObj, silentMode=True)
                            if deviceGroupName == response.json()['name']:
                                self.ixnObj.logInfo(str([endpointObj]), timestamp=False)
                                return [endpointObj]
                        else:
                            objectHandle.append(endpointObj)
            else:
                if any(protocol in x for x in protocols):
                    index = [index for index, item in enumerate(protocols) if protocol in item]
                    protocolObjectHandle = protocols[index[0]]
                    self.ixnObj.logInfo(str([protocolObjectHandle]), timestamp=False)
                    return [protocolObjectHandle]

        if objectHandle:
            self.ixnObj.logInfo(str(objectHandle), timestamp=False)
            return objectHandle
        else:
            return None

    def getProtocolObjFromHostIp(self, topologyList, protocol):
        """
        Description
           This is an internal API used after calling self.getProtocolListByHostIpNgpf().
           self.getProtocolListByHostIpNgpf() returns a list of Dicts containing all the topologies
           and its device group(s) that has a hostIp configured.
        
           Use this API to get the protocol object handle by passing in the NGPF endpoint protocol name.

        Parameters
           topologyList: <list>:  A returned list of Dicts from self.getProtocolListByHostIpNgpf(.
           protocol: <str>: The NGPF endpoint protocol name. View below:
        
         protocol (These are the NGPF endpoint objects):
            'ancp', 'bfdv4Interface', 'bgpIpv4Peer', 'bgpIpv6Peer', 'dhcpv4relayAgent', 'dhcpv6relayAgent',
            'dhcpv4server', 'dhcpv6server', 'geneve', 'greoipv4', 'greoipv6', 'igmpHost', 'igmpQuerier',
            'lac', 'ldpBasicRouter', 'ldpBasicRouterV6', 'ldpConnectedInterface', 'ldpv6ConnectedInterface',
            'ldpTargetedRouter', 'ldpTargetedRouterV6', 'lns', 'mldHost', 'mldQuerier', 'ptp',
            'ipv6sr', 'openFlowController', 'openFlowSwitch', 'ospfv2', 'ospfv3',  'ovsdbcontroller',
            'ovsdbserver', 'pcc', 'pce', 'pcepBackupPCEs', 'pimV4Interface', 'pimV6Interface', 'ptp',
            'rsvpteIf', 'rsvpteLsps', 'tag', 'vxlan'

        Example usage:
            protocolObj = Protocol(mainObj)
            x = protocolObj.getProtocolListByHostIpNgpf('1.1.1.1')
            objHandle = protocolObj.getProtocolObjFromHostIp(x, protocol='bgpIpv4Peer')

        Returns
            This API returns a list of object handle(s).

            Example 1:
            The protocol object handle in a list. For example:
               ['/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/2/ethernet/1/ipv4/1/bgpIpv4Peer']

            Example 2:
                If there are multiple device groups and you want to get all the IPv4 endpoints that has the hostIp,
                this API will return you a list:
                   ['/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1',
                    '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/2/ethernet/1/ipv4/1']   
        """
        self.ixnObj.logInfo('{0}...'.format('\ngetProtocolObjFromHostIp'), timestamp=False)
        objectHandle = []

        for element in topologyList:
            if protocol == 'topology':
                return element['topology']
            
            self.ixnObj.logInfo('\nTopologyGroup: {0}'.format(element['topology']), timestamp=False)

            for eachDeviceGroup in element['deviceGroup']:                
                self.ixnObj.logInfo('\n{0}'.format(eachDeviceGroup), timestamp=False)

                for deviceGroupEndpoint in eachDeviceGroup:
                    if protocol in ['deviceGroup', 'networkGroup', 'ethernet', 'ipv4', 'ipv6']:
                        match = re.search(r'(/api/v1/sessions/[0-9]+/ixnetwork/topology/[0-9]+.*%s/[0-9]+)$' % protocol,
                                          deviceGroupEndpoint)
                        if match:
                            objectHandle.append(deviceGroupEndpoint)
                    else:
                        if protocol in deviceGroupEndpoint:
                            objectHandle.append(deviceGroupEndpoint)

        if objectHandle:
            self.ixnObj.logInfo('\nObject handles: {0}'.format(str(objectHandle)), timestamp=False)
            return objectHandle
        else:
            return None

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
            'ancp', 'bfdv4Interface', 'bgpIpv4Peer', 'bgpIpv6Peer', 'dhcpv4relayAgent', 'dhcpv6relayAgent',
            'dhcpv4server', 'dhcpv6server', 'geneve', 'greoipv4', 'greoipv6', 'igmpHost', 'igmpQuerier',
            'lac', 'ldpBasicRouter', 'ldpBasicRouterV6', 'ldpConnectedInterface', 'ldpv6ConnectedInterface',
            'ldpTargetedRouter', 'ldpTargetedRouterV6', 'lns', 'mldHost', 'mldQuerier', 'ptp',
            'ipv6sr', 'openFlowController', 'openFlowSwitch', 'ospfv2', 'ospfv3',  'ovsdbcontroller',
            'ovsdbserver', 'pcc', 'pce', 'pcepBackupPCEs', 'pimV4Interface', 'pimV6Interface', 'ptp',
            'rsvpteIf', 'rsvpteLsps', 'tag', 'vxlan'
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
        self.ixnObj.logInfo('startStopIpv4Ngpf: {0}'.format(action))
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
        self.ixnObj.logInfo('startStopBgpNgpf: {0}'.format(action))
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
        self.ixnObj.logInfo('startStopOspfNgpf: {0}'.format(action))
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
        self.ixnObj.logInfo('startStopIgmpHostNgpf: {0}'.format(action))
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
        self.ixnObj.logInfo('startStopPimV4InterfaceNgpf: {0}'.format(action))
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
        self.ixnObj.logInfo('startStopMldHostNgpf: {0}'.format(action))
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
        self.ixnObj.logInfo('startStopIsisL3Ngpf: {0}'.format(action))
        self.ixnObj.logInfo('\t%s' % isisObjList)
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def startStopLdpBasicRouterNgpf(self, ldpObjList, action='start'):
        """
        Description
            Start or stop LDP Basic Router protocol.

        Parameters
            ldpObjList: Provide a list of one or more ldpBasicRouter object handles to start or stop.
                      Ex: ["/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ldpBasicRouter/3", ...]

        action = start or stop
        """
        if type(ldpObjList) != list:
            raise IxNetRestApiException('startStopLdpBasicRouterNgpf error: The parameter ldpObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl+'/topology/deviceGroup/ldpBasicRouter/operations/'+action
        data = {'arg1': ldpObjList}
        self.ixnObj.logInfo('startStopLdpBasicRouterNgpf: {0}'.format(action))
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
        self.ixnObj.logInfo('Configured groupRangeValues: %s' % groupRangeValues)

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

        self.ixnObj.logInfo('sendIgmpJoinNgpf: List of configured Mcast IP addresses: %s' % listOfConfiguredMcastIpAddresses)
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
        self.ixnObj.logInfo('sendIgmpJoinNgpf: %s' % url)
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

        self.ixnObj.logInfo('sendPimV4JoinNgpf: List of configured Mcast IP addresses: %s' % listOfConfiguredMcastIpAddresses)
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
        self.ixnObj.logInfo('sendPimv4JoinNgpf: %s' % url)
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

        queryResponse = self.ixnObj.query(data=queryData, silentMode=True)
        self.ixnObj.logInfo('', timestamp=False)
        for topology in queryResponse.json()['result'][0]['topology']:
            self.ixnObj.logInfo('TopologyGroup: {0}   Name: {1}'.format(topology['id'], topology['name']), timestamp=False)
            self.ixnObj.logInfo('    Status: {0}'.format(topology['status']), timestamp=False)
            vportObjList = topology['vports']
            for vportObj in vportObjList:
                vportResponse = self.ixnObj.get(self.ixnObj.httpHeader+vportObj, silentMode=True)
                self.ixnObj.logInfo('    VportId: {0} Name: {1}  AssignedTo: {2}  State: {3}'.format(vportResponse.json()['id'],
                                                                                                vportResponse.json()['name'],
                                                                                                vportResponse.json()['assignedTo'],
                                                                                                vportResponse.json()['state']), timestamp=False)
            self.ixnObj.logInfo('\n', end='', timestamp=False)

            for deviceGroup in topology['deviceGroup']:
                self.ixnObj.logInfo('    DeviceGroup:{0}  Name:{1}'.format(deviceGroup['id'], deviceGroup['name']), timestamp=False)
                self.ixnObj.logInfo('\tStatus: {0}'.format(deviceGroup['status']), end='\n\n', timestamp=False)
                for ethernet in deviceGroup['ethernet']:
                    ethernetObj = ethernet['href']
                    ethernetSessionStatus = self.getSessionStatus(ethernetObj)
                    self.ixnObj.logInfo('\tEthernet:{0}  Name:{1}'.format(ethernet['id'], ethernet['name']), timestamp=False)
                    self.ixnObj.logInfo('\t    Status: {0}'.format(ethernet['status']), timestamp=False)
                    enableVlansResponse = self.ixnObj.get(self.ixnObj.httpHeader+ethernet['enableVlans'], silentMode=True)
                    enableVlansMultivalue = enableVlansResponse.json()['links'][0]['href']
                    enableVlansValues = self.getMultivalueValues(enableVlansMultivalue, silentMode=True)[0]
                    self.ixnObj.logInfo('\t    Vlan enabled: %s\n' % enableVlansValues, timestamp=False)

                    if ethernet['ipv6'] == []:
                        ethernet['ipv6'].insert(0, None)

                    for mac,vlan,ipv4,ipv6 in zip(ethernet['mac'], ethernet['vlan'], ethernet['ipv4'], ethernet['ipv6']):
                        ipv4Obj = ipv4['href']
                        ipv4SessionStatus = self.getSessionStatus(ipv4Obj)
                        
                        self.ixnObj.logInfo('\tIPv4:{0} Status: {1}'.format(ipv4['id'], ipv4['status']), timestamp=False)
                        macResponse = self.ixnObj.get(self.ixnObj.httpHeader+ethernet['mac'], silentMode=True)
                        macAddress = self.getMultivalueValues(macResponse.json()['links'][0]['href'], silentMode=True)

                        vlanResponse = self.ixnObj.get(self.ixnObj.httpHeader+vlan['vlanId'], silentMode=True)
                        vlanId = self.getMultivalueValues(vlanResponse.json()['links'][0]['href'], silentMode=True)

                        priorityResponse = self.ixnObj.get(self.ixnObj.httpHeader+vlan['priority'], silentMode=True)
                        vlanPriority = self.getMultivalueValues(priorityResponse.json()['links'][0]['href'],
                                                                       silentMode=True)

                        ipResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv4['address'], silentMode=True)
                        ipAddress = self.getMultivalueValues(ipResponse.json()['links'][0]['href'], silentMode=True)

                        gatewayResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv4['gatewayIp'], silentMode=True)
                        gateway = self.getMultivalueValues(gatewayResponse.json()['links'][0]['href'], silentMode=True)

                        prefixResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv4['prefix'], silentMode=True)
                        prefix = self.getMultivalueValues(prefixResponse.json()['links'][0]['href'], silentMode=True)

                        index = 1
                        self.ixnObj.logInfo('\t    {0:8} {1:14} {2:7} {3:9} {4:12} {5:16} {6:12} {7:7} {8:7}'.format('Index', 'MacAddress', 'VlanId', 'VlanPri', 'EthSession',
                                                                                                        'IPv4Address', 'Gateway', 'Prefix', 'Ipv4Session'), timestamp=False)
                        self.ixnObj.logInfo('\t    {0}'.format('-'*104), timestamp=False)
                        for mac,vlanId,vlanPriority,ethSession,ip,gateway,prefix,ipv4Session in zip(macAddress,
                                                                                                    vlanId,
                                                                                                    vlanPriority,
                                                                                                    ethernetSessionStatus,
                                                                                                    ipAddress,
                                                                                                    gateway,
                                                                                                    prefix,
                                                                                                    ipv4SessionStatus):
                            self.ixnObj.logInfo('\t    {0:^5} {1:18} {2:^6} {3:^9} {4:13} {5:<15} {6:<13} {7:6} {8:7}'.format(index, mac, vlanId, vlanPriority,
                                                                                                    ethSession, ip, gateway, prefix, ipv4Session), timestamp=False)
                            index += 1

                        # IPv6
                        if None not in ethernet['ipv6']:
                            ipResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv6['address'], silentMode=True)
                            gatewayResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv6['gatewayIp'], silentMode=True)
                            prefixResponse = self.ixnObj.get(self.ixnObj.httpHeader+ipv6['prefix'], silentMode=True)
                            self.ixnObj.logInfo('\tIPv6:{0} Status: {1}'.format(ipv6['id'], ipv6['status']), timestamp=False)
                            self.ixnObj.logInfo('\t    {0:8} {1:14} {2:7} {3:9} {4:12} {5:19} {6:18} {7:7} {8:7}'.format('Index', 'MacAddress', 'VlanId', 'VlanPri', 'EthSession',
                                                                                                            'IPv6Address', 'Gateway', 'Prefix', 'Ipv6Session'), timestamp=False)
                            self.ixnObj.logInfo('\t   %s' % '-'*113)
                            for mac,vlanId,vlanPriority,ethSession,ip,gateway,prefix,ipv4Session in zip(macResponse.json()['values'],
                                                                            vlanResponse.json()['values'],
                                                                            priorityResponse.json()['values'],
                                                                            ethernet['sessionStatus'],
                                                                            ipResponse.json()['values'], gatewayResponse.json()['values'],
                                                                            prefixResponse.json()['values'], ipv6['sessionStatus']):
                                self.ixnObj.logInfo('\t    {0:^5} {1:18} {2:^6} {3:^9} {4:13} {5:<15} {6:<13} {7:8} {8:7}'.format(index, mac, vlanId, vlanPriority,
                                                                                                        ethSession, ip, gateway, prefix, ipv4Session), timestamp=False)
                                index += 1

                        self.ixnObj.logInfo('\n', end='', timestamp=False)
                        if ipv4['bgpIpv4Peer'] != []:
                            for bgpIpv4Peer in ipv4['bgpIpv4Peer']:
                                bgpIpv4PeerHref = bgpIpv4Peer['href']
                                bgpIpv4PeerSessionStatus = self.getSessionStatus(bgpIpv4PeerHref)

                                self.ixnObj.logInfo('\tBGPIpv4Peer:{0}  Name:{1}'.format(bgpIpv4Peer['id'], bgpIpv4Peer['name'],
                                                                                         bgpIpv4Peer['status']), timestamp=False)
                                dutIpResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['dutIp'], silentMode=True)
                                dutIp = self.getMultivalueValues(dutIpResponse.json()['links'][0]['href'], silentMode=True)

                                typeResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['type'], silentMode=True)
                                typeMultivalue = typeResponse.json()['links'][0]['href']
                                bgpType = self.getMultivalueValues(typeMultivalue, silentMode=True)

                                localAs2BytesResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['localAs2Bytes'],
                                                                        silentMode=True)
                                localAs2BytesMultivalue = localAs2BytesResponse.json()['links'][0]['href']
                                localAs2Bytes = self.getMultivalueValues(localAs2BytesMultivalue, silentMode=True)

                                flapResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['flap'], silentMode=True)
                                flap = self.getMultivalueValues(flapResponse.json()['links'][0]['href'], silentMode=True)

                                uptimeResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['uptimeInSec'],
                                                                 silentMode=True)
                                uptime = self.getMultivalueValues(uptimeResponse.json()['links'][0]['href'], silentMode=True)
                                downtimeResponse = self.ixnObj.get(self.ixnObj.httpHeader+bgpIpv4Peer['downtimeInSec'],
                                                                   silentMode=True)
                                downtime = self.getMultivalueValues(downtimeResponse.json()['links'][0]['href'],
                                                                           silentMode=True)
                                self.ixnObj.logInfo('\t    Type: {0}  localAs2Bytes: {1}'.format(bgpType[0],
                                                                                                 localAs2Bytes[0]), timestamp=False)
                                self.ixnObj.logInfo('\t    Status: {0}'.format(bgpIpv4Peer['status']), timestamp=False)
                                index = 1

                                for dutIp,bgpSession,flap,uptime,downtime in zip(dutIp,
                                                                                 bgpIpv4PeerSessionStatus,
                                                                                 flap,
                                                                                 uptime,
                                                                                 downtime):
                                    self.ixnObj.logInfo('\t\t{0}: DutIp:{1}  SessionStatus:{2}  Flap:{3}  upTime:{4}  downTime:{5}'.format(index, dutIp, bgpSession, flap, uptime, downtime), timestamp=False)
                                    index += 1

                        for ospfv2 in ipv4['ospfv2']:
                            self.ixnObj.logInfo('\t    OSPFv2:{0}  Name:{1}'.format(ospfv2['id'], ospfv2['name'], ospfv2['status']), timestamp=False)
                            self.ixnObj.logInfo('\t\tStatus: {0}'.format(ospfv2['status']), end='\n\n', timestamp=False)

                        for igmpHost in ipv4['igmpHost']:
                            self.ixnObj.logInfo('\t    igmpHost:{0}  Name:{1}'.format(igmpHost['id'], igmpHost['name'], igmpHost['status']), timestamp=False)
                            self.ixnObj.logInfo('\t\tStatus: {0}'.format(igmpHost['status']), end='\n\n', timestamp=False)
                        for igmpQuerier in ipv4['igmpQuerier']:
                            self.ixnObj.logInfo('\t    igmpQuerier:{0}  Name:{1}'.format(igmpQuerier['id'], igmpQuerier['name'], igmpQuerier['status']), timestamp=False)
                            self.ixnObj.logInfo('\t\tStatus: {0}'.format(igmpQuerier['status']), end='\n\n', timestamp=False)
                        for vxlan in ipv4['vxlan']:
                            self.ixnObj.logInfo('\t    vxlan:{0}  Name:{1}'.format(vxlan['id'], vxlan['name'], vxlan['status']), timestamp=False)
                            self.ixnObj.logInfo('\tStatus: {0}'.format(vxlan['status']), end='\n\n, timestamp=False')

                for networkGroup in deviceGroup['networkGroup']:
                    self.ixnObj.logInfo('\n\tNetworkGroup:{0}  Name:{1}'.format(networkGroup['id'], networkGroup['name']), timestamp=False)
                    self.ixnObj.logInfo('\t    Multiplier: {0}'.format(networkGroup['multiplier']), timestamp=False)
                    response = self.ixnObj.get(self.ixnObj.httpHeader+networkGroup['href']+'/ipv4PrefixPools', silentMode=True)
                    prefixPoolHref = response.json()[0]['links'][0]['href']

                    response = self.ixnObj.get(self.ixnObj.httpHeader+response.json()[0]['networkAddress'], silentMode=True)
                    startingAddressMultivalue = response.json()['links'][0]['href']
                    startingAddress = self.getMultivalueValues(startingAddressMultivalue, silentMode=True)[0]
                    endingAddress = self.getMultivalueValues(startingAddressMultivalue, silentMode=True)[-1]
                                        
                    prefixPoolResponse = self.ixnObj.get(self.ixnObj.httpHeader+prefixPoolHref, silentMode=True)
                    self.ixnObj.logInfo('\t    StartingAddress:{0}  EndingAddress:{1}  Prefix:{2}'.format(startingAddress,
                                                                                                          endingAddress,
                                                                                                          response.json()['formatLength']), timestamp=False)
                    if None not in ethernet['ipv6']:
                        for ipv6 in ethernet['ipv6']:
                            self.ixnObj.logInfo('\t    IPv6:{0}  Name:{1}'.format(ipv6['id'], ipv6['name']), timestamp=False)
                            for bgpIpv6Peer in ipv6['bgpIpv6Peer']:
                                self.ixnObj.logInfo('\t    BGPIpv6Peer:{0}  Name:{1}'.format(bgpIpv6Peer['id'], bgpIpv6Peer['name']), timestamp=False)
                            for ospfv3 in ipv6['ospfv3']:
                                self.ixnObj.logInfo('\t    OSPFv3:{0}  Name:{1}'.format(ospfv3['id'], ospfv3['name']), timestamp=False)
                            for mldHost in ipv6['mldHost']:
                                self.ixnObj.logInfo('\t    mldHost:{0}  Name:{1}'.format(mldHost['id'], mldHost['name']), timestamp=False)
                            for mldQuerier in ipv6['mldQuerier']:
                                self.ixnObj.logInfo('\t    mldQuerier:{0}  Name:{1}'.format(mldQuerier['id'], mldQuerier['name']), timestamp=False)
            self.ixnObj.logInfo('\n', timestamp=False)

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
 
        self.ixnObj.logInfo('Configuruing: %s' % bgpRouteObj)
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

    def getObject(self, keys, ngpfEndpointName=None):
        """
        Description
            This is an internal function usage for getNgpfObjectHandleByName() only.
        """
        object = None
        for key,value in keys.items():
            # All the Topology Groups
            if type(value) is list:
                for keyValue in value:
                    for key,value in keyValue.items():
                        if key == 'name' and value == ngpfEndpointName:
                            return keyValue['href']

                    object = self.getObject(keys=keyValue, ngpfEndpointName=ngpfEndpointName)
                    if object != None:
                        return object
        return None

    def getNgpfObjectHandleByName(self, ngpfEndpointObject=None, ngpfEndpointName=None):
        """
        Description
           Get the NGPF object handle filtering by the NGPF component name.
           The NGPF object name is something that you could configure for each NGPF stack.
           Stack meaning: topology, deviceGroup, ethernet, ipv44, bgpIpv4Peer, etc

        Parameters
           ngpfEndpointObject: See below ngpfL2ObjectList and ngpfL3ObjectList. 
           ngpfEndpointName:   The name of the NGPF component object.

        Examples:
           protocolObj.getNgpfObjectHandleByName(ngpfEndpointObject='topology', ngpfEndpointName='Topo2')
                 return objectHandle: /api/v1/sessions/1/ixnetwork/topology/2

           protocolObj.getNgpfObjectHandleByName(ngpfEndpointObject='ipv4', ngpfEndpointName='IPv4 1')
                 return objectHandle: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1

           protocolObj.getNgpfObjectHandleByName(ngpfEndpointObject='bgpIpv4Peer', ngpfEndpointName='bgp_2')
                 return objectHandle: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/2

           protocolObj.getNgpfObjectHandleByName(ngpfEndpointObject='networkGroup', ngpfEndpointName='networkGroup1')
                 return objectHandle: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/networkGroup/1

           protocolObj.getNgpfObjectHandleByName(ngpfEndpointObject='ipv4PrefixPools', ngpfEndpointName='Basic IPv4 Addresses 1')
                 return objectHandle: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/networkGroup1/ipv4PrefixPools/1
        """
        ngpfMainObjectList = ['topology', 'deviceGroup', 'ethernet', 'ipv4', 'ipv6',
                              'networkGroup', 'ipv4PrefixPools', 'ipv6PrefixPools']

        ngpfL2ObjectList = ['isisL3', 'lacp', 'mpls']

        ngpfL3ObjectList = ['ancp', 'bfdv4Interface', 'bgpIpv4Peer', 'bgpIpv6Peer', 'dhcpv4relayAgent', 'dhcpv6relayAgent',
                            'geneve', 'greoipv4', 'greoipv6', 'igmpHost', 'igmpQuerier',
                            'lac', 'ldpBasicRouter', 'ldpBasicRouterV6', 'ldpConnectedInterface', 'ldpv6ConnectedInterface',
                            'ldpTargetedRouter', 'ldpTargetedRouterV6', 'lns', 'mldHost', 'mldQuerier', 'ptp', 'ipv6sr',
                            'openFlowController', 'openFlowSwitch', 'ospfv2', 'ospfv3', 'ovsdbcontroller', 'ovsdbserver',
                            'pcc', 'pce', 'pcepBackupPCEs', 'pimV4Interface', 'pimV6Interface', 'ptp', 'rsvpteIf',
                            'rsvpteLsps', 'tag', 'vxlan'
                        ]
        
        if ngpfEndpointObject not in ngpfL2ObjectList+ngpfL3ObjectList+ngpfMainObjectList:
            raise IxNetRestApiException('\nError: No such ngpfEndpointObject: %s' % ngpfEndpointObject)

        if ngpfEndpointObject in ngpfL2ObjectList + ngpfL3ObjectList:
            if ngpfEndpointObject in ngpfL2ObjectList:
                nodesList = [{'node': 'topology', 'properties': [], 'where': []},
                             {'node': 'deviceGroup', 'properties': [], 'where': []},
                             {'node': 'ethernet', 'properties': [], 'where': []}
                ]

            if ngpfEndpointObject in ngpfL3ObjectList:
                nodesList = [{'node': 'topology', 'properties': [], 'where': []},
                             {'node': 'deviceGroup', 'properties': [], 'where': []},
                             {'node': 'ethernet', 'properties': [], 'where': []},
                             {'node': 'ipv4', 'properties': [], 'where': []},
                             {'node': 'ipv6', 'properties': [], 'where': []}
                ]

            nodesList.insert(len(nodesList), {'node': ngpfEndpointObject, 'properties': ['name'],
                                              'where': [{'property': 'name', 'regex': ngpfEndpointName}]})

        # Get the NGPF top level objects that are not a protocol:
        #    topology, deviceGroup, ethernet, ipv4, ipv6, networkGroup ...
        if ngpfEndpointObject not in ngpfL2ObjectList + ngpfL3ObjectList:
            nodesList = []
            # Get the index position of the ngptEndpointObject in the ngpfMainObjectList
            ngpfEndpointIndex = ngpfMainObjectList.index(ngpfEndpointObject)
            # Example:
            #    If ngpfEndpointObject is 'ethernet',
            #    then do a for loop from the topology level to the ethernet level.
            for eachNgpfEndpoint in ngpfMainObjectList[:ngpfEndpointIndex+1]:
                # topology, deviceGroup, ethernet, ipv4, ipv6, networkGroup ...
                if eachNgpfEndpoint == ngpfEndpointObject:
                    nodesList.append({'node': eachNgpfEndpoint, 'properties': ['name'],
                                      'where': [{'property': 'name', 'regex': ngpfEndpointName}]})
                else:
                    nodesList.append({'node': eachNgpfEndpoint, 'properties': [], 'where': []})

        queryData = {'from': '/', 'nodes': nodesList}
        queryResponse = self.ixnObj.query(data=queryData)

        # Get a list of all the nested keys
        objectHandle = self.getObject(keys=queryResponse.json()['result'][0], ngpfEndpointName=ngpfEndpointName)
        self.ixnObj.logInfo('getNgpfObjectHandleByName: %s' % objectHandle)
        return objectHandle

    def getNgpfObjectHandleByRouterId(self, ngpfEndpointObject, routerId):
        """
        Description
           Get the NGPF object handle filtering by the routerId.
           All host interface has a router ID by default and the router ID is located in the 
           Device Group in the IxNetwork GUI.  The API endpoint is: /topology/deviceGroup/routerData
        
           Note: Router ID exists only if there are protocols configured.

        Parameters
           ngpfEndpointObject: <str>: The NGPF endpoint. Example:
                               deviceGroup, ethernet, ipv4, ipv6, bgpIpv4Peer, ospfv2, etc.
                               These endpoint object names are the IxNetwork API endpoints and you could
                               view them in the IxNetwork API browser.

           routerId: <str>: The router ID IP address.

        Example:
              protocolObj.getNgpfObject(ngpfEndpointObject='ipv4', routerId='192.0.0.1')
                 return objectHandle: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1

              protocolObj.getNgpfObject(ngpfEndpointObject='bgpIpv4Peer', routerId='193.0.0.1')
                 return objectHandle: /api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/2

              protocolObj.getNgpfObject(ngpfEndpointObject='networkGroup', routerId='193.0.0.1')
                 return objectHandle: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/networkGroup/1

              protocolObj.getNgpfObject(ngpfEndpointObject='ipv4PrefixPools', routerId='193.0.0.1')
                 return objectHandle: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/networkGroup1/ipv4PrefixPools/1
        """
        ngpfMainObjectList = ['topology', 'deviceGroup', 'ethernet', 'ipv4', 'ipv6',
                              'networkGroup', 'ipv4PrefixPools', 'ipv6PrefixPools']

        ngpfL2ObjectList = ['isisL3', 'lacp', 'mpls']

        ngpfL3ObjectList = ['ancp', 'bfdv4Interface', 'bgpIpv4Peer', 'bgpIpv6Peer', 'dhcpv4relayAgent', 'dhcpv6relayAgent',
                            'geneve', 'greoipv4', 'greoipv6', 'igmpHost', 'igmpQuerier',
                            'lac', 'ldpBasicRouter', 'ldpBasicRouterV6', 'ldpConnectedInterface', 'ldpv6ConnectedInterface',
                            'ldpTargetedRouter', 'ldpTargetedRouterV6', 'lns', 'mldHost', 'mldQuerier', 'ptp', 'ipv6sr',
                            'openFlowController', 'openFlowSwitch', 'ospfv2', 'ospfv3', 'ovsdbcontroller', 'ovsdbserver',
                            'pcc', 'pce', 'pcepBackupPCEs', 'pimV4Interface', 'pimV6Interface', 'ptp', 'rsvpteIf',
                            'rsvpteLsps', 'tag', 'vxlan'
                        ]
        
        if ngpfEndpointObject not in ngpfL2ObjectList + ngpfL3ObjectList + ngpfMainObjectList:
            raise IxNetRestApiException('\nError: No such ngpfEndpointObject: %s' % ngpfEndpointObject)

        if ngpfEndpointObject in ngpfL2ObjectList + ngpfL3ObjectList:
            if ngpfEndpointObject in ngpfL2ObjectList:
                nodesList = [{'node': 'topology', 'properties': [], 'where': []},
                             {'node': 'deviceGroup', 'properties': [], 'where': []},
                             {'node': 'routerData', 'properties': ['routerId'], 'where': []},
                             {'node': 'ethernet', 'properties': [], 'where': []}
                ]

            if ngpfEndpointObject in ngpfL3ObjectList:
                nodesList = [{'node': 'topology', 'properties': [], 'where': []},
                             {'node': 'deviceGroup', 'properties': [], 'where': []},
                             {'node': 'routerData', 'properties': ['routerId'], 'where': []},
                             {'node': 'ethernet', 'properties': [], 'where': []},
                             {'node': 'ipv4', 'properties': [], 'where': []},
                             {'node': 'ipv6', 'properties': [], 'where': []}
                ]

            # Add the protocol level to the end of the list.
            nodesList.insert(len(nodesList), {'node': ngpfEndpointObject, 'properties': [], 'where': []})

        # User is looking for non protocol object handle such as deviceGroup, ethernet, ipv4 or ipv6
        if ngpfEndpointObject not in ngpfL2ObjectList + ngpfL3ObjectList:
                nodesList = [{'node': 'topology', 'properties': [], 'where': []},
                             {'node': 'deviceGroup', 'properties': [], 'where': []},
                             {'node': 'networkGroup', 'properties': [], 'where': []},
                             {'node': 'ethernet', 'properties': [], 'where': []},
                             {'node': 'ipv4PrefixPools', 'properties': [], 'where': []},
                             {'node': 'ipv6Prefixpools', 'properties': [], 'where': []},
                             {'node': 'routerData', 'properties': ['routerId'], 'where': []},
                             {'node': 'ethernet', 'properties': [], 'where': []},
                             {'node': 'ipv4', 'properties': [], 'where': []},
                             {'node': 'ipv6', 'properties': [], 'where': []}
                ]

        queryData = {'from': '/', 'nodes': nodesList}
        queryResponse = self.ixnObj.query(data=queryData)

        # This is for getObject out of scope variable tracking
        class getObjectVar:
            protocolObjHandle= None
            foundRouterId = False

        def __getObject(keys):
            """
            This is an internal function usage for getNgpfObjectHandleByRouterId() only.
            """
            object = None
            for key,value in keys.items():
                # All the Topology Groups
                if type(value) is list:
                    for keyValue in value:
                        for key,value in keyValue.items():
                            if key == ngpfEndpointObject and value != []:
                                getObjectVar.protocolObjHandle = value[0]['href']

                            if key == 'routerId':
                                routerIdMultivalue = value
                                routerIdList = self.getMultivalueValues(routerIdMultivalue)
                                if routerId in routerIdList:
                                    getObjectVar.foundRouterId = True
                                    return

                        object = __getObject(keyValue)
                        if getObjectVar.foundRouterId == True:
                            return getObjectVar.protocolObjHandle
 
        objectHandle = __getObject(queryResponse.json()['result'][0])
        self.ixnObj.logInfo('getNgpfObject: %s' % objectHandle)
        return objectHandle

    def getDeviceGroupByRouterId(self, routerId=None, queryDict=None, runQuery=True):
        """
        Description
            Get the Device Group object handle for the routerId.
            
            Note:
               A Device Group could have many IP host (sessions). This is configured as multipliers in
               a Device Group.  If multiplier = 5, there will be 5 IP host. Each host will
               have a unique router ID identifier.
               To get the Device Group that has a specific router ID, pass in the router ID for the
               parameter routerId.

        Parameter
            routerId: <str>: The router ID in the format of 192.0.0.1.
            queryDict: <dict>: Ignore this parameter. This parameter is only used internally. 
            runQuery: Ignore this parameter.  <bool>: This parameter is only used internally.  

        Example:
            obj = mainObj.getDeviceGroupByRouterId(routerId='192.0.0.3')

           How to getMac:
               Step 1> Get the Device Group that has routerId
                       deviceGroupObjHandle = self.getDeviceGroupByRouterId(routerId=routerId)
               Step 2> Append the /ethernet/1 endpoint object to the Device Group object.
                       ethernetObjHandle = deviceGroupObjHandle + '/ethernet/1'
               Step 3> Get the mac address using the ethernetObjHandle
                       return self.getObjAttributeValue(ethernetObjHandle, 'mac')

        Return
            - deviceGroup object handle: /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1
            - Exception error if routerId is not found in any Device Group
        """
        if runQuery:
            queryData = {'from': '/',
                        'nodes': [{'node': 'topology',    'properties': ['name'], 'where': []},
                                  {'node': 'deviceGroup', 'properties': [], 'where': []},
                                  {'node': 'routerData', 'properties': ['routerId'], 'where': []}
                              ]
                        }
            queryResponse = self.ixnObj.query(data=queryData)
            queryDict = queryResponse.json()['result'][0]
        
        object = None
        for key,value in queryDict.items():
            # All the Topology Groups
            if type(value) is list:
                for keyValue in value:
                    print()
                    for deepKey,deepValue in keyValue.items():
                        if deepKey == 'routerId':
                            # deepValue = /api/v1/sessions/1/ixnetwork/multivalue/1054
                            # ['192.0.0.1', '192.0.0.2', '192.0.0.3']
                            multivalueObj = deepValue
                            value = self.ixnObj.getMultivalueValues(multivalueObj)
                            if routerId in value:
                                # /api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/routerData/1
                                match = re.match('(/api.*)/routerData', keyValue['href'])
                                deviceGroupObj = match.group(1)
                                self.ixnObj.logInfo('deviceGroupHandle for routerId: {0}\n\t{1}'.format(routerId, deviceGroupObj), timestamp=False)
                                return deviceGroupObj

                    object = self.getDeviceGroupByRouterId(queryDict=keyValue, routerId=routerId, runQuery=False)
                    if object != None:
                        return object

        raise IxNetRestApiException('\nError: No routerId found in any Device Group: {0}'.format(routerId))

    def getEthernetPropertyValue(self, routerId=None, ngpfEndpointName=None, property=None):
        """
        Description
            Get any NGPF Ethernet property value based on the router ID or by the NGPF 
            component name.

        Parameters
            routerId: <str>: The router ID IP address.
            ngpfEndpointName: <str>: The NGPF endpoint name.
            property: <str>: The NGPF Ethernet property.
                      Choices: name, mac, mtu, status, vlanCount, enableVlans 
        """
        ethernetProperties = ['name', 'mac', 'mtu', 'status', 'vlanCount', 'enableVlans']
        if property not in ethernetProperties:
            raise IxNetRestApiException('\nError: No such Ethernet property: %s.\n\nAvailable NGPF Ethernet properies: %s' % (property, ethernetProperties))

        if routerId:
            ethernetObj = self.getNgpfObjectHandleByRouterId(routerId=routerId, ngpfEndpointObject='ethernet')
        
        if ngpfEndpointName:
            ethernetObj = self.getNgpfObjectHandleByName(ngpfEndpointName=ngpfEndpointName, ngpfEndpointObject='ethernet')

        return self.ixnObj.getObjAttributeValue(ethernetObj, property)

    def sendNsNgpf(self, ipv6ObjList):
        # """
        # Description
        #     Send NS out of all the IPv6 objects that you provide in a list.
        #
        # Parameter
        #    ipv6ObjList: <str>:  Provide a list of one or more IPv6 object handles to send arp.
        #                 Ex: ["/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/1"]
        # """
        if type(ipv6ObjList) != list:
            raise IxNetRestApiException('sendNsNgpf error: The parameter ipv6ObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl + '/topology/deviceGroup/ethernet/ipv6/operations/sendns'
        data = {'arg1': ipv6ObjList}
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url + '/' + response.json()['id'])

    def configIpv6Ngpf(self, obj=None, port=None, portName=None, ngpfEndpointName=None, **kwargs):
        """
        Description
            Create or modify NGPF IPv6.
            To create a new IPv6 stack in NGPF, pass in the Ethernet object.
            If modifying, there are four options. 2-4 will query for the IP object handle.

               1> Provide the BGP object handle using the obj parameter.
               2> Set port: The physical port.
               3> Set portName: The vport port name.
               4> Set NGPF IP name that you configured.

        Parameters
            obj: <str>: None or Ethernet obj: '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1'
                                IPv6 obj: '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/1'

            port: <list>: Format: [ixChassisIp, str(cardNumber), str(portNumber)]
            portName: <str>: The virtual port name.
            ngpfEndpointName: <str>: The name that you configured for the NGPF BGP.

            kwargs:
               ipv6Address: <dict>: {'start': '2000:0:0:1:0:0:0:1', 'direction': 'increment', 'step': '0:0:0:0:0:0:0:1'},
               ipv6AddressPortStep: <str>|<dict>:  disable|0:0:0:0:0:0:0:1
                                    Incrementing the IP address on each port based on your input.
                                    0:0:0:0:0:0:0:1 means to increment the last octet on each port.

               gateway: <dict>: {'start': '2000:0:0:1:0:0:0:2', 'direction': 'increment', 'step': '0:0:0:0:0:0:0:1'},
               gatewayPortStep:  <str>|<dict>:  disable|0:0:0:0:0:0:0:1
                                 Incrementing the IP address on each port based on your input.
                                 0:0:0:0:0:0:0:1 means to increment the last octet on each port.

               prefix: <int>:  Example: 64
               resolveGateway: <bool>
        Syntax
            POST:  /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv6
            PATCH: /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv6/{id}

        Example to create a new IPv6 object:
             ipv6Obj = configIpv4Ngpf(ethernetObj1,
                                      ipv6Address={'start': '2000:0:0:1:0:0:0:1',
                                                   'direction': 'increment',
                                                   'step': '0:0:0:0:0:0:0:1'},
                                      ipv6AddressPortStep='disabled',
                                      gateway={'start': '2000:0:0:1:0:0:0:2',
                                               'direction': 'increment',
                                               'step': '0:0:0:0:0:0:0:0'},
                                      gatewayPortStep='disabled',
                                      prefix=64,
                                      resolveGateway=True)

        Return
            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv6/{id}
        """
        createNewIpv6Obj = True

        if obj != None:
            if 'ipv6' in obj:
                # To modify IPv6
                ipv6Obj = obj
                createNewIpv6Obj = False
            else:
                # To create a new IPv6 object
                ipv6Url = self.ixnObj.httpHeader+obj+'/ipv6'
                self.ixnObj.logInfo('Creating new IPv6 in NGPF')
                response = self.ixnObj.post(ipv6Url)
                ipv6Obj = response.json()['links'][0]['href']
                
        # To modify
        if ngpfEndpointName:
            ipv6Obj = self.getNgpfObjectHandleByName(ngpfEndpointName=ngpfEndpointName, ngpfEndpointObject='ipv6')
            createNewIpv6Obj = False

        # To modify
        if port:
            x = self.getProtocolListByPortNgpf(port=port)
            ipv6Obj = self.getProtocolObjFromProtocolList(x['deviceGroup'], 'ipv6')[0]
            createNewIpv6Obj = False

        # To modify
        if portName:
            x = self.getProtocolListByPortNgpf(portName=portName)
            ipv6Obj = self.getProtocolObjFromProtocolList(x['deviceGroup'], 'ipv6')[0]
            createNewIpv6Obj = False

        ipv6Response = self.ixnObj.get(self.ixnObj.httpHeader+ipv6Obj)

        if 'name' in kwargs:
            self.ixnObj.patch(self.ixnObj.httpHeader+ipv6Obj, data={'name': kwargs['name']})

        if 'multiplier' in kwargs:
            self.configDeviceGroupMultiplier(objectHandle=ipv6Obj, multiplier=kwargs['multiplier'], applyOnTheFly=False)

        # Config IPv6 address
        if 'ipv6Address' in kwargs:
            multivalue = ipv6Response.json()['address']
            self.ixnObj.logInfo('Configuring IPv6 address. Attribute for multivalueId = jsonResponse["address"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['ipv6Address'])

            # Config IPv6 port step
            # disabled|0.0.0.1
            if 'ipv6AddressPortStep' in kwargs:
                portStepMultivalue = self.ixnObj.httpHeader+multivalue+'/nest/1'
                self.ixnObj.logInfo('Configure IPv6 address port step')
                if kwargs['ipv6AddressPortStep'] != 'disabled':
                    self.ixnObj.patch(portStepMultivalue, data={'step': kwargs['ipv6AddressPortStep']})

                if kwargs['ipv6AddressPortStep'] == 'disabled':
                    self.ixnObj.patch(portStepMultivalue, data={'enabled': False})

        # Config Gateway
        if 'gateway' in kwargs:
            multivalue = ipv6Response.json()['gatewayIp']
            self.ixnObj.logInfo('Configure IPv6 gateway. Attribute for multivalueId = jsonResponse["gatewayIp"]')
            self.configMultivalue(multivalue, 'counter', data=kwargs['gateway'])

        # Config Gateway port step
        if 'gatewayPortStep' in kwargs:
            portStepMultivalue = self.ixnObj.httpHeader+multivalue+'/nest/1'
            self.ixnObj.logInfo('Configure IPv6 gateway port step')
            if kwargs['gatewayPortStep'] != 'disabled':
                self.ixnObj.patch(portStepMultivalue, data={'step': kwargs['gatewayPortStep']})

            if kwargs['gatewayPortStep'] == 'disabled':
                self.ixnObj.patch(portStepMultivalue, data={'enabled': False})

        # Config resolve gateway
        if 'resolveGateway' in kwargs:
            multivalue = ipv6Response.json()['resolveGateway']
            self.ixnObj.logInfo('Configure IPv6 gateway to resolve gateway. Attribute for multivalueId = jsonResponse["resolveGateway"]')
            self.configMultivalue(multivalue, 'singleValue', data={'value': kwargs['resolveGateway']})

        if 'prefix' in kwargs:
            multivalue = ipv6Response.json()['prefix']
            self.ixnObj.logInfo('Configure IPv6 prefix. Attribute for multivalueId = jsonResponse["prefix"]')
            self.configMultivalue(multivalue, 'singleValue', data={'value': kwargs['prefix']})

        if createNewIpv6Obj == True:
            self.configuredProtocols.append(ipv6Obj)

        return ipv6Obj

    def configDeviceGroupMultiplier(self, objectHandle, multiplier, applyOnTheFly=False):
        """
        Description
           Configure a Device Group multiplier.  Pass in a NGPF object handle and
           this API will parse out the Device Group object to use for configuring 
           the multiplier.
        
        Parameter
           objectHandle: <str>: A NGPF object handle.
           multiplier: <int>: The number of multiplier.
           applyOnTheFly: <bool>: Default to False. applyOnTheFly is for protocols already running.
        """
        deviceGroupObject = re.search("(.*deviceGroup/\d).*", objectHandle)
        deviceGroupObjectUrl = self.ixnObj.httpHeader+deviceGroupObject.group(1)
        self.ixnObj.patch(deviceGroupObjectUrl, data={"multiplier": int(multiplier)})
        if applyOnTheFly: self.applyOnTheFly()

    def startStopLdpBasicRouterV6Ngpf(self, ldpV6ObjList, action='start'):
        """
        Description
            Start or stop LDP Basic Router V6 protocol.

        Parameters
            ldpV6ObjList: <list>: Provide a list of one or more ldpBasicRouterV6 object handles to start or stop.
                      Ex: ["/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ldpBasicRouterV6/1", ...]
            action: <str>: start or stop
        """
        if type(ldpV6ObjList) != list:
            raise IxNetRestApiException('startStopLdpBasicRouterV6Ngpf error: The parameter ldpV6ObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl+'/topology/deviceGroup/ldpBasicRouterV6/operations/'+action
        data = {'arg1': ldpV6ObjList }
        self.ixnObj.logInfo('startStopLdpBasicRouterV6Ngpf: {0}'.format(action))
        self.ixnObj.logInfo('\t%s' % ldpV6ObjList)
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

    def startStopLdpConnectedInterfaceNgpf(self, ldpConnectedIntObjList, action='start'):
        """
        Description
            Start or stop LDP Basic Router Connected Interface protocol.

        Parameters
            ldpConnectedIntObjList: <list>: Provide a list of one or more ldpBasicRouter
                                    object handles to start or stop.
                Ex: ["/api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv4/{id}/ldpConnectedInterface/{id}", ...]
            action: <str>: start or stop
        """
        if type(ldpConnectedIntObjList) != list:
            raise IxNetRestApiException('startStopLdpConnectedInterfaceNgpf error: The parameter ldpObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl + '/topology/deviceGroup/ethernet/ipv4/ldpConnectedInterface/operations/'+action
        data = {'arg1': ldpConnectedIntObjList}
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url + '/' + response.json()['id'])

    def startStopLdpV6ConnectedInterfaceNgpf(self, ldpV6ConnectedIntObjList, action='start'):
        """
        Description
            Start or stop LDP Basic Router V6 Connected Interface protocol.

        Parameters
            ldpV6ConnectedIntObjList: <list>:  Provide a list of one or more ldpBasicRouter object handles to start or stop.
                      Ex: ["/api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}/ipv6/{id}/ldpConnectedInterface/{id}", ...]
            action = start or stop
        """
        if type(ldpV6ConnectedIntObjList) != list:
            raise IxNetRestApiException('startStopLdpV6ConnectedInterfaceNgpf error: The parameter ldpV6ConnectedIntObjList must be a list of objects.')

        url = self.ixnObj.sessionUrl + '/topology/deviceGroup/ethernet/ipv6/ldpv6ConnectedInterface/operations/'+action
        data = {'arg1': ldpV6ConnectedIntObjList}
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url + '/' + response.json()['id'])
