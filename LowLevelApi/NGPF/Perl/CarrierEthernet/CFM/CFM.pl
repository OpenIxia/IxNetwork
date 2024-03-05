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

#################################################################################
#                                                                               #
# Description:                                                                  #
#    This script intends to demonstrate how to use NGPF CFM PERL API.           #
#    About Topology:                                                            #
#      Hub & Spoke topology is configured on 2 Ixia Ports. Each Hub & Spoke     #
#    topology consists of one emulated CFM MP (hub) and 3 simulated CFM MPs     #
#    (spoke).                                                                   #
#    Script Flow:                                                               #
#       Step 1. Configuration of protocols.                                     #
#            i.   Adding CFM emulated MP(emulated device group.)                #
#            ii.  Adding CFM Simulated Topology behind Emulated Device Group.   #
#            iii. Configuring simulated topology type as Hub & Spoke using      #
#                 CFM Network Group Wizard.                                     #
#            iv.  Changing Simulated topology connector to CFM stack.           #
#            v.   Configuring MD level and MA parameters in Simulated topology  #
#                 using CFM Network Group wizard.                               #
#            vi.  Execute configMDLevels command after setting required MD level#
#                 parameters.                                                   #
#        Step 2. Start of protocol                                              #
#        Step 3. Protocol Statistics display                                    #
#        Step 4. Learned Info display   (Continuity Check messages,             #
#                Loopback messages and Link Trace mesages)                      #
#        Step 5. On The Fly(OTF) change of protocol parameter.                  #
#                (OTF Stop CCM in emulated MP and Apply changes on the fly.)    #
#        Step 6. Again statistics display to see OTF changes took place         #
#        Step 7. Configuration L2-L3 Traffic                                    #
#        Step 8. Apply and Start of L2-L3 traffic                               #
#        Step 9. Display of L2-L3  traffic Stats                                #
#        Step 10.Stop of L2-L3 traffic                                          #
#        Step 11.Stop of all protocols                                          #
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
my $ixTclServer = '10.39.50.134';
my $ixTclPort   = '8039';
my @ports       = (('10.39.43.154', '3', '9'), ('10.39.43.154', '3', '10'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '9.10',
    '-setAttribute', 'strict');
print("Creating a new config\n");
$ixNet->execute('newConfig');
#################################################################################
# Step 1> protocol configuration section
#################################################################################
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

# Creating topology and device group
my @topologies = $ixNet->getList($ixNet->getRoot(), 'topology');
my $topo1 = $topologies[0];
my $topo2 = $topologies[1];

print("Adding 2 device groups\n");
$ixNet->add($topo1, 'deviceGroup');
$ixNet->add($topo2, 'deviceGroup');
$ixNet->commit();

my @t1devices = $ixNet->getList($topo1, 'deviceGroup');
my @t2devices = $ixNet->getList($topo2, 'deviceGroup');
print("Renaming the topologies and the device groups");
$ixNet->setAttribute($topo1,  '-name', 'CFM Topology 1');
$ixNet->setAttribute($topo2,  '-name', 'CFM Topology 2');
$ixNet->commit();
my $t1dev1 = $t1devices[0];
my $t2dev1 = $t2devices[0];
$ixNet->setAttribute($t1dev1, '-name', 'Emulated MP 1');
$ixNet->setAttribute($t2dev1, '-name', 'Emulated MP 2');
$ixNet->commit();

print("Configuring the multipliers (number of sessions)\n");
$ixNet->setAttribute($t1dev1, '-multiplier', '1');
$ixNet->setAttribute($t2dev1, '-multiplier', '1');
$ixNet->commit();

#  Adding ethernet stack and configuring MAC

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

#  Adding CFM protocol stack and configuring it
print("\n\nAdding CFM emulated MP over Ethernet stack\n");
$ixNet->add($mac1, 'cfmBridge');
$ixNet->add($mac2, 'cfmBridge');
$ixNet->commit();

my $cfmBridge1 = ($ixNet->getList($mac1, 'cfmBridge'))[0];
my $cfmBridge2 = ($ixNet->getList($mac2, 'cfmBridge'))[0];
my $cfmMp1 = ($ixNet->getList($cfmBridge1, 'cfmMp'))[0];
my $cfmMp2 = ($ixNet->getList($cfmBridge2, 'cfmMp'))[0];

# Adding CFM Simulated Topology behind Emulated Device Group
print("\n\nAdding CFM Simulated Topology\n");

my $addNetworkGroup1 = ($ixNet->add($t1dev1, 'networkGroup'))[0];
my $addNetworkGroup2 = ($ixNet->add($t2dev1, 'networkGroup'))[0];
$ixNet->commit();

my $addNetworkTopology1 = ($ixNet->add($addNetworkGroup1, 'networkTopology'))[0];
my $addNetworkTopology2 = ($ixNet->add($addNetworkGroup2, 'networkTopology'))[0];
$ixNet->commit();

# Configuring simulated topology type as Hub & Spoke using CFM Network Group Wizard
print("\n\nConfiguring simulated topology type as Hub & Spoke using CFM Network Group Wizard\n");

my $addHubnSpoke1 = ($ixNet->add($addNetworkTopology1, "netTopologyHubNSpoke"))[0];
my $addHubnSpoke2 = ($ixNet->add($addNetworkTopology2, "netTopologyHubNSpoke"))[0];

$ixNet->setMultiAttribute($addHubnSpoke1, '-enableLevel2Spokes', 'false', '-includeEntryPoint', 'true');
$ixNet->setMultiAttribute($addHubnSpoke2, '-enableLevel2Spokes', 'false', '-includeEntryPoint', 'true');
$ixNet->commit();

my $networkGroup1 = ($ixNet->getList($t1dev1, 'networkGroup'))[0];
$ixNet->setAttribute($networkGroup1, '-name', "Simulated Topology 1");
my $networkGroup2 = ($ixNet->getList($t2dev1, 'networkGroup'))[0];
$ixNet->setAttribute($networkGroup2, '-name', "Simulated Topology 2");

my $networkTopology1 = ($ixNet->getList($networkGroup1, 'networkTopology'))[0];
my $simRouterBridge1 = ($ixNet->getList($networkTopology1, 'simRouterBridge'))[0];
my $networkTopology2 = ($ixNet->getList($networkGroup2, 'networkTopology'))[0];
my $simRouterBridge2 = ($ixNet->getList($networkTopology2, 'simRouterBridge'))[0];

# Changing Simulated topology connector to CFM stack
print("\n\nChanging Simulated topology connector to CFM stack\n");

my $addconnector1 = $ixNet->add($simRouterBridge1, 'connector');
$ixNet->setMultiAttribute($addconnector1, '-connectedTo', $cfmBridge1);
$ixNet->commit();

my $addconnector2 = $ixNet->add($simRouterBridge2, 'connector');
$ixNet->setMultiAttribute($addconnector2, '-connectedTo', $cfmBridge2);
$ixNet->commit();

# Configuring MD level and MA parameters from Simulated topology from CFM Network Group wizard
print("\n\nConfiguring MD level and MA parameters for Simulated topology 1 using CFM Network Group wizard\n");
my $cfmST1 = ($ixNet->getList($networkTopology1, 'cfmSimulatedTopology'))[0];
my $configMANames1 = ($ixNet->getList($cfmST1, 'configMANamesParams'))[0];
$ixNet->setMultiAttribute($configMANames1, '-maName', "MA-12");
$ixNet->commit();
$ixNet->execute('configMANames', $configMANames1);

my $configMDLevels1 = ($ixNet->getList($cfmST1, 'configMDLevelsParams'))[0];
$ixNet->setMultiAttribute($configMDLevels1, '-numMDLevels', '2', '-mdLevel1', "1",  '-mdNameFormat1', "mdNameFormatDomainNameBasedStr", '-mdName1', "MD-1", '-mdLevel2', "2", '-mdNameFormat2', "mdNameFormatCharacterStr", '-mdName2', "MD-2");
$ixNet->commit();
$ixNet->execute('configMDLevels', $configMDLevels1);

print("\n\nConfiguring MD level and MA parameters for Simulated topology 2 using CFM Network Group wizard\n");
my $cfmST2 = ($ixNet->getList($networkTopology2, 'cfmSimulatedTopology'))[0];
my $configMANames2 = ($ixNet->getList($cfmST2, 'configMANamesParams'))[0];
$ixNet->setMultiAttribute($configMANames2, '-maName', "MA-12");
$ixNet->commit();
$ixNet->execute('configMANames', $configMANames2);

my $configMDLevels2 = ($ixNet->getList($cfmST2, 'configMDLevelsParams'))[0];
$ixNet->setMultiAttribute($configMDLevels2, '-numMDLevels', '2', '-mdLevel1', "1", '-mdNameFormat1', "mdNameFormatDomainNameBasedStr", '-mdName1', "MD-1", '-mdLevel2', "2", '-mdNameFormat2', "mdNameFormatCharacterStr", '-mdName2', "MD-2");
$ixNet->commit();
$ixNet->execute('configMDLevels', $configMDLevels2);

print("************************************************************");

################################################################################
# Step 2> Start of protocol.
################################################################################
print("Starting protocols and waiting for 60 seconds for protocols to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);

################################################################################
# Step 3> Retrieve protocol statistics.
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
# Step 4> Retrieve protocol learned info
# Note: Blank columns in learned information are shown as '{ }' in output
###############################################################################

print("Fetching CCM Learned Info\n");
$ixNet->execute('getCfmCcmLearnedInformation', $cfmBridge1, '1');
sleep(5);
my $linfo  = ($ixNet->getList($cfmBridge1, 'learnedInfo'))[0];
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


print("Fetching Loopback Learned Info\n");
$ixNet->execute('getCfmLoopbackDbLearnedInformation', $cfmBridge1, '1');
sleep(5);
my $linfo  = ($ixNet->getList($cfmBridge1, 'learnedInfo'))[0];
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


print("Fetching Link Trace Learned Info\n");
$ixNet->execute('getCfmLinkTraceDbLearnedInformation', $cfmBridge1, '1');
sleep(5);
my $linfo  = ($ixNet->getList($cfmBridge1, 'learnedInfo'))[0];
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

################################################################################
# Step 5> OTF Stop CCM in emulated MP and Apply changes on the fly.
################################################################################
print "OTF stop  CCM for root(emualated) MP in topology 2 from right-click action\n";
$ixNet->execute('stopCcmEmulated', $cfmMp2);
print "Wait for 10 seconds before checking stats ...\n";
sleep(10);

################################################################################
# Step 6> Retrieve protocol statistics.
################################################################################
print("Fetching CFM Per Port Stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"CFM Per Port"/page';
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

################################################################################
# Step 7> Configure L2-L3 traffic.
################################################################################
print ("Congfiguring L2-L3 Traffic Item\n");
my $trafficItem1 = $ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->setMultiAttribute($trafficItem1, '-name', 'Ethernet Traffic 1',
    '-roundRobinPacketOrdering', 'false',
    '-trafficType', 'ethernetVlan');
$ixNet->commit();

$trafficItem1    = ($ixNet->remapIds($trafficItem1))[0];
my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');
my @source       = ($mac1);
my @destination  = ($mac2);

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
    '-trackBy',        ['ethernetIiSourceaddress0', 'ethernetIiDestinationaddress0', 'trackingenabled0'],
    '-fieldWidth',     'thirtyTwoBits',
    '-protocolOffset', 'Root.0',
    '-values',         (''));
$ixNet->commit();

###############################################################################
# Step 8> Apply and start L2/L3 traffic.
###############################################################################
print("applying L2/L3 traffic\n");
$ixNet->execute('apply', ($ixNet->getRoot()).'/traffic');
sleep(5);

print("starting L2/L3 traffic\n");
$ixNet->execute('start', ($ixNet->getRoot()).'/traffic');

###############################################################################
# Step 9> Retrieve L2/L3 traffic item statistics.
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
# Step 10> Stop L2/L3 traffic.
#################################################################################
print("Stopping L2/L3 traffic\n");
$ixNet->execute('stop', ($ixNet->getRoot()).'/traffic');

################################################################################
# Step 11> Stop all protocols.
################################################################################
print("Stopping all protocols\n");
$ixNet->execute('stopAllProtocols');
sleep(60);
print("!!! Test Script Ends !!!");
