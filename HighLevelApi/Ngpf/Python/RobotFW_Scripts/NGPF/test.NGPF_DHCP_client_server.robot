*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.104/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.104/PythonApi  ngpf

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
	

 ####################### Create Topologies ################################

 ########################### Topology 1 ###################################

	${result} =  Topology Config  topology_name=DHCPv4 Client  port_handle=@{portHandles}[0]  device_group_multiplier=10
	${topology_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${topology_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_first_handle} =  Get From Dictionary  ${result}  device_group_handle
	${top_1} =  Get From Dictionary  ${result}  topology_handle

 ########################### Topology 2 ###################################
 
	${result} =  Topology Config  topology_name=DHCPv4 Server  port_handle=@{portHandles}[1]  device_group_multiplier=1
	${topology_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${topology_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_second_handle} =  Get From Dictionary  ${result}  device_group_handle
	${top_handle} =  Get From Dictionary  ${result}  topology_handle
	${top_2} =  Get From Dictionary  ${result}  topology_handle

####################################################################
#              Configure dhcp_client and server                    #
####################################################################

	${result} =  Emulation Dhcp Group Config  handle=${deviceGroup_first_handle}  protocol_name=Dhcp_client  dhcp_range_server_address=5.5.5.5  dhcp4_gateway_address=0.0.0.0  mac_addr=000a.a0b0.ffff  mac_addr_step=00.00.00.00.00.02  use_rapid_commit=1  enable_stateless=0  num_sessions=30  vlan_id=100  vlan_id_step=0  vlan_user_priority=0  dhcp4_broadcast=1  dhcp_range_use_first_server=1  dhcp_range_renew_timer=2000  dhcp_range_ip_type=ipv4  vendor_id=any
	${dhcp_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_client} =  Get From Dictionary  ${result}  dhcpv4client_handle
	
	${result} =  Emulation Dhcp Config  handle=${dhcp_client}  mode=modify  release_rate=65  msg_timeout=5  request_rate=7  retry_count=2  interval_stop=5  interval_start=6  min_lifetime=10  max_restarts=20  max_lifetime=30  enable_restart=1  enable_lifetime=0  client_port=68  skip_release_on_stop=1  renew_on_link_up=1
	${dhcp_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
############## configure dhcp server ##############################
	
	${result} =  Emulation Dhcp Server Config  handle=${deviceGroup_second_handle}  count=5  lease_time=86400  ipaddress_count=10  ip_dns1=10.10.10.10  ip_dns1_step=0.0.0.1  ip_dns2=20.20.20.20  ip_dns2_step=0.0.1.0  ipaddress_pool=5.5.1.1  ipaddress_pool_step=0.0.0.1  ipaddress_pool_prefix_length=16  ipaddress_pool_prefix_step=1  dhcp_offer_router_address=5.5.5.5  dhcp_offer_router_address_step=0.0.0.1  ip_address=5.5.5.5  ip_step=0.0.0.1  ip_gateway=5.5.5.6  ip_gateway_step=0.0.0.1  ip_prefix_length=16  ip_prefix_step=1  local_mac=000a.0001.0001  local_mac_outer_step=0000.0001.0000  local_mtu=800  vlan_id=100  vlan_id_step=10  protocol_name=DHCP4 Server modified  use_rapid_commit=1  pool_address_increment=0.0.0.1  pool_address_increment_step=0.0.0.2  ping_timeout=10  ping_check=1  echo_relay_info=1  enable_resolve_gateway=0  manual_gateway_mac=00bd.2340.0000  manual_gateway_mac_step=0000.0000.0001  vlan_user_priority=0
	${dhcp_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server} =  Get From Dictionary  ${result}  dhcpv4server_handle
	
###########################################################################
#                       Modify dhcp server                                #
###########################################################################
	
	${result} =  Emulation Dhcp Server Config  handle=${dhcp_server}  mode=modify  lease_time=86400  ipaddress_count=10  ipaddress_pool=5.5.5.10  ipaddress_pool_step=0.0.0.1  ipaddress_pool_prefix_length=16  protocol_name=Dhcpv4_Server  vlan_user_priority=2
	${dhcp_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
##########################################################################
#                      start dhcp_client and server                      #
##########################################################################
	Log  Starting dhcp server....
	${result} =  Emulation Dhcp Server Control  dhcp_handle=${dhcp_server}  action=collect
	${control_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Starting dhcp client....
	${result} =  Emulation Dhcp Control  handle=${dhcp_client}  action=bind
	${control_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  40s
	
#########################################################################
#                     Retrieve statistics                               #
#########################################################################
	
	Log  Retrieve statistics
	${result} =  Emulation Dhcp Server Stats  port_handle=@{portHandles}[1]  action=collect  execution_timeout=60
	${dhcp_stats_0} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_0}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  DHCP Server aggregate statistics:
	Log  ${dhcp_stats_0}
	
	${result} =  Emulation Dhcp Server Stats  dhcp_handle=${dhcp_server}  action=collect  execution_timeout=60
	${dhcp_stats_0} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_0}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  DHCP Server per session statistics:
	Log  ${dhcp_stats_0}
	
	${result} =  Emulation Dhcp Stats  port_handle=@{portHandles}[0]  mode=aggregate_stats  dhcp_version=dhcp4  execution_timeout=60
	${dhcp_stats_0} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_0}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  DHCP Client aggregate statistics:
	Log  ${dhcp_stats_0}
	
	${result} =  Emulation Dhcp Stats  handle=${dhcp_client}  mode=aggregate_stats  dhcp_version=dhcp4  execution_timeout=60
	${dhcp_stats_0} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_0}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  DHCP Client aggregate statistics:
	Log  ${dhcp_stats_0}
	
	${result} =  Emulation Dhcp Stats  handle=${dhcp_client}  mode=session  dhcp_version=dhcp4  execution_timeout=60
	${dhcp_stats_0} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_0}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  DHCP Client per session statistics:
	Log  ${dhcp_stats_0}

	
#########################################################################
#                    Stop protocols                                     #
#########################################################################

############ stop server ################
 
	Log  Stopping server....
	${result} =  Emulation Dhcp Server Control  dhcp_handle=${dhcp_server}  action=abort
	${control_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
############ stop all protocol on port 1#####################
	
	${result} =  Test Control  handle=${deviceGroup_second_handle}  action=stop_protocol
	${stop_item_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${stop_item_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  10s
	
################ stop client ###################################
	
	Log  Stopping client....
	
	${result} =  Emulation Dhcp Control  handle=${dhcp_client}  action=abort
	${control_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Test Control  handle=${deviceGroup_first_handle}  action=stop_protocol
	${stop_item_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${stop_item_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  10s
	
########################################################################
#                    delete topology                                   #
########################################################################
	
	Log  Deleting dhcp server topology...
	
	${result} =  Emulation Dhcp Server Config  handle=${dhcp_server}  mode=reset
	${dhcp_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
########### delete dhcp server ############################
	
	Log  Deleting dhcp client topology...
	
	${result} =  Emulation Dhcp Server Config  handle=${dhcp_client}  mode=reset
	${dhcp_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
############## delete both topology ###################################
	
	${result} =  Topology Config  mode=destroy  topology_name=DHCPv4 Client  topology_handle=${top_1}  device_group_multiplier=10  device_group_enabled=0  device_group_handle=${deviceGroup_first_handle}
	${topology_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${topology_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Topology Config  mode=destroy  topology_name=DHCPv4 Server  topology_handle=${top_2}  device_group_multiplier=10  device_group_enabled=0  device_group_handle=${deviceGroup_second_handle}
	${topology_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${topology_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
# #######################################################################
# 							CLEANUP SESSION
# #######################################################################
	
	${result} =  Cleanup Session  reset=1
	${cleanup_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${cleanup_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  IxNetwork session is closed...
	Log  !!! TEST is PASSED !!!