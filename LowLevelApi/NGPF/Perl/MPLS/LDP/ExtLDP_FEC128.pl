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


######################################################################################
#                                                                                    #
# Description:                                                                       #
#    This script intends to demonstrate how to use NGPF LDP API.                     #
#                                                                                    #
# About Topology:							                                         #
#         Within topology both Provider Edge(PE) and Provider(P) Routers are created.#
# created.P router is emulated in the front Device Group(DG), which consists of both #
# OSPF as routing protocol as well as Basic LDP sessions for Transport Label         #
# Distribution Protocol. The chained DG act as PE Router, where LDP Extended Martini #
# is configured for VPN Label distribution protocol.Bidirectional L2-L3 Traffic is   #
# configured in between two CE cloud.                                                #
#	 Script Flow:			                                                         #
#	 1. Configuration of protocols.	                                                 #
#    Configuration flow of the script is as follow:                                  #
# 		i.    Adding of OSPF router.			        	                         #
# 		ii.   Adding of Network Cloud.      				                         #
# 		iii.  Adding of chain DG.					                                 #
# 		iv.   Adding of LDP(basic session) on Front DG 		                         #
# 		v.    Adding of LDP Extended Martini(Targeted sess.) over chained DG.        #
# 		vi.   Adding of LDP PW/VPLS Tunnel over LDP Extended Martini.	             #
#    2. Start the ldp protocol.                                                      #
#    3. Retrieve protocol statistics.                                         	     #
#    4. Retrieve protocol learned info.                                              #
#    5. Disable/Enable the ldp FECs and change label & apply change on the fly       #
#    6. Retrieve protocol learned info again and notice the difference with          #
#       previously retrieved learned info.                                           #
#    7. Configure L2-L3 traffic.                                                     #
#    8. Start the L2-L3 traffic.                                                     #
#    9. Retrieve L2-L3 traffic stats.                                                #
#   10. Stop L2-L3 traffic.                                                          #
#   11. Stop all protocols.                                                          #
#                                                                                    #
######################################################################################

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
my $ixTclServer = '10.216.108.49';
my $ixTclPort   = '8999';
my @ports       = (('10.216.102.209', '1', '3'), ('10.216.102.209', '1', '4'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '7.50',
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

print ("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'Topology for FEC128 1');
$ixNet->setAttribute($topo2, '-name', 'Topology for FEC128 2');

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

#print("\$ixNet->help ::ixNet::OBJ-/topology/deviceGroup/ethernet\n");
#print($ixNet->help('::ixNet::OBJ-/topology/deviceGroup/ethernet'));
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

#print("\$ixNet->help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4\n");
#print($ixNet->help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4'));
print("Adding LDP over IP4 stacks\n");
$ixNet->add($ip1, 'ldpBasicRouter');
$ixNet->add($ip2, 'ldpBasicRouter');
$ixNet->commit();

my $ldp1 = ($ixNet->getList($ip1, 'ldpBasicRouter'))[0];
my $ldp2 = ($ixNet->getList($ip2, 'ldpBasicRouter'))[0];

print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($t1dev1, '-name', 'Provider Router 1');
$ixNet->setAttribute($t2dev1, '-name', 'Provider Router 2');
$ixNet->commit();

#print ("$ixNet->help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp\n");
#print ($ixNet->help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ldp'));

print ("Adding OSPFv2 over IP4 stack\n");
$ixNet->add($ip1, 'ospfv2');
$ixNet->add($ip2, 'ospfv2');
$ixNet->commit();
my $ospf1 = ($ixNet->getList($ip1, 'ospfv2'))[0];
my $ospf2 = ($ixNet->getList($ip2, 'ospfv2'))[0];
print ("Making the NetworkType to Point to Point in the first OSPF router\n");
my $networkTypeMultiValue1 = $ixNet->getAttribute($ospf1, '-networkType');
$ixNet->setAttribute($networkTypeMultiValue1, '-clearOverlays', 'false', '-pattern', 'singleValue');
$ixNet->commit();
my $networkType1 =$ixNet->add($networkTypeMultiValue1, 'singleValue');
$ixNet->setMultiAttribute($networkType1, '-value', 'pointtopoint');
$ixNet->commit();

print ("Making the NetworkType to Point to Point in the second OSPF router\n");
my $networkTypeMultiValue2 = $ixNet->getAttribute($ospf2, '-networkType');
$ixNet->setAttribute($networkTypeMultiValue2, '-clearOverlays', 'false', '-pattern', 'singleValue');
$ixNet->commit();
my $networkType2 =$ixNet->add($networkTypeMultiValue2, 'singleValue'); 
$ixNet->setMultiAttribute($networkType2, '-value', 'pointtopoint');
$ixNet->commit();

# **********************************************************************************
print("Adding NetworkGroup behind LDP DG\n");
$ixNet->execute('createDefaultStack', $t1dev1, 'ipv4PrefixPools');
$ixNet->execute('createDefaultStack', $t2dev1, 'ipv4PrefixPools');

my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
my $networkGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];

$ixNet->setAttribute($networkGroup1, '-name', 'LDP_1_Network_Group1');
$ixNet->setAttribute($networkGroup2, '-name', 'LDP_2_Network_Group1');
$ixNet->setAttribute($networkGroup1, '-multiplier', '10');
$ixNet->setAttribute($networkGroup2, '-multiplier', '10');
$ixNet->commit();

#Change IP address and Prefix Of Network Group 
my $ipV4PrefixPools1  = ($ixNet->getList($networkGroup1, 'ipv4PrefixPools'))[0];
my $prefixLength1 = $ixNet->getAttribute($ipV4PrefixPools1, '-prefixLength');
$ixNet->setMultiAttribute($prefixLength1, '-clearOverlays', 'false', '-pattern', 'singleValue');
$ixNet->commit();
my $ipV4PrefixPools2  = ($ixNet->getList($networkGroup2, 'ipv4PrefixPools'))[0];
my $prefixLength2 = $ixNet->getAttribute($ipV4PrefixPools2, '-prefixLength');
$ixNet->setMultiAttribute($prefixLength2,  '-clearOverlays', 'false', '-pattern', 'singleValue');
$ixNet->commit();

my $prefix1 = $ixNet->add($prefixLength1, 'singleValue');
$ixNet->setMultiAttribute($prefix1, '-value', '32');
$ixNet->commit();
my $prefix2 = $ixNet->add($prefixLength2, 'singleValue');
$ixNet->setMultiAttribute($prefix2, '-value', '32');
$ixNet->commit();
my $addressSet1 = $ixNet->getAttribute($ipV4PrefixPools1, '-networkAddress');
$ixNet->setMultiAttribute($addressSet1, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();
my $addressSet2 = $ixNet->getAttribute($ipV4PrefixPools2, '-networkAddress');
$ixNet->setMultiAttribute($addressSet2, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();
print("changing Ip and Prefix Of Network group\n");
my $addressSet1 = $ixNet->add($addressSet1, 'counter');
$ixNet->setMultiAttribute($addressSet1, '-step', '0.0.0.1', '-start', '200.1.0.1', '-direction', 'increment');
$ixNet->commit();
my $addressSet2 = $ixNet->add($addressSet2, 'counter');
$ixNet->setMultiAttribute($addressSet2, '-step', '0.0.0.1', '-start', '201.1.0.1', '-direction', 'increment');
$ixNet->commit();


# Add ipv4 loopback1 for PE Router
print("Adding ipv4 loopback1  for configuring PE Routers above it\n");
my $chainedDg1 = $ixNet->add($networkGroup1, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg1, '-multiplier', '1', '-name', 'Device Group 3');
$ixNet->commit();
$chainedDg1 = ($ixNet->remapIds($chainedDg1))[0];

my $loopback1 = $ixNet->add($chainedDg1, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback1, '-stackedLayers', '', '-name', 'IPv4 Loopback 2');
$ixNet->commit();

my $connector1 = $ixNet->add($loopback1, 'connector');
$ixNet->setMultiAttribute($connector1,
     '-connectedTo', $networkGroup1.'/ipv4PrefixPools:1');
$ixNet->commit();

my $connector1 = ($ixNet->remapIds($connector1))[0];

my $addressSet1 = $ixNet->getAttribute($loopback1, '-address');
$ixNet->setMultiAttribute($addressSet1, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$addressSet1 = $ixNet->add($addressSet1, 'counter');
$ixNet->setMultiAttribute($addressSet1, '-step', '0.0.0.1', '-start', '200.1.0.1', '-direction', 'increment');
$ixNet->commit();
my $addressSet1 = ($ixNet->remapIds($addressSet1))[0];

# Add ipv4 loopback2  for PE Router
print("Adding ipv4 loopback2 for configuring PE Routers above it\n");
my $chainedDg2 = $ixNet->add($networkGroup2, 'deviceGroup');
$ixNet->setMultiAttribute($chainedDg2, '-multiplier', '1', '-name', 'Device Group 4');
$ixNet->commit();
$chainedDg2 = ($ixNet->remapIds($chainedDg2))[0];

my $loopback2 = $ixNet->add($chainedDg2, 'ipv4Loopback');
$ixNet->setMultiAttribute($loopback2, '-stackedLayers', '', '-name', 'IPv4 Loopback 2');
$ixNet->commit();

my $connector2 = $ixNet->add($loopback2, 'connector');
$ixNet->setMultiAttribute($connector2, '-connectedTo',
    $networkGroup2.'/ipv4PrefixPools:1');
$ixNet->commit();
$connector2 = ($ixNet->remapIds($connector2))[0];

my $addressSet2 = $ixNet->getAttribute($loopback2, '-address');
$ixNet->setMultiAttribute($addressSet2, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

$addressSet2 = $ixNet->add($addressSet2, 'counter');
$ixNet->setMultiAttribute($addressSet2, '-step', '0.0.0.1', '-start', '201.1.0.1', '-direction', 'increment');
$ixNet->commit();
$addressSet2 = ($ixNet->remapIds($addressSet2))[0];
################################################################################
# 2. Add LDP targeted Router
################################################################################

$ixNet->add($loopback1, 'ldpTargetedRouter');
$ixNet->add($loopback2, 'ldpTargetedRouter');
$ixNet->commit();
my $ldpTargeted1 = ($ixNet->getList($loopback1, 'ldpTargetedRouter'))[0];
my $ldpTargeted2 = ($ixNet->getList($loopback2, 'ldpTargetedRouter'))[0];
my $ldpTargetedPeer1 = ($ixNet->getList($ldpTargeted1, 'ldpTargetedPeer'))[0];
my $ldpTargetedPeer2 = ($ixNet->getList($ldpTargeted2, 'ldpTargetedPeer'))[0];
#print ("\$ixNet->help ::ixNet::OBJ-/topology:1/deviceGroup:1/networkGroup:4/deviceGroup:1/ipv4Loopback:1/ldpTargetedRouter:1/ldpTargetedPeer\n");
#print ($ixNet->help('::ixNet::OBJ-/topology:2/deviceGroup:2/networkGroup:2/deviceGroup:1/ipv4Loopback:1/ldpTargetedRouter:1/ldpTargetedPeer'));
my $addressSet5 = $ixNet->getAttribute($ldpTargetedPeer1, '-iPAddress');
$ixNet->setMultiAttribute($addressSet5, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();
my $addressSet5 = $ixNet->add($addressSet5, 'counter');
$ixNet->setMultiAttribute($addressSet5, '-step', '0.0.0.1', '-start', '201.1.0.1', '-direction', 'increment');
$ixNet->commit();

my $addressSet6 = $ixNet->getAttribute($ldpTargetedPeer2, '-iPAddress');
$ixNet->setMultiAttribute($addressSet6, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();
my $addressSet6 = $ixNet->add($addressSet6, 'counter');
$ixNet->setMultiAttribute($addressSet6, '-step', '0.0.0.1', '-start', '200.1.0.1', '-direction', 'increment');
$ixNet->commit();

#Add LDP FEC129 on top of LDP targeted Router

my $ldppwvpls1 = $ixNet->add($ldpTargeted1, 'ldppwvpls');
my $ldppwvpls2 = $ixNet->add($ldpTargeted2, 'ldppwvpls');
$ixNet->commit();
#print ("\$ixNet->help ::ixNet::OBJ-/topology:1/deviceGroup:1/networkGroup:1/deviceGroup:1/ipv4Loopback:1/ldpTargetedRouter:1/ldppwvpls:1\n");
#print ($ixNet->help('::ixNet::OBJ-/topology:1/deviceGroup:1/networkGroup:1/deviceGroup:1/ipv4Loopback:1/ldpTargetedRouter:1/ldppwvpls:1'));

my $ldppwvpls1 = ($ixNet->remapIds($ldppwvpls1))[0];
my $ldppwvpls2 = ($ixNet->remapIds($ldppwvpls2))[0];

my $peerId1 = ($ixNet->getAttribute($ldppwvpls1, '-peerId'));
$ixNet->setMultiAttribute($peerId1, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

my $peerId1 = $ixNet->add($peerId1, 'counter');
$ixNet->setMultiAttribute($peerId1, '-step', '0.0.0.1',
    '-start', '201.1.0.1', '-direction', 'increment');
$ixNet->commit();
my $peerId2 = ($ixNet->getAttribute($ldppwvpls2, '-peerId'));
$ixNet->setMultiAttribute($peerId2, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

my $peerId2 = $ixNet->add($peerId2, 'counter');
$ixNet->setMultiAttribute($peerId2, '-step', '0.0.0.1',
    '-start', '200.1.0.1', '-direction', 'increment');
$ixNet->commit();
 
################################################################################
# 3. Add MAC Cloud behind LDP PWs
################################################################################
$ixNet->execute('createDefaultStack', $chainedDg1, 'macPools');
$ixNet->execute('createDefaultStack', $chainedDg2, 'macPools');
$ixNet->commit();

my $macPools1 = ($ixNet->getList($chainedDg1, 'networkGroup'))[0];
my $macPools2 = ($ixNet->getList($chainedDg2, 'networkGroup'))[0];
print("Renaming MAC Cloud\n");
$ixNet->setAttribute($macPools1, '-name', 'CE MAC Cloud 1');
$ixNet->setAttribute($macPools2, '-name', 'CE MAC Cloud 1');
$ixNet->commit();
###############################################################################
# 4. Start LDP protocol and wait for 60 seconds
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);

################################################################################
# 5. Retrieve protocol statistics.
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
		    printf(" %-34s:%s\n", $statcap[$index], $statIndiv);
			$index++;
        }
    }    
}
print("***************************************************\n");

###############################################################################
# 6. Retrieve protocol learned info
###############################################################################
print("Fetching LDP Basic Learned Info\n");
$ixNet->execute('getIPv4FECLearnedInfo', $ldp1, '1');
sleep(5);
my $linfo1  = ($ixNet->getList($ldp1, 'learnedInfo'))[0];
my @values1 = $ixNet->getAttribute($linfo1, '-values');
my $v      = '';
print("***************************************************\n");
foreach $v (@values1) {
 	my $w = '0';
	foreach $w (@$v) {
	    printf("%12s", $w);
	}
	print("\n");
}
print("***************************************************\n");

print ("Fetching FEC 128 Learned Info\n");
$ixNet->execute('getIPv4FECLearnedInfo', $ldpTargeted2, '1');
sleep(5);
my $linfo2  = ($ixNet->getList($ldpTargeted2, 'learnedInfo'))[0];
my @values2 = $ixNet->getAttribute($linfo2, '-values');
my $v      = '';
print("***************************************************\n");
foreach $v (@values2) {
 	my $w = '0';
	foreach $w (@$v) {
	    printf("%12s", $w);
	}
	print("\n");
}
print("***************************************************\n");

################################################################################
# 7. Change the labels of FEC element And apply changes On The Fly (OTF).
################################################################################
print ("Changing FEC labels on the fly\n ");
my $feclabel1 = $ixNet->getAttribute($ldppwvpls1, '-label');
$ixNet->setMultiAttribute($feclabel1, '-clearOverlays', 'false', '-pattern', 'counter');
$ixNet->commit();

my $feclabel1 = $ixNet->add($feclabel1, 'counter');
$ixNet->setMultiAttribute($feclabel1, '-step', '100', '-start', '5001', '-direction', 'increment');
$ixNet->commit();
my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(15);

###############################################################################
# 8. Retrieve protocol learned info again and compare with
#    previously retrieved learned info.  
###############################################################################
print("Fetching LDP Learned Info after changing Labels\n");
$ixNet->execute('getIPv4FECLearnedInfo', $ldp1, '1');
sleep(5);
my $linfo  = ($ixNet->getList($ldp1, 'learnedInfo'))[0];
my @values = $ixNet->getAttribute($linfo, '-values');
my $v      = '';
print("***************************************************\n");
foreach $v (@values) {
 	my $w = '0';
	foreach $w (@$v) {
	    printf("%12s", $w);
	}
	print("\n");
}
print("***************************************************\n");


################################################################################
# 9. Configure L2-L3 traffic 
################################################################################
print ("Congfiguring L2-L3 Traffic Item\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ethernetVlan');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source       = $networkGroup1;
my @destination  = $networkGroup2;

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
    '-trackBy',        ['sourceDestEndpointPair0','trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();

# puts "ixNet help [ixNet getRoot]/traffic"
# puts "[ixNet help [ixNet getRoot]/traffic]"

###############################################################################
# 10. Apply and start L2/L3 traffic
###############################################################################
print("applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'traffic');
print("Let traffic run for 1 minute\n");
sleep(60);
###############################################################################
# 11. Retrieve L2/L3 traffic item statistics
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
		    printf(" %-34s:%s\n", $statcap[$index], $statIndiv);
			$index++;
        }
    }    
}
print("***************************************************\n");

#################################################################################
# 12. Stop L2/L3 traffic
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# 13. Stop all protocols
################################################################################
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!");

