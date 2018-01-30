#!/usr/local/python2.7.6/bin/python2.7

import requests, json, sys, os, time

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

def getVportMapping(portNumber):
    # Search all vport for the port number.
    # Port format = 1/1/1.  Not 1/1.
    for vport in vportList:
        # connectedTo = /api/v1/sessions/1/ixnetwork/availableHardware/chassis/1/card/1/port/1
        response = requests.get(vport)
        connectedTo = response.json()["connectedTo"]
        chassisId = connectedTo.split("/")[8]
        card = connectedTo.split("/")[10]
        portNum = connectedTo.split("/")[12]
        port = chassisId+"/"+card+"/"+portNum
        if port == portNumber:
            print "\nReturing vport:", vport
            return vport

def verifyProtocolSessionsNgpf(protocolObjList, timeout=90):
    # Verify the user specified protocol list to verify for session UP.
    #
    # sessionUrl = http://10.219.x.x:11009/api/v1/sessions/1/ixnetwork
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

def regenerateAllTrafficItems(sessionUrl):
    # Performs regenerate on all enabled Traffic Items.
    # Requires API: waitForComplete.
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



root = "http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork"

serverUrl = "http://192.168.70.127:11009"

# Create blank configuration

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/operations/newconfig', data=json.dumps({}), headers={'content-type': 'application/json'})

waitForComplete(response, root+"/operations/newconfig/"+response.json()["id"])

# Create virtual ports

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/vport', data=json.dumps({}), headers={'content-type': 'application/json'})

# Create virtual ports

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/vport', data=json.dumps({}), headers={'content-type': 'application/json'})

response = requests.get('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/vport')

vportList = ["%s/vport/%s" % (root, str(i["id"])) for i in response.json()]

# Assign ports

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/operations/assignports', data=json.dumps({'arg1': [{'arg1': '192.168.70.10', 'arg2': '1', 'arg3': '1'}, {'arg1': '192.168.70.10', 'arg2': '2', 'arg3': '1'}], 'arg2': [], 'arg3': vportList, 'arg4': 'true'}), headers={'content-type': 'application/json'})

waitForComplete(response, root+"/operations/assignports/"+response.json()["id"])

[waitForComplete(requests.get(vport), vport) for vport in vportList]

# Create Topology

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology', data=json.dumps({}), headers={'content-type': 'application/json'})

topology1Vports = []

topology1Vports.append(getVportMapping("1/1/1"))

response = requests.patch('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1', data=json.dumps({'name': 'L2L3 Topo 1'}), headers={'content-type': 'application/json'})

response = requests.patch('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1', data=json.dumps({'vports': topology1Vports}), headers={'content-type': 'application/json'})

# Create Topology

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology', data=json.dumps({}), headers={'content-type': 'application/json'})

topology2Vports = []

topology2Vports.append(getVportMapping("1/2/1"))

response = requests.patch('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2', data=json.dumps({'name': 'L2L3 Topo 2'}), headers={'content-type': 'application/json'})

response = requests.patch('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2', data=json.dumps({'vports': topology2Vports}), headers={'content-type': 'application/json'})

# Create Device Group

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup', data=json.dumps({}), headers={'content-type': 'application/json'})

response = requests.patch('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1', data=json.dumps({'multiplier': 4}), headers={'content-type': 'application/json'})

response = requests.patch('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1', data=json.dumps({'name': 'T1DG1 DG1'}), headers={'content-type': 'application/json'})

# Create Device Group

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup', data=json.dumps({}), headers={'content-type': 'application/json'})

response = requests.patch('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1', data=json.dumps({'multiplier': 4}), headers={'content-type': 'application/json'})

response = requests.patch('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1', data=json.dumps({'name': 'T2DG1 DG1'}), headers={'content-type': 'application/json'})

# Create Ethernet

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet', data=json.dumps({}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1")

multiValue = response.json()['mac']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/counter", data=json.dumps({'start': '00:01:01:00:00:01', 'direction': 'increment', 'step': '00:00:00:00:00:01'}), headers={'content-type': 'application/json'})

response = requests.patch('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1', data=json.dumps({'name': 'TG1DG1 Eth1'}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1")

multiValue = response.json()['enableVlans']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/singleValue", data=json.dumps({'value': True}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1")

multiValue = response.json()['mtu']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/singleValue", data=json.dumps({'value': 1500}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/vlan/1")

multiValue = response.json()['priority']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/singleValue", data=json.dumps({'value': 7}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/vlan/1")

multiValue = response.json()['vlanId']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/counter", data=json.dumps({'start': 103, 'direction': 'increment', 'step': 1}), headers={'content-type': 'application/json'})

# Create Ethernet

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet', data=json.dumps({}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1")

multiValue = response.json()['mac']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/counter", data=json.dumps({'start': '00:01:03:00:00:01', 'direction': 'increment', 'step': '00:00:00:00:00:01'}), headers={'content-type': 'application/json'})

response = requests.patch('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1', data=json.dumps({'name': 'TG2DG1 Eth1'}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1")

multiValue = response.json()['enableVlans']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/singleValue", data=json.dumps({'value': True}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1")

multiValue = response.json()['mtu']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/singleValue", data=json.dumps({'value': 1500}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/vlan/1")

multiValue = response.json()['priority']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/singleValue", data=json.dumps({'value': 5}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/vlan/1")

multiValue = response.json()['vlanId']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/counter", data=json.dumps({'start': 103, 'direction': 'increment', 'step': 1}), headers={'content-type': 'application/json'})

# Create IPv4

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4', data=json.dumps({}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1")

multiValue = response.json()['resolveGateway']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/singleValue", data=json.dumps({'value': True}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1")

multiValue = response.json()['prefix']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/singleValue", data=json.dumps({'value': 24}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1")

multiValue = response.json()['gatewayIp']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/counter", data=json.dumps({'start': '100.1.1.100', 'direction': 'increment', 'step': '0.0.0.1'}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1")

multiValue = response.json()['address']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/counter", data=json.dumps({'start': '100.1.1.1', 'direction': 'increment', 'step': '0.0.0.1'}), headers={'content-type': 'application/json'})

# Create IPv4

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4', data=json.dumps({}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4/1")

multiValue = response.json()['resolveGateway']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/singleValue", data=json.dumps({'value': True}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4/1")

multiValue = response.json()['prefix']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/singleValue", data=json.dumps({'value': 24}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4/1")

multiValue = response.json()['gatewayIp']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/counter", data=json.dumps({'start': '100.1.1.1', 'direction': 'increment', 'step': '0.0.0.1'}), headers={'content-type': 'application/json'})

response = requests.get("http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4/1")

multiValue = response.json()['address']

response = requests.patch('http://192.168.70.127:11009'+multiValue+"/counter", data=json.dumps({'start': '100.1.1.100', 'direction': 'increment', 'step': '0.0.0.1'}), headers={'content-type': 'application/json'})

# Start All Protocols

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/operations/startallprotocols', data=json.dumps({}), headers={'content-type': 'application/json'})

verifyProtocolSessionsNgpf(['http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1', 'http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1', 'http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1', 'http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4/1'])

# Create Traffic Item
print '\nCreating traffic item with appLibrary ...'
response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/traffic/trafficItem',
                         data=json.dumps({'name': 'Topo1 to Topo2',
                                          'trafficType': 'ipv4ApplicationTraffic',
                                          'trafficItemType': 'applicationLibrary'}),
                         headers={'content-type': 'application/json'})

# Create Endpoints

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/endpointSet', data=json.dumps({'name': 'FlowGroup-1',
                                                                                                                                       'sources': ['http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/1'],
                                                                                                                                       'destinations': ['http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/topology/2']}), headers={'content-type': 'application/json'})


# Create appLibraryProfile

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/appLibProfile',
                          data=json.dumps({'configuredFlows': ['Amazon_EC2_Create_Key_Pair_Flow']}),
                          headers={'content-type': 'application/json'})

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/traffic/operations/applystatefultraffic', data=json.dumps({'arg1': 'http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/traffic'}), headers={'content-type': 'application/json'})

waitForComplete(response, root+"/traffic/operations/applystatefultraffic/"+response.json()["id"])

response = requests.post('http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/traffic/operations/startstatefultraffic', data=json.dumps({'arg1': 'http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/traffic'}), headers={'content-type': 'application/json'})

print '\nWaiting for statistics ...'
time.sleep(17)

getStats(sessionUrl='http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork',
         csvFile=None, csvEnableFileTimestamp=False, viewName='Application Traffic Item TCP Statistics')

'''
Row: 1
        Traffic Item: Topo1 to Topo2
        Initiator SYNs Sent: 115532
        Initiator SYN/SYN-ACKs Received: 115532
        Initiator FINs Sent: 115432
        Initiator FINs Received: 115431
        Initiator FIN-ACKs Sent: 115431
        Initiator FIN-ACKs Received: 115431
        Initiator Resets Sent: 0
        Initiator Resets Received: 0
        Initiator Retries: 0
        Initiator Timeouts: 0
        Responder SYN-ACKs Sent: 115533
        Responder SYN/SYN-ACKs Received: 115533
        Responder FINs Sent: 115432
        Responder FINs Received: 115433
        Responder FIN-ACKs Sent: 115432
        Responder FIN-ACKs Received: 115432
        Responder Accept Queue Entries: 0
        Responder Resets Sent: 0
        Responder Resets Received: 0
        Responder Retries: 0
        Responder Timeouts: 0
        Responder Connection Requests Failed: 0
        Responder Listen Queue Drops: 0
