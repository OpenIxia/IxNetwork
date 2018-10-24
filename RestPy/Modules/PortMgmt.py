import sys, time

class Ports(object):
    def __init__(self, ixNetworkObject):
        self.ixNetObj = ixNetworkObject

    def connectToChassis(self,ixChassisIpList):
        """
        Connect to one or more chassis and wait until all chassis's are connected and ready.

        :param ixChassisIpList: <list>: One or more chassis IP address in a list.
        """
        counterStop = 45
        for ixChassisIp in ixChassisIpList:
            for counter in range(1, counterStop+1):
                #chassisStatus = self.ixNetObj.AvailableHardware.add_Chassis(Hostname=ixChassisIp)
                chassisStatus = self.ixNetObj.AvailableHardware.Chassis.add(Hostname=ixChassisIp)
                if counter < counterStop and chassisStatus.State != 'ready':
                    print('\nChassis {0} is not connected yet. Waiting {1}/{2} seconds'.format(ixChassisIp,
                                                                                               counter, counterStop))
                    time.sleep(1)

                if counter < counterStop and chassisStatus.State == 'ready':
                    print('\n{0}'.format(chassisStatus))
                    break

                if counter == counterStop:
                    raise Exception('\nFailed to connect to chassis: {0}'.format(ixChassisIp[0]))

    def arePortsAvailable(self, portList, raiseException=False):
        """
        Description
           Verify if ports are owned by another user.
        
        Parameters
           portList: <list>: [[ixChassisIp, 1, 2], [ixChassisIp, 1, 3], ]
           raiseException: <bool>: Raise an exception if True.

        Example
           # 0=Available  1=Not Available. Currently owned.
           if portObj.arePortsAvailable(portList) != 0:
               if forceTakePortOwnership == True:
                   portObj.releasePorts(portList)
               else:
                   raise Exception('Ports are currently owned by another user and forceTakePortOwnership is set to False')

        Raise
           Exception if raiseException == True

        Returns
           0 = Available
           1 = Not available.
        """
        exceptionFlag = 0
        for port in portList:
            ixChassisIp = port[0]
            cardId = port[1]
            portId = port[2]

            portIdObj = self.ixNetObj.AvailableHardware.Chassis(Ip=ixChassisIp)[0].Card(CardId=cardId)[0].Port(PortId=portId)[0]
            if portIdObj.Owner != '':
                print('\n{0} is currently owned by: {1}'.format(port, portIdObj.Owner))
                exceptionFlag = 1

        if exceptionFlag and raiseException:
            raise Exception('Ports are not available')

        if exceptionFlag and raiseException == False:
            return 1

        if exceptionFlag == 0:
            # Ports are not owned
            return 0

    def releasePorts(self, ports='all'):
        """
        Release all ports or release specified ports in the param ports.
        
        :param ports: <'all'|list>:
                         If ports == 'all', release all ports.
                         If ports = list: [[ixChassisIp, 1, 2], [ixChassisIp, 1, 3], ...],
                            release specified ports.
        """
        if ports == 'all':
            self.ixNetObj.Vport.find().ReleasePort()

        if ports != 'all':
            for port in ports:
                regexString = ''
                # Construct the regex string format = '(1.1.1.1:2:3)'
                regexString = regexString + '(' + str(port[0])+':'+str(port[1])+':'+str(port[2]) + ')'
                vport = self.ixNetObj.Vport.find(AssignedTo=regexString)
                if vport:
                    print('\nReleasing port: {0}:{1}'.format(port, vport.href))
                    vport.ReleasePort()

    def getVportFromPortList(self, portList):
        """
        Get vports from the portList

        :param portList: <list>: [[ixChassisIp, 1, 2], [ixChassisIp, 1, 3], ]

        Return:
           List of vports or None
        """
        vports = []
        regexString = ''
        for port in portList:
            # Construct the regex string format = '(1.1.1.1:2:3)|(1.1.1.1:6:2)'
            regexString = regexString + '(' + str(port[0])+':'+str(port[1])+':'+str(port[2]) + ')'
            if port != portList[-1]:
                regexString = regexString + '|'

        vports = [vport.href for vport in self.ixNetObj.Vport.find(AssignedTo=regexString)]
        return vports
 
    def assignPorts(self, portList, takePortOwnership=False, getVportList=False):
        """
        Assign ports.

        :param portList: <list>: [[ixChassisIp, 1, 2], [ixChassisIp, 1, 3], ]
        :param takePortOwnership: <bool>: True == forcefully take port ownership.
        :param getVportList: <bool>: Set to True if one of the below conditions are true:
                                           - already created vports.
                                           - loading a saved config file that
                                             has vports configured.

                                      This will get the configured vports
                                      and assign physical ports to the already created vports. 
        
        Raise:
           If portList are owned by another user and if takePortOwnership
           is False, then raise exception. 
        """
        vportList = []
        testPorts = []
        if getVportList:
            vportList = [vport.href for vport in self.ixNetObj.Vport.find()]

        for port in portList:
            testPorts.append(dict(Arg1=port[0], Arg2=port[1], Arg3=port[2]))

        print('\nAssignPorts: {0}'.format(portList))
        self.ixNetObj.AssignPorts(testPorts, [], vportList, takePortOwnership)
