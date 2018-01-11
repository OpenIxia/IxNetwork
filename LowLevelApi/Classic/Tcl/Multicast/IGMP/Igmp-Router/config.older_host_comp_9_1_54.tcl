# IxNetwork version: 5.30.67.45
# time of scriptgen: 4/3/2008, 10:20 AM

package require IxTclNetwork
proc ixNetScriptgenProc {} {
ixNet rollback
ixNet execute newConfig
set ixNetSG_Stack(0) [ixNet getRoot]

#
# setting global options
#
set sg_top [ixNet getRoot]
ixNet setAttribute $sg_top/testConfiguration -enableAbortIfLinkDown False
ixNet setAttribute $sg_top/testConfiguration -comments {}
ixNet setAttribute $sg_top/testConfiguration -selectedSuite custom
ixNet setAttribute $sg_top/testConfiguration -enableRebootCpu False
ixNet setAttribute $sg_top/testConfiguration -enableSwitchToResult True
ixNet setAttribute $sg_top/testConfiguration -enableCapture False
ixNet setAttribute $sg_top/testConfiguration -sleepTimeAfterReboot 10
ixNet setAttribute $sg_top/testConfiguration -linkDownTimeout 5
ixNet setAttribute $sg_top/testConfiguration -productLabel {Your switch/router name here}
ixNet setAttribute $sg_top/testConfiguration -serialNumber {Your switch/router serial number here}
ixNet setAttribute $sg_top/testConfiguration -enableCheckLinkState False
ixNet setAttribute $sg_top/testConfiguration -enableSwitchToStats True
ixNet setAttribute $sg_top/testConfiguration -version {Your firmware version here}
ixNet setAttribute $sg_top/testConfiguration -enableGenerateReportAfterRun False
ixNet setAttribute $sg_top/traffic -enableDestMacRetry True
ixNet setAttribute $sg_top/traffic -enableStreamOrdering False
ixNet setAttribute $sg_top/traffic -globalIterationMode continuous
ixNet setAttribute $sg_top/traffic -enableMinFrameSize False
ixNet setAttribute $sg_top/traffic -destMacRetryDelay 5
ixNet setAttribute $sg_top/traffic -enableStaggeredTransmit False
ixNet setAttribute $sg_top/traffic -largeErrorThreshhold 2
ixNet setAttribute $sg_top/traffic -destMacRetryCount 1
ixNet setAttribute $sg_top/traffic -waitTime 1
ixNet setAttribute $sg_top/traffic -macChangeOnFly False
ixNet setAttribute $sg_top/traffic -enableSequenceChecking False
ixNet setAttribute $sg_top/traffic -globalIterationCount 1
ixNet setAttribute $sg_top/traffic -enableMulticastScalingFactor False
ixNet setAttribute $sg_top/traffic -refreshLearnedInfoBeforeApply False
ixNet setAttribute $sg_top/traffic -latencyBinType cutThroughLatency
ixNet setAttribute $sg_top/availableHardware -isOffChassis False
ixNet setAttribute $sg_top/availableHardware -offChassisHwM {}
ixNet setAttribute $sg_top/globals/interfaces -arpOnLinkup True
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
ixNet setAttribute $sg_vport -rxMode capture
ixNet setAttribute $sg_vport -connectedTo [ixNet getNull]
ixNet setAttribute $sg_vport -type ethernet
ixNet setAttribute $sg_vport -txMode sequential
ixNet setAttribute $sg_vport -name {Ethernet - 001}
ixNet setAttribute $sg_vport -transmitIgnoreLinkStatus False
ixNet setAttribute $sg_vport -txGapControlMode fixedMode
ixNet setAttribute $sg_vport -isPullOnly False
ixNet setAttribute $sg_vport/l1Config -currentType ethernet
ixNet setAttribute $sg_vport/protocols/arp -enabled True
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
ixNet setAttribute $sg_vport/protocols/cfm -enabled False
ixNet setAttribute $sg_vport/protocols/cfm -receiveCcm True
ixNet setAttribute $sg_vport/protocols/cfm -sendCcm True
ixNet setAttribute $sg_vport/protocols/eigrp -enabled False
ixNet setAttribute $sg_vport/protocols/igmp -enabled True
ixNet setAttribute $sg_vport/protocols/igmp -numberOfGroups 0
ixNet setAttribute $sg_vport/protocols/igmp -numberOfQueries 0
ixNet setAttribute $sg_vport/protocols/igmp -queryTimePeriod 0
ixNet setAttribute $sg_vport/protocols/igmp -sendLeaveOnStop True
ixNet setAttribute $sg_vport/protocols/igmp -statsEnabled True
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
ixNet setAttribute $sg_vport/protocols/mld -numberOfQueries 0
ixNet setAttribute $sg_vport/protocols/mld -queryTimePeriod 0
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
ixNet setAttribute $sg_vport/protocols/ping -enabled True
ixNet setAttribute $sg_vport/protocols/rip -enabled False
ixNet setAttribute $sg_vport/protocols/ripng -enabled False
ixNet setAttribute $sg_vport/protocols/rsvp -enableBgpOverLsp True
ixNet setAttribute $sg_vport/protocols/rsvp -enabled False
ixNet setAttribute $sg_vport/protocols/stp -enabled False
ixNet setAttribute $sg_vport/capture -hardwareEnabled True
ixNet setAttribute $sg_vport/capture -softwareEnabled True
ixNet commit
set sg_vport [lindex [ixNet remapIds $sg_vport] 0]
set ixNetSG_Stack(1) $sg_vport

#
# configuring the object that corresponds to /vport:1/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - ProtocolInterface - 100:01 - 1}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 7C FF FE F0 2D 18 }
ixNet setAttribute $sg_interface -mtu 1500
ixNet setAttribute $sg_interface -type default
ixNet setAttribute $sg_interface/atm -encapsulation llcBridgeFcs
ixNet setAttribute $sg_interface/atm -vci 32
ixNet setAttribute $sg_interface/atm -vpi 0
ixNet setAttribute $sg_interface/dhcpV4Properties -clientId {}
ixNet setAttribute $sg_interface/dhcpV4Properties -enabled False
ixNet setAttribute $sg_interface/dhcpV4Properties -renewTimer 0
ixNet setAttribute $sg_interface/dhcpV4Properties -requestRate 0
ixNet setAttribute $sg_interface/dhcpV4Properties -serverId 0.0.0.0
ixNet setAttribute $sg_interface/dhcpV4Properties -tlvs [list ]
ixNet setAttribute $sg_interface/dhcpV4Properties -vendorId {}
ixNet setAttribute $sg_interface/dhcpV6Properties -enabled False
ixNet setAttribute $sg_interface/dhcpV6Properties -iaId 0
ixNet setAttribute $sg_interface/dhcpV6Properties -iaType temporary
ixNet setAttribute $sg_interface/dhcpV6Properties -renewTimer 0
ixNet setAttribute $sg_interface/dhcpV6Properties -requestRate 0
ixNet setAttribute $sg_interface/dhcpV6Properties -tlvs [list ]
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:7c:f0:2d:18"
ixNet setAttribute $sg_interface/ethernet -mtu 1500
ixNet setAttribute $sg_interface/ethernet -uidFromMac True
ixNet setAttribute $sg_interface/gre -dest 0.0.0.0
ixNet setAttribute $sg_interface/gre -inKey 0
ixNet setAttribute $sg_interface/gre -outKey 0
ixNet setAttribute $sg_interface/gre -source [ixNet getNull]
ixNet setAttribute $sg_interface/gre -useChecksum False
ixNet setAttribute $sg_interface/gre -useKey False
ixNet setAttribute $sg_interface/gre -useSequence False
ixNet setAttribute $sg_interface/unconnected -connectedVia [ixNet getNull]
ixNet setAttribute $sg_interface/vlan -tpid {0x8100}
ixNet setAttribute $sg_interface/vlan -vlanCount 1
ixNet setAttribute $sg_interface/vlan -vlanEnable False
ixNet setAttribute $sg_interface/vlan -vlanId {1}
ixNet setAttribute $sg_interface/vlan -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(3) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:1/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 11.1.1.5
ixNet setAttribute $sg_ipv4 -ip 11.1.1.1
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/l1Config/ethernet
#
set sg_ethernet $ixNetSG_Stack(1)/l1Config/ethernet
ixNet setAttribute $sg_ethernet -speed speed100fd
ixNet setAttribute $sg_ethernet -media copper
ixNet setAttribute $sg_ethernet -autoNegotiate True
ixNet setAttribute $sg_ethernet -loopback False
ixNet commit
set sg_ethernet [lindex [ixNet remapIds $sg_ethernet] 0]
set ixNetSG_Stack(2) $sg_ethernet

#
# configuring the object that corresponds to /vport:1/l1Config/ethernet/oam
#
set sg_oam $ixNetSG_Stack(2)/oam
ixNet setAttribute $sg_oam -enabled False
ixNet commit
set sg_oam [lindex [ixNet remapIds $sg_oam] 0]

#
# configuring the object that corresponds to /vport:1/protocols/igmp/host:1
#
set sg_host [ixNet add $ixNetSG_Stack(1)/protocols/igmp host]
ixNet setAttribute $sg_host -enabled False
ixNet setAttribute $sg_host -gqResponseMode True
ixNet setAttribute $sg_host -interfaceId [ixNet getNull]
ixNet setAttribute $sg_host -reportFreq 120
ixNet setAttribute $sg_host -respToQueryImmediately False
ixNet setAttribute $sg_host -routerAlert True
ixNet setAttribute $sg_host -sqResponseMode True
ixNet setAttribute $sg_host -suppressReports False
ixNet setAttribute $sg_host -upResponseMode False
ixNet setAttribute $sg_host -version igmpv2
ixNet commit
set sg_host [lindex [ixNet remapIds $sg_host] 0]

#
# configuring the object that corresponds to /vport:1/protocols/igmp/querier:1
#
set sg_querier [ixNet add $ixNetSG_Stack(1)/protocols/igmp querier]
ixNet setAttribute $sg_querier -discardLearnedInfo False
ixNet setAttribute $sg_querier -enabled True
ixNet setAttribute $sg_querier -generalQueryInterval 60
ixNet setAttribute $sg_querier -gqResponseInterval 10000
ixNet setAttribute $sg_querier -interfaceId $ixNetSG_ref(3)
ixNet setAttribute $sg_querier -robustnessVariable 2
ixNet setAttribute $sg_querier -routerAlert True
ixNet setAttribute $sg_querier -sqResponseInterval 5000
ixNet setAttribute $sg_querier -sqTransmissionCount 4
ixNet setAttribute $sg_querier -startupQueryCount 2
ixNet setAttribute $sg_querier -supportElection True
ixNet setAttribute $sg_querier -supportOlderVersionHost True
ixNet setAttribute $sg_querier -supportOlderVersionQuerier True
ixNet setAttribute $sg_querier -version igmpv3
ixNet commit
set sg_querier [lindex [ixNet remapIds $sg_querier] 0]

#
# configuring the object that corresponds to /vport:2
#
set sg_vport [ixNet add $ixNetSG_Stack(0) vport]
ixNet setAttribute $sg_vport -rxMode capture
ixNet setAttribute $sg_vport -connectedTo [ixNet getNull]
ixNet setAttribute $sg_vport -type ethernet
ixNet setAttribute $sg_vport -txMode sequential
ixNet setAttribute $sg_vport -name {Ethernet - 002}
ixNet setAttribute $sg_vport -transmitIgnoreLinkStatus False
ixNet setAttribute $sg_vport -txGapControlMode fixedMode
ixNet setAttribute $sg_vport -isPullOnly False
ixNet setAttribute $sg_vport/l1Config -currentType ethernet
ixNet setAttribute $sg_vport/protocols/arp -enabled True
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
ixNet setAttribute $sg_vport/protocols/cfm -enabled False
ixNet setAttribute $sg_vport/protocols/cfm -receiveCcm True
ixNet setAttribute $sg_vport/protocols/cfm -sendCcm True
ixNet setAttribute $sg_vport/protocols/eigrp -enabled False
ixNet setAttribute $sg_vport/protocols/igmp -enabled True
ixNet setAttribute $sg_vport/protocols/igmp -numberOfGroups 0
ixNet setAttribute $sg_vport/protocols/igmp -numberOfQueries 0
ixNet setAttribute $sg_vport/protocols/igmp -queryTimePeriod 0
ixNet setAttribute $sg_vport/protocols/igmp -sendLeaveOnStop True
ixNet setAttribute $sg_vport/protocols/igmp -statsEnabled True
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
ixNet setAttribute $sg_vport/protocols/mld -numberOfQueries 0
ixNet setAttribute $sg_vport/protocols/mld -queryTimePeriod 0
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
ixNet setAttribute $sg_vport/protocols/ping -enabled True
ixNet setAttribute $sg_vport/protocols/rip -enabled False
ixNet setAttribute $sg_vport/protocols/ripng -enabled False
ixNet setAttribute $sg_vport/protocols/rsvp -enableBgpOverLsp True
ixNet setAttribute $sg_vport/protocols/rsvp -enabled False
ixNet setAttribute $sg_vport/protocols/stp -enabled False
ixNet setAttribute $sg_vport/capture -hardwareEnabled True
ixNet setAttribute $sg_vport/capture -softwareEnabled True
ixNet commit
set sg_vport [lindex [ixNet remapIds $sg_vport] 0]
set ixNetSG_Stack(1) $sg_vport

#
# configuring the object that corresponds to /vport:2/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - ProtocolInterface - 100:02 - 2}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 7C FF FE F0 5A 43 }
ixNet setAttribute $sg_interface -mtu 1500
ixNet setAttribute $sg_interface -type default
ixNet setAttribute $sg_interface/atm -encapsulation llcBridgeFcs
ixNet setAttribute $sg_interface/atm -vci 32
ixNet setAttribute $sg_interface/atm -vpi 0
ixNet setAttribute $sg_interface/dhcpV4Properties -clientId {}
ixNet setAttribute $sg_interface/dhcpV4Properties -enabled False
ixNet setAttribute $sg_interface/dhcpV4Properties -renewTimer 0
ixNet setAttribute $sg_interface/dhcpV4Properties -requestRate 0
ixNet setAttribute $sg_interface/dhcpV4Properties -serverId 0.0.0.0
ixNet setAttribute $sg_interface/dhcpV4Properties -tlvs [list ]
ixNet setAttribute $sg_interface/dhcpV4Properties -vendorId {}
ixNet setAttribute $sg_interface/dhcpV6Properties -enabled False
ixNet setAttribute $sg_interface/dhcpV6Properties -iaId 0
ixNet setAttribute $sg_interface/dhcpV6Properties -iaType temporary
ixNet setAttribute $sg_interface/dhcpV6Properties -renewTimer 0
ixNet setAttribute $sg_interface/dhcpV6Properties -requestRate 0
ixNet setAttribute $sg_interface/dhcpV6Properties -tlvs [list ]
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:7c:f0:5a:43"
ixNet setAttribute $sg_interface/ethernet -mtu 1500
ixNet setAttribute $sg_interface/ethernet -uidFromMac True
ixNet setAttribute $sg_interface/gre -dest 0.0.0.0
ixNet setAttribute $sg_interface/gre -inKey 0
ixNet setAttribute $sg_interface/gre -outKey 0
ixNet setAttribute $sg_interface/gre -source [ixNet getNull]
ixNet setAttribute $sg_interface/gre -useChecksum False
ixNet setAttribute $sg_interface/gre -useKey False
ixNet setAttribute $sg_interface/gre -useSequence False
ixNet setAttribute $sg_interface/unconnected -connectedVia [ixNet getNull]
ixNet setAttribute $sg_interface/vlan -tpid {0x8100}
ixNet setAttribute $sg_interface/vlan -vlanCount 1
ixNet setAttribute $sg_interface/vlan -vlanEnable False
ixNet setAttribute $sg_interface/vlan -vlanId {1}
ixNet setAttribute $sg_interface/vlan -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(10) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:1/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 11.1.1.1
ixNet setAttribute $sg_ipv4 -ip 11.1.1.5
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:2
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - ProtocolInterface - 100:02 - 3}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 7C FF FE F0 5A 44 }
ixNet setAttribute $sg_interface -mtu 1500
ixNet setAttribute $sg_interface -type default
ixNet setAttribute $sg_interface/atm -encapsulation llcBridgeFcs
ixNet setAttribute $sg_interface/atm -vci 32
ixNet setAttribute $sg_interface/atm -vpi 0
ixNet setAttribute $sg_interface/dhcpV4Properties -clientId {}
ixNet setAttribute $sg_interface/dhcpV4Properties -enabled False
ixNet setAttribute $sg_interface/dhcpV4Properties -renewTimer 0
ixNet setAttribute $sg_interface/dhcpV4Properties -requestRate 0
ixNet setAttribute $sg_interface/dhcpV4Properties -serverId 0.0.0.0
ixNet setAttribute $sg_interface/dhcpV4Properties -tlvs [list ]
ixNet setAttribute $sg_interface/dhcpV4Properties -vendorId {}
ixNet setAttribute $sg_interface/dhcpV6Properties -enabled False
ixNet setAttribute $sg_interface/dhcpV6Properties -iaId 0
ixNet setAttribute $sg_interface/dhcpV6Properties -iaType temporary
ixNet setAttribute $sg_interface/dhcpV6Properties -renewTimer 0
ixNet setAttribute $sg_interface/dhcpV6Properties -requestRate 0
ixNet setAttribute $sg_interface/dhcpV6Properties -tlvs [list ]
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:7c:f0:5a:44"
ixNet setAttribute $sg_interface/ethernet -mtu 1500
ixNet setAttribute $sg_interface/ethernet -uidFromMac True
ixNet setAttribute $sg_interface/gre -dest 0.0.0.0
ixNet setAttribute $sg_interface/gre -inKey 0
ixNet setAttribute $sg_interface/gre -outKey 0
ixNet setAttribute $sg_interface/gre -source [ixNet getNull]
ixNet setAttribute $sg_interface/gre -useChecksum False
ixNet setAttribute $sg_interface/gre -useKey False
ixNet setAttribute $sg_interface/gre -useSequence False
ixNet setAttribute $sg_interface/unconnected -connectedVia [ixNet getNull]
ixNet setAttribute $sg_interface/vlan -tpid {0x8100}
ixNet setAttribute $sg_interface/vlan -vlanCount 1
ixNet setAttribute $sg_interface/vlan -vlanEnable False
ixNet setAttribute $sg_interface/vlan -vlanId {1}
ixNet setAttribute $sg_interface/vlan -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(12) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:2/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 11.1.1.1
ixNet setAttribute $sg_ipv4 -ip 11.1.1.6
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:3
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - ProtocolInterface - 100:02 - 4}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 7C FF FE F0 5A 45 }
ixNet setAttribute $sg_interface -mtu 1500
ixNet setAttribute $sg_interface -type default
ixNet setAttribute $sg_interface/atm -encapsulation llcBridgeFcs
ixNet setAttribute $sg_interface/atm -vci 32
ixNet setAttribute $sg_interface/atm -vpi 0
ixNet setAttribute $sg_interface/dhcpV4Properties -clientId {}
ixNet setAttribute $sg_interface/dhcpV4Properties -enabled False
ixNet setAttribute $sg_interface/dhcpV4Properties -renewTimer 0
ixNet setAttribute $sg_interface/dhcpV4Properties -requestRate 0
ixNet setAttribute $sg_interface/dhcpV4Properties -serverId 0.0.0.0
ixNet setAttribute $sg_interface/dhcpV4Properties -tlvs [list ]
ixNet setAttribute $sg_interface/dhcpV4Properties -vendorId {}
ixNet setAttribute $sg_interface/dhcpV6Properties -enabled False
ixNet setAttribute $sg_interface/dhcpV6Properties -iaId 0
ixNet setAttribute $sg_interface/dhcpV6Properties -iaType temporary
ixNet setAttribute $sg_interface/dhcpV6Properties -renewTimer 0
ixNet setAttribute $sg_interface/dhcpV6Properties -requestRate 0
ixNet setAttribute $sg_interface/dhcpV6Properties -tlvs [list ]
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:7c:f0:5a:45"
ixNet setAttribute $sg_interface/ethernet -mtu 1500
ixNet setAttribute $sg_interface/ethernet -uidFromMac True
ixNet setAttribute $sg_interface/gre -dest 0.0.0.0
ixNet setAttribute $sg_interface/gre -inKey 0
ixNet setAttribute $sg_interface/gre -outKey 0
ixNet setAttribute $sg_interface/gre -source [ixNet getNull]
ixNet setAttribute $sg_interface/gre -useChecksum False
ixNet setAttribute $sg_interface/gre -useKey False
ixNet setAttribute $sg_interface/gre -useSequence False
ixNet setAttribute $sg_interface/unconnected -connectedVia [ixNet getNull]
ixNet setAttribute $sg_interface/vlan -tpid {0x8100}
ixNet setAttribute $sg_interface/vlan -vlanCount 1
ixNet setAttribute $sg_interface/vlan -vlanEnable False
ixNet setAttribute $sg_interface/vlan -vlanId {1}
ixNet setAttribute $sg_interface/vlan -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(14) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:3/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 11.1.1.1
ixNet setAttribute $sg_ipv4 -ip 11.1.1.7
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/l1Config/ethernet
#
set sg_ethernet $ixNetSG_Stack(1)/l1Config/ethernet
ixNet setAttribute $sg_ethernet -speed speed100fd
ixNet setAttribute $sg_ethernet -media copper
ixNet setAttribute $sg_ethernet -autoNegotiate True
ixNet setAttribute $sg_ethernet -loopback False
ixNet commit
set sg_ethernet [lindex [ixNet remapIds $sg_ethernet] 0]
set ixNetSG_Stack(2) $sg_ethernet

#
# configuring the object that corresponds to /vport:2/l1Config/ethernet/oam
#
set sg_oam $ixNetSG_Stack(2)/oam
ixNet setAttribute $sg_oam -enabled False
ixNet commit
set sg_oam [lindex [ixNet remapIds $sg_oam] 0]

#
# configuring the object that corresponds to /vport:2/protocols/igmp/host:1
#
set sg_host [ixNet add $ixNetSG_Stack(1)/protocols/igmp host]
ixNet setAttribute $sg_host -enabled False
ixNet setAttribute $sg_host -gqResponseMode True
ixNet setAttribute $sg_host -interfaceId $ixNetSG_ref(10)
ixNet setAttribute $sg_host -reportFreq 120
ixNet setAttribute $sg_host -respToQueryImmediately False
ixNet setAttribute $sg_host -routerAlert True
ixNet setAttribute $sg_host -sqResponseMode True
ixNet setAttribute $sg_host -suppressReports False
ixNet setAttribute $sg_host -upResponseMode False
ixNet setAttribute $sg_host -version igmpv1
ixNet commit
set sg_host [lindex [ixNet remapIds $sg_host] 0]
set ixNetSG_Stack(2) $sg_host

#
# configuring the object that corresponds to /vport:2/protocols/igmp/host:1/group:1
#
set sg_group [ixNet add $ixNetSG_Stack(2) group]
ixNet setAttribute $sg_group -enablePacking False
ixNet setAttribute $sg_group -enabled True
ixNet setAttribute $sg_group -groupCount 1
ixNet setAttribute $sg_group -groupFrom 224.1.1.1
ixNet setAttribute $sg_group -incrementStep 1
ixNet setAttribute $sg_group -recordsPerFrame 0
ixNet setAttribute $sg_group -sourceMode exclude
ixNet setAttribute $sg_group -sourcesPerRecord 0
ixNet setAttribute $sg_group -updateRequired False
ixNet commit
set sg_group [lindex [ixNet remapIds $sg_group] 0]

#
# configuring the object that corresponds to /vport:2/protocols/igmp/host:2
#
set sg_host [ixNet add $ixNetSG_Stack(1)/protocols/igmp host]
ixNet setAttribute $sg_host -enabled False
ixNet setAttribute $sg_host -gqResponseMode True
ixNet setAttribute $sg_host -interfaceId $ixNetSG_ref(12)
ixNet setAttribute $sg_host -reportFreq 120
ixNet setAttribute $sg_host -respToQueryImmediately False
ixNet setAttribute $sg_host -routerAlert True
ixNet setAttribute $sg_host -sqResponseMode True
ixNet setAttribute $sg_host -suppressReports False
ixNet setAttribute $sg_host -upResponseMode False
ixNet setAttribute $sg_host -version igmpv2
ixNet commit
set sg_host [lindex [ixNet remapIds $sg_host] 0]
set ixNetSG_Stack(2) $sg_host

#
# configuring the object that corresponds to /vport:2/protocols/igmp/host:2/group:1
#
set sg_group [ixNet add $ixNetSG_Stack(2) group]
ixNet setAttribute $sg_group -enablePacking False
ixNet setAttribute $sg_group -enabled True
ixNet setAttribute $sg_group -groupCount 1
ixNet setAttribute $sg_group -groupFrom 224.1.1.1
ixNet setAttribute $sg_group -incrementStep 1
ixNet setAttribute $sg_group -recordsPerFrame 0
ixNet setAttribute $sg_group -sourceMode exclude
ixNet setAttribute $sg_group -sourcesPerRecord 0
ixNet setAttribute $sg_group -updateRequired False
ixNet commit
set sg_group [lindex [ixNet remapIds $sg_group] 0]

#
# configuring the object that corresponds to /vport:2/protocols/igmp/host:3
#
set sg_host [ixNet add $ixNetSG_Stack(1)/protocols/igmp host]
ixNet setAttribute $sg_host -enabled False
ixNet setAttribute $sg_host -gqResponseMode True
ixNet setAttribute $sg_host -interfaceId $ixNetSG_ref(14)
ixNet setAttribute $sg_host -reportFreq 120
ixNet setAttribute $sg_host -respToQueryImmediately False
ixNet setAttribute $sg_host -routerAlert True
ixNet setAttribute $sg_host -sqResponseMode True
ixNet setAttribute $sg_host -suppressReports False
ixNet setAttribute $sg_host -upResponseMode False
ixNet setAttribute $sg_host -version igmpv3
ixNet commit
set sg_host [lindex [ixNet remapIds $sg_host] 0]
set ixNetSG_Stack(2) $sg_host

#
# configuring the object that corresponds to /vport:2/protocols/igmp/host:3/group:1
#
set sg_group [ixNet add $ixNetSG_Stack(2) group]
ixNet setAttribute $sg_group -enablePacking False
ixNet setAttribute $sg_group -enabled True
ixNet setAttribute $sg_group -groupCount 1
ixNet setAttribute $sg_group -groupFrom 224.1.1.1
ixNet setAttribute $sg_group -incrementStep 1
ixNet setAttribute $sg_group -recordsPerFrame 0
ixNet setAttribute $sg_group -sourceMode exclude
ixNet setAttribute $sg_group -sourcesPerRecord 0
ixNet setAttribute $sg_group -updateRequired False
ixNet commit
set sg_group [lindex [ixNet remapIds $sg_group] 0]

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
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -backoff 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -algorithm unchanged
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -maxValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -initialValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -value 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -stepValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -resolution 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -valueList [list ]
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -acceptableFrameLoss 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -minValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -selectedAdditionalLoopParameter frameSize
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -algorithm unchanged
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -maxValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -initialValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -value 0
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -valueList [list ]
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -step 0
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -count 1
ixNet setAttribute $sg_fixedDuration/protocols -startBehavior startWithCurrent
ixNet setAttribute $sg_fixedDuration/protocols -waitAfterStop 0
ixNet setAttribute $sg_fixedDuration/protocols -waitAfterStart 0
ixNet setAttribute $sg_fixedDuration/traffic -learningStartDelay 0
ixNet setAttribute $sg_fixedDuration/traffic -l3RepeatCount 3
ixNet setAttribute $sg_fixedDuration/traffic -l3Gap 1
ixNet setAttribute $sg_fixedDuration/traffic -l2FrameSizeType sameAsStream
ixNet setAttribute $sg_fixedDuration/traffic -learningFrequency oncePerTest
ixNet setAttribute $sg_fixedDuration/traffic -l3RepeatInterval 2
ixNet setAttribute $sg_fixedDuration/traffic -enableStaggeredTransmit False
ixNet setAttribute $sg_fixedDuration/traffic -trafficStartDelay 5
ixNet setAttribute $sg_fixedDuration/traffic -l2BurstCount 1
ixNet setAttribute $sg_fixedDuration/traffic -l2FrameSize 128
ixNet setAttribute $sg_fixedDuration/traffic -delayAfterTransmit 5
ixNet setAttribute $sg_fixedDuration/traffic -generateStreams True
ixNet setAttribute $sg_fixedDuration/traffic -enableLearning False
ixNet setAttribute $sg_fixedDuration/traffic -l2Rate 1
ixNet setAttribute $sg_fixedDuration/runParameters -enableCalculateLatency False
ixNet setAttribute $sg_fixedDuration/runParameters -latencyLessThanEqualTo 10
ixNet setAttribute $sg_fixedDuration/runParameters -enableRatePassCriteria False
ixNet setAttribute $sg_fixedDuration/runParameters -latencyPortType averagePort
ixNet setAttribute $sg_fixedDuration/runParameters -latencyUnit microSeconds
ixNet setAttribute $sg_fixedDuration/runParameters -testDuration {00:00:20}
ixNet setAttribute $sg_fixedDuration/runParameters -ratePortType averagePort
ixNet setAttribute $sg_fixedDuration/runParameters -enableLatencyCriteria False
ixNet setAttribute $sg_fixedDuration/runParameters -numTrials 1
ixNet setAttribute $sg_fixedDuration/runParameters -rateGreaterThanEqualTo 10
ixNet commit
set sg_fixedDuration [lindex [ixNet remapIds $sg_fixedDuration] 0]
return 0
}

ixNetScriptgenProc
