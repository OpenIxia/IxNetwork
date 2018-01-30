#!/usr/bin/perl
################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    19/07/2016 - Sarabjeet Kaur - created sample                              #
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
#    This script intends to demonstrate how to use NGPF OpenFlow Controller API#
#    It will create 1 topology of OpenFlow Controller, it will start the 
#    emulation and then it will retrieve and display few statistics 
#    It will also check detailed learned info and learned info after sending on#
#    demand message                                                            #
# Ixia Software:                                                               #
#    IxOS      8.10 EA                                                         #
#    IxNetwork 8.10 EA                                                         #
#                                                                              #
################################################################################
use IxNetwork


# Script Starts
print("!!! Test Script Starts !!!\n");

# Edit this variables values to match your setup
my $ixTclServer = '10.214.101.141';
my $ixTclPort   = '8564';
my @ports       = (('12.0.1.253', '5', '10'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

################################################################################
# Connecting to IxTclNetwork Server and adding ports                           #
################################################################################ 

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '7.40',
    '-setAttribute', 'strict');

print("Creating a new config\n");
$ixNet->execute('newConfig');

print("Adding a vports\n");
$ixNet->add($ixNet->getRoot(), 'vport');
$ixNet->commit();

my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vportTx = $vPorts[0];
print "vport is : $vportTx\n";
sleep(5);

my $chassis1 = $ports[0];
my $card1    = $ports[1];
my $port1    = $ports[2];
my $vport1   = $vportTx;
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

################################################################################
# protocol configuration section                                               #
################################################################################ 

print("Adding 2 topologies\n");
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', $vportTx);
$ixNet->commit();

my @topologies = $ixNet->getList($ixNet->getRoot(), 'topology');
my $topo1 = $topologies[0];


print("Adding device groups\n");
$ixNet->add($topo1, 'deviceGroup');
$ixNet->commit();

my @t1devices = ($ixNet->getList($topo1, 'deviceGroup'));
my $t1devices = ($ixNet->getList($topo1, 'deviceGroup'));
my $t1dev1 = $t1devices[0];

print("Configuring the multipliers (number of sessions)\n");
$ixNet->setAttribute($t1dev1, '-multiplier', '1');
$ixNet->commit();

print("Adding ethernet/mac endpoints\n");
$ixNet->add($t1dev1, 'ethernet');
$ixNet->commit();

my $mac1 = ($ixNet->getList($t1dev1, 'ethernet'))[0];


print("Add ipv4\n");
$ixNet->add($mac1, 'ipv4');
$ixNet->commit();

my $ip1 = ($ixNet->getList($mac1, 'ipv4'))[0];
my $mvAdd1 = $ixNet->getAttribute($ip1, '-address');
my $mvGw1  = $ixNet->getAttribute($ip1, '-gatewayIp');

print("configuring ipv4 addresses \n");
$ixNet->setAttribute($mvAdd1.'/singleValue', '-value', '1.1.1.2');
$ixNet->setAttribute($mvGw1.'/singleValue', '-value', '1.1.1.1');
$ixNet->setAttribute($ixNet->getAttribute($ip1, '-prefix').'/singleValue', '-value', '24');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-resolveGateway').'/singleValue', '-value', 'true');
$ixNet->commit();

print("Adding Openflow Controller over IP4 stacks \n");
$ixNet->add($ip1, 'openFlowController');
$ixNet->commit();

my $openFlowController1 = ($ixNet->getList($ip1, 'openFlowController'))[0];
print "of controller is : $openFlowController1\n";
my $openflowchannels = $ixNet->add($openFlowController1, 'openFlowChannel');
$ixNet->commit();
print "OFchannel is : $openflowchannels\n";

sleep(2);
my $openflowchannellist = ($ixNet->getList($openFlowController1, 'openFlowChannel'))[0];
$ixNet->setAttribute($openflowchannels, '-groupsPerChannel', '1');
$ixNet->commit();
sleep(2);

$ixNet->setMultiAttribute($openflowchannels, '-metersPerChannel', '1');
$ixNet->commit();

my $table1 = ($ixNet->getList($openflowchannellist, 'tables'))[0];
my $flowset = ($ixNet->getList($table1, 'flowSet'))[0];
my $flowprofile = ($ixNet->getList($flowset, 'flowProfile'))[0];
print "flow profile is : $flowprofile\n";
my $root = $ixNet->getRoot();
my $global1 = ($ixNet->getList($root, 'globals'))[0];
print "global is :$global1\n";
my $topo1 = ($ixNet->getList($global1, 'topology'))[0];
print "topo is: $topo1\n";
my $ofcontroller1 = ($ixNet->getList($topo1, 'openFlowController'))[0];
print "ofcontroller is : $ofcontroller1\n";

################################################################################
# Adding Flow Profile template                                                 #
################################################################################
my $flowtemp = ($ixNet->getList($ofcontroller1, 'flowSetTemplate'))[0];
print "flow temp is : $flowtemp\n";
my $predefined_template = $ixNet->add($flowtemp, 'predefined');
print "predef temp is : $predefined_template\n";
my $flow_template = $ixNet->add($predefined_template, 'flowTemplate');
print "Flow templated added : $flow_template\n";
$ixNet->commit();
sleep(5);
@matchactionlist = $ixNet->getList($flow_template, 'matchAction');
print "@matchactionlist\n";
foreach $i (@matchactionlist){
    print "$i\n";
    $ixNet->getAttribute($i, '-name');
    if (($ixNet->getAttribute($i, '-name')) eq "[1] Blank Template") {
        print "success\n";
        $ixNet->execute('addFromTemplate', $flowprofile, $i);
        $ixNet->commit();
        sleep(5);
    }
}
##########################################################################################
# Adding Match Criteria :Ethernet Source , Ethernet Destination,Ipv4 Source, Destination #
##########################################################################################
my $flow_profile_matchAction = ($ixNet->getList($flowprofile, 'matchAction'))[0];
my $flow_profilematch_criteria = ($ixNet->getList($flow_profile_matchAction, 'matchCriteria'))[0];
@match_criteria_list = $ixNet->getList($flow_profilematch_criteria, 'matchCriteria');
print "@match_criteria_list\n";
foreach $matchCriteria (@match_criteria_list){
    print "$matchCriteria\n";
    if (($ixNet->getAttribute($matchCriteria, '-name')) eq "Ethernet") {
        print "Match criteria is ethernet\n";
        $ixNet->setMultiAttribute($matchCriteria, '-isEnabled', 'true');
        $ixNet->commit();
        @ethernetmatchCriteria = $ixNet->getList($matchCriteria, 'matchCriteria');
        print "@ethernetmatchCriteria\n";
        foreach $ethernetmatchlist (@ethernetmatchCriteria) {
            if (($ixNet->getAttribute($ethernetmatchlist, '-name')) eq "Ethernet Source") {
                $ethernetsourcefield = ($ixNet->getList($ethernetmatchlist, 'field'))[0];
                print "$ethernetsourcefield\n";
                $valuemulti = $ixNet->getAttribute($ethernetsourcefield, '-value');
                print "$valuemulti\n";
                $ixNet->setAttribute($valuemulti.'/singleValue', '-value', '44:0:0:0:0:77');
                $ixNet->commit();
                sleep(5)
            } else {
               $ethernetdestinationfield = ($ixNet->getList($ethernetmatchlist, 'field'))[0];
                print "$ethernetdestinationfield\n";
                $valuemulti = $ixNet->getAttribute($ethernetdestinationfield, '-value');
                print "$valuemulti\n";
                $ixNet->setAttribute($valuemulti.'/singleValue', '-value', '11:0:0:0:0:77');
                $ixNet->commit();
                sleep(5);
            }
                
        }
    }
    if (($ixNet->getAttribute($matchCriteria, '-name')) eq "IP") {
        print "Match criteria is IP";
        $ixNet->setMultiAttribute($matchCriteria, '-isEnabled', 'true');
        $ixNet->commit();
        $ipmatchCriteria = ($ixNet->getList($matchCriteria, 'matchCriteria'))[0];
        print $ipmatchCriteria;
        @ipv4list = $ixNet->getList($ipmatchCriteria, 'matchCriteria');
        foreach $ipv4names (@ipv4list) {
            if (($ixNet->getAttribute($ipv4names, '-name')) eq "IPv4 Source") {
                $ipsourcefield = ($ixNet->getList($ipv4names, 'field'))[0];
                print $ipsourcefield;
                $valuemulti = $ixNet->getAttribute($ipsourcefield, '-value');
                print $valuemulti;
                $ixNet->setAttribute($valuemulti.'/singleValue', '-value', '67.1.1.1');
                $ixNet->commit();
                sleep(5);
            } else {
                $ipdestinationfield = ($ixNet->getList($ipv4names, 'field'))[0];
                print $ipdestinationfield;
                $valuemulti = $ixNet->getAttribute($ipdestinationfield, '-value');
                print $valuemulti;
                $ixNet->setAttribute($valuemulti.'/singleValue', '-value', '4.1.1.1');
                $ixNet->commit();
                sleep(5);
                
            }
        }
    }
}
################################################################################
# Adding match instruction action : ETHERNET, IP                               #
################################################################################
$flowProfileMatchAction = ($ixNet->getList($flowprofile, 'matchAction'))[0];
print "$flowProfileMatchAction\n";
$flowProfileInstruction = ($ixNet->getList($flowProfileMatchAction, 'instructions'))[0];
print "$flowProfileInstruction\n";
print "Adding instruction\n";
$ixNet->execute('addInstruction', $flowProfileInstruction, "Apply Actions");
$ixNet->commit();
$flowProfileInstructionAdded = ($ixNet->getList($flowProfileInstruction, 'instruction'))[0];
print "$flowProfileInstructionAdded\n";
print "Adding 2 action\n";
my @requiredaction = ("Set Ethernet Source", "Set Ethernet Destination");
print "@requiredaction\n";
foreach $action (@requiredaction) {
    $ixNet->execute('addAction', $flowProfileInstructionAdded, $action);
    $ixNet->commit();
}
$actionsAdded = ($ixNet->getList($flowProfileInstructionAdded, 'actions'))[0];
@actionList = $ixNet->getList($actionsAdded, 'action');
print "$actionList\n";
foreach $action (@actionList) {
    if (($ixNet->getAttribute($action, '-name')) eq "Set Ethernet Source") {
        print "action is Set Ethernet Source\n";
        $val = "4:6:0:0:0:0";
        print $val;
    } else {
        print "action is Set Ethernet Destination";
        $val = "7:7:4:8:1:7";
        print $val;
    }
    $field = ($ixNet->getList($action, 'field'))[0];
    print $field;
    $actionValue = $ixNet->getAttribute($field, '-value');
    print $actionValue;
    $ixNet->setAttribute($actionValue.'/singleValue', '-value', $val);
    $ixNet->commit();
}

################################################################################
# Start open flow controller and wait for 45 seconds                           #
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

print("Verifying OpenFlow Controller Per Port stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"OpenFlow Controller Per Port"/page';
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
# On the fly section                                                           #  
################################################################################

my $flowProfileMatchAction = ($ixNet->getList($flowprofile, 'matchAction'))[0];
print $flowProfileMatchAction;
my $flowProfileInstruction = ($ixNet->getList($flowProfileMatchAction, 'instructions'))[0];    
my $flowProfileInstructionAdded = ($ixNet->getList($flowProfileInstruction, 'instruction'))[0];
my $actionsAdded = ($ixNet->getList($flowProfileInstructionAdded, 'actions'))[0];
my $actionList = ($ixNet->getList($actionsAdded, 'action'))[0];
print $actionList;
if ($ixNet->getAttribute($actionList, '-name') == "Set Ethernet Source") {
    print "Modifying Set Ethernet Source  Value OTF to 16:44:33:2:1:1";
    $val = "16:44:33:2:1:1";
    }
my $Ethernetfield = ($ixNet->getList($actionList, 'field'))[0];
my $actionValue = ($ixNet->getAttribute($Ethernetfield, '-value'));
$ixNet->setAttribute($actionValue .'/singleValue', '-value', $val);
$ixNet->commit();   

my $globals   = ($ixNet->getRoot()).'/globals';
my $topology  = $globals.'/topology';
print("Applying changes on the fly\n");
$ixNet->execute('applyOnTheFly', $topology);
sleep(5);

###############################################################################
# print learned info                                                          #
###############################################################################
$ixNet->execute('getOFChannelLearnedInfo', $openFlowController1, '1');
sleep(5);

print("Print OF Channel Learned Info \n");
my $learnedInfoList = ($ixNet->getList($openFlowController1, 'learnedInfo'))[0];
my $learnedInfo = ($learnedInfoList, 'end')[0];
my $table = ($ixNet->getList($learnedInfo, 'table'))[0];
my @learnedInfoColumnsList = ($ixNet->getAttribute($table, '-columns'));
my @learnedInfoValuesList = ($ixNet->getAttribute($table, '-values'));
my @row2 = (@learnedInfoValuesList) [1];
print("@learnedInfoColumnsList\n");
my $v      = '';
print("***************************************************\n");
foreach $v (@row2) {
     my $w = '0';
    foreach $w (@$v) {
        printf("%10s", $w);
    }
    print("\n");
}
print("***************************************************\n");

print "Set on demand message for flow stat!!!!";
my $OfChanneLearnedinfoList = ($ixNet->getList($openFlowController1, 'ofChannelLearnedInfoList'))[0];
my $OnDemandMessage = ($ixNet->getAttribute($OfChanneLearnedinfoList, '-onDemandMessages'));
my @values1 = ($ixNet->getAttribute($OnDemandMessage, '-values'))[0];
$ixNet->setAttribute($OnDemandMessage.'/singleValue', '-value', "flowstat");
print "sending on demand message on the fly for flow stat learned info";
$ixNet->execute('sendOnDemandMessage', $OfChanneLearnedinfoList, 1);
sleep(5);

################################################################################
# Stop all protocols                                                           #
################################################################################
$ixNet->execute('stopAllProtocols');
print("!!! Test Script Ends !!!\n");





