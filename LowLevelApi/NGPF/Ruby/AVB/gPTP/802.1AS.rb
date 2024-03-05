################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
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
#                                                                              #
# Description:                                                                 #
#   This script intends to demonstrate how to configure VxLAN with DHCPv6      #
#   Client and DHCPv6 Server. It configures one topology with one Device Group #
#   with VxLAN and a chained Device Group with the DHCPv6 Client stack         #
#   and a corresponding topology containing one Device Group with VxLAN and a  #
#   chained Device Group with DHCPv6 Server stack.                             #
#   Also demonstrates how to set a multivalue.                                 #
# Module:                                                                      #
#    The sample was tested on an FlexAP10G16S module.                          #
################################################################################

################################################################################
# Import the ixnetwork library
# First add the library to Ruby's $LOAD_PATH:    $:.unshift <library_dir>
################################################################################
require 'ixnetwork'

# create an instance of the IxNet class
@ixNet = IxNetwork.new

# create absolute path for the config and load it
puts("Connecting to server: localhost")
@ixNet.connect('10.200.115.203', '-port', 8009, '-version', '7.40')

puts("Cleaning up IxNetwork...")
@ixNet.execute('newConfig')

# all objects are under root
root = @ixNet.getRoot()

puts("\nAdd virtual ports to configuration...")
vports = []
vports.push(@ixNet.add(root, 'vport'))
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
@ixNet.setAttribute(vports[0], '-connectedTo', '/availableHardware/chassis:"10.200.115.151"/card:4/port:1')
@ixNet.setAttribute(vports[1], '-connectedTo', '/availableHardware/chassis:"10.200.115.151"/card:4/port:2')
@ixNet.commit()

puts("Rebooting ports...")
jobs = Array.new
for vp in vports.each do
    jobs.push(@ixNet.setAsync().execute('resetPortCpu', vp))
end
for j in jobs.each do
    puts(j + ' ' + @ixNet.getResult(j))
end
puts("Done... Ports are rebooted...")
sleep(5)
@ixNet.execute('clearStats')

# ######################## Add gPTP Master and gPTP Slave ############################ #

# adding topology with gPTP Master and gPTP Slave
puts('\n\nCreate first topology with gPTP master...')
puts('\nAdd topology...')
@ixNet.add(root, 'topology')
puts('\nUse @ixNet.commit() to commit added child under root.')
@ixNet.commit()

puts('\nUse @ixNet.getList to get newly added child under root.')
topM = @ixNet.getList(root, 'topology')[0]
puts('Add virtual port to topology and change its name...')
@ixNet.setMultiAttribute(topM, '-vports', vports[0], '-name', '802.1AS Master')
@ixNet.commit()

puts('Add DeviceGroup for 802.1AS...')
@ixNet.add(topM, 'deviceGroup')
@ixNet.commit()

dg_gPTP_m = @ixNet.getList(topM, 'deviceGroup')[0]
puts('Create the Ethernet stack in this DeviceGroup...')
puts('Add Ethernet layer...')
@ixNet.add(dg_gPTP_m, 'ethernet')
@ixNet.commit()

ethM = @ixNet.getList(dg_gPTP_m, 'ethernet')[0]
puts('Add PTP layer...')
@ixNet.add(ethM, 'ptp')
@ixNet.commit()

gPTPM = @ixNet.getList(ethM, 'ptp')[0]
puts('Change each Device Group multiplier on master topology...')
@ixNet.setAttribute(dg_gPTP_m, '-multiplier', 1)
@ixNet.commit()

# adding topology with 802.1AS Slave
puts('\n\nCreate  topology with 802.1AS Slave...')
puts('Add topology...')
@ixNet.add(root, 'topology')
@ixNet.commit()

# the newly added topology is the second 'topology' object type under root
topS = @ixNet.getList(root, 'topology')[1]
puts('Add virtual port to topology and change its name...')
@ixNet.setMultiAttribute(topS, '-vports', vports[1], '-name', '802.1AS Slave')
@ixNet.commit()

puts('Add DeviceGroup for 802.1AS Slave...')
@ixNet.add(topS, 'deviceGroup')
@ixNet.commit()

dg_gPTP_s = @ixNet.getList(topS, 'deviceGroup')[0]
puts('Create the Ethernet stack in this DeviceGroup...')
puts('Add Ethernet layer...')
@ixNet.add(dg_gPTP_s, 'ethernet')
@ixNet.commit()

ethS = @ixNet.getList(dg_gPTP_s, 'ethernet')[0]
puts('Add PTP layer...')
@ixNet.add(ethS, 'ptp')
@ixNet.commit()

gPTPS = @ixNet.getList(ethS, 'ptp')[0]
puts('Change each Device Group multiplier on slave topology...')
@ixNet.setAttribute(dg_gPTP_s, '-multiplier', 1)
@ixNet.commit()

# ###################### Configure parameters ################################ #
# ######################## Configure Clock Role  on DG1################################ #

#edit Clock Role in DG1
puts('# \n###################### HOW TO set a parameter  ####### #')
puts('\n\nChange Clock Role from slave to master on the first DG...')
#@ixNet.help(gPTPM)

puts('\n\nChange Role ..')
role = @ixNet.getAttribute(gPTPM, '-role')
@ixNet.setAttribute(role, '-pattern', 'singleValue')
@ixNet.commit()

role_singleValue = @ixNet.getList(role, 'singleValue')[0]
@ixNet.setMultiAttribute(role_singleValue, '-value', 'master')
@ixNet.commit()

# ######################## Configure Profile on Master DG ################################ #
puts('\n\nChange Profile  on the first DG...')
# ######################## Configure Profile  ############################### #

puts('\n\nChange Profile ..')
profile = @ixNet.getAttribute(gPTPM, '-profile')
@ixNet.setAttribute(profile, '-pattern', 'singleValue')
@ixNet.commit()

profile_singleValue = @ixNet.getList(profile, 'singleValue')[0]
@ixNet.setMultiAttribute(profile_singleValue, '-value', 'ieee8021as')
@ixNet.commit()

# ######################## Configure Profile on Slave DG ################################ #
puts('\n\nChange Profile  on the second DG...')
# ######################## Configure Profile  ############################### #

puts('\n\nChange Profile ..')
profile = @ixNet.getAttribute(gPTPS, '-profile')
@ixNet.setAttribute(profile, '-pattern', 'singleValue')
@ixNet.commit()

profile_singleValue = @ixNet.getList(profile, 'singleValue')[0]
@ixNet.setMultiAttribute(profile_singleValue, '-value', 'ieee8021as')
@ixNet.commit()

# ######################## Configure Delay Mechanism on Master DG ################################ #
puts('\n\nChange Delay Mechanism  on the first DG...')
# ######################## Configure Delay Mechanism  ############################### #

puts('\n\nChange Delay Mechanism ..')
delayMechanism = @ixNet.getAttribute(gPTPM, '-delayMechanism')
@ixNet.setAttribute(delayMechanism, '-pattern', 'singleValue')
@ixNet.commit()

delayMechanism_singleValue = @ixNet.getList(delayMechanism, 'singleValue')[0]
@ixNet.setMultiAttribute(delayMechanism_singleValue, '-value', 'peerdelay')
@ixNet.commit()

# ######################## Configure Delay Mechanism on Slave DG ################################ #
puts('\n\nChange Delay Mechanism  on the second DG...')
# ######################## Configure Delay Mechanism  ############################### #

puts('\n\nChange Delay Mechanism ..')
delayMechanism = @ixNet.getAttribute(gPTPS, '-delayMechanism')
@ixNet.setAttribute(profile, '-delayMechanism', 'singleValue')
@ixNet.commit()

delayMechanism_singleValue = @ixNet.getList(delayMechanism, 'singleValue')[0]
@ixNet.setMultiAttribute(delayMechanism_singleValue, '-value', 'peerdelay')
@ixNet.commit()

# ######################## Configure Step Mode on Master DG ################################ #

puts('\n\nChange Step Mode  on the first DG...')
# ######################## Configure Step Mode  ############################### #

puts('\n\nChange Step Mode ..')
stepMode = @ixNet.getAttribute(gPTPM, '-stepMode')
@ixNet.setAttribute(stepMode, '-pattern', 'singleValue')
@ixNet.commit()

stepMode_singleValue = @ixNet.getList(stepMode, 'singleValue')[0]
@ixNet.setMultiAttribute(stepMode_singleValue, '-value', 'twostep')
@ixNet.commit()

# ######################## Configure Step Mode on Slave DG ################################ #

puts('\n\nChange Step Mode on the second DG...')
# ######################## Configure Step Mode  ############################### #

puts('\n\nChange Step Mode ..')
stepMode = @ixNet.getAttribute(gPTPS, '-stepMode')
@ixNet.setAttribute(profile, '-stepMode', 'singleValue')
@ixNet.commit()

stepMode_singleValue = @ixNet.getList(stepMode, 'singleValue')[0]
@ixNet.setMultiAttribute(stepMode_singleValue, '-value', 'twostep')
@ixNet.commit()

# ################################### Dynamics ############################### #

puts('# \n####################### HOW TO start/stop protocols ####### #')
#starting 802.1AS protocol
puts("\n\nStarting the 802.1AS DGs using @ixNet.execute('start', dg_gPTP_m)")
@ixNet.execute('start', dg_gPTP_m)
sleep(0.5)
@ixNet.execute('start', dg_gPTP_s)
sleep(2)

puts('# \n####################### HOW TO send Signall messages  ####### #')
#send Signal Messages on 802.1AS protocol
#@ixNet.help(gPTPS)
puts("\n\nSend Signalling messages from gPTP slave using @ixNet.execute('gPtpSendSignaling', listOfSlaveObjects[0], 'enumOpt-DoNotChange', 'enumOpt-DoNotChange', 'enumOpt-V2_1_per_4_seconds_', 'false', 'false') command")
@ixNet.execute('gPtpSendSignaling', gPTPS, 'enumOpt-DoNotChange', 'enumOpt-DoNotChange', 'enumOpt-V2_1_per_4_seconds_', 'false', 'false')
puts('\n\nStop topologies...')
@ixNet.execute('stop',topS)
sleep(10)

@ixNet.execute('stop',topM)
puts("\n\nCleaning up IxNetwork...")
@ixNet.execute('newConfig')

@ixNet.disconnect()
puts("Done: IxNetwork session is closed...")
