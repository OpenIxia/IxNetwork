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

#####################################################################################################        
#                                                                                                   #
# Description:                                                                                      #
#    This script intends to demonstrate how to use Flex-Algo Over  ISIS-SRv6 Using TCL APIs.        #  
#                                                                                                   #
#    1. It will create 2 ISISL3 topologies with Flex Algorithm enabled, each having an ipv6 network #                    
#       topology and loopback devicegroup behind the network group(NG) with loopback interface.     #
#    2. Configure ISIS with SRv6.                                                                   #
#    3. Configure Flex-Algo related fields one by one.                                              #
#    4. Start protocols                                                                             #
#    5. Retrieve protocol statistics.                                                               #
#    6. Retrieve protocol learned info.                                                             #
#    7. Stop all protocols.                                                                         #                                                                                          
##################################################################################################### 

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
ixTclServer = '10.39.50.121'
ixTclPort   = '8017'
ports       = [('10.39.50.179', '2', '1',), ('10.39.50.179', '2', '2',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '9.10',
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
ixNet.setAttribute(ixNet.getAttribute(mac1, '-mac') + '/singleValue',
    '-value', '18:03:73:C7:6C:B1')
ixNet.commit()

ixNet.setAttribute(ixNet.getAttribute(mac2, '-mac') + '/singleValue',
    '-value', '18:03:73:C7:6C:01')
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

isisL3_1 = ixNet.getList(mac1, 'isisL3')[0]
isisL3_2 = ixNet.getList(mac2, 'isisL3')[0]

print "Renaming the topologies and the device groups"
ixNet.setAttribute(topo1, '-name', 'isisL3 Topology 1')
ixNet.setAttribute(topo2, '-name', 'isisL3 Topology 2')

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

#Enable the ipv6Srh means Enable SR-IPv6
print "Enabling the ipv6Srh means Enable SR-IPv6"
ipv6Srh_1 = ixNet.getAttribute(t1dev1+'/isisL3Router:1', '-ipv6Srh')
ixNet.setMultiAttribute(ipv6Srh_1, '-clearOverlays', 'false')
ixNet.commit()

single_value_1 = ixNet.add(ipv6Srh_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, 
	'-value', 'true')
ixNet.commit()
		
ipv6Srh_2 = ixNet.getAttribute(t2dev1+'/isisL3Router:1', '-ipv6Srh')
ixNet.setMultiAttribute(ipv6Srh_2, '-clearOverlays', 'false')
ixNet.commit()

single_value_2 = ixNet.add(ipv6Srh_2, 'singleValue')
ixNet.setMultiAttribute(single_value_2, 
	'-value', 'true')
ixNet.commit()

#Change the value', 'of, '-enableIPv6SID
print "Change the valueenableIPv6SID"
enableIPv6SID_1 = ixNet.getAttribute(isisL3_1, '-enableIPv6SID')
ixNet.setMultiAttribute(enableIPv6SID_1, '-clearOverlays', 'false')
ixNet.commit()
single_value_1 = ixNet.add(enableIPv6SID_1, 'singleValue')
ixNet.setMultiAttribute(single_value_1, '-value', 'true')
ixNet.commit()

enableIPv6SID_2 = ixNet.getAttribute(isisL3_2, '-enableIPv6SID')
ixNet.setMultiAttribute(enableIPv6SID_2, '-clearOverlays', 'false')
ixNet.commit()
single_value2 = ixNet.add(enableIPv6SID_2, 'singleValue')
ixNet.setMultiAttribute(single_value2, '-value', 'true')
ixNet.commit()


#Flex Algorithm related Configuration
print "Setting Flex Algo Count"
ixNet.setAttribute(t1dev1+'/isisL3Router:1', '-flexAlgoCount', '4')
ixNet.setAttribute(t2dev1+'/isisL3Router:1', '-flexAlgoCount', '4')
ixNet.commit()

isisFlexAlgorithmList1 = ixNet.getList(t1dev1+'/isisL3Router:1', 'isisFlexAlgorithmList')
isisFlexAlgorithmList11 = isisFlexAlgorithmList1 [0]
isisFlexAlgorithmList2 = ixNet.getList(t2dev1+'/isisL3Router:1', 'isisFlexAlgorithmList')
isisFlexAlgorithmList12 = isisFlexAlgorithmList2 [0]

print "Setting Metric Type"
metricType1 = ixNet.getAttribute(t1dev1+'/isisL3Router:1/isisFlexAlgorithmList', '-metricType')
ixNet.setMultiAttribute(metricType1, 
	'-clearOverlays', 'false')
ixNet.commit()
singleValuemetricType1 = ixNet.add(metricType1, 'singleValue')
ixNet.setMultiAttribute(singleValuemetricType1, 
	'-value', '1')
ixNet.commit()

print "Setting Calc Type"
calcType1 = ixNet.getAttribute(t2dev1+'/isisL3Router:1/isisFlexAlgorithmList', '-calcType')
ixNet.setMultiAttribute(calcType1, 
	'-clearOverlays', 'false')
ixNet.commit()
singleValuecalcType1 = ixNet.add(metricType1, 'singleValue')
ixNet.setMultiAttribute(singleValuecalcType1, 
	'-value', '1')
ixNet.commit()

print "Setting priority Type"
priority1 = ixNet.getAttribute(isisFlexAlgorithmList11, '-priority')
ixNet.setMultiAttribute(priority1,
	'-clearOverlays', 'false')
ixNet.commit()
prioritycounter =ixNet.add(priority1, 'counter')
ixNet.setMultiAttribute(prioritycounter,
	'-step', '1',
	'-start', '100',
	'-direction', 'increment')
ixNet.commit()

print "Setting enable Exclude Ag"
enableExcludeAg1 = ixNet.getAttribute(t1dev1+'/isisL3Router:1/isisFlexAlgorithmList', '-enableExcludeAg')
ixNet.setMultiAttribute(enableExcludeAg1, 
	'-clearOverlays', 'false')
ixNet.commit()
singleValueenableExcludeAg1 = ixNet.add(enableExcludeAg1, 'singleValue')
ixNet.setMultiAttribute(singleValueenableExcludeAg1, 
	'-value', 'true')
ixNet.commit()

print "Setting Ext Ag Len"
excludeAgExtAgLen1 = ixNet.getAttribute(t1dev1+'/isisL3Router:1/isisFlexAlgorithmList', '-excludeAgExtAgLen')
ixNet.setMultiAttribute(excludeAgExtAgLen1, 
	'-clearOverlays', 'false')
ixNet.commit()
singleValueexcludeAgExtAgLen1 = ixNet.add(excludeAgExtAgLen1, 'singleValue')
ixNet.setMultiAttribute(singleValueexcludeAgExtAgLen1, 
	'-value', '2')
ixNet.commit()

print "set Ext-ExcludeAG Value .."
ExcludeAgExtAg =ixNet.getAttribute(isisFlexAlgorithmList11, '-excludeAgExtAg')
ixNet.setMultiAttribute(ExcludeAgExtAg,
	'-clearOverlays', 'false')
ixNet.commit()

excludeAgExtAgcounter =ixNet.add(ExcludeAgExtAg, 'counter')
ixNet.setMultiAttribute(excludeAgExtAgcounter,
	'-step', '01',
	'-start', '00000000',
	'-direction', 'increment')
ixNet.commit()

overlay1 =ixNet.add(ExcludeAgExtAg, 'overlay')
ixNet.setMultiAttribute(overlay1,
	'-count', '1',
	'-index', '1',
	'-value', '0000000000000005')
ixNet.commit()

overlay2 =ixNet.add(ExcludeAgExtAg, 'overlay')
ixNet.setMultiAttribute(overlay2,
	'-count', '1',
	'-index', '2',
	'-value', '0000000000000066')
ixNet.commit()

overlay3 =ixNet.add(ExcludeAgExtAg, 'overlay')
ixNet.setMultiAttribute(overlay3,
	'-count', '1',
	'-index', '3',
	'-value', '0000000000000077')
ixNet.commit()

overlay4 =ixNet.add(ExcludeAgExtAg, 'overlay')
ixNet.setMultiAttribute(overlay4,
	'-count', '1',
	'-index', '4',
	'-value', '0000000000000088')
ixNet.commit()

print "Setting enable Include Any Ag"
enableIncludeAnyAg1 = ixNet.getAttribute(isisFlexAlgorithmList11, '-enableIncludeAnyAg')
ixNet.setMultiAttribute(enableIncludeAnyAg1, 
	'-clearOverlays', 'false')
ixNet.commit()
singleValueenableIncludeAnyAg1= ixNet.add(enableIncludeAnyAg1, 'singleValue')
ixNet.setMultiAttribute(singleValueenableIncludeAnyAg1, 
	'-value', 'true')
ixNet.commit()

enableIncludeAnyAg2 = ixNet.getAttribute(isisFlexAlgorithmList12, '-enableIncludeAnyAg')
ixNet.setMultiAttribute(enableIncludeAnyAg2, 
	'-clearOverlays', 'false')
ixNet.commit()
singleValueenableIncludeAnyAg2 = ixNet.add(enableIncludeAnyAg2, 'singleValue')
ixNet.setMultiAttribute(singleValueenableIncludeAnyAg2, 
	'-value', 'true')
ixNet.commit()

print "Setting Ext Ag Len"
includeAnyAgExtAgLen1 = ixNet.getAttribute(isisFlexAlgorithmList11, '-includeAnyAgExtAgLen')
ixNet.setMultiAttribute(includeAnyAgExtAgLen1, 
	'-clearOverlays', 'false')
ixNet.commit()
singleValueincludeAnyAgExtAgLen1 = ixNet.add(includeAnyAgExtAgLen1, 'singleValue')
ixNet.setMultiAttribute(singleValueincludeAnyAgExtAgLen1, 
	'-value', '1')
ixNet.commit()

print "Setting include AnyAgExt"
includeAnyAgExtAg1 = ixNet.getAttribute(isisFlexAlgorithmList11, '-includeAnyAgExtAg')
ixNet.setMultiAttribute(includeAnyAgExtAg1, 
	'-clearOverlays', 'false')
ixNet.commit()
singleValueincludeAnyAgExtAg1 = ixNet.add(includeAnyAgExtAg1, 'singleValue')
ixNet.setMultiAttribute(singleValueincludeAnyAgExtAg1, 
	'-value', 'BB000001')
ixNet.commit()

includeAnyAgExtAg2 = ixNet.getAttribute(isisFlexAlgorithmList12, '-includeAnyAgExtAg')
ixNet.setMultiAttribute(includeAnyAgExtAg2, 
	'-clearOverlays', 'false')
ixNet.commit()
singleValueincludeAnyAgExtAg2 = ixNet.add(includeAnyAgExtAg2, 'singleValue')
ixNet.setMultiAttribute(singleValueincludeAnyAgExtAg2, 
	'-value', 'CD000001')
ixNet.commit()

print "Setting enable Include All Ag"
enableIncludeAllAg1 = ixNet.getAttribute(isisFlexAlgorithmList11, '-enableIncludeAllAg')
ixNet.setMultiAttribute(enableIncludeAllAg1, 
	'-clearOverlays', 'false')
ixNet.commit()
singleValueenableIncludeAllAg1 = ixNet.add(enableIncludeAllAg1, 'singleValue')
ixNet.setMultiAttribute(singleValueenableIncludeAllAg1, 
	'-value', 'true')
ixNet.commit()

print "Setting Ext Ag Len"
IncludeAllAgExtAgLen = ixNet.getAttribute(isisFlexAlgorithmList11, '-includeAllAgExtAgLen')
ixNet.setMultiAttribute(IncludeAllAgExtAgLen,
	'-clearOverlays', 'false')
ixNet.commit()

IncludeAllAgExtAgLencounter = ixNet.add(IncludeAllAgExtAgLen, 'counter')
ixNet.setMultiAttribute(IncludeAllAgExtAgLencounter,
	'-step', '1',
	'-start', '1',
	'-direction', 'increment')
ixNet.commit()

includeAllAgExtAgLen2 = ixNet.getAttribute(isisFlexAlgorithmList12, '-includeAllAgExtAgLen')
ixNet.setMultiAttribute(includeAllAgExtAgLen2, 
	'-clearOverlays', 'false')
ixNet.commit()
singleValueincludeAllAgExtAgLen = ixNet.add(includeAllAgExtAgLen2, 'singleValue')
ixNet.setMultiAttribute(singleValueincludeAllAgExtAgLen, 
	'-value', '1')
ixNet.commit()

print "Setting include AllAgExt"
IncludeAllAgExtAg = ixNet.getAttribute(isisFlexAlgorithmList11, '-includeAllAgExtAg')
ixNet.setMultiAttribute(IncludeAllAgExtAg,
	'-clearOverlays', 'false')
ixNet.commit()

includeallAgExtAgcounter = ixNet.add(IncludeAllAgExtAg, 'counter')
ixNet.setMultiAttribute(includeallAgExtAgcounter,
	'-step', '01',
	'-start', '00000000',
	'-direction', 'increment')
ixNet.commit()

overlay1 = ixNet.add(IncludeAllAgExtAg, 'overlay')
ixNet.setMultiAttribute(overlay1,
	'-count', '1',
	'-index', '1',
	'-value', '0000055')
ixNet.commit()

overlay2 = ixNet.add(IncludeAllAgExtAg, 'overlay')
ixNet.setMultiAttribute(overlay2,
	'-count', '1',
	'-index', '2',
	'-value', '0000000000000066')
ixNet.commit()

overlay3 = ixNet.add(IncludeAllAgExtAg, 'overlay')
ixNet.setMultiAttribute(overlay3,
	'-count', '1',
	'-index', '3',
	'-value', '000000000000000000000077')
ixNet.commit()

overlay4 = ixNet.add(IncludeAllAgExtAg, 'overlay')
ixNet.setMultiAttribute(overlay4,
	'-count', '1',
	'-index', '4',
	'-value', '00000000000000000000000000000088')
ixNet.commit()

print "Setting enableFadfTlv"
EnableFadfTlv = ixNet.getAttribute(isisFlexAlgorithmList11, '-enableFadfTlv')
ixNet.setMultiAttribute(EnableFadfTlv,
	'-clearOverlays', 'false')
ixNet.commit()

EnableFadfTlvalternate = ixNet.add(EnableFadfTlv, 'alternate')
ixNet.setMultiAttribute(EnableFadfTlvalternate,
	'-value', 'true')
ixNet.commit()


enableFadfTlv1 = ixNet.getAttribute(isisFlexAlgorithmList12, '-enableFadfTlv')
ixNet.setMultiAttribute(enableFadfTlv1, 
	'-clearOverlays', 'false')
ixNet.commit()

singleValueenableFadfTlv1 = ixNet.add(enableFadfTlv1, 'singleValue')
ixNet.setMultiAttribute(singleValueenableFadfTlv1, 
	'-value', 'true')
ixNet.commit()

print "Setting FAD Len"
fadfLen1 = ixNet.getAttribute(isisFlexAlgorithmList11, '-fadfLen')
ixNet.setMultiAttribute(fadfLen1, 
	'-clearOverlays', 'false')
ixNet.commit()

singleValuefadfLen1 = ixNet.add(fadfLen1, 'singleValue')
ixNet.setMultiAttribute(singleValuefadfLen1, 
	'-value', '1')
ixNet.commit()

fadfLen2 = ixNet.getAttribute(isisFlexAlgorithmList12, '-fadfLen')
ixNet.setMultiAttribute(fadfLen2,
	'-clearOverlays', 'false')
ixNet.commit()

fadflengthcounter = ixNet.add(fadfLen2, 'counter')
ixNet.setMultiAttribute(fadflengthcounter,
	'-step', '1',
	'-start', '1',
	'-direction', 'increment')
ixNet.commit()

print "Setting include mFlag"
mFlag1 = ixNet.getAttribute(isisFlexAlgorithmList11, '-mFlag')
ixNet.setMultiAttribute(mFlag1, 
	'-clearOverlays', 'false')
ixNet.commit()

singleValuEmFlag1 = ixNet.add(mFlag1, 'singleValue')
ixNet.setMultiAttribute(singleValuEmFlag1, 
	'-value', 'true')
ixNet.commit()

mFlag2 = ixNet.getAttribute(isisFlexAlgorithmList12, '-mFlag')
ixNet.setMultiAttribute(mFlag2,
	'-clearOverlays', 'false')
ixNet.commit()

singleValuemFlag2 = ixNet.add(mFlag2, 'singleValue')
ixNet.setMultiAttribute(singleValuemFlag2,
	'-value', 'true')
ixNet.commit()

mFlag2overlay = ixNet.add(mFlag2, 'overlay')
ixNet.setMultiAttribute(mFlag2overlay,
	'-count', '1',
	'-index', '1',
	'-value', 'false')
ixNet.commit()

print "Setting Reserved bits"
reservedBits2 = ixNet.getAttribute(isisFlexAlgorithmList12, '-reservedBits')
ixNet.setMultiAttribute(reservedBits2,
	'-clearOverlays', 'false')
ixNet.commit()

singleValuereservedBits2 = ixNet.add(reservedBits2, 'singleValue')
ixNet.setMultiAttribute(singleValuereservedBits2,
	'-value', '0xAB')
ixNet.commit()

reservedBits2counteroverlay1 = ixNet.add(reservedBits2, 'overlay')
ixNet.setMultiAttribute(reservedBits2counteroverlay1,
	'-count', '1',
	'-index', '3',
	'-value', '00AB',)
ixNet.commit()


reservedBits2counteroverlay2 = ixNet.add(reservedBits2, 'overlay')
ixNet.setMultiAttribute(reservedBits2counteroverlay2,
	'-count', '1',
	'-index', '4',
	'-value', '0000AB',)
ixNet.commit()

################################################################################
# 2. Start ISISl3 protocol and wait for 60 seconds
################################################################################
print 'Starting protocols and waiting for 60 seconds for protocols to come up'
ixNet.execute('startAllProtocols')
time.sleep(60)

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
print ("Verifying all the stats\n")
viewPage = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues'):
    for statVal in statValList :
        print ("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
print ("***************************************************")

################################################################################
# 8. Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
print ('!!! Test Script Ends !!!')
print "!!! Test Script Ends !!!"
