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

#################################################################################
#                                                                               #
# Description:                                                                  #
#    This script intends to demonstrate how to use NGPF RSVPTE P2MP API         #
#    About Topology:                                                            #
#       Within topology both Sender and Receiver PEs are configured, each behind# 
#    Ingress and Egress P routers respectively. P2MP tunnels used in topology is# 
#	 RSVPTE-P2MP. Both I-PMSI and S-PMSI tunnels for IPv4 & Ipv6 multicast      #
#    streams are configured using RSVPTE-P2MP. Multicast traffic soruce address #
#    are distributed by BGP as UMH routes(AFI:1,SAFI:129). Multicast L2-L3      #
#    Traffic from Seder to Receiver                                             #
# Script Flow:                                                                  #
#        Step 1. Configuration of protocols.                                    #
#    Configuration flow of the script is as follow:                             #
#         i.      Adding of OSPF router                                         #
#         ii.     Adding of Network Topology(NT)                                #
#         iii.    Enabling of TE(Traffic Engineering) and configuring loopback  #
#                         address as Router ID                                  #
#         iv.     Adding of chain DG for behind both Sender/Receiver PE Router  #
#         v.      Adding of RSVP-TE LSPs(both P2P and P2MP) and mVRF over       #
#                     BGP within chain DG                                       #
#         vi.     Configuring Parameters in mVRF at sender PE Router            #
#         vii.    Adding mVRF Route Range(both IPv4 and v6) as Sender Site      #
#                     behind Sender PE Router and as Receiver Site behind       # 
#                     Receiver PE Router                                        #
#         viii.   Configuring S-PMSI Tunnel in Sender Site (both IPv4/v6 range) #
#        Step 2. Start of protocol                                              #
#        Step 3. Retrieve protocol statistics                                   #
#        Step 4. Retrieve IPv4 mVPN learned info                                #
#        Step 5. Apply changes on the fly                                       #
#        Step 6. S-PMSI Trigger                                                 #
#        Step 7. Retrieve protocol learned info after OTF                       #
#        Step 8. Configure L2-L3 IPv4 I-PMSI traffic.                           #
#        Step 9. Configure L2-L3 IPv6 S-PMSI traffic.                           #
#        Step 10. Apply and start L2/L3 traffic.                                #
#        Step 11. Retrieve L2/L3 traffic item statistics.                       #
#        Step 12. Stop L2/L3 traffic.                                           #
#        Step 13. Stop all protocols.                                           #
#################################################################################

################################################################################
# Please ensure that PERL5LIB environment variable is set properly so that 
# IxNetwork.pm module is available. IxNetwork.pm is generally available in
# C:\<IxNetwork Install Path>\API\Perl
################################################################################
use IxNetwork;
use strict;

sub assignPorts {
    my @my_resource = @_;
    my $ixNet    = $my_resource[0];
    my $chassis1 = $my_resource[1];
    my $card1    = $my_resource[2];
    my $port1    = $my_resource[3];
    my $chassis2 = $my_resource[4];
    my $card2    = $my_resource[5];
    my $port2    = $my_resource[6];
    my $vport1   = $my_resource[7];
    my $vport2   = $my_resource[8];
    
    my $root = $ixNet->getRoot();
    my $chassisObj1 = $ixNet->add($root.'/availableHardware', 'chassis');
    $ixNet->setAttribute($chassisObj1, '-hostname', $chassis1);
    $ixNet->commit();
    $chassisObj1 = ($ixNet->remapIds($chassisObj1))[0];
    
    my $chassisObj2 = '';
    if ($chassis1 ne $chassis2) {
        $chassisObj2 = $ixNet->add($root.'/availableHardware', 'chassis');
        $ixNet->setAttribute($chassisObj2, '-hostname', $chassis2);
        $ixNet->commit();
        $chassisObj2 = ($ixNet->remapIds($chassisObj2))[0];
    } else {
        $chassisObj2 = $chassisObj1;
    }
    
    my $cardPortRef1 = $chassisObj1.'/card:'.$card1.'/port:'.$port1;
    $ixNet->setMultiAttribute($vport1, '-connectedTo', $cardPortRef1,
        '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 001');
    $ixNet->commit();

    my $cardPortRef2 = $chassisObj2.'/card:'.$card2.'/port:'.$port2;
    $ixNet->setMultiAttribute($vport2, '-connectedTo', $cardPortRef2,
        '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 002');
    $ixNet->commit();
}

# Script Starts
print("!!! Test Script Starts !!!\n");
# Edit this variables values to match your setup
my $ixTclServer = '10.39.50.134';
my $ixTclPort   = '8990';
my @ports       = (('10.39.50.126', '2', '1'), ('10.39.50.126', '2', '2'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '8.50',
    '-setAttribute', 'strict');
print("Creating a new config\n");
$ixNet->execute('newConfig');

#################################################################################
# Step 1> protocol configuration section
#################################################################################
print("Adding 2 vports\n");
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->commit();

my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vportTx = $vPorts[0];
my $vportRx = $vPorts[1];
assignPorts($ixNet, @ports, $vportTx, $vportRx);
sleep(5);

print("Adding 2 topologies\n");
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', $vportTx);
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', $vportRx);
$ixNet->commit();

my @topologies = $ixNet->getList($ixNet->getRoot(), 'topology');
my $topo1 = $topologies[0];
my $topo2 = $topologies[1];

print("Adding 2 device groups\n");
$ixNet->add($topo1, 'deviceGroup');
$ixNet->add($topo2, 'deviceGroup');
$ixNet->commit();

my @t1devices = $ixNet->getList($topo1, 'deviceGroup');
my @t2devices = $ixNet->getList($topo2, 'deviceGroup');
print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1,  '-name', 'Ingress Topology');
$ixNet->setAttribute($topo2,  '-name', 'Egress Topology');
$ixNet->commit();
my $t1dev1 = $t1devices[0];
my $t2dev1 = $t2devices[0];
$ixNet->setAttribute($t1dev1, '-name', 'Sender P router');
$ixNet->setAttribute($t2dev1, '-name', 'Receiver P router');
$ixNet->commit();

print("Configuring the multipliers (number of sessions)\n");
$ixNet->setAttribute($t1dev1, '-multiplier', '2');
$ixNet->setAttribute($t2dev1, '-multiplier', '2');
$ixNet->commit();

print("Adding ethernet/mac endpoints\n");
$ixNet->add($t1dev1, 'ethernet');
$ixNet->add($t2dev1, 'ethernet');
$ixNet->commit();

my $mac1 = ($ixNet->getList($t1dev1, 'ethernet'))[0];
my $mac2 = ($ixNet->getList($t2dev1, 'ethernet'))[0];

print("Configuring the mac addresses\n");
$ixNet->setMultiAttribute($ixNet->getAttribute($mac1, '-mac').'/counter',
        '-direction', 'increment',
        '-start',     '22:22:22:22:22:22',
        '-step',      '00:00:00:00:00:01');

$ixNet->setAttribute($ixNet->getAttribute($mac2, '-mac').'/counter',
        '-direction', 'increment',
        '-start',     '44:44:44:44:44:44',
        '-step',      '00:00:00:00:00:01');
$ixNet->commit();

print("Enabling VLAN\n");
$ixNet->setMultiAttribute($ixNet->getAttribute($mac1, '-enableVlans').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($mac2, '-enableVlans').'/singleValue', '-value', 'true');
$ixNet->commit();

print("Configuring VLAN ID\n");
$ixNet->setAttribute($ixNet->getAttribute($mac1.'/vlan:1', '-vlanId').'/counter',
        '-direction', 'increment',
        '-start',     '400',
        '-step',      '1');
$ixNet->commit();

$ixNet->setAttribute($ixNet->getAttribute($mac2.'/vlan:1', '-vlanId').'/counter',
        '-direction', 'increment',
        '-start',     '400',
        '-step',      '1');
$ixNet->commit();

print("Add ipv4\n");
$ixNet->add($mac1, 'ipv4');
$ixNet->add($mac2, 'ipv4');
$ixNet->commit();

my $ip1 = ($ixNet->getList($mac1, 'ipv4'))[0];
my $ip2 = ($ixNet->getList($mac2, 'ipv4'))[0];

my $mvAdd1 = $ixNet->getAttribute($ip1, '-address');
my $mvAdd2 = $ixNet->getAttribute($ip2, '-address');
my $mvGw1  = $ixNet->getAttribute($ip1, '-gatewayIp');
my $mvGw2  = $ixNet->getAttribute($ip2, '-gatewayIp');

print("configuring ipv4 addresses\n");
$ixNet->setMultiAttribute($mvAdd1.'/counter',
        '-direction', 'increment',
        '-start',     '50.50.50.2',
        '-step',      '0.1.0.0');
$ixNet->setMultiAttribute($mvAdd2.'/counter',
        '-direction', 'increment',
        '-start',     '50.50.50.20',
        '-step',      '0.1.0.0');
$ixNet->setMultiAttribute($mvGw1.'/counter',
        '-direction', 'increment',
        '-start',     '50.50.50.20',
        '-step',      '0.1.0.0');
$ixNet->setMultiAttribute($mvGw2.'/counter',
        '-direction', 'increment',
        '-start',     '50.50.50.2',
        '-step',      '0.1.0.0');
$ixNet->commit();

print("Adding OSPFv2 over IP4 stacks\n");
$ixNet->add($ip1, 'ospfv2');
$ixNet->add($ip2, 'ospfv2');
$ixNet->commit();

my $ospf1 = ($ixNet->getList($ip1, 'ospfv2'))[0];
my $ospf2 = ($ixNet->getList($ip2, 'ospfv2'))[0];
$ixNet->commit();

print("Making the NetworkType to Point to Point in the first OSPF router\n");
my $networkTypeMultiValue1 = $ixNet->getAttribute($ospf1, '-networkType');
$ixNet->setMultiAttribute($networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($networkTypeMultiValue1.'/singleValue', '-value', 'pointtopoint');

print("Making the NetworkType to Point to Point in the Second OSPF router\n");
my $networkTypeMultiValue2 = $ixNet->getAttribute($ospf2, '-networkType');
$ixNet->setAttribute($networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setAttribute($networkTypeMultiValue2.'/singleValue', '-value', 'pointtopoint');

print("Disabling the Discard Learned Info CheckBox\n");
my $ospfv2RouterDiscardLearnedLSA1 = $ixNet->getAttribute(($ixNet->getList($t1devices[0], 'ospfv2Router'))[0],
    '-discardLearnedLsa');

my $ospfv2RouterDiscardLearnedLSA2 = $ixNet->getAttribute(($ixNet->getList($t2devices[0], 'ospfv2Router'))[0],
    '-discardLearnedLsa');

$ixNet->setAttribute($ospfv2RouterDiscardLearnedLSA1,
     '-pattern', 'singleValue',
     '-clearOverlays', 'False');
$ixNet->setAttribute($ospfv2RouterDiscardLearnedLSA1.'/singleValue', '-value', 'False');

$ixNet->setAttribute($ospfv2RouterDiscardLearnedLSA2,
    '-pattern', 'singleValue',
    '-clearOverlays', 'False');
$ixNet->setAttribute($ospfv2RouterDiscardLearnedLSA2.'/singleValue', '-value', 'False');
$ixNet->commit();

print("Adding Connected LDP-IF over IPv4 stack\n");
$ixNet->add($ip1, 'ldpConnectedInterface');
$ixNet->add($ip2, 'ldpConnectedInterface');
$ixNet->commit();

print("Adding Connected LDP-RTR over IPv4 stack\n");
$ixNet->add($ip1, 'ldpBasicRouter');
$ixNet->add($ip2, 'ldpBasicRouter');
$ixNet->commit();

my $ldp1 = ($ixNet->getList($ip1, 'ldpBasicRouter'))[0];
my $ldp2 = ($ixNet->getList($ip2, 'ldpBasicRouter'))[0];

print("Enabling P2MP Capability in the first LDP router\n");
my $p2MpCapability1 = $ixNet->getAttribute($ldp1, '-enableP2MPCapability');
$ixNet->setAttribute($p2MpCapability1,
     '-pattern', 'singleValue',
     '-clearOverlays', 'False');
$ixNet->setAttribute($p2MpCapability1.'/singleValue', '-value', 'true');

print("Enabling P2MP Capability in the second LDP router\n");
my $p2MpCapability2 = $ixNet->getAttribute($ldp2, '-enableP2MPCapability');
$ixNet->setAttribute($p2MpCapability2,
     '-pattern', 'singleValue',
     '-clearOverlays', 'False');
$ixNet->setAttribute($p2MpCapability2.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Enabling Root ranges in the Sender P LDP router\n");
$ixNet->setMultiAttribute($ldp1, '-rootRangesCountV4', '1');
$ixNet->commit();

print("Enabling Root ranges in the Receiver P LDP router\n");
$ixNet->setMultiAttribute($ldp2, '-rootRangesCountV4', '1');
$ixNet->commit();

print("Enabling Leaf ranges in the Sender P LDP router\n");
$ixNet->setMultiAttribute($ldp1, '-leafRangesCountV4', '1');
$ixNet->commit();

print("Enabling Leaf ranges in the Receiver P LDP router\n");
$ixNet->setMultiAttribute($ldp2, '-leafRangesCountV4', '1');
$ixNet->commit();

print("Configuring mLDP Leaf range in Sender LDP router\n");
$ixNet->setMultiAttribute($ldp1.'/ldpLeafRangeV4', '-numberOfTLVs', '3');
$ixNet->commit();

print("Configuring mLDP Leaf range in Receiver LDP router\n");
$ixNet->setMultiAttribute($ldp2.'/ldpLeafRangeV4', '-numberOfTLVs', '3');
$ixNet->commit();

print("Activating mLDP Leaf range in Sender LDP router\n");
my $active1 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4', '-active');
$ixNet->setMultiAttribute($active1,
     '-pattern', 'singleValue',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($active1.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Changing Continuous Increment Opaque Value Across Root in mLDP Leaf range in Sender LDP router\n");
my $contIncOpq1 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4', '-continuousIncrementOVAcrossRoot');
$ixNet->setMultiAttribute($contIncOpq1.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Changing Label Value Step in mLDP Leaf range in Sender LDP router\n");
my $label1 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4', '-labelValueStep');
$ixNet->setMultiAttribute($label1.'/singleValue', '-value', '1');
$ixNet->commit();

print("Changing Label Value Start in mLDP Leaf range in Sender LDP router\n");
my $start1 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4', '-labelValueStart');
$ixNet->setMultiAttribute($start1,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($start1.'/counter',
        '-direction', 'increment',
        '-start',     '12321',
        '-step',      '1');
$ixNet->commit();

print("Changing LSP count per root in mLDP Leaf range in Sender LDP router\n");
my $lspCountPerRoot1 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4', '-lspCountPerRoot');
$ixNet->setMultiAttribute($lspCountPerRoot1.'/singleValue', '-value', '2');
$ixNet->commit();

print("Changing Root Address Step in mLDP Leaf range in Sender LDP router\n");
my $rootAddStep1 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4', '-rootAddressStep');
$ixNet->setMultiAttribute($rootAddStep1.'/singleValue', '-value', '0.0.0.1');
$ixNet->commit();

print("Changing Root Address Count in mLDP Leaf range in Sender LDP router\n");
my $rootAddCnt1 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4', '-rootAddressCount');
$ixNet->setMultiAttribute($rootAddCnt1.'/singleValue', '-value', '1');
$ixNet->commit();

print("Changing Root Address in mLDP Leaf range in Sender LDP router\n");
my $rootAdd1 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4', '-rootAddress');
$ixNet->setMultiAttribute($rootAdd1,
     '-pattern', 'singleValue',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($rootAdd1.'/singleValue',
        '-value', '7.7.7.7');
$ixNet->commit();

print("Changing TLV1 name in mLDP Leaf range in Sender LDP router\n");
$ixNet->setMultiAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:1', '-name', 'LDP Opaque TLV 1');
$ixNet->commit();

print("Deactivating TLV1 in mLDP Leaf range in Sender LDP router\n");
my $active1 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:1', '-active');
$ixNet->setMultiAttribute($active1.'/singleValue', '-value', 'false');
$ixNet->commit();

print("Changing Type of TLV1 in mLDP Leaf range in Sender LDP router\n");
my $type1 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:1', '-type');
$ixNet->setMultiAttribute($type1.'/singleValue', '-value', '1');
$ixNet->commit();

print("Changing Length of TLV1 in mLDP Leaf range in Sender LDP router\n");
my $len1 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:1', '-tlvLength');
$ixNet->setMultiAttribute($len1.'/singleValue', '-value', '4');
$ixNet->commit();

print("Changing Value of TLV1 in mLDP Leaf range in Sender LDP router\n");
my $val1 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:1', '-value');
$ixNet->setMultiAttribute($val1,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($val1.'/counter',
        '-direction', 'increment',
        '-start',     '00000001',
        '-step',      '01');
$ixNet->commit();

print("Changing Increment of TLV1 in mLDP Leaf range in Sender LDP router\n");
my $inc1 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:1', '-increment');
$ixNet->setMultiAttribute($inc1.'/singleValue', '-value', '00000001');
$ixNet->commit();

print("Changing TLV2 name in mLDP Leaf range in Sender LDP router\n");
$ixNet->setMultiAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:2', '-name', 'LDP Opaque TLV 2');
$ixNet->commit();

print("Activating TLV2 in mLDP Leaf range in Sender LDP router\n");
my $active2 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:2', '-active');
$ixNet->setMultiAttribute($active2.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Changing Type of TLV2 in mLDP Leaf range in Sender LDP router\n");
my $type2 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:2', '-type');
$ixNet->setMultiAttribute($type2.'/singleValue', '-value', '123');
$ixNet->commit();

print("Changing Length of TLV2 in mLDP Leaf range in Sender LDP router\n");
my $len2 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:2', '-tlvLength');
$ixNet->setMultiAttribute($len2.'/singleValue', '-value', '5');
$ixNet->commit();

print("Changing Value of TLV2 in mLDP Leaf range in Sender LDP router\n");
my $val2 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:2', '-value');
$ixNet->setMultiAttribute($val2,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($val2.'/counter',
        '-direction', 'increment',
        '-start',     '00000000A1',
        '-step',      '04');
$ixNet->commit();

print("Changing Increment of TLV2 in mLDP Leaf range in Sender LDP router\n");
my $inc2 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:2', '-increment');
$ixNet->setMultiAttribute($inc2.'/singleValue', '-value', '0000000001');
$ixNet->commit();

print("Activating TLV3 in mLDP Leaf range in Sender LDP router\n");
my $active3 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:3', '-active');
$ixNet->setMultiAttribute($active3.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Changing Type of TLV3 in mLDP Leaf range in Sender LDP router\n");
my $type3 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:3', '-type');
$ixNet->setMultiAttribute($type3.'/singleValue', '-value', '1');
$ixNet->commit();

print("Changing Length of TLV3 in mLDP Leaf range in Sender LDP router\n");
my $len3 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:3', '-tlvLength');
$ixNet->setMultiAttribute($len3.'/singleValue', '-value', '4');
$ixNet->commit();

print("Changing Value of TLV3 in mLDP Leaf range in Sender LDP router\n");
my $val3 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:3', '-value');
$ixNet->setMultiAttribute($val3,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($val3.'/counter',
        '-direction', 'increment',
        '-start',     '00000001',
        '-step',      '04');
$ixNet->commit();

print("Changing Increment of TLV3 in mLDP Leaf range in Sender LDP router\n");
my $inc3 = $ixNet->getAttribute($ldp1.'/ldpLeafRangeV4/ldpTLVList:3', '-increment');
$ixNet->setMultiAttribute($inc3.'/singleValue', '-value', '00000001');
$ixNet->commit();

print("Configuring mLDP Leaf range in Receiver LDP router\n");
print("Activating mLDP Leaf range in Receiver LDP router\n");
my $active22 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4', '-active');
$ixNet->setMultiAttribute($active22,
     '-pattern', 'singleValue',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($active22.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Changing Continuous Increment Opaque Value Across Root in mLDP Leaf range in Receiver LDP router\n");
my $contIncOpq22 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4', '-continuousIncrementOVAcrossRoot');
$ixNet->setMultiAttribute($contIncOpq22.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Changing Label Value Step in mLDP Leaf range in Receiver LDP router\n");
my $label22 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4', '-labelValueStep');
$ixNet->setMultiAttribute($label22.'/singleValue', '-value', '1');
$ixNet->commit();

print("Changing Label Value Start in mLDP Leaf range in Receiver LDP router\n");
my $start22 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4', '-labelValueStart');
$ixNet->setMultiAttribute($start22,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($start22.'/counter',
        '-direction', 'increment',
        '-start',     '8916',
        '-step',      '100');
$ixNet->commit();

print("Changing LSP count per root in mLDP Leaf range in Receiver LDP router\n");
my $lspCountPerRoot22 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4', '-lspCountPerRoot');
$ixNet->setMultiAttribute($lspCountPerRoot22.'/singleValue', '-value', '6');
$ixNet->commit();

print("Changing Root Address Step in mLDP Leaf range in Receiver LDP router\n");
my $rootAddStep22 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4', '-rootAddressStep');
$ixNet->setMultiAttribute($rootAddStep22.'/singleValue', '-value', '0.0.0.1');
$ixNet->commit();

print("Changing Root Address Count in mLDP Leaf range in Receiver LDP router\n");
my $rootAddCnt22 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4', '-rootAddressCount');
$ixNet->setMultiAttribute($rootAddCnt22.'/singleValue', '-value', '1');
$ixNet->commit();

print("Changing Root Address in mLDP Leaf range in Receiver LDP router\n");
my $rootAdd22 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4', '-rootAddress');
$ixNet->setMultiAttribute($rootAdd22,
     '-pattern', 'singleValue',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($rootAdd22.'/singleValue',
        '-value', '8.8.8.7');
$ixNet->commit();

print("Changing TLV1 name in mLDP Leaf range in Receiver LDP router\n");
$ixNet->setMultiAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:1', '-name', 'LDP Opaque TLV 4');
$ixNet->commit();

print("Activating TLV1 in mLDP Leaf range in Receiver LDP router\n");
my $active4 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:1', '-active');
$ixNet->setMultiAttribute($active4.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Changing Type of TLV1 in mLDP Leaf range in Receiver LDP router\n");
my $type4 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:1', '-type');
$ixNet->setMultiAttribute($type4.'/singleValue', '-value', '111');
$ixNet->commit();

print("Changing Length of TLV1 in mLDP Leaf range in Receiver LDP router\n");
my $len4 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:1', '-tlvLength');
$ixNet->setMultiAttribute($len4.'/singleValue', '-value', '33');
$ixNet->commit();

print("Changing Value of TLV1 in mLDP Leaf range in Receiver LDP router\n");
my $val4 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:1', '-value');
$ixNet->setMultiAttribute($val4,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($val4.'/counter',
        '-direction', 'increment',
        '-start',     '000000000000000000000000000000000000000000000000000000000000007651',
        '-step',      '04');
$ixNet->commit();

print("Changing Increment of TLV1 in mLDP Leaf range in Receiver LDP router\n");
my $inc4 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:1', '-increment');
$ixNet->setMultiAttribute($inc4.'/singleValue', '-value', '000000000000000000000000000000000000000000000000000000000000000001');
$ixNet->commit();

print("Changing TLV2 name in mLDP Leaf range in Receiver LDP router\n");
$ixNet->setMultiAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:2', '-name', 'LDP Opaque TLV 5');
$ixNet->commit();

print("Activating TLV2 in mLDP Leaf range in Receiver LDP router\n");
my $active5 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:2', '-active');
$ixNet->setMultiAttribute($active5.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Changing Type of TLV2 in mLDP Leaf range in Receiver LDP router\n");
my $type5 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:2', '-type');
$ixNet->setMultiAttribute($type5.'/singleValue', '-value', '123');
$ixNet->commit();

print("Changing Length of TLV2 in mLDP Leaf range in Receiver LDP router\n");
my $len5 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:2', '-tlvLength');
$ixNet->setMultiAttribute($len5.'/singleValue', '-value', '5');
$ixNet->commit();

print("Changing Value of TLV2 in mLDP Leaf range in Receiver LDP router\n");
my $val5 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:2', '-value');
$ixNet->setMultiAttribute($val5,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($val5.'/counter',
        '-direction', 'increment',
        '-start',     '00000000A1',
        '-step',      '04');
$ixNet->commit();

print("Changing Increment of TLV2 in mLDP Leaf range in Receiver LDP router\n");
my $inc5 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:2', '-increment');
$ixNet->setMultiAttribute($inc5.'/singleValue', '-value', '0000000001');
$ixNet->commit();

print("Changing TLV3 name in mLDP Leaf range in Receiver LDP router\n");
$ixNet->setMultiAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:3', '-name', 'LDP Opaque TLV 6');
$ixNet->commit();

print("Activating TLV3 in mLDP Leaf range in Receiver LDP router\n");
my $active6 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:3', '-active');
$ixNet->setMultiAttribute($active6.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Changing Type of TLV3 in mLDP Leaf range in Receiver LDP router\n");
my $type6 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:3', '-type');
$ixNet->setMultiAttribute($type6.'/singleValue', '-value', '1');
$ixNet->commit();

print("Changing Length of TLV3 in mLDP Leaf range in Receiver LDP router\n");
my $len6 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:3', '-tlvLength');
$ixNet->setMultiAttribute($len6.'/singleValue', '-value', '4');
$ixNet->commit();

print("Changing Value of TLV3 in mLDP Leaf range in Receiver LDP router\n");
my $val6 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:3', '-value');
$ixNet->setMultiAttribute($val6,
     '-pattern', 'singleValue',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($val6.'/singleValue',
        '-value',     '00000001');
$ixNet->commit();

print("Changing Increment of TLV3 in mLDP Leaf range in Receiver LDP router\n");
my $inc6 = $ixNet->getAttribute($ldp2.'/ldpLeafRangeV4/ldpTLVList:3', '-increment');
$ixNet->setMultiAttribute($inc6.'/singleValue', '-value', '00000001');
$ixNet->commit();

print("Adding IPv4 Address Pool in Topology1\n");
$ixNet->add($t1dev1, 'networkGroup');
$ixNet->add($t2dev1, 'networkGroup');
$ixNet->commit();

my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
my $networkGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];

print("Adding the Network Topology behind Ethernet for Sender P router\n");
$ixNet->add($ixNet->add($networkGroup1, 'networkTopology'),'netTopologyLinear');
$ixNet->commit();

$ixNet->setMultiAttribute($ixNet->remapIds(($ixNet->getList(($ixNet->getList($networkGroup1, 'networkTopology'), 'netTopologyLinear')))[0]), '-nodes', '5');
$ixNet->commit();

my $networkTopology1 = ($ixNet->getList($networkGroup1, 'networkTopology'));
$networkTopology1 = ($ixNet->remapIds($networkTopology1))[0];
$ixNet->commit();

print("Adding the Network Topology behind Ethernet for Receiver P router\n");
$ixNet->add($ixNet->add($networkGroup2, 'networkTopology'),'netTopologyLinear');
$ixNet->commit();

$ixNet->setMultiAttribute($ixNet->remapIds(($ixNet->getList(($ixNet->getList($networkGroup2, 'networkTopology'), 'netTopologyLinear')))[0]), '-nodes', '5');
$ixNet->commit();

my $networkTopology2 = ($ixNet->getList($networkGroup2, 'networkTopology'));
$networkTopology2 = ($ixNet->remapIds($networkTopology2))[0];
$ixNet->commit();
my $netTopo1 = ($ixNet->getList($networkGroup1, 'networkTopology'))[0];
my $netTopo2 = ($ixNet->getList($networkGroup2, 'networkTopology'))[0];

print("Enabling Traffic Engineering behind mVRF for Sender P router\n");
my $simInterface1 = ($ixNet->getList($netTopo1, 'simInterface'))[0];
my $simInterfaceIPv4Config1 = ($ixNet->getList($simInterface1, 'simInterfaceIPv4Config'))[0];
my $ospfPseudoInterface1 = ($ixNet->getList($simInterfaceIPv4Config1, 'ospfPseudoInterface'))[0];
my $ospfPseudoInterface1_teEnable = $ixNet->getAttribute($ospfPseudoInterface1, '-enable');
$ixNet->setMultiAttribute($ospfPseudoInterface1_teEnable, '-clearOverlays', 'False', '-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($ospfPseudoInterface1_teEnable.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Enabling Traffic Engineering behind mVRF for Receiver P router\n");
my $simInterface2 = ($ixNet->getList($netTopo2, 'simInterface'))[0];
my $simInterfaceIPv4Config2 = ($ixNet->getList($simInterface2, 'simInterfaceIPv4Config'))[0];
my $ospfPseudoInterface2 = ($ixNet->getList($simInterfaceIPv4Config2, 'ospfPseudoInterface'))[0];
my $ospfPseudoInterface2_teEnable = $ixNet->getAttribute($ospfPseudoInterface2, '-enable');
$ixNet->setMultiAttribute($ospfPseudoInterface2_teEnable, '-clearOverlays', 'False', '-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($ospfPseudoInterface2_teEnable.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Renaming Network Topology \n");
$ixNet->setAttribute($networkGroup1, '-name', 'Simulated Topology for Sender PE Address');
$ixNet->setAttribute($networkGroup2, '-name', 'Simulated Topology for Receiver PE Address');
$ixNet->commit();

print("Add IPv4 Loopback for PE\n");
my $loopback1 = $ixNet->add($t1dev1, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback1, '-stackedLayers', [], '-name', 'IPv4 Loopback 1');
$ixNet->commit();

my $loopback2 = $ixNet->add($t2dev1, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback2, '-stackedLayers', [], '-name', 'IPv4 Loopback 2');
$ixNet->commit();

print("Changing the IPv4 Loopback addresses\n");
my $lpbk_add1 = $ixNet->getAttribute($loopback1, '-address');
$ixNet->setMultiAttribute($lpbk_add1,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($lpbk_add1.'/counter',
        '-direction', 'increment',
        '-start',     '8.8.8.7',
        '-step',      '0.0.0.1');
$ixNet->commit();

my $lpbk_add2 = $ixNet->getAttribute($loopback2, '-address');
$ixNet->setMultiAttribute($lpbk_add2,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($lpbk_add2.'/counter',
        '-direction', 'increment',
        '-start',     '7.7.7.7',
        '-step',      '0.0.0.1');
$ixNet->commit();

print("Adding BGP over IPv4 Loopback interface 1 \n");
my $bgp1 = $ixNet->add($loopback1, 'bgpIpv4Peer');
$ixNet->commit();
$bgp1 = ($ixNet->remapIds($bgp1))[0];

print("Adding BGP over IPv4 Loopback interface 2 \n");
my $bgp2 = $ixNet->add($loopback2, 'bgpIpv4Peer');
$ixNet->commit();
$bgp2 = ($ixNet->remapIds($bgp2))[0];

print("Setting IPs in BGP DUT IP tab\n");
my $dutIp1 = $ixNet->getAttribute($bgp1, '-dutIp');
$ixNet->setMultiAttribute($dutIp1,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($dutIp1.'/counter',
        '-direction', 'increment',
        '-start',     '7.7.7.7',
        '-step',      '0.0.0.1');
$ixNet->commit();

my $dutIp2 = $ixNet->getAttribute($bgp2, '-dutIp');
$ixNet->setMultiAttribute($dutIp2,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($dutIp2.'/counter',
        '-direction', 'increment',
        '-start',     '8.8.8.7',
        '-step',      '0.0.0.1');
$ixNet->commit();

print("Enabling MVPN Capabilities for BGP Router \n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-capabilityIpV4MplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-capabilityIpV4Multicast').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-capabilityIpV4Multicast').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-capabilityIpV4Multicast').'/singleValue', '-value', 'true');

$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-capabilityIpV6MplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-capabilityIpV6Multicast').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-capabilityIpV6MulticastVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-ipv6MulticastBgpMplsVpn').'/singleValue', '-value', 'true');

$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-capabilityIpV4MplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-capabilityIpV4Multicast').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-capabilityIpV4Multicast').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-capabilityIpV4Multicast').'/singleValue', '-value', 'true');

$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-capabilityIpV6MplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-capabilityIpV6Multicast').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-capabilityIpV6MulticastVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-ipv6MulticastBgpMplsVpn').'/singleValue', '-value', 'true');
$ixNet->commit();

print("Enabling MVPN Learned Information for BGP Router \n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-filterIpV4Unicast').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-filterIpV4MplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-filterIpv4MulticastBgpMplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-filterIpV4MulticastVpn').'/singleValue', '-value', 'true');

$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-filterIpV6Unicast').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-filterIpV6MplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-filterIpv6MulticastBgpMplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-filterIpV6MulticastVpn').'/singleValue', '-value', 'true');


$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-filterIpV4Unicast').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-filterIpV4MplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-filterIpv4MulticastBgpMplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-filterIpV4MulticastVpn').'/singleValue', '-value', 'true');

$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-filterIpV6Unicast').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-filterIpV6MplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-filterIpv6MulticastBgpMplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-filterIpV6MulticastVpn').'/singleValue', '-value', 'true');
$ixNet->commit();

print("Adding mVRF over BGP in both ports \n");
$ixNet->add($bgp1, 'bgpIpv4MVrf');
$ixNet->add($bgp2, 'bgpIpv4MVrf');
$ixNet->commit();
my $mVRF1 = ($ixNet->getList($bgp1, 'bgpIpv4MVrf'))[0];
my $mVRF2 = ($ixNet->getList($bgp2, 'bgpIpv4MVrf'))[0];

print("Configuring mLDP P2MP as the Tunnel Type in Sender P router\n");
my $tunnel_type1 = $ixNet->getAttribute($mVRF1, '-multicastTunnelType');
$ixNet->setMultiAttribute($tunnel_type1.'/singleValue', '-value', 'tunneltypemldpp2mp');
$ixNet->commit();

print("Configuring mLDP P2MP as the Tunnel Type in Receiver P router\n");
my $tunnel_type2 = $ixNet->getAttribute($mVRF2, '-multicastTunnelType');
$ixNet->setMultiAttribute($tunnel_type2.'/singleValue', '-value', 'tunneltypemldpp2mp');
$ixNet->commit();

print("Configuring Root Address in Topology 1\n");
my $rtAdd1 = $ixNet->getAttribute($mVRF1, '-rootAddress');
$ixNet->setMultiAttribute($rtAdd1.'/singleValue', '-value', '8.8.8.7');
$ixNet->commit();

print("Configuring Root Address in Topology 2\n");
my $rtAdd2 = $ixNet->getAttribute($mVRF2, '-rootAddress');
$ixNet->setMultiAttribute($rtAdd2.'/singleValue', '-value', '7.7.7.7');
$ixNet->commit();

print("Enabling CheckBox for use of Up/DownStream Assigned Label for Ingress Topology\n");
my $useUpOrDownStreamAssigneLabel1 = $ixNet->getAttribute($mVRF1, '-useUpOrDownStreamAssigneLabel');
$ixNet->setMultiAttribute($useUpOrDownStreamAssigneLabel1,
     '-pattern', 'singleValue',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($useUpOrDownStreamAssigneLabel1.'/singleValue',
        '-value', 'True');
$ixNet->commit();

print("Assigning value for Up/DownStream Assigned Label for Ingress Topology\n");
my $upOrDownStreamAssignedLabel1 = $ixNet->getAttribute($mVRF1, '-upOrDownStreamAssignedLabel');
$ixNet->setMultiAttribute($upOrDownStreamAssignedLabel1,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($upOrDownStreamAssignedLabel1.'/counter',
     '-step', '1', 
	 '-start', '10001', 
	 '-direction', 'increment');
$ixNet->commit();

print("Enabling CheckBox for use of Up/DownStream Assigned Label for Egress Topology\n");
my $useUpOrDownStreamAssigneLabel2 = $ixNet->getAttribute($mVRF2, '-useUpOrDownStreamAssigneLabel');
$ixNet->setMultiAttribute($useUpOrDownStreamAssigneLabel2,
     '-pattern', 'singleValue',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($useUpOrDownStreamAssigneLabel2.'/singleValue',
        '-value', 'True');
$ixNet->commit();

print("Assigning value for Up/DownStream Assigned Label for Egress Topology\n");
my $upOrDownStreamAssignedLabel2 = $ixNet->getAttribute($mVRF2, '-upOrDownStreamAssignedLabel');
$ixNet->setMultiAttribute($upOrDownStreamAssignedLabel2,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($upOrDownStreamAssignedLabel2.'/counter',
     '-step', '1', 
	 '-start', '3116', 
	 '-direction', 'increment');
$ixNet->commit();

print("Configuring Opaque TLV Type for I-PMSI in Sender mVRF\n");
my $opaque_type1 = $ixNet->getAttribute($mVRF1.'/pnTLVList:1', '-type');
$ixNet->setMultiAttribute($opaque_type1.'/singleValue', '-value', '111');
$ixNet->commit();

print("Configuring Opaque TLV Length for I-PMSI in Sender mVRF\n");
my $opaque_len1 = $ixNet->getAttribute($mVRF1.'/pnTLVList:1', '-tlvLength');
$ixNet->setMultiAttribute($opaque_len1.'/singleValue', '-value', '33');
$ixNet->commit();

print("Configuring Opaque TLV Value for I-PMSI in Sender mVRF\n");
my $opaque_val1 = $ixNet->getAttribute($mVRF1.'/pnTLVList:1', '-value');
$ixNet->setMultiAttribute($opaque_val1,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($opaque_val1.'/counter',
        '-direction', 'increment',
        '-start',     '000000000000000000000000000000000000000000000000000000000000007651',
        '-step',      '04');
$ixNet->commit();

print("Configuring Opaque TLV Increment for I-PMSI in Sender mVRF\n");
my $opaque_inc1 = $ixNet->getAttribute($mVRF1.'/pnTLVList:1', '-increment');
$ixNet->setMultiAttribute($opaque_inc1.'/singleValue', '-value', '000000000000000000000000000000000000000000000000000000000000000001');
$ixNet->commit();

print("Configuring Opaque TLV Type for I-PMSI in Receiver mVRF\n");
my $opaque_type2 = $ixNet->getAttribute($mVRF2.'/pnTLVList:1', '-type');
$ixNet->setMultiAttribute($opaque_type2.'/singleValue', '-value', '123');
$ixNet->commit();

print("Configuring Opaque TLV Length for I-PMSI in Receiver mVRF\n");
my $opaque_len2 = $ixNet->getAttribute($mVRF2.'/pnTLVList:1', '-tlvLength');
$ixNet->setMultiAttribute($opaque_len2.'/singleValue', '-value', '5');
$ixNet->commit();

print("Configuring Opaque TLV Value for I-PMSI in Receiver mVRF\n");
my $opaque_val2 = $ixNet->getAttribute($mVRF2.'/pnTLVList:1', '-value');
$ixNet->setMultiAttribute($opaque_val2,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($opaque_val2.'/counter',
        '-direction', 'increment',
        '-start',     '00000000A1',
        '-step',      '04');
$ixNet->commit();

print("Configuring Opaque TLV Increment for I-PMSI in Receiver mVRF\n");
my $opaque_inc2 = $ixNet->getAttribute($mVRF2.'/pnTLVList:1', '-increment');
$ixNet->setMultiAttribute($opaque_inc2.'/singleValue', '-value', '0000000001');
$ixNet->commit();

print("Adding Network Group behind mVRF for Ingress Topology \n");
$ixNet->add($t1dev1, 'networkGroup');
$ixNet->commit();
my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[1];
$ixNet->setAttribute($networkGroup1, '-name', 'IPv4 Sender Site-IPv6 Receiver Site');
$ixNet->commit();

print("Adding Network Group behind mVRF for Egress Topology \n");
$ixNet->add($t2dev1, 'networkGroup');
$ixNet->commit();
my $networkGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[1];
$ixNet->setAttribute($networkGroup2, '-name', 'IPv4 Receiver Site-IPv6 Sender Site');
$ixNet->commit();

print("Adding IPv4/IPv6 Prefix pools in Ingress Topology\n");
$ixNet->add($networkGroup1, 'ipv4PrefixPools');
$ixNet->commit();

$ixNet->add($networkGroup1, 'ipv6PrefixPools');
$ixNet->commit();


print("Adding IPv4/IPv6 Prefix pools in Egress Topology\n");
$ixNet->add($networkGroup2, 'ipv4PrefixPools');
$ixNet->commit();

$ixNet->add($networkGroup2, 'ipv6PrefixPools');
$ixNet->commit();

print("Configuring the addresses in IPv4/IPv6 Prefix pools in IPv4 Sender Site-IPv6 Receiver Site\n");
my $ipv4PrefixPools1 = ($ixNet->getList($networkGroup1, 'ipv4PrefixPools'))[0];
my $ipv6PrefixPools1 = ($ixNet->getList($networkGroup1, 'ipv6PrefixPools'))[0];

print("Changing Address for IPv4 Address Pool in Sender Site \n");
my $nwAdd1 = $ixNet->getAttribute($ipv4PrefixPools1, '-networkAddress');
$ixNet->setMultiAttribute($nwAdd1.'/counter',
        '-direction', 'increment',
        '-start',     '200.1.0.1',
        '-step',      '0.1.0.0');
$ixNet->commit();

print("Changing Prefix Length for IPv4 Address Pool in Sender Site \n");
my $mulValPrefLen1 = $ixNet->getAttribute($ipv4PrefixPools1, '-prefixLength');
$ixNet->setMultiAttribute($mulValPrefLen1.'/singleValue', '-value', '32');
$ixNet->commit();

print("Changing Address Count for IPv4 Address Pool in Sender Site \n");
$ixNet->setAttribute($ipv4PrefixPools1, '-numberOfAddresses', '3');
$ixNet->commit();

print("Changing Address for IPv6 Address Pool in Sender Site \n");
my $nwAdd2 = $ixNet->getAttribute($ipv6PrefixPools1, '-networkAddress');
$ixNet->setMultiAttribute($nwAdd2.'/counter',
        '-direction', 'increment',
        '-start',     '5001:1:0:0:0:0:0:1',
        '-step',      '0:0:1:0:0:0:0:0');
$ixNet->setMultiAttribute($nwAdd2.'/singleValue', '-value', '5001:1:0:0:0:0:0:1');
$ixNet->commit();

print("Changing Prefix Length for IPv6 Address Pool in Sender Site \n");
my $mulValPrefLen2 = $ixNet->getAttribute($ipv6PrefixPools1, '-prefixLength');
$ixNet->setMultiAttribute($mulValPrefLen2.'/singleValue', '-value', '128');
$ixNet->commit();

print("Changing Address Count for IPv6 Address Pool in Sender Site \n");
$ixNet->setAttribute($ipv6PrefixPools1, '-numberOfAddresses', '5');
$ixNet->commit();

print("Changing label value for IPv4/IPv6 in IPv4 Sender Site-IPv6 Receiver Site\n");
my $bgpL3VpnRouteProperty1 = ($ixNet->getList($ipv4PrefixPools1, 'bgpL3VpnRouteProperty'))[0];
my $bgp6L3VpnRouteProperty1 = ($ixNet->getList($ipv6PrefixPools1, 'bgpV6L3VpnRouteProperty'))[0];

my $label1 = $ixNet->getAttribute($bgpL3VpnRouteProperty1, '-labelStart');
$ixNet->setMultiAttribute($label1.'/counter',
        '-direction', 'increment',
        '-start',     '97710',
        '-step',      '10');
$ixNet->commit();

my $label2 = $ixNet->getAttribute($bgp6L3VpnRouteProperty1, '-labelStart');
$ixNet->setMultiAttribute($label2.'/counter',
        '-direction', 'increment',
        '-start',     '55410',
        '-step',      '10');
$ixNet->commit();

print("Disabling Receiver site and enabling Sender Site for IPv4 in Ingress Topology \n");
my $bgpL3VpnRouteProperty1 = ($ixNet->getList($ipv4PrefixPools1, 'bgpL3VpnRouteProperty'))[0];
my $bgp6L3VpnRouteProperty1 = ($ixNet->getList($ipv6PrefixPools1, 'bgpV6L3VpnRouteProperty'))[0];

$ixNet->setAttribute($bgpL3VpnRouteProperty1, '-enableIpv4Sender', 'True');
$ixNet->setAttribute($bgpL3VpnRouteProperty1, '-enableIpv4Receiver', 'False');
$ixNet->commit();

print("Disabling Sender site and enabling Receiver Site for IPv6 in Ingress Topology \n");
$ixNet->setAttribute($bgp6L3VpnRouteProperty1, '-enableIpv6Sender', 'False');
$ixNet->setAttribute($bgp6L3VpnRouteProperty1, '-enableIpv6Receiver', 'True');
$ixNet->commit();

print("Configuring the addresses in IPv4/IPv6 Prefix pools in IPv4 Receiver Site-IPv6 Sender Site\n");
my $ipv4PrefixPools2 = ($ixNet->getList($networkGroup2, 'ipv4PrefixPools'))[0];
my $ipv6PrefixPools2 = ($ixNet->getList($networkGroup2, 'ipv6PrefixPools'))[0];

print("Changing Address for IPv4 Address Pool in Receiver Site \n");
my $nwAdd3 = $ixNet->getAttribute($ipv4PrefixPools2, '-networkAddress');
$ixNet->setMultiAttribute($nwAdd3.'/counter',
        '-direction', 'increment',
        '-start',     '202.0.0.1',
        '-step',      '0.1.0.0');
$ixNet->commit();

print("Changing Prefix Length for IPv4 Address Pool in Receiver Site \n");
my $mulValPrefLen3 = $ixNet->getAttribute($ipv4PrefixPools2, '-prefixLength');
$ixNet->setMultiAttribute($mulValPrefLen3.'/singleValue', '-value', '32');
$ixNet->commit();

print("Changing Address Count for IPv4 Address Pool in Sender Site \n");
$ixNet->setAttribute($ipv4PrefixPools2, '-numberOfAddresses', '3');
$ixNet->commit();

print("Changing Address for IPv6 Address Pool in Sender Site \n");
my $nwAdd4 = $ixNet->getAttribute($ipv6PrefixPools2, '-networkAddress');
$ixNet->setMultiAttribute($nwAdd4.'/counter',
        '-direction', 'increment',
        '-start',     '3001:1:0:0:0:0:0:1',
        '-step',      '0:0:1:0:0:0:0:0');
$ixNet->commit();

print("Changing Prefix Length for IPv6 Address Pool in Sender Site \n");
my $mulValPrefLen4 = $ixNet->getAttribute($ipv6PrefixPools2, '-prefixLength');
$ixNet->setMultiAttribute($mulValPrefLen4.'/singleValue', '-value', '128');
$ixNet->commit();

print("Changing label value for IPv4/IPv6 in IPv4 Receiver Site-IPv6 Sender Site\n");
my $bgpL3VpnRouteProperty2 = ($ixNet->getList($ipv4PrefixPools2, 'bgpL3VpnRouteProperty'))[0];
my $bgp6L3VpnRouteProperty2 = ($ixNet->getList($ipv6PrefixPools2, 'bgpV6L3VpnRouteProperty'))[0];

my $label11 = $ixNet->getAttribute($bgpL3VpnRouteProperty2, '-labelStart');
$ixNet->setMultiAttribute($label11.'/counter',
        '-direction', 'increment',
        '-start',     '87710',
        '-step',      '10');
$ixNet->commit();

my $label21 = $ixNet->getAttribute($bgp6L3VpnRouteProperty2, '-labelStart');
$ixNet->setMultiAttribute($label21.'/counter',
        '-direction', 'increment',
        '-start',     '2765',
        '-step',      '10');
$ixNet->commit();

print("Disabling Receiver site and enabling Sender Site for IPv6 in Egress Topology\n");

$ixNet->setAttribute($bgp6L3VpnRouteProperty2, '-enableIpv6Sender', 'True');
$ixNet->setAttribute($bgp6L3VpnRouteProperty2, '-enableIpv6Receiver', 'False');
$ixNet->commit();

print("Disabling Sender site and enabling Receiver Site for IPv4 in Egress Topology\n");
$ixNet->setAttribute($bgpL3VpnRouteProperty2, '-enableIpv4Sender', 'False');
$ixNet->setAttribute($bgpL3VpnRouteProperty2, '-enableIpv4Receiver', 'True');
$ixNet->commit();

my $bgpMVpnSenderSitesIpv4 = ($ixNet->getList($ipv4PrefixPools1, 'bgpMVpnSenderSitesIpv4'))[0];
my $bgpMVpnSenderSitesIpv6 = ($ixNet->getList($ipv6PrefixPools2, 'bgpMVpnSenderSitesIpv6'))[0];
my $bgpMVpnReceiverSitesIpv4 = ($ixNet->getList($ipv4PrefixPools2, 'bgpMVpnReceiverSitesIpv4'))[0];
my $bgpMVpnReceiverSitesIpv6 = ($ixNet->getList($ipv6PrefixPools1, 'bgpMVpnReceiverSitesIpv6'))[0];

print("Changing Group Address Count for IPv4 Cloud in Sender Site \n");
my $mulValGCount = $ixNet->getAttribute($bgpMVpnSenderSitesIpv4, '-groupAddressCount');
$ixNet->setMultiAttribute($mulValGCount.'/singleValue', '-value', '4');
$ixNet->commit();

print("Changing Source Address Count for IPv4 Cloud in Sender Site \n");
my $mulValSCount = $ixNet->getAttribute($bgpMVpnSenderSitesIpv4, '-sourceAddressCount');
$ixNet->setMultiAttribute($mulValSCount.'/singleValue', '-value', '2');
$ixNet->commit();

print("Changing Group Address for IPv4 Cloud in Sender Site \n");
my $mulValGAdd = $ixNet->getAttribute($bgpMVpnSenderSitesIpv4, '-startGroupAddressIpv4');
$ixNet->setMultiAttribute($mulValGAdd.'/counter',
        '-direction', 'increment',
        '-start',     '234.161.1.1',
        '-step',      '0.1.0.0');
$ixNet->commit();

print("Changing Source Address for IPv4 Cloud in Sender Site \n");
my $mulValSAdd = $ixNet->getAttribute($bgpMVpnSenderSitesIpv4, '-startSourceAddressIpv4');
$ixNet->setMultiAttribute($mulValSAdd.'/counter',
        '-direction', 'increment',
        '-start',     '200.1.0.1',
        '-step',      '0.1.0.0');
$ixNet->commit();

print("Changing Group Address Count for IPv4 Cloud in Receiver Site \n");
my $mulValGCount1 = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv4, '-groupAddressCount');
$ixNet->setMultiAttribute($mulValGCount1.'/singleValue', '-value', '4');
$ixNet->commit();

print("Changing Source Address Count for IPv4 Cloud in Receiver Site \n");
my $mulValSCount1 = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv4, '-sourceAddressCount');
$ixNet->setMultiAttribute($mulValSCount1.'/singleValue', '-value', '2');
$ixNet->commit();

print("Changing Group Address for IPv4 Cloud in Receiver Site \n");
my $mulValGAdd1 = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv4, '-startGroupAddressIpv4');
$ixNet->setMultiAttribute($mulValGAdd1.'/counter',
        '-direction', 'increment',
        '-start',     '234.161.1.1',
        '-step',      '0.1.0.0');
$ixNet->commit();

print("Changing Source Address for IPv4 Cloud in Receiver Site \n");
my $mulValSAdd1 = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv4, '-startSourceOrCrpAddressIpv4');
$ixNet->setMultiAttribute($mulValSAdd1.'/counter',
        '-direction', 'increment',
        '-start',     '200.1.0.1',
        '-step',      '0.1.0.0');
$ixNet->commit();

print("Changing C-Multicast Route Type for IPv4 Cloud in Receiver Site \n");
my $mulValCMRType = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv4, '-cMulticastRouteType');
$ixNet->setMultiAttribute($mulValCMRType.'/singleValue', '-value', 'sharedtreejoin');
$ixNet->commit();

print("Changing Group Address Count for IPv6 Cloud in Sender Site \n");
my $mulValGCount2 = $ixNet->getAttribute($bgpMVpnSenderSitesIpv6, '-groupAddressCount');
$ixNet->setMultiAttribute($mulValGCount2.'/singleValue', '-value', '5');
$ixNet->commit();

print("Changing source Group Mapping for IPv6 Cloud in Sender Site \n");
my $mulValSGMap = $ixNet->getAttribute($bgpMVpnSenderSitesIpv6, '-sourceGroupMapping');
$ixNet->setMultiAttribute($mulValSGMap.'/singleValue', '-value', 'onetoone');
$ixNet->commit();

print("Changing Group Address for IPv6 Cloud in Sender Site \n");
my $mulValGAdd2 = $ixNet->getAttribute($bgpMVpnSenderSitesIpv6, '-startGroupAddressIpv6');
$ixNet->setMultiAttribute($mulValGAdd2,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($mulValGAdd2.'/counter',
        '-direction', 'increment',
        '-start',     'ff15:1:0:0:0:0:0:1',
        '-step',      '0:0:0:0:0:0:0:1');
$ixNet->commit();

print("Changing Source Address for IPv6 Cloud in Sender Site \n");
my $mulValSAdd2 = $ixNet->getAttribute($bgpMVpnSenderSitesIpv6, '-startSourceAddressIpv6');
$ixNet->setMultiAttribute($mulValSAdd2,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($mulValSAdd2.'/counter',
        '-direction', 'increment',
        '-start',     '3000:1:1:1:0:0:0:0',
        '-step',      '0:0:1:0:0:0:0:0');
$ixNet->commit();

print("Changing Group Address Count for IPv6 Cloud in Receiver Site \n");
my $mulValGCount22 = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv6, '-groupAddressCount');
$ixNet->setMultiAttribute($mulValGCount22.'/singleValue', '-value', '5');
$ixNet->commit();

print("Changing source Group Mapping for IPv6 Cloud in Receiver Site \n");
my $mulValSGMap = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv6, '-sourceGroupMapping');
$ixNet->setMultiAttribute($mulValSGMap.'/singleValue', '-value', 'onetoone');
$ixNet->commit();

print("Changing Group Address for IPv6 Cloud in Receiver Site \n");
my $mulValGAdd22 = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv6, '-startGroupAddressIpv6');
$ixNet->setMultiAttribute($mulValGAdd22,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($mulValGAdd22.'/counter',
        '-direction', 'increment',
        '-start',     'ff15:1:0:0:0:0:0:1',
        '-step',      '0:0:0:0:0:0:0:1');
$ixNet->commit();

print("Changing Source Address for IPv6 Cloud in Receiver Site \n");
my $mulValSAdd22 = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv6, '-startSourceAddressIpv6');
$ixNet->setMultiAttribute($mulValSAdd22,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($mulValSAdd22.'/counter',
        '-direction', 'increment',
        '-start',     '3000:1:1:1:0:0:0:0',
        '-step',      '0:0:1:0:0:0:0:0');
$ixNet->commit();

print("Changing Tunnel Type to mLDP for S-PMSI in IPv4 Address Pool in Sender Site\n");
my $bgpMVpnSenderSiteSpmsiV4 = ($ixNet->getList($bgpMVpnSenderSitesIpv4, 'bgpMVpnSenderSiteSpmsiV4'))[0];
my $mulValsPMSITunType = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV4, '-multicastTunnelType');
$ixNet->setMultiAttribute($mulValsPMSITunType.'/singleValue', '-value', 'tunneltypemldpp2mp');
$ixNet->commit();

print("Enabling Use Upstream/Downstream Assigned Label for S-PMSI in IPv4 Address Pool in Sender Sites\n");
my $mulValUpAsLabEn = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV4, '-useUpstreamOrDownstreamAssignedLabel');
$ixNet->setMultiAttribute($mulValUpAsLabEn,
     '-pattern', 'singleValue',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($mulValUpAsLabEn.'/singleValue',
        '-value', 'True');
$ixNet->commit();

print("Configuring the Upstream/Downstream Assigned Label for S-PMSI in IPv4 Address Pool in Sender Sites\n");
my $mulValUpAsLabel = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV4, '-upstreamOrDownstreamAssignedLabel');
$ixNet->setMultiAttribute($mulValUpAsLabel,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($mulValUpAsLabel.'/counter',
     '-step', '10', 
	 '-start', '14400', 
	 '-direction', 'increment');
$ixNet->commit();

print("Configuring Root Address for S-PMSI in IPv4 Address Pool in Sender Sites\n");
my $mulValRootAdd = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV4, '-sPmsirootAddress');
$ixNet->setMultiAttribute($mulValRootAdd.'/counter',
     '-step', '0.0.0.1', 
	 '-start', '8.8.8.7', 
	 '-direction', 'increment');
$ixNet->commit();

print("Changing Tunnel Count for S-PMSI in IPv4 Address Pool in Sender Site\n");
my $mulValsPMSITunCnt = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV4, '-sPmsiTunnelCount');
$ixNet->setMultiAttribute($mulValsPMSITunCnt.'/singleValue', '-value', '3');
$ixNet->commit();

print("Changing Type of TLV1 in S-PMSI mLDP Leaf range in IpV4 Sender Site\n");
my $type_s1 = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV4.'/pnTLVList:1', '-type');
$ixNet->setMultiAttribute($type_s1.'/singleValue', '-value', '111');
$ixNet->commit();

print("Changing Length of TLV1 in S-PMSI mLDP Leaf range in IpV4 Sender Site\n");
my $len_s1 = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV4.'/pnTLVList:1', '-tlvLength');
$ixNet->setMultiAttribute($len_s1.'/singleValue', '-value', '33');
$ixNet->commit();

print("Changing Value of TLV1 in S-PMSI mLDP Leaf range in IpV4 Sender Site\n");
my $val_s1 = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV4.'/pnTLVList:1', '-value');
$ixNet->setMultiAttribute($val_s1,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($val_s1.'/counter',
        '-direction', 'increment',
        '-start',     '000000000000000000000000000000000000000000000000000000000000007653',
        '-step',      '04');
$ixNet->commit();

print("Changing Increment of TLV1 in S-PMSI mLDP Leaf range in IpV4 Sender Site\n");
my $inc_s1 = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV4.'/pnTLVList:1', '-increment');
$ixNet->setMultiAttribute($inc_s1.'/singleValue', '-value', '000000000000000000000000000000000000000000000000000000000000000001');
$ixNet->commit();

print("Changing Tunnel Type to mLDP for S-PMSI in IPv6 Address Pool in Sender Site\n");
my $bgpMVpnSenderSiteSpmsiV6 = ($ixNet->getList($bgpMVpnSenderSitesIpv6, 'bgpMVpnSenderSiteSpmsiV6'))[0];
my $mulValsPMSIv6TunType = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV6, '-multicastTunnelType');
$ixNet->setMultiAttribute($mulValsPMSIv6TunType.'/singleValue', '-value', 'tunneltypemldpp2mp');
$ixNet->commit();

print("Enabling Use Upstream/Downstream Assigned Label for S-PMSI in IPv6 Address Pool in Sender Sites\n");
my $mulValUpAsLabEn_S = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV6, '-useUpstreamOrDownstreamAssignedLabel');
$ixNet->setMultiAttribute($mulValUpAsLabEn_S,
     '-pattern', 'singleValue',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($mulValUpAsLabEn_S.'/singleValue',
        '-value', 'True');
$ixNet->commit();

print("Configuring the Upstream/Downstream Assigned Label for S-PMSI in IPv6 Address Pool in Sender Sites\n");
my $mulValUpAsLabel_S = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV6, '-upstreamOrDownstreamAssignedLabel');
$ixNet->setMultiAttribute($mulValUpAsLabel_S,
     '-pattern', 'counter',
     '-clearOverlays', 'False');
$ixNet->setMultiAttribute($mulValUpAsLabel_S.'/counter',
     '-step', '10', 
	 '-start', '14400', 
	 '-direction', 'increment');
$ixNet->commit();

print("Configuring Root Address for S-PMSI in IPv6 Address Pool in Sender Sites\n");
my $mulValRootAddv6 = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV6, '-sPmsirootAddress');
$ixNet->setMultiAttribute($mulValRootAddv6.'/counter',
     '-step', '0.0.0.1', 
	 '-start', '7.7.7.7', 
	 '-direction', 'increment');
$ixNet->commit();

print("Changing Tunnel Count for S-PMSI in IPv6 Address Pool in Sender Site\n");
my $mulValsPMSITunCntv6 = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV6, '-sPmsiTunnelCount');
$ixNet->setMultiAttribute($mulValsPMSITunCntv6.'/singleValue', '-value', '3');
$ixNet->commit();

print("Changing Type of TLV1 in S-PMSI mLDP Leaf range in IpV6 Sender Site\n");
my $type_s2 = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV6.'/pnTLVList:1', '-type');
$ixNet->setMultiAttribute($type_s2.'/singleValue', '-value', '123');
$ixNet->commit();

print("Changing Length of TLV1 in S-PMSI mLDP Leaf range in IpV6 Sender Site\n");
my $len_s2 = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV6.'/pnTLVList:1', '-tlvLength');
$ixNet->setMultiAttribute($len_s2.'/singleValue', '-value', '5');
$ixNet->commit();

print("Changing Value of TLV1 in S-PMSI mLDP Leaf range in IpV6 Sender Site\n");
my $val_s2 = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV6.'/pnTLVList:1', '-value');
$ixNet->setMultiAttribute($val_s2.'/singleValue',
        '-value',     '00000000A4');
$ixNet->commit();

print("Changing Increment of TLV1 in S-PMSI mLDP Leaf range in IpV6 Sender Site\n");
my $inc_s2 = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV6.'/pnTLVList:1', '-increment');
$ixNet->setMultiAttribute($inc_s2.'/singleValue', '-value', '0000000001');
$ixNet->commit();

################################################################################
# 2. Start protocols.
################################################################################
print("Wait for 5 seconds before starting protocol \n");
sleep(5);
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
print("Fetching all Protocol Summary Statistics\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"BGP Peer Per Port"/page';
my @statcap  = $ixNet->getAttribute($viewPage, '-columnCaptions');
my @rowvals  = $ixNet->getAttribute($viewPage, '-rowValues');
my $index    = 0;
my $statValueList= '';
foreach $statValueList (@rowvals) {
    print("***************************************************\n");
    my $statVal = '';
    foreach $statVal (@$statValueList) {
        my $statIndiv = ''; 
        $index = 0;
        foreach $statIndiv (@$statVal) {
            printf(" %-30s:%s\n", $statcap[$index], $statIndiv);
            $index++;
        }
    }    
}
print("***************************************************\n");

###############################################################################
# 4. Retrieve IPv4/IPv6 mVPN learned info
###############################################################################
print("Fetching IPv4 mVPN Learned Info at Receiver side PE Router\n ");
$ixNet->execute('getIpv4MvpnLearnedInfo', $bgp2, '1');
print(" %%%%%%%%%%%%%%%%% Learned Info fetched\n ");
sleep(5);
print("IPv4 MVPN Learned Info at Receiver side PE Router\n ");
my $linfo  = ($ixNet->getList($bgp2, 'learnedInfo'))[0];

my @values = $ixNet->getAttribute($linfo, '-values');

print("***************************************************\n ");
my $v      = '';
foreach $v (@values) {
     my $w = '0';
    foreach $w (@$v) {
        printf("%10s", $w);
    }
    print("\n");
}
print("***************************************************\n ");

print("Fetching IPv6 mVPN Learned Info at Sender side PE Router\n ");
$ixNet->execute('getIpv6MvpnLearnedInfo', $bgp1, '1');
print(" %%%%%%%%%%%%%%%%% Learned Info fetched\n ");
sleep(5);
print("IPv6 MVPN Learned Info at Sender side PE Router\n ");
my $linfo  = ($ixNet->getList($bgp1, 'learnedInfo'))[0];

my @values = $ixNet->getAttribute($linfo, '-values');

print("***************************************************\n ");
my $v      = '';
foreach $v (@values) {
     my $w = '0';
    foreach $w (@$v) {
        printf("%10s", $w);
    }
    print("\n");
}
print("***************************************************\n ");

################################################################################
# 5. Apply changes on the fly.
################################################################################
print("Changing Source Address Count for IPv6 Cloud in Receiver Site\n ");
my $mulValSCount = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv6, '-sourceAddressCount');
$ixNet->setMultiAttribute($mulValSCount.'/singleValue', '-value', '4');
$ixNet->commit();
my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);

################################################################################
# 6. S-PMSI Trigger
################################################################################
print("Switching to S-PMSI for IPv4 Cloud from Sender Site\n ");
$ixNet->execute('switchToSpmsi', $bgpMVpnSenderSitesIpv4,1);
$ixNet->execute('switchToSpmsi', $bgpMVpnSenderSitesIpv4,2);
sleep(10);

###############################################################################
# 7. Retrieve protocol learned info after OTF
###############################################################################
print("Fetching IPv4 mVPN Learned Info\n ");
$ixNet->execute('getIpv4MvpnLearnedInfo', $bgp2, '1');
print(" %%%%%%%%%%%%%%%%% Learned Info fetched\n ");
sleep(5);
print("IPv4 MVPN Learned Info at receiver PE Router\n ");
my $linfo  = ($ixNet->getList($bgp1, 'learnedInfo'))[0];
my @values = $ixNet->getAttribute($linfo, '-values');
print("***************************************************\n ");
my $v      = '';
foreach $v (@values) {
     my $w = '0';
    foreach $w (@$v) {
        printf("%10s", $w);
    }
    print("\n");
}
print("***************************************************\n ");

################################################################################
# 8. Configure L2-L3 IPv6 I-PMSI traffic.
################################################################################
print("Configuring L2-L3 IPv6 I-PMSI Traffic Item\n ");
my $trafficItem1 = $ixNet->add($ixNet->getRoot().'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'NGMVPN I-PMSI Traffic 1',
    '-roundRobinPacketOrdering', 'false','-numVlansForMulticastReplication', '1', '-trafficType', 'ipv6', '-routeMesh', 'fullMesh');
$ixNet->commit();

$trafficItem1 = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my $destination  = ['$bgpMVpnReceiverSitesIpv6'];

$ixNet->setMultiAttribute($endpointSet1,
    '-name',                  'EndpointSet-1',
    '-sources',               $bgpMVpnSenderSitesIpv6,
    '-multicastDestinations', [['false','none', 'ff15:1:0:0:0:0:0:1', '0:0:0:0:0:0:0:1', '5']]);
$ixNet->commit();

$endpointSet1 = ($ixNet->remapIds($endpointSet1))[0];

$ixNet->setMultiAttribute($trafficItem1.'/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'mplsFlowDescriptor0', 'trackingenabled0', 'mplsMplsLabelValue0', 'ipv6DestIp0', 'ipv6SourceIp0']);
$ixNet->commit();

################################################################################
# 9. Configure L2-L3 IPv4 S-PMSI traffic.
################################################################################
print("Configuring L2-L3 IPv4 S-PMSI Traffic Item\n ");
my $trafficItem2 = $ixNet->add($ixNet->getRoot().'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem2, '-name', 'NGMVPN S-PMSI Traffic 2',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv4');
$ixNet->commit();

$trafficItem2 = ($ixNet->remapIds($trafficItem2))[0];
my $endpointSet2 = $ixNet->add($trafficItem2, 'endpointSet');
my $destination  = ['$bgpMVpnReceiverSitesIpv4'];

$ixNet->setMultiAttribute($endpointSet2,
    '-name',                  'EndpointSet-1',
    '-sources',               $bgpMVpnSenderSiteSpmsiV4,
    '-multicastDestinations', [['false','none','234.161.1.1','0.0.0.1','4'],['false','none','234.162.1.1','0.0.0.1','4']]);
$ixNet->commit();

$endpointSet2 = ($ixNet->remapIds($endpointSet2))[0];

$ixNet->setMultiAttribute($trafficItem2.'/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'ipv4DestIp0', 'ipv4SourceIp0', 'trackingenabled0', 'mplsFlowDescriptor0']);
$ixNet->commit();

###############################################################################
# 10. Apply and start L2/L3 traffic.
###############################################################################
print("applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

###############################################################################
# 11. Retrieve L2/L3 traffic item statistics.
###############################################################################
print("Verifying all the L2-L3 traffic stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"Flow Statistics"/page';
my @statcap  = $ixNet->getAttribute($viewPage, '-columnCaptions');
my @rowvals  = $ixNet->getAttribute($viewPage, '-rowValues');
my $index    = 0;
my $statValueList= '';
foreach $statValueList (@rowvals) {
    print("***************************************************\n");
    my $statVal = '';
    foreach $statVal (@$statValueList) {
	    my $statIndiv = ''; 
		$index = 0;
	    foreach $statIndiv (@$statVal) {
		    printf(" %-30s:%s\n", $statcap[$index], $statIndiv);
			$index++;
        }
    }    
}
print("***************************************************\n");

#################################################################################
# 12. Stop L2/L3 traffic.
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# 13. Stop all protocols.
################################################################################
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!\n");
