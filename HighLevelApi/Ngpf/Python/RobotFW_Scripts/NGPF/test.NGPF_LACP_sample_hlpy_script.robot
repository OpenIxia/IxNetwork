*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  OperatingSystem  WITH NAME  OS
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl

*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.232
${client_api_port} =  	8136
@{portlist} =  	12/1  12/2  12/3  12/4
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
#  Creating a topology on 1st and 3rd port
	Log To Console  Adding topology 1 on port 1 and port 3
	${result} =  Topology Config  topology_name="LAG1-LHS"  port_handle=@{portHandles}[0] @{portHandles}[2]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 1 in topology 1
	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name="SYSTEM1-lacp-LHS"  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# Creating a topology on 2nd and 4th port
	Log To Console  Adding topology 2 on port 2 and port 4
	${result} =  Topology Config  topology_name="LAG1-RHS"  port_handle=@{portHandles}[1] @{portHandles}[3]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 2 in topology 2
	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name="SYSTEM1-lacp-RHS"  device_group_multiplier=1  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${deviceGroup_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	
################################################################################
# 1.Configure protocol                                                         #
################################################################################

# Creating ethernet stack for the first Device Group 
	Log To Console  Creating ethernet stack for the first Device Group
	${result} =  Interface Config  protocol_name="Ethernet 1"  protocol_handle=${deviceGroup_1_handle}  mtu=1500  src_mac_addr=00.11.01.00.00.01  src_mac_addr_step=00.00.01.00.00.00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# Creating ethernet stack for the second Device Group
	Log To Console  Creating ethernet for the second Device Group
	${result} =  Interface Config  protocol_name="Ethernet 2"  protocol_handle=${deviceGroup_2_handle}  mtu=1500  src_mac_addr=00.12.01.00.00.01  src_mac_addr_step=00.00.01.00.00.00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_2_handle} =  Get From Dictionary  ${result}  ethernet_handle

# Creating LACP on top of Ethernet Stack for the first Device Group
	Log To Console  Creating LACP on top of Ethernet Stack for the first Device Group
	
# Creating multivalue for Actor key = 666
	Log To Console  Creating multivalue for Actor key = 666
	${result} =  Multivalue Config  pattern=single_value  single_value=1  nest_step=1  nest_owner=${topology_1_handle}  nest_enabled=0  overlay_value=666,666  overlay_value_step=666,666  overlay_index=1,2  overlay_index_step=0,0  overlay_count=1,1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log To Console  "Status is SUCCESS"
	${multivalue_1_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating multivalue for System Id = 00:00:00:00:06:66
	Log To Console  Creating multivalue for System Id = 00:00:00:00:06:66
	${result} =  Multivalue Config  pattern=counter  counter_start=00:00:00:00:00:01  counter_step=00:00:00:00:00:00  counter_direction=increment  nest_step=00:00:00:00:00:01  nest_owner=${topology_1_handle}  nest_enabled=0  overlay_value=00:00:00:00:06:66,00:00:00:00:06:66  overlay_value_step=00:00:00:00:06:66,00:00:00:00:06:66  overlay_index=1,2  overlay_index_step=0,0  overlay_count=1,1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log To Console  "Status is SUCCESS"
	${multivalue_2_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Configuring SYSTEM1-lacp-LHS with Actor Key, System Id and flags
	Log To Console  Configuring SYSTEM1-lacp-LHS with Actor Key, System Id and flags
	${result} =  Emulation Lacp Link Config  mode=create  handle=${ethernet_1_handle}  active=1  session_type=lacp  actor_key=${multivalue_1_handle}  actor_port_num=1  actor_port_num_step=0  actor_port_pri=1  actor_port_pri_step=0  actor_system_id=${multivalue_2_handle}  administrative_key=1  collecting_flag=1  distributing_flag=1  sync_flag=1  aggregation_flag=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${lacp_1_handle} =  Get From Dictionary  ${result}  lacp_handle
	
# Creating LACP on top of Ethernet Stack for the second Device Group
	Log To Console  Creating LACP on top of Ethernet Stack for the second Device Group
	
# Creating multivalue for Actor key = 777
	Log To Console  Creating multivalue for Actor key = 777
	${result} =  Multivalue Config  pattern=single_value  single_value=1  nest_step=1  nest_owner=${topology_2_handle}  nest_enabled=0  overlay_value=777,777  overlay_value_step=777,777  overlay_index=1,2  overlay_index_step=0,0  overlay_count=1,1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_3_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Creating multivalue for System Id = 00:00:00:00:07:77
	Log To Console  Creating multivalue for System Id = 00:00:00:00:07:77
	${result} =  Multivalue Config  pattern=counter  counter_start=00:00:00:00:00:02  counter_step=00:00:00:00:00:00  counter_direction=increment  nest_step=00:00:00:00:00:01  nest_owner=${topology_2_handle}  nest_enabled=0  overlay_value=00:00:00:00:07:77,00:00:00:00:07:77  overlay_value_step=00:00:00:00:07:77,00:00:00:00:07:77  overlay_index=1 2  overlay_index_step=0 0  overlay_count=1 1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_4_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
# Configuring SYSTEM1-lacp-RHS with Actor Key, System Id and flags
	Log To Console  Configuring SYSTEM1-lacp-RHS with Actor Key, System Id and flags
	${result} =  Emulation Lacp Link Config  mode=create  handle=${ethernet_2_handle}  active=1  session_type=lacp  actor_key=${multivalue_3_handle}  actor_port_num=1  actor_port_num_step=0  actor_port_pri=1  actor_port_pri_step=0  actor_system_id=${multivalue_4_handle}  administrative_key=1  collecting_flag=1  distributing_flag=1  sync_flag=1  aggregation_flag=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${lacp_2_handle} =  Get From Dictionary  ${result}  lacp_handle
	
	Log To Console  Waiting 5 seconds before starting protocol(s) ...
	Sleep  5s
	
################################################################################
# Start protocol                                                               #
################################################################################

	Log To Console  Starting LACP on topology1
	${result} =  Emulation Lacp Control  handle=${lacp_1_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Starting LACP on topology2
	${result} =  Emulation Lacp Control  handle=${lacp_2_handle}  mode=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Waiting for 20 seconds
	Sleep  20s
	

################################################################################
# Get LACP learned_info   stats                                                #
################################################################################
	
	Log To Console  Fetching SYSTEM1-lacp-LHS learned_info
	${result} =  Emulation Lacp Info  handle=${lacp_1_handle}  mode=global_learned_info  session_type=lacp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  Printing SYSTEM1-lacp-LHS learned_info
	Log To Console  ${result}
	
################################################################################
# Get LACP per-port stats                                                      #
################################################################################
	Log To Console  Fetching SYSTEM1-lacp-RHS per port stats
	${result} =  Emulation Lacp Info  handle=${lacp_2_handle}  mode=per_port  session_type=lacp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log To Console  Printing SYSTEM1-lacp-RHS per port stats
	Log  ${result}
	Sleep  5s
	
################################################################################
# Disable Synchronization flag on port1 in System1-LACP-LHS                    #
################################################################################
	
	Log To Console  Disable Synchronization flag on port1 in System1-LACP-LHS
	${result} =  Emulation Lacp Link Control  handle=${lacp_1_handle}  mode=modify  sync_flag=0  session_type=lacp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
################################################################################
# Applying changes one the fly                                                 #
################################################################################
	
	Log To Console  Applying changes on the fly
	${result} =  Test Control  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  5s
	
################################################################################
# Get LACP learned_info   stats                                                #
################################################################################
	
	Log To Console  Fetching SYSTEM1-lacp-LHS learned_info
	${result} =  Emulation Lacp Info  handle=${lacp_1_handle}  mode=global_learned_info  session_type=lacp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  Printing SYSTEM1-lacp-LHS learned_info
	Log To Console  ${result}
	
################################################################################
# Get LACP per-port   stats                                                    #
################################################################################
	
	Log To Console  Fetching SYSTEM1-lacp-RHS per port stats
	${result} =  Emulation Lacp Info  handle=${lacp_2_handle}  mode=per_port  session_type=lacp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log To Console  Printing SYSTEM1-lacp-RHS per port stats
	Log  ${result}
	Sleep  5s
	
################################################################################
# Re-enable Synchronization flag on port1 in System1-LACP-LHS                  #
################################################################################
	
	Log To Console  Re-enable Synchronization flag on port1 in System1-LACP-LHS
	${result} =  Emulation Lacp Link Control  handle=${lacp_1_handle}  mode=modify  sync_flag=1  session_type=lacp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
################################################################################
# Applying changes one the fly                                                 #
################################################################################
	
	Log To Console  Applying changes on the fly
	${result} =  Test Control  action=apply_on_the_fly_changes
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  5s
	
################################################################################
# Get LACP learned_info   stats                                                #
################################################################################
	
	Log To Console  Fetching SYSTEM1-lacp-LHS learned_info
	${result} =  Emulation Lacp Info  handle=${lacp_1_handle}  mode=global_learned_info  session_type=lacp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  Printing SYSTEM1-lacp-LHS learned_info
	Log To Console  ${result}
	
################################################################################
# Get LACP per-port stats                                                      #
################################################################################
	
	Log To Console  Fetching SYSTEM1-lacp-RHS per port stats
	${result} =  Emulation Lacp Info  handle=${lacp_2_handle}  mode=per_port  session_type=lacp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log To Console  Printing SYSTEM1-lacp-RHS per port stats
	Log  ${result}
	Sleep  5s
	
################################################################################
# Perform Simulate Link Down on port1 in System1-LACP-LHS                      #
################################################################################
	
	Log To Console  Perform Simulate Link Down on port1 in System1-LACP-LHS
	${result} =  Interface Config  port_handle=@{portHandles}[0]  op_mode=sim_disconnect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  5s
	
################################################################################
# Get LACP learned_info   stats                                                #
################################################################################
	
	Log To Console  Fetching SYSTEM1-lacp-LHS learned_info
	${result} =  Emulation Lacp Info  handle=${lacp_1_handle}  mode=global_learned_info  session_type=lacp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  Printing SYSTEM1-lacp-LHS learned_info
	Log To Console  ${result}
	
################################################################################
# Get LACP per-port stats                                                      #
################################################################################
	
	Log To Console  Fetching SYSTEM1-lacp-RHS per port stats
	${result} =  Emulation Lacp Info  handle=${lacp_2_handle}  mode=per_port  session_type=lacp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log To Console  Printing SYSTEM1-lacp-RHS per port stats
	Log  ${result}
	Sleep  5s
	
################################################################################
# Perform Simulate Link Down on port1 in System1-LACP-LHS                      #
################################################################################
	
	Log To Console  Perform Simulate Link Down on port1 in System1-LACP-LHS
	${result} =  Interface Config  port_handle=@{portHandles}[0]  op_mode=normal
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Sleep  5s
	
################################################################################
# Get LACP learned_info   stats                                                #
################################################################################
	
	Log To Console  Fetching SYSTEM1-lacp-LHS learned_info
	${result} =  Emulation Lacp Info  handle=${lacp_1_handle}  mode=global_learned_info  session_type=lacp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  Printing SYSTEM1-lacp-LHS learned_info
	Log To Console  ${result}
	
################################################################################
# Get LACP per-port stats                                                      #
################################################################################
	
	Log To Console  Fetching SYSTEM1-lacp-RHS per port stats
	${result} =  Emulation Lacp Info  handle=${lacp_2_handle}  mode=per_port  session_type=lacp
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log To Console  Printing SYSTEM1-lacp-RHS per port stats
	Log  ${result}
	Sleep  5s
	
###############################################################################
# Stop all protocols                                                          #
###############################################################################
	Log  Stopping all protocol(s) ...
	{result} =  Test Control  action=stop_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log TO Console  !!! Test Script Ends !!!
	
	
