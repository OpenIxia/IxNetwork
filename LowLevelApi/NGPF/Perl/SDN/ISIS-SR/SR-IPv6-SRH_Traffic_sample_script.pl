################################################################################
# Version 1.0    $Revision: #1 $                                               #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    28/11/2016 - Shilpam Sinha - created sample                          #
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
##                                                                              #
## Description:                                                                 #
##    This script intends to demonstrate how to use NGPF SR-IPv6-SRH Traffic    #
##    Using Low Level Perl API                                                  #
##   1.It will create 1 IPv6 SR Ext Stack in topology1 and in topology2 will    #
##     contain only ipv6 stack.                                                 #
##	2.Configure the multipliers for IPv6 SR Ext                             #
##	3.Set values of 'Segment List Max Index[n]'                             #
##	4.Disable the checkbox 'Use This Device As Ingress' for the 2nd Tunnel  #
##     in 1st device of IPv6 SR Ext.                                            #
##	5.Set values to 'Segment Left' field for the 2nd tunnel of device 1     #
##	6.Disable the checkbox 'Enable Segment 4' for the 1st Tunnel in 1st     #
##	  device of IPv6 SR Ext                                                 #
##	7.Create IPv6 PrefixPool behind both topologies                         #
##	8.Start All protocol                                                    #
##	9.Create TrafficItem between NetworkGroup1 to NetworkGroup2             #
##  10.Apply and Start Traffic                                                  #
##  11.Print Traffic Flow Statistics                                            #
##  12.Stop Traffic                                                             #
##  13.Stop Protocols	                                                        #
##                                                                              #
## Ixia Software:                                                               #
##    IxOS      8.20 EA                                                         #
##    IxNetwork 8.20 EA                                                         #
##                                                                              #
#################################################################################

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
my $ixTclServer = '10.216.104.58';
my $ixTclPort   = '8919';
my @ports       = (('10.216.108.99', '11', '3'), ('10.216.108.99', '11', '4'));

# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '8.20',
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

print("Assigning the ports\n");
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

# Add IPv6 Stack
print("Add ipv6 over Ethernet stack\n");
$ixNet->add($mac1, 'ipv6');
$ixNet->add($mac2, 'ipv6');
$ixNet->commit();

my $ip1 = ($ixNet->getList($mac1, 'ipv6'))[0];
my $ip2 = ($ixNet->getList($mac2, 'ipv6'))[0];

my $mvAdd1 = $ixNet->getAttribute($ip1, '-address');
my $mvAdd2 = $ixNet->getAttribute($ip2, '-address');
my $mvGw1  = $ixNet->getAttribute($ip1, '-gatewayIp');
my $mvGw2  = $ixNet->getAttribute($ip2, '-gatewayIp');

print("configuring ipv6 addresses");
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '2000:0:0:1:0:0:0:1');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '2000:0:0:1:0:0:0:101');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '2000:0:0:1:0:0:0:101');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', '2000:0:0:1:0:0:0:1');

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '64');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '64');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

print("Adding IPv6 SR Ext stack over IPv6 stack for Device Group 1\n");
$ixNet->add($ip1, 'ipv6sr');
$ixNet->commit();
my $ipv6sr = ($ixNet->getList($ip1, 'ipv6sr'))[0];

print("Configuring the multipliers for IPv6 SR Ext\n");
$ixNet->setAttribute($ipv6sr, '-multiplier', '2');
$ixNet->commit();

print("Set values to Segment List Max Index[n]\n");
$ixNet->setAttribute($ipv6sr, '-numberSegments', '5');
$ixNet->commit();

print("Disabling the checkbox 'Use This Device As Ingress' for the 2nd Tunnel in 1st device of IPv6 SR Ext\n");
my $useAsIngress = $ixNet->getAttribute($ipv6sr, '-useAsIngress');
my $OverlayIngress = $ixNet->add($useAsIngress, 'overlay');
$ixNet->setAttribute($OverlayIngress, '-count', '1', 
                                      '-index', '2', 
                                      '-indexStep', '0', 
                                      '-valueStep', 'false', 
                                      '-value', 'false');
$ixNet->commit();

print("Setting values to 'Segment Left' field for the 2nd tunnel of device 1\n");
my $segmentsLeft = $ixNet->getAttribute($ipv6sr, '-segmentsLeft');
my $OverlaySL = $ixNet->add($segmentsLeft, 'overlay');
$ixNet->setAttribute($OverlaySL, '-count', '1', 
                                 '-index', '2', 
                                 '-indexStep', '0', 
                                 '-valueStep', '3', 
                                 '-value', '3');
$ixNet->commit();

print("Disabling the checkbox 'Enable Segment 4' for the 1st Tunnel in 1st device of IPv6 SR Ext\n");
my $IPv6SegmentsList4 = ($ixNet->getList($ipv6sr, 'IPv6SegmentsList'))[3];
my $sIDEnable = $ixNet->getAttribute($IPv6SegmentsList4, '-sIDEnable');
my $OverlaySID = $ixNet->add($sIDEnable, 'overlay');
$ixNet->setMultiAttribute($OverlaySID, '-count', '1', 
                                       '-index', '1', 
                                       '-indexStep', '0', 
                                       '-valueStep', 'false', 
                                       '-value', 'false');
$ixNet->commit();

$ixNet->execute('createDefaultStack', $t1dev1, 'ipv6PrefixPools');
my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
$ixNet->commit();

$ixNet->execute('createDefaultStack', $t2dev1, 'ipv6PrefixPools');
my $networkGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];
$ixNet->commit();

################################################################################
# Start ISIS protocol and wait for 60 seconds
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);

################################################################################
## Configure L2-L3 traffic 
#################################################################################

print ("Congfiguring L2-L3 IPv4 Traffic Item\n");
print("Configuring traffic item with endpoints src ::ipv6PrefixPools & dst :ipv6PrefixPools");

my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'IPv6_Traffic_Item_1',
                                         '-roundRobinPacketOrdering', 'false',
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
    '-trackBy',        ['sourceDestEndpointPair0','trackingenabled0', 'smFlowDescriptor0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();

###############################################################################
## Apply and start L2/L3 traffic
################################################################################
print("Applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

###############################################################################
## Retrieve L2/L3 traffic flow statistics
################################################################################
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
## Stop L2/L3 traffic
##################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# Stop all protocols
################################################################################
print("Stopping All Protocols");
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!\n");

