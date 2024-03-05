# PLEASE READ DISCLAIMER
#
#    This class demonstrates sample IxNetwork REST PY usage for demo and
#    reference purpose only.It is subject to change for updates without
#    warning.
#
# Description
#    A class object for IxNetwork Classic Framework.

import re
import time
from IxNetRestApi import IxNetRestApiException
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiStatistics import Statistics


class ClassicProtocol(object):
    def __init__(self, ixnObj=None):
        """
        Parameters
           ixnObj: <str>: The main connection object.
        """
        self.ixnObj = ixnObj
        self.ixNetwork = ixnObj.ixNetwork
        self.portMgmtObj = PortMgmt(self.ixnObj)
        self.statObj = Statistics(self.ixnObj)

    def getPortsByProtocol(self, protocolName):
        """
        Description
            Based on the specified protocol, return all ports associated with the protocol.

        Parameters
           protocolName options:
              bfd, bgp, cfm, eigrp, elmi, igmp, isis, lacp, ldp, linkOam, lisp, mld, mplsOam,
              mplsTp, openFlow, ospf, ospfV3, pimsm, ping, rip, ripng, rsvp, static, stp

        Returns: [chassisIp, cardNumber, portNumber]
                  Example: [['192.168.70.11', '1', '1'],['192.168.70.11', '1', '2']]

        Returns [] if no port is configured with the specified protocolName
        """
        portList = []
        vportList = self.ixNetwork.Vport.find()
        for vport in vportList:
            protocol = protocolName[0].capitalize() + protocolName[1:]
            protocolObj = getattr(vport.Protocols.find(), protocol)
            if protocolObj.Enabled:
                assignedTo = vport.AssignedTo
                currentChassisIp = assignedTo.split(':')[0]
                currentCardNumber = assignedTo.split(':')[1]
                currentPortNumber = assignedTo.split(':')[2]
                currentPort = [currentChassisIp, currentCardNumber, currentPortNumber]
                portList.append(currentPort)
        return portList

    def getProtocolListByPort(self, port):
        """
        Description
            Get all enabled protocols by the specified port.

        Parameters
            port: [chassisIp, cardNumber, portNumber] ->['192.168.70.11', '2', '8']
        """
        self.ixnObj.logInfo('\ngetProtocolListByPort...')
        protocolList = ['bfd', 'bgp', 'cfm', 'eigrp', 'elmi', 'igmp', 'isis', 'lacp', 'ldp',
                        'linkOam', 'lisp', 'mld', 'mplsOam', 'mplsTp', 'openFlow', 'ospf', 'ospfV3',
                        'pimsm', 'ping', 'rip', 'ripng', 'rsvp', 'stp']
        self.ixnObj.logInfo('\ngetProtocolListByPort...')
        chassis = str(port[0])
        card = str(port[1])
        port = str(port[2])
        portObj = chassis + ":" + card + ":" + port
        enabledProtocolList = []
        vport = self.ixNetwork.Vport.find(AssignedTo=portObj)
        for protocol in protocolList:
            currentProtocol = protocol[0].capitalize() + protocol[1:]
            protocolObj = getattr(vport.Protocols.find(), currentProtocol)
            if protocolObj.Enabled:
                enabledProtocolList.append(str(protocol))
        return enabledProtocolList

    def sendArpOnPort(self, portName):
        """
        Description
            Send Arp request on a specified port

        Parameters
            portName: <str>: Name of the port. eg: '1/1/11'

        Examples
            sendArpOnPort(portName='1/1/11')
        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport is None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))
        vport.SendArp()

    def getDiscoverdNeighborOnPort(self, portName):
        """
        Description
            Get Arp discovered neighbor on a specified port

        Parameters
            portName: <str>: Name of the port. eg: '1/1/11'

        Examples
            getDiscoverdNeighborOnPort(portName='1/1/11')

        Return
            Discovered mac address
        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport is None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))
        discoveredNeighborMac = vport.DiscoveredNeighbor.find().NeighborMac
        self.ixnObj.logInfo('Discovered Neighbor: %s' % discoveredNeighborMac)
        return discoveredNeighborMac

    def startStopProtocolOnPort(self, protocol, portName, action='start'):
        """
        Description
            Start and stop a protocol on a specified port

        Parameters
            protocol: <str>: Protocol to start
            portName: <str>: Name of the port, eg: '1/1/11'
            action: <str>: start or stop a protocol, default is start

        Examples
            startStopProtocolOnPort(protocol='ospf', portName='1/1/11')
            startStopProtocolOnPort(protocol='ospf', portName='1/1/11', action='stop')
        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport is None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))
        protocol = protocol[0].capitalize() + protocol[1:]
        protocolObj = getattr(vport.Protocols.find(), protocol)
        if action == "start":
            protocolObj.Start()
        if action == "stop":
            protocolObj.Stop()

    def getConfiguredProtocols(self):
        """
        Description
            Get the list of protocols configured on vports.

        Return
            A list or one or more congfigured protocols eg: "['ospf','bgp']"
            return [] if no protocol is configured
        """
        configuredProtocolList = []
        availableProtocolList = ['bfd', 'bgp', 'cfm', 'eigrp', 'elmi', 'igmp', 'isis', 'lacp',
                                 'ldp', 'linkOam', 'lisp', 'mld', 'mplsOam', 'mplsTp', 'openFlow',
                                 'ospf', 'ospfV3', 'pimsm', 'ping', 'rip', 'ripng', 'rsvp', 'stp']
        vportList = self.ixNetwork.Vport.find()
        if not vportList:
            raise IxNetRestApiException('No ports connected to chassis')

        protocolNextNodeDict = {'bgp': 'NeighborRange', 'igmp': 'Host', 'mld': 'Host',
                                'stp': 'Bridge', 'cfm': 'Bridge', 'rsvp': 'NeighborPair',
                                'lacp': 'Link', 'linkOam': 'Link', 'elmi': 'Uni',
                                'openFlow': 'Device'}
        protocols = ['bgp', 'igmp', 'mld', 'stp', 'cfm', 'rsvp', 'lacp', 'linkOam', 'elmi',
                     'openFlow']
        for eachVport in vportList:
            for protocol in availableProtocolList:
                if protocol in protocols:
                    nextNode = protocolNextNodeDict[protocol]
                else:
                    nextNode = 'Router'
                protocol = protocol[0].capitalize() + protocol[1:]
                protocolResponse = getattr(eachVport.Protocols.find(), protocol)
                nextNodeObj = getattr(protocolResponse, nextNode)
                routerInstancesObj = nextNodeObj.find()
                if routerInstancesObj:
                    if routerInstancesObj.Enabled and protocolResponse.RunningState == 'started':
                        configuredProtocolList.append(protocol)
        configuredProtocolList = list(set(configuredProtocolList))
        return configuredProtocolList

    def enableProtocolOnPort(self, protocol, portName, enable=True):
        """
        Description
           Enable protocol on a speficied port

        Parameters
            protocol: <str>: Protocol to start
            portName: <str>: Name of the port eg: '1/1/11'
            enable: <bool> enable or disable specified protocol.

        Examples
            enableProtocolOnPort(protocol='ospf', portName='1/1/11')
            enableProtocolOnPort(protocol='ospf', portName='1/1/11', enable=False)
        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport is None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))

        RouterInstanceList = self.getRouterInstanceByPortAndProtocol(protocol=protocol, vport=vport)
        if not RouterInstanceList:
            raise IxNetRestApiException('No Router instance exists in protocol {0}'.format(
                protocol))
        for eachRouterInstance in RouterInstanceList:
            eachRouterInstance.Enabled = enable

    def getProtocolSessionsStats(self, portName, protocol):
        """
        Description
            Get a protocol session status for a specified protocol on a port

        Parameters
            portName: <str>: Name of the Port eg: "1/1/11"
            protocol: <str>: Name of the protocol. eg: <ospf/ospfV3/bgp/isis/ripng/bfd/rip/ldp/pim>

        Examples
            getProtocolSessionsStats(portName='1/1/11', protocol='ospf')

        Return
            Protocol stats in dictionary format eg: {'ospf': {'Configured': 2, 'Up': 1}}
        """
        protocolStats = {}
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport is None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))
        protocolNextNodeDict = {'bgp': 'NeighborRange', 'igmp': 'Host', 'mld': 'Host',
                                'stp': 'Bridge', 'cfm': 'Bridge', 'rsvp': 'NeighborPair', 'lacp':
                                    'Link', 'linkOam': 'Link', 'elmi': 'Uni', 'openFlow': 'Device'}
        protocols = ['bgp', 'igmp', 'mld', 'stp', 'cfm', 'rsvp', 'lacp', 'linkOam', 'elmi',
                     'openFlow']
        if protocol in protocols:
            nextNode = protocolNextNodeDict[protocol]
        else:
            nextNode = 'Router'
        protocol = protocol[0].capitalize() + protocol[1:]
        protocolResponse = getattr(vport.Protocols.find(), protocol)
        nextNodeObj = getattr(protocolResponse, nextNode)
        routerInstancesObj = nextNodeObj.find()

        if routerInstancesObj:
            if routerInstancesObj.Enabled and (protocolResponse.RunningState == 'started' or
                                               protocolResponse.ProtocolState == 'started'):
                if protocol in ['Bfd', 'Bgp', 'Cfm', 'Eigrp', 'Elmi', 'Igmp', 'Isis', 'Lacp', 'Ldp',
                                'Lisp', 'Mld', 'MplsTp', 'MplsOam', 'Ospf', 'Rip', 'Rsvp', 'Stp']:
                    protocolViewName = protocol.upper() + 'Aggregated Statistics'
                elif re.search('LinkOam', protocol, re.I):
                    protocolViewName = 'OAM Aggregated Statistics'
                elif re.search('openFlow', protocol, re.I):
                    protocolViewName = 'OpenFlow Switch Aggregated Statistics'
                elif re.search('OspfV3', protocol, re.I):
                    protocolViewName = 'OSPFv3 Aggregated Statistics'
                elif re.search('Pim', protocol, re.I):
                    protocolViewName = 'PIMSM Aggregated Statistics'
                elif re.search('Ripng', protocol, re.I):
                    protocolViewName = 'RIPng Aggregated Statistics'
                else:
                    raise IxNetRestApiException('No viewName defined')
            else:
                raise IxNetRestApiException('No {0} protocol running or enabled on port {1}'.
                                            format(protocol, portName))
        else:
            raise IxNetRestApiException('No {0} protocol configured on port {1}'.format(protocol,
                                                                                        portName))

        stats = self.statObj.getStats(viewName=protocolViewName, displayStats=False)
        self.ixnObj.logInfo('ProtocolViewName: {0}'.format(protocolViewName))
        for session in stats.keys():
            if re.search('BFD', protocolViewName, re.I) or re.search('RIPng', protocolViewName,
                                                                     re.I):
                sessionsUp = int(stats[session]['Routers Running'])
                totalSessions = int(stats[session]['Routers Configured'])
            elif re.search('BGP', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Sess. Up'])
                totalSessions = int(stats[session]['Sess. Configured'])
            elif re.search('CFM', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Bridges Running'])
                totalSessions = int(stats[session]['Bridges Configured'])
            elif re.search('EIGRP', protocolViewName, re.I) or re.search('ELMI', protocolViewName,
                                                                         re.I):
                sessionsUp = int(stats[session]['IPv4 Routers Running'])
                totalSessions = int(stats[session]['IPv4 Routers Configured'])
            elif re.search('IGMP', protocolViewName, re.I) or re.search('MLD', protocolViewName,
                                                                        re.I):
                sessionsUp = int(stats[session]['Host Total Frames Tx'])
                totalSessions = int(stats[session]['Host Total Frames Rx'])
            elif re.search('ISIS', protocolViewName, re.I):
                sessionsUp = int(stats[session]['L2 Sess. Up'])
                totalSessions = int(stats[session]['L2 Sess. Configured'])
            elif re.search('LACP', protocolViewName, re.I):
                sessionsUp = int(stats[session]['LAG Member Ports UP'])
                totalSessions = int(stats[session]['Total LAG Member Ports'])
            elif re.search('LDP', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Targeted Sess. Up'])
                totalSessions = int(stats[session]['Targeted Sess. Configured'])
            elif re.search('OAM', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Links Running'])
                totalSessions = int(stats[session]['Links Configured'])
            elif re.search('LISP', protocolViewName, re.I):
                sessionsUp = int(stats[session]['MS/MR Running'])
                totalSessions = int(stats[session]['MS/MR Configured'])
            elif re.search('MPLSTP', protocolViewName, re.I):
                sessionsUp = int(stats[session]['CCCV Up'])
                totalSessions = int(stats[session]['CCCV Configured'])
            elif re.search('MPLSOAM', protocolViewName, re.I):
                sessionsUp = int(stats[session]['BFD Up-Sessions'])
                totalSessions = int(stats[session]['BFD Session Count'])
            elif re.search('OpenFlow', protocolViewName, re.I):
                sessionsUp = int(stats[session]['OF Channel Configured Up'])
                totalSessions = int(stats[session]['OF Channel Configured'])
            elif re.search('OSPF', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Full Nbrs.'])
                totalSessions = int(stats[session]['Sess. Configured'])
            elif re.search('PIM', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Rtrs. Running'])
                totalSessions = int(stats[session]['Rtrs. Configured'])
            elif re.search('RIP', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Request Packet Tx'])
                totalSessions = int(stats[session]['Routers Configured'])
            elif re.search('RSVP', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Ingress LSPs Up'])
                totalSessions = int(stats[session]['Ingress LSPs Configured'])
            elif re.search('STP', protocolViewName, re.I):
                sessionsUp = int(stats[session]['Forwarding State Count'])
                totalSessions = int(stats[session]['Discarding State Count'])
            else:
                raise IxNetRestApiException('No protocol viewName found')

            if stats[session]['Port Name'] == portName:
                self.ixnObj.logInfo('\n\tPortName: {0}\n\t   TotalSessionsUp: {1}\n\t   '
                                    'TotalSessionsConfigured: {2}'.
                                    format(stats[session]['Port Name'], sessionsUp, totalSessions),
                                    timestamp=False)
                protocolStats[protocol] = {'Configured': totalSessions, 'Up': sessionsUp}
        return protocolStats

    def enableRouteRangeOnProtocol(self, portName, protocol, routeRange, enable=True):
        """
        Description
            Enable a route range for a protocol on a speficied port

        Parameters
            portName: <str>: Name of the port eg: "1/1/11"
            protocol: <str>: protocol to enable route range.
            routeRange: <str>: route range <IPv4|IPv6> address
            enable: <bool>: enable or disable route range, default is True

        Examples:
            enableRouteRangeOnProtocol(protName='1/1/11', protocol='ospf', routeRange='10.10.10.1')
            enableRouteRangeOnProtocol(protName='1/1/11', protocol='ospfv3', routeRange='10::1',
            enable=True)
        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport is None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))

        RouterInstanceList = self.getRouterInstanceByPortAndProtocol(protocol=protocol, vport=vport)
        if not RouterInstanceList:
            raise IxNetRestApiException('No Router instance exists in protocol {0}'.
                                        format(protocol))
        argsDict = {'ospf': 'NetworkNumber', 'bgp': 'NetworkAddress'}

        if protocol in ['ospf', 'bgp']:
            args = argsDict[protocol]
        else:
            args = 'firstRoute'

        for eachRouterInstance in RouterInstanceList:
            RouteRangeInstanceList = eachRouterInstance.RouteRange.find()
            self.ixnObj.logInfo('Route Range list %s' % RouteRangeInstanceList)

            for eachRouteRange in RouteRangeInstanceList:
                RouteRangeNetwork = getattr(eachRouteRange, args)
                if RouteRangeNetwork == routeRange:
                    eachRouteRange.Enabled = enable
                    return
            raise IxNetRestApiException('Route range: {0} does not exist in protocol: {1} port: {2}'
                                        .format(routeRange, protocol, portName))

    def removeRouteRangeOnProtocol(self, portName, protocol, routeRange):
        """
        Description
            Remove a route range for a protocol on a speficied port

        Parameters
            portName: <str>: Name of the port eg: "1/1/11"
            protocol: <str>: protocol to remove route range.
            routeRange: <str>: route range <IPv4|IPv6> address

        Examples:
            removeRouteRangeOnProtocol(protName='1/1/11', protocol='ospf', routeRange='10.10.10.1')
            removeRouteRangeOnProtocol(protName='1/1/11', protocol='ospfv3', routeRange='10::1')
        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport is None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))

        RouterInstanceList = self.getRouterInstanceByPortAndProtocol(protocol=protocol, vport=vport)
        if not RouterInstanceList:
            raise IxNetRestApiException('No Router instance exists in protocol {0}'.format(
                protocol))

        self.ixnObj.logInfo('Router list %s' % RouterInstanceList)
        argsDict = {'ospf': 'NetworkNumber', 'bgp': 'NetworkAddress'}

        if protocol in ['ospf', 'bgp']:
            args = argsDict[protocol]
        else:
            args = 'firstRoute'

        for eachRouterInstance in RouterInstanceList:
            RouteRangeInstanceList = eachRouterInstance.RouteRange.find()
            self.ixnObj.logInfo('Route Range list %s' % RouteRangeInstanceList)
            for eachRouteRange in RouteRangeInstanceList:
                RouteRangeNetwork = getattr(eachRouteRange, args)
                if RouteRangeNetwork == routeRange:
                    eachRouteRange.remove()
                    return
            raise IxNetRestApiException('Route range: {0} does not exist in protocol: {1} port: {2}'
                                        .format(routeRange, protocol, portName))

    def createRouteRangeOnProtocol(self, portName, protocol, routeRange):
        """
        Description
            Create a route range for a protocol on a speficied port

        Parameters
            portName: <str>: Name of the port eg: "1/1/11"
            protocol: <str>: protocol to create route range.
            routeRange: <dict>: route range to configure <IPv4|IPv6> address
            eg: {'enabled': 'True', 'mask': 24, 'origin': 'externalType1',
            'networkNumber': '8.7.7.1', 'metric': 10, 'numberOfRoutes': 5}
                {'enabled': 'True', 'maskWidth': 64, 'numberOfRoute': 10, 'firstRoute': '7::1',
                'metric': 10, 'nextHop': '7::2'}

        Examples
            createRouteRangeOnProtocol(portName='1/1/11', protocol='ospf',
            routeRange={'enabled': 'True', 'mask': 24, 'numberOfRoutes': 5,
            'networkNumber': '8.7.7.1', 'metric': 10, 'origin': 'externalType1'}
            createRouteRangeOnProtocol(portName='1/1/11', protocol='ospf',
            routeRange={'networkNumber': '8.7.7.1'}

        """
        vport = self.portMgmtObj.getVportObjectByName(portName)
        if vport is None:
            raise IxNetRestApiException('PortName {0} not connected to chassis'.format(portName))

        RouterInstanceList = self.getRouterInstanceByPortAndProtocol(protocol=protocol, vport=vport)
        if not RouterInstanceList:
            raise IxNetRestApiException('No Router instance exists in protocol {0}'.format(
                protocol))

        self.ixnObj.logInfo('Router list %s' % RouterInstanceList)
        for eachRouterInstance in RouterInstanceList:
            if not eachRouterInstance.RouteRange.find():
                routeRangeObj = eachRouterInstance.RouteRange.add()
            else:
                routeRangeObj = eachRouterInstance.RouteRange.find()
            for key, value in routeRange:
                key = key[0].capitalize() + key[1:]
                setattr(routeRangeObj, key, value)

    def getRouterInstanceByPortAndProtocol(self, protocol, vport):
        """
        Description
            Get router instance for the specified protocol on a speficied vport

        Parameters
            protocol: <str>: protocol to get a router instance
            vport: <str>: vport instance

        Examples
            getRouterInstanceByPortAndProtocol(protocol='ospf', vport=vport object)

        Return
            RouterInstanceList
            Returns [] if no router instance exists
        """
        protocolNextNodeDict = {'bgp': 'NeighborRange', 'igmp': 'Host', 'mld': 'Host',
                                'stp': 'Bridge', 'cfm': 'Bridge', 'rsvp': 'NeighborPair',
                                'lacp': 'Link', 'linkOam': 'Link', 'elmi': 'Uni',
                                'openFlow': 'Device'}
        protocols = ['bgp', 'igmp', 'mld', 'stp', 'cfm', 'rsvp', 'lacp', 'linkOam', 'elmi',
                     'openFlow']
        if protocol in protocols:
            nextNode = protocolNextNodeDict[protocol]
        else:
            nextNode = 'Router'
        RouterInstanceList = []
        protocol = protocol[0].capitalize() + protocol[1:]
        protocolObj = getattr(vport.Protocols.find(), protocol)
        nextNodeObj = getattr(protocolObj, nextNode)
        RouterInstancesList = nextNodeObj.find()
        for eachRouterInstance in RouterInstancesList:
            RouterInstanceList.append(eachRouterInstance)
        self.ixnObj.logInfo('Router Instance list %s' % RouterInstanceList)
        return RouterInstanceList

    def verifyProtocolSessionsUp(self, protocolViewName='BGP Peer Per Port', timeout=60):
        """
        Description
            Verify the specified protocol sessions are UP or not.

        Parameters
            protocolViewName: <str>: The protocol view name.
            timeout: <int>: Duration to wait for the protocol sessions to up.Default = 60 seconds.

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
        totalSessions = 0
        totalPortsUpFlag = 0
        totalExpectedSessionsUp = 0
        sessionsUp = 0
        self.ixnObj.logInfo('Protocol view name %s' % protocolViewName)
        time.sleep(10)
        for counter in range(1, timeout + 1):
            stats = self.statObj.getStats(viewName=protocolViewName, displayStats=False)
            totalPorts = len(stats.keys())
            self.ixnObj.logInfo('ProtocolName: {0}'.format(protocolViewName))
            for session in stats.keys():
                if re.search('BFD', protocolViewName, re.I) or re.search('RIPng', protocolViewName,
                                                                         re.I):
                    sessionsUp = int(stats[session]['Routers Running'])
                    totalSessions = int(stats[session]['Routers Configured'])
                elif re.search('BGP', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Sess. Up'])
                    totalSessions = int(stats[session]['Sess. Configured'])
                elif re.search('CFM', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Bridges Running'])
                    totalSessions = int(stats[session]['Bridges Configured'])
                elif re.search('EIGRP', protocolViewName, re.I) or \
                        re.search('ELMI', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['IPv4 Routers Running'])
                    totalSessions = int(stats[session]['IPv4 Routers Configured'])
                elif re.search('IGMP', protocolViewName, re.I) or re.search('MLD',
                                                                            protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Host Total Frames Tx'])
                    totalSessions = int(stats[session]['Host Total Frames Rx'])
                elif re.search('ISIS', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['L2 Sess. Up'])
                    totalSessions = int(stats[session]['L2 Sess. Configured'])
                elif re.search('LACP', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['LAG Member Ports UP'])
                    totalSessions = int(stats[session]['Total LAG Member Ports'])
                elif re.search('LDP', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Targeted Sess. Up'])
                    totalSessions = int(stats[session]['Targeted Sess. Configured'])
                elif re.search('OAM', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Links Running'])
                    totalSessions = int(stats[session]['Links Configured'])
                elif re.search('LISP', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['MS/MR Running'])
                    totalSessions = int(stats[session]['MS/MR Configured'])
                elif re.search('MPLSTP', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['CCCV Up'])
                    totalSessions = int(stats[session]['CCCV Configured'])
                elif re.search('MPLSOAM', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['BFD Up-Sessions'])
                    totalSessions = int(stats[session]['BFD Session Count'])
                elif re.search('OpenFlow', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['OF Channel Configured Up'])
                    totalSessions = int(stats[session]['OF Channel Configured'])
                elif re.search('OSPF', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Full Nbrs.'])
                    totalSessions = int(stats[session]['Sess. Configured'])
                elif re.search('PIM', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Rtrs. Running'])
                    totalSessions = int(stats[session]['Rtrs. Configured'])
                elif re.search('RIP', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Request Packet Tx'])
                    totalSessions = int(stats[session]['Routers Configured'])
                elif re.search('RSVP', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Ingress LSPs Up'])
                    totalSessions = int(stats[session]['Ingress LSPs Configured'])
                elif re.search('STP', protocolViewName, re.I):
                    sessionsUp = int(stats[session]['Forwarding State Count'])
                    totalSessions = int(stats[session]['Discarding State Count'])
                totalExpectedSessionsUp = totalSessions

                if totalExpectedSessionsUp != 0:
                    self.ixnObj.logInfo('\n\tPortName: {0}\n\t   TotalSessionsUp: {1}\n\t   '
                                        'ExpectedTotalSessionsup: {2}'.
                                        format(stats[session]['Port Name'], sessionsUp,
                                               totalExpectedSessionsUp), timestamp=False)
                    if counter < timeout and sessionsUp != totalExpectedSessionsUp:
                        self.ixnObj.logInfo('\t   Protocol Session is still down', timestamp=False)

                    if counter < timeout and sessionsUp == totalExpectedSessionsUp:
                        totalPortsUpFlag += 1
                        if totalPortsUpFlag == totalPorts:
                            self.ixnObj.logInfo('All protocol sessions are up!')
                            return

            if counter == timeout and sessionsUp != totalExpectedSessionsUp:
                raise IxNetRestApiException('Protocol Sessions failed to come up')

            self.ixnObj.logInfo('\n\tWait {0}/{1} seconds\n'.format(counter, timeout),
                                timestamp=False)
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
        confifuredProtocols = self.getConfiguredProtocols()
        if not confifuredProtocols:
            raise IxNetRestApiException('No protocols Running or Configured or Enabled')

        for protocol in confifuredProtocols:
            if protocol in ['Bfd', 'Bgp', 'Cfm', 'Eigrp', 'Elmi', 'Igmp', 'Isis', 'Lacp', 'Ldp',
                            'Lisp', 'Mld', 'MplsTp', 'MplsOam', 'Ospf', 'Rip', 'Rsvp', 'Stp']:
                protocolViewName = protocol.upper() + 'Aggregated Statistics'
            elif re.search('LinkOam', protocol, re.I):
                protocolViewName = 'OAM Aggregated Statistics'
            elif re.search('openFlow', protocol, re.I):
                protocolViewName = 'OpenFlow Switch Aggregated Statistics'
            elif re.search('OspfV3', protocol, re.I):
                protocolViewName = 'OSPFv3 Aggregated Statistics'
            elif re.search('Pim', protocol, re.I):
                protocolViewName = 'PIMSM Aggregated Statistics'
            elif re.search('Ripng', protocol, re.I):
                protocolViewName = 'RIPng Aggregated Statistics'
            else:
                raise IxNetRestApiException('No viewName defined')
            self.verifyProtocolSessionsUp(protocolViewName=protocolViewName, timeout=duration)
