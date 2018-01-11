*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxOS/QA_REGR/HLT3.50/DHCPv4_Server/test.04_dhcp_v4_srv_clnt_all_prm_b2b.tcl
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
# Configure DHCP client session
################################################################################

	${result} =  Emulation Dhcp Config  version=ixnetwork  reset=1  mode=create  port_handle=@{portHandles}[0]  lease_time=300  max_dhcp_msg_size=1000
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_client_session_handle} =  Get From Dictionary  ${result}  handle
	
################################################################################
# Configure DHCP client 1 group
################################################################################
	
	${result} =  Emulation Dhcp Group Config  version=ixnetwork  mode=create  handle=${dhcp_client_session_handle}  num_sessions=10  encap=ethernet_ii  mac_addr=20.00.01.00.00.01
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Configure DHCP client 2 group
################################################################################
	
	${result} =  Emulation Dhcp Group Config  version=ixnetwork  mode=create  handle=${dhcp_client_session_handle}  num_sessions=10  encap=ethernet_ii_vlan  vlan_id=10  vlan_id_count=1  mac_addr=30.00.01.00.00.01
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Configure DHCP client 3 group
################################################################################
	
	${result} =  Emulation Dhcp Group Config  version=ixnetwork  mode=create  handle=${dhcp_client_session_handle}  num_sessions=10  encap=ethernet_ii_qinq  vlan_id_outer=50  vlan_id_outer_count=1  vlan_id=10  vlan_id_count=1  mac_addr=40.00.01.00.00.01
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# START - DHCP Servers configuration
################################################################################
################################################################################
# Start DHCP Server 1 Call
################################################################################

	${result} =  Emulation Dhcp Server Config  count=1  encapsulation=ETHERNET_II  ip_address=20.10.0.1  ip_gateway=20.10.0.2  ip_prefix_length=16  ip_prefix_step=0.0.1.0  ip_repeat=1  ip_step=0.1.0.0  ipaddress_count=10  ipaddress_pool=20.10.1.1  lease_time=86400  local_mac=2000.0001.0001  mode=create  port_handle=@{portHandles}[1]  ipaddress_pool_step=0.1.0.0  ip_dns1=110.110.0.1  ip_dns1_step=0.1.0.0  ip_dns2=${EMPTY}  ip_dns2_step=0.1.0.0  ip_gateway_step=0.1.0.0  ip_version=4  lease_time_max=864000  local_mac_step=0000.0000.0001  local_mac_outer_step=0000.0001.0000  local_mtu=1500  pvc_incr_mode=both  ping_check=0  ping_timeout=1  single_address_pool=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_handles} =  Set Variable  ${result['handle']['dhcp_handle']}
	
################################################################################
# End DHCP Server 1 Call
################################################################################
	
################################################################################
# Start DHCP Server 2 Call
################################################################################
	
	${result} =  Emulation Dhcp Server Config  count=1  encapsulation=ETHERNET_II  ip_address=30.10.0.1  ip_gateway=30.10.0.2  ip_prefix_length=16  ip_prefix_step=0.0.1.0  ip_repeat=1  ip_step=0.1.0.0  ipaddress_count=1000  ipaddress_pool=30.10.1.1  lease_time=86400  local_mac=3000.0001.0001  mode=create  port_handle=@{portHandles}[1]  vlan_id=10  ipaddress_pool_step=0.1.0.0  ip_dns1=${EMPTY}  ip_dns1_step=0.1.0.0  ip_dns2=${EMPTY}  ip_dns2_step=0.1.0.0  ip_gateway_step=0.1.0.0  ip_version=4  lease_time_max=864000  local_mac_step=0000.0000.0001  local_mac_outer_step=0000.0001.0000  local_mtu=1500  pvc_incr_mode=both  ping_check=0  ping_timeout=1  single_address_pool=0  vlan_id_count=1  vlan_id_repeat=1  vlan_id_step=1  vlan_user_priority=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_handles1} =  Set Variable  ${result['handle']['dhcp_handle']}
	
################################################################################
# End DHCP Server 2 Call
################################################################################
	
################################################################################
# Start DHCP Server 3 Call
################################################################################
	
	${result} =  Emulation Dhcp Server Config  count=1  encapsulation=ETHERNET_II  ip_address=40.10.0.1  ip_gateway=40.10.0.2  ip_prefix_length=16  ip_prefix_step=16  ip_repeat=1  ip_step=0.1.0.0  ipaddress_count=1000  ipaddress_pool=40.10.1.1  lease_time=86400  local_mac=4000.0001.0001  mode=create  port_handle=@{portHandles}[1]  vlan_id=50  ipaddress_pool_step=0.1.0.0  ip_dns1=${EMPTY}  ip_dns1_step=0.1.0.0  ip_dns2=${EMPTY}  ip_dns2_step=0.1.0.0  ip_gateway_step=0.1.0.0  ip_version=4  lease_time_max=864000  local_mac_step=0000.0000.0001  local_mac_outer_step=0000.0001.0000  local_mtu=1500  pvc_incr_mode=both  qinq_incr_mode=both  ping_check=0  ping_timeout=1  single_address_pool=0  vlan_id_count=1  vlan_id_count_inner=1  vlan_id_inner=10  vlan_id_repeat=1  vlan_id_repeat_inner=1  vlan_id_step=1  vlan_id_step_inner=1  vlan_user_priority=0  vlan_user_priority_inner=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_handles2} =  Set Variable  ${result['handle']['dhcp_handle']}
	
################################################################################
# End DHCP Server 3 Call
################################################################################
################################################################################
# END - DHCP Server configuration
################################################################################
	
################################################################################
# START DHCP Server & Client
################################################################################
	
	${result} =  Emulation Dhcp Server Control  port_handle=@{portHandles}[1]  action=collect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
	${result} =  Emulation Dhcp Control  port_handle=@{portHandles}[0]  action=bind
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  20s
	
##################################################
#             GET DHCP STATISTICS                #
##################################################
	
	${result} =  Emulation Dhcp Stats  port_handle=@{portHandles}[0]  version=ixnetwork
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log To Console  "--------------DHCP CLIENT stats-------------"
	Log  ${result}
	
	${result} =  Emulation Dhcp Server Stats  port_handle=@{portHandles}[1]  action=collect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log To Console  "--------------DHCP SERVER stats-------------"
	Log  ${result}
	
	
	
	
	