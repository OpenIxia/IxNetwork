# PLEASE READ DISCLAIMER
#
#    This class demonstrates sample IxNetwork REST API usage for
#    demo and reference purpose only.
#    It is subject to change for updates without warning.
#
# Description
#    A class object for IxNetwork Classic Framework.

from .IxNetRestApi import IxNetRestApiException

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
