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
#     L3vpn interAS OptionC Scenario.                                          #
#                                                                              #
#    1. It will create a BGP topology with LDP & OSPF configured in Provider   #
#        Router.                                                               #
#    2. In Provider Edge Router configuration 2 BGP Peer are configured.       #
#       - iBGP Peer                                                            #
#       - eBGP Peer to configure Multi Hop BGP session.                        #
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
print("!!!L3VPN Option C Test Script Starts !!!\n");

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

print("Adding LDP over IP4 stacks\n");
$ixNet->add($ip1, 'ldpBasicRouter');
$ixNet->commit();

my $ldp1 = ($ixNet->getList($ip1, 'ldpBasicRouter'))[0];

print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'L3vpn_interAS_OptionC_Topology');

$ixNet->setAttribute($t1dev1, '-name', 'Provider Router');
$ixNet->commit();

print("Adding NetworkGroup behind Provider Router  DG\n");
$ixNet->execute('createDefaultStack', $t1dev1, 'ipv4PrefixPools');

my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];

$ixNet->setAttribute($networkGroup1, '-name', 'Network_Group');
$ixNet->setAttribute($networkGroup1, '-multiplier', '1');

print("Configuring LDP prefixes\n");
my $ldpPrefixPool1 = ($ixNet->getList($networkGroup1, 'ipv4PrefixPools'))[0];
$ixNet->setAttribute($ixNet->getAttribute($ldpPrefixPool1, '-networkAddress').'/singleValue', '-value', '2.2.2.2');
$ixNet->setAttribute($ixNet->getAttribute($ldpPrefixPool1, '-prefixLength').'/singleValue', '-value', '32');
$ixNet->commit();

# Add Chanied DG behind LDP NetworkGroup
print("Add Chanied DG behind LDP NetworkGroup\n");
my $chainedDg1 = $ixNet->add($networkGroup1, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg1, '-multiplier', '1', '-name', 'Provider Edge Router');
$ixNet->commit();
$chainedDg1 = ($ixNet->remapIds($chainedDg1))[0];

my $loopback1 = $ixNet->add($chainedDg1, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback1, '-stackedLayers', '', '-name', 'IPv4 Loopback 1');
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

# Adding BGP over IPv4 loopback interfaces (multi Hop eBGP Peer)
print("Adding BGP over IPv4 loopback interfaces\n");
$ixNet->add($loopback1, 'bgpIpv4Peer');
$ixNet->commit();
my $ebgp = ($ixNet->getList($loopback1, 'bgpIpv4Peer'))[0];

# Changing bgp type to external
print("Changing bgp type to external\n");

$ixNet->setAttribute($ixNet->getAttribute($ebgp, '-type').'/singleValue', '-value', 'external');
$ixNet->commit();

# Changing name of eBGP Peer
$ixNet->setAttribute($ebgp, '-name', 'Multihop eBGP Peer');
$ixNet->commit();

print("Setting IPs in BGP DUT IP tab\n");
$ixNet->setAttribute($ixNet->getAttribute($ebgp, '-dutIp').'/singleValue', '-value', '3.2.2.2');
$ixNet->commit();

# Adding another BGP Peer over IPv4 loopback interfaces (iBGP Peer)
print("Adding another BGP Peer over same IPv4 loopback interface\n");
$ixNet->add($loopback1, 'bgpIpv4Peer');
$ixNet->commit();
my $ibgp = ($ixNet->getList($loopback1, 'bgpIpv4Peer'))[1];

# Changing name of iBGP Peer
$ixNet->setAttribute($ibgp, '-name', 'iBGP Peer');
$ixNet->commit();

print("Setting IPs in eBGP DUT IP tab\n");
$ixNet->setAttribute($ixNet->getAttribute($ibgp, '-dutIp').'/singleValue', '-value', '4.2.2.2');
$ixNet->commit();

# Enabling IPv4 MPLS Capability in iBGP Peer
print("Enabling IPv4 MPLS Capability in iBGP Peer\n");
$ixNet->setMultiAttribute($ibgp, '-ipv4MplsCapability', 'true');
$ixNet->commit();

print("Enabling L3VPN  Learned Information filters for BGP Router\n");
$ixNet->setAttribute($ixNet->getAttribute($ebgp, '-filterIpV4Mpls').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($ebgp, '-filterIpV4MplsVpn').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($ibgp, '-filterIpV4Mpls').'/singleValue', '-value', 'true');
$ixNet->setAttribute($ixNet->getAttribute($ibgp, '-filterIpV4MplsVpn').'/singleValue', '-value', 'true');
$ixNet->commit();

print("Adding VRF over eBGP Peer\n");
$ixNet->add($ebgp, 'bgpVrf');
$ixNet->commit();

my $bgpVrf = ($ixNet->getList($ebgp, 'bgpVrf'))[0];

print("Adding IPv4 Address Pool behind bgpVrf with name VPN RouteRange(Src)\n");
my $networkGroup3 = ($ixNet->add($chainedDg1, 'networkGroup'));
my $ipv4PrefixPool1 = ($ixNet->add($networkGroup3, 'ipv4PrefixPools'));
$ixNet->setAttribute($networkGroup3, '-name', 'VPN RouteRange(Src)');
$ixNet->setAttribute($networkGroup3, '-multiplier', '1');
$ixNet->commit();

print("Changing default values of IP prefixes in VPN RouteRange(Src)\n");
$ixNet->setAttribute($ixNet->getAttribute($ipv4PrefixPool1, '-networkAddress').'/singleValue', '-value', '11.11.11.1');
$ixNet->commit();

print("Adding another IPv4 Address Pool connected to iBGP Peer\n");
my $networkGroup4 = ($ixNet->add($chainedDg1, 'networkGroup'));
my $ipv4PrefixPool2 = ($ixNet->add($networkGroup4, 'ipv4PrefixPools'));
$ixNet->setAttribute($networkGroup4, '-name', 'eBGP Lpbk Addr(MPLS RR)');
$ixNet->setAttribute($networkGroup4, '-multiplier', '1');
$ixNet->commit();

print("Changing default values of IP prefixes in eBGP Lpbk Addr(MPLS RR)\n");
$ixNet->setAttribute($ixNet->getAttribute($ipv4PrefixPool2, '-networkAddress').'/singleValue', '-value', '2.2.2.2');
$ixNet->commit();

#Change connector to iBGP Peer
print("Changing BGP Connector in 2nd Prefix pool\n");
my $connector = $ixNet->add($ipv4PrefixPool2, 'connector');
$ixNet->setAttribute($connector, '-connectedTo', $ibgp);
$ixNet->commit();

# Enabling IPv4 MPLS Capability in iBGP Prefix Pool
print("Enabling IPv4 MPLS Capability in iBGP Prefix Pool\n");
my $bgpIPRouteProperty = ($ixNet->getList($ipv4PrefixPool2, 'bgpIPRouteProperty'))[0];
$ixNet->setMultiAttribute($bgpIPRouteProperty, '-advertiseAsBgp3107', 'true');
$ixNet->commit();

# Changing label start value in iBGP Prefix Pool
print("Changing label start value in iBGP Prefix Pool\n");
my $labelStart = $ixNet->getAttribute($bgpIPRouteProperty, '-labelStart');
$ixNet->setMultiAttribute($labelStart, '-clearOverlays', 'false');
$ixNet->commit();

my $counter = $ixNet->add($labelStart, 'counter');
$ixNet->setMultiAttribute($counter,  '-step', '5', '-start', '21', '-direction', 'increment');
$ixNet->commit();


print ("!!! Configured topology Successfully!!!\n");
print("!!! Test Script Ends !!!");

