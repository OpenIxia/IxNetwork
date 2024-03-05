# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
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
#    This script intends to demonstrate how to use Low Level Python APIs to    #
#    import BGP IPv4 Routes in Ixia csv format.                                #
#    1. It will create 2 BGP topologies.                                       #
#    2. Generate Statistical IPv4 routes in topology2.                         #
#    3. Start the BGP protocol.                                                #
#    4. Retrieve protocol statistics.                                          #
#    5. Retrieve protocol learned info.                                        #
#    6. Stop all protocols.                                                    #
#                                                                              #
################################################################################
import os
import sys
import time

import generateIpMacCsv
import overLay1Bit

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
# Either feed the ixNetwork library path in the sys.path as below, or put the  #
# IxNetwork.py file somewhere else where we python can autoload it             #
# "IxNetwork.py" is available in <IxNetwork_installer_path>\API\Python         #
################################################################################
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.20-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information   #
# below                                                                         #
#################################################################################
ixTclServer = '10.216.108.113'
ixTclPort   = '8074'
ports       = [('10.216.108.96', '6', '3',), ('10.216.108.96', '6', '4',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client %s %s" % (ixTclServer, ixTclPort))
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.20',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

# assigning ports
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

root       = ixNet.getRoot()
vportTx    = ixNet.getList(root, 'vport')[0]
vportRx    = ixNet.getList(root, 'vport')[1]
multiplier = 100
csvPath1   = './scaleStack.csv'
csvPath2   = './myOneBit.csv'

print("adding topologies")
ixNet.add(root, 'topology', '-vports', vportTx)
ixNet.add(root, 'topology', '-vports', vportRx)
ixNet.commit()

###############################################################################
# Add topologies
###############################################################################
topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

print ("Adding 2 device groups")
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

###############################################################################
# Add device group
###############################################################################
t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices[0]
t2dev1 = t2devices[0]

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(t1dev1, '-multiplier', multiplier)
ixNet.setAttribute(t2dev1, '-multiplier', multiplier)
ixNet.commit()

################################################################################
# Adding ethernet/mac endpoints
################################################################################
print("Adding ethernet/mac endpoints")
ixNet.add(t1dev1, 'ethernet')
ixNet.add(t2dev1, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = ixNet.getList(t2dev1, 'ethernet')[0]

###############################################################################
# Create a multivalue CSV
###############################################################################
myMultiValueCsv = generateIpMacCsv.MultivalueCsv(csvPath1, multiplier)
myMultiValueCsv.generate()

################################################################################
# Read MAC address from .csv file for port 1
################################################################################
macAddrMv1 = ixNet.getAttribute(mac1, '-mac')
valueListMv1 = ixNet.add(macAddrMv1, 'valueList')
ixNet.execute('import', valueListMv1, ixNet.readFrom(csvPath1), "csv", '0')
ixNet.commit()

################################################################################
# Read MAC address from .csv file port 2
################################################################################
macAddrMv2 = ixNet.getAttribute(mac2, '-mac')
valueListMv2 = ixNet.add(macAddrMv2, 'valueList')
ixNet.execute('import', valueListMv2, ixNet.readFrom(csvPath1), "csv", '1')
ixNet.commit()

#################################################################################
# Adding IPv4 Layer
#################################################################################
print("Add ipv4")
ixNet.add(mac1, 'ipv4')
ixNet.add(mac2, 'ipv4')
ixNet.commit()

ip1               = ixNet.getList(mac1, 'ipv4')[0]
mvAdd1            = ixNet.getAttribute(ip1, '-address')
mvIpAddValuelist1 = ixNet.add(mvAdd1, 'valueList')
mvGw1             = ixNet.getAttribute(ip1, '-gatewayIp')
mvGwAddValuelist1 = ixNet.add(mvGw1, 'valueList')

ixNet.execute('import', mvIpAddValuelist1, ixNet.readFrom(csvPath1), "csv", '4')
ixNet.execute('import', mvGwAddValuelist1, ixNet.readFrom(csvPath1), "csv", '5')
ixNet.commit()

ip2               = ixNet.getList(mac2, 'ipv4')[0]
mvAdd2            = ixNet.getAttribute(ip2, '-address')
mvIpAddValuelist2 = ixNet.add(mvAdd2, 'valueList')
mvGw2             = ixNet.getAttribute(ip2, '-gatewayIp')
mvGwAddValuelist2 = ixNet.add(mvGw2, 'valueList')

ixNet.execute('import', mvIpAddValuelist2, ixNet.readFrom(csvPath1), "csv", '5')
ixNet.execute('import', mvGwAddValuelist2, ixNet.readFrom(csvPath1), "csv", '4')
ixNet.commit()

#################################################################################
# Adding OSPFv2 
#################################################################################
print("Adding OSPFv2")
ixNet.add(ip1, 'ospfv2')
ixNet.add(ip2, 'ospfv2')
ixNet.commit()

ospfv2Router1 = ixNet.getList(ip1, 'ospfv2')[0]
ospfv2Router2 = ixNet.getList(ip2, 'ospfv2')[0]

networkTypeMv1 = ixNet.getAttribute(ospfv2Router1, '-networkType')
ixNet.setAttribute(networkTypeMv1 + '/singleValue', '-value', 'pointtopoint')
ixNet.commit()

networkTypeMv2 = ixNet.getAttribute(ospfv2Router2, '-networkType')
ixNet.setAttribute(networkTypeMv2 + '/singleValue', '-value', 'pointtopoint')
ixNet.commit()

#################################################################################
# Generate boolean valuelist 
#################################################################################
myOneBitValue = overLay1Bit.OneBitValue(csvPath2, 10, 10)
myOneBitValue.generate()

activeBitMv = ixNet.getAttribute(ospfv2Router1, '-active')
activeBitMvValueList = ixNet.add(activeBitMv, 'valueList')
ixNet.execute('import', activeBitMvValueList, ixNet.readFrom(csvPath2), "csv", '0')
ixNet.commit()
