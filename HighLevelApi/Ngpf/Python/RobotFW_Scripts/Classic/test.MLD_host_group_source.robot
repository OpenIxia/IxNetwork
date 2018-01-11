*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/DEV_REGR/Routing/MLD/test.MLD_host_group_source.tcl
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
#  Configure 2 MLD hosts on interface           #
#  MLD Version 2                                #
#################################################
	
	${result} =  Emulation Mld Config  mode=create  port_handle=@{portHandles}[0]  mld_version=v2  count=10  intf_ip_addr=30::31  intf_prefix_len=64  msg_interval=10  max_groups_per_pkts=5  unsolicited_report_interval=30  general_query=1  group_query=1  max_response_control=1  max_response_time=0  ip_router_alert=1  suppress_report=1  mac_address_init=0000.0000.0001  reset=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${mld_host_handle_list} =  Get From Dictionary  ${result}  handle
	@{mld_host_handle_list} =  Split String  ${mld_host_handle_list}
#####################################################################
#  Configure 2 MLD groups on each MLD hosts  on interface           #
#  MLD Version 2                                                    #
#####################################################################
# Set multicast group
	${result} =  Emulation Multicast Group Config  mode=create  num_groups=2  ip_addr_start=FF15::1  ip_addr_step=0::1  ip_prefix_len=64  
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multicast_group_handle} =  Get From Dictionary  ${result}  handle
	
# Set multicast sources
	
	${result} =  Emulation Multicast Source Config  mode=create  num_sources=5  ip_addr_start=20::21  ip_addr_step=0::1  ip_prefix_len=64  
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${multicast_source_handle} =  Get From Dictionary  ${result}  handle
	
#####################################################################
#  Configure 5 MLD sources on each MLD groups for each MLD host     #
#  MLD Version 2                                                    #
#####################################################################
	
	:FOR  ${mld_host_handle}  IN  @{mld_host_handle_list}
	\  Log  Stats on current port are: ${mld_host_handle}
	\  ${result} =  Emulation Mld Group Config  mode=create  session_handle=${mld_host_handle}  group_pool_handle=${multicast_group_handle}  source_pool_handle=${multicast_source_handle}
	\  ${status} =  Get From Dictionary  ${result}  status
	\  Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
######################
# START MLD          #
######################
	
	${result} =  Emulation Mld Control  mode=start  port_handle=@{portHandles}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
