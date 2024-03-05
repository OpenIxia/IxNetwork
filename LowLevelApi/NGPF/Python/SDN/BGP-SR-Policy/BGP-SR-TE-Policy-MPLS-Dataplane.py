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
#    This script intends to demonstrate how to use NGPF BGP API                #
#    It will create 2 BGP topologies, it will start the emulation and          #
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
ixTclServer = '10.39.50.121'
ixTclPort   = '8239'
ports       = [('10.39.50.123', '1', '7',), ('10.39.50.123', '1', '8',)]

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

print("Adding BGP over IPv4 stacks")
ixNet.add(ip1, 'bgpIpv4Peer')
ixNet.add(ip2, 'bgpIpv4Peer')
ixNet.commit()

bgp1 = ixNet.getList(ip1, 'bgpIpv4Peer')[0]
bgp2 = ixNet.getList(ip2, 'bgpIpv4Peer')[0]

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1,  '-name', 'BGP Topology 1')
ixNet.setAttribute(topo2,  '-name', 'BGP Topology 2')

ixNet.setAttribute(t1dev1,  '-name', 'SR-TE Policy Controller')
ixNet.setAttribute(t2dev1,  '-name', 'Head/Tail End Router')
ixNet.commit()

print("Setting IPs in BGP DUT IP tab")
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-dutIp') + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-dutIp') + '/singleValue', '-value', '20.20.20.2')
ixNet.commit()

print ("Enabling IPv4 SRTE Capability")
cap1 = ixNet.getAttribute(bgp1, '-capabilitySRTEPoliciesV4')
cap2 = ixNet.getAttribute(bgp2, '-capabilitySRTEPoliciesV4')
sv1 = ixNet.getList(cap1, 'singleValue')[0]
sv2 = ixNet.getList(cap2, 'singleValue')[0]
ixNet.setAttribute(sv1, '-value', 'true')
ixNet.setAttribute(sv2, '-value', 'true')
ixNet.commit()

print ("Enabling IPv4 SR TE Policy Learned Info filter")
filter1 = ixNet.getAttribute(bgp1, '-filterSRTEPoliciesV4')
filter2 = ixNet.getAttribute(bgp2, '-filterSRTEPoliciesV4')
sv1 = ixNet.getList(filter1, 'singleValue')[0]
sv2 = ixNet.getList(filter2, 'singleValue')[0]
ixNet.setAttribute(sv1, '-value', 'true')
ixNet.setAttribute(sv2, '-value', 'true')
ixNet.commit()

print ("*************************************************************")
print ("Configuring Controller")
print ("*************************************************************")

print ("Setting number of polocies")
ixNet.setAttribute(bgp1, '-numberSRTEPolicies', '1')
ixNet.commit()

print ("Setting IPv4 End Point Value")
ixNet.setAttribute(ixNet.getAttribute(bgp1 + '/bgpSRTEPoliciesListV4', '-endPointV4') + '/singleValue', '-value', '30.30.30.1')
ixNet.commit()

print ("Setting color Value")
ixNet.setAttribute(ixNet.getAttribute(bgp1 + '/bgpSRTEPoliciesListV4', '-policyColor') + '/singleValue', '-value', '200')
ixNet.commit()

print ("Setting Number of Segment Lists")
ixNet.setAttribute(bgp1 + '/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4', '-numberOfSegmentListV4', '2')
ixNet.commit()

print ("Enabling Binding SID")
ixNet.setAttribute(ixNet.getAttribute(bgp1 + '/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4', '-enBindingTLV') + '/singleValue', '-value', 'true')
ixNet.commit()

print ("Setting Binding SID Type")
ixNet.setAttribute(ixNet.getAttribute(bgp1 + '/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4', '-bindingSIDType') + '/singleValue', '-value', 'sid4')
ixNet.commit()

print ("Setting SID value")
ixNet.setAttribute(ixNet.getAttribute(bgp1 + '/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4', '-SID4Octet') + '/singleValue', '-value', '400')
ixNet.commit()

print ("Setting Number of Segments")
ixNet.setAttribute(bgp1 + '/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4/bgpSRTEPoliciesSegmentListV4', '-numberOfSegmentsV4', '3')
ixNet.commit()

print ("Setting lable value for -MPLS SID Only- Segment Type")
ixNet.setAttribute(ixNet.getAttribute(bgp1 + '/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4/bgpSRTEPoliciesSegmentListV4/bgpSRTEPoliciesSegmentsCollectionV4', '-label') + '/singleValue', '-value', '999')
ixNet.commit()

print ("*************************************************************")
print ("Configuring Prefix")
print ("*************************************************************")

print("Adding the NetworkGroup with Routers at back of it")
prefixpool1  = ixNet.execute('createDefaultStack', t2dev1, 'ipv4PrefixPools')
networkGroup1 = (ixNet.getList(t2dev1, 'networkGroup'))[0]
ixNet.setAttribute(networkGroup1, '-name', 'Endpoint Prefix Advertising color')

ip4pool = (ixNet.getList(networkGroup1, 'ipv4PrefixPools'))[0]
bgpIPRouteProperty = (ixNet.getList(ip4pool, 'bgpIPRouteProperty'))[0]

print ("Setting Network Address")
ixNet.setAttribute(ixNet.getAttribute(ip4pool, '-networkAddress') + '/singleValue', '-value', '30.30.30.1')

print ("Enabling Extended Community")
ixNet.setAttribute(ixNet.getAttribute(bgpIPRouteProperty,'-enableExtendedCommunity') + '/singleValue', '-value', 'true')

print ("Setting Extended Community Type")
ixNet.setAttribute(ixNet.getAttribute(bgpIPRouteProperty + '/bgpExtendedCommunitiesList:1', '-type') + '/singleValue', '-value', 'opaque')

print ("Setting Extended Community Sub-Type")
ixNet.setAttribute(ixNet.getAttribute(bgpIPRouteProperty + '/bgpExtendedCommunitiesList:1', '-subType') + '/singleValue', '-value', 'color')

print ("Setting Color Value")
ixNet.setAttribute(ixNet.getAttribute(bgpIPRouteProperty + '/bgpExtendedCommunitiesList:1', '-colorValue') + '/singleValue', '-value', '200')
ixNet.commit()

################################################################################
# Start protocol and check statistics                                          #
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
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

################################################################################
# On the fly section                                                           #  
################################################################################
print("Changing the label Value on the Fly")
ixNet.setAttribute(ixNet.getAttribute(bgp1 + '/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4/bgpSRTEPoliciesSegmentListV4/bgpSRTEPoliciesSegmentsCollectionV4', '-label') + '/singleValue', '-value', '1000')
ixNet.commit()

globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")
# end try/expect
time.sleep(10)

###############################################################################
# print learned info                                                          #
###############################################################################
ixNet.execute('getbgpSrTeLearnedInfoLearnedInfo', bgp2, '1')
time.sleep(5)

print("Print Bgp Ipv4 SR-TE Learned Info")
linfo  = ixNet.getList(bgp2, 'learnedInfo')[0]
linfoList = ixNet.getList(linfo, 'table')
#print "##################################################################"
#print linfoList
#print "##################################################################"
print("***************************************************")
tableType = ixNet.getAttribute(linfoList[0], '-type')
print(tableType)
print("=================================================")
columns = ixNet.getAttribute(linfoList[0], '-columns')
print(columns)
values = ixNet.getAttribute(linfoList[0], '-values')
for value in values :
    print(value)
          #end for
      # end for
# end for 

time.sleep(15)

print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
