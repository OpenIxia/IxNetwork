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
	${result} =  Topology Config  topology_name="IGMP Host Topology"  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log  Creating device group 1 in topology 1
	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name="IGMP Host Device Group"  device_group_multiplier=2  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating a topology on second port
	Log  Adding topology 2 on port 2
	${result} =  Topology Config  topology_name="IGMP Querier Topology"  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log  Creating device group 2 in topology 2
	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name="IGMP Querier Device Group"  device_group_multiplier=1  device_group_enabled=1
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
	
# Creating multivalue for IPv4
	
	${result} =  Multivalue Config  pattern=counter  counter_start=20.20.20.2  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.1.0.0  nest_owner=${topology_1_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_2_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating IPv4 Stack on top of Ethernet Stack for the first Device Group     
	Log  Creating IPv4 Stack on top of Ethernet Stack for the first Device Group
	${result} =  Interface Config  protocol_name="IPv4 1"  protocol_handle=${ethernet_1_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.1  gateway=0.0.0.0  intf_ip_addr=${multivalue_2_handle}  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_1_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group 
	Log  Creating IPv4 2 stack on ethernet 2 stack for the second Device Group
	${result} =  Interface Config  protocol_name="IPv4 2"  protocol_handle=${ethernet_2_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.2  gateway=0.0.0.0  intf_ip_addr=20.20.20.1  intf_ip_addr_step=0.0.0.0  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_2_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
################################################################################
# Other protocol configurations                                                # 
################################################################################
	
# This will create IGMP v3 Host Stack with IPTV disabled on top of IPv4 stack

# Creating IGMP Host Stack on top of IPv4 stack
	Log  Creating IGMP Host Stack on top of IPv4 stack in first topology  
	${result} =  Emulation Igmp Config  handle=${ipv4_1_handle}  protocol_name="IGMP Host"  mode=create  filter_mode=include  igmp_version=v3
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${igmpHost_1_handle} =  Get From Dictionary  ${result}  igmp_host_handle
	
# Creating multivalue for group address
	Log  Creating multivalue pattern for IGMP Host group address
	${result} =  Multivalue Config  pattern=counter  counter_start=226.0.0.1  counter_step=1.0.0.0  counter_direction=increment  nest_step=0.1.0.0  nest_owner=${topology_1_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_3_handle} =  Get From Dictionary  ${result}  multivalue_handle
# Creating IGMP Group Ranges 
	Log  Creating IGMP Group Ranges"
	${result} =  Emulation Multicast Group Config  mode=create  ip_addr_start=${multivalue_3_handle}  ip_addr_step=0.0.0.1  num_groups=1  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${igmpMcastIPv4GroupList_1_handle} =  Get From Dictionary  ${result}  multicast_group_handle
# Creating IGMP Source Ranges
	Log  Creating IGMP Source Ranges
	${result} =  Emulation Multicast Source Config  mode=create  ip_addr_start=20.20.20.1  ip_addr_step=0.0.0.1  num_sources=1  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${igmpUcastIPv4SourceList_1_handle} =  Get From Dictionary  ${result}  multicast_source_handle
	
# Creating IGMP Group and Source Ranges in IGMP Host stack
	Log  Creating IGMP Group and Source Ranges in IGMP Host stack
	${result} =  Emulation Igmp Group Config  mode=create  g_filter_mode=include  group_pool_handle=${igmpMcastIPv4GroupList_1_handle}  no_of_grp_ranges=1  no_of_src_ranges=1  session_handle=${igmpHost_1_handle}  source_pool_handle=${igmpUcastIPv4SourceList_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${igmpGroup_1_handle} =  Get From Dictionary  ${result}  igmp_group_handle
# This will create IGMP v3 Querier Stack on top of IPv6 stack

# Creating IGMP Querier Stack on top of IPv4 stack
	Log  Creating IGMP Querier Stack on top of IPv4 stack in second topology
	${result} =  Emulation Igmp Querier Config  mode=create  discard_learned_info=0  active=1  general_query_response_interval=11000  handle=${ipv4_2_handle}  igmp_version=v3  query_interval=140  name="IGMP Querier"
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${igmpQuerier_1_handle} =  Get From Dictionary  ${result}  igmp_querier_handle
	
	Log  Waiting 05 seconds before starting protocol(s) ...
	
	Sleep  5s
	
############################################################################
# Start IGMP protocol                                                      #
############################################################################

	Log  Starting IGMP Host on topology1
	${result} =  Emulation Igmp Control  handle=${igmpHost_1_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Starting IGMP Querier on topology2
	${result} =  Emulation Igmp Control  handle=${igmpQuerier_1_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Waiting for 40 seconds
	Sleep  40s
	
############################################################################
# Retrieve protocol statistics                                             #
############################################################################
	
	Log  Fetching IGMP Host aggregated statistics
	${result} =  Emulation Igmp Info  handle=${deviceGroup_1_handle}  type=host  mode=aggregate
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
	Log  Fetching IGMP Querier aggregated statistics
	${result} =  Emulation Igmp Info  handle=${deviceGroup_2_handle}  type=querier  mode=aggregate
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
############################################################################
# Retrieve Learned Info                                                    #
############################################################################
	
	Log  Fetching IGMP Querier LearnedInfo
	${result} =  Emulation Igmp Info  handle=${igmpQuerier_1_handle}  type=querier  mode=learned_info
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
############################################################################ 
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv4, Destination->Multicast group                #
# 2. Type      : Multicast IPv4 traffic                                    #
# 3. Flow Group: Source Destination Endpoint Pair                          #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : Source Destination Endpoint Pair                          #
############################################################################
	
	Log  Configuring L2-L3 traffic
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${topology_2_handle}  emulation_dst_handle=${EMPTY}  emulation_multicast_dst_handle=226.0.0.1/0.0.0.0/1 227.0.0.1/0.0.0.0/1  emulation_multicast_dst_handle_type=none none  emulation_multicast_rcvr_handle=${igmpMcastIPv4GroupList_1_handle} ${igmpMcastIPv4GroupList_1_handle}  emulation_multicast_rcvr_port_index=0 0  emulation_multicast_rcvr_host_index=0 1  emulation_multicast_rcvr_mcast_index=0 0  name=TI0-Traffic_Item_1  circuit_endpoint_type=ipv4  transmit_distribution=srcDestEndpointPair0  rate_pps=1000  frame_size=512  track_by=trackingenabled0 sourceDestEndpointPair0
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
# Sending leave using IGMP host group handle                               #
############################################################################
	
	Log  Sending leave using IGMP host group handle
	${result} =  Emulation Igmp Control  mode=leave  group_member_handle=${igmpGroup_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  2s
	
############################################################################
# Sending join using IGMP host group handle                                #
############################################################################
	
	Log  Sending join using IGMP host group handle
	${result} =  Emulation Igmp Control  mode=join  group_member_handle=${igmpGroup_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  2s
	
############################################################################
# Making on the fly changes for IGMP Group and Source Ranges               #
############################################################################
	
	Log  Making on the fly changes for IGMP Group Ranges
	${result} =  Emulation Multicast Group Config  handle=${igmpMcastIPv4GroupList_1_handle}  mode=modify  ip_addr_start=230.1.1.1  ip_addr_step=0.0.0.2  num_groups=2  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Making on the fly changes for IGMP Source Ranges
	${result} =  Emulation Multicast Source Config  handle=${igmpUcastIPv4SourceList_1_handle}  mode=modify  ip_addr_start=30.30.30.1  ip_addr_step=0.0.0.1  num_sources=5  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Making on the fly chnages for IGMP Group and Source Ranges in IGMP Host stack
	${result} =  Emulation Igmp Group Config  mode=modify  handle=${igmpHost_1_handle}  g_filter_mode=exclude  group_pool_handle=${igmpMcastIPv4GroupList_1_handle}  no_of_grp_ranges=1  no_of_src_ranges=1  session_handle=${igmpHost_1_handle}  source_pool_handle=${igmpUcastIPv4SourceList_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  5s
	
############################################################################
# Making on the fly changes for IGMP Querier                               #
############################################################################
	
	Log  Making on the fly changes for IGMP Querier
	${result} =  Emulation Igmp Querier Config  mode=modify  handle=${igmpQuerier_1_handle}  general_query_response_interval=240  ip_router_alert=0  robustness_variable=5  startup_query_count=5  query_interval=180
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  2s
	
############################################################################
# Applying changes one the fly                                             #
############################################################################
	
	Log  Applying changes on the fly
	${result} =  Test Control  handle=${ipv4_1_handle}  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  5s
	
############################################################################
# Retrieve protocol statistics  after making on the fly changes             #
############################################################################
	
	Log  Fetching IGMP Host aggregated statistics
	${result} =  Emulation Igmp Info  handle=${deviceGroup_1_handle}  type=host  mode=aggregate
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
	Log  Fetching IGMP Querier aggregated statistics
	${result} =  Emulation Igmp Info  handle=${deviceGroup_2_handle}  type=querier  mode=aggregate
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
	#Log  Sleep !!! Test Script Ends !!!
	