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

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF MPLSOAM with RSCP-TE   #
#    using Python                                                              #
#    with FEC128.                                                              #
#                                                                              #
# About Topology:                                                              #
#                                                                              #
#     On each port, it will create one topology of MPLSOAM with LDPv4 FEC 128. #
#     In each topology, there will be two device groups and two network groups.#
#     First device group will simulate as a RSVP-TE basic P router and other as#
#     LDPv4 targeted PE router with pseudo wire FEC 128 is configured.         #
#     After first device group, there is one network group in which IPv4 prefix#
#     pools is configured. The other network group has mac pools which is      #
#     simulated as CE router and also is used as traffic end point.            #
#                                                                              #
# Script Flow:                                                                 #
#    1. Configuration of protocols as described in topology.                   #
#    2. Start the LDP protocol.                                                #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Change LDP PW/VPLS labels & apply change on the fly                    #
#    6. Retrieve protocol learned info again.                                  #
#    7. Configure L2-L3 traffic.                                               #
#    8. Start the L2-L3 traffic.                                               #
#   11. Retrieve L2-L3 traffic stats.                                          #
#   12. Stop L2-L3 traffic.                                                    #
#   13. Stop all protocols.                                                    #
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
ixNetPath = r'/home/lacp/regress-test/linux-run'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.216.108.103'
ixTclPort   = '8039'
ports       = [('10.216.100.12', '2', '11',), ('10.216.100.12', '2', '12',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.30', '-setAttribute', 'strict')
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

print ("Adding 2 device groups")
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


print("Adding rsvp-te over IP4 stacks")
ixNet.add(ip1, 'rsvpteIf')
ixNet.add(ip2, 'rsvpteIf')
ixNet.commit()

print("Adding ospfv2 over IP4 stacks")
ixNet.add(ip1, 'ospfv2')
ixNet.add(ip2, 'ospfv2')
ixNet.commit()

#remoteip1 = ixNet.getAttribute(rsvpig1, '-remoteIp')
#remoteip2 = ixNet.getAttribute(rsvpig2, '-remoteIp')


rsvpte1 = ixNet.getList(ip1, 'rsvpteIf')[0]
rsvpte2 = ixNet.getList(ip2, 'rsvpteIf')[0]

ospf1 = ixNet.getList(ip1, 'ospfv2')[0]
ospf2 = ixNet.getList(ip2, 'ospfv2')[0]

print ("Changing network type to point to point on ospfv2")
ixNet.setMultiAttribute(ixNet.getAttribute(ospf1, '-networkType') + '/singleValue', '-value', 'pointtopoint')
ixNet.setMultiAttribute(ixNet.getAttribute(ospf2, '-networkType') + '/singleValue', '-value', 'pointtopoint')
ixNet.commit()

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'RSVP-TE Topology')
ixNet.setAttribute(topo2, '-name', 'RSVP-TE Topology')

ixNet.setAttribute(t1dev1, '-name', 'P Router 1')
ixNet.setAttribute(t2dev1, '-name', 'P Router 2')
ixNet.commit()


print("Adding NetworkGroup behind RSVP-TE DG")

ixNet.add(t1dev1, 'networkGroup')
ixNet.add(t2dev1, 'networkGroup')
ixNet.commit()

networkGroup1 = ixNet.getList(t1dev1, 'networkGroup')[0]
networkGroup2 = ixNet.getList(t2dev1, 'networkGroup')[0]

ixNet.setAttribute(networkGroup1, '-name', 'RSVP-TE_1_Network_Group1')
ixNet.setAttribute(networkGroup2, '-name', 'RSVP-TE_2_Network_Group1')
ixNet.setAttribute(networkGroup1, '-multiplier', '1')
ixNet.setAttribute(networkGroup2, '-multiplier', '1')
ixNet.commit()

print("Adding IPv4 prefix pools in Network Groups")
ixNet.add(networkGroup1, 'ipv4PrefixPools')
ixNet.add(networkGroup2, 'ipv4PrefixPools')
ixNet.commit()

ipV4PrefixPools1 = ixNet.getList(networkGroup1, 'ipv4PrefixPools')[0]
ipV4PrefixPools2 = ixNet.getList(networkGroup2, 'ipv4PrefixPools')[0]


print("Configuring network address and prefic length of IPV4 prefix pools")
prefixLength1 = ixNet.getAttribute(ipV4PrefixPools1, '-prefixLength')
prefixLength2 = ixNet.getAttribute(ipV4PrefixPools2, '-prefixLength')
ixNet.setMultiAttribute(prefixLength1, '-clearOverlays',  'false', '-pattern', 'singleValue')
ixNet.setMultiAttribute(prefixLength2, '-clearOverlays',  'false', '-pattern', 'singleValue')
ixNet.commit()

singleValue1 = ixNet.add(prefixLength1, 'singleValue')
singleValue2 = ixNet.add(prefixLength2, 'singleValue')
ixNet.setMultiAttribute(singleValue1, '-value', '32')
ixNet.setMultiAttribute(singleValue2, '-value', '32')
ixNet.commit()

networkAddress1 = ixNet.getAttribute(ipV4PrefixPools1, '-networkAddress')
networkAddress2 = ixNet.getAttribute(ipV4PrefixPools2, '-networkAddress')
ixNet.setMultiAttribute(networkAddress1, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.setMultiAttribute(networkAddress2, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()

counter1 = ixNet.add(networkAddress1, 'counter')
counter2 = ixNet.add(networkAddress2, 'counter')
ixNet.setMultiAttribute(counter1, '-step', '0.0.0.1', '-start', '2.2.2.2', '-direction', 'increment')
ixNet.setMultiAttribute(counter2, '-step', '0.0.0.1', '-start', '1.1.1.1', '-direction', 'increment')
ixNet.commit()


print("Adding Device Group behind Network Groups")
ixNet.add(networkGroup1, 'deviceGroup')
ixNet.add(networkGroup2, 'deviceGroup')
ixNet.commit()

t1dev2 = ixNet.getList(networkGroup1, 'deviceGroup')[0]
t2dev2 = ixNet.getList(networkGroup2, 'deviceGroup')[0]

print("Configuring the multipliers")
ixNet.setAttribute(t1dev2, '-multiplier', '1')
ixNet.setAttribute(t2dev2, '-multiplier', '1')
ixNet.commit()

ixNet.setAttribute(t1dev2, '-name', 'PE Router 1')
ixNet.setAttribute(t2dev2, '-name', 'PE Router 2')
ixNet.commit()

print("Adding loopback in second device group of both topologies")
ixNet.add(t1dev2, 'ipv4Loopback')
ixNet.add(t2dev2, 'ipv4Loopback')
ixNet.commit()

ipv4Loopback1 = ixNet.getList(t1dev2, 'ipv4Loopback')[0]
ipv4Loopback2 = ixNet.getList(t2dev2, 'ipv4Loopback')[0]


print("Assigning ipv4 address on Loop Back Interface")
addressSet1 = ixNet.getAttribute(ipv4Loopback1, '-address')
ixNet.setMultiAttribute(addressSet1, '-clearOverlays', 'false', '-pattern', 'counter')
addressSet2 = ixNet.getAttribute(ipv4Loopback2, '-address')
ixNet.setMultiAttribute(addressSet2, '-clearOverlays', 'false', '-pattern', 'counter')

ixNet.commit()

counter1 = ixNet.add(addressSet1, 'counter')
counter2 = ixNet.add(addressSet2, 'counter')
ixNet.setMultiAttribute(counter1, '-step', '0.0.0.1', '-start', '2.2.2.2', '-direction', 'increment')
ixNet.setMultiAttribute(counter2, '-step', '0.0.0.1', '-start', '1.1.1.1', '-direction', 'increment')
ixNet.commit()

ixNet.add(ipv4Loopback1, 'rsvpteLsps')
ixNet.add(ipv4Loopback2, 'rsvpteLsps')
ixNet.commit()

print("Adding targeted RSVP-TE LSPs over these loopbacks")
rsvplsp1 = ixNet.getList(ipv4Loopback1, 'rsvpteLsps')[0]
rsvplsp2 = ixNet.getList(ipv4Loopback2, 'rsvpteLsps')[0]

rsvpig1 = ixNet.getList(rsvplsp1, 'rsvpP2PIngressLsps')[0]
rsvpig2 = ixNet.getList(rsvplsp2, 'rsvpP2PIngressLsps')[0]

rsvpeg1 = ixNet.getList(rsvplsp1, 'rsvpP2PEgressLsps')[0]
rsvpeg2 = ixNet.getList(rsvplsp2, 'rsvpP2PEgressLsps')[0]


remoteip1 = ixNet.getAttribute(rsvpig1, '-remoteIp')
remoteip2 = ixNet.getAttribute(rsvpig2, '-remoteIp')


print ("Enabling LDP Router capabilities for mplsOam")
ixNet.setMultiAttribute(ixNet.getAttribute(rsvpig1, '-enableBfdMpls') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(rsvpig2, '-enableBfdMpls') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(rsvpig1, '-enableLspPing') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(rsvpig2, '-enableLspPing') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(rsvpeg1, '-enableReplyingLspPing') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(rsvpeg2, '-enableReplyingLspPing') + '/singleValue', '-value', 'true')

ixNet.setAttribute(remoteip1 + '/singleValue', '-value', '1.1.1.1')
ixNet.setAttribute(remoteip2 + '/singleValue', '-value', '2.2.2.2')

ixNet.commit()

print("Adding targeted LDPv4 router over these loopbacks")
ixNet.add(ipv4Loopback1, 'ldpTargetedRouter')
ixNet.add(ipv4Loopback2, 'ldpTargetedRouter')
ixNet.commit()

ldpTargetedRouterV41 = ixNet.getList(ipv4Loopback1, 'ldpTargetedRouter')[0]
ldpTargetedRouterV42 = ixNet.getList(ipv4Loopback2, 'ldpTargetedRouter')[0]

print("Configuring DUT IP in LDPv4 targeted peers")
iPAddress1 = ixNet.getAttribute(ldpTargetedRouterV41 + '/ldpTargetedPeer', '-iPAddress')
iPAddress2 = ixNet.getAttribute(ldpTargetedRouterV42 + '/ldpTargetedPeer', '-iPAddress')
ixNet.setMultiAttribute(iPAddress1, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.setMultiAttribute(iPAddress2, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()

counter1 = ixNet.add(iPAddress1, 'counter')
counter2 = ixNet.add(iPAddress2, 'counter')
ixNet.setMultiAttribute(counter1, '-step', '0.0.0.1', '-start', '1.1.1.1', '-direction', 'increment')
ixNet.setMultiAttribute(counter2, '-step', '0.0.0.1', '-start', '2.2.2.2', '-direction', 'increment')
ixNet.commit()


print("Adding mplsoam on the loopback interface of both topologies")
ixNet.add(ipv4Loopback1, 'mplsOam')
ixNet.add(ipv4Loopback2, 'mplsOam')
ixNet.commit()

mplsoam1 = ixNet.getList(ipv4Loopback1, 'mplsOam')[0]
mplsoam2 = ixNet.getList(ipv4Loopback2, 'mplsOam')[0]

print ("Enabling periodic ping on mplsOam")
ixNet.setMultiAttribute(ixNet.getAttribute(mplsoam1, '-enablePeriodicPing') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(mplsoam2, '-enablePeriodicPing') + '/singleValue', '-value', 'true')
ixNet.commit()

print ("Changing reply mode to 2")
ixNet.setMultiAttribute(ixNet.getAttribute(mplsoam1, '-replyMode') + '/singleValue', '-value', 'replyviaipv4ipv6udppacket')
ixNet.setMultiAttribute(ixNet.getAttribute(mplsoam2, '-replyMode') + '/singleValue', '-value', 'replyviaipv4ipv6udppacket')
ixNet.commit()

print ("Changing echo request interval to 5sec")
ixNet.setMultiAttribute(ixNet.getAttribute(mplsoam1, '-echoRequestInterval') + '/singleValue', '-value', '5000')
ixNet.setMultiAttribute(ixNet.getAttribute(mplsoam2, '-echoRequestInterval') + '/singleValue', '-value', '5000')
ixNet.commit()


remoteip1 = ixNet.getAttribute(rsvpig1, '-remoteIp')
remoteip2 = ixNet.getAttribute(rsvpig2, '-remoteIp')

print("Adding LDP PW/VPLS over these targeted routers")
ixNet.add(ldpTargetedRouterV41, 'ldppwvpls')
ixNet.add(ldpTargetedRouterV42, 'ldppwvpls')
ixNet.commit()

ldppwvpls1 = ixNet.getList(ldpTargetedRouterV41, 'ldppwvpls')[0]
ldppwvpls2 = ixNet.getList(ldpTargetedRouterV42, 'ldppwvpls')[0]

ixNet.commit()

print("Enabling C-Bit in LDP PW/VPLS")
ixNet.setMultiAttribute(ixNet.getAttribute(ldppwvpls1, '-cBitEnabled') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ldppwvpls2, '-cBitEnabled') + '/singleValue', '-value', 'true')
ixNet.commit()
ixNet.commit()

print("Enabling cv negotiation in LDP PW/VPLS")
ixNet.setMultiAttribute(ixNet.getAttribute(ldppwvpls1, '-enableCCCVNegotiation') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ldppwvpls2, '-enableCCCVNegotiation') + '/singleValue', '-value', 'true')
ixNet.commit()
ixNet.commit()

ixNet.commit()
print("Enabling Auto Peer Address in LDP PW/VPLS")
ixNet.setAttribute(ldppwvpls1, '-autoPeerId', 'true')
ixNet.setAttribute(ldppwvpls2, '-autoPeerId', 'true')
ixNet.commit()



print("Adding Network Group behind each PE routers")
ixNet.add(t1dev2, 'networkGroup')
ixNet.add(t2dev2, 'networkGroup')
ixNet.commit()

networkGroup3 = ixNet.getList(t1dev2, 'networkGroup')[0]
networkGroup4 = ixNet.getList(t2dev2, 'networkGroup')[0]

ixNet.setAttribute(networkGroup3, '-name', 'MAC_POOL_1')
ixNet.setAttribute(networkGroup4, '-name', 'MAC_POOL_2')
ixNet.commit()

print("Adding MAC pools in Network Groups")
ixNet.add(networkGroup3, 'macPools')
ixNet.add(networkGroup4, 'macPools')
ixNet.commit()

macPools1 = ixNet.getList(networkGroup3, 'macPools')
macPools2 = ixNet.getList(networkGroup4, 'macPools')

print("All configuration is completed..Wait for 5 seconds...")
time.sleep(5)

print("Enabling transport labels on ldp interface")
root = ixNet.getRoot()
globalsV = ixNet.getList(root, 'globals')[0]
globalTopo = ixNet.getList(globalsV, 'topology')[0]
globalLdp = ixNet.getList(globalTopo, 'ldpBasicRouter')[0]
ixNet.setMultiAttribute(ixNet.getAttribute(globalLdp, '-transportLabels') + '/singleValue', '-value', 'true')
ixNet.commit()


################################################################################
# 2. Start all protocols and wait for 120 seconds
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(120)

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
print ("Fetching all Protocol Summary Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"MPLSOAM IF Per Port"/page'
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
print("Fetching mplsoam Basic Learned Info")
ixNet.execute('getAllLearnedInfo', mplsoam1, '1')
time.sleep(5)
linfo  = ixNet.getList(mplsoam1, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")


################################################################################
# 5.Change the LDP PW/VPLS labels And apply changes On The Fly (OTF).
################################################################################
print("Changing labels of LDPv4 PW/VPLS Range")
label2 = ixNet.getAttribute(ldppwvpls2, '-label')
ixNet.setMultiAttribute(label2, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()
labelSet =ixNet.add(label2,'counter')
ixNet.setMultiAttribute(labelSet, '-step', '1', '-start', '500', '-direction', 'increment')
#ixNet.setAttribute(activeMultivalue1 + '/singleValue', '-value', 'true')
ixNet.commit()

globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")
# end try/expect
time.sleep(20)

###############################################################################
# 6. Retrieve protocol learned info again and compare with
#    previouly retrieved learned info.
###############################################################################
print("Fetching mplsoam learned info after changing labels of FEC")
ixNet.execute('getAllLearnedInfo', mplsoam1, '1')
time.sleep(5)
linfo  = ixNet.getList(mplsoam1, 'learnedInfo')[0]
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
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ethernetVlan')
ixNet.commit()

trafficItem1 = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')
source       = [networkGroup1]
destination  = [networkGroup2]

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
#print ('Stopping applib traffic')
#ixNet.execute('stopStatefulTraffic', ixNet.getRoot() + '/traffic')
#time.sleep(5)

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
