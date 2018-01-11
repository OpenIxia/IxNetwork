################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           # 
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    11/17/2016 - Rupam Paul - created sample                                  #
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
#    This script intends to demonstrate how to use NGPF IPv6 SR Low Level      #
#    Perl API.                                                                 #
#                                                                              #
#    1. It will create 2 ISIS topologies, topology2 will have                  #
#       IPv6 prefix pool & Simulated Topology.                                 #
#    2. Enable SR and SR IPv6 in ISIS Emulated Router.                         #
#    3. Set IPv6 Node Prefix & IPv6 Adj-Sid.                                   #
#    4. Enable Segment Routing in Simulated Router and                         #
#       Set IPv6 Node Prefix & IPv6 Adj-Sid in Simulated Router.               #  
#    5. Start protocol.                                                        #
#    6. Retrieve protocol statistics.                                          #
#    7. Retrieve protocol learned info in Port1.                               #
#    8. On the fly disable Adj-Sid in simulated interface.                     #
#    9. Retrieve protocol learned info in Port1 after On the Fly change.       #
#    10. Stop all protocols.                                                   #
#                                                                              #
# Ixia Softwares:                                                              #
#    IxOS      8.20 EA                                                         #
#    IxNetwork 8.20 EA                                                         #
#                                                                              #
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
my $ixTclServer = '10.216.104.58';
my $ixTclPort   = '5555';
my @ports       = (('10.216.108.99', '11', '3'), ('10.216.108.99', '11', '4'));
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

print("Add ipv6\n");
$ixNet->add($mac1, 'ipv6');
$ixNet->add($mac2, 'ipv6');
$ixNet->commit();

my $ip1 = ($ixNet->getList($mac1, 'ipv6'))[0];
my $ip2 = ($ixNet->getList($mac2, 'ipv6'))[0];

my $mvAdd1 = ($ixNet->getAttribute($ip1, '-address'));
my $mvAdd2 = ($ixNet->getAttribute($ip2, '-address'));
my $mvGw1 = ($ixNet->getAttribute($ip1, '-gatewayIp'));
my $mvGw2 = ($ixNet->getAttribute($ip2, '-gatewayIp'));

print("Configuring ipv6 addresses\n");
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '2000::1');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '2000::101');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '2000::101');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', '2000::1');

print("Configuring the mac addresses\n");
$ixNet->setMultiAttribute($ixNet->getAttribute($mac1, '-mac').'/counter',
        '-direction', 'increment',
        '-start',     '18:03:73:C7:6C:B1',
        '-step',      '00:00:00:00:00:01');

$ixNet->setAttribute($ixNet->getAttribute($mac2, '-mac').'/singleValue',
        '-value', '18:03:73:C7:6C:01');
$ixNet->commit();

print("Add ISISL3\n");
$ixNet->add($mac1, 'isisL3');
$ixNet->add($mac2, 'isisL3');
$ixNet->commit();

my $isisL3_1 = ($ixNet->getList($mac1, 'isisL3'))[0];
my $isisL3_2 = ($ixNet->getList($mac2, 'isisL3'))[0];

print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'ISIS Topology 1');
$ixNet->setAttribute($topo2, '-name', 'ISIS Topology 2');

$ixNet->setAttribute($t1dev1, '-name', 'ISIS Topology 1 Router');
$ixNet->setAttribute($t2dev1, '-name', 'ISIS Topology 2 Router');
$ixNet->commit();

my $isisL3Router1_1 = ($ixNet->getList($t1dev1, 'isisL3Router'));
my $isisL3Router2_1 = ($ixNet->getList($t2dev1, 'isisL3Router'));

# Enable host name in ISIS routers
print("Enabling Host name in Emulated ISIS Routers\n");
my $deviceGroup1 = ($ixNet->getList($topo1, 'deviceGroup'))[0];
my $isisL3Router1 = ($ixNet->getList($deviceGroup1, 'isisL3Router'))[0];
my $enableHostName1 = ($ixNet->getAttribute($isisL3Router1, '-enableHostName'));
$ixNet->setAttribute($enableHostName1.'/singleValue', '-value', 'True');
$ixNet->commit();
my $configureHostName1 = $ixNet->getAttribute($isisL3Router1, '-hostName');
$ixNet->setAttribute($configureHostName1.'/singleValue', '-value', 'isisL3Router1');
$ixNet->commit();
# Enable host name in ISIS router2
my $deviceGroup2 = ($ixNet->getList($topo2, 'deviceGroup'))[0];
my $isisL3Router2 = ($ixNet->getList($deviceGroup2, 'isisL3Router'))[0];
my $enableHostName2 = ($ixNet->getAttribute($isisL3Router2, '-enableHostName'));
$ixNet->setAttribute($enableHostName2.'/singleValue', '-value', 'True');
$ixNet->commit();
my $configureHostName2 = ($ixNet->getAttribute($isisL3Router2, '-hostName'));
$ixNet->setAttribute($configureHostName2.'/singleValue', '-value', 'isisL3Router2');
$ixNet->commit();

# Disable Discard Learned LSP
print("Disabling the Discard Learned Info CheckBox\n");
my $isisL3RouterDiscardLearnedLSP1 = $ixNet->getAttribute(($ixNet->getList($t1devices[0], 'isisL3Router'))[0],
    '-discardLSPs');

my $isisL3RouterDiscardLearnedLSP2 = $ixNet->getAttribute(($ixNet->getList($t2devices[0], 'isisL3Router'))[0],
    '-discardLSPs');

$ixNet->setAttribute($isisL3RouterDiscardLearnedLSP1,
     '-pattern', 'singleValue',
	 '-clearOverlays', 'False');
$ixNet->setAttribute($isisL3RouterDiscardLearnedLSP1.'/singleValue', '-value', 'false');

$ixNet->setAttribute($isisL3RouterDiscardLearnedLSP2,
    '-pattern', 'singleValue',
	'-clearOverlays', 'False');
$ixNet->setAttribute($isisL3RouterDiscardLearnedLSP2.'/singleValue', '-value', 'false');

print('$ixNet->help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2\')\n');
$ixNet->commit();


################################################################################
# Enabling Segment Routing in Emulated Router
################################################################################

print("Enabling Segment Routing for ISIS\n");
$ixNet->setAttribute($isisL3Router1, '-enableSR', 'true');
$ixNet->setAttribute($isisL3Router2, '-enableSR', 'true');
$ixNet->commit();

################################################################################
# Enabling SR-IPv6 Flag under Segnment Routing Tab in ISIS-L3 RTR
################################################################################
print("Enabling SR-IPv6 Flag under Segment Routing Tab\n");

my $sr_ipv6_flag1 = ($ixNet->getAttribute($isisL3Router1, '-ipv6Srh'));
$ixNet->setAttribute($sr_ipv6_flag1.'/singleValue', '-value', 'True');
$ixNet->commit();

my $sr_ipv6_flag2 = ($ixNet->getAttribute($isisL3Router2, '-ipv6Srh'));
$ixNet->setAttribute($sr_ipv6_flag2.'/singleValue', '-value', 'True');
$ixNet->commit();


################################################################################
# Setting IPv6 Node Prefix Address
################################################################################
print("Setting IPv6 Node Prefix Address\n");

my $ipv6_node_prefix_add1 = ($ixNet->getAttribute($isisL3Router1, '-ipv6NodePrefix'));
$ixNet->setAttribute($ipv6_node_prefix_add1.'/singleValue', '-value', '3000::1');
$ixNet->commit();

my $ipv6_node_prefix_add2 = ($ixNet->getAttribute($isisL3Router2, '-ipv6NodePrefix'));
$ixNet->setAttribute($ipv6_node_prefix_add2.'/singleValue', '-value', '4000::101');
$ixNet->commit();


################################################################################
# Enabling Adj-Sid under Segnment Routing Tab in ISIS-L3 IF
################################################################################

print("Enabling Adj-SID in first Emulated Router\n");

my $enableAdjSID1 = ($ixNet->getAttribute($isisL3_1, '-enableAdjSID'));
$ixNet->setAttribute($enableAdjSID1.'/singleValue', '-value', 'True');
$ixNet->commit();

print("Enabling Adj-SID in second Emulated Router\n");

my $enableAdjSID2 = ($ixNet->getAttribute($isisL3_2, '-enableAdjSID'));
$ixNet->setAttribute($enableAdjSID2.'/singleValue', '-value', 'True');
$ixNet->commit();

print("Set IPv6 Adj-SID value in first Emulated Router\n");

my $ipv6SidValue1 = ($ixNet->getAttribute($isisL3_1, '-ipv6SidValue'));
$ixNet->setAttribute($ipv6SidValue1.'/singleValue', '-value', '5000::1');
$ixNet->commit();


print("Set IPv6 Adj-SID value in second Emulated Router\n");

my $ipv6SidValue2 = ($ixNet->getAttribute($isisL3_2, '-ipv6SidValue'));
$ixNet->setAttribute($ipv6SidValue2.'/singleValue', '-value', '6000::1');
$ixNet->commit();

print("Adding Network Group behind ISIS Device Group2\n");
$ixNet->execute('createDefaultStack', $t2dev1, 'networkTopology');
my $networkGroup1 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];
my $networkGroup2 = ($ixNet->add($t2dev1, 'networkGroup'))[0];

$ixNet->setAttribute($networkGroup1, '-name', 'ISIS_1_Network_Group1');
$ixNet->setAttribute($networkGroup2, '-name', 'ISIS_2_Network_Group1');
$ixNet->commit();

print("Adding IPv6 Prefix Pool behind ISIS Device Group2\n");
my $ipv6PrefixPools = ($ixNet->add($networkGroup2, 'ipv6PrefixPools'))[0];
$ixNet->setAttribute($networkGroup2, '-multiplier', '1');
$ixNet->commit();

$ixNet->setAttribute($networkGroup2, '-name', 'ISIS_IPv6_Prefix_Pools');
$ixNet->commit();

print("Enabling Advertise IPv6 SID under IPv6 PrefixPool\n");
my $isisL3RouteProperty = ($ixNet->add($ipv6PrefixPools, 'isisL3RouteProperty'));
my $ipv6Srh = ($ixNet->getAttribute($isisL3RouteProperty, '-ipv6Srh'));
$ixNet->setAttribute($ipv6Srh.'/singleValue', '-value', 'True');
$ixNet->commit();


################################################################################
# Enabling Segment Routing in simulated router
################################################################################
print("Enabling Segment Routing in Simulated Routers on Network Group behind Device Group2\n");
my $networkTopo1 = ($ixNet->getList($networkGroup1, 'networkTopology'))[0];
my $simRouter1 = ($ixNet->getList($networkTopo1, 'simRouter'))[0];
my $isisPseudoRouter1 = ($ixNet->getList($simRouter1, 'isisL3PseudoRouter'))[0];
$ixNet->setAttribute($isisPseudoRouter1, '-enableSR', 'true');
print("Enabling Segment4\n");
$ixNet->commit();

print("Enabling SR-IPv6 Flag in Simulated Routers on Network Group behind Device Group2\n");
my $sr_ipv6_flag1 = ($ixNet->getAttribute($isisPseudoRouter1, '-ipv6Srh'))[0];
$ixNet->setAttribute($sr_ipv6_flag1.'/singleValue', '-value', 'True');
$ixNet->commit();

print("Setting IPv6 Node Prefix Address in Simulated Routers on Network Group behind Device Group2\n");
my $ipv6_node_prefix_add1 = ($ixNet->getAttribute($isisPseudoRouter1, '-ipv6NodePrefix'))[0];
$ixNet->setAttribute($ipv6_node_prefix_add1.'/singleValue', '-value', '7000::1');
$ixNet->commit();

print("Enabling Adj-Sid in Simulated Interface on Network Group behind Device Group2\n");
my $networkTopo1 = ($ixNet->getList($networkGroup1, 'networkTopology'))[0];
my $simInterface1 = ($ixNet->getList($networkTopo1, 'simInterface'))[0];
my $isisL3PseudoInterface1 = ($ixNet->getList($simInterface1, 'isisL3PseudoInterface'))[0];
my $adj_sid = ($ixNet->getAttribute($isisL3PseudoInterface1, '-enableAdjSID'))[0];
$ixNet->setAttribute($adj_sid.'/singleValue', '-value', 'True');
$ixNet->commit();


print("Set IPv6 Adj-SID value for Simulated Interface\n");
my $ipv6SidValue1 = ($ixNet->getAttribute($isisL3PseudoInterface1, '-ipv6SidValue'))[0];
$ixNet->setAttribute($ipv6SidValue1.'/singleValue', '-value', '8000::1');
$ixNet->commit();


################################################################################
#  Start ISIS protocol and wait for 60 seconds
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);

################################################################################
#  Retrieve protocol statistics.
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
#  Retrieve protocol learned info in Port 1
###############################################################################
print("Fetching ISISL3 SR IPv6 Prefix Learned Info\n");
$ixNet->execute('getLearnedInfo', $isisL3_1, '1');
sleep(5);
my $linfo = ($ixNet->getList($isisL3_1, 'learnedInfo'))[0];
my $ipv6table = ($ixNet->getList($linfo, 'table'))[2];
     my @values   = $ixNet->getAttribute($ipv6table, '-values');
     my $v        = ''; 
	 

print("***************************************************\n");
foreach $v (@values) {
 	my $w = '0';
	foreach $w (@$v) {
	    printf("%15s", $w);
	}    
	print("\n");
}
print("***************************************************\n");

print("Fetching ISISL3 SR IPv6 Adj Learned Info\n");
$ixNet->execute('getLearnedInfo', $isisL3_1, '1');
sleep(5);
my $linfo = ($ixNet->getList($isisL3_1, 'learnedInfo'))[0];
my $ipv6table = ($ixNet->getList($linfo, 'table'))[3];
     my @values   = $ixNet->getAttribute($ipv6table, '-values');
     my $v        = ''; 
	 

print("***************************************************\n");
foreach $v (@values) {
 	my $w = '0';
	foreach $w (@$v) {
	    printf("%15s", $w);
	}    
	print("\n");
}
print("***************************************************\n");

################################################################################
#  Setting on the fly change of IPv6 Node Prefix Address in Simulated Router
################################################################################
print("Disabling Adl_sid on the fly \n");
my $ipv6SidValue1 = ($ixNet->getAttribute($isisL3PseudoInterface1, '-enableAdjSID'))[0];
$ixNet->setAttribute($ipv6SidValue1.'/singleValue', '-value', 'false');
$ixNet->commit();

my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
print("Wait for 30 seconds ...\n");
sleep(30);

###############################################################################
#  Retrieve protocol learned info
###############################################################################

print("Fetching ISISL3 SR IPv6 Adj Learned Info after OTF action\n");
$ixNet->execute('getLearnedInfo', $isisL3_1, '1');
sleep(5);
my $linfo = ($ixNet->getList($isisL3_1, 'learnedInfo'))[0];
my $ipv6table = ($ixNet->getList($linfo, 'table'))[3];
     my @values   = $ixNet->getAttribute($ipv6table, '-values');
     my $v        = ''; 
	 

print("***************************************************\n");
foreach $v (@values) {
 	my $w = '0';
	foreach $w (@$v) {
	    printf("%15s", $w);
	}    
	print("\n");
}
print("***************************************************\n");


################################################################################
# Stop all protocols
################################################################################
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!");

