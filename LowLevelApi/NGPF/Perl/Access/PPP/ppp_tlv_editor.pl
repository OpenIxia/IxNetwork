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
# The script is not a standard commercial product offered by Ixia Keysight and #
# have     																	   #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia Keysight and/or by the user and/or by a third party)] shall at  #
# all times 																   #
# remain the property of Ixia Keysight.                                        #
#                                                                              #
# Ixia Keysight does not warrant (i) that the functions contained in the script#
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND Ixia Keysight#
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL Ixia Keysight BE LIABLE FOR ANY DAMAGES RESULTING FROM OR  #
# ARISING   																   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF Ixia Keysight HAS BEEN ADVISED OF THE          #
# POSSIBILITY OF  SUCH DAMAGES IN ADVANCE.                                     #
# Ixia Keysight will not be required to provide any software maintenance or    #
# support services of any kind (e.g. any error corrections) in connection with #
# script or any part thereof. The user acknowledges that although Ixia Keysight# 
# may     																	   #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia Keysight to  #
# provide any additional maintenance or support services.                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    Script  will create following:                                            #
#    1. Create PPPoX Client and Server                                         #
#    2.	Setting DSL type in DSL line Attribute.                                #
#    3. Setting CUSTOM TLV in DSL Line Attribute..	     					   #
#  	 4. Setting 01 Access-Loop-Circuit-ID	   	   							   #
#	 5. Setting PON-Access-Line-Attributes									   #
#	 6. Start PPPox client and PPPox Server                             	   #
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
my $ixTclServer = '10.39.65.1';
my $ixTclPort   = '9862';
my @ports       = (('10.39.64.117', '2', '5'), ('10.39.64.117', '2', '6'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '7.40',
    '-setAttribute', 'strict');

print("Creating a new config\n");
$ixNet->execute('newConfig');

################################################################################
# 1. Adding ports to configuration
################################################################################

print "Adding ports to configuration\n";
my $root = $ixNet->getRoot();
$ixNet->add($root, 'vport');
$ixNet->add($root, 'vport');
$ixNet->commit();
my @vPorts = $ixNet->getList($root, 'vport');
my $vport1 = @vPorts[0];
my $vport2 = @vPorts[1];

sleep(20);
################################################################################
# 2.PPPoX client and server
################################################################################

print "Add topologies\n";
$ixNet->add($root, 'topology');
$ixNet->add($root, 'topology');
$ixNet->commit();
my @top = $ixNet->getList($root, 'topology');
my $topo1 = @top[0];
my $topo2 = @top[1];

print "Add ports to topologies\n";
$ixNet->setAttribute($topo1, '-vports', $vport1);
$ixNet->setAttribute($topo2, '-vports', $vport2);
$ixNet->commit();

print "Name the topologies\n";
$ixNet->setAttribute($topo1, '-name', 'PPP Servers Topology');
$ixNet->setAttribute($topo2, '-name', 'PPP Clients Topology');
$ixNet->commit();


my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vportTx = $vPorts[0];
my $vportRx = $vPorts[1];
assignPorts($ixNet, @ports, $vportTx, $vportRx);

print "Add device groups to topologies\n";
$ixNet->add($topo1, 'deviceGroup');
$ixNet->add($topo2, 'deviceGroup');
$ixNet->commit();

my @dg1 = $ixNet->getList($topo1, 'deviceGroup');
my @dg2 = $ixNet->getList($topo2, 'deviceGroup');
my $dg1_1 = @dg1[0];
my $dg2_1 = @dg2[0];


print "Add Multiplier to device groups\n";
$ixNet->setAttribute($dg1_1, 
	'-multiplier', '2', 
	'-name', 'PPP Servers');
$ixNet->commit();

$ixNet->setAttribute($dg2_1, 
	'-multiplier', '5', 
	'-name', 'PPP Clients');
$ixNet->commit();

print "Add Ethernet stacks to device groups\n";
$ixNet->add($dg1_1, 'ethernet');
$ixNet->add($dg2_1, 'ethernet');
$ixNet->commit();

my @mac1 = $ixNet->getList($dg1_1, 'ethernet');
my @mac2 = $ixNet->getList($dg2_1, 'ethernet');
my $mac1_1 = @mac1[0];
my $mac2_1 = @mac2[0];

print "Add PPPox Clients and Server";
my $pppox_server = $ixNet->add($mac1_1, 'pppoxserver');
my $pppox_client = $ixNet->add($mac2_1, 'pppoxclient');
$ixNet->commit();

$ixNet->setAttribute($pppox_server, 
	'-sessionsCount', '5', 
	'-stackedLayers', [], 
	'-name', 'PPPoX Server 1');
$ixNet->commit();

$ixNet->setAttribute($pppox_client, 
	'-stackedLayers', [], 
	'-name', 'PPPoX Client 1');
$ixNet->commit();

my @tlv_profile_1 = $ixNet->getList($pppox_client, 'tlvProfile');
my $tlv_profile = @tlv_profile_1[0];
print "\n Get Global templates ...";
my @global = $ixNet->getList($root, 'globals');
my $global_config = @global[0];
my @global_topology = $ixNet->getList($global_config, 'topology');
my $global_top = @global_topology[0];
my @glob_bgre = $ixNet->getList($global_top, 'pppoxclient');
my $global_bgre = @glob_bgre[0];
my @glob_tlv = $ixNet->getList($global_bgre, 'tlvEditor');
my $global_tlv_editor = @glob_tlv[0];
my @global_default_tlv = $ixNet->getList($global_tlv_editor, 'defaults');
my $global_tlv_default = @global_default_tlv[0];
my @glob_temp = $ixNet->getList($global_tlv_default, 'template');
my $global_template = @glob_temp[0];

print "\n Global templates : $global_template...";

# #############################################################################
#  Create DSL line Attribute and fetch DSL Line subtlv and custom sub tlv parameters
# #############################################################################
# This part is doing following:
# 1. Create DSL line Attribute TLV
# 2. Fetch [84] Minimum-Net-Data-Rate-Downstream sub tlv value handle
#	 Sub TLV API path is :::ixNet::OBJ-/topology:2/deviceGroup:1/ethernet:1/pppoxclient:1/tlvProfile/tlv:1/value/object:5
# 3. Fetch [00] Custom TLV sub tlv value handle and type handle
#    Sub TLV API Path is : ::ixNet::OBJ-/topology:2/deviceGroup:1/ethernet:1/pppoxclient:1/tlvProfile/tlv:1/value/object:26

print "\n Creating DSL-Line-Attributes";
my $dsl = 'DSL-Line-Attributes';
# Get DSL Line attribute TLV from many default templates
my @dsl_line_attribute_array = $ixNet->getFilteredList($global_template, 'tlv', '-name', $dsl);
my $dsl_line_attribute = @dsl_line_attribute_array[0];
print "\n dsl_line_attribute : $dsl_line_attribute...";
$ixNet->commit();


# Copy DSL Line attribute TLV template to tlv profile
my $dsl_line_attribute_tlv = $ixNet->execute('copyTlv', $tlv_profile, $dsl_line_attribute);
$ixNet->commit();

my $req_tlv = "::ixNet::OBJ-/topology:2/deviceGroup:1/ethernet:1/pppoxclient:1/tlvProfile/tlv:1/value/object:5";
my @sub_tlv_array = $ixNet->getList($req_tlv, 'subTlv');
my $sub_tlv = @sub_tlv_array[0];
print "\n sub_tlv: $sub_tlv \n";

#Enable [84] Minimum-Net-Data-Rate-Downstream sub tlv 
$ixNet->setMultiAttribute($sub_tlv, '-isEnabled', 'true');
$ixNet->commit();

print "\n Change the type for tlv name $req_tlv to value 456";
# Get sub-tlv value
my @dsl_type_tlv_value = $ixNet->getList($sub_tlv, 'value');
# Get Sub-tlv value object
my @dsl_type_tlv_obj = $ixNet->getList($dsl_type_tlv_value[0], 'object');

# Get Sub-Tlv field value
my @dsl_type_field = $ixNet->getList($dsl_type_tlv_obj[0], 'field');

my @dsl_type_tlv_field_value = $ixNet->getAttribute($dsl_type_field[0], '-value');

my $dsl_counter_value = $ixNet->add($dsl_type_tlv_field_value[0], 'singleValue');;
$ixNet->setMultiAttribute($dsl_counter_value, 
	'-value', '456');
$ixNet->commit();


print "\n *******Enable Custom TLV inside DSL line atrributes*********";
my $req_custom_tlv = "::ixNet::OBJ-/topology:2/deviceGroup:1/ethernet:1/pppoxclient:1/tlvProfile/tlv:1/value/object:26";
my @sub_tlv__custom_array = $ixNet->getList($req_custom_tlv, 'subTlv');
my $sub_tlv_custom = @sub_tlv__custom_array[0];
print "\n sub_tlv_custom: $sub_tlv_custom \n";

#Enable [84] Minimum-Net-Data-Rate-Downstream sub tlv 
$ixNet->setMultiAttribute($sub_tlv_custom, '-isEnabled', 'true');
$ixNet->commit();

print "\n Change the value for tlv name $req_custom_tlv to value 12345";
# Get sub-tlv value
my @custom_tlv_value = $ixNet->getList($sub_tlv_custom, 'value');
# Get Sub-tlv value object
my @custom_tlv_obj = $ixNet->getList($custom_tlv_value[0], 'object');

# Get Sub-Tlv field value
my @custom_field = $ixNet->getList($custom_tlv_obj[0], 'field');

my @custom_tlv_field_value = $ixNet->getAttribute($custom_field[0], '-value');

my $custom_counter_value = $ixNet->add($custom_tlv_field_value[0], 'singleValue');;
$ixNet->setMultiAttribute($custom_counter_value, 
	'-value', '12345');
$ixNet->commit();


print "\n Change the type for tlv name $req_custom_tlv to value cc";
# Get sub-tlv value
my @custom_type_tlv_value = $ixNet->getList($sub_tlv_custom, 'type');
# Get Sub-tlv value object
my @custom_type_tlv_obj = $ixNet->getList($custom_type_tlv_value[0], 'object');

# Get Sub-Tlv field value
my @custom_type_field = $ixNet->getList($custom_type_tlv_obj[0], 'field');

my @custom_type_tlv_field_value = $ixNet->getAttribute($custom_type_field[0], '-value');

my $custom_counter_value = $ixNet->add($custom_type_tlv_field_value[0], 'singleValue');;
$ixNet->setMultiAttribute($custom_counter_value, 
	'-value', 'cc');
$ixNet->commit();


#############################################################################
#      Setting Access-Loop-Circuit-ID..
#############################################################################

# Create [01] Access-Loop-Circuit-ID TLV and enable using tlv_is_enabled parameter
print "\n 	Setting 01 Access-Loop-Circuit-ID.";
my $access_loop = '[01] Access-Loop-Circuit-ID';

# Get [01] Access-Loop-Circuit-ID TLV from many default templates
my @access_loop_circuit_array = $ixNet->getFilteredList($global_template, 'tlv', '-name', $access_loop);
my $access_loop_circuit = @access_loop_circuit_array[0];
print "\n access_loop_circuit : $access_loop_circuit...";
$ixNet->commit();


# Copy [01] Access-Loop-Circuit-ID TLV template to tlv profile
my $access_loop_tlv = $ixNet->execute('copyTlv', $tlv_profile, $access_loop_circuit);
$ixNet->commit();

print "\n Change the type for tlv name $access_loop_tlv to value 456";
# Get tlv value
my @access_loop_tlv_value = $ixNet->getList($access_loop_tlv, 'value');
# Get tlv value object
my @access_loop_tlv_object = $ixNet->getList($access_loop_tlv_value[0], 'object');

# Get Tlv field value
my @access_loop_tlv_field = $ixNet->getList($access_loop_tlv_object[0], 'field');

my @dsl_type_tlv_field_value = $ixNet->getAttribute($access_loop_tlv_field[0], '-value');

my $access_loop_single_value = $ixNet->add($dsl_type_tlv_field_value[0], 'singleValue');;
$ixNet->setMultiAttribute($access_loop_single_value, 
	'-value', 'circuit1');
$ixNet->commit();


#############################################################################
#    Setting PON-Access-Line-Attributes..
#############################################################################
# This part is doing following:
# 1. Create PON-Access-Line-Attributes
# 2. Fetch [96] ONT/ONU-Assured-Data-Rate-Upstream handle 
#	 Sub TLV API path is : /topology:2/deviceGroup:1/ethernet:1/pppoxclient:1/tlvProfile/tlv:3/value/object:5/subTlv


print "\n Setting PON-Access-Line-Attributes";
my $pon_attribute = 'PON-Access-Line-Attributes';
# Get DSL Line attribute TLV from many default templates
my @pon_attribute_data_array = $ixNet->getFilteredList($global_template, 'tlv', '-name', $pon_attribute);
my $pon_attribute_data = @pon_attribute_data_array[0];
print "\n pon_attribute_data : $pon_attribute_data...";
$ixNet->commit();


# Copy PON-Access-Line-Attributes template to tlv profile
my $pon_attribute_tlv = $ixNet->execute('copyTlv', $tlv_profile, $pon_attribute_data);
$ixNet->commit();

my $req_pon_tlv = "::ixNet::OBJ-/topology:2/deviceGroup:1/ethernet:1/pppoxclient:1/tlvProfile/tlv:3/value/object:5";
my @req_pon_tlv_array = $ixNet->getList($req_pon_tlv, 'subTlv');
my $req_pon_tlv_subtlv = @req_pon_tlv_array[0];
print "\n req_pon_tlv_subtlv: $req_pon_tlv_subtlv \n";

#Enable [96] ONT/ONU-Assured-Data-Rate-Upstream tlv
$ixNet->setMultiAttribute($req_pon_tlv_subtlv, '-isEnabled', 'true');
$ixNet->commit();

print "\n Change the type for tlv name $pon_attribute to value 876\n";
# Get sub-tlv value
my @pon_type_tlv_value = $ixNet->getList($req_pon_tlv_subtlv, 'value');
# Get Sub-tlv value object
my @pon_type_tlv_obj = $ixNet->getList($pon_type_tlv_value[0], 'object');

# Get Sub-Tlv field value
my @pon_type_field = $ixNet->getList($pon_type_tlv_obj[0], 'field');

my @pon_type_tlv_field_value = $ixNet->getAttribute($pon_type_field[0], '-value');

my $pon_counter_value = $ixNet->add($pon_type_tlv_field_value[0], 'singleValue');;
$ixNet->setMultiAttribute($pon_counter_value, 
	'-value', '876');
$ixNet->commit();




###############################################################################
#Start protocol 
###############################################################################

print("\n Starting protocol\n");
$ixNet->execute('startAllProtocols');
print("Running the protocol for 30 seconds ..\n");
sleep(30);

###############################################################################
#Retrieve protocol statistics.
###############################################################################

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
print("PPPox Client  per port Stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"PPPoX Client Per Port"/page';
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


###############################################################################
#Stop protocol 
###############################################################################

print("\nStopping protocol\n");
$ixNet->execute('stopAllProtocols');

print("!!! Test Script Ends !!!");