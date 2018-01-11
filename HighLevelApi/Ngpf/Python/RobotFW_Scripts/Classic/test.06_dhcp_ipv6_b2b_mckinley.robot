*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxOS/QA_REGR/HLT3.40/DHCP/test.06_dhcp_ipv6_b2b_mckinley.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.232
${client_api_port} =  	8136
@{portlist} =  	12/1  12/2

*** Test Cases ***
test
################################################################################
# START - Connect to the chassis
################################################################################

	# Connect to the chassis and get port handles from the result
	${result} =  Connect  device=${chassis}  ixnetwork_tcl_server=${client}:${client_api_port}  port_list=@{portlist}  reset=1  mode=connect  break_locks=1  interactive=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	Log Many  @{portHandles}
#############################################
# IXIA EMULATION DHCP CONFIG FUNCTION     #
#############################################

	${result} =  Emulation Dhcp Config  port_handle=@{portHandles}[0]  mode=create  version=ixnetwork  no_write=0  reset=0  accept_partial_config=0  lease_time=3600  max_dhcp_msg_size=576  msg_timeout=4  outstanding_releases_count=500  outstanding_session_count=50  release_rate=50  release_rate_increment=50  request_rate=10  request_rate_increment=50  retry_count=3  server_port=67  wait_for_completion=0  dhcp6_echo_ia_info=0  dhcp6_reb_max_rt=600  dhcp6_reb_timeout=10  dhcp6_rel_max_rc=5  dhcp6_rel_timeout=1  dhcp6_ren_max_rt=600  dhcp6_ren_timeout=10  dhcp6_req_max_rc=5  dhcp6_req_max_rt=30  dhcp6_req_timeout=1  dhcp6_sol_max_rc=3  dhcp6_sol_max_rt=120  dhcp6_sol_timeout=1  msg_timeout_factor=2  override_global_setup_rate=1  override_global_teardown_rate=1  release_rate_max=500  request_rate_max=50
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_handles_0} =  Get From Dictionary  ${result}  handle
	
	
#############################################
# IXIA EMULATION DHCP CONFIG FUNCTION     #
#############################################
	
	${result} =  Emulation Dhcp Config  port_handle=@{portHandles}[1]  mode=create  version=ixnetwork  no_write=0  reset=0  accept_partial_config=0  lease_time=3600  max_dhcp_msg_size=576  msg_timeout=4  outstanding_releases_count=500  outstanding_session_count=50  release_rate=50  release_rate_increment=50  request_rate=10  request_rate_increment=50  retry_count=3  server_port=67  wait_for_completion=0  dhcp6_echo_ia_info=0  dhcp6_reb_max_rt=600  dhcp6_reb_timeout=10  dhcp6_rel_max_rc=5  dhcp6_rel_timeout=1  dhcp6_ren_max_rt=600  dhcp6_ren_timeout=10  dhcp6_req_max_rc=5  dhcp6_req_max_rt=30  dhcp6_req_timeout=1  dhcp6_sol_max_rc=3  dhcp6_sol_max_rt=120  dhcp6_sol_timeout=1  msg_timeout_factor=2  override_global_setup_rate=1  override_global_teardown_rate=1  release_rate_max=500  request_rate_max=50
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_handles_1} =  Get From Dictionary  ${result}  handle
	
#############################################
# IXIA EMULATION DHCP GROUP CONFIG FUNCTION #
#############################################
	
	${result} =  Emulation Dhcp Group Config  handle=${dhcp_handles_0}  mode=create  version=ixnetwork  target_subport=0  no_write=0  encap=ethernet_ii_vlan  mac_addr=00.00.01.00.00.01  mac_addr_step=00.00.01.00.00.01  num_sessions=10  qinq_incr_mode=both  vlan_id=4094  vlan_id_count=100  vlan_id_outer=10  vlan_id_outer_count=5  vlan_id_outer_step=7  vlan_id_step=3  vlan_id_outer_increment_step=2  vlan_id_outer_priority=0  vlan_user_priority=0  dhcp6_range_duid_enterprise_id=10  dhcp6_range_duid_type=duid_llt  dhcp6_range_duid_vendor_id=10  dhcp6_range_duid_vendor_id_increment=1  dhcp6_range_ia_id=10  dhcp6_range_ia_id_increment=1  dhcp6_range_ia_t1=302400  dhcp6_range_ia_t2=483840  dhcp6_range_ia_type=iana  dhcp6_range_param_request_list=2  dhcp_range_ip_type=ipv6  dhcp_range_param_request_list=2  dhcp_range_relay6_hosts_per_opt_interface_id=1  dhcp_range_relay6_opt_interface_id="id-[001-900]"  dhcp_range_relay6_use_opt_interface_id=0  dhcp_range_relay_address_increment=0.0.0.1  dhcp_range_relay_circuit_id=CIRCUITID-p  dhcp_range_relay_count=1  dhcp_range_relay_destination=20.0.0.1  dhcp_range_relay_first_address=20.0.0.100  dhcp_range_relay_first_vlan_id=1  dhcp_range_relay_gateway=20.0.0.1  dhcp_range_relay_hosts_per_circuit_id=1  dhcp_range_relay_hosts_per_remote_id=1  dhcp_range_relay_override_vlan_settings=0  dhcp_range_relay_remote_id=REMOTEID-I  dhcp_range_relay_subnet=24  dhcp_range_relay_use_circuit_id=0  dhcp_range_relay_use_remote_id=0  dhcp_range_relay_use_suboption6=0  dhcp_range_relay_vlan_count=1  dhcp_range_relay_vlan_increment=1  dhcp_range_renew_timer=0  dhcp_range_server_address=10.0.0.1  dhcp_range_suboption6_address_subnet=24  dhcp_range_suboption6_first_address=20.1.1.100  dhcp_range_use_first_server=1  dhcp_range_use_relay_agent=0  dhcp_range_use_trusted_network_element=0  mac_mtu=1500  server_id=7.7.7.7  use_vendor_id=0  vendor_id=Ixia
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_group_handles_0} =  Get From Dictionary  ${result}  handle
	
#############################################
# IXIA EMULATION DHCP GROUP CONFIG FUNCTION #
#############################################
	
	${result} =  Emulation Dhcp Group Config  handle=${dhcp_group_handles_0}  mode=modify  version=ixnetwork  target_subport=0  no_write=0  encap=ethernet_ii_qinq  mac_addr=00.aa.01.00.cc.01  mac_addr_step=00.00.00.00.01.01  num_sessions=10  qinq_incr_mode=outer  vlan_id=4094  vlan_id_count=100  vlan_id_outer=10  vlan_id_outer_count=5  vlan_id_outer_step=7  vlan_id_step=3  vlan_id_outer_increment_step=2  vlan_id_outer_priority=0  vlan_user_priority=0  dhcp6_range_duid_enterprise_id=10  dhcp6_range_duid_type=duid_llt  dhcp6_range_duid_vendor_id=10  dhcp6_range_duid_vendor_id_increment=1  dhcp6_range_ia_id=10  dhcp6_range_ia_id_increment=1  dhcp6_range_ia_t1=302400  dhcp6_range_ia_t2=483840  dhcp6_range_ia_type=iana  dhcp6_range_param_request_list=2  dhcp_range_ip_type=ipv6  dhcp_range_param_request_list=2  dhcp_range_relay6_hosts_per_opt_interface_id=1  dhcp_range_relay6_opt_interface_id="id-[001-900]"  dhcp_range_relay6_use_opt_interface_id=0  dhcp_range_relay_address_increment=0.0.0.1  dhcp_range_relay_circuit_id=CIRCUITID-p  dhcp_range_relay_count=1  dhcp_range_relay_destination=20.0.0.1  dhcp_range_relay_first_address=20.0.0.100  dhcp_range_relay_first_vlan_id=1  dhcp_range_relay_gateway=20.0.0.1  dhcp_range_relay_hosts_per_circuit_id=1  dhcp_range_relay_hosts_per_remote_id=1  dhcp_range_relay_override_vlan_settings=0  dhcp_range_relay_remote_id=REMOTEID-I  dhcp_range_relay_subnet=24  dhcp_range_relay_use_circuit_id=0  dhcp_range_relay_use_remote_id=0  dhcp_range_relay_use_suboption6=0  dhcp_range_relay_vlan_count=1  dhcp_range_relay_vlan_increment=1  dhcp_range_renew_timer=0  dhcp_range_server_address=10.0.0.1  dhcp_range_suboption6_address_subnet=24  dhcp_range_suboption6_first_address=20.1.1.100  dhcp_range_use_first_server=1  dhcp_range_use_relay_agent=0  dhcp_range_use_trusted_network_element=0  mac_mtu=1500  server_id=7.7.7.7  use_vendor_id=0  vendor_id=Ixia
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${dhcp_group_handles_1} =  Get From Dictionary  ${result}  handle
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	