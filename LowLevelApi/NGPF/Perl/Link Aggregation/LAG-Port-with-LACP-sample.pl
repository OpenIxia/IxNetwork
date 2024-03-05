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
#    This script intends to demonstrate how to use NGPF LAG API.               #
#	 Script uses four ports for demonstration.                                 #
#                                                                              #
#    1. It will create 2 LAGs as RED-LAG & BLUE-LAG with LACP as LAG protocol, # 
#       each LAG having two member ports . It will then modify  the            #
#       ActorSystemId and ActorKey for both the LAG systems.                   #
#    2. Start the LAG.                                                         #
#    3. Retrieve protocol statistics and LACP per port statistics.             #
#	 4. Disable Synchronization flag on RED-LAG-port1 in RED-LAG.              # 
#	 5. Retrieve protocol statistics and LACP per port statistics.             #
#	 6. Re-enable Synchronization flag on RED-LAG-port1 in RED-LAG.            # 
#	 7. Retrieve protocol statistics and LACP per port statistics.             #
#	 8. Perform StopPDU on RED-LAG-port1 in RED-LAG.                           # 
#	 9. Retrieve LACP global learned info.                                     #
#	 10. Perform StartPDU on RED-LAG-port1 in RED-LAG.                         # 
#	 11. Retrieve LACP global learned info.                                    #
#	 12. Stop All protocols.                                                   #
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
my $ixTclServer = '10.39.50.102';
my $ixTclPort   = '5555';
my @ports       = (('10.39.50.96', '10', '1'), ('10.39.50.96', '10', '3'), ('10.39.50.96', '10', '5'), ('10.39.50.96', '10', '7'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '8.50',
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

# ADD LAGs named RED-LAG & BLUE-LAG
print("ADD LAGs named RED-LAG & BLUE-LAG\n");
$ixNet->add($ixNet->getRoot(), 'lag', '-vports', "$vportTx1 $vportTx2", '-name', "RED-LAG");
$ixNet->add($ixNet->getRoot(), 'lag', '-vports', "$vportRx1 $vportRx2", '-name', "BLUE-LAG");
$ixNet->commit();

print("sumit-1");
my @lagList = $ixNet->getList($ixNet->getRoot(), 'lag');
my $lag1 = $lagList[0];
my $lag2 = $lagList[1];

print ("Adding LACP over RED-LAG & BLUE-LAG");
$ixNet->add($lag1, 'protocolStack');
$ixNet->commit();
$ixNet->add($lag2, 'protocolStack');
$ixNet->commit();

my $lag1stack = ($ixNet->getList($lag1, 'protocolStack'))[0];
my $lag2stack = ($ixNet->getList($lag2, 'protocolStack'))[0];


print("Adding LAG ethernet");
$ixNet->add($lag1stack, 'ethernet');
$ixNet->commit();
$ixNet->add($lag2stack, 'ethernet');
$ixNet->commit();

my $lag1eth = ($ixNet->getList($lag1stack, 'ethernet'))[0];
my $lag2eth = ($ixNet->getList($lag2stack, 'ethernet'))[0];

print("Adding LACP as LAG Aggregation protocol");
$ixNet->add($lag1eth, 'lagportlacp');
$ixNet->commit();
$ixNet->add($lag2eth, 'lagportlacp');
$ixNet->commit();

my $lag1lacp = ($ixNet->getList($lag1eth, 'lagportlacp'))[0];
my $lag2lacp = ($ixNet->getList($lag2eth, 'lagportlacp'))[0];

##################################################################################
# To ADD staticLAG as LAG protocol
#Command sets 
#$ixNet->add($lag1eth, 'lagportstaticlag');
#$ixNet->commit();
#$ixNet->add($lag2eth, 'lagportstaticlag');
#$ixNet->commit();

#my $lag1slag = ($ixNet->getList($lag1eth, 'lagportstaticlag'))[0];
#my $lag2slag = ($ixNet->getList($lag2eth, 'lagportstaticlag'))[0];
##################################################################################

# configure LACP ActorSystemID and ActorKey to user defined values
print("configure LACP ActorSystemID and ActorKey to user defined values");

my $lag1lacpActKey = ($ixNet->getAttribute($lag1lacp, '-actorKey'));
my $lag2lacpActKey = ($ixNet->getAttribute($lag2lacp, '-actorKey'));

my $lag1lacpSysId = ($ixNet->getAttribute($lag1lacp, '-actorSystemId'));
my $lag2lacpSysId = ($ixNet->getAttribute($lag2lacp, '-actorSystemId'));

$ixNet->setMultiAttribute($lag1lacpActKey, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($lag2lacpActKey, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->commit();

$ixNet->setMultiAttribute($lag1lacpActKey.'/singleValue', '-value', '666');
$ixNet->setMultiAttribute($lag2lacpActKey.'/singleValue', '-value', '777');
$ixNet->commit();

$ixNet->setMultiAttribute($lag1lacpSysId, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->setMultiAttribute($lag2lacpSysId, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->commit();

$ixNet->setMultiAttribute($lag1lacpSysId.'/singleValue', '-value', '11666');
$ixNet->setMultiAttribute($lag2lacpSysId.'/singleValue', '-value', '11777');
$ixNet->commit();

################################################################################
# Start LAG protocols and wait for 60 seconds                                  #
################################################################################
print ("\nStart LAG and waiting for 60 seconds for sessions to come up\n");
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
# Disable Synchronization flag on port1 in RED-LAG                             #
################################################################################
print ("\nDisable Synchronization flag on port1 in RED-LAG   \n");
my $redLagport1 = ($ixNet->getList($lag1lacp, 'port'))[0];
my $redLagport1SyncFlag = ($ixNet->getAttribute($redLagport1, '-synchronizationFlag'));
$ixNet->setAttribute($redLagport1SyncFlag, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->commit();
$ixNet->setAttribute($redLagport1SyncFlag.'/singleValue', '-value', 'false');
$ixNet->commit();
print("Apply changes On The Fly (OTF)\n");
my $globals   = ($ixNet->getRoot()).'/globals';
my $laglogy  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $laglogy);
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
sleep(10);
################################################################################
# Re-enable Synchronization flag on port1 in System1-LACP-LHS                  #
################################################################################
print ("\nRe-enabable Synchronization flag on port1 in RED-LAG   \n");
my $redLagport1 = ($ixNet->getList($lag1lacp, 'port'))[0];
my $redLagport1SyncFlag = ($ixNet->getAttribute($redLagport1, '-synchronizationFlag'));
$ixNet->setAttribute($redLagport1SyncFlag, '-pattern', 'singleValue', '-clearOverlays', 'False');
$ixNet->commit();
$ixNet->setAttribute($redLagport1SyncFlag.'/singleValue', '-value', 'true');
$ixNet->commit();
print("Apply changes On The Fly (OTF)\n");
my $globals   = ($ixNet->getRoot()).'/globals';
my $laglogy  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $laglogy);
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
# Perform LACPDU stop on RED-LAG-LACP                                      #
################################################################################
print ("\n\nPerform LACPDU stop on RED-LAG-LACP ");
$ixNet->execute('lacpStopPDU', $lag1lacp);
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
# Perform LACPDU start on RED-LAG-LACP                                      #
################################################################################
print ("\n\nPerform LACPDU start on RED-LAG-LACP ");
$ixNet->execute('lacpStartPDU', $lag1lacp);
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
