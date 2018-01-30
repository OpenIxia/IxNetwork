################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    24/06/2016 - Debarati Chakraborty - created sample                        #
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
#    This script intends to demonstrate how to use NGPF BGP RFC 3107 TCL APIs   #
#    About Topology:                                                            #
#       The scenario consists of two BGP peers.                                 #
#       Each of them capable of carrying Label information for the attached     #
#       advertising Route Range. Unidirectional Traffic is created in between   #
#       the peers.                                                              #
#         Script Flow:                                                          #
#        Step 1. Creation of 2 BGP topologies with RFC3107 IPv4 MPLS Capability #
#        Step 2. Start of protocol                                              #
#        Step 3. Protocol Stat display                                          #
#        Step 4. Learned Info display                                           #
#        Step 5. Configuration L2-L3 Traffic                                    #
#        Step 6. Apply and Start of L2-L3 traffic                               #
#        Step 7. Display of L2-L3  traffic Stats                                #
#        Step 8.Stop of L2-L3 traffic                                           #
#        Step 9.Stop of all protocols                                           #
#################################################################################
# Ixia Software Used to develop the script:                                     #
#    IxOS      8.10 EA                                                          #
#    IxNetwork 8.10 EA                                                          #
#                                                                               #
#################################################################################

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
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '20.20.20.2');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', "20.20.20.2");

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '24');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '24');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

#  Adding BGP and configuring it
print("Adding BGP over IP4 stacks\n");
$ixNet->add($ip1, 'bgpIpv4Peer');
$ixNet->add($ip2, 'bgpIpv4Peer');
$ixNet->commit();

my $bgp1 = ($ixNet->getList($ip1, 'bgpIpv4Peer'))[0];
my $bgp2 = ($ixNet->getList($ip2, 'bgpIpv4Peer'))[0];

print("Enabling IPv4 MPLS Capability in the BGP Peers");
$ixNet->setMultiAttribute($bgp1, '-ipv4MplsCapability', 'true');
$ixNet->commit();

$ixNet->setMultiAttribute($bgp2, '-ipv4MplsCapability', 'true');
$ixNet->commit();

print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'BGP Topology 1');
$ixNet->setAttribute($topo2, '-name', 'BGP Topology 2');

$ixNet->setAttribute($t1dev1, '-name', 'BGP Router 1');
$ixNet->setAttribute($t2dev1, '-name', 'BGP Router 2');
$ixNet->commit();

print("Setting IPs in BGP DUT IP tab\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-dutIp').'/singleValue', '-value', '50.50.50.1');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-dutIp').'/singleValue', '-value', '50.50.50.2');
$ixNet->commit();

# Add NetworkGroup behind BGP DG
print("Adding NetworkGroup behind BGP DG\n");
my $networkGroup1 = $ixNet->add($t1dev1, 'networkGroup');
$ixNet->commit();
$networkGroup1 = ($ixNet->remapIds($networkGroup1))[0];

my $ipv4PrefixPools1 = $ixNet->add($networkGroup1, 'ipv4PrefixPools');
$ixNet->commit();

my $networkGroup2 = $ixNet->add($t2dev1, 'networkGroup');
$ixNet->commit();
$networkGroup2 = ($ixNet->remapIds($networkGroup2))[0];

my $ipv4PrefixPools2 = $ixNet->add($networkGroup2, 'ipv4PrefixPools');
$ixNet->commit();

print("Configuring the number of addresses\n");
$ixNet->setMultiAttribute($ipv4PrefixPools1, '-numberOfAddresses', '5');
$ixNet->commit();

$ixNet->setMultiAttribute($ipv4PrefixPools2, '-numberOfAddresses', '5');
$ixNet->commit();

print("Enabling BGP 3107 advertising capability in BGP Peer\n");
my $bgpIPRouteProp1 = ($ixNet->getList($ipv4PrefixPools1, 'bgpIPRouteProperty'))[0];
$ixNet->setMultiAttribute($bgpIPRouteProp1, '-advertiseAsBgp3107', 'true');
$ixNet->commit();
$bgpIPRouteProp1 = ($ixNet->remapIds($bgpIPRouteProp1))[0];

my $bgpIPRouteProp2 = ($ixNet->getList($ipv4PrefixPools2, 'bgpIPRouteProperty'))[0];
$ixNet->setMultiAttribute($bgpIPRouteProp2, '-advertiseAsBgp3107', 'true');
$ixNet->commit();
$bgpIPRouteProp2 = ($ixNet->remapIds($bgpIPRouteProp2))[0];

print("Editing Label values in BGP IP Route Ranges\n");
my $labelStrt_1 = ($ixNet->getAttribute($bgpIPRouteProp1, '-labelStart'));
$ixNet->setMultiAttribute($labelStrt_1, '-clearOverlays', 'False', '-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($labelStrt_1.'/singleValue', '-value', '1006');
$ixNet->commit();


my $labelStrt_2 = ($ixNet->getAttribute($bgpIPRouteProp2, '-labelStart'));
$ixNet->setMultiAttribute($labelStrt_2, '-clearOverlays', 'False', '-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($labelStrt_2.'/singleValue', '-value', '2006');
$ixNet->commit();

print("Enabling IPv4 MPLS Learned Information for BGP Routers\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-filterIpV4Mpls').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-filterIpV4Mpls').'/singleValue', '-value', 'true');
$ixNet->commit();

print("Configuring the multipliers (number of sessions)\n");
$ixNet->setAttribute($t1dev1, '-multiplier', '5');
$ixNet->setAttribute($t2dev1, '-multiplier', '5');
$ixNet->commit();

################################################################################
# Start protocol and wait for 60 seconds                                       #
################################################################################
print("Starting protocols and waiting for 45 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(45);

################################################################################
# Retrieve protocol statistics                                                 #
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
# Retrieve protocol learned info                                              #
###############################################################################
print("Fetching BGP Learned Info\n");
$ixNet->execute('getIPv4MplsLearnedInfo', $bgp1, '1');
sleep(5);
my $linfo  = ($ixNet->getList($bgp1, 'learnedInfo'))[0];
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
print ("Congfiguring L2-L3 Traffic Item\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ipv4');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source       = ($networkGroup1.'/ipv4PrefixPools:1');
my @destination  = ($networkGroup2.'/ipv4PrefixPools:1');

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
    '-trackBy',        ['sourceDestEndpointPair0','trackingenabled0', 'mplsMplsLabelValue0', 'ipv4DestIp0', 'ipv4SourceIp0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();

###############################################################################
# Apply and start L2/L3 traffic                                               #  
###############################################################################
print("applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

print("Let traffic run for 2 minutes\n");
sleep(120);

###############################################################################
# Retrieve L2/L3 traffic item statistics                                      #
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
# Stop L2/L3 traffic                                                            #
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# Stop all protocols                                                           #
################################################################################
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!\n");
