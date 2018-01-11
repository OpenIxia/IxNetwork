*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.60/DualStackPPPoverL2TP/test.90_DualStackPPPServer_session_dhcpv6_vlan.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.191
${client} =  	10.215.133.232
${client_api_port} =  	8136
@{portlist} =  	9/1  9/2

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

 ####################### Create Topologies ###################################
	Log To Console  Configure topology 1
	${result} =  Topology Config  topology_name=DHCPv6 Client  port_handle=@{portHandles}[0]  device_group_multiplier=10  device_group_name=Basic conf  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_first_handle} =  Get From Dictionary  ${result}  device_group_handle
	${top_1} =  Get From Dictionary  ${result}  topology_handle
	
 ########################### Topology 2 ###################################
	Log To Console  Configure topology 2
	${result} =  Topology Config  topology_name=DHCPv6 Server  port_handle=@{portHandles}[1]  device_group_multiplier=2  device_group_name=Basic conf
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_second_handle} =  Get From Dictionary  ${result}  device_group_handle
	${top_2} =  Get From Dictionary  ${result}  topology_handle
	
#################### Configure  IPv6 #####################################
	
	Log To Console  Configure Ipv6
	${result} =  Interface Config  protocol_handle=${deviceGroup_second_handle}  port_handle=@{portHandles}[1]  src_mac_addr=0000.0005.0001  ipv6_intf_addr=3000::3000:0001  ipv6_intf_addr_step=::1000  ipv6_resolve_gateway=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6_hand} =  Get From Dictionary  ${result}  ipv6_handle
	
################################################################################
#                          Configure dhcp_client and server                    #
################################################################################
	
	${result} =  Emulation Dhcp Server Config  handle=${ipv6_hand}  ip_version=6  dhcp6_ia_type=iata
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server} =  Get From Dictionary  ${result}  dhcpv6server_handle

	${result} =  Emulation Dhcp Server Config  handle=${dhcp_server}  mode=modify  count=3  dhcp6_ia_type=iata  lease_time=5400  ip_version=6  ipaddress_count=10  ip_dns1=1110::100  ip_dns1_step=0:0:0:0:0:0:0:1  ip_dns2=100::100  ip_dns2_step=0:0:0:0:0:0:1:1  ipaddress_pool=10::100  ipaddress_pool_step=0:0:0:0:0:0:0:1  ipaddress_pool_prefix_length=12  ipaddress_pool_prefix_step=1  ip_address=1000::100  ip_step=0:0:0:0:0:0:0:0100  ip_gateway=1110::100  ip_gateway_step=0:0:0:0:0:0:0:1  ipv6_gateway=1110::101  ipv6_gateway_step=::1  ip_prefix_length=12  ip_prefix_step=3  local_mac_outer_step=0000.0001.0000  local_mtu=1500  protocol_name=DHCPv6_server  use_rapid_commit=1  pool_address_increment=200:200:200::0  pool_address_increment_step=0:0:0:0:0:0:0:2  dns_domain=blabla  custom_rebind_time=240  custom_renew_time=140  use_custom_times=1  start_pool_prefix=100::20  start_pool_prefix_step=0::2  pool_prefix_increment_step=0::3  pool_prefix_size=100  prefix_length=24  ping_timeout=10  ping_check=1  pool_prefix_increment=300:200:200::0  local_mac=00bc.00ad.0003
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Configure dhcp client
	
	${result} =  Emulation Dhcp Group Config  handle=${deviceGroup_first_handle}  mac_addr=00:00:01:00:00:01  mac_addr_step=00.00.00.00.00.02  num_sessions=3  mac_mtu=1800  vlan_user_priority=2  dhcp_range_ip_type=ipv6  dhcp6_range_duid_enterprise_id=15  dhcp6_range_duid_type=duid_en  dhcp6_range_duid_vendor_id=20  dhcp6_range_duid_vendor_id_increment=2  dhcp_range_renew_timer=10  use_vendor_id=1  dhcp6_use_pd_global_address=1  protocol_name=dhcpv6client  dhcp6_range_ia_type=iana_iapd  dhcp6_range_ia_t2=40000  dhcp6_range_ia_t1=30000  dhcp6_range_ia_id_increment=2  dhcp6_range_ia_id=20  use_rapid_commit=1  dhcp6_range_param_request_list=5
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_client} =  Get From Dictionary  ${result}  dhcpv6client_handle
	
################################################################################
#                          start dhcp_client and server                        #
################################################################################
	
	Log To Console  Starting dhcp server...
	${result} =  Emulation Dhcp Server Control  dhcp_handle=${dhcp_server}  action=collect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Starting dhcp client...
	${result} =  Emulation Dhcp Control  handle=${dhcp_client}  action=bind
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
#                       Retrieve statistics                                    #
################################################################################
	
	Log To Console  Retrieve statistics
	${result} =  Emulation Dhcp Server Stats  port_handle=@{portHandles}[1]  action=collect  execution_timeout=30
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Dhcp Server Stats  dhcp_handle=${dhcp_server}  action=collect  execution_timeout=30
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Dhcp Stats  port_handle=@{portHandles}[0]  mode=aggregate_stats  dhcp_version=dhcp6  execution_timeout=30
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Dhcp Stats  handle=${dhcp_client}  mode=aggregate_stats  dhcp_version=dhcp6  execution_timeout=30
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Dhcp Stats  handle=${dhcp_client}  mode=session  dhcp_version=dhcp6  execution_timeout=30
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
##############################################################################
#                       Stop protocols                                         #
################################################################################
	Log To Console  Stopping server...
	${result} =  Emulation Dhcp Server Control  dhcp_handle=${dhcp_server}  action=abort
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
 ############ stop all protocol on port 1#####################
	
	${result} =  Test Control  action=stop_protocol  handle=${deviceGroup_second_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  20s
	Log To Console  Checking if server has stopped ...
	${result} =  Protocol Info  mode=aggregate  handle=${dhcp_server}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${down} =  Set Variable  ${result['${dhcp_server}']['aggregate']['sessions_down']}
	Run Keyword If  '${down}' != '0'  FAIL  "DHCP Server was not stopped"  ELSE  Log  "Status is SUCCESS"
 ################ stop client ################################### 
	
	${result} =  Emulation Dhcp Control  handle=${dhcp_client}  action=abort
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"