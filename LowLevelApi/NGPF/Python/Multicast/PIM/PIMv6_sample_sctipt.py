# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    11/01/2012 - Rupam Paul   - created sample                                #
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
#    Description:                                                              #
#    This script intends to demonstrate how to use NGPF PIM API.               #
#                                                                              #
#    1. It will create 2 PIM topologies, each having an ipv6 network           #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. A loopback device group(DG) behind network   # 
#       group is needed to support applib traffic.                             #
#    2. Start the pim protocol.                                                #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Modify the Rangetype from "SG" to "*G" in the First and Second PIM     #
#       router.And apply changes On The Fly (OTF)                              #
#    6. Retrieve protocol learned info again and notice the difference with    #
#       previouly retrieved learned info.                                      #
#    7. Configure L2-L3 traffic.                                               #
#    8. Configure application traffic.                                         #
#    9. Start the L2-L3 traffic.                                               #
#   10. Start the application traffic.                                         #
#   11. Retrieve Appilcation traffic stats.                                    #
#   12. Retrieve L2-L3 traffic stats.                                          #
#   13. Stop L2-L3 traffic.                                                    #
#   14. Stop Application traffic.                                              #
#   15. Stop all protocols.                                                    #                                                                                          
# Ixia Softwares:                                                              #
#    IxOS      6.80 EB (6.80.1101.110)                                         #
#    IxNetwork 7.40 EB (7.40.0.355)                                            #
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
# Either feed the ixNetwork library path in the sys.path as below, or put the
# IxNetwork.pm file somewhere else where we python can autoload it.
# "IxNetwork.pm" is available in <IxNetwork_installer_path>\API\Python
################################################################################
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\7.40.0.347-EB\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.205.28.50'
ixTclPort   = '8585'
ports       = [('10.205.28.170', '2', '7',), ('10.205.28.170', '2', '8',)]

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

print("Add ipv6")
ixNet.add(mac1, 'ipv6')
ixNet.add(mac2, 'ipv6')
ixNet.commit()

ip1 = ixNet.getList(mac1, 'ipv6')[0]
ip2 = ixNet.getList(mac2, 'ipv6')[0]

mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvAdd2 = ixNet.getAttribute(ip2, '-address')
mvGw1  = ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = ixNet.getAttribute(ip2, '-gatewayIp')

print("configuring ipv6 addresses")
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '2000::1')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '2000::2')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '2000::2')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '2000::1')

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

print ('ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6\')')
print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6'))

print("Adding pimV6Interface over IP6 stacks")
ixNet.add(ip1, 'pimV6Interface')
ixNet.add(ip2, 'pimV6Interface')
ixNet.commit()

pim1 = ixNet.getList(ip1, 'pimV6Interface')[0]
pim2 = ixNet.getList(ip2, 'pimV6Interface')[0]

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'PIM Topology 1')
ixNet.setAttribute(topo2, '-name', 'PIM Topology 2')

ixNet.setAttribute(t1dev1, '-name', 'PIM Topology 1 Router')
ixNet.setAttribute(t2dev1, '-name', 'PIM Topology 2 Router')
ixNet.commit()

print ("Modifying the Hello Interval in the first PIM router")
helloIntervalMultiValue1 = ixNet.getAttribute(pim1, '-helloInterval')
ixNet.setMultiAttribute(helloIntervalMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(helloIntervalMultiValue1 + '/singleValue', '-value', '40')

print ("Modifying the Hello Hold time in the first PIM router")
helloHoldTimeMultiValue1 = ixNet.getAttribute(pim1, '-helloHoldTime')
ixNet.setMultiAttribute(helloHoldTimeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(helloHoldTimeMultiValue1 + '/singleValue', '-value', '110')

print ("Enabling Bootstrap in the first PIM router")
enableBootstrapMultiValue1 = ixNet.getAttribute(pim1, '-enableBootstrap')
ixNet.setMultiAttribute(enableBootstrapMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(enableBootstrapMultiValue1 + '/singleValue', '-value', 'True')

print ("Modifying the Hello Interval in the Second PIM router")
helloIntervalMultiValue2 = ixNet.getAttribute(pim2, '-helloInterval')
ixNet.setMultiAttribute(helloIntervalMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(helloIntervalMultiValue2 + '/singleValue', '-value', '40')

print ("Modifying the Hello Hold time in the second PIM router")
helloHoldTimeMultiValue2 = ixNet.getAttribute(pim2, '-helloHoldTime')
ixNet.setMultiAttribute(helloHoldTimeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(helloHoldTimeMultiValue2 + '/singleValue', '-value', '110')

print ("Enabling Bootstrap in the Second PIM router")
enableBootstrapMultiValue2 = ixNet.getAttribute(pim2, '-enableBootstrap')
ixNet.setMultiAttribute(enableBootstrapMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(enableBootstrapMultiValue2 + '/singleValue', '-value', 'True')

pimV6JoinPruneList1 = ixNet.getList(pim1, 'pimV6JoinPruneList')[0]
pimV6JoinPruneList2 = ixNet.getList(pim2, 'pimV6JoinPruneList')[0]

print ("Modifying the RP Address in the first PIM router")
rpMultiValue1 = ixNet.getAttribute(pimV6JoinPruneList1, '-rpV6Address')
ixNet.setMultiAttribute(rpMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(rpMultiValue1 + '/singleValue', '-value', '"3000::1"')

print ("Modifying the RP Address in the Second PIM router")
rpMultiValue2 = ixNet.getAttribute(pimV6JoinPruneList2, '-rpV6Address')
ixNet.setMultiAttribute(rpMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(rpMultiValue2 + '/singleValue', '-value', '"3000::1"')

print ("Modifying the Rangetype from *G to SG in the first PIM router")
rangeTypeMultiValue1 = ixNet.getAttribute(pimV6JoinPruneList1, '-rangeType')
ixNet.setMultiAttribute(rangeTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(rangeTypeMultiValue1 + '/singleValue', '-value', 'sourcetogroup')

print ("Modifying the Rangetype from *G to SG in the Second PIM router")
rangeTypeMultiValue2 = ixNet.getAttribute(pimV6JoinPruneList2, '-rangeType')
ixNet.setMultiAttribute(rangeTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(rangeTypeMultiValue2 + '/singleValue', '-value', 'sourcetogroup')

print ("Modifying the Group Address in the first PIM router")
groupaddressMultiValue1 = ixNet.getAttribute(pimV6JoinPruneList1, '-groupV6Address')
ixNet.setMultiAttribute(groupaddressMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(groupaddressMultiValue1 + '/singleValue', '-value', '"ff15::1"')

print ("Modifying the Group Address in the Second PIM router")
groupaddressMultiValue2 = ixNet.getAttribute(pimV6JoinPruneList2, '-groupV6Address')
ixNet.setMultiAttribute(groupaddressMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(groupaddressMultiValue2 + '/singleValue', '-value', '"ff16::1"')

pimV6SourcesList1 = ixNet.getList(pim1, 'pimV6SourcesList')[0]
pimV6SourcesList2 = ixNet.getList(pim2, 'pimV6SourcesList')[0]

print ("Modifying the TX Iteration Gap in the first PIM router")
txgapMultiValue1 = ixNet.getAttribute(pimV6SourcesList1, '-txIterationGap')
ixNet.setMultiAttribute(txgapMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(txgapMultiValue1 + '/singleValue', '-value', '30000')

print ("Modifying the TX Iteration Gap in the Second PIM router")
txgapMultiValue2 = ixNet.getAttribute(pimV6SourcesList2, '-txIterationGap')
ixNet.setMultiAttribute(txgapMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(txgapMultiValue2 + '/singleValue', '-value', '30000')

pimV6CandidateRPsList1 = ixNet.getList(pim1, 'pimV6CandidateRPsList')[0]
pimV6CandidateRPsList2 = ixNet.getList(pim2, 'pimV6CandidateRPsList')[0]

print ("Modifying Priority in the first PIM router")
priorityMultiValue1 = ixNet.getAttribute(pimV6CandidateRPsList1, '-priority')
ixNet.setMultiAttribute(priorityMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(priorityMultiValue1 + '/singleValue', '-value', '180')

print ("Modifying Priority in the Second PIM router")
priorityMultiValue2 = ixNet.getAttribute(pimV6CandidateRPsList2, '-priority')
ixNet.setMultiAttribute(priorityMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(priorityMultiValue2 + '/singleValue', '-value', '190')

print ("Disabling the Enable pack checkbox for the first pim router")
enableMultiValue1 = ixNet.getAttribute(pimV6JoinPruneList1, '-enablePack')
ixNet.setMultiAttribute(enableMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(enableMultiValue1 + '/singleValue', '-value', 'False')

print ("Disabling the Enable pack checkbox for the second pim router")
enableMultiValue2 = ixNet.getAttribute(pimV6JoinPruneList2, '-enablePack')
ixNet.setMultiAttribute(enableMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(enableMultiValue2 + '/singleValue', '-value', 'False')

print ("Disabling the Discard Learned Info CheckBox in the first PIM router")

discardlrpinfoMultiValue1 = ixNet.getAttribute(pim1, '-discardLearnedRpInfo')
ixNet.setMultiAttribute(discardlrpinfoMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(discardlrpinfoMultiValue1 + '/singleValue', '-value', 'False')

print ("Disabling the Discard Learned Info CheckBox in the Second PIM router")

discardlrpinfoMultiValue2 = ixNet.getAttribute(pim2, '-discardLearnedRpInfo')
ixNet.setMultiAttribute(discardlrpinfoMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(discardlrpinfoMultiValue2 + '/singleValue', '-value', 'False')

print ('ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6/pimV6Interface\')')
print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6/pimV6Interface'))

print ("Adding Ipv6 prefixpool behind PIM DG")
ixNet.execute('createDefaultStack', t1devices, 'networkTopology')
ixNet.execute('createDefaultStack', t2devices, 'networkTopology')

networkGroup1 = ixNet.add(t1dev1, 'networkGroup')
networkGroup2 = ixNet.add(t2dev1, 'networkGroup')
ixNet.commit()

ipv6prefixpool1 = ixNet.add(networkGroup1, 'ipv6PrefixPools')
ipv6prefixpool2 = ixNet.add(networkGroup2, 'ipv6PrefixPools')
ixNet.commit()

# Add ipv6 loopback1 for applib traffic
print("Adding ipv6 loopback1 for applib traffic")
chainedDg1 = ixNet.add(networkGroup1, 'deviceGroup')
ixNet.setMultiAttribute(chainedDg1, '-multiplier', '7', '-name', 'Device Group 4')
ixNet.commit()
chainedDg1 = ixNet.remapIds(chainedDg1)[0]

loopback1 = ixNet.add(chainedDg1, 'ipv6Loopback')
ixNet.setMultiAttribute(loopback1, '-stackedLayers', [], '-name', 'IPv6 Loopback 2')
ixNet.commit()

connector1 = ixNet.add(loopback1, 'connector')
ixNet.setMultiAttribute(connector1, '-connectedTo', networkGroup1 + '/ipv6PrefixPools:1')
ixNet.commit()
connector1 = ixNet.remapIds(connector1)[0]

addressSet1 = ixNet.getAttribute(loopback1, '-address')
ixNet.setMultiAttribute(addressSet1, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()

addressSet1 = ixNet.add(addressSet1, 'counter')
ixNet.setMultiAttribute(addressSet1, '-step', '::1', '-start', '2010::1', '-direction', 'increment')
ixNet.commit()
addressSet1 = ixNet.remapIds(addressSet1)[0]

# Add ipv6 loopback2 for applib traffic
print("Adding ipv6 loopback2 for applib traffic")
chainedDg2 = ixNet.add(networkGroup2, 'deviceGroup')
ixNet.setMultiAttribute(chainedDg2, '-multiplier', '7', '-name', 'Device Group 3')
ixNet.commit()
chainedDg2 = ixNet.remapIds(chainedDg2)[0]

loopback2 = ixNet.add(chainedDg2, 'ipv6Loopback')
ixNet.setMultiAttribute(loopback2, '-stackedLayers', [], '-name', 'IPv6 Loopback 1')
ixNet.commit()

connector2 = ixNet.add(loopback2, 'connector')
ixNet.setMultiAttribute(connector2, '-connectedTo', networkGroup2 + '/ipv6PrefixPools:1')
ixNet.commit()
connector1 = ixNet.remapIds(connector2)[0]

addressSet2 = ixNet.getAttribute(loopback2, '-address')
ixNet.setMultiAttribute(addressSet2, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()

addressSet2 = ixNet.add(addressSet2, 'counter')
ixNet.setMultiAttribute(addressSet2, '-step', '::1', '-start', '2060::1', '-direction', 'increment')
ixNet.commit()
addressSet2 = ixNet.remapIds(addressSet2)[0]

################################################################################
# 2. Start PIM protocol and wait for 60 seconds
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)

################################################################################
# 3. Retrieve protocol statistics.
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
print("***************************************************")

###############################################################################
# 4. Retrieve protocol learned info
###############################################################################
print("Fetching PIM Basic Learned Info")
ixNet.execute('getLearnedInfo', pim2, '1')
time.sleep(5)
linfo  = ixNet.getList(pim2, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# 5. Modifying the Rangetype from "SG" to "*G" in the First and Second PIM router.
#    And apply changes On The Fly (OTF).
################################################################################

print ("Modifying the Rangetype from SG to *G in the first PIM router")
rangeTypeMultiValue1 = ixNet.getAttribute(pimV6JoinPruneList1, '-rangeType')
ixNet.setMultiAttribute(rangeTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(rangeTypeMultiValue1 + '/singleValue', '-value', 'startogroup')

print ("Modifying the Rangetype from SG to *G in the Second PIM router")
rangeTypeMultiValue2 = ixNet.getAttribute(pimV6JoinPruneList2, '-rangeType')
ixNet.setMultiAttribute(rangeTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(rangeTypeMultiValue2 + '/singleValue', '-value', 'startogroup')

ixNet.commit()

time.sleep(5)

###############################################################################
# 6. Retrieve protocol learned info again and compare with
#    previouly retrieved learned info.
###############################################################################
print("Fetching PIM Learned Info after modifying RangeType")
ixNet.execute('getLearnedInfo', pim2, '1')
time.sleep(5)
linfo  = ixNet.getList(pim2, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# 7. Configure L2-L3 traffic
################################################################################
print("Congfiguring L2-L3 Traffic Item")
trafficItem1 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv6')
ixNet.commit()

trafficItem1 = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')
source       = [networkGroup1 + '/ipv6PrefixPools:1']
destination  = [networkGroup2 + '/ipv6PrefixPools:1']

ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
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

################################################################################
# 8. Configure Application traffic
################################################################################
print("Configuring Applib traffic")
trafficItem2 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')

ixNet.setMultiAttribute(trafficItem2,
    '-name',                     'Traffic Item 2',             
    '-trafficItemType',          'applicationLibrary',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType',              'ipv6ApplicationTraffic')
ixNet.commit()
trafficItem2 = ixNet.remapIds(trafficItem2)[0]

endpointSet2 = ixNet.add(trafficItem2, 'endpointSet')
source_app   = [ixNet.getList(t1dev1, 'networkGroup')[0]]
destin_app   = [ixNet.getList(t2dev1, 'networkGroup')[0]]

ixNet.setMultiAttribute(endpointSet2,
    '-name',                  "EndpointSet-2",
    '-multicastDestinations', [],
    '-scalableSources',       [],
    '-multicastReceivers',    [],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               source_app,
    '-destinations',          destin_app)    
ixNet.commit()

endpointSet2 = ixNet.remapIds(endpointSet2)[0]

appLibProfile = ixNet.add(trafficItem2, 'appLibProfile')
flows_configured  = ['Bandwidth_BitTorrent_File_Download',
                            'Bandwidth_eDonkey',
                            'Bandwidth_HTTP',
                            'Bandwidth_IMAPv4',
                            'Bandwidth_POP3',
                            'Bandwidth_Radius',
                            'Bandwidth_Raw',
                            'Bandwidth_Telnet',
                            'Bandwidth_uTorrent_DHT_File_Download',
                            'BBC_iPlayer',
                            'BBC_iPlayer_Radio',
                            'BGP_IGP_Open_Advertise_Routes',
                            'BGP_IGP_Withdraw_Routes',
                            'Bing_Search',
                            'BitTorrent_Ares_v217_File_Download',
                            'BitTorrent_BitComet_v126_File_Download',
                            'BitTorrent_Blizzard_File_Download',
                            'BitTorrent_Cisco_EMIX',
                            'BitTorrent_Enterprise',
                            'BitTorrent_File_Download',
                            'BitTorrent_LimeWire_v5516_File_Download',
                            'BitTorrent_RMIX_5M']

ixNet.setMultiAttribute (appLibProfile,
    '-enablePerIPStats', 'false',
    '-objectiveDistribution', 'applyFullObjectiveToEachPort',
    '-configuredFlows', flows_configured)
ixNet.commit()
appLibProfile = ixNet.remapIds(appLibProfile)[0]

print ('ixNet.help(ixNet.getRoot() + \'/traffic\')')
print (ixNet.help(ixNet.getRoot() + '/traffic'))

###############################################################################
# 9. Apply and start L2/L3 traffic
###############################################################################
print ('applying L2/L3 traffic')
ixNet.execute('apply', ixNet.getRoot() + '/traffic')
time.sleep(5)

print ('starting L2/L3 traffic')
ixNet.execute('start', ixNet.getRoot() + '/traffic')

###############################################################################
# 10. Apply and start applib traffic
###############################################################################
print ('applying applib traffic')
ixNet.execute('applyStatefulTraffic', ixNet.getRoot() + '/traffic')
time.sleep(5)

print ('starting applib traffic')
ixNet.execute('startStatefulTraffic', ixNet.getRoot() + '/traffic')

print ('Let traffic run for 1 minute')
time.sleep(60)

###############################################################################
# 11. Retrieve Applib traffic item statistics
###############################################################################
print ('Verifying all the applib traffic stats')
viewPage = '::ixNet::OBJ-/statistics/view:"Application Traffic Item Statistics"/page'
statcap = ixNet.getAttribute(viewPage, '-columnCaptions')
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
print("***************************************************")

###############################################################################
# 12. Retrieve L2/L3 traffic item statistics
###############################################################################
print ('Verifying all the L2-L3 traffic stats')
viewPage = '::ixNet::OBJ-/statistics/view:"Flow Statistics"/page'
statcap =  ixNet.getAttribute(viewPage, '-columnCaptions')
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
print("***************************************************")

################################################################################
# 13. Stop applib traffic
################################################################################
print ('Stopping applib traffic')
ixNet.execute('stopStatefulTraffic', ixNet.getRoot() + '/traffic')
time.sleep(5)

################################################################################
# 14. Stop L2/L3 traffic
################################################################################
print ('Stopping L2/L3 traffic')
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)

################################################################################
# 15. Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
