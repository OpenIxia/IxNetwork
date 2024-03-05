################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
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
# Description :                                                                #
#   1. This scripts shows how we should configure Netconf Client & Netconf 	   #
#      Server. Different capoabilities configuration.						   #
#   2. Assign ports.                                                           #
#   3. Start all protocols.                                                    #
#   4. Send Command Snippet of Netconf executing Right Click Action	   		   #
#   5. Retrieve Netconf Client Sessions Per Port statistics.                   #
#   6. Retrieve Netconf Server Per port statistics.                            #
#   7. Stop all protocols.    												   #
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
my @ports       = (('10.39.50.227', '1', '5'), ('10.39.50.227', '1', '6'));
my $ixTclServer = '10.39.50.102';
my $ixTclPort   = '8785';
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

################################################################################
# Connect to IxNet client
################################################################################
print("Connect to IxNetwork Tcl server");
$ixNet->connect($ixTclServer,
                '-port',        $ixTclPort,
                '-version',      '8.50',
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
# Adding IPv4 layer
################################################################################
print("Adding ipv4 1\n");
my $ipv4Addr1 = $ixNet->add($ethernet1, 'ipv4');
$ixNet->commit();
$ipv4Addr1 = ($ixNet->remapIds($ipv4Addr1))[0];
my $addressMv = $ixNet->getAttribute($ipv4Addr1, '-address');
$ixNet->add($addressMv, 'singleValue');
$ixNet->setMultiAttribute($addressMv.'/singleValue',
            '-value', '1.1.1.1');
$ixNet->commit();
my $gatewayIpMv = $ixNet->getAttribute($ipv4Addr1, '-gatewayIp');
$ixNet->add($gatewayIpMv, 'singleValue');
$ixNet->setMultiAttribute($gatewayIpMv.'/singleValue',
            '-value', '1.1.1.2');
$ixNet->commit();
################################################################################
# Adding Netcont Server layer
# Configured parameters :
################################################################################
print("Adding Netcont Server 1\n");
my $netconfServer1 = $ixNet->add($ipv4Addr1, 'netconfServer');
$ixNet->commit();
$netconfServer1 = ($ixNet->remapIds($netconfServer1))[0];
my $clientIPMv = $ixNet->getAttribute($netconfServer1, '-clientIpv4Address');
$ixNet->add($clientIPMv, 'singleValue');
$ixNet->setMultiAttribute($clientIPMv.'/singleValue',
            '-value', '1.1.1.2');

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
# Adding IPv4 layer
################################################################################
print("Adding ipv4 2\n");
my $ipv4Addr2 = $ixNet->add($ethernet2, 'ipv4');
$ixNet->commit();
$ipv4Addr2 = ($ixNet->remapIds($ipv4Addr2))[0];
my $addressMv = $ixNet->getAttribute($ipv4Addr2, '-address');
$ixNet->add($addressMv, 'counter');
$ixNet->setMultiAttribute($addressMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '1.1.1.2',
             '-step'     , '0.0.0.1');
$ixNet->commit();
my $gatewayIpMv = $ixNet->getAttribute($ipv4Addr2, '-gatewayIp');
$ixNet->add($gatewayIpMv, 'singleValue');
$ixNet->setMultiAttribute($gatewayIpMv.'/singleValue',
            '-value', '1.1.1.1');
$ixNet->commit();
################################################################################
# Adding Netconf Client layer
# Configured parameters :
#    -pceIpv4Address
#    -expectedInitiatedLspsForTraffic
#    -preEstablishedSrLspsPerPcc
#    -requestedLspsPerPcc
################################################################################
print("Adding Netconf Client 2\n");
my $netconfClient2 = $ixNet->add($ipv4Addr2, 'netconfClient');
$ixNet->commit();
$netconfClient2 = ($ixNet->remapIds($netconfClient2))[0];
my $serverIPMv = $ixNet->getAttribute($netconfClient2, '-serverIpv4Address');
$ixNet->add($serverIPMv, 'singleValue');
$ixNet->setMultiAttribute($serverIPMv.'/singleValue',
            '-value', '1.1.1.1');

#Adding Netconf Client 2 Command Snippet Data
print("Adding Netconf Client 2 Command Snippet Data \n");
my @commandSnippetsDataMv = $ixNet->getList($netconfClient2, 'commandSnippetsData');
my $commandSnippetsData1 = $commandSnippetsDataMv[0];
$ixNet->commit();
$commandSnippetsData1 = ($ixNet->remapIds($commandSnippetsData1))[0];
$ixNet->commit();

#Setting Command Snippet Directory
print("Setting Command Snippet Directory \n");
my $commandSnippetDirectoryMv = $ixNet->getAttribute($commandSnippetsData1, '-commandSnippetDirectory');
$ixNet->commit();
$commandSnippetDirectoryMv = ($ixNet->remapIds($commandSnippetDirectoryMv))[0];
$ixNet->commit();

$ixNet->setAttribute($commandSnippetDirectoryMv.'/singleValue', '-value',  "C:\\Program Files (x86)\\Ixia\\IxNetwork\\8.50-EA\\SampleScripts\\IxNetwork\\NGPF\\Tcl\\SDN\\Netconf");
$ixNet->commit();

#Setting Command Snippet File Name
print("Setting Command Snippet File Name \n");
my $commandSnippetFile1 = $ixNet->getAttribute($commandSnippetsData1, '-commandSnippetFile');
$ixNet->commit();
$commandSnippetFile1 = ($ixNet->remapIds($commandSnippetFile1))[0];
$ixNet->commit();

$ixNet->setMultiAttribute($commandSnippetFile1.'/singleValue', '-value', "Get-config.xml");
$ixNet->commit();

#Setting Command Snippet Active
print("Setting Command Snippet Active \n");
my $commandSnippetDataActive1 = $ixNet->getAttribute($commandSnippetsData1, '-active');
$ixNet->commit();
my $commandSnippetDataActive1 = ($ixNet->remapIds($commandSnippetDataActive1))[0];
$ixNet->commit();
$ixNet->setAttribute($commandSnippetDataActive1.'/singleValue', '-value', 'true');
$ixNet->commit();

#Setting Command Snippet Transmission Behaviour
print("Setting Command Snippet Transmission Behaviour \n");
my $transmissionBehaviour1 = $ixNet->getAttribute($commandSnippetsData1, '-transmissionBehaviour');
$ixNet->commit();
$transmissionBehaviour1 = ($ixNet->remapIds($transmissionBehaviour1))[0];
$ixNet->commit();
my $transmissionBehaviourOv = $ixNet->add($transmissionBehaviour1, 'overlay');
$ixNet->commit();
$transmissionBehaviourOv = ($ixNet->remapIds($transmissionBehaviourOv))[0];
$ixNet->commit();

$ixNet->setMultiAttribute($transmissionBehaviourOv, '-count', '1', '-index', '1', '-value', "once");
$ixNet->commit();
$ixNet->setMultiAttribute($transmissionBehaviourOv, '-count', '1', '-index', '2', '-value', "periodiccontinuous");
$ixNet->commit();
################################################################################
# Assign ports
################################################################################
print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, 
                '-port', $ixTclPort, 
                '-version', '8.50', 
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
print "Wait for 1 minute";
sleep(60);

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
# 4. Sending Command Snippet by executing Right Click Action 				   #
################################################################################
print("Sending Command Snippet by executing Right Click Action");
$ixNet->execute('executeCommand', $commandSnippetsData1, '1');
sleep(15);

################################################################################
# Retrieve protocol statistics. (Netconf Server Per Port)
################################################################################
print("Fetching all Netconf Server Per Port Stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"Netconf Server Per Port"/page';
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
# Retrieve protocol statistics. (Netconf Client Per Port)
################################################################################
print("Fetching all Netconf Client Per Port Stats\n");
$viewPage = '::ixNet::OBJ-/statistics/view:"Netconf Client Per Port"/page';
@statcap  = $ixNet->getAttribute($viewPage, '-columnCaptions');
@rowvals  = $ixNet->getAttribute($viewPage, '-rowValues');
$index    = 0;
$statValueList= '';
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
# Stop all protocols                                                           #
################################################################################
print "Stopping all protocol\n";
$ixNet->execute('stopAllProtocols');

