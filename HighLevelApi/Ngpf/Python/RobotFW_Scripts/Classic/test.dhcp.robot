*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.147/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.147/PythonApi  classic

# Based on script: /home/HLT-Regression/REG_TEST/feature-test/IxN/QA_REGR/HLT4.00/DHCPv6_server/test.05_dhcp_v6_srv_renew_b2b.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.191
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	9/1  9/2

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
# Configure DHCP client session
################################################################################

	# Configure DHCP client session
	${result} =  Emulation DHCP Config  mode=create  port_handle=@{portHandles}[0]  version=ixnetwork  reset=1  lease_time=300  max_dhcp_msg_size=1000
	${dhcp_client_session_handle} =  Get From Dictionary  ${result}  handle
	${dhcp_portHandle_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_portHandle_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

################################################################################
# Configure DHCP client group
################################################################################

	${result} =  Emulation Dhcp Group Config  version=ixnetwork  mode=create  handle=${dhcp_client_session_handle}  dhcp_range_ip_type=ipv6  num_sessions=500  encap=ethernet_ii_qinq  vlan_id_outer=200  vlan_id_outer_count=1  vlan_id=20  vlan_id_count=1
	${dhcp_handle} =  Get From Dictionary  ${result}  handle
	${dhcp_group_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_group_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

################################################################################
# START - DHCP Server configuration
################################################################################

	${result} =  Emulation Dhcp Server Config  count=1  functional_specification=v4_v6_compatible  encapsulation=ETHERNET_II  encapsulation=ETHERNET_II  ip_address=3000::2  ip_step=0:0:0:3::0  ipv6_gateway=3000::1  ip_prefix_length=64  ip_prefix_step=3  ip_repeat=1  ipaddress_count=1000  ipaddress_pool=3000::3  ipaddress_pool_step=0::2:0:0:0  lease_time=86400  local_mac=0000.0001.0001  mode=create  port_handle=@{portHandles}[1]  vlan_id=200  ipaddress_pool_prefix_length=64  ipaddress_pool_prefix_step=64  ip_dns1=5000::1  ip_dns1_step=0::5:0:0:0  ip_dns2=6000::1  ip_dns2_step=0::6:0:0:0  ipv6_gateway_step=0::4  ip_version=6  lease_time_max=864000  local_mac_step=0000.0000.0001  local_mac_outer_step=0000.0001.0000  local_mtu=1500  pvc_incr_mode=vci  qinq_incr_mode=inner  ping_check=0  ping_timeout=1  single_address_pool=0  vlan_id_count=2  vlan_id_count_inner=2  vlan_id_inner=20  vlan_id_repeat=1  vlan_id_repeat_inner=1  vlan_id_step=1  vlan_id_step_inner=1  vlan_user_priority=0  vlan_user_priority_inner=0  vci=32  vci_count=4063  vci_repeat=1  vci_step=1  vpi=0  vpi_count=1  vpi_repeat=1  vpi_step=1  dhcp6_ia_type=iana
	${dhcp_server_handle} =  Get From Dictionary  ${result}  handle
	${dhcp_server_handle_new} =  Get From Dictionary  ${dhcp_server_handle}  dhcp_handle
	${dhcp_server_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_server_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# START DHCP
################################################################################

	${result} =  Emulation Dhcp Server Control  port_handle=@{portHandles}[1]  action=collect
	${control_status1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
	${result} =  Emulation Dhcp Control  port_handle=@{portHandles}[0]  action=bind
	${control_status0} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status0}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  15s
################################################################################
#             GET DHCP STATISTICS                
################################################################################
	${result} =  Emulation Dhcp Stats  port_handle=@{portHandles}[0]  version=ixnetwork
	${dhcp_stats_0_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_0_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${get_stats} =  Get Dictionary Values  ${result}
	Log Many  ${get_stats}
	
	${result} =  Emulation Dhcp Server Stats  port_handle=@{portHandles}[1]  action=collect  ip_version=6
	${dhcp_stats_1_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_1_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${get_stats} =  Get Dictionary Values  ${result}
	Log Many  ${get_stats}

################################################################################
# START - DHCP Server modification
################################################################################
	# START - DHCP Server Call Modify
	${result} =  Emulation Dhcp Server Config  count=1  functional_specification=v4_v6_compatible  encapsulation=ETHERNET_II  handle=${dhcp_server_handle_new}  ip_address=3333::2  ip_step=0:0:0:3::0  ipv6_gateway=3333::1  ip_prefix_length=64  ip_prefix_step=3  ip_repeat=1  ipaddress_count=500  ipaddress_pool=3333::3  ipaddress_pool_step=0::2:0:0:0  lease_time=86400  local_mac=0000.0001.0001  mode=modify  port_handle=@{portHandles}[1]  vlan_id=200  ipaddress_pool_prefix_length=64  ipaddress_pool_prefix_step=64  ip_dns1=5555::1  ip_dns1_step=0::5:0:0:0  ip_dns2=6666::1  ip_dns2_step=0::6:0:0:0  ipv6_gateway_step=0::4  ip_version=6  lease_time_max=864000  local_mac_step=0000.0000.0001  local_mac_outer_step=0000.0001.0000  local_mtu=1500  pvc_incr_mode=vci  qinq_incr_mode=inner  ping_check=0  ping_timeout=1  single_address_pool=0  vlan_id_count=2  vlan_id_count_inner=2  vlan_id_inner=20  vlan_id_repeat=1  vlan_id_repeat_inner=1  vlan_id_step=1  vlan_id_step_inner=1  vlan_user_priority=0  vlan_user_priority_inner=0  vci=32  vci_count=4063  vci_repeat=1  vci_step=1  vpi=0  vpi_count=1  vpi_repeat=1  vpi_step=1  dhcp6_ia_type=iana
	${dhcp_server_handle} =  Get From Dictionary  ${result}  handle
	${dhcp_server_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_server_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

################################################################################
# RENEW DHCP
################################################################################

	${result} =  Emulation Dhcp Server Control  port_handle=@{portHandles}[1]  action=renew
	${control_status1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
	${result} =  Emulation Dhcp Control  port_handle=@{portHandles}[0]  action=renew
	${control_status0} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status0}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  15s
################################################################################
#             GET DHCP STATISTICS                
################################################################################

	${result} =  Emulation Dhcp Stats  port_handle=@{portHandles}[0]  version=ixnetwork
	${dhcp_stats_0_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_0_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${get_stats} =  Get Dictionary Values  ${result}
	Log Many  ${get_stats}
	
	${result} =  Emulation Dhcp Server Stats  port_handle=@{portHandles}[1]  action=collect  ip_version=6
	${dhcp_stats_1_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_1_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${get_stats} =  Get Dictionary Values  ${result}
	Log Many  ${get_stats}
