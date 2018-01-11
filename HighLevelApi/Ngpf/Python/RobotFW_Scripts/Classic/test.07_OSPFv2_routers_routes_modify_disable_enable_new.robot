*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/OSPF/test.07_OSPFv2_routers_routes_modify_disable_enable_new.tcl
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
	
#################################################
#                                               #
# Configure interface in the test      			#
# IPv4                                 			#
#################################################
	
	${result} =  Interface Config  port_handle=@{portHandles}  autonegotiation=0  duplex=full
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#################################################
#                                               #
#  Configure n OSPFv2 neighbors                 #
#                                               #
#################################################
	
	${result} =  Emulation Ospf Config  port_handle=@{portHandles}[0]  reset=1  session_type=ospfv2  mode=create  count=1  mac_address_init=1000.0000.0001  intf_ip_addr=100.1.1.1  intf_ip_addr_step=0.0.1.0  router_id=1.1.1.1  router_id_step=0.0.1.0  neighbor_intf_ip_addr=100.1.1.2  neighbor_intf_ip_addr_step=0.0.1.0  neighbor_router_id=11.11.11.11  neighbor_router_id_step=0.0.1.0  vlan=1  vlan_id=1000  vlan_id_mode=fixed  vlan_id_step=5  area_id=0.0.0.1  area_id_step=0.0.0.1  area_type=ppp  authentication_mode=null  dead_interval=222  hello_interval=333  interface_cost=55  lsa_discard_mode=1  mtu=670  network_type=ptomp  router_priority=131  vlan_user_priority=5  enable_dr_bdr=1  option_bits=0x48
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospf_handle_list} =  Get From Dictionary  ${result}  handle
	
#################################################
#                                               #
#  Delete n OSPFv2 neighbors                    #
#                                               #
#################################################
	
	${result} =  Emulation Ospf Config  port_handle=@{portHandles}[0]  handle=${ospf_handle_list}  session_type=ospfv2  mode=delete
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#################################################
#                                               #
#  Configure n OSPFv2 neighbors                 #
#                                               #
#################################################
	
	${result} =  Emulation Ospf Config  port_handle=@{portHandles}[0]  reset=1  session_type=ospfv2  mode=create  count=1  mac_address_init=1000.0000.0001  intf_ip_addr=100.1.1.1  intf_ip_addr_step=0.0.1.0  router_id=1.1.1.1  router_id_step=0.0.1.0  neighbor_intf_ip_addr=100.1.1.2  neighbor_intf_ip_addr_step=0.0.1.0  neighbor_router_id=11.11.11.11  neighbor_router_id_step=0.0.1.0  vlan=1  vlan_id=1000  vlan_id_mode=fixed  vlan_id_step=5  area_id=0.0.0.1  area_id_step=0.0.0.1  area_type=external-capable  authentication_mode=null  dead_interval=222  hello_interval=333  interface_cost=55  lsa_discard_mode=1  mtu=670  network_type=broadcast  option_bits=0x48
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospf_handle_list} =  Get From Dictionary  ${result}  handle
	
#################################################
#                                               #
#  Modify n OSPFv2 neighbors                    #
#                                               #
#################################################
	
	${result} =  Emulation Ospf Config  port_handle=@{portHandles}[0]  handle=${ospf_handle_list}  session_type=ospfv2  mode=modify  area_type=ppp  network_type=ptomp  router_priority=131  vlan_user_priority=5  enable_dr_bdr=1  validate_received_mtu=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${ospf_handle_list} =  Get From Dictionary  ${result}  handle
	
#################################################
#                                               #
#  Disable n OSPFv2 neighbors                   #
#                                               #
#################################################
	
	${result} =  Emulation Ospf Config  port_handle=@{portHandles}[0]  handle=${ospf_handle_list}  session_type=ospfv2  mode=disable
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#################################################
#                                               #
#  Enable n OSPFv2 neighbors                    #
#                                               #
#################################################
	
	${result} =  Emulation Ospf Config  port_handle=@{portHandles}[0]  handle=${ospf_handle_list}  session_type=ospfv2  mode=enable
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#################################################
#                                               #
#  Create Topology Route - Router               #
#                                               #
#################################################
	
	${result} =  Emulation Ospf Topology Route Config  mode=create  handle=${ospf_handle_list}  type=router  router_id=123.1.1.1  router_abr=1  router_asbr=1  router_te=1  interface_ip_address=22.0.0.1  interface_ip_mask=255.255.0.0  link_type=external-capable
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${elem_handle} =  Get From Dictionary  ${result}  elem_handle
	
#################################################
#                                               #
#  Disable Topology Route - Router              #
#                                               #
#################################################
	
	${result} =  Emulation Ospf Config  port_handle=@{portHandles}[0]  handle=${ospf_handle_list}  session_type=ospfv2  mode=disable
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#################################################
#                                               #
#  Enable n OSPFv2 neighbors                    #
#                                               #
#################################################
	
	${result} =  Emulation Ospf Config  port_handle=@{portHandles}[0]  handle=${ospf_handle_list}  session_type=ospfv2  mode=enable
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#################################################
#                                               #
#  Create Topology Route - Router               #
#                                               #
#################################################
	
	${result} =  Emulation Ospf Topology Route Config  mode=create  handle=${ospf_handle_list}  type=router  router_id=123.1.1.1  router_abr=1  router_asbr=1  router_te=1  interface_ip_address=22.0.0.1  interface_ip_mask=255.255.0.0  link_type=external-capable
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${elem_handle} =  Get From Dictionary  ${result}  elem_handle
	
#################################################
#                                               #
#  Enable Topology Route - Router               #
#                                               #
#################################################
	
	${result} =  Emulation Ospf Topology Route Config  handle=${ospf_handle_list}  elem_handle=${elem_handle}  mode=disable  type=router
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#################################################
#                                               #
#  Enable n OSPFv2 neighbors                    #
#                                               #
#################################################
	
	${result} =  Emulation Ospf Topology Route Config  handle=${ospf_handle_list}  elem_handle=${elem_handle}  mode=enable  type=router
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#################################################
#                                               #
#  Create External Topology Route - Router      #
#                                               #
#################################################
	
	${result} =  Emulation Ospf Topology Route Config  mode=create  handle=${ospf_handle_list}  type=ext_routes  external_ip_type=ipv4  no_write=1  external_address_family=multicast  external_prefix_start=10.0.0.31
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
	
	
	
	
	
	
	
	
	
	