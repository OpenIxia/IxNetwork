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
	${result} =  Topology Config  topology_name="ldp Topology 1"  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 1 in topology 1
	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name="ldp Topology 1 Router"  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating a topology on second port
	Log To Console  Adding topology 2 on port 2
	${result} =  Topology Config  topology_name="ldp Topology 2"  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 2 in topology 2
	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name="ldp Topology 2 Router""  device_group_multiplier=1  device_group_enabled=1
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

# Configuration of LDP Router and LDP Interface for the first Device Group with label space = 30, hello interval= 10, hold time = 45, keepalive interval = 30, keepalive holdtime =30
	Log To Console  Creating LDP Router for 1st Device Group
	${result} =  Emulation Ldp Config  handle=${ipv4_1_handle}  mode=create  lsr_id=193.0.0.1  label_space=30  hello_interval=10  hello_hold_time=30  keepalive_interval=30  keepalive_holdtime=45  interface_name="LDP-IF 1"  router_name="LDP 1"
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ldpBasicRouter_1_handle} =  Get From Dictionary  ${result}  ldp_basic_router_handle
	
# Configuration of LDP Router and LDP Interface for the second Device Group with label space = 30, hello interval= 10, hold time = 45, keepalive interval = 30, keepalive holdtime =30
	Log To Console  Creating LDP Router for 2nd Device Group
	${result} =  Emulation Ldp Config  handle=${ipv4_2_handle}  mode=create  lsr_id=194.0.0.1  label_space=30  hello_interval=10  hello_hold_time=30  keepalive_interval=30  keepalive_holdtime=45  interface_name="LDP-IF 2"  router_name="LDP 2"
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
	${result} =  Emulation Ldp Route Config  handle=${networkGroup_1_handle}  mode=modify  fec_type=ipv4_prefix  label_value_start=516  label_value_start_step=1  lsp_handle=${networkGroup_1_handle}  fec_name={LDP FEC Range 1}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${fec_handle_1} =  Get From Dictionary  ${result}  fecproperty_handle
	
# Modifying in IPv4 prefix for LDP Router related Configurations "label_value_start"=18
	Log To Console  Modification of LDP related parameters in Network Cloud
	${result} =  Emulation Ldp Route Config  handle=${networkGroup_2_handle}  mode=modify  fec_type=ipv4_prefix  label_value_start=216  label_value_start_step=1  lsp_handle=${networkGroup_2_handle}  fec_name={LDP FEC Range 2}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${fec_handle_2} =  Get From Dictionary  ${result}  fecproperty_handle
	
# Creating multivalue for Device Group 3 for multiplier 10 
	Log To Console  Creating multivalue for Device Group 3
	${result} =  Topology Config  device_group_name="Device Group 3"  device_group_multiplier=10  device_group_enabled=1  device_group_handle=${networkGroup_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating of Chained Device Group for configuration of loopback behind first Device Group
	Log To Console  Creating IPv4 loopback for configuring L4-L7 App Traffic for Topology 1
	${result} =  Interface Config  protocol_name="IPv4 Loopback 1"  protocol_handle=${deviceGroup_2_handle}  enable_loopback=1  connected_to_handle=${networkGroup_1_handle}  intf_ip_addr=201.1.0.0  netmask=255.255.255.255
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4Loopback_1_handle} =  Get From Dictionary  ${result}  ipv4_loopback_handle
	
	
# Creating multivalue for Device Group 4 for multiplier 10 
	Log To Console  Creating multivalue for Device Group 4
	${result} =  Topology Config  device_group_name="Device Group 4"  device_group_multiplier=10  device_group_enabled=1  device_group_handle=${networkGroup_2_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_3_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating of Chained Device Group for configuration of loopback behind second Device Group
	Log To Console  Creating IPv4 loopback for configuring L4-L7 App Traffic for Topology 2
	${result} =  Interface Config  protocol_name="IPv4 Loopback 2"  protocol_handle=${deviceGroup_3_handle}  enable_loopback=1  connected_to_handle=${networkGroup_2_handle}  intf_ip_addr=202.1.0.0  netmask=255.255.255.255
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4Loopback_2_handle} =  Get From Dictionary  ${result}  ipv4_loopback_handle
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
	${result} =  Emulation Ldp Info  handle=${ldpBasicRouter_1_handle}  mode=stats
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
############################################################################
# Retrieve protocol learned info                                           #
############################################################################
	
	Log To Console  Fetching LDP  aggregated learned info for Topology 2
	${result} =  Emulation Ldp Info  handle=${ldpBasicRouter_2_handle}  mode=lsp_labels
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
############################################################################
# Changing Label in both sides of FEC Ranges                               #
############################################################################
	
	Log To Console  Changing Label value for Topology 1 LDP VPN Ranges:
	${result} =  Emulation Ldp Route Config  mode=modify  handle=${fec_handle_2}  lsp_handle=${fec_handle_2}  label_value_start=5016  label_value_start_step=100
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
	${result} =  Emulation Ldp Info  handle=${ldpBasicRouter_1_handle}  mode=lsp_labels
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
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${ipv4PrefixPools_1_handle}  emulation_dst_handle=${ipv4PrefixPools_2_handle}  frame_sequencing=disable  frame_sequencing_mode=rx_threshold  name=Traffic_1_Item  circuit_endpoint_type=ipv4  transmit_distribution=ipv4DestIp0  rate_pps=1000  frame_size=512  track_by=sourceDestEndpointPair0 trackingenabled0
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
	${result} =  Traffic Stats  mode=all  traffic_generator=ixnetwork_540  measure_mode=mixed
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
	
	
