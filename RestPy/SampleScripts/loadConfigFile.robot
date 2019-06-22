*** Settings ***
Documentation  sample demonstrating traffic creation using ixnetwork_restpy and robot extended variable syntax
 
Library  BuiltIn
Library  Collections
Library  ixnetwork_restpy.testplatform.testplatform.TestPlatform  192.168.70.3  rest_port=11009


*** Variables ***
${apiServerIp} =  192.168.70.3
${apiServerPort} =  11009
${apiServerOs} =  windows
${forceTakePortOwnership} =  True
${debugMode} =  True
@{licenseServerIp} =  192.168.70.3
${licenseMode} =  subscription
${licenseTier} =  tier3  
${ixChassisIp} =  192.168.70.128
${configFile} =  bgp_ngpf_8.30.ixncfg

# Creating a list and nested list
@{port_1_1} =  ${ixChassisIp}  1  1
@{port_2_1} =  ${ixChassisIp}  2  1
@{portList} =  ${port_1_1}  ${port_2_1}
@{trackBy} =  flowGroup0  
@{EMPTYLIST} =  

*** Test Cases ***
Load a saved config file that configures BGP in NGPF

	Log To Console  Connecting ...
	${testPlatform} =  Get Library Instance  ixnetwork_restpy.testplatform.testplatform.TestPlatform
	${sessions} =   Set Variable  ${testPlatform.Sessions}
	${ixNetwork} =  Set Variable  ${sessions.find().Ixnetwork}

	Log To Console  New blank config ...
	Call Method  ${ixNetwork}  NewConfig
 	
	Log To Console  Loading config file: ${configFile} ...
        Import Library  ixnetwork_restpy.files.Files  ${configFile}  local_file=True  WITH NAME  fileObj
	${fileTransfer} =  Get Library Instance  fileObj
        Call Method  ${ixNetwork}  LoadConfig  ${fileTransfer}

	Log To Console  Configuring license details ...
	${ixNetwork.Globals.Licensing.LicensingServers} =  Set Variable  ${licenseServerIp}
        ${ixNetwork.Globals.Licensing.Mode} =  Set Variable  ${licenseMode}
        ${ixNetwork.Globals.Licensing.Tier} =  Set Variable  ${licenseTier}

	Log To Console  Assigning ports ...
        @{testPorts} =  Create List
        @{vportList} =  Create List

	:FOR  ${port}  IN  @{portList}
	\    &{portDict} =  Create Dictionary
	\    Set To Dictionary  ${portDict}  Arg1  @{port}[0]  Arg2  @{port}[1]  Arg3  @{port}[2]
	\    Append To List    ${testPorts}    ${portDict}

	:FOR  ${vport}  IN  @{ixNetwork.Vport.find()}
	\    Append To List  ${vportList}  ${vport.href}

	Call Method  ${ixNetwork}  AssignPorts  ${testPorts}  ${EMPTYLIST}  ${vportList}  ${forceTakePortOwnership} 
	
	Log To Console  Start all protocols
	Call Method  ${ixNetwork}  StartAllProtocols  sync

	Log To Console  Verifying protocol sessions
	Import Library  ixnetwork_restpy.assistants.statistics.statviewassistant.StatViewAssistant  ${ixNetwork}  Protocols Summary
	...  WITH NAME  protocolsSummaryObj
	${protocolsSummary} =  Get Library Instance  protocolsSummaryObj

	${result} =  Set Variable  ${protocolsSummary.CheckCondition('Sessions Not Started', '==', 0, RaiseException=False)}
	Run Keyword If  "${result}"=="False"  Run Keywords
	...  Fail  Protocol sessions not started

	${result} =  Set Variable  ${protocolsSummary.CheckCondition('Sessions Down', '==', 0, RaiseException=True)}

	Log To Console  ${protocolsSummary}

        ${trafficItem} =  Set Variable  ${ixNetwork.Traffic.TrafficItem.find()[0]}
	Call Method  ${trafficItem}  Generate
    	Call Method  ${ixNetwork.Traffic}  Apply

	Log To Console  Starting traffic
    	Call Method  ${ixNetwork.Traffic}  Start

	Import Library  ixnetwork_restpy.assistants.statistics.statviewassistant.StatViewAssistant  ${ixNetwork}  Flow Statistics
	...  WITH NAME  flowStatisticsObj
	${flowStatistics} =  Get Library Instance  flowStatisticsObj

	Log To Console  ${flowStatistics}
	Log To Console  TxFrames: ${flowStatistics.Rows[0]['Tx Frames']}
	Log To Console  RxFrames: ${flowStatistics.Rows[0]['Rx Frames']}
