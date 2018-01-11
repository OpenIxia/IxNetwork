*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.07_OSPFv2_routers_routes_modify_disable_enable_new.tcl
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
# START - PIM Router Configuration
################################################################################

	Log To Console  Start PIM configuration ...

	${result} =  Emulation Pim Config  mode=create  reset=1  port_handle=@{portHandles}[0]  count=1  pim_mode=sm  type=remote_rp  ip_version=4  intf_ip_addr=112.0.0.101  intf_ip_addr_step=0.0.0.1  intf_ip_prefix_len=24  gateway_intf_ip_addr=112.0.0.1  gateway_intf_ip_addr_step=0.0.0.1  vlan=0  vlan_id=12  vlan_id_mode=increment  vlan_id_step=1  vlan_user_priority=0  vlan_cfi=0  mac_address_init=00aa.00bb.0001  mac_address_step=0000.0000.0001  bidir_capable=0  dr_priority=0  generation_id_mode=constant  hello_interval=30  hello_holdtime=105  join_prune_interval=60  join_prune_holdtime=180  neighbor_intf_ip_addr=112.0.0.1  override_interval=2500  prune_delay_enable=1  prune_delay=500  prune_delay_tbit=0  router_id=112.0.0.101  router_id_step=0.0.0.1  send_generation_id=1  mvpn_enable=0  mvpn_pe_count=1  mvpn_pe_ip=12.0.0.101  mvpn_pe_ip_incr=0.0.0.1  mvrf_count=1  mvrf_unique=0  default_mdt_ip=232.0.0.101  default_mdt_ip_incr=0.0.0.1  gre_checksum_enable=0  gre_key_enable=0  gre_key_in=0  gre_key_out=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	@{pim_cfg_router_handles}=    Create List
	${pim_router_handles} =  Get From Dictionary  ${result}  handle
	Append To List  ${pim_cfg_router_handles}  ${pim_router_handles}
################################################################################
# END - PIM Router Configuration
################################################################################

################################################################################
# START - Multicast Group Configuration - 1
################################################################################
	Log To Console  Start Multicast group configuration ...
	${result} =  Emulation Multicast Group Config  mode=create  num_groups=3  ip_addr_start=238.0.0.101  ip_addr_step=0.0.0.1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	@{mcast_cfg_group_handles}=    Create List
	${mcast_group_handles} =  Get From Dictionary  ${result}  handle
	Append To List  ${mcast_cfg_group_handles}  ${mcast_group_handles}
################################################################################
# END - Multicast Group Configuration - 1
################################################################################
	
	Log To Console  Start Multicast group configuration ...
	${result} =  Emulation Multicast Group Config  mode=create  num_groups=3  ip_addr_start=238.0.0.101  ip_addr_step=0.0.0.1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${mcast_group_handle} =  Get From Dictionary  ${result}  handle
	Log To Console  End Multicast Group configuration ...
	${mcast_group_handles} =  Get From Dictionary  ${result}  handle
	Append To List  ${mcast_cfg_group_handles}  ${mcast_group_handles}
################################################################################
# START - Multicast Source Configuration - 1
################################################################################
	Log To Console  Start Multicast source configuration ...
	${result} =  Emulation Multicast Source Config  mode=create  num_sources=5  ip_addr_start=111.0.0.101  ip_addr_step=0.0.0.1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	@{mcast_cfg_source_handles}=    Create List
	${mcast_source_handles} =  Get From Dictionary  ${result}  handle
	Append To List  ${mcast_cfg_source_handles}  ${mcast_source_handles}
################################################################################
# END - Multicast Source Configuration - 1
################################################################################
	
################################################################################
# START - Multicast Source Configuration - 2
################################################################################
	
	${result} =  Emulation Multicast Source Config  mode=create  num_sources=5  ip_addr_start=111.0.0.101  ip_addr_step=0.0.0.1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${mcast_source_handles} =  Get From Dictionary  ${result}  handle
	Append To List  ${mcast_cfg_source_handles}  ${mcast_source_handles}
################################################################################
# END - Multicast Source Configuration - 2
################################################################################
	
################################################################################
# START - PIM Join/Prune Configuration
################################################################################
	
	${result} =  Emulation Pim Group Config  mode=create  session_handle=@{pim_cfg_router_handles}[0]  group_pool_handle=@{mcast_cfg_group_handles}[0]  source_pool_handle=@{mcast_cfg_source_handles}[0]  group_pool_mode=send  interval=50  join_prune_aggregation_factor=10  join_prune_per_interval=10  rate_control=0  register_per_interval=10  register_stop_per_interval=10  register_tx_iteration_gap=100  register_stop_trigger_count=1  register_udp_destination_port=10  register_udp_source_port=10  register_triggered_sg=0  rp_ip_addr=21.21.25.1  rp_ip_addr_step=0.0.1.0  send_null_register=0  source_group_mapping=one_to_one  spt_switchover=0  switch_over_interval=1  s_g_rpt_group=0  wildcard_group=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	@{pim_cfg_group_handles}=    Create List
	${pim_group_handles} =  Get From Dictionary  ${result}  handle
	Append To List  ${pim_cfg_group_handles}  ${pim_group_handles}
	
########################################
# End emulation_pim_group_config       #
########################################
	
################################################################################
# START - PIM Source Configuration
################################################################################
	
	${result} =  Emulation Pim Group Config  mode=create  session_handle=@{pim_cfg_router_handles}[0]  group_pool_handle=@{mcast_cfg_group_handles}[1]  source_pool_handle=@{mcast_cfg_source_handles}[1]  interval=50  join_prune_aggregation_factor=10  rate_control=0  register_per_interval=10  register_stop_per_interval=10  register_tx_iteration_gap=100  register_stop_trigger_count=1  register_udp_destination_port=10  register_udp_source_port=10  register_triggered_sg=0  rp_ip_addr=21.21.25.1  rp_ip_addr_step=0.0.1.0  send_null_register=0  source_group_mapping=one_to_one  spt_switchover=0  switch_over_interval=1  s_g_rpt_group=0  wildcard_group=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	@{pim_cfg_source_handles}=    Create List
	${pim_group_handles} =  Get From Dictionary  ${result}  handle
	Append To List  ${pim_cfg_source_handles}  ${pim_group_handles}
################################################################################
# START - PIM Join/Prune Modification
################################################################################
	
	${result} =  Emulation Pim Group Config  mode=modify  handle=@{pim_cfg_group_handles}[0]  flap_interval=10  rp_ip_addr=114.0.0.101  source_group_mapping=fully_meshed  spt_switchover=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pim_group_handles} =  Get From Dictionary  ${result}  handle
	Append To List  ${pim_cfg_group_handles}  ${pim_group_handles}
	
########################################
# Start emulation_pim_group_config     #
########################################
	
	${result} =  Emulation Pim Group Config  mode=modify  handle=@{pim_cfg_source_handles}  register_udp_destination_port=3001  register_udp_source_port=3001  spt_switchover=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pim_group_handles} =  Get From Dictionary  ${result}  handle
	Append To List  ${pim_cfg_source_handles}  ${pim_group_handles}
	
########################################
# Start PIM                            #
########################################
	
	${result} =  Emulation Pim Control  port_handle=@{portHandles}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  20s
########################################
# Check PIM routers configured         #
########################################
	
	${result} =  Emulation Pim Info  handle=@{pim_cfg_router_handles}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${stats} =  Set Variable  ${result['@{portHandles}[0]']['aggregate']['num_routers_configured']}
	















