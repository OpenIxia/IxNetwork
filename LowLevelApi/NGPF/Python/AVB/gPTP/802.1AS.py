################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright ? 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    13/08/2013 - Irina Popa - created sample                                  #
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
#   Also demonstrates how to set a multivalue. 		   						   #
# Module:                                                                      #
#    The sample was tested on an FlexAP10G16S module.                          #
# Software:                                                                    #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
#                                                                              #
################################################################################
# import Python packages

import time
import os
from IxNetwork import IxNet

# create an instance of the IxNet class
ixNet = IxNet()

# create absolute path for the config and load it
print ("Connecting to server: localhost")
ixNet.connect('localhost', '-port', 8009, '-version', '7.40')

print ("Cleaning up IxNetwork...")
ixNet.execute('newConfig')

# all objects are under root
root = ixNet.getRoot()

print ("\nAdd virtual ports to configuration...")
vports = []
vports.append(ixNet.add(root, 'vport'))
vports.append(ixNet.add(root, 'vport'))
ixNet.commit()

# get virtual ports
vports = ixNet.getList(ixNet.getRoot(), 'vport')
print ('Add chassis in IxNetwork...')
chassis = '10.205.15.90'
availableHardwareId = ixNet.getRoot()+'availableHardware'
ixNet.add(availableHardwareId, 'chassis', '-hostname', chassis)
ixNet.commit()

print ("Assigning ports from " + chassis + " to "+ str(vports) + " ...")
ixNet.setAttribute(vports[0], '-connectedTo', '/availableHardware/chassis:"10.205.15.90"/card:1/port:1')
ixNet.setAttribute(vports[1], '-connectedTo', '/availableHardware/chassis:"10.205.15.90"/card:1/port:2')
ixNet.commit()

print ("Rebooting ports...")
jobs = [ixNet.setAsync().execute('resetPortCpu', vp) for vp in vports]
for j in jobs:
    print j + ' ' + ixNet.getResult(j)
print ("Done... Ports are rebooted...")
time.sleep(5)
ixNet.execute('clearStats')

# ######################## Add gPTP Master and gPTP Slave ############################ #

# adding topology with gPTP Master and gPTP Slave
print ('\n\nCreate first topology with gPTP master...')
print ('\nAdd topology...')
ixNet.add(root, 'topology')
print ('\nUse ixNet.commit() to commit added child under root.')
ixNet.commit()

print ('\nUse ixNet.getList to get newly added child under root.')
topM = ixNet.getList(root, 'topology')[0]
print ('Add virtual port to topology and change its name...')
ixNet.setMultiAttribute(topM, '-vports', vports[0], '-name', '802.1AS Master')
ixNet.commit()

print ('Add DeviceGroup for 802.1AS...')
ixNet.add(topM, 'deviceGroup')
ixNet.commit()

dg_gPTP_m = ixNet.getList(topM, 'deviceGroup')[0]
print ('Create the Ethernet stack in this DeviceGroup...')
print ('Add Ethernet layer...')
ixNet.add(dg_gPTP_m, 'ethernet')
ixNet.commit()

ethM = ixNet.getList(dg_gPTP_m, 'ethernet')[0]
print ('Add PTP layer...')
ixNet.add(ethM, 'ptp')
ixNet.commit()

gPTPM = ixNet.getList(ethM, 'ptp')[0]
print ('Change each Device Group multiplier on master topology...')
ixNet.setAttribute(dg_gPTP_m, '-multiplier', 1)
ixNet.commit()

# adding topology with 802.1AS Slave
print ('\n\nCreate  topology with 802.1AS Slave...')
print ('Add topology...')
ixNet.add(root, 'topology')
ixNet.commit()

# the newly added topology is the second 'topology' object type under root
topS = ixNet.getList(root, 'topology')[1]
print ('Add virtual port to topology and change its name...')
ixNet.setMultiAttribute(topS, '-vports', vports[1], '-name', '802.1AS Slave')
ixNet.commit()

print ('Add DeviceGroup for 802.1AS Slave...')
ixNet.add(topS, 'deviceGroup')
ixNet.commit()

dg_gPTP_s = ixNet.getList(topS, 'deviceGroup')[0]
print ('Create the Ethernet stack in this DeviceGroup...')
print ('Add Ethernet layer...')
ixNet.add(dg_gPTP_s, 'ethernet')
ixNet.commit()

ethS = ixNet.getList(dg_gPTP_s, 'ethernet')[0]
print ('Add PTP layer...')
ixNet.add(ethS, 'ptp')
ixNet.commit()

gPTPS = ixNet.getList(ethS, 'ptp')[0]
print ('Change each Device Group multiplier on slave topology...')
ixNet.setAttribute(dg_gPTP_s, '-multiplier', 1)
ixNet.commit()

# ######################## End Add 802.1 AS DGs ######################## #
# ###################### Configure parameters ################################ #
# ######################## Configure Clock Role  on DG1################################ #

#edit Clock Role in DG1
print ('# \n###################### HOW TO set a parameter  ####### #')
print ('\n\nChange Clock Role from slave to master on the first DG...')
#ixNet.help(gPTPM)

print ('\n\nChange Role ..')
role = ixNet.getAttribute(gPTPM, '-role')
ixNet.setAttribute(role, '-pattern', 'singleValue')
ixNet.commit()

role_singleValue = ixNet.getList(role, 'singleValue')[0]
ixNet.setMultiAttribute(role_singleValue, '-value', 'master')
ixNet.commit()

# ######################## Configure Profile on Master DG ################################ #
print ('\n\nChange Profile  on the first DG...')
# ######################## Configure Profile  ############################### #

print ('\n\nChange Profile ..')
profile = ixNet.getAttribute(gPTPM, '-profile')
ixNet.setAttribute(profile, '-pattern', 'singleValue')
ixNet.commit()

profile_singleValue = ixNet.getList(profile, 'singleValue')[0]
ixNet.setMultiAttribute(profile_singleValue, '-value', 'ieee8021as')
ixNet.commit()

# ######################## Configure Profile on Slave DG ################################ #
print ('\n\nChange Profile  on the second DG...')
# ######################## Configure Profile  ############################### #

print ('\n\nChange Profile ..')
profile = ixNet.getAttribute(gPTPS, '-profile')
ixNet.setAttribute(profile, '-pattern', 'singleValue')
ixNet.commit()

profile_singleValue = ixNet.getList(profile, 'singleValue')[0]
ixNet.setMultiAttribute(profile_singleValue, '-value', 'ieee8021as')
ixNet.commit()

# ######################## Configure Delay Mechanism on Master DG ################################ #
print ('\n\nChange Delay Mechanism  on the first DG...')
# ######################## Configure Delay Mechanism  ############################### #

print ('\n\nChange Delay Mechanism ..')
delayMechanism = ixNet.getAttribute(gPTPM, '-delayMechanism')
ixNet.setAttribute(delayMechanism, '-pattern', 'singleValue')
ixNet.commit()

delayMechanism_singleValue = ixNet.getList(delayMechanism, 'singleValue')[0]
ixNet.setMultiAttribute(delayMechanism_singleValue, '-value', 'peerdelay')
ixNet.commit()

# ######################## Configure Delay Mechanism on Slave DG ################################ #
print ('\n\nChange Delay Mechanism  on the second DG...')
# ######################## Configure Delay Mechanism  ############################### #

print ('\n\nChange Delay Mechanism ..')
delayMechanism = ixNet.getAttribute(gPTPS, '-delayMechanism')
ixNet.setAttribute(profile, '-delayMechanism', 'singleValue')
ixNet.commit()

delayMechanism_singleValue = ixNet.getList(delayMechanism, 'singleValue')[0]
ixNet.setMultiAttribute(delayMechanism_singleValue, '-value', 'peerdelay')
ixNet.commit()

# ######################## Configure Step Mode on Master DG ################################ #

print ('\n\nChange Step Mode  on the first DG...')
# ######################## Configure Step Mode  ############################### #

print ('\n\nChange Step Mode ..')
stepMode = ixNet.getAttribute(gPTPM, '-stepMode')
ixNet.setAttribute(stepMode, '-pattern', 'singleValue')
ixNet.commit()

stepMode_singleValue = ixNet.getList(stepMode, 'singleValue')[0]
ixNet.setMultiAttribute(stepMode_singleValue, '-value', 'twostep')
ixNet.commit()

# ######################## Configure Step Mode on Slave DG ################################ #

print ('\n\nChange Step Mode on the second DG...')
# ######################## Configure Step Mode  ############################### #

print ('\n\nChange Step Mode ..')
stepMode = ixNet.getAttribute(gPTPS, '-stepMode')
ixNet.setAttribute(profile, '-stepMode', 'singleValue')
ixNet.commit()

stepMode_singleValue = ixNet.getList(stepMode, 'singleValue')[0]
ixNet.setMultiAttribute(stepMode_singleValue, '-value', 'twostep')
ixNet.commit()

# ################################### Dynamics ############################### #

print ('# \n####################### HOW TO start/stop protocols ####### #')
#starting 802.1AS protocol
print ("\n\nStarting the 802.1AS DGs using ixNet.execute('start', dg_gPTP_m)")
ixNet.execute('start', dg_gPTP_m)
time.sleep(0.5)
ixNet.execute('start', dg_gPTP_s)
time.sleep(2)

print ('# \n####################### HOW TO send Signall messages  ####### #')
#send Signal Messages on 802.1AS protocol
#ixNet.help(gPTPS)
print ("\n\nSend Signalling messages from gPTP slave using ixNet.execute('gPtpSendSignaling', listOfSlaveObjects[0], 'enumOpt-DoNotChange', 'enumOpt-DoNotChange', 'enumOpt-V2_1_per_4_seconds_', 'false', 'false') command")
ixNet.execute('gPtpSendSignaling', gPTPS, 'enumOpt-DoNotChange', 'enumOpt-DoNotChange', 'enumOpt-V2_1_per_4_seconds_', 'false', 'false')
print ('\n\nStop topologies...')
ixNet.execute('stop',topS)
time.sleep(10)

ixNet.execute('stop',topM)
print ("\n\nCleaning up IxNetwork...")
ixNet.execute('newConfig')

ixNet.disconnect()
print ("Done: IxNetwork session is closed...")
