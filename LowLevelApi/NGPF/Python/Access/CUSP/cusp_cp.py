#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by Keysight                                         #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by  Keysight and     #
# have     																	   #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by  Keysight and/or by the user and/or by a third party)] shall at      #
# all times 																   #
# remain the property of  Keysight.                                            #
#                                                                              #
#  Keysight does not warrant (i) that the functions contained in the script    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND  Keysight    #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL  Keysight BE LIABLE FOR ANY DAMAGES RESULTING FROM OR      #
# ARISING   																   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF  Keysight HAS BEEN ADVISED OF THE              #
# POSSIBILITY OF  SUCH DAMAGES IN ADVANCE.                                     #
#  Keysight will not be required to provide any software maintenance or        #
# support services of any kind (e.g. any error corrections) in connection with #
# script or any part thereof. The user acknowledges that although  Keysight    # 
# may from time to time and in its sole discretion provide maintenance or      #
# support services for the script any such services are subject to the warranty#
# and damages limitations set forth herein and will not obligate  Keysight to  #
# provide any additional maintenance or support services.                      #
#                                                                              #
################################################################################

# ##############################################################################
# Description:                                                                 #
#    This script intends to demonstrate how to use IEEE 802.1x API
#    It will do the  following :
#1.    Add topology and devicegroup 
#2.    Configure ethernet,IPv4,CUSP CP, UP Group Info.
#3.    Add PPPoE server to CP device group
#4.    Set the PPPoE Subscriber group
#5.    Start protocols
#6.    Check for  stats
#7.    Trigger Update request
#8.    OTF change PPPoE subscriber profile value
#9.    Fetch learned info
#10.   Stop protocols
################################################################################
# Module:                                                                      #
#    The sample was tested on a 10GE Novus  module.                            #
#                                                                              #
# ##############################################################################

import time
import os
from IxNetwork import IxNet
ixNet = IxNet()


def assignPorts (ixNet, realPort1) :
    chassis1 = realPort1[0]
    card1 = realPort1[1]
    port1 = realPort1[2]
    root = ixNet.getRoot()
    vport1 = ixNet.add(root, 'vport')
    ixNet.commit()
    vport1 = ixNet.remapIds(vport1)[0]
    chassisObj1 = ixNet.add(root + '/availableHardware', 'chassis')
    ixNet.setAttribute(chassisObj1, '-hostname', chassis1)
    ixNet.commit()
    chassisObj1 = ixNet.remapIds(chassisObj1)[0]

    cardPortRef1 = chassisObj1 + '/card:%s/port:%s' % (card1, port1)
    ixNet.setMultiAttribute(vport1, '-connectedTo', cardPortRef1,
                                 '-rxMode', 'captureAndMeasure', '-name',
                                 'Ethernet - 001')
    ixNet.commit()
# end def assignPorts

# end def assignPorts

################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information  #
# below                                                                        #
################################################################################
ixTclServer = '10.39.65.210'
ixTclPort   = '7601'
ports       = [('10.39.65.190', '1', '27',)]


ixNet = IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.50',
     '-setAttribute', 'strict')

print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

# assigning ports
assignPorts(ixNet, ports[0])
time.sleep(5)
root    = ixNet.getRoot()
vport1 = ixNet.getList(root, 'vport')[0]

print("*************************************************************************************************")
print('\n\nCreate  CUSP CP topology \n\n')
print("*************************************************************************************************")

print ('\nAdding CUSP CP topology...')
cp_topology = ixNet.add(root, 'topology')
ixNet.setMultiAttribute(cp_topology,
                              '-name', 'CUSP CP',
                              '-ports', vport1)
print ('\nUse ixNet.commit() to commit added child under root.')
ixNet.commit()

print ('\n.........Adding CP...............')
cp_device = ixNet.add(cp_topology, 'deviceGroup')
ixNet.setMultiAttribute(cp_device,
                              '-multiplier', '1',
                              '-name', 'CP Device Group')
ixNet.commit()


print ('\nAdd Ethernet to CP ...')
ethernet1 = ixNet.add(cp_device, 'ethernet')
ixNet.commit()
mac = ixNet.getAttribute(ethernet1, '-mac')
mac_val = ixNet.add(mac, 'counter')
ixNet.setMultiAttribute(mac_val,
                        '-step', '00:00:00:00:00:01',
                        '-start', '00:12:01:00:00:01',
                        '-direction', 'increment')
ixNet.commit()

print ('\nAdd ipv4 to CP device')
ixNet.add(ethernet1, 'ipv4')
ixNet.commit()

ip1 = ixNet.getList(ethernet1, 'ipv4')[0]
mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvGw1 = ixNet.getAttribute(ip1, '-gatewayIp')

print ('\n Configuring ipv4 addresses for CP device ...')
ip_address = ixNet.add(mvAdd1, 'singleValue')
gateway_address = ixNet.add(mvGw1, 'singleValue')
ixNet.setMultiAttribute(ip_address, '-value', '1.1.1.1')
ixNet.setMultiAttribute(gateway_address, '-value', '1.1.1.101')
ixNet.commit()

### Disabling IPv4 resolve gateway is only for bringing up the standalone CP device ###
ip1_resolve_gw_mul_val = ixNet.getAttribute(ip1,'-resolveGateway')
ixNet.setAttribute(ip1_resolve_gw_mul_val, '-pattern', 'singleValue')
ixNet.commit()
ip1_gw_single_val = ixNet.getList(ip1_resolve_gw_mul_val, 'singleValue')[0]
ixNet.setAttribute(ip1_gw_single_val,'-value','false')
ixNet.commit()

print ('\n Add CUSP CP in CP device ...')
cuspcp = ixNet.add(ip1, 'cuspCP')
ixNet.setMultiAttribute(cuspcp, '-name', 'CUSP CP')
ixNet.commit()

print ('\n Add UP Group Info ...')
upgroupinfo = ixNet.add(cuspcp, 'upGroupInfo')
ixNet.setMultiAttribute(upgroupinfo, '-name', 'UP Group Info')
ixNet.commit()

print ('\n Add Vxlan GPE ...')
vxlangpe = ixNet.add(ip1, 'vxlangpe')
ixNet.setMultiAttribute(vxlangpe, '-name', 'VXLAN GPE')
ixNet.commit()

# Fetching CP device group details
cp_topo = ixNet.getList(root, 'topology')[0]
deviceGroup_cp = ixNet.getList(cp_topo, 'deviceGroup')[0]
ethernet_cp = ixNet.getList(deviceGroup_cp, 'ethernet')[0]
ipv4_cp = ixNet.getList(ethernet_cp, 'ipv4')[0]
cusp_cp = ixNet.getList(ipv4_cp, 'cuspCP')[0]
upgroupinfo_cp = ixNet.getList(cusp_cp, 'upGroupInfo')[0]

# print handles
print("\n CUSP CP handle is : %s" % cusp_cp)
print("\n UP Group Info handle is : %s" % upgroupinfo_cp)


print ('\n.........Adding PPPoE Server...............')
print('''
Similarly servers can be added for DHCP,L2TP LNS 
''')
cp_dg = ixNet.getList(cp_topology, 'deviceGroup')[0]
pppoe_server_device = ixNet.add(cp_dg, 'deviceGroup')
ixNet.setMultiAttribute(pppoe_server_device,
                              '-multiplier', '1',
                              '-name', 'PPPoE Server')
ixNet.commit()

ethernet2 = ixNet.add(pppoe_server_device, 'ethernet')
ixNet.commit()

pppoe_server = ixNet.add(ethernet2, 'pppoxserver')
ixNet.commit()

print('''
# #############################################################################
#    Set the PPPoE subscriber groups                        ""
# #############################################################################
''')
print('''
Similar command can be used to set for other subscriber groups:
DHCP Subscriber Group ,L2TP Subscriber Group, Static Subscriber Group
''')

pppoe_subscriber_group_cp = ixNet.getAttribute(upgroupinfo_cp,'-numberOfPppoeUsers')
ixNet.setMultiAttribute(upgroupinfo_cp,'-numberOfPppoeUsers', '1',)
ixNet.commit()

print("*************************************************************************************************")
print('\n Starting Protocols \n')
print("*************************************************************************************************")


print("\n Starting CP Device Group")
ixNet.execute('start', deviceGroup_cp)
time.sleep(10)

print ("Fetching all CUSP CP per port Stats\n")
viewPage = '::ixNet::OBJ-/statistics/view:"CUSP CP Per Port"/page'
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

print('''
# #############################################################################
#    Right click actions for sending Update Request                          ""
# #############################################################################
''')
'''
Similar command can be used for all right click actions like:
Start Sending Update Delete Request, Keep Alive Send, Keep Alive Stop
'''
print ("################ Trigger Burst Update Request ####################")

if (ixNet.execute('sendUpdateRequestBursts', upgroupinfo_cp,1) != '::ixNet::OK'):
    print(" Burst Update Request failed to trigger ")

print ("Burst Update Request triggered successfully ")

##############################################################
#####       OTF Change PPPoE Profile value         ###########
##############################################################

#####################################################################
# Similarly values can be changed OTF for L2TP,DHCP,Static profiles #
#####################################################################

print ("##### OTF Change PPPoE Profile value #####")
pppoE_profile=  ixNet.getList(upgroupinfo_cp,'pppoEUsersList')[0]
pppoE_access_type_mul_val = ixNet.getAttribute(pppoE_profile,'-accessType')
ixNet.setAttribute(pppoE_access_type_mul_val, '-pattern', 'singleValue')
ixNet.commit()
pppoE_access_type_single_val = ixNet.getList(pppoE_access_type_mul_val, 'singleValue')[0]
ixNet.setAttribute(pppoE_access_type_single_val,'-value','access_pppoe')
ixNet.commit()
globals = ixNet.getList(root, 'globals')[0]
topology = ixNet.getList(globals, 'topology')[0]
ixNet.execute('applyOnTheFly', topology)
time.sleep(10)

################################################################################
#                Fetch learned info  for PPPoE                                 #
# Similarly learned info can be fetched for UP Resource Info,L2TP, DHCP,Static #                                                           #
################################################################################
print("Fetching CP PPPoE learned info")
ixNet.execute('getPppSubscriberInfo', upgroupinfo_cp, '1')
time.sleep(5)
linfo  = ixNet.getList(upgroupinfo_cp, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
time.sleep(10)

print ("\n\nCleaning up IxNetwork...")
ixNet.execute('newConfig')
print ("\n\nDisconnect IxNetwork...")
ixNet.disconnect()
print ('!!! Test Script Ends !!!')
