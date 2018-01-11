*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.232
${client_api_port} =  	8136
@{portlist} =  	12/1  12/2
${client_and_port} =  ${client}:${client_api_port}


*** Test Cases ***
test
################################################################################
# START - Connect to the chassis and get port handles from the result
################################################################################
	
	${result} =  Connect  device=${chassis}  ixnetwork_tcl_server=${client_and_port}  port_list=@{portlist}  reset=1  tcl_server=${chassis}  username=ixiaHLTQA
	${connect_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${connect_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	Log Many  @{portHandles}


################################################################################
# Configure interface in the test
################################################################################

	${result} =  Interface Config  port_handle=@{portHandles}  autonegotiation=0  duplex=full  speed=ether1000
	${interface_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Config L2 L3 interface1
################################################################################

	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[0]  l23_config_type=protocol_interface  arp_on_linkup=1  single_arp_per_gateway=1  mtu=1500  src_mac_addr=0000.0f68.fc04  vlan=0  intf_ip_addr=1.1.1.1  gateway=1.1.1.2  netmask=255.255.255.0
	${interface_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${interface_handle1} =  Get From Dictionary  ${result}  interface_handle
	
################################################################################
# Config L2 L3 interface2
################################################################################

	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[1]  l23_config_type=protocol_interface  arp_on_linkup=1  single_arp_per_gateway=1  mtu=1500  src_mac_addr=0000.0f68.fc05  vlan=0  intf_ip_addr=1.1.1.2  gateway=1.1.1.1  netmask=255.255.255.0
	${interface_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${interface_handle2} =  Get From Dictionary  ${result}  interface_handle
	
################################################################################
# Configure count OSPFv2 neighbors on port_0 with the same info anc check if configured 
################################################################################
	${result} =  Emulation Ospf Config  mode=create  reset=1  port_handle=@{portHandles}[0]  session_type=ospfv2  count=10  mac_address_init=1000.0000.0001  mac_address_step=0000.0000.0000  router_id=1.1.1.2  router_id_step=0.0.0.0  intf_ip_addr=10.10.10.11  intf_ip_addr_step=0.0.0.0  area_id=0.0.0.2  area_id_step=0.0.0.0  lsa_discard_mode=0  network_type=ptop  area_type=external-capable  enable_dr_bdr=1  override_existence_check=1  override_tracking=1  option_bits=0x48
	
	${ospf_neighbor_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ospf_neighbor_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospf_interface_handle10} =  Get From Dictionary  ${result}  handle
	${ospf_interface_handle10} =  Split String    ${ospf_interface_handle10}
	Sleep  10s
################################################################################
# Check for override existing  and delete count neigbors
################################################################################
	Ixnet  connect  ${client}  -port  ${client_api_port}  -version  8.20
	${root} =  Ixnet  getRoot
	${vports} =  Ixnet  getList  ${root}  vport
	${vport1} =  Get From List  ${vports}  0
	${interfaces} =  Ixnet  getList  ${vport1}  interface
	${interfaces_count} =  Get Length  ${interfaces}
	${ospf_interface_handle10_count} =  Get Length  ${ospf_interface_handle10}


	Run Keyword If  ${interfaces_count} != 11  FAIL  "Number of interfaces configured in IxN using override is incorrect"  ELSE  Log  "Number of interfaces configured in IxN using override is correct"
	Log Many  ${ospf_interface_handle10_count}
	Run Keyword If  ${ospf_interface_handle10_count} != 10  FAIL  "Number of interfaces from HLT handle using override is incorrect"  ELSE  Log  "Number of interfaces from HLT handle using override is correct"


	${result} =  Emulation Ospf Config  port_handle=@{portHandles}[0]  reset=1  session_type=ospfv2  mode=delete  handle=${ospf_interface_handle10}
	
	${ospf_neighbor_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ospf_neighbor_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Interface Config  mode=destroy  port_handle=@{portHandles}[0]
	${interface_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	#Config interface1 again

	${result} =  Interface Config  mode=modify  port_handle=@{portHandles}[0]  l23_config_type=protocol_interface  arp_on_linkup=1  single_arp_per_gateway=1  mtu=1500  src_mac_addr=0000.0f68.fc04  vlan=0  intf_ip_addr=1.1.1.1  gateway=1.1.1.2  netmask=255.255.255.0
	${interface_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${interface_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${interface_handle1} =  Get From Dictionary  ${result}  interface_handle
	
	#  Configure 1 OSPFv2 neighbors on port_0
	
	${result} =  Emulation Ospf Config  mode=create  reset=1  port_handle=@{portHandles}[0]  session_type=ospfv2  mac_address_init=1000.0000.0001  router_id=1.1.1.1  interface_handle=${interface_handle1}  area_id=0.0.0.1  lsa_discard_mode=0  network_type=ptop  area_type=external-capable  enable_dr_bdr=1  option_bits=0x48
	
	${ospf_neighbor_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ospf_neighbor_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospf_handle_list} =  Get From Dictionary  ${result}  handle
	@{ospf_handle_list} =  Split String  ${ospf_handle_list}
	
	${result} =  Emulation Ospf Lsa Config  mode=create  handle=@{ospf_handle_list}  type=opaque_type_10  adv_router_id=101.0.0.1  link_state_id=202.0.0.1  options=255  router_abr=1  router_asbr=1  router_virtual_link_endpt=0  router_link_mode=create  router_link_id=22.0.0.1  router_link_data=33.0.0.1  router_link_type=stub  router_link_metric=100  area_id=50.1.1.1  ls_type_function_code=666  no_write=0  router_wildcard=1  opaque_enable_link_id=1  opaque_enable_link_local_ip_addr=1  opaque_enable_link_max_bw=1  opaque_enable_link_max_resv_bw=1  opaque_enable_link_metric=1  opaque_enable_link_remote_ip_addr=1  opaque_enable_link_resource_class=1  opaque_enable_link_type=1  opaque_enable_link_unresv_bw=1  opaque_link_id=5.5.5.5  opaque_link_local_ip_addr=7.7.7.7  opaque_link_max_bw=100  opaque_link_max_resv_bw=200  opaque_link_metric=300000  opaque_link_remote_ip_addr=9.9.9.9  opaque_link_resource_class=0x00000042  opaque_link_type=multiaccess  opaque_link_unresv_bw_priority=100000  opaque_tlv_type=link

	${ospf_lsa_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ospf_lsa_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${opaque_lsa_handle_list} =  Get From Dictionary  ${result}  lsa_handle
	@{opaque_lsa_handle_list} =  Split String  ${opaque_lsa_handle_list}
#                                               #
#  Create Topology Route - Router on port_0     #
#                                               #

	${result} =  Emulation Ospf Topology Route Config  mode=create  handle=@{ospf_handle_list}  type=summary_routes  link_type=stub  summary_ip_type=ipv4  summary_address_family=multicast  summary_route_type=same_area  summary_prefix_start=11.1.1.1  summary_prefix_length=21  summary_number_of_prefix=5

	${route_config_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${route_config_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

#                                               #
#  Configure 1 OSPFv2 neighbors on port_1       #
#                                               #
	Log Many  here fails
	${result} =  Emulation Ospf Config  port_handle=@{portHandles}[1]  reset=1  session_type=ospfv2  mode=create  mac_address_init=2000.0000.0001  interface_handle=${interface_handle2}  area_id=0.0.0.1  router_id=2.2.2.2  lsa_discard_mode=0  network_type=ptop  area_type=external-capable  option_bits=0x48
	${ospf_neighbor_status2} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ospf_neighbor_status2}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospf_handle_list2} =  Get From Dictionary  ${result}  handle
	@{ospf_handle_list2} =  Split String  ${ospf_handle_list2}
#                                               #
#  Create Opaque LSA                            #
#                                               #

	${result} =  Emulation Ospf Lsa Config  mode=create  handle=@{ospf_handle_list2}  type=opaque_type_10  opaque_tlv_type=router  opaque_router_addr=192.168.1.1  adv_router_id=101.0.0.2  link_state_id=202.0.0.2  options=255
	${ospf_lsa_status2} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ospf_lsa_status2}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${opaque_lsa_handle_list2} =  Get From Dictionary  ${result}  lsa_handle
	@{opaque_lsa_handle_list2} =  Split String  ${opaque_lsa_handle_list2}

#                                               #
#  Create Topology Route - Router on port_1     #
#                                               #

	${result} =  Emulation Ospf Topology Route Config  mode=create  handle=@{ospf_handle_list2}  type=summary_routes  link_type=stub  summary_ip_type=ipv4  summary_address_family=multicast  summary_route_type=same_area  summary_prefix_start=12.1.1.1  summary_prefix_length=21  summary_number_of_prefix=5
	${route_config_status2} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${route_config_status2}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"


#                                               #
#		Start OSPF protocol on ports			#
#                                               #

	${result} =  Emulation Ospf Control  port_handle=@{portHandles}  mode=start
	${ospf_emulation_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ospf_emulation_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	Sleep  20s

#                                               #
#		Stop OSPF protocol on ports				#
#                                               #

	${result} =  Emulation Ospf Control  port_handle=@{portHandles}  mode=stop
	${ospf_emulation_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ospf_emulation_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	Sleep  20s

#                                               #
#		Restart OSPF protocol on ports			#
#                                               #

	${result} =  Emulation Ospf Control  port_handle=@{portHandles}  mode=restart
	${ospf_emulation_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ospf_emulation_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  20s
	

#                                               #
#		Get OSPF learned information on port1   #
#                                               #

	Log Many  "############### Learned Info statistics ##################"

	:FOR	${port}	IN	@{portHandles}
	\	${ospf_emulation_status2} =  Emulation Ospf Info  port_handle=${port}  mode=learned_info
	\	${status} =  Get From Dictionary  ${ospf_emulation_status2}  status
	\	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	\	@{router_keys} =  Get Dictionary Keys  ${ospf_emulation_status2}
		:FOR	${router_handle}	IN	@{router_keys}[0]
		\	@{intf_keys} =  Get From Dictionary  ${ospf_emulation_status2}  ${router_handle}
			:FOR	${interface_handle}	IN	@{intf_keys}
			\	@{session_keys} =  Set Variable  ${ospf_emulation_status2['${router_handle}']['${interface_handle}']['session']}
				:FOR	${session_no}	IN	@{session_keys}
				\	Log  Learned info for session number ${session_no}
				\	Log  {ospf_emulation_status2['${router_handle}']['${interface_handle}']['session']['${session_no}']['adv_router_id']}
				\	Log  {ospf_emulation_status2['${router_handle}']['${interface_handle}']['session']['${session_no}']['age']}
				\	Log  {ospf_emulation_status2['${router_handle}']['${interface_handle}']['session']['${session_no}']['link_state_id']}
				\	Log  {ospf_emulation_status2['${router_handle}']['${interface_handle}']['session']['${session_no}']['lsa_type']}
				\	Log  {ospf_emulation_status2['${router_handle}']['${interface_handle}']['session']['${session_no}']['seq_number']}

#                                               #
#		Get OSPF aggregated statistics			#
#                                               #

	${result} =  Emulation Ospf Info  port_handle=@{portHandles}  mode=aggregate_stats
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  "############### Aggregated statistics ##################"
	Log  Sessions configured: ${result['@{portHandles}[0]']['aggregate']['sessions_configured']}
	Log  Full neighbors: ${result['@{portHandles}[0]']['aggregate']['full_neighbors']}
	Log  Session flap count: ${result['@{portHandles}[0]']['aggregate']['session_flap_count']}
	Log  Neighbor down count: ${result['@{portHandles}[0]']['aggregate']['neighbor_down_count']}
	Log  Neighbor attempt count: ${result['@{portHandles}[0]']['aggregate']['neighbor_attempt_count']}
	Log  Neighbor init count: ${result['@{portHandles}[0]']['aggregate']['neighbor_init_count']}
	Log  Neighbor 2way count: ${result['@{portHandles}[0]']['aggregate']['neighbor_2way_count']}
	Log  Neighbor exstart count: ${result['@{portHandles}[0]']['aggregate']['neighbor_exstart_count']}
	Log  Neighbor exchange count: ${result['@{portHandles}[0]']['aggregate']['neighbor_exchange_count']}
	Log  Neighbor loading count: ${result['@{portHandles}[0]']['aggregate']['neighbor_loading_count']}
	Log  Neighbor full count: ${result['@{portHandles}[0]']['aggregate']['neighbor_full_count']}
	
#                                               #
#		Checking OSPF aggregated statistics		#
#                                               #
	
	Log  "############# Check Aggregated statistics ################"
	Run Keyword If  '${result['@{portHandles}[0]']['aggregate']['sessions_configured']}' != '1'  FAIL  "Number of sessions configured incorrect"  ELSE  Log  "Number of session configured is correct"
	
	Run Keyword If  '${result['@{portHandles}[0]']['aggregate']['full_neighbors']}' != '1'  FAIL  "Number of full neighbours incorrect"  ELSE  Log  "Number of full neighbours is correct"
	
	Run Keyword If  '${result['@{portHandles}[0]']['aggregate']['neighbor_full_count']}' != '1'  FAIL  "Number of full neighbours incorrect"  ELSE  Log  "Number of full neighbours is correct"
	
#                                               #
#		Clear OSPF statistics					#
#                                               #
	${result} =  Emulation Ospf Info  port_handle=@{portHandles}  mode=clear_stats
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#                                               #
#  Delete and create LSA 1                      #
#                                               #
	
	:FOR	${ospf_handle}	IN	@{ospf_handle_list}
	\	${ospf_lsa_status} =  Emulation Ospf Lsa Config  mode=delete  handle=${ospf_handle}  lsa_handle=@{opaque_lsa_handle_list}[0]
	\	${status} =  Get From Dictionary  ${ospf_lsa_status}  status
	\	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	@{opaque_lsa_handle_list3} =  Create List
	:FOR	${ospf_handle}	IN	@{ospf_handle_list}
	\	${ospf_lsa_status} =  Emulation Ospf Lsa Config  mode=create  handle=${ospf_handle}  type=ext_pool  adv_router_id=101.0.0.4  link_state_id=202.0.0.4  options=5  external_number_of_prefix=10  external_prefix_start=fec0:0:0:5::100  external_prefix_length=10  external_prefix_metric=4  external_prefix_step=0.0.0.1  external_prefix_type=1  external_prefix_forward_addr=fec0:0:0:5::1  external_route_tag=10.10.10.10  external_metric_ebit=1  external_metric_fbit=0  external_metric_tbit=0
	\	${status} =  Get From Dictionary  ${ospf_lsa_status}  status
	\	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS
	\	${lsa_handle} =  Get From Dictionary  ${ospf_lsa_status}  lsa_handle
	\	Append To List  @{opaque_lsa_handle_list3}  ${lsa_handle}

#                                               #
#  Delete and create LSA 2                      #
#                                               #

	:FOR	${ospf_handle}	IN	@{ospf_handle_list}
	\	${ospf_lsa_status} =  Emulation Ospf Lsa Config  mode=delete  handle=${ospf_handle}  lsa_handle=@{opaque_lsa_handle_list2}[0]
	\	${status} =  Get From Dictionary  ${ospf_lsa_status}  status
	\	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	@{opaque_lsa_handle_list4} =  Create List
	:FOR	${ospf_handle}	IN	@{ospf_handle_list}
	\	${ospf_lsa_status} =  Emulation Ospf Lsa Config  mode=create  handle=${ospf_handle}  type=router  adv_router_id=101.0.0.1  link_state_id=202.0.0.1  link_state_id_step=0.0.0.1  options=225  router_abr=1  router_asbr=1  router_virtual_link_endpt=0  router_link_mode=create  router_link_id=0.0.0.10  router_link_data=33.0.0.1  router_link_type=stub  router_link_metric=100  router_wildcard=1
	\	${status} =  Get From Dictionary  ${ospf_lsa_status}  status
	\	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS
	\	${lsa_handle} =  Get From Dictionary  ${ospf_lsa_status}  lsa_handle
	\	Append To List  @{opaque_lsa_handle_list4}  ${lsa_handle}

#                                               #
#		Stop OSPF protocol on ports				#
#                                               #

	${result} =  Emulation Ospf Control  port_handle=@{portHandles}  mode=stop
	${status} =  Get From Dictionary  ${ospf_lsa_status}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS