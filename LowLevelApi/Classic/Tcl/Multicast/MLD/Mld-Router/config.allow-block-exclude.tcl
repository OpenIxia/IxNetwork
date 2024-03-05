################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

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
    ixNet setAttribute $sg_vport/protocols/mld -enabled True
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
    ixNet setAttribute $sg_vport/protocols/ping -enabled False
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
    ixNet setAttribute $sg_interface -eui64Id {02 00 01 FF FE 0C 99 E6 }
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
    ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:01:0c:99:e6"
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
    # configuring the object that corresponds to /vport:1/interface:1/ipv6:1
    #
    set sg_ipv6 [ixNet add $ixNetSG_Stack(2) ipv6]
    ixNet setAttribute $sg_ipv6 -ip 4001:0:0:0:0:0:0:1
    ixNet setAttribute $sg_ipv6 -prefixLength 64
    ixNet commit
    set sg_ipv6 [lindex [ixNet remapIds $sg_ipv6] 0]

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
    # configuring the object that corresponds to /vport:1/protocols/mld/querier:2
    #
    set sg_querier [ixNet add $ixNetSG_Stack(1)/protocols/mld querier]
    ixNet setAttribute $sg_querier -discardLearnedInfo False
    ixNet setAttribute $sg_querier -enabled True
    ixNet setAttribute $sg_querier -generalQueryInterval 125
    ixNet setAttribute $sg_querier -gqResponseInterval 10000
    ixNet setAttribute $sg_querier -interfaceId $ixNetSG_ref(3)
    ixNet setAttribute $sg_querier -robustnessVariable 1
    ixNet setAttribute $sg_querier -routerAlert True
    ixNet setAttribute $sg_querier -sqResponseInterval 5000
    ixNet setAttribute $sg_querier -sqTransmissionCount 4
    ixNet setAttribute $sg_querier -startupQueryCount 1
    ixNet setAttribute $sg_querier -supportElection True
    ixNet setAttribute $sg_querier -supportOlderVersionHost True
    ixNet setAttribute $sg_querier -supportOlderVersionQuerier True
    ixNet setAttribute $sg_querier -version version2
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
    ixNet setAttribute $sg_vport/protocols/mld -enabled True
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
    ixNet setAttribute $sg_vport/protocols/ping -enabled False
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
    ixNet setAttribute $sg_interface -eui64Id {02 00 01 FF FE 0C 99 E7 }
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
    ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:01:0c:99:e7"
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
    # configuring the object that corresponds to /vport:2/interface:1/ipv6:1
    #
    set sg_ipv6 [ixNet add $ixNetSG_Stack(2) ipv6]
    ixNet setAttribute $sg_ipv6 -ip 4001:0:0:0:0:0:0:2
    ixNet setAttribute $sg_ipv6 -prefixLength 64
    ixNet commit
    set sg_ipv6 [lindex [ixNet remapIds $sg_ipv6] 0]

    #
    # configuring the object that corresponds to /vport:2/interface:2
    #
    set sg_interface [ixNet add $ixNetSG_Stack(1) interface]
    ixNet setAttribute $sg_interface -description {Connected - ProtocolInterface - 100:02 - 7}
    ixNet setAttribute $sg_interface -enabled True
    ixNet setAttribute $sg_interface -eui64Id {02 00 00 FF FE 0F C6 F6 }
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
    ixNet setAttribute $sg_interface/ethernet -macAddress "00:00:00:0f:c6:f6"
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
    # configuring the object that corresponds to /vport:2/interface:2/ipv6:1
    #
    set sg_ipv6 [ixNet add $ixNetSG_Stack(2) ipv6]
    ixNet setAttribute $sg_ipv6 -ip 4001:0:0:0:0:0:0:3
    ixNet setAttribute $sg_ipv6 -prefixLength 64
    ixNet commit
    set sg_ipv6 [lindex [ixNet remapIds $sg_ipv6] 0]

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
    # configuring the object that corresponds to /vport:2/protocols/mld/host:2
    #
    set sg_host [ixNet add $ixNetSG_Stack(1)/protocols/mld host]
    ixNet setAttribute $sg_host -enableImmediateResp True
    ixNet setAttribute $sg_host -enableQueryResMode True
    ixNet setAttribute $sg_host -enableRouterAlert True
    ixNet setAttribute $sg_host -enableSpecificResMode True
    ixNet setAttribute $sg_host -enableSuppressReport False
    ixNet setAttribute $sg_host -enableUnsolicitedResMode False
    ixNet setAttribute $sg_host -enabled True
    ixNet setAttribute $sg_host -protocolInterface $ixNetSG_ref(9)
    ixNet setAttribute $sg_host -reportFreq 120
    ixNet setAttribute $sg_host -trafficGroupId [ixNet getNull]
    ixNet setAttribute $sg_host -version version2
    ixNet commit
    set sg_host [lindex [ixNet remapIds $sg_host] 0]
    set ixNetSG_Stack(2) $sg_host

    #
    # configuring the object that corresponds to /vport:2/protocols/mld/host:2/groupRange:1
    #
    set sg_groupRange [ixNet add $ixNetSG_Stack(2) groupRange]
    ixNet setAttribute $sg_groupRange -enablePacking False
    ixNet setAttribute $sg_groupRange -enableUpdateRequired False
    ixNet setAttribute $sg_groupRange -enabled True
    ixNet setAttribute $sg_groupRange -groupCount 1
    ixNet setAttribute $sg_groupRange -groupIpFrom FF03:0:0:0:0:0:0:14
    ixNet setAttribute $sg_groupRange -incrementStep 1
    ixNet setAttribute $sg_groupRange -recordsPerFrame 0
    ixNet setAttribute $sg_groupRange -sourceMode exclude
    ixNet setAttribute $sg_groupRange -sourcesPerRecord 0
    ixNet commit
    set sg_groupRange [lindex [ixNet remapIds $sg_groupRange] 0]
    set ixNetSG_Stack(3) $sg_groupRange

    #
    # configuring the object that corresponds to /vport:2/protocols/mld/host:2/groupRange:1/sourceRange:2
    #
    set sg_sourceRange [ixNet add $ixNetSG_Stack(3) sourceRange]
    ixNet setAttribute $sg_sourceRange -count 1
    ixNet setAttribute $sg_sourceRange -ipFrom 2001:0:0:0:0:0:0:1
    ixNet commit
    set sg_sourceRange [lindex [ixNet remapIds $sg_sourceRange] 0]

    #
    # configuring the object that corresponds to /vport:2/protocols/mld/host:2/groupRange:1/sourceRange:3
    #
    set sg_sourceRange [ixNet add $ixNetSG_Stack(3) sourceRange]
    ixNet setAttribute $sg_sourceRange -count 1
    ixNet setAttribute $sg_sourceRange -ipFrom 2001:0:0:0:0:0:0:2
    ixNet commit
    set sg_sourceRange [lindex [ixNet remapIds $sg_sourceRange] 0]

    #
    # configuring the object that corresponds to /vport:2/protocols/mld/host:2/groupRange:1/sourceRange:4
    #
    set sg_sourceRange [ixNet add $ixNetSG_Stack(3) sourceRange]
    ixNet setAttribute $sg_sourceRange -count 1
    ixNet setAttribute $sg_sourceRange -ipFrom 2001:0:0:0:0:0:0:3
    ixNet commit
    set sg_sourceRange [lindex [ixNet remapIds $sg_sourceRange] 0]

    #
    # configuring the object that corresponds to /vport:2/protocols/mld/host:2/groupRange:1/sourceRange:9
    #
    set sg_sourceRange [ixNet add $ixNetSG_Stack(3) sourceRange]
    ixNet setAttribute $sg_sourceRange -count 1
    ixNet setAttribute $sg_sourceRange -ipFrom 2001:0:0:0:0:0:0:4
    ixNet commit
    set sg_sourceRange [lindex [ixNet remapIds $sg_sourceRange] 0]

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