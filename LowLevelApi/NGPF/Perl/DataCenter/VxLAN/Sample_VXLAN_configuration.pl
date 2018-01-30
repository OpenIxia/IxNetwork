################################################################################
# Version 1.0    $Revision: #1 $                                               #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    02/04/2015 - Indranil Acharya - created sample                            #
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
#    This script intends to demonstrate how to use NGPF VxLAN  API             #
#    than it will retrieve and display few statistics                          #
# Ixia Softwares:                                                              #
#    IxOS      6.80 EA (6.80.1100.7)                                           #
#    IxNetwork 7.50 EA (7.50.0.45)                                             #
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
my $ixTclServer = '10.200.115.31';
my $ixTclPort   = '8009';
my @ports       = (('10.200.115.31', '5', '1'), ('10.200.115.31', '6', '1'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '7.40',
    '-setAttribute', 'strict');

print("Creating a new config\n");
$ixNet->execute('newConfig');

################################################################################
# Adding ports to configuration
################################################################################

print "Adding ports to configuration\n";
my $root = $ixNet->getRoot();
$ixNet->add($root, 'vport');
$ixNet->add($root, 'vport');
$ixNet->commit();
my @vPorts = $ixNet->getList($root, 'vport');
my $vport1 = @vPorts[0];
my $vport2 = @vPorts[1];

################################################################################
# Adding VXLAN Protocol
################################################################################

print "Add topologies\n";
$ixNet->add($root, 'topology');
$ixNet->add($root, 'topology');
$ixNet->commit();
my @top = $ixNet->getList($root, 'topology');
my $topo1 = @top[0];
my $topo2 = @top[1];

print "Add ports to topologies\n";
$ixNet->setAttribute($topo1, '-vports', $vport1);
$ixNet->setAttribute($topo2, '-vports', $vport2);
$ixNet->commit();

my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vportTx = $vPorts[0];
my $vportRx = $vPorts[1];
assignPorts($ixNet, @ports, $vportTx, $vportRx);

print "Add device groups to topologies\n";
$ixNet->add($topo1, 'deviceGroup');
$ixNet->add($topo2, 'deviceGroup');
$ixNet->commit();

my @dg1 = $ixNet->getList($topo1, 'deviceGroup');
my @dg2 = $ixNet->getList($topo2, 'deviceGroup');
my $dg1_1 = @dg1[0];
my $dg2_1 = @dg2[0];

print "Add Ethernet stacks to device groups\n";
$ixNet->add($dg1_1, 'ethernet');
$ixNet->add($dg2_1, 'ethernet');
$ixNet->commit();

my @mac1 = $ixNet->getList($dg1_1, 'ethernet');
my @mac2 = $ixNet->getList($dg2_1, 'ethernet');
my $mac1_1 = @mac1[0];
my $mac2_1 = @mac2[0];

print "Add ipv4 stacks to Ethernets\n";
$ixNet->add($mac1_1, 'ipv4');
$ixNet->add($mac2_1, 'ipv4');
$ixNet->commit();
my @ipv41 = $ixNet->getList($mac1_1, 'ipv4');
my @ipv42 = $ixNet->getList($mac2_1, 'ipv4');
my $ipv41_1 = @ipv41[0];
my $ipv42_1 = @ipv42[0];
print "Setting multi values for ipv4 addresses\n";
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv41_1, '-address').'/counter', '-start', '22.1.1.1', '-step', '0.0.1.0');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv41_1, '-gatewayIp').'/counter', '-start', '22.1.1.2', '-step', '0.0.1.0');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv41_1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv42_1, '-address').'/counter', '-start', '22.1.1.2', '-step', '0.0.1.0');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv42_1, '-gatewayIp').'/counter', '-start', '22.1.1.1', '-step', '0.0.1.0');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv42_1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

print "Add VXLAN stacks to IPv4\n";
$ixNet->add($ipv41_1, 'vxlan');
$ixNet->add($ipv42_1, 'vxlan');
$ixNet->commit();

my @vxlan1 = $ixNet->getList($ipv41_1, 'vxlan');
my @vxlan2 = $ixNet->getList($ipv42_1, 'vxlan');

my $vxlan1_1 = @vxlan1[0];
my $vxlan2_1 = @vxlan2[0];

$ixNet->setMultiAttribute($ixNet->getAttribute($vxlan1_1, '-vni').'/counter', '-start', '1100', '-step', '1');
$ixNet->setMultiAttribute($ixNet->getAttribute($vxlan1_1, '-ipv4_multicast').'/counter', '-start', '225.0.0.1', '-step', '1.0.0.0');
$ixNet->setMultiAttribute($ixNet->getAttribute($vxlan2_1, '-vni').'/counter', '-start', '1100', '-step', '1');
$ixNet->setMultiAttribute($ixNet->getAttribute($vxlan2_1, '-ipv4_multicast').'/counter', '-start', '225.0.0.1', '-step', '1.0.0.0');

print "Add Inner Device Groups to the Outer Device Groups\n";
$ixNet->add($dg1_1, 'deviceGroup');
$ixNet->add($dg2_1, 'deviceGroup');
$ixNet->commit();

my @dg3 = $ixNet->getList($dg1_1, 'deviceGroup');
my @dg4 = $ixNet->getList($dg2_1, 'deviceGroup');

my $dg3_1 = @dg3[0];
my $dg4_1 = @dg4[0];

print "Add Ethernet stacks to the inner device groups\n";
$ixNet->add($dg3_1, 'ethernet');
$ixNet->add($dg4_1, 'ethernet');
$ixNet->commit();

my @mac3 = $ixNet->getList($dg3_1, 'ethernet');
my @mac4 = $ixNet->getList($dg4_1, 'ethernet');

my $mac3_1 = @mac3[0];
my $mac4_1 = @mac4[0];

print "Add a connector between the Ethernet and VXLAN\n";
$ixNet->add($mac3_1, 'connector');
$ixNet->add($mac4_1, 'connector');
$ixNet->commit();


my @connector1 = $ixNet->getList($mac3_1, 'connector');
my @connector2 = $ixNet->getList($mac4_1, 'connector');

my $connector1_1 = @connector1[0];
my $connector2_1 = @connector2[0];

$ixNet->setAttribute($connector1_1, '-connectedTo', $vxlan1_1);
$ixNet->setAttribute($connector2_1, '-connectedTo', $vxlan2_1);
$ixNet->commit();

print "Add IPv4 stacks to inner Ethernets\n";
$ixNet->add($mac3_1, 'ipv4');
$ixNet->add($mac4_1, 'ipv4');
$ixNet->commit();

my @ipv4_3 = $ixNet->getList($mac3_1, 'ipv4');
my @ipv4_4 = $ixNet->getList($mac4_1, 'ipv4');

my $ipv4_3_1= @ipv4_3[0];
my $ipv4_4_1= @ipv4_4[0];

print "Setting multi values for inner IPv4 addresses\n";
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv4_3_1, '-address').'/counter', '-start', '5.1.1.1', '-step', '0.0.1.0');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv4_3_1, '-gatewayIp').'/counter', '-start', '5.1.1.2', '-step', '0.0.1.0');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv4_3_1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv4_4_1, '-address').'/counter', '-start', '5.1.1.2', '-step', '0.0.1.0');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv4_4_1, '-gatewayIp').'/counter', '-start', '5.1.1.1', '-step', '0.0.1.0');
$ixNet->setMultiAttribute($ixNet->getAttribute($ipv4_4_1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

################################################################################
# Start protocol 
################################################################################

print("Starting protocol\n");
$ixNet->execute('startAllProtocols');
print("Running the protocol for 30 seconds ..\n");
sleep(30);

################################################################################
# Retrieve protocol statistics.
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
sleep(5);

################################################################################
# Stop protocol 
################################################################################

print("\nStopping protocol\n");
$ixNet->execute('stopAllProtocols');

print("!!! Test Script Ends !!!");