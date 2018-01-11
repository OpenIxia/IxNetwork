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
# The script creates and configures 2 PPP stacks.							   #
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
print ("")

time.sleep(5)
ixNet.execute('clearStats')



# ######################## Add PPP DGs ####################################### #

# adding topology with dhcp server

print ('# \n######## HOW TO create a topology with DGs and various layers ##### #')
print ('\n\nCreate first topology with PPPServer...')

print ('\nAdd topology...')
ixNet.add(root, 'topology')
print ('\nUse ixNet.commit() to commit added child under root.')
ixNet.commit()
print ('\nUse ixNet.getList to get newly added child under root.')
topS = ixNet.getList(root, 'topology')[0]

print ('Add virtual port to topology and change its name...')
ixNet.setMultiAttribute(topS, '-vports', vports[0], '-name', 'PPP server')
ixNet.commit()

print ('Add DeviceGroup for PPP server...')
ixNet.add(topS, 'deviceGroup')
ixNet.commit()
DG1 = ixNet.getList(topS, 'deviceGroup')[0]

print ('Create the PPP server stack in this DeviceGroup...')
print ('Add Ethernet layer...')
ixNet.add(DG1, 'ethernet')
ixNet.commit()
eth1 = ixNet.getList(DG1, 'ethernet')[0]

print ('Add PPP Server layer...')
ixNet.add(eth1, 'pppoxserver')
ixNet.commit()
pppServer = ixNet.getList(eth1, 'pppoxserver')[0]

print ('Change each Device Group multipliers on server topology...')
ixNet.setAttribute(DG1, '-multiplier', 20)
ixNet.commit()


# adding topology with dhcp client

print ('\n\nCreate first topology with PPP client...')

print ('Add topology...')
ixNet.add(root, 'topology')
ixNet.commit()
# the newly added topology is the second 'topology' object type under root
topC = ixNet.getList(root, 'topology')[1]

print ('Add virtual port to topology and change its name...')
ixNet.setMultiAttribute(topC, '-vports', vports[1], '-name', 'PPP client')
ixNet.commit()

print ('Add DeviceGroup for PPP client...')
ixNet.add(topC, 'deviceGroup')
ixNet.commit()
DG2 = ixNet.getList(topC, 'deviceGroup')[0]

print ('Create the client stack in this DeviceGroup...')
print ('Add Ethernet layer...')
ixNet.add(DG2, 'ethernet')
ixNet.commit()
eth2 = ixNet.getList(DG2, 'ethernet')[0]

print ('Add PPP client layer...')
ixNet.add(eth2, 'pppoxclient')
ixNet.commit()
pppClient = ixNet.getList(eth2, 'pppoxclient')[0]

print ('Change each Device Group multipliers on server topology...')
ixNet.setAttribute(DG2, '-multiplier', 20)
ixNet.commit()

# ######################## End Add PPP DGs ################################## #


# ###################### Configure parameters ################################ #
# ###################### Configure parameters ################################ #
# ###################### Configure parameters ################################ #


# ######################## Configure VLAN IDs ################################ #


# #################### Enable VLANs for ethernet layer  ###################### #
print ("\n\nEnable VLANs on both Ethernet layers...")
# print ixNet.help(eth1)
vlan_mv_1      = ixNet.getAttribute(eth1, '-enableVlans')
vlan_mv_2      = ixNet.getAttribute(eth2, '-enableVlans')

ixNet.setAttribute(vlan_mv_1, '-pattern', 'singleValue')
ixNet.setAttribute(vlan_mv_2, '-pattern', 'singleValue')
ixNet.commit()

vlan_mv_1_singleValue = ixNet.getList(vlan_mv_1, 'singleValue')[0]
vlan_mv_2_singleValue = ixNet.getList(vlan_mv_2, 'singleValue')[0]

ixNet.setAttribute(vlan_mv_1_singleValue, '-value', 'true')
ixNet.setAttribute(vlan_mv_2_singleValue, '-value', 'true')
ixNet.commit()
# #################### Enable VLANs for ethernet layer  ###################### #

# ######################## Configure VLAN IDs ################################ #
print ('# ######################## HOW TO set a multivalue attribute ########## #')
print ('\n\nChange VLAN IDs for both Ethernet layers...')
# print ixNet.help(eth1)  # desired attribute is not found on eth

vlan1 = ixNet.getList(eth1, 'vlan')[0]
vlan2 = ixNet.getList(eth2, 'vlan')[0]
# print ixNet.help(vlan1)  # desired attribute is '-vlanId'

# VLAN ID parameter is a multivalue object
vlanID1_mv      = ixNet.getAttribute(vlan1, '-vlanId')
vlanID2_mv      = ixNet.getAttribute(vlan2, '-vlanId')

print ('\nTo see childs and attributes of an object just type: "ixNet.help(current_object)". The output should be like this:')
print ixNet.help(vlanID1_mv)

print ('\nAvailable patterns for this multivalue can be found out by using getAttribute on the "-availablePatterns" attribute.')
print ("Output for:  ixNet.getAttribute(vlanID1_mv, '-availablePatterns')")
print ixNet.getAttribute(vlanID1_mv, '-availablePatterns')

print ('\nSelected pattern: counter. Set this pattern under "-pattern" attribute with setAttribute.')
print ("ixNet.setAttribute(vlanID1_mv, '-pattern', 'counter')")
ixNet.setAttribute(vlanID1_mv, '-pattern', 'counter')
ixNet.setAttribute(vlanID2_mv, '-pattern', 'counter')

print ('\nUse ixNet.commit() to commit changes made with setAttribute.')
ixNet.commit()

vlanID1_mv_counter = ixNet.getList(vlanID1_mv, 'counter')[0]
vlanID2_mv_counter = ixNet.getList(vlanID2_mv, 'counter')[0]

print ('Use setMultiAttribute to set more attributes at once.')
ixNet.setMultiAttribute(vlanID1_mv_counter, '-direction', 'decrement', '-start', '1000', '-step', '5')
ixNet.setMultiAttribute(vlanID2_mv_counter, '-direction', 'decrement', '-start', '1000', '-step', '5')
ixNet.commit()
# ######################## Configure VLAN IDs ################################ #


# ######################## Configure NCP type ################################ #
print ('\n\nChange Ncp Type...')
ncpType_mvC = ixNet.getAttribute(pppClient, '-ncpType')
ncpType_mvS = ixNet.getAttribute(pppServer, '-ncpType')

ixNet.setAttribute(ncpType_mvC, '-pattern', 'singleValue')
ixNet.setAttribute(ncpType_mvS, '-pattern', 'singleValue')
ixNet.commit()

ncpType_mv_singleValueC = ixNet.getList(ncpType_mvC, 'singleValue')[0]
ncpType_mv_singleValueS = ixNet.getList(ncpType_mvS, 'singleValue')[0]

ixNet.setMultiAttribute(ncpType_mv_singleValueC, '-value', 'dual_stack')
ixNet.setMultiAttribute(ncpType_mv_singleValueS, '-value', 'dual_stack')
ixNet.commit()
# ######################## Configure NCP type ################################ #



# ################################### Dynamics ############################### #
print ('# \n####################### HOW TO start/stop/restart protocols ####### #')
#starting topologies
print ("\n\nStarting the topologies using ixNet.execute('start', topS)")
ixNet.execute('start', topS)
time.sleep(0.5)
ixNet.execute('start', topC)


# wait for all sessions to start
while (int(ixNet.getAttribute(pppServer, '-stateCounts')[1]) + int(ixNet.getAttribute(pppClient, '-stateCounts')[1])) > 0:
    print ('\npppServer layer: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(pppServer, '-stateCounts'))))
    print ('pppClient layer: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(pppClient, '-stateCounts'))))
    print ('Waiting for all sessions to be started...')
    time.sleep(3)

print ('pppServer layer: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(pppServer, '-stateCounts'))))
print ('pppClient layer: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(pppClient, '-stateCounts'))))

print ('All sessions started...')
time.sleep(15)

print ('Learned information - Negotiated PPP Client Sessions:')
for i in range(0, len(ixNet.getAttribute(pppClient, '-discoveredIpv4Addresses'))):
    ipv4 = ixNet.getAttribute(pppClient, '-discoveredIpv4Addresses')[i]
    ipv6 = ixNet.getAttribute(pppClient, '-discoveredIpv6Addresses')[i]
    mac = ixNet.getAttribute(pppClient, '-discoveredMacs')[i]
    print ('\n PPP Session %i --> IPV4 Address: %s IPv6 Address: %s Remote MAC Address: %s' % (i+1, ipv4, ipv6, mac))

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

