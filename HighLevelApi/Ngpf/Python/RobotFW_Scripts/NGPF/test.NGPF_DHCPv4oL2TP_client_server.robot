*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.104/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.104/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	12/7  12/8
${client_and_port} =  ${client}:${client_api_port}


*** Test Cases ***
test
################################################################################
# START - Connect to the chassis and get port handles from the result
################################################################################
	
	${result} =  Connect  reset=1  device=${chassis}  ixnetwork_tcl_server=${client_and_port}  tcl_server=${chassis}  port_list=@{portlist}  username=ixiaHLTQA  break_locks=1  interactive=1
	${connect_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${connect_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}

##############################################################################
#                Create a topology and a device group for LAC           
##############################################################################

	${result} =  Topology Config  topology_name=LAC 1  port_handle=@{portHandles}[1]  device_group_multiplier=10  device_group_name=LAC DG 1  device_group_enabled=1
	${topology_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${topology_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dg_handle_1} =  Get From Dictionary  ${result}  device_group_handle
	${topology_handle_1} =  Get From Dictionary  ${result}  topology_handle

	${result} =  Interface Config  protocol_handle=${dg_handle_1}  src_mac_addr=0000.0005.0001  src_mac_addr_step=0000.0000.1000
	${interface_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_handle_1} =  Get From Dictionary  ${result}  ethernet_handle


# #############################################################################
# 							LAC Stack		    							   
# #############################################################################

	${result} =  L2tp Config  mode=lac  handle=${ethernet_handle_1}  action=create  sessions_per_tunnel=10  num_tunnels=1  l2tp_dst_addr=12.70.1.1  l2tp_dst_step=0.0.0.1  l2tp_src_gw=0.0.0.0  l2tp_src_prefix_len=16  l2tp_src_addr=12.70.0.1  l2tp_src_count=1  l2tp_src_step=0.0.0.1  enable_term_req_timeout=0  udp_src_port=1600  udp_dst_port=1800  redial_timeout=13  rws=15  offset_len=16  max_ctrl_timeout=9  redial_max=2048  hostname=ixia_dut  secret=ixia_secret  hostname_wc=1  secret_wc=1  wildcard_bang_start=1  wildcard_bang_end=10  wildcard_dollar_start=1  wildcard_dollar_end=1  username=ixia_\#_?  password=pwd_\#_?  username_wc=1  password_wc=1  wildcard_pound_start=1  wildcard_pound_end=1  wildcard_question_start=1  wildcard_question_end=10  init_ctrl_timeout=6  hello_interval=101  framing_capability=async  ctrl_retries=11  bearer_type=digital  bearer_capability=digital  enable_mru_negotiation=1  desired_mru_rate=1501  lcp_enable_accm=1  lcp_accm=1501  max_auth_req=15  auth_req_timeout=7  auth_mode=pap_or_chap  chap_name=ixia_chap_name  chap_secret=ixia_chap_secret  client_dns_options=request_primary_and_secondary  ppp_client_ip=3.3.3.3  ppp_client_step=0.0.0.2  ppp_client_iid=00:44:44:44:00:00:00:01  client_ipv4_ncp_configuration=request  client_netmask=255.255.0.0  client_netmask_options=request_specific_netmask  client_ipv6_ncp_configuration=request  client_wins_options=request_primaryandsecondary_wins  client_wins_primary_address=88.88.88.88  client_wins_secondary_address=99.99.99.99  enable_domain_groups=1  echo_req=1  echo_req_interval=9  echo_rsp=1  max_configure_req=8  max_terminate_req=6  config_req_timeout=25  protocol_name=Ixia LAC  max_ipcp_req=12  ipcp_req_timeout=13  ip_cp=dual_stack  client_primary_dns_address=5.5.5.5  client_secondary_dns_address=6.6.6.6
	${LAC_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${LAC_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pppox_1_handle} =  Get From Dictionary  ${result}  pppox_client_handle

# #############################################################################
# 						  DHCPv6 Client Stack  		        			      
# #############################################################################

	${result} =  Emulation Dhcp Group Config  handle=${pppox_1_handle}  mode=create  dhcp_range_ip_type=ipv6  dhcp6_range_duid_enterprise_id=15  dhcp6_range_duid_type=duid_en  dhcp6_range_duid_vendor_id=20  dhcp6_range_duid_vendor_id_increment=2  dhcp_range_renew_timer=10  dhcp6_use_pd_global_address=1  protocol_name=Ixia DHCPv6  dhcp6_range_ia_type=iana_iapd  dhcp6_range_ia_t2=40000  dhcp6_range_ia_t1=30000  dhcp6_range_ia_id_increment=2  dhcp6_range_ia_id=20
	${dhcp_config_for_lac} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_config_for_lac}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcpclient_1_handle} =  Get From Dictionary  ${result}  dhcpv6client_handle

# #############################################################################
# 				Create a topology and a device group for LNS    			  
# #############################################################################

	${result} =  Topology Config  topology_name=LNS 1  port_handle=@{portHandles}[0]  device_group_multiplier=10  device_group_name=LNS DG 1  device_group_enabled=1

	${topology_status_2} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${topology_status_2}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dg_handle_2} =  Get From Dictionary  ${result}  device_group_handle
	${topology_handle_2} =  Get From Dictionary  ${result}  topology_handle
	
	${result} =  Interface Config  protocol_handle=${dg_handle_2}  src_mac_addr=0000.0065.0001  src_mac_addr_step=0000.0000.1000
	${command_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${command_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_handle_2} =  Get From Dictionary  ${result}  ethernet_handle
	
# #############################################################################
# 							LNS Stack		    							  
# #############################################################################
	
	${result} =  L2tp Config  mode=lns  handle=${ethernet_handle_2}  protocol_name=L2TP Network Server  action=create  num_tunnels=10  sessions_per_tunnel=50  l2tp_src_addr=12.70.1.1  l2tp_src_count=10  l2tp_src_gw=0.0.0.0  l2tp_src_step=0.0.0.1  l2tp_src_prefix_len=16  enable_term_req_timeout=0  username=ixia_lns_user  password=ixia_lns_pass  chap_name=ixia_chap_name  chap_secret=ixia_chap_secret  enable_domain_groups=1  udp_src_port=1800  udp_dst_port=1600  redial_timeout=13  rws=15  offset_len=16  max_ctrl_timeout=9  redial_max=2048  secret=ixia_secret  hostname=ixia_dut  init_ctrl_timeout=6  hello_interval=101  framing_capability=async  ctrl_retries=11  bearer_type=digital  bearer_capability=digital  accept_any_auth_value=1  max_auth_req=121  auth_req_timeout=132  auth_mode=pap_or_chap  ppp_client_iid=00:55:55:55:00:00:00:01  ppp_client_iid_step=00:00:00:00:00:00:00:01  ppp_client_ip=22.22.22.1  ppp_client_step=0.0.0.3  dns_server_list=100:0:0:1:0:0:0:0  echo_req_interval=17  send_dns_options=1  echo_req=1  echo_rsp=1  ipv6_pool_addr_prefix_len=90  ipv6_pool_prefix=1:1:1:1:1:1:1:1  ipv6_pool_prefix_len=72  lcp_accm=234  lcp_enable_accm=1  max_configure_req=111  max_terminate_req=120  config_req_timeout=55  enable_mru_negotiation=1  desired_mru_rate=1501  max_ipcp_req=14  ipcp_req_timeout=15  ip_cp=dual_stack  ppp_server_iid=00:66:66:66:00:00:00:01  ppp_server_ip=45.45.45.1  server_dns_options=supply_primary_and_secondary  ppp_local_iid_step=3  ppp_local_ip_step=0.0.15.15  server_ipv4_ncp_configuration=clientmay  server_netmask=255.255.255.128  server_netmask_options=supply_netmask  server_primary_dns_address=12.12.12.1  server_secondary_dns_address=13.13.13.1  server_ipv6_ncp_configuration=clientmay  server_wins_options=supply_primary_and_secondary  server_wins_primary_address=21.21.21.1  server_wins_secondary_address=31.31.31.1
	
	${LNS_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${LNS_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pppox_2_handle} =  Get From Dictionary  ${result}  pppox_server_handle
	
	${result} =  Emulation Dhcp Server Config  handle=${pppox_2_handle}  mode=create  dhcp6_ia_type=iana_iapd  protocol_name=Ixia DHCPv6 Server  ip_dns1=11:0:0:0:0:0:0:1  ip_dns2=22:0:0:0:0:0:0:1  ip_version=6  ipaddress_count=1  ipaddress_pool=5:a::1  lease_time=86400  pool_address_increment=0:0:0:0:0:0:0:1  start_pool_prefix=55:aa::  pool_prefix_increment=1:0:0:0:0:0:0:0  pool_prefix_size=1  prefix_length=64  custom_renew_time=34560  custom_rebind_time=55296  use_custom_times=1
	
	${dhcp_server_config_for_lns} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_server_config_for_lns}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_1_handle} =  Get From Dictionary  ${result}  dhcpv6server_handle
	
	Sleep  3s
	
# ###########################################################################

# 								START PROTOCOLS

# ###########################################################################
	
	${result} =  Test Control  action=start_protocol  handle=${dhcp_server_1_handle}
	${start_servers} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${start_servers}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  10s
	
	${result} =  Test Control  action=start_protocol  handle=${dhcpclient_1_handle}
	${start_clients} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${start_clients}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  20s
	
# ###########################################################################

# 								COLLECT STATS

# ###########################################################################
	
	${result} =  Emulation Dhcp Server Stats  dhcp_handle=${dhcp_server_1_handle}  action=collect  execution_timeout=60
	${server_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${server_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  The returned DHCPv4 server statistics are:
	Log  ${result}
	
	${result} =  Emulation Dhcp Stats  handle=${dhcpclient_1_handle}  mode=aggregate_stats  dhcp_version=dhcp6  execution_timeout=60
	${client_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${client_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  The aggragted DHCPv4 client statistics are:
	Log  ${result}
	
# ###########################################################################
# 								CLEANUP SESSION
# ###########################################################################
	${result} =  Cleanup Session  reset=1
	${cleanup_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${cleanup_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  IxNetwork session is closed...
	Log  !!! TEST is PASSED !!!