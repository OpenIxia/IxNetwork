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
#    This script intends to demonstrate how to use NGPF mLDP API.              #
#                                                                              #
#    1. It will create 2 mLDP topologies: 1 Ingress with Root Range configured #
#       and another Egress with Leaf Range.                                    #
#    2. Configure Root Ranges with Source Endpoint.                            #
#    3. Configure Leaf Ranges with Multicast Destination Endpoint.             #
#    4. Start the ldp protocol.                                                #
#    5. Retrieve protocol statistics.                                          #
#    6. Retrieve protocol learned info.                                        #
#    7. Change label and LSP Count per Root & apply change on the fly          #
#    8. Retrieve protocol learned info again and notice the difference with    #
#       previouly retrieved learned info.                                      #
#    9. Configure IPv4 & IPv6 L2-L3 traffic.                                   #
#   10. Retrieve L2-L3 traffic stats.                                          #
#   11. Stop L2-L3 traffic.                                                    #
#   12. Stop all protocols.                                                    #
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
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.30.1076.4-EB\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.39.50.155'
ixTclPort   = '8332'
ports       = [('10.39.43.154', '4', '1',), ('10.39.43.154', '4', '2',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("Connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.30',
     '-setAttribute', 'strict')

# Cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

# Assigning ports
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

root    = ixNet.getRoot()
vportTx = ixNet.getList(root, 'vport')[0]
vportRx = ixNet.getList(root, 'vport')[1]

print("Adding topologies")
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

print("Add IPv4")
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

print("Adding mLDP over IPv4 stacks")
ixNet.add(ip1, 'ldpBasicRouter')
ixNet.add(ip2, 'ldpBasicRouter')
ixNet.commit()

ldp1 = ixNet.getList(ip1, 'ldpBasicRouter')[0]
ldp2 = ixNet.getList(ip2, 'ldpBasicRouter')[0]

print ("Enabling P2MP capability for mLDP")
capability1 =(ixNet.getAttribute(ldp1, '-enableP2MPCapability'))
capability2 =(ixNet.getAttribute(ldp2, '-enableP2MPCapability'))

ixNet.setAttribute(capability1 + '/singleValue', '-value', 'true')
ixNet.setAttribute(capability2 + '/singleValue', '-value', 'true')
ixNet.commit()

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'mLDP Topology 1:Ingress')
ixNet.setAttribute(topo2, '-name', 'mLDP Topology 2:Egress')

ixNet.setAttribute(t1dev1, '-name', 'mLDP Topology 1:Ingress Router')
ixNet.setAttribute(t2dev1, '-name', 'mLDP Topology 2:Egress Router')
ixNet.commit()

print("Configuring Root Ranges behind Topology 1")
ixNet.setMultiAttribute(ldp1, '-rootRangesCountV4', '1')
ixNet.commit()

print("Configuring Leaf Ranges behind Topology 2")
ixNet.setMultiAttribute(ldp2, '-leafRangesCountV4', '1')
ixNet.commit()

print("Changing Root Address in Root Ranges behind Topology 1")
rootRanges= ixNet.getList(ldp1, 'ldpRootRangeV4')[0]
rootRange_rootAddrCount =(ixNet.getAttribute(rootRanges, '-rootAddress'))
ixNet.setMultiAttribute(rootRange_rootAddrCount + '/counter', '-start', '15.1.1.1') 
ixNet.commit()

print("Changing Root Address in Leaf Ranges behind Topology 2")
leafRanges= ixNet.getList(ldp2, 'ldpLeafRangeV4')[0]
leafRange_rootAddrCount =(ixNet.getAttribute(leafRanges, '-rootAddress'))
ixNet.setMultiAttribute(leafRange_rootAddrCount + '/counter', '-start', '15.1.1.1') 
ixNet.commit()

print("Configuring 2 Opaque TLVs for Root Ranges")	
rootRange_numberOfTLV=(ixNet.setAttribute(rootRanges, '-numberOfTLVs', '2'))
ixNet.commit()

print("Configuring 2 Opaque TLVs for Leaf Ranges")	
leafRange_numberOfTLV=(ixNet.setAttribute(leafRanges, '-numberOfTLVs', '2'))
ixNet.commit()

print("Configuring 2nd Opaque TLV as Type:2 for Root Ranges")
type_2_1= (ixNet.getAttribute(rootRanges + '/ldpTLVList:2', '-type'))
ixNet.setMultiAttribute(type_2_1 + '/singleValue', '-value', '2')
ixNet.commit()

print("Configuring 2nd Opaque TLV as Type:2 for Leaf Ranges")
type_2_2= (ixNet.getAttribute(leafRanges + '/ldpTLVList:2', '-type'))
ixNet.setMultiAttribute(type_2_2 + '/singleValue', '-value', '2')
ixNet.commit()

print("Changing 1st Opaque TLV Value for Root Ranges")
value_2_1=(ixNet.getAttribute(rootRanges + '/ldpTLVList:1', '-value'))
ixNet.setMultiAttribute(value_2_1 + '/singleValue', '-value', '00000066')  
ixNet.commit()

print("Changing 1st Opaque TLV Value for Leaf Ranges")
value_2_2=(ixNet.getAttribute(leafRanges + '/ldpTLVList:1', '-value'))
ixNet.setMultiAttribute(value_2_2 + '/singleValue', '-value', '00000066')  
ixNet.commit()

print("Changing 2nd Opaque TLV Increment for Root Ranges")
increment_2_1 =(ixNet.getAttribute(rootRanges + '/ldpTLVList:2', '-increment'))
ixNet.setMultiAttribute(increment_2_1 + '/singleValue', '-value', '0000000000000010')  
ixNet.commit()

print("Changing 2nd Opaque TLV Increment for Leaf Ranges")
increment_2_2 =(ixNet.getAttribute(leafRanges + '/ldpTLVList:2', '-increment'))
ixNet.setMultiAttribute(increment_2_2 + '/singleValue', '-value', '0000000000000010')  
ixNet.commit()

print("Changing IPv4 Group Addresses under Leaf Ranges behind Egress Router")
groupAddressV4= (ixNet.getAttribute(leafRanges, '-groupAddressV4'))
ixNet.setMultiAttribute(groupAddressV4 + '/singleValue', '-value', '225.0.1.1') 
ixNet.commit()

print("Changing IPv6 Group Addresses under Leaf Ranges behind Egress Router")
groupAddressV6= (ixNet.getAttribute(leafRanges, '-groupAddressV6'))
ixNet.setMultiAttribute(groupAddressV6 + '/singleValue', '-value', 'ff15:0:1::') 
ixNet.commit()

print("Changing IPv4 Source Addresses under Root Ranges behind Ingress Router")
sourceAddressV4=(ixNet.getAttribute(rootRanges, '-sourceAddressV4'))
ixNet.setMultiAttribute(sourceAddressV4 + '/singleValue', '-value', '5.1.1.1')   
ixNet.commit()

print("Changing IPv6 Source Addresses under Root Ranges behind Ingress Router")
sourceAddressV6=(ixNet.getAttribute(rootRanges, '-sourceAddressV6'))
ixNet.setMultiAttribute(sourceAddressV6 + '/singleValue', '-value', '6001:1::1')   
ixNet.commit()

print("Changing Group Addresses count under Leaf Ranges behind Egress Router")
groupCountPerLsp=(ixNet.getAttribute(leafRanges, '-groupCountPerLsp'))
ixNet.setMultiAttribute(groupCountPerLsp + '/singleValue', '-value', '5')
ixNet.commit()

################################################################################
# 2. Start ldp protocol and wait for 60 seconds
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
print("Fetching P2MP FEC Learned Info in Ingress Router on Topology 1")
ixNet.execute('getP2MPFECLearnedInfo', ldp1, '1')
time.sleep(5)
linfo  = ixNet.getList(ldp1, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# 5.Change the label, number of LSP Count And apply changes On The Fly (OTF).
################################################################################
print("Changing LSP Count per root On The Fly behind Egress Router on Topology 2")
lsp2=(ixNet.getAttribute(leafRanges, '-lspCountPerRoot'))
ixNet.setMultiAttribute(lsp2 + '/singleValue', '-value', '5')

print("Changing Label value  On The Fly behind Egress Router on Topology 2")
label=(ixNet.getAttribute(leafRanges, '-labelValueStart'))
ixNet.setMultiAttribute(label + '/singleValue', '-value', '666') 
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
# 6. Retrieve protocol learned info again and compare with
#    previously retrieved learned info.
###############################################################################
print("Fetching P2MP FEC Learned Info in Ingress Router on Topology 1")
ixNet.execute('getP2MPFECLearnedInfo', ldp1, '1')
time.sleep(5)
linfo  = ixNet.getList(ldp1, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# 7. Configure L2-L3 traffic
################################################################################
print("Configuring L2-L3 Traffic Item")
trafficItem1 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem1, '-name', 'IPv4 Traffic Item',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv4')
ixNet.commit()

trafficItem1 = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')
source       = [ldp1 + '/ldpRootRangeV4']

ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
    '-scalableSources',       [],
    '-multicastReceivers',    [[ldp2+ '/ldpLeafRangeV4','0','0','0']],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               source,
    '-destinations',          [])
ixNet.commit()

ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'trackingenabled0', 'mplsMplsLabelValue0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         [])
ixNet.commit()

trafficItem2 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem2, '-name', 'IPv6 Traffic Item',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv6')
ixNet.commit()

trafficItem2 = ixNet.remapIds(trafficItem2)[0]
endpointSet2 = ixNet.add(trafficItem2, 'endpointSet')
source       = [ldp1 + '/ldpRootRangeV4']

ixNet.setMultiAttribute(endpointSet2,
    '-name',                  'EndpointSet-1',
    '-scalableSources',       [],
    '-multicastReceivers',    [[ldp2+ '/ldpLeafRangeV4','0','0','0']],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               source,
    '-destinations',          [])
ixNet.commit()

ixNet.setMultiAttribute(trafficItem2 + '/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'trackingenabled0', 'mplsMplsLabelValue0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         [])
ixNet.commit()

###############################################################################
# 8. Apply and start L2/L3 traffic
###############################################################################
print ('applying L2/L3 traffic')
ixNet.execute('apply', ixNet.getRoot() + '/traffic')
time.sleep(5)

print ('starting L2/L3 traffic')
ixNet.execute('start', ixNet.getRoot() + '/traffic')

print ('Let traffic run for 1 minute')
time.sleep(60)

###############################################################################
# 9. Retrieve L2/L3 traffic item statistics
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
# 10. Stop L2/L3 traffic
################################################################################
print ('Stopping L2/L3 traffic')
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)

################################################################################
# 11. Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
