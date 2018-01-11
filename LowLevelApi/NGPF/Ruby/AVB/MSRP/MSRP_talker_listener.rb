################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright � 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/12/2014 - Sayantan Pramanick - created sample                          #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinsleep("the script") is an        #
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
# damages limitations forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF Audio Video Bridging   #
#     API.                                                                     #
#                                                                              #
#    1. It will create one MSRP Talker in one topology and 2 MSRP Listeners    #
#       in another topology. gPTP clocks will be added in talkers and          #
#       listeners.                                                             #
#    2. Start all protocols.                                                   #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    7. Configure L2-L3 traffic.                                               #
#    9. Start the L2-L3 traffic.                                               #
#   12. Retrieve L2-L3 traffic stats.                                          #
#   13. Stop L2-L3 traffic.                                                    #
#   15. Stop all protocols.                                                    #
# Ixia Softwares:                                                              #
#    IxOS      6.80 EA (6.80.1100.7)                                         #
#    IxNetwork 7.40 EA (7.40.929.15)                                            #
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
puts("!!! Test Script Starts !!!")

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

root   = @ixNet.getRoot()
vport1 = @ixNet.getList(root, 'vport')[0]
vport2 = @ixNet.getList(root, 'vport')[1]

puts("Adding 2 topologies")
@ixNet.add(root, 'topology', '-vports', vport1)
@ixNet.add(root, 'topology', '-vports', vport2)
@ixNet.commit()

topologies = @ixNet.getList(@ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

puts("Adding 1 device groups in topology 1")
@ixNet.add(topo1, 'deviceGroup')

puts("Adding 2 device groups in topology 2")
@ixNet.add(topo2, 'deviceGroup')
@ixNet.add(topo2, 'deviceGroup')
@ixNet.commit()

t1devices = @ixNet.getList(topo1, 'deviceGroup')
t2devices = @ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices[0]
t2dev1 = t2devices[0]
t2dev2 = t2devices[1]

puts("Configuring the multipliers (number of sessions)")
@ixNet.setAttribute(t1dev1, '-multiplier', 1)
@ixNet.setAttribute(t2dev1, '-multiplier', 2)
@ixNet.setAttribute(t2dev2, '-multiplier', 1)
@ixNet.commit()

puts("Adding ethernet/mac endpoints")
@ixNet.add(t1dev1, 'ethernet')
@ixNet.add(t2dev1, 'ethernet')
@ixNet.add(t2dev2, 'ethernet')
@ixNet.commit()

mac1 = @ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = @ixNet.getList(t2dev1, 'ethernet')[0]
mac3 = @ixNet.getList(t2dev2, 'ethernet')[0]

puts("Configuring the mac addresses")
@ixNet.setMultiAttribute(@ixNet.getAttribute(mac1, '-mac') + '/counter',
'-direction', 'increment',
'-start', '22:22:22:22:22:22',
'-step', '00:00:00:00:00:01')

@ixNet.setMultiAttribute(@ixNet.getAttribute(mac2, '-mac') + '/counter',
'-direction', 'increment',
'-start', '44:44:44:44:44:44',
'-step', '00:00:00:00:00:01')

@ixNet.setMultiAttribute(@ixNet.getAttribute(mac3, '-mac') + '/singleValue',
'-value', '66:66:66:66:66:66')
@ixNet.commit()

puts("Adding MSRP talker in topology 1")
talker1 = @ixNet.add(mac1, 'msrpTalker')
@ixNet.commit()
talker1 = @ixNet.remapIds(talker1)[0]

puts("Configuring 2 streams in talker")
@ixNet.setAttribute(talker1, '-streamCount', '2')
@ixNet.commit()

puts("Adding gPTP clock in topology 1")
ptp1 = @ixNet.add(mac1, 'ptp')
@ixNet.commit()
ptp1 = @ixNet.remapIds(ptp1)[0]

puts("Setting clock role as master in AVB talker")
@ixNet.setAttribute(@ixNet.getAttribute(ptp1, '-role') + '/singleValue',
'-value', 'master')
@ixNet.commit()

puts("Adding MSRP listener in topology 2")
listener1 = @ixNet.add(mac2, 'msrpListener')
@ixNet.commit()
listener1 = @ixNet.remapIds(listener1)[0]

puts("Adding gptp clock in topology 2")
ptp2 = @ixNet.add(mac3, 'ptp')
@ixNet.commit()
ptp2 = @ixNet.remapIds(ptp2)[0]

@ixNet.setAttribute(@ixNet.getAttribute(ptp2, '-profile') + '/singleValue',
'-value', 'ieee8021as')
@ixNet.setAttribute(@ixNet.getAttribute(ptp2, '-delayMechanism') + '/singleValue',
'-value', 'peerdelay')
@ixNet.commit()

################################################################################
# 2. Start AVB protocols and wait for 60 seconds
################################################################################
puts("Starting protocols and waiting for 60 seconds for protocols to come up")
@ixNet.execute('startAllProtocols')
sleep(60)

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
puts("Fetching all Protocol Summary Stats\n")
viewPage = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap  = @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues')
    for  statVal in statValList
        puts("***************************************************")
        index = 0
        for statIndv in statVal
            puts(statcap[index] + ' ' + statIndv)
            index = index + 1
        end
    end
end
puts("***************************************************")

################################################################################
# 4. Retrieve protocol learned info
################################################################################
puts("Fetching MSRP Talker Learned Info")
@ixNet.execute('getTalkerDatabases', talker1)
sleep(5)
linfo = @ixNet.getList(talker1, 'learnedInfo')
streamDb = linfo[0]
domainDb = linfo[1]
vlanDb   = linfo[2]

values = @ixNet.getAttribute(streamDb, '-values')
column = @ixNet.getAttribute(streamDb, '-columns')
puts("***************************************************")
puts("****  MSRP Talker stream database learned info ****")
for index in (0..(values.length-1)) do
    rowValue = values[index]
    for col in (0..(column.length-1)) do
        puts(column[col]+' '+ rowValue[col])
    end
end
puts("***************************************************")

values = @ixNet.getAttribute(domainDb, '-values')
column = @ixNet.getAttribute(domainDb, '-columns')
puts("***************************************************")
puts("****  MSRP Talker Domain database learned info ****")
for index in (0..(values.length-1)) do
    rowValue = values[index]
    for col in (0..(column.length-1)) do
        puts(column[col] + ' ' +  rowValue[col])
    end
end

puts("***************************************************")

values = @ixNet.getAttribute(vlanDb, '-values')
column = @ixNet.getAttribute(vlanDb, '-columns')
puts("***************************************************")
puts("*****  MSRP Talker VLAN database learned info *****")
for index in (0..(values.length-1)) do
    rowValue = values[index]
    for col in (0..(column.length-1)) do
        puts(column[col]+' '+ rowValue[col])
    end
end
puts("***************************************************")

puts("Fetching MSRP Listener Learned Info for listener 1")
@ixNet.execute('getListenerDatabases', listener1, '1')
sleep(5)
linfo = @ixNet.getList(listener1, 'learnedInfo')
streamDb = linfo[0]
domainDb = linfo[1]
vlanDb   = linfo[2]

values = @ixNet.getAttribute(streamDb, '-values')
column = @ixNet.getAttribute(streamDb, '-columns')
puts("***************************************************")
puts("*** MSRP Listener stream database learned info ****")
for index in (0..(values.length-1)) do
    rowValue = values[index]
    for col in (0..(column.length-1)) do
        puts(column[col]+' '+ rowValue[col])
    end
end
puts("***************************************************")

values = @ixNet.getAttribute(domainDb, '-values')
column = @ixNet.getAttribute(domainDb, '-columns')
puts("***************************************************")
puts("*** MSRP Listener Domain database learned info ****")
for index in (0..(values.length-1)) do
    rowValue = values[index]
    for col in (0..(column.length-1)) do
        puts(column[col]+' '+ rowValue[col])
    end
end
puts("***************************************************")

values = @ixNet.getAttribute(vlanDb, '-values')
column = @ixNet.getAttribute(vlanDb, '-columns')
puts("***************************************************")
puts("**** MSRP Listener VLAN database learned info *****")
for index in (0..(values.length-1)) do
    rowValue = values[index]
    for col in (0..(column.length-1)) do
        puts(column[col]+' '+ rowValue[col])
    end
end
puts("***************************************************")

################################################################################
# 5. Disable streams and apply changes On The Fly (OTF). Enable again.
################################################################################
puts("Deactivating the streams")
streams = @ixNet.getList(mac1, 'streams')[0]
multiValue = @ixNet.getAttribute(streams, '-active')
@ixNet.setAttribute(multiValue + '/singleValue', '-value', 'false')
@ixNet.commit()

globals = @ixNet.getRoot() + '/globals'
topology = globals + '/topology'
puts("Applying changes on the fly")
begin
    @ixNet.execute('applyOnTheFly', topology)
rescue
    puts("error in applying on the fly change")
end
sleep(5)

puts("Activating the streams")
@ixNet.setAttribute(multiValue + '/singleValue', '-value', 'true')
@ixNet.commit()

puts("Applying changes on the fly")
begin
    @ixNet.execute('applyOnTheFly', topology)
rescue
    puts("error in applying on the fly change")
end
sleep(5)

################################################################################
# 7. Configure L2-L3 traffic
################################################################################
puts("Configuring L2-L3 Traffic Item")
trafficItem1 = @ixNet.add(@ixNet.getRoot() + '/traffic', 'trafficItem')
@ixNet.setMultiAttribute(trafficItem1,
'-name', 'avb_traffic',
'-roundRobinPacketOrdering', 'false',
'-trafficType', 'avb1722')
@ixNet.commit()

trafficItem1 = @ixNet.remapIds(trafficItem1)[0]
endpointSet1 = @ixNet.add(trafficItem1, 'endpointSet')
mcastDestination = [['false', 'none', '22:22:22:22:22:22:00:01',
    '00:00:00:00:00:00:00:00', '1'], ['false', 'none', '22:22:22:22:22:22:00:02',
    '00:00:00:00:00:00:00:00', '1']]
mcastReceiver = [[listener1 + '/subscribedStreams', '0', '0', '0'],
    [listener1 + '/subscribedStreams', '0', '0', '1'],
    [listener1 + '/subscribedStreams', '0', '1', '0'],
    [listener1 + '/subscribedStreams', '0', '1', '1']]

@ixNet.setMultiAttribute(endpointSet1,
'-name',                  'EndpointSet-1',
'-multicastDestinations', mcastDestination,
'-scalableSources',       [],
'-multicastReceivers',    mcastReceiver,
'-scalableDestinations',  [],
'-ngpfFilters',           [],
'-trafficGroups',         [],
'-sources',               [],
'-destinations',          [])
@ixNet.commit()

@ixNet.setMultiAttribute(trafficItem1 + '/tracking',
'-trackBy', ['trackingenabled0', 'avbStreamName0'])
@ixNet.commit()

###############################################################################
# 9. Apply and start L2/L3 traffic
###############################################################################
puts('applying L2/L3 traffic')
@ixNet.execute('apply', @ixNet.getRoot() + '/traffic')
sleep(5)

puts('starting L2/L3 traffic')
@ixNet.execute('start', @ixNet.getRoot() + '/traffic')

###############################################################################
# 12. Retrieve L2/L3 traffic item statistics
###############################################################################
puts('Verifying all the L2-L3 traffic stats')
viewPage = '::ixNet::OBJ-/statistics/view:"Flow Statistics"/page'
statcap =  @ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in @ixNet.getAttribute(viewPage, '-rowValues')
    for  statVal in statValList
        puts("***************************************************")
        index = 0
        for satIndv in statVal
            puts(statcap[index]+' '+satIndv)
            index = index + 1
        end
    end
end
puts("***************************************************")

################################################################################
# 14. Stop L2/L3 traffic
#################################################################################
puts('Stopping L2/L3 traffic')
@ixNet.execute('stop', @ixNet.getRoot() + '/traffic')
sleep(5)

################################################################################
# 15. Stop all protocols
################################################################################
puts('Stopping protocols')
@ixNet.execute('stopAllProtocols')
puts('!!! Test Script Ends !!!')
