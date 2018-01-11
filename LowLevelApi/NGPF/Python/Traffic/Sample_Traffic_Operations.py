################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mario Dicu $
#
#    Copyright © 1997 - 2015 by IXIA
#    All Rights Reserved.
#
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample configures 10 IPv4 sessions on each of the two ports,         # 
#    and performs the following traffic actions                                #
#    - Creating 2 Traffic Items for IPv4                                       #
#    - Add 2 new Endpoint sets to TI 1 IPv4                                    #
#    - Remove last configured Endpoint set from TI 1 IPv4                      #
#    - Disable TI 1 IPv4                                                       #
#    - Enable TI 1 IPv4                                                        #
#    - Duplicate TI 1 IPv4 3 times                                             #
#    - Remove a Traffic Item copy                                              #
#    - Adding Ingress Tracking for bot Traffic Items                           #
#    - Adding Egress Tracking for both Traffic Items                           #
#    - Adding Latency Bins Tracking for both Traffic Items                     #
#    - Generate Traffic                                                        #
#    - Apply Traffic                                                           #
#    - Start Traffic                                                           #
#                                                                              #
################################################################################

if 'py' not in dir():
    class TestFailedError(Exception): pass
    class Py: pass
    py = Py()
    py.ports = [('10.205.15.62', 3, 5), ('10.205.15.62', 3, 6)]
    py.ixTclServer = '10.205.15.224'
    py.ixTclPort = 8009

################################################################################
# Import the IxNet library
################################################################################
from IxNetwork import IxNet
import time
ixNet = IxNet()

################################################################################
# Connect to IxNet client
################################################################################

ixNet.connect(py.ixTclServer, '-port', py.ixTclPort, '-version', '7.40')

################################################################################
# Cleaning up IxNetwork
################################################################################
print "Cleaning up IxNetwork..."
ixNet.execute('newConfig')

################################################################################
# Defining the create IPv4 Traffic Item function
################################################################################
def createBasicIPv4TrafficItem(ixNet, name, sourceEP, destEP):
    print ("- creating traffic item: %s") % name
    ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
    ixNet.commit()
    trafficItem = ixNet.getList(ixNet.getRoot() + '/traffic', 'trafficItem')[-1]
    ixNet.setMultiAttribute( trafficItem,
            '-name'                 ,name,
            '-trafficType'          ,'ipv4',
            '-allowSelfDestined'    ,False,
            '-trafficItemType'      ,'l2L3',
            '-mergeDestinations'    ,True,
            '-egressEnabled'        ,False,
            '-srcDestMesh'          ,'manyToMany',
            '-enabled'              ,True,
            '-routeMesh'            ,'fullMesh',
            '-transmitMode'         ,'interleaved',
            '-biDirectional'        ,True,
            '-hostsPerNetwork'      ,1)
    ixNet.commit()
    ixNet.setAttribute(trafficItem, '-trafficType', 'ipv4')
    ixNet.commit()
    ixNet.add(trafficItem, 'endpointSet',
            '-sources',             sourceEP,
            '-destinations',        destEP,
            '-name',                'ep-set1',
            '-sourceFilter',        '',
            '-destinationFilter',   '')
    ixNet.commit()
    ixNet.setMultiAttribute(trafficItem + "/configElement:1/frameSize",
            '-type',        'fixed',
            '-fixedSize',   128)
    ixNet.setMultiAttribute(trafficItem + "/configElement:1/frameRate",
            '-type',        'percentLineRate',
            '-rate',        2)
    ixNet.setMultiAttribute(trafficItem + "/configElement:1/transmissionControl",
            '-duration'               ,1,
            '-iterationCount'         ,1,
            '-startDelayUnits'        ,'bytes',
            '-minGapBytes'            ,12,
            '-frameCount'             ,10000,
            '-type'                   ,'continuous',
            '-interBurstGapUnits'     ,'nanoseconds',
            '-interBurstGap'          , 0,
            '-enableInterBurstGap'    ,False,
            '-interStreamGap'         ,0,
            '-repeatBurst'            ,1,
            '-enableInterStreamGap'   ,False,
            '-startDelay'             ,0,
            '-burstPacketCount'       ,1,)
    ixNet.commit()

################################################################################
# Defining the Ingress Tracking for Traffic Item set function
################################################################################
def setIngressTrackingForTI(ixNet, ti, trackingList):
    tiName = ixNet.getAttribute(ti, '-name')
    print "--- Traffic Item: %s setting ingress tracking %s " % (tiName, trackingList)
    ixNet.setMultiAttribute(ti + "/tracking", '-trackBy', trackingList)
    ixNet.commit()

################################################################################
# Defining the Egress Tracking for Traffic Item set function
################################################################################    
def setFirstEgressTrackingForTI(ixNet, ti, stack, field):
    tiName = ixNet.getAttribute(ti, '-name')
    print "--- Traffic Item: %s setting eggress tracking to field %s for stack %s " % (tiName, field, stack)
    ixNet.setAttribute(ti, '-egressEnabled', True)
    et = ixNet.getList(ti, 'egressTracking')[0]
    ixNet.setAttribute(et, '-encapsulation', 'Any: Use Custom Settings')
    ixNet.setAttribute(et, '-offset', 'CustomByField')
    ixNet.commit()
    stackList = ixNet.getList(ixNet.getList(ti, 'egressTracking')[0] + '/fieldOffset', 'stack')
    for mstack in stackList:
        if stack in mstack:
            fieldList = ixNet.getList(mstack, 'field')
            for mfield in fieldList:
                if field in mfield:
                    ixNet.setAttribute(mfield, '-activeFieldChoice', True)
                    ixNet.setAttribute(mfield, '-trackingEnabled', True)
                    ixNet.setAttribute(mfield, '-valueType', 'valueList')
                    ixNet.setAttribute(mfield, '-valueList', [4, 6])
                    ixNet.commit()
                    break

################################################################################
# Defining the Latency Bins for Traffic Item set function
################################################################################
def setLatencyBinsTrackingForTI(ixNet, ti, binNo):
    tiName = ixNet.getAttribute(ti, '-name')
    print "--- Traffic Item: %s setting latency bins tracking %s " % (tiName, binNo)
    latencyBin = ixNet.getList(ti + '/tracking', 'latencyBin')[0]
    ixNet.setAttribute(latencyBin, '-enabled', True)
    ixNet.setAttribute(latencyBin, '-numberOfBins', binNo)
    ixNet.commit()

################################################################################
# Defining the Add EndpointSet function
################################################################################
def addEndpointSet(ixNet, trafficItem, epName, sourceEPs, destEPs):
    print "- adding %s endpoint set" %epName
    ixNet.add(trafficItem, 'endpointSet',
            '-sources',             sourceEPs,
            '-destinations',        destEPs,
            '-name',                epName,
            '-sourceFilter',        '',
            '-destinationFilter',   '')
    ixNet.commit()

################################################################################
# Defining the Remove EndpointSet function
################################################################################
def removeEndpointSet(ixNet, trafficItem, epName):
    print "- removing %s endpoint set" %epName
    eps = ixNet.getList(trafficItem, 'endpointSet')
    for ep in eps:
        mName = ixNet.getAttribute(ep, '-name')
        if str(mName) == str(epName):
            ixNet.remove(ep)
            ixNet.commit()
            break

################################################################################
# Adding ports to configuration
################################################################################
print "Adding ports to configuration"
root = ixNet.getRoot()
ixNet.add(root, 'vport')
ixNet.add(root, 'vport')
ixNet.commit()
vPorts = ixNet.getList(root, 'vport')
vport1 = vPorts[0]
vport2 = vPorts[1]

################################################################################
# Configure IPv4 Endpoints to configuration
################################################################################
print "Add topologies"
ixNet.add(root, 'topology')
ixNet.add(root, 'topology')
ixNet.commit()

topo1 = ixNet.getList(root, 'topology')[0]
topo2 = ixNet.getList(root, 'topology')[1]

print "Add ports to topologies"
ixNet.setAttribute(topo1, '-vports', vport1)
ixNet.setAttribute(topo2, '-vports', vport2)
ixNet.commit()

print "Add device groups to topologies"
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

dg1 = ixNet.getList(topo1, 'deviceGroup')[0]
dg2 = ixNet.getList(topo2, 'deviceGroup')[0]

print "Add Ethernet stacks to device groups"
ixNet.add(dg1, 'ethernet')
ixNet.add(dg2, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(dg1, 'ethernet')[0]
mac2 = ixNet.getList(dg2, 'ethernet')[0]

print "Add ipv4 stacks to Ethernets"
ixNet.add(mac1, 'ipv4')
ixNet.add(mac2, 'ipv4')
ixNet.commit()

ipv4_1 = ixNet.getList(mac1, 'ipv4')[0]
ipv4_2 = ixNet.getList(mac2, 'ipv4')[0]

print "Setting multi values for ipv4 addresses"
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_1, '-address') + '/counter', '-start', '22.1.1.1', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_1, '-gatewayIp') + '/counter', '-start', '22.1.1.2', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_2, '-address') + '/counter', '-start', '22.1.1.2', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_2, '-gatewayIp') + '/counter', '-start', '22.1.1.1', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

################################################################################
# Assign ports 
################################################################################
vports = ixNet.getList(ixNet.getRoot(), 'vport')
print "Assigning ports to " + str(vports) + " ..."
assignPorts = ixNet.execute('assignPorts', py.ports, [], ixNet.getList("/","vport"), True)
if assignPorts != vports:
    raise TestFailedError("FAILED assigning ports. Got %s" %assignPorts)
else:
    print("PASSED assigning ports. Got %s" %assignPorts)

################################################################################
# Start protocols
################################################################################
print "Starting All Protocols"
ixNet.execute('startAllProtocols')
print "Sleep 30sec for protocols to start"
time.sleep(30)

################################################################################
# Create 2 IPv4 Traffic Items
################################################################################
print "######################"
print "## Traffic Samples ##"
print "######################"
print ''
print "Creating 2 Traffic Items for IPv4"
createBasicIPv4TrafficItem(ixNet, "TI 1 IPv4", ipv4_1, ipv4_2)
createBasicIPv4TrafficItem(ixNet, "TI 2 IPv4", ipv4_2, ipv4_1)

ti1 = ixNet.getList('/traffic', 'trafficItem')[0]
ti2 = ixNet.getList('/traffic', 'trafficItem')[1]
print "Add 2 new Endpoint sets to TI 1 IPv4"
addEndpointSet(ixNet, ti1, 'ep-set2', ipv4_2, ipv4_1)
addEndpointSet(ixNet, ti1, 'ep-set3', ipv4_2, ipv4_1)
print "Remove last configured Endpoint set from TI 1 IPv4"
removeEndpointSet(ixNet, ti1, 'ep-set3')

################################################################################
# Performing the Traffic Actions Samples
################################################################################
print "Traffic Actions Samples:"
print "- Disable TI 1 IPv4"
ixNet.setAttribute(ti1, '-enabled', False)
ixNet.commit()
print "- Enable TI 1 IPv4"
ixNet.setAttribute(ti1, '-enabled', True)
ixNet.commit()
print "- Duplicate TI 1 IPv4 3 times"
ixNet.execute('duplicate', ti1, 3)
print "- Remove a Traffic Item copy"
ti_remove = ixNet.getList('/traffic', 'trafficItem')[2:]
ixNet.remove(ti_remove)
ixNet.commit()
print "- Adding Ingress Tracking for bot Traffic Items"
trackingList = ['sourceDestValuePair0']
setIngressTrackingForTI(ixNet, ti1, trackingList)
setIngressTrackingForTI(ixNet, ti2, trackingList)
print "- Adding Egress Tracking for both Traffic Items"
setFirstEgressTrackingForTI(ixNet, ti1, "ipv4", "ipv4.header.version-1")
setFirstEgressTrackingForTI(ixNet, ti2, "ipv4", "ipv4.header.version-1")
print "- Adding Latency Bins Tracking for both Traffic Items"
setLatencyBinsTrackingForTI(ixNet, ti1, 4)
setLatencyBinsTrackingForTI(ixNet, ti2, 4)
print "- Generate Traffic"
ixNet.execute('generate', [ti1, ti2])
print "- Apply Traffic"
ixNet.execute('apply', '/traffic')
print "- Start Traffic"
ixNet.execute('start', '/traffic')
print "Sleep 30sec then stop traffic"
time.sleep(30)
print "- Stop Traffic"
ixNet.execute('stop', '/traffic')

################################################################################
# Stop Protocols
################################################################################
print "Stop All Protocols"
ixNet.execute('stopAllProtocols')
print "Sleep 30sec for protocols to stop"
time.sleep(30)

