*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.151/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.151/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.60/Port_name_in_all_stats_view/test.04_ISIS_info_stats.tcl
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

	
#########################################
# Configure the first IS-IS L1L2 router #
#########################################

	${result} =  Emulation Isis Config  mode=create  reset=1  port_handle=@{portHandles}[0]  intf_ip_addr=22.1.1.2  gateway_ip_addr=22.1.1.1  intf_ip_prefix_length=24  mac_address_init=0000.0000.0001  count=1  wide_metrics=1  discard_lsp=1  attach_bit=1  partition_repair=1  overloaded=1  lsp_refresh_interval=888  lsp_life_time=777  max_packet_size=1492  intf_metric=0  routing_level=L1L2  te_enable=1  te_max_bw=10  te_max_resv_bw=20  te_unresv_bw_priority0=10  te_unresv_bw_priority2=20  te_unresv_bw_priority3=30  te_unresv_bw_priority4=40  te_unresv_bw_priority5=50  te_unresv_bw_priority6=60  te_unresv_bw_priority7=70  te_metric=10
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${router_handle1} =  Get From Dictionary  ${result}  handle
	
#####################################################
# Add a stub route range for the first IS-IS router #
#####################################################
	
	${result} =  Emulation Isis Topology Route Config  mode=create  handle=${router_handle1}  type=stub  ip_version=4  stub_ip_start=44.0.0.1  stub_ip_pfx_len=20  stub_count=5  stub_metric=22  stub_up_down_bit=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
##########################################
# Configure the second IS-IS L1L2 router #
##########################################
	
	${result} =  Emulation Isis Config  mode=create  reset=1  port_handle=@{portHandles}[1]  intf_ip_addr=22.1.1.1  gateway_ip_addr=22.1.1.2  intf_ip_prefix_length=24  mac_address_init=0000.0000.0002  count=1  wide_metrics=1  discard_lsp=1  attach_bit=1  partition_repair=1  overloaded=1  lsp_refresh_interval=888  lsp_life_time=777  max_packet_size=1492  intf_metric=0  routing_level=L1L2  te_enable=1  te_max_bw=10  te_max_resv_bw=20  te_unresv_bw_priority0=10  te_unresv_bw_priority2=20  te_unresv_bw_priority3=30  te_unresv_bw_priority4=40  te_unresv_bw_priority5=50  te_unresv_bw_priority6=60  te_unresv_bw_priority7=70  te_metric=10
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${router_handle2} =  Get From Dictionary  ${result}  handle
	
######################################################
# Add a stub route range for the second IS-IS router #
######################################################
	
	${result} =  Emulation Isis Topology Route Config  mode=create  handle=${router_handle2}  type=stub  ip_version=4  stub_ip_start=55.0.0.3  stub_ip_pfx_len=14  stub_count=3  stub_metric=20  stub_up_down_bit=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
######################################
# Start the IS-IS protocol emulation #
######################################
	
	${result} =  Emulation Isis Control  port_handle=@{portHandles}[0]  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Isis Control  port_handle=@{portHandles}[1]  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
######################################
# Gather statistics IS-IS statistics #
######################################
	
	${result} =  Emulation Isis Info  handle=${router_handle1}  mode=stats
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result['@{portHandles}[0]']['port_name']}
	
	
	${result} =  Emulation Isis Info  handle=${router_handle2}  mode=stats
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result['@{portHandles}[1]']['port_name']}
	
	