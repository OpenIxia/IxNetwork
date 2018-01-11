# ##############################################################################
# Version 1.0    $Revision: 1 $
# $Author: Alexandra Apetroaei
#    Copyright  1997 - 2014 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#
# ##############################################################################

# ##############################################################################
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
# ##############################################################################


# ##############################################################################
#                                                                              #
# Description:                                                                 #
#	 The script adds DHCPv6 Client protocol and configures TLVs on it.		   #
#	 Add a new TLV template. Add and modify TLVs and subTLVs in the template.  #
#	 Add the custom TLV from the new TLV template created previously. 		   #
#	 Add a new TLV from the default Template. Modify this TLV.				   #
#	 Delete TLVs.															   #
# Module:                                                                      #
#    The sample was tested on a 10GE LSM  module.                              #
#                                                                              #
# ##############################################################################

set PASSED 0
set FAILED 1

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return $FAILED
}

set port1 						11/1
set port2 						11/2
set test_name                   [info script]
set chassis_ip                  10.205.15.90
set ixnetwork_tcl_server        ixro-smqa-r-23
set port_list                   [list $port1 $port2]


set connect_status [::ixiangpf::connect                         \
    -reset         1                                            \
    -device                 $chassis_ip                         \
    -port_list              $port_list                          \
    -ixnetwork_tcl_server   $ixnetwork_tcl_server               \
]


ixNet setSessionParameter setAttribute loose
ixNet commit

set port_1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port_2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]
set port_handle [list $port_1 $port_2]

puts "Connected..."


# ######################## Topology 1 ############################
puts ""
puts "Creating topology..."

set topology_1_status [::ixiangpf::topology_config  \
        -topology_name      {Topology 1}			\
        -port_handle        $port_1                 \
    ]
if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $topology_1_status"
    return $FAILED
}
set topology_1_handle [keylget topology_1_status topology_handle]

# ############################ DG 1 #############################

puts ""
puts "Creating DG 1..."

set device_group_1_status [::ixiangpf::topology_config 		\
        -topology_handle              $topology_1_handle    \
        -device_group_name            {Device Group 1}      \
        -device_group_multiplier      10                    \
        -device_group_enabled         1                     \
    ]
if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $device_group_1_status"
    return $FAILED
}
set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

set multivalue_1_status [::ixiangpf::multivalue_config          \
        -pattern                counter                         \
        -counter_start          00.15.01.00.00.01               \
        -counter_step           00.00.00.00.00.01               \
        -counter_direction      increment                       \
        -nest_step              00.00.01.00.00.00               \
        -nest_owner             $topology_1_handle              \
        -nest_enabled           0                               \
    ]
if {[keylget multivalue_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $multivalue_1_status"
    return $FAILED
}
set multivalue_1_handle [keylget multivalue_1_status multivalue_handle]


puts ""
puts "Creating Ethernet 1 layer..."

set ethernet_1_status [::ixiangpf::interface_config 			 \
        -protocol_name                {Ethernet 1}               \
        -protocol_handle              $deviceGroup_1_handle      \
        -mtu                          1500                       \
        -src_mac_addr                 $multivalue_1_handle       \
        -vlan                         0                          \
        -vlan_id                      1                          \
        -vlan_id_step                 0                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
        -use_vpn_parameters           0                          \
        -site_id                      0                          \
]
if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $ethernet_1_status"
    return $FAILED
}
set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]


# ########################### DHCPv6 Client ###########################

puts ""
puts "Adding DHCPv6 Client 1 layer..."

set dhcp_1_status [::ixiangpf::emulation_dhcp_group_config    	\
		-handle                      	$ethernet_1_handle      \
		-mode                    		create        			\
		-dhcp_range_ip_type             ipv6        			\
		-dhcp6_range_duid_enterprise_id 15        				\
		-dhcp6_range_duid_type          duid_en        			\
		-dhcp6_range_duid_vendor_id     20        				\
		-dhcp6_range_duid_vendor_id_increment    2        		\
		-dhcp_range_renew_timer         10        				\
		-dhcp6_use_pd_global_address    1        				\
		-protocol_name                	"Ixia DHCPv6"    		\
		-dhcp6_range_ia_type        	iapd        			\
		-dhcp6_range_ia_t2            	40000        			\
		-dhcp6_range_ia_t1            	30000        			\
		-dhcp6_range_ia_id_increment    2        				\
		-dhcp6_range_ia_id            	20        				\
]

if {[keylget dhcp_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $dhcp_1_status"
    return $FAILED
}
set dhcpclient_1_handle [keylget dhcp_1_status dhcpv6client_handle]

puts ""
puts "# ############################## DHCPv6 Construct a new TLV template ##########"
puts ""

puts  "Create a custom Template for DHCPv6 Client."
set template_result [::ixiangpf::tlv_config			\
    -mode 	 				create_template_group	\
    -handle  				"/globals"				\
    -protocol 				dhcp6_client			\
    -template_group_name  	{My new custom template}\
]

if {[keylget template_result status] != $::SUCCESS} {
    puts "FAIL - [info script] - $template_result"
    return $FAILED
}

set template_handle [keylget template_result tlv_template_group_handle]

puts ""
puts  "Add a new TLV to the template created."
set tlv_result [::ixiangpf::tlv_config					\
    -mode		 				create_tlv 				\
    -handle						$template_handle 		\
    -tlv_name 					{Custom created TLV} 	\
    -tlv_description 			{This is my custom TLV created using the tlv_config HL command} \
    -tlv_is_repeatable 			0 						\
    -tlv_is_required 			1 						\
	-type_name					{Type of the TLV} 		\
    -length_name 				{Length of the TLV} 	\
    -length_description 		{Length description} 	\
    -length_encoding 			hex 					\
    -length_size 				2 						\
    -length_value 				2 						\
    -length_is_required 		1 						\
	-tlv_include_in_messages 	solicit 				\
]

if {[keylget tlv_result status] != $::SUCCESS} {
    puts "FAIL - [info script] - $tlv_result"
    return $FAILED
}

puts "Returned handles:"
ixia::keylprint tlv_result

set custom_tlv_handle [keylget tlv_result tlv_template_handle]
set tlv_value_handle [keylget tlv_result tlv_value_handle]
set tlv_type_handle [keylget tlv_result tlv_type_handle]
set tlv_length_handle [keylget tlv_result tlv_length_handle]

puts ""
puts  "Modify the new TLV."
set tlv_result [::ixiangpf::tlv_config				\
    -mode		 				modify 				\
    -handle						$custom_tlv_handle 		\
    -tlv_is_repeatable 			0 					\
    -tlv_is_required 			1 					\
	-tlv_include_in_messages 	{solicit release} 	\
] 

if {[keylget tlv_result status] != $::SUCCESS} {
    puts "FAIL - [info script] - $tlv_result"
    return $FAILED
}

puts ""
puts  "Create a new field under the type node."
set tlv_result [::ixiangpf::tlv_config				\
    -mode		 				create_field 		\
    -handle						$tlv_type_handle 	\
    -field_name 				{Code} 				\
    -field_description 			{Code description} 	\
    -field_encoding 			decimal 			\
    -field_size 				2 					\
    -field_value 				2 					\
    -field_is_required 			1 					\
    -field_is_repeatable 		0 					\
]

if {[keylget tlv_result status] != $::SUCCESS} {
    puts "FAIL - [info script] - $tlv_result"
    return $FAILED
}

puts "To display the returned handles use: ixia::keylprint tlv_result"

set type_field_handle [keylget tlv_result tlv_field_handle]

puts ""
puts  "Create a new field under for the value node."
set tlv_result [::ixiangpf::tlv_config					\
    -mode		 				create_field 			\
    -handle						$tlv_value_handle 		\
    -field_name 				{Value Field} 			\
    -field_description 			{Value Field description} \
    -field_encoding 			hex 					\
    -field_size 				2 						\
    -field_value 				160 					\
    -field_is_required 			1 						\
    -field_is_repeatable 		1 						\
]

if {[keylget tlv_result status] != $::SUCCESS} {
    puts "FAIL - [info script] - $tlv_result"
    return $FAILED
}

puts "Returned handles:"
ixia::keylprint tlv_result

set value_field_handle [keylget tlv_result tlv_field_handle]

puts ""
puts  "Create a subTLV under the newly created TLV. Use the tlv_value_handle."
set tlv_result [::ixiangpf::tlv_config					\
    -mode		 				create_tlv 				\
    -handle						$tlv_value_handle 		\
    -tlv_name 					{Custom created subTLV} \
    -tlv_description 			{This is my custom subTLV created using the tlv_config HL command} \
    -tlv_is_repeatable 			0 						\
    -tlv_is_required 			1 						\
	-type_name					{Type of the subTLV} 	\
    -length_name 				{Length of the subTLV} 	\
    -length_description 		{Length description} 	\
    -length_encoding 			hex 					\
    -length_size 				2 						\
    -length_value 				2 						\
    -length_is_required 		1 						\
]

puts "To display the returned handles use: ixia::keylprint tlv_result"
# status: 1
# subtlv_template_handle: /globals/topology/dhcpv6client/tlvEditor/template:1/tlv:1/value/object:2/subTlv
# tlv_value_handle: /globals/topology/dhcpv6client/tlvEditor/template:1/tlv:1/value/object:2/subTlv/value
# tlv_type_handle: /globals/topology/dhcpv6client/tlvEditor/template:1/tlv:1/value/object:2/subTlv/type
# tlv_length_handle: /globals/topology/dhcpv6client/tlvEditor/template:1/tlv:1/value/object:2/subTlv/length

set subtlv_handle [keylget tlv_result subtlv_template_handle]
set subtlv_value_handle [keylget tlv_result tlv_value_handle]
set subtlv_type_handle [keylget tlv_result tlv_type_handle]
set subtlv_length_handle [keylget tlv_result tlv_length_handle]

puts ""
puts  "Create a new container under the value node of the subTLV."
set tlv_result [::ixiangpf::tlv_config						\
    -mode		 				create_tlv_container 		\
    -handle						$subtlv_value_handle 		\
    -container_name 			{SubTLV Container} 			\
	-container_is_repeatable		1							\
]

puts "To display the returned handles use: ixia::keylprint tlv_result"

if {[keylget tlv_result status] != $::SUCCESS} {
    puts "FAIL - [info script] - $tlv_result"
    return $FAILED
}

set container_handle [keylget tlv_result tlv_container_handle]

puts ""
puts  "Create a new field under the new container of the subTLV."
set tlv_result [::ixiangpf::tlv_config					\
    -mode		 				create_field 			\
    -handle						$container_handle 		\
    -field_name 				{Value Field} 			\
    -field_description 			{Value Field description} \
    -field_encoding 			hex 					\
    -field_size 				2 						\
    -field_value 				160 					\
    -field_is_required 			1 						\
    -field_is_repeatable 		0 						\
]

if {[keylget tlv_result status] != $::SUCCESS} {
    puts "FAIL - [info script] - $tlv_result"
    return $FAILED
}

puts "To display the returned handles use: ixia::keylprint tlv_result"
set field_handle [keylget tlv_result tlv_field_handle]

puts ""
puts  "Modify the new field under the new container of the subTLV."
set tlv_result [::ixiangpf::tlv_config				\
    -mode		 				modify 				\
    -handle						$field_handle 		\
    -field_name 				{SubTLV Value Field}\
    -field_description 			{SubTLV Field description} \
    -field_encoding 			hex 				\
    -field_size 				4 					\
    -field_value 				2 					\
    -field_is_required 			1 					\
    -field_is_repeatable 		0 					\
]

if {[keylget tlv_result status] != $::SUCCESS} {
    puts "FAIL - [info script] - $tlv_result"
    return $FAILED
}

puts ""
puts "You have created a new TLV template that includes one TLV!!!!"
puts "The TLV contains the Type, Length and Value fields and another subTLV!!!!"
puts "The subTLV contains the Type, Length and a container with the Value field!!!!"
puts ""


puts "# ############################## Add TLVs to the DHCPv6Client protocol ##########"

puts ""
puts "Add TLVs on protocols."
puts "Add TLV 32 on DHCPv6Client."
set addTLV_result [::ixiangpf::tlv_config 	\
    -mode  			create_tlv				\
    -handle  		$dhcpclient_1_handle	\
    -protocol 		dhcp6_client			\
    -tlv_name 		32						\
	-tlv_include_in_messages request inform_req release renew rebind \
]

if {[keylget addTLV_result status] != $::SUCCESS} {
    puts "FAIL - [info script] - $addTLV_result"
    return $FAILED
}

puts "To display the returned handles use: ixia::keylprint addTLV_result"
# status: 1
# tlv_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:1
# tlv_value_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:1/value
# /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:1/value:
#  tlv_field_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:1/value/object:1/field
# tlv_type_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:1/type
# /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:1/type:
#  tlv_field_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:1/type/object:1/field
# tlv_length_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:1/length

set TLV_handle [keylget addTLV_result tlv_handle]
set tlv_value_handle [keylget addTLV_result tlv_value_handle]
set tlv_value_field_handle [keylget addTLV_result $tlv_value_handle.tlv_field_handle]
# set tlv_2_value_field_handle [keylget addTLV_result [keylget addTLV_result tlv_value_handle].tlv_field_handle]

puts ""
puts "Modifying the TLV 32 value."
set result [ixiangpf::tlv_config 	\
	-mode			modify			\
	-handle			$tlv_value_field_handle	\
	-field_value	100				\
]

if {[keylget result status] != $::SUCCESS} {
	return "FAIL - $test_name - [keylget connect_status log]"
    return $FAILED
}

puts ""
puts "Modifying the TLV 32 messages to be include in."
set result [ixiangpf::tlv_config 		\
	-mode			modify				\
	-handle			$TLV_handle		\
	-tlv_include_in_messages request 	\
]

if {[keylget result status] != $::SUCCESS} {
	return "FAIL - $test_name - [keylget connect_status log]"
    return $FAILED
}

puts ""
puts "Add TLVs on protocols. Add custom TLV."
puts "Add the custom TLV on DHCPv6Client."
set addTLV_result1 [::ixiangpf::tlv_config 	\
    -mode  			create_tlv				\
    -handle  		$dhcpclient_1_handle	\
    -protocol 		dhcp6_client			\
    -tlv_handle 	$custom_tlv_handle		\
]

# %  ixia::keylprint addTLV_result1
#status: 1
# tlv_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2
# tlv_value_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value
# /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value:
#  tlv_container_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value/object:1/repeatableContainer
#  /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value/object:1/repeatableContainer:
#   tlv_field_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value/object:1/repeatableContainer/object:1/field
#  subtlv_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value/object:2/subTlv
#  tlv_value_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value/object:2/subTlv/value
#  /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value/object:2/subTlv/value:
#   tlv_container_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value/object:2/subTlv/value/object:1/repeatableContainer
#   /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value/object:2/subTlv/value/object:1/repeatableContainer:
#    tlv_container_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value/object:2/subTlv/value/object:1/repeatableContainer/object:1/container
#    /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value/object:2/subTlv/value/object:1/repeatableContainer/object:1/container:
#     tlv_field_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value/object:2/subTlv/value/object:1/repeatableContainer/object:1/container/object:1/field
#  tlv_type_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value/object:2/subTlv/type
#  tlv_length_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/value/object:2/subTlv/length
# tlv_type_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/type
# /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/type:
#  tlv_field_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/type/object:1/field
# tlv_length_handle: /topology:1/deviceGroup:1/ethernet:1/dhcpv6client:1/tlvProfile/tlv:2/length

set TLV2_handle [keylget addTLV_result1 tlv_handle]

set tlv_value_handle [keylget addTLV_result1 tlv_value_handle]
set subtlv_value_handle [keylget addTLV_result1 $tlv_value_handle.tlv_value_handle]
set tlv_container_handle [keylget addTLV_result1 $tlv_value_handle.$subtlv_value_handle.tlv_container_handle]
set tlv_container_handle2 [keylget addTLV_result1 $tlv_value_handle.$subtlv_value_handle.$tlv_container_handle.tlv_container_handle]
set tlv_value_field_handle [keylget addTLV_result1 $tlv_value_handle.$subtlv_value_handle.$tlv_container_handle.$tlv_container_handle2.tlv_field_handle]

puts ""
puts "Modifying the field value for the subTLV in the custom TLV.."
set result [ixiangpf::tlv_config 	\
	-mode			modify			\
	-handle			$tlv_value_field_handle	\
	-field_value	555				\
]

if {[keylget result status] != $::SUCCESS} {
	return "FAIL - $test_name - [keylget connect_status log]"
    return $FAILED
}

puts ""
puts "You have added 2 TLVs to the DHCPv6 Client protocol!!!!"
puts ""



puts ""
puts "Delete the TLV."
set tlv_result [::ixiangpf::tlv_config	\
    -mode 		delete					\
    -handle 	$TLV_handle 			\
    -protocol	dhcp4_client			\
]

puts ""
puts "Delete the TLV."
set tlv_result [::ixiangpf::tlv_config	\
    -mode 		delete					\
    -handle 	$TLV2_handle 			\
    -protocol	dhcp4_client			\
]

puts ""
puts "Delete topology."
set topology_1_status [::ixiangpf::topology_config     	\
		-mode               destroy                     \
        -port_handle        $port_1              		\
		-topology_handle    $topology_1_handle          \
]

if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - [info script] - $topology_1_status"
    return $FAILED
}
puts ""
puts "!!! TEST END !!!"

