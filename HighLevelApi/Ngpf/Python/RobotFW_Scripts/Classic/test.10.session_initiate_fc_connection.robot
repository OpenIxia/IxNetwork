*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.147/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.147/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.60/FC/test.10.session_initiate_fc_connection.tcl
# Topology 2P-B2B
*** Variables ***
${chassis} =  	10.215.133.218
${client} =  	10.215.133.232
${client_api_port} =  	8136
@{portlist} =  	9/1  9/2

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
	${fc_client_port_handle} =  Set Variable  @{portHandles}[0]
	${fc_fport_port_handle} =  Set Variable  @{portHandles}[1]

#========================== ADD CLIENT =======================================#

	Log To Console  Adding client ...
	${result} =  Fc Client Config  mode=add  port_handle=${fc_client_port_handle}  flogi_count=1  flogi_plogi_enabled=1  flogi_name=FLOGI-NAME
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${fc_client_handle} =  Get From Dictionary  ${result}  handle
	
#================================ ADD FPORT ==================================#
	
	Log To Console  Adding F-PORT ...
	${result} =  Fc Fport Config  mode=add  port_handle=${fc_fport_port_handle}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${fc_fport_handle} =  Get From Dictionary  ${result}  handle
	
#========================== ADD VNPORT =======================================#
	
	Log To Console  Adding vnport ...
	${result} =  Fc Fport Vnport Config  mode=add  handle=${fc_fport_handle}  count=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${fc_fport_vnport_handle} =  Get From Dictionary  ${result}  handle
	
#========================== ADD VNPORT FOR FLOGI =============================#
	
	Log To Console  Adding vnport for FLOGI...
	${result} =  Fc Fport Vnport Config  mode=add  handle=${fc_fport_handle}  name=N_PORT-FLOGI  simulated=1  plogi_enable=1  plogi_target_name=FLOGI-NAME  count=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${fc_fport_vnport_flogi_handle} =  Get From Dictionary  ${result}  handle
	
#========================= CONFIG CLIENT TO PLOGI TO FPORT ===================#
	
	Log To Console  Config client ...
	${result} =  Fc Client Config  mode=modify  handle=${fc_client_handle}  flogi_plogi_target_name=N_PORT-FLOGI  flogi_prli_enabled=1
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
#============================ START F-PORT and CLIENT-PORT ===================#
	
	Log To Console  Start session in sync mode...
	${result} =  Fc Control  action=start  port_handle=@{portHandles}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	Log To Console  Wait 10 seconds for the sessions to come up
	Sleep  10s
	
#============================ VERIFY STATISTICS ==============================#
	Log To Console  Verify Session by Statistics ... 
#============================ For Client Port ================================#
	Log To Console  Compare statistics for Client Port
	${result} =  Fc Client Stats  mode=aggregate  port_handle=@{portHandles}
	
	Log To Console  Wait 5 seconds to get aggregate stats for client
	Sleep  5s
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	