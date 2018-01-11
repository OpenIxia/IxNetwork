*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.104/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.104/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/DEV_REGR/Routing/EIGRP/test.EIGRP_modify_routes.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	12/7  12/8

*** Test Cases ***
test
################################################################################
# START - Connect to the chassis and get port handles from the result
################################################################################

	${result} =  Connect  device=${chassis}  ixnetwork_tcl_server=${client}:${client_api_port}  port_list=@{portlist}  reset=1  tcl_server=${chassis}  username=ixiaHLTQA
	${connect_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${connect_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	Log Many  @{portHandles}


################################################################################
# Configure interface in the test
################################################################################

	${result} =  Interface Config  port_handle=@{portHandles}[0]  autonegotiation=1  duplex=auto  speed=auto
	${interface_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Configure EIGRP routers
################################################################################

	${result} =  Emulation Eigrp Config  mode=create  reset=1  port_handle=@{portHandles}[0]  count=3  intf_ip_addr=25.0.0.2  intf_ip_addr_step=1.0.0.0  intf_ip_prefix_length=24  intf_gw_ip_addr=25.0.0.1  intf_gw_ip_addr_step=1.0.0.0  vlan=1  vlan_id=25  vlan_id_step=1  mac_address_init=0000.0000.0001  router_id=25.0.0.2  router_id_step=1.0.0.0  enable_piggyback=1  bfd_registration=1
	${eigrp_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${eigrp_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${router_handles} =  Get From Dictionary  ${result}  router_handles

################################################################################
# Configure EIGRP routes
################################################################################

	${result} =  Emulation Eigrp Route Config  mode=create  handle=${router_handles}  prefix_start=50.0.0.1  count=2  num_prefixes=10  next_hop=25.0.0.1  next_hop_outside_step=1.0.0.0
	${eigrp_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${eigrp_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${route_handle} =  Get From Dictionary  ${result}  route_handles
	@{route_handles} =  Split String    ${route_handle}
################################################################################
# Modify EIGRP routes
################################################################################
	
	@{route_handles}=  Get Slice From List  ${route_handles}  1  4
	${result} =  Emulation Eigrp Route Config  mode=modify  route_handle=@{route_handles}  next_hop=1.1.1.1
	${eigrp_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${eigrp_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"