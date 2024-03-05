# -*- coding: cp1252 -*-
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
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF BGP EPE API            #
#    It will create 2 BGP EPE topologies, it will start the emulation and      #
#    than it will retrieve and display few statistics                          #
################################################################################

# edit this variables values to match your setup

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
my $ixTclServer = '10.39.43.12';
my $ixTclPort   = '8072';
my @ports       = (('10.39.37.45', '2', '1'), ('10.39.37.45', '2', '2'));
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

################################################################################
# protocol configuration section                                               #
################################################################################ 
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

my @t1devices = ($ixNet->getList($topo1, 'deviceGroup'));
my @t2devices = ($ixNet->getList($topo2, 'deviceGroup'));

my $t1devices = ($ixNet->getList($topo1, 'deviceGroup'));
my $t2devices = ($ixNet->getList($topo2, 'deviceGroup'));

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

print("configuring ipv4 addresses \n");
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '20.20.20.2');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', "20.20.20.2");

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '24');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '24');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

print("Adding BGP over IP4 stacks \n");
$ixNet->add($ip1, 'bgpIpv4Peer');
$ixNet->add($ip2, 'bgpIpv4Peer');
$ixNet->commit();

my $bgp1 = ($ixNet->getList($ip1, 'bgpIpv4Peer'))[0];
my $bgp2 = ($ixNet->getList($ip2, 'bgpIpv4Peer'))[0];

print("Setting IPs in BGP DUT IP tab\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-dutIp').'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-dutIp').'/singleValue', '-value', '20.20.20.2');
$ixNet->commit();

print ("Enabling BGP Link State Non-VPN Capability\n");
my $cap1 = $ixNet->getAttribute($bgp1, '-capabilityLinkStateNonVpn');
my $cap2 = $ixNet->getAttribute($bgp2, '-capabilityLinkStateNonVpn');
my $sv1 = ($ixNet->getList($cap1, 'singleValue'))[0];
my $sv2 = ($ixNet->getList($cap2, 'singleValue'))[0];
$ixNet->setAttribute($sv1, '-value', 'true');
$ixNet->setAttribute($sv2, '-value', 'true');

print ("Enabling BGP Filter Link State\n");
my $filter1 = $ixNet->getAttribute($bgp1, '-filterLinkState');
my $filter2 = $ixNet->getAttribute($bgp2, '-filterLinkState');
my $sv1 = ($ixNet->getList($filter1, 'singleValue'))[0];
my $sv2 = ($ixNet->getList($filter2, 'singleValue'))[0];
$ixNet->setAttribute($sv1, '-value', 'true');
$ixNet->setAttribute($sv2, '-value', 'true');

print ("Enable BGP EPE in Topology 1\n");
$ixNet->setAttribute($bgp1, '-noOfEpePeers', '3');
$ixNet->commit();

my $bgpEpePeerList = ($ixNet->getList($bgp1, 'bgpEpePeerList'))[0];
my $bgpEpePeerLinkList = ($ixNet->getList($bgpEpePeerList, 'bgpEpePeerLinkList'))[0];
$ixNet->commit();

print ("Setting Number of Links for BGP EPE to 2 in Topology 1\n");
$ixNet->setAttribute($bgpEpePeerList, '-noOflinks', '2');
$ixNet->commit();

print ("Setting Number of EPE Peer Set to 3 in Topology 1\n");
$ixNet->setAttribute($bgpEpePeerList, '-noOfPeerSet', '2');
$ixNet->commit();

print ("Selection of Peer Set Group\n");
my $peerSetGroup = ($ixNet->getAttribute($bgpEpePeerList, '-peerSetGroup'));
$ixNet->setMultiAttribute($peerSetGroup, '-clearOverlays', 'true');
my $activeOverlay = $ixNet->add($peerSetGroup, 'overlay');
my $activeOverlay = $ixNet->add($peerSetGroup, 'singleValue');
$ixNet->setMultiAttribute($activeOverlay, '-value', 'peersetgroup1 peersetgroup2');
$ixNet->commit();


print ("Setting BGP Remote Router ID as DUT IP of BGP Peer\n");
$ixNet->setAttribute($ixNet->getAttribute($bgpEpePeerList, '-bgpRemoteRouterId').'/singleValue', '-value', '20.20.20.1');
$ixNet->commit();

print ("Setting EPE Peer Links Peer-Adj-SID to True\n");
$ixNet->setAttribute($ixNet->getAttribute($bgpEpePeerLinkList, '-enablePeerAdjSid').'/singleValue', '-value', 'true');
$ixNet->commit();

print ("Setting EPE Peer Links Remote IPv4 Link Address");
$ixNet->setAttribute($ixNet->getAttribute($bgpEpePeerLinkList, '-remoteIpv4LinkAddress').'/singleValue', '-value', '20.20.20.1');
$ixNet->commit();

my $bgpLocalIp = $ixNet->getAttribute($bgp1, '-localIpv4Ver2');

print ("Setting EPE Peer Links Local IPv4 Link Address\n");
$ixNet->setAttribute($ixNet->getAttribute($bgpEpePeerLinkList, '-localIpv4LinkAddress').'/singleValue', '-value', $ixNet->getAttribute($bgp1, '-localIpv4Ver2'));
$ixNet->commit();

print("Adding OSPFv2 over IP4 stack\n");
my $ospf1 = ($ixNet->add($ip1, 'ospfv2'));
my $ospf2 = ($ixNet->add($ip2, 'ospfv2'));
$ixNet->commit();

print("Changing OSPFv2 Network Type \n");
my $networkTypeMultiValue1 = $ixNet->getAttribute($ospf1, '-networkType');
$ixNet->setAttribute($networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'false');
$ixNet->setAttribute($networkTypeMultiValue1.'/singleValue', '-value', 'pointtopoint');

my $networkTypeMultiValue2 = $ixNet->getAttribute($ospf2, '-networkType');
$ixNet->setAttribute($networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'false');
$ixNet->setAttribute($networkTypeMultiValue2.'/singleValue', '-value', 'pointtopoint');

print("Renaming the topologies and the device groups \n");
$ixNet->setAttribute($topo1,  '-name', 'BGP Topology 1');
$ixNet->setAttribute($topo2,  '-name', 'BGP Topology 2');

$ixNet->setAttribute($t1dev1, '-name', 'BGP Topology 1 Router');
$ixNet->setAttribute($t2dev1, '-name', 'BGP Topology 2 Router');
$ixNet->commit();

################################################################################
# Start protocol and check statistics                                          #
################################################################################
print("Starting protocols and waiting for 45 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(45);

print("***************************************************");

print("Verifying BGP Peer related stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"BGP Peer Per Port"/page';
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
# print learned info                                                          #
###############################################################################
$ixNet->execute('getLinkStateLearnedInfo', $bgp2, '1');
sleep(45);

print("Print BGP-LS EPE Learned Info \n");
my $learnedInfoList = ($ixNet->getList($bgp2, 'learnedInfo'))[0];
my $learnedInfo = ($learnedInfoList, 'end')[0];
my $table = ($ixNet->getList($learnedInfo, 'table'))[3];
my @learnedInfoColumnsList = ($ixNet->getAttribute($table, '-columns'));
my @learnedInfoValuesList = ($ixNet->getAttribute($table, '-values'));
my @row2 = (@learnedInfoValuesList) [1];
print("@learnedInfoColumnsList\n");
my $v      = '';
print("***************************************************\n");
foreach $v (@row2) {
    my $w = '0';
    foreach $w (@$v) {
        printf("%10s", $w);
    }
    print("\n");
}
print("***************************************************\n");

sleep(15);

print ('Stopping protocols');
$ixNet->execute('stopAllProtocols');

print ('!!! Test Script Ends !!!')
