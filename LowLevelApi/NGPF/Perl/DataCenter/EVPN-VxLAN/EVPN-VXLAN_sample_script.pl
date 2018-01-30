################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    03/12/2015 - Subhradip Pramanik - created sample                          #
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
#    This script intends to demonstrate how to use NGPF EVPN VXLAN API          #
#    About Topology:                                                            #
#        It will create 2 BGP EVPN-VXLAN topologies, each having OSPFv2         #
#    configured in connected Device Group .BGP EVPN VXLAN configured in chained # 
#    device group along with Mac pools connected behind the chained             # 
#    Device Group.                                                              #
#         Script Flow:                                                          #
#        Step 1. Configuration of protocols.                                    #
#    Configuration flow of the script is as follow:                             #
#             i.      Adding OSPF router.                                       #
#             ii.     Adding Network Topology(NT).                              #
#             iii.    Adding chain DG.                                          #
#             iv.     Adding BGP over loopback.                                 #
#             v.      Adding EVPN VXLAN over BGP                                #
#             vi.     Adding MAC Cloud with associated IPv4 Addresses           #
#        Step 2. Start of protocol                                              #
#        Step 3. Protocol Stat display                                          #
#        Step 4. Learned Info display                                           #
#        Step 5. On The Fly(OTF) change of protocol parameter.                  #
#        Step 6. Again Learned Info display to see OTF changes take place       #
#        Step 7. Configuration L2-L3 Traffic                                    #
#        Step 8. Apply and Start of L2-L3 traffic.                              #
#        Step 9. Diplay of L2-L3  traffic Stats.                                #
#        Step 10.Stop of L2-L3 traffic.                                         #
#        Step 11.Stop of all protocols.                                         #
#################################################################################
# Ixia Software Used to develop the script:                                     #
#    IxOS      8.00 EA                                                          #
#    IxNetwork 8.00 EA                                                          #
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
my $ixTclPort   = '8999';
my @ports       = (('10.216.108.82', '2', '15'), ('10.216.108.82', '2', '16'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '8.00',
    '-setAttribute', 'strict');

print("Creating a new config\n");
$ixNet->execute('newConfig');

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


print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'EVPN VXLAN Topology 1');
$ixNet->setAttribute($topo2, '-name', 'EVPN VXLAN Topology 2');
print ("Adding 2 device groups\n");
$ixNet->add($topo1, 'deviceGroup');
$ixNet->add($topo2, 'deviceGroup');
$ixNet->commit();

my @t1devices = $ixNet->getList($topo1, 'deviceGroup');
my @t2devices = $ixNet->getList($topo2, 'deviceGroup');

my $t1dev1 = $t1devices[0];
my $t2dev1 = $t2devices[0];
$ixNet->setAttribute($t1dev1, '-name', 'Label Switch Router 1');
$ixNet->setAttribute($t2dev1, '-name', 'Label Switch Router 2');
$ixNet->commit();

print("Configuring the multipliers (number of sessions)");
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



print("Configuring the mac addresses %s");
$ixNet->setMultiAttribute($ixNet->getAttribute($mac1, '-mac').'/counter',
    '-direction', 'increment',
    '-start',     '22:01:01:01:01:01',
    '-step',      '00:00:00:00:00:01');

$ixNet->setAttribute($ixNet->getAttribute($mac2, '-mac').'/singleValue',
    '-value', '44:01:01:01:01:01');
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
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '51.51.51.2');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '51.51.51.1');
$ixNet->setAttribute($mvGw1 .'/singleValue', '-value', '51.51.51.1');
$ixNet->setAttribute($mvGw2 .'/singleValue', '-value', '51.51.51.2');
$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '26');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '26');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

#  Adding OSPF and configuring it
print("Adding OSPFv2 over IP4 stack");
$ixNet->add($ip1, 'ospfv2');
$ixNet->add($ip2, 'ospfv2');
$ixNet->commit();
my $ospf1 = ($ixNet->getList($ip1, 'ospfv2'))[0];
my $ospf2 = ($ixNet->getList($ip2, 'ospfv2'))[0];
print("Making the NetworkType to Point to Point in the first OSPF router");
my $networkTypeMultiValue1 = $ixNet->getAttribute($ospf1, '-networkType');
$ixNet->setMultiAttribute($networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($networkTypeMultiValue1.'/singleValue', '-value', 'pointtopoint');
$ixNet->commit();
print('Making the NetworkType to Point to Point in the Second OSPF router');
my $networkTypeMultiValue2 = $ixNet->getAttribute($ospf2, '-networkType');
$ixNet->setMultiAttribute($networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($networkTypeMultiValue2.'/singleValue', '-value', 'pointtopoint');
$ixNet->commit();
print("Disabling the Discard Learned Info CheckBox\n");
my $ospfv2RouterDiscardLearnedLSA1 = $ixNet->getAttribute(($ixNet->getList($t1devices[0], 'ospfv2Router'))[0],
    '-discardLearnedLsa');

my $ospfv2RouterDiscardLearnedLSA2 = $ixNet->getAttribute(($ixNet->getList($t2devices[0], 'ospfv2Router'))[0],
    '-discardLearnedLsa');

$ixNet->setMultiAttribute($ospfv2RouterDiscardLearnedLSA1, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($ospfv2RouterDiscardLearnedLSA1.'/singleValue', '-value', 'False');
$ixNet->commit();
$ixNet->setMultiAttribute($ospfv2RouterDiscardLearnedLSA2, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($ospfv2RouterDiscardLearnedLSA2.'/singleValue', '-value', 'False');
$ixNet->commit();


print("Adding the NetworkGroup with Routers at back of it");

$ixNet->execute('createDefaultStack', $t1dev1, 'networkTopology');
$ixNet->execute('createDefaultStack', $t2dev1, 'networkTopology');

my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
my $networkGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];
$ixNet->setAttribute($networkGroup1, '-name', 'Network Topology 1');
$ixNet->setAttribute($networkGroup2, '-name', 'Network Topology 2');
$ixNet->commit();

my $netTopo1 =($ixNet->getList($networkGroup1, 'networkTopology'))[0];
my $netTopo2 =($ixNet->getList($networkGroup2, 'networkTopology'))[0];

# Adding Chained Device Group Behind front Device Group for IPv4 loopback
print("Add Chained Device Group Behind front Device Group for IPv4 loopback");
my $chainedDg1 = $ixNet->add($networkGroup1, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg1, '-multiplier', '1', '-name', 'Edge Router 1');
$ixNet->commit();

my $chainedDg1 = ($ixNet->remapIds($chainedDg1))[0];
my $loopback1 = $ixNet->add($chainedDg1, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback1, '-stackedLayers', [], '-name', 'IPv4 Loopback 2');
$ixNet->commit();

my $connector1 = $ixNet->add($loopback1, 'connector');
$ixNet->setMultiAttribute($connector1, '-connectedTo', $networkGroup1.'/networkTopology/simRouter:1');
$ixNet->commit();

$connector1 = ($ixNet->remapIds($connector1))[0];
my $addressSet1 = $ixNet->getAttribute($loopback1, '-address');
$ixNet->setMultiAttribute($addressSet1, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$addressSet1 = $ixNet->add($addressSet1, 'counter');
$ixNet->setMultiAttribute($addressSet1, '-step', '0.1.0.0', '-start', '2.1.1.1', '-direction', 'increment');
$ixNet->commit();

$addressSet1 = ($ixNet->remapIds($addressSet1))[0];
print("add ipv4 loopback1 for RSVP Leaf Ranges");
my $chainedDg2 = $ixNet->add($networkGroup2, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg2, '-multiplier', '1', '-name', 'Edge Router 2');
$ixNet->commit();

$chainedDg2 = ($ixNet->remapIds($chainedDg2))[0];
my $loopback2 = $ixNet->add($chainedDg2, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback2, '-stackedLayers', [], '-name', 'IPv4 Loopback 1');
$ixNet->commit();

my $connector2 = $ixNet->add($loopback2, 'connector');
$ixNet->setMultiAttribute($connector2, '-connectedTo', $networkGroup2.'/networkTopology/simRouter:1');
$ixNet->commit();

my $connector1 = ($ixNet->remapIds($connector2))[0];
my $addressSet2 = $ixNet->getAttribute($loopback2, '-address');
$ixNet->setMultiAttribute($addressSet2, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$addressSet2 = $ixNet->add($addressSet2, 'counter');
$ixNet->setMultiAttribute($addressSet2, '-step', '0.0.0.1', '-start', '3.1.1.1', '-direction', 'increment');
$ixNet->commit();

$addressSet2 = ($ixNet->remapIds($addressSet2))[0];

print("Adding BGPv4 over IP4 loopback in chained DG");
my $bgpIpv4Peer1 = $ixNet->add($loopback1, 'bgpIpv4Peer');
$ixNet->commit();
$bgpIpv4Peer1 = ($ixNet->remapIds($bgpIpv4Peer1))[0];

print("Adding EVPN VXLAN over IPv4 Loopback 2");
my $bgpIpv4Peer2 = $ixNet->add($loopback2, 'bgpIpv4Peer');
$ixNet->commit();
$bgpIpv4Peer2 = ($ixNet->remapIds($bgpIpv4Peer2))[0];



print("Setting DUT IP in BGPv4 Peer");
$ixNet->setAttribute($ixNet->getAttribute($bgpIpv4Peer1, '-dutIp').'/singleValue',
    '-value', '3.1.1.1');
$ixNet->commit();

$ixNet->setMultiAttribute($ixNet->getAttribute($bgpIpv4Peer2, '-dutIp').'/counter',
    '-direction', 'increment',
    '-start',     '2.1.1.1',
    '-step',      '0.0.0.1');

$ixNet->commit();

print("Enabling Learned Route Filters for EVPN VXLAN in BGP4 Peer");
$ixNet->setAttribute($ixNet->getAttribute($bgpIpv4Peer1, '-filterEvpn').'/singleValue',
        '-value', '1');
$ixNet->commit();

$ixNet->setAttribute($ixNet->getAttribute($bgpIpv4Peer2, '-filterEvpn').'/singleValue',
        '-value', '1');
$ixNet->commit();



print("Configuring Router's MAC Addresses for EVPN VXLAN in BGP4 Peer");

$ixNet->setMultiAttribute($ixNet->getAttribute($bgpIpv4Peer1, '-routersMacOrIrbMacAddress').'/counter',
    '-direction', 'increment',
    '-start',     'aa:aa:aa:aa:aa:aa',
    '-step',      '00:00:00:00:00:01');

$ixNet->commit();

$ixNet->setAttribute($ixNet->getAttribute($bgpIpv4Peer2, '-routersMacOrIrbMacAddress').'/singleValue',
    '-value', 'cc:cc:cc:cc:cc:cc');
$ixNet->commit();

print("Changing Router Id of Network Topology to Loopback Address of Chained Device Group under Edge Router 1");
my $simRouter1 = ($ixNet->getList($netTopo1, 'simRouter'))[0];
my $simRouterId1 = $ixNet->getAttribute($simRouter1, '-routerId');
$ixNet->setMultiAttribute($simRouterId1, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$ixNet->setMultiAttribute($simRouterId1.'/counter', '-step', '0.0.0.1', '-start', '2.1.1.1', '-direction', 'increment');
$ixNet->commit();

$simRouterId1 = ($ixNet->remapIds($simRouterId1))[0];
print("Changing Router Id of Network Topology to Loopback Address of Chained Device Group under Edge Router 2");
my $simRouter2 = ($ixNet->getList($netTopo2, 'simRouter'))[0];
my $simRouterId2 = $ixNet->getAttribute($simRouter2, '-routerId');
$ixNet->setMultiAttribute($simRouterId2, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$ixNet->setMultiAttribute($simRouterId2.'/counter', '-step', '0.0.0.1', '-start', '3.1.1.1', '-direction', 'increment');
$ixNet->commit();

$simRouterId2 = ($ixNet->remapIds($simRouterId2))[0];

print("Adding EVPN VXLAN over BGPv4 in chained DG");

my $bgpIPv4EvpnVXLAN1 = $ixNet->add($bgpIpv4Peer1, 'bgpIPv4EvpnVXLAN');
$ixNet->commit();
my $bgpIPv4EvpnVXLAN1 = ($ixNet->remapIds($bgpIPv4EvpnVXLAN1))[0];

my $bgpIPv4EvpnVXLAN2 = $ixNet->add($bgpIpv4Peer2, 'bgpIPv4EvpnVXLAN');
$ixNet->commit();
$bgpIPv4EvpnVXLAN2 = ($ixNet->remapIds($bgpIPv4EvpnVXLAN2))[0];

print("Changing Import Route Target AS No.");
my $bgpImportRouteTargetList1 = ($ixNet->getList($bgpIPv4EvpnVXLAN1, 'bgpImportRouteTargetList')) [0];

my $bgpImportRouteTargetList2 = ($ixNet->getList($bgpIPv4EvpnVXLAN2, 'bgpImportRouteTargetList')) [0];

my $targetAsNo1 = $ixNet->getAttribute($bgpImportRouteTargetList1, '-targetAsNumber');
my $targetAsNo2 = $ixNet->getAttribute($bgpImportRouteTargetList2, '-targetAsNumber');

$ixNet->setMultiAttribute($targetAsNo1.'/counter', '-step', '0', '-start', '200', '-direction', 'increment');

$ixNet->commit();

$ixNet->setMultiAttribute($targetAsNo2.'/counter', '-step', '0', '-start', '200', '-direction', 'increment');

$ixNet->commit();


print("Changing Export Route Target AS No.\n");
my $bgpExportRouteTargetList1 = ($ixNet->getList($bgpIPv4EvpnVXLAN1, 'bgpExportRouteTargetList')) [0];

my $bgpExportRouteTargetList2 = ($ixNet->getList($bgpIPv4EvpnVXLAN2, 'bgpExportRouteTargetList')) [0];

$ixNet->setMultiAttribute($ixNet->getAttribute($bgpExportRouteTargetList1, '-targetAsNumber').'/counter',
    '-direction', 'increment',
    '-start',     '200',
    '-step',      '0');

$ixNet->commit();

$ixNet->setMultiAttribute($ixNet->getAttribute($bgpExportRouteTargetList2, '-targetAsNumber').'/counter',
    '-direction', 'increment',
    '-start',     '200',
    '-step',      '0');

$ixNet->commit();



print("Adding Mac Pools behind EVPN VXLAN  DG");

$ixNet->execute('createDefaultStack', $chainedDg1, 'macPools');
$ixNet->execute('createDefaultStack', $chainedDg2, 'macPools');

my $networkGroup3 = ($ixNet->getList($chainedDg1, 'networkGroup')) [0];
my $networkGroup4 = ($ixNet->getList($chainedDg2, 'networkGroup')) [0];


$ixNet->setAttribute($networkGroup3 , '-name', "MAC_Pool_1");

$ixNet->setAttribute($networkGroup4 , '-name', "MAC_Pool_2");

$ixNet->setAttribute($networkGroup3 , '-multiplier', "1");
$ixNet->setAttribute($networkGroup4 , '-multiplier', "1");


my $mac3 = ($ixNet->getList($networkGroup3, 'macPools')) [0];
my $mac4 = ($ixNet->getList($networkGroup4, 'macPools')) [0];

print("Configuring IPv4 Addresses associated with CMAC Addresses");

my $ipv4PrefixPools1 = $ixNet->add($mac3, 'ipv4PrefixPools');
$ixNet->commit();
my $ipv4PrefixPools2 = $ixNet->add($mac4, 'ipv4PrefixPools');
$ixNet->commit();


print("Changing no. of CMAC Addresses\n");
$ixNet->setAttribute($mac3 , '-numberOfAddresses', "1");
$ixNet->commit();

$ixNet->setAttribute($mac4 , '-numberOfAddresses', "1");
$ixNet->commit();


print("Changing MAC Addresses of CMAC Ranges\n");
$ixNet->setMultiAttribute($ixNet->getAttribute($mac3, '-mac').'/counter',
    '-direction', 'increment',
    '-start',     '66:66:66:66:66:66',
    '-step',      '00:00:00:00:00:01');

$ixNet->setAttribute($ixNet->getAttribute($mac4, '-mac').'/singleValue',
    '-value', '88:88:88:88:88:88');
$ixNet->commit();


print("Enabling using of VLAN  in CMAC Ranges\n");

$ixNet->setAttribute($mac3 , '-useVlans', "true");
$ixNet->commit();

$ixNet->setAttribute($mac4 , '-useVlans', "true");
$ixNet->commit();


print("Configuring CMAC Vlan properties\n");
my $cMacvlan1 = ($ixNet->getList($mac3, 'vlan')) [0];
my $cMacvlan2 = ($ixNet->getList($mac4, 'vlan')) [0];

print("Configuring VLAN Ids\n");

$ixNet->setMultiAttribute($ixNet->getAttribute($cMacvlan1, '-vlanId').'/counter',
    '-direction', 'increment',
    '-start',     '501',
    '-step',      '1');
$ixNet->commit();

$ixNet->setMultiAttribute($ixNet->getAttribute($cMacvlan2, '-vlanId').'/counter',
    '-direction', 'increment',
    '-start',     '501',
    '-step',      '1');
$ixNet->commit();

print("Configuring VLAN Priorities\n");

$ixNet->setAttribute($ixNet->getAttribute($cMacvlan1, '-priority').'/singleValue',
    '-value', '7');
$ixNet->commit();

$ixNet->setAttribute($ixNet->getAttribute($cMacvlan2, '-priority').'/singleValue',
    '-value', '7');
$ixNet->commit();


print("Changing VNI related Parameters under CMAC Properties\n");

my $cMacProperties1 = ($ixNet->getList($mac3, 'cMacProperties')) [0];
my $cMacProperties2 = ($ixNet->getList($mac4, 'cMacProperties')) [0];


print("Changing 1st Label(L2VNI)\n");
$ixNet->setMultiAttribute($ixNet->getAttribute($cMacProperties1, '-firstLabelStart').'/counter',
    '-direction', 'increment',
    '-start',     '1001',
    '-step',      '10');
$ixNet->commit();

$ixNet->setMultiAttribute($ixNet->getAttribute($cMacProperties2, '-firstLabelStart').'/counter',
    '-direction', 'increment',
    '-start',     '1001',
    '-step',      '10');
$ixNet->commit();
################################################################################

print("Changing 2nd Label(L3VNI)\n");
$ixNet->setMultiAttribute($ixNet->getAttribute($cMacProperties1, '-secondLabelStart').'/counter',
    '-direction', 'increment',
    '-start',     '2001',
    '-step',      '10');
$ixNet->commit();

$ixNet->setMultiAttribute($ixNet->getAttribute($cMacProperties2, '-secondLabelStart').'/counter',
    '-direction', 'increment',
    '-start',     '2001',
    '-step',      '10');
$ixNet->commit();

print("Changing Increment Modes across all VNIs\n");


$ixNet->setAttribute($ixNet->getAttribute($cMacProperties1, '-labelMode').'/singleValue',
    '-value', 'increment');
$ixNet->commit();

$ixNet->setAttribute($ixNet->getAttribute($cMacProperties2, '-labelMode').'/singleValue',
    '-value', 'increment');
$ixNet->commit();


print("Changing VNI step\n");
$ixNet->setMultiAttribute($ixNet->getAttribute($cMacProperties1, '-labelStep').'/counter',
    '-direction', 'increment',
    '-start',     '1',
    '-step',      '0');
$ixNet->commit();

$ixNet->setMultiAttribute($ixNet->getAttribute($cMacProperties2, '-labelStep').'/counter',
    '-direction', 'increment',
    '-start',     '1',
    '-step',      '0');
$ixNet->commit();

###############################################################################
# 2. Start protocols and wait for 60 seconds
################################################################################
print("Wait for 5 seconds before starting protocols\n");
sleep(5);
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(30);

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
print("Fetching all Protocol Summary Stats\n");
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
# 4. Retrieve protocol learned info
###############################################################################

print("Fetching EVPN-VXLAN Learned Info\n");
$ixNet->execute('getEVPNLearnedInfo', $bgpIpv4Peer1);
sleep(5);

my $linfo  = ($ixNet->getList($bgpIpv4Peer1, 'learnedInfo'))[0];
my @linfoList = ($ixNet->getList($linfo, 'table'));
my $table = '';
my $v      = '';
my $c      = '';
print("***************************************************\n");
foreach $table (@linfoList) {
    my $type = ($ixNet->getAttribute($table, '-type'));
    printf("%12s Routes:", $type);
    print("\n***************************************************\n");
    my @columns = ($ixNet->getAttribute($table, '-columns'));
    foreach $c (@columns) {
            printf("%12s", $c);
    }
    my @values = ($ixNet->getAttribute($table, '-values'));
    foreach $v (@values) {
        my $w = '0';
        foreach $w (@$v) {
            printf("%12s", $w);
        }
    }
    print("\n***************************************************\n");
}
print("\n***************************************************\n");
################################################################################
# 5 Apply changes on the fly.
################################################################################
print("Changing Host IP Address Value associated with CMAC in Topology 2");
$ixNet->setAttribute($ixNet->getAttribute($ipv4PrefixPools2, '-networkAddress').'/singleValue',
    '-value', '203.101.1.1');

$ixNet->commit();
my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);
###############################################################################
# 6. Retrieve protocol learned info to show On The Fly changes
###############################################################################

print("Fetching EVPN-VXLAN Learned Info\n");
$ixNet->execute('getEVPNLearnedInfo', $bgpIpv4Peer1);
sleep(5);

my $linfo  = ($ixNet->getList($bgpIpv4Peer1, 'learnedInfo'))[0];
my @linfoList = ($ixNet->getList($linfo, 'table'));
my $table = '';
my $v      = '';
my $c      = '';
print("***************************************************\n");
foreach $table (@linfoList) {
    my $type = ($ixNet->getAttribute($table, '-type'));
    printf("%12s Routes:", $type);
    print("\n***************************************************\n");
    my @columns = ($ixNet->getAttribute($table, '-columns'));
    foreach $c (@columns) {
            printf("%12s", $c);
    }
    my @values = ($ixNet->getAttribute($table, '-values'));
    foreach $v (@values) {
        my $w = '0';
        foreach $w (@$v) {
            printf("%12s", $w);
        }
    }
    print("\n***************************************************\n");
}
print("\n***************************************************\n");
################################################################################
# 7. Configure L2-L3 traffic 
################################################################################
print ("Congfiguring L2-L3 Traffic Item\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ipv4');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');


$ixNet->setMultiAttribute($endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', (''),
    '-scalableSources',       (''),
    '-multicastReceivers',    (''),
    '-scalableDestinations',  (''),
    '-ngpfFilters',           (''),
    '-trafficGroups',         (''),
    '-sources',               $ipv4PrefixPools1,
    '-destinations',          $ipv4PrefixPools2);
$ixNet->commit();

$ixNet->setMultiAttribute($trafficItem1.'/tracking',
    '-trackBy',        ['mplsFlowDescriptor0', 'sourceDestEndpointPair0', 'ethernetIiWithoutFcsSourceaddress0', 'vxlanVni0', 'ipv4SourceIp1', 'ethernetIiWithoutFcsDestinationaddress0', 'ipv4DestIp1', 'trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();

###############################################################################
# 8. Apply and start L2/L3 traffic
###############################################################################
print("applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

###############################################################################
# 9. Retrieve L2/L3 traffic item statistics
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
# 10. Stop L2/L3 traffic
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# 11. Stop all protocols
################################################################################
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!");

