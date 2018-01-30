# IxNetwork version: 5.30.67.56
# time of scriptgen: 4/14/2008, 5:36 PM

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
ixNet setAttribute $sg_vport -rxMode measure
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
ixNet setAttribute $sg_vport/protocols/cfm -enabled True
ixNet setAttribute $sg_vport/protocols/cfm -receiveCcm False
ixNet setAttribute $sg_vport/protocols/cfm -sendCcm False
ixNet setAttribute $sg_vport/protocols/eigrp -enabled False
ixNet setAttribute $sg_vport/protocols/igmp -enabled False
ixNet setAttribute $sg_vport/protocols/igmp -numberOfGroups 0
ixNet setAttribute $sg_vport/protocols/igmp -numberOfQueries 0
ixNet setAttribute $sg_vport/protocols/igmp -queryTimePeriod 0
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
ixNet setAttribute $sg_interface -description {Connected - ProtocolInterface - 100:01 - 3}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 00 FF FE 10 FF 82 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:00:10:ff:82"
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
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.2
ixNet setAttribute $sg_ipv4 -ip 1.1.1.1
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
# configuring the object that corresponds to /vport:1/protocols/cfm/bridge:1
#
set sg_bridge [ixNet add $ixNetSG_Stack(1)/protocols/cfm bridge]
ixNet setAttribute $sg_bridge -aisInterval oneSec
ixNet setAttribute $sg_bridge -bridgeId "00:00:98:52:00:01"
ixNet setAttribute $sg_bridge -enableAis False
ixNet setAttribute $sg_bridge -enableOutOfSequenceDetection False
ixNet setAttribute $sg_bridge -enabled True
ixNet setAttribute $sg_bridge -encapsulation ethernet
ixNet setAttribute $sg_bridge -etherType 35074
ixNet setAttribute $sg_bridge -function faultManagement
ixNet setAttribute $sg_bridge -operationMode y1731
ixNet setAttribute $sg_bridge -userBvlan noVlanId
ixNet setAttribute $sg_bridge -userBvlanId 1
ixNet setAttribute $sg_bridge -userBvlanPriority 0
ixNet setAttribute $sg_bridge -userBvlanTpId 0x8100
ixNet setAttribute $sg_bridge -userCvlan noVlanId
ixNet setAttribute $sg_bridge -userCvlanId 1
ixNet setAttribute $sg_bridge -userCvlanPriority 0
ixNet setAttribute $sg_bridge -userCvlanTpId 0x88A8
ixNet setAttribute $sg_bridge -userDelayType dm
ixNet setAttribute $sg_bridge -userDstMacAddress "00:00:00:00:00:02"
ixNet setAttribute $sg_bridge -userDstMepId 65535
ixNet setAttribute $sg_bridge -userLearnedInfoTimeOut 5000
ixNet setAttribute $sg_bridge -userMdLevel 0
ixNet setAttribute $sg_bridge -userPbbTeDelayType dm
ixNet setAttribute $sg_bridge -userSelectDstMepById False
ixNet setAttribute $sg_bridge -userSelectSrcMepById False
ixNet setAttribute $sg_bridge -userSendType unicast
ixNet setAttribute $sg_bridge -userShortMaName {0}
ixNet setAttribute $sg_bridge -userShortMaNameFormat characterString
ixNet setAttribute $sg_bridge -userSrcMacAddress "00:00:00:00:00:01"
ixNet setAttribute $sg_bridge -userSrcMepId 1
ixNet setAttribute $sg_bridge -userSvlan vlanId
ixNet setAttribute $sg_bridge -userSvlanId 1
ixNet setAttribute $sg_bridge -userSvlanPriority 0
ixNet setAttribute $sg_bridge -userSvlanTpId 0x8100
ixNet setAttribute $sg_bridge -userTransactionId 1
ixNet setAttribute $sg_bridge -userTtlInterval 64
ixNet commit
set sg_bridge [lindex [ixNet remapIds $sg_bridge] 0]
set ixNetSG_Stack(2) $sg_bridge

#
# configuring the object that corresponds to /vport:1/protocols/cfm/bridge:1/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -interfaceId $ixNetSG_ref(3)
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:1/protocols/cfm/bridge:1/link:1
#
set sg_link [ixNet add $ixNetSG_Stack(2) link]
ixNet setAttribute $sg_link -enabled True
ixNet setAttribute $sg_link -linkType pointToPoint
ixNet setAttribute $sg_link -moreMps [list ]
ixNet setAttribute $sg_link -mpOutwardsIxia [ixNet getNull]
ixNet setAttribute $sg_link -mpTowardsIxia [ixNet getNull]
ixNet commit
set sg_link [lindex [ixNet remapIds $sg_link] 0]
set ixNetSG_ref(9) $sg_link

#
# configuring the object that corresponds to /vport:1/protocols/cfm/bridge:1/mdLevel:1
#
set sg_mdLevel [ixNet add $ixNetSG_Stack(2) mdLevel]
ixNet setAttribute $sg_mdLevel -enabled True
ixNet setAttribute $sg_mdLevel -mdLevelId 0
ixNet setAttribute $sg_mdLevel -mdName {00 00 00 00 00 AC-0}
ixNet setAttribute $sg_mdLevel -mdNameFormat macAddress2OctetInteger
ixNet commit
set sg_mdLevel [lindex [ixNet remapIds $sg_mdLevel] 0]
set ixNetSG_ref(10) $sg_mdLevel

#
# configuring the object that corresponds to /vport:1/protocols/cfm/bridge:1/mp:1
#
set sg_mp [ixNet add $ixNetSG_Stack(2) mp]
ixNet setAttribute $sg_mp -cciInterval 1sec
ixNet setAttribute $sg_mp -enabled True
ixNet setAttribute $sg_mp -macAddress "00:00:00:00:00:01"
ixNet setAttribute $sg_mp -mdLevel $ixNetSG_ref(10)
ixNet setAttribute $sg_mp -megId {Ixia-00001}
ixNet setAttribute $sg_mp -megIdFormat iccBasedFormat
ixNet setAttribute $sg_mp -mepId 1
ixNet setAttribute $sg_mp -mipId 1
ixNet setAttribute $sg_mp -mpType mep
ixNet setAttribute $sg_mp -shortMaName {0-0}
ixNet setAttribute $sg_mp -shortMaNameFormat rfc2685VpnId
ixNet setAttribute $sg_mp -vlan [ixNet getNull]
ixNet commit
set sg_mp [lindex [ixNet remapIds $sg_mp] 0]
set ixNetSG_ref(11) $sg_mp
ixNet setAttribute $ixNetSG_ref(9) -mpOutwardsIxia $ixNetSG_ref(11)
ixNet commit

#
# configuring the object that corresponds to /vport:1/protocols/cfm/bridge:1/vlans:1
#
set sg_vlans [ixNet add $ixNetSG_Stack(2) vlans]
ixNet setAttribute $sg_vlans -cVlanId 1
ixNet setAttribute $sg_vlans -cVlanPriority 0
ixNet setAttribute $sg_vlans -cVlanTpId 0x8100
ixNet setAttribute $sg_vlans -enabled True
ixNet setAttribute $sg_vlans -sVlanId 1
ixNet setAttribute $sg_vlans -sVlanPriority 0
ixNet setAttribute $sg_vlans -sVlanTpId 0x8100
ixNet setAttribute $sg_vlans -type singleVlan
ixNet commit
set sg_vlans [lindex [ixNet remapIds $sg_vlans] 0]
set ixNetSG_ref(12) $sg_vlans
ixNet setAttribute $ixNetSG_ref(11) -vlan $ixNetSG_ref(12)
ixNet commit

#
# configuring the object that corresponds to /vport:2
#
set sg_vport [ixNet add $ixNetSG_Stack(0) vport]
ixNet setAttribute $sg_vport -rxMode measure
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
ixNet setAttribute $sg_vport/protocols/cfm -enabled True
ixNet setAttribute $sg_vport/protocols/cfm -receiveCcm False
ixNet setAttribute $sg_vport/protocols/cfm -sendCcm False
ixNet setAttribute $sg_vport/protocols/eigrp -enabled False
ixNet setAttribute $sg_vport/protocols/igmp -enabled False
ixNet setAttribute $sg_vport/protocols/igmp -numberOfGroups 0
ixNet setAttribute $sg_vport/protocols/igmp -numberOfQueries 0
ixNet setAttribute $sg_vport/protocols/igmp -queryTimePeriod 0
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
ixNet setAttribute $sg_interface -description {Connected - ProtocolInterface - 100:02 - 4}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 00 FF FE 10 FF 83 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:00:10:ff:83"
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
# configuring the object that corresponds to /vport:2/interface:1/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $sg_ipv4 -gateway 1.1.1.1
ixNet setAttribute $sg_ipv4 -ip 1.1.1.2
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
# configuring the object that corresponds to /vport:2/protocols/cfm/bridge:1
#
set sg_bridge [ixNet add $ixNetSG_Stack(1)/protocols/cfm bridge]
ixNet setAttribute $sg_bridge -aisInterval oneSec
ixNet setAttribute $sg_bridge -bridgeId "00:00:98:53:00:01"
ixNet setAttribute $sg_bridge -enableAis False
ixNet setAttribute $sg_bridge -enableOutOfSequenceDetection False
ixNet setAttribute $sg_bridge -enabled True
ixNet setAttribute $sg_bridge -encapsulation ethernet
ixNet setAttribute $sg_bridge -etherType 35074
ixNet setAttribute $sg_bridge -function faultManagement
ixNet setAttribute $sg_bridge -operationMode y1731
ixNet setAttribute $sg_bridge -userBvlan noVlanId
ixNet setAttribute $sg_bridge -userBvlanId 1
ixNet setAttribute $sg_bridge -userBvlanPriority 0
ixNet setAttribute $sg_bridge -userBvlanTpId 0x8100
ixNet setAttribute $sg_bridge -userCvlan noVlanId
ixNet setAttribute $sg_bridge -userCvlanId 1
ixNet setAttribute $sg_bridge -userCvlanPriority 0
ixNet setAttribute $sg_bridge -userCvlanTpId 0x88A8
ixNet setAttribute $sg_bridge -userDelayType dm
ixNet setAttribute $sg_bridge -userDstMacAddress "00:00:00:00:00:02"
ixNet setAttribute $sg_bridge -userDstMepId 65535
ixNet setAttribute $sg_bridge -userLearnedInfoTimeOut 5000
ixNet setAttribute $sg_bridge -userMdLevel 0
ixNet setAttribute $sg_bridge -userPbbTeDelayType dm
ixNet setAttribute $sg_bridge -userSelectDstMepById False
ixNet setAttribute $sg_bridge -userSelectSrcMepById False
ixNet setAttribute $sg_bridge -userSendType unicast
ixNet setAttribute $sg_bridge -userShortMaName {0}
ixNet setAttribute $sg_bridge -userShortMaNameFormat characterString
ixNet setAttribute $sg_bridge -userSrcMacAddress "00:00:00:00:00:01"
ixNet setAttribute $sg_bridge -userSrcMepId 1
ixNet setAttribute $sg_bridge -userSvlan vlanId
ixNet setAttribute $sg_bridge -userSvlanId 1
ixNet setAttribute $sg_bridge -userSvlanPriority 0
ixNet setAttribute $sg_bridge -userSvlanTpId 0x8100
ixNet setAttribute $sg_bridge -userTransactionId 1
ixNet setAttribute $sg_bridge -userTtlInterval 64
ixNet commit
set sg_bridge [lindex [ixNet remapIds $sg_bridge] 0]
set ixNetSG_Stack(2) $sg_bridge

#
# configuring the object that corresponds to /vport:2/protocols/cfm/bridge:1/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -interfaceId $ixNetSG_ref(14)
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:2/protocols/cfm/bridge:1/link:1
#
set sg_link [ixNet add $ixNetSG_Stack(2) link]
ixNet setAttribute $sg_link -enabled True
ixNet setAttribute $sg_link -linkType pointToPoint
ixNet setAttribute $sg_link -moreMps [list ]
ixNet setAttribute $sg_link -mpOutwardsIxia [ixNet getNull]
ixNet setAttribute $sg_link -mpTowardsIxia [ixNet getNull]
ixNet commit
set sg_link [lindex [ixNet remapIds $sg_link] 0]
set ixNetSG_ref(20) $sg_link

#
# configuring the object that corresponds to /vport:2/protocols/cfm/bridge:1/mdLevel:1
#
set sg_mdLevel [ixNet add $ixNetSG_Stack(2) mdLevel]
ixNet setAttribute $sg_mdLevel -enabled True
ixNet setAttribute $sg_mdLevel -mdLevelId 0
ixNet setAttribute $sg_mdLevel -mdName {00 00 00 00 00 AC-0}
ixNet setAttribute $sg_mdLevel -mdNameFormat macAddress2OctetInteger
ixNet commit
set sg_mdLevel [lindex [ixNet remapIds $sg_mdLevel] 0]
set ixNetSG_ref(21) $sg_mdLevel

#
# configuring the object that corresponds to /vport:2/protocols/cfm/bridge:1/mp:1
#
set sg_mp [ixNet add $ixNetSG_Stack(2) mp]
ixNet setAttribute $sg_mp -cciInterval 1sec
ixNet setAttribute $sg_mp -enabled True
ixNet setAttribute $sg_mp -macAddress "00:00:00:00:00:02"
ixNet setAttribute $sg_mp -mdLevel $ixNetSG_ref(21)
ixNet setAttribute $sg_mp -megId {Ixia-00001}
ixNet setAttribute $sg_mp -megIdFormat iccBasedFormat
ixNet setAttribute $sg_mp -mepId 2
ixNet setAttribute $sg_mp -mipId 2
ixNet setAttribute $sg_mp -mpType mep
ixNet setAttribute $sg_mp -shortMaName {0-0}
ixNet setAttribute $sg_mp -shortMaNameFormat rfc2685VpnId
ixNet setAttribute $sg_mp -vlan [ixNet getNull]
ixNet commit
set sg_mp [lindex [ixNet remapIds $sg_mp] 0]
set ixNetSG_ref(22) $sg_mp
ixNet setAttribute $ixNetSG_ref(20) -mpOutwardsIxia $ixNetSG_ref(22)
ixNet commit

#
# configuring the object that corresponds to /vport:2/protocols/cfm/bridge:1/vlans:1
#
set sg_vlans [ixNet add $ixNetSG_Stack(2) vlans]
ixNet setAttribute $sg_vlans -cVlanId 1
ixNet setAttribute $sg_vlans -cVlanPriority 0
ixNet setAttribute $sg_vlans -cVlanTpId 0x8100
ixNet setAttribute $sg_vlans -enabled True
ixNet setAttribute $sg_vlans -sVlanId 1
ixNet setAttribute $sg_vlans -sVlanPriority 0
ixNet setAttribute $sg_vlans -sVlanTpId 0x8100
ixNet setAttribute $sg_vlans -type singleVlan
ixNet commit
set sg_vlans [lindex [ixNet remapIds $sg_vlans] 0]
set ixNetSG_ref(23) $sg_vlans
ixNet setAttribute $ixNetSG_ref(22) -vlan $ixNetSG_ref(23)
ixNet commit

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
