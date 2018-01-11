# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    14/06/2016 - Debarati Chakraborty - created sample                        #
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

#################################################################################
#                                                                               #
# Description:                                                                  #
#    This script intends to demonstrate how to use NGPF RSVPTE P2MP API         #
#    About Topology:                                                            #
#       Within topology both Label Switch Router(LSR) and Label Edge Router(LER)#
#    are created. LSR is emulated in the front Device Group(DG), which consists #
#    of both OSPF as routing protocol as well as RSVPTE-IF for Label            # 
#    Distribution Protocol. The chained DG act as LER, where RSVP-TE P2MP LSPs  #
#    are configured. Unidirectional L2-L3 Traffic from Ingress to Egress is     #
#    created.                                                                   #
#         Script Flow:                                                          #
#        Step 1. Configuration of protocols.                                    #
#    Configuration flow of the script is as follow:                             #
#             i.      Adding of OSPF router                                     #
#             ii.     Adding of Network Topology(NT)                            #
#             iii.    Enabling of TE(Traffic Engineering)                       #
#             iv.     Adding of chain DG                                        #
#             v.      Adding of RSVP-TE LSPs within chain DG                    #
#        Step 2. Start of protocol                                              #
#        Step 3. Protocol Stat display                                          #
#        Step 4. Learned Info display                                           #
#        Step 5. Configuration L2-L3 Traffic                                    #
#        Step 6. Apply and Start of L2-L3 traffic                               #
#        Step 7. Display of L2-L3  traffic Stats                                #
#        Step 8.Stop of L2-L3 traffic                                           #
#        Step 9.Stop of all protocols                                           #
#################################################################################
# Ixia Software Used to develop the script:                                     #
#    IxOS      8.10 EA                                                          #
#    IxNetwork 8.10 EA                                                          #
#                                                                               #
#################################################################################

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
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.10-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.216.104.58'
ixTclPort   = '8239'
ports       = [('10.216.108.82', '7', '15',), ('10.216.108.82', '7', '16',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.10',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')
#################################################################################
# Step 1> protocol configuration section
#################################################################################

# assigning ports
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

root    = ixNet.getRoot()
vportTx = ixNet.getList(root, 'vport')[0]
vportRx = ixNet.getList(root, 'vport')[1]
# Creating topology and device group
print("adding topologies")
ixNet.add(root, 'topology', '-vports', vportTx)
ixNet.add(root, 'topology', '-vports', vportRx)
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]
print ('Renaming the topologies and the device groups')
ixNet.setAttribute(topo1, '-name', 'RSVPTE P2MP Topology 1')
ixNet.setAttribute(topo2, '-name', 'RSVPTE P2MP Topology 2')
print ("Adding 2 device groups")
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices[0]
t2dev1 = t2devices[0]
ixNet.setAttribute(t1dev1, '-name', 'Label Switch Router 1')
ixNet.setAttribute(t2dev1, '-name', 'Label Switch Router 2')
ixNet.commit()

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(t1dev1, '-multiplier', '1')
ixNet.setAttribute(t2dev1, '-multiplier', '1')
ixNet.commit()
#  Adding ethernet stack and configuring MAC
print("Adding ethernet/mac endpoints")
ixNet.add(t1dev1, 'ethernet')
ixNet.add(t2dev1, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = ixNet.getList(t2dev1, 'ethernet')[0]

print("Configuring the mac addresses %s" % (mac1))
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '22:22:22:22:22:22',
    '-step',      '00:00:00:00:00:01')

ixNet.setAttribute(ixNet.getAttribute(mac2, '-mac') + '/singleValue',
    '-value', '44:44:44:44:44:44')
ixNet.commit()
#  Adding IPv4 stack and configuring  IP Address
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
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '50.50.50.2')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '50.50.50.1')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '50.50.50.1')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '50.50.50.2')
ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '26')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '26')
ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

#  Adding OSPF and configuring it
print ('Adding OSPFv2 over IP4 stack')
ixNet.add(ip1, 'ospfv2')
ixNet.add(ip2, 'ospfv2')
ixNet.commit()
ospf1 = ixNet.getList(ip1, 'ospfv2')[0]
ospf2 = ixNet.getList(ip2, 'ospfv2')[0]
print ('Making the NetworkType to Point to Point in the first OSPF router')
networkTypeMultiValue1 = ixNet.getAttribute(ospf1, '-networkType')
ixNet.setMultiAttribute(networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(networkTypeMultiValue1 + '/singleValue', '-value', 'pointtopoint')
ixNet.commit()
print('Making the NetworkType to Point to Point in the Second OSPF router')
networkTypeMultiValue2 = ixNet.getAttribute(ospf2, '-networkType')
ixNet.setMultiAttribute(networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(networkTypeMultiValue2 + '/singleValue', '-value', 'pointtopoint')
ixNet.commit()
print ('Disabling the Discard Learned Info CheckBox')
ospfv2RouterDiscardLearnedLSA1 = ixNet.getAttribute(ixNet.getList(t1dev1, 'ospfv2Router')[0], '-discardLearnedLsa')
ospfv2RouterDiscardLearnedLSA2 = ixNet.getAttribute(ixNet.getList(t2dev1, 'ospfv2Router')[0], '-discardLearnedLsa')

ixNet.setMultiAttribute(ospfv2RouterDiscardLearnedLSA1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(ospfv2RouterDiscardLearnedLSA1 + '/singleValue', '-value', 'False')
ixNet.commit()
ixNet.setMultiAttribute(ospfv2RouterDiscardLearnedLSA2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(ospfv2RouterDiscardLearnedLSA2 + '/singleValue', '-value', 'False')
ixNet.commit()

print ('ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2\')')
print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2'))

print('Adding IPv4 Address Pool in Topology1')
ixNet.add(t1dev1, 'networkGroup')
ixNet.add(t2dev1, 'networkGroup')
ixNet.commit()

networkGroup1 = ixNet.getList(t1dev1, 'networkGroup')[0]
networkGroup2 = ixNet.getList(t2dev1, 'networkGroup')[0]

ixNet.add(networkGroup1, 'ipv4PrefixPools')
ixNet.commit()

print('Adding Linear Tree in Topology2')

netTopologyLinear1 = ixNet.add(networkGroup2, 'networkTopology')
netTopologyLinear = ixNet.add(netTopologyLinear1, 'netTopologyLinear')
netTopologyLinear = ixNet.remapIds(netTopologyLinear)[0]
ixNet.commit()

netTopo1 =ixNet.getList(networkGroup1, 'ipv4PrefixPools')
netTopo2 =ixNet.getList(networkGroup2, 'networkTopology')
netTopo2 = ixNet.remapIds(netTopo2)[0]
ixNet.commit()

ixNet.setMultiAttribute(netTopologyLinear, '-nodes', '5')
ixNet.commit()

# Configuring Traffic Engineering
print ('Enabling Traffic Engineering in Network Topology 2')
simInterface2 = ixNet.getList(netTopo2, 'simInterface')[0]
simInterfaceIPv4Config2 = ixNet.getList(simInterface2, 'simInterfaceIPv4Config')[0]
ospfPseudoInterface2 = ixNet.getList(simInterfaceIPv4Config2, 'ospfPseudoInterface')[0]
ospfPseudoInterface2_teEnable = ixNet.getAttribute(ospfPseudoInterface2, '-enable')
ixNet.setMultiAttribute(ospfPseudoInterface2_teEnable, '-clearOverlays', 'false', '-pattern', 'singleValue')
ixNet.commit()
ixNet.setMultiAttribute(ospfPseudoInterface2_teEnable + '/singleValue', '-value', 'true')
ixNet.commit()

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(networkGroup1, '-multiplier', '2')
ixNet.setAttribute(networkGroup2, '-multiplier', '2')
ixNet.commit()

# Adding Chained Device Group Behind front Device Group for IPv4 loopback
print ('adding Chained DG behind IPv4 Address Pool in Topology 1')
chainedDg1 = ixNet.add(networkGroup1, 'deviceGroup')
ixNet.setMultiAttribute(chainedDg1, '-multiplier', '1', '-name', 'Edge Router 1')
ixNet.commit()

chainedDg1 = ixNet.remapIds(chainedDg1)[0]
loopback1 = ixNet.add(chainedDg1, 'ipv4Loopback')
ixNet.setMultiAttribute(loopback1, '-stackedLayers', [], '-name', 'IPv4 Loopback 1')
ixNet.commit()

print ('adding Chained DG behind Network topology in Topology 2')
chainedDg2 = ixNet.add(networkGroup2, 'deviceGroup')
ixNet.setMultiAttribute(chainedDg2, '-multiplier', '1', '-name', 'Edge Router 2')
ixNet.commit()

chainedDg2 = ixNet.remapIds(chainedDg2)[0]
loopback2 = ixNet.add(chainedDg2, 'ipv4Loopback')
ixNet.setMultiAttribute(loopback2, '-stackedLayers', [], '-name', 'IPv4 Loopback 2')
ixNet.commit()

print('Adding RSVPTE P2MP LSPs over "IPv4 Loopback 1"')
rsvpteLsps1 = ixNet.add(loopback1, 'rsvpteLsps')
ixNet.setMultiAttribute(rsvpteLsps1, '-ingressP2PLsps', '0', '-enableP2PEgress', 'false', '-p2mpIngressLspCount', '1', '-p2mpEgressTunnelCount', '0', '-name', 'RSVP-TE 1')
ixNet.commit()

rsvpteLsps1 = ixNet.remapIds(rsvpteLsps1)[0]

print('Adding RSVPTE P2MP LSPs over "IPv4 Loopback 2"')
rsvpteLsps2 = ixNet.add(loopback2, 'rsvpteLsps')
ixNet.setMultiAttribute(rsvpteLsps2, '-ingressP2PLsps', '0', '-enableP2PEgress', 'false', '-p2mpIngressLspCount', '0', '-p2mpEgressTunnelCount', '5', '-name', 'RSVP-TE 2')
ixNet.commit()

rsvpteLsps2 = ixNet.remapIds(rsvpteLsps2)[0]

print ('Editing P2MP ID in Ingress LSPs')
rsvpP2mpIngressLsps = ixNet.getList(rsvpteLsps1, 'rsvpP2mpIngressLsps')[0]
p2mpIdAsNumber_ingress = ixNet.getAttribute(rsvpP2mpIngressLsps, '-p2mpIdAsNumber')
ixNet.setMultiAttribute(p2mpIdAsNumber_ingress, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()

ixNet.setMultiAttribute(p2mpIdAsNumber_ingress + '/counter', '-step', '1', '-start', '1', '-direction', 'increment')
ixNet.commit()

print ('Editing P2MP ID in Egress LSPs')
rsvpP2mpEgressLsps = ixNet.getList(rsvpteLsps2, 'rsvpP2mpEgressLsps')[0]
p2mpIdAsNumber_egress = ixNet.getAttribute(rsvpP2mpEgressLsps, '-p2mpIdAsNumber')
ixNet.setMultiAttribute(p2mpIdAsNumber_egress, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()

p2mpIdAsNumber_egress_Custom = ixNet.add(p2mpIdAsNumber_egress, 'custom')
ixNet.setMultiAttribute(p2mpIdAsNumber_egress_Custom, '-step', '0', '-start', '1')
p2mpIdAsNumber_egress_Custom = ixNet.remapIds(p2mpIdAsNumber_egress_Custom)[0]

p2mpIdAsNumber_egress_Custom_inc = ixNet.add(p2mpIdAsNumber_egress_Custom, 'increment')
ixNet.setMultiAttribute(p2mpIdAsNumber_egress_Custom_inc, '-count', '2', '-value', '1')
ixNet.commit()
p2mpIdAsNumber_egress_Custom = ixNet.remapIds(p2mpIdAsNumber_egress_Custom)[0]
ixNet.commit()

print ('Editing P2MP Ingress SubLSPs counter')
ixNet.setAttribute(rsvpP2mpIngressLsps, '-ingressP2mpSubLspRanges', '5')
ixNet.commit()

print ('Editing Leaf IP in Ingress SubLSPs')
leafIp = ixNet.getAttribute(rsvpteLsps1+'/rsvpP2mpIngressLsps/rsvpP2mpIngressSubLsps', '-leafIp')
ixNet.setMultiAttribute(leafIp, '-clearOverlays', 'false')
ixNet.commit()

custom_leaf = ixNet.add(leafIp, 'custom')
ixNet.setMultiAttribute(custom_leaf, '-step', '0.0.0.0', '-start', '3.2.2.2')
ixNet.commit()
custom_leaf = ixNet.remapIds(custom_leaf)[0]

increment_leaf = ixNet.add(custom_leaf, 'increment')
ixNet.setMultiAttribute(increment_leaf, '-count', '2', '-value', '0.0.0.1')
ixNet.commit()
increment_leaf = ixNet.remapIds(increment_leaf)[0]

print ('************************************************************')

################################################################################
# Step 2> Start of protocol.
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)
################################################################################
# Step 3> Retrieve protocol statistics.
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
# Step 4> Retrieve protocol learned info
###############################################################################
print("Fetching RSVPTE P2MP Received learned info")
rsvpteIf1 = ixNet.getList(ip1, 'rsvpteIf')[0]
ixNet.execute('getLearnedInfo', rsvpteIf1, '1')
print(' %%%%%%%%%%%%%%%%% Learned Info fetched')
time.sleep(5)
linfo  = ixNet.getList(rsvpteIf1, 'learnedInfo')[3]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************") 
################################################################################
# Step 5> Apply changes on the fly.
################################################################################
print ('Changing Label Value for first RSVPTE router to single value in Topology 1')
labelSpaceStartMultValue1 = ixNet.getAttribute(rsvpteIf1, '-labelSpaceStart')
ixNet.setMultiAttribute(labelSpaceStartMultValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(labelSpaceStartMultValue1 + '/singleValue', '-value', '8000')
ixNet.commit()

globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")
# end try/expectX
time.sleep(5)

###############################################################################
# Step 6> Retrieve protocol learned info again and compare with.
###############################################################################
print("Fetching RSVPTE P2MP Received learned info")
rsvpteIf1 = ixNet.getList(ip1, 'rsvpteIf')[0]
ixNet.execute('getLearnedInfo', rsvpteIf1)
time.sleep(5)
linfo  = ixNet.getList(rsvpteIf1, 'learnedInfo')[3]
rcvd_linfo = ixNet.getList(linfo, 'table')[0]
values = ixNet.getAttribute(rcvd_linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************") 

################################################################################
# Step 7> Configure L2-L3 traffic
################################################################################
print("Configuring L2-L3 Traffic Item")
trafficItem1 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem1, '-name', 'RSVPTE P2MP Traffic 1',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv4')
ixNet.commit()

trafficItem1 = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')
source       = [rsvpteLsps1 + '/rsvpP2mpIngressLsps']
destination  = [rsvpteLsps2 + '/rsvpP2mpEgressLsps']

ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
    '-sources',               source,
    '-multicastDestinations', [['false','none','225.0.0.0','0.0.0.0','1']])
ixNet.commit()

endpointSet1 = ixNet.remapIds(endpointSet1)[0]

ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'trackingenabled0', 'mplsMplsLabelValue0', 'ipv4DestIp0', 'ipv4SourceIp0'])
ixNet.commit()

###############################################################################
# Step 8> Apply and start L2/L3 traffic
###############################################################################
print ('applying L2/L3 traffic')
ixNet.execute('apply', ixNet.getRoot() + '/traffic')
time.sleep(5)

print ('starting L2/L3 traffic')
ixNet.execute('start', ixNet.getRoot() + '/traffic')

print ('let traffic run for 120 second')
time.sleep(120)
###############################################################################
# Step 9> Retrieve L2/L3 traffic item statistics.
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
# Step 10> Stop L2/L3 traffic.
################################################################################
print ('Stopping L2/L3 traffic')
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)
################################################################################
# Step 11> Stop all protocols.
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
print ('!!! Test Script Ends !!!') 
