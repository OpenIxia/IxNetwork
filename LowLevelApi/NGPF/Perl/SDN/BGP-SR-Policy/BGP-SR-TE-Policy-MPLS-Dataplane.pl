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
#    This script intends to demonstrate how to use NGPF BGP API                #
#    It will create 2 BGP topologies, it will start the emulation and          #
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
my $ixTclServer = '10.39.50.121';
my $ixTclPort   = '8239';
my @ports       = (('10.39.50.123', '5', '7'), ('10.39.50.123', '5', '8'));
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

print("Adding BGP over IPv4 stacks \n");
$ixNet->add($ip1, 'bgpIpv4Peer');
$ixNet->add($ip2, 'bgpIpv4Peer');
$ixNet->commit();

my $bgp1 = ($ixNet->getList($ip1, 'bgpIpv4Peer'))[0];
my $bgp2 = ($ixNet->getList($ip2, 'bgpIpv4Peer'))[0];

print("Renaming the topologies and the device groups \n");
$ixNet->setAttribute($topo1,  '-name', 'BGP Topology 1');
$ixNet->setAttribute($topo2,  '-name', 'BGP Topology 2');

$ixNet->setAttribute($t1dev1, '-name', 'SR-TE Policy Controller');
$ixNet->setAttribute($t2dev1, '-name', 'Head/Tail End Router');
$ixNet->commit();

print("Setting IPs in BGP DUT IP tab\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1, '-dutIp').'/singleValue', '-value', '20.20.20.1');
$ixNet->setAttribute($ixNet->getAttribute($bgp2, '-dutIp').'/singleValue', '-value', '20.20.20.2');
$ixNet->commit();


print("Enabling IPv4 SRTE Policy Capability \n");
my $cap1 = $ixNet->getAttribute($bgp1, '-capabilitySRTEPoliciesV4');
my $cap2 = $ixNet->getAttribute($bgp2, '-capabilitySRTEPoliciesV4');
my $sv1 = ($ixNet->getList($cap1, 'singleValue'))[0];
my $sv2 = ($ixNet->getList($cap2, 'singleValue'))[0];
$ixNet->setAttribute($sv1, '-value', 'true');
$ixNet->setAttribute($sv2, '-value', 'true');

print("Enabling IPv4 SRTE Policy Learn Info filter \n");
my $filter1 = $ixNet->getAttribute($bgp1, '-filterSRTEPoliciesV4');
my $filter2 = $ixNet->getAttribute($bgp2, '-filterSRTEPoliciesV4');
my $sv1 = ($ixNet->getList($filter1, 'singleValue'))[0];
my $sv2 = ($ixNet->getList($filter2, 'singleValue'))[0];
$ixNet->setAttribute($sv1, '-value', 'true');
$ixNet->setAttribute($sv2, '-value', 'true');


print("*************************************************************\n");
print ("Configuring Controller\n");
print("*************************************************************\n");

print ("Setting Number of policies\n");
$ixNet->setAttribute($bgp1, '-numberSRTEPolicies', '1');
$ixNet->commit();

print ("Setting IPv4 End Point value\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1.'/bgpSRTEPoliciesListV4', '-endPointV4').'/singleValue', '-value', '30.30.30.1');
$ixNet->commit();

print ("Setting color Value\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1.'/bgpSRTEPoliciesListV4', '-policyColor').'/singleValue', '-value', '200');
$ixNet->commit();

print ("Setting Number of Segmnent Lists\n");
$ixNet->setAttribute($bgp1.'/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4', '-numberOfSegmentListV4', '2');
$ixNet->commit();

print ("Enabling Binding SID\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1.'/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4', '-enBindingTLV').'/singleValue', '-value', 'true');
$ixNet->commit();

print ("Setting Binding SID Type\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1.'/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4', '-bindingSIDType').'/singleValue', '-value', 'sid4');
$ixNet->commit();

print ("Setting Binding SID Type\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1.'/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4', '-SID4Octet').'/singleValue', '-value', '400');
$ixNet->commit();

print ("Setting Number of Segments\n");
$ixNet->setAttribute($bgp1.'/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4/bgpSRTEPoliciesSegmentListV4', '-numberOfSegmentsV4', '3');
$ixNet->commit();

print ("Setting lable value for -MPLS SID Only- Segment Type\n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1.'/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4/bgpSRTEPoliciesSegmentListV4/bgpSRTEPoliciesSegmentsCollectionV4', '-label').'/singleValue', '-value', '999');
$ixNet->commit();

print("*************************************************************\n");
print("Configuring Prefix\n");
print("*************************************************************\n");

print("Adding the NetworkGroup with Routers at back of it \n");
$ixNet->execute('createDefaultStack', $t2dev1, 'ipv4PrefixPools');
my $networkGroup1 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];
$ixNet->setAttribute($networkGroup1, '-name', 'Endpoint Prefix Advertising color');

my $ip4pool = ($ixNet->getList($networkGroup1, 'ipv4PrefixPools'))[0];
my $bgpIPRouteProperty = ($ixNet->getList($ip4pool, 'bgpIPRouteProperty'))[0];

print ("Setting Network Address\n");
$ixNet->setAttribute($ixNet->getAttribute($ip4pool, '-networkAddress').'/singleValue', '-value', '30.30.30.1');

print ("Enabling Extended Community\n");
$ixNet->setAttribute($ixNet->getAttribute($bgpIPRouteProperty, '-enableExtendedCommunity').'/singleValue', '-value', 'true');

print ("Setting Extended Community Type\n");
$ixNet->setAttribute($ixNet->getAttribute($bgpIPRouteProperty.'/bgpExtendedCommunitiesList:1', '-type').'/singleValue', '-value', 'opaque');

print ("Setting Extended Community Sub-Type\n");
$ixNet->setAttribute($ixNet->getAttribute($bgpIPRouteProperty.'/bgpExtendedCommunitiesList:1', '-subType').'/singleValue', '-value', 'color');

print ("Setting Color Value\n");
$ixNet->setAttribute($ixNet->getAttribute($bgpIPRouteProperty.'/bgpExtendedCommunitiesList:1', '-colorValue').'/singleValue', '-value', '200');
$ixNet->commit();

################################################################################
# Start BGP protocol and wait for 60 seconds                                   #
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
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


################################################################################
# On the fly section                                                           #  
################################################################################
print("Changing the Lable Value on the Fly \n");
$ixNet->setAttribute($ixNet->getAttribute($bgp1.'/bgpSRTEPoliciesListV4/bgpSRTEPoliciesTunnelEncapsulationListV4/bgpSRTEPoliciesSegmentListV4/bgpSRTEPoliciesSegmentsCollectionV4', '-label').'/singleValue', '-value', '1000');
$ixNet->commit();

my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(10);

###############################################################################
# print learned info                                                          #
###############################################################################
$ixNet->execute('getbgpSrTeLearnedInfoLearnedInfo', $bgp2, '1');
sleep(5);

print("Print Bgp Ipv4 SR-TE Learned Info");
my $learnedInfoList = ($ixNet->getList($bgp2, 'learnedInfo'))[0];
my $learnedInfo = ($learnedInfoList, 'end')[0];
my $table = ($ixNet->getList($learnedInfo, 'table'))[0];
my @learnedInfoColumnsList = ($ixNet->getAttribute($table, '-columns'));
my @learnedInfoValuesList = ($ixNet->getAttribute($table, '-values'));
print("***************************************************\n");
print("@learnedInfoColumnsList\n");
my $v      = '';
print("***************************************************\n");
foreach $v (@learnedInfoValuesList) {
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
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!\n");
