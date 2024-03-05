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

#################################################################################
#                                                                               #
# Description:                                                                  #
#    This script intends to demonstrate how to use NGPF CFM Python API.         #
#    About Topology:                                                            #
#      Hub & Spoke topology is configured on 2 Ixia Ports. Each Hub & Spoke     #
#    topology consists of one emulated CFM MP (hub) and 3 simulated CFM MPs     #
#    (spoke).                                                                   #
#    Script Flow:                                                               #
#       Step 1. Configuration of protocols.                                     #
#            i.   Adding CFM emulated MP(emulated device group.)                #
#            ii.  Adding CFM Simulated Topology behind Emulated Device Group.   #
#            iii. Configuring simulated topology type as Hub & Spoke using      #
#                 CFM Network Group Wizard.                                     #
#            iv.  Changing Simulated topology connector to CFM stack.           #
#            v.   Configuring MD level and MA parameters in Simulated topology  #
#                 using CFM Network Group wizard.                               #
#            vi.  Execute configMDLevels command after setting required MD level#
#                 parameters.                                                   #
#        Step 2. Start of protocol                                              #
#        Step 3. Protocol Statistics display                                    #
#        Step 4. Learned Info display   (Continuity Check messages,             #
#                Loopback messages and Link Trace mesages)                      #
#        Step 5. On The Fly(OTF) change of protocol parameter.                  #
#                (OTF Stop CCM in emulated MP and Apply changes on the fly.)    #
#        Step 6. Again statistics display to see OTF changes took place         #
#        Step 7. Configuration L2-L3 Traffic                                    #
#        Step 8. Apply and Start of L2-L3 traffic                               #
#        Step 9. Display of L2-L3  traffic Stats                                #
#        Step 10.Stop of L2-L3 traffic                                          #
#        Step 11.Stop of all protocols                                          #
#                                                                               #
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
#ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\7.40-EA\API\Python'
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\9.00-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.39.50.134'
ixTclPort   = '8039'
ports       = [('10.39.43.154', '3', '9',), ('10.39.43.154', '3', '10',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '9.10',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')
#################################################################################
# Step 1> protocol configuration section
#################################################################################

# assigning ports
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

root    = ixNet.getRoot()
vportTx = ixNet.getList(root, 'vport')[0]
vportRx = ixNet.getList(root, 'vport')[1]
# Creating topology and device group
print("adding topologies")
ixNet.add(root, 'topology', '-vports', vportTx)
ixNet.add(root, 'topology', '-vports', vportRx)
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]
print ('Renaming the topologies and the device groups')
ixNet.setAttribute(topo1, '-name', 'CFM Topology 1')
ixNet.setAttribute(topo2, '-name', 'CFM Topology 2')
print ("Adding 2 device groups")
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

deviceGroup1 = t1devices[0]
deviceGroup2 = t2devices[0]
ixNet.setAttribute(deviceGroup1, '-name', 'Emulated MP 1')
ixNet.setAttribute(deviceGroup2, '-name', 'Emulated MP 2')
ixNet.commit()

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(deviceGroup1, '-multiplier', '1')
ixNet.setAttribute(deviceGroup2, '-multiplier', '1')
ixNet.commit()


#  Adding ethernet stack and configuring MAC
print("Adding ethernet/mac endpoints")
ixNet.add(deviceGroup1, 'ethernet')
ixNet.add(deviceGroup2, 'ethernet')
ixNet.commit()

ethernet1 = ixNet.getList(deviceGroup1, 'ethernet')[0]
ethernet2 = ixNet.getList(deviceGroup2, 'ethernet')[0]

print("Configuring the mac addresses %s" % (ethernet1))
ixNet.setMultiAttribute(ixNet.getAttribute(ethernet1, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '22:22:22:22:22:22',
    '-step',      '00:00:00:00:00:01')

ixNet.setAttribute(ixNet.getAttribute(ethernet2, '-mac') + '/singleValue',
    '-value', '44:44:44:44:44:44')
ixNet.commit()

#  Adding CFM protocol stack and configuring it
print("\n\nAdding CFM emulated MP over Ethernet stack\n")
ixNet.add(ethernet1, 'cfmBridge')
ixNet.add(ethernet2, 'cfmBridge')
ixNet.commit()

cfmBridge1 = ixNet.getList(ethernet1, 'cfmBridge')[0]
cfmBridge2 = ixNet.getList(ethernet2, 'cfmBridge')[0]
cfmMp1 = ixNet.getList(cfmBridge1, 'cfmMp')[0]
cfmMp2 = ixNet.getList(cfmBridge2, 'cfmMp')[0]


# Adding CFM Simulated Topology behind Emulated Device Group
print("\n\nAdding CFM Simulated Topology\n")
addNetworkGroup1 = ixNet.add(deviceGroup1, 'networkGroup')
addNetworkGroup2 = ixNet.add(deviceGroup2, 'networkGroup')
ixNet.commit()

networkGroup1 = ixNet.getList(deviceGroup1, 'networkGroup')[0]
networkGroup2 = ixNet.getList(deviceGroup2, 'networkGroup')[0]
ixNet.setAttribute(networkGroup1, '-name', 'Network Topology 1')
ixNet.setAttribute(networkGroup2, '-name', 'Network Topology 2')
ixNet.commit()

addNetworkTopology1 = ixNet.add(addNetworkGroup1, 'networkTopology')[0]
addNetworkTopology2 = ixNet.add(addNetworkGroup2, 'networkTopology')[0]
ixNet.commit()

networkTopology1 =ixNet.getList(networkGroup1, 'networkTopology')[0]
networkTopology2 =ixNet.getList(networkGroup2, 'networkTopology')[0]


# Configuring simulated topology type as Hub & Spoke using CFM Network Group Wizard
print("\n\nConfiguring simulated topology type as Hub & Spoke using CFM Network Group Wizard\n")
addHubnSpoke1 = ixNet.add(networkTopology1, 'netTopologyHubNSpoke')
ixNet.commit()

addHubnSpoke2 = ixNet.add(networkTopology2, 'netTopologyHubNSpoke')
ixNet.commit()

ixNet.setMultiAttribute(addHubnSpoke1, '-enableLevel2Spokes', 'false', '-includeEntryPoint', 'true')
ixNet.setMultiAttribute(addHubnSpoke2, '-enableLevel2Spokes', 'false', '-includeEntryPoint', 'true')
ixNet.commit()


networkGroup1 = ixNet.getList(deviceGroup1, 'networkGroup')[0]
ixNet.setAttribute(networkGroup1, '-name', "Simulated Topology 1")
networkGroup2 = ixNet.getList(deviceGroup2, 'networkGroup')[0]
ixNet.setAttribute(networkGroup2, '-name', "Simulated Topology 2")

simRouterBridge1 = ixNet.getList(networkTopology1, 'simRouterBridge')[0]
print(simRouterBridge1)
simRouterBridge2 = ixNet.getList(networkTopology2, 'simRouterBridge')[0]
print(simRouterBridge2)

# Changing Simulated topology connector to CFM stack
print("\n\nChanging Simulated topology connector to CFM stack\n")

addconnector1 = ixNet.add(simRouterBridge1, 'connector')
ixNet.setMultiAttribute(addconnector1, '-connectedTo', cfmBridge1)
ixNet.commit()

addconnector2 = ixNet.add(simRouterBridge2,  'connector')
ixNet.setMultiAttribute(addconnector2, '-connectedTo', cfmBridge2)
ixNet.commit()


# Configuring MD level and MA parameters from Simulated topology from CFM Network Group wizard
print("\n\nConfiguring MD level and MA parameters for Simulated topology 1 using CFM Network Group wizard\n")
cfmST1 = ixNet.getList(networkTopology1, 'cfmSimulatedTopology')[0]
configMANames1 = ixNet.getList(cfmST1, 'configMANamesParams')[0]
ixNet.setMultiAttribute(configMANames1, '-maName', "MA-12")
ixNet.commit()
ixNet.execute('configMANames', configMANames1)


configMDLevels1 = ixNet.getList(cfmST1, 'configMDLevelsParams')[0]
ixNet.setMultiAttribute(configMDLevels1, '-numMDLevels', '2', '-mdLevel1', "1",  '-mdNameFormat1', "mdNameFormatDomainNameBasedStr", '-mdName1', "MD-1", '-mdLevel2', "2", '-mdNameFormat2', "mdNameFormatCharacterStr", '-mdName2', "MD-2")
ixNet.commit()
ixNet.execute('configMDLevels', configMDLevels1)


print("\n\nConfiguring MD level and MA parameters for Simulated topology 2 using CFM Network Group wizard\n")
cfmST2 = ixNet.getList(networkTopology2, 'cfmSimulatedTopology')[0]
configMANames2 = ixNet.getList(cfmST2, 'configMANamesParams')[0]
ixNet.setMultiAttribute(configMANames2, '-maName', "MA-12")
ixNet.commit()
ixNet.execute('configMANames', configMANames2)


configMDLevels2 = ixNet.getList(cfmST2, 'configMDLevelsParams')[0]
ixNet.setMultiAttribute(configMDLevels2, '-numMDLevels', '2', '-mdLevel1', "1",  '-mdNameFormat1', "mdNameFormatDomainNameBasedStr", '-mdName1', "MD-1", '-mdLevel2', "2", '-mdNameFormat2', "mdNameFormatCharacterStr", '-mdName2', "MD-2")
ixNet.commit()
ixNet.execute('configMDLevels', configMDLevels2)

print ('************************************************************')

################################################################################
# Step 2> Start of protocol.
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)

################################################################################
# Step 3> Retrieve protocol statistics.
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
# Step 4> Retrieve protocol learned info
# Note: Blank columns in learned information are shown as '{ }' in output
###############################################################################

print("Fetching CCM Learned Info")
ixNet.execute('getCfmCcmLearnedInformation', cfmBridge1, '1')
time.sleep(5)
linfo  = ixNet.getList(cfmBridge1, 'learnedInfo')[0]
columns = ixNet.getAttribute(linfo, '-columns')
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
print(columns)
for v in values :
    print(v)
# end for
print("***************************************************")

print("Fetching Loopback Message Learned Info")
ixNet.execute('getCfmLoopbackDbLearnedInformation', cfmBridge1, '1')
time.sleep(5)
linfo  = ixNet.getList(cfmBridge1, 'learnedInfo')[1]
columns = ixNet.getAttribute(linfo, '-columns')
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
print(columns)
for v in values :
    print(v)
# end for
print("***************************************************")

print("Fetching Link trace Message Learned Info")
ixNet.execute('getCfmLinkTraceDbLearnedInformation', cfmBridge1, '1')
time.sleep(5)
linfo  = ixNet.getList(cfmBridge1, 'learnedInfo')[2]
columns = ixNet.getAttribute(linfo, '-columns')
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
print(columns)
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# Step 5> OTF Stop CCM in emulated MP and Apply changes on the fly.
################################################################################
print("OTF stop  CCM for root(emualated) MP in topology 2 from right-click action ...\n")
ixNet.execute('stopCcmEmulated', cfmMp2)
print("Wait for 10 seconds before checking stats ...\n")
time.sleep(10)

###############################################################################
# Step 6> Retrieve protocol learned info again and compare with.
###############################################################################
ixNet.execute('clearAllLearnedInfo', cfmBridge1)
print("Fetching CFM Learned Info")
ixNet.execute('getCfmCcmLearnedInformation', cfmBridge1, '1')
time.sleep(5)
linfo  = ixNet.getList(cfmBridge1, 'learnedInfo')[0]
columns = ixNet.getAttribute(linfo, '-columns')
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
print(columns)
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# Step 7> Configure L2-L3 traffic
################################################################################
print("Configuring L2-L3 Traffic Item")
trafficItem1 = ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.setMultiAttribute(trafficItem1, '-name', 'Ethernet Traffic 1',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ethernetVlan')
ixNet.commit()

trafficItem1 = ixNet.remapIds(trafficItem1)[0]
endpointSet1 = ixNet.add(trafficItem1, 'endpointSet')
source       = [ethernet1]
destination  = [ethernet2]

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
    '-trackBy',        ['ethernetIiSourceaddress0', 'ethernetIiDestinationaddress0', 'trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         [])
ixNet.commit()

###############################################################################
# Step 8> Apply and start L2/L3 traffic
###############################################################################
print ('applying L2/L3 traffic')
ixNet.execute('apply', ixNet.getRoot() + '/traffic')
time.sleep(5)

print ('starting L2/L3 traffic')
ixNet.execute('start', ixNet.getRoot() + '/traffic')

print ('let traffic run for 60 second')
time.sleep(60)

###############################################################################
# Step 9> Retrieve L2/L3 traffic item statistics.
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

################################################################################
# Step 10> Stop L2/L3 traffic.
################################################################################
print ('Stopping L2/L3 traffic')
ixNet.execute('stop', ixNet.getRoot() + '/traffic')
time.sleep(5)

################################################################################
# Step 11> Stop all protocols.
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
time.sleep(30)
print ('!!! Test Script Ends !!!')
