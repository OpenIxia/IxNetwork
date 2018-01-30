################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    04/09/2015 - Sumeer Kumar - created sample                                #
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
#                                                                              #
# About Topology:                                                              #
#     On each port, it will create one topology of LDP dual stack router.      #
#     In each topology, there will be one device group and a network group.    #
#     The device group will simulate as a LDP dual stack router having LDP and #
#     LDPv6 interface over IPv4 and IPv6 stack respectively and a basic LDP    #
#     dual stack router connected to both IPv4 and IPv6 interface. The         #
#     transport connection preference in LDP router is set to IPv6.            #
#     The network groups consists of both IPv4 and IPv6 prefix pools.          #
#     Traffic is configured in between IPv6 prefix pools as end points.        #       
#                                                                              #
# Script Flow:                                                                 #
#    1. Configuration of protocols as described in topology.                   #
#    2. Start the LDP protocol.                                                #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Change LDP FEC labels & apply change on the fly                        #
#    6. Retrieve protocol learned info again.                                  #
#    7. Configure L2-L3 traffic.                                               #
#    8. Start the L2-L3 traffic.                                               #
#   11. Retrieve L2-L3 traffic stats.                                          #
#   12. Stop L2-L3 traffic.                                                    #
#   13. Stopallprotocols.                                                      #
#                                                                              #                                                                                
# Ixia Software:                                                               #
#    IxOS      6.90 EA                                                         #
#    IxNetwork 7.50 EA                                                         #
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
my $ixTclPort   = '8981';
my @ports       = (('10.205.28.12', '6', '1'), ('10.205.28.12', '6', '2'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '7.50',
    '-setAttribute', 'strict');

print("Creating a new config\n");
$ixNet->execute('newConfig');

################################################################################
# Protocol configuration section                                               #
# Configure LDPv6 as per the description given above                           #
################################################################################ 
print("Adding two virtual ports\n");
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->commit();

my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vportTx = $vPorts[0];
my $vportRx = $vPorts[1];
assignPorts($ixNet, @ports, $vportTx, $vportRx);
sleep(5);

print("Adding two topologies\n");
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', $vportTx);
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', $vportRx);
$ixNet->commit();

my @topologies = $ixNet->getList($ixNet->getRoot(), 'topology');
my $topo1 = $topologies[0];
my $topo2 = $topologies[1];

print("Adding one device group in each topology\n");
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

print("Adding Ethernet/MAC endpoints for the device groups\n");
$ixNet->add($t1dev1, 'ethernet');
$ixNet->add($t2dev1, 'ethernet');
$ixNet->commit();

my $mac1 = ($ixNet->getList($t1dev1, 'ethernet'))[0];
my $mac2 = ($ixNet->getList($t2dev1, 'ethernet'))[0];

print("Configuring the MAC addresses for the device groups\n");
$ixNet->setMultiAttribute($ixNet->getAttribute($mac1, '-mac').'/counter',
        '-direction', 'increment',
        '-start',     '00:11:01:00:00:01',
        '-step',      '00:00:00:00:00:01');

$ixNet->setAttribute($ixNet->getAttribute($mac2, '-mac').'/singleValue',
        '-value', '00:12:01:00:00:01');
$ixNet->commit();

print("Adding IPv4 and IPv6 over Ethernet stack for both device groups\n");
$ixNet->add($mac1, 'ipv4');
$ixNet->add($mac2, 'ipv4');
$ixNet->add($mac1, 'ipv6');
$ixNet->add($mac2, 'ipv6');
$ixNet->commit();

my $ipv41 = ($ixNet->getList($mac1, 'ipv4'))[0];
my $ipv42 = ($ixNet->getList($mac2, 'ipv4'))[0];
my $ipv61 = ($ixNet->getList($mac1, 'ipv6'))[0];
my $ipv62 = ($ixNet->getList($mac2, 'ipv6'))[0];

my $mvAddv41 = $ixNet->getAttribute($ipv41, '-address');
my $mvAddv42 = $ixNet->getAttribute($ipv42, '-address');
my $mvAddv61 = $ixNet->getAttribute($ipv61, '-address');
my $mvAddv62 = $ixNet->getAttribute($ipv62, '-address');

my $mvGwv41  = $ixNet->getAttribute($ipv41, '-gatewayIp');
my $mvGwv42  = $ixNet->getAttribute($ipv42, '-gatewayIp');
my $mvGwv61  = $ixNet->getAttribute($ipv61, '-gatewayIp');
my $mvGwv62  = $ixNet->getAttribute($ipv62, '-gatewayIp');

print("Configuring IPv4 addresses for both device groups\n");
$ixNet->setAttribute($mvAddv41.'/singleValue', '-value', '100.1.0.2');
$ixNet->setAttribute($mvAddv42.'/singleValue', '-value', '100.1.0.1');
$ixNet->setAttribute($mvGwv41.'/singleValue', '-value', '100.1.0.1');
$ixNet->setAttribute($mvGwv42.'/singleValue', '-value', "100.1.0.2");

print("Configuring IPv6 addresses for both device groups\n");
$ixNet->setAttribute($mvAddv61.'/singleValue', '-value', '2000:0:0:1:0:0:0:2');
$ixNet->setAttribute($mvAddv62.'/singleValue', '-value', '2000:0:0:1:0:0:0:1');
$ixNet->setAttribute($mvGwv61.'/singleValue', '-value', '2000:0:0:1:0:0:0:1');
$ixNet->setAttribute($mvGwv62.'/singleValue', '-value', "2000:0:0:1:0:0:0:2");

print("Configuring IPv4 prefix for both device groups\n");
$ixNet->setAttribute($ixNet->getAttribute($ipv41, '-prefix').'/singleValue', '-value', '24');
$ixNet->setAttribute($ixNet->getAttribute($ipv42, '-prefix').'/singleValue', '-value', '24');

print("Configuring IPv6 prefix for both device groups\n");
$ixNet->setAttribute($ixNet->getAttribute($ipv61, '-prefix').'/singleValue', '-value', '64');
$ixNet->setAttribute($ixNet->getAttribute($ipv62, '-prefix').'/singleValue', '-value', '64');

$ixNet->setMultiAttribute($ixNet->getAttribute($ipv41, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv42, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv61, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv62, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

print("Adding LDP Connected Interface over IPv4 stack\n");
$ixNet->add($ipv41, 'ldpConnectedInterface');
$ixNet->add($ipv42, 'ldpConnectedInterface');
$ixNet->commit();

my $ldpIf1 = ($ixNet->getList($ipv41, 'ldpConnectedInterface'))[0];
my $ldpIf2 = ($ixNet->getList($ipv42, 'ldpConnectedInterface'))[0];

print("Adding LDPv6 Connected Interface over IPv6 stack\n");
$ixNet->add($ipv61, 'ldpv6ConnectedInterface');
$ixNet->add($ipv62, 'ldpv6ConnectedInterface');
$ixNet->commit();

my $ldpv6If1 = ($ixNet->getList($ipv61, 'ldpv6ConnectedInterface'))[0];
my $ldpv6If2 = ($ixNet->getList($ipv62, 'ldpv6ConnectedInterface'))[0];

print("Adding LDPv6 dual stack router in both device groups\n");
$ixNet->add($t1dev1, 'ldpBasicRouterV6');
$ixNet->add($t2dev1, 'ldpBasicRouterV6');
$ixNet->commit();

my @ldpv6DualStackRouter1 = $ixNet->getList($t1dev1, 'ldpBasicRouterV6');
my @ldpv6DualStackRouter2 = $ixNet->getList($t2dev1, 'ldpBasicRouterV6');

$ixNet->setAttribute($ipv41, '-stackedLayers', @ldpv6DualStackRouter1);
$ixNet->setAttribute($ipv61, '-stackedLayers', @ldpv6DualStackRouter1);

$ixNet->setAttribute($ipv42, '-stackedLayers', @ldpv6DualStackRouter2);
$ixNet->setAttribute($ipv62, '-stackedLayers', @ldpv6DualStackRouter2);
$ixNet->commit();

print("Setting IPv6 as transport connection preference\n");
my $sessionPreference1 = $ixNet->getAttribute(@ldpv6DualStackRouter1, '-sessionPreference');
my $sessionPreference2 = $ixNet->getAttribute(@ldpv6DualStackRouter2, '-sessionPreference');

my $singleValue1 = ($ixNet->getList($sessionPreference1, 'singleValue'))[0];
my $singleValue2 = ($ixNet->getList($sessionPreference2, 'singleValue'))[0];

$ixNet->setAttribute($singleValue1, '-value', 'ipv6');
$ixNet->setAttribute($singleValue2, '-value', 'ipv6');
$ixNet->commit();

print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'LDPv6 Topology 1');
$ixNet->setAttribute($topo2, '-name', 'LDPv6 Topology 2');

$ixNet->setAttribute($t1dev1, '-name', 'LDP Dual Stack Router 1');
$ixNet->setAttribute($t2dev1, '-name', 'LDP Dual Stack Router 2');
$ixNet->commit();

print("Adding Network Group behind LDPv6 dual stack DG\n");
$ixNet->add($t1dev1, 'networkGroup');
$ixNet->add($t2dev1, 'networkGroup');
$ixNet->commit();

my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
my $networkGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];

$ixNet->setAttribute($networkGroup1, '-name', 'LDP_1_Network_Group1');
$ixNet->setAttribute($networkGroup2, '-name', 'LDP_2_Network_Group1');
$ixNet->setAttribute($networkGroup1, '-multiplier', '1');
$ixNet->setAttribute($networkGroup2, '-multiplier', '1');
$ixNet->commit();

print("Adding IPv4 and Ipv6 prefix pools in Network Groups\n");
$ixNet->add($networkGroup1, 'ipv6PrefixPools');
$ixNet->add($networkGroup1, 'ipv4PrefixPools');
$ixNet->add($networkGroup2, 'ipv6PrefixPools');
$ixNet->add($networkGroup2, 'ipv4PrefixPools');
$ixNet->commit();

my $ipv6PrefixPools1 = ($ixNet->getList($networkGroup1, 'ipv6PrefixPools'))[0];
my $ipv4PrefixPools1 = ($ixNet->getList($networkGroup1, 'ipv4PrefixPools'))[0];

my $ipv6PrefixPools2 = ($ixNet->getList($networkGroup2, 'ipv6PrefixPools'))[0];
my $ipv4PrefixPools2 = ($ixNet->getList($networkGroup2, 'ipv4PrefixPools'))[0];

print("Changing count of network group address\n");
$ixNet->setMultiAttribute($ipv6PrefixPools1, '-numberOfAddresses', '5');
$ixNet->setMultiAttribute($ipv4PrefixPools1, '-numberOfAddresses', '5');
$ixNet->setMultiAttribute($ipv6PrefixPools2, '-numberOfAddresses', '5');
$ixNet->setMultiAttribute($ipv4PrefixPools2, '-numberOfAddresses', '5');
$ixNet->commit();

print("All configuration is completed..Wait for 5 seconds...\n");
sleep(5);

################################################################################
# Start LDPv6 protocol and wait for 60 seconds                                 #  
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);

################################################################################
# Retrieve protocol statistics                                                 #
################################################################################
print("Fetching LDP Per Port Stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"LDP Per Port"/page';
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
# Retrieve protocol learned info                                                #
#################################################################################
print("Fetching LDPv6 Basic Learned Info\n");
$ixNet->execute('getIPv4FECLearnedInfo', @ldpv6DualStackRouter1, '1');
$ixNet->execute('getIPv6FECLearnedInfo', @ldpv6DualStackRouter1, '1');
sleep(5);
my @linfoList  = ($ixNet->getList(@ldpv6DualStackRouter1, 'learnedInfo'));
print("***************************************************\n");
my $linfo = '';
foreach $linfo (@linfoList) { 
    my @values = $ixNet->getAttribute($linfo, '-values');
    my $v      = '';
    print("***************************************************\n");
    foreach $v (@values) {
 	    my $w = '0';
	    foreach $w (@$v) {
	        printf("%12s", $w);
	    }
	    print("\n");
    }
}
print("***************************************************\n");

################################################################################
# Change the labels of FEC elements                                            #
################################################################################
print("Changing Labels of LDP and LDPv6 FEC Range on second Network Group\n");
my $ldpFEC2 = ($ixNet->getList($ipv4PrefixPools2, 'ldpFECProperty'))[0];
my $ldpv6FEC2 = ($ixNet->getList($ipv6PrefixPools2, 'ldpIpv6FECProperty'))[0];

my $labelV4MultiValue2 = $ixNet->getAttribute($ldpFEC2, '-labelValue');
$ixNet->setMultiAttribute($labelV4MultiValue2, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();
my $labelSetV4 = $ixNet->add($labelV4MultiValue2, 'counter');
$ixNet->setMultiAttribute($labelSetV4, '-step', '5', '-start', '30', '-direction', 'increment');

my $labelV6MultiValue2 = $ixNet->getAttribute($ldpv6FEC2, '-labelValue');
$ixNet->setMultiAttribute($labelV6MultiValue2, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();
my $labelSetV6 = $ixNet->add($labelV6MultiValue2, 'counter');
$ixNet->setMultiAttribute($labelSetV6, '-step', '10', '-start', '60', '-direction', 'decrement');
$ixNet->commit();
sleep(2);

################################################################################
# Applying changes one the fly                                                 #
################################################################################
print("Applying changes on the fly\n");
my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);

#################################################################################
# Retrieve protocol learned info again                                          #
#################################################################################
print("Fetching LDPv6 Basic Learned Info again after changing labels on the fly\n");
$ixNet->execute('getIPv4FECLearnedInfo', @ldpv6DualStackRouter1, '1');
$ixNet->execute('getIPv6FECLearnedInfo', @ldpv6DualStackRouter1, '1');
sleep(5);
my @linfoList  = ($ixNet->getList(@ldpv6DualStackRouter1, 'learnedInfo'));
print("***************************************************\n");
my $linfo = '';
foreach $linfo (@linfoList) { 
    my @values = $ixNet->getAttribute($linfo, '-values');
    my $v      = '';
    print("***************************************************\n");
    foreach $v (@values) {
 	    my $w = '0';
	    foreach $w (@$v) {
	        printf("%12s", $w);
	    }
	    print("\n");
    }
}
print("***************************************************\n");

#################################################################################
# Configure L2-L3 traffic                                                       #
#################################################################################
print ("Congfiguring L2/L3 Traffic Item\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
	'-biDirectional', 'true',
    '-trafficType', 'ipv6');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source       = ($networkGroup1.'/ipv6PrefixPools:1');
my @destination  = ($networkGroup2.'/ipv6PrefixPools:1');

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
# Apply L2/L3 traffic                                                         #
###############################################################################
print("Applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

###############################################################################
# Start L2/L3 traffic                                                         #
###############################################################################
print("Starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

print("Let traffic run for 60 seconds\n");
sleep(60);

###############################################################################
# Retrieve L2/L3 traffic item statistics                                      #
###############################################################################
print("Retrieving all L2/L3 traffic stats\n");
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
# Stop all protocols                                                          #
################################################################################
print("Stopping all protocols\n");
$ixNet->execute('stopAllProtocols');

print("!!! Test Script Ends !!!\n");
