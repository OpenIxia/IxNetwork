# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    03/12/2015 - Chandan Mishra - created sample                              #
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
#    This script intends to demonstrate how to use NGPF OSPFv2 API.            #
#                                                                              #
#    1. It will create 2 OSPFv2 topologies, each having an ipv4 network        #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. A loopback device group(DG) behind network   # 
#       group is needed to support applib traffic.                             #
#    2. Start the ospfv2 protocol.                                             #
#    3. Enabling Segment Routing in ospfv2                                     #
#    4. Retrieve protocol statistics.                                          #
#    5. Retrieve protocol learned info.                                        #
#    6. Enable the Ospfv2 simulated topologies External Route type1 for DG1,   #
#       which was disabled by default and apply change on the fly.             #
#    7. Enable Segment Routing in Simulated Router                             #
#    8.	Setting SRGB range and SID Count for Emulated Router                   #
#	 9.	Enabling Adj-SID in both emulated router                               #
#	10.	Setting Adj-SID value in both emulated router                          #
#	11.	Adding Network Group behind both OSPFv2 Device Groups                  #
#	12.	Enabling Segment Routing in simulated router                           #
#	13.	Starting protocols                                                     #
#	14.	Fetching all Protocol Summary Stats                                    #
#	15.	Setting on the fly change sidIndexLabel value for ipv4PrefixPools      #
#		and Simulated Router                                                   #
#	16.	Fetching OSPFv2 Basic Learned Info									   #
#	17.	Enabling External Type-1 Simulated Routes on Network Group behind 	   #
#		Device Group1														   #
#	18.	Fetching OSPFv2 on DG2 learned info after enabling ospf external       #
#		route type1															   #
#	19.	Configuring MPLS L2-L3 Traffic Item									   #
#	20.	Verifying all the L2-L3 traffic stats                                  #
#   21. Stop L2-L3 traffic.                                                    #
#   22. Stop Application traffic.                                              #
#   23. Stop all protocols.                                                    #
#                                                                  			   #                                                                                          
# 	Ixia Softwares:                                                            #
#    IxOS      8.00 EB (8.00.1201.21)                                          #
#    IxNetwork 8.00 EB (8.00.1206.6)                                           #
#                                                                              #
################################################################################
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
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.00.0.27-EB\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# 1.Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.216.104.58'
ixTclPort   = '8091'
ports       = [('10.216.108.129', '1', '3',), ('10.216.108.129', '1', '4',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.00',
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

print("Adding OSPFv2 over IP4 stacks")
ixNet.add(ip1, 'ospfv2')
ixNet.add(ip2, 'ospfv2')
ixNet.commit()

ospf1 = ixNet.getList(ip1, 'ospfv2')[0]
ospf2 = ixNet.getList(ip2, 'ospfv2')[0]

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'OSPF Topology 1')
ixNet.setAttribute(topo2, '-name', 'OSPF Topology 2')

ixNet.setAttribute(t1dev1, '-name', 'OSPF Topology 1 Router')
ixNet.setAttribute(t2dev1, '-name', 'OSPF Topology 2 Router')
ixNet.commit()

print ("Making the NetworkType to Point to Point in the first OSPF router")
networkTypeMultiValue1 = ixNet.getAttribute(ospf1, '-networkType')
ixNet.setMultiAttribute(networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(networkTypeMultiValue1 + '/singleValue', '-value', 'pointtopoint')

print("Making the NetworkType to Point to Point in the Second OSPF router")
networkTypeMultiValue2 = ixNet.getAttribute(ospf2, '-networkType')
ixNet.setMultiAttribute(networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(networkTypeMultiValue2 + '/singleValue', '-value', 'pointtopoint')

print("Disabling the Discard Learned Info CheckBox")
ospfv2RouterDiscardLearnedLSA1 = ixNet.getAttribute(ixNet.getList(t1dev1, 'ospfv2Router')[0], '-discardLearnedLsa')
ospfv2RouterDiscardLearnedLSA2 = ixNet.getAttribute(ixNet.getList(t2dev1, 'ospfv2Router')[0], '-discardLearnedLsa')

ixNet.setMultiAttribute(ospfv2RouterDiscardLearnedLSA1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(ospfv2RouterDiscardLearnedLSA1 + '/singleValue', '-value', 'False')

ixNet.setMultiAttribute(ospfv2RouterDiscardLearnedLSA2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(ospfv2RouterDiscardLearnedLSA2 + '/singleValue', '-value', 'False')

print ('ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2\')')
print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2'))
################################################################################
# 2.Enabling Segment Routing in Emulated Router
################################################################################
print ("Enabling Segment Routing for OSPFv2")
ospfv2Router1 = ixNet.getList(t1dev1, 'ospfv2Router')[0]
ospfv2Router2 = ixNet.getList(t2dev1, 'ospfv2Router')[0]
ixNet.setAttribute(ospfv2Router1, '-enableSegmentRouting', 'true')
ixNet.setAttribute(ospfv2Router2, '-enableSegmentRouting', 'true')
ixNet.commit()

################################################################################
# 3.Setting SRGB range and SID Count for Emulated Router
################################################################################
print ("Setting SRGB range and SID Count for Emulated Router")

print ("Setting SRGB range pool for second emulated router")
ospfSRGBRangeSubObjectsList2 = ixNet.getList(ospfv2Router2, 'ospfSRGBRangeSubObjectsList')[0]
startSIDLabel2 = ixNet.getAttribute(ospfSRGBRangeSubObjectsList2, '-startSIDLabel')
svsrgb2 = ixNet.getList(startSIDLabel2, 'singleValue')[0]
ixNet.setAttribute(svsrgb2, '-value', '5000')
ixNet.commit()

print ("Setting SRGB range pool for first emulated router")
ospfSRGBRangeSubObjectsList1 = ixNet.getList(ospfv2Router1, 'ospfSRGBRangeSubObjectsList')[0]
startSIDLabel1 = ixNet.getAttribute(ospfSRGBRangeSubObjectsList1, '-startSIDLabel')
svsrgb1 = ixNet.getList(startSIDLabel1, 'singleValue')[0]
ixNet.setAttribute(svsrgb1, '-value', '4000')
ixNet.commit()

print ("Setting SID count for second emulated router")
sidCount2 = ixNet.getAttribute(ospfSRGBRangeSubObjectsList2, '-sidCount')
sidcountsv2 = ixNet.getList(sidCount2, 'singleValue')[0]
ixNet.setAttribute(sidcountsv2, '-value', '100')
ixNet.commit()

print ("Setting SID count for first emulated router")
sidCount1 = ixNet.getAttribute(ospfSRGBRangeSubObjectsList1, '-sidCount')
sidcountsv1 = ixNet.getList(sidCount1, 'singleValue')[0]
ixNet.setAttribute(sidcountsv1, '-value', '100')
ixNet.commit()

print ("Enabling Adj-SID in first emulated router")
enableAdjSID1 = ixNet.getAttribute(ospf1, '-enableAdjSID')
svAdjSID1 = ixNet.add(enableAdjSID1, 'singleValue')
ixNet.setAttribute(svAdjSID1, '-value', 'true')
ixNet.commit()

print ("Enabling Adj-SID in second emulated router")
enableAdjSID2 = ixNet.getAttribute(ospf2, '-enableAdjSID')
svAdjSID2 = ixNet.add(enableAdjSID2, 'singleValue')
ixNet.setAttribute(svAdjSID2, '-value', 'true')
ixNet.commit()

print ("Setting Adj-SID value in first emulated router")
adjSID1 = ixNet.getAttribute(ospf1, '-adjSID')
counteradjSID1 = ixNet.add(adjSID1, 'counter')
ixNet.setMultiAttribute(counteradjSID1 ,
'-step', '1',
'-start', '9001' ,
'-direction', 'increment')
ixNet.commit()

print ("Setting Adj-SID value in second emulated router")
adjSID2 = ixNet.getAttribute(ospf2, '-adjSID')
counteradjSID2 = ixNet.add(adjSID2, 'counter')
ixNet.setMultiAttribute(counteradjSID2 ,
'-step', '1',
'-start', '9002' ,
'-direction', 'increment')
ixNet.commit()

print ("Adding NetworkGroup behind OSPFv2 Device Group1")
ixNet.execute('createDefaultStack', t1devices, 'networkTopology')
time.sleep(20)
networkGroup1 = ixNet.getList(t1dev1, 'networkGroup')[0]
ixNet.commit()
networkGroup2 = ixNet.add(t2dev1, 'networkGroup')
print ("Adding Prefix Pool behind OSPFv2 Device Group2")
ipv4PrefixPools = ixNet.add(networkGroup2, 'ipv4PrefixPools')
ixNet.setAttribute(networkGroup2, '-multiplier', '7')
ixNet.commit()

ixNet.setAttribute(networkGroup1, '-name', 'OSPF_1_Network_Group1')
ixNet.setAttribute(networkGroup2, '-name', 'OSPF_2_ipv4_Prefix_Pools')
ixNet.commit()

################################################################################
# 4.Enabling Segment Routing in simulated router
################################################################################
print ("Enabling Segment Routing in Simulated Routers on Network Group behind Device Group1")
networkTopo1 = ixNet.getList(networkGroup1, 'networkTopology')[0]
simRouter1 = ixNet.getList(networkTopo1, 'simRouter')[0]
ospfPseudoRouter1 = ixNet.getList(simRouter1, 'ospfPseudoRouter')[0]
ixNet.setAttribute(ospfPseudoRouter1, '-enableSegmentRouting', 'true')
ixNet.commit()

################################################################################
# 5. Start OSPFv2 protocol and wait for 60 seconds
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)

################################################################################
# 6. Retrieve protocol statistics.
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

################################################################################
# 7. Setting on the fly change sidIndexLabel value for ipv4PrefixPools
################################################################################
print ("Setting on the fly change sidIndexLabel value for ipv4PrefixPools from Index 10 ")
ospfRouteProperty1 = ixNet.getList(ipv4PrefixPools, 'ospfRouteProperty')[0]
sidIndexLabel1 = ixNet.getAttribute(ospfRouteProperty1, '-sidIndexLabel')
sidIndexLabelcounter1 = ixNet.add(sidIndexLabel1, 'counter')
ixNet.setMultiAttribute(sidIndexLabelcounter1 ,
'-step', '2' ,
 '-start', '10' ,
 '-direction','increment')
ixNet.commit()

globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")
# end try/expect
time.sleep(5)

################################################################################
# 8. Setting on the fly change sidIndexLabel value for Simulated Router
################################################################################
print ("Setting on the fly change sidIndexLabel value for Simulated Router from Index 11")
sidIndexLabel2 =ixNet.getAttribute(ospfPseudoRouter1, '-sidIndexLabel')
sidIndexLabelcounter1 =ixNet.add(sidIndexLabel2, 'counter')
ixNet.setMultiAttribute (sidIndexLabelcounter1 ,
'-step', '2' ,
 '-start', '11', 
 '-direction', 'increment')
ixNet.commit()

print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")
time.sleep(5)

###############################################################################
# 9. Retrieve protocol learned info
###############################################################################
print("Fetching OSPFv2 Basic Learned Info")
ixNet.execute('getBasicLearnedInfo', ospf1, '1')
time.sleep(5)
linfo  = ixNet.getList(ospf1, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# 10. Enable the Ospfv2 simulated topology's External Route type1, which
#    was disabled by default. And apply changes On The Fly (OTF).
################################################################################
print("Enabling External Type-1 Simulated Routes on Network Group behind Device Group1 to send SR routes for Simulated node routes")
extRoute1         = ixNet.getList(ospfPseudoRouter1, 'ospfPseudoRouterType1ExtRoutes')[0]
activeMultivalue1 = ixNet.getAttribute(extRoute1, '-active')
ixNet.setAttribute(activeMultivalue1 + '/singleValue', '-value', 'true')
ixNet.commit()


globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")
# end try/expect
time.sleep(5)

###############################################################################
# 11. Retrieve protocol learned info again and compare with
#    previously retrieved learned info.
###############################################################################
print("Fetching OSPFv2 on DG2 learned info after enabling ospf external route type1")
ixNet.execute('getBasicLearnedInfo', ospf2, '1')
time.sleep(5)
linfo  = ixNet.getList(ospf2, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# 12. Configure L2-L3 traffic
################################################################################
print("Configuring MPLS L2-L3 Traffic Item")
print ("Configuring traffic item 1 with endpoints src :ospfPseudoRouterType1ExtRoutes & dst :ipv4PrefixPools ")
trafficItem1 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv4')
ixNet.commit()

trafficItem1 = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')
source       = [networkGroup1 + '/networkTopology/simRouter:1/ospfPseudoRouter:1/ospfPseudoRouterType1ExtRoutes:1']
destination   = [ipv4PrefixPools]

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

ixNet.setMultiAttribute(trafficItem1 + '/configElement:1/transmissionDistribution',
    '-distributions', ['ipv4SourceIp0'])
ixNet.commit()

ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['sourceDestValuePair0', 'trackingenabled0', 'mplsMplsLabelValue0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         [])
ixNet.commit()

print "Configuring traffic item 2 with endpoints src :ospfv2RouterDG1 & dst :ospfv2RouterDG2 "

trafficItem2 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem2, '-name', 'Traffic Item 2',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv4')
ixNet.commit()

trafficItem2 = ixNet.remapIds(trafficItem2)[0]
endpointSet2 = ixNet.add(trafficItem2, 'endpointSet')
source       = [t1dev1 + '/ospfv2Router:1']
destination   = [t2dev1 + '/ospfv2Router:1']

ixNet.setMultiAttribute(endpointSet2,
    '-name',                  'EndpointSet-2',
    '-multicastDestinations', [],
    '-scalableSources',       [],
    '-multicastReceivers',    [],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               source,
    '-destinations',          destination)
ixNet.commit()

ixNet.setMultiAttribute(trafficItem2 + '/configElement:1/transmissionDistribution',
    '-distributions', ['ipv4SourceIp0'])
ixNet.commit()

ixNet.setMultiAttribute(trafficItem2 + '/tracking',
    '-trackBy',        ['sourceDestValuePair0', 'trackingenabled0', 'mplsMplsLabelValue0' ,'mplsFlowDescriptor0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         [])
ixNet.commit()

print ("Enabling option Display Dynamic Value when Tracking by Dynamic Flow Descriptor from Traffic Options in Global")
traffic = ixNet.getRoot() + '/traffic'
ixNet.setAttribute(traffic, '-displayMplsCurrentLabelValue', 'true')
ixNet.commit()

###############################################################################
# 13. Apply and start L2/L3 traffic
###############################################################################
print ('Applying L2/L3 traffic')
ixNet.execute('apply', ixNet.getRoot() + '/traffic')
time.sleep(5)

print ('Starting L2/L3 traffic')
ixNet.execute('start', ixNet.getRoot() + '/traffic')

###############################################################################
# 14. Retrieve L2/L3 traffic item statistics
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
# 15. Stop L2/L3 traffic
################################################################################
print ('Stopping L2/L3 traffic')
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)

################################################################################
# 16. Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
