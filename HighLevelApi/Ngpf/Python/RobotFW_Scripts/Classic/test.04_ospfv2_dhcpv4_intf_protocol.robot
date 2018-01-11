*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxOS/QA_REGR/HLT3.50/DHCPv4_Server/test.02_dhcp_v4_srv_modify_prm_b2b.tcl

*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.232
${client_api_port} =  	8136
@{portlist} =  	12/1  12/2

*** Test Cases ***
test
################################################################################
# START - Connect to the chassis
################################################################################

	# Connect to the chassis and get port handles from the result
	${result} =  Connect  device=${chassis}  ixnetwork_tcl_server=${client}:${client_api_port}  port_list=@{portlist}  reset=1  mode=connect  break_locks=1  interactive=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	Log Many  @{portHandles}

	${result} =  Interface Config  port_handle=@{portHandles}[0]  mode=modify  intf_ip_addr=33.33.33.3  netmask=255.255.255.0  gateway=33.33.33.1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${prot_intf_handle} =  Get From Dictionary  ${result}  interface_handle
	
################################################################################
# Configure DHCP client session
################################################################################

	${result} =  Emulation Dhcp Config  version=ixnetwork  reset=1  mode=create  port_handle=@{portHandles}[0]  lease_time=300  max_dhcp_msg_size=1000
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_client_session_handle_0} =  Get From Dictionary  ${result}  handle

################################################################################
# Configure DHCP client group
################################################################################

	${result} =  Emulation Dhcp Group Config  version=ixnetwork  mode=create  handle=${dhcp_client_session_handle_0}  num_sessions=10  encap=ethernet_ii
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_client_group_handle_0} =  Get From Dictionary  ${result}  handle
	${index} =  Set Variable  7
#	@{interface_handles_list} =  Create List
#	: FOR    ${index}    IN RANGE    1    5
#	\    Append To List  ${interface_handles_list}  ${dhcp_client_group_handle_0}
#	Append To List  ${interface_handles_list}  ${prot_intf_handle}
#	: FOR    ${index}    IN RANGE    1    3
#	\    Append To List  ${interface_handles_list}  ${dhcp_client_group_handle_0}
#	Log  ${interface_handles_list}
################################################################################
# Configure an OSPFv2 emulated router
################################################################################
	
#	${result} =  Emulation Ospf Config  mode=create  reset=1  lsa_discard_mode=0  session_type=ospfv2  port_handle=@{portHandles}[0]  interface_handle=@{interface_handles_list}  count=7  area_id=0.0.0.0  area_type=external-capable  network_type=broadcast  option_bits=0x02  router_id=218.149.0.0  router_id_step=0.1.0.0
	@{interface_handles_list} =  Create List 
	Append To List  ${interface_handles_list}  ${dhcp_client_group_handle_0}|1,3-5
	Append To List  ${interface_handles_list}  ${prot_intf_handle}
	Append To List  ${interface_handles_list}  ${dhcp_client_group_handle_0}|8,10
	Log  ${interface_handles_list}
	${result} =  Emulation Ospf Config  mode=create  reset=1  lsa_discard_mode=0  session_type=ospfv2  port_handle=@{portHandles}[0]  interface_handle=@{interface_handles_list}  count=7  area_id=0.0.0.0  area_type=external-capable  network_type=broadcast  option_bits=0x02  router_id=218.149.0.0  router_id_step=0.1.0.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospf_router_handle_0} =  Get From Dictionary  ${result}  handle
	
	${result} =  Emulation Ospf Topology Route Config  mode=create  handle=${ospf_router_handle_0}  count=1  summary_prefix_length=24  summary_prefix_metric=0  summary_prefix_start=15.0.15.1  summary_number_of_prefix=1  type=summary_routes
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospf_topology_route_handle_} =  Get From Dictionary  ${result}  elem_handle
	
	${result} =  Emulation Ospf Control  handle=${ospf_router_handle_0}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	
	
	
	




