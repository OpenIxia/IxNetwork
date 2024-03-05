#/usr/bin/tclsh

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
# damages limitations forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use L3vpn Over SRv6 TCL APIs.   #
#                                                                              #
#    1. It will create 2 ISISL3 topologies, each having an ipv6 network        #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. L3vpn configure behind IPv6 Loopback.        #
#       IPv4 NG  configured begind L3vpn DG which is used to generate traffic. # 
#    2. Start the ISISL3 protocol.                                             #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Start the L2-L3 traffic.                                               #
#    6. Retrieve L2-L3 traffic stats.                                          #
#    7. Stop L2-L3 traffic.                                                    #
#    8. Stop all protocols.                                                    #                                                                                          
################################################################################

# Script Starts
print "!!! Test Script Starts !!!"
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
ixTclServer = '10.39.43.12'
ixTclPort   = '8009'
ports       = [('10.39.50.122', '1', '1',), ('10.39.50.122', '1', '2',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.50',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

################################################################################
# 1. Protocol configuration section. Configure OSPFv3 as per the description
#    give above
################################################################################ 
root = ixNet.getRoot()
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

print ("Adding 2 vports")
vportTx = ixNet.getList(root, 'vport')[0]
vportRx = ixNet.getList(root, 'vport')[1]

print "Adding 2 topologies"
print("adding topologies")
ixNet.add(root, 'topology', '-vports', vportTx)
ixNet.add(root, 'topology', '-vports', vportRx)
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

print ('Renaming the topologies and the device groups')
ixNet.setAttribute(topo1, '-name', 'Egress Topology: Sender')
ixNet.setAttribute(topo2, '-name', 'Ingress Topology: Receiver')

print "Adding 2 device groups"
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices [0]
t2dev1 = t2devices [0]

ixNet.setAttribute(t1dev1, '-name', 'Sender PE Router')
ixNet.setAttribute(t2dev1, '-name', 'Receiver PE Router')
ixNet.commit()
print "Configuring the multipliers (number of sessions)"
ixNet.setAttribute(t1dev1, '-multiplier', '1')
ixNet.setAttribute(t2dev1, '-multiplier', '1')
ixNet.commit()

print "Adding ethernet/mac endpoints"
ixNet.add(t1dev1, 'ethernet')
ixNet.add(t2dev1, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = ixNet.getList(t2dev1, 'ethernet')[0]

print "Configuring the mac addresses"
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '00:11:01:00:00:01',
    '-step',     '00:00:00:00:00:01')

ixNet.setMultiAttribute(ixNet.getAttribute(mac2, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '00:12:01:00:00:01',
    '-step',     '00:00:00:00:00:01')
ixNet.commit()

print "Add ipv6"
ixNet.add(mac1, 'ipv6')
ixNet.add(mac2, 'ipv6')
ixNet.commit()

ip1 = ixNet.getList(mac1, 'ipv6')[0]
ip2 = ixNet.getList(mac2, 'ipv6')[0]
mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvAdd2 = ixNet.getAttribute(ip2, '-address')
mvGw1  = ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = ixNet.getAttribute(ip2, '-gatewayIp')

print "configuring ipv6 addresses"
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '2000:0:0:1:0:0:0:1')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '2000:0:0:1:0:0:0:2')
ixNet.setAttribute(mvGw1 + '/singleValue',  '-value', '2000:0:0:1:0:0:0:2')
ixNet.setAttribute(mvGw2 + '/singleValue',  '-value', '2000:0:0:1:0:0:0:1')


#ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '64')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '64')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()
print "Adding isisL3 over IPv6 stacks"
ixNet.add(mac1, 'isisL3')
ixNet.add(mac2, 'isisL3')
ixNet.commit()

isisL3_1 = (ixNet.getList(mac1, 'isisL3'))[0]
isisL3_2 = (ixNet.getList(mac2, 'isisL3'))[0]

print "Renaming the topologies and the device groups"
ixNet.setAttribute(topo1, '-name', 'isisL3 Topology 1')
ixNet.setAttribute(topo2, '-name', 'isisL3 Topology 2')

ixNet.setAttribute(t1dev1, '-name', 'isisL3 Topology 1 Router')
ixNet.setAttribute(t2dev1, '-name', 'isisL3 Topology 2 Router')
ixNet.commit()

#Change the property of ISIS-L3
print "Change the Property of ISIS-L3"
Network_Type_1 = ixNet.getAttribute(isisL3_1, '-networkType')
ixNet.setMultiAttribute(Network_Type_1, '-clearOverlays', 'false')
ixNet.commit()
singleValue_1 = ixNet.add(Network_Type_1, 'singleValue')
ixNet.setMultiAttribute(singleValue_1, '-value', 'pointpoint')
ixNet.commit()
Network_Type_1 = ixNet.getAttribute(isisL3_2, '-networkType')
ixNet.setMultiAttribute(Network_Type_1, '-clearOverlays', 'false')
ixNet.commit()
singleValue_1 = ixNet.add(Network_Type_1, 'singleValue')
ixNet.setMultiAttribute(singleValue_1, '-value', 'pointpoint')
ixNet.commit()
#Change the value of fFlag
print "Change the value F Flag"
f_Flag_1 = ixNet.getAttribute(isisL3_1, '-fFlag')
ixNet.setMultiAttribute(f_Flag_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(f_Flag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
f_Flag_1 = ixNet.getAttribute(isisL3_2, '-fFlag')
ixNet.setMultiAttribute(f_Flag_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(f_Flag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Change the value', 'of, '-enableIPv6SID
print "Change the valueenableIPv6SID"
enableIPv6SID_1 = ixNet.getAttribute(isisL3_1, '-enableIPv6SID')
ixNet.setMultiAttribute(enableIPv6SID_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(enableIPv6SID_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
enableIPv6SID_1 = ixNet.getAttribute(isisL3_2, '-enableIPv6SID')
ixNet.setMultiAttribute(enableIPv6SID_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(enableIPv6SID_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Change the value', 'of, '-ipv6SidValue
print "Change the value ipv6SidValue"
ipv6SidValue_1 = ixNet.getAttribute(isisL3_1, '-ipv6SidValue')
ixNet.setMultiAttribute(ipv6SidValue_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv6SidValue_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '3333::1')
ixNet.commit()
ipv6SidValue_1 = ixNet.getAttribute(isisL3_2, '-ipv6SidValue')
ixNet.setMultiAttribute(ipv6SidValue_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv6SidValue_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '4444::1')
ixNet.commit()
#Change the value of srv6SidFlags
print "Change the value srv6SidFlags"
srv6SidFlags_1 = ixNet.getAttribute(isisL3_1, '-srv6SidFlags')
ixNet.setMultiAttribute(srv6SidFlags_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(srv6SidFlags_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'cd')
ixNet.commit()
srv6SidFlags_1 = ixNet.getAttribute(isisL3_2, '-srv6SidFlags')
ixNet.setMultiAttribute(srv6SidFlags_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(srv6SidFlags_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'ef')
ixNet.commit()
#Change the value', 'of discardLSPs
print "Change the value discardLSPs"
isisRtr_1 = ixNet.getList(t1dev1, 'isisL3Router')[0]
#discardLSPs_1 = ixNet.getAttribute(('t1dev1' + '/isisL3Router:1'), '-discardLSPs')
discardLSPs_1 = ixNet.getAttribute(isisRtr_1, '-discardLSPs')
ixNet.setMultiAttribute(discardLSPs_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(discardLSPs_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()
isisRtr_2 = ixNet.getList(t2dev1, 'isisL3Router')[0]
#discardLSPs_1 = ixNet.getAttribute('t2dev1' + '/isisL3Router:1', '-discardLSPs')
discardLSPs_2 = ixNet.getAttribute(isisRtr_2, '-discardLSPs')
ixNet.setMultiAttribute(discardLSPs_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(discardLSPs_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()
#Enable of enableWideMetric
print "Enable the enableWideMetric"
#enableWideMetric_1 = ixNet.getAttribute('t1dev1' + '/isisL3Router:1', '-enableWideMetric')
enableWideMetric_1 = ixNet.getAttribute(isisRtr_1, '-enableWideMetric')
ixNet.setMultiAttribute(enableWideMetric_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(enableWideMetric_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#enableWideMetric_1 = ixNet.getAttribute('t2dev1' + '/isisL3Router:1', '-enableWideMetric')
enableWideMetric_1 = ixNet.getAttribute(isisRtr_2, '-enableWideMetric')
ixNet.setMultiAttribute(enableWideMetric_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(enableWideMetric_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Enable Segment Routing
print "Enable Segment routing"
ixNet.setMultiAttribute(isisRtr_1,
	'-enableSR', 'true',
	'-name', 'ISIS-L3 RTR 1')
ixNet.commit()
ixNet.setMultiAttribute (isisRtr_2,
	'-enableSR', 'true',
	'-name', 'ISIS-L3 RTR 1')
ixNet.commit()
#Enable the DBit
print "Enable the sBit"
dBit_1 = ixNet.getAttribute(isisRtr_1, '-dBit')
ixNet.setMultiAttribute(dBit_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(dBit_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
dBit_1 = (ixNet.getAttribute(isisRtr_2, '-dBit'))
ixNet.setMultiAttribute(dBit_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = (ixNet.add(dBit_1, 'singleValue'))
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Enable the SBit
print "Enabling the SBit"
sBit_1 = ixNet.getAttribute(isisRtr_1, '-sBit')
ixNet.setMultiAttribute(sBit_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(sBit_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
sBit_1 = ixNet.getAttribute(isisRtr_2, '-sBit')
ixNet.setMultiAttribute(sBit_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(sBit_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Enable the ipv6Flag
print "Enabling the ipv6Flag"
ipv6Flag_1 = ixNet.getAttribute(isisRtr_1, '-ipv6Flag')
ixNet.setMultiAttribute(ipv6Flag_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv6Flag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()
ipv6Flag_1 = ixNet.getAttribute(isisRtr_2, '-ipv6Flag')
ixNet.setMultiAttribute(ipv6Flag_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv6Flag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()
#Enable the ipv4Flag
print "Enabling the ipv4Flag"
ipv4Flag_1 = ixNet.getAttribute(isisRtr_1, '-ipv4Flag')
ixNet.setMultiAttribute(ipv4Flag_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv4Flag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()
ipv4Flag_1 = ixNet.getAttribute(isisRtr_2, '-ipv4Flag')
ixNet.setMultiAttribute(ipv4Flag_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv4Flag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()
#Enable the configureSIDIndexLabel
print "Enabling the configureSIDIndexLabel"
configureSIDIndexLabel_1 = ixNet.getAttribute(isisRtr_1, '-configureSIDIndexLabel')
ixNet.setMultiAttribute(configureSIDIndexLabel_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(configureSIDIndexLabel_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()
configureSIDIndexLabel_1 = ixNet.getAttribute(isisRtr_2, '-configureSIDIndexLabel')
ixNet.setMultiAttribute(configureSIDIndexLabel_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(configureSIDIndexLabel_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()
#Enable the ipv6Srh means Enable SR-IPv6
print "Enabling the ipv6Srh means Enable SR-IPv6"
ipv6Srh_1 = ixNet.getAttribute(isisRtr_1, '-ipv6Srh')
ixNet.setMultiAttribute(ipv6Srh_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv6Srh_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
ipv6Srh_1 = ixNet.getAttribute(isisRtr_2, '-ipv6Srh')
ixNet.setMultiAttribute(ipv6Srh_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv6Srh_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Enable the oFlagOfSRv6CapTlv
print "Enabling the oFlagOfSRv6CapTlv"
oFlagOfSRv6CapTlv_1 = ixNet.getAttribute(isisRtr_1, '-oFlagOfSRv6CapTlv')
ixNet.setMultiAttribute(oFlagOfSRv6CapTlv_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(oFlagOfSRv6CapTlv_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
oFlagOfSRv6CapTlv_1 = ixNet.getAttribute(isisRtr_2, '-oFlagOfSRv6CapTlv')
ixNet.setMultiAttribute(oFlagOfSRv6CapTlv_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(oFlagOfSRv6CapTlv_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Enable the eFlagOfSRv6CapTlv
print "Enabling the eFlagOfSRv6CapTlv"
eFlagOfSRv6CapTlv_1 = ixNet.getAttribute(isisRtr_1, '-eFlagOfSRv6CapTlv')
ixNet.setMultiAttribute(eFlagOfSRv6CapTlv_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(eFlagOfSRv6CapTlv_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
eFlagOfSRv6CapTlv_1 = ixNet.getAttribute(isisRtr_2, '-eFlagOfSRv6CapTlv')
ixNet.setMultiAttribute(eFlagOfSRv6CapTlv_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(eFlagOfSRv6CapTlv_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Enable the sBitForSRv6Cap
print "Enabling the sBitForSRv6Cap"
sBitForSRv6Cap_1 = ixNet.getAttribute(isisRtr_1, '-sBitForSRv6Cap')
ixNet.setMultiAttribute(sBitForSRv6Cap_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(sBitForSRv6Cap_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
sBitForSRv6Cap_1 = ixNet.getAttribute(isisRtr_2, '-sBitForSRv6Cap')
ixNet.setMultiAttribute(sBitForSRv6Cap_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(sBitForSRv6Cap_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Enable the dBitForSRv6Cap
print "Enabling the dBitForSRv6Cap"
dBitForSRv6Cap_1 = ixNet.getAttribute(isisRtr_1, '-dBitForSRv6Cap')
ixNet.setMultiAttribute(dBitForSRv6Cap_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(dBitForSRv6Cap_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
dBitForSRv6Cap_1 = ixNet.getAttribute(isisRtr_2, '-dBitForSRv6Cap')
ixNet.setMultiAttribute(dBitForSRv6Cap_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(dBitForSRv6Cap_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Enable the reservedInsideSRv6CapFlag
print "Enabling the reservedInsideSRv6CapFlag"
reservedInsideSRv6CapFlag_1 = ixNet.getAttribute(isisRtr_1, '-reservedInsideSRv6CapFlag')
ixNet.setMultiAttribute(reservedInsideSRv6CapFlag_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(reservedInsideSRv6CapFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '3fff')
ixNet.commit()
reservedInsideSRv6CapFlag_1 = ixNet.getAttribute(isisRtr_2, '-reservedInsideSRv6CapFlag')
ixNet.setMultiAttribute(reservedInsideSRv6CapFlag_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(reservedInsideSRv6CapFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '2fff')
ixNet.commit()
#Enable the includeMaximumEndDSrhTLV
print "Enabling the includeMaximumEndDSrhTLV"
includeMaximumEndDSrhTLV_1 = ixNet.getAttribute(isisRtr_1, '-includeMaximumEndDSrhTLV')
ixNet.setMultiAttribute(includeMaximumEndDSrhTLV_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(includeMaximumEndDSrhTLV_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
includeMaximumEndDSrhTLV_1 = ixNet.getAttribute(isisRtr_2, '-includeMaximumEndDSrhTLV')
ixNet.setMultiAttribute(includeMaximumEndDSrhTLV_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(includeMaximumEndDSrhTLV_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Enable the includeMaximumEndPopSrhTLV
print "Enabling the includeMaximumEndPopSrhTLV"
includeMaximumEndPopSrhTLV_1 = ixNet.getAttribute(isisRtr_1, '-includeMaximumEndPopSrhTLV')
ixNet.setMultiAttribute(includeMaximumEndPopSrhTLV_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(includeMaximumEndPopSrhTLV_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
includeMaximumEndPopSrhTLV_1 = ixNet.getAttribute(isisRtr_2, '-includeMaximumEndPopSrhTLV')
ixNet.setMultiAttribute(includeMaximumEndPopSrhTLV_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(includeMaximumEndPopSrhTLV_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Enable the includeMaximumSLTLV
print "Enabling the includeMaximumSLTLV"
includeMaximumSLTLV_1 = ixNet.getAttribute(isisRtr_1, '-includeMaximumSLTLV')
ixNet.setMultiAttribute(includeMaximumSLTLV_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(includeMaximumSLTLV_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
includeMaximumSLTLV_1 = ixNet.getAttribute(isisRtr_2, '-includeMaximumSLTLV')
ixNet.setMultiAttribute(includeMaximumSLTLV_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(includeMaximumSLTLV_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Enable the includeMaximumTEncapSrhTLV
print "Enabling the includeMaximumTEncapSrhTLV"
includeMaximumTEncapSrhTLV_1 = ixNet.getAttribute(isisRtr_1, '-includeMaximumTEncapSrhTLV')
ixNet.setMultiAttribute(includeMaximumTEncapSrhTLV_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(includeMaximumTEncapSrhTLV_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
includeMaximumTEncapSrhTLV_1 = ixNet.getAttribute(isisRtr_2, '-includeMaximumTEncapSrhTLV')
ixNet.setMultiAttribute(includeMaximumTEncapSrhTLV_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(includeMaximumTEncapSrhTLV_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Enable the includeMaximumTInsertSrhTLV
print "Enabling the includeMaximumTInsertSrhTLV"
includeMaximumTInsertSrhTLV_1 = ixNet.getAttribute(isisRtr_1, '-includeMaximumTInsertSrhTLV')
ixNet.setMultiAttribute(includeMaximumTInsertSrhTLV_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(includeMaximumTInsertSrhTLV_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
includeMaximumTInsertSrhTLV_1 = ixNet.getAttribute(isisRtr_2, '-includeMaximumTInsertSrhTLV')
ixNet.setMultiAttribute(includeMaximumTInsertSrhTLV_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(includeMaximumTInsertSrhTLV_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
#Enable the dBitForSRv6Cap
print "Enabling the dBitForSRv6Cap"
dBitInsideSRv6SidTLV_1 = ixNet.getAttribute(isisRtr_1, '-dBitInsideSRv6SidTLV')
ixNet.setMultiAttribute(dBitInsideSRv6SidTLV_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(dBitInsideSRv6SidTLV_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
dBitInsideSRv6SidTLV_1 = ixNet.getAttribute(isisRtr_2, '-dBitInsideSRv6SidTLV')
ixNet.setMultiAttribute(dBitInsideSRv6SidTLV_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(dBitInsideSRv6SidTLV_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
IPv6_LoopBack = ixNet.add(t1dev1, 'networkGroup')
ixNet.setMultiAttribute(IPv6_LoopBack,
	'-name', 'IPv6_LoopBack_Address')
ixNet.commit()
IPv6_LoopBack = ixNet.remapIds(IPv6_LoopBack)[0]
ipv6PrefixPools = ixNet.add(IPv6_LoopBack, 'ipv6PrefixPools')
ixNet.setMultiAttribute(ipv6PrefixPools,
	'-addrStepSupported', 'true',
	'-name', 'BasicIPv6Addresses1')
ixNet.commit()
ipv6PrefixPools = ixNet.remapIds(ipv6PrefixPools)[0]
Connector = ixNet.add(ipv6PrefixPools, 'connector')
ixNet.setMultiAttribute(Connector,
	'-connectedTo', 'mac1')
ixNet.commit()
networkAddress = ixNet.getAttribute(ipv6PrefixPools, '-networkAddress')
ixNet.setMultiAttribute(networkAddress, '-clearOverlays', 'false')
ixNet.commit()
counter_networkAddress = ixNet.add(networkAddress, 'counter')
ixNet.setMultiAttribute(counter_networkAddress,
	'-step', '::0.0.0.1',
	'-start', '1111::1',
	'-direction', 'increment')
ixNet.commit()
#Create Network Group At PEER2 Side
networkGroup_P2 = ixNet.add(t2dev1, 'networkGroup')
ixNet.setMultiAttribute(networkGroup_P2,
	'-name', 'Routers')
ixNet.commit()
networkGroup_P2 = ixNet.remapIds(networkGroup_P2)[0]
Network_Topology = ixNet.add(networkGroup_P2, 'networkTopology')
ixNet.commit()
Network_Topology = ixNet.remapIds(Network_Topology)[0]
netTopologyCustom = ixNet.add(Network_Topology, 'netTopologyCustom')
ixNet.commit()
netTopologyCustom = ixNet.remapIds(netTopologyCustom)[0]
ixNet.setMultiAttribute(netTopologyCustom + '/linkTable',
	'-fromNodeIndex', ['5','5','1','1','6','6','2','2','9','9','9','9'], 
    '-toNodeIndex', ['3','7','0','3','4','8','0','4','1','5','2','6'])
ixNet.setMultiAttribute(Network_Topology + '/simInterface:1',
	'-name', 'Simulated Interfaces 1')
ixNet.setMultiAttribute(Network_Topology + '/simInterface:1' + '/simInterfaceIPv4Config:1',
	'-name', 'Simulated Link IPv4 Address 1')
ixNet.commit()
#Enable the F Flag of SR-MPLS of Network Topology
fFlag_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/isisL3PseudoInterface:1', '-fFlag')
ixNet.setMultiAttribute(fFlag_1, '-clearOverlays', 'false')
ixNet.commit()
Single_Value_1 = ixNet.add(fFlag_1, 'singleValue')
ixNet.setMultiAttribute(Single_Value_1, '-value', 'true')
ixNet.commit()
#Enable the enableWideMetric of SR-MPLS of Simulated Interfaces of Network Topology
enableWideMetric = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1', '-enableWideMetric')
ixNet.setMultiAttribute(enableWideMetric, '-clearOverlays', 'false')
ixNet.commit()
Single_Value_1 = ixNet.add(enableWideMetric, 'singleValue')
ixNet.setMultiAttribute(Single_Value_1, '-value', 'true')
ixNet.commit()
#Enable the enableSR/IPv4/IPv6/configureSIDIndexLabel of Simulated Bridge of Network Topology
ixNet.setMultiAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1', '-enableSR', 'true')
ixNet.commit()
ipv4Flag = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1', '-ipv4Flag')
ixNet.setMultiAttribute(ipv4Flag, '-clearOverlays', 'false')
ixNet.commit()
Single_Value_1 = ixNet.add(ipv4Flag, 'singleValue')
ixNet.setMultiAttribute(Single_Value_1, '-value', 'false')
ixNet.commit()
ipv6Flag = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1', '-ipv6Flag')
ixNet.setMultiAttribute(ipv6Flag, '-clearOverlays', 'false')
ixNet.commit()
Single_Value_1 = ixNet.add(ipv6Flag, 'singleValue')
ixNet.setMultiAttribute(Single_Value_1, '-value', 'false')
ixNet.commit()
configureSIDIndexLabel = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1',
'-configureSIDIndexLabel')
ixNet.setMultiAttribute(configureSIDIndexLabel, '-clearOverlays', 'false')
ixNet.commit()
Single_Value_1 = ixNet.add(configureSIDIndexLabel, 'singleValue')
ixNet.setMultiAttribute(Single_Value_1, '-value', 'false')
ixNet.commit()
#The value for the IPv6 Node SID
ipv6NodePrefix = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1', '-ipv6NodePrefix')
ixNet.setMultiAttribute(ipv6NodePrefix, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(ipv6NodePrefix, 'counter')
ixNet.setMultiAttribute(counter,
            '-step', '1::',
            '-start', '7001::1',
            '-direction', 'increment')
ixNet.commit()
#Enable the filed of', 'Enable SR-IPv6"
ipv6Srh = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1', '-ipv6Srh')
ixNet.setMultiAttribute(ipv6Srh, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(ipv6Srh, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
#Change the Network Address of ISIS Simulated IPv6 Node Routers of Simulated Bridge
networkAddress = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1',
'-networkAddress')
ixNet.setMultiAttribute(networkAddress, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(networkAddress, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '2222::1')
ixNet.commit()
singleValue = ixNet.remapIds(singleValue)[0]
ixNet.setMultiAttribute(networkAddress + '/nest:1', '-enabled', 'false',
            '-step', '::0.0.0.1')
ixNet.setMultiAttribute(networkAddress + '/nest:2',
            '-enabled', 'false',
            '-step', '::0.0.0.1')
ixNet.commit()
active = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1', '-active')
ixNet.setMultiAttribute(active, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(active, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'false')
ixNet.commit()
overlay = ixNet.add(active, 'overlay')
ixNet.setMultiAttribute(overlay,
            '-count', '1',
            '-index', '5',
            '-indexStep', '0',
            '-value', 'Steptrue',
            '-value', 'true')
ixNet.commit()
overlay = ixNet.remapIds(overlay)[0]
overlay_1 = ixNet.add(active, 'overlay')
ixNet.setMultiAttribute(overlay_1,
            '-count', '1',
            '-index', '9',
            '-indexStep', '0',
            '-valueStep', 'true',
            '-value', 'true')
ixNet.commit()

#Add Device Group Behind IPv6 Network Group
deviceGroup_bgp = ixNet.add(IPv6_LoopBack, 'deviceGroup')
ixNet.setMultiAttribute(deviceGroup_bgp,
	'-multiplier', '1',
	'-name', 'BGP_L3vpn_1')
ixNet.commit()
deviceGroup_bgp = ixNet.remapIds(deviceGroup_bgp)[0]
enable = ixNet.getAttribute(deviceGroup_bgp, '-enabled')
ixNet.setMultiAttribute(enable,
	'-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(enable, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'true')
ixNet.commit()
singleValue = ixNet.remapIds(singleValue)[0]

ipv6Loopback = ixNet.add(deviceGroup_bgp, 'ipv6Loopback')
ixNet.setMultiAttribute(ipv6Loopback,
	'-stackedLayers', [],
	'-name', 'IPv6 Loopback 1')
ixNet.commit()
ipv6Loopback = ixNet.remapIds(ipv6Loopback)[0]

Connector = ixNet.add(ipv6Loopback, 'connector')
ixNet.setMultiAttribute(Connector,
	'-connectedTo', 'ipv6PrefixPools')
ixNet.commit()
Connector = ixNet.remapIds(Connector)[0]
prefix = ixNet.getAttribute(ipv6Loopback, '-prefix')
ixNet.setMultiAttribute(prefix,
	'-clearOverlays', 'false')
ixNet.commit()
Single_Value = ixNet.add(prefix, 'singleValue')
ixNet.setMultiAttribute(Single_Value,
	'-value', ' 128')
ixNet.commit()        
address = ixNet.getAttribute(ipv6Loopback, '-address')
ixNet.setMultiAttribute(address,
	'-clearOverlays', 'false')
ixNet.commit()
Counter = ixNet.add(address, 'counter')
ixNet.setMultiAttribute(Counter,
	'-step', '::0.0.0.1',
	'-start', '1111::1',
	'-direction', 'increment')
ixNet.commit()
bgpIpv6Peer_1 = ixNet.add(ipv6Loopback, 'bgpIpv6Peer')
ixNet.setMultiAttribute(bgpIpv6Peer_1,
	'-numberSRTEPolicies', '2',
	'-enSRv6DataPlane', 'true',
	'-stackedLayers', [],
	'-name', 'BGP6Peer2')
ixNet.commit()
bgpIpv6Peer_1 = ixNet.remapIds(bgpIpv6Peer_1)[0]
dutIp = ixNet.getAttribute(bgpIpv6Peer_1, '-dutIp')
ixNet.setMultiAttribute(dutIp,
	'-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(dutIp, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '::0.0.0.1',
	'-start', '2222::1',
	'-direction', 'increment')
ixNet.commit()
counter = ixNet.remapIds(counter)[0]
filterSRTEPoliciesV6 = ixNet.getAttribute(bgpIpv6Peer_1, '-filterSRTEPoliciesV6')
ixNet.setMultiAttribute(filterSRTEPoliciesV6,
	'-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(filterSRTEPoliciesV6, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'true')
ixNet.commit()
filterSRTEPoliciesV4 = ixNet.getAttribute(bgpIpv6Peer_1, '-filterSRTEPoliciesV4')
ixNet.setMultiAttribute(filterSRTEPoliciesV4,
	'-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(filterSRTEPoliciesV4, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'true')
ixNet.commit()
filterIpV4MplsVpn = ixNet.getAttribute(bgpIpv6Peer_1, '-filterIpV4MplsVpn')
ixNet.setMultiAttribute(filterIpV4MplsVpn, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(filterIpV4MplsVpn, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
capabilitySRTEPoliciesV4 = ixNet.getAttribute(bgpIpv6Peer_1, '-capabilitySRTEPoliciesV4')
ixNet.setMultiAttribute(capabilitySRTEPoliciesV4,
	'-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(capabilitySRTEPoliciesV4, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'true')
ixNet.commit()
capabilitySRTEPoliciesV6 = ixNet.getAttribute(bgpIpv6Peer_1, '-capabilitySRTEPoliciesV6')
ixNet.setMultiAttribute(capabilitySRTEPoliciesV6,	'-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(capabilitySRTEPoliciesV6, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
capabilityNHEncodingCapabilities = ixNet.getAttribute(bgpIpv6Peer_1, '-capabilityNHEncodingCapabilities')
ixNet.setMultiAttribute(capabilityNHEncodingCapabilities, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(capabilityNHEncodingCapabilities, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
#Configuring the SRTE Policy Properties
print "Configuring the SRTE Policy Properties: BGP SRTE Policy Tab"
policyType = ixNet.getAttribute(bgpIpv6Peer_1 + '/bgpSRTEPoliciesListV6', '-policyType')
ixNet.setMultiAttribute(policyType, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(policyType, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'ipv6')
ixNet.commit()
endPointV6 = ixNet.getAttribute(bgpIpv6Peer_1 + '/bgpSRTEPoliciesListV6', '-endPointV6')
ixNet.setMultiAttribute(endPointV6, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(endPointV6, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '2222::1')
ixNet.commit()
ixNet.setMultiAttribute(bgpIpv6Peer_1 + '/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6',
	'-numberOfSegmentsV6', '6')
ixNet.commit()
#singleValue = ixNet.add('numberOfActiveSegments', 'singleValue')
#ixNet.setMultiAttribute('singleValue',
#	'-value', '6')
#ixNet.commit()
segmentType = ixNet.getAttribute(bgpIpv6Peer_1 + '/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6', '-segmentType')
ixNet.setMultiAttribute(segmentType, '-clearOverlays', 'false')

ixNet.commit()
singleValue = ixNet.add(segmentType, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'ipv6sid')
ixNet.commit()
ipv6SID = ixNet.getAttribute(bgpIpv6Peer_1 + '/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6', '-ipv6SID')
ixNet.setMultiAttribute(ipv6SID, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(ipv6SID, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '6666::1')
ixNet.commit()
singleValue = ixNet.remapIds(singleValue)[0]
ixNet.setMultiAttribute(ipv6SID + '/nest:1',
	'-enabled', 'false',
	'-step', '::0.0.0.1')

ixNet.setMultiAttribute(ipv6SID + '/nest:2',
	'-enabled', 'false',
	'-step', '::0.0.0.1')

ixNet.setMultiAttribute(ipv6SID + '/nest:3',
	'-enabled', 'false',
	'-step', '::0.0.0.1')
ixNet.commit()
overlay = ixNet.add(ipv6SID, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '2',
	'-indexStep', '0',
	'-valueStep', '7001::1',
	'-value', '7001::1')
ixNet.commit()
overlay = ixNet.remapIds(overlay)[0]

overlay = ixNet.add(ipv6SID, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '3',
	'-indexStep', '0',
	'-valueStep', '7003::1',
	'-value', '7003::1')
ixNet.commit()
overlay = ixNet.remapIds(overlay)[0]

overlay = ixNet.add(ipv6SID, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '4',
	'-indexStep', '0',
	'-valueStep', '7004::1',
	'-value', '7004::1')
ixNet.commit()
overlay = ixNet.remapIds(overlay)[0]

overlay = ixNet.add(ipv6SID, 'overlay')
ixNet.setMultiAttribute(overlay, '-count', '1',
	'-index', '5',
	'-indexStep', '0',
	'-valueStep', '7007::1',
	'-value', '7007::1')
ixNet.commit()
overlay = ixNet.remapIds(overlay)[0]

overlay = ixNet.add(ipv6SID, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '6',
	'-indexStep', '0',
	'-valueStep', '7009::1',
	'-value', '7009::1')
ixNet.commit()
overlay = ixNet.remapIds(overlay)[0]

overlay = ixNet.add(ipv6SID, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '8',
	'-indexStep', '0',
	'-valueStep', '7002::1',
	'-value', '7002::1')
ixNet.commit()
overlay = ixNet.remapIds(overlay)[0]

overlay = ixNet.add(ipv6SID, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '9',
	'-indexStep', '0',
	'-valueStep', '7006::1',
	'-value', '7006::1')
ixNet.commit()
overlay = ixNet.remapIds(overlay)[0]

overlay = ixNet.add(ipv6SID, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '10',
	'-indexStep', '0',
	'-valueStep', '7008::1',
	'-value', '7008::1')
ixNet.commit()
overlay = ixNet.remapIds(overlay)[0]

overlay = ixNet.add(ipv6SID, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '11',
	'-indexStep', '0',
	'-valueStep', '7004::1',
	'-value', '7004::1')
ixNet.commit()
overlay = ixNet.remapIds(overlay)[0]

overlay = ixNet.add(ipv6SID, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '12',
	'-indexStep', '0',
	'-valueStep', '7005::1',
	'-value', '7005::1')
ixNet.commit()
#Adding BGPVRF on top of BGP+
bgpV6Vrf_1 = ixNet.add(bgpIpv6Peer_1, 'bgpV6Vrf')
ixNet.setMultiAttribute(bgpV6Vrf_1,
	'-multiplier', '4',
	'-stackedLayers', [],
	'-name', 'BGP6VRF2')
ixNet.commit()
bgpV6Vrf_1 = ixNet.remapIds(bgpV6Vrf_1)[0]
targetAsNumber = ixNet.getAttribute(bgpV6Vrf_1 + '/bgpExportRouteTargetList:1', '-targetAsNumber')
ixNet.setMultiAttribute(targetAsNumber,
	'-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(targetAsNumber, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '1',
	'-start', '100',
	'-direction', 'increment')
ixNet.commit()
#Adding Network Group Behind BGP+
networkGroup = ixNet.add(deviceGroup_bgp, 'networkGroup')
ixNet.setMultiAttribute(networkGroup, '-name', 'IPv4_VPN_Rote')
ixNet.commit()
networkGroup = ixNet.remapIds(networkGroup)[0]
networkGroup_1 = ixNet.getAttribute(networkGroup, '-enabled')
ixNet.setMultiAttribute(networkGroup_1,
	'-clearOverlays', 'false')
ixNet.commit()
networkGroup_1 = ixNet.add(networkGroup_1, 'singleValue')
ixNet.setMultiAttribute(networkGroup_1, '-value', 'true')
ixNet.commit()
networkGroup_1 = ixNet.remapIds(networkGroup_1)[0]
ipv4PrefixPools = ixNet.add(networkGroup, 'ipv4PrefixPools')
ixNet.setMultiAttribute(ipv4PrefixPools, '-addrStepSupported', 'true',	'-name', 'BasicIPv4Addresses2')
ixNet.commit()
ipv4PrefixPools = ixNet.remapIds(ipv4PrefixPools)[0]
connector = ixNet.add(ipv4PrefixPools, 'connector')
ixNet.setMultiAttribute(connector,
	'-connectedTo', 'bgpV6Vrf_1')
ixNet.commit()
networkAddress = ixNet.getAttribute(ipv4PrefixPools, '-networkAddress')
ixNet.setMultiAttribute(networkAddress,
	'-clearOverlays', 'false')

ixNet.commit()
counter = ixNet.add(networkAddress, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '0.1.0.0',
	'-start', '1.1.1.1',
	'-direction', 'increment')
ixNet.commit()
bgpV6L3VpnRouteProperty = ixNet.getList(ipv4PrefixPools, 'bgpV6L3VpnRouteProperty')[0]
labelStep = ixNet.getAttribute(bgpV6L3VpnRouteProperty, '-labelStep')
ixNet.setMultiAttribute(labelStep,
	'-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(labelStep, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '1')
ixNet.commit()
enableSrv6Sid = ixNet.getAttribute(bgpV6L3VpnRouteProperty, '-enableSrv6Sid')
ixNet.setMultiAttribute(enableSrv6Sid, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(enableSrv6Sid, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
srv6SidLoc = ixNet.getAttribute(bgpV6L3VpnRouteProperty, '-srv6SidLoc')
ixNet.setMultiAttribute(srv6SidLoc, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(srv6SidLoc, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '1::',
	'-start', 'a1::d100',
	'-direction', 'increment')
ixNet.commit()
#Configure BGP/BGP-vrf at PEER2 side
deviceGroup_P2 = ixNet.add(networkGroup_P2, 'deviceGroup')
ixNet.setMultiAttribute(deviceGroup_P2,
	'-multiplier', '1',
	'-name', 'BGP_L3vpn_2')
ixNet.commit()
deviceGroup_P2 = ixNet.remapIds(deviceGroup_P2)[0]
ipv6Loopback_P2 = ixNet.add(deviceGroup_P2, 'ipv6Loopback')
ixNet.setMultiAttribute(ipv6Loopback_P2,
	'-stackedLayers', [],
	'-name', 'IPv6Loopback1')
ixNet.commit()
ipv6Loopback_P2 = ixNet.remapIds(ipv6Loopback_P2)[0]
connector = ixNet.add(ipv6Loopback_P2, 'connector')
ixNet.commit()
address = ixNet.getAttribute(ipv6Loopback_P2, '-address')
ixNet.setMultiAttribute(address, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(address, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '::0.0.0.1',
	'-start', '2222::1',
	'-direction', 'increment')
ixNet.commit()
bgpIpv6Peer_p2 = ixNet.add(ipv6Loopback_P2, 'bgpIpv6Peer')
#ixNet.setMultiAttribute(bgpIpv6Peer_p2, '-stackedLayers', '-name', 'BGP6Peer1')
ixNet.commit()
bgpIpv6Peer_p2 = ixNet.remapIds(bgpIpv6Peer_p2)[0]
dutIp = ixNet.getAttribute(bgpIpv6Peer_p2, '-dutIp')
ixNet.setMultiAttribute(dutIp, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(dutIp, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '::0.0.0.1',
	'-start', '1111::1',
	'-direction', 'increment')
ixNet.commit()
filterSRTEPoliciesV6 = ixNet.getAttribute(bgpIpv6Peer_p2, '-filterSRTEPoliciesV6')
ixNet.setMultiAttribute(filterSRTEPoliciesV6, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(filterSRTEPoliciesV6, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
filterSRTEPoliciesV4 = ixNet.getAttribute(bgpIpv6Peer_p2, '-filterSRTEPoliciesV4')
ixNet.setMultiAttribute(filterSRTEPoliciesV4, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(filterSRTEPoliciesV4, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
filterIpV4MplsVpn_2 = ixNet.getAttribute(bgpIpv6Peer_p2, '-filterIpV4MplsVpn')
ixNet.setMultiAttribute(filterIpV4MplsVpn_2, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(filterIpV4MplsVpn_2, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
capabilitySRTEPoliciesV4 = ixNet.getAttribute(bgpIpv6Peer_p2, '-capabilitySRTEPoliciesV4')
ixNet.setMultiAttribute(capabilitySRTEPoliciesV4, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(capabilitySRTEPoliciesV4, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
capabilitySRTEPoliciesV6 = ixNet.getAttribute(bgpIpv6Peer_p2, '-capabilitySRTEPoliciesV6')
ixNet.setMultiAttribute(capabilitySRTEPoliciesV6, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(capabilitySRTEPoliciesV6, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
capabilityNHEncodingCapabilities_2 = ixNet.getAttribute(bgpIpv6Peer_p2, '-capabilityNHEncodingCapabilities')
ixNet.setMultiAttribute(capabilityNHEncodingCapabilities_2, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(capabilityNHEncodingCapabilities_2, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
#Adding BGPVRF on top of BGP+ @Peer2 side
bgpV6Vrf_2 = ixNet.add(bgpIpv6Peer_p2, 'bgpV6Vrf')
ixNet.setMultiAttribute(bgpV6Vrf_2,
	'-multiplier', '4',
	'-stackedLayers', [],
	'-name', 'BGP6VRF2')
ixNet.commit()
bgpV6Vrf_2 = ixNet.remapIds(bgpV6Vrf_2)[0]
targetAsNumber = ixNet.getAttribute(bgpV6Vrf_2 + '/bgpExportRouteTargetList:1', '-targetAsNumber')
ixNet.setMultiAttribute(targetAsNumber, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(targetAsNumber, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '1',
	'-start', '100',
	'-direction', 'increment')
ixNet.commit()
#Adding Network Group Behind BGP+ AT PEER2 Side
networkGroup_P2 = ixNet.add(deviceGroup_P2, 'networkGroup')
ixNet.setMultiAttribute(networkGroup_P2,
	'-name', 'IPv4_VPN_Rote_2')
ixNet.commit()
networkGroup_P2 = ixNet.remapIds(networkGroup_P2)[0]
networkGroup_2 = ixNet.getAttribute(networkGroup_P2, '-enabled')
ixNet.setMultiAttribute(networkGroup_2, '-clearOverlays', 'false')
ixNet.commit()
networkGroup_2 = ixNet.add(networkGroup_2, 'singleValue')
ixNet.setMultiAttribute(networkGroup_2, '-value', 'true')
ixNet.commit()
networkGroup_1 = ixNet.remapIds(networkGroup_2)[0]
ipv4PrefixPools_P2 = ixNet.add(networkGroup_P2, 'ipv4PrefixPools')
ixNet.setMultiAttribute(ipv4PrefixPools_P2,
	'-addrStepSupported', 'true',
	'-name', 'BasicIPv4Addresses2')
ixNet.commit()
ipv4PrefixPools_P2 = ixNet.remapIds(ipv4PrefixPools_P2)[0]
connector_P2 = ixNet.add(ipv4PrefixPools_P2, 'connector')
ixNet.setMultiAttribute(connector_P2, '-connectedTo', 'bgpV6Vrf_2')
ixNet.commit()
networkAddress_P2 = ixNet.getAttribute(ipv4PrefixPools_P2, '-networkAddress')
ixNet.setMultiAttribute(networkAddress_P2, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(networkAddress_P2, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '0.1.0.0',
	'-start', '2.2.2.2',
	'-direction', 'increment')
ixNet.commit()
bgpV6L3VpnRouteProperty_P2 = ixNet.getList(ipv4PrefixPools_P2, 'bgpV6L3VpnRouteProperty')[0]
labelStep = ixNet.getAttribute(bgpV6L3VpnRouteProperty_P2, '-labelStep')
ixNet.setMultiAttribute(labelStep, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(labelStep, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '1')
ixNet.commit()
enableSrv6Sid = ixNet.getAttribute(bgpV6L3VpnRouteProperty_P2, '-enableSrv6Sid')
ixNet.setMultiAttribute(enableSrv6Sid, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(enableSrv6Sid, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
srv6SidLoc = ixNet.getAttribute(bgpV6L3VpnRouteProperty_P2, '-srv6SidLoc')
ixNet.setMultiAttribute(srv6SidLoc, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(srv6SidLoc, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '::1',
	'-start', 'a1::d100',
	'-direction', 'increment')
ixNet.commit()
enableExtendedCommunity = ixNet.getAttribute(bgpV6L3VpnRouteProperty_P2, '-enableExtendedCommunity')
ixNet.setMultiAttribute(enableExtendedCommunity, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(enableExtendedCommunity, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()
colorValue = ixNet.getAttribute(bgpV6L3VpnRouteProperty_P2 + '/bgpExtendedCommunitiesList:1', '-colorValue')
ixNet.setMultiAttribute(colorValue, '-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(colorValue, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '1',
	'-start', '100',
	'-direction', 'increment')
ixNet.commit()
subType = ixNet.getAttribute(bgpV6L3VpnRouteProperty_P2 + '/bgpExtendedCommunitiesList:1', '-subType')
ixNet.setMultiAttribute(subType,	'-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(subType, 'singleValue')
ixNet.setMultiAttribute(singleValue,	'-value', 'color')
ixNet.commit()
type = ixNet.getAttribute(bgpV6L3VpnRouteProperty_P2 + '/bgpExtendedCommunitiesList:1', '-type')
ixNet.setMultiAttribute(type, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(type, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'opaque')
ixNet.commit()

################################################################################
# 2. Start ISISl3/BGP+ protocol and wait for 60 seconds
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(30)

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

################################################################################
# 4. Configure L2-L3 traffic 
################################################################################
print "Congfiguring L2-L3 Traffic Item"
Root = ixNet.getRoot()
statistic_1 = ixNet.add(Root + '/globals/testInspector', 'statistic')
ixNet.commit()
statistic_1 = ixNet.remapIds('statistic_1')[0]

statistic_2 = ixNet.add(Root + '/globals/testInspector', 'statistic')
ixNet.commit()
statistic_2 = ixNet.remapIds('statistic_2')[0]

statistic_3 = ixNet.add(Root + '/globals/testInspector', 'statistic')
ixNet.commit()
statistic_3 = ixNet.remapIds('statistic_3')[0]

statistic_4 = ixNet.add(Root + '/globals/testInspector', 'statistic')
ixNet.commit()
statistic_4 = ixNet.remapIds('statistic_4')[0]

statistic_5 = ixNet.add(Root + '/globals/testInspector', 'statistic')
ixNet.commit()
statistic_5 = ixNet.remapIds('statistic_5')[0]

statistic_6 = ixNet.add(Root + '/globals/testInspector', 'statistic')
ixNet.setMultiAttribute(statistic_6, '-value', '1')
ixNet.commit()

statistic_6 = ixNet.remapIds('statistic_6')[0]

statistic_7 = ixNet.add(Root + '/globals/testInspector', 'statistic')
ixNet.commit()
statistic_7 = ixNet.remapIds('statistic_7')[0]

statistic_8 = ixNet.add(Root + '/globals/testInspector', 'statistic')
ixNet.setMultiAttribute(statistic_8, '-value', '3')
ixNet.commit()
statistic_8 = ixNet.remapIds('statistic_8')[0]
ixNet.setMultiAttribute(Root + '/globals/interfaces',
	'-arpOnLinkup', 'true',
	'-nsOnLinkup', 'true',
	'-sendSingleArpPerGateway', 'true',
	'-sendSingleNsPerGateway', 'true')

ixNet.commit()
ixNet.setMultiAttribute(Root + '/traffic',
	'-cycleTimeUnitForScheduledStart', 'milliseconds',
	'-refreshLearnedInfoBeforeApply', 'true',
	'-detectMisdirectedOnAllPorts', 'false',
	'-useRfc5952', 'true',
	'-cycleOffsetForScheduledStart', '0',
	'-cycleOffsetUnitForScheduledStart', 'nanoseconds',
	'-enableEgressOnlyTracking', 'false',
	'-cycleTimeForScheduledStart', '1',
	'-enableLagFlowBalancing', 'true',
	'-peakLoadingReplicationCount', '1')

ixNet.setMultiAttribute(Root + '/traffic/statistics/misdirectedPerFlow', '-enabled', 'false')
ixNet.setMultiAttribute(Root + '/traffic/statistics/multipleJoinLeaveLatency',
	'-enabled', 'false')

ixNet.setMultiAttribute(Root + '/traffic/statistics/oneTimeJoinLeaveLatency',
	'-enabled', 'false')
ixNet.commit()
trafficItem  = ixNet.add(Root + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem,
	'-name', 'Top1-To-Top2',
	'-multicastForwardingMode', 'replication',
	'-useControlPlaneRate', 'true',
	'-useControlPlaneFrameSize', 'true',
	'-roundRobinPacketOrdering', 'false',
	'-numVlansForMulticastReplication', '1',
	'-trafficType', 'ipv4')
ixNet.commit()
trafficItem = ixNet.remapIds(trafficItem)[0]
endpoint = ixNet.add(trafficItem, 'endpointSet')

ixNet.setMultiAttribute(endpoint,
	'-name',                  'EndpointSet-1',
	'-multicastDestinations', [],
	'-scalableSources',       [],
	'-multicastReceivers',    [],
	'-scalableDestinations',  [],
	'-ngpfFilters',           [],
	'-trafficGroups',         [],
	'-sources',               [topo1],
	'-destinations',          [deviceGroup_P2])

ixNet.commit()
endpoint = ixNet.remapIds('endpointSet')[0]

egressTracking = ixNet.add(trafficItem, 'egressTracking')
ixNet.commit()
egressTracking = ixNet.remapIds('egressTracking')[0]


ixNet.setMultiAttribute(trafficItem + '/tracking',
	'-trackBy', ['ipv4SourceIp0', 'trackingenabled0'],
	'-values', [],
	'-fieldWidth', 'thirtyTwoBits',
	'-protocolOffset', 'Root.0')

ixNet.setMultiAttribute(trafficItem + '/tracking/latencyBin',
	'-binLimits', ['1','1.42','2','2.82','4','5.66','8','2147483647'])
ixNet.commit()

###############################################################################
# 5. Apply and start L2/L3 traffic
###############################################################################
print ('applying L2/L3 traffic')
ixNet.execute('apply', ixNet.getRoot() + '/traffic')
time.sleep(5)
print ('starting L2/L3 traffic')
ixNet.execute('start', ixNet.getRoot() + '/traffic')
print ('let traffic run for 60 second')
time.sleep(20)

###############################################################################
# 6. Retrieve L2/L3 traffic item statistics
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
# 7. Stop L2/L3 traffic.
#################################################################################
print ('Stopping L2/L3 traffic')
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)

################################################################################
# 8. Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
print ('!!! Test Script Ends !!!')

