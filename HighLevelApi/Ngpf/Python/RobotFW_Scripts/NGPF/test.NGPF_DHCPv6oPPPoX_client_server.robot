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

# #############################################################################
# 								PPP STACK 1
# #############################################################################
	Log  Creating PPP servers...
	${result} =  Topology Config  topology_name=PPP Servers Topology  port_handle=@{portHandles}[1] 
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle

	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name=PPP Servers  device_group_multiplier=2  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
	${result} =  Interface Config  protocol_handle=${deviceGroup_1_handle}  mtu=1500  vlan=0  use_vpn_parameters=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
	${result} =  Multivalue Config  pattern=single_value  single_value=0  nest_step=1  nest_owner=${topology_1_handle}  nest_enabled=0  overlay_value=1  overlay_value_step=0  overlay_index=1  overlay_index_step=0  overlay_count=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_7_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=single_value  single_value=0  nest_step=1  nest_owner=${topology_1_handle}  nest_enabled=0  overlay_value=1  overlay_value_step=0  overlay_index=2  overlay_index_step=0  overlay_count=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_9_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	
	${result} =  Pppox Config  port_role=network  handle=${ethernet_1_handle}  enable_mru_negotiation=0  desired_mru_rate=1492  enable_max_payload=0  server_ipv6_ncp_configuration=clientmay  server_ipv4_ncp_configuration=clientmay  num_sessions=5  auth_req_timeout=10  config_req_timeout=10  echo_req=0  echo_rsp=1  ip_cp=ipv6_cp  ipcp_req_timeout=10  max_auth_req=20  max_terminate_req=3  password=pwd  username=user  mode=add  auth_mode=pap  echo_req_interval=10  max_configure_req=3  max_ipcp_req=3  ac_name=ixia  enable_domain_group_map=0  enable_server_signal_iwf=0  enable_server_signal_loop_char=0  enable_server_signal_loop_encap=0  enable_server_signal_loop_id=0  ipv6_pool_prefix_len=48  ppp_local_ip_step=0.0.0.1  ppp_local_iid_step=1  ppp_peer_iid_step=1  ppp_peer_ip_step=0.0.0.1  send_dns_options=${multivalue_7_handle}  server_dns_options=disable_extension  server_dns_primary_address=10.10.10.10  server_dns_secondary_address=11.11.11.11  server_netmask_options=disable_extension  server_netmask=255.255.255.0  server_wins_options=disable_extension  server_wins_primary_address=10.10.10.10  server_wins_secondary_address=11.11.11.11  accept_any_auth_value=${multivalue_9_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pppoxserver_1_handle} =  Get From Dictionary  ${result}  pppox_server_handle
	
	Log  DONE creating PPP servers.
	
	
# #############################################################################
# 								PPP STACK 2
# #############################################################################
	
	Log  Creating PPP clients...
	${result} =  Topology Config  topology_name=PPP Clients Topology  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle

	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name=PPP Clients  device_group_multiplier=5  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	
	${result} =  Multivalue Config  pattern=repeatable_random  nest_step=1  nest_owner=${topology_2_handle}  nest_enabled=0  repeatable_random_seed=1  repeatable_random_count=4000000  repeatable_random_fixed=5  repeatable_random_mask=25
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_12_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	
	${result} =  Pppox config  port_role=access  handle=${deviceGroup_2_handle}  unlimited_redial_attempts=0  enable_mru_negotiation=0  desired_mru_rate=1492  max_payload=1700  enable_max_payload=0  client_ipv6_ncp_configuration=learned  client_ipv4_ncp_configuration=learned  lcp_enable_accm=0  lcp_accm=ffffffff  ac_select_mode=first_responding  auth_req_timeout=10  config_req_timeout=10  echo_req=0  echo_rsp=1  ip_cp=ipv6_cp  ipcp_req_timeout=10  max_auth_req=20  max_padi_req=5  max_padr_req=5  max_terminate_req=3  padi_req_timeout=10  padr_req_timeout=10  password=pwd  chap_secret=secret  username=user  chap_name=user  mode=add  auth_mode=pap  echo_req_interval=10  max_configure_req=3  max_ipcp_req=3  actual_rate_downstream=10  actual_rate_upstream=10  data_link=ethernet  enable_domain_group_map=0  enable_client_signal_iwf=0  enable_client_signal_loop_char=0  enable_client_signal_loop_encap=0  enable_client_signal_loop_id=0  intermediate_agent_encap1=untagged_eth  intermediate_agent_encap2=na  ppp_local_iid=0:11:11:11:0:0:0:1  ppp_local_ip=1.1.1.1  redial_timeout=10  service_type=any
	
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pppoxclient_1_handle} =  Get From Dictionary  ${result}  pppox_client_handle
	
	
	${result} =  Multivalue Config  pattern=distributed  distributed_value=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_13_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=distributed  distributed_value=10
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_14_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=distributed  distributed_value=10
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_15_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	
# #############################################################################
# 								PPP GLOBALS
# #############################################################################
	
	${result} =  Pppox Config  port_role=access  handle=/globals  mode=add  ipv6_global_address_mode=icmpv6  ra_timeout=30  create_interfaces=0  attempt_rate=200  attempt_max_outstanding=400  attempt_interval=1000  attempt_enabled=1  attempt_scale_mode=port  disconnect_rate=200  disconnect_max_outstanding=400  disconnect_interval=1000  disconnect_enabled=1  disconnect_scale_mode=port  enable_session_lifetime=0  min_lifetime=${multivalue_13_handle}  max_lifetime=${multivalue_14_handle}  enable_session_lifetime_restart=0  max_session_lifetime_restarts=${multivalue_15_handle}  unlimited_session_lifetime_restarts=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  DONE creating and configuring PPP clients.
	
#############################################################################
# 								DHCP CLIENT
# #############################################################################
	${result} =  Emulation Dhcp Group Config  handle=${pppoxclient_1_handle}  mode=create  dhcp_range_ip_type=ipv6  dhcp6_range_duid_enterprise_id=15  dhcp6_range_duid_type=duid_en  dhcp6_range_duid_vendor_id=20  dhcp6_range_duid_vendor_id_increment=2  dhcp_range_renew_timer=10  dhcp6_use_pd_global_address=1  protocol_name=Ixia DHCPv6  dhcp6_range_ia_type=iana_iapd  dhcp6_range_ia_t2=40000  dhcp6_range_ia_t1=30000  dhcp6_range_ia_id_increment=2  dhcp6_range_ia_id=20
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcpclient_1_handle} =  Get From Dictionary  ${result}  dhcpv6client_handle
	Log  DONE creating and configuring DHCPv6 clients.
	
	
#############################################################################
# 								DHCP SERVER
##############################################################################
	${result} =  Emulation Dhcp Server Config  handle=${pppoxserver_1_handle}  mode=create  dhcp6_ia_type=iana_iapd  protocol_name=Ixia DHCPv6 Server  ip_dns1=11:0:0:0:0:0:0:1  ip_dns2=22:0:0:0:0:0:0:1  ip_version=6  ipaddress_count=1  ipaddress_pool=5:a::1  ipaddress_pool_prefix_length=64  lease_time=86400  pool_address_increment=0:0:0:0:0:0:0:1  start_pool_prefix=55:aa::  pool_prefix_increment=1:0:0:0:0:0:0:0  pool_prefix_size=1  prefix_length=64  custom_renew_time=34560  custom_rebind_time=55296  use_custom_times=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_1_handle} =  Get From Dictionary  ${result}  dhcpv6server_handle
	
	Sleep  3s
	Log  DONE creating and configuring DHCPv6 servers.
	
#############################################################################
# 								START PROTOCOLS
##############################################################################
	
	${result} =  Test Control  action=start_protocol  handle=${deviceGroup_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  20s
	
	${result} =  Test Control  action=start_protocol  handle=${pppoxclient_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  20s
	
	${result} =  Test Control  action=start_protocol  handle=${dhcpclient_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  20s
	
##############################################################################
# 								COLLECT STATS
##############################################################################
	${result} =  Emulation Dhcp Stats  handle=${dhcpclient_1_handle}  mode=aggregate_stats  dhcp_version=dhcp6  execution_timeout=60
	Log  The aggragted DHCPv4 client statistics are:\
	Log  ${result}
	
	

###########################################################################
# 								CLEANUP SESSION
# ###########################################################################
	${result} =  Cleanup Session  reset=1
	${cleanup_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${cleanup_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  IxNetwork session is closed...
	Log  !!! TEST is PASSED !!!