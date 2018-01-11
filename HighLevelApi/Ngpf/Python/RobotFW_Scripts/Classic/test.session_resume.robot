*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.104/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.104/PythonApi  classic

# Based on script: /home/HLT-Regression/REG_TEST/feature-test/IxN/QA_REGR/HLT4.70/Session_resume_filters/test.220_ANCP_over_IPv4.tcl
# Topology 1P-B2B
*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.144
${client_api_port} =  	8136
@{portlist} =  	12/9

${ixn_cfg} =  	/home/pythar/ROBOT/protocols\ test\ cases/220_ANCP_over_IPv4.ixncfg
${list_resume_filters} =  emulation_ancp_config  emulation_ancp_subscriber_lines_config

*** Test Cases ***
test
	# Connect to the chassis and get port handles from the result
	${result} =  Connect  config_file=${ixn_cfg}  device=${chassis}  ixnetwork_tcl_server=${client}:${client_api_port}  port_list=@{portlist}  mode=connect  session_resume_include_filter=${list_resume_filters}
	${connect_status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${connect_status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	${portHandles} =  Split String  ${vport_list}
	Log Many  ${portHandles}[0]
	
	
	
	${filtered_handles_port_0} =  Get Dictionary Keys  ${result${portHandles}} 
	
	Run Keyword If  ${filtered_handles_port_0} != ['emulation_ancp_config', 'emulation_ancp_subscriber_lines_config']  FAIL  "Some ANCP keys returned are missing: EXPECTED -> emulation_ancp_config emulation_ancp_subscriber_lines_config; RETURNED -> ${filtered_handles_port_0}"  ELSE  Log  "ANCP keys returned are correct"

	${filtered_handles_port_1} =  Set Variable  ${result${portHandles}['emulation_ancp_config']['handle']}
	
	Run Keyword If  '${filtered_handles_port_1}' != '::ixNet::OBJ-/vport:1/protocolStack/ethernet:\\"825aac4e-f94d-4867-9d65-de7d8ab98c69\\"/ipEndpoint:\\"77d4f1e6-05ca-4c82-b7c5-9cea2ce2aede\\"/range:\\"973e55d1-651b-490e-ba87-8aa2f7117e81\\"/ancpRange:1'  FAIL  "the ANCP config handle returned is wrong; EXPECTED ->"  ELSE  Log  "the ANCP config handle returned is correct"
	
	${filtered_handles_port_2} =  Set Variable  ${result${portHandles}['emulation_ancp_subscriber_lines_config']['handle']}
	
	Run Keyword If  '${filtered_handles_port_2}' != '::ixNet::OBJ-/globals/protocolStack/ancpGlobals:1/ancpDslProfile:\\"c23ad765-51eb-4411-a789-8de0b621a3cb\\"\' != \'::ixNet::OBJ-/globals/protocolStack/ancpGlobals:1/ancpDslProfile:"c23ad765-51eb-4411-a789-8de0b621a3cb\"'  FAIL  "the ANCP config handle returned is wrong; EXPECTED ->"  ELSE  Log  "the ANCP config handle returned is correct"
	