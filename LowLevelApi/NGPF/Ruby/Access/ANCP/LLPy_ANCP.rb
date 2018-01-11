################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright ? 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/08/2014 - Paul Ganea - created sample                         #
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
# The script creates and configures a topology with one ANCP DG.                               #
# Set/Get multivalue parameters.                                               #
# Start/Stop protocols.                                                        #
# Module:                                                                      #
#    The sample was tested on an XMVDC module.                          #
# Software:                                                                    #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
#                                                                              #
################################################################################

$:.unshift 'C:\samples\IxNetwork.rb'
require 'IxNetwork'

# create an instance of the IxNet class
@ixNet = IxNetwork.new

# create absolute path for the config and load it
puts("Connecting to server: localhost")
@ixNet.connect('10.200.115.203', '-port', 8009, '-version', '7.40')

puts("Cleaning up IxNetwork...")
@ixNet.execute('newConfig')

# all objects are under root
root = @ixNet.getRoot()

puts("\nAdd one virtual port to configuration...")
vports = []
vports.push(@ixNet.add(root, 'vport'))
@ixNet.commit()
# get virtual ports
vports = @ixNet.getList(@ixNet.getRoot(), 'vport')

puts('Add chassis in IxNetwork...')
chassis = '10.200.115.151'
availableHardwareId = @ixNet.getRoot()+'availableHardware'
@ixNet.add(availableHardwareId, 'chassis', '-hostname', chassis)
@ixNet.commit()

puts("Assigning ports from " + chassis + " to "+ vports.to_s + " ...")
@ixNet.setAttribute(vports[0], '-connectedTo', '/availableHardware/chassis:"10.200.115.151"/card:4/port:2')
@ixNet.commit()

puts("Rebooting ports...")
jobs = Array.new
for vp in vports do
    jobs.push(@ixNet.setAsync().execute('resetPortCpu', vp))
end
for j in jobs
    puts j + ' ' + @ixNet.getResult(j)
end
puts("Done... Ports are rebooted...")
puts("")
sleep(5)
@ixNet.execute('clearStats')

# ######################## Add ANCP DGs ####################################### #
puts('# \n######## HOW TO create a topology with one DG and various layers ##### #')
puts('\n\nCreate first the topology...')
puts('\nAdd topology...')
@ixNet.add(root, 'topology')
puts('\nUse @ixNet.commit() to commit added child under root.')
@ixNet.commit()

puts('\nUse @ixNet.getList to get newly added child under root.')
topANCP = @ixNet.getList(root, 'topology')[0]
puts('Add virtual port to topology and change its name...')
@ixNet.setMultiAttribute(topANCP, '-vports', vports[0], '-name', 'AN Topology')
@ixNet.commit()

puts('Add DeviceGroup for ANCP...')
@ixNet.add(topANCP, 'deviceGroup')
@ixNet.commit()

DG = @ixNet.getList(topANCP, 'deviceGroup')[0]
puts('Create the ANCP stack in this DeviceGroup...')
puts('Add Ethernet layer...')
@ixNet.add(DG, 'ethernet')
@ixNet.commit()

eth = @ixNet.getList(DG, 'ethernet')[0]
puts('Add the IP layer...')
@ixNet.add(eth, 'ipv4')
@ixNet.commit()

ip = @ixNet.getList(eth, 'ipv4')[0]
puts('Add the ANCP layer...')
@ixNet.add(ip, 'ancp')
@ixNet.commit()

ancp = @ixNet.getList(ip, 'ancp')[0]
puts('Chain the DSL lines Network Group to the ANCP DG...')
@ixNet.add(DG, 'networkGroup')
@ixNet.commit()

netGr = @ixNet.getList(DG, 'networkGroup')[0]
@ixNet.add(netGr, 'dslPools')
@ixNet.commit()

dsl = @ixNet.getList(netGr, 'dslPools')[0]
puts('Change each Device Group multiplier...')
@ixNet.setAttribute(DG, '-multiplier', 5)
@ixNet.commit()

@ixNet.setAttribute(netGr, '-multiplier', 10)
@ixNet.commit()

# ###################### Configure parameters ################################ #
# ###################### Configure parameters ################################ #
# ###################### Configure parameters ################################ #
# ######################## Configure VLAN IDs ################################ #
# #################### Enable VLANs for ethernet layer  ###################### #

puts("\n\nEnable VLANs on both Ethernet layers...")
# puts @ixNet.help(eth)
vlan      = @ixNet.getAttribute(eth, '-enableVlans')
vlan_value = @ixNet.getList(vlan, 'singleValue')
@ixNet.setAttribute(vlan_value[0], '-value', 'true')
@ixNet.commit()

# #################### Enabled VLANs for ethernet layer  ###################### #
# ######################## Configure VLAN IDs ################################ #
puts('# ######################## HOW TO set a multivalue attribute ########## #')

puts('\n\nChange VLAN IDs for both Ethernet layers...')
# puts @ixNet.help(eth)  # desired attribute is not found on eth
vlan = @ixNet.getList(eth, 'vlan')[0]
# puts @ixNet.help(vlan)  # desired attribute is '-vlanId'
# VLAN ID parameter is a multivalue object
vlanID_mv      = @ixNet.getAttribute(vlan, '-vlanId')

puts('\nTo see childs and attributes of an object just type: "@ixNet.help(current_object)". The output should be like this:')
puts @ixNet.help(vlanID_mv)

puts('\nAvailable patterns for this multivalue can be found out by using getAttribute on the "-availablePatterns" attribute.')
puts("Output for:  @ixNet.getAttribute(vlanID1_mv, '-availablePatterns')")
puts @ixNet.getAttribute(vlanID_mv, '-availablePatterns')

puts('\nSelected pattern: counter. Set this pattern under "-pattern" attribute with setAttribute.')
puts("@ixNet.setAttribute(vlanID_mv, '-pattern', 'singleValue')")
@ixNet.setAttribute(vlanID_mv, '-pattern', 'singleValue')

puts('\nUse @ixNet.commit() to commit changes made with setAttribute.')
@ixNet.commit()

vlanID_mv_value = @ixNet.getList(vlanID_mv, 'singleValue')[0]

puts('Use setMultiAttribute to set more attributes at once.')
@ixNet.setMultiAttribute(vlanID_mv_value, '-value', '5')
@ixNet.commit()

# ######################## Configured VLAN IDs ################################ #
# ######################## Configure AN IP Values ################################ #

puts('\n\nChange AN IP...')
ip_add = @ixNet.getAttribute(ip, '-address')
ip_add_counter = @ixNet.getList(ip_add, 'counter')
@ixNet.setMultiAttribute(ip_add_counter[0], '-direction', 'increment', '-start', '5.5.5.5', '-step', '0.0.0.1')
@ixNet.commit()

# ######################## Configured AN IP Values ################################ #
# ######################## Configure AN Gateway IP Values ################################ #

gw = @ixNet.getAttribute(ip, '-gatewayIp')
gw_counter = @ixNet.getList(gw, 'counter')
@ixNet.setMultiAttribute(gw_counter[0], '-direction', 'increment', '-start', '5.5.5.1', '-step', '0.0.0.0')
@ixNet.commit()

# ######################## Configured AN Gateway IP Values ################################ #
# ######################## Configure NAS IP Values ################################ #

nasip = @ixNet.getAttribute(ancp, '-nasIp')
nasip_counter = @ixNet.getList(nasip, 'counter')
@ixNet.setMultiAttribute(nasip_counter[0], '-direction', 'increment', '-start', '5.5.5.1', '-step', '0.0.0.0')
@ixNet.commit()

# ######################### Configured NAS IP Values ############################### #
# ######################## Enable Trigger Access Loops Parameter ################################ #

trigger = @ixNet.getAttribute(ancp, '-triggerAccessLoopEvents')
trigger_value = @ixNet.getList(trigger, 'singleValue')
@ixNet.setAttribute(trigger_value[0], '-value', 'true')
@ixNet.commit()

# ######################## Enabled Trigger Access Loops Parameter ################################ #
# ######################## Enable Remote ID Parameter on DSL lines################################ #

remoteID = @ixNet.getAttribute(dsl, '-enableRemoteId')
remoteID_value = @ixNet.getList(remoteID, 'singleValue')
@ixNet.setAttribute(remoteID_value[0], '-value', 'true')
@ixNet.commit()

# ######################## Enabled Remote ID Parameter on DSL lines################################ #
# ################################### Dynamics ############################### #

puts('# \n####################### HOW TO start/stop/restart protocols ####### #')
#starting topologies
puts("\n\nStarting the topologies using @ixNet.execute('start', topANCP)")
@ixNet.execute('start', topANCP)
# wait for all sessions to start

while (@ixNet.getAttribute(ancp, '-stateCounts')[1]).to_i > 0 do
    puts('ancp layer: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: '+ @ixNet.getAttribute(ancp, '-stateCounts').to_s)
    puts('Waiting for all sessions to be started...')
    sleep(3)
end
puts('ancp layer: Sessions TOTAL/ NOT STARTED/ DOWN/ UP: ' + @ixNet.getAttribute(ancp, '-stateCounts').to_s)
puts('All sessions started...')
sleep(15)

puts("\n\nRefreshing NGPF statistics views can be done from API using the following exec command: @ixNet.execute('refresh', '__allNextGenViews')")
@ixNet.execute('refresh', '__allNextGenViews')
sleep(3)
mv          = @ixNet.getList(@ixNet.getRoot(), 'statistics')[0]
view_list   = @ixNet.getList(mv, 'view')

puts('\n\nAvailable statistics views are :\n ' + view_list.to_s   )
#stopping per topology

puts('\n\nStop ANCP topology...')
@ixNet.execute('stop',topANCP)
sleep(10)

puts("\n\nCleaning up IxNetwork...")
@ixNet.execute('newConfig')

@ixNet.disconnect()
puts("Done: IxNetwork session is closed...")
