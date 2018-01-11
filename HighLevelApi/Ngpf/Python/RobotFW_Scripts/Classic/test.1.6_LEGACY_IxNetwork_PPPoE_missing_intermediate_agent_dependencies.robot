*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/PPP/test.6_LEGACY_IxNetwork_PPPoE_missing_intermediate_agent_dependencies.tcl
# Topology 2P-B2B

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
################################################################################
# END - Connect to the chassis
################################################################################

########################################
# Start PPPoX Call                     #
########################################

	
	
	${result} =  Pppox Config  mode=add  num_sessions=10  port_handle=@{portHandles}[0]  protocol=pppoe  port_role=access  attempt_rate=100  disconnect_rate=100  max_outstanding=1000  addr_count_per_vci=1  addr_count_per_vpi=1  encap=ethernet_ii  mac_addr=00:0c:0a:0b:00:01  mac_addr_step=00:00:00:00:00:01  pvc_incr_mode=vci  vci=32  vci_count=1  vci_step=1  vlan_id=1  vlan_id_count=4094  vlan_id_outer=1  vlan_id_outer_count=4094  vlan_id_outer_step=1  vlan_id_step=1  vlan_user_priority=0  vlan_user_priority_count=8  vlan_user_priority_step=1  vpi=0  vpi_count=1  vpi_step=1  qinq_incr_mode=both  ac_select_list=${EMPTY}  ac_select_mode=first_responding  max_padi_req=10  max_padr_req=10  padi_req_timeout=6  padr_req_timeout=6  redial=1  redial_max=25  redial_timeout=15  service_name=${EMPTY}  service_type=any  domain_group_map=${EMPTY}  config_req_timeout=6  echo_req=1  echo_req_interval=70  echo_rsp=1  max_configure_req=15  max_terminate_req=15  local_magic=1  term_req_timeout=6  ip_cp=ipv4_cp  ipcp_req_timeout=6  ipv6_pool_addr_prefix_len=64  ipv6_pool_prefix=::  ipv6_pool_prefix_len=48  max_ipcp_req=10  ppp_local_ip=1.1.1.100  ppp_local_ip_step=0.0.0.1  ppp_local_iid=00 00 00 00 00 00 00 00  ppp_peer_ip=1.1.1.1  ppp_peer_ip_step=0.0.0.1  ppp_peer_iid=00 00 00 00 00 00 00 00  auth_mode=none  auth_req_timeout=6  max_auth_req=15  password=${EMPTY}  password_wildcard=0  username=${EMPTY}  username_wildcard=0  wildcard_pound_end=0  wildcard_pound_start=0  wildcard_question_end=0  wildcard_question_start=0  actual_rate_downstream=20  actual_rate_upstream=20  agent_circuit_id=${EMPTY}  agent_remote_id=${EMPTY}  data_link=atm_aal5  enable_client_signal_iwf=1  enable_client_signal_loop_char=1  enable_client_signal_loop_encap=1  enable_client_signal_loop_id=1  enable_server_signal_iwf=1  enable_server_signal_loop_char=1  enable_server_signal_loop_encap=1  enable_server_signal_loop_id=1  intermediate_agent_encap1=single_tagged_eth  intermediate_agent_encap2=pppoa_llc  intermediate_agent=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pppox_handle_0} =  Get From Dictionary  ${result}  handle
	
########################################
# End PPPoX Call                       #
########################################
################################################################################
# END - PPPoX configuration - Access Port
################################################################################
	
################################################################################
# START - PPPoX configuration - Network Port
################################################################################
	
	${result} =  Pppox Config  mode=add  num_sessions=10  port_handle=@{portHandles}[1]  protocol=pppoe  port_role=network  attempt_rate=100  disconnect_rate=100  max_outstanding=1000  addr_count_per_vci=1  addr_count_per_vpi=1  encap=ethernet_ii  mac_addr=00:01:0c:0a:00:01  mac_addr_step=00:00:00:00:00:01  pvc_incr_mode=vci  vci=32  vci_count=1  vci_step=1  vlan_id=1  vlan_id_count=4094  vlan_id_outer=1  vlan_id_outer_count=4094  vlan_id_outer_step=1  vlan_id_step=1  vlan_user_priority=0  vlan_user_priority_count=8  vlan_user_priority_step=1  vpi=0  vpi_count=1  vpi_step=1  qinq_incr_mode=both  ac_name=ac_name_ixia  ac_select_list=${EMPTY}  max_padi_req=10  max_padr_req=10  padi_req_timeout=5  padr_req_timeout=5  redial=1  redial_max=20  redial_timeout=10  service_name=${EMPTY}  service_type=any  domain_group_map=${EMPTY}  config_req_timeout=5  echo_req=0  echo_req_interval=60  echo_rsp=1  max_configure_req=10  max_terminate_req=10  local_magic=1  term_req_timeout=5  ip_cp=ipv4_cp  ipcp_req_timeout=5  ipv6_pool_addr_prefix_len=64  ipv6_pool_prefix=::  ipv6_pool_prefix_len=48  max_ipcp_req=10  ppp_local_ip=1.1.1.1  ppp_local_ip_step=0.0.0.1  ppp_local_iid=00 00 00 00 00 00 00 00  ppp_peer_ip=1.1.1.100  ppp_peer_ip_step=0.0.0.1  ppp_peer_iid=00 00 00 00 00 00 00 00  auth_mode=none  auth_req_timeout=5  max_auth_req=10  password=${EMPTY}  password_wildcard=0  username=${EMPTY}  username_wildcard=0  wildcard_pound_end=0  wildcard_pound_start=0  wildcard_question_end=0  wildcard_question_start=0  actual_rate_downstream=20  actual_rate_upstream=20  agent_circuit_id=${EMPTY}  agent_remote_id=${EMPTY}  data_link=atm_aal5  enable_client_signal_iwf=1  enable_client_signal_loop_char=1  enable_client_signal_loop_encap=1  enable_client_signal_loop_id=1  enable_server_signal_iwf=1  enable_server_signal_loop_char=1  enable_server_signal_loop_encap=1  enable_server_signal_loop_id=1  intermediate_agent_encap1=single_tagged_eth  intermediate_agent_encap2=pppoa_llc  intermediate_agent=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pppox_handle_1} =  Get From Dictionary  ${result}  handle
	
########################################
# End PPPoX Call                       #
########################################
################################################################################
# END - PPPoX configuration - Network Port
################################################################################
	
########################################
# Start PPP                            #
########################################
	
	${result} =  Pppox Control  handle=${pppox_handle_1}  action=connect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

########################################
# Start PPP                            #
########################################
	
	${result} =  Pppox Control  handle=${pppox_handle_0}  action=connect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	Sleep  10s
	
########################################
# Aggregate Stats                      #
########################################
	
	${result} =  Pppox Stats  port_handle=@{portHandles}[0]  mode=aggregate
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${sess_num} =  Set Variable  ${result['@{portHandles}[0]']['aggregate']['num_sessions']}
	${sess_count_up} =  Set Variable  ${result['@{portHandles}[0]']['aggregate']['connected']}
	${sess_min_setup} =  Set Variable  ${result['@{portHandles}[0]']['aggregate']['min_setup_time']}
	${sess_max_setup} =  Set Variable  ${result['@{portHandles}[0]']['aggregate']['max_setup_time']}
	${sess_avg_setup} =  Set Variable  ${result['@{portHandles}[0]']['aggregate']['avg_setup_time']}
	
	Log  Number of sessions = ${sess_num}
	Log  Number of connected sessions = ${sess_count_up}
	Log  Minimum Setup Time (ms) = ${sess_min_setup}
	Log  Maximum Setup Time (ms) = ${sess_max_setup}
	Log  Average Setup Time (ms) = ${sess_avg_setup}
	
	Run Keyword If  '${sess_count_up}' != '10'  FAIL  "Not all PPPoX sessions are up."  ELSE  Log  "All PPPoX sessions are up."
	
########################################
# Stop PPP                             #
########################################
	
	${result} =  Pppox Control  handle=${pppox_handle_0}  action=disconnect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
########################################
# Stop PPP                             #
########################################
	
	${result} =  Pppox Control  handle=${pppox_handle_1}  action=disconnect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	
	
########################################
# Reset_async PPP                      #
########################################
	
	${result} =  Pppox Control  handle=${pppox_handle_0}  action=reset_async
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
########################################
# Reset_async PPP                      #
########################################
	
	${result} =  Pppox Control  handle=${pppox_handle_1}  action=reset_async
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	
	
	
	
	
	
	
	