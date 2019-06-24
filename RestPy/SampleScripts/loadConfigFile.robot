*** Settings ***
Documentation  sample demonstrating traffic creation using ixnetwork_restpy and robot extended variable syntax

...  loadConfigFile.robot

...  Tested with two back-2-back Ixia ports
...     - Connect to the API server
...     - Configure license server IP
...     - Loads a saved config file
...     - Configure license server IP
...     - Optional: Assign ports or use the ports that are in the saved config file.
...     - Start all protocols
...     - Verify all protocols
...     - Start traffic 
...     - Get Traffic Item
...     - Get Flow Statistics stats

...  Supports IxNetwork API servers:
...     - Windows, Windows Connection Mgr and Linux

...  Requirements
...     - RestPy 1.0.33   
...     - IxNetwork 8.50
...     - Python 2.7 and 3+
...     - pip install requests
...     - pip install -U --no-cache-dir ixnetwork_restpy

...  RestPy Doc:
...      https://www.openixia.com/userGuides/restPyDoc

 
Library  BuiltIn
Library  Collections

*** Variables ***
${apiServerIp} =  192.168.70.12

# For Linux API server only
${username} =  admin
${password} =  admin

# Forcefully take port ownership if the portList are owned by other users.
${forceTakePortOwnership} =  True

@{licenseServerIp} =  192.168.70.3
${licenseMode} =  subscription
${licenseTier} =  tier3  

${configFile} =  bgp_ngpf_8.30.ixncfg

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
${debugMode} =  False

# Create a list and nested list
${ixChassisIp} =  192.168.70.128
@{port_1_1} =  ${ixChassisIp}  1  1
@{port_2_1} =  ${ixChassisIp}  2  1
@{portList} =  ${port_1_1}  ${port_2_1}

@{trackBy} =  flowGroup0
@{EMPTYLIST} =  

*** Test Cases ***
Load a saved config file that configures BGP in NGPF

	Log To Console  Connecting ...

	# If using RestPy version < 1.0.33, uncomment this.  Backward compatibility still works, but
	# the parameters rest_port and platform are deprecated.
	#Import Library  ixnetwork_restpy.testplatform.testplatform.TestPlatform  
	#...  ${apiServerIp}  rest_port=11009  platform=windows  log_file_name=restpy.log  WITH NAME  testPlatformObj

	# If using RestPy version >= 1.0.33
	Import Library  ixnetwork_restpy.testplatform.testplatform.TestPlatform  ${apiServerIp}  log_file_name=restpy.log  WITH NAME  testPlatformObj

	${testPlatform} =  Get Library Instance  testPlatformObj
	Call Method  ${testPlatform}  Authenticate  ${username}  ${password}
        ${session} =  Set Variable  ${testPlatform.Sessions.add()}
	${ixNetwork} =  Set Variable  ${session.find().Ixnetwork}

	Log To Console  New blank config ...
	Call Method  ${ixNetwork}  NewConfig

	Log To Console  Configuring license details ...
	${ixNetwork.Globals.Licensing.LicensingServers} =  Set Variable  ${licenseServerIp}
        ${ixNetwork.Globals.Licensing.Mode} =  Set Variable  ${licenseMode}
        ${ixNetwork.Globals.Licensing.Tier} =  Set Variable  ${licenseTier}
 	
	Log To Console  Loading config file: ${configFile} ...
        Import Library  ixnetwork_restpy.files.Files  ${configFile}  local_file=True  WITH NAME  fileObj
	${fileTransfer} =  Get Library Instance  fileObj
        Call Method  ${ixNetwork}  LoadConfig  ${fileTransfer}

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

        # Note: Using Call Method to remove the session doesn't work.
	${status} =  Run Keyword If  "${debugMode}"=="False"   Set Variable  ${session.remove()}  
