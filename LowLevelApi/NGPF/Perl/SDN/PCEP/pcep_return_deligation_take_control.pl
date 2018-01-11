
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
#    This script intends to demonstrate how to use NGPF PCEP API.              #
#      1.  Configure a PCE on topology1 (with 10 PCC group) and a 10 PCC on    #
#          topology2. PCE has 10 PCE initiated LSP configured (1 per PCC).     #
#          Each PCE initiated LSP has 1 ERO. On the Topology 2 each PCC has    #
#          one pre-established LSP configured with 1 ERO each.                 #
#      2.  Assign ports                                                        #
#      3.  Start both PCC and PCE                                              #
#      4.  Retrieve "PCE Sessions Per Port" statistics                         #
#      5.  Execute return delegation from PCE end                              #
#      6.  Check LSP status                                                    #
#      7.  Execute take control from PCE end                                   #
#      8.  Retrieve "PCE Sessions Per Port" statistics                         #
#      9.  Check LSP status.                                                   #
#     10. Stop all protocols.                                                  #
# Ixia Softwares:                                                              #
#    IxOS      8.10 EA                                                         #
#    IxNetwork 8.10 EA                                                         #
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
$ixNet->add($pccIpv4AddressMv, 'counter');
$ixNet->setMultiAttribute($pccIpv4AddressMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '1.1.1.2',
             '-step'     , '0.0.0.1');
$ixNet->commit();
$ixNet->setAttribute($pccGroup1, '-multiplier', '10');
$ixNet->commit();
$ixNet->setAttribute($pccGroup1, '-pceInitiatedLspsPerPcc', '1');
$ixNet->commit();
################################################################################
# Adding PCE Initiated LSP parameterd
# Configured parameters :
#    -numberOfEroSubObjects
#    -srcEndPointIpv4
#    -destEndPointIpv4
#    -symbolicPathName
################################################################################
my $pccInit1 = $pccGroup1.'/pceInitiateLspParameters:1';
$ixNet->setAttribute($pccInit1, '-numberOfEroSubObjects', '1');
$ixNet->commit();
my $srcEndPointIpv4Mv = $ixNet->getAttribute($pccInit1, '-srcEndPointIpv4');
$ixNet->add($srcEndPointIpv4Mv, 'counter');
$ixNet->setMultiAttribute($srcEndPointIpv4Mv.'/counter',  
             '-direction', 'increment',
             '-start'    , '100.0.0.1',
             '-step'     , '0.0.0.1');
$ixNet->commit();
my $destEndPointIpv4Mv = $ixNet->getAttribute($pccInit1, '-destEndPointIpv4');
$ixNet->add($destEndPointIpv4Mv, 'counter');
$ixNet->setMultiAttribute($destEndPointIpv4Mv.'/counter',  
             '-direction', 'increment',
             '-start'    , '200.0.0.1',
             '-step'     , '0.0.0.1');
$ixNet->commit();
my $symbolicPathNameMv = $ixNet->getAttribute($pccInit1, '-symbolicPathName');
$ixNet->add($symbolicPathNameMv, 'string');
$ixNet->setMultiAttribute($symbolicPathNameMv.'/string',
            '-pattern', 'IXIA LSP {Inc:1,1}');
$ixNet->commit();
################################################################################
# Adding ERO parameterd
# Configured parameters :
#    -mplsLabel
#    -localIpv4Address
#    -remoteIpv4Address
#    -fBit
#    -sidType
################################################################################
my $pccEro1 = $pccInit1.'/pcepEroSubObjectsList:1';
my $mplsLabelMv = $ixNet->getAttribute($pccEro1, '-mplsLabel');
$ixNet->add($mplsLabelMv, 'counter');
$ixNet->setMultiAttribute($mplsLabelMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '16',
             '-step'     , '1');
$ixNet->commit();
my $localIpv4AddressMv = $ixNet->getAttribute($pccEro1, '-localIpv4Address');
$ixNet->add($localIpv4AddressMv, 'singleValue');
$ixNet->setMultiAttribute($localIpv4AddressMv.'/singleValue',
            '-value', '0.0.0.0');
$ixNet->commit();
my $remoteIpv4AddressMv = $ixNet->getAttribute($pccEro1, '-remoteIpv4Address');
$ixNet->add($remoteIpv4AddressMv, 'singleValue');
$ixNet->setMultiAttribute($remoteIpv4AddressMv.'/singleValue',
            '-value', '0.0.0.0');
$ixNet->commit();
my $fBitMv = $ixNet->getAttribute($pccEro1, '-fBit');
$ixNet->add($fBitMv, 'singleValue');
$ixNet->setMultiAttribute($fBitMv.'/singleValue',
            '-value', 'true');
$ixNet->commit();
my $sidTypeMv = $ixNet->getAttribute($pccEro1, '-sidType');
$ixNet->add($sidTypeMv, 'singleValue');
$ixNet->setMultiAttribute($sidTypeMv.'/singleValue',
            '-value', 'mplslabel20bit');
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
$ixNet->setAttribute($device2, '-multiplier', '10');
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
$ixNet->setAttribute($pcc2, '-preEstablishedSrLspsPerPcc', '1');
$ixNet->setAttribute($pcc2, '-requestedLspsPerPcc', '0');
################################################################################
# Adding pre established  sr LSP
# Configured parameters :
#    -symbolicPathName
#    -srcEndPointIpv4
#    -srcEndPointIpv6
################################################################################
my $preLsp2 = $pcc2.'/preEstablishedSrLsps:1';
my $symbolicPathNameMv = $ixNet->getAttribute($preLsp2, '-symbolicPathName');
$ixNet->add($symbolicPathNameMv, 'string');
$ixNet->setMultiAttribute($symbolicPathNameMv.'/string',
            '-pattern', 'IXIA LSP {Inc:1,1}');
my $srcEndPointIpv4Mv = $ixNet->getAttribute($preLsp2, '-srcEndPointIpv4');
$ixNet->add($srcEndPointIpv4Mv, 'singleValue');
$ixNet->setMultiAttribute($srcEndPointIpv4Mv.'/singleValue',
            '-value', '0.0.0.0');
my $srcEndPointIpv6Mv = $ixNet->getAttribute($preLsp2, '-srcEndPointIpv6');
$ixNet->add($srcEndPointIpv6Mv, 'singleValue');
$ixNet->setMultiAttribute($srcEndPointIpv6Mv.'/singleValue',
            '-value', '0:0:0:0:0:0:0:0');
################################################################################
# Adding pre established ERO of sr LSP
# Configured parameters :
#    -mplsLabel
#    -localIpv4Address
#    -remoteIpv4Address
#    -fBit
#    -sidType
################################################################################
my $preSr2 = $preLsp2.'/pcepEroSubObjectsList:1';
my $mplsLabelMv = $ixNet->getAttribute($preSr2, '-mplsLabel');
$ixNet->add($mplsLabelMv, 'counter');
$ixNet->setMultiAttribute($mplsLabelMv.'/counter',  
             '-direction', 'increment',
             '-start'    , '16',
             '-step'     , '1');
$ixNet->commit();
my $localIpv4AddressMv = $ixNet->getAttribute($preSr2, '-localIpv4Address');
$ixNet->add($localIpv4AddressMv, 'singleValue');
$ixNet->setMultiAttribute($localIpv4AddressMv.'/singleValue',
            '-value', '0.0.0.0');
$ixNet->commit();
my $remoteIpv4AddressMv = $ixNet->getAttribute($preSr2, '-remoteIpv4Address');
$ixNet->add($remoteIpv4AddressMv, 'singleValue');
$ixNet->setMultiAttribute($remoteIpv4AddressMv.'/singleValue',
            '-value', '0.0.0.0');
$ixNet->commit();
my $fBitMv = $ixNet->getAttribute($preSr2, '-fBit');
$ixNet->add($fBitMv, 'singleValue');
$ixNet->setMultiAttribute($fBitMv.'/singleValue',
            '-value', 'true');
$ixNet->commit();
my $sidTypeMv = $ixNet->getAttribute($preSr2, '-sidType');
$ixNet->add($sidTypeMv, 'singleValue');
$ixNet->setMultiAttribute($sidTypeMv.'/singleValue',
            '-value', 'mplslabel20bit');
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
# Execute take control
################################################################################
print "Executing return delegation";
for (my $i = 1; $i <=10; $i++) {
    $ixNet->execute('returnDelegation', $pccInit1, $i);
} 

#################################################################################
#  6. Check LSP state
#################################################################################
print "Checking LSP State";
my @lspState = $ixNet->getAttribute($pccInit1, '-sessionInfo');
my $lspNo = 1;
foreach my $ls (@lspState) {
    print "State of LSP $lspNo is $ls\n";
    $lspNo++;
}


################################################################################
# Execute take control
################################################################################
print "Executing take control";
for (my $i = 1; $i <=10; $i++) {
    $ixNet->execute('takeControl', $pccInit1, $i);
}

#################################################################################
#  6. Check LSP state
#################################################################################
print "Checking LSP State";
my @lspState = $ixNet->getAttribute($pccInit1, '-sessionInfo');
my $lspNo = 1;
foreach my $ls (@lspState) {
    print "State of LSP $lspNo is $ls\n";
    $lspNo++;
}

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
# Stop all protocols                                                           #
################################################################################
print "Stopping all protocol\n";
$ixNet->execute('stopAllProtocols');

