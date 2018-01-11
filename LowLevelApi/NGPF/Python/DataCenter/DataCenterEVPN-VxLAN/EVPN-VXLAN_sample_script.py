# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    03/12/2015 - Subhradip Pramanik - created sample                          #
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
#    This script intends to demonstrate how to use NGPF EVPN VXLAN API          #
#    About Topology:                                                            #
#        It will create 2 BGP EVPN-VXLAN topologies, each having OSPFv2         #
#    configured in connected Device Group .BGP EVPN VXLAN configured in chained # 
#    device group along with Mac pools connected behind the chained             # 
#    Device Group.                                                              #
#         Script Flow:                                                          #
#        Step 1. Configuration of protocols.                                    #
#    Configuration flow of the script is as follow:                             #
#             i.      Adding OSPF router.                                       #
#             ii.     Adding Network Topology(NT).                              #
#             iii.    Adding chain DG.                                          #
#             iv.     Adding BGP over loopback.                                 #
#             v.      Adding EVPN VXLAN over BGP                                #
#             vi.     Adding MAC Cloud with associated IPv4 Addresses           #
#        Step 2. Start of protocol                                              #
#        Step 3. Protocol Stat display                                          #
#        Step 4. Learned Info display                                           #
#        Step 5. On The Fly(OTF) change of protocol parameter.                  #
#        Step 6. Again Learned Info display to see OTF changes take place       #
#        Step 7. Configuration L2-L3 Traffic                                    #
#        Step 8. Apply and Start of L2-L3 traffic.                              #
#        Step 9. Diplay of L2-L3  traffic Stats.                                #
#        Step 10.Stop of L2-L3 traffic.                                         #
#        Step 11.Stop of all protocols.                                         #
#################################################################################
# Ixia Software Used to develop the script:                                     #
#    IxOS      8.00 EA                                                          #
#    IxNetwork 8.00 EA                                                          #
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
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.00.1026.7-EB\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.216.104.58'
ixTclPort   = '8999'
ports       = [('10.216.108.82', '2', '15',), ('10.216.108.82', '2', '16',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")

#version = ixNet.getVersion
#scan [split $version "."] "%d %d" major minor
#set version "$major.$minor"

ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.00',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')
#################################################################################
# 1. protocol configuration section
#################################################################################

# Assigning ports
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
ixNet.setAttribute(topo1, '-name', 'EVPN VXLAN Topology 1')
ixNet.setAttribute(topo2, '-name', 'EVPN VXLAN Topology 2')
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
    '-start',     '22:01:01:01:01:01',
    '-step',      '00:00:00:00:00:01')

ixNet.setAttribute(ixNet.getAttribute(mac2, '-mac') + '/singleValue',
    '-value', '44:01:01:01:01:01')
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
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '51.51.51.2')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '51.51.51.1')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '51.51.51.1')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '51.51.51.2')
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


print('Adding the NetworkGroup with Routers at back of it')
ixNet.execute('createDefaultStack', t1devices, 'networkTopology')
ixNet.execute('createDefaultStack', t2devices, 'networkTopology')
networkGroup1 = ixNet.getList(t1dev1, 'networkGroup')[0]
networkGroup2 = ixNet.getList(t2dev1, 'networkGroup')[0]
ixNet.setAttribute(networkGroup1, '-name', 'Network Topology 1')
ixNet.setAttribute(networkGroup2, '-name', 'Network Topology 2')
ixNet.commit()

netTopo1 =ixNet.getList(networkGroup1, 'networkTopology')[0]
netTopo2 =ixNet.getList(networkGroup2, 'networkTopology')[0]

# Adding Chained Device Group Behind front Device Group for IPv4 loopback
print ('add ipv4 loopback1 for EVPN VXLAN Leaf Ranges')
chainedDg1 = ixNet.add(networkGroup1, 'deviceGroup')
ixNet.setMultiAttribute(chainedDg1, '-multiplier', '1', '-name', 'Edge Router 1')
ixNet.commit()

chainedDg1 = ixNet.remapIds(chainedDg1)[0]
loopback1 = ixNet.add(chainedDg1, 'ipv4Loopback')
ixNet.setMultiAttribute(loopback1, '-stackedLayers', [], '-name', 'IPv4 Loopback 2')
ixNet.commit()

connector1 = ixNet.add(loopback1, 'connector')
ixNet.setMultiAttribute(connector1, '-connectedTo', networkGroup1 + '/networkTopology/simRouter:1')
ixNet.commit()

connector1 = ixNet.remapIds(connector1)[0]
addressSet1 = ixNet.getAttribute(loopback1, '-address')
ixNet.setMultiAttribute(addressSet1, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()

addressSet1 = ixNet.add(addressSet1, 'counter')
ixNet.setMultiAttribute(addressSet1, '-step', '0.1.0.0', '-start', '2.1.1.1', '-direction', 'increment')
ixNet.commit()

addressSet1 = ixNet.remapIds(addressSet1)[0]
print ('add ipv4 loopback1 for EVPN VXLAN Leaf Ranges')
chainedDg2 = ixNet.add(networkGroup2, 'deviceGroup')
ixNet.setMultiAttribute(chainedDg2, '-multiplier', '1', '-name', 'Edge Router 2')
ixNet.commit()

chainedDg2 = ixNet.remapIds(chainedDg2)[0]
loopback2 = ixNet.add(chainedDg2, 'ipv4Loopback')
ixNet.setMultiAttribute(loopback2, '-stackedLayers', [], '-name', 'IPv4 Loopback 1')
ixNet.commit()

connector2 = ixNet.add(loopback2, 'connector')
ixNet.setMultiAttribute(connector2, '-connectedTo', networkGroup2 + '/networkTopology/simRouter:1')
ixNet.commit()

connector1 = ixNet.remapIds(connector2)[0]
addressSet2 = ixNet.getAttribute(loopback2, '-address')
ixNet.setMultiAttribute(addressSet2, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()

addressSet2 = ixNet.add(addressSet2, 'counter')
ixNet.setMultiAttribute(addressSet2, '-step', '0.0.0.1', '-start', '3.1.1.1', '-direction', 'increment')
ixNet.commit()

addressSet2 = ixNet.remapIds(addressSet2)[0]

print('Adding BGPv4 over IP4 loopback in chained DG"')
bgpIpv4Peer1 = ixNet.add(loopback1, 'bgpIpv4Peer')
ixNet.commit()
bgpIpv4Peer1 = ixNet.remapIds(bgpIpv4Peer1)[0]

print('Adding EVPN VXLAN over "IPv4 Loopback 2"')
bgpIpv4Peer2 = ixNet.add(loopback2, 'bgpIpv4Peer')
ixNet.commit()
bgpIpv4Peer2 = ixNet.remapIds(bgpIpv4Peer2)[0]



print ('Setting DUT IP in BGPv4 Peer')
ixNet.setAttribute(ixNet.getAttribute(bgpIpv4Peer1, '-dutIp') + '/singleValue',
    '-value', '3.1.1.1')
ixNet.commit()

ixNet.setMultiAttribute(ixNet.getAttribute(bgpIpv4Peer2, '-dutIp') + '/counter',
    '-direction', 'increment',
    '-start',     '2.1.1.1',
    '-step',      '0.0.0.1')

ixNet.commit()

print('Enabling Learned Route Filters for EVPN VXLAN in BGP4 Peer')
ixNet.setAttribute(ixNet.getAttribute(bgpIpv4Peer1, '-filterEvpn') + '/singleValue',
        '-value', '1')
ixNet.commit()

ixNet.setAttribute(ixNet.getAttribute(bgpIpv4Peer2, '-filterEvpn') + '/singleValue',
        '-value', '1')
ixNet.commit()



print('Configuring Router\'s MAC Addresses for EVPN VXLAN in BGP4 Peer')

ixNet.setMultiAttribute(ixNet.getAttribute(bgpIpv4Peer1, '-routersMacOrIrbMacAddress') + '/counter',
    '-direction', 'increment',
    '-start',     'aa:aa:aa:aa:aa:aa',
    '-step',      '00:00:00:00:00:01')

ixNet.commit()

ixNet.setAttribute(ixNet.getAttribute(bgpIpv4Peer2, '-routersMacOrIrbMacAddress') + '/singleValue',
    '-value', 'cc:cc:cc:cc:cc:cc')
ixNet.commit()

print ('Changing Router Id of Network Topology to Loopback Address of Chained Device Group under Edge Router 1')
simRouter1 = ixNet.getList(netTopo1, 'simRouter')[0]
simRouterId1 = ixNet.getAttribute(simRouter1, '-routerId')
ixNet.setMultiAttribute(simRouterId1, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()

ixNet.setMultiAttribute(simRouterId1 + '/counter', '-step', '0.0.0.1', '-start', '2.1.1.1', '-direction', 'increment')
ixNet.commit()

simRouterId1 = ixNet.remapIds(simRouterId1)[0]
print ('Changing Router Id of Network Topology to Loopback Address of Chained Device Group under Edge Router 2')
simRouter2 = ixNet.getList(netTopo2, 'simRouter')[0]
simRouterId2 = ixNet.getAttribute(simRouter2, '-routerId')
ixNet.setMultiAttribute(simRouterId2, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()

ixNet.setMultiAttribute(simRouterId2 + '/counter', '-step', '0.0.0.1', '-start', '3.1.1.1', '-direction', 'increment')
ixNet.commit()

simRouterId2 = ixNet.remapIds(simRouterId2)[0]

print ('Adding EVPN VXLAN over BGPv4 in chained DG')

bgpIPv4EvpnVXLAN1 = ixNet.add(bgpIpv4Peer1, 'bgpIPv4EvpnVXLAN')
ixNet.commit()
bgpIPv4EvpnVXLAN1 = ixNet.remapIds(bgpIPv4EvpnVXLAN1)[0]

bgpIPv4EvpnVXLAN2 = ixNet.add(bgpIpv4Peer2, 'bgpIPv4EvpnVXLAN')
ixNet.commit()
bgpIPv4EvpnVXLAN2 = ixNet.remapIds(bgpIPv4EvpnVXLAN2)[0]

print ('Changing Import Route Target AS No.')
bgpImportRouteTargetList1 = ixNet.getList(bgpIPv4EvpnVXLAN1, 'bgpImportRouteTargetList') [0]

bgpImportRouteTargetList2 = ixNet.getList(bgpIPv4EvpnVXLAN2, 'bgpImportRouteTargetList') [0]

targetAsNo1 = ixNet.getAttribute(bgpImportRouteTargetList1, '-targetAsNumber')
targetAsNo2 = ixNet.getAttribute(bgpImportRouteTargetList2, '-targetAsNumber')

ixNet.setMultiAttribute(targetAsNo1 + '/counter', '-step', '0', '-start', '200', '-direction', 'increment')

ixNet.commit()

ixNet.setMultiAttribute(targetAsNo2 + '/counter', '-step', '0', '-start', '200', '-direction', 'increment')

ixNet.commit()


print ('Changing Export Route Target AS No.')
bgpExportRouteTargetList1 = ixNet.getList(bgpIPv4EvpnVXLAN1, 'bgpExportRouteTargetList') [0]

bgpExportRouteTargetList2 = ixNet.getList(bgpIPv4EvpnVXLAN2, 'bgpExportRouteTargetList') [0]

ixNet.setMultiAttribute(ixNet.getAttribute(bgpExportRouteTargetList1, '-targetAsNumber') + '/counter',
    '-direction', 'increment',
    '-start',     '200',
    '-step',      '0')

ixNet.commit()

ixNet.setMultiAttribute(ixNet.getAttribute(bgpExportRouteTargetList2, '-targetAsNumber') + '/counter',
    '-direction', 'increment',
    '-start',     '200',
    '-step',      '0')

ixNet.commit()


print ('Adding Mac Pools behind EVPN VXLAN  DG')

ixNet.execute('createDefaultStack', chainedDg1, 'macPools')
ixNet.execute('createDefaultStack', chainedDg2, 'macPools')

networkGroup3 = ixNet.getList(chainedDg1, 'networkGroup') [0]
networkGroup4 = ixNet.getList(chainedDg2, 'networkGroup') [0]


ixNet.setAttribute(networkGroup3 , '-name', "MAC_Pool_1")

ixNet.setAttribute(networkGroup4 , '-name', "MAC_Pool_2")

ixNet.setAttribute(networkGroup3 , '-multiplier', "1")
ixNet.setAttribute(networkGroup4 , '-multiplier', "1")


mac3 = ixNet.getList(networkGroup3, 'macPools') [0]
mac4 = ixNet.getList(networkGroup4, 'macPools') [0]

print ('Configuring IPv4 Addresses associated with CMAC Addresses')

ipv4PrefixPools1 = ixNet.add(mac3, 'ipv4PrefixPools')
ixNet.commit()
ipv4PrefixPools2 = ixNet.add(mac4, 'ipv4PrefixPools')
ixNet.commit()


print ('Changing no. of CMAC Addresses')
ixNet.setAttribute(mac3 , '-numberOfAddresses', "1")
ixNet.commit()

ixNet.setAttribute(mac4 , '-numberOfAddresses', "1")
ixNet.commit()


print ('Changing MAC Addresses of CMAC Ranges')
ixNet.setMultiAttribute(ixNet.getAttribute(mac3, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '66:66:66:66:66:66',
    '-step',      '00:00:00:00:00:01')

ixNet.setAttribute(ixNet.getAttribute(mac4, '-mac') + '/singleValue',
    '-value', '88:88:88:88:88:88')
ixNet.commit()


print  ('Enabling using of VLAN  in CMAC Ranges')

ixNet.setAttribute(mac3 , '-useVlans', "true")
ixNet.commit()

ixNet.setAttribute(mac4 , '-useVlans', "true")
ixNet.commit()


print  ('Configuring CMAC Vlan properties')
cMacvlan1 = ixNet.getList(mac3, 'vlan') [0]
cMacvlan2 = ixNet.getList(mac4, 'vlan') [0]

print  ('"Configuring VLAN Ids')

ixNet.setMultiAttribute(ixNet.getAttribute(cMacvlan1, '-vlanId') + '/counter',
    '-direction', 'increment',
    '-start',     '501',
    '-step',      '1')
ixNet.commit()

ixNet.setMultiAttribute(ixNet.getAttribute(cMacvlan2, '-vlanId') + '/counter',
    '-direction', 'increment',
    '-start',     '501',
    '-step',      '1')
ixNet.commit()

print  ('Configuring VLAN Priorities')

ixNet.setAttribute(ixNet.getAttribute(cMacvlan1, '-priority') + '/singleValue',
    '-value', '7')
ixNet.commit()

ixNet.setAttribute(ixNet.getAttribute(cMacvlan2, '-priority') + '/singleValue',
    '-value', '7')
ixNet.commit()


print  ('Changing VNI related Parameters under CMAC Properties')

cMacProperties1 = ixNet.getList(mac3, 'cMacProperties') [0]
cMacProperties2 = ixNet.getList(mac4, 'cMacProperties') [0]


print  ('Changing 1st Label(L2VNI)')
ixNet.setMultiAttribute(ixNet.getAttribute(cMacProperties1, '-firstLabelStart') + '/counter',
    '-direction', 'increment',
    '-start',     '1001',
    '-step',      '10')
ixNet.commit()

ixNet.setMultiAttribute(ixNet.getAttribute(cMacProperties2, '-firstLabelStart') + '/counter',
    '-direction', 'increment',
    '-start',     '1001',
    '-step',      '10')
ixNet.commit()
################################################################################

print  ('Changing 2nd Label(L3VNI)')
ixNet.setMultiAttribute(ixNet.getAttribute(cMacProperties1, '-secondLabelStart') + '/counter',
    '-direction', 'increment',
    '-start',     '2001',
    '-step',      '10')
ixNet.commit()

ixNet.setMultiAttribute(ixNet.getAttribute(cMacProperties2, '-secondLabelStart') + '/counter',
    '-direction', 'increment',
    '-start',     '2001',
    '-step',      '10')
ixNet.commit()

print  ('Changing Increment Modes across all VNIs')


ixNet.setAttribute(ixNet.getAttribute(cMacProperties1, '-labelMode') + '/singleValue',
    '-value', 'increment')
ixNet.commit()

ixNet.setAttribute(ixNet.getAttribute(cMacProperties2, '-labelMode') + '/singleValue',
    '-value', 'increment')
ixNet.commit()


print  ('Changing VNI step')
ixNet.setMultiAttribute(ixNet.getAttribute(cMacProperties1, '-labelStep') + '/counter',
    '-direction', 'increment',
    '-start',     '1',
    '-step',      '0')
ixNet.commit()

ixNet.setMultiAttribute(ixNet.getAttribute(cMacProperties2, '-labelStep') + '/counter',
    '-direction', 'increment',
    '-start',     '1',
    '-step',      '0')
ixNet.commit()

# ##############################################################################

################################################################################
# 2> Start of protocol.
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)
################################################################################
# 3> Retrieve protocol statistics.
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
# 4> Retrieve protocol learned info
###############################################################################
print("Fetching EVPN-VXLAN Learned Info")
ixNet.execute('getEVPNLearnedInfo', bgpIpv4Peer1, '1')
time.sleep(5)
linfo  = ixNet.getList(bgpIpv4Peer1, 'learnedInfo')[0]

print("EVPN VXLAN learned info")
linfoList = ixNet.getList(linfo, 'table')
print("***************************************************")
for table in linfoList :
     tableType = ixNet.getAttribute(table, '-type')
     print(tableType)
     print("=================================================")
     columns = ixNet.getAttribute(table, '-columns')
     print(columns)
     values = ixNet.getAttribute(table, '-values')
     for value in values :
          for word in values :
               print(word)
          #end for
      # end for
# end for
print("***************************************************")

################################################################################
# 5> Apply changes on the fly.
################################################################################
print("Changing Host IP Address Value associated with CMAC in Topology 2")
ixNet.setAttribute(ixNet.getAttribute(ipv4PrefixPools2, '-networkAddress') + '/singleValue',
    '-value', '203.101.1.1')
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
# 6> Retrieve protocol learned info to show On The Fly changes
###############################################################################
print("Fetching EVPN-VXLAN Learned Info")
ixNet.execute('getEVPNLearnedInfo', bgpIpv4Peer1, '1')
time.sleep(5)
linfo  = ixNet.getList(bgpIpv4Peer1, 'learnedInfo')[0]

print("EVPN VXLAN learned info")
linfoList = ixNet.getList(linfo, 'table')
print("***************************************************")
for table in linfoList :
     tableType = ixNet.getAttribute(table, '-type')
     print(tableType)
     print("=================================================")
     columns = ixNet.getAttribute(table, '-columns')
     print(columns)
     values = ixNet.getAttribute(table, '-values')
     for value in values :
          for word in values :
               print(word)
          #end for
      # end for
# end for
print("***************************************************")

################################################################################
# 7> Configure L2-L3 traffic
################################################################################
print("Configuring L2-L3 Traffic Item")
trafficItem1 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem1, '-name', 'EVPN VXLAN Traffic 1',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv4')
ixNet.commit()

trafficItem1 = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')

ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', [],
    '-scalableSources',       [],
    '-multicastReceivers',    [],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               ipv4PrefixPools1,
    '-destinations',          ipv4PrefixPools2)
ixNet.commit()

ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['mplsFlowDescriptor0', 'sourceDestEndpointPair0', 'ethernetIiWithoutFcsSourceaddress0', 'vxlanVni0', 'ipv4SourceIp1', 'ethernetIiWithoutFcsDestinationaddress0', 'ipv4DestIp1', 'trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         [])
ixNet.commit()

###############################################################################
# 8> Apply and start L2/L3 traffic
###############################################################################
print ('applying L2/L3 traffic')
ixNet.execute('apply', ixNet.getRoot() + '/traffic')
time.sleep(5)

print ('starting L2/L3 traffic')
ixNet.execute('start', ixNet.getRoot() + '/traffic')

print ('let traffic run for 120 second')
time.sleep(120)
###############################################################################
# 9> Retrieve L2/L3 traffic item statistics.
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
# 10> Stop L2/L3 traffic.
################################################################################
print ('Stopping L2/L3 traffic')
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)
################################################################################
# 11> Stop all protocols.
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
print ('!!! Test Script Ends !!!')
