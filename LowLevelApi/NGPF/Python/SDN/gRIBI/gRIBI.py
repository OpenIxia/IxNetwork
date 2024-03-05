# -*- coding: cp1252 -*-
################################################################################
#                                                                              #
#    Copyright 1997 - 2021 by IXIA  Keysight                                   #
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
#    This script intends to demonstrate how to use NGPF gRIBI API to configure  #
#    gRIBI client topology.                                                     #
#                                                                               #
#    About Topology:                                                            #
#       Within topology gRIBI Client is configured in one port. Other port will #
#    be connected to gRIBI server. gRIBI Client is emulated in the Device Group #
#    which consists of 1 gRPC channel, 1 gRIBI clinet, 2 Next-Hop Group and 3   #
#    next hops per next hop group.                                              #
#      The Network Group consists of gRIBI IPv4 entries which will be advertised#
#    by gRIBI client.                                                           #
#                                                                               #
# Script Flow:                                                                  #
#    Configuration flow of the script is as follows:                            #
#    Step 1. Configuration of protocols.                                        #
#         i.   Adding of gRIBI client topology.                                 #
#         ii.  Adding of Network Topology.                                      #
#         iii. Configuring some default paramaters.                             #
#         iv.  Add IPv4 topology in other port. gRIBI Server will run behind    #
#                this port.                                                     #
#         Note: IxNetwork 9.20 EA does not support gRIBI server yet. User can   #
#             connect a real server connected to emualted gRIBI cliente.        #
#             We are running a demo server in the gRIBI server port using some  #
#             cli commands. For example purpose the command to run demo server  #
#             is provided in sample script, but it will not run the commands.   #
#             so gRIBI client sessions will not be up unless we connect it to   # 
#             real server  session  with matching IP and port number.           #
#                                                                               #
#               The script flow shows how to configure gRIBI client topology in #
#             and related parameters in IxNetwork using low level Python API.   #
#                                                                               #
#        Step 2. Start of protocol                                              #
#        Step 3. Protocol Statistics display                                    #
#        Step 4. On The Fly(OTF) change of protocol parameter.                  #
#        Step 5. Again Statistics display to see OTF changes took place         #
#        Step 6.Stop of all protocols                                           #
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
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\9.20-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.66.47.72'
ixTclPort   = '8961'
ports       = [('10.39.50.126', '1', '1',), ('10.39.50.126', '1', '2',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '9.20',
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
ixNet.setAttribute(topo1, '-name', 'gRIBI Client Topology')
ixNet.setAttribute(topo2, '-name', 'gRIBI Server Topology')

print ("Adding 2 device groups")
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

deviceGroup1 = t1devices[0]
deviceGroup2 = t2devices[0]
ixNet.setAttribute(deviceGroup1, '-name', 'gRIBI Client')
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

ixNet.setMultiAttribute(ixNet.getAttribute(ethernet2, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '44:44:44:44:44:44',
    '-step',      '00:00:00:00:00:01')
ixNet.commit()

# Adding IPv4 stack and configuring  IP Address
print("\n\nAdding IPv4 stack\n")
ixNet.add(ethernet1, 'ipv4')
ixNet.add(ethernet2, 'ipv4')
ixNet.commit()

ip1 = ixNet.getList(ethernet1, 'ipv4')[0]
ip2 = ixNet.getList(ethernet2, 'ipv4')[0]

mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvAdd2 = ixNet.getAttribute(ip2, '-address')
mvGw1 = ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2 = ixNet.getAttribute(ip2, '-gatewayIp')

print ("\n\nconfiguring ipv4 addresses\n")
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', "50.50.50.2")
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', "50.50.50.1")
ixNet.setAttribute(mvGw1 + '/singleValue', '-value', "50.50.50.1")
ixNet.setAttribute(mvGw2 + '/singleValue', '-value', "50.50.50.2")

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')


ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

print ('************************************************************')

#  Adding gRPC Client and configuring it in topology 1 
print "Adding gRPC Client and configuring it in topology\n"
ixNet.add(ip1, 'gRPCClient')
ixNet.commit()
gRPCClient = ixNet.getList(ip1, 'gRPCClient')[0]

print ("Configuring remote ip and remote port in gRPC Client\n")
remoteIpMultiValue1 = ixNet.getAttribute(gRPCClient, '-remoteIp')
ixNet.setAttribute(remoteIpMultiValue1 + '/singleValue', '-value', "50.50.50.1")
remotePortMultiValue1 = ixNet.getAttribute(gRPCClient, '-remotePort')
ixNet.setAttribute(remotePortMultiValue1 + '/singleValue', '-value', "50001")
ixNet.commit()


#  Adding gRIBI Client stack over gRPC Client in topology 1 
print "Adding gRIBI Client stack over gRPC Client in topology 1\n"
ixNet.add(gRPCClient, 'gRIBIClient')
ixNet.commit()
gRIBIClient = ixNet.getList(gRPCClient, 'gRIBIClient')[0]

print "Configuring Client Redundancy and election IDs in gRIBI Client\n"
countMV1 = ixNet.getAttribute(gRIBIClient, '-count')

clientRedundancyMultiValue1 = ixNet.getAttribute(gRIBIClient, '-clientRedundancy')
ixNet.setAttribute(clientRedundancyMultiValue1 + '/singleValue', '-value', "singleprimary")

electionIdHighMultiValue1 = ixNet.getAttribute(gRIBIClient, '-electionIdHigh')
ixNet.setAttribute(electionIdHighMultiValue1 + '/singleValue', '-value', "1001")

electionIdLowMultiValue1 = ixNet.getAttribute(gRIBIClient, '-electionIdLow')
ixNet.setAttribute(electionIdLowMultiValue1 + '/singleValue', '-value', "2001")
ixNet.commit()

#  Adding gRIBI Next Hop Stack over gRIBI Client in topology 1 
print "Adding gRIBI Next Hop Stack over gRIBI Client in topology 1\n"
ixNet.add(gRIBIClient, 'gRIBINextHopGroup')
ixNet.commit()
gRIBINextHopGroup = ixNet.getList(gRIBIClient, 'gRIBINextHopGroup')[0]

ixNet.setAttribute(gRIBINextHopGroup, '-multiplier', '5')
ixNet.commit()

numberOfNextHopsMultiValue1 = ixNet.getAttribute(gRIBINextHopGroup, '-numberOfNextHops')
ixNet.setAttribute(gRIBINextHopGroup, '-numberOfNextHops', "3")
ixNet.commit()

# Adding Network Topology behind Device Group
print "Adding the Network Topology\n"

ixNet.execute('createDefaultStack', gRIBINextHopGroup, 'ipv4PrefixPools')
networkGroup1 = ixNet.getList(deviceGroup1, 'networkGroup')[0]
ixNet.setAttribute(networkGroup1, '-name', "Network Group 1")
ixNet.commit()

print "Configure metadata and Decapsulation Header type for gRIBI IPv4 entries\n"
ipv4PrefixPools = ixNet.getList(networkGroup1, 'ipv4PrefixPools')[0]
gRIBIIpv4Entry = ixNet.getList(ipv4PrefixPools, 'gRIBIIpv4Entry')[0]

metaDataMv1 = ixNet.getAttribute(gRIBIIpv4Entry, '-metaData')
counter = ixNet.add(metaDataMv1, 'counter')
ixNet.setMultiAttribute(counter, '-direction', 'increment', '-start', "aabbccd1", '-step', "00000001")
ixNet.commit()

decapsulationHeaderMv1 = ixNet.getAttribute(gRIBIIpv4Entry, '-decapsulationHeader')
ixNet.setAttribute(decapsulationHeaderMv1 + '/singleValue', '-value', "ipv4")
ixNet.commit()

################################################################################
# Configure gRIBI server on other port( topology 2) or run demo sever in the port
################################################################################
# To enable hw filters on ixia HW ports execute following command.
# filter --enable-all
#
# To enable hw filters on ixia VM ports execute following command.
# sudo /opt/Ixia/sstream/bin/filter --port=1 --enable-all
#
# To start demo server (ixia specific on server port execute following command.
#  <server_filename> -p <remote port>
# ./SyncServer -p 50051
#
# To start gribi_go_server (openconfig gribi server binary file on server port
#  execute following command.
#  <server_filename> -v -logtostderr -gRIBIPort <remote port>
# ./gribi_mips64 -v 5 -logtostderr -gRIBIPort 50051
#
################################################################################


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

print ("Fetching gRIBI client per port Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"gRIBI Client Per Port"/page'
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
# Step 4 > Change following parameters in Next Hop Group 1 
#          Apply changes on the fly.
################################################################################
#---------------------------------------------------------------------------
#    - Color
#    - Backup Next Hop Group
#---------------------------------------------------------------------------

print "\n\nChange parameters in Next Hop Group 1 on-the-fly.....\n"

print "OTF change Color.....\n"
nhGroupMv = ixNet.getAttribute(gRIBINextHopGroup, '-color')
ixNet.setMultiAttribute(nhGroupMv, '-clearOverlays', 'false')
ixNet.commit()

counter = ixNet.add(nhGroupMv, "counter")
ixNet.setMultiAttribute(counter, '-step', '5', '-start', '4001', '-direction', 'increment')
ixNet.commit()
time.sleep(2)

print "OTF change Backup Next Hop Group.....\n"
nhGroupMv = ixNet.getAttribute(gRIBINextHopGroup, '-backupNextHopGroup')
ixNet.setMultiAttribute(nhGroupMv, '-clearOverlays', 'false')
ixNet.commit()

counter = ixNet.add(nhGroupMv, "counter")
ixNet.setMultiAttribute(counter, '-step', '101', '-start', '1', '-direction', 'increment')
ixNet.commit()
time.sleep(2)

globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")
# end try/expect
time.sleep(10)

################################################################################
# Step 5> Retrieve protocol statistics again
################################################################################
print ("Fetching gRIBI client per port Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"gRIBI Client Per Port"/page'
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
# Step 6> Stop all protocols.
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
time.sleep(30)
print ('!!! Test Script Ends !!!')
