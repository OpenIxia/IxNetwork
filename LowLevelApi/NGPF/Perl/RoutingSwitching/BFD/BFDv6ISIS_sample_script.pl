################################################################################
# Version 1.0    $Revision: #1 $                                               #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    05/12/2015 - Dhiraj Khandelwal - created sample                           #
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
#    This script intends to demonstrate how to use NGPF BFDv6 API.             #
#                                                                              #
#    1. It will create 2 BGP topologies, each having an ipv4 network           #
#       topology and emulate the same , collect stats and learned info         #
# Ixia Software:                                                               #
#    IxOS      8.00 EA                                                         #
#    IxNetwork 8.00 EA                                                         #
#                                                                              #
################################################################################

################################################################################
# Please ensure that PERL5LIB environment variable is set properly so that     # 
# IxNetwork.pm module is available. IxNetwork.pm is generally available in     #
# C:\<IxNetwork Install Path>\API\Perl                                         #
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
my $ixTclServer = '10.216.22.27';
my $ixTclPort   = '8229';
my @ports       = (('10.216.108.99', '11', '3'), ('10.216.108.99', '11', '4'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '8.00',
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
print("Add ipv6\n");
$ixNet->add($mac1, 'ipv6');
$ixNet->add($mac2, 'ipv6');
$ixNet->commit();

my $ip1 = ($ixNet->getList($mac1, 'ipv6'))[0];
my $ip2 = ($ixNet->getList($mac2, 'ipv6'))[0];

my $mvAdd1 = $ixNet->getAttribute($ip1, '-address');
my $mvAdd2 = $ixNet->getAttribute($ip2, '-address');
my $mvGw1  = $ixNet->getAttribute($ip1, '-gatewayIp');
my $mvGw2  = $ixNet->getAttribute($ip2, '-gatewayIp');

print("configuring ipv6 addresses\n");
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '11:0:0:0:0:0:0:1');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '11:0:0:0:0:0:0:2');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '11:0:0:0:0:0:0:2');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', '11:0:0:0:0:0:0:1');

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '64');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '64');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();
###########################################################################
#Add and Configure bfdv6 Interface 
###########################################################################
print("Adding and Configuring Bfdv6 Interface\n");
$ixNet->add($ip1, 'bfdv6Interface');
$ixNet->add($ip2, 'bfdv6Interface');
$ixNet->commit();

my $bfdv61 = ($ixNet->getList($ip1, 'bfdv6Interface'))[0];
my $bfdv62 = ($ixNet->getList($ip2, 'bfdv6Interface'))[0];

my $txInterval1 = $ixNet->getAttribute($bfdv61, '-txInterval');
my $txInterval2 = $ixNet->getAttribute($bfdv62, '-txInterval');
my $minRxInterval1 = $ixNet->getAttribute($bfdv61, '-minRxInterval');
my $minRxInterval2 = $ixNet->getAttribute($bfdv62, '-minRxInterval');

$ixNet->setAttribute($txInterval1.'/singleValue', '-value', '2000');
$ixNet->setAttribute($txInterval2.'/singleValue', '-value', '2000');
$ixNet->setAttribute($minRxInterval1.'/singleValue', '-value', '2000');
$ixNet->setAttribute($minRxInterval2.'/singleValue', '-value', '2000');
$ixNet->commit();

############################################################################
#Add and Configure ISIS-L3 Router
############################################################################
print("Adding and Configuring ISIS-L3\n");
$ixNet->add($mac1, 'isisL3');
$ixNet->add($mac2, 'isisL3');
$ixNet->commit();

my $isisL31 = ($ixNet->getList($mac1, 'isisL3'))[0];
my $isisL32 = ($ixNet->getList($mac2, 'isisL3'))[0];

my $enableBFD1 = $ixNet->getAttribute($isisL31, '-enableBfdRegistration');
print("Adding and Configuring ISIS-L3\n");
my $enableBFD2 = $ixNet->getAttribute($isisL32, '-enableBfdRegistration');
print("Adding and Configuring ISIS-L3\n");
my $networkType1 = $ixNet->getAttribute($isisL31, '-networkType');
print("Adding and Configuring ISIS-L3\n");
my $networkType2 = $ixNet->getAttribute($isisL32, '-networkType');

$ixNet->setAttribute($enableBFD1.'/singleValue', '-value', 'true');
$ixNet->setAttribute($enableBFD2.'/singleValue', '-value', 'true');
$ixNet->setAttribute($networkType1.'/singleValue', '-value', 'pointpoint');
$ixNet->setAttribute($networkType2.'/singleValue', '-value', 'pointpoint');
$ixNet->commit();

################################################################################
# Start BFD protocol and wait for 60 seconds                                   #
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

################################################################################
#On The Fly Section
################################################################################
print("Activating and Deactivating bfdv6 Interface on the fly");
my $activation = $ixNet->getAttribute($bfdv61, '-active');

$ixNet->setAttribute($activation.'/singleValue', '-value', 'false');
$ixNet->commit();
my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(10);
$ixNet->setAttribute($activation.'/singleValue', '-value', 'true');
$ixNet->commit();
my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(10);

###############################################################################
# Retrieve protocol learned info                                              #
###############################################################################
print("Fetching BFD Learned Info\n");
$ixNet->execute('getLearnedInfo', $bfdv61, '1');
sleep(5);
my $linfo  = ($ixNet->getList($bfdv61, 'learnedInfo'))[0];
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
# Stop all protocols                                                           #
################################################################################
print("Stopping all Protocols");
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!");
