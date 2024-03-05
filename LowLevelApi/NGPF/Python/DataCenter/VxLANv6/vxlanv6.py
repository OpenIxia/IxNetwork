#!/usr/bin/python
################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################


################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia Keysight and #
# have     																	   #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia Keysight and/or by the user and/or by a third party)] shall at  #
# all times 																   #
# remain the property of Ixia Keysight.                                        #
#                                                                              #
# Ixia Keysight does not warrant (i) that the functions contained in the script#
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND Ixia Keysight#
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL Ixia Keysight BE LIABLE FOR ANY DAMAGES RESULTING FROM OR  #
# ARISING   																   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF Ixia Keysight HAS BEEN ADVISED OF THE          #
# POSSIBILITY OF  SUCH DAMAGES IN ADVANCE.                                     #
# Ixia Keysight will not be required to provide any software maintenance or    #
# support services of any kind (e.g. any error corrections) in connection with #
# script or any part thereof. The user acknowledges that although Ixia Keysight# 
# may     																	   #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia Keysight to  #
# provide any additional maintenance or support services.                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    Script  will create following:                                            #
#    1. Adding ports to configuration                                          #
#    2. Create VxLanV6 with IPv4 hosts                                         #
#    3.	Enable unicast info                                                    #
#    4. Start all protocols                           						   #
#  	 5. Check stats and learned info										   #
#    6. Stop all protocols	   					  							   #
#                                                                              #
################################################################################


import time
import os
from IxNetwork import IxNet

ixNet = IxNet()

print ("Connecting to the server")
ixNet.connect('10.39.65.1', '-setAttribute', 'strict', '-port', 9863, '-version', '9.00')

print ("Cleaning up IxNetwork...")
ixNet.execute('newConfig')

root = ixNet.getRoot()

print ("\nAdd virtual ports to configuration...")
vports = ixNet.getList(ixNet.getRoot(), 'vport')

print ('Add chassis in IxNetwork...')
chassis = '10.39.64.117'
availableHardwareId = ixNet.getRoot()+'availableHardware'
ixNet.add(availableHardwareId, 'chassis', '-hostname', chassis)
ixNet.commit()
time.sleep(5)

###############################################################################
# 1. Adding ports to configuration
################################################################################
print "Adding ports to configuration"
root = ixNet.getRoot()
ixNet.add(root, 'vport')
ixNet.add(root, 'vport')
ixNet.commit()
vPorts = ixNet.getList(root, 'vport')
vport1 = vPorts[0]
vport2 = vPorts[1]
print ("Assigning ports from " + chassis + " to "+ str(vports) + " ...")
ixNet.setAttribute(vport1, '-connectedTo', '/availableHardware/chassis:"10.39.64.117"/card:2/port:9')
ixNet.setAttribute(vport2, '-connectedTo', '/availableHardware/chassis:"10.39.64.117"/card:2/port:10')
ixNet.commit()

################################################################################
# 2. Adding VXLANv6 Protocol
################################################################################

print "Add VxLANv6 topologies"
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

print "Add Ethernet stacks to VxLANv6 device groups"
ixNet.add(dg1, 'ethernet')
ixNet.add(dg2, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(dg1, 'ethernet')[0]
mac2 = ixNet.getList(dg2, 'ethernet')[0]

print "Add ipv6 stacks to Ethernet"
ixNet.add(mac1, 'ipv6')
ixNet.add(mac2, 'ipv6')
ixNet.commit()

ipv6_1 = ixNet.getList(mac1, 'ipv6')[0]
ipv6_2 = ixNet.getList(mac2, 'ipv6')[0]

# Setting ipv6 address and ipv6 gateway address
print "Setting multi values for ipv6 addresses"

ixNet.setMultiAttribute(ixNet.getAttribute(ipv6_1, '-address') + '/counter', '-start', '2000:0:0:1:0:0:0:2', '-step', '0:0:0:1:0:0:0:0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv6_1, '-gatewayIp') + '/counter', '-start', '2000:0:0:1:0:0:0:1', '-step', '0:0:0:1:0:0:0:0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv6_1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv6_2, '-address') + '/counter', '-start', '2000:0:0:1:0:0:0:1', '-step', '0:0:0:1:0:0:0:0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv6_2, '-gatewayIp') + '/counter', '-start', '2000:0:0:1:0:0:0:2', '-step', '0:0:0:1:0:0:0:0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv6_2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

print "Add VXLANv6 stacks to ipv6"
ixNet.add(ipv6_1, 'vxlanv6')
ixNet.add(ipv6_2, 'vxlanv6')
ixNet.commit()

vxlanv6_1 = ixNet.getList(ipv6_1, 'vxlanv6')[0]
vxlanv6_2 = ixNet.getList(ipv6_2, 'vxlanv6')[0]

ixNet.setMultiAttribute(ixNet.getAttribute(vxlanv6_1, '-vni') + '/counter', '-start', '1100', '-step', '1')
ixNet.setMultiAttribute(ixNet.getAttribute(vxlanv6_1, '-ipv6_multicast') + '/counter', '-start', 'ff03:0:0:0:0:0:0:1', '-step', '0:0:0:0:0:0:0:1')
ixNet.setMultiAttribute(ixNet.getAttribute(vxlanv6_2, '-vni') + '/counter', '-start', '1100', '-step', '1')
ixNet.setMultiAttribute(ixNet.getAttribute(vxlanv6_2, '-ipv6_multicast') + '/counter', '-start', 'ff03:0:0:0:0:0:0:1', '-step', '0:0:0:0:0:0:0:1')

# Adding IPv4 Hosts behind VxLANv6 device group
print "Add IPv4 hosts to VXLANv6 device group "
ixNet.add(dg1, 'deviceGroup')
ixNet.add(dg2, 'deviceGroup')
ixNet.commit()

dg3 = ixNet.getList(dg1, 'deviceGroup')[0]
dg4 = ixNet.getList(dg2, 'deviceGroup')[0]

print "Add Ethernet stacks to VM hosts"
ixNet.add(dg3, 'ethernet')
ixNet.add(dg4, 'ethernet')
ixNet.commit()

mac3 = ixNet.getList(dg3, 'ethernet')[0]
mac4 = ixNet.getList(dg4, 'ethernet')[0]
print "Add IPv4 stacks to VM hosts"
ixNet.add(mac3, 'ipv4')
ixNet.add(mac4, 'ipv4')
ixNet.commit()

ipv4_3 = ixNet.getList(mac3, 'ipv4')[0]
ipv4_4 = ixNet.getList(mac4, 'ipv4')[0]

print "Setting multi values for inner IPv4 addresses"
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_3, '-address') + '/counter', '-start', '5.1.1.1', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_3, '-gatewayIp') + '/counter', '-start', '5.1.1.2', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_3, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_4, '-address') + '/counter', '-start', '5.1.1.2', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_4, '-gatewayIp') + '/counter', '-start', '5.1.1.1', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_4, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

################################################################################
# 3. Start All Protocols
################################################################################
print ("Starting All Protocols")
ixNet.execute('startAllProtocols')
print ("Sleep 30sec for protocols to start")
time.sleep(30)

################################################################################
# 4. Retrieve protocol statistics.
################################################################################
print ("Fetching all Protocol Summary Stats\n")
viewPage = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues'):
    for statVal in statValList:
        print("***************************************************")
        index = 0
        for satIndv in statVal:
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")

print ("Fetching all VxLANv6 per port Stats\n")
viewPage = '::ixNet::OBJ-/statistics/view:"VXLANv6 Per Port"/page'
statcap = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues'):
    for statVal in statValList:
        print("***************************************************")
        index = 0
        for satIndv in statVal:
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")

###############################################################################
# 5. Retrieve protocol learned info in Port 1
###############################################################################
print("VxLANv6 Learned info\n")
ixNet.execute('getVXLANLearnedInfo', vxlanv6_1, '1')
time.sleep(5)
linfo = ixNet.getList(vxlanv6_1, 'learnedInfo')[0]
table = ixNet.getList(linfo, 'table')[0]
values = ixNet.getAttribute(table, '-values')

print("***************************************************\n")
for v in values:
    print(v)
# end for
print("***************************************************")

################################################################################
# 6. Stop all protocols                                                           #
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
time.sleep(10)

print ("\n\nCleaning up IxNetwork...")
ixNet.execute('newConfig')
print ('!!! Test Script Ends !!!')



