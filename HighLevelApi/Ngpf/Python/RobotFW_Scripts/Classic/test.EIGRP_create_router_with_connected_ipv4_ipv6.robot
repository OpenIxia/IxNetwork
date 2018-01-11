*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/DEV_REGR/Routing/EIGRP/test.EIGRP_create_router_with_connected_ipv4_ipv6.tcl
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
# Configure interface in the test
################################################################################

	${result} =  Interface Config  port_handle=@{portHandles}[0]  autonegotiation=1  duplex=auto  speed=auto
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Configure EIGRP routers
################################################################################
	
	${result} =  Emulation Eigrp Config  mode=create  reset=1  port_handle=@{portHandles}[0]  count=3  intf_ip_addr=25.0.0.2  intf_ip_addr_step=1.0.0.0  intf_ip_prefix_length=24  intf_gw_ip_addr=25.0.0.1  intf_gw_ip_addr_step=1.0.0.0  intf_ipv6_addr=25::2  intf_ipv6_addr_step=0:1::0  intf_ipv6_prefix_length=24  vlan=1  vlan_id=25  vlan_id_step=1  mac_address_init=0000.0000.0001  router_id=25.0.0.2  router_id_step=1.0.0.0  enable_piggyback=1  bfd_registration=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	