#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division

import os

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
# The script is not a standard commercial product offered by Ixia Keysight and #
# have     																	   #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia Keysight and/or by the user and/or by a third party)] shall at  #
# all times 																   #
# remain the property of Ixia Keysight.                                        #
#                                                                              #
# Ixia Keysight does not warrant (i) that the functions contained in the script#
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND Ixia Keysight#
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL Ixia Keysight BE LIABLE FOR ANY DAMAGES RESULTING FROM OR  #
# ARISING   																   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF Ixia Keysight HAS BEEN ADVISED OF THE          #
# POSSIBILITY OF  SUCH DAMAGES IN ADVANCE.                                     #
# Ixia Keysight will not be required to provide any software maintenance or    #
# support services of any kind (e.g. any error corrections) in connection with #
# script or any part thereof. The user acknowledges that although Ixia Keysight# 
# may     																	   #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia Keysight to  #
# provide any additional maintenance or support services.                      #
#                                                                              #
################################################################################

# ##############################################################################
# Description:                                                                 #
# This script will demonstrate Bonded GRE as per RFC 8157                      #
#     Script  will do following:                                               #
#    1. Load the config bonded_gre_sample_script.ixncfg                        #
#        Config has following:                                                 #
#        a. Config having HAAP side simulation pre configured                  #
#        b. Client side Bonded GRE will be configured in this sample           #
#    2.  Create Bonded GRE topology                                            #
#    3.  Create Link TLV {[77] Link Type]}                                     #
#        and custom TLV {[xx] Bonded GRE Custom TLV}                           #
#        These TLV 's are not mandatory to create                              #
#    4.  Start Protocol in following order as start all protocol not supported #
#        a. Start LTE Bonded GRE device group                                  #
#        b. Start DSL Bonded GRE device group                                  #
#        c. Start HAAP GRE   												   #
#		    d. Simulate control traffic after starting device group mentioned  #
#			in steps from (a to c) for LTE and DSL setup Accept message so that#
#			Bonded GRE to come up.                                             #
#        d. Start HAAP DHCP server                                             #
#        e. Start Home Gateway dhcp client                                     #
#    5. Create data traffic between HomeGateway DHCP Client to DHCP IPv4 Server#
#    6. Send Active Hello Notify packet from HAAP to Home Gateway.             #
#    7. Send right click actions like stop hello, resume hello, overflowLte    #
#    8. Check following session info state:                                    #
#       a. Bonded Gateway Session Info                                         #
#       b. Home Gateway Session Info 										   #
#	 9. Send LTE tear down control traffic from HAAP to HG  	               #
#    10. Stop and start Bonded GRE LTE after tear down                         #
#    11. Send Tear Down from Home Gateway to HAAP with error code 11           #
#    12. Check     Stats                                                       #
#    13. Stop Protocols                                                        #
#    14.Disable Tlv                                                            #
# Module:                                                                      #
#    The sample was tested on a 10GE LSM  module.                              #
#                                                                              #
# ##############################################################################

import time
import os
from IxNetwork import IxNet
ixNet = IxNet()


#####################################################################################
# Procedure : traffitem_enable_regenerate
# Purpose   : Enable the Traffic Item based on name and Regenerate traffic for that
# Parameters: ixNet, tItemName
#             ixNet - ixNetwork Instance
#             tItemName - Expected traffic Item Name which needs to be enabled and regenerated
# Return    :  flag
# error: -1
# ###################################################################################
def traffitem_enable_regenerate(ixNet, tItemName):
    root = ixNet.getRoot()
    traffic = ixNet.getList(root, 'traffic')[0]
    trafficItems = ixNet.getList(traffic, 'trafficItem')
    flag = 1
    for item in trafficItems:
        obt_name = ixNet.getAttribute(item, '-name')
        if obt_name == tItemName:
            ixNet.setAttribute(item, '-enabled', 'true')
            ixNet.commit()
            ixNet.execute('generate', item)
            flag = 0
    return flag


###############################################################################
# Procedure : traffitem_disable
# Purpose   : Disable the Traffic Item based on name
# Parameters: ixNet, tItemName
#             ixNet - ixNetwork Instance
#             tItemName - Expected traffic Item Name which needs to be Disabled
# Return    :  flag
# error: -1
# ##############################################################################
def traffitem_disable(ixNet, tItemName):
    root = ixNet.getRoot()
    traffic = ixNet.getList(root, 'traffic')[0]
    trafficItems = ixNet.getList(traffic, 'trafficItem')
    # print trafficItems
    flag = 1
    for item in trafficItems:
        obt_name = ixNet.getAttribute(item, '-name')
        if obt_name == tItemName:
            ixNet.setAttribute(item, '-enabled', 'false')
            ixNet.commit()
            flag = 0
    return flag


print ("Connecting to the server")
ixNet.connect('10.39.65.1', '-setAttribute', 'strict', '-port', 9862, '-version', '9.00')

print ("Cleaning up IxNetwork...")
ixNet.execute('newConfig')

config_file = "bonded_gre_sample_script.ixncfg"

print("Loading sample configuration " + config_file + "...")
ixNet.execute('loadConfig', ixNet.readFrom(config_file))
print("Successfully loaded .ixncfg file !!!")
root = ixNet.getRoot()

# get virtual ports
vports = ixNet.getList(ixNet.getRoot(), 'vport')
print ('Add chassis in IxNetwork...')
chassis = '10.39.64.117'
availableHardwareId = ixNet.getRoot()+'availableHardware'
ixNet.add(availableHardwareId, 'chassis', '-hostname', chassis)
ixNet.commit()
vport1 = vports[0]
vport2 = vports[1]
print ("Assigning ports from " + chassis + " to "+ str(vports) + " ...")
ixNet.setAttribute(vports[0], '-connectedTo', '/availableHardware/chassis:"10.39.64.117"/card:2/port:5')
ixNet.setAttribute(vports[1], '-connectedTo', '/availableHardware/chassis:"10.39.64.117"/card:2/port:6')
ixNet.commit()
time.sleep(5)

print("*************************************************************************************************")
print('\n\nCreate  Home Gateway topology \n\n')
print("*************************************************************************************************")

print ('\nAdding Home Gateway topology...')
hg_topology = ixNet.add(root, 'topology')
ixNet.setMultiAttribute(hg_topology,
                              '-name', 'Home Gateway',
                              '-ports', vport1)
print ('\nUse ixNet.commit() to commit added child under root.')
ixNet.commit()

print ('\n.........Adding Bonded GRE LTE...............')
lte_device = ixNet.add(hg_topology, 'deviceGroup')
ixNet.setMultiAttribute(lte_device,
                              '-multiplier', '1',
                              '-name', 'LTE Device Group')
ixNet.commit()

# Adding Bonded GRE LTE
print ('\nAdd Ethernet to LTE ...')
ethernet1 = ixNet.add(lte_device, 'ethernet')
ixNet.commit()
mac = ixNet.getAttribute(ethernet1, '-mac')
mac_val = ixNet.add(mac, 'counter')
ixNet.setMultiAttribute(mac_val,
                        '-step', '00:00:00:00:00:01',
                        '-start', '00:12:01:00:00:01',
                        '-direction', 'increment')
ixNet.commit()

print ('\nAdd ipv4 to LTE device')
ixNet.add(ethernet1, 'ipv4')
ixNet.commit()

ip1 = ixNet.getList(ethernet1, 'ipv4')[0]
mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvGw1 = ixNet.getAttribute(ip1, '-gatewayIp')

print ('\nconfiguring ipv4 addresses for LTE device ...')
ip_address = ixNet.add(mvAdd1, 'singleValue')
gateway_address = ixNet.add(mvGw1, 'singleValue')
ixNet.setMultiAttribute(ip_address, '-value', '1.1.1.1')
ixNet.setMultiAttribute(gateway_address, '-value', '1.1.1.101')
ixNet.commit()

print ('\nAdd GREoIPV4 in LTE device ...')
greoipv4 = ixNet.add(ip1, 'greoipv4')
ixNet.setMultiAttribute(greoipv4, '-name', 'GREoIPv4 2')
ixNet.commit()

print ('\nAdd DHCPv4 Client ...')
dhcpv4client = ixNet.add(greoipv4, 'dhcpv4client')
ixNet.setMultiAttribute(dhcpv4client, '-name', 'DHCPv4 Client 1')
ixNet.commit()

print ('\nAdd DHCPv4 Client in LTE device ...')
dhcpv4client_bgre = ixNet.getList(greoipv4, 'dhcpv4client')[0]
bonded_gre_lte = ixNet.add(greoipv4, 'bondedGRE')
ixNet.setMultiAttribute(greoipv4, '-name', 'LTE Bonded GRE"')
ixNet.commit()

# Adding Bonded GRE DSL
print ('\n.........Adding Bonded GRE DSL ...............')
dsl_device = ixNet.add(hg_topology, 'deviceGroup')
ixNet.setMultiAttribute(dsl_device,
                        '-multiplier', '1',
                        '-name', 'DSL Device Group')
ixNet.commit()

print ('\nAdd Ethernet to DSL device group...')
ethernet2 = ixNet.add(dsl_device, 'ethernet')
ixNet.commit()
mac = ixNet.getAttribute(ethernet2, '-mac')
mac_val = ixNet.add(mac, 'counter')
ixNet.setMultiAttribute(mac_val,
                        '-step', '00:00:00:00:00:01',
                        '-start', '00:14:01:00:00:01',
                        '-direction', 'increment')
ixNet.commit()

print ('\nAdd ipv4 to DSL device group ...')
ixNet.add(ethernet2, 'ipv4')
ixNet.commit()

ip2 = ixNet.getList(ethernet2, 'ipv4')[0]
mvAdd2 = ixNet.getAttribute(ip2, '-address')
mvGw2 = ixNet.getAttribute(ip2, '-gatewayIp')

print ('\nConfiguring ipv4 addresses for  DSL device group ...')
ip_address = ixNet.add(mvAdd2, 'singleValue')
gateway_address = ixNet.add(mvGw2, 'singleValue')
ixNet.setMultiAttribute(ip_address, '-value', '1.1.1.2')
ixNet.setMultiAttribute(gateway_address, '-value', '1.1.1.101')
ixNet.commit()

print ('\nAdd GREoIPV4 for  DSL device group')
greoipv4_dsl = ixNet.add(ip2, 'greoipv4')
ixNet.setMultiAttribute(greoipv4_dsl, '-name', 'GREoIPv4 2')
ixNet.commit()

bonded_gre_dsl = ixNet.add(greoipv4_dsl, 'bondedGRE')
print ('\n Modify tunnel type of DSL device group to DSL value')

ixNet.setMultiAttribute(bonded_gre_dsl,
                              '-tunnelType', 'dsl',
                              '-stackedLayers', [],
                              '-name', 'DSL Bonded GRE')
ixNet.commit()

# Fetching HAAP device group details
haap_topo = ixNet.getList(root, 'topology')[0]
deviceGroup_haap = ixNet.getList(haap_topo, 'deviceGroup')[0]
ethernet_haap = ixNet.getList(deviceGroup_haap, 'ethernet')[0]
ipv4_haap = ixNet.getList(ethernet_haap, 'ipv4')[0]
greoipv4 = ixNet.getList(ipv4_haap, 'greoipv4')[0]
dhcpip = ixNet.getList(greoipv4, 'ipv4')[0]
dhcpv4server = ixNet.getList(dhcpip, 'dhcpv4server')[0]

# print handles
print("\n Bonded GRE LTE handle is : %s" % bonded_gre_lte)
print("\n Bonded GRE DSL handle is : %s" % bonded_gre_dsl)
print("\n GRE Home gateway handle is : %s" % greoipv4)
print("\n GRE HAAP handle is : %s" % greoipv4)
print("\n HomeGateway DHCP client handle  is : %s" % dhcpv4client_bgre)
print("\n HAAP DHCP server handle  is : %s" % dhcpv4server)
print("\n HAAP DHCPv4 Server IP handle is :  %s" % dhcpip)

print ('\nGet Global templates ...')
global_config = ixNet.getList(root, 'globals')[0]
global_top = ixNet.getList(global_config, 'topology')[0]
global_bgre = ixNet.getList(global_top, 'bondedGRE')[0]
global_tlv_editor = ixNet.getList(global_bgre, 'tlvEditor')[0]
global_tlv_default = ixNet.getList(global_tlv_editor, 'defaults')[0]
global_template = ixNet.getList(global_tlv_default, 'template')[0]
print("\nGlobal Template is :  %s" % global_template)

print("*************************************************************************************************")
print('\n\n Add Link and custom TLV in LTE \n\n')
print("*************************************************************************************************")

print("\n 1. Creating Link TLV ")

link_value = '[77] Link Type'
tlv_profile = ixNet.getList(bonded_gre_lte, 'tlvProfile')
print("\n TLV profile is :  %s" % tlv_profile)

# Get Link Type TLV from many default templates
tlv_list = ixNet.getFilteredList(global_template, 'tlv', '-name', link_value)[0]
ixNet.commit()

name = ixNet.getAttribute(tlv_list, '-name')

# Copy Link Type TLV template to tlv profile
link_type_tlv = ixNet.execute("copyTlv", tlv_profile, tlv_list)
ixNet.commit()

print("\n 2. Creating custom TLV with Type , Length and Value")
custom_tlv = '[xx] Bonded GRE Custom TLV'

# Get Custom Type TLV from many default templates
tlv_list = ixNet.getFilteredList(global_template, 'tlv', '-name', custom_tlv)
ixNet.commit()

# Copy Custom Type TLV template to tlv profile
custom_type_tlv = ixNet.execute("copyTlv", tlv_profile, tlv_list)
ixNet.commit()


# Get Custom type field value
tlv_val = ixNet.getList(custom_type_tlv, 'type')[0]
# Get Custom type field object
tlv_obj_val = ixNet.getList(tlv_val, 'object')[0]
# Get Custom type field
obj_field_val = ixNet.getList(tlv_obj_val, 'field')[0]

# Modify field value for sub-tlv
obj_value = ixNet.getAttribute(obj_field_val, '-value')
obj_counter = ixNet.add(obj_value, 'counter')
ixNet.setMultiAttribute(obj_counter,
                        '-step', '01',
                        '-start', '12',
                        '-direction', 'increment')
ixNet.commit()


print("\n Change the Value for tlv name %s to value aabbccdd" % custom_tlv)
# Get Custom value
tlv_value = ixNet.getList(custom_type_tlv, 'value')[0]
# Get Custom value object
tlv_obj_val = ixNet.getList(tlv_value, 'object')[0]
# Get Custom value field
obj_field_val = ixNet.getList(tlv_obj_val, 'field')[0]
obj_value = ixNet.getAttribute(obj_field_val, '-value')
obj_counter = ixNet.add(obj_value, 'counter')
# Modify field value for custom-tlv value
ixNet.setMultiAttribute(obj_counter,
                        '-step', '01',
                        '-start', 'aabbccdd',
                        '-direction', 'increment')
ixNet.commit()

print("*************************************************************************************************")
print('\n Starting Protocols \n')
print("*************************************************************************************************")


print("\n 1. Starting LTE Bonded GRE protocols")
ixNet.execute('start', bonded_gre_lte)

print("\n 2. Starting DSL Bonded GRE protocols")
ixNet.execute('start', bonded_gre_dsl)

print("\n 3. Starting HAAP GRE")
ixNet.execute('start', greoipv4)

time.sleep(15)
traffic = ixNet.getList(root, 'traffic')[0]

print('\n Making LTE up by sending traffic for LTE \n')
lte_setup_accept = "LTE setup Accept - All attributes"
traffitem_enable_regenerate(ixNet, lte_setup_accept)
print('Apply traffic...')
ixNet.execute('apply', traffic)
print('Starting traffic...')
ixNet.execute('start', traffic)
time.sleep(10)
print("Disable LTE setup accept traffic items")
traffitem_disable(ixNet, lte_setup_accept)


print('\n Making dsl tunnel up by sending traffic for  DSL setup Accept message \n')
dsl_setup_accept = "DSL Setup Accept - All attributes"
traffitem_enable_regenerate(ixNet, dsl_setup_accept)
print('Apply traffic...')
ixNet.execute('apply', traffic)
print('Starting traffic...')
ixNet.execute('start', traffic)
time.sleep(10)
print("Disable DSL setup accept traffic items")
traffitem_disable(ixNet, dsl_setup_accept)

print ("Fetching all BondedGRE per port Stats\n")
viewPage = '::ixNet::OBJ-/statistics/view:"BondedGRE Per Port"/page'
statcap = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues'):
    for statVal in statValList:
        print("***************************************************")
        index = 0
        for satIndv in statVal:
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")

print("\n 4. Starting Home Gateway dhcp Server")
ixNet.execute('start', dhcpv4server)

print("\n 5. Starting Home Gateway dhcp client")
ixNet.execute('start', dhcpv4client_bgre)
time.sleep(5)

print("\n Creating Traffic from Home Gateway DHCP client to DHCP Server IPV4")
ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.commit()
ti1 = ixNet.getList(ixNet.getRoot() + '/traffic', 'trafficItem')[4]
ixNet.setMultiAttribute(ti1, '-name', 'LTE-DHCP-HG-HAAP')
ixNet.commit()
ixNet.setAttribute(ti1, '-trafficType', 'ipv4')
ixNet.commit()

ep = ixNet.add(ti1, 'endpointSet')
ixNet.setMultiAttribute(ep,
			'-scalableSources', [],
			'-sources', dhcpv4client_bgre,
			'-fullyMeshedEndpoints', [],
			'-multicastDestinations', [],
			'-destinations', dhcpip,
			'-scalableDestinations', [],
			'-multicastReceivers', [],
			'-ngpfFilters', [],
			'-trafficGroups', [],
			'-name', 'ep-set1')
ixNet.commit()

# Track flows by Ethernet Src , Etnernet Dest, Ipv4 Src, Ipv4 Dest Address
ixNet.setMultiAttribute(ti1+'/tracking', '-trackBy', ['ethernetIiSourceaddress0','sourceDestEndpointPair0',\
                                                      'trackingenabled0','ipv4DestIp0','ipv4SourceIp0',\
                                                      'ipv4SourceIp0','ethernetIiDestinationaddress0'])
ixNet.commit()

print('Apply traffic...')
ixNet.execute('apply', traffic)

print('Starting traffic...')
ixNet.execute('start', traffic)
time.sleep(5)
print ("Fetching all BondedGRE per port Stats\n")
viewPage = '::ixNet::OBJ-/statistics/view:"Flow Statistics"/page'
statcap = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues'):
    for statVal in statValList:
        print("***************************************************")
        index = 0
        for satIndv in statVal:
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")
print('Stop traffic...')
ixNet.execute('stop', traffic)
time.sleep(2)

lte_traffic_home_gateway_haap= "LTE-DHCP-HG-HAAP"
print("Disable traffic from Home Gateway DHCP client to DHCP Server IPV4s")
traffitem_disable(ixNet, lte_traffic_home_gateway_haap)

print('''
# #############################################################################
#       Send right click actions for Overflow lte, Stop Hello and resume hello""
# #############################################################################
''')
'''
Similar command can be used for all right click actions like:
Diag:Bonding tunnel start, Diag:DSL tunnel start, Diag:LTE tunnel Start, Diag: End Diagnostics
Switch To DSL tunnel, DSL link failure, LTE link failure
'''
print("\n Sending Stop hello")
ixNet.execute('stophello', bonded_gre_lte, '1')
time.sleep(5)
stop_hello_info = ixNet.getAttribute(bonded_gre_lte, '-bSessionInfo')
print("\n Bonded GRE info after stop hello is %s:" % stop_hello_info)

print("\n Sending Resume hello")
ixNet.execute('resumehello', bonded_gre_lte, '1')
time.sleep(5)
resume_hello_info = ixNet.getAttribute(bonded_gre_lte, '-bSessionInfo')
print("\n Bonded GRE info after resume hello is %s:" % resume_hello_info)

print("\n Sending overflowLte")
ixNet.execute('overflowLte', bonded_gre_lte, '1')
time.sleep(2)
hgateway_info = ixNet.getAttribute(bonded_gre_lte, '-homeGatewayInfo')
print("\n Home Gateway info after sending right click action is %s:" % hgateway_info)

print ("Fetching all BondedGRE per port Stats\n")
viewPage = '::ixNet::OBJ-/statistics/view:"BondedGRE Per Port"/page'
statcap = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues'):
    for statVal in statValList:
        print("***************************************************")
        index = 0
        for satIndv in statVal:
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")

print('''
# #############################################################################
#       Verify the behavior when tear down is received by Home Gateway from HAAP
# #############################################################################
''')
# As per RFC 8157 LTE tear down from HAAP with error code 01 is sent to home gateway
print("Enabling traffic for  LTE tear down with error code 01")
lte_teardown_error = "LTE-Teardowncode01"
traffitem_enable_regenerate(ixNet, lte_teardown_error)

print('Apply traffic...')
ixNet.execute('apply', traffic)

print('Starting traffic...')
ixNet.execute('start', traffic)
time.sleep(5)
# Get Bonded GRE session Info for tear down
bgre_session_info = ixNet.getAttribute(bonded_gre_lte, '-bSessionInfo')
print("\n Bonded GRE session Info for tear down is %s:" % bgre_session_info)

# Get Error Code for tear down
error_code = ixNet.getAttribute(bonded_gre_lte, '-errorCode')
print("\n Error Code for tear down is: %s" % error_code)

print("Disable traffic for LTE tear down")
traffitem_disable(ixNet, lte_teardown_error)


print("\n Stop LTE Bonded GRE protocols and start again...")
ixNet.execute('stop', bonded_gre_lte)
ixNet.execute('start', bonded_gre_lte)
time.sleep(3)

print('\n Making LTE up by sending traffic for LTE \n')
lte_setup_accept = "LTE setup Accept - All attributes"
traffitem_enable_regenerate(ixNet, lte_setup_accept)
print('Apply traffic...')
ixNet.execute('apply', traffic)
print('Starting traffic...')
ixNet.execute('start', traffic)
time.sleep(10)
print("Disable LTE setup accept traffic items")
traffitem_disable(ixNet, lte_setup_accept)

print('''
# #############################################################################
#       Send LTE tear down traffic from Homegateway to HAAP
# #############################################################################
''')
ixNet.execute('teardown', bonded_gre_lte, '11', '1')
time.sleep(2)
teardown_home_info = ixNet.getAttribute(bonded_gre_lte, '-homeGatewayInfo')
print("\nHomeGateway after Tear down from Homegateway to HAAP %s:" % teardown_home_info)

teardown_info = ixNet.getAttribute(bonded_gre_lte, '-bSessionInfo')
print("\nBonded GRE info after Tear down from Homegateway to HAAP %s:" % teardown_info)

print ('Stopping protocols')
ixNet.execute('stopAllProtocols')
time.sleep(10)

print('''
# #############################################################################
#       Disable Link and custom TLV
# #############################################################################
''')

# Get TLV profile list
tlv_profile_list = ixNet.getList(bonded_gre_lte, 'tlvProfile')[0]
tlv = ixNet.getList(tlv_profile_list, 'tlv')

# Disable each tlv by making -isEnabled parameter False
for tlv_l in tlv:
    ixNet.setMultiAttribute(tlv_l, '-isEnabled', 'false')
    ixNet.commit()

print ("\n\nCleaning up IxNetwork...")
ixNet.execute('newConfig')
print ("\n\nDisconnect IxNetwork...")
ixNet.disconnect()
print ('!!! Test Script Ends !!!')
