#from runJobApi import logInfo, logError
import sys
import re
import time

# Python global names cannot be shared across modules.
# Stuffing all the ngpf modules and objects in SharedIxiaNgpf.py
# so any module and scripts can use it simultaneously.
#from SharedIxiaNgpf import *

#from ixiatcl import IxiaTcl
#from ixiahlt import IxiaHlt
#from ixiangpf import IxiaNgpf
#from ixiaerror import IxiaError

#ixia_tcl = IxiaTcl()
#ixia_hlt = IxiaHlt(ixia_tcl)
#ixia_ngpf = IxiaNgpf(ixia_hlt)
#ixNet = ixia_ngpf.ixnet ;# For low level Python API commands

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


def ShowKwargs(**kwargs):
    for key,value in kwargs.iteritems():
        print '\t%s: %s' % (key,value)
    print '\n'


def ConnectHlPy(device='', reset=1, port_list='', 
               ixnetwork_tcl_server='', tcl_server='', 
                username='unknown'):

    print 'ConnectHlPy: Chassis:%s IxNetTclServer=%s' % (device, ixnetwork_tcl_server)
    connect_status = ixia_ngpf.connect(
        reset = reset,
        device = device,
        port_list = port_list,
        ixnetwork_tcl_server = ixnetwork_tcl_server,
        tcl_server = tcl_server,
        username = username
        )
    
    PrintDict(connect_status)
    
    if connect_status['status'] != '1':
        return 1
    else:
        return connect_status


def ConnectAndResumeNgpfHlPy(ixNetworkTclServer, tclServer,
                             userName
                             ):
    '''
    Connect to an existing configuration and use the configured ports.
    This API will return all configuration handles.
    '''

    connectStatus = ixia_ngpf.connect ( 
        ixnetwork_tcl_server = ixNetworkTclServer,
        tcl_server = tclServer,
        username = userName,
        session_resume_keys = '1',
        break_locks = '1',
        ) 
    if connectStatus['status'] != '1':
        return 1
    else:
        return connectStatus


def ConnectAndResumeReassignPortsNgpfHlPy(ixNetworkTclServer, tclServer,
                             userName, portList, chassisIp
                             ):
    '''
    Connect to an existing configuration and use the provided list of portList.
    portList format: 1/3. Not 1/1/3.
    This API will return all session configuration handles.
    '''

    connectStatus = ixia_ngpf.connect ( 
        ixnetwork_tcl_server = ixNetworkTclServer,
        tcl_server = tclServer,
        username = userName,
        port_list = portList,
        device = chassisIp,
        session_resume_keys = '1',
        break_locks = '1',
        ) 
    if connectStatus['status'] != '1':
        return 1
    else:
        return connectStatus


def LoadConfigFileNgpfHlPy(configFile, ixNetworkTclServer,
                           tclServer, userName):
    '''
    Load a saved configuration file with assigned ports.
    This will return all configuration handles.
    '''

    connectStatus = ixia_ngpf.connect ( 
        config_file = configFile,
        reset = '1',
        ixnetwork_tcl_server = ixNetworkTclServer,
        tcl_server = tclServer,
        username = userName,
        session_resume_keys = '1',
        break_locks = '1',
        ) 
    if connectStatus['status'] != '1':
        return 1
    else:
        return connectStatus
    

def LoadConfigFileReassignPortsNgpfHlPy(configFile, ixNetworkTclServer, tclServer,
                                chassisIp, portList, userName
                                ):
    '''
    Load a saved configuration file and reassign ports.
    The benefit of this API is that you could apply the same configuration 
    in any testbed, and use different Ixia ports.
    
    configFile: The full path to the config file on your Linux network
    portList format:  1/3. Not 1/1/3
    '''

    connectStatus = ixia_ngpf.connect ( 
        config_file = configFile,
        ixnetwork_tcl_server = ixNetworkTclServer,
        tcl_server = tclServer,
        device = chassisIp,
        port_list = portList,
        username = userName,
        break_locks = '1',
        ) 
    if connectStatus['status'] != '1':
        return 1
    else:
        return connectStatus


def Disconnect_IxNet():
    print '\nDisconect_IxNet'
    disconnect = ixNet.disconnect()


def VerifyPortState( stopTime = 40 ):
    # Search for all the created vports and get its state.

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

def GetVportMapping( port ):
    # Search all vport for the port number.
    # Port format = 1/1.  Not 1/1/1.

    vportList = ixNet.getList(ixNet.getRoot(), 'vport')

    for vport in vportList:
        # ::ixNet::OBJ-/availableHardware/chassis:"10.219.117.101"/card:1/port:5
        connectedTo = ixNet.getAttribute(vport, '-connectedTo')
        card    = connectedTo.split('/')[3].split(':')[-1]
        portNum = connectedTo.split('/')[4].split(':')[-1]
        portNumber = card +'/' + portNum

        if portNumber == port:
            return vport

def CleanUpNgpfHlPy():
    status = ixiangpf.cleanup_session(reset='1')
    if status['status'] != IxiaHlt.SUCCESS:
        print '\nCleanUp: Failed:', status['log']

def DisconnectHlPy():
    print '\nDisconnectHlPy'
    ixia_ngpf.cleanup_session(reset='0')

def AddIxiaChassisPy( ixChassisIp ):
    print '\nAdding chassis: ', ixChassisIp
    ixChassisObj = ixNet.add(ixNet.getRoot()+'availableHardware', 'chassis', '-hostname', ixChassisIp)
    ixNet.commit()

    #::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"
    ixChassisObj = ixNet.remapIds(ixChassisObj)[0]
    return ixChassisObj

def RemoveIxiaChassisPy( ixChassisIp ):
    availableHardware = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    chassisList = ixNet.getList(availableHardware, 'chassis')
    for eachIxChassis in chassisList:
        currentChassisIp = ixNet.getAttribute(eachIxChassis, '-ip')
        if currentChassisIp == ixChassisIp:
            print '\nRemoveIxiaChassis: ', eachIxChassis
            ixNet.remove(eachIxChassis)
            ixNet.commit()

def ReleaseAllPortsPy(ixNet):
    print '\nReleaseAllPortsPy'
    ixNet.execute('releaseAllPorts')

def CreateTopologyPy(topologyName, vPorts):
    print '\nCreateTopology: %s : %s' % (topologyName, vPorts)
    topologyObj = ixNet.add(ixNet.getRoot(), 'topology')
    ixNet.setMultiAttribute(topologyObj,
                            '-name', topologyName,
                            '-vports', vPorts
                        )
    ixNet.commit()
    return topologyObj
    
def CreateTopologyNgpfHlPy(topology_name='Topology', ports=''):
    ''' port_handle format = 12/1 '''

    print '\nCreateTopologyNgpfHlPy'
    status = ixia_ngpf.topology_config(
        topology_name = topology_name,
        port_handle = ports
        )
    
    if status['status'] != '1':
        return 1

    # /topology:1
    topology_handle = status['topology_handle']
    return topology_handle
        
def CreateDeviceGroupPy(topologyObj, deviceGroupName, multiplier):
    print '\nCreateDeviceGroup: %s : %s' % (topologyObj, deviceGroupName)
    deviceGroupObj = ixNet.add(topologyObj, 'deviceGroup')
    ixNet.setMultiAttribute(deviceGroupObj,
                            '-name', deviceGroupName,
                            '-multiplier', multiplier
                        )
    ixNet.commit()
    return deviceGroupObj
        
def CreateDeviceGroupNgpfHlPy(topology_handle='',
                              device_group_name='',
                              multiplier=1,
                              enabled=1
                              ):

    print '\nCreateDeviceGroupNgpfHlPy'
    status = ixia_ngpf.topology_config(
        topology_handle = topology_handle,
        device_group_name = device_group_name,
        device_group_multiplier = multiplier,
        device_group_enabled = enabled
        )
    
    if status['status'] != '1':
        return 1
        
    # /topology:1/deviceGroup:1
    device_group_handle = status['device_group_handle']
    return device_group_handle


def ConfigPortHlPy(mode='config', 
                   port_handle='', 
                   phy_mode='copper', 
                   speed='ether1000',
                   autonegotiation='1', 
                   duplex='full', 
                   intf_mode='ethernet'):
    
    print '\nConfigPortHlPy:', port_handle, phy_mode
    status = ixia_hlt.interface_config(mode=mode,
                                       port_handle=port_handle,
                                       phy_mode=phy_mode,
                                       speed=speed,
                                       autonegotiation=autonegotiation,
                                       duplex=duplex,
                                       intf_mode=intf_mode
                                       )
    
    if status['status'] != '1':
        print '\nConfig_Port failed: %s\n' % status['log']
        sys.exit()
        

def ConfigProtocolInterfaceNgpfHlPy(**kwargs):
    """ Usage:

     PortConfigProtocolIntNgpf(
        mode = 'config',
        protocol_handle = device_group_1_handle,
        mtu = '1500',
        src_mac_addr = '00:01:01:01:00:01',
        src_mac_addr_step = '00:00:00:00:00:01',
        intf_ip_addr = '1.1.1.1',
        intf_ip_addr_step = '0.0.0.1',
        netmask = '255.255.255.0',
        gateway = '1.1.1.4',
        gateway_step = '0.0.0.0',
        arp_send_req = '1',
        arp_req_retries = '3',
        ipv4_resolve_gateway = '1',
        vlan = '0',
        vlan_id = '101',
        vlan_id_step = '1',
        vlan_id_count = '1',
        vlan_user_priority = '0',
        vlan_user_priority_step = '0'
        )
    """

    print '\nConfigProtocolInterfaceNgpfHlPy:'
    ShowKwargs(**kwargs)

    status = ixia_ngpf.interface_config(**kwargs)
    if status['status'] != '1':
        return 1

    '''
    status: 1
    ethernet_handle: /topology:1/deviceGroup:1/ethernet:1
    ipv4_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1
    interface_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:1
                      /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:2
                      /topology:1/deviceGroup:1/ethernet:1/ipv4:1/item:3
                      /topology:1/deviceGroup:1/ethernet:1/item:1
                      /topology:1/deviceGroup:1/ethernet:1/item:2
                      /topology:1/deviceGroup:1/ethernet:1/item:3
    '''
    return status


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

def ConfigTrafficItemNgpfHlPy(**kwargs):
    """ Usage:
    
    CreateTrafficItem(
    mode = 'create',
    name = 'Traffic_Item_1',
    emulation_src_handle = topology_1_handle,
    emulation_dst_handle = topology_2_handle,
    transmit_mode = 'continuous',
    pkts_per_burst = '50000',
    frame_size = '256',
    rate_percent = '100',
    src_dest_mesh = 'one_to_one',
    route_mesh = 'one_to_one',
    bidirectional = '0',
    allow_self_destined = '0',
    circuit_endpoint_type = 'ipv4',
    track_by = 'flowGroup0 sourceDestValuePair0',
    l3_protocol = 'ipv4'
    )
    """
    print '\nConfigTrafficItemNgpfHlPy:'
    ShowKwargs(**kwargs)
    
    status = ixia_ngpf.traffic_config(**kwargs)
     
    if status['status'] != '1':
        return 1
         
    '''
    status: 1
    stream_id: TI0-Traffic_Item_1
    log: 
    ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1:
    
    headers: ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ethernet-1"
             ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ipv4-2"
             ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"fcs-3"
    ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1:
    
    headers: ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"ethernet-1"
             ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"ipv4-2"
             ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1/stack:"fcs-3"
    
    encapsulation_name: Ethernet.IPv4
    endpoint_set_id: 1
    stream_ids: ::ixNet::OBJ-/traffic/trafficItem:1/highLevelStream:1
    traffic_item: ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1
    '''
    
    return status


def ConfigIpv4SingleBurstTrafficNgpfHlPy(name='Traffic_Item_1', 
                                     rate_percent='100', 
                                     pkt_per_burst='100000', 
                                     bidirectional='0', src_endpoint='', 
                                     dst_endpoint='',
                                     track_by='sourceDestValuePair0'):
    
    status = ixia_ngpf.traffic_config(mode = 'create',
                                      name = name,
                                      emulation_src_handle = src_endpoint,
                                      emulation_dst_handle = dst_endpoint,
                                      transmit_mode = 'single_burst',
                                      pkts_per_burst = pkt_per_burst,
                                      rate_percent = rate_percent,
                                      frame_size = '85',
                                      src_dest_mesh = 'one_to_one',
                                      route_mesh = 'one_to_one',
                                      bidirectional = bidirectional,
                                      allow_self_destined = '0',
                                      circuit_endpoint_type = 'ipv4',
                                      track_by = track_by,
                                      l3_protocol = 'ipv4')
    
    if status['status'] != '1':
        print '\nTraffic_Ipv4SingleBurst failed:', status['log']
        sys.exit()
        
    print '\nTraffic_Ipv4SingleBurst: Successfully created.'
    PrintDict(status)
        

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

    
def ApplyTrafficPy():
    print "\nApplyTrafficPy ..."
    traffic = ixNet.getRoot()+'/traffic'
    status = ixNet.execute('apply', traffic)
    
def ApplyChangesOnTheFly(timeout=90):
    count = 0
    status = ixNet.getAttribute('/globals/topology', '-applyOnTheFlyState')
    print 'Aplying changes on the fly:', status
    while status == "notAllowed":
        print "      {count}: /globals/topology -applyOnTheFlyState --> {status}".format(count=count, status=status)
        status = ixNet.getAttribute('/globals/topology', '-applyOnTheFlyState')
        time.sleep(1)
        count += 1
        if count > timeout:
            print "Waited for {count}".format(count=count)

    status = ixNet.getAttribute('/globals/topology', '-applyOnTheFlyState')
    if status == "allowed":
        ixNet.execute('applyOnTheFly', '/globals/topology')
        return 0
    elif status == "nothingToApply":
        ixNet.execute('applyOnTheFly', '/globals/topology')
        return 0
    else:
        print "Status unknown '$status'"
        return 1

def StartAllProtocolsPy():
    print '\nStartAllProtocolsPy'
    ixNet.execute('startAllProtocols')
    ixNet.commit()
    time.sleep(2)

def StopAllProtocolsPy():
    print '\nStopAllProtocolsPy'
    ixNet.execute('stopAllProtocols')
    ixNet.commit()
    time.sleep(2)

def StartAllProtocolsNgpfHlPy():
    print '\nStartAllProtocolsNgpfHlPy'
    status = ixia_ngpf.test_control(action = 'start_all_protocols')    
    if status['status'] != '1':
        print '\nStartAllProtocolsNgpfHlPy failed:', status['log']
        return 1

    time.sleep(5)
    return status


def StopAllProtocolsNgpfHlPy():
    print '\nStopAllProtocolsNgpfHlPy'
    status = ixia_ngpf.test_control(action = 'stop_all_protocols')    
    if status['status'] != '1':
        print '\nStopAllProtocolsNgpfHlPy failed:', status['log']
        return 1

    return status


def VerifyProtocolSessionStatusUpNgpfHlPy(protocolHandleList, totalTime=60):
    '''
    protocolHandleList: One or more protocol handles in a list
                        to verify for sessions status 'UP'.
    
    Protocol handle example:
                     /topology:1/deviceGroup:1/ethernet:1/ipv4:1
                     /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1
    '''
    errorFlag = 0

    for eachProtocolSessionToVerify in protocolHandleList:
        for timer in range(1, totalTime+1):
            sessionStatus = ixia_ngpf.protocol_info(
                handle = eachProtocolSessionToVerify,
                mode = 'aggregate'
                )

            currentSessionUp = sessionStatus[eachProtocolSessionToVerify]['aggregate']['sessions_up']
            totalSessions = sessionStatus[eachProtocolSessionToVerify]['aggregate']['sessions_total']

            print '\nVerifying protocol sessions', eachProtocolSessionToVerify
            print '\t%s/%s: CurrentSessionUp:%s   TotalSessions:%s\n' % (timer, totalTime, currentSessionUp, totalSessions)

            if timer < totalTime and currentSessionUp != totalSessions:
                time.sleep(1)
                continue

            if timer < totalTime and currentSessionUp == totalSessions:
                break

            if timer == totalTime and currentSessionUp != totalSessions:
                print '\nError: It has been %s seconds and total sessions are not all UP. ' % timer
                errorFlag = 1

    if errorFlag:
        sys.exit()

def StartTrafficNgpfHlPy():
    print '\nStartTrafficNgpfHlPy'
    status = ixia_ngpf.traffic_control(action = 'run')    
    if status == 1:
        print '\nStartTrafficNgpfHlPy failed: ', status['log']
        return 1

    return status


def StopTrafficNgpfHlPy():
    print '\nStopTrafficNgpfHlPy'
    status = ixia_ngpf.traffic_control(
        action='stop',
        max_wait_timer=60
        )
    PrintDict(status)
    if status['status'] != '1':
        return 1

    VerifyTrafficState()
    return 0

def StopTrafficByTrafficItemNamePy(tiList=None):
    # Stop traffic by the Traffic Item name.
    # Usage: tiList = A list of Traffic Item names to stop.
    # Requires APIs: StopTrafficPy and VerifyTrafficStatePy
    if tiList:
        for item in ixNet.getList(ixNet.getRoot()+'traffic', 'trafficItem'):
            currentTrafficItemName = ixNet.getAttribute(item, '-name')
            if currentTrafficItemName in tiList:
                print '\nStopTraffic:', currentTrafficItemName
                ixNet.execute('stopStatelessTraffic', item)

def CheckTrafficStatePy():
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


def VerifyTrafficStatePy():
    # Returns 1 if traffic failed to start
    startCounter = 1
    stopCounter = 16

    for start in xrange(startCounter, stopCounter):
        trafficState = CheckTrafficState()
        if start == stopCounter:
            if trafficState not in ['started', 'startedWaitingForStats', 'stoppedWaitingForStats', 'stopped']:
                print '\nVerifyTrafficState Error: Traffic failed to start'
                return 1

        if trafficState is 'started':
            print '\nVerifyTrafficState: Traffic started'
            break

        if trafficState is 'stopped':
            print '\nVerifyTrafficState: Traffic stopped'
            break

        if trafficState in ['startedWaitingForStats', 'stoppedWaitingForStats']:
            print '\nVerifyTrafficState: Traffic started. Waiting for stats to complete'
            break

        if start < stopCounter:
            if trafficState not in ['started', 'startedWaitingForStats', 'stoppedWaitingForStats', 'stopped']:
                print '\nVerifyTrafficState: Current state = %s. Waiting %s/%s' % (trafficState, start, stopCounter)
                time.sleep(1)


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

def GetStatsNgpfHlPy(type_of_stats='flow'):
    print '\nGetStatsNgpfHlPy:', type_of_stats
    status = ixia_ngpf.traffic_stats(mode = type_of_stats)    
    if status['status'] != '1':
        print '\nGetStatsNgpfHlPy failed: ', status['log']
        sys.exit()

    PrintDict(status)
    return status


def RegenerateAllTrafficItemsPy():
    for trafficItem in ixNet.getList(ixNet.getRoot()+'/traffic', 'trafficItem'):
        result = ixNet.execute('generate', trafficItem)
        
        if result != '::ixNet::OK':
            print '\nRegenerate_All_TrafficItems failed: ', trafficItem
            ixNet.disconnect()
            sys.exit()
        else:
            print '\nRegenerate_All_TrafficItems:', trafficItem


def GetTopologyGroupHandleNgpfPy( topologyGroupNumber='1' ):
    for topologyHandle in ixNet.getList(ixNet.getRoot(), 'topology'):
        match = re.match(r'::ixNet::OBJ-/topology:%s' % topologyGroupNumber, topologyHandle)
        if match:
            return topologyHandle

    return 0

def GetDeviceGroupHandleNgpfPy( deviceGroupNumber='1' ):
    for topologyHandle in ixNet.getList(ixNet.getRoot(), 'topology'):
        for deviceGroupHandle in ixNet.getList(topologyHandle, 'deviceGroup'):
            match = re.match(r'::ixNet::OBJ-/topology:[0-9]+/deviceGroup:%s' % deviceGroupNumber, deviceGroupHandle)
            if match:
                return deviceGroupHandle

    return 0


def ModifyTopologyNameNgpfPy( topologyHandle, topologyName ):
    # topologyHandle example:ixNet::OBJ-/topology:1
    
    print '\nModifyTopologyName: %s : %s' % (topologyHandle, topologyName)
    ixNet.setAttribute(topologyHandle, '-name', topologyName)
    ixNet.commit()

def ModifyDeviceGroupNamePy( deviceGroupHandle, deviceGroupName):
    # deviceGroupHandle example: ::ixNet::OBJ-/topology:1/deviceGroup:1

    print '\nModifyDeviceGroupName: %s : %s' % (deviceGroupHandle, deviceGroupName)
    ixNet.setAttribute(deviceGroupHandle, '-name', deviceGroupName)
    ixNet.commit()

def ConfigIgmpEmulationNgpfHlPy( **kwargs ):
    print '\nConfigIgmpEmulationNgpfHlPy:'
    for key, value in kwargs.iteritems():
        print '\t%s: %s' % (key,value)

    status = ixia_ngpf.emulation_igmp_config(**kwargs)

    if status['status'] != '1':
        print '\nConfigIgmpEmulationNgpfHlPy failed: %s\n' % status['log']
        sys.exit()

    PrintDict(status)
    return status


def ConfigIgmpMulticastGroupNgpfHlPy( **kwargs ):
    print '\nConfigIgmpMulticastGroupNgpfHlPy:'
    for key,value in kwargs.iteritems():
        print '\t%s: %s' % (key,value)

    status = ixia_ngpf.emulation_multicast_group_config(**kwargs)
    if status['status'] != '1':
        print '\nConfigIgmpGroupNgpfPy failed: %s\n' % status['log']
        sys.exit()

    PrintDict(status)
    return status


def ConfigIgmpSourceGroupNgpfHlPy( **kwargs ):
    print '\nConfigIgmpSourceGroupNgpfHlPy:'
    for key,value in kwargs.iteritems():
        print '\t%s: %s' % (key,value)

    status = ixia_ngpf.emulation_multicast_source_config(**kwargs)
    if status['status'] != '1':
        print '\nConfigIgmpSourceGroupNgpfHlPy failed: %s\n' % status['log']
        sys.exit()

    PrintDict(status)
    #return status['multicast_source_handle']
    return status


def ConfigIgmpGroupNgpfHlPy( **kwargs ):
    print '\nConfigIgmpGroupNgpfHlPy:'
    for key,value in kwargs.iteritems():
        print '\t%s: %s' % (key,value)

    status = ixia_ngpf.emulation_igmp_group_config(**kwargs)
    if status['status'] != '1':
        print '\nConfigIgmpGroupNgpfHlPy failed: %s\n' % status['log']
        sys.exit()

    PrintDict(status)
    return status


def ConfigIgmpQuerierNgpfHlPy( **kwargs ):
    print '\nConfigIgmpQuerierNgpfHlPy:'
    for key,value in kwargs.iteritems():
        print '\t%s: %s' % (key,value)

    status = ixia_ngpf.emulation_igmp_querier_config(**kwargs)
    if status['status'] != '1':
        print '\nConfigIgmpQuerierNgpfHlPy failed: %s\n' % status['log']
        sys.exit()

    # igmpQuerierStatus:: status: 1
    # igmp_querier_handle: /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1
    # igmp_querier_handles: /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:1 
    #                       /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:2 
    #                       /topology:2/deviceGroup:1/ethernet:1/ipv4:1/igmpQuerier:1/item:3
        
    PrintDict(status)
    return status


def ConfigVxlanEmulationNgpfHlPy(get_handle='yes', **kwargs):
    # get_handle = Defaults to yes.
    # 
    # The reason there is get_handle is because this
    # API has two usage.
    #    1> VxLAN emulation
    #    2> VxLAN global settings.
    # Configuring VxLAN global settings won't have a 
    # handle to return.

    print '\nConfigVxlanEmulationNgpfHlPy:'
    for key,value in kwargs.iteritems():
        print '\t%s: %s' % (key,value)

    status = ixia_ngpf.emulation_vxlan_config(**kwargs)
    if status['status'] != '1':
        print '\nonfigVxlanEmulationNgpfHlPy failed: %s\n' % status['log']
        sys.exit()

    PrintDict(status)
    if get_handle == 'yes':
        # status: 1
        # ethernet_handle: /topology:1/deviceGroup:1/ethernet:1
        # handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/vxlan:1/item:1 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/vxlan:1/item:2 /topology:1/deviceGroup:1/ethernet:1/ipv4:1/vxlan:1/item:3
        # ipv4_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1
        # vxlan_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/vxlan:1
        # vxlan_static_info: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/vxlan:1/vxlanStaticInfo
        # dg_handle: /topology:1/deviceGroup:1
        return status


def ModifyBgpNumberOfRoutesNgpf( networkGroupName='', totalRoutes='' ):
    for topology in ixNet.getList(ixNet.getRoot(), 'topology'):
        for deviceGroup in ixNet.getList(topology, 'deviceGroup'):
            for networkGroup in ixNet.getList(deviceGroup, 'networkGroup'):
                currentNetworkGroupName = ixNet.getAttribute(networkGroup, '-name')
                nameMatch = re.search(r'%s' % networkGroupName, currentNetworkGroupName, re.IGNORECASE)
                if nameMatch:
                    for ipv4PrefixPool in ixNet.getList(networkGroup, 'ipv4PrefixPools'):
                        print '\nModifyBgpNumberOfRoutesNgpf: %s : totalRoutes:%s' % (ipv4PrefixPool, totalRoutes)
                        ixNet.setAttribute(ipv4PrefixPool, '-numberOfAddresses', totalRoutes)
                        ixNet.commit()
                        return

    print '\nModifyBgpNumberOfRoutesNgpf Error: No such networkGroupName: %s' % networkGroupName


def CreateMultivalueNgpfHlPy(**kwargs):
    print '\nCreateMultivalueNgpfHlPy:'
    ShowKwargs(**kwargs)

    multivalue = ixia_ngpf.multivalue_config(**kwargs)
    if multivalue['status'] != '1':
        print '\nConfigMultivalueHlPy: Failed'
        return 1

    return multivalue['multivalue_handle']


def ConfigOspfEmulationNgpfHlPy(**kwargs):
    print '\nConfigOspfEmulationNgpfHlPy:'
    ShowKwargs(**kwargs)

    ospfEmulation = ixia_ngpf.emulation_ospf_config(**kwargs)
    if ospfEmulation['status'] != '1':
        print '\nConfigOspfEmulationHlPy: Failed'
        return 1

    # status: 1
    # ospfv2_handle: /topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1
    return ospfEmulation


def ConfigBgpEmulationNgpfHlPy(**kwargs):
    print '\nConfigBgpEmulationNgpfHlPy:'
    for key,value in kwargs.iteritems():
        print '\t%s: %s' % (key,value)

    bgpEmulation = ixia_ngpf.emulation_bgp_config(**kwargs)
    if bgpEmulation['status'] != '1':
        print '\nConfigBgpEmulationNgpfHlPy: Failed'
        return 0

    return bgpEmulation


def ModifyBgpNumberOfRoutesNgpfHlPy( networkGroupName='', totalRoutes='' ):
    for topology in ixNet.getList(ixNet.getRoot(), 'topology'):
        for deviceGroup in ixNet.getList(topology, 'deviceGroup'):
            for networkGroup in ixNet.getList(deviceGroup, 'networkGroup'):
                currentNetworkGroupName = ixNet.getAttribute(networkGroup, '-name')
                nameMatch = re.search(r'%s' % networkGroupName, currentNetworkGroupName, re.IGNORECASE)
                if nameMatch:
                    for ipv4PrefixPool in ixNet.getList(networkGroup, 'ipv4PrefixPools'):
                        print '\nModifyBgpNumberOfRoutesNgpf: %s : totalRoutes:%s' % (ipv4PrefixPool, totalRoutes)
                        ixNet.setAttribute(ipv4PrefixPool, '-numberOfAddresses', totalRoutes)
                        ixNet.commit()
                        return

    print '\nModifyBgpNumberOfRoutesNgpfHlPy Error: No such networkGroupName: %s' % networkGroupName



def ConfigNetworkGroupNgpfHlPy(**kwargs):
    print '\nConfigNetworkGroupNgpfHlPy:'
    ShowKwargs(**kwargs)

    networkGroup = ixia_ngpf.network_group_config(**kwargs)
    if networkGroup['status'] != '1':
        print '\nConfigNetworkGroupHlPyHlPy: Failed:'
        return 1

    # status: 1
    # ipv4_prefix_pools_handle: /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1
    # network_group_handle: /topology:1/deviceGroup:1/networkGroup:1
    return networkGroup


def ConfigOspfNetworkGroupNgpfHlPy(**kwargs):
    print '\nConfigOspfNetworkGroupNgpfHlPy:'
    ShowKwargs(**kwargs)

    ospfNetworkGroup = ixia_ngpf.emulation_ospf_network_group_config(**kwargs)
    if ospfNetworkGroup['status'] != '1':
        print '\nConfigOspfNetworkGroupHlPy: Failed'
        return 1

    # status: 1
    # ipv4_prefix_pools_handle: /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1
    # ipv4_prefix_interface_handle: /topology:1/deviceGroup:1/networkGroup:1/ipv4PrefixPools:1/ospfRouteProperty:1
    # network_group_handle: /topology:1/deviceGroup:1/networkGroup:1
    return ospfNetworkGroup


def DisableSupressArpAllPortsPy(action='', ipType='ipv4'):
    # Description:
    #    This API will automatically disable or enable
    #    suppress ARP for duplicate gateway on all the
    #    ports with ipv4.

    # action = true or false

    # Code logic:
    #    - Verify if the multiValue -pattern is "counter"
    #    - If not, make it counter (so that we could create overlays to modify things.)
    #    - If it is counter, verify if there is any overlay.
    #    - If there are overlays, verify if the correct portName index exists.
    #    - If yes, then change its value true/false.
    #    - If no, create an overlay and set true/false for the portIndex number.

    root = ixNet.getRoot()
    ixNetGlobals = root+'globals'
    globalTopology = ixNetGlobals+'/topology'
    globalTopologyIp = globalTopology+'/'+ipType

    if ipType is 'ipv4':
        supressKey = '-suppressArpForDuplicateGateway'
    else:
        supressKey = '-suppressNsForDuplicateGateway'

    portNameList = ixNet.getAttribute(globalTopologyIp, '-rowNames')
    for portName in portNameList:
        multiValue = ixNet.getAttribute(globalTopologyIp, supressKey)

        try:
            portIndex = portNameList.index(portName)+1
        except:
            print '\nDisableSupressArpAllPorts Error: No such port configured:', portName
            return 1
        else:
            overlayDiscoveredFlag = 0
            overlayList = ixNet.getList(multiValue, 'overlay')
            if overlayList:
                for overlay in overlayList:
                    currentIndex = ixNet.getAttribute(overlay, '-index')
                    if portIndex == currentIndex:
                        overlayDiscoveredFlag = 1
                        print '\nEnableDisableSuppressArpAllPorts = %s' % action
                        ixNetResult = ixNet.setMultiAttribute(overlay,
                                                              '-value', action,
                                                              '-valueStep', action,
                                                              '-count', '1',
                                                              '-indexStep', '0'
                                                              )
                        if ixNetResult != '::ixNet::OK':
                            print '\EnableDisableSuppressArpAllPorts error:', ixNetResult

                        ixNet.commit()

                    if overlayDiscoveredFlag == 0:
                        # Getting here means no overlay index found for the $portIndex.
                        # Have to create an overlay with the proper -index number.
                        print '\nEnableDisableSuppressArpAllPorts: No overlay found for:', portName
                        print 'Creating an overlay ...'
                        currentOverlay = ixNet.add(multiValue, 'overlay')
                        ixNet.setMultiAttribute(currentOverlay,
                                           '-value', action,
                                           '-valueStep', action,
                                           '-count', '1',
                                           '-index', portIndex
                                           )
                        ixNet.commit()
            else:
                # Getting here means there is no overlays.
                # Change the multiValue pattern to counter so that we
                # are able to modify anything
                ixNet.setAttribute(multiValue, '-pattern', 'counter')
                ixNet.commit()
                ixNet.setAttribute(multiValue+'/counter', '-start', 'true')
                ixNet.commit()
                
                print '\nEnableDisableSuppressArpAllPorts: Creating overlay: %s -index %s -value %s' % (
                    portName, portIndex, action)
                # Create Overlays with proper index number based on the portIndex
                # in $root/globals/topology/ipv4 -rowNames indexes
                currentOverlay = ixNet.add(multiValue, 'overlay')
                ixNet.setMultiAttribute(currentOverlay,
                                        '-value', action,
                                        '-valueStep', action,
                                        '-count', '1',
                                        '-index', portIndex
                                        )
                ixNet.commit()
    return 0

def TakeSnapshotPy(copyToLocalPath=None, view='Flow Statistics', osPlatform='windows'):
    """
    Take a snapshot of the selected stat view and transfer the file to 
    the local file system where the script was executed.
        
    Parameters
       copyToLocalPath: The local path to save the CSV stat file.
       view: The stat view to take snapshot of.
       osPlatform: The IxNetwork API server OS: windows|linux
    """
    if osPlatform == 'windows':
        # This directory will hold the snapshot on the Windows filesystem.
        # If the folder does not exists, it will be created.
        path = 'C:\\Results'

    if osPlatform == 'linux':
        path = '/home/ixia_logs'

    stats = ixNet.getRoot() + '/statistics'
    csvFileName = view.replace(' ', '_')
    listOfTrafficStats = [view]

    opts = ixNet.execute('GetDefaultSnapshotSettings')

    filePathToChange = 'Snapshot.View.Csv.Location: '+ path
    print '\ntakeSnapshot src file path:%s' % (filePathToChange)
    
    opts[1] = filePathToChange
    generatingModeToChange= 'Snapshot.View.Csv.GeneratingMode: "kOverwriteCSVFile"'
    opts[2] = generatingModeToChange
    fileNameToAppend = 'Snapshot.View.Csv.Name: '+ csvFileName ;# Flow_Statistics
    opts.append(fileNameToAppend)

    ixNet.execute('TakeViewCSVSnapshot', listOfTrafficStats, opts)

    if copyToLocalPath is None:
        copyToLocalPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if osPlatform == 'windows':
        readPath = path + '\\' + csvFileName + '.csv'
        writePath = '%s/%s_%s.csv' % (copyToLocalPath, csvFileName, timestamp)
        
    if osPlatform == 'linux':
        readPath = '%s/%s.csv' %s (path, csvFileName)
        writePath = '%s/%s_%s.csv' % (copyToLocalPath, csvFileName, timestamp)

     print '\ntakeSnapshot: Saving file to: %s' % (writePath)
    ixNet.execute('copyFile', ixNet.readFrom(readPath, '-ixNetRelative'), ixNet.writeTo(writePath, '-overwrite'))


def GetVportConnectedToPortPy(vport):
    # Return the physical port of the vport

    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
    connectedTo = ixNet.getAttribute(vport, '-connectedTo')
    connectedTo = connectedTo.split('/')[3:]
    card = connectedTo[0].split(':')[1]
    port = connectedTo[1].split(':')[1]
    return card+'/'+port


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

def GetStatViewPy( getStatsBy='Flow Statistics' ):
    '''
    Description:
        This API will return you a Python Dict of all the stats 
        based on your specified stat name which are shown below.

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

    view = viewList[statsViewIndex]
    ixNet.setAttribute(view, '-enabled', 'true')
    ixNet.commit()
    columnList = ixNet.getAttribute(view+'/page', '-columnCaptions')
    print '\n', columnList
    
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
            
            for rowIndex in xrange(0, len(rowList)):
                row += 1
                cellList = rowList[rowIndex]
                statDict[row] = {}
                # CellList: ['Ethernet - 002', 'Ethernet - 001', 'OSPF T1 to T2', '206.27.0.0-201.27.0.0', 'OSPF T1 to T2-FlowGroup-1 - Flow Group 0002', '1225', '1225', '0', '0', '0', '0', '0', '0', '156800', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '00:00:00.781', '00:00:00.849']
                index = 0
                for statValue in cellList:
                    statDict[row].update({columnList[index]: statValue})
                    index += 1
    return statDict

def VerifyProtocolSessionsNgpfPy(protocol):
    # This API will return a list of protocol session status on the specified protocol
    # handle.  The protocol handle is provided when you create a new protocol.
    # 
    # For example:
    #   ospf handle: ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1/ipv4:1/ospfv2:1
    #   bgp handle:  ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1/ipv4:1/bgpIpv4Peer:1
    return ixNet.getAttribute(protocol, '-sessionStatus')

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
                                    print '\tWait %d/%d seconds' % (timer, timeEnd)
                                    time.sleep(1)
                                    continue
                                if timer == timeEnd and [element for element in sessionDownList if element in currentStatus] != []:
                                    print '\tProtocol session failed to come up:'
                                    return 1
    return 0

def VerifySessionsOspfV2NgpfPy():
    # This API will loop through all Topology Groups for ospf configuration and
    # verify all of its sessions.
    #
    # Returns 0 if all sessions are UP.
    # Returns a list of local router ID addresses that are down.

    for topology in ixNet.getList(ixNet.getRoot(), 'topology'):
        for deviceGroup in ixNet.getList(topology, 'deviceGroup'):
            for ethernet in ixNet.getList(deviceGroup, 'ethernet'):
                for ipv4 in ixNet.getList(ethernet, 'ipv4'):
                    for ospfV2 in ixNet.getList(ipv4, 'ospfv2'):
                        print '\nVerifying ospfV2Router sessions:', ospfV2
                        sessionStatusList = ixNet.getAttribute(ospfV2, '-sessionStatus')
                        localRouterIdList = ixNet.getAttribute(ospfV2, '-localRouterID')
                        if 'down' in sessionStatusList:
                            duplicateIndexes = [index for index,element in enumerate(sessionStatusList) if element == 'down']
                            returnList = []
                            print 'duplicateIndexes:', duplicateIndexes
                            for eachIndex in duplicateIndexes:
                                localRouterIpAddress = localRouterIdList[eachIndex]
                                returnList.append(localRouterIpAddress)
                                print 'Local router ID Address is down:', localRouterIpAddress
                            return returnList
                        else:
                            return 0

def VerifySessionsBgpNgpfPy():
    # This API will loop through all Topology Groups for bgp configuration and
    # verify all of its sessions.
    #
    # Returns 0 if all sessions are UP.
    # Returns a list of local Ip addresses that are down.

    for topology in ixNet.getList(ixNet.getRoot(), 'topology'):
        for deviceGroup in ixNet.getList(topology, 'deviceGroup'):
            for ethernet in ixNet.getList(deviceGroup, 'ethernet'):
                for ipv4 in ixNet.getList(ethernet, 'ipv4'):
                     for bgp in ixNet.getList(ipv4, 'bgpIpv4Peer'):
                        print '\nVerifying BGP sessions:', bgp
                        sessionStatusList = ixNet.getAttribute(bgp, '-sessionStatus')
                        localIpList = ixNet.getAttribute(bgp, '-localIpv4Ver2')
                        if 'down' in sessionStatusList:
                            duplicateIndexes = [index for index,element in enumerate(sessionStatusList) if element == 'down']
                            returnList = []
                            for eachIndex in duplicateIndexes:
                                localIpAddress = localIpList[eachIndex]
                                returnList.append(localIpAddress)
                                print 'Local IP Address is down:', localIpAddress
                            return returnList
                        else:
                            return 0

def SetLicenseServerIp( ixNet, licenseServerIp ):
    ixNet.setAttribute(ixNet.getRoot()+'globals/licensing', '-licensingServers', licenseServerIp)
    ixNet.commit()

def SetLicenseServerMode( ixNet, mode ):
    # mode options: subscription, mixed, perpetual
    ixNet.setAttribute(ixNet.getRoot()+'globals/licensing', '-mode', mode)
    ixNet.commit()

def SetLicenseServerTier( ixNet, tier ):
    # tier options: tier0, tier1, tier2, tier3, tier3-10g
    ixNet.setAttribute(ixNet.getRoot()+'globals/licensing', '-tier', tier)
    ixNet.commit()

def GetLicenseServerIp( ixNet ):
    # Returns a list of license server IP addresses
    return ixNet.getAttribute(ixNet.getRoot()+'globals/licensing', '-licensingServers')

def GetLicenseServerMode( ixNet ):
    # mode options: subscription, mixed, perpetual
    return ixNet.getAttribute(ixNet.getRoot()+'globals/licensing', '-mode')

def GetLicenseServerTier( ixNet ):
    return ixNet.getAttribute(ixNet.getRoot()+'globals/licensing', '-tier')

def IxVmConnectToVChassisPy(vChassisIp):
    # Besides connecting to ixNet, you must also connect to the 
    # virtual chassis to configure IxVM ports.

    ixvmChassisStatus = ixNet.execute('connectToChassis', vChassisIp)
    if ixvmChassisStatus != '::ixNet::OK':
        print '\nFailed to connect to virtual chassis IP: %s\n' % vChassisIp
        return 1
    else:
        return 0

def IxVmAddHypervisor(ixNet, vChassisIp, vLoadModuleLogin, vLoadModulePassword, vLoadModuleType):
    availableHardwareObj = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardwareObj, 'virtualChassis')[0]

    try:
        hypervisor = ixNet.add(vChassisObj, 'hypervisor')
        ixNet.setAttribute(hypervisor, '-enable', '%s' % 'true')
        ixNet.setAttribute(hypervisor, '-serverIp', '%s' % vChassisIp)
        ixNet.setAttribute(hypervisor, '-user', '%s' % vLoadModuleLogin)
        ixNet.setAttribute(hypervisor, '-password', '%s' % vLoadModulePassword)
        ixNet.setAttribute(hypervisor, '-type', '%s' % vLoadModuleType)
        ixNet.commit()
    except:
        #hypervisor = '::ixNet::OBJ-/availableHardware/virtualChassis/hypervisor:"192.168.70.10"'
        hypervisor = ixNet.getList(vChassisObj, 'hypervisor')[0]

    if len(hypervisor) != 0:
        print 'Hypervisor:', hypervisor
        return hypervisor
    else:
        return 0

def IxVmDiscoverAppliancesPy(ixNet):
    availableHardwareObj = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardwareObj, 'virtualChassis')[0]

    # Load Modules
    # ['::ixNet::OBJ-/availableHardware/virtualChassis/discoveredAppliance:"192.168.70.130"', 
    #   '::ixNet::OBJ-/availableHardware/virtualChassis/discoveredAppliance:"192.168.70.131"']
    discoveredApplianceList = ixNet.getList(vChassisObj, 'discoveredAppliance')
    for eachDiscoveredAppliance in discoveredApplianceList:
        print 'DiscoveredAppliances:', eachDiscoveredAppliance
    return discoveredApplianceList

def IxVmRemoveAllHypervisorsPy( ixNet ):
    # ixNet = object
    # Example: ixNet = IxNetwork.IxNet() & ixNet.connect(apiServer)

    availableHardware = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardware, 'virtualChassis')[0]
    hypervisorList = ixNet.getList(vChassisObj, 'hypervisor')

    for eachHypervisor in hypervisorList:
        print 'Removing hypervisor:', eachHypervisor
        ixNet.remove(eachHypervisor)
        ixNet.commit()

    hypervisorList = ixNet.getList(vChassisObj, 'hypervisor')
    if len(hypervisorList) == 0:
        print 'removeAllHypervisors: verified good'
        return 1
    else:
        print 'removeAllHypervisors: verified failed'
        return 0

def IxVmCreateVmCardsAndPortsPy(ixNet):
    # This API will go discover all created IxVM Load Modules and bring them up
    # as cards/ports for usage.
    # This API will assume that each virtual load module has one eth1 interface created
    # as test port.

    # This API requires calling APIs:
    #    - ixVmRediscoverAppliances()
    #    - ixVmDiscoverAppliances()

    # Returns an XML format of discovered load module management IP addresses
    rediscoverStatus = ixVmRediscoverAppliancesPy(ixNet)
    discoveredAppliances = IxVmDiscoverAppliancesPy(ixNet)

    availableHardwareObj = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardwareObj, 'virtualChassis')[0]

    cardNumber = 1
    for eachAppliance in discoveredAppliances:
        mgmtIp =ixNet.getAttribute(eachAppliance, '-managementIp')
        print 'Adding new ixVmCard %d/%s: %s' % (cardNumber, '1', eachAppliance)
        # ::ixNet::OBJ-/availableHardware/virtualChassis/ixVmCard:L6
        ixVmCardObj = ixNet.add(vChassisObj, 'ixVmCard')

        ixNet.setMultiAttribute(ixVmCardObj, '-managementIp', mgmtIp, '-cardId', str(cardNumber))
        ixNet.commit()

        # ::ixNet::OBJ-/availableHardware/virtualChassis/ixVmCard:"Card1"/ixVmPort:L7
        ixVmPortObj = ixNet.add(ixVmCardObj, 'ixVmPort')
        ixNet.setMultiAttribute(ixVmPortObj,
                                '-portId', '1',
                                '-interface', 'eth1',
                                '-promiscuous', 'false',
                                '-mtu', '1500')
        ixNet.commit()
        cardNumber += 1

def IxVmRemoveCardIdPy(ixNet, vmCardId):
    # This API will remove the specified vm card ID.
    # ixNet = object
    # Example: ixNet = IxNetwork.IxNet() & ixNet.connect(apiServer)

    import re
    availableHardware = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardware, 'virtualChassis')[0]
    vmCardList = ixNet.getList(vChassisObj, 'ixVmCard')
    releaseAllPortsPy(ixNet)

    for eachVmCardId in vmCardList:
        # '::ixNet::OBJ-/availableHardware/virtualChassis/ixVmCard:"Card1"'
        currentCardIdMatch = re.match('::ixNet.*ixVmCard.*Card([0-9]+)', eachVmCardId)
        if currentCardIdMatch:
            if int(currentCardIdMatch.group(1)) == vmCardId:
                print '\nremoveCardId:', eachVmCardId
                ixNet.remove(eachVmCardId)
                ixNet.commit()
                return 0
    return 1

def IxVmRemoveAllCardsPy(ixNet):
    # This API will remove all vm cards.
    # ixNet = object
    # Example: ixNet = IxNetwork.IxNet() & ixNet.connect(apiServer)

    availableHardware = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardware, 'virtualChassis')[0]
    vmCardList = ixNet.getList(vChassisObj, 'ixVmCard')
    releaseAllPortsPy(ixNet)

    for eachVmCardId in vmCardList:
        # '::ixNet::OBJ-/availableHardware/virtualChassis/ixVmCard:"Card1"'
        print '\nremoveCardId:', eachVmCardId
        ixNet.remove(eachVmCardId)
        ixNet.commit()

def IxVmRemovePortIdPy(ixNet, vmCardId, vmPortId):
    # This API will remove the specified vmCardId/vmPortId
    # ixNet = object
    # Example: ixNet = IxNetwork.IxNet() & ixNet.connect(apiServer)

    import re
    availableHardware = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardware, 'virtualChassis')[0]
    vmCardList = ixNet.getList(vChassisObj, 'ixVmCard')

    for eachVmCardId in vmCardList:
        # '::ixNet::OBJ-/availableHardware/virtualChassis/ixVmCard:"Card1"'
        currentCardIdMatch = re.match('::ixNet.*ixVmCard.*Card([0-9]+)', eachVmCardId)
        if currentCardIdMatch:
            if int(currentCardIdMatch.group(1)) == vmCardId:
                vmPortIdList = ixNet.getList(eachVmCardId, 'ixVmPort')

                for eachVmPortId in vmPortIdList:
                    currentPortIdMatch = re.match('::ixNet.*ixVmPort.*Port([0-9]+)', eachVmPortId)
                    if int(currentPortIdMatch.group(1)) == vmPortId:
                        print '\nremoveCardIdPortId: Removing:', eachVmPortId
                        ixNet.remove(eachVmPortId)
                        ixNet.commit()
                        return 0
    return 1

def IxVmRediscoverAppliancesPy(ixNet):
    # Returns an XML data:
    #    <ApplianceInfo>
    #    <ApplianceName>port1</ApplianceName>
    #    <ApplianceType>VMware</ApplianceType>
    #    <ManagementIP>192.168.70.130</ManagementIP>
    #    <RODiskVersion />
    #    <InterfaceName>eth0</InterfaceName>
    #    <State>Assigned</State>
    #    </ApplianceInfo>
    return ixNet.execute('rediscoverAppliances')

def IxVmRefreshChassisTopologyPy(ixNet):
    ixNet.execute('ixVmRefreshChassisTopology')

def IxVmRemoveAllVmConfigPy(ixNet):
    IxVmRemoveAllCardsPy(ixNet)
    IxVmRemoveAllHypervisorsPy(ixNet)

def IxVmRebuildChassisTopologyPy(ixNet, ixNetworkVersion):
    print '\nRebuilding chassis topology ...'
    #rebuildChassisTopology (kString - ixnVersion ,kBool - usePrevSlotID ,kBool - promiscMode)
    ixNet.execute('rebuildChassisTopology', ixNetworkVersion, 'false', 'false')

def EnableFlowGroup(endpointSetName, mode=True):
    '''
    endpointSetName: The name of the EndpointSetId (Flow Group) 
    mode: True|False
    '''
    for trafficItem in ixNet.getList(ixNet.getRoot()+'traffic', 'trafficItem'):            
        for endpointSetIdObj in ixNet.getList(trafficItem, 'endpointSet'):
            endpointSetIdName = ixNet.getAttribute(endpointSetIdObj, '-name')
            endpointSetId = endpointSetIdObj.split(':')[-1]

            if endpointSetName == endpointSetIdName:
                for highLevelStream in ixNet.getList(trafficItem, 'highLevelStream'):
                    endpointId = ixNet.getAttribute(highLevelStream, '-endpointSetId')
                    
                    if endpointId == endpointSetId:
                        print '\nEnableFlowGroup=%s: endpontSetName:%s' % (mode, endpointSetName)
                        print highLevelStream
                        ixNet.setAttribute(highLevelStream, '-enabled', mode)
                        ixNet.commit()

