#!/usr/bin/python
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
#    Script  will create following:                                            #
#    1. Create PPPoX Client and server                                         #
#    2. Modify various parameters:											   #
#		Enable MRRU Negotiation												   #
#		Multilink MRRU size													   #
#		ML-PPP Endpoint Discriminator Option								   #
#		Endpoint discriminator class_ip_address                                #
#		Internet Protocol Address                                              #
#		MAC address                                                            #
#	 3. Start
#	 4. Stop                                                          	       #
#                                                                              #
################################################################################


import time
import os
from IxNetwork import IxNet

ixNet = IxNet()

print ("Connecting to the server")
ixNet.connect('10.39.65.1', '-setAttribute', 'strict', '-port', 9861, '-version', '8.50')

print ("Cleaning up IxNetwork...")
ixNet.execute('newConfig')

root = ixNet.getRoot()

print ("\nAdd virtual ports to configuration...")
vports = []
vports.append(ixNet.add(root, 'vport'))
vports.append(ixNet.add(root, 'vport'))
ixNet.commit()

# get virtual ports
vports = ixNet.getList(ixNet.getRoot(), 'vport')

print ('Add chassis in IxNetwork...')
chassis = '10.39.64.117'
availableHardwareId = ixNet.getRoot()+'availableHardware'
ixNet.add(availableHardwareId, 'chassis', '-hostname', chassis)
ixNet.commit()

print ("Assigning ports from " + chassis + " to "+ str(vports) + " ...")
ixNet.setAttribute(vports[0], '-connectedTo', '/availableHardware/chassis:"10.39.64.117"/card:2/port:9')
ixNet.setAttribute(vports[1], '-connectedTo', '/availableHardware/chassis:"10.39.64.117"/card:2/port:10')
ixNet.commit()

time.sleep(5)
ixNet.execute('clearStats')

print "**************************************************************************************************"
print ('\n\nCreate  topology with PPPoX client and PPPoX Client.')
print "***************************************************************************************************"

print ('\nAdd topology...')
ixNet.add(root, 'topology')

print ('\nUse ixNet.commit() to commit added child under root.')
ixNet.commit()

print ('\nUse ixNet.getList to get newly added child under root.')
topS = ixNet.getList(root, 'topology')[0]

print ('Add virtual port to topology and change its name...')
ixNet.setMultiAttribute(topS, '-vports', vports[0], '-name', 'pppoxclient')
ixNet.commit()

print ('Add DeviceGroup for pppoxclient...')
ixNet.add(topS, 'deviceGroup')
ixNet.commit()
DG1 = ixNet.getList(topS, 'deviceGroup')[0]

print ('Create the pppoxclient stack in this DeviceGroup...')
print ('Add Ethernet layer...')
ixNet.add(DG1, 'ethernet')
ixNet.commit()
eth1 = ixNet.getList(DG1, 'ethernet')[0]

print ('Add PPPoX client layer...')
ixNet.add(eth1, 'pppoxclient')
ixNet.commit()
pppoxclient = ixNet.getList(eth1, 'pppoxclient')[0]

print ('Change each Device Group multipliers on server topology...')
ixNet.setAttribute(DG1, '-multiplier', 10)
ixNet.commit()


print ('Add topology...')
ixNet.add(root, 'topology')
ixNet.commit()
topC = ixNet.getList(root, 'topology')[1]

print ('\n\nCreate first topology with PPPoX Server...')

print ('Add virtual port to topology and change its name to PPPoX Server...')
ixNet.setMultiAttribute(topC, '-vports', vports[1], '-name', 'PPPoX Server')
ixNet.commit()

print ('Add DeviceGroup for pppoxserver...')
ixNet.add(topC, 'deviceGroup')
ixNet.commit()
DG2 = ixNet.getList(topC, 'deviceGroup')[0]

print ('Create the client stack in this DeviceGroup...')
print ('Add Ethernet layer...')
ixNet.add(DG2, 'ethernet')
ixNet.commit()
eth2 = ixNet.getList(DG2, 'ethernet')[0]

print ('Add pppoxserver layer...')
ixNet.add(eth2, 'pppoxserver')
ixNet.commit()
pppoxserver = ixNet.getList(eth2, 'pppoxserver')[0]

print ('Change each Device Group multipliers on server topology...')
ixNet.setAttribute(DG2, '-multiplier', 1)
ixNet.commit()

topC1 = ixNet.getList(root, 'topology')[0]
topS1 = ixNet.getList(root, 'topology')[1]

print ('\nFetch PPPox Client details.')
topology1 = ixNet.getList(root, 'topology')[0]
dg = ixNet.getList(topology1, 'deviceGroup')[0]
eth = ixNet.getList(dg, 'ethernet')[0]
pppox_client = ixNet.getList(eth, 'pppoxclient')[0]


print "***************************************************"
print ('\n\nSet values to ML-PPP Parameters for PPPoX Client..')
print "***************************************************"

print "1. Configure ML-PPP with ML-PPP Endpoint discriminator option as True"
end_point_negotiation = ixNet.getAttribute(pppox_client, '-endpointDiscNegotiation')
end_point_negotiation_val = ixNet.add(end_point_negotiation, 'singleValue')
ixNet.setMultiAttribute(end_point_negotiation_val,
    '-value', 'true')
ixNet.commit()

print "2. Configure ML-PPP with Enable MRRU Negotiation as true"
mrru_negotiation = ixNet.getAttribute(pppox_client, '-mrruNegotiation')
mrru_negotiation_val = ixNet.add(mrru_negotiation, 'singleValue')
ixNet.setMultiAttribute(mrru_negotiation_val,
    '-value', 'true')
ixNet.commit()

print "3. Configure ML-PPP with MAC address"
mlpp_mac_address        = ixNet.getAttribute(pppox_client, '-mlpppMACAddress')
mlpp_mac_address_val    = ixNet.add(mlpp_mac_address, 'counter')
ixNet.setMultiAttribute(mlpp_mac_address_val,
    '-step', '00:00:00:00:00:01',
    '-start', '10:11:01:00:00:01',
    '-direction', 'increment')
ixNet.commit()


print "4. Configure ML-PPP with IP address"
mlppp_ip_address = ixNet.getAttribute(pppox_client, '-mlpppIPAddress')
mlppp_ip_address_val = ixNet.add(mlppp_ip_address, 'counter')
ixNet.setMultiAttribute(mlppp_ip_address_val,
    '-step', '0.0.0.1',
    '-start', '10.1.1.2',
    '-direction', 'increment')
ixNet.commit()

print "5. Configure ML-PPP with End point discriminator class"
# Different End point discriminator class values are:
#a. ipaddress
#b. nullclass
#c. macaddress
end_point_disc = ixNet.getAttribute(pppox_client, '-endpointDiscriminatorClass')
end_point_disc_val = ixNet.add(end_point_disc, 'singleValue')
ixNet.setMultiAttribute(end_point_disc_val,
    '-value', 'nullclass')
ixNet.commit()

print "6. Configure ML-PPP with MRRU size"
mrru = ixNet.getAttribute(pppox_client, '-mrru')
mrru_val = ixNet.add(mrru, 'singleValue')
ixNet.setMultiAttribute(mrru_val,
    '-value', '1487')
ixNet.commit()



print "***************************************************"
print ('\n\nSet values to ML-PPP Parameters for PPPoX Server..')
print "***************************************************"

print "1. Configure ML-PPP with ML-PPP Endpoint discriminator option as True"
end_point_negotiation = ixNet.getAttribute(pppoxserver, '-endpointDiscNegotiation')
end_point_negotiation_val = ixNet.add(end_point_negotiation, 'singleValue')
ixNet.setMultiAttribute(end_point_negotiation_val,
    '-value', 'true')
ixNet.commit()

print "2. Configure ML-PPP with Enable MRRU Negotiation as true"
mrru_negotiation = ixNet.getAttribute(pppoxserver, '-mrruNegotiation')
mrru_negotiation_val = ixNet.add(mrru_negotiation, 'singleValue')
ixNet.setMultiAttribute(mrru_negotiation_val,
    '-value', 'true')
ixNet.commit()

print "3. Configure ML-PPP with MAC address"
mlpp_mac_address = ixNet.getAttribute(pppoxserver, '-mlpppMACAddress')
mlpp_mac_address_val = ixNet.add(mlpp_mac_address, 'counter')
ixNet.setMultiAttribute(mlpp_mac_address_val,
    '-step', '00:00:00:00:00:01',
    '-start', '10:11:01:00:00:01',
    '-direction', 'increment')
ixNet.commit()


print "4. Configure ML-PPP with IP address"
mlppp_ip_address = ixNet.getAttribute(pppoxserver, '-mlpppIPAddress')
mlppp_ip_address_val = ixNet.add(mlppp_ip_address, 'counter')
ixNet.setMultiAttribute(mlppp_ip_address_val,
    '-step', '0.0.0.1',
    '-start', '10.1.1.2',
    '-direction', 'increment')
ixNet.commit()

print "5. Configure ML-PPP with End point discriminator class"
end_point_disc = ixNet.getAttribute(pppoxserver, '-endpointDiscriminatorClass')
end_point_disc_val = ixNet.add(end_point_disc, 'singleValue')
ixNet.setMultiAttribute(end_point_disc_val,
    '-value', 'nullclass')
ixNet.commit()


print "6. Configure ML-PPP with MRRU size"
mrru = ixNet.getAttribute(pppoxserver, '-mrru')
mrru_val = ixNet.add(mrru, 'singleValue')
ixNet.setMultiAttribute(mrru_val,
    '-value', '1487')
ixNet.commit()

print ('\n\nStart topologies...')
ixNet.execute('start', topC1)
ixNet.execute('start', topS1)
time.sleep(30)
print ('\n\nStop topologies...')
ixNet.execute('stop',topC1)
ixNet.execute('stop', topS1)
time.sleep(30)

print ("\n\nCleaning up IxNetwork...")
ixNet.execute('newConfig')



