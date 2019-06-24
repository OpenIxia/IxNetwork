*** Settings ***
Documentation  sample demonstrating traffic creation using ixnetwork_restpy and robot extended variable syntax

...  bgpNgpf.robot

...  Tested with two back-2-back Ixia ports

...   - Connect to the API server
...   - Configure license server IP
...   - Optional: Assign ports or use the ports that are in the saved config file.
...   - Configure two IPv4 BGP in NGPF with network advertisements
...   - Start all protocols
...   - Verify all protocols
...   - Start traffic 
...   - Get Traffic Item
...   - Get Flow Statistics stats

...  Supports IxNetwork API servers:
...   - Windows, Windows Connection Mgr and Linux

...  Requirements
...   - RestPy 1.0.33   
...   - IxNetwork 8.50
...   - Python 2.7 and 3+
...   - pip install requests
 ...  - pip install -U --no-cache-dir ixnetwork_restpy

...  RestPy Doc:
...    https://www.openixia.com/userGuides/restPyDoc


Library  BuiltIn
Library  Collections

*** Variables ***
${apiServerIp} =  192.168.70.3

# For Linux API server only
${username} =  admin
${password} =  admin

# Forcefully take port ownership if the portList are owned by other users.
${forceTakePortOwnership} =  True

@{licenseServerIp} =  192.168.70.3
${licenseMode} =  subscription
${licenseTier} =  tier3  

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
Configure BGP in NGPF

	Log To Console  Connecting ...

	# If you are using RestPy version < 1.0.33, uncomment this.  Backward compatibility still works, but
	# the parameters rest_port and platform are deprecated.
	#Import Library  ixnetwork_restpy.testplatform.testplatform.TestPlatform  
	#...  ${apiServerIp}  rest_port=11009  platform=winodws  log_file_name=restpy.log  WITH NAME  testPlatformObj

	# For RestPy version >= 1.0.33
	Import Library  ixnetwork_restpy.testplatform.testplatform.TestPlatform  ${apiServerIp}  log_file_name=restpy.log  WITH NAME  testPlatformObj

	${testPlatform} =  Get Library Instance  testPlatformObj
	Call Method  ${testPlatform}  Authenticate  ${username}  ${password}
        ${session} =  Set Variable  ${testPlatform.Sessions.add()}
	Log To Console  sessionId ${session}
	${ixNetwork} =  Set Variable  ${session.Ixnetwork}

	Log To Console  New blank config ...
	Call Method  ${ixNetwork}  NewConfig

	Log To Console  Configuring license details ...
	${ixNetwork.Globals.Licensing.LicensingServers} =  Set Variable  ${licenseServerIp}
        ${ixNetwork.Globals.Licensing.Mode} =  Set Variable  ${licenseMode}
        ${ixNetwork.Globals.Licensing.Tier} =  Set Variable  ${licenseTier}

	${vport1} =  Set Variable  ${ixNetwork.Vport.add(Name='Port1')}
	${vport2} =  Set Variable  ${ixNetwork.Vport.add(Name='Port2')}

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
	
	Log To Console  Create Topology 1
	${topology1} =  Set Variable  ${ixNetwork.Topology.add(Name='Topo1')}
	${topology1.Ports} =  Set Variable  ${vport1}

	Log To Console  Create Device Group
    	${deviceGroup1} =  Set Variable  ${topology1.DeviceGroup.add(Name='DG1', Multiplier=1)}

	Log To Console  Create Ethernet
   	${ethernet1} =  Set Variable  ${deviceGroup1.Ethernet.add(Name='Eth1')}
    	Call Method  ${ethernet1.Mac}  Increment  start_value=00:01:01:01:00:01  step_value=00:00:00:00:00:01

	Log To Console  Enabling Vlan
    	Call Method  ${ethernet1.EnableVlans}  Single  True
	${vlanObj} =  Set Variable  ${ethernet1.Vlan.find()[0]}
	Call Method  ${vlanObj.VlanId}  Increment  start_value=103  step_value=0

    	Log To Console  Configuring IPv4-1
    	${ipv4_1} =  Set Variable  ${ethernet1.Ipv4.add(Name='Ipv4-1')}
    	Call Method  ${ipv4_1.Address}  Increment  start_value=1.1.1.1  step_value=0.0.0.1
    	Call Method  ${ipv4_1.GatewayIp}  Increment  start_value=1.1.1.2  step_value=0.0.0.0

	Log To Console  Configuring BgpIpv4Peer 1
    	${bgp1} =  Set Variable  ${ipv4_1.BgpIpv4Peer.add(Name='Bgp1')}
    	Call Method  ${bgp1.DutIp}  Increment  start_value=1.1.1.2  step_value=0.0.0.0
    	Call Method  ${bgp1.Type}  Single  internal
    	Call Method  ${bgp1.LocalAs2Bytes}  Increment  start_value=101  step_value=0

    	Log To Console  Configuring Network Group 1
    	${networkGroup1} =  Set Variable  ${deviceGroup1.NetworkGroup.add(Name='BGP-Routes1', Multiplier=100)}
    	${ipv4PrefixPool} =  Set Variable  ${networkGroup1.Ipv4PrefixPools.add(NumberOfAddresses=1)}
    	Call Method  ${ipv4PrefixPool.NetworkAddress}  Increment  start_value=10.10.0.1  step_value=0.0.0.1
    	Call Method  ${ipv4PrefixPool.PrefixLength}  Single  32

	Log To Console  Create Topology 2
	${topology2} =  Set Variable  ${ixNetwork.Topology.add(Name='Topo2')}
	${topology2.Ports} =  Set Variable  ${vport2}

	Log To Console  Create Device Group 2
    	${deviceGroup2} =  Set Variable  ${topology2.DeviceGroup.add(Name='DG2', Multiplier=1)}

	Log To Console  Create Ethernet 2
   	${ethernet2} =  Set Variable  ${deviceGroup2.Ethernet.add(Name='Eth2')}
    	Call Method  ${ethernet2.Mac}  Increment  start_value=00:01:02:01:00:01  step_value=00:00:00:00:00:01

	Log To Console  Enabling Vlan 2
    	Call Method  ${ethernet2.EnableVlans}  Single  True
	${vlanObj} =  Set Variable  ${ethernet2.Vlan.find()[0]}
	Call Method  ${vlanObj.VlanId}  Increment  start_value=103  step_value=0

    	Log To Console  Configuring IPv4 2
    	${ipv4_2} =  Set Variable  ${ethernet2.Ipv4.add(Name='Ipv4-2')}
    	Call Method  ${ipv4_2.Address}  Increment  start_value=1.1.1.2  step_value=0.0.0.1

    	Call Method  ${ipv4_2.GatewayIp}  Increment  start_value=1.1.1.1  step_value=0.0.0.0
	Log To Console  Configuring BgpIpv4Peer 2
    	${bgp2} =  Set Variable  ${ipv4_2.BgpIpv4Peer.add(Name='Bgp1')}
    	Call Method  ${bgp2.DutIp}  Increment  start_value=1.1.1.1  step_value=0.0.0.0
    	Call Method  ${bgp2.Type}  Single  internal
    	Call Method  ${bgp2.LocalAs2Bytes}  Increment  start_value=101  step_value=0

    	Log To Console  Configuring Network Group 2
    	${networkGroup2} =  Set Variable  ${deviceGroup2.NetworkGroup.add(Name='BGP-Routes2', Multiplier=100)}
    	${ipv4PrefixPool2} =  Set Variable  ${networkGroup2.Ipv4PrefixPools.add(NumberOfAddresses=1)}
    	Call Method  ${ipv4PrefixPool2.NetworkAddress}  Increment  start_value=20.10.0.1  step_value=0.0.0.1
    	Call Method  ${ipv4PrefixPool2.PrefixLength}  Single  32

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

	Log To Console  Create Traffic Item
	${trafficItem} =  Set Variable  ${ixnetwork.Traffic.TrafficItem.add(Name='BGP', TrafficType='ipv4')}

	Log To Console  Add Endpoints
	${endpoint} =  Set Variable  ${trafficItem.EndpointSet.add(Sources=['${networkGroup1.href}'], Destinations=['${networkGroup2.href}'])}

	${configElement} =  Set Variable  ${trafficItem.ConfigElement.find()[0]}
    	${configElement.FrameRate.Rate} =  Set Variable  28
    	${configElement.FrameRate.Type} =  Set Variable  framesPerSecond
    	${configElement.TransmissionControl.FrameCount} =  Set Variable  10000
        ${configElement.TransmissionControl.Type} =  Set Variable  fixedFrameCount
    	${configElement.FrameSize.FixedSize} =  Set Variable  128
    	${configElement.FrameRateDistribution.PortDistribution} =  Set Variable  splitRateEvenly

    	${tracking} =  Set Variable  ${trafficItem.Tracking.find()[0]}
	${tracking.TrackBy} =  Set Variable  ${trackBy}

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


