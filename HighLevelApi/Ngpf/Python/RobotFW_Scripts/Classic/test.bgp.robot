*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.104/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.104/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.50/BGPoIP/test.01_bgp_over_ipv4_sm_traffic_stats.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.144
${client_api_port} =  	8139
@{portlist} =  	12/7  12/8

*** Test Cases ***
test
################################################################################
# START - Connect to the chassis and get port handles from the result
################################################################################

	${result} =  Connect  device=${chassis}  ixnetwork_tcl_server=${client}:${client_api_port}  port_list=@{portlist}  reset=1  tcl_server=${chassis}
	${connect_status} =  Get From Dictionary  ${result}  status
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	Log Many  @{portHandles}

################################################################################
# Configure multiple BGP Peers with count option on first port
################################################################################

	${result} =  Emulation BGP Config  mode=reset  port_handle=@{portHandles}[0]  ip_version=4  local_ip_addr=192.1.1.2  remote_ip_addr=192.1.1.1  local_addr_step=0.0.1.0  remote_addr_step=0.0.1.0  count=1  neighbor_type=internal  local_as=200  local_as_step=1  local_as_mode=increment
	${ce_bgp_neighbor_handle_list} =  Get From Dictionary  ${result}  handles
	${bgp_config_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${bgp_config_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

############################################################################
# Configure BGP routes on each BGP peer
############################################################################

	${result} =  Emulation BGP Route Config  mode=add   handle=${ce_bgp_neighbor_handle_list}  prefix=55.0.0.1  prefix_step=1  netmask=255.255.255.0  num_routes=1  ip_version=4  origin_route_enable=1  origin=igp
	${bgp_route_config_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${bgp_config_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

############################################################################
# Configure interface static endpoint on second port
############################################################################

	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[1]  mtu=1500  vlan=0  l23_config_type=static_endpoint  gateway=192.1.1.2  intf_ip_addr=192.1.1.1  netmask=255.255.255.0  check_opposite_ip_version=0  src_mac_addr=0000.0022.a90d  arp_on_linkup=0  ns_on_linkup=0  single_ns_per_gateway=1  single_arp_per_gateway=1
	${interface_handle} =  Get From Dictionary  ${result}  interface_handle
	${interface_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

################################################################################
# Configure multiple BGP Peers on the second Ixia port
################################################################################
	Log Many  Start BGP client configuration on $port_1 ...
	${result} =  Emulation BGP Config  mode=reset  port_handle=@{portHandles}[1]  handle=${ce_bgp_neighbor_handle_list}  interface_handle=${interface_handle}|1  ip_version=4  remote_ip_addr=192.1.1.2  local_addr_step=0.0.1.0  remote_addr_step=0.0.1.0  count=1  neighbor_type=internal  local_as=200  local_as_step=1  local_as_mode=increment
	${pe_bgp_neighbor_handle_list} =  Get From Dictionary  ${result}  handles
	${bgp_config_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${bgp_config_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

############################################################################
# Configure BGP routes on the second Ixia port
############################################################################
	
	${result} =  Emulation BGP Route Config  mode=add   handle=${pe_bgp_neighbor_handle_list}  prefix=70.0.0.1  prefix_step=1  netmask=255.255.255.0  num_routes=1  ip_version=4  origin_route_enable=1  origin=igp
	${bgp_route_config_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${bgp_config_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

################################################################################
# Start the BGP sessions
################################################################################
	Log Many  Start BGP protocol ...

	${result} =  Emulation Bgp Control  port_handle=@{portHandles}[0]  mode=start
	${bgp_config_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${bgp_config_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	${result} =  Emulation Bgp Control  port_handle=@{portHandles}[1]  mode=start
	${bgp_config_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${bgp_config_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

###################################################################################
#### Wait for the BGP sessions to establish on first port. 
#### Any BGP peer handle configured for the port can be provided to -handle 
#### parameter in order to retrive the BGP session' stats for the port.
###################################################################################
	${bgp_sessions_established}=    Set Variable    0
	${num_of_bgp_neighbors}=    Set Variable    1
	${retries}=    Set Variable    10
	: FOR    ${retries}    IN RANGE    0    10
		\	${result} =  Emulation BGP Info  handle=${ce_bgp_neighbor_handle_list}  mode=stats
		\	Log Many  Retrieving aggregate BGP stats ${ce_bgp_neighbor_handle_list}[0], number of retries left: ${retries} ...
		\	${bgp_sessions_established} =  Get From Dictionary  ${result}  sessions_established
		\	Run Keyword If  ${bgp_sessions_established} != ${num_of_bgp_neighbors}  Sleep  2s
		\		Exit For Loop If    ${bgp_sessions_established} >= 1
	Run Keyword If    ${bgp_sessions_established} != ${num_of_bgp_neighbors}  FAIL  Not all BGP sessions have been established  ELSE  Log  all BGP sessions have been established
	Log Many  There are ${bgp_sessions_established} BGP sessions established on @{portHandles}[0] ...

###################################################################################
#### Wait for the BGP sessions to establish on second port.
#### Any BGP peer handle configured for the port can be provided to -handle 
#### parameter in order to retrive the BGP session' stats for the port.
###################################################################################
	${bgp_sessions_established}=    Set Variable    0
	${num_of_bgp_neighbors}=    Set Variable    1
	${retries}=    Set Variable    10
	: FOR    ${retries}    IN RANGE    0    10
		\	${result} =  Emulation BGP Info  handle=${pe_bgp_neighbor_handle_list}  mode=stats
		\	Log Many  Retrieving aggregate BGP stats ${pe_bgp_neighbor_handle_list}[0], number of retries left: ${retries} ...
		\	${bgp_sessions_established} =  Get From Dictionary  ${result}  sessions_established
		\	Run Keyword If  ${bgp_sessions_established} != ${num_of_bgp_neighbors}  Sleep  2s
		\		Exit For Loop If    ${bgp_sessions_established} >= 1
	Run Keyword If    ${bgp_sessions_established} != ${num_of_bgp_neighbors}  FAIL  Not all BGP sessions have been established  ELSE  Log  all BGP sessions have been established
	Log Many  There are ${bgp_sessions_established} BGP sessions established on @{portHandles}[1] ...

################################################################################
# Use ixnetwork traffic generator to configure traffic from bgp routes on 
# the first port to the bgp routes on the second port. 
# The traffic flow is tracked by source/destination endpoint pair.
################################################################################
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  transmit_mode=continuous  name=IPv4_TRAFFIC  src_dest_mesh=one_to_one  route_mesh=one_to_one  circuit_type=none  circuit_endpoint_type=ipv4  emulation_src_handle=${ce_bgp_neighbor_handle_list}  emulation_dst_handle=${pe_bgp_neighbor_handle_list}  track_by=endpoint_pair  stream_packing=one_stream_per_endpoint_pair  rate_percent=10  tx_delay=10  length_mode=fixed  frame_size=512
	${traffic_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${traffic_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${trafficHandle} =  Get From Dictionary  ${result}  traffic_item  

################################################################################
# Start the traffic 
################################################################################

	${result} =  Traffic Control  action=run  traffic_generator=ixnetwork_540
	${traffic_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${traffic_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s

################################################################################
# Stop the traffic 
################################################################################

	${result} =  Traffic Control  action=stop  traffic_generator=ixnetwork_540
	${traffic_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${traffic_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s

################################################################################
# Gather and display aggregate statistics
################################################################################
	# ##Set variable
	@{aggregated_traffic_results_name}=    Create List    "Scheduled Frames Tx."  "Scheduled Frames Tx. Rate"  "Line Speed"  "Frames Tx."  "Total Frames Tx."  "Frames Tx. Rate"  "Frames Tx. Rate"  "Bytes Tx."  "Bytes Tx. Rate"  "Tx. Rate (bps)"  "Tx. Rate (Kbps)"  "Tx. Rate (Mbps)"  "Bytes Rx."  "Bytes Rx. Rate"  "Rx. Rate (bps)"  "Rx. Rate (Kbps)"  "Rx. Rate (Mbps)"  "Data Integrity Frames Rx."  "Data Integrity Errors"  "Valid Frames Rx."  "Valid Frames Rx. Rate"  
	@{aggregated_traffic_results}=    Create List    ['aggregate']['tx']['scheduled_pkt_count']  ['aggregate']['tx']['scheduled_pkt_rate']  ['aggregate']['tx']['line_speed']  ['aggregate']['tx']['pkt_count']  ['aggregate']['tx']['total_pkts']  ['aggregate']['tx']['pkt_rate']  ['aggregate']['tx']['total_pkt_rate']  ['aggregate']['tx']['pkt_byte_count']  ['aggregate']['tx']['pkt_byte_rate']  ['aggregate']['tx']['pkt_bit_rate']  ['aggregate']['tx']['pkt_kbit_rate']  ['aggregate']['tx']['pkt_mbit_rate']  ['aggregate']['rx']['pkt_byte_count']  ['aggregate']['rx']['pkt_byte_rate']  ['aggregate']['rx']['pkt_bit_rate']  ['aggregate']['rx']['pkt_kbit_rate']  ['aggregate']['rx']['pkt_mbit_rate']  ['aggregate']['rx']['data_int_frames_count']  ['aggregate']['rx']['data_int_errors_count']  ['aggregate']['rx']['pkt_count']  ['aggregate']['rx']['pkt_rate']
	
	${result} =  Traffic Stats  mode=aggregate  traffic_generator=ixnetwork_540
	:FOR	${port}	IN	@{portHandles}
	\	Log	Stats on current port are: ${port}
		:FOR    ${name}    IN    @{aggregated_traffic_results_name}
			\	Log  ${name}
				:FOR    ${key}    IN    @{aggregated_traffic_results}
			\	Log  Current ELEMENT IN List is: ${name} : ${result['${port}']${key}}
	
	Run Keyword If  ${result['@{portHandles}[0]']['aggregate']['tx']['pkt_count']} != ${result['@{portHandles}[1]']['aggregate']['rx']['pkt_count']}  FAIL  "Not all packets were received"  ELSE  Log  "All packets were received"