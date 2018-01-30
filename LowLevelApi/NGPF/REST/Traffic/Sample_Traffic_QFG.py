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

if 'py' not in dir():                       # define stuff if we don't run from harness
    class TestFailedError(Exception): pass
    class Py: pass
    py = Py()
    py.ports        = [('10.200.113.7', '8', '7'), ('10.200.113.7', '8', '8')]
    py.ixTclServer  =  "10.200.225.53"
    py.ixRestPort    =  '11020'
    py.ixTclPort     =  8020
# END HARNESS VARS ************************************************************

################################################################################
# Import the IxNet library
################################################################################
import sys,time,copy,pprint,os,ast
from restAPIV import *

################################################################################
# Connect to IxNet client
################################################################################

ixNet = IxNet(py.ixTclServer, int(py.ixTclPort)+3000)
ixNet.connect()
root = ixNet.getRoot()

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
ixNet.setAttribute(topo1, '-vports', [vport1])
ixNet.setAttribute(topo2, '-vports', [vport2])
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
assignPorts=ixNet.execute('assignPorts',py.ports,[],vports,True )

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


################################################################################
# Add the Quick Flow Group, Generate, Apply and Start the traffic
################################################################################
print "- Add Quick Flow Group"
data = {'name':'Quick Flow Groups','trafficItemType':'quick','trafficType':'raw'}
quick_flow_group = ixNet.add(root+'/traffic', 'trafficItem',data)
ixNet.commit()

################################################################################
# Setting the endpoint set attributes
################################################################################
data = {'destinations':[vport2+'/protocols'],'sources':[vport1+'/protocols']}
endpoint_set = ixNet.add(root+'/traffic/trafficItem/1', 'endpointSet',data)
ixNet.commit()

################################################################################
# Set the frameSize, frameRate attributes for the first stream in endpoint set 1
################################################################################
highlevelstream1 = ixNet.getList(quick_flow_group[0], 'highLevelStream')[0]
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
time.sleep(10)
r = ixNet.getRoot()
ti1 = ixNet.getList(ixNet.getRoot() + '/traffic', 'trafficItem')[0]
ixNet.execute('generate', ti1)
ixNet.execute('apply', r + '/traffic')
ixNet.execute('start', r + '/traffic')
print "Sleep 30sec to send all traffic"
time.sleep(30)
ixNet.execute('stop', r + '/traffic')
time.sleep(10)

################################################################################
# Stop All Protocols
################################################################################
print "Stop All Protocols"
ixNet.execute('stopAllProtocols')
print "Sleep 30sec for protocols to stop"
time.sleep(30)

