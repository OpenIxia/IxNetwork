# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    05/12/2015 - Rupkatha Guha - created sample                           #
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
#    This script intends to demonstrate how to use NGPF BFDv6 API              #
#    It will create 2 BFDv4 topologies over VXLAN, it will start the emulation and        #
#    than it will retrieve and display few statistics                          #
# Module:                                                                      #
#    The sample was tested on an XMVDC16 module.                               #
# Software:                                                                    #
#    IxOS      8.20 EA                                                         #
#    IxNetwork 8.20 EA                                                         #
#                                                                              #
################################################################################
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
# Either feed the ixNetwork library path in the sys.path as below, or put the  #
# IxNetwork.py file somewhere else where we python can autoload it             #
# "IxNetwork.py" is available in <IxNetwork_installer_path>\API\Python         #
################################################################################
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.20.0.219-EB\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information   #
# below                                                                         #
#################################################################################
ixTclServer = '10.216.22.32'
ixTclPort   = '8009'
ports       = [('10.216.100.12', '2', '3',), ('10.216.100.12', '2', '4',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.20',
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

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(t1dev1, '-multiplier', '1')
ixNet.setAttribute(t2dev1, '-multiplier', '1')
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

ixNet.setAttribute(ixNet.getAttribute(mac2, '-mac') + '/singleValue',
    '-value', '18:03:73:C7:6C:01')
ixNet.commit()

print ('ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet\')')
print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet'))

print("Add ipv4")
ixNet.add(mac1, 'ipv4')
ixNet.add(mac2, 'ipv4')
ixNet.commit()

ip1 = ixNet.getList(mac1, 'ipv4')[0]
ip2 = ixNet.getList(mac2, 'ipv4')[0]

mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvAdd2 = ixNet.getAttribute(ip2, '-address')
mvGw1  = ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = ixNet.getAttribute(ip2, '-gatewayIp')

print("configuring ipv4 addresses")
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '20.20.20.2')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '20.20.20.2')

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

print ('ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4\')')
print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4'))

###########################################################################
#Add and Configure VXLAN Interface 
###########################################################################
print("Adding BFDv4 and Configuring")
ixNet.add(ip1, 'vxlan')
ixNet.add(ip2, 'vxlan')
ixNet.commit()

vxlan1 = ixNet.getList(ip1, 'vxlan')[0]
vxlan2 = ixNet.getList(ip2, 'vxlan')[0]
vni2 = ixNet.getAttribute(vxlan2, '-vni')
ipv4_multicast = ixNet.getAttribute(vxlan2, '-ipv4_multicast')
ixNet.setAttribute(vni2 + '/singleValue', '-value', '1000')
ixNet.setAttribute(ipv4_multicast + '/singleValue', '-value', '225.0.1.1')


###########################################################################
#Add and Configure BFDv4 Interface 
###########################################################################
print("Adding BFDv4 and Configuring")
ixNet.add(vxlan1, 'bfdv4Interface')
ixNet.add(vxlan2, 'bfdv4Interface')
ixNet.commit()

bfdv41 = ixNet.getList(vxlan1, 'bfdv4Interface')[0]
bfdv42 = ixNet.getList(vxlan2, 'bfdv4Interface')[0]
bfdv4session1 = ixNet.getList(bfdv41, 'bfdv4Session')[0]
bfdv4session2 = ixNet.getList(bfdv42, 'bfdv4Session')[0]
remoteIP1 = ixNet.getAttribute(bfdv4session1, '-remoteIp4')
remoteIP2 = ixNet.getAttribute(bfdv4session2, '-remoteIp4')
remoteMac1 = ixNet.getAttribute(bfdv4session1, '-remoteMac')
remoteMac2 = ixNet.getAttribute(bfdv4session2, '-remoteMac')
ixNet.setAttribute(remoteIP1 + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(remoteIP2 + '/singleValue', '-value', '20.20.20.2')
ixNet.setAttribute(remoteMac1 + '/singleValue', '-value', '18:03:73:C7:6C:01')
ixNet.setAttribute(remoteMac2 + '/singleValue', '-value', '18:03:73:C7:6C:B1')


ixNet.commit()

txInterval1 = ixNet.getAttribute(bfdv41, '-txInterval')
txInterval2 = ixNet.getAttribute(bfdv42, '-txInterval')
minRxInterval1 = ixNet.getAttribute(bfdv41, '-minRxInterval')
minRxInterval2 = ixNet.getAttribute(bfdv42, '-minRxInterval')


ixNet.setAttribute(txInterval1 + '/singleValue', '-value', '2000')
ixNet.setAttribute(txInterval2 + '/singleValue', '-value', '2000')
ixNet.setAttribute(minRxInterval1 + '/singleValue', '-value', '2000')
ixNet.setAttribute(minRxInterval2 + '/singleValue', '-value', '2000')


ixNet.commit()

print('ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/bfdv4Interface\')')
print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/bfdv4Interface'))


################################################################################
# Start BFD protocol and wait for 45 seconds                                   #
################################################################################
print("Starting protocols and waiting for 45 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(45)

################################################################################
# Retrieve protocol statistics                                              #
################################################################################
print ("Fetching all Protocol Summary Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for

############################################################################
##On The Fly Section
############################################################################
print("Deactivating and Activating BFDv4 Interface On the fly")
activation = ixNet.getAttribute(bfdv41, '-active')

ixNet.setAttribute(activation +'/singleValue', '-value', 'false')
ixNet.commit()
globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")

time.sleep(10)
ixNet.setAttribute(activation +'/singleValue', '-value', 'true')
ixNet.commit()
globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")
# end try/expect
time.sleep(10)

###############################################################################
# Retrieve protocol learned info                                              # 
###############################################################################
print("Fetching BFD learned info")
ixNet.execute('getLearnedInfo', bfdv41, '1')
time.sleep(5)
linfo  = ixNet.getList(bfdv41, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# Stop all protocols                                                           #
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
