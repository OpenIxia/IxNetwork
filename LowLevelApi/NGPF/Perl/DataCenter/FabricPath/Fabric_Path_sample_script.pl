################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    04/10/2015 - Sayantan Pramanick - created sample                          #
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
#    This script intends to demonstrate how to use NGPF Fabric Path APIs       #
#                                                                              #
#    1. It will create one Fabric Path RBridge per topology in two ports.      #
#       Behind RBridge it will add FAT Tree network topology. Behind network   #
#       topology it will add Fabric Path simulated edge RBRidge. Behind        #
#       simulated                                                              #
#       edge, it will add MAC pool which will serve as endpoints in traffic.   #
#    2. Start all protocols.                                                   #
#    3. Retrieve protocol statistics.                                          #
#    4. Retrieve protocol learned info.                                        #
#    5. Chnage some fields and apply change on the fly                         #
#    6. Configure L2-L3 traffic.                                               #
#    7. Start the L2-L3 traffic.                                               #
#    8. Retrieve L2-L3 traffic stats.                                          #
#    9. Stop L2-L3 traffic.                                                    #
#   10. Stop all protocols.                                                    #
#                                                                              #
# Ixia Softwares:                                                              #
#    IxOS      6.90 EB (6.90.0.240)                                            #
#    IxNetwork 7.50 EB (7.50.0.160)                                            #
#                                                                              #
################################################################################

################################################################################
#    Please ensure that PERL5LIB environment variable is set properly so that  #
#    IxNetwork.pm module is available. IxNetwork.pm is generally available in  #
#    C:\<IxNetwork Install Path>\API\Perl                                      #
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
my $ixTclServer = '10.205.25.88';
my $ixTclPort   = '8009';
my @ports       = (('10.205.27.69', '1', '1'), ('10.205.27.69', '1', '2'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '7.40',
    '-setAttribute', 'strict');

print("Creating a new config\n");
$ixNet->execute('newConfig');

print("Adding 2 vports\n");
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->commit();

my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vport1 = $vPorts[0];
my $vport2 = $vPorts[1];
assignPorts($ixNet, @ports, $vport1, $vport2);
sleep(5);

my $root = $ixNet->getRoot();

print("Adding 2 topologies\n");
$ixNet->add($root, 'topology', '-vports', $vport1);
$ixNet->add($root, 'topology', '-vports', $vport2);
$ixNet->commit();

my @topologies = $ixNet->getList($root, 'topology');
my $topo1 = $topologies[0];
my $topo2 = $topologies[1];

print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'Topology 1 for Fabric Path');
$ixNet->setAttribute($topo2, '-name', 'Topology 2 for Fabric Path');

print("Adding 2 device groups\n");
$ixNet->add($topo1, 'deviceGroup');
$ixNet->add($topo2, 'deviceGroup');
$ixNet->commit();

my @t1devices = $ixNet->getList($topo1, 'deviceGroup');
my @t2devices = $ixNet->getList($topo2, 'deviceGroup');

my $t1dev1 = $t1devices[0];
my $t2dev1 = $t2devices[0];

print("Configuring the multipliers (number of sessions)\n");
$ixNet->setAttribute($t1dev1, '-multiplier', 1);
$ixNet->setAttribute($t2dev1, '-multiplier', 1);
$ixNet->commit();

print("Adding ethernet/mac endpoints\n");
$ixNet->add($t1dev1, 'ethernet');
$ixNet->add($t2dev1, 'ethernet');
$ixNet->commit();

my $mac1 = ($ixNet->getList($t1dev1, 'ethernet'))[0];
my $mac2 = ($ixNet->getList($t2dev1, 'ethernet'))[0];

print("Configuring the mac addresses\n");
$ixNet->setMultiAttribute($ixNet->getAttribute($mac1, '-mac').'/counter',
    '-direction',  'increment',
    '-start', '18:03:73:C7:6C:B1',
    '-step', '00:00:00:00:00:01');

$ixNet->setAttribute($ixNet->getAttribute($mac2, '-mac').'/singleValue',
    '-value', '18:03:73:C7:6C:01');
$ixNet->commit();

print("Adding Fabric Path interfaces\n");
$ixNet->add($mac1, 'isisFabricPath');
$ixNet->add($mac2, 'isisFabricPath');
$ixNet->commit();

my $fabricPathIf1 = ($ixNet->getList($mac1, 'isisFabricPath'))[0];
my $fabricPathIf2 = ($ixNet->getList($mac2, 'isisFabricPath'))[0];

print("Setting discard LSP off in Fabric Path Routers\n");
my $fabricPathRouter1 = ($ixNet->getList($t1dev1, 'isisFabricPathRouter'))[0];
my $fabricPathRouter2 = ($ixNet->getList($t2dev1, 'isisFabricPathRouter'))[0];
my $mv1 = $ixNet->getAttribute($fabricPathRouter1, '-discardLSPs');
my $mv2 = $ixNet->getAttribute($fabricPathRouter2, '-discardLSPs');
$ixNet->setAttribute($mv1, '-pattern', 'singleValue');
$ixNet->setAttribute($mv2, '-pattern', 'singleValue');
$ixNet->commit();

$ixNet->setAttribute($mv1.'/singleValue', '-value', 'false');
$ixNet->setAttribute($mv2.'/singleValue', '-value', 'false');
$ixNet->commit();

print("Setting Mulitcast IPv4 group in Fabric Path Router 2\n");
$ixNet->setAttribute($fabricPathRouter2, '-dceMCastIpv4GroupCount', 1);
$ixNet->commit();

my $dceMcastIpv4GroupList = ($ixNet->getList($fabricPathRouter2, 'dceMCastIpv4GroupList'))[0];
my $mvMcastAddrCount = $ixNet->getAttribute($dceMcastIpv4GroupList, '-mcastAddrCnt');
my $mvStartMcastAddr = $ixNet->getAttribute($dceMcastIpv4GroupList, '-startMcastAddr');

$ixNet->setAttribute($mvMcastAddrCount, '-pattern', 'singleValue');
$ixNet->setAttribute($mvMcastAddrCount.'/singleValue', '-value', 2);
$ixNet->setAttribute($mvStartMcastAddr, '-pattern', 'singleValue');
$ixNet->setAttribute($mvStartMcastAddr.'/singleValue', '-value', '230.0.0.1');
$ixNet->commit();

print("Setting Multicast MAC Groups in Fabric Path Router 2\n");
$ixNet->setAttribute($fabricPathRouter2, '-dceMCastMacGroupCount', 1);
$ixNet->commit();

my $dceMCastMacGroupList = ($ixNet->getList($fabricPathRouter2, 'dceMCastMacGroupList'))[0];

my $mvMcastAddrCount = $ixNet->getAttribute($dceMCastMacGroupList, '-mcastAddrCnt');
my $mvStartMcastAddr = $ixNet->getAttribute($dceMCastMacGroupList, '-startMcastAddr');

$ixNet->setAttribute($mvMcastAddrCount, '-pattern', 'singleValue');
$ixNet->setAttribute($mvMcastAddrCount.'/singleValue', '-value', 2);
$ixNet->setAttribute($mvStartMcastAddr, '-pattern', 'singleValue');
$ixNet->setAttribute($mvStartMcastAddr.'/singleValue', '-value', '01:55:55:55:55:55');
$ixNet->commit();

print("Setting Mulitcast IPv6 group in Fabric Path Router 2\n");
$ixNet->setAttribute($fabricPathRouter2, '-dceMCastIpv6GroupCount', 1);
$ixNet->commit();

my $dceMcastIpv6GroupList = ($ixNet->getList($fabricPathRouter2, 'dceMCastIpv6GroupList'))[0];
my $mvMcastAddrCount = $ixNet->getAttribute($dceMcastIpv6GroupList, '-mcastAddrCnt');
my $mvStartMcastAddr = $ixNet->getAttribute($dceMcastIpv6GroupList, '-startMcastAddr');

$ixNet->setAttribute($mvMcastAddrCount, '-pattern', 'singleValue');
$ixNet->setAttribute($mvMcastAddrCount.'/singleValue', '-value', 2);
$ixNet->setAttribute($mvStartMcastAddr, '-pattern', 'singleValue');
$ixNet->setAttribute($mvStartMcastAddr.'/singleValue', '-value', 'ff03::1111');
$ixNet->commit();

print("Adding network group with FAT tree topology\n");
$ixNet->add($t1dev1, 'networkGroup');
$ixNet->add($t2dev1, 'networkGroup');
$ixNet->commit();

my $netGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
my $netGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];

$ixNet->add($netGroup1, 'networkTopology');
$ixNet->add($netGroup2, 'networkTopology');
$ixNet->commit();

my $netTopo1 = ($ixNet->getList($netGroup1, 'networkTopology'))[0];
my $netTopo2 = ($ixNet->getList($netGroup2, 'networkTopology'))[0];

$ixNet->add($netTopo1, 'netTopologyFatTree');
$ixNet->add($netTopo2, 'netTopologyFatTree');
$ixNet->commit();

print("Adding device group behind network group\n");
$ixNet->add($netGroup1, 'deviceGroup');
$ixNet->add($netGroup2, 'deviceGroup');
$ixNet->commit();

my $t1dev2 = ($ixNet->getList($netGroup1, 'deviceGroup'))[0];
my $t2dev2 = ($ixNet->getList($netGroup2, 'deviceGroup'))[0];

print("Adding ethernet\n");
$ixNet->add($t1dev2, 'ethernet');
$ixNet->add($t2dev2, 'ethernet');
$ixNet->commit();

my $mac3 = ($ixNet->getList($t1dev2, 'ethernet'))[0];
my $mac4 = ($ixNet->getList($t2dev2, 'ethernet'))[0];

print("Adding Fabric Path Simulated Egde\n");
$ixNet->add($mac3, 'isisDceSimRouter');
$ixNet->add($mac4, 'isisDceSimRouter');
$ixNet->commit();

print("Adding MAC Pools behind Fabric Path Simulated Edge Device\n");
$ixNet->add($t1dev2, 'networkGroup');
$ixNet->add($t2dev2, 'networkGroup');
$ixNet->commit();

my $netGroup3 = ($ixNet->getList($t1dev2, 'networkGroup'))[0];
my $netGroup4 = ($ixNet->getList($t2dev2, 'networkGroup'))[0];
$ixNet->add($netGroup3, 'macPools');
$ixNet->add($netGroup4, 'macPools');
$ixNet->commit();

my $macPool1 = ($ixNet->getList($netGroup3, 'macPools'))[0];
my $macPool2 = ($ixNet->getList($netGroup4, 'macPools'))[0];

my $mvMac1 = $ixNet->getAttribute($macPool1, '-mac');
my $mvMac2 = $ixNet->getAttribute($macPool2, '-mac');

$ixNet->setAttribute($mvMac1, '-pattern', 'counter');
$ixNet->setAttribute($mvMac2, '-pattern', 'counter');
$ixNet->commit();

my $mvCounter1 = ($ixNet->getList($mvMac1, 'counter'))[0];
my $mvCounter2 = ($ixNet->getList($mvMac2, 'counter'))[0];

$ixNet->setMultiAttribute($mvCounter1, '-step', '00:00:00:00:00:01', '-start', '22:22:22:22:22:22', '-direction', 'increment');
$ixNet->setMultiAttribute($mvCounter2, '-step', '00:00:00:00:00:01', '-start', '44:44:44:44:44:44', '-direction', 'increment');
$ixNet->commit();

print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);

################################################################################
# 2. Retrieve protocol statistics.
################################################################################
print("Fetching all Protocol Summary Stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"Fabric-Path RTR Per Port"/page';
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
		    printf(" %-34s:%s\n", $statcap[$index], $statIndiv);
			$index++;
        }
    }    
}
print("***************************************************\n");

###############################################################################
# 3. Retrieve protocol learned info
###############################################################################
print("Fetching Fabric Path Learned Info\n");
$ixNet->execute('getLearnedInfo', $fabricPathIf1, 1);
sleep(5);
my $linfo1 = ($ixNet->getList($fabricPathIf1, 'learnedInfo'))[0];

my @linfoTables  = $ixNet->getList($linfo1, 'table');
my $table1 = $linfoTables[0];
my $table2 = $linfoTables[1];
my $table3 = $linfoTables[2];
my $table4 = $linfoTables[3];

my @values = $ixNet->getAttribute($table1, '-values');
my @column = $ixNet->getAttribute($table1, '-columns');
print("***************************************************\n");
for (my $index = 0; $index < @values; $index++) {
    my $rowValue = $values[$index];
		for (my $col = 0; $col < @column; $col++) {
        printf("%-30s:%s\n", $column[$col], @{$rowValue}[$col]);
    }#end for
}#end for

my @values = $ixNet->getAttribute($table2, '-values');
my @column = $ixNet->getAttribute($table2, '-columns');
print("***************************************************\n");
for (my $index = 0; $index < @values; $index++) {
    my $rowValue = $values[$index];
		for (my $col = 0; $col < @column; $col++) {
        printf("%-30s:%s\n", $column[$col], @{$rowValue}[$col]);
    }#end for
}#end for

my @values = $ixNet->getAttribute($table3, '-values');
my @column = $ixNet->getAttribute($table3, '-columns');
print("***************************************************\n");
for (my $index = 0; $index < @values; $index++) {
    my $rowValue = $values[$index];
		for (my $col = 0; $col < @column; $col++) {
        printf("%-30s:%s\n", $column[$col], @{$rowValue}[$col]);
    }#end for
}#end for

my @values = $ixNet->getAttribute($table4, '-values');
my @column = $ixNet->getAttribute($table4, '-columns');
print("***************************************************\n");
for (my $index = 0; $index < @values; $index++) {
    my $rowValue = $values[$index];
		for (my $col = 0; $col < @column; $col++) {
        printf("%-30s:%s\n", $column[$col], @{$rowValue}[$col]);
    }#end for
}#end for
print("***************************************************\n");

###############################################################################
# 4. Apply on the fly
###############################################################################
my $dceMCastMacGroupList = ($ixNet->getList($fabricPathRouter2, 'dceMCastMacGroupList'))[0];
my $mvMcastAddrCount = $ixNet->getAttribute($dceMCastMacGroupList, '-mcastAddrCnt');

$ixNet->setAttribute($mvMcastAddrCount, '-pattern', 'singleValue');
$ixNet->setAttribute($mvMcastAddrCount.'/singleValue', '-value', 10);
$ixNet->commit();

my $globals = $root.'/globals';
my $topology = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(15);

################################################################################
# 5. Configure L2-L3 traffic 
################################################################################
print("Congfiguring L2-L3 Traffic Item\n");
my $trafficItem1 = $ixNet->add($root.'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, 
    '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ethernetVlan',
	'-biDirectional', 1);
$ixNet->commit();

my $trafficItem1 = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source = $netGroup3;
my @destination = $netGroup4;

$ixNet->setMultiAttribute($endpointSet1,
    '-name', 'EndpointSet-1',
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
    '-trackBy',        ['sourceDestEndpointPair0', 'trackingenabled0'],
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
		    printf(" %-34s:%s\n", $statcap[$index], $statIndiv);
			$index++;
        }
    }    
}
print("***************************************************\n");

################################################################################
# 8. Stop L2/L3 traffic
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# 9. Stop all protocols
################################################################################
print ("Stopping protocols\n");
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!");
