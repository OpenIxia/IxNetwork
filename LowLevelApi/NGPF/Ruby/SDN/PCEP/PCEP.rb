# -*- coding: cp1252 -*-
################################################################################
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    19/02/2015 - Rudra Dutta - created sample                                 #
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
#    This script intends to demonstrate how to use NGPF PCEP API.              #
#      1. Configures a PCE on the topology1 and a PCC on topology2. The PCE    #
#         channel has one LSP with two ERO in it. The PCC has one "Expected    #
#         PCE initiated LSP" configured in it. The "Symbolic Path Name" of the #
#         LSP in the PCE channel is same as that of "Expected PCE initiated    #
#         LSP" in the PCC. Also source end of the PCE initiated LSP at the PCE #
#         end is matching with that of "Expected PCE Initiated LSP" at the     #
#         PCC end.                                                             #
#      2. Stats PCC and PCE.                                                   #
#      3. Verify statistics from "Protocols Summary" view                      #
#      4. Fetch PCC learned information                                        #
#      5. Configure L2/L3 traffic - source end is the topology2 (PCC) and      #
#         destinaton end is topology1                                          #
#      6. Apply and start L2/L3 traffic.                                       #
#      7. Verify L2/L3 traffic statistics.                                     #
#      8. Stop traffic.                                                        #
#      9. Change the MPLS Label value in ERO1 of LSP1 at the PCE end in        #
#         topology1.                                                           #
#     10. Wait for a few seconds and verify learned info                       #
#     11. Apply L2/L3 traffic.                                                 #
#     12. Verify traffic L2/L3 statistics.                                     #
#     13. Stop traiic.                                                         #
#     13. Stop all protocols.                                                  #
# Ixia Softwares:                                                              #
#    IxOS      8.00 EA                                                         #
#    IxNetwork 8.00 EA                                                         #
#                                                                              #
################################################################################
def assignPorts (ixNet, realPort1, realPort2)
    chassis1 = realPort1[0]
    chassis2 = realPort2[0]
    card1    = realPort1[1]
    card2    = realPort2[1]
    port1    = realPort1[2]
    port2    = realPort2[2]

    root = @ixNet.getRoot()
    vport1 = @ixNet.add(root, 'vport')
    @ixNet.commit()
    vport1 = @ixNet.remapIds(vport1)[0]

    vport2 = @ixNet.add(root, 'vport')
    @ixNet.commit()
    vport2 = @ixNet.remapIds(vport2)[0]

    chassisObj1 = @ixNet.add(root + '/availableHardware', 'chassis')
    @ixNet.setAttribute(chassisObj1, '-hostname', chassis1)
    @ixNet.commit()
    chassisObj1 = @ixNet.remapIds(chassisObj1)[0]

    if (chassis1 != chassis2) then
        chassisObj2 = @ixNet.add(root + '/availableHardware', 'chassis')
        @ixNet.setAttribute(chassisObj2, '-hostname', chassis2)
        @ixNet.commit()
        chassisObj2 = @ixNet.remapIds(chassisObj2)[0]
    else
        chassisObj2 = chassisObj1
    end

    cardPortRef1 = chassisObj1 + '/card:'+card1+'/port:'+port1
    @ixNet.setMultiAttribute(vport1, '-connectedTo', cardPortRef1,
    '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 001')
    @ixNet.commit()

    cardPortRef2 = chassisObj2 + '/card:'+card2+'/port:'+port2
    @ixNet.setMultiAttribute(vport2, '-connectedTo', cardPortRef2,
    '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 002')
    @ixNet.commit()
end

################################################################################
# Either feed the ixNetwork library path in the sys.path as below, or put the  #
# IxNetwork.py file somewhere else where we python can autoload it             #
# "IxNetwork.py" is available in <IxNetwork_installer_path>\API\Python         #
################################################################################
$:.unshift 'C:\samples\IxNetwork.rb'
require 'IxNetwork'

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information   #
# below                                                                         #
#################################################################################
ixTclServer = '10.200.115.203'
ixTclPort   = '8009'
ports       = [['10.200.115.151', '4', '1'], ['10.200.115.151', '4', '2']]

# get IxNet class
@ixNet = IxNetwork.new
puts("connecting to IxNetwork client")
@ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.00',
'-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
puts("cleaning up the old configfile, and creating an empty config")
@ixNet.execute('newConfig')

# assigning ports
assignPorts(@ixNet, ports[0], ports[1])
sleep(5)

root    = @ixNet.getRoot()
vportTx = @ixNet.getList(root, 'vport')[0]
vportRx = @ixNet.getList(root, 'vport')[1]

################################################################################
# 1. Configure the PCC and PCE as per the description given above.             #
################################################################################
puts("adding topologies")
@ixNet.add(root, 'topology', '-vports', vportTx)
@ixNet.add(root, 'topology', '-vports', vportRx)
@ixNet.commit()

topologies = @ixNet.getList(@ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

print "Adding 2 device groups"
@ixNet.add(topo1, 'deviceGroup')
@ixNet.add(topo2, 'deviceGroup')
@ixNet.commit()

t1devices = @ixNet.getList(topo1, 'deviceGroup')
t2devices = @ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices[0]
t2dev1 = t2devices[0]

puts("Configuring the multipliers (number of sessions)")
@ixNet.setAttribute(t1dev1, '-multiplier', '1')
@ixNet.setAttribute(t2dev1, '-multiplier', '1')
@ixNet.commit()

puts("Adding ethernet/mac endpoints")
@ixNet.add(t1dev1, 'ethernet')
@ixNet.add(t2dev1, 'ethernet')
@ixNet.commit()

mac1 = @ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = @ixNet.getList(t2dev1, 'ethernet')[0]

puts("Configuring the mac addresses %s" % (mac1))
@ixNet.setAttribute(@ixNet.getAttribute(mac1, '-mac') + '/singleValue',
'-value', '18:03:73:C7:6C:B1')
@ixNet.commit()

@ixNet.setAttribute(@ixNet.getAttribute(mac2, '-mac') + '/singleValue',
'-value', '18:03:73:C7:6C:01')
@ixNet.commit()

puts('@ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet\')')
puts(@ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet'))

puts("Add ipv4")
@ixNet.add(mac1, 'ipv4')
@ixNet.add(mac2, 'ipv4')
@ixNet.commit()

ip1 = @ixNet.getList(mac1, 'ipv4')[0]
ip2 = @ixNet.getList(mac2, 'ipv4')[0]

mvAdd1 = @ixNet.getAttribute(ip1, '-address')
mvAdd2 = @ixNet.getAttribute(ip2, '-address')
mvGw1  = @ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = @ixNet.getAttribute(ip2, '-gatewayIp')

puts("configuring ipv4 addresses")
@ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '20.20.20.2')
@ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '20.20.20.1')
@ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '20.20.20.1')
@ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '20.20.20.2')

@ixNet.setAttribute(@ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
@ixNet.setAttribute(@ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')

@ixNet.setMultiAttribute(@ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.setMultiAttribute(@ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.commit()

puts("Adding a PCC object on the Topology 2")
pce = @ixNet.add(ip1, 'pce')
@ixNet.commit()
pce = @ixNet.remapIds(pce)[0]

puts("Adding a PCC group on the top of PCE")
pccGroup = @ixNet.add(pce, 'pccGroup')
@ixNet.commit()
pccGroup = @ixNet.remapIds(pccGroup)[0]

# Adding PCC with expectedPceInitiatedLspPerPcc 1
puts("Adding a PCC object on the Topology 2")
pcc  = @ixNet.add(ip2, 'pcc')
@ixNet.setAttribute(pcc, '-expectedPceInitiatedLspPerPcc',  '1')
@ixNet.commit()
pcc = @ixNet.remapIds(pcc)[0]

# Set pcc group multiplier to 1
@ixNet.setAttribute(pccGroup, '-multiplier',  '1')
@ixNet.commit()

# Set PCC group's  "PCC IPv4 Address" field  to 20.20.20.1
pccIpv4AddressMv = @ixNet.getAttribute(pccGroup, '-pccIpv4Address')
@ixNet.setAttribute(pccIpv4AddressMv + '/singleValue', '-value',  '20.20.20.1')
@ixNet.commit()

################################################################################
# Set  pceInitiateLspParameters                                                #
# 1. IP version                -- ipv4                                         #
# 2. IPv4 source endpoint      -- 2.0.0.1                                      #
# 3. IPv4 destination endpoint -- 3.0.0.1                                      #
################################################################################
ipVerisionMv = @ixNet.getAttribute(pccGroup + '/pceInitiateLspParameters',
'-ipVersion')
@ixNet.setAttribute(ipVerisionMv + '/singleValue', '-value', 'ipv4')
@ixNet.commit()

ipv4SrcEndpointsMv = @ixNet.getAttribute(pccGroup + '/pceInitiateLspParameters',
'-srcEndPointIpv4')
@ixNet.setAttribute(ipv4SrcEndpointsMv + '/singleValue', '-value', '2.0.0.1')

ipv4DestEndpointsMv = @ixNet.getAttribute(pccGroup + '/pceInitiateLspParameters',
'-destEndPointIpv4')
@ixNet.setAttribute(ipv4DestEndpointsMv + '/singleValue', '-value', '3.0.0.1')
@ixNet.commit()

# Set  pceInitiateLspParameters
# 1. Include srp
ipv4SrpEndpointsMv = @ixNet.getAttribute(pccGroup + '/pceInitiateLspParameters',
'-includeSrp')
@ixNet.setAttribute(ipv4SrpEndpointsMv + '/singleValue',  '-value',  'True')
@ixNet.commit()

################################################################################
# Set  pceInitiateLspParameters                                                #
# a. Include srp                                                               #
# b. Include symbolic pathname TLV                                             #
# c. Symbolic path name                                                        #
################################################################################
includeLspMv = @ixNet.getAttribute(pccGroup + '/pceInitiateLspParameters',
'-includeLsp')
@ixNet.setAttribute(includeLspMv + '/singleValue', '-value', 'True')

includeSymbolicPathMv = @ixNet.getAttribute(pccGroup + '/pceInitiateLspParameters',
'-includeSymbolicPathNameTlv')
@ixNet.setAttribute(includeSymbolicPathMv + '/singleValue', '-value', 'True')

symbolicPathNameMv = @ixNet.getAttribute(pccGroup + '/pceInitiateLspParameters',
'-symbolicPathName')
@ixNet.setAttribute(symbolicPathNameMv + '/singleValue', '-value',
'IXIA_SAMPLE_LSP_1')
@ixNet.commit()

# Add 2 EROs
@ixNet.setMultiAttribute(pccGroup + '/pceInitiateLspParameters',
'-numberOfEroSubObjects', '2',
'-name', '{Initiated LSP Parameters}')
@ixNet.commit()

################################################################################
# Set the properties of ERO1                                                   #
# a. Active                                                                    #
# b. Sid Type                                                                  #
# c. MPLS Label                                                                #
# d. TC                                                                        #
# e. TTL                                                                       #
# f. NAI Type                                                                  #
################################################################################
ero1ActiveMv = @ixNet.getAttribute(
pccGroup + '/pceInitiateLspParameters/pcepEroSubObjectsList:1',
'-active')
@ixNet.setAttribute(ero1ActiveMv + '/singleValue', '-value', 'True')

ero1SidTypeMv = @ixNet.getAttribute(
pccGroup + '/pceInitiateLspParameters/pcepEroSubObjectsList:1',
'-sidType')
@ixNet.setAttribute(ero1SidTypeMv + '/singleValue', '-value',  'mplslabel32bit')

ero1MplsLabelMv = @ixNet.getAttribute(
pccGroup + '/pceInitiateLspParameters/pcepEroSubObjectsList:1',
'-mplsLabel')
@ixNet.setAttribute(ero1MplsLabelMv + '/singleValue', '-value', '1111')

ero1TcMv = @ixNet.getAttribute(
pccGroup + '/pceInitiateLspParameters/pcepEroSubObjectsList:1',
'-tc')

@ixNet.setAttribute(ero1TcMv + '/singleValue', '-value',  '1')

ero1TtlMv = @ixNet.getAttribute(
pccGroup + '/pceInitiateLspParameters/pcepEroSubObjectsList:1',
'-ttl')
@ixNet.setAttribute(ero1TtlMv + '/singleValue', '-value', '125')

ero1NaiTypeMv = @ixNet.getAttribute(
pccGroup + '/pceInitiateLspParameters/pcepEroSubObjectsList:1',
'-naiType')
@ixNet.setAttribute(ero1NaiTypeMv + '/singleValue', '-value', 'notapplicable')
@ixNet.commit()

################################################################################
# Set the properties of ERO1                                                   #
# a. Active                                                                    #
# b. Sid Type                                                                  #
# c. MPLS Label                                                                #
# d. TC                                                                        #
# e. TTL                                                                       #
# f. NAI Type                                                                  #
################################################################################
ero2ActiveMv = @ixNet.getAttribute(
pccGroup + '/pceInitiateLspParameters/pcepEroSubObjectsList:2',
'-active')
@ixNet.setAttribute(ero2ActiveMv + '/singleValue', '-value', 'True')

ero2SidTypeMv = @ixNet.getAttribute(
pccGroup + '/pceInitiateLspParameters/pcepEroSubObjectsList:2',
'-sidType')
@ixNet.setAttribute(ero2SidTypeMv + '/singleValue', '-value', 'mplslabel32bit')

ero2MplsLabelMv = @ixNet.getAttribute(
pccGroup + '/pceInitiateLspParameters/pcepEroSubObjectsList:2',
'-mplsLabel')
@ixNet.setAttribute(ero2MplsLabelMv + '/singleValue', '-value', '5555')

ero2TcMv = @ixNet.getAttribute(
pccGroup + '/pceInitiateLspParameters/pcepEroSubObjectsList:2',
'-tc')
@ixNet.setAttribute(ero2TcMv + '/singleValue', '-value', '0')

ero2TtlMv = @ixNet.getAttribute(
pccGroup + '/pceInitiateLspParameters/pcepEroSubObjectsList:2',
'-ttl')
@ixNet.setAttribute(ero2TtlMv + '/singleValue', '-value', '100')

ero2NaiTypeMv = @ixNet.getAttribute(
pccGroup + '/pceInitiateLspParameters/pcepEroSubObjectsList:2',
'-naiType')
@ixNet.setAttribute(ero2NaiTypeMv + '/singleValue', '-value', 'notapplicable')
@ixNet.commit()

# Set PCC's  "PCE IPv4 Address" field  to 20.20.20.20
pceIpv4AddressMv = @ixNet.getAttribute(pcc, '-pceIpv4Address')
@ixNet.setAttribute(pceIpv4AddressMv + '/singleValue', '-value', '20.20.20.2')
@ixNet.commit()

# Add one expectedInitiatedLspList
@ixNet.setMultiAttribute(pcc + '/expectedInitiatedLspList',
'-maxExpectedSegmentCount',  '1',
'-name', '{Expected PCE Initiated LSP 1}')
@ixNet.commit()
################################################################################
# Add expected PCC's Expected Initiated LSP traffic end point                  #
# a. Active                                                                    #
# b. Source IP addresses                                                       #
# c. Symbolic path name                                                        #
################################################################################
pccExpectedLspActiveMv = @ixNet.getAttribute(pcc + '/expectedInitiatedLspList',
'-active')
@ixNet.setAttribute(pccExpectedLspActiveMv + '/singleValue', '-value', 'True')
@ixNet.commit()

pccExpectedSrcIpAddrMv = @ixNet.getAttribute(pcc + '/expectedInitiatedLspList',
'-sourceIpv4Address')
@ixNet.setAttribute(pccExpectedSrcIpAddrMv + '/singleValue', '-value',  '2.0.0.1')
@ixNet.commit()

pccExpectedSymbolicPathMv = @ixNet.getAttribute(pcc + '/expectedInitiatedLspList',
'-symbolicPathName')
@ixNet.setAttribute(pccExpectedSymbolicPathMv + '/singleValue', '-value',
'{IXIA_SAMPLE_LSP_1}')
@ixNet.commit()

################################################################################
# 2. Start PCEP protocol and wait for 45 seconds                               #
################################################################################
puts("Starting protocols and waiting for 45 seconds for protocols to come up")
@ixNet.execute('startAllProtocols')
sleep(45)

################################################################################
# 3. Retrieve protocol statistics                                              #
################################################################################
puts("Fetching all Protocol Summary Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap   = @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList
        puts("***************************************************")
        index = 0
        for satIndv in statVal
            puts(statcap[index]+" "+satIndv)
            index = index + 1
        end
    end
end
puts("***************************************************")

################################################################################
# 4. Retrieve protocol learned info                                            #
################################################################################
totalNumberOfPcc = 1
i = 1
while (i <= totalNumberOfPcc) do
    @ixNet.execute('getPccLearnedInfo', pcc, "%d"%i)
    i = i + 1
end

puts('-' * 60)
learnedInfoList = @ixNet.getList(pcc, 'learnedInfo')
for learnedInfo in learnedInfoList
    table = @ixNet.getList(learnedInfo, 'table')
    for t in table
        colList = @ixNet.getAttribute(t, '-columns')
        rowList = @ixNet.getAttribute(t, '-values')
        for valList in rowList
            ndx = 0
            for val in valList
                name  = colList[ndx]
                value = val
                puts(name+" "+value)
                ndx = ndx + 1
            end
            puts('-' * 60)
            # end for valList in  $rowList
        end
    end
end

################################################################################
# 5. Configure L2-L3 traffic                                                   #
################################################################################
puts("Configuring L2-L3 Traffic Item")
@ixNet.setAttribute(@ixNet.getRoot() + '/traffic',
'-refreshLearnedInfoBeforeApply', 'true')
@ixNet.commit()

trafficItem1=@ixNet.add(@ixNet.getRoot() + '/traffic',
'trafficItem')
@ixNet.setMultiAttribute(trafficItem1,
'-name',                     '{Traffic Item 1}',
'-roundRobinPacketOrdering', 'false',
'-trafficType',              'ipv4')
@ixNet.commit()

trafficItem1 = @ixNet.remapIds(trafficItem1)[0]
endpointSet1 = @ixNet.add(trafficItem1, 'endpointSet')
source       = [pcc + '/expectedInitiatedLspList']
destination  = [topo1]

@ixNet.setMultiAttribute(endpointSet1,
'-name',         'EndpointSet-1',
'-sources',      source,
'-destinations', destination)
@ixNet.commit()

@ixNet.setMultiAttribute(trafficItem1 + '/transmissionDistribution',
'-distributions', ['mplsMplsLabelValue0'])

@ixNet.setMultiAttribute(trafficItem1 + '/tracking',
'-trackBy',        ['trackingenabled0', 'mplsMplsLabelValue0'],
'-fieldWidth',     'thirtyTwoBits',
'-protocolOffset', 'Root.0',
'-values',         '')
@ixNet.commit()
################################################################################
# 6. Apply and start L2/L3 traffic                                             #
################################################################################
puts('applying L2/L3 traffic')
@ixNet.execute('apply', @ixNet.getRoot() + '/traffic')
sleep(5)

puts('starting L2/L3 traffic')
@ixNet.execute('start', @ixNet.getRoot() + '/traffic')

puts('let the traffic run for 1 minute');
sleep(60)

################################################################################
# 7. Retrieve L2/L3 traffic item statistics                                    #
################################################################################
puts('Verifying all the L2-L3 traffic stats')
viewPage = '::ixNet::OBJ-/statistics/view:"Flow Statistics"/page'
statcap =  @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList
        puts("***************************************************")
        index = 0
        for satIndv in statVal
            puts(statcap[index]+" "+satIndv)
            index = index + 1
        end
    end
end

puts("***************************************************")

################################################################################
# 8. Stop L2/L3 traffic                                                        #
################################################################################
puts('Stopping L2/L3 traffic')
@ixNet.execute('stop', @ixNet.getRoot() + '/traffic')
sleep(5)

################################################################################
# 9. Change MPLS label valie in the ERO1 of LSP1                               #
################################################################################
@ixNet.setAttribute(ero1MplsLabelMv + '/singleValue', '-value', '6666')
@ixNet.commit()
@ixNet.execute('applyOnTheFly', '/globals/topology')
sleep(5)

################################################################################
# 10. Retrieve protocol learned info                                           #
################################################################################
totalNumberOfPcc = 1
i = 1
while (i <= totalNumberOfPcc) do
    @ixNet.execute('getPccLearnedInfo', pcc, "%d"%i)
    i = i + 1
end

puts('-' * 60)
learnedInfoList = @ixNet.getList(pcc, 'learnedInfo')
for learnedInfo in learnedInfoList
    table = @ixNet.getList(learnedInfo, 'table')
    for t in table
        colList = @ixNet.getAttribute(t, '-columns')
        rowList = @ixNet.getAttribute(t, '-values')
        for valList in rowList
            ndx = 0
            for val in valList
                name  = colList[ndx]
                value = val
                puts(name+" "+value)
                ndx = ndx + 1
            end
            puts('-' * 60)
        end
    end
end

################################################################################
# 11. Apply and start L2/L3 traffic                                            #
################################################################################
puts('applying L2/L3 traffic')
@ixNet.execute('apply', @ixNet.getRoot() + '/traffic')
sleep(5)

puts('starting L2/L3 traffic')
@ixNet.execute('start', @ixNet.getRoot() + '/traffic')

puts('let the traffic run for 1 minute');
sleep(60)

################################################################################
# 12. Retrieve L2/L3 traffic item statistics                                   #
################################################################################
puts('Verifying all the L2-L3 traffic stats')
viewPage = '::ixNet::OBJ-/statistics/view:"Flow Statistics"/page'
statcap =  @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList
        puts("***************************************************")
        index = 0
        for satIndv in statVal
            puts(statcap[index]+" "+satIndv)
            index = index + 1
        end
    end
end
puts("***************************************************")

################################################################################
# 13. Stop L2/L3 traffic                                                       #
################################################################################
puts('Stopping L2/L3 traffic')
@ixNet.execute('stop', @ixNet.getRoot() + '/traffic')
sleep(5)

################################################################################
# 14. Stop all protocols                                                       #
################################################################################
puts('Stopping protocols')
@ixNet.execute('stopAllProtocols')
puts('!!! Test Script Ends !!!')

