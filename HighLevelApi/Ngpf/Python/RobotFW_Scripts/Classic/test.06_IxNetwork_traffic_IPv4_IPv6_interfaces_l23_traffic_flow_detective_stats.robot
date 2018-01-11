*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT3.80/Uds_Stats/test.06_IxNetwork_traffic_IPv4_IPv6_interfaces_l23_traffic_flow_detective_stats.tcl
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

	${result} =  Interface Config  port_handle=@{portHandles}[0] @{portHandles}[0] @{portHandles}[0] @{portHandles}[0] @{portHandles}[0]  intf_ip_addr=20.1.1.1 20.1.1.2 20.1.1.3 20.1.1.4 20.1.1.5  gateway=20.1.2.1 20.1.2.2 20.1.2.3 20.1.2.4 20.1.2.5  netmask=255.255.0.0  ipv6_intf_addr=2000:0:0:0:1:1:0:0 2000:0:0:0:1:2:0:0 2000:0:0:0:1:3:0:0 2000:0:0:0:1:4:0:0 2000:0:0:0:1:5:0:0  ipv6_prefix_length=64 64 64 64 64  ipv6_gateway=2000:0:0:0:2:1:0:0 2000:0:0:0:2:2:0:0 2000:0:0:0:2:3:0:0 2000:0:0:0:2:4:0:0 2000:0:0:0:2:5:0:0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${interface_handles_ipv4_1} =  Get From Dictionary  ${result}  interface_handle
	
	${result} =  Interface Config  port_handle=@{portHandles}[1] @{portHandles}[1] @{portHandles}[1] @{portHandles}[1] @{portHandles}[1]  intf_ip_addr=20.1.2.1 20.1.2.2 20.1.2.3 20.1.2.4 20.1.2.5  gateway=20.1.1.1 20.1.1.2 20.1.1.3 20.1.1.4 20.1.1.5  netmask=255.255.0.0  ipv6_intf_addr=2000:0:0:0:2:1:0:0 2000:0:0:0:2:2:0:0 2000:0:0:0:2:3:0:0 2000:0:0:0:2:4:0:0 2000:0:0:0:2:5:0:0  ipv6_prefix_length=64 64 64 64 64  ipv6_gateway=2000:0:0:0:1:1:0:0 2000:0:0:0:1:2:0:0 2000:0:0:0:1:3:0:0 2000:0:0:0:1:4:0:0 2000:0:0:0:1:5:0:0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${interface_handles_ipv4_2} =  Get From Dictionary  ${result}  interface_handle

################################################################################
# Configure interfaces - IPv6
################################################################################
	
	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[0] @{portHandles}[0] @{portHandles}[0] @{portHandles}[0] @{portHandles}[0]  ipv6_intf_addr=2000:0:0:0:1:1:0:0 2000:0:0:0:1:2:0:0 2000:0:0:0:1:3:0:0 2000:0:0:0:1:4:0:0 2000:0:0:0:1:5:0:0  ipv6_prefix_length=64 64 64 64 64  ipv6_gateway=2000:0:0:0:2:1:0:0 2000:0:0:0:2:2:0:0 2000:0:0:0:2:3:0:0 2000:0:0:0:2:4:0:0 2000:0:0:0:2:5:0:0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${interface_handles_ipv6_1} =  Get From Dictionary  ${result}  interface_handle
	
	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[1] @{portHandles}[1] @{portHandles}[1] @{portHandles}[1] @{portHandles}[1]  ipv6_intf_addr=2000:0:0:0:2:1:0:0 2000:0:0:0:2:2:0:0 2000:0:0:0:2:3:0:0 2000:0:0:0:2:4:0:0 2000:0:0:0:2:5:0:0  ipv6_prefix_length=64 64 64 64 64  ipv6_gateway=2000:0:0:0:1:1:0:0 2000:0:0:0:1:2:0:0 2000:0:0:0:1:3:0:0 2000:0:0:0:1:4:0:0 2000:0:0:0:1:5:0:0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${interface_handles_ipv6_2} =  Get From Dictionary  ${result}  interface_handle

################################################################################
# Delete all the streams first
################################################################################
	
	${result} =  Traffic Control  action=reset  traffic_generator=ixnetwork
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Create traffic items - IPv4
################################################################################
	
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  transmit_mode=continuous  name=IPv4_Traffic  src_dest_mesh=fully  route_mesh=fully  circuit_type=none  circuit_endpoint_type=ipv4  emulation_src_handle=${interface_handles_ipv4_1}  emulation_dst_handle=${interface_handles_ipv4_2}  track_by=source_ip  rate_percent=5  l3_protocol=ipv4  ip_src_tracking=1  ip_dst_tracking=1  ip_precedence_tracking=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Create traffic items - IPv6
################################################################################
	
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  transmit_mode=continuous  name=IPv6_Traffic  src_dest_mesh=fully  route_mesh=fully  circuit_type=none  circuit_endpoint_type=ipv6  emulation_src_handle=${interface_handles_ipv6_1}  emulation_dst_handle=${interface_handles_ipv6_2}  track_by=endpoint_pair  rate_percent=5  l3_protocol=ipv4  ip_src_tracking=1  ip_dst_tracking=1  ip_precedence_tracking=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Start the traffic 
################################################################################
	
	${result} =  Traffic Control  action=run  traffic_generator=ixnetwork_540
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
################################################################################
# Wait for the traffic to be transmitted
################################################################################
	Sleep  25s
	
################################################################################
# Stop the traffic 
################################################################################
	
	${result} =  Traffic Control  action=stop  traffic_generator=ixnetwork_540
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Wait for the traffic to stop 
################################################################################
	Sleep  5s
	
################################################################################
# Collect stats without filters
################################################################################
	
	${result} =  Traffic Stats  traffic_generator=ixnetwork_540  mode=user_defined_stats  uds_type=l23_traffic_flow_detective  uds_action=get_stats
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

################################################################################
# Collect stats with traffic item filters
################################################################################
	
	${result} =  Traffic Stats  traffic_generator=ixnetwork_540  mode=user_defined_stats  uds_type=l23_traffic_flow_detective  uds_action=get_available_traffic_item_filters
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${filters_list} =  Get From Dictionary  ${result}  filters
	@{filters_list} =  Split String  ${filters_list}
	:FOR	${filter}	IN	@{filters_list}
	\	${result} =  Traffic Stats  traffic_generator=ixnetwork_540  mode=user_defined_stats  uds_type=l23_traffic_flow_detective  uds_action=get_stats  uds_traffic_item_filter=${filter}
	\	${status} =  Get From Dictionary  ${result}  status
	\	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Collect stats with traffic item and tracking filters
################################################################################
	
	${result} =  Traffic Stats  traffic_generator=ixnetwork_540  mode=user_defined_stats  uds_type=l23_traffic_flow_detective  uds_action=get_available_traffic_item_filters
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ti_filters_list} =  Get From Dictionary  ${result}  filters
	@{ti_filters_list} =  Split String  ${ti_filters_list}
	:FOR	${ti_filter}	IN	@{ti_filters_list}
		\	${result} =  Traffic Stats  traffic_generator=ixnetwork_540  mode=user_defined_stats  uds_type=l23_traffic_flow_detective  uds_action=get_available_tracking_filters  uds_traffic_item_filter=${ti_filter}
		\	${status} =  Get From Dictionary  ${result}  status
		\	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
		
		\	${result} =  Traffic Stats  traffic_generator=ixnetwork_540  mode=user_defined_stats  uds_type=l23_traffic_flow_detective  uds_action=get_stats  uds_traffic_item_filter=${ti_filter}  uds_l23tfd_flow_type=all_flows  uds_l23tfd_dead_flows_treshold=5  uds_tracking_filter_count=1  uds_l23tfd_tracking_operator=is_equal  uds_l23tfd_tracking_value=20.1.1.1/255.255.255.0  uds_statistic_filter_count=1    uds_l23tfd_statistic_operator=is_equal_or_greater  uds_l23tfd_statistic_value=0
		\	${status} =  Get From Dictionary  ${result}  status
		\	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	
	
	
	
	
	
	
	
