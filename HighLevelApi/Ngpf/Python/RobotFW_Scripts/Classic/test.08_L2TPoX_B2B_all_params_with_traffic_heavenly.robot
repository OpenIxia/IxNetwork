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

	
#####################
# Start L2TPoX Call #
#####################

	${result} =  L2tp Config  mode=lns  num_tunnels=3  port_handle=@{portHandles}[1]  attempt_rate=200  disconnect_rate=200  enable_term_req_timeout=1  max_outstanding=200  max_terminate_req=10  terminate_req_timeout=5  l2_encap=ethernet_ii  l2tp_dst_addr=12.70.0.2  l2tp_dst_step=0.0.0.1  src_mac_addr=00.de.ad.be.ef.00  vci=32  vci_count=1  vci_step=1  vlan_count=4094  vlan_id=1  vlan_id_step=1  vlan_user_priority=0  vlan_user_priority_count=1  vlan_user_priority_step=1  vpi=0  vpi_count=1  vpi_step=1  bearer_capability=digital  bearer_type=digital  ctrl_retries=5  framing_capability=sync  hello_interval=60  init_ctrl_timeout=2  max_ctrl_timeout=8  redial_max=20  redial_timeout=10  rws=10  sess_distribution=next  sessions_per_tunnel=1  offset_byte=0  offset_len=0  udp_dst_port=1701  udp_src_port=1701  avp_rx_connect_speed=128  hostname=lac  secret=secret  tun_distribution=next_tunnelfill_tunnel  wildcard_bang_end=0  wildcard_bang_start=0  wildcard_dollar_end=0  wildcard_dollar_start=0  config_req_timeout=5  echo_req_interval=60  max_configure_req=10  ip_cp=ipv4_cp  ipcp_req_timeout=5  max_ipcp_req=10  ppp_client_ip=1.1.1.2  ppp_client_step=0.0.0.1  ppp_server_ip=1.1.1.1  ppp_server_step=::A0A:4  ipv6_pool_addr_prefix_len=64  ipv6_pool_prefix=::  ipv6_pool_prefix_len=48  auth_mode=none  auth_req_timeout=5  max_auth_req=10  password=${EMPTY}  username=${EMPTY}  wildcard_pound_end=0  wildcard_pound_start=0  wildcard_question_end=0  wildcard_question_start=0  addr_count_per_vci=1  addr_count_per_vpi=1  l2tp_src_addr=12.70.0.1  l2tp_src_count=1  l2tp_src_gw=0.0.0.0  l2tp_src_prefix_len=24  l2tp_src_step=0.0.0.1  no_call_timeout=5  session_id_start=1  tunnel_id_start=1  hello_req=0  redial=0  ctrl_chksum=0  data_chksum=0  length_bit=0  offset_bit=0  sequence_bit=0  avp_hide=0  hostname_wc=0  secret_wc=0  tun_auth=0  echo_req=0  echo_rsp=0  password_wc=0  username_wc=0  enable_magic=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${network_l2tp_handle} =  Get From Dictionary  ${result}  handle
	
################################################################################
#                                                                              #
# Description:                                                                 #
#    Call to ::ixia::l2tp_config using all parameters.                         #
#    Use this call as a starting point for specific L2TPoX configurations.     #
#                                                                              #
################################################################################
	
	${result} =  L2tp Config  mode=lac  num_tunnels=3  port_handle=@{portHandles}[0]  attempt_rate=200  disconnect_rate=200  enable_term_req_timeout=1  max_outstanding=200  max_terminate_req=10  terminate_req_timeout=5  l2_encap=ethernet_ii  l2tp_dst_addr=12.70.0.1  l2tp_dst_step=0.0.0.0  src_mac_addr=00.de.ad.be.ef.00  vci=32  vci_count=1  vci_step=1  vlan_count=4094  vlan_id=1  vlan_id_step=1  vlan_user_priority=0  vlan_user_priority_count=1  vlan_user_priority_step=1  vpi=0  vpi_count=1  vpi_step=1  bearer_capability=digital  bearer_type=digital  ctrl_retries=5  framing_capability=sync  hello_interval=60  init_ctrl_timeout=2  max_ctrl_timeout=8  redial_max=20  redial_timeout=10  rws=10  sess_distribution=next  sessions_per_tunnel=1  offset_byte=0  offset_len=0  udp_dst_port=1701  udp_src_port=1701  avp_rx_connect_speed=128  hostname=lac  secret=secret  tun_distribution=next_tunnelfill_tunnel  wildcard_bang_end=0  wildcard_bang_start=0  wildcard_dollar_end=0  wildcard_dollar_start=0  config_req_timeout=5  echo_req_interval=60  max_configure_req=10  ip_cp=ipv4_cp  ipcp_req_timeout=5  max_ipcp_req=10  ppp_client_ip=1.1.1.2  ppp_client_step=0.0.0.1  ppp_server_ip=1.1.1.1  ppp_server_step=::A0A:4  ipv6_pool_addr_prefix_len=64  ipv6_pool_prefix=::  ipv6_pool_prefix_len=48  auth_mode=none  auth_req_timeout=5  max_auth_req=10  password=${EMPTY}  username=${EMPTY}  wildcard_pound_end=0  wildcard_pound_start=0  wildcard_question_end=0  wildcard_question_start=0  addr_count_per_vci=1  addr_count_per_vpi=1  l2tp_src_addr=12.70.0.2  l2tp_src_count=3  l2tp_src_gw=0.0.0.0  l2tp_src_prefix_len=24  l2tp_src_step=0.0.0.1  no_call_timeout=5  session_id_start=1  tunnel_id_start=1  hello_req=0  redial=0  ctrl_chksum=0  data_chksum=0  length_bit=0  offset_bit=0  sequence_bit=0  avp_hide=0  hostname_wc=0  secret_wc=0  tun_auth=0  echo_req=0  echo_rsp=0  password_wc=0  username_wc=0  enable_magic=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${access_l2tp_handle} =  Get From Dictionary  ${result}  handle
	
####################
# End L2TPoX Call  #
####################
################################################################################
# END - L2TP Configuration
################################################################################
	
################################################################################
# Connect sessions                                                             #
################################################################################
	
	${result} =  L2tp Control  handle=${network_l2tp_handle} ${access_l2tp_handle}  action=connect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  20s
################################################################################
# Get L2TP aggregate statistics                                                #
################################################################################
	
	${result} =  L2tp Stats  port_handle=@{portHandles}[0] @{portHandles}[1]  mode=aggregate
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
	${tunnels_up_port1} =  Set Variable  ${result['@{portHandles}[0]']['aggregate']['tunnels_up']}
	Run Keyword If  '${tunnels_up_port1}' != '3'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${sessions_up_port1} =  Set Variable  ${result['@{portHandles}[0]']['aggregate']['sessions_up']}
	Run Keyword If  '${sessions_up_port1}' != '3'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${tunnels_up_port2} =  Set Variable  ${result['@{portHandles}[1]']['aggregate']['tunnels_up']}
	Run Keyword If  '${tunnels_up_port2}' != '3'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${sessions_up_port2} =  Set Variable  ${result['@{portHandles}[1]']['aggregate']['sessions_up']}
	Run Keyword If  '${sessions_up_port2}' != '3'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Delete all the streams first
################################################################################
	
	${result} =  Traffic Control  action=reset  traffic_generator=ixnetwork
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
#                                                                              #
# Description:                                                                 #
#    Call to ::ixia::traffic_config using all parameters.                      #
#    Use this call as a starting point for specific traffic configurations.    #
#                                                                              #
################################################################################

########################
# TRAFFIC CONFIG START #
########################

	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork  bidirectional=1  port_handle=@{portHandles}  emulation_dst_handle=${access_l2tp_handle}  emulation_src_handle=${network_l2tp_handle}  allow_self_destined=0  hosts_per_net=1  stream_packing=optimal_packing  fr_range_count=1  transmit_mode=continuous  pkts_per_burst=100  rate_bps=100000  rate_percent=10  rate_pps=100000  inter_burst_gap=64  inter_frame_gap=64  inter_stream_gap=64  enforce_min_gap=12  tx_delay=0  track_by=endpoint_pair  burst_loop_count=1  loop_count=1  fcs=0  fcs_type=no_CRC  frame_size=256  length_mode=fixed
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
#######################
# TRAFFIC CONFIG STOP #
#######################
	
################################################################################
# Start the traffic                                                            #
################################################################################
	
	${result} =  Traffic Control  action=run  traffic_generator=ixnetwork
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  25s
	
	
################################################################################
# Stop the traffic                                                             #
################################################################################
	
	
	${result} =  Traffic Control  action=stop  traffic_generator=ixnetwork
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  20s
	
################################################################################
# Gather and display traffic statistics                                        #
################################################################################
	
	${result} =  Traffic Stats  mode=aggregate  traffic_generator=ixnetwork
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${pkt_tx_p0} =  Set Variable  ${result['@{portHandles}[0]']['aggregate']['tx']['pkt_count']}
	${pkt_rx_p0} =  Set Variable  ${result['@{portHandles}[0]']['aggregate']['rx']['pkt_count']}
	${pkt_tx_p1} =  Set Variable  ${result['@{portHandles}[1]']['aggregate']['tx']['pkt_count']}
	${pkt_rx_p1} =  Set Variable  ${result['@{portHandles}[1]']['aggregate']['rx']['pkt_count']}
	
	${condition1} =  Evaluate  ${pkt_tx_p0} - ${pkt_rx_p1}
	${condition2} =  Evaluate  int(${pkt_tx_p0}) / 10
	Run Keyword If  '${condition1}' > '${condition2}'  FAIL  "Frame loss detected on port @{portHandles}[1]"  ELSE  Log  "Status is SUCCESS"
	
	${condition1} =  Evaluate  ${pkt_tx_p1} - ${pkt_rx_p0}
	${condition2} =  Evaluate  int(${pkt_tx_p1}) / 10
	Run Keyword If  '${condition1}' > '${condition2}'  FAIL  "Frame loss detected on port @{portHandles}[0]"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Disconnect sessions                                                             #
################################################################################
	
	${result} =  L2tp Control  handle=${network_l2tp_handle} ${access_l2tp_handle}  action=disconnect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	
	
	
	