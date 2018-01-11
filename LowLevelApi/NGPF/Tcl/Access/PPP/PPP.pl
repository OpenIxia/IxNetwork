################################################################################
# Version 1.0    $Revision: #2 $                                                #
#                                                                              #
#    Copyright © 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    13/08/2013 - Alexandra Apetroaei - created sample                         #
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
# The script creates and configures 2 PPP stacks.							   #
# Set/Get multivalue parameters.							                   #
# Start/Stop protocols.                                                        #
# Module:                                                                      #
#    The sample was tested on an FlexAP10G16S module.                          #
# Software:                                                                    #
#    IxOS      6.70 EA                                                         #
#    IxNetwork 7.30 EA                                                         #
#                                                                              #
################################################################################
            

$py_ixTclServer = "localhost";
$py_ixTclPort	= 8009;

#-----------------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------Import Lib and Other pl packages---------------------------------------------------# 
use IxNetwork;
#use Time::Seconds;
#use strict;
#-----------------------------------------------------------------------------------------------------------------------------------#


print "\n Create an instance of the IxNetwork class.";
$ixNet 	= new IxNetwork();


print "\n Connecting to the Client.\n";
$ixNet->connect($py_ixTclServer, '-port', $py_ixTclPort, '-version', '7.30');


print "\n Clear the configuration.";
$asyncHandle = $ixNet->setAsync()->execute('newConfig');
$ixNet->wait($asyncHandle);


print "\n\n Adding 2 virtual ports.";
$root 	= $ixNet->getRoot();
$vport1 	= $ixNet->add($root, 'vport', '-name', 'PPP1');
$vport2 	= $ixNet->add($root, 'vport', '-name', 'PPP2');
$ixNet->commit();

@vPorts = $ixNet->getList($root, 'vport');
print "\n\t\tvPorts: ",@vPorts,"\n";
$vportTx 	= @vPorts[0];
$vportRx 	= @vPorts[1];


print "\n Adding 2 topologies.";
$ixNet->add($root, 'topology', '-name',  'Client Topology');
$ixNet->add($root, 'topology', '-name',  'Server Topology');
$ixNet->commit();

@topologies = $ixNet->getList($root, 'topology');
print "\n\t\tTopology: ",@topologies,"\n";
$topo1 	= @topologies[0];
$topo2 	= @topologies[1];


print "\n Adding deviceGroups and set multipliers.";
$ixNet->add($topo1, 'deviceGroup', '-name', 'Client Device Group', '-multiplier', 20);
$ixNet->add($topo2, 'deviceGroup', '-name', 'Server Device Group', '-multiplier', 1);
$ixNet->commit();

@t1devices 	= $ixNet->getList($topo1, 'deviceGroup');
@t2devices 	= $ixNet->getList($topo2, 'deviceGroup');
print "\n\t\tDeviceGroup: ",@t1devices," for ",$topo1,"\n";
print "\n\t\tDeviceGroup: ",@t2devices," for ",$topo2,"\n";

$t1dev1 	= @t1devices[0];
$t2dev1 	= @t2devices[0];


print "\n Assign vports to topologies.";
$ixNet->setAttribute($topo1, '-vports', $vportTx);
$ixNet->setAttribute($topo2, '-vports', $vportRx);
$ixNet->commit();


print "\n Adding ethernet layer.";
$ixNet->add($t1dev1, 'ethernet');
$ixNet->add($t2dev1, 'ethernet');
$ixNet->commit();

@mac1 	= $ixNet->getList($t2dev1, 'ethernet');
@mac2 	= $ixNet->getList($t1dev1, 'ethernet');


print "\n Adding PPP layers. ";
$ixNet->add($mac1[0], 'pppoxserver');
$ixNet->add($mac2[0], 'pppoxclient');
$ixNet->commit();

@serverT 	= $ixNet->getList($mac1[0], 'pppoxserver');
@clientT 	= $ixNet->getList($mac2[0], 'pppoxclient');
$server		= $serverT[0];
$client 	= $clientT[0];


print "\n Set the PPP Server Sessions Count to 20.";
$ixNet->setAttribute($server, '-sessionsCount', 20);
$ixNet->commit();


print "\n Set NCP type to dual stack.";
$multivalue_ncp1		= $ixNet->getAttribute($client, '-ncpType');
$multivalue_ncp2		= $ixNet->getAttribute($server, '-ncpType');

@multivalue_ncp_sv1			= $ixNet->getList($multivalue_ncp1, 'singleValue');
@multivalue_ncp_sv2			= $ixNet->getList($multivalue_ncp2, 'singleValue');

$ixNet->setAttribute($multivalue_ncp_sv1[0], '-value', 'dual_stack');
$ixNet->setAttribute($multivalue_ncp_sv2[0], '-value', 'dual_stack');
$ixNet->commit();


$chassis1  = '10.205.15.62';
$card1     = '2';
$port1     = '15';

$card2     = '2';
$port2     = '16';

$chassis = $ixNet->add($ixNet->getRoot().'availableHardware', 'chassis', '-hostname', $chassis1);
$ixNet->commit();
@chassisItems = $ixNet->remapIds($chassis);
$chassis = $chassisItems[0];


print "\n\n Assign hardware ports to virtual ports.";
$ixNet->setAttribute($vport1, '-connectedTo', $chassis.'/card:'.$card1.'/port:'.$port1);
$ixNet->setAttribute($vport2, '-connectedTo', $chassis.'/card:'.$card2.'/port:'.$port2);
$ixNet->commit();


print "\n\n Start the PPP Server.";
$ixNet->execute('start', $server);
sleep(10);


print "\n\n Start the PPP Client.";
$ixNet->execute('start', $client);
sleep(10);

print "\n\n PPP Client Learned Information: \n";
@addresses_v4	= $ixNet->getAttribute($client, '-discoveredIpv4Addresses');
@addresses_v6	= $ixNet->getAttribute($client, '-discoveredIpv6Addresses');
@session_ids	= $ixNet->getAttribute($client, '-discoveredSessionIds');

print "\n IPv4 Addresses: \n";
print join("\n ", @addresses_v4);
print "\n IPv6 Addresses: \n";
print join("\n ", @addresses_v6);
print "\n Session IDs: \n";
print join("\n ", @session_ids);

print "\n\n Stop the PPP Client.";
$ixNet->execute('stop', $mac2[0]);
sleep(10);

print "\n\n Stop the PPP Server.";
$ixNet->execute('stop', $mac1[0]);
sleep(10);


print "\n\n Clear the configuration.";
$asyncHandle = $ixNet->setAsync()->execute('newConfig');
$ixNet->wait($asyncHandle);


print "\n\n Disconnect from the IxNetwork Client.\n";
$ixNet->disconnect();
