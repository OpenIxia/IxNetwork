*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.151/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.151/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.191
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	9/1  9/2
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
	Log To Console  Adding topology 1 on port 1
	${result} =  Topology Config  topology_name=BGP Topology 1  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 1 in topology 1
	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name=BGP Topology 1 Router  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating a topology on second port
	Log To Console  Adding topology 2 on port 2
	${result} =  Topology Config  topology_name=BGP Topology 2  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology
	Log To Console  Creating device group 2 in topology 2
	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name=BGP Topology Router 2  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	
################################################################################
#  Configure protocol interfaces                                               #
################################################################################
	
# Creating ethernet stack for the first Device Group 
	Log To Console  Creating ethernet stack for the first Device Group
	${result} =  Interface Config  protocol_name=Ethernet 1  protocol_handle=${deviceGroup_1_handle}  mtu=1500  src_mac_addr=18.03.73.c7.6c.b1  src_mac_addr_step=00.00.00.00.00.00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# Creating ethernet stack for the second Device Group
	Log To Console  Creating ethernet stack for the first Device Group
	${result} =  Interface Config  protocol_name=Ethernet 2  protocol_handle=${deviceGroup_2_handle}  mtu=1500  src_mac_addr=18.03.73.c7.6c.01  src_mac_addr_step=00.00.00.00.00.00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_2_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
	
# Creating IPv4 Stack on top of Ethernet Stack for the first Device Group
	Log To Console  Creating IPv4 Stack on top of Ethernet Stack for the first Device Group
	${result} =  Interface Config  protocol_name=IPv4 1  protocol_handle=${ethernet_1_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.1  gateway_step=0.0.0.0  intf_ip_addr=20.20.20.2  intf_ip_addr_step=0.0.0.0  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_1_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group 
	Log To Console  Creating IPv4 Stack on top of Ethernet Stack for the second Device Group 
	${result} =  Interface Config  protocol_name=IPv4 2  protocol_handle=${ethernet_2_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.2  gateway_step=0.0.0.0  intf_ip_addr=20.20.20.1  intf_ip_addr_step=0.0.0.0  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_2_handle} =  Get From Dictionary  ${result}  ipv4_handle

################################################################################
# Other protocol configurations                                                # 
################################################################################
# This will Create BGP Stack on top of IPv4 Stack of Topology1 & Topology2

	Log To Console  Creating BGP Stack on top of IPv4 1 stack on Topology 1 and enabling BGP_LS on it
	${result} =  Emulation Bgp Config  mode=enable  active=1  md5_enable=0  handle= ${ipv4_1_handle}  ip_version=4  remote_ip_addr=20.20.20.1  next_hop_enable=0  next_hop_ip=0.0.0.0  filter_link_state=1  capability_linkstate_nonvpn=1  bgp_ls_id=300  instance_id=400  number_of_communities=1  enable_community=0  community_type=no_export  community_as_number=0  community_last_two_octets=0  number_of_ext_communities=1  enable_ext_community=0  ext_communities_type=admin_as_two_octet  ext_communities_subtype=route_target  ext_community_as_number=1  ext_community_as_4_bytes=1  ext_community_ip=1.1.1.1  ext_community_opaque_data=0  enable_override_peer_as_set_mode=0  bgp_ls_as_set_mode=include_as_seq  number_of_as_path_segments=1  enable_as_path_segments=1  enable_as_path_segment=1  number_of_as_number_in_segment=1  as_path_segment_type=as_set  as_path_segment_enable_as_number=1  as_path_segment_as_number=1  number_of_clusters=1  enable_cluster=0  cluster_id=0.0.0.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${bgpInterface_1_handle} =  Get From Dictionary  ${result}  bgp_handle
	
	Log To Console  Creating BGP Stack on top of IPv4 1 stack on Topology 2 and enabling BGP_LS on it
	${result} =  Emulation Bgp Config  mode=enable  active=1  md5_enable=0  handle= ${ipv4_2_handle}  ip_version=4  remote_ip_addr=20.20.20.2  next_hop_enable=0  next_hop_ip=0.0.0.0  filter_link_state=1  capability_linkstate_nonvpn=1  bgp_ls_id=300  instance_id=400  number_of_communities=1  enable_community=0  community_type=no_export  community_as_number=0  community_last_two_octets=0  number_of_ext_communities=1  enable_ext_community=0  ext_communities_type=admin_as_two_octet  ext_communities_subtype=route_target  ext_community_as_number=1  ext_community_as_4_bytes=1  ext_community_ip=1.1.1.1  ext_community_opaque_data=0  enable_override_peer_as_set_mode=0  bgp_ls_as_set_mode=include_as_seq  number_of_as_path_segments=1  enable_as_path_segments=1  enable_as_path_segment=1  number_of_as_number_in_segment=1  as_path_segment_type=as_set  as_path_segment_enable_as_number=1  as_path_segment_as_number=1  number_of_clusters=1  enable_cluster=0  cluster_id=0.0.0.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${bgpInterface_2_handle} =  Get From Dictionary  ${result}  bgp_handle
	
	Log To Console  Creating OSPFv2 Stack on top of IPv4 1 stack on Topology 1
	${result} =  Emulation Ospf Config  handle=${ipv4_1_handle}  area_id=0.0.0.0  area_id_as_number=0  area_id_type=number  authentication_mode=null  dead_interval=40  hello_interval=10  router_interface_active=1  enable_fast_hello=0  hello_multiplier=2  max_mtu=1500  protocol_name=OSPFv2-IF 1  router_active=1  router_asbr=0  do_not_generate_router_lsa=0  router_abr=0  inter_flood_lsupdate_burst_gap=33  lsa_refresh_time=1800  lsa_retransmit_time=5  max_ls_updates_per_burst=1  oob_resync_breakout=0  interface_cost=10  lsa_discard_mode=1  md5_key_id=1  network_type=ptop  mode=create
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospfv2_1_handle} =  Get From Dictionary  ${result}  ospfv2_handle
	
	Log To Console  Creating OSPFv2 Stack on top of IPv4 1 stack on Topology 1
	${result} =  Emulation Ospf Config  handle=${ipv4_2_handle}  area_id=0.0.0.0  area_id_as_number=0  area_id_type=number  authentication_mode=null  dead_interval=40  hello_interval=10  router_interface_active=1  enable_fast_hello=0  hello_multiplier=2  max_mtu=1500  protocol_name=OSPFv2-IF 2  router_active=1  router_asbr=0  do_not_generate_router_lsa=0  router_abr=0  inter_flood_lsupdate_burst_gap=33  lsa_refresh_time=1800  lsa_retransmit_time=5  max_ls_updates_per_burst=1  oob_resync_breakout=0  interface_cost=10  lsa_discard_mode=1  md5_key_id=1  network_type=ptop  mode=create
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospfv2_2_handle} =  Get From Dictionary  ${result}  ospfv2_handle
	
	
############################################
## Network Group Config
############################################
	
	${result} =  Network Group Config  protocol_handle=${deviceGroup_2_handle}  protocol_name=Direct/Static Routes  multiplier=1  enable_device=1  connected_to_handle=${ethernet_2_handle}  type=ipv4-prefix  ipv4_prefix_network_address=200.1.0.0  ipv4_prefix_network_address_step=0.1.0.0  ipv4_prefix_length=24  ipv4_prefix_number_of_addresses=2
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_1_handle} =  Get From Dictionary  ${result}  network_group_handle
	
	${result} =  Network Group Config  protocol_handle=${deviceGroup_2_handle}  protocol_name=IPv6 Prefix NLRI  connected_to_handle=${ethernet_2_handle}  type=ipv6-prefix  multiplier=2  enable_device=1  ipv6_prefix_network_address=3000:0:1:1:0:0:0:0  ipv6_prefix_network_address_step=0:0:1:0:0:0:0:0  ipv6_prefix_length=64  ipv6_prefix_number_of_addresses=2
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_2_handle} =  Get From Dictionary  ${result}  network_group_handle
	
	${result} =  Network Group Config  protocol_handle=${deviceGroup_2_handle}  protocol_name=IPv4 Prefix NLRI  multiplier=2  enable_device=1  connected_to_handle=${ethernet_2_handle}  type=ipv4-prefix  ipv4_prefix_network_address=200.1.0.0  ipv4_prefix_network_address_step=0.1.0.0  ipv4_prefix_length=24  ipv4_prefix_number_of_addresses=2
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_3_handle} =  Get From Dictionary  ${result}  network_group_handle
	
	${result} =  Network Group Config  protocol_handle=${deviceGroup_2_handle}  protocol_name=Node/Link/Prefix NLRI  multiplier=1  enable_device=1  type=mesh  mesh_number_of_nodes=3  mesh_include_emulated_device=0  mesh_link_multiplier=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_4_handle} =  Get From Dictionary  ${result}  network_group_handle
	
	
############################################################################
# Start BGP protocol                                                       #
############################################################################ 
	Log To Console  Starting BGP on topology1
	${result} =  Emulation Ldp Control  handle=${bgpInterface_1_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	Log To Console  Starting LDP on topology2
	${result} =  Emulation Ospf Control  handle=${bgpInterface_2_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Test Control  action=start_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log To Console  Waiting for 30 seconds for all sessions to come up ...
	Sleep  30s
	
	
############################################################################
# OTF changing the valye of BGPLS ID & Instance ID                         #
############################################################################
	
	Log To Console  Changing BGPLS ID and Instance ID On The Fly
	${result} =  Emulation Bgp Config  mode=modify  active=1  md5_enable=0  handle=${bgpInterface_2_handle}  ip_version=4  bgp_ls_id=700  instance_id=800
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Applying changes one the fly                                                 #
################################################################################
	
	Log To Console  Applying changes on the fly
	${result} =  Test Control  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Waiting for 10 seconds
	Sleep  10s
	
################################################################################
# Retrieve protocol statistics                                                 #
################################################################################
	Log  printing protocol statistics ...
	${protostats} =  Emulation Bgp Info  handle=${bgpInterface_1_handle}  mode=stats_per_device_group  
	${status} =  Get From Dictionary  ${protostats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${protostats}
	
	

############################################################################
# Retrieve Learned Info                                                    #
############################################################################
	Log To Console  Fetching OSPFv2 learned info for Topology 1
	${learnedInfo} =  Emulation Bgp Info  handle=${bgpInterface_1_handle}  mode=learned_info
	${status} =  Get From Dictionary  ${learnedInfo}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${learnedInfo}

	
############################################################################
# Stop all protocols                                                       #
############################################################################

	Log  Stopping all protocols
	${result} =  Test Control  action=stop_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  2s
	Log  !!! Test Script Ends !!!