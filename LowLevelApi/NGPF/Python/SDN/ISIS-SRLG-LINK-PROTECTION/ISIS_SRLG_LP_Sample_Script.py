# -*- coding: cp1252 -*-
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
#    This script intends to demonstrate how to use NGPF ISIS Link Protection-  #
#    SRLG - Low Level Python API                                                            #
#                                                                              #
#    1. It will create 2 ISIS topologies, topology1 will have a simulated      #
#       topology Linear behind Device Group1 and Mesh behind Device Group2     #
#    2. Enable Shared Risk Link Group(SRLG) in ISIS Emulated                   #
#       Router in both Device Group.                                           # 
#    3. Give SRLG count 2 with value 5 and 6 for ISIS Emulated router          #
#       Router in both Device Group.                                           #
#    4. Give SRLG count 1 with value 10 for all ISIS simulated routers         #
#       Router behind Device Group1 & with value 15 for all ISIS simulated     #
#       routers Router behind Device Group2 .                                  #
#    5. Enable Link Protection in ISIS Emulated Router in both Device Group    #
#    6. Give Link Protection type Of Extra traffic,Unprotected and Dedicated   # 
#       :true for emulated Router in both device group.                        #
#    7. Give Link Protection type Of Dedicated 1:1 and shared:true for all     #
#       simulated Router behind  both device group.                            #
#    8. Start protocol.                                                        #
#    9. Retrieve protocol statistics.                                          #
#    10. On the fly uncheck "Enable SRLG"  emulated router in Device group2 &  #
#        check  "Enable SRLG" for all simulated Routers behind device group1   #
#    11. On the fly do change on Link type i.e  make enhanced:true and         #
#       unprotected:false for emulated router in Device group1 & disable"Enable# 
#       Link Protection" for first 2 simulated Routers behind device group2    #
#                                                                              #
#    12. Stop all protocols.                                                   #
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
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '100.0.0.1')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '100.0.0.2')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '100.0.0.2')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '100.0.0.1')

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

print("Add ipv6 over Ethernet stack")
ixNet.add(mac1, 'ipv6')
ixNet.add(mac2, 'ipv6')
ixNet.commit()

ip3 = ixNet.getList(mac1, 'ipv6')[0]
ip4 = ixNet.getList(mac2, 'ipv6')[0]

mvAdd1 = ixNet.getAttribute(ip3, '-address')
mvAdd2 = ixNet.getAttribute(ip4, '-address')
mvGw1  = ixNet.getAttribute(ip3, '-gatewayIp')
mvGw2  = ixNet.getAttribute(ip4, '-gatewayIp')

print("Configuring ipv6 addresses")
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '2000:0:0:1:0:0:0:2')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '2000:0:0:1:0:0:0:1')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '2000:0:0:1:0:0:0:1')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '2000:0:0:1:0:0:0:2')

ixNet.setAttribute(ixNet.getAttribute(ip3, '-prefix') + '/singleValue', '-value', '64')
ixNet.setAttribute(ixNet.getAttribute(ip4, '-prefix') + '/singleValue', '-value', '64')

ixNet.setMultiAttribute(ixNet.getAttribute(ip3, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip4, '-resolveGateway') + '/singleValue', '-value', 'true')
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

# Enable host name in ISIS router1
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

# Enable host name in ISIS router2
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
print ("Making the NetworkType to Point to Point in the first ISISrouter in Device Group 1")
networkTypeMultiValue1 = ixNet.getAttribute(isisL3_1, '-networkType')
ixNet.setMultiAttribute(networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(networkTypeMultiValue1 + '/singleValue', '-value', 'pointpoint')

print("Making the NetworkType to Point to Point in the Second ISISrouter in Device Group 2")
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

# Adding Network group behind DeviceGroup
print("Adding NetworkGroup behind DeviceGroup")
networkGoup1 = ixNet.add(t1dev1, 'networkGroup')
ixNet.commit()
networkTopology1 = ixNet.add(networkGoup1,  'networkTopology')
ixNet.commit()
lineartopo = ixNet.add(networkTopology1, 'netTopologyLinear')
ixNet.commit()
ixNet.setAttribute(networkGoup1, '-multiplier', '3')
ixNet.commit()
ixNet.setAttribute(networkGoup1, '-name', 'ISIS_Linear Topology 1')
ixNet.commit()

networkGoup2 = ixNet.add(t2dev1, 'networkGroup')
ixNet.commit()
networkTopology2 = ixNet.add(networkGoup2, 'networkTopology')
ixNet.commit()
lineartopo2 =ixNet.add(networkTopology2, 'netTopologyMesh')
ixNet.commit()
ixNet.setAttribute(networkGoup2, '-multiplier', '1')
ixNet.commit()
ixNet.setAttribute(networkGoup2, '-name', 'ISIS_Mesh Topology 1')
ixNet.commit()

###############################################################################
# 2. Enable SRLG in Both emulated Router 
###############################################################################
print("Enabling SRLG in emulated router in both device group")

#For DG1
enableSrlg1 = ixNet.getAttribute(isisL3_1, '-enableSRLG')
s3 = ixNet.add(enableSrlg1, 'singleValue')
ixNet.setAttribute(s3, '-value', 'True')
ixNet.commit()

#For DG2
enableSrlg2 = ixNet.getAttribute(isisL3_2, '-enableSRLG')
s31 = ixNet.add(enableSrlg2, 'singleValue')
ixNet.setAttribute(s31, '-value', 'True')
ixNet.commit()

##########################################################################################################
# 3. Give SRLG count to 2 and SRLG value to 5 and 6 for ISIS Emulated  Router in both Device Group      
##########################################################################################################       
print("Setting SRLG count to 2 and SRLG Value to 5 and 6 in emulated router in both Device Group ")
ixNet.setAttribute(isisL3_1, '-srlgCount', '2')
ixNet.commit()

#For DG1
srlgValueList1 = ixNet.getList(isisL3_1, 'srlgValueList')[0]
srlgValue = ixNet.getAttribute(srlgValueList1, '-srlgValue')
ixNet.setAttribute(srlgValue + '/singleValue', '-value', '5')

srlgValueList2 = ixNet.getList(isisL3_1, 'srlgValueList')[1]
srlgValue = ixNet.getAttribute(srlgValueList2, '-srlgValue')
ixNet.setAttribute(srlgValue + '/singleValue', '-value', '6')
ixNet.commit()

#For DG2
ixNet.setAttribute (isisL3_2, '-srlgCount', '2')
ixNet.commit()

srlgValueList1 = ixNet.getList(isisL3_2, 'srlgValueList')[0]
srlgValue = ixNet.getAttribute(srlgValueList1, '-srlgValue')
ixNet.setAttribute(srlgValue + '/singleValue', '-value', '5')

srlgValueList2 = ixNet.getList(isisL3_2, 'srlgValueList')[1]
srlgValue = ixNet.getAttribute(srlgValueList2, '-srlgValue')
ixNet.setAttribute(srlgValue + '/singleValue', '-value', '6')
ixNet.commit()

#############################################################################################
# 4.Setting SRLG Value for both Simulated router as described above
#############################################################################################
print("Setting SRLG value to 10 for Simulated routers behind Device Group1")
simInterface = ixNet.getList(networkTopology1, 'simInterface')[0]
isisL3PseudoInterface_Linear = ixNet.getList(simInterface, 'isisL3PseudoInterface')[0]
ixNet.commit()

enableSrlg_Linear = ixNet.getAttribute(isisL3PseudoInterface_Linear, '-enableSRLG')
ixNet.setAttribute(enableSrlg_Linear + '/singleValue', '-value', 'True')
ixNet.commit()

srlgValueList1 = ixNet.getList(isisL3PseudoInterface_Linear, 'srlgValueList')[0]
srlgValue = ixNet.getAttribute(srlgValueList1, '-srlgValue')
ixNet.setAttribute(srlgValue + '/singleValue', '-value', '10')
ixNet.commit()

enableSrlg_Linear = ixNet.getAttribute(isisL3PseudoInterface_Linear, '-enableSRLG')
ixNet.setAttribute(enableSrlg_Linear + '/singleValue', '-value', 'False')
ixNet.commit()

print("Setting SRLG value to 15 for Simulated routers behind Device Group2")
simInterface = ixNet.getList(networkTopology2, 'simInterface')[0]
isisL3PseudoInterface_Mesh = ixNet.getList(simInterface, 'isisL3PseudoInterface')[0]
ixNet.commit()

enableSrlg_Mesh = ixNet.getAttribute(isisL3PseudoInterface_Mesh, '-enableSRLG')
ixNet.setAttribute(enableSrlg_Mesh + '/singleValue', '-value', 'True')
ixNet.commit()

srlgValueList2 = ixNet.getList(isisL3PseudoInterface_Mesh, 'srlgValueList')[0]
srlgValue = ixNet.getAttribute(srlgValueList2, '-srlgValue')
ixNet.setAttribute(srlgValue + '/singleValue', '-value', '15')
ixNet.commit()

#############################################################################################
# 5. Enable Link Protection in Emulated Router in Both Device Group
#############################################################################################
print("Enable Link Protection For Device Group 2 Emulated Router1")

#For DG1
enableLP1  = ixNet.getAttribute(isisL3_1, '-enableLinkProtection')
ixNet.setAttribute(enableLP1 + '/singleValue', '-value', 'True')
ixNet.commit()

print("Enable Link Protection For Device Group 2 Emulated Router1")
enableLP2 = ixNet.getAttribute(isisL3_2, '-enableLinkProtection')
ixNet.setAttribute(enableLP2 + '/singleValue', '-value', 'True')
ixNet.commit()

##############################################################################################
# 6.Setting Link Protection type as Described above For Emulated Router
##############################################################################################
print("Enable Extratraffic ----- unprotected ----- dedicatedoneplusone  For emulated Router1")
extraTraffic = ixNet.getAttribute(isisL3_1, '-extraTraffic')
ixNet.setAttribute(extraTraffic + '/singleValue', '-value', 'True')
ixNet.commit()

unprotected = ixNet.getAttribute(isisL3_1, '-unprotected')
ixNet.setAttribute(unprotected + '/singleValue', '-value', 'True')
ixNet.commit()

dedicatedOnePlusOne = ixNet.getAttribute(isisL3_1,  '-dedicatedOnePlusOne')
ixNet.setAttribute(dedicatedOnePlusOne + '/singleValue', '-value', 'True')
ixNet.commit()

print("Enable Extratraffic ----- unprotected ----- dedicatedoneplusone  For emulated Router2")
extraTraffic = ixNet.getAttribute(isisL3_2, '-extraTraffic')
ixNet.setAttribute(extraTraffic + '/singleValue', '-value', 'True')
ixNet.commit()

unprotected = ixNet.getAttribute(isisL3_2, '-unprotected')
ixNet.setAttribute(unprotected + '/singleValue', '-value', 'True')
ixNet.commit()

dedicatedOnePlusOne = ixNet.getAttribute(isisL3_2,  '-dedicatedOnePlusOne')
ixNet.setAttribute(dedicatedOnePlusOne + '/singleValue', '-value', 'True')
ixNet.commit()

################################################################################
# 7. Setting Link Protection Type For Simulated Router as Described above
################################################################################
print("Enable Link Protection For Simulated Routers Behind Device Group1")
enableLP1 = ixNet.getAttribute(isisL3PseudoInterface_Linear,  '-enableLinkProtection')
ixNet.setAttribute(enableLP1 + '/singleValue', '-value', 'True')
ixNet.commit()

#Make true to DedicatedonePlusOne field
print("Making DedicatedonePlusOne And Shared Link Protection Type to True")
dedicatedOnePlusOne = ixNet.getAttribute(isisL3PseudoInterface_Linear, '-dedicatedOnePlusOne')
ixNet.setAttribute(dedicatedOnePlusOne + '/singleValue', '-value', 'True')
ixNet.commit()

#Make true to Shared field
shared = ixNet.getAttribute(isisL3PseudoInterface_Linear, '-shared')
ixNet.setAttribute(shared + '/singleValue', '-value', 'True')
ixNet.commit()

#Enable some enable link protection on st router
print("Enable Link Protection For Simulated Routers Behind Device Group2")
enableLP2 = ixNet.getAttribute(isisL3PseudoInterface_Mesh,  '-enableLinkProtection')
ixNet.setAttribute(enableLP2 + '/singleValue', '-value', 'True')
ixNet.commit()

#Make true to DedicatedonePlusOne field
print("Making DedicatedonePlusOne And Shared Link Protection Type to True")
dedicatedOnePlusOne = ixNet.getAttribute(isisL3PseudoInterface_Mesh, '-dedicatedOnePlusOne')
ixNet.setAttribute(dedicatedOnePlusOne + '/singleValue', '-value', 'True')
ixNet.commit()

#Make true to Shared field
shared = ixNet.getAttribute(isisL3PseudoInterface_Mesh, '-shared')
ixNet.setAttribute(shared + '/singleValue', '-value', 'True')
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
# 10. OTF on SRLG
################################################################################
print("Disabling SRLG for DG1")
enableSrlg1 = ixNet.getAttribute(isisL3_1, '-enableSRLG')
ixNet.setAttribute(enableSrlg1 + '/singleValue', '-value', 'False')
ixNet.commit()

print("Enabling SRLG for Linear ST behind DG1")
isisL3PseudoInterface_Linear = ixNet.getAttribute(isisL3PseudoInterface_Linear, '-enableSRLG')
ixNet.setAttribute(enableSrlg_Linear + '/singleValue', '-value', 'True')
ixNet.commit()

print("Performing OTF on SRLG")
globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")
# end try/expect
print("Wait for 30 seconds ...")
time.sleep(30)

################################################################################
# OTF on Enable Link Protection
################################################################################
print("Performing OTF on Link Protection\n")
print("Making unprotected field of DG1 False")
unprotected = ixNet.getAttribute(isisL3_1, '-unprotected')
ixNet.setAttribute(unprotected + '/singleValue', '-value', 'False');
ixNet.commit()

print("Making enhanced field of DG1 True")
enhanced = ixNet.getAttribute(isisL3_1, '-enhanced')
ixNet.setAttribute(enhanced + '/singleValue', '-value', 'True')
ixNet.commit()

print("Disabling Link Protection for Mesh ST behind DG2")
enableLP1 = ixNet.getAttribute(isisL3PseudoInterface_Mesh, '-enableLinkProtection')
OverlayLP = ixNet.add(enableLP1, 'overlay')
ixNet.setMultiAttribute(OverlayLP,'-index', '2', '-value', 'False')
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
time.sleep(30)

################################################################################
# Stop all protocols
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
