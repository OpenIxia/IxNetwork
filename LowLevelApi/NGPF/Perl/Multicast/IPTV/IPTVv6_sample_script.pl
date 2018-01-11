################################################################################
# Version 1.0    $Revision: #1 $                                               #
#                                                                              #
#    Copyright  1997 - 2014 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    12/10/2014 - Sumeer Kumar - created sample                                #
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
#    This script intends to demonstrate how to use NGPF IPTVv6  API            #
#    It will create IPTV in MLD Host topology, it will start the emulation and #
#    than it will retrieve and display few statistics                          #
# Ixia Softwares:                                                              #
#    IxOS      6.80 EA (6.80.1100.4)                                           #
#    IxNetwork 7.40 EA (7.40.929.8)                                            #
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
my $ixTclPort   = '8921';
my @ports       = (('10.205.28.101', '3', '3'), ('10.205.28.101', '3', '4'));
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

print("Add ipv6\n");
$ixNet->add($mac1, 'ipv6');
$ixNet->add($mac2, 'ipv6');
$ixNet->commit();

my $ip1 = ($ixNet->getList($mac1, 'ipv6'))[0];
my $ip2 = ($ixNet->getList($mac2, 'ipv6'))[0];

my $mvAdd1 = $ixNet->getAttribute($ip1, '-address');
my $mvAdd2 = $ixNet->getAttribute($ip2, '-address');
my $mvGw1  = $ixNet->getAttribute($ip1, '-gatewayIp');
my $mvGw2  = $ixNet->getAttribute($ip2, '-gatewayIp');

print("Configuring ipv6 addresses");
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '20::2');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '20::1');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '20::1');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', "20::2");

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '64');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '64');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

################################################################################
# adding MLD Host over ipv6 stack
################################################################################ 
print("Adding MLD Host over IPv6 stack\n");
$ixNet->add($ip1, 'mldHost');
$ixNet->commit();

my $mldHost = ($ixNet->getList($ip1, 'mldHost'))[0];

print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'MLD Topology 1');
$ixNet->setAttribute($topo2, '-name', 'IPv6 Topology 2');
$ixNet->commit();

################################################################################
# Enabling IPTV in MLD host 
################################################################################
print("Enabling IPTV\n");
my $enableIptv = $ixNet->getAttribute($mldHost, '-enableIptv');
my $singleValue = ($ixNet->getList($enableIptv, 'singleValue'))[0];
$ixNet->setAttribute($singleValue, '-value', 'true');
$ixNet->commit();

################################################################################
# Changing STB Leave Join Delay in IPTV tab of MLD host
################################################################################
print("Changing STB Leave Join Delay\n");
my $iptv = ($ixNet->getList($mldHost, 'iptv'))[0];
my $stbLeaveJoinDelay = $ixNet->getAttribute($iptv, '-stbLeaveJoinDelay');
$singleValue = ($ixNet->getList($stbLeaveJoinDelay, 'singleValue'))[0];
$ixNet->setAttribute($singleValue, '-value', '3000');
$ixNet->commit();

################################################################################
# Changing join latency threshold in IPTV tab of MLD host
################################################################################
print("Changing join latency threshold\n");
my $joinLatencyThreshold = $ixNet->getAttribute($iptv, '-joinLatencyThreshold');
$singleValue = ($ixNet->getList($joinLatencyThreshold, 'singleValue'))[0];
$ixNet->setAttribute($singleValue, '-value', '10000');
$ixNet->commit();

################################################################################
# Changing leave latency threshold in IPTV tab of MLD host
################################################################################
print("Changing leave latency threshold\n");
my $leaveLatencyThreshold = $ixNet->getAttribute($iptv, '-leaveLatencyThreshold');
$singleValue = ($ixNet->getList($leaveLatencyThreshold, 'singleValue'))[0];
$ixNet->setAttribute($singleValue, '-value', '10000');
$ixNet->commit();

################################################################################
# Changing zap behavior in IPTV tab of MLD host
################################################################################
print("Changing zap behavior\n");
my $zapBehavior = $ixNet->getAttribute($iptv, '-zapBehavior');
$singleValue = ($ixNet->getList($zapBehavior, 'singleValue'))[0];
$ixNet->setAttribute($singleValue, '-value', 'zapandview');
$ixNet->commit();

################################################################################
# Start OSPFv2 protocol and wait for 60 seconds
################################################################################
print("Starting protocols and waiting for 20 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(20);

################################################################################
# Retrieve protocol statistics.
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
    '-scalableSources',       [],
    '-multicastReceivers',    [[$topo1.'/deviceGroup:1/ethernet:1/ipv6:1/mldHost:1/mldMcastIPv6GroupList', '0', '0', '0']],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               @source,
    '-destinations',          @destination);
$ixNet->commit();

$ixNet->setMultiAttribute($trafficItem1.'/tracking',
    '-trackBy',        ['ipv6DestIp0','trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         []);
$ixNet->commit();

###############################################################################
# 9. Apply and start L2/L3 traffic
###############################################################################
print("Applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("Starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

###############################################################################
# Starting IPTV
###############################################################################
print("Starting IPTV\n");
$ixNet->execute('startIptv', $iptv);
sleep(5);

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

################################################################################
# Making on the fly changes for zapDirection, zapIntervalType, zapInterval,
# numChannelChangesBeforeView and viewDuration in IPTV tab of MLD host
################################################################################
print("Making on the fly chnages for zapDirection, zapIntervalType,\
zapInterval,numChannelChangesBeforeView and viewDuration\n");
my $zapDirection = $ixNet->getAttribute($iptv, '-zapDirection');
$singleValue = ($ixNet->getList($zapDirection, 'singleValue'))[0];
$ixNet->setAttribute($singleValue, '-value', 'down');

my $zapIntervalType = $ixNet->getAttribute($iptv, '-zapIntervalType');
$singleValue = ($ixNet->getList($zapIntervalType, 'singleValue'))[0];
$ixNet->setAttribute($singleValue, '-value', 'multicasttoleave');

my $zapInterval = $ixNet->getAttribute($iptv, '-zapInterval');
$singleValue = ($ixNet->getList($zapInterval, 'singleValue'))[0];
$ixNet->setAttribute($singleValue, '-value', '10000');

my $numChannelChangesBeforeView = $ixNet->getAttribute($iptv, '-numChannelChangesBeforeView');
$singleValue = ($ixNet->getList($numChannelChangesBeforeView, 'singleValue'))[0];
$ixNet->setAttribute($singleValue, '-value', '1');

my $viewDuration =  $ixNet->getAttribute($iptv, '-viewDuration');
$singleValue = ($ixNet->getList($viewDuration, 'singleValue'))[0];
$ixNet->setAttribute($singleValue, '-value', '10000');
$ixNet->commit();


################################################################################
# Applying changes one the fly
################################################################################
print("Applying changes on the fly\n");
my $root = $ixNet->getRoot();
my $globals = $root.'/globals';
my $topology = $globals.'/topology';
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);

###############################################################################
# Stopping IPTV
###############################################################################
print("Stopping IPTV\n");
$ixNet->execute('stopIptv', $iptv);
sleep(5);

################################################################################
# Stop L2/L3 traffic
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', $ixNet->getRoot().'/traffic');
sleep(5);

################################################################################
# Stop protocol 
################################################################################
print("Stopping protocol\n");
$ixNet->execute('stopAllProtocols');

print("!!! Test Script Ends !!!");