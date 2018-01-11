################################################################################
# Version 1.0    $Revision: #1 $                                                #
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
# The script creates and configures 2 L2TP stacks.							   #
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
$ixNet->add($root, 'topology', '-name',  'Server Topology');
$ixNet->add($root, 'topology', '-name',  'Client Topology');
$ixNet->commit();

@topologies = $ixNet->getList($root, 'topology');
print "\n\t\tTopology: ",@topologies,"\n";
$topo1 	= @topologies[0];
$topo2 	= @topologies[1];


print "\n Adding deviceGroups and set multipliers.";
$ixNet->add($topo1, 'deviceGroup', '-name', 'Server Device Group', '-multiplier', 2);
$ixNet->add($topo2, 'deviceGroup', '-name', 'Client Device Group', '-multiplier', 2);
$ixNet->commit();

@t1devices 	= $ixNet->getList($topo1, 'deviceGroup');
@t2devices 	= $ixNet->getList($topo2, 'deviceGroup');
print "\n\t\tDeviceGroup: ",@t1devices," for ",$topo1,"\n";
print "\n\t\tDeviceGroup: ",@t2devices," for ",$topo2,"\n";

$t1dev1 	= @t1devices[0];
$t2dev1 	= @t2devices[0];

print "\n Adding chained deviceGroup and set multipliers.";
$ixNet->add($t2dev1, 'deviceGroup', '-name', 'PPP Client Device Group', '-multiplier', 10);
$ixNet->commit();
@chained_dg 	= $ixNet->getList($t2dev1, 'deviceGroup');


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


print "\n Adding IP layers. ";
$ixNet->add($mac1[0], 'ipv4');
$ixNet->add($mac2[0], 'ipv4');
$ixNet->commit();

@ip1 	= $ixNet->getList($mac1[0], 'ipv4');
@ip2 	= $ixNet->getList($mac2[0], 'ipv4');


print "\n Adding L2TP layers. ";
$ixNet->add($ip1[0], 'lac');
$ixNet->add($ip2[0], 'lns');
$ixNet->commit();

@lacT 	= $ixNet->getList($ip1[0], 'lac');
@lnsT 	= $ixNet->getList($ip2[0], 'lns');
$lac	= $lacT[0];
$lns	= $lnsT[0];

print "\n Adding PPP Server layer. ";
$ixNet->add($lns, 'pppoxserver');
$ixNet->commit();

@ppp_server 	= $ixNet->getList($lns, 'pppoxserver');
$ppp_server		= $ppp_server[0];



print "\n Adding ethernet layer.";
$ixNet->add($chained_dg[0], 'ethernet');
$ixNet->commit();

@mac3 	= $ixNet->getList($chained_dg[0], 'ethernet');

print "\n Adding PPP Client layer. ";
$ixNet->add($mac3[0], 'pppoxclient');
$ixNet->commit();

@ppp_client 	= $ixNet->getList($mac3[0], 'pppoxclient');
$ppp_client		= $ppp_client[0];




print "\n Set the IP address of the L2TP Network Server.";
$multivalue_ipAddress	= $ixNet->getAttribute($ip2[0], '-address');
@temp2					= $ixNet->setAttribute($multivalue_ipAddress, '-pattern', 'counter');
$ixNet->commit();

@multivalue_ipAddress_counter	= $ixNet->getList($multivalue_ipAddress, 'counter');
$ixNet->setMultiAttribute($multivalue_ipAddress_counter[0], '-direction', 'increment', '-start', '22.1.1.2', '-step', '0.0.0.2');
$ixNet->commit();


print "\n Set the IP address of the L2TP Access Concentrator.";
$multivalue_ipAddress	= $ixNet->getAttribute($ip1[0], '-address');
@temp2					= $ixNet->setAttribute($multivalue_ipAddress, '-pattern', 'counter');
$ixNet->commit();

@multivalue_ipAddress_counter	= $ixNet->getList($multivalue_ipAddress, 'counter');
$ixNet->setMultiAttribute($multivalue_ipAddress_counter[0], '-direction', 'increment', '-start', '22.1.1.1', '-step', '0.0.0.2');
$ixNet->commit();


print "\n Set the LNS Destination IP address for the L2TP Access Concentrator.";
$multivalue_ipAddress	= $ixNet->getAttribute($lac, '-baseLnsIp');


# print $ixNet->getAttribute($multivalue_ipAddress, '-pattern');

@temp2					= $ixNet->setAttribute($multivalue_ipAddress, '-pattern', 'counter');
$ixNet->commit();

@multivalue_ipAddress_counter	= $ixNet->getList($multivalue_ipAddress, 'counter');
$ixNet->setMultiAttribute($multivalue_ipAddress_counter[0], '-direction', 'increment', '-start', '22.1.1.2', '-step', '0.0.0.2');
$ixNet->commit();

print "\n Set IP layer to not resolve gateway IP.";
$multivalue_gateway1		= $ixNet->getAttribute($ip1[0], '-resolveGateway');
$multivalue_gateway2		= $ixNet->getAttribute($ip2[0], '-resolveGateway');

@multivalue_gateway_sv1			= $ixNet->getList($multivalue_gateway1, 'singleValue');
@multivalue_gateway_sv2			= $ixNet->getList($multivalue_gateway2, 'singleValue');

$ixNet->setAttribute($multivalue_gateway_sv1[0], '-value', 'false');
$ixNet->setAttribute($multivalue_gateway_sv2[0], '-value', 'false');
$ixNet->commit();


print "\n Set the PPP Server Sessions Count to 10.";
$ixNet->setAttribute($ppp_server, '-sessionsCount', 10);
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
$ixNet->execute('start', $ppp_server);
sleep(10);


print "\n\n Start the PPP Client.";
$ixNet->execute('start', $ppp_client);
sleep(10);

print "\n\n PPP Client Learned Information: \n";
@addresses_v4	= $ixNet->getAttribute($ppp_client, '-discoveredIpv4Addresses');
@addresses_v6	= $ixNet->getAttribute($ppp_client, '-discoveredIpv6Addresses');
@session_ids	= $ixNet->getAttribute($ppp_client, '-discoveredSessionIds');

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
