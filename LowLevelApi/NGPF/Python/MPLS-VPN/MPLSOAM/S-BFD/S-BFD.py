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
#   This script intends to demonstrate how to use NGPF S-BFD using Python      #               					                               
#                                                                              #
#    1. Configuration of protocols as described in topology.                   #
#    2. Start all protocols.                                                   #
#    3. Retrieve protocol statistics and check Learned Information             #
#    4. Deactivate the first initiator OTF                                     #
#    5. Retrieve protocol statistics check Learned Information again.          #
#    6. Deactivate the first initiator OTF                                     #
#    7. Retrieve protocol statistics again                                     #
#    8. Change the discrminator of the first responder OTF                     #
#    9. Retrieve protocol statistics again.                                    #
#   10. Stop all protocols.                                                    #                                                                                
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
ixTclServer = '10.39.50.134'
ixTclPort   = '8998'
ports       = [('10.39.50.126', '1', '9',), ('10.39.50.126', '1', '13',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.60', '-setAttribute', 'strict')
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
    '-start',     '00:11:01:00:00:01',
    '-step',      '00:00:00:00:00:01')

ixNet.setMultiAttribute(ixNet.getAttribute(mac2, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '00:12:01:00:00:01',
    '-step',      '00:00:00:00:00:01')
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
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '20.20.20.2')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '20.20.20.2')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '20.20.20.1')

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

# Adding ISIS over Ethernet stack
print("Adding ISISl3 over Ethernet stacks")
ixNet.add(mac1, 'isisL3')
ixNet.add(mac2, 'isisL3')
ixNet.commit()

isisL3_1 = ixNet.getList(mac1, 'isisL3')[0]
isisL3_2 = ixNet.getList(mac2, 'isisL3')[0]


print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'S-BFD Inititator Topology')
ixNet.setAttribute(topo2, '-name', 'S-BFD Responder Topology')

ixNet.commit()



# Adding Network group behind DeviceGroup
print("Adding NetworkGroup behind ISISL3 DG")

ixNet.add(t1dev1, 'networkGroup')
ixNet.add(t2dev1, 'networkGroup')
ixNet.commit()

networkGroup1 = ixNet.getList(t1dev1, 'networkGroup')[0]
networkGroup2 = ixNet.getList(t2dev1, 'networkGroup')[0]
ixNet.commit()

ixNet.setAttribute(networkGroup1, '-multiplier', '1')
ixNet.setAttribute(networkGroup2, '-multiplier', '1')
ixNet.commit()


print("Configuring network topology in the network group")

ixNet.add(networkGroup1, 'networkTopology')
ixNet.add(networkGroup2, 'networkTopology')
ixNet.commit()

nt1 = ixNet.getList(networkGroup1, 'networkTopology')[0]
nt2 = ixNet.getList(networkGroup2, 'networkTopology')[0]

ixNet.commit()
ixNet.add(nt1, 'netTopologyLinear')
ixNet.add(nt2, 'netTopologyLinear')
ixNet.commit()

nt11 = ixNet.getList(nt1, 'netTopologyLinear')[0]
nt12 = ixNet.getList(nt2, 'netTopologyLinear')[0]


ixNet.setAttribute(nt11, '-nodes', '150')
ixNet.setAttribute(nt12, '-nodes', '150')
ixNet.commit()

print("Enabling segment routing and ocnfiguring Node prefix and labels")

ixNet.add(nt1, 'simRouter')
ixNet.add(nt2, 'simRouter')
ixNet.commit()

simRouter1 = ixNet.getList(nt1, 'simRouter')[0]
simRouter2 = ixNet.getList(nt2, 'simRouter')[0]


ixNet.add(simRouter1, 'isisL3PseudoRouter')
ixNet.add(simRouter2, 'isisL3PseudoRouter')
ixNet.commit()

simRouter1 = ixNet.getList(simRouter1, 'isisL3PseudoRouter')[0]
simRouter2 = ixNet.getList(simRouter2, 'isisL3PseudoRouter')[0]

print("Enabling Segment Routing")
ixNet.setAttribute(simRouter2, '-enableSR', 'true')
ixNet.commit()

nodePrefix1 = ixNet.getAttribute(simRouter2, '-nodePrefix')
ixNet.setMultiAttribute(nodePrefix1, '-clearOverlays', 'false', '-pattern', 'counter')
counter1 = ixNet.add(nodePrefix1, 'counter')
ixNet.setMultiAttribute(counter1, '-step', '0.0.0.1', '-start', '2.2.2.2', '-direction', 'increment')
ixNet.commit()

sIDIndexLabel1 = ixNet.getAttribute(simRouter2, '-sIDIndexLabel')
ixNet.setMultiAttribute(sIDIndexLabel1, '-clearOverlays', 'false', '-pattern', 'counter')
counter2 = ixNet.add(sIDIndexLabel1, 'counter')
ixNet.setMultiAttribute(counter2, '-step', '1', '-start', '1', '-direction', 'increment')
ixNet.commit()



print("Adding Device Group behind Network Groups")
ixNet.add(networkGroup1, 'deviceGroup')
ixNet.add(networkGroup2, 'deviceGroup')
ixNet.commit()

t1dev2 = ixNet.getList(networkGroup1, 'deviceGroup')[0]
t2dev2 = ixNet.getList(networkGroup2, 'deviceGroup')[0]

print("Configuring the multipliers")
ixNet.setAttribute(t1dev2, '-multiplier', '150')
ixNet.setAttribute(t2dev2, '-multiplier', '150')
ixNet.commit()

ixNet.setAttribute(t1dev2, '-name', 'Inititator')
ixNet.setAttribute(t2dev2, '-name', 'Responder')
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
ixNet.setMultiAttribute(counter1, '-step', '0.0.0.1', '-start', '1.1.1.1', '-direction', 'increment')
ixNet.setMultiAttribute(counter2, '-step', '0.0.0.1', '-start', '2.2.2.2', '-direction', 'increment')
ixNet.commit()

print("Adding mplsoam on the loopback interface of both topologies")
ixNet.add(ipv4Loopback1, 'mplsOam')
ixNet.add(ipv4Loopback2, 'mplsOam')
ixNet.commit()

mplsoam1 = ixNet.getList(ipv4Loopback1, 'mplsOam')[0]
mplsoam2 = ixNet.getList(ipv4Loopback2, 'mplsOam')[0]


ipv4Loopback1 = ixNet.getList(t1dev2, 'ipv4Loopback')[0]
ipv4Loopback2 = ixNet.getList(t2dev2, 'ipv4Loopback')[0]


ixNet.setAttribute(mplsoam2, '-enableSBfdResponder', 'true')
ixNet.setAttribute(mplsoam1, '-initiatorSBFDSessionCount', '1')

ixNet.commit()

ixNet.add(mplsoam1, 'sbfdInitiator')

ixNet.commit()

sbfdinit = ixNet.getList(mplsoam1, 'sbfdInitiator')[0]
ixNet.commit()

peerDisc = ixNet.getAttribute(sbfdinit, '-peerDiscriminator')
ixNet.setMultiAttribute(peerDisc, '-clearOverlays', 'false', '-pattern', 'counter')
counter3 = ixNet.add(peerDisc, 'counter')
ixNet.setMultiAttribute(counter3, '-step', '1', '-start', '1', '-direction', 'increment')
ixNet.commit()

ixNet.add(sbfdinit, 'mplsLabelList')

ixNet.commit()

sbflabel = ixNet.getList(sbfdinit, 'mplsLabelList')[0]

label = ixNet.getAttribute(sbflabel, '-mplsLabel')
ixNet.setMultiAttribute(label, '-clearOverlays', 'false', '-pattern', 'counter')
counter4 = ixNet.add(label, 'counter')
ixNet.setMultiAttribute(counter4, '-step', '1', '-start', '16001', '-direction', 'increment')
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
# Retrieve protocol learned info                                              # 
###############################################################################
print("Fetching MPLSOAM learned info")
ixNet.execute('getAllLearnedInfo', mplsoam1, '3')
time.sleep(5)
linfo  = ixNet.getList(mplsoam1, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")



################################################################################
# 3.Deactivating the 1st initiator OTF
################################################################################
print("Deactivating the 1st initiator OTF")

active = ixNet.getAttribute(sbfdinit, '-active')
overlay1 = ixNet.add(active, 'overlay')
ixNet.setMultiAttribute(overlay1, '-index', 1, '-value', 'false')
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
# 4. Retrieve protocol statistics again and compare with
#    previouly retrieved statistics.
###############################################################################

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
# Retrieve protocol learned info                                              # 
###############################################################################
print("Fetching MPLSOAM learned info")
ixNet.execute('getAllLearnedInfo', mplsoam1, '3')
time.sleep(5)
linfo  = ixNet.getList(mplsoam1, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# 5.Activating the 1st initiator OTF
################################################################################
print("Activating the 1st initiator OTF")

active2 = ixNet.getAttribute(sbfdinit, '-active')
overlay2 = ixNet.add(active2, 'overlay')
ixNet.setMultiAttribute(overlay2, '-index', 1, '-value', 'true')
ixNet.commit()

globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")
# end try/expect
time.sleep(30)

###############################################################################
# 6. Retrieve protocol statistics again and compare with
#    previouly retrieved statistics.
###############################################################################

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
time.sleep(5)

################################################################################
# 7. Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
