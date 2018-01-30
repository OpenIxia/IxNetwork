#!/opt/ActivePython-2.7/bin/python

# The IxNetwork module is the file IxNetwork.py
# located in /IxNetwork_7.0_EA/PythonApi
# Users have to manually copy this file to their
# Python location because each Unix platform has
# Python installed in different locations.

import sys
import os
import re
import time

#sys.path.append('/home/hgee/Dropbox/MyIxiaWork/Python')
#import IxNetwork721
#import IxNetLowLevel
import IxNetwork

def ConnectToIxia(ixNetTclServer='', ixNetTclPort='8009', ixNetVersion=''):
    global ixNet

    ixNetConnect = ixNet.connect(ixNetTclServer, 'port', ixNetTclPort, '-version', ixNetVersion)

    print ('Verifying ixNet.connect() :'), ixNetConnect ;# ::ixNet::OK

    if ixNetConnect != '::ixNet::OK':
        print('Failed to connect to'), ixNetTclServer
        sys.exit()
    else:
        print('Successfully connected to'), ixNetTclServer


def CreateNewBlankConfig():
    print('Creating a blank configuration ...')
    ixNet.execute('newConfig')
    
def AddIxiaChassis( ixChassisIp ):
    print('Adding chassis: '), ixChassisIp
    ixChassisObj = ixNet.add(ixNet.getRoot()+'availableHardware', 'chassis', '-hostname', ixChassisIp)
    ixNet.commit()
    '''
    ixChassisObj1:  ::ixNet::OBJ-/availableHardware/chassis:L10988
    ixChassisObj2:  ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"
    '''
    ixChassisObj = ixNet.remapIds(ixChassisObj)[0]
    return ixChassisObj


def ClearPortOwnership(ixChassisObj, portList):
    # Clear port ownership
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


def CreateVPort(port):
    print 'Creating new VPort for %s' % port

    vPortObj = ixNet.add(ixNet.getRoot(), 'vport')
    ixNet.commit()
    vPortObj = ixNet.remapIds(vPortObj)[0]
    
    return vPortObj
    

def ConnectToPorts(vPortList, portList, ixChassisObj):
    for vPort, port in zip(vPortList, portList):
        cardNumber = port.split('/')[0]
        portNumber = port.split('/')[1]
        
        print 'ConnectToPort:', ixChassisObj + '/card:' + cardNumber + '/port:' + portNumber
        print '\tvPort =', vPort

        ixNet.setAttribute(vPort, \
                               '-connectedTo', ixChassisObj + '/card:' + cardNumber + '/port:' + portNumber
                           )

    print '\nRebooting ports.  Will take 40 seconds ...'
    ixNet.commit()


def VerifyPortState( stopTime = 5 ):
    global ixTopo

    for vPort in ixNet.getList(ixNet.getRoot(), 'vport'):
        port = ixTopo.getPort[vPort]

        for timer in range(0, stopTime):
            timer = timer + 1
            portState = ixNet.getAttribute(vPort, '-state')

            if portState == 'up':
                print('VerifyPortState: '), port + ' is up'
                break

            if portState != 'up':
                print 'VerifyPortState: %s is not up yet. Verifying %d/%d seconds' % (port, timer, stopTime)
                time.sleep(1)
            
            if timer == stopTime:
                print('Port can\'t come up.  Exiting test')
                ixNet.disconnect()
                sys.exit()

                
def CreateProtocolInterface(vPort, port):
    #global ixNet

    print 'Creating Protocol Interface:', port + '...'
    vPortInterfaceObj = ixNet.add(vPort, 'interface')
    
    addPortIntResult = ixNet.setMultiAttribute(vPortInterfaceObj, \
                                                   '-enabled', 'True', \
                                                   '-description', port \
                                                   )
    ixNet.commit()
    vPortInterfaceObj = ixNet.remapIds(vPortInterfaceObj)[0]
    return vPortInterfaceObj


def ProtocolIntMacAddress(protocolIntObj, macAddress):
    print '\nProtocol Interface MacAddress:', macAddress
    ixNet.setAttribute(protocolIntObj + '/ethernet', \
                           '-macAddress', macAddress \
                           )
    ixNet.commit()
    

def ProtocolIntIpv4(protocolIntObj, ipAddress, gateway):
    print '\nProtocol Interface IPv4:', ipAddress
    
    ipv4IntObj = ixNet.add(protocolIntObj, 'ipv4')
    
    ixNet.setMultiAttribute(ipv4IntObj, \
                                '-gateway', gateway, \
                                '-ip', ipAddress, \
                                '-maskWidth', '24' \
                                )
    ixNet.commit()
    ipv4IntObj = ixNet.remapIds(ipv4IntObj)[0]
    return ipv4IntObj


def CreateTrafficItem(name=          'My Traffic Item', 
                      trafficType=   'ipv4', 
                      transmitMode=  'interleaved', 
                      biDirectional= '1', 
                      routeMesh=     'oneToOne', 
                      srcDestMesh=   'oneToOne'):

    print '\nCreating Traffic Item: %s ...' % name
    
    trafficItemObj = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
    
    ixNet.setMultiAttribute(trafficItemObj, \
                                '-enabled', 'True', \
                                '-name', name, \
                                '-routeMesh', routeMesh, \
                                '-srcDestMesh', srcDestMesh, \
                                '-trafficType', trafficType, \
                                '-transmitMode', transmitMode, \
                                '-biDirectional', biDirectional, \
                                )
    ixNet.commit()
    trafficItemObj = ixNet.remapIds(trafficItemObj)[0]
    return trafficItemObj


def ConfigTracking(trafficItemObj, trackingList):
    print '\nConfiguring trackBy: %s ...' % trackingList
    
    ixNet.setAttribute(trafficItemObj + '/tracking', \
                           '-trackBy', trackingList \
                           )
    ixNet.commit()
    
    
def CreateEndPointSet(trafficItemObj='', name='Flow_Group', srcEndpoints='', destEndpoints=''):
    '''
    Each endpoint is a highlevelstream in a Traffic Item
    '''

    print '\nCreating Endpoint: %s ...' % name
    
    endpointObj = ixNet.add(trafficItemObj, 'endpointSet', \
                                '-name', name, \
                                '-sources', srcEndpoints, \
                                '-destinations', destEndpoints \
                                )
    ixNet.commit()
    endpointObj = ixNet.remapIds(endpointObj)[0]
    return endpointObj


def ConfigFlowGroup(flowGroupObj='', frameSize='128', frameRate='100'):
    print '\nConfiguring Flow Group:', flowGroupObj
    print 'Configuring frame size:', frameSize
    ixNet.setAttribute(flowGroupObj + '/frameSize', '-fixedSize', frameSize)
    
    print 'Configuring line rate: %s%s' % (frameRate, '%')
    ixNet.setAttribute(flowGroupObj + '/frameRate', '-rate', frameRate)
    
    ixNet.commit()

        
def ConfigFlowGroupFrameCount(flowGroupObj, frameCount) :
    print 'Configuring frame count:', frameCount
    result = ixNet.setMultiAttribute(flowGroupObj + '/transmissionControl', \
                                         '-frameCount', frameCount, \
                                         '-type', 'fixedFrameCount' \
                                         )
    ixNet.commit()
    

def ApplyTraffic():
    print('Applying Traffic to hardware ...')
    
    stopCounter = 10
    for startCounter in range(1,10):

        applyResult = ixNet.execute('apply', ixNet.getRoot() + 'traffic')

        print('ApplyTraffic: '), applyResult

        if applyResult != '::ixNet::OK' and startCounter < stopCounter:
            print('ApplyTraffic: Attempting to apply traffic: '), startCounter+'/'+stopCounter+' tries'
            time.sleep(1)
            continue

        if applyResult == '::ixNet::OK' and startCounter == stopCounter:
            print('ApplyTraffic Error: '), applyResult
            ixNet.disconnect()
            sys.exit()

        if applyResult == '::ixNet::OK' and startCounter < stopCounter:
            print('Successfully applied traffic to hardware')
            break


def RegenerateAllTrafficItems():
    for trafficItem in ixNet.getList(ixNet.getRoot()+'/traffic', 'trafficItem'):

        regenerateResult = ixNet.execute('generate', trafficItem)

        if regenerateResult != '::ixNet::OK':
            print('RegenerateAllTrafficItem error: '), trafficItem
            ixNet.disconnect()
            sys.exit()
        else:
            print('RegenerateAllTrafficItem: '), trafficItem


def SendArp():
    for vPort in ixNet.getList(ixNet.getRoot(), 'vport'):
        for interface in ixNet.getList(vPort, 'interface'):
            interfaceType = ixNet.getAttribute(interface, '-type')

            # Don't send arps on Unconnected Routed or GRE interfaces
            if re.search(r'default', interfaceType):
                isIntEnabled = ixNet.getAttribute(interface, '-enabled')
                if re.search(r'true', isIntEnabled, re.I):
                    print('Sent ARP on '), interface
                    ixNet.execute('sendArp', interface)
                    ixNet.execute('sendNs', interface)


def VerifyArpDiscoveries():
    '''
       - First, get a list of all the expected Gateway IP addresses for each vPort.
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

    print('Expected IP addresses to resolve ARPs:')
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
                print('Discovered arp on '), currentPort, ': ', discoveredIp, discoveredMac
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
        print('Error: Unresloved ARPs:')
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

    print('Starting traffic ...')

    for retry in range(1,10):
        retry = retry + 1

        try:
            result = ixNet.execute('start', traffic)
            if result != '::ixNet::OK':
                print('Failed to start traffic: '), result
                ixNet.disconnect()
                sys.exit()
            else:
                print('Executing startTraffic: '), result
                break

        except Exception, e:
            print('Exception error: Failed to start traffic: '), e
            print('Retrying '), retry, '/', 10
            time.sleep(1)

            if retry == 10:
                print('Can\'t start traffic. Exiting.')
                ixNet.disconnect()
                sys.exit()

    time.sleep(2)
    startCounter = 1
    stopCounter = 11

    #global CheckTrafficState

    for start in range(startCounter, stopCounter):
        start = start + 1
        trafficState = IxNetLowLevel.CheckTrafficState()
        
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
                print('StartTraffic: Current state = '), trafficState+'.'+' Waiting', start+'/'+stopCounter
                time.sleep(1)

        if start == stopCounter:
            if trafficState != 'started' or trafficState != 'startedWaitingForStats' or \
                    trafficState != 'stoppedWaitingForStats' or trafficStats != 'stopped':
                print('Failed: Traffic failed to start')
                ixNet.disconnect()
                sys.exit()
    


def Lsearch(searchList, searchWord):
    wordExists = 0
    for index in range(0, len(searchList)):
        if re.search(r'%s' % searchWord, searchList[index], re.I):
            return index
            
    if wordExists == 0:
        # Return 'None' if not found
        return


def GetKeyListDependency(searchPattern, keys):
    # print 'match:', searchPattern, keys
    # searchPattern = ('eth2', '2.2', 'AA:BB:CC:DD:EE:FF') 
    # keys          = ('eth2', '2.2.2.2', 'AA:BB:CC:DD:EE:FF')

    #i:  0 ; x:  eth2
    #i:  1 ; x:  *
    #i:  2 ; x:  AA:BB:CC:DD:EE:FF
    
    #keys[i]:  eth2
    #keys[i]:  2.2.2.2
    #keys[i]:  AA:BB:CC:DD:EE:FF
    #keys[i]:  eth1
    #keys[i]:  eth2
    #keys[i]:  3.3.3.3
    #keys[i]:  AA:BB:CC:DD:EE:FF

    # Loop through each keys looking for each pattern.
    # As soon as it doesn't match, break out.
    for i, x in enumerate(searchPattern):
        if x is not '*' and not re.search(x, keys[i]):
            return False

    return True


def GetKeyList(datas, searchPattern):
    myList = []

    for keys, values in datas.iteritems():
        # keys = ('eth1', '1.1.1.1', '11:22:33:44:55:66') ; values = machineA
        if GetKeyListDependency(searchPattern, keys):
            keyValue = keys, values
            myList.append(keyValue)
        
    return myList


def GetStatistics( getStatsBy='trafficItem' ):
    getStats = {}

    viewList = ixNet.getList(ixNet.getRoot()+'/'+'statistics', 'view')
    statViewSelection = 'Flow Statistics'
    flowStatsViewIndex = Lsearch(viewList, statViewSelection)
    if flowStatsViewIndex == None:
        print('GetStatistics error: Can\'t find \'Flow Statistics\' in viewList')
        ixNet.disconnect
        sys.exit()

    view = viewList[flowStatsViewIndex]
    ixNet.setAttribute(view, '-enabled', 'true')
    ixNet.commit()

    columnList = ixNet.getAttribute(view+'/page', '-columnCaptions')
    print columnList, '\n'
    trafficItemIndex = Lsearch(columnList, "Traffic Item")
    if trafficItemIndex == None:
        print 'Traffic Item column wasn\'t found'
        return

    startTime = 1
    stopTime = 30
    while startTime < stopTime:
        totalPages = ixNet.getAttribute(view+'/page', '-totalPages')
        if re.match(r'null', totalPages, re.I):
            print 'Getting total pages for' + view + 'is not ready.' + startTime+'/'+stopTime
            time.sleep(2)
        else:
            break

    totalFlows = 0

    for currentPage in range(1, int(totalPages)+1):
        print('currentPage: '), currentPage
        ixNet.setAttribute(view + '/page', '-currentPage', currentPage)
        ixNet.commit()
        
        whileLoopStopCounter = 0
        while ixNet.getAttribute(view + '/page', '-isReady') != 'true':
            if whileLoopCounter == 5:
                print 'ViewStats: Not ready yet. Waiting', whileLoopCounter + '/5 seconds ...'
                time.sleep(1)

            whileLoopStopCounter += 1

        pageList = ixNet.getAttribute(view + '/page', '-rowValues')
        totalFlowStatsForCurrentPage = len(pageList)
        print 'Total Flow Statistics for page %d:' % totalFlowStatsForCurrentPage

        for pageListIndex in range(0, int(totalFlowStatsForCurrentPage)):
            totalFlows += 1
            rowList = pageList[pageListIndex]

            for rowIndex in range(0, len(rowList)):
                cellList = rowList[rowIndex]
                #print cellList
                trafficItem = cellList[trafficItemIndex]
                
                flowGroupIndex = Lsearch(columnList, 'Flow Group')
                if flowGroupIndex == None:
                    flowGroup = pageListIndex
                else:
                    # Parse out 'Flow Group 0008' only
                    flowGroup = cellList[flowGroupIndex].split('-')[-1].strip()
                    
                rxPortIndex = Lsearch(columnList, 'Rx Port')
                rxPort = cellList[rxPortIndex]
                
                for column, item in zip(columnList, cellList):
                    #print column, item ;# <- Thi is a great way to pring out keyed list counter values
                    if re.match(r'VLAN:VLAN Priority', column, re.I):
                        column = 'Vlan Priority'
                        
                    if re.match(r'VLAN:VLAN-ID', column):
                        column = 'Vlan ID'
                            
                    if getStatsBy == 'trafficItem':
                        if re.match(r'Traffic Item', column) == None:
                            getStats['trafficItem','_'.join(trafficItem.split()),'flow',totalFlows,'_'.join(column.split())] = item
                            getStats['totalFlows'] = totalFlows

                    if getStatsBy == 'port':
                        if re.match(r'Rx Port', column):
                            getStats['rxPort',rxPort,'trafficItem','_'.join(trafficItem.split()),'_'.join(column.split())] = item

    return getStats


def DisconnectIxNet():
    print '\nDisconnecting IxNetwork ...'
    disconnect = ixNet.disconnect()



class SetKeys(object):
    def __init__(self):
        pass

    def CreateKeys(self, *args):
        print args
        for allKeys, theValue in args:
            for i in range(0, len(allKeys) - 1, 2):
                # Join in-between spaces with an underscore
                setattr(self, '_'.join(allKeys[i].split()), allKeys[i + 1])

                if i is (len(allKeys) / 2):
                    #print i, '_'.join(allKeys[-1].split()), theValue
                    setattr(self, '_'.join(allKeys[-1].split()), theValue)
                    #print 'Self: ', self.allKeys[-1]


if __name__ == "__main__":
    ixNet  = IxNetwork.IxNet()

    class IxTopoNamespace: pass
    ixTopo = IxTopoNamespace()
    ixTopo.ixNetTclServer = '10.205.4.160'
    ixTopo.ixChassisIp = '10.205.4.155'
    ixTopo.ixNetTclPort = '8009'
    ixTopo.ixNetVersion = '7.22'
    ixTopo.cfgFile = 'mySavedConfig.ixncfg'

    ConnectToIxia(ixNetTclServer=ixTopo.ixNetTclServer, ixNetVersion=ixTopo.ixNetVersion)
    
    # ixNet exec saveConfig [ixNet writeTo $ixNetworkCfgFile -overwrite]
    ixNet.execute('saveConfig', ixNet.writeTo('mySavedConfig.ixncfg', '-overwrite'))
