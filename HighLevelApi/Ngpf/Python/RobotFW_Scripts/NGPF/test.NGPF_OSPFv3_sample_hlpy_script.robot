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

	${result} =  Topology Config  topology_name=OSPFv3 Topology 1  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 

	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name=OSPFv3 Router 1  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating a topology on second port
	
	${result} =  Topology Config  topology_name=OSPFv3 Topology 2  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology

	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name=OSPFv3 Router 2  device_group_multiplier=1  device_group_enabled=1
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
	
	
# Creating IPv6 Stack on top of Ethernet Stack for the first Device Group
	Log To Console  Creating IPv6 Stack on top of Ethernet Stack for the first Device Group
	
	${result} =  Interface Config  protocol_name=IPv6 1  protocol_handle=${ethernet_1_handle}  ipv6_gateway=2000:0:0:1:0:0:0:2  ipv6_intf_addr=2000:0:0:1:0:0:0:1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6_1_handle} =  Get From Dictionary  ${result}  ipv6_handle
	
# Creating IPv6 Stack on top of Ethernet Stack for the second Device Group 
	Log To Console  Creating IPv6 Stack on top of Ethernet Stack for the second Device Group 
	
	${result} =  Interface Config  protocol_name=IPv6 2  protocol_handle=${ethernet_2_handle}  ipv6_gateway=2000:0:0:1:0:0:0:1  ipv6_intf_addr=2000:0:0:1:0:0:0:2
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6_2_handle} =  Get From Dictionary  ${result}  ipv6_handle

# ###############################################################################
# Configure OSPFv3 protocol                                                     # 
# ###############################################################################

# Creating OSPFv3 Stack on top of IPv6 Stack for the first Device Group

	Log To Console  Creating OSPFv3 Stack on top of IPv6 1 stack
	${result} =  Emulation Ospf Config  handle=${ipv6_1_handle}  area_id_type=area_id_as_number  router_interface_active=1  protocol_name=OSPFv3-IF 1  router_active=1  lsa_discard_mode=0  network_type=ptop  mode=create  session_type=ospfv3
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospfv3_1_handle} =  Get From Dictionary  ${result}  ospfv3_handle
	
# Creating OSPFv3 Stack on top of IPv6 Stack for the second Device Group

	Log To Console  Creating OSPFv3 Stack on top of IPv6 2 stack
	${result} =  Emulation Ospf Config  handle=${ipv6_2_handle}  area_id_type=area_id_as_number  router_interface_active=1  protocol_name=OSPFv3-IF 2  router_active=1  lsa_discard_mode=0  network_type=ptop  mode=create  session_type=ospfv3
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospfv3_2_handle} =  Get From Dictionary  ${result}  ospfv3_handle
	
# ###############################################################################
# Configure Network Topology & Loopback Device Groups                           # 
# ###############################################################################
	
# Creating Tree Network Topology in Topology 1
	Log To Console  Creating Tree Network Topology in Topology 1
	${result} =  Network Group Config  protocol_handle=${deviceGroup_1_handle}  protocol_name=OSPFv3 Network Group 1  multiplier=1  enable_device=1  type=tree
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_1_handle} =  Get From Dictionary  ${result}  network_group_handle
	${simRouter_1_handle} =  Get From Dictionary  ${result}  simulated_router_handle
	${interAreaPrefix_1_handle} =  Get From Dictionary  ${result}  v3_inter_area_prefix_handle
	
	
# Creating Loopback Device Group in Topology 1
	Log  Creating Loopback Device Group in Topology 1
	${result} =  Topology Config  device_group_name=Applib Endpoint 1  device_group_multiplier=7  device_group_enabled=1  device_group_handle=${networkGroup_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_3_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating multivalue pattern for IPv6 Loopback
	Log  Creating multivalue pattern for IPv6 Loopback on Port 1
	${result} =  Multivalue Config  pattern=counter  counter_start=3000:0:1:1:0:0:0:0  counter_step=0:0:0:1:0:0:0:0  counter_direction=increment  nest_step=0:0:0:0:0:0:0:1,0:0:0:0:0:0:0:1,0:0:0:1:0:0:0:0  nest_owner=${networkGroup_1_handle},${deviceGroup_1_handle},${topology_1_handle}  nest_enabled=0,0,1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_1_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating IPv6 Loopback
	Log  Creating IPv4 Loopback on Port 1
	${result} =  Interface Config  protocol_name=IPv6 Loopback 1  protocol_handle=${deviceGroup_3_handle}  enable_loopback=1  connected_to_handle=${simRouter_1_handle}  ipv6_intf_addr=${multivalue_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6Loopback_1_handle} =  Get From Dictionary  ${result}  ipv6_loopback_handle
	
	
# Creating Tree Network Topology in Topology 2
	Log To Console  Creating Tree Network Topology in Topology 2
	${result} =  Network Group Config  protocol_handle=${deviceGroup_2_handle}  protocol_name=OSPFv3 Network Group 2  multiplier=1  enable_device=1  type=tree
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_2_handle} =  Get From Dictionary  ${result}  network_group_handle
	${simRouter_2_handle} =  Get From Dictionary  ${result}  simulated_router_handle
	${interAreaPrefix_2_handle} =  Get From Dictionary  ${result}  v3_inter_area_prefix_handle
	
	
# Creating Loopback Device Group in Topology 2
	Log  Creating Loopback Device Group in Topology 2
	${result} =  Topology Config  device_group_name=Applib Endpoint 2  device_group_multiplier=7  device_group_enabled=1  device_group_handle=${networkGroup_2_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_4_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating multivalue pattern for IPv6 Loopback
	Log  Creating multivalue pattern for IPv6 Loopback on Port 1
	${result} =  Multivalue Config  pattern=counter  counter_start=3000:5:1:1:0:0:0:0  counter_step=0:0:0:1:0:0:0:0  counter_direction=increment  nest_step=0:0:0:0:0:0:0:1,0:0:0:0:0:0:0:1,0:0:0:1:0:0:0:0  nest_owner=${networkGroup_2_handle},${deviceGroup_2_handle},${topology_2_handle}  nest_enabled=0,0,1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_2_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating IPv6 Loopback
	Log  Creating IPv4 Loopback on Port 1
	${result} =  Interface Config  protocol_name=IPv6 Loopback 2  protocol_handle=${deviceGroup_4_handle}  enable_loopback=1  connected_to_handle=${simRouter_2_handle}  ipv6_intf_addr=${multivalue_2_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6Loopback_1_handle} =  Get From Dictionary  ${result}  ipv6_loopback_handle
	
# ###########################################################################
# Start all protocols                                                       #
# ###########################################################################
	Log To Console  Performing Start on ISIS interfaces
	${result} =  Emulation Ospf Control  handle=${ospfv3_1_handle}  mode=stop
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Ospf Control  handle=${ospfv3_2_handle}  mode=stop
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Test Control  action=start_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log To Console  Waiting for 20 seconds for OSPFv3 sessions to come up ...
	Sleep  20s
	
# ###############################################################################
# Making on the fly changes for Inter-Area Prefix Network Address in            #
# both Network Topologies                                                       #
# ###############################################################################
# Modifying Inter-Area Prefix Network Address in Network Topology 1
	Log To Console  Modifying Inter-Area Prefix Network Address in Network Topology 1
	${result} =  Multivalue Config  pattern=counter  counter_start=3000:0:1:1:0:0:0:0  counter_step=0:0:0:1:0:0:0:0  counter_direction=increment  nest_step=0:0:0:0:0:0:0:1,0:0:1:0:0:0:0:0  nest_owner=${deviceGroup_1_handle},${topology_1_handle}  nest_enabled=0,1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_3_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Emulation Ospf Network Group Config  handle=${networkGroup_1_handle}  mode=modify  inter_area_prefix_active=1  inter_area_prefix_network_address=${multivalue_3_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
# Modifying Inter-Area Prefix Network Address in Network Topology 2
	Log To Console  Modifying Inter-Area Prefix Network Address in Network Topology 2
	${result} =  Multivalue Config  pattern=counter  counter_start=3000:5:1:1:0:0:0:0  counter_step=0:0:0:1:0:0:0:0  counter_direction=increment  nest_step=0:0:0:0:0:0:0:1,0:0:1:0:0:0:0:0  nest_owner=${deviceGroup_2_handle},${topology_2_handle}  nest_enabled=0,1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_4_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Emulation Ospf Network Group Config  handle=${networkGroup_2_handle}  mode=modify  inter_area_prefix_active=1  inter_area_prefix_network_address=${multivalue_4_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
###########################################################################
# Applying changes one the fly                                            #
###########################################################################
	Log  Applying changes on the fly
	${applyChanges} =  Test Control  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${applyChanges}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  10s

############################################################################
# Retrieve Learned Info                                                    #
############################################################################
	Log  Fetching OSPFv3 statistics ...
	${protostats} =  Emulation Ospf Info  handle=${ospfv3_1_handle}  session_type=ospfv3  mode=aggregate_stats
	${status} =  Get From Dictionary  ${protostats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${protostats}

	Log  Fetching OSPFv3 statistics ...
	${protostats} =  Emulation Ospf Info  handle=${ospfv3_1_handle}  session_type=ospfv3  mode=learned_info
	${status} =  Get From Dictionary  ${protostats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${protostats}
	
# ########################################################################### 
# Configure L2-3 & L4-7 traffic                                             #
# 1. Endpoints : Source->IPv6, Destination->IPv6                            #
# 2. Type      : Unicast IPv6 traffic                                       #
# 3. Flow Group: On IPv6 Destination Address                                #
# 4. Rate      : 2000 pps                                                   #
# 5. Frame Size: 500 bytes                                                  #
# 6. Tracking  : Source Destination EndpointPair                            #    
# ###########################################################################
# Configuring L2-L3 traffic item

	Log  Configure L2-L3 traffic
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${interAreaPrefix_1_handle}  emulation_dst_handle=${interAreaPrefix_2_handle}  name=Traffic_Item_1  circuit_endpoint_type=ipv6  track_by=sourceDestEndpointPair0 trackingenabled0  rate_pps=2000  frame_size=500
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

############################################################################ 
# Configure L4-L7 traffic                                                  #
############################################################################
	Log  Configure L4-L7 traffic
	${result} =  Traffic L47 Config  mode=create  name=Traffic Item 2  circuit_endpoint_type=ipv6_application_traffic  emulation_src_handle=${networkGroup_1_handle}  emulation_dst_handle=${networkGroup_2_handle}  objective_type=users  objective_value=100  objective_distribution=apply_full_objective_to_each_port  enable_per_ip_stats=0  flows=Bandwidth_BitTorrent_File_Download Bandwidth_eDonkey Bandwidth_HTTP Bandwidth_IMAPv4 Bandwidth_POP3 Bandwidth_Radius Bandwidth_Raw Bandwidth_Telnet Bandwidth_uTorrent_DHT_File_Download BBC_iPlayer BBC_iPlayer_Radio BGP_IGP_Open_Advertise_Routes BGP_IGP_Withdraw_Routes Bing_Search BitTorrent_Ares_v217_File_Download BitTorrent_BitComet_v126_File_Download BitTorrent_Blizzard_File_Download BitTorrent_Cisco_EMIX BitTorrent_Enterprise BitTorrent_File_Download BitTorrent_LimeWire_v5516_File_Download BitTorrent_RMIX_5M
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