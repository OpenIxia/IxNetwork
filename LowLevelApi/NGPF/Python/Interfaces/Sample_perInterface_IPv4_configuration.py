# -*- coding: cp1252 -*-

################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    10/05/2016 - Jayasri Dhar - created sample                                #
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

####################################################################################
#                                                                                  #
# Description:                                                                     #
#    This script intends to demonstrate how to configure IP Address per interface  #
#    It will create 2 ipv4 topologyes, it will generate random ipaddress & gateway #
#    and then will assign those to ipv4 interfaces                                 #
# Module:                                                                          #
#    The sample was tested on an FLexAP module.                                    #
# Software:                                                                        #
#    IxOS      8.01 EA (8.01.1213.5)                                               #
#    IxNetwork 8.01 EA (8.01.1029.6)                                               #
#                                                                                  #
####################################################################################
import os
import sys
import time

def assignPorts (ixNet, realPort1, realPort2) :
     chassis1 = realPort1[0]
     chassis2 = realPort2[0]
     card1    = realPort1[1]
     card2    = realPort2[1]
     port1    = realPort1[2]
     port2    = realPort2[2]

     root = ixNet.getRoot()
     vport1 = ixNet.add(root, 'vport')
     ixNet.commit()
     vport1 = ixNet.remapIds(vport1)[0]

     vport2 = ixNet.add(root, 'vport')
     ixNet.commit()
     vport2 = ixNet.remapIds(vport2)[0]

     chassisObj1 = ixNet.add(root + '/availableHardware', 'chassis')
     ixNet.setAttribute(chassisObj1, '-hostname', chassis1)
     ixNet.commit()
     chassisObj1 = ixNet.remapIds(chassisObj1)[0]

     if (chassis1 != chassis2) :
         chassisObj2 = ixNet.add(root + '/availableHardware', 'chassis')
         ixNet.setAttribute(chassisObj2, '-hostname', chassis2)
         ixNet.commit()
         chassisObj2 = ixNet.remapIds(chassisObj2)[0]
     else :
         chassisObj2 = chassisObj1
     # end if

     cardPortRef1 = chassisObj1 + '/card:%s/port:%s' % (card1,port1)
     ixNet.setMultiAttribute(vport1, '-connectedTo', cardPortRef1,
         '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 001')
     ixNet.commit()

     cardPortRef2 = chassisObj2 + '/card:%s/port:%s' % (card2,port2)
     ixNet.setMultiAttribute(vport2, '-connectedTo', cardPortRef2,
         '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 002')
     ixNet.commit()
# end def assignPorts

################################################################################
# setting number of sessions or interfaces
################################################################################
N = 100

################################################################################
# Using python's random to generate ip address and gateway
################################################################################
import random

r1 = []
r2 = []

random.seed(1)
for i in range(0,N) :
    r1.append(int(random.random()*252)+2)

random.seed(100)
for i in range(0,N) :
    r2.append(int(random.random()*252)+2)

srcAddr = []
destAddr = []

for i in range(0,N) :
    srcAddr.append("40.29.1." + (str(r1[i])))
    destAddr.append("40.30.1." + (str(r2[i])))
#print (srcAddr, destAddr)

# Done generating ip address and gateway

################################################################################
# Either feed the ixNetwork library path in the sys.path as below, or put the
# IxNetwork.pm file somewhere else where we python can autoload it.
# "IxNetwork.pm" is available in <IxNetwork_installer_path>\API\Python
################################################################################
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.01-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.216.108.58'
ixTclPort   = '8009'
ports       = [('10.216.106.15', '2', '1',), ('10.216.106.15', '2', '2',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '7.40',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

# assigning ports
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

root    = ixNet.getRoot()
vportTx = ixNet.getList(root, 'vport')[0]
vportRx = ixNet.getList(root, 'vport')[1]

print("adding topologies")
ixNet.add(root, 'topology', '-vports', vportTx)
ixNet.add(root, 'topology', '-vports', vportRx)
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

print "Adding 2 device groups"
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices[0]
t2dev1 = t2devices[0]

print("Configuring the multipliers (number of sessions or interfaces)")
ixNet.setAttribute(t1dev1, '-multiplier', N)
ixNet.setAttribute(t2dev1, '-multiplier', N)
ixNet.commit()

print("Adding ethernet/mac endpoints")
ixNet.add(t1dev1, 'ethernet')
ixNet.add(t2dev1, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = ixNet.getList(t2dev1, 'ethernet')[0]

print("Configuring the mac addresses %s" % (mac1))
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '18:03:73:C7:6C:B1',
    '-step',      '00:00:00:00:00:01')

ixNet.setMultiAttribute(ixNet.getAttribute(mac2, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '18:03:73:C7:6C:01',
    '-step',      '00:00:00:00:00:01')
    
ixNet.commit()

#print ('ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet\')')
#print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet'))

print("Add ipv4")
ixNet.add(mac1, 'ipv4')
ixNet.add(mac2, 'ipv4')
ixNet.commit()

ip1 = ixNet.getList(mac1, 'ipv4')[0]
ip2 = ixNet.getList(mac2, 'ipv4')[0]

#print ("Print help on : ", ip1)
#print (ixNet.help(ip1))


mvAdd1 = ixNet.getAttribute(ip1, '-address')
# print ("Print help on multiValue ip address : ", mvAdd1)
# print (ixNet.help(mvAdd1))
print("Add ipv4 address overlay! *** ")
indexAdd1 = ixNet.add(mvAdd1, 'overlay')
ixNet.commit()
indexAdd1 = ixNet.remapIds(indexAdd1)[0]

mvAdd2 = ixNet.getAttribute(ip2, '-address')
indexAdd2 = ixNet.add(mvAdd2, 'overlay')
ixNet.commit()
indexAdd2 = ixNet.remapIds(indexAdd2)[0]

mvGw1  = ixNet.getAttribute(ip1, '-gatewayIp')
indexGw1 = ixNet.add(mvGw1, 'overlay')
ixNet.commit()
indexGw1 = ixNet.remapIds(indexGw1)[0]

mvGw2  = ixNet.getAttribute(ip2, '-gatewayIp')
indexGw2 = ixNet.add(mvGw2, 'overlay')
ixNet.commit()
indexGw2 = ixNet.remapIds(indexGw2)[0]

print("configuring ipv4 addresses")

for i in range(0,N) :
    ixNet.setMultiAttribute(indexAdd1, 
            '-count', '1', 
            '-index', i+1, 
            '-value', srcAddr[i])
    ixNet.commit()

    ixNet.setMultiAttribute(indexAdd2, 
            '-count', '1', 
            '-index', i+1, 
            '-value', destAddr[i])
    ixNet.commit()
    
    ixNet.setMultiAttribute(indexGw1, 
            '-count', '1', 
            '-index', i+1, 
            '-value', destAddr[i])
    ixNet.commit()

    ixNet.setMultiAttribute(indexGw2, 
            '-count', '1', 
            '-index', i+1, 
            '-value', srcAddr[i])
    ixNet.commit()

print("done configuring ipv4 addresses!")
