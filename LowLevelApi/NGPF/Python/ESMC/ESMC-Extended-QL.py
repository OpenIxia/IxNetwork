# -*- coding: cp1252 -*-
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    29/06/2018 - Rupkatha Guha - created sample                               #
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
#    This script intends to demonstrate how to configure ESMC topology         #
#                                                                              #
# About Topology:                                                              #
#                                                                              #
#     On the port, configure an ESMC topology with extended Quality Level      #
#     enabled. 					                               #
#                                                                              #
# Script Flow:                                                                 #
#    1. Configuration of protocols as described in topology.                   #
#    2. Start the ESMC protocol.                                               #
#    3. Retrieve protocol statistics.                                          #
#    4. Stop all protocols.                                                    #
#                                                                              #                                                                                
# Ixia Software:                                                               #
#    IxOS      9.10 EB                                                         #
#    IxNetwork 9.10 EB                                                         #
#                                                                              #
################################################################################
import os
import sys
import time

def assignPorts (ixNet, realPort1) :
     chassis1 = realPort1[0]
     card1    = realPort1[1]
     port1    = realPort1[2]

     root = ixNet.getRoot()
     vport1 = ixNet.add(root, 'vport')
     ixNet.commit()
     vport1 = ixNet.remapIds(vport1)[0]


     chassisObj1 = ixNet.add(root + '/availableHardware', 'chassis')
     ixNet.setAttribute(chassisObj1, '-hostname', chassis1)
     ixNet.commit()
     chassisObj1 = ixNet.remapIds(chassisObj1)[0]


     cardPortRef1 = chassisObj1 + '/card:%s/port:%s' % (card1,port1)
     ixNet.setMultiAttribute(vport1, '-connectedTo', cardPortRef1,
         '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 001')
     ixNet.commit()

# end def assignPorts

################################################################################
# Either feed the ixNetwork library path in the sys.path as below, or put the
# IxNetwork.pm file somewhere else where we python can autoload it.
# "IxNetwork.pm" is available in <IxNetwork_installer_path>\API\Python
################################################################################
ixNetPath = r'/home/lacp/regress-test/linux-run'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.39.50.134'
ixTclPort   = '8779'
ports       = [('10.39.50.126', '1', '3',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '9.10', '-setAttribute', 'strict')
print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

# assigning ports
assignPorts(ixNet, ports[0])
time.sleep(5)

root    = ixNet.getRoot()
vportTx = ixNet.getList(root, 'vport')[0]


print("adding topologies")
ixNet.add(root, 'topology', '-vports', vportTx)
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]


print "Adding 2 device groups"
ixNet.add(topo1, 'deviceGroup')

ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')


t1dev1 = t1devices[0]


print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(t1dev1, '-multiplier', '1')

ixNet.commit()

print("Adding ethernet/mac endpoints")
ixNet.add(t1dev1, 'ethernet')

ixNet.commit()

mac1 = ixNet.getList(t1dev1, 'ethernet')[0]


print("Configuring the mac addresses %s" % (mac1))
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '00:11:01:00:00:01',
    '-step',      '00:00:00:00:00:01')


ixNet.commit()


print("Add esmc")
ixNet.add(mac1, 'esmc')

ixNet.commit()

esmc1 = ixNet.getList(mac1, 'esmc')[0]

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'ESMC Topology')

ixNet.commit()


print("Enabling Extended Quality Level")
customSyncE = ixNet.getAttribute(esmc1, '-extendedQlTlvEnable')
customSyncE_enable = customSyncE + '/singleValue'
ixNet.setMultiAttribute(customSyncE_enable, '-value', 'true')
ixNet.commit()


print("Setting the Quality Level to EEEC option1")
ql = ixNet.getAttribute(esmc1, '-qualityLevel')
qllevel = ql + '/singleValue'
ixNet.setMultiAttribute(qllevel, '-value', 'ql_eeec_op1')
ixNet.commit()


print"Enabling Custom SyncE CLock Identity for topo1"
customSyncE = ixNet.getAttribute(esmc1, '-enableCustomSyncEclockIdentity')
customSyncE_enable = customSyncE + '/singleValue'
ixNet.setMultiAttribute(customSyncE_enable, '-value', 'true')
ixNet.commit()


print("Setting the SyncE clock Identiy")
custsync = ixNet.getAttribute(esmc1, '-customSyncEclockIdentity')
custsync1 = custsync + '/singleValue'
ixNet.setMultiAttribute(custsync1, '-value', '2202AAFD000006')
ixNet.commit()

print"Enabling Mixed EECs for topo1"
mixed_eecs = ixNet.getAttribute(esmc1, '-mixedEECs')
mixed_eecs_1 = mixed_eecs + '/singleValue'
ixNet.setMultiAttribute(mixed_eecs_1, '-value', 'true')
ixNet.commit()

print"Enabling Partial Chain for topo1"
partial_chain = ixNet.getAttribute(esmc1, '-partialChain')
partial_Chain_1 = partial_chain + '/singleValue'
ixNet.setMultiAttribute(partial_Chain_1, '-value', 'true')
ixNet.commit()


print("Configuring the number of cascased EECs")

caseecs = ixNet.getAttribute(esmc1, '-numberOfCascadedEecs')
caseecs1 = caseecs + '/singleValue'
ixNet.setMultiAttribute(caseecs1, '-value', '4')
ixNet.commit()

print"Configuring the number of Cascaded eEECs"
cascaded_Eeecs = ixNet.getAttribute(esmc1, '-numberOfCascadedEeecs')
cascaded_Eeecs_1 = cascaded_Eeecs + '/singleValue'
ixNet.setMultiAttribute(cascaded_Eeecs_1, '-value', '20')
ixNet.commit()

################################################################################
# 2. Start all protocols and wait for 30 seconds
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(30)


################################################################################
# 3. Retrieve protocol statistics.
################################################################################
print ("Fetching all Protocol Summary Stats\n")

viewPage  = '::ixNet::OBJ-/statistics/view:"ESMC Per Port"/page'
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
