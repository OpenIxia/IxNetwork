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
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################
#################################################################################
#                                                                               #
# Description:                                                                  #
#    This script intends to demonstrate how to use NGPF API for NGMVPN-BIER     #
#    with underlay ISIS                                                         #
# About Topology:                                                               #
#    Within topology both Sender and Receiver PEs are configured, each behind   #
#    Ingress and Egress P routers respectively. PMSI tunnels used in topology   #
#    is BIER. Both I-PMSI and S-PMSI tunnels for IPv4 multicast streams are     #
#    configured. Multicast traffic soruce address are distributed by BGP as     #
#    MVPN routes (AFI:1,SAFI:129) with TYPE I-PMSI, S-PMSI & Leaf AD. ISIS is   #
#    being used as underlay & IGP for BIER emulation. It provides Label for     #
#    multicast stream as per PMSI tunnel configration based on BSL,SD & SI.     #
#    I-PMSI, S-PMSI Multicast L2-L3 Traffic from Sender to Receiver are         #
#    configured.                                                                #
# Script Flow:                                                                  #
#    Step 1. Configuration of protocols.                                        #
#    Configuration flow of the script is as follow:                             #
#        i.   Add ISIS router and enable BIER and configure BIER related        #
#             parameters.                                                       #
#        ii.  Add Network Topology(NT) and configure BIER related parameters.   #
#        iii. Add chain DG behind both P routers                                #
#        iv.  Add loopback on chained DG, confiugre BGP on loopback.            #
#              add mVRF over BGP within chain DG.                               #
#        v.   Configure I-PMSI Tunnel as BIER related parameterfor mVRF at BFIR #
#              and BFER as well as  Traffic related parameters                  #
#        vi.  Add mVRF Route Range(IPv4) as Sender Site behind BFIR and as      #
#             Receiver Site behind BFER.                                        #
#        vii. Configuring S-PMSI Tunnel as BIER at Sender Site and configure    #
#             BIER realted parameter and Traffic related parameters as well.    #
#        Step 2. Start of protocol                                              #
#        Step 3. Retrieve protocol statistics                                   #
#        Step 4. S-PMSI Trigger                                                 #
#        Step 5. Retrieve IPv4 mVPN learned info                                #
#        Step 6. Configure L2-L3 IPv4 I-PMSI traffic.                           #
#        Step 7. Configure L2-L3 IPv4 S-PMSI traffic.                           #
#        Step 8. Apply and start L2/L3 traffic.                                 #
#        Step 9. Retrieve L2/L3 traffic item statistics.                        #
#        Step 10. Stop L2/L3 traffic.                                           #
#        Step 11. Stop all protocols.                                           #
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
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.50-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.39.40.148'
ixTclPort   = '8239'
ports       = [('10.39.50.123', '11', '7',), ('10.39.50.123', '11', '8',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.50',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')
#################################################################################
# 1. Configuration of protocols
#################################################################################

assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

print ("Adding 2 vports")
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

print ('Renaming the topologies and the device groups')
ixNet.setAttribute(topo1, '-name', 'Ingress Topology: Sender')
ixNet.setAttribute(topo2, '-name', 'Egress Topology: Receiver')

print ("Adding 2 device groups")
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices[0]
t2dev1 = t2devices[0]
ixNet.setAttribute(t1dev1, '-name', 'Sender P Router')
ixNet.setAttribute(t2dev1, '-name', 'Receiver P Router')
ixNet.commit()

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
    '-start',     '22:22:22:22:22:22',
    '-step',      '00:00:00:00:00:01')

ixNet.setAttribute(ixNet.getAttribute(mac2, '-mac') + '/singleValue',
    '-value', '44:44:44:44:44:44')
ixNet.commit()

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
ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')
ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

print ('Adding ISIS over Ethernet stacks')
ixNet.add(mac1, 'isisL3')
ixNet.add(mac2, 'isisL3')
ixNet.commit()
isisL3_1 = ixNet.getList(mac1, 'isisL3')[0]
isisL3_2 = ixNet.getList(mac2, 'isisL3')[0]

print ('Making the NetworkType to Point to Point in the first ISIS router')
networkTypeMultiValue1 = ixNet.getAttribute(isisL3_1, '-networkType')
ixNet.setMultiAttribute(networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(networkTypeMultiValue1 + '/singleValue', '-value', 'pointpoint')
ixNet.commit()

print('Making the NetworkType to Point to Point in the Second ISIS router')
networkTypeMultiValue2 = ixNet.getAttribute(isisL3_2, '-networkType')
ixNet.setMultiAttribute(networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(networkTypeMultiValue2 + '/singleValue', '-value', 'pointpoint')
ixNet.commit()

print ('Disabling the Discard Learned Info CheckBox')
isisL3RouterDiscardLearnedLSP1 = ixNet.getAttribute(ixNet.getList(t1dev1, 'isisL3Router')[0], '-discardLSPs')
isisL3RouterDiscardLearnedLSP2 = ixNet.getAttribute(ixNet.getList(t2dev1, 'isisL3Router')[0], '-discardLSPs')

ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP1 + '/singleValue', '-value', 'False')
ixNet.commit()
ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP2 + '/singleValue', '-value', 'False')
ixNet.commit()

isisL3Router1_1 = ixNet.getList(t1dev1, 'isisL3Router')[0]
isisL3Router1_2 = ixNet.getList(t2dev1, 'isisL3Router')[0]

# BIER related configuration
print ('Enabling BIER')
ixNet.setAttribute(isisL3Router1_1, '-enableBIER', '1')
ixNet.setAttribute(isisL3Router1_2, '-enableBIER', '1')
ixNet.commit()

print ('Setting Node Prefix')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3Router1_1, '-BIERNodePrefix') + '/singleValue', '-value', '30.30.30.1')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3Router1_2, '-BIERNodePrefix') + '/singleValue', '-value', '60.60.60.1')
ixNet.commit()

print ('Setting Prefix Attribute Flag')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3Router1_1, '-includePrefixAttrFlags') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3Router1_2, '-includePrefixAttrFlags') + '/singleValue', '-value', 'true')
ixNet.commit()

print ('Setting R Flag')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3Router1_1, '-bierRFlag') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3Router1_2, '-bierRFlag') + '/singleValue', '-value', 'true')
ixNet.commit()

print ('Setting SubDomainId value')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3Router1_1+'/isisBierSubDomainList', '-subDomainId') + '/singleValue', '-value', '41')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3Router1_2+'/isisBierSubDomainList', '-subDomainId') + '/singleValue', '-value', '41')
ixNet.commit()

print ('Setting BFR Id value')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3Router1_1+'/isisBierSubDomainList', '-BFRId') + '/singleValue', '-value', '141')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3Router1_2+'/isisBierSubDomainList', '-BFRId') + '/singleValue', '-value', '142')
ixNet.commit()

bitStringObj1 = ixNet.getList(isisL3Router1_1+'/isisBierSubDomainList', 'isisBierBSObjectList')[0]
bitStringObj2 = ixNet.getList(isisL3Router1_2+'/isisBierSubDomainList', 'isisBierBSObjectList')[0]

print ('Setting Bit String Length')
ixNet.setMultiAttribute(ixNet.getAttribute(bitStringObj1, '-BIERBitStringLength') + '/singleValue', '-value', '4096bits')
ixNet.setMultiAttribute(ixNet.getAttribute(bitStringObj2, '-BIERBitStringLength') + '/singleValue', '-value', '4096bits')
ixNet.commit()

print ('Setting Label Range Size')
ixNet.setMultiAttribute(ixNet.getAttribute(bitStringObj1, '-labelRangeSize') + '/singleValue', '-value', '5')
ixNet.setMultiAttribute(ixNet.getAttribute(bitStringObj2, '-labelRangeSize') + '/singleValue', '-value', '5')
ixNet.commit()

print ('Setting Label Start value')
ixNet.setMultiAttribute(ixNet.getAttribute(bitStringObj1, '-labelStart') + '/singleValue', '-value', '444')
ixNet.setMultiAttribute(ixNet.getAttribute(bitStringObj2, '-labelStart') + '/singleValue', '-value', '44')
ixNet.commit()

print('Adding Network Topology')
ixNet.add(t1dev1, 'networkGroup')
ixNet.add(t2dev1, 'networkGroup')
ixNet.commit()

networkGroup1 = ixNet.getList(t1dev1, 'networkGroup')[0]
networkGroup2 = ixNet.getList(t2dev1, 'networkGroup')[0]

print('Adding the Network Topology')
ixNet.add(networkGroup1, 'ipv4PrefixPools')
ixNet.add(networkGroup2, 'ipv4PrefixPools')
ixNet.commit()

netTopo1 =ixNet.getList(networkGroup1, 'ipv4PrefixPools')
netTopo2 =ixNet.getList(networkGroup2, 'ipv4PrefixPools')

netTopo1 = ixNet.remapIds(netTopo1)[0]
netTopo2 = ixNet.remapIds(netTopo2)[0]
ixNet.commit()

print("Renaming Network Topology")
ixNet.setAttribute(networkGroup1, '-name', 'NG1 For PE Loopback Address')
ixNet.setAttribute(networkGroup2, '-name', 'NG2 For PE Loopback Address')
ixNet.commit()

ixNet.setAttribute(netTopo1, '-numberOfAddresses', '5')
ixNet.setAttribute(netTopo2, '-numberOfAddresses', '5')
ixNet.commit()

ixNet.setMultiAttribute(ixNet.getAttribute(netTopo1, '-networkAddress') + '/singleValue', '-value', '2.2.2.2')
ixNet.setMultiAttribute(ixNet.getAttribute(netTopo2, '-networkAddress') + '/singleValue', '-value', '3.2.2.2')
ixNet.commit()

ixNet.setMultiAttribute(ixNet.getAttribute(netTopo1, '-prefixLength') + '/singleValue', '-value', '32')
ixNet.setMultiAttribute(ixNet.getAttribute(netTopo2, '-prefixLength') + '/singleValue', '-value', '32')
ixNet.commit()

isisL3RouteProperty1 = ixNet.getList(netTopo1, 'isisL3RouteProperty')[0]
isisL3RouteProperty2 = ixNet.getList(netTopo2, 'isisL3RouteProperty')[0]

print ('Configuring BIER in network group')
print ('Setting Sub-domain Id')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3RouteProperty1, '-subDomainId') + '/singleValue', '-value', '41')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3RouteProperty2, '-subDomainId') + '/singleValue', '-value', '41')
ixNet.commit()

print ('Setting IPA')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3RouteProperty1, '-IPA') + '/singleValue', '-value', '49')
ixNet.commit()

print ('Setting BFR Id')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3RouteProperty1, '-BFRId') + '/singleValue', '-value', '12')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3RouteProperty2, '-BFRId') + '/singleValue', '-value', '14')
ixNet.commit()

print ('Setting Bit String Length')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3RouteProperty1, '-BIERBitStringLength') + '/singleValue', '-value', '4096bits')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3RouteProperty2, '-BIERBitStringLength') + '/singleValue', '-value', '4096bits')
ixNet.commit()

print ('Setting Label Range Size')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3RouteProperty1, '-labelRangeSize') + '/singleValue', '-value', '5')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3RouteProperty2, '-labelRangeSize') + '/singleValue', '-value', '5')
ixNet.commit()

print ('Setting Label Range Start')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3RouteProperty1, '-labelStart') + '/singleValue', '-value', '1111')
ixNet.setMultiAttribute(ixNet.getAttribute(isisL3RouteProperty2, '-labelStart') + '/singleValue', '-value', '2222')
ixNet.commit()

print ('adding Chained DG behind IPv4 Address Pool in Ingress Topology')
chainedDg1 = ixNet.add(networkGroup1, 'deviceGroup')
ixNet.setMultiAttribute(chainedDg1, '-multiplier', '5', '-name', 'BFIR')
ixNet.commit()

chainedDg1 = ixNet.remapIds(chainedDg1)[0]
loopback1 = ixNet.add(chainedDg1, 'ipv4Loopback')
ixNet.setMultiAttribute(loopback1, '-stackedLayers', [], '-name', 'IPv4 Loopback 1')
ixNet.commit()

print ('adding Chained DG behind Network topology in Egress Topology')
chainedDg2 = ixNet.add(networkGroup2, 'deviceGroup')
ixNet.setMultiAttribute(chainedDg2, '-multiplier', '5', '-name', 'BFER')
ixNet.commit()

chainedDg2 = ixNet.remapIds(chainedDg2)[0]
loopback2 = ixNet.add(chainedDg2, 'ipv4Loopback')
ixNet.setMultiAttribute(loopback2, '-stackedLayers', [], '-name', 'IPv4 Loopback 2')
ixNet.commit()

print ('Adding BGP over IPv4 loopback interfaces')
ixNet.add(loopback1, 'bgpIpv4Peer')
ixNet.add(loopback2, 'bgpIpv4Peer')
ixNet.commit()

bgp1 = ixNet.getList(loopback1, 'bgpIpv4Peer')[0]
bgp2 = ixNet.getList(loopback2, 'bgpIpv4Peer')[0]

print ('Setting IPs in BGP DUT IP tab')
dutIp1 = ixNet.add(ixNet.getAttribute(bgp1, '-dutIp'), 'counter')
dutIp2 = ixNet.add(ixNet.getAttribute(bgp2, '-dutIp'), 'counter')

ixNet.setMultiAttribute(dutIp1, '-step', '0.0.0.1', '-start', '3.2.2.2', '-direction', 'increment')
ixNet.setMultiAttribute(dutIp2, '-step', '0.0.0.1', '-start', '2.2.2.2', '-direction', 'increment')
ixNet.commit()

print ('Enabling MVPN Capabilities for BGP Router')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-capabilityIpV4MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-capabilityIpV4Multicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-capabilityIpV4MulticastVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-ipv4MulticastBgpMplsVpn') + '/singleValue', '-value', 'true')
ixNet.commit()

ixNet.setAttribute(ixNet.getAttribute(bgp2, '-capabilityIpV4MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-capabilityIpV4Multicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-capabilityIpV4MulticastVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-ipv4MulticastBgpMplsVpn') + '/singleValue', '-value', 'true')
ixNet.commit()

print ('Enabling MVPN Learned Information for BGP Router')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-filterIpV4Unicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-filterIpV4MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-filterIpv4MulticastBgpMplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-filterIpV4MulticastVpn') + '/singleValue', '-value', 'true')
ixNet.commit()

ixNet.setAttribute(ixNet.getAttribute(bgp2, '-filterIpV4Unicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-filterIpV4MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-filterIpv4MulticastBgpMplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-filterIpV4MulticastVpn') + '/singleValue', '-value', 'true')
ixNet.commit()

print ('Adding mVRF over BGP on both ports')
ixNet.add(bgp1, 'bgpIpv4MVrf')
ixNet.add(bgp2, 'bgpIpv4MVrf')
ixNet.commit()

mVRF1 = ixNet.getList(bgp1, 'bgpIpv4MVrf')[0]
mVRF2 = ixNet.getList(bgp2, 'bgpIpv4MVrf')[0]

print('etting Tunnel Type as BIER for I-PMSI')
ixNet.setAttribute(ixNet.getAttribute(mVRF1, '-multicastTunnelType') + '/singleValue', '-value', 'tunneltypebier')
ixNet.setAttribute(ixNet.getAttribute(mVRF2, '-multicastTunnelType') + '/singleValue', '-value', 'tunneltypebier')
ixNet.commit()

print ('Assigning value for Up/DownStream Assigned Label for I-PMSI')
ixNet.setMultiAttribute(ixNet.getAttribute(mVRF1, '-upOrDownStreamAssignedLabel') + '/counter', '-step', '1', '-start', '3333', '-direction', 'increment')
ixNet.setMultiAttribute(ixNet.getAttribute(mVRF2, '-upOrDownStreamAssignedLabel') + '/counter', '-step', '1', '-start', '4444', '-direction', 'increment')
ixNet.commit()

print('Setting Sub Domain ID for I-PMSI')
ixNet.setAttribute(ixNet.getAttribute(mVRF1, '-BIERSubDomainId') + '/singleValue', '-value', '41')
ixNet.setAttribute(ixNet.getAttribute(mVRF2, '-BIERSubDomainId') + '/singleValue', '-value', '41')
ixNet.commit()

print('Setting BFR ID for I-PMSI')
ixNet.setMultiAttribute(ixNet.getAttribute(mVRF1, '-BFRId') + '/counter', '-step', '1', '-start', '33', '-direction', 'increment')
ixNet.setMultiAttribute(ixNet.getAttribute(mVRF2, '-BFRId') + '/counter', '-step', '1', '-start', '44', '-direction', 'increment')
ixNet.commit()

print('Setting BFR IPv4 Prefix for I-PMSI')
ixNet.setMultiAttribute(ixNet.getAttribute(mVRF1, '-BFRIpv4Prefix') + '/counter', '-step', '0.0.0.1', '-start', '33.1.1.1', '-direction', 'increment')
ixNet.setMultiAttribute(ixNet.getAttribute(mVRF2, '-BFRIpv4Prefix') + '/counter', '-step', '0.0.0.1', '-start', '44.1.1.1', '-direction', 'increment')
ixNet.commit()

print('Setting Bit String Length for I-PMSI')
ixNet.setAttribute(ixNet.getAttribute(mVRF1, '-bierBitStringLength') + '/singleValue', '-value', '4096bits')
ixNet.setAttribute(ixNet.getAttribute(mVRF2, '-bierBitStringLength') + '/singleValue', '-value', '4096bits')
ixNet.commit()

print ('Setting Entropy for I-PMSI')
ixNet.setAttribute(ixNet.getAttribute(mVRF1, '-entropy') + '/singleValue', '-value', '100')

print('Setting OAM for I-PMSI')
ixNet.setAttribute(ixNet.getAttribute(mVRF1, '-oam') + '/singleValue', '-value', '2')

print('Setting DSCP for I-PMSI')
ixNet.setAttribute(ixNet.getAttribute(mVRF1, '-dscp') + '/singleValue', '-value', '63')

print ('Adding Network Group behind mVRF for Ingress Topology')
ixNet.add(chainedDg1, 'networkGroup')
ixNet.commit()
networkGroup3 = ixNet.getList(chainedDg1, 'networkGroup')[0]
ixNet.setAttribute(networkGroup3, '-name', 'Sender Site')
ixNet.commit()

print ('Adding Network Group behind mVRF for Egress Topology')
ixNet.add(chainedDg2, 'networkGroup')
ixNet.commit()
networkGroup4 = ixNet.getList(chainedDg2, 'networkGroup')[0]
ixNet.setAttribute(networkGroup4, '-name', 'Receiver Site')
ixNet.commit()

print ('Adding IPv4 Prefix pools in Ingress Topology behind Sender PE router')
ixNet.add(networkGroup3, 'ipv4PrefixPools')
ixNet.commit()

print ('Adding IPv4 Prefix pools in Egress Topology behind Receiver PE router')
ixNet.add(networkGroup4, 'ipv4PrefixPools')
ixNet.commit()

print ('Disabling Sender site and enabling Receiver Site for both IPv4 in Egress Topology')
ipv4PrefixPools3 = ixNet.getList(networkGroup3, 'ipv4PrefixPools')[0]
ipv4PrefixPools4 = ixNet.getList(networkGroup4, 'ipv4PrefixPools')[0]
bgpL3VpnRouteProperty4 = ixNet.getList(ipv4PrefixPools4, 'bgpL3VpnRouteProperty')[0]

ixNet.setAttribute(bgpL3VpnRouteProperty4, '-enableIpv4Sender', 'False')
ixNet.setAttribute(bgpL3VpnRouteProperty4, '-enableIpv4Receiver', 'True')
ixNet.commit()

bgpMVpnSenderSitesIpv4 = ixNet.getList(ipv4PrefixPools3, 'bgpMVpnSenderSitesIpv4')[0]
bgpMVpnReceiverSitesIpv4 = ixNet.getList(ipv4PrefixPools4, 'bgpMVpnReceiverSitesIpv4')[0]

print ('Changing Group Address Count for IPv4 Cloud in Sender Site')
mulValGCount = ixNet.getAttribute(bgpMVpnSenderSitesIpv4, '-groupAddressCount')
ixNet.setMultiAttribute(mulValGCount + '/singleValue', '-value', '3')
ixNet.commit()

print ('Changing Source Address Count for IPv4 Cloud in Sender Site')
mulValSCount = ixNet.getAttribute(bgpMVpnSenderSitesIpv4, '-sourceAddressCount')
ixNet.setMultiAttribute(mulValSCount + '/singleValue', '-value', '2')
ixNet.commit()

print ('Changing Group Address for IPv4 Cloud in Sender Site')
mulValGAdd = ixNet.getAttribute(bgpMVpnSenderSitesIpv4, '-startGroupAddressIpv4')
ixNet.setMultiAttribute(mulValGAdd + '/counter', '-step', '0.0.1.0', '-start', '234.161.1.1', '-direction', 'increment')
ixNet.commit()

print ('Changing Source Address for IPv4 Cloud in Sender Site')
mulValSAdd = ixNet.getAttribute(bgpMVpnSenderSitesIpv4, '-startSourceAddressIpv4')
ixNet.setMultiAttribute(mulValSAdd + '/counter', '-step', '0.0.1.0', '-start', '191.0.1.1', '-direction', 'increment')
ixNet.commit()

print ('Changing Group Address Count for IPv4 Cloud in Receiver Site')
mulValGCount = ixNet.getAttribute(bgpMVpnReceiverSitesIpv4, '-groupAddressCount')
ixNet.setMultiAttribute(mulValGCount + '/singleValue', '-value', '3')
ixNet.commit()

print ('Changing Source Address Count for IPv4 Cloud in Receiver Site')
mulValSCount = ixNet.getAttribute(bgpMVpnReceiverSitesIpv4, '-sourceAddressCount')
ixNet.setMultiAttribute(mulValSCount + '/singleValue', '-value', '2')
ixNet.commit()

print ('Changing Group Address for IPv4 Cloud in Receiver Site')
mulValGAdd = ixNet.getAttribute(bgpMVpnReceiverSitesIpv4, '-startGroupAddressIpv4')
ixNet.setMultiAttribute(mulValGAdd + '/counter', '-step', '0.0.1.0', '-start', '234.161.1.1', '-direction', 'increment')
ixNet.commit()

print ('Changing Source Address for IPv4 Cloud in Receiver Site')
mulValSAdd = ixNet.getAttribute(bgpMVpnReceiverSitesIpv4, '-startSourceAddressIpv4')
ixNet.setMultiAttribute(mulValSAdd + '/counter', '-step', '0.0.1.0', '-start', '191.0.1.1', '-direction', 'increment')
ixNet.commit()

print ('Changing Prefix Length for IPv4 Address Pool in Sender Site')
mulValPrefLen = ixNet.getAttribute(ipv4PrefixPools3, '-prefixLength')
ixNet.setMultiAttribute(mulValPrefLen + '/singleValue', '-value', '32')
ixNet.commit()

print ('Changing Prefix Length for IPv4 Address Pool in Receiver Site')
mulValPrefLen = ixNet.getAttribute(ipv4PrefixPools4, '-prefixLength')
ixNet.setMultiAttribute(mulValPrefLen + '/singleValue', '-value', '32')
ixNet.commit()

print ('Configuring S-PMSI on Sender SItes')
bgpMVpnSenderSiteSpmsiV4 = ixNet.getList(bgpMVpnSenderSitesIpv4, 'bgpMVpnSenderSiteSpmsiV4')[0]

print('Setting Tunnel Type as BIER for S-PMSI')
ixNet.setAttribute(ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-multicastTunnelType') + '/singleValue', '-value', 'tunneltypebier')
ixNet.commit()

print('Setting Sub-domain Id value  for S-PMSI')
ixNet.setAttribute(ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-BIERSubDomainId') + '/singleValue', '-value', '41')
ixNet.commit()

print('Setting BFR ID  for S-PMSI')
ixNet.setMultiAttribute(ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-BFRId') + '/counter', '-step', '1', '-start', '200', '-direction', 'increment')
ixNet.commit()

print('Setting BFR IPv4 Prefix for S-PMSI at Sender Site (same as own loopback ip')
ixNet.setMultiAttribute(ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-BFRIpv4Prefix') + '/counter', '-step', '0.0.0.1', '-start', '2.2.2.2', '-direction', 'increment')
ixNet.commit()

print ('Assigning value for Up/DownStream Assigned Label for S-PMSI')
ixNet.setMultiAttribute(ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-upstreamOrDownstreamAssignedLabel') + '/counter', '-step', '1', '-start', '5555', '-direction', 'increment')
ixNet.commit()

print ('Setting Bit String Length for S-PMSI')
ixNet.setMultiAttribute(ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-bierBitStringLength') + '/singleValue', '-value', '4096bits')

print ('Setting Entropy for S-PMSI')
ixNet.setAttribute(ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-entropy') + '/singleValue', '-value', '999')

print('Setting OAM for S-PMSI')
ixNet.setAttribute(ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-oam') + '/singleValue', '-value', '3')

print('Setting DSCP for S-PMSI')
ixNet.setMultiAttribute(ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-dscp') + '/singleValue', '-value', '50')
ixNet.commit()

print('Setting BFR ID Receiver Site')
ixNet.setMultiAttribute(ixNet.getAttribute(bgpMVpnReceiverSitesIpv4, '-BFRId') + '/counter', '-step', '1', '-start', '300', '-direction', 'increment')
ixNet.commit()

print('Setting BFR IPv4 Prefix for S-PMSI at Receiver Site (same as own loopback ip')
ixNet.setMultiAttribute(ixNet.getAttribute(bgpMVpnReceiverSitesIpv4, '-BFRIpv4Prefix') + '/counter', '-step', '0.0.0.1', '-start', '3.2.2.2', '-direction', 'increment')
ixNet.commit()


################################################################################
# 2. Start protocols.
################################################################################
print ('Wait for 5 seconds before starting protocol')
time.sleep(5)
print("Starting protocols and waiting for 2 min for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(120)

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
print ('Fetching all BGP Peer Per Port\n')
viewPage  = '::ixNet::OBJ-/statistics/view:"BGP Peer Per Port"/page'
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

################################################################################
# 4. S-PMSI Trigger
################################################################################
print ('Switching to S-PMSI for IPv4 Cloud from Sender Site')
try :
    ixNet.execute('switchToSpmsi', bgpMVpnSenderSitesIpv4)
except :
    print ('error in S-PMSI Trigger')
# end try/expectX
time.sleep(10)

###############################################################################
# 5. Retrieve BGP MVPN learned info
###############################################################################
print ('Fetching mVPN Learned Info in Ingress Topology')
ixNet.execute('getIpv4MvpnLearnedInfo', bgp1, '1')
print(' %%%%%%%%%%%%%%%%% Learned Info fetched')
time.sleep(5)
print ('IPv4 MVPN Learned Info at BFIR')
linfo  = ixNet.getList(bgp1, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

print ('Fetching mVPN Learned Info in Egress Topology')
ixNet.execute('getIpv4MvpnLearnedInfo', bgp2, '1')
print(' %%%%%%%%%%%%%%%%% Learned Info fetched')
time.sleep(5)
print ('IPv4 MVPN Learned Info at BFER')
linfo  = ixNet.getList(bgp2, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# 6. Configure L2-L3 IPv4 I-PMSI traffic.
################################################################################
print ('Configuring L2-L3 IPv4 I-PMSI Traffic Item')
ipmsiTrafficItem = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(ipmsiTrafficItem, '-name', 'NGMVPN I-PMSI Traffic',
                        '-multicastForwardingMode', 'replication',
                        '-useControlPlaneRate', 'true',
                        '-useControlPlaneFrameSize', 'true',
                        '-roundRobinPacketOrdering', 'false',
                        '-numVlansForMulticastReplication', '1',
                        '-trafficType', 'ipv4')
ixNet.commit()

ipmsiTrafficItem = ixNet.remapIds(ipmsiTrafficItem)[0]
endpointSet = ixNet.add(ipmsiTrafficItem, 'endpointSet')
destination  = ['bgpMVpnReceiverSitesIpv4']

ixNet.setMultiAttribute(endpointSet,
    '-name',                  'EndpointSet-1',
    '-sources',               bgpMVpnSenderSitesIpv4,
    '-multicastDestinations', [['false','none','234.161.1.1','0.0.0.1','3'],['false','none','234.161.2.1','0.0.0.1','3'],['false','none','234.161.3.1','0.0.0.1','3'],['false','none','234.161.4.1','0.0.0.1','3'],['false','none','234.161.5.1','0.0.0.1','3']])
ixNet.commit()

endpointSet = ixNet.remapIds(endpointSet)[0]

ixNet.setMultiAttribute(ipmsiTrafficItem+'/configElement:1/frameSize', '-fixedSize', '570')
ixNet.setMultiAttribute(ipmsiTrafficItem+'/configElement:1/frameRate', '-rate', '1000', '-type', 'framesPerSecond')
ixNet.setMultiAttribute(ipmsiTrafficItem+'/configElement:1/frameRateDistribution', '-streamDistribution', 'applyRateToAll')

ixNet.setMultiAttribute(ipmsiTrafficItem + '/tracking',
    '-trackBy',        ['trackingenabled0','mplsMplsLabelValue0','mplsMplsLabelValue1','ipv4DestIp0','bierBsl0'])
ixNet.commit()


################################################################################
# 7. Configure L2-L3 IPv4 S-PMSI traffic.
################################################################################
print ('Configuring L2-L3 IPv4 S-PMSI Traffic Item')
SpmsiTrafficItem = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(SpmsiTrafficItem, '-name', 'NGMVPN S-PMSI Traffic', 
			'-multicastForwardingMode', 'replication', 
			'-useControlPlaneRate', 'true', 
			'-useControlPlaneFrameSize', 'true', 
			'-roundRobinPacketOrdering', 'false', 
			'-numVlansForMulticastReplication', '1', 
			'-trafficType', 'ipv4')
ixNet.commit()

SpmsiTrafficItem = ixNet.remapIds(SpmsiTrafficItem)[0]
endpointSet = ixNet.add(SpmsiTrafficItem, 'endpointSet')
destination  = ['bgpMVpnReceiverSitesIpv4']

ixNet.setMultiAttribute(endpointSet,
    '-name',                  'EndpointSet-1',
    '-sources',               bgpMVpnSenderSiteSpmsiV4,
    '-multicastDestinations', [['false','none','234.161.1.1','0.0.0.1','3'],['false','none','234.161.2.1','0.0.0.1','3'],['false','none','234.161.3.1','0.0.0.1','3'],['false','none','234.161.4.1','0.0.0.1','3'],['false','none','234.161.5.1','0.0.0.1','3']])
ixNet.commit()

endpointSet = ixNet.remapIds(endpointSet)[0]

ixNet.setMultiAttribute(SpmsiTrafficItem+'/configElement:1/frameSize', '-fixedSize', '570')
ixNet.setMultiAttribute(SpmsiTrafficItem+'/configElement:1/frameRate', '-rate', '1000', '-type', 'framesPerSecond')
ixNet.setMultiAttribute(SpmsiTrafficItem+'/configElement:1/frameRateDistribution', '-streamDistribution', 'applyRateToAll')

ixNet.setMultiAttribute(SpmsiTrafficItem + '/tracking',
    '-trackBy',        ['trackingenabled0','mplsMplsLabelValue0','mplsMplsLabelValue1','ipv4DestIp0','bierBsl0'])
ixNet.commit()

###############################################################################
# 8. Apply and start L2/L3 traffic.
###############################################################################
print ('applying L2/L3 traffic')
ixNet.execute('apply', ixNet.getRoot() + '/traffic')
time.sleep(5)
print ('starting L2/L3 traffic')
ixNet.execute('start', ixNet.getRoot() + '/traffic')
print ('let traffic run for 60 second')
time.sleep(60)

###############################################################################
# 9. Retrieve L2/L3 traffic item statistics.
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

#################################################################################
# 10. Stop L2/L3 traffic.
#################################################################################
print ('Stopping L2/L3 traffic')
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)

################################################################################
# 11. Stop all protocols.
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
print ('!!! Test Script Ends !!!')
