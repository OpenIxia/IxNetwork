*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  OperatingSystem  WITH NAME  OS
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.147/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.147/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.232
${client_api_port} =  	8136
@{portlist} =  	12/1  12/2
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
# Configure Topology, Device Group on port 1                                   # 
################################################################################

# Creating a topology on first port

	${result} =  Topology Config  topology_name=Topology 1  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 

	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name=Device Group 1  device_group_multiplier=3  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating multivalue 
	
	${result} =  Multivalue Config  pattern=counter  counter_start=00.11.01.00.00.01  counter_step=00.00.00.00.00.01  counter_direction=increment  nest_step=00.00.01.00.00.00  nest_owner=${topology_1_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_1_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
###################################
##Configure Ethernet
###################################
	
	${result} =  Interface Config  protocol_name=Ethernet 1  protocol_handle=${deviceGroup_1_handle}  mtu=1500  src_mac_addr=${multivalue_1_handle}  vlan=1  vlan_id=1  vlan_id_step=1  vlan_id_count=1  vlan_tpid=0x8100  vlan_user_priority=0  vlan_user_priority_step=0  use_vpn_parameters=0  site_id=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# Creating multivalue 
	
	${result} =  Multivalue Config  pattern=counter  counter_start=100.1.0.2  counter_step=0.0.1.0  counter_direction=increment  nest_step=0.1.0.0  nest_owner=${topology_1_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_2_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=100.1.0.1  counter_step=0.0.1.0  counter_direction=increment  nest_step=0.1.0.0  nest_owner=${topology_1_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_3_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	
#####################################
#Configure Ipv4
#####################################
	
	${result} =  Interface Config  protocol_name=IPv4 1  protocol_handle=${ethernet_1_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=${multivalue_3_handle}  intf_ip_addr=${multivalue_2_handle}  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_1_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=192.1.0.1  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.1.0.0  nest_owner=${topology_1_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_4_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
####################################################
##Configure BFD
####################################################
	
	${result} =  Emulation Bfd Config  count=1  echo_rx_interval=0  echo_timeout=1500  echo_tx_interval=0  control_plane_independent=0  enable_demand_mode=0  flap_tx_interval=0  handle=${ipv4_1_handle}  min_rx_interval=1000  mode=create  detect_multiplier=3  poll_interval=0  router_id=${multivalue_4_handle}  tx_interval=1000  configure_echo_source_ip=0  echo_source_ip4=0.0.0.0  ip_diff_serv=0  interface_active=1  interface_name=BFDv4 IF 1  router_active=1  router_name=BfdRouter 1  session_count=1  enable_auto_choose_source=1  enable_learned_remote_disc=1  ip_version=4  session_discriminator=1  session_discriminator_step=0  remote_discriminator=1  remote_discriminator_step=0  source_ip_addr=0.0.0.0  remote_ip_addr=100.1.0.1  remote_ip_addr_step=0.0.1.0  hop_mode=singlehop  session_active=1  session_name=BFDv4 Session 1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${handle_bfd_topology1} =  Get From Dictionary  ${result}  bfd_v4_interface_handle
	
	
# Creating a device group in topology 

	${result} =  Topology Config  device_group_name=Device Group 3  device_group_multiplier=1  device_group_enabled=1  device_group_handle=${deviceGroup_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating multivalue 
	
	${result} =  Multivalue Config  pattern=counter  counter_start=2.2.2.2  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.0.0.1,0.1.0.0  nest_owner=${deviceGroup_1_handle},${topology_1_handle}  nest_enabled=0,1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_5_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
#################################################
#Configure IPv4 Loopback
#################################################
	
	${result} =  Interface Config  protocol_name=IPv4 Loopback 1  protocol_handle=${deviceGroup_2_handle}  enable_loopback=1  connected_to_handle=${ethernet_1_handle}  intf_ip_addr=${multivalue_5_handle}  netmask=255.255.255.255
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4Loopback_1_handle} =  Get From Dictionary  ${result}  ipv4_loopback_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=3.2.2.2  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.0.0.1,0.0.0.1  nest_owner=${deviceGroup_1_handle},${topology_1_handle}  nest_enabled=0,0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_6_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=194.0.0.1  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.0.0.1,0.1.0.0  nest_owner=${deviceGroup_1_handle},${topology_1_handle}  nest_enabled=0,1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_7_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
######################################
#Configure BFD
######################################
	
	${result} =  Emulation Bfd Config  count=1  echo_rx_interval=0  echo_timeout=1500  echo_tx_interval=0  control_plane_independent=0  enable_demand_mode=0  flap_tx_interval=0  handle=${ipv4Loopback_1_handle}  min_rx_interval=1000  mode=create  detect_multiplier=3  poll_interval=0  router_id=${multivalue_7_handle}  tx_interval=1000  configure_echo_source_ip=0  echo_source_ip4=0.0.0.0  ip_diff_serv=0  interface_active=1  interface_name=BFDv4 IF 3  router_active=1  router_name=BfdRouter 3  session_count=1  enable_auto_choose_source=1  enable_learned_remote_disc=1  ip_version=4  session_discriminator=1  session_discriminator_step=0  remote_discriminator=1  remote_discriminator_step=0  source_ip_addr=${multivalue_6_handle}  remote_ip_addr=3.2.2.2  remote_ip_addr_step=0.0.0.1  hop_mode=multiplehop  session_active=1  session_name=BFDv4 Session 3
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${handle_bfd_loop} =  Get From Dictionary  ${result}  bfd_v4_interface_handle
	
	
################################################################################
# Configure Topology, Device Group on port 2                                   # 
################################################################################

# Creating a topology on first port

	${result} =  Topology Config  topology_name=Topology 2  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 

	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name=Device Group 3  device_group_multiplier=3  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_3_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating multivalue 
	
	${result} =  Multivalue Config  pattern=counter  counter_start=00.12.01.00.00.01  counter_step=00.00.00.00.00.01  counter_direction=increment  nest_step=00.00.01.00.00.00  nest_owner=${topology_2_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_8_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
###################################
##Configure Ethernet
###################################
	
	${result} =  Interface Config  protocol_name=Ethernet 2  protocol_handle=${deviceGroup_3_handle}  mtu=1500  src_mac_addr=${multivalue_8_handle}  vlan=1  vlan_id=1  vlan_id_step=1  vlan_id_count=1  vlan_tpid=0x8100  vlan_user_priority=0  vlan_user_priority_step=0  use_vpn_parameters=0  site_id=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_2_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# Creating multivalue 
	
	${result} =  Multivalue Config  pattern=counter  counter_start=100.1.0.1  counter_step=0.0.1.0  counter_direction=increment  nest_step=0.1.0.0  nest_owner=${topology_2_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_9_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=100.1.0.2  counter_step=0.0.1.0  counter_direction=increment  nest_step=0.1.0.0  nest_owner=${topology_2_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_10_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	
#####################################
#Configure Ipv4
#####################################
	
	${result} =  Interface Config  protocol_name=IPv4 2  protocol_handle=${ethernet_2_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=${multivalue_10_handle}  intf_ip_addr=${multivalue_9_handle}  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_2_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=193.1.0.1  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.1.0.0  nest_owner=${topology_2_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_11_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
####################################################
##Configure BFD
####################################################
	
	${result} =  Emulation Bfd Config  count=1  echo_rx_interval=0  echo_timeout=1500  echo_tx_interval=0  control_plane_independent=0  enable_demand_mode=0  flap_tx_interval=0  handle=${ipv4_2_handle}  min_rx_interval=1000  mode=create  detect_multiplier=3  poll_interval=0  router_id=${multivalue_11_handle}  tx_interval=1000  configure_echo_source_ip=0  echo_source_ip4=0.0.0.0  ip_diff_serv=0  interface_active=1  interface_name=BFDv4 IF 2    router_active=1  router_name=BfdRouter 2    session_count=1  enable_auto_choose_source=1  enable_learned_remote_disc=1  ip_version=4  session_discriminator=1  session_discriminator_step=0  remote_discriminator=1  remote_discriminator_step=0  source_ip_addr=0.0.0.0  remote_ip_addr=100.1.0.2  remote_ip_addr_step=0.0.1.0  hop_mode=singlehop  session_active=1  session_name=BFDv4 Session 2
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${handle_bfd_topology2} =  Get From Dictionary  ${result}  bfd_v4_interface_handle
	
	
# Creating a device group in topology 

	${result} =  Topology Config  device_group_name=Device Group 4  device_group_multiplier=1  device_group_enabled=1  device_group_handle=${deviceGroup_3_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_4_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating multivalue 
	
	${result} =  Multivalue Config  pattern=counter  counter_start=3.2.2.2  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.0.0.1,0.1.0.0  nest_owner=${deviceGroup_3_handle},${topology_2_handle}  nest_enabled=0,1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_12_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
#################################################
#Configure IPv4 Loopback
#################################################
	
	${result} =  Interface Config  protocol_name=IPv4 Loopback 2  protocol_handle=${deviceGroup_4_handle}  enable_loopback=1  connected_to_handle=${ethernet_2_handle}  intf_ip_addr=${multivalue_12_handle}  netmask=255.255.255.255
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4Loopback_2_handle} =  Get From Dictionary  ${result}  ipv4_loopback_handle
	
	${result} =  Multivalue Config  pattern=counter  counter_start=195.0.0.1  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.0.0.1,0.1.0.0  nest_owner=${deviceGroup_3_handle},${topology_2_handle}  nest_enabled=0,1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_13_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
######################################
#Configure BFD
######################################
	
	${result} =  Emulation Bfd Config  count=1  echo_rx_interval=0  echo_timeout=1500  echo_tx_interval=0  control_plane_independent=0  enable_demand_mode=0  flap_tx_interval=0  handle=${ipv4Loopback_2_handle}  min_rx_interval=1000  mode=create  detect_multiplier=3  poll_interval=0  router_id=${multivalue_13_handle}  tx_interval=1000  configure_echo_source_ip=0  echo_source_ip4=0.0.0.0  ip_diff_serv=0  interface_active=1  interface_name=BFDv4 IF 4    router_active=1  router_name=BfdRouter 4    session_count=1  enable_auto_choose_source=1  enable_learned_remote_disc=1  ip_version=4  session_discriminator=1  session_discriminator_step=0  remote_discriminator=1  remote_discriminator_step=0  source_ip_addr=0.0.0.0  remote_ip_addr=2.2.2.2  remote_ip_addr_step=0.0.0.1  hop_mode=multiplehop  session_active=1  session_name=BFDv4 Session 4
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${handle_bfd_loop1} =  Get From Dictionary  ${result}  bfd_v4_interface_handle
	
	${result} =  Interface Config  protocol_handle=/globals  arp_on_linkup=0  single_arp_per_gateway=1  ipv4_send_arp_rate=200  ipv4_send_arp_interval=1000  ipv4_send_arp_max_outstanding=400  ipv4_send_arp_scale_mode=port  ipv4_attempt_enabled=0  ipv4_attempt_rate=200  ipv4_attempt_interval=1000  ipv4_attempt_scale_mode=port  ipv4_diconnect_enabled=0  ipv4_disconnect_rate=200  ipv4_disconnect_interval=1000  ipv4_disconnect_scale_mode=port  ipv4_re_send_arp_on_link_up=true
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Interface Config  protocol_handle=/globals  ethernet_attempt_enabled=0  ethernet_attempt_rate=200  ethernet_attempt_interval=1000  ethernet_attempt_scale_mode=port  ethernet_diconnect_enabled=0  ethernet_disconnect_rate=200  ethernet_disconnect_interval=1000  ethernet_disconnect_scale_mode=port
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	Log To Console  Waiting 5 seconds before starting protocol(s) ...
	Sleep  5s
	
#########################################################
#Starting Protocols
#########################################################
	Log To Console  Starting all protocol(s) ...
	
	${result} =  Test Control  action=start_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Waiting for 90 seconds
	Sleep  90s
###########################################################
#Checking Aggregate Stats using emulation_bfd_info
###########################################################
	
	Log To Console  Checking BFD Per Port Stats for Topology 1
	${result} =  Emulation Bfd Info  handle=${handle_bfd_topology1}  mode=aggregate
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	${sessions_configured} =  Set Variable  ${result['@{portHandles}[0]']['aggregate']['sessions_configured']}
	${sessions_configured_up} =  Set Variable   ${result['@{portHandles}[0]']['aggregate']['sessions_configured_up']}
	
	Run Keyword If  '${sessions_configured}' != '6'  FAIL  "Not all sessions configured"  ELSE  Log  "Status is SUCCESS"
	Run Keyword If  '${sessions_configured}' != '${sessions_configured_up}'  FAIL  "Not all sessions configured are UP"  ELSE  Log  "Status is SUCCESS"
	
	
######################################################################
#fetching and Verifying BFd learned info using emulation_bfd_info
######################################################################
	
	Log To Console  Checking Learned Info for Topology 1:item1
	${result} =  Emulation Bfd Info  handle=${handle_bfd_topology1}  mode=learned_info
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	${state} =  Set Variable  ${result['${handle_bfd_topology1}']['bfd_learned_info']['peer_session_state']}
	${session_type} =  Set Variable  ${result['${handle_bfd_topology1}']['bfd_learned_info']['session_type']}
	${session_used_by_protocol} =  Set Variable  ${result['${handle_bfd_topology1}']['bfd_learned_info']['session_used_by_protocol']}
	${my_disc} =  Set Variable  ${result['${handle_bfd_topology1}']['bfd_learned_info']['my_discriminator']}
	${my_ip} =  Set Variable  ${result['${handle_bfd_topology1}']['bfd_learned_info']['my_ip_address']}
	${tx_interval} =  Set Variable  ${result['${handle_bfd_topology1}']['bfd_learned_info']['recvd_tx_interval']}
	${multiplier} =  Set Variable  ${result['${handle_bfd_topology1}']['bfd_learned_info']['recvd_multiplier']}
	${recvd_flags} =  Set Variable  ${result['${handle_bfd_topology1}']['bfd_learned_info']['recvd_peer_flags']}
	
####################################################################
#Performing Stop/Start BFD interface using emualtion_bfd_control
####################################################################
	
	Log To Console  Performing Stop/Start on BFD interfaces and verifying stat
	${result} =  Emulation Bfd Control  handle=${handle_bfd_topology1}  mode=stop
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	${result} =  Emulation Bfd Control  handle=${handle_bfd_topology2}  mode=stop
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
###############################################################################
#Changing bfd configuration using emulation_bfd_config and -mode as modify
###############################################################################
	
	Log To Console  Changing Session discriminator and remote discriminator OTF, and verifing in Learned Info
	
	${result} =  Emulation Bfd Config  handle=${handle_bfd_topology1}  mode=modify  ip_version=4  session_discriminator=20  remote_discriminator=30  
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Applying changes one the fly                                                 #
################################################################################
	
	Log To Console  Applying changes on the fly
	${result} =  Test Control  handle=${ipv4_1_handle}  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  10s
	
	
#########################################################
#Stopping Protocols
#########################################################
	Log To Console  Starting all protocol(s) ...
	
	${result} =  Test Control  action=stop_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  TEST COMPLETED
	
	
	
	
	
	
	
	