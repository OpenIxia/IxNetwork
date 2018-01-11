*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/NGPF_support/NGPF_Backwards_Compatibility/IP_MAC/CPF_intf_modify/test.14_CPF_multiple_list_IPv6_connected_modify.tcl
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
	
################################################################################
# Configure interfaces                                                         #
################################################################################

	${result} =  Interface Config  port_handle=@{portHandles}[0] @{portHandles}[0] @{portHandles}[1] @{portHandles}[1]  ipv6_intf_addr=30::1:1 30::1:1 30::1:1 30::1:1  ipv6_gateway=30::1:2 30::1:2 30::1:1 30::1:1  ipv6_prefix_length=80  autonegotiation=1  op_mode=normal  target_link_layer_address=1 1 0 0  vlan=1 0 1 0  vlan_id=20 1 40 1  vlan_user_priority=2 0 4 0  vlan_tpid=0x8100  intf_mode=ethernet  src_mac_addr=0000.0000.000a 0000.0000.000b 0000.0000.000c 0000.0000.000d
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${interface_modif} =  Get From Dictionary  ${result}  interface_handle
	${eth} =  Get From Dictionary  ${result}  ethernet_handle

##############################################################################
# Modify interfaces in the test      
# IPv4                                 
##############################################################################
	
	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[0] @{portHandles}[0] @{portHandles}[1] @{portHandles}[1]  interface_handle=${interface_modif}  ipv6_intf_addr=20::1:1 20::1:1 20::1:2 20::1:2  ipv6_gateway=20::1:2 20::1:2 20::1:1 20::1:1  ipv6_prefix_length=60  autonegotiation=1  op_mode=normal  target_link_layer_address=1 0 1 0  vlan=1  vlan_id=120 130 120 130  vlan_user_priority=5 7 5 7  vlan_tpid=0x9100 0x8100 0x9100 0x8100  intf_mode=ethernet  src_mac_addr=0000.0000.001a 0000.0000.001b 0000.0000.001c 0000.0000.001d
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${interface_modif} =  Get From Dictionary  ${result}  interface_handle
	
	
	
	
	
	
	
	
	
	
	
	
	
	