*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/PPP/test.6_LEGACY_IxNetwork_PPPoE_missing_intermediate_agent_dependencies.tcl
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
# END - Connect to the chassis
################################################################################

################################################################################
# Start RSVP Call - port_0 - Ingress
################################################################################
	
	${result} =  Emulation Rsvp Config  mode=create  count=1  intf_ip_addr=1.1.1.1  intf_prefix_length=24  ip_version=4  neighbor_intf_ip_addr=1.1.1.2  port_handle=@{portHandles}[0]  reset=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${rsvpHandleList} =  Get From Dictionary  ${result}  handles
	${rsvpHandleList_ingress} =  Set Variable  ${rsvpHandleList}
################################################################################
# END - RSVP configuration - Ingress
################################################################################
	
################################################################################
# START - RSVP configuration $port_1 - Egress
################################################################################
	
	${result} =  Emulation Rsvp Config  mode=create  count=1  intf_ip_addr=1.1.1.2  intf_prefix_length=24  ip_version=4  neighbor_intf_ip_addr=1.1.1.1  port_handle=@{portHandles}[1]  reset=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${rsvpHandleList} =  Get From Dictionary  ${result}  handles
	${rsvpHandleList_egress} =  Set Variable  ${rsvpHandleList}
	
################################################################################
# END - RSVP configuration - Egress
################################################################################
	
################################################################################
# START - RSVP Tunnel configuration - Ingress
################################################################################
	
	${result} =  Emulation Rsvp Tunnel Config  count=1  emulation_type=rsvptep2mp  handle=${rsvpHandleList_ingress}  mode=create  port_handle=@{portHandles}[0]  rsvp_behavior=rsvpIngress  egress_ip_addr=5.5.5.1  egress_ip_step=0.0.1.0  egress_leaf_ip_count=10  egress_leaf_range_count=10  egress_leaf_range_step=0.0.1.0  p2mp_id=1  ingress_ip_addr=4.4.4.1  lsp_id_start=0  tunnel_id_start=1  head_traffic_start_ip=100.100.100.100  tail_traffic_start_ip=224.0.0.20
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${rsvpTunnelHandleList} =  Get From Dictionary  ${result}  tunnel_handle
	${rsvp_ingress_handle} =  Set Variable  ${rsvpTunnelHandleList}
	
################################################################################
# End RSVP Tunnel Call
################################################################################
	
################################################################################
# START - RSVP Tunnel configuration - Egress
################################################################################
	
	${result} =  Emulation Rsvp Tunnel Config  mode=create  count=1  emulation_type=rsvptep2mp  handle=${rsvpHandleList_egress}  port_handle=@{portHandles}[1]  rsvp_behavior=rsvpEgress  egress_ip_addr=5.5.5.1  egress_ip_step=0.0.1.0  egress_leaf_ip_count=10  egress_leaf_range_count=10  egress_leaf_range_step=0.0.1.0  p2mp_id=1  tail_traffic_start_ip=224.0.0.20
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${rsvpTunnelHandleList} =  Get From Dictionary  ${result}  tunnel_handle
	${rsvp_egress_handle} =  Set Variable  ${rsvpTunnelHandleList}
	
################################################################################
# End RSVP Tunnel Call
################################################################################
	
################################################################################
# Start - RSVP emulation - Egress
################################################################################
	${result} =  Emulation Rsvp Control  mode=start  handle=${rsvp_egress_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
################################################################################
# Start - RSVP emulation - Ingress
################################################################################
	${result} =  Emulation Rsvp Control  mode=start  handle=${rsvp_ingress_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# RSVP Tunnel info - Ingress - handle
################################################################################
	
	${result} =  Emulation Rsvp Tunnel Info  handle=${rsvp_ingress_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	