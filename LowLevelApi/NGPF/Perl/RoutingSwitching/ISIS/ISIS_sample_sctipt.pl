################################################################################
# Version 1.0    $Revision: #1 $                                               #
#                                                                              #
#    Copyright  1997 - 2014 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/10/2014 - Poulomi Chatterjee - created sample                          #
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
#    This script intends to demonstrate how to use NGPF ISISL3 API.            #
#                                                                              #
#    1. It will create 2 ISISL3 topologies, each having an ipv4 & ipv6 network #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. A loopback device group(DG) behind network   # 
#       group is needed to support applib traffic.                             #
#    2. Start the isisL3 protocol.                                             #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Enable the IsisL3 simulated topologies ipv4 & ipv6 noderoutes, which   #
#       was disabled by default and apply change on the fly.                   #
#    6. Retrieve protocol learned info again and notice the difference with    #
#       previously retrieved learned info.                                     #
#    7. Configure L2-L3 traffic.                                               #
#    8. Configure IPv4 application traffic.[application Traffic type is set    #
#       using variable "trafficType". "ipv4ApplicationTraffic" for ipv4 profile#
#       and "ipv6ApplicationTraffic" for ipv6 profile.                         #
#       Note: IPv4 & IPv6 both could not be configured in same endpoint set.   # 
#    9. Start the L2-L3 traffic.                                               #
#   10. Start the application traffic.                                         #
#   11. Retrieve Application traffic stats.                                    #
#   12. Retrieve L2-L3 traffic stats.                                          #
#   13. Stop L2-L3 traffic.                                                    #
#   14. Stop Application traffic.                                              #
#   15. Stop all protocols.                                                    #
# Ixia Software:                                                               #
#    IxOS      6.80 EB                                                         #
#    IxNetwork 7.40 EB                                                         #
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
my $ixTclServer = '10.205.28.41';
my $ixTclPort   = '8067';
my @ports       = (('10.205.28.170', '1', '5'), ('10.205.28.170', '1', '6'));

# Variable named trafficType sets type of application traffic to be configured.
# "ipv4ApplicationTraffic" for ipv4 profile & "ipv6ApplicationTraffic" for ipv6 profile.
my $trafficType = 'ipv6ApplicationTraffic';

# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '7.40',
    '-setAttribute', 'strict');

print("Creating a new config\n");
$ixNet->execute('newConfig');

################################################################################
#  Protocol configuration section. Configure ISIS as per the description
#  give above
################################################################################ 
# Adding Virtual ports
print("Adding 2 vports\n");
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->commit();

my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vportTx = $vPorts[0];
my $vportRx = $vPorts[1];
assignPorts($ixNet, @ports, $vportTx, $vportRx);
sleep(5);

# Adding Topologies
print("Adding 2 topologies\n");
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', $vportTx);
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', $vportRx);
$ixNet->commit();

my @topologies = $ixNet->getList($ixNet->getRoot(), 'topology');
my $topo1 = $topologies[0];
my $topo2 = $topologies[1];

# Adding Device Groups
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

# Adding Ethernet
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
print('$ixNet->help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet\')\n');

# Add IPv4
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

print('$ixNet->help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4\')');

# Adding ISIS over Ethernet stack
print("Adding ISISL3 over Ethernet stacks");
$ixNet->add($mac1, 'isisL3');
$ixNet->add($mac2, 'isisL3');
$ixNet->commit();

my $isisL3_1 = ($ixNet->getList($mac1, 'isisL3'))[0];
my $isisL3_2 = ($ixNet->getList($mac2, 'isisL3'))[0];

print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'ISIS Topology 1');
$ixNet->setAttribute($topo2, '-name', 'ISIS Topology 2');

$ixNet->setAttribute($t1dev1, '-name', 'ISIS Topology 1 Router');
$ixNet->setAttribute($t2dev1, '-name', 'ISIS Topology 2 Router');
$ixNet->commit();

# Enable host name in ISIS router1
print("Enabling Host name in Emulated ISIS Routers\n");
my $deviceGroup1 = ($ixNet->getList($topo1, 'deviceGroup'))[0];
my $isisL3Router1 = ($ixNet->getList($deviceGroup1, 'isisL3Router'))[0];
my $enableHostName1 = ($ixNet->getAttribute($isisL3Router1, '-enableHostName'));
$ixNet->setAttribute($enableHostName1.'/singleValue', '-value', 'True');
$ixNet->commit();
my $configureHostName1 = $ixNet->getAttribute($isisL3Router1, '-hostName');
$ixNet->setAttribute($configureHostName1.'/singleValue', '-value', 'isisL3Router1');
$ixNet->commit();
# Enable host name in ISIS router2
my $deviceGroup2 = ($ixNet->getList($topo2, 'deviceGroup'))[0];
my $isisL3Router2 = ($ixNet->getList($deviceGroup2, 'isisL3Router'))[0];
my $enableHostName2 = ($ixNet->getAttribute($isisL3Router2, '-enableHostName'));
$ixNet->setAttribute($enableHostName2.'/singleValue', '-value', 'True');
$ixNet->commit();
my $configureHostName2 = ($ixNet->getAttribute($isisL3Router2, '-hostName'));
$ixNet->setAttribute($configureHostName2.'/singleValue', '-value', 'isisL3Router2');
$ixNet->commit();

print("Making the NetworkType to Point to Point in the first ISISrouter\n");
my $networkTypeMultiValue1 = ($ixNet->getAttribute($isisL3_1, '-networkType'));
$ixNet->setMultiAttribute($networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($networkTypeMultiValue1.'/singleValue', '-value', 'pointpoint');

print("Making the NetworkType to Point to Point in the Second ISIS router\n");
my $networkTypeMultiValue2 = ($ixNet->getAttribute($isisL3_2, '-networkType'));
$ixNet->setAttribute($networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setAttribute($networkTypeMultiValue2.'/singleValue', '-value', 'pointpoint');

# Disable Discard Learned LSP 
print("Disabling the Discard Learned Info CheckBox\n");
my $isisL3RouterDiscardLearnedLSP1 = $ixNet->getAttribute(($ixNet->getList($t1devices[0], 'isisL3Router'))[0],
    '-discardLSPs');

my $isisL3RouterDiscardLearnedLSP2 = $ixNet->getAttribute(($ixNet->getList($t2devices[0], 'isisL3Router'))[0],
    '-discardLSPs');

$ixNet->setAttribute($isisL3RouterDiscardLearnedLSP1,
     '-pattern', 'singleValue',
	 '-clearOverlays', 'False');
$ixNet->setAttribute($isisL3RouterDiscardLearnedLSP1.'/singleValue', '-value', 'false');

$ixNet->setAttribute($isisL3RouterDiscardLearnedLSP2,
    '-pattern', 'singleValue',
	'-clearOverlays', 'False');
$ixNet->setAttribute($isisL3RouterDiscardLearnedLSP2.'/singleValue', '-value', 'false');

print('$ixNet->help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2\')\n');
$ixNet->commit();

# Adding Network group behind DeviceGroup
print("Adding NetworkGroup behind ISIS DG\n");
$ixNet->execute('createDefaultStack', $t1dev1, 'networkTopology');
$ixNet->execute('createDefaultStack', $t2dev1, 'networkTopology');
my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
my $networkGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];

$ixNet->setAttribute($networkGroup1, '-name', 'ISIS_1_Network_Group1');
$ixNet->setAttribute($networkGroup2, '-name', 'ISIS_2_Network_Group1');
$ixNet->commit();

# Enabling Host name in Simulated ISIS Routers
print("Enabling Host name in Simulated ISIS Routers\n");
my $networkTopology1 = ($ixNet->getList($networkGroup1, 'networkTopology'))[0];
my $isisL3SimulatedTopologyConfig1 = ($ixNet->getList($networkTopology1, 'isisL3SimulatedTopologyConfig'))[0];
my $enableHostName1 = ($ixNet->getAttribute($isisL3SimulatedTopologyConfig1, '-enableHostName'));
$ixNet->setAttribute($enableHostName1.'/singleValue', '-value', 'True');
$ixNet->commit();
my $configureHostName1 = ($ixNet->getAttribute($isisL3SimulatedTopologyConfig1, '-hostName'));
$ixNet->setAttribute($configureHostName1.'/singleValue', '-value', 'isisL3SimulatedRouter1');
$ixNet->commit();

my $networkTopology2 = ($ixNet->getList($networkGroup2, 'networkTopology'))[0];
my $isisL3SimulatedTopologyConfig2 = ($ixNet->getList($networkTopology2, 'isisL3SimulatedTopologyConfig'))[0];
my $enableHostName2 = ($ixNet->getAttribute($isisL3SimulatedTopologyConfig2, '-enableHostName'));
$ixNet->setAttribute($enableHostName2.'/singleValue', '-value', 'True');
$ixNet->commit();
my $configureHostName2 = ($ixNet->getAttribute($isisL3SimulatedTopologyConfig2, '-hostName'));
$ixNet->setAttribute($configureHostName2.'/singleValue', '-value', 'isisL3SimulatedRouter2');
$ixNet->commit();

# Add ipv4 loopback1 for applib traffic
print("Adding ipv4 loopback1 for applib traffic\n");
my $chainedDg1 = $ixNet->add($networkGroup1, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg1, '-multiplier', '7', '-name', 'Device Group 4');
$ixNet->commit();
$chainedDg1 = ($ixNet->remapIds($chainedDg1))[0];

my $loopback1 = $ixNet->add($chainedDg1, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback1, '-stackedLayers', '', '-name', 'IPv4 Loopback 2');
$ixNet->commit();

my $connector1 = $ixNet->add($loopback1, 'connector');
$ixNet->setMultiAttribute($connector1,
     '-connectedTo', $networkGroup1.'/networkTopology/simRouter:1');
$ixNet->commit();

my $connector1 = ($ixNet->remapIds($connector1))[0];

my $addressSet1 = $ixNet->getAttribute($loopback1, '-address');
$ixNet->setMultiAttribute($addressSet1, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$addressSet1 = $ixNet->add($addressSet1, 'counter');
$ixNet->setMultiAttribute($addressSet1, '-step', '0.1.0.0',
    '-start', '201.1.0.0', '-direction', 'increment');
$ixNet->commit();
my $addressSet1 = ($ixNet->remapIds($addressSet1))[0];

# Add ipv4 loopback2 for applib traffic
print("Adding ipv4 loopback2 for applib traffic\n");
my $chainedDg2 = $ixNet->add($networkGroup2, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg2, '-multiplier', '7', '-name', 'Device Group 3');
$ixNet->commit();
$chainedDg2 = ($ixNet->remapIds($chainedDg2))[0];

my $loopback2 = $ixNet->add($chainedDg2, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback2, '-stackedLayers', '', '-name', 'IPv4 Loopback 1');
$ixNet->commit();

my $connector2 = $ixNet->add($loopback2, 'connector');
$ixNet->setMultiAttribute($connector2, '-connectedTo',
    $networkGroup2.'/networkTopology/simRouter:1');
$ixNet->commit();
$connector2 = ($ixNet->remapIds($connector2))[0];

my $addressSet2 = $ixNet->getAttribute($loopback2, '-address');
$ixNet->setMultiAttribute($addressSet2, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$addressSet2 = $ixNet->add($addressSet2, 'counter');
$ixNet->setMultiAttribute($addressSet2, '-step', '0.1.0.0',
    '-start', '206.1.0.0', '-direction', 'increment');
$ixNet->commit();
$addressSet2 = ($ixNet->remapIds($addressSet2))[0];

# Add ipv6 loopback1 for applib traffic
print("Adding ipv6 loopback1 for applib traffic\n");
my $chainedDg3 = $ixNet->add($networkGroup1, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg3, '-multiplier', '7', '-name', 'Device Group 6');
$ixNet->commit();
$chainedDg3 = ($ixNet->remapIds($chainedDg3))[0];

my $loopback1 = $ixNet->add($chainedDg3, 'ipv6Loopback');
$ixNet->setMultiAttribute($loopback1, '-stackedLayers', '', '-name', 'IPv6 Loopback 1');
$ixNet->commit();

my $connector1 = $ixNet->add($loopback1, 'connector');
$ixNet->setMultiAttribute($connector1, '-connectedTo',
    $networkGroup1.'/networkTopology/simRouter:1');
$ixNet->commit();
$connector1 = ($ixNet->remapIds($connector1))[0];

my $addressSet1 = $ixNet->getAttribute($loopback1, '-address');
$ixNet->setMultiAttribute($addressSet1, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$addressSet1 = $ixNet->add($addressSet1, 'counter');
$ixNet->setMultiAttribute($addressSet1, '-step', '::1',
    '-start', '2010::1', '-direction', 'increment');
$ixNet->commit();
$addressSet1 = ($ixNet->remapIds($addressSet1))[0];


# Add ipv6 loopback2 for applib traffic
print("Adding ipv6 loopback2 for applib traffic\n");
my $chainedDg4 = $ixNet->add($networkGroup2, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg4, '-multiplier', '7', '-name', 'Device Group 5');
$ixNet->commit();
$chainedDg4 = ($ixNet->remapIds($chainedDg4))[0];

my $loopback2 = $ixNet->add($chainedDg4, 'ipv6Loopback');
$ixNet->setMultiAttribute($loopback2, '-stackedLayers', '', '-name', 'IPv6 Loopback 2');
$ixNet->commit();

my $connector2 = $ixNet->add($loopback2, 'connector');
$ixNet->setMultiAttribute($connector2, '-connectedTo',
    $networkGroup2.'/networkTopology/simRouter:1');
$ixNet->commit();
$connector2 = ($ixNet->remapIds($connector2))[0];

my $addressSet2 = $ixNet->getAttribute($loopback2, '-address');
$ixNet->setMultiAttribute($addressSet2, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$addressSet2 = $ixNet->add($addressSet2, 'counter');
$ixNet->setMultiAttribute($addressSet2, '-step', '::1',
    '-start', '2060::1', '-direction', 'increment');
$ixNet->commit();
$addressSet2 = ($ixNet->remapIds($addressSet2))[0];

################################################################################
# Start ISIS protocol and wait for 60 seconds
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);

################################################################################
# Retrieve protocol statistics
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
# Retrieve protocol learned info
###############################################################################
print("Fetching ISIS Learned Info\n");
$ixNet->execute('getLearnedInfo', $isisL3_1, '1');
sleep(5);
my $linfo  = ($ixNet->getList($isisL3_1, 'learnedInfo'))[0];
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
# Enable ISISL3 simulated topology's ISIS Simulated IPv4 & IPv6 Node Routes,
# which was disabled by default. And apply changes On The Fly (OTF).
################################################################################
print("Enabling IPv4 & IPv6 Simulated Node Routes\n");
my $netTopology1      = ($ixNet->getList($networkGroup1, 'networkTopology'))[0];
my $simRouter1        = ($ixNet->getList($netTopology1, 'simRouter'))[0];
my $isisL3PseudoRouter1 = ($ixNet->getList($simRouter1, 'isisL3PseudoRouter'))[0];
my $ipv4PseudoNodeRoutes1  = ($ixNet->getList($isisL3PseudoRouter1, 'IPv4PseudoNodeRoutes'))[0];
my $ipv4PseudoNodeRouteMultivalue1 = ($ixNet->getAttribute($ipv4PseudoNodeRoutes1, '-active'));

$ixNet->setAttribute($ipv4PseudoNodeRouteMultivalue1.'/singleValue', '-value', 'true');

my $ipv6PseudoNodeRoutes1 = ($ixNet->getList($isisL3PseudoRouter1, 'IPv6PseudoNodeRoutes'))[0];
my $ipv6PseudoNodeRouteMultivalue1 = ($ixNet->getAttribute($ipv6PseudoNodeRoutes1, '-active'));

$ixNet->setAttribute($ipv6PseudoNodeRouteMultivalue1.'/singleValue', '-value', 'true');
$ixNet->commit();

my $netTopology2       = ($ixNet->getList($networkGroup2, 'networkTopology'))[0];
my $simRouter2         = ($ixNet->getList($netTopology2, 'simRouter'))[0];
my $isisL3PseudoRouter2 = ($ixNet->getList($simRouter2, 'isisL3PseudoRouter'))[0];
my $ipv4PseudoNodeRoutes2         = ($ixNet->getList($isisL3PseudoRouter2, 'IPv4PseudoNodeRoutes'))[0];
my $ipv4PseudoNodeRouteMultivalue2 = ($ixNet->getAttribute($ipv4PseudoNodeRoutes2, '-active'));

$ixNet->setAttribute($ipv4PseudoNodeRouteMultivalue2.'/singleValue', '-value', 'true');

my $ipv6PseudoNodeRoutes2 = ($ixNet->getList($isisL3PseudoRouter2, 'IPv6PseudoNodeRoutes'))[0];
my $ipv6PseudoNodeRouteMultivalue2 = ($ixNet->getAttribute($ipv6PseudoNodeRoutes2, '-active'));
$ixNet->commit();
sleep(5);

################################################################################
# Stop/Start ISIS Router on both ports and apply changes on-the-fly
################################################################################
print("Stop ISIS Router on both ports and apply changes on-the-fly\n");
my $deviceGroup1 = ($ixNet->getList($topo1, 'deviceGroup'))[0];
my $isisL3Router1 = ($ixNet->getList($deviceGroup1, 'isisL3Router'))[0];
my $isisL3RouterDeactivate1 = $ixNet->getAttribute($isisL3Router1, '-active');

my $deviceGroup2 = ($ixNet->getList($topo2, 'deviceGroup'))[0];
my $isisL3Router2 = ($ixNet->getList($deviceGroup2, 'isisL3Router'))[0];
my $isisL3RouterDeactivate2 = $ixNet->getAttribute($isisL3Router2, '-active');

$ixNet->setAttribute($isisL3RouterDeactivate1.'/singleValue', '-value', 'False');
$ixNet->setAttribute($isisL3RouterDeactivate2.'/singleValue', '-value', 'False');
$ixNet->commit();

my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
print("Wait for 30 seconds ...");
sleep(30);
################################################################################
# Start ISIS Router on both ports and apply changes on-the-fly
################################################################################
print("Start ISIS Router on both ports and apply changes on-the-fly\n");
my $deviceGroup1 = ($ixNet->getList($topo1, 'deviceGroup'))[0];
my $isisL3Router1 = ($ixNet->getList($deviceGroup1, 'isisL3Router'))[0];
my $isisL3RouterActivate1 = $ixNet->getAttribute($isisL3Router1, '-active');

my $deviceGroup2 = ($ixNet->getList($topo2, 'deviceGroup'))[0];
my $isisL3Router2 = ($ixNet->getList($deviceGroup2, 'isisL3Router'))[0];
my $isisL3RouterActivate2 = $ixNet->getAttribute($isisL3Router2, '-active');

$ixNet->setAttribute($isisL3RouterActivate1.'/singleValue', '-value', 'True');
$ixNet->setAttribute($isisL3RouterActivate2.'/singleValue', '-value', 'True');
$ixNet->commit();

my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
print("Wait for 30 seconds ...\n");
sleep(30);

###############################################################################
# Retrieve protocol learned info again and compare with
# previously retrieved learned info.  
###############################################################################
print("Fetching ISISL3 learned info after enabling IPv4 Node Routes\n");
$ixNet->execute('getLearnedInfo', $isisL3_1, '1');
sleep(5);
my $linfo  = ($ixNet->getList($isisL3_1, 'learnedInfo'))[0];
my @values = $ixNet->getAttribute($linfo, '-values');
my $v      = '';
print("***************************************************\n");
foreach $v (@values) {
 	my $w = '0';
	foreach $w (@$v) {
	    printf("%15s", $w);
	}
	print("\n");
}
print("***************************************************\n");

print("Fetching ISISL3 IPv6 Learned Info\n");
$ixNet->execute('getLearnedInfo', $isisL3_1, '1');
sleep(5);
my $linfo = ($ixNet->getList($isisL3_1, 'learnedInfo'))[0];
my $ipv6table = ($ixNet->getList($linfo, 'table'))[1];
     my @values   = $ixNet->getAttribute($ipv6table, '-values');
     my $v        = ''; 
	 

print("***************************************************\n");
foreach $v (@values) {
 	my $w = '0';
	foreach $w (@$v) {
	    printf("%15s", $w);
	}    
	print("\n");
}
print("***************************************************\n");

################################################################################
# Configure L2-L3 traffic 
################################################################################
print ("Congfiguring L2-L3 IPv4 Traffic Item\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ipv4');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source       = ($networkGroup1.'/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv4PseudoNodeRoutes:1');
my @destination  = ($networkGroup2.'/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv4PseudoNodeRoutes:1');

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
    '-trackBy',        ['sourceDestEndpointPair0','trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();

print ("Congfiguring L2-L3 IPv6 Traffic Item\n");
my $trafficItem2 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem2, '-name', 'Traffic Item 2',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ipv6');
$ixNet->commit();

$trafficItem2    = ($ixNet->remapIds($trafficItem2))[0];
my $endpointSet1 = $ixNet->add($trafficItem2, 'endpointSet');
my @source       = ($networkGroup1.'/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1');
my @destination  = ($networkGroup2.'/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1');

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

$ixNet->setMultiAttribute($trafficItem2.'/tracking',
    '-trackBy',        ['sourceDestEndpointPair0','trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();
################################################################################
# Configure Application traffic
################################################################################
# Configuring Applib traffic
print ("Configuring Applib traffic profile  $trafficType \n");
my $trafficItem2 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem2, '-name', 'Traffic Item 3',
    '-trafficItemType', 'applicationLibrary',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', $trafficType);
$ixNet->commit();
my $trafficItem2 = ($ixNet->remapIds($trafficItem2))[0];

my $endpointSet2 = $ixNet->add($trafficItem2, 'endpointSet');
my @source_app = (($ixNet->getList($t1dev1, 'networkGroup'))[0]);
my @destin_app = (($ixNet->getList($t2dev1, 'networkGroup'))[0]);

$ixNet->setMultiAttribute($endpointSet2,
    '-name',                  'EndpointSet-2',
    '-multicastDestinations', (''),
    '-scalableSources',       (''),
    '-multicastReceivers',    (''),
    '-scalableDestinations',  (''),
    '-ngpfFilters',           (''),
    '-trafficGroups',         (''),
    '-sources',               @source_app,
    '-destinations',          @destin_app);    
$ixNet->commit();
$endpointSet2 = ($ixNet->remapIds($endpointSet2))[0];

my $appLibProfile  = $ixNet->add($trafficItem2, 'appLibProfile');
my $flows_configured  = ('Bandwidth_BitTorrent_File_Download',
                         'Bandwidth_eDonkey',
                         'Bandwidth_HTTP',
                         'Bandwidth_IMAPv4',
                         'Bandwidth_POP3',
                         'Bandwidth_Radius',
                         'Bandwidth_Raw',
                         'Bandwidth_Telnet',
                         'Bandwidth_uTorrent_DHT_File_Download',
                         'BBC_iPlayer',
                         'BBC_iPlayer_Radio',
                         'BGP_IGP_Open_Advertise_Routes',
                         'BGP_IGP_Withdraw_Routes',
                         'Bing_Search',
                         'BitTorrent_Ares_v217_File_Download',
                         'BitTorrent_BitComet_v126_File_Download',
                         'BitTorrent_Blizzard_File_Download',
                         'BitTorrent_Cisco_EMIX',
                         'BitTorrent_Enterprise',
                         'BitTorrent_File_Download',
                         'BitTorrent_LimeWire_v5516_File_Download',
                         'BitTorrent_RMIX_5M');

$ixNet->setMultiAttribute($appLibProfile,
    '-enablePerIPStats', 'false',
    '-objectiveDistribution', 'applyFullObjectiveToEachPort',
    '-configuredFlows', $flows_configured);
$ixNet->commit();
my $appLibProfile = ($ixNet->remapIds($appLibProfile))[0];

print("$ixNet->help(\'[ixNet getRoot]/traffic\')\n");

###############################################################################
# Apply and start L2/L3 traffic
###############################################################################
print("Applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

###############################################################################
# Apply and start applib traffic
###############################################################################
print("Applying applib traffic\n");
$ixNet->execute('applyStatefulTraffic',  $ixNet->getRoot().'/traffic');
sleep(5);

print("starting applib traffic\n");
$ixNet->execute('startStatefulTraffic', $ixNet->getRoot().'/traffic');
print("Let traffic run for 1 minute\n");
sleep(60);

###############################################################################
# Retrieve Applib traffic item statistics
###############################################################################
print("Verifying all the applib traffic stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"Application Traffic Item Statistics"/page';
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
# Retrieve L2/L3 traffic item statistics
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
# Stop applib traffic
#################################################################################
print("Stopping applib traffic\n");
$ixNet->execute('stopStatefulTraffic', ($ixNet->getRoot()).'/traffic');
sleep(5);

#################################################################################
# Stop L2/L3 traffic
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# Stop all protocols
################################################################################
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!");

