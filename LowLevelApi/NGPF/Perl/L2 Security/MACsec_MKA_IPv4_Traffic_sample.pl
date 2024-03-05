################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA                                             #
#    All Rights Reserved.                                                      #
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
# Description: 
# 1. Configuring MKA and MACSec (HW based)
# 2. Create traffic Item
# 3. Assign ports
# 4. Start all protocols
# 5. Retrieve protocol statistics. (MACsec Per Port)
# 6. Start traffic
# 7. Stop traffic
# 8. Stop all protocols
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

# Edit this variables values to match your setup
my @ports       = (('10.36.74.52', '1', '13'), ('10.36.74.52', '1', '17'));
my $ixTclServer = '10.36.67.90';
my $ixTclPort   = '8909';
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

################################################################################
# Connect to IxNet client
################################################################################
print("Connect to IxNetwork Tcl server");
$ixNet->connect($ixTclServer,
                '-port',        $ixTclPort,
                '-version',      '9.01',
                '-setAttribute', 'strict');
################################################################################
# Clean up IxNetwork
################################################################################
print("Clean up IxNetwork GUI");
$ixNet->execute('newConfig');
print("Get IxNetwork root object\n");
my $root = $ixNet->getRoot();

################################################################################
# Adding virtual ports
################################################################################
print("Add virtual port 1\n");
my $vport1 = $ixNet->add($root, 'vport');
$ixNet->commit();
$vport1 = ($ixNet->remapIds($vport1))[0];

print("Add virtual port 2\n");
my $vport2 = $ixNet->add($root, 'vport');
$ixNet->commit();
$vport2 = ($ixNet->remapIds($vport2))[0];

################################################################################
# Add topology
################################################################################
print("Add Topology 1\n");
my $topology1 = $ixNet->add($root, 'topology');
$ixNet->commit();
$topology1 = ($ixNet->remapIds($topology1))[0];
$ixNet->setAttribute($topology1, '-vports', $vport1);
$ixNet->commit();
################################################################################
# Add Device Group in Topoloy 1
################################################################################
print("Add Device Group 1 \n");
my $device1 = $ixNet->add($topology1, 'deviceGroup');
$ixNet->commit();
$device1 = ($ixNet->remapIds($device1))[0];
$ixNet->setAttribute($device1, '-name', 'Device Group 1');
$ixNet->setAttribute($device1, '-multiplier', '10');
$ixNet->commit();
################################################################################
# Add Ethernet in Device Group 1
################################################################################
print("Add Ethernet 1\n");
my $ethernet1 = $ixNet->add($device1, 'ethernet');
$ixNet->commit();
$ethernet1 = ($ixNet->remapIds($ethernet1))[0];
my $macMv = $ixNet->getAttribute($ethernet1, '-mac');
$ixNet->add($macMv, 'counter');
$ixNet->setMultiAttribute($macMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '00:11:01:00:00:01',
             '-step'     , '00:00:00:00:00:01');

################################################################################
# Add Macsec on top of Ethernet in Device Group 1
################################################################################
print("Add MACsec in Device Group 1\n");
my $macsec1 = $ixNet->add($ethernet1, 'macsec');
$ixNet->commit();

################################################################################
# Add MKA in Device Group 1
################################################################################
print("Add MKA in Device Group 1\n");
my $mka1 = $ixNet->add($ethernet1, 'mka');
$ixNet->commit();
$mka1 = ($ixNet->remapIds($mka1))[0];

################################################################################
# Set CipherSuite AES-XPN-128 for all devices in MKA 1
################################################################################
print("Set CipherSuite AES-XPN-128 for all devices in MKA 1\n");
my $cipherSuite1 = $ixNet->getAttribute($mka1, '-cipherSuite');
$cipherSuite1 = ($ixNet->remapIds($cipherSuite1))[0];
my $cipherSuiteOverlay1 = $ixNet->add($cipherSuite1, 'overlay');
my $cipherSuiteOverlay1 = ($ixNet->remapIds($cipherSuiteOverlay1))[0];
my $loop1 = 1;
for( $loop1 = 1; $loop1 <= 10; $loop1 = $loop1 + 1 ) {
	$ixNet->setMultiAttribute($cipherSuiteOverlay1, '-index', $loop1, '-count', '1', '-value', 'aesxpn128');
	$ixNet->commit();
	sleep(1);
}
################################################################################
# Add topology
################################################################################
print("Add Topology 2\n");
my $topology2 = $ixNet->add($root, 'topology');
$ixNet->commit();
$topology2 = ($ixNet->remapIds($topology2))[0];
$ixNet->setAttribute($topology2, '-vports', $vport2);
$ixNet->commit();
################################################################################
# Add Device Group in Topoloy 2
################################################################################
print("Add Device Group in Topoloy 2\n");
my $device2 = $ixNet->add($topology2, 'deviceGroup');
$ixNet->commit();
$device2 = ($ixNet->remapIds($device2))[0];
$ixNet->setAttribute($device2, '-name', 'Device Group 2');
$ixNet->setAttribute($device2, '-multiplier', '10');
$ixNet->commit();
################################################################################
# Add Ethernet in Device Group 2
################################################################################
print("Add Ethernet 2\n");
my $ethernet2 = $ixNet->add($device2, 'ethernet');
$ixNet->commit();
$ethernet2 = ($ixNet->remapIds($ethernet2))[0];
my $macMv = $ixNet->getAttribute($ethernet2, '-mac');
$ixNet->add($macMv, 'counter');
$ixNet->setMultiAttribute($macMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '00:12:01:00:00:01',
             '-step'     , '00:00:00:00:00:01');

################################################################################
# Add Macsec on top of Ethernet in Device Group 2
################################################################################
print("Add MACsec in Device Group 2\n");
my $macsec2 = $ixNet->add($ethernet2, 'macsec');
$ixNet->commit();
$macsec2 = ($ixNet->remapIds($macsec2))[0];

################################################################################
# Add MKA in Device Group 2
################################################################################
print("Add MKA in Device Group 2\n");
my $mka2 = $ixNet->add($ethernet2, 'mka');
$ixNet->commit();
$mka2 = ($ixNet->remapIds($mka2))[0];

################################################################################
# Set CipherSuite AES-XPN-128 for all devices in MKA 1
################################################################################
print("Set CipherSuite AES-XPN-128 for all devices in MKA 2\n");
my $cipherSuite2 = $ixNet->getAttribute($mka2, '-cipherSuite');
$cipherSuite2 = ($ixNet->remapIds($cipherSuite2))[0];
my $cipherSuiteOverlay2 = $ixNet->add($cipherSuite2, 'overlay');
my $cipherSuiteOverlay2 = ($ixNet->remapIds($cipherSuiteOverlay2))[0];
my $loop1 = 1;
for( $loop1 = 1; $loop1 <= 10; $loop1 = $loop1 + 1 ) {
	$ixNet->setMultiAttribute($cipherSuiteOverlay2, '-index', $loop1, '-count', '1', '-value', 'aesxpn128');
	$ixNet->commit();
	sleep(1);
}

################################################################################
# Add IPv4 on top of MACsec
################################################################################
print("Add IPv4 on top of MACsec \n");
$ixNet->add($macsec1, 'ipv4');
$ixNet->add($macsec2, 'ipv4');
$ixNet->commit();

my $ip1 = ($ixNet->getList($macsec1, 'ipv4'))[0];
my $ip2 = ($ixNet->getList($macsec2, 'ipv4'))[0];

my $mvAdd1 = $ixNet->getAttribute($ip1, '-address');
my $mvAdd2 = $ixNet->getAttribute($ip2, '-address');
my $mvGw1  = $ixNet->getAttribute($ip1, '-gatewayIp');
my $mvGw2  = $ixNet->getAttribute($ip2, '-gatewayIp');

print("Configure ipv4 addresses \n");
$ixNet->setAttribute($mvAdd1.'/counter', '-direction', "increment", '-start', '20.20.1.1', '-step', '0.0.1.0');
$ixNet->setAttribute($mvAdd2.'/counter', '-direction', "increment", '-start', '20.20.2.1', '-step', '0.0.1.0');
$ixNet->setAttribute($mvGw1.'/counter', '-direction', "increment", '-start', '20.20.2.1', '-step', '0.0.1.0');
$ixNet->setAttribute($mvGw2.'/counter', '-direction', "increment", '-start', '20.20.1.1', '-step', '0.0.1.0');

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '24');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '24');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

################################################################################
# 2. Create L3 Traffic over IPv4 end points from Device Group 1 to Device Group 2
################################################################################
print ("Create L3 Traffic over IPv4 end points from Device Group 1 to Device Group 2\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'Macsec_IPv4_L3_Traffic',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ipv4');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source       = ($topology1.'/deviceGroup:1/ethernet:1/macsec:1/ipv4:1');
my @destination  = ($topology2.'/deviceGroup:1/ethernet:1/macsec:1/ipv4:1');

$ixNet->setMultiAttribute($endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', [[]],
    '-scalableSources',       [],
    '-multicastReceivers',    [[]],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               @source,
    '-destinations',          @destination);
$ixNet->commit();

################################################################################
# set frame size in Traffic Item
################################################################################
$ixNet->setMultiAttribute($trafficItem1.'/configElement:1/frameSize', 
	'-incrementFrom', '72', 
	'-incrementTo', '1518', 
	'-type', 'increment');
	
################################################################################
# set frame rate in Traffic Item
################################################################################	
$ixNet->setMultiAttribute($trafficItem1.'/configElement:1/frameRate', 
	'-rate', '100');

$ixNet->setMultiAttribute($trafficItem1.'/tracking',
    '-trackBy', ['ipv4DestIp0'],,
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();

################################################################################
# 3. Assign ports
################################################################################
my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vport1 = $vPorts[0];
my $vport2 = $vPorts[1];
assignPorts($ixNet, @ports, $vport1, $vport2);


################################################################################
# 4. Start all protocols
################################################################################
print "Start all protocols\n";
$ixNet->execute('startAllProtocols');
print "Wait for 30 seconds\n";
sleep(30);

################################################################################
# 5. Retrieve protocol statistics. (MACsec Per Port)
################################################################################
print("Fetch MACsec Per Port Statistics \n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"MACsec Per Port"/page';
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
# 6. Generate, apply and Start traffic
###############################################################################
my @traffic_items = $ixNet->getList(($ixNet->getRoot()).'/traffic', 'trafficItem');
foreach my $item (@traffic_items) {
	print ("Generate the configured Traffic Item\n");
    $ixNet->execute('generate', $item);
}
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

print("Run Traffic for 30 secs \n"); 
sleep(30);

################################################################################
# Retrieve Traffic Item Flow Statistics 
################################################################################
print "Retrieve Flow Statistics\n";
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
# 7. Stop traffic
################################################################################
print("Stop L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');

################################################################################
# Stop all protocols                                                           #
################################################################################
print "Stop all protocols\n";
$ixNet->execute('stopAllProtocols');
print "Test Script ends\n";
