#!/usr/local/python2.7.6/bin/python2.7

# This sample script will handle 2 conditions:
#
#   1: If the variable "resume" = 0, then load the config file.
#      You could reassign ports also: set reassignPorts to 1.
#   
#   2: If the variable "resume" = 1, then connect to
#      an existing configuration.
#
#   - This sample script can be applied on any testbed using 
#     different Ixia chassis and ports. All you do is set 
#     the variables accordingly.
#
#   - Users will provide a list of Traffic Item names to the variable
#     "enableTrafficItemList" to be enabled for the test.
#
#   - At the end of the script, the enabled Traffic Items will be disabled.
#

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

# Default settings
chassisIp = '10.219.117.101'
ixNetworkTclServer = '10.219.117.103'
tclServer = chassisIp
userName = 'hgee'
portList = '1/5 1/6'
port1 = '1/1/5'
port2 = '1/1/6'

# If 0, then load configFile. If 1, resume from existing config
resume = 1

# If 0, don't assign new ports. Use the saved config's ports.
# If 1, load the config and reassign ports using variable portList.
reassignPorts = 0

# To control which Traffic Item is enabled, insert the Traffic Item
# name in this list.
enableTrafficItemList = ['my ospf', 'my bgp']

configFile = '/home/hgee/Dropbox/MyIxiaWork/Temp/ospfNgpf_8.10.ixncfg'


def EnableTrafficItemByName( trafficItemNameList, condition='True' ):
    # condition: True or False

    for trafficItemName in trafficItemNameList:
        flag = 0
        for eachTrafficItem in ixNet.getList(ixNet.getRoot()+'traffic', 'trafficItem'):
            currentTrafficItemName = ixNet.getAttribute(eachTrafficItem, '-name')
            if trafficItemName == currentTrafficItemName:
                try:
                    print '\nEnableTrafficItemByName:', trafficItemName
                    ixNet.setAttribute(eachTrafficItem, '-enabled',  condition)
                    ixNet.commit()
                    flag = 1
                except Exception, errMsg:
                    print '\nEnableTrafficItemByName Error:', errMsg
                    return 1

        if flag == 0:
            print '\nEnableTrafficItemByName Error: No Traffic Item name found on configuration:', trafficItemName
            sys.exit()


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


def GetTopologyPortsNgpfPy(topologyName):
    # Gets all the ports associated with the Topology
    
    for topology in ixNet.getList(ixNet.getRoot(), 'topology'):
        currentName = ixNet.getAttribute(topology, '-name')
        if currentName is topologyName:
            topologyVports = ixNet.getAttribute(topology, '-vports')
            portList = ''
            for vport in topologyVports:
                portList.append(GetVportConnectedToPort(vport))

    if 'portList' in vars():
        return portList
    else:
        return

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
        #topologyPorts = GetTopologyPorts(currentTopologyName)
        topologyPorts = GetTopologyPortsNgpfPy(currentTopologyName)

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
                            print '\tARP is resolved'
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


def StartTrafficNgpfHlPy():
    print '\nStartTrafficNgpfHlPy'
    status = ixia_ngpf.traffic_control(action = 'run')    
    if status == 1:
        print '\nStartTrafficNgpfHlPy failed: ', status['log']
        return 1

    return status

def GetStatsNgpfHlPy(type_of_stats='flow'):
    print '\nGetStatsNgpfHlPy:', type_of_stats
    status = ixia_ngpf.traffic_stats(mode = type_of_stats)    
    if status['status'] != '1':
        print '\nGetStatsNgpfHlPy failed: ', status['log']
        sys.exit()

    PrintDict(status)
    return status


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


if resume == 1:
    # Connect to the existing configuration to resume running traffic.
    print '\nResuming existing configuration ...'
    connectStatus = ixia_ngpf.connect ( 
        ixnetwork_tcl_server = ixNetworkTclServer,
        tcl_server = tclServer,
        username = userName,
        break_locks = '1',
       ) 

if resume == 0 and reassignPorts == 0:
    # Load config file and use the saved config's ports.
    print '\nLoading config file:', configFile
    connectStatus = ixia_ngpf.connect ( 
        ixnetwork_tcl_server = ixNetworkTclServer,
        tcl_server = tclServer,
        username = userName,
        break_locks = 1,
        config_file = configFile,
        session_resume_keys = 1,
        ) 

if resume == 0 and reassignPorts == 1:
    # Load config file and reassign ports.
    print '\nLoading config file:', configFile
    print '\nUsing port list:', portList
    connectStatus = ixia_ngpf.connect ( 
        ixnetwork_tcl_server = ixNetworkTclServer,
        tcl_server = tclServer,
        device = chassisIp,
        port_list = portList,
        username = userName,
        break_locks = 1,
        config_file = configFile,
        ) 
    
PrintDict(connectStatus)
VerifyPortState()

print '\nStarting all protocols ...'
start_protocol_status = ixia_ngpf.test_control(action = 'start_all_protocols')
if start_protocol_status['status'] != '1':
    print '\nError: Failed to start all protocols.\n'
    sys.exit()

PrintDict(start_protocol_status)

VerifyAllProtocolSessionsNgpfPy()

if VerifyArpNgpfPy() != None:
    sys.exit()

#EnableTrafficItemByName( enableTrafficItemList, condition='True' )

StartTrafficNgpfHlPy()

print '\nSleep 10 seconds before verifying stats'
time.sleep(10)

trafficStats = ixia_ngpf.traffic_stats(mode = 'flow')
if trafficStats['status'] != '1':
    print '\nError: Failed to get traffic flow stats.\n'
    print trafficStats
    sys.exit()

PrintDict(trafficStats)

#EnableTrafficItemByName( enableTrafficItemList, condition='False' )

stats = GetStatsNgpfHlPy()

PrintDict(stats)
