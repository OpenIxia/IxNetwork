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
# Description :                                                                #
#   1. This scripts shows how we should configure Netconf Client & Netconf        #
#      Server. Different capoabilities configuration.                           #
#   2. Assign ports.                                                           #
#   3. Start all protocols.                                                    #
#   4. Send Command Snippet of Netconf executing Right Click Action                  #
#   5. Retrieve Netconf Client Sessions Per Port statistics.                   #
#   6. Retrieve Netconf Server Per port statistics.                            #
#   7. Stop all protocols.                                                     #
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
# Either feed the ixNetwork library path in the sys.path as below, or put the  #
# IxNetwork.py file somewhere else where we python can autoload it             #
# "IxNetwork.py" is available in <IxNetwork_installer_path>\API\Python         #
################################################################################
IX_NETWORK_LIBRARY_PATH = 'C:/Program Files (x86)/Ixia/IxNetwork/8.30-EA/API/Python'
sys.path.append(IX_NETWORK_LIBRARY_PATH)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information   #
# below                                                                         #
#################################################################################
ixTclServer = '10.39.50.102'
ixTclPort   = '8785'
ports       = [('10.39.50.227', '1', '5'), ('10.39.50.227', '1', '6')]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.50',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

# assigning ports
assignPorts(ixNet, ports[0], ports[1])
time.sleep(5)

root    = ixNet.getRoot()
vportTx = ixNet.getList(root, 'vport')[0]
vportRx = ixNet.getList(root, 'vport')[1]

################################################################################
# 1. Configure the PCC and PCE as per the description given above.             #
################################################################################
print("adding topologies")
ixNet.add(root, 'topology', '-vports', vportTx)
ixNet.add(root, 'topology', '-vports', vportRx)
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

print("Adding 2 device groups")
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
ixNet.setAttribute(ixNet.getAttribute(mac1, '-mac') + '/singleValue',
    '-value', '18:03:73:C7:6C:B1')
ixNet.commit()

ixNet.setAttribute(ixNet.getAttribute(mac2, '-mac') + '/singleValue',
    '-value', '18:03:73:C7:6C:01')
ixNet.commit()

print('ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet\')')
#print(ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet'))

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
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '20.20.20.2')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '20.20.20.2')

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

print("Adding a Netconf Server object on the Topology 2")
netconfServer = ixNet.add(ip1, 'netconfServer')
ixNet.commit()
netconfServer = ixNet.remapIds(netconfServer)[0]

# Adding Netconf Client with expectedPceInitiatedLspPerPcc 1
print("Adding a Netconf Client object on the Topology 2")
netconfClient  = ixNet.add(ip2, 'netconfClient')
ixNet.commit()
netconfClient = ixNet.remapIds(netconfClient)[0]

#print(ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/netconfServer'))
# Set Netconf Server  "clientIpv4Address" field  to 20.20.20.1
print("Set Netconf Server  clientIpv4Address field  to 20.20.20.1")
clientIpv4AddressMv = ixNet.getAttribute(netconfServer, '-clientIpv4Address')
clientIpv4AddressMv = ixNet.remapIds(clientIpv4AddressMv)[0]
ixNet.setAttribute(clientIpv4AddressMv + '/singleValue', '-value',  '20.20.20.1')
ixNet.commit()
#print(ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/netconfClient'))
# Set Netconf Client  "serverIpv4Adress" field  to 20.20.20.2
print("Set Netconf Client  serverIpv4Adress field  to 20.20.20.2")
serverIpMv = ixNet.getAttribute(netconfClient, '-serverIpv4Address')
serverIpMv = ixNet.remapIds(serverIpMv)[0]
ixNet.commit()
ixNet.setMultiAttribute(serverIpMv, '-clearOverlays', 'false', '-pattern', 'singleValue')
ixNet.commit()
ixNet.setAttribute(serverIpMv + '/singleValue', '-value',  '20.20.20.2')
ixNet.commit()

#Adding Netconf Client 2 Command Snippet Data
print("Adding Netconf Client 2 Command Snippet Data")
commandSnippetsData1 = ixNet.getList(netconfClient, 'commandSnippetsData')
commandSnippetsData1 = ixNet.remapIds(commandSnippetsData1)[0]
ixNet.commit()

#Setting Command Snippet Directory
print("Setting Command Snippet Directory \n")
commandSnippetDirectory1 = ixNet.getAttribute(commandSnippetsData1, '-commandSnippetDirectory')
commandSnippetDirectory1 = ixNet.remapIds(commandSnippetDirectory1)[0]
ixNet.commit()

ixNet.setAttribute(commandSnippetDirectory1 + '/singleValue', '-value',  "C:\\Program Files (x86)\\Ixia\\IxNetwork\\8.50-EA\\SampleScripts\\IxNetwork\\NGPF\\Tcl\\SDN\\Netconf")
ixNet.commit()

#Setting Command Snippet File Name
print("Setting Command Snippet File Name \n")
commandSnippetFile1 = ixNet.getAttribute(commandSnippetsData1, '-commandSnippetFile')
commandSnippetFile1 = ixNet.remapIds(commandSnippetFile1)[0]

ixNet.setMultiAttribute(commandSnippetFile1+ '/singleValue', '-value', 'Get-config.xml')
ixNet.commit()

#Setting Command Snippet Active
print("Setting Command Snippet Active \n")
commandSnippetDataActive1 = ixNet.getAttribute(commandSnippetsData1, '-active')
ixNet.commit()
commandSnippetDataActive1 = ixNet.remapIds(commandSnippetDataActive1)[0]
ixNet.commit()
ixNet.setAttribute(commandSnippetDataActive1 + '/singleValue', '-value', 'true')
ixNet.commit()

#Setting Command Snippet Transmission Behaviour
print("Setting Command Snippet Transmission Behaviour \n")
transmissionBehaviour1 = ixNet.getAttribute(commandSnippetsData1, '-transmissionBehaviour')
transmissionBehaviour1 = ixNet.remapIds(transmissionBehaviour1)[0]
transmissionBehaviourOv = ixNet.add(transmissionBehaviour1, 'overlay')
transmissionBehaviourOv = ixNet.remapIds(transmissionBehaviourOv)[0]

ixNet.setMultiAttribute(transmissionBehaviourOv, '-count', '1', '-index', '1', '-value', 'once')
ixNet.commit()
ixNet.setMultiAttribute(transmissionBehaviourOv, '-count', '1', '-index', '2', '-value', 'periodiccontinuous')
ixNet.commit()
################################################################################
# 2. Start PCEP protocol and wait for 45 seconds                               #
################################################################################
print("Starting protocols and waiting for 45 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(45)

################################################################################
# 3. Retrieve protocol statistics                                              #
################################################################################
print("Fetching all Protocol Summary Stats\n")
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
# 4. Sending Command Snippet by executing Right Click Action                    #
################################################################################
print("Sending Command Snippet by executing Right Click Action")
indices = [1, 2]
ixNet.execute('executeCommand', commandSnippetsData1, indices)
time.sleep(15)

################################################################################
# 4. Retrieve protocol statistics. (Netconf Client Per Port)                   #
################################################################################
print("Fetching all Netconf Client Per Port Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"Netconf Client Per Port"/page'
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
# 5. Retrieve protocol statistics. (Netconf Server Per Port)                   #
################################################################################
print("Fetching all Netconf Server Per Port Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"Netconf Server Per Port"/page'
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
# 6. Stop all protocols                                                        #
################################################################################
print('Stopping protocols')
ixNet.execute('stopAllProtocols')
print('!!! Test Script Ends !!!')

