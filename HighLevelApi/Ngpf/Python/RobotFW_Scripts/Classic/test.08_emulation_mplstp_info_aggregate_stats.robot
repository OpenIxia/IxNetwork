*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.20/mplstp/test.08_emulation_mplstp_info_aggregate_stats.tcl
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
	
	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[0]  mtu=1500  vlan=0  l23_config_type=protocol_interface  gateway=20.20.20.1  intf_ip_addr=20.20.20.2  netmask=255.255.255.0  check_opposite_ip_version=0  src_mac_addr=0000.24fa.2c3e  arp_on_linkup=0  ns_on_linkup=0  single_arp_per_gateway=1  single_ns_per_gateway=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[0]  mtu=1500  vlan=0  l23_config_type=protocol_interface  check_opposite_ip_version=0  src_mac_addr=0000.3017.82d4  arp_on_linkup=0  ns_on_linkup=0  single_arp_per_gateway=1  single_ns_per_gateway=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${intf_0} =  Get From Dictionary  ${result}  interface_handle
	
	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[1]  mtu=1500  vlan=0  l23_config_type=protocol_interface  check_opposite_ip_version=0  src_mac_addr=0000.3018.82cb  arp_on_linkup=0  ns_on_linkup=0  single_arp_per_gateway=1  single_ns_per_gateway=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[1]  mtu=1500  vlan=0  l23_config_type=protocol_interface  gateway=20.20.20.2  intf_ip_addr=20.20.20.1  netmask=255.255.255.0  check_opposite_ip_version=0  src_mac_addr=0000.3018.82d0  arp_on_linkup=0  ns_on_linkup=0  single_arp_per_gateway=1  single_ns_per_gateway=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${intf_1} =  Get From Dictionary  ${result}  interface_handle
	
#configure MPLS-TP router emulation
	
	${result} =  Emulation Mplstp Config  mode=create  port_handle=@{portHandles}[0]  interface_count=1  interface_handle=${intf_0}  aps_channel_type=0002  bfdcc_channel_type=0007  delay_management_channel_type=0005  high_performance_mode_enable=1  fault_management_channel_type=0003  loss_measurement_channel_type=0004  ondemand_cv_channel_type=0009  pw_status_channel_type=0001  y1731_channel_type=7FFA  dut_mac_addr=ffff.ffff.ffff  router_id=20.20.20.2
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${mpls_intf_0} =  Get From Dictionary  ${result}  interface_handles
	
	${result} =  Emulation Mplstp Config  mode=create  port_handle=@{portHandles}[1]  interface_count=1  interface_handle=${intf_1}  aps_channel_type=0002  bfdcc_channel_type=0007  delay_management_channel_type=0005  high_performance_mode_enable=1  fault_management_channel_type=0003  loss_measurement_channel_type=0004  ondemand_cv_channel_type=0009  pw_status_channel_type=0001  y1731_channel_type=7FFA  dut_mac_addr=ffff.ffff.ffff  router_id=20.20.20.1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${mpls_intf_1} =  Get From Dictionary  ${result}  interface_handles
	
##########################################################.
#  port 1
##########################################################
	
	${result} =  Emulation Mplstp Lsp Pw Config  mode=create  handle=${mpls_intf_0}  alarm_traffic_class=7  alarm_type=ietf  aps_traffic_class=7  aps_type=ietf  cccv_interval=3.33  cccv_traffic_class=7  cccv_type=y1731  description=IXIA.0003.0005.0001.0002  dest_ac_id=2  dest_ac_id_step=1  dest_global_id=1  dest_lsp_number=1  dest_lsp_number_step=1  dest_mep_id=31  dest_mep_id_step=1  dest_node_id=2  dest_tunnel_number=1  dest_tunnel_number_step=1  dm_time_format=ieee  dm_traffic_class=7  dm_type=ietf  ip_address=0.0.0.0  ip_address_mask_len=24  ip_address_step=1  ip_host_per_lsp=0  ip_type=ipv4  lm_counter_type=32b  lm_initial_rx_value=1  lm_initial_tx_value=1  lm_rx_step=1  lm_traffic_class=7  lm_tx_step=1  lm_type=ietf  lsp_incoming_label=2000  lsp_incoming_label_step=1  lsp_outgoing_label=1000  lsp_outgoing_label_step=1  mac_address=0000.0000.0000  mac_per_pw=0  meg_id_integer_step=1  meg_id_prefix=Ixia-Prt-0001  lsp_count=10  pw_per_lsp_count=1  on_demand_cv_traffic_class=7  pw_incoming_label=6000  pw_incoming_label_step=1  pw_incoming_label_step_across_lsp=0  pw_outgoing_label=5000  pw_outgoing_label_step=1  pw_outgoing_label_step_across_lsp=0  pw_status_fault_reply_interval=600  pw_status_traffic_class=7  range_role=protect  repeat_mac=0  src_ac_id=1  src_ac_id_step=1  src_global_id=1  src_lsp_number=1  src_lsp_number_step=1  src_mep_id=21  src_mep_id_step=1  src_node_id=1  src_tunnel_number=1  src_tunnel_number_step=1  support_slow_start=0  protection_switching_type=one_to_one_bidir  range_type=pw
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${peer_lsp_pw_range_00} =  Get From Dictionary  ${result}  range_handle_list
	
	${result} =  Emulation Mplstp Lsp Pw Config  mode=create  handle=${mpls_intf_0}  alarm_traffic_class=7  alarm_type=ietf  aps_traffic_class=7  aps_type=ietf  cccv_interval=3.33  cccv_traffic_class=7  cccv_type=y1731  description=IXIA.0003.0005.0001.0001  dest_ac_id=2  dest_ac_id_step=1  dest_global_id=1  dest_lsp_number=1  dest_lsp_number_step=1  dest_mep_id=31  dest_mep_id_step=1  dest_node_id=2  dest_tunnel_number=1  dest_tunnel_number_step=1  dm_time_format=ieee  dm_traffic_class=7  dm_type=ietf  peer_lsp_pw_range=${peer_lsp_pw_range_00}  ip_address=2.1.1.1  ip_address_mask_len=32  ip_address_step=1  ip_host_per_lsp=100  ip_type=ipv4  lm_counter_type=32b  lm_initial_rx_value=1  lm_initial_tx_value=1  lm_rx_step=1  lm_traffic_class=7  lm_tx_step=1  lm_type=ietf  lsp_incoming_label=2000  lsp_incoming_label_step=1  lsp_outgoing_label=1000  lsp_outgoing_label_step=1  mac_address=0000.0000.0000  mac_per_pw=0  meg_id_integer_step=1  meg_id_prefix=Ixia-Wrk-0001  lsp_count=10  pw_per_lsp_count=1  on_demand_cv_traffic_class=7  pw_incoming_label=6000  pw_incoming_label_step=1  pw_incoming_label_step_across_lsp=0  pw_outgoing_label=5000  pw_outgoing_label_step=1  pw_outgoing_label_step_across_lsp=0  pw_status_fault_reply_interval=600  pw_status_traffic_class=7  range_role=protect  repeat_mac=0  src_ac_id=1  src_ac_id_step=1  src_global_id=1  src_lsp_number=1  src_lsp_number_step=1  src_mep_id=21  src_mep_id_step=1  src_node_id=1  src_tunnel_number=1  src_tunnel_number_step=1  support_slow_start=0  protection_switching_type=one_to_one_bidir  range_type=pw
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${peer_lsp_pw_range_01} =  Get From Dictionary  ${result}  range_handle_list
	
##########################################################.
#  port 2
##########################################################
	
	${result} =  Emulation Mplstp Lsp Pw Config  mode=create  handle=${mpls_intf_1}  alarm_traffic_class=7  alarm_type=ietf  aps_traffic_class=7  aps_type=ietf  cccv_interval=3.33  cccv_traffic_class=7  cccv_type=y1731  description=IXIA.0004.0004.0001.0002  dest_ac_id=2  dest_ac_id_step=1  dest_global_id=1  dest_lsp_number=1  dest_lsp_number_step=1  dest_mep_id=31  dest_mep_id_step=1  dest_node_id=2  dest_tunnel_number=1  dest_tunnel_number_step=1  dm_time_format=ieee  dm_traffic_class=7  dm_type=ietf  ip_address=0.0.0.0  ip_address_mask_len=24  ip_address_step=1  ip_host_per_lsp=0  ip_type=ipv4  lm_counter_type=32b  lm_initial_rx_value=1  lm_initial_tx_value=1  lm_rx_step=1  lm_traffic_class=7  lm_tx_step=1  lm_type=ietf  lsp_incoming_label=2000  lsp_incoming_label_step=1  lsp_outgoing_label=1000  lsp_outgoing_label_step=1  mac_address=0000.0000.0000  mac_per_pw=0  meg_id_integer_step=1  meg_id_prefix=Ixia-Prt-0001  lsp_count=10  pw_per_lsp_count=1  on_demand_cv_traffic_class=7  pw_incoming_label=6000  pw_incoming_label_step=1  pw_incoming_label_step_across_lsp=0  pw_outgoing_label=5000  pw_outgoing_label_step=1  pw_outgoing_label_step_across_lsp=0  pw_status_fault_reply_interval=600  pw_status_traffic_class=7  range_role=protect  repeat_mac=0  src_ac_id=1  src_ac_id_step=1  src_global_id=1  src_lsp_number=1  src_lsp_number_step=1  src_mep_id=21  src_mep_id_step=1  src_node_id=1  src_tunnel_number=1  src_tunnel_number_step=1  support_slow_start=0  protection_switching_type=one_to_one_bidir  range_type=pw
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${peer_lsp_pw_range_10} =  Get From Dictionary  ${result}  range_handle_list
	
	${result} =  Emulation Mplstp Lsp Pw Config  mode=create  handle=${mpls_intf_1}  alarm_traffic_class=7  alarm_type=ietf  aps_traffic_class=7  aps_type=ietf  cccv_interval=3.33  cccv_traffic_class=7  cccv_type=y1731  description=IXIA.0004.0004.0001.0001  dest_ac_id=2  dest_ac_id_step=1  dest_global_id=1  dest_lsp_number=1  dest_lsp_number_step=1  dest_mep_id=31  dest_mep_id_step=1  dest_node_id=2  dest_tunnel_number=1  dest_tunnel_number_step=1  dm_time_format=ieee  dm_traffic_class=7  dm_type=ietf  peer_lsp_pw_range=${peer_lsp_pw_range_10}  ip_address=1.1.1.1  ip_address_mask_len=32  ip_address_step=1  ip_host_per_lsp=100  ip_type=ipv4  lm_counter_type=32b  lm_initial_rx_value=1  lm_initial_tx_value=1  lm_rx_step=1  lm_traffic_class=7  lm_tx_step=1  lm_type=ietf  lsp_incoming_label=2000  lsp_incoming_label_step=1  lsp_outgoing_label=1000  lsp_outgoing_label_step=1  mac_address=0000.0000.0000  mac_per_pw=0  meg_id_integer_step=1  meg_id_prefix=Ixia-Wrk-0001  lsp_count=10  pw_per_lsp_count=1  on_demand_cv_traffic_class=7  pw_incoming_label=6000  pw_incoming_label_step=1  pw_incoming_label_step_across_lsp=0  pw_outgoing_label=5000  pw_outgoing_label_step=1  pw_outgoing_label_step_across_lsp=0  pw_status_fault_reply_interval=600  pw_status_traffic_class=7  range_role=protect  repeat_mac=0  src_ac_id=1  src_ac_id_step=1  src_global_id=1  src_lsp_number=1  src_lsp_number_step=1  src_mep_id=21  src_mep_id_step=1  src_node_id=1  src_tunnel_number=1  src_tunnel_number_step=1  support_slow_start=0  protection_switching_type=one_to_one_bidir  range_type=pw
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${peer_lsp_pw_range_11} =  Get From Dictionary  ${result}  range_handle_list
	
	:FOR	${port}	IN	@{portHandles}
	\	${result} =  Emulation Mplstp Control  port_handle=${port}  mode=start
	\	${status} =  Get From Dictionary  ${result}  status
	\	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	:FOR	${port}	IN	@{portHandles}
	\	${result} =  Emulation Mplstp Info  port_handle=${port}  mode=aggregate_stats
	\	${status} =  Get From Dictionary  ${result}  status
	\	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	\	${stats} =  Set Variable  ${result['${port}']['aggregate']['cccv_up']}
	\	Run Keyword If  '${stats}' != '0'  FAIL  "not all mplstp sessions are down"  ELSE  Log  "Status is SUCCESS"
	
	
	
	
	
	
	
	
	
	
	