#!/usr/bin/ruby
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2014 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/10/2014 - Alka pattnaik - created sample                               #
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

######################################################################################
#                                                                                    #
# Description:                                                                       #
#    This script intends to demonstrate how to use NGPF LDP API.                     #
#                                                                                    #
# About Topology:                                                                     #
#          Within toplogy both Provider Edge(PE) and Provider(P) Routers are created.#
# created.P router is emulated in the front Device Group(DG), which consists of both #
# OSPF as routing protocol as well as Basic LDP sessions for Transport Label         #
# Distribution Protocol. The chained DG act as PE Router, where LDP Extended Martini #
# is configured for VPN Label distibution protocol.Bidirectional L2-L3 Traffic is    #
# configured in between two CE cloud is created.                                     #
#     Script Flow:                                                                     #
#     1. Configuration of protocols.                                                     #
#    Configuration flow of the script is as follow:                                  #
#         i.    Adding of OSPF router.                                                 #
#         ii.   Adding of Network Cloud.                                               #
#         iii.  Adding of chain DG.                                                     #
#         iv.   Adding of LDP(basic session) on Front DG                                  #
#         v.    Adding of LDP Extended Martini(Targeted sess.) over chained DG.        #
#         vi.   Adding of LDP PW/VPLS Tunnel over LDP Extended Martini.                 #
#    2. Start the ldp protocol.                                                      #
#    3. Retrieve protocol statistics.                                                  #
#    4. Retrieve protocol learned info.                                              #
#    5. Disbale/Enable the ldp FECs and change label & apply change on the fly       #
#    6. Retrieve protocol learned info again and notice the difference with          #
#       previouly retrieved learned info.                                            #
#    7. Configure L2-L3 traffic.                                                     #
#    8. Start the L2-L3 traffic.                                                     #
#    9. Retrieve L2-L3 traffic stats.                                                #
#   10. Stop L2-L3 traffic.                                                          #
#   11. Stop all protocols.                                                          #
# Ixia Software:                                                                     #
#    IxOS      6.80 EB (6.80.1101.116)                                               #
#    IxNetwork 7.40 EB (7.40.929.3)                                                  #
#                                                                                    #
######################################################################################





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
# Either feed the ixNetwork library path in the sys.path as below, or put the
# IxNetwork.rb file somewhere else where we ruby can autoload it.
# "IxNetwork.rb" is available in <IxNetwork_installer_path>\API\Ruby
################################################################################
$:.unshift 'C:\samples\IxNetwork.rb'
require 'IxNetwork'

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixApiServer = '10.200.115.203'
ixApiPort   = '8009'
ports       = [['10.200.115.151', '4', '1'], ['10.200.115.151', '4', '2']]

# get IxNet class
@ixNet = IxNetwork.new
puts("connecting to IxNetwork client")
@ixNet.connect(ixApiServer, '-port', ixApiPort, '-version', '7.40',
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

puts("adding topologies")
@ixNet.add(root, 'topology', '-vports', vportTx)
@ixNet.add(root, 'topology', '-vports', vportRx)
@ixNet.commit()

topologies = @ixNet.getList(@ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

puts "Renaming the topologies and the device groups"
@ixNet.setAttribute(topo1, '-name', 'Topology for FEC128 1')
@ixNet.setAttribute(topo2, '-name', 'Topology for FEC128 2')

puts "Adding 2 device groups"
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
@ixNet.setMultiAttribute(@ixNet.getAttribute(mac1, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '18:03:73:C7:6C:B1',
    '-step',      '00:00:00:00:00:01')

@ixNet.setAttribute(@ixNet.getAttribute(mac2, '-mac') + '/singleValue',
    '-value', '18:03:73:C7:6C:01')
@ixNet.commit()
#puts("@ixNet.help ::ixNet::OBJ-/topology/deviceGroup/ethernet")
#puts(@ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet'))

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

#puts("@ixNet.help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4")
#puts(@ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4'))


puts("Adding ldp over IP4 stacks")
@ixNet.add(ip1, 'ldpBasicRouter')
@ixNet.add(ip2, 'ldpBasicRouter')
@ixNet.commit()

ldp1 = @ixNet.getList(ip1, 'ldpBasicRouter')[0]
ldp2 = @ixNet.getList(ip2, 'ldpBasicRouter')[0]

puts("Renaming the topologies and the device groups")
@ixNet.setAttribute(t1dev1, '-name', 'Provider Router 1')
@ixNet.setAttribute(t2dev1, '-name', 'Provider Router 2')
@ixNet.commit()
#puts("@ixNet.help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp")
#puts(@ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp'))

puts("Adding OSPFv2 over IP4 stack")
@ixNet.add(ip1, 'ospfv2')
@ixNet.add(ip2, 'ospfv2')
@ixNet.commit()
ospf1 = @ixNet.getList(ip1, 'ospfv2')[0]
ospf2 = @ixNet.getList(ip2, 'ospfv2')[0]
puts("Making the NetworkType to Point to Point in the first OSPF router")
networkTypeMultiValue1 = @ixNet.getAttribute(ospf1, '-networkType')
@ixNet.setMultiAttribute(networkTypeMultiValue1, '-clearOverlays', 'false', '-pattern', 'singleValue')
@ixNet.commit()
networkType1 = @ixNet.add(networkTypeMultiValue1, 'singleValue') 
@ixNet.setMultiAttribute(networkType1, '-value', 'pointtopoint')
@ixNet.commit()

puts("Making the NetworkType to Point to Point in the second OSPF router")
networkTypeMultiValue2 = @ixNet.getAttribute(ospf2, '-networkType')
@ixNet.setMultiAttribute(networkTypeMultiValue2, '-clearOverlays', 'false', '-pattern', 'singleValue')
@ixNet.commit()
networkType2 =@ixNet.add(networkTypeMultiValue2, 'singleValue') 
@ixNet.setMultiAttribute(networkType2, '-value', 'pointtopoint')
@ixNet.commit()

# **********************************************************************************
puts("Adding NetworkGroup behind ldp DG")
@ixNet.execute('createDefaultStack', t1devices, 'ipv4PrefixPools')
@ixNet.execute('createDefaultStack', t2devices, 'ipv4PrefixPools')

networkGroup1 = @ixNet.getList(t1dev1, 'networkGroup')[0]
networkGroup2 = @ixNet.getList(t2dev1, 'networkGroup')[0]

@ixNet.setAttribute(networkGroup1, '-name', 'LDP_1_Network_Group1')
@ixNet.setAttribute(networkGroup2, '-name', 'LDP_2_Network_Group1')
@ixNet.setAttribute(networkGroup1, '-multiplier', '10')
@ixNet.setAttribute(networkGroup2, '-multiplier', '10')
@ixNet.commit()


#Change IP address and Prefix Of Network Group 
ipV4PrefixPools1  = @ixNet.getList(networkGroup1, 'ipv4PrefixPools')[0]
prefixLength1 = @ixNet.getAttribute(ipV4PrefixPools1, '-prefixLength')
@ixNet.setMultiAttribute(prefixLength1, '-clearOverlays', 'false', '-pattern', 'singleValue')
@ixNet.commit()
ipV4PrefixPools2  = @ixNet.getList(networkGroup2, 'ipv4PrefixPools')[0]
prefixLength2 = @ixNet.getAttribute(ipV4PrefixPools2, '-prefixLength')
@ixNet.setMultiAttribute(prefixLength2,  '-clearOverlays', 'false', '-pattern', 'singleValue')
@ixNet.commit()

prefix1 = @ixNet.add(prefixLength1, 'singleValue')
@ixNet.setMultiAttribute(prefix1, '-value', '32')
@ixNet.commit()
prefix2 = @ixNet.add(prefixLength2, 'singleValue')
@ixNet.setMultiAttribute(prefix2, '-value', '32')
@ixNet.commit()
addressSet1 = @ixNet.getAttribute(ipV4PrefixPools1, '-networkAddress')
@ixNet.setMultiAttribute(addressSet1, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()
addressSet2 = @ixNet.getAttribute(ipV4PrefixPools2, '-networkAddress')
@ixNet.setMultiAttribute(addressSet2, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()
puts("changing Ip and Prefix Of Network group")
addressSet1 = @ixNet.add(addressSet1, 'counter')
@ixNet.setMultiAttribute(addressSet1, '-step', '0.0.0.1', '-start', '200.1.0.1', '-direction', 'increment')
@ixNet.commit()
addressSet2 = @ixNet.add(addressSet2, 'counter')
@ixNet.setMultiAttribute(addressSet2, '-step', '0.0.0.1', '-start', '201.1.0.1', '-direction', 'increment')    
@ixNet.commit()
# Add ipv4 loopback1 for PE Router

puts("Adding ipv4 loopback1 for for configuring PE Routers above it")

chainedDg1 = @ixNet.add(networkGroup1, 'deviceGroup')
@ixNet.setMultiAttribute(chainedDg1, '-multiplier', '1', '-name', 'Device Group 3')
@ixNet.commit()
chainedDg1 = @ixNet.remapIds(chainedDg1)[0]

loopback1 = @ixNet.add(chainedDg1, 'ipv4Loopback')
@ixNet.setMultiAttribute(loopback1, '-stackedLayers', [], '-name', 'IPv4 Loopback 1')
@ixNet.commit()

connector1 = @ixNet.add(loopback1, 'connector')
@ixNet.setMultiAttribute(connector1, '-connectedTo', networkGroup1 + '/ipv4PrefixPools:1')
@ixNet.commit()
connector1 = @ixNet.remapIds(connector1)[0]

addressSet3 = @ixNet.getAttribute(loopback1, '-address')
@ixNet.setMultiAttribute(addressSet3, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()

addressSet3 = @ixNet.add(addressSet3, 'counter')
@ixNet.setMultiAttribute(addressSet3, '-step', '0.0.0.1', '-start', '200.1.0.1', '-direction', 'increment')
@ixNet.commit()
addressSet3 = @ixNet.remapIds(addressSet3)[0]

# Add ipv4 loopback2 for PE Router
puts("Adding ipv4 loopback2 for for configuring PE Routers above it")
chainedDg2 = @ixNet.add(networkGroup2, 'deviceGroup')
@ixNet.setMultiAttribute(chainedDg2, '-multiplier', '1', '-name', 'Device Group 4')
@ixNet.commit()
chainedDg2 = @ixNet.remapIds(chainedDg2)[0]

loopback2 = @ixNet.add(chainedDg2, 'ipv4Loopback')
@ixNet.setMultiAttribute(loopback2, '-stackedLayers', [], '-name', 'IPv4 Loopback 2')
@ixNet.commit()

connector2 = @ixNet.add(loopback2, 'connector')
@ixNet.setMultiAttribute(connector2, '-connectedTo', networkGroup2 + '/ipv4PrefixPools:1')
@ixNet.commit()
connector1 = @ixNet.remapIds(connector2)[0]

addressSet4 = @ixNet.getAttribute(loopback2, '-address')
@ixNet.setMultiAttribute(addressSet4, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()

addressSet4 = @ixNet.add(addressSet4, 'counter')
@ixNet.setMultiAttribute(addressSet4, '-step', '0.0.0.1', '-start', '201.1.0.1', '-direction', 'increment')
@ixNet.commit()
addressSet2 = @ixNet.remapIds(addressSet4)[0]
################################################################################
# 2. Add LDP targeted(Extended Martini) Router
################################################################################

@ixNet.add(loopback1, 'ldpTargetedRouter')
@ixNet.add(loopback2, 'ldpTargetedRouter')
@ixNet.commit()

ldpTargeted1 = @ixNet.getList(loopback1, 'ldpTargetedRouter')[0]
ldpTargeted2 = @ixNet.getList(loopback2, 'ldpTargetedRouter')[0]

ldpTargetedPeer1 = @ixNet.getList(ldpTargeted1, 'ldpTargetedPeer')[0]
ldpTargetedPeer2 = @ixNet.getList(ldpTargeted2, 'ldpTargetedPeer')[0]
#ptint ("@ixNet.help ::ixNet::OBJ-/topology:1/deviceGroup:1/networkGroup:4/deviceGroup:1/ipv4Loopback:1/ldpTargetedRouter:1/ldpTargetedPeer")
#puts(@ixNet.help('::ixNet::OBJ-/topology:2/deviceGroup:2/networkGroup:2/deviceGroup:1/ipv4Loopback:1/ldpTargetedRouter:1/ldpTargetedPeer'))

addressSet5 = @ixNet.getAttribute(ldpTargetedPeer1, '-iPAddress')
@ixNet.setMultiAttribute(addressSet5, '-clearOverlays', 'false',
    '-pattern', 'counter')
@ixNet.commit()
addressSet5 = @ixNet.add(addressSet5, 'counter')
@ixNet.setMultiAttribute(addressSet5, '-step', '0.0.0.1',
    '-start', '201.1.0.1',
    '-direction', 'increment')
@ixNet.commit()

addressSet6 = @ixNet.getAttribute(ldpTargetedPeer2, '-iPAddress')
@ixNet.setMultiAttribute(addressSet6, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()
addressSet6 = @ixNet.add(addressSet6, 'counter')
@ixNet.setMultiAttribute(addressSet6, '-step', '0.0.0.1',
    '-start', '200.1.0.1',
    '-direction', 'increment')
@ixNet.commit()

#Add LDP FEC129 on top of LDP targeted Router

ldppwvpls1 = @ixNet.add(ldpTargeted1, 'ldppwvpls')
ldppwvpls2 = @ixNet.add(ldpTargeted2, 'ldppwvpls')
@ixNet.commit()
#puts("ixNet help ::ixNet::OBJ-/topology:1/deviceGroup:1/networkGroup:1/deviceGroup:1/ipv4Loopback:1/ldpTargetedRouter:1/ldppwvpls:1")
#puts(@ixNet.help(::ixNet::OBJ-/topology:1/deviceGroup:1/networkGroup:1/deviceGroup:1/ipv4Loopback:1/ldpTargetedRouter:1/ldppwvpls:1))

ldppwvpls1 = @ixNet.remapIds(ldppwvpls1)[0]
ldppwvpls2 = @ixNet.remapIds(ldppwvpls2)[0]

peerId1 = @ixNet.getAttribute(ldppwvpls1, '-peerId')
@ixNet.setMultiAttribute(peerId1, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()

peerId1 = @ixNet.add(peerId1, 'counter')
@ixNet.setMultiAttribute(peerId1, '-step', '0.0.0.1',
    '-start', '201.1.0.1', '-direction', 'increment')
@ixNet.commit()
 
peerId2 = @ixNet.getAttribute(ldppwvpls2, '-peerId')
@ixNet.setMultiAttribute(peerId2, '-clearOverlays', 'false',
    '-pattern', 'counter')
@ixNet.commit()

peerId2 = @ixNet.add(peerId2, 'counter')
@ixNet.setMultiAttribute(peerId2, '-step', '0.0.0.1',
    '-start', '200.1.0.1', '-direction', 'increment')
@ixNet.commit()
 
################################################################################
# 3. Add MAC Cloud behind LDP PWs
################################################################################
@ixNet.execute('createDefaultStack', chainedDg1, 'macPools')
@ixNet.execute('createDefaultStack', chainedDg2, 'macPools')
@ixNet.commit()

macPools1 = @ixNet.getList(chainedDg1, 'networkGroup')[0]
macPools2 = @ixNet.getList(chainedDg2, 'networkGroup')[0]
puts("Renaming MAC Cloud")
@ixNet.setAttribute(macPools1, '-name', 'CE MAC Cloud 1')
@ixNet.setAttribute(macPools2, '-name', 'CE MAC Cloud 1')
@ixNet.commit()
################################################################################
# 4. Start ldp protocol and wait for 60 seconds
################################################################################
puts("Starting protocols and waiting for 60 seconds for protocols to come up")
@ixNet.execute('startAllProtocols')
sleep(60)

################################################################################
# 5. Retrieve protocol statistics.
################################################################################
puts("Fetching all Protocol Summary Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap   = @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues')
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

###############################################################################
# 6. Retrieve protocol learned info
###############################################################################
puts("Fetching ldp Basic Learned Info")
@ixNet.execute('getIPv4FECLearnedInfo', ldp1, '1')
sleep(5)
linfo1  = @ixNet.getList(ldp1, 'learnedInfo')[0]
@ixNet.getAttribute(linfo1, '-columns')
values1 = @ixNet.getAttribute(linfo1, '-values')

puts("***************************************************")
for v in values1
    puts(v)
end
puts("***************************************************")

puts("Fetching FEC 128 Learned Info")
@ixNet.execute('getFEC128LearnedInfo', ldpTargeted2, '1')
sleep(5)
linfo2  = @ixNet.getList(ldpTargeted2, 'learnedInfo')[0]
@ixNet.getAttribute(linfo2, '-columns')
values2 = @ixNet.getAttribute(linfo2, '-values')

puts("***************************************************")
for v in values2
    puts(v)
end
puts("***************************************************")

################################################################################
# 7.Change the labels of FEC element And apply changes On The Fly (OTF).
################################################################################
puts(" Changing FEC labels on the fly ")
feclabel1 = @ixNet.getAttribute(ldppwvpls1, '-label')
@ixNet.setMultiAttribute(feclabel1, '-clearOverlays', 'false', '-pattern', 'counter')
@ixNet.commit()

feclabel1 = @ixNet.add(feclabel1, 'counter')
@ixNet.setMultiAttribute(feclabel1, '-step', '100', '-start', '5001', '-direction', 'increment')
@ixNet.commit()

globalObj = @ixNet.getRoot() + '/globals'
topology = globalObj + '/topology'
puts("Applying changes on the fly")
begin
    @ixNet.execute('applyOnTheFly', topology)
rescue
    puts("error in applying on the fly change")
end
sleep(15)


###############################################################################
# 8. Retrieve protocol learned info again and compare with
#    previously retrieved learned info.
###############################################################################
puts("Fetching FEC 128 Learned Info 2nd time")
@ixNet.execute('getFEC128LearnedInfo', ldpTargeted2, '1')
linfo2 = @ixNet.getList(ldpTargeted2, 'learnedInfo')[0]
@ixNet.getAttribute(linfo2, '-columns')
values = @ixNet.getAttribute(linfo2, '-values')
puts("***************************************************")
for v in values
    puts(v)
end
puts("***************************************************")

################################################################################
# 9. Configure L2-L3 traffic
################################################################################
puts("Configuring L2-L3 Traffic Item")
trafficItem1 = @ixNet.add(@ixNet.getRoot() + '/traffic', 'trafficItem')
@ixNet.setMultiAttribute(trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ethernetVlan')
@ixNet.commit()

trafficItem1 = @ixNet.remapIds(trafficItem1)[0]
endpointSet1 = @ixNet.add(trafficItem1, 'endpointSet')
source       = networkGroup1
destination  = networkGroup2

@ixNet.setMultiAttribute(endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', [],
    '-scalableSources',       [],
    '-multicastReceivers',    [],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               source,
    '-destinations',          destination)
@ixNet.commit()

@ixNet.setMultiAttribute(trafficItem1 + '/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         [])
@ixNet.commit()

###############################################################################
# 10. Apply and start L2/L3 traffic
###############################################################################
puts('applying L2/L3 traffic')
@ixNet.execute('apply', @ixNet.getRoot() + '/traffic')
sleep(5)

puts('starting L2/L3 traffic')
@ixNet.execute('start', @ixNet.getRoot() + '/traffic')


puts('Let traffic run for 1 minute')
sleep(60)

###############################################################################
# 11. Retrieve L2/L3 traffic item statistics
###############################################################################
puts('Verifying all the L2-L3 traffic stats')
viewPage = '::ixNet::OBJ-/statistics/view:"Flow Statistics"/page'
statcap =  @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues')
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
# 12. Stop L2/L3 traffic
################################################################################
puts('Stopping L2/L3 traffic')
@ixNet.execute('stop', @ixNet.getRoot() + '/traffic')
sleep(5)

################################################################################
# 13. Stop all protocols
################################################################################
puts('Stopping protocols')
@ixNet.execute('stopAllProtocols')

puts('!!! Test Script Ends !!!')
