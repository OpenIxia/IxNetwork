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
	
	${result} =  Connect  reset=1  device=${chassis}  ixnetwork_tcl_server=${client_and_port}  port_list=@{portlist}  username=ixiaHLTQA  break_locks=1  interactive=1
	${connect_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${connect_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	

################################################################################
# Configure Topology, Device Group                                             # 
################################################################################

# Creating a topology on first port
	Log To Console  Adding topology 1 on port 1
	${result} =  Topology Config  topology_name=ISIS Topology 1  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 1 in topology 1
	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name=Device Group 1  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating a topology on second port
	Log To Console  Adding topology 2 on port 2
	${result} =  Topology Config  topology_name=ISIS Topology 2  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology
	Log To Console  Creating device group 2 in topology 2
	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name=Device Group 2  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_4_handle} =  Get From Dictionary  ${result}  device_group_handle
	
################################################################################
#  Configure protocol interfaces                                               #
################################################################################
	
# Creating ethernet stack for the first Device Group 
	Log To Console  Creating ethernet stack for the first Device Group
	${result} =  Interface Config  protocol_name=Ethernet 1  protocol_handle=${deviceGroup_1_handle}  mtu=1500  src_mac_addr=18.03.73.c7.6c.b2
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# Creating ethernet stack for the second Device Group
	Log To Console  Creating ethernet for the second Device Group
	${result} =  Interface Config  protocol_name=Ethernet 2  protocol_handle=${deviceGroup_4_handle}  mtu=1500  src_mac_addr=18.03.73.c7.6c.01
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_2_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
	
# Creating IPv4 Stack on top of Ethernet Stack
	Log To Console  Creating IPv4 Stack on top of Ethernet Stack
	${result} =  Interface Config  protocol_name=IPv4 1  protocol_handle=${ethernet_1_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.1  intf_ip_addr=20.20.20.2  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_1_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
# Creating IPv4 Stack on top of Ethernet Stack
	Log To Console  Creating IPv4 Stack on top of Ethernet Stack
	${result} =  Interface Config  protocol_name=IPv4 2  protocol_handle=${ethernet_2_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.2  intf_ip_addr=20.20.20.1  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_2_handle} =  Get From Dictionary  ${result}  ipv4_handle

################################################################################
# Other protocol configurations                                                # 
################################################################################
################################################################################
# Creating  ISIS Stack on top of ethernet stack                                #
# Descrtiption of protocol arguments : discard_lsp: enables learning LSPs      #
#                                      intf_type: sets interface type          #
#                                      system_id: sets system id               #
#                                      protocol_name: sets prtoocol name       #
#                                      active: activates ISIS router           #
#                                      if_active: activates router interface   #
################################################################################

	Log To Console  Creating ISIS Stack on top of ethernet 1 stack
	${result} =  Emulation Isis Config  mode=create  discard_lsp=0  handle=${ethernet_1_handle}  intf_type=ptop  routing_level=L2  system_id=64:01:00:01:00:00  protocol_name=ISIS-L3 IF 1  active=1  if_active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${isisL3_1_handle} =  Get From Dictionary  ${result}  isis_l3_handle

# Creating ISIS Network Group in port 1
	Log To Console  Creating ISIS IPv4 Network group in port 1
	${result} =  Network Group Config  protocol_handle=${deviceGroup_1_handle}  protocol_name=ISIS Network Group 1  enable_device=1  connected_to_handle=${ethernet_1_handle}  type=ipv4-prefix
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_1_handle} =  Get From Dictionary  ${result}  network_group_handle
	${ipv4PrefixPools_1_handle} =  Get From Dictionary  ${result}  ipv4_prefix_pools_handle
	
	Log To Console  Creating ISIS IPv4 Network group in port 1
	${result} =  Emulation Isis Network Group Config  handle=${networkGroup_1_handle}  mode=modify  enable_device=1  stub_router_origin=stub
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Topology Config  device_group_name=Device Group 3  device_group_multiplier=1  device_group_enabled=1  device_group_handle=${networkGroup_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	

# Creating ipv4 Loopback interface for applib traffic
	Log  Adding ipv4 loopback1 for applib traffic
	${result} =  Interface Config  protocol_name=IPv4 Loopback 1  protocol_handle=${deviceGroup_2_handle}  enable_loopback=1  connected_to_handle=${networkGroup_1_handle}  intf_ip_addr=4.4.4.4
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4Loopback_1_handle} =  Get From Dictionary  ${result}  ipv4_loopback_handle
	
	
# Creating ISIS Network group 3 for ipv6 ranges
	Log To Console  Creating ISIS Network group 3 for ipv6 ranges
	${result} =  Network Group Config  protocol_handle=${deviceGroup_1_handle}  protocol_name=ISIS Network Group 3  connected_to_handle=${ethernet_1_handle}  type=ipv6-prefix
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_3_handle} =  Get From Dictionary  ${result}  network_group_handle
	${ipv6PrefixPools_1_handle} =  Get From Dictionary  ${result}  ipv6_prefix_pools_handle
	
	${result} =  Emulation Isis Network Group Config  handle=${networkGroup_3_handle}  mode=modify  enable_device=1  stub_router_origin=stub
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Topology Config  device_group_name=Device Group 6  device_group_multiplier=1  device_group_enabled=1  device_group_handle=${networkGroup_3_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_3_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating ipv6 loopback 1 interface for applib traffic
	Log  Adding ipv6 loopback1 for applib traffic
	${result} =  Interface Config  protocol_name=IPv6 Loopback 2  protocol_handle=${deviceGroup_3_handle}  enable_loopback=1  connected_to_handle=${networkGroup_3_handle}  ipv6_intf_addr=2222:0:1:0:0:0:0:1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6Loopback_1_handle} =  Get From Dictionary  ${result}  ipv6_loopback_handle
	
################################################################################
# Creating  ISIS Stack on top of ethernet stack                                #
# Descrtiption of protocol arguments : discard_lsp: enables learning LSPs      #
#                                      intf_type: sets interface type          #
#                                      system_id: sets system id               #
#                                      protocol_name: sets prtoocol name       #
#                                      active: activates ISIS router           #
#                                      if_active: activates router interface   #
################################################################################
	
	Log To Console  Creating ISIS Stack on top of ethernet 1 stack
	${result} =  Emulation Isis Config  mode=create  discard_lsp=0  handle=${ethernet_2_handle}  intf_type=ptop  routing_level=L2  system_id=65:01:00:01:00:00  protocol_name=ISIS-L3 IF 2  active=1  if_active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${isisL3_2_handle} =  Get From Dictionary  ${result}  isis_l3_handle

# Creating IPv4 Prefix Ranges
	Log To Console  Creating ISIS IPv4 Prefix Ranges
	${result} =  Network Group Config  protocol_handle=${deviceGroup_4_handle}  protocol_name=ISIS Network Group 2  enable_device=1  connected_to_handle=${ethernet_2_handle}  type=ipv4-prefix
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_5_handle} =  Get From Dictionary  ${result}  network_group_handle
	${ipv4PrefixPools_3_handle} =  Get From Dictionary  ${result}  ipv4_prefix_pools_handle
	
	${result} =  Emulation Isis Network Group Config  handle=${networkGroup_5_handle}  mode=modify  enable_device=1  stub_router_origin=stub
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
# Creating a device group in topology for loopback interface
	Log To Console  Creating a device group in topology for loopback interface
	${result} =  Topology Config  device_group_name=Device Group 4  device_group_multiplier=1  device_group_enabled=1  device_group_handle=${networkGroup_5_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_5_handle} =  Get From Dictionary  ${result}  device_group_handle
	

# Creating ipv4 loopback 2 for applib traffic
	Log  Adding ipv4 loopback2 for applib traffic
	${result} =  Interface Config  protocol_name=IPv4 Loopback 2  protocol_handle=${deviceGroup_5_handle}  enable_loopback=1  connected_to_handle=${networkGroup_5_handle}  intf_ip_addr=5.5.5.5
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4Loopback_2_handle} =  Get From Dictionary  ${result}  ipv4_loopback_handle
	
	
# Creating ISIS Prefix ranges
	Log To Console  Creating ISIS IPv6 Prefix ranges
	${result} =  Network Group Config  protocol_handle=${deviceGroup_4_handle}  protocol_name=ISIS Network Group 4  connected_to_handle=${ethernet_2_handle}  type=ipv6-prefix
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_7_handle} =  Get From Dictionary  ${result}  network_group_handle
	${ipv6PrefixPools_3_handle} =  Get From Dictionary  ${result}  ipv6_prefix_pools_handle
	
	${result} =  Emulation Isis Network Group Config  handle=${networkGroup_7_handle}  mode=modify  enable_device=1  stub_router_origin=stub
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
# Creating a device group in topology for loopback interface
	Log To Console  Creating device group 2 in topology 2 for loopback interface
	${result} =  Topology Config  device_group_name=Device Group 5  device_group_multiplier=1  device_group_enabled=1  device_group_handle=${networkGroup_7_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_6_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating ipv6 loopback 2 for applib traffic
	Log  Adding ipv6 loopback2 for applib traffic
	${result} =  Interface Config  protocol_name=IPv6 Loopback 2  protocol_handle=${deviceGroup_6_handle}  enable_loopback=1  connected_to_handle=${networkGroup_7_handle}  ipv6_intf_addr=2222:0:0:0:0:0:0:1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6Loopback_2_handle} =  Get From Dictionary  ${result}  ipv6_loopback_handle
	
	Log To Console  Waiting 5 seconds before starting protocol(s) ...
	Sleep  5s
	
############################################################################
# Start ISIS protocol                                                      #
############################################################################   
	
	
	Log To Console  Performing Start on ISIS interfaces
	${result} =  Emulation Isis Control  handle=${isisL3_1_handle}  mode=stop
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Isis Control  handle=${isisL3_2_handle}  mode=stop
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	${result} =  Test Control  action=start_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  40s
	
############################################################################
# Retrieve protocol statistics                                             #
############################################################################

	Log  Fetching BGP aggregated statistics on Port1
	${protostats} =  Emulation Isis Info  handle=${isisL3_1_handle}  mode=stats
	${status} =  Get From Dictionary  ${protostats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log Many  ${protostats}
	


############################################################################
# Retrieve Learned Info                                                    #
############################################################################
	Log  Fetching BGP LearnedInfo on Port1
	${isisLearnedInfo} =  Emulation Isis Info  handle=${isisL3_1_handle}  mode=learned_info
	${status} =  Get From Dictionary  ${isisLearnedInfo}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${isisLearnedInfo}
	
	Log  Fetching BGP LearnedInfo on Port2
	${isisLearnedInfo} =  Emulation Isis Info  handle=${isisL3_1_handle}  mode=learned_info
	${status} =  Get From Dictionary  ${isisLearnedInfo}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${isisLearnedInfo}
	
################################################################################
# Configure_L2_L3_IPv4 traffic                                                 #
################################################################################
	Log  Configuring L2-L3 IPv4 traffic item ...
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${ipv4PrefixPools_1_handle}  emulation_dst_handle=${ipv4PrefixPools_3_handle}  name=Traffic_Item_1  circuit_endpoint_type=ipv4  rate_pps=1000  frame_size=512  track_by=sourceDestEndpointPair0 ipv4DestIp0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${traffic_item_ipv4} =  Get From Dictionary  ${result}  traffic_item
	
################################################################################
# Configure_L2_L3_IPv6 traffic                                                 #
################################################################################
	Log  Configuring L2-L3 IPv6 traffic item ...
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  endpointset_count=1  circuit_endpoint_type=ipv6  emulation_src_handle=${ipv6PrefixPools_1_handle}  emulation_dst_handle=${ipv6PrefixPools_3_handle}  name=Traffic_Item_2  tag_filter=${EMPTY}  merge_destinations=1  pending_operations_timeout=30
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${traffic_item_ipv6} =  Get From Dictionary  ${result}  traffic_item
	
	Log  Modify L2-L3 IPv6 traffic item ...
	${result} =  Traffic Config  mode=modify  traffic_generator=ixnetwork_540  stream_id=${traffic_item_ipv6}  track_by=trackingenabled0 ipv6DestIp0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Configure_L4_L7_IPv4                                                         #
################################################################################
	Log  Set applib traffic mode in variable traffic_mode, for IPv4: 1, IPv6: 2
	${result} =  Traffic L47 Config  mode=create  name=Traffic Item 3  circuit_endpoint_type=ipv6_application_traffic  emulation_src_handle=${ipv6PrefixPools_1_handle}  emulation_dst_handle=${ipv6PrefixPools_3_handle}  objective_type=users  objective_value=100  objective_distribution=apply_full_objective_to_each_port  enable_per_ip_stats=0  flows=Bandwidth_BitTorrent_File_Download Bandwidth_eDonkey Bandwidth_HTTP Bandwidth_IMAPv4 Bandwidth_POP3 Bandwidth_Radius Bandwidth_Raw Bandwidth_Telnet Bandwidth_uTorrent_DHT_File_Download BBC_iPlayer BBC_iPlayer_Radio BGP_IGP_Open_Advertise_Routes BGP_IGP_Withdraw_Routes Bing_Search BitTorrent_Ares_v217_File_Download
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${traffic_item_l47} =  Get From Dictionary  ${result}  traffic_l47_handle
############################################################################
#  Start L2-L3 & L4-L7 traffic configured earlier                          #
############################################################################
	Log  Running Traffic
	${result} =  Traffic Control  action=run  traffic_generator=ixnetwork_540  type=l23 l47
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	Log  Let the traffic run for 60 seconds
	Sleep  60s
	
############################################################################
# Retrieve L2-L3 & L4-L7 traffic stats                                     #
############################################################################

	Log  Retrieving L2-L3 & L4-L7 traffic stats
	${protostats} =  Traffic Stats  mode=all  traffic_generator=ixnetwork_540  measure_mode=mixed
	${status} =  Get From Dictionary  ${protostats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${protostats}

############################################################################
# Stop L2-L3 & L4-L7 traffic started earlier                                       #
############################################################################

	Log  Stopping Traffic
	${result} =  Traffic Control  action=stop  traffic_generator=ixnetwork_540  type=l23 l47
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  2s
	
############################################################################
# Stop all protocols                                                       #
############################################################################

	Log  Stopping all protocols
	${result} =  Test Control  action=stop_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  2s
	Log  !!! Test Script Ends !!!