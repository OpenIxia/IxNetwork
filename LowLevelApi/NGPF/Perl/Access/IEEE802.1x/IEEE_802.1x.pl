################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################

################################################################################
# Description:                                                                 
#    This script intends to demonstrate how to use IEEE 802.1x API
#    It will do the  following :
#1.    Add topology and devicegroup 
#2.    Configure ethernet and dot1x Layer.
#3.    Change protocol type to PEAPV0
#4.    Change few global parameters
#5.    Start of Device group
#6.    Check for session info and stats
#7.    Stop of Device group
################################################################################
################################################################################
# Please ensure that PERL5LIB environment variable is set properly so that     #
# IxNetwork.pm module is available. IxNetwork.pm is generally available in     #
# C:\<IxNetwork Install Path>\API\Perl                                         #
################################################################################
use IxNetwork;
use strict;

# Script Starts
print("!!! Test Script Starts !!!\n");
my $ixTclServer = '10.39.65.1';
my $ixTclPort   = '7889';
my @ports       = (('10.39.65.187', '1', '4'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

################################################################################
# Connecting to IxTCl server and creating new config                           #
################################################################################

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '8.50',
    '-setAttribute', 'strict');

print("Creating a new config\n");
$ixNet->execute('newConfig');

print("Adding a vports\n");
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->commit();

my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vport1= $vPorts[0];
print "vport is : $vport1\n";
sleep(5);

my $chassis1 = $ports[0];
my $card1    = $ports[1];
my $port1    = $ports[2];
sleep(5);

my $root = $ixNet->getRoot();
my $chassisObj1 = $ixNet->add($root.'/availableHardware', 'chassis');
$ixNet->setAttribute($chassisObj1, '-hostname', $chassis1);
$ixNet->commit();
$chassisObj1 = ($ixNet->remapIds($chassisObj1))[0];
my $cardPortRef1 = $chassisObj1.'/card:'.$card1.'/port:'.$port1;
$ixNet->setMultiAttribute($vport1, '-connectedTo', $cardPortRef1,
    '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 001');
$ixNet->commit();

##################### Creating topology and Device group #######################
print("Adding 1 topology\n");
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', $vport1);
$ixNet->commit();
my @topologies = $ixNet->getList($ixNet->getRoot(), 'topology');
my $topo1 = $topologies[0];

print("Adding 1 device group\n");
$ixNet->add($topo1, 'deviceGroup');
$ixNet->commit();

my @t1devices = $ixNet->getList($topo1, 'deviceGroup');
my $dot1x_dg = $t1devices[0];
print("Configuring the multipliers (number of sessions)\n");
$ixNet->setAttribute($dot1x_dg, 
                    '-multiplier', '1',
                    '-name', 'Dot1x DG');
$ixNet->commit();

########### Creating Dot1x layer #################
print("Adding ethernet Layer\n");
my $ethernet = ($ixNet->add($dot1x_dg, 'ethernet'));
$ixNet->commit();
$ixNet->setMultiAttribute($ethernet, '-name', 'Ethernet');
$ixNet->commit();

print("Adding Dot1x Layer\n");
my $dot1x = ($ixNet->add($ethernet, 'dotOneX'));
$ixNet->commit();
$ixNet->setMultiAttribute($dot1x, '-name', 'Dot1x');
$ixNet->commit();

####### Change protocol type to PEAPV0 ###########
print("Change protocol type to PEAPV0\n");
my $dot1x_protocol = $ixNet->getAttribute($dot1x, '-protocol');
$ixNet->setMultiAttribute($dot1x_protocol, '-clearOverlays', 'false');
$ixNet->commit();
my $dot1x_protocol_single_val = $ixNet->add($dot1x_protocol, 'singleValue');
$ixNet->setMultiAttribute($dot1x_protocol_single_val, '-value', 'eappeapv0');
$ixNet->commit();

######################## Change few global parameters ##########################
print ("Change few global parameters\n");
my @glob1 = ($ixNet->getList($ixNet->getRoot(), 'globals'));
my @glob_topo = ($ixNet->getList(@glob1, 'topology'));
my @dot1x_glob = ($ixNet->getList(@glob_topo, 'dotOneX'));

#### Enable Don't logoff global parameter ######
print ("Enable Don't logoff global parameter\n");
my $disable_logoff = $ixNet->getAttribute(@dot1x_glob, '-disableLogoff');
$ixNet->setMultiAttribute($disable_logoff, '-clearOverlays', 'false');
$ixNet->commit();
my $disable_logoff_single_val = $ixNet->add($disable_logoff, 'singleValue');
$ixNet->setMultiAttribute($disable_logoff_single_val, '-value', 'true');
$ixNet->commit();

######### Change the DUT Test mode #############
print ("Change the DUT Test mode\n");
my $dut_mode = $ixNet->getAttribute(@dot1x_glob, '-dutTestMode');
$ixNet->setMultiAttribute($dut_mode, '-clearOverlays', 'false');
$ixNet->commit();
my $dut_mode_single_val = $ixNet->add($dut_mode, 'singleValue');
$ixNet->setMultiAttribute($dut_mode_single_val, '-value', 'singlehost');
$ixNet->commit();

######### Change Wait before Run value #########
print ("Change Wait before Run value\n");
my $wait_before_run = $ixNet->getAttribute(@dot1x_glob, '-waitBeforeRun');
$ixNet->setMultiAttribute($wait_before_run, '-clearOverlays', 'false');
$ixNet->commit();
my $wait_before_run_single_val = $ixNet->add($wait_before_run, 'singleValue');
$ixNet->setMultiAttribute($wait_before_run_single_val, '-value', 10);
$ixNet->commit();

######### Change EAPOL Version #########
print ("Change EAPOL Version\n");
my $eapol_version = $ixNet->getAttribute(@dot1x, '-eapolVersion');
$ixNet->setMultiAttribute($eapol_version, '-clearOverlays', 'false');
$ixNet->commit();
my $eapol_version_single_val = $ixNet->add($eapol_version, 'singleValue');
$ixNet->setMultiAttribute($eapol_version_single_val, '-value', 'eapolver2020');
$ixNet->commit();

######### Enable Ignore Authenticator EAPOL Version #########
print ("Enable Ignore Authenticator EAPOL Version\n");
my $ignore_auth_eapol_ver = $ixNet->getAttribute(@dot1x, '-ignoreAuthEapolVer');
$ixNet->setMultiAttribute($ignore_auth_eapol_ver, '-clearOverlays', 'false');
$ixNet->commit();
my $ignore_auth_eapol_ver_single_val = $ixNet->add($ignore_auth_eapol_ver, 'singleValue');
$ixNet->setMultiAttribute($ignore_auth_eapol_ver_single_val, '-value', 'true');
$ixNet->commit();

################################################################################
#           Start Dot1x DG and wait for 40 seconds                             #
################################################################################
print("Start Dot1x DG and wait for 40 seconds for protocols to come up\n");
$ixNet->execute('start', $dot1x_dg);
sleep(40);

################################################################################
#           Retrieve Session info and protocol statistics                      #
################################################################################
my @session_info = $ixNet->getAttribute($dot1x, '-sessionInfo');
print ("Session info =",@session_info);
print("\nFetching Protocol Summary Stats\n");
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
print("Fetching Dot1x Per Port stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"IEEE 802.1X Per Port"/page';
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
# Stop all protocols                                                           #
################################################################################
print("Stopping All Protocols\n");
$ixNet->execute('stop', $dot1x_dg);
sleep(30);

print("!!! Test Script Ends !!!");
