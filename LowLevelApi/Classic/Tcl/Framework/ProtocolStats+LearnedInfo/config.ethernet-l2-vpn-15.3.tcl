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
# object excluded from script (originally /traffic)
# object excluded from script (originally /statistics)
# setting up object 1. (originally /)
set ixNetSG_curObj [ixNet getRoot]
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 1 (originally /).
set ixNetSG_ref(1) $ixNetSG_curObj
# adding children for object 1 (originally /).
set ixNetSG_Stack(0) $ixNetSG_curObj
# setting up object 2. (originally /vport:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(0) vport]
ixNet setAttribute $ixNetSG_curObj -type ethernet
ixNet setAttribute $ixNetSG_curObj -isPullOnly False
ixNet setAttribute $ixNetSG_curObj -name {Ethernet - 001}
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
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -enabled True
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
ixNet setAttribute $ixNetSG_curObj/protocols/ospf -enabled True
ixNet setAttribute $ixNetSG_curObj/protocols/ospf -enableDrOrBdr False
ixNet setAttribute $ixNetSG_curObj/protocols/ospfV3 -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/ping -enabled True
ixNet setAttribute $ixNetSG_curObj/protocols/rip -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/ripng -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/rsvp -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/stp -enabled False
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 2 (originally /vport:1).
# adding children for object 2 (originally /vport:1).
set ixNetSG_Stack(1) $ixNetSG_curObj
# setting up object 3. (originally /vport:1/interface:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $ixNetSG_curObj -description {20.20.20.2/24 - 148:219 - 1}
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -eui64Id {02 00 9A FF FE 49 64 EB }
ixNet setAttribute $ixNetSG_curObj -type default
ixNet setAttribute $ixNetSG_curObj/vlan -tpid {0x8100}
ixNet setAttribute $ixNetSG_curObj/vlan -vlanCount 1
ixNet setAttribute $ixNetSG_curObj/vlan -vlanEnable False
ixNet setAttribute $ixNetSG_curObj/vlan -vlanId {1}
ixNet setAttribute $ixNetSG_curObj/vlan -vlanPriority {5}
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
ixNet setAttribute $ixNetSG_curObj/ethernet -macAddress 00:00:9a:49:64:eb
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
# finished attributes for object 3 (originally /vport:1/interface:1).
set ixNetSG_ref(3) $ixNetSG_curObj
# adding children for object 3 (originally /vport:1/interface:1).
set ixNetSG_Stack(2) $ixNetSG_curObj
# setting up object 4. (originally /vport:1/interface:1/IPv4)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $ixNetSG_curObj -gateway 20.20.20.2
ixNet setAttribute $ixNetSG_curObj -ip 20.20.20.1
ixNet setAttribute $ixNetSG_curObj -maskWidth 24
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 4 (originally /vport:1/interface:1/IPv4).
# adding children for object 4 (originally /vport:1/interface:1/IPv4).
# finished children for object 4 (originally /vport:1/interface:1/IPv4).
# finished children for object 3 (originally /vport:1/interface:1).
# setting up object 5. (originally /vport:1/interface:2)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $ixNetSG_curObj -description {2.2.2.2/32 - 148:219 - 1}
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -eui64Id {02 00 9A FF FE 49 64 EC }
ixNet setAttribute $ixNetSG_curObj -type routed
ixNet setAttribute $ixNetSG_curObj/vlan -tpid {0x8100}
ixNet setAttribute $ixNetSG_curObj/vlan -vlanCount 1
ixNet setAttribute $ixNetSG_curObj/vlan -vlanEnable False
ixNet setAttribute $ixNetSG_curObj/vlan -vlanId {1}
ixNet setAttribute $ixNetSG_curObj/vlan -vlanPriority {5}
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
ixNet setAttribute $ixNetSG_curObj/ethernet -macAddress 00:00:9a:49:64:ec
ixNet setAttribute $ixNetSG_curObj/ethernet -uidFromMac True
ixNet setAttribute $ixNetSG_curObj/gre -dest 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/gre -inKey 0
ixNet setAttribute $ixNetSG_curObj/gre -outKey 0
ixNet setAttribute $ixNetSG_curObj/gre -source [ixNet getNull]
ixNet setAttribute $ixNetSG_curObj/gre -useChecksum False
ixNet setAttribute $ixNetSG_curObj/gre -useKey False
ixNet setAttribute $ixNetSG_curObj/gre -useSequence False
ixNet setAttribute $ixNetSG_curObj/unconnected -connectedVia $ixNetSG_ref(3)
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 5 (originally /vport:1/interface:2).
set ixNetSG_ref(5) $ixNetSG_curObj
# adding children for object 5 (originally /vport:1/interface:2).
set ixNetSG_Stack(2) $ixNetSG_curObj
# setting up object 6. (originally /vport:1/interface:2/IPv4)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $ixNetSG_curObj -gateway 20.20.20.2
ixNet setAttribute $ixNetSG_curObj -ip 2.2.2.2
ixNet setAttribute $ixNetSG_curObj -maskWidth 32
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 6 (originally /vport:1/interface:2/IPv4).
# adding children for object 6 (originally /vport:1/interface:2/IPv4).
# finished children for object 6 (originally /vport:1/interface:2/IPv4).
# finished children for object 5 (originally /vport:1/interface:2).
# setting up object 7. (originally /vport:1/protocols/ldp/router:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1)/protocols/ldp router]
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableFilterFec False
ixNet setAttribute $ixNetSG_curObj -enableGracefulRestart False
ixNet setAttribute $ixNetSG_curObj -enablePduRateControl False
ixNet setAttribute $ixNetSG_curObj -enableVcFecs True
ixNet setAttribute $ixNetSG_curObj -enableVcGroupMatch False
ixNet setAttribute $ixNetSG_curObj -interPduGap 50
ixNet setAttribute $ixNetSG_curObj -reconnectTime 120000
ixNet setAttribute $ixNetSG_curObj -recoveryTime 120000
ixNet setAttribute $ixNetSG_curObj -routerId 148.219.0.1
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 7 (originally /vport:1/protocols/ldp/router:1).
# adding children for object 7 (originally /vport:1/protocols/ldp/router:1).
set ixNetSG_Stack(2) $ixNetSG_curObj
# setting up object 8. (originally /vport:1/protocols/ldp/router:1/advFECRange:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) advFecRange]
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enablePacking False
ixNet setAttribute $ixNetSG_curObj -firstNetwork 2.2.2.2
ixNet setAttribute $ixNetSG_curObj -labelMode none
ixNet setAttribute $ixNetSG_curObj -labelValueStart 3
ixNet setAttribute $ixNetSG_curObj -maskWidth 32
ixNet setAttribute $ixNetSG_curObj -numberOfNetworks 1
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 8 (originally /vport:1/protocols/ldp/router:1/advFECRange:1).
# adding children for object 8 (originally /vport:1/protocols/ldp/router:1/advFECRange:1).
# finished children for object 8 (originally /vport:1/protocols/ldp/router:1/advFECRange:1).
# setting up object 9. (originally /vport:1/protocols/ldp/router:1/interface:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) interface]
# ixNet setAttribute $ixNetSG_curObj -advertisingMode unsolicited
# ixNet setAttribute $ixNetSG_curObj -atmVcDirection bidirectional
ixNet setAttribute $ixNetSG_curObj -authentication null
ixNet setAttribute $ixNetSG_curObj -discoveryMode basic
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableAtmSession False
ixNet setAttribute $ixNetSG_curObj -labelSpaceId 0
ixNet setAttribute $ixNetSG_curObj -md5Key {}
ixNet setAttribute $ixNetSG_curObj -protocolInterface $ixNetSG_ref(3)
ixNet setAttribute $ixNetSG_curObj/learnedFilter -ipv4FecAddress 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -ipv4FecMask 24
ixNet setAttribute $ixNetSG_curObj/learnedFilter -ipv4FecMaskMatch looseMatch
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableFilter False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableIpv4FecAddress False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableIpv4FecMask False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableLabel False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniDescription False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniGroupId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniVcId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniVcType False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enablePeerAddress False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enablePeerMask False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -label 0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniDescription {}
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniGroupId 0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniVcId 0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniVcType frameRelay
ixNet setAttribute $ixNetSG_curObj/learnedFilter -peerAddress 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -peerMask 24
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 9 (originally /vport:1/protocols/ldp/router:1/interface:1).
# adding children for object 9 (originally /vport:1/protocols/ldp/router:1/interface:1).
# finished children for object 9 (originally /vport:1/protocols/ldp/router:1/interface:1).
# finished children for object 7 (originally /vport:1/protocols/ldp/router:1).
# setting up object 10. (originally /vport:1/protocols/ldp/router:2)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1)/protocols/ldp router]
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableFilterFec False
ixNet setAttribute $ixNetSG_curObj -enableGracefulRestart False
ixNet setAttribute $ixNetSG_curObj -enablePduRateControl False
ixNet setAttribute $ixNetSG_curObj -enableVcFecs True
ixNet setAttribute $ixNetSG_curObj -enableVcGroupMatch False
ixNet setAttribute $ixNetSG_curObj -interPduGap 50
ixNet setAttribute $ixNetSG_curObj -reconnectTime 120000
ixNet setAttribute $ixNetSG_curObj -recoveryTime 120000
ixNet setAttribute $ixNetSG_curObj -routerId 2.2.2.2
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 10 (originally /vport:1/protocols/ldp/router:2).
# adding children for object 10 (originally /vport:1/protocols/ldp/router:2).
set ixNetSG_Stack(2) $ixNetSG_curObj
# setting up object 11. (originally /vport:1/protocols/ldp/router:2/interface:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) interface]
ixNet setAttribute $ixNetSG_curObj -advertisingMode unsolicited
# ixNet setAttribute $ixNetSG_curObj -atmVcDirection bidirectional
# ixNet setAttribute $ixNetSG_curObj -authentication null
ixNet setAttribute $ixNetSG_curObj -discoveryMode extendedMartini
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableAtmSession False
ixNet setAttribute $ixNetSG_curObj -labelSpaceId 0
ixNet setAttribute $ixNetSG_curObj -md5Key {}
ixNet setAttribute $ixNetSG_curObj -protocolInterface $ixNetSG_ref(5)
ixNet setAttribute $ixNetSG_curObj/learnedFilter -ipv4FecAddress 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -ipv4FecMask 24
ixNet setAttribute $ixNetSG_curObj/learnedFilter -ipv4FecMaskMatch looseMatch
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableFilter False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableIpv4FecAddress False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableIpv4FecMask False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableLabel False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniDescription False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniGroupId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniVcId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniVcType False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enablePeerAddress False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enablePeerMask False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -label 0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniDescription {}
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniGroupId 0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniVcId 0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniVcType frameRelay
ixNet setAttribute $ixNetSG_curObj/learnedFilter -peerAddress 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -peerMask 24
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 11 (originally /vport:1/protocols/ldp/router:2/interface:1).
# adding children for object 11 (originally /vport:1/protocols/ldp/router:2/interface:1).
set ixNetSG_Stack(3) $ixNetSG_curObj
# setting up object 12. (originally /vport:1/protocols/ldp/router:2/interface:1/targetPeer:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(3) targetPeer]
ixNet setAttribute $ixNetSG_curObj -ipAddress 2.2.2.3
ixNet setAttribute $ixNetSG_curObj -authentication null
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -md5Key {}
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 12 (originally /vport:1/protocols/ldp/router:2/interface:1/targetPeer:1).
# adding children for object 12 (originally /vport:1/protocols/ldp/router:2/interface:1/targetPeer:1).
# finished children for object 12 (originally /vport:1/protocols/ldp/router:2/interface:1/targetPeer:1).
# finished children for object 11 (originally /vport:1/protocols/ldp/router:2/interface:1).
# setting up object 13. (originally /vport:1/protocols/ldp/router:2/l2Interface:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) l2Interface]
ixNet setAttribute $ixNetSG_curObj -count 1
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -groupId 1
ixNet setAttribute $ixNetSG_curObj -type vlan
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 13 (originally /vport:1/protocols/ldp/router:2/l2Interface:1).
# adding children for object 13 (originally /vport:1/protocols/ldp/router:2/l2Interface:1).
set ixNetSG_Stack(3) $ixNetSG_curObj
# setting up object 14. (originally /vport:1/protocols/ldp/router:2/l2Interface:1/l2VCRange:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(3) l2VcRange]
ixNet setAttribute $ixNetSG_curObj -ceIpAddress 1.1.1.1
ixNet setAttribute $ixNetSG_curObj -cemOption 0
ixNet setAttribute $ixNetSG_curObj -cemPayload 48
ixNet setAttribute $ixNetSG_curObj -count 1
ixNet setAttribute $ixNetSG_curObj -description {}
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableCBit False
ixNet setAttribute $ixNetSG_curObj -enableCemOption False
ixNet setAttribute $ixNetSG_curObj -enableCemPayload False
ixNet setAttribute $ixNetSG_curObj -enableDescriptionPresent False
ixNet setAttribute $ixNetSG_curObj -enableMaxAtmPresent False
ixNet setAttribute $ixNetSG_curObj -enableMtuPresent True
ixNet setAttribute $ixNetSG_curObj -enablePacking False
ixNet setAttribute $ixNetSG_curObj -ipType 17
ixNet setAttribute $ixNetSG_curObj -labelMode increment
ixNet setAttribute $ixNetSG_curObj -labelStart 16
ixNet setAttribute $ixNetSG_curObj -maxNumberOfAtmCells 1
ixNet setAttribute $ixNetSG_curObj -peerAddress 2.2.2.3
ixNet setAttribute $ixNetSG_curObj -step 1
ixNet setAttribute $ixNetSG_curObj -vcId 10
ixNet setAttribute $ixNetSG_curObj -vcIdStep 1
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -count 2
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -enabled True
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -enableRepeatMac False
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -enableSameVlan False
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -enableVlan True
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -firstVlanId 100
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -startMac 00:00:00:01:00:00
ixNet setAttribute $ixNetSG_curObj/l2VcIpRange -enabled True
ixNet setAttribute $ixNetSG_curObj/l2VcIpRange -incrementBy 1
ixNet setAttribute $ixNetSG_curObj/l2VcIpRange -mask 24
ixNet setAttribute $ixNetSG_curObj/l2VcIpRange -numHosts 1
ixNet setAttribute $ixNetSG_curObj/l2VcIpRange -startAddress 1.1.1.1
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 14 (originally /vport:1/protocols/ldp/router:2/l2Interface:1/l2VCRange:1).
# adding children for object 14 (originally /vport:1/protocols/ldp/router:2/l2Interface:1/l2VCRange:1).
# finished children for object 14 (originally /vport:1/protocols/ldp/router:2/l2Interface:1/l2VCRange:1).
# finished children for object 13 (originally /vport:1/protocols/ldp/router:2/l2Interface:1).
# finished children for object 10 (originally /vport:1/protocols/ldp/router:2).
# setting up object 15. (originally /vport:1/protocols/ospf/router:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1)/protocols/ospf router]
ixNet setAttribute $ixNetSG_curObj -discardLearnedLsa False
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -generateRouterLsa True
ixNet setAttribute $ixNetSG_curObj -gracefulRestart False
ixNet setAttribute $ixNetSG_curObj -rebuildAdjForLsdbChange False
ixNet setAttribute $ixNetSG_curObj -routerId 148.219.0.1
ixNet setAttribute $ixNetSG_curObj -strictLsaChecking True
ixNet setAttribute $ixNetSG_curObj -supportForRfc3623 False
ixNet setAttribute $ixNetSG_curObj -supportReasonSoftReloadUpgrade True
ixNet setAttribute $ixNetSG_curObj -supportReasonSoftRestart True
ixNet setAttribute $ixNetSG_curObj -supportReasonSwotchRedundantCntrlProcessor True
ixNet setAttribute $ixNetSG_curObj -supportReasonUnknown True
ixNet setAttribute $ixNetSG_curObj -trafficGroupId [ixNet getNull]
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 15 (originally /vport:1/protocols/ospf/router:1).
# adding children for object 15 (originally /vport:1/protocols/ospf/router:1).
set ixNetSG_Stack(2) $ixNetSG_curObj
# setting up object 16. (originally /vport:1/protocols/ospf/router:1/interface:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) interface]
ixNet setAttribute $ixNetSG_curObj -advertiseNetworkRange False
ixNet setAttribute $ixNetSG_curObj -areaId 0
ixNet setAttribute $ixNetSG_curObj -authenticationMethods null
ixNet setAttribute $ixNetSG_curObj -authenticationPassword {}
ixNet setAttribute $ixNetSG_curObj -connectedToDut True
ixNet setAttribute $ixNetSG_curObj -deadInterval 40
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableBfdRegistration False
ixNet setAttribute $ixNetSG_curObj -helloInterval 10
ixNet setAttribute $ixNetSG_curObj -interfaceIpAddress 20.20.20.1
ixNet setAttribute $ixNetSG_curObj -interfaceIpMaskAddress 255.255.255.0
ixNet setAttribute $ixNetSG_curObj -protocolInterface $ixNetSG_ref(3)
ixNet setAttribute $ixNetSG_curObj -linkTypes transit
ixNet setAttribute $ixNetSG_curObj -md5AuthenticationKey {}
ixNet setAttribute $ixNetSG_curObj -md5AuthenticationKeyId 1
ixNet setAttribute $ixNetSG_curObj -metric 10
ixNet setAttribute $ixNetSG_curObj -neighborIpAddress 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -neighborRouterId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -networkRangeIp 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -networkRangeIpByMask False
ixNet setAttribute $ixNetSG_curObj -networkRangeIpIncrementBy 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -networkRangeIpMask 0
ixNet setAttribute $ixNetSG_curObj -networkRangeLinkType broadcast
ixNet setAttribute $ixNetSG_curObj -networkRangeRouterId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -networkRangeRouterIdIncrementBy 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -networkType pointToPoint
ixNet setAttribute $ixNetSG_curObj -noOfCols 0
ixNet setAttribute $ixNetSG_curObj -noOfRows 0
ixNet setAttribute $ixNetSG_curObj -options 2
ixNet setAttribute $ixNetSG_curObj -priority 2
ixNet setAttribute $ixNetSG_curObj -showExternal True
ixNet setAttribute $ixNetSG_curObj -showNssa False
ixNet setAttribute $ixNetSG_curObj -teAdminGroup {00 00 00 00}
ixNet setAttribute $ixNetSG_curObj -teEnable False
ixNet setAttribute $ixNetSG_curObj -teMaxBandwidth 0
ixNet setAttribute $ixNetSG_curObj -teMetricLevel 0
ixNet setAttribute $ixNetSG_curObj -teResMaxBandwidth 0
ixNet setAttribute $ixNetSG_curObj -teUnreservedBwPriority [list 0 0 0 0 0 0 0 0]
ixNet setAttribute $ixNetSG_curObj -validateReceivedMtuSize True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -advRouterId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableAdvRouterId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableFilter False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableLinkStateId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -excludeAdvRouterId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -excludeLinkStateId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -linkStateId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showExternalAsLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showNssaLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showNetworkLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showOpaqueAreaLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showOpaqueDomainLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showOpaqueLocalLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showRouterLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showSummaryAsLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showSummaryIpLsa True
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 16 (originally /vport:1/protocols/ospf/router:1/interface:1).
# adding children for object 16 (originally /vport:1/protocols/ospf/router:1/interface:1).
# finished children for object 16 (originally /vport:1/protocols/ospf/router:1/interface:1).
# setting up object 17. (originally /vport:1/protocols/ospf/router:1/interface:2)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) interface]
ixNet setAttribute $ixNetSG_curObj -advertiseNetworkRange True
ixNet setAttribute $ixNetSG_curObj -areaId 0
ixNet setAttribute $ixNetSG_curObj -authenticationMethods null
ixNet setAttribute $ixNetSG_curObj -authenticationPassword {}
ixNet setAttribute $ixNetSG_curObj -connectedToDut False
ixNet setAttribute $ixNetSG_curObj -deadInterval 40
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableBfdRegistration False
ixNet setAttribute $ixNetSG_curObj -helloInterval 10
ixNet setAttribute $ixNetSG_curObj -interfaceIpAddress 11.1.1.1
ixNet setAttribute $ixNetSG_curObj -interfaceIpMaskAddress 255.255.255.0
ixNet setAttribute $ixNetSG_curObj -protocolInterface [ixNet getNull]
ixNet setAttribute $ixNetSG_curObj -linkTypes transit
ixNet setAttribute $ixNetSG_curObj -md5AuthenticationKey {}
ixNet setAttribute $ixNetSG_curObj -md5AuthenticationKeyId 1
ixNet setAttribute $ixNetSG_curObj -metric 10
ixNet setAttribute $ixNetSG_curObj -mtu 1500
ixNet setAttribute $ixNetSG_curObj -neighborIpAddress 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -neighborRouterId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -networkRangeIp 2.2.2.2
ixNet setAttribute $ixNetSG_curObj -networkRangeIpByMask True
ixNet setAttribute $ixNetSG_curObj -networkRangeIpIncrementBy 0.0.0.1
ixNet setAttribute $ixNetSG_curObj -networkRangeIpMask 32
ixNet setAttribute $ixNetSG_curObj -networkRangeLinkType pointToPoint
ixNet setAttribute $ixNetSG_curObj -networkRangeRouterId 2.2.2.2
ixNet setAttribute $ixNetSG_curObj -networkRangeRouterIdIncrementBy 0.0.0.1
ixNet setAttribute $ixNetSG_curObj -networkType broadcast
ixNet setAttribute $ixNetSG_curObj -noOfCols 1
ixNet setAttribute $ixNetSG_curObj -noOfRows 1
ixNet setAttribute $ixNetSG_curObj -options 2
ixNet setAttribute $ixNetSG_curObj -priority 2
ixNet setAttribute $ixNetSG_curObj -showExternal True
ixNet setAttribute $ixNetSG_curObj -showNssa False
ixNet setAttribute $ixNetSG_curObj -teAdminGroup {00 00 00 00}
ixNet setAttribute $ixNetSG_curObj -teEnable False
ixNet setAttribute $ixNetSG_curObj -teMaxBandwidth 0
ixNet setAttribute $ixNetSG_curObj -teMetricLevel 0
ixNet setAttribute $ixNetSG_curObj -teResMaxBandwidth 0
ixNet setAttribute $ixNetSG_curObj -teUnreservedBwPriority [list 0 0 0 0 0 0 0 0]
ixNet setAttribute $ixNetSG_curObj -validateReceivedMtuSize True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -advRouterId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableAdvRouterId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableFilter False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableLinkStateId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -excludeAdvRouterId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -excludeLinkStateId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -linkStateId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showExternalAsLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showNssaLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showNetworkLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showOpaqueAreaLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showOpaqueDomainLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showOpaqueLocalLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showRouterLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showSummaryAsLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showSummaryIpLsa True
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 17 (originally /vport:1/protocols/ospf/router:1/interface:2).
# adding children for object 17 (originally /vport:1/protocols/ospf/router:1/interface:2).
# finished children for object 17 (originally /vport:1/protocols/ospf/router:1/interface:2).
# finished children for object 15 (originally /vport:1/protocols/ospf/router:1).
# finished children for object 2 (originally /vport:1).
# setting up object 18. (originally /vport:2)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(0) vport]
ixNet setAttribute $ixNetSG_curObj -type ethernet
ixNet setAttribute $ixNetSG_curObj -isPullOnly False
ixNet setAttribute $ixNetSG_curObj -name {Ethernet - 002}
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
ixNet setAttribute $ixNetSG_curObj/protocols/ldp -enabled True
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
ixNet setAttribute $ixNetSG_curObj/protocols/ospf -enabled True
ixNet setAttribute $ixNetSG_curObj/protocols/ospf -enableDrOrBdr False
ixNet setAttribute $ixNetSG_curObj/protocols/ospfV3 -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/pimsm -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/ping -enabled True
ixNet setAttribute $ixNetSG_curObj/protocols/rip -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/ripng -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/rsvp -enabled False
ixNet setAttribute $ixNetSG_curObj/protocols/stp -enabled False
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 18 (originally /vport:2).
# adding children for object 18 (originally /vport:2).
set ixNetSG_Stack(1) $ixNetSG_curObj
# setting up object 19. (originally /vport:2/interface:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $ixNetSG_curObj -description {20.20.21.2/24 - 148:220 - 1}
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -eui64Id {02 00 9A FF FE 4A 65 0A }
ixNet setAttribute $ixNetSG_curObj -type default
ixNet setAttribute $ixNetSG_curObj/vlan -tpid {0x8100}
ixNet setAttribute $ixNetSG_curObj/vlan -vlanCount 1
ixNet setAttribute $ixNetSG_curObj/vlan -vlanEnable False
ixNet setAttribute $ixNetSG_curObj/vlan -vlanId {1}
ixNet setAttribute $ixNetSG_curObj/vlan -vlanPriority {5}
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
ixNet setAttribute $ixNetSG_curObj/ethernet -macAddress 00:00:9a:4a:65:0a
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
# finished attributes for object 19 (originally /vport:2/interface:1).
set ixNetSG_ref(19) $ixNetSG_curObj
# adding children for object 19 (originally /vport:2/interface:1).
set ixNetSG_Stack(2) $ixNetSG_curObj
# setting up object 20. (originally /vport:2/interface:1/IPv4)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $ixNetSG_curObj -gateway 20.20.20.1
ixNet setAttribute $ixNetSG_curObj -ip 20.20.20.2
ixNet setAttribute $ixNetSG_curObj -maskWidth 24
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 20 (originally /vport:2/interface:1/IPv4).
# adding children for object 20 (originally /vport:2/interface:1/IPv4).
# finished children for object 20 (originally /vport:2/interface:1/IPv4).
# finished children for object 19 (originally /vport:2/interface:1).
# setting up object 21. (originally /vport:2/interface:2)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1) interface]
ixNet setAttribute $ixNetSG_curObj -description {2.2.2.3/32 - 148:220 - 1}
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -eui64Id {02 00 9A FF FE 4A 65 0B }
ixNet setAttribute $ixNetSG_curObj -type routed
ixNet setAttribute $ixNetSG_curObj/vlan -tpid {0x8100}
ixNet setAttribute $ixNetSG_curObj/vlan -vlanCount 1
ixNet setAttribute $ixNetSG_curObj/vlan -vlanEnable False
ixNet setAttribute $ixNetSG_curObj/vlan -vlanId {1}
ixNet setAttribute $ixNetSG_curObj/vlan -vlanPriority {5}
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
ixNet setAttribute $ixNetSG_curObj/ethernet -macAddress 00:00:9a:4a:65:0b
ixNet setAttribute $ixNetSG_curObj/ethernet -uidFromMac True
ixNet setAttribute $ixNetSG_curObj/gre -dest 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/gre -inKey 0
ixNet setAttribute $ixNetSG_curObj/gre -outKey 0
ixNet setAttribute $ixNetSG_curObj/gre -source [ixNet getNull]
ixNet setAttribute $ixNetSG_curObj/gre -useChecksum False
ixNet setAttribute $ixNetSG_curObj/gre -useKey False
ixNet setAttribute $ixNetSG_curObj/gre -useSequence False
ixNet setAttribute $ixNetSG_curObj/unconnected -connectedVia $ixNetSG_ref(19)
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 21 (originally /vport:2/interface:2).
set ixNetSG_ref(21) $ixNetSG_curObj
# adding children for object 21 (originally /vport:2/interface:2).
set ixNetSG_Stack(2) $ixNetSG_curObj
# setting up object 22. (originally /vport:2/interface:2/IPv4)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) ipv4]
ixNet setAttribute $ixNetSG_curObj -gateway 20.20.21.2
ixNet setAttribute $ixNetSG_curObj -ip 2.2.2.3
ixNet setAttribute $ixNetSG_curObj -maskWidth 32
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 22 (originally /vport:2/interface:2/IPv4).
# adding children for object 22 (originally /vport:2/interface:2/IPv4).
# finished children for object 22 (originally /vport:2/interface:2/IPv4).
# finished children for object 21 (originally /vport:2/interface:2).
# setting up object 23. (originally /vport:2/protocols/ldp/router:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1)/protocols/ldp router]
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableFilterFec False
ixNet setAttribute $ixNetSG_curObj -enableGracefulRestart False
ixNet setAttribute $ixNetSG_curObj -enablePduRateControl False
ixNet setAttribute $ixNetSG_curObj -enableVcFecs True
ixNet setAttribute $ixNetSG_curObj -enableVcGroupMatch False
ixNet setAttribute $ixNetSG_curObj -interPduGap 50
ixNet setAttribute $ixNetSG_curObj -reconnectTime 120000
ixNet setAttribute $ixNetSG_curObj -recoveryTime 120000
ixNet setAttribute $ixNetSG_curObj -routerId 148.220.0.1
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 23 (originally /vport:2/protocols/ldp/router:1).
# adding children for object 23 (originally /vport:2/protocols/ldp/router:1).
set ixNetSG_Stack(2) $ixNetSG_curObj
# setting up object 24. (originally /vport:2/protocols/ldp/router:1/advFECRange:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) advFecRange]
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enablePacking False
ixNet setAttribute $ixNetSG_curObj -firstNetwork 2.2.2.3
ixNet setAttribute $ixNetSG_curObj -labelMode none
ixNet setAttribute $ixNetSG_curObj -labelValueStart 3
ixNet setAttribute $ixNetSG_curObj -maskWidth 32
ixNet setAttribute $ixNetSG_curObj -numberOfNetworks 1
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 24 (originally /vport:2/protocols/ldp/router:1/advFECRange:1).
# adding children for object 24 (originally /vport:2/protocols/ldp/router:1/advFECRange:1).
# finished children for object 24 (originally /vport:2/protocols/ldp/router:1/advFECRange:1).
# setting up object 25. (originally /vport:2/protocols/ldp/router:1/interface:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) interface]
ixNet setAttribute $ixNetSG_curObj -advertisingMode unsolicited
#ixNet setAttribute $ixNetSG_curObj -atmVcDirection bidirectional
#ixNet setAttribute $ixNetSG_curObj -authentication null
ixNet setAttribute $ixNetSG_curObj -discoveryMode basic
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableAtmSession False
ixNet setAttribute $ixNetSG_curObj -labelSpaceId 0
ixNet setAttribute $ixNetSG_curObj -md5Key {}
ixNet setAttribute $ixNetSG_curObj -protocolInterface $ixNetSG_ref(19)
ixNet setAttribute $ixNetSG_curObj/learnedFilter -ipv4FecAddress 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -ipv4FecMask 24
ixNet setAttribute $ixNetSG_curObj/learnedFilter -ipv4FecMaskMatch looseMatch
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableFilter False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableIpv4FecAddress False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableIpv4FecMask False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableLabel False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniDescription False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniGroupId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniVcId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniVcType False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enablePeerAddress False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enablePeerMask False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -label 0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniDescription {}
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniGroupId 0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniVcId 0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniVcType frameRelay
ixNet setAttribute $ixNetSG_curObj/learnedFilter -peerAddress 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -peerMask 24
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 25 (originally /vport:2/protocols/ldp/router:1/interface:1).
# adding children for object 25 (originally /vport:2/protocols/ldp/router:1/interface:1).
# finished children for object 25 (originally /vport:2/protocols/ldp/router:1/interface:1).
# finished children for object 23 (originally /vport:2/protocols/ldp/router:1).
# setting up object 26. (originally /vport:2/protocols/ldp/router:2)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1)/protocols/ldp router]
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableFilterFec False
ixNet setAttribute $ixNetSG_curObj -enableGracefulRestart False
ixNet setAttribute $ixNetSG_curObj -enablePduRateControl False
ixNet setAttribute $ixNetSG_curObj -enableVcFecs True
ixNet setAttribute $ixNetSG_curObj -enableVcGroupMatch False
ixNet setAttribute $ixNetSG_curObj -interPduGap 50
ixNet setAttribute $ixNetSG_curObj -reconnectTime 120000
ixNet setAttribute $ixNetSG_curObj -recoveryTime 120000
ixNet setAttribute $ixNetSG_curObj -routerId 2.2.2.3
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 26 (originally /vport:2/protocols/ldp/router:2).
# adding children for object 26 (originally /vport:2/protocols/ldp/router:2).
set ixNetSG_Stack(2) $ixNetSG_curObj
# setting up object 27. (originally /vport:2/protocols/ldp/router:2/interface:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) interface]
ixNet setAttribute $ixNetSG_curObj -advertisingMode unsolicited
# ixNet setAttribute $ixNetSG_curObj -atmVcDirection bidirectional
# ixNet setAttribute $ixNetSG_curObj -authentication null
ixNet setAttribute $ixNetSG_curObj -discoveryMode extendedMartini
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableAtmSession False
ixNet setAttribute $ixNetSG_curObj -labelSpaceId 0
ixNet setAttribute $ixNetSG_curObj -md5Key {}
ixNet setAttribute $ixNetSG_curObj -protocolInterface $ixNetSG_ref(21)
ixNet setAttribute $ixNetSG_curObj/learnedFilter -ipv4FecAddress 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -ipv4FecMask 24
ixNet setAttribute $ixNetSG_curObj/learnedFilter -ipv4FecMaskMatch looseMatch
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableFilter False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableIpv4FecAddress False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableIpv4FecMask False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableLabel False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniDescription False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniGroupId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniVcId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableMartiniVcType False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enablePeerAddress False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enablePeerMask False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -label 0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniDescription {}
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniGroupId 0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniVcId 0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -martiniVcType frameRelay
ixNet setAttribute $ixNetSG_curObj/learnedFilter -peerAddress 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -peerMask 24
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 27 (originally /vport:2/protocols/ldp/router:2/interface:1).
# adding children for object 27 (originally /vport:2/protocols/ldp/router:2/interface:1).
set ixNetSG_Stack(3) $ixNetSG_curObj
# setting up object 28. (originally /vport:2/protocols/ldp/router:2/interface:1/targetPeer:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(3) targetPeer]
ixNet setAttribute $ixNetSG_curObj -ipAddress 2.2.2.2
ixNet setAttribute $ixNetSG_curObj -authentication null
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -md5Key {}
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 28 (originally /vport:2/protocols/ldp/router:2/interface:1/targetPeer:1).
# adding children for object 28 (originally /vport:2/protocols/ldp/router:2/interface:1/targetPeer:1).
# finished children for object 28 (originally /vport:2/protocols/ldp/router:2/interface:1/targetPeer:1).
# finished children for object 27 (originally /vport:2/protocols/ldp/router:2/interface:1).
# setting up object 29. (originally /vport:2/protocols/ldp/router:2/l2Interface:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) l2Interface]
ixNet setAttribute $ixNetSG_curObj -count 1
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -groupId 1
ixNet setAttribute $ixNetSG_curObj -type vlan
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 29 (originally /vport:2/protocols/ldp/router:2/l2Interface:1).
# adding children for object 29 (originally /vport:2/protocols/ldp/router:2/l2Interface:1).
set ixNetSG_Stack(3) $ixNetSG_curObj
# setting up object 30. (originally /vport:2/protocols/ldp/router:2/l2Interface:1/l2VCRange:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(3) l2VcRange]
ixNet setAttribute $ixNetSG_curObj -ceIpAddress 1.1.1.1
ixNet setAttribute $ixNetSG_curObj -cemOption 0
ixNet setAttribute $ixNetSG_curObj -cemPayload 48
ixNet setAttribute $ixNetSG_curObj -count 1
ixNet setAttribute $ixNetSG_curObj -description {}
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableCBit False
ixNet setAttribute $ixNetSG_curObj -enableCemOption False
ixNet setAttribute $ixNetSG_curObj -enableCemPayload False
ixNet setAttribute $ixNetSG_curObj -enableDescriptionPresent False
ixNet setAttribute $ixNetSG_curObj -enableMaxAtmPresent False
ixNet setAttribute $ixNetSG_curObj -enableMtuPresent True
ixNet setAttribute $ixNetSG_curObj -enablePacking False
ixNet setAttribute $ixNetSG_curObj -ipType 17
ixNet setAttribute $ixNetSG_curObj -labelMode increment
ixNet setAttribute $ixNetSG_curObj -labelStart 16
ixNet setAttribute $ixNetSG_curObj -maxNumberOfAtmCells 1
ixNet setAttribute $ixNetSG_curObj -mtu 1500
ixNet setAttribute $ixNetSG_curObj -peerAddress 2.2.2.2
ixNet setAttribute $ixNetSG_curObj -step 1
ixNet setAttribute $ixNetSG_curObj -vcId 10
ixNet setAttribute $ixNetSG_curObj -vcIdStep 1
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -count 2
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -enabled True
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -enableRepeatMac False
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -enableSameVlan False
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -enableVlan True
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -firstVlanId 100
ixNet setAttribute $ixNetSG_curObj/l2MacVlanRange -startMac 00:00:00:01:00:02
ixNet setAttribute $ixNetSG_curObj/l2VcIpRange -enabled True
ixNet setAttribute $ixNetSG_curObj/l2VcIpRange -incrementBy 1
ixNet setAttribute $ixNetSG_curObj/l2VcIpRange -mask 24
ixNet setAttribute $ixNetSG_curObj/l2VcIpRange -numHosts 1
ixNet setAttribute $ixNetSG_curObj/l2VcIpRange -startAddress 1.1.1.1
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 30 (originally /vport:2/protocols/ldp/router:2/l2Interface:1/l2VCRange:1).
# adding children for object 30 (originally /vport:2/protocols/ldp/router:2/l2Interface:1/l2VCRange:1).
# finished children for object 30 (originally /vport:2/protocols/ldp/router:2/l2Interface:1/l2VCRange:1).
# finished children for object 29 (originally /vport:2/protocols/ldp/router:2/l2Interface:1).
# finished children for object 26 (originally /vport:2/protocols/ldp/router:2).
# setting up object 31. (originally /vport:2/protocols/ospf/router:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(1)/protocols/ospf router]
ixNet setAttribute $ixNetSG_curObj -discardLearnedLsa False
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -generateRouterLsa True
ixNet setAttribute $ixNetSG_curObj -gracefulRestart False
ixNet setAttribute $ixNetSG_curObj -rebuildAdjForLsdbChange False
ixNet setAttribute $ixNetSG_curObj -routerId 148.220.0.1
ixNet setAttribute $ixNetSG_curObj -strictLsaChecking True
ixNet setAttribute $ixNetSG_curObj -supportForRfc3623 False
ixNet setAttribute $ixNetSG_curObj -supportReasonSoftReloadUpgrade True
ixNet setAttribute $ixNetSG_curObj -supportReasonSoftRestart True
ixNet setAttribute $ixNetSG_curObj -supportReasonSwotchRedundantCntrlProcessor True
ixNet setAttribute $ixNetSG_curObj -supportReasonUnknown True
ixNet setAttribute $ixNetSG_curObj -trafficGroupId [ixNet getNull]
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 31 (originally /vport:2/protocols/ospf/router:1).
# adding children for object 31 (originally /vport:2/protocols/ospf/router:1).
set ixNetSG_Stack(2) $ixNetSG_curObj
# setting up object 32. (originally /vport:2/protocols/ospf/router:1/interface:1)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) interface]
ixNet setAttribute $ixNetSG_curObj -advertiseNetworkRange False
ixNet setAttribute $ixNetSG_curObj -areaId 0
ixNet setAttribute $ixNetSG_curObj -authenticationMethods null
ixNet setAttribute $ixNetSG_curObj -authenticationPassword {}
ixNet setAttribute $ixNetSG_curObj -connectedToDut True
ixNet setAttribute $ixNetSG_curObj -deadInterval 40
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableBfdRegistration False
ixNet setAttribute $ixNetSG_curObj -helloInterval 10
ixNet setAttribute $ixNetSG_curObj -interfaceIpAddress 20.20.20.2
ixNet setAttribute $ixNetSG_curObj -interfaceIpMaskAddress 255.255.255.0
ixNet setAttribute $ixNetSG_curObj -protocolInterface $ixNetSG_ref(19)
ixNet setAttribute $ixNetSG_curObj -linkTypes transit
ixNet setAttribute $ixNetSG_curObj -md5AuthenticationKey {}
ixNet setAttribute $ixNetSG_curObj -md5AuthenticationKeyId 1
ixNet setAttribute $ixNetSG_curObj -metric 10
ixNet setAttribute $ixNetSG_curObj -mtu 1500
ixNet setAttribute $ixNetSG_curObj -neighborIpAddress 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -neighborRouterId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -networkRangeIp 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -networkRangeIpByMask False
ixNet setAttribute $ixNetSG_curObj -networkRangeIpIncrementBy 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -networkRangeIpMask 0
ixNet setAttribute $ixNetSG_curObj -networkRangeLinkType broadcast
ixNet setAttribute $ixNetSG_curObj -networkRangeRouterId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -networkRangeRouterIdIncrementBy 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -networkType pointToPoint
ixNet setAttribute $ixNetSG_curObj -noOfCols 0
ixNet setAttribute $ixNetSG_curObj -noOfRows 0
ixNet setAttribute $ixNetSG_curObj -options 2
ixNet setAttribute $ixNetSG_curObj -priority 2
ixNet setAttribute $ixNetSG_curObj -showExternal True
ixNet setAttribute $ixNetSG_curObj -showNssa False
ixNet setAttribute $ixNetSG_curObj -teAdminGroup {00 00 00 00}
ixNet setAttribute $ixNetSG_curObj -teEnable False
ixNet setAttribute $ixNetSG_curObj -teMaxBandwidth 0
ixNet setAttribute $ixNetSG_curObj -teMetricLevel 0
ixNet setAttribute $ixNetSG_curObj -teResMaxBandwidth 0
ixNet setAttribute $ixNetSG_curObj -teUnreservedBwPriority [list 0 0 0 0 0 0 0 0]
ixNet setAttribute $ixNetSG_curObj -validateReceivedMtuSize True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -advRouterId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableAdvRouterId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableFilter False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableLinkStateId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -excludeAdvRouterId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -excludeLinkStateId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -linkStateId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showExternalAsLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showNssaLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showNetworkLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showOpaqueAreaLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showOpaqueDomainLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showOpaqueLocalLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showRouterLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showSummaryAsLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showSummaryIpLsa True
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 32 (originally /vport:2/protocols/ospf/router:1/interface:1).
# adding children for object 32 (originally /vport:2/protocols/ospf/router:1/interface:1).
# finished children for object 32 (originally /vport:2/protocols/ospf/router:1/interface:1).
# setting up object 33. (originally /vport:2/protocols/ospf/router:1/interface:2)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(2) interface]
ixNet setAttribute $ixNetSG_curObj -advertiseNetworkRange True
ixNet setAttribute $ixNetSG_curObj -areaId 0
ixNet setAttribute $ixNetSG_curObj -authenticationMethods null
ixNet setAttribute $ixNetSG_curObj -authenticationPassword {}
ixNet setAttribute $ixNetSG_curObj -connectedToDut False
ixNet setAttribute $ixNetSG_curObj -deadInterval 40
ixNet setAttribute $ixNetSG_curObj -enabled True
ixNet setAttribute $ixNetSG_curObj -enableBfdRegistration False
ixNet setAttribute $ixNetSG_curObj -helloInterval 10
ixNet setAttribute $ixNetSG_curObj -interfaceIpAddress 11.1.2.1
ixNet setAttribute $ixNetSG_curObj -interfaceIpMaskAddress 255.255.255.0
ixNet setAttribute $ixNetSG_curObj -protocolInterface [ixNet getNull]
ixNet setAttribute $ixNetSG_curObj -linkTypes transit
ixNet setAttribute $ixNetSG_curObj -md5AuthenticationKey {}
ixNet setAttribute $ixNetSG_curObj -md5AuthenticationKeyId 1
ixNet setAttribute $ixNetSG_curObj -metric 10
ixNet setAttribute $ixNetSG_curObj -mtu 1500
ixNet setAttribute $ixNetSG_curObj -neighborIpAddress 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -neighborRouterId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj -networkRangeIp 2.2.2.3
ixNet setAttribute $ixNetSG_curObj -networkRangeIpByMask True
ixNet setAttribute $ixNetSG_curObj -networkRangeIpIncrementBy 0.0.0.1
ixNet setAttribute $ixNetSG_curObj -networkRangeIpMask 32
ixNet setAttribute $ixNetSG_curObj -networkRangeLinkType pointToPoint
ixNet setAttribute $ixNetSG_curObj -networkRangeRouterId 2.2.2.3
ixNet setAttribute $ixNetSG_curObj -networkRangeRouterIdIncrementBy 0.0.0.1
ixNet setAttribute $ixNetSG_curObj -networkType broadcast
ixNet setAttribute $ixNetSG_curObj -noOfCols 1
ixNet setAttribute $ixNetSG_curObj -noOfRows 1
ixNet setAttribute $ixNetSG_curObj -options 2
ixNet setAttribute $ixNetSG_curObj -priority 2
ixNet setAttribute $ixNetSG_curObj -showExternal True
ixNet setAttribute $ixNetSG_curObj -showNssa False
ixNet setAttribute $ixNetSG_curObj -teAdminGroup {00 00 00 00}
ixNet setAttribute $ixNetSG_curObj -teEnable False
ixNet setAttribute $ixNetSG_curObj -teMaxBandwidth 0
ixNet setAttribute $ixNetSG_curObj -teMetricLevel 0
ixNet setAttribute $ixNetSG_curObj -teResMaxBandwidth 0
ixNet setAttribute $ixNetSG_curObj -teUnreservedBwPriority [list 0 0 0 0 0 0 0 0]
ixNet setAttribute $ixNetSG_curObj -validateReceivedMtuSize True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -advRouterId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableAdvRouterId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableFilter False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -enableLinkStateId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -excludeAdvRouterId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -excludeLinkStateId False
ixNet setAttribute $ixNetSG_curObj/learnedFilter -linkStateId 0.0.0.0
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showExternalAsLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showNssaLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showNetworkLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showOpaqueAreaLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showOpaqueDomainLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showOpaqueLocalLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showRouterLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showSummaryAsLsa True
ixNet setAttribute $ixNetSG_curObj/learnedFilter -showSummaryIpLsa True
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 33 (originally /vport:2/protocols/ospf/router:1/interface:2).
# adding children for object 33 (originally /vport:2/protocols/ospf/router:1/interface:2).
# finished children for object 33 (originally /vport:2/protocols/ospf/router:1/interface:2).
# finished children for object 31 (originally /vport:2/protocols/ospf/router:1).
# finished children for object 18 (originally /vport:2).
# setting up object 34. (originally /availableHardware/chassis:"Pansy-400t")
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 34 (originally /availableHardware/chassis:"Pansy-400t").
# adding children for object 34 (originally /availableHardware/chassis:"Pansy-400t").
# finished children for object 34 (originally /availableHardware/chassis:"Pansy-400t").
# setting up object 35. (originally /trafficGroupId/item:1)
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 35 (originally /trafficGroupId/item:1).
# adding children for object 35 (originally /trafficGroupId/item:1).
# finished children for object 35 (originally /trafficGroupId/item:1).
# setting up object 36. (originally /trafficGroupId/item:2)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(0)/traffic trafficGroup]
ixNet setAttribute $ixNetSG_curObj -name {L2VPN - 1 - 1}
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 36 (originally /trafficGroupId/item:2).
# adding children for object 36 (originally /trafficGroupId/item:2).
# finished children for object 36 (originally /trafficGroupId/item:2).
# setting up object 37. (originally /trafficGroupId/item:3)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(0)/traffic trafficGroup]
ixNet setAttribute $ixNetSG_curObj -name {L2VPN - 2 - 0}
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 37 (originally /trafficGroupId/item:3).
# adding children for object 37 (originally /trafficGroupId/item:3).
# finished children for object 37 (originally /trafficGroupId/item:3).
# setting up object 38. (originally /trafficGroupId/item:4)
set ixNetSG_curObj [ixNet add $ixNetSG_Stack(0)/traffic trafficGroup]
ixNet setAttribute $ixNetSG_curObj -name {L2VPN - 2 - 1}
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 38 (originally /trafficGroupId/item:4).
# adding children for object 38 (originally /trafficGroupId/item:4).
# finished children for object 38 (originally /trafficGroupId/item:4).
# setting up object 39. (originally /testConfiguration/optionalPage1:"Protocols")
ixNet commit
set ixNetSG_curObj [lindex [ixNet remapIds $ixNetSG_curObj] 0]
# finished attributes for object 39 (originally /testConfiguration/optionalPage1:"Protocols").
# adding children for object 39 (originally /testConfiguration/optionalPage1:"Protocols").
# finished children for object 39 (originally /testConfiguration/optionalPage1:"Protocols").
# setting up object 40. (originally /testConfiguration/optionalPage2:"Traffic")
ixNet commit
# finished attributes for object 40 (originally /testConfiguration/optionalPage2:"Traffic").
# adding children for object 40 (originally /testConfiguration/optionalPage2:"Traffic").
# finished children for object 40 (originally /testConfiguration/optionalPage2:"Traffic").
# finished children for object 1 (originally /).
return 0
}
#if {[catch {ixNetScriptgenProc} result_ixNetScriptgenProc]} { puts $::errorInfo }
ixNetScriptgenProc
