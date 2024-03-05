################################################################################
#                                                                              #
#    Copyright © 1997 - 20121 by IXIA                                           #
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

#################################################################################
#                                                                               #
# Description:                                                                  #
#    This script intends to demonstrate how to use NGPF gRIBI Perl API to       #
#    configure gRIBI client topology.                                           #
#                                                                               #
#    About Topology:                                                            #
#       Within topology gRIBI Client is configured in one port. Other port will #
#    be connected to gRIBI server. gRIBI Client is emulated in the front Device #
#    Group(DG)which consists of 1 gRPC channel, 1 gRIBI clinet, 2 Next-Hop Group#
#    and 3 Next hop per next hop group.                                         #
#      The Network Group consists of gRIBI IPv4 entries which will be advertised#
#    by gRIBI client.                                                           #
#                                                                               #
# Script Flow:                                                                  #
#    Configuration flow of the script is as follows:                            #
#    Step 1. Configuration of protocols.                                        #
#         i.   Adding of gRIBI client topology.                                 #
#         ii.  Adding of Network Topology.                                      #
#         iii. Configuring some default paramaters.                             #
#         iv.  Add IPv4 topology in other port. gRIBI Server will run behind    #
#                this port.                                                     #
#                                                                               #
#         Note: IxNetwork 9.20 EA does not support gRIBI server yet. User can   #
#          connect a real server connected to emualted gRIBI cliente.           #
#          We are running a demo server in the gRIBI server port using some     #
#          cli commands. For example purpose the command to run demo server     #
#          is provided in sample script, but it will not run the commands.      # 
#          so gRIBI client sessions will not be up unless we connect it to      # 
#          real server  session  with matching IP and port number.              #
#                                                                               #
#              The script flow only gives an example of how to configure gRIBI  #
#          client topology and related parameters in IxNetwork using low        #
#          level PERL API.                                                      #
#                                                                               #
#        Step 2. Start of protocol.                                             #
#        Step 3. Protocol Statistics display.                                   #
#        Step 4. On The Fly(OTF) change of protocol parameter.                  #
#        Step 5. Again Statistics display to see OTF changes took place.        #
#        Step 6. Stop of all protocols.                                         #
#                                                                               #
#################################################################################


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
my $ixTclServer = '10.66.47.72';
my $ixTclPort   = '8961';
my @ports       = (('10.39.50.126', '1', '1'), ('10.39.50.126', '1', '2'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '9.20',
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

$ixNet->setAttribute($topo1, '-name', 'gRIBI Client Topology');
$ixNet->setAttribute($topo2, '-name', 'gRIBI Server Topology');

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
        '-start',     '22:22:22:22:22:22',
        '-step',      '00:00:00:00:00:01');

$ixNet->setAttribute($ixNet->getAttribute($mac2, '-mac').'/singleValue',
        '-value', '44:44:44:44:44:44');
$ixNet->commit();

# print("\$ixNet->help ::ixNet::OBJ-/topology/deviceGroup/ethernet\n");
# print($ixNet->help ('::ixNet::OBJ-/topology/deviceGroup/ethernet'));
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

# print("\$ixNet->help ::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4\n)"
# print($ixNet->help ('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4'))"

#  Adding gRPC Client and configuring it in topology 1 
print("Adding gRPC Client and configuring it in topology\n");
$ixNet->add($ip1, 'gRPCClient');
$ixNet->commit();
my $gRPCClient = ($ixNet->getList($ip1, 'gRPCClient'))[0];

print ("Configuring remote ip and remote port in gRPC Client\n");
my $remoteIpMultiValue1 = ($ixNet->getAttribute($gRPCClient, '-remoteIp'));
$ixNet->setAttribute($remoteIpMultiValue1.'/singleValue', '-value', "20.20.20.1");
my $remotePortMultiValue1 = ($ixNet->getAttribute($gRPCClient, '-remotePort'));
$ixNet->setAttribute($remotePortMultiValue1.'/singleValue', '-value', "50001");
$ixNet->commit();

#  Adding gRIBI Client stack over gRPC Client in topology 1 
print("Adding gRIBI Client stack over gRPC Client in topology 1\n");
$ixNet->add($gRPCClient, 'gRIBIClient');
$ixNet->commit();
my $gRIBIClient = ($ixNet->getList($gRPCClient, 'gRIBIClient'))[0];

print("Configuring Client Redundancy and election IDs in gRIBI Client\n");
my $countMV1 = ($ixNet->getAttribute($gRIBIClient, '-count'));

my $clientRedundancyMultiValue1 = ($ixNet->getAttribute($gRIBIClient, '-clientRedundancy'));
$ixNet->setAttribute($clientRedundancyMultiValue1.'/singleValue', '-value', "singleprimary");

my $electionIdHighMultiValue1 = ($ixNet->getAttribute($gRIBIClient, '-electionIdHigh'));
$ixNet->setAttribute($electionIdHighMultiValue1.'/singleValue', '-value', "1001");

my $electionIdLowMultiValue1 = ($ixNet->getAttribute($gRIBIClient, '-electionIdLow'));
$ixNet->setAttribute($electionIdLowMultiValue1.'/singleValue', '-value', "2001");
$ixNet->commit();

#  Adding gRIBI Next Hop Stack over gRIBI Client in topology 1 
print("Adding gRIBI Next Hop Stack over gRIBI Client in topology 1\n");
$ixNet->add($gRIBIClient, 'gRIBINextHopGroup');
$ixNet->commit();
my $gRIBINextHopGroup = ($ixNet->getList($gRIBIClient, 'gRIBINextHopGroup'))[0];

$ixNet->setAttribute($gRIBINextHopGroup, '-multiplier', '5');
$ixNet->commit();

my $numberOfNextHopsMultiValue1 = ($ixNet->getAttribute($gRIBINextHopGroup, '-numberOfNextHops'));
$ixNet->setAttribute($gRIBINextHopGroup, '-numberOfNextHops', "3");
$ixNet->commit();

# Adding Network Topology behind Device Group
print("Adding the Network Topology\n");

$ixNet->execute('createDefaultStack', $gRIBINextHopGroup, 'ipv4PrefixPools');
my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
$ixNet->setAttribute($networkGroup1, '-name', "Network Group 1");
$ixNet->commit();

print("Configure metadata and Decapsulation Header type for gRIBI IPv4 entries\n");
my $ipv4PrefixPools = ($ixNet->getList($networkGroup1, 'ipv4PrefixPools'))[0];
my $gRIBIIpv4Entry = ($ixNet->getList($ipv4PrefixPools, 'gRIBIIpv4Entry'))[0];

my $metaDataMv1 = ($ixNet->getAttribute($gRIBIIpv4Entry, '-metaData'));
my $counter = ($ixNet->add($metaDataMv1, 'counter'));
$ixNet->setMultiAttribute($counter, '-direction', 'increment', '-start', "aabbccd1", '-step', "00000001");
$ixNet->commit();

my $decapsulationHeaderMv1 = ($ixNet->getAttribute($gRIBIIpv4Entry, '-decapsulationHeader'));
$ixNet->setAttribute($decapsulationHeaderMv1.'/singleValue', '-value', "ipv4");
$ixNet->commit();

################################################################################
# Configure gRIBI server on other port( topology 2) or run demo sever in the port
################################################################################
# To enable hw filters on ixia HW ports execute following command.
# filter --enable-all
#
# To enable hw filters on ixia VM ports execute following command.
# sudo /opt/Ixia/sstream/bin/filter --port=1 --enable-all
#
# To start demo server (ixia specific on server port execute following command.
#  <server_filename> -p <remote port>
# ./SyncServer -p 50051
#
# To start gribi_go_server (openconfig gribi server binary file on server port
#  execute following command.
#  <server_filename> -v -logtostderr -gRIBIPort <remote port>
# ./gribi_mips64 -v 5 -logtostderr -gRIBIPort 50051
#
################################################################################

###############################################################################
# 2. Start protocols and wait for 60 seconds
################################################################################
print("Wait for 5 seconds before starting protocols\n");
sleep(5);
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(30);

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

print("Fetching gRIBI Client Per Port Stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"gRIBI Client Per Port"/page';
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
# 4. Change following parameters in Next Hop Group 1 
#          Apply changes on the fly.
################################################################################
#---------------------------------------------------------------------------
#    - Color
#    - Backup Next Hop Group
#---------------------------------------------------------------------------

print("\n\nChange parameters in Next Hop Group 1 on-the-fly.....\n");

print("OTF change Color.....\n");
my $nhGroupMv = ($ixNet->getAttribute($gRIBINextHopGroup, '-color'));
$ixNet->setMultiAttribute($nhGroupMv, '-clearOverlays', 'false');
$ixNet->commit();

my $counter = $ixNet->add($nhGroupMv, "counter");
$ixNet->setMultiAttribute($counter, '-step', '5', '-start', '4001', '-direction', 'increment');
$ixNet->commit();
time.sleep(2);

print ("OTF change Backup Next Hop Group.....\n");
my $nhGroupMv = ($ixNet->getAttribute($gRIBINextHopGroup, '-backupNextHopGroup'));
$ixNet->setMultiAttribute($nhGroupMv, '-clearOverlays', 'false');
$ixNet->commit();

my $counter = ($ixNet->add($nhGroupMv, "counter"));
$ixNet->setMultiAttribute($counter, '-step', '101', '-start', '1', '-direction', 'increment');
$ixNet->commit();
time.sleep(2);

my $globalObj = ($ixNet->getRoot().'/globals');
my $topology  = $globalObj.'/topology';
print ("Applying changes on the fly\n");
try :
    $ixNet->execute('applyOnTheFly', $topology);
except :
    print("error in applying on the fly change");
# end try/expect
time.sleep(10);

################################################################################
# 5. Retreive protocol stats again 
################################################################################
#
print("Fetching gRIBI Client Per Port Stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"gRIBI Client Per Port"/page';
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
# 6. Stop all protocols
################################################################################
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!");

