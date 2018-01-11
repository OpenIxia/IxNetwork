################################################################################
# Version 1.0    $Revision: #1 $                                               #
#                                                                              #
#    Copyright © 1997 - 2016 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    25/11/2015 - Shilpam Sinha - created sample                               #
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
##                                                                              #
## Description:                                                                 #
##    This script intends to demonstrate how to use NGPF BGPLS &                #
##    ISIS TE SR Low Level Perl API.                                            #
##                                                                              #
##    1. It will create 2 BGP and 2 ISIS Topologies and 1 Network Group.        #
##    2. ISIS SR, TE and SR Algorithm is enabled on both Emulated and           #
##       Simulated Routers.                                                     #
##    3. BGP LS is Enabled                                                      #
##    4. Start All Protocols                                                    #
##    5. Check Protocol Stats                                                   #
##    6. Check BGPLS Learned Info	                                        #
##    7. Stop all protocols.                                                    #
##                                                                              #
## Ixia Softwares:                                                              #
##    IxOS      8.20 EA                                                         #
##    IxNetwork 8.20 EA                                                         #
##                                                                              #
#################################################################################

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
my $ixTclPort   = '8919';
my @ports       = (('10.216.108.99', '11', '3'), ('10.216.108.99', '11', '4'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '8.20',
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

print("Add ISISL3\n");
$ixNet->add($mac1, 'isisL3');
$ixNet->add($mac2, 'isisL3');
$ixNet->commit();

my $isisL3_1 = ($ixNet->getList($mac1, 'isisL3'))[0];
my $isisL3_2 = ($ixNet->getList($mac2, 'isisL3'))[0];

print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'BGP Topology 1');
$ixNet->setAttribute($topo2, '-name', 'BGP Topology 2');

$ixNet->setAttribute($t1dev1, '-name', 'BGP-LS ISIS-TE Topology 1 Router');
$ixNet->setAttribute($t2dev1, '-name', 'BGP-LS ISIS-TE Topology 2 Router');
$ixNet->commit();

my $deviceGroup1 = ($ixNet->getList($topo1, 'deviceGroup'))[0];
my $isisL3Router1 = ($ixNet->getList($deviceGroup1, 'isisL3Router'))[0];

my $deviceGroup2 = ($ixNet->getList($topo2, 'deviceGroup'))[0];
my $isisL3Router2 = ($ixNet->getList($deviceGroup2, 'isisL3Router'))[0];

print("Enabling Host name in Emulated ISIS Routers\n");

# Enable host name in ISIS router1
my $enableHostName1 = ($ixNet->getAttribute($isisL3Router1, '-enableHostName'));
$ixNet->setAttribute($enableHostName1.'/singleValue', '-value', 'True');
$ixNet->commit();
my $configureHostName1 = $ixNet->getAttribute($isisL3Router1, '-hostName');
$ixNet->setAttribute($configureHostName1.'/singleValue', '-value', 'isisL3Router1');
$ixNet->commit();

#Enable host name in ISIS router2
my $enableHostName2 = ($ixNet->getAttribute($isisL3Router2, '-enableHostName'));
$ixNet->setAttribute($enableHostName2.'/singleValue', '-value', 'True');
$ixNet->commit();
my $configureHostName2 = ($ixNet->getAttribute($isisL3Router2, '-hostName'));
$ixNet->setAttribute($configureHostName2.'/singleValue', '-value', 'isisL3Router2');
$ixNet->commit();

print("Making the NetworkType to Point to Point in the first ISISrouter\n");
my $networkTypeMultiValue1 = ($ixNet->getAttribute($isisL3_1, '-networkType'));
$ixNet->setMultiAttribute($networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($networkTypeMultiValue1.'/singleValue', '-value', 'pointpoint');

print("Making the NetworkType to Point to Point in the Second ISIS router\n");
my $networkTypeMultiValue2 = ($ixNet->getAttribute($isisL3_2, '-networkType'));
$ixNet->setAttribute($networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setAttribute($networkTypeMultiValue2.'/singleValue', '-value', 'pointpoint');


################################################################################
## Traffic Engineering Configuration for ISIS Emulated Routers
#################################################################################
print("Enabling TE on Router1\n");
my $enableTE_1 = ($ixNet->getAttribute($isisL3Router1, '-enableTE'));
$ixNet->setAttribute($enableTE_1.'/singleValue', '-value', 'True');
$ixNet->commit();

print("Enabling TE on Router2\n");
my $enableTE_2 = ($ixNet->getAttribute($isisL3Router2, '-enableTE'));
$ixNet->setAttribute($enableTE_2.'/singleValue', '-value', 'True');
$ixNet->commit();

print("Enabling Metric Level for Traffic Engineering under ISISL3-IF in DG1\n");
my $isisTrafficEngineering1 = ($ixNet->getList($isisL3_1, 'isisTrafficEngineering'))[0];
my $metricLevel1 = ($ixNet->getAttribute($isisTrafficEngineering1, '-metricLevel'));
$ixNet->setAttribute($metricLevel1.'/singleValue', '-value', '44');
$ixNet->commit();

print("Enabling Metric Level for Traffic Engineering under ISISL3-IF in DG2\n");
my $isisTrafficEngineering2 = ($ixNet->getList($isisL3_2, 'isisTrafficEngineering'))[0];
my $metricLevel2 = ($ixNet->getAttribute($isisTrafficEngineering2, '-metricLevel'));
$ixNet->setAttribute($metricLevel2.'/singleValue', '-value', '55');
$ixNet->commit();

print("Setting Maximum Bandwidth Value for Traffic Engineering under ISISL3-IF in DG1\n");
my $maxBandwidth1 = ($ixNet->getAttribute($isisTrafficEngineering1, '-maxBandwidth'));
$ixNet->setAttribute($maxBandwidth1.'/singleValue', '-value', '126000000');
$ixNet->commit();

print("Setting Maximum Bandwidth Value for Traffic Engineering under ISISL3-IF in DG2\n");
my $maxBandwidth2 = ($ixNet->getAttribute($isisTrafficEngineering2, '-maxBandwidth'));
$ixNet->setAttribute($maxBandwidth2.'/singleValue', '-value', '127000000');
$ixNet->commit();

print("Setting Maximum Reservable Bandwidth Value for Traffic Engineering under ISISL3-IF in DG1\n");
my $maxReservableBandwidth1 = ($ixNet->getAttribute($isisTrafficEngineering1, '-maxReservableBandwidth'));
$ixNet->setAttribute($maxReservableBandwidth1.'/singleValue', '-value', '128000000');
$ixNet->commit();

print("Setting Maximum Reservable Bandwidth Value for Traffic Engineering under ISISL3-IF in DG2\n");
my $maxReservableBandwidth2 = ($ixNet->getAttribute($isisTrafficEngineering2, '-maxReservableBandwidth'));
$ixNet->setAttribute($maxReservableBandwidth2.'/singleValue', '-value', '129000000');
$ixNet->commit();

print("Setting Administrator Group Value for Traffic Engineering under ISISL3-IF in DG1\n");
my $administratorGroup1 = ($ixNet->getAttribute($isisTrafficEngineering1, '-administratorGroup'));
$ixNet->setAttribute($administratorGroup1.'/singleValue', '-value', '22');
$ixNet->commit();

print("Setting Administrator Group Value for Traffic Engineering under ISISL3-IF in DG2\n");
my $administratorGroup2 = ($ixNet->getAttribute($isisTrafficEngineering2, '-administratorGroup'));
$ixNet->setAttribute($administratorGroup2.'/singleValue', '-value', '33');
$ixNet->commit();

################################################################################
## Enabling Segment Routing in Emulated Router
#################################################################################
print("Enabling Segment Routing for ISIS\n");
$ixNet->setAttribute($isisL3Router1, '-enableSR', 'True');
$ixNet->commit();

$ixNet->setAttribute($isisL3Router2, '-enableSR', 'True');
$ixNet->commit();

################################################################################
## Setting SRGB range and SID Count for Emulated Router
#################################################################################
print("Setting SRGB range pool for first Emulated Router\n");
my $isisSRGBRangeSubObjectsList1 = ($ixNet->getList($isisL3Router1, 'isisSRGBRangeSubObjectsList'))[0];
my $startSIDLabel1 = ($ixNet->getAttribute($isisSRGBRangeSubObjectsList1, '-startSIDLabel'));
$ixNet->setAttribute($startSIDLabel1.'/singleValue', '-value', '15000');
$ixNet->commit();

print("Setting SID count for first Emulated Router\n");
my $sIDCount1 = ($ixNet->getAttribute($isisSRGBRangeSubObjectsList1, '-sIDCount'));
$ixNet->setAttribute($sIDCount1.'/singleValue', '-value', '100');
$ixNet->commit();

print("Setting SRGB range pool for second Emulated Router\n");
my $isisSRGBRangeSubObjectsList2 = ($ixNet->getList($isisL3Router2, 'isisSRGBRangeSubObjectsList'))[0];
my $startSIDLabel2 = ($ixNet->getAttribute($isisSRGBRangeSubObjectsList2, '-startSIDLabel'));
$ixNet->setAttribute($startSIDLabel2.'/singleValue', '-value', '10000');
$ixNet->commit();

print("Setting SID count for second Emulated Router\n");
my $sIDCount2 = ($ixNet->getAttribute($isisSRGBRangeSubObjectsList2, '-sIDCount'));
$ixNet->setAttribute($sIDCount2.'/singleValue', '-value', '100');
$ixNet->commit();

print("Enabling Adj-SID in first Emulated Router\n");
my $enableAdjSID1 = ($ixNet->getAttribute($isisL3_1, '-enableAdjSID'));
$ixNet->setAttribute($enableAdjSID1.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Enabling Adj-SID in second Emulated Router\n");
my $enableAdjSID2 = ($ixNet->getAttribute($isisL3_2, '-enableAdjSID'));
$ixNet->setAttribute($enableAdjSID2.'/singleValue', '-value', 'true');
$ixNet->commit();

print("Setting Adj-SID value in first Emulated Router\n");
my $adjSID1 = ($ixNet->getAttribute($isisL3_1, '-adjSID'));
$ixNet->setAttribute($adjSID1.'/counter', '-step', '1',
                                          '-start', '9001', 
                                          '-direction', 'increment');
$ixNet->commit();

print("Setting Adj-SID value in second Emulated Router\n");
my $adjSID2 = ($ixNet->getAttribute($isisL3_2, '-adjSID'));
$ixNet->setAttribute($adjSID2.'/counter', '-step', '1',
                                          '-start', '9002', 
                                          '-direction', 'increment');
$ixNet->commit();

################################################################################
## Enabling Segment Routing Algorithm in Emulated Router
################################################################################
print("Enabling Segment Routing Algorithm in Emulated Router1\n");
my $isisSRAlgorithmList1 = ($ixNet->getList($isisL3Router1, 'isisSRAlgorithmList'))[0];
my $isisSrAlgorithm1 = ($ixNet->getAttribute($isisSRAlgorithmList1, '-isisSrAlgorithm'));
$ixNet->setAttribute($isisSrAlgorithm1.'/singleValue', '-value', '30');
$ixNet->commit();

print("Enabling Segment Routing Algorithm in Emulated Router2\n");
my $isisSRAlgorithmList2 = ($ixNet->getList($isisL3Router2, 'isisSRAlgorithmList'))[0];
my $isisSrAlgorithm2 = ($ixNet->getAttribute($isisSRAlgorithmList2, '-isisSrAlgorithm'));
$ixNet->setAttribute($isisSrAlgorithm2.'/singleValue', '-value', '60');
$ixNet->commit();

################################################################################
## Adding BGP and Enabling BGPLS
#################################################################################
print("Adding BGP over IP4 stacks \n");
$ixNet->add($ip1, 'bgpIpv4Peer');
$ixNet->add($ip2, 'bgpIpv4Peer');
$ixNet->commit();

my $bgp1 = ($ixNet->getList($ip1, 'bgpIpv4Peer'))[0];
my $bgp2 = ($ixNet->getList($ip2, 'bgpIpv4Peer'))[0];

print("Enabling BGPLS Capability \n");
my $capLS1 = $ixNet->getAttribute($bgp1, '-capabilityLinkStateNonVpn');
my $capLS2 = $ixNet->getAttribute($bgp2, '-capabilityLinkStateNonVpn');
my $svCap1 = ($ixNet->getList($capLS1, 'singleValue'))[0];
my $svCap2 = ($ixNet->getList($capLS2, 'singleValue'))[0];
$ixNet->setAttribute($svCap1, '-value', 'True');
$ixNet->setAttribute($svCap2, '-value', 'True');
$ixNet->commit();

print("Enabling BGPLS Filter Link State \n");
my $filterLS1 = $ixNet->getAttribute($bgp1, '-filterLinkState');
my $filterLS2 = $ixNet->getAttribute($bgp2, '-filterLinkState');
my $svLS1 = ($ixNet->getList($filterLS1, 'singleValue'))[0];
my $svLS2 = ($ixNet->getList($filterLS2, 'singleValue'))[0];
$ixNet->setAttribute($svLS1, '-value', 'True');
$ixNet->setAttribute($svLS2, '-value', 'True');
$ixNet->commit();

print("Setting IPs in BGP DUT IP tab\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-dutIp').'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-dutIp').'/singleValue', '-value', '20.20.20.2');
$ixNet->commit();

print("Adding the NetworkGroup with Routers at back of it \n");
$ixNet->execute('createDefaultStack', $t1dev1, 'networkTopology');
my $networkGroup = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
my $networkTopology = ($ixNet->getList($networkGroup, 'networkTopology'))[0];
$ixNet->setAttribute($networkGroup,'-name', 'ISIS_Network_Group1');
$ixNet->commit();

################################################################################
## Enabling Segment Routing in simulated router
#################################################################################
print("Enabling Segment Routing in Simulated Routers on Network Group behind Device Group1\n");
my $simRouter = ($ixNet->getList($networkTopology, 'simRouter'))[0];
my $isisL3PseudoRouter = ($ixNet->getList($simRouter, 'isisL3PseudoRouter'))[0];
$ixNet->setAttribute($isisL3PseudoRouter, '-enableSR', 'True');
$ixNet->commit();

print("Set Value for SID/Index/Label\n");
my $sIDIndexLabel = ($ixNet->getAttribute($isisL3PseudoRouter, '-sIDIndexLabel'));
$ixNet->setAttribute($sIDIndexLabel.'/singleValue', '-value', '100');
$ixNet->commit();

print("Set Value for Start SID/Label-1\n");
my $isisSRGBRangeSubObjectsList = ($ixNet->getList($isisL3PseudoRouter, 'isisSRGBRangeSubObjectsList'))[0];
my $sIDIndexLabel = ($ixNet->getAttribute($isisSRGBRangeSubObjectsList, '-startSIDLabel'));
$ixNet->setAttribute($sIDIndexLabel.'/counter', '-step', '100','-start', '116000', '-direction', 'increment');
$ixNet->commit();

print("Set Value for Start SID Count-1\n");
my $sIDCount = ($ixNet->getAttribute($isisSRGBRangeSubObjectsList, '-sIDCount'));
$ixNet->setAttribute($sIDCount.'/singleValue', '-value', '9000');
$ixNet->commit();

print("Enabling Adj-Sid in Simulated Interface on Network Group behind Device Group2\n");
my $simInterface = ($ixNet->getList($networkTopology, 'simInterface'))[0];
my $isisL3PseudoInterface = ($ixNet->getList($simInterface, 'isisL3PseudoInterface'))[0];
my $enableAdjSID = ($ixNet->getAttribute($isisL3PseudoInterface, '-enableAdjSID'));
$ixNet->setAttribute($enableAdjSID.'/singleValue', '-value', 'True');
$ixNet->commit();

print("Set IPv6 Adj-SID value for Simulated Interface\n");
my $ipv6SidValue = ($ixNet->getAttribute($isisL3PseudoInterface, '-ipv6SidValue'));
$ixNet->setAttribute($ipv6SidValue.'/singleValue', '-value', '8000::1');
$ixNet->commit();

################################################################################
## Traffic Engineering Configuration for ISIS Simulated Routers
#################################################################################
print("Enabling TE on Simulated Router\n");
my $enableTE = ($ixNet->getAttribute($isisL3PseudoRouter, '-enable'));
$ixNet->setAttribute($enableTE.'/singleValue', '-value', 'True');
$ixNet->commit();

print("Enabling Metric Level for Traffic Engineering under ISISL3-IF in DG1\n");
my $metricLevel = ($ixNet->getAttribute($isisL3PseudoInterface, '-metricLevel'));
$ixNet->setAttribute($metricLevel.'/singleValue', '-value', '67');
$ixNet->commit();

print("Setting Maximum Bandwidth Value for Traffic Engineering under ISISL3-IF in DG1\n");
my $maxBandwidth_Bps = ($ixNet->getAttribute($isisL3PseudoInterface, '-maxBandwidth_Bps'));
$ixNet->setAttribute($maxBandwidth_Bps.'/singleValue', '-value', '136000000');
$ixNet->commit();

print("Setting Maximum Reservable Bandwidth Value for Traffic Engineering under ISISL3-IF in DG1\n");
my $maxReservableBandwidth_Bps = ($ixNet->getAttribute($isisL3PseudoInterface, '-maxReservableBandwidth_Bps'));
$ixNet->setAttribute($maxReservableBandwidth_Bps.'/singleValue', '-value', '138000000');
$ixNet->commit();

print("Setting Administrator Group Value for Traffic Engineering under ISISL3-IF in DG1\n");
my $administratorGroup = ($ixNet->getAttribute($isisL3PseudoInterface, '-administratorGroup'));
$ixNet->setAttribute($administratorGroup.'/singleValue', '-value', '77');
$ixNet->commit();

################################################################################
# Start all protocol and wait for 45 seconds                                   #
################################################################################
print("Starting protocols and waiting for 45 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(45);

################################################################################
# Retrieve protocol statistics                                                 #
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
# print learned info                                                          #
###############################################################################
$ixNet->execute('getLinkStateLearnedInfo', $bgp2, '1');
sleep(15);

print("Print BGP-LS Node/Link Learned Info \n");
my $learnedInfoList = ($ixNet->getList($bgp2, 'learnedInfo'))[0];
my $learnedInfo = ($learnedInfoList, 'end')[0];
my $table = ($ixNet->getList($learnedInfo, 'table'))[0];
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

print("Print BGP-LS IPv4 Prefix Learned Info \n");
my $learnedInfoList = ($ixNet->getList($bgp2, 'learnedInfo'))[0];
my $learnedInfo = ($learnedInfoList, 'end')[0];
my $table = ($ixNet->getList($learnedInfo, 'table'))[1];
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

print("Print BGP-LS IPv6 Prefix Learned Info");
my $learnedInfoList = ($ixNet->getList($bgp2, 'learnedInfo'))[0];
my $learnedInfo = ($learnedInfoList, 'end')[0];
my $table = ($ixNet->getList($learnedInfo, 'table'))[2];
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

################################################################################
# Stop all protocols                                                           #
################################################################################
print("stopping All Protocols\n");
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!\n");
