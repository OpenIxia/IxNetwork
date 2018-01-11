################################################################################
# Version 1.0    $Revision: #1 $                                               #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    23/06/2016 - Debarati Chakraborty - created sample                        #
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
#       Within topology both Label Switch Router(LSR) and Label Edge Router(LER)#
#    are created. LSR is emulated in the front Device Group(DG), which consists #
#    of both OSPF as routing protocol as well as RSVPTE-IF for Label            # 
#    Distribution Protocol. The chained DG act as LER, where RSVP-TE P2MP LSPs  #
#    are configured. Unidirectional L2-L3 Traffic from Ingress to Egress is     #
#    created.                                                                   #
#         Script Flow:                                                          #
#        Step 1. Configuration of protocols.                                    #
#    Configuration flow of the script is as follow:                             #
#             i.      Adding of OSPF router                                     #
#             ii.     Adding of Network Topology(NT)                            #
#             iii.    Enabling of TE(Traffic Engineering)                       #
#             iv.     Adding of chain DG                                        #
#             v.      Adding of RSVP-TE LSPs within chain DG                    #
#        Step 2. Start of protocol                                              #
#        Step 3. Protocol Stat display                                          #
#        Step 4. Learned Info display                                           #
#        Step 5. On The Fly(OTF) change of protocol parameter.                  #
#        Step 6. Again Learned Info display to see OTF changes take place       #
#        Step 7. Configuration L2-L3 Traffic                                    #
#        Step 8. Apply and Start of L2-L3 traffic                               #
#        Step 9. Display of L2-L3  traffic Stats                                #
#        Step 10.Stop of L2-L3 traffic                                          #
#        Step 11.Stop of all protocols                                          #
#################################################################################
# Ixia Software Used to develop the script:                                     #
#    IxOS      8.10 EA                                                          #
#    IxNetwork 8.10 EA                                                          #
#                                                                               #
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
my $ixTclServer = '10.216.104.58';
my $ixTclPort   = '8239';
my @ports       = (('10.216.108.82', '7', '15'), ('10.216.108.82', '7', '16'));
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

# Creating topology and device group
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
$ixNet->setAttribute($topo1,  '-name', 'RSVPTE P2MP Topology 1');
$ixNet->setAttribute($topo2,  '-name', 'RSVPTE P2MP Topology 2');
$ixNet->commit();
my $t1dev1 = $t1devices[0];
my $t2dev1 = $t2devices[0];
$ixNet->setAttribute($t1dev1, '-name', 'Label Switch Router 1');
$ixNet->setAttribute($t2dev1, '-name', 'Label Switch Router 2');
$ixNet->commit();

print("Configuring the multipliers (number of sessions)\n");
$ixNet->setAttribute($t1dev1, '-multiplier', '1');
$ixNet->setAttribute($t2dev1, '-multiplier', '1');
$ixNet->commit();

#  Adding ethernet stack and configuring MAC

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

#  Adding IPv4 stack and configuring  IP Address
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
#  Adding OSPF and configuring it
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

# Adding Network Topology behind Device Group
print("Adding IPv4 Address Pool in Topology1\n");
$ixNet->add($t1dev1, 'networkGroup');
$ixNet->add($t2dev1, 'networkGroup');
$ixNet->commit();

my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
my $networkGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];

$ixNet->add($networkGroup1, 'ipv4PrefixPools');
$ixNet->commit();

my $ipv4PrefixPools1 = ($ixNet->getList($networkGroup1, 'ipv4PrefixPools'));
$ixNet->commit();

print("Adding Linear Tree in Topology2\n");
$ixNet->add($ixNet->add($networkGroup2, 'networkTopology'),'netTopologyLinear');
$ixNet->commit();

$ixNet->setMultiAttribute($ixNet->remapIds(($ixNet->getList(($ixNet->getList($networkGroup2, 'networkTopology'), 'netTopologyLinear')))[0]), '-nodes', '5');
$ixNet->commit();

my $networkTopology1 = ($ixNet->getList($networkGroup2, 'networkTopology'));
$networkTopology1 = ($ixNet->remapIds($networkTopology1))[0];
$ixNet->commit();

my $netTopo1 = ($ixNet->getList($networkGroup1, 'ipv4PrefixPools'))[0];
my $netTopo2 = ($ixNet->getList($networkGroup2, 'networkTopology'))[0];

# Configuring Traffic Engineering
print("Enabling Traffic Engineering in Network Topology\n");
my $simInterface1 = ($ixNet->getList($netTopo2, 'simInterface'))[0];
my $simInterfaceIPv4Config1 = ($ixNet->getList($simInterface1, 'simInterfaceIPv4Config'))[0];
my $ospfPseudoInterface1 = ($ixNet->getList($simInterfaceIPv4Config1, 'ospfPseudoInterface'))[0];
my $ospfPseudoInterface1_teEnable = $ixNet->getAttribute($ospfPseudoInterface1, '-enable');
$ixNet->setMultiAttribute($ospfPseudoInterface1_teEnable, '-clearOverlays', 'False', '-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($ospfPseudoInterface1_teEnable.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Configuring the multipliers (number of sessions)\n");
$ixNet->setAttribute($networkGroup1, '-multiplier', '2');
$ixNet->setAttribute($networkGroup2, '-multiplier', '2');
$ixNet->commit();

# Adding Chained Device Group Behind front Device Group for IPv4 loopback
print("Adding Chained DG behind Network Topology in Topology 1\n");
my $chainedDg1 = $ixNet->add($networkGroup1, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg1, '-multiplier', '1', '-name', 'Edge Router 1');
$ixNet->commit();
$chainedDg1 = ($ixNet->remapIds($chainedDg1))[0];
my $loopback1 = $ixNet->add($chainedDg1, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback1, '-stackedLayers', '', '-name', 'IPv4 Loopback 1');
$ixNet->commit();

print("Adding Chained DG behind Network Topology in Topology 2\n");
my $chainedDg2 = $ixNet->add($networkGroup2, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg2, '-multiplier', '1', '-name', 'Edge Router 2');
$ixNet->commit();
$chainedDg2 = ($ixNet->remapIds($chainedDg2))[0];
my $loopback2 = $ixNet->add($chainedDg2, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback2, '-stackedLayers', '', '-name', 'IPv4 Loopback 2');
$ixNet->commit();

# Adding RSVPTE P2MP over IPv4 stack and configuring related parameters
print("Adding RSVPTE P2MP router over 'IPv4 Loopback 1'\n");
my $rsvpteLsps1 = $ixNet->add($loopback1, 'rsvpteLsps');
$ixNet->setMultiAttribute($rsvpteLsps1, '-ingressP2PLsps', '0', '-enableP2PEgress', 'False', '-p2mpIngressLspCount', '1', '-p2mpEgressTunnelCount', '0');
$ixNet->commit();
$rsvpteLsps1 = ($ixNet->remapIds($rsvpteLsps1))[0];

print("Adding RSVPTE P2MP router over 'IPv4 Loopback 2'\n");
my $rsvpteLsps2 = $ixNet->add($loopback2, 'rsvpteLsps');
$ixNet->setMultiAttribute($rsvpteLsps2, '-ingressP2PLsps', '0', '-enableP2PEgress', 'False', '-p2mpIngressLspCount', '0', '-p2mpEgressTunnelCount', '5');
$ixNet->commit();
$rsvpteLsps2 = ($ixNet->remapIds($rsvpteLsps2))[0];

#Edit P2MP ID in Ingress and Egress LSPs
print("Editing P2MP ID in Ingress and Egress LSPs\n");
#my $rsvpP2mpIngressLsps = ($ixNet->getList($rsvpteLsps1, 'rsvpP2mpIngressLsps'))[0];
my $p2mpIdAsNumber_ingress = $ixNet->getAttribute($rsvpteLsps1.'/rsvpP2mpIngressLsps', '-p2mpIdAsNumber');
$ixNet->commit();
$ixNet->setMultiAttribute($p2mpIdAsNumber_ingress, '-clearOverlays', 'False', '-pattern', 'counter');
$ixNet->commit();
$ixNet->setMultiAttribute($p2mpIdAsNumber_ingress.'/counter', '-step', '1', '-start', '1', '-direction', 'increment');
$ixNet->commit();

my $rsvpP2mpEgressLsps = ($ixNet->getList($rsvpteLsps2, 'rsvpP2mpEgressLsps'))[0];
my $p2mpIdAsNumber_egress = $ixNet->getAttribute($rsvpteLsps2.'/rsvpP2mpEgressLsps', '-p2mpIdAsNumber');
$ixNet->setMultiAttribute($p2mpIdAsNumber_egress, '-clearOverlays', 'False', '-pattern', 'custom');
$ixNet->commit();

my $custom = $ixNet->add($p2mpIdAsNumber_egress, 'custom');
$ixNet->setMultiAttribute($custom, '-step', '9', '-start', '1');
$ixNet->commit();
$custom = ($ixNet->remapIds($custom))[0];

my $inc1 = $ixNet->add($custom, 'increment');
$ixNet->setMultiAttribute($inc1, '-count', '2', '-value', '1');
$ixNet->commit();
$inc1 = ($ixNet->remapIds($inc1))[0];
$ixNet->commit();

#Edit P2MP Ingress SubLSPs counter
print("Editing P2MP Ingress SubLSPs counter\n");
$ixNet->setAttribute($rsvpteLsps1.'/rsvpP2mpIngressLsps', '-ingressP2mpSubLspRanges', '5');
$ixNet->commit();

#Edit Leaf IP in Ingress SubLSPs
print("Editing Leaf IP in Ingress SubLSPs\n");
my $leafIp = $ixNet->getAttribute($rsvpteLsps1.'/rsvpP2mpIngressLsps'.'/rsvpP2mpIngressSubLsps', '-leafIp');
$ixNet->setMultiAttribute($leafIp, '-clearOverlays', 'False');
$ixNet->commit();

my $custom_leaf = $ixNet->add($leafIp, 'custom');
$ixNet->setMultiAttribute($custom_leaf, '-step', '0.0.0.0', '-start', '3.2.2.2');
$ixNet->commit();
$custom_leaf = ($ixNet->remapIds($custom_leaf))[0];

my $increment_leaf = $ixNet->add($custom_leaf, 'increment');
$ixNet->setMultiAttribute($increment_leaf, '-count', '2', '-value', '0.0.0.1');
$ixNet->commit();
$increment_leaf = ($ixNet->remapIds($increment_leaf))[0];

print("************************************************************\n");
################################################################################
# Step 2> Start of protocol.
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);
################################################################################
# Step 3> Retrieve protocol statistics.
################################################################################
print("Fetching all Protocol Summary Statistics\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page';
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
# Step 4> Retrieve protocol learned info
###############################################################################
print("Fetching RSVPTE P2MP Received learned Info\n");
my $rsvpteIf1 = ($ixNet->getList($ip1, 'rsvpteIf'))[0];
$ixNet->execute('getLearnedInfo', $rsvpteIf1, '1');
sleep(5);
my $linfo  = ($ixNet->getList($rsvpteIf1, 'learnedInfo'))[3];
my @values = $ixNet->getAttribute($linfo, '-values');
my $v      = '';
print("***************************************************\n");
foreach $v (@values) {
     my $w = '0';
    foreach $w (@$v) {
        printf("%10s", $w);
    }
    print("\n");
}
print("***************************************************\n");
################################################################################
# Step 5> Apply changes on the fly.
################################################################################
print("Changing Label Value for first RSVPTE router to single value in Topology 1 \n");
my $labelSpaceStartMultValue1 = $ixNet->getAttribute($rsvpteIf1, '-labelSpaceStart');
$ixNet->setMultiAttribute($labelSpaceStartMultValue1, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($labelSpaceStartMultValue1.'/singleValue', '-value', '8000');
$ixNet->commit();
my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);
################################################################################
# Step 6> Retrieve protocol learned info again and compare with.
################################################################################
print("Fetching RSVPTE P2MP Received learned Info\n");
my $rsvpteIf1 = ($ixNet->getList($ip1, 'rsvpteIf'))[0];
$ixNet->execute('getLearnedInfo', $rsvpteIf1, '1');
sleep(5);
my $linfo  = ($ixNet->getList($rsvpteIf1, 'learnedInfo'))[3];
my @values = $ixNet->getAttribute($linfo, '-values');
my $v      = '';
print("***************************************************\n");
foreach $v (@values) {
     my $w = '0';
    foreach $w (@$v) {
        printf("%10s", $w);
    }
    print("\n");
}
print("***************************************************\n");
################################################################################
# Step 7> Configure L2-L3 traffic.
################################################################################
print ("Congfiguring L2-L3 Traffic Item\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'RSVPTE P2MP Traffic 1',
    '-roundRobinPacketOrdering', 'False',
	'-numVlansForMulticastReplication', '1',
    '-trafficType', 'ipv4');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source       = ($rsvpteLsps1.'/rsvpP2mpIngressLsps');
my @destination  = ($rsvpteLsps2.'/rsvpP2mpEgressLsps');

$ixNet->setMultiAttribute($endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', [['false','none','225.0.0.0','0.0.0.0','1']],
    '-sources',               @source);
$ixNet->commit();

$ixNet->setMultiAttribute($trafficItem1.'/tracking',
    '-trackBy',        ['sourceDestEndpointPair0','trackingenabled0', 'mplsFlowDescriptor0', 'mplsMplsLabelValue0', 'ipv4DestIp0', 'ipv4SourceIp0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();

###############################################################################
# Step 8> Apply and start L2/L3 traffic.
###############################################################################
print("applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

###############################################################################
# Step 9> Retrieve L2/L3 traffic item statistics.
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
# Step 10> Stop L2/L3 traffic.
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# Step 11> Stop all protocols.
################################################################################
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!\n");
