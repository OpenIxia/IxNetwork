################################################################################
# Version 1.0    $Revision: #1 $                                               #
#                                                                              #
#    Copyright  1997 - 2015 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    06/04/2015 - Sumit Deb - created sample                                   #
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
#    This script intends to demonstrate how to use NGPF LACP API.              #
#	 Script uses four ports to demonstrate LAG properties					   #
#                                                                              #
#    1. It will create 2 LACP topologies, each having two ports which are      #
#       LAG members. It will then modify the ActorSystemId and ActorKey	for	   # 
#       both the LAG systems.                                                  #
#    2. Start the LACP protocol.                                               #
#    3. Retrieve protocol statistics and LACP per port statistics              #
#	 4. Disable Synchronization flag on port1 in System1-LACP-LHS              # 
#	 5. Retrieve protocol statistics and LACP per port statistics              #
#	 6. Re-enable Synchronization flag on port1 in System1-LACP-LHS            # 
#	 7. Retrieve protocol statistics and LACP per port statistics              #
#	 8. Perform StopPDU on port1 in System1-LACP-LHS                		   # 
#	 9. Retrieve LACP global learned info              			   			   #
#	 10. Perform StopPDU on port1 in System1-LACP-LHS                          # 
#	 11. Retrieve LACP global learned info                                     #
#	 12. Stop All protocols                                                    # 
#                                                                              #
# 	Ixia Software:                                                             #
#    IxOS      6.90 EA                                                         #
#    IxNetwork 7.50 EA                                                         #
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
	my $chassis3 = $my_resource[7];
	my $card3    = $my_resource[8];
	my $port3    = $my_resource[9];
	my $chassis4 = $my_resource[10];
	my $card4    = $my_resource[11];
	my $port4    = $my_resource[12];
	my $vport1   = $my_resource[13];
	my $vport2   = $my_resource[14];
	my $vport3   = $my_resource[15];
	my $vport4   = $my_resource[16];
	
	my $root = $ixNet->getRoot();
	my $chassisObj1 = $ixNet->add($root.'/availableHardware', 'chassis');
    $ixNet->setAttribute($chassisObj1, '-hostname', $chassis1);
    $ixNet->commit();
    $chassisObj1 = ($ixNet->remapIds($chassisObj1))[0];
	
	my $chassisObj2 = '';
	my $chassisObj3 = '';
	my $chassisObj4 = '';
	
	if ($chassis1 ne $chassis2) {
	    $chassisObj2 = $ixNet->add($root.'/availableHardware', 'chassis');
        $ixNet->setAttribute($chassisObj2, '-hostname', $chassis2);
        $ixNet->commit();
        $chassisObj2 = ($ixNet->remapIds($chassisObj2))[0];
	    
		$chassisObj3 = $ixNet->add($root.'/availableHardware', 'chassis');
        $ixNet->setAttribute($chassisObj3, '-hostname', $chassis3);
        $ixNet->commit();
        $chassisObj3 = ($ixNet->remapIds($chassisObj3))[0];
		
		$chassisObj4 = $ixNet->add($root.'/availableHardware', 'chassis');
        $ixNet->setAttribute($chassisObj4, '-hostname', $chassis4);
        $ixNet->commit();
        $chassisObj4 = ($ixNet->remapIds($chassisObj4))[0];
	} else {
	    $chassisObj2 = $chassisObj1;
		$chassisObj3 = $chassisObj1;
		$chassisObj4 = $chassisObj1;
	}
	print("sumit-3");
	my $cardPortRef1 = $chassisObj1.'/card:'.$card1.'/port:'.$port1;
    $ixNet->setMultiAttribute($vport1, '-connectedTo', $cardPortRef1,
        '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 001');
    $ixNet->commit();

    my $cardPortRef2 = $chassisObj2.'/card:'.$card2.'/port:'.$port2;
    $ixNet->setMultiAttribute($vport2, '-connectedTo', $cardPortRef2,
        '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 002');

	my $cardPortRef3 = $chassisObj3.'/card:'.$card3.'/port:'.$port3;
    $ixNet->setMultiAttribute($vport3, '-connectedTo', $cardPortRef3,
        '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 003');
    $ixNet->commit();

    my $cardPortRef4 = $chassisObj4.'/card:'.$card4.'/port:'.$port4;
    $ixNet->setMultiAttribute($vport4, '-connectedTo', $cardPortRef4,
        '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 004');
		
    $ixNet->commit();
}
sub gererateLacpLearnedInfoView {
    my @args = @_;
	my $ixNet    = $args[0];
    my $viewCaption = $args[1] ;
    my $protocol = 'LACP';
    my $drillDownType = 'Global Learned Info';
    my $root    = $ixNet->getRoot();
    my $statistics = $root.'/statistics';
    my $statsViewList = $ixNet->getList($statistics, 'view');
	
   # Add a StatsView
    my $view = $ixNet->add($statistics, 'view');
    $ixNet->setAttribute($view, '-caption', $viewCaption);
    $ixNet->setAttribute($view, '-type', 'layer23NextGenProtocol');
    $ixNet->setAttribute($view, '-visible', 'true');
    $ixNet->commit();
    $view = ($ixNet->remapIds($view))[0];

   # Set Filters        
    my $trackingFilter = $ixNet->add($view, 'advancedCVFilters');
    $ixNet->setAttribute($trackingFilter, '-protocol', $protocol);
    $ixNet->commit();
    #ixNet getAttr $trackingFilter -availableGroupingOptions        
    $ixNet->setAttribute($trackingFilter, '-grouping', $drillDownType);
    $ixNet->commit();
    my $layer23NextGenProtocolFilter = $view.'/'.'layer23NextGenProtocolFilter';        
    $ixNet->setAttribute($layer23NextGenProtocolFilter, '-advancedCVFilter', $trackingFilter);
    $ixNet->commit();

    # Enable Stats Columns to be displayed
    my @statsList = $ixNet->getList($view, 'statistic');
    my $stat = '';
	foreach $stat (@statsList) {
        $ixNet->setAttribute($stat, '-enabled', 'true');
	}
    $ixNet->commit();

    # Enable Statsview
    $ixNet->setAttribute($view, '-enabled', 'true');
    $ixNet->commit();
}
# Script Starts
print("!!! Test Script Starts !!!\n");

# Edit this variables values to match your setup
my $ixTclServer = '10.205.28.122';
my $ixTclPort   = '8987';
my @ports       = (('10.205.28.173', '1', '1'), ('10.205.28.173', '1', '2'), ('10.205.28.173', '1', '3'), ('10.205.28.173', '1', '4'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '7.50',
    '-setAttribute', 'strict');

print("Creating a new config\n");
$ixNet->execute('newConfig');

print("Adding 4 vports\n");
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->commit();

my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vportTx1 = $vPorts[0];
my $vportRx1 = $vPorts[1];
my $vportTx2 = $vPorts[2];
my $vportRx2 = $vPorts[3];

assignPorts($ixNet, @ports, $vportTx1, $vportRx1, $vportTx2, $vportRx2);
sleep(5);

print("Adding 2 topologies\n");
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', "$vportTx1 $vportTx2");
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', "$vportRx1 $vportRx2");
$ixNet->commit();
print("sumit-1");
my @topologies = $ixNet->getList($ixNet->getRoot(), 'topology');
my $topo1 = $topologies[0];
my $topo2 = $topologies[1];

print("Adding 2 device groups\n");
$ixNet->add($topo1, 'deviceGroup');
$ixNet->add($topo2, 'deviceGroup');
$ixNet->commit();
print("sumit-2");
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
        '-start',     '00:11:01:00:00:01',
        '-step',      '00:00:01:00:00:00');

$ixNet->setMultiAttribute($ixNet->getAttribute($mac2, '-mac').'/counter',
        '-direction', 'increment',
        '-start',     '00:11:01:00:00:01',
        '-step',      '00:00:01:00:00:00');
$ixNet->commit();

print("Adding LACP over Ethernet stacks\n");
$ixNet->add($mac1, 'lacp');
$ixNet->add($mac2, 'lacp');
$ixNet->commit();

my $lacp1 = ($ixNet->getList($mac1, 'lacp'))[0];
my $lacp2 = ($ixNet->getList($mac2, 'lacp'))[0];

print("Renaming the topologies and the device groups\n");
$ixNet->setAttribute($topo1, '-name', 'LAG1-LHS');
$ixNet->setAttribute($topo2, '-name', 'LAG1-RHS');

$ixNet->setAttribute($t1dev1, '-name', 'SYSTEM1-LACP-LHS');
$ixNet->setAttribute($t2dev1, '-name', 'SYSTEM1-LACP-RHS');
$ixNet->commit();
print("Modifying ActorSystemID and ActorKey to user defined values");
my $sys1LagLHS = ($ixNet->getList($mac1, 'lacp'))[0];
my $sys1LagRHS = ($ixNet->getList($mac2, 'lacp'))[0];

my $sys1LagLHSport1 = ($ixNet->getList($sys1LagLHS, 'port'))[0];
my $sys1LagLHSport2 = ($ixNet->getList($sys1LagLHS, 'port'))[1];
my $sys1LagRHSport1 = ($ixNet->getList($sys1LagRHS, 'port'))[0];
my $sys1LagRHSport2 = ($ixNet->getList($sys1LagRHS, 'port'))[1];

print"sumit-1";
my $sys1LagLHSport1ActKey = ($ixNet->getAttribute($sys1LagLHSport1, '-actorKey'));
my $sys1LagLHSport2ActKey = ($ixNet->getAttribute($sys1LagLHSport2, '-actorKey'));
my $sys1LagRHSport1ActKey = ($ixNet->getAttribute($sys1LagRHSport1, '-actorKey'));
my $sys1LagRHSport2ActKey = ($ixNet->getAttribute($sys1LagRHSport2, '-actorKey'));

my $sys1LagLHSport1SysId = ($ixNet->getAttribute($sys1LagLHSport1, '-actorSystemId'));
my $sys1LagLHSport2SysId = ($ixNet->getAttribute($sys1LagLHSport2, '-actorSystemId'));
my $sys1LagRHSport1SysId = ($ixNet->getAttribute($sys1LagRHSport1, '-actorSystemId'));
my $sys1LagRHSport2SysId = ($ixNet->getAttribute($sys1LagRHSport2, '-actorSystemId'));

print"sumit-2";
$ixNet->setMultiAttribute($sys1LagLHSport1ActKey, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($sys1LagLHSport2ActKey, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($sys1LagRHSport1ActKey, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($sys1LagRHSport2ActKey, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->commit();

$ixNet->setMultiAttribute($sys1LagLHSport1ActKey.'/singleValue', '-value', '666');
$ixNet->setMultiAttribute($sys1LagLHSport2ActKey.'/singleValue', '-value', '666');
$ixNet->setMultiAttribute($sys1LagRHSport1ActKey.'/singleValue', '-value', '777');
$ixNet->setMultiAttribute($sys1LagRHSport2ActKey.'/singleValue', '-value', '777');
$ixNet->commit();

$ixNet->setMultiAttribute($sys1LagLHSport1SysId, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($sys1LagLHSport2SysId, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($sys1LagRHSport1SysId, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($sys1LagRHSport2SysId, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->commit();

$ixNet->setMultiAttribute($sys1LagLHSport1SysId.'/singleValue', '-value', '666');
$ixNet->setMultiAttribute($sys1LagLHSport2SysId.'/singleValue', '-value', '666');
$ixNet->setMultiAttribute($sys1LagRHSport1SysId.'/singleValue', '-value', '777');
$ixNet->setMultiAttribute($sys1LagRHSport2SysId.'/singleValue', '-value', '777');
$ixNet->commit();

################################################################################
# Start LACP protocol and wait for 60 seconds                                  #
################################################################################
print ("\nStarting LACP and waiting for 60 seconds for sessions to come up\n");
$ixNet->execute('startAllProtocols');
sleep(60);

################################################################################
# Retrieve protocol statistics and LACP per port statistics                    #
################################################################################
print("\nFetching all Protocol Summary Stats\n");
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
print("\nFetching all LACP Per Port Stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"LACP Per Port"/page';
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
# Disable Synchronization flag on port1 in System1-LACP-LHS                    #
################################################################################
print ("\n\nDisable Synchronization flag on port1 in System1-LACP-LHS\n");
my $sys1LagLHSport1SyncFlag = ($ixNet->getAttribute($sys1LagLHSport1, '-synchronizationFlag'));
$ixNet->setAttribute($sys1LagLHSport1SyncFlag, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->commit();
$ixNet->setAttribute($sys1LagLHSport1SyncFlag.'/singleValue', '-value', 'false');
$ixNet->commit();
print("Apply changes On The Fly (OTF)\n");
my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);

################################################################################
# Retrieve protocol statistics and LACP per port statistics                    #
################################################################################
print("\nFetching all Protocol Summary Stats\n");
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
print("\nFetching all LACP Per Port Stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"LACP Per Port"/page';
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
# Re-enable Synchronization flag on port1 in System1-LACP-LHS                  #
################################################################################
print ("\n\nRe-enable Synchronization flag on port1 in System1-LACP-LHS\n");
my $sys1LagLHSport1SyncFlagTemp = ($ixNet->getAttribute($sys1LagLHSport1, '-synchronizationFlag'));
$ixNet->setAttribute($sys1LagLHSport1SyncFlagTemp, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->commit();
$ixNet->setAttribute($sys1LagLHSport1SyncFlagTemp.'/singleValue', '-value', 'true');
$ixNet->commit();
print("Apply changes On The Fly (OTF)\n");
my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);

################################################################################
# Retrieve protocol statistics and LACP per port statistics                    #
################################################################################
print("\nFetching all Protocol Summary Stats\n");
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
print("\nFetching all LACP Per Port Stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"LACP Per Port"/page';
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
# Perform LACPDU stop on System1-LACP-LHS                                      # 
################################################################################
print ("\n\nPerform LACPDU stop on System1-LACP-LHS ");
$ixNet->execute('lacpStopPDU', $sys1LagLHS);
sleep(90);

################################################################################
# Retrieve LACP global Learned Info                                            #
################################################################################
print ("\n\n Retrieve LACP global Learned Info\n");
my $viewName = 'LACP-global-learned-Info-TCLview';
gererateLacpLearnedInfoView($ixNet, $viewName);
my $viewPageName = '::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"';
my $viewPage = '::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"/page';
$ixNet->execute('refresh', $viewPageName);
sleep(10);
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
# Perform LACPDU start on System1-LACP-LHS                                     # 
################################################################################
print ("\n\nPerform LACPDU start on System1-LACP-LHS ");
$ixNet->execute('lacpStartPDU', $sys1LagLHS);
sleep(90);

################################################################################
# Retrieve LACP global Learned Info                                            #
################################################################################
print ("\n\n Retrieve LACP global Learned Info\n");
my $viewPageName = '::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"';
my $viewPage = '::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"/page';
$ixNet->execute('refresh', $viewPageName);
sleep(10);
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
# Stop all protocols                                                          #
################################################################################
print ("Stopping all protocols\n");
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!");
