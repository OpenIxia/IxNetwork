*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/NGPF_support/NGPF_Backwards_Compatibility/IP_MAC/CPF_FEA435780/test.21_CPF_Interface_ethernet_connected_IPv6_4port_5intf_default_steps.tcl
# Topology 4P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	12/5  12/6  12/7  12/8

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
	
###############################################################################
# Configure interface in the test IPv4 
################################################################################
	
	
	
	${result} =  Interface Config  port_handle=@{portHandles}[0] @{portHandles}[1] @{portHandles}[2] @{portHandles}[3]  connected_count=5  ipv6_intf_addr=12::100 13::100 14::100 15::100  ipv6_prefix_length=96 96 96 96  autonegotiation=1  src_mac_addr=00aa.00aa.0001 00bb.00bb.0001 00cc.00cc.0001 00dd.00dd.0001  op_mode=normal  intf_mode=ethernet  duplex=auto  speed=auto
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${intf_eth} =  Get From Dictionary  ${result}  ethernet_handle
	${intf_ipv6} =  Get From Dictionary  ${result}  ipv6_handle
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	