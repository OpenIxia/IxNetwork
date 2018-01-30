################################################################################
# Version 1.0    $Revision: #1 $                                               #
#                                                                              #
#    Copyright  1997 - 2016 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    23/11/2016 - Shilpam Sinha - created sample                          #
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
##    This script intends to demonstrate how to use NGPF ISIS Link Protection-  #
##    SRLG - Perl API                                                            #
##                                                                              #
##    1. It will create 2 ISIS topologies, topology1 will have a simulated      #
##       topology Linear behind Device Group1 and Mesh behind Device Group2     #
##    2. Enable Shared Risk Link Group(SRLG) in ISIS Emulated                   #
##       Router in both Device Group.                                           # 
##    3. Give SRLG count 2 with value 5 and 6 for ISIS Emulated router          #
##       Router in both Device Group.                                           #
##    4. Give SRLG count 1 with value 10 for all ISIS simulated routers         #
##       Router behind Device Group1 & with value 15 for all ISIS simulated     #
##       routers Router behind Device Group2 .                                  #
##    5. Enable Link Protection in ISIS Emulated Router in both Device Group    #
##    6. Give Link Protection type Of Extra traffic,Unprotected and Dedicated   # 
##       :true for emulated Router in both device group.                        #
##    7. Give Link Protection type Of Dedicated 1:1 and shared:true for all     #
##       simulated Router behind  both device group.                            #
##    8. Start protocol.                                                        #
##    9. Retrieve protocol statistics.                                          #
##    10. On the fly uncheck "Enable SRLG"  emulated router in Device group2 &  #
##        check  "Enable SRLG" for all simulated Routers behind device group1   #
##    11. On the fly do change on Link type i.e  make enhanced:true and         #
##       unprotected:false for emulated router in Device group1 & disable"Enable# 
##       Link Protection" for first 2 simulated Routers behind device group2    #
##                                                                              #
##    12. Stop all protocols.                                                   #
##                                                                              #
## Ixia Softwares:                                                              #
##    IxOS      8.20 EA                                                         #
##    IxNetwork 8.20 EA                                                         #
##                                                                              #
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

################################################################################
#  Protocol configuration section. Configure ISIS as per the description
#  give above
################################################################################ 
# Adding Virtual ports
print("Adding 2 vports\n");
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->commit();

my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vportTx = $vPorts[0];
my $vportRx = $vPorts[1];

print("Assigning the ports\n");
assignPorts($ixNet, @ports, $vportTx, $vportRx);
sleep(5);

# Adding Topologies
print("Adding 2 topologies\n");
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', $vportTx);
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', $vportRx);
$ixNet->commit();

my @topologies = $ixNet->getList($ixNet->getRoot(), 'topology');
my $topo1 = $topologies[0];
my $topo2 = $topologies[1];

# Adding Device Groups
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

# Adding Ethernet
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

# Add IPv4 Stack
print("Add ipv4 over Ethernet stack\n");
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
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '100.0.0.1');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '100.0.0.2');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '100.0.0.2');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', '100.0.0.1');

$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '24');
$ixNet->setAttribute($ixNet->getAttribute($ip2, '-prefix').'/singleValue', '-value', '24');

# Add IPv6 Stack
print("Add ipv6 over Ethernet stack\n");
$ixNet->add($mac1, 'ipv6');
$ixNet->add($mac2, 'ipv6');
$ixNet->commit();

my $ip3 = ($ixNet->getList($mac1, 'ipv6'))[0];
my $ip4 = ($ixNet->getList($mac2, 'ipv6'))[0];

my $mvAdd1 = $ixNet->getAttribute($ip3, '-address');
my $mvAdd2 = $ixNet->getAttribute($ip4, '-address');
my $mvGw1  = $ixNet->getAttribute($ip3, '-gatewayIp');
my $mvGw2  = $ixNet->getAttribute($ip4, '-gatewayIp');

print("configuring ipv6 addresses");
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '2000:0:0:1:0:0:0:2');
$ixNet->setAttribute($mvAdd2.'/singleValue', '-value', '2000:0:0:1:0:0:0:1');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '2000:0:0:1:0:0:0:1');
$ixNet->setAttribute($mvGw2.'/singleValue', '-value', '2000:0:0:1:0:0:0:2');

$ixNet->setAttribute($ixNet->getAttribute($ip3, '-prefix').'/singleValue', '-value', '64');
$ixNet->setAttribute($ixNet->getAttribute($ip4, '-prefix').'/singleValue', '-value', '64');

# Adding ISIS over Ethernet stack
print("Adding ISISL3 over Ethernet stacks");
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

# Enable host name in ISIS router1
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

print("Making the NetworkType to Point to Point in the first ISISrouter\n");
my $networkTypeMultiValue1 = ($ixNet->getAttribute($isisL3_1, '-networkType'));
$ixNet->setMultiAttribute($networkTypeMultiValue1, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($networkTypeMultiValue1.'/singleValue', '-value', 'pointpoint');

print("Making the NetworkType to Point to Point in the Second ISIS router\n");
my $networkTypeMultiValue2 = ($ixNet->getAttribute($isisL3_2, '-networkType'));
$ixNet->setAttribute($networkTypeMultiValue2, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setAttribute($networkTypeMultiValue2.'/singleValue', '-value', 'pointpoint');

# Disable Discard Learned LSP 
print("Disabling the Discard Learned Info CheckBox\n");
my $isisL3RouterDiscardLearnedLSP1 = $ixNet->getAttribute(($ixNet->getList($t1devices[0], 'isisL3Router'))[0],'-discardLSPs');
my $isisL3RouterDiscardLearnedLSP2 = $ixNet->getAttribute(($ixNet->getList($t2devices[0], 'isisL3Router'))[0],'-discardLSPs');

$ixNet->setAttribute($isisL3RouterDiscardLearnedLSP1,'-pattern', 'singleValue','-clearOverlays', 'False');
$ixNet->setAttribute($isisL3RouterDiscardLearnedLSP1.'/singleValue', '-value', 'false');
$ixNet->setAttribute($isisL3RouterDiscardLearnedLSP2,'-pattern', 'singleValue','-clearOverlays', 'False');
$ixNet->setAttribute($isisL3RouterDiscardLearnedLSP2.'/singleValue', '-value', 'false');

# Adding Network group behind DeviceGroup
print("Adding NetworkGroup behind ISIS DG\n");
$ixNet->execute('createDefaultStack', $t1dev1, 'networkTopology');
my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
my $networkTopology1 = ($ixNet->getList($networkGroup1, 'networkTopology'))[0];
$ixNet->add($networkTopology1, 'netTopologyLinear');
my $linearTopo =  ($ixNet->getList($networkTopology1, 'netTopologyLinear'))[0];
$ixNet->setAttribute($networkGroup1, '-multiplier', '3','-name', 'ISIS_Linear Topology 1');
$ixNet->commit();

$ixNet->execute('createDefaultStack', $t2dev1, 'networkTopology');
my $networkGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];
my $networkTopology2 = ($ixNet->getList($networkGroup2, 'networkTopology'))[0];
$ixNet->add($networkTopology2, 'netTopologyMesh');
my $meshTopo =  ($ixNet->getList($networkTopology2, 'netTopologyMesh'))[0];
$ixNet->setAttribute($networkGroup2, '-multiplier', '1','-name', 'ISIS_Mesh Topology 1');
$ixNet->commit();

###############################################################################
## Enable SRLG in Both emulated Router 
################################################################################

print("Enabling SRLG in emulated router in both device group\n");

#For DG1
my $enableSrlg1 = ($ixNet->getAttribute($isisL3_1, '-enableSRLG')); 
$ixNet->setAttribute($enableSrlg1.'/singleValue', '-value', 'True');
$ixNet->commit();

#For DG2
my $enableSrlg2 = ($ixNet->getAttribute($isisL3_2, '-enableSRLG'));
$ixNet->setAttribute($enableSrlg2.'/singleValue', '-value', 'True');
$ixNet->commit();

##########################################################################################################
##  Give SRLG count to 2 and SRLG value to 5 and 6 for ISIS Emulated  Router in both Device Group      
###########################################################################################################       

print("Setting SRLG count to 2 and SRLG Value to 5 and 6 in emulated router in both Device Group\n");

#For DG1
$ixNet->setAttribute($isisL3_1, '-srlgCount', '2');
$ixNet->commit();
my $srlgValueList1 = ($ixNet->getList($isisL3_1, 'srlgValueList'))[0];
my $srlgValue = ($ixNet->getAttribute($srlgValueList1, '-srlgValue'));
$ixNet->setAttribute($srlgValue.'/singleValue', '-value', '5');
my $srlgValueList2 = ($ixNet->getList($isisL3_1, 'srlgValueList'))[1];
my $srlgValue = ($ixNet->getAttribute($srlgValueList2, '-srlgValue'));
$ixNet->setAttribute($srlgValue.'/singleValue', '-value', '6');
$ixNet->commit();

#For DG2
$ixNet->setAttribute($isisL3_2, '-srlgCount', '2');
$ixNet->commit();
my $srlgValueList1 = ($ixNet->getList($isisL3_2, 'srlgValueList'))[0];
my $srlgValue = ($ixNet->getAttribute($srlgValueList1, '-srlgValue'));
$ixNet->setAttribute($srlgValue.'/singleValue', '-value', '5');
my $srlgValueList2 = ($ixNet->getList($isisL3_2, 'srlgValueList'))[1];
my $srlgValue = ($ixNet->getAttribute($srlgValueList2, '-srlgValue'));
$ixNet->setAttribute($srlgValue.'/singleValue', '-value', '6');
$ixNet->commit();

#############################################################################################
##Setting SRLG Value for both Simulated router as described above
##############################################################################################

print("Setting SRLG value to 10 for Simulated routers behind Device Group1\n");

my $simInterface = ($ixNet->getList($networkTopology1, 'simInterface'))[0];
my $isisL3PseudoInterface_Linear = ($ixNet->getList($simInterface, 'isisL3PseudoInterface'))[0];
$ixNet->commit();

my $enableSrlg_Linear = ($ixNet->getAttribute($isisL3PseudoInterface_Linear, '-enableSRLG'));
$ixNet->setAttribute($enableSrlg_Linear.'/singleValue', '-value', 'True');
$ixNet->commit();

my $srlgValueList1 = ($ixNet->getList($isisL3PseudoInterface_Linear, 'srlgValueList'))[0];
my $srlgValue = ($ixNet->getAttribute($srlgValueList1, '-srlgValue'));
$ixNet->setAttribute($srlgValue.'/singleValue', '-value', '10');
$ixNet->commit();

my $enableSrlg_Linear = ($ixNet->getAttribute($isisL3PseudoInterface_Linear, '-enableSRLG'));
$ixNet->setAttribute($enableSrlg_Linear.'/singleValue', '-value', 'False');
$ixNet->commit();

print("Setting SRLG value to 15 for Simulated routers behind Device Group2\n");

my $simInterface = ($ixNet->getList($networkTopology2, 'simInterface'))[0];
my $isisL3PseudoInterface_Mesh = ($ixNet->getList($simInterface, 'isisL3PseudoInterface'))[0];
$ixNet->commit();

my $enableSrlg_Mesh = ($ixNet->getAttribute($isisL3PseudoInterface_Mesh, '-enableSRLG'));
$ixNet->setAttribute($enableSrlg_Mesh.'/singleValue', '-value', 'True');
$ixNet->commit();

my $srlgValueList2 = ($ixNet->getList($isisL3PseudoInterface_Mesh, 'srlgValueList'))[0];
my $srlgValue = ($ixNet->getAttribute($srlgValueList2, '-srlgValue'));
$ixNet->setAttribute($srlgValue.'/singleValue', '-value', '15');
$ixNet->commit();

#############################################################################################
## Enable Link Protection in Emulated Router in Both Device Group
##############################################################################################

print("Enable Link Protection on Emulated Router For Device Group 1\n");

#For DG1
my $enableLP1 = ($ixNet->getAttribute($isisL3_1, '-enableLinkProtection'));
$ixNet->setAttribute($enableLP1.'/singleValue', '-value', 'True');
$ixNet->commit();

##For DG2
my $enableLP2 = ($ixNet->getAttribute($isisL3_2, '-enableLinkProtection'));
$ixNet->setAttribute($enableLP2.'/singleValue', '-value', 'True');
$ixNet->commit();

##############################################################################################
## 6.Setting Link Protection type as Described above For Emulated Router
###############################################################################################

print("Enable Extratraffic ----- unprotected ----- dedicatedoneplusone  For Emulated Router 1\n");

my $extraTraffic = ($ixNet->getAttribute($isisL3_1, '-extraTraffic'));
$ixNet->setAttribute($extraTraffic.'/singleValue', '-value', 'True');
$ixNet->commit();

my $unprotected = ($ixNet->getAttribute($isisL3_1, '-unprotected'));
$ixNet->setAttribute($unprotected.'/singleValue', '-value', 'True');
$ixNet->commit();

my $dedicatedOnePlusOne = ($ixNet->getAttribute($isisL3_1, '-dedicatedOnePlusOne'));
$ixNet->setAttribute($dedicatedOnePlusOne.'/singleValue', '-value', 'True');
$ixNet->commit();

print("Enable Extratraffic ----- unprotected ----- dedicatedoneplusone  For Emulated Router 2\n");

my $extraTraffic = ($ixNet->getAttribute($isisL3_2, '-extraTraffic'));
$ixNet->setAttribute($extraTraffic.'/singleValue', '-value', 'True');
$ixNet->commit();

my $unprotected = ($ixNet->getAttribute($isisL3_2, '-unprotected'));
$ixNet->setAttribute($unprotected.'/singleValue', '-value', 'True');
$ixNet->commit();

my $dedicatedOnePlusOne = ($ixNet->getAttribute($isisL3_2, '-dedicatedOnePlusOne'));
$ixNet->setAttribute($dedicatedOnePlusOne.'/singleValue', '-value', 'True');
$ixNet->commit();

################################################################################
## 7. Setting Link Protection Type For Simulated Router as Described above
#################################################################################

print("Enable Link Protection For Simulated Routers Behind Device Group 1\n");
my $enableLP1 = ($ixNet->getAttribute($isisL3PseudoInterface_Linear, '-enableLinkProtection'));
$ixNet->setAttribute($enableLP1.'/singleValue', '-value', 'True');
$ixNet->commit();

#Make true to DedicatedonePlusOne field
print("Making DedicatedonePlusOne And Shared Link Protection Type to True\n");
my $dedicatedOnePlusOne = ($ixNet->getAttribute($isisL3PseudoInterface_Linear, '-dedicatedOnePlusOne'));
$ixNet->setAttribute($dedicatedOnePlusOne.'/singleValue', '-value', 'True');
$ixNet->commit();

#Make true to Shared field
my $shared = ($ixNet->getAttribute($isisL3PseudoInterface_Linear, '-shared'));
$ixNet->setAttribute($shared.'/singleValue', '-value', 'True');
$ixNet->commit();

print("Enable Link Protection For Simulated Routers Behind Device Group 2\n");
my $enableLP2 = ($ixNet->getAttribute($isisL3PseudoInterface_Mesh, '-enableLinkProtection'));
$ixNet->setAttribute($enableLP2.'/singleValue', '-value', 'True');
$ixNet->commit();

#Make true to DedicatedonePlusOne field
print("Making DedicatedonePlusOne And Shared Link Protection Type to True\n");
my $dedicatedOnePlusOne = ($ixNet->getAttribute($isisL3PseudoInterface_Mesh, '-dedicatedOnePlusOne'));
$ixNet->setAttribute($dedicatedOnePlusOne.'/singleValue', '-value', 'True');
$ixNet->commit();

##Make true to Shared field
my $shared = ($ixNet->getAttribute($isisL3PseudoInterface_Mesh, '-shared'));
$ixNet->setAttribute($shared.'/singleValue', '-value', 'True');
$ixNet->commit();

################################################################################
# Start ISIS protocol and wait for 60 seconds
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);

################################################################################
# Retrieve protocol statistics
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
# OTF on SRLG
################################################################################

print("Performing OTF on SRLG\n");
print("Disabling SRLG for DG1\n");
my $enableSrlg1 = ($ixNet->getAttribute($isisL3_1, '-enableSRLG'));
$ixNet->setAttribute($enableSrlg1.'/singleValue', '-value', 'False');
$ixNet->commit();

print("Enabling SRLG for Linear ST behind DG1\n");
my $enableSrlg_Linear = ($ixNet->getAttribute($isisL3PseudoInterface_Linear, '-enableSRLG'));
$ixNet->setAttribute($enableSrlg_Linear.'/singleValue', '-value', 'True');
$ixNet->commit();

my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
print("Wait for 30 seconds ...\n");
sleep(30);

################################################################################
## OTF on Link Protection
#################################################################################

print("Performing OTF on Link Protection\n");
print("\nDisabling unprotected field of DG1");
my $unprotected = ($ixNet->getAttribute($isisL3_1, '-unprotected'));
$ixNet->setAttribute($unprotected.'/singleValue', '-value', 'False');
$ixNet->commit();

print("\nEnabling enhanced field of DG1");
my $enhanced = ($ixNet->getAttribute($isisL3_1, '-enhanced'));
$ixNet->setAttribute($enhanced.'/singleValue', '-value', 'True');
$ixNet->commit();

print("\nDisabling one of the Link Protection for Mesh ST behind DG2\n");
my $enableLP1 = ($ixNet->getAttribute($isisL3PseudoInterface_Mesh, '-enableLinkProtection'));
my $OverlayLP = $ixNet->add($enableLP1, 'overlay');
$ixNet->setAttribute($OverlayLP,'-index', '2', '-value', 'False');
$ixNet->commit();

my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
print("Wait for 30 seconds ...\n");
sleep(30);

################################################################################
# Stop all protocols
################################################################################
print("Stopping All Protocols\n");
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!\n");

