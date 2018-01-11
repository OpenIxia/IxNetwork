*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.147/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.147/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.191
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	11/1  11/2
${client_and_port} =  ${client}:${client_api_port}
${file_param}=  /home/pythar/ROBOT/protocols\ test\ cases/file_params.csv

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

##########################
# Configure first topology
##########################

	${result} =  Topology Config  topology_name={Topology 1}  port_handle=@{portHandles}[0]
	${top_1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${top_1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle

#### Configure first DG

	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name={Device Group 1}  device_group_multiplier=10  device_group_enabled=1
	${dg_1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dg_1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle

#### Configure Multivalue

	${result} =  Multivalue Config  pattern=value_list  values_file=${file_param}  values_file_type=csv  values_file_column_index=1  nest_owner=${topology_1_handle}  nest_enabled=1
	${mv1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_1_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=custom  nest_owner=${topology_1_handle}  nest_step=1  nest_enabled=0
	${mv2} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv2}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_2_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  multivalue_handle=${multivalue_2_handle}  custom_start=1  custom_step=1
	${mv3} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv3}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${custom_1_handle} =  Get From Dictionary  ${result}  custom_handle
	
	${result} =  Multivalue Config  custom_handle=${custom_1_handle}  custom_increment_value=0  custom_increment_count=3
	${mv4} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv4}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${increment_1_handle} =  Get From Dictionary  ${result}  increment_handle
	
	${result} =  Multivalue Config  pattern=value_list  values_file=${file_param}  values_file_type=csv  values_file_column_index=0  nest_owner=${topology_1_handle}  nest_enabled=1
	${mv_mtu} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv_mtu}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${mtu_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Interface Config  protocol_name={Ethernet 1}  protocol_handle=${deviceGroup_1_handle}  mtu=${mtu_handle}  src_mac_addr=${multivalue_1_handle}  vlan=1  vlan_id=${multivalue_2_handle}  vlan_id_step=0  vlan_id_count=1  vlan_tpid=0x8100  vlan_user_priority=0  vlan_user_priority_step=0  use_vpn_parameters=0  site_id=0
	${intf1} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${intf1}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
	${result} =  Multivalue Config  pattern=custom  nest_step=0.1.0.0  nest_owner=${topology_1_handle}  nest_enabled=1
	${mv5} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv5}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_3_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  multivalue_handle=${multivalue_3_handle}  custom_start=100.1.0.2  custom_step=0.0.1.0
	${mv6} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv6}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${custom_2_handle} =  Get From Dictionary  ${result}  custom_handle
	
	${result} =  Multivalue Config  custom_handle=${custom_2_handle}  custom_increment_value=0.0.0.1  custom_increment_count=3
	${mv7} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv7}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${increment_2_handle} =  Get From Dictionary  ${result}  increment_handle
	
	${result} =  Multivalue Config  pattern=custom  nest_step=0.0.0.1  nest_owner=${topology_1_handle}  nest_enabled=0  overlay_value=100.1.3.1  overlay_value_step=100.1.3.1  overlay_index=10  overlay_index_step=0  overlay_count=1
	${mv8} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv8}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_4_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  multivalue_handle=${multivalue_4_handle}  custom_start=100.1.0.5  custom_step=0.0.1.0
	${mv9} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv9}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${custom_3_handle} =  Get From Dictionary  ${result}  custom_handle
	
	${result} =  Multivalue Config  custom_handle=${custom_3_handle}  custom_increment_value=0.0.0.0  custom_increment_count=3
	${mv10} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv10}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${increment_3_handle} =  Get From Dictionary  ${result}  increment_handle
	
	${result} =  Interface Config  protocol_name={IPv4 1}  protocol_handle=${ethernet_1_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.02.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=${multivalue_4_handle}  intf_ip_addr=${multivalue_3_handle}  netmask=255.255.255.0
	${intf2} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${intf2}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_1_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
############################
# Configure second topology
############################
	
	${result} =  Topology Config  topology_name={Topology 2}  port_handle=@{portHandles}[1]
	${top_2} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${top_2}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle

#### Configure Second DG

	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name={Device Group 2}  device_group_multiplier=10  device_group_enabled=1
	${dg_2} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${dg_2}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_handle} =  Get From Dictionary  ${result}  device_group_handle

#### Configure Multivalue
	
	${result} =  Multivalue Config  pattern=counter  counter_start=00.12.01.00.00.01  counter_step=00.00.00.00.00.01  counter_direction=increment  nest_step=00.00.01.00.00.00  nest_owner=${topology_2_handle}  nest_enabled=1
	${mv11} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv11}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_5_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=custom  nest_step=1  nest_owner=${topology_2_handle}  nest_enabled=0
	${mv12} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv12}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_6_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  multivalue_handle=${multivalue_6_handle}  custom_start=1  custom_step=1
	${mv13} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv13}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${custom_4_handle} =  Get From Dictionary  ${result}  custom_handle
	
	${result} =  Multivalue Config  custom_handle=${custom_4_handle}  custom_increment_value=0  custom_increment_count=3
	${mv14} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv14}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${increment_4_handle} =  Get From Dictionary  ${result}  increment_handle
	
	${result} =  Interface Config  protocol_name={Ethernet 2}  protocol_handle=${deviceGroup_2_handle}  mtu=1500  src_mac_addr=${multivalue_5_handle}  vlan=1  vlan_id=${multivalue_6_handle}  vlan_id_step=0  vlan_id_count=1  vlan_tpid=0x8100  vlan_user_priority=0  vlan_user_priority_step=0  use_vpn_parameters=0  site_id=0
	${intf3} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${intf3}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_2_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
	${result} =  Multivalue Config  pattern=custom  nest_step=0.0.0.1  nest_owner=${topology_2_handle}  nest_enabled=1  overlay_value=100.1.3.1  overlay_value_step=100.1.3.1  overlay_index=10  overlay_index_step=0  overlay_count=1
	${mv15} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv15}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_7_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  multivalue_handle=${multivalue_7_handle}  custom_start=100.1.0.5  custom_step=0.0.1.0
	${mv16} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv16}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${custom_5_handle} =  Get From Dictionary  ${result}  custom_handle
	
	${result} =  Multivalue Config  custom_handle=${custom_5_handle}  custom_increment_value=0.0.0.1  custom_increment_count=3
	${mv17} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv17}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${increment_5_handle} =  Get From Dictionary  ${result}  increment_handle
	
	${result} =  Multivalue Config  pattern=custom  nest_step=0.1.0.0  nest_owner=${topology_2_handle}  nest_enabled=1
	${mv18} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv18}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_8_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	
	${result} =  Multivalue Config  multivalue_handle=${multivalue_8_handle}  custom_start=100.1.0.2  custom_step=0.0.1.0
	${mv19} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv19}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${custom_6_handle} =  Get From Dictionary  ${result}  custom_handle
	
	${result} =  Multivalue Config  custom_handle=${custom_6_handle}  custom_increment_value=0.0.0.0  custom_increment_count=3
	${mv20} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${mv20}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${increment_6_handle} =  Get From Dictionary  ${result}  increment_handle
	
	${result} =  Interface Config  protocol_name={IPv4 2}  protocol_handle=${ethernet_2_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.01.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=${multivalue_8_handle}  intf_ip_addr=${multivalue_7_handle}  netmask=255.255.255.0
	${intf4} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${intf4}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_2_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
	
	${result} =  Interface Config  protocol_handle=/globals  arp_on_linkup=0  single_arp_per_gateway=1  ipv4_send_arp_rate=200  ipv4_send_arp_interval=1000  ipv4_send_arp_max_outstanding=400  ipv4_send_arp_scale_mode=port  ipv4_attempt_enabled=0  ipv4_attempt_rate=200  ipv4_attempt_interval=1000  ipv4_attempt_scale_mode=port  ipv4_diconnect_enabled=0  ipv4_disconnect_rate=200  ipv4_disconnect_interval=1000  ipv4_disconnect_scale_mode=port  ipv4_re_send_arp_on_link_up=true
	${intf5} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${intf5}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	${result} =  Interface Config  protocol_handle=/globals  ethernet_attempt_enabled=0  ethernet_attempt_rate=200  ethernet_attempt_interval=1000  ethernet_attempt_scale_mode=port  ethernet_diconnect_enabled=0  ethernet_disconnect_rate=200  ethernet_disconnect_interval=1000  ethernet_disconnect_scale_mode=port
	${intf6} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${intf6}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
#######Starting protocols
	Log  Starting all protocols
	${result} =  Test Control  action=start_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	Log  Sleep for 30 seconds
	Sleep  30s
#######Stopping protocols
	Log  Stopping all protocols
	${result} =  Test Control  action=stop_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#######Gather and print ethernet and ipv4 protocol_info stats (mode = aggregate) ... 
	Log  Gather and print ethernet and ipv4 protocol_info stats (mode = aggregate) ... 
#######Ethernet Info
	Log  Gather Ethernet Info
	
	${result} =  Protocol Info  handle=${ethernet_1_handle}  mode=aggregate
	${eth_1_info} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${eth_1_info}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  Ethernet info (port 0) ... 
	Log  ${result}
	
	${result} =  Protocol Info  handle=${ethernet_1_handle}  mode=aggregate
	${eth_2_info} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${eth_2_info}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  Ethernet info (port 1) ... 
	Log  ${result}
	
#######IPv4 Info
	Log  Gather IPv4 Info
	
	${result} =  Protocol Info  handle=${ipv4_1_handle}  mode=aggregate
	${ipv4_1_info} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ipv4_1_info}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  IPv4 info (port 0) ... 
	Log  ${result}
	
	${result} =  Protocol Info  handle=${ipv4_2_handle}  mode=aggregate
	${ipv4_2_info} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ipv4_2_info}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  IPv4 info (port 1) ... 
	Log  ${result}
	
#######Gather and print ethernet and ipv4 protocol_info stats (mode = handles) ...
	Log  Gather and print ethernet and ipv4 protocol_info stats (mode = handles) ...
#######Ethernet Info
	Log  Gather Ethernet Info
	
	${result} =  Protocol Info  handle=${ethernet_1_handle}  mode=handles
	${eth_3_info} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${eth_3_info}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  Ethernet info (port 0) ... 
	Log  ${result}
	
	${result} =  Protocol Info  handle=${ethernet_2_handle}  mode=handles
	${eth_4_info} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${eth_4_info}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  Ethernet info (port 0) ... 
	Log  ${result}
	
#######IPv4 Info
	Log  Gather IPv4 Info
	
	${result} =  Protocol Info  handle=${ipv4_1_handle}  mode=handles
	${ipv4_3_info} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ipv4_1_info}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  IPv4 info (port 0) ... 
	Log  ${result}
	
	${result} =  Protocol Info  handle=${ipv4_2_handle}  mode=handles
	${ipv4_4_info} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ipv4_2_info}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  IPv4 info (port 1) ... 
	Log  ${result}
	
	Log  Script ended SUCCESSFULLY!
	
	
	
	
	
	
	
	
	
	
	
	