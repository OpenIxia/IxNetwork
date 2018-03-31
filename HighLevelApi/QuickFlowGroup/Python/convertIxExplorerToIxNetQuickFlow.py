
# Description
#
#    Customers who has legacy IxExplorer-FT HL API scripts and need to
#    convert scripts to IxNetwork.
#
#    Mainly because the IxExplorer-FT scripts are not supported in IxNetwork
#    after version 6.80.
#
#    The solution is to use IxNetwork Quick Flow Group, which is designed for
#    IxExplorer usage in IxNetwork.
#
#    This script is a sample to show how to use customer's existing HL API parameters/values
#    and automatically ...
#        - Create a Quick Flow Group (Traffic Item)
#        - Get all the configured vports and add all vports to the HLAPI parameter -port_handle2
#          as receiving ports.
#        - Enable traffic item Ingress tracking.
#        - Regenerate Traffic Item.
#        - Start traffic
#        - Get Port Statistics stats.
#        - Look for all the ports that received traffic.

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

ixnetwork_tcl_server = '192.168.70.3'
port_1 = '1/1/1'
port_2 = '1/2/1'

# Convert vport to physical port
def GetVportConnectedToPortPy(vport):
    # Return the physical port of the vport

    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
    connectedTo = ixNet.getAttribute(vport, '-connectedTo')
    connectedTo = connectedTo.split('/')[3:]
    card = connectedTo[0].split(':')[1]
    port = connectedTo[1].split(':')[1]
    return '1/'+card+'/'+port

def CreateQuickFlowGroup():
    print '\nCreating a traffic item'
    quickFlowGroupObj = ixNet.add(ixNet.getRoot()+'/traffic', 'trafficItem')
    ixNet.setMultiAttribute(quickFlowGroupObj ,'-trafficItemType', 'quick', '-trafficType', 'raw')
    ixNet.commit()
    quickFlowGroupObj = ixNet.remapIds(quickFlowGroupObj)[0]
    #ixNet.setAttribute(quickFlowGroupObj + '/tracking', '-trackBy', ['trackingenabled0'])
    #ixNet.commit()
    print 'Done: Returning:', quickFlowGroupObj
    return quickFlowGroupObj

def ConfigQuickFlowGroup(portHandle, **trafficParams):
    """
    Desciption
        Using IxExplorer-FT HL APIs to configure IxNetwork Quick Flow Group.
        For Quick Flow Group, only one QFG is allowed and required.
        If you have multiple streams, they all fall under this QFG.
    """
    print '\nExisting Traffic Item:', ixNet.getList(ixNet.getRoot()+'/traffic', 'trafficItem')

    if ixNet.getList(ixNet.getRoot()+'/traffic', 'trafficItem') == []:
        print '\nCreating new traffic item for Quick Flow Group'
        quickFlowGroupObj = ixNet.add(ixNet.getRoot()+'/traffic', 'trafficItem')
        ixNet.setMultiAttribute(quickFlowGroupObj ,'-trafficItemType', 'quick', '-trafficType', 'raw')
        ixNet.commit()
        quickFlowGroupObj = ixNet.remapIds(quickFlowGroupObj)[0]
        print 'QuickFlowGroupObj:', quickFlowGroupObj

    print 'ConfigQuickFlowGroup:', trafficParams['name']

    # Get a list of all the configured ports as the receiving ports.
    portList = []
    for eachVport in ixNet.getList(ixNet.getRoot(), 'vport'):
        port = GetVportConnectedToPortPy(eachVport)
        portList.append(port)
    print '\nAll vport list for Rx ports:', portList

    trafficParams.update({'port_handle': portHandle, 'port_handle2': ' '.join(portList), 'circuit_type':'quick_flows'})
    print '\nConfiguring HLT params:', trafficParams
    result = ixia_hlt.traffic_config(**trafficParams)
    print '\nResult:', result

    # Enable ingress tracking
    print 'Enabling Quick Flow Group statistics tracking'
    quickFlowGroupObj = ixNet.getList(ixNet.getRoot()+'/traffic', 'trafficItem')[0]
    ixNet.setAttribute(quickFlowGroupObj + '/tracking', '-trackBy', ['trackingenabled0'])
    ixNet.commit()

def RegenerateAllTrafficItemsPy():
    for trafficItem in ixNet.getList(ixNet.getRoot()+'/traffic', 'trafficItem'):
        result = ixNet.execute('generate', trafficItem)
        
        if result != '::ixNet::OK':
            print '\nRegenerate_All_TrafficItems failed: ', trafficItem
            ixNet.disconnect()
            sys.exit()

def StartTrafficNgpfHlPy():
    print '\nStartTrafficNgpfHlPy'
    status = ixia_ngpf.traffic_control(action = 'run')    
    if status == 1:
        print '\nStartTrafficNgpfHlPy failed: ', status['log']
        return 1

    return status


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


connect_result = ixia_ngpf.connect ( 
    ixnetwork_tcl_server = ixnetwork_tcl_server,
    tcl_server = tcl_server,
    username = user_name,
    break_locks = '1'
    ) 

trafficItem1 = { 'name': 'rule1',
                 'mode': 'create',
                 'mac_dst_mode' : 'fixed',
                 'mac_src_mode' : 'fixed',
                 'mac_src'   :   '00:0C:29:AA:86:E1',
                 'mac_dst'   :   '00:0C:29:84:37:16',
                 'transmit_mode': 'single_burst',
                 'rate_pps' : 1000,
                 'l3_protocol': 'ipv4',
                 'ip_src_addr': '1.1.1.1',
                 'ip_src_mode': 'increment',
                 'ip_src_step': '0.0.0.1',
                 'ip_src_count': '1',
                 'ip_dst_addr': '1.1.1.2',
                 'ip_dst_mode':'increment',
                 'ip_dst_step': '0.0.0.1',
                 'ip_dst_count': '1',
                 'rate_percent': '10',
                 'frame_size': '1000',
                 'number_of_packets_per_stream': 50000
             }

trafficItem2 = { 'name': 'rule2',
                 'mode': 'create',
                 'mac_dst_mode' : 'fixed',
                 'mac_src_mode' : 'fixed',
                 'mac_src'   :   '00:0C:29:AA:86:E1',
                 'mac_dst'   :   '00:0C:29:84:37:16',
                 'transmit_mode': 'single_burst',
                 'rate_pps' : 1000,
                 'l3_protocol': 'ipv4',
                 'ip_src_addr': '10.10.10.1',
                 'ip_src_mode': 'increment',
                 'ip_src_step': '0.0.0.1',
                 'ip_src_count': '1',
                 'ip_dst_addr': '10.10.10.2',
                 'ip_dst_mode':'increment',
                 'ip_dst_step': '0.0.0.1',
                 'ip_dst_count': '1',
                 'rate_percent': '10',
                 'frame_size': '1000',
                 'number_of_packets_per_stream': 50000
             }

ConfigQuickFlowGroup(portHandle=port_1, **trafficItem1)
ConfigQuickFlowGroup(portHandle=port_2, **trafficItem2)

RegenerateAllTrafficItemsPy()
StartTrafficNgpfHlPy()
time.sleep(15)

traffic_stats = GetStatsPy(getStatsBy='Port Statistics')
PrintDict(traffic_stats)

# TODO: Look for all the ports that received traffic
