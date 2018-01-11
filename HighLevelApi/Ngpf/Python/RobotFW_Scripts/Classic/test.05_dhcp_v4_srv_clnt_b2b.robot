*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxOS/QA_REGR/HLT3.50/DHCPv4_Server/test.02_dhcp_v4_srv_modify_prm_b2b.tcl
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
# Configure DHCP client group
################################################################################

	${result} =  Emulation Dhcp Group Config  version=ixnetwork  mode=create  handle=${dhcp_client_session_handle}  num_sessions=10  encap=ethernet_ii_qinq  vlan_id_outer=100  vlan_id_outer_count=1  vlan_id=10  vlan_id_count=1
 	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_client_group_handle} =  Get From Dictionary  ${result}  handle
################################################################################
# Start DHCP Server Call
################################################################################

	${result} =  Emulation Dhcp Server Config  count=3  encapsulation=ETHERNET_II  handle=REPLACE_ME  ip_address=10.10.0.1  ip_gateway=10.10.0.2  ip_prefix_length=16  ip_prefix_step=0.0.1.0  ip_repeat=1  ip_step=0.1.0.0  ipaddress_count=100  ipaddress_pool=10.10.1.1  lease_time=86400  local_mac=0000.0001.0001  mode=create  port_handle=@{portHandles}[1]  vlan_id=100  ipaddress_pool_step=0.1.0.0  ip_dns1=2.2.2.2  ip_dns1_step=0.1.0.0  ip_dns2=3.3.3.3  ip_dns2_step=0.1.0.0  ip_gateway_step=0.1.0.0  ip_version=4  lease_time_max=864000  local_mac_step=0000.0000.0001  local_mac_outer_step=0000.0001.0000  local_mtu=1500  pvc_incr_mode=both  qinq_incr_mode=both  ping_check=0  ping_timeout=1  single_address_pool=0  vlan_id_count=1  vlan_id_count_inner=1  vlan_id_inner=10  vlan_id_repeat=1  vlan_id_repeat_inner=1  vlan_id_step=1  vlan_id_inter_device_step=100  vlan_id_step_inner=1  vlan_id_inner_inter_device_step=10  vlan_user_priority=0  vlan_user_priority_inner=0  vci=32  vci_count=4063  vci_repeat=1  vci_step=1  vpi=0  vpi_count=1  vpi_repeat=1  vpi_step=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_handles} =  Set Variable  ${result['handle']['dhcp_handle']}

################################################################################
# End DHCP Server Call
################################################################################

################################################################################
# START DHCP
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

	${dhcp_stats_0} =  Emulation Dhcp Stats  port_handle=@{portHandles}[0]  version=ixnetwork
	${status} =  Get From Dictionary  ${dhcp_stats_0}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${dhcp_stats_1} =  Emulation Dhcp Server Stats  port_handle=@{portHandles}[1]  action=collect
	${status} =  Get From Dictionary  ${dhcp_stats_1}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

##################################################
#            PRINT DHCP STATISTICS               #
##################################################

	Log To Console  "--------------DHCP CLIENT stats-------------"
	Log  ${dhcp_stats_0}
	Log To Console  "--------------DHCP SERVER stats-------------"
	Log  ${dhcp_stats_1}
	
################################################################################
# Retrieve per session stats
################################################################################

	${result} =  Emulation Dhcp Stats  port_handle=@{portHandles}[0]  mode=session  version=ixnetwork
	Log To Console  "--------------Pers Session stats-------------"
	Log  ${result}

	${result} =  Emulation Dhcp Stats  handle=${dhcp_client_group_handle}  mode=session  version=ixnetwork
	Log To Console  "--------------Pers Session stats-------------"
	Log  ${result}





