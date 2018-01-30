
################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2016 by IXIA                                           # 
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    24/11/2016 - Anit Ghosal - created sample                                 #
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
#    This script intends to demonstrate how to use NGPF ISIS SR MS Perl API.   #
#                                                                              #
#    1. It will create 2 ISIS topologies, topology1 will have a simulated      #
#       topology Linear behind Device Group1 and Mesh behind Device Group2.    #
#    2. Enable Segment Routing in ISIS Emulated Router.                        #
#    3. Set SRGB range and SID Count for Emulated Router.                      #
#    4. Set IPV4 and IPV6 Ranges for both router acts as Mapping Server(MS)    #
#         and accordingly IPV4 & IPV6 Node Routes in Simulated Topologies.     #
#    5. Start Protocol And Retrieve protocol statistics.                       #
#    6. Retrieve protocol learned info in Port1.                               #
#    7. Retrieve protocol learned info in Port2.                               #
#    8. On the fly change SID Index value for IPv4 MS Ranges in Device Group1. #
#    9. On the fly Change IPV6 prefix in MS range and accordingly IPV6 address #
#        count of Node Routes in  Mesh Simulated Topology behind Device Group2.#  
#    10.On the fly Change in IPV6 FEC prefix in MS  and accordingly IPV6       #
#       address of Node Routes in Mesh Simulated Topology behind Device Group2.#
#    11. Retrieve protocol learned info in both ports after On the Fly changes.#
#    12. Configuring ISIS L2-L3 IPv4 & IPv6 Traffic Item for MS prefix ranges. #
#    13. Verifying all the L2-L3 traffic stats                                 #
#    14. Stop L2-L3 traffic.                                                   #
#    15. Stop all protocols.                                                   #
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
my $ixTclPort   = '8245';
my @ports       = (('10.216.108.99', '11', '1'), ('10.216.108.99', '11', '2'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '8.20',
    '-setAttribute', 'strict');

print("Creating a new config\n");
$ixNet->execute('newConfig');
################################################################################
# 1. Protocol configuration section. Configure ISIS as per the description
#  give above
################################################################################ 
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
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '100.0.0.1');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '100.0.0.2');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '100.0.0.2');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', "100.0.0.1");

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '24');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '24');

$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

# Adding ISIS over Ethernet stack
print("Add ISISL3\n");
$ixNet->add($mac1, 'isisL3');
$ixNet->add($mac2, 'isisL3');
$ixNet->commit();
my $isisL3_1 =($ixNet->getList( $mac1 ,'isisL3'))[0];
my $isisL3_2 =($ixNet->getList($mac2 ,'isisL3'))[0];
print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'ISIS Topology 1');
$ixNet->setAttribute($topo2, '-name', 'ISIS Topology 2');
$ixNet->commit();
$ixNet->setAttribute($t1dev1, '-name', 'ISIS Topology 1 Router');
$ixNet->setAttribute($t2dev1, '-name', 'ISIS Topology 2 Router');
$ixNet->commit();
my $isisL3Router1_1 = ($ixNet->getList($t1dev1, 'isisL3Router'));
my $isisL3Router2_1 = ($ixNet->getList($t2dev1, 'isisL3Router'));
$ixNet->commit();
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
print("Making the NetworkType to Point to Point in the ISIS router in Device Group1\n ");
my $networkTypeMultiValue1 = $ixNet->getAttribute($isisL3_1, '-networkType');
$ixNet->setMultiAttribute($networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($networkTypeMultiValue1.'/singleValue', '-value', 'pointpoint');

print("Making the NetworkType to Point to Point in the ISIS router in Device Group2\n" );
my $networkTypeMultiValue2 = $ixNet->getAttribute($isisL3_2, '-networkType');
$ixNet->setAttribute($networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setAttribute($networkTypeMultiValue2.'/singleValue', '-value', 'pointpoint');
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

$ixNet->commit();

print("Add Linear ST on the back of Device Group1");
my $networkGoup1 = $ixNet->add($t1dev1, 'networkGroup');
$ixNet->commit();
my $networkTopology1 = $ixNet->add($networkGoup1, 'networkTopology'); 
$ixNet->commit();
my $lineartopo = $ixNet->add($networkTopology1, 'netTopologyLinear');
$ixNet->commit();

print( "Add Mesh ST on the back of Device Group2 ");
my $networkGoup2 = $ixNet->add($t2dev1, 'networkGroup');

$ixNet->commit();
my $networkTopology2 = $ixNet->add($networkGoup2, 'networkTopology'); 
$ixNet->commit();
my $lineartopo = $ixNet->add($networkTopology2, 'netTopologyMesh');
$ixNet->commit();
#Setting Multiplier
$ixNet->setAttribute($networkGoup1, '-multiplier', '3');
$ixNet->setAttribute($networkGoup2, '-multiplier', '1');
$ixNet->commit();
$ixNet->setAttribute($networkGoup1, '-name', 'ISIS_Linear Topology 1');
$ixNet->setAttribute($networkGoup2, '-name', 'ISIS_Mesh Topology 2');
$ixNet->commit();
########################################################################################
# 2.Enabling Segment Routing in Emulated Router on Device Group 1 and Device Group 2 
########################################################################################
print ( "Enabling Segment Routing for ISIS");
$ixNet->setAttribute($isisL3Router1, '-enableSR', 'true');
$ixNet->setAttribute($isisL3Router2, '-enableSR', 'true');
$ixNet->commit();
################################################################################
# 3.Setting SRGB range and SID Count for Emulated Router
################################################################################
print ("Setting SRGB range and SID Count for Emulated Router\n");
print ("Setting SRGB range pool for first emulated router\n");
my $isisSRGBRangeSubObjectsList1 = ($ixNet->getList($isisL3Router1, 'isisSRGBRangeSubObjectsList'))[0];
my $startSIDLabel1 = $ixNet->getAttribute($isisSRGBRangeSubObjectsList1, '-startSIDLabel');
my $svsrgb1 = ($ixNet->getList($startSIDLabel1, 'singleValue'))[0];
$ixNet->setAttribute($svsrgb1, '-value', '15000');
$ixNet->commit();
my $sidCount1 = $ixNet->getAttribute($isisSRGBRangeSubObjectsList1, '-sIDCount');
my $sidcountsv1 = ($ixNet->getList($sidCount1, 'singleValue'))[0];
$ixNet->setAttribute($sidcountsv1, '-value', '100');
$ixNet->commit();
print ("Setting SRGB range pool for  Emulated Router Device Group2\n");
my $isisSRGBRangeSubObjectsList2 = ($ixNet->getList($isisL3Router2, 'isisSRGBRangeSubObjectsList'))[0];
my $startSIDLabel2 = $ixNet->getAttribute($isisSRGBRangeSubObjectsList2, '-startSIDLabel');
my $svsrgb2 = ($ixNet->getList($startSIDLabel2, 'singleValue'))[0];
$ixNet->setAttribute($svsrgb2, '-value', '10000');
$ixNet->commit();
my $sidCount2 = $ixNet->getAttribute($isisSRGBRangeSubObjectsList2, '-sIDCount');
my $sidcountsv2 = ($ixNet->getList($sidCount2, 'singleValue'))[0];
$ixNet->setAttribute($sidcountsv2, '-value', '100');
$ixNet->commit();
###########################################################################################################################################
# 4. Set IPV4 and IPV6 Ranges for both router acts as Mapping Server(MS)and accordingly IPV4 & IPV6 Node Routes in Simulated Topologies    
###########################################################################################################################################         
print ("Enabling IPV4  and IPV6 Node Routes Simulated Routers on Linear Network Group behind Device Group1\n");

my $networkTopo1 = ($ixNet->getList($networkGoup1, 'networkTopology'))[0];
my $simRouter1 = ($ixNet->getList($networkTopo1, 'simRouter'))[0];
$ixNet->commit();
my $isisPseudoRouter1 = ($ixNet->getList($simRouter1, 'isisL3PseudoRouter'))[0];
my $ipv4noderoutes = ($ixNet->getList($isisPseudoRouter1, 'IPv4PseudoNodeRoutes'))[0];
my $active = $ixNet->getAttribute( $ipv4noderoutes, '-active'); 
my $activesin = $ixNet->add($active, 'singleValue');
$ixNet->setAttribute($activesin, '-value', 'True');
$ixNet->commit();

my $ipv6noderoutes = ($ixNet->getList($isisPseudoRouter1, 'IPv6PseudoNodeRoutes'))[0];
my $active1 = $ixNet->getAttribute($ipv6noderoutes, '-active');
my $activesin1 = $ixNet->add($active1, 'singleValue');
$ixNet->setAttribute($activesin1, '-value', 'True');
$ixNet->commit();
print ( "Changing Prefix Length to 24\n");
my $prefixlen = $ixNet->getAttribute($ipv4noderoutes, '-prefixLength');
my $prefix = $ixNet->add($prefixlen, 'singleValue');
$ixNet->setAttribute($prefix, '-value', '24');
$ixNet->commit();
print ( "Changing Prefix Length to 24\n");
my $prefixlen = $ixNet->getAttribute($ipv4noderoutes, '-prefixLength');
my $prefix = $ixNet->add($prefixlen, 'singleValue');
$ixNet->setAttribute($prefix, '-value', '24');
$ixNet->commit();
print("Enabling IPV4  and IPV6 Node Routes Simulated Routers on Mesh Network Group behind Device Group2\n");
my $networkTopo2 = ($ixNet->getList($networkGoup2, 'networkTopology'))[0];
my $simRouter2 = ($ixNet->getList($networkTopo2, 'simRouter'))[0];
$ixNet->commit();
my $isisPseudoRouter2 = ($ixNet->getList($simRouter2, 'isisL3PseudoRouter'))[0];
my $ipv4noderoutes2 = ($ixNet->getList($isisPseudoRouter2, 'IPv4PseudoNodeRoutes'))[0];
my $active2 = $ixNet->getAttribute( $ipv4noderoutes2, '-active'); 
my $activesin2 = $ixNet->add($active2 , 'singleValue');
$ixNet->setAttribute($activesin2,' -value', 'True');
$ixNet->commit();
my $ipv6noderoutes2 = ($ixNet->getList($isisPseudoRouter2, 'IPv6PseudoNodeRoutes'))[0];
my $active2 = $ixNet->getAttribute( $ipv4noderoutes2, '-active');
my $activesin2 = $ixNet->add($active2 , 'singleValue');
$ixNet->setAttribute($activesin2,' -value', 'True');
$ixNet->commit();
print ( "Changing Prefix Length to 24\n");
my $prefixlen2 = $ixNet->getAttribute($ipv4noderoutes2, '-prefixLength');
my $prefix2 = $ixNet->add($prefixlen2, 'singleValue');
$ixNet->setAttribute($prefix2, '-value', '24');
$ixNet->commit();
print( "Enabling Mapping Server on  Emulated Router in Device Group 1  and Setting No. of IPV4 and IPV6 Mapping Ranges\n");
my $enablems1 = $ixNet->getAttribute($t1dev1.'/isisL3Router:1', '-enableMappingServer');
my $single =$ixNet->add($enablems1, 'singleValue');
$ixNet->setMultiAttribute($single, '-value', 'true');
$ixNet->commit();

$ixNet->setMultiAttribute($t1dev1.'/isisL3Router:1',
            '-enableSR', 'true',
            '-numberOfMappingIPV4Ranges', '3',
            '-numberOfMappingIPV6Ranges', '3',);
$ixNet->commit();

print( "Enabling Mapping Server on  Emulated Router in Device Group 2  and Setting No. of IPV4 and IPV6 Mapping Ranges\n");
my $enablems2 = $ixNet->getAttribute($t2dev1.'/isisL3Router:1', '-enableMappingServer');
my $single =$ixNet->add($enablems2, 'singleValue');
$ixNet->setMultiAttribute($single, '-value', 'true');
$ixNet->commit();

$ixNet->setMultiAttribute($t2dev1.'/isisL3Router:1',
            '-enableSR', 'true',
            '-numberOfMappingIPV4Ranges', '3',
            '-numberOfMappingIPV6Ranges', '3',);
$ixNet->commit();

print( "Setting Mapping Server IPV4 FEC Prefix ranges For Emulated Router1 in Device Group1\n" );
my $isisvmsppingserverv4 = ($ixNet->getList($isisL3Router1, 'isisMappingServerIPV4List'))[0];
my $fecprefix = $ixNet->getAttribute($isisvmsppingserverv4, '-fECPrefix');
$ixNet->commit();
my $counter = $ixNet->add($fecprefix, 'counter');
$ixNet->setMultiAttribute($counter,
            '-step', '0.1.0.0',
            '-start', '201.1.0.0',
            '-direction', 'increment');
$ixNet->commit();
print("Setting Mapping Server IPV6 FEC Prefix ranges For Emulated Router1 in Device Group1\n");
my $isisvmsppingserverv6 = ($ixNet->getList($isisL3Router1, 'isisMappingServerIPV6List'))[0];
my $fecprefix = $ixNet->getAttribute($isisvmsppingserverv6, '-fECPrefix');
$ixNet->commit();
my $counter1 = $ixNet->add($fecprefix, 'counter');
$ixNet->setMultiAttribute($counter1,
            '-step', '0:0:0:1:0:0:0:0',
            '-start', '3000:0:1:1:0:0:0:0',
            '-direction', 'increment');
$ixNet->commit();

print("Setting Mapping Server IPV4 FEC Prefix ranges For Emulated Router2 in Device Group2\n");
my $isisvmsppingserverv4 = ($ixNet->getList($isisL3Router2, 'isisMappingServerIPV4List'))[0];
my $fecprefix = $ixNet->getAttribute($isisvmsppingserverv4, '-fECPrefix');
$ixNet->commit();
my $counter = $ixNet->add($fecprefix, 'counter');
$ixNet->setMultiAttribute($counter,
            '-step', '0.1.0.0',
            '-start', '202.1.0.0',
            '-direction', 'increment');
$ixNet->commit();


print("Setting Mapping Server IPV6 FEC Prefix ranges For Emulated Router1 in Device Group2\n");
my $isisvmsppingserverv6 = ($ixNet->getList($isisL3Router2, 'isisMappingServerIPV6List'))[0];
my $fecprefix = $ixNet->getAttribute($isisvmsppingserverv6, '-fECPrefix');
$ixNet->commit();
my $counter1 = $ixNet->add($fecprefix, 'counter');
$ixNet->setMultiAttribute($counter1,
            '-step', '0:0:0:1:0:0:0:0',
            '-start', '3000:1:1:1:0:0:0:0',
            '-direction', 'increment');
$ixNet->commit();
######################################################################################
# 5. Start ISIS protocol and wait for 60 seconds And  Retrieve protocol statistics.
######################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);
###############################################################################
# 6. Retrieve protocol learned info in Port 1
###############################################################################
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
# 6. Retrieve protocol learned info in Port 1
###############################################################################
print("Fetching ISIS IPv4 & IPv6 Learned Info of Device Group1 Topology1 Emulated Router  for Proper Prefix-Label Binding in Port1\n");
$ixNet->execute('getLearnedInfo', $isisL3_1, '1');
sleep(5);
my $linfo = ($ixNet->getList($isisL3_1, 'learnedInfo'))[0];
my $ipv6table = ($ixNet->getList($linfo, 'table'))[0];
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

$ixNet->execute('getLearnedInfo', $isisL3_1, '1');
sleep(5);
my $linfo = ($ixNet->getList($isisL3_1, 'learnedInfo'))[0];
my $ipv6table = ($ixNet->getList($linfo, 'table'))[1];
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
###############################################################################
# 7. Retrieve protocol learned info in Port 2
###############################################################################
print("9155783\n");
$ixNet->execute('getLearnedInfo', $isisL3_2, '1');
sleep(5);
my $linfo = ($ixNet->getList($isisL3_2, 'learnedInfo'))[0];
my $ipv6table = ($ixNet->getList($linfo, 'table'))[0];
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

$ixNet->execute('getLearnedInfo', $isisL3_2, '1');
sleep(5);
my $linfo = ($ixNet->getList($isisL3_2, 'learnedInfo'))[0];
my $ipv6table = ($ixNet->getList($linfo, 'table'))[1];
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
###############################################################################
# 8. OTF on SID value
###############################################################################
print("OTF on Device Group1  in Topology1 IPV4 MS SID value ");
my $isisvmsppingserverv4 = ($ixNet->getList($isisL3Router1, 'isisMappingServerIPV4List'))[0];
my $newsid11 = $ixNet->getAttribute($isisvmsppingserverv4, '-startSIDLabel');
my $overlay61 = $ixNet->add($newsid11, 'overlay');
$ixNet->setMultiAttribute($overlay61, '-index', '1', '-value', '10');
$ixNet->commit();
#######################################################################################################
# 9. OTF on  Address  Of Mapping Server  IPV6 and Simulated Topology  And Apply Changes
######################################################################################################
print("OTF on Device Group 2 Topology 1 Address Field\n");
my $isisvmsppingserverv6 = ($ixNet->getList($isisL3Router2, 'isisMappingServerIPV6List'))[0]; 
my $fecprefix = $ixNet->getAttribute($isisvmsppingserverv6, '-fECPrefix');
my $overlay10 = $ixNet->add($fecprefix, 'overlay');
$ixNet->setMultiAttribute($overlay10, '-count', '1', '-index', '2', '-value', '3000:4:1:2:0:0:0:0');
$ixNet->commit();

my $v6noderoutes = $ixNet->getAttribute($ipv6noderoutes2, '-networkAddress');
my $overlay = $ixNet->add($v6noderoutes, 'overlay');
$ixNet->setMultiAttribute($overlay, '-count', '1', '-index', '2', '-value', '3000:4:1:2:0:0:0:0');
$ixNet->commit();

my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
print("Wait for 30 seconds ...\n");
sleep(30);
#######################################################################################################
# 10. OTF on Range  Of  Mapping Server  IPV6 and Simulated Topology  also And Apply Changes
######################################################################################################
print("OTF on Device Group2 Topology2 IPV6 MS range and  also in ST \n");
my $range = $ixNet->getAttribute($ipv6noderoutes2, '-rangeSize');
my $overlay1 = $ixNet->add($range, 'overlay');
$ixNet->setMultiAttribute($overlay1, '-count', '1', '-index', '1', '-value', '4');
$ixNet->commit();

my $range1 = $ixNet->getAttribute($isisvmsppingserverv6, '-range');
my $overlay11 = $ixNet->add($range1, 'overlay');
$ixNet->setMultiAttribute($overlay11, '-count', '1', '-index', '1', '-value', '4');
$ixNet->commit();

my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
print("Wait for 30 seconds ...\n");
sleep(30);
###############################################################################
# 11 . Retrieve protocol learned info in Both Port 
###############################################################################
print("Fetching ISIS IPv4 & IPv6 Learned Info of Device Group1 Topology1 Emulated Router  for Proper Prefix-Label Binding in Port1\n");
$ixNet->execute('getLearnedInfo', $isisL3_1, '1');
sleep(5);
my $linfo = ($ixNet->getList($isisL3_1, 'learnedInfo'))[0];
my $ipv6table = ($ixNet->getList($linfo, 'table'))[0];
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

$ixNet->execute('getLearnedInfo', $isisL3_1, '1');
sleep(5);
my $linfo = ($ixNet->getList($isisL3_1, 'learnedInfo'))[0];
my $ipv6table = ($ixNet->getList($linfo, 'table'))[1];
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

$ixNet->execute('getLearnedInfo', $isisL3_2, '1');
sleep(5);
my $linfo = ($ixNet->getList($isisL3_2, 'learnedInfo'))[0];
my $ipv6table = ($ixNet->getList($linfo, 'table'))[0];
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

$ixNet->execute('getLearnedInfo', $isisL3_2, '1');
sleep(5);
my $linfo = ($ixNet->getList($isisL3_2, 'learnedInfo'))[0];
my $ipv6table = ($ixNet->getList($linfo, 'table'))[1];
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
# 12. Configure L2-L3 traffic 
################################################################################

print ("Congfigure L2-L3 Traffic Item\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'IPv4_MPLS_Traffic_Item_1',
    '-roundRobinPacketOrdering', 'false',
    '-biDirectional', 'true',
    '-useControlPlaneRate', 'true',
    '-useControlPlaneFrameSize', 'true',
    '-mergeDestinations', 'false',
    '-roundRobinPacketOrdering', 'false', 
    '-numVlansForMulticastReplication', '1',
    '-trafficType', 'ipv4');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');

my @source       = ($networkGoup1.'/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv4PseudoNodeRoutes:1');
my @destination  = ($networkGoup2.'/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv4PseudoNodeRoutes:1');

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
    '-trackBy',        ['sourceDestValuePair0', 'trackingenabled0', 'mplsMplsLabelValue0', 'ipv4DestIp0', 'ipv4SourceIp0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();
print("Configuring  L2-L3 IPv6 Traffic Item # 2\n");
print ("Configuring traffic item 2 with endpoints src :isisPseudoNodeRoutes IPV6 & dst :isisPseudoNodeRoutes IPV6\n");
my $trafficItem2 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem2, '-name', 'IPv6_MPLS_Traffic_Item_1',
    '-roundRobinPacketOrdering', 'false',
    '-biDirectional', 'true',
    '-useControlPlaneRate', 'true',
    '-useControlPlaneFrameSize', 'true',
    '-mergeDestinations', 'false',
    '-roundRobinPacketOrdering', 'false', 
    '-numVlansForMulticastReplication', '1',
    '-trafficType', 'ipv6');
$ixNet->commit();

$trafficItem2 = ($ixNet->remapIds($trafficItem2))[0];
my $endpointSet2 = $ixNet->add($trafficItem2, 'endpointSet');

my @source       = ($networkGoup1.'/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1');
my @destination  = ($networkGoup2.'/networkTopology/simRouter:1/isisL3PseudoRouter:1/IPv6PseudoNodeRoutes:1');

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

$ixNet->setMultiAttribute($trafficItem2.'/tracking',
    '-trackBy',        ['sourceDestValuePair0', 'trackingenabled0', 'mplsMplsLabelValue0', 'ipv6DestIp0', 'ipv6SourceIp0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();
###############################################################################
#13 Apply and start L2/L3 traffic and Retrieve L2/L3 traffic item statistics  #                                              
###############################################################################
print("Applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');
print("Print all the L2-L3 traffic flow stats\n");
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
#14 Stop L2/L3 traffic                                                            #
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');
sleep(5);
################################################################################
#15 Stop all protocols                                                           #
################################################################################
print ("Stop All Protocols\n");
$ixNet->execute('stopAllProtocols');
print("Sample Script Ends");
