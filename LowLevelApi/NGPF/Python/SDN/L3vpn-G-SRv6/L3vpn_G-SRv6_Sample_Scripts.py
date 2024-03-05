#/usr/bin/tclsh

################################################################################
#                                                                              #
#    Copyright 1997 - 2021 by Keysight                                         #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################

####################################################################################    
#                                                                                  #
#                                LEGAL  NOTICE:                                    #
#                                ==============                                    #
# The following code and documentation (hereinafter "the script") is an            #
# example script for demonstration purposes only.                                  #
# The script is not a standard commercial product offered by Keysight and have     #
# been developed and is being provided for use only as indicated herein. The       #
# script [and all modifications enhancements and updates thereto (whether          #
# made by Keysight and/or by the user and/or by a third party)] shall at all times #
# remain the property of Keysight.                                                 #
#                                                                                  #
# Keysight does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without              #
# omissions or error-free.                                                         #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND Keysight         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE                  #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR     #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                     #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE     #
# USER.                                                                            #
# IN NO EVENT SHALL Keysight BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF         #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR              #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR                  #
# CONSEQUENTIAL DAMAGES EVEN IF Keysight HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                         #
# Keysight will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the         #
# script or any part thereof. The user acknowledges that although Keysight may     #
# from time to time and in its sole discretion provide maintenance or support      #
# services for the script any such services are subject to the warranty and        #
# damages limitations forth herein and will not obligate Keysight to provide       #
# any additional maintenance or support services.                                  #
#                                                                                  #
####################################################################################    

#####################################################################################
#                                                                              		#
# Description:                                                                 		#
#    This script intends to demonstrate how to use L3vpn Over G-SRv6 underlay using #
#    TCL APIs.                                                                      #
#                                                                                   #
#    1.This topology scenario shows how to configure and run tests on IPv4 Layer 3  #
#      VPNs over ISIS SRv6 core. As an example IPv4 Layer 3 VPN topology over G-SRv6#
#      core is configured in b2b ports.Left-hand-side of the topology has ISIS SRv6 #
#      node. One of them (PE1) is acting as PE node running BGP. On the right-hand  #
#      side of the port is configured with a single G-SRv6 PE node (PE2) and BGP    #
#      policy is configured. Behind both PEs emulated CEs are connected .           #
#    2. Start all protocols.                                             		    #
#    3. Retrieve protocol statistics.                                          		#
#    4. Retrieve protocol learned info.                                        		#
#    5. Start the L2-L3 traffic.                                               		#
#    6. Retrieve L2-L3 traffic stats.                                          		#
#    7. Stop L2-L3 traffic.                                                    		#
#    8. Stop all protocols.                                                    		#                                                                                          
#####################################################################################

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
#ixNetPath = r'C:\Program Files (x86)\Keysight\IxNetwork\9.10.2007.7\API\Python'
#sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.39.43.12'
ixTclPort   = '8015'
ports       = [('10.39.50.179', '1', '5',), ('10.39.50.179', '1', '6',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.50',
	 '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

################################################################################
# 1. Protocol configuration section. Configure ISISL3/BGP+ as per the description
#    give above
################################################################################ 
root = ixNet.getRoot()
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

print ("Adding 2 vports")
vportTx = ixNet.getList(root, 'vport')[0]
vportRx = ixNet.getList(root, 'vport')[1]

print "Assigning the ports"


print "Adding 2 topologies"
print("adding topologies")
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

t1dev1 = t1devices [0]
t2dev1 = t2devices [0]

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
ixNet.setAttribute(topo1, '-name', 'Single PE - PE')
ixNet.setAttribute(topo2, '-name', 'IPv4 L3VPN G-SRv6 Topology')

ixNet.setAttribute(t1dev1, '-name', 'PE2')
ixNet.setAttribute(t2dev1, '-name', 'Emulated P Node')
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

print "Change the value enableIPv6SID"
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

#Change the value of discardLSPs
print "Change the value discardLSPs"
discardLSPs_1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1', '-discardLSPs')
ixNet.setMultiAttribute(discardLSPs_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(discardLSPs_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()
discardLSPs_1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1', '-discardLSPs')
ixNet.setMultiAttribute(discardLSPs_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(discardLSPs_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()

#Enable of enableWideMetric
print "Enable the enableWideMetric"
enableWideMetric_1 = ixNet.getAttribute(t1dev1 + '/isisL3Router:1', '-enableWideMetric')
ixNet.setMultiAttribute(enableWideMetric_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(enableWideMetric_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
enableWideMetric_1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1', '-enableWideMetric')
ixNet.setMultiAttribute(enableWideMetric_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(enableWideMetric_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Enable Segment Routing
print "Enable Segment routing"
ixNet.setMultiAttribute(t1dev1 + '/isisL3Router:1',
	'-enableSR', 'true')
ixNet.commit()
ixNet.setMultiAttribute(t2dev1 + '/isisL3Router:1',
	'-enableSR', 'true')
ixNet.commit()

print "Enabling the ipv6Flag"
ipv6Flag_1 = ixNet.getAttribute(t1dev1 + '/isisL3Router:1', '-ipv6Flag')
ixNet.setMultiAttribute(ipv6Flag_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv6Flag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()
ipv6Flag_1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1', '-ipv6Flag')
ixNet.setMultiAttribute(ipv6Flag_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv6Flag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()

#Enable the ipv4Flag
print "Enabling the ipv4Flag"
ipv4Flag_1 = ixNet.getAttribute(t1dev1 + '/isisL3Router:1', '-ipv4Flag')
ixNet.setMultiAttribute(ipv4Flag_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv4Flag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()
ipv4Flag_1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1', '-ipv4Flag')
ixNet.setMultiAttribute(ipv4Flag_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv4Flag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'false')
ixNet.commit()

#Enable the ipv6Srh means Enable SR-IPv6
print "Enabling the ipv6Srh means Enable SR-IPv6"
ipv6Srh_1 = ixNet.getAttribute(t1dev1 + '/isisL3Router:1', '-ipv6Srh')
ixNet.setMultiAttribute(ipv6Srh_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv6Srh_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Configure locator for isisL3Router in t1dev1
print "Configure locator for isisL3Router in t1dev1"
locator2 = ixNet.getAttribute(t1dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList', '-locator')
ixNet.commit()
singleV2 = ixNet.add(locator2, 'singleValue')
ixNet.setMultiAttribute(singleV2,
	'-value', '5000:0:1:1:0:0:0:0')
ixNet.commit()

#configure sidCount locator in for isisL3Router in t1dev1
print "configure sidCount locator in for isisL3Router in t1dev1"
ixNet.setMultiAttribute(t1dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList', '-sidCount', '3') 
ixNet.commit()

#Configure EndSid Value for isisL3Router in t1dev1
print "Configure EndSid Value for isisL3Router in t1dev1"
sid2 = ixNet.getAttribute(t1dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-sid')
ixNet.commit()
counter = ixNet.add(sid2, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '0:0:0:0:1:0:0:0',
	'-start', '5000:0:1:1:1:0:0:0',
	'-direction', 'increment')
ixNet.commit()

#Configure C flag in EndSid for isisL3Router in t1dev1
print "Configure C flag in EndSid for isisL3Router in t1dev1"
cFlag2 = ixNet.getAttribute(t1dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-cFlag')
singleValue = ixNet.add(cFlag2, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'false')
ixNet.commit()
overlay = ixNet.add(cFlag2, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '2',
	'-value', 'true')
ixNet.commit()

#Configure endPointFunction in EndSid for isisL3Router in t1dev1
print "Configure endPointFunction in EndSid for isisL3Router in t1dev1"
endPointFunction2 = ixNet.getAttribute(t1dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-endPointFunction')
ixNet.commit()
singleV22 = ixNet.add(endPointFunction2, 'singleValue')
ixNet.setMultiAttribute(singleV22,
	'-value', '4')
ixNet.commit()

ixNet.setMultiAttribute(endPointFunction2 + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
overlay22 = ixNet.add(endPointFunction2, 'overlay')
ixNet.setMultiAttribute(overlay22,
	'-count', '1',
	'-index', '2',
	'-value', '104')
ixNet.commit()

#Configure includeSRv6SIDStructureSubSubTlv in EndSid for isisL3Router in t1dev1
print "Configure includeSRv6SIDStructureSubSubTlv in EndSid for isisL3Router in t1dev1"
includeSRv6SIDStructureSubSubTlv2 = ixNet.getAttribute(t1dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-includeSRv6SIDStructureSubSubTlv')
ixNet.commit()
sValue2_1 = ixNet.add(includeSRv6SIDStructureSubSubTlv2, 'singleValue')
ixNet.setMultiAttribute(sValue2_1,
	'-value', 'true')
ixNet.commit()
locatorBlockLength2 = ixNet.getAttribute(t1dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-locatorBlockLength')
ixNet.commit()
sValue2_2 = ixNet.add(locatorBlockLength2, 'singleValue')
ixNet.setMultiAttribute(sValue2_2,
	'-value', '48',)
ixNet.commit()
ixNet.setMultiAttribute(locatorBlockLength2 + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
locatorNodeLength2 = ixNet.getAttribute(t1dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-locatorNodeLength')
ixNet.commit()
sValue2_3 = ixNet.add(locatorNodeLength2, 'singleValue')
ixNet.setMultiAttribute(sValue2_3,
	'-value', '16')
ixNet.commit()
ixNet.setMultiAttribute(locatorNodeLength2 + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
functionLength2 = ixNet.getAttribute(t1dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-functionLength')
ixNet.commit()
sValue2_4 = ixNet.add(functionLength2, 'singleValue')
ixNet.setMultiAttribute(sValue2_4,
	'-value', '16')
ixNet.commit()

#Configure ADJ SID Count in isisL3_1
print "Configure ADJ SID Count in isisL3_1"
ixNet.setMultiAttribute(isisL3_1,
	'-adjSidCount', '3')
ixNet.commit()

#Configure ipv6AdjSid Value in isisL3_1
print "Configure ipv6AdjSid Value in isisL3_1"
ipv6AdjSid_2 = ixNet.getAttribute(isisL3_1 + '/isisSRv6AdjSIDList', '-ipv6AdjSid')		
ixNet.commit()
counter = ixNet.add(ipv6AdjSid_2, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '0:0:0:0:1:0:0:0',
	'-start', '5000:0:1:1:41:0:0:0',
	'-direction', 'increment')
ixNet.commit()

#Configure 	cFlag for ipv6AdjSid in isisL3_1
print "Configure cFlag for ipv6AdjSid in isisL3_1"
cFlag2_1 = ixNet.getAttribute(isisL3_1 + '/isisSRv6AdjSIDList', '-cFlag')
ixNet.commit()
singleV3 = ixNet.add(cFlag2_1, 'singleValue')
ixNet.commit()
overlay = ixNet.add(cFlag2_1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '2',
	'-value', 'true')
ixNet.commit()

#Configure endPointFunction for ipv6AdjSid in isisL3_1
print "Configure endPointFunction for ipv6AdjSid in isisL3_1"
endPointFunction_2 = ixNet.getAttribute(isisL3_1 + '/isisSRv6AdjSIDList', '-endPointFunction')
ixNet.commit()
singleV4_2 = ixNet.add(endPointFunction_2, 'singleValue')
ixNet.setMultiAttribute(singleV4_2,
	'-value', '8')
ixNet.commit()
ixNet.setMultiAttribute(endPointFunction_2 + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
overlay = ixNet.add(endPointFunction_2, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '2',
	'-value', '108')
ixNet.commit()

#Configure includeSRv6SIDStructureSubSubTlv in isisL3_1
print "Configure includeSRv6SIDStructureSubSubTlv in isisL3_1"
includeSRv6SIDStructureSubSubTlv_2 = ixNet.getAttribute(isisL3_1 + '/isisSRv6AdjSIDList', '-includeSRv6SIDStructureSubSubTlv')
ixNet.commit()
singlV5 = ixNet.add(includeSRv6SIDStructureSubSubTlv_2, 'singleValue')
ixNet.setMultiAttribute(singlV5,
	'-value', 'true')
ixNet.commit() 
locatorBlockLength_2 = ixNet.getAttribute(isisL3_1 + '/isisSRv6AdjSIDList', '-locatorBlockLength')
ixNet.setMultiAttribute(locatorBlockLength_2,
	'-clearOverlays', 'false')
ixNet.commit()
singlV6 = ixNet.add(locatorBlockLength_2, 'singleValue')
ixNet.setMultiAttribute(singlV6,
	'-value', '48',)
ixNet.commit()		
ixNet.setMultiAttribute(locatorBlockLength_2 + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
locatorNodeLength_2 = ixNet.getAttribute(isisL3_1 + '/isisSRv6AdjSIDList', '-locatorNodeLength')
ixNet.commit()
singlV7 = ixNet.add(locatorNodeLength_2, 'singleValue')
ixNet.setMultiAttribute(singlV7,
	'-value', '16')
ixNet.commit()
ixNet.setMultiAttribute(locatorNodeLength_2 + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
functionLength_2 = ixNet.getAttribute(isisL3_1 + '/isisSRv6AdjSIDList', '-functionLength')
ixNet.commit()
singlV8 = ixNet.add(functionLength_2, 'singleValue')
ixNet.setMultiAttribute(singlV8,
	'-value', '16')
ixNet.commit()
ipv6Srh_1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1', '-ipv6Srh')
ixNet.setMultiAttribute(ipv6Srh_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(ipv6Srh_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Configuring Locator
print "Configuring Locator"
locator1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList', '-locator')
ixNet.commit()
singleV = ixNet.add(locator1, 'singleValue')
ixNet.setMultiAttribute(singleV,
	'-value', '5000:0:2:1:0:0:0:0')
ixNet.commit()

#configure sidCount
print "configure sidCount"
ixNet.setMultiAttribute(t2dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList', '-sidCount', '3') 
ixNet.commit()

#Configure EndSid Value
print "Configure EndSid Value"
sid1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-sid')
ixNet.commit()
counter = ixNet.add(sid1, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '0:0:0:0:1:0:0:0',
	'-start', '5000:0:2:1:1:0:0:0',
	'-direction', 'increment')
ixNet.commit()

#Configure C flag
print "Configure C flag"
cFlag1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-cFlag')
singleValue = ixNet.add(cFlag1, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'false')
ixNet.commit()
overlay = ixNet.add(cFlag1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '2',
	'-value', 'true')
ixNet.commit()

#Configure endPointFunction
print "Configure endPointFunction"
endPointFunction1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-endPointFunction')
ixNet.commit()
singleV2 = ixNet.add(endPointFunction1, 'singleValue')
ixNet.setMultiAttribute(singleV2,
	'-value', '4')
ixNet.commit()

ixNet.setMultiAttribute(endPointFunction1 + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
overlay = ixNet.add(endPointFunction1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '2',
	'-value', '104')
ixNet.commit()

#Configure includeSRv6SIDStructureSubSubTlv
print "Configure includeSRv6SIDStructureSubSubTlv"
includeSRv6SIDStructureSubSubTlv1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-includeSRv6SIDStructureSubSubTlv')
ixNet.commit()
sValue1 = ixNet.add(includeSRv6SIDStructureSubSubTlv1, 'singleValue')
ixNet.setMultiAttribute(sValue1,
	'-value', 'true')
ixNet.commit()
locatorBlockLength1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-locatorBlockLength')
ixNet.commit()
sValue2 = ixNet.add(locatorBlockLength1, 'singleValue')
ixNet.setMultiAttribute(sValue2,
	'-value', '48')
ixNet.commit()
ixNet.setMultiAttribute(locatorBlockLength1 + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
locatorNodeLength1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-locatorNodeLength')
ixNet.commit()
sValue3 = ixNet.add(locatorNodeLength1, 'singleValue')
ixNet.setMultiAttribute(sValue3,
	'-value', '16')
ixNet.commit()
ixNet.setMultiAttribute(locatorNodeLength1 + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
functionLength1 = ixNet.getAttribute(t2dev1 + '/isisL3Router:1/isisSRv6LocatorEntryList/isisSRv6EndSIDList', '-functionLength')
ixNet.commit()
sValue4 = ixNet.add(functionLength1, 'singleValue')
ixNet.setMultiAttribute(sValue4,
	'-value', '16')
ixNet.commit()

#Configure ADJ SID Count
print "Configure ADJ SID Count"
ixNet.setMultiAttribute(isisL3_2,
	'-adjSidCount', '3')
ixNet.commit()

#Configure ipv6AdjSid Value
print "Configure ipv6AdjSid Value"
ipv6AdjSid = ixNet.getAttribute(isisL3_2 + '/isisSRv6AdjSIDList', '-ipv6AdjSid')		
ixNet.commit()
counter = ixNet.add(ipv6AdjSid, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '0:0:0:0:1:0:0:0',
	'-start', '5000:0:2:1:41:0:0:0',
	'-direction', 'increment')
ixNet.commit()

#Configure cFlag for ipv6AdjSid
print "Configure cFlag for ipv6AdjSid"
cFlag2 = ixNet.getAttribute(isisL3_2 + '/isisSRv6AdjSIDList', '-cFlag')
ixNet.commit()
singleV3 = ixNet.add(cFlag2, 'singleValue')
ixNet.commit()
overlay = ixNet.add(cFlag2, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '2',
	'-value', 'true')
ixNet.commit()

#Configure endPointFunction for ipv6AdjSid
print "Configure endPointFunction for ipv6AdjSid"
endPointFunction = ixNet.getAttribute(isisL3_2 + '/isisSRv6AdjSIDList', '-endPointFunction')
ixNet.commit()
singleV4 = ixNet.add(endPointFunction, 'singleValue')
ixNet.setMultiAttribute(singleV4,
	'-value', '8')
ixNet.commit()
ixNet.setMultiAttribute(endPointFunction + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
overlay = ixNet.add(endPointFunction, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '2',
	'-value', '108')
ixNet.commit()

#Configure includeSRv6SIDStructureSubSubTlv
print "Configure includeSRv6SIDStructureSubSubTlv"
includeSRv6SIDStructureSubSubTlv = ixNet.getAttribute(isisL3_2 + '/isisSRv6AdjSIDList', '-includeSRv6SIDStructureSubSubTlv')
ixNet.commit()
singleV5 = ixNet.add(includeSRv6SIDStructureSubSubTlv, 'singleValue')
ixNet.setMultiAttribute(singleV5,
	'-value', 'true')
ixNet.commit() 
locatorBlockLength = ixNet.getAttribute(isisL3_2 + '/isisSRv6AdjSIDList', '-locatorBlockLength')
ixNet.setMultiAttribute(locatorBlockLength,
	'-clearOverlays', 'false')
ixNet.commit()
singleV6 = ixNet.add(locatorBlockLength, 'singleValue')
ixNet.setMultiAttribute(singleV6,
	'-value', '48')
ixNet.commit()		
ixNet.setMultiAttribute(locatorBlockLength + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
locatorNodeLength = ixNet.getAttribute(isisL3_2 + '/isisSRv6AdjSIDList', '-locatorNodeLength')
ixNet.commit()
singleV7 = ixNet.add(locatorNodeLength, 'singleValue')
ixNet.setMultiAttribute(singleV7,
	'-value', '16')
ixNet.commit()
ixNet.setMultiAttribute(locatorNodeLength + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
functionLength = ixNet.getAttribute(isisL3_2 + '/isisSRv6AdjSIDList', '-functionLength')
ixNet.commit()
singleV8 = ixNet.add(functionLength, 'singleValue')
ixNet.setMultiAttribute(singleV8,
	'-value', '16')
ixNet.commit()

#Create Network Group At Single PE - PE
print "Create Network Group At Single PE - PE"
ipv6Loopback2 = ixNet.add(t1dev1, 'ipv6Loopback')
ixNet.setMultiAttribute(ipv6Loopback2,
	'-stackedLayers', [],
	'-name', "IPv6 Loopback 2")
ixNet.commit()
address2 = ixNet.getAttribute(ipv6Loopback2, '-address')
ixNet.setMultiAttribute(address2,
	'-clearOverlays', 'false')
ixNet.commit()
singleValue2 = ixNet.add(address2, 'singleValue')
ixNet.setMultiAttribute(singleValue2,
	'-value', '1000:0:0:2:0:0:0:1')
ixNet.commit()
prefix2 = ixNet.getAttribute(ipv6Loopback2, '-prefix')
ixNet.commit()
singleValue = ixNet.add(prefix2, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', '128')
ixNet.commit()
bgpIpv6Peer2 = ixNet.add(ipv6Loopback2, 'bgpIpv6Peer')
ixNet.setMultiAttribute(bgpIpv6Peer2,
	'-stackedLayers', [],
	'-name', 'BGP+ Peer 2')
ixNet.commit()
dutIp2 = ixNet.getAttribute(bgpIpv6Peer2, '-dutIp')
ixNet.setMultiAttribute(dutIp2,
	'-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(dutIp2, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', '1001:0:0:1:0:0:0:4')
ixNet.commit()
bgpV6Vrf2 = ixNet.add(bgpIpv6Peer2, 'bgpV6Vrf')
ixNet.setMultiAttribute(bgpV6Vrf2,
	'-stackedLayers', [],
	'-name', 'BGP+ VRF 2')
ixNet.commit()
networkGroup = ixNet.add(t1dev1, 'networkGroup')
ixNet.setMultiAttribute(networkGroup,
	'-name', 'CE2')
ixNet.commit()
ipv4PrefixPools = ixNet.add(networkGroup, 'ipv4PrefixPools')
ixNet.setMultiAttribute(ipv4PrefixPools,
	'-addrStepSupported', 'true',
	'-name', 'Basic IPv4 Addresses 1')
ixNet.commit()
networkAddress = ixNet.getAttribute(ipv4PrefixPools, '-networkAddress')
ixNet.setMultiAttribute(networkAddress,
	'-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(networkAddress, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '0.1.0.0',
	'-start', '201.1.0.0',
	'-direction', 'increment')
ixNet.commit()
	
#Create Network Group At PEER2 Side
print "Create Network Group At PEER2 Side"
networkGroup_P2 = ixNet.add(t2dev1, 'networkGroup')
ixNet.setMultiAttribute(networkGroup_P2,
	'-name', 'Simulated P and PE Nodes')
ixNet.commit()
#networkGroup_P2 = (lindex (ixNet remapIds(networkGroup_P2) 0)
Network_Topology = ixNet.add(networkGroup_P2, 'networkTopology')
ixNet.commit()
netTopologyRing = ixNet.add(Network_Topology, 'netTopologyRing')
ixNet.setMultiAttribute(netTopologyRing,
	'-nodes', '10')
ixNet.commit()
deviceGroup_P2 = ixNet.add(networkGroup_P2, 'deviceGroup')
ixNet.setMultiAttribute(deviceGroup_P2,
	'-multiplier', '1',
	'-name', 'PE1 BGP')
ixNet.commit()
ipv6Loopback_P2 = ixNet.add(deviceGroup_P2, 'ipv6Loopback')
ixNet.setMultiAttribute(ipv6Loopback_P2,
	'-stackedLayers', [],
	'-name', 'IPv6 Loopback 1')
ixNet.commit()
address = ixNet.getAttribute(ipv6Loopback_P2, '-address')
ixNet.setMultiAttribute(address,
	'-clearOverlays', 'false')
ixNet.commit()
singleValue2 = ixNet.add(address, 'singleValue')
ixNet.setMultiAttribute(singleValue2,
	'-value', '1001:0:0:1:0:0:0:4')
ixNet.commit()
bgpIpv6Peer1 = ixNet.add(ipv6Loopback_P2, 'bgpIpv6Peer')
ixNet.setMultiAttribute(bgpIpv6Peer1,
	'-stackedLayers', [],
	'-name', 'BGP+ Peer 1')
ixNet.commit()
dutIp1 = ixNet.getAttribute(bgpIpv6Peer1, '-dutIp')
ixNet.setMultiAttribute(dutIp2,
	'-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(dutIp1, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', '1000:0:0:2:0:0:0:1')
ixNet.commit()
bgpV6Vrf2 = ixNet.add(bgpIpv6Peer1, 'bgpV6Vrf')
ixNet.setMultiAttribute(bgpV6Vrf2,
	'-stackedLayers', [],
	'-name', 'BGP+ VRF 1')
ixNet.commit()
networkGroup1 = ixNet.add(deviceGroup_P2, 'networkGroup')
ixNet.commit()
ixNet.setMultiAttribute(networkGroup1,
	'-name', 'CE1')
ixNet.commit()
ipv4PrefixPools1 = ixNet.add(networkGroup1, 'ipv4PrefixPools')
ixNet.setMultiAttribute(ipv4PrefixPools1,
	'-addrStepSupported', 'true',
	'-name', 'CE1')
ixNet.commit()
networkAddress = ixNet.getAttribute(ipv4PrefixPools1, '-networkAddress')
ixNet.setMultiAttribute(networkAddress,
	'-clearOverlays', 'false')
ixNet.commit()
counter = ixNet.add(networkAddress, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '0.1.0.0',
	'-start', '200.1.0.0',
	'-direction', 'increment')
ixNet.commit()

#Enable the field of "Enable SR-IPv6"
print "Enable the field of Enable SR-IPv6"
ipv6Srh = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1', '-ipv6Srh')
ixNet.setMultiAttribute(ipv6Srh, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(ipv6Srh, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()

#Configure Node prefix sRv6NodePrefix
print "Configure Node prefix sRv6NodePrefix"
sRv6NodePrefix1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1', '-sRv6NodePrefix')
counter_2 = ixNet.add(sRv6NodePrefix1, 'counter')
ixNet.setMultiAttribute(counter_2,
	'-step', '0:0:0:0:0:0:0:1',
	'-start', '1001:0:0:1:0:0:0:1',
	'-direction', 'increment')
ixNet.commit()

#Configure SID Count in isisPseudoSRv6LocatorEntryList for Simulated PE Nodes
print "Configure SID Count in isisPseudoSRv6LocatorEntryList for Simulated PE Nodes"
ixNet.setMultiAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/isisPseudoSRv6LocatorEntryList', '-sidCount', '3')
ixNet.commit()

#Configure C flag for isisPseudoSRv6EndSIDList
print "Configure C flag for isisPseudoSRv6EndSIDList"
cFlag_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/isisPseudoSRv6LocatorEntryList/isisPseudoSRv6EndSIDList', '-cFlag')
ixNet.commit()
singleValue = ixNet.add(cFlag_1, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'false')
ixNet.commit()
overlay = ixNet.add(cFlag_1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '2',
	'-value', 'true')
ixNet.commit()
overlay = ixNet.add(cFlag_1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '5',
	'-value', 'true')
ixNet.commit()
overlay = ixNet.add(cFlag_1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '8',
	'-value', 'true')
ixNet.commit()
overlay = ixNet.add(cFlag_1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '11',
	'-value', 'true')
ixNet.commit()
overlay = ixNet.add(cFlag_1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '14',
	'-value', 'true')
ixNet.commit()
overlay = ixNet.add(cFlag_1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '17',
	'-value', 'true')
ixNet.commit()
overlay = ixNet.add(cFlag_1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '20',
	'-value', 'true')
ixNet.commit()
overlay = ixNet.add(cFlag_1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '23',
	'-value', 'true')
ixNet.commit()
overlay = ixNet.add(cFlag_1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '26',
	'-value', 'true')
ixNet.commit()
overlay = ixNet.add(cFlag_1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '2',
	'-index', '29',
	'-value', 'true')
ixNet.commit()

#Configure endPointFunction for isisPseudoSRv6EndSIDList
print "Configure endPointFunction for isisPseudoSRv6EndSIDList"
endPointFunction_pseudo = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/isisPseudoSRv6LocatorEntryList/isisPseudoSRv6EndSIDList', '-endPointFunction')
ixNet.commit()
singleValue_2 = ixNet.add(endPointFunction_pseudo, 'singleValue')
ixNet.setMultiAttribute(singleValue_2,
	'-value', 'end_psp_usp')
ixNet.commit()
ov1 = ixNet.add(endPointFunction_pseudo, 'overlay')
ixNet.setMultiAttribute(ov1,
	'-count', '1',
	'-index', '2',
	'-value', 'end_psp_usp_coc')
ixNet.commit()
ov2 = ixNet.add(endPointFunction_pseudo, 'overlay')
ixNet.setMultiAttribute(ov2,
	'-count', '1',
	'-index', '5',
	'-value', 'end_psp_usp_coc')
ixNet.commit()
ov3 = ixNet.add(endPointFunction_pseudo, 'overlay')
ixNet.setMultiAttribute(ov3,
	'-count', '1',
	'-index', '8',
	'-value', 'end_psp_usp_coc')
ixNet.commit()
ov4 = ixNet.add(endPointFunction_pseudo, 'overlay')
ixNet.setMultiAttribute(ov4,
	'-count', '1',
	'-index', '11',
	'-value', 'end_psp_usp_coc')
ixNet.commit()
ov5 = ixNet.add(endPointFunction_pseudo, 'overlay')
ixNet.setMultiAttribute(ov5,
	'-count', '1',
	'-index', '14',
	'-value', 'end_psp_usp_coc')
ixNet.commit()
ov6 = ixNet.add(endPointFunction_pseudo, 'overlay')
ixNet.setMultiAttribute(ov6,
	'-count', '1',
	'-index', '17',
	'-value', 'end_psp_usp_coc')
ixNet.commit()
ov7 = ixNet.add(endPointFunction_pseudo, 'overlay')
ixNet.setMultiAttribute(ov7,
	'-count', '1',
	'-index', '20',
	'-value', 'end_psp_usp_coc')
ixNet.commit()
ov8 = ixNet.add(endPointFunction_pseudo, 'overlay')
ixNet.setMultiAttribute(ov8,
	'-count', '1',
	'-index', '23',
	'-value', 'end_psp_usp_coc')
ixNet.commit()
ov9 = ixNet.add(endPointFunction_pseudo, 'overlay')
ixNet.setMultiAttribute(ov9,
	'-count', '1',
	'-index', '26',
	'-value', 'end_psp_usp_coc')
ixNet.commit()
ov10 = ixNet.add(endPointFunction_pseudo, 'overlay')
ixNet.setMultiAttribute(ov10,
	'-count', '1',
	'-index', '29',
	'-value', 'end_psp_usp_coc')
ixNet.commit()

#Configure sid values for isisPseudoSRv6EndSIDList
print "Configure sid values for isisPseudoSRv6EndSIDList"
sid_values = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/isisPseudoSRv6LocatorEntryList/isisPseudoSRv6EndSIDList', '-sid')
ixNet.commit()
counter11 = ixNet.add(sid_values, 'counter')
ixNet.setMultiAttribute(counter11,
	'-step', '0:0:0:1:0:0:0:0',
	'-start', '5001:0:0:1:1:0:0:0',
	'-direction', 'increment')
ixNet.commit()
ixNet.setMultiAttribute(sid_values + '/nest:1',
	'-enabled', 'false',
	'-step', '0:0:0:0:0:0:0:1',)
ixNet.setMultiAttribute(sid_values + '/nest:2',
	'-enabled', 'true',
	'-step', '0:1:0:0:0:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '2',
	'-value', '5001:0:0:1:2:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '3',
	'-value', '5001:0:0:1:3:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '4',
	'-value', '5001:0:0:2:1:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '5',
	'-value', '5001:0:0:2:2:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '6',
	'-value', '5001:0:0:2:3:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '7',
	'-value', '5001:0:0:3:1:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '8',
	'-value', '5001:0:0:3:2:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '9',
	'-value', '5001:0:0:3:3:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '10',
	'-value', '5001:0:0:4:1:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '11',
	'-value', '5001:0:0:4:2:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '12',
	'-value', '5001:0:0:4:3:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '13',
	'-value', '5001:0:0:5:1:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '14',
	'-value', '5001:0:0:5:2:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '15',
	'-value', '5001:0:0:5:3:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '16',
	'-value', '5001:0:0:6:1:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '17',
	'-value', '5001:0:0:6:2:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '18',
	'-value', '5001:0:0:6:3:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '19',
	'-value', '5001:0:0:7:1:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '20',
	'-value', '5001:0:0:7:2:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '21',
	'-value', '5001:0:0:7:3:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '22',
	'-value', '5001:0:0:8:1:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '23',
	'-value', '5001:0:0:8:2:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '24',
	'-value', '5001:0:0:8:3:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '25',
	'-value', '5001:0:0:9:1:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '26',
	'-value', '5001:0:0:9:2:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '27',
	'-value', '5001:0:0:9:3:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '28',
	'-value', '5001:0:0:a:1:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '29',
	'-value', '5001:0:0:a:2:0:0:0')
ixNet.commit()
overlay = ixNet.add(sid_values, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '30',
	'-value', '5001:0:0:a:3:0:0:0')
ixNet.commit()

#Configure includeSRv6SIDStructureSubSubTlv for isisPseudoSRv6EndSIDList
print "Configure includeSRv6SIDStructureSubSubTlv for isisPseudoSRv6EndSIDList"
includeSRv6SIDStructureSubSubTlv_pseudo = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/isisPseudoSRv6LocatorEntryList/isisPseudoSRv6EndSIDList', '-includeSRv6SIDStructureSubSubTlv')
ixNet.commit()
singleValue_3 = ixNet.add(includeSRv6SIDStructureSubSubTlv_pseudo, 'singleValue')
ixNet.setMultiAttribute(singleValue_3,
	'-value', 'true')
ixNet.commit()
locatorBlockLength_pseudo = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/isisPseudoSRv6LocatorEntryList/isisPseudoSRv6EndSIDList', '-locatorBlockLength')
singleValu1 = ixNet.add(locatorBlockLength_pseudo, 'singleValue')
ixNet.setMultiAttribute(singleValu1,
	'-value', '48')
ixNet.commit()
ixNet.setMultiAttribute(locatorBlockLength_pseudo + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
ixNet.setMultiAttribute(locatorBlockLength_pseudo + '/nest:2',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
locatorNodeLength_pseudo = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/isisPseudoSRv6LocatorEntryList/isisPseudoSRv6EndSIDList', '-locatorNodeLength')
ixNet.commit()
singleValu2 = ixNet.add(locatorNodeLength_pseudo, 'singleValue')
ixNet.setMultiAttribute(singleValu2,
	'-value', '16')
ixNet.commit()
ixNet.setMultiAttribute(locatorNodeLength_pseudo + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.setMultiAttribute(locatorNodeLength_pseudo + '/nest:2',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
functionLength_pseudo = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/isisPseudoSRv6LocatorEntryList/isisPseudoSRv6EndSIDList', '-functionLength')
ixNet.commit()
singleValu4 = ixNet.add(functionLength_pseudo, 'singleValue')
ixNet.setMultiAttribute(singleValu4,
	'-value', '16')
ixNet.commit()

#Enable enableIPv6SID in isisL3PseudoInterface
print "Enable enableIPv6SID in isisL3PseudoInterface"
enableIPv6SID1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/isisL3PseudoInterface:1', '-enableIPv6SID')
singleValue = ixNet.add(enableIPv6SID1, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'true')
ixNet.commit()

#Change the Network Address of ISIS Simulated IPv6 Node Routers of Simulated Bridge
print "Change the Network Address of ISIS Simulated IPv6 Node Routers of Simulated Bridge"
networkAddress = ixNet.getAttribute(Network_Topology + '/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1', '-networkAddress')
ixNet.setMultiAttribute(networkAddress, '-clearOverlays', 'false')
ixNet.commit()
singleValue = ixNet.add(networkAddress, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '2222::1')
ixNet.commit()
#singleValue = (ixNet remapIds(singleValue)[0]
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
	'-valueStep', 'true',
	'-value', 'true')
ixNet.commit()
#overlay = (lindex (ixNet remapIds(overlay) 0)
overlay_1 = ixNet.add(active, 'overlay')
ixNet.setMultiAttribute(overlay_1,
	'-count', '1',
	'-index', '9',
	'-indexStep', '0',
	'-valueStep', 'true',
	'-value', 'true')
ixNet.commit()

#Enable enSRv6DataPlane
print "Enable enSRv6DataPlane"
ixNet.setMultiAttribute(bgpIpv6Peer1, '-enSRv6DataPlane', 'true')
ixNet.commit()
#Enable numberSRTEPolicies for bgpIpv6Peer1
print "Enable numberSRTEPolicies for bgpIpv6Peer1"
ixNet.setMultiAttribute(bgpIpv6Peer1, '-numberSRTEPolicies', '1')
ixNet.commit()
#Configure policyType for bgpIpv6Peer1
print "Configure policyType for bgpIpv6Peer1"
policyType = ixNet.getAttribute(bgpIpv6Peer1 + '/bgpSRTEPoliciesListV6', '-policyType')
singleValue = ixNet.add(policyType, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', 'ipv6')
ixNet.commit()
#Configure endPointV6 for bgpSRTEPoliciesListV6
print "Configure endPointV6 for bgpSRTEPoliciesListV6"
endPointV6 = ixNet.getAttribute(bgpIpv6Peer1 + '/bgpSRTEPoliciesListV6', '-endPointV6')
singleValue = ixNet.add(endPointV6, 'singleValue')
ixNet.setMultiAttribute(singleValue, '-value', '1000:0:0:2:0:0:0:1')
ixNet.commit()
#Configure numberOfSegmentsV6
print "Configure numberOfSegmentsV6"
ixNet.setMultiAttribute(bgpIpv6Peer1 + '/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6',
	'-numberOfSegmentsV6', '5')
ixNet.commit()

#Configure colorValue for bgpSRTEPoliciesTunnelEncapsulationListV6
print "Configure colorValue for bgpSRTEPoliciesTunnelEncapsulationListV6"
policyColor1 = ixNet.getAttribute(bgpIpv6Peer1 + '/bgpSRTEPoliciesListV6', '-policyColor')
singleVal4 = ixNet.add(policyColor1, 'singleValue')
ixNet.setMultiAttribute(singleVal4, '-value', '200')
ixNet.commit()
#Configure SegmentType
print "Configure SegmentType"
segmentType = ixNet.getAttribute(bgpIpv6Peer1 + '/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6', '-segmentType')
singleValue = ixNet.add(segmentType, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'typeb')
ixNet.commit()

#Configure ipv6SID for bgpSRTEPoliciesSegmentsCollectionV6
print "Configure ipv6SID for bgpSRTEPoliciesSegmentsCollectionV6"
ipv6SID1 = ixNet.getAttribute(bgpIpv6Peer1 + '/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6', '-ipv6SID')
counter = ixNet.add(ipv6SID1, 'counter')
ixNet.setMultiAttribute(counter,
	'-step', '0:0:0:1:0:0:0:0',
	'-start', '5001:0:0:5:1:0:0:0',
	'-direction', 'increment')
ixNet.commit()
ixNet.setMultiAttribute(ipv6SID1 + '/nest:1',
	'-enabled', 'false',
	'-step', '0:0:0:0:0:0:0:1')
ixNet.setMultiAttribute(ipv6SID1 + '/nest:2',
	'-enabled', 'false',
	'-step', '0:0:0:0:0:0:0:1')
ixNet.setMultiAttribute(ipv6SID1 + '/nest:3',
	'-enabled', 'false',
	'-step', '0:0:0:0:0:0:0:1')
ixNet.commit()
overlay = ixNet.add(ipv6SID1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '2',
	'-value', '5001:0:0:6:2:0:0:0')
ixNet.commit()
overlay = ixNet.add(ipv6SID1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '3',
	'-value', '5001:0:0:7:2:0:0:0')
ixNet.commit()
overlay = ixNet.add(ipv6SID1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '4',
	'-value', '5001:0:0:8:2:0:0:0')
ixNet.commit()
overlay = ixNet.add(ipv6SID1, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '5',
	'-value', '5001:0:0:a:3:0:0:0')
ixNet.commit()

#Configure End'-pointpoint
print "Configure End'-pointpoint"
endPointBehaviour11 = ixNet.getAttribute(bgpIpv6Peer1 + '/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6', '-endPointBehaviour')
singleValue = ixNet.add(endPointBehaviour11, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'end_psp_usp_coc')
ixNet.commit()

#Configure lbLength for bgpSRTEPoliciesSegmentsCollectionV6
print "Configure lbLength for bgpSRTEPoliciesSegmentsCollectionV6"
lbLength_policy = ixNet.getAttribute(bgpIpv6Peer1 + '/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6', '-lbLength')
singleValue = ixNet.add(lbLength_policy, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', '48')
ixNet.commit()
ixNet.setMultiAttribute(lbLength_policy + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.setMultiAttribute(lbLength_policy + '/nest:2',
	'-enabled', 'false',
	'-step', '1')
ixNet.setMultiAttribute(lbLength_policy + '/nest:3',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()

#Configure lnLength for bgpSRTEPoliciesSegmentsCollectionV6
print "Configure lnLength for bgpSRTEPoliciesSegmentsCollectionV6"
lnLength_policy = ixNet.getAttribute(bgpIpv6Peer1 + '/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6', '-lnLength')
singleValue = ixNet.add(lnLength_policy, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', '16')
ixNet.commit()
ixNet.setMultiAttribute(lnLength_policy + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.setMultiAttribute(lnLength_policy + '/nest:2',
	'-enabled', 'false',
	'-step', '1')
ixNet.setMultiAttribute(lnLength_policy + '/nest:3',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
#Configure funLength for bgpSRTEPoliciesSegmentsCollectionV6
print "Configure funLength for bgpSRTEPoliciesSegmentsCollectionV6"
funLength_policy = ixNet.getAttribute(bgpIpv6Peer1 + '/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6', '-funLength')
singleValue = ixNet.add(funLength_policy, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', '16')
ixNet.commit()
ixNet.setMultiAttribute(funLength_policy + '/nest:1',
	'-enabled', 'false',
	'-step', '1')
ixNet.setMultiAttribute(funLength_policy + '/nest:2',
	'-enabled', 'false',
	'-step', '1')
ixNet.setMultiAttribute(funLength_policy + '/nest:3',
	'-enabled', 'false',
	'-step', '1')
ixNet.commit()
#configure bFlag for bgpSRTEPoliciesSegmentsCollectionV6
print "configure bFlag for bgpSRTEPoliciesSegmentsCollectionV6"
bFlag_policy = ixNet.getAttribute(bgpIpv6Peer1 + '/bgpSRTEPoliciesListV6/bgpSRTEPoliciesTunnelEncapsulationListV6/bgpSRTEPoliciesSegmentListV6/bgpSRTEPoliciesSegmentsCollectionV6', '-bFlag')
singleValue = ixNet.add(bFlag_policy, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'true')
ixNet.commit()
overlay = ixNet.add(bFlag_policy, 'overlay')
ixNet.setMultiAttribute(overlay,
	'-count', '1',
	'-index', '1',
	'-value', 'false')
ixNet.commit()

#Configure capabilities in BGP
print "Configure capabilities in BGP"
capabilitySRTEPoliciesV6_1 = ixNet.getAttribute(bgpIpv6Peer1, '-capabilitySRTEPoliciesV6')
singleValue = ixNet.add(capabilitySRTEPoliciesV6_1, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'true')
ixNet.commit()
capabilitySRTEPoliciesV6_2 = ixNet.getAttribute(bgpIpv6Peer2, '-capabilitySRTEPoliciesV6')
singleValue = ixNet.add(capabilitySRTEPoliciesV6_2, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'true')
ixNet.commit()

#Configure Learned Routes Filter in bgpIpv6Peer1
print "Configure Learned Routes Filter in bgpIpv6Peer1"
filterIpV4MplsVpn1 = ixNet.getAttribute(bgpIpv6Peer1, '-filterIpV4MplsVpn')
singleValue = ixNet.add(filterIpV4MplsVpn1, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'true')
ixNet.commit()
filterIpV6MplsVpn1 = ixNet.getAttribute(bgpIpv6Peer1, '-filterIpV6MplsVpn')
singleValue = ixNet.add(filterIpV6MplsVpn1, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'true')
ixNet.commit()

#Configure Learned Routes Filter in bgpIpv6Peer2
print "Configure Learned Routes Filter in bgpIpv6Peer2"
filterIpV4MplsVpn2 = ixNet.getAttribute(bgpIpv6Peer2, '-filterIpV4MplsVpn')
singleValue = ixNet.add(filterIpV4MplsVpn2, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'true')
ixNet.commit()
filterIpV6MplsVpn2 = ixNet.getAttribute(bgpIpv6Peer2, '-filterIpV6MplsVpn')
singleValue = ixNet.add(filterIpV6MplsVpn2, 'singleValue')
ixNet.setMultiAttribute(singleValue,
	'-value', 'true')
ixNet.commit()

#Configure enableSrv6Sid for bgpV6L3VpnRouteProperty in CE1
print "Configure enableSrv6Sid for bgpV6L3VpnRouteProperty in CE1"
bgpV6L3VpnRouteProperty1 = ixNet.add(ipv4PrefixPools1, 'bgpV6L3VpnRouteProperty')
ixNet.setMultiAttribute(bgpV6L3VpnRouteProperty1,
	'-name', 'BGP+ L3 VPN Route Range 2')
ixNet.commit()
enableSrv6Sid_prefixpool = ixNet.getAttribute(bgpV6L3VpnRouteProperty1, '-enableSrv6Sid')
singlVal1 = ixNet.add(enableSrv6Sid_prefixpool, 'singleValue')
ixNet.setMultiAttribute(singlVal1,
	'-value', 'true')
ixNet.commit()

#Configure srv6SidLoc for bgpV6L3VpnRouteProperty IN CE1
print "Configure srv6SidLoc for bgpV6L3VpnRouteProperty IN CE1"
srv6SidLoc_prefixpool = ixNet.getAttribute(bgpV6L3VpnRouteProperty1, '-srv6SidLoc')
singlVal2 = ixNet.add(srv6SidLoc_prefixpool, 'singleValue')
ixNet.setMultiAttribute(singlVal2,
	'-value', '5001:0:0:4:45:0:0:0')
ixNet.commit()

#Enable enableExtendedCommunity on CE2
print "Enable enableExtendedCommunity on CE2"
bgpV6L3VpnRouteProperty = ixNet.add(ipv4PrefixPools, 'bgpV6L3VpnRouteProperty')
ixNet.setMultiAttribute(bgpV6L3VpnRouteProperty,
	'-name', 'BGP+ L3 VPN Route Range 1')
ixNet.commit()

enableExtendedCommunity = ixNet.getAttribute(bgpV6L3VpnRouteProperty, '-enableExtendedCommunity')
singlVal3 = ixNet.add(enableExtendedCommunity, 'singleValue')
ixNet.setMultiAttribute(singlVal3,
	'-value', 'true')
ixNet.commit()

#Configure enableSrv6Sid for bgpV6L3VpnRouteProperty in CE2
print "Configure enableSrv6Sid for bgpV6L3VpnRouteProperty in CE2"
ixNet.setMultiAttribute(bgpV6L3VpnRouteProperty,
	'-name', 'BGP+ L3 VPN Route Range 1')
ixNet.commit()
enableSrv6Sid_prefixpool = ixNet.getAttribute(bgpV6L3VpnRouteProperty, '-enableSrv6Sid')
singlVal1 = ixNet.add(enableSrv6Sid_prefixpool, 'singleValue')
ixNet.setMultiAttribute(singlVal1,
	'-value', 'true')
ixNet.commit()

#Configure srv6SidLoc for bgpV6L3VpnRouteProperty IN CE2
print "Configure srv6SidLoc for bgpV6L3VpnRouteProperty IN CE2"
srv6SidLoc_prefixpool1 = ixNet.getAttribute(bgpV6L3VpnRouteProperty, '-srv6SidLoc')
singlVal2 = ixNet.add(srv6SidLoc_prefixpool1, 'singleValue')
ixNet.setMultiAttribute(singlVal2,
	'-value', '5001:0:1:1:45:0:0:0')
ixNet.commit()

#Configure bgpExtendedCommunitiesList in bgpV6L3VpnRouteProperty for CE2
print "Configure bgpExtendedCommunitiesList in bgpV6L3VpnRouteProperty for CE2"
type_bgpExtendedCommunitiesList = ixNet.getAttribute(bgpV6L3VpnRouteProperty + '/bgpExtendedCommunitiesList:1', '-type')
singlVal4 = ixNet.add(type_bgpExtendedCommunitiesList, 'singleValue')
ixNet.setMultiAttribute(singlVal4,
	'-value', 'opaque')
ixNet.commit()
subType_bgpExtendedCommunitiesList = ixNet.getAttribute(bgpV6L3VpnRouteProperty + '/bgpExtendedCommunitiesList:1', '-subType')
singlVal5 = ixNet.add(subType_bgpExtendedCommunitiesList, 'singleValue')
ixNet.setMultiAttribute(singlVal5,
	'-value', 'color')
ixNet.commit()
colorValue_bgpExtendedCommunitiesList = ixNet.getAttribute(bgpV6L3VpnRouteProperty + '/bgpExtendedCommunitiesList:1', '-colorValue')
singlVal6 = ixNet.add(colorValue_bgpExtendedCommunitiesList, 'singleValue')
ixNet.setMultiAttribute(singlVal6,
	'-value', '200')
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
	'-name', 'CE1-CE2',
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
	'-sources',               [deviceGroup_P2],
	'-destinations',          [topo1])

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
