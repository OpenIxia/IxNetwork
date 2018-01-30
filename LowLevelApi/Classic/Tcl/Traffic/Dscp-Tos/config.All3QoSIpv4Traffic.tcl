# IxNetwork version: 5.30.41.294
# time of scriptgen: 3/24/2008, 7:10 PM

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
ixNet setAttribute $sg_top/traffic -enableStreamOrdering False
ixNet setAttribute $sg_top/traffic -globalIterationMode fixed
ixNet setAttribute $sg_top/traffic -enableMinFrameSize False
ixNet setAttribute $sg_top/traffic -enableStaggeredTransmit False
ixNet setAttribute $sg_top/traffic -largeErrorThreshhold 2
ixNet setAttribute $sg_top/traffic -waitTime 1
ixNet setAttribute $sg_top/traffic -macChangeOnFly False
ixNet setAttribute $sg_top/traffic -enableSequenceChecking False
ixNet setAttribute $sg_top/traffic -globalIterationCount 1
ixNet setAttribute $sg_top/traffic -enableMulticastScalingFactor False
ixNet setAttribute $sg_top/traffic -refreshLearnedInfoBeforeApply True
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
ixNet setAttribute $sg_vport -rxMode measure
ixNet setAttribute $sg_vport -connectedTo [ixNet getNull]
ixNet setAttribute $sg_vport -type ethernet
ixNet setAttribute $sg_vport -txMode sequential
ixNet setAttribute $sg_vport -name {Ethernet - 001}
ixNet setAttribute $sg_vport -transmitIgnoreLinkStatus False
ixNet setAttribute $sg_vport -txGapControlMode fixedMode
ixNet setAttribute $sg_vport -isPullOnly False
ixNet setAttribute $sg_vport/l1Config -currentType ethernet
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
ixNet setAttribute $sg_vport/capture -hardwareEnabled False
ixNet setAttribute $sg_vport/capture -softwareEnabled False
ixNet commit
set sg_vport [lindex [ixNet remapIds $sg_vport] 0]
set ixNetSG_Stack(1) $sg_vport

#
# configuring the object that corresponds to /vport:1/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.1/24 - 100:01 - 1}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 C8 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:c8"
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
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.30
ixNet setAttribute $sg_ipv4 -ip 1.1.1.1
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:2
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.2/24 - 100:01 - 2}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 CA }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:ca"
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
set ixNetSG_ref(5) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:2/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.31
ixNet setAttribute $sg_ipv4 -ip 1.1.1.2
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:3
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.3/24 - 100:01 - 3}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 CC }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:cc"
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
set ixNetSG_ref(7) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:3/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.32
ixNet setAttribute $sg_ipv4 -ip 1.1.1.3
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:4
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.4/24 - 100:01 - 4}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 CE }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:ce"
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
set ixNetSG_ref(9) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:4/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.33
ixNet setAttribute $sg_ipv4 -ip 1.1.1.4
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:5
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.5/24 - 100:01 - 5}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 D0 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:d0"
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
set ixNetSG_ref(11) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:5/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.34
ixNet setAttribute $sg_ipv4 -ip 1.1.1.5
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:6
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.6/24 - 100:01 - 6}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 D2 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:d2"
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
set ixNetSG_ref(13) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:6/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.35
ixNet setAttribute $sg_ipv4 -ip 1.1.1.6
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:7
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.7/24 - 100:01 - 7}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 D4 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:d4"
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
set ixNetSG_ref(15) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:7/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.36
ixNet setAttribute $sg_ipv4 -ip 1.1.1.7
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:8
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.8/24 - 100:01 - 8}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 D6 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:d6"
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
set ixNetSG_ref(17) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:8/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.37
ixNet setAttribute $sg_ipv4 -ip 1.1.1.8
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:9
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.9/24 - 100:01 - 9}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 D8 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:d8"
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
set ixNetSG_ref(19) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:9/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.38
ixNet setAttribute $sg_ipv4 -ip 1.1.1.9
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:10
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.10/24 - 100:01 - 10}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 DA }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:da"
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
set ixNetSG_ref(21) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:10/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.39
ixNet setAttribute $sg_ipv4 -ip 1.1.1.10
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:11
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.11/24 - 100:01 - 11}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 DC }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:dc"
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
set ixNetSG_ref(23) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:11/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.40
ixNet setAttribute $sg_ipv4 -ip 1.1.1.11
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:12
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.12/24 - 100:01 - 12}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 DE }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:de"
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
set ixNetSG_ref(25) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:12/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.41
ixNet setAttribute $sg_ipv4 -ip 1.1.1.12
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:13
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.13/24 - 100:01 - 13}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 E0 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:e0"
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
set ixNetSG_ref(27) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:13/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.42
ixNet setAttribute $sg_ipv4 -ip 1.1.1.13
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:14
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.14/24 - 100:01 - 14}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 E2 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:e2"
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
set ixNetSG_ref(29) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:14/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.43
ixNet setAttribute $sg_ipv4 -ip 1.1.1.14
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:15
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.15/24 - 100:01 - 15}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 E4 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:e4"
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
set ixNetSG_ref(31) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:15/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.44
ixNet setAttribute $sg_ipv4 -ip 1.1.1.15
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:16
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.16/24 - 100:01 - 16}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 E6 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:e6"
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
set ixNetSG_ref(33) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:16/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.45
ixNet setAttribute $sg_ipv4 -ip 1.1.1.16
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:17
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.17/24 - 100:01 - 17}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 E8 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:e8"
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
set ixNetSG_ref(35) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:17/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.46
ixNet setAttribute $sg_ipv4 -ip 1.1.1.17
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:18
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.18/24 - 100:01 - 18}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 EA }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:ea"
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
set ixNetSG_ref(37) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:18/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.47
ixNet setAttribute $sg_ipv4 -ip 1.1.1.18
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:19
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.19/24 - 100:01 - 19}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 EC }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:ec"
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
set ixNetSG_ref(39) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:19/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.48
ixNet setAttribute $sg_ipv4 -ip 1.1.1.19
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:20
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.20/24 - 100:01 - 20}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 EE }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:ee"
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
set ixNetSG_ref(41) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:20/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.49
ixNet setAttribute $sg_ipv4 -ip 1.1.1.20
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:21
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.21/24 - 100:01 - 21}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 F0 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:f0"
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
set ixNetSG_ref(43) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:21/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.50
ixNet setAttribute $sg_ipv4 -ip 1.1.1.21
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:22
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.22/24 - 100:01 - 22}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 F2 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:f2"
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
set ixNetSG_ref(45) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:22/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.51
ixNet setAttribute $sg_ipv4 -ip 1.1.1.22
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:23
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.23/24 - 100:01 - 23}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 F4 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:f4"
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
set ixNetSG_ref(47) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:23/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.52
ixNet setAttribute $sg_ipv4 -ip 1.1.1.23
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:24
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.24/24 - 100:01 - 24}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 F6 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:f6"
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
set ixNetSG_ref(49) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:24/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.53
ixNet setAttribute $sg_ipv4 -ip 1.1.1.24
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:25
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.25/24 - 100:01 - 25}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 F8 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:f8"
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
set ixNetSG_ref(51) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:25/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.54
ixNet setAttribute $sg_ipv4 -ip 1.1.1.25
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:26
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.26/24 - 100:01 - 26}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 FA }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:fa"
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
set ixNetSG_ref(53) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:26/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.55
ixNet setAttribute $sg_ipv4 -ip 1.1.1.26
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:27
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.27/24 - 100:01 - 27}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 FC }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:fc"
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
set ixNetSG_ref(55) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:27/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.56
ixNet setAttribute $sg_ipv4 -ip 1.1.1.27
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:28
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.28/24 - 100:01 - 28}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 42 FE }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:42:fe"
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
set ixNetSG_ref(57) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:28/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.57
ixNet setAttribute $sg_ipv4 -ip 1.1.1.28
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:29
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.1.29/24 - 100:01 - 29}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 00 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:00"
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
set ixNetSG_ref(59) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:29/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.58
ixNet setAttribute $sg_ipv4 -ip 1.1.1.29
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
ixNet setAttribute $sg_vport/capture -hardwareEnabled True
ixNet setAttribute $sg_vport/capture -softwareEnabled False
ixNet commit
set sg_vport [lindex [ixNet remapIds $sg_vport] 0]
set ixNetSG_Stack(1) $sg_vport

#
# configuring the object that corresponds to /vport:2/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.1/24 - 100:02 - 30}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 02 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:02"
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
set ixNetSG_ref(63) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:1/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.1
ixNet setAttribute $sg_ipv4 -ip 1.1.1.30
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:2
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.2/24 - 100:02 - 31}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 04 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:04"
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
set ixNetSG_ref(65) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:2/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.2
ixNet setAttribute $sg_ipv4 -ip 1.1.1.31
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:3
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.3/24 - 100:02 - 32}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 06 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:06"
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
set ixNetSG_ref(67) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:3/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.3
ixNet setAttribute $sg_ipv4 -ip 1.1.1.32
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:4
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.4/24 - 100:02 - 33}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 08 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:08"
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
set ixNetSG_ref(69) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:4/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.4
ixNet setAttribute $sg_ipv4 -ip 1.1.1.33
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:5
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.5/24 - 100:02 - 34}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 0A }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:0a"
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
set ixNetSG_ref(71) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:5/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.5
ixNet setAttribute $sg_ipv4 -ip 1.1.1.34
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:6
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.6/24 - 100:02 - 35}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 0C }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:0c"
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
set ixNetSG_ref(73) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:6/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.6
ixNet setAttribute $sg_ipv4 -ip 1.1.1.35
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:7
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.7/24 - 100:02 - 36}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 0E }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:0e"
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
set ixNetSG_ref(75) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:7/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.7
ixNet setAttribute $sg_ipv4 -ip 1.1.1.36
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:8
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.8/24 - 100:02 - 37}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 10 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:10"
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
set ixNetSG_ref(77) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:8/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.8
ixNet setAttribute $sg_ipv4 -ip 1.1.1.37
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:9
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.9/24 - 100:02 - 38}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 12 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:12"
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
set ixNetSG_ref(79) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:9/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.9
ixNet setAttribute $sg_ipv4 -ip 1.1.1.38
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:10
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.10/24 - 100:02 - 39}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 14 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:14"
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
set ixNetSG_ref(81) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:10/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.10
ixNet setAttribute $sg_ipv4 -ip 1.1.1.39
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:11
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.11/24 - 100:02 - 40}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 16 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:16"
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
set ixNetSG_ref(83) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:11/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.11
ixNet setAttribute $sg_ipv4 -ip 1.1.1.40
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:12
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.12/24 - 100:02 - 41}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 18 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:18"
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
set ixNetSG_ref(85) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:12/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.12
ixNet setAttribute $sg_ipv4 -ip 1.1.1.41
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:13
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.13/24 - 100:02 - 42}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 1A }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:1a"
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
set ixNetSG_ref(87) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:13/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.13
ixNet setAttribute $sg_ipv4 -ip 1.1.1.42
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:14
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.14/24 - 100:02 - 43}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 1C }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:1c"
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
set ixNetSG_ref(89) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:14/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.14
ixNet setAttribute $sg_ipv4 -ip 1.1.1.43
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:15
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.15/24 - 100:02 - 44}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 1E }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:1e"
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
set ixNetSG_ref(91) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:15/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.15
ixNet setAttribute $sg_ipv4 -ip 1.1.1.44
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:16
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.16/24 - 100:02 - 45}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 20 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:20"
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
set ixNetSG_ref(93) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:16/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.16
ixNet setAttribute $sg_ipv4 -ip 1.1.1.45
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:17
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.17/24 - 100:02 - 46}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 22 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:22"
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
set ixNetSG_ref(95) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:17/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.17
ixNet setAttribute $sg_ipv4 -ip 1.1.1.46
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:18
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.18/24 - 100:02 - 47}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 24 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:24"
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
set ixNetSG_ref(97) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:18/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.18
ixNet setAttribute $sg_ipv4 -ip 1.1.1.47
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:19
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.19/24 - 100:02 - 48}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 26 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:26"
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
set ixNetSG_ref(99) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:19/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.19
ixNet setAttribute $sg_ipv4 -ip 1.1.1.48
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:20
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.20/24 - 100:02 - 49}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 28 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:28"
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
set ixNetSG_ref(101) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:20/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.20
ixNet setAttribute $sg_ipv4 -ip 1.1.1.49
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:21
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.21/24 - 100:02 - 50}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 2A }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:2a"
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
set ixNetSG_ref(103) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:21/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.21
ixNet setAttribute $sg_ipv4 -ip 1.1.1.50
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:22
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.22/24 - 100:02 - 51}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 2C }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:2c"
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
set ixNetSG_ref(105) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:22/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.22
ixNet setAttribute $sg_ipv4 -ip 1.1.1.51
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:23
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.23/24 - 100:02 - 52}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 2E }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:2e"
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
set ixNetSG_ref(107) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:23/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.23
ixNet setAttribute $sg_ipv4 -ip 1.1.1.52
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:24
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.24/24 - 100:02 - 53}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 30 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:30"
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
set ixNetSG_ref(109) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:24/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.24
ixNet setAttribute $sg_ipv4 -ip 1.1.1.53
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:25
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.25/24 - 100:02 - 54}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 32 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:32"
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
set ixNetSG_ref(111) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:25/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.25
ixNet setAttribute $sg_ipv4 -ip 1.1.1.54
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:26
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.26/24 - 100:02 - 55}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 34 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:34"
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
set ixNetSG_ref(113) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:26/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.26
ixNet setAttribute $sg_ipv4 -ip 1.1.1.55
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:27
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.27/24 - 100:02 - 56}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 36 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:36"
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
set ixNetSG_ref(115) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:27/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.27
ixNet setAttribute $sg_ipv4 -ip 1.1.1.56
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:28
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.28/24 - 100:02 - 57}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 38 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:38"
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
set ixNetSG_ref(117) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:28/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.28
ixNet setAttribute $sg_ipv4 -ip 1.1.1.57
ixNet setAttribute $sg_ipv4 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:29
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {Connected - 1.1.2.29/24 - 100:02 - 58}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 3E FF FE 2A 43 3A }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:3e:2a:43:3a"
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
set ixNetSG_ref(119) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:29/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.29
ixNet setAttribute $sg_ipv4 -ip 1.1.1.58
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

###
### /testConfiguration area
###

#
# configuring the object that corresponds to /testConfiguration/custom:1
#
set sg_custom $ixNetSG_Stack(0)/testConfiguration/custom:1
ixNet setAttribute $sg_custom -selectedTest continuousDuration
ixNet commit
set sg_custom [lindex [ixNet remapIds $sg_custom] 0]
set ixNetSG_Stack(1) $sg_custom

#
# configuring the object that corresponds to /testConfiguration/custom:1/continuousDuration:1
#
set sg_continuousDuration $ixNetSG_Stack(1)/continuousDuration:1
ixNet setAttribute $sg_continuousDuration -selectedItems [list ]
ixNet setAttribute $sg_continuousDuration/testSetup -selectedVariableParameter percentLineRate
ixNet setAttribute $sg_continuousDuration/testSetup/variableLoop -backoff 0
ixNet setAttribute $sg_continuousDuration/testSetup/variableLoop -algorithm unchanged
ixNet setAttribute $sg_continuousDuration/testSetup/variableLoop -maxValue 0
ixNet setAttribute $sg_continuousDuration/testSetup/variableLoop -initialValue 0
ixNet setAttribute $sg_continuousDuration/testSetup/variableLoop -value 0
ixNet setAttribute $sg_continuousDuration/testSetup/variableLoop -stepValue 0
ixNet setAttribute $sg_continuousDuration/testSetup/variableLoop -resolution 0
ixNet setAttribute $sg_continuousDuration/testSetup/variableLoop -valueList [list ]
ixNet setAttribute $sg_continuousDuration/testSetup/variableLoop -acceptableFrameLoss 0
ixNet setAttribute $sg_continuousDuration/testSetup/variableLoop -minValue 0
ixNet setAttribute $sg_continuousDuration/testSetup/additionalLoop -selectedAdditionalLoopParameter frameSize
ixNet setAttribute $sg_continuousDuration/testSetup/additionalLoop -algorithm unchanged
ixNet setAttribute $sg_continuousDuration/testSetup/additionalLoop -maxValue 0
ixNet setAttribute $sg_continuousDuration/testSetup/additionalLoop -initialValue 0
ixNet setAttribute $sg_continuousDuration/testSetup/additionalLoop -value 0
ixNet setAttribute $sg_continuousDuration/testSetup/additionalLoop -valueList [list ]
ixNet setAttribute $sg_continuousDuration/testSetup/additionalLoop -step 0
ixNet setAttribute $sg_continuousDuration/testSetup/additionalLoop -count 1
ixNet setAttribute $sg_continuousDuration/protocols -startBehavior startWithCurrent
ixNet setAttribute $sg_continuousDuration/protocols -waitAfterStop 0
ixNet setAttribute $sg_continuousDuration/protocols -waitAfterStart 0
ixNet setAttribute $sg_continuousDuration/traffic -learningStartDelay 0
ixNet setAttribute $sg_continuousDuration/traffic -l3RepeatCount 3
ixNet setAttribute $sg_continuousDuration/traffic -l3Gap 1
ixNet setAttribute $sg_continuousDuration/traffic -l2FrameSizeType sameAsStream
ixNet setAttribute $sg_continuousDuration/traffic -learningFrequency oncePerTest
ixNet setAttribute $sg_continuousDuration/traffic -l3RepeatInterval 2
ixNet setAttribute $sg_continuousDuration/traffic -enableStaggeredTransmit False
ixNet setAttribute $sg_continuousDuration/traffic -trafficStartDelay 5
ixNet setAttribute $sg_continuousDuration/traffic -l2BurstCount 1
ixNet setAttribute $sg_continuousDuration/traffic -l2FrameSize 128
ixNet setAttribute $sg_continuousDuration/traffic -delayAfterTransmit 5
ixNet setAttribute $sg_continuousDuration/traffic -generateStreams True
ixNet setAttribute $sg_continuousDuration/traffic -enableLearning False
ixNet setAttribute $sg_continuousDuration/traffic -l2Rate 1
ixNet setAttribute $sg_continuousDuration/runParameters -enableCalculateLatency False
ixNet setAttribute $sg_continuousDuration/runParameters -latencyLessThanEqualTo 10
ixNet setAttribute $sg_continuousDuration/runParameters -enableRatePassCriteria False
ixNet setAttribute $sg_continuousDuration/runParameters -latencyPortType averagePort
ixNet setAttribute $sg_continuousDuration/runParameters -latencyUnit microSeconds
ixNet setAttribute $sg_continuousDuration/runParameters -testDuration {00:00:20}
ixNet setAttribute $sg_continuousDuration/runParameters -ratePortType averagePort
ixNet setAttribute $sg_continuousDuration/runParameters -enableLatencyCriteria False
ixNet setAttribute $sg_continuousDuration/runParameters -numTrials 1
ixNet setAttribute $sg_continuousDuration/runParameters -rateGreaterThanEqualTo 10
ixNet commit
set sg_continuousDuration [lindex [ixNet remapIds $sg_continuousDuration] 0]

###
### /traffic area
###

#
# configuring the object that corresponds to /traffic/trafficItem:1
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI0-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType TOS
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "000 Routine"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:1/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(3)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(63)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:1/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
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

#
# configuring the object that corresponds to /traffic/trafficItem:2
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI1-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType TOS
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "001 Priority"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:2/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(5)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(65)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:2/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:2/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:3
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI2-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType TOS
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "010 Immediate"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:3/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(7)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(67)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:3/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:3/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:4
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI3-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType TOS
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "011 Flash"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:4/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(9)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(69)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:4/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:4/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:5
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI4-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType TOS
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "100 Flash Override"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:5/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(11)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(71)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:5/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:5/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:6
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI5-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType TOS
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "101 CRITIC/ECP"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:6/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(13)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(73)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:6/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:6/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:7
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI6-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType TOS
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "110 Internetwork Control"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:7/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(15)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(75)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:7/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:7/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:8
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI7-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType TOS
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "111 Network Control"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:8/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(17)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(77)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:8/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:8/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:9
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI8-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "Default"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:9/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(19)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(79)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:9/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:9/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:10
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI9-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "AF11"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:10/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(21)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(81)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:10/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:10/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:11
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI10-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "AF12"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:11/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(23)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(83)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:11/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:11/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:12
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI11-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "AF13"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:12/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(25)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(85)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:12/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:12/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:13
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI12-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "AF21"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:13/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(27)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(87)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:13/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:13/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:14
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI13-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "AF22"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:14/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(29)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(89)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:14/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:14/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:15
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI14-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "AF23"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:15/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(31)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(91)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:15/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:15/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:16
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI15-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "AF31"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:16/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(33)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(93)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:16/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:16/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:17
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI16-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "AF32"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:17/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(35)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(95)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:17/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:17/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:18
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI17-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "AF33"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:18/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(37)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(97)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:18/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:18/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:19
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI18-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "AF41"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:19/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(39)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(99)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:19/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:19/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:20
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI19-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "AF42"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:20/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(41)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(101)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:20/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:20/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:21
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI20-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "AF43"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:21/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(43)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(103)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:21/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:21/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:22
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI21-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "EF"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:22/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(45)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(105)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:22/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:22/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:23
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI22-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "C1"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:23/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(47)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(107)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:23/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:23/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:24
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI23-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "C2"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:24/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(49)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(109)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:24/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:24/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:25
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI24-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "C3"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:25/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(51)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(111)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:25/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:25/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:26
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI25-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "C4"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:26/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(53)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(113)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:26/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:26/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:27
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI26-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "C5"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:27/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(55)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(115)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:27/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:27/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:28
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI27-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "C6"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:28/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(57)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(117)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:28/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:28/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:29
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setAttribute $sg_trafficItem -allowSelfDestined False
ixNet setAttribute $sg_trafficItem -payloadType incByte
ixNet setAttribute $sg_trafficItem -encapsulationType nonMpls
ixNet setAttribute $sg_trafficItem -routeMesh oneToOne
ixNet setAttribute $sg_trafficItem -endpointType ipv4
ixNet setAttribute $sg_trafficItem -streamPackingMode optimalPacking
ixNet setAttribute $sg_trafficItem -forceError noError
ixNet setAttribute $sg_trafficItem -name {TI28-TRAFFICTESTITEM}
ixNet setAttribute $sg_trafficItem -enabled True
ixNet setAttribute $sg_trafficItem -hostsPerNetwork 1
ixNet setAttribute $sg_trafficItem -srcDestMesh oneToOne
ixNet setAttribute $sg_trafficItem -payloadData {}
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerBurst 100
ixNet setAttribute $sg_trafficItem/rateOptions -packetCountType auto
ixNet setAttribute $sg_trafficItem/rateOptions -enforceMinGap 12
ixNet setAttribute $sg_trafficItem/rateOptions -txDelay 0
ixNet setAttribute $sg_trafficItem/rateOptions -lineRate 10
ixNet setAttribute $sg_trafficItem/rateOptions -burstsPerStream 1
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterStreamGap False
ixNet setAttribute $sg_trafficItem/rateOptions -packetsPerSecond 1
ixNet setAttribute $sg_trafficItem/rateOptions -packetGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -enableInterBurstGap False
ixNet setAttribute $sg_trafficItem/rateOptions -interStreamGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -interBurstGap 64
ixNet setAttribute $sg_trafficItem/rateOptions -rateMode packetsPerSecond
ixNet setAttribute $sg_trafficItem/rateOptions -bitRate 100000
ixNet setAttribute $sg_trafficItem/frameOptions -frameSizeMode fixed
ixNet setAttribute $sg_trafficItem/packetOptions -qosType DSCP
ixNet setAttribute $sg_trafficItem/packetOptions -destPort 0
ixNet setAttribute $sg_trafficItem/packetOptions -qosValue "C7"
ixNet setAttribute $sg_trafficItem/packetOptions -desiredL4ProtocolType None
ixNet setAttribute $sg_trafficItem/packetOptions -sourcePort 0
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:29/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(59)]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(119)]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:29/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -selectedTrackBy none
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:29/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]
return 0
}

ixNetScriptgenProc
