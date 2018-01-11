################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    11/01/2012 - Chandan Mishra - created sample                              #
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
#    This script intends to demonstrate how to use NGPF MLD API.               #
#                                                                              #
#    1. It will create 2 MLD topologies, each having an ipv6 network           #
#       topology                                                               #
#    2. Add MLD over ipv6 stack.                                               #
#    3. Change MLD parameters like general query interval and general query    #
#       response interval                                                      #
#    4. Change protocol version of MLD host and querier.                       #
#    5. Start MLD protocol.                                                    #
#    6. Configure L2-L3 traffic.                                               #
#    7. Start L2/L3 protocol.                                                  #
#    8. Retreive protocol statistics                                           #                                                                         #
#    9. Retreive  L2/L3 protocol statistics.                                   #
#   10. Change mldstart group address and applyOnTheFly                        #                                                #
#   11. Stop protocol and L2/L3 traffic.                                       #
#   12. Configure few parameters of MLD host and querier which can be changed  #
#       when protocol is not started.                                          #
#   13. Start protocol.                                                        #
#   14. Retreive protocol statistics                                           #
#   15. Stop all protocols.                                                    #                
# Ixia Softwares:                                                              #
#    IxOS      6.80 EB (6.80.1100.7)                                          #
#    IxNetwork 7.40 EB (7.40.929.15)                                            #
#                                                                              #
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
my $ixTclServer = '10.205.25.83';
my $ixTclPort   = '8009';
my @ports       = (('10.205.28.81', '3', '5'), ('10.205.28.81', '3', '6'));
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
$ixNet->setAttribute($t1dev1, '-multiplier', '2');
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

print("Add ipv6 \n");
$ixNet->add($mac1, 'ipv6');
$ixNet->add($mac2, 'ipv6');
$ixNet->commit();

my $ip1 = ($ixNet->getList($mac1, 'ipv6'))[0];
my $ip2 = ($ixNet->getList($mac2, 'ipv6'))[0];

my $mvAdd1 = $ixNet->getAttribute($ip1, '-address');
my $mvAdd2 = $ixNet->getAttribute($ip2, '-address');
my $mvGw1  = $ixNet->getAttribute($ip1, '-gatewayIp');
my $mvGw2  = $ixNet->getAttribute($ip2, '-gatewayIp');

print("configuring ipv6 addresses \n");
$ixNet->setMultiAttribute($ixNet->add($mvAdd1, 'counter'),
         '-step', '0:0:0:0:0:0:0:1',
		 '-start', '2001:0:0:1:0:0:0:2',
	     '-direction', 'increment');
$ixNet->commit();
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '2001:0:0:1:0:0:0:1');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '2001:0:0:1:0:0:0:1');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', "2001:0:0:1:0:0:0:2");

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '64');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '64');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

################################################################################
# adding MLD over ipv6 stack
################################################################################ 
print("Adding MLD over ipv6 stack \n");
$ixNet->add($ip1, 'mldHost');
$ixNet->add($ip2, 'mldQuerier');
$ixNet->commit();
my $mldHost = ($ixNet->getList($ip1, 'mldHost'))[0];
my $mldQuerier = ($ixNet->getList($ip2, 'mldQuerier'))[0];
print("Renaming the topologies and the device groups \n");
$ixNet->setAttribute($topo1, '-name', 'mldHost Topology 1');
$ixNet->setAttribute($topo2, '-name', 'mldQuerier Topology 2');
$ixNet->commit();

################################################################################
# change genaral query interval
################################################################################
print("Changing genaral query interval \n");
my $gqueryi = $ixNet->getAttribute($mldQuerier, '-generalQueryInterval');
$ixNet->setMultiAttribute ($gqueryi,
      '-clearOverlays', 'false',
	  '-pattern', 'counter');
$ixNet->commit();
$ixNet->setMultiAttribute($ixNet->add($gqueryi, 'counter'),
     '-step', '1', 
	 '-start', '140',
	 '-direction', 'increment');                   
$ixNet->commit();

################################################################################
# change general query response interval
################################################################################
print("Changing general query response interval \n");
my $gqueryrespvi = $ixNet->getAttribute($mldQuerier, '-generalQueryResponseInterval');
$ixNet->setMultiAttribute ($gqueryrespvi,
         '-clearOverlays', 'false',
	     '-pattern', 'counter');
$ixNet->commit();
$ixNet->setMultiAttribute($ixNet->add($gqueryrespvi, 'counter'),
        '-step', '1',
	'-start', '11000',
	'-direction', 'increment');
$ixNet->commit();

################################################################################
# change version of MLD HOST
################################################################################
print("Changing version of MLD HOST to v2 \n");
my $mldport1 = ($ixNet->getList($mldHost, 'port'))[0];
my $vesriontypehost = $ixNet->getAttribute($mldport1, '-versionType');
my $versionvaluehost = ($ixNet->getList($vesriontypehost, 'singleValue'))[0];
$ixNet->setAttribute($versionvaluehost, '-value', 'version2');                               
$ixNet->commit();

################################################################################
# change version of MLD querier
################################################################################
print("Changing version of MLD querier to v2 \n");
my $mldport2 =($ixNet->getList($mldQuerier, 'port'))[0];
my $vesriontypequerier = $ixNet->getAttribute($mldport2, '-versionType');
my $versionvaluequerier = ($ixNet->getList($vesriontypequerier, 'singleValue'))[0];
$ixNet->setAttribute($versionvaluequerier, '-value', 'version2');
$ixNet->commit();

################################################################################
# Discard learned info
################################################################################
print("Disabling disacrd learned info \n");
my $discardLearntInfo1 = $ixNet->getAttribute($mldQuerier, '-discardLearntInfo');
$ixNet->setMultiAttribute ($discardLearntInfo1,
	'-clearOverlays', 'false',
	'-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($ixNet->add($discardLearntInfo1, 'singleValue'),
	'-value', 'false');
$ixNet->commit();

################################################################################
# 2. Start protocol and wait for 30 seconds
################################################################################
print("Starting protocols and waiting for 30 seconds for protocols to come up\n");
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

################################################################################
# change state of MLD Groupranges(only when the protocol is started)
################################################################################
my $ipv6grouplist1 = ($ixNet->getList($mldHost, 'mldMcastIPv6GroupList'))[0];
print("Change state of MLD Groupranges to leave \n");
$ixNet->execute('mldLeaveGroup', $ipv6grouplist1);

###############################################################################
# print learned info
###############################################################################
print ("Getting learnedInfo \n");
$ixNet->execute('mldGetLearnedInfo', $mldQuerier);
sleep(5);
my $learnedInfo = ($ixNet->getList($mldQuerier, 'learnedInfo'))[0];
sleep(10);
my $table = ($ixNet->getList($learnedInfo, 'table'))[0];
my @values = $ixNet->getAttribute($table, '-values');
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
# 7. Configure L2-L3 traffic 
################################################################################
print ("Congfiguring L2-L3 Traffic Item\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ipv6');
$ixNet->commit();
$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source       = ($topo2.'/deviceGroup:1/ethernet:1/ipv6:1');
my @destination  = ($topo1.'/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList');

$ixNet->setMultiAttribute($endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', [['false', 'none', 'ff03:0:0:0:0:0:0:1', '0::0', '1']],
    '-scalableSources',       [''],
    '-multicastReceivers',    [[$topo1.'/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList', '0', '0', '0'], [$topo1.'/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList', '0', '1', '0']],
    '-scalableDestinations',  [''],
    '-ngpfFilters',           [''],
    '-trafficGroups',         [''],
    '-sources',               @source,
    '-destinations',          @destination);
$ixNet->commit();
$ixNet->setMultiAttribute($trafficItem1.'/tracking',
    '-trackBy',        ['trackingenabled0','ipv6DestIp0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         ['']);
$ixNet->commit();

###############################################################################
# 9. Apply and start L2/L3 traffic
###############################################################################
print("applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);
print("starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');
print("***************************************************\n");

###############################################################################
# 12. Retrieve L2/L3 traffic item statistics
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

################################################################################
#  change mldstart group address and applyOnTheFly
################################################################################
print("Changing mldstart group address and applyOnTheFly changes\n");
my $mcastaddr1 = $ixNet->getAttribute($ipv6grouplist1, '-startMcastAddr');
print("Changing MLD start group address \n");
$ixNet->setAttribute($mcastaddr1, '-clearOverlays', 'false');
$ixNet->setAttribute($mcastaddr1, '-pattern', 'counter');
$ixNet->commit();
print ("Configuring the mldstart group address \n");
$ixNet->setMultiAttribute($ixNet->add($mcastaddr1, 'counter'),
        '-step', '0:0:0:0:0:0:0:1',
        '-start', 'ff04:0:0:0:0:0:0:1',
        '-direction', 'increment');
$ixNet->commit();
my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);

#################################################################################
# 14. Stop L2/L3 traffic
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# 15. Stop all protocols
################################################################################
$ixNet->execute('stopAllProtocols');
print("!!! *********** !!! \n");
sleep(10);

################################################################################
# changing sourcemode
################################################################################
print("Changing sourcemode \n");
my $sourcemode = ($ixNet->getAttribute($ipv6grouplist1, '-sourceMode'));
$ixNet->setMultiAttribute($ixNet->add($sourcemode, 'singleValue'),
	'-value', 'exclude');
$ixNet->commit();

################################################################################
# change number of source address count
#(to be changed only when the protocol is not started)
################################################################################
print("Changing number of source address count \n");
my $ipv6grouplist1 = ($ixNet->getList($ipv6grouplist1, 'mldUcastIPv6SourceList'))[0];
my $ucastSrcAddrCnt = $ixNet->getAttribute($ipv6grouplist1, '-ucastSrcAddrCnt');
my $singleValue = ($ixNet->getList($ucastSrcAddrCnt, 'singleValue'))[0];
$ixNet->setAttribute($singleValue,
        '-value', '2');
$ixNet->commit();

################################################################################
# change general query responsemode
################################################################################
print ("Changing general query responsemode \n");
my $gQResponseMode = $ixNet->getAttribute($mldHost, '-gQResponseMode');
$ixNet->setMultiAttribute($gQResponseMode,
	'-clearOverlays', 'false',
	'-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($ixNet->add($gQResponseMode, 'singleValue'),
	'-value', 'false');
$ixNet->commit();

################################################################################
# change group specific query responsemode
################################################################################
print("Disabling group specific query responsemode \n");
my $gSResponseMode = $ixNet->getAttribute($mldHost, '-gSResponseMode');
$ixNet->setMultiAttribute($gSResponseMode,
	'-clearOverlays', 'false',
	'-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($ixNet->add($gSResponseMode, 'singleValue'),
        '-value', 'false');
$ixNet->commit();

################################################################################
# change immediate responsemode
################################################################################
print ("Disabling immediate responsemode \n");
my $imResponse = ($ixNet->getAttribute($mldHost, '-imResponse'));
$ixNet->setMultiAttribute($imResponse,
	'-clearOverlays', 'false',
	'-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($ixNet->add($imResponse, 'singleValue'),
        '-value', 'true');
$ixNet->commit();

################################################################################
# configure jlMultiplier value
################################################################################
print ("Configuring jlMultiplier value \n");
$ixNet->setAttribute($mldHost, '-jlMultiplier', '2');
$ixNet->commit();

################################################################################
# change router alert value
################################################################################
print("Changing router alert value \n");
my $routerAlert = ($ixNet->getAttribute($mldHost, '-routerAlert'));
$ixNet->setMultiAttribute($routerAlert,
	'-clearOverlays', 'false',
	'-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($ixNet->add($routerAlert, 'singleValue'),
        '-value', 'false');
$ixNet->commit();

################################################################################
# change value of number of group ranges
################################################################################
print("Change value of number of group ranges \n");
$ixNet->setAttribute($mldHost, '-noOfGrpRanges', '2');
$ixNet->commit();

################################################################################
# Change unsolicit response mode
################################################################################
print("Change unsolicit response mode to true \n");
my $uSResponseMode =($ixNet->getAttribute($mldHost, '-uSResponseMode'));
$ixNet->setMultiAttribute($uSResponseMode,
	'-clearOverlays', 'false',
	'-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($ixNet->add($uSResponseMode, 'singleValue'),
	'-value', 'true');
$ixNet->commit();

################################################################################
# enable proxy reporting
################################################################################
print("Enable proxy reporting \n");
my $enableProxyReporting =($ixNet->getAttribute($mldHost, '-enableProxyReporting'));
$ixNet->setMultiAttribute($enableProxyReporting,
	'-clearOverlays', 'false',
	'-pattern', 'singleValue');
$ixNet->commit();
$ixNet->setMultiAttribute($ixNet->add($enableProxyReporting, 'singleValue'),
        '-value', 'true');
$ixNet->commit();

################################################################################
# change number of source ranges
#(to be changed only when the protocol is not started)
################################################################################
print ("Changing number of source ranges\n");
$ixNet->setAttribute($ipv6grouplist1, 'noOfSrcRanges', '2');
$ixNet->commit();

################################################################################
# 2. Start protocol and wait for 30 seconds
################################################################################
print("Starting protocols and waiting for 30 seconds for protocols to come up\n");
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

################################################################################
# 15. Stop all protocols
################################################################################
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!");

