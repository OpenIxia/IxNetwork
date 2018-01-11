*** Settings ***
Library  BuiltIn
Library  String
Library  Collections

Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic


# Based on script: /home/HLT-Regression/REG_TEST/feature-test/IxOS/QA_REGR/HLT3.40/ANCP/test.01_ANCP_over_IPv4_heavenly.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.232
${client_api_port} =  	8136
@{portlist} =  	12/1  12/2
${client_and_port} =  ${client}:${client_api_port}

*** Test Cases ***
test
	# Connect to the chassis and get port handles from the result
	${result} =  Connect  api=classic  device=${chassis}  ixnetwork_tcl_server=${client_and_port}  port_list=@{portlist}  reset=1
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	Log Many  @{portHandles}
	
	# Configure interfaces
	${result} =  Interface Config  api=classic  mode=modify  port_handle=@{portHandles}[0]  src_mac_addr=0001.0012.0001  atm_encapsulation=LLCRoutedCLIP  vpi=0  vci=32  intf_ip_addr=20.20.0.1  gateway=20.20.0.2  netmask=255.255.255.0  l23_config_type=static_endpoint
	${intf1Handle} =  Get From Dictionary  ${result}  interface_handle
	${result} =  Interface Config  api=classic  mode=modify  port_handle=@{portHandles}[1]  src_mac_addr=0001.0012.0002  atm_encapsulation=LLCRoutedCLIP  vpi=0  vci=32  intf_ip_addr=20.20.0.2  gateway=20.20.0.1  netmask=255.255.255.0  l23_config_type=static_endpoint
	${intf2Handle} =  Get From Dictionary  ${result}  interface_handle
	
	#configure ANCP intf1
	${result} =  Emulation Ancp Config  api=classic  device_count=10  handle=intf1Handle  mode=create  port_handle=@{portHandles}[0]  ancp_standard=ietf-ancp-protocol2  events_per_interval=10  global_port_down_rate=50  global_port_up_rate=10  global_resync_rate=50  gsmp_standard=gsmp-v3-base  interval=1  line_config=0  port_down_rate=50  port_resync_rate=50  port_up_rate=50  port_override_globals=1  topology_discovery=1  access_aggregation=0  access_aggregation_dsl_inner_vlan=1  access_aggregation_dsl_inner_vlan_type=actual_dsl_subscriber_vlan  access_aggregation_dsl_outer_vlan=1  access_aggregation_dsl_outer_vlan_type=actual_dsl_subscriber_vlan  circuit_id=circuit  keep_alive=10000  keep_alive_retries=3  sut_ip_addr=20.20.0.2  sut_service_port=6068  distribution_alg_percentage=0  gateway_incr_mode=every_subnet  gateway_ip_addr=0.0.0.0  gateway_ip_prefix_len=16  gateway_ip_step=0.0.0.0  intf_ip_addr=45.23.8.1  intf_ip_prefix_len=16  intf_ip_step=0.0.0.1  local_mss=1460  encap_type=ETHERNETII  local_mac_addr=000a.0abc.0200  local_mac_step=0000.0000.0001  local_mac_addr_auto=0  local_mtu=1500  qinq_incr_mode=both  vlan_id=11  vlan_id_count=1  vlan_id_count_inner=1  vlan_id_inner=1  vlan_id_repeat=1  vlan_id_repeat_inner=1  vlan_id_step=1  vlan_id_step_inner=1  vlan_user_priority=0  vlan_user_priority_inner=0  pvc_incr_mode=both  vci=32  vci_count=4053  vci_repeat=1  vci_step=1  vpi=0  vpi_count=1  vpi_repeat=1  vpi_step=1
	${ANCP_config_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ANCP_config_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ANCP_handle1} =  Get From Dictionary  ${result}  handle
	
	#configure ANCP intf2
	${result} =  Emulation Ancp Config  api=classic  device_count=10  handle=intf2Handle  mode=create  port_handle=@{portHandles}[1]  ancp_standard=ietf-ancp-protocol2  events_per_interval=10  global_port_down_rate=50  global_port_up_rate=10  global_resync_rate=50  gsmp_standard=gsmp-v3-base  interval=1  line_config=0  port_down_rate=50  port_resync_rate=50  port_up_rate=50  port_override_globals=1  topology_discovery=1  access_aggregation=0  access_aggregation_dsl_inner_vlan=1  access_aggregation_dsl_inner_vlan_type=actual_dsl_subscriber_vlan  access_aggregation_dsl_outer_vlan=1  access_aggregation_dsl_outer_vlan_type=actual_dsl_subscriber_vlan  circuit_id=circuit  keep_alive=10000  keep_alive_retries=3  sut_ip_addr=20.20.0.2  sut_service_port=6068  distribution_alg_percentage=0  gateway_incr_mode=every_subnet  gateway_ip_addr=0.0.0.0  gateway_ip_prefix_len=16  gateway_ip_step=0.0.0.0  intf_ip_addr=10.10.0.1  intf_ip_prefix_len=16  intf_ip_step=0.0.0.1  local_mss=1460  encap_type=ETHERNETII  local_mac_addr=000b.0b00.0200  local_mac_step=0000.0000.0001  local_mac_addr_auto=0  local_mtu=1500  qinq_incr_mode=both  vlan_id=11  vlan_id_count=1  vlan_id_count_inner=1  vlan_id_inner=1  vlan_id_repeat=1  vlan_id_repeat_inner=1  vlan_id_step=1  vlan_id_step_inner=1  vlan_user_priority=0  vlan_user_priority_inner=0  pvc_incr_mode=both  vci=32  vci_count=4053  vci_repeat=1  vci_step=1  vpi=0  vpi_count=1  vpi_repeat=1  vpi_step=1
	${ANCP_config_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${ANCP_config_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ANCP_handle2} =  Get From Dictionary  ${result}  status
################################################################################
# End ANCP Call
################################################################################
