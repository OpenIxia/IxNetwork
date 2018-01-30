#!/usr/local/python2.7.6/bin/python2.7

# Written by: Hubert Gee
# 
# This is a sample IxNetwork REST API script written in a human friendly readable
# way to show how the REST APIs are done.
#
# If you know the IxNet low level API, you could easily
# translate these REST APIs to the IxNet style.
#

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

import sys
import requests
import json
import time

ixChassisIp = '10.219.117.101'
restServerIp = '10.219.117.103'
restServerPort = '11009'
port1 = '1/1'
port2 = '1/2'

timeout = 5
httpHeader = 'http://%s:%s' % (restServerIp, restServerPort)
root = '%s/api/v1/sessions/1/ixnetwork' % httpHeader
urlHeadersJson = {'content-type': 'application/json'}
urlHeadersData = {'content-type': 'application/octet-stream'}
    
def JsonPrintPretty( jsonContents ):
    contents = json.loads(jsonContents)
    print json.dumps(contents, indent=4, sort_keys=True)


restSessionObj = requests.post( 'http://%s:%s/api/v1/sessions/' % (restServerIp, restServerPort))
#JsonPrintPretty(restSessionObj.text)

# Root = http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork

# Execute
# Create new config
newConfig = requests.post('%s/operations/newconfig' % root, data=json.dumps({}), headers=urlHeadersJson)
print '\nNew Config:%s' % JsonPrintPretty(newConfig.text)
time.sleep(5)

# Create 2 vports for 2 ports
vport1 = requests.post('%s/%s' % (root, 'vport/'), data=json.dumps([{}]), headers=urlHeadersJson)
vport2 = requests.post('%s/%s' % (root, 'vport/'), data=json.dumps([{}]), headers=urlHeadersJson)
print '\nvport1:%s' % JsonPrintPretty(vport1.text)
print '\nvport2:%s' % JsonPrintPretty(vport2.text)

# GetList
vportList = requests.get('%s/%s' % (root, 'vport'), data=json.dumps([{}]), headers=urlHeadersJson)
print '\nvportList:', JsonPrintPretty(vportList.text)

data = {'arg1': [{'arg1': ixChassisIp, 'arg2': port1.split('/')[0], 'arg3': port1.split('/')[1]}, 
                 {'arg1': ixChassisIp, 'arg2': port2.split('/')[0], 'arg3': port2.split('/')[1]}], 
        'arg2': [],
        'arg3': ['%s/vport/1' % root, 
                 '%s/vport/2' % root 
                 ], 
        'arg4': True
        }
assignPorts = requests.post(url='%s/operations/assignports' % root, data=json.dumps(data), headers=urlHeadersJson)
print '\nAssignPorts:', JsonPrintPretty(assignPorts.text)
print '\nWait 25 seconds for ports to come up', time.sleep(25)

# GetList on vport level
vportGetList = requests.get('%s/%s' % (root, 'vport'), headers=urlHeadersJson)
print '\nvportGetList:', JsonPrintPretty(vportGetList.text)

# ['http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/vport/1', 
# 'http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/vport/2']
vportList = ["%s/%s%s" % (root, 'vport/',str(i['id'])) for i in vportGetList.json()]

# http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/vport/1
vportTx = vportList[0]
# http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/vport/2
vportRx = vportList[1]

# Create Topologies
# Add
requests.post('%s/%s' % (root, 'topology'), data=json.dumps([{}]), headers=urlHeadersJson)
requests.post('%s/%s' % (root, 'topology'), data=json.dumps([{}]), headers=urlHeadersJson)

#['http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology1', 
# 'http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology2']
topologyList = requests.get('%s/%s' % (root, 'topology'), headers=urlHeadersJson)
topologies = ["%s/%s/%s" % (root, 'topology', str(i['id'])) for i in topologyList.json()]
topo1 = topologies[0]
topo2 = topologies[1]

print '\ntopo1:', topo1
print '\ntopo2:', topo2

# SetAttribute
print '\nAdd ports to topologies', topo1, vportTx
response = requests.patch(url=topo1, data=json.dumps({'vports':[vportTx]}), headers=urlHeadersJson)
response = requests.patch(url=topo2, data=json.dumps({'vports':[vportRx]}), headers=urlHeadersJson)

# Create Device Groups
print '\nCreate Device Groups'
requests.post('%s/%s' % (topo1, 'deviceGroup'), data=json.dumps([{}]), headers=urlHeadersJson)
requests.post('%s/%s' % (topo2, 'deviceGroup'), data=json.dumps([{}]), headers=urlHeadersJson)

# GetList
# http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1
deviceGroupList = requests.get('%s/%s' % (topo1, 'deviceGroup'), headers=urlHeadersJson)
topo1DeviceGroup1 = ["%s/%s/%s" % (topo1, 'deviceGroup', str(i['id'])) for i in deviceGroupList.json()][0]

# http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/topology/2/deviceGroup/1
deviceGroupList = requests.get('%s/%s' % (topo2, 'deviceGroup'), headers=urlHeadersJson)
topo2DeviceGroup1 = ["%s/%s/%s" % (topo2, 'deviceGroup', str(i['id'])) for i in deviceGroupList.json()][0]

# SetAttribute
requests.patch(url=topo1DeviceGroup1, data=json.dumps({'multiplier':'1'}), headers=urlHeadersJson)
requests.patch(url=topo2DeviceGroup1, data=json.dumps({'multiplier':'1'}), headers=urlHeadersJson)

# Add
requests.post('%s/%s' % (topo1DeviceGroup1, 'ethernet'), data=json.dumps([{}]), headers=urlHeadersJson)
requests.post('%s/%s' % (topo2DeviceGroup1, 'ethernet'), data=json.dumps([{}]), headers=urlHeadersJson)

# GetList
mac1List = requests.get('%s/%s' % (topo1DeviceGroup1, 'ethernet'), headers=urlHeadersJson)
mac1 = ["%s/%s/%s" % (topo1DeviceGroup1, 'ethernet', str(i['id'])) for i in mac1List.json()][0]

mac2List = requests.get('%s/%s' % (topo2DeviceGroup1, 'ethernet'), headers=urlHeadersJson)
mac2 = ["%s/%s/%s" % (topo2DeviceGroup1, 'ethernet', str(i['id'])) for i in mac2List.json()][0]

print '\nMac1:', mac1
print '\nMac2:', mac2

# GetAttribute
# /api/v1/sessions/1/ixnetwork/multivalue/3
response = requests.get(mac1)
mac1Attrib = response.json()['mac']

# SetMutliAttribute
requests.patch(url=httpHeader + mac1Attrib + '/counter',
               data=json.dumps({'direction': 'increment',
                                'start': '00:01:01:01:00:01',
                                'step': '00:00:00:00:00:01'
                                }), 
               headers=urlHeadersJson)

response = requests.get(mac2)
mac2Attrib = response.json()['mac']

# SetAttribute
requests.patch(url=httpHeader + mac2Attrib + '/singleValue',
               data=json.dumps({'value': '00:01:01:02:00:01'}), 
               headers=urlHeadersJson)

# Add IPv4
requests.post('%s/%s' % (mac1, 'ipv4'), data=json.dumps([{}]), headers=urlHeadersJson)
requests.post('%s/%s' % (mac2, 'ipv4'), data=json.dumps([{}]), headers=urlHeadersJson)

# GetList
ip1List = requests.get('%s/%s' % (mac1, 'ipv4'), headers=urlHeadersJson)
ip1 = ["%s/%s/%s" % (mac1, 'ipv4', str(i['id'])) for i in ip1List.json()][0]

ip2List = requests.get('%s/%s' % (mac2, 'ipv4'), headers=urlHeadersJson)
ip2 = ["%s/%s/%s" % (mac2, 'ipv4', str(i['id'])) for i in ip2List.json()][0]

# GetAttribute for IPv4
response = requests.get(ip1)
multivalueIp1 = response.json()['address']
response = requests.get(ip2)
multivalueIp2 = response.json()['address']
response = requests.get(ip1)
multivalueGateway1 = response.json()['gatewayIp']
response = requests.get(ip2)
multivalueGateway2 = response.json()['gatewayIp']

# SetAttribute
requests.patch(url=httpHeader + multivalueIp1 + '/singleValue',
               data=json.dumps({'value': '10.10.10.1'}), 
               headers=urlHeadersJson)

requests.patch(url=httpHeader + multivalueIp2 + '/singleValue',
               data=json.dumps({'value': '10.10.10.2'}), 
               headers=urlHeadersJson)

requests.patch(url=httpHeader + multivalueGateway1 + '/singleValue',
               data=json.dumps({'value': '10.10.10.2'}), 
               headers=urlHeadersJson)

requests.patch(url=httpHeader + multivalueGateway2 + '/singleValue',
               data=json.dumps({'value': '10.10.10.1'}), 
               headers=urlHeadersJson)

# GetAttribute
response = requests.get(ip1)
ip1Prefix = response.json()['prefix']
response = requests.get(ip2)
ip2Prefix = response.json()['prefix']

# SetAttribute
requests.patch(url=httpHeader + ip1Prefix + '/singleValue',
               data=json.dumps({'value': '24'}), 
               headers=urlHeadersJson)

# SetAttribute
requests.patch(url=httpHeader + ip2Prefix + '/singleValue',
               data=json.dumps({'value': '24'}), 
               headers=urlHeadersJson)

# GetAttribute
response = requests.get(ip1)
ip1ResolveGw = response.json()['resolveGateway']
response = requests.get(ip2)
ip2ResolveGw = response.json()['resolveGateway']

# SetMultiAttribute
requests.patch(url=httpHeader + ip1ResolveGw + '/singleValue',
               data=json.dumps({'value': 'true'}), 
               headers=urlHeadersJson)

requests.patch(url=httpHeader + ip2ResolveGw + '/singleValue',
               data=json.dumps({'value': 'true'}), 
               headers=urlHeadersJson)

requests.delete(root)

# Add
print '\nAdd BGP over IPv4 stack'
requests.post('%s/%s' % (ip1, 'bgpIpv4Peer'), data=json.dumps([{}]), headers=urlHeadersJson)
requests.post('%s/%s' % (ip2, 'bgpIpv4Peer'), data=json.dumps([{}]), headers=urlHeadersJson)

# GetList
bgp1List = requests.get('%s/%s' % (ip1, 'bgpIpv4Peer'), headers=urlHeadersJson)
bgp1 = ["%s/%s/%s" % (ip1, 'bgpIpv4Peer', str(i['id'])) for i in bgp1List.json()][0]
bgp2List = requests.get('%s/%s' % (ip2, 'bgpIpv4Peer'), headers=urlHeadersJson)
bgp2 = ["%s/%s/%s" % (ip2, 'bgpIpv4Peer', str(i['id'])) for i in bgp2List.json()][0]

# SetAttribute
requests.patch(url=topo1DeviceGroup1,
               data=json.dumps({'name': 'BGP DG1'}), 
               headers=urlHeadersJson)

requests.patch(url=topo2DeviceGroup1,
               data=json.dumps({'name': 'BGP DG2'}), 
               headers=urlHeadersJson)

# GetAttribute
response = requests.get(bgp1)
bgp1DutIp = response.json()['dutIp']
response = requests.get(bgp2)
bgp2DutIp = response.json()['dutIp']

# SetAttribute
requests.patch(url=httpHeader + bgp1DutIp + '/singleValue',
               data=json.dumps({'value': '10.10.10.2'}), 
               headers=urlHeadersJson)

requests.patch(url=httpHeader + bgp2DutIp + '/singleValue',
               data=json.dumps({'value': '10.10.10.1'}), 
               headers=urlHeadersJson)

# Add Network Group
print '\nAdd Network Group'
requests.post('%s/%s' % (topo1DeviceGroup1, 'networkGroup'), data=json.dumps([{}]), headers=urlHeadersJson)
requests.post('%s/%s' % (topo2DeviceGroup1, 'networkGroup'), data=json.dumps([{}]), headers=urlHeadersJson)

# GetList
networkGroup1List = requests.get('%s/%s' % (topo1DeviceGroup1, 'networkGroup'), headers=urlHeadersJson)
networkGroup1 = ["%s/%s/%s" % (topo1DeviceGroup1, 'networkGroup', str(i['id'])) for i in networkGroup1List.json()][0]
networkGroup2List = requests.get('%s/%s' % (topo2DeviceGroup1, 'networkGroup'), headers=urlHeadersJson)
networkGroup2 = ["%s/%s/%s" % (topo2DeviceGroup1, 'networkGroup', str(i['id'])) for i in networkGroup2List.json()][0]

# SetAttribute
requests.patch(url=networkGroup1,
               data=json.dumps({'name': 'NetworkGroup1'}), 
               headers=urlHeadersJson)

requests.patch(url=networkGroup2,
               data=json.dumps({'name': 'NetworkGroup2'}), 
               headers=urlHeadersJson)

# Add 
#    Network Group Prefix Pools
print '\nAdd Network Group Prefix Pools'
requests.post('%s/%s' % (networkGroup1, 'ipv4PrefixPools'), data=json.dumps([{}]), headers=urlHeadersJson)
requests.post('%s/%s' % (networkGroup2, 'ipv4PrefixPools'), data=json.dumps([{}]), headers=urlHeadersJson)

# Execute
print '\nStarting all protocols'
print '\nWaiting 30 seconds for BGP to come up', 
requests.post('%s/operations/startAllProtocols' % root, data=json.dumps({}), headers=urlHeadersJson)
time.sleep(30)

# Execute
topology  = root + '/globals/topology'
print '\nApplying changes on the fly. Wait 10 seconds'
# http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/globals/topology/operations/applyOnTheFly
response = requests.post(url='%s/operations/applyOnTheFly' % topology, data=json.dumps({'arg1': topology}), headers=urlHeadersJson)
#time.sleep(10)

# Add Traffic
trafficItem1 = requests.post('%s/%s' % (root + '/traffic', 'trafficItem'), data=json.dumps([{}]), headers=urlHeadersJson)
print '\ntrafficItem1:', trafficItem1.json()

trafficItemList = requests.get('%s/%s/%s' % (root, 'traffic', 'trafficItem'), headers=urlHeadersJson)
trafficItem1 = ["%s/traffic/%s/%s" % (root, 'trafficItem', str(i['id'])) for i in trafficItemList.json()][0]

# SetMultiAttribute
requests.patch(url=trafficItem1,
               data=json.dumps({'name': 'Traffic Item 1',
                                'trafficType': 'ipv4'}), 
               headers=urlHeadersJson)

endpointSet1 = requests.post('%s/%s' % (trafficItem1, 'endpointSet'), data=json.dumps([{}]), headers=urlHeadersJson)
endpointSetList = requests.get('%s/%s' % (trafficItem1, 'endpointSet'), headers=urlHeadersJson)
endpointSet = ['%s/%s/%s' % (trafficItem1, 'endpointSet', str(i['id'])) for i in endpointSetList.json()][0]

sourceList = requests.get('%s/%s' % (networkGroup1, 'ipv4PrefixPools'), headers=urlHeadersJson)
source = ["%s/%s/%s" % (networkGroup1, 'ipv4PrefixPools', str(i['id'])) for i in sourceList.json()][0]

destinationList = requests.get('%s/%s' % (networkGroup2, 'ipv4PrefixPools'), headers=urlHeadersJson)
destination = ["%s/%s/%s" % (networkGroup2, 'ipv4PrefixPools', str(i['id'])) for i in destinationList.json()][0]

# SetMultiAttribute
response = requests.patch(url=endpointSet,
                          data=json.dumps({'name': 'EndpointSet-1',
                                           'sources': [source],
                                           'destinations': [destination]
                                           }), 
                          headers=urlHeadersJson)

requests.patch(url=trafficItem1 + '/tracking',
               data=json.dumps({'trackBy': ['sourceDestEndpointPair0', 'trackingenabled0']
                                }), 
               headers=urlHeadersJson)

# Execute
print '\nApplying configuration. Wait 5 seconds.'
response = requests.post(url='%s/traffic/operations/apply' % root, data=json.dumps({'arg1': root +'/traffic'}), headers=urlHeadersJson)
time.sleep(5)

print '\nStarting traffic'
response = requests.post(url='%s/traffic/operations/start' % root, data=json.dumps({'arg1': root +'/traffic'}), headers=urlHeadersJson)
time.sleep(10)

response = requests.post(url='%s/traffic/operations/stop' % root, data=json.dumps({'arg1': root +'/traffic'}), headers=urlHeadersJson)
time.sleep(5)

viewName = "Flow Statistics"

viewList = requests.get('%s/%s/%s' % (root, 'statistics', 'view'), headers=urlHeadersJson)
views = ['%s/%s/%s/%s' % (root, 'statistics', 'view', str(i['id'])) for i in viewList.json()]

for view in views:
    # GetAttribute
    response = requests.get('%s' % (view), headers=urlHeadersJson)
    caption = response.json()['caption']
    print '\ncaption:', caption
    if viewName == caption:
        viewObj = view
        print '\nviewObj:', viewObj
        break

txFrames = requests.post(url='%s/operations/getColumnValues' % viewObj, data=json.dumps({'arg1': viewObj,
                                                                                         'arg2': 'Tx Frames'}), headers=urlHeadersJson)
rxFrames = requests.post(url='%s/operations/getColumnValues' % viewObj, data=json.dumps({'arg1': viewObj,
                                                                                         'arg2': 'Rx Frames'}), headers=urlHeadersJson)
for txStat, rxStat in zip(txFrames.json()['result'], rxFrames.json()['result']):
    if txStat != rxStat:
        print '\nFailed: TxFrames=%s  RxFrames=%s' % (txStat, rxStat)
    else:
        print '\nPassed! No frame loss'

requests.post('%s/operations/stopAllProtocols' % root, data=json.dumps({}), headers=urlHeadersJson)

# Disconnect
requests.delete(root)
