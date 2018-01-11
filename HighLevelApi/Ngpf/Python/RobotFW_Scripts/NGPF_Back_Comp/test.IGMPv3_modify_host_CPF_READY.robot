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

##################################################
#  Configure interfaces and create IGMP sessions #
##################################################

	:FOR	${port}	IN	@{portHandles}
	\	${result} =  Emulation Igmp Config  port_handle=${port}  mode=create  reset=1  msg_interval=1000  igmp_version=v3  ip_router_alert=1  general_query=1  group_query=1  unsolicited_report_interval=50  suppress_report=0  max_response_control=1  max_response_time=0  filter_mode=exclude  count=1  intf_ip_addr=100.41.1.2  neighbor_intf_ip_addr=100.41.1.1  intf_prefix_len=24  vlan_id_mode=increment  vlan_id=10  vlan_id_step=1  vlan_user_priority=7
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${session} =  Get From Dictionary  ${result}  handle
	@{session} =  Split String  ${session}
	${host} =  Get From Dictionary  ${result}  igmp_host_handle
	@{host} =  Split String  ${host}
	
# Create multicast group pool number 1
	
	${result} =  Emulation Multicast Group Config  mode=create  num_groups=5  ip_addr_start=226.0.1.1  ip_addr_step=0.0.0.1  ip_prefix_len=24
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${group1} =  Get From Dictionary  ${result}  handle
	
# Create multicast group pool number 2
	
	${result} =  Emulation Multicast Group Config  mode=create  num_groups=5  ip_addr_start=227.0.1.1  ip_addr_step=0.0.0.1  ip_prefix_len=24
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${group2} =  Get From Dictionary  ${result}  handle
	
# Create multicast source pool number 1
	
	${result} =  Emulation Multicast Source Config  mode=create  num_sources=3  ip_addr_start=100.41.1.1  ip_addr_step=0.0.1.0  ip_prefix_len=24
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${source1} =  Get From Dictionary  ${result}  handle
	
# Create multicast source pool number 1
	
	${result} =  Emulation Multicast Source Config  mode=create  num_sources=3  ip_addr_start=100.43.1.1  ip_addr_step=0.0.1.0  ip_prefix_len=24
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${source2} =  Get From Dictionary  ${result}  handle
	
# Create group member for session1 with group_pool_handle group1
	
	${result} =  Emulation Igmp Group Config  mode=create  session_handle=@{session}[0]  group_pool_handle=${group1}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${group_member1} =  Get From Dictionary  ${result}  handle
	
# Create group member for session1 with group_pool_handle group2 and
# source handle source1 and source2
	${result} =  Emulation Igmp Group Config  mode=create  session_handle=@{session}[0]  group_pool_handle=${group2}  source_pool_handle=${source1} ${source2}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${group_member2} =  Get From Dictionary  ${result}  handle
	
# Modify session to have filter_mode include and no ip_router_alert
	
	${result} =  Emulation Igmp Config  mode=modify  handle=@{session}[0]  filter_mode=include  ip_router_alert=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	
	
	
	
	
	