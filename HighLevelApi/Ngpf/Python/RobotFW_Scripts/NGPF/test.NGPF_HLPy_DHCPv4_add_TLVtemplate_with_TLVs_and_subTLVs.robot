*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.147/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.147/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.132.206
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	6/7  6/8
${client_and_port} =  ${client}:${client_api_port}


*** Test Cases ***
test
################################################################################
# START - Connect to the chassis and get port handles from the result
################################################################################
	
	${result} =  Connect  reset=1  device=${chassis}  ixnetwork_tcl_server=${client_and_port}  port_list=@{portlist}  username=ixiaHLTQA  break_locks=1  interactive=1
	${connect_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${connect_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	
# #############################################################################
#                               DHCPv4 Client CONFIG
# #############################################################################

 ####################### Create Topologies ################################
	Log To Console  Configure DHCPv4 client stack ...
# CREATE TOPOLOGY 1
	${result} =  Topology Config  topology_name=Topology 1  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
# CREATE DEVICE GROUP 1
	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name=DHCPv4 Client  device_group_multiplier=50  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${device_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# CREATE ETHERNET STACK FOR DHCPv4 Client 1
	
	${result} =  Multivalue Config  pattern=counter  counter_start=00.11.01.00.00.01  counter_step=00.00.00.00.00.01  counter_direction=increment  nest_step=00.00.01.00.00.00  nest_owner=${topology_1_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_11_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Interface Config  protocol_name=Ethernet 1  protocol_handle=${device_1_handle}  mtu=1500  src_mac_addr=${multivalue_11_handle}  vlan=1  vlan_id=101  vlan_id_step=0  vlan_id_count=1  vlan_tpid=0x8100  vlan_user_priority=0  vlan_user_priority_step=0  use_vpn_parameters=0  site_id=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle

# #############################################################################
#                                DHCPv4 CLIENT
# #############################################################################

	${result} =  Emulation Dhcp Group Config  handle=${ethernet_1_handle}  dhcp_range_ip_type=ipv4  use_rapid_commit=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_client_handle} =  Get From Dictionary  ${result}  dhcpv4client_handle
	
# #############################################################################
#                                DHCPv4 Construct a new TLV template
# #############################################################################
	
	Log To Console  Create a template
	${result} =  Tlv Config  mode=create_template_group  handle=/globals  protocol=dhcp4_client  template_group_name=custom_template
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${template_handle} =  Get From Dictionary  ${result}  tlv_template_group_handle
	
# #############################################################################
#                               1. Add a TLV
# #############################################################################
	
	Log To Console  Add a TLV
	${result} =  Tlv Config  mode=create_tlv  handle=${template_handle}  protocol=dhcp4_client  tlv_name=custom tlv  tlv_description=This is my custom TLV  tlv_is_required=1  tlv_is_editable=1  type_name=Type  type_is_editable=1  length_name=lenght  length_description=description  length_encoding=hex  length_size=2  length_value=2  length_is_required=1  length_is_editable=1  length_is_enabled=1  tlv_include_in_messages=disco
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${tlv_handle} =  Get From Dictionary  ${result}  tlv_template_handle
	${tlv_value_handle} =  Get From Dictionary  ${result}  tlv_value_handle
	${tlv_type_handle} =  Get From Dictionary  ${result}  tlv_type_handle
	${tlv_length_handle} =  Get From Dictionary  ${result}  tlv_length_handle
	
# #############################################################################
#                              2.  Modify the TLV
# #############################################################################
	
	${result} =  Tlv Config  mode=modify  handle=${tlv_handle}  tlv_name=custom tlv 1  tlv_description=Custom TLV no 1  tlv_is_repeatable=0  tlv_is_required=0  tlv_include_in_messages=disco, Request
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
# #############################################################################
#                              3.  Modify the TLVs type
# #############################################################################
	
	Log To Console  Modify type name
	${result} =  Tlv Config  mode=modify  handle=${tlv_type_handle}  type_name=Type of TLV
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Add a new field under the type node.
	${result} =  Tlv Config  mode=create_field  handle=${tlv_type_handle}  field_name=Type field  field_description=Type field description  field_encoding=hex  field_size=2  field_value=160  field_is_required=1  field_is_repeatable=0  field_is_editable=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${field_handle} =  Get From Dictionary  ${result}  tlv_field_handle
	
# #############################################################################
#                             4.   Modify length
# #############################################################################
	
	Log To Console  Modify the parameters for the length and check the new values
	${result} =  Tlv Config  mode=modify  handle=${tlv_length_handle}  length_name=lenght1  length_description=length description1  length_encoding=decimal  length_size=3  length_value=3  length_is_required=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
# #############################################################################
#                             5.   Create field under value
# #############################################################################
	
	Log To Console  Create a new field under the value node.
	${result} =  Tlv Config  mode=create_field  handle=${tlv_value_handle}  field_name=custom_name  field_description=custom description  field_encoding=hex  field_size=2  field_value=160  field_is_required=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${field_handle} =  Get From Dictionary  ${result}  tlv_field_handle
	
# #############################################################################
#                             6.  Create a new container
# #############################################################################
	
	Log To Console  Create a new container under the value node.
	${result} =  Tlv Config  mode=create_tlv_container  handle=${tlv_value_handle}  protocol=dhcp4_client  container_name=custom_name_4  container_description=container description  container_is_required=1  container_is_editable=1  container_is_repeatable=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${container_handle} =  Get From Dictionary  ${result}  tlv_container_handle
	
# #############################################################################
#                          7.  create a new tlv under the previous tlv (subtlv)
# #############################################################################
	
	Log To Console  Create a new tlv under the value node.
	${result} =  Tlv Config  mode=create_tlv  handle=${container_handle}  protocol=dhcp4_client  tlv_name=custom_tlv2  tlv_description=This is my custom TLV_0  tlv_is_repeatable=1  tlv_is_required=1  length_name=lenght  length_description=length description  length_encoding=hex  length_size=2  length_value=2  length_is_required=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${subtlv_handle} =  Get From Dictionary  ${result}  subtlv_template_handle
	${subtlv_type_handle} =  Get From Dictionary  ${result}  tlv_type_handle
	${subtlv_length_handle} =  Get From Dictionary  ${result}  tlv_length_handle
	${subtlv_value_handle} =  Get From Dictionary  ${result}  tlv_value_handle
	
# #############################################################################
#                           8.    create a new field in the sub-tlv
# #############################################################################
	
	Log To Console  Create a new field under the value node.
	${result} =  Tlv Config  mode=create_tlv  handle=${subtlv_value_handle}  field_name=custom_name  field_description=custom description  field_encoding=hex  field_size=2  field_value=160  field_is_required=1  field_is_repeatable=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${field_handle} =  Get From Dictionary  ${result}  subtlv_template_handle
	
# #############################################################################
#                            9.   remove the tlv
# #############################################################################
	
	Log To Console  Remove the tlv from the template.
	${result} =  Tlv Config  mode=delete  handle=${tlv_handle}  protocol=dhcp4_client  
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
# #############################################################################
#                           10.    remove the template
# #############################################################################
	
	Log To Console  Remove the template from the protocol.
	${result} =  Tlv Config  mode=delete  handle=${template_handle}  protocol=dhcp4_client  
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
# #############################################################################
#                           11.    CLEANUP SESSION
# #############################################################################
	
	${result} =  Cleanup Session  reset=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log To Console  IxNetwork session is closed...
	Log To Console  Test is Passed