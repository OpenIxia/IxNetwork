*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.60/DualStackPPPoverL2TP_extensions/test.210_DualStackLNS_add_all_params_modify_remove_ext.tcl
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
	${result} =  Connect  device=${chassis}  ixnetwork_tcl_server=${client}:${client_api_port}  port_list=@{portlist}  reset=1
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	Log Many  @{portHandles}


################################################################################
# Configure DHCP Dual Stack PPP                                          #
################################################################################

	${result} =  L2tp Config  port_handle=@{portHandles}[0]  l2_encap=ethernet_ii  l2tp_dst_addr=40.0.0.1  l2tp_src_addr=40.0.0.100  num_tunnels=5  mode=lac  dhcpv6_hosts_enable=0  auth_mode=chap  ip_cp=ipv4_cp  password=dualstack  username=dualstack  echo_req_interval=10  echo_req=0  config_req_timeout=10  max_configure_req=3  ipcp_req_timeout=10  max_ipcp_req=3  auth_req_timeout=10  max_auth_req=20
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${l2tp_handle_client} =  Get From Dictionary  ${result}  handle

	${result} =  Dhcp Client Extension Config  handle=${l2tp_handle_client}  dhcp6_client_range_duid_type=duid_llt  dhcp6_client_range_duid_enterprise_id=10  dhcp6_client_range_duid_vendor_id=10  dhcp6_client_range_duid_vendor_id_increment=1  dhcp6_client_range_param_request_list=2 7 23 24  dhcp6_client_range_use_vendor_class_id=1  dhcp6_pgdata_max_outstanding_requests=20  dhcp6_pgdata_override_global_setup_rate=0  dhcp6_pgdata_setup_rate_increment=0  dhcp6_pgdata_setup_rate_initial=10  dhcp6_pgdata_setup_rate_max=10  dhcp6_global_max_outstanding_requests=20  dhcp6_global_setup_rate_increment=0  dhcp6_global_setup_rate_initial=10  dhcp6_global_setup_rate_max=10
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dsppp_handle_client} =  Get From Dictionary  ${result}  handle
	
	
	${result} =  L2tp Config  port_handle=@{portHandles}[1]  l2_encap=ethernet_ii  l2tp_dst_addr=40.0.0.100  l2tp_src_addr=40.0.0.1  num_tunnels=5  mode=lns  dhcpv6_hosts_enable=0  auth_mode=chap  ip_cp=ipv4_cp  password=dualstack  username=dualstack  echo_req_interval=10  echo_req=0  config_req_timeout=10  max_configure_req=3  ipcp_req_timeout=10  max_ipcp_req=3  auth_req_timeout=10  max_auth_req=20  lease_time_max=864000  lease_time=86400  ipv6_pool_prefix=bb::  ipv6_pool_prefix_len=48
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${l2tp_handle_server} =  Get From Dictionary  ${result}  handle
	
	${result} =  Dhcp Server Extension Config  handle=${l2tp_handle_server}  dhcp6_server_range_start_pool_address=3201::  dhcp6_server_range_subnet_prefix=48  dhcp6_server_range_first_dns_server=60:0:2::2  dhcp6_server_range_second_dns_server=70:0:2::3  dhcp6_server_range_dns_domain_search_list=example.com  dhcp6_pgdata_max_outstanding_releases=500  dhcp6_pgdata_max_outstanding_requests=20  dhcp6_pgdata_override_global_setup_rate=0  dhcp6_pgdata_override_global_teardown_rate=0  dhcp6_pgdata_setup_rate_increment=0  dhcp6_pgdata_setup_rate_initial=10  dhcp6_pgdata_setup_rate_max=10  dhcp6_pgdata_teardown_rate_increment=50  dhcp6_pgdata_teardown_rate_initial=50  dhcp6_pgdata_teardown_rate_max=500
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dsppp_handle_server} =  Get From Dictionary  ${result}  handle
	
	${result} =  Dhcp Server Extension Config  handle=${l2tp_handle_server}  dhcp6_server_range_start_pool_address=4501::  dhcp6_server_range_subnet_prefix=52  dhcp6_server_range_first_dns_server=89:0:2::2  dhcp6_server_range_second_dns_server=99:0:2::3  dhcp6_server_range_dns_domain_search_list=example99.com  dhcp6_pgdata_max_outstanding_releases=555  dhcp6_pgdata_max_outstanding_requests=33  dhcp6_pgdata_override_global_setup_rate=1  dhcp6_pgdata_override_global_teardown_rate=1  dhcp6_pgdata_setup_rate_increment=1  dhcp6_pgdata_setup_rate_initial=17  dhcp6_pgdata_setup_rate_max=19  dhcp6_pgdata_teardown_rate_increment=55  dhcp6_pgdata_teardown_rate_initial=67  dhcp6_pgdata_teardown_rate_max=444
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dsppp_handle_server} =  Get From Dictionary  ${result}  handle
	
	${result} =  L2tp Control  action=connect  handle=${l2tp_handle_server}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  L2tp Control  action=connect  handle=${l2tp_handle_client}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  L2tp Stats  mode=aggregate  handle=${l2tp_handle_server}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  L2tp Stats  mode=aggregate  handle=${l2tp_handle_client}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	
	
	
	
	
	
