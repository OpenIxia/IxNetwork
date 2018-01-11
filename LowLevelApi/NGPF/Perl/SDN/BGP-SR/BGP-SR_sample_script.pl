################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    09/06/2016 - Sumit - created sample                                 #
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
#    This script demonstrates usage NGPF BGP API for BGP-SR                    #
#	 Script uses two back-to-back Ixia ports to demonstrate the protocol       #
#                                                                              #
#    1. It will create 2 BGP-SR topologies, each having an ipv4 Prefix pool    #
#    2. Start the ospfv2 protocol.                                             #
#    3. Retrieve protocol statistics.                                          #
#    4. Enable the IPv4 MPLS Learned Info. filter on the fly.                  #
#    5. Retrieve protocol learned info.                                        #
#    6. Configure L2-L3 traffic.                                               #
#    7. Start the L2-L3 traffic.                                               #
#    8. Retrieve L2-L3 traffic stats.                                          #
#    9. Stop L2-L3 traffic.                                                    #
#   10. Stop all protocols.                                                    #
#                                                                              # 
# Ixia Software:                                                               #
#    IxOS      8.10 EA                                                         #
#    IxNetwork 8.10 EA                                                         #
#                                                                              #
################################################################################

################################################################################
# Please ensure that PERL5LIB environment variable is set properly so that     #
# IxNetwork.pm module is available. IxNetwork.pm is generally available in     #
# C:\<IxNetwork Install Path>\API\Perl                                         #
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
my $ixTclServer = '10.216.108.113';
my $ixTclPort   = '5555';
my @ports       = (('xg12-regr', '1', '5'), ('xg12-regr', '1', '6'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '7.40',
    '-setAttribute', 'strict');

print("Create a new config\n");
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

print("Configure the multipliers (number of sessions)\n");
$ixNet->setAttribute($t1dev1, '-multiplier', '1');
$ixNet->setAttribute($t2dev1, '-multiplier', '1');
$ixNet->commit();

print("Adding ethernet/mac endpoints\n");
$ixNet->add($t1dev1, 'ethernet');
$ixNet->add($t2dev1, 'ethernet');
$ixNet->commit();

my $mac1 = ($ixNet->getList($t1dev1, 'ethernet'))[0];
my $mac2 = ($ixNet->getList($t2dev1, 'ethernet'))[0];

print("Configure the mac addresses\n");
$ixNet->setMultiAttribute($ixNet->getAttribute($mac1, '-mac').'/counter',
        '-direction', 'increment',
        '-start',     '18:03:73:C7:6C:B1',
        '-step',      '00:00:00:00:00:01');

$ixNet->setAttribute($ixNet->getAttribute($mac2, '-mac').'/singleValue',
        '-value', '18:03:73:C7:6C:01');
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

print("Configure ipv4 addresses");
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '20.20.20.2');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', "20.20.20.2");

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '24');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '24');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

print("Add BGP over IP4 stacks");
$ixNet->add($ip1, 'bgpIpv4Peer');
$ixNet->add($ip2, 'bgpIpv4Peer');
$ixNet->commit();

my $bgp1 = ($ixNet->getList($ip1, 'bgpIpv4Peer'))[0];
my $bgp2 = ($ixNet->getList($ip2, 'bgpIpv4Peer'))[0];

print("Rename the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'BGP Topology 1');
$ixNet->setAttribute($topo2, '-name', 'BGP Topology 2');

$ixNet->setAttribute($t1dev1, '-name', 'BGP Topology 1 Router');
$ixNet->setAttribute($t2dev1, '-name', 'BGP Topology 2 Router');
$ixNet->commit();

#Configure BGP-SR related fields in BGP router
print("Enable Capabilities in BGP Routers - IPv4 MPLS & IPv6 MPLS");
$ixNet->setAttribute($bgp1, '-ipv4MplsCapability', 'true');
$ixNet->setAttribute($bgp1, '-ipv6MplsCapability', 'true');
$ixNet->setAttribute($bgp2, '-ipv4MplsCapability', 'true');
$ixNet->setAttribute($bgp2, '-ipv6MplsCapability', 'true');
$ixNet->commit();

print("Set IPs in BGP DUT IP tab\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-dutIp').'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-dutIp').'/singleValue', '-value', '20.20.20.2');
$ixNet->commit();

print("Add IPv4 Prefix pool behind BGP Routers\n");
$ixNet->execute('createDefaultStack', $t1dev1, 'ipv4PrefixPools');
$ixNet->execute('createDefaultStack', $t2dev1, 'ipv4PrefixPools');

my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
my $networkGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];

$ixNet->setAttribute($networkGroup1, '-name', 'BGP_1_IP_Prefix_pool');
$ixNet->setAttribute($networkGroup2, '-name', 'BGP_1_IP_Prefix_pool');
$ixNet->commit();

print("Configure BGP-SR related fields in IPv4 Prefix Pool behind BGP-SR Topology 1 Router\n");
my $networkGroup1ipv4PrefixPools = ($ixNet->getList($networkGroup1, 'ipv4PrefixPools'))[0];
my $ipv4PrefixPoolBgpIPRouteProperty = ($ixNet->getList($networkGroup1ipv4PrefixPools, 'bgpIPRouteProperty'))[0];

print("Configure prefix pool start address and range on BGP_1_IP_Prefix_pool\n");
$ixNet->setMultiAttribute($ixNet->getAttribute($networkGroup1ipv4PrefixPools, '-networkAddress').'/singleValue', '-value', '5.1.1.1');
$ixNet->setAttribute($networkGroup1ipv4PrefixPools, '-numberOfAddresses', '5');
$ixNet->commit();

print("Enable BGP-SR and set Segment ID on BGP_1_IP_Prefix_pool\n");
$ixNet->setAttribute($ipv4PrefixPoolBgpIPRouteProperty, '-advertiseAsBgp3107Sr', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv4PrefixPoolBgpIPRouteProperty, '-segmentId').'/singleValue', '-value', '101');
$ixNet->commit();

################################################################################
# Start All Protocols and wait for 60 seconds                                   #
################################################################################
print("Start All Protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);

################################################################################
# Retrieve protocol statistics                                                 #
################################################################################
print("Fetch all Protocol Summary Stats\n");
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

################################################################################
# Enable the BGP IPv4 Learned Information Filter                               #
# And apply changes On The Fly                                                 #
################################################################################
print("Enable IPv4 MPLS Learned Information filter for BGP Router\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-filterIpV4Mpls').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-filterIpV4Mpls').'/singleValue', '-value', 'true');
$ixNet->commit();

my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Apply changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(30);

###############################################################################
# Retrieve protocol learned info                                              #
###############################################################################
print("Fetch BGP IPv4 Learned Info\n");
$ixNet->execute('getIPv4MplsLearnedInfo', $bgp2, '1');
sleep(5);
my $linfo  = ($ixNet->getList($bgp2, 'learnedInfo'))[0];
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
# Configure L2-L3 traffic                                                      #    
################################################################################
print ("Congfigure L2-L3 Traffic Item\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'BGP-SR-Traffic Item',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ipv4');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source       = ($networkGroup2.'/ipv4PrefixPools:1');
my @destination  = ($networkGroup1.'/ipv4PrefixPools:1');

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
    '-trackBy',        ['mplsFlowDescriptor0', 'trackingenabled0', 'mplsMplsLabelValue0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();

###############################################################################
# Apply and start L2/L3 traffic                                               #  
###############################################################################
print("Applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

###############################################################################
# Retrieve L2/L3 traffic item statistics                                      #
###############################################################################
print("Print all the L2-L3 traffic flow stats\n");
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
# Stop L2/L3 traffic                                                            #
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# Stop all protocols                                                           #
################################################################################
print ("Stop All Protocols\n");
$ixNet->execute('stopAllProtocols');
print("Sample Script Ends");