################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA                                             #
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
# Description: 
# 1. Configuring macsec Hardware Based IP Data Traffic.
# 2. Assign ports
# 3. Start all protocols
# 4. Create traffic Item
# 5. Start traffic
# 6. Stop traffic
# 7. Stop all protocols
################################################################################

import time
import sys

#-------------------------------------------------------------------------------
# import IxNetwork
#-------------------------------------------------------------------------------
IX_NETWORK_LIBRARY_PATH = 'C:/Program Files (x86)/Ixia/IxNetwork/9.01.1910.73/API/Python'
sys.path.append(IX_NETWORK_LIBRARY_PATH)
import IxNetwork
# START HARNESS VARS **********************************************************
if 'py' not in dir():
    class Py: pass
    py = Py()
    py.ports        = (('10.39.50.226','1','5'),('10.39.50.226','1','6'))
    py.ixTclServer  =  "10.39.50.102"
    py.ixTclPort    =  9890
# END HARNESS VARS ************************************************************

################################################################################
# Connect to IxNet client
################################################################################
ixNet = IxNetwork.IxNet()
ixNet.connect(py.ixTclServer, '-port',  py.ixTclPort,  '-version', '9.01')

################################################################################
# Cleaning up IxNetwork
################################################################################

print("Cleaning up IxNetwork...")
ixNet.execute('newConfig')
print("Get IxNetwork root object")
root = ixNet.getRoot()

################################################################################
# Adding virtual ports
################################################################################
print("Adding virtual port 1")
vport1 = ixNet.add(root, 'vport')
ixNet.commit()
vport1 = ixNet.remapIds(vport1)[0]
ixNet.setAttribute(vport1, '-name', '10GE LAN - 001')
ixNet.commit()

print("Adding virtual port 2")
vport2 = ixNet.add(root, 'vport')
ixNet.commit()
vport2 = ixNet.remapIds(vport2)[0]
ixNet.setAttribute(vport2, '-name', '10GE LAN - 002')
ixNet.commit()

################################################################################
# Adding topology
################################################################################
print("Adding topology 1")
topology1 = ixNet.add(root, 'topology')
ixNet.commit()
topology1 = ixNet.remapIds(topology1)[0]
ixNet.setAttribute(topology1, '-name', 'Topology 1')
ixNet.setAttribute(topology1, '-vports', vport1)
ixNet.commit()
################################################################################
# Adding device group
################################################################################
print("Adding device group 1")
device1 = ixNet.add(topology1, 'deviceGroup')
ixNet.commit()
device1 = ixNet.remapIds(device1)[0]
ixNet.setAttribute(device1, '-name', 'Device Group 1')
ixNet.setAttribute(device1, '-multiplier', '1')
ixNet.commit()
################################################################################
# Adding ethernet layer
################################################################################
print("Adding ethernet 1")
ethernet1 = ixNet.add(device1, 'ethernet')
ixNet.commit()
ethernet1 = ixNet.remapIds(ethernet1)[0]
macMv = ixNet.getAttribute(ethernet1, '-mac')
ixNet.add(macMv, 'counter')
ixNet.setMultiAttribute(macMv + '/counter',  
             '-direction', 'increment',
             '-start'    , '00:11:01:00:00:01',
             '-step'     , '00:00:00:00:00:01')
ixNet.commit()

################################################################################
# Adding Static Macsec layer on Topology 1
################################################################################
print("Adding Static MACsec 1")
staticMacsec1 = ixNet.add(ethernet1, 'staticMacsec')
ixNet.commit()
staticMacsec1 = ixNet.remapIds(staticMacsec1)[0]
dutMacMv = ixNet.getAttribute(staticMacsec1, '-dutMac')
ixNet.add(dutMacMv, 'counter')
ixNet.setMultiAttribute(dutMacMv + '/counter',
             '-direction', 'increment',
             '-start',     '00:12:01:00:00:01',
             '-step',      '00:00:00:00:00:01')

ixNet.commit()
dutSciMacMv = ixNet.getAttribute(staticMacsec1, '-dutSciMac')
ixNet.add(dutSciMacMv, 'counter')
ixNet.setMultiAttribute(dutSciMacMv + '/counter',
             '-direction', 'increment',
             '-start',     '00:12:01:00:00:01',
             '-step',      '00:00:00:00:00:01')

ixNet.commit()
portIdMv = ixNet.getAttribute(staticMacsec1, '-portId')
ixNet.add(portIdMv, 'counter')
ixNet.setMultiAttribute(portIdMv + '/counter',
             '-direction', 'increment',
             '-start',     '20',
             '-step',      '1')

ixNet.commit()
dutSciPortIdMv = ixNet.getAttribute(staticMacsec1, '-dutSciPortId')
ixNet.add(dutSciPortIdMv, 'counter')
ixNet.setMultiAttribute(dutSciPortIdMv + '/counter',
             '-direction', 'increment',
             '-start',     '20',
             '-step',      '1')

ixNet.commit()

################################################################################
# Adding topology
################################################################################
print("Adding topology 2")
topology2 = ixNet.add(root, 'topology')
ixNet.commit()
topology2 = ixNet.remapIds(topology2)[0]
ixNet.setAttribute(topology2, '-name', 'Topology 2')
ixNet.setAttribute(topology2, '-vports', vport2)
ixNet.commit()
################################################################################
# Adding device group
################################################################################
print("Adding device group 2")
device2 = ixNet.add(topology2, 'deviceGroup')
ixNet.commit()
device2 = ixNet.remapIds(device2)[0]
ixNet.setAttribute(device2, '-name', 'Device Group 2')
ixNet.setAttribute(device2, '-multiplier', '1')
ixNet.commit()
################################################################################
# Adding ethernet layer
################################################################################
print("Adding ethernet 2")
ethernet2 = ixNet.add(device2, 'ethernet')
ixNet.commit()
ethernet2 = ixNet.remapIds(ethernet2)[0]
macMv = ixNet.getAttribute(ethernet2, '-mac')
ixNet.add(macMv, 'counter')
ixNet.setMultiAttribute(macMv + '/counter',  
             '-direction', 'increment',
             '-start'    , '00:12:01:00:00:01',
             '-step'     , '00:00:00:00:00:01')
ixNet.commit()

################################################################################
# Adding Static Macsec layer on Topology 2
################################################################################
print("Adding Static MACsec 2")
staticMacsec2 = ixNet.add(ethernet2, 'staticMacsec')
ixNet.commit()
staticMacsec2 = ixNet.remapIds(staticMacsec2)[0]
dutMacMv = ixNet.getAttribute(staticMacsec2, '-dutMac')
ixNet.add(dutMacMv, 'counter')
ixNet.setMultiAttribute(dutMacMv + '/counter',
             '-direction', 'increment',
             '-start',     '00:11:01:00:00:01',
             '-step',      '00:00:00:00:00:01')

ixNet.commit()
dutSciMacMv = ixNet.getAttribute(staticMacsec2, '-dutSciMac')
ixNet.add(dutSciMacMv, 'counter')
ixNet.setMultiAttribute(dutSciMacMv + '/counter',
             '-direction', 'increment',
             '-start',     '00:11:01:00:00:01',
             '-step',      '00:00:00:00:00:01')

ixNet.commit()
portIdMv = ixNet.getAttribute(staticMacsec2, '-portId')
ixNet.add(portIdMv, 'counter')
ixNet.setMultiAttribute(portIdMv + '/counter',
             '-direction', 'increment',
             '-start',     '20',
             '-step',      '1')

ixNet.commit()
dutSciPortIdMv = ixNet.getAttribute(staticMacsec2, '-dutSciPortId')
ixNet.add(dutSciPortIdMv, 'counter')
ixNet.setMultiAttribute(dutSciPortIdMv + '/counter',
             '-direction', 'increment',
             '-start',     '20',
             '-step',      '1')

ixNet.commit()
################################################################################
# Creating Traffic for Creating Traffic from Static MACsec1 to Static MACsec2
################################################################################
print ('')
print ("Creating Traffic for Creating Traffic from Static MACsec1 to Static MACsec2")

ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.commit()
ti1 = ixNet.getList(ixNet.getRoot() + '/traffic', 'trafficItem')[0]
ixNet.setMultiAttribute( ti1,
        '-name'                 ,'Static_Macsec_IP_Traffic',
        '-trafficType'          ,'ipv4',
        '-allowSelfDestined'    ,False,
        '-trafficItemType'      ,'l2L3',
        '-mergeDestinations'    ,True,
        '-egressEnabled'        ,False,
        '-enabled'              ,True,
        '-routeMesh'            ,'fullMesh',
        '-transmitMode'         ,'interleaved',
        '-hostsPerNetwork'      ,1)
ixNet.commit()
ixNet.setAttribute(ti1, '-trafficType', 'ipv4')
ixNet.commit()
ixNet.add(ti1, 'endpointSet',
        '-sources',             staticMacsec1,
        '-destinations',        staticMacsec2,
        '-name',                'Static_Macsec_IP_Traffic',
        '-sourceFilter',        '',
        '-destinationFilter',   '')
ixNet.commit()
ixNet.setMultiAttribute(ti1 + "/configElement:1/frameSize",
        '-type',        'fixed',
        '-fixedSize',   128)
ixNet.setMultiAttribute(ti1 + "/configElement:1/frameRate",
        '-type',        'packetsPerSecond',
        '-rate',        10)
ixNet.setMultiAttribute(ti1 + "/configElement:1/transmissionControl",
        '-duration'               ,1,
        '-iterationCount'         ,1,
        '-startDelayUnits'        ,'bytes',
        '-minGapBytes'            ,12,
        '-frameCount'             ,1000000,
        '-type'                   ,'fixedFrameCount',
        '-interBurstGapUnits'     ,'nanoseconds',
        '-interBurstGap'          , 0,
        '-enableInterBurstGap'    ,False,
        '-interStreamGap'         ,0,
        '-repeatBurst'            ,1,
        '-enableInterStreamGap'   ,False,
        '-startDelay'             ,0,
        '-burstPacketCount'       ,1,)

ixNet.commit()

################################################################################
# 2. Assign ports
################################################################################
print("Assigning ports")
chassisIp = py.ports[0][0]
card1     = py.ports[0][1]
port1     = py.ports[0][2]
card2     = py.ports[1][1]
port2     = py.ports[1][2]

chassis = ixNet.add(root + '/availableHardware', 'chassis')
ixNet.setMultiAttribute(chassis, '-hostname', chassisIp)
ixNet.commit()

ixNet.setAttribute(vport1, '-connectedTo',
    '%s/card:%s/port:%s' % (chassis, card1, port1))
ixNet.commit()

ixNet.setAttribute(vport2, '-connectedTo',
    '%s/card:%s/port:%s' % (chassis, card2, port2))
ixNet.commit()

time.sleep(5)
print("Starting all protocols")
################################################################################
# 3. Start all protocols
################################################################################
ixNet.execute('startAllProtocols')
print("Wait for 20 Seconds")
time.sleep(20)

################################################################################
# 4. Retrieve protocol statistics. (Static MACsec Per Port)                   #
################################################################################
print("Fetching all Static MACsec Per Port Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"Static MACsec Per Port"/page'
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
# Generate, apply and start traffic
################################################################################
r = ixNet.getRoot()
ixNet.execute('generate', ti1)
ixNet.execute('apply', r + '/traffic')
ixNet.execute('start', r + '/traffic')
print ("Sleep 30sec to send all traffic")
time.sleep(30)

################################################################################
# Checking Stats to see if traffic was sent OK
################################################################################
print ("Checking Stats to see if traffic was sent OK")
print ("Getting the object for view Traffic Item Statistics")
viewName = "Traffic Item Statistics"
views = ixNet.getList('/statistics', 'view')
viewObj = ''
editedViewName = '::ixNet::OBJ-/statistics/view:\"' + viewName + '\"'
for view in views:
    if editedViewName == view:
         viewObj = view
         break
print ("Getting the Tx/Rx Frames values")
txFrames = ixNet.execute('getColumnValues', viewObj, 'Tx Frames')
rxFrames = ixNet.execute('getColumnValues', viewObj, 'Rx Frames')
for txStat, rxStat in zip(txFrames, rxFrames):
    if txStat != rxStat:
        print ("Rx Frames (%s) != Tx Frames (%s)" % (txStat, rxStat))
        raise TestFailedError('Fail the test')
    else:
        print ("No loss found: Rx Frames (%s) = Tx Frames (%s)" % (txStat, rxStat))
		
##############################################################################
# Stop traffic
################################################################################
ixNet.execute('stop', r + '/traffic')
print ("Sleep 10sec to send all traffic")
time.sleep(10)
		
print("***************************************************")

################################################################################
# 6. Stop all protocols                                                        #
################################################################################
print ("Stop all protocols")
ixNet.execute('stopAllProtocols')
