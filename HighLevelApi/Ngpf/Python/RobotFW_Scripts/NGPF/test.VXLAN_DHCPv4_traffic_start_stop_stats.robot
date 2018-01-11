*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.104/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.104/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
# Topology 2P-B2B-DC
*** Variables ***
${chassis} =  	10.215.132.206
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	3/07  3/10
${client_and_port} =  ${client}:${client_api_port}


*** Test Cases ***
test
################################################################################
# START - Connect to the chassis and get port handles from the result
################################################################################
	
	${result} =  Connect  reset=1  device=${chassis}  ixnetwork_tcl_server=${client_and_port}  port_list=@{portlist}  tcl_server=${chassis}  username=ixiaHLTQA  break_locks=1  interactive=1
	${connect_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${connect_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	

# #############################################################################
# 								VTEP 1 CONFIG
# #############################################################################

# CREATE TOPOLOGY 1

	Log  Configure VXLAN stack 1 ...
	${result} =  Topology Config  topology_name=Topology 1  port_handle=@{portHandles}[0]
	${topology_1_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${topology_1_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# CREATE DEVICE GROUP 1
	
	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name=VTEP 1  device_group_multiplier=3  device_group_enabled=1
	${device_group_1_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${device_group_1_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${device_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# CREATE ETHERNET STACK FOR VXLAN 1
	
	${result} =  Multivalue Config  pattern=counter  counter_start=00.11.01.00.00.01  counter_step=00.00.00.00.00.01  counter_direction=increment  nest_step=00.00.01.00.00.00  nest_owner=${topology_1_handle}  nest_enabled=1
	${multivalue_1_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${multivalue_1_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_1_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Interface Config  protocol_name=Ethernet 1  protocol_handle=${device_1_handle}  mtu=1500  src_mac_addr=${multivalue_1_handle}  vlan=1  vlan_id=101  vlan_id_step=1  vlan_id_count=1  vlan_tpid=0x8100  vlan_user_priority=0  vlan_user_priority_step=0  use_vpn_parameters=0  site_id=0
	${ethernet_1_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ethernet_1_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
	${result} =  Emulation Vxlan Config  mode=create  handle=${ethernet_1_handle}  intf_ip_addr=23.0.0.1  intf_ip_addr_step=0.0.0.1  ip_num_sessions=2  intf_ip_prefix_length=24  gateway=23.0.0.100  gateway_step=0.0.0.1  enable_resolve_gateway=1  vni=600  create_ig=0  ipv4_multicast=225.3.0.9  sessions_per_vxlan=1  ip_to_vxlan_multiplier=1
	${vxlan_1_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${vxlan_1_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vxlan_1_handle} =  Get From Dictionary  ${result}  vxlan_handle
	
# #############################################################################
# 								VTEP 2 CONFIG
# #############################################################################

# CREATE TOPOLOGY 2
	
	Log  Configure VXLAN stack 2 ...
	${result} =  Topology Config  topology_name=Topology 2  port_handle=@{portHandles}[1]
	${topology_2_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${topology_2_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# CREATE DEVICE GROUP 2
	
	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name=VTEP 2  device_group_multiplier=3  device_group_enabled=1
	${device_group_2_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${device_group_2_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${device_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# CREATE ETHERNET STACK FOR VXLAN 2
	
	${result} =  Multivalue Config  pattern=counter  counter_start=00.24.01.00.00.01  counter_step=00.00.00.00.00.01  counter_direction=increment  nest_step=00.00.01.00.00.00  nest_owner=${topology_2_handle}  nest_enabled=1
	${multivalue_2_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${multivalue_2_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_2_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Interface Config  protocol_name=Ethernet 2  protocol_handle=${device_2_handle}  mtu=1500  src_mac_addr=${multivalue_2_handle}  vlan=1  vlan_id=101  vlan_id_step=1  vlan_id_count=1  vlan_tpid=0x8100  vlan_user_priority=0  vlan_user_priority_step=0  use_vpn_parameters=0  site_id=0
	${ethernet_2_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ethernet_2_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_2_handle} =  Get From Dictionary  ${result}  ethernet_handle

# CREATE IPv4 STACK FOR VXLAN 2

	${result} =  Multivalue Config  pattern=counter  counter_start=23.0.0.100  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.1.0.0  nest_owner=${topology_1_handle}  nest_enabled=1
	${multivalue_2_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${multivalue_2_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_2_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=23.0.0.1  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.1.0.0  nest_owner=${topology_1_handle}  nest_enabled=1
	${gw_multivalue_1_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${gw_multivalue_1_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${gw_multivalue_1_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Interface Config  protocol_name=IPv4 2  protocol_handle=${ethernet_2_handle}  ipv4_resolve_gateway=1  gateway=${gw_multivalue_1_handle}  intf_ip_addr=${multivalue_2_handle}  netmask=255.255.255.0
	${ipv4_2_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ipv4_2_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_2_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
	${result} =  Emulation Vxlan Config  mode=create  handle=${ipv4_2_handle}  intf_ip_prefix_length=24  vni=600  create_ig=1  ipv4_multicast=225.3.0.9  ip_to_vxlan_multiplier=1  ig_intf_ip_addr=80.0.0.100  ig_intf_ip_addr_step=1.0.0.0  ig_intf_ip_prefix_length=16  ig_mac_address_init=00:67:22:33:00:00  ig_mac_address_step=00:00:00:00:00:11  ig_gateway=80.0.0.101  ig_gateway_step=1.0.0.0  ig_enable_resolve_gateway=0  sessions_per_vxlan=1
	${vxlan_2_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${vxlan_2_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${inner_ipv4_2_handle} =  Get From Dictionary  ${result}  ig_ipv4_handle
	${vxlan_2_handle} =  Get From Dictionary  ${result}  vxlan_handle
	
# #############################################################################
# 								 DHCPv4 SERVER
# #############################################################################
	
	${result} =  Multivalue Config  pattern=counter  counter_start=80.0.0.1  counter_step=1.0.0.0  counter_direction=increment  nest_step=1.0.0.0  nest_owner=${topology_2_handle}  nest_enabled=1
	${multivalue_pool} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${multivalue_pool}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_pool_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=16  counter_step=0  counter_direction=increment  nest_step=0  nest_owner=${topology_2_handle}  nest_enabled=1
	${multivalue_prefix} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${multivalue_prefix}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_prefix_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Emulation Dhcp Server Config  mode=create  handle=${inner_ipv4_2_handle}  lease_time=84600  ipaddress_count=100  ipaddress_pool=${multivalue_pool_handle}  ipaddress_pool_prefix_length=${multivalue_prefix_handle}  ip_version=4
	${dhcp_server_config_status1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_server_config_status1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_server_handle} =  Get From Dictionary  ${result}  dhcpv4server_handle
	
# #############################################################################
# 								 DHCPv4 CLIENT
# #############################################################################
	
	${result} =  Topology Config  device_group_multiplier=5  device_group_handle=${device_1_handle}
	${device_group_chained_status_1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${device_group_chained_status_1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${chained_dg_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
	${result} =  Emulation Dhcp Group Config  handle=${chained_dg_1_handle}  dhcp_range_ip_type=ipv4  dhcp_range_renew_timer=2000  use_rapid_commit=0  dhcp_range_server_address=80.0.0.100  dhcp4_gateway_address=80.0.0.100
	${dhcp_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dhcp_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_client_handle} =  Get From Dictionary  ${result}  dhcpv4client_handle
	
# #############################################################################
# 								START PROTOCOLS
# #############################################################################
	
	Log  Start VXLAN ...
	
	${result} =  Emulation Vxlan Control  handle=${vxlan_1_handle}  action=start
	${control_status_1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status_1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Vxlan Control  handle=${vxlan_2_handle}  action=start
	${control_status_2} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status_2}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Start DHCP server...
	
	${result} =  Emulation Dhcp Server Control  dhcp_handle=${dhcp_server_handle}  action=collect
	${control_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Start DHCP clients...
	
	${result} =  Emulation Dhcp Control  handle=${dhcp_client_handle}  action=bind
	${control_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  80s
	
# #############################################################################
# 								STATISTICS
# #############################################################################
# CLIENT
	${vxlan_stats_2} =  Emulation Vxlan Stats  port_handle=@{portHandles}[0]  mode=aggregate_stats  execution_timeout=30
	${status} =  Get From Dictionary  ${vxlan_stats_2}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${dhcp_client_stats} =  Emulation Dhcp Stats  port_handle=@{portHandles}[0]  mode=aggregate_stats  execution_timeout=30
	${status} =  Get From Dictionary  ${dhcp_client_stats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
# SERVER
	${vxlan_stats_1} =  Emulation Vxlan Stats  port_handle=@{portHandles}[1]  mode=aggregate_stats  execution_timeout=30
	${status} =  Get From Dictionary  ${vxlan_stats_1}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${dhcp_server_stats} =  Emulation Dhcp Server Stats  port_handle=@{portHandles}[1]  action=collect  execution_timeout=30
	${status} =  Get From Dictionary  ${dhcp_server_stats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  3s
	Log  VXLAN aggregate stats port 1:
	Log  ${vxlan_stats_2}
	
	Log  VXLAN aggregate stats port 2:
	Log  ${vxlan_stats_1}
	
	Log  DHCP Client aggregate stats:
	Log  ${dhcp_client_stats}
	
	Log  DHCP Server aggregate stats:
	Log  ${dhcp_server_stats}
	Log  ${dhcp_client_stats['aggregate']['success_percentage']}
	${success_percentage} =  Set Variable  ${dhcp_client_stats['@{portHandles}[0]']['aggregate']['success_percentage']}
	Run Keyword If  '${success_percentage}' != '100'  FAIL  "Error: Not all DHCP sessions are up!"  ELSE  Log  "All DHCP sessions are up!"
	Log  ${dhcp_server_stats['aggregate']['@{portHandles}[1]']['sessions_up']}
	${sessions_up} =  Set Variable  ${dhcp_server_stats['aggregate']['@{portHandles}[1]']['sessions_up']}
	Run Keyword If  '${sessions_up}' != '3'  FAIL  "Error: Not all DHCP Server sessions are up!"  ELSE  Log  "All DHCP Server sessions are up!"
	
	
	Sleep  5s
# #############################################################################
# 								TRAFFIC CONFIG
# #############################################################################

	Log  Configuring traffic between DHCP Clients and IPv4...
	${result} =  Traffic Config  traffic_generator=ixnetwork_540  mode=create  circuit_endpoint_type=ipv4  bidirectional=0  track_by=source_ip  name=IPv4_TRAFFIC  emulation_src_handle=${dhcp_client_handle}  emulation_dst_handle=${inner_ipv4_2_handle}  src_dest_mesh=one_to_one  route_mesh=one_to_one  rate_percent=10  frame_size=512
	${traffic_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${traffic_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	Sleep  5s

# #############################################################################
# 								TRAFFIC CONTROL
# #############################################################################

	Log  Starting traffic...
	${result} =  Traffic Control  action=run  traffic_generator=ixnetwork_540
	${traffic_control_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${traffic_control_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  20s
	
# #############################################################################
# 								TRAFFIC STATS
# #############################################################################
	
	Log  Collecting traffic stats...
	${result} =  Traffic Stats  mode=flow  traffic_generator=ixnetwork_540
	${traffic_stats} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${traffic_stats}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  IPv4 traffic flow stats: ${result}
	
	${result} =  Traffic Stats  mode=traffic_item  traffic_generator=ixnetwork_540
	${traffic_stats} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${traffic_stats}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  IPv4 traffic item stats: ${result}
	
	${result} =  Traffic Stats  mode=l23_test_summary  traffic_generator=ixnetwork_540
	${traffic_stats} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${traffic_stats}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  IPv4 traffic L23 Summary stats: ${result}
	
# #############################################################################
# 								STOP TRAFFIC
# #############################################################################

	Log  Stopping traffic...
	${result} =  Traffic Control  action=stop  traffic_generator=ixnetwork_540
	${traffic_control_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${traffic_control_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	Sleep  10s
	
# #############################################################################
# 								STOP PROTOCOLS
# #############################################################################

	Log  Stop VXLAN ...
	${result} =  Emulation Vxlan Control  handle=${vxlan_1_handle}  action=stop
	${control_status_1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status_1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Vxlan Control  handle=${vxlan_2_handle}  action=stop
	${control_status_2} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${control_status_2}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
# #############################################################################
# 								CLEANUP SESSION
# #############################################################################
	















