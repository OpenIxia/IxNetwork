*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.00/IPv6_Gateway/test.05_ixn_gre_interface_ipv6_ipv4.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.191
${client} =  	10.215.133.232
${client_api_port} =  	8136
@{portlist} =  	11/1  11/3

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
# Configure interface in the test
################################################################################

	${result} =  Interface Config  mode=config  port_handle=@{portHandles}[0]  gre_count=2  gre_dst_ip_addr=2001::1:2  gre_dst_ip_addr_step=::1  gre_ip_addr=9.9.10.1  gre_ip_addr_step=0.0.0.1  gre_ip_prefix_length=24  ipv6_intf_addr=2001::1:1  ipv6_intf_addr_step=::1  ipv6_gateway=2001::1:2  l23_config_type=protocol_interface
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	${result} =  Interface Config  mode=config  port_handle=@{portHandles}[1]  gre_count=2  gre_dst_ip_addr=2001::1:1  gre_dst_ip_addr_step=::1  gre_ip_addr=9.9.10.2  gre_ip_addr_step=0.0.0.1  gre_ip_prefix_length=24  ipv6_intf_addr=2001::1:2  ipv6_intf_addr_step=::1  ipv6_gateway=2001::1:1  l23_config_type=protocol_interface
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	