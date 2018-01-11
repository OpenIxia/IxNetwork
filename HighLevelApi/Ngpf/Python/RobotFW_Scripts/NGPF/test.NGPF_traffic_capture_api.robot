*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  OperatingSystem  WITH NAME  OS
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.147/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.147/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.191
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	11/1  11/3
${client_and_port} =  ${client}:${client_api_port}
${dirname} =  	/home/pythar/ROBOT/protocols\ test\ cases
*** Test Cases ***
test
################################################################################
# START - Connect to the chassis and get port handles from the result
################################################################################

	${result} =  Connect  device=${chassis}  reset=1  ixnetwork_tcl_server=${client_and_port}  port_list=@{portlist}  username=ixiaHLTQA  break_locks=1  interactive=1
	${connect_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${connect_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	
########################################
# Configure the IPv4 interfaces        #
########################################

	${result} =  Interface Config  port_handle=@{portHandles}  intf_ip_addr=1.1.1.2 1.1.1.1  gateway=1.1.1.1 1.1.1.2  netmask=255.255.255.0 255.255.255.0  autonegotiation=1 1  duplex=full full  src_mac_addr=0000.debb.0001 0000.debb.0002  speed=ether1000 ether1000  port_rx_mode=capture capture
	${interface_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_list} =  Get From Dictionary  ${result}  ipv4_handle
	@{ipv4_handles} =  Split String  ${ipv4_list}
	 
##################################
#  Configure streams on TX port  #
##################################

	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=@{ipv4_handles}[0]  emulation_dst_handle=@{ipv4_handles}[1]  global_dest_mac_retry_count=1  global_dest_mac_retry_delay=5  enable_data_integrity=1  global_enable_dest_mac_retry=1  global_enable_min_frame_size=0  global_enable_staggered_transmit=0  global_enable_stream_ordering=0  global_stream_control=continuous  global_stream_control_iterations=1  global_large_error_threshhold=2  global_enable_mac_change_on_fly=0  global_max_traffic_generation_queries=500  global_mpls_label_learning_timeout=30  global_refresh_learned_info_before_apply=0  global_use_tx_rx_sync=1  global_wait_time=1  global_display_mpls_current_label_value=0  frame_sequencing=disable  frame_sequencing_mode=rx_threshold  src_dest_mesh=one_to_one  route_mesh=one_to_one  bidirectional=0  allow_self_destined=0  enable_dynamic_mpls_labels=0  hosts_per_net=1  name=Traffic_Item_1  source_filter=all  destination_filter=all  merge_destinations=1  circuit_endpoint_type=ipv4  egress_tracking=none
	${traffic_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${traffic_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${traffic_item} =  Get From Dictionary  ${result}  traffic_item
	
	${result} =  Interface Config  port_handle=@{portHandles}[1]  arp_send_req=1
	${interface_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  10s
	
	${result} =  Interface Config  port_handle=@{portHandles}[0]  arp_send_req=1
	${interface_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
# Clear stats before sending traffic
	
	${result} =  Traffic Control  port_handle=@{portHandles}  action=clear_stats
	${clear_stats_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${clear_stats_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  5s
	
####################################
#  Configure triggers and filters  #
####################################
	
	${result} =  Packet Config Buffers  port_handle=@{portHandles}[1]  capture_mode=trigger
	${config_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${config_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Packet Config Filter  port_handle=@{portHandles}[1]
	${config_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${config_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Packet Config Triggers  port_handle=@{portHandles}[1]  capture_trigger=1  capture_trigger_framesize=1  capture_trigger_framesize_from=62  capture_trigger_framesize_to=67  capture_filter=1  capture_filter_framesize=1  capture_filter_framesize_from=62  capture_filter_framesize_to=67  uds1=1  uds1_framesize=1  uds1_framesize_from=62  uds1_framesize_to=67  uds2=1  uds2_framesize=1  uds2_framesize_from=68  uds2_framesize_to=1020
	${config_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${config_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  5s
	
#########################
# Start capture on port #
#########################

	Log  Starting capture ...
	
	${result} =  Packet Control  port_handle=@{portHandles}[1]  action=start  packet_type=data
	${start_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${start_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  10s
	
	Log  Capturing ...
	
#########################
# Start traffic on port #
#########################
	Log  Start Traffic ...
	${result} =  Traffic Control  handle=${traffic_item}  action=run
	${traffic_control_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${traffic_control_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  15s
	
#########################
# Stop traffic on port  #
#########################
	Log  Stop Traffic ...
	${result} =  Traffic Control  handle=${traffic_item}  action=stop
	${traffic_control_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${traffic_control_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  20s
	
#########################
# Stop capture on port  #
#########################
	
	Log  Stopping capture ...
	
	${result} =  Packet Control  port_handle=@{portHandles}[1]  action=stop
	${stop_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${stop_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  15s
	
#############################################
# Get capture and statistics to csv         #
#############################################
	
	Log  Dirname ${EXECDIR}
	${result} =  Packet Stats  port_handle=@{portHandles}[1]  format=csv  stop=1  dirname=${EXECDIR}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${data_file} =  Set Variable  ${result['@{portHandles}[1]']['data_file']}
	${data_file} =  Set Variable  ${/}${data_file}
	${check_file_exist} =  OS.File Should Exist  ${data_file}  msg=CSV File Do Not Exist
	${remove_file} =  OS.Remove File  ${data_file}
	
	
	
	
	
	