################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA                                           #
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
# 1. Configuring macsec Hardware Based IP Data Traffic.
# 2. Assign ports
# 3. Start all protocols
# 4. Create traffic Item
# 5. Start traffic
# 6. Stop traffic
# 7. Stop all protocols  												   
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
my @ports       = (('10.39.50.226', '1', '5'), ('10.39.50.226', '1', '6'));
my $ixTclServer = '10.39.50.102';
my $ixTclPort   = '9890';
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
# Cleaning up IxNetwork
################################################################################
$ixNet->execute('newConfig');
print("Get IxNetwork root object\n");
my $root = $ixNet->getRoot();

################################################################################
# Adding virtual ports
################################################################################
print("Adding virtual port 1\n");
my $vport1 = $ixNet->add($root, 'vport');
$ixNet->commit();
$vport1 = ($ixNet->remapIds($vport1))[0];

print("Adding virtual port 2\n");
my $vport2 = $ixNet->add($root, 'vport');
$ixNet->commit();
$vport2 = ($ixNet->remapIds($vport2))[0];

################################################################################
# Adding topology
################################################################################
print("Adding topology 1\n");
my $topology1 = $ixNet->add($root, 'topology');
$ixNet->commit();
$topology1 = ($ixNet->remapIds($topology1))[0];
$ixNet->setAttribute($topology1, '-vports', $vport1);
$ixNet->commit();
################################################################################
# Adding device group
################################################################################
print("Adding device group 1\n");
my $device1 = $ixNet->add($topology1, 'deviceGroup');
$ixNet->commit();
$device1 = ($ixNet->remapIds($device1))[0];
$ixNet->setAttribute($device1, '-name', 'Device Group 1');
$ixNet->setAttribute($device1, '-multiplier', '1');
$ixNet->commit();
################################################################################
# Adding ethernet layer
################################################################################
print("Adding ethernet 1\n");
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
# Adding Static Macsec layer 1
################################################################################
print("Adding Static Macsec layer 1\n");
my $staticMacsec1 = $ixNet->add($ethernet1, 'staticMacsec');
$ixNet->commit();
$staticMacsec1 = ($ixNet->remapIds($staticMacsec1))[0];
my $dutMacMv = $ixNet->getAttribute($staticMacsec1, '-dutMac');
$ixNet->add($dutMacMv, 'counter');
$ixNet->setMultiAttribute($dutMacMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '00:12:01:00:00:01',
             '-step'     , '00:00:00:00:00:01');
$ixNet->commit();

my $dutSciMacMv = $ixNet->getAttribute($staticMacsec1, '-dutSciMac');
$ixNet->add($dutSciMacMv, 'counter');
$ixNet->setMultiAttribute($dutSciMacMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '00:12:01:00:00:01',
             '-step'     , '00:00:00:00:00:01');
$ixNet->commit();

my $portIdMv = $ixNet->getAttribute($staticMacsec1, '-portId');
$ixNet->add($portIdMv, 'counter');
$ixNet->setMultiAttribute($portIdMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '30',
             '-step'     , '1');
$ixNet->commit();

my $dutSciPortIdMv = $ixNet->getAttribute($staticMacsec1, '-dutSciPortId');
$ixNet->add($dutSciPortIdMv, 'counter');
$ixNet->setMultiAttribute($dutSciPortIdMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '30',
             '-step'     , '1');
$ixNet->commit();
################################################################################
# Adding topology
################################################################################
print("Adding topology 2\n");
my $topology2 = $ixNet->add($root, 'topology');
$ixNet->commit();
$topology2 = ($ixNet->remapIds($topology2))[0];
$ixNet->setAttribute($topology2, '-vports', $vport2);
$ixNet->commit();
################################################################################
# Adding device group
################################################################################
print("Adding device group 2\n");
my $device2 = $ixNet->add($topology2, 'deviceGroup');
$ixNet->commit();
$device2 = ($ixNet->remapIds($device2))[0];
$ixNet->setAttribute($device2, '-name', 'Device Group 2');
$ixNet->setAttribute($device2, '-multiplier', '1');
$ixNet->commit();
################################################################################
# Adding ethernet layer
################################################################################
print("Adding ethernet 2\n");
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
# Adding Static Macsec layer 2
################################################################################
print("Adding Static Macsec layer 2\n");
my $staticMacsec2 = $ixNet->add($ethernet2, 'staticMacsec');
$ixNet->commit();
$staticMacsec2 = ($ixNet->remapIds($staticMacsec2))[0];
my $dutMacMv = $ixNet->getAttribute($staticMacsec2, '-dutMac');
$ixNet->add($dutMacMv, 'counter');
$ixNet->setMultiAttribute($dutMacMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '00:12:01:00:00:01',
             '-step'     , '00:00:00:00:00:01');
$ixNet->commit();

my $dutSciMacMv = $ixNet->getAttribute($staticMacsec2, '-dutSciMac');
$ixNet->add($dutSciMacMv, 'counter');
$ixNet->setMultiAttribute($dutSciMacMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '00:12:01:00:00:01',
             '-step'     , '00:00:00:00:00:01');
$ixNet->commit();

my $portIdMv = $ixNet->getAttribute($staticMacsec2, '-portId');
$ixNet->add($portIdMv, 'counter');
$ixNet->setMultiAttribute($portIdMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '30',
             '-step'     , '1');
$ixNet->commit();

my $dutSciPortIdMv = $ixNet->getAttribute($staticMacsec2, '-dutSciPortId');
$ixNet->add($dutSciPortIdMv, 'counter');
$ixNet->setMultiAttribute($dutSciPortIdMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '30',
             '-step'     , '1');
$ixNet->commit();
################################################################################
# Assign ports
################################################################################
print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, 
                '-port', $ixTclPort, 
                '-version', '9.01', 
                '-setAttribute', 'strict');

my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vport1 = $vPorts[0];
my $vport2 = $vPorts[1];
assignPorts($ixNet, @ports, $vport1, $vport2);

print "Starting all protocols\n";
################################################################################
# Start all protocols
################################################################################
$ixNet->execute('startAllProtocols');
print "Wait for 10 seconds\n";
sleep(10);

################################################################################
# 3. Retrieve protocol statistics                                              #
################################################################################
print("Fetching all Protocols Summary Stats\n");
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
# Retrieve protocol statistics. (Static MACsec Per Port)
################################################################################
print("Fetching all Static MACsec Per Port Stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"Static MACsec Per Port"/page';
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
# Configure L2-L3 traffic 
################################################################################

print ("Congfiguring L2-L3 Traffic Item\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'Static_Macsec_IP_Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ipv4');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source       = ($topology2.'/deviceGroup:1/ethernet:1/staticMacsec:1');
my @destination  = ($topology1.'/deviceGroup:1/ethernet:1/staticMacsec:1');

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

###############################################################################
# Apply and start L2/L3 traffic
###############################################################################

print("Applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("Starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');
sleep(20);

print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# Retrieve Traffic statistics.
################################################################################

print "Checking Stats to check if traffic was sent OK\n";
print "Getting the object for view Traffic Item Statistics\n";
my $viewName = "Traffic Item Statistics";
my @views = $ixNet->getList('/statistics', 'view');
my $viewObj = '::ixNet::OBJ-/statistics/view:"Traffic Item Statistics"';
print "Getting the Tx/Rx Frames values\n";
my @txFrames = $ixNet->execute('getColumnValues', $viewObj, 'Tx Frames');
my @rxFrames = $ixNet->execute('getColumnValues', $viewObj, 'Rx Frames');
if (@txFrames[0] != @rxFrames[0]) {
        print "Rx Frames != Tx Frames \n";
		}  else {
        print "No loss found: Rx Frames == Tx Frames\n";
}
print @rxFrames[0];
print "==";
print @txFrames[0];

################################################################################
# Stop all protocols                                                           #
################################################################################
print "Stopping all protocol\n";
$ixNet->execute('stopAllProtocols');

