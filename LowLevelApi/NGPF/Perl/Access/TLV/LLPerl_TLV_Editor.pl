################################################################################
# Version 1.0    $Revision: #1 $                                                #
#                                                                              #
#    Copyright ? 1997 - 2014 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    10/2/2014 - Vlad Mihai - created sample                         #
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
# The script creates one Custom TLV and adds it and another predefined TLV     #
# to the configuration.                                                        #
# Start/Stop protocols.                                                        #
# Module:                                                                      #
#    The sample was tested on an FlexAP10G16S module.                          #
# Software:                                                                    #
#    IxOS      6.80 EA                                                         #
#    IxNetwork 7.40 EA                                                         #
#                                                                              #
################################################################################


$py_ixTclServer = "ixro-smqa-r-22";
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
$ixNet->connect($py_ixTclServer, '-port', $py_ixTclPort, '-version', '7.40');

print "\n Clear the configuration.";
$asyncHandle = $ixNet->setAsync()->execute('newConfig');
$ixNet->wait($asyncHandle);

print "\n\n Adding 2 virtual ports.";
$root 	= $ixNet->getRoot();
$vport1 	= $ixNet->add($root, 'vport', '-name', 'DHCP1');
$vport2 	= $ixNet->add($root, 'vport', '-name', 'DHCP2');
$ixNet->commit();

@vPorts = $ixNet->getList($root, 'vport');
print "\n\t\tvPorts: ",@vPorts,"\n";
$vportTx 	= @vPorts[0];
$vportRx 	= @vPorts[1];

print "\n Adding 2 topologies.";
$ixNet->add($root, 'topology');
$ixNet->add($root, 'topology');
$ixNet->commit();

@topologies = $ixNet->getList($root, 'topology');
print "\n\t\tTopology: ",@topologies,"\n";
$topo1 	= @topologies[0];
$topo2 	= @topologies[1];


print "\n Adding deviceGroups.";
$ixNet->add($topo1, 'deviceGroup');
$ixNet->add($topo2, 'deviceGroup');
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


print "\n Change topologies and and device group names.";
$ixNet->setAttribute($topo1, '-name',  'Server Topology');
$ixNet->setAttribute($topo2, '-name',  'Client Topology');
$ixNet->setAttribute($t1dev1, '-name', 'Server Device Group');
$ixNet->setAttribute($t2dev1, '-name', 'Client Device Group');


print "\n Set Device Groups multipliers.";
$ixNet->setAttribute($t1dev1, '-multiplier', 1);
$ixNet->setAttribute($t2dev1, '-multiplier', 10);
$ixNet->commit();


print "\n Adding ethernet layer.";
$ixNet->add($t1dev1, 'ethernet');
$ixNet->add($t2dev1, 'ethernet');
$ixNet->commit();

@mac1 	= $ixNet->getList($t1dev1, 'ethernet');
@mac2 	= $ixNet->getList($t2dev1, 'ethernet');


print "\n Adding DHCPv4 server and DHCPv4 client layers. DHCPv4 server goes over IPv4 layer.";
$ixNet->add($mac1[0], 'ipv4');
$ixNet->commit();

@ipv4T		= $ixNet->getList($mac1[0], 'ipv4');
$ipv4	 	= $ipv4T[0];

$ixNet->add($ipv4, 'dhcpv4server');
$ixNet->commit();

@serverv4T 	= $ixNet->getList($ipv4, 'dhcpv4server');
$dhcpServer	= $serverv4T[0];

$ixNet->add($mac2[0], 'dhcpv4client');
$ixNet->commit();

@clientv4T 	= $ixNet->getList($mac2[0], 'dhcpv4client');
$dhcpClient 	= $clientv4T[0];


print "\n Set the IP address of the DHCPv4 Server.";
$multivalue_ipAddress	= $ixNet->getAttribute($ipv4, '-address');
@temp2					= $ixNet->setAttribute($multivalue_ipAddress, '-pattern', 'counter');
$ixNet->commit();

@multivalue_ipAddress_counter	= $ixNet->getList($multivalue_ipAddress, 'counter');
$multivalue_ipAddress_start 	= $ixNet->setAttribute($multivalue_ipAddress_counter[0], '-start', '22.1.1.1');
$ixNet->commit();


print "\n Set IP layer to not resolve gateway IP.";
$multivalue_gateway		= $ixNet->getAttribute($ipv4, '-resolveGateway');

@multivalue_gateway_sv			= $ixNet->getList($multivalue_gateway, 'singleValue');
$multivalue_gateway_sv_value 	= $ixNet->setAttribute($multivalue_gateway_sv[0], '-value', 'false');
$ixNet->commit();


print "\n Set start IP address to be leased by the DHCPv4 Server.";
@serverSess 			= $ixNet->getList($dhcpServer, 'dhcp4ServerSessions');
$multivalue_poolAddress	= $ixNet->getAttribute($serverSess[0], '-ipAddress');

@multivalue_poolAddress_counter	= $ixNet->getList($multivalue_poolAddress, 'counter');
$multivalue_poolAddress_start 	= $ixNet->setAttribute($multivalue_poolAddress_counter[0], '-start', '22.1.1.100');
$ixNet->commit();


print "\n Set pool size.";
$multivalue_poolSize	= $ixNet->getAttribute($serverSess[0], '-poolSize');

@multivalue_poolSize_sv			= $ixNet->getList($multivalue_poolSize, 'singleValue');
$multivalue_poolSize_sv_value	= $ixNet->setAttribute($multivalue_poolSize_sv[0], '-value', '10');
$ixNet->commit();


$chassis1  = '10.205.15.90';
$card1     = '11';
$port1     = '3';

$card2     = '11';
$port2     = '4';

$chassis = $ixNet->add($ixNet->getRoot().'availableHardware', 'chassis', '-hostname', $chassis1);
$ixNet->commit();
@chassisItems = $ixNet->remapIds($chassis);
$chassis = $chassisItems[0];


print "\n\n Assign hardware ports to virtual ports.";
$ixNet->setAttribute($vport1, '-connectedTo', $chassis.'/card:'.$card1.'/port:'.$port1);
$ixNet->setAttribute($vport2, '-connectedTo', $chassis.'/card:'.$card2.'/port:'.$port2);
$ixNet->commit();

# ###################### Create a Custom TLV ################################ #
# ###################### Create a Custom TLV ################################ #
# ###################### Create a Custom TLV ################################ #


print "\nGet global templates";
@global_config = $ixNet->getList($root, 'globals');
@global_top = $ixNet->getList($global_config[0], 'topology');
@global_dhcp = $ixNet->getList($global_top[0], 'dhcpv4client');
@global_tlv_editor = $ixNet->getList($global_dhcp[0], 'tlvEditor');
@global_defaults = $ixNet->getList($global_tlv_editor[0], 'defaults');
@global_default_template = $ixNet->getList($global_defaults[0], 'template');


print "\nCreate a custom TLV";

print "\nAdd a new template";
@new_template = $ixNet->add($global_tlv_editor[0], "template");
$ixNet->commit();

print "\nChange the name";
$ixNet->setAttribute($new_template[0], "-name", "Test Template");
$ixNet->commit();

print "\nAdd a new TLV";
@new_tlv = $ixNet->add($new_template[0], "tlv");
$ixNet->commit();

print "\nChange the name";
$ixNet->setAttribute($new_tlv[0], "-name", "Test TLV");
$ixNet->commit();

print "\nModify Length";

@new_tlv_length = $ixNet->getList($new_tlv[0], "length");

print "\nModify Length Attributes";

print "\nSet the name";
$ixNet->setAttribute($new_tlv_length[0], "-name", "Length");
$ixNet->commit();

print '\nChange the Value for Length';
@value_mv = $ixNet->getAttribute($new_tlv_length[0], '-value');
$ixNet->setAttribute($value_mv[0], '-pattern', 'singleValue');
$ixNet->commit();
@value_mv_singleValue = $ixNet->getList($value_mv[0], 'singleValue');
$ixNet->setMultiAttribute($value_mv_singleValue[0], '-value', '2');
$ixNet->commit();


print "\nModify type";

@new_tlv_type = $ixNet->getList($new_tlv[0], "type");

print "\nSet the name";
$ixNet->setAttribute($new_tlv_type[0], "-name", "Type");
$ixNet->commit();

@new_object = $ixNet->add($new_tlv_type[0], "object");
$ixNet->commit();

@new_field = $ixNet->add($new_object[0], "field");
$ixNet->commit();

print "\nModify Field Attributes";

print "\nSet the name";
$ixNet->setAttribute($new_field[0], "-name", "Code");
$ixNet->commit();

print '\nChange the Code for Type';
@value_mv = $ixNet->getAttribute($new_field[0], '-value');
$ixNet->setAttribute($value_mv[0], '-pattern', 'singleValue');
$ixNet->commit();
@value_mv_singleValue = $ixNet->getList($value_mv[0], 'singleValue');
$ixNet->setMultiAttribute($value_mv_singleValue[0], '-value', '150');
$ixNet->commit();

print "\nModify value";
@new_value = $ixNet->getList($new_tlv[0], "value");

print "\nEdit Value Atributes";

print "\nSet the name";
$ixNet->setAttribute($new_value[0], "-name", "Value");
$ixNet->commit();

print "\nAdd a container with two fields";
@new_object = $ixNet->add($new_value[0], "object");
@new_container = $ixNet->add($new_object[0], "container");
@new_object_1 = $ixNet->add($new_container[0], "object");
@new_object_2 = $ixNet->add($new_container[0], "object");

@new_field_1 = $ixNet->add($new_object_1[0], "field");
@new_field_2 = $ixNet->add($new_object_2[0], "field");
$ixNet->commit();

print "\nModify Field Attributes";

print "\nSet the name";
$ixNet->setAttribute($new_field_1[0], "-name", "Field_1");
$ixNet->commit();

print '\nChange the Value for Field_1';
@value_mv = $ixNet->getAttribute($new_field_1[0], '-value');
$ixNet->setAttribute($value_mv[0], '-pattern', 'singleValue');
$ixNet->commit();
@value_mv_singleValue = $ixNet->getList($value_mv[0], 'singleValue');
$ixNet->setMultiAttribute($value_mv_singleValue[0], '-value', '4');
$ixNet->commit();

print "\nSet the name";
$ixNet->setAttribute($new_field_1[0], "-name", "Field_2");
$ixNet->commit();

print '\nChange the Value for Field_2';
@value_mv = $ixNet->getAttribute($new_field_2[0], '-value');
$ixNet->setAttribute($value_mv[0], '-pattern', 'singleValue');
$ixNet->commit();
@value_mv_singleValue = $ixNet->getList($value_mv[0], 'singleValue');
$ixNet->setMultiAttribute($value_mv_singleValue[0], '-value', '5');
$ixNet->commit();


print "\nAdd a subTlv with two fields";

@new_object = $ixNet->add($new_value[0], "object");
@new_subtlv = $ixNet->add($new_object[0], "subTlv");
$ixNet->commit();

print "\nModify Length";

@new_tlv_length = $ixNet->getList($new_subtlv[0], "length");

print "\nModify Length Attributes";

print "\nSet the name";
$ixNet->setAttribute($new_tlv_length[0], "-name", "Length");
$ixNet->commit();

print '\nChange the Value for Length';
@value_mv = $ixNet->getAttribute($new_tlv_length[0], '-value');
$ixNet->setAttribute($value_mv[0], '-pattern', 'singleValue');
$ixNet->commit();
@value_mv_singleValue = $ixNet->getList($value_mv[0], 'singleValue');
$ixNet->setMultiAttribute($value_mv_singleValue[0], '-value', '2');
$ixNet->commit();


print "\nModify type";

@new_tlv_type = $ixNet->getList($new_subtlv[0], "type");

print "\nSet the name";
$ixNet->setAttribute($new_tlv_type[0], "-name", "Type");
$ixNet->commit();

@new_object = $ixNet->add($new_tlv_type[0], "object");
$ixNet->commit();

@new_field = $ixNet->add($new_object[0], "field");
$ixNet->commit();

print "\nModify Field Attributes";

print "\nSet the name";
$ixNet->setAttribute($new_field[0], "-name", "Code");
$ixNet->commit();

print "\nChange the Code for Type";
@value_mv = $ixNet->getAttribute($new_field[0], '-value');
$ixNet->setAttribute($value_mv[0], '-pattern', 'singleValue');
$ixNet->commit();
@value_mv_singleValue = $ixNet->getList($value_mv[0], 'singleValue');
$ixNet->setMultiAttribute($value_mv_singleValue[0], '-value', '1');
$ixNet->commit();


print "\nAdding the two fields";

@new_value = $ixNet->getList($new_subtlv[0], "value");

@new_object_1 = $ixNet->add($new_value[0], "object");
@new_object_2 = $ixNet->add($new_value[0], "object");

@new_field_1 = $ixNet->add($new_object_1[0], "field");
@new_field_2 = $ixNet->add($new_object_2[0], "field");
$ixNet->commit();

print "\nModify Field Attributes";

print "\nSet the name";
$ixNet->setAttribute($new_field_1[0], "-name", "Field_1");
$ixNet->commit();

print "\nChange the Value for Field_1";
@value_mv = $ixNet->getAttribute($new_field_1[0], '-value');
$ixNet->setAttribute($value_mv[0], '-pattern', 'singleValue');
$ixNet->commit();
@value_mv_singleValue = $ixNet->getList($value_mv[0], 'singleValue');
$ixNet->setMultiAttribute($value_mv_singleValue[0], '-value', '4');
$ixNet->commit();

print "\nSet the name";
$ixNet->setAttribute($new_field_2[0], "-name", "Field_2");
$ixNet->commit();

print "\nChange the Value for Field_2";
@value_mv = $ixNet->getAttribute($new_field_2[0], '-value');
$ixNet->setAttribute($value_mv[0], '-pattern', 'singleValue');
$ixNet->commit();
@value_mv_singleValue = $ixNet->getList($value_mv[0], 'singleValue');
$ixNet->setMultiAttribute($value_mv_singleValue[0], '-value', '5');
$ixNet->commit();

# ###################### End Create a Custom TLV ################################ #

# ###################### Add TLVs to DCPv4 Client ############################## #
# ###################### Add TLVs to DCPv4 Client ############################## #
# ###################### Add TLVs to DCPv4 Client ############################## #

@dhcpv4_tlvProfile = $ixNet->getList($dhcpClient, 'tlvProfile');

print "\nGetting default TLV";
@dhcp_default_tlv = $ixNet->getList($dhcpv4_tlvProfile[0], 'defaultTlv');

print "\nAdding TLVs to the DHCP client";
$prototype_custom_tlv_1_name = 'Test TLV';
$prototype_predefined_tlv_1_name = '[12] Host Name';

@global_predefined_tlv_1 = $ixNet->getFilteredList($global_default_template[0], 'tlv', '-name', $prototype_predefined_tlv_1_name);
@global_predefined_custom_tlv_1 = $ixNet->getFilteredList($new_template[0], 'tlv', '-name', $prototype_custom_tlv_1_name);

@predefined_tlv_1 = $ixNet->execute("copyTlv", $dhcpv4_tlvProfile[0], $global_predefined_tlv_1[0]);
$ixNet->commit();
@custom_tlv_1 = $ixNet->execute("copyTlv", $dhcpv4_tlvProfile[0], $global_predefined_custom_tlv_1[0]);
$ixNet->commit();

@messages = $ixNet->getAttribute($predefined_tlv_1[0], '-availableIncludeInMessages');
$discover = $messages[0];
$request = $messages[1];
$decline = $messages[2];
$release = $messages[3];

# ###################### Configure TLV values ############################## #
print "\nConfigure TLV values";

print "\nChange the Value for TLV 18";
@predefined_tlv_1_value = $ixNet->getList($predefined_tlv_1[0], 'value');
@predefined_tlv_1_value_object = $ixNet->getList($predefined_tlv_1_value[0], 'object');
@predefined_tlv_1_value_object_field = $ixNet->getList($predefined_tlv_1_value_object[0], 'field');

@value_mv = $ixNet->getAttribute($predefined_tlv_1_value_object_field[0], '-value');
$ixNet->setAttribute($value_mv[0], '-pattern', 'singleValue');
$ixNet->commit();
@value_mv_singleValue = $ixNet->getList($value_mv[0], 'singleValue');
$ixNet->setMultiAttribute($value_mv_singleValue[0], '-value', 'Custom_Value');
$ixNet->commit();

print "\nEnable SubTlv 1 for the Default TLV, Option 55";
@default_tlv_1_value = $ixNet->getList($dhcp_default_tlv[0], 'value');
@default_tlv_1_value_object = $ixNet->getList($predefined_tlv_1_value[0], 'object');
@default_tlv_1_value_object_field = $ixNet->getList($predefined_tlv_1_value_object[0], 'field');
$ixNet->setAttribute($default_tlv_1_value_object_field[0], '-isEnabled', 'true');
$ixNet->commit();

print "\nChange the Value for one of the fields in the sub Tlv of the custom created TLV";

@custom_tlv_1_value = $ixNet->getList($custom_tlv_1[0], 'value');



@custom_tlv_1_value_object_1 = $ixNet->getList($custom_tlv_1_value[0], 'object');

@custom_tlv_1_value_object_1_subTlv = $ixNet->getList($custom_tlv_1_value_object_1[1], 'subTlv');

@subTlv_value = $ixNet->getList($custom_tlv_1_value_object_1_subTlv[0], 'value');

@subTlv_value_object_1 = $ixNet->getList($subTlv_value[0], 'object');

@custom_tlv_1_value_object_1_field = $ixNet->getList($subTlv_value_object_1[0], 'field');

print "\nDebug 3";
@value_mv = $ixNet->getAttribute($custom_tlv_1_value_object_1_field[0], '-value');
$ixNet->setAttribute($value_mv[0], '-pattern', 'singleValue');
$ixNet->commit();
@value_mv_singleValue = $ixNet->getList($value_mv[0], 'singleValue');
$ixNet->setMultiAttribute($value_mv_singleValue[0], '-value', '20');
$ixNet->commit();

print "\nSet Include in Messages";

$ixNet->setAttribute($predefined_tlv_1[0], '-includeInMessages', ($discover,$request,$release));
$ixNet->setAttribute($dhcp_default_tlv[0], '-includeInMessages', ($discover,$request,$decline));
$ixNet->setAttribute($custom_tlv_1[0], '-includeInMessages', ($request, $release));
$ixNet->commit();


# ################################### Dynamics ############################### #
#starting topologies


print "\n\n Assign hardware ports to virtual ports.";
$ixNet->setAttribute($vport1, '-connectedTo', $chassis.'/card:'.$card1.'/port:'.$port1);
$ixNet->setAttribute($vport2, '-connectedTo', $chassis.'/card:'.$card2.'/port:'.$port2);
$ixNet->commit();


print "\n\n Start All Protocols.";
$ixNet->execute('startAllProtocols');
sleep(10);


print "\n\n DHCPv4 Client Learned Information: \n";
@addresses	= $ixNet->getAttribute($dhcpClient, '-discoveredAddresses');
print join("\n ", @addresses);


print "\n\n Stop the DHCP Server.";
$ixNet->execute('stop', $mac1[0]);
sleep(10);


print "\n\n Stop the DHCP Client.";
$ixNet->execute('stop', $mac2[0]);
sleep(10);


print "\n\n Clear the configuration.";
$asyncHandle = $ixNet->setAsync()->execute('newConfig');
$ixNet->wait($asyncHandle);


print "\n\n Disconnect from the IxNetwork Client.\n";
$ixNet->disconnect();
