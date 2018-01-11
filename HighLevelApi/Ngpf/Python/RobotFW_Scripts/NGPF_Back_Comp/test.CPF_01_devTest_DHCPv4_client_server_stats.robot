*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/NGPF_support/NGPF_Backwards_Compatibility/DHCP/CPF_01_DHCPv4_client_server_stats/test.CPF_01_devTest_DHCPv4_client_server_stats.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	12/5  12/6

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
	
# START - Configure DHCP client session
	
	${result} =  Emulation Dhcp Config  version=ixnetwork  reset=1  mode=create  port_handle=@{portHandles}[0]  lease_time=300  max_dhcp_msg_size=1000
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_client_session_handle} =  Get From Dictionary  ${result}  handle
	
# START - Configure DHCP client group
	
	${result} =  Emulation Dhcp Group Config  version=ixnetwork  mode=create  handle=${dhcp_client_session_handle}  dhcp_range_ip_type=ipv6  num_sessions=100  encap=ethernet_ii_qinq  vlan_id_outer=100  vlan_id_outer_count=1  vlan_id=10  vlan_id_count=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
# START - DHCP Server configuration
	Log To Console  Start DHCP Server configuration ...
	${result} =  Emulation Dhcp Server Config  mode=create  port_handle=@{portHandles}[1]  count=3  encapsulation=ETHERNET_II  local_mac=0000.0001.0001  local_mac_step=0000.0000.0001  local_mac_outer_step=0000.0001.0000  qinq_incr_mode=both  vlan_id_count=1  vlan_id_count_inner=1  vlan_id=100  vlan_id_inner=10  vlan_id_repeat=1  vlan_id_repeat_inner=1  vlan_id_step=1  vlan_id_step_inner=1  vlan_user_priority=0  vlan_user_priority_inner=0  ip_version=4  ip_address=10.10.0.1  ip_gateway=10.10.0.2  ip_prefix_length=16  ip_prefix_step=2  ip_repeat=1  ip_step=0.1.0.0  ipaddress_count=1000  ipaddress_pool=10.10.1.1  ipaddress_pool_step=0.1.0.0  ip_gateway_step=0.1.0.0  lease_time=86400  lease_time_max=864000  local_mtu=1500  ping_check=0  ping_timeout=1  single_address_pool=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_handles} =  Set Variable  ${result['handle']['dhcp_handle']}
	
	Log To Console  End DHCP Server configuration ...
	
# END - DHCP Server configuration
	
# START DHCP
	
	${result} =  Emulation Dhcp Server Control  port_handle=@{portHandles}[1]  action=collect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  5s
	
	${result} =  Emulation Dhcp Control  port_handle=@{portHandles}[0]  action=bind
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  25s
	
#             GET DHCP STATISTICS                #
	
	${result} =  Emulation Dhcp Stats  port_handle=@{portHandles}[0]  version=ixnetwork
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	${result} =  Emulation Dhcp Server Stats  port_handle=@{portHandles}[1]  action=collect  ip_version=6
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
	
	
	
	
	
	
	
	
	