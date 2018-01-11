# IxNetwork version: 5.35.54.331
# time of scriptgen: 11/12/2008, 2:30 PM

package require IxTclNetwork
proc ixNetScriptgenProc {} {
ixNet rollback
ixNet setSessionParameter version 5.35.54.331
ixNet execute newConfig
set ixNetSG_Stack(0) [ixNet getRoot]

#
# setting global options
#
set sg_top [ixNet getRoot]
ixNet setMultiAttrs $sg_top/testConfiguration \
 -enableGenerateReportAfterRun False \
 -selectedSuite custom \
 -sleepTimeAfterReboot 10 \
 -productLabel {Your switch/router name here} \
 -serialNumber {Your switch/router serial number here} \
 -enableCheckLinkState False \
 -enableAbortIfLinkDown False \
 -version {Your firmware version here} \
 -enableSwitchToStats True \
 -enableCapture False \
 -enableSwitchToResult True \
 -linkDownTimeout 5 \
 -enableRebootCpu False \
 -comments {}
ixNet setMultiAttrs $sg_top/traffic \
 -destMacRetryDelay 5 \
 -globalIterationCount 1 \
 -refreshLearnedInfoBeforeApply False \
 -enableMinFrameSize False \
 -largeErrorThreshhold 2 \
 -globalIterationMode continuous \
 -flowMeasurementMode normal \
 -enableMulticastScalingFactor False \
 -enableStreamOrdering False \
 -destMacRetryCount 1 \
 -waitTime 1 \
 -enableSequenceChecking False \
 -enableDestMacRetry True \
 -enableStaggeredTransmit False \
 -macChangeOnFly False \
 -sequenceCheckingMode SeqErrorThreshold \
 -latencyBinType cutThroughLatency
ixNet setMultiAttrs $sg_top/availableHardware \
 -isOffChassis False \
 -offChassisHwM {}
ixNet setMultiAttrs $sg_top/globals/interfaces \
 -arpOnLinkup False \
 -sendSingleArpPerGateway True
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
ixNet setMultiAttrs $sg_vport \
 -rxMode measure \
 -connectedTo ::ixNet::OBJ-null \
 -type ethernet \
 -txMode sequential \
 -name {Ethernet - 001} \
 -transmitIgnoreLinkStatus False \
 -txGapControlMode fixedMode \
 -isPullOnly False
ixNet setMultiAttrs $sg_vport/l1Config \
 -currentType ethernet
ixNet setMultiAttrs $sg_vport/protocols/arp \
 -enabled True
ixNet setMultiAttrs $sg_vport/protocols/bfd \
 -enabled False \
 -intervalValue 0 \
 -packetsPerInterval 0
ixNet setMultiAttrs $sg_vport/protocols/bgp \
 -enableExternalActiveConnect True \
 -enableInternalActiveConnect True \
 -enableLabelExchangeOverLsp True \
 -enabled False \
 -externalRetries 0 \
 -externalRetryDelay 120 \
 -internalRetries 0 \
 -internalRetryDelay 120
ixNet setMultiAttrs $sg_vport/protocols/cfm \
 -enableOptionalTlvValidation True \
 -enabled False \
 -receiveCcm True \
 -sendCcm True
ixNet setMultiAttrs $sg_vport/protocols/eigrp \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/igmp \
 -enabled False \
 -numberOfGroups 0 \
 -numberOfQueries 0 \
 -queryTimePeriod 0 \
 -sendLeaveOnStop True \
 -statsEnabled False \
 -timePeriod 0
ixNet setMultiAttrs $sg_vport/protocols/isis \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/lacp \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/ldp \
 -enableDiscardSelfAdvFecs False \
 -enableHelloJitter True \
 -enableLabelExchangeOverLsp True \
 -enabled False \
 -helloHoldTime 15 \
 -helloInterval 5 \
 -keepAliveHoldTime 30 \
 -keepAliveInterval 10 \
 -targetedHelloInterval 15 \
 -targetedHoldTime 45
ixNet setMultiAttrs $sg_vport/protocols/mld \
 -enableDoneOnStop True \
 -enabled False \
 -mldv2Report type143 \
 -numberOfGroups 0 \
 -numberOfQueries 0 \
 -queryTimePeriod 0 \
 -timePeriod 0
ixNet setMultiAttrs $sg_vport/protocols/ospf \
 -enableDrOrBdr False \
 -enabled True
ixNet setMultiAttrs $sg_vport/protocols/ospfV3 \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/pimsm \
 -bsmFramePerInterval 0 \
 -crpFramePerInterval 0 \
 -dataMdtFramePerInterval 0 \
 -enableRateControl False \
 -enabled False \
 -interval 0 \
 -joinPruneMessagesPerInterval 0 \
 -registerMessagesPerInterval 0 \
 -registerStopMessagesPerInterval 0
ixNet setMultiAttrs $sg_vport/protocols/ping \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/rip \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/ripng \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/rsvp \
 -enableBgpOverLsp True \
 -enabled True
ixNet setMultiAttrs $sg_vport/protocols/stp \
 -enabled False
ixNet setMultiAttrs $sg_vport/capture \
 -hardwareEnabled False \
 -softwareEnabled False
ixNet commit
set sg_vport [lindex [ixNet remapIds $sg_vport] 0]
set ixNetSG_Stack(1) $sg_vport

#
# configuring the object that corresponds to /vport:1/interface:97
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {ProtocolInterface - 06:74 - 1} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 A6 } \
 -mtu 1500 \
 -type default
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:a6" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia ::ixNet::OBJ-null
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {100} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(3) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:97/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.6 \
 -ip 20.20.20.1 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:98
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {2.2.2.1/24 - 06:74 - 1} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 A7 } \
 -mtu 1500 \
 -type routed
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:a7" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia $ixNetSG_ref(3)
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {1} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:98/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.1 \
 -ip 2.2.2.1 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:99
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {ProtocolInterface - 06:74 - 3} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 A8 } \
 -mtu 1500 \
 -type default
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:a8" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia ::ixNet::OBJ-null
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {101} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(7) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:99/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.7 \
 -ip 20.20.20.2 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:100
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {2.2.3.1/24 - 06:74 - 1} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 A9 } \
 -mtu 1500 \
 -type routed
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:a9" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia $ixNetSG_ref(7)
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {1} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:100/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.2 \
 -ip 2.2.3.1 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:101
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {ProtocolInterface - 06:74 - 5} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 AA } \
 -mtu 1500 \
 -type default
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:aa" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia ::ixNet::OBJ-null
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {102} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(11) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:101/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.8 \
 -ip 20.20.20.3 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:102
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {2.2.4.1/24 - 06:74 - 1} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 AB } \
 -mtu 1500 \
 -type routed
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:ab" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia $ixNetSG_ref(11)
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {1} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:102/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.3 \
 -ip 2.2.4.1 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:103
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {ProtocolInterface - 06:74 - 7} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 AC } \
 -mtu 1500 \
 -type default
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:ac" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia ::ixNet::OBJ-null
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {103} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(15) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:103/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.9 \
 -ip 20.20.20.4 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:104
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {2.2.5.1/24 - 06:74 - 1} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 AD } \
 -mtu 1500 \
 -type routed
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:ad" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia $ixNetSG_ref(15)
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {1} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:104/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.4 \
 -ip 2.2.5.1 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:105
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {ProtocolInterface - 06:74 - 9} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 AE } \
 -mtu 1500 \
 -type default
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:ae" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia ::ixNet::OBJ-null
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {104} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(19) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:105/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.10 \
 -ip 20.20.20.5 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/interface:106
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {2.2.6.1/24 - 06:74 - 1} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 AF } \
 -mtu 1500 \
 -type routed
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:af" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia $ixNetSG_ref(19)
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {1} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:1/interface:106/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.5 \
 -ip 2.2.6.1 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:1/l1Config/ethernet
#
set sg_ethernet $ixNetSG_Stack(1)/l1Config/ethernet
ixNet setMultiAttrs $sg_ethernet \
 -speed speed100fd \
 -media copper \
 -autoNegotiate True \
 -loopback False
ixNet commit
set sg_ethernet [lindex [ixNet remapIds $sg_ethernet] 0]
set ixNetSG_Stack(2) $sg_ethernet

#
# configuring the object that corresponds to /vport:1/l1Config/ethernet/oam
#
set sg_oam $ixNetSG_Stack(2)/oam
ixNet setMultiAttrs $sg_oam \
 -tlvType {00} \
 -tlvValue {00} \
 -vendorSpecificInformation {00 00 00 00} \
 -enableTlvOption False \
 -organizationUniqueIdentifier {000000} \
 -loopback False \
 -macAddress "00:00:00:00:00:00" \
 -maxOAMPDUSize 1518 \
 -enabled False \
 -idleTimer 5 \
 -linkEvents False
ixNet commit
set sg_oam [lindex [ixNet remapIds $sg_oam] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1
#
set sg_router [ixNet add $ixNetSG_Stack(1)/protocols/ospf router]
ixNet setMultiAttrs $sg_router \
 -discardLearnedLsa True \
 -enabled True \
 -generateRouterLsa True \
 -gracefulRestart False \
 -rebuildAdjForLsdbChange False \
 -routerId 20.20.20.1 \
 -strictLsaChecking True \
 -supportForRfc3623 False \
 -supportReasonSoftReloadUpgrade True \
 -supportReasonSoftRestart True \
 -supportReasonSwotchRedundantCntrlProcessor True \
 -supportReasonUnknown True \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]
set ixNetSG_Stack(2) $sg_router

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut True \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 20.20.20.1 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes transit \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 0.0.0.0 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 66 \
 -priority 2 \
 -protocolInterface $ixNetSG_ref(3) \
 -showExternal True \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable True \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/interface:2
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut False \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 11.1.1.1 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes pointToPoint \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 2.2.2.1 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 64 \
 -priority 2 \
 -protocolInterface ::ixNet::OBJ-null \
 -showExternal False \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable False \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/userLsaGroup:1
#
set sg_userLsaGroup [ixNet add $ixNetSG_Stack(2) userLsaGroup]
ixNet setMultiAttrs $sg_userLsaGroup \
 -areaId 0 \
 -description {} \
 -enabled True
ixNet commit
set sg_userLsaGroup [lindex [ixNet remapIds $sg_userLsaGroup] 0]
set ixNetSG_Stack(3) $sg_userLsaGroup

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/userLsaGroup:1/userLsa:1
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.2.1 \
 -enabled True \
 -linkStateId 2.2.2.1 \
 -lsaType router \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/userLsaGroup:1/userLsa:1/router
#
set sg_router $ixNetSG_Stack(4)/router
ixNet setMultiAttrs $sg_router \
 -bBit False \
 -eBit False \
 -interfaces  { {20.20.20.1 11.1.1.2 pointToPoint 1} {11.1.1.0 255.255.255.0 stub 1} {2.2.2.1 255.255.255.255 stub 1} } \
 -vBit False
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/userLsaGroup:1/userLsa:2
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.2.1 \
 -enabled True \
 -linkStateId 1.0.20.1 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/userLsaGroup:1/userLsa:2/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv True
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/userLsaGroup:1/userLsa:2/opaque/routerTlv
#
set sg_routerTlv $ixNetSG_Stack(5)/routerTlv
ixNet setAttribute $sg_routerTlv -routerAddress 2.2.2.1
ixNet commit
set sg_routerTlv [lindex [ixNet remapIds $sg_routerTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/userLsaGroup:1/userLsa:3
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.2.1 \
 -enabled True \
 -linkStateId 1.0.20.2 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/userLsaGroup:1/userLsa:3/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/userLsaGroup:1/userLsa:3/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 20.20.20.1 \
 -linkLocalIpAddress 11.1.1.2 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.1.1 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/userLsaGroup:1/userLsa:4
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 20.20.20.1 \
 -enabled True \
 -linkStateId 1.0.20.3 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/userLsaGroup:1/userLsa:4/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:1/userLsaGroup:1/userLsa:4/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 2.2.2.1 \
 -linkLocalIpAddress 11.1.1.1 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.1.2 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2
#
set sg_router [ixNet add $ixNetSG_Stack(1)/protocols/ospf router]
ixNet setMultiAttrs $sg_router \
 -discardLearnedLsa True \
 -enabled True \
 -generateRouterLsa True \
 -gracefulRestart False \
 -rebuildAdjForLsdbChange False \
 -routerId 20.20.20.2 \
 -strictLsaChecking True \
 -supportForRfc3623 False \
 -supportReasonSoftReloadUpgrade True \
 -supportReasonSoftRestart True \
 -supportReasonSwotchRedundantCntrlProcessor True \
 -supportReasonUnknown True \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]
set ixNetSG_Stack(2) $sg_router

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut True \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 20.20.20.2 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes transit \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 0.0.0.0 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 66 \
 -priority 2 \
 -protocolInterface $ixNetSG_ref(7) \
 -showExternal True \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable True \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/interface:2
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut False \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 11.1.2.1 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes pointToPoint \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 2.2.3.1 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 64 \
 -priority 2 \
 -protocolInterface ::ixNet::OBJ-null \
 -showExternal False \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable False \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/userLsaGroup:1
#
set sg_userLsaGroup [ixNet add $ixNetSG_Stack(2) userLsaGroup]
ixNet setMultiAttrs $sg_userLsaGroup \
 -areaId 0 \
 -description {} \
 -enabled True
ixNet commit
set sg_userLsaGroup [lindex [ixNet remapIds $sg_userLsaGroup] 0]
set ixNetSG_Stack(3) $sg_userLsaGroup

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/userLsaGroup:1/userLsa:1
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.3.1 \
 -enabled True \
 -linkStateId 2.2.3.1 \
 -lsaType router \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/userLsaGroup:1/userLsa:1/router
#
set sg_router $ixNetSG_Stack(4)/router
ixNet setMultiAttrs $sg_router \
 -bBit False \
 -eBit False \
 -interfaces  { {20.20.20.2 11.1.2.2 pointToPoint 1} {11.1.2.0 255.255.255.0 stub 1} {2.2.3.1 255.255.255.255 stub 1} } \
 -vBit False
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/userLsaGroup:1/userLsa:2
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.3.1 \
 -enabled True \
 -linkStateId 1.0.20.2 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/userLsaGroup:1/userLsa:2/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv True
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/userLsaGroup:1/userLsa:2/opaque/routerTlv
#
set sg_routerTlv $ixNetSG_Stack(5)/routerTlv
ixNet setAttribute $sg_routerTlv -routerAddress 2.2.3.1
ixNet commit
set sg_routerTlv [lindex [ixNet remapIds $sg_routerTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/userLsaGroup:1/userLsa:3
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.3.1 \
 -enabled True \
 -linkStateId 1.0.20.3 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/userLsaGroup:1/userLsa:3/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/userLsaGroup:1/userLsa:3/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 20.20.20.2 \
 -linkLocalIpAddress 11.1.2.2 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.2.1 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/userLsaGroup:1/userLsa:4
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 20.20.20.2 \
 -enabled True \
 -linkStateId 1.0.20.4 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/userLsaGroup:1/userLsa:4/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:2/userLsaGroup:1/userLsa:4/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 2.2.3.1 \
 -linkLocalIpAddress 11.1.2.1 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.2.2 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3
#
set sg_router [ixNet add $ixNetSG_Stack(1)/protocols/ospf router]
ixNet setMultiAttrs $sg_router \
 -discardLearnedLsa True \
 -enabled True \
 -generateRouterLsa True \
 -gracefulRestart False \
 -rebuildAdjForLsdbChange False \
 -routerId 20.20.20.3 \
 -strictLsaChecking True \
 -supportForRfc3623 False \
 -supportReasonSoftReloadUpgrade True \
 -supportReasonSoftRestart True \
 -supportReasonSwotchRedundantCntrlProcessor True \
 -supportReasonUnknown True \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]
set ixNetSG_Stack(2) $sg_router

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut True \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 20.20.20.3 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes transit \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 0.0.0.0 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 66 \
 -priority 2 \
 -protocolInterface $ixNetSG_ref(11) \
 -showExternal True \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable True \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/interface:2
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut False \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 11.1.3.1 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes pointToPoint \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 2.2.4.1 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 64 \
 -priority 2 \
 -protocolInterface ::ixNet::OBJ-null \
 -showExternal False \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable False \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/userLsaGroup:1
#
set sg_userLsaGroup [ixNet add $ixNetSG_Stack(2) userLsaGroup]
ixNet setMultiAttrs $sg_userLsaGroup \
 -areaId 0 \
 -description {} \
 -enabled True
ixNet commit
set sg_userLsaGroup [lindex [ixNet remapIds $sg_userLsaGroup] 0]
set ixNetSG_Stack(3) $sg_userLsaGroup

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/userLsaGroup:1/userLsa:1
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.4.1 \
 -enabled True \
 -linkStateId 2.2.4.1 \
 -lsaType router \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/userLsaGroup:1/userLsa:1/router
#
set sg_router $ixNetSG_Stack(4)/router
ixNet setMultiAttrs $sg_router \
 -bBit False \
 -eBit False \
 -interfaces  { {20.20.20.3 11.1.3.2 pointToPoint 1} {11.1.3.0 255.255.255.0 stub 1} {2.2.4.1 255.255.255.255 stub 1} } \
 -vBit False
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/userLsaGroup:1/userLsa:2
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.4.1 \
 -enabled True \
 -linkStateId 1.0.20.3 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/userLsaGroup:1/userLsa:2/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv True
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/userLsaGroup:1/userLsa:2/opaque/routerTlv
#
set sg_routerTlv $ixNetSG_Stack(5)/routerTlv
ixNet setAttribute $sg_routerTlv -routerAddress 2.2.4.1
ixNet commit
set sg_routerTlv [lindex [ixNet remapIds $sg_routerTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/userLsaGroup:1/userLsa:3
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.4.1 \
 -enabled True \
 -linkStateId 1.0.20.4 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/userLsaGroup:1/userLsa:3/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/userLsaGroup:1/userLsa:3/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 20.20.20.3 \
 -linkLocalIpAddress 11.1.3.2 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.3.1 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/userLsaGroup:1/userLsa:4
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 20.20.20.3 \
 -enabled True \
 -linkStateId 1.0.20.5 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/userLsaGroup:1/userLsa:4/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:3/userLsaGroup:1/userLsa:4/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 2.2.4.1 \
 -linkLocalIpAddress 11.1.3.1 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.3.2 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4
#
set sg_router [ixNet add $ixNetSG_Stack(1)/protocols/ospf router]
ixNet setMultiAttrs $sg_router \
 -discardLearnedLsa True \
 -enabled True \
 -generateRouterLsa True \
 -gracefulRestart False \
 -rebuildAdjForLsdbChange False \
 -routerId 20.20.20.4 \
 -strictLsaChecking True \
 -supportForRfc3623 False \
 -supportReasonSoftReloadUpgrade True \
 -supportReasonSoftRestart True \
 -supportReasonSwotchRedundantCntrlProcessor True \
 -supportReasonUnknown True \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]
set ixNetSG_Stack(2) $sg_router

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut True \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 20.20.20.4 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes transit \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 0.0.0.0 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 66 \
 -priority 2 \
 -protocolInterface $ixNetSG_ref(15) \
 -showExternal True \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable True \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/interface:2
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut False \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 11.1.4.1 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes pointToPoint \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 2.2.5.1 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 64 \
 -priority 2 \
 -protocolInterface ::ixNet::OBJ-null \
 -showExternal False \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable False \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/userLsaGroup:1
#
set sg_userLsaGroup [ixNet add $ixNetSG_Stack(2) userLsaGroup]
ixNet setMultiAttrs $sg_userLsaGroup \
 -areaId 0 \
 -description {} \
 -enabled True
ixNet commit
set sg_userLsaGroup [lindex [ixNet remapIds $sg_userLsaGroup] 0]
set ixNetSG_Stack(3) $sg_userLsaGroup

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/userLsaGroup:1/userLsa:1
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.5.1 \
 -enabled True \
 -linkStateId 2.2.5.1 \
 -lsaType router \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/userLsaGroup:1/userLsa:1/router
#
set sg_router $ixNetSG_Stack(4)/router
ixNet setMultiAttrs $sg_router \
 -bBit False \
 -eBit False \
 -interfaces  { {20.20.20.4 11.1.4.2 pointToPoint 1} {11.1.4.0 255.255.255.0 stub 1} {2.2.5.1 255.255.255.255 stub 1} } \
 -vBit False
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/userLsaGroup:1/userLsa:2
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.5.1 \
 -enabled True \
 -linkStateId 1.0.20.4 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/userLsaGroup:1/userLsa:2/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv True
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/userLsaGroup:1/userLsa:2/opaque/routerTlv
#
set sg_routerTlv $ixNetSG_Stack(5)/routerTlv
ixNet setAttribute $sg_routerTlv -routerAddress 2.2.5.1
ixNet commit
set sg_routerTlv [lindex [ixNet remapIds $sg_routerTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/userLsaGroup:1/userLsa:3
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.5.1 \
 -enabled True \
 -linkStateId 1.0.20.5 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/userLsaGroup:1/userLsa:3/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/userLsaGroup:1/userLsa:3/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 20.20.20.4 \
 -linkLocalIpAddress 11.1.4.2 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.4.1 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/userLsaGroup:1/userLsa:4
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 20.20.20.4 \
 -enabled True \
 -linkStateId 1.0.20.6 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/userLsaGroup:1/userLsa:4/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:4/userLsaGroup:1/userLsa:4/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 2.2.5.1 \
 -linkLocalIpAddress 11.1.4.1 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.4.2 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5
#
set sg_router [ixNet add $ixNetSG_Stack(1)/protocols/ospf router]
ixNet setMultiAttrs $sg_router \
 -discardLearnedLsa True \
 -enabled True \
 -generateRouterLsa True \
 -gracefulRestart False \
 -rebuildAdjForLsdbChange False \
 -routerId 20.20.20.5 \
 -strictLsaChecking True \
 -supportForRfc3623 False \
 -supportReasonSoftReloadUpgrade True \
 -supportReasonSoftRestart True \
 -supportReasonSwotchRedundantCntrlProcessor True \
 -supportReasonUnknown True \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]
set ixNetSG_Stack(2) $sg_router

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut True \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 20.20.20.5 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes transit \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 0.0.0.0 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 66 \
 -priority 2 \
 -protocolInterface $ixNetSG_ref(19) \
 -showExternal True \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable True \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/interface:2
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut False \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 11.1.5.1 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes pointToPoint \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 2.2.6.1 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 64 \
 -priority 2 \
 -protocolInterface ::ixNet::OBJ-null \
 -showExternal False \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable False \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/userLsaGroup:1
#
set sg_userLsaGroup [ixNet add $ixNetSG_Stack(2) userLsaGroup]
ixNet setMultiAttrs $sg_userLsaGroup \
 -areaId 0 \
 -description {} \
 -enabled True
ixNet commit
set sg_userLsaGroup [lindex [ixNet remapIds $sg_userLsaGroup] 0]
set ixNetSG_Stack(3) $sg_userLsaGroup

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/userLsaGroup:1/userLsa:1
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.6.1 \
 -enabled True \
 -linkStateId 2.2.6.1 \
 -lsaType router \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/userLsaGroup:1/userLsa:1/router
#
set sg_router $ixNetSG_Stack(4)/router
ixNet setMultiAttrs $sg_router \
 -bBit False \
 -eBit False \
 -interfaces  { {20.20.20.5 11.1.5.2 pointToPoint 1} {11.1.5.0 255.255.255.0 stub 1} {2.2.6.1 255.255.255.255 stub 1} } \
 -vBit False
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/userLsaGroup:1/userLsa:2
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.6.1 \
 -enabled True \
 -linkStateId 1.0.20.5 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/userLsaGroup:1/userLsa:2/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv True
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/userLsaGroup:1/userLsa:2/opaque/routerTlv
#
set sg_routerTlv $ixNetSG_Stack(5)/routerTlv
ixNet setAttribute $sg_routerTlv -routerAddress 2.2.6.1
ixNet commit
set sg_routerTlv [lindex [ixNet remapIds $sg_routerTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/userLsaGroup:1/userLsa:3
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 2.2.6.1 \
 -enabled True \
 -linkStateId 1.0.20.6 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/userLsaGroup:1/userLsa:3/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/userLsaGroup:1/userLsa:3/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 20.20.20.5 \
 -linkLocalIpAddress 11.1.5.2 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.5.1 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/userLsaGroup:1/userLsa:4
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 20.20.20.5 \
 -enabled True \
 -linkStateId 1.0.20.7 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/userLsaGroup:1/userLsa:4/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:1/protocols/ospf/router:5/userLsaGroup:1/userLsa:4/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 2.2.6.1 \
 -linkLocalIpAddress 11.1.5.1 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.5.2 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:1
#
set sg_neighborPair [ixNet add $ixNetSG_Stack(1)/protocols/rsvp neighborPair]
ixNet setMultiAttrs $sg_neighborPair \
 -actualRestartTime 15000 \
 -dutIp 20.20.20.6 \
 -enableGracefulRestartHelperMode True \
 -enableGracefulRestartingMode False \
 -enableHello True \
 -enabled True \
 -gracefulRestartStartTime 30000 \
 -gracefulRestartUpTime 30000 \
 -helloInterval 5 \
 -helloTimeoutMultiplier 3 \
 -helloTlvs  {  } \
 -labelSpaceEnd 100000 \
 -labelSpaceStart 1000 \
 -numberOfGracefulRestarts 0 \
 -ourIp 20.20.20.1 \
 -recoveryTimeInterval 30000 \
 -refreshReduction False \
 -restartTimeInterval 30000 \
 -summaryRefreshInterval 15000 \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_neighborPair [lindex [ixNet remapIds $sg_neighborPair] 0]
set ixNetSG_Stack(2) $sg_neighborPair

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:1/destinationRange:1
#
set sg_destinationRange [ixNet add $ixNetSG_Stack(2) destinationRange]
ixNet setMultiAttrs $sg_destinationRange \
 -behavior ingress \
 -emulationType rsvpTe \
 -enabled True \
 -ipAddressFrom 3.3.3.1 \
 -ipCount 1 \
 -isConnectedIpAppended True \
 -isHeadIpPrepended True \
 -isLeafIpPrepended True \
 -isSendingAsRro True \
 -isSendingAsSrro False \
 -p2mpId 3.3.3.1
ixNet setMultiAttrs $sg_destinationRange/egress \
 -bandwidth 0 \
 -egressBehavior alwaysUseConfiguredStyle \
 -enableFixedLabelForResv False \
 -labelValue {explicitNull} \
 -pathErrorTlv  {  } \
 -reflectRro True \
 -refreshInterval 30000 \
 -reservationStyle se \
 -reservationTearTlv  {  } \
 -reservationTlv  {  } \
 -rro  {  } \
 -sendResvConfirmation False \
 -timeoutMultiplier 3
ixNet setMultiAttrs $sg_destinationRange/ingress \
 -enableEro False \
 -ero  {  } \
 -prefixLength 32 \
 -prependDutToEro prependLoose \
 -reservationErrorTlv  {  } \
 -rro  {  } \
 -sendRro False \
 -tunnelIdsCount 1 \
 -tunnelIdsStart 1
ixNet commit
set sg_destinationRange [lindex [ixNet remapIds $sg_destinationRange] 0]
set ixNetSG_Stack(3) $sg_destinationRange

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:1/destinationRange:1/ingress/senderRange:1
#
set sg_senderRange [ixNet add $ixNetSG_Stack(3)/ingress senderRange]
ixNet setMultiAttrs $sg_senderRange \
 -autoGenerateSessionName True \
 -bandwidth 0 \
 -bandwidthProtectionDesired False \
 -enableFastReroute False \
 -enableResourceAffinities False \
 -enabled True \
 -excludeAny 0 \
 -fastRerouteBandwidth 0 \
 -fastRerouteDetour  {  } \
 -fastRerouteExcludeAny 0 \
 -fastRerouteFacilityBackupDesired False \
 -fastRerouteHoldingPriority 7 \
 -fastRerouteHopLimit 3 \
 -fastRerouteIncludeAll 0 \
 -fastRerouteIncludeAny 0 \
 -fastRerouteOne2OneBackupDesired False \
 -fastRerouteSendDetour False \
 -fastRerouteSetupPriority 7 \
 -holdingPriority 7 \
 -includeAll 0 \
 -includeAny 0 \
 -ipCount 1 \
 -ipStart 2.2.2.1 \
 -labelRecordingDesired False \
 -localProtectionDesired True \
 -lspIdCount 1 \
 -lspIdStart 1 \
 -maximumPacketSize 0 \
 -minimumPolicedUnit 0 \
 -nodeProtectionDesired False \
 -pathTearTlv  {  } \
 -pathTlv  {  } \
 -peakDataRate 0 \
 -refreshInterval 30000 \
 -seStyleDesired True \
 -sessionName {} \
 -setupPriority 7 \
 -timeoutMultiplier 3 \
 -tokenBucketRate 0 \
 -tokenBucketSize 0
ixNet commit
set sg_senderRange [lindex [ixNet remapIds $sg_senderRange] 0]

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:2
#
set sg_neighborPair [ixNet add $ixNetSG_Stack(1)/protocols/rsvp neighborPair]
ixNet setMultiAttrs $sg_neighborPair \
 -actualRestartTime 15000 \
 -dutIp 20.20.20.7 \
 -enableGracefulRestartHelperMode True \
 -enableGracefulRestartingMode False \
 -enableHello True \
 -enabled True \
 -gracefulRestartStartTime 30000 \
 -gracefulRestartUpTime 30000 \
 -helloInterval 5 \
 -helloTimeoutMultiplier 3 \
 -helloTlvs  {  } \
 -labelSpaceEnd 100000 \
 -labelSpaceStart 1000 \
 -numberOfGracefulRestarts 0 \
 -ourIp 20.20.20.2 \
 -recoveryTimeInterval 30000 \
 -refreshReduction False \
 -restartTimeInterval 30000 \
 -summaryRefreshInterval 15000 \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_neighborPair [lindex [ixNet remapIds $sg_neighborPair] 0]
set ixNetSG_Stack(2) $sg_neighborPair

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:2/destinationRange:1
#
set sg_destinationRange [ixNet add $ixNetSG_Stack(2) destinationRange]
ixNet setMultiAttrs $sg_destinationRange \
 -behavior ingress \
 -emulationType rsvpTe \
 -enabled True \
 -ipAddressFrom 3.3.4.1 \
 -ipCount 1 \
 -isConnectedIpAppended True \
 -isHeadIpPrepended True \
 -isLeafIpPrepended True \
 -isSendingAsRro True \
 -isSendingAsSrro False \
 -p2mpId 3.3.4.1
ixNet setMultiAttrs $sg_destinationRange/egress \
 -bandwidth 0 \
 -egressBehavior alwaysUseConfiguredStyle \
 -enableFixedLabelForResv False \
 -labelValue {explicitNull} \
 -pathErrorTlv  {  } \
 -reflectRro True \
 -refreshInterval 30000 \
 -reservationStyle se \
 -reservationTearTlv  {  } \
 -reservationTlv  {  } \
 -rro  {  } \
 -sendResvConfirmation False \
 -timeoutMultiplier 3
ixNet setMultiAttrs $sg_destinationRange/ingress \
 -enableEro False \
 -ero  {  } \
 -prefixLength 32 \
 -prependDutToEro prependLoose \
 -reservationErrorTlv  {  } \
 -rro  {  } \
 -sendRro False \
 -tunnelIdsCount 1 \
 -tunnelIdsStart 1
ixNet commit
set sg_destinationRange [lindex [ixNet remapIds $sg_destinationRange] 0]
set ixNetSG_Stack(3) $sg_destinationRange

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:2/destinationRange:1/ingress/senderRange:1
#
set sg_senderRange [ixNet add $ixNetSG_Stack(3)/ingress senderRange]
ixNet setMultiAttrs $sg_senderRange \
 -autoGenerateSessionName True \
 -bandwidth 0 \
 -bandwidthProtectionDesired False \
 -enableFastReroute False \
 -enableResourceAffinities False \
 -enabled True \
 -excludeAny 0 \
 -fastRerouteBandwidth 0 \
 -fastRerouteDetour  {  } \
 -fastRerouteExcludeAny 0 \
 -fastRerouteFacilityBackupDesired False \
 -fastRerouteHoldingPriority 7 \
 -fastRerouteHopLimit 3 \
 -fastRerouteIncludeAll 0 \
 -fastRerouteIncludeAny 0 \
 -fastRerouteOne2OneBackupDesired False \
 -fastRerouteSendDetour False \
 -fastRerouteSetupPriority 7 \
 -holdingPriority 7 \
 -includeAll 0 \
 -includeAny 0 \
 -ipCount 1 \
 -ipStart 2.2.3.1 \
 -labelRecordingDesired False \
 -localProtectionDesired True \
 -lspIdCount 1 \
 -lspIdStart 1 \
 -maximumPacketSize 0 \
 -minimumPolicedUnit 0 \
 -nodeProtectionDesired False \
 -pathTearTlv  {  } \
 -pathTlv  {  } \
 -peakDataRate 0 \
 -refreshInterval 30000 \
 -seStyleDesired True \
 -sessionName {} \
 -setupPriority 7 \
 -timeoutMultiplier 3 \
 -tokenBucketRate 0 \
 -tokenBucketSize 0
ixNet commit
set sg_senderRange [lindex [ixNet remapIds $sg_senderRange] 0]

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:3
#
set sg_neighborPair [ixNet add $ixNetSG_Stack(1)/protocols/rsvp neighborPair]
ixNet setMultiAttrs $sg_neighborPair \
 -actualRestartTime 15000 \
 -dutIp 20.20.20.8 \
 -enableGracefulRestartHelperMode True \
 -enableGracefulRestartingMode False \
 -enableHello True \
 -enabled True \
 -gracefulRestartStartTime 30000 \
 -gracefulRestartUpTime 30000 \
 -helloInterval 5 \
 -helloTimeoutMultiplier 3 \
 -helloTlvs  {  } \
 -labelSpaceEnd 100000 \
 -labelSpaceStart 1000 \
 -numberOfGracefulRestarts 0 \
 -ourIp 20.20.20.3 \
 -recoveryTimeInterval 30000 \
 -refreshReduction False \
 -restartTimeInterval 30000 \
 -summaryRefreshInterval 15000 \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_neighborPair [lindex [ixNet remapIds $sg_neighborPair] 0]
set ixNetSG_Stack(2) $sg_neighborPair

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:3/destinationRange:1
#
set sg_destinationRange [ixNet add $ixNetSG_Stack(2) destinationRange]
ixNet setMultiAttrs $sg_destinationRange \
 -behavior ingress \
 -emulationType rsvpTe \
 -enabled True \
 -ipAddressFrom 3.3.5.1 \
 -ipCount 1 \
 -isConnectedIpAppended True \
 -isHeadIpPrepended True \
 -isLeafIpPrepended True \
 -isSendingAsRro True \
 -isSendingAsSrro False \
 -p2mpId 3.3.5.1
ixNet setMultiAttrs $sg_destinationRange/egress \
 -bandwidth 0 \
 -egressBehavior alwaysUseConfiguredStyle \
 -enableFixedLabelForResv False \
 -labelValue {explicitNull} \
 -pathErrorTlv  {  } \
 -reflectRro True \
 -refreshInterval 30000 \
 -reservationStyle se \
 -reservationTearTlv  {  } \
 -reservationTlv  {  } \
 -rro  {  } \
 -sendResvConfirmation False \
 -timeoutMultiplier 3
ixNet setMultiAttrs $sg_destinationRange/ingress \
 -enableEro False \
 -ero  {  } \
 -prefixLength 32 \
 -prependDutToEro prependLoose \
 -reservationErrorTlv  {  } \
 -rro  {  } \
 -sendRro False \
 -tunnelIdsCount 1 \
 -tunnelIdsStart 1
ixNet commit
set sg_destinationRange [lindex [ixNet remapIds $sg_destinationRange] 0]
set ixNetSG_Stack(3) $sg_destinationRange

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:3/destinationRange:1/ingress/senderRange:1
#
set sg_senderRange [ixNet add $ixNetSG_Stack(3)/ingress senderRange]
ixNet setMultiAttrs $sg_senderRange \
 -autoGenerateSessionName True \
 -bandwidth 0 \
 -bandwidthProtectionDesired False \
 -enableFastReroute False \
 -enableResourceAffinities False \
 -enabled True \
 -excludeAny 0 \
 -fastRerouteBandwidth 0 \
 -fastRerouteDetour  {  } \
 -fastRerouteExcludeAny 0 \
 -fastRerouteFacilityBackupDesired False \
 -fastRerouteHoldingPriority 7 \
 -fastRerouteHopLimit 3 \
 -fastRerouteIncludeAll 0 \
 -fastRerouteIncludeAny 0 \
 -fastRerouteOne2OneBackupDesired False \
 -fastRerouteSendDetour False \
 -fastRerouteSetupPriority 7 \
 -holdingPriority 7 \
 -includeAll 0 \
 -includeAny 0 \
 -ipCount 1 \
 -ipStart 2.2.4.1 \
 -labelRecordingDesired False \
 -localProtectionDesired True \
 -lspIdCount 1 \
 -lspIdStart 1 \
 -maximumPacketSize 0 \
 -minimumPolicedUnit 0 \
 -nodeProtectionDesired False \
 -pathTearTlv  {  } \
 -pathTlv  {  } \
 -peakDataRate 0 \
 -refreshInterval 30000 \
 -seStyleDesired True \
 -sessionName {} \
 -setupPriority 7 \
 -timeoutMultiplier 3 \
 -tokenBucketRate 0 \
 -tokenBucketSize 0
ixNet commit
set sg_senderRange [lindex [ixNet remapIds $sg_senderRange] 0]

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:4
#
set sg_neighborPair [ixNet add $ixNetSG_Stack(1)/protocols/rsvp neighborPair]
ixNet setMultiAttrs $sg_neighborPair \
 -actualRestartTime 15000 \
 -dutIp 20.20.20.9 \
 -enableGracefulRestartHelperMode True \
 -enableGracefulRestartingMode False \
 -enableHello True \
 -enabled True \
 -gracefulRestartStartTime 30000 \
 -gracefulRestartUpTime 30000 \
 -helloInterval 5 \
 -helloTimeoutMultiplier 3 \
 -helloTlvs  {  } \
 -labelSpaceEnd 100000 \
 -labelSpaceStart 1000 \
 -numberOfGracefulRestarts 0 \
 -ourIp 20.20.20.4 \
 -recoveryTimeInterval 30000 \
 -refreshReduction False \
 -restartTimeInterval 30000 \
 -summaryRefreshInterval 15000 \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_neighborPair [lindex [ixNet remapIds $sg_neighborPair] 0]
set ixNetSG_Stack(2) $sg_neighborPair

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:4/destinationRange:1
#
set sg_destinationRange [ixNet add $ixNetSG_Stack(2) destinationRange]
ixNet setMultiAttrs $sg_destinationRange \
 -behavior ingress \
 -emulationType rsvpTe \
 -enabled True \
 -ipAddressFrom 3.3.6.1 \
 -ipCount 1 \
 -isConnectedIpAppended True \
 -isHeadIpPrepended True \
 -isLeafIpPrepended True \
 -isSendingAsRro True \
 -isSendingAsSrro False \
 -p2mpId 3.3.6.1
ixNet setMultiAttrs $sg_destinationRange/egress \
 -bandwidth 0 \
 -egressBehavior alwaysUseConfiguredStyle \
 -enableFixedLabelForResv False \
 -labelValue {explicitNull} \
 -pathErrorTlv  {  } \
 -reflectRro True \
 -refreshInterval 30000 \
 -reservationStyle se \
 -reservationTearTlv  {  } \
 -reservationTlv  {  } \
 -rro  {  } \
 -sendResvConfirmation False \
 -timeoutMultiplier 3
ixNet setMultiAttrs $sg_destinationRange/ingress \
 -enableEro False \
 -ero  {  } \
 -prefixLength 32 \
 -prependDutToEro prependLoose \
 -reservationErrorTlv  {  } \
 -rro  {  } \
 -sendRro False \
 -tunnelIdsCount 1 \
 -tunnelIdsStart 1
ixNet commit
set sg_destinationRange [lindex [ixNet remapIds $sg_destinationRange] 0]
set ixNetSG_Stack(3) $sg_destinationRange

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:4/destinationRange:1/ingress/senderRange:1
#
set sg_senderRange [ixNet add $ixNetSG_Stack(3)/ingress senderRange]
ixNet setMultiAttrs $sg_senderRange \
 -autoGenerateSessionName True \
 -bandwidth 0 \
 -bandwidthProtectionDesired False \
 -enableFastReroute False \
 -enableResourceAffinities False \
 -enabled True \
 -excludeAny 0 \
 -fastRerouteBandwidth 0 \
 -fastRerouteDetour  {  } \
 -fastRerouteExcludeAny 0 \
 -fastRerouteFacilityBackupDesired False \
 -fastRerouteHoldingPriority 7 \
 -fastRerouteHopLimit 3 \
 -fastRerouteIncludeAll 0 \
 -fastRerouteIncludeAny 0 \
 -fastRerouteOne2OneBackupDesired False \
 -fastRerouteSendDetour False \
 -fastRerouteSetupPriority 7 \
 -holdingPriority 7 \
 -includeAll 0 \
 -includeAny 0 \
 -ipCount 1 \
 -ipStart 2.2.5.1 \
 -labelRecordingDesired False \
 -localProtectionDesired True \
 -lspIdCount 1 \
 -lspIdStart 1 \
 -maximumPacketSize 0 \
 -minimumPolicedUnit 0 \
 -nodeProtectionDesired False \
 -pathTearTlv  {  } \
 -pathTlv  {  } \
 -peakDataRate 0 \
 -refreshInterval 30000 \
 -seStyleDesired True \
 -sessionName {} \
 -setupPriority 7 \
 -timeoutMultiplier 3 \
 -tokenBucketRate 0 \
 -tokenBucketSize 0
ixNet commit
set sg_senderRange [lindex [ixNet remapIds $sg_senderRange] 0]

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:5
#
set sg_neighborPair [ixNet add $ixNetSG_Stack(1)/protocols/rsvp neighborPair]
ixNet setMultiAttrs $sg_neighborPair \
 -actualRestartTime 15000 \
 -dutIp 20.20.20.10 \
 -enableGracefulRestartHelperMode True \
 -enableGracefulRestartingMode False \
 -enableHello True \
 -enabled True \
 -gracefulRestartStartTime 30000 \
 -gracefulRestartUpTime 30000 \
 -helloInterval 5 \
 -helloTimeoutMultiplier 3 \
 -helloTlvs  {  } \
 -labelSpaceEnd 100000 \
 -labelSpaceStart 1000 \
 -numberOfGracefulRestarts 0 \
 -ourIp 20.20.20.5 \
 -recoveryTimeInterval 30000 \
 -refreshReduction False \
 -restartTimeInterval 30000 \
 -summaryRefreshInterval 15000 \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_neighborPair [lindex [ixNet remapIds $sg_neighborPair] 0]
set ixNetSG_Stack(2) $sg_neighborPair

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:5/destinationRange:1
#
set sg_destinationRange [ixNet add $ixNetSG_Stack(2) destinationRange]
ixNet setMultiAttrs $sg_destinationRange \
 -behavior ingress \
 -emulationType rsvpTe \
 -enabled True \
 -ipAddressFrom 3.3.7.1 \
 -ipCount 1 \
 -isConnectedIpAppended True \
 -isHeadIpPrepended True \
 -isLeafIpPrepended True \
 -isSendingAsRro True \
 -isSendingAsSrro False \
 -p2mpId 3.3.7.1
ixNet setMultiAttrs $sg_destinationRange/egress \
 -bandwidth 0 \
 -egressBehavior alwaysUseConfiguredStyle \
 -enableFixedLabelForResv False \
 -labelValue {explicitNull} \
 -pathErrorTlv  {  } \
 -reflectRro True \
 -refreshInterval 30000 \
 -reservationStyle se \
 -reservationTearTlv  {  } \
 -reservationTlv  {  } \
 -rro  {  } \
 -sendResvConfirmation False \
 -timeoutMultiplier 3
ixNet setMultiAttrs $sg_destinationRange/ingress \
 -enableEro False \
 -ero  {  } \
 -prefixLength 32 \
 -prependDutToEro prependLoose \
 -reservationErrorTlv  {  } \
 -rro  {  } \
 -sendRro False \
 -tunnelIdsCount 1 \
 -tunnelIdsStart 1
ixNet commit
set sg_destinationRange [lindex [ixNet remapIds $sg_destinationRange] 0]
set ixNetSG_Stack(3) $sg_destinationRange

#
# configuring the object that corresponds to /vport:1/protocols/rsvp/neighborPair:5/destinationRange:1/ingress/senderRange:1
#
set sg_senderRange [ixNet add $ixNetSG_Stack(3)/ingress senderRange]
ixNet setMultiAttrs $sg_senderRange \
 -autoGenerateSessionName True \
 -bandwidth 0 \
 -bandwidthProtectionDesired False \
 -enableFastReroute False \
 -enableResourceAffinities False \
 -enabled True \
 -excludeAny 0 \
 -fastRerouteBandwidth 0 \
 -fastRerouteDetour  {  } \
 -fastRerouteExcludeAny 0 \
 -fastRerouteFacilityBackupDesired False \
 -fastRerouteHoldingPriority 7 \
 -fastRerouteHopLimit 3 \
 -fastRerouteIncludeAll 0 \
 -fastRerouteIncludeAny 0 \
 -fastRerouteOne2OneBackupDesired False \
 -fastRerouteSendDetour False \
 -fastRerouteSetupPriority 7 \
 -holdingPriority 7 \
 -includeAll 0 \
 -includeAny 0 \
 -ipCount 1 \
 -ipStart 2.2.6.1 \
 -labelRecordingDesired False \
 -localProtectionDesired True \
 -lspIdCount 1 \
 -lspIdStart 1 \
 -maximumPacketSize 0 \
 -minimumPolicedUnit 0 \
 -nodeProtectionDesired False \
 -pathTearTlv  {  } \
 -pathTlv  {  } \
 -peakDataRate 0 \
 -refreshInterval 30000 \
 -seStyleDesired True \
 -sessionName {} \
 -setupPriority 7 \
 -timeoutMultiplier 3 \
 -tokenBucketRate 0 \
 -tokenBucketSize 0
ixNet commit
set sg_senderRange [lindex [ixNet remapIds $sg_senderRange] 0]

#
# configuring the object that corresponds to /vport:2
#
set sg_vport [ixNet add $ixNetSG_Stack(0) vport]
ixNet setMultiAttrs $sg_vport \
 -rxMode measure \
 -connectedTo ::ixNet::OBJ-null \
 -type ethernet \
 -txMode sequential \
 -name {Ethernet - 002} \
 -transmitIgnoreLinkStatus False \
 -txGapControlMode fixedMode \
 -isPullOnly False
ixNet setMultiAttrs $sg_vport/l1Config \
 -currentType ethernet
ixNet setMultiAttrs $sg_vport/protocols/arp \
 -enabled True
ixNet setMultiAttrs $sg_vport/protocols/bfd \
 -enabled False \
 -intervalValue 0 \
 -packetsPerInterval 0
ixNet setMultiAttrs $sg_vport/protocols/bgp \
 -enableExternalActiveConnect True \
 -enableInternalActiveConnect True \
 -enableLabelExchangeOverLsp True \
 -enabled False \
 -externalRetries 0 \
 -externalRetryDelay 120 \
 -internalRetries 0 \
 -internalRetryDelay 120
ixNet setMultiAttrs $sg_vport/protocols/cfm \
 -enableOptionalTlvValidation True \
 -enabled False \
 -receiveCcm True \
 -sendCcm True
ixNet setMultiAttrs $sg_vport/protocols/eigrp \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/igmp \
 -enabled False \
 -numberOfGroups 0 \
 -numberOfQueries 0 \
 -queryTimePeriod 0 \
 -sendLeaveOnStop True \
 -statsEnabled False \
 -timePeriod 0
ixNet setMultiAttrs $sg_vport/protocols/isis \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/lacp \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/ldp \
 -enableDiscardSelfAdvFecs False \
 -enableHelloJitter True \
 -enableLabelExchangeOverLsp True \
 -enabled False \
 -helloHoldTime 15 \
 -helloInterval 5 \
 -keepAliveHoldTime 30 \
 -keepAliveInterval 10 \
 -targetedHelloInterval 15 \
 -targetedHoldTime 45
ixNet setMultiAttrs $sg_vport/protocols/mld \
 -enableDoneOnStop True \
 -enabled False \
 -mldv2Report type143 \
 -numberOfGroups 0 \
 -numberOfQueries 0 \
 -queryTimePeriod 0 \
 -timePeriod 0
ixNet setMultiAttrs $sg_vport/protocols/ospf \
 -enableDrOrBdr False \
 -enabled True
ixNet setMultiAttrs $sg_vport/protocols/ospfV3 \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/pimsm \
 -bsmFramePerInterval 0 \
 -crpFramePerInterval 0 \
 -dataMdtFramePerInterval 0 \
 -enableRateControl False \
 -enabled False \
 -interval 0 \
 -joinPruneMessagesPerInterval 0 \
 -registerMessagesPerInterval 0 \
 -registerStopMessagesPerInterval 0
ixNet setMultiAttrs $sg_vport/protocols/ping \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/rip \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/ripng \
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/rsvp \
 -enableBgpOverLsp True \
 -enabled True
ixNet setMultiAttrs $sg_vport/protocols/stp \
 -enabled False
ixNet setMultiAttrs $sg_vport/capture \
 -hardwareEnabled False \
 -softwareEnabled False
ixNet commit
set sg_vport [lindex [ixNet remapIds $sg_vport] 0]
set ixNetSG_Stack(1) $sg_vport

#
# configuring the object that corresponds to /vport:2/interface:83
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {ProtocolInterface - 06:75 - 1} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 A7 } \
 -mtu 1500 \
 -type default
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:a7" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia ::ixNet::OBJ-null
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {400} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(116) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:83/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.1 \
 -ip 20.20.20.6 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:84
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {3.3.3.1/24 - 06:75 - 1} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 A8 } \
 -mtu 1500 \
 -type routed
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:a8" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia $ixNetSG_ref(116)
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {1} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:84/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.6 \
 -ip 3.3.3.1 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:85
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {ProtocolInterface - 06:75 - 3} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 A9 } \
 -mtu 1500 \
 -type default
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:a9" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia ::ixNet::OBJ-null
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {401} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(120) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:85/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.2 \
 -ip 20.20.20.7 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:86
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {3.3.4.1/24 - 06:75 - 1} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 AA } \
 -mtu 1500 \
 -type routed
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:aa" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia $ixNetSG_ref(120)
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {1} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:86/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.7 \
 -ip 3.3.4.1 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:87
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {ProtocolInterface - 06:75 - 5} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 AB } \
 -mtu 1500 \
 -type default
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:ab" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia ::ixNet::OBJ-null
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {402} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(124) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:87/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.3 \
 -ip 20.20.20.8 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:88
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {3.3.5.1/24 - 06:75 - 1} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 AC } \
 -mtu 1500 \
 -type routed
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:ac" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia $ixNetSG_ref(124)
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {1} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:88/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.8 \
 -ip 3.3.5.1 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:89
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {ProtocolInterface - 06:75 - 7} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 AD } \
 -mtu 1500 \
 -type default
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:ad" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia ::ixNet::OBJ-null
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {403} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(128) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:89/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.4 \
 -ip 20.20.20.9 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:90
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {3.3.6.1/24 - 06:75 - 1} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 AE } \
 -mtu 1500 \
 -type routed
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:ae" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia $ixNetSG_ref(128)
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {1} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:90/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.9 \
 -ip 3.3.6.1 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:91
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {ProtocolInterface - 06:75 - 9} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 AF } \
 -mtu 1500 \
 -type default
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:af" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia ::ixNet::OBJ-null
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {404} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(132) $sg_interface
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:91/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.5 \
 -ip 20.20.20.10 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/interface:92
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {3.3.7.1/24 - 06:75 - 1} \
 -enabled True \
 -eui64Id {02 00 05 FF FE 10 B6 B0 } \
 -mtu 1500 \
 -type routed
ixNet setMultiAttrs $sg_interface/atm \
 -encapsulation llcBridgeFcs \
 -vci 32 \
 -vpi 0
ixNet setMultiAttrs $sg_interface/dhcpV4Properties \
 -clientId {} \
 -enabled False \
 -renewTimer 0 \
 -requestRate 0 \
 -serverId 0.0.0.0 \
 -tlvs  {  } \
 -vendorId {}
ixNet setMultiAttrs $sg_interface/dhcpV6Properties \
 -enabled False \
 -iaId 0 \
 -iaType temporary \
 -renewTimer 0 \
 -requestRate 0 \
 -tlvs  {  }
ixNet setMultiAttrs $sg_interface/ethernet \
 -macAddress "00:00:05:10:b6:b0" \
 -mtu 1500 \
 -uidFromMac True
ixNet setMultiAttrs $sg_interface/gre \
 -dest 0.0.0.0 \
 -inKey 0 \
 -outKey 0 \
 -source ::ixNet::OBJ-null \
 -useChecksum False \
 -useKey False \
 -useSequence False
ixNet setMultiAttrs $sg_interface/unconnected \
 -connectedVia $ixNetSG_ref(132)
ixNet setMultiAttrs $sg_interface/vlan \
 -tpid {0x8100} \
 -vlanCount 1 \
 -vlanEnable False \
 -vlanId {1} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_Stack(2) $sg_interface

#
# configuring the object that corresponds to /vport:2/interface:92/ipv4
#
set sg_ipv4 [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setMultiAttrs $sg_ipv4 \
 -gateway 20.20.20.10 \
 -ip 3.3.7.1 \
 -maskWidth 24
ixNet commit
set sg_ipv4 [lindex [ixNet remapIds $sg_ipv4] 0]

#
# configuring the object that corresponds to /vport:2/l1Config/ethernet
#
set sg_ethernet $ixNetSG_Stack(1)/l1Config/ethernet
ixNet setMultiAttrs $sg_ethernet \
 -speed speed100fd \
 -media copper \
 -autoNegotiate True \
 -loopback False
ixNet commit
set sg_ethernet [lindex [ixNet remapIds $sg_ethernet] 0]
set ixNetSG_Stack(2) $sg_ethernet

#
# configuring the object that corresponds to /vport:2/l1Config/ethernet/oam
#
set sg_oam $ixNetSG_Stack(2)/oam
ixNet setMultiAttrs $sg_oam \
 -tlvType {00} \
 -tlvValue {00} \
 -vendorSpecificInformation {00 00 00 00} \
 -enableTlvOption False \
 -organizationUniqueIdentifier {000000} \
 -loopback False \
 -macAddress "00:00:00:00:00:00" \
 -maxOAMPDUSize 1518 \
 -enabled False \
 -idleTimer 5 \
 -linkEvents False
ixNet commit
set sg_oam [lindex [ixNet remapIds $sg_oam] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1
#
set sg_router [ixNet add $ixNetSG_Stack(1)/protocols/ospf router]
ixNet setMultiAttrs $sg_router \
 -discardLearnedLsa True \
 -enabled True \
 -generateRouterLsa True \
 -gracefulRestart False \
 -rebuildAdjForLsdbChange False \
 -routerId 20.20.20.6 \
 -strictLsaChecking True \
 -supportForRfc3623 False \
 -supportReasonSoftReloadUpgrade True \
 -supportReasonSoftRestart True \
 -supportReasonSwotchRedundantCntrlProcessor True \
 -supportReasonUnknown True \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]
set ixNetSG_Stack(2) $sg_router

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut True \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 20.20.20.6 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes transit \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 0.0.0.0 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 66 \
 -priority 2 \
 -protocolInterface $ixNetSG_ref(116) \
 -showExternal True \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable True \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/interface:2
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut False \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 11.1.6.1 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes pointToPoint \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 3.3.3.1 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 64 \
 -priority 2 \
 -protocolInterface ::ixNet::OBJ-null \
 -showExternal False \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable False \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/userLsaGroup:1
#
set sg_userLsaGroup [ixNet add $ixNetSG_Stack(2) userLsaGroup]
ixNet setMultiAttrs $sg_userLsaGroup \
 -areaId 0 \
 -description {} \
 -enabled True
ixNet commit
set sg_userLsaGroup [lindex [ixNet remapIds $sg_userLsaGroup] 0]
set ixNetSG_Stack(3) $sg_userLsaGroup

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/userLsaGroup:1/userLsa:1
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.3.1 \
 -enabled True \
 -linkStateId 3.3.3.1 \
 -lsaType router \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/userLsaGroup:1/userLsa:1/router
#
set sg_router $ixNetSG_Stack(4)/router
ixNet setMultiAttrs $sg_router \
 -bBit False \
 -eBit False \
 -interfaces  { {20.20.20.6 11.1.6.2 pointToPoint 1} {11.1.6.0 255.255.255.0 stub 1} {3.3.3.1 255.255.255.255 stub 1} } \
 -vBit False
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/userLsaGroup:1/userLsa:2
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.3.1 \
 -enabled True \
 -linkStateId 1.0.20.6 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/userLsaGroup:1/userLsa:2/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv True
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/userLsaGroup:1/userLsa:2/opaque/routerTlv
#
set sg_routerTlv $ixNetSG_Stack(5)/routerTlv
ixNet setAttribute $sg_routerTlv -routerAddress 3.3.3.1
ixNet commit
set sg_routerTlv [lindex [ixNet remapIds $sg_routerTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/userLsaGroup:1/userLsa:3
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.3.1 \
 -enabled True \
 -linkStateId 1.0.20.7 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/userLsaGroup:1/userLsa:3/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/userLsaGroup:1/userLsa:3/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 20.20.20.6 \
 -linkLocalIpAddress 11.1.6.2 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.6.1 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/userLsaGroup:1/userLsa:4
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 20.20.20.6 \
 -enabled True \
 -linkStateId 1.0.20.8 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/userLsaGroup:1/userLsa:4/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:1/userLsaGroup:1/userLsa:4/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 3.3.3.1 \
 -linkLocalIpAddress 11.1.6.1 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.6.2 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2
#
set sg_router [ixNet add $ixNetSG_Stack(1)/protocols/ospf router]
ixNet setMultiAttrs $sg_router \
 -discardLearnedLsa True \
 -enabled True \
 -generateRouterLsa True \
 -gracefulRestart False \
 -rebuildAdjForLsdbChange False \
 -routerId 20.20.20.7 \
 -strictLsaChecking True \
 -supportForRfc3623 False \
 -supportReasonSoftReloadUpgrade True \
 -supportReasonSoftRestart True \
 -supportReasonSwotchRedundantCntrlProcessor True \
 -supportReasonUnknown True \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]
set ixNetSG_Stack(2) $sg_router

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut True \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 20.20.20.7 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes transit \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 0.0.0.0 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 66 \
 -priority 2 \
 -protocolInterface $ixNetSG_ref(120) \
 -showExternal True \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable True \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/interface:2
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut False \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 11.1.7.1 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes pointToPoint \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 3.3.4.1 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 64 \
 -priority 2 \
 -protocolInterface ::ixNet::OBJ-null \
 -showExternal False \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable False \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/userLsaGroup:1
#
set sg_userLsaGroup [ixNet add $ixNetSG_Stack(2) userLsaGroup]
ixNet setMultiAttrs $sg_userLsaGroup \
 -areaId 0 \
 -description {} \
 -enabled True
ixNet commit
set sg_userLsaGroup [lindex [ixNet remapIds $sg_userLsaGroup] 0]
set ixNetSG_Stack(3) $sg_userLsaGroup

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/userLsaGroup:1/userLsa:1
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.4.1 \
 -enabled True \
 -linkStateId 3.3.4.1 \
 -lsaType router \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/userLsaGroup:1/userLsa:1/router
#
set sg_router $ixNetSG_Stack(4)/router
ixNet setMultiAttrs $sg_router \
 -bBit False \
 -eBit False \
 -interfaces  { {20.20.20.7 11.1.7.2 pointToPoint 1} {11.1.7.0 255.255.255.0 stub 1} {3.3.4.1 255.255.255.255 stub 1} } \
 -vBit False
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/userLsaGroup:1/userLsa:2
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.4.1 \
 -enabled True \
 -linkStateId 1.0.20.7 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/userLsaGroup:1/userLsa:2/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv True
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/userLsaGroup:1/userLsa:2/opaque/routerTlv
#
set sg_routerTlv $ixNetSG_Stack(5)/routerTlv
ixNet setAttribute $sg_routerTlv -routerAddress 3.3.4.1
ixNet commit
set sg_routerTlv [lindex [ixNet remapIds $sg_routerTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/userLsaGroup:1/userLsa:3
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.4.1 \
 -enabled True \
 -linkStateId 1.0.20.8 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/userLsaGroup:1/userLsa:3/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/userLsaGroup:1/userLsa:3/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 20.20.20.7 \
 -linkLocalIpAddress 11.1.7.2 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.7.1 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/userLsaGroup:1/userLsa:4
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 20.20.20.7 \
 -enabled True \
 -linkStateId 1.0.20.9 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/userLsaGroup:1/userLsa:4/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:2/userLsaGroup:1/userLsa:4/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 3.3.4.1 \
 -linkLocalIpAddress 11.1.7.1 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.7.2 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3
#
set sg_router [ixNet add $ixNetSG_Stack(1)/protocols/ospf router]
ixNet setMultiAttrs $sg_router \
 -discardLearnedLsa True \
 -enabled True \
 -generateRouterLsa True \
 -gracefulRestart False \
 -rebuildAdjForLsdbChange False \
 -routerId 20.20.20.8 \
 -strictLsaChecking True \
 -supportForRfc3623 False \
 -supportReasonSoftReloadUpgrade True \
 -supportReasonSoftRestart True \
 -supportReasonSwotchRedundantCntrlProcessor True \
 -supportReasonUnknown True \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]
set ixNetSG_Stack(2) $sg_router

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut True \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 20.20.20.8 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes transit \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 0.0.0.0 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 66 \
 -priority 2 \
 -protocolInterface $ixNetSG_ref(124) \
 -showExternal True \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable True \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/interface:2
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut False \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 11.1.8.1 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes pointToPoint \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 3.3.5.1 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 64 \
 -priority 2 \
 -protocolInterface ::ixNet::OBJ-null \
 -showExternal False \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable False \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/userLsaGroup:1
#
set sg_userLsaGroup [ixNet add $ixNetSG_Stack(2) userLsaGroup]
ixNet setMultiAttrs $sg_userLsaGroup \
 -areaId 0 \
 -description {} \
 -enabled True
ixNet commit
set sg_userLsaGroup [lindex [ixNet remapIds $sg_userLsaGroup] 0]
set ixNetSG_Stack(3) $sg_userLsaGroup

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/userLsaGroup:1/userLsa:1
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.5.1 \
 -enabled True \
 -linkStateId 3.3.5.1 \
 -lsaType router \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/userLsaGroup:1/userLsa:1/router
#
set sg_router $ixNetSG_Stack(4)/router
ixNet setMultiAttrs $sg_router \
 -bBit False \
 -eBit False \
 -interfaces  { {20.20.20.8 11.1.8.2 pointToPoint 1} {11.1.8.0 255.255.255.0 stub 1} {3.3.5.1 255.255.255.255 stub 1} } \
 -vBit False
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/userLsaGroup:1/userLsa:2
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.5.1 \
 -enabled True \
 -linkStateId 1.0.20.8 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/userLsaGroup:1/userLsa:2/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv True
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/userLsaGroup:1/userLsa:2/opaque/routerTlv
#
set sg_routerTlv $ixNetSG_Stack(5)/routerTlv
ixNet setAttribute $sg_routerTlv -routerAddress 3.3.5.1
ixNet commit
set sg_routerTlv [lindex [ixNet remapIds $sg_routerTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/userLsaGroup:1/userLsa:3
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.5.1 \
 -enabled True \
 -linkStateId 1.0.20.9 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/userLsaGroup:1/userLsa:3/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/userLsaGroup:1/userLsa:3/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 20.20.20.8 \
 -linkLocalIpAddress 11.1.8.2 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.8.1 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/userLsaGroup:1/userLsa:4
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 20.20.20.8 \
 -enabled True \
 -linkStateId 1.0.20.10 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/userLsaGroup:1/userLsa:4/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:3/userLsaGroup:1/userLsa:4/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 3.3.5.1 \
 -linkLocalIpAddress 11.1.8.1 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.8.2 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4
#
set sg_router [ixNet add $ixNetSG_Stack(1)/protocols/ospf router]
ixNet setMultiAttrs $sg_router \
 -discardLearnedLsa True \
 -enabled True \
 -generateRouterLsa True \
 -gracefulRestart False \
 -rebuildAdjForLsdbChange False \
 -routerId 20.20.20.9 \
 -strictLsaChecking True \
 -supportForRfc3623 False \
 -supportReasonSoftReloadUpgrade True \
 -supportReasonSoftRestart True \
 -supportReasonSwotchRedundantCntrlProcessor True \
 -supportReasonUnknown True \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]
set ixNetSG_Stack(2) $sg_router

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut True \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 20.20.20.9 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes transit \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 0.0.0.0 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 66 \
 -priority 2 \
 -protocolInterface $ixNetSG_ref(128) \
 -showExternal True \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable True \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/interface:2
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut False \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 11.1.9.1 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes pointToPoint \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 3.3.6.1 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 64 \
 -priority 2 \
 -protocolInterface ::ixNet::OBJ-null \
 -showExternal False \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable False \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/userLsaGroup:1
#
set sg_userLsaGroup [ixNet add $ixNetSG_Stack(2) userLsaGroup]
ixNet setMultiAttrs $sg_userLsaGroup \
 -areaId 0 \
 -description {} \
 -enabled True
ixNet commit
set sg_userLsaGroup [lindex [ixNet remapIds $sg_userLsaGroup] 0]
set ixNetSG_Stack(3) $sg_userLsaGroup

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/userLsaGroup:1/userLsa:1
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.6.1 \
 -enabled True \
 -linkStateId 3.3.6.1 \
 -lsaType router \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/userLsaGroup:1/userLsa:1/router
#
set sg_router $ixNetSG_Stack(4)/router
ixNet setMultiAttrs $sg_router \
 -bBit False \
 -eBit False \
 -interfaces  { {20.20.20.9 11.1.9.2 pointToPoint 1} {11.1.9.0 255.255.255.0 stub 1} {3.3.6.1 255.255.255.255 stub 1} } \
 -vBit False
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/userLsaGroup:1/userLsa:2
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.6.1 \
 -enabled True \
 -linkStateId 1.0.20.9 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/userLsaGroup:1/userLsa:2/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv True
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/userLsaGroup:1/userLsa:2/opaque/routerTlv
#
set sg_routerTlv $ixNetSG_Stack(5)/routerTlv
ixNet setAttribute $sg_routerTlv -routerAddress 3.3.6.1
ixNet commit
set sg_routerTlv [lindex [ixNet remapIds $sg_routerTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/userLsaGroup:1/userLsa:3
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.6.1 \
 -enabled True \
 -linkStateId 1.0.20.10 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/userLsaGroup:1/userLsa:3/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/userLsaGroup:1/userLsa:3/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 20.20.20.9 \
 -linkLocalIpAddress 11.1.9.2 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.9.1 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/userLsaGroup:1/userLsa:4
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 20.20.20.9 \
 -enabled True \
 -linkStateId 1.0.20.11 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/userLsaGroup:1/userLsa:4/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:4/userLsaGroup:1/userLsa:4/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 3.3.6.1 \
 -linkLocalIpAddress 11.1.9.1 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.9.2 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5
#
set sg_router [ixNet add $ixNetSG_Stack(1)/protocols/ospf router]
ixNet setMultiAttrs $sg_router \
 -discardLearnedLsa True \
 -enabled True \
 -generateRouterLsa True \
 -gracefulRestart False \
 -rebuildAdjForLsdbChange False \
 -routerId 20.20.20.10 \
 -strictLsaChecking True \
 -supportForRfc3623 False \
 -supportReasonSoftReloadUpgrade True \
 -supportReasonSoftRestart True \
 -supportReasonSwotchRedundantCntrlProcessor True \
 -supportReasonUnknown True \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]
set ixNetSG_Stack(2) $sg_router

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut True \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 20.20.20.10 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes transit \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 0.0.0.0 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 66 \
 -priority 2 \
 -protocolInterface $ixNetSG_ref(132) \
 -showExternal True \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable True \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/interface:2
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -advertiseNetworkRange False \
 -areaId 0 \
 -authenticationMethods null \
 -authenticationPassword {} \
 -bBit False \
 -connectedToDut False \
 -deadInterval 40 \
 -eBit False \
 -enableAdvertiseRouterLsaLoopback False \
 -enableBfdRegistration False \
 -enabled True \
 -entryColumn 0 \
 -entryRow 0 \
 -helloInterval 10 \
 -interfaceIpAddress 11.1.10.1 \
 -interfaceIpMaskAddress 255.255.255.0 \
 -linkTypes pointToPoint \
 -md5AuthenticationKey {} \
 -md5AuthenticationKeyId 1 \
 -metric 10 \
 -mtu 1500 \
 -neighborIpAddress 0.0.0.0 \
 -neighborRouterId 3.3.7.1 \
 -networkRangeIp 0.0.0.0 \
 -networkRangeIpByMask False \
 -networkRangeIpIncrementBy 0.0.0.0 \
 -networkRangeIpMask 0 \
 -networkRangeLinkType broadcast \
 -networkRangeRouterId 0.0.0.0 \
 -networkRangeRouterIdIncrementBy 0.0.0.0 \
 -networkType broadcast \
 -noOfCols 0 \
 -noOfRows 0 \
 -options 64 \
 -priority 2 \
 -protocolInterface ::ixNet::OBJ-null \
 -showExternal False \
 -showNssa False \
 -teAdminGroup {00 00 00 00} \
 -teEnable False \
 -teMaxBandwidth 0 \
 -teMetricLevel 0 \
 -teResMaxBandwidth 0 \
 -teUnreservedBwPriority {0 0 0 0 0 0 0 0} \
 -validateReceivedMtuSize True
ixNet setMultiAttrs $sg_interface/learnedFilter \
 -advRouterId 0.0.0.0 \
 -enableAdvRouterId False \
 -enableFilter False \
 -enableLinkStateId False \
 -excludeAdvRouterId False \
 -excludeLinkStateId False \
 -linkStateId 0.0.0.0 \
 -showExternalAsLsa True \
 -showNetworkLsa True \
 -showNssaLsa True \
 -showOpaqueAreaLsa True \
 -showOpaqueDomainLsa True \
 -showOpaqueLocalLsa True \
 -showRouterLsa True \
 -showSummaryAsLsa True \
 -showSummaryIpLsa True
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/userLsaGroup:1
#
set sg_userLsaGroup [ixNet add $ixNetSG_Stack(2) userLsaGroup]
ixNet setMultiAttrs $sg_userLsaGroup \
 -areaId 0 \
 -description {} \
 -enabled True
ixNet commit
set sg_userLsaGroup [lindex [ixNet remapIds $sg_userLsaGroup] 0]
set ixNetSG_Stack(3) $sg_userLsaGroup

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/userLsaGroup:1/userLsa:1
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.7.1 \
 -enabled True \
 -linkStateId 3.3.7.1 \
 -lsaType router \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/userLsaGroup:1/userLsa:1/router
#
set sg_router $ixNetSG_Stack(4)/router
ixNet setMultiAttrs $sg_router \
 -bBit False \
 -eBit False \
 -interfaces  { {20.20.20.10 11.1.10.2 pointToPoint 1} {11.1.10.0 255.255.255.0 stub 1} {3.3.7.1 255.255.255.255 stub 1} } \
 -vBit False
ixNet commit
set sg_router [lindex [ixNet remapIds $sg_router] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/userLsaGroup:1/userLsa:2
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.7.1 \
 -enabled True \
 -linkStateId 1.0.20.10 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/userLsaGroup:1/userLsa:2/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv True
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/userLsaGroup:1/userLsa:2/opaque/routerTlv
#
set sg_routerTlv $ixNetSG_Stack(5)/routerTlv
ixNet setAttribute $sg_routerTlv -routerAddress 3.3.7.1
ixNet commit
set sg_routerTlv [lindex [ixNet remapIds $sg_routerTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/userLsaGroup:1/userLsa:3
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 3.3.7.1 \
 -enabled True \
 -linkStateId 1.0.20.11 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/userLsaGroup:1/userLsa:3/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/userLsaGroup:1/userLsa:3/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 20.20.20.10 \
 -linkLocalIpAddress 11.1.10.2 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.10.1 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/userLsaGroup:1/userLsa:4
#
set sg_userLsa [ixNet add $ixNetSG_Stack(3) userLsa]
ixNet setMultiAttrs $sg_userLsa \
 -advertisingRouterId 20.20.20.10 \
 -enabled True \
 -linkStateId 1.0.20.12 \
 -lsaType opaqueAreaScope \
 -optBitDemandCircuit False \
 -optBitExternalAttributes False \
 -optBitExternalRouting False \
 -optBitLsaNoForward True \
 -optBitMulticast False \
 -optBitNssaCapability False \
 -optBitTypeOfService False \
 -option 64
ixNet commit
set sg_userLsa [lindex [ixNet remapIds $sg_userLsa] 0]
set ixNetSG_Stack(4) $sg_userLsa

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/userLsaGroup:1/userLsa:4/opaque
#
set sg_opaque $ixNetSG_Stack(4)/opaque
ixNet setAttribute $sg_opaque -enableRouterTlv False
ixNet commit
set sg_opaque [lindex [ixNet remapIds $sg_opaque] 0]
set ixNetSG_Stack(5) $sg_opaque

#
# configuring the object that corresponds to /vport:2/protocols/ospf/router:5/userLsaGroup:1/userLsa:4/opaque/linkTlv
#
set sg_linkTlv $ixNetSG_Stack(5)/linkTlv
ixNet setMultiAttrs $sg_linkTlv \
 -enableLinkId True \
 -enableLinkMetric True \
 -enableLinkResourceClass False \
 -enableLinkType True \
 -enableLocalIpAddress True \
 -enableMaxBandwidth True \
 -enableMaxResBandwidth True \
 -enableRemoteIpAddress True \
 -enableUnreservedBandwidth True \
 -linkId 3.3.7.1 \
 -linkLocalIpAddress 11.1.10.1 \
 -linkMetric 1 \
 -linkRemoteIpAddress 11.1.10.2 \
 -linkResourceClass {00 00 00 00} \
 -linkType pointToPoint \
 -linkUnreservedBandwidth  { 1000 1000 1000 1000 1000 1000 1000 1000 } \
 -maxBandwidth 1000000 \
 -maxResBandwidth 100000 \
 -subTlvs  {  }
ixNet commit
set sg_linkTlv [lindex [ixNet remapIds $sg_linkTlv] 0]

#
# configuring the object that corresponds to /vport:2/protocols/rsvp/neighborPair:1
#
set sg_neighborPair [ixNet add $ixNetSG_Stack(1)/protocols/rsvp neighborPair]
ixNet setMultiAttrs $sg_neighborPair \
 -actualRestartTime 15000 \
 -dutIp 20.20.20.1 \
 -enableGracefulRestartHelperMode False \
 -enableGracefulRestartingMode True \
 -enableHello True \
 -enabled True \
 -gracefulRestartStartTime 30000 \
 -gracefulRestartUpTime 30000 \
 -helloInterval 5 \
 -helloTimeoutMultiplier 3 \
 -helloTlvs  {  } \
 -labelSpaceEnd 100000 \
 -labelSpaceStart 1000 \
 -numberOfGracefulRestarts 0 \
 -ourIp 20.20.20.6 \
 -recoveryTimeInterval 30000 \
 -refreshReduction False \
 -restartTimeInterval 30000 \
 -summaryRefreshInterval 15000 \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_neighborPair [lindex [ixNet remapIds $sg_neighborPair] 0]
set ixNetSG_Stack(2) $sg_neighborPair

#
# configuring the object that corresponds to /vport:2/protocols/rsvp/neighborPair:1/destinationRange:1
#
set sg_destinationRange [ixNet add $ixNetSG_Stack(2) destinationRange]
ixNet setMultiAttrs $sg_destinationRange \
 -behavior egress \
 -emulationType rsvpTe \
 -enabled True \
 -ipAddressFrom 3.3.3.1 \
 -ipCount 1 \
 -isConnectedIpAppended True \
 -isHeadIpPrepended True \
 -isLeafIpPrepended True \
 -isSendingAsRro True \
 -isSendingAsSrro False \
 -p2mpId 3.3.3.1
ixNet setMultiAttrs $sg_destinationRange/egress \
 -bandwidth 0 \
 -egressBehavior alwaysUseConfiguredStyle \
 -enableFixedLabelForResv False \
 -labelValue {explicitNull} \
 -pathErrorTlv  {  } \
 -reflectRro True \
 -refreshInterval 30000 \
 -reservationStyle se \
 -reservationTearTlv  {  } \
 -reservationTlv  {  } \
 -rro  {  } \
 -sendResvConfirmation False \
 -timeoutMultiplier 3
ixNet setMultiAttrs $sg_destinationRange/ingress \
 -enableEro False \
 -ero  {  } \
 -prefixLength 32 \
 -prependDutToEro prependLoose \
 -reservationErrorTlv  {  } \
 -rro  {  } \
 -sendRro False \
 -tunnelIdsCount 1 \
 -tunnelIdsStart 1
ixNet commit
set sg_destinationRange [lindex [ixNet remapIds $sg_destinationRange] 0]

#
# configuring the object that corresponds to /vport:2/protocols/rsvp/neighborPair:2
#
set sg_neighborPair [ixNet add $ixNetSG_Stack(1)/protocols/rsvp neighborPair]
ixNet setMultiAttrs $sg_neighborPair \
 -actualRestartTime 15000 \
 -dutIp 20.20.20.2 \
 -enableGracefulRestartHelperMode False \
 -enableGracefulRestartingMode True \
 -enableHello True \
 -enabled True \
 -gracefulRestartStartTime 30000 \
 -gracefulRestartUpTime 30000 \
 -helloInterval 5 \
 -helloTimeoutMultiplier 3 \
 -helloTlvs  {  } \
 -labelSpaceEnd 100000 \
 -labelSpaceStart 1000 \
 -numberOfGracefulRestarts 0 \
 -ourIp 20.20.20.7 \
 -recoveryTimeInterval 30000 \
 -refreshReduction False \
 -restartTimeInterval 30000 \
 -summaryRefreshInterval 15000 \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_neighborPair [lindex [ixNet remapIds $sg_neighborPair] 0]
set ixNetSG_Stack(2) $sg_neighborPair

#
# configuring the object that corresponds to /vport:2/protocols/rsvp/neighborPair:2/destinationRange:1
#
set sg_destinationRange [ixNet add $ixNetSG_Stack(2) destinationRange]
ixNet setMultiAttrs $sg_destinationRange \
 -behavior egress \
 -emulationType rsvpTe \
 -enabled True \
 -ipAddressFrom 3.3.4.1 \
 -ipCount 1 \
 -isConnectedIpAppended True \
 -isHeadIpPrepended True \
 -isLeafIpPrepended True \
 -isSendingAsRro True \
 -isSendingAsSrro False \
 -p2mpId 3.3.4.1
ixNet setMultiAttrs $sg_destinationRange/egress \
 -bandwidth 0 \
 -egressBehavior alwaysUseConfiguredStyle \
 -enableFixedLabelForResv False \
 -labelValue {explicitNull} \
 -pathErrorTlv  {  } \
 -reflectRro True \
 -refreshInterval 30000 \
 -reservationStyle se \
 -reservationTearTlv  {  } \
 -reservationTlv  {  } \
 -rro  {  } \
 -sendResvConfirmation False \
 -timeoutMultiplier 3
ixNet setMultiAttrs $sg_destinationRange/ingress \
 -enableEro False \
 -ero  {  } \
 -prefixLength 32 \
 -prependDutToEro prependLoose \
 -reservationErrorTlv  {  } \
 -rro  {  } \
 -sendRro False \
 -tunnelIdsCount 1 \
 -tunnelIdsStart 1
ixNet commit
set sg_destinationRange [lindex [ixNet remapIds $sg_destinationRange] 0]

#
# configuring the object that corresponds to /vport:2/protocols/rsvp/neighborPair:3
#
set sg_neighborPair [ixNet add $ixNetSG_Stack(1)/protocols/rsvp neighborPair]
ixNet setMultiAttrs $sg_neighborPair \
 -actualRestartTime 15000 \
 -dutIp 20.20.20.3 \
 -enableGracefulRestartHelperMode False \
 -enableGracefulRestartingMode True \
 -enableHello True \
 -enabled True \
 -gracefulRestartStartTime 30000 \
 -gracefulRestartUpTime 30000 \
 -helloInterval 5 \
 -helloTimeoutMultiplier 3 \
 -helloTlvs  {  } \
 -labelSpaceEnd 100000 \
 -labelSpaceStart 1000 \
 -numberOfGracefulRestarts 0 \
 -ourIp 20.20.20.8 \
 -recoveryTimeInterval 30000 \
 -refreshReduction False \
 -restartTimeInterval 30000 \
 -summaryRefreshInterval 15000 \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_neighborPair [lindex [ixNet remapIds $sg_neighborPair] 0]
set ixNetSG_Stack(2) $sg_neighborPair

#
# configuring the object that corresponds to /vport:2/protocols/rsvp/neighborPair:3/destinationRange:1
#
set sg_destinationRange [ixNet add $ixNetSG_Stack(2) destinationRange]
ixNet setMultiAttrs $sg_destinationRange \
 -behavior egress \
 -emulationType rsvpTe \
 -enabled True \
 -ipAddressFrom 3.3.5.1 \
 -ipCount 1 \
 -isConnectedIpAppended True \
 -isHeadIpPrepended True \
 -isLeafIpPrepended True \
 -isSendingAsRro True \
 -isSendingAsSrro False \
 -p2mpId 3.3.5.1
ixNet setMultiAttrs $sg_destinationRange/egress \
 -bandwidth 0 \
 -egressBehavior alwaysUseConfiguredStyle \
 -enableFixedLabelForResv False \
 -labelValue {explicitNull} \
 -pathErrorTlv  {  } \
 -reflectRro True \
 -refreshInterval 30000 \
 -reservationStyle se \
 -reservationTearTlv  {  } \
 -reservationTlv  {  } \
 -rro  {  } \
 -sendResvConfirmation False \
 -timeoutMultiplier 3
ixNet setMultiAttrs $sg_destinationRange/ingress \
 -enableEro False \
 -ero  {  } \
 -prefixLength 32 \
 -prependDutToEro prependLoose \
 -reservationErrorTlv  {  } \
 -rro  {  } \
 -sendRro False \
 -tunnelIdsCount 1 \
 -tunnelIdsStart 1
ixNet commit
set sg_destinationRange [lindex [ixNet remapIds $sg_destinationRange] 0]

#
# configuring the object that corresponds to /vport:2/protocols/rsvp/neighborPair:4
#
set sg_neighborPair [ixNet add $ixNetSG_Stack(1)/protocols/rsvp neighborPair]
ixNet setMultiAttrs $sg_neighborPair \
 -actualRestartTime 15000 \
 -dutIp 20.20.20.4 \
 -enableGracefulRestartHelperMode False \
 -enableGracefulRestartingMode True \
 -enableHello True \
 -enabled True \
 -gracefulRestartStartTime 30000 \
 -gracefulRestartUpTime 30000 \
 -helloInterval 5 \
 -helloTimeoutMultiplier 3 \
 -helloTlvs  {  } \
 -labelSpaceEnd 100000 \
 -labelSpaceStart 1000 \
 -numberOfGracefulRestarts 0 \
 -ourIp 20.20.20.9 \
 -recoveryTimeInterval 30000 \
 -refreshReduction False \
 -restartTimeInterval 30000 \
 -summaryRefreshInterval 15000 \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_neighborPair [lindex [ixNet remapIds $sg_neighborPair] 0]
set ixNetSG_Stack(2) $sg_neighborPair

#
# configuring the object that corresponds to /vport:2/protocols/rsvp/neighborPair:4/destinationRange:1
#
set sg_destinationRange [ixNet add $ixNetSG_Stack(2) destinationRange]
ixNet setMultiAttrs $sg_destinationRange \
 -behavior egress \
 -emulationType rsvpTe \
 -enabled True \
 -ipAddressFrom 3.3.6.1 \
 -ipCount 1 \
 -isConnectedIpAppended True \
 -isHeadIpPrepended True \
 -isLeafIpPrepended True \
 -isSendingAsRro True \
 -isSendingAsSrro False \
 -p2mpId 3.3.6.1
ixNet setMultiAttrs $sg_destinationRange/egress \
 -bandwidth 0 \
 -egressBehavior alwaysUseConfiguredStyle \
 -enableFixedLabelForResv False \
 -labelValue {explicitNull} \
 -pathErrorTlv  {  } \
 -reflectRro True \
 -refreshInterval 30000 \
 -reservationStyle se \
 -reservationTearTlv  {  } \
 -reservationTlv  {  } \
 -rro  {  } \
 -sendResvConfirmation False \
 -timeoutMultiplier 3
ixNet setMultiAttrs $sg_destinationRange/ingress \
 -enableEro False \
 -ero  {  } \
 -prefixLength 32 \
 -prependDutToEro prependLoose \
 -reservationErrorTlv  {  } \
 -rro  {  } \
 -sendRro False \
 -tunnelIdsCount 1 \
 -tunnelIdsStart 1
ixNet commit
set sg_destinationRange [lindex [ixNet remapIds $sg_destinationRange] 0]

#
# configuring the object that corresponds to /vport:2/protocols/rsvp/neighborPair:5
#
set sg_neighborPair [ixNet add $ixNetSG_Stack(1)/protocols/rsvp neighborPair]
ixNet setMultiAttrs $sg_neighborPair \
 -actualRestartTime 15000 \
 -dutIp 20.20.20.5 \
 -enableGracefulRestartHelperMode False \
 -enableGracefulRestartingMode True \
 -enableHello True \
 -enabled True \
 -gracefulRestartStartTime 30000 \
 -gracefulRestartUpTime 30000 \
 -helloInterval 5 \
 -helloTimeoutMultiplier 3 \
 -helloTlvs  {  } \
 -labelSpaceEnd 100000 \
 -labelSpaceStart 1000 \
 -numberOfGracefulRestarts 0 \
 -ourIp 20.20.20.10 \
 -recoveryTimeInterval 30000 \
 -refreshReduction False \
 -restartTimeInterval 30000 \
 -summaryRefreshInterval 15000 \
 -trafficGroupId ::ixNet::OBJ-null
ixNet commit
set sg_neighborPair [lindex [ixNet remapIds $sg_neighborPair] 0]
set ixNetSG_Stack(2) $sg_neighborPair

#
# configuring the object that corresponds to /vport:2/protocols/rsvp/neighborPair:5/destinationRange:1
#
set sg_destinationRange [ixNet add $ixNetSG_Stack(2) destinationRange]
ixNet setMultiAttrs $sg_destinationRange \
 -behavior egress \
 -emulationType rsvpTe \
 -enabled True \
 -ipAddressFrom 3.3.7.1 \
 -ipCount 1 \
 -isConnectedIpAppended True \
 -isHeadIpPrepended True \
 -isLeafIpPrepended True \
 -isSendingAsRro True \
 -isSendingAsSrro False \
 -p2mpId 3.3.7.1
ixNet setMultiAttrs $sg_destinationRange/egress \
 -bandwidth 0 \
 -egressBehavior alwaysUseConfiguredStyle \
 -enableFixedLabelForResv False \
 -labelValue {explicitNull} \
 -pathErrorTlv  {  } \
 -reflectRro True \
 -refreshInterval 30000 \
 -reservationStyle se \
 -reservationTearTlv  {  } \
 -reservationTlv  {  } \
 -rro  {  } \
 -sendResvConfirmation False \
 -timeoutMultiplier 3
ixNet setMultiAttrs $sg_destinationRange/ingress \
 -enableEro False \
 -ero  {  } \
 -prefixLength 32 \
 -prependDutToEro prependLoose \
 -reservationErrorTlv  {  } \
 -rro  {  } \
 -sendRro False \
 -tunnelIdsCount 1 \
 -tunnelIdsStart 1
ixNet commit
set sg_destinationRange [lindex [ixNet remapIds $sg_destinationRange] 0]

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
ixNet setMultiAttrs $sg_fixedDuration \
 -selectedItems  {  }
ixNet setMultiAttrs $sg_fixedDuration/testSetup \
 -selectedVariableParameter percentLineRate
ixNet setMultiAttrs $sg_fixedDuration/testSetup/variableLoop \
 -backoff 0 \
 -algorithm unchanged \
 -maxValue 0 \
 -initialValue 0 \
 -value 0 \
 -stepValue 0 \
 -resolution 0 \
 -valueList  {  } \
 -acceptableFrameLoss 0 \
 -minValue 0
ixNet setMultiAttrs $sg_fixedDuration/testSetup/additionalLoop \
 -selectedAdditionalLoopParameter frameSize \
 -algorithm unchanged \
 -maxValue 0 \
 -initialValue 0 \
 -value 0 \
 -valueList  {  } \
 -step 0 \
 -count 1
ixNet setMultiAttrs $sg_fixedDuration/protocols \
 -startBehavior startWithCurrent \
 -waitAfterStop 0 \
 -waitAfterStart 0
ixNet setMultiAttrs $sg_fixedDuration/traffic \
 -learningStartDelay 0 \
 -l3RepeatCount 3 \
 -l3Gap 1 \
 -l2FrameSizeType sameAsStream \
 -learningFrequency oncePerTest \
 -l3RepeatInterval 2 \
 -enableStaggeredTransmit False \
 -trafficStartDelay 5 \
 -l2BurstCount 1 \
 -l2FrameSize 128 \
 -delayAfterTransmit 5 \
 -generateStreams True \
 -enableLearning False \
 -l2Rate 1
ixNet setMultiAttrs $sg_fixedDuration/runParameters \
 -enableCalculateLatency False \
 -latencyLessThanEqualTo 10 \
 -enableRatePassCriteria False \
 -latencyPortType averagePort \
 -latencyUnit microSeconds \
 -testDuration {00:00:20} \
 -ratePortType averagePort \
 -enableLatencyCriteria False \
 -numTrials 1 \
 -rateGreaterThanEqualTo 10
ixNet commit
set sg_fixedDuration [lindex [ixNet remapIds $sg_fixedDuration] 0]
return 0
}

ixNetScriptgenProc
