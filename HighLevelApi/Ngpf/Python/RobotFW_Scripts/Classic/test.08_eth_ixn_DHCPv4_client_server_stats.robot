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
# START - DHCP Server configuration
################################################################################

	${result} =  Emulation Dhcp Server Config  dhcp_offer_options=1  dhcp_offer_router_address=10.10.0.199  dhcp6_ia_type=iapd  count=3   encapsulation=ethernet_ii_qinq  ip_address=10.10.0.1  ip_gateway=10.10.0.2  ip_prefix_length=16  ip_prefix_step=0.0.1.0   ip_repeat=1  ip_step=0.1.0.0  ipaddress_count=100  ipaddress_pool=10.10.1.1   lease_time=86400  local_mac=0000.0001.0001  mode=create  port_handle=@{portHandles}[1]  vlan_id=100  ipaddress_pool_step=0.1.0.0  ip_dns1=2.2.2.2  ip_dns1_step=0.1.0.0  ip_dns2=3.3.3.3  ip_dns2_step=0.1.0.0  ip_gateway_step=0.1.0.0  ip_version=4  lease_time_max=864000   local_mac_step=0000.0000.0001   local_mac_outer_step=0000.0001.0000  local_mtu=1500  pvc_incr_mode=both  qinq_incr_mode=both   ping_check=0  ping_timeout=1  single_address_pool=0  vlan_id_count=1  vlan_id_count_inner=1  vlan_id_inner=10  vlan_id_repeat=1   vlan_id_repeat_inner=1  vlan_id_step=1  vlan_id_inter_device_step=100  vlan_id_step_inner=1  vlan_id_inner_inter_device_step=10  vlan_user_priority=0  vlan_user_priority_inner=0  vci=32  vci_count=4063  vci_repeat=1  vci_step=1  vpi=0  vpi_count=1  vpi_repeat=1  vpi_step=1
	${dhcp_server_handle} =  Get From Dictionary  ${result}  handle
	${dhcp_server_handle_new} =  Get From Dictionary  ${dhcp_server_handle}  dhcp_handle
	${dhcp_server_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_server_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	@{get_assoc_split1} =  Split String  ${dhcp_server_handle_new}  separator=\\
	${get_assoc_split2} =  Fetch From Left  ${get_assoc_split1}[1]  /ethernet
	${assoc} =  Fetch From Right  ${get_assoc_split2}  '
################################################################################
# End DHCP Server Call
################################################################################
	
################################################################################
# Configure DHCP client session
################################################################################

	# Configure DHCP client session
	${result} =  Emulation DHCP Config  mode=create  port_handle=@{portHandles}[0]  version=ixnetwork  reset=1  lease_time=300  max_dhcp_msg_size=1000  associates=${assoc}
	${dhcp_client_session_handle} =  Get From Dictionary  ${result}  handle
	${dhcp_portHandle_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_portHandle_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_client_session_handle} =  Get From Dictionary  ${result}  handle
################################################################################
# Configure DHCP client group
################################################################################

	${result} =  Emulation Dhcp Group Config  version=ixnetwork  mode=create  handle=${dhcp_client_session_handle}
	${dhcp_handle} =  Get From Dictionary  ${result}  handle
	${dhcp_group_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_group_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_client_group_handle} =  Get From Dictionary  ${result}  handle
	
################################################################################
# Modify DHCP client group
################################################################################

	${result} =  Emulation Dhcp Group Config  version=ixnetwork  mode=modify  handle=${dhcp_client_group_handle}  mac_addr=00.00.01.00.00.01  mac_addr_step=00.00.00.00.00.01  num_sessions=10  encap=ethernet_ii_qinq  vlan_id_outer=100  vlan_id_outer_count=1  vlan_id=10  vlan_id_count=1  qinq_incr_mode=inner
	${dhcp_handle} =  Get From Dictionary  ${result}  handle
	${dhcp_group_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_group_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_client_group_handle} =  Get From Dictionary  ${result}  handle
	
################################################################################
# Create another DHCP client group
################################################################################
	
	${result} =  Emulation Dhcp Group Config  version=ixnetwork  mode=create  handle=${dhcp_client_session_handle}  mac_addr=00.00.02.00.00.01  mac_addr_step=00.00.00.00.00.01  num_sessions=10  encap=ethernet_ii_qinq  vlan_id_outer=100  vlan_id_outer_count=1  vlan_id=10  vlan_id_count=1  qinq_incr_mode=inner
	${dhcp_handle} =  Get From Dictionary  ${result}  handle
	${dhcp_group_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_group_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_client_group_handle2} =  Get From Dictionary  ${result}  handle
	
################################################################################
# END - DHCP Client configuration
################################################################################
	
	
################################################################################
# START DHCP
################################################################################

	${result} =  Emulation Dhcp Server Control  port_handle=@{portHandles}[1]  action=collect
	${control_status1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
	
################################################################################
# Abort Sync DHCP SERVER
################################################################################

	${result} =  Emulation Dhcp Server Control  port_handle=@{portHandles}[1]  action=abort_async
	${control_status1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
################################################################################
# START AGAIN DHCP
################################################################################

	${result} =  Emulation Dhcp Server Control  port_handle=@{portHandles}[1]  action=collect
	${control_status1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s

################################################################################
# BIND DHCP
################################################################################  

	${result} =  Emulation Dhcp Control  port_handle=@{portHandles}[0]  action=bind
	${control_status1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s

	
################################################################################
# ABORT ASYNC DHCP
################################################################################

	${result} =  Emulation Dhcp Control  port_handle=@{portHandles}[0]  action=abort_async
	${control_status1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s

################################################################################
# BIND DHCP
################################################################################

	${result} =  Emulation Dhcp Control  port_handle=@{portHandles}[0]  action=bind
	${control_status1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
	
################################################################################
#             GET DHCP STATISTICS                
################################################################################

	
	${result} =  Emulation Dhcp Server Stats  port_handle=@{portHandles}[1]  action=collect
	${dhcp_stats_1_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_1_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${get_stats} =  Get Dictionary Values  ${result}
	Log Many  ${get_stats}

	${result} =  Emulation Dhcp Server Stats  port_handle=@{portHandles}[1]  dhcp_handle=${dhcp_server_handle_new}  action=collect
	${dhcp_stats_1_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_1_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${get_stats} =  Get Dictionary Values  ${result}
	Log Many  ${get_stats}
	
################################################################################
# Retrieve aggregate stats
################################################################################
	
	${result} =  Emulation Dhcp Stats  port_handle=@{portHandles}[0]  version=ixnetwork
	${dhcp_stats_0_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_0_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${get_stats} =  Get Dictionary Values  ${result}
	Log Many  ${get_stats}

	${result} =  Emulation Dhcp Stats  port_handle=@{portHandles}[0]  version=ixnetwork  mode=aggregate_stats
	${dhcp_stats_0_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_0_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${get_stats} =  Get Dictionary Values  ${result}
	Log Many  ${get_stats}
