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
set ixNetSG_curObj [ixNet getRoot]
ixNet setAttribute $ixNetSG_curObj/traffic -globalIterationMode continuous
ixNet setAttribute $ixNetSG_curObj/traffic -enableMinFrameSize False
ixNet setAttribute $ixNetSG_curObj/traffic -enableStaggeredTransmit False
ixNet setAttribute $ixNetSG_curObj/traffic -latencyBinType cutThroughLatency
ixNet setAttribute $ixNetSG_curObj/traffic -waitTime 1
ixNet setAttribute $ixNetSG_curObj/traffic -enableStreamOrdering False
ixNet setAttribute $ixNetSG_curObj/traffic -globalIterationCount 1
ixNet setAttribute $ixNetSG_curObj/testConfiguration -productLabel {Your switch/router name here}
ixNet setAttribute $ixNetSG_curObj/testConfiguration -enableAbortIfLinkDown False
ixNet setAttribute $ixNetSG_curObj/testConfiguration -enableGenerateReportAfterRun False
ixNet setAttribute $ixNetSG_curObj/testConfiguration -enableCheckLinkState False
ixNet setAttribute $ixNetSG_curObj/testConfiguration -enableSwitchToResult False
ixNet setAttribute $ixNetSG_curObj/testConfiguration -selectedSuite custom
ixNet setAttribute $ixNetSG_curObj/testConfiguration -version {Your firmware version here}
ixNet setAttribute $ixNetSG_curObj/testConfiguration -enableCapture False
ixNet setAttribute $ixNetSG_curObj/testConfiguration -serialNumber {Your switch/router serial number here}
ixNet setAttribute $ixNetSG_curObj/testConfiguration -enableRebootCpu False
ixNet setAttribute $ixNetSG_curObj/testConfiguration -sleepTimeAfterReboot 10
ixNet setAttribute $ixNetSG_curObj/testConfiguration -comments {}
ixNet setAttribute $ixNetSG_curObj/testConfiguration -linkDownTimeout 5
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
set ixNetSG_Stack(0) $ixNetSG_curObj

###
### /vport area
###

#
# configuring the object that corresponds to /vport:1
#
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(0) vport]
ixNet setAttribute $ixNetSG_curObj -type ethernet
ixNet setAttribute $ixNetSG_curObj -isPullOnly False
ixNet setAttribute $ixNetSG_curObj -name {optixia2:05:01-Ethernet}
ixNet setAttribute $ixNetSG_curObj -txMode sequential
ixNet setAttribute $ixNetSG_curObj -txGapControlMode fixedMode
ixNet setAttribute $ixNetSG_curObj -connectedTo [ixNet getNull]
ixNet setAttribute $ixNetSG_curObj -rxMode measure
ixNet setAttribute $ixNetSG_curObj/l1Config -currentType ethernet
ixNet setAttribute $ixNetSG_curObj/l1Config/ethernet -autoNegotiate False
ixNet setAttribute $ixNetSG_curObj/l1Config/ethernet -speed speed10fd
ixNet setAttribute $ixNetSG_curObj/l1Config/ethernet -loopback True
ixNet setAttribute $ixNetSG_curObj/l1Config/ethernet -media copper
ixNet setAttribute $ixNetSG_curObj/protocols/arp -enabled True
ixNet setAttribute $ixNetSG_curObj/protocols/bfd -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/bfd -intervalValue 0
ixNet setAttribute $ixNetSG_curObj/protocols/bfd -packetsPerInterval 0
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -enableExternalActiveConnect True
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -enableInternalActiveConnect True
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -externalRetries 0
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -externalRetryDelay 120
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -internalRetries 0
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -internalRetryDelay 120
ixNet setAttribute $ixNetSG_curObj/protocols/eigrp -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/igmp -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/igmp -numberOfGroups 0
ixNet setAttribute $ixNetSG_curObj/protocols/igmp -sendLeaveOnStop True
ixNet setAttribute $ixNetSG_curObj/protocols/igmp -statsEnabled False
ixNet setAttribute $ixNetSG_curObj/protocols/igmp -timePeriod 0
ixNet setAttribute $ixNetSG_curObj/protocols/isis -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -enableDiscardSelfAdvFecs False
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -enableHelloJitter True
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -helloHoldTime 15
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -helloInterval 5
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -keepAliveHoldTime 30
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -keepAliveInterval 10
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -targetedHelloInterval 15
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -targetedHoldTime 45
ixNet setAttribute $ixNetSG_curObj/protocols/mld -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/mld -enableDoneOnStop True
ixNet setAttribute $ixNetSG_curObj/protocols/mld -mldv2Report type143
ixNet setAttribute $ixNetSG_curObj/protocols/mld -numberOfGroups 0
ixNet setAttribute $ixNetSG_curObj/protocols/mld -timePeriod 0
ixNet setAttribute $ixNetSG_curObj/protocols/ospf -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/ospf -enableDrOrBdr False
ixNet setAttribute $ixNetSG_curObj/protocols/ospfV3 -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -dataMdtFramePerInterval 0
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -enableRateControl False
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -interval 0
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -joinPruneMessagesPerInterval 0
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -registerMessagesPerInterval 0
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -registerStopMessagesPerInterval 0
ixNet setAttribute $ixNetSG_curObj/protocols/ping -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/rip -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/ripng -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/rsvp -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/stp -enabled False
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
set ixNetSG_ref(2) $ixNetSG_curObj
set ixNetSG_Stack(1) $ixNetSG_curObj

#
# configuring the object that corresponds to /vport:1/interface:1
#
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $ixNetSG_curObj -description {ProtocolInterface - 100:01 - 1}
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -eui64Id {02 00 23 FF FE F9 5A 4C }
ixNet setAttribute $ixNetSG_curObj -mtu 1500
ixNet setAttribute $ixNetSG_curObj -type default
ixNet setAttribute $ixNetSG_curObj/vlan -tpid {0x8100}
ixNet setAttribute $ixNetSG_curObj/vlan -vlanCount 1
ixNet setAttribute $ixNetSG_curObj/vlan -vlanEnable False
ixNet setAttribute $ixNetSG_curObj/vlan -vlanId {1}
ixNet setAttribute $ixNetSG_curObj/vlan -vlanPriority {0}
ixNet setAttribute $ixNetSG_curObj/atm -encapsulation llcBridgeFcs
ixNet setAttribute $ixNetSG_curObj/atm -vci 32
ixNet setAttribute $ixNetSG_curObj/atm -vpi 0
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -clientId {}
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -enabled False
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -renewTimer 0
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -requestRate 0
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -serverId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -tlvs [list ]
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -vendorId {}
ixNet setAttribute $ixNetSG_curObj/dhcpV6Properties -enabled False
ixNet setAttribute $ixNetSG_curObj/dhcpV6Properties -iaId 0
ixNet setAttribute $ixNetSG_curObj/dhcpV6Properties -iaType temporary
ixNet setAttribute $ixNetSG_curObj/dhcpV6Properties -renewTimer 0
ixNet setAttribute $ixNetSG_curObj/dhcpV6Properties -requestRate 0
ixNet setAttribute $ixNetSG_curObj/dhcpV6Properties -tlvs [list ]
ixNet setAttribute $ixNetSG_curObj/ethernet -macAddress 00:00:23:f9:5a:4c
ixNet setAttribute $ixNetSG_curObj/ethernet -mtu 1500
ixNet setAttribute $ixNetSG_curObj/ethernet -uidFromMac True
ixNet setAttribute $ixNetSG_curObj/gre -dest 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/gre -inKey 0
ixNet setAttribute $ixNetSG_curObj/gre -outKey 0
ixNet setAttribute $ixNetSG_curObj/gre -source [ixNet getNull]
ixNet setAttribute $ixNetSG_curObj/gre -useChecksum False
ixNet setAttribute $ixNetSG_curObj/gre -useKey False
ixNet setAttribute $ixNetSG_curObj/gre -useSequence False
ixNet setAttribute $ixNetSG_curObj/unconnected -connectedVia [ixNet getNull]
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
set ixNetSG_Stack(2) $ixNetSG_curObj

#
# configuring the object that corresponds to /vport:1/interface:1/IPv4
#
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $ixNetSG_curObj -gateway 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -ip 1.1.1.1
ixNet setAttribute $ixNetSG_curObj -maskWidth 24
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]

#
# configuring the object that corresponds to /vport:2
#
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(0) vport]
ixNet setAttribute $ixNetSG_curObj -type ethernet
ixNet setAttribute $ixNetSG_curObj -isPullOnly False
ixNet setAttribute $ixNetSG_curObj -name {optixia2:05:02-Ethernet}
ixNet setAttribute $ixNetSG_curObj -txMode sequential
ixNet setAttribute $ixNetSG_curObj -txGapControlMode fixedMode
ixNet setAttribute $ixNetSG_curObj -connectedTo [ixNet getNull]
ixNet setAttribute $ixNetSG_curObj -rxMode measure
ixNet setAttribute $ixNetSG_curObj/l1Config -currentType ethernet
ixNet setAttribute $ixNetSG_curObj/l1Config/ethernet -autoNegotiate True
ixNet setAttribute $ixNetSG_curObj/l1Config/ethernet -speed speed100fd
ixNet setAttribute $ixNetSG_curObj/l1Config/ethernet -loopback False
ixNet setAttribute $ixNetSG_curObj/l1Config/ethernet -media copper
ixNet setAttribute $ixNetSG_curObj/protocols/arp -enabled True
ixNet setAttribute $ixNetSG_curObj/protocols/bfd -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/bfd -intervalValue 0
ixNet setAttribute $ixNetSG_curObj/protocols/bfd -packetsPerInterval 0
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -enableExternalActiveConnect True
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -enableInternalActiveConnect True
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -externalRetries 0
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -externalRetryDelay 120
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -internalRetries 0
ixNet setAttribute $ixNetSG_curObj/protocols/bgp -internalRetryDelay 120
ixNet setAttribute $ixNetSG_curObj/protocols/eigrp -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/igmp -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/igmp -numberOfGroups 0
ixNet setAttribute $ixNetSG_curObj/protocols/igmp -sendLeaveOnStop True
ixNet setAttribute $ixNetSG_curObj/protocols/igmp -statsEnabled False
ixNet setAttribute $ixNetSG_curObj/protocols/igmp -timePeriod 0
ixNet setAttribute $ixNetSG_curObj/protocols/isis -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -enableDiscardSelfAdvFecs False
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -enableHelloJitter True
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -helloHoldTime 15
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -helloInterval 5
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -keepAliveHoldTime 30
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -keepAliveInterval 10
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -targetedHelloInterval 15
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -targetedHoldTime 45
ixNet setAttribute $ixNetSG_curObj/protocols/mld -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/mld -enableDoneOnStop True
ixNet setAttribute $ixNetSG_curObj/protocols/mld -mldv2Report type143
ixNet setAttribute $ixNetSG_curObj/protocols/mld -numberOfGroups 0
ixNet setAttribute $ixNetSG_curObj/protocols/mld -timePeriod 0
ixNet setAttribute $ixNetSG_curObj/protocols/ospf -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/ospf -enableDrOrBdr False
ixNet setAttribute $ixNetSG_curObj/protocols/ospfV3 -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -dataMdtFramePerInterval 0
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -enableRateControl False
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -interval 0
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -joinPruneMessagesPerInterval 0
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -registerMessagesPerInterval 0
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -registerStopMessagesPerInterval 0
ixNet setAttribute $ixNetSG_curObj/protocols/ping -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/rip -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/ripng -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/rsvp -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/stp -enabled False
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
set ixNetSG_ref(5) $ixNetSG_curObj
set ixNetSG_Stack(1) $ixNetSG_curObj

#
# configuring the object that corresponds to /vport:2/interface:1
#
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $ixNetSG_curObj -description {ProtocolInterface - 100:02 - 2}
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -eui64Id {02 00 23 FF FE F9 5A 4D }
ixNet setAttribute $ixNetSG_curObj -mtu 1500
ixNet setAttribute $ixNetSG_curObj -type default
ixNet setAttribute $ixNetSG_curObj/vlan -tpid {0x8100}
ixNet setAttribute $ixNetSG_curObj/vlan -vlanCount 1
ixNet setAttribute $ixNetSG_curObj/vlan -vlanEnable False
ixNet setAttribute $ixNetSG_curObj/vlan -vlanId {1}
ixNet setAttribute $ixNetSG_curObj/vlan -vlanPriority {0}
ixNet setAttribute $ixNetSG_curObj/atm -encapsulation llcBridgeFcs
ixNet setAttribute $ixNetSG_curObj/atm -vci 32
ixNet setAttribute $ixNetSG_curObj/atm -vpi 0
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -clientId {}
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -enabled False
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -renewTimer 0
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -requestRate 0
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -serverId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -tlvs [list ]
ixNet setAttribute $ixNetSG_curObj/dhcpV4Properties -vendorId {}
ixNet setAttribute $ixNetSG_curObj/dhcpV6Properties -enabled False
ixNet setAttribute $ixNetSG_curObj/dhcpV6Properties -iaId 0
ixNet setAttribute $ixNetSG_curObj/dhcpV6Properties -iaType temporary
ixNet setAttribute $ixNetSG_curObj/dhcpV6Properties -renewTimer 0
ixNet setAttribute $ixNetSG_curObj/dhcpV6Properties -requestRate 0
ixNet setAttribute $ixNetSG_curObj/dhcpV6Properties -tlvs [list ]
ixNet setAttribute $ixNetSG_curObj/ethernet -macAddress 00:00:23:f9:5a:4d
ixNet setAttribute $ixNetSG_curObj/ethernet -mtu 1500
ixNet setAttribute $ixNetSG_curObj/ethernet -uidFromMac True
ixNet setAttribute $ixNetSG_curObj/gre -dest 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/gre -inKey 0
ixNet setAttribute $ixNetSG_curObj/gre -outKey 0
ixNet setAttribute $ixNetSG_curObj/gre -source [ixNet getNull]
ixNet setAttribute $ixNetSG_curObj/gre -useChecksum False
ixNet setAttribute $ixNetSG_curObj/gre -useKey False
ixNet setAttribute $ixNetSG_curObj/gre -useSequence False
ixNet setAttribute $ixNetSG_curObj/unconnected -connectedVia [ixNet getNull]
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
set ixNetSG_Stack(2) $ixNetSG_curObj

#
# configuring the object that corresponds to /vport:2/interface:1/IPv4
#
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $ixNetSG_curObj -gateway 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -ip 1.1.1.2
ixNet setAttribute $ixNetSG_curObj -maskWidth 24
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]

###
### /availableHardware area
###

#
# configuring the object that corresponds to /availableHardware/chassis:"optixia2"
#
#set ixNetSG_curObj [ixNet add $ixNetSG_Stack(0)/availableHardware chassis]
#ixNet setAttribute $ixNetSG_curObj -hostname {optixia2}
#ixNet commit
#set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
#set ixNetSG_ref(8) $ixNetSG_curObj
#ixNet setAttribute $ixNetSG_ref(2) -connectedTo $ixNetSG_ref(8)/card:5/port:1
#ixNet setAttribute $ixNetSG_ref(5) -connectedTo $ixNetSG_ref(8)/card:5/port:2
#ixNet commit

###
### /traffic area
###

#
# configuring the object that corresponds to /traffic/trafficItem:7
#
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -srcDestMesh fullMesh
ixNet setAttribute $ixNetSG_curObj -payloadData {}
ixNet setAttribute $ixNetSG_curObj -streamPackingMode optimalPacking
ixNet setAttribute $ixNetSG_curObj -allowSelfDestined False
ixNet setAttribute $ixNetSG_curObj -name {LOR-TRAFFICITEM}
ixNet setAttribute $ixNetSG_curObj -encapsulationType nonMpls
ixNet setAttribute $ixNetSG_curObj -forceError noError
ixNet setAttribute $ixNetSG_curObj -routeMesh fullMesh
ixNet setAttribute $ixNetSG_curObj -payloadType incByte
ixNet setAttribute $ixNetSG_curObj -hostsPerNetwork 1
ixNet setAttribute $ixNetSG_curObj -endpointType ipv4ApplicationTraffic
ixNet setAttribute $ixNetSG_curObj/applicationProfile -testObjectiveValue 100
ixNet setAttribute $ixNetSG_curObj/applicationProfile -applicationProfileType [ixNet getNull]
ixNet setAttribute $ixNetSG_curObj/applicationProfile -enableCeToPeTraffic False
ixNet setAttribute $ixNetSG_curObj/applicationProfile -numDestinationPorts 1
ixNet setAttribute $ixNetSG_curObj/applicationProfile -useAllIpSubnets True
ixNet setAttribute $ixNetSG_curObj/applicationProfile -enableTestObjective False
ixNet setAttribute $ixNetSG_curObj/applicationProfile -rampUpPercentage 50
ixNet setAttribute $ixNetSG_curObj/frameOptions -frameSizeMode fixed
ixNet setAttribute $ixNetSG_curObj/rateOptions -interBurstGap 64
ixNet setAttribute $ixNetSG_curObj/rateOptions -rateMode lineRate
ixNet setAttribute $ixNetSG_curObj/rateOptions -txDelay 0
ixNet setAttribute $ixNetSG_curObj/rateOptions -enforceMinGap 12
ixNet setAttribute $ixNetSG_curObj/rateOptions -enableInterStreamGap False
ixNet setAttribute $ixNetSG_curObj/rateOptions -burstsPerStream 1
ixNet setAttribute $ixNetSG_curObj/rateOptions -packetsPerBurst 100
ixNet setAttribute $ixNetSG_curObj/rateOptions -bitRate 100000
ixNet setAttribute $ixNetSG_curObj/rateOptions -packetGap 64
ixNet setAttribute $ixNetSG_curObj/rateOptions -interStreamGap 64
ixNet setAttribute $ixNetSG_curObj/rateOptions -enableInterBurstGap False
ixNet setAttribute $ixNetSG_curObj/rateOptions -lineRate 10
ixNet setAttribute $ixNetSG_curObj/rateOptions -packetCountType auto
ixNet setAttribute $ixNetSG_curObj/rateOptions -packetsPerSecond 100000
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
set ixNetSG_ref(9) $ixNetSG_curObj
set ixNetSG_Stack(1) $ixNetSG_curObj

#
# configuring the object that corresponds to /traffic/trafficItem:7/pair:1
#
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $ixNetSG_curObj -sources [list $ixNetSG_ref(2)/protocols]
ixNet setAttribute $ixNetSG_curObj -destinations [list $ixNetSG_ref(5)/protocols]
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:7/frameOptions/fixed
#
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1)/frameOptions fixed]
ixNet setAttribute $ixNetSG_curObj -fixedFrameSize 64
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
ixNet setAttribute $ixNetSG_ref(9)/applicationProfile -applicationProfileType $ixNetSG_ref(9)/applicationProfileType:"HTTP_1.1_TM_20MB"
ixNet commit

###
### /testConfiguration area
###

#
# configuring the object that corresponds to /testConfiguration/custom:1
#
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(0)/testConfiguration custom]
ixNet setAttribute $ixNetSG_curObj -selectedTest fixedDuration
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
set ixNetSG_Stack(1) $ixNetSG_curObj

#
# configuring the object that corresponds to /testConfiguration/custom:1/fixedDuration:1
#
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1) fixedDuration]
ixNet setAttribute $ixNetSG_curObj -selectedItems [list ]
ixNet setAttribute $ixNetSG_curObj/testSetup -selectedVariableParameter percentLineRate
ixNet setAttribute $ixNetSG_curObj/testSetup/variableLoop -algorithm unchanged
ixNet setAttribute $ixNetSG_curObj/testSetup/variableLoop -backoff 0
ixNet setAttribute $ixNetSG_curObj/testSetup/variableLoop -value 0
ixNet setAttribute $ixNetSG_curObj/testSetup/variableLoop -stepValue 0
ixNet setAttribute $ixNetSG_curObj/testSetup/variableLoop -minValue 0
ixNet setAttribute $ixNetSG_curObj/testSetup/variableLoop -valueList [list ]
ixNet setAttribute $ixNetSG_curObj/testSetup/variableLoop -maxValue 0
ixNet setAttribute $ixNetSG_curObj/testSetup/variableLoop -initialValue 0
ixNet setAttribute $ixNetSG_curObj/testSetup/variableLoop -resolution 0
ixNet setAttribute $ixNetSG_curObj/testSetup/variableLoop -acceptableFrameLoss 0
ixNet setAttribute $ixNetSG_curObj/testSetup/additionalLoop -algorithm unchanged
ixNet setAttribute $ixNetSG_curObj/testSetup/additionalLoop -step 0
ixNet setAttribute $ixNetSG_curObj/testSetup/additionalLoop -valueList [list ]
ixNet setAttribute $ixNetSG_curObj/testSetup/additionalLoop -count 1
ixNet setAttribute $ixNetSG_curObj/testSetup/additionalLoop -selectedAdditionalLoopParameter frameSize
ixNet setAttribute $ixNetSG_curObj/testSetup/additionalLoop -maxValue 0
ixNet setAttribute $ixNetSG_curObj/testSetup/additionalLoop -value 0
ixNet setAttribute $ixNetSG_curObj/testSetup/additionalLoop -initialValue 0
ixNet setAttribute $ixNetSG_curObj/protocols -startBehavior startWithCurrent
ixNet setAttribute $ixNetSG_curObj/protocols -waitAfterStart 0
ixNet setAttribute $ixNetSG_curObj/protocols -waitAfterStop 0
ixNet setAttribute $ixNetSG_curObj/traffic -learningFrequency oncePerTest
ixNet setAttribute $ixNetSG_curObj/traffic -l2FrameSizeType sameAsStream
ixNet setAttribute $ixNetSG_curObj/traffic -delayAfterTransmit 5
ixNet setAttribute $ixNetSG_curObj/traffic -l3RepeatInterval 2
ixNet setAttribute $ixNetSG_curObj/traffic -l3RepeatCount 3
ixNet setAttribute $ixNetSG_curObj/traffic -learningStartDelay 0
ixNet setAttribute $ixNetSG_curObj/traffic -trafficStartDelay 5
ixNet setAttribute $ixNetSG_curObj/traffic -generateStreams True
ixNet setAttribute $ixNetSG_curObj/traffic -enableLearning False
ixNet setAttribute $ixNetSG_curObj/traffic -l2FrameSize 128
ixNet setAttribute $ixNetSG_curObj/traffic -enableStaggeredTransmit False
ixNet setAttribute $ixNetSG_curObj/traffic -l2BurstCount 1
ixNet setAttribute $ixNetSG_curObj/traffic -l3Gap 1
ixNet setAttribute $ixNetSG_curObj/traffic -l2Rate 1
ixNet setAttribute $ixNetSG_curObj/runParameters -enableLatencyCriteria False
ixNet setAttribute $ixNetSG_curObj/runParameters -numTrials 1
ixNet setAttribute $ixNetSG_curObj/runParameters -ratePortType averagePort
ixNet setAttribute $ixNetSG_curObj/runParameters -enableRatePassCriteria False
ixNet setAttribute $ixNetSG_curObj/runParameters -latencyUnit microSeconds
ixNet setAttribute $ixNetSG_curObj/runParameters -testDuration {00:00:20}
ixNet setAttribute $ixNetSG_curObj/runParameters -enableCalculateLatency False
ixNet setAttribute $ixNetSG_curObj/runParameters -latencyPortType averagePort
ixNet setAttribute $ixNetSG_curObj/runParameters -latencyLessThanEqualTo 10
ixNet setAttribute $ixNetSG_curObj/runParameters -rateGreaterThanEqualTo 10
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
return 0
}
ixNetScriptgenProc
