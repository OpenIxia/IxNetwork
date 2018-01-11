
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
#    This script intends to demonstrate how to use NGPF PCEP's PPAG            #
#    related APIs like Association Id, Protection LSP, Standby Mode etc.       #
#      1. Configures a 2PCE on the topology1 and a 2PCC on topology2. The PCE  #
#         two PCC Group each with 5 LSPs and associated PPAG (Path Protection  #
#         Association Group) properties.                                       #
#      2. Stats PCC and PCE.                                                   #
#      3. Verify statistics from "Protocols Summary" view                      #
#      4. Fetch PCC learned information                                        #
#      5. Stop all protocols.                                                  #
# Ixia Software:                                                               #
#    IxOS      8.20 EA                                                         #
#    IxNetwork 8.20 EA                                                         #
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
    py.ports        = (('10.216.108.96','6','3'),('10.216.108.96','6','4'))
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

print("Cleaning up IxNetwork ...");
ixNet.execute('newConfig');
print("Get IxNetwork root object")
root = ixNet.getRoot()

################################################################################
# Adding virtual ports
################################################################################
print("Adding virtual port 1")
vport1 = ixNet.add(root, 'vport')
ixNet.commit()
vport1 = ixNet.remapIds(vport1)[0]
ixNet.setAttribute(vport1, '-name', 'Ethernet - 001')
ixNet.commit()

print("Adding virtual port 2")
vport2 = ixNet.add(root, 'vport')
ixNet.commit()
vport2 = ixNet.remapIds(vport2)[0]
ixNet.setAttribute(vport2, '-name', 'Ethernet - 002')
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
ixNet.setAttribute(device1, '-multiplier', '2')
ixNet.commit()
################################################################################
# Adding ethernet layer
################################################################################
print("Adding ethernet 1")
ethernet1 = ixNet.add(device1, 'ethernet')
ixNet.commit()
ethernet1 = ixNet.remapIds(ethernet1)[0]
# setting -mac
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
# setting -address
addressMv = ixNet.getAttribute(ipv4Addr1, '-address')
ixNet.add(addressMv, 'counter')
ixNet.setMultiAttribute(addressMv + '/counter',  
             '-direction', 'increment',
             '-start'    , '20.0.0.1',
             '-step'     , '0.0.0.1')
ixNet.commit()
# setting -gatewayIp
gatewayIpMv = ixNet.getAttribute(ipv4Addr1, '-gatewayIp')
ixNet.add(gatewayIpMv, 'singleValue')
ixNet.setMultiAttribute(gatewayIpMv + '/singleValue',
            '-value', '20.0.0.11')
ixNet.commit()
################################################################################
# Adding PCC layer
# Configured parameters :
#    -pceIpv4Address
#    -expectedInitiatedLspsForTraffic
#    -preEstablishedSrLspsPerPcc
#    -requestedLspsPerPcc
################################################################################
print("Adding PCC 1")
pcc1 = ixNet.add(ipv4Addr1, 'pcc')
ixNet.commit()
pcc1 = ixNet.remapIds(pcc1)[0]
# setting -pceIpv4Address
pceIpv4AddressMv = ixNet.getAttribute(pcc1, '-pceIpv4Address')
ixNet.add(pceIpv4AddressMv, 'singleValue')
ixNet.setMultiAttribute(pceIpv4AddressMv + '/singleValue',
            '-value', '20.0.0.11')
ixNet.commit()
# setting -expectedInitiatedLspsForTraffic
ixNet.setAttribute(pcc1, '-expectedInitiatedLspsForTraffic', '0')
ixNet.commit()
# setting -preEstablishedSrLspsPerPcc
ixNet.setAttribute(pcc1, '-preEstablishedSrLspsPerPcc', '0')
ixNet.commit()
# setting -requestedLspsPerPcc
ixNet.setAttribute(pcc1, '-requestedLspsPerPcc', '0')
ixNet.commit()
################################################################################
# Adding PCC Expected  LSP parameterd
# Configured parameters :
#    -symbolicPathName
#    -sourceIpv4Address
#    -sourceIpv6Address
################################################################################
################################################################################
# Adding pre established  sr LSP
# Configured parameters :
#    -symbolicPathName
#    -srcEndPointIpv4
#    -srcEndPointIpv6
################################################################################
################################################################################
# Adding Requested LSPs
# Configured parameters :
#    -sourceIpv6Address
#    -sourceIpv4Address
#    -includeMetric
#    -maxNoOfIroSubObjects
################################################################################

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
# setting -mac
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
# setting -address
addressMv = ixNet.getAttribute(ipv4Addr2, '-address')
ixNet.add(addressMv, 'singleValue')
ixNet.setMultiAttribute(addressMv + '/singleValue',
            '-value', '20.0.0.11')
ixNet.commit()
# setting -gatewayIp
gatewayIpMv = ixNet.getAttribute(ipv4Addr2, '-gatewayIp')
ixNet.add(gatewayIpMv, 'counter')
ixNet.setMultiAttribute(gatewayIpMv + '/counter',  
             '-direction', 'increment',
             '-start'    , '0.0.0.0',
             '-step'     , '0.0.1.0')
ixNet.commit()
################################################################################
# Adding PCE layer
################################################################################
print("Adding PCE 2")
pce2 = ixNet.add(ipv4Addr2, 'pce')
ixNet.commit()
pce2 = ixNet.remapIds(pce2)[0]
################################################################################
# Adding PCC Group
# Configured parameters :
#    -pccIpv4Address
#    -multiplier
#    -pceInitiatedLspsPerPcc
################################################################################
print("Adding PCC Group2");
pccGroup2 = ixNet.add(pce2, 'pccGroup')
ixNet.commit()
pccGroup2 = ixNet.remapIds(pccGroup2)[0]
# setting -pccIpv4Address
pccIpv4AddressMv = ixNet.getAttribute(pccGroup2, '-pccIpv4Address')
ixNet.add(pccIpv4AddressMv, 'counter')
ixNet.setMultiAttribute(pccIpv4AddressMv + '/counter',  
             '-direction', 'increment',
             '-start'    , '20.0.0.1',
             '-step'     , '0.0.0.1')
ixNet.commit()
# setting -multiplier
ixNet.setAttribute(pccGroup2, '-multiplier', '2')
ixNet.commit()
# setting -pceInitiatedLspsPerPcc
ixNet.setAttribute(pccGroup2, '-pceInitiatedLspsPerPcc', '10')
ixNet.commit()
################################################################################
# Adding PCE Initiated LSP parameterd
# Configured parameters :
#    -numberOfEroSubObjects
#    -srcEndPointIpv4
#    -destEndPointIpv4
#    -symbolicPathName
#    -includeAssociation
#    -standbyMode
#    -protectionLsp
#    -associationId
################################################################################
pccInit2 = pccGroup2+'/pceInitiateLspParameters:10'
# setting -numberOfEroSubObjects
ixNet.setAttribute(pccInit2, '-numberOfEroSubObjects', '1')
ixNet.commit()
# setting -srcEndPointIpv4
srcEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-srcEndPointIpv4')
ixNet.add(srcEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(srcEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 2 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 3 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 4 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 5 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 6 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 7 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 8 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 9 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 10 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 11 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 12 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 13 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 14 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 15 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 16 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 17 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 18 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 19 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# Adding overlay 20 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# setting -destEndPointIpv4
destEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-destEndPointIpv4')
ixNet.add(destEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(destEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 2 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 3 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 4 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 5 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 6 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 7 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 8 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 9 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 10 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 11 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 12 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 13 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 14 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 15 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 16 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 17 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 18 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 19 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# Adding overlay 20 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# setting -symbolicPathName
symbolicPathNameMv = ixNet.getAttribute(pccInit2, '-symbolicPathName')
ixNet.add(symbolicPathNameMv, 'string')
ixNet.setMultiAttribute(symbolicPathNameMv + '/string',
            '-pattern', 'IXIA LSP {Inc:1,1}')
ixNet.commit()
# setting -includeAssociation
includeAssociationMv = ixNet.getAttribute(pccInit2, '-includeAssociation')
ixNet.add(includeAssociationMv, 'singleValue')
ixNet.setMultiAttribute(includeAssociationMv + '/singleValue',
            '-value', 'true')
# Adding overlay 1 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 5 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 6 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 7 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 8 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 9 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 10 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -standbyMode
standbyModeMv = ixNet.getAttribute(pccInit2, '-standbyMode')
ixNet.add(standbyModeMv, 'alternate')
# Adding overlay 1 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -protectionLsp
protectionLspMv = ixNet.getAttribute(pccInit2, '-protectionLsp')
ixNet.add(protectionLspMv, 'singleValue')
ixNet.setMultiAttribute(protectionLspMv + '/singleValue',
            '-value', 'false')
# Adding overlay 1 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 2 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 3 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 4 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 5 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 6 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 7 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 8 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 9 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 10 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# setting -associationId
associationIdMv = ixNet.getAttribute(pccInit2, '-associationId')
ixNet.add(associationIdMv, 'singleValue')
ixNet.setMultiAttribute(associationIdMv + '/singleValue',
            '-value', '1')
# Adding overlay 1 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 2 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 3 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 4 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 5 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 6 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 7 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 8 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 9 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 10 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 11 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

# Adding overlay 12 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

pccInit2 = pccGroup2+'/pceInitiateLspParameters:10'
# setting -numberOfEroSubObjects
ixNet.setAttribute(pccInit2, '-numberOfEroSubObjects', '1')
ixNet.commit()
# setting -srcEndPointIpv4
srcEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-srcEndPointIpv4')
ixNet.add(srcEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(srcEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 2 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 3 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 4 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 5 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 6 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 7 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 8 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 9 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 10 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 11 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 12 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 13 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 14 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 15 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 16 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 17 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 18 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 19 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# Adding overlay 20 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# setting -destEndPointIpv4
destEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-destEndPointIpv4')
ixNet.add(destEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(destEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 2 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 3 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 4 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 5 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 6 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 7 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 8 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 9 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 10 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 11 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 12 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 13 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 14 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 15 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 16 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 17 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 18 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 19 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# Adding overlay 20 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# setting -symbolicPathName
symbolicPathNameMv = ixNet.getAttribute(pccInit2, '-symbolicPathName')
ixNet.add(symbolicPathNameMv, 'string')
ixNet.setMultiAttribute(symbolicPathNameMv + '/string',
            '-pattern', 'IXIA LSP {Inc:1,1}')
ixNet.commit()
# setting -includeAssociation
includeAssociationMv = ixNet.getAttribute(pccInit2, '-includeAssociation')
ixNet.add(includeAssociationMv, 'singleValue')
ixNet.setMultiAttribute(includeAssociationMv + '/singleValue',
            '-value', 'true')
# Adding overlay 1 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 5 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 6 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 7 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 8 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 9 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 10 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -standbyMode
standbyModeMv = ixNet.getAttribute(pccInit2, '-standbyMode')
ixNet.add(standbyModeMv, 'alternate')
# Adding overlay 1 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -protectionLsp
protectionLspMv = ixNet.getAttribute(pccInit2, '-protectionLsp')
ixNet.add(protectionLspMv, 'singleValue')
ixNet.setMultiAttribute(protectionLspMv + '/singleValue',
            '-value', 'false')
# Adding overlay 1 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 2 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 3 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 4 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 5 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 6 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 7 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 8 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 9 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 10 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# setting -associationId
associationIdMv = ixNet.getAttribute(pccInit2, '-associationId')
ixNet.add(associationIdMv, 'singleValue')
ixNet.setMultiAttribute(associationIdMv + '/singleValue',
            '-value', '1')
# Adding overlay 1 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 2 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 3 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 4 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 5 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 6 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 7 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 8 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 9 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 10 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 11 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

# Adding overlay 12 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

pccInit2 = pccGroup2+'/pceInitiateLspParameters:10'
# setting -numberOfEroSubObjects
ixNet.setAttribute(pccInit2, '-numberOfEroSubObjects', '1')
ixNet.commit()
# setting -srcEndPointIpv4
srcEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-srcEndPointIpv4')
ixNet.add(srcEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(srcEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 2 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 3 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 4 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 5 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 6 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 7 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 8 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 9 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 10 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 11 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 12 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 13 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 14 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 15 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 16 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 17 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 18 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 19 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# Adding overlay 20 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# setting -destEndPointIpv4
destEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-destEndPointIpv4')
ixNet.add(destEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(destEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 2 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 3 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 4 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 5 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 6 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 7 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 8 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 9 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 10 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 11 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 12 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 13 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 14 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 15 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 16 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 17 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 18 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 19 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# Adding overlay 20 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# setting -symbolicPathName
symbolicPathNameMv = ixNet.getAttribute(pccInit2, '-symbolicPathName')
ixNet.add(symbolicPathNameMv, 'string')
ixNet.setMultiAttribute(symbolicPathNameMv + '/string',
            '-pattern', 'IXIA LSP {Inc:1,1}')
ixNet.commit()
# setting -includeAssociation
includeAssociationMv = ixNet.getAttribute(pccInit2, '-includeAssociation')
ixNet.add(includeAssociationMv, 'singleValue')
ixNet.setMultiAttribute(includeAssociationMv + '/singleValue',
            '-value', 'true')
# Adding overlay 1 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 5 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 6 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 7 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 8 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 9 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 10 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -standbyMode
standbyModeMv = ixNet.getAttribute(pccInit2, '-standbyMode')
ixNet.add(standbyModeMv, 'alternate')
# Adding overlay 1 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -protectionLsp
protectionLspMv = ixNet.getAttribute(pccInit2, '-protectionLsp')
ixNet.add(protectionLspMv, 'singleValue')
ixNet.setMultiAttribute(protectionLspMv + '/singleValue',
            '-value', 'false')
# Adding overlay 1 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 2 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 3 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 4 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 5 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 6 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 7 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 8 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 9 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 10 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# setting -associationId
associationIdMv = ixNet.getAttribute(pccInit2, '-associationId')
ixNet.add(associationIdMv, 'singleValue')
ixNet.setMultiAttribute(associationIdMv + '/singleValue',
            '-value', '1')
# Adding overlay 1 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 2 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 3 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 4 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 5 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 6 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 7 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 8 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 9 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 10 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 11 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

# Adding overlay 12 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

pccInit2 = pccGroup2+'/pceInitiateLspParameters:10'
# setting -numberOfEroSubObjects
ixNet.setAttribute(pccInit2, '-numberOfEroSubObjects', '1')
ixNet.commit()
# setting -srcEndPointIpv4
srcEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-srcEndPointIpv4')
ixNet.add(srcEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(srcEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 2 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 3 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 4 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 5 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 6 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 7 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 8 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 9 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 10 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 11 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 12 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 13 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 14 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 15 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 16 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 17 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 18 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 19 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# Adding overlay 20 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# setting -destEndPointIpv4
destEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-destEndPointIpv4')
ixNet.add(destEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(destEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 2 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 3 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 4 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 5 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 6 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 7 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 8 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 9 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 10 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 11 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 12 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 13 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 14 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 15 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 16 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 17 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 18 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 19 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# Adding overlay 20 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# setting -symbolicPathName
symbolicPathNameMv = ixNet.getAttribute(pccInit2, '-symbolicPathName')
ixNet.add(symbolicPathNameMv, 'string')
ixNet.setMultiAttribute(symbolicPathNameMv + '/string',
            '-pattern', 'IXIA LSP {Inc:1,1}')
ixNet.commit()
# setting -includeAssociation
includeAssociationMv = ixNet.getAttribute(pccInit2, '-includeAssociation')
ixNet.add(includeAssociationMv, 'singleValue')
ixNet.setMultiAttribute(includeAssociationMv + '/singleValue',
            '-value', 'true')
# Adding overlay 1 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 5 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 6 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 7 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 8 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 9 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 10 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -standbyMode
standbyModeMv = ixNet.getAttribute(pccInit2, '-standbyMode')
ixNet.add(standbyModeMv, 'alternate')
# Adding overlay 1 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -protectionLsp
protectionLspMv = ixNet.getAttribute(pccInit2, '-protectionLsp')
ixNet.add(protectionLspMv, 'singleValue')
ixNet.setMultiAttribute(protectionLspMv + '/singleValue',
            '-value', 'false')
# Adding overlay 1 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 2 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 3 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 4 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 5 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 6 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 7 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 8 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 9 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 10 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# setting -associationId
associationIdMv = ixNet.getAttribute(pccInit2, '-associationId')
ixNet.add(associationIdMv, 'singleValue')
ixNet.setMultiAttribute(associationIdMv + '/singleValue',
            '-value', '1')
# Adding overlay 1 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 2 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 3 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 4 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 5 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 6 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 7 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 8 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 9 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 10 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 11 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

# Adding overlay 12 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

pccInit2 = pccGroup2+'/pceInitiateLspParameters:10'
# setting -numberOfEroSubObjects
ixNet.setAttribute(pccInit2, '-numberOfEroSubObjects', '1')
ixNet.commit()
# setting -srcEndPointIpv4
srcEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-srcEndPointIpv4')
ixNet.add(srcEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(srcEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 2 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 3 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 4 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 5 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 6 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 7 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 8 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 9 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 10 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 11 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 12 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 13 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 14 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 15 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 16 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 17 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 18 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 19 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# Adding overlay 20 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# setting -destEndPointIpv4
destEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-destEndPointIpv4')
ixNet.add(destEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(destEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 2 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 3 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 4 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 5 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 6 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 7 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 8 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 9 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 10 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 11 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 12 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 13 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 14 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 15 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 16 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 17 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 18 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 19 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# Adding overlay 20 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# setting -symbolicPathName
symbolicPathNameMv = ixNet.getAttribute(pccInit2, '-symbolicPathName')
ixNet.add(symbolicPathNameMv, 'string')
ixNet.setMultiAttribute(symbolicPathNameMv + '/string',
            '-pattern', 'IXIA LSP {Inc:1,1}')
ixNet.commit()
# setting -includeAssociation
includeAssociationMv = ixNet.getAttribute(pccInit2, '-includeAssociation')
ixNet.add(includeAssociationMv, 'singleValue')
ixNet.setMultiAttribute(includeAssociationMv + '/singleValue',
            '-value', 'true')
# Adding overlay 1 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 5 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 6 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 7 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 8 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 9 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 10 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -standbyMode
standbyModeMv = ixNet.getAttribute(pccInit2, '-standbyMode')
ixNet.add(standbyModeMv, 'alternate')
# Adding overlay 1 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -protectionLsp
protectionLspMv = ixNet.getAttribute(pccInit2, '-protectionLsp')
ixNet.add(protectionLspMv, 'singleValue')
ixNet.setMultiAttribute(protectionLspMv + '/singleValue',
            '-value', 'false')
# Adding overlay 1 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 2 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 3 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 4 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 5 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 6 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 7 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 8 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 9 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 10 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# setting -associationId
associationIdMv = ixNet.getAttribute(pccInit2, '-associationId')
ixNet.add(associationIdMv, 'singleValue')
ixNet.setMultiAttribute(associationIdMv + '/singleValue',
            '-value', '1')
# Adding overlay 1 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 2 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 3 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 4 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 5 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 6 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 7 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 8 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 9 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 10 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 11 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

# Adding overlay 12 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

pccInit2 = pccGroup2+'/pceInitiateLspParameters:10'
# setting -numberOfEroSubObjects
ixNet.setAttribute(pccInit2, '-numberOfEroSubObjects', '1')
ixNet.commit()
# setting -srcEndPointIpv4
srcEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-srcEndPointIpv4')
ixNet.add(srcEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(srcEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 2 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 3 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 4 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 5 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 6 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 7 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 8 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 9 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 10 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 11 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 12 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 13 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 14 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 15 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 16 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 17 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 18 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 19 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# Adding overlay 20 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# setting -destEndPointIpv4
destEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-destEndPointIpv4')
ixNet.add(destEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(destEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 2 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 3 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 4 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 5 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 6 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 7 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 8 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 9 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 10 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 11 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 12 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 13 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 14 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 15 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 16 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 17 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 18 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 19 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# Adding overlay 20 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# setting -symbolicPathName
symbolicPathNameMv = ixNet.getAttribute(pccInit2, '-symbolicPathName')
ixNet.add(symbolicPathNameMv, 'string')
ixNet.setMultiAttribute(symbolicPathNameMv + '/string',
            '-pattern', 'IXIA LSP {Inc:1,1}')
ixNet.commit()
# setting -includeAssociation
includeAssociationMv = ixNet.getAttribute(pccInit2, '-includeAssociation')
ixNet.add(includeAssociationMv, 'singleValue')
ixNet.setMultiAttribute(includeAssociationMv + '/singleValue',
            '-value', 'true')
# Adding overlay 1 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 5 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 6 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 7 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 8 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 9 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 10 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -standbyMode
standbyModeMv = ixNet.getAttribute(pccInit2, '-standbyMode')
ixNet.add(standbyModeMv, 'alternate')
# Adding overlay 1 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -protectionLsp
protectionLspMv = ixNet.getAttribute(pccInit2, '-protectionLsp')
ixNet.add(protectionLspMv, 'singleValue')
ixNet.setMultiAttribute(protectionLspMv + '/singleValue',
            '-value', 'false')
# Adding overlay 1 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 2 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 3 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 4 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 5 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 6 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 7 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 8 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 9 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 10 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# setting -associationId
associationIdMv = ixNet.getAttribute(pccInit2, '-associationId')
ixNet.add(associationIdMv, 'singleValue')
ixNet.setMultiAttribute(associationIdMv + '/singleValue',
            '-value', '1')
# Adding overlay 1 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 2 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 3 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 4 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 5 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 6 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 7 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 8 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 9 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 10 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 11 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

# Adding overlay 12 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

pccInit2 = pccGroup2+'/pceInitiateLspParameters:10'
# setting -numberOfEroSubObjects
ixNet.setAttribute(pccInit2, '-numberOfEroSubObjects', '1')
ixNet.commit()
# setting -srcEndPointIpv4
srcEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-srcEndPointIpv4')
ixNet.add(srcEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(srcEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 2 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 3 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 4 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 5 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 6 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 7 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 8 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 9 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 10 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 11 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 12 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 13 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 14 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 15 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 16 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 17 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 18 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 19 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# Adding overlay 20 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

ixNet.commit()
# setting -destEndPointIpv4
destEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-destEndPointIpv4')
ixNet.add(destEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(destEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 2 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 3 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 4 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 5 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 6 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 7 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 8 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 9 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 10 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 11 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 12 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 13 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 14 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 15 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 16 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 17 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 18 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 19 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# Adding overlay 20 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# setting -symbolicPathName
symbolicPathNameMv = ixNet.getAttribute(pccInit2, '-symbolicPathName')
ixNet.add(symbolicPathNameMv, 'string')
ixNet.setMultiAttribute(symbolicPathNameMv + '/string',
            '-pattern', 'IXIA LSP {Inc:1,1}')
ixNet.commit()
# setting -includeAssociation
includeAssociationMv = ixNet.getAttribute(pccInit2, '-includeAssociation')
ixNet.add(includeAssociationMv, 'singleValue')
ixNet.setMultiAttribute(includeAssociationMv + '/singleValue',
            '-value', 'true')
# Adding overlay 1 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 5 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 6 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 7 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 8 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 9 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 10 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -standbyMode
standbyModeMv = ixNet.getAttribute(pccInit2, '-standbyMode')
ixNet.add(standbyModeMv, 'alternate')
# Adding overlay 1 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -protectionLsp
protectionLspMv = ixNet.getAttribute(pccInit2, '-protectionLsp')
ixNet.add(protectionLspMv, 'singleValue')
ixNet.setMultiAttribute(protectionLspMv + '/singleValue',
            '-value', 'false')
# Adding overlay 1 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 2 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 3 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 4 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 5 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 6 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 7 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 8 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 9 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 10 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# setting -associationId
associationIdMv = ixNet.getAttribute(pccInit2, '-associationId')
ixNet.add(associationIdMv, 'singleValue')
ixNet.setMultiAttribute(associationIdMv + '/singleValue',
            '-value', '1')
# Adding overlay 1 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 2 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 3 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 4 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 5 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 6 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 7 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 8 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 9 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 10 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 11 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

# Adding overlay 12 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

pccInit2 = pccGroup2+'/pceInitiateLspParameters:10'
# setting -numberOfEroSubObjects
ixNet.setAttribute(pccInit2, '-numberOfEroSubObjects', '1')
ixNet.commit()
# setting -srcEndPointIpv4
srcEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-srcEndPointIpv4')
ixNet.add(srcEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(srcEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 2 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 3 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 4 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 5 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 6 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 7 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 8 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 9 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 10 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 11 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 12 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 13 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 14 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 15 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 16 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 17 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 18 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 19 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# Adding overlay 20 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# setting -destEndPointIpv4
destEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-destEndPointIpv4')
ixNet.add(destEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(destEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 2 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 3 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 4 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 5 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 6 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 7 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 8 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 9 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 10 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 11 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 12 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 13 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 14 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 15 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 16 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 17 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 18 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 19 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# Adding overlay 20 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# setting -symbolicPathName
symbolicPathNameMv = ixNet.getAttribute(pccInit2, '-symbolicPathName')
ixNet.add(symbolicPathNameMv, 'string')
ixNet.setMultiAttribute(symbolicPathNameMv + '/string',
            '-pattern', 'IXIA LSP {Inc:1,1}')
ixNet.commit()
# setting -includeAssociation
includeAssociationMv = ixNet.getAttribute(pccInit2, '-includeAssociation')
ixNet.add(includeAssociationMv, 'singleValue')
ixNet.setMultiAttribute(includeAssociationMv + '/singleValue',
            '-value', 'true')
# Adding overlay 1 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 5 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 6 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 7 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 8 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 9 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 10 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -standbyMode
standbyModeMv = ixNet.getAttribute(pccInit2, '-standbyMode')
ixNet.add(standbyModeMv, 'alternate')
# Adding overlay 1 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -protectionLsp
protectionLspMv = ixNet.getAttribute(pccInit2, '-protectionLsp')
ixNet.add(protectionLspMv, 'singleValue')
ixNet.setMultiAttribute(protectionLspMv + '/singleValue',
            '-value', 'false')
# Adding overlay 1 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 2 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 3 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 4 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 5 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 6 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 7 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 8 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 9 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 10 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# setting -associationId
associationIdMv = ixNet.getAttribute(pccInit2, '-associationId')
ixNet.add(associationIdMv, 'singleValue')
ixNet.setMultiAttribute(associationIdMv + '/singleValue',
            '-value', '1')
# Adding overlay 1 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 2 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 3 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 4 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 5 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 6 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 7 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 8 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 9 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 10 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 11 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

# Adding overlay 12 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

pccInit2 = pccGroup2+'/pceInitiateLspParameters:10'
# setting -numberOfEroSubObjects
ixNet.setAttribute(pccInit2, '-numberOfEroSubObjects', '1')
ixNet.commit()
# setting -srcEndPointIpv4
srcEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-srcEndPointIpv4')
ixNet.add(srcEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(srcEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 2 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 3 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 4 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 5 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 6 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 7 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 8 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 9 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 10 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 11 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 12 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 13 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 14 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 15 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 16 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 17 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 18 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 19 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# Adding overlay 20 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# setting -destEndPointIpv4
destEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-destEndPointIpv4')
ixNet.add(destEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(destEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 2 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 3 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 4 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 5 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 6 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 7 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 8 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 9 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 10 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 11 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 12 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 13 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 14 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 15 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 16 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 17 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 18 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 19 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# Adding overlay 20 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# setting -symbolicPathName
symbolicPathNameMv = ixNet.getAttribute(pccInit2, '-symbolicPathName')
ixNet.add(symbolicPathNameMv, 'string')
ixNet.setMultiAttribute(symbolicPathNameMv + '/string',
            '-pattern', 'IXIA LSP {Inc:1,1}')
ixNet.commit()
# setting -includeAssociation
includeAssociationMv = ixNet.getAttribute(pccInit2, '-includeAssociation')
ixNet.add(includeAssociationMv, 'singleValue')
ixNet.setMultiAttribute(includeAssociationMv + '/singleValue',
            '-value', 'true')
# Adding overlay 1 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 5 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 6 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 7 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 8 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 9 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 10 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -standbyMode
standbyModeMv = ixNet.getAttribute(pccInit2, '-standbyMode')
ixNet.add(standbyModeMv, 'alternate')
# Adding overlay 1 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -protectionLsp
protectionLspMv = ixNet.getAttribute(pccInit2, '-protectionLsp')
ixNet.add(protectionLspMv, 'singleValue')
ixNet.setMultiAttribute(protectionLspMv + '/singleValue',
            '-value', 'false')
# Adding overlay 1 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 2 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 3 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 4 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 5 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 6 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 7 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 8 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 9 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 10 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# setting -associationId
associationIdMv = ixNet.getAttribute(pccInit2, '-associationId')
ixNet.add(associationIdMv, 'singleValue')
ixNet.setMultiAttribute(associationIdMv + '/singleValue',
            '-value', '1')
# Adding overlay 1 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 2 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 3 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 4 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 5 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 6 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 7 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 8 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 9 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 10 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 11 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

# Adding overlay 12 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

pccInit2 = pccGroup2+'/pceInitiateLspParameters:10'
# setting -numberOfEroSubObjects
ixNet.setAttribute(pccInit2, '-numberOfEroSubObjects', '1')
ixNet.commit()
# setting -srcEndPointIpv4
srcEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-srcEndPointIpv4')
ixNet.add(srcEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(srcEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 2 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '1.0.0.11',
                '-value',     '1.0.0.11')
ixNet.commit()

# Adding overlay 3 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 4 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '1.0.0.12',
                '-value',     '1.0.0.12')
ixNet.commit()

# Adding overlay 5 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 6 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '1.0.0.13',
                '-value',     '1.0.0.13')
ixNet.commit()

# Adding overlay 7 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 8 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '1.0.0.14',
                '-value',     '1.0.0.14')
ixNet.commit()

# Adding overlay 9 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 10 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '1.0.0.15',
                '-value',     '1.0.0.15')
ixNet.commit()

# Adding overlay 11 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 12 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '100.0.0.11',
                '-value',     '100.0.0.11')
ixNet.commit()

# Adding overlay 13 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 14 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '100.0.0.12',
                '-value',     '100.0.0.12')
ixNet.commit()

# Adding overlay 15 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 16 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '100.0.0.13',
                '-value',     '100.0.0.13')
ixNet.commit()

# Adding overlay 17 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 18 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '100.0.0.14',
                '-value',     '100.0.0.14')
ixNet.commit()

# Adding overlay 19 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# Adding overlay 20 for srcEndPointIpv4
ovrly = ixNet.add(srcEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '100.0.0.15',
                '-value',     '100.0.0.15')
ixNet.commit()

# setting -destEndPointIpv4
destEndPointIpv4Mv = ixNet.getAttribute(pccInit2, '-destEndPointIpv4')
ixNet.add(destEndPointIpv4Mv, 'singleValue')
ixNet.setMultiAttribute(destEndPointIpv4Mv + '/singleValue',
            '-value', '0.0.0.0')
# Adding overlay 1 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 2 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '2.0.0.11',
                '-value',     '2.0.0.11')
ixNet.commit()

# Adding overlay 3 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 4 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '2.0.0.12',
                '-value',     '2.0.0.12')
ixNet.commit()

# Adding overlay 5 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 6 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '2.0.0.13',
                '-value',     '2.0.0.13')
ixNet.commit()

# Adding overlay 7 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 8 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', '2.0.0.14',
                '-value',     '2.0.0.14')
ixNet.commit()

# Adding overlay 9 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 10 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', '2.0.0.15',
                '-value',     '2.0.0.15')
ixNet.commit()

# Adding overlay 11 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 12 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '101.0.0.11',
                '-value',     '101.0.0.11')
ixNet.commit()

# Adding overlay 13 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 14 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '101.0.0.12',
                '-value',     '101.0.0.12')
ixNet.commit()

# Adding overlay 15 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 16 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '101.0.0.13',
                '-value',     '101.0.0.13')
ixNet.commit()

# Adding overlay 17 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 18 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', '101.0.0.14',
                '-value',     '101.0.0.14')
ixNet.commit()

# Adding overlay 19 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# Adding overlay 20 for destEndPointIpv4
ovrly = ixNet.add(destEndPointIpv4Mv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', '101.0.0.15',
                '-value',     '101.0.0.15')
ixNet.commit()

# setting -symbolicPathName
symbolicPathNameMv = ixNet.getAttribute(pccInit2, '-symbolicPathName')
ixNet.add(symbolicPathNameMv, 'string')
ixNet.setMultiAttribute(symbolicPathNameMv + '/string',
            '-pattern', 'IXIA LSP {Inc:1,1}')
ixNet.commit()
# setting -includeAssociation
includeAssociationMv = ixNet.getAttribute(pccInit2, '-includeAssociation')
ixNet.add(includeAssociationMv, 'singleValue')
ixNet.setMultiAttribute(includeAssociationMv + '/singleValue',
            '-value', 'true')
# Adding overlay 1 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '7',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '8',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '9',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 5 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '10',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 6 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 7 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '17',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 8 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '18',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 9 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '19',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 10 for includeAssociation
ovrly = ixNet.add(includeAssociationMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '20',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -standbyMode
standbyModeMv = ixNet.getAttribute(pccInit2, '-standbyMode')
ixNet.add(standbyModeMv, 'alternate')
# Adding overlay 1 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 2 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 3 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# Adding overlay 4 for standbyMode
ovrly = ixNet.add(standbyModeMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'false',
                '-value',     'false')
ixNet.commit()

# setting -protectionLsp
protectionLspMv = ixNet.getAttribute(pccInit2, '-protectionLsp')
ixNet.add(protectionLspMv, 'singleValue')
ixNet.setMultiAttribute(protectionLspMv + '/singleValue',
            '-value', 'false')
# Adding overlay 1 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 2 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 3 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 4 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 5 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 6 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 7 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 8 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 9 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# Adding overlay 10 for protectionLsp
ovrly = ixNet.add(protectionLspMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', 'true',
                '-value',     'true')
ixNet.commit()

# setting -associationId
associationIdMv = ixNet.getAttribute(pccInit2, '-associationId')
ixNet.add(associationIdMv, 'singleValue')
ixNet.setMultiAttribute(associationIdMv + '/singleValue',
            '-value', '1')
# Adding overlay 1 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '1',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 2 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '2',
                '-indexStep', '0',
                '-valueStep', '11',
                '-value',     '11')
ixNet.commit()

# Adding overlay 3 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '3',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 4 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '4',
                '-indexStep', '0',
                '-valueStep', '12',
                '-value',     '12')
ixNet.commit()

# Adding overlay 5 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '5',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 6 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '6',
                '-indexStep', '0',
                '-valueStep', '13',
                '-value',     '13')
ixNet.commit()

# Adding overlay 7 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '11',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 8 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '12',
                '-indexStep', '0',
                '-valueStep', '111',
                '-value',     '111')
ixNet.commit()

# Adding overlay 9 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '13',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 10 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '14',
                '-indexStep', '0',
                '-valueStep', '112',
                '-value',     '112')
ixNet.commit()

# Adding overlay 11 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '15',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

# Adding overlay 12 for associationId
ovrly = ixNet.add(associationIdMv, 'overlay')
ixNet.setMultiAttribute(ovrly, 
                '-count',     '1',
                '-index',     '16',
                '-indexStep', '0',
                '-valueStep', '113',
                '-value',     '113')
ixNet.commit()

################################################################################
# Adding ERO parameterd
# Configured parameters :
#    -mplsLabel
#    -localIpv4Address
#    -remoteIpv4Address
#    -fBit
#    -sidType
################################################################################
pccEro2 = pccInit2+'/pcepEroSubObjectsList:1'
# setting -mplsLabel
mplsLabelMv = ixNet.getAttribute(pccEro2, '-mplsLabel')
ixNet.add(mplsLabelMv, 'singleValue')
ixNet.setMultiAttribute(mplsLabelMv + '/singleValue',
            '-value', '16')
ixNet.commit()
# setting -localIpv4Address
localIpv4AddressMv = ixNet.getAttribute(pccEro2, '-localIpv4Address')
ixNet.add(localIpv4AddressMv, 'singleValue')
ixNet.setMultiAttribute(localIpv4AddressMv + '/singleValue',
            '-value', '0.0.0.0')
ixNet.commit()
# setting -remoteIpv4Address
remoteIpv4AddressMv = ixNet.getAttribute(pccEro2, '-remoteIpv4Address')
ixNet.add(remoteIpv4AddressMv, 'singleValue')
ixNet.setMultiAttribute(remoteIpv4AddressMv + '/singleValue',
            '-value', '0.0.0.0')
ixNet.commit()
# setting -fBit
fBitMv = ixNet.getAttribute(pccEro2, '-fBit')
ixNet.add(fBitMv, 'singleValue')
ixNet.setMultiAttribute(fBitMv + '/singleValue',
            '-value', 'true')
ixNet.commit()
# setting -sidType
sidTypeMv = ixNet.getAttribute(pccEro2, '-sidType')
ixNet.add(sidTypeMv, 'singleValue')
ixNet.setMultiAttribute(sidTypeMv + '/singleValue',
            '-value', 'mplslabel20bit')
ixNet.commit()


################################################################################
# Assign ports
################################################################################
print("Assigning ports")
chassisIp = py.ports[0][0]
card1     = py.ports[0][1]
port1     = py.ports[0][2]
card2     = py.ports[1][1]
port2     = py.ports[1][2]

chassis = ixNet.add(root + '/availableHardware', 'chassis');
ixNet.setMultiAttribute(chassis, '-hostname', chassisIp);
ixNet.commit();

ixNet.setAttribute(vport1, '-connectedTo',
    '%s/card:%s/port:%s' % (chassis, card1, port1));
ixNet.commit();

ixNet.setAttribute(vport2, '-connectedTo',
    '%s/card:%s/port:%s' % (chassis, card2, port2));
ixNet.commit();

time.sleep(5);
print("Starting all protocols")
################################################################################
# Start all protocols
################################################################################
ixNet.execute('startAllProtocols')
print("Wait for 1 minute")
time.sleep(60)

################################################################################
# 2. Start PCEP protocol and wait for 45 seconds                               #
################################################################################
print("Starting protocols and waiting for 45 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(45)

################################################################################
# 3. Retrieve protocol statistics                                              #
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
# 4. Retrieve protocol learned info                                            #
################################################################################
totalNumberOfPcc = 1
i = 1
while (i <= totalNumberOfPcc) :
    ixNet.execute('getPccLearnedInfo', pcc1, "%d"%i)
    i = i + 1
# end while

print('-' * 60)
learnedInfoList = ixNet.getList(pcc1, 'learnedInfo')
for learnedInfo in learnedInfoList :
    table = ixNet.getList(learnedInfo, 'table')
    for t in table :
        colList = ixNet.getAttribute(t, '-columns')
        rowList = ixNet.getAttribute(t, '-values')
        for valList in rowList :
            ndx = 0  
            for val in valList :
                name  = colList[ndx]
                value = val
                print("%-30s:\t%s" % (name, value))
                ndx = ndx + 1
            # end for val in valList
            print('-' * 60)
        # end for valList in  $rowList
    # enf for t in table
# end for learnedInfo in learnedInfoList

################################################################################
# 14. Stop all protocols                                                       #
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
print ('!!! Test Script Ends !!!')
