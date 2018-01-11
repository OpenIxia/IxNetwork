*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.104/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.104/PythonApi  ngpf

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

	${result} =  Topology Config  topology_name=BGP_1 Topology  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 

	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name=BGP_1 Device Group  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating a topology on second port
	
	${result} =  Topology Config  topology_name=BGP_1 Topology  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology

	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name=BGP_1 Device Group  device_group_multiplier=1  device_group_enabled=1
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
	Log Many  Creating IPv4 Stack on Ethernet Stack for the first Device Group
	
	${result} =  Interface Config  protocol_name=IPv4 1  protocol_handle=${ethernet_1_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.1  gateway_step=0.0.0.0  intf_ip_addr=20.20.20.2  intf_ip_addr_step=0.0.0.0  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_1_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group 
	Log Many  Creating IPv4 2 stack on ethernet 2 stack for the second Device Group
	
	${result} =  Interface Config  protocol_name=IPv4 2  protocol_handle=${ethernet_2_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.2  gateway_step=0.0.0.0  intf_ip_addr=20.20.20.1  intf_ip_addr_step=0.0.0.0  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_2_handle} =  Get From Dictionary  ${result}  ipv4_handle

################################################################################
# Other protocol configurations                                                # 
################################################################################

# This will create BGP Stack on top of IPv4 stack

# Creating BGP Stack on top of IPv4 stack
	Log Many  Creating BGP Stack on top of IPv4 stack in first topology on port 1
	${result} =  Emulation Bgp Config  mode=enable  active=1  handle=${ipv4_1_handle}  remote_ip_addr=20.20.20.1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${bgpIpv4Peer_1_handle} =  Get From Dictionary  ${result}  bgp_handle
	
	Log Many  Creating BGP Stack on top of IPv4 stack in first topology on port 2
	${result} =  Emulation Bgp Config  mode=enable  active=1  handle=${ipv4_2_handle}  remote_ip_addr=20.20.20.2
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${bgpIpv4Peer_2_handle} =  Get From Dictionary  ${result}  bgp_handle
	
# Creating multivalue for network group
	Log Many  Creating multivalue pattern for BGP network group on Port 1
	${result} =  Multivalue Config  pattern=counter  counter_start=200.1.0.0  counter_step=0.1.0.0  counter_direction=increment  nest_step=0.0.0.1 0.1.0.0  nest_owner=${deviceGroup_1_handle} ${topology_1_handle}  nest_enabled=0 1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_4_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating BGP Network Group 
	Log  Creating BGP Network Group on Port 1
	${result} =  Network Group Config  protocol_handle=${deviceGroup_1_handle}  protocol_name=BGP_1_Network_Group1  multiplier=1  enable_device=1  connected_to_handle=${ethernet_1_handle}  type=ipv4-prefix  ipv4_prefix_network_address=${multivalue_4_handle}  ipv4_prefix_length=24  ipv4_prefix_number_of_addresses=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_1_handle} =  Get From Dictionary  ${result}  network_group_handle
	${ipv4PrefixPools_1_handle} =  Get From Dictionary  ${result}  ipv4_prefix_pools_handle
	
# Creating multivalue for network group
	Log  Creating multivalue pattern for BGP network group on Port 2
	${result} =  Multivalue Config  pattern=counter  counter_start=201.1.0.0  counter_step=0.1.0.0  counter_direction=increment  nest_step=0.0.0.1 0.1.0.0  nest_owner=${deviceGroup_2_handle} ${topology_2_handle}  nest_enabled=0 1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_10_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating BGP Network Group
	Log  Creating BGP Network Group on Port 2
	${result} =  Network Group Config  protocol_handle=${deviceGroup_2_handle}  protocol_name=BGP_2_Network_Group1  multiplier=1  enable_device=1  connected_to_handle=${ethernet_2_handle}  type=ipv4-prefix  ipv4_prefix_network_address=${multivalue_10_handle}  ipv4_prefix_length=24  ipv4_prefix_number_of_addresses=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_3_handle} =  Get From Dictionary  ${result}  network_group_handle
	${ipv4PrefixPools_3_handle} =  Get From Dictionary  ${result}  ipv4_prefix_pools_handle
	
# Creating multivalue for IPv4 Loopback
	Log  Creating multivalue for IPv4 Loopback
	${result} =  Topology Config  device_group_name=Device Group 3  device_group_multiplier=1  device_group_enabled=1  device_group_handle=${networkGroup_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_3_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating multivalue pattern for IPv4 Loopback
	Log  Creating multivalue pattern for IPv4 Loopback on Port 1
	${result} =  Multivalue Config  pattern=counter  counter_start=200.1.0.0  counter_step=0.1.0.0  counter_direction=increment  nest_step=0.0.0.1 0.0.0.1 0.1.0.0  nest_owner=${networkGroup_1_handle} ${deviceGroup_1_handle} ${topology_1_handle}  nest_enabled=0 0 1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_7_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating IPv4 Loopback
	Log  Creating IPv4 Loopback on Port 1
	${result} =  Interface Config  protocol_name=IPv4 Loopback 1  protocol_handle=${deviceGroup_3_handle}  enable_loopback=1  connected_to_handle=${networkGroup_1_handle}  intf_ip_addr=${multivalue_7_handle}  netmask=255.255.255.255
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4Loopback_1_handle} =  Get From Dictionary  ${result}  ipv4_loopback_handle
	
# Creating multivalue for IPv4 Loopback
	Log  Creating multivalue for IPv4 Loopback
	${result} =  Topology Config  device_group_name=Device Group 4  device_group_multiplier=1  device_group_enabled=1  device_group_handle=${networkGroup_3_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_4_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating multivalue pattern for IPv4 Loopback
	Log  Creating multivalue pattern for IPv4 Loopback on Port 2
	${result} =  Multivalue Config  pattern=counter  counter_start=201.1.0.0  counter_step=0.1.0.0  counter_direction=increment  nest_step=0.0.0.1 0.0.0.1 0.1.0.0  nest_owner=${networkGroup_3_handle} ${deviceGroup_3_handle} ${topology_2_handle}  nest_enabled=0 0 1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_13_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating IPv4 Loopback
	Log  Creating IPv4 Loopback on Port 2
	${result} =  Interface Config  protocol_name=IPv4 Loopback 2  protocol_handle=${deviceGroup_4_handle}  enable_loopback=1  connected_to_handle=${networkGroup_3_handle}  intf_ip_addr=${multivalue_13_handle}  netmask=255.255.255.255
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4Loopback_2_handle} =  Get From Dictionary  ${result}  ipv4_loopback_handle
	Log  Waiting 05 seconds before starting protocol(s) ...
	Sleep  5s
	
############################################################################
# Start BGP protocol                                                       #
############################################################################
	
	${result} =  Test Control  action=start_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  20s
	
############################################################################
# Retrieve protocol statistics                                             #
############################################################################

	Log  Fetching BGP aggregated statistics on Port1
	${protostats} =  Emulation Bgp Info  handle=${bgpIpv4Peer_1_handle}  mode=stats
	${status} =  Get From Dictionary  ${protostats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log Many  ${protostats}
	
	Log  Fetching BGP aggregated statistics on Port2
	${protostats} =  Emulation Bgp Info  handle=${bgpIpv4Peer_2_handle}  mode=stats
	${status} =  Get From Dictionary  ${protostats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log Many  ${protostats}
	
############################################################################
# Enable IPv4 Learned Information Filter on the Fly                        #
############################################################################
	Log  Enabling IPv4 Unicast Learned Info Filter on Port1
	${bgp_1_status} =  Emulation Bgp Config  handle=${bgpIpv4Peer_1_handle}  mode=modify  ipv4_filter_unicast_nlri=1
	${status} =  Get From Dictionary  ${bgp_1_status}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Enabling IPv4 Unicast Learned Info Filter on Port2
	${bgp_1_status} =  Emulation Bgp Config  handle=${bgpIpv4Peer_2_handle}  mode=modify  ipv4_filter_unicast_nlri=1
	${status} =  Get From Dictionary  ${bgp_1_status}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
###########################################################################
# Applying changes one the fly                                            #
###########################################################################
	Log  Applying changes on the fly
	${applyChanges} =  Test Control  handle=${ipv4_1_handle}  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${applyChanges}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  10s

############################################################################
# Retrieve Learned Info                                                    #
############################################################################
	Log  Fetching BGP LearnedInfo on Port1
	${bgpLearnedInfo} =  Emulation Bgp Info  handle=${bgpIpv4Peer_1_handle}  mode=learned_info
	${status} =  Get From Dictionary  ${bgpLearnedInfo}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${bgpLearnedInfo}
	
	Log  Fetching BGP LearnedInfo on Port2
	${bgpLearnedInfo} =  Emulation Bgp Info  handle=${bgpIpv4Peer_2_handle}  mode=learned_info
	${status} =  Get From Dictionary  ${bgpLearnedInfo}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${bgpLearnedInfo}
	
############################################################################ 
# Configure L2-L3 traffic                                                  #
############################################################################
	Log  Configure L2-L3 traffic
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${networkGroup_1_handle}  emulation_dst_handle=${networkGroup_3_handle}  track_by=sourceDestEndpointPair0 trackingenabled0  rate_pps=1000  frame_size=512
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

############################################################################ 
# Configure L4-L7 traffic                                                  #
############################################################################
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