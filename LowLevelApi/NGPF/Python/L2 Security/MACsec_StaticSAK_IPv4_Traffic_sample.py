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
# 1. Configure MACSec with Static SAK (HW based)
# 2. Create traffic Item
# 3. Assign ports
# 4. Start all protocols
# 5. Retrieve protocol statistics. (MACsec Per Port)
# 6. Start traffic
# 7. Stop traffic
# 8. Stop all protocols
################################################################################

import time
import sys

#-------------------------------------------------------------------------------
# import IxNetwork
#-------------------------------------------------------------------------------
#IX_NETWORK_LIBRARY_PATH = 'C:/Program Files (x86)/Ixia/IxNetwork/9.15.2101.4/API/Python'
#sys.path.append(IX_NETWORK_LIBRARY_PATH)
import IxNetwork
# START HARNESS VARS **********************************************************
if 'py' not in dir():
    class Py: pass
    py = Py()
    py.ports        = (('10.36.74.52','1','13'),('10.36.74.52','1','17'))
    py.ixTclServer  =  "10.36.67.90"
    py.ixTclPort    =  8909
# END HARNESS VARS ************************************************************

################################################################################
# Connect to IxNet client
################################################################################
ixNet = IxNetwork.IxNet()
ixNet.connect(py.ixTclServer, '-port',  py.ixTclPort,  '-version', '9.15')

################################################################################
# Cleaning up IxNetwork
################################################################################

print("Clean up IxNetwork...")
ixNet.execute('newConfig')
print("Get IxNetwork root object")
root = ixNet.getRoot()

################################################################################
# Add virtual ports
################################################################################
print("Add virtual port 1")
vport1 = ixNet.add(root, 'vport')
ixNet.commit()
vport1 = ixNet.remapIds(vport1)[0]
ixNet.setAttribute(vport1, '-name', '10GE LAN - 001')
ixNet.commit()

print("Add virtual port 2")
vport2 = ixNet.add(root, 'vport')
ixNet.commit()
vport2 = ixNet.remapIds(vport2)[0]
ixNet.setAttribute(vport2, '-name', '10GE LAN - 002')
ixNet.commit()

################################################################################
# Add topology
################################################################################
print("Add Topology 1")
topology1 = ixNet.add(root, 'topology')
ixNet.commit()
topology1 = ixNet.remapIds(topology1)[0]
ixNet.setAttribute(topology1, '-name', 'Topology 1')
ixNet.setAttribute(topology1, '-vports', vport1)
ixNet.commit()
################################################################################
# Add device group in Topology 1
################################################################################
print("Add Device Group 1 in Topology 1")
device1 = ixNet.add(topology1, 'deviceGroup')
ixNet.commit()
device1 = ixNet.remapIds(device1)[0]
ixNet.setAttribute(device1, '-name', 'Device Group 1')
ixNet.setAttribute(device1, '-multiplier', '10')
ixNet.commit()
################################################################################
# Add Ethernet in Device Group 1
################################################################################
print("Add Ethernet in Device Group 1")
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
# Add Macsec on top of Ethernet in Device Group 1
################################################################################
print("Add MACsec in Device Group 1")
macsec1 = ixNet.add(ethernet1, 'macsec')
ixNet.commit()
macsec1 = ixNet.remapIds(macsec1)[0]

print("Configure DUT SCI in Rx Properties of MACsec 1")
dutSciMacMv = ixNet.getAttribute(macsec1, '-dutSciMac')
ixNet.add(dutSciMacMv, 'counter')
ixNet.setMultiAttribute(dutSciMacMv + '/counter',
             '-direction', 'increment',
             '-start',     '00:12:01:00:00:01',
             '-step',      '00:00:00:00:00:01')

ixNet.commit()

################################################################################
# Set CipherSuite AES-XPN-128 for all devices in MACsec 1
################################################################################
print("Set Cipher Suite AES-XPN-128 for all devices in MACsec 1")
cipherSuite1 = ixNet.getAttribute(macsec1, '-cipherSuite')
cipherSuite1 = ixNet.remapIds(cipherSuite1)[0]
cipherSuiteOverlay1 = ixNet.add(cipherSuite1, 'overlay')
cipherSuiteOverlay1 = ixNet.remapIds(cipherSuiteOverlay1)[0]
loop1 = 1
while loop1 <= 10:
    ixNet.setMultiAttribute(cipherSuiteOverlay1, '-index', loop1, '-count', '1', '-value', 'aesxpn128')
    time.sleep(1)
    ixNet.commit()
    time.sleep(1)
    loop1 = loop1 + 1

################################################################################
#  Set Tx SAK Pool size and Rx SAK Pool size for all devices in MACSec 1
################################################################################
print("Set Tx SAK Pool size and Rx SAK Pool size as 4 for all devices in MACsec 1")
ixNet.setAttribute(macsec1, '-txSakPoolSize', '4')
ixNet.setAttribute(macsec1, '-rxSakPoolSize', '4')
ixNet.commit()

################################################################################
#  configure Tx SAK and Rx SAK for all devices in MACSec 1
################################################################################
print("Configure Tx SAK and Rx SAK for all devices in MACSec 1")
txSakPool1 = ixNet.getList(macsec1, 'txSakPool')[0]
txSak128mv1 = ixNet.getAttribute(txSakPool1, '-txSak128')
ixNet.setMultiAttribute(txSak128mv1 + '/counter',
             '-direction', 'increment',
             '-start',     'f123456789abcdef0123456789a11111',
             '-step',      '00000000000000000000000000000001')
ixNet.commit()

rxSakPool1 = ixNet.getList(macsec1, 'rxSakPool')[0]
rxSak128mv1 = ixNet.getAttribute(rxSakPool1, '-rxSak128')
ixNet.setMultiAttribute(rxSak128mv1 + '/counter',
             '-direction', 'increment',
             '-start',     'f123456789abcdef0123456789a11111',
             '-step',      '00000000000000000000000000000001')
ixNet.commit()

################################################################################
# Add Topology 
################################################################################
print("Add Topology 2")
topology2 = ixNet.add(root, 'topology')
ixNet.commit()
topology2 = ixNet.remapIds(topology2)[0]
ixNet.setAttribute(topology2, '-name', 'Topology 2')
ixNet.setAttribute(topology2, '-vports', vport2)
ixNet.commit()
################################################################################
# Add Device Group in Topoloy 2
################################################################################
print("Add Device Group in Topology 2")
device2 = ixNet.add(topology2, 'deviceGroup')
ixNet.commit()
device2 = ixNet.remapIds(device2)[0]
ixNet.setAttribute(device2, '-name', 'Device Group 2')
ixNet.setAttribute(device2, '-multiplier', '10')
ixNet.commit()
################################################################################
# Add Ethernet in Device Group 2
################################################################################
print("Add Ethernet in Device Group 2")
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
# Add Macsec on top of Ethernet in Device Group 2
################################################################################
print("Add MACsec in Device Group 2")
macsec2 = ixNet.add(ethernet2, 'macsec')
ixNet.commit()
macsec2 = ixNet.remapIds(macsec2)[0]

print("Configure DUT SCI in Rx Properties of MACsec 2")
dutSciMacMv = ixNet.getAttribute(macsec2, '-dutSciMac')
ixNet.add(dutSciMacMv, 'counter')
ixNet.setMultiAttribute(dutSciMacMv + '/counter',
             '-direction', 'increment',
             '-start',     '00:11:01:00:00:01',
             '-step',      '00:00:00:00:00:01')

ixNet.commit()

################################################################################
# Set CipherSuite AES-XPN-128 for all devices in MACsec 2
################################################################################
print("Set CipherSuite AES-XPN-128 for all devices in MACsec 2")
cipherSuite2 = ixNet.getAttribute(macsec2, '-cipherSuite')
cipherSuite2 = ixNet.remapIds(cipherSuite2)[0]
cipherSuiteOverlay2 = ixNet.add(cipherSuite2, 'overlay')
cipherSuiteOverlay2 = ixNet.remapIds(cipherSuiteOverlay2)[0]
loop1 = 1
while loop1 <= 10:
    ixNet.setMultiAttribute(cipherSuiteOverlay2, '-index', loop1, '-count', '1', '-value', 'aesxpn128')
    time.sleep(1)
    ixNet.commit()
    time.sleep(1)
    loop1 = loop1 + 1

################################################################################
#  Set Tx SAK Pool size and Rx SAK Pool size for all devices in MACSec 2
################################################################################
print("Set Tx SAK Pool size and Rx SAK Pool size as 4 for all devices in MACSec 2")
ixNet.setAttribute(macsec2, '-txSakPoolSize', '4')
ixNet.setAttribute(macsec2, '-rxSakPoolSize', '4')
ixNet.commit()
################################################################################
#  configure Tx SAK and Rx SAK for all devices in MACSec 2
################################################################################
print("Configure Tx SAK and Rx SAK for all devices in MACSec 2")
txSakPool2 = ixNet.getList(macsec2, 'txSakPool')[0]
txSak128mv2 = ixNet.getAttribute(txSakPool2, '-txSak128')
ixNet.setMultiAttribute(txSak128mv2 + '/counter',
             '-direction', 'increment',
             '-start',     'f123456789abcdef0123456789a11111',
             '-step',      '00000000000000000000000000000001')
ixNet.commit()
rxSakPool2 = ixNet.getList(macsec2, 'rxSakPool')[0]
rxSak128mv2 = ixNet.getAttribute(rxSakPool2, '-rxSak128')
ixNet.setMultiAttribute(rxSak128mv2 + '/counter',
             '-direction', 'increment',
             '-start',     'f123456789abcdef0123456789a11111',
             '-step',      '00000000000000000000000000000001')
ixNet.commit()

################################################################################
# Add IPv4 on top of MACsec
################################################################################
print("Add IPv4")
ixNet.add(macsec1, 'ipv4')
ixNet.add(macsec2, 'ipv4')
ixNet.commit()

ip1 = ixNet.getList(macsec1, 'ipv4')[0]
ip2 = ixNet.getList(macsec2, 'ipv4')[0]

mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvAdd2 = ixNet.getAttribute(ip2, '-address')
mvGw1  = ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = ixNet.getAttribute(ip2, '-gatewayIp')

print("Configure IPv4 Address and Gateway")

ixNet.setMultiAttribute(mvAdd1 + '/counter',
             '-direction', 'increment',
             '-start',     '20.20.1.1',
             '-step',      '0.0.1.0')

ixNet.setMultiAttribute(mvAdd2 + '/counter',
             '-direction', 'increment',
             '-start',     '20.20.1.2',
             '-step',      '0.0.1.0')

ixNet.setMultiAttribute(mvGw1 + '/counter',
             '-direction', 'increment',
             '-start',     '20.20.1.2',
             '-step',      '0.0.1.0')

ixNet.setMultiAttribute(mvGw2 + '/counter',
             '-direction', 'increment',
             '-start',     '20.20.1.1',
             '-step',      '0.0.1.0')
			 
ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
################################################################################
# Create L3 Traffic over IPv4 end points from Device Group 1 to Device Group 2
################################################################################
print ("Create L3 Traffic over IPv4 end points from Device Group 1 to Device Group 2")
ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.commit()
trafficItem1 = ixNet.getList(ixNet.getRoot() + '/traffic', 'trafficItem')[0]
ixNet.setMultiAttribute( trafficItem1,
        '-name'                 ,'Macsec_IPv4_L3_Traffic',
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
ixNet.setAttribute(trafficItem1, '-trafficType', 'ipv4')
ixNet.commit()
ixNet.add(trafficItem1, 'endpointSet',
        '-sources',             ip1,
        '-destinations',        ip2,
        '-name',                'Macsec_IPv4_L3_Traffic',
        '-sourceFilter',        '',
        '-destinationFilter',   '')
ixNet.commit()

################################################################################
# set frame size in Traffic Item
################################################################################
ixNet.setMultiAttribute(trafficItem1 + "/configElement:1/frameSize",
        '-type',        'increment',
        '-incrementFrom', '72',
		'-incrementTo', '1518')
################################################################################
# set frame rate in Traffic Item
################################################################################		
ixNet.setMultiAttribute(trafficItem1 + "/configElement:1/frameRate",
		'-rate',        100)
		
ixNet.setMultiAttribute(trafficItem1 + "/configElement:1/transmissionControl",
        '-duration'               ,1,
        '-iterationCount'         ,1,
        '-startDelayUnits'        ,'bytes',
        '-minGapBytes'            ,12,
        '-frameCount'             ,10000000000,
        '-type'                   ,'fixedFrameCount',
        '-interBurstGapUnits'     ,'nanoseconds',
        '-interBurstGap'          , 0,
        '-enableInterBurstGap'    ,False,
        '-interStreamGap'         ,0,
        '-repeatBurst'            ,1,
        '-enableInterStreamGap'   ,False,
        '-startDelay'             ,0,
        '-burstPacketCount'       ,1,)

ixNet.setMultiAttribute(trafficItem1 + "/tracking", '-trackBy', ['ipv4DestIp0'])

ixNet.commit()

################################################################################
# 3. Assign ports
################################################################################
print("Assign real ports")
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
print("Start all protocols")
################################################################################
# 4. Start all protocols
################################################################################
ixNet.execute('startAllProtocols')
print("Wait for 30 Seconds")
time.sleep(30)

################################################################################
# 5. Retrieve protocol statistics. (MACsec Per Port)                   		   #
################################################################################
print("Fetch MACsec Per Port Statistics\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"MACsec Per Port"/page'
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
# 6. Generate, apply and Start traffic
################################################################################
r = ixNet.getRoot()
ixNet.execute('generate', trafficItem1)
ixNet.execute('apply', r + '/traffic')
ixNet.execute('start', r + '/traffic')

print ("Run traffic for 30 secs")
time.sleep(30)

################################################################################
# Retrieve Traffic Item Flow Statistics 
################################################################################
print ("Retrieve Flow Statistics\n")
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
# 7. Stop traffic
################################################################################
ixNet.execute('stop', r + '/traffic')

################################################################################
# 8. Stop all protocols                                                        #
################################################################################
print ("Stop all protocols")
ixNet.execute('stopAllProtocols')
print ("TEST script ends")
