*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.60/DualStackPPPoverL2TP/test.90_DualStackPPPServer_session_dhcpv6_vlan.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.191
${client} =  	10.215.133.232
${client_api_port} =  	8136
@{portlist} =  	11/1  11/3

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
################################################################################
# Configure interface in the test
################################################################################

	${result} =  Pppox Config  port_handle=@{portHandles}[0]  mode=add  protocol=pppoe  encap=ethernet_ii_qinq  dhcpv6_hosts_enable=1  dhcpv6pd_type=client  num_sessions=1  ip_cp=dual_stack  hosts_range_count=1  hosts_range_eui_increment=00:00:00:00:00:00:00:01  hosts_range_first_eui=00:00:00:00:00:00:11:11  hosts_range_ip_prefix=64  hosts_range_subnet_count=1  port_role=access  ppp_local_iid=00:11:11:11:00:00:00:01  ppp_peer_iid=00:11:22:11:00:00:00:01  ipv6_pool_prefix=1:1:1::  ipv6_global_address_mode=dhcpv6_pd  auth_req_timeout=10  config_req_timeout=10  echo_req=0  echo_req_interval=10  ipcp_req_timeout=10  max_auth_req=20  max_configure_req=3  max_ipcp_req=3  max_padi_req=5  max_padr_req=5  max_terminate_req=3  padi_req_timeout=10  padr_req_timeout=10  term_req_timeout=15  vlan_id=5  vlan_id_count=4040  vlan_id_step=1  vlan_user_priority=1  vlan_id_outer=4  vlan_id_outer_count=3  vlan_id_outer_step=1  vlan_user_priority_count=6  vlan_user_priority_step=1  qinq_incr_mode=both
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dsppp_handle_client} =  Get From Dictionary  ${result}  handle
	
	${result} =  Pppox Config  port_handle=@{portHandles}[1]  mode=add  protocol=pppoe  encap=ethernet_ii_qinq  dhcpv6_hosts_enable=1  dhcpv6pd_type=server  dhcp6_pd_server_range_start_pool_address=2001::  dhcp6_pd_server_range_subnet_prefix=48  num_sessions=1  ip_cp=dual_stack  hosts_range_count=1  hosts_range_ip_prefix=96  hosts_range_subnet_count=1  hosts_range_first_eui=00:00:00:00:00:00:11:11  hosts_range_eui_increment=00:00:00:00:00:00:00:01  hosts_range_ip_prefix_addr=3001::  hosts_range_ip_outer_prefix=64  port_role=network  auth_req_timeout=10  config_req_timeout=10  echo_req=0  echo_req_interval=10  ipcp_req_timeout=10  max_auth_req=20  max_configure_req=3  max_ipcp_req=3  max_padi_req=5  max_padr_req=5  max_terminate_req=3  padi_req_timeout=10  padr_req_timeout=10  term_req_timeout=15  ppp_local_iid=00:11:11:11:00:00:00:01  ppp_peer_iid=00:11:22:11:00:00:00:01  ipv6_pool_prefix=1:1:1::  ipv6_global_address_mode=dhcpv6_pd  vlan_id=5  vlan_id_count=4040  vlan_id_step=1  vlan_user_priority=1  vlan_id_outer=4  vlan_id_outer_count=3  vlan_id_outer_step=1  vlan_user_priority_count=6  vlan_user_priority_step=1  qinq_incr_mode=both
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dsppp_handle_server} =  Get From Dictionary  ${result}  handle
	
	${result} =  Pppox COntrol  action=connect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  20s
	
#########################################
#  Retrieve aggregate session stats     #
#########################################
	
	${result} =  Pppox Stats  mode=session_all  port_handle=@{portHandles}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
	
	
	
	
	
	
	
	