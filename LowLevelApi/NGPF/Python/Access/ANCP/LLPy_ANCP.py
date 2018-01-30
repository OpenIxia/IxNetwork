################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright ? 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/08/2014 - Paul Ganea - created sample                         #
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
# The script creates and configures a topology with one ANCP DG.							   #
# Set/Get multivalue parameters.							                   #
# Start/Stop protocols.                                                        #
# Module:                                                                      #
#    The sample was tested on an XMVDC module.                          #
# Software:                                                                    #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
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
ixNet.connect('localhost', '-port', 8009, '-version', '7.40')

print ("Cleaning up IxNetwork...")
ixNet.execute('newConfig')

# all objects are under root
root = ixNet.getRoot()

print ("\nAdd one virtual port to configuration...")
vports = []
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
ixNet.commit()

print ("Rebooting ports...")
jobs = [ixNet.setAsync().execute('resetPortCpu', vp) for vp in vports]
for j in jobs:
    print j + ' ' + ixNet.getResult(j)
print ("Done... Ports are rebooted...")
print ("")
time.sleep(5)
ixNet.execute('clearStats')

# ######################## Add ANCP DGs ####################################### #
print ('# \n######## HOW TO create a topology with one DG and various layers ##### #')
print ('\n\nCreate first the topology...')
print ('\nAdd topology...')
ixNet.add(root, 'topology')
print ('\nUse ixNet.commit() to commit added child under root.')
ixNet.commit()

print ('\nUse ixNet.getList to get newly added child under root.')
topANCP = ixNet.getList(root, 'topology')[0]
print ('Add virtual port to topology and change its name...')
ixNet.setMultiAttribute(topANCP, '-vports', vports[0], '-name', 'AN Topology')
ixNet.commit()

print ('Add DeviceGroup for ANCP...')
ixNet.add(topANCP, 'deviceGroup')
ixNet.commit()

DG = ixNet.getList(topANCP, 'deviceGroup')[0]
print ('Create the ANCP stack in this DeviceGroup...')
print ('Add Ethernet layer...')
ixNet.add(DG, 'ethernet')
ixNet.commit()

eth = ixNet.getList(DG, 'ethernet')[0]
print ('Add the IP layer...')
ixNet.add(eth, 'ipv4')
ixNet.commit()

ip = ixNet.getList(eth, 'ipv4')[0]
print ('Add the ANCP layer...')
ixNet.add(ip, 'ancp')
ixNet.commit()

ancp = ixNet.getList(ip, 'ancp')[0]
print ('Chain the DSL lines Network Group to the ANCP DG...')
ixNet.add(DG, 'networkGroup')
ixNet.commit()

netGr = ixNet.getList(DG, 'networkGroup')[0]
ixNet.add(netGr, 'dslPools')
ixNet.commit()

dsl = ixNet.getList(netGr, 'dslPools')[0]
print ('Change each Device Group multiplier...')
ixNet.setAttribute(DG, '-multiplier', 5)
ixNet.commit()

ixNet.setAttribute(netGr, '-multiplier', 10)
ixNet.commit()

# ######################## End Add ANCP DGs ################################## #
# ###################### Configure parameters ################################ #
# ###################### Configure parameters ################################ #
# ###################### Configure parameters ################################ #
# ######################## Configure VLAN IDs ################################ #
# #################### Enable VLANs for ethernet layer  ###################### #

print ("\n\nEnable VLANs on both Ethernet layers...")
# print ixNet.help(eth)
vlan      = ixNet.getAttribute(eth, '-enableVlans')
vlan_value = ixNet.getList(vlan, 'singleValue')
ixNet.setAttribute(vlan_value[0], '-value', 'True')
ixNet.commit()

# #################### Enabled VLANs for ethernet layer  ###################### #
# ######################## Configure VLAN IDs ################################ #
print ('# ######################## HOW TO set a multivalue attribute ########## #')

print ('\n\nChange VLAN IDs for both Ethernet layers...')
# print ixNet.help(eth)  # desired attribute is not found on eth
vlan = ixNet.getList(eth, 'vlan')[0]
# print ixNet.help(vlan)  # desired attribute is '-vlanId'
# VLAN ID parameter is a multivalue object
vlanID_mv      = ixNet.getAttribute(vlan, '-vlanId')

print ('\nTo see childs and attributes of an object just type: "ixNet.help(current_object)". The output should be like this:')
print ixNet.help(vlanID_mv)

print ('\nAvailable patterns for this multivalue can be found out by using getAttribute on the "-availablePatterns" attribute.')
print ("Output for:  ixNet.getAttribute(vlanID1_mv, '-availablePatterns')")
print ixNet.getAttribute(vlanID_mv, '-availablePatterns')

print ('\nSelected pattern: counter. Set this pattern under "-pattern" attribute with setAttribute.')
print ("ixNet.setAttribute(vlanID_mv, '-pattern', 'singleValue')")
ixNet.setAttribute(vlanID_mv, '-pattern', 'singleValue')

print ('\nUse ixNet.commit() to commit changes made with setAttribute.')
ixNet.commit()

vlanID_mv_value = ixNet.getList(vlanID_mv, 'singleValue')[0]

print ('Use setMultiAttribute to set more attributes at once.')
ixNet.setMultiAttribute(vlanID_mv_value, '-value', '5')
ixNet.commit()

# ######################## Configured VLAN IDs ################################ #
# ######################## Configure AN IP Values ################################ #

print ('\n\nChange AN IP...')
ip_add = ixNet.getAttribute(ip, '-address')
ip_add_counter = ixNet.getList(ip_add, 'counter')
ixNet.setMultiAttribute(ip_add_counter[0], '-direction', 'increment', '-start', '5.5.5.5', '-step', '0.0.0.1')
ixNet.commit()

# ######################## Configured AN IP Values ################################ #
# ######################## Configure AN Gateway IP Values ################################ #

gw = ixNet.getAttribute(ip, '-gatewayIp')
gw_counter = ixNet.getList(gw, 'counter')
ixNet.setMultiAttribute(gw_counter[0], '-direction', 'increment', '-start', '5.5.5.1', '-step', '0.0.0.0')
ixNet.commit()

# ######################## Configured AN Gateway IP Values ################################ #
# ######################## Configure NAS IP Values ################################ #

nasip = ixNet.getAttribute(ancp, '-nasIp')
nasip_counter = ixNet.getList(nasip, 'counter')
ixNet.setMultiAttribute(nasip_counter[0], '-direction', 'increment', '-start', '5.5.5.1', '-step', '0.0.0.0')
ixNet.commit()

# ######################### Configured NAS IP Values ############################### #
# ######################## Enable Trigger Access Loops Parameter ################################ #

trigger = ixNet.getAttribute(ancp, '-triggerAccessLoopEvents')
trigger_value = ixNet.getList(trigger, 'singleValue')
ixNet.setAttribute(trigger_value[0], '-value', 'True')
ixNet.commit()

# ######################## Enabled Trigger Access Loops Parameter ################################ #
# ######################## Enable Remote ID Parameter on DSL lines################################ #

remoteID = ixNet.getAttribute(dsl, '-enableRemoteId')
remoteID_value = ixNet.getList(remoteID, 'singleValue')
ixNet.setAttribute(remoteID_value[0], '-value', 'True')
ixNet.commit()

# ######################## Enabled Remote ID Parameter on DSL lines################################ #
# ################################### Dynamics ############################### #

print ('# \n####################### HOW TO start/stop/restart protocols ####### #')
#starting topologies
print ("\n\nStarting the topologies using ixNet.execute('start', topANCP)")
ixNet.execute('start', topANCP)
# wait for all sessions to start

while (int(ixNet.getAttribute(ancp, '-stateCounts')[1])) > 0:
    print ('ancp layer: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(ancp, '-stateCounts'))))
    print ('Waiting for all sessions to be started...')
    time.sleep(3)
print ('ancp layer: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: %s ' % ', '.join(map(str, ixNet.getAttribute(ancp, '-stateCounts'))))
print ('All sessions started...')
time.sleep(15)

print ("\n\nRefreshing NGPF statistics views can be done from API using the following exec command: ixNet.execute('refresh', '__allNextGenViews')")
ixNet.execute('refresh', '__allNextGenViews')
time.sleep(3)
mv          = ixNet.getList (ixNet.getRoot(), 'statistics')[0]
view_list   = ixNet.getList (mv, 'view')

print ('\n\nAvailable statistics views are :\n %s ' % '\n '.join(map(str, view_list)))
#stopping per topology

print ('\n\nStop ANCP topology...')
ixNet.execute('stop',topANCP)
time.sleep(10)

print ("\n\nCleaning up IxNetwork...")
ixNet.execute('newConfig')

ixNet.disconnect()
print ("Done: IxNetwork session is closed...")
