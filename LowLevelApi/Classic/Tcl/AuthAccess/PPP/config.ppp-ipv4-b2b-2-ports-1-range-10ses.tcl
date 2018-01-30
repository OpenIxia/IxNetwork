# TCL script modified by TCL Script Doctor on 10/29/2008 5:40:51 PM
###################################################################################
# The procedure below is generated from Script Gen utility. The steps to generate
# Chassis/Card/Port independent utility is
# (1) Create the configuration manually in the GUI
# (2) Unassign all ports
# (3) Delete the chassis from the chassis list
# (4) Then generate the scripts corresponding to the protocol from
#     Tools --> Scriptgen
# (5) The heart of the generated script is the ixNetScriptgenProc {}, which is
#     represented below
# (6) NOTE:- One need not have to modify anything inside the ixNetScriptgenProc {}
###################################################################################

proc ixNetScriptgenProc {} {
ixNet rollback
ixNet execute newConfig
set ixNetSG_Stack(0) [ixNet getRoot]

#
# setting global options
#
set sg_top [ixNet getRoot]
ixNet setAttribute $sg_top/availableHardware -isOffChassis False
ixNet setAttribute $sg_top/availableHardware -offChassisHwM {}
ixNet setAttribute $sg_top/globals/interfaces -arpOnLinkup True
ixNet setAttribute $sg_top/traffic -refreshLearnedInfoBeforeApply True
ixNet setAttribute $sg_top/traffic -globalIterationMode continuous
ixNet setAttribute $sg_top/traffic -enableMinFrameSize False
ixNet setAttribute $sg_top/traffic -enableStaggeredTransmit False
ixNet setAttribute $sg_top/traffic -latencyBinType cutThroughLatency
ixNet setAttribute $sg_top/traffic -waitTime 1
ixNet setAttribute $sg_top/traffic -enableStreamOrdering False
ixNet setAttribute $sg_top/traffic -globalIterationCount 1
ixNet setAttribute $sg_top/testConfiguration -productLabel {Your switch/router name here}
ixNet setAttribute $sg_top/testConfiguration -enableAbortIfLinkDown False
ixNet setAttribute $sg_top/testConfiguration -enableGenerateReportAfterRun False
ixNet setAttribute $sg_top/testConfiguration -enableCheckLinkState False
ixNet setAttribute $sg_top/testConfiguration -enableSwitchToResult False
ixNet setAttribute $sg_top/testConfiguration -enableRebootCpu False
ixNet setAttribute $sg_top/testConfiguration -selectedSuite custom
ixNet setAttribute $sg_top/testConfiguration -version {Your firmware version here}
ixNet setAttribute $sg_top/testConfiguration -enableCapture False
ixNet setAttribute $sg_top/testConfiguration -serialNumber {Your switch/router serial number here}
ixNet setAttribute $sg_top/testConfiguration -sleepTimeAfterReboot 10
ixNet setAttribute $sg_top/testConfiguration -comments {}
ixNet setAttribute $sg_top/testConfiguration -linkDownTimeout 5
ixNet commit
set sg_top [lindex [ixNet remapIds $sg_top] 0]
set ixNetSG_Stack(0) $sg_top

###
### /vport area
###

#
# configuring the object that corresponds to /vport:1
#
set sg_vport [ixNet add $ixNetSG_Stack(0) vport]
ixNet setAttribute $sg_vport -type ethernet
ixNet setAttribute $sg_vport -isPullOnly False
ixNet setAttribute $sg_vport -name {Ethernet - 001}
ixNet setAttribute $sg_vport -txMode sequential
ixNet setAttribute $sg_vport -txGapControlMode fixedMode
ixNet setAttribute $sg_vport -connectedTo [ixNet getNull]
ixNet setAttribute $sg_vport -rxMode measure
ixNet setAttribute $sg_vport/l1Config -currentType ethernet
ixNet setAttribute $sg_vport/capture -hardwareEnabled False
ixNet setAttribute $sg_vport/capture -softwareEnabled False
ixNet setAttribute $sg_vport/protocols/arp -enabled False
ixNet setAttribute $sg_vport/protocols/bfd -enabled False
ixNet setAttribute $sg_vport/protocols/bfd -intervalValue 0
ixNet setAttribute $sg_vport/protocols/bfd -packetsPerInterval 0
ixNet setAttribute $sg_vport/protocols/bgp -enableExternalActiveConnect True
ixNet setAttribute $sg_vport/protocols/bgp -enableInternalActiveConnect True
ixNet setAttribute $sg_vport/protocols/bgp -enabled False
ixNet setAttribute $sg_vport/protocols/bgp -externalRetries 0
ixNet setAttribute $sg_vport/protocols/bgp -externalRetryDelay 120
ixNet setAttribute $sg_vport/protocols/bgp -internalRetries 0
ixNet setAttribute $sg_vport/protocols/bgp -internalRetryDelay 120
ixNet setAttribute $sg_vport/protocols/eigrp -enabled False
ixNet setAttribute $sg_vport/protocols/igmp -enabled False
ixNet setAttribute $sg_vport/protocols/igmp -numberOfGroups 0
ixNet setAttribute $sg_vport/protocols/igmp -sendLeaveOnStop True
ixNet setAttribute $sg_vport/protocols/igmp -statsEnabled False
ixNet setAttribute $sg_vport/protocols/igmp -timePeriod 0
ixNet setAttribute $sg_vport/protocols/isis -enabled False
ixNet setAttribute $sg_vport/protocols/ldp -enableDiscardSelfAdvFecs False
ixNet setAttribute $sg_vport/protocols/ldp -enableHelloJitter True
ixNet setAttribute $sg_vport/protocols/ldp -enabled False
ixNet setAttribute $sg_vport/protocols/ldp -helloHoldTime 15
ixNet setAttribute $sg_vport/protocols/ldp -helloInterval 5
ixNet setAttribute $sg_vport/protocols/ldp -keepAliveHoldTime 30
ixNet setAttribute $sg_vport/protocols/ldp -keepAliveInterval 10
ixNet setAttribute $sg_vport/protocols/ldp -targetedHelloInterval 15
ixNet setAttribute $sg_vport/protocols/ldp -targetedHoldTime 45
ixNet setAttribute $sg_vport/protocols/mld -enableDoneOnStop True
ixNet setAttribute $sg_vport/protocols/mld -enabled False
ixNet setAttribute $sg_vport/protocols/mld -mldv2Report type143
ixNet setAttribute $sg_vport/protocols/mld -numberOfGroups 0
ixNet setAttribute $sg_vport/protocols/mld -timePeriod 0
ixNet setAttribute $sg_vport/protocols/ospf -enableDrOrBdr False
ixNet setAttribute $sg_vport/protocols/ospf -enabled False
ixNet setAttribute $sg_vport/protocols/ospfV3 -enabled False
ixNet setAttribute $sg_vport/protocols/pimsm -dataMdtFramePerInterval 0
ixNet setAttribute $sg_vport/protocols/pimsm -enableRateControl False
ixNet setAttribute $sg_vport/protocols/pimsm -enabled False
ixNet setAttribute $sg_vport/protocols/pimsm -interval 0
ixNet setAttribute $sg_vport/protocols/pimsm -joinPruneMessagesPerInterval 0
ixNet setAttribute $sg_vport/protocols/pimsm -registerMessagesPerInterval 0
ixNet setAttribute $sg_vport/protocols/pimsm -registerStopMessagesPerInterval 0
ixNet setAttribute $sg_vport/protocols/ping -enabled False
ixNet setAttribute $sg_vport/protocols/rip -enabled False
ixNet setAttribute $sg_vport/protocols/ripng -enabled False
ixNet setAttribute $sg_vport/protocols/rsvp -enableBgpOverLsp True
ixNet setAttribute $sg_vport/protocols/rsvp -enabled False
ixNet setAttribute $sg_vport/protocols/stp -enabled False
ixNet commit
set sg_vport [lindex [ixNet remapIds $sg_vport] 0]
set ixNetSG_ref(2) $sg_vport
set ixNetSG_Stack(1) $sg_vport

#
# configuring the object that corresponds to /vport:1/l1Config/ethernet
#
set sg_ethernet $ixNetSG_Stack(1)/l1Config/ethernet
ixNet setAttribute $sg_ethernet -autoNegotiate True
ixNet setAttribute $sg_ethernet -loopback False
ixNet setAttribute $sg_ethernet -speed speed100fd
ixNet setAttribute $sg_ethernet -media copper
ixNet commit
set sg_ethernet [lindex [ixNet remapIds $sg_ethernet] 0]

#
# configuring the object that corresponds to /vport:1/protocolStack/ethernet:"1c569ec9-ca9e-46c3-a1b1-03c4de579822"
#
set sg_ethernet [ixNet add $ixNetSG_Stack(1)/protocolStack ethernet]
ixNet setAttribute $sg_ethernet -name {MAC/VLAN-1}
ixNet commit
set sg_ethernet [lindex [ixNet remapIds $sg_ethernet] 0]
set ixNetSG_Stack(2) $sg_ethernet

#
# configuring the object that corresponds to /vport:1/protocolStack/ethernet:"1c569ec9-ca9e-46c3-a1b1-03c4de579822"/pppoxEndpoint:"6b044cae-1425-4ba5-9af1-dcfdf437e0a5"
#
set sg_pppoxEndpoint [ixNet add $ixNetSG_Stack(2) pppoxEndpoint]

ixNet setAttribute $sg_pppoxEndpoint -name {PPPoX-1}
ixNet commit
set sg_pppoxEndpoint [lindex [ixNet remapIds $sg_pppoxEndpoint] 0]
set ixNetSG_Stack(3) $sg_pppoxEndpoint

#
# configuring the object that corresponds to /vport:1/protocolStack/ethernet:"1c569ec9-ca9e-46c3-a1b1-03c4de579822"/pppoxEndpoint:"6b044cae-1425-4ba5-9af1-dcfdf437e0a5"/range:"2e43a6e5-ac9f-42da-875c-ede707c6972f"
#
set sg_range [ixNet add $ixNetSG_Stack(3) range]
ixNet setAttribute $sg_range/macRange -mac {AA:BB:CC:00:00:00}
ixNet setAttribute $sg_range/macRange -incrementBy {00:00:00:00:00:01}
ixNet setAttribute $sg_range/macRange -mtu 1500
ixNet setAttribute $sg_range/macRange -count 10
ixNet setAttribute $sg_range/macRange -name {mac-1}
ixNet setAttribute $sg_range/vlanRange -enabled False
ixNet setAttribute $sg_range/vlanRange -firstId 100
ixNet setAttribute $sg_range/vlanRange -incrementStep 1
ixNet setAttribute $sg_range/vlanRange -increment 1
ixNet setAttribute $sg_range/vlanRange -uniqueCount 4094
ixNet setAttribute $sg_range/vlanRange -priority 1
ixNet setAttribute $sg_range/vlanRange -innerEnable False
ixNet setAttribute $sg_range/vlanRange -innerFirstId 1
ixNet setAttribute $sg_range/vlanRange -innerIncrementStep 1
ixNet setAttribute $sg_range/vlanRange -innerIncrement 1
ixNet setAttribute $sg_range/vlanRange -innerUniqueCount 4094
ixNet setAttribute $sg_range/vlanRange -innerPriority 1
ixNet setAttribute $sg_range/vlanRange -idIncrMode 2
ixNet setAttribute $sg_range/vlanRange -name {vlan-1}
ixNet setAttribute $sg_range/pppoxRange -pppoeOptions {PPPoE Options}
ixNet setAttribute $sg_range/pppoxRange -padiTimeout 10
ixNet setAttribute $sg_range/pppoxRange -padiRetries 5
ixNet setAttribute $sg_range/pppoxRange -padrTimeout 10
ixNet setAttribute $sg_range/pppoxRange -padrRetries 5
ixNet setAttribute $sg_range/pppoxRange -enableMruNegotiation False
ixNet setAttribute $sg_range/pppoxRange -serviceOptions {anyService}
ixNet setAttribute $sg_range/pppoxRange -serviceName {}
ixNet setAttribute $sg_range/pppoxRange -acOptions {useFirstResponder}
ixNet setAttribute $sg_range/pppoxRange -acName {}
ixNet setAttribute $sg_range/pppoxRange -enableRedial True
ixNet setAttribute $sg_range/pppoxRange -redialTimeout 10
ixNet setAttribute $sg_range/pppoxRange -redialMax 20
#ixNet setAttribute $sg_range/pppoxRange -enableIntermediateAgentTags False
#ixNet setAttribute $sg_range/pppoxRange -enableIncludeTagInPadi False
#ixNet setAttribute $sg_range/pppoxRange -enableIncludeTagInPadr False
#ixNet setAttribute $sg_range/pppoxRange -enableIncludeTagInPado False
#ixNet setAttribute $sg_range/pppoxRange -enableIncludeTagInPads False
ixNet setAttribute $sg_range/pppoxRange -agentCircuitId {}
ixNet setAttribute $sg_range/pppoxRange -agentRemoteId {}
#ixNet setAttribute $sg_range/pppoxRange -startIfId 0
ixNet setAttribute $sg_range/pppoxRange -lcpOptions {LCP Options}
ixNet setAttribute $sg_range/pppoxRange -lcpTimeout 10
ixNet setAttribute $sg_range/pppoxRange -lcpRetries 3
ixNet setAttribute $sg_range/pppoxRange -mtu 1492
ixNet setAttribute $sg_range/pppoxRange -enableEchoRsp True
ixNet setAttribute $sg_range/pppoxRange -enableEchoReq False
ixNet setAttribute $sg_range/pppoxRange -echoReqInterval 10
ixNet setAttribute $sg_range/pppoxRange -ncpType {IPv4}
ixNet setAttribute $sg_range/pppoxRange -ncpTimeout 10
ixNet setAttribute $sg_range/pppoxRange -ncpRetries 3
ixNet setAttribute $sg_range/pppoxRange -clientBaseIp {1.1.1.1}
ixNet setAttribute $sg_range/pppoxRange -clientIpIncr {0.0.0.1}
ixNet setAttribute $sg_range/pppoxRange -serverBaseIp {2.2.2.2}
ixNet setAttribute $sg_range/pppoxRange -serverIpIncr {0.0.0.0}
ixNet setAttribute $sg_range/pppoxRange -clientBaseIid {00:11:11:11:00:00:00:01}   ## fixed by TCL Script Doctor
ixNet setAttribute $sg_range/pppoxRange -clientIidIncr 1   ## fixed by TCL Script Doctor
ixNet setAttribute $sg_range/pppoxRange -serverBaseIid {00:11:22:11:00:00:00:01}   ## fixed by TCL Script Doctor
ixNet setAttribute $sg_range/pppoxRange -serverIidIncr 1   ## fixed by TCL Script Doctor
ixNet setAttribute $sg_range/pppoxRange -ipv6PoolPrefix {1:1:1::}
ixNet setAttribute $sg_range/pppoxRange -ipv6PoolPrefixLen 48
ixNet setAttribute $sg_range/pppoxRange -ipv6AddrPrefixLen 64
ixNet setAttribute $sg_range/pppoxRange -authOptions {Authentication Options}
ixNet setAttribute $sg_range/pppoxRange -authType {chap}
ixNet setAttribute $sg_range/pppoxRange -papUser {user}
ixNet setAttribute $sg_range/pppoxRange -papPassword {password}
ixNet setAttribute $sg_range/pppoxRange -chapName {user}
ixNet setAttribute $sg_range/pppoxRange -chapSecret {secret}
ixNet setAttribute $sg_range/pppoxRange -lcpTermTimeout 15
ixNet setAttribute $sg_range/pppoxRange -lcpTermRetries 3
ixNet setAttribute $sg_range/pppoxRange -useMagic True
ixNet setAttribute $sg_range/pppoxRange -authTimeout 10
ixNet setAttribute $sg_range/pppoxRange -authRetries 20
ixNet setAttribute $sg_range/pppoxRange -enableDomainGroups False
ixNet setAttribute $sg_range/pppoxRange -domainList {Domain Groups}
ixNet setAttribute $sg_range/pppoxRange -numSessions 10
ixNet setAttribute $sg_range/pppoxRange -name {pppox-1}
ixNet commit
set sg_range [lindex [ixNet remapIds $sg_range] 0]

#
# configuring the object that corresponds to /vport:1/protocolStack/pppoxOptions:1
#
set sg_pppoxOptions [ixNet add $ixNetSG_Stack(1)/protocolStack pppoxOptions]
ixNet setAttribute $sg_pppoxOptions -role {client}
ixNet setAttribute $sg_pppoxOptions -associates [list ]
ixNet setAttribute $sg_pppoxOptions -overrideGlobalRateControls False
ixNet setAttribute $sg_pppoxOptions -setupRateInitial 150
ixNet setAttribute $sg_pppoxOptions -maxOutstandingRequests 150
ixNet setAttribute $sg_pppoxOptions -teardownRateInitial 150
ixNet setAttribute $sg_pppoxOptions -maxOutstandingReleases 150
ixNet setAttribute $sg_pppoxOptions -useWaitForCompletionTimeout False
ixNet commit
set sg_pppoxOptions [lindex [ixNet remapIds $sg_pppoxOptions] 0]

#
# configuring the object that corresponds to /vport:2
#
set sg_vport [ixNet add $ixNetSG_Stack(0) vport]
ixNet setAttribute $sg_vport -type ethernet
ixNet setAttribute $sg_vport -isPullOnly False
ixNet setAttribute $sg_vport -name {Ethernet - 002}
ixNet setAttribute $sg_vport -txMode sequential
ixNet setAttribute $sg_vport -txGapControlMode fixedMode
ixNet setAttribute $sg_vport -connectedTo [ixNet getNull]
ixNet setAttribute $sg_vport -rxMode measure
ixNet setAttribute $sg_vport/l1Config -currentType ethernet
ixNet setAttribute $sg_vport/capture -hardwareEnabled False
ixNet setAttribute $sg_vport/capture -softwareEnabled False
ixNet setAttribute $sg_vport/protocols/arp -enabled False
ixNet setAttribute $sg_vport/protocols/bfd -enabled False
ixNet setAttribute $sg_vport/protocols/bfd -intervalValue 0
ixNet setAttribute $sg_vport/protocols/bfd -packetsPerInterval 0
ixNet setAttribute $sg_vport/protocols/bgp -enableExternalActiveConnect True
ixNet setAttribute $sg_vport/protocols/bgp -enableInternalActiveConnect True
ixNet setAttribute $sg_vport/protocols/bgp -enabled False
ixNet setAttribute $sg_vport/protocols/bgp -externalRetries 0
ixNet setAttribute $sg_vport/protocols/bgp -externalRetryDelay 120
ixNet setAttribute $sg_vport/protocols/bgp -internalRetries 0
ixNet setAttribute $sg_vport/protocols/bgp -internalRetryDelay 120
ixNet setAttribute $sg_vport/protocols/eigrp -enabled False
ixNet setAttribute $sg_vport/protocols/igmp -enabled False
ixNet setAttribute $sg_vport/protocols/igmp -numberOfGroups 0
ixNet setAttribute $sg_vport/protocols/igmp -sendLeaveOnStop True
ixNet setAttribute $sg_vport/protocols/igmp -statsEnabled False
ixNet setAttribute $sg_vport/protocols/igmp -timePeriod 0
ixNet setAttribute $sg_vport/protocols/isis -enabled False
ixNet setAttribute $sg_vport/protocols/ldp -enableDiscardSelfAdvFecs False
ixNet setAttribute $sg_vport/protocols/ldp -enableHelloJitter True
ixNet setAttribute $sg_vport/protocols/ldp -enabled False
ixNet setAttribute $sg_vport/protocols/ldp -helloHoldTime 15
ixNet setAttribute $sg_vport/protocols/ldp -helloInterval 5
ixNet setAttribute $sg_vport/protocols/ldp -keepAliveHoldTime 30
ixNet setAttribute $sg_vport/protocols/ldp -keepAliveInterval 10
ixNet setAttribute $sg_vport/protocols/ldp -targetedHelloInterval 15
ixNet setAttribute $sg_vport/protocols/ldp -targetedHoldTime 45
ixNet setAttribute $sg_vport/protocols/mld -enableDoneOnStop True
ixNet setAttribute $sg_vport/protocols/mld -enabled False
ixNet setAttribute $sg_vport/protocols/mld -mldv2Report type143
ixNet setAttribute $sg_vport/protocols/mld -numberOfGroups 0
ixNet setAttribute $sg_vport/protocols/mld -timePeriod 0
ixNet setAttribute $sg_vport/protocols/ospf -enableDrOrBdr False
ixNet setAttribute $sg_vport/protocols/ospf -enabled False
ixNet setAttribute $sg_vport/protocols/ospfV3 -enabled False
ixNet setAttribute $sg_vport/protocols/pimsm -dataMdtFramePerInterval 0
ixNet setAttribute $sg_vport/protocols/pimsm -enableRateControl False
ixNet setAttribute $sg_vport/protocols/pimsm -enabled False
ixNet setAttribute $sg_vport/protocols/pimsm -interval 0
ixNet setAttribute $sg_vport/protocols/pimsm -joinPruneMessagesPerInterval 0
ixNet setAttribute $sg_vport/protocols/pimsm -registerMessagesPerInterval 0
ixNet setAttribute $sg_vport/protocols/pimsm -registerStopMessagesPerInterval 0
ixNet setAttribute $sg_vport/protocols/ping -enabled False
ixNet setAttribute $sg_vport/protocols/rip -enabled False
ixNet setAttribute $sg_vport/protocols/ripng -enabled False
ixNet setAttribute $sg_vport/protocols/rsvp -enableBgpOverLsp True
ixNet setAttribute $sg_vport/protocols/rsvp -enabled False
ixNet setAttribute $sg_vport/protocols/stp -enabled False
ixNet commit
set sg_vport [lindex [ixNet remapIds $sg_vport] 0]
set ixNetSG_ref(8) $sg_vport
set ixNetSG_Stack(1) $sg_vport

#
# configuring the object that corresponds to /vport:2/l1Config/ethernet
#
set sg_ethernet $ixNetSG_Stack(1)/l1Config/ethernet
ixNet setAttribute $sg_ethernet -autoNegotiate True
ixNet setAttribute $sg_ethernet -loopback False
ixNet setAttribute $sg_ethernet -speed speed100fd
ixNet setAttribute $sg_ethernet -media copper
ixNet commit
set sg_ethernet [lindex [ixNet remapIds $sg_ethernet] 0]

#
# configuring the object that corresponds to /vport:2/protocolStack/ethernet:"779f80a4-0452-42c9-b503-a1166ec5b781"
#
set sg_ethernet [ixNet add $ixNetSG_Stack(1)/protocolStack ethernet]
ixNet setAttribute $sg_ethernet -name {MAC/VLAN-2}
ixNet commit
set sg_ethernet [lindex [ixNet remapIds $sg_ethernet] 0]
set ixNetSG_Stack(2) $sg_ethernet

#
# configuring the object that corresponds to /vport:2/protocolStack/ethernet:"779f80a4-0452-42c9-b503-a1166ec5b781"/pppoxEndpoint:"7251633e-e2d3-4759-810f-0e1b103fe6f0"
#
set sg_pppoxEndpoint [ixNet add $ixNetSG_Stack(2) pppoxEndpoint]

ixNet setAttribute $sg_pppoxEndpoint -name {PPPoX-2}
ixNet commit
set sg_pppoxEndpoint [lindex [ixNet remapIds $sg_pppoxEndpoint] 0]
set ixNetSG_Stack(3) $sg_pppoxEndpoint

#
# configuring the object that corresponds to /vport:2/protocolStack/ethernet:"779f80a4-0452-42c9-b503-a1166ec5b781"/pppoxEndpoint:"7251633e-e2d3-4759-810f-0e1b103fe6f0"/range:"d383332d-6873-4ab0-9cd9-4a882c58bdd8"
#
set sg_range [ixNet add $ixNetSG_Stack(3) range]
ixNet setAttribute $sg_range/macRange -mac {AA:BB:1C:00:00:01}
ixNet setAttribute $sg_range/macRange -incrementBy {00:00:00:00:00:01}
ixNet setAttribute $sg_range/macRange -mtu 1500
ixNet setAttribute $sg_range/macRange -count 10
ixNet setAttribute $sg_range/macRange -name {mac-2}
ixNet setAttribute $sg_range/vlanRange -enabled False
ixNet setAttribute $sg_range/vlanRange -firstId 100
ixNet setAttribute $sg_range/vlanRange -incrementStep 1
ixNet setAttribute $sg_range/vlanRange -increment 1
ixNet setAttribute $sg_range/vlanRange -uniqueCount 4094
ixNet setAttribute $sg_range/vlanRange -priority 1
ixNet setAttribute $sg_range/vlanRange -innerEnable False
ixNet setAttribute $sg_range/vlanRange -innerFirstId 1
ixNet setAttribute $sg_range/vlanRange -innerIncrementStep 1
ixNet setAttribute $sg_range/vlanRange -innerIncrement 1
ixNet setAttribute $sg_range/vlanRange -innerUniqueCount 4094
ixNet setAttribute $sg_range/vlanRange -innerPriority 1
ixNet setAttribute $sg_range/vlanRange -idIncrMode 2
ixNet setAttribute $sg_range/vlanRange -name {vlan-2}
ixNet setAttribute $sg_range/pppoxRange -pppoeOptions {PPPoE Options}
ixNet setAttribute $sg_range/pppoxRange -padiTimeout 10
ixNet setAttribute $sg_range/pppoxRange -padiRetries 5
ixNet setAttribute $sg_range/pppoxRange -padrTimeout 10
ixNet setAttribute $sg_range/pppoxRange -padrRetries 5
ixNet setAttribute $sg_range/pppoxRange -enableMruNegotiation False
ixNet setAttribute $sg_range/pppoxRange -serviceOptions {anyService}
ixNet setAttribute $sg_range/pppoxRange -serviceName {}
ixNet setAttribute $sg_range/pppoxRange -acOptions {useFirstResponder}
ixNet setAttribute $sg_range/pppoxRange -acName {}
ixNet setAttribute $sg_range/pppoxRange -enableRedial True
ixNet setAttribute $sg_range/pppoxRange -redialTimeout 10
ixNet setAttribute $sg_range/pppoxRange -redialMax 20
#ixNet setAttribute $sg_range/pppoxRange -enableIntermediateAgentTags False
#ixNet setAttribute $sg_range/pppoxRange -enableIncludeTagInPadi False
#ixNet setAttribute $sg_range/pppoxRange -enableIncludeTagInPadr False
#ixNet setAttribute $sg_range/pppoxRange -enableIncludeTagInPado False
#ixNet setAttribute $sg_range/pppoxRange -enableIncludeTagInPads False
ixNet setAttribute $sg_range/pppoxRange -agentCircuitId {}
ixNet setAttribute $sg_range/pppoxRange -agentRemoteId {}
#ixNet setAttribute $sg_range/pppoxRange -startIfId 0
ixNet setAttribute $sg_range/pppoxRange -lcpOptions {LCP Options}
ixNet setAttribute $sg_range/pppoxRange -lcpTimeout 10
ixNet setAttribute $sg_range/pppoxRange -lcpRetries 3
ixNet setAttribute $sg_range/pppoxRange -mtu 1492
ixNet setAttribute $sg_range/pppoxRange -enableEchoRsp True
ixNet setAttribute $sg_range/pppoxRange -enableEchoReq False
ixNet setAttribute $sg_range/pppoxRange -echoReqInterval 10
ixNet setAttribute $sg_range/pppoxRange -ncpType {IPv4}
ixNet setAttribute $sg_range/pppoxRange -ncpTimeout 10
ixNet setAttribute $sg_range/pppoxRange -ncpRetries 3
ixNet setAttribute $sg_range/pppoxRange -clientBaseIp {1.1.1.1}
ixNet setAttribute $sg_range/pppoxRange -clientIpIncr {0.0.0.1}
ixNet setAttribute $sg_range/pppoxRange -serverBaseIp {2.2.2.2}
ixNet setAttribute $sg_range/pppoxRange -serverIpIncr {0.0.0.0}
ixNet setAttribute $sg_range/pppoxRange -clientBaseIid {00:11:11:11:00:00:00:01}   ## fixed by TCL Script Doctor
ixNet setAttribute $sg_range/pppoxRange -clientIidIncr 1   ## fixed by TCL Script Doctor
ixNet setAttribute $sg_range/pppoxRange -serverBaseIid {00:11:22:11:00:00:00:01}   ## fixed by TCL Script Doctor
ixNet setAttribute $sg_range/pppoxRange -serverIidIncr 1   ## fixed by TCL Script Doctor
ixNet setAttribute $sg_range/pppoxRange -ipv6PoolPrefix {1:1:1::}
ixNet setAttribute $sg_range/pppoxRange -ipv6PoolPrefixLen 48
ixNet setAttribute $sg_range/pppoxRange -ipv6AddrPrefixLen 64
ixNet setAttribute $sg_range/pppoxRange -authOptions {Authentication Options}
ixNet setAttribute $sg_range/pppoxRange -authType {chap}
ixNet setAttribute $sg_range/pppoxRange -papUser {user}
ixNet setAttribute $sg_range/pppoxRange -papPassword {password}
ixNet setAttribute $sg_range/pppoxRange -chapName {user}
ixNet setAttribute $sg_range/pppoxRange -chapSecret {secret}
ixNet setAttribute $sg_range/pppoxRange -lcpTermTimeout 15
ixNet setAttribute $sg_range/pppoxRange -lcpTermRetries 3
ixNet setAttribute $sg_range/pppoxRange -useMagic True
ixNet setAttribute $sg_range/pppoxRange -authTimeout 10
ixNet setAttribute $sg_range/pppoxRange -authRetries 20
ixNet setAttribute $sg_range/pppoxRange -enableDomainGroups False
ixNet setAttribute $sg_range/pppoxRange -domainList {Domain Groups}
ixNet setAttribute $sg_range/pppoxRange -numSessions 10
ixNet setAttribute $sg_range/pppoxRange -name {pppox-2}
ixNet commit
set sg_range [lindex [ixNet remapIds $sg_range] 0]

#
# configuring the object that corresponds to /vport:2/protocolStack/pppoxOptions:1
#
set sg_pppoxOptions [ixNet add $ixNetSG_Stack(1)/protocolStack pppoxOptions]
ixNet setAttribute $sg_pppoxOptions -role {server}
ixNet setAttribute $sg_pppoxOptions -associates [list ]
ixNet setAttribute $sg_pppoxOptions -overrideGlobalRateControls False
ixNet setAttribute $sg_pppoxOptions -setupRateInitial 150
ixNet setAttribute $sg_pppoxOptions -maxOutstandingRequests 150
ixNet setAttribute $sg_pppoxOptions -teardownRateInitial 150
ixNet setAttribute $sg_pppoxOptions -maxOutstandingReleases 150
ixNet setAttribute $sg_pppoxOptions -useWaitForCompletionTimeout False
ixNet commit
set sg_pppoxOptions [lindex [ixNet remapIds $sg_pppoxOptions] 0]

###
### /globals area
###

#
# configuring the object that corresponds to /globals/protocolStack/pppoxGlobals:1
#
set sg_pppoxGlobals [ixNet add $ixNetSG_Stack(0)/globals/protocolStack pppoxGlobals]
ixNet setAttribute $sg_pppoxGlobals -setupRateInitial 300
ixNet setAttribute $sg_pppoxGlobals -maxOutstandingRequests 300
ixNet setAttribute $sg_pppoxGlobals -teardownRateInitial 300
ixNet setAttribute $sg_pppoxGlobals -maxOutstandingReleases 300
ixNet commit
set sg_pppoxGlobals [lindex [ixNet remapIds $sg_pppoxGlobals] 0]

###
### /traffic area
###

#
# configuring the object that corresponds to /traffic/trafficItem:1
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -srcDestMesh fullMesh
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -name {TI0-TRAFFICITEM}
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -routeMesh fullMesh
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode lineRate
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 100000
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:1/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(2)/protocolStack]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(8)/protocolStack]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:1/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -selectedTrackBy sourceIp
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:1/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

###
### /testConfiguration area
###

#
# configuring the object that corresponds to /testConfiguration/custom:1
#
set sg_custom $ixNetSG_Stack(0)/testConfiguration/custom:1
ixNet setAttribute $sg_custom -selectedTest fixedDuration
ixNet commit
set sg_custom [lindex [ixNet remapIds $sg_custom] 0]
set ixNetSG_Stack(1) $sg_custom

#
# configuring the object that corresponds to /testConfiguration/custom:1/fixedDuration:1
#
set sg_fixedDuration $ixNetSG_Stack(1)/fixedDuration:1
ixNet setAttribute $sg_fixedDuration -selectedItems [list ]
ixNet setAttribute $sg_fixedDuration/testSetup -selectedVariableParameter percentLineRate
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -algorithm unchanged
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -backoff 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -value 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -stepValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -minValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -valueList [list ]
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -maxValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -initialValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -resolution 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -acceptableFrameLoss 0
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -algorithm unchanged
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -step 0
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -valueList [list ]
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -count 1
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -selectedAdditionalLoopParameter frameSize
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -maxValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -value 0
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -initialValue 0
ixNet setAttribute $sg_fixedDuration/protocols -startBehavior startWithCurrent
ixNet setAttribute $sg_fixedDuration/protocols -waitAfterStart 0
ixNet setAttribute $sg_fixedDuration/protocols -waitAfterStop 0
ixNet setAttribute $sg_fixedDuration/traffic -learningFrequency oncePerTest
ixNet setAttribute $sg_fixedDuration/traffic -l2FrameSize 128
ixNet setAttribute $sg_fixedDuration/traffic -delayAfterTransmit 5
ixNet setAttribute $sg_fixedDuration/traffic -l3RepeatCount 3
ixNet setAttribute $sg_fixedDuration/traffic -learningStartDelay 0
ixNet setAttribute $sg_fixedDuration/traffic -l2FrameSizeType sameAsStream
ixNet setAttribute $sg_fixedDuration/traffic -trafficStartDelay 5
ixNet setAttribute $sg_fixedDuration/traffic -generateStreams True
ixNet setAttribute $sg_fixedDuration/traffic -enableLearning False
ixNet setAttribute $sg_fixedDuration/traffic -l3RepeatInterval 2
ixNet setAttribute $sg_fixedDuration/traffic -enableStaggeredTransmit False
ixNet setAttribute $sg_fixedDuration/traffic -l2BurstCount 1
ixNet setAttribute $sg_fixedDuration/traffic -l3Gap 1
ixNet setAttribute $sg_fixedDuration/traffic -l2Rate 1
ixNet setAttribute $sg_fixedDuration/runParameters -enableLatencyCriteria False
ixNet setAttribute $sg_fixedDuration/runParameters -numTrials 1
ixNet setAttribute $sg_fixedDuration/runParameters -ratePortType averagePort
ixNet setAttribute $sg_fixedDuration/runParameters -testDuration {00:00:20}
ixNet setAttribute $sg_fixedDuration/runParameters -enableRatePassCriteria False
ixNet setAttribute $sg_fixedDuration/runParameters -enableCalculateLatency False
ixNet setAttribute $sg_fixedDuration/runParameters -latencyUnit microSeconds
ixNet setAttribute $sg_fixedDuration/runParameters -latencyPortType averagePort
ixNet setAttribute $sg_fixedDuration/runParameters -latencyLessThanEqualTo 10
ixNet setAttribute $sg_fixedDuration/runParameters -rateGreaterThanEqualTo 10
ixNet commit
set sg_fixedDuration [lindex [ixNet remapIds $sg_fixedDuration] 0]
return 0
}

ixNetScriptgenProc

