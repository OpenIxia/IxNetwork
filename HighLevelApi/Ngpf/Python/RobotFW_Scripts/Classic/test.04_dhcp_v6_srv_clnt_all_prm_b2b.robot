*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.147/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.147/PythonApi  classic

# Based on script: /home/HLT-Regression/REG_TEST/feature-test/IxN/QA_REGR/HLT4.00/DHCPv6_server/test.05_dhcp_v6_srv_renew_b2b.tcl
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
	${result} =  Connect  device=${chassis}  ixnetwork_tcl_server=${client}:${client_api_port}  port_list=@{portlist}  reset=1
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
	
	${result} =  Emulation Dhcp Group Config  version=ixnetwork  mode=create  dhcp_range_ip_type=ipv6  dhcp6_range_ia_type=iapd  handle=${dhcp_client_session_handle}  num_sessions=10  encap=ethernet_ii  mac_addr=20.00.01.00.00.01  vlan_id=1  vlan_id_count=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Configure DHCP client 2 group
################################################################################
	
	${result} =  Emulation Dhcp Group Config  version=ixnetwork  mode=create  dhcp_range_ip_type=ipv6  dhcp6_range_ia_type=iata  handle=${dhcp_client_session_handle}  num_sessions=20  encap=ethernet_ii_vlan  vlan_id=100  vlan_id_count=1  mac_addr=40.00.01.00.00.01
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Configure DHCP client 3 group
################################################################################
	
	${result} =  Emulation Dhcp Group Config  version=ixnetwork  mode=create  dhcp_range_ip_type=ipv6  dhcp6_range_ia_type=iana  handle=${dhcp_client_session_handle}  num_sessions=30  encap=ethernet_ii_qinq  vlan_id_outer=50  vlan_id_outer_count=1  vlan_id=10  vlan_id_count=1  mac_addr=30.00.01.00.00.01
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# START - DHCP Servers configuration
################################################################################
################################################################################
# Start DHCP Server 1 Call
################################################################################
	${result} =  Emulation Dhcp Server Config  count=1  functional_specification=v4_v6_compatible  encapsulation=ETHERNET_II  ip_address=3000::2  ipv6_gateway=3000::1  ip_prefix_length=64  ip_prefix_step=3  ip_repeat=1  ip_step=0:0:0:2::0  ipaddress_count=10  ipaddress_pool=3000::  ipaddress_pool_step=0:0:0:2::0  lease_time=86400  local_mac=0000.0011.0001  mode=create  port_handle=@{portHandles}[1]  ipaddress_pool_prefix_length=64  ipaddress_pool_prefix_step=2  ip_dns1=5000::1  ip_dns1_step=0::5:0:0:0  ip_dns2=6000::1  ip_dns2_step=0::6:0:0:0  ipv6_gateway_step=0:0:0:2::0  ip_version=6  lease_time_max=864000  local_mac_step=0000.0000.0001  local_mac_outer_step=0000.0001.0000  local_mtu=1500  pvc_incr_mode=vci  ping_check=0  ping_timeout=1  single_address_pool=0  dhcp6_ia_type=iapd
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_handles} =  Get From Dictionary  ${result}  handle
	${dhcp_server_handles1_new} =  Get From Dictionary  ${dhcp_server_handles}  dhcp_handle
################################################################################
# End DHCP Server 1 Call
################################################################################
	
################################################################################
# Start DHCP Server 2 Call
################################################################################
	
	${result} =  Emulation Dhcp Server Config  count=1  functional_specification=v4_v6_compatible  encapsulation=ETHERNET_II  ip_address=3300::2  ipv6_gateway=3300::1  ip_prefix_length=80  ip_prefix_step=3  ip_repeat=1  ip_step=::2:0:0  ipaddress_count=20  ipaddress_pool=3300::3  ipaddress_pool_step=::2:0:0  lease_time=86400  local_mac=0000.0111.0001  mode=create  port_handle=@{portHandles}[1]  ipaddress_pool_prefix_length=80  ipaddress_pool_prefix_step=2  ip_dns1=5500::1  ip_dns1_step=0::5:0:0:0  ip_dns2=6600::1  ip_dns2_step=0::6:0:0:0  ipv6_gateway_step=0::2:0:0:0  ip_version=6  lease_time_max=864000  local_mac_step=0000.0000.0001  local_mac_outer_step=0000.0001.0000  local_mtu=1500  pvc_incr_mode=vci  ping_check=0  ping_timeout=1  single_address_pool=0  dhcp6_ia_type=iata  vlan_id=100  vlan_id_count=1  vlan_id_repeat=1  vlan_id_step=1  vlan_user_priority=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_handles} =  Get From Dictionary  ${result}  handle
	${dhcp_server_handles2_new} =  Get From Dictionary  ${dhcp_server_handles}  dhcp_handle
	
################################################################################
# Start DHCP Server 3 Call
################################################################################
	
	${result} =  Emulation Dhcp Server Config  count=1  functional_specification=v4_v6_compatible  encapsulation=ETHERNET_II  ip_address=3330::2  ipv6_gateway=3330::1  ip_prefix_length=96  ip_prefix_step=3  ip_repeat=1  ip_step=::2:0:0  ipaddress_count=30  ipaddress_pool=3330::3  ipaddress_pool_step=::2:0  vlan_id=50  lease_time=86400  local_mac=0000.1111.0001  mode=create  port_handle=@{portHandles}[1]  ipaddress_pool_prefix_length=96  ipaddress_pool_prefix_step=2  ip_dns1=5550::1  ip_dns1_step=0::5:0:0:0  ip_dns2=6660::1  ip_dns2_step=0::6:0:0:0  ipv6_gateway_step=0::2:0:0:0  ip_version=6  lease_time_max=864000  local_mac_step=0000.0000.0001  local_mac_outer_step=0000.0001.0000  local_mtu=1500  pvc_incr_mode=both  ping_check=0  ping_timeout=1  single_address_pool=0  dhcp6_ia_type=iana  qinq_incr_mode=both  vlan_id_count=1  vlan_id_count_inner=1  vlan_id_inner=10  vlan_id_repeat=1  vlan_id_repeat_inner=1  vlan_id_step=1  vlan_id_step_inner=1  vlan_user_priority=0  vlan_user_priority_inner=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_handles} =  Get From Dictionary  ${result}  handle
	${dhcp_server_handles2_new} =  Get From Dictionary  ${dhcp_server_handles}  dhcp_handle
	
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
	
	${result} =  Emulation Dhcp Control  port_handle=@{portHandles}[0]  action=bind
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  30s
	
##################################################
#             GET DHCP STATISTICS                #
##################################################
	
	${result} =  Emulation Dhcp Stats  port_handle=@{portHandles}[0]  version=ixnetwork
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	${result} =  Emulation Dhcp Server Stats  port_handle=@{portHandles}[1]  action=collect  ip_version=6
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
################################################################################
# ABORT ASYNC DHCP
################################################################################
	
	${result} =  Emulation Dhcp Server Control  port_handle=@{portHandles}[1]  action=abort_async
	
	
	
	
	
	
	
	
	
	