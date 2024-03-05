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
# damages limitations forth herein and will not obligate Ixia to provide       #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF Fabric Path APIs       #
#                                                                              #
#    1. It will create one Fabric Path RBridge per topology in two ports.      #
#       Behind RBridge it will add FAT Tree network topology. Behind network   #
#       topology it will add Fabric Path simulated edge RBRidge. Behind        #
#       simulated edge, it will add MAC pool which will serve as endpoints     #
#       in traffic.                                                            #
#    2. Start all protocols.                                                   #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Chnage some fields and apply change on the fly                         #
#    6. Configure L2-L3 traffic.                                               #
#    7. Start the L2-L3 traffic.                                               #
#    8. Retrieve L2-L3 traffic stats.                                          #
#    9. Stop L2-L3 traffic.                                                    #
#   10. Stop all protocols.                                                    #
#                                                                              #
################################################################################

# Script Starts
print("!!! Test Script Starts !!!")

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
# Either feed the ixNetwork library path in the sys.path as below, or put the
# IxNetwork.pm file somewhere else where we python can autoload it.
# "IxNetwork.pm" is available in <IxNetwork_installer_path>\API\Python
################################################################################
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\7.40-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.205.25.88'
ixTclPort   = '8009'
ports       = [('10.205.27.69', '2', '1',), ('10.205.27.69', '2', '2',)]

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
root   = ixNet.getRoot()
vport1 = ixNet.getList(root, 'vport')[0]
vport2 = ixNet.getList(root, 'vport')[1]

print("Adding 2 topologies")
ixNet.add(root, 'topology', '-vports', vport1)
ixNet.add(root, 'topology', '-vports', vport2)
ixNet.commit()

topologies = ixNet.getList(root, 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'Topology 1 for Fabric Path')
ixNet.setAttribute(topo2, '-name', 'Topology 2 for Fabric Path')

print("Adding 2 device groups")
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices[0]
t2dev1 = t2devices[0]

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(t1dev1, '-multiplier', 1)
ixNet.setAttribute(t2dev1, '-multiplier', 1)
ixNet.commit()

print("Adding ethernet/mac endpoints")
ixNet.add(t1dev1, 'ethernet')
ixNet.add(t2dev1, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = ixNet.getList(t2dev1, 'ethernet')[0]

print("Configuring the mac addresses")
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-mac') + '/counter',
    '-direction',  'increment',
    '-start', '18:03:73:C7:6C:B1',
    '-step', '00:00:00:00:00:01')

ixNet.setAttribute(ixNet.getAttribute(mac2, '-mac') + '/singleValue',
    '-value', '18:03:73:C7:6C:01')
ixNet.commit()

print("Adding Fabric Path interfaces")
ixNet.add(mac1, 'isisFabricPath')
ixNet.add(mac2, 'isisFabricPath')
ixNet.commit()

fabricPathIf1 = ixNet.getList(mac1, 'isisFabricPath')[0]
fabricPathIf2 = ixNet.getList(mac2, 'isisFabricPath')[0]

print("Setting discard LSP off in Fabric Path Routers")
fabricPathRouter1 = ixNet.getList(t1dev1, 'isisFabricPathRouter')[0]
fabricPathRouter2 = ixNet.getList(t2dev1, 'isisFabricPathRouter')[0]
mv1 = ixNet.getAttribute(fabricPathRouter1, '-discardLSPs')
mv2 = ixNet.getAttribute(fabricPathRouter2, '-discardLSPs')
ixNet.setAttribute(mv1, '-pattern', 'singleValue')
ixNet.setAttribute(mv2, '-pattern', 'singleValue')
ixNet.commit()

ixNet.setAttribute(mv1 + '/singleValue', '-value', 'false')
ixNet.setAttribute(mv2 + '/singleValue', '-value', 'false')
ixNet.commit()

print("Setting Mulitcast IPv4 group in Fabric Path Router 2")
ixNet.setAttribute(fabricPathRouter2, '-dceMCastIpv4GroupCount', 1)
ixNet.commit()

dceMCastIpv4GroupList = ixNet.getList(fabricPathRouter2, 'dceMCastIpv4GroupList')[0]
mvMcastAddrCount = ixNet.getAttribute(dceMCastIpv4GroupList, '-mcastAddrCnt')
mvStartMcastAddr = ixNet.getAttribute(dceMCastIpv4GroupList, '-startMcastAddr')

ixNet.setAttribute(mvMcastAddrCount, '-pattern', 'singleValue')
ixNet.setAttribute(mvMcastAddrCount + '/singleValue', '-value', 2)
ixNet.setAttribute(mvStartMcastAddr, '-pattern', 'singleValue')
ixNet.setAttribute(mvStartMcastAddr + '/singleValue', '-value', '230.0.0.1')
ixNet.commit()

print("Setting Multicast MAC Groups in Fabric Path Router 2")
ixNet.setAttribute(fabricPathRouter2, '-dceMCastMacGroupCount', 1)
ixNet.commit()

dceMCastMacGroupList = ixNet.getList(fabricPathRouter2, 'dceMCastMacGroupList')[0]

mvMcastAddrCount = ixNet.getAttribute(dceMCastMacGroupList, '-mcastAddrCnt')
mvStartMcastAddr = ixNet.getAttribute(dceMCastMacGroupList, '-startMcastAddr')

ixNet.setAttribute(mvMcastAddrCount, '-pattern', 'singleValue')
ixNet.setAttribute(mvMcastAddrCount + '/singleValue', '-value', 2)
ixNet.setAttribute(mvStartMcastAddr, '-pattern', 'singleValue')
ixNet.setAttribute(mvStartMcastAddr + '/singleValue', '-value', '01:55:55:55:55:55')
ixNet.commit()

print("Setting Mulitcast IPv6 group in Fabric Path Router 2")
ixNet.setAttribute(fabricPathRouter2, '-dceMCastIpv6GroupCount', 1)
ixNet.commit()

dceMCastIpv6GroupList = ixNet.getList(fabricPathRouter2, 'dceMCastIpv6GroupList')[0]
mvMcastAddrCount = ixNet.getAttribute(dceMCastIpv6GroupList, '-mcastAddrCnt')
mvStartMcastAddr = ixNet.getAttribute(dceMCastIpv6GroupList, '-startMcastAddr')

ixNet.setAttribute(mvMcastAddrCount, '-pattern', 'singleValue')
ixNet.setAttribute(mvMcastAddrCount + '/singleValue', '-value', 2)
ixNet.setAttribute(mvStartMcastAddr, '-pattern', 'singleValue')
ixNet.setAttribute(mvStartMcastAddr + '/singleValue', '-value', 'ff03::1111')
ixNet.commit()

print("Adding network group with FAT tree topology")
ixNet.add(t1dev1, 'networkGroup')
ixNet.add(t2dev1, 'networkGroup')
ixNet.commit()

netGroup1 = ixNet.getList(t1dev1, 'networkGroup')[0]
netGroup2 = ixNet.getList(t2dev1, 'networkGroup')[0]

ixNet.add(netGroup1, 'networkTopology')
ixNet.add(netGroup2, 'networkTopology')
ixNet.commit()

netTopo1 = ixNet.getList(netGroup1, 'networkTopology')[0]
netTopo2 = ixNet.getList(netGroup2, 'networkTopology')[0]

ixNet.add(netTopo1, 'netTopologyFatTree')
ixNet.add(netTopo2, 'netTopologyFatTree')
ixNet.commit()

print("Adding device group behind network group")
ixNet.add(netGroup1, 'deviceGroup')
ixNet.add(netGroup2, 'deviceGroup')
ixNet.commit()

t1dev2 = ixNet.getList(netGroup1, 'deviceGroup')[0]
t2dev2 = ixNet.getList(netGroup2, 'deviceGroup')[0]

print("Adding ethernet")
ixNet.add(t1dev2, 'ethernet')
ixNet.add(t2dev2, 'ethernet')
ixNet.commit()

mac3 = ixNet.getList(t1dev2, 'ethernet')[0]
mac4 = ixNet.getList(t2dev2, 'ethernet')[0]

print("Adding Fabric Path Simulated Egde")
ixNet.add(mac3, 'isisDceSimRouter')
ixNet.add(mac4, 'isisDceSimRouter')
ixNet.commit()

print("Adding MAC Pools behind Fabric Path Simulated Edge Device")
ixNet.add(t1dev2, 'networkGroup')
ixNet.add(t2dev2, 'networkGroup')
ixNet.commit()

netGroup3 = ixNet.getList(t1dev2, 'networkGroup')[0]
netGroup4 = ixNet.getList(t2dev2, 'networkGroup')[0]
ixNet.add(netGroup3, 'macPools')
ixNet.add(netGroup4, 'macPools')
ixNet.commit()

macPool1 = ixNet.getList(netGroup3, 'macPools')[0]
macPool2 = ixNet.getList(netGroup4, 'macPools')[0]

mvMac1 = ixNet.getAttribute(macPool1, '-mac')
mvMac2 = ixNet.getAttribute(macPool2, '-mac')

ixNet.setAttribute(mvMac1, '-pattern', 'counter')
ixNet.setAttribute(mvMac2, '-pattern', 'counter')
ixNet.commit()

mvCounter1 = ixNet.getList(mvMac1, 'counter')[0]
mvCounter2 = ixNet.getList(mvMac2, 'counter')[0]

ixNet.setMultiAttribute(mvCounter1, '-step', '00:00:00:00:00:01', '-start', '22:22:22:22:22:22', '-direction', 'increment')
ixNet.setMultiAttribute(mvCounter2, '-step', '00:00:00:00:00:01', '-start', '44:44:44:44:44:44', '-direction', 'increment')
ixNet.commit()

print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)

################################################################################
# 2. Retrieve protocol statistics.
################################################################################
print("Fetching all Protocol Summary Stats\n")
viewPage = '::ixNet::OBJ-/statistics/view:"Fabric-Path RTR Per Port"/page'
statcap = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-34s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")

###############################################################################
# 3. Retrieve protocol learned info
###############################################################################
print("Fetching Fabric Path Learned Info")
ixNet.execute('getLearnedInfo', fabricPathIf1, 1)
time.sleep(5)
linfo1 = ixNet.getList(fabricPathIf1, 'learnedInfo')[0]

linfoTables  = ixNet.getList(linfo1, 'table')
table1 = linfoTables[0]
table2 = linfoTables[1]
table3 = linfoTables[2]
table4 = linfoTables[3]

values = ixNet.getAttribute(table1, '-values')
column = ixNet.getAttribute(table1, '-columns')
print("***************************************************")
for index in range(len(values)):
    rowValue = values[index]
    for col in range(len(column)):
        print("%-30s:%s" % (column[col], rowValue[col]))
    #end for
#end for

values = ixNet.getAttribute(table2, '-values')
column = ixNet.getAttribute(table2, '-columns')
print("***************************************************")
for index in range(len(values)):
    rowValue = values[index]
    for col in range(len(column)):
        print("%-30s:%s" % (column[col], rowValue[col]))
    #end for
#end for

values = ixNet.getAttribute(table3, '-values')
column = ixNet.getAttribute(table3, '-columns')
print("***************************************************")
for index in range(len(values)):
    rowValue = values[index]
    for col in range(len(column)):
        print("%-30s:%s" % (column[col], rowValue[col]))
    #end for
#end for

values = ixNet.getAttribute(table4, '-values')
column = ixNet.getAttribute(table4, '-columns')
print("***************************************************")
for index in range(len(values)):
    rowValue = values[index]
    for col in range(len(column)):
        print("%-30s:%s" % (column[col], rowValue[col]))
    #end for
#end for
print("***************************************************")

###############################################################################
# 4. Apply on the fly
###############################################################################
dceMCastMacGroupList = ixNet.getList(fabricPathRouter2, 'dceMCastMacGroupList')[0]
mvMcastAddrCount = ixNet.getAttribute(dceMCastMacGroupList, '-mcastAddrCnt')

ixNet.setAttribute(mvMcastAddrCount, '-pattern', 'singleValue')
ixNet.setAttribute(mvMcastAddrCount + '/singleValue', '-value', 10)
ixNet.commit()

globals = root + '/globals'
topology = globals + '/topology'
print("Applying changes on the fly")

try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")
# end try/expect
time.sleep(5)

################################################################################
# 5. Configure L2-L3 traffic 
################################################################################
print("Congfiguring L2-L3 Traffic Item")
trafficItem1 = ixNet.add(root + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem1, 
    '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ethernetVlan',
	'-biDirectional', 1)
ixNet.commit()

trafficItem1 = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')
source = netGroup3
destination = netGroup4

ixNet.setMultiAttribute(endpointSet1,
    '-name', 'EndpointSet-1',
    '-multicastDestinations', [],
    '-scalableSources',       [],
    '-multicastReceivers',    [],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               source,
    '-destinations',          destination)
ixNet.commit()

ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         [])
ixNet.commit()

###############################################################################
# 6. Apply and start L2/L3 traffic
###############################################################################
print("applying L2/L3 traffic")
ixNet.execute('apply', root + '/traffic')
time.sleep(5)

print("starting L2/L3 traffic")
ixNet.execute('start', root + '/traffic')

###############################################################################
# 7. Retrieve L2/L3 traffic item statistics
###############################################################################
print ('Verifying all the L2-L3 traffic stats')
viewPage = '::ixNet::OBJ-/statistics/view:"Flow Statistics"/page'
statcap =  ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-34s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")

################################################################################
# 8. Stop L2/L3 traffic
#################################################################################
print ('Stopping L2/L3 traffic')
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)

################################################################################
# 9. Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
print ('!!! Test Script Ends !!!')
