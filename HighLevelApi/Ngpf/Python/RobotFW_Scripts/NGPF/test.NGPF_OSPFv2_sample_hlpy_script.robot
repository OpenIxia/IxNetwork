*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.147/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.147/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	12/7  12/8
${client_and_port} =  ${client}:${client_api_port}


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

	${result} =  Topology Config  topology_name=OSPFv2 Topology 1  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 

	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name=OSPFv2 Router 1  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating a topology on second port
	
	${result} =  Topology Config  topology_name=OSPFv2 Topology 2  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology

	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name=OSPFv2 Router 2  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	
################################################################################
#  Configure protocol interfaces                                               #
################################################################################
	
# Creating ethernet stack for the first Device Group 

	${result} =  Interface Config  protocol_name=Ethernet 1  protocol_handle=${deviceGroup_1_handle}  mtu=1500  src_mac_addr=18.03.73.c7.6c.b1  src_mac_addr_step=00.00.00.00.00.00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# Creating ethernet stack for the second Device Group

	${result} =  Interface Config  protocol_name=Ethernet 2  protocol_handle=${deviceGroup_2_handle}  mtu=1500  src_mac_addr=18.03.73.c7.6c.01  src_mac_addr_step=00.00.00.00.00.00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_2_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
	
# Creating IPv4 Stack on top of Ethernet Stack for the first Device Group
	Log To Console  Creating IPv4 Stack on top of Ethernet Stack for the first Device Group
	
	${result} =  Interface Config  protocol_name=IPv4 1  protocol_handle=${ethernet_1_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.1  intf_ip_addr=20.20.20.2  intf_ip_addr_step=0.0.0.0  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_1_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group 
	Log To Console  Creating IPv4 Stack on top of Ethernet Stack for the second Device Group 
	
	${result} =  Interface Config  protocol_name=IPv4 2  protocol_handle=${ethernet_2_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.2  intf_ip_addr=20.20.20.1  intf_ip_addr_step=0.0.0.0  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_2_handle} =  Get From Dictionary  ${result}  ipv4_handle

# ###############################################################################
# Configure OSPFv2 protocol                                                     # 
# ###############################################################################

# Creating OSPFv2 Stack on top of IPv4 Stack for the first Device Group

	Log To Console  Creating OSPFv2 Stack on top of IPv4 1 stack
	${result} =  Emulation Ospf Config  handle=${ipv4_1_handle}  mode=create  network_type=ptop  protocol_name=OSPFv2-IF 1  lsa_discard_mode=0  router_id=193.0.0.1  router_interface_active=1  router_active=1  
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospfv2_handle1} =  Get From Dictionary  ${result}  ospfv2_handle
	
# Creating OSPFv2 Stack on top of IPv4 Stack for the second Device Group

	Log To Console  Creating OSPFv2 Stack on top of IPv4 2 stack
	${result} =  Emulation Ospf Config  handle=${ipv4_2_handle}  mode=create  network_type=ptop  protocol_name=OSPFv2-IF 2  lsa_discard_mode=0  router_id=194.0.0.1  router_interface_active=1  router_active=1  
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospfv2_handle2} =  Get From Dictionary  ${result}  ospfv2_handle
	
# ###############################################################################
# Configure Network Topology & Loopback Device Groups                           # 
# ###############################################################################
	
# Creating Tree Network Topology in Topology 1
	Log To Console  Creating Tree Network Topology in Topology 1
	${result} =  Network Group Config  protocol_handle=${deviceGroup_1_handle}  protocol_name=Network Cloud 1  connected_to_handle=${ethernet_1_handle}  type=ipv4-prefix  ipv4_prefix_network_address=201.1.0.1  ipv4_prefix_length=32  ipv4_prefix_number_of_addresses=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_1_handle} =  Get From Dictionary  ${result}  network_group_handle
	${ipv4PrefixPools_1_handle} =  Get From Dictionary  ${result}  ipv4_prefix_pools_handle

# Configure OSPFv2 group range for topology 1
	Log To Console  Configuring OSPFv2 group range for topology 1
	${result} =  Emulation Ospf Network Group Config  handle=${networkGroup_1_handle}  mode=modify  ipv4_prefix_active=1  ipv4_prefix_route_origin=another_area
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

# Creating IPv4 prefix pool of Network for Network Cloud behind second
# Device Group  with "ipv4_prefix_network_address" =202.1.0.1
	Log To Console  Creating IPv4 prefix pool behind second Device Group
	${result} =  Network Group Config  protocol_handle=${deviceGroup_2_handle}  protocol_name=Network Cloud 2  connected_to_handle=${ethernet_2_handle}  type=ipv4-prefix  ipv4_prefix_network_address=202.1.0.1  ipv4_prefix_length=32  ipv4_prefix_number_of_addresses=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_2_handle} =  Get From Dictionary  ${result}  network_group_handle
	${ipv4PrefixPools_2_handle} =  Get From Dictionary  ${result}  ipv4_prefix_pools_handle
	
# Configure OSPFv2 group range for topology 2
	Log To Console  Configuring OSPFv2 group range for topology 2
	${result} =  Emulation Ospf Network Group Config  handle=${networkGroup_2_handle}  mode=modify  ipv4_prefix_active=1  ipv4_prefix_route_origin=another_area
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

# Going to create Chained Device Group 3 behind Network Cloud 1
# within Topology 1 and renaming of that chained DG to "Loopback Router 1"
	Log To Console  Going to create Chained DG 3 in Topology 1 behind Network Cloud 1 and renaming it
	${result} =  Topology Config  device_group_name=Loopback Router 1  device_group_multiplier=1  device_group_enabled=1  device_group_handle=${networkGroup_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating multivalue loopback adderress within chained DG in Topology 1
	Log To Console  Creating multivalue for loopback adderress within chained DG
	${result} =  Multivalue Config  pattern=counter  counter_start=201.1.0.1  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.0.0.1,0.0.0.1,0.1.0.0  nest_owner=${networkGroup_1_handle},${deviceGroup_1_handle},${topology_1_handle}  nest_enabled=0,0,1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_4_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating Loopback behind Chained DG.
	Log To Console  Creating Loopback behind Chained DG.
	${result} =  Interface Config  protocol_name=IPv4 Loopback 1  protocol_handle=${deviceGroup_1_1_handle}  enable_loopback=1  connected_to_handle=${networkGroup_1_handle}  intf_ip_addr=${multivalue_4_handle}  netmask=255.255.255.255
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4Loopback_1_handle} =  Get From Dictionary  ${result}  ipv4_loopback_handle
	
# Going to create Chained Device Group 4 behind Network Cloud 1 within
# Topology 2 and renaming of that chained DG to "Loopback Router 2"
	Log To Console  Going to create Chained DG 4 in Topology 2 behind Network Cloud 2 and renaming it
	${result} =  Topology Config  device_group_name=Loopback Router 2  device_group_multiplier=1  device_group_enabled=1  device_group_handle=${networkGroup_2_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating multivalue loopback addresses within chained DG in Topology 2
	Log To Console  Creating multivalue for loopback adderress within chained DG
	${result} =  Multivalue Config  pattern=counter  counter_start=202.1.0.1  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.0.0.1,0.0.0.1,0.1.0.0  nest_owner=${networkGroup_2_handle},${deviceGroup_2_handle},${topology_2_handle}  nest_enabled=0,0,1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_4_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating Loopback behind Chained DG.
	Log To Console  Creating Loopback behind Chained DG.
	${result} =  Interface Config  protocol_name=IPv4 Loopback 2  protocol_handle=${deviceGroup_2_1_handle}  enable_loopback=1  connected_to_handle=${networkGroup_2_handle}  intf_ip_addr=${multivalue_4_handle}  netmask=255.255.255.255
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4Loopback_2_handle} =  Get From Dictionary  ${result}  ipv4_loopback_handle
	
	
################################################################################
# Start LDP protocol                                                           #
################################################################################
	Log To Console  Starting LDP on topology1
	${result} =  Emulation Ldp Control  handle=${topology_1_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	Log To Console  Starting LDP on topology2
	${result} =  Emulation Ospf Control  handle=${topology_2_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Test Control  action=start_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log To Console  Waiting for 20 seconds for OSPFv3 sessions to come up ...
	Sleep  20s
	

############################################################################
# Retrieve Learned Info                                                    #
############################################################################
	Log To Console  Fetching OSPFv2 learned info for Topology 1
	${learnedInfo} =  Emulation Ospf Info  handle=${ospfv2_handle1}  mode=learned_info
	${status} =  Get From Dictionary  ${learnedInfo}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${learnedInfo}

################################################################################
# Retrieve protocol statistics                                                 #
################################################################################
	Log  printing protocol statistics ...
	${ospf_stats} =  Emulation Ospf Info  handle=${ospfv2_handle1}  mode=aggregate_stats  
	${status} =  Get From Dictionary  ${ospf_stats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${ospf_stats}
	
################################################################################
# Disabling the OSPFv2 group-range on the topology 2                           #
################################################################################
	
	Log To Console  Disabling the OSPFv2 group-range on the topology 2
	${result} =  Emulation Ospf Network Group Config  handle=${networkGroup_2_handle}  mode=modify  ipv4_prefix_active=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Applying changes one the fly                                                 #
################################################################################
	
	Log To Console  Applying changes on the fly
	${result} =  Test Control  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Waiting for 30 seconds
	Sleep  30s
	
################################################################################
# Retrieve protocol learned info again and notice the difference with          #
# previously retrieved learned info                                            #    
################################################################################
	
	
	Log To Console  Fetching OSPFv2 learned info for Topology 1 after disabling the network range in topology 2
	${learnedInfo} =  Emulation Ospf Info  handle=${ospfv2_handle1}  mode=learned_info
	${status} =  Get From Dictionary  ${learnedInfo}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${learnedInfo}
	
################################################################################
# Enabling the OSPFv2 group-range on the topology 2                            #
################################################################################
	
	Log To Console  Enabling the OSPFv2 group-range on the topology 2
	${result} =  Emulation Ospf Network Group Config  handle=${networkGroup_2_handle}  mode=modify  ipv4_prefix_active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Applying changes one the fly                                                 #
################################################################################
	
	Log To Console  Applying changes on the fly
	${result} =  Test Control  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Waiting for 30 seconds
	Sleep  30s
	
################################################################################
# Retrieve protocol learned info again and notice the difference with          #
# previously retrieved learned info                                            #    
################################################################################
	
	
	Log To Console  Fetching OSPFv2 learned info for Topology 1 after disabling the network range in topology 2
	${learnedInfo} =  Emulation Ospf Info  handle=${ospfv2_handle1}  mode=learned_info
	${status} =  Get From Dictionary  ${learnedInfo}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${learnedInfo}
	

################################################################################
# Configure L2-L3 traffic                                                      #
# 1 Endpoints  : Source->IPv4 loopback, Destination->IPv4 loopback             #
# 2 Type       : Unicast IPv4 traffic                                          #
# 3 Flow Group : On IPv4 Destination Address                                   #
# 4 Rate       : 1000 packets per second                                       #
# 5 Frame Size : 512 bytes                                                     #
# 6 Tracking   : Source Destination EndPoint Set                               #
################################################################################
# Configuring L2-L3 traffic item

	Log  Configure L2-L3 traffic
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${ipv4PrefixPools_1_handle}  emulation_dst_handle=${ipv4PrefixPools_2_handle}  frame_sequencing=disable  frame_sequencing_mode=rx_threshold  name=Traffic_Item_1  circuit_endpoint_type=ipv4  rate_pps=100000  frame_size=64  mac_dst_mode=fixed  mac_src_mode=fixed  mac_src_tracking=1  track_by=sourceDestEndpointPair0 trackingenabled0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

################################################################################# 
# Configure L4-L7 Application traffic                                           #
# 1. Endpoints      : Source->IPv4 Loopback, Destination->IPv4 Loopback         #
# 2. Flow Group     : On IPv4 Destination Address                               #
# 3. objective value: 100                                                       #
#################################################################################
	Log  Configure L4-L7 traffic
	${result} =  Traffic L47 Config  mode=create  name=Traffic Item 2  circuit_endpoint_type=ipv4_application_traffic  emulation_src_handle=${ipv4Loopback_1_handle}  emulation_dst_handle=${ipv4Loopback_2_handle}  objective_type=users  objective_value=100  objective_distribution=apply_full_objective_to_each_port  enable_per_ip_stats=0  flows=Bandwidth_BitTorrent_File_Download Bandwidth_eDonkey Bandwidth_HTTP Bandwidth_IMAPv4 Bandwidth_POP3 Bandwidth_Radius Bandwidth_Raw Bandwidth_Telnet Bandwidth_uTorrent_DHT_File_Download BBC_iPlayer BBC_iPlayer_Radio BGP_IGP_Open_Advertise_Routes BGP_IGP_Withdraw_Routes Bing_Search BitTorrent_Ares_v217_File_Download BitTorrent_BitComet_v126_File_Download BitTorrent_Blizzard_File_Download BitTorrent_Cisco_EMIX BitTorrent_Enterprise BitTorrent_File_Download BitTorrent_LimeWire_v5516_File_Download BitTorrent_RMIX_5M
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

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
# Stop L2-L3 traffic started earlier                                       #
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