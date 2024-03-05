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
#    This script intends to demonstrate how to use mLDP as P-tunnel in NGMVPN   #
#    through API.                                                               #
#    About Topology:                                                            #
#    Within topology both Sender and Receiver PEs are configured, each behind   #
#    Ingress and Egress P routers respectively. P2MP tunnels used in topology   #
#	 is mLDP-P2MP. Both I-PMSI and S-PMSI tunnels for IPv4 & Ipv6 multicast     #
#    streams are configured using mLDP-P2MP. Multicast traffic source address   #
#    are distributed by BGP as VPN routes(AFI:1,SAFI:128). Multicast L2-L3      #
#    Traffic from Seder to Receiver                                             #
# Script Flow:                                                                  #
#        Step 1. Configuration of protocols.                                    #
#    Configuration flow of the script is as follow:                             #
#         i.      Adding of OSPF router                                         #
#         ii.     Adding of Network Topology(NT)                                #
#         iii.    Enabling of TE(Traffic Engineering) and configuring loopback  #
#                         address as Router ID                                  #
#         iv.     Adding of mLDP LSPs within LDP RTR and mVRF over BGP over     #
#                  loopback within connected DG.                                #
#         v.     Configuring Parameters in mVRF at sender and Receiver PE       #
#         vi.    Adding Route Ranges(both IPv4 and v6) behind mVRF as Sender    #
#                 Router and Receiver Sites.                                    #
#         vii.   Configuring I-PMSI and S-PMSI Tunnel in Sender Sites for both  #
#                 IPv4/v6 ranges as per mLDP LSP.                               #
#        Step 2. Start of protocol                                              #
#        Step 3. Retrieve protocol statistics                                   #
#        Step 4. Retrieve IPv4 mVPN learned info                                #
#        Step 5. Apply changes on the fly                                       #
#        Step 6. S-PMSI Trigger                                                 #
#        Step 7. Retrieve protocol learned info after OTF                       #
#        Step 8. Configure L2-L3 IPv6 I-PMSI traffic.                           #
#        Step 9. Configure L2-L3 IPv4 S-PMSI traffic.                           #
#        Step 10. Apply and start L2/L3 traffic.                                #
#        Step 11. Retrieve L2/L3 traffic item statistics.                       #
#        Step 12. Stop L2/L3 traffic.                                           #
#        Step 13. Stop all protocols.                                           #
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
# IxNetwork.pm file somewhere else where we python can auto load it.
# "IxNetwork.pm" is available in <IxNetwork_installer_path>\API\Python
################################################################################
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.10-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.39.50.134'
ixTclPort   = '8819'
ports       = [('10.39.50.161', '2', '3',), ('10.39.50.161', '2', '4',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.50',
     '-setAttribute', 'strict')

# cleaning up the old config file, and creating an empty config
print("cleaning up the old config file, and creating an empty config")
ixNet.execute('newConfig')
#################################################################################
# Step 1> protocol configuration section
#################################################################################

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
print ('Renaming the topologies and the device groups')
ixNet.setAttribute(topo1, '-name', 'Ingress Topology')
ixNet.setAttribute(topo2, '-name', 'Egress Topology')
print ("Adding 2 device groups")
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices[0]
t2dev1 = t2devices[0]
ixNet.setAttribute(t1dev1, '-name', 'Sender P router')
ixNet.setAttribute(t2dev1, '-name', 'Receiver P router')
ixNet.commit()

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(t1dev1, '-multiplier', '2')
ixNet.setAttribute(t2dev1, '-multiplier', '2')
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

ixNet.setMultiAttribute(ixNet.getAttribute(mac2, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '44:44:44:44:44:44',
    '-step',      '00:00:00:00:00:01')

ixNet.commit()

print("Enabling VLAN")
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-enableVlans') + '/singleValue',
    '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(mac2, '-enableVlans') + '/singleValue',
    '-value', 'true')
ixNet.commit()

print("Configuring VLAN ID")
ixNet.setMultiAttribute(ixNet.getAttribute(mac1 +'/vlan:1', '-vlanId') + '/counter',
    '-step', '1', '-start', '400', '-direction', 'increment')
ixNet.setMultiAttribute(ixNet.getAttribute(mac2 +'/vlan:1', '-vlanId') + '/counter',
    '-step', '1', '-start', '400', '-direction', 'increment')
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
ixNet.setMultiAttribute(mvAdd1, '-pattern', 'counter', '-clearOverlays', 'False')
ixNet.commit()
ixNet.setMultiAttribute(mvAdd1 + '/counter', '-step', '0.1.0.0', '-start', '50.50.50.2', '-direction', 'increment')
ixNet.commit()

ixNet.setMultiAttribute(mvAdd2, '-pattern', 'counter', '-clearOverlays', 'False')
ixNet.commit()
ixNet.setMultiAttribute(mvAdd2 + '/counter', '-step', '0.1.0.0', '-start', '50.50.50.20', '-direction', 'increment')
ixNet.commit()

ixNet.setMultiAttribute(mvGw1, '-pattern', 'counter', '-clearOverlays', 'False')
ixNet.commit()
ixNet.setMultiAttribute(mvGw1 + '/counter', '-step', '0.1.0.0', '-start', '50.50.50.20', '-direction', 'increment')
ixNet.commit()

ixNet.setMultiAttribute(mvGw2, '-pattern', 'counter', '-clearOverlays', 'False')
ixNet.commit()
ixNet.setMultiAttribute(mvGw2 + '/counter', '-step', '0.1.0.0', '-start', '50.50.50.2', '-direction', 'increment')
ixNet.commit()

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')
ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

print ('Adding OSPFv2 over IPv4 stack')
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

print ('Adding Connected LDP-IF over IPv4 stack')
ixNet.add(ip1, 'ldpConnectedInterface')
ixNet.add(ip2, 'ldpConnectedInterface')
ixNet.commit()

print ('Adding Connected LDP-RTR over IPv4 stack')
ixNet.add(ip1, 'ldpBasicRouter')
ixNet.add(ip2, 'ldpBasicRouter')
ixNet.commit()

ldp1 = ixNet.getList(ip1, 'ldpBasicRouter')[0]
ldp2 = ixNet.getList(ip2, 'ldpBasicRouter')[0]

print ('Enabling P2MP Capability in the first LDP router')
p2MpCapability1 = ixNet.getAttribute(ldp1, '-enableP2MPCapability')
ixNet.setMultiAttribute(p2MpCapability1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(p2MpCapability1 + '/singleValue', '-value', 'true')
ixNet.commit()

print ('Enabling P2MP Capability in the second LDP router')
p2MpCapability2 = ixNet.getAttribute(ldp2, '-enableP2MPCapability')
ixNet.setMultiAttribute(p2MpCapability2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(p2MpCapability2 + '/singleValue', '-value', 'true')
ixNet.commit()

print ('Enabling Root ranges in the Sender P LDP router')
ixNet.setMultiAttribute(ldp1, '-rootRangesCountV4', '1')
ixNet.commit()
print ('Enabling Leaf ranges in the Receiver P LDP router')
ixNet.setMultiAttribute(ldp2, '-leafRangesCountV4', '1')
ixNet.commit()

print ('Enabling Root ranges in the Receiver P LDP router')
ixNet.setMultiAttribute(ldp2, '-rootRangesCountV4', '1')
ixNet.commit()
print ('Enabling Leaf ranges in the Sender P LDP router')
ixNet.setMultiAttribute(ldp1, '-leafRangesCountV4', '1')
ixNet.commit()

print('Configuring mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ldp1 + '/ldpLeafRangeV4', '-numberOfTLVs', '3')
ixNet.commit()

print('Configuring mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ldp2 + '/ldpLeafRangeV4', '-numberOfTLVs', '3')
ixNet.commit()

print('Activating mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4', '-active') + '/singleValue', '-value', 'true')
ixNet.commit()

print('Changing Continuous Increment Opaque Value Across Root in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4', '-continuousIncrementOVAcrossRoot') + '/singleValue', '-value', 'true')
ixNet.commit()

print('Changing Label Value Step in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4', '-labelValueStep') + '/singleValue', '-value', '1')
ixNet.commit()

print('Changing Label Value Start in mLDP Leaf range in Sender LDP router')
start1 = ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4', '-labelValueStart')
ixNet.setMultiAttribute(start1, '-pattern', 'counter', '-clearOverlays', 'False')
ixNet.commit()
ixNet.setMultiAttribute(start1 + '/counter', '-step', '1', '-start', '12321', '-direction', 'increment')
ixNet.commit()

print('Changing LSP count per root in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4', '-lspCountPerRoot') + '/singleValue', '-value', '2')
ixNet.commit()

print('Changing Root Address Step in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4', '-rootAddressStep') + '/singleValue', '-value', '0.0.0.1')
ixNet.commit()

print('Changing Root Address count in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4', '-rootAddressCount') + '/singleValue', '-value', '1')
ixNet.commit()

print('Changing Root Address in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4', '-rootAddress') + '/singleValue', '-value', '7.7.7.7')
ixNet.commit()

print('Changing TLV1 name in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute((ldp1 + '/ldpLeafRangeV4/ldpTLVList:1'), '-name', 'LDP Opaque TLV 1')
ixNet.commit()

print('Deactivating TLV1 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:1', '-active') + '/singleValue', '-value', 'false')
ixNet.commit()

print('Changing Type of TLV1 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:1', '-type') + '/singleValue', '-value', '1')
ixNet.commit()

print('Changing Length of TLV1 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:1', '-tlvLength') + '/singleValue', '-value', '4')
ixNet.commit()

print('Changing Value of TLV1 in mLDP Leaf range in Sender LDP router')
val1 = ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:1', '-value')
ixNet.setMultiAttribute(val1, '-pattern', 'counter', '-clearOverlays', 'False')
ixNet.commit()
ixNet.setMultiAttribute(val1 + '/counter', '-step', '01', '-start', '00000001', '-direction', 'increment')
ixNet.commit()

print('Changing Increment of TLV1 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:1', '-increment') + '/singleValue', '-value', '00000001')
ixNet.commit()

print('Changing TLV2 name in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute((ldp1 + '/ldpLeafRangeV4/ldpTLVList:2'), '-name', 'LDP Opaque TLV 2')
ixNet.commit()

print('Activating TLV2 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:2', '-active') + '/singleValue', '-value', 'true')
ixNet.commit()

print('Changing Type of TLV2 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:2', '-type') + '/singleValue', '-value', '123')
ixNet.commit()

print('Changing Length of TLV2 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:2', '-tlvLength') + '/singleValue', '-value', '5')
ixNet.commit()

print('Changing Value of TLV2 in mLDP Leaf range in Sender LDP router')
val2 = ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:2', '-value')
ixNet.setMultiAttribute(val2, '-pattern', 'counter', '-clearOverlays', 'False')
ixNet.commit()
ixNet.setMultiAttribute(val2 + '/counter', '-step', '04', '-start', '00000000A1', '-direction', 'increment')
ixNet.commit()

print('Changing Increment of TLV2 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:2', '-increment') + '/singleValue', '-value', '00000001')
ixNet.commit()

print('Changing TLV3 name in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute((ldp1 + '/ldpLeafRangeV4/ldpTLVList:3'), '-name', 'LDP Opaque TLV 3')
ixNet.commit()

print('Activating TLV3 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:3', '-active') + '/singleValue', '-value', 'true')
ixNet.commit()

print('Changing Type of TLV3 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:3', '-type') + '/singleValue', '-value', '1')
ixNet.commit()

print('Changing Length of TLV3 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:3', '-tlvLength') + '/singleValue', '-value', '4')
ixNet.commit()

print('Changing Value of TLV3 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:3', '-value') + '/singleValue', '-value', '00000001')
ixNet.commit()

print('Changing Increment of TLV3 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp1 + '/ldpLeafRangeV4/ldpTLVList:3', '-increment') + '/singleValue', '-value', '00000001')
ixNet.commit()

print('Configuring mLDP Leaf range in Receiver LDP router')
print('Activating mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4', '-active') + '/singleValue', '-value', 'true')
ixNet.commit()

print('Changing Continuous Increment Opaque Value Across Root in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4', '-continuousIncrementOVAcrossRoot') + '/singleValue', '-value', 'true')
ixNet.commit()

print('Changing Label Value Step in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4', '-labelValueStep') + '/singleValue', '-value', '1')
ixNet.commit()

print('Changing Label Value Start in mLDP Leaf range in Receiver LDP router')
start2 = ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4', '-labelValueStart')

ixNet.setMultiAttribute(start2, '-pattern', 'counter', '-clearOverlays', 'False')
ixNet.commit()
ixNet.setMultiAttribute(start2 + '/counter', '-step', '100', '-start', '8916', '-direction', 'increment')
ixNet.commit()

print('Changing LSP count per root in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4', '-lspCountPerRoot') + '/singleValue', '-value', '6')
ixNet.commit()

print('Changing Root Address Step in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4', '-rootAddressStep') + '/singleValue', '-value', '0.0.0.1')
ixNet.commit()

print('Changing Root Address count in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4', '-rootAddressCount') + '/singleValue', '-value', '1')
ixNet.commit()

print('Changing Root Address in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4', '-rootAddress') + '/singleValue', '-value', '8.8.8.7')
ixNet.commit()

print('Changing TLV1 name in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute((ldp2 + '/ldpLeafRangeV4/ldpTLVList:1'), '-name', 'LDP Opaque TLV 4')
ixNet.commit()

print('Activating TLV1 in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:1', '-active') + '/singleValue', '-value', 'true')
ixNet.commit()

print('Changing Type of TLV1 in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:1', '-type') + '/singleValue', '-value', '111')
ixNet.commit()

print('Changing Length of TLV1 in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:1', '-tlvLength') + '/singleValue', '-value', '33')
ixNet.commit()

print('Changing Value of TLV1 in mLDP Leaf range in Receiver LDP router')
val4 = ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:1', '-value')
ixNet.setMultiAttribute(val4, '-pattern', 'counter', '-clearOverlays', 'False')
ixNet.commit()
ixNet.setMultiAttribute(val4 + '/counter', '-step', '04', '-start', '000000000000000000000000000000000000000000000000000000000000007651', '-direction', 'increment')
ixNet.commit()

print('Changing Increment of TLV1 in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:1', '-increment') + '/singleValue', '-value', '000000000000000000000000000000000000000000000000000000000000000001')
ixNet.commit()

print('Changing TLV2 name in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute((ldp2 + '/ldpLeafRangeV4/ldpTLVList:1'), '-name', 'LDP Opaque TLV 5')
ixNet.commit()

print('Activating TLV2 in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:2', '-active') + '/singleValue', '-value', 'true')
ixNet.commit()

print('Changing Type of TLV2 in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:2', '-type') + '/singleValue', '-value', '123')
ixNet.commit()

print('Changing Length of TLV2 in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:2', '-tlvLength') + '/singleValue', '-value', '5')
ixNet.commit()

print('Changing Value of TLV2 in mLDP Leaf range in Receiver LDP router')
val4 = ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:2', '-value')
ixNet.setMultiAttribute(val4, '-pattern', 'counter', '-clearOverlays', 'False')
ixNet.commit()
ixNet.setMultiAttribute(val4 + '/counter', '-step', '04', '-start', '00000000A1', '-direction', 'increment')
ixNet.commit()

print('Changing Increment of TLV2 in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:2', '-increment') + '/singleValue', '-value', '00000001')
ixNet.commit()

print('Changing TLV3 name in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute((ldp2 + '/ldpLeafRangeV4/ldpTLVList:3'), '-name', 'LDP Opaque TLV 6')
ixNet.commit()

print('Activating TLV3 in mLDP Leaf range in Receiver LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:3', '-active') + '/singleValue', '-value', 'true')
ixNet.commit()

print('Changing Type of TLV3 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:3', '-type') + '/singleValue', '-value', '1')
ixNet.commit()

print('Changing Length of TLV3 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:3', '-tlvLength') + '/singleValue', '-value', '4')
ixNet.commit()

print('Changing Value of TLV3 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:3', '-value') + '/singleValue', '-value', '00000001')
ixNet.commit()

print('Changing Increment of TLV3 in mLDP Leaf range in Sender LDP router')
ixNet.setMultiAttribute(ixNet.getAttribute(ldp2 + '/ldpLeafRangeV4/ldpTLVList:3', '-increment') + '/singleValue', '-value', '00000001')
ixNet.commit()

print ('Adding Network Topology behind Ethernet for Sender P router')
ixNet.execute('createDefaultStack', t1dev1, 'networkTopology')
n1 = ixNet.getList(t1dev1, 'networkGroup')[0]
netTopo1 = ixNet.getList(n1, 'networkTopology')[0]
ixNet.setAttribute(n1, '-name', 'Simulated Topology for Sender PE Address')

print ('Enabling Traffic Engineering behind mVRF for Sender P router')
ospfPseudoInterface1 = ixNet.getList(netTopo1 + '/simInterface:1/simInterfaceIPv4Config:1', 'ospfPseudoInterface')[0]
ospfPseudoInterface_teEnable1 = ixNet.getAttribute(ospfPseudoInterface1, '-enable')
ixNet.setMultiAttribute(ospfPseudoInterface_teEnable1 +'/singleValue', '-value','true')
ixNet.commit()

print ('Adding Network Topology behind Ethernet for Receiver P router')
ixNet.execute('createDefaultStack', t2dev1, 'networkTopology')
n2 = ixNet.getList(t2dev1, 'networkGroup')[0]
netTopo2 = ixNet.getList(n2, 'networkTopology')[0]
ixNet.setAttribute(n2, '-name', 'Simulated Topology for Receiver PE Address')

print ('Enabling Traffic Engineering behind mVRF for Receiver P router')
ospfPseudoInterface2 = ixNet.getList(netTopo2 + '/simInterface:1/simInterfaceIPv4Config:1', 'ospfPseudoInterface')[0]
ospfPseudoInterface_teEnable2 = ixNet.getAttribute(ospfPseudoInterface2, '-enable')
ixNet.setMultiAttribute(ospfPseudoInterface_teEnable2 +'/singleValue', '-value', 'true')
ixNet.commit()

print("Add IPv4 Loopback for PE")
ixNet.add(t1dev1, 'ipv4Loopback')
ixNet.add(t2dev1, 'ipv4Loopback')

ixNet.commit()
loopback1 = ixNet.getList(t1dev1, 'ipv4Loopback')[0]
loopback2 = ixNet.getList(t2dev1, 'ipv4Loopback')[0]

print('Changing the IPv4 Loopback name and address in Sender P router')
ixNet.setMultiAttribute(loopback1, '-name', 'IPv4 Loopback 1')
ixNet.commit()

ixNet.setMultiAttribute(ixNet.getAttribute(loopback1, '-address') + '/counter', '-start', '8.8.8.7', '-direction', 'increment')
ixNet.commit()

print('Changing the IPv4 Loopback name and address in Receiver P router')
ixNet.setMultiAttribute(loopback2, '-name', 'IPv4 Loopback 2')
ixNet.commit()
ixNet.setMultiAttribute(ixNet.getAttribute(loopback2, '-address') + '/counter', '-step', '0.0.0.1', '-start', '7.7.7.7', '-direction', 'increment')
ixNet.commit()

print ('Adding BGP over IPv4Loopback')

ixNet.add(loopback1, 'bgpIpv4Peer')
ixNet.add(loopback2, 'bgpIpv4Peer')
ixNet.commit()

bgp1 = ixNet.getList(loopback1, 'bgpIpv4Peer')[0]
bgp2 = ixNet.getList(loopback2, 'bgpIpv4Peer')[0]

print ('Setting IPs in BGP DUT IP tab')

dutIp1 = ixNet.getAttribute(bgp1, '-dutIp')
ixNet.setMultiAttribute(dutIp1, '-pattern', 'counter', '-clearOverlays', 'False')
ixNet.setMultiAttribute(dutIp1 + '/counter', '-step', '0.0.0.1', '-start', '7.7.7.7', '-direction', 'increment')
ixNet.commit()

dutIp2 = ixNet.getAttribute(bgp2, '-dutIp')
ixNet.setMultiAttribute(dutIp2, '-pattern', 'counter', '-clearOverlays', 'False')
ixNet.setMultiAttribute(dutIp2 + '/counter', '-step', '0.0.0.1', '-start', '8.8.8.7', '-direction', 'increment')
ixNet.commit()

print ('Enabling MVPN Capabilities for BGP Router')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-capabilityIpV4MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-capabilityIpV4Multicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-capabilityIpV4Multicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-capabilityIpV4Multicast') + '/singleValue', '-value', 'true')

ixNet.setAttribute(ixNet.getAttribute(bgp1, '-capabilityIpV6MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-capabilityIpV6Multicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-capabilityIpV6MulticastVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-ipv6MulticastBgpMplsVpn') + '/singleValue', '-value', 'true')


ixNet.setAttribute(ixNet.getAttribute(bgp2, '-capabilityIpV4MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-capabilityIpV4Multicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-capabilityIpV4Multicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-capabilityIpV4Multicast') + '/singleValue', '-value', 'true')

ixNet.setAttribute(ixNet.getAttribute(bgp2, '-capabilityIpV6MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-capabilityIpV6Multicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-capabilityIpV6MulticastVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-ipv6MulticastBgpMplsVpn') + '/singleValue', '-value', 'true')
ixNet.commit()

print ('Enabling MVPN Learned Information for BGP Router')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-filterIpV4Unicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-filterIpV4MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-filterIpv4MulticastBgpMplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-filterIpV4MulticastVpn') + '/singleValue', '-value', 'true')

ixNet.setAttribute(ixNet.getAttribute(bgp1, '-filterIpV6Unicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-filterIpV6MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-filterIpv6MulticastBgpMplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-filterIpV6MulticastVpn') + '/singleValue', '-value', 'true')


ixNet.setAttribute(ixNet.getAttribute(bgp2, '-filterIpV4Unicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-filterIpV4MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-filterIpv4MulticastBgpMplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-filterIpV4MulticastVpn') + '/singleValue', '-value', 'true')

ixNet.setAttribute(ixNet.getAttribute(bgp2, '-filterIpV6Unicast') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-filterIpV6MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-filterIpv6MulticastBgpMplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-filterIpV6MulticastVpn') + '/singleValue', '-value', 'true')
ixNet.commit()

print ('Adding mVRF over BGP in both topology')

ixNet.add(bgp1, 'bgpIpv4MVrf')
ixNet.add(bgp2, 'bgpIpv4MVrf')

ixNet.commit()

mVRF1 = ixNet.getList(bgp1, 'bgpIpv4MVrf')[0]
mVRF2 = ixNet.getList(bgp2, 'bgpIpv4MVrf')[0]

print ('Configuring mLDP P2MP as the Tunnel Type in Sender P router')
ixNet.setAttribute(ixNet.getAttribute(mVRF1, '-multicastTunnelType') + '/singleValue', '-value', 'tunneltypemldpp2mp')
ixNet.commit()

print ('Configuring mLDP P2MP as the Tunnel Type in Receiver P router')
ixNet.setAttribute(ixNet.getAttribute(mVRF2, '-multicastTunnelType') + '/singleValue', '-value', 'tunneltypemldpp2mp')
ixNet.commit()

print ('Configuring Root Address in Topology 1')
ixNet.setAttribute(ixNet.getAttribute(mVRF1, '-rootAddress') + '/singleValue', '-value', '8.8.8.7')
ixNet.commit()

print ('Enabling  CheckBox for use of Up/DownStream Assigned Label for Ingress Topology')
ixNet.setAttribute(ixNet.getAttribute(mVRF1, '-useUpOrDownStreamAssigneLabel') + '/singleValue', '-value', 'True')
ixNet.commit()

print ('Assigning value for Up/DownStream Assigned Label for Ingress Topology')
ixNet.setMultiAttribute(ixNet.getAttribute(mVRF1, '-upOrDownStreamAssignedLabel') + '/counter', '-step', '1', '-start', '10001', '-direction', 'increment')
ixNet.commit()

print ('Configuring Root Address in Topology 2')
ixNet.setAttribute(ixNet.getAttribute(mVRF2, '-rootAddress') + '/singleValue', '-value', '7.7.7.7')
ixNet.commit()

print ('Enabling  CheckBox for use of Up/DownStream Assigned Label for Egress Topology')
ixNet.setAttribute(ixNet.getAttribute(mVRF2, '-useUpOrDownStreamAssigneLabel') + '/singleValue', '-value', 'True')
ixNet.commit()

print ('Assigning value for Up/DownStream Assigned Label for Egress Topology')
ixNet.setMultiAttribute(ixNet.getAttribute(mVRF2, '-upOrDownStreamAssignedLabel') + '/counter', '-step', '1', '-start', '3116', '-direction', 'increment')
ixNet.commit()

print ('Configuring Opaque TLV Type for I-PMSI in Sender mVRF')
ixNet.setAttribute(ixNet.getAttribute(mVRF1+ '/pnTLVList:1', '-type') + '/singleValue', '-value', '111')
ixNet.commit()

print ('Configuring Opaque TLV Length for I-PMSI in Sender mVRF')
ixNet.setAttribute(ixNet.getAttribute(mVRF1+ '/pnTLVList:1', '-tlvLength') + '/singleValue', '-value', '33')
ixNet.commit()


print ('Configuring Opaque TLV Value for I-PMSI in Sender mVRF')
ixNet.setMultiAttribute(ixNet.getAttribute(mVRF1+ '/pnTLVList:1', '-value'), '-clearOverlays', 'false')
ixNet.commit()
ixNet.setMultiAttribute(ixNet.getAttribute(mVRF1+ '/pnTLVList:1', '-value') + '/counter', '-step', '04', '-start', '000000000000000000000000000000000000000000000000000000000000007651', '-direction', 'increment')
ixNet.commit()

print ('Configuring Opaque TLV Increment for I-PMSI in Sender mVRF')
ixNet.setAttribute(ixNet.getAttribute(mVRF1+ '/pnTLVList:1', '-increment') + '/singleValue', '-value', '000000000000000000000000000000000000000000000000000000000000000001')
ixNet.commit()

print ('Configuring Opaque TLV Type for I-PMSI in Receiver mVRF')
ixNet.setAttribute(ixNet.getAttribute(mVRF2+ '/pnTLVList:1', '-type') + '/singleValue', '-value', '123')
ixNet.commit()

print ('Configuring Opaque TLV Length for I-PMSI in Receiver mVRF')
ixNet.setAttribute(ixNet.getAttribute(mVRF2+ '/pnTLVList:1', '-tlvLength') + '/singleValue', '-value', '5')
ixNet.commit()

print ('Configuring Opaque TLV Value for I-PMSI in Receiver mVRF')
ixNet.setMultiAttribute(ixNet.getAttribute(mVRF2+ '/pnTLVList:1', '-value'), '-clearOverlays', 'false')
ixNet.commit()
ixNet.setMultiAttribute(ixNet.getAttribute(mVRF2+ '/pnTLVList:1', '-value') + '/counter', '-step', '04', '-start', '00000000A1', '-direction', 'increment')
ixNet.commit()

print ('Configuring Opaque TLV Increment for I-PMSI in Receiver mVRF')
ixNet.setAttribute(ixNet.getAttribute(mVRF2+ '/pnTLVList:1', '-increment') + '/singleValue', '-value', '0000000001')
ixNet.commit()

print ('Adding Network Group behind mVRF for Ingress Topology')
ixNet.add(t1dev1, 'networkGroup')
ixNet.commit()
networkGroup1 = ixNet.getList(t1dev1, 'networkGroup')[1]
ixNet.setAttribute(networkGroup1, '-name', 'IPv4 Sender Site-IPv6 Receiver Site')
ixNet.commit()

print ('Adding Network Group behind mVRF for Egress Topology')
ixNet.add(t2dev1, 'networkGroup')
ixNet.commit()
networkGroup2 = ixNet.getList(t2dev1, 'networkGroup')[1]
ixNet.setAttribute(networkGroup2, '-name', 'IPv4 Receiver Site-IPv6 Sender Site')
ixNet.commit()

print ('Adding IPv4/IPv6 Prefix pools in Ingress Topology')
ixNet.add(networkGroup1, 'ipv4PrefixPools')
ixNet.commit()

ixNet.add(networkGroup1, 'ipv6PrefixPools')
ixNet.commit()

print ('Adding IPv4/IPv6 Prefix pools in Egress Topology')
ixNet.add(networkGroup2, 'ipv4PrefixPools')
ixNet.commit()

ixNet.add(networkGroup2, 'ipv6PrefixPools')
ixNet.commit()

print ('Configuring the addresses in IPv4/IPv6 Prefix pools in IPv4 Sender Site-IPv6 Receiver Site')
ipv4PrefixPools1 = ixNet.getList(networkGroup1, 'ipv4PrefixPools')[0]
ipv6PrefixPools1 = ixNet.getList(networkGroup1, 'ipv6PrefixPools')[0]

print ('Changing Address for IPv4 Address Pool in Sender Site')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4PrefixPools1, '-networkAddress') + '/counter', '-step', '0.1.0.0', '-start', '200.1.0.1', '-direction', 'increment')
ixNet.commit()

print ('Changing Prefix Length for IPv4 Address Pool in Sender Site')
mulValPrefLen = ixNet.getAttribute(ipv4PrefixPools1, '-prefixLength')
ixNet.setMultiAttribute(mulValPrefLen + '/singleValue', '-value', '32')
ixNet.commit()

print ('Changing Address Count for IPv4 Address Pool in Sender Site')
ixNet.setAttribute(ipv4PrefixPools1, '-numberOfAddresses', '3')
ixNet.commit()

print ('Changing Address for IPv6 Address Pool in Sender Site')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv6PrefixPools1, '-networkAddress') + '/counter', '-step', '0:0:1:0:0:0:0:0', '-start', '5001:1:0:0:0:0:0:1', '-direction', 'increment')
ixNet.commit()

print ('Changing Prefix Length for IPv6 Address Pool in Sender Site')
mulValPrefLen = ixNet.getAttribute(ipv6PrefixPools1, '-prefixLength')
ixNet.setMultiAttribute(mulValPrefLen + '/singleValue', '-value', '128')
ixNet.commit()

print ('Changing Address Count Address Pool in Sender Site')
ixNet.setAttribute(ipv6PrefixPools1, '-numberOfAddresses', '5')
ixNet.commit()

print ('Changing label value for IPv4/IPv6 in IPv4 Sender Site-IPv6 Receiver Site')
bgpL3VpnRouteProperty1 = ixNet.getList(ipv4PrefixPools1, 'bgpL3VpnRouteProperty')[0]
bgp6L3VpnRouteProperty1 = ixNet.getList(ipv6PrefixPools1, 'bgpV6L3VpnRouteProperty')[0]

ixNet.setMultiAttribute(ixNet.getAttribute(bgpL3VpnRouteProperty1, '-labelStart') + '/counter', '-step', '10', '-start', '97710', '-direction', 'increment')
ixNet.commit()

ixNet.setMultiAttribute(ixNet.getAttribute(bgp6L3VpnRouteProperty1, '-labelStart') + '/counter', '-step', '10', '-start', '55410', '-direction', 'increment')
ixNet.commit()

print ('Disabling Receiver site and enabling Sender Site for IPv4 in Ingress Topology')
ixNet.setAttribute(bgpL3VpnRouteProperty1, '-enableIpv4Sender', 'True')
ixNet.setAttribute(bgpL3VpnRouteProperty1, '-enableIpv4Receiver', 'False')
ixNet.commit()

print ('Disabling Sender site and enabling Receiver Site for IPv6 in Ingress Topology')

ixNet.setAttribute(bgp6L3VpnRouteProperty1, '-enableIpv6Sender', 'False')
ixNet.setAttribute(bgp6L3VpnRouteProperty1, '-enableIpv6Receiver', 'True')
ixNet.commit()

print ('Configuring the addresses in IPv4/IPv6 Prefix pools in IPv4 Receiver Site-IPv6 Sender Site')
ipv4PrefixPools2 = ixNet.getList(networkGroup2, 'ipv4PrefixPools')[0]
ipv6PrefixPools2 = ixNet.getList(networkGroup2, 'ipv6PrefixPools')[0]

nwAdd2 = ixNet.getAttribute(ipv4PrefixPools2, '-networkAddress')
ixNet.setMultiAttribute(nwAdd2 + '/counter', '-step', '0.1.0.0', '-start', '202.0.0.1', '-direction', 'increment')
ixNet.commit()

nwAdd21 = ixNet.getAttribute(ipv6PrefixPools2, '-networkAddress')
ixNet.setMultiAttribute(nwAdd21 + '/counter', '-step', '0:0:1:0:0:0:0:0', '-start', '3001:1:0:0:0:0:0:1', '-direction', 'increment')
ixNet.commit()

ixNet.setAttribute(ixNet.getAttribute(ipv4PrefixPools2, '-prefixLength') + '/singleValue', '-value', '32')
ixNet.commit()

ixNet.setAttribute(ixNet.getAttribute(ipv6PrefixPools2, '-prefixLength') + '/singleValue', '-value', '128')
ixNet.commit()

print ('Changing label value for IPv4/IPv6 in IPv4 Receiver Site-IPv6 Sender Site')
bgpL3VpnRouteProperty2 = ixNet.getList(ipv4PrefixPools2, 'bgpL3VpnRouteProperty')[0]
bgp6L3VpnRouteProperty2 = ixNet.getList(ipv6PrefixPools2, 'bgpV6L3VpnRouteProperty')[0]

ixNet.setMultiAttribute(ixNet.getAttribute(bgpL3VpnRouteProperty2, '-labelStart') + '/counter', '-step', '10', '-start', '87710', '-direction', 'increment')
ixNet.commit()
ixNet.setMultiAttribute(ixNet.getAttribute(bgp6L3VpnRouteProperty2, '-labelStart') + '/counter', '-step', '10', '-start', '2765', '-direction', 'increment')
ixNet.commit()

print ('Disabling Sender site and enabling Receiver Site for both IPv4 in Egress topology')
ixNet.setAttribute(bgpL3VpnRouteProperty2, '-enableIpv4Sender', 'False')
ixNet.setAttribute(bgpL3VpnRouteProperty2, '-enableIpv4Receiver', 'True')
ixNet.commit()

print ('Disabling Receiver site and enabling Sender Site for IPv6 in Egress Topology')

ixNet.setAttribute(bgp6L3VpnRouteProperty2, '-enableIpv6Sender', 'True')
ixNet.setAttribute(bgp6L3VpnRouteProperty2, '-enableIpv6Receiver', 'False')
ixNet.commit()

bgpMVpnSenderSitesIpv4 = ixNet.getList(ipv4PrefixPools1, 'bgpMVpnSenderSitesIpv4')[0]
bgpMVpnSenderSitesIpv6 = ixNet.getList(ipv6PrefixPools2, 'bgpMVpnSenderSitesIpv6')[0]
bgpMVpnReceiverSitesIpv4 = ixNet.getList(ipv4PrefixPools2, 'bgpMVpnReceiverSitesIpv4')[0]
bgpMVpnReceiverSitesIpv6 = ixNet.getList(ipv6PrefixPools1, 'bgpMVpnReceiverSitesIpv6')[0]

print ('Changing Group Address Count for IPv4 Cloud in Sender Site')
mulValGCount = ixNet.getAttribute(bgpMVpnSenderSitesIpv4, '-groupAddressCount')
ixNet.setMultiAttribute(mulValGCount + '/singleValue', '-value', '4')
ixNet.commit()

print ('Changing Source Address Count for IPv4 Cloud in Sender Site')
mulValSCount = ixNet.getAttribute(bgpMVpnSenderSitesIpv4, '-sourceAddressCount')
ixNet.setMultiAttribute(mulValSCount + '/singleValue', '-value', '2')
ixNet.commit()

print ('Changing Group Address for IPv4 Cloud in Sender Site')
mulValGAdd = ixNet.getAttribute(bgpMVpnSenderSitesIpv4, '-startGroupAddressIpv4')
ixNet.setMultiAttribute(mulValGAdd + '/counter', '-step', '0.1.0.0', '-start', '234.161.1.1')
ixNet.commit()

print ('Changing Source Address for IPv4 Cloud in Sender Site')
mulValSAdd = ixNet.getAttribute(bgpMVpnSenderSitesIpv4, '-startSourceAddressIpv4')
ixNet.setMultiAttribute(mulValSAdd + '/counter', '-step', '0.1.0.0', '-start', '200.1.0.1')
ixNet.commit()

print ('Changing Group Address Count for IPv4 Cloud in Receiver Site')
mulValGCount = ixNet.getAttribute(bgpMVpnReceiverSitesIpv4, '-groupAddressCount')
ixNet.setMultiAttribute(mulValGCount + '/singleValue', '-value', '4')
ixNet.commit()

print ('Changing Source Address Count for IPv4 Cloud in Receiver Site')
mulValSCount = ixNet.getAttribute(bgpMVpnReceiverSitesIpv4, '-sourceAddressCount')
ixNet.setMultiAttribute(mulValSCount + '/singleValue', '-value', '2')
ixNet.commit()

print ('Changing Group Address for IPv4 Cloud in Receiver Site')
mulValGAdd = ixNet.getAttribute(bgpMVpnReceiverSitesIpv4, '-startGroupAddressIpv4')
ixNet.setMultiAttribute(mulValGAdd + '/counter', '-step', '0.1.0.0', '-start', '234.161.1.1')
ixNet.commit()

print ('Changing Source Address for IPv4 Cloud in Receiver Site')
mulValSAdd = ixNet.getAttribute(bgpMVpnReceiverSitesIpv4, '-startSourceOrCrpAddressIpv4')
ixNet.setMultiAttribute(mulValSAdd + '/counter', '-step', '0.1.0.0', '-start', '200.1.0.1')
ixNet.commit()

print ('Changing C-Multicast Route Type for IPv4 Cloud in Receiver Site')
mulValCMRType = ixNet.getAttribute(bgpMVpnReceiverSitesIpv4, '-cMulticastRouteType')
ixNet.setMultiAttribute(mulValCMRType + '/singleValue', '-value', 'sharedtreejoin')
ixNet.commit()

print ('Changing Group Address Count for IPv6 Cloud in Sender Site')
mulValGCount = ixNet.getAttribute(bgpMVpnSenderSitesIpv6, '-groupAddressCount')
ixNet.setMultiAttribute(mulValGCount + '/singleValue', '-value', '5')
ixNet.commit()

print ('Changing Source Group Mapping for IPv6 Cloud in Sender Site')
mulValSGMap = ixNet.getAttribute(bgpMVpnSenderSitesIpv6, '-sourceGroupMapping')
ixNet.setMultiAttribute(mulValSGMap + '/singleValue', '-value', 'onetoone')
ixNet.commit()

print ('Changing Group Address for IPv6 Cloud in Sender Site')
mulValGAdd = ixNet.getAttribute(bgpMVpnSenderSitesIpv6, '-startGroupAddressIpv6')
ixNet.setMultiAttribute(mulValGAdd + '/counter', '-step', '0:0:0:0:0:0:0:1', '-start', 'ff15:1:0:0:0:0:0:1', '-direction', 'increment')
ixNet.commit()

print ('Changing Source Address for IPv6 Cloud in Sender Site')
mulValSAdd = ixNet.getAttribute(bgpMVpnSenderSitesIpv6, '-startSourceAddressIpv6')
ixNet.setMultiAttribute(mulValSAdd + '/counter', '-step', '0:0:1:0:0:0:0:0', '-start', '3000:1:0:0:0:0:0:1', '-direction', 'increment')
ixNet.commit()

print ('Changing Group Address Count for IPv6 Cloud in Receiver Site')
mulValGCount = ixNet.getAttribute(bgpMVpnReceiverSitesIpv6, '-groupAddressCount')
ixNet.setMultiAttribute(mulValGCount + '/singleValue', '-value', '5')
ixNet.commit()

print ('Changing source Group Mapping for IPv6 Cloud in Receiver Site')
mulValSGMap = ixNet.getAttribute(bgpMVpnReceiverSitesIpv6, '-sourceGroupMapping')
ixNet.setMultiAttribute(mulValSGMap + '/singleValue', '-value', 'onetoone')
ixNet.commit()

print ('Changing Group Address for IPv6 Cloud in Receiver Site')
mulValGAdd = ixNet.getAttribute(bgpMVpnReceiverSitesIpv6, '-startGroupAddressIpv6')
ixNet.setMultiAttribute(mulValGAdd + '/counter', '-step', '::0:0:0:1', '-start', 'ff15:1:0:0:0:0:0:1', '-direction', 'increment')
ixNet.commit()

print ('Changing Source Address for IPv6 Cloud in Receiver Site')
mulValSAdd = ixNet.getAttribute(bgpMVpnReceiverSitesIpv6, '-startSourceAddressIpv6')
ixNet.setMultiAttribute(mulValSAdd + '/counter', '-step', '0:0:1::', '-start', '3000:1:1:1:0:0:0:0', '-direction', 'increment')
ixNet.commit()

print ('Changing Tunnel Type to mLDP for S-PMSI in IPv4 Address Pool in Sender Site')
bgpMVpnSenderSiteSpmsiV4 = ixNet.getList(bgpMVpnSenderSitesIpv4, 'bgpMVpnSenderSiteSpmsiV4')[0]
mulValsPMSITunType = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-multicastTunnelType')
ixNet.setMultiAttribute(mulValsPMSITunType + '/singleValue', '-value', 'tunneltypemldpp2mp')
ixNet.commit()

print ('Enabling Use Upstream/Downstream Assigned Label for S-PMSI in IPv4 Address Pool in Sender Sites')
mulValUpAsLabEn = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-useUpstreamOrDownstreamAssignedLabel')
ixNet.setMultiAttribute(mulValUpAsLabEn + '/singleValue', '-value', 'true')
ixNet.commit()

print ('Configuring the Upstream/Downstream Assigned Label for S-PMSI in IPv4 Address Pool in Sender Sites')
mulValUpAsLabel = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-upstreamOrDownstreamAssignedLabel')
ixNet.setMultiAttribute(mulValUpAsLabel +'/counter', '-step', '10', '-start', '144', '-direction', 'increment')
ixNet.commit()

print ('Configuring Root Address for S-PMSI in IPv4 Address Pool in Sender Sites')
mulValRootAdd = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-sPmsirootAddress')
ixNet.setMultiAttribute(mulValRootAdd + '/counter', '-step', '0.0.0.1', '-start', '8.8.8.7', '-direction', 'increment')
ixNet.commit()

print ('Changing Tunnel Count for S-PMSI in IPv4 Address Pool in Sender Site')
mulValsPMSITunCnt = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4, '-sPmsiTunnelCount')
ixNet.setMultiAttribute(mulValsPMSITunCnt + '/singleValue', '-value', '3')
ixNet.commit()

print('Changing Type of TLV1 in S-PMSI mLDP Leaf range in IpV4 Sender Site')
type_s1 = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4 + '/pnTLVList:1', '-type')
ixNet.setMultiAttribute(type_s1 + '/singleValue', '-value', '111')
ixNet.commit()

print('Changing Length of TLV1 in S-PMSI mLDP Leaf range in IpV4 Sender Site')
len_s1 = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4 + '/pnTLVList:1', '-tlvLength')
ixNet.setMultiAttribute(len_s1 + '/singleValue', '-value', '33')
ixNet.commit()

print('Changing Value of TLV1 in S-PMSI mLDP Leaf range in IpV4 Sender Site')
val_s1 = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4 + '/pnTLVList:1', '-value')
ixNet.setMultiAttribute(val_s1 + '/counter', '-step', '04', '-start', '000000000000000000000000000000000000000000000000000000000000007653', '-direction', 'increment')
ixNet.commit()

print('Changing Increment of TLV1 in S-PMSI mLDP Leaf range in IpV4 Sender Site')
inc_s1 = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV4 + '/pnTLVList:1', '-increment')
ixNet.setMultiAttribute(inc_s1 + '/singleValue', '-value', '000000000000000000000000000000000000000000000000000000000000000001')
ixNet.commit()

bgpMVpnSenderSiteSpmsiV6 = ixNet.getList(bgpMVpnSenderSitesIpv6, 'bgpMVpnSenderSiteSpmsiV6')[0]

print ('Changing Tunnel Type to mLDP for S-PMSI in IPv6 Address Pool in Sender Site')
mulValsPMSIv6TunType = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV6, '-multicastTunnelType')
ixNet.setMultiAttribute(mulValsPMSIv6TunType + '/singleValue', '-value', 'tunneltypemldpp2mp')
ixNet.commit()

print ('Configuring Root Address for S-PMSI in IPv6 Address Pool in Sender Sites')
mulValRootAddv6 = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV6, '-sPmsirootAddress')
ixNet.setMultiAttribute(mulValRootAddv6 + '/counter', '-step', '0.0.0.1', '-start', '7.7.7.7', '-direction', 'increment')
ixNet.commit()

print ('Enabling Use Upstream/Downstream Assigned Label for S-PMSI in IPv6 Address Pool in Sender Sites')
mulValUpAsLabEn_S = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV6, '-useUpstreamOrDownstreamAssignedLabel')
ixNet.setMultiAttribute(mulValUpAsLabEn_S + '/singleValue', '-value', 'true')
ixNet.commit()

print ('Configuring the Upstream/Downstream Assigned Label for S-PMSI in IPv6 Address Pool in Sender Sites')
mulValUpAsLabel_S = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV6, '-upstreamOrDownstreamAssignedLabel')
ixNet.setMultiAttribute(mulValUpAsLabel_S +'/counter', '-step', '10', '-start', '14400', '-direction', 'increment')
ixNet.commit()

print ('Changing Tunnel Count for S-PMSI in IPv6 Address Pool in Sender Site')
mulValsPMSITunCntv6 = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV6, '-sPmsiTunnelCount')
ixNet.setMultiAttribute(mulValsPMSITunCntv6 + '/singleValue', '-value', '3')
ixNet.commit()


print('Changing Type of TLV1 in S-PMSI mLDP Leaf range in IpV6 Sender Site')
type_s2 = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV6 + '/pnTLVList:1', '-type')
ixNet.setMultiAttribute(type_s2 + '/singleValue', '-value', '123')
ixNet.commit()

print('Changing Length of TLV1 in S-PMSI mLDP Leaf range in IpV6 Sender Site')
len_s2 = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV6 + '/pnTLVList:1', '-tlvLength')
ixNet.setMultiAttribute(len_s2 + '/singleValue', '-value', '5')
ixNet.commit()

print('Changing Value of TLV1 in S-PMSI mLDP Leaf range in IpV6 Sender Site')
val_s2 = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV6 + '/pnTLVList:1', '-value')
ixNet.setMultiAttribute(val_s2 + '/counter', '-step', '01', '-start', '00000000A3', '-direction', 'increment')
#ixNet.setMultiAttribute(val_s2 + '/singleValue', '-value', '00000000A4')
ixNet.commit()

print('Changing Increment of TLV1 in S-PMSI mLDP Leaf range in IpV6 Sender Site')
inc_s2 = ixNet.getAttribute(bgpMVpnSenderSiteSpmsiV6 + '/pnTLVList:1', '-increment')
ixNet.setMultiAttribute(inc_s2 + '/singleValue', '-value', '0000000001')
ixNet.commit()

################################################################################
# 2. Start protocols.
################################################################################
print ('Wait for 5 seconds before starting protocol')
time.sleep(5)
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)

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
###############################################################################
# 4. Retrieve IPv4/IPv6 mVPN learned info
###############################################################################
print ('Fetching IPv4 mVPN Learned Info at Receiver side PE Router')
ixNet.execute('getIpv4MvpnLearnedInfo', bgp2, '1')
print(' %%%%%%%%%%%%%%%%% Learned Info fetched')
time.sleep(5)
print ('IPv4 MVPN Learned Info at Receiver PE Router')
linfo  = ixNet.getList(bgp2, 'learnedInfo')[0]

values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

print ('Fetching IPv6 mVPN Learned Info at Sender side PE Router')
ixNet.execute('getIpv6MvpnLearnedInfo', bgp1, '1')
print ('IPv6 MVPN Learned Info at Sender PE Router')
time.sleep(5)
linfo  = ixNet.getList(bgp1, 'learnedInfo')[0]

values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# 5. Apply changes on the fly.
################################################################################
print ('Changing Source Address Count for IPv6 Cloud in Receiver Site')
mulValSCount = ixNet.getAttribute(bgpMVpnReceiverSitesIpv6, '-sourceAddressCount')
ixNet.setMultiAttribute(mulValSCount + '/singleValue', '-value', '4')
ixNet.commit()

globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print ('error in applying on the fly change')
# end try/expectX
time.sleep(10)

################################################################################
# 6. S-PMSI Trigger
################################################################################
print ('Switching to S-PMSI for IPv4 Cloud from Sender Site')
try :
    ixNet.execute('switchToSpmsi', bgpMVpnSenderSitesIpv4, 1)
    ixNet.execute('switchToSpmsi', bgpMVpnSenderSitesIpv4, 2)
except :
    print ('error in S-PMSI Trigger')
# end try/expectX
time.sleep(10)

###############################################################################
# 7. Retrieve protocol learned info after OTF
###############################################################################

print ('Fetching IPv4 mVPN Learned Info')
ixNet.execute('getIpv4MvpnLearnedInfo', bgp2, '1')
print(' %%%%%%%%%%%%%%%%% Learned Info fetched')
time.sleep(5)
print ('Fetched Learned Info at Receiver side PE Router')
linfo  = ixNet.getList(bgp2, 'learnedInfo')[0]
print linfo
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# 8. Configure L2-L3 IPv6 I-PMSI traffic.
################################################################################
print ('Configuring L2-L3 IPv6 I-PMSI Traffic Item')
trafficItem1 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem1, '-name', 'NGMVPN I-PMSI Traffic 1',
    '-roundRobinPacketOrdering', 'false','-numVlansForMulticastReplication', '1', '-trafficType', 'ipv6', '-routeMesh', 'fullMesh')
ixNet.commit()

trafficItem1 = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')
destination  = ['bgpMVpnReceiverSitesIpv6']

ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
    '-sources',               bgpMVpnSenderSitesIpv6,
    '-multicastDestinations', [['false','none','ff15:1:0:0:0:0:0:1','0:0:0:0:0:0:0:1','5']])
ixNet.commit()

endpointSet1 = ixNet.remapIds(endpointSet1)[0]

ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'mplsFlowDescriptor0', 'trackingenabled0', 'mplsMplsLabelValue0', 'ipv6DestIp0', 'ipv6SourceIp0'])
ixNet.commit()

################################################################################
# 9. Configure L2-L3 IPv4 S-PMSI traffic.
################################################################################

print ('Configuring L2-L3 IPv4 S-PMSI Traffic Item')
trafficItem2 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem2, '-name', 'NGMVPN S-PMSI Traffic 2',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv4')
ixNet.commit()

trafficItem2 = ixNet.remapIds(trafficItem2)[0]
endpointSet2 = ixNet.add(trafficItem2, 'endpointSet')
destination  = ['bgpMVpnReceiverSitesIpv4']

ixNet.setMultiAttribute(endpointSet2,
    '-name',                  'EndpointSet-1',
    '-sources',               bgpMVpnSenderSiteSpmsiV4,
    '-multicastDestinations', [['false','none','234.161.1.1','0.0.0.1','4'],['false','none','234.162.1.1','0.0.0.1','4']])
ixNet.commit()

endpointSet2 = ixNet.remapIds(endpointSet2)[0]

ixNet.setMultiAttribute(trafficItem2 + '/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'ipv4DestIp0', 'ipv4SourceIp0', 'trackingenabled0', 'mplsFlowDescriptor0'])
ixNet.commit()

###############################################################################
# 10. Apply and start L2/L3 traffic.
###############################################################################
print ('applying L2/L3 traffic')
ixNet.execute('apply', ixNet.getRoot() + '/traffic')
time.sleep(5)
print ('starting L2/L3 traffic')
ixNet.execute('start', ixNet.getRoot() + '/traffic')
print ('let traffic run for 60 second')
time.sleep(60)

###############################################################################
# 11. Retrieve L2/L3 traffic item statistics.
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
# 12. Stop L2/L3 traffic.
#################################################################################
print ('Stopping L2/L3 traffic')
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)

################################################################################

# 13. Stop all protocols.
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
print ('!!! Test Script Ends !!!')
