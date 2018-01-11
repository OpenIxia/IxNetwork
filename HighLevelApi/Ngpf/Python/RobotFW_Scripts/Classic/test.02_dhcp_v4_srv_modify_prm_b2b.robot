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
# Start DHCP Server Call
################################################################################

	${result} =  Emulation Dhcp Server Config  count=3  encapsulation=ETHERNET_II  handle=REPLACE_ME  ip_address=10.10.0.1  ip_gateway=10.10.0.2  ip_prefix_length=16  ip_prefix_step=0.0.1.0  ip_repeat=1  ip_step=0.1.0.0  ipaddress_count=1000  ipaddress_pool=10.10.1.1  lease_time=86400  local_mac=0000.0001.0001   mode=create  port_handle=@{portHandles}[0]  vlan_id=100  ipaddress_pool_step=0.1.0.0  ip_dns1=${EMPTY}  ip_dns1_step=0.1.0.0  ip_dns2=${EMPTY}  ip_dns2_step=0.1.0.0  ip_gateway_step=0.1.0.0  ip_version=4  lease_time_max=864000  local_mac_step=0000.0000.0001  local_mac_outer_step=0000.0001.0000  local_mtu=1500  pvc_incr_mode=both  qinq_incr_mode=both  ping_check=0  ping_timeout=1  single_address_pool=0  vlan_id_count=1  vlan_id_count_inner=1  vlan_id_inner=10  vlan_id_repeat=1  vlan_id_repeat_inner=1  vlan_id_step=1  vlan_id_step_inner=1  vlan_user_priority=0  vlan_user_priority_inner=0  vci=32  vci_count=4063  vci_repeat=1  vci_step=1  vpi=0  vpi_count=1  vpi_repeat=1  vpi_step=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_handles} =  Set Variable  ${result['handle']['dhcp_handle']}

################################################################################
# End DHCP Server Call
################################################################################


################################################################################
# Start DHCP Server Call
################################################################################


	${result} =  Emulation Dhcp Server Config  count=3  encapsulation=ETHERNET_II  handle=${dhcp_server_handles}  ip_address=20.20.0.1  ip_gateway=20.20.0.2  ip_prefix_length=16  ip_prefix_step=0.0.2.0  ip_repeat=1  ip_step=0.2.0.0  ipaddress_count=16000  ipaddress_pool=20.20.1.1  lease_time=3600  local_mac=0000.0002.0002  mode=modify  port_handle=@{portHandles}[0]  vlan_id=1  ipaddress_pool_step=0.5.0.0  ip_dns1=110.11.0.1  ip_dns1_step=0.10.0.0  ip_dns2=120.12.0.0  ip_dns2_step=0.20.0.0  ip_gateway_step=0.50.0.0  ip_version=4  lease_time_max=3600  local_mac_step=0000.0000.0002  local_mac_outer_step=0000.0002.0000  local_mtu=9500  pvc_incr_mode=both  qinq_incr_mode=inner  ping_check=1  ping_timeout=100  single_address_pool=1  vlan_id_count=2  vlan_id_count_inner=2  vlan_id_inner=10  vlan_id_repeat=2  vlan_id_repeat_inner=2  vlan_id_step=5  vlan_id_step_inner=5  vlan_user_priority=6  vlan_user_priority_inner=7  vci=32  vci_count=4063  vci_repeat=1  vci_step=1  vpi=0  vpi_count=1  vpi_repeat=1  vpi_step=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_handles} =  Set Variable  ${result['handle']['dhcp_handle']}

################################################################################
# END - DHCP Server modification
################################################################################















