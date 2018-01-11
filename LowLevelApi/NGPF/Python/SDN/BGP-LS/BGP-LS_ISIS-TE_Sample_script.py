################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            # 
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    22/11/2016 - Chandan Mishra - created sample                                 #
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
##   This script intends to demonstrate how to use NGPF BGPLS &                #
#    ISIS TE SR Low Level Python API.                                            #
#                                                                              #
#    1. It will create 2 BGP and 2 ISIS Topologies and 1 Network Group.        #
#    2. ISIS SR, TE and SR Algorithm is enabled on both Emulated and           #
#       Simulated Routers.                                                     #
#    3. BGP LS is Enabled                                                      #
#    4. Start All Protocols                                                    #
#    5. Check Protocol Stats                                                   #
#    6. Check BGPLS Learned Info	                                        #
#    7. Stop all protocols.                                                    #
#                                                                              #
# Ixia Softwares:                                                              #
#    IxOS      8.20 EA                                                         #
#    IxNetwork 8.20 EA                                                         #
#                                                                              #
#################################################################################

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
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.20.0.194-EB\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.216.108.27'
ixTclPort   = '8092'
ports       = [('10.216.108.99', '11', '5',), ('10.216.108.99', '11', '6',)]

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

# Adding Device Groups
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

# Adding Ipv4 stack 
print("Add ipv4 over Ethernet stack")
ixNet.add(mac1, 'ipv4')
ixNet.add(mac2, 'ipv4')
ixNet.commit()

ip1 = ixNet.getList(mac1, 'ipv4')[0]
ip2 = ixNet.getList(mac2, 'ipv4')[0]

mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvAdd2 = ixNet.getAttribute(ip2, '-address')
mvGw1  = ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = ixNet.getAttribute(ip2, '-gatewayIp')

print("Configuring ipv4 addresses")
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '20.20.20.2')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '20.20.20.2')

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

print("Adding ISIS")
ixNet.add(mac1, 'isisL3')
ixNet.add(mac2, 'isisL3')
ixNet.commit()

isisL3_1 = ixNet.getList(mac1, 'isisL3')[0]
isisL3_2 = ixNet.getList(mac2, 'isisL3')[0]

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'BGP Topology 1')
ixNet.setAttribute(topo2, '-name', 'BGP Topology 2')

ixNet.setAttribute(t1dev1, '-name', 'BGP Topology 1 Router')
ixNet.setAttribute(t2dev1, '-name', 'BGP Topology 2 Router')
ixNet.commit()

deviceGroup1 = ixNet.getList(topo1, 'deviceGroup')[0]
isisL3Router1 = ixNet.getList(deviceGroup1, 'isisL3Router')[0]

deviceGroup2 = ixNet.getList(topo2, 'deviceGroup')[0]
isisL3Router2 = ixNet.getList(deviceGroup2, 'isisL3Router')[0]

print("Enabling Host name in Emulated ISIS Routers")

# Enable host name in ISIS router1
enableHostName1 = ixNet.getAttribute(isisL3Router1, '-enableHostName')
ixNet.setAttribute(enableHostName1 + '/singleValue', '-value', 'True')
ixNet.commit()
time.sleep(5)
configureHostName1 = ixNet.getAttribute(isisL3Router1, '-hostName')
ixNet.setAttribute(configureHostName1 + '/singleValue', '-value', 'isisL3Router1')
ixNet.commit()

# Enable host name in ISIS router2
enableHostName2 = ixNet.getAttribute(isisL3Router2, '-enableHostName')
ixNet.setAttribute(enableHostName2 + '/singleValue', '-value', 'True')
ixNet.commit()
time.sleep(5)
configureHostName2 = ixNet.getAttribute(isisL3Router2, '-hostName')
ixNet.setAttribute(configureHostName2 + '/singleValue', '-value', 'isisL3Router2')
ixNet.commit

# Change Network type
print ("Making the NetworkType to Point to Point in the first ISISrouter in Device Group 1")
networkTypeMultiValue1 = ixNet.getAttribute(isisL3_1, '-networkType')
ixNet.setMultiAttribute(networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(networkTypeMultiValue1 + '/singleValue', '-value', 'pointpoint')

print("Making the NetworkType to Point to Point in the Second ISISrouter in Device Group 2")
networkTypeMultiValue2 = ixNet.getAttribute(isisL3_2, '-networkType')
ixNet.setMultiAttribute(networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(networkTypeMultiValue2 + '/singleValue', '-value', 'pointpoint')

################################################################################
## Traffic Engineering Configuration for ISIS Emulated Routers
#################################################################################
print("Enabling TE on Router1")
enableTE_1 = ixNet.getAttribute(isisL3Router1, '-enableTE')
ixNet.setAttribute(enableTE_1 + '/singleValue', '-value', 'True')
ixNet.commit()

print("Enabling TE on Router2\n")
enableTE_2 = ixNet.getAttribute(isisL3Router2, '-enableTE')
ixNet.setAttribute(enableTE_2 + '/singleValue', '-value', 'True')
ixNet.commit()

print("Enabling Metric Level for Traffic Engineering under ISISL3-IF in DG1")
isisTrafficEngineering1 = ixNet.getList(isisL3_1, 'isisTrafficEngineering')[0]
metricLevel1 = ixNet.getAttribute(isisTrafficEngineering1, '-metricLevel')
ixNet.setAttribute(metricLevel1 + '/singleValue', '-value', '44')
ixNet.commit()

print("Enabling Metric Level for Traffic Engineering under ISISL3-IF in DG2")
isisTrafficEngineering2 = ixNet.getList(isisL3_2, 'isisTrafficEngineering')[0]
metricLevel2 = ixNet.getAttribute(isisTrafficEngineering2, '-metricLevel')
ixNet.setAttribute(metricLevel2 + '/singleValue', '-value', '55')
ixNet.commit()

print("Setting Maximum Bandwidth Value for Traffic Engineering under ISISL3-IF in DG1")
maxBandwidth1 = ixNet.getAttribute(isisTrafficEngineering1, '-maxBandwidth')
ixNet.setAttribute(maxBandwidth1 + '/singleValue', '-value', '126000000')
ixNet.commit()

print("Setting Maximum Bandwidth Value for Traffic Engineering under ISISL3-IF in DG2")
maxBandwidth2 = ixNet.getAttribute(isisTrafficEngineering2, '-maxBandwidth')
ixNet.setAttribute(maxBandwidth2 + '/singleValue', '-value', '127000000')
ixNet.commit()

print("Setting Maximum Reservable Bandwidth Value for Traffic Engineering under ISISL3-IF in DG1")
maxReservableBandwidth1 = ixNet.getAttribute(isisTrafficEngineering1, '-maxReservableBandwidth')
ixNet.setAttribute(maxReservableBandwidth1 + '/singleValue', '-value', '128000000')
ixNet.commit()

print("Setting Maximum Reservable Bandwidth Value for Traffic Engineering under ISISL3-IF in DG2")
maxReservableBandwidth2 = ixNet.getAttribute(isisTrafficEngineering2, '-maxReservableBandwidth')
ixNet.setAttribute(maxReservableBandwidth2 + '/singleValue', '-value', '129000000')
ixNet.commit()

print("Setting Administrator Group Value for Traffic Engineering under ISISL3-IF in DG1\n")
administratorGroup1 = ixNet.getAttribute(isisTrafficEngineering1, '-administratorGroup')
ixNet.setAttribute(administratorGroup1 + '/singleValue', '-value', '22')
ixNet.commit()

print("Setting Administrator Group Value for Traffic Engineering under ISISL3-IF in DG2")
administratorGroup2 = ixNet.getAttribute(isisTrafficEngineering2, '-administratorGroup')
ixNet.setAttribute(administratorGroup2 + '/singleValue', '-value', '33')
ixNet.commit()

################################################################################
## Enabling Segment Routing in Emulated Router
#################################################################################
print("Enabling Segment Routing for ISIS")
ixNet.setAttribute(isisL3Router1, '-enableSR', 'True')
ixNet.commit()

ixNet.setAttribute(isisL3Router2, '-enableSR', 'True')
ixNet.commit()

################################################################################
## Setting SRGB range and SID Count for Emulated Router
#################################################################################
print("Setting SRGB range pool for first Emulated Router")
isisSRGBRangeSubObjectsList1 = ixNet.getList(isisL3Router1, 'isisSRGBRangeSubObjectsList')[0]
startSIDLabel1 = ixNet.getAttribute(isisSRGBRangeSubObjectsList1, '-startSIDLabel')
ixNet.setAttribute(startSIDLabel1 + '/singleValue', '-value', '15000')
ixNet.commit()

print("Setting SID count for first Emulated Router")
sIDCount1 = ixNet.getAttribute(isisSRGBRangeSubObjectsList1, '-sIDCount')
ixNet.setAttribute(sIDCount1 + '/singleValue', '-value', '100')
ixNet.commit()

print("Setting SRGB range pool for second Emulated Router")
isisSRGBRangeSubObjectsList2 = ixNet.getList(isisL3Router2, 'isisSRGBRangeSubObjectsList')[0]
startSIDLabel2 = ixNet.getAttribute(isisSRGBRangeSubObjectsList2, '-startSIDLabel')
ixNet.setAttribute(startSIDLabel2 + '/singleValue', '-value', '10000')
ixNet.commit()

print("Setting SID count for second Emulated Router")
sIDCount2 = ixNet.getAttribute(isisSRGBRangeSubObjectsList2, '-sIDCount')
ixNet.setAttribute(sIDCount2 + '/singleValue', '-value', '100')
ixNet.commit()

print("Enabling Adj-SID in first Emulated Router\n")
enableAdjSID1 = ixNet.getAttribute(isisL3_1, '-enableAdjSID')
ixNet.setAttribute(enableAdjSID1 + '/singleValue', '-value', 'true')
ixNet.commit()

print("Enabling Adj-SID in second Emulated Router")
enableAdjSID2 = ixNet.getAttribute(isisL3_2, '-enableAdjSID')
ixNet.setAttribute(enableAdjSID2 + '/singleValue', '-value', 'true')
ixNet.commit()

print("Setting Adj-SID value in first Emulated Router")
adjSID1 = ixNet.getAttribute(isisL3_1, '-adjSID')
ixNet.setMultiAttribute(adjSID1 + '/counter', '-step', '1','-start', '9001', '-direction', 'increment')
ixNet.commit()

print("Setting Adj-SID value in second Emulated Router")
adjSID2 = ixNet.getAttribute(isisL3_2, '-adjSID')
ixNet.setMultiAttribute(adjSID2 + '/counter', '-step', '1','-start', '9002', '-direction', 'increment')
ixNet.commit()

################################################################################
## Enabling Segment Routing Algorithm in Emulated Router
################################################################################
print("Enabling Segment Routing Algorithm in Emulated Router1")
isisSRAlgorithmList1 = ( ixNet.getList( isisL3Router1, 'isisSRAlgorithmList'))[0]
isisSrAlgorithm1 = ixNet.getAttribute(isisSRAlgorithmList1, '-isisSrAlgorithm')
ixNet.setAttribute( isisSrAlgorithm1 + '/singleValue', '-value', '30')
ixNet.commit()

print("Enabling Segment Routing Algorithm in Emulated Router2")
isisSRAlgorithmList2 = ixNet.getList( isisL3Router2, 'isisSRAlgorithmList')[0]
isisSrAlgorithm2 = ixNet.getAttribute( isisSRAlgorithmList2, '-isisSrAlgorithm')
ixNet.setAttribute(isisSrAlgorithm2 + '/singleValue', '-value', '60')
ixNet.commit()

################################################################################
## Adding BGP and Enabling BGPLS
#################################################################################
print("Adding BGP over IP4 stacks")
ixNet.add(ip1, 'bgpIpv4Peer') 
ixNet.add(ip2, 'bgpIpv4Peer') 
ixNet.commit() 

bgp1 = ixNet.getList(ip1, 'bgpIpv4Peer')[0] 
bgp2 = ixNet.getList(ip2, 'bgpIpv4Peer')[0] 

print("Enabling BGPLS Capability") 
capLS1 = ixNet.getAttribute(bgp1, '-capabilityLinkStateNonVpn') 
capLS2 = ixNet.getAttribute(bgp2, '-capabilityLinkStateNonVpn') 
svCap1 = ixNet.getList(capLS1, 'singleValue')[0] 
svCap2 = ixNet.getList(capLS2, 'singleValue')[0] 
ixNet.setAttribute(svCap1, '-value', 'True') 
ixNet.setAttribute(svCap2, '-value', 'True') 
ixNet.commit() 

print("Enabling BGPLS Filter Link State") 
filterLS1 = ixNet.getAttribute(bgp1, '-filterLinkState') 
filterLS2 = ixNet.getAttribute(bgp2, '-filterLinkState') 
svLS1 = ixNet.getList(filterLS1, 'singleValue')[0] 
svLS2 = ixNet.getList(filterLS2, 'singleValue')[0] 
ixNet.setAttribute(svLS1, '-value', 'True') 
ixNet.setAttribute(svLS2, '-value', 'True') 
ixNet.commit() 

print("Setting IPs in BGP DUT IP tab") 
ixNet.setAttribute(ixNet.getAttribute(bgp1, '-dutIp') + '/singleValue', '-value', '20.20.20.1') 
ixNet.setAttribute(ixNet.getAttribute(bgp2, '-dutIp') + '/singleValue', '-value', '20.20.20.2') 
ixNet.commit() 

print("Adding the NetworkGroup with Routers at back of it") 
ixNet.execute('createDefaultStack', t1dev1, 'networkTopology') 
networkGroup = ixNet.getList(t1dev1, 'networkGroup')[0] 
networkTopology = ixNet.getList(networkGroup, 'networkTopology')[0] 
ixNet.setAttribute(networkGroup,'-name', 'ISIS_Network_Group1') 
ixNet.commit() 

################################################################################
## Enabling Segment Routing in simulated router
#################################################################################
print("Enabling Segment Routing in Simulated Routers on Network Group behind Device Group1")
simRouter = ixNet.getList(networkTopology, 'simRouter')[0]
isisL3PseudoRouter = ixNet.getList(simRouter, 'isisL3PseudoRouter')[0]
ixNet.setAttribute(isisL3PseudoRouter, '-enableSR', 'True')
ixNet.commit()

print("Set Value for SID/Index/Label\n")
sIDIndexLabel = ixNet.getAttribute(isisL3PseudoRouter, '-sIDIndexLabel')
ixNet.setAttribute(sIDIndexLabel + '/singleValue', '-value', '100')
ixNet.commit()

print("Set Value for Start SID/Label-1\n")
isisSRGBRangeSubObjectsList = ixNet.getList(isisL3PseudoRouter, 'isisSRGBRangeSubObjectsList')[0]
sIDIndexLabel = ixNet.getAttribute(isisSRGBRangeSubObjectsList, '-startSIDLabel')
ixNet.setMultiAttribute(sIDIndexLabel + '/counter', '-step', '100','-start', '116000', '-direction', 'increment')
ixNet.commit()

print("Set Value for Start SID Count-1")
sIDCount = ixNet.getAttribute(isisSRGBRangeSubObjectsList, '-sIDCount')
ixNet.setAttribute(sIDCount + '/singleValue', '-value', '9000')
ixNet.commit()

print("Enabling Adj-Sid in Simulated Interface on Network Group behind Device Group2")
simInterface = ixNet.getList(networkTopology, 'simInterface')[0]
isisL3PseudoInterface = ixNet.getList(simInterface, 'isisL3PseudoInterface')[0]
enableAdjSID = ixNet.getAttribute(isisL3PseudoInterface, '-enableAdjSID')
ixNet.setAttribute(enableAdjSID + '/singleValue', '-value', 'True')
ixNet.commit()

print("Set IPv6 Adj-SID value for Simulated Interface")
ipv6SidValue = ixNet.getAttribute(isisL3PseudoInterface, '-ipv6SidValue')
ixNet.setAttribute(ipv6SidValue + '/singleValue', '-value', '8000::1')
ixNet.commit()

################################################################################
## Traffic Engineering Configuration for ISIS Simulated Routers
#################################################################################
print("Enabling TE on Simulated Router")
enableTE = ixNet.getAttribute(isisL3PseudoRouter, '-enable')
ixNet.setAttribute(enableTE + '/singleValue', '-value', 'True')
ixNet.commit()

print("Enabling Metric Level for Traffic Engineering under ISISL3-IF in DG1")
metricLevel = ixNet.getAttribute(isisL3PseudoInterface, '-metricLevel')
ixNet.setAttribute(metricLevel + '/singleValue', '-value', '67')
ixNet.commit()

print("Setting Maximum Bandwidth Value for Traffic Engineering under ISISL3-IF in DG1")
maxBandwidth_Bps = ixNet.getAttribute(isisL3PseudoInterface, '-maxBandwidth_Bps')
ixNet.setAttribute(maxBandwidth_Bps + '/singleValue', '-value', '136000000')
ixNet.commit()

print("Setting Maximum Reservable Bandwidth Value for Traffic Engineering under ISISL3-IF in DG1")
maxReservableBandwidth_Bps = ixNet.getAttribute(isisL3PseudoInterface, '-maxReservableBandwidth_Bps')
ixNet.setAttribute(maxReservableBandwidth_Bps + '/singleValue', '-value', '138000000')
ixNet.commit()

print("Setting Administrator Group Value for Traffic Engineering under ISISL3-IF in DG1")
administratorGroup = ixNet.getAttribute(isisL3PseudoInterface, '-administratorGroup')
ixNet.setAttribute(administratorGroup + '/singleValue', '-value', '77')
ixNet.commit()

################################################################################
# 8. Start ISIS protocol and wait for 60 seconds
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)

################################################################################
# Retrieve protocol statistics.
################################################################################
print("Fetching all Protocol Summary Stats")
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
# print learned info                                                          #
###############################################################################
ixNet.execute('getLinkStateLearnedInfo', bgp2, '1')
time.sleep(5)

print("Print BGP-LS Node/Link, BGP-LS IPv6 Prefix & BGP-LS IPv4 Prefix Learned Info")
linfo  = ixNet.getList(bgp2, 'learnedInfo')[0]
linfoList = ixNet.getList(linfo, 'table')
print("***************************************************")
for table in linfoList :
     tableType = ixNet.getAttribute(table, '-type')
     print(tableType)
     print("=================================================")
     columns = ixNet.getAttribute(table, '-columns')
     print(columns)
     values = ixNet.getAttribute(table, '-values')
     for value in values :
          for word in values :
               print(word)
          #end for
      # end for
# end for 

time.sleep(15)

################################################################################
# Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
