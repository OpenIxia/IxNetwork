#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: #2 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    19/01/2015 - Sumit Deb - created sample                                #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter("the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not guarantee (i) that the functions contained in the script will   #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED("AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
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
#    This script intends to demonstrate how to use NGPF OSPFv2 API.            #
#                                                                              #
#    1. Create 2 interfaces with OSPFv2 enabled, each having 1 OSPFv2          #
#       router with 10 route-ranges per router with first 5 enabled			   #
#    2. Start the ospfv2 protocol.                                             #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Enable remaining route-ranges on each OSPFv2 router                    #
#    6. Disable and enable router interfaces to reflect changes                # 
#    7. Retrieve protocol learned info.                                        #                                     
#    8. Configure L2-L3 traffic.                                               #
#    9. Start the L2-L3 traffic.                                               #
#    10. Retrieve L2-L3 traffic stats.                                         #
#    11. Stop L2-L3 traffic.                                                   #
#    12. Stop all protocols.                                                   #       #                                                                              #              
# Ixia Softwares:                                                              #
#    IxOS      6.80 EA (6.80.1100.7)                                           #
#    IxNetwork 7.40 EA (7.40.929.15)                                           #
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
	my $ixNet  = $my_resource[0];
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
my $ixTclPort   = '5555';
#my @ports       = (('10.205.28.71', '2', '15'), ('10.205.28.71', '2', '16'));
my @ports       = (('xm2-10', '2', '13'), ('xm2-10', '2', '14'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '7.40',
    '-setAttribute', 'strict');

print("Creating a new config\n");
$ixNet->execute('newConfig');

################################################################################
# 1. Protocol configuration section. Configure OSPFv2 as per the description
#    give above
################################################################################ 
print("Add 2 Virtual ports\n");
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->commit();

my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vPort1 = $vPorts[0];
my $vPort2 = $vPorts[1];
assignPorts($ixNet, @ports, $vPort1, $vPort2);
sleep(5);

################################################################################
# setting ipv4 interfaces
################################################################################
print("Add ipv4 interfaces\n");
my $interface1 = $ixNet->add($vPort1, 'interface');
my $ipv4_1 = $ixNet->add($interface1, 'ipv4');
my $interface2 = $ixNet->add($vPort2, 'interface');
my $ipv4_2 = $ixNet->add($interface2, 'ipv4');
$ixNet->commit();

################################################################################
# enabling protocol interface
################################################################################
print("Enable protocol interface\n");
$ixNet->setAttribute($interface1, '-enabled', 'true');
$ixNet->setAttribute($interface2, '-enabled', 'true');
$ixNet->commit();

################################################################################
# configuring ip and gateway on each interface
################################################################################
print("Add IP address, Gateway and Mask on Protocol Interface 1\n");
$ixNet->setAttribute($ipv4_1, '-ip', '20.20.20.1');
$ixNet->setAttribute($ipv4_1, '-maskWidth', '24');
$ixNet->setAttribute($ipv4_1, '-gateway', '20.20.20.2');
$ixNet->commit();
print("Add IP address, Gateway and Mask on Protocol Interface 2\n");
$ixNet->setAttribute($ipv4_2, '-ip', '20.20.20.2');
$ixNet->setAttribute($ipv4_2, '-maskWidth', '24');
$ixNet->setAttribute($ipv4_2, '-gateway', '20.20.20.1');
$ixNet->commit();

################################################################################
# Enable OSPFv2 on ports
################################################################################
# Enable ospf from protocol management
my $protocol1 = ($ixNet->getList($vPort1, 'protocols'))[0];
my $ospf1 = ($ixNet->getList($protocol1, 'ospf'))[0];
$ixNet->setAttribute($ospf1, '-enabled', 'true');
$ixNet->commit();

my $protocol2 = ($ixNet->getList($vPort2, 'protocols'))[0];
my $ospf2 = ($ixNet->getList($protocol2, 'ospf'))[0];
$ixNet->setAttribute($ospf2, '-enabled', 'true');
$ixNet->commit();

################################################################################
# Configure OSPFv2 routers on ports
################################################################################
$ixNet->add($ospf1, 'router');
$ixNet->commit();
my $router1 = ($ixNet->getList($ospf1, 'router'))[0];
$ixNet->setAttribute($router1, '-enabled', 'true');
$ixNet->setAttribute($router1, '-routerId', '1.1.1.1');
$ixNet->setAttribute($router1, '-discardLearnedLsa', 'false');
$ixNet->commit();

$ixNet->add($ospf2, 'router');
$ixNet->commit();
my $router2 = ($ixNet->getList($ospf2, 'router'))[0];
$ixNet->setAttribute($router2, '-enabled', 'true');
$ixNet->setAttribute($router2, '-routerId', '2.2.2.2');
$ixNet->setAttribute($router2, '-discardLearnedLsa', 'false');
$ixNet->commit();

################################################################################
# Configure interfaces on OSPFv2 routers 
################################################################################
$ixNet->add($router1, 'interface');
$ixNet->commit();
my $router1Interface = ($ixNet->getList($router1, 'interface'))[0];
print "router1Interface : $router1Interface";
$ixNet->setAttribute($router1Interface, '-connectedToDut', 'true');
$ixNet->setAttribute($router1Interface, '-protocolInterface', $interface1);
$ixNet->setAttribute($router1Interface, '-enabled', 'true');
$ixNet->setAttribute($router1Interface, '-networkType', 'pointToPoint');
$ixNet->commit();

$ixNet->add($router2, 'interface');
$ixNet->commit();
my $router2Interface = ($ixNet->getList($router2, 'interface'))[0];
$ixNet->setAttribute($router2Interface, '-connectedToDut', 'true');
$ixNet->setAttribute($router2Interface, '-protocolInterface', $interface2);
$ixNet->setAttribute($router2Interface, '-enabled', 'true');
$ixNet->setAttribute($router2Interface, '-networkType', 'pointToPoint');
$ixNet->commit();

#######################################################################################
# Configure 10 route range on each OSPFv2 router , enable only the first 5 route ranges
#######################################################################################
for(my $count = 1; $count <= 10; $count++ ){
	my $index = $count - 1;
	$ixNet->add($router1, 'routeRange');
	$ixNet->commit();
	my $router1routeRange = ($ixNet->getList($router1, 'routeRange'))[$index];
	if ($count < 6) {
		$ixNet->setAttribute($router1routeRange, '-enabled', 'true');
		$ixNet->setAttribute($router1routeRange, '-origin', 'externalType1');
	}
	# End if
	$ixNet->setAttribute($router1routeRange, '-networkNumber', '55.55.55.'. $count);
	$ixNet->commit();
	$ixNet->add($router2, 'routeRange');
	$ixNet->commit();
	my $router2routeRange = ($ixNet->getList($router2, 'routeRange'))[$index];
	if($count < 6) {
		$ixNet->setAttribute($router2routeRange, '-enabled', 'true');
		$ixNet->setAttribute($router2routeRange, '-origin', 'externalType1');
	}
	# End if
	$ixNet->setAttribute($router2routeRange, '-networkNumber', '66.66.66.'. $count);
	$ixNet->commit();
}
#End for
################################################################################
# 2. Start OSPFv2 protocol and wait for 60 seconds
################################################################################
print("Start OSPFv2 protocol and wait for 60 seconds for protocol to come up");
$ixNet->execute('startAllProtocols');
sleep(20);

################################################################################
# 3. Retrieve protocol statistics.
################################################################################
print ("Fetching all OSPF Aggregated Stats\n");
my $viewPage  = '::ixNet::OBJ-/statistics/view:"OSPF Aggregated Statistics"/page';
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
sleep(5);
###############################################################################
# 4. Retrieve protocol learned info
###############################################################################
print("Retrieve protocol learned info. \n");
$ixNet->execute('refreshLearnedInfo', $router1Interface);
$ixNet->execute('refreshLearnedInfo', $router2Interface);
my $waitPeriod = 0;
my $isRefreshedInterface1 = $ixNet->getAttribute($router1Interface, '-isLearnedInfoRefreshed');
my $isRefreshedInterface2 = $ixNet->getAttribute($router2Interface, '-isLearnedInfoRefreshed');
while ($isRefreshedInterface1 ne "true" && $isRefreshedInterface2 ne "true") {
	$isRefreshedInterface1 = $ixNet->getAttribute($router1Interface, '-isLearnedInfoRefreshed');
	$isRefreshedInterface2 = $ixNet->getAttribute($router2Interface, '-isLearnedInfoRefreshed');
	sleep(1);
	$waitPeriod += 1;
	if ($waitPeriod > 60){
		print("Could not retrieve learnt info on ports after 60 secs\n");
	}
	#End if
}
#End While
my @listLSA1 = $ixNet->getList($router1Interface, 'learnedLsa');
my @listLSA2 = $ixNet->getList($router2Interface, 'learnedLsa');
my $temp = 1;
my $item = "";
print("\nLSA retrieved on port 1\n");
foreach $item (@listLSA1) {
	print("\nLSA : $temp");
	print("\n***************************************************");

	my $linkStateID = $ixNet->getAttribute($item, '-linkStateId');
	my $advRouterID = $ixNet->getAttribute($item, '-advRouterId');
	my $lsaType = $ixNet->getAttribute($item, '-lsaType');
	my $seqNumber = $ixNet->getAttribute($item, '-seqNumber');
	my $age = $ixNet->getAttribute($item, '-age');

	print("\n linkStateID \t:\t $linkStateID ");
	print("\n advRouterID \t:\t $advRouterID ");
	print("\n lsaType     \t:\t $lsaType ");
	print("\n seqNumber   \t:\t $seqNumber");
	print("\n age         \t:\t $age");
	print("\n");
	$temp += 1;
}
#End For
$temp = 1;
$item = "";
print("\nLSA retrieved on port 2\n");
foreach $item (@listLSA2) {
	print("\nLSA : $temp \n");
	print("*************************************************** \n");

	my $linkStateID = $ixNet->getAttribute($item, '-linkStateId');
	my $advRouterID = $ixNet->getAttribute($item, '-advRouterId');
	my $lsaType = $ixNet->getAttribute($item, '-lsaType');
	my $seqNumber = $ixNet->getAttribute($item, '-seqNumber');
	my $age = $ixNet->getAttribute($item, '-age');

	print("\n linkStateID \t:\t $linkStateID ");
	print("\n advRouterID \t:\t $advRouterID ");
	print("\n lsaType     \t:\t $lsaType ");
	print("\n seqNumber   \t:\t $seqNumber");
	print("\n age         \t:\t $age");
	print("\n");
	$temp += 1;
}
#End For

print ("***************************************************\n");
sleep(20);
################################################################################
# 5. Enable all route ranges on each OSPFv2 router
################################################################################
print ("Enable all available route ranges on each OSPFv2 router\n");
my @router1routeRangeList = $ixNet->getList($router1, 'routeRange');
my @router2routeRangeList = $ixNet->getList($router2, 'routeRange');
my $routeRange = "";
foreach $routeRange (@router1routeRangeList) {
   $ixNet->setAttribute($routeRange, '-enabled', 'true');
   $ixNet->commit();
}   
#End For
$routeRange = "";
foreach $routeRange (@router2routeRangeList) {
   $ixNet->setAttribute($routeRange, '-enabled', 'true');
   $ixNet->commit();
}   
#End For

##################################################################################
# 6. Disable / Enable interfaces on each OSPFv2 router for new routes to be available
##################################################################################
my @router1InterfaceList = $ixNet->getList($router1, 'interface');
my @router2InterfaceList = $ixNet->getList($router2, 'interface');
my $interface = "";
foreach $interface (@router1InterfaceList) {
   $ixNet->setAttribute($interface, '-enabled', 'false');
   $ixNet->commit();
   $ixNet->setAttribute($interface, '-enabled', 'true');
   $ixNet->commit();
}
#End For
$interface = "";
foreach $interface (@router2InterfaceList) {
   $ixNet->setAttribute($interface, '-enabled', 'false');
   $ixNet->commit();
   $ixNet->setAttribute($interface, '-enabled', 'true');
   $ixNet->commit();
}
#End For

#################################################################################
# 7. Retrieve protocol learned info , wait till 60 sec for table to be refreshed
#################################################################################
sleep(10);
print("Retrieve protocol learned info after the changes. \n");
$ixNet->execute('refreshLearnedInfo', $router1Interface);
$ixNet->execute('refreshLearnedInfo', $router2Interface);
#sleep(10);
my $waitPeriod = 0;
my $isRefreshedInterface1 = $ixNet->getAttribute($router1Interface, '-isLearnedInfoRefreshed');
my $isRefreshedInterface2 = $ixNet->getAttribute($router2Interface, '-isLearnedInfoRefreshed');
while ($isRefreshedInterface1 ne "true" && $isRefreshedInterface2 ne "true") {
	$isRefreshedInterface1 = $ixNet->getAttribute($router1Interface, '-isLearnedInfoRefreshed');
	$isRefreshedInterface2 = $ixNet->getAttribute($router2Interface, '-isLearnedInfoRefreshed');
	sleep(1);
	$waitPeriod += 1;
	if ($waitPeriod > 60){
		print("Could not retrieve learnt info on ports after 60 secs\n");
	}
	#End if
}
#End While
my @listLSA1_1 = $ixNet->getList($router1Interface, 'learnedLsa');
my @listLSA2_1 = $ixNet->getList($router2Interface, 'learnedLsa');
my $temp = 1;
my $item = '';

print("\nLSA retrieved on port 1\n");
foreach $item (@listLSA1_1) {
	print("\nLSA : $temp");
	print("\n***************************************************");
	
	my $linkStateID = $ixNet->getAttribute($item, '-linkStateId');
	my $advRouterID = $ixNet->getAttribute($item, '-advRouterId');
	my $lsaType = $ixNet->getAttribute($item, '-lsaType');
	my $seqNumber = $ixNet->getAttribute($item, '-seqNumber');
	my $age = $ixNet->getAttribute($item, '-age');

	print("\n linkStateID \t:\t $linkStateID ");
	print("\n advRouterID \t:\t $advRouterID ");
	print("\n lsaType     \t:\t $lsaType ");
	print ("\n seqNumber   \t:\t $seqNumber");
	print ("\n age         \t:\t $age");
	print ("\n");
	$temp += 1;
}
#End For
$temp = 1;
$item = '';
print ("\nLSA retrieved on port 2\n");
foreach $item (@listLSA2_1) {
	print("\nLSA : $temp");
	print("\n***************************************************");

	my $linkStateID = $ixNet->getAttribute($item, '-linkStateId');
	my $advRouterID = $ixNet->getAttribute($item, '-advRouterId');
	my $lsaType = $ixNet->getAttribute($item, '-lsaType');
	my $seqNumber = $ixNet->getAttribute($item, '-seqNumber');
	my $age = $ixNet->getAttribute($item, '-age');

	print("\n linkStateID \t:\t $linkStateID ");
	print("\n advRouterID \t:\t $advRouterID ");
	print("\n lsaType     \t:\t $lsaType ");
	print("\n seqNumber   \t:\t $seqNumber");
	print("\n age         \t:\t $age");
	print("\n");
	$temp += 1;
}

################################################################################
# 8. Configure L2-L3 traffic
################################################################################
print ("Congfiguring L2-L3 Traffic Item\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'Traffic Item OSPF',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ipv4');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my $source       = ($vPort1 . '/protocols/ospf');
my $destination  = ($vPort2 . '/protocols/ospf');
print ("source : $source");
print ("destination : $destination");
$ixNet->setMultiAttribute($endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', (''),
    '-scalableSources',       (''),
    '-multicastReceivers',    (''),
    '-scalableDestinations',  (''),
    '-ngpfFilters',           (''),
    '-trafficGroups',         (''),
    '-sources',               $source ,
    '-destinations',          $destination);
$ixNet->commit();

$ixNet->setMultiAttribute($trafficItem1.'/tracking',
    '-trackBy',        ['sourceDestEndpointPair0','trackingenabled0']);
$ixNet->commit();

###############################################################################
# 9. Apply and start L2/L3 traffic
###############################################################################
print("applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

print ('Let traffic run for 1 minute\n');
time.sleep(60);

###############################################################################
# 10. Retrieve L2/L3 traffic item statistics
###############################################################################
print("***************************************************\n");
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

################################################################################
# 11. Stop L2/L3 traffic
################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# 12. Stop all protocols
#############################################################################
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!");

