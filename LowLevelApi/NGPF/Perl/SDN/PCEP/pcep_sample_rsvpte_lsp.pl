
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
#   1. This scripts shows how we should configure PCC/RSVP to synchronize      #
#      RSVP-TE LSPs by PCC. RSVP-TE and PCC will be running on same device and #
#      LSPs that are brought up by the RSVP-TE will be synchronized by the     #
#      PCC to the PCE.                                                         #
#   2. Assign ports.                                                           #
#   3. Start all protocols.                                                    #
#   4. Retrieve PCE Sessions Per Port statistics.                              #
#   5. Retrieve PCC Per port statistics.                                       #
#   6. Stop all protocols.                                                     #
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
my @ports       = (('10.216.108.96', '4', '3'), ('10.216.108.96', '4', '4'));
my $ixTclServer = '10.216.108.113';
my $ixTclPort   = '8074';
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

################################################################################
# Connect to IxNet client
################################################################################
print("Connect to IxNetwork Tcl server
");
$ixNet->connect($ixTclServer,
                '-port',        $ixTclPort,
                '-version',      '8.00',
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
# Adding PCE layer
################################################################################
print("Adding PCE 1\n");
my $pce1 = $ixNet->add($ipv4Addr1, 'pce');
$ixNet->commit();
$pce1 = ($ixNet->remapIds($pce1))[0];
################################################################################
# Adding PCC Group
# Configured parameters :
#    -pccIpv4Address
#    -multiplier
#    -pceInitiatedLspsPerPcc
################################################################################
print("Adding PCC Group1");
my $pccGroup1 = $ixNet->add($pce1, 'pccGroup');
$ixNet->commit();
$pccGroup1 = ($ixNet->remapIds($pccGroup1))[0];
my $pccIpv4AddressMv = $ixNet->getAttribute($pccGroup1, '-pccIpv4Address');
$ixNet->add($pccIpv4AddressMv, 'singleValue');
$ixNet->setMultiAttribute($pccIpv4AddressMv.'/singleValue',
            '-value', '1.1.1.2');
$ixNet->commit();
$ixNet->setAttribute($pccGroup1, '-multiplier', '1');
$ixNet->commit();
$ixNet->setAttribute($pccGroup1, '-pceInitiatedLspsPerPcc', '0');
$ixNet->commit();

################################################################################
# Adding RSVP layer
# Configured parameters :
#    -dutIp
################################################################################
print("Adding rsvp 1\n");
my $rsvpIf1 = $ixNet->add($ipv4Addr1, 'rsvpteIf');
$ixNet->commit();
$rsvpIf1 = ($ixNet->remapIds($rsvpIf1))[0];
my $dutIpMv = $ixNet->getAttribute($rsvpIf1, '-dutIp');
$ixNet->add($dutIpMv, 'singleValue');
$ixNet->setMultiAttribute($dutIpMv.'/singleValue',
            '-value', '1.1.1.2');
################################################################################
# Adding RSVP LSP
# Configured parameters :
#    -ingressP2PLsps
################################################################################
print("Adding rsvp 1\n");
my $rsvpteLsps1 = $ixNet->add($ipv4Addr1, 'rsvpteLsps');
$ixNet->commit();
$rsvpteLsps1 = ($ixNet->remapIds($rsvpteLsps1))[0];

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
$ixNet->add($addressMv, 'singleValue');
$ixNet->setMultiAttribute($addressMv.'/singleValue',
            '-value', '1.1.1.2');
$ixNet->commit();
my $gatewayIpMv = $ixNet->getAttribute($ipv4Addr2, '-gatewayIp');
$ixNet->add($gatewayIpMv, 'singleValue');
$ixNet->setMultiAttribute($gatewayIpMv.'/singleValue',
            '-value', '1.1.1.1');
$ixNet->commit();
################################################################################
# Adding PCC layer
# Configured parameters :
#    -pceIpv4Address
#    -expectedInitiatedLspsForTraffic
#    -preEstablishedSrLspsPerPcc
#    -requestedLspsPerPcc
################################################################################
print("Adding PCC 2\n");
my $pcc2 = $ixNet->add($ipv4Addr2, 'pcc');
$ixNet->commit();
$pcc2 = ($ixNet->remapIds($pcc2))[0];
my $pceIpv4AddressMv = $ixNet->getAttribute($pcc2, '-pceIpv4Address');
$ixNet->add($pceIpv4AddressMv, 'singleValue');
$ixNet->setMultiAttribute($pceIpv4AddressMv.'/singleValue',
            '-value', '1.1.1.1');
$ixNet->setAttribute($pcc2, '-expectedInitiatedLspsForTraffic', '0');
$ixNet->setAttribute($pcc2, '-preEstablishedSrLspsPerPcc', '0');
$ixNet->setAttribute($pcc2, '-requestedLspsPerPcc', '0');

################################################################################
# Adding RSVP layer
# Configured parameters :
#    -dutIp
################################################################################
print("Adding rsvp 2\n");
my $rsvpIf2 = $ixNet->add($ipv4Addr2, 'rsvpteIf');
$ixNet->commit();
$rsvpIf2 = ($ixNet->remapIds($rsvpIf2))[0];
my $dutIpMv = $ixNet->getAttribute($rsvpIf2, '-dutIp');
$ixNet->add($dutIpMv, 'singleValue');
$ixNet->setMultiAttribute($dutIpMv.'/singleValue',
            '-value', '1.1.1.1');
################################################################################
# Adding RSVP LSP
# Configured parameters :
#    -ingressP2PLsps
################################################################################
print("Adding rsvp 2\n");
my $rsvpteLsps2 = $ixNet->add($ipv4Addr2, 'rsvpteLsps');
$ixNet->commit();
$rsvpteLsps2 = ($ixNet->remapIds($rsvpteLsps2))[0];
################################################################################
# Adding RSVP P2P tunnel
# Configured parameters :
#    -tunnelId
#    -remoteIp
################################################################################
my $rsvpp2p2 = $rsvpteLsps2.'/rsvpP2PIngressLsps';
my $tunnelIdMv = $ixNet->getAttribute($rsvpp2p2, '-tunnelId');
$ixNet->add($tunnelIdMv, 'counter');
$ixNet->setMultiAttribute($tunnelIdMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '1',
             '-step'     , '1');
$ixNet->commit();
my $remoteIpMv = $ixNet->getAttribute($rsvpp2p2, '-remoteIp');
$ixNet->add($remoteIpMv, 'singleValue');
$ixNet->setMultiAttribute($remoteIpMv.'/singleValue',
            '-value', '1.1.1.1');
$ixNet->commit();


################################################################################
# Assign ports
################################################################################
print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, 
                '-port', $ixTclPort, 
                '-version', '8.00', 
                '-setAttribute', 'strict');
my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vport1 = $vPorts[0];
my $vport2 = $vPorts[1];
assignPorts($ixNet, @ports, $vport1, $vport2);
sleep(5);
print "Starting all protocols\n";
################################################################################
# Start all protocols
################################################################################
$ixNet->execute('startAllProtocols');
print "Wait for 1 minute";
sleep(60);

################################################################################
# Retrieve protocol statistics. (PCE Sessions Per Port)
################################################################################
print("Fetching all PCE Sessions Per Port Stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"PCE Sessions Per Port"/page';
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
# Retrieve protocol statistics. (PCC Per Port)
################################################################################
print("Fetching all PCC Per Port Stats\n");
$viewPage = '::ixNet::OBJ-/statistics/view:"PCC Per Port"/page';
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


