*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  OperatingSystem  WITH NAME  OS
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.147/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.147/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl

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

	${result} =  Connect  device=${chassis}  reset=1  ixnetwork_tcl_server=${client_and_port}  port_list=@{portlist}  username=ixiaHLTQA  break_locks=1  interactive=1
	${connect_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${connect_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	
################################################################################
# Configure Topology, Device Group                                             # 
################################################################################
# Creating a topology on first port
	Log To Console  Adding topology 1 on port 1
	${result} =  Topology Config  topology_name="Topology for FEC128 1"  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 1 in topology 1
	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name="Provider Router 1"  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating a topology on second port
	Log To Console  Adding topology 2 on port 2
	${result} =  Topology Config  topology_name="Topology for FEC128 2"  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 2 in topology 2
	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name="Provider Router 2""  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	
################################################################################
# 1.Configure protocol                                                         #
################################################################################

# Creating ethernet stack for the first Device Group 
	Log To Console  Creating ethernet stack for the first Device Group
	${result} =  Interface Config  protocol_name="Ethernet 1"  protocol_handle=${deviceGroup_1_handle}  mtu=1500  src_mac_addr=18.03.73.c7.6c.b1  src_mac_addr_step=00.00.00.00.00.00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# Creating ethernet stack for the second Device Group
	Log To Console  Creating ethernet for the second Device Group
	${result} =  Interface Config  protocol_name="Ethernet 2"  protocol_handle=${deviceGroup_2_handle}  mtu=1500  src_mac_addr=18.03.73.c7.6c.01  src_mac_addr_step=00.00.01.00.00.00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_2_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# Creating IPv4 Stack on top of Ethernet Stack for the first Device Group
	Log To Console  Creating IPv4 Stack on top of Ethernet Stack for the first Device Group
	${result} =  Interface Config  protocol_name="IPv4 1"  protocol_handle=${ethernet_1_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.1  intf_ip_addr=20.20.20.2  intf_ip_addr_step=0.0.0.0  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_1_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group
	Log To Console  Creating IPv4 Stack on top of Ethernet Stack for the second Device Group
	${result} =  Interface Config  protocol_name="IPv4 2"  protocol_handle=${ethernet_2_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.2  intf_ip_addr=20.20.20.1  intf_ip_addr_step=0.0.0.0  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_2_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
################################################################################
# Other protocol configurations                                                # 
################################################################################
# This will create OSPFv2 on top of IP within Topology 1 
	Log To Console  This will create OSPFv2 on top of IP within Topology 1 
	${result} =  Emulation Ospf Config  handle=${ipv4_1_handle}  mode=create  network_type=ptop  protocol_name={OSPFv2-IF 1}  router_id=193.0.0.1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Creating OSPFv2 on top of IPv4 2 stack
	${result} =  Emulation Ospf Config  handle=${ipv4_2_handle}  mode=create  network_type=ptop  protocol_name={OSPFv2-IF 2}  router_id=194.0.0.1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
# Configuration of LDP Router and LDP Interface for the first Device Group with label space = 30, hello interval= 10, hold time = 45, keepalive interval = 30, keepalive holdtime =30
	Log To Console  Creating LDP Router for 1st Device Group
	${result} =  Emulation Ldp Config  handle=${ipv4_1_handle}  mode=create  lsr_id=193.0.0.1  interface_name="LDP-IF 1"  router_name="LDP 1"
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ldpBasicRouter_1_handle} =  Get From Dictionary  ${result}  ldp_basic_router_handle
	
# Configuration of LDP Router and LDP Interface for the second Device Group with label space = 30, hello interval= 10, hold time = 45, keepalive interval = 30, keepalive holdtime =30
	Log To Console  Creating LDP Router for 2nd Device Group
	${result} =  Emulation Ldp Config  handle=${ipv4_2_handle}  mode=create  lsr_id=194.0.0.1  interface_name="LDP-IF 2"  router_name="LDP 2"
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ldpBasicRouter_2_handle} =  Get From Dictionary  ${result}  ldp_basic_router_handle
	
# Creating IPv4 prefix pool of Network for Network Cloud behind first Device Group  with "ipv4_prefix_network_address" =201.1.0.1
	
	Log To Console  Creating IPv4 prefix pool behind first Device Group
	${result} =  Network Group Config  protocol_handle=${deviceGroup_1_handle}  protocol_name={Network Cloud 1}  connected_to_handle=${ethernet_1_handle}  type=ipv4-prefix  ipv4_prefix_network_address=201.1.0.1  ipv4_prefix_length=32  ipv4_prefix_number_of_addresses=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_1_handle} =  Get From Dictionary  ${result}  network_group_handle
	${ipv4PrefixPools_1_handle} =  Get From Dictionary  ${result}  ipv4_prefix_pools_handle
	
# Creating IPv4 prefix pool of Network for Network Cloud behind second Device Group  with "ipv4_prefix_network_address" =202.1.0.1
	
	Log To Console  Creating IPv4 prefix pool behind second Device Group
	${result} =  Network Group Config  protocol_handle=${deviceGroup_2_handle}  protocol_name={Network Cloud 2}  connected_to_handle=${ethernet_2_handle}  type=ipv4-prefix  ipv4_prefix_network_address=201.1.0.1  ipv4_prefix_length=32  ipv4_prefix_number_of_addresses=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_2_handle} =  Get From Dictionary  ${result}  network_group_handle
	${ipv4PrefixPools_2_handle} =  Get From Dictionary  ${result}  ipv4_prefix_pools_handle
	
# Modifying in IPv4 prefix for LDP Router related Configurations "label_value_start"=17
	Log To Console  Modification of LDP related parameters in Network Cloud
	${result} =  Emulation Ldp Route Config  handle=${networkGroup_1_handle}  mode=modify  egress_label_mode=fixed  fec_type=ipv4_prefix  label_value_start=17  label_value_start_step=1  lsp_handle=${networkGroup_1_handle}  fec_name={LDP FEC Range 1}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
# Modifying in IPv4 prefix for LDP Router related Configurations "label_value_start"=18
	Log To Console  Modification of LDP related parameters in Network Cloud
	
	${result} =  Emulation Ldp Route Config  handle=${networkGroup_2_handle}  mode=modify  egress_label_mode=fixed  fec_type=ipv4_prefix  label_value_start=18  label_value_start_step=1  lsp_handle=${networkGroup_2_handle}  fec_name={LDP FEC Range 2}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
# Going to create Chained Device Group 3  behind Network Cloud 1 within Topology 1 and renaming of that chained DG to "Provider Edge Router 1"
	Log To Console  Going to create Chained DG 3 in Topology 1 behind Network Cloud 1 and renaming it
	${result} =  Topology Config  device_group_name={Provider Edge Router 1}  device_group_multiplier=1  device_group_enabled=1  device_group_handle=${networkGroup_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating multivalue loopback adderress within chained DG in Topology 1
	Log To Console  Creating multivalue for loopback adderress within chained DG
	${result} =  Multivalue Config  pattern=counter  counter_start=201.1.0.1  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.0.0.1 0.0.0.1 0.1.0.0  nest_owner=${networkGroup_1_handle} ${deviceGroup_1_handle} ${topology_1_handle}  nest_enabled=0 0 1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_4_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating Loopback behind Chained DG.
	Log To Console  Creating Loopback behind Chained DG
	${result} =  Interface Config  protocol_name={IPv4 Loopback 1}  protocol_handle=${deviceGroup_1_1_handle}  enable_loopback=1  connected_to_handle=${networkGroup_1_handle}  intf_ip_addr=${multivalue_4_handle}  netmask=255.255.255.255
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4Loopback_1_handle} =  Get From Dictionary  ${result}  ipv4_loopback_handle
	
# Going to create Chained Device Group 4  behind Network Cloud 1 within Topology 2 and renaming of that chained DG to "Provider Edge Router 2"
	Log To Console  Going to create Chained DG 4 in Topology 2 behind Network Cloud 2 and renaming it
	${result} =  Topology Config  device_group_name={Provider Edge Router 2}  device_group_multiplier=1  device_group_enabled=1  device_group_handle=${networkGroup_2_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating multivalue loopback addresses within chained DG in Topology 2
	Log To Console  Creating multivalue for loopback addresses within chained DG
	${result} =  Multivalue Config  pattern=counter  counter_start=202.1.0.1  counter_step=0.0.0.1  counter_direction=increment  nest_step=0.0.0.1 0.0.0.1 0.1.0.0  nest_owner=${networkGroup_2_handle} ${deviceGroup_2_handle} ${topology_2_handle}  nest_enabled=0 0 1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_4_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating Loopback behind Chained DG.
	Log To Console  Creating Loopback behind Chained DG
	${result} =  Interface Config  protocol_name={IPv4 Loopback 2}  protocol_handle=${deviceGroup_2_1_handle}  enable_loopback=1  connected_to_handle=${networkGroup_2_handle}  intf_ip_addr=${multivalue_4_handle}  netmask=255.255.255.255
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4Loopback_2_handle} =  Get From Dictionary  ${result}  ipv4_loopback_handle
	
#Adding Targeted Router and LDP PW/VPLS on top of Loopback within Chained device group under topology 1 lsr_id="195.0.0.1",remote_ip_addr ="202.1.0.1",remote_ip_addr_step="0.0.0.1"
	Log To Console  Adding Targeted Router under topology 1
	${result} =  Emulation Ldp Config  handle=${ipv4Loopback_1_handle}  mode=create  label_adv=unsolicited  lsr_id=195.0.0.1  remote_ip_addr=202.1.0.1  remote_ip_addr_step=0.0.0.1  target_name={LDP 3}  initiate_targeted_hello=1  targeted_peer_name={LDP Targeted Peers 1}  lpb_interface_name={LDP-IF 3}  lpb_interface_active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ldpTargetedRouter_1_handle} =  Get From Dictionary  ${result}  ldp_targeted_router_handle
	
# Configuration LDP PW/VPLS on top of on top of Targeted Router fec_vc_label_value_start="216", fec_vc_peer_address="202.1.0.1",fec_vc_type="eth",
	Log To Console  Configuring LDP PW/VPLS on top of on top of Targeted Router
	${result} =  Emulation Ldp Route Config  mode=create  handle=${ldpTargetedRouter_1_handle}  fec_type=vc  fec_vc_count=1  fec_vc_fec_type=pw_id_fec  fec_vc_group_id=1  fec_vc_id_start=1  fec_vc_name={LDP PW/VPLS 1}  fec_vc_active=1  fec_vc_label_value_start=216  fec_vc_peer_address=202.1.0.1  fec_vc_type=eth  fec_vc_pw_status_code=clear_fault_code
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ldppwvpls_1_handle} =  Get From Dictionary  ${result}  ldppwvpls_handle
	
#Adding Targeted Router and LDP PW/VPLS on top of Loopback within Chained device group under topology 2 lsr_id="196.0.0.1",remote_ip_addr ="201.1.0.1",remote_ip_addr_step="0.0.0.1"
	Log To Console  Adding Targeted Router under topology 2
	${result} =  Emulation Ldp Config  handle=${ipv4Loopback_2_handle}  mode=create  label_adv=unsolicited  lsr_id=196.0.0.1  remote_ip_addr=201.1.0.1  remote_ip_addr_step=0.0.0.1  target_name={LDP 4}  initiate_targeted_hello=1  targeted_peer_name={LDP Targeted Peers 2}  lpb_interface_name={LDP-IF 4}  lpb_interface_active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ldpTargetedRouter_2_handle} =  Get From Dictionary  ${result}  ldp_targeted_router_handle
	
# Configuration LDP PW/VPLS on top of on top of Targeted Router fec_vc_label_value_start="516", fec_vc_peer_address="201.1.0.1",fec_vc_type="eth",
	Log To Console  Configuring LDP PW/VPLS on top of on top of Targeted Router
	${result} =  Emulation Ldp Route Config  mode=create  handle=${ldpTargetedRouter_2_handle}  fec_type=vc  fec_vc_count=1  fec_vc_fec_type=pw_id_fec  fec_vc_group_id=1  fec_vc_id_start=1  fec_vc_name={LDP PW/VPLS 2}  fec_vc_active=1  fec_vc_label_value_start=516  fec_vc_peer_address=201.1.0.1  fec_vc_type=eth  fec_vc_pw_status_code=clear_fault_code
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ldppwvpls_2_handle} =  Get From Dictionary  ${result}  ldppwvpls_handle
	
# Configuration of MAC Pool behind Chained Device within Topology 1
	Log To Console  Configuring CE MAC Pool in Topology 1
	${result} =  Network Group Config  protocol_handle=${deviceGroup_1_1_handle}  protocol_name={CE MAC Cloud 1}  connected_to_handle=${ldppwvpls_1_handle}  type=mac-pools  mac_pools_mac=a0.12.01.00.00.01
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_4_handle} =  Get From Dictionary  ${result}  network_group_handle
	${macPools_1_handle} =  Get From Dictionary  ${result}  mac_pools_handle
	
# Configuration of MAC Pool behind Chained Device within Topology 2
	Log To Console  Configuring CE MAC Pool in Topology 2
	${result} =  Network Group Config  protocol_handle=${deviceGroup_2_1_handle}  protocol_name={CE MAC Cloud 2}  connected_to_handle=${ldppwvpls_2_handle}  type=mac-pools  mac_pools_mac=a0.11.01.00.00.01
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${networkGroup_5_handle} =  Get From Dictionary  ${result}  network_group_handle
	${macPools_2_handle} =  Get From Dictionary  ${result}  mac_pools_handle
	
	Log To Console  Waiting 5 seconds before starting protocol(s) ...
	Sleep  5s
	
############################################################################
# Start LDP protocol                                                       #
############################################################################ 
	
	Log To Console  Starting LDP on topology1
	${result} =  Emulation Ldp Control  handle=${topology_1_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Starting LDP on topology2
	${result} =  Emulation Ldp Control  handle=${topology_2_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Waiting 30 seconds before starting protocol(s) ...
	Sleep  30s
	
############################################################################
# Retrieve protocol statistics                                             #
############################################################################
	
	Log To Console  Fetching LDP aggregated statistics
	${result} =  Emulation Ldp Info  handle=${ldpTargetedRouter_1_handle}  mode=stats
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
############################################################################
# Retrieve protocol learned info                                           #
############################################################################
	
	Log To Console  Fetching LDP  aggregated learned info for Topology 2
	${result} =  Emulation Ldp Info  handle=${ldpTargetedRouter_2_handle}  mode=lsp_labels
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
############################################################################
# Changing Label in both sides of FEC Ranges                               #
############################################################################
	
	Log To Console  Changing Label value for Topology 1 LDP VPN Ranges:
	${result} =  Emulation Ldp Route Config  mode=modify  handle=${ldppwvpls_2_handle}  lsp_handle=${ldppwvpls_2_handle}  fec_vc_label_value_start=5001
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Applying changes one the fly                                                 #
################################################################################
	
	Log To Console  Applying changes on the fly
	${result} =  Test Control  handle=${ipv4_1_handle}  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
	
############################################################################
# Retrieve protocol learned info again and notice the difference with      #
# previously retrieved learned info.                                       #    
############################################################################
	
	Log To Console  Fetching LDP  aggregated learned info for Topology 1
	${result} =  Emulation Ldp Info  handle=${ldpTargetedRouter_2_handle}  mode=lsp_labels
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
############################################################################
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv4 FEC Range, Destination->IPv4 FEC Range       #
# 2. Type      : Unicast IPv4 traffic                                      #
# 3. Flow Group: On IPv4 Destination Address                               #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : Source Destination EndPoint Set                           #
############################################################################
	
	Log To Console  Configuring L2-L3 traffic
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${macPools_1_handle}  emulation_dst_handle=${macPools_2_handle}  frame_sequencing=disable  frame_sequencing_mode=rx_threshold  name=Traffic_1_Item  circuit_endpoint_type=ethernet_vlan  rate_pps=100000  frame_size=64  mac_dst_mode=fixed  mac_src_mode=fixed  mac_src_tracking=1  track_by=ethernetIiSourceaddress0 trackingenabled0 ethernetIiDestinationaddress0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
############################################################################
# Start L2-L3 traffic configured earlier                                   #
############################################################################
	
	Log To Console  "Running Traffic...
	${result} =  Traffic Control  action=run  traffic_generator=ixnetwork_540  type=l23
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Let the traffic run for 20 seconds ...
	Sleep  20s
	
############################################################################
# Retrieve L2-L3 traffic stats                                             #
############################################################################
	
	Log To Console  Retrieving L2-L3 traffic stats
	${result} =  Traffic Stats  mode=all traffic_generator=ixnetwork_540  measure_mode=mixed
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
############################################################################
# Stop L2-L3 traffic started earlier                                       #
############################################################################
	
	Log To Console  "Stopping Traffic...
	${result} =  Traffic Control  action=stop  traffic_generator=ixnetwork_540  type=l23
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Sleep for 10 seconds ...
	Sleep  10s
	
############################################################################
# Stop all protocols                                                       #
############################################################################
	
	Log To Console  Stopping LDP on topology1
	${result} =  Emulation Ldp Control  handle=${topology_1_handle}  mode=stop
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Stopping LDP on topology2
	${result} =  Emulation Ldp Control  handle=${topology_2_handle}  mode=stop
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Stopping all protocol(s) ...
	${result} =  Test Control  action=stop_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  2s
	
	Log To Console  !!! Test Script Ends !!!
	
	
