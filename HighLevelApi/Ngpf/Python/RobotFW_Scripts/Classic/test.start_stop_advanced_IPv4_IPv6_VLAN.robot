*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.60/DualStackPPPoverL2TP/test.90_DualStackPPPServer_session_dhcpv6_vlan.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.191
${client} =  	10.215.133.232
${client_api_port} =  	8136
@{portlist} =  	9/1  9/2

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
# Configure Protocol Interfaces on both ports                                  #
################################################################################

	${result} =  Interface Config  mode=config  port_handle=@{portHandles}[0]  transmit_clock_source=external  internal_ppm_adjust=0  data_integrity=1  intf_mode=ethernet  duplex=full  autonegotiation=1  phy_mode=copper  transmit_mode=advanced  tx_gap_control_mode=fixed
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Interface Config  mode=config  port_handle=@{portHandles}[1]  transmit_clock_source=external  internal_ppm_adjust=0  data_integrity=1  intf_mode=ethernet  duplex=full  autonegotiation=1  phy_mode=copper  transmit_mode=advanced  tx_gap_control_mode=fixed
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[0]  vlan=0  l23_config_type=protocol_interface  mtu=1500  gateway=10.10.10.1  ipv6_intf_addr=2001::1  ipv6_gateway=2001::2  ipv6_prefix_length=64  intf_ip_addr=10.10.10.2  netmask=255.255.255.0  check_opposite_ip_version=0  src_mac_addr=0000.0107.4232
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${src_handle} =  Get From Dictionary  ${result}  interface_handle
	
	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[1]  vlan=0  l23_config_type=protocol_interface  mtu=1500  gateway=10.10.10.2  ipv6_intf_addr=2001::2  ipv6_gateway=2001::1  ipv6_prefix_length=64  intf_ip_addr=10.10.10.1  netmask=255.255.255.0  check_opposite_ip_version=0  src_mac_addr=0000.0107.4233
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dest_handle} =  Get From Dictionary  ${result}  interface_handle
	
############## Configure MAC+VLAN ##################
	
	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[1]  l23_config_type=protocol_interface  static_enable=1  static_mac_dst=0000.0376.4456  static_vlan_enable=1  static_vlan_id=200  static_lan_range_count=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dest_vlan} =  Get From Dictionary  ${result}  interface_handle
	
	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[0]  l23_config_type=protocol_interface  static_enable=1  static_mac_dst=0000.0476.4456  static_vlan_enable=1  static_vlan_id=200  static_lan_range_count=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${src_vlan} =  Get From Dictionary  ${result}  interface_handle
	
################################################################################
#                 Configure Traffic on ports                                   #
################################################################################
	Log To Console  Configure Traffic...
	${result} =  Traffic Control  action=reset  traffic_generator=ixnetwork_540  cpdp_convergence_enable=0  delay_variation_enable=0  packet_loss_duration_enable=0  latency_bins=3  latency_values=1.5 3 6.8  latency_control=store_and_forward
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
####################### one_te_one traffic ####################################
	
	${result} =  Traffic Config  mode=create  preamble_size_mode=auto  transmit_mode=continuous  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${src_handle}  emulation_dst_handle=${dest_handle}  global_dest_mac_retry_count=1  global_dest_mac_retry_delay=5  enable_data_integrity=1  global_enable_dest_mac_retry=1  global_enable_min_frame_size=0  global_enable_staggered_transmit=0  global_enable_stream_ordering=0  global_stream_control=continuous  global_stream_control_iterations=1  global_large_error_threshhold=2  global_enable_mac_change_on_fly=0  global_max_traffic_generation_queries=500  global_mpls_label_learning_timeout=30  global_refresh_learned_info_before_apply=0  global_use_tx_rx_sync=1  global_wait_time=1  global_display_mpls_current_label_value=0  frame_sequencing=disable  frame_sequencing_mode=rx_threshold  src_dest_mesh=one_to_one  route_mesh=one_to_one  bidirectional=1  allow_self_destined=0  enable_dynamic_mpls_labels=0  hosts_per_net=1  name=Traffic_IPv4_o2o  source_filter=all  destination_filter=all  merge_destinations=1  circuit_endpoint_type=ipv4  l2_encap=ethernet_ii  preamble_custom_size=8  data_pattern=AAAA  data_pattern_mode=incr_byte  track_by=ipv4Precedence0 ipv4DestIp0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_stream_id_1} =  Get From Dictionary  ${result}  stream_id
	${ipv4_config_element_1} =  Get From Dictionary  ${result}  traffic_item
	${ipv4_titem_1} =  Fetch From Left  ${ipv4_config_element_1}  /configElement
	
	${result} =  Traffic Config  mode=create  preamble_size_mode=auto  transmit_mode=continuous  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${src_vlan}  emulation_dst_handle=${dest_vlan}  global_dest_mac_retry_count=1  global_dest_mac_retry_delay=5  enable_data_integrity=1  global_enable_dest_mac_retry=1  global_enable_min_frame_size=0  global_enable_staggered_transmit=0  global_enable_stream_ordering=0  global_stream_control=continuous  global_stream_control_iterations=1  global_large_error_threshhold=2  global_enable_mac_change_on_fly=0  global_max_traffic_generation_queries=500  global_mpls_label_learning_timeout=30  global_refresh_learned_info_before_apply=0  global_use_tx_rx_sync=1  global_wait_time=1  global_display_mpls_current_label_value=0  frame_sequencing=disable  frame_sequencing_mode=rx_threshold  src_dest_mesh=one_to_one  route_mesh=one_to_one  bidirectional=1  source_filter=all  destination_filter=all  allow_self_destined=0  enable_dynamic_mpls_labels=0  hosts_per_net=1  name=Traffic_VLAN_o2o  merge_destinations=1  circuit_endpoint_type=ethernet_vlan  l2_encap=ethernet_ii  preamble_custom_size=8  data_pattern=AAAA  data_pattern_mode=incr_byte
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vlan_stream_id_1} =  Get From Dictionary  ${result}  stream_id
	${vlan_config_element_1} =  Get From Dictionary  ${result}  traffic_item
	${vlan_titem_1} =  Fetch From Left  ${vlan_config_element_1}  /configElement
	
################## fully meshed traffic ###############################
	
	${result} =  Traffic Config  mode=create  preamble_size_mode=auto  transmit_mode=continuous  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${dest_handle}  emulation_dst_handle=${src_handle}  global_dest_mac_retry_count=1  global_dest_mac_retry_delay=5  enable_data_integrity=1  global_enable_dest_mac_retry=1  global_enable_min_frame_size=0  global_enable_staggered_transmit=0  global_enable_stream_ordering=0  global_stream_control=continuous  global_stream_control_iterations=1  global_large_error_threshhold=2  global_enable_mac_change_on_fly=0  global_max_traffic_generation_queries=500  global_mpls_label_learning_timeout=30  global_refresh_learned_info_before_apply=0  global_use_tx_rx_sync=1  global_wait_time=1  global_display_mpls_current_label_value=0  frame_sequencing=disable  frame_sequencing_mode=rx_threshold  src_dest_mesh=fully  route_mesh=fully  bidirectional=1  allow_self_destined=0  source_filter=all  destination_filter=all  allow_self_destined=0  enable_dynamic_mpls_labels=0  hosts_per_net=1  name=Traffic_IPv6_fully  merge_destinations=1  circuit_endpoint_type=ipv6  l2_encap=ethernet_ii  preamble_custom_size=8  data_pattern=AAAA  data_pattern_mode=incr_byte  track_by=ipv6_flow_label
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6_stream_id_2} =  Get From Dictionary  ${result}  stream_id
	${ipv6_config_element_2} =  Get From Dictionary  ${result}  traffic_item
	${ipv6_titem_2} =  Fetch From Left  ${ipv6_config_element_2}  /configElement
	
	${result} =  Traffic Config  mode=create  preamble_size_mode=auto  transmit_mode=continuous  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${dest_vlan}  emulation_dst_handle=${src_vlan}  global_dest_mac_retry_count=1  global_dest_mac_retry_delay=5  enable_data_integrity=1  global_enable_dest_mac_retry=1  global_enable_min_frame_size=0  global_enable_staggered_transmit=0  global_enable_stream_ordering=0  global_stream_control=continuous  global_stream_control_iterations=1  global_large_error_threshhold=2  global_enable_mac_change_on_fly=0  global_max_traffic_generation_queries=500  global_mpls_label_learning_timeout=30  global_refresh_learned_info_before_apply=0  global_use_tx_rx_sync=1  global_wait_time=1  global_display_mpls_current_label_value=0  frame_sequencing=disable  frame_sequencing_mode=rx_threshold  src_dest_mesh=fully  route_mesh=fully  bidirectional=0  source_filter=all  destination_filter=all  allow_self_destined=0  enable_dynamic_mpls_labels=0  hosts_per_net=1  name=Traffic_VLAN_fully  merge_destinations=1  circuit_endpoint_type=ethernet_vlan  l2_encap=ethernet_ii  preamble_custom_size=8  data_pattern=AAAA  data_pattern_mode=incr_byte
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vlan_stream_id_2} =  Get From Dictionary  ${result}  stream_id
	${vlan_config_element_2} =  Get From Dictionary  ${result}  traffic_item
	${vlan_titem_2} =  Fetch From Left  ${vlan_config_element_2}  /configElement
	
################## one to many traffic endpoints ###########################
	
	${result} =  Traffic Config  mode=create  preamble_size_mode=auto  transmit_mode=continuous  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${src_handle}  emulation_dst_handle=${dest_handle}  global_dest_mac_retry_count=1  global_dest_mac_retry_delay=5  enable_data_integrity=1  global_enable_dest_mac_retry=1  global_enable_min_frame_size=0  global_enable_staggered_transmit=0  global_enable_stream_ordering=0  global_stream_control=continuous  global_stream_control_iterations=1  global_large_error_threshhold=2  global_enable_mac_change_on_fly=0  global_max_traffic_generation_queries=500  global_mpls_label_learning_timeout=30  global_refresh_learned_info_before_apply=0  global_use_tx_rx_sync=1  global_wait_time=1  global_display_mpls_current_label_value=0  frame_sequencing=disable  frame_sequencing_mode=rx_threshold  src_dest_mesh=many_to_many  route_mesh=one_to_one  bidirectional=1  allow_self_destined=0  source_filter=all  destination_filter=all  allow_self_destined=0  enable_dynamic_mpls_labels=0  hosts_per_net=1  name=Traffic_IPv6_o2M  merge_destinations=1  circuit_endpoint_type=ipv6  l2_encap=ethernet_ii  preamble_custom_size=8  data_pattern=AAAA  data_pattern_mode=incr_byte  track_by=ipv6_flow_label
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6_stream_id_3} =  Get From Dictionary  ${result}  stream_id
	${ipv6_config_element_3} =  Get From Dictionary  ${result}  traffic_item
	${ipv6_titem_3} =  Fetch From Left  ${ipv6_config_element_3}  /configElement
	
	${result} =  Traffic Config  mode=create  preamble_size_mode=auto  transmit_mode=continuous  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${dest_handle}  emulation_dst_handle=${src_handle}  global_dest_mac_retry_count=1  global_dest_mac_retry_delay=5  enable_data_integrity=1  global_enable_dest_mac_retry=1  global_enable_min_frame_size=0  global_enable_staggered_transmit=0  global_enable_stream_ordering=0  global_stream_control=continuous  global_stream_control_iterations=1  global_large_error_threshhold=2  global_enable_mac_change_on_fly=0  global_max_traffic_generation_queries=500  global_mpls_label_learning_timeout=30  global_refresh_learned_info_before_apply=0  global_use_tx_rx_sync=1  global_wait_time=1  global_display_mpls_current_label_value=0  frame_sequencing=disable  frame_sequencing_mode=rx_threshold  src_dest_mesh=many_to_many  route_mesh=one_to_one  bidirectional=1  allow_self_destined=0  enable_dynamic_mpls_labels=0  hosts_per_net=1  name=Traffic_IPv4_o2M  source_filter=all  destination_filter=all  merge_destinations=1  circuit_endpoint_type=ipv4  l2_encap=ethernet_ii  preamble_custom_size=8  data_pattern=AAAA  data_pattern_mode=incr_byte  track_by=ipv4Precedence0 ipv4DestIp0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_stream_id_3} =  Get From Dictionary  ${result}  stream_id
	${ipv4_config_element_3} =  Get From Dictionary  ${result}  traffic_item
	${ipv4_titem_3} =  Fetch From Left  ${ipv4_config_element_3}  /configElement
	
################################################################################
#                 Start/stop individual traffic items                          #
################################################################################
	
	Log To Console  Starting IPV6 and MAC+VLAN traffic
	${result} =  Traffic Control  action=run  handle=${ipv6_titem_2} ${ipv6_config_element_3}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${result} =  Traffic Control  action=run  handle=${vlan_stream_id_1} ${vlan_titem_2}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  25s
	
 ################# Stop MAC traffic and start IPv4 traffic ###################
	

	${result} =  Traffic Control  action=stop  handle=${vlan_stream_id_1} ${vlan_titem_2}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  15s
	${result} =  Traffic Control  action=run  handle=${ipv4_config_element_1} ${ipv4_stream_id_3}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  20s
 ################ Stop IPv6 and Start MAC #################################
	
	${result} =  Traffic Control  action=run  handle=${vlan_stream_id_1} ${vlan_titem_2}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  20s
	${result} =  Traffic Control  action=stop  handle=${ipv6_stream_id_2} ${ipv6_stream_id_3}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  15s
	
 ################ Stop all trafic #################################
	
	${result} =  Traffic Control  action=stop  handle=${vlan_config_element_1} ${vlan_config_element_2} ${ipv4_stream_id_1} ${ipv4_stream_id_3} ${ipv6_titem_2} ${ipv6_titem_3}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  15s
	
	
	
	