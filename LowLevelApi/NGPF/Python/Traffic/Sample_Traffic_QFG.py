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
#    This sample configures 10 IPv4 sessions on each of the two ports          #
#    - Adds a Quick Flow Group                                                 #
#    - Edit some settings for the Quick Flow Group like: frameSize, frameRate  #
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
# Adding IPv4 endpoints to configuration
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
# Start All Protocols
################################################################################
print "Starting All Protocols"
ixNet.execute('startAllProtocols')
print "Sleep 30sec for protocols to start"
time.sleep(30)

################################################################################
# Create a Basic Quick Flow Group
################################################################################
print "######################"
print "## Traffic Samples ##"
print "######################"
print ''

def addBasicQuickFlowGroup(ixNet, srcPort, dstPort ):
    print "- add quick flow group"
    quick_flow_group = ixNet.add('/traffic', 'trafficItem')

    ################################################################################
    # Setting the quick flow group attributes
    ################################################################################
    ixNet.setMultiAttribute(quick_flow_group,
                '-name', 'Quick Flow Groups',
                '-trafficItemType', 'quick',
                '-trafficType', 'raw')
    ixNet.commit()
    quick_flow_group = ixNet.remapIds(quick_flow_group)[0]

    ################################################################################
    # Setting the endpoint set attributes
    ################################################################################
    endpoint_set = ixNet.add(quick_flow_group, 'endpointSet')
    ixNet.setMultiAttribute(endpoint_set,
                '-destinations', [dstPort+'/protocols'],
                '-sources', [srcPort+'/protocols'])
    ixNet.commit()

    ################################################################################
    # Set the frameSize, frameRate attributes for the first stream in endpoint set 1
    ################################################################################
    endpoint_set = ixNet.remapIds(endpoint_set)[0]
    highlevelstream1 = ixNet.getList(quick_flow_group, 'highLevelStream')[0]
    ixNet.setAttribute(highlevelstream1+'/frameSize', '-fixedSize', '120')
    ixNet.setAttribute(highlevelstream1+'/frameRate',	'-rate', '500')
    ixNet.setAttribute(highlevelstream1+'/frameRate',	'-type', 'framesPerSecond')
    ixNet.commit()

    ################################################################################
    # setting the Ethernet source and destination mac addresses
    ################################################################################
    for stack in ixNet.getList(highlevelstream1, 'stack'):
        if "ethernet-" in stack:
            for field in ixNet.getList(stack, 'field'):
                if "ethernet.header.destinationAddress-" in field:
                    ixNet.setAttribute(field, '-singleValue', '33:00:00:00:00:00')
                elif "ethernet.header.sourceAddress-" in field:
                    ixNet.setAttribute(field, '-singleValue', '11:00:00:00:00:00')
    ixNet.commit()

################################################################################
# Add the Quick Flow Group, Generate, Apply and Start the traffic
################################################################################
print "- Add Quick Flow Group"
addBasicQuickFlowGroup(ixNet, vport1, vport2)
print "- Generate Traffic"
ti1 = ixNet.getList('/traffic', 'trafficItem')
ixNet.execute('generate', ti1)
print "- Apply Traffic"
ixNet.execute('apply', '/traffic')
print "- Start Traffic"
ixNet.execute('start', '/traffic')
print "Sleep 30sec then stop traffic"
time.sleep(30)
print "- Stop Traffic"
ixNet.execute('stop', '/traffic')

################################################################################
# Stop All Protocols
################################################################################
print "Stop All Protocols"
ixNet.execute('stopAllProtocols')
print "Sleep 30sec for protocols to stop"
time.sleep(30)

