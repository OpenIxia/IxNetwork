################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright  1997  2015 by IXIA                                             #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    02/02/2015  Alexandru Iordachescu - created sample                        #
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
# omissions or errorfree.                                                      #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NONINFRINGEMENT.                                  #
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
# damages limitations  forth herein and will not obligate Ixia to provide      #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

#################################################################################
#                                                                              	#
# Description:                                                                 	#
#	The script below represents an end to end workflow for AppLibrary Traffic. 	#
#	Steps:																	   	#			
#	1. Chassis connection and TCL server connection							   	#	
#	2. Scenario configuration at layer 2-3									   	#	
#	3. Creation of Applibrary traffic										   	#	
#	4. Per connection parameters configuration 								   	#	
#	5. Traffic apply and start 												   	#
#	6. Statistics operations: drill down in a loop							   	#	
#	7. Test criteria evaluation													#
#	8. Stop traffic															   	#
#													  	 						#		
#################################################################################

print "\n\n\n#######################################\n";
print "Running AppLibrary Sample Workflow Script\n";
print "#######################################\n\n\n";

#---------------------------------------------------------
# Loading required packages
#---------------------------------------------------------

use IxNetwork;
use strict;
use warnings;
use List::MoreUtils;

#---------------------------------------------------------
# Setting global variables for the sample run
#---------------------------------------------------------

my $chassisIP='10.205.23.34'; 										# chassis IP
my $applicationVersion='7.50'; 										# IxN version
my $ixNPort=8109; 													# the TCL port on which the IxTcl Server is listening
my $port1='/card:2/port:9'; 										# port 1
my $port2='/card:2/port:10'; 										# port 2
my @PFCriteria_Higher= ('Initiator Tx Rate (Mbps)', '40'); 			# statistic from Application Traffic item Statistics view that has to be higher than given value
my @PFCriteria_Lower = ('Flows Failed', '40');						# statistic from Application Traffic item Statistics view that has to be lower than given value

package applib_workflow;

sub new {
	# This routine will create a new instance
	my $class = shift;
	my $self = {
		_ixNet => new IxNetwork(),
		_objRefs => {}
	};
	bless $self, $class;
	return $self;
}

sub _connect {
	# This routine will connect to a running automation server on a specified port
	my($self) = @_;
	return $self->{_ixNet}->connect('127.0.0.1', '-port', $ixNPort, '-version', $applicationVersion);
}
sub _loadConfig {
	# This routine will create a new IxNetwork config, will add chassis and ports, ethernet stack, IP stack, L4-7 AppLibrary profile and will configure AppLibrary flows
	my($self) = @_;
	$self->{_ixNet}->rollback();
	my $result1 = $self->{_ixNet}->execute('newConfig'); #create a new config
	$self->{_objRefs}->{1} = $self->{_ixNet}->getRoot();

	$self->{_ixNet}->commit();
	
	#------------------------------------
	# Adding chassis
	#------------------------------------
	
	$self->{_objRefs}->{2} = $self->{_ixNet}->add($self->{_objRefs}->{1}.'/availableHardware', 'chassis');;
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{2},
		'-hostname', $chassisIP); #adding a new chassis
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{2} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{2}))[0];

	#------------------------------------
	# Adding 2 ports 
	#------------------------------------
	
	$self->{_objRefs}->{3} = $self->{_ixNet}->add($self->{_objRefs}->{1}, 'vport');;
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{3},  
		'-connectedTo', $self->{_objRefs}->{2}.$port1); #adding port1
		
		
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{3} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{3}))[0];
	
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{4} = $self->{_ixNet}->add($self->{_objRefs}->{1}, 'vport');;
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{4}, 
		'-connectedTo', $self->{_objRefs}->{2}.$port2); #adding port2
		
		
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{4} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{4}))[0];
	
	
	print "Connected to ports\n";
	
	#------------------------------------
	# Adding 1st topology, Device Group, Ethernet, IPv4 
	#------------------------------------
	
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{5} = $self->{_ixNet}->add($self->{_objRefs}->{1}, 'topology');;
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{5},  
		'-vports', [$self->{_objRefs}->{3}]); #create a new topology and map it to card 2 port 9
		
		
	
	#------------------------------------
	# Configure 1st topology
	#------------------------------------
	
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{5} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{5}))[0];

	$self->{_objRefs}->{6} = $self->{_ixNet}->add($self->{_objRefs}->{5}, 'deviceGroup');; #adding a new device group to the first topology
	
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{6} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{6}))[0];
	

	$self->{_objRefs}->{7} = $self->{_ixNet}->add($self->{_objRefs}->{6}, 'ethernet');;
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{7} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{7}))[0];
	
	
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{8} = $self->{_ixNet}->add($self->{_objRefs}->{7}, 'ipv4');;  #adding an IP stack to the first device group
		
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{8} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{8}))[0];
	

	$self->{_objRefs}->{9} = $self->{_ixNet}->getAttribute($self->{_objRefs}->{8}, '-gatewayIp');
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{9}, 
		'-pattern', 'counter');

	$self->{_ixNet}->commit();
	$self->{_objRefs}->{10} = $self->{_ixNet}->add($self->{_objRefs}->{9}, 'counter');;
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{10}, 
		'-step', '0.0.0.1', 
		'-start', '100.2.0.1', 
		'-direction', 'increment'); #Configuring gateway IP addresses for first IP stack
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{10} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{10}))[0];

	
	$self->{_objRefs}->{11} = $self->{_ixNet}->getAttribute($self->{_objRefs}->{8}, '-address');
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{11},  
		'-pattern', 'counter');

	$self->{_ixNet}->commit();
	$self->{_objRefs}->{12} = $self->{_ixNet}->add($self->{_objRefs}->{11}, 'counter');;
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{12}, 
		'-step', '0.0.0.1', 
		'-start', '100.1.0.1', 
		'-direction', 'increment'); #Configuring IP addresses for first IP stack
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{12} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{12}))[0];
	$self->{_ixNet}->commit();
	
	print "Configured IP1\n";

	#------------------------------------
	# Adding 2nd topology, DG, ethernet, IPv4 
	#------------------------------------
	
	$self->{_objRefs}->{13} = $self->{_ixNet}->add($self->{_objRefs}->{1}, 'topology');;
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{13},  
		'-vports', [$self->{_objRefs}->{4}]); #adding a second topology mapped to card 2 port 10
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{13} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{13}))[0];

	
	#------------------------------------
	# Configure 2nd topology
	#------------------------------------

	
	$self->{_objRefs}->{14} = $self->{_ixNet}->add($self->{_objRefs}->{13}, 'deviceGroup');;
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{14},  
		'-name', 'Device Group 2'); #adding a second device group to the second topology
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{14} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{14}))[0];
	
		
	$self->{_objRefs}->{15} = $self->{_ixNet}->add($self->{_objRefs}->{14}, 'ethernet');;
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{15} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{15}))[0];
	
	
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{16} = $self->{_ixNet}->add($self->{_objRefs}->{15}, 'ipv4');; #adding a second IP stack
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{16} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{16}))[0];
	
	
	$self->{_objRefs}->{17} = $self->{_ixNet}->getAttribute($self->{_objRefs}->{16}, '-gatewayIp');
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{17},
		'-pattern', 'counter');

	$self->{_ixNet}->commit();
	$self->{_objRefs}->{18} = $self->{_ixNet}->add($self->{_objRefs}->{17}, 'counter');;
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{18}, 
		'-step', '0.0.0.1', 
		'-start', '100.1.0.1', 
		'-direction', 'increment'); #Configuring gateway IP addresses for second IP stack
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{18} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{18}))[0];

	
	$self->{_objRefs}->{19} = $self->{_ixNet}->getAttribute($self->{_objRefs}->{16}, '-address');
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{19},  
		'-pattern', 'counter');

	$self->{_ixNet}->commit();
	$self->{_objRefs}->{20} = $self->{_ixNet}->add($self->{_objRefs}->{19}, 'counter');;
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{20}, 
		'-step', '0.0.0.1', 
		'-start', '100.2.0.1', 
		'-direction', 'increment'); #Configuring IP addresses for second IP stack
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{20} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{20}))[0];

	$self->{_ixNet}->commit();
	
	
	print "Configured IP2\n";
	
	
	#-------------------------------------------
	# Create traffic item and add flows
	#-------------------------------------------
		
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{21} = $self->{_ixNet}->add($self->{_objRefs}->{1}.'/traffic', 'trafficItem');;
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{21},  
		'-trafficItemType', 'applicationLibrary',   
		'-trafficType', 'ipv4ApplicationTraffic'); #adding an AppLibrary L4-7 traffic item
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{21} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{21}))[0];

	#-----------------------------------------------------
	# Link the traffic item to the new topology set
	#-----------------------------------------------------
	
	$self->{_objRefs}->{22} = $self->{_ixNet}->add($self->{_objRefs}->{21}, 'endpointSet');;
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{22},  
		'-destinations', [$self->{_objRefs}->{13}],  
		'-sources', [$self->{_objRefs}->{5}]); 
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{22} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{22}))[0];

	#----------------------------------------------------------
	# Edit traffic item parameters for the added traffic item
	#----------------------------------------------------------
	
	$self->{_objRefs}->{23} = $self->{_ixNet}->add($self->{_objRefs}->{21}, 'appLibProfile');;
	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{23}, 
		'-objectiveValue', '133',
		'-enablePerIPStats', 'true',
		'-objectiveType', 'throughputMbps',		
		'-objectiveDistribution', 'applyFullObjectiveToEachPort', 
		'-configuredFlows', ['ActiveSync_Unencrypted','AIM6_Chat','AppleJuice']); #adding 3 flows to the AppLib profile, and enabling Per IP Statistics
	$self->{_ixNet}->commit();
	$self->{_objRefs}->{23} = ($self->{_ixNet}->remapIds($self->{_objRefs}->{23}))[0];
	
	print "Added AppLib with 3 flows\n";
	
	#----------------------------------------------------------
	# Setting flow percentages and configuring flow parameters
	#----------------------------------------------------------

	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{23}.'/appLibFlow:"ActiveSync_Unencrypted"', 
		'-percentage', '65');

	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{23}.'/appLibFlow:"ActiveSync_Unencrypted"/connection:1/parameter:"serverPort"', 
		'-option', 'value');

	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{23}.'/appLibFlow:"ActiveSync_Unencrypted"/connection:1/parameter:"serverPort"/number', 
		'-value', '8080'); #modifying the server port for ActiveSync_Unencrypted flow to 8080

	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{23}.'/appLibFlow:"AIM6_Chat"', 
		'-percentage', '20');

	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{23}.'/appLibFlow:"AppleJuice"', 
		'-percentage', '15');

	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{23}.'/appLibFlow:"AppleJuice"/connection:1/parameter:"enableTOS"', 
		'-option', 'value');

	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{23}.'/appLibFlow:"AppleJuice"/connection:1/parameter:"enableTOS"/bool', 
		'-value', 'true'); #enable parameter enableTOS for AppleJuice flow

	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{23}.'/appLibFlow:"AppleJuice"/connection:1/parameter:"tosValue"', 
		'-option', 'choice');

	$self->{_ixNet}->setMultiAttribute($self->{_objRefs}->{23}.'/appLibFlow:"AppleJuice"/connection:1/parameter:"tosValue"/choice', 
		'-value', '0xA0'); #setting the value for enableTOS to 0xA0
		
	print "Configured AppLib flows\n";
		
	$self->{_ixNet}->commit();
	return '1';
}



sub run {
	my($self) = @_;
	my $result2 = $self->_connect();
	my $result3 = $self->_loadConfig();
	#----------------------------------------------------------
	# Starting up protocols
	#----------------------------------------------------------
	$self->{_ixNet}->execute('startAllProtocols');;
	print "Started Protocols\n";
	#----------------------------------------------------------
	# Apply and start traffic
	#----------------------------------------------------------
	$self->{_ixNet}->execute('applyApplicationTraffic', $self->{_objRefs}->{1}.'/traffic');; #applying L4-7 traffic
	print "Applied Traffic\n";
	$self->{_ixNet}->execute('startApplicationTraffic', $self->{_objRefs}->{1}.'/traffic');; #starting L4-7 traffic
	print "Started AppLib\n";
	print "Waiting 10 seconds before clearing AppLibrary statistics ...\n";
	sleep(10);
	#----------------------------------------------------------
	# Clearing Statistics for AppLibrary Traffic
	#----------------------------------------------------------
	$self->{_ixNet}->execute('clearAppLibraryStats');; #clearing statistics
	print "Statistics have been cleared\n";
	print "Drilling down to reveal per IP address flow activity\n";
	
	#----------------------------------------------------------
	# Drilling down per IP 
	#----------------------------------------------------------
	
	my @viewsList = $self->{_ixNet}->getList($self->{_objRefs}->{1}.'/statistics', 'view');;
	my $want = "::ixNet::OBJ-/statistics/view:\"Application Traffic Item Statistics\"";
	my $index = List::MoreUtils::first_index {$_ eq $want} @viewsList;;
	
	my $target = $viewsList[$index];
	print "Configuring drill down per IP addresses\n";
	
	$self->{_ixNet}->setMultiAttribute($target.'/drillDown', '-targetRowIndex', '0');
	$self->{_ixNet}->commit();
	$self->{_ixNet}->setMultiAttribute($target.'/drillDown', '-targetDrillDownOption', '"Application Traffic:Per IPs"');
	$self->{_ixNet}->commit();
	$self->{_ixNet}->setMultiAttribute($target.'/drillDown', '-targetRow', '"Traffic Item=Traffic Item"'); #selecting which views to show
	$self->{_ixNet}->commit();
	
	print "Launching the drill down per IP addresses view\n";
	$self->{_ixNet}->execute('doDrillDown', $target.'/drillDown');
	sleep(3);
	print "Refreshing statistics five times in a row\n";
	@viewsList = $self->{_ixNet}->getList($self->{_objRefs}->{1}.'/statistics', 'view');; #drilling down Per IP Stats
	$want = "::ixNet::OBJ-/statistics/view:\"Application Traffic Drill Down\"";
	$index = List::MoreUtils::first_index {$_ eq $want} @viewsList;;
	$target = $viewsList[$index];
	for (my $i=0; $i < 5; $i++) {
		$self->{_ixNet}->execute('refresh', $target); #refreshing views
		sleep(5);
		print "Statistics refreshed...\n";
	}
	sleep(20);
	
	
	
	#----------------------------------------------------------
	# Pass Fail Evaluation
	#----------------------------------------------------------

	# selecting the "Application Traffic Item Statistics view from all the views"	
	@viewsList = $self->{_ixNet}->getList($self->{_objRefs}->{1}.'/statistics', 'view');;
	$want = "::ixNet::OBJ-/statistics/view:\"Application Traffic Item Statistics\"";
	$index = List::MoreUtils::first_index {$_ eq $want} @viewsList;;
	
	# selecting the columns based on the configured criteria
	my $targetView = $viewsList[$index];
	my @targetColumnForHigh = $self->{_ixNet}->getAttribute($targetView.'/page', '-columnCaptions');
	my $want2 = $PFCriteria_Higher[0];
	my $index2 = List::MoreUtils::first_index {$_ eq $want2} @targetColumnForHigh;;
	
	my @targetColumnForLow = $self->{_ixNet}->getAttribute($targetView.'/page', '-columnCaptions');
	my $want3 = $PFCriteria_Lower[0];
	my $index3 = List::MoreUtils::first_index {$_ eq $want3} @targetColumnForLow;;
	
	# measuring the selected statistic
	my @measuredHigher = $self->{_ixNet}->getAttribute($targetView.'/page', '-rowValues');
	my $mH = $measuredHigher[0][0][$index2];
	my @measuredLower = $self->{_ixNet}->getAttribute($targetView.'/page', '-rowValues');
	my $mL = $measuredLower[0][0][$index3];
	
	# comparing with pass fail condition - second item in the PFCriteria list
	if(($mH>$PFCriteria_Higher[1])&&($mL<$PFCriteria_Lower[1]))
	{
		my $testResult= "\n Test run is PASSED";
		print "\n $testResult";
	} else {
		my $testResult= "\n Test run is FAILED: pass fail conditions - $PFCriteria_Higher[0] and $PFCriteria_Lower[0] - configured in the start of the script are not met";
		print "\n $testResult";
	}
	
	#----------------------------------------------------------
	# Stop traffic 
	#----------------------------------------------------------
	$self->{_ixNet}->execute('stopApplicationTraffic', $self->{_objRefs}->{1}.'/traffic');
	return '1';
}


package main;
new applib_workflow()->run();
#----------------------------------------------------------
# Test END
#----------------------------------------------------------
print "\n#####################\n";
print "Test run is COMPLETED\n";
print "#####################\n";