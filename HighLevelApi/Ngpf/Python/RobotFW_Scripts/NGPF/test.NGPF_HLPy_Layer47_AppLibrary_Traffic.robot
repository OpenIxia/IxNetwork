*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.147/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.147/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
# Topology 4P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	12/7  12/8  12/9  12/10
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
# Configure Topology 1, Device Group 1                                         #
################################################################################


	Log To Console  Adding topology 1 on port 1
	${result} =  Topology Config  topology_name=Topology 1  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 1 in topology 1
	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name=Device Group 1  device_group_multiplier=45  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
################################################################################
# Configure protocol interfaces for first topology                             #
################################################################################
	
	${result} =  Multivalue Config  pattern=counter  counter_start=00.11.01.00.00.01  counter_step=00.00.00.00.00.01  counter_direction=increment  nest_step=00.00.01.00.00.00  nest_owner=${topology_1_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_1_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	Log To Console  Creating ethernet stack for the first Device Group
	${result} =  Interface Config  protocol_name=Ethernet 1  protocol_handle=${deviceGroup_1_handle}  mtu=1500  src_mac_addr=${multivalue_1_handle}  vlan=0  vlan_id=1  vlan_id_step=0  vlan_id_count=1  vlan_tpid=0x8100  vlan_user_priority=0  vlan_user_priority_step=0  use_vpn_parameters=0  site_id=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=100.1.0.1  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.1.0.0  nest_owner=${topology_1_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_2_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=101.1.0.1  counter_step=255.255.255.255  counter_direction=decrement  nest_step=0.0.0.1  nest_owner=${topology_1_handle}  nest_enabled=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_3_handle} =  Get From Dictionary  ${result}  multivalue_handle
	

	${result} =  Interface Config  protocol_name=IPv4 1  protocol_handle=${ethernet_1_handle}  mtu=1500  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  gateway=${multivalue_3_handle}  intf_ip_addr=${multivalue_2_handle}  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_1_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
################################################################################
# Configure Topology 2, Device Group 2                                         #
################################################################################
	
	Log To Console  Adding topology 2 on port 2
	${result} =  Topology Config  topology_name=Topology 2  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 2 in topology 2
	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name=Device Group 2  device_group_multiplier=45  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	
################################################################################
# Configure protocol interfaces for second topology                             #
################################################################################
	
	${result} =  Multivalue Config  pattern=counter  counter_start=00.12.01.00.00.01  counter_step=00.00.00.00.00.01  counter_direction=increment  nest_step=00.00.01.00.00.00  nest_owner=${topology_2_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_4_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	Log To Console  Creating ethernet stack for the second Device Group
	${result} =  Interface Config  protocol_name=Ethernet 2  protocol_handle=${deviceGroup_2_handle}  mtu=1500  src_mac_addr=${multivalue_4_handle}  vlan=0  vlan_id=1  vlan_id_step=0  vlan_id_count=1  vlan_tpid=0x8100  vlan_user_priority=0  vlan_user_priority_step=0  use_vpn_parameters=0  site_id=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_2_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=101.1.0.1  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.1.0.0  nest_owner=${topology_2_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_5_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=100.1.0.1  counter_step=255.255.255.255  counter_direction=decrement  nest_step=0.0.0.1  nest_owner=${topology_2_handle}  nest_enabled=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_6_handle} =  Get From Dictionary  ${result}  multivalue_handle
	

	${result} =  Interface Config  protocol_name=IPv4 2  protocol_handle=${ethernet_2_handle}  mtu=1500  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  gateway=${multivalue_6_handle}  intf_ip_addr=${multivalue_5_handle}  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_2_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
################################################################################
# Configure Topology 3, Device Group 3                                         #
################################################################################
	
	Log To Console  Adding topology 3 on port 3
	${result} =  Topology Config  topology_name=Topology 3  port_handle=@{portHandles}[2]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_3_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 3 in topology 3
	${result} =  Topology Config  topology_handle=${topology_3_handle}  device_group_name=Device Group 3  device_group_multiplier=45  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_3_handle} =  Get From Dictionary  ${result}  device_group_handle
	
################################################################################
# Configure protocol interfaces for the third topology                         #
################################################################################
	
	${result} =  Multivalue Config  pattern=counter  counter_start=00.13.01.00.00.01  counter_step=00.00.00.00.00.01  counter_direction=increment  nest_step=00.00.01.00.00.00  nest_owner=${topology_3_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_7_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	Log To Console  Creating ethernet stack for the third Device Group
	${result} =  Interface Config  protocol_name=Ethernet 3  protocol_handle=${deviceGroup_3_handle}  mtu=1500  src_mac_addr=${multivalue_7_handle}  vlan=0  vlan_id=1  vlan_id_step=0  vlan_id_count=1  vlan_tpid=0x8100  vlan_user_priority=0  vlan_user_priority_step=0  use_vpn_parameters=0  site_id=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_3_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=3000:0:0:1:0:0:0:2  counter_step=0:0:0:1:0:0:0:0  counter_direction=increment  nest_step=0:0:0:1:0:0:0:0  nest_owner=${topology_3_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_8_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=3000:0:1:1:0:0:0:2  counter_step=0:0:0:1:0:0:0:0  counter_direction=increment  nest_step=0:0:0:1:0:0:0:0  nest_owner=${topology_3_handle}  nest_enabled=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_9_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Interface Config  protocol_name=IPv6 3  protocol_handle=${ethernet_3_handle}  ipv6_multiplier=1  ipv6_resolve_gateway=1  ipv6_manual_gateway_mac=00.00.00.00.00.01  ipv6_manual_gateway_mac_step=00.00.00.00.00.00  ipv6_gateway=${multivalue_9_handle}  ipv6_gateway_step=::0  ipv6_intf_addr=${multivalue_8_handle}  ipv6_intf_addr_step=::0  ipv6_prefix_length=64
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6_3_handle} =  Get From Dictionary  ${result}  ipv6_handle

################################################################################
# Configure Topology 4, Device Group 4                                         #
################################################################################
	
	Log To Console  Adding topology 4 on port 4
	${result} =  Topology Config  topology_name=Topology 4  port_handle=@{portHandles}[3]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_4_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 4 in topology 4
	${result} =  Topology Config  topology_handle=${topology_4_handle}  device_group_name=Device Group 4  device_group_multiplier=45  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_4_handle} =  Get From Dictionary  ${result}  device_group_handle
	
################################################################################
# Configure protocol interfaces for the fourth topology                        #
################################################################################
	
	${result} =  Multivalue Config  pattern=counter  counter_start=00.14.01.00.00.01  counter_step=00.00.00.00.00.01  counter_direction=increment  nest_step=00.00.01.00.00.00  nest_owner=${topology_4_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_10_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	Log To Console  Creating ethernet stack for the fourth Device Group
	${result} =  Interface Config  protocol_name=Ethernet 4  protocol_handle=${deviceGroup_4_handle}  mtu=1500  src_mac_addr=${multivalue_10_handle}  vlan=0  vlan_id=1  vlan_id_step=0  vlan_id_count=1  vlan_tpid=0x8100  vlan_user_priority=0  vlan_user_priority_step=0  use_vpn_parameters=0  site_id=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_4_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=3000:0:1:1:0:0:0:2  counter_step=0:0:0:1:0:0:0:0  counter_direction=increment  nest_step=0:0:0:1:0:0:0:0  nest_owner=${topology_4_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_11_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=3000:0:0:1:0:0:0:2  counter_step=0:0:0:1:0:0:0:0  counter_direction=increment  nest_step=0:0:0:1:0:0:0:0  nest_owner=${topology_4_handle}  nest_enabled=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_12_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Interface Config  protocol_name=IPv6 4  protocol_handle=${ethernet_4_handle}  ipv6_multiplier=1  ipv6_resolve_gateway=1  ipv6_manual_gateway_mac=00.00.00.00.00.01  ipv6_manual_gateway_mac_step=00.00.00.00.00.00  ipv6_gateway=${multivalue_12_handle}  ipv6_gateway_step=::0  ipv6_intf_addr=${multivalue_11_handle}  ipv6_intf_addr_step=::0  ipv6_prefix_length=64
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv6_4_handle} =  Get From Dictionary  ${result}  ipv6_handle
	
####################################################
##Configure traffic for all configuration elements##

##########################################################
# Configure trafficItem 1 for Layer 47 AppLibrary Profile
##########################################################

	${traffic_item_1_status} =  Traffic L47 Config  mode=create  name=Traffic_Item_1  circuit_endpoint_type=ipv4_application_traffic  emulation_src_handle=${topology_1_handle}  emulation_dst_handle=${topology_2_handle}  objective_type=users  objective_value=100  objective_distribution=apply_full_objective_to_each_port  enable_per_ip_stats=1  flows=IRC_Login_Auth_Failure IRC_Private_Chat iSCSI_Read_and_Write iTunes_Desktop_App_Store iTunes_Mobile_App_Store Jabber_Chat Laposte_Webmail_1307 LinkedIn Linkedin_1301 LPD
	${status} =  Get From Dictionary  ${traffic_item_1_status}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
##########################################################
# Configure trafficItem 2 for Layer 47 AppLibrary Profile
##########################################################

	${traffic_item_2_status} =  Traffic L47 Config  mode=create  name=Traffic_Item_2  circuit_endpoint_type=ipv6_application_traffic  emulation_src_handle=${topology_3_handle}  emulation_dst_handle=${topology_4_handle}  objective_type=users  objective_value=100  objective_distribution=apply_full_objective_to_each_port  enable_per_ip_stats=1  flows=MAX_Bandwidth_HTTP Microsoft_Update MMS_MM1_WAP_HTTP Modbus MS_SQL_Create MS_SQL_Delete MS_SQL_Drop MS_SQL_Insert MS_SQL_Server MS_SQL_Server_Advanced
	${status} =  Get From Dictionary  ${traffic_item_2_status}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	${trafficItem_1_handle} =  Set Variable  ${traffic_item_1_status['traffic_l47_handle']}
	${responder_port_item1} =  Set Variable  ${traffic_item_1_status['${trafficItem_1_handle}']['responder_ports']}
	${applib_handle_item1} =  Set Variable  ${traffic_item_1_status['${trafficItem_1_handle}']['applib_profile']}
	${applib_flow_item1} =  Set Variable  ${traffic_item_1_status['${trafficItem_1_handle}']['${applib_handle_item1}']['applib_flow']}
	
	
	${trafficItem_2_handle} =  Set Variable  ${traffic_item_2_status['traffic_l47_handle']}
	${responder_port_item2} =  Set Variable  ${traffic_item_2_status['${trafficItem_2_handle}']['responder_ports']}
	${applib_handle_item2} =  Set Variable  ${traffic_item_2_status['${trafficItem_2_handle}']['applib_profile']}
	${applib_flow_item2} =  Set Variable  ${traffic_item_2_status['${trafficItem_2_handle}']['${applib_handle_item2}']['applib_flow']}


####################################################
# Start protocols
####################################################

	${result} =  Test Control  action=start_all_protocols
	${status} =  Get From Dictionary  ${traffic_item_2_status}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

################################################################################
# Start traffic                                                                #
################################################################################
	Log To Console  Running traffic
	${result} =  Traffic Control  action=run  traffic_generator=ixnetwork_540  type=l47
	${status} =  Get From Dictionary  ${traffic_item_2_status}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  10s
	
	${result} =  Traffic Stats  mode=L47_traffic_item_tcp  drill_down_type=per_ports_per_initiator_flows  drill_down_traffic_item=${trafficItem_1_handle}  drill_down_port=@{portHandles}[0]  drill_down_flow=IRC_Login_Auth_Failure
	${status} =  Get From Dictionary  ${traffic_item_2_status}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  10s
	
	${result} =  Traffic Stats  mode=L47_traffic_item_tcp  drill_down_type=per_ports_per_initiator_flows  drill_down_traffic_item=${trafficItem_2_handle}  drill_down_port=@{portHandles}[2]  drill_down_flow=Microsoft_Update
	${status} =  Get From Dictionary  ${traffic_item_2_status}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  10s
	
####################################################
# Stop traffic
####################################################
	${result} =  Traffic Control  action=stop  traffic_generator=ixnetwork_540  type=l47
	${status} =  Get From Dictionary  ${traffic_item_2_status}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  20s
	
####################################################
# Test END
####################################################
	Log To Console  Test run is PASSED




