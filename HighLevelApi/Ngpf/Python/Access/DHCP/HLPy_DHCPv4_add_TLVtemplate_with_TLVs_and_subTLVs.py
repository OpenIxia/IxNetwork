################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Vlad Mihai
#    Copyright 1997 - 2014 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
# Description:                                                                 #
#	 The script adds DHCPv4 Client protocol and configures TLVs on it.		   #
#	 Add a new TLV template. Add and modify TLVs and subTLVs in the template.  #
#	 Delete TLVs and template.												   #
#																			   #
# Module:                                                                      #
#    The sample was tested on a 10GE LSM  module.                              #
#                                                                              #
################################################################################


# HARNESS VARS ****************************************************************

if 'py' not in dir():
    class TestFailedError(Exception): pass
    class Py: pass

py = Py()
py.ports = [('ixro-hlt-xm2-08', 2, 1), ('ixro-hlt-xm2-08', 2, 2)]
py.ixTclServer = 'localhost'
py.ixTclPort = 8009

# END HARNESS VARS ************************************************************


import sys, os
import time, re

sys.path.append('C:/Program Files (x86)/Ixia/hltapi/4.95.117.27/TclScripts/lib/hltapi/library/common/ixiangpf/python')
sys.path.append('C:/Program Files (x86)/Ixia/IxNetwork/7.40.0.319-EB/API/Python')

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError

ixiatcl 	= IxiaTcl()
ixiatcl 	= IxiaTcl()
ixiahlt 	= IxiaHlt(ixiatcl)
ixiangpf 	= IxiaNgpf(ixiahlt)

try:
    ixnHLT_errorHandler('', {})
except (NameError,):
    def ixnHLT_errorHandler(cmd, retval):
        global ixiatcl
        err = ixiatcl.tcl_error_info()
        log = retval['log']
        additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
        raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)

# CONNECTION VARS

port1                  =     str(py.ports[0][1])+str('/')+str(py.ports[0][2])
port2                  =     str(py.ports[1][1])+str('/')+str(py.ports[1][2])
chassis_ip             =     py.ports[0][0]
tcl_server             =     chassis_ip
ixnetwork_tcl_server   =     str(py.ixTclServer) + ':' + str(py.ixTclPort)
port_list              =     [port1, port2]

# END CONNECTION VARS

# #############################################################################
#                               CONNECT AND PORT HANDLES
# #############################################################################

print('\n\nConnect to IxNetwork Tcl Server and get port handles...\n\n')

connect_status = ixiangpf.connect(
    reset                  = 1,
    vport_count = 2,
    ixnetwork_tcl_server   = ixnetwork_tcl_server,
    tcl_server             = chassis_ip,
)
if connect_status['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('connect', connect_status)

port_handle = connect_status['vport_list']

port_0 = port_handle.split(' ')[0]
port_1 = port_handle.split(' ')[1]

print ('''
# #############################################################################
#                               DHCPv4 Client CONFIG
# #############################################################################
''')

# CREATE TOPOLOGY 1

print('\n\nConfigure DHCPv4 client stack ...\n\n')

topology_1_status =ixiangpf.topology_config(
    topology_name = 'Topology 1',
    port_handle = port_0,
)

if topology_1_status['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('topology_config', topology_1_status)

topology_1_handle = topology_1_status['topology_handle']

# CREATE DEVICE GROUP 1

device_group_1_status = ixiangpf.topology_config(
    topology_handle          =    topology_1_handle,
    device_group_name        =   'DHCPv4 Client',
    device_group_multiplier  =    '50',
    device_group_enabled     =    '1',
)
if device_group_1_status['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('topology_config', device_group_1_status)

device_1_handle = device_group_1_status['device_group_handle']

# CREATE ETHERNET STACK FOR DHCPv4 Client 1

multivalue_11 = ixiangpf.multivalue_config(
    pattern              =  'counter',
    counter_start        =  '00.11.01.00.00.01',
    counter_step         =  '00.00.00.00.00.01',
    counter_direction    =  'increment',
    nest_step            =  '00.00.01.00.00.00',
    nest_owner           =  topology_1_handle,
    nest_enabled         =  '1',
)
if multivalue_11['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('multivalue_config', multivalue_11)

multivalue_11_handle = multivalue_11['multivalue_handle']

ethernet_1_status = ixiangpf.interface_config(
    protocol_name           =     'Ethernet 1',
    protocol_handle         =     device_1_handle,
    mtu                     =     '1500',
    src_mac_addr            =     multivalue_11_handle,
    vlan                    =     '1',
    vlan_id                 =     '101',
    vlan_id_step            =     '0',
    vlan_id_count           =     '1',
    vlan_tpid               =     '0x8100',
    vlan_user_priority      =     '0',
    vlan_user_priority_step =     '0',
    use_vpn_parameters      =     '0',
    site_id                 =     '0',
)
if ethernet_1_status['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('interface_config', ethernet_1_status)

ethernet_1_handle = ethernet_1_status['ethernet_handle']

print ('''
# #############################################################################
#                                DHCPv4 CLIENT
# #############################################################################
''')

dhcp_status = ixiangpf.emulation_dhcp_group_config(
        handle                      =   ethernet_1_handle    ,
        dhcp_range_ip_type          =   'ipv4'                       ,
        use_rapid_commit            =   '0'                          ,
)
if dhcp_status['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('emulation_dhcp_group_config', dhcp_status)

dhcp_client_handle = dhcp_status['dhcpv4client_handle']

print ('''
# #############################################################################
#                                DHCPv4 Construct a new TLV template
# #############################################################################
''')

print ("create a template")

template_result = ixiangpf.tlv_config(
    mode 				= "create_template_group",
    handle 				= '/globals',
    protocol 			= 'dhcp4_client',
    template_group_name = "custom_template"
)

if template_result['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('tlv_config', template_result)

template_handle = template_result['tlv_template_group_handle']


print ('''
# #############################################################################
#                               1. Add a TLV
# #############################################################################
''')

print ("Add a TLV")

tlv_result = ixiangpf.tlv_config(
	mode 					= "create_tlv",
	handle 					= template_handle,
	protocol 				= 'dhcp4_client',
	tlv_name 				= "custom tlv",
	tlv_description 		= "This is my custom TLV",
	tlv_is_required 		= "1",
	tlv_is_editable     	= "1",
	type_name               = "Type",
	type_is_editable        = 1,
	length_name 			= "lenght",
	length_description 		= "length description",
	length_encoding 		= "hex",
	length_size 			= 2,
	length_value 			= 2,
	length_is_required 		= 1,
	length_is_editable      = 1,
	length_is_enabled 		= 1,
	tlv_include_in_messages = ["disco"],
)

if tlv_result['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('tlv_config', tlv_result)

tlv_handle 			= tlv_result['tlv_template_handle']
tlv_value_handle 	= tlv_result['tlv_value_handle']
tlv_type_handle 	= tlv_result['tlv_type_handle']
tlv_length_handle 	= tlv_result['tlv_length_handle']


print ('''
# #############################################################################
#                              2.  Modify the TLV
# #############################################################################
''')

tlv_result = ixiangpf.tlv_config(
   mode 					= "modify",
   handle 					= tlv_handle,
   tlv_name	 				= "custom tlv 1",
   tlv_description 			= "Custom TLV no 1",
   tlv_is_repeatable 		= "0",
   tlv_is_required 			= "0",
   tlv_include_in_messages 	= ["disco", "Request"],
)

if tlv_result['status'] != IxiaHlt.SUCCESS:
   ixnHLT_errorHandler('tlv_config', tlv_result)
   
print ('''
# #############################################################################
#                              3.  Modify the TLVs type
# #############################################################################
''')

print ("Modify type name")
tlv_result = ixiangpf.tlv_config(
	mode 		= "modify",
	handle 		= tlv_type_handle,
	type_name 	= "Type of TLV",
	)

if tlv_result['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('tlv_config', tlv_result)

print ("Add a new field under the type node.")
tlv_result = ixiangpf.tlv_config(
	mode 				= "create_field",
	handle 				= tlv_type_handle,
	field_name 			= "Type field",
	field_description 	= "Type field description",
	field_encoding 		= "hex",
	field_size 			= 2,
	field_value 		= 160,
	field_is_required 	= 1,
	field_is_repeatable = 0,
	field_is_editable   = 0,
)

if tlv_result['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('tlv_config', tlv_result)

field_handle = tlv_result['tlv_field_handle']

	
print ('''  
# #############################################################################
#                             4.   Modify length
# #############################################################################
''')

 
print("modify the parameters for the length and check the new values")
tlv_result = ixiangpf.tlv_config(
	mode 				= "modify",
	handle 				= tlv_length_handle,
	length_name 		= "lenght1",
	length_description 	= "length description1",
	length_encoding 	= "decimal",
	length_size 		= 3,
	length_value 		= 3,
	length_is_required 	= 0,
)

if tlv_result['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('tlv_config', tlv_result)

print('''
# #############################################################################
#                             5.   Create field under value
# #############################################################################
''')

print ("Create a new field under the value node.")

tlv_result = ixiangpf.tlv_config(
    mode 				= "create_field",
    handle	 			= tlv_value_handle,
    field_name 			= "custom_name",
    field_description 	= "custom description",
    field_encoding 		= "hex",
    field_size 			= 2,
    field_value 		= 160,
    field_is_required 	= 0,
)

if tlv_result['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('tlv_config', tlv_result)

field_handle = tlv_result['tlv_field_handle']


print('''
# #############################################################################
#                             6.  Create a new container
# #############################################################################
''') 

print ("Create a new container under the value node.")

tlv_result = ixiangpf.tlv_config(
	mode 					= "create_tlv_container",
	handle 					= tlv_value_handle,
	protocol 				= "dhcp4_client",
	container_name 			= "custom_name_4",
	container_description	= 'container description',
	container_is_required	= 1,
	container_is_editable	= 1,
	container_is_repeatable	= 1,	
)

if tlv_result['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('tlv_config', tlv_result)

container_handle = tlv_result['tlv_container_handle']


print('''
# #############################################################################
#                          7.  create a new tlv under the previous tlv (subtlv)
# #############################################################################
''')

print ("Create a new tlv under the value node.")

tlv_result = ixiangpf.tlv_config(
    mode 				= "create_tlv",
    handle 				= container_handle,
    protocol 			= 'dhcp4_client',
    tlv_name 			= "custom_tlv2",
    tlv_description 	= "This is my custom TLV_0",
    tlv_is_repeatable 	= "1",
    tlv_is_required 	= "1",
    length_name 		= "lenght",
    length_description 	= "length description",
    length_encoding 	= "hex",
    length_size 		= 2,
    length_value 		= 2,
    length_is_required 	= 1,
)

if tlv_result['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('tlv_config', tlv_result)
	
subtlv_handle 			= tlv_result['subtlv_template_handle']
subtlv_type_handle 		= tlv_result['tlv_type_handle']
subtlv_length_handle	= tlv_result['tlv_length_handle']
subtlv_value_handle 	= tlv_result['tlv_value_handle']

print('''
# #############################################################################
#                           8.    create a new field in the sub-tlv
# #############################################################################
''')

print ("Create a new field under the value node.")

tlv_result = ixiangpf.tlv_config(
    mode 				= "create_field",
    handle 				= subtlv_value_handle,
    field_name 			= "custom_name",
    field_description 	= "custom description",
    field_encoding 		= "hex",
    field_size 			= 2,
    field_value 		= 160,
    field_is_required 	= 1,
    field_is_repeatable = 1,
)

if tlv_result['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('tlv_config', tlv_result)

field_handle = tlv_result['tlv_field_handle']

   
print('''
# #############################################################################
#                            9.   remove the tlv
# #############################################################################
''')

print ("Remove the tlv from the template.")

template_result = ixiangpf.tlv_config(
    mode 		= "delete",
    handle 		= tlv_handle,
    protocol 	= 'dhcp4_client',
)

print('''
# #############################################################################
#                           10.    remove the template
# #############################################################################
''')

print ("Remove the template from the protocol.")

template_result = ixiangpf.tlv_config(
    mode 		= "delete",
    handle 		= template_handle,
    protocol 	= 'dhcp4_client',
)

print('''
# #############################################################################
#                           11.    CLEANUP SESSION
# #############################################################################
''')

cleanup_status = ixiangpf.cleanup_session(reset='1')
if cleanup_status['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('cleanup_session', cleanup_status)

print('\n\nIxNetwork session is closed...\n\n')
print('!!! TEST is PASSED !!!')


