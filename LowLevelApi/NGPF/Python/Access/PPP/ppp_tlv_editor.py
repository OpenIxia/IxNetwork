#!/usr/bin/tclsh
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

################################################################################
#                                                                              #
# Description:                                                                 #
#    Script  will create following:                                            #
#    1. Create PPPoX Client                                                    #
#    2.	Setting DSL type in DSL line Attribute.                                #
#    3. Setting CUSTOM TLV in DSL Line Attribute..	     					   #
#  	 4. Setting 01 Access-Loop-Circuit-ID	   	   							   #
#	 5. Setting PON-Access-Line-Attributes                             		   #
#                                                                              #
################################################################################



import time
import os
from IxNetwork import IxNet

ixNet = IxNet()

print ("Connecting to the server")
ixNet.connect('10.39.64.169', '-setAttribute', 'strict', '-port', 8876, '-version', '9.00')

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
chassis = '10.39.65.151'
availableHardwareId = ixNet.getRoot()+'availableHardware'
ixNet.add(availableHardwareId, 'chassis', '-hostname', chassis)
ixNet.commit()

print ("Assigning ports from " + chassis + " to "+ str(vports) + " ...")
ixNet.setAttribute(vports[0], '-connectedTo', '/availableHardware/chassis:"10.39.65.151"/card:9/port:1')
ixNet.setAttribute(vports[1], '-connectedTo', '/availableHardware/chassis:"10.39.65.151"/card:9/port:2')
ixNet.commit()

time.sleep(5)
ixNet.execute('clearStats')

print "**************************************************************************************************"
print ('\n\nCreate  topology with PPPoX client and PPPoX Server \n\n')
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
print ('Add GPON as PON type TLV...')
get_pon_type_tlv = ixNet.getAttribute(pppoxclient, '-ponTypeTlv')
single_value = ixNet.add(get_pon_type_tlv, 'singleValue')
ixNet.setMultiAttribute(single_value,
                              '-value', 'gpon')
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

global_config = ixNet.getList(root, 'globals')[0]
global_top = ixNet.getList(global_config, 'topology')[0]
global_ppox = ixNet.getList(global_top, 'pppoxclient')[0]

print ('\nFetch PPPox Client details.')
topology1 = ixNet.getList(root, 'topology')[0]
dg = ixNet.getList(topology1, 'deviceGroup')[0]
eth = ixNet.getList(dg, 'ethernet')[0]
pppox_client = ixNet.getList(eth, 'pppoxclient')[0]

print ('\nFetch PPPox Client TLVs')
tlv_profile = ixNet.getList(pppox_client, 'tlvProfile')[0]
global_tlv_editor = ixNet.getList(global_ppox, 'tlvEditor')[0]

print ('\n\nGet global templates...')
global_default_template = ixNet.getList(ixNet.getList(global_tlv_editor, 'defaults')[0], 'template')[0]
print global_default_template
predefined_template = ixNet.getList(global_default_template, 'tlv')


print('''
# #############################################################################
#              Setting DSL type in DSL line Attribute..
# #############################################################################
''')
"""
This part is doing following:
1. Create DSL line Attribute TLV
2. It will search for sub tlv and put the object in req_tlv variable
3. Fetch required type TLV handle which corresponds to particular index value in sub tlv value handle list
4. Enable  DSL type sub tlv by enabling tlv_is_enabled parameter
5. Set value field for subtlv to 123
"""
dsl = 'DSL-Line-Attributes'
# Get DSL Line attribute TLV from many default templates
dsl_line_attribute = ixNet.getFilteredList(global_default_template, 'tlv', '-name', dsl)
ixNet.commit()
print "DSL Line attribute is :%s" % dsl_line_attribute

# Copy DSL Line attribute TLV template to tlv profile
dsl_line_attribute_tlv = ixNet.execute("copyTlv", tlv_profile, dsl_line_attribute)
ixNet.commit()
print "DSL Line attribute TLV is :%s" % dsl_line_attribute_tlv
parent_tlv_value = ixNet.getList(dsl_line_attribute_tlv, 'value')[0]
parent_tlv_object = ixNet.getList(parent_tlv_value, 'object')

# Searching for [84] Minimum-Net-Data-Rate-Downstream tlv and put the object in req_tlv variable
req_tlv = ""
tlv_name = ""
for obj in parent_tlv_object:
    dsl_tlv = "[84] Minimum-Net-Data-Rate-Downstream"
    obt_name = ixNet.getAttribute(obj, '-name')
    if obt_name == dsl_tlv:
        tlv_name = obt_name
        req_tlv = obj

sub_tlv = ixNet.getList(req_tlv, 'subTlv')[0]

# Enable sub tlv
ixNet.setMultiAttribute(sub_tlv, '-isEnabled', 'true')
ixNet.commit()

print ("\n\n Change the type for tlv name req_tlv to value 456 \n\n")
# Get sub-tlv value
dsl_type_tlv_value = ixNet.getList(sub_tlv, 'value')[0]
# Get Sub-tlv value object
dsl_type_tlv_obj = ixNet.getList(dsl_type_tlv_value, 'object')[0]
# Get Sub-Tlv field value
dsl_type_field = ixNet.getList(dsl_type_tlv_obj, 'field')[0]
dsl_type_tlv_field_value = ixNet.getAttribute(dsl_type_field, '-value')
dsl_counter_value = ixNet.add(dsl_type_tlv_field_value, 'counter')
# Modify field value for sub-tlv
ixNet.setMultiAttribute(dsl_counter_value,
                        '-step', '01',
                        '-start', '456',
                        '-direction', 'increment')
ixNet.commit()

print('''
# #############################################################################
#             Setting CUSTOM TLV in DSL Line Attribute
# #############################################################################
''')
"""
This part is doing following:
1. It will search for Custom Sub Tlv in  DSL Line Attribute and put the object in req_tlv variable
2. Fetch required custom TLV handle which corresponds to particular index value in sub tlv value handle list
3. Enable Custom sub tlv by enabling tlv_is_enabled parameter
4. Set value field for custom_sub_tlv to 123
5. Fetch custom tlv type handle
6. Fetching custom tlv type field handle
"""
# Searching for [00] Custom TLV  and put the object in req_tlv variable

req_tlv = ""
tlv_name = ""
for obj in parent_tlv_object:
    dsl_tlv = "[00] Custom TLV"
    obt_name = ixNet.getAttribute(obj, '-name')
    if obt_name == dsl_tlv:
        tlv_name = obt_name
        req_tlv = obj

sub_tlv = ixNet.getList(req_tlv, 'subTlv')[0]
# Enable sub tlv
ixNet.setMultiAttribute(sub_tlv, '-isEnabled', 'true')
ixNet.commit()

print "Change the Type for tlv name %s to value 12" % tlv_name
# Get sub-tlv type field value
tlv_type = ixNet.getList(sub_tlv, 'type')[0]
# Get Sub-tlv type field object
tlv_obj_val = ixNet.getList(tlv_type, 'object')[0]
# Get Sub-Tlv type field
obj_field_val = ixNet.getList(tlv_obj_val, 'field')[0]
# Modify field value for sub-tlv
obj_value = ixNet.getAttribute(obj_field_val, '-value')
obj_counter = ixNet.add(obj_value, 'counter')
ixNet.setMultiAttribute(obj_counter,
                        '-step', '01',
                        '-start', '12',
                        '-direction', 'increment')
ixNet.commit()

print "Change the Value for tlv name %s to value aabbccdd" % tlv_name
# Get sub-tlv value
tlv_value = ixNet.getList(sub_tlv, 'value')[0]
# Get Sub-tlv value object
tlv_obj_val = ixNet.getList(tlv_value, 'object')[0]
# Get Sub-Tlv value field
obj_field_val = ixNet.getList(tlv_obj_val, 'field')[0]
obj_value = ixNet.getAttribute(obj_field_val, '-value')
obj_counter = ixNet.add(obj_value, 'counter')
# Modify field value for sub-tlv value
ixNet.setMultiAttribute(obj_counter,
                        '-step', '01',
                        '-start', 'aabbccdd',
                        '-direction', 'increment')
ixNet.commit()


print('''
# #############################################################################
#             Setting 01 Access-Loop-Circuit-ID
# #############################################################################
''')
access_loop = "[01] Access-Loop-Circuit-ID"

print "Configure access_loop tlv %s" %access_loop
# Get Access-Loop-Circuit-ID TLV from many default templates
access_loop_circuit = ixNet.getFilteredList(global_default_template, 'tlv', '-name', access_loop)
ixNet.commit()
# Copy Access-Loop-Circuit-ID TLV template to tlv profile
access_loop_tlv = ixNet.execute("copyTlv", tlv_profile, access_loop_circuit)
ixNet.commit()
# Get tlv value
access_loop_tlv_value = ixNet.getList(access_loop_tlv, 'value')[0]
# Get tlv value object
access_loop_tlv_object = ixNet.getList(access_loop_tlv_value, 'object')[0]
# Get Tlv field value
access_loop_tlv_field = ixNet.getList(access_loop_tlv_object, 'field')[0]
access_loop_tlv_field_value = ixNet.getAttribute(access_loop_tlv_field, '-value')
access_loop_single_value = ixNet.add(access_loop_tlv_field_value, 'singleValue')

print("\n\n Change the value for tlv name %s to  circuit1" % access_loop)
ixNet.setMultiAttribute(access_loop_single_value, '-value', 'circuit1')
ixNet.commit()

print('''
# #############################################################################
#              Setting PON-Access-Line-Attributes..
# #############################################################################
''')
"""
# This part is doing following:
# 1. Create PON-Access-Line-Attributes TLV
# 2. It will search for [96] sub tlv  and put the object in req_tlv variable
# 3. Fetch required  [96] type TLV handle which corresponds to particular index value in sub tlv value handle list
# 4. Enable [96] type sub tlv by enabling tlv_is_enabled parameter
# 5. Set value field for [96] subtlv to 123345
"""

print "Creating PON-Access-Line-Attributes"
pon_attribute = 'PON-Access-Line-Attributes'
pon_attribute_data = ixNet.getFilteredList(global_default_template, 'tlv', '-name', pon_attribute)
ixNet.commit()
pon_attribute_tlv = ixNet.execute("copyTlv", tlv_profile, pon_attribute_data)
ixNet.commit()

parent_tlv_value = ixNet.getList(pon_attribute_tlv, 'value')[0]
parent_tlv_object = ixNet.getList(parent_tlv_value, 'object')

# Searching for [96] ONT/ONU-Assured-Data-Rate-Upstream tlv and put the object in req_tlv variable

req_tlv = ""
tlv_name = ""
for obj in parent_tlv_object:
    pon_tlv = "[96] ONT/ONU-Assured-Data-Rate-Upstream"
    obt_name = ixNet.getAttribute(obj, '-name')
    if obt_name == pon_tlv:
        tlv_name = obt_name
        req_tlv = obj

sub_tlv = ixNet.getList(req_tlv, 'subTlv')[0]
ixNet.setMultiAttribute(sub_tlv, '-isEnabled', 'true')
ixNet.commit()

print ("\n\n Change the value for tlv name %s to value 4561" % tlv_name)
ont_onu_tlv_value = ixNet.getList(sub_tlv, 'value')[0]
ont_onu_tlv_obj = ixNet.getList(ont_onu_tlv_value, 'object')[0]
ont_onu_field = ixNet.getList(ont_onu_tlv_obj, 'field')[0]
ont_onu_tlv_field_value = ixNet.getAttribute(ont_onu_field, '-value')

ont_onu_counter_value = ixNet.add(ont_onu_tlv_field_value, 'counter')
ixNet.setMultiAttribute(ont_onu_counter_value,
                        '-step', '01',
                        '-start', '4561',
                        '-direction', 'increment')
ixNet.commit()

print ('\n\nStart topologies...')
ixNet.execute('start', topC1)
ixNet.execute('start', topS1)
time.sleep(30)

print ('\n\nStop topologies...')
ixNet.execute('stop', topC1)
ixNet.execute('stop', topS1)
time.sleep(30)

print ("\n\nCleaning up IxNetwork...")
#ixNet.execute('newConfig')



