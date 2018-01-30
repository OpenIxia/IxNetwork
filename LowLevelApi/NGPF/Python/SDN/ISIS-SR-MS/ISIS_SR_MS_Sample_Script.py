# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2016 by IXIA                                           # 
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    24/11/2016 - Anit Ghosal - created sample                                 #
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
#    This script intends to demonstrate how to use NGPF ISIS SR MS Python API. #
#                                                                              #
#    1. It will create 2 ISIS topologies, topology1 will have a simulated      #
#       topology Linear behind Device Group1 and Mesh behind Device Group2.    #
#    2. Enable Segment Routing in ISIS Emulated Router.                        #
#    3. Set SRGB range and SID Count for Emulated Router.                      #
#    4. Set IPV4 and IPV6 Ranges for both router acts as Mapping Server(MS)    #
#         and accordingly IPV4 & IPV6 Node Routes in Simulated Topologies.     #
#    5. Start Protocol And Retrieve protocol statistics.                       #
#    6. Retrieve protocol learned info in Port1.                               #
#    7. Retrieve protocol learned info in Port2.                               #
#    8. On the fly change SID Index value for IPv4 MS Ranges in Device Group1. #
#    9. On the fly Change IPV6 prefix in MS range and accordingly IPV6 address #
#        count of Node Routes in  Mesh Simulated Topology behind Device Group2.#  
#    10.On the fly Change in IPV6 FEC prefix in MS  and accordingly IPV6       #
#       address of Node Routes in Mesh Simulated Topology behind Device Group2.#
#    11. Retrieve protocol learned info in both ports after On the Fly changes.#
#    12. Configuring ISIS L2-L3 IPv4 & IPv6 Traffic Item for MS prefix ranges. #
#    13. Verifying all the L2-L3 traffic stats                                 #
#    14. Stop L2-L3 traffic.                                                   #
#    15. Stop all protocols.                                                   #
#                                                                              #
# Ixia Softwares:                                                              #
#    IxOS      8.20 EA                                                         #
#    IxNetwork 8.20 EA                                                         #
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
ixTclServer = '10.216.104.58'
ixTclPort   = '8245'
ports       = [('10.216.108.99', '11', '1',), ('10.216.108.99', '11', '2',)]

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
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '100.0.0.1')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '100.0.0.2')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '100.0.0.2')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '100.0.0.1')

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')

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

# Change Network type
print ("Making the NetworkType to Point to Point in the first ISIS router in Device Group 1")
networkTypeMultiValue1 = ixNet.getAttribute(isisL3_1, '-networkType')
ixNet.setMultiAttribute(networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(networkTypeMultiValue1 + '/singleValue', '-value', 'pointpoint')

print("Making the NetworkType to Point to Point in the Second ISIS router in Device Group 2")
networkTypeMultiValue2 = ixNet.getAttribute(isisL3_2, '-networkType')
ixNet.setMultiAttribute(networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(networkTypeMultiValue2 + '/singleValue', '-value', 'pointpoint')

# Disable Discard Learned LSP
print("Disabling the Discard Learned Info CheckBox")
isisL3RouterDiscardLearnedLSP1 = ixNet.getAttribute(ixNet.getList(t1dev1, 'isisL3Router')[0], '-discardLSPs')
isisL3RouterDiscardLearnedLSP2 = ixNet.getAttribute(ixNet.getList(t2dev1, 'isisL3Router')[0], '-discardLSPs')

ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP1 + '/singleValue', '-value', 'False')

ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP2, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(isisL3RouterDiscardLearnedLSP2 + '/singleValue', '-value', 'False')

print ('ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/isisL3\')')
print (ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/isisL3'))

# Adding Network group behind DeviceGroup
print("Adding NetworkGroup behind DeviceGroup")
networkGoup1 = ixNet.add(t1dev1, 'networkGroup')
ixNet.commit()
networkTopology1 = ixNet.add(networkGoup1,  'networkTopology')
ixNet.commit()
lineartopo = ixNet.add(networkTopology1, 'netTopologyLinear')
ixNet.commit()
networkGoup2 = ixNet.add(t2dev1, 'networkGroup')
ixNet.commit()
networkTopology2 = ixNet.add(networkGoup2, 'networkTopology')
ixNet.commit()
lineartopo2 =ixNet.add(networkTopology2, 'netTopologyMesh')
ixNet.commit()
ixNet.setAttribute(networkGoup1, '-multiplier', '3')
ixNet.commit()
ixNet.setAttribute(networkGoup2, '-multiplier', '1')
ixNet.commit()
ixNet.setAttribute(networkGoup1, '-name', 'ISIS_Linear Topology 1')
ixNet.commit()
ixNet.setAttribute(networkGoup2, '-name', 'ISIS_Mesh Topology 2')
ixNet.commit()
########################################################################################
# 2.Enabling Segment Routing in Emulated Router on Device Group 1 and Device Group 2 
########################################################################################
print ( "Enabling Segment Routing for ISIS")
ixNet.setAttribute(isisL3Router1, '-enableSR', 'true')
ixNet.setAttribute(isisL3Router2, '-enableSR', 'true')
ixNet.commit()
################################################################################
# 3.Setting SRGB range and SID Count for Emulated Router
################################################################################
print ("Setting SRGB range and SID Count for Emulated Router\n")

print ("Setting SRGB range pool for first emulated router\n")
isisSRGBRangeSubObjectsList1 = (ixNet.getList(isisL3Router1, 'isisSRGBRangeSubObjectsList'))[0]
startSIDLabel1 = ixNet.getAttribute(isisSRGBRangeSubObjectsList1, '-startSIDLabel')
svsrgb1 = (ixNet.getList(startSIDLabel1, 'singleValue'))[0]
ixNet.setAttribute(svsrgb1, '-value', '15000')
ixNet.commit()

sidCount1 = ixNet.getAttribute(isisSRGBRangeSubObjectsList1, '-sIDCount')
sidcountsv1 = (ixNet.getList(sidCount1, 'singleValue'))[0]
ixNet.setAttribute(sidcountsv1, '-value', '100')
ixNet.commit()

print ("Setting SRGB range pool for  Emulated Router Device Group2\n")
isisSRGBRangeSubObjectsList2 = (ixNet.getList(isisL3Router2, 'isisSRGBRangeSubObjectsList'))[0]

startSIDLabel2 = ixNet.getAttribute(isisSRGBRangeSubObjectsList2, '-startSIDLabel')
svsrgb2 = (ixNet.getList(startSIDLabel2, 'singleValue'))[0]
ixNet.setAttribute(svsrgb2, '-value', '10000')
ixNet.commit()

sidCount2 = ixNet.getAttribute(isisSRGBRangeSubObjectsList2, '-sIDCount')
sidcountsv2 = (ixNet.getList(sidCount2, 'singleValue'))[0]
ixNet.setAttribute(sidcountsv2, '-value', '100')
ixNet.commit()
###########################################################################################################################################
# 4. Set IPV4 and IPV6 Ranges for both router acts as Mapping Server(MS)and accordingly IPV4 & IPV6 Node Routes in Simulated Topologies    
###########################################################################################################################################         
print ("Enabling IPV4  and IPV6 Node Routes Simulated Routers on Linear Network Group behind Device Group1\n")

networkTopo1 = (ixNet.getList(networkGoup1, 'networkTopology'))[0]
simRouter1 = (ixNet.getList(networkTopo1, 'simRouter'))[0]
ixNet.commit()
isisPseudoRouter1 = (ixNet.getList(simRouter1, 'isisL3PseudoRouter'))[0]
ipv4noderoutes = (ixNet.getList(isisPseudoRouter1, 'IPv4PseudoNodeRoutes'))[0]
active = ixNet.getAttribute( ipv4noderoutes, '-active');
activesin = ixNet.add(active, 'singleValue')
ixNet.setAttribute(activesin, '-value', 'True')
ixNet.commit()

ipv6noderoutes = (ixNet.getList(isisPseudoRouter1, 'IPv6PseudoNodeRoutes'))[0]
active1 = ixNet.getAttribute(ipv6noderoutes, '-active')
activesin1 = ixNet.add(active1, 'singleValue')
ixNet.setAttribute(activesin1, '-value', 'True')
ixNet.commit()
print ( "Changing Prefix Length to 24\n")
prefixlen = ixNet.getAttribute(ipv4noderoutes, '-prefixLength')
prefix = ixNet.add(prefixlen, 'singleValue')
ixNet.setAttribute(prefix, '-value', '24')
ixNet.commit()

print("Enabling IPV4  and IPV6 Node Routes Simulated Routers on Mesh Network Group behind Device Group2\n")
networkTopo2 = (ixNet.getList(networkGoup2, 'networkTopology'))[0]
simRouter2 = (ixNet.getList(networkTopo2, 'simRouter'))[0]
ixNet.commit()
isisPseudoRouter2 = (ixNet.getList(simRouter2, 'isisL3PseudoRouter'))[0]
ipv4noderoutes2 = (ixNet.getList(isisPseudoRouter2, 'IPv4PseudoNodeRoutes'))[0]
active2 = ixNet.getAttribute( ipv4noderoutes2, '-active')
activesin2 = ixNet.add(active2 , 'singleValue')
ixNet.setAttribute(activesin2,' -value', 'True')
ixNet.commit()

ipv6noderoutes2 = (ixNet.getList(isisPseudoRouter2, 'IPv6PseudoNodeRoutes'))[0]
active2 = ixNet.getAttribute(ipv4noderoutes2, '-active')
activesin2 = ixNet.add(active2 , 'singleValue')
ixNet.setAttribute(activesin2,' -value', 'True')
ixNet.commit()
print ( "Changing Prefix Length to 24\n")

prefixlen2 = ixNet.getAttribute(ipv4noderoutes2, '-prefixLength')
prefix2 = ixNet.add(prefixlen2, 'singleValue')
ixNet.setAttribute(prefix2, '-value', '24')
ixNet.commit()

print( "Enabling Mapping Server on  Emulated Router in Device Group 1  and Setting No. of IPV4 and IPV6 Mapping Ranges\n")
enablems1 = ixNet.getAttribute(isisL3Router1_1, '-enableMappingServer')
single = ixNet.add(enablems1, 'singleValue')
ixNet.setMultiAttribute(single, '-value', 'true')
ixNet.commit()

ixNet.setMultiAttribute(isisL3Router1_1,
            '-enableSR', 'true',
            '-numberOfMappingIPV4Ranges', '3',
            '-numberOfMappingIPV6Ranges', '3',)
ixNet.commit()

print( "Enabling Mapping Server on  Emulated Router in Device Group 1  and Setting No. of IPV4 and IPV6 Mapping Ranges\n")
enablems1 = ixNet.getAttribute(isisL3Router2_1, '-enableMappingServer')
single = ixNet.add(enablems1, 'singleValue')
ixNet.setMultiAttribute(single, '-value', 'true')
ixNet.commit()

ixNet.setMultiAttribute(isisL3Router2_1,
            '-enableSR', 'true',
            '-numberOfMappingIPV4Ranges', '3',
            '-numberOfMappingIPV6Ranges', '3',)
ixNet.commit()

print( "Setting Mapping Server IPV4 FEC Prefix ranges For Emulated Router1 in Device Group1\n" )
isisvmsppingserverv4 = (ixNet.getList(isisL3Router1, 'isisMappingServerIPV4List'))[0]
fecprefix = ixNet.getAttribute(isisvmsppingserverv4, '-fECPrefix')
ixNet.commit()
counter = ixNet.add(fecprefix, 'counter')
ixNet.setMultiAttribute(counter,
            '-step', '0.1.0.0',
            '-start', '201.1.0.0',
            '-direction', 'increment')
ixNet.commit()

print( "Setting Mapping Server IPV6 FEC Prefix ranges For Emulated Router1 in Device Group1\n" )
isisvmsppingserverv6 = (ixNet.getList(isisL3Router1, 'isisMappingServerIPV6List'))[0]
fecprefix = ixNet.getAttribute(isisvmsppingserverv6, '-fECPrefix')
ixNet.commit()
counter = ixNet.add(fecprefix, 'counter')
ixNet.setMultiAttribute(counter,
            '-step', '0:0:0:1:0:0:0:0',
            '-start', '3000:0:1:1:0:0:0:0',
            '-direction', 'increment')
ixNet.commit()

print( "Setting Mapping Server IPV4 FEC Prefix ranges For Emulated Router1 in Device Group2\n" )
isisvmsppingserverv4 = (ixNet.getList(isisL3Router2, 'isisMappingServerIPV4List'))[0]
fecprefix = ixNet.getAttribute(isisvmsppingserverv4, '-fECPrefix')
ixNet.commit()
counter = ixNet.add(fecprefix, 'counter')
ixNet.setMultiAttribute(counter,
            '-step', '0.1.0.0',
            '-start', '202.1.0.0',
            '-direction', 'increment')
ixNet.commit()

print( "Setting Mapping Server IPV6 FEC Prefix ranges For Emulated Router1 in Device Group2\n" )
isisvmsppingserverv6 = (ixNet.getList(isisL3Router2, 'isisMappingServerIPV6List'))[0]
fecprefix = ixNet.getAttribute(isisvmsppingserverv6, '-fECPrefix')
ixNet.commit()
counter = ixNet.add(fecprefix, 'counter')
ixNet.setMultiAttribute(counter,
            '-step', '0:0:0:1:0:0:0:0',
            '-start', '3000:1:1:1:0:0:0:0',
            '-direction', 'increment')
ixNet.commit()
################################################################################
# 5. Start ISIS protocol and wait for 60 seconds And  Retrieve protocol statistics.
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)


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
#6. Retrieve protocol learned info in Port 1
################################################################################
print("Fetching ISISL3 IPV4 Prefix Learned Info")
ixNet.execute('getLearnedInfo', isisL3_1, '1')
time.sleep(5)
linfo  = ixNet.getList(isisL3_1, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

print("Fetching ISISL3 IPV6 Prefix Learned Info")
ixNet.execute('getLearnedInfo', isisL3_1, '1')
time.sleep(5)
linfo = (ixNet.getList(isisL3_1, 'learnedInfo'))[0]
ipv6table = (ixNet.getList(linfo, 'table'))[1]
values   = ixNet.getAttribute(ipv6table, '-values')
v        = ''
	 
print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")
################################################################################
#7. Retrieve protocol learned info in Port 2
################################################################################
print("Fetching ISISL3 IPV4 Prefix Learned Info")
ixNet.execute('getLearnedInfo', isisL3_2, '1')
time.sleep(5)
linfo  = ixNet.getList(isisL3_2, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

print("Fetching ISISL3 IPV6 Prefix Learned Info")
ixNet.execute('getLearnedInfo', isisL3_2, '1')
time.sleep(5)
linfo = (ixNet.getList(isisL3_2, 'learnedInfo'))[0]
ipv6table = (ixNet.getList(linfo, 'table'))[1]
values   = ixNet.getAttribute(ipv6table, '-values')
v        = ''
	 
print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")
###############################################################################
# 8. OTF on SID value
###############################################################################
print("OTF on Device Group1  in Topology1 IPV4 MS SID value ")
isisvmsppingserverv4 = (ixNet.getList(isisL3Router1, 'isisMappingServerIPV4List'))[0]
newsid11 = ixNet.getAttribute(isisvmsppingserverv4, '-startSIDLabel')
overlay61 = ixNet.add(newsid11, 'overlay')
ixNet.setMultiAttribute(overlay61, '-index', '1', '-value', '10')
ixNet.commit()
#######################################################################################################
# 9. OTF on  Address  Of Mapping Server  IPV6 and Simulated Topology  And Apply Changes
######################################################################################################
print("OTF on Device Group 2 Topology 1 Address Field\n")
isisvmsppingserverv6 = (ixNet.getList(isisL3Router2, 'isisMappingServerIPV6List'))[0]
fecprefix = ixNet.getAttribute(isisvmsppingserverv6, '-fECPrefix')
overlay10 = ixNet.add(fecprefix, 'overlay')
ixNet.setMultiAttribute(overlay10, '-count', '1', '-index', '2', '-value', '3000:4:1:2:0:0:0:0')
ixNet.commit()
v6noderoutes = ixNet.getAttribute(ipv6noderoutes2, '-networkAddress')
overlay = ixNet.add(v6noderoutes, 'overlay')
ixNet.setMultiAttribute(overlay, '-count', '1', '-index', '2', '-value', '3000:4:1:2:0:0:0:0')
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
#######################################################################################################
# 10. OTF on Range  Of  Mapping Server  IPV6 and Simulated Topology  also And Apply Changes
######################################################################################################
print("OTF on Device Group2 Topology2 IPV6 MS range and  also in ST \n")
range = ixNet.getAttribute(ipv6noderoutes2, '-rangeSize')
overlay1 = ixNet.add(range, 'overlay')
ixNet.setMultiAttribute(overlay1, '-count', '1', '-index', '1', '-value', '4')
ixNet.commit()
range1 = ixNet.getAttribute(isisvmsppingserverv6, '-range')
overlay11 = ixNet.add(range1, 'overlay')
ixNet.setMultiAttribute(overlay11, '-count', '1', '-index', '1', '-value', '4')
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
# 11 . Retrieve protocol learned info in Both Port 
###############################################################################
print("Fetching ISISL3 IPV4 Prefix Learned Info")
ixNet.execute('getLearnedInfo', isisL3_1, '1')
time.sleep(5)
linfo  = ixNet.getList(isisL3_1, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

print("Fetching ISISL3 IPV6 Prefix Learned Info")
ixNet.execute('getLearnedInfo', isisL3_1, '1')
time.sleep(5)
linfo = (ixNet.getList(isisL3_1, 'learnedInfo'))[0]
ipv6table = (ixNet.getList(linfo, 'table'))[1]
values   = ixNet.getAttribute(ipv6table, '-values')
v        = ''
	 
print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

print("Fetching ISISL3 IPV4 Prefix Learned Info")
ixNet.execute('getLearnedInfo', isisL3_2, '1')
time.sleep(5)
linfo  = ixNet.getList(isisL3_2, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

print("Fetching ISISL3 IPV6 Prefix Learned Info")
ixNet.execute('getLearnedInfo', isisL3_2, '1')
time.sleep(5)
linfo = (ixNet.getList(isisL3_2, 'learnedInfo'))[0]
ipv6table = (ixNet.getList(linfo, 'table'))[1]
values   = ixNet.getAttribute(ipv6table, '-values')
v        = ''
	 
print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")
################################################################################
# 12. Configure L2-L3 traffic 
################################################################################
#Configuring L2-L3 IPv4 Traffic Item
print("Configuring L2-L3 IPV4 Traffic Item")
trafficItem1 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem1, '-name', 'IPv4_MPLS_Traffic_Item_1',
    '-roundRobinPacketOrdering', 'false',
	'-trafficType', 'ipv4',
	'-biDirectional', 'true',
    '-useControlPlaneRate', 'true',
    '-useControlPlaneFrameSize', 'true',
    '-mergeDestinations', 'false',
    '-roundRobinPacketOrdering', 'false', 
    '-numVlansForMulticastReplication', '1')
ixNet.commit()

trafficItem1 = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')
source       = [networkGoup1 + '/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv4PseudoNodeRoutes:1']
destination  = [networkGoup2 + '/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv4PseudoNodeRoutes:1']

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
print("hii")
ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy', ['sourceDestValuePair0', 'trackingenabled0', 'mplsMplsLabelValue0', 'ipv4DestIp0', 'ipv4SourceIp0'],
    '-fieldWidth', 'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values', [])
ixNet.commit()

#Configuring L2-L3 IPv6 Traffic Item
print ("Configuring L2-L3 IPv6 Traffic Item\n")
trafficItem2 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem2, '-name', 'IPv6_MPLS_Traffic_Item_1',
    '-roundRobinPacketOrdering', 'false',
	 '-biDirectional', 'true',
    '-useControlPlaneRate', 'true',
    '-useControlPlaneFrameSize', 'true',
    '-mergeDestinations', 'false',
    '-roundRobinPacketOrdering', 'false', 
    '-numVlansForMulticastReplication', '1',
    '-trafficType', 'ipv6')
ixNet.commit()

trafficItem2    = ixNet.remapIds(trafficItem2)[0]
endpointSet1 = ixNet.add(trafficItem2, 'endpointSet')
source       = [networkGoup1 + '/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1']
destination  = [networkGoup2 + '/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1']

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

ixNet.setMultiAttribute(trafficItem2 + '/tracking',
    '-trackBy',        ['sourceDestValuePair0', 'trackingenabled0', 'mplsMplsLabelValue0', 'ipv6DestIp0', 'ipv6SourceIp0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',          [])
ixNet.commit()
###############################################################################
#13 Apply and start L2/L3 traffic and Retrieve L2/L3 traffic item statistics  
###############################################################################
print ('Applying L2/L3 traffic')
ixNet.execute('apply', ixNet.getRoot() + '/traffic')
time.sleep(5)
print ('Starting L2/L3 traffic')
ixNet.execute('start', ixNet.getRoot() + '/traffic')
# Retrieve L2/L3 traffic item statistics
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
#14 Stop L2/L3 traffic
################################################################################
print ('Stopping L2/L3 traffic')
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)

################################################################################
#15 Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')