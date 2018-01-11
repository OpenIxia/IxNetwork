################################################################################
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    19/02/2015 - Sumit Deb - created sample                                   #
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
#    This script intends to demonstrate how to use NGPF PCEP API.              #
#      1. Configures a PCE on the topology1 and a PCC on topology2. The PCE    #
#         channel has one LSP with two ERO in it. The PCC has one "Expected    #
#         PCE initiated LSP" configured in it. The "Symbolic Path Name" of the #
#         LSP in the PCE channel is same as that of "Expected PCE initiated    #
#         LSP" in the PCC. Also source end of the PCE initiated LSP at the PCE #
#         end is matching with that of "Expected PCE Initiated LSP" at the     #
#         PCC end.                                                             #
#      2. Stats PCC and PCE.                                                   #
#      3. Verify statistics from "Protocols Summary" view                      #
#      4. Fetch PCC learned information                                        #
#      5. Configure L2/L3 traffic - source end is the topology2 (PCC) and      #
#         destinaton end is topology1                                          #
#      6. Apply and start L2/L3 traffic.                                       #
#      7. Verify L2/L3 traffic statistics.                                     #
#      8. Stop traffic.                                                        #
#      9. Change the MPLS Label value in ERO1 of LSP1 at the PCE end in        #
#         topology1.                                                           #      
#     10. Wait for a few seconds and verify learned info                       #
#     11. Apply L2/L3 traffic.                                                 #
#     12. Verify traffic L2/L3 statistics.                                     #
#     13. Stop traffic.                                                        #
#     14. Stop all protocols.                                                  # 
# Ixia Software:                                                               #
#    IxOS      8.00 EA                                                         #
#    IxNetwork 8.00 EA                                                         #
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
my $ixTclServer = '10.216.108.113';
my $ixTclPort   = '8027';
my @ports       = (('10.216.108.104', '4', '1'), ('10.216.108.104', '4', '2'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '8.00', '-setAttribute', 'strict');

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

print("Add ipv4\n");
$ixNet->add($mac1, 'ipv4');
$ixNet->add($mac2, 'ipv4');
$ixNet->commit();

my $ip1 = ($ixNet->getList($mac1, 'ipv4'))[0];
my $ip2 = ($ixNet->getList($mac2, 'ipv4'))[0];

my $mvAdd1 = $ixNet->getAttribute($ip1, '-address');
my $mvAdd2 = $ixNet->getAttribute($ip2, '-address');
my $mvGw1  = $ixNet->getAttribute($ip1, '-gatewayIp');
my $mvGw2  = $ixNet->getAttribute($ip2, '-gatewayIp');

print("configuring ipv4 addresses\n");
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '20.20.20.2');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', "20.20.20.2");

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '24');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '24');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

print("Adding a PCE on Topology 1\n");
$ixNet->add($ip1, 'pce');
$ixNet->commit();
my $pce = ($ixNet->getList($ip1, 'pce'))[0];

print("Adding a PCC group on the top of PCE\n");
$ixNet->add($pce, 'pccGroup');
$ixNet->commit();
my $pccGroup = ($ixNet->getList($pce, 'pccGroup'))[0];

# Adding PCC with expectedPceInitiatedLspPerPcc 1
print("Adding a PCC object on the Topology 2\n");
$ixNet->add($ip2, 'pcc');
$ixNet->commit();
my $pcc = ($ixNet->getList($ip2, 'pcc'))[0];

# Set expectedInitiatedLspsForTraffic in pcc
$ixNet->setMultiAttribute($pcc, '-expectedInitiatedLspsForTraffic',  '1');
$ixNet->commit();

# Set pcc group multiplier to 1
$ixNet->setAttribute($pccGroup, '-multiplier',  '1');
$ixNet->commit();

# Set pcc multiplier to 1
$ixNet->setAttribute($pcc, '-multiplier',  '1');
$ixNet->commit();

# Set PCC group's  "PCC IPv4 Address" field  to 20.20.20.1
my $pccIpv4AddressMv = $ixNet->getAttribute($pccGroup, '-pccIpv4Address');
$ixNet->setAttribute($pccIpv4AddressMv.'/singleValue', '-value',  '20.20.20.1');
$ixNet->commit();

#Configuring PCE Initiated LSP parameters
my $ipVerisionMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters', '-ipVersion');
$ixNet->setAttribute($ipVerisionMv.'/singleValue', '-value', 'ipv4');
$ixNet->commit();

my $Ipv4SrcEndpointsMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters', '-srcEndPointIpv4');
$ixNet->setAttribute($Ipv4SrcEndpointsMv.'/singleValue', '-value', '2.0.0.1');

my $Ipv4DestEndpointsMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters', '-destEndPointIpv4');
$ixNet->setAttribute($Ipv4DestEndpointsMv.'/singleValue', '-value', '3.0.0.1');
$ixNet->commit();

################################################################################
# Set  pceInitiateLspParameters                                                #
# a. Include srp,lsp                                                           #
# b. Include symbolic pathname TLV                                             #
# c. Symbolic path name                                                        #
################################################################################

# Include srp
my $Ipv4SrpEndpointsMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters', '-includeSrp');
$ixNet->setAttribute($Ipv4SrpEndpointsMv.'/singleValue',  '-value',  'True');
$ixNet->commit();

# Include lsp
my $includeLspMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters', '-includeLsp');
$ixNet->setAttribute($includeLspMv.'/singleValue',  '-value',  'True');
$ixNet->commit();

my $includeSymbolicPathMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters', '-includeSymbolicPathNameTlv');
$ixNet->setAttribute($includeSymbolicPathMv.'/singleValue',  '-value',  'True');
$ixNet->commit();    
    
my $symbolicPathNameMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters', '-symbolicPathName');
$ixNet->setAttribute($symbolicPathNameMv.'/singleValue',  '-value', 'IXIA_SAMPLE_LSP_1');
$ixNet->commit();

# Add 2 EROs
$ixNet->setMultiAttribute($pccGroup.'/pceInitiateLspParameters', '-numberOfEroSubObjects', '2');
$ixNet->commit();

################################################################################
# Set the properties of ERO1                                                   # 
# a. Active                                                                    #
# b. Sid Type                                                                  #
# c. MPLS Label                                                                #
# d. TC                                                                        #
# e. TTL                                                                       #
# f. NAI Type                                                                  #
################################################################################
my $ero1ActiveMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters/pcepEroSubObjectsList:1', '-active');
$ixNet->setAttribute($ero1ActiveMv.'/singleValue', '-value', 'True');

my $ero1SidTypeMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters/pcepEroSubObjectsList:1', '-sidType');
$ixNet->setAttribute($ero1SidTypeMv.'/singleValue', '-value',  'mplslabel32bit');

my $ero1MplsLabelMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters/pcepEroSubObjectsList:1', '-mplsLabel');
$ixNet->setAttribute($ero1MplsLabelMv.'/singleValue', '-value', '1111');

my $ero1TcMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters/pcepEroSubObjectsList:1', '-tc');
$ixNet->setAttribute($ero1TcMv.'/singleValue', '-value',  '1'); 

my $ero1TtlMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters/pcepEroSubObjectsList:1', '-ttl');
$ixNet->setAttribute($ero1TtlMv.'/singleValue', '-value', '125');

my $ero1NaiTypeMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters/pcepEroSubObjectsList:1', '-naiType');
$ixNet->setAttribute($ero1NaiTypeMv.'/singleValue', '-value', 'notapplicable');
$ixNet->commit();

################################################################################
# Set the properties of ERO2                                                   #
# a. Active                                                                    #
# b. Sid Type                                                                  #
# c. MPLS Label                                                                #
# d. TC                                                                        #
# e. TTL                                                                       #
# f. NAI Type                                                                  #
################################################################################
my $ero2ActiveMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters/pcepEroSubObjectsList:2', '-active');
$ixNet->setAttribute($ero2ActiveMv.'/singleValue', '-value', 'True');

my $ero2SidTypeMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters/pcepEroSubObjectsList:2', '-sidType');
$ixNet->setAttribute($ero2SidTypeMv.'/singleValue', '-value', 'mplslabel32bit');

my $ero2MplsLabelMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters/pcepEroSubObjectsList:2', '-mplsLabel');
$ixNet->setAttribute($ero2MplsLabelMv.'/singleValue', '-value', '5555');

my $ero2TcMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters/pcepEroSubObjectsList:2', '-tc');
$ixNet->setAttribute($ero2TcMv.'/singleValue', '-value', '0');

my $ero2TtlMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters/pcepEroSubObjectsList:2', '-ttl');
$ixNet->setAttribute($ero2TtlMv.'/singleValue', '-value', '100');

my $ero2NaiTypeMv = $ixNet->getAttribute($pccGroup.'/pceInitiateLspParameters/pcepEroSubObjectsList:2', '-naiType');
$ixNet->setAttribute($ero2NaiTypeMv.'/singleValue', '-value', 'notapplicable');
$ixNet->commit();

# Set PCC's  "PCE IPv4 Address" field  to 20.20.20.2
my $pceIpv4AddressMv = $ixNet->getAttribute($pcc, '-pceIpv4Address');
$ixNet->setAttribute($pceIpv4AddressMv.'/singleValue', '-value', '20.20.20.2');
$ixNet->commit();

# Configure MaxExpectedSegmentCount in expectedInitiatedLspList
$ixNet->setMultiAttribute($pcc.'/expectedInitiatedLspList','-maxExpectedSegmentCount',  '2');
$ixNet->commit();

################################################################################
# Add expected PCC's Expected Initiated LSP traffic end point                  # 
# a. Active                                                                    #
# b. Source IP addresses                                                       #
# c. Symbolic path name                                                        #
################################################################################
my $pccExpectedLspActiveMv = $ixNet->getAttribute($pcc.'/expectedInitiatedLspList', '-active');
$ixNet->setAttribute($pccExpectedLspActiveMv.'/singleValue', '-value', 'True');
$ixNet->commit();

my $pccExpectedSrcIpAddrMv = $ixNet->getAttribute($pcc.'/expectedInitiatedLspList', '-sourceIpv4Address');
$ixNet->setAttribute($pccExpectedSrcIpAddrMv.'/singleValue', '-value',  '2.0.0.1');
$ixNet->commit();

my $pccExpectedSymbolicPathMv = $ixNet->getAttribute($pcc.'/expectedInitiatedLspList', '-symbolicPathName');
$ixNet->setAttribute($pccExpectedSymbolicPathMv.'/singleValue', '-value', '{IXIA_SAMPLE_LSP_1}');
$ixNet->commit();

################################################################################
# 2. # 2. Start PCEP protocol and wait for 60 seconds  
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);

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

###############################################################################
# 4. Retrieve protocol learned info
###############################################################################
print("Fetching PCC Learned Info\n");
$ixNet->execute('getPccLearnedInfo', $pcc, '1');
sleep(5);
my $linfo  = ($ixNet->getList($pcc, 'learnedInfo'))[0];
my @values = $ixNet->getAttribute($linfo, '-values');
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
# 5. Configure L2-L3 traffic 
################################################################################
print("Congfiguring L2-L3 Traffic Item\n");
$ixNet->setAttribute($ixNet->getRoot().'/traffic', '-refreshLearnedInfoBeforeApply', 'true');
$ixNet->commit();
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ipv4');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source       = ($pcc.'/expectedInitiatedLspList');
my @destination  = ($topo1);

$ixNet->setMultiAttribute($endpointSet1,
    '-name',                  'EndpointSet-1',
    '-sources',               @source,
    '-destinations',          @destination);
$ixNet->commit();

$ixNet->setMultiAttribute($trafficItem1.'/transmissionDistribution', '-distributions', ['mplsMplsLabelValue0']);

$ixNet->setMultiAttribute($trafficItem1.'/tracking',
    '-trackBy',        ['mplsFlowDescriptor0','mplsMplsLabelValue0','trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();

###############################################################################
# 6. Apply and start L2/L3 traffic
###############################################################################
print("Applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("Starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

print("Let the traffic run for 1 minute");
sleep(60);

print("***************************************************\n");
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
            printf(" %-30s:%s\n", $statcap[$index], $statIndiv);
            $index++;
        }
    }    
}
print("***************************************************\n");

#################################################################################
# 8. Stop L2/L3 traffic
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

#################################################################################
# 9. Change MPLS label value in the ERO1 of LSP1   in   pceInitiateLspParameters#
#################################################################################
$ixNet->setAttribute($ero1MplsLabelMv.'/singleValue', '-value', '6666');
$ixNet->commit();
my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);

###############################################################################
# 10. Retrieve protocol learned info
###############################################################################
print("Fetching PCC Learned Info\n");
$ixNet->execute('getPccLearnedInfo', $pcc, '1');
sleep(5);
my $linfo  = ($ixNet->getList($pcc, 'learnedInfo'))[0];
my @values = $ixNet->getAttribute($linfo, '-values');
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

###############################################################################
# 11. Apply and start L2/L3 traffic
###############################################################################
print("Applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("Starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

print("Let the traffic run for 1 minute");
sleep(60);

###############################################################################
# 12. Retrieve L2/L3 traffic item statistics
###############################################################################
print("Displaying all the L2-L3 traffic stats\n");
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
# 13. Stop L2/L3 traffic
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# 14. Stop all protocols
################################################################################
print("Stopping All Protocols\n");
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!");

