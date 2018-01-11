#!/usr/local/python2.7.6/bin/python2.7

# 2 Conditions in this script:
#   
# 1: Load a saved config file.
# 2: Load a config file and use the specified Ixia chassis 
#    and Ixia ports.

import sys, os
import time, re

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError

ixia_tcl = IxiaTcl()
ixia_hlt = IxiaHlt(ixia_tcl)
ixia_ngpf = IxiaNgpf(ixia_hlt)
ixNet = ixia_ngpf.ixnet ;# For low level Python API commands

chassis_ip = '10.219.117.101'
ixnetwork_tcl_server = '10.219.117.103'
tcl_server = chassis_ip
user_name = 'hgee'
port_list = '1/1 1/2'
port_1 = '1/1/1'
port_2 = '1/1/2'

configFile = '/home/hgee/Dropbox/MyIxiaWork/Temp/ospfNgpf_8.10.ixncfg'

def VerifyPortState( stopTime = 40 ):
    for vPort in ixNet.getList(ixNet.getRoot(), 'vport'):
        # [u'::ixNet::OBJ-', u'availableHardware', u'chassis:"10.219.117.101"', u'card:1', u'port:1']
        connectedTo = ixNet.getAttribute(vPort, '-connectedTo')
        card = connectedTo.split('/')[3].split(':')[1]
        portNum = connectedTo.split('/')[4].split(':')[1]
        port = card+'/'+portNum

        for timer in range(0, stopTime):
            timer = timer + 1
            portState = ixNet.getAttribute(vPort, '-state')

            if portState == 'up':
                print 'VerifyPortState: ', port + ' is up'
                break

            if portState != 'up':
                print 'VerifyPortState: %s is not up yet. Verifying %d/%d seconds' % (port, timer, stopTime)
                time.sleep(1)
            
            if timer == stopTime:
                print 'Port can\'t come up.  Exiting test'
                return 1

    return 0


def VerifyAllProtocolSessionsNgpfPy():
    # This API will loop through each created Topology Group and verify
    # all the created protocols for session up for up to 90 seconds total.
    # 
    # Returns 0 if all sessions are UP.
    # Returns 1 if any session remains DOWN after 90 seconds.

    protocolList = ['ancp',
                    'bfdv4Interface',
                    'bgpIpv4Peer',
                    'dhcpv4relayAgent',
                    'dhcpv4server',
                    'geneve',
                    'greoipv4',
                    'igmpHost',
                    'igmpQuerier',
                    'lac',
                    'ldpBasicRouter',
                    'ldpConnectedInterface',
                    'ldpTargetedRouter',
                    'lns',
                    'openFlowController',
                    'openFlowSwitch',
                    'ospfv2',
                    'ovsdbcontroller',
                    'ovsdbserver',
                    'pcc',
                    'pce',
                    'pcepBackupPCEs',
                    'pimV4Interface',
                    'ptp',
                    'rsvpteIf',
                    'rsvpteLsps',
                    'tag',
                    'vxlan'
                ]

    sessionDownList = ['down', 'notStarted']
    startCounter = 1
    timeEnd = 120
    import time

    for protocol in protocolList:
        for topology in ixNet.getList(ixNet.getRoot(), 'topology'):
            for deviceGroup in ixNet.getList(topology, 'deviceGroup'):
                for ethernet in ixNet.getList(deviceGroup, 'ethernet'):
                    for ipv4 in ixNet.getList(ethernet, 'ipv4'):                        
                        for currentProtocol in ixNet.getList(ipv4, protocol):
                            for timer in range(startCounter, timeEnd+1):
                                currentStatus = ixNet.getAttribute(currentProtocol, '-sessionStatus')
                                print '\n%s' % currentProtocol
                                print '\tTotal sessions: %d' % len(currentStatus)
                                totalDownSessions = 0
                                for eachStatus in currentStatus:
                                    if eachStatus != 'up':
                                        totalDownSessions += 1
                                print '\tTotal sessions Down: %d' % totalDownSessions

                                if timer < timeEnd and [element for element in sessionDownList if element in currentStatus] == []:
                                    print '\tProtocol sessions are all up'
                                    startCounter = timer
                                    break
                                if timer < timeEnd and [element for element in sessionDownList if element in currentStatus] != []:
                                    print '\tWaiting %d/%d seconds' % (timer, timeEnd)
                                    time.sleep(1)
                                    continue
                                if timer == timeEnd and [element for element in sessionDownList if element in currentStatus] != []:
                                    print '\tProtocol session failed to come up:'
                                    return 1
    return 0


def VerifyArpNgpfPy(ipType='ipv4', maxRetry=3):
    unresolvedArpList = []
    for topology in ixNet.getList(ixNet.getRoot(), 'topology'):
        currentTopologyName = ixNet.getAttribute(topology, '-name')
        topologyPorts = GetTopologyPorts(currentTopologyName)

        for deviceGroup in ixNet.getList(topology, 'deviceGroup'):
            if ixNet.getAttribute(deviceGroup, '-status') == 'started':
                for ethernet in ixNet.getList(deviceGroup, 'ethernet'):
                    for ipv4 in ixNet.getList(ethernet, ipType):
                        print '\nProtocol is started on:', ipv4
                        flag = 0
                        sessionStatus = ixNet.getAttribute(ipv4, '-sessionStatus')
                        resolvedGatewayMac = ixNet.getAttribute(ipv4, '-resolvedGatewayMac')

                        # Only care for unresolved ARPs
                        for index in xrange(0, len(resolvedGatewayMac)):
                            for timer in xrange(1, maxRetry+1):
                                if (re.match('.*Unresolved', resolvedGatewayMac[index]) and 
                                    sessionStatus[index] != 'notStarted' and
                                    timer <= maxRetry
                                    ):
                                    # Gettting in here means the interface should be up
                                    multiValueNumber = ixNet.getAttribute(ipv4, '-address')
                                    ipAddrNotResolved = ixNet.getAttribute(ixNet.getRoot()+multiValueNumber, '-values')[index]
                                    # /topology:2/deviceGroup:1/ethernet:1/ipv4:1 -address
                                    topologyDeviceGroupSource = ixNet.getAttribute(ixNet.getRoot()+multiValueNumber, '-source')
                                    
                                    match = re.match('.*(topology:[0-9]+)/deviceGroup:([0-9]+).*', topologyDeviceGroupSource)
                                    if match:
                                        topologyNum = match.group(1)
                                        deviceGroupNum = match.group(2)
                                        vport = ixNet.getAttribute(ixNet.getRoot()+topologyNum, '-vports')
                                        for eachVport in vport:
                                            realPortNumber = GetVportConnectedToPort(eachVport)
                                            print '\n%s %s %s did not resolve ARP yet. Verify %s/%s ...' % (
                                                topologyNum, realPortNumber, ipAddrNotResolved, timer, maxRetry
                                            )
                                        time.sleep(1)

                                if (re.match('.*Unresolved', resolvedGatewayMac[index]) and 
                                    sessionStatus[index] != 'notStarted' and
                                    timer == maxRetry
                                    ):
                                    print '\t%s %s %s cannot resolve ARP after %s/%s retries' % (
                                        topologyNum, realPortNumber, ipAddrNotResolved, timer, maxRetry)
                                    unresolvedArpList.append('%s Port:%s IP:%s' % (topologyNum, realPortNumber, ipAddrNotResolved))
                                    flag = 1

                        if flag is 0:
                            print '\tARP passed'
            else:
                print '\n\tVerifyArpNgpf. Protocol not started on:\n\t\t%s' % deviceGroup

    if unresolvedArpList is None:
        return 0

    if unresolvedArpList:
        print '\n'
        for unresolvedArp in unresolvedArpList:
            print 'UnresolvedArps:', unresolvedArp

        print '\n'
        return unresolvedArpList



def VerifyProtocolSessionStatusUpNgpfHlPy(protocolHandle, totalTime=60):
    '''
    Pass in a protocol handle to verify for sessions status 'UP'.
    
    '''

    for timer in range(0, totalTime):
        sessionStatus = ixia_ngpf.protocol_info(
            handle = protocolHandle,
            mode = 'aggregate'
            )

        currentSessionUp = sessionStatus[protocolHandle]['aggregate']['sessions_up']
        totalSessions = sessionStatus[protocolHandle]['aggregate']['sessions_total']

        print '\nVerifying protocol sessions', protocolHandle
        print '\t%s/%s: CurrentSessionUp:%s   TotalSessions:%s\n' % (timer, totalTime, currentSessionUp, totalSessions)

        if timer < totalTime and currentSessionUp != totalSessions:
            time.sleep(1)
            continue
        
        if timer < totalTime and currentSessionUp == totalSessions:
            return 0

        if timer == totalTime and currentSessionUp != totalSessions:
            print '\nError: It has been %s seconds and total sessions are not all UP. ' % timer
            return 1

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


if os.path.isfile(configFile) == False:
    sys.exit('\nError: Config file does not exists: %s' % configFile)

# Load Config File
'''
connect_result = ixia_ngpf.connect ( 
    reset = '1',
    ixnetwork_tcl_server = ixnetwork_tcl_server,
    tcl_server = tcl_server,
    username = user_name,
    break_locks = 1,
    configFile = configFile,
    ) 
'''

# Load config file and specifying which Ixia chassis and ports to use.
connect_result = ixia_ngpf.connect ( 
    ixnetwork_tcl_server = ixnetwork_tcl_server,
    tcl_server = tcl_server,
    device = chassis_ip,
    port_list = port_list,
    username = user_name,
    break_locks = 1,
    config_file = configFile,
    ) 

PrintDict(connect_result)

if VerifyPortState():
    sys.exit()

print '\nStarting all protocols ...'
startProtocolStatus = ixia_ngpf.test_control(action = 'start_all_protocols')
if startProtocolStatus['status'] != '1':
    print '\nError: Failed to start all protocols.\n'
    sys.exit()

VerifyAllProtocolSessionsNgpfPy()

trafficControlStatus = ixia_ngpf.traffic_control(action = 'run')
if trafficControlStatus['status'] != '1':
    print '\nError: Failed to start traffic.\n'
    sys.exit()

PrintDict(trafficControlStatus)

time.sleep(10)

trafficStats = ixia_ngpf.traffic_stats(mode='flow')
if trafficStats['status'] != '1':
    print '\nError: Failed to get traffic flow stats.\n'
    print trafficStats
    sys.exit()

#PrintDict(trafficStats)

print '\n--- RX:', trafficStats['flow']['1']['rx']['total_pkts']
sys.exit()
