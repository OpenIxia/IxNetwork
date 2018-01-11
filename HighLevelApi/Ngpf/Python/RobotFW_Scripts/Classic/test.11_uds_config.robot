*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  IxHLRobot  /home/builds/ixNetwork-8.20.0.161/hltapi/library/common/ixiangpf/python  /home/builds/ixNetwork-8.20.0.161/PythonApi  classic

# Based on script: //hltapi/QA/pythar_regression_scripts/IxN/QA_REGR/HLT4.80/Legacy_scripts_for_full_coverage/PPP/test.6_LEGACY_IxNetwork_PPPoE_missing_intermediate_agent_dependencies.tcl
# Topology 1P-B2B

*** Variables ***
${chassis} =  	10.215.133.158
${client} =  	10.215.133.232
${client_api_port} =  	8136
@{portlist} =  	12/1

*** Test Cases ***
test
################################################################################
# START - Connect to the chassis
################################################################################

	# Connect to the chassis and get port handles from the result
	${result} =  Connect  device=${chassis}  ixnetwork_tcl_server=${client}:${client_api_port}  port_list=@{portlist}  reset=1  vport_count=1  tcl_server=${chassis}
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	${vport_list} =  Get From Dictionary  ${result}  vport_list
	@{portHandles} =  Split String  ${vport_list}
	Log Many  @{portHandles}
################################################################################
# END - Connect to the chassis
################################################################################
	
########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
	
	${result} =  Interface Config  port_handle=@{portHandles}  port_rx_mode=capture
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
##########################
#  packet_config_filter
##########################

# using the pattern1* parameters that will match the predefined match_type1 settings
	
	${result} =  Uds Filter Pallette Config  port_handle=@{portHandles}  pattern1=0C 01  DA1=00:de:ad:be:ef:00  DA2=ba:ba:fa:ce:ca:ca  DA_mask1=0000.0000.11ff  DA_mask2=0000.0000.ff11  pattern2=aa bb cc dd ee ff 00 11 22  pattern_mask2=ff ff 11 22 00 00 00 00 00  pattern_offset2=66  pattern_offset_type2=startOfIp  SA1=0000.1111.2222  SA2=1111.2222.3333  SA_mask1=11 11 00 00 00 00  SA_mask2=aa bb cc dd 00 00
	${status} =  Get From Dictionary  ${result}  status
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
##########################
#  uds_config_triggers
##########################
	
	${result} =  Uds Config  port_handle=  uds1=1  uds1_SA=notSA2  uds1_DA=notDA2  uds1_error=errAnyFrame  uds1_framesize=undersized  uds1_pattern=pattern1  uds2=1  uds2_SA=SA2  uds2_DA=DA2  uds2_error=errBadFrame  uds2_framesize=0  uds2_pattern=notPattern2  uds3=1  uds3_SA=notSA2  uds3_DA=notDA2  uds3_error=errAnyFrame  uds3_framesize=undersized  uds3_pattern=pattern1  uds4=1  uds4_SA=SA2  uds4_DA=DA2  uds4_error=errBadFrame  uds4_framesize=oversized  uds4_pattern=pattern2  uds5=1  uds5_SA=notSA1  uds5_DA=DA1  uds5_error=errGoodFrame  uds5_framesize=jumbo  uds5_pattern=pattern1  uds6=1  uds6_SA=notSA2  uds6_DA=notDA2  uds6_error=errAnyFrame  uds6_framesize=undersized  uds6_pattern=pattern1
	Run Keyword If  '${status}' != '1'  FAIL  "Error: Status is not SUCCESS"  ELSE  Log  "Status is SUCCESS"
	
	
