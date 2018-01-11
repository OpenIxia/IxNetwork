################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright ? 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    13/08/2013 - Alexandra Apetroaei - created sample                         #
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
# The script creates and configures 2 DHCP stacks.							   #
# Set/Get multivalue parameters.							                   #
# Start/Stop protocols.                                                        #
# Module:                                                                      #
#    The sample was tested on an FlexAP10G16S module.                          #
# Software:                                                                    #
#    IxOS      6.70 EA                                                         #
#    IxNetwork 7.30 EA                                                         #
#                                                                              #
################################################################################



# import Python packages
import time
import os
from IxNetwork import IxNet

# create an instance of the IxNet class
ixNet = IxNet()

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
    print j + ' ' + ixNet.getResult(j)
print ("Done... Ports are rebooted...")


time.sleep(5)
ixNet.execute('clearStats')



# ######################## Add DHCP DGs ####################################### #

# adding topology with dhcp server

print ('# \n######## HOW TO create a topology with DGs and various layers ##### #')
print ('\n\nCreate first topology with DHCPServer...')

print ('\nAdd topology...')
ixNet.add(root, 'topology')
print ('\nUse ixNet.commit() to commit added child under root.')
ixNet.commit()
print ('\nUse ixNet.getList to get newly added child under root.')
topS = ixNet.getList(root, 'topology')[0]

print ('Add virtual port to topology and change its name...')
ixNet.setMultiAttribute(topS, '-vports', vports[0], '-name', 'DHCPserver')
ixNet.commit()

print ('Add DeviceGroup for DHCPserver...')
ixNet.add(topS, 'deviceGroup')
ixNet.commit()
DG1 = ixNet.getList(topS, 'deviceGroup')[0]

print ('Create the DHCPserver stack in this DeviceGroup...')
print ('Add Ethernet layer...')
ixNet.add(DG1, 'ethernet')
ixNet.commit()
eth1 = ixNet.getList(DG1, 'ethernet')[0]

print ('Add IPv4 layer...')
ixNet.add(eth1, 'ipv6')
ixNet.commit()
ip1 = ixNet.getList(eth1, 'ipv6')[0]

print ('Add DHCPServer layer...')
ixNet.add(ip1, 'dhcpv6server')
ixNet.commit()
dhcpServer = ixNet.getList(ip1, 'dhcpv6server')[0]

print ('Change each Device Group multipliers on server topology...')
ixNet.setAttribute(DG1, '-multiplier', 2)
ixNet.commit()


# adding topology with dhcp client

print ('\n\nCreate first topology with DHCPclient...')

print ('Add topology...')
ixNet.add(root, 'topology')
ixNet.commit()
# the newly added topology is the second 'topology' object type under root
topC = ixNet.getList(root, 'topology')[1]

print ('Add virtual port to topology and change its name...')
ixNet.setMultiAttribute(topC, '-vports', vports[1], '-name', 'DHCP client')
ixNet.commit()

print ('Add DeviceGroup for DHCPclient...')
ixNet.add(topC, 'deviceGroup')
ixNet.commit()
DG2 = ixNet.getList(topC, 'deviceGroup')[0]

print ('Create the client stack in this DeviceGroup...')
print ('Add Ethernet layer...')
ixNet.add(DG2, 'ethernet')
ixNet.commit()
eth2 = ixNet.getList(DG2, 'ethernet')[0]

print ('Add DHCPclient layer...')
ixNet.add(eth2, 'dhcpv6client')
ixNet.commit()
dhcpClient = ixNet.getList(eth2, 'dhcpv6client')[0]

print ('Change each Device Group multipliers on server topology...')
ixNet.setAttribute(DG2, '-multiplier', 10)
ixNet.commit()

# ######################## End Add DHCP DGs ################################## #


# ###################### Configure parameters ################################ #
# ###################### Configure parameters ################################ #
# ###################### Configure parameters ################################ #


# ######################## Configure pool of addresses ####################### #
print ('# ######################## HOW TO set a multivalue attribute ########## #')
print ('\n\nChange Start Pool Address for DHCP Server...')
# print ixNet.help(dhcpServer)  # desired attribute is not found on dhcpServer

serverSess = ixNet.getList(dhcpServer, 'dhcp6ServerSessions')[0]
# print ixNet.help(serverSess)  # desired attribute is '-ipAddressPD'

# IP address parameter is a multivalue object
add_mv      = ixNet.getAttribute(serverSess, '-ipAddressPD')

print ('\nTo see childs and attributes of an object just type: "ixNet.help(current_object)". The output should be like this:')
print ixNet.help(add_mv)

print ('\nAvailable patterns for this multivalue can be found out by using getAttribute on the "-availablePatterns" attribute.')
print ("Output for:  ixNet.getAttribute(add_mv, '-availablePatterns')")
print ixNet.getAttribute(add_mv, '-availablePatterns')

print ('\nSelected pattern: counter. Set this pattern under "-pattern" attribute with setAttribute.')
print ("ixNet.setAttribute(add_mv, '-pattern', 'counter')")
ixNet.setAttribute(add_mv, '-pattern', 'counter')

print ('\nUse ixNet.commit() to commit changes made with setAttribute.')
ixNet.commit()

add_counter = ixNet.getList(add_mv, 'counter')[0]

print ('Use setMultiAttribute to set more attributes at once.')
ixNet.setMultiAttribute(add_counter, '-direction', 'increment', '-start', 'cd::0', '-step', '0:1::')
ixNet.commit()
# ######################## Configure pool of addresses ####################### #


# ######################## Configure Pool size ############################### #
print ('\n\nChange Pool size...')
size_mv = ixNet.getAttribute(serverSess, '-poolPrefixSize')
ixNet.setAttribute(size_mv, '-pattern', 'singleValue')
ixNet.commit()
size_mv_singleValue = ixNet.getList(size_mv, 'singleValue')[0]
ixNet.setMultiAttribute(size_mv_singleValue, '-value', '20')
ixNet.commit()
# ######################## Configure Pool size ############################### #


# #################### Disabling  IP gateway resolution ###################### #
print ("\n\nDisabling Gw resolution...")
res_mv=ixNet.getAttribute(ip1, '-resolveGateway')
ixNet.setAttribute(res_mv, '-pattern', 'counter')
ixNet.commit()
res_counter = ixNet.getList(res_mv, 'counter')[0]
ixNet.setMultiAttribute(res_counter, '-direction', 'increment', '-start', 'False', '-step', '0')
ixNet.commit()
# ################### Disabled IP gateway resolution ######################### #



# ################################### Dynamics ############################### #
print ('# \n####################### HOW TO start/stop/restart protocols ####### #')
#starting topologies
print ("\n\nStarting the topologies using ixNet.execute('start', topS)")
ixNet.execute('start', topS)
time.sleep(0.5)
ixNet.execute('start', topC)


# wait for all sessions to start
while (int(ixNet.getAttribute(dhcpServer, '-stateCounts')[1]) + int(ixNet.getAttribute(dhcpClient, '-stateCounts')[1])) > 0:
    print ('\ndhcpServer layer: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(dhcpServer, '-stateCounts'))))
    print ('dhcpClient layer: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(dhcpClient, '-stateCounts'))))
    print ('Waiting for all sessions to be started...')
    time.sleep(3)

print ('dhcpServer layer: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(dhcpServer, '-stateCounts'))))
print ('dhcpClient layer: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(dhcpClient, '-stateCounts'))))

print ('All sessions started...')
time.sleep(15)

print ('Learned information - Negotiated client addresses:')
print ('\n'.join(map(str, ixNet.getAttribute(dhcpClient, '-discoveredPrefix'))))

print ("\n\nRenewing the client leases using ixNet.execute('renew', dhcpClient)")
ixNet.execute('renew', dhcpClient)

#reading stats

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

