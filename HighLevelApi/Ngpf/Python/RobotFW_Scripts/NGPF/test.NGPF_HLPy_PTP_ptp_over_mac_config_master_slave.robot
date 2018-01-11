*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.147/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.147/PythonApi  ngpf

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.09_OSPFv2_routers_routes_lsa_start_stop_restart_stats_new.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	12/7  12/8
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

# Configure PTP Master ...
	Log To Console  Configure PTP Master ...
	Log To Console  Adding topology 1 on port 1
	${result} =  Topology Config  topology_name=PTP Master Topology  port_handle=@{portHandles}[0]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_1_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 1 in topology 1
	${result} =  Topology Config  topology_handle=${topology_1_handle}  device_group_name=PTP MAster 1  device_group_multiplier=3  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${device_1_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# CREATE ETHERNET STACK FOR PTP 1
	
	${result} =  Multivalue Config  pattern=counter  counter_start=00.11.01.00.00.01  counter_step=00.00.00.00.00.01  counter_direction=increment  nest_step=00.00.01.00.00.00  nest_owner=${topology_1_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_1_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	Log To Console  Creating ethernet stack for the first Device Group
	${result} =  Interface Config  protocol_name=Ethernet 1  protocol_handle=${device_1_handle}  mtu=1500  src_mac_addr=${multivalue_1_handle}  vlan=1  vlan_id=101  vlan_id_step=1  vlan_id_count=1  vlan_tpid=0x8100  vlan_user_priority=0  vlan_user_priority_step=0  use_vpn_parameters=0  site_id=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_1_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# CREATE PTP STACK
	
	${result} =  Ptp Over Mac Config  parent_handle=${ethernet_1_handle}  profile=ieee1588  role=master  mode=create  name=PTP Master  port_number=6323  communication_mode=multicast  domain=123  priority1=10  priority2=100
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ptp_master} =  Get From Dictionary  ${result}  ptp_handle
	
##############################################################################
# 								PTP SLAVE CONFIG
##############################################################################
	
# CREATE TOPOLOGY 2
	Log To Console  Configure PTP Slave ...
	Log To Console  Adding topology 2 on port 2
	${result} =  Topology Config  topology_name=PTP Slave Topology  port_handle=@{portHandles}[1]
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${topology_2_handle} =  Get From Dictionary  ${result}  topology_handle
	
# Creating a device group in topology 
	Log To Console  Creating device group 2 in topology 2
	${result} =  Topology Config  topology_handle=${topology_2_handle}  device_group_name=PTP Slave 1  device_group_multiplier=3  device_group_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${device_2_handle} =  Get From Dictionary  ${result}  device_group_handle
	
# CREATE ETHERNET STACK FOR PTP 2
	
	${result} =  Multivalue Config  pattern=counter  counter_start=00.24.01.00.00.01  counter_step=00.00.00.00.00.01  counter_direction=increment  nest_step=00.00.01.00.00.00  nest_owner=${topology_2_handle}  nest_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multivalue_2_handle} =  Get From Dictionary  ${result}  multivalue_handle
	
	Log To Console  Creating ethernet stack for the first Device Group
	${result} =  Interface Config  protocol_name=Ethernet 2  protocol_handle=${device_2_handle}  mtu=1500  src_mac_addr=${multivalue_2_handle}  vlan=1  vlan_id=101  vlan_id_step=1  vlan_id_count=1  vlan_tpid=0x8100  vlan_user_priority=0  vlan_user_priority_step=0  use_vpn_parameters=0  site_id=0
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ethernet_2_handle} =  Get From Dictionary  ${result}  ethernet_handle
	
# CREATE PTP STACK
	
	${result} =  Ptp Over Mac Config  parent_handle=${ethernet_2_handle}  profile=ieee1588  role=master  mode=create  name=PTP Slave  port_number=6323  communication_mode=multicast  domain=123  priority1=10  priority2=100
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ptp_slave} =  Get From Dictionary  ${result}  ptp_handle
	

	
############################################################################
# START PTP protocol                                                       #
############################################################################ 
	Log To Console  Starting PTP on topology1
	${result} =  Ptp Over Mac Control  handle=${ptp_master}  action=start
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	Log To Console  Starting PTP on topology2
	${result} =  Ptp Over Mac Control  handle=${ptp_slave}  action=connect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	${result} =  Test Control  action=start_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log To Console  Waiting for 30 seconds for all sessions to come up ...
	Sleep  30s
	
	
################################################################################
# Retrieve protocol statistics                                                 #
################################################################################
	Log  printing protocol statistics ...
	${protostats} =  Ptp Over Mac Stats  port_handle=@{portHandles}[0]  mode=aggregate  
	${status} =  Get From Dictionary  ${protostats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${protostats}
	
	Log  printing protocol statistics ...
	${protostats} =  Ptp Over Mac Stats  port_handle=@{portHandles}[1]  mode=aggregate  
	${status} =  Get From Dictionary  ${protostats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${protostats}

################################################################################
# Retrieve session statistics                                                 #
################################################################################
	Log  printing protocol statistics ...
	${protostats} =  Ptp Over Mac Stats  handle=${ptp_master}  mode=session  
	${status} =  Get From Dictionary  ${protostats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${protostats}
	
	Log  printing protocol statistics ...
	${protostats} =  Ptp Over Mac Stats  handle=${ptp_slave}  mode=session  
	${status} =  Get From Dictionary  ${protostats}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	Log  ${protostats}

	
############################################################################
# Stop all protocols                                                       #
############################################################################
	Log To Console  Stopping PTP on topology1
	${result} =  Ptp Over Mac Control  handle=${ptp_slave}  action=stop
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"

	Log To Console  Stopping PTP on topology2
	${result} =  Ptp Over Mac Control  handle=${ptp_master}  action=disconnect
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log  Stopping all protocols
	${result} =  Test Control  action=stop_all_protocols
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Sleep  2s
	Log  !!! Test Script Ends !!!