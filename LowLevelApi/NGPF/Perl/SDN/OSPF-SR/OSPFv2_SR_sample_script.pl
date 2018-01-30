################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    03/12/2015 - Chandan Mishra - created sample                              #
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
#    This script intends to demonstrate how to use NGPF OSPFv2 API.            #
#                                                                              #
#    1. It will create 2 OSPFv2 topologies, each having an ipv4 network        #
#       topology and loopback device group behind the network group(NG) with   # 
#       loopback interface on it. A loopback device group(DG) behind network   # 
#       group is needed to support applib traffic.                             #
#    2. Start the ospfv2 protocol.                                             #
#    3. Enabling Segment Routing in ospfv2                                     #
#    4. Retrieve protocol statistics.                                          #
#    5. Retrieve protocol learned info.                                        #
#    6. Enable the Ospfv2 simulated topologies External Route type1 for DG1,   #
#       which was disabled by default and apply change on the fly.             #
#    7. Enable Segment Routing in Simulated Router                             #
#    8.	Setting SRGB range and SID Count for Emulated Router                   #
#	 9.	Enabling Adj-SID in both emulated router                               #
#	10.	Setting Adj-SID value in both emulated router                          #
#	11.	Adding Network Group behind both OSPFv2 Device Groups                  #
#	12.	Enabling Segment Routing in simulated router                           #
#	13.	Starting protocols                                                     #
#	14.	Fetching all Protocol Summary Stats                                    #
#	15.	Setting on the fly change sidIndexLabel value for ipv4PrefixPools      #
#		and Simulated Router                                                   #
#	16.	Fetching OSPFv2 Basic Learned Info									   #
#	17.	Enabling External Type-1 Simulated Routes on Network Group behind 	   #
#		Device Group1														   #
#	18.	Fetching OSPFv2 on DG2 learned info after enabling ospf external       #
#		route type1															   #
#	19.	Configuring MPLS L2-L3 Traffic Item									   #
#	20.	Verifying all the L2-L3 traffic stats                                  #
#   21. Stop L2-L3 traffic.                                                    #
#   22. Stop Application traffic.                                              #
#   23. Stop all protocols.                                                    #
#                                                                  			   #                                                                                          
# 	Ixia Softwares:                                                            #
#    IxOS      8.00 EB (8.00.1201.21)                                          #
#    IxNetwork 8.00 EB (8.00.1206.6)                                           #
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
my $ixTclServer = '10.216.104.58';
my $ixTclPort   = '8091';
my @ports       = (('10.216.108.129', '1', '3'), ('10.216.108.129', '1', '4'));
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

# puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet]"
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

print("configuring ipv4 addresses");
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '20.20.20.2');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', "20.20.20.2");

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '24');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '24');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

# puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4]"

print("Adding OSPFv2 over IPv4 stacks");
$ixNet->add($ip1, 'ospfv2');
$ixNet->add($ip2, 'ospfv2');
$ixNet->commit();

my $ospf1 = ($ixNet->getList($ip1, 'ospfv2'))[0];
my $ospf2 = ($ixNet->getList($ip2, 'ospfv2'))[0];

print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'OSPF Topology 1');
$ixNet->setAttribute($topo2, '-name', 'OSPF Topology 2');

$ixNet->setAttribute($t1dev1, '-name', 'OSPF Topology 1 Router');
$ixNet->setAttribute($t2dev1, '-name', 'OSPF Topology 2 Router');
$ixNet->commit();

print("Making the NetworkType to Point to Point in the first OSPF router\n");
my $networkTypeMultiValue1 = $ixNet->getAttribute($ospf1, '-networkType');
$ixNet->setMultiAttribute($networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($networkTypeMultiValue1.'/singleValue', '-value', 'pointtopoint');

print("Making the NetworkType to Point to Point in the Second OSPF router\n");
my $networkTypeMultiValue2 = $ixNet->getAttribute($ospf2, '-networkType');
$ixNet->setAttribute($networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setAttribute($networkTypeMultiValue2.'/singleValue', '-value', 'pointtopoint');

print("Disabling the Discard Learned Info CheckBox\n");
my $ospfv2RouterDiscardLearnedLSA1 = $ixNet->getAttribute(($ixNet->getList($t1devices[0], 'ospfv2Router'))[0],
    '-discardLearnedLsa');

my $ospfv2RouterDiscardLearnedLSA2 = $ixNet->getAttribute(($ixNet->getList($t2devices[0], 'ospfv2Router'))[0],
    '-discardLearnedLsa');

$ixNet->setAttribute($ospfv2RouterDiscardLearnedLSA1,
     '-pattern', 'singleValue',
	 '-clearOverlays', 'False');
$ixNet->setAttribute($ospfv2RouterDiscardLearnedLSA1.'/singleValue', '-value', 'False');

$ixNet->setAttribute($ospfv2RouterDiscardLearnedLSA2,
    '-pattern', 'singleValue',
	'-clearOverlays', 'False');
$ixNet->setAttribute($ospfv2RouterDiscardLearnedLSA2.'/singleValue', '-value', 'False');

# puts "ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2"
# puts "[ixNet help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4/ospfv2]"
$ixNet->commit();

################################################################################
# 1.Enabling Segment Routing in Emulated Router
################################################################################
print ("Enabling Segment Routing for OSPFv2\n");
my $ospfv2Router1 = ($ixNet->getList($t1dev1, 'ospfv2Router'))[0];
my $ospfv2Router2 = ($ixNet->getList($t2dev1, 'ospfv2Router'))[0];
$ixNet->setAttribute($ospfv2Router1, '-enableSegmentRouting', 'true');
$ixNet->setAttribute($ospfv2Router2, '-enableSegmentRouting', 'true');
$ixNet->commit();

################################################################################
# 2.Setting SRGB range and SID Count for Emulated Router
################################################################################
print ("Setting SRGB range and SID Count for Emulated Router\n");

print ("Setting SRGB range pool for second emulated router\n");
my $ospfSRGBRangeSubObjectsList2 = ($ixNet->getList($ospfv2Router2, 'ospfSRGBRangeSubObjectsList'))[0];

my $startSIDLabel2 = $ixNet->getAttribute($ospfSRGBRangeSubObjectsList2, '-startSIDLabel');
my $svsrgb2 = ($ixNet->getList($startSIDLabel2, 'singleValue'))[0];
$ixNet->setAttribute($svsrgb2, '-value', '5000');
$ixNet->commit();

print ("Setting SRGB range pool for first emulated router\n");
my $ospfSRGBRangeSubObjectsList1 = ($ixNet->getList($ospfv2Router1, 'ospfSRGBRangeSubObjectsList'))[0];

my $startSIDLabel1 = $ixNet->getAttribute($ospfSRGBRangeSubObjectsList1, '-startSIDLabel');
my $svsrgb1 = ($ixNet->getList($startSIDLabel1, 'singleValue'))[0];
$ixNet->setAttribute($svsrgb1, '-value', '4000');
$ixNet->commit();

print ("Setting SID count for second emulated router\n");
my $sidCount2 = $ixNet->getAttribute($ospfSRGBRangeSubObjectsList2, '-sidCount');
my $sidcountsv2 = ($ixNet->getList($sidCount2, 'singleValue'))[0];
$ixNet->setAttribute($sidcountsv2, '-value', '100');
$ixNet->commit();

print ("Setting SID count for first emulated router\n");
my $sidCount1 = $ixNet->getAttribute($ospfSRGBRangeSubObjectsList1, '-sidCount');
my $sidcountsv1 = ($ixNet->getList($sidCount1, 'singleValue'))[0];
$ixNet->setAttribute($sidcountsv1, '-value', '100');
$ixNet->commit();

print ("Enabling Adj-SID in first emulated router\n");
my $enableAdjSID1 = $ixNet->getAttribute($ospf1, '-enableAdjSID');
my $svAdjSID1 = $ixNet->add($enableAdjSID1, 'singleValue');
$ixNet->setAttribute($svAdjSID1, '-value', 'true');
$ixNet->commit();

print ("Enabling Adj-SID in second emulated router\n");
my $enableAdjSID2 = $ixNet->getAttribute($ospf2, '-enableAdjSID');
my $svAdjSID2 = $ixNet->add($enableAdjSID2, 'singleValue');
$ixNet->setAttribute($svAdjSID2, '-value', 'true');
$ixNet->commit();

print ("Setting Adj-SID value in first emulated router\n");
my $adjSID1 = $ixNet->getAttribute($ospf1, '-adjSID');
my $counteradjSID1 = $ixNet->add($adjSID1, 'counter');
$ixNet->setMultiAttribute($counteradjSID1 ,
'-step', '1',
'-start', '9001' ,
'-direction', 'increment');
$ixNet->commit();

print ("Setting Adj-SID value in second emulated router\n");
my $adjSID2 = $ixNet->getAttribute($ospf2, '-adjSID');
my $counteradjSID2 = $ixNet->add($adjSID2, 'counter');
$ixNet->setMultiAttribute($counteradjSID2 ,
'-step', '1',
'-start', '9002' ,
'-direction', 'increment');
$ixNet->commit();

print("Adding NetworkGroup behind OSPFv2 Device Group1\n");
$ixNet->execute('createDefaultStack', $t1dev1, 'networkTopology');
sleep(60);
my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
$ixNet->commit();
my $networkGroup2 = $ixNet->add($t2dev1, 'networkGroup');
print ("Adding Prefix Pool behind OSPFv2 Device Group2\n");
my $ipv4PrefixPools = $ixNet->add($networkGroup2, 'ipv4PrefixPools');
$ixNet->setAttribute($networkGroup2, '-multiplier', '7');
$ixNet->commit();

$ixNet->setAttribute($networkGroup1, '-name', 'OSPF_1_Network_Group1');
$ixNet->setAttribute($networkGroup2, '-name', 'OSPF_2_ipv4_Prefix_Pools');
$ixNet->commit();

################################################################################
# 3.Enabling Segment Routing in simulated router
################################################################################
print ("Enabling Segment Routing in Simulated Routers on Network Group behind Device Group1\n");
my $networkTopo1 = ($ixNet->getList($networkGroup1, 'networkTopology'))[0];
my $simRouter1 = ($ixNet->getList($networkTopo1, 'simRouter'))[0];
my $ospfPseudoRouter1 = ($ixNet->getList($simRouter1, 'ospfPseudoRouter'))[0];
$ixNet->setAttribute($ospfPseudoRouter1, '-enableSegmentRouting', 'true');
$ixNet->commit();

################################################################################
# 4.Start OSPFv2 protocol and wait for 60 seconds
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
		    printf(" %-30s:%s\n", $statcap[$index], $statIndiv);
			$index++;
        }
    }    
}
print("***************************************************\n");

################################################################################
# 6. Setting on the fly change sidIndexLabel value for ipv4PrefixPools
################################################################################
print ("Setting on the fly change sidIndexLabel value for ipv4PrefixPools from Index 10 ");
my $ospfRouteProperty1 = ($ixNet->getList($ipv4PrefixPools, 'ospfRouteProperty'))[0];
my $sidIndexLabel1 = $ixNet->getAttribute($ospfRouteProperty1, '-sidIndexLabel');
my $sidIndexLabelcounter1 = $ixNet->add($sidIndexLabel1, 'counter');
$ixNet->setMultiAttribute($sidIndexLabelcounter1 ,
'-step', '2' ,
 '-start', '10' ,
 '-direction','increment');
$ixNet->commit();

my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);

################################################################################
# 7. Setting on the fly change sidIndexLabel value for Simulated Router
################################################################################
print ("Setting on the fly change sidIndexLabel value for Simulated Router from Index 11");
my $sidIndexLabel2 =$ixNet->getAttribute($ospfPseudoRouter1, '-sidIndexLabel');
my $sidIndexLabelcounter1 =$ixNet->add($sidIndexLabel2, 'counter');
$ixNet->setMultiAttribute ($sidIndexLabelcounter1 ,
'-step', '2' ,
 '-start', '11', 
 '-direction', 'increment');
$ixNet->commit();

print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);

###############################################################################
# 8. Retrieve protocol learned info
###############################################################################
print("Fetching OSPFv2 Basic Learned Info\n");
$ixNet->execute('getBasicLearnedInfo', $ospf1, '1');
sleep(5);
my $linfo  = ($ixNet->getList($ospf1, 'learnedInfo'))[0];
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
# 9. Enable the Ospfv2 simulated topology's External Route type1, which
#    was disabled by default. And apply changes On The Fly (OTF).
################################################################################
print("Enabling External Type-1 Simulated Routes on Network Group behind Device Group1 to send SR routes for Simulated node routes\n");
my $extRoute1         = ($ixNet->getList($ospfPseudoRouter1, 'ospfPseudoRouterType1ExtRoutes'))[0];
my $activeMultivalue1 = $ixNet->getAttribute($extRoute1, '-active');

$ixNet->setAttribute($activeMultivalue1.'/singleValue', '-value', 'true');
$ixNet->commit();

my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);

###############################################################################
# 10. Retrieve protocol learned info again and compare with
#    previously retrieved learned info.  
###############################################################################
print("Fetching OSPFv2 on DG2 learned info after enabling ospf external route type1\n");
$ixNet->execute('getBasicLearnedInfo', $ospf2, '1');
sleep(5);
my $linfo  = ($ixNet->getList($ospf2, 'learnedInfo'))[0];
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
# 11. Configure L2-L3 traffic 
################################################################################
print ("Congfiguring MPLS L2-L3 Traffic Item\n");
print ("Configuring traffic item 1 with endpoints src :ospfPseudoRouterType1ExtRoutes & dst :ipv4PrefixPools\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'Traffic Item 1',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ipv4');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source       = ($networkGroup1.'/networkTopology/simRouter:1/ospfPseudoRouter:1/ospfPseudoRouterType1ExtRoutes:1');
my @destination  = ($ipv4PrefixPools);

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

$ixNet->setMultiAttribute($trafficItem1.'/configElement:1/transmissionDistribution',
    '-distributions', ['ipv4SourceIp0']);
$ixNet->commit();

$ixNet->setMultiAttribute($trafficItem1.'/tracking',
    '-trackBy',        ['sourceDestEndpointPair0','trackingenabled0','mplsMplsLabelValue0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();

print ("Configuring traffic item 2 with endpoints src :ospfv2RouterDG1 & dst :ospfv2RouterDG2\n");
my $trafficItem2 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem2, '-name', 'Traffic Item 2',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ipv4');
$ixNet->commit();

$trafficItem2    = ($ixNet->remapIds($trafficItem2))[0];
my $endpointSet2 = $ixNet->add($trafficItem2, 'endpointSet');
my @source       = ($t1dev1.'/ospfv2Router:1');
my @destination  = ($t2dev1.'/ospfv2Router:1');

$ixNet->setMultiAttribute($endpointSet2,
    '-name',                  'EndpointSet-2',
    '-multicastDestinations', (''),
    '-scalableSources',       (''),
    '-multicastReceivers',    (''),
    '-scalableDestinations',  (''),
    '-ngpfFilters',           (''),
    '-trafficGroups',         (''),
    '-sources',               @source,
    '-destinations',          @destination);
$ixNet->commit();

$ixNet->setMultiAttribute($trafficItem2.'/configElement:1/transmissionDistribution',
    '-distributions', ['ipv4SourceIp0']);
$ixNet->commit();

$ixNet->setMultiAttribute($trafficItem2.'/tracking',
    '-trackBy',        ['sourceDestEndpointPair0','trackingenabled0','mplsMplsLabelValue0','mplsFlowDescriptor0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();

print ("Enabling option Display Dynamic Value when Tracking by Dynamic Flow Descriptor from Traffic Options in Global");
my $traffic = (($ixNet->getRoot()).'/traffic');
#(($ixNet->getRoot()).'/traffic', 'trafficItem')
$ixNet->setAttribute($traffic, '-displayMplsCurrentLabelValue', 'true');
$ixNet->commit();

###############################################################################
# 12. Apply and start L2/L3 traffic
###############################################################################
print("Applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("Starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');


###############################################################################
# 13. Retrieve L2/L3 traffic item statistics
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
# 14. Stop L2/L3 traffic
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);

################################################################################
# 15. Stop all protocols
################################################################################
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!");
