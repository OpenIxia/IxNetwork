################################################################################
# Version 1.0    $Revision: #1 $                                               #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    03/12/2015- Pchatterjee Chatterjee created sample                         #
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

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF BGP PBB EVPN PERL API. #
#                                                                              #
#    1. It will create 2 BGP PBB EVPN topologies, each having LDP configured in#
#        connected Device Group .BGP EVPN configured in chained device group   #
#        along with Mac pools connected behind the chained Device Group.       #
#    2. Start all protocol.                                                    #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Configure L2-L3 traffic.                                               #
#    6. Start the L2-L3 traffic.                                               #
#    7. Retrieve L2-L3 traffic stats.                                          #
#    8. Stop L2-L3 traffic.                                                    #
#    9. Stopallprotocols.                                                      #
# Ixia Software:                                                               #
#    IxOS      8.00 EA                                                         #
#    IxNetwork 8.00 EA                                                         #
#                                                                              #
################################################################################

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
my $ixTclPort   = '8350';
my @ports       = (('10.216.108.82', '2', '7'), ('10.216.108.82', '2', '8'));
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

print("Adding 2 device groups\n");
$ixNet->add($topo1, 'deviceGroup');
$ixNet->add($topo2, 'deviceGroup');
$ixNet->commit();

my @t1devices = $ixNet->getList($topo1, 'deviceGroup');
my @t2devices = $ixNet->getList($topo2, 'deviceGroup');

my $t1dev1 = $t1devices[0];
my $t2dev1 = $t2devices[0];

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
        '-start',     '18:03:73:C7:6C:B1',
        '-step',      '00:00:00:00:00:01');

$ixNet->setAttribute($ixNet->getAttribute($mac2, '-mac').'/singleValue',
        '-value', '18:03:73:C7:6C:01');
$ixNet->commit();

# print("\$ixNet->help ::ixNet::OBJ-/topology/deviceGroup/ethernet\n");
# print($ixNet->help ('::ixNet::OBJ-/topology/deviceGroup/ethernet'));
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

print("configuring ipv4 addresses");
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '20.20.20.2');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', "20.20.20.2");

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '24');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '24');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

# print("\$ixNet->help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4\n)"
# print($ixNet->help ('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4'))"
print("Adding LDP over IP4 stacks");
$ixNet->add($ip1, 'ldpBasicRouter');
$ixNet->add($ip2, 'ldpBasicRouter');
$ixNet->commit();

my $ldp1 = ($ixNet->getList($ip1, 'ldpBasicRouter'))[0];
my $ldp2 = ($ixNet->getList($ip2, 'ldpBasicRouter'))[0];

print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'EVPN Topology 1');
$ixNet->setAttribute($topo2, '-name', 'EVPN Topology 2');

$ixNet->setAttribute($t1dev1, '-name', 'LDP Router1');
$ixNet->setAttribute($t2dev1, '-name', 'LDP Router2');
$ixNet->commit();

print("Adding NetworkGroup behind LDP DG\n");
$ixNet->execute('createDefaultStack', $t1dev1, 'ipv4PrefixPools');
$ixNet->execute('createDefaultStack', $t2dev1, 'ipv4PrefixPools');

my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
my $networkGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];

$ixNet->setAttribute($networkGroup1, '-name', 'LDP_1_Network_Group1');
$ixNet->setAttribute($networkGroup2, '-name', 'LDP_2_Network_Group1');
$ixNet->setAttribute($networkGroup1, '-multiplier', '1');
$ixNet->setAttribute($networkGroup2, '-multiplier', '1');

print("Configuring LDP prefixes\n");
my $ldpPrefixPool1 = ($ixNet->getList($networkGroup1, 'ipv4PrefixPools'))[0];
my $ldpPrefixPool2 = ($ixNet->getList($networkGroup2, 'ipv4PrefixPools'))[0];
$ixNet->setAttribute($ixNet->getAttribute($ldpPrefixPool1, '-networkAddress').'/singleValue', '-value', '2.2.2.2');
$ixNet->setAttribute($ixNet->getAttribute($ldpPrefixPool2, '-networkAddress').'/singleValue', '-value', '3.2.2.2');
$ixNet->setAttribute($ixNet->getAttribute($ldpPrefixPool1, '-prefixLength').'/singleValue', '-value', '32');
$ixNet->setAttribute($ixNet->getAttribute($ldpPrefixPool2, '-prefixLength').'/singleValue', '-value', '32');
$ixNet->commit();

# Add ipv4 loopback2 behind LDP Topology 1
print("Adding ipv4 loopback1\n");
my $chainedDg1 = $ixNet->add($networkGroup1, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg1, '-multiplier', '1', '-name', 'Device Group 3');
$ixNet->commit();
$chainedDg1 = ($ixNet->remapIds($chainedDg1))[0];

my $loopback1 = $ixNet->add($chainedDg1, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback1, '-stackedLayers', '', '-name', 'IPv4 Loopback 2');
$ixNet->commit();

my $connector1 = $ixNet->add($loopback1, 'connector');
$ixNet->setMultiAttribute($connector1,
     '-connectedTo', $networkGroup1.'/ipv4PrefixPools:1');
$ixNet->commit();

my $connector1 = ($ixNet->remapIds($connector1))[0];

my $addressSet1 = $ixNet->getAttribute($loopback1, '-address');
$ixNet->setMultiAttribute($addressSet1, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$addressSet1 = $ixNet->add($addressSet1, 'counter');
$ixNet->setMultiAttribute($addressSet1, '-step', '0.0.0.1',
    '-start', '2.2.2.2', '-direction', 'increment');
$ixNet->commit();
my $addressSet1 = ($ixNet->remapIds($addressSet1))[0];

# Add ipv4 loopback2 behind LDP Topology 1
print("Adding ipv4 loopback2\n");
my $chainedDg2 = $ixNet->add($networkGroup2, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg2, '-multiplier', '1', '-name', 'Device Group 4');
$ixNet->commit();
$chainedDg2 = ($ixNet->remapIds($chainedDg2))[0];

my $loopback2 = $ixNet->add($chainedDg2, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback2, '-stackedLayers', '', '-name', 'IPv4 Loopback 2');
$ixNet->commit();

my $connector2 = $ixNet->add($loopback2, 'connector');
$ixNet->setMultiAttribute($connector2, '-connectedTo',
    $networkGroup2.'/ipv4PrefixPools:1');
$ixNet->commit();
$connector2 = ($ixNet->remapIds($connector2))[0];

my $addressSet2 = $ixNet->getAttribute($loopback2, '-address');
$ixNet->setMultiAttribute($addressSet2, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$addressSet2 = $ixNet->add($addressSet2, 'counter');
$ixNet->setMultiAttribute($addressSet2, '-step', '0.0.0.1',
    '-start', '3.2.2.2', '-direction', 'increment');
$ixNet->commit();
$addressSet2 = ($ixNet->remapIds($addressSet2))[0];

print("Adding BGP over IPv4 loopback interfaces\n");
$ixNet->add($loopback1, 'bgpIpv4Peer');
$ixNet->add($loopback2, 'bgpIpv4Peer');
$ixNet->commit();

my $bgp1 = ($ixNet->getList($loopback1, 'bgpIpv4Peer'))[0];
my $bgp2 = ($ixNet->getList($loopback2, 'bgpIpv4Peer'))[0];

print("Setting IPs in BGP DUT IP tab\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-dutIp').'/singleValue', '-value', '3.2.2.2');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-dutIp').'/singleValue', '-value', '2.2.2.2');
$ixNet->commit();

print("Enabling EVPN Learned Information for BGP Router\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-filterEvpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-filterEvpn').'/singleValue', '-value', 'true');
$ixNet->commit();

print("Adding PBB EVPN over BGP in both ports\n");
$ixNet->add($bgp1, 'bgpIPv4EvpnPbb');
$ixNet->add($bgp2, 'bgpIPv4EvpnPbb');
$ixNet->commit();

my $EvpnPbb1 = ($ixNet->getList($bgp1, 'bgpIPv4EvpnPbb'))[0];
my $EvpnPbb2 = ($ixNet->getList($bgp2, 'bgpIPv4EvpnPbb'))[0];

print("Configuring ESI value in both ports\n");
my $ethernetSegment1 = ($ixNet->getList($bgp1, 'bgpEthernetSegmentV4'))[0];
my $ethernetSegment2 = ($ixNet->getList($bgp2, 'bgpEthernetSegmentV4'))[0];
$ixNet->setAttribute($ixNet->getAttribute($ethernetSegment1, '-esiValue').'/singleValue', '-value', '1');
$ixNet->setAttribute($ixNet->getAttribute($ethernetSegment2, '-esiValue').'/singleValue', '-value', '2');
$ixNet->commit();

print("Configuring B-MAC Prefix value in both ports\n");
$ixNet->setAttribute($ixNet->getAttribute($ethernetSegment1, '-bMacPrefix').'/singleValue', '-value', 'B0:11:01:00:00:03');
$ixNet->setAttribute($ixNet->getAttribute($ethernetSegment2, '-bMacPrefix').'/singleValue', '-value', 'B0:12:01:00:00:03');


print("Adding Mac Pools behind PBB EVPN DG\n");
$ixNet->execute('createDefaultStack', $chainedDg1, 'macPools');
$ixNet->execute('createDefaultStack', $chainedDg2, 'macPools');

my $networkGroup3 = ($ixNet->getList($chainedDg1, 'networkGroup'))[0]; 
my $networkGroup4 = ($ixNet->getList($chainedDg2, 'networkGroup'))[0]; 

$ixNet->setAttribute($networkGroup3, '-name', 'MAC_Pool_1');
$ixNet->setAttribute($networkGroup4, '-name', 'MAC_Pool_2');
$ixNet->setAttribute($networkGroup3, '-multiplier', '1');
$ixNet->setAttribute($networkGroup4, '-multiplier', '1');

print("Changing default values of MAC Addresses in MAC Pools\n");
my $macPool1 = ($ixNet->getList($networkGroup3, 'macPools'))[0];
my $macPool2 = ($ixNet->getList($networkGroup4, 'macPools'))[0];
$ixNet->setAttribute($ixNet->getAttribute($macPool1, '-mac').'/singleValue', '-value', 'A0:11:01:00:00:03');
$ixNet->setAttribute($ixNet->getAttribute($macPool2, '-mac').'/singleValue', '-value', 'A0:12:01:00:00:03');
$ixNet->commit();


###############################################################################
# 2. Start protocols and wait for 60 seconds
################################################################################
print("Wait for 5 seconds before starting protocols\n");
sleep(5);
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);

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
print("Fetching EVPN Learned Info\n");
$ixNet->execute('getEVPNLearnedInfo', $bgp1);
sleep(5);

my $linfo  = ($ixNet->getList($bgp1, 'learnedInfo'))[0];
my @linfoList = ($ixNet->getList($linfo, 'table'));
my $table = '';
my $v      = '';
my $c      = '';
print("***************************************************\n");
foreach $table (@linfoList) {
    my $type = ($ixNet->getAttribute($table, '-type'));
    printf("%12s Routes :", $type);
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
# 5. Configure L2-L3 traffic 
################################################################################
print ("Congfiguring L2-L3 Traffic Item\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ethernetVlan');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source       = ($networkGroup3.'/macPools:1');
my @destination  = ($networkGroup4.'/macPools:1');

$ixNet->setMultiAttribute($endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', (''),
    '-scalableSources',       (''),
    '-multicastReceivers',    (''),
    '-scalableDestinations',  (''),
    '-ngpfFilters',           (''),
    '-trafficGroups',         (''),
    '-sources',               @source,
    '-destinations',          @destination);
$ixNet->commit();

$ixNet->setMultiAttribute($trafficItem1.'/tracking',
    '-trackBy',        ['mplsFlowDescriptor0','trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();
###############################################################################
# 6. Apply and start L2/L3 traffic
###############################################################################
print("applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

###############################################################################
# 7. Retrieve L2/L3 traffic item statistics
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
# 8. Stop L2/L3 traffic
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# 9. Stop all protocols
################################################################################
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!");

