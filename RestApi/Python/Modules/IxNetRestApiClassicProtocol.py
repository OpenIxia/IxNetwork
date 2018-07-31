# PLEASE READ DISCLAIMER
#
#    This class demonstrates sample IxNetwork REST API usage for
#    demo and reference purpose only.
#    It is subject to change for updates without warning.
#
# Description
#    A class object for IxNetwork Classic Framework.

from IxNetRestApi import IxNetRestApiException
import requests, json, os, re, sys, time, datetime, ast

class ClassicProtocol(object):
    def __init__(self, ixnObj=None):
        """
        Parameters
           ixnObj: <str>: The main connection object.
        """
        self.ixnObj = ixnObj

        from IxNetRestApiPortMgmt import PortMgmt
        self.portMgmtObj = PortMgmt(self.ixnObj)

        from IxNetRestApiStatistics import Statistics
        self.statObj = Statistics(self.ixnObj)

    def getPortsByProtocol(self, protocolName):
        """
        Description
            Based on the specified protocol, return all ports associated with the protocol.

        Parameters
           protocolName options:
              bfd, bgp, cfm, eigrp, elmi, igmp, isis, lacp, ldp, linkOam, lisp, mld,
              mplsOam, mplsTp, openFlow, ospf, ospfV3, pimsm, ping, rip, ripng, rsvp,
              static, stp

        Returns: [chassisIp, cardNumber, portNumber]
                  Example: [['192.168.70.11', '1', '1'], ['192.168.70.11', '1', '2']]

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
                # 192.168.70.11:1:5
                response = self.ixnObj.get(vport)
                assignedTo = response.json()['assignedTo']
                currentChassisIp  = str(assignedTo.split(':')[0])
                currentCardNumber = str(assignedTo.split(':')[1])
                currentPortNumber = str(assignedTo.split(':')[2])
                currentPort = [currentChassisIp, currentCardNumber, currentPortNumber]
                portList.append(currentPort)

        return portList

    def getProtocolListByPort(self, port):
        """
        Description
            Get all enabled protocols by the specified port.

        Parameters
            port: [chassisIp, cardNumber, portNumber] -> ['192.168.70.11', '2', '8']
        """
        self.ixnObj.logInfo('\ngetProtocolListByPort...')
        chassis = str(port[0])
        card = str(port[1])
        port = str(port[2])
        specifiedPort = [chassis, card, port]
        enabledProtocolList = []
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/vport')
        vportList = ['%s/%s/%s' % (self.ixnObj.sessionUrl, 'vport', str(i["id"])) for i in response.json()]
        for vport in vportList:
            response = self.ixnObj.get(vport, 'assignedTo')
            # 192.168.70.11:1:5
            assignedTo = response.json()['assignedTo']
            currentChassisIp  = str(assignedTo.split(':')[0])
            currentCardNumber = str(assignedTo.split(':')[1])
            currentPortNumber = str(assignedTo.split(':')[2])
            currentPort = [currentChassisIp, currentCardNumber, currentPortNumber]
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

    def sendArpOnPort(self, portName):
        """
        Description
            Send Arp request on a specified port

        Parameters
            portName: <str>: Name of the port. eg: '1/1/11'

        Syntax
            POST: http://10.154.162.94:11009/api/v1/sessions/1/ixnetwork/vport/operations/sendarp
            DATA: {"arg1": "/api/v1/sessions/1/ixnetwork/vport/1"}

        Examples
            sendArpOnPort(portName='1/1/11')
        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport == None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))

        url = self.ixnObj.sessionUrl + '/vport/operations/sendarp'
        response = self.ixnObj.post(url, data={'arg1': vport})
        self.ixnObj.waitForComplete(response, url + '/' + response.json()['id'])

    def getDiscoverdNeighborOnPort(self, portName):
        """
        Description
            Get Arp discovered neighbor on a specified port

        Parameters
            portName: <str>: Name of the port. eg: '1/1/11'

        Syntax
            GET: http://10.154.162.94:11009/api/v1/sessions/1/ixnetwork/vport/1/discoveredNeighbor/1

        Examples
            getDiscoverdNeighborOnPort(portName='1/1/11')

        Return
            Discovered mac address
        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport == None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))

        url = vport + '/discoveredNeighbor'
        response = self.ixnObj.get(url)

        url = self.ixnObj.httpHeader + response.json()[0]['links'][0]['href']
        response = self.ixnObj.get(url)

        self.ixnObj.logInfo('Discovered Neighbor: %s' % response.json()['neighborMac'])
        return response.json()['neighborMac']


    def startStopProtocolOnPort(self, protocol, portName, action='start'):
        """
        Description
            Start and stop a protocol on a specified port

        Parameters
            protocol: <str>: Protocol to start
            portName: <str>: Name of the port, eg: '1/1/11'
            action: <str>: start or stop a protocol, default is start

        Syntax
            POST: /api/v1/sessions/{id}/ixnetwork/vport/protocols/<protocol>
            DATA: {'args': 'api/v1/sessions/1/ixnetwork/vport/1'}

        Examples
            startStopProtocolOnPort(protocol='ospf', portName='1/1/11')
            startStopProtocolOnPort(protocol='ospf', portName='1/1/11', action='stop')

        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport == None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))

        url = self.ixnObj.sessionUrl + '/vport/protocols/' + protocol + '/operations/' + action
        vport = vport + '/protocols/' + protocol
        response = self.ixnObj.post(url, data={'arg1': vport})
        self.ixnObj.waitForComplete(response, url + '/' + response.json()['id'])

    def getConfiguredProtocols(self):
        """
        Description
            Get the list of protocols configured on vports.

        Return
            A list or one or more congfigured protocols eg: "['ospf','bgp']"
            return [] if no protocol is configured
        """
        time.sleep(5)
        configuredProtocolList = []
        protocolList = ['bfd', 'bgp', 'eigrp', 'isis', 'ldp', 'lisp',
                        'mplsOam', 'mplsTp', 'ospf', 'ospfV3', 'pimsm',
                        'rip', 'ripng']
        response = self.ixnObj.get(self.ixnObj.sessionUrl + '/vport')
        if response == False:
            raise IxNetRestApiException('No ports connected to chassis')

        vportList = ['%s' % vport['links'][0]['href'] for vport in response.json()]
        for eachVport in vportList:
            for eachProtocol in protocolList:
                node = '/router'
                if re.search('bgp', eachProtocol, re.I):
                    node = '/neighborRange'
                protocolResponse = self.ixnObj.get(self.ixnObj.httpHeader + eachVport + '/protocols/' + eachProtocol)
                response = self.ixnObj.get(self.ixnObj.httpHeader + eachVport + '/protocols/' + eachProtocol + node)
                if response.json() != []:
                    if response.json()[0]['enabled'] == True and protocolResponse.json()['runningState'] == 'started':
                        configuredProtocolList.append(eachProtocol)
        configuredProtocolList = list(set(configuredProtocolList))
        return configuredProtocolList

    def enableProtocolOnPort(self, protocol, portName, enable=True):
        """
        Description
           Enable protocol on a speficied port

        Parameters
            protocol: <str>: Protocol to start
            portName: <str>: Name of the port eg: '1/1/11'
            enable: <bool> enable or disable specified protocol. default is True

        Syntax
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/router/{id}
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/neighborRange/{id}
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/host/{id}
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/bridge/{id}
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/actor/{id}
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/neighborPair/{id}

        Examples
            enableProtocolOnPort(protocol='ospf', portName='1/1/11')
            enableProtocolOnPort(protocol='ospf', portName='1/1/11', enable=False)
        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport == None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))

        RouterInstanceList = self.getRouterInstanceByPortAndProtocol(protocol=protocol, vport=vport)
        if RouterInstanceList == []:
            raise IxNetRestApiException('No Router instance exists in protocol {0}'.format(protocol))

        for eachRouterInstance in RouterInstanceList:
            url = self.ixnObj.httpHeader + eachRouterInstance
            self.ixnObj.patch(url, data={"enabled": enable})

    def getProtocolSessionsStats(self, portName, protocol):
        """
        Description
            Get a protocol session status for a specified protocol on a port

        Parameters
            portName: <str>: Name of the Port to get the protocol session stats eg: "1/1/11"
            protocol: <str>: Name of the protocol. eg: <ospf/ospfV3/bgp/isis/ripng/bfd/rip/ldp/mplsoam/pim>

        Examples
            getProtocolSessionsStats(portName='1/1/11', protocol='ospf')

        Return
            Protocol stats in dictionary format eg: {'ospf': {'Configured': 2, 'Up': 1}}
        """
        protocolStats = {}
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport == None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))

        node = '/router'
        if re.search('bgp', protocol, re.I):
            node = '/neighborRange'
        protocolResponse = self.ixnObj.get(vport + '/protocols/' + protocol)
        response = self.ixnObj.get(vport + '/protocols/' + protocol + node)

        if response.json() != []:
            if response.json()[0]['enabled'] == True and protocolResponse.json()['runningState'] == 'started':
                if re.search('ospf', protocol, re.I):
                    protocolViewName = 'OSPF Aggregated Statistics'
                elif re.search('ospfV3', protocol, re.I):
                    protocolViewName = 'OSPFv3 Aggregated Statistics'
                elif re.search('bgp', protocol, re.I):
                    protocolViewName = 'BGP Aggregated Statistics'
                elif re.search('isis', protocol, re.I):
                    protocolViewName = 'ISIS Aggregated Statistics'
                elif re.search('ripng', protocol, re.I):
                    protocolViewName = 'RIPng Aggregated Statistics'
                elif re.search('bfd', protocol, re.I):
                    protocolViewName = 'BFD Aggregated Statistics'
                elif re.search('rip', protocol, re.I):
                    protocolViewName = 'RIP Aggregated Statistics'
                elif re.search('ldp', protocol, re.I):
                    protocolViewName = 'LDP Aggregated Statistics'
                elif re.search('mplsoam', protocol, re.I):
                    protocolViewName = 'MPLSOAM Aggregated Statistics'
                elif re.search('pim', protocol, re.I):
                    protocolViewName = 'PIMSM Aggregated Statistics'
                else:
                    raise IxNetRestApiException('No viewName defined')
            else:
                raise IxNetRestApiException('No {0} protocol running or enabled on port {1}'.format(protocol, portName))
        else:
            raise IxNetRestApiException('No {0} protocol configured on port {1}'.format(protocol, portName))

        stats = self.statObj.getStats(viewName=protocolViewName, displayStats=False)

        #totalPorts = len(stats.keys());  # Length stats.keys() represents total ports.
        self.ixnObj.logInfo('ProtocolViewName: {0}'.format(protocolViewName))
        for session in stats.keys():
            if re.search('OSPF', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Full Nbrs.'])
                totalSessions = int(stats[session]['Sess. Configured'])
            elif re.search('BGP', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Sess. Up'])
                totalSessions = int(stats[session]['Sess. Configured'])
            elif re.search('ISIS', protocolViewName, re.I):
                sessionsUp = int(stats[session]['L2 Sess. Up'])
                totalSessions = int(stats[session]['L2 Sess. Configured'])
            elif re.search('RIPng', protocolViewName, re.I) or re.search('BFD', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Routers Running'])
                totalSessions = int(stats[session]['Routers Configured'])
            elif re.search('RIP', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Request Packet Tx'])
                totalSessions = int(stats[session]['Routers Configured'])
            elif re.search('LACP', protocolViewName, re.I):
                sessionsUp = int(stats[session]['LAG Member Ports UP'])
                totalSessions = int(stats[session]['Total LAG Member Ports'])
            elif re.search('LDP', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Targeted Sess. Up'])
                totalSessions = int(stats[session]['Targeted Sess. Configured'])
            elif re.search('MPLS', protocolViewName, re.I):
                sessionsUp = int(stats[session]['BFD Up-Sessions'])
                totalSessions = int(stats[session]['BFD Session Count'])
            elif re.search('PIM', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Rtrs. Running'])
                totalSessions = int(stats[session]['Rtrs. Configured'])
                # totalSessionsNotStarted = int(stats[session]['Sessions Not Started'])
            else:
                raise IxNetRestApiException('No protocol viewName found')

            if stats[session]['Port Name'] == portName:
                self.ixnObj.logInfo('\n\tPortName: {0}\n\t   TotalSessionsUp: {1}\n\t   TotalSessionsConfigured: {2}'.format(
                    stats[session]['Port Name'], sessionsUp, totalSessions), timestamp=False)
                protocolStats[protocol] = {'Configured': totalSessions, 'Up': sessionsUp}
        return protocolStats

    def enableRouteRangeOnProtocol(self, portName, protocol, routeRange, enable=True):
        """
        Description
            Enable a route range for a protocol on a speficied port

        Parameters
            portName: <str>: Name of the port eg: "1/1/11"
            protocol: <str>: protocol to enable route range. eg: <OSPF|OSPFV3|BGP|ISIS|EIGRP|RIP|RIPng>
            routeRange: <str>: route range <IPv4|IPv6> address
            enable: <bool>: enable or disable route range, default is True (enable)

        Syntax
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/router/{id}/routeRange/{id}
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/neighborRange/{id}/routeRange/{id}

        Examples:
            enableRouteRangeOnProtocol(protName='1/1/11', protocol='ospf', routeRange='10.10.10.1')
            enableRouteRangeOnProtocol(protName='1/1/11', protocol='ospfv3', routeRange='10::1', enable=True)
        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport == None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))

        RouterInstanceList = self.getRouterInstanceByPortAndProtocol(protocol=protocol, vport=vport)
        if RouterInstanceList == []:
            raise IxNetRestApiException('No Router instance exists in protocol {0}'.format(protocol))

        args = 'firstRoute'
        if protocol == 'ospf':
            args = 'networkNumber'
        if protocol == 'bgp':
            args = 'networkAddress'

        for eachRouterInstance in RouterInstanceList:
            url = self.ixnObj.httpHeader + eachRouterInstance + '/routeRange'
            response = self.ixnObj.get(url)
            RouteRangeInstanceList = ["%s" % (str(i["links"][0]["href"])) for i in response.json()]
            self.ixnObj.logInfo('Route Range list %s' % RouteRangeInstanceList)

            for eachRouteRange in RouteRangeInstanceList:
                url = self.ixnObj.httpHeader + eachRouteRange
                response = self.ixnObj.get(url)
                RouteRangeNetwork = response.json()[args]
                if RouteRangeNetwork == routeRange:
                    self.ixnObj.patch(url, data={"enabled": enable})
                    return
            raise IxNetRestApiException(
                'Route range: {0} does not exist in protocol: {1} port: {2}'.format(routeRange, protocol, portName))

    def removeRouteRangeOnProtocol(self, portName, protocol, routeRange):
        """
        Description
            Remove a route range for a protocol on a speficied port

        Parameters
            portName: <str>: Name of the port eg: "1/1/11"
            protocol: <str>: protocol to remove route range. eg: <OSPF|OSPFV3|BGP|ISIS|EIGRP|RIP|RIPng>
            routeRange: <str>: route range <IPv4|IPv6> address

        Syntax
            DELETE: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/router/{id}/routeRange/{id}
            DELETE: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/neighborRange/{id}/routeRange/{id}

        Examples:
            removeRouteRangeOnProtocol(protName='1/1/11', protocol='ospf', routeRange='10.10.10.1')
            removeRouteRangeOnProtocol(protName='1/1/11', protocol='ospfv3', routeRange='10::1')
        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport == None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))

        RouterInstanceList = self.getRouterInstanceByPortAndProtocol(protocol=protocol, vport=vport)
        if RouterInstanceList == []:
            raise IxNetRestApiException('No Router instance exists in protocol {0}'.format(protocol))

        self.ixnObj.logInfo('Router list %s' % RouterInstanceList)
        args = 'firstRoute'
        if protocol == 'ospf':
            args = 'networkNumber'
        if protocol == 'bgp':
            args = 'networkAddress'

        for eachRouterInstance in RouterInstanceList:
            url = self.ixnObj.httpHeader + eachRouterInstance + '/routeRange'
            response = self.ixnObj.get(url)
            RouteRangeInstanceList = ["%s" % (str(i["links"][0]["href"])) for i in response.json()]
            self.ixnObj.logInfo('Route Range list %s' % RouteRangeInstanceList)
            for eachRouteRange in RouteRangeInstanceList:
                url = self.ixnObj.httpHeader + eachRouteRange
                response = self.ixnObj.get(url)
                RouteRangeNetwork = response.json()[args]
                if RouteRangeNetwork == routeRange:
                    self.ixnObj.delete(url)
                    return

            raise IxNetRestApiException(
                'Route range: {0} does not exist in protocol: {1} port: {2}'.format(routeRange, protocol, portName))

    def createRouteRangeOnProtocol(self, portName, protocol, routeRange):
        """
        Description
            Create a route range for a protocol on a speficied port

        Parameters
            portName: <str>: Name of the port eg: "1/1/11"
            protocol: <str>: protocol to create route range. eg: <OSPF|OSPFV3|BGP|ISIS|EIGRP|RIP|RIPng>
            routeRange: <dict>: route range to configure <IPv4|IPv6> address
            eg: {'enabled': 'True', 'mask': 24, 'numberOfRoutes': 5, 'networkNumber': '8.7.7.1', 'metric': 10, 'origin': 'externalType1'}
                {'enabled': 'True', 'maskWidth': 64, 'numberOfRoute': 10, 'firstRoute': '7::1', 'metric': 10, 'nextHop': '7::2'}

        Syntax
            POST: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/ospf/router/{id}/routeRange/{id}
            DATA: {'enabled': 'True', 'mask': 24, 'numberOfRoutes': 5, 'networkNumber': '7.7.7.1', 'metric': 10, 'origin': 'externalType1'}

            POST: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/ospfV3/router/{id}/routeRange/{id}
            DATA: {'enabled': 'True', 'mask': 64, 'numberOfRoutes': 5, 'firstRoute': '7::1', 'metric': 10, 'type': 'anotherArea', 'addressFamily': 'unicast'}

            POST: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/eigrp/router/{id}/routeRange/{id}
            DATA: {'enabled': 'True', 'mask': 24, 'numberOfRoutes': 10, 'firstRoute': '7.7.7.1', 'metric': 10, 'nextHop': '7.7.7.2'}

            POST: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/rip/router/{id}/routeRange/{id}
            DATA: {'enabled': 'True', 'maskWidth': 24, 'noOfRoutes': 10, 'firstRoute': '7.7.7.1', 'metric': 10, 'nextHop': '7.7.7.2'}

            POST: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/ripng/router/{id}/routeRange/{id}
            DATA: {'enabled': 'True', 'maskWidth': 64, 'numberOfRoute': 10, 'firstRoute': '7::1', 'metric': 10, 'nextHop': '7::2'}

            POST: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/bgp/neighborRange/{id}/routeRange/{id}
            DATA: {'enabled': 'True', 'fromPrefix': 24, 'thruPrefix': 24, 'numRoutes': 10, 'networkAddress': '7.7.7.7'}

            POST: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/bgp/neighborRange/{id}/routeRange/{id}
            DATA: {'enabled': 'True', 'fromPrefix': 64, 'thruPrefix': 64, 'numRoutes': 10, 'networkAddress': '7::1'}

        Examples
            createRouteRangeOnProtocol(portName='1/1/11', protocol='ospf', routeRange={'enabled': 'True', 'mask': 24,
                                                                         'numberOfRoutes': 5, 'networkNumber': '8.7.7.1',
                                                                         'metric': 10, 'origin': 'externalType1'}
            createRouteRangeOnProtocol(portName='1/1/11', protocol='ospf', routeRange={'networkNumber': '8.7.7.1'}

        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport == None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))

        RouterInstanceList = self.getRouterInstanceByPortAndProtocol(protocol=protocol, vport=vport)
        if RouterInstanceList == []:
            raise IxNetRestApiException('No Router instance exists in protocol {0}'.format(protocol))

        self.ixnObj.logInfo('Router list %s' % RouterInstanceList)
        #routeRange = ast.literal_eval(routeRange)
        for eachRouterInstance in RouterInstanceList:
            url = self.ixnObj.httpHeader + eachRouterInstance + '/routeRange'
            self.ixnObj.post(url, data=routeRange)

    def getRouterInstanceByPortAndProtocol(self, protocol, vport):
        """
        Description
            Get router instance for the specified protocol on a speficied vport

        Parameters
            protocol: <str>: protocol to get a router instance
            vport: <str>: vport instance eg: "/api/v1/sessions/1/ixnetwork/vport/1"

        Syntax
            GET: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/router
            GET: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/neighborRange
            GET: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/host
            GET: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/bridge
            GET: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/actor
            GET: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/neighborPair

        Examples
            getRouterInstanceByPortAndProtocol(protocol='ospf', vport='/api/v1/sessions/1/ixnetwork/vport/1')

        Return
            RouterInstanceList
            Returns [] if no router instance exists
        """
        if protocol == 'bgp':
            nextNode = '/neighborRange'
        elif protocol == 'igmp' or protocol == 'mld':
            nextNode = '/host'
        elif protocol == 'stp':
            nextNode = '/bridge'
        elif protocol == 'rsvp':
            nextNode = '/neighborPair'
        elif protocol == 'lacp':
            nextNode = '/link'
        else:
            nextNode = '/router'
        url = vport+'/protocols/'+protocol+nextNode
        response = self.ixnObj.get(url)
        RouterInstanceList = ["%s" % (str(i["links"][0]["href"])) for i in response.json()]
        self.ixnObj.logInfo('Router Instance list %s' % RouterInstanceList)
        return RouterInstanceList

    def verifyProtocolSessionsUp(self, protocolViewName='BGP Peer Per Port', timeout=60):
        """
        Description
            Verify the specified protocol sessions are UP or not.

        Parameters
            protocolViewName: <str>: The protocol view name. Get this name from API browser or in IxNetwork GUI statistic tabs.
            timeout: <int>: Duration to wait for the protocol sessions to up. Default = 60 seconds.

        protocolViewName options:
            'BFD Aggregated Statistics'
            'BGP Aggregated Statistics'
            'ISIS Aggregated Statistics'
            'OSPF Aggregated Statistics'
            'RIPng Aggregated Statistics'
            'RIP Aggregated Statistics'
            'LDP Aggregated Statistics'
            'PIMSM Aggregated Statistics'
            'MPLSOAM Aggregated Statistics'

        Examples
            verifyProtocolSessionsUp(protcolViewName='ospf Aggregated Statistics')
            verifyProtocolSessionsUp(protcolViewName='ospf Aggregated Statistics',timeout=90)
        """
        totalSessionsDetectedUp = 0
        totalSessionsDetectedDown = 0
        totalPortsUpFlag = 0
        self.ixnObj.logInfo('Protocol view name %s' % protocolViewName)
        time.sleep(10)
        for counter in range(1, timeout + 1):
            stats = self.statObj.getStats(viewName=protocolViewName, displayStats=False)
            totalPorts = len(stats.keys())  # Length stats.keys() represents total ports.
            self.ixnObj.logInfo('ProtocolName: {0}'.format(protocolViewName))
            for session in stats.keys():
                if re.search('OSPF', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Full Nbrs.'])
                    totalSessions = int(stats[session]['Sess. Configured'])
                elif re.search('BGP', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Sess. Up'])
                    totalSessions = int(stats[session]['Sess. Configured'])
                elif re.search('ISIS', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['L2 Sess. Up'])
                    totalSessions = int(stats[session]['L2 Sess. Configured'])
                elif re.search('RIPng', protocolViewName, re.I) or re.search('BFD', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Routers Running'])
                    totalSessions = int(stats[session]['Routers Configured'])
                elif re.search('RIP', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Request Packet Tx'])
                    totalSessions = int(stats[session]['Routers Configured'])
                elif re.search('LACP', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['LAG Member Ports UP'])
                    totalSessions = int(stats[session]['Total LAG Member Ports'])
                elif re.search('LDP', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Targeted Sess. Up'])
                    totalSessions = int(stats[session]['Targeted Sess. Configured'])
                elif re.search('MPLS', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['BFD Up-Sessions'])
                    totalSessions = int(stats[session]['BFD Session Count'])
                elif re.search('PIM', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Rtrs. Running'])
                    totalSessions = int(stats[session]['Rtrs. Configured'])
                # totalSessionsNotStarted = int(stats[session]['Sessions Not Started'])
                totalExpectedSessionsUp = totalSessions

                if totalExpectedSessionsUp != 0:
                    self.ixnObj.logInfo(
                        '\n\tPortName: {0}\n\t   TotalSessionsUp: {1}\n\t   ExpectedTotalSessionsup: {2}'.format(
                            stats[session]['Port Name'], sessionsUp, totalExpectedSessionsUp), timestamp=False)
                    if counter < timeout and sessionsUp != totalExpectedSessionsUp:
                        self.ixnObj.logInfo('\t   Protocol Session is still down', timestamp=False)

                    if counter < timeout and sessionsUp == totalExpectedSessionsUp:
                        totalPortsUpFlag += 1
                        if totalPortsUpFlag == totalPorts:
                            self.ixnObj.logInfo('All protocol sessions are up!')
                            return

            if counter == timeout and sessionsUp != totalExpectedSessionsUp:
                raise IxNetRestApiException('Protocol Sessions failed to come up')

            self.ixnObj.logInfo('\n\tWait {0}/{1} seconds\n'.format(counter, timeout), timestamp=False)
            time.sleep(1)

    def verifyAllConfiguredProtocolSessions(self, duration):
        """
        Description
            verify all configured protocol sessions are UP or not

        Parameters
            duration: <int>: duration to wait for the protocol sessions to UP

        Examples
            verifyAllConfiguredProtocolSessions(duration=120)
            verifyAllConfiguredProtocolSessions(120)
        """
        response = self.getConfiguredProtocols()
        if response == []:
            raise IxNetRestApiException('No protocols Running or Configured or Enabled')

        for eachProtocol in response:
            if re.search('ospf', eachProtocol,re.I):
                viewName = 'OSPF Aggregated Statistics'
            elif re.search('ospfV3', eachProtocol,re.I):
                viewName = 'OSPFv3 Aggregated Statistics'
            elif re.search('bgp', eachProtocol,re.I):
                viewName = 'BGP Aggregated Statistics'
            elif re.search('isis', eachProtocol,re.I):
                viewName = 'ISIS Aggregated Statistics'
            elif re.search('ripng', eachProtocol,re.I):
                viewName = 'RIPng Aggregated Statistics'
            elif re.search('bfd', eachProtocol,re.I):
                viewName = 'BFD Aggregated Statistics'
            elif re.search('rip', eachProtocol,re.I):
                viewName = 'RIP Aggregated Statistics'
            elif re.search('ldp', eachProtocol,re.I):
                viewName = 'LDP Aggregated Statistics'
            elif re.search('mplsoam', eachProtocol,re.I):
                viewName = 'MPLSOAM Aggregated Statistics'
            elif re.search('pim', eachProtocol,re.I):
                viewName = 'PIMSM Aggregated Statistics'
            else:
                raise IxNetRestApiException('No viewName defined')

            self.verifyProtocolSessionsUp(protocolViewName=viewName, timeout=duration)
