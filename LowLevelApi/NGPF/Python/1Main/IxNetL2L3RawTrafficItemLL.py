#!/usr/local/python2.7.6/bin/python2.7

# Description
#
#    This script will use Python and IxNetwork low level APIs to 
#    create two NGPF IPv4 topolopgies with back-to-back ports.
#    Then it will add TCP header to the Traffic Item and modify
#    the tcp srcPort and dstPort fields.
#
#    If you use NGPF, its has to be Ethernet/LAN or IPv4 trafifc type, that is not RAW.
#    No need create DG, if you create RAW, just source and dest are ports.
#    If you use VM ports to do back to back, you probably not seeing the traffic. Use a physical ports instead.

import sys
import os
import re
import time

import IxNetwork

def ConnectToIxia( ixNetTclServer='', ixNetTclPort='8009', ixNetVersion='' ):
    ixNetConnect = ixNet.connect(ixNetTclServer, 'port', ixNetTclPort, '-version', ixNetVersion)

    print 'Verifying ixNet.connect():', ixNetConnect ;# ::ixNet::OK

    if ixNetConnect != '::ixNet::OK':
        print 'Failed to connect to:', ixNetTclServer
        sys.exit()
    else:
        print 'Successfully connected to:', ixNetTclServer


def CreateNewBlankConfig():
    print '\nCreating a blank configuration ...'
    ixNet.execute('newConfig')
    

def AddIxiaChassis( ixChassisIp ):
    print '\nAdding chassis: ', ixChassisIp
    ixChassisObj = ixNet.add(ixNet.getRoot()+'availableHardware', 'chassis', '-hostname', ixChassisIp)
    ixNet.commit()
    '''
    ixChassisObj1:  ::ixNet::OBJ-/availableHardware/chassis:L10988
    ixChassisObj2:  ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"
    '''
    ixChassisObj = ixNet.remapIds(ixChassisObj)[0]
    return ixChassisObj


def ClearPortOwnership( ixChassisObj, portList ):
    for port in portList:
        # port looks like '1 2'.
        # Must do a port.split(' ') to convert string to list -> ['1', '2']
        cardNumber = port.split('/')[0]
        portNumber = port.split('/')[1]
        
        # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:2
        #print ('Clearing port'), 'card:'+cardNumber+'/port:'+portNumber
        print 'Clearing port:', ixChassisObj+'/card:' + cardNumber + '/port:' + portNumber

        try:
            ixNet.execute('clearOwnership', ixChassisObj+'/card:'+cardNumber+'/port:'+portNumber)
        except Exception, e:
            # Unable to release ownership is ok when the configuration is blanked already
            pass


def CreateVPort( port ):
    print '\nCreating new VPort for %s' % port

    vPortObj = ixNet.add(ixNet.getRoot(), 'vport')
    ixNet.commit()
    vPortObj = ixNet.remapIds(vPortObj)[0]
    return vPortObj
    

def ConnectToPorts(vPortList, portList, ixChassisObj):
    print '\nConnectToPorts: vportList:', vPortList
    print 'portList:', portList
    print 'ixChassisObj:', ixChassisObj

    for vPort, port in zip(vPortList, portList):
        cardNumber = port.split('/')[0]
        portNumber = port.split('/')[1]
        
        print '\nConnectToPort:', ixChassisObj + '/card:' + cardNumber + '/port:' + portNumber
        print '\tvPort =', vPort

        ixNet.setAttribute(vPort, \
                               '-connectedTo', ixChassisObj + '/card:' + cardNumber + '/port:' + portNumber
                           )

    print '\nRebooting ports.  Will take 40 seconds ...'
    ixNet.commit()


def VerifyPortState( portList='', stopTime=120 ):
    for vPort in ixNet.getList(ixNet.getRoot(), 'vport'):
        assignedPort = ixNet.getAttribute(vPort, '-assignedTo')        
        print '\nVerifying port state on port::', assignedPort

        for timer in range(0, stopTime):
            portState = ixNet.getAttribute(vPort, '-state')
            print '\tCurrent port state:', portState

            if timer < stopTime and portState == 'up':
                print '\tVerifyPortState: ', assignedPort + ' is up'
                break

            if timer < stopTime and portState != 'up':
                print '\tVerifyPortState: %s is not up yet. Verifying %d/%d seconds' % (assignedPort, timer, stopTime)
                time.sleep(1)

            if timer == stopTime and portState != 'up':
                print '\nPort can\'t come up.  Exiting test'
                return 1


def CreateTopologyPy(topologyName, vPorts):
    print '\nCreateTopology: %s : %s' % (topologyName, vPorts)
    topologyObj = ixNet.add(ixNet.getRoot(), 'topology')
    ixNet.setMultiAttribute(topologyObj,
                            '-name', topologyName,
                            '-vports', vPorts
                        )
    ixNet.commit()
    return topologyObj

def CreateDeviceGroupPy(topologyObj, deviceGroupName, multiplier):
    print '\nCreateDeviceGroup: %s : %s' % (topologyObj, deviceGroupName)
    deviceGroupObj = ixNet.add(topologyObj, 'deviceGroup')
    ixNet.setMultiAttribute(deviceGroupObj,
                            '-name', deviceGroupName,
                            '-multiplier', multiplier
                        )
    ixNet.commit()
    return deviceGroupObj

def CreateEthernetNgpfPy(deviceGroupObj, ethernetName):
    print '\nCreateEthernetNgpfPy: %s : %s' % (deviceGroupObj, ethernetName)
    ethernetObj = ixNet.add(deviceGroupObj, 'ethernet')
    ixNet.setMultiAttribute(ethernetObj, '-name', 'ethernetName')
    ixNet.commit()
    return ethernetObj

def CreateIpv4NgpfPy(ethernetObj, ipv4Name='',
                     ipv4StartValue=None, ipv4Step='0.0.0.1', ipv4Direction='increment',
                     ipv4PrefixStartValue=None, ipv4PrefixStep='0', ipv4PrefixDirection='incremnet',
                     gatewayIpStartValue=None, gatewayIpStep='0.0.0.1', gatewayIpDirection='increment'):

    # Example: 
    #     ipv4Obj = CreateIpv4NgpfPy(ethernet1, 'ipv4-1', ipv4StartValue='1.1.1.1', gatewayIpStartValue='1.1.1.2', ipv4PrefixStartValue='24')

    print '\nCreateIpv4StackNgpf: %s : %s' % (ethernetObj, ipv4Name)
    ipv4Obj = ixNet.add(ethernetObj, 'ipv4')
    if ipv4Name != '':
        ixNet.setAttribute(ipv4Obj, '-name', ipv4Name)
        ixNet.commit()

    if ipv4StartValue != None:
        # ::ixNet::OBJ-/multivalue:2
        ipv4Multivalue = ixNet.getAttribute(ipv4Obj, '-address')
        ixNet.setMultiAttribute(ipv4Multivalue,
                                '-clearOverlays', 'true',
                                '-pattern', 'counter'
                            )

        # ::ixNet::OBJ-/multivalue:2/counter
        ipv4MultivalueCounter = ixNet.add(ipv4Multivalue, 'counter')
        ixNet.setMultiAttribute(ipv4MultivalueCounter,
                                '-start', ipv4StartValue,
                                '-step', ipv4Step,
                                '-direction', ipv4Direction
                            )

    if ipv4PrefixStartValue != None:
        prefixMultivalue = ixNet.getAttribute(ipv4Obj, '-prefix')

        ixNet.setMultiAttribute(prefixMultivalue,
                                '-clearOverlays', 'true',
                                '-pattern', 'conter'
                            )

        prefixMultivalueCounter = ixNet.add(prefixMultivalue, 'counter')
        ixNet.setMultiAttribute(prefixMultivalueCounter,
                                '-start', ipv4PrefixStartValue,
                                '-step', ipv4PrefixStep,
                                '-direction', ipv4PrefixDirection
                            )

    if gatewayIpStartValue != None:
        gatewayMultivalue = ixNet.getAttribute(ipv4Obj, '-gatewayIp')
        ixNet.setMultiAttribute(gatewayMultivalue,
                                '-clearOverlays', 'true',
                                '-pattern', 'counter'
        )

        gatewayMultivalueCounter = ixNet.add(gatewayMultivalue, 'counter')
        ixNet.setMultiAttribute(gatewayMultivalueCounter,
                                '-start', gatewayIpStartValue,
                                '-step', gatewayIpStep,
                                '-direction', gatewayIpDirection
        )
    ixNet.commit()        
    return ipv4Obj

def StartAllProtocolsPy():
    print '\nStartAllProtocolsPy'
    ixNet.execute('startAllProtocols')
    ixNet.commit()
    time.sleep(2)

def DeviceGroupProtocolStackNgpfPy(deviceGroup, ipType):
    # This Proc is an internal API for VerifyArpNgpf.
    # It's created because each deviceGroup has IPv4/IPv6 and
    # a deviceGroup could have inner deviceGroup that has IPv4/IPv6.
    # Therefore, you can loop device groups.

    import re
    unresolvedArpList = []
    for ethernet in ixNet.getList(deviceGroup, 'ethernet'):
        for ipProtocol in ixNet.getList(ethernet, ipType):
            resolvedGatewayMac = ixNet.getAttribute(ipProtocol, '-resolvedGatewayMac')
            for index in range(0, len(resolvedGatewayMac)):
                if (bool(re.match('.*Unresolved.*', resolvedGatewayMac[index]))):
                    multivalueNumber = ixNet.getAttribute(ipProtocol, '-address')
                    srcIpAddrNotResolved = ixNet.getAttribute(ixNet.getRoot()+multivalueNumber, '-values')[index]
                    print '\tFailed to resolveARP:',  srcIpAddrNotResolved
                    unresolvedArpList.append(srcIpAddrNotResolved)

    if unresolvedArpList == []:
        print '\tARP is resolved'
        return 0
    else:
        return unresolvedArpList

def VerifyArpNgpfPy(ipType='ipv4'):
    # This API requires:
    #    1> DeviceGroupProtocolStacksNgpfPy
    #
    # ipType:  ipv4 or ipv6
    #
    # This API will verify for ARP session resolvement on 
    # every TopologyGroup/DeviceGroup and/or
    #       TopologyGroup/DeviceGroup/DeviceGroup that has protocol "enabled".
    # 
    # How it works?
    #    Each device group has a list of $sessionStatus: up, down or notStarted.
    #    If the deviceGroup has sessionStatus as "up", then ARP will be verified.
    #    It also has a list of $resolvedGatewayMac: MacAddress or removePacket[Unresolved]
    #    These two lists are aligned.
    #    If lindex 0 on $sessionSatus is up, then the API expects lindex 0 on $resolvedGatewayMac 
    #    to have a mac address.
    #    If not, then arp is not resolved.
    #    This script will wait up to the $maxRetry before it declares failed.
    #
    # Return 0 if ARP passes.
    # Return 1 if device group is not started
    # Return a list of unresolved ARPs
    print '\nVerifyArpNgpfPy'

    startFlag = 0
    unresolvedArpList = []
    for topology in ixNet.getList(ixNet.getRoot(), 'topology'):
        for deviceGroup in ixNet.getList(topology, 'deviceGroup'):
            print '\n', deviceGroup
            deviceGroupStatus = ixNet.getAttribute(deviceGroup, '-status')
            print '\tdeviceGroup status:', deviceGroupStatus
            if deviceGroupStatus == 'started':
                startFlag = 1
                arpResult = DeviceGroupProtocolStackNgpfPy(deviceGroup, ipType)
                if arpResult != 0:
                    unresolvedArpList = unresolvedArpList + arpResult
                
                if ixNet.getList(deviceGroup, 'deviceGroup') != '':
                    for innerDeviceGroup in ixNet.getList(deviceGroup, 'deviceGroup'):
                        print '\n', innerDeviceGroup
                        arpResult = DeviceGroupProtocolStackNgpfPy(innerDeviceGroup, ipType)
                        if arpResult != 0:
                            unresolvedArpList = unresolvedArpList + arpResult
            elif ixNet.getAttribute(deviceGroup, '-status') == 'mixed':
                startFlag = 1
                print '\tWarning: Ethernet stack is started, but layer3 is not started'
                arpResult = DeviceGroupProtocolStackNgpf(deviceGroup, ipType)
                if arpResult != 0:
                    unresolvedArpList = unresolvedArpList + arpResult
                    
                if ixNet.getList(deviceGroup, 'deviceGroup') != '':
                    for innerDeviceGroup in ixNet.getList(deviceGroup, 'deviceGroup'):
                        print '\n', innerDeviceGroup
                        deviceGroupStatus2 = ixNet.getAttribute(innerDeviceGroup, '-status')
                        if deviceGroupStatus2 == 'started':
                            arpResult = DeviceGroupProtocolStackNgpfPy(deviceGroup, ipType)
                            if arpResult != 0:
                                unresolvedArpList = unresolvedArpList + arpResult

    if unresolvedArpList == [] and startFlag == 1:
        return 0
    if unresolvedArpList == [] and startFlag == 0:
        return 1
    if unresolvedArpList != [] and startFlag == 1:
        print '\n'
        for unresolvedArp in unresolvedArpList:
            print 'UnresolvedArps:', unresolvedArp
        print '\n'
        return unresolvedArpList

def CreateTrafficItem(name=          'My Traffic Item', 
                      trafficType=   'ipv4', 
                      transmitMode=  'interleaved', 
                      biDirectional= '1', 
                      routeMesh=     'oneToOne', 
                      srcDestMesh=   'oneToOne'
                      ):
    
    print '\nCreating Traffic Item: %s ...' % name
    trafficItemObj = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
    
    ixNet.setMultiAttribute(trafficItemObj,
                            '-enabled', 'True',
                            '-name', name,
                            '-routeMesh', routeMesh,
                            '-srcDestMesh', srcDestMesh,
                            '-trafficType', trafficType,
                            '-transmitMode', transmitMode,
                            '-biDirectional', biDirectional,
                            )
    ixNet.commit()
    trafficItemObj = ixNet.remapIds(trafficItemObj)[0]
    return trafficItemObj


def ConfigTracking( trafficItemObj, trackingList ):
    print '\nConfiguring trackBy: %s ...' % trackingList
    ixNet.setAttribute(trafficItemObj + '/tracking',
                       '-trackBy', trackingList
                       )
    ixNet.commit()
    
def CreateEndPointSet(trafficItemObj='', 
                      name='Flow_Group', 
                      srcEndpoints='', 
                      destEndpoints=''
                      ):
    '''
    Each endpoint is a highlevelstream in a Traffic Item
    '''
    
    print '\nCreating Endpoint: %s ...' % name
    endpointObj = ixNet.add(trafficItemObj, 'endpointSet',
                            '-name', name,
                            '-sources', srcEndpoints,
                            '-destinations', destEndpoints
                            )
    ixNet.commit()
    endpointObj = ixNet.remapIds(endpointObj)[0]
    return endpointObj


def ConfigFlowGroup(flowGroupObj='', frameSize='128', frameRate='100'):
    print '\nConfiguring Flow Group:', flowGroupObj
    print '\nConfiguring frame size:', frameSize
    ixNet.setAttribute(flowGroupObj + '/frameSize', '-fixedSize', frameSize)
    
    print '\nConfiguring line rate: %s%s' % (frameRate, '%')
    ixNet.setAttribute(flowGroupObj + '/frameRate', '-rate', frameRate)
    ixNet.commit()

        
def ConfigFlowGroupFrameCount(flowGroupObj, frameCount):
    print '\nConfiguring frame count:', frameCount
    result = ixNet.setMultiAttribute(flowGroupObj + '/transmissionControl',
                                     '-frameCount', frameCount,
                                     '-type', 'fixedFrameCount'
                                     )
    ixNet.commit()
    

def ApplyTraffic():
    print '\nApplying Traffic to hardware ...'
    #traffic = ixNet.getRoot()+'/traffic'
    #ixNet.execute('apply', traffic)

    stopCounter = 10
    for startCounter in range(1,10):
        applyResult = ixNet.execute('apply', ixNet.getRoot() + 'traffic')

        print '\nApplyTraffic: ', applyResult
        if applyResult != '::ixNet::OK' and startCounter < stopCounter:
            print '\nApplyTraffic: Attempting to apply traffic:', startCounter+'/'+stopCounter+' tries'
            time.sleep(1)
            continue

        if applyResult == '::ixNet::OK' and startCounter == stopCounter:
            print '\nApplyTraffic Error:', applyResult
            ixNet.disconnect()
            sys.exit()

        if applyResult == '::ixNet::OK' and startCounter < stopCounter:
            print '\nSuccessfully applied traffic to hardware'
            break

def RegenerateAllTrafficItems():
    for trafficItem in ixNet.getList(ixNet.getRoot()+'/traffic', 'trafficItem'):
        regenerateResult = ixNet.execute('generate', trafficItem)
        if regenerateResult != '::ixNet::OK':
            print '\nRegenerateAllTrafficItem error:', trafficItem
            ixNet.disconnect()
            sys.exit()
        else:
            print '\nRegenerateAllTrafficItem:', trafficItem


def SendArp():
    for vPort in ixNet.getList(ixNet.getRoot(), 'vport'):
        for interface in ixNet.getList(vPort, 'interface'):
            interfaceType = ixNet.getAttribute(interface, '-type')

            # Don't send arps on Unconnected Routed or GRE interfaces
            if re.search(r'default', interfaceType):
                isIntEnabled = ixNet.getAttribute(interface, '-enabled')
                if re.search(r'true', isIntEnabled, re.I):
                    print 'Sent ARP on:', interface
                    ixNet.execute('sendArp', interface)
                    ixNet.execute('sendNs', interface)


def VerifyArpDiscoveries():
    '''
       - Get a list of all the expected Gateway IP addresses for each vPort.
       - Get only if the interface is enabled. We don't care about gateways if the
         interface isn't enabled.
       - Ignore Routed and GRE and Unconnected interfaces
       - Then get a list of all the discovered arps.
       - At the end, compare the two list. Any left overs are unresolved arps.
    '''

    resolvedArp = []
    allIpGateways = []

    for vPort in ixNet.getList(ixNet.getRoot(), 'vport'):
	# Refresh the arp table on this vport first
        ixNet.execute('refreshUnresolvedNeighbors', vPort)
        currentVportInterfaceList = ixNet.getList(vPort, 'interface')
        for interface in currentVportInterfaceList:
            # Ignore the Unconnected Routed and GRE interfaces
            interfaceType = ixNet.getAttribute(interface, '-type')
            if re.search(r'default', interfaceType):
                # Only append the gateway if the interface is enabled.
                isIntEnabled = ixNet.getAttribute(interface, '-enabled')
                if re.search(r'true', isIntEnabled, re.I):
                    ipv4Gateway = ixNet.getAttribute(interface+'/ipv4', '-gateway')
                    if re.search(r'null', ipv4Gateway, re.I) is None:
                        if ipv4Gateway not in allIpGateways:
                            allIpGateways.append(ipv4Gateway)

                    ipv6GatewayList = ixNet.getList(interface, 'ipv6')
                    if ipv6GatewayList:
                        for ipv6Gateway in ipv6GatewayList:
                            ipv6 = ixNet.getAttribute(ipv6Gateway, '-gateway')
                            if ipv6 != '0:0:0:0:0:0:0:0':
                                if ipv6 not in allIpGateways:
                                    allIpGateways.append(ipv6)

    print '\nExpected IP addresses to resolve ARPs:'
    for arp in allIpGateways:
        print '\t', arp

    for vPort in ixNet.getList(ixNet.getRoot(), 'vport'):
        # Get all the discovered ARPs for the current vPort
        vPortInterfaceList = ixNet.getList(vPort, 'discoveredNeighbor')
        if vPortInterfaceList:
            currentPort = ixTopo.getPort[vPort]

            for vPortInt in vPortInterfaceList:
                # vPortInt = ::ixNet::OBJ-/vport:1/discoveredNeighbor:1
                currentVp = vPortInt.split('/')
                currentVp = currentVp[:2]
                currentVp = '/'.join(currentVp)
                discoveredIp = ixNet.getAttribute(vPortInt, '-neighborIp')
                discoveredMac = ixNet.getAttribute(vPortInt, '-neighborMac')
                print '\nDiscovered arp on:', currentPort, ': ', discoveredIp, discoveredMac
                # discoveredMac is not empty or != 00:00:00:00:00:00
                if discoveredMac is not '' and discoveredMac is not '00:00:00:00:00:00':
                    # if  true, then append resolvedArp
                    if discoveredIp in allIpGateways:
                        resolvedArp.append(discoveredIp)

    # Now compare the expected list of arps with what is resolved.
    # Any left overs are unresovled arps.
    for resolvedGateway in resolvedArp:
        if resolvedGateway in allIpGateways:
            ipGatewayIndex = allIpGateways.index(resolvedGateway)
            allIpGateways.pop(ipGatewayIndex)

    if allIpGateways:
        print '\nError: Unresloved ARPs:'
        for unresolvedArp in allIpGateways:
            print '\t',(unresolvedArp)
        ixNet.disconnect()
        sys.exit()
    else:
        print('All ARPs are resolved')


def CheckTrafficState():
    currentTrafficState = ixNet.getAttribute(ixNet.getRoot()+'traffic', '-state')

    if currentTrafficState == '::ixNet::OK':
        return 'notRunning'
    elif currentTrafficState == 'stopped':
        return 'stopped'
    elif currentTrafficState == 'started':
        return 'started'
    elif currentTrafficState == 'locked':
        return 'locked'
    elif currentTrafficState == 'unapplied':
        return 'unapplied'
    elif currentTrafficState == 'startedWaitingForStreams':
        return 'startedWaitingForStreams'
    elif currentTrafficState == 'stoppedWaitingForStats':
        return 'stoppedWaitingForStats'
    else:
        return currentTrafficState


def StartTraffic():
    traffic = ixNet.getRoot()+'traffic'

    print '\nStarting traffic ...'
    for retry in range(1,10):
        retry = retry + 1

        try:
            result = ixNet.execute('start', traffic)
            if result != '::ixNet::OK':
                print '\nFailed to start traffic:', result
                ixNet.disconnect()
                sys.exit()
            else:
                print '\nExecuting startTraffic:', result
                break

        except Exception, e:
            print '\nException error: Failed to start traffic:', e
            print '\nRetrying:', retry, '/', 10
            time.sleep(1)

            if retry == 10:
                print '\nCan\'t start traffic. Exiting.'
                ixNet.disconnect()
                sys.exit()

    time.sleep(2)
    startCounter = 1
    stopCounter = 11

    for start in range(startCounter, stopCounter):
        start = start + 1
        trafficState = CheckTrafficState()
        
        if trafficState == 'started':
            print('Traffic started')
            break

        if trafficState == 'stopped':
            print('Traffic stopped')
            break

        if trafficState == 'startedWaitingForStats' or trafficState == 'stoppedWaitingForStats':
            print('Traffic started. Waiting for stats to complete')
            break

        if start < stopCounter:
            if trafficState != 'started' or trafficState != 'startedWaitingForStats' or \
                    trafficState != 'stoppedWaitingForStats' or trafficStats != 'stopped':
                print '\nStartTraffic: Current state = ', trafficState+'.'+' Waiting', start+'/'+stopCounter
                time.sleep(1)

        if start == stopCounter:
            if trafficState != 'started' or trafficState != 'startedWaitingForStats' or \
                    trafficState != 'stoppedWaitingForStats' or trafficStats != 'stopped':
                print '\nFailed: Traffic failed to start'
                ixNet.disconnect()
                sys.exit()
    

def GetStatsPy( getStatsBy='Flow Statistics', csvFile=None, csvEnableFileTimestamp=False):
    '''
    Description:
        This API will return you a Python Dict of all the stats 
        based on your specified stats. The exact stat name could 
        be found on your IxNetwork GUI statistic tablets.

    Parameters:
        getStatsBy = The exact name of the stat that could be found on the IxNetwork GUI.
        csvFile    = The name of the CSV file that you want to store stats in.
        csvEnableFileTimestamp = Append a timestamp to the CSV file so they don't get overwritten.
                                 This should only be used for getting the final stat result such as 
                                 when the traffic has completely stopped.
                            
    getStatsBy options (case sensitive):
    
        "Port Statistics"
        "Tx-Rx Frame Rate Statistics"
        "Port CPU Statistics"
        "Global Protocol Statistics"
        "Protocols Summary"
        "Port Summary"
        "OSPFv2-RTR Drill Down"
        "OSPFv2-RTR Per Port"
        "IPv4 Drill Down"
        "L2-L3 Test Summary Statistics"
        "Flow Statistics"
        "Traffic Item Statistics"
    '''

    viewList = ixNet.getList(ixNet.getRoot()+'/statistics', 'view')
    statViewSelection = getStatsBy
    try:
        statsViewIndex = viewList.index('::ixNet::OBJ-/statistics/view:"' + getStatsBy +'"')
    except Exception, errMsg:
        sys.exit('\nNo such statistic name: %s' % getStatsBy)

    # ::ixNet::OBJ-/statistics/view:"Flow Statistics"
    view = viewList[statsViewIndex]

    columnList = ixNet.getAttribute(view+'/page', '-columnCaptions')
    #print '\n', columnList

    if csvFile != None:
        import csv
        csvFileName = csvFile.replace(' ', '_')
        if csvEnableFileTimestamp:
            import datetime
            timestamp = datetime.datetime.now().strftime('%H%M%S')
            if '.' in csvFileName:
                csvFileNameTemp = csvFileName.split('.')[0]
                csvFileNameExtension = csvFileName.split('.')[1]
                csvFileName = csvFileNameTemp+'_'+timestamp+'.'+csvFileNameExtension
            else:
                csvFileName = csvFileName+'_'+timestamp

        csvFile = open(csvFileName, 'w')
        csvWriteObj = csv.writer(csvFile)
        csvWriteObj.writerow(columnList)

    startTime = 1
    stopTime = 30
    for timer in xrange(startTime, stopTime + 1):
        totalPages = ixNet.getAttribute(view+'/page', '-totalPages')
        if totalPages == 'null':
            print 'GetStatView: Getting total pages for %s is not ready: %s/%s' % (getStatsBy, startTime, stopTime)
            time.sleep(2)
        else:
            break

    row = 0
    statDict = {}

    print '\nPlease wait for all the stats to be queried ...'
    for currentPage in xrange(1, int(totalPages)+1):
        ixNet.setAttribute(view+'/page', '-currentPage', currentPage)
        ixNet.commit()

        whileLoopStopCounter = 0
        while (ixNet.getAttribute(view+'/page', '-isReady')) != 'true':
            if whileLoopStopCounter == 5:
                print'\nGetStatView: Could not get stats'
                return 1

            if whileLoopStopCounter < 5:
                print'\nGetStatView: Not ready yet. Waiting %s/5 seconds ...' % whileLoopStopCounter
                time.sleep(1)
                whileLoopStopCounter += 1

        pageList = ixNet.getAttribute(view+'/page', '-rowValues')
        totalFlowStatistics = len(pageList)

        for pageListIndex in xrange(0, totalFlowStatistics):
            rowList = pageList[pageListIndex]
            if csvFile != None:
                csvWriteObj.writerow(rowList[0])
            
            for rowIndex in xrange(0, len(rowList)):
                row += 1
                cellList = rowList[rowIndex]
                statDict[row] = {}
                # CellList: ['Ethernet - 002', 'Ethernet - 001', 'OSPF T1 to T2', '206.27.0.0-201.27.0.0', 'OSPF T1 to T2-FlowGroup-1 - Flow Group 0002', '1225', '1225', '0', '0', '0', '0', '0', '0', '156800', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '00:00:00.781', '00:00:00.849']
                index = 0
                for statValue in cellList:
                    statDict[row].update({columnList[index]: statValue})
                    index += 1

    if csvFile != None:
        csvFile.close()
    return statDict


def DisconnectIxNet():
    print '\nDisconnecting IxNetwork ...'
    disconnect = ixNet.disconnect()

def PrintDict(obj, nested_level=0, output=sys.stdout):
    """
    Print each dict key with indentions for readability.
    """

    spacing = '   '
    if type(obj) == dict:
        print >> output, '%s' % ((nested_level) * spacing)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                PrintDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % ((nested_level + 1) * spacing, k, v)

        print >> output, '%s' % (nested_level * spacing)

    elif type(obj) == list:
        print >> output, '%s[' % ((nested_level) * spacing)
        for v in obj:
            if hasattr(v, '__iter__'):
                PrintDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % ((nested_level) * spacing)

    else:
        print >> output, '%s%s' % (nested_level * spacing, obj)


ixNet  = IxNetwork.IxNet()

class IxTopoNamespace: pass
ixTopo = IxTopoNamespace()

ixNetTclServer = '192.168.70.127'
ixChassisIp = '192.168.70.10'
ixNetTclPort = '8009'
ixNetVersion = '8.20'
portList = ['1/1', '2/1']

ConnectToIxia(ixNetTclServer=ixNetTclServer, ixNetVersion=ixNetVersion)
CreateNewBlankConfig()
ixChassisObj = AddIxiaChassis(ixChassisIp)
ClearPortOwnership(ixChassisObj, portList)

vport1Obj = CreateVPort('1/1')
vport2Obj = CreateVPort('2/1')
ixTopo.vPortList = [vport1Obj, vport2Obj]

ConnectToPorts(ixTopo.vPortList, portList, ixChassisObj)
if VerifyPortState():
    sys.exit()


topology1 = CreateTopologyPy('Topo1', vport1Obj)
topology2 = CreateTopologyPy('Topo2', vport2Obj)

deviceGroup1 = CreateDeviceGroupPy(topology1, 'DG1', '1')
deviceGroup2 = CreateDeviceGroupPy(topology2, 'DG2', '1')

ethernet1 = CreateEthernetNgpfPy(deviceGroup1, 'Ethernet1')
ethernet2 = CreateEthernetNgpfPy(deviceGroup2, 'Ethernet2')

ipv41 = CreateIpv4NgpfPy(ethernet1, 'ipv4-1', ipv4StartValue='1.1.1.1', gatewayIpStartValue='1.1.1.2', ipv4PrefixStartValue='24')
#ConfigIpv4AddressNgpfPy(ipv41, '1.1.1.1')
#ConfigIpv4GatewayNgpfPy(ipv41, '1.1.1.2')

ipv42 = CreateIpv4NgpfPy(ethernet2, 'ipv42', ipv4StartValue='1.1.1.2', gatewayIpStartValue='1.1.1.1', ipv4PrefixStartValue='27')
#ConfigIpv4AddressNgpfPy(ipv42, '1.1.1.2')
#ConfigIpv4GatewayNgpfPy(ipv42, '1.1.1.1')

StartAllProtocolsPy()
VerifyArpNgpfPy()



trafficItem1Obj = CreateTrafficItem(name='TCP', trafficType='ipv4')

# ::ixNet::OBJ-/traffic/trafficItem:1/endpointSet:1
endpoint1Obj = CreateEndPointSet(trafficItemObj=trafficItem1Obj,
                                 name='FlowGroup1', 
                                 srcEndpoints=topology1,
                                 destEndpoints=topology2,
                             )
configElementObj = ixNet.getList(trafficItem1Obj, 'configElement')[0]

print '\nconfigElementObj:', configElementObj

ConfigFlowGroup(flowGroupObj=configElementObj, frameSize='256', frameRate='75')
ConfigTracking(trafficItem1Obj, ['flowGroup0'])

#ixNet.commit()
#RegenerateAllTrafficItems()

# ------ Add a TCP header  -------#

currentPacketHeaders = ixNet.getList(configElementObj, 'stack')
print '\nCurrent packet headers ...'
for currentHeader in currentPacketHeaders:
    if bool(re.search('ipv4', currentHeader, re.I)):
        ipv4Header = currentHeader
    print '\t', currentHeader

# currentPacketHeaders
# ['::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ethernet-1"',
#  '::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ipv4-2"',
#  '::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"fcs-4"']

# Get a list of all the protocol headers
protocolTemplate = ixNet.getList(ixNet.getRoot()+'/traffic', 'protocolTemplate')

for eachProtocolTemplate in protocolTemplate:
    if bool(re.search('tcp', eachProtocolTemplate, re.I)):
        tcpTemplate = eachProtocolTemplate
        break

# tcpTemplate = ::ixNet::OBJ-/traffic/protocolTemplate:"tcp"
print '\nAdding tcp Header:', tcpTemplate
print 'Behind:', ipv4Header

# Add tcp to the top of the ipv4 header:
# protocolTemplate = ::ixNet::OBJ-/traffic/protocolTemplate:
ixNet.execute('append', ipv4Header, tcpTemplate)
ixNet.commit()

# Verify the new stack for the tcp header
newPacketHeader = ixNet.getList(configElementObj, 'stack')
print '\nNew packdet headers...'
for eachHeader in newPacketHeader:
    print '\t', eachHeader
    if bool(re.search('tcp', eachHeader, re.I)):
        tcpHeader = eachHeader

# tcpHeader = ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"tcp-3"
print '\ntcp header:', tcpHeader

# entire tcp header = ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"tcp-3"/field:"tcp.header.srcPort-1"
ixNet.setMultiAttribute(tcpHeader+'/field:"tcp.header.srcPort-1"',
                        '-auto', 'false',
                        '-valueType', 'singleValue',
                        '-fieldValue', '3333',
                        '-singleValue', '3333')

ixNet.setMultiAttribute(tcpHeader+'/field:"tcp.header.dstPort-2"',
                        '-auto', 'false',
                        '-valueType', 'singleValue',
                        '-singleValue', '80')
ixNet.commit()

ApplyTraffic()
RegenerateAllTrafficItems()
time.sleep(10)
StartTraffic()
time.sleep(10)

stats = GetStatsPy()
PrintDict(stats)

DisconnectIxNet()

