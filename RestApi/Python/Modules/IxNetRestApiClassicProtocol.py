# PLEASE READ DISCLAIMER
#
#    This class demonstrates sample IxNetwork REST API usage for
#    demo and reference purpose only.
#    It is subject to change for updates without warning.
#
# Description
#    A class object for IxNetwork Classic Framework.

from IxNetRestApi import IxNetRestApiException

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
            Based on the specified protocol, return all ports associated withe the protocol.

        Parameter
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
            Get all enabled protocolss by the specified port.

        Parameter
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

    def sendArpOnPort(self, vport):
        """
        Description
            send Arp request on a vport interface.

        Return
            True on success Or False on failure
        """
        url = self.sessionUrl+'/vport/operations/sendarp'
        response = self.post(url, data={'arg1': vport})
        if self.waitForComplete(response, url+'/'+response.json()['id']) == False:
            return False

        return True

    def getDiscoveredNeighborOnPort(self, vport):
        """
        Description
            Get Arp discovered neighbor on a vport interface.

        Return
            discoverd mac address on success or False on failure
        """
        url = self.httpHeader+vport+'/discoveredNeighbor'
        response = self.get(url)
        if response == False: return False

        url = self.httpHeader+response.json()[0]['links'][0]['href']
        response = self.get(url)
        if response == False: return False

        self.logInfo('Discovered Neighbor: %s' % response.json()['neighborMac'])
        return response.json()['neighborMac']

    def startProtocolOnPort(self, protocol, port):
        """
        Description
            Start a protocol on a speficied port

        Syntax
            POST: /api/v1/sessions/{id}/ixnetwork/vport/protocols/<protocol>
            DATA: {'args': 'api/v1/sessions/1/ixnetwork/vport/1'}

        Return
            True on success Or False on failure
        """
        url = self.sessionUrl+'/vport/protocols/'+protocol+'/operations/start'
        port = port+'/protocols/'+protocol
        response = self.post(url, data={'arg1': port})
        if self.waitForComplete(response, url+'/'+response.json()['id']) == False:
            return False

        return True

    def getConfiguredProtocolList(self):
        """
        Description
            Get the list of protocols configured on vports.

        Return
            protocl list on success Or False on failure
            protocol list in format: "['ospf','bgp']"
        """
        configuredProtocolList = []
        node = '/router'
        protocolList = ['bfd', 'bgp', 'eigrp', 'isis', 'ldp', 'lisp',
                        'mplsOam', 'mplsTp', 'ospf', 'ospfV3', 'pimsm',
                        'rip', 'ripng']
        response = self.get(self.sessionUrl + '/vport')
        if response == False:
            self.logError('No ports connected to chassis')
            return False
        vportList = ['%s' % vport['links'][0]['href'] for vport in response.json()]
        for eachVport in vportList:
            for eachProtocol in protocolList:
                node = '/router'
                if re.search('bgp', eachProtocol):
                    node = '/neighborRange'
                protocolResponse = self.get(self.httpHeader + eachVport + '/protocols/' + eachProtocol)
                response = self.get(self.httpHeader + eachVport + '/protocols/' + eachProtocol + node)
                if response.json() != []:
                    if response.json()[0]['enabled'] == True and protocolResponse.json()['runningState'] == 'started':
                        configuredProtocolList.append(eachProtocol)
        configuredProtocolList = list(set(configuredProtocolList))
        return configuredProtocolList

    def enableProtocolOnPort(self, protocol, port, enable=True):
        """
         Description
            Enable protocol on a speficied port

        Syntax
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/router/{id}
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/neighborRange/{id}
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/host/{id}
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/bridge/{id}
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/actor/{id}
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/neighborPair/{id}

        Params
            protocol
            port - vport in format

        Return
            True on success Or False on failure
        """
        count = 0
        RouterInstanceList = self.getRouterInstanceOnProtocol(protocol=protocol, port=port)
        self.logInfo('RouterInstanceList %s' % RouterInstanceList)
        if RouterInstanceList == False:
            self.logError('No Router instance exists in protocol %s' % protocol)
            return False

        for eachRouterInstance in RouterInstanceList:
            url = self.httpHeader+eachRouterInstance
            if self.patch(url, data={"enabled": enable}) == False:
                count += 1

        if count != 0:
            return False

        return True

    def getProtocolSessionsStats(self, port, protocol):
        """
        Description
            Get protocol session status for a specified protocol on a port

        Parameter
            protocol: <str>: The protocol name.
            port:

        Return
              protocol stats in dictionary format eg: {'ospf': {'Configured': 2, 'Up': 1}} or False on failure
        """
        protocolStats = {}
        vport = self.getVportFromPhysicalPort(port=port)
        if vport == False:
            return False
        node = '/router'
        if re.search('bgp',protocol):
            node = '/neighborRange'
        response = self.get(self.httpHeader+vport+'/protocols/'+protocol+node)
        if response != False:
            if response.json()[0]['enabled'] == True:
                if re.search('ospf',protocol):
                    protocolViewName = 'OSPF Aggregated Statistics'
                elif re.search('ospfV3',protocol):
                    protocolViewName = 'OSPFv3 Aggregated Statistics'
                elif re.search('bgp',protocol):
                    protocolViewName = 'BGP Aggregated Statistics'
                elif re.search('isis',protocol):
                    protocolViewName = 'ISIS Aggregated Statistics'
                elif re.search('ripng',protocol):
                    protocolViewName = 'RIPng Aggregated Statistics'
                elif re.search('bfd',protocol):
                    protocolViewName = 'BFD Aggregated Statistics'
                elif re.search('rip',protocol):
                    protocolViewName = 'RIP Aggregated Statistics'
                elif re.search('ldp',protocol):
                    protocolViewName = 'LDP Aggregated Statistics'
                elif re.search('mplsoam',protocol):
                    protocolViewName = 'MPLSOAM Aggregated Statistics'
                elif re.search('pim',protocol):
                    protocolViewName = 'PIMSM Aggregated Statistics'
                else:
                    self.logError('No viewName defined')
                    return False
        else:
            self.logError('No {0} protocol running or configured or enabled on port {1}'.format(protocol,port))
            return False

        stats = self.getStats(viewName=protocolViewName, displayStats=False)
        if stats == False or stats == None:
            return False
        totalPorts = len(stats.keys()) ;# Length stats.keys() represents total ports.
        self.logInfo('ProtocolViewName: {0}'.format(protocolViewName))
        for session in stats.keys():
            #sessionsUp = int(stats[session]['Sessions Up'])
            if re.search('OSPF',protocolViewName):
                sessionsUp = int(stats[session]['Full Nbrs.'])
                totalSessions = int(stats[session]['Sess. Configured'])
            elif re.search('BGP',protocolViewName):
                sessionsUp = int(stats[session]['Sess. Up'])
                totalSessions = int(stats[session]['Sess. Configured'])
            elif re.search('ISIS',protocolViewName):
                sessionsUp = int(stats[session]['L2 Sess. Up'])
                totalSessions = int(stats[session]['L2 Sess. Configured'])
            elif re.search('RIPng',protocolViewName) or re.search('BFD',protocolViewName):
                sessionsUp = int(stats[session]['Routers Running'])
                totalSessions = int(stats[session]['Routers Configured'])
            elif re.search('RIP',protocolViewName):
                sessionsUp = int(stats[session]['Request Packet Tx'])
                totalSessions = int(stats[session]['Routers Configured'])
            elif re.search('LACP',protocolViewName):
                sessionsUp = int(stats[session]['LAG Member Ports UP'])
                totalSessions = int(stats[session]['Total LAG Member Ports'])
            elif re.search('LDP',protocolViewName):
                sessionsUp = int(stats[session]['Targeted Sess. Up'])
                totalSessions = int(stats[session]['Targeted Sess. Configured'])
            elif re.search('MPLS',protocolViewName):
                sessionsUp = int(stats[session]['BFD Up-Sessions'])
                totalSessions = int(stats[session]['BFD Session Count'])
            elif re.search('PIM',protocolViewName):
                sessionsUp = int(stats[session]['Rtrs. Running'])
                totalSessions = int(stats[session]['Rtrs. Configured'])
                #totalSessionsNotStarted = int(stats[session]['Sessions Not Started'])
            else:
                return False
            if stats[session]['Port Name'] == port:
                self.logInfo('\n\tPortName: {0}\n\t   TotalSessionsUp: {1}\n\t   TotalSessionsConfigured: {2}'.format(stats[session]['Port Name'], sessionsUp, totalSessions), timestamp=False)
                protocolStats[protocol] = {'Configured':totalSessions, 'Up':sessionsUp}
        return protocolStats

    def enableRouteRangeOnProtocol(self, port, protocol, routeRange, enable=True):
        """
        Description
            Enable a route range for a protocol on a speficied port
        Syntax
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/router/{id}/routeRange/{id}
            PATCH: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/neighborRange/{id}/routeRange/{id}

        Params
            protocol - <OSPF|OSPFV3|BGP|ISIS|EIGRP|RIP|RIPng>
            port - vport in format
            routeRange - IPv4|IPv6 address

        Return
            True on success Or False on failure
        """
        RouterInstanceList = self.getRouterInstanceOnProtocol(protocol=protocol, port=port)
        self.logInfo('Router list %s' % RouterInstanceList)
        node = '/routeRange'
        args = 'firstRoute'
        if protocol == 'ospf':
            args = 'networkNumber'
        if protocol == 'bgp':
            args = 'networkAddress'
        if RouterInstanceList == False:
            self.logError('No Router instance exists in protocol %s' % protocol)
            return False

        for eachRouterInstance in RouterInstanceList:
            url = self.httpHeader + eachRouterInstance + '/routeRange'
            response = self.get(url)
            RouteRangeInstanceList = ["%s" % (str(i["links"][0]["href"])) for i in response.json()]
            self.logInfo('Route Range list %s' % RouteRangeInstanceList)
            for eachRouteRange in RouteRangeInstanceList:
                url = self.httpHeader + eachRouteRange
                response = self.get(url)
                RouteRangeNetwork = response.json()[args]
                if RouteRangeNetwork == routeRange:
                    if self.patch(url, data={"enabled": enable}) == False:
                        return False

                    return True
            self.logError('Route range {0} does not exists in protocol {1}'.format(routeRange, protocol))
            return False

    def removeRouteRangeOnProtocol(self, port, protocol, routeRange):
        """
        Description
            Remove a route range for a protocol on a speficied port

        Syntax
            DELETE: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/router/{id}/routeRange/{id}
            DELETE: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/neighborRange/{id}/routeRange/{id}

        Params
            protocol - <OSPF|OSPFV3|BGP|ISIS|EIGRP|RIP|RIPng>
            port - vport in format
            routeRange - IPv4|IPv6 address

        Return
            True on success Or False on failure
        """
        RouterInstanceList = self.getRouterInstanceOnProtocol(protocol=protocol, port=port)
        self.logInfo('Router list %s' % RouterInstanceList)
        node = '/routeRange'
        args = 'firstRoute'
        if protocol == 'ospf':
            args = 'networkNumber'
        if protocol == 'bgp':
            args = 'networkAddress'
        if RouterInstanceList == False:
            self.logError('No Router instance exists in protocol %s' % protocol)
            return False

        for eachRouterInstance in RouterInstanceList:
            url = self.httpHeader+eachRouterInstance+'/routeRange'
            response = self.get(url)
            RouteRangeInstanceList = ["%s" % (str(i["links"][0]["href"])) for i in response.json()]
            self.logInfo('Route Range list %s' % RouteRangeInstanceList)
            for eachRouteRange in RouteRangeInstanceList:
                url = self.httpHeader+eachRouteRange
                response = self.get(url)
                RouteRangeNetwork = response.json()[args]
                if RouteRangeNetwork == routeRange:
                    if self.delete(url) == False:
                        return False

                    return True
            self.logError('Route range {0} does not exists in protocol {1}'.format(routeRange,protocol))
            return False

    def createRouteRangeOnProtocol(self, port, protocol, routeRange):
        """
        Description
            Create a route range for a protocol on a speficied port

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

        Params
            protocol - <OSPF|OSPFV3|BGP|EIGRP|RIP|RIPng>
            port - vport in format
            routeRange

        Return
            True on success Or False on failure
        """
        RouterInstanceList = self.getRouterInstanceOnProtocol(protocol=protocol, port=port)
        self.logInfo('Router list %s' % RouterInstanceList)
        if RouterInstanceList == False:
            self.logError('No Router instance exists in protocol %s' % protocol)
            return False

        routeRange = ast.literal_eval(routeRange)
        for eachRouterInstance in RouterInstanceList:
            url = self.httpHeader + eachRouterInstance + '/routeRange'
            if self.post(url, data=routeRange) == False:
                return False

            return True

    def getRouterInstanceOnProtocol(self, protocol, port):
        """
        Description
            Get router instance for the specified protocol on a speficied port

        Syntax
            GET: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/router
            GET: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/neighborRange
            GET: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/host
            GET: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/bridge
            GET: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/actor
            GET: /api/v1/sessions/{id}/ixnetwork/vport/{id}/protocols/<protocol>/neighborPair

        Params
            protocol
            port - vport in format

        Return
            RouterInstanceList on success or False on failure
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
        url = self.httpHeader+port+'/protocols/'+protocol+nextNode
        response = self.get(url)
        if response == False:
            self.logError('No such Protocols exists: %s' % protocol)
            return False

        RouterInstanceList = ["%s" % (str(i["links"][0]["href"])) for i in response.json()]
        if RouterInstanceList != []:
            return RouterInstanceList

        return False

    def verifyProtocolSessionsUp(self, protocolViewName='BGP Peer Per Port', timeout=60):
        """
        Description
            Verify all specified protocols sessions for UP.

        Parameter
            protocolViewName: <str>: The protocol view name. Get this name from API browser or in IxNetwork GUI statistic tabs.

            timeout: <int>: The timeout value to declare as failed. Default = 60 seconds.

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

        Return
            True on success Or False on failure
        """
        totalSessionsDetectedUp = 0
        totalSessionsDetectedDown = 0
        totalPortsUpFlag = 0
        self.logInfo('Protocol view name %s' % protocolViewName)
        time.sleep(10)
        for counter in range(1, timeout + 1):
            stats = self.getStats(viewName=protocolViewName, displayStats=False)
            totalPorts = len(stats.keys());  # Length stats.keys() represents total ports.
            self.logInfo('ProtocolName: {0}'.format(protocolViewName))
            for session in stats.keys():
                # sessionsUp = int(stats[session]['Sessions Up'])
                if re.search('OSPF', protocolViewName):
                    sessionsUp = int(stats[session]['Full Nbrs.'])
                    totalSessions = int(stats[session]['Sess. Configured'])
                elif re.search('BGP', protocolViewName):
                    sessionsUp = int(stats[session]['Sess. Up'])
                    totalSessions = int(stats[session]['Sess. Configured'])
                elif re.search('ISIS', protocolViewName):
                    sessionsUp = int(stats[session]['L2 Sess. Up'])
                    totalSessions = int(stats[session]['L2 Sess. Configured'])
                elif re.search('RIPng', protocolViewName) or re.search('BFD', protocolViewName):
                    sessionsUp = int(stats[session]['Routers Running'])
                    totalSessions = int(stats[session]['Routers Configured'])
                elif re.search('RIP', protocolViewName):
                    sessionsUp = int(stats[session]['Request Packet Tx'])
                    totalSessions = int(stats[session]['Routers Configured'])
                elif re.search('LACP', protocolViewName):
                    sessionsUp = int(stats[session]['LAG Member Ports UP'])
                    totalSessions = int(stats[session]['Total LAG Member Ports'])
                elif re.search('LDP', protocolViewName):
                    sessionsUp = int(stats[session]['Targeted Sess. Up'])
                    totalSessions = int(stats[session]['Targeted Sess. Configured'])
                elif re.search('MPLS', protocolViewName):
                    sessionsUp = int(stats[session]['BFD Up-Sessions'])
                    totalSessions = int(stats[session]['BFD Session Count'])
                elif re.search('PIM', protocolViewName):
                    sessionsUp = int(stats[session]['Rtrs. Running'])
                    totalSessions = int(stats[session]['Rtrs. Configured'])
                # totalSessionsNotStarted = int(stats[session]['Sessions Not Started'])
                totalExpectedSessionsUp = totalSessions

                if totalExpectedSessionsUp != 0:
                    self.logInfo(
                        '\n\tPortName: {0}\n\t   TotalSessionsUp: {1}\n\t   ExpectedTotalSessionsup: {2}'.format(
                            stats[session]['Port Name'], sessionsUp, totalExpectedSessionsUp), timestamp=False)
                    if counter < timeout and sessionsUp != totalExpectedSessionsUp:
                        self.logInfo('\t   Protocol Session is still down', timestamp=False)

                    if counter < timeout and sessionsUp == totalExpectedSessionsUp:
                        totalPortsUpFlag += 1
                        if totalPortsUpFlag == totalPorts:
                            self.logInfo('All protocol sessions are up!')
                            return True

            if counter == timeout and sessionsUp != totalExpectedSessionsUp:
                self.logError('\nProtocol Sessions failed to come up')
                return False
            self.logInfo('\n\tWait {0}/{1} seconds\n'.format(counter, timeout), timestamp=False)
            time.sleep(1)

