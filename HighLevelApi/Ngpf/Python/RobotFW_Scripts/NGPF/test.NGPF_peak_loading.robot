*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.104/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.104/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
# Topology 4P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	12/7  12/8  12/9  12/10
${client_and_port} =  ${client}:${client_api_port}
${config_file} =  /home/pythar/ROBOT/protocols\ test\ cases/peak_loading_ipv4_vlan_traffic.ixncfg

*** Test Cases ***
test
################################################################################
# START - Connect to the chassis and get port handles from the result
################################################################################
	
	${result} =  Connect  device=${chassis}  ixnetwork_tcl_server=${client_and_port}  tcl_server=${chassis}  port_list=@{portlist}  username=ixiaHLTQA  break_locks=1  break_locks=1  config_file=${config_file}
	${connect_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${connect_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	
	Log  Printing connection result
	${aux} =  Get From Dictionary  ${result}  Traffic Item 1
	${aux2} =  Get From Dictionary  ${aux}  traffic_config
	${ti_name} =  Get From Dictionary  ${aux2}  traffic_item
	

	${result} =  Test Control  action=start_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  15s
	
	${result} =  Traffic Config  mode=modify  global_dest_mac_retry_count=3  global_dest_mac_retry_delay=3  global_enable_dest_mac_retry=1  global_enable_mac_change_on_fly=1  global_frame_ordering=peak_loading  stream_id=${ti_name}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Ixnet  connect  ${client}  -port  ${client_api_port}  -version  8.20
	${root} =  Ixnet  getRoot
	${ordering_mode} =  Ixnet  getAttribute  /traffic  -frameOrderingMode
	Run Keyword If  '${ordering_mode}' != 'peakLoading'  FAIL  "Error: Ordering mode is not current, should be peakLoading but value from IxN is: ${ordering_mode}"  ELSE  Log  "SUCCESS: Ordering mode is ${ordering_mode}"
	

###########################################################################
# 								CLEANUP SESSION
# ###########################################################################
	${result} =  Cleanup Session  reset=1
	${cleanup_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${cleanup_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  IxNetwork session is closed...
	Log  !!! TEST is PASSED !!!