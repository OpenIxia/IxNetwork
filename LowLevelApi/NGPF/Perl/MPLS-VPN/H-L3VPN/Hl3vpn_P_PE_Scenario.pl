################################################################################
# Version 1.0    $Revision: #2 $                                               #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/12/2016 - Poulomi Chatterjee- created sample                           #
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
#    This script intends to demonstrate how to use NGPF BGP API to configure   #
#     H-L3vpn Scenario.                                                        #
#                                                                              #
#    1. It will create a BGP topology with OSPF, RSVP-TE and Targeted LDP      #
#       configured in Area Border Router.                                      #
#    2. In Provider Edge Router configuration  BGP Peer is configured.         #
#    3. BGP VRF is configured on top of BGP Peer.                              #
#    4. IPv4 & IPv6 Prefix Pools are added behind BGP VRF.                     #
#    5. IPv4 and IPv6 addresses  are configured in IPv4 and IPv6 Prefix Pools. #
#    6. Label values are configured in V4 & V6 Prefix Pools.                   #
#    3. Only one side configuration is provided.                               #
#    4. Traffic configuration will be similar to L3VPN scenario.               #
# Ixia Software:                                                               #
#    IxOS      8.20 EA                                                         #
#    IxNetwork 8.20 EA                                                         #
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
print("!!!H-L3VPN Test Script Starts !!!\n");

# Edit this variables values to match your setup
my $ixTclServer = '10.216.108.113';
my $ixTclPort   = '8650';
my @ports       = (('10.216.108.82', '7', '11'), ('10.216.108.82', '7', '12'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '8.20',
    '-setAttribute', 'strict');

print("Creating a new config\n");
$ixNet->execute('newConfig');

print("Adding vports\n");
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->commit();

my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vportTx = $vPorts[0];
my $vportRx = $vPorts[1];
assignPorts($ixNet, @ports, $vportTx, $vportRx);
sleep(5);

print("Adding topology\n");
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', $vportTx);
$ixNet->commit();

my @topologies = $ixNet->getList($ixNet->getRoot(), 'topology');
my $topo1 = $topologies[0];

print("Adding device group\n");
$ixNet->add($topo1, 'deviceGroup');
$ixNet->commit();

my @t1devices = $ixNet->getList($topo1, 'deviceGroup');

my $t1dev1 = $t1devices[0];

print("Configuring the multipliers (number of sessions)\n");
$ixNet->setAttribute($t1dev1, '-multiplier', '1');
$ixNet->commit();

print("Adding ethernet/mac endpoints\n");
$ixNet->add($t1dev1, 'ethernet');
$ixNet->commit();

my $mac1 = ($ixNet->getList($t1dev1, 'ethernet'))[0];

print("Configuring the mac addresses\n");
$ixNet->setMultiAttribute($ixNet->getAttribute($mac1, '-mac').'/counter',
        '-direction', 'increment',
        '-start',     '18:03:73:C7:6C:B1',
        '-step',      '00:00:00:00:00:01');

$ixNet->commit();

# print("\$ixNet->help ::ixNet::OBJ-/topology/deviceGroup/ethernet\n");
# print($ixNet->help ('::ixNet::OBJ-/topology/deviceGroup/ethernet'));
print("Add ipv4\n");
$ixNet->add($mac1, 'ipv4');
$ixNet->commit();

my $ip1 = ($ixNet->getList($mac1, 'ipv4'))[0];

my $mvAdd1 = $ixNet->getAttribute($ip1, '-address');
my $mvGw1  = $ixNet->getAttribute($ip1, '-gatewayIp');

print("configuring ipv4 addresses\n");
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '20.20.20.2');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '20.20.20.1');

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '24');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

# print("\$ixNet->help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4\n)"
# print($ixNet->help ('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4'))"

print("Adding OSPF over IP4 stacks\n");
$ixNet->add($ip1, 'ospfv2');
$ixNet->commit();

my $ospf1 = ($ixNet->getList($ip1, 'ospfv2'))[0];

print("Adding NetworkGroup behind Area Border Router  DG\n");
$ixNet->execute('createDefaultStack', $t1dev1, 'ipv4PrefixPools');

my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];

$ixNet->setAttribute($networkGroup1, '-name', 'Network_Group');
$ixNet->setAttribute($networkGroup1, '-multiplier', '1');

print("Adding IPv4 Loobcak in first Device Group\n");
my $loopback1 = $ixNet->add($t1dev1, 'ipv4Loopback');
$ixNet->commit();

print("Adding Targeted LDP over IPv4 Loopback\n");
$ixNet->add($loopback1, 'ldpTargetedRouter');
$ixNet->commit();

print("Adding RSVP-TE over sameIPv4 Loopback\n");
$ixNet->add($loopback1, 'rsvpteLsps');
$ixNet->commit();

print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'Hl3VPN_Topology');

$ixNet->setAttribute($t1dev1, '-name', 'Area Border Router');
$ixNet->commit();

print("Configuring LDP prefixes\n");
my $ldpPrefixPool1 = ($ixNet->getList($networkGroup1, 'ipv4PrefixPools'))[0];
$ixNet->setAttribute($ixNet->getAttribute($ldpPrefixPool1, '-networkAddress').'/singleValue', '-value', '2.2.2.2');
$ixNet->setAttribute($ixNet->getAttribute($ldpPrefixPool1, '-prefixLength').'/singleValue', '-value', '32');
$ixNet->commit();

# Add Chanied DG behind NetworkGroup
print("Add Chanied DG behind NetworkGroup\n");
my $chainedDg1 = $ixNet->add($networkGroup1, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg1, '-multiplier', '1', '-name', 'Provider Edge Router');
$ixNet->commit();
$chainedDg1 = ($ixNet->remapIds($chainedDg1))[0];

# Add ipv4 loopback in Chained DG
my $loopback1 = $ixNet->add($chainedDg1, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback1, '-stackedLayers', '', '-name', 'IPv4 Loopback');
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

# Adding BGP over IPv4 loopback interfaces
print("Adding BGP over IPv4 loopback interfaces\n");
$ixNet->add($loopback1, 'bgpIpv4Peer');
$ixNet->commit();
my $bgp = ($ixNet->getList($loopback1, 'bgpIpv4Peer'))[0];

print("Setting IPs in BGP DUT IP tab\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp, '-dutIp').'/singleValue', '-value', '3.2.2.2');
$ixNet->commit();

print("Enabling L3VPN  Learned Information filters for BGP Router\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp, '-filterIpV4MplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($bgp, '-filterIpV6MplsVpn').'/singleValue', '-value', 'true');
$ixNet->commit();

print("Adding VRF over BGP Peer\n");
$ixNet->add($bgp, 'bgpVrf');
$ixNet->commit();

my $bgpVrf = ($ixNet->getList($bgp, 'bgpVrf'))[0];

print("Adding IPv4 Address Pool behind bgpVrf\n");
my $networkGroup3 = ($ixNet->add($chainedDg1, 'networkGroup'));
$ixNet->commit();
my $ipv4PrefixPool = ($ixNet->add($networkGroup3, 'ipv4PrefixPools'));
$ixNet->commit();
$ixNet->setAttribute($networkGroup3, '-multiplier', '1');
$ixNet->commit();

print("Changing default values of IP prefixes\n");
$ixNet->setAttribute($ixNet->getAttribute($ipv4PrefixPool, '-networkAddress').'/singleValue', '-value', '203.1.0.0');
$ixNet->commit();

# Changing label start value in IPv4 Prefix Pool
print("Changing label start value in IPv4 Prefix Pool\n");
my $v4RouteProperty = ($ixNet->getList($ipv4PrefixPool, 'bgpL3VpnRouteProperty'))[0];
my $labelStart = ($ixNet->getAttribute($v4RouteProperty, '-labelStart'));
$ixNet->setMultiAttribute($labelStart, '-clearOverlays', 'false');

my $counter = $ixNet->add($labelStart, 'counter');
$ixNet->setMultiAttribute($counter,  '-step', '5', '-start', '7111', '-direction', 'increment');
$ixNet->commit();

# Adding IPv6 Address Pool behind bgpVrf
print("Adding IPv6 Address Pools behind bgpVrf\n");
my $networkGroup4 = $ixNet->add($chainedDg1, 'networkGroup');
$ixNet->commit();
my $ipv6PrefixPool = $ixNet->add($networkGroup4, 'ipv6PrefixPools');
$ixNet->commit();
$ixNet->setAttribute($networkGroup4, '-multiplier', '1');
$ixNet->commit();

# Changing default values of IPv6 prefixes
print("Changing default values of IPv6 prefixes\n");
$ixNet->setAttribute($ixNet->getAttribute($ipv6PrefixPool, '-networkAddress').'/singleValue', '-value', '2000:1:1:1:0:0:0:0');
$ixNet->commit();

# Changing Label value in IPv6 Prefix Pool
print("Changing Label value in IPv6 Prefix Pool\n");
my $v6RouteProperty = ($ixNet->getList($ipv6PrefixPool, 'bgpV6L3VpnRouteProperty'))[0];
my $multiValue = $ixNet->getAttribute($v6RouteProperty, '-labelStart');
$ixNet->setMultiAttribute($multiValue, '-clearOverlays', 'false');
my $count = $ixNet->add($multiValue, 'counter');
$ixNet->setMultiAttribute($count,  '-step', '10', '-start', '5000', '-direction', 'increment');
$ixNet->commit();

print("!!! Scenario confiugrd Successfully!!!\n");
print("!!! Test Script Ends !!!\n");

