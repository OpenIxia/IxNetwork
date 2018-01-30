################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright � 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    05/12/2015 - Dhiraj Khandelwal - created sample                           #
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
#    This script intends to demonstrate how to use NGPF BFDv6  API             #
#    It will create 2 BFDv6  topologyes, it will start the emulation and       #
#    than it will retrieve and display few statistics                          #
# Software:                                                                    #
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

    if (chassis1 != chassis2)
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
@ixNet.setMultiAttribute(@ixNet.getAttribute(mac1, '-mac') + '/counter',
'-direction', 'increment',
'-start',     '18:03:73:C7:6C:B1',
'-step',      '00:00:00:00:00:01')

@ixNet.setAttribute(@ixNet.getAttribute(mac2, '-mac') + '/singleValue',
'-value', '18:03:73:C7:6C:01')
@ixNet.commit()

puts('@ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet\')')
puts(@ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet'))

puts("Add ipv6")
@ixNet.add(mac1, 'ipv6')
@ixNet.add(mac2, 'ipv6')
@ixNet.commit()

ip1 = @ixNet.getList(mac1, 'ipv6')[0]
ip2 = @ixNet.getList(mac2, 'ipv6')[0]

mvAdd1 = @ixNet.getAttribute(ip1, '-address')
mvAdd2 = @ixNet.getAttribute(ip2, '-address')
mvGw1  = @ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = @ixNet.getAttribute(ip2, '-gatewayIp')

puts("configuring ipv6 addresses")
@ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '11:0:0:0:0:0:0:1')
@ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '11:0:0:0:0:0:0:2')
@ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '11:0:0:0:0:0:0:2')
@ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '11:0:0:0:0:0:0:1')

@ixNet.setAttribute(@ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '64')
@ixNet.setAttribute(@ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '64')

@ixNet.setMultiAttribute(@ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.setMultiAttribute(@ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.commit()

puts('@ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6\')')
puts(@ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv6'))

###########################################################################
#Adding and Configuring ISISL3 Router
###########################################################################
puts('Adding ISIS L3 and Configuring')
@ixNet.add(mac1, 'isisL3')
@ixNet.add(mac2, 'isisL3')
@ixNet.commit()

isisL31 = @ixNet.getList(mac1, 'isisL3')[0]
isisL32 = @ixNet.getList(mac2, 'isisL3')[0]

enableBFD1 = @ixNet.getAttribute(isisL31, '-enableBfdRegistration')
enableBFD2 = @ixNet.getAttribute(isisL32, '-enableBfdRegistration')
networkType1 = @ixNet.getAttribute(isisL31, '-networkType')
networkType2 = @ixNet.getAttribute(isisL32, '-networkType')

@ixNet.setAttribute(enableBFD1 +'/singleValue', '-value', 'true')
@ixNet.setAttribute(enableBFD2 +'/singleValue', '-value', 'true')
@ixNet.setAttribute(networkType1 + '/singleValue', '-value', 'pointpoint')
@ixNet.setAttribute(networkType2 + '/singleValue', '-value', 'pointpoint')
@ixNet.commit()

puts('@ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/isisL3\')')
@ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/isisL3')

###########################################################################
#Add and Configure BFDv6 Interface
###########################################################################
puts("Adding BFDv6 and Configuring")
@ixNet.add(ip1, 'bfdv6Interface')
@ixNet.add(ip2, 'bfdv6Interface')
@ixNet.commit()

bfdv61 = @ixNet.getList(ip1, 'bfdv6Interface')[0]
bfdv62 = @ixNet.getList(ip2, 'bfdv6Interface')[0]

txInterval1 = @ixNet.getAttribute(bfdv61, '-txInterval')
txInterval2 = @ixNet.getAttribute(bfdv62, '-txInterval')
minRxInterval1 = @ixNet.getAttribute(bfdv61, '-txInterval')
minRxInterval2 = @ixNet.getAttribute(bfdv62, '-txInterval')

@ixNet.setAttribute(txInterval1 + '/singleValue', '-value', '2000')
@ixNet.setAttribute(txInterval2 + '/singleValue', '-value', '2000')
@ixNet.setAttribute(minRxInterval1 + '/singleValue', '-value', '2000')
@ixNet.setAttribute(minRxInterval2 + '/singleValue', '-value', '2000')
@ixNet.commit()

puts('@ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/bfdv6Interface\')')
@ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/bfdv6Interface')

################################################################################
# Start BFD protocol and wait for 45 seconds                                   #
################################################################################
puts("Starting protocols and waiting for 45 seconds for protocols to come up")
@ixNet.execute('startAllProtocols')
sleep(45)

################################################################################
# Retrieve protocol statistics                                              #
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

############################################################################
##On The Fly Section
############################################################################
puts("Deactivating and Activating BFDv6 Interface On the fly")
activation = @ixNet.getAttribute(bfdv61, '-active')

@ixNet.setAttribute(activation +'/singleValue', '-value', 'false')
@ixNet.commit()
globalObj = @ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
puts("Applying changes on the fly")
begin
    @ixNet.execute('applyOnTheFly', topology)
rescue
    puts("error in applying on the fly change")
end
sleep(10)
@ixNet.setAttribute(activation +'/singleValue', '-value', 'true')
@ixNet.commit()
globalObj = @ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
puts("Applying changes on the fly")
begin
    @ixNet.execute('applyOnTheFly', topology)
rescue
    puts("error in applying on the fly change")
end
sleep(10)

###############################################################################
# Retrieve protocol learned info                                              #
###############################################################################
puts("Fetching BFD learned info")
@ixNet.execute('getLearnedInfo', bfdv61, '1')
sleep(5)
linfo  = @ixNet.getList(bfdv61, 'learnedInfo')[0]
values = @ixNet.getAttribute(linfo, '-values')

puts("***************************************************")
for v in values :
    puts(v)
end
puts("***************************************************")

################################################################################
# Stop all protocols                                                           #
################################################################################
puts('Stopping protocols')
@ixNet.execute('stopAllProtocols')

puts('!!! Test Script Ends !!!')
