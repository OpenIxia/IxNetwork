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
#	 RSVPTE-P2MP. Both I-PMSI and S-PMSI tunnels for IPv4 & Ipv6 multicast  #
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
my $ixTclServer = '10.216.25.13';
my $ixTclPort   = '8990';
my @ports       = (('10.216.108.82', '7', '11'), ('10.216.108.82', '7', '12'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '8.10',
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
$ixNet->setAttribute($t1dev1, '-multiplier', '1');
$ixNet->setAttribute($t2dev1, '-multiplier', '1');
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

$ixNet->setAttribute($ixNet->getAttribute($mac2, '-mac').'/singleValue',
        '-value', '44:44:44:44:44:44');
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
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '50.50.50.2');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '50.50.50.1');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '50.50.50.1');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', '50.50.50.2');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
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

print("Adding IPv4 Address Pool in Topology1\n");
$ixNet->add($t1dev1, 'networkGroup');
$ixNet->add($t2dev1, 'networkGroup');
$ixNet->commit();

my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
my $networkGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];

print("Adding Linear Tree in Topology1\n");
$ixNet->add($ixNet->add($networkGroup1, 'networkTopology'),'netTopologyLinear');
$ixNet->commit();

$ixNet->setMultiAttribute($ixNet->remapIds(($ixNet->getList(($ixNet->getList($networkGroup1, 'networkTopology'), 'netTopologyLinear')))[0]), '-nodes', '5');
$ixNet->commit();

my $networkTopology1 = ($ixNet->getList($networkGroup1, 'networkTopology'));
$networkTopology1 = ($ixNet->remapIds($networkTopology1))[0];
$ixNet->commit();

print("Adding Linear Tree in Topology2\n");
$ixNet->add($ixNet->add($networkGroup2, 'networkTopology'),'netTopologyLinear');
$ixNet->commit();

$ixNet->setMultiAttribute($ixNet->remapIds(($ixNet->getList(($ixNet->getList($networkGroup2, 'networkTopology'), 'netTopologyLinear')))[0]), '-nodes', '5');
$ixNet->commit();

my $networkTopology2 = ($ixNet->getList($networkGroup2, 'networkTopology'));
$networkTopology2 = ($ixNet->remapIds($networkTopology2))[0];
$ixNet->commit();
my $netTopo1 = ($ixNet->getList($networkGroup1, 'networkTopology'))[0];
my $netTopo2 = ($ixNet->getList($networkGroup2, 'networkTopology'))[0];

print("Enabling Traffic Engineering in Network Ingress Topology \n");
my $simInterface1 = ($ixNet->getList($netTopo1, 'simInterface'))[0];
my $simInterfaceIPv4Config1 = ($ixNet->getList($simInterface1, 'simInterfaceIPv4Config'))[0];
my $ospfPseudoInterface1 = ($ixNet->getList($simInterfaceIPv4Config1, 'ospfPseudoInterface'))[0];
my $ospfPseudoInterface1_teEnable = $ixNet->getAttribute($ospfPseudoInterface1, '-enable');
$ixNet->setMultiAttribute($ospfPseudoInterface1_teEnable, '-clearOverlays', 'False', '-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($ospfPseudoInterface1_teEnable.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Enabling Traffic Engineering in Network Egress Topology \n");
my $simInterface2 = ($ixNet->getList($netTopo2, 'simInterface'))[0];
my $simInterfaceIPv4Config2 = ($ixNet->getList($simInterface2, 'simInterfaceIPv4Config'))[0];
my $ospfPseudoInterface2 = ($ixNet->getList($simInterfaceIPv4Config2, 'ospfPseudoInterface'))[0];
my $ospfPseudoInterface2_teEnable = $ixNet->getAttribute($ospfPseudoInterface2, '-enable');
$ixNet->setMultiAttribute($ospfPseudoInterface2_teEnable, '-clearOverlays', 'False', '-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($ospfPseudoInterface2_teEnable.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Renaming Network Topology \n");
$ixNet->setAttribute($networkGroup1, '-name', 'Sender PE Loopback');
$ixNet->setAttribute($networkGroup2, '-name', 'Receiver PE Loopback');
$ixNet->commit();

print("adding Chained DG behind IPv4 Address Pool in Ingress Topology \n");
my  $chainedDg1 = $ixNet->add($networkGroup1, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg1, '-multiplier', '1', '-name', 'Sender PE Router');
$ixNet->commit();

my $chainedDg1 = ($ixNet->remapIds($chainedDg1))[0];
my $loopback1 = $ixNet->add($chainedDg1, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback1, '-stackedLayers', [], '-name', 'IPv4 Loopback 1');
$ixNet->commit();

print("adding Chained DG behind Network topology in Egress Topology \n");
my $chainedDg2 = $ixNet->add($networkGroup2, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg2, '-multiplier', '1', '-name', 'Receiver PE Router');
$ixNet->commit();

$chainedDg2 = ($ixNet->remapIds($chainedDg2))[0];
my $loopback2 = $ixNet->add($chainedDg2, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback2, '-stackedLayers', [], '-name', 'IPv4 Loopback 2');
$ixNet->commit();

print("Adding RSVPTE P2MP LSPs over IPv4 Loopback 1 \n");
my $rsvpteLsps1 = $ixNet->add($loopback1, 'rsvpteLsps');
$ixNet->setMultiAttribute($rsvpteLsps1, '-ingressP2PLsps', '1', '-enableP2PEgress', 'true', '-p2mpIngressLspCount', '3', '-p2mpEgressTunnelCount', '0', '-name', 'RSVP-TE 1');
$ixNet->commit();

$rsvpteLsps1 = ($ixNet->remapIds($rsvpteLsps1))[0];

print("Adding RSVPTE P2MP LSPs over IPv4 Loopback 2 \n");
my $rsvpteLsps2 = $ixNet->add($loopback2, 'rsvpteLsps');
$ixNet->setMultiAttribute($rsvpteLsps2, '-ingressP2PLsps', '1', '-enableP2PEgress', 'true', '-p2mpIngressLspCount', '0', '-p2mpEgressTunnelCount', '3', '-name', 'RSVP-TE 2');
$ixNet->commit();

$rsvpteLsps2 = ($ixNet->remapIds($rsvpteLsps2))[0];

print("Editing P2MP ID in Ingress LSPs \n");
my $rsvpP2mpIngressLsps = ($ixNet->getList($rsvpteLsps1, 'rsvpP2mpIngressLsps'))[0];
my $p2mpIdAsNumber_ingress = $ixNet->getAttribute($rsvpP2mpIngressLsps, '-p2mpIdAsNumber');
$ixNet->setMultiAttribute($p2mpIdAsNumber_ingress, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$ixNet->setMultiAttribute($p2mpIdAsNumber_ingress.'/counter', '-step', '1', '-start', '1', '-direction', 'increment');
$ixNet->commit();

print("Editing P2MP ID in Egress LSPs \n");
my $rsvpP2mpEgressLsps = ($ixNet->getList($rsvpteLsps2, 'rsvpP2mpEgressLsps'))[0];
my $p2mpIdAsNumber_egress = $ixNet->getAttribute($rsvpP2mpEgressLsps, '-p2mpIdAsNumber');
$ixNet->setMultiAttribute($p2mpIdAsNumber_egress, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

my $p2mpIdAsNumber_egress_Custom = $ixNet->add($p2mpIdAsNumber_egress, 'custom');
$ixNet->setMultiAttribute($p2mpIdAsNumber_egress_Custom, '-step', '0', '-start', '1');
my $p2mpIdAsNumber_egress_Custom = ($ixNet->remapIds($p2mpIdAsNumber_egress_Custom))[0];

my $p2mpIdAsNumber_egress_Custom_inc = $ixNet->add($p2mpIdAsNumber_egress_Custom, 'increment');
$ixNet->setMultiAttribute($p2mpIdAsNumber_egress_Custom_inc, '-count', '2');
$ixNet->commit();

$p2mpIdAsNumber_egress_Custom = ($ixNet->remapIds($p2mpIdAsNumber_egress_Custom))[0];
$ixNet->commit();

print("Editing P2MP Ingress SubLSPs counter \n");
$ixNet->setAttribute($rsvpP2mpIngressLsps, '-ingressP2mpSubLspRanges', '5');
$ixNet->commit();

print("Editing Leaf IP in Ingress SubLSPs \n");
my $leafIp = $ixNet->getAttribute($rsvpteLsps1.'/rsvpP2mpIngressLsps/rsvpP2mpIngressSubLsps', '-leafIp');
$ixNet->setMultiAttribute($leafIp, '-clearOverlays', 'false');
$ixNet->commit();

my $custom_leaf = $ixNet->add($leafIp, 'custom');
$ixNet->setMultiAttribute($custom_leaf, '-step', '0.0.0.0', '-start', '3.2.2.2');
$ixNet->commit();
$custom_leaf = ($ixNet->remapIds($custom_leaf))[0];

my $increment_leaf = $ixNet->add($custom_leaf, 'increment');
$ixNet->setMultiAttribute($increment_leaf, '-count', '2', '-value', '0.0.0.1');
$ixNet->commit();

$increment_leaf = ($ixNet->remapIds($increment_leaf))[0];

print("Changing P2MP ID config/Type for RSVP-P2MP to IP for P2MP Ingress LSPs to use with I-PMSI & S-PMSI tunnel config \n");
$ixNet->setAttribute($rsvpteLsps1.'/rsvpP2mpIngressLsps', '-typeP2mpId', 'iP');
$ixNet->commit();

my $p2mpIdAsIp_ingress = $ixNet->getAttribute($rsvpteLsps1.'/rsvpP2mpIngressLsps', '-p2mpIdIp');
$ixNet->setMultiAttribute($p2mpIdAsIp_ingress, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$ixNet->setMultiAttribute($p2mpIdAsIp_ingress.'/counter', '-step', '0.0.0.1', '-start', '11.11.11.1', '-direction', 'increment');
$ixNet->commit();

print("Changing Tunnel Id for P2MP Ingress LSPs \n");

my $tunnelId_ingress = $ixNet->getAttribute($rsvpteLsps1.'/rsvpP2mpIngressLsps', '-tunnelId');
$ixNet->setMultiAttribute($tunnelId_ingress, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$ixNet->setMultiAttribute($tunnelId_ingress.'/counter', '-step', '0', '-start', '1', '-direction', 'increment');
$ixNet->commit();

print("Changing P2MP ID config/Type for RSVP-P2MP to IP for P2MP Egress LSPs to use with I-PMSI & S-PMSI tunnel config \n");
$ixNet->setAttribute($rsvpteLsps2.'/rsvpP2mpEgressLsps', '-typeP2mpId', 'iP');
$ixNet->commit();

my $p2mpIdAsIp_egress = $ixNet->getAttribute($rsvpteLsps2.'/rsvpP2mpEgressLsps', '-p2mpIdIp');
$ixNet->setMultiAttribute($p2mpIdAsIp_egress, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$ixNet->setMultiAttribute($p2mpIdAsIp_egress.'/counter', '-step', '0.0.0.1', '-start', '11.11.11.1', '-direction', 'increment');
$ixNet->commit();

print("Editing Leaf IP in Ingress SubLSPs \n");
my $leafIp = $ixNet->getAttribute($rsvpteLsps1.'/rsvpP2mpIngressLsps/rsvpP2mpIngressSubLsps', '-leafIp');
$ixNet->setMultiAttribute($leafIp, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$ixNet->setMultiAttribute($leafIp.'/singleValue', '-value', '3.2.2.2');
$ixNet->commit();

print("Assigning Remote IP to RSVPTE P2P LSPs under Ingress Topology \n");
my $remoteIp4Rsvp1 = $ixNet->getAttribute($rsvpteLsps1.'/rsvpP2PIngressLsps', '-remoteIp');
$ixNet->setMultiAttribute($remoteIp4Rsvp1, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$ixNet->setMultiAttribute($remoteIp4Rsvp1.'/counter', '-step', '0.0.0.1', '-start', '3.2.2.2', '-direction', 'increment');
$ixNet->commit();

print("Assigning Remote IP to RSVPTE P2P LSPs under Egress Topology \n");
my $remoteIp4Rsvp2 = $ixNet->getAttribute($rsvpteLsps2.'/rsvpP2PIngressLsps', '-remoteIp');
$ixNet->setMultiAttribute($remoteIp4Rsvp2, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$ixNet->setMultiAttribute($remoteIp4Rsvp2.'/counter', '-step', '0.0.0.1', '-start', '2.2.2.2', '-direction', 'increment');
$ixNet->commit();

print("Adding BGP over IPv4 loopback interfaces \n");
$ixNet->add($loopback1, 'bgpIpv4Peer');
$ixNet->add($loopback2, 'bgpIpv4Peer');
$ixNet->commit();
my $bgp1 = ($ixNet->getList($loopback1, 'bgpIpv4Peer'))[0];
my $bgp2 = ($ixNet->getList($loopback2, 'bgpIpv4Peer'))[0];
print("Setting IPs in BGP DUT IP tab \n");

$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-dutIp').'/singleValue', '-value', '3.2.2.2');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-dutIp').'/singleValue', '-value', '2.2.2.2');
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

print("Configuring RSVP P2MP ID value as IP in I-PMSI Tunnel in Egress Topology \n");
my $p2mpIdAsIp_pmsi1 = $ixNet->getAttribute($mVRF1, '-rsvpP2mpId');

my $p2mpIdAsIp_egress = $ixNet->getAttribute($rsvpteLsps2.'/rsvpP2mpEgressLsps', '-p2mpIdIp');
$ixNet->setMultiAttribute($p2mpIdAsIp_pmsi1, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$ixNet->setMultiAttribute($p2mpIdAsIp_pmsi1.'/counter', '-step', '0.0.0.0', '-start', '11.11.11.1', '-direction', 'increment');
$ixNet->commit();

print("Enabling  CheckBox for use of Up/DownStream Assigned Label for Ingress Topology \n");
$ixNet->setAttribute($ixNet->getAttribute($mVRF1, '-useUpOrDownStreamAssigneLabel').'/singleValue', '-value', 'True');
$ixNet->commit();

print("Assigning value for Up/DownStream Assigned Label for Ingress Topology \n");
$ixNet->setAttribute($ixNet->getAttribute($mVRF1, '-upOrDownStreamAssignedLabel').'/singleValue', '-value', '10001');
$ixNet->commit();

print("Adding Network Group behind mVRF for Ingress Topology \n");
$ixNet->add($chainedDg1, 'networkGroup');
$ixNet->commit();
my $networkGroup3 = ($ixNet->getList($chainedDg1, 'networkGroup'))[0];
$ixNet->setAttribute($networkGroup3, '-name', 'Sender Site');
$ixNet->commit();

print("Adding Network Group behind mVRF for Egress Topology \n");
$ixNet->add($chainedDg2, 'networkGroup');
$ixNet->commit();
my $networkGroup4 = ($ixNet->getList($chainedDg2, 'networkGroup'))[0];
$ixNet->setAttribute($networkGroup4, '-name', 'Receiver Site');
$ixNet->commit();

print("Adding IPv4/IPv6 Prefix pools in Ingress Topology behind Sender PE router \n");
$ixNet->add($networkGroup3, 'ipv4PrefixPools');
$ixNet->commit();

$ixNet->add($networkGroup3, 'ipv6PrefixPools');
$ixNet->commit();


print("Adding IPv4/IPv6 Prefix pools in Egress Topology behind Receiver PE router \n");
$ixNet->add($networkGroup4, 'ipv4PrefixPools');
$ixNet->commit();

$ixNet->add($networkGroup4, 'ipv6PrefixPools');
$ixNet->commit();

print("Disabling Sender site and enabling Receiver Site for both IPv4 in Egress Topology \n");
my $ipv4PrefixPools4 = ($ixNet->getList($networkGroup4, 'ipv4PrefixPools'))[0];
my $bgpL3VpnRouteProperty4 = ($ixNet->getList($ipv4PrefixPools4, 'bgpL3VpnRouteProperty'))[0];

$ixNet->setAttribute($bgpL3VpnRouteProperty4, '-enableIpv4Sender', 'False');
$ixNet->setAttribute($bgpL3VpnRouteProperty4, '-enableIpv4Receiver', 'True');
$ixNet->commit();


print("Disabling Sender site and enabling Receiver Site for both IPv6 in Egress Topology \n");
my $ipv6PrefixPools4 = ($ixNet->getList($networkGroup4, 'ipv6PrefixPools'))[0];
my $bgpV6L3VpnRouteProperty = ($ixNet->getList($ipv6PrefixPools4, 'bgpV6L3VpnRouteProperty'))[0];

$ixNet->setAttribute($bgpV6L3VpnRouteProperty, '-enableIpv6Sender', 'False');
$ixNet->setAttribute($bgpV6L3VpnRouteProperty, '-enableIpv6Receiver', 'True');
$ixNet->commit();

print("Enabling UMH Route check box in Sender Site \n");
my $ipv4PrefixPools3 = ($ixNet->getList($networkGroup3, 'ipv4PrefixPools'))[0];
my $ipv6PrefixPools3 = ($ixNet->getList($networkGroup3, 'ipv6PrefixPools'))[0];
my $bgpL3VpnRouteProperty3 = ($ixNet->getList($ipv4PrefixPools3, 'bgpL3VpnRouteProperty'))[0];
my $bgpV6L3VpnRouteProperty3 = ($ixNet->getList($ipv6PrefixPools3, 'bgpV6L3VpnRouteProperty'))[0];
$ixNet->setAttribute($bgpL3VpnRouteProperty3, '-useAsIpv4UmhRoutes', 'True');
$ixNet->setAttribute($bgpV6L3VpnRouteProperty3, '-useAsIpv6UmhRoutes', 'True');
$ixNet->commit();

my $bgpMVpnSenderSitesIpv4 = ($ixNet->getList($ipv4PrefixPools3, 'bgpMVpnSenderSitesIpv4'))[0];
my $ipv6PrefixPools3 = ($ixNet->getList($networkGroup3, 'ipv6PrefixPools'))[0];
my $bgpMVpnSenderSitesIpv6 = ($ixNet->getList($ipv6PrefixPools3, 'bgpMVpnSenderSitesIpv6'))[0];
my $bgpMVpnReceiverSitesIpv4 = ($ixNet->getList($ipv4PrefixPools4, 'bgpMVpnReceiverSitesIpv4'))[0];
my $bgpMVpnReceiverSitesIpv6 = ($ixNet->getList($ipv6PrefixPools4, 'bgpMVpnReceiverSitesIpv6'))[0];

print("Changing Group Address Count for IPv4 Cloud in Sender Site \n");
my $mulValGCount = $ixNet->getAttribute($bgpMVpnSenderSitesIpv4, '-groupAddressCount');
$ixNet->setMultiAttribute($mulValGCount.'/singleValue', '-value', '5');
$ixNet->commit();

print("Changing Source Address Count for IPv4 Cloud in Sender Site \n");
my $mulValSCount = $ixNet->getAttribute($bgpMVpnSenderSitesIpv4, '-sourceAddressCount');
$ixNet->setMultiAttribute($mulValSCount.'/singleValue', '-value', '3');
$ixNet->commit();

print("Changing Group Address for IPv4 Cloud in Sender Site \n");
my $mulValGAdd = $ixNet->getAttribute($bgpMVpnSenderSitesIpv4, '-startGroupAddressIpv4');
$ixNet->setMultiAttribute($mulValGAdd.'/singleValue', '-value', '234.161.1.1');
$ixNet->commit();

print("Changing Source Address for IPv4 Cloud in Sender Site \n");
my $mulValSAdd = $ixNet->getAttribute($bgpMVpnSenderSitesIpv4, '-startSourceAddressIpv4');
$ixNet->setMultiAttribute($mulValSAdd.'/singleValue', '-value', '191.0.1.1');
$ixNet->commit();

print("Changing Group Address Count for IPv4 Cloud in Receiver Site \n");
my $mulValGCount = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv4, '-groupAddressCount');
$ixNet->setMultiAttribute($mulValGCount.'/singleValue', '-value', '5');
$ixNet->commit();

print("Changing Source Address Count for IPv4 Cloud in Receiver Site \n");
my $mulValSCount = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv4, '-sourceAddressCount');
$ixNet->setMultiAttribute($mulValSCount.'/singleValue', '-value', '3');
$ixNet->commit();

print("Changing Group Address for IPv4 Cloud in Receiver Site \n");
my $mulValGAdd = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv4, '-startGroupAddressIpv4');
$ixNet->setMultiAttribute($mulValGAdd.'/singleValue', '-value', '234.161.1.1');
$ixNet->commit();

print("Changing Source Address for IPv4 Cloud in Receiver Site \n");
my $mulValSAdd = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv4, '-startSourceOrCrpAddressIpv4');
$ixNet->setMultiAttribute($mulValSAdd.'/singleValue', '-value', '191.0.1.1');
$ixNet->commit();

print("Changing C-Multicast Route Type for IPv4 Cloud in Receiver Site \n");
my $mulValCMRType = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv4, '-cMulticastRouteType');
$ixNet->setMultiAttribute($mulValCMRType.'/singleValue', '-value', 'sharedtreejoin');
$ixNet->commit();

print("Changing Group Address Count for IPv6 Cloud in Sender Site \n");
my $mulValGCount = $ixNet->getAttribute($bgpMVpnSenderSitesIpv6, '-groupAddressCount');
$ixNet->setMultiAttribute($mulValGCount.'/singleValue', '-value', '5');
$ixNet->commit();

print("Changing source Group Mapping for IPv6 Cloud in Sender Site \n");
my $mulValSGMap = $ixNet->getAttribute($bgpMVpnSenderSitesIpv6, '-sourceGroupMapping');
$ixNet->setMultiAttribute($mulValSGMap.'/singleValue', '-value', 'onetoone');
$ixNet->commit();

print("Changing Group Address for IPv6 Cloud in Sender Site \n");
my $mulValGAdd = $ixNet->getAttribute($bgpMVpnSenderSitesIpv6, '-startGroupAddressIpv6');
$ixNet->setMultiAttribute($mulValGAdd.'/singleValue', '-value', 'ff15:1:0:0:0:0:0:1');
$ixNet->commit();

print("Changing Source Address for IPv6 Cloud in Sender Site \n");
my $mulValSAdd = $ixNet->getAttribute($bgpMVpnSenderSitesIpv6, '-startSourceAddressIpv6');
$ixNet->setMultiAttribute($mulValSAdd.'/singleValue', '-value', '5001:1:0:0:0:0:0:1');
$ixNet->commit();

my $bgpMVpnReceiverSitesIpv4 = ($ixNet->getList($ipv4PrefixPools4, 'bgpMVpnReceiverSitesIpv4'))[0];
my $bgpMVpnReceiverSitesIpv6 = ($ixNet->getList($ipv6PrefixPools4, 'bgpMVpnReceiverSitesIpv6'))[0];

print("Changing Group Address Count for IPv6 Cloud in Receiver Site \n");
my $mulValGCount = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv6, '-groupAddressCount');
$ixNet->setMultiAttribute($mulValGCount.'/singleValue', '-value', '5');
$ixNet->commit();

print("Changing source Group Mapping for IPv6 Cloud in Receiver Site \n");
my $mulValSGMap = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv6, '-sourceGroupMapping');
$ixNet->setMultiAttribute($mulValSGMap.'/singleValue', '-value', 'onetoone');
$ixNet->commit();

print("Changing Group Address for IPv6 Cloud in Receiver Site \n");
my $mulValGAdd = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv6, '-startGroupAddressIpv6');
$ixNet->setMultiAttribute($mulValGAdd.'/singleValue', '-value', 'ff15:1:0:0:0:0:0:1');
$ixNet->commit();

print("Changing Source Address for IPv6 Cloud in Receiver Site \n");
my $mulValSAdd = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv6, '-startSourceOrCrpAddressIpv6');
$ixNet->setMultiAttribute($mulValSAdd.'/singleValue', '-value', '5001:1:0:0:0:0:0:1');
$ixNet->commit();

print("Changing Address for IPv4 Address Pool in Sender Site \n");
my $mulValIpAdd = $ixNet->getAttribute($ipv4PrefixPools3, '-networkAddress');
$ixNet->setMultiAttribute($mulValIpAdd.'/singleValue', '-value', '191.0.1.1');
$ixNet->commit();

print("Changing Prefix Length for IPv4 Address Pool in Sender Site \n");
my $mulValPrefLen = $ixNet->getAttribute($ipv4PrefixPools3, '-prefixLength');
$ixNet->setMultiAttribute($mulValPrefLen.'/singleValue', '-value', '32');
$ixNet->commit();

print("Changing Address Count Address Pool in Sender Site \n");
$ixNet->setAttribute($ipv4PrefixPools3, '-numberOfAddresses', '3');
$ixNet->commit();

print("Changing Address for IPv6 Address Pool in Sender Site \n");
my $mulValIpAdd = $ixNet->getAttribute($ipv6PrefixPools3, '-networkAddress');
$ixNet->setMultiAttribute($mulValIpAdd.'/singleValue', '-value', '5001:1:0:0:0:0:0:1');
$ixNet->commit();

print("Changing Prefix Length for IPv6 Address Pool in Sender Site \n");
my $mulValPrefLen = $ixNet->getAttribute($ipv6PrefixPools3, '-prefixLength');
$ixNet->setMultiAttribute($mulValPrefLen.'/singleValue', '-value', '128');
$ixNet->commit();

print("Changing Address Count Address Pool in Sender Site \n");
$ixNet->setAttribute($ipv6PrefixPools3, '-numberOfAddresses', '5');
$ixNet->commit();

print("Configuring S-PMSI on Sender Sites \n");
my $bgpMVpnSenderSiteSpmsiV4 = ($ixNet->getList($bgpMVpnSenderSitesIpv4, 'bgpMVpnSenderSiteSpmsiV4'))[0];
my $mulValp2mpId = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV4, '-sPmsiRsvpP2mpId');
$ixNet->setMultiAttribute($mulValp2mpId.'/singleValue', '-value', '11.11.11.2');
$ixNet->commit();

print("Changing RSVP TunnelId Step for S-PMSI in IPv4 Address Pool in Sender Site \n");
my $mulValsPMSIRsvpTunId = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV4, '-sPmsiRsvpTunnelIdStep');
$ixNet->setMultiAttribute($mulValsPMSIRsvpTunId.'/singleValue', '-value', '0');
$ixNet->commit();

print("Changing RSVP Tunnel Count for S-PMSI in IPv4 Address Pool in Ingress Topology \n");
my $mulValsPMSTidCnt = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV4, '-sPmsiTunnelCount');
$ixNet->setMultiAttribute($mulValsPMSTidCnt.'/singleValue', '-value', '2');
$ixNet->commit();

my $bgpMVpnSenderSiteSpmsiV6 = ($ixNet->getList($bgpMVpnSenderSitesIpv6, 'bgpMVpnSenderSiteSpmsiV6'))[0];

print("Changing RSVP P2MP Id for S-PMSI in IPv6 Address Pool in Sender Site \n");
my $mulValp2mpId = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV6, '-sPmsiRsvpP2mpId');
$ixNet->setMultiAttribute($mulValp2mpId.'/singleValue', '-value', '11.11.11.2');
$ixNet->commit();

print("Changing RSVP TunnelId Step for S-PMSI in IPv6 Address Pool  in Sender Site \n");
my $mulValsPMSIRsvpTunId = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV6, '-sPmsiRsvpTunnelIdStep');
$ixNet->setMultiAttribute($mulValsPMSIRsvpTunId.'/singleValue', '-value', '0');
$ixNet->commit();

print("Changing RSVP Tunnel Count for S-PMSI in IPv6 Address Pool  in Sender Site \n");
my $mulValsPMSTidCnt = $ixNet->getAttribute($bgpMVpnSenderSiteSpmsiV6, '-sPmsiTunnelCount');
$ixNet->setMultiAttribute($mulValsPMSTidCnt.'/singleValue', '-value', '2');
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
# 4. Retrieve IPv4 mVPN learned info
###############################################################################
print("Fetching mVPN Learned Info\n ");
$ixNet->execute('getIpv4MvpnLearnedInfo', $bgp1, '1');
print(" %%%%%%%%%%%%%%%%% Learned Info fetched\n ");
sleep(5);
print("IPv4 MVPN Learned Info at Sender PE Router\n ");
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

print("Fetching IPv6 UMH Learned Info at Receiver PE Router\n ");
$ixNet->execute('getIpv6UmhRoutesLearnedInfo', $bgp2, '1');
print("IPv6 UMH Learned Info at Receiver PE Router\n ");
sleep(5);
my $linfo  = ($ixNet->getList($bgp2, 'learnedInfo'))[0];

my @values = $ixNet->getAttribute($linfo, '-values');

print("***************************************************\n ");
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
print("Changing C-Multicast Route Type for IPv6 Cloud in Receiver Site\n ");

print("Changing C-Multicast Route Type for IPv4 Cloud in Receiver Site\n ");
my $mulValCMRType = $ixNet->getAttribute($bgpMVpnReceiverSitesIpv6, '-cMulticastRouteType');
$ixNet->setMultiAttribute($mulValCMRType.'/singleValue', '-value', 'sharedtreejoin');
$ixNet->commit();
my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);

################################################################################
# 6. S-PMSI Trigger
################################################################################
print("Switching to S-PMSI for IPv6 Cloud from Sender Site\n ");
$ixNet->execute('switchToSpmsi', $bgpMVpnSenderSitesIpv6,1);
sleep(10);

###############################################################################
# 7. Retrieve protocol learned info after OTF
###############################################################################
print("Fetching IPv6 mVPN Learned Info\n ");
$ixNet->execute('getIpv6MvpnLearnedInfo', $bgp1, '1');
print(" %%%%%%%%%%%%%%%%% Learned Info fetched\n ");
sleep(5);
print("IPv6 MVPN Learned Info at Sender PE Router\n ");
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
# 8. Configure L2-L3 IPv4 I-PMSI traffic.
################################################################################
print("Configuring L2-L3 IPv4 I-PMSI Traffic Item\n ");
my $trafficItem1 = $ixNet->add($ixNet->getRoot().'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'NGMVPN I-PMSI Traffic 1',
    '-roundRobinPacketOrdering', 'false','-numVlansForMulticastReplication', '1', '-trafficType', 'ipv4', '-routeMesh', 'fullMesh');
$ixNet->commit();

$trafficItem1 = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my $destination  = ['$bgpMVpnReceiverSitesIpv4'];

$ixNet->setMultiAttribute($endpointSet1,
    '-name',                  'EndpointSet-1',
    '-sources',               $bgpMVpnSenderSitesIpv4,
    '-multicastDestinations', [['false','none','234.161.1.1','0.0.0.1','5']]);
$ixNet->commit();

$endpointSet1 = ($ixNet->remapIds($endpointSet1))[0];

$ixNet->setMultiAttribute($trafficItem1.'/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'mplsFlowDescriptor0', 'trackingenabled0', 'mplsMplsLabelValue0', 'ipv4DestIp0', 'ipv4SourceIp0']);
$ixNet->commit();

################################################################################
# 9. Configure L2-L3 IPv6 S-PMSI traffic.
################################################################################
print("Configuring L2-L3 IPv6 S-PMSI Traffic Item\n ");
my $trafficItem2 = $ixNet->add($ixNet->getRoot().'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem2, '-name', 'NGMVPN S-PMSI Traffic 2',
    '-roundRobinPacketOrdering', 'false', '-trafficType', 'ipv6');
$ixNet->commit();

$trafficItem2 = ($ixNet->remapIds($trafficItem2))[0];
my $endpointSet2 = $ixNet->add($trafficItem2, 'endpointSet');
my $destination  = ['$bgpMVpnReceiverSitesIpv6'];

$ixNet->setMultiAttribute($endpointSet2,
    '-name',                  'EndpointSet-1',
    '-sources',               $bgpMVpnSenderSiteSpmsiV6,
    '-multicastDestinations', [['false','none','ff15:1:0:0:0:0:0:1','0:0:0:0:0:0:0:1','5']]);
$ixNet->commit();

$endpointSet2 = ($ixNet->remapIds($endpointSet2))[0];

$ixNet->setMultiAttribute($trafficItem2.'/tracking',
    '-trackBy',        ['sourceDestEndpointPair0', 'ipv6DestIp0', 'ipv6SourceIp0', 'trackingenabled0', 'mplsFlowDescriptor0']);
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
