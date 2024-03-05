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
# damages limitations set forth herein and will not obligate Keysight to provide   #
# any additional maintenance or support services.                                  #
#                                                                                  #
####################################################################################   

################################################################################################
#                                                                                              #
# Description:                                                                                 #
#    This script intends to demonstrate how to use OSPFv3 SRv6 TCL APIs.                       #
#                                                                                              #
#    1. This configuration template provides an example of basic OSPFv3 Segment Routing over   #
#       IPV6 data plane configuration in back-to-back scenerio for point-to-point network.     #
#       One port emulates 1 OSPFv3 router and other port emulates 1 OSPFv3 router with a       #
#       Linear topology having 2 nodes behind it.Each node of linear topology are configured   #
#		with SRV6, also emulated OSPFv3 router are SRv6 enabled and it will providee the Locator#
#		and SID.                                                                               #
#    2. Start the OSPFV3 protocol.                                                             #
#    3. Retrieve protocol statistics.                                                          #
#    4. Stop all protocols.                                                                    #                                                                                          
################################################################################################   
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
ixTclPort   = '8012'
ports       = [('10.39.50.200', '1', '5',), ('10.39.50.200', '1', '6',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.50',
	 '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

################################################################################
# 1. Protocol configuration section. Configure ISIS as per the description
#    give above
################################################################################ 
root = ixNet.getRoot()
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

print ("Adding 2 vports")
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
ixNet.setAttribute(topo1, '-name', 'ospfv3 Topology 1')
ixNet.setAttribute(topo2, '-name', 'ospfv3 Topology 2')

print "Adding 2 device groups"
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices [0]
t2dev1 = t2devices [0]

ixNet.setAttribute(t1dev1, '-name', 'ospfv3 Topology 1 Router')
ixNet.setAttribute(t2dev1, '-name', 'ospfv3 Topology 2 Router')
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
print "Adding OSPFv3 over IPv6 stacks"
ixNet.add(ip1, 'ospfv3')
ixNet.add(ip2, 'ospfv3')
ixNet.commit()

ospfv3_1 = (ixNet.getList(ip1, 'ospfv3'))[0]
ospfv3_2 = (ixNet.getList(ip2, 'ospfv3'))[0]

ospfv3Rtr_1 = ixNet.getList(t1dev1, 'ospfv3Router')[0]
ospfv3Rtr_2 = ixNet.getList(t2dev1, 'ospfv3Router')[0]

#Change the Property of OSPFv3 IF
print "Change the Property of OSPFv3 IF"
Network_Type_1 = ixNet.getAttribute(ospfv3_1, '-networkType')
singleValue_1 = ixNet.add(Network_Type_1, 'singleValue')
ixNet.setMultiAttribute(singleValue_1, '-value', 'pointtopoint')
ixNet.commit()
Network_Type_1 = ixNet.getAttribute(ospfv3_2, '-networkType')
singleValue_1 = ixNet.add(Network_Type_1, 'singleValue')
ixNet.setMultiAttribute(singleValue_1, '-value', 'pointtopoint')
ixNet.commit()

#Change the value of -enableIPv6SID
print "Change the value of enableIPv6SID"
enableIPv6SID_1 = ixNet.getAttribute(ospfv3_1, '-enableIPv6SID')
single_value_1 = ixNet.add(enableIPv6SID_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()
enableIPv6SID_1 = ixNet.getAttribute(ospfv3_2, '-enableIPv6SID')
single_value_1 = ixNet.add(enableIPv6SID_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Enable the ipv6Srh means Enable SR-IPv6
print "Enabling the ipv6Srh means Enable SR-IPv6"
ipv6Srh_1 = ixNet.getAttribute(ospfv3Rtr_1, '-ipv6Srh')
single_value_1 = ixNet.add(ipv6Srh_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

ipv6Srh_1 = ixNet.getAttribute(ospfv3Rtr_2, '-ipv6Srh')
single_value_1 = ixNet.add(ipv6Srh_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value flagOfSRv6Cap 
print "Change the value flagOfSRv6Cap"
flagOfSRv6Cap_1 = ixNet.getAttribute(ospfv3Rtr_1, '-flagOfSRv6Cap')
single_value_1 = ixNet.add(flagOfSRv6Cap_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '4000')
ixNet.commit()

flagOfSRv6Cap_1 = ixNet.getAttribute(ospfv3Rtr_2, '-flagOfSRv6Cap')
single_value_1 = ixNet.add(flagOfSRv6Cap_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '4000')
ixNet.commit()

#Change the value reservedInsideSRv6Cap 
print "Change the value reservedInsideSRv6Cap"
reservedInsideSRv6Cap_1 = ixNet.getAttribute(ospfv3Rtr_1, '-reservedInsideSRv6Cap')
single_value_1 = ixNet.add(reservedInsideSRv6Cap_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '3fff')
ixNet.commit()

reservedInsideSRv6Cap_1 = ixNet.getAttribute(ospfv3Rtr_2, '-reservedInsideSRv6Cap')
single_value_1 = ixNet.add(reservedInsideSRv6Cap_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '3fff')
ixNet.commit()

#Change the value sRv6NodePrefix 
print "Change the value sRv6NodePrefix"
sRv6NodePrefix_1 = ixNet.getAttribute(ospfv3Rtr_1, '-sRv6NodePrefix')
single_value_1 = ixNet.add(sRv6NodePrefix_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '2000:0:0:1:0:0:0:1')
ixNet.commit()

sRv6NodePrefix_1 = ixNet.getAttribute(ospfv3Rtr_2, '-sRv6NodePrefix')
single_value_1 = ixNet.add(sRv6NodePrefix_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '2000:0:0:1:0:0:0:2')
ixNet.commit()

#Change the value srv6PrefixOptions 
print "Change the value srv6PrefixOptions"
srv6PrefixOptions_1 = ixNet.getAttribute(ospfv3Rtr_1, '-srv6PrefixOptions')
single_value_1 = ixNet.add(srv6PrefixOptions_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '128')
ixNet.commit()

srv6PrefixOptions_1 = ixNet.getAttribute(ospfv3Rtr_2, '-srv6PrefixOptions')
single_value_1 = ixNet.add(srv6PrefixOptions_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '128')
ixNet.commit()


#Change the value advertiseNodeMsd 
print "Change the value advertiseNodeMsd"
advertiseNodeMsd_1 = ixNet.getAttribute(ospfv3Rtr_1, '-advertiseNodeMsd')
single_value_1 = ixNet.add(advertiseNodeMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

advertiseNodeMsd_1 = ixNet.getAttribute(ospfv3Rtr_2, '-advertiseNodeMsd')
single_value_1 = ixNet.add(advertiseNodeMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value includeMaxSlMsd 
print "Change the value includeMaxSlMsd"
includeMaxSlMsd_1 = ixNet.getAttribute(ospfv3Rtr_1, '-includeMaxSlMsd')
single_value_1 = ixNet.add(includeMaxSlMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

includeMaxSlMsd_1 = ixNet.getAttribute(ospfv3Rtr_2, '-includeMaxSlMsd')
single_value_1 = ixNet.add(includeMaxSlMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value includeMaximumEndPopMsd 
print "Change the value includeMaximumEndPopMsd"
includeMaximumEndPopMsd_1 = ixNet.getAttribute(ospfv3Rtr_1, '-includeMaximumEndPopMsd')
single_value_1 = ixNet.add(includeMaximumEndPopMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

includeMaximumEndPopMsd_1 = ixNet.getAttribute(ospfv3Rtr_2, '-includeMaximumEndPopMsd')
single_value_1 = ixNet.add(includeMaximumEndPopMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value includeMaximumHEncapMsd 
print "Change the value includeMaximumHEncapMsd"
includeMaximumHEncapMsd_1 = ixNet.getAttribute(ospfv3Rtr_1, '-includeMaximumHEncapMsd')
single_value_1 = ixNet.add(includeMaximumHEncapMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

includeMaximumHEncapMsd_1 = ixNet.getAttribute(ospfv3Rtr_2, '-includeMaximumHEncapMsd')
single_value_1 = ixNet.add(includeMaximumHEncapMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value includeMaximumEndDMsd 
print "Change the value includeMaximumEndDMsd"
includeMaximumEndDMsd_1 = ixNet.getAttribute(ospfv3Rtr_1, '-includeMaximumEndDMsd')
single_value_1 = ixNet.add(includeMaximumEndDMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

includeMaximumEndDMsd_1 = ixNet.getAttribute(ospfv3Rtr_2, '-includeMaximumEndDMsd')
single_value_1 = ixNet.add(includeMaximumEndDMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value maxSlMsd 
print "Change the value maxSlMsd"
maxSlMsd_1 = ixNet.getAttribute(ospfv3Rtr_1, '-maxSlMsd')
single_value_1 = ixNet.add(maxSlMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()

maxSlMsd_1 = ixNet.getAttribute(ospfv3Rtr_2, '-maxSlMsd')
single_value_1 = ixNet.add(maxSlMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()

#Change the value maxEndPopMsd 
print "Change the value maxEndPopMsd"
maxEndPopMsd_1 = ixNet.getAttribute(ospfv3Rtr_1, '-maxEndPopMsd')
single_value_1 = ixNet.add(maxEndPopMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()

maxEndPopMsd_1 = ixNet.getAttribute(ospfv3Rtr_2, '-maxEndPopMsd')
single_value_1 = ixNet.add(maxEndPopMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()

#Change the value maxHEncapsMsd 
print "Change the value maxHEncapsMsd"
maxHEncapsMsd_1 = ixNet.getAttribute(ospfv3Rtr_1, '-maxHEncapsMsd')
single_value_1 = ixNet.add(maxHEncapsMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()

maxHEncapsMsd_1 = ixNet.getAttribute(ospfv3Rtr_2, '-maxHEncapsMsd')
single_value_1 = ixNet.add(maxHEncapsMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()

#Change the value maxEndDMsd 
print "Change the value maxEndDMsd"
maxEndDMsd_1 = ixNet.getAttribute(ospfv3Rtr_1, '-maxEndDMsd')
single_value_1 = ixNet.add(maxEndDMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()

maxEndDMsd_1 = ixNet.getAttribute(ospfv3Rtr_2, '-maxEndDMsd')
single_value_1 = ixNet.add(maxEndDMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()


#Change the value of locatorCount 
print "Change the value of locatorCount"
ixNet.setAttribute(ospfv3Rtr_1, '-locatorCount', '1')
ixNet.commit()
ixNet.setAttribute(ospfv3Rtr_2, '-locatorCount', '1')
ixNet.commit()

#Change the value metric 
print "Change the value metric"
metric_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList', '-metric')
single_value_1 = ixNet.add(metric_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '1')
ixNet.commit()

metric_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList', '-metric')
single_value_1 = ixNet.add(metric_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '1')
ixNet.commit()

#Change the value algorithm 
print "Change the value algorithm"
algorithm_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList', '-algorithm')
single_value_1 = ixNet.add(algorithm_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '1')
ixNet.commit()

algorithm_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList', '-algorithm')
single_value_1 = ixNet.add(algorithm_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '1')
ixNet.commit()

#Change the value nBit 
print "Change the value nBit"
nBit_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList', '-nBit')
single_value_1 = ixNet.add(nBit_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

nBit_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList', '-nBit')
single_value_1 = ixNet.add(nBit_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value aBit 
print "Change the value aBit"
aBit_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList', '-aBit')
single_value_1 = ixNet.add(aBit_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

aBit_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList', '-aBit')
single_value_1 = ixNet.add(aBit_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value reservedFlag 
print "Change the value reservedFlag"
reservedFlag_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList', '-reservedFlag')
single_value_1 = ixNet.add(reservedFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '01')
ixNet.commit()

reservedFlag_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList', '-reservedFlag')
single_value_1 = ixNet.add(reservedFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '01')
ixNet.commit()

#Change the value locatorLength 
print "Change the value locatorLength"
locatorLength_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList', '-locatorLength')
single_value_1 = ixNet.add(locatorLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '64')
ixNet.commit()

locatorLength_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList', '-locatorLength')
single_value_1 = ixNet.add(locatorLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '64')
ixNet.commit()

#Change the value advertiseLocatorAsPrefix 
print "Change the value advertiseLocatorAsPrefix"
advertiseLocatorAsPrefix_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList', '-advertiseLocatorAsPrefix')
single_value_1 = ixNet.add(advertiseLocatorAsPrefix_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

advertiseLocatorAsPrefix_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList', '-advertiseLocatorAsPrefix')
single_value_1 = ixNet.add(advertiseLocatorAsPrefix_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value locatorRouteType 
print "Change the value locatorRouteType"
locatorRouteType_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList', '-locatorRouteType')
single_value_1 = ixNet.add(locatorRouteType_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'intraarea')
ixNet.commit()

locatorRouteType_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList', '-locatorRouteType')
single_value_1 = ixNet.add(locatorRouteType_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'intraarea')
ixNet.commit()

#Change the value prefixMetric 
print "Change the value prefixMetric"
prefixMetric_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList', '-prefixMetric')
single_value_1 = ixNet.add(prefixMetric_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '10')
ixNet.commit()

prefixMetric_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList', '-prefixMetric')
single_value_1 = ixNet.add(prefixMetric_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '10')
ixNet.commit()


#Change the value flags 
print "Change the value flags"
flags_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-flags')
single_value_1 = ixNet.add(flags_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '01')
ixNet.commit()

flags_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-flags')
single_value_1 = ixNet.add(flags_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '01')
ixNet.commit()

#Change the value reserved 
print "Change the value reserved"
reserved_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-reserved')
single_value_1 = ixNet.add(reserved_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '02')
ixNet.commit()

reserved_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-reserved')
single_value_1 = ixNet.add(reserved_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '02')
ixNet.commit()

#Change the value endPointFunction 
print "Change the value endPointFunction"
endPointFunction_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-endPointFunction')
single_value_1 = ixNet.add(endPointFunction_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()

endPointFunction_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-endPointFunction')
single_value_1 = ixNet.add(endPointFunction_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()

#Change the value includeSRv6SIDStructureSubTlv 
print "Change the value includeSRv6SIDStructureSubTlv"
includeSRv6SIDStructureSubTlv_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-includeSRv6SIDStructureSubTlv')
single_value_1 = ixNet.add(includeSRv6SIDStructureSubTlv_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

includeSRv6SIDStructureSubTlv_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-includeSRv6SIDStructureSubTlv')
single_value_1 = ixNet.add(includeSRv6SIDStructureSubTlv_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()


#Change the value locatorBlockLength 
print "Change the value locatorBlockLength"
locatorBlockLength_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-locatorBlockLength')
single_value_1 = ixNet.add(locatorBlockLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '40')
ixNet.commit()

locatorBlockLength_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-locatorBlockLength')
single_value_1 = ixNet.add(locatorBlockLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '40')
ixNet.commit()

#Change the value locatorNodeLength 
print "Change the value locatorNodeLength"
locatorNodeLength_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-locatorNodeLength')
single_value_1 = ixNet.add(locatorNodeLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '24')
ixNet.commit()

locatorNodeLength_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-locatorNodeLength')
single_value_1 = ixNet.add(locatorNodeLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '24')
ixNet.commit()

#Change the value functionLength 
print "Change the value functionLength"
functionLength_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-functionLength')
single_value_1 = ixNet.add(functionLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '16')
ixNet.commit()

functionLength_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-functionLength')
single_value_1 = ixNet.add(functionLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '16')
ixNet.commit()

#Change the value argumentLength 
print "Change the value argumentLength"
argumentLength_1 = ixNet.getAttribute(ospfv3Rtr_1 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-argumentLength')
single_value_1 = ixNet.add(argumentLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '0')
ixNet.commit()

argumentLength_1 = ixNet.getAttribute(ospfv3Rtr_2 + '/ospfv3SRv6LocatorEntryList/ospfv3SRv6EndSIDList', '-argumentLength')
single_value_1 = ixNet.add(argumentLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '0')
ixNet.commit()

#Change the value bFlag 
print "Change the value bFlag"
bFlag_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-bFlag')
single_value_1 = ixNet.add(bFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

bFlag_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-bFlag')
single_value_1 = ixNet.add(bFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value sFlag 
print "Change the value sFlag"
sFlag_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-sFlag')
single_value_1 = ixNet.add(sFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

sFlag_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-sFlag')
single_value_1 = ixNet.add(sFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value pFlag 
print "Change the value pFlag"
pFlag_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-pFlag')
single_value_1 = ixNet.add(pFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

pFlag_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-pFlag')
single_value_1 = ixNet.add(pFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()


#Change the value reservedFlag 
print "Change the value reservedFlag"
reservedFlag_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-reservedFlag')
single_value_1 = ixNet.add(reservedFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '01')
ixNet.commit()

reservedFlag_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-reservedFlag')
single_value_1 = ixNet.add(reservedFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '01')
ixNet.commit()

#Change the value algorithm 
print "Change the value algorithm"
algorithm_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-algorithm')
single_value_1 = ixNet.add(algorithm_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '1')
ixNet.commit()

algorithm_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-algorithm')
single_value_1 = ixNet.add(algorithm_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '1')
ixNet.commit()

#Change the value weight 
print "Change the value weight"
weight_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-weight')
single_value_1 = ixNet.add(weight_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '100')
ixNet.commit()

weight_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-weight')
single_value_1 = ixNet.add(weight_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '100')
ixNet.commit()

#Change the value reserved1 
print "Change the value reserved1"
reserved1_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-reserved1')
single_value_1 = ixNet.add(reserved1_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '01')
ixNet.commit()

reserved1_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-reserved1')
single_value_1 = ixNet.add(reserved1_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '01')
ixNet.commit()

#Change the value reserved2 
print "Change the value reserved2"
reserved2_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-reserved2')
single_value_1 = ixNet.add(reserved2_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '0001')
ixNet.commit()

reserved2_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-reserved2')
single_value_1 = ixNet.add(reserved2_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '0001')
ixNet.commit()

#Change the value endPointFunction 
print "Change the value endPointFunction"
endPointFunction_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-endPointFunction')
single_value_1 = ixNet.add(endPointFunction_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '9')
ixNet.commit()

endPointFunction_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-endPointFunction')
single_value_1 = ixNet.add(endPointFunction_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '9')
ixNet.commit()

#Change the value includeSRv6SIDStructureSubTlv 
print "Change the value includeSRv6SIDStructureSubTlv"
includeSRv6SIDStructureSubTlv_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-includeSRv6SIDStructureSubTlv')
single_value_1 = ixNet.add(includeSRv6SIDStructureSubTlv_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

includeSRv6SIDStructureSubTlv_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-includeSRv6SIDStructureSubTlv')
single_value_1 = ixNet.add(includeSRv6SIDStructureSubTlv_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value locatorBlockLength 
print "Change the value locatorBlockLength"
locatorBlockLength_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-locatorBlockLength')
single_value_1 = ixNet.add(locatorBlockLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '40')
ixNet.commit()

locatorBlockLength_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-locatorBlockLength')
single_value_1 = ixNet.add(locatorBlockLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '40')
ixNet.commit()

#Change the value locatorNodeLength 
print "Change the value locatorNodeLength"
locatorNodeLength_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-locatorNodeLength')
single_value_1 = ixNet.add(locatorNodeLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '24')
ixNet.commit()

locatorNodeLength_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-locatorNodeLength')
single_value_1 = ixNet.add(locatorNodeLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '24')
ixNet.commit()

#Change the value functionLength 
print "Change the value functionLength"
functionLength_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-functionLength')
single_value_1 = ixNet.add(functionLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '16')
ixNet.commit()

functionLength_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-functionLength')
single_value_1 = ixNet.add(functionLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '16')
ixNet.commit()

#Change the value argumentLength 
print "Change the value argumentLength"
argumentLength_1 = ixNet.getAttribute(ospfv3_1 + '/ospfv3SRv6AdjSIDList', '-argumentLength')
single_value_1 = ixNet.add(argumentLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '0')
ixNet.commit()

argumentLength_1 = ixNet.getAttribute(ospfv3_2 + '/ospfv3SRv6AdjSIDList', '-argumentLength')
single_value_1 = ixNet.add(argumentLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '0')
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
netTopologyLinear = ixNet.add(Network_Topology, 'netTopologyLinear')
ixNet.commit()
netTopologyLinear = ixNet.remapIds(netTopologyLinear)[0]
ixNet.setMultiAttribute(netTopologyLinear, '-nodes', '4')
ixNet.commit()

#Enable the ipv6Srh means Enable SR-IPv6 ospfv3PseudoRouter
print "Enabling the ipv6Srh means Enable SR-IPv6 ospfv3PseudoRouter"
ipv6Srh_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-ipv6Srh')
single_value_1 = ixNet.add(ipv6Srh_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value flagOfSRv6Cap 
print "Change the value flagOfSRv6Cap"
flagOfSRv6Cap_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-flagOfSRv6Cap')
single_value_1 = ixNet.add(flagOfSRv6Cap_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '4000')
ixNet.commit()

#Change the value reservedInsideSRv6Cap 
print "Change the value reservedInsideSRv6Cap"
reservedInsideSRv6Cap_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-reservedInsideSRv6Cap')
single_value_1 = ixNet.add(reservedInsideSRv6Cap_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '3fff')
ixNet.commit()

#Change the value sRv6NodePrefix 
print "Change the value sRv6NodePrefix"
sRv6NodePrefix_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-sRv6NodePrefix')
single_value_1 = ixNet.add(sRv6NodePrefix_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '2000:0:0:1:0:0:0:1')
ixNet.commit()

#Change the value srv6PrefixOptions 
print "Change the value srv6PrefixOptions"
srv6PrefixOptions_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-srv6PrefixOptions')
single_value_1 = ixNet.add(srv6PrefixOptions_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '128')
ixNet.commit()


#Change the value advertiseNodeMsd 
print "Change the value advertiseNodeMsd"
advertiseNodeMsd_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-advertiseNodeMsd')
single_value_1 = ixNet.add(advertiseNodeMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()


#Change the value includeMaxSlMsd 
print "Change the value includeMaxSlMsd"
includeMaxSlMsd_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-includeMaxSlMsd')
single_value_1 = ixNet.add(includeMaxSlMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()


#Change the value includeMaximumEndPopMsd 
print "Change the value includeMaximumEndPopMsd"
includeMaximumEndPopMsd_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-includeMaximumEndPopMsd')
single_value_1 = ixNet.add(includeMaximumEndPopMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()


#Change the value includeMaximumHEncapsMsd 
print "Change the value includeMaximumHEncapMsd"
includeMaximumHEncapMsd_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-includeMaximumHEncapsMsd')
single_value_1 = ixNet.add(includeMaximumHEncapMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value includeMaximumEndDMsd 
print "Change the value includeMaximumEndDMsd"
includeMaximumEndDMsd_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-includeMaximumEndDMsd')
single_value_1 = ixNet.add(includeMaximumEndDMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()


#Change the value maxSlMsd 
print "Change the value maxSlMsd"
maxSlMsd_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-maxSlMsd')
single_value_1 = ixNet.add(maxSlMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()


#Change the value maxEndPopMsd 
print "Change the value maxEndPopMsd"
maxEndPopMsd_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-maxEndPopMsd')
single_value_1 = ixNet.add(maxEndPopMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()



#Change the value maxHEncapsMsd 
print "Change the value maxHEncapsMsd"
maxHEncapsMsd_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-maxHEncapsMsd')
single_value_1 = ixNet.add(maxHEncapsMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()


#Change the value maxEndDMsd 
print "Change the value maxEndDMsd"
maxEndDMsd_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1', '-maxEndDMsd')
single_value_1 = ixNet.add(maxEndDMsd_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '5')
ixNet.commit()

#Change the value metric 
print "Change the value metric"
metric_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList', '-metric')
single_value_1 = ixNet.add(metric_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '1')
ixNet.commit()

#Change the value algorithm 
print "Change the value algorithm"
algorithm_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList', '-algorithm')
single_value_1 = ixNet.add(algorithm_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '1')
ixNet.commit()


#Change the value nBit 
print "Change the value nBit"
nBit_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList', '-nBit')
single_value_1 = ixNet.add(nBit_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()


#Change the value aBit 
print "Change the value aBit"
aBit_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList', '-aBit')
single_value_1 = ixNet.add(aBit_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value reservedFlag 
print "Change the value reservedFlag"
reservedFlag_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList', '-reservedFlag')
single_value_1 = ixNet.add(reservedFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '01')
ixNet.commit()


#Change the value locatorLength 
print "Change the value locatorLength"
locatorLength_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList', '-locatorLength')
single_value_1 = ixNet.add(locatorLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '64')
ixNet.commit()


#Change the value advertiseLocatorAsPrefix 
print "Change the value advertiseLocatorAsPrefix"
advertiseLocatorAsPrefix_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList', '-advertiseLocatorAsPrefix')
single_value_1 = ixNet.add(advertiseLocatorAsPrefix_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()


#Change the value locatorRouteType 
print "Change the value locatorRouteType"
locatorRouteType_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList', '-locatorRouteType')
single_value_1 = ixNet.add(locatorRouteType_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'intraarea')
ixNet.commit()


#Change the value prefixMetric 
print "Change the value prefixMetric"
prefixMetric_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList', '-prefixMetric')
single_value_1 = ixNet.add(prefixMetric_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '10')
ixNet.commit()


#Change the value flags 
print "Change the value flags"
flags_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList', '-flags')
single_value_1 = ixNet.add(flags_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '01')
ixNet.commit()

#Change the value reserved 
print "Change the value reserved"
reserved_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList', '-reserved')
single_value_1 = ixNet.add(reserved_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '02')
ixNet.commit()


#Change the value endPointFunction 
print "Change the value endPointFunction"
endPointFunction_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList', '-endPointFunction')
single_value_1 = ixNet.add(endPointFunction_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'endt_nopsp_nousp')
ixNet.commit()


#Change the value includeSRv6SIDStructureSubTlv 
print "Change the value includeSRv6SIDStructureSubTlv"
includeSRv6SIDStructureSubTlv_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList', '-includeSRv6SIDStructureSubTlv')
single_value_1 = ixNet.add(includeSRv6SIDStructureSubTlv_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()


#Change the value locatorBlockLength 
print "Change the value locatorBlockLength"
locatorBlockLength_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList', '-locatorBlockLength')
single_value_1 = ixNet.add(locatorBlockLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '40')
ixNet.commit()


#Change the value locatorNodeLength 
print "Change the value locatorNodeLength"
locatorNodeLength_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList', '-locatorNodeLength')
single_value_1 = ixNet.add(locatorNodeLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '24')
ixNet.commit()


#Change the value functionLength 
print "Change the value functionLength"
functionLength_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList', '-functionLength')
single_value_1 = ixNet.add(functionLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '16')
ixNet.commit()


#Change the value argumentLength 
print "Change the value argumentLength"
argumentLength_1 = ixNet.getAttribute(Network_Topology + '/simRouter:1/ospfv3PseudoRouter:1/ospfv3PseudoSRv6LocatorEntryList/ospfv3PseudoSRv6EndSIDList', '-argumentLength')
single_value_1 = ixNet.add(argumentLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '0')
ixNet.commit()


#Change the value enableIPv6SID 
print "Change the value enableIPv6SID"
enableIPv6SID_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1', '-enableIPv6SID')
single_value_1 = ixNet.add(enableIPv6SID_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value bFlag 
print "Change the value bFlag"
bFlag_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-bFlag')
single_value_1 = ixNet.add(bFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value sFlag 
print "Change the value sFlag"
sFlag_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-sFlag')
single_value_1 = ixNet.add(sFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value pFlag 
print "Change the value pFlag"
pFlag_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-pFlag')
single_value_1 = ixNet.add(pFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value reservedFlag 
print "Change the value reservedFlag"
reservedFlag_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-reservedFlag')
single_value_1 = ixNet.add(reservedFlag_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '01')
ixNet.commit()

#Change the value algorithm 
print "Change the value algorithm"
algorithm_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-algorithm')
single_value_1 = ixNet.add(algorithm_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '1')
ixNet.commit()


#Change the value weight 
print "Change the value weight"
weight_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-weight')
single_value_1 = ixNet.add(weight_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '100')
ixNet.commit()

#Change the value reserved1 
print "Change the value reserved1"
reserved1_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-reserved1')
single_value_1 = ixNet.add(reserved1_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '01')
ixNet.commit()

#Change the value reserved2 
print "Change the value reserved2"
reserved2_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-reserved2')
single_value_1 = ixNet.add(reserved2_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '0001')
ixNet.commit()

#Change the value endPointFunction 
print "Change the value endPointFunction"
endPointFunction_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-endPointFunction')
single_value_1 = ixNet.add(endPointFunction_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'endt_nopsp_nousp')
ixNet.commit()

#Change the value includeSRv6SIDStructureSubTlv 
print "Change the value includeSRv6SIDStructureSubTlv"
includeSRv6SIDStructureSubTlv_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-includeSRv6SIDStructureSubTlv')
single_value_1 = ixNet.add(includeSRv6SIDStructureSubTlv_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

#Change the value locatorBlockLength 
print "Change the value locatorBlockLength"
locatorBlockLength_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-locatorBlockLength')
single_value_1 = ixNet.add(locatorBlockLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '40')
ixNet.commit()

#Change the value locatorNodeLength 
print "Change the value locatorNodeLength"
locatorNodeLength_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-locatorNodeLength')
single_value_1 = ixNet.add(locatorNodeLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '24')
ixNet.commit()

#Change the value functionLength 
print "Change the value functionLength"
functionLength_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-functionLength')
single_value_1 = ixNet.add(functionLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '16')
ixNet.commit()

#Change the value argumentLength 
print "Change the value argumentLength"
argumentLength_1 = ixNet.getAttribute(Network_Topology + '/simInterface:1/simInterfaceIPv6Config:1/ospfv3PseudoInterface:1/ospfv3PseudoSRv6AdjSIDList', '-argumentLength')
single_value_1 = ixNet.add(argumentLength_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', '0')
ixNet.commit()

################################################################################
# 2. Start OSPFv3 protocol and wait for 60 seconds
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
# 4. Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
print ('!!! Test Script Ends !!!')
