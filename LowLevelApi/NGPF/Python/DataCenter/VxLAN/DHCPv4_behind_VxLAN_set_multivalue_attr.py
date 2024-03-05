# -*- coding: cp1252 -*-
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

################################################################################
#                                                                              #
# Description:                                                                 #
#   This script intends to demonstrate how to configure VxLAN with DHCPv6      #
#   Client and DHCPv6 Server. It configures one topology with one Device Group #
#   with VxLAN and a chained Device Group with the DHCPv6 Client stack         #
#   and a corresponding topology containing one Device Group with VxLAN and a  #
#   chained Device Group with DHCPv6 Server stack.                             #
#   Also demonstrates how to set a multivalue. 		   						   #
# Module:                                                                      #
#    The sample was tested on an FlexAP10G16S module.                          #
#                                                                              #
################################################################################



# import Python packages
import time
import os
import IxNetwork

# create an instance of the IxNet class
ixNet = IxNetwork.IxNet()

# create absolute path for the config and load it
print ("Connecting to server: localhost")
ixNet.connect('localhost', '-port', 8009, '-version', '7.30')

print ("Cleaning up IxNetwork...")
ixNet.execute('newConfig')

# all objects are under root
root = ixNet.getRoot()

print ("\nAdd virtual ports to configuration...")
vports = []
vports.append(ixNet.add(root, 'vport'))
vports.append(ixNet.add(root, 'vport'))
ixNet.commit()

# get virtual ports
vports = ixNet.getList(ixNet.getRoot(), 'vport')

print ('Add chassis in IxNetwork...')
chassis = '10.205.15.184'
availableHardwareId = ixNet.getRoot()+'availableHardware'
ixNet.add(availableHardwareId, 'chassis', '-hostname', chassis)
ixNet.commit()


print ("Assigning ports from " + chassis + " to "+ str(vports) + " ...")
ixNet.setAttribute(vports[0], '-connectedTo', '/availableHardware/chassis:"10.205.15.184"/card:9/port:2')
ixNet.setAttribute(vports[1], '-connectedTo', '/availableHardware/chassis:"10.205.15.184"/card:9/port:10')
ixNet.commit()


print ("Rebooting ports...")
jobs = [ixNet.setAsync().execute('resetPortCpu', vp) for vp in vports]

for j in jobs:
    print (j + ' ' + ixNet.getResult(j))
print ("Done... Ports are rebooted...")

time.sleep(5)
ixNet.execute('clearStats')



# ######################## Add VxLAN and DHCP DGs ############################ #

# adding topology with vxlan and dhcp server

print ('# \n######## HOW TO create a topology with DGs and various layers ####### #')
print ('\n\nCreate first topology with DHCPServer chained to VXLAN...')

print ('\nAdd topology...')
ixNet.add(root, 'topology')
print ('\nUse ixNet.commit() to commit added child under root.')
ixNet.commit()
print ('\nUse ixNet.getList to get newly added child under root.')
topS = ixNet.getList(root, 'topology')[0]

print ('Add virtual port to topology and change its name...')
ixNet.setMultiAttribute(topS, '-vports', vports[0], '-name', 'vxlan-server')
ixNet.commit()

print ('Add DeviceGroup for VXLAN...')
ixNet.add(topS, 'deviceGroup')
ixNet.commit()
dgVxlan1 = ixNet.getList(topS, 'deviceGroup')[0]

print ('Create the VXLAN stack in this DeviceGroup...')
print ('Add Ethernet layer...')
ixNet.add(dgVxlan1, 'ethernet')
ixNet.commit()
ethV1 = ixNet.getList(dgVxlan1, 'ethernet')[0]

print ('Add IPv4 layer...')
ixNet.add(ethV1, 'ipv4')
ixNet.commit()
ipV1 = ixNet.getList(ethV1, 'ipv4')[0]

print ('Add VxLAN layer...')
ixNet.add(ipV1, 'vxlan')
ixNet.commit()
vxlan1 = ixNet.getList(ipV1, 'vxlan')[0]


print ('Add a chained Device Group to the VXLAN Device Group...')
ixNet.add(dgVxlan1, 'deviceGroup')
ixNet.commit()
chained_dgS = ixNet.getList(dgVxlan1, 'deviceGroup')[0]

print ('Create the DHCPServer stack in this DeviceGroup...')
print ('Add Ethernet layer...')
ixNet.add(chained_dgS, 'ethernet')
ixNet.commit()
ethS = ixNet.getList(chained_dgS, 'ethernet')[0]

print ('Add IPv4 layer...')
ixNet.add(ethS, 'ipv6')
ixNet.commit()
ipS = ixNet.getList(ethS, 'ipv6')[0]

print ('Add DHCPServer layer...')
ixNet.add(ipS, 'dhcpv6server')
ixNet.commit()
dhcpServer = ixNet.getList(ipS, 'dhcpv6server')[0]


print ('Change each Device Group multipliers on server topology...')
ixNet.setAttribute(dgVxlan1, '-multiplier', 2)
ixNet.setAttribute(chained_dgS, '-multiplier', 2)
ixNet.commit()

print ('Ethernet layer under DHCPServer has to be connected to the VXLAN layer...')
print ('Set connecters...')
connector1 = ixNet.getList(ethS, 'connector')[0]
ixNet.setAttribute(connector1, '-connectedTo', vxlan1)
ixNet.commit()


# adding topology with vxlan and dhcp client

print ('\n\nCreate first topology with DHCPclient chained to VXLAN...')

print ('Add topology...')
ixNet.add(root, 'topology')
ixNet.commit()
# the newly added topology is the second 'topology' object type under root
topC = ixNet.getList(root, 'topology')[1]

print ('Add virtual port to topology and change its name...')
ixNet.setMultiAttribute(topC, '-vports', vports[1], '-name', 'vxlan-client')
ixNet.commit()

print ('Add DeviceGroup for VXLAN...')
ixNet.add(topC, 'deviceGroup')
ixNet.commit()
dgVxlan2 = ixNet.getList(topC, 'deviceGroup')[0]

print ('Create the VXLAN stack in this DeviceGroup...')
print ('Add Ethernet layer...')
ixNet.add(dgVxlan2, 'ethernet')
ixNet.commit()
ethV2 = ixNet.getList(dgVxlan2, 'ethernet')[0]

print ('Add IPv4 layer...')
ixNet.add(ethV2, 'ipv4')
ixNet.commit()
ipV2 = ixNet.getList(ethV2, 'ipv4')[0]

print ('Add VxLAN layer...')
ixNet.add(ipV2, 'vxlan')
ixNet.commit()
vxlan2 = ixNet.getList(ipV2, 'vxlan')[0]

print ('Add a chained Device Group to the VXLAN Device Group...')
ixNet.add(dgVxlan2, 'deviceGroup')
ixNet.commit()
chained_dgC = ixNet.getList(dgVxlan2, 'deviceGroup')[0]

print ('Create the DHCPclient stack in this DeviceGroup...')
print ('Add Ethernet layer...')
ixNet.add(chained_dgC, 'ethernet')
ixNet.commit()
ethC = ixNet.getList(chained_dgC, 'ethernet')[0]

print ('Add DHCPclient layer...')
ixNet.add(ethC, 'dhcpv6client')
ixNet.commit()
dhcpClient = ixNet.getList(ethC, 'dhcpv6client')[0]

print ('Change each Device Group multipliers on server topology...')
ixNet.setAttribute(dgVxlan2, '-multiplier', 2)
ixNet.setAttribute(chained_dgC, '-multiplier', 2)
ixNet.commit()

print ('Ethernet layer under DHCPclient has to be connected to the VXLAN layer...')
print ('Set connecters...')
connector2 = ixNet.getList(ethC, 'connector')[0]
ixNet.setAttribute(connector2, '-connectedTo', vxlan2)
ixNet.commit()

# ######################## End Add VxLAN and DHCP DGs ######################## #




# ###################### Configure parameters ################################ #
# ###################### Configure parameters ################################ #
# ###################### Configure parameters ################################ #


# ######################## Configure outer IP ################################ #
#edit IP addresses in DG1 - set decrement step

print ('# ######################## HOW TO set a multivalue attribute ########## #')
print ('\n\nChange outer IP address...')
# ixNet.help(ipV1)
# IP address parameter is a multivalue object
add_mv      = ixNet.getAttribute(ipV1, '-address')

print ('\nTo see childs and attributes of an object just type: "ixNet.help(current_object)". The output should be like this:')
print (ixNet.help(add_mv))

print ('\nAvailable patterns for this multivalue can be found out by using getAttribute on the "-availablePatterns" attribute.')
print ("Output for:  ixNet.getAttribute(add_mv, '-availablePatterns')")
print (ixNet.getAttribute(add_mv, '-availablePatterns'))

print ('\nSelected pattern: counter. Set this pattern under "-pattern" attribute with setAttribute.')
print ("Output for:  ixNet.setAttribute(add_mv, '-pattern', 'counter')")
ixNet.setAttribute(add_mv, '-pattern', 'counter')

print ('\nUse ixNet.commit() to commit changes made with setAttribute.')
ixNet.commit()

add_counter = ixNet.getList(add_mv, 'counter')[0]

print ('Use setMultiAttribute to set more attributes at once.')
ixNet.setMultiAttribute(add_counter, '-direction', 'increment', '-start', '160.0.0.1', '-step', '0.0.0.1')
ixNet.commit()


print ('\nChange outer IP address the same way also for the other IPv4 layer...')
add_mv      = ixNet.getAttribute(ipV2, '-address')
ixNet.setAttribute(add_mv, '-pattern', 'counter')
ixNet.commit()
add_counter = ixNet.getList(add_mv, 'counter')[0]
ixNet.setMultiAttribute(add_counter, '-direction', 'increment', '-start', '160.0.0.100', '-step', '0.0.0.1')
ixNet.commit()
# ######################## Configure outer IP ################################ #



# ######################## Configure outer Gw IP ############################# #
print ('\n\nChange Gw IP...')
gw_mv = ixNet.getAttribute(ipV1, '-gatewayIp')
ixNet.setAttribute(gw_mv, '-pattern', 'counter')
ixNet.commit()
gw_counter = ixNet.getList(gw_mv, 'counter')[0]
ixNet.setMultiAttribute(gw_counter, '-direction', 'increment', '-start', '160.0.0.100', '-step', '0.0.0.1')
ixNet.commit()

gw_mv = ixNet.getAttribute(ipV2, '-gatewayIp')
ixNet.setAttribute(gw_mv, '-pattern', 'counter')
ixNet.commit()
gw_counter = ixNet.getList(gw_mv, 'counter')[0]
ixNet.setMultiAttribute(gw_counter, '-direction', '-direction', 'increment', '-start', '160.0.0.1', '-step', '0.0.0.1')
ixNet.commit()
# ######################## Configure outer Gw IP ############################# #



# ############################ Configure VNIS ################################ #
#edit VNI values and multicast values in DG1 - set increment step

print ('\n\nChange VXLAN - VNIs...')
# --------DG1-------------------------------------------------------------------
vni_mv = ixNet.getAttribute(vxlan1, '-vni')
ixNet.setAttribute(vni_mv, '-pattern', 'custom')
ixNet.commit()
vni_custom = ixNet.getList(vni_mv, 'custom')[0]

ixNet.add(vni_custom, 'increment')
ixNet.commit()

ixNet.setMultiAttribute(vni_custom, '-start', 700, '-step', 10)
ixNet.commit()


# --------DG2-------------------------------------------------------------------
vni_mv = ixNet.getAttribute(vxlan2, '-vni')
ixNet.setAttribute(vni_mv, '-pattern', 'custom')
ixNet.commit()
vni_custom = ixNet.getList(vni_mv, 'custom')[0]

ixNet.add(vni_custom, 'increment')
ixNet.commit()

ixNet.setMultiAttribute(vni_custom, '-start', 700, '-step', 10)
ixNet.commit()
# ############################ Configure VNIS ################################ #



# ######################## Configure multicast IP ############################ #
print ('\n\nChange multicast addresses...')
# --------DG1-------------------------------------------------------------------
vni_mv = ixNet.getAttribute(vxlan1, '-ipv4_multicast')
ixNet.setAttribute(vni_mv, '-pattern', 'counter')
ixNet.commit()
vni_counter = ixNet.getList(vni_mv, 'counter')[0]
ixNet.setMultiAttribute(vni_counter, '-direction', 'increment', '-start', '235.0.0.1', '-step', '0.0.0.1')
ixNet.commit()


# --------DG2-------------------------------------------------------------------
vni_mv = ixNet.getAttribute(vxlan2, '-ipv4_multicast')
ixNet.setAttribute(vni_mv, '-pattern', 'counter')
ixNet.commit()
vni_counter = ixNet.getList(vni_mv, 'counter')[0]
ixNet.setMultiAttribute(vni_counter, '-direction', 'increment', '-start', '235.0.0.1', '-step', '0.0.0.1')
ixNet.commit()
# ######################## Configure multicast IP ############################ #



# #################### Disabling inner IP gateway resolution ################# #
print ("\n\nDisabling inner Gw resolution...")
res_mv=ixNet.getAttribute(ipS, '-resolveGateway')
ixNet.setAttribute(res_mv, '-pattern', 'counter')
ixNet.commit()
res_counter = ixNet.getList(res_mv, 'counter')[0]
ixNet.setMultiAttribute(res_counter, '-direction', 'increment', '-start', 'False', '-step', '0')
ixNet.commit()
# ################### Disabled inner IP gateway resolution ################### #




# ################################### Dynamics ############################### #
print ('# \n####################### HOW TO start/stop/restart protocols ####### #')
#starting VXLAN side topologies
print ("\n\nStarting the VXLAN DGs using ixNet.execute('start', vxlan1)")
ixNet.execute('start', vxlan1)
time.sleep(0.5)
ixNet.execute('start', vxlan2)


# wait for all sessions to start
while (int(ixNet.getAttribute(ipV1, '-stateCounts')[1]) + int(ixNet.getAttribute(ipV2, '-stateCounts')[1])) > 0:
    print ('\nIP layer 1: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(ipV1, '-stateCounts'))))
    print ('IP layer 2: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(ipV2, '-stateCounts'))))
    print ('Waiting for all sessions to be started...')
    time.sleep(3)

print ('IP layer 1: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(ipV1, '-stateCounts'))))
print ('IP layer 2: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(ipV2, '-stateCounts'))))
print ('All IP started...')

# arp retry timeouts in 12 seconds
time.sleep(12)

print ("If ARP fails and IP sessions remain down, protocol can be restarted using ixNet.execute('restartDown', ipV1)")
# if there are any down then restart
if int(ixNet.getAttribute(ipV1, '-stateCounts')[2]) > 0 or int(ixNet.getAttribute(ipV2, '-stateCounts')[2]) > 0:
    print ('\nSome sessions are down, Restart Down is performed...')
    ixNet.execute('restartDown', ipV1)
    time.sleep(1)
    ixNet.execute('restartDown', ipV2)
    time.sleep(12) # arp retry timeouts in 12 seconds
    print ('\nIP layer 1: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(ipV1, '-stateCounts'))))
    print ('IP layer 2: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(ipV2, '-stateCounts'))))


print ("\n\nStarting the DHCP Server Device Group.")
ixNet.execute('start', chained_dgS)

time.sleep(10)
print ('Server sessions are: %s ' % ', '.join(map(str, ixNet.getAttribute(dhcpServer, '-sessionStatus'))))

print ("\n\nStarting the DHCP Client Device Group.")
ixNet.execute('start', chained_dgC)

time.sleep(10)
print ('Client sessions are: %s ' % ', '.join(map(str, ixNet.getAttribute(dhcpClient, '-sessionStatus'))))


#reading VXLAN stats

time.sleep(20)
print ("\n\nRefreshing NGPF statistics views can be done from API using the following exec command: ixNet.execute('refresh', '__allNextGenViews')")
ixNet.execute('refresh', '__allNextGenViews')
time.sleep(3)

mv          = ixNet.getList (ixNet.getRoot(), 'statistics')[0]
view_list   = ixNet.getList (mv, 'view')
print ('\n\nAvailable statistics views are :\n %s ' % '\n '.join(map(str, view_list)))


#stopping per topology

print ('\n\nStop topologies...')
ixNet.execute('stop',topC)

time.sleep(10)
ixNet.execute('stop',topS)


print ("\n\nCleaning up IxNetwork...")
ixNet.execute('newConfig')
ixNet.disconnect()
print ("Done: IxNetwork session is closed...")

