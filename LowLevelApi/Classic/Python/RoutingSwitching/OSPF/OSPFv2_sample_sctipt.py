# -*- coding: cp1252 -*-
# ###############################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    22/01/2015 - Sumit Deb - created sample                                   #
#                                                                              #
# ###############################################################################

# ###############################################################################
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
# Ixia does not gurantee (i) that the functions contained in the script will   #
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
# ###############################################################################

# ###############################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF OSPFv2 API.            #
#                                                                              #
#    1. Create 2 interfaces with OSPFv2 enabled, each having 1 OSPFv2          #
#       router with 1 route-range per router.							       #
#    2. Start the ospfv2 protocol.                                             #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #                                      
#    5. Configure L2-L3 traffic.                                               #
#    6. Start the L2-L3 traffic.                                               #
#    7. Retrieve L2-L3 traffic stats.                                          #
#    8. Stop L2-L3 traffic.                                                    #
#    9. Stop all protocols.                                                    #                                                                                    #              
# Ixia Softwares:                                                              #
#    IxOS      6.80 EA (6.80.1100.7)                                           #
#    IxNetwork 7.40 EA (7.40.929.15)                                           #
#                                                                              #
# ###############################################################################
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
ixNetPath = r'C:\Program Files\Ixia\IxNetwork\7.40-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.205.27.23'
ixTclPort   = '8009'
ports       = [('ixin-asd-2', '2', '1',), ('ixin-asd-2', '2', '2',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '7.40',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

################################################################################
# 1. Protocol configuration section. Configure OSPFv2 as per the description
#    given above
################################################################################ 
# Assign real ports
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

root    = ixNet.getRoot()
vPort1 = ixNet.getList(root, 'vport')[0]
vPort2 = ixNet.getList(root, 'vport')[1]

################################################################################
# Set ipv4 interfaces
################################################################################
print ("Set ipv4 interfaces") 
ixNet.add(vPort1, 'interface')
ixNet.add(vPort2, 'interface')
ixNet.commit()

interface1 = ixNet.getList(vPort1, 'interface')[0]
interface2 = ixNet.getList(vPort2, 'interface')[0]
ixNet.add(interface1, 'ipv4')
ixNet.add(interface2, 'ipv4')
ixNet.commit()

ipv41 = ixNet.getList(interface1, 'ipv4')[0]
ipv42 = ixNet.getList(interface2, 'ipv4')[0]

################################################################################
# Enable protocol interface
################################################################################
print ("Enable protocol interface")
ixNet.setAttribute(interface1, '-enabled', 'true')
ixNet.setAttribute(interface2, '-enabled', 'true')
ixNet.commit()

################################################################################
# Configure ip and gateway on each interface
################################################################################
print ("Add IP address, Gateway and Mask on Protocol Interface 1")
ixNet.setAttribute(ipv41, '-ip', '20.20.20.1')
ixNet.setAttribute(ipv41, '-maskWidth', '24')
ixNet.setAttribute(ipv41, '-gateway', '20.20.20.2')
ixNet.commit()

print ("Add IP address, Gateway and Mask on Protocol Interface 2")
ixNet.setAttribute(ipv42, '-ip', '20.20.20.2')
ixNet.setAttribute(ipv42, '-maskWidth', '24')
ixNet.setAttribute(ipv42, '-gateway', '20.20.20.1')
ixNet.commit()

################################################################################
# Enable OSPFv2 on ports
################################################################################
# Enable ospf from protocol management
protocol1 = ixNet.getList(vPort1, 'protocols')[0]
ospf1 = ixNet.getList(protocol1, 'ospf')[0]
ixNet.setAttribute(ospf1, '-enabled', 'true')
ixNet.commit()

protocol2 = ixNet.getList(vPort2, 'protocols')[0]
ospf2 = ixNet.getList(protocol2, 'ospf')[0]
ixNet.setAttribute(ospf2, '-enabled', 'true')
ixNet.commit()

################################################################################
# Configure OSPFv2 routers on ports
################################################################################
ixNet.add(ospf1, 'router')
ixNet.commit()
router1 = ixNet.getList(ospf1, 'router')[0]
ixNet.setAttribute(router1, '-enabled', 'true')
ixNet.setAttribute(router1, '-routerId', '1.1.1.1')
ixNet.setAttribute(router1, '-discardLearnedLsa', 'false')
ixNet.commit()

ixNet.add(ospf2, 'router')
ixNet.commit()
router2 = ixNet.getList(ospf2, 'router')[0]
ixNet.setAttribute(router2, '-enabled', 'true')
ixNet.setAttribute(router2, '-routerId', '2.2.2.2')
ixNet.setAttribute(router2, '-discardLearnedLsa', 'false')
ixNet.commit()

################################################################################
# Configure interfaces on OSPFv2 routers 
################################################################################
ixNet.add(router1, 'interface')
ixNet.commit()
router1Interface = ixNet.getList(router1, 'interface')[0]
ixNet.setAttribute(router1Interface, '-connectedToDut', 'true')
ixNet.setAttribute(router1Interface, '-protocolInterface', interface1)
ixNet.setAttribute(router1Interface, '-enabled', 'true')
ixNet.setAttribute(router1Interface, '-networkType', 'pointToPoint')
ixNet.commit()

ixNet.add(router2, 'interface')
ixNet.commit()
router2Interface = ixNet.getList(router2, 'interface')[0]
ixNet.setAttribute(router2Interface, '-connectedToDut', 'true')
ixNet.setAttribute(router2Interface, '-protocolInterface', interface2)
ixNet.setAttribute(router2Interface, '-enabled', 'true')
ixNet.setAttribute(router2Interface, '-networkType', 'pointToPoint')
ixNet.commit()

#######################################################################################
# Configure 10 route range on each OSPFv2 router , enable only the first 5 route ranges
#######################################################################################
for count in range(1, 11):
	temp = str(count)
	index = count - 1
	ixNet.add(router1, 'routeRange')
	ixNet.commit()
	router1routeRange = ixNet.getList(router1, 'routeRange')[index]
	if count < 6 :
		ixNet.setAttribute(router1routeRange, '-enabled', 'true')
		ixNet.setAttribute(router1routeRange, '-origin', 'externalType1')
	# End if
	ixNet.setAttribute(router1routeRange, '-networkNumber', '55.55.55.'+ temp)
	ixNet.commit()
	ixNet.add(router2, 'routeRange')
	ixNet.commit()
	router2routeRange = ixNet.getList(router2, 'routeRange')[index]
	if count < 6 :
		ixNet.setAttribute(router2routeRange, '-enabled', 'true')
		ixNet.setAttribute(router2routeRange, '-origin', 'externalType1')
	# End if
	ixNet.setAttribute(router2routeRange, '-networkNumber', '66.66.66.'+ temp)
	ixNet.commit()

#End for

################################################################################
# 2. Start OSPFv2 protocol and wait for 60 seconds
################################################################################
print("Start OSPFv2 protocol and wait for 60 seconds for protocol to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
print ("Fetch all OSPF Aggregated Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"OSPF Aggregated Statistics"/page'
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # End For
    # End For
# End For
print("***************************************************")

time.sleep(5)
###############################################################################
# 4. Retrieve protocol learned info
###############################################################################
print ("Retrieve protocol learned info")
ixNet.execute('refreshLearnedInfo', router1Interface)
ixNet.execute('refreshLearnedInfo', router2Interface)
waitPeriod = 0
isRefreshedInterface1 = 'false'
isRefreshedInterface2 = 'false'
while (isRefreshedInterface1 != 'true' and isRefreshedInterface2 != 'true') :
	isRefreshedInterface1 = ixNet.getAttribute(router1Interface, '-isLearnedInfoRefreshed')
	isRefreshedInterface2 = ixNet.getAttribute(router2Interface, '-isLearnedInfoRefreshed')
	time.sleep(1)
	waitPeriod += 1
	if waitPeriod > 60 :
		print ("Could not retrieve learnt info on ports")
	#End if
#End While

listLSA1 = ixNet.getList(router1Interface, 'learnedLsa')
listLSA2 = ixNet.getList(router2Interface, 'learnedLsa')
temp = 1

print ("LSA retrieved on port 1")
for item  in listLSA1 :
	count = str(temp)
	print ("LSA :") + count
	print ("***************************************************")

	linkStateID = ixNet.getAttribute(item, '-linkStateId')
	advRouterID = ixNet.getAttribute(item, '-advRouterId')
	lsaType = ixNet.getAttribute(item, '-lsaType')
	seqNumber = ixNet.getAttribute(item, '-seqNumber')
	age = ixNet.getAttribute(item, '-age')

	print ( "linkStateID \t:\t") + linkStateID
	print ( "advRouterID \t:\t") + advRouterID
	print ( "lsaType     \t:\t") + lsaType
	print ( "seqNumber   \t:\t") + seqNumber
	print ( "age         \t:\t") + age
	print ("")
	temp += 1
#End For
temp = 1
print ("LSA retrieved on port 2")
for item  in listLSA2 :
	count = str(temp)
	print ("LSA :") + count
	print ("***************************************************")

	linkStateID = ixNet.getAttribute(item, '-linkStateId')
	advRouterID = ixNet.getAttribute(item, '-advRouterId')
	lsaType = ixNet.getAttribute(item, '-lsaType')
	seqNumber = ixNet.getAttribute(item, '-seqNumber')
	age = ixNet.getAttribute(item, '-age')

	print ( "linkStateID \t:\t") + linkStateID
	print ( "advRouterID \t:\t") + advRouterID
	print ( "lsaType     \t:\t") + lsaType
	print ( "seqNumber   \t:\t") + seqNumber
	print ( "age         \t:\t") + age
	print ("")
	temp += 1
#End For

print ("***************************************************")

################################################################################
# 5. Enable all route ranges on each OSPFv2 router
################################################################################
print ("Enable all available route ranges on each OSPFv2 router")
router1routeRangeList = ixNet.getList(router1, 'routeRange')
router2routeRangeList = ixNet.getList(router2, 'routeRange')
for routeRange  in router1routeRangeList :
   ixNet.setAttribute(routeRange, '-enabled', 'true')
   ixNet.commit()
   #End For
for routeRange  in router2routeRangeList :
   ixNet.setAttribute(routeRange, '-enabled', 'true')
   ixNet.commit()
#End For

##################################################################################
# 6. Disable / Enable interfaces on each OSPFv2 router for new routes to be available
##################################################################################
router1InterfaceList = ixNet.getList(router1, 'interface')
router2InterfaceList = ixNet.getList(router2, 'interface')
for interface in router1InterfaceList :
   ixNet.setAttribute(interface, '-enabled', 'false')
   ixNet.commit()
   ixNet.setAttribute(interface, '-enabled', 'true')
   ixNet.commit()
#End For

for interface in router1InterfaceList :
   ixNet.setAttribute(interface, '-enabled', 'false')
   ixNet.commit()
   ixNet.setAttribute(interface, '-enabled', 'true')
   ixNet.commit()
#End For

#################################################################################
# 7. Retrieve protocol learned info , wait till 60 sec for table to be refreshed
#################################################################################
time.sleep(10)
print ("Retrieve protocol learned info")
ixNet.execute('refreshLearnedInfo', router1Interface)
ixNet.execute('refreshLearnedInfo', router2Interface)
waitPeriod = 0
isRefreshedInterface1 = 'false'
isRefreshedInterface2 = 'false'
while (isRefreshedInterface1 != 'true' and isRefreshedInterface2 != 'true') :
	isRefreshedInterface1 = ixNet.getAttribute(router1Interface, '-isLearnedInfoRefreshed')
	isRefreshedInterface2 = ixNet.getAttribute(router2Interface, '-isLearnedInfoRefreshed')
	time.sleep(1)
	waitPeriod += 1
	if waitPeriod > 60 :
		print ("Could not retrieve learnt info on ports")
	#End if
#End While

listLSA1 = ixNet.getList(router1Interface, 'learnedLsa')
listLSA2 = ixNet.getList(router2Interface, 'learnedLsa')
temp = 1

print ("LSA retrieved on port 1")
for item  in listLSA1 :
	count = str(temp)
	print ("LSA :") + count
	print ("***************************************************")

	linkStateID = ixNet.getAttribute(item, '-linkStateId')
	advRouterID = ixNet.getAttribute(item, '-advRouterId')
	lsaType = ixNet.getAttribute(item, '-lsaType')
	seqNumber = ixNet.getAttribute(item, '-seqNumber')
	age = ixNet.getAttribute(item, '-age')

	print ( "linkStateID \t:\t") + linkStateID
	print ( "advRouterID \t:\t") + advRouterID
	print ( "lsaType     \t:\t") + lsaType
	print ( "seqNumber   \t:\t") + seqNumber
	print ( "age         \t:\t") + age
	print ("")
	temp += 1
#End For
temp = 1
print ("LSA retrieved on port 2")
for item  in listLSA2 :
	count = str(temp)
	print ("LSA :") + count
	print ("***************************************************")

	linkStateID = ixNet.getAttribute(item, '-linkStateId')
	advRouterID = ixNet.getAttribute(item, '-advRouterId')
	lsaType = ixNet.getAttribute(item, '-lsaType')
	seqNumber = ixNet.getAttribute(item, '-seqNumber')
	age = ixNet.getAttribute(item, '-age')

	print ( "linkStateID \t:\t") + linkStateID
	print ( "advRouterID \t:\t") + advRouterID
	print ( "lsaType     \t:\t") + lsaType
	print ( "seqNumber   \t:\t") + seqNumber
	print ( "age         \t:\t") + age
	print ("")
	temp += 1
#End For

print ("***************************************************")

################################################################################
# 8. Configure L2-L3 traffic
################################################################################
print("Congfiguring L2-L3 Traffic Item")
trafficItem1 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem1, '-name', 'Traffic Item OSPF',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv4')
ixNet.commit()

trafficItem1 = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')
source       = [ vPort1 + '/protocols/ospf']
destination  = [ vPort2 + '/protocols/ospf']

ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', [],
    '-scalableSources',       [],
    '-multicastReceivers',    [],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               source,
    '-destinations',          destination)
ixNet.commit()

ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'trackingenabled0'])
ixNet.commit()

###############################################################################
# 9. Apply and start L2/L3 traffic
###############################################################################
print ('applying L2/L3 traffic')
ixNet.execute('apply', ixNet.getRoot() + '/traffic')
time.sleep(5)

print ('starting L2/L3 traffic')
ixNet.execute('start', ixNet.getRoot() + '/traffic')

print ('Let traffic run for 1 minute')
time.sleep(60)

###############################################################################
# 10. Retrieve L2/L3 traffic item statistics
###############################################################################
print ('Verifying all the L2-L3 traffic stats')
viewPage = '::ixNet::OBJ-/statistics/view:"Flow Statistics"/page'
statcap =  ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print ("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # End For
    # End For
# End For
print ("***************************************************")

################################################################################
# 11. Stop L2/L3 traffic
################################################################################
print ('Stopping L2/L3 traffic')
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)

################################################################################
# 12. Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
