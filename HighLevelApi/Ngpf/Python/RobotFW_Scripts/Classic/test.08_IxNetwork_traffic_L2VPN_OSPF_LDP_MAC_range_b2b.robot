*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.151/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.151/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/009660_Qualify_HLTAPI_on_VM/test.08_IxNetwork_traffic_L2VPN_OSPF_LDP_MAC_range_b2b.tcl
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
# OSPF configuration
################################################################################
	
	${result} =  Emulation Ospf Config  port_handle=@{portHandles}[0]  reset=1  session_type=ospfv2  mode=create  count=1  intf_ip_addr=20.20.20.1  intf_prefix_length=24  neighbor_intf_ip_addr=20.20.20.2  loopback_ip_addr=1.1.1.1  router_id=20.20.20.1  area_id=0.0.0.0  area_id_step=0.0.0.0  area_type=external-capable  authentication_mode=null  network_type=ptop  lsa_discard_mode=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${p_ospf_router_1} =  Get From Dictionary  ${result}  handle
	
	${result} =  Emulation Ospf Config  port_handle=@{portHandles}[1]  reset=1  session_type=ospfv2  mode=create  count=1  intf_ip_addr=20.20.20.2  intf_prefix_length=24  neighbor_intf_ip_addr=20.20.20.1  loopback_ip_addr=2.2.2.2  router_id=20.20.20.2  area_id=0.0.0.0  area_id_step=0.0.0.0  area_type=external-capable  authentication_mode=null  network_type=ptop  lsa_discard_mode=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${p_ospf_router_1} =  Get From Dictionary  ${result}  handle
	
################################################################################
# LDP configuration
################################################################################
	
	${result} =  Emulation Ldp Config  reset=1  mode=create  port_handle=@{portHandles}[0]  count=1  intf_ip_addr=20.20.20.1  intf_prefix_length=24  gateway_ip_addr=20.20.20.2  lsr_id=20.20.20.1  label_space=0  label_adv=unsolicited  peer_discovery=link  hello_interval=5  hello_hold_time=15  keepalive_interval=10  keepalive_holdtime=30  discard_self_adv_fecs=0  enable_l2vpn_vc_fecs=1  enable_explicit_include_ip_fec=0  enable_remote_connect=1  enable_vc_group_matching=0  targeted_hello_hold_time=45  targeted_hello_interval=15
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${p_ldp_router_1} =  Get From Dictionary  ${result}  handle
	
	${result} =  Emulation Ldp Config  reset=1  mode=create  port_handle=@{portHandles}[1]  count=1  intf_ip_addr=20.20.20.2  intf_prefix_length=24  gateway_ip_addr=20.20.20.1  lsr_id=20.20.20.2  label_space=0  label_adv=unsolicited  peer_discovery=link  hello_interval=5  hello_hold_time=15  keepalive_interval=10  keepalive_holdtime=30  discard_self_adv_fecs=0  enable_l2vpn_vc_fecs=1  enable_explicit_include_ip_fec=0  enable_remote_connect=1  enable_vc_group_matching=0  targeted_hello_hold_time=45  targeted_hello_interval=15
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${p_ldp_router_2} =  Get From Dictionary  ${result}  handle
	
    # Provider advertised FECs
	
	${result} =  Emulation Ldp Route Config  mode=create  handle=${p_ldp_router_1}  fec_type=ipv4_prefix  label_msg_type=mapping  egress_label_mode=nextlabel  num_lsps=1  fec_ip_prefix_start=1.1.1.1  fec_ip_prefix_length=32  packing_enable=0  label_value_start=111  provisioning_model=manual_configuration
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Ldp Route Config  mode=create  handle=${p_ldp_router_2}  fec_type=ipv4_prefix  label_msg_type=mapping  egress_label_mode=nextlabel  num_lsps=1  fec_ip_prefix_start=2.2.2.2  fec_ip_prefix_length=32  packing_enable=0  label_value_start=222  provisioning_model=manual_configuration
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
    # PE
	
	${result} =  Emulation Ldp Config  mode=create  port_handle=@{portHandles}[0]  count=1  intf_ip_addr=20.20.20.1  intf_prefix_length=24  gateway_ip_addr=20.20.20.2  loopback_ip_addr=1.1.1.1  lsr_id=1.1.1.1  remote_ip_addr=2.2.2.2  label_space=0  peer_discovery=targeted_martini  hello_interval=5  hello_hold_time=15  keepalive_interval=10  keepalive_holdtime=30  discard_self_adv_fecs=0  enable_l2vpn_vc_fecs=1  enable_explicit_include_ip_fec=0  enable_remote_connect=1  enable_vc_group_matching=0  targeted_hello_hold_time=45  targeted_hello_interval=15
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pe_ldp_router_1} =  Get From Dictionary  ${result}  handle
	
	
	
	${result} =  Emulation Ldp Config  mode=create  port_handle=@{portHandles}[1]  count=1  intf_ip_addr=20.20.20.2  intf_prefix_length=24  gateway_ip_addr=20.20.20.1  loopback_ip_addr=2.2.2.2  lsr_id=2.2.2.2  remote_ip_addr=1.1.1.1  label_space=0  peer_discovery=targeted_martini  hello_interval=5  hello_hold_time=15  keepalive_interval=10  keepalive_holdtime=30  discard_self_adv_fecs=0  enable_l2vpn_vc_fecs=1  enable_explicit_include_ip_fec=0  enable_remote_connect=1  enable_vc_group_matching=0  targeted_hello_hold_time=45  targeted_hello_interval=15
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pe_ldp_router_2} =  Get From Dictionary  ${result}  handle
	
    # PE L2 VC
	
	${result} =  Emulation Ldp Route Config  mode=create  handle=${pe_ldp_router_1}  fec_type=vc  fec_vc_type=eth  fec_vc_count=3  fec_vc_group_id=1  fec_vc_group_count=1  fec_vc_cbit=0  fec_vc_id_start=311  fec_vc_id_step=1  fec_vc_id_count=1  fec_vc_intf_mtu_enable=1  fec_vc_intf_mtu=1500  fec_vc_intf_desc=ixia_ldp_vc  packing_enable=0  fec_vc_label_mode=increment_label  fec_vc_label_value_start=211  fec_vc_label_value_step=1  fec_vc_peer_address=2.2.2.2  fec_vc_ce_ip_addr=1.1.1.1  fec_vc_mac_range_enable=1  fec_vc_mac_range_count=5  fec_vc_mac_range_repeat_mac=0  fec_vc_mac_range_same_vlan=0  fec_vc_mac_range_vlan_enable=0  fec_vc_mac_range_start=0000.1111.0000  provisioning_model=manual_configuration
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${lsp_vc_range_handles_1} =  Get From Dictionary  ${result}  lsp_vc_range_handles
	
	${result} =  Emulation Ldp Route Config  mode=create  handle=${pe_ldp_router_2}  fec_type=vc  fec_vc_type=eth  fec_vc_count=3  fec_vc_group_id=1  fec_vc_group_count=1  fec_vc_cbit=0  fec_vc_id_start=311  fec_vc_id_step=1  fec_vc_id_count=1  fec_vc_intf_mtu_enable=1  fec_vc_intf_mtu=1500  fec_vc_intf_desc=ixia_ldp_vc  packing_enable=0  fec_vc_label_mode=increment_label  fec_vc_label_value_start=311  fec_vc_label_value_step=1  fec_vc_peer_address=1.1.1.1  fec_vc_ce_ip_addr=2.2.2.2  fec_vc_mac_range_enable=1  fec_vc_mac_range_count=5  fec_vc_mac_range_repeat_mac=0  fec_vc_mac_range_same_vlan=0  fec_vc_mac_range_vlan_enable=0  fec_vc_mac_range_start=0000.2222.0000  provisioning_model=manual_configuration
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${lsp_vc_range_handles_2} =  Get From Dictionary  ${result}  lsp_vc_range_handles
	
################################################################################
# Start protocols
################################################################################
	
	${result} =  Emulation Ospf Control  port_handle=@{portHandles}[0] @{portHandles}[1]  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Ldp Control  port_handle=@{portHandles}[0] @{portHandles}[1]  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Wait 60 seconds for the OSPF and LDP to learn routes and labels
	Sleep  60s
	
################################################################################
# Configure traffic
################################################################################
	
	${result} =  Traffic Control  action=reset  traffic_generator=ixnetwork
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  transmit_mode=continuous  name=VC_Range_Traffic  src_dest_mesh=one_to_one  route_mesh=one_to_one  circuit_type=l2vpn  circuit_endpoint_type=ethernet_vlan  emulation_src_handle=${lsp_vc_range_handles_1}  emulation_dst_handle=${lsp_vc_range_handles_2}  track_by=mpls_label  stream_packing=one_stream_per_endpoint_pair  rate_percent=2  length_mode=fixed  frame_size=512
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Start traffic
################################################################################
	
	${result} =  Traffic Control  action=run  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  20s
################################################################################
# Stop traffic
################################################################################
	
	${result} =  Traffic Control  action=stop  port_handle=@{portHandles}[0]  traffic_generator=ixnetwork
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Retrieve stats 
################################################################################
	
	${result} =  Traffic Stats  port_handle=@{portHandles}[0] @{portHandles}[1]  traffic_generator=ixnetwork  mode=aggregate
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	Log  Packets Tx: ${result['aggregate']['tx']['pkt_count']}
	Log  Packets Rx: ${result['aggregate']['rx']['pkt_count']}
	
	
	
	
	

