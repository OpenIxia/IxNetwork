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
@{portlist} =  	9/1  9/2
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
	
################################################################################
# Configure Topology, Device Group                                             # 
################################################################################
# Creating a topology on first port
	Log  Adding topology 1 on port 1
	${result} =  Topology Config  topology_name="PIMv6 Topology 1"  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log  Creating device group 1 in topology 1
	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name="Device Group 1"  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating a topology on second port
	Log  Adding topology 2 on port 2
	${result} =  Topology Config  topology_name="PIMv6 Topology 2"  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log  Creating device group 2 in topology 2
	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name="Device Group 2"  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	
################################################################################
#  Configure protocol interfaces                                               #
################################################################################
	
# Creating ethernet stack for the first Device Group 
	Log  Creating ethernet stack for the first Device Group
	${result} =  Interface Config  protocol_name="Ethernet 1"  protocol_handle=${deviceGroup_1_handle}  mtu=1500  src_mac_addr=18.03.73.c7.6c.b1  src_mac_addr_step=00.00.00.00.00.00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# Creating ethernet stack for the second Device Group
	Log  Creating ethernet for the second Device Group
	${result} =  Interface Config  protocol_name="Ethernet 2"  protocol_handle=${deviceGroup_2_handle}  mtu=1500  src_mac_addr=18.03.73.c7.6c.01  src_mac_addr_step=00.00.00.00.00.00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_2_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# Creating IPv6 Stack on top of Ethernet Stack for the first Device Group     
	Log  Creating IPv6 Stack on top of Ethernet Stack for the first Device Group
	${result} =  Interface Config  protocol_name="IPv6 1"  protocol_handle=${ethernet_1_handle}  ipv6_multiplier=1  ipv6_resolve_gateway=1  ipv6_manual_gateway_mac=00.00.00.00.00.01  ipv6_manual_gateway_mac_step=00.00.00.00.00.00  ipv6_gateway=2000:0:0:0:0:0:0:1  ipv6_gateway_step=::0  ipv6_intf_addr=2000:0:0:0:0:0:0:2  ipv6_intf_addr_step=::0  ipv6_prefix_length=64
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6_1_handle} =  Get From Dictionary  ${result}  ipv6_handle
	
# Creating IPv6 Stack on top of Ethernet Stack for the second Device Group 
	Log  Creating IPv6 Stack on top of Ethernet Stack for the second Device Group
	${result} =  Interface Config  protocol_name="IPv6 2"  protocol_handle=${ethernet_2_handle}  ipv6_multiplier=1  ipv6_resolve_gateway=1  ipv6_manual_gateway_mac=00.00.00.00.00.01  ipv6_manual_gateway_mac_step=00.00.00.00.00.00  ipv6_gateway=2000:0:0:0:0:0:0:2  ipv6_gateway_step=::0  ipv6_intf_addr=2000:0:0:0:0:0:0:1  ipv6_intf_addr_step=::0  ipv6_prefix_length=64
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6_2_handle} =  Get From Dictionary  ${result}  ipv6_handle
	
################################################################################
# Other protocol configurations                                                # 
################################################################################
	
#This will Create PIMv6 Stack on top of IPv6 Stack of Topology1

# Creating PIMv6 Stack on top of IPv6 1 stack
	Log  Creating PIMv6 Stack on top of IPv6 1 stack
	${result} =  Emulation Pim Config  mode=create  handle=${ipv6_1_handle}  ip_version=6
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6Interface_1_handle} =  Get From Dictionary  ${result}  pim_v6_interface_handle
	
	
#Creating Multicast Group address
	Log  Creating Multicast Group address
	${result} =  Emulation Multicast Group Config  mode=create  ip_addr_start=ff15:0:0:0:0:0:0:1  num_groups=1  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6JoinPruneList_1_handle_group} =  Get From Dictionary  ${result}  multicast_group_handle
	
#Creating Multicast Source address
	Log  Creating Multicast Source address
	${result} =  Emulation Multicast Source Config  mode=create  ip_addr_start=4:0:0:0:0:0:0:1  num_sources=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6JoinPruneList_1_handle_source} =  Get From Dictionary  ${result}  multicast_source_handle

#Creating PIM Join-Prune List
	Log  Creating Join Prune List
	${result} =  Emulation Pim Group Config  mode=create  session_handle=${pimV6Interface_1_handle}  group_pool_handle=${pimV6JoinPruneList_1_handle_group}  source_pool_handle=${pimV6JoinPruneList_1_handle_source}  rp_ip_addr=3000:0:0:0:0:0:0:1  group_pool_mode=send  join_prune_aggregation_factor=1  flap_interval=60  register_stop_trigger_count=10  source_group_mapping=fully_meshed  switch_over_interval=5  group_range_type=startogroup  enable_flap_info=false  prune_source_address=0:0:0:0:0:0:0:0  prune_source_mask_width=32  prune_source_address_count=0  join_prune_group_mask_width=32  join_prune_source_mask_width=32
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6JoinPruneList_1_handle} =  Get From Dictionary  ${result}  pim_v6_join_prune_handle
	
#Creating Multicast Group address
	Log  Creating Multicast Group address
	${result} =  Emulation Multicast Group Config  mode=create  ip_addr_start=ff15:0:0:0:0:0:0:0  num_groups=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6SourcesList_1_handle_group} =  Get From Dictionary  ${result}  multicast_group_handle
	
#Creating Multicast Source address
	Log  Creating Multicast Source address
	${result} =  Emulation Multicast Source Config  mode=create  ip_addr_start=fec0:0:0:0:0:0:0:1  num_sources=1  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6SourcesList_1_handle_source} =  Get From Dictionary  ${result}  multicast_source_handle
	
#Creating PIM Source List
	Log  Creating PIM Source List
	${result} =  Emulation Pim Group Config  mode=create  session_handle=${pimV6Interface_1_handle}  group_pool_handle=${pimV6SourcesList_1_handle_group}  source_pool_handle=${pimV6SourcesList_1_handle_source}  rp_ip_addr=0:0:0:0:0:0:0:0  group_pool_mode=register  register_tx_iteration_gap=30000  register_udp_destination_port=3000  register_udp_source_port=3000  switch_over_interval=0  send_null_register=0  discard_sg_join_states=true  multicast_data_length=64  supression_time=60  register_probe_time=5
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6SourcesList_1_handle} =  Get From Dictionary  ${result}  pim_v6_source_handle
	
#Creating Group Address for Candidate RP 

	Log  Creating Group Address for Candidate RP
	${result} =  Emulation Multicast Group Config  mode=create  ip_addr_start=ff15:0:0:0:0:0:0:1  num_groups=1  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6CandidateRPsList_1_handle} =  Get From Dictionary  ${result}  multicast_group_handle

#Creating PIM Candidate RP List
	Log  Creating PIM Candidate RP List
	${result} =  Emulation Pim Group Config  mode=create  session_handle=${pimV6Interface_1_handle}  group_pool_handle=${pimV6CandidateRPsList_1_handle}  adv_hold_time=150  back_off_interval=3  crp_ip_addr=fec0:0:0:0:0:0:0:1  group_pool_mode=candidate_rp  periodic_adv_interval=60  pri_change_interval=60  pri_type=same  pri_value=180  router_count=1  source_group_mapping=fully_meshed  trigger_crp_msg_count=3  crp_group_mask_len=32
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6CandidateRPsList_1_handle} =  Get From Dictionary  ${result}  pim_v6_candidate_rp_handle

#Creating and Adding IPv6-prefix pool under Network Group1
	Log  Creating ipv6 prefix network addres
	${result} =  Multivalue Config  pattern=counter  counter_start=3000:0:1:1:0:0:0:0  counter_step=0:0:0:1:0:0:0:0  counter_direction=increment  nest_step=0:0:0:0:0:0:0:1 0:0:1:0:0:0:0:0  nest_owner=${deviceGroup_1_handle} ${topology_1_handle}  nest_enabled=0 1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_2_handle} =  Get From Dictionary  ${result}  multivalue_handle

	Log  Creating and Adding IPv6-prefix pool under Network Group
	${result} =  Network Group Config  protocol_handle=${deviceGroup_1_handle}  protocol_name="Network Group 1"  multiplier=1  enable_device=1  connected_to_handle=${ethernet_1_handle}  type=ipv6-prefix  ipv6_prefix_network_address=${multivalue_2_handle}  ipv6_prefix_length=24  ipv6_prefix_number_of_addresses=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_1_handle} =  Get From Dictionary  ${result}  network_group_handle
	${ipv6PrefixPools_1_handle} =  Get From Dictionary  ${result}  ipv6_prefix_pools_handle

# This will Create PIMv6 Stack on top of IPv6 Stack of Topology1
	Log  Creating PIMv6 Stack on top of IPv6 Stack of Topology2
	${result} =  Emulation Pim Config  mode=create  handle=${ipv6_2_handle}  ip_version=6
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6Interface_2_handle} =  Get From Dictionary  ${result}  pim_v6_interface_handle
	
#Creating Multicast Group address
	Log  Creating Multicast Group address
	${result} =  Emulation Multicast Group Config  mode=create  ip_addr_start=ff16:0:0:0:0:0:0:1  num_groups=1  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6JoinPruneList_5_handle_group} =  Get From Dictionary  ${result}  multicast_group_handle
	
#Creating Multicast Source address
	Log  Creating Multicast Source address
	${result} =  Emulation Multicast Source Config  mode=create  ip_addr_start=fec0:0:0:0:0:0:0:1  num_sources=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6JoinPruneList_5_handle_source} =  Get From Dictionary  ${result}  multicast_source_handle

#Creating PIM Join Prune List
	Log  Creating PIM Join Prune List
	${result} =  Emulation Pim Group Config  mode=create  session_handle=${pimV6Interface_2_handle}  group_pool_handle=${pimV6JoinPruneList_5_handle_group}  source_pool_handle=${pimV6JoinPruneList_5_handle_source}  rp_ip_addr=3000:0:0:0:0:0:0:1  group_pool_mode=send  join_prune_aggregation_factor=1  flap_interval=60  register_stop_trigger_count=10  source_group_mapping=fully_meshed  switch_over_interval=5  group_range_type=startogroup  enable_flap_info=false  prune_source_address=0:0:0:0:0:0:0:0  prune_source_mask_width=32  prune_source_address_count=0  join_prune_group_mask_width=32  join_prune_source_mask_width=32
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6JoinPruneList_2_handle} =  Get From Dictionary  ${result}  pim_v6_join_prune_handle
	
#Creating Group address for Join-Prune list 
	Log  Creating Group address for Join-Prune list
	${result} =  Emulation Multicast Group Config  mode=create  ip_addr_start=ff15:0:0:0:0:0:0:0  num_groups=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6SourcesList_5_handle_group} =  Get From Dictionary  ${result}  multicast_group_handle
	
#Creating Source address for Join-Prune list 
	Log  Creating Source address for Join-Prune list
	${result} =  Emulation Multicast Source Config  mode=create  ip_addr_start=fec0:0:0:0:0:0:0:1  num_sources=1  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6SourcesList_5_handle_source} =  Get From Dictionary  ${result}  multicast_source_handle
	
#Creating PIM Source List
	Log  Creating PIM Source List
	${result} =  Emulation Pim Group Config  mode=create  session_handle=${pimV6Interface_2_handle}  group_pool_handle=${pimV6SourcesList_5_handle_group}  source_pool_handle=${pimV6SourcesList_5_handle_source}  rp_ip_addr=0:0:0:0:0:0:0:0  group_pool_mode=register  register_tx_iteration_gap=30000  register_udp_destination_port=3000  register_udp_source_port=3000  switch_over_interval=0  send_null_register=0  discard_sg_join_states=true  multicast_data_length=64  supression_time=60  register_probe_time=5
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6SourcesList_5_handle} =  Get From Dictionary  ${result}  pim_v6_source_handle
	
#Creating Group Address for Candidate RP 

	Log  Creating Group Address for Candidate RP
	${result} =  Emulation Multicast Group Config  mode=create  ip_addr_start=ff15:0:0:0:0:0:0:0  num_groups=1  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6CandidateRPsList_3_handle} =  Get From Dictionary  ${result}  multicast_group_handle

#Creating PIM Candidate RP List
	Log  Creating PIM Candidate RP List
	${result} =  Emulation Pim Group Config  mode=create  session_handle=${pimV6Interface_2_handle}  group_pool_handle=${pimV6CandidateRPsList_3_handle}  adv_hold_time=150  back_off_interval=3  crp_ip_addr=fec0:0:0:0:0:0:0:1  group_pool_mode=candidate_rp  periodic_adv_interval=60  pri_change_interval=60  pri_type=same  pri_value=180  router_count=1  source_group_mapping=fully_meshed  trigger_crp_msg_count=3  crp_group_mask_len=32
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${pimV6CandidateRPsList_3_handle} =  Get From Dictionary  ${result}  pim_v6_candidate_rp_handle

# Creating and Adding IPv6-prefix pool under Network Group2
	Log  Creating ipv6 prefix network address
	${result} =  Multivalue Config  pattern=counter  counter_start=3000:1:1:1:0:0:0:0  counter_step=0:0:0:1:0:0:0:0  counter_direction=increment  nest_step=0:0:0:0:0:0:0:1 0:0:1:0:0:0:0:0  nest_owner=${deviceGroup_2_handle} ${topology_2_handle}  nest_enabled=0 1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_4_handle} =  Get From Dictionary  ${result}  multivalue_handle

	Log  Creating and Adding IPv6-prefix pool under Network Group2
	${result} =  Network Group Config  protocol_handle=${deviceGroup_2_handle}  protocol_name="Network Group 2"  multiplier=1  enable_device=1  connected_to_handle=${ethernet_2_handle}  type=ipv6-prefix  ipv6_prefix_network_address=${multivalue_4_handle}  ipv6_prefix_length=24  ipv6_prefix_number_of_addresses=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_2_handle} =  Get From Dictionary  ${result}  network_group_handle
	${ipv6PrefixPools_2_handle} =  Get From Dictionary  ${result}  ipv6_prefix_pools_handle
	
	Log  Waiting 5 seconds before starting protocol(s) ...
	Sleep  5s
############################################################################
# Start protocols                                                       #
############################################################################
	Log  Starting PIM protocol ...
	${result} =  Emulation Pim Control  mode=start  handle=${pimV6Interface_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Starting PIM protocol ...
	${result} =  Emulation Pim Control  mode=start  handle=${pimV6Interface_2_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Starting all protocol(s) ...
	${result} =  Test Control  action=start_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Waiting for 60 seconds
	Sleep  60s
	
############################################################################
# Retrieve protocol statistics                                             #
############################################################################
	
	Log  Fetching pimv4 aggregated statistics
	${result} =  Emulation Pim Info  handle=${pimV6Interface_2_handle}  mode=aggregate
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
	
############################################################################
# Retrieve Learned Info                                                    #
############################################################################
	
	Log  Fetching pim learned info
	${result} =  Emulation Pim Info  handle=${pimV6Interface_1_handle}  mode=learned_crp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	

############################################################################
# Modifying the GroupRange Type from *G to SG and Enabling Bootstrap       #
############################################################################
	
#Modifying the GroupRange Type from *G to SG for Topology1
	Log  "Modifying the GroupRange Type from *G to SG for Topology1"
	${result} =  Emulation Pim Group Config  handle=${pimV6JoinPruneList_1_handle}  mode=modify  group_range_type=sourcetogroup
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#Modifying the GroupRange Type from *G to SG for Topology2
	Log  Modifying the GroupRange Type from *G to SG for Topology2
	${result} =  Emulation Pim Group Config  handle=${pimV6JoinPruneList_2_handle}  mode=modify  group_range_type=sourcetogroup
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#Enabling Bootstrap for Topology1   
	Log  Enabling Bootstrap for Topology1
	${result} =  Emulation Pim Config  handle=${pimV6Interface_1_handle}  mode=modify  ip_version=6  bootstrap_enable=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#Enabling Bootstrap and Modifying Priority for Topology2
	Log  Enabling Bootstrap and Modifying Priority for Topology2
	${result} =  Emulation Pim Config  handle=${pimV6Interface_2_handle}  mode=modify  ip_version=6  bootstrap_enable=1  bootstrap_priority=74
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#Applying changes on the fly
	Log  Applying changes on the fly
	${result} =  Test Control  handle=${pimV6Interface_1_handle}  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
	
	Log  Applying changes on the fly
	${result} =  Test Control  handle=${pimV6Interface_2_handle}  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
	
	Log  Waiting for 60 seconds
	Sleep  60s
	
############################################################################
# Retrieve protocol learned info again after RangeType modification        #
############################################################################
	
	Log  Fetching pim learned info
	${result} =  Emulation Pim Info  handle=${pimV6Interface_1_handle}  mode=learned_crp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
############################################################################ 
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv6, Destination->Multicast group                #
# 2. Type      : Multicast IPv6 traffic                                    #
# 3. Flow Group: On IPv6 Destination Address                               #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : IPv6 Destination Address                                  #
############################################################################
	
	Log  Configuring L2-L3 traffic
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${ipv6PrefixPools_1_handle}  emulation_dst_handle=${ipv6PrefixPools_2_handle}  name=Traffic_Item_1  circuit_endpoint_type=ipv6  transmit_distribution=ipv6DestIp0  rate_pps=1000  frame_size=512  track_by=trackingenabled0 ipv6DestIp0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
############################################################################
#  Start L2-L3 traffic configured earlier                                  #
############################################################################
	
	Log  Running Traffic...
	${result} =  Traffic Control  action=run  traffic_generator=ixnetwork_540  type=l23
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Let the traffic run for 20 seconds ...
	Sleep  20s

############################################################################
# Retrieve L2-L3 traffic stats                                             #
############################################################################
	
	Log  Retrieving L2-L3 traffic stats
	${result} =  Traffic Stats  mode=all  traffic_generator=ixnetwork_540  measure_mode=mixed
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
############################################################################
# Stop L2-L3 traffic started earlier                                       #
############################################################################
	
	Log  Stopping Traffic...
	${result} =  Traffic Control  action=stop  traffic_generator=ixnetwork_540  type=l23
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
	
############################################################################
# Stop all protocols                                                       #
############################################################################
	
	Log  Stopping all protocol(s) ...
	${result} =  Test Control  action=stop_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  Sleep !!! Test Script Ends !!!
	