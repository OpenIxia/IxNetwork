# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/12/2016 - Poulomi Chatterjee - created sample                          #
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
#    This script intends to demonstrate how to use NGPF BGP API to configure   #
#     L3vpn interAS OptionC Scenario.                                          #
#                                                                              #
#    1. It will create a BGP topology with LDP & OSPF configured in Provider   #
#        Router.                                                               #
#    2. In Provider Edge Router configuration 2 BGP Peer are configured.       #
#       - iBGP Peer                                                            #
#       - eBGP Peer to configure Multi Hop BGP session.                        #
#    3. Only one side configuration is provided.                               #
#    4. Traffic configuration will be similar to L3VPN scenario.               #
# Ixia Software:                                                               #
#    IxOS      8.20 EA                                                         #
#    IxNetwork 8.20 EA                                                         #
#                      
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
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.20-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
# Script Starts
print("!!!L3VPN Option C Test Script Starts !!!")
ixTclServer = '10.216.108.113'
ixTclPort   = '8650'
ports       = [('10.216.108.82', '7', '11'), ('10.216.108.82', '7', '12')]

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

print("Adding topology")
ixNet.add(root, 'topology', '-vports', vportTx)
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]

print "Adding device group"
ixNet.add(topo1, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')

t1dev1 = t1devices[0]

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(t1dev1, '-multiplier', '1')
ixNet.commit()

print("Adding ethernet/mac endpoints")
ixNet.add(t1dev1, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(t1dev1, 'ethernet')[0]

print("Configuring the mac addresses %s" % (mac1))
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '18:03:73:C7:6C:B1',
    '-step',      '00:00:00:00:00:01')

ixNet.commit()

#print ("ixNet.help ::ixNet::OBJ-/topology/deviceGroup/ethernet")
#print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet'))

print("Add ipv4")
ixNet.add(mac1, 'ipv4')
ixNet.commit()

ip1 = ixNet.getList(mac1, 'ipv4')[0]

mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvGw1  = ixNet.getAttribute(ip1, '-gatewayIp')

print("configuring ipv4 addresses")
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '20.20.20.2')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '20.20.20.1')

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

#print ("ixNet.help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4")
#print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4'))

print("Adding OSPF over IP4 stacks")
ixNet.add(ip1, 'ospfv2')
ixNet.commit()

ospf1 = ixNet.getList(ip1, 'ospfv2')[0]

print("Adding LDP over IP4 stacks")
ixNet.add(ip1, 'ldpBasicRouter')
ixNet.commit()

ldp1 = ixNet.getList(ip1, 'ldpBasicRouter')[0]

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'L3vpn_interAS_OptionC_Topology')

ixNet.setAttribute(t1dev1, '-name', 'Provider Router')
ixNet.commit()

#print ("ixNet.help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp")
#print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp'))

print("Adding NetworkGroup behind Provider Router DG")
ixNet.execute('createDefaultStack', t1devices, 'ipv4PrefixPools')

networkGroup1 = ixNet.getList(t1dev1, 'networkGroup')[0]

ixNet.setAttribute(networkGroup1, '-name', 'Network_Group')
ixNet.setAttribute(networkGroup1, '-multiplier', '1')

print("Configuring LDP prefixes")
ldpPrefixPool1 = ixNet.getList(networkGroup1, 'ipv4PrefixPools')[0]
ixNet.setAttribute(ixNet.getAttribute(ldpPrefixPool1, '-networkAddress') + '/singleValue', '-value', '2.2.2.2')
ixNet.setAttribute(ixNet.getAttribute(ldpPrefixPool1, '-prefixLength') + '/singleValue', '-value', '32')
ixNet.commit()

# Add Chanied DG behind LDP NetworkGroup
print("Add Chanied DG behind LDP NetworkGroup")
chainedDg1 = ixNet.add(networkGroup1, 'deviceGroup')
ixNet.setMultiAttribute(chainedDg1, '-multiplier', '1', '-name', 'Device Group 3')
ixNet.commit()
chainedDg1 = ixNet.remapIds(chainedDg1)[0]

loopback1 = ixNet.add(chainedDg1, 'ipv4Loopback')
ixNet.setMultiAttribute(loopback1, '-stackedLayers', [], '-name', 'IPv4 Loopback 1')
ixNet.commit()

connector1 = ixNet.add(loopback1, 'connector')
ixNet.setMultiAttribute(connector1, '-connectedTo', networkGroup1 + '/ipv4PrefixPools:1')
ixNet.commit()
connector1 = ixNet.remapIds(connector1)[0]

addressSet1 = ixNet.getAttribute(loopback1, '-address')
ixNet.setMultiAttribute(addressSet1, '-clearOverlays', 'false', '-pattern', 'counter')
ixNet.commit()

addressSet1 = ixNet.add(addressSet1, 'counter')
ixNet.setMultiAttribute(addressSet1, '-step', '0.0.0.1', '-start', '2.2.2.2', '-direction', 'increment')
ixNet.commit()
addressSet1 = ixNet.remapIds(addressSet1)[0]


# Adding BGP over IPv4 loopback interfaces (multi Hop eBGP Peer)
print("Adding BGP over IPv4 loopback interfaces")
ixNet.add(loopback1, 'bgpIpv4Peer')
ixNet.commit()
ebgp = ixNet.getList(loopback1, 'bgpIpv4Peer')[0]

# Changing bgp type to external
print("Changing bgp type to external")
ixNet.setAttribute(ixNet.getAttribute(ebgp, '-type') + '/singleValue', '-value', 'external')
ixNet.commit()

#addressSet1 = ixNet.add(addressSet1, 'counter')
#ixNet.setMultiAttribute(addressSet1, '-step', '0.1.0.0', '-start', '200.1.0.0', '-direction', 'increment')
#ixNet.commit()

# Changing name of eBGP Peer
ixNet.setAttribute(ebgp, '-name', 'Multihop eBGP Peer')
ixNet.commit()

print("Setting IPs in BGP DUT IP tab")
ixNet.setAttribute(ixNet.getAttribute(ebgp, '-dutIp') + '/singleValue', '-value', '3.2.2.2')
ixNet.commit()

# Adding another BGP Peer over IPv4 loopback interfaces (iBGP Peer)
print("Adding another BGP Peer over same IPv4 loopback interface")
ixNet.add(loopback1, 'bgpIpv4Peer')
ixNet.commit()
ibgp = ixNet.getList(loopback1, 'bgpIpv4Peer')[1]

# Changing name of iBGP Peer
ixNet.setAttribute(ibgp, '-name', 'iBGP Peer')
ixNet.commit()

print("Setting IPs in eBGP DUT IP tab")
ixNet.setAttribute(ixNet.getAttribute(ibgp, '-dutIp') + '/singleValue', '-value', '4.2.2.2')
ixNet.commit()

# Enabling IPv4 MPLS Capability in iBGP Peer
print("Enabling IPv4 MPLS Capability in iBGP Peer")
ixNet.setMultiAttribute(ibgp, '-ipv4MplsCapability', 'true')
ixNet.commit()

print("Enabling L3VPN  Learned Information filters for BGP Router")
ixNet.setAttribute(ixNet.getAttribute(ebgp, '-filterIpV4Mpls') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(ebgp, '-filterIpV4MplsVpn') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(ibgp, '-filterIpV4Mpls') + '/singleValue', '-value', 'true')
ixNet.setAttribute(ixNet.getAttribute(ibgp, '-filterIpV4MplsVpn') + '/singleValue', '-value', 'true')
ixNet.commit()

print("Adding VRF over eBGP Peer")
ixNet.add(ebgp, 'bgpVrf')
ixNet.commit()

bgpVrf = ixNet.getList(ebgp, 'bgpVrf')[0]

print("Adding IPv4 Address Pool behind bgpVrf with name VPN RouteRange(Src)")
networkGroup3 = ixNet.add(chainedDg1, 'networkGroup')
ipv4PrefixPool1 = ixNet.add(networkGroup3, 'ipv4PrefixPools')
ixNet.setAttribute(networkGroup3, '-name', 'VPN RouteRange(Src)')
ixNet.setAttribute(networkGroup3, '-multiplier', '1')
ixNet.commit()

print("Changing default values of IP prefixes in VPN RouteRange(Src)")
ixNet.setAttribute(ixNet.getAttribute(ipv4PrefixPool1, '-networkAddress') + '/singleValue', '-value', '11.11.11.1')
ixNet.commit()

print("Adding another IPv4 Address Pool connected to iBGP Peer")
networkGroup4 = ixNet.add(chainedDg1, 'networkGroup')
ipv4PrefixPool2 = ixNet.add(networkGroup4, 'ipv4PrefixPools')
ixNet.setAttribute(networkGroup4, '-name', 'eBGP Lpbk Addr(MPLS RR)')
ixNet.setAttribute(networkGroup4, '-multiplier', '1')
ixNet.commit()

print("Changing default values of IP prefixes in eBGP Lpbk Addr(MPLS RR)")
ixNet.setAttribute(ixNet.getAttribute(ipv4PrefixPool2, '-networkAddress') + '/singleValue', '-value', '2.2.2.2')
ixNet.commit()

# Change connector to iBGP Peer
print("Changing BGP Connector in 2nd Prefix pool")
connector = ixNet.add(ipv4PrefixPool2, 'connector')
ixNet.setMultiAttribute(connector, '-connectedTo', ibgp)
ixNet.commit()

#connector1 = ixNet.add(loopback1, 'connector')
#ixNet.setMultiAttribute(connector1, '-connectedTo', networkGroup1 + '/ipv4PrefixPools:1')
#ixNet.commit()
#connector1 = ixNet.remapIds(connector1)[0]

# Enabling IPv4 MPLS Capability in iBGP Prefix Pool
print("Enabling IPv4 MPLS Capability in iBGP Prefix Pool")
bgpIPRouteProperty = ixNet.getList(ipv4PrefixPool2, 'bgpIPRouteProperty')[0]
ixNet.setMultiAttribute(bgpIPRouteProperty, '-advertiseAsBgp3107', 'true')
ixNet.commit()

# Changing label start value in iBGP Prefix Pool
print("Changing label start value in iBGP Prefix Pool")
labelStart = ixNet.getAttribute(bgpIPRouteProperty, '-labelStart')
ixNet.setMultiAttribute(labelStart, '-clearOverlays', 'false')
ixNet.commit()

counter = ixNet.add(labelStart, 'counter')
ixNet.setMultiAttribute(counter,  '-step', '5', '-start', '21', '-direction', 'increment')
ixNet.commit()

print("!!! Configured topology Successfully!!!")
print ('!!! Test Script Ends !!!')
