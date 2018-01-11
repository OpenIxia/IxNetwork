*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.50/IGMP_ENHANCEMENTS/test.17_IGMP_group_configuration_mode_remove.tcl
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

	
##################################################
#  Configure interfaces and create IGMP sessions #
##################################################

	Log To Console  Configure IGMP on Port 1
	${result} =  Emulation Igmp Config  port_handle=@{portHandles}[0]  mode=create  reset=1  msg_interval=167  igmp_version=v3  ip_router_alert=1  general_query=0  group_query=0  filter_mode=exclude  count=1  intf_ip_addr=100.0.1.2  neighbor_intf_ip_addr=100.0.1.1  intf_prefix_len=24  vlan_id_mode=increment  vlan_id=10  vlan_id_step=1  vlan_user_priority=4
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${session_handle_1} =  Get From Dictionary  ${result}  handle
	
	Log To Console  Configure IGMP on Port 2
	${result} =  Emulation Igmp Config  port_handle=@{portHandles}[1]  mode=create  reset=1  msg_interval=167  igmp_version=v3  ip_router_alert=0  general_query=0  group_query=0  filter_mode=exclude  count=1  intf_ip_addr=100.0.1.1  neighbor_intf_ip_addr=100.0.1.2  intf_prefix_len=24  vlan_id_mode=increment  vlan_id=7  vlan_id_step=1  vlan_user_priority=7
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${session_handle_2} =  Get From Dictionary  ${result}  handle
	
############################################################################
# Create IGMP group member by asociating a multicast group pool to a session
############################################################################
	
	${result} =  Emulation Igmp Group Config  mode=create  session_handle=100.0.1.2  group_pool_handle=226.0.1.1/0.0.0.1/5 226.0.1.6/0.0.0.2/4  source_pool_handle=100.0.1.2/0.0.0.2/2,110.0.1.2/0.0.0.1/3 120.0.1.2/0.0.0.1/5,130.0.1.2/0.0.0.1/5,140.0.1.2/0.0.0.1/5
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${group_handle_0} =  Get From Dictionary  ${result}  group_pool_handle
	
	${result} =  Emulation Igmp Group Config  mode=create  session_handle=100.0.1.1  group_pool_handle=227.0.1.1/0.0.0.1/5 227.0.2.1/0.0.0.2/3 227.0.3.1/0.0.0.2/3  source_pool_handle=150.0.1.2/0.0.0.1/4,160.0.1.2/0.0.0.1/5 170.0.1.2/0.0.0.1/4 180.0.1.2/0.0.0.1/4,190.0.1.2/0.0.0.1/5,200.0.1.2/0.0.0.3/2
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${group_handle_1} =  Get From Dictionary  ${result}  group_pool_handle
	
# Delete the IGMP group members
	
	${result} =  Emulation Igmp Group Config  handle=226.0.1.1/0.0.0.1/5 227.0.2.1/0.0.0.2/3  mode=delete
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Igmp Group Config  handle=226.0.1.6/0.0.0.2/4 227.0.1.1/0.0.0.1/5  mode=delete
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
# delete the hosts on each port
	
	${result} =  Emulation Igmp Group Config  session_handle=100.0.1.2  mode=clear_all
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Igmp Group Config  session_handle=100.0.1.1  mode=clear_all
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	
	
	