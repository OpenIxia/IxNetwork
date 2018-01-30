
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
#    This script intends to demonstrate how to use NGPF PCEP API.              #
#      1.  Configure a PCE on topology1 (with 10 PCC group) and a 10 PCC on    #
#          topology2. PCE has 10 PCE initiated LSP configured (1 per PCC).     #
#          Each PCE initiated LSP has 1 ERO. On the Topology 2 each PCC has    #
#          one pre-established LSP configured with 1 ERO each.                 #
#      2.  Assign ports                                                        #
#      3.  Start both PCC and PCE                                              #
#      4.  Retrieve "PCE Sessions Per Port" statistics                         #
#      5.  Execute return delegation from PCE end                              #
#      6.  Check LSP status                                                    #
#      7.  Execute take control from PCE end                                   #
#      8.  Retrieve "PCE Sessions Per Port" statistics                         #
#      9.  Check LSP status.                                                   #
#     10. Stop all protocols.                                                  #
# Ixia Softwares:                                                              #
#    IxOS      8.10 EA                                                         #
#    IxNetwork 8.10 EA                                                         #
#                                                                              #
################################################################################
import time
import sys

#-------------------------------------------------------------------------------
# import IxNetwork
#-------------------------------------------------------------------------------
IX_NETWORK_LIBRARY_PATH = 'C:/Program Files (x86)/Ixia/IxNetwork/8.10.1045.2-EB/API/Python'
sys.path.append(IX_NETWORK_LIBRARY_PATH)
import IxNetwork
# START HARNESS VARS **********************************************************
if 'py' not in dir():
    class Py: pass
    py = Py()
    py.ports        = (('10.216.108.96','4','7'),('10.216.108.96','4','8'))
    py.ixTclServer  =  "10.216.108.113"
    py.ixTclPort    =  8074
# END HARNESS VARS ************************************************************

################################################################################
# Connect to IxNet client
################################################################################
ixNet = IxNetwork.IxNet()
ixNet.connect(py.ixTclServer, '-port',  py.ixTclPort,  '-version', '8.10')

################################################################################
# Cleaning up IxNetwork
################################################################################

print "Cleaning up IxNetwork..."
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
# Adding IPv4 layer
################################################################################
print("Adding ipv4 1")
ipv4Addr1 = ixNet.add(ethernet1, 'ipv4')
ixNet.commit()
ipv4Addr1 = ixNet.remapIds(ipv4Addr1)[0]
addressMv = ixNet.getAttribute(ipv4Addr1, '-address')
ixNet.add(addressMv, 'singleValue')
ixNet.setMultiAttribute(addressMv + '/singleValue',
            '-value', '1.1.1.1')
ixNet.commit()
gatewayIpMv = ixNet.getAttribute(ipv4Addr1, '-gatewayIp')
ixNet.add(gatewayIpMv, 'singleValue')
ixNet.setMultiAttribute(gatewayIpMv + '/singleValue',
            '-value', '1.1.1.2')
ixNet.commit()
################################################################################
# Adding PCE layer
################################################################################
print("Adding PCE 1")
pce1 = ixNet.add(ipv4Addr1, 'pce')
ixNet.commit()
pce1 = ixNet.remapIds(pce1)[0]
################################################################################
# Adding PCC Group
################################################################################
print("Adding PCC Group1")
pccGroup1 = ixNet.add(pce1, 'pccGroup')
ixNet.commit()
pccGroup1 = ixNet.remapIds(pccGroup1)[0]
pccIpv4AddressMv = ixNet.getAttribute(pccGroup1, '-pccIpv4Address')
ixNet.add(pccIpv4AddressMv, 'counter')
ixNet.setMultiAttribute(pccIpv4AddressMv + '/counter',  
             '-direction', 'increment',
             '-start'    , '1.1.1.2',
             '-step'     , '0.0.0.1')
ixNet.commit()
ixNet.setAttribute(pccGroup1, '-multiplier', '10')
ixNet.commit()
ixNet.setAttribute(pccGroup1, '-pceInitiatedLspsPerPcc', '1')
ixNet.commit()
################################################################################
# Adding PCE Initiated LSP parameterd
################################################################################
pccInit1 = pccGroup1+'/pceInitiateLspParameters:1'
ixNet.setAttribute(pccInit1, '-numberOfEroSubObjects', '1')
ixNet.commit()
srcEndPointIpv4Mv = ixNet.getAttribute(pccInit1, '-srcEndPointIpv4')
ixNet.add(srcEndPointIpv4Mv, 'counter')
ixNet.setMultiAttribute(srcEndPointIpv4Mv + '/counter',  
             '-direction', 'increment',
             '-start'    , '100.0.0.1',
             '-step'     , '0.0.0.1')
ixNet.commit()
destEndPointIpv4Mv = ixNet.getAttribute(pccInit1, '-destEndPointIpv4')
ixNet.add(destEndPointIpv4Mv, 'counter')
ixNet.setMultiAttribute(destEndPointIpv4Mv + '/counter',  
             '-direction', 'increment',
             '-start'    , '200.0.0.1',
             '-step'     , '0.0.0.1')
ixNet.commit()
ixNet.setAttribute(pccInit1, '-expectedInitiatedLspList', '::ixNet::OK')
ixNet.commit()
symbolicPathNameMv = ixNet.getAttribute(pccInit1, '-symbolicPathName')
ixNet.add(symbolicPathNameMv, 'string')
ixNet.setMultiAttribute(symbolicPathNameMv + '/string',
            '-pattern', 'IXIA LSP {Inc:1,1}')
ixNet.commit()
################################################################################
# Adding ERO parameterd
################################################################################
pccEro1 = pccInit1+'/pcepEroSubObjectsList:1'
mplsLabelMv = ixNet.getAttribute(pccEro1, '-mplsLabel')
ixNet.add(mplsLabelMv, 'counter')
ixNet.setMultiAttribute(mplsLabelMv + '/counter',  
             '-direction', 'increment',
             '-start'    , '16',
             '-step'     , '1')
ixNet.commit()
localIpv4AddressMv = ixNet.getAttribute(pccEro1, '-localIpv4Address')
ixNet.add(localIpv4AddressMv, 'singleValue')
ixNet.setMultiAttribute(localIpv4AddressMv + '/singleValue',
            '-value', '0.0.0.0')
ixNet.commit()
remoteIpv4AddressMv = ixNet.getAttribute(pccEro1, '-remoteIpv4Address')
ixNet.add(remoteIpv4AddressMv, 'singleValue')
ixNet.setMultiAttribute(remoteIpv4AddressMv + '/singleValue',
            '-value', '0.0.0.0')
ixNet.commit()
fBitMv = ixNet.getAttribute(pccEro1, '-fBit')
ixNet.add(fBitMv, 'singleValue')
ixNet.setMultiAttribute(fBitMv + '/singleValue',
            '-value', 'true')
ixNet.commit()
sidTypeMv = ixNet.getAttribute(pccEro1, '-sidType')
ixNet.add(sidTypeMv, 'singleValue')
ixNet.setMultiAttribute(sidTypeMv + '/singleValue',
            '-value', 'mplslabel20bit')
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
ixNet.setAttribute(device2, '-multiplier', '10')
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
# Adding IPv4 layer
################################################################################
print("Adding ipv4 2")
ipv4Addr2 = ixNet.add(ethernet2, 'ipv4')
ixNet.commit()
ipv4Addr2 = ixNet.remapIds(ipv4Addr2)[0]
addressMv = ixNet.getAttribute(ipv4Addr2, '-address')
ixNet.add(addressMv, 'counter')
ixNet.setMultiAttribute(addressMv + '/counter',  
             '-direction', 'increment',
             '-start'    , '1.1.1.2',
             '-step'     , '0.0.0.1')
ixNet.commit()
gatewayIpMv = ixNet.getAttribute(ipv4Addr2, '-gatewayIp')
ixNet.add(gatewayIpMv, 'singleValue')
ixNet.setMultiAttribute(gatewayIpMv + '/singleValue',
            '-value', '1.1.1.1')
ixNet.commit()
################################################################################
# Adding PCC layer
################################################################################
print("Adding PCC 2")
pcc2 = ixNet.add(ipv4Addr2, 'pcc')
ixNet.commit()
pcc2 = ixNet.remapIds(pcc2)[0]
pceIpv4AddressMv = ixNet.getAttribute(pcc2, '-pceIpv4Address')
ixNet.add(pceIpv4AddressMv, 'singleValue')
ixNet.setMultiAttribute(pceIpv4AddressMv + '/singleValue',
            '-value', '1.1.1.1')
ixNet.commit()
ixNet.setAttribute(pcc2, '-expectedInitiatedLspsForTraffic', '0')
ixNet.commit()
ixNet.setAttribute(pcc2, '-preEstablishedSrLspsPerPcc', '1')
ixNet.commit()

################################################################################
# Adding pre established sr LSP
################################################################################
preLsp2 = pcc2+'/preEstablishedSrLsps:1'
symbolicPathNameMv = ixNet.getAttribute(preLsp2, '-symbolicPathName')
ixNet.add(symbolicPathNameMv, 'string')
ixNet.setMultiAttribute(symbolicPathNameMv + '/string',
            '-pattern', 'IXIA SYNC LSP {Inc:1,1}')
ixNet.commit()
srcEndPointIpv4Mv = ixNet.getAttribute(preLsp2, '-srcEndPointIpv4')
ixNet.add(srcEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(srcEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
ixNet.commit()
srcEndPointIpv6Mv = ixNet.getAttribute(preLsp2, '-srcEndPointIpv6')
ixNet.add(srcEndPointIpv6Mv, 'singleValue')
ixNet.setMultiAttribute(srcEndPointIpv6Mv + '/singleValue',
            '-value', '0:0:0:0:0:0:0:0')
ixNet.commit()
################################################################################
# Adding pre established ERO of sr LSP
################################################################################
preSr2 = preLsp2+'/pcepEroSubObjectsList:1'
mplsLabelMv = ixNet.getAttribute(preSr2, '-mplsLabel')
ixNet.add(mplsLabelMv, 'singleValue')
ixNet.setMultiAttribute(mplsLabelMv + '/singleValue',
            '-value', '16')
ixNet.commit()
localIpv4AddressMv = ixNet.getAttribute(preSr2, '-localIpv4Address')
ixNet.add(localIpv4AddressMv, 'singleValue')
ixNet.setMultiAttribute(localIpv4AddressMv + '/singleValue',
            '-value', '0.0.0.0')
ixNet.commit()
remoteIpv4AddressMv = ixNet.getAttribute(preSr2, '-remoteIpv4Address')
ixNet.add(remoteIpv4AddressMv, 'singleValue')
ixNet.setMultiAttribute(remoteIpv4AddressMv + '/singleValue',
            '-value', '0.0.0.0')
ixNet.commit()
fBitMv = ixNet.getAttribute(preSr2, '-fBit')
ixNet.add(fBitMv, 'singleValue')
ixNet.setMultiAttribute(fBitMv + '/singleValue',
            '-value', 'true')
ixNet.commit()
sidTypeMv = ixNet.getAttribute(preSr2, '-sidType')
ixNet.add(sidTypeMv, 'singleValue')
ixNet.setMultiAttribute(sidTypeMv + '/singleValue',
            '-value', 'mplslabel20bit')
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
print("Wait for 1 minute")
time.sleep(60)

################################################################################
# 4. Retrieve protocol statistics  (PCE Sessions Per Port)                     #
################################################################################
print ("Fetching all Protocol Summary Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"PCE Sessions Per Port"/page'
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-40s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")

#################################################################################
# 5. Execute return deligation
#################################################################################
print("Executing return deligation")
for i in range(1, 11) :
    ixNet.execute('returnDelegation', pccInit1, i)
# end for
time.sleep(5)

#################################################################################
#  6. Check LSP state
#################################################################################
print("Checking LSP State")
lspState = ixNet.getAttribute(pccInit1, '-sessionInfo')
for i in range(1, 11) :
    print ("State of LSP %s is %s" % (i, lspState[i - 1]))
# end for

#################################################################################
# 7. Execute return takeControl
#################################################################################
print("Executing take control")
for i in range(1, 11) :
    ixNet.execute('takeControl', pccInit1, i)
# end for
time.sleep(5)

#################################################################################
# 8. Check LSP state again
#################################################################################
print("Checking LSP State")
lspState = ixNet.getAttribute(pccInit1, '-sessionInfo')
for i in range(1, 11) :
    print ("State of LSP %s is %s" % (i, lspState[i - 1]))
# end for

################################################################################
# 9. Retrieve protocol statistics                                              #
################################################################################
print ("Fetching all Protocol Summary Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"PCE Sessions Per Port"/page'
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-40s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")

################################################################################
# 10. Stop all protocols                                                       #
################################################################################
ixNet.execute('stopAllProtocols')




