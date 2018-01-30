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
ixNet setAttribute $sg_vport -name {Ethernet - 01}
ixNet setAttribute $sg_vport -txMode sequential
ixNet setAttribute $sg_vport -txGapControlMode fixedMode
ixNet setAttribute $sg_vport -connectedTo [ixNet getNull]
ixNet setAttribute $sg_vport -rxMode measure
ixNet setAttribute $sg_vport/l1Config -currentType ethernet
ixNet setAttribute $sg_vport/capture -hardwareEnabled False
ixNet setAttribute $sg_vport/capture -softwareEnabled False
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
# configuring the object that corresponds to /vport:1/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {ProtocolInterface - 100:01 - 1}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 01 FF FE 31 5D 76 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress 00:00:01:31:5d:76
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
set sg_ethernet [ixNet add $ixNetSG_Stack(1)/l1Config ethernet]
ixNet setAttribute $sg_ethernet -autoNegotiate True
ixNet setAttribute $sg_ethernet -loopback False
ixNet setAttribute $sg_ethernet -speed speed100fd
ixNet setAttribute $sg_ethernet -media copper
ixNet commit
set sg_ethernet [lindex [ixNet remapIds $sg_ethernet] 0]

#
# configuring the object that corresponds to /vport:1/protocols/static/lan:1
#
set sg_lan [ixNet add $ixNetSG_Stack(1)/protocols/static lan]
ixNet setAttribute $sg_lan -count 1
ixNet setAttribute $sg_lan -enableIncrementMac True
ixNet setAttribute $sg_lan -enableIncrementVlan False
ixNet setAttribute $sg_lan -enableSiteId False
ixNet setAttribute $sg_lan -enableVlan False
ixNet setAttribute $sg_lan -enabled True
ixNet setAttribute $sg_lan -mac 00:00:00:00:00:01
ixNet setAttribute $sg_lan -siteId 0
ixNet setAttribute $sg_lan -trafficGroupId [ixNet getNull]
ixNet setAttribute $sg_lan -vlanId 1
ixNet commit
set sg_lan [lindex [ixNet remapIds $sg_lan] 0]

#
# configuring the object that corresponds to /vport:2
#
set sg_vport [ixNet add $ixNetSG_Stack(0) vport]
ixNet setAttribute $sg_vport -type ethernet
ixNet setAttribute $sg_vport -isPullOnly False
ixNet setAttribute $sg_vport -name {Ethernet - 02}
ixNet setAttribute $sg_vport -txMode sequential
ixNet setAttribute $sg_vport -txGapControlMode fixedMode
ixNet setAttribute $sg_vport -connectedTo [ixNet getNull]
ixNet setAttribute $sg_vport -rxMode measure
ixNet setAttribute $sg_vport/l1Config -currentType ethernet
ixNet setAttribute $sg_vport/capture -hardwareEnabled False
ixNet setAttribute $sg_vport/capture -softwareEnabled False
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
set ixNetSG_ref(7) $sg_vport
set ixNetSG_Stack(1) $sg_vport

#
# configuring the object that corresponds to /vport:2/interface:1
#
set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $sg_interface -description {ProtocolInterface - 100:02 - 2}
ixNet setAttribute $sg_interface -enabled True
ixNet setAttribute $sg_interface -eui64Id {02 00 01 FF FE 31 5D 77 }
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
ixNet setAttribute $sg_interface/ethernet -macAddress 00:00:01:31:5d:77
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
set sg_ethernet [ixNet add $ixNetSG_Stack(1)/l1Config ethernet]
ixNet setAttribute $sg_ethernet -autoNegotiate True
ixNet setAttribute $sg_ethernet -loopback False
ixNet setAttribute $sg_ethernet -speed speed100fd
ixNet setAttribute $sg_ethernet -media copper
ixNet commit
set sg_ethernet [lindex [ixNet remapIds $sg_ethernet] 0]

#
# configuring the object that corresponds to /vport:2/protocols/static/lan:1
#
set sg_lan [ixNet add $ixNetSG_Stack(1)/protocols/static lan]
ixNet setAttribute $sg_lan -count 1
ixNet setAttribute $sg_lan -enableIncrementMac True
ixNet setAttribute $sg_lan -enableIncrementVlan False
ixNet setAttribute $sg_lan -enableSiteId False
ixNet setAttribute $sg_lan -enableVlan False
ixNet setAttribute $sg_lan -enabled True
ixNet setAttribute $sg_lan -mac 00:00:00:00:00:02
ixNet setAttribute $sg_lan -siteId 0
ixNet setAttribute $sg_lan -trafficGroupId [ixNet getNull]
ixNet setAttribute $sg_lan -vlanId 1
ixNet commit
set sg_lan [lindex [ixNet remapIds $sg_lan] 0]

###
### /availableHardware area
###

#
# configuring the object that corresponds to /availableHardware/chassis:"munish-400t"
#
#set sg_chassis [ixNet add $ixNetSG_Stack(0)/availableHardware chassis]
#ixNet setAttribute $sg_chassis -hostname {munish-400t}
#ixNet setAttribute $sg_chassis -masterChassis {}
#ixNet setAttribute $sg_chassis -cableLength 0
#ixNet commit
#set sg_chassis [lindex [ixNet remapIds $sg_chassis] 0]
#set ixNetSG_ref(12) $sg_chassis
#ixNet setAttribute $ixNetSG_ref(2) -connectedTo $ixNetSG_ref(12)/card:1/port:3
#ixNet setAttribute $ixNetSG_ref(7) -connectedTo $ixNetSG_ref(12)/card:1/port:4
#ixNet commit

###
### /traffic area
###

#
# configuring the object that corresponds to /traffic/trafficItem:2
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
ixNet setAttribute $sg_trafficItem -endpointType ethernetVlan
ixNet setAttribute $sg_trafficItem -routeMesh fullMesh
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
set ixNetSG_ref(13) $sg_trafficItem
set ixNetSG_Stack(1) $sg_trafficItem

#
# configuring the object that corresponds to /traffic/trafficItem:2/pair:1
#
set sg_pair [ixNet add $ixNetSG_Stack(1) pair]
ixNet setAttribute $sg_pair -sources [list $ixNetSG_ref(2)/protocols]
ixNet setAttribute $sg_pair -destinations [list $ixNetSG_ref(7)/protocols]
ixNet commit
set sg_pair [lindex [ixNet remapIds $sg_pair] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:2/tracking
#
set sg_tracking [ixNet add $ixNetSG_Stack(1) tracking]
ixNet setAttribute $sg_tracking -enableOverrideValue False
ixNet setAttribute $sg_tracking -selectedTrackBy srcMac
ixNet setAttribute $sg_tracking -overrideValueList [list ]
ixNet setAttribute $sg_tracking -customOffset 64
ixNet commit
set sg_tracking [lindex [ixNet remapIds $sg_tracking] 0]

#
# configuring the object that corresponds to /traffic/trafficItem:2/frameOptions
#
set sg_frameOptions [ixNet add $ixNetSG_Stack(1) frameOptions]
ixNet setAttribute $sg_frameOptions -frameSizeMode fixed
ixNet commit
set sg_frameOptions [lindex [ixNet remapIds $sg_frameOptions] 0]
set ixNetSG_Stack(2) $sg_frameOptions

#
# configuring the object that corresponds to /traffic/trafficItem:2/frameOptions/fixed
#

#This has to be verified.... ###########################
#set sg_fixed [ixNet add $ixNetSG_Stack(2) fixed]
#ixNet setAttribute $sg_fixed -fixedFrameSize 64
#ixNet commit
#set sg_fixed [lindex [ixNet remapIds $sg_fixed] 0]

###
### /testConfiguration area
###

#
# configuring the object that corresponds to /testConfiguration/custom:1
#
set sg_custom [ixNet add $ixNetSG_Stack(0)/testConfiguration custom]
ixNet setAttribute $sg_custom -selectedTest fixedDuration
ixNet commit
set sg_custom [lindex [ixNet remapIds $sg_custom] 0]
set ixNetSG_Stack(1) $sg_custom

#
# configuring the object that corresponds to /testConfiguration/custom:1/fixedDuration:1
#
set sg_fixedDuration [ixNet add $ixNetSG_Stack(1) fixedDuration]
ixNet setAttribute $sg_fixedDuration -selectedItems [list $ixNetSG_ref(13)]
ixNet setAttribute $sg_fixedDuration/testSetup -selectedVariableParameter mbitPerSec
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -algorithm fixed
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -backoff 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -value 10
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -stepValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -minValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -valueList [list ]
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -maxValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -initialValue 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -resolution 0
ixNet setAttribute $sg_fixedDuration/testSetup/variableLoop -acceptableFrameLoss 0
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -algorithm random
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -step 0
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -valueList [list ]
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -count 2
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -selectedAdditionalLoopParameter frameSize
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -maxValue 1200
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -value 0
ixNet setAttribute $sg_fixedDuration/testSetup/additionalLoop -initialValue 64
ixNet setAttribute $sg_fixedDuration/protocols -startBehavior startWithCurrent
ixNet setAttribute $sg_fixedDuration/protocols -waitAfterStart 0
ixNet setAttribute $sg_fixedDuration/protocols -waitAfterStop 0
ixNet setAttribute $sg_fixedDuration/traffic -learningFrequency oncePerTest
ixNet setAttribute $sg_fixedDuration/traffic -l2FrameSize 120
ixNet setAttribute $sg_fixedDuration/traffic -delayAfterTransmit 5
ixNet setAttribute $sg_fixedDuration/traffic -l3RepeatCount 3
ixNet setAttribute $sg_fixedDuration/traffic -learningStartDelay 0
ixNet setAttribute $sg_fixedDuration/traffic -l2FrameSizeType fixed
ixNet setAttribute $sg_fixedDuration/traffic -trafficStartDelay 5
ixNet setAttribute $sg_fixedDuration/traffic -generateStreams True
ixNet setAttribute $sg_fixedDuration/traffic -enableLearning True
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
