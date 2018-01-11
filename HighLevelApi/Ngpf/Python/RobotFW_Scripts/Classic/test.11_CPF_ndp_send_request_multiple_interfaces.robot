*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.104/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.104/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
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
	
	${result} =  Connect  reset=1  device=${chassis}  ixnetwork_tcl_server=${client}:${client_api_port}  port_list=@{portlist}  tcl_server=${chassis}  username=ixiaHLTQA
	${connect_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${connect_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	Log Many  @{portHandles}


################################################################################
#  Configure interfaces on first port
################################################################################
	#@{int_count_list}=  Create List  10  20  50  80  100  150
	@{int_count_list}=  Create List  10  20
	:FOR	${intf_count}	IN	@{int_count_list}
	\	Log	Configuring ${intf_count} interfaces
	\	${result} =  Interface Config  port_handle=@{portHandles}[0]  ipv6_intf_addr=3000:0::1  ipv6_prefix_length=64  autonegotiation=1  connected_count=${intf_count}  mode=config  speed=ether1000  ipv6_gateway=3000:0::151
	\	${interface_status} =  Get From Dictionary  ${result}  status
	\	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
################################################################################
#  Configure interfaces on second port
################################################################################
	\	Log	Configuring ${intf_count} interfaces
	\	${result} =  Interface Config  port_handle=@{portHandles}[1]  ipv6_intf_addr=3000:0::151  ipv6_prefix_length=64  autonegotiation=1  connected_count=${intf_count}  mode=config  speed=ether1000  ipv6_gateway=3000:0::1  
	\	${interface_status} =  Get From Dictionary  ${result}  status
	\	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

################################################################################
#  Send NDP request
################################################################################
	\	${result} =  Interface Config  mode=config  port_handle=@{portHandles}  enable_ndp=1  ndp_send_req=1
	\	Log	${result['@{portHandles}[0]']['router_solicitation_success']}
	\	Log	${result['@{portHandles}[1]']['router_solicitation_success']}
	\	${interface_status} =  Get From Dictionary  ${result}  status
	\	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
		:FOR	${port}	IN	@{portHandles}
		\	Log  Send RS on ${port}
		\	${failed_ndp} =  Set Variable  ${result['${port}']['router_solicitation_success']}
		\	Run Keyword If  '${failed_ndp}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${result} =  Interface Config  port_handle=@{portHandles}  mode=destroy
	${interface_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
		
		
		
		