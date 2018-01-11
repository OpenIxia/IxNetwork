*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  OperatingSystem  WITH NAME  OS
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.147/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.147/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
# Topology 2P-B2B
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
	Log  Adding topology 1 on port 1
	${result} =  Topology Config  topology_name="IGMP Host Topology"  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log  Creating device group 1 in topology 1
	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name="IGMP Host"  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating a topology on second port
	Log  Adding topology 2 on port 2
	${result} =  Topology Config  topology_name="IPv4 Topology 2"  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log  Creating device group 2 in topology 2
	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name=Device Group 2"  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	
################################################################################
#  Configure protocol interfaces                                               #
################################################################################
	
# Creating ethernet stack for the first Device Group 
	Log  Creating ethernet stack for the first Device Group
	${result} =  Interface Config  protocol_name="Ethernet 1"  protocol_handle=${deviceGroup_1_handle}  mtu=1500  src_mac_addr=18.03.73.c7.6c.b1  src_mac_addr_step=00.00.00.00.00.00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# Creating ethernet stack for the second Device Group
	Log  Creating ethernet for the second Device Group
	${result} =  Interface Config  protocol_name="Ethernet 2"  protocol_handle=${deviceGroup_2_handle}  mtu=1500  src_mac_addr=18.03.73.c7.6c.01  src_mac_addr_step=00.00.00.00.00.00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_2_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
	
# Creating IPv4 Stack on top of Ethernet Stack for the first Device Group     
	Log  Creating IPv4 Stack on top of Ethernet Stack for the first Device Group
	${result} =  Interface Config  protocol_name="IPv4 1"  protocol_handle=${ethernet_1_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.1  gateway=0.0.0.0  intf_ip_addr=20.20.20.2  intf_ip_addr_step=0.0.0.0  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_1_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
# Creating IPv4 Stack on top of Ethernet Stack for the second Device Group 
	Log  Creating IPv4 2 stack on ethernet 2 stack for the second Device Group
	${result} =  Interface Config  protocol_name="IPv4 2"  protocol_handle=${ethernet_2_handle}  ipv4_resolve_gateway=1  ipv4_manual_gateway_mac=00.00.00.00.00.01  ipv4_manual_gateway_mac_step=00.00.00.00.00.00  gateway=20.20.20.2  gateway=0.0.0.0  intf_ip_addr=20.20.20.1  intf_ip_addr_step=0.0.0.0  netmask=255.255.255.0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ipv4_2_handle} =  Get From Dictionary  ${result}  ipv4_handle
	
################################################################################
# Other protocol configurations                                                # 
################################################################################
	
# This will create IGMP v3 Host Stack with IPTV enabled on top of IPv4 stack having zap behavior as zap and view, zapping type as multicast to leave and zap direction as down.

# Creating IGMP Host Stack on top of IPv4 1 stack
	Log  Creating IGMP Host Stack on top of IPv4 1 stack
	${result} =  Emulation Igmp Config  handle=${ipv4_1_handle}  protocol_name="IGMP Host 1"  mode=create  filter_mode=include  igmp_version=v3  enable_iptv=true  iptv_name="IPTV 1"  stb_leave_join_delay=3000  join_latency_threshold=10000  leave_latency_threshold=10000  zap_behavior=zapandview  zap_direction=down  zap_interval_type=multicasttoleave  zap_interval=10000  num_channel_changes_before_view=1  view_duration=10000  log_failure_timestamps=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${igmpHost_1_handle} =  Get From Dictionary  ${result}  igmp_host_handle
	${igmp_host_iptv_handle} =  Get From Dictionary  ${result}  igmp_host_iptv_handle
	
	
# Creating IGMP Group Ranges 
	Log  Creating IGMP Group Ranges"
	${result} =  Emulation Multicast Group Config  mode=create  ip_addr_start=226.0.0.1  ip_addr_step=0.0.0.1  num_groups=1  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${igmpMcastIPv4GroupList_1_handle} =  Get From Dictionary  ${result}  multicast_group_handle
	
# Creating IGMP Source Ranges
	Log  Creating IGMP Source Ranges
	${result} =  Emulation Multicast Source Config  mode=create  ip_addr_start=10.10.10.1  ip_addr_step=0.0.0.0  num_sources=1  active=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${igmpUcastIPv4SourceList_1_handle} =  Get From Dictionary  ${result}  multicast_source_handle
	
# Creating IGMP Group and Source Ranges in IGMP Host stack
	Log  Creating IGMP Group and Source Ranges in IGMP Host stack
	${result} =  Emulation Igmp Group Config  mode=create  g_filter_mode=include  group_pool_handle=${igmpMcastIPv4GroupList_1_handle}  no_of_grp_ranges=1  no_of_src_ranges=1  session_handle=${igmpHost_1_handle}  source_pool_handle=${igmpUcastIPv4SourceList_1_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

# Configuring inter stb delay and rate control for IGMP Host global settings
	Log  Configuring inter stb delay and rate control for IGMP host
	${result} =  Emulation Igmp Config  handle=/globals  mode=create  global_settings_enable=1  inter_stb_start_delay=0  msg_count_per_interval=600  msg_interval=1000
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Waiting 5 seconds before starting protocol(s) ...
	Sleep  5s
	

############################################################################
# Start IGMP protocol                                                      #
############################################################################

	Log  Starting IGMP on topology1
	${result} =  Emulation Igmp Control  handle=${igmpHost_1_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Starting IPv4 on topology2
	${result} =  Test Control  handle=${ipv4_2_handle}  action=start_protocol
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Waiting for 30 seconds
	Sleep  30s
	
############################################################################
# Retrieve protocol statistics                                             #
############################################################################
	
	Log  Fetching IGMP aggregated statistics
	${result} =  Emulation Igmp Info  handle=${deviceGroup_1_handle}  type=host  mode=aggregate
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
	
############################################################################ 
# Configure L2-L3 traffic                                                  #
# 1. Endpoints : Source->IPv4, Destination->Multicast group                #
# 2. Type      : Multicast IPv4 traffic                                    #
# 3. Flow Group: On IPv4 Destination Address                               #
# 4. Rate      : 1000 packets per second                                   #
# 5. Frame Size: 512 bytes                                                 #
# 6. Tracking  : IPv4 Destination Address                                  #
############################################################################
	
	Log  Configuring L2-L3 traffic
	${result} =  Traffic Config  mode=create  traffic_generator=ixnetwork_540  endpointset_count=1  emulation_src_handle=${ipv4_2_handle}  emulation_dst_handle=${igmpMcastIPv4GroupList_1_handle}  emulation_multicast_dst_handle=226.0.0.1/0.0.0.0/1  emulation_multicast_dst_handle_type=none  emulation_multicast_rcvr_handle=${igmpMcastIPv4GroupList_1_handle}  emulation_multicast_rcvr_port_index=0  emulation_multicast_rcvr_host_index=0  emulation_multicast_rcvr_mcast_index=0  name=TI0-Traffic_Item_1  circuit_endpoint_type=ipv4  transmit_distribution=ipv4DestIp0  rate_pps=1000  frame_size=512  track_by=trackingenabled0 ipv4DestIp0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
############################################################################
#  Start L2-L3 traffic configured earlier                                  #
############################################################################
	
	Log  Running Traffic...
	${result} =  Traffic Control  action=run  traffic_generator=ixnetwork_540  type=l23
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Let the traffic run for 20 seconds ...
	Sleep  20s

	
############################################################################
# Starting IPTV                                                            #
############################################################################

	Log  Starting IPTV...
	${result} =  Emulation Igmp Control  handle=${igmp_host_iptv_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  10s
############################################################################
# Retrieve L2-L3 traffic stats                                             #
############################################################################
	
	Log  Retrieving L2-L3 traffic stats
	${result} =  Traffic Stats  mode=all  traffic_generator=ixnetwork_540  measure_mode=mixed
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
	
############################################################################
# Making on the fly changes for zapDirection, zapIntervalType, zapInterval,#    
# numChannelChangesBeforeView and viewDuration in IPTV tab of IGMP host    #
	
	Log  Making on the fly chnages for zapDirection, zapIntervalType, zapInterval, numChannelChangesBeforeView and viewDuration
	${result} =  Emulation Igmp Config  handle=${igmpHost_1_handle}  mode=modify  zap_direction=up  zap_interval_type=leavetoleave  zap_interval=30000  num_channel_changes_before_view=4  view_duration=40000
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

############################################################################
# Applying changes one the fly                                             #
############################################################################
	
	Log  Applying changes on the fly
	${result} =  Test Control  handle=${ipv4_1_handle}  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  5s
	
############################################################################
# Retrieve protocol statistics after doing on the fly changes              #
############################################################################
	
	Log  Fetching IGMP aggregated statistics
	${result} =  Emulation Igmp Info  handle=${deviceGroup_1_handle}  type=host  mode=aggregate
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${result}
	
############################################################################
# Stopping IPTV                                                            #
############################################################################

	Log  Stopping IPTV...
	${result} =  Emulation Igmp Control  handle=${igmp_host_iptv_handle}  mode=stop
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
############################################################################
# Stop L2-L3 traffic started earlier                                       #
############################################################################
	
	Log  Stopping Traffic...
	${result} =  Traffic Control  action=stop  traffic_generator=ixnetwork_540  type=l23
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
	
############################################################################
# Stop all protocols                                                       #
############################################################################
	
	Log  Stopping all protocol(s) ...
	${result} =  Test Control  action=stop_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	#Log  Sleep !!! Test Script Ends !!!
	