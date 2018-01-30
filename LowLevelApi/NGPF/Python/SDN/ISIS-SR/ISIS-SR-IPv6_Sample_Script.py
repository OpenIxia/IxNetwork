# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    21/11/2016 - Chandan Mishra - created sample                                     #
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
#    This script intends to demonstrate how to use NGPF IPv6 SR Low Level      #
#    Python API.                                                                 #
#                                                                              #
#    1. It will create 2 ISIS topologies, topology2 will have                  #
#       IPv6 prefix pool & Simulated Topology.                                 #
#    2. Enable SR and SR IPv6 in ISIS Emulated Router.                         #
#    3. Set IPv6 Node Prefix & IPv6 Adj-Sid.                                   #
#    4. Enable Segment Routing in Simulated Router and                         #
#       Set IPv6 Node Prefix & IPv6 Adj-Sid in Simulated Router.               #  
#    5. Start protocol.                                                        #
#    6. Retrieve protocol statistics.                                          #
#    7. Retrieve protocol learned info in Port1.                               #
#    8. On the fly disable Adj-Sid in simulated interface.                     #
#    9. Retrieve protocol learned info in Port1 after On the Fly change.       #
#    10. Stop all protocols.                                                   #
#                                                                              #
# Ixia Softwares:                                                              #
#    IxOS      8.20 EA                                                         #
#    IxNetwork 8.20 EA                                                         #
#                                                                              #
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
# Either feed the ixNetwork library path in the sys.path as below, or put the  #
# IxNetwork.py file somewhere else where we python can autoload it             #
# "IxNetwork.py" is available in <IxNetwork_installer_path>\API\Python         #
################################################################################
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.20.0.194-EB\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information   #
# below                                                                         #
#################################################################################
ixTclServer = '10.216.108.27'
ixTclPort   = '8091'
ports       = [('10.216.108.99', '4', '5',), ('10.216.108.99', '4', '6',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.20',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

################################################################################
# 1. Protocol configuration section. Configure ISIS as per the description
#  give above
################################################################################ 

# assigning ports
print("Assigning the ports")
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

root    = ixNet.getRoot()
vportTx = ixNet.getList(root, 'vport')[0]
vportRx = ixNet.getList(root, 'vport')[1]

# Adding topologies
print("Adding 2 topologies")
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

print("Add ipv6")
ixNet.add(mac1, 'ipv6')
ixNet.add(mac2, 'ipv6')
ixNet.commit()

ip1 = ixNet.getList(mac1, 'ipv6')[0]
ip2 = ixNet.getList(mac2, 'ipv6')[0]

mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvAdd2 = ixNet.getAttribute(ip2, '-address')
mvGw1  = ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = ixNet.getAttribute(ip2, '-gatewayIp')

print("configuring ipv6 addresses")
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '2000::1')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '2000::101')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '2000::101')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '2000::1')

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '64')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '64')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

print("Adding ISIS over Ethernet stacks")
ixNet.add(mac1, 'isisL3')
ixNet.add(mac2, 'isisL3')
ixNet.commit()

isisL3_1 = ixNet.getList(mac1, 'isisL3')[0]
isisL3_2 = ixNet.getList(mac2, 'isisL3')[0]

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'ISIS Topology 1')
ixNet.setAttribute(topo2, '-name', 'ISIS Topology 2')

ixNet.setAttribute(t1dev1, '-name', 'ISIS Topology 1 Router')
ixNet.setAttribute(t2dev1, '-name', 'ISIS Topology 2 Router')
ixNet.commit()

isisL3Router1_1 = ixNet.getList(t1dev1, 'isisL3Router')[0]
isisL3Router2_1 = ixNet.getList(t2dev1, 'isisL3Router')[0]

# Enable host name in ISIS routers
print("Enabling Host name in Emulated ISIS Routers")
deviceGroup1 = ixNet.getList(topo1, 'deviceGroup')[0]
isisL3Router1 = ixNet.getList(deviceGroup1, 'isisL3Router')[0]
enableHostName1 = ixNet.getAttribute(isisL3Router1, '-enableHostName')
ixNet.setAttribute(enableHostName1 + '/singleValue', '-value', 'True')
ixNet.commit()
time.sleep(5)
configureHostName1 = ixNet.getAttribute(isisL3Router1, '-hostName')
ixNet.setAttribute(configureHostName1 + '/singleValue', '-value', 'isisL3Router1')
ixNet.commit()

deviceGroup2 = ixNet.getList(topo2, 'deviceGroup')[0]
isisL3Router2 = ixNet.getList(deviceGroup2, 'isisL3Router')[0]
enableHostName2 = ixNet.getAttribute(isisL3Router2, '-enableHostName')
ixNet.setAttribute(enableHostName2 + '/singleValue', '-value', 'True')
ixNet.commit()
time.sleep(5)
configureHostName2 = ixNet.getAttribute(isisL3Router2, '-hostName')
ixNet.setAttribute(configureHostName2 + '/singleValue', '-value', 'isisL3Router2')
ixNet.commit

# Disable Discard Learned LSP
print("Disabling the Discard Learned Info CheckBox")
isisL3RouterDiscardLearnedLSP1 = ixNet.getAttribute(ixNet.getList(t1dev1, 'isisL3Router')[0], '-discardLSPs')
isisL3RouterDiscardLearnedLSP2 = ixNet.getAttribute(ixNet.getList(t2dev1, 'isisL3Router')[0], '-discardLSPs')

ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP1 + '/singleValue', '-value', 'False')

ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP2 + '/singleValue', '-value', 'False')

#print ('ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/isisL3\')')
#print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/isisL3'))

################################################################################
# 2.Enabling Segment Routing in Emulated Router                                #
################################################################################
print("Enabling Segment Routing for ISIS")
ixNet.setAttribute(isisL3Router1, '-enableSR', 'true')
ixNet.setAttribute(isisL3Router2, '-enableSR', 'true')
ixNet.commit()

################################################################################
# 3.Enabling SR-IPv6 Flag under Segnment Routing Tab in ISIS-L3 RTR
################################################################################
print("Enabling SR-IPv6 Flag under Segment Routing Tab")
sr_ipv6_flag1 = ixNet.getAttribute(isisL3Router1, '-ipv6Srh')
ixNet.setMultiAttribute(sr_ipv6_flag1  + '/singleValue', '-value', 'true')
ixNet.commit()
sr_ipv6_flag2 = ixNet.getAttribute(isisL3Router2, '-ipv6Srh')
ixNet.setMultiAttribute(sr_ipv6_flag2  + '/singleValue', '-value', 'true')
ixNet.commit()

################################################################################
# 4.Setting IPv6 Node Prefix Address
################################################################################
print("Setting IPv6 Node Prefix Address")
ipv6_node_prefix_add1 = ixNet.getAttribute(isisL3Router1, '-ipv6NodePrefix')
ixNet.setAttribute(ipv6_node_prefix_add1  + '/singleValue', '-value', '3000::1')
ixNet.commit()

ipv6_node_prefix_add2 = ixNet.getAttribute(isisL3Router1, '-ipv6NodePrefix')
ixNet.setAttribute(ipv6_node_prefix_add2  + '/singleValue', '-value', '4000::101')
ixNet.commit()

################################################################################
# 5.Enabling Adj-Sid under Segnment Routing Tab in ISIS-L3 IF
################################################################################
print("Enabling Adj-SID in first Emulated Router")
enableAdjSID1 = ixNet.getAttribute(isisL3_1, '-enableAdjSID')
ixNet.setAttribute(enableAdjSID1  + '/singleValue', '-value', 'true')
ixNet.commit()

print("Enabling Adj-SID in second Emulated Router")
enableAdjSID2 = ixNet.getAttribute(isisL3_2, '-enableAdjSID')
ixNet.setAttribute(enableAdjSID2  + '/singleValue', '-value', 'true')
ixNet.commit()

print("Set IPv6 Adj-SID value in first Emulated Router")
ipv6SidValue1 =ixNet.getAttribute(isisL3_1, '-ipv6SidValue')
ixNet.setAttribute(ipv6SidValue1  + '/singleValue', '-value', '5000::1')
ixNet.commit()

print("Set IPv6 Adj-SID value in second Emulated Router")
ipv6SidValue2 = ixNet.getAttribute(isisL3_2, '-ipv6SidValue')
ixNet.setAttribute(ipv6SidValue2  + '/singleValue', '-value', '6000::1')
ixNet.commit()

print("Adding Network Group behind ISIS Device Group2")
ixNet.execute('createDefaultStack', t2devices, 'networkTopology')
time.sleep(5)
networkGroup1 =ixNet.getList(t2dev1, 'networkGroup')[0]
networkGroup2 = ixNet.add(t2dev1, 'networkGroup')
ixNet.setAttribute(networkGroup1, '-name', 'ISIS_Network_Group1')
ixNet.commit()

print("Adding IPv6 Prefix Pool behind ISIS Device Group2")
ipv6PrefixPools = ixNet.add(networkGroup2, 'ipv6PrefixPools')
time.sleep(2)
ixNet.commit()
ixNet.setAttribute(networkGroup2, '-multiplier', '1')
ixNet.commit()
ixNet.setAttribute(networkGroup2, '-name', 'ISIS_IPv6_Prefix_Pools')
ixNet.commit()

print("Enabling Advertise IPv6 SID under IPv6 PrefixPool")
isisL3RouteProperty = ixNet.add(ipv6PrefixPools, 'isisL3RouteProperty')
ipv6Srh = ixNet.getAttribute(isisL3RouteProperty, '-ipv6Srh')
ixNet.setAttribute(ipv6Srh  + '/singleValue', '-value', 'True')
ixNet.commit()

################################################################################
# 4.Enabling Segment Routing in simulated router
################################################################################
print("Enabling Segment Routing in Simulated Routers on Network Group behind Device Group2")
networkTopo1 = ixNet.getList(networkGroup1, 'networkTopology')[0]
simRouter1 =ixNet.getList(networkTopo1, 'simRouter')[0]
isisPseudoRouter1 =ixNet.getList(simRouter1, 'isisL3PseudoRouter')[0]
ixNet.setAttribute(isisPseudoRouter1, '-enableSR', 'true')
ixNet.commit()

print("Enabling SR-IPv6 Flag in Simulated Routers on Network Group behind Device Group2")
sr_ipv6_flag1 = ixNet.getAttribute(isisPseudoRouter1, '-ipv6Srh')
ixNet.setAttribute(sr_ipv6_flag1 + '/singleValue', '-value', 'true')
ixNet.commit()

print("Setting IPv6 Node Prefix Address in Simulated Routers on Network Group behind Device Group2")

ipv6_node_prefix_add1 =ixNet.getAttribute(isisPseudoRouter1, '-ipv6NodePrefix')
svSID2 = ixNet.add(ipv6_node_prefix_add1, 'singleValue')
ixNet.setAttribute(svSID2, '-value', '7000::1')
ixNet.commit()

print("Enabling Adj-Sid in Simulated Interface on Network Group behind Device Group2")
networkTopo1 = ixNet.getList(networkGroup1, 'networkTopology')[0]
simInterface1 = ixNet.getList(networkTopo1, 'simInterface')[0]
isisL3PseudoInterface1 = ixNet.getList(simInterface1, 'isisL3PseudoInterface')[0]

adj_sid = ixNet.getAttribute(isisL3PseudoInterface1, '-enableAdjSID')
ixNet.setAttribute(adj_sid + '/singleValue', '-value', 'true')
ixNet.commit()

print("Set IPv6 Adj-SID value for Simulated Interface")
ipv6SidValue1 = ixNet.getAttribute(isisL3PseudoInterface1, '-ipv6SidValue')
svAdjSID2 = ixNet.add(ipv6SidValue1, 'singleValue')
ixNet.setAttribute(svAdjSID2, '-value', '8000::1')
ixNet.commit()

################################################################################
# 5. Start ISIS protocol and wait for 60 seconds
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)

################################################################################
# Retrieve protocol statistics.
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
# 7. Retrieve protocol learned info in Port 1
###############################################################################
print("Fetching ISIS SR IPv6 Prefix Learned Info in Port 1\n")
ixNet.execute('getLearnedInfo', isisL3_1, '1')
time.sleep(5)
linfo = ixNet.getList(isisL3_1, 'learnedInfo')[0]
ipv6table = ixNet.getList(linfo, 'table')[2]
values    = ixNet.getAttribute(ipv6table, '-values')
	 
print("***************************************************\n")
for v in values:
    print(v)
# end for
print("***************************************************")

print("Fetching ISIS SR IPv6 Adjacency Learned Info in Port 1\n")
ixNet.execute('getLearnedInfo', isisL3_1, '1')
time.sleep(5)
linfo = ixNet.getList(isisL3_1, 'learnedInfo')[0]
ipv6table = ixNet.getList(linfo, 'table')[3]
values    = ixNet.getAttribute(ipv6table, '-values')
	 
print("***************************************************\n")
for v in values:
    print(v)
# end for
print("***************************************************")

################################################################################
# 9. Setting on the fly change of IPv6 Node Prefix Address in Simulated Router
################################################################################
print("Disabling Adj-Sid on the fly \n")
ipv6SidValue1 = ixNet.getAttribute(isisL3PseudoInterface1, '-enableAdjSID')
ixNet.setAttribute(ipv6SidValue1  + '/singleValue', '-value', 'false')
ixNet.commit()

globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")
# end try/expect
print("Wait for 30 seconds ...")
time.sleep(5)

###############################################################################
# 10. Retrieve protocol learned info
###############################################################################
print("Fetching ISIS SR IPv6 Adjacency Learned Info in Port 1\n")
ixNet.execute('getLearnedInfo', isisL3_1, '1')
time.sleep(5)
linfo = ixNet.getList(isisL3_1, 'learnedInfo')[0]
ipv6table = ixNet.getList(linfo, 'table')[3]
values    = ixNet.getAttribute(ipv6table, '-values')
	 
print("***************************************************\n")
for v in values:
    print(v)
# end for
print("***************************************************")

################################################################################
# Stop all protocols                                                           #
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
