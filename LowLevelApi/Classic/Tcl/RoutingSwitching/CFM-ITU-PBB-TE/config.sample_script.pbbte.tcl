# IxNetwork version: 5.35.54.323
# time of scriptgen: 11/6/2008, 1:18 PM

package require IxTclNetwork
proc ixNetScriptgenProc {} {
ixNet rollback
ixNet setSessionParameter version 5.35.54.323
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
 -rxMode capture \
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
 -enabled True \
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
 -enabled False
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
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/stp \
 -enabled False
ixNet setMultiAttrs $sg_vport/capture \
 -hardwareEnabled False \
 -softwareEnabled False
ixNet commit
set sg_vport [lindex [ixNet remapIds $sg_vport] 0]
set ixNetSG_ref(2) $sg_vport
set ixNetSG_Stack(1) $sg_vport

#
# configuring the object that corresponds to /vport:1/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {Connected - ProtocolInterface - 100:01 - 1} \
 -enabled True \
 -eui64Id {02 00 0E FF FE FA C1 15 } \
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
 -macAddress "00:00:0e:fa:c1:15" \
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
 -vlanId {1} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(3) $sg_interface

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
 -vendorSpecificInformation {00000000} \
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
# configuring the object that corresponds to /vport:1/protocols/cfm/bridge:1
#
set sg_bridge [ixNet add $ixNetSG_Stack(1)/protocols/cfm bridge]
ixNet setMultiAttrs $sg_bridge \
 -aisInterval oneSec \
 -bridgeId "00:00:98:52:00:01" \
 -enableAis False \
 -enableOutOfSequenceDetection False \
 -enabled True \
 -encapsulation ethernet \
 -etherType 35074 \
 -garbageCollectTime 10 \
 -operationMode pbbTe \
 -userBvlan allVlanId \
 -userBvlanId 0 \
 -userBvlanPriority 0 \
 -userBvlanTpId {0x8100} \
 -userCvlan noVlanId \
 -userCvlanId 0 \
 -userCvlanPriority 0 \
 -userCvlanTpId {0x8100} \
 -userDelayType dm \
 -userDstMacAddress "00:00:00:00:00:00" \
 -userDstMepId 1 \
 -userDstType mepMac \
 -userLearnedInfoTimeOut 5000 \
 -userMdLevel allMd \
 -userPbbTeDelayType dm \
 -userPeriodicOamType linkTrace \
 -userSendType unicast \
 -userShortMaName {} \
 -userShortMaNameFormat allFormats \
 -userSrcMacAddress "00:00:00:00:00:00" \
 -userSrcMepId 1 \
 -userSrcType mepMac \
 -userSvlan noVlanId \
 -userSvlanId 0 \
 -userSvlanPriority 0 \
 -userSvlanTpId {0x8100} \
 -userTransactionId 1 \
 -userTtlInterval 64 \
 -userUsabilityOption manual
ixNet commit
set sg_bridge [lindex [ixNet remapIds $sg_bridge] 0]
set ixNetSG_Stack(2) $sg_bridge

#
# configuring the object that corresponds to /vport:1/protocols/cfm/bridge:1/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -enabled True \
 -interfaceId $ixNetSG_ref(3)
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:1/protocols/cfm/bridge:1/link:1
#
set sg_link [ixNet add $ixNetSG_Stack(2) link]
ixNet setMultiAttrs $sg_link \
 -enabled False \
 -linkType pointToPoint \
 -moreMps  {  } \
 -mpOutwardsIxia ::ixNet::OBJ-null \
 -mpTowardsIxia ::ixNet::OBJ-null
ixNet commit
set sg_link [lindex [ixNet remapIds $sg_link] 0]
set ixNetSG_ref(8) $sg_link

#
# configuring the object that corresponds to /vport:1/protocols/cfm/bridge:1/mdLevel:1
#
set sg_mdLevel [ixNet add $ixNetSG_Stack(2) mdLevel]
ixNet setMultiAttrs $sg_mdLevel \
 -enabled False \
 -mdLevelId 0 \
 -mdName {Ixiacom-0} \
 -mdNameFormat characterString
ixNet commit
set sg_mdLevel [lindex [ixNet remapIds $sg_mdLevel] 0]
set ixNetSG_ref(9) $sg_mdLevel

#
# configuring the object that corresponds to /vport:1/protocols/cfm/bridge:1/mp:1
#
set sg_mp [ixNet add $ixNetSG_Stack(2) mp]
ixNet setMultiAttrs $sg_mp \
 -addCcmCustomTlvs False \
 -addDataTlv True \
 -addInterfaceStatusTlv True \
 -addLbmCustomTlvs False \
 -addLbrCustomTlvs False \
 -addLtmCustomTlvs False \
 -addLtrCustomTlvs False \
 -addOrganizationSpecificTlv False \
 -addPortStatusTlv True \
 -addSenderIdTlv True \
 -autoDmAllDestination False \
 -autoDmDestination "00:00:00:00:00:00" \
 -autoDmIteration 0 \
 -autoDmTimeout 30 \
 -autoDmTimer 60 \
 -autoLbAllDestination False \
 -autoLbDestination "00:00:00:00:00:00" \
 -autoLbIteration 0 \
 -autoLbTimeout 30 \
 -autoLbTimer 60 \
 -autoLtAllDestination False \
 -autoLtDestination "00:00:00:00:00:00" \
 -autoLtIteration 0 \
 -autoLtTimeout 30 \
 -autoLtTimer 60 \
 -cciInterval 1sec \
 -ccmPriority 0 \
 -chassisId {00 00 00 00 00 00 } \
 -chassisIdLength 6 \
 -chassisIdSubType macAddress \
 -dataTlvLength 4 \
 -dataTlvValue {44 61 74 61 } \
 -dmmPriority 0 \
 -enableAutoDm False \
 -enableAutoLb False \
 -enableAutoLt False \
 -enabled False \
 -lbmPriority 0 \
 -ltmPriority 0 \
 -macAddress "00:00:00:00:00:01" \
 -managementAddress {01 02 03 03 04 05 } \
 -managementAddressDomain {4D 61 6E 61 67 65 6D 65 6E 74 20 41 64 64 72 20 44 6F 6D 61 69 6E } \
 -managementAddressDomainLength 22 \
 -managementAddressLength 6 \
 -mdLevel $ixNetSG_ref(9) \
 -megId {Ixia-00001} \
 -megIdFormat iccBasedFormat \
 -mepId 1 \
 -mipId 1 \
 -mpType mep \
 -organizationSpecificTlvLength 4 \
 -organizationSpecificTlvValue {00 00 00 00 } \
 -overrideVlanPriority False \
 -shortMaName {Ixia-0} \
 -shortMaNameFormat characterString \
 -ttl 64 \
 -vlan ::ixNet::OBJ-null
ixNet commit
set sg_mp [lindex [ixNet remapIds $sg_mp] 0]
set ixNetSG_ref(10) $sg_mp
ixNet setAttribute $ixNetSG_ref(8) -mpOutwardsIxia $ixNetSG_ref(10)
ixNet commit

#
# configuring the object that corresponds to /vport:1/protocols/cfm/bridge:1/trunk:1
#
set sg_trunk [ixNet add $ixNetSG_Stack(2) trunk]
ixNet setMultiAttrs $sg_trunk \
 -addCcmCustomTlvs False \
 -addDataTlv True \
 -addInterfaceStatusTlv False \
 -addLbmCustomTlvs True \
 -addLbrCustomTlvs True \
 -addLtmCustomTlvs False \
 -addLtrCustomTlvs False \
 -addOrganizationSpecificTlv True \
 -addPortStatusTlv False \
 -addSenderIdTlv False \
 -autoDmIteration 2 \
 -autoDmTimeout 5 \
 -autoDmTimer 5 \
 -autoLbIteration 2 \
 -autoLbTimeout 5 \
 -autoLbTimer 5 \
 -autoLtIteration 2 \
 -autoLtTimeout 5 \
 -autoLtTimer 5 \
 -bVlanId 1 \
 -bVlanPriority 0 \
 -bVlanTpId {0x8100} \
 -cciInterval 1sec \
 -ccmPriority 0 \
 -chassisId {00 00 00 00 00 00 } \
 -chassisIdLength 6 \
 -chassisIdSubType networkAddress \
 -dataTlvLength 4 \
 -dataTlvValue {44 61 74 61 } \
 -dmmPriority 0 \
 -dstMacAddress "00:00:00:00:00:02" \
 -enableAutoDm True \
 -enableAutoLb True \
 -enableAutoLt True \
 -enableReverseBvlan True \
 -enabled True \
 -lbmPriority 0 \
 -ltmPriority 0 \
 -managementAddress {01 02 03 03 04 05 } \
 -managementAddressDomain {00 00 00 00 00 00 } \
 -managementAddressDomainLength 22 \
 -managementAddressLength 6 \
 -mdLevelId 0 \
 -mdName {Ixiacom-0} \
 -mdNameFormat characterString \
 -mepId 1 \
 -organizationSpecificTlvLength 4 \
 -organizationSpecificTlvValue {10 00 00 00 } \
 -overrideVlanPriority False \
 -reverseBvlanId 5 \
 -shortMaName {Ixia-0} \
 -shortMaNameFormat characterString \
 -srcMacAddress "00:00:00:00:00:01" \
 -ttl 64
ixNet commit
set sg_trunk [lindex [ixNet remapIds $sg_trunk] 0]
set ixNetSG_Stack(3) $sg_trunk

#
# configuring the object that corresponds to /vport:1/protocols/cfm/bridge:1/trunk:1/macRanges:1
#
set sg_macRanges [ixNet add $ixNetSG_Stack(3) macRanges]
ixNet setMultiAttrs $sg_macRanges \
 -cVlanId 1 \
 -cVlanPriority 0 \
 -cVlanTpId {0x8100} \
 -count 1 \
 -enableVlan False \
 -enabled True \
 -iTagiSid 10 \
 -sVlanId 1 \
 -sVlanPriority 0 \
 -sVlanTpId {0x8100} \
 -startMacAddress "00:00:00:00:00:05" \
 -step "00:00:00:00:00:00" \
 -trafficGroupId ::ixNet::OBJ-null \
 -type singleVlan
ixNet commit
set sg_macRanges [lindex [ixNet remapIds $sg_macRanges] 0]

#
# configuring the object that corresponds to /vport:2
#
set sg_vport [ixNet add $ixNetSG_Stack(0) vport]
ixNet setMultiAttrs $sg_vport \
 -rxMode capture \
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
 -enabled True \
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
 -enabled False
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
 -enabled False
ixNet setMultiAttrs $sg_vport/protocols/stp \
 -enabled False
ixNet setMultiAttrs $sg_vport/capture \
 -hardwareEnabled True \
 -softwareEnabled True
ixNet commit
set sg_vport [lindex [ixNet remapIds $sg_vport] 0]
set ixNetSG_ref(13) $sg_vport
set ixNetSG_Stack(1) $sg_vport

#
# configuring the object that corresponds to /vport:2/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setMultiAttrs $sg_interface \
 -description {Connected - ProtocolInterface - 100:02 - 2} \
 -enabled True \
 -eui64Id {02 00 0E FF FE FA C1 16 } \
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
 -macAddress "00:00:0e:fa:c1:16" \
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
 -vlanId {1} \
 -vlanPriority {0}
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]
set ixNetSG_ref(14) $sg_interface

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
 -vendorSpecificInformation {00000000} \
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
# configuring the object that corresponds to /vport:2/protocols/cfm/bridge:1
#
set sg_bridge [ixNet add $ixNetSG_Stack(1)/protocols/cfm bridge]
ixNet setMultiAttrs $sg_bridge \
 -aisInterval oneSec \
 -bridgeId "00:00:98:53:00:01" \
 -enableAis False \
 -enableOutOfSequenceDetection False \
 -enabled True \
 -encapsulation ethernet \
 -etherType 35074 \
 -garbageCollectTime 10 \
 -operationMode pbbTe \
 -userBvlan allVlanId \
 -userBvlanId 0 \
 -userBvlanPriority 0 \
 -userBvlanTpId {0x8100} \
 -userCvlan noVlanId \
 -userCvlanId 0 \
 -userCvlanPriority 0 \
 -userCvlanTpId {0x8100} \
 -userDelayType dm \
 -userDstMacAddress "00:00:00:00:00:00" \
 -userDstMepId 1 \
 -userDstType mepMac \
 -userLearnedInfoTimeOut 5000 \
 -userMdLevel allMd \
 -userPbbTeDelayType dm \
 -userPeriodicOamType linkTrace \
 -userSendType unicast \
 -userShortMaName {} \
 -userShortMaNameFormat allFormats \
 -userSrcMacAddress "00:00:00:00:00:00" \
 -userSrcMepId 1 \
 -userSrcType mepMac \
 -userSvlan noVlanId \
 -userSvlanId 0 \
 -userSvlanPriority 0 \
 -userSvlanTpId {0x8100} \
 -userTransactionId 1 \
 -userTtlInterval 64 \
 -userUsabilityOption manual
ixNet commit
set sg_bridge [lindex [ixNet remapIds $sg_bridge] 0]
set ixNetSG_Stack(2) $sg_bridge

#
# configuring the object that corresponds to /vport:2/protocols/cfm/bridge:1/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(2) interface]
ixNet setMultiAttrs $sg_interface \
 -enabled True \
 -interfaceId $ixNetSG_ref(14)
ixNet commit
set sg_interface [lindex [ixNet remapIds $sg_interface] 0]

#
# configuring the object that corresponds to /vport:2/protocols/cfm/bridge:1/link:1
#
set sg_link [ixNet add $ixNetSG_Stack(2) link]
ixNet setMultiAttrs $sg_link \
 -enabled False \
 -linkType pointToPoint \
 -moreMps  {  } \
 -mpOutwardsIxia ::ixNet::OBJ-null \
 -mpTowardsIxia ::ixNet::OBJ-null
ixNet commit
set sg_link [lindex [ixNet remapIds $sg_link] 0]
set ixNetSG_ref(19) $sg_link

#
# configuring the object that corresponds to /vport:2/protocols/cfm/bridge:1/mdLevel:1
#
set sg_mdLevel [ixNet add $ixNetSG_Stack(2) mdLevel]
ixNet setMultiAttrs $sg_mdLevel \
 -enabled False \
 -mdLevelId 0 \
 -mdName {Ixiacom-0} \
 -mdNameFormat characterString
ixNet commit
set sg_mdLevel [lindex [ixNet remapIds $sg_mdLevel] 0]
set ixNetSG_ref(20) $sg_mdLevel

#
# configuring the object that corresponds to /vport:2/protocols/cfm/bridge:1/mp:1
#
set sg_mp [ixNet add $ixNetSG_Stack(2) mp]
ixNet setMultiAttrs $sg_mp \
 -addCcmCustomTlvs False \
 -addDataTlv True \
 -addInterfaceStatusTlv True \
 -addLbmCustomTlvs False \
 -addLbrCustomTlvs False \
 -addLtmCustomTlvs False \
 -addLtrCustomTlvs False \
 -addOrganizationSpecificTlv False \
 -addPortStatusTlv True \
 -addSenderIdTlv True \
 -autoDmAllDestination False \
 -autoDmDestination "00:00:00:00:00:00" \
 -autoDmIteration 0 \
 -autoDmTimeout 30 \
 -autoDmTimer 60 \
 -autoLbAllDestination False \
 -autoLbDestination "00:00:00:00:00:00" \
 -autoLbIteration 0 \
 -autoLbTimeout 30 \
 -autoLbTimer 60 \
 -autoLtAllDestination False \
 -autoLtDestination "00:00:00:00:00:00" \
 -autoLtIteration 0 \
 -autoLtTimeout 30 \
 -autoLtTimer 60 \
 -cciInterval 1sec \
 -ccmPriority 0 \
 -chassisId {00 00 00 00 00 00 } \
 -chassisIdLength 6 \
 -chassisIdSubType macAddress \
 -dataTlvLength 4 \
 -dataTlvValue {44 61 74 61 } \
 -dmmPriority 0 \
 -enableAutoDm False \
 -enableAutoLb False \
 -enableAutoLt False \
 -enabled False \
 -lbmPriority 0 \
 -ltmPriority 0 \
 -macAddress "00:00:00:00:00:02" \
 -managementAddress {01 02 03 03 04 05 } \
 -managementAddressDomain {4D 61 6E 61 67 65 6D 65 6E 74 20 41 64 64 72 20 44 6F 6D 61 69 6E } \
 -managementAddressDomainLength 22 \
 -managementAddressLength 6 \
 -mdLevel $ixNetSG_ref(20) \
 -megId {Ixia-00001} \
 -megIdFormat iccBasedFormat \
 -mepId 2 \
 -mipId 2 \
 -mpType mep \
 -organizationSpecificTlvLength 4 \
 -organizationSpecificTlvValue {00 00 00 00 } \
 -overrideVlanPriority False \
 -shortMaName {Ixia-0} \
 -shortMaNameFormat characterString \
 -ttl 64 \
 -vlan ::ixNet::OBJ-null
ixNet commit
set sg_mp [lindex [ixNet remapIds $sg_mp] 0]
set ixNetSG_ref(21) $sg_mp
ixNet setAttribute $ixNetSG_ref(19) -mpOutwardsIxia $ixNetSG_ref(21)
ixNet commit

#
# configuring the object that corresponds to /vport:2/protocols/cfm/bridge:1/trunk:1
#
set sg_trunk [ixNet add $ixNetSG_Stack(2) trunk]
ixNet setMultiAttrs $sg_trunk \
 -addCcmCustomTlvs False \
 -addDataTlv True \
 -addInterfaceStatusTlv False \
 -addLbmCustomTlvs True \
 -addLbrCustomTlvs True \
 -addLtmCustomTlvs False \
 -addLtrCustomTlvs False \
 -addOrganizationSpecificTlv True \
 -addPortStatusTlv False \
 -addSenderIdTlv False \
 -autoDmIteration 2 \
 -autoDmTimeout 5 \
 -autoDmTimer 5 \
 -autoLbIteration 2 \
 -autoLbTimeout 5 \
 -autoLbTimer 5 \
 -autoLtIteration 2 \
 -autoLtTimeout 5 \
 -autoLtTimer 5 \
 -bVlanId 1 \
 -bVlanPriority 0 \
 -bVlanTpId {0x8100} \
 -cciInterval 1sec \
 -ccmPriority 0 \
 -chassisId {00 00 00 00 00 00 } \
 -chassisIdLength 6 \
 -chassisIdSubType networkAddress \
 -dataTlvLength 4 \
 -dataTlvValue {44 61 74 61 } \
 -dmmPriority 0 \
 -dstMacAddress "00:00:00:00:00:01" \
 -enableAutoDm True \
 -enableAutoLb True \
 -enableAutoLt True \
 -enableReverseBvlan True \
 -enabled True \
 -lbmPriority 0 \
 -ltmPriority 0 \
 -managementAddress {01 02 03 03 04 05 } \
 -managementAddressDomain {00 00 00 00 00 00 } \
 -managementAddressDomainLength 22 \
 -managementAddressLength 6 \
 -mdLevelId 0 \
 -mdName {Ixiacom-0} \
 -mdNameFormat characterString \
 -mepId 2 \
 -organizationSpecificTlvLength 4 \
 -organizationSpecificTlvValue {10 00 00 00 } \
 -overrideVlanPriority False \
 -reverseBvlanId 5 \
 -shortMaName {Ixia-0} \
 -shortMaNameFormat characterString \
 -srcMacAddress "00:00:00:00:00:02" \
 -ttl 64
ixNet commit
set sg_trunk [lindex [ixNet remapIds $sg_trunk] 0]
set ixNetSG_Stack(3) $sg_trunk

#
# configuring the object that corresponds to /vport:2/protocols/cfm/bridge:1/trunk:1/macRanges:1
#
set sg_macRanges [ixNet add $ixNetSG_Stack(3) macRanges]
ixNet setMultiAttrs $sg_macRanges \
 -cVlanId 1 \
 -cVlanPriority 0 \
 -cVlanTpId {0x8100} \
 -count 1 \
 -enableVlan False \
 -enabled True \
 -iTagiSid 10 \
 -sVlanId 1 \
 -sVlanPriority 0 \
 -sVlanTpId {0x8100} \
 -startMacAddress "00:00:00:00:00:10" \
 -step "00:00:00:00:00:00" \
 -trafficGroupId ::ixNet::OBJ-null \
 -type singleVlan
ixNet commit
set sg_macRanges [lindex [ixNet remapIds $sg_macRanges] 0]

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

###
### /traffic area
###

#
# configuring the object that corresponds to /traffic/trafficItem:5
#
set sg_trafficItem [ixNet add $ixNetSG_Stack(0)/traffic trafficItem]
ixNet setMultiAttrs $sg_trafficItem \
 -allowSelfDestined False \
 -payloadType incByte \
 -encapsulationType macInMac \
 -routeMesh oneToOne \
 -endpointType ethernetVlan \
 -streamPackingMode optimalPacking \
 -forceError noError \
 -name {TI0-TRAFFICITEM} \
 -enabled True \
 -hostsPerNetwork 1 \
 -srcDestMesh oneToOne \
 -payloadData {}
ixNet setMultiAttrs $sg_trafficItem/packetOptions \
 -qosType TOS \
 -destPort 0 \
 -desiredL4ProtocolType None \
 -sourcePort 0 \
 -qosValue "000 Routine"
ixNet setMultiAttrs $sg_trafficItem/frameOptions \
 -frameSizeMode fixed
ixNet setMultiAttrs $sg_trafficItem/rateOptions \
 -packetsPerBurst 100 \
 -packetCountType auto \
 -enforceMinGap 12 \
 -txDelay 0 \
 -lineRate 10 \
 -burstsPerStream 1 \
 -enableInterStreamGap False \
 -packetsPerSecond 100000 \
 -packetGap 64 \
 -enableInterBurstGap False \
 -interStreamGap 64 \
 -interBurstGap 64 \
 -rateMode lineRate \
 -bitRate 100000
ixNet commit
set sg_trafficItem [lindex [ixNet remapIds $sg_trafficItem] 0]
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:5/tracking
#
set sg_tracking $ixNetSG_Stack(1)/tracking
ixNet setMultiAttrs $sg_tracking \
 -enableOverrideValue False \
 -overrideValueList  {  } \
 -selectedTrackBy iTagIsid \
 -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:5/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setMultiAttrs $sg_pair \
 -sources  [list $ixNetSG_ref(2)/protocols ] \
 -trafficGroups  {  } \
 -destinations  [list $ixNetSG_ref(13)/protocols ]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:5/frameOptions/fixed
#
set sg_fixed $ixNetSG_Stack(1)/frameOptions/fixed
ixNet setAttribute $sg_fixed -fixedFrameSize 64
ixNet commit
set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]
return 0
}

ixNetScriptgenProc

