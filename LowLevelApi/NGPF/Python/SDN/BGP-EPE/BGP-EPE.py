# -*- coding: cp1252 -*-
#!/usr/bin/tclsh
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
#    This script intends to demonstrate how to use NGPF BGP EPE API            #
#    It will create 2 BGP EPE topologies, it will start the emulation and      #
#    than it will retrieve and display few statistics                          #
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
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\7.40-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information   #
# below                                                                         #
#################################################################################
ixTclServer = '10.39.43.12'
ixTclPort   = '8072'
ports       = [('10.39.50.123', '5', '7',), ('10.39.50.123', '5', '8',)]
# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '7.40',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

################################################################################
# protocol configuration section                                               #
################################################################################ 
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

print ('ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet\')')

print("Adding IPv4 protocol stack")
ixNet.add(mac1, 'ipv4')
ixNet.add(mac2, 'ipv4')
ixNet.commit()

ip1 = ixNet.getList(mac1, 'ipv4')[0]
ip2 = ixNet.getList(mac2, 'ipv4')[0]

mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvAdd2 = ixNet.getAttribute(ip2, '-address')
mvGw1  = ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = ixNet.getAttribute(ip2, '-gatewayIp')

print("Configuring IPv4 addresses")
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '20.20.20.2')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '20.20.20.2')

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

print("Adding BGP protocol stack over IP4")
ixNet.add(ip1, 'bgpIpv4Peer')
ixNet.add(ip2, 'bgpIpv4Peer')
ixNet.commit()

bgp1 = ixNet.getList(ip1, 'bgpIpv4Peer')[0]
bgp2 = ixNet.getList(ip2, 'bgpIpv4Peer')[0]

print("Setting IPs in BGP DUT IP tab")
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-dutIp') + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-dutIp') + '/singleValue', '-value', '20.20.20.2')
ixNet.commit()

print ("Enabling BGP Link State Non-VPN Capability")
cap1 = ixNet.getAttribute(bgp1, '-capabilityLinkStateNonVpn')
cap2 = ixNet.getAttribute(bgp2, '-capabilityLinkStateNonVpn')
sv1 = ixNet.getList(cap1, 'singleValue')[0]
sv2 = ixNet.getList(cap2, 'singleValue')[0]
ixNet.setAttribute(sv1, '-value', 'true')
ixNet.setAttribute(sv2, '-value', 'true')
ixNet.commit()

print ("Enabling BGP Filter Link State")
filter1 = ixNet.getAttribute(bgp1, '-filterLinkState')
filter2 = ixNet.getAttribute(bgp2, '-filterLinkState')
sv1 = ixNet.getList(filter1, 'singleValue')[0]
sv2 = ixNet.getList(filter2, 'singleValue')[0]
ixNet.setAttribute(sv1, '-value', 'true')
ixNet.setAttribute(sv2, '-value', 'true')
ixNet.commit()


print ("Enable BGP EPE in Topology 1")
ixNet.setAttribute(bgp1, '-noOfEpePeers', '3')
ixNet.commit()

bgpEpePeerList = ixNet.getList(bgp1, 'bgpEpePeerList')[0]
bgpEpePeerLinkList = ixNet.getList(bgpEpePeerList, 'bgpEpePeerLinkList')[0]

print ("Setting Number of Links for BGP EPE to 2 in Topology 1")
ixNet.setAttribute(bgpEpePeerList, '-noOflinks', '2')
ixNet.commit()

print ("Setting Number of EPE Peer Set to 3 in Topology 1")
ixNet.setAttribute(bgpEpePeerList, '-noOfPeerSet', '2')
ixNet.commit()

print ("Selection of Peer Set Group")
peerSetGroup = ixNet.getAttribute(bgpEpePeerList, '-peerSetGroup')
ixNet.setMultiAttribute(peerSetGroup, '-clearOverlays', 'true')
activeOverlay = ixNet.add(peerSetGroup, 'overlay')
activeOverlay =ixNet.add(peerSetGroup, 'singleValue')
ixNet.setMultiAttribute(activeOverlay, '-value', 'peersetgroup1 peersetgroup2')
ixNet.commit()


print ("Setting BGP Remote Router ID as DUT IP of BGP Peer")
ixNet.setAttribute(ixNet.getAttribute(bgpEpePeerList, '-bgpRemoteRouterId') + '/singleValue', '-value', '20.20.20.1')
ixNet.commit()

print ("Setting EPE Peer Links Peer-Adj-SID to True")
ixNet.setAttribute(ixNet.getAttribute(bgpEpePeerLinkList, '-enablePeerAdjSid') + '/singleValue', '-value', 'True')
ixNet.commit()

print ("Setting EPE Peer Links Remote IPv4 Link Address")
ixNet.setAttribute(ixNet.getAttribute(bgpEpePeerLinkList, '-remoteIpv4LinkAddress') + '/singleValue', '-value', '20.20.20.1')
ixNet.commit()

bgpLocalIp = ixNet.getAttribute(bgp1, '-localIpv4Ver2')

print ("Setting EPE Peer Links Local IPv4 Link Address")
ixNet.setAttribute(ixNet.getAttribute(bgpEpePeerLinkList, '-localIpv4LinkAddress') + '/singleValue', '-value', bgpLocalIp)
ixNet.commit()

print("Adding OSPFv2 over IP4 stacks")
ospf1 = ixNet.add(ip1, 'ospfv2')
ospf2 = ixNet.add(ip2, 'ospfv2')
ixNet.commit()

print("Changing OSPFv2 Network Type")
networkTypeMultiValue1 = ixNet.getAttribute(ospf1, '-networkType')
ixNet.setAttribute(ixNet.getAttribute(ospf1, '-networkType') + '/singleValue', '-value', 'pointtopoint')
ixNet.commit()

print("Changing OSPFv2 Network Type")
networkTypeMultiValue1 = ixNet.getAttribute(ospf2, '-networkType')
ixNet.setAttribute(ixNet.getAttribute(ospf2, '-networkType') + '/singleValue', '-value', 'pointtopoint')
ixNet.commit()

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1,  '-name', 'BGP Topology 1')
ixNet.setAttribute(topo2,  '-name', 'BGP Topology 2')

ixNet.setAttribute(t1dev1,  '-name', 'BGP Topology 1 Router')
ixNet.setAttribute(t2dev1,  '-name', 'BGP Topology 2 Router')
ixNet.commit()

################################################################################
# Start protocol and check statistics                                          #
################################################################################
print("Starting protocols and waiting for 45 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(45)
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

print ("Verifying BGP Peer related stats\n")
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
print("***************************************************")

###############################################################################
# print learned info                                                          #
###############################################################################
ixNet.execute('getLinkStateLearnedInfo', bgp2, '1')
time.sleep(5)

linfo  = ixNet.getList(bgp2, 'learnedInfo')[0] 
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

time.sleep(15)

print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
