#!/usr/local/python2.7.6/bin/python2.7

# By Hubert Gee
# 2/5/2017

# Tested with IxNetwork 8.20
#
# Description:
#
#    - Load a saved config file.
#    - Reassign Ports:  Exclude calling assignPorts if it's unecessary.
#    - Verify port states.
#    - Start all protocols.
#    - Verify all protocol sessions.
#    - Apply Traffic
#    - Regenerate Traffic
#    - Start Traffic
#    - Get Stats
#

import sys
import zipfile
import requests
import json
import os
import time

class TestFailedError(Exception): pass
class Py: pass

py = Py()
portList = [['10.219.117.101', '1', '1'], ['10.219.117.101', '1', '2']]
py.ixTclServer  =  "10.219.117.103"
py.ixRestPort   =  '11009'

py.ixTclServer  =  "192.168.70.127"
py.ixRestPort   =  '11009'

def waitForComplete(response, sessionUrl, timeout=90):
    # response: Provide the POST action response.  Generally, after an /operations action.
    #           Such as /operations/startallprotocols, /operations/assignports
    # sessionUrl: http://10.219.x.x:11009/api/v1/sessions/1/ixnetwork
    # 
    # Returns 0 if the state is good
    # Returns 1 if the  state remains down or IN_PROGRESS after timeout.

    if response.json().has_key("errors"):
        print response.json()["errors"][0]
        return 1
    print "\n", sessionUrl
    print "\t\tState:",response.json()["state"]
    while response.json()["state"] == "IN_PROGRESS" or response.json()["state"] == "down":
        if timeout == 0:
            return 1
        time.sleep(1)
        response = requests.get(sessionUrl)
        state = response.json()["state"]
        print "\t\tState:", state
        timeout = timeout - 1
    
    # Falling down here means success
    return 0

def assignPorts(sessionUrl, portList):
    # Use this API to assign or reassign ports.
    # 
    # sessionUrl: http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork
    # portList: [['10.219.117.101','1','1'], ['10.219.117.101','1','2']]
    #
    # POST:  http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/operations/assignports
    #        data={arg1: [{arg1: 10.219.117.101, arg2: 1, arg3: 1}, {arg1: 10.219.117.101, arg2: 1, arg3: 2}],
    #              arg2: [],
    #              arg3: [http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/vport/1,
    #                     http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/vport/2],
    #              arg4: true}
    #        headers={'content-type': 'application/json'}
    # GET:  http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/operations/assignports/1
    #       data={}
    #       headers={}
    # GET RESPONSE:  SUCCESS
    #
    # Returns 0 if success
    # Returns 1 if failed
    
    response = requests.get(sessionUrl+'/vport')
    if response.status_code != 200:
        return 1

    vportList = ["%s/vport/%s" % (sessionUrl, str(i["id"])) for i in response.json()]
    if len(vportList) != len(portList):
        print '\nassignPorts error: The amount of configured virtual ports is not equal to the portList amount'
        return 1

    data = {"arg1": [], "arg2": [], "arg3": vportList, "arg4": "true"}
    [data["arg1"].append({"arg1":str(chassis), "arg2":str(card), "arg3":str(port)}) for chassis,card,port in portList] 
    response = requests.post(sessionUrl+'/operations/assignports',
                             data=json.dumps(data),
                             headers={'content-type': 'application/json'})
    if waitForComplete(response, sessionUrl+'/operations/assignports/'+response.json()['id']) == 1:
        return 1
    else:
        return 0

def verifyPortState(sessionUrl):
    # sessionUrl: http://10.219.x.x:11009/api/v1/sessions/1/ixnetwork
    #
    # Returns 0 if all ports are up.
    # Returns 1 if any port is down.

    response = requests.get(sessionUrl+'/vport')
    vportList = ["%s/vport/%s" % (sessionUrl, str(i["id"])) for i in response.json()]
    for eachVport in vportList:
        for counter in range(0,61):
            response = requests.get(eachVport)
            print '\n', eachVport
            print '\t\tVerify Port State:', response.json()['state']
            if counter < 60 and response.json()['state'] == 'down':
                time.sleep(1)
                continue
            if counter < 60 and response.json()['state'] == 'up':
                return 0
            if counter == 60 and response.json()['state'] == 'down':
                # Failed
                return 1

def startAllProtocols(sessionUrl):
    # sessionUrl: http://10.219.x.x:11009/api/v1/sessions/1/ixnetwork

    # POST:  http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/operations/startallprotocols
    #        data={}
    #        headers={'content-type': 'application/json'}
    # 
    # Returns 0 if success
    # Returns 1 if failed

    print '\nstartAllProtocols'
    response = requests.post(sessionUrl+'/operations/startallprotocols', data={}, headers={})
    if response.status_code == 202:
        return 0
    else:
        return 1

def stopAllProtocols(session):
    # sessionUrl: http://10.219.x.x:11009/api/v1/sessions/1/ixnetwork
    # 
    # Returns 0 if success
    # Returns 1 if failed

    print '\nstopAllProtocols'
    response = requests.post(sessionUrl+'/operations/stopallprotocols', data={}, headers={})
    if response.status_code == 202:
        return 0
    else:
        return 1

def verifyProtocolSessions(protocolObjList, timeout=90):
    # Verify the user specified protocol list to verify for session UP.
    #
    # GET:  http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1
    #       data={}
    #       headers={}
    # GET RESPONSE:  [u'notStarted', u'notStarted', u'notStarted', u'notStarted', u'notStarted', u'notStarted']
    # GET:  http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1
    #       data={}
    #       headers={}
    # GET RESPONSE:  [u'up', u'up', u'up', u'up', u'up', u'up', u'up', u'up']
    # GET:  http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1
    #       data={}
    #       headers={}
    #
    #protocolObjList: ['http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1',
    #                  'http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1',
    #                  'http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1',
    #                  'http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/ospfv2/1',]
    # timeout: Total wait time for all the protocols in the provided list to come up.

    timerStop = timeout

    for eachProtocol in protocolObjList:
        # notStarted, up or down
        print '\nVerifyProtocolSessions: %s\n' % eachProtocol
        for timer in range(1,timerStop+1):
            #response = requests.get(sessionUrl+eachProtocol)
            response = requests.get(eachProtocol)
            if response.status_code != 200:
                print 'Failed to get response'
                continue

            protocolSessionStatus = response.json()['sessionStatus']
            print '\tStatus: Down : Wait %s/%s seconds' % (timer, timerStop)
            if timer < timerStop+1:
                if 'down' in protocolSessionStatus or 'notStarted' in protocolSessionStatus:
                    time.sleep(1)
            if timer < timerStop+1: 
                if 'down' not in protocolSessionStatus and 'notStarted' not in protocolSessionStatus:
                    print '\n\tStatus: All UP'
                    break
            if timer == timerStop:
                if 'down' in protocolSessionStatus or 'notStarted' in protocolSessionStatus:
                    print '\nverifyProtocolSessions Failed'
                    return 1
    return 0

def verifyAllProtocolSessionsNgpf(sessionUrl, timeout=120):
    # This API will loop through each created Topology Group and verify
    # all the created protocols for session up for up to 120 seconds total.
    # Will verify IPv4 and IPv6.
    # 
    # Returns 0 if all sessions are UP.
    # Returns 1 if any session remains DOWN after 120 seconds.

    protocolList = ['ancp',
                    'bfdv4Interface',
                    'bgpIpv4Peer',
                    'bgpIpv6Peer',
                    'dhcpv4relayAgent',
                    'dhcpv6relayAgent',
                    'dhcpv4server',
                    'dhcpv6server',
                    'geneve',
                    'greoipv4',
                    'greoipv6',
                    'igmpHost',
                    'igmpQuerier',
                    'lac',
                    'ldpBasicRouter',
                    'ldpBasicRouterV6',
                    'ldpConnectedInterface',
                    'ldpv6ConnectedInterface',
                    'ldpTargetedRouter',
                    'ldpTargetedRouterV6',
                    'lns',
                    'mldHost',
                    'mldQuerier',
                    'ptp',
                    'ipv6sr',
                    'openFlowController',
                    'openFlowSwitch',
                    'ospfv2',
                    'ospfv3',
                    'ovsdbcontroller',
                    'ovsdbserver',
                    'pcc',
                    'pce',
                    'pcepBackupPCEs',
                    'pimV4Interface',
                    'pimV6Interface',
                    'ptp',
                    'rsvpteIf',
                    'rsvpteLsps',
                    'tag',
                    'vxlan'
                ]

    sessionDownList = ['down', 'notStarted']
    startCounter = 1
    import time

    response = requests.get(sessionUrl+'/topology')
    topologyList = ['%s/%s/%s' % (sessionUrl, 'topology', str(i["id"])) for i in response.json()]
    for topology in topologyList:
        response = requests.get(topology+'/deviceGroup')
        deviceGroupList = ['%s/%s/%s' % (topology, 'deviceGroup', str(i["id"])) for i in response.json()]
        for deviceGroup in deviceGroupList:
            response = requests.get(deviceGroup+'/ethernet')
            ethernetList = ['%s/%s/%s' % (deviceGroup, 'ethernet', str(i["id"])) for i in response.json()]
            for ethernet in ethernetList:
                response = requests.get(ethernet+'/ipv4')
                ipv4List = ['%s/%s/%s' % (ethernet, 'ipv4', str(i["id"])) for i in response.json()]
                response = requests.get(ethernet+'/ipv6')
                ipv6List = ['%s/%s/%s' % (ethernet, 'ipv6', str(i["id"])) for i in response.json()]
                for ipv4 in ipv4List+ipv6List:
                    for protocol in protocolList:
                        response = requests.get(ipv4+'/'+protocol)
                        if response.json() == [] or 'errors' in response.json():
                            continue

                        currentProtocolList = ['%s/%s/%s' % (ipv4, protocol, str(i["id"])) for i in response.json()]
                        for currentProtocol in currentProtocolList:
                            for timer in range(startCounter, timeout+1):
                                response = requests.get(currentProtocol)
                                currentStatus = response.json()['sessionStatus']
                                print '\n%s' % currentProtocol
                                print '\tTotal sessions: %d' % len(currentStatus)
                                totalDownSessions = 0
                                for eachStatus in currentStatus:
                                    if eachStatus != 'up':
                                        totalDownSessions += 1
                                print '\tTotal sessions Down: %d' % totalDownSessions

                                if timer < timeout and [element for element in sessionDownList if element in currentStatus] == []:
                                    print '\tProtocol sessions are all up'
                                    startCounter = timer
                                    break
                                if timer < timeout and [element for element in sessionDownList if element in currentStatus] != []:
                                    print '\tWait %d/%d seconds' % (timer, timeout)
                                    time.sleep(1)
                                    continue
                                if timer == timeout and [element for element in sessionDownList if element in currentStatus] != []:
                                    print '\tProtocol session failed to come up:'
                                    return 1

    # All active protocols are up. Return 0
    return 0

                        
def applyTraffic(sessionUrl):
    # sessionUrl: http://10.219.x.x:11009/api/v1/sessions/1/ixnetwork
    #        data={arg1: http://10.219.x.x:11009/api/v1/sessions/1/ixnetwork/traffic}
    #        headers={'content-type': 'application/json'}    
    #
    # Returns 0 if success
    # Returns 1 if failed
    
    print '\napplyTraffic:', sessionUrl
    response = requests.post(sessionUrl+'/traffic/operations/apply',
                             data=json.dumps({'arg1': sessionUrl+'/traffic'}),
                             headers={'content-type': 'application/json'})
    if response.status_code == 202:
        if waitForComplete(response, sessionUrl+'/traffic/operations/apply/'+response.json()['id']) == 1:
            print 'applyTraffic: waitForComplete failed'
            return 1
        else:
            return 0
    else:
        return 1

def regenerateAllTrafficItems(sessionUrl):
    # Performs regenerate on all enabled Traffic Items.
    # This API requires the waitForComplete API also.
    #
    # sessionUrl: http://10.219.x.x:11009/api/v1/sessions/1/ixnetwork
    #
    # Returns 0 if success
    # Returns 1 if failed

    serverUrl = sessionUrl.split('/api')[0]
    response = requests.get(sessionUrl + "/traffic/trafficItem")
    trafficItemList = ["%s%s" % (serverUrl, str(i["links"][0]["href"])) for i in response.json()]
    for trafficItem in trafficItemList:
        response = requests.get(trafficItem)
        if response.status_code != 200:
            return 1

        if response.json()['enabled'] == True:
            print '\nRegenerating:', trafficItem
            response = requests.post(trafficItem+"/operations/generate",
                                     data=json.dumps({"arg1": trafficItem}),
                                     headers={"content-type": "application/json"})
            if response.status_code != 202:
                return 1

            if waitForComplete(response, trafficItem+"/operations/generate/"+response.json()['id']) == 1:
                return 1
            else:
                return 0

def startTraffic(sessionUrl):
    # sessionUrl: http://10.219.x.x:11009/api/v1/sessions/1/ixnetwork
    #
    # POST:  http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/traffic/operations/start
    #        data={arg1: http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/traffic}
    #        headers={'content-type': 'application/json'}
    #
    # Returns 0 if success
    # Returns 1 if failed

    print '\nstartTraffic:', sessionUrl+'/traffic/operations/start'
    response = requests.post(sessionUrl+'/traffic/operations/start',
                             data=json.dumps({'arg1': sessionUrl+'/traffic'}),
                             headers={'content-type': 'application/json'})
    print response.json()
    if response.status_code == 202:
        return 0
    else:
        return 1

def stopTraffic(sessionUrl):
    # sessionUrl: http://10.219.x.x:11009/api/v1/sessions/1/ixnetwork
    # 
    # Returns 0 if success
    # Returns 1 if failed
    
    print '\nstopTraffic:', sessionUrl+'/traffic/operations/stop'
    response = requests.post(sessionUrl+'/traffic/operations/stop',
                             data=json.dumps({'arg1': sessionUrl+'/traffic'}),
                             headers={'content-type': 'application/json'})
    print response.json()
    if response.status_code == 202:
        return 0
    else:
        return 1

def getStats(sessionUrl, csvFile=None, csvEnableFileTimestamp=False, viewName='Flow Statistics'):
    # sessionUrl: http://10.219.x.x:11009/api/v1/sessions/1/ixnetwork
    #
    # csvFile = None or <filename.csv>.
    #           None will not create a CSV file.
    #           Provide a <filename>.csv to record all stats to a CSV file.
    #           Example: getStats(sessionUrl, csvFile='Flow_Statistics.csv')
    #
    # csvEnableFileTimestamp = True or False. If True, timestamp will be appended to the filename.
    #
    # viewName options (Not case sensitive):
    #    NOTE: Not all statistics are listed here.
    #          You could get the statistic viewName directly from the IxNetwork GUI in the statistics.
    #
    #    'Port Statistics'
    #    'Tx-Rx Frame Rate Statistics'
    #    'Port CPU Statistics'
    #    'Global Protocol Statistics'
    #    'Protocols Summary'
    #    'Port Summary'
    #    'OSPFv2-RTR Drill Down'
    #    'OSPFv2-RTR Per Port'
    #    'IPv4 Drill Down'
    #    'L2-L3 Test Summary Statistics'
    #    'Flow Statistics'
    #    'Traffic Item Statistics'
    #    'IGMP Host Drill Down'
    #    'IGMP Host Per Port'
    #    'IPv6 Drill Down'
    #    'MLD Host Drill Down'
    #    'MLD Host Per Port'
    #    'PIMv6 IF Drill Down'
    #    'PIMv6 IF Per Port'

    # Note: Not all of the viewNames are listed here. You have to get the exact names from 
    #       the IxNetwork GUI in statistics based on your protocol(s).
    # 
    # Return you a dictionary of all the stats: statDict[rowNumber][columnName] == statValue
    #   Get stats on row 2 for 'Tx Frames' = statDict[2]['Tx Frames']

    urlHeadersJson = {'content-type': 'application/json'}
    viewList = requests.get('%s/%s/%s' % (sessionUrl, 'statistics', 'view'), headers=urlHeadersJson)
    views = ['%s/%s/%s/%s' % (sessionUrl, 'statistics', 'view', str(i['id'])) for i in viewList.json()]

    for view in views:
        # GetAttribute
        response = requests.get('%s' % view, headers=urlHeadersJson)
        if response.status_code != 200:
            print '\ngetStats: Failed:', response.text
            return 1

        import re
        #caption = response.json()['caption']
        captionMatch = re.match(viewName, response.json()['caption'], re.I)
        if captionMatch:
            # viewObj: sessionUrl + /statistics/view/11'
            viewObj = view
            break

    try:
        response = requests.patch(viewObj, data=json.dumps({'enabled': 'true'}), headers=urlHeadersJson)
    except:
        print '\ngetStats error: No stats available'
        return 0

    response = requests.get(viewObj+'/page')
    if response.status_code != 200:
        print '\ngetStats: Failed to get total pages'
        return 1

    for counter in range(0,31):
        totalPages = response.json()['totalPages']
        if totalPages == 'null':
            print '\nGetting total pages is not ready yet. Waiting %d/30 seconds' % counter
            time.sleep(1)
        if totalPages != 'null':
            break
        if totalPages == 'null' and counter == 30:
            print '\ngetStats failed: Getting total pages'
            return 1

    response = requests.get(viewObj+'/page', '-columnCaptions')
    if response.status_code != 200:
        print '\ngetStats: Failed to get statistic column names'
        return 1

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

    # Get the stat column names
    columnList = response.json()['columnCaptions']
    if csvFile != None:
        csvWriteObj.writerow(columnList)

    # Get the stat values
    response = requests.get(viewObj+'/page')
    statValueList = response.json()['pageValues']

    statDict = {}
    flowNumber = 1
    for statValue in statValueList:
        if csvFile != None:
            csvWriteObj.writerow(statValue[0])

        print '\nRow: %d' % flowNumber
        statDict[flowNumber] = {}
        index = 0
        for statValue in statValue[0]:
            statName = columnList[index]
            statDict[flowNumber].update({statName: statValue})
            print '\t%s: %s' % (statName, statValue)
            index += 1
        flowNumber += 1

    if csvFile != None:
        csvFile.close()
    return statDict
    
    # Flow Statistics dictionary output example
    '''
    Flow: 50
        Tx Port: Ethernet - 002
        Rx Port: Ethernet - 001
        Traffic Item: OSPF T1 to T2
        Source/Dest Value Pair: 2.0.21.1-1.0.21.1
        Flow Group: OSPF T1 to T2-FlowGroup-1 - Flow Group 0002
        Tx Frames: 35873
        Rx Frames: 35873
        Frames Delta: 0
        Loss %: 0
        Tx Frame Rate: 3643.5
        Rx Frame Rate: 3643.5
        Tx L1 Rate (bps): 4313904
        Rx L1 Rate (bps): 4313904
        Rx Bytes: 4591744
        Tx Rate (Bps): 466368
        Rx Rate (Bps): 466368
        Tx Rate (bps): 3730944
        Rx Rate (bps): 3730944
        Tx Rate (Kbps): 3730.944
        Rx Rate (Kbps): 3730.944
        Tx Rate (Mbps): 3.731
        Rx Rate (Mbps): 3.731
        Store-Forward Avg Latency (ns): 0
        Store-Forward Min Latency (ns): 0
        Store-Forward Max Latency (ns): 0
        First TimeStamp: 00:00:00.722
        Last TimeStamp: 00:00:10.568
    '''
    return

def printDict(obj, nested_level=0, output=sys.stdout):
    """
    Print each dict key with indentions for readability.
    """

    spacing = '   '
    if type(obj) == dict:
        print >> output, '%s' % ((nested_level) * spacing)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                printDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % ((nested_level + 1) * spacing, k, v)

        print >> output, '%s' % (nested_level * spacing)

    elif type(obj) == list:
        print >> output, '%s[' % ((nested_level) * spacing)
        for v in obj:
            if hasattr(v, '__iter__'):
                printDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % ((nested_level) * spacing)

    else:
        print >> output, '%s%s' % (nested_level * spacing, obj)


def enableDisableBgpFlapNgpf(sessionUrl, action='true', upTimeInSec=0, downTimeInSec=0):
    # This API will enable or disable flapping on all the BGP interfaces.
    #
    # sessionUrl = The BGP object handle.
    #              http://10.219.117.x:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1
    # 
    # action     = string format.  Not boolean.
    #              'true'  = enable BGP flap.
    #              'false' = disable BGP flap.
    #
    # upTimeInSecs   = Up Time In Seconds.  Provide an integer.
    # downTimeInSecs = Down Time In Seconds. Provide an integer.

    urlHeadersJson = {'content-type': 'application/json'}
    httpHeader = sessionUrl.split('/api')[0]
    print '\nenableBgpRouteFlapNgpf: Please wait a moment while I query for datas...'
    response = requests.get(sessionUrl)
    if response.status_code != 200:
        return 1

    # NOTE:  This will take a moment if the config is large
    # /api/v1/sessions/1/ixnetwork/multivalue/600
    flapMultivalue = response.json()['flap']

    upTimeInSecsMultivalue = response.json()['uptimeInSec']
    downTimeInSecsMultivalue = response.json()['downtimeInSec']

    print '\nenableDisableBgpFlapNgpf:', action
    response = requests.patch(httpHeader+flapMultivalue+'/singleValue',
                              data=json.dumps({'value': action}),
                              headers=urlHeadersJson)
    if response.status_code != 200:
        return 1

    print 'enableDisableBgpFlapNgpf upTimeInSec:', upTimeInSec
    response = requests.patch(httpHeader+upTimeInSecsMultivalue+'/singleValue',
                              data=json.dumps({'value': str(upTimeInSec)}),
                              headers=urlHeadersJson)
    if response.status_code != 200:
        return 1

    print 'enableDisableBgpFlapNgpf downTimeInSec:', downTimeInSec
    response = requests.patch(httpHeader+downTimeInSecsMultivalue+'/singleValue',
                              data=json.dumps({'value': str(downTimeInSec)}),
                              headers=urlHeadersJson)
    if response.status_code != 200:
        return 1


def startStopIgmpHostNgpf(protocolSessionUrl, action='start'):
    # protocolSessionUrl: http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1
    # action: start or stop
    
    # http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork
    sessionUrl = protocolSessionUrl.split('/topology')[0]
    url = sessionUrl+'/topology/deviceGroup/ethernet/ipv4/igmpHost/operations/%s' % action
    dataUrl = protocolSessionUrl.split('api')[1]
    data = {'arg1': [dataUrl]}
    urlHeadersJson = {'content-type': 'application/json'}
    print '\nstartStopIgmpHostNgpf: %s: %s' % (action, protocolSessionUrl)
    response = requests.post(url, data=json.dumps(data), headers=urlHeadersJson)
    if response.status_code != 202:
        return 1
    if waitForComplete(response, url+response.json()['id']) == 1:
        return 1
    else:
        return 0

def startStopPimV4InterfaceNgpf(protocolSessionUrl, action='start'):
    # protocolSessionUrl: http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/pimV4Interface/1
    # action: start or stop

    # http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork
    sessionUrl = protocolSessionUrl.split('/topology')[0]
    url = sessionUrl+'/topology/deviceGroup/ethernet/ipv4/pimV4Interface/operations/%s' % action
    dataUrl = protocolSessionUrl.split('api')[1]
    data = {'arg1': [dataUrl]}
    urlHeadersJson = {'content-type': 'application/json'}
    print '\nstartStopPimV4InterfaceNgpf: %s: %s' % (action, protocolSessionUrl)
    response = requests.post(url, data=json.dumps(data), headers=urlHeadersJson)
    if response.status_code != 202:
        return 1
    if waitForComplete(response, url+response.json()['id']) == 1:
        return 1
    else:
        return 0

def startStopMldHostNgpf(protocolSessionUrl, action='start'):
    # For IPv6 only
    # 
    # protocolSessionUrl: Ex: http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/1/mldHost/1
    # action: start or stop
    #
    # http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork
    sessionUrl = protocolSessionUrl.split('/topology')[0]
    url = sessionUrl+'/topology/deviceGroup/ethernet/ipv6/mldHost/operations/%s' % action
    dataUrl = protocolSessionUrl.split('api')[1]
    data = {'arg1': [dataUrl]}
    urlHeadersJson = {'content-type': 'application/json'}
    print '\nstartStopMldHostNgpf: %s: %s' % (action, protocolSessionUrl)
    response = requests.post(url, data=json.dumps(data), headers=urlHeadersJson)
    if response.status_code != 202:
        return 1
    if waitForComplete(response, url+response.json()['id']) == 1:
        return 1
    else:
        return 0

def enableDisableIgmpGroupNgpf(protocolSessionUrl, groupRangeList, action='disable'):
    # protocolSessionUrl: http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1
    # groupRangeList: A list of multicast group range addresses to disable.
    #                        Example: ['225.0.0.1', '225.0.0.5']
    # action: disable or enable
    #
    # Description:
    #   To enable or disable specific multicast group range IP addresses by using 
    #   overlay.
    #
    # 1> Get a list of all the Multicast group range IP addresses.
    # 2> Get the multivalue list of ACTIVE STATE group ranges.
    # 3> Loop through the user list "groupRangeList" and look
    #    for the index position of the specified group range IP address.
    # 4> Using overlay to enable|disable the index value.
    #
    # Note: If an overlay is not created, then create one by:
    #       - Creating a "ValueList" for overlay pattern.
    #       - And add an Overlay.
    #
    # Return 0 if success
    # Return 1 if failed

    if action == 'disable':
        enableDisable = 'false'
    else:
        enableDisable = 'true'

    httpHeader = protocolSessionUrl.split('/api')[0]
    urlHeadersJson = {'content-type': 'application/json'}

    url = protocolSessionUrl+'/igmpMcastIPv4GroupList'
    response = requests.get(url)
    if response.status_code != 200:
        return 1
    # /api/v1/sessions/1/ixnetwork/multivalue/59

    # Get startMcastAddr multivalue to get a list of all the configured Group Range IP addresses.
    groupRangeAddressMultivalue = response.json()['startMcastAddr']
    # Get the active multivalue to do the overlay on top of.
    activeMultivalue = response.json()['active']

    # Getting the list of Group Range IP addresses.
    response = requests.get(httpHeader+groupRangeAddressMultivalue)
    if response.status_code != 200:
        return 1

    # groupRangeValues are multicast group ranges:
    # [u'225.0.0.1', u'225.0.0.2', u'225.0.0.3', u'225.0.0.4', u'225.0.0.5']
    groupRangeValues = response.json()['values']
    print '\nConfigured groupRangeValues:', groupRangeValues
    
    listOfIndexesToDisable = []
    # Loop through user list of specified group ranges to disable.
    for groupRangeIp in groupRangeList:
        index = groupRangeValues.index(groupRangeIp)
        listOfIndexesToDisable.append(index)
    
    if listOfIndexesToDisable == []:
        print '\ndisableIgmpGroupNgpf Error: No multicast group range ip address found on your list'
        return 1
    
    for index in listOfIndexesToDisable:
        currentOverlayUrl = httpHeader+activeMultivalue+'/overlay'
        # http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/multivalue/5/overlay
        # NOTE:  Index IS NOT zero based.
        print 'enableDisableIgmpGroupNgpf: %s: %s' % (action, groupRangeValues[index]) 
        response = requests.post(currentOverlayUrl, 
                                 data=json.dumps({'index': index+1, 'value': enableDisable}),
                                 headers=urlHeadersJson)
        if response.status_code != 201:
            return 1
    
    return 0

def enableDisableMldGroupNgpf(protocolSessionUrl, groupRangeList, action='disable'):
    # For IPv6 only
    #
    # protocolSessionUrl: http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1
    # groupRangeList: A list of multicast group range addresses to disable.
    #                        Example: ['ff03::1', 'ff03::2']
    # action: disable or enable
    #
    # Description:
    #   To enable or disable specific multicast group range IP addresses by using 
    #   overlay.
    #
    # 1> Get a list of all the Multicast group range IP addresses.
    # 2> Get the multivalue list of ACTIVE STATE group ranges.
    # 3> Loop through the user list "groupRangeList" and look
    #    for the index position of the specified group range IP address.
    # 4> Using overlay to enable|disable the index value.
    #
    # Note: If an overlay is not created, then create one by:
    #       - Creating a "ValueList" for overlay pattern.
    #       - And add an Overlay.
    #
    # Return 0 if success
    # Return 1 if failed

    if action == 'disable':
        enableDisable = 'false'
    else:
        enableDisable = 'true'

    httpHeader = protocolSessionUrl.split('/api')[0]
    urlHeadersJson = {'content-type': 'application/json'}

    #url = protocolSessionUrl+'/igmpMcastIPv4GroupList'
    url = protocolSessionUrl+'/mldMcastIPv6GroupList'
    response = requests.get(url)
    if response.status_code != 200:
        return 1
    # /api/v1/sessions/1/ixnetwork/multivalue/59

    # Get startMcastAddr multivalue to get a list of all the configured Group Range IP addresses.
    groupRangeAddressMultivalue = response.json()['startMcastAddr']
    # Get the active multivalue to do the overlay on top of.
    activeMultivalue = response.json()['active']

    # Getting the list of Group Range IP addresses.
    response = requests.get(httpHeader+groupRangeAddressMultivalue)
    if response.status_code != 200:
        return 1

    # groupRangeValues are multicast group ranges:
    # ['ff03::1', 'ff03::2']
    groupRangeValues = response.json()['values']
    print '\nConfigured groupRangeValues:', groupRangeValues
    
    listOfIndexesToDisable = []
    # Loop through user list of specified group ranges to disable.
    for groupRangeIp in groupRangeList:
        index = groupRangeValues.index(groupRangeIp)
        listOfIndexesToDisable.append(index)
    
    if listOfIndexesToDisable == []:
        print '\ndisableMldGroupNgpf Error: No multicast group range ip address found on your list'
        return 1
    
    for index in listOfIndexesToDisable:
        currentOverlayUrl = httpHeader+activeMultivalue+'/overlay'
        # http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/multivalue/5/overlay
        # NOTE:  Index IS NOT zero based.
        print 'enableDisableMldGroupNgpf: %s: %s' % (action, groupRangeValues[index]) 
        response = requests.post(currentOverlayUrl, 
                                 data=json.dumps({'index': index+1, 'value': enableDisable}),
                                 headers=urlHeadersJson)
        if response.status_code != 201:
            return 1
    
    return 0

def sendIgmpJoinNgpf_backup(sessionUrl, multicastIpAddress):
    # This API will send IGMP join.
    # If multicastIpAddress is 'all', this will send IGMP join on all multicast addresses.
    # Else, provide a list of multicast IP addresses to send join.
    # 
    # sessionUrl: 'http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1'
    # multicastIpAddress: 'all' or a list of multicast IP addresses to send joins
    #                      Example: ['225.0.0.3', '225.0.0.4']

    httpHeader = sessionUrl.split('/api')[0]
    jsonHeader = {'content-type': 'application/json'}
    
    # 1> Based on the list of multicastIpAddress, get all their indexes.
    response = requests.get(sessionUrl+'/igmpMcastIPv4GroupList')
    if response.status_code != 200:
        return 1
    startMcastAddrMultivalue = response.json()['startMcastAddr']
    
    response = requests.get(httpHeader+startMcastAddrMultivalue)
    if response.status_code != 200:
        return 1
    listOfConfiguredMcastIpAddresses = response.json()['values']
    print '\nsendIgmpJoinNgpf: List of configured Mcast IP addresses:', listOfConfiguredMcastIpAddresses
    if listOfConfiguredMcastIpAddresses == []:
        print 'sendIgmpJoinNgpf: No Mcast IP address configured'
        return 1

    if multicastIpAddress == 'all':
        listOfMcastAddresses = listOfConfiguredMcastIpAddresses
    else:
        listOfMcastAddresses = multicastIpAddress

    # Note: Index position is not zero based.
    indexListToSend = []
    for eachMcastAddress in listOfMcastAddresses:
        index = listOfConfiguredMcastIpAddresses.index(eachMcastAddress)
        indexListToSend.append(index+1)

    url = sessionUrl+'/igmpMcastIPv4GroupList/operations/igmpjoingroup'
    data = {'arg1': [sessionUrl+'/igmpMcastIPv4GroupList'], 'arg2': indexListToSend}

    print '\nsendIgmpJoinNgpf:', url
    print '\t', multicastIpAddress
    response = requests.post(url, data=json.dumps(data), headers=jsonHeader)
    if response.status_code != 202:
        return 1
    if waitForComplete(response, url+response.json()['id']) == 1:
        return 1
    else:
        return 0

def sendIgmpJoinOrLeaveNgpf(**kwargs):
    # This API will send IGMP joins or leaves.
    # 
    # If groupRangeList or sourceRangeList is 'all', this will send IGMP join
    # on all configured multicast addresses.
    # Else, provide a list of group range IP addresses to send join or leave.
    # 
    # MANDATORY PARAMETERS:
    #    protocolObject or sessionUrl
    #    groupRangeList or sourcRangeList
    #    action (join or leave)
    # 
    # OPTIONAL PARAMETERS:
    #    portName
    #    hostIp
    #
    # PARAMETER DEFINITIONS:
    #    action:          State join or leave.
    #
    #    protocolObject:  The igmpHost object to send joins|leaves.
    #
    #    sessionUrl:      This is the session ID: 'http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork'.
    #                     If you want this API to dynamically figure out the igmp host
    #                     object based on hostIp or portName, then use sessionUrl 
    #                     because this API needs to know your REST API server:port and the connected session ID.
    #
    #    groupRangeList:  State 'all' or a list of mcast group range ip addresses to send joins|leaves.
    # 
    #    sourceRangeList: State 'all' or a list of mcast source group ip addresses to send joins|leaves.
    # 
    #    hostIp:          Dynamically get the igmpHost object based on the provided host IP address.
    #
    #    portName:        Dynamically get the igmpHost object based on the provided host IP address.
    #
    # USAGE: SELECT A METHOD
    # 
    #    1> protocolObject + action + groupRangeList or sourceRangeList
    #    2> sessionUrl  + action + portName + mcastGroupRangeList or sourceRangeList
    #    3> sessionUrl  + action + hostIp   + mcastGroupRangeList or sourceRangeList
    #    4> sessionUrl  + action + hostIp   + portName + mcastGroupRangeList or sourceRangeList
    #       (About #4: Include a portName to handle VPN configurations if the 
    #        same IP address is on multiple ports.)
    # 
    # EXAMPLE #1:
    #    Provide a known IGMP host object:
    #    sendIgmpJoinOrLeaveNgpf(protocolObject='http://x.x.x.x:11009/api/v1/.../topology/1/.../ipv4/1/igmpHost/1', 
    #                            groupRangeList=['225.0.0.2', '255.0.0.4'],
    #                            action='join')
    #
    # All examples below will search for the corresponding igmpHost 
    # object based on hostIp or portName.
    #
    # EXAMPLE #2:
    #    sendIgmpJoinOrLeaveNgpf(sessionUrl='http://192.168.70.127:11009',
    #                            portName='my port1', 
    #                            groupRangeList='all',
    #                            action='leave')
    #
    # EXAMPLE #3:
    #    sendIgmpJoinOrLeaveNgpf(sessionUrl='http://192.168.70.127:11009',
    #                            hostIp='1.1.1.1', 
    #                            groupRangeList=['225.0.0.2', '255.0.0.4'],
    #                            action='join')
    #
    # EXAMPLE #4:
    #    This is similar to the above, with an addition of providing a portName for filtering.
    #    In a scenario such as VPN where multiple ports have the same IP, this API uses the portName
    #    as a filter to distinguish which multicast IP address to send joins or leaves.
    #    sendIgmpJoinOrLeaveNgpf(sessionUrl='http://192.168.70.127:11009',
    #                            hostIp='my 1.1.1.1',
    #                            portName='my port1', 
    #                            groupRangeList=['225.0.0.2', '255.0.0.4'],
    #                            action='leave')
    
    if 'protocolObject' not in kwargs and 'sessionUrl' not in kwargs:
        print '\nError: You must provide one of the followings: protocolObject or sessionUrl'
        print 'Please read the API description for usage.'
        return 1

    if 'protocolObject' in kwargs:
        httpHeader = kwargs['protocolObject'].split('/api')[0]

    if 'sessionUrl' in kwargs:
        import re
        # Do some error checking and grab the serverIp:socket
        serverUrlMatch = re.match('(http://[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+)/api/v1/sessions/[0-9]+/ixnetwork$', kwargs['sessionUrl'])
        if serverUrlMatch:
            httpHeader = serverUrlMatch.group(1)
        else:
            print '\nError: sessionUrl parameter should be: http://<serverIp>:socketPort/api/v1/sessions/<sessionId>/ixnetwork'
            print 'You entered:', kwargs['sessionUrl']
            return 1

    if 'action' not in kwargs:
        print '\nError: You must include the "action" parameter and state join or leave'
        return 1
    
    if kwargs['action'] == 'join':
        sendAction = 'igmpjoingroup'
    if kwargs['action'] == 'leave':
        sendAction = 'igmpleavegroup'

    if 'groupRangeList' in kwargs and 'sourceRangeList' in kwargs:
        print '\nError: Please select either groupRangeList or sourceRangeList. Not both.'
        return 1

    if 'groupRangeList' not in kwargs and 'sourceRangeList' not in kwargs:
        print '\nError: It is mandatory to provide either groupRangeList or sourceRangeList.'
        return 1

    jsonHeader = {'content-type': 'application/json'}
    igmpHostSessionUrlList = []

    # 'portName' logics:
    #     Get a list of Topologies
    #     Get a list of vports
    #     Match portName with vport's name
    #     If found, look for matching mcastGroupRangeList:
    #        Use the topology object and:
    #        Get a list of ipv4
    #        Get a list of igmpHost objects (This becomes the current sessionUrl).

    if 'portName' in kwargs or 'hostIp' in kwargs:
        response = requests.get(kwargs['sessionUrl']+'/topology')
        topologyList = ['%s/%s/%s' % (kwargs['sessionUrl'], 'topology', str(i["id"])) for i in response.json()]
        for topology in topologyList:
            response = requests.get(topology)
            if response.status_code != 200:
                return 1
            vportList = response.json()['vports']
            if vportList == []:
                print 'Error: No vport is created'
                return 1
            for vport in vportList:
                response = requests.get(httpHeader+vport)
                if response.status_code != 200:
                    print 'Error: Get vport status code:', response.status_code
                    return 1
                currentVportName = response.json()['name']
                response = requests.get(topology+'/deviceGroup')
                deviceGroupList = ['%s/%s/%s' % (topology, 'deviceGroup', str(i["id"])) for i in response.json()]
                for deviceGroup in deviceGroupList:
                    response = requests.get(deviceGroup+'/ethernet')
                    ethernetList = ['%s/%s/%s' % (deviceGroup, 'ethernet', str(i["id"])) for i in response.json()]
                    for ethernet in ethernetList:
                        response = requests.get(ethernet+'/ipv4')
                        configuredIpv4ObjList = ['%s/%s/%s' % (ethernet, 'ipv4', str(i["id"])) for i in response.json()]
                        response = requests.get(ethernet+'/ipv6')
                        configuredIpv6ObjList = ['%s/%s/%s' % (ethernet, 'ipv6', str(i["id"])) for i in response.json()]

                        for layer3IpObj in (configuredIpv4ObjList + configuredIpv6ObjList):
                            response = requests.get(layer3IpObj)
                            if response.status_code != 200:
                                print 'Error: GET:', layer3IpObj
                                print 'Error: Status code failed', response.status_code
                                return 1
                            currentIpAddrMultivalue = response.json()['address']
                            response = requests.get(httpHeader + currentIpAddrMultivalue)
                            if response.status_code != 200:
                                print 'Error: GET:', layer3IpObj
                                print 'Error: Status code failed:', response.status_code
                                return 1
                            configuredIpAddresses = response.json()['values']
                            if 'hostIp' in kwargs and kwargs['hostIp'] not in configuredIpAddresses:
                                continue
                            response = requests.get(layer3IpObj+'/igmpHost')
                            if response.status_code != 200:
                                # Ignore status code failures here because it is expected that
                                # not all layer3 objects have igmpHost configured.
                                continue
                            foreachHostObj = response.json()[0]['links'][0]['href']
                            if 'igmpHost' in foreachHostObj:
                                # Scenario #1:  Based on portName only
                                if ('portName' in kwargs and
                                    'hostIp' not in kwargs and
                                    kwargs['portName'] == currentVportName):
                                    igmpHostSessionUrlList.append(httpHeader + foreachHostObj)

                                # Scenario #2:  Based on hostIp only
                                if ('hostIp' in kwargs and
                                    'portName' not in kwargs
                                    and kwargs['hostIp'] in configuredIpAddresses):
                                    igmpHostSessionUrlList.append(httpHeader + foreachHostObj)

                                # Scenario #3:  Based on hostIp & portName (VPN handlings)
                                if ('hostIp' in kwargs and
                                    'portName' in kwargs and
                                    kwargs['portName'] == currentVportName and
                                    kwargs['hostIp'] in configuredIpAddresses):
                                    igmpHostSessionUrlList.append(httpHeader + foreachHostObj)

        if igmpHostSessionUrlList == []:
            print 'Error: No IGMP host object found.'
            return 1
        protocolHostObj = igmpHostSessionUrlList[0]
        
    if 'protocolObject' in kwargs:
        protocolHostObj = kwargs['protocolObject']
    
    # Logic:
    #     - Get igmpHost object.
    #     - Get its list of configured mcast:
    #          - groupRange IP addresses.
    #          - incrementing steps.
    #          - total count.
    #     - Match user defined groupRangeList with listOfConfiguredMcastIpAddresses
    #       to get all the indexes.
    #     - Send join|leave using igmpHost object with list of indexes.

    response = requests.get(protocolHostObj)
    if response.status_code != 200:
        return 1
    if response.json()['sessionStatus'][0] == 'notStarted':
        print 'Error: IGMP protocol is not started. Cannot send joins|leaves'
        return 1

    # 1> Based on the list of groupRangeList, get all their indexes.
    if 'groupRangeList' in kwargs:
        response = requests.get(protocolHostObj+'/igmpMcastIPv4GroupList')
        if response.status_code != 200:
            return 1
        startAddrMultivalue = response.json()['startMcastAddr']
        incrAddrMultivalue = response.json()['mcastAddrIncr']
        addrCntMultivalue = response.json()['mcastAddrCnt']

    if 'sourceRangeList' in kwargs:
        response = requests.get(protocolHostObj+'/igmpMcastIPv4GroupList/igmpUcastIPv4SourceList')
        if response.status_code != 200:
            return 1
        startAddrMultivalue = response.json()['startUcastAddr']
        incrAddrMultivalue = response.json()['ucastAddrIncr']
        addrCntMultivalue = response.json()['ucastSrcAddrCnt']

    response = requests.get(httpHeader + startAddrMultivalue)
    if response.status_code != 200:
        return 1

    listOfConfiguredMcastIpAddresses = response.json()['values']
    #print '\nsendIgmpJoinNgpf: List of configured Mcast IP addresses:', listOfConfiguredMcastIpAddresses
    if listOfConfiguredMcastIpAddresses == []:
        print 'sendIgmpJoinNgpf: No Mcast IP address configured'
        return 1    

    try:
        if 'groupRangeList' in kwargs and kwargs['groupRangeList'] == 'all':
            listOfMcastAddresses = listOfConfiguredMcastIpAddresses
        else:
            listOfMcastAddresses = kwargs['groupRangeList']
    except:
        pass

    try:
        if 'sourceRangeList' in kwargs and kwargs['sourceRangeList'] == 'all':
            listOfMcastAddresses = listOfConfiguredMcastIpAddresses
        else:
            listOfMcastAddresses = kwargs['sourceRangeList']
    except:
        pass

    indexListToSend = []
    for eachMcastAddress in listOfMcastAddresses:
        try:
            index = listOfConfiguredMcastIpAddresses.index(eachMcastAddress)
            # Note: Index position is not zero based.
            indexListToSend.append(index+1)
        except:
            print '\nsendIgmpJoinNgpf: Error: The multicast IP address that you provided is not a configured address:', eachMcastAddress
            return 1

    # Get the multicast group increment
    response = requests.get(httpHeader + incrAddrMultivalue)
    if response.status_code != 200:
        return 1
    mcastIncrValueList = response.json()['values']

    # Get the multicast group total count
    response = requests.get(httpHeader + addrCntMultivalue)
    if response.status_code != 200:
        return 1
    mcastGroupCountValueList = response.json()['values']

    if sendAction == 'igmpjoingroup':
        igmpSend = 'join'
    else:
        igmpSend = 'leave'

    print '\nSending IGMP %s on:' % igmpSend
    for index in indexListToSend:
        groupIp = listOfConfiguredMcastIpAddresses[index-1]
        incrStep    = mcastIncrValueList[index-1]
        # The total number of mcast IP address count
        groupIpAddrCount  = mcastGroupCountValueList[index-1]

        # Write some logic to get the last group IP address for display
        convertIncrStepToList  = incrStep.split('.')

        try:
            # Look for the index position of '1' in '0.0.0.1'
            incrStepIndex = convertIncrStepToList.index('1')
            convertGroupIpToList = groupIp.split('.')
            ipOctetToIncrement = convertGroupIpToList[incrStepIndex]

            lastOctetGroupIpAddress = int(ipOctetToIncrement) + int(groupIpAddrCount)-1
            convertGroupIpToList[incrStepIndex] = str(lastOctetGroupIpAddress)
            lastGroupIpAddress = '.'.join(convertGroupIpToList)
        except:
            lastGroupIpAddress = groupIp

        print '\tmcastGroupAddress={groupIp}  step={incrStep}  groupAddressCount={groupIpAddrCount}  lastgroupIp={lastGroupIp}'.format(
            groupIp=groupIp,
            incrStep=incrStep,
            groupIpAddrCount=groupIpAddrCount,
            lastGroupIp=lastGroupIpAddress
        )
        
    url = protocolHostObj+'/igmpMcastIPv4GroupList/operations/%s' % sendAction
    if indexListToSend != []:
        data = {'arg1': [protocolHostObj+'/igmpMcastIPv4GroupList'], 'arg2': indexListToSend}
        print '\nURL:', url
        print '\nDATA:', data
        response = requests.post(url, data=json.dumps(data), headers=jsonHeader)
        if response.status_code != 202:
            return 1
        if waitForComplete(response, url+response.json()['id']) == 1:
            return 1
        else:
            return 0



def sendIgmpJoinNgpf_backup(sessionUrl, multicastIpAddress):
    # This API will send IGMP join.
    # If multicastIpAddress is 'all', this will send IGMP join on all multicast addresses.
    # Else, provide a list of multicast IP addresses to send join.
    # 
    # sessionUrl: 'http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1'
    # multicastIpAddress: 'all' or a list of multicast IP addresses to send joins
    #                      Example: ['225.0.0.3', '225.0.0.4']

    httpHeader = sessionUrl.split('/api')[0]
    jsonHeader = {'content-type': 'application/json'}
    
    # 1> Based on the list of multicastIpAddress, get all their indexes.
    response = requests.get(sessionUrl+'/igmpMcastIPv4GroupList')
    if response.status_code != 200:
        return 1
    startMcastAddrMultivalue = response.json()['startMcastAddr']
    
    response = requests.get(httpHeader+startMcastAddrMultivalue)
    if response.status_code != 200:
        return 1
    listOfConfiguredMcastIpAddresses = response.json()['values']
    print '\nsendIgmpJoinNgpf: List of configured Mcast IP addresses:', listOfConfiguredMcastIpAddresses
    if listOfConfiguredMcastIpAddresses == []:
        print 'sendIgmpJoinNgpf: No Mcast IP address configured'
        return 1

    if multicastIpAddress == 'all':
        listOfMcastAddresses = listOfConfiguredMcastIpAddresses
    else:
        listOfMcastAddresses = multicastIpAddress

    # Note: Index position is not zero based.
    indexListToSend = []
    for eachMcastAddress in listOfMcastAddresses:
        index = listOfConfiguredMcastIpAddresses.index(eachMcastAddress)
        indexListToSend.append(index+1)

    url = sessionUrl+'/igmpMcastIPv4GroupList/operations/igmpjoingroup'
    data = {'arg1': [sessionUrl+'/igmpMcastIPv4GroupList'], 'arg2': indexListToSend}

    print '\nsendIgmpJoinNgpf:', url
    print '\t', multicastIpAddress
    response = requests.post(url, data=json.dumps(data), headers=jsonHeader)
    if response.status_code != 202:
        return 1
    if waitForComplete(response, url+response.json()['id']) == 1:
        return 1
    else:
        return 0

def sendIgmpLeaveNgpf(sessionUrl, multicastIpAddress):
    # This API will send IGMP leaves.
    # If multicastIpAddress is 'all', this will send IGMP leaves on all multicast addresses.
    # Else, provide a list of multicast IP addresses to send leaves.
    # 
    # sessionUrl: 'http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1'
    # multicastIpAddress: 'all' or a list of multicast IP addresses to send leaves
    #                      Example: ['225.0.0.3', '225.0.0.4']

    httpHeader = sessionUrl.split('/api')[0]
    jsonHeader = {'content-type': 'application/json'}
    
    # 1> Based on the list of multicastIpAddress, get all their indexes.
    response = requests.get(sessionUrl+'/igmpMcastIPv4GroupList')
    if response.status_code != 200:
        return 1
    startMcastAddrMultivalue = response.json()['startMcastAddr']
    
    response = requests.get(httpHeader+startMcastAddrMultivalue)
    if response.status_code != 200:
        return 1
    listOfConfiguredMcastIpAddresses = response.json()['values']
    print '\nsendIgmpLeaveNgpf: List of configured Mcast IP addresses:', listOfConfiguredMcastIpAddresses
    if listOfConfiguredMcastIpAddresses == []:
        print 'sendIgmpLeaveNgpf: No Mcast IP address configured'
        return 1

    if multicastIpAddress == 'all':
        listOfMcastAddresses = listOfConfiguredMcastIpAddresses
    else:
        listOfMcastAddresses = multicastIpAddress

    # Note: Index position is not zero based.
    indexListToSend = []
    for eachMcastAddress in listOfMcastAddresses:
        index = listOfConfiguredMcastIpAddresses.index(eachMcastAddress)
        indexListToSend.append(index+1)

    url = sessionUrl+'/igmpMcastIPv4GroupList/operations/igmpleavegroup'
    data = {'arg1': [sessionUrl+'/igmpMcastIPv4GroupList'], 'arg2': indexListToSend}

    print '\nsendIgmpLeaveNgpf:', url
    print '\t', multicastIpAddress
    response = requests.post(url, data=json.dumps(data), headers=jsonHeader)
    if response.status_code != 202:
        return 1
    if waitForComplete(response, url+response.json()['id']) == 1:
        return 1
    else:
        return 0
    
def sendPimV4JoinNgpf(sessionUrl):
    # sessionUrl: The pimV4Interace object.
    #    Example: http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/pimV4Interface/2

    url = sessionUrl+'/pimV4JoinPruneList/operations/join'

    # data = {'arg1': [A list of /api/v1/.../topology/1/.../pimV4Interface/<number>/pimV4JoinPruneList]}
    #    ['/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/pimV4Interface/2/pimV4JoinPruneList']}
    pimV4InterfacePath = sessionUrl.split('/api')[1]
    data = {'arg1': [pimV4InterfacePath+'/pimV4JoinPruneList']}
    urlHeadersJson = {'content-type': 'application/json'}

    print '\nsendPimV4JoinNgpf:', url
    response = requests.post(url, data=json.dumps(data), headers=urlHeadersJson)
    if response.status_code != 202:
        return 1
    if waitForComplete(response, url+response.json()['id']) == 1:
        return 1
    else:
        return 0

def sendPimV4LeaveNgpf(sessionUrl):
    # sessionUrl: The pimV4Interace object.
    #    Example: http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/pimV4Interface/2

    url = sessionUrl+'/pimV4JoinPruneList/operations/leave'

    # data = {'arg1': [A list of /api/v1/.../topology/1/.../pimV4Interface/<number>/pimV4JoinPruneList]}
    #    ['/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/pimV4Interface/2/pimV4JoinPruneList']}
    pimV4InterfacePath = sessionUrl.split('/api')[1]
    data = {'arg1': [pimV4InterfacePath+'/pimV4JoinPruneList']}
    urlHeadersJson = {'content-type': 'application/json'}

    print '\nsendPimV4LeaveNgpf:', url
    response = requests.post(url, data=json.dumps(data), headers=urlHeadersJson)
    if response.status_code != 202:
        return 1
    if waitForComplete(response, url+response.json()['id']) == 1:
        return 1
    else:
        return 0

def sendMldJoinNgpf(sessionUrl, ipv6AddressList):
    # For IPv6 only
    #
    # This API will take the mld sessionUrl object and loop through all the configured ports
    # looking for the specified ipv6Address to send a join.
    # 
    # sessionUrl: http://192.168.70.127.:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1
    # ipv6AddressList: 'all' or a list of IPv6 addresses that must be EXACTLY how it is configured on the GUI.

    httpHeader = sessionUrl.split('/api')[0]
    jsonHeader = {'content-type': 'application/json'}

    # Loop all port objects to get user specified IPv6 address to send the join.
    portObjectList = sessionUrl+'/mldMcastIPv6GroupList/port'
    response = requests.get(portObjectList)
    if response.status_code != 200:
        return

    for eachPortIdDetails in response.json():
        currentPortId = eachPortIdDetails['id']
        # For each ID, get the 'startMcastAddr' multivalue
        startMcastAddrMultivalue = eachPortIdDetails['startMcastAddr']

        # Go to the multivalue and get the 'values'
        response = requests.get(httpHeader+startMcastAddrMultivalue)
        if response.status_code != 200:
            return 1

        listOfConfiguredGroupIpAddresses = response.json()['values']
        if ipv6AddressList == 'all':
            listOfGroupAddresses = listOfConfiguredGroupIpAddresses
        else:
            listOfGroupAddresses = ipv6AddressList

        for eachSpecifiedIpv6Addr in listOfGroupAddresses:
            if eachSpecifiedIpv6Addr in listOfConfiguredGroupIpAddresses:
                # if 'values' match ipv4Address, do a join on: 
                #      http://192.168.70.127.:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1/mldMcastIPv6GroupList/port/1/operations/mldjoingroup
                #    arg1: port/1 object
                url = sessionUrl+'/mldMcastIPv6GroupList/port/%s/operations/mldjoingroup' % currentPortId
                portIdObj = sessionUrl+'/mldMcastIPv6GroupList/port/%s' % currentPortId
                # portIdObj = http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1/mldMcastIPv6GroupList/port/1
                response = requests.post(url, data=json.dumps({'arg1': [portIdObj]}), headers=jsonHeader)
                if response.status_code != 202:
                    return 1
                if waitForComplete(response, url+response.json()['id']) == 1:
                    return 1
                else:
                    return 0

    return 0

def sendMldLeaveNgpf(sessionUrl, ipv6AddressList):
    # For IPv6 only
    #
    # This API will take the mld sessionUrl object and loop through all the configured ports
    # looking for the specified ipv6Address to send a leave.
    # 
    # sessionUrl: http://192.168.70.127.:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1
    # ipv6AddressList: 'all' or a list of IPv6 addresses that must be EXACTLY how it is configured on the GUI.

    httpHeader = sessionUrl.split('/api')[0]
    jsonHeader = {'content-type': 'application/json'}

    # Loop all port objects to get user specified IPv6 address to send the leave.
    portObjectList = sessionUrl+'/mldMcastIPv6GroupList/port'
    response = requests.get(portObjectList)
    if response.status_code != 200:
        return

    for eachPortIdDetails in response.json():
        currentPortId = eachPortIdDetails['id']
        # For each ID, get the 'startMcastAddr' multivalue
        startMcastAddrMultivalue = eachPortIdDetails['startMcastAddr']

        # Go to the multivalue and get the 'values'
        response = requests.get(httpHeader+startMcastAddrMultivalue)
        if response.status_code != 200:
            return 1

        listOfConfiguredGroupIpAddresses = response.json()['values']
        if ipv6AddressList == 'all':
            listOfGroupAddresses = listOfConfiguredGroupIpAddresses
        else:
            listOfGroupAddresses = ipv6AddressList

        for eachSpecifiedIpv6Addr in listOfGroupAddresses:
            if eachSpecifiedIpv6Addr in listOfConfiguredGroupIpAddresses:
                # if 'values' match ipv4Address, do a join on: 
                #      http://192.168.70.127.:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1/mldMcastIPv6GroupList/port/1/operations/mldjoingroup
                #    arg1: port/1 object
                url = sessionUrl+'/mldMcastIPv6GroupList/port/%s/operations/mldleavegroup' % currentPortId
                portIdObj = sessionUrl+'/mldMcastIPv6GroupList/port/%s' % currentPortId
                # portIdObj = http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1/mldMcastIPv6GroupList/port/1
                response = requests.post(url, data=json.dumps({'arg1': [portIdObj]}), headers=jsonHeader)
                if response.status_code != 202:
                    return 1
                if waitForComplete(response, url+response.json()['id']) == 1:
                    return 1
                else:
                    return 0

    return 0

def prettyPrintAllOperations(sessionUrl, searchPath='/operations'):
    # Dispaly all the operation commands and its description:
    #    http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/operations

    #response = requests.get(sessionUrl+'/operations')
    response = requests.get(sessionUrl+searchPath)
    for item in response.json():
        if 'operation' in item.keys():
            print '\n', item['operation']
            print '\t%s' % item['description']
            if 'args' in item.keys():
                for nestedKey,nestedValue in item['args'][0].items():
                    print '\t\t%s: %s' % (nestedKey, nestedValue)

ixNetUrl = "http://"+py.ixTclServer+":"+str(py.ixRestPort)+"/api/v1"
sessionUrl = ixNetUrl+'/sessions/1/ixnetwork'
serverUrl = 'http://'+py.ixTclServer+':'+str(py.ixRestPort)

# Uncomment this if you want to reassign ports
#if assignPorts(sessionUrl, portList) == 1:
#    sys.exit()

'''
sendIgmpJoinOrLeaveNgpf(protocolObject='http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1', 
                        groupRangeList=['225.0.0.2', '225.0.0.4'],
                        action='leave')

sys.exit()
'''

'''
sendIgmpJoinOrLeaveNgpf(sessionUrl=sessionUrl,
                        portName='my port1', 
                        groupRangeList='all',
                        action='join')
sys.exit()
'''

'''
sendIgmpJoinOrLeaveNgpf(sessionUrl=sessionUrl,
                        hostIp='1.1.1.1', 
                        groupRangeList=['225.0.0.2', '225.0.0.4'],
                        action='leave')
'''

'''
sendIgmpJoinOrLeaveNgpf(sessionUrl=sessionUrl,
                        hostIp='1.1.1.1',
                        portName='my port1', 
                        groupRangeList='all',
                        action='join')
sys.exit()
'''

sendIgmpJoinOrLeaveNgpf(sessionUrl=sessionUrl,
                        portName='my port1', 
                        sourceRangeList='all',
                        action='join')

#x enableDisableIMld
#x Join/leave mld: simple join/leave for mld with only group specified
#     Source Group specific join/leave: igmp, mld, and pim
#  Join | Leave: 
#     1> By portName
#     2> By host IP address
#           Scenario #1: Host IP
#           Scenario #2: Handle same host IP on multiple ports (VPN). Must filter by port parameter.
#     3> Display the Group Range, Increment=#, and Last Group IP Address.
#     4> Source Group join|leave 
# 
#  Pim: join, prune
#x  Igmp stats
#x  Mld stats
#x  Pim stats

#sendMldJoinNgpf('http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1', ['ff03::1'])
#sendMldJoinNgpf('http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1', 'all')

#sendMldLeaveNgpf('http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1', ['ff03::1'])
#sendMldLeaveNgpf('http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1', 'all')

#sendPimV4JoinNgpf('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/pimV4Interface/2')

#prettyPrintAllOperations(sessionUrl, searchPath='/topology/deviceGroup/ethernet/ipv4/pimV4Interface/operations')
#prettyPrintAllOperations(sessionUrl, searchPath='/operations')


#startStopIgmpHostNgpf('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1', action='stop')

#stopIgmpHost('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1')

#startStopPimV4InterfaceNgpf('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/pimV4Interface/2', action='stop')

#startStopMldHostNgpf('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/ml#dHost/1', action='stop')

#enableDisableIgmpGroupRangeNgpf('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1',
#                                groupRangeList=['225.0.0.1', '225.0.0.5'],
#                                action='enable')

#enableDisableMldGroupNgpf('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv6/2/mldHost/1',
#                          groupRangeList=['ff03::1', 'ff03::1'],
#                          action='disable')

#sendIgmpJoinOrLeaveNgpf('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1', ['225.0.0.2', '225.0.0.4'])
#sendIgmpJoinOrLeaveNgpf('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1', 'all')

#sendIgmpLeaveNgpf('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1', ['225.0.0.2', '225.0.0.4'])
#sendIgmpLeaveNgpf('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1', 'all')

#verifyAllProtocolSessionsNgpf(sessionUrl)
#verifyProtocolSessions(['http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1'])

sys.exit()
#enableDisableBgpFlap('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bgpIpv4Peer/1',
#                     action='false',
#                     upTimeInSec=3,
#                     downTimeInSec=4)

    
#stats = getStats(sessionUrl, csvFile='Flow_Statistics', csvEnableFileTimestamp=False)


if verifyPortState(sessionUrl) == 1:
    sys.exit()

if startAllProtocols(sessionUrl) == 1:
    sys.exit()

if verifyAllProtocolSessionsNgpf(sessionUrl, timeout=120) == 1:
    sys.exit()

if regenerateAllTrafficItems(sessionUrl) == 1:
    sys.exit()

if applyTraffic(sessionUrl) == 1:
    sys.exit()

if startTraffic(sessionUrl) == 1:
    sys.exit()

time.sleep(10)

stats = getStats(sessionUrl, viewName='Flow Statistics')
print printDict(stats)

print '--- tx frames:', stats[16]['Tx Frames']



















