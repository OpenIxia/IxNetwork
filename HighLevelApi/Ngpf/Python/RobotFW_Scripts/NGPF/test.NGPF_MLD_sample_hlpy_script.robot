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
	${result} =  Topology Config  topology_name="MLD Host Topology"  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log  Creating device group 1 in topology 1
	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name="MLD Host Device Group"  device_group_multiplier=2  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating a topology on second port
	Log  Adding topology 2 on port 2
	${result} =  Topology Config  topology_name="MLD Querier Topology"  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log  Creating device group 2 in topology 2
	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name="MLD Querier Device Group"  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	
################################################################################
#  Configure protocol interfaces                                               #
################################################################################
	
# Creating multivalue for ethernet
	Log  Creating multivalue pattern for ethernet
	${result} =  Multivalue Config  pattern=counter  counter_start=18.03.73.c7.6c.b1  counter_step=00.00.00.00.00.01  counter_direction=increment  nest_step=00.00.01.00.00.00  nest_owner=${topology_1_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_1_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating ethernet stack for the first Device Group 
	Log  Creating ethernet stack for the first Device Group
	${result} =  Interface Config  protocol_name="Ethernet 1"  protocol_handle=${deviceGroup_1_handle}  mtu=1500  src_mac_addr=${multivalue_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# Creating ethernet stack for the second Device Group
	Log  Creating ethernet for the second Device Group
	${result} =  Interface Config  protocol_name="Ethernet 2"  protocol_handle=${deviceGroup_2_handle}  mtu=1500  src_mac_addr=18.03.73.c7.6c.01  src_mac_addr_step=00.00.00.00.00.00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_2_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# Creating multivalue for IPv6                                 
	Log  Creating multivalue pattern for IPv6
	${result} =  Multivalue Config  pattern=counter  counter_start=2001:0:0:1:0:0:0:2  counter_step=0:0:0:0:0:0:0:1  counter_direction=increment  nest_step=0:0:0:1:0:0:0:0  nest_owner=${topology_1_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_2_handle} =  Get From Dictionary  ${result}  multivalue_handle

# Creating IPv6 Stack on top of Ethernet Stack for the first Device Group    
	Log  Creating IPv6 Stack on top of Ethernet Stack for the first Device Group
	${result} =  Interface Config  protocol_name="IPv6 1"  protocol_handle=${ethernet_1_handle}  ipv6_multiplier=1  ipv6_resolve_gateway=1  ipv6_manual_gateway_mac=00.00.00.00.00.01  ipv6_manual_gateway_mac_step=00.00.00.00.00.00  ipv6_gateway=2001:0:0:1:0:0:0:1  ipv6_gateway_step=::0  ipv6_intf_addr=${multivalue_2_handle}  ipv6_prefix_length=64
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6_1_handle} =  Get From Dictionary  ${result}  ipv6_handle
	
# Creating IPv6 Stack on top of Ethernet Stack for the second Device Group 
	Log  Creating IPv6 Stack on top of Ethernet Stack for the first Device Group
	${result} =  Interface Config  protocol_name="IPv6 2"  protocol_handle=${ethernet_2_handle}  ipv6_multiplier=1  ipv6_resolve_gateway=1  ipv6_manual_gateway_mac=00.00.00.00.00.01  ipv6_manual_gateway_mac_step=00.00.00.00.00.00  ipv6_gateway=2001:0:0:1:0:0:0:2  ipv6_gateway_step=::0  ipv6_intf_addr=2001:0:0:1:0:0:0:1  ipv6_intf_addr_step=::0  ipv6_prefix_length=64
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6_2_handle} =  Get From Dictionary  ${result}  ipv6_handle
	
################################################################################
# Other protocol configurations                                                # 
################################################################################
	
# This will create MLD v2 Host Stack with IPTV disabled on top of IPv6 stack

# Creating MLD Host Stack on top of IPv6 stack
	Log  Creating MLD Host Stack on top of IPv6 stack in first topology
	${result} =  Emulation MLD Config  mode=create  handle=${ipv6_1_handle}  mld_version=v2  name="MLD Host 1"
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${mldHost_1_handle} =  Get From Dictionary  ${result}  mld_host_handle
	
# Creating multivalue for group address
	Log  Creating multivalue pattern for MLD Host group address
	${result} =  Multivalue Config  pattern=counter  counter_start=ff0a:0:0:0:0:0:0:1  counter_step=1:0:0:0:0:0:0:0  counter_direction=increment  nest_step=0:0:0:1:0:0:0:0  nest_owner=${topology_1_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_3_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	
# Creating MLD Group Ranges 
	Log  Creating MLD Group Ranges
	${result} =  Emulation Multicast Group Config  mode=create  ip_addr_start=${multivalue_3_handle}  ip_addr_step=0:0:0:0:0:0:0:1  num_groups=1  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${mldMcastIPv6GroupList_1_handle} =  Get From Dictionary  ${result}  multicast_group_handle
	
# Creating MLD Source Ranges
	Log  Creating MLD Source Ranges
	${result} =  Emulation Multicast Source Config  mode=create  ip_addr_start=2001:0:0:1:0:0:0:1  ip_addr_step=0:0:0:0:0:0:0:1  num_sources=1  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${mldUcastIPv6SourceList_1_handle} =  Get From Dictionary  ${result}  multicast_source_handle

# This will create MLD v2 Querier Stack on top of IPv6 stack

# Creating MLD Group and Source Ranges in MLD Host stack
	Log  Creating MLD Group and Source Ranges in MLD Host stack
	${result} =  Emulation Mld Group Config  mode=create  g_filter_mode=include  group_pool_handle=${mldMcastIPv6GroupList_1_handle}  no_of_grp_ranges=1  no_of_src_ranges=1  session_handle=${mldHost_1_handle}  source_pool_handle=${mldUcastIPv6SourceList_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${mldGroup_1_handle} =  Get From Dictionary  ${result}  mld_group_handle

# This will create MLD v2 Querier Stack on top of IPv6 stack
	Log  Creating MLD Querier Stack on top of IPv6 stack in second topology
	${result} =  Emulation Mld Querier Config  mode=create  discard_learnt_info=0  active=1  general_query_response_interval=11000  handle=${ipv6_2_handle}  version=version2  general_query_interval=140  name="MLD Querier"
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${mldQuerier_1_handle} =  Get From Dictionary  ${result}  mld_querier_handle
	Log  Waiting 05 seconds before starting protocol(s) ...
	Sleep  5s
############################################################################
# Start MLD protocol                                                      #
############################################################################

	Log  Starting MLD Host on topology1
	${result} =  Emulation Mld Control  handle=${mldHost_1_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Starting MLD Querier on topology2
	${result} =  Emulation Mld Control  handle=${mldQuerier_1_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Waiting for 30 seconds
	Sleep  30s
	
############################################################################
# Retrieve protocol statistics                                             #
############################################################################
	
	Log  Fetching MLD Host aggregated statistics
	${result} =  Emulation Mld Info  handle=${deviceGroup_1_handle}  type=host  mode=aggregate
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
	Log  Fetching MLD Querier aggregated statistics
	${result} =  Emulation Mld Info  handle=${deviceGroup_2_handle}  type=querier  mode=aggregate
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
############################################################################
# Retrieve Learned Info                                                    #
############################################################################
	
	Log  Fetching MLD Querier LearnedInfo
	${result} =  Emulation Mld Info  handle=${mldQuerier_1_handle}  type=querier  mode=learned_info
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
	
############################################################################ 
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv6, Destination->Multicast group                #
# 2. Type      : Multicast IPv6 traffic                                    #
# 3. Flow Group: Source Destination Endpoint Pair                          #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : Source Destination Endpoint Pair                          #
############################################################################
	
	Log  Configuring L2-L3 traffic
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${topology_2_handle}  emulation_dst_handle=${EMPTY}  emulation_multicast_dst_handle=ff0a:0:0:0:0:0:0:1/0:0:0:0:0:0:0:0/1 ff0b:0:0:0:0:0:0:1/0:0:0:0:0:0:0:0/1  emulation_multicast_dst_handle_type=none none  emulation_multicast_rcvr_handle=${mldMcastIPv6GroupList_1_handle} ${mldMcastIPv6GroupList_1_handle}  emulation_multicast_rcvr_port_index=0 0  emulation_multicast_rcvr_host_index=0 1  emulation_multicast_rcvr_mcast_index=0 0  name=TI0-Traffic_Item_1  circuit_endpoint_type=ipv6  transmit_distribution=srcDestEndpointPair0  rate_pps=1000  frame_size=512  track_by=trackingenabled0 sourceDestEndpointPair0
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
# Sending leave using MLD host group handle                                #
############################################################################
	
	Log  Sending leave using MLD host group handle
	${result} =  Emulation Mld Control  mode=leave  group_member_handle=${mldGroup_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  2s

############################################################################
# Sending join using MLD host group handle                                 #
############################################################################
	
	Log  Sending join using MLD host group handle
	${result} =  Emulation Mld Control  mode=join  group_member_handle=${mldGroup_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  2s

	
	
############################################################################
# Making on the fly changes for IGMP Group and Source Ranges               #
############################################################################
	
	Log  Making on the fly changes for MLD Group Ranges
	${result} =  Emulation Multicast Group Config  handle=${mldMcastIPv6GroupList_1_handle}  mode=modify  ip_addr_start=ffff:0:0:1:0:0:0:1  ip_addr_step=0:0:0:0:0:0:0:2  num_groups=2  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Making on the fly changes for MLD Source Ranges
	${result} =  Emulation Multicast Source Config  handle=${mldUcastIPv6SourceList_1_handle}  mode=modify  ip_addr_start=bbbb:0:0:1:0:0:0:1  ip_addr_step=0:0:0:0:0:0:0:1  num_sources=5  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Making on the fly chnages for MLD Group and Source Ranges in MLD Host stack
	${result} =  Emulation Mld Group Config  mode=modify  handle=${mldHost_1_handle}  g_filter_mode=exclude  group_pool_handle=${mldMcastIPv6GroupList_1_handle}  no_of_grp_ranges=1  no_of_src_ranges=1  session_handle=${mldHost_1_handle}  source_pool_handle=${mldUcastIPv6SourceList_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  5s
	
############################################################################
# Making on the fly changes for MLD Querier                                #
############################################################################
	
	Log  Making on the fly changes for MLD Querier
	${result} =  Emulation Mld Querier Config  mode=modify  handle=${mldQuerier_1_handle}  general_query_response_interval=240  router_alert=0  robustness_variable=5  startup_query_count=5  general_query_interval=180
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  2s
	
	
############################################################################
# Applying changes one the fly                                             #
############################################################################
	
	Log  Applying changes on the fly
	${result} =  Test Control  handle=${ipv6_1_handle}  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  5s
	
############################################################################
# Retrieve protocol statistics after doing on the fly changes              #
############################################################################
	
	Log  Fetching MLD Host aggregated statistics
	${result} =  Emulation Mld Info  handle=${deviceGroup_1_handle}  type=host  mode=aggregate
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
	Log  Fetching MLD Querier aggregated statistics
	${result} =  Emulation Mld Info  handle=${deviceGroup_2_handle}  type=querier  mode=aggregate
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
	