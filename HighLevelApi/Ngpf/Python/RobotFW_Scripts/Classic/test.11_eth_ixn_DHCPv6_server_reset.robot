*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/DHCP/test.11_eth_ixn_DHCPv6_server_reset.tcl
# Topology 1P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.232
${client_api_port} =  	8136
@{portlist} =  	12/7
${client_and_port} =  ${client}:${client_api_port}


*** Test Cases ***
test
################################################################################
# START - Connect to the chassis and get port handles from the result
################################################################################

	${result} =  Connect  reset=1  device=${chassis}  ixnetwork_tcl_server=${client_and_port}  port_list=@{portlist}  username=ixiaHLTQA  break_locks=1  interactive=1
	${connect_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${connect_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}

# START - LAYER 1 INTERFACE CONFIG

	${result} =  Interface Config  port_handle=@{portHandles}[0]  mode=config  intf_mode=ethernet  autonegotiation=1  speed=auto  duplex=auto  phy_mode=copper
	${interface_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

# START - DHCP Server configuration
	${result} =  Emulation Dhcp Server Config  count=1  functional_specification=v4_v6_compatible  encapsulation=ethernet_ii_vlan  ip_address=3000::2  ip_step=0:0:0:3::0  ipv6_gateway=3000::1  ip_prefix_length=64  ip_prefix_step=3  ip_repeat=1  ipaddress_count=1000  ipaddress_pool=3000::3  ipaddress_pool_step=0::2:0:0:0  lease_time=86400  local_mac=0000.0001.0001  mode=create  port_handle=@{portHandles}[0]  vlan_id=200  ipaddress_pool_prefix_length=64  ipaddress_pool_prefix_step=2  ip_dns1=5000::1  ip_dns1_step=0::5:0:0:0  ip_dns2=6000::1  ip_dns2_step=0::6:0:0:0  ipv6_gateway_step=0::4  ip_version=6  lease_time_max=864000  local_mac_step=0000.0000.0001  local_mac_outer_step=0000.0001.0000  local_mtu=1500  ping_check=0  ping_timeout=1  single_address_pool=0  dhcp6_ia_type=iana_iapd
	${dhcp_server_config_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_server_config_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_handles} =  Set Variable  ${result['handle']['dhcp_handle']}

# Validate Iana_Iapd
	Log Many  "############### Check IxN Lowlevel vs HLT ##################"
	Ixnet  connect  ${client}  -port  ${client_api_port}  -version  8.20
	${root} =  Ixnet  getRoot
	${vports} =  Ixnet  getList  ${root}  vport
	${vport1} =  Get From List  ${vports}  0
	${protocolStack} =  Ixnet  getList  ${vport1}  protocolStack
	${protocolStack1} =  Get From List  ${protocolStack}  0
	${ethernet} =  Ixnet  getList  ${protocolStack1}  ethernet
	${ethernet1} =  Get From List  ${ethernet}  0
	${dhcpServerEndpoint} =  Ixnet  getList  ${ethernet1}  dhcpServerEndpoint
	${dhcpServerEndpoint1} =  Get From List  ${dhcpServerEndpoint}  0
	${range} =  Ixnet  getList  ${dhcpServerEndpoint1}  range
	${range1} =  Get From List  ${range}  0
	${IA_ixN} =  Ixnet  getList  ${range1}  dhcpServerRange
	${IA_ixN1} =  Get From List  ${IA_ixN}  0
	${IA_ixN2} =  Ixnet  getAttribute  ${IA_ixN1}  -dhcp6IaType

	Run Keyword If  '${IA_ixN2}' != 'IANA+IAPD'  FAIL  "Error: IA type misconfigured - LowLevel: ${IA_ixN2} - HLT: iana_iapd"  ELSE  Log  "IA type configured correctly - LowLevel: ${IA_ixN2} - HLT: iana_iapd"

###########START DHCP############
	${result} =  Emulation Dhcp Server Control  port_handle=@{portHandles}[0]  action=collect
	${control_status_1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status_1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	Sleep  20s

###########GET DHCP STATISTICS############
	
	${result} =  Emulation Dhcp Server Stats  port_handle=@{portHandles}[0]  ip_version=6  action=collect
	${dhcp_stats_1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_stats_1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	Sleep  5s

###########STOP DHCP SERVER############

	${result} =  Emulation Dhcp Server Control  port_handle=@{portHandles}[0]  action=abort
	${control_status_2} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status_2}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

###########RESET DHCP SERVER############

	${result} =  Emulation Dhcp Server Config  handle=${dhcp_server_handles}  mode=reset 
	${config_status_2} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${config_status_2}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

###########GET DHCP STATISTICS############

	${status}   ${result} =  Run Keyword And Ignore Error  Emulation Dhcp Server Stats  port_handle=@{portHandles}[0]  action=collect
	Run Keyword If  '${status}' != 'FAIL'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"









