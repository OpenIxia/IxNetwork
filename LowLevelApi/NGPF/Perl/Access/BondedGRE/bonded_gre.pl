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



# ##############################################################################
# Description:                                                                 #
# This script will demonstrate Bonded GRE as per RFC 8157                      #
#     Script  will do following:                                               #
#    1. Load the config bonded_gre_sample_script.ixncfg                        #
#        Config has following:                                                 #
#        a. Config having HAAP side simulation pre configured                  #
#        b. Client side Bonded GRE will be configured in this sample           #
#    2.  Create Bonded GRE topology                                            #
#    3.  Create Link TLV {[77] Link Type]}                                     #
#        and custom TLV {[xx] Bonded GRE Custom TLV}                           #
#        These TLV 's are not mandatory to create                              #
#    4.  Start Protocol in following order as start all protocol not supported #
#        a. Start LTE Bonded GRE device group                                  #
#        b. Start DSL Bonded GRE device group                                  #
#        c. Start HAAP GRE   												   #
#		 d. Simulate control traffic after starting device group mentioned in  #
#			steps from (a to c) for LTE and DSL setup Accept message so that   #
#			Bonded GRE to come up.                                             #
#        d. Start HAAP DHCP server                                             #
#        e. Start Home Gateway dhcp client                                     #
#    5. Create data traffic between HomeGateway DHCP Client to DHCP IPv4 Server#
#    6. Send Active Hello Notify packet from HAAP to Home Gateway.             #
#    7. Send right click actions like stop hello, resume hello, overflowLte    #
#    8. Check following session info state:                                    #
#       a. Bonded Gateway Session Info                                         #
#       b. Home Gateway Session Info 										   #
#	 9. Send LTE tear down control traffic from HAAP to HG  	               #
#    10. Stop and start Bonded GRE LTE after tear down                         #
#    11. Send Tear Down from Home Gateway to HAAP with error code 11           #
#    12. Check     Stats                                                       #
#    13. Stop Protocols                                                        #
#    14.Disable Tlv                                                            #
# Module:                                                                      #
#    The sample was tested on a 10GE LSM  module.                              #
#                                                                              #
# ##############################################################################




################################################################################
# Please ensure that PERL5LIB environment variable is set properly so that 
# IxNetwork.pm module is available. IxNetwork.pm is generally available in
# C:\<IxNetwork Install Path>\API\Perl
################################################################################
use IxNetwork;
use strict;

#####################################################################################
# Procedure : traffitem_enable_regenerate
# Purpose   : Enable the Traffic Item based on name and Regenerate traffic for that
# Parameters: ixNet, tItemName
#             ixNet - ixNetwork Instance
#             tItemName - Expected traffic Item Name which needs to be enabled and regenerated
# Return    :  flag
# error: -1
# ###################################################################################

sub traffitem_enable_regenerate {
my @my_resource = @_;
my $ixNet    = $my_resource[0];
my $tItemName = $my_resource[1];

my @traffic_items = $ixNet->getList(($ixNet->getRoot()).'/traffic', 'trafficItem');
my $flag = 1;
foreach my $item (@traffic_items) {
    my $name = $ixNet->getAttribute($item, '-name');
    if ($name eq $tItemName) {
        $ixNet->setMultiAttribute($item, '-enabled', 'True');
        $ixNet->commit();
        $ixNet->execute('generate', $item);
        my $flag = 0;
    }
    }
return $flag;
}


###############################################################################
# Procedure : traffitem_disable
# Purpose   : Disable the Traffic Item based on name
# Parameters: ixNet, tItemName
#             ixNet - ixNetwork Instance
#             tItemName - Expected traffic Item Name which needs to be Disabled
# Return    :  flag
# error: -1
# ##############################################################################
sub traffitem_disable {
my @my_resource = @_;
my $ixNet    = $my_resource[0];
my $tItemName = $my_resource[1];

my @traffic_items = $ixNet->getList(($ixNet->getRoot()).'/traffic', 'trafficItem');
my $flag = 1;
foreach my $item (@traffic_items) {
    my $name = $ixNet->getAttribute($item, '-name');
    if ($name eq $tItemName) {
        $ixNet->setMultiAttribute($item, '-enabled', 'False');
        $ixNet->commit();
        my $flag = 0;
    }
    }
return $flag;
}


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
#my @ports       = (('10.39.64.117', '2', '9'), ('10.39.64.117', '2', '10'));
my @ports       = (('10.39.64.117', '2', '5'), ('10.39.64.117', '2', '6'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '7.40',
    '-setAttribute', 'strict');
 

print("Creating a new config\n");
$ixNet->execute('newConfig');

print("Loading sample configuration\n");
my $config_file = "bonded_gre_sample_script.ixncfg";
$ixNet->execute('loadConfig', $ixNet->readFrom($config_file));

print "Adding ports to configuration\n";
my $root = $ixNet->getRoot();
my @vPorts = $ixNet->getList($root, 'vport');
my $vport1 = @vPorts[0];
my $vport2 = @vPorts[1];

sleep(5);

print "########################################################################";
print "\n\nCreate  Home Gateway topology \n\n";
print "########################################################################";

print "\n\nAdding Home Gateway topology \n\n";
my $hg_topology = $ixNet->add($root, 'topology');
$ixNet->commit();
$ixNet->setAttribute($hg_topology, '-vports', $vport1);

print "Assigning ports\n";
my @vPorts  = $ixNet->getList($ixNet->getRoot(), 'vport');
my $vportTx = $vPorts[0];
my $vportRx = $vPorts[1];
assignPorts($ixNet, @ports, $vportTx, $vportRx);

print "\n.........Adding Bonded GRE LTE...............";
my $lte_device = $ixNet->add($hg_topology, 'deviceGroup');
$ixNet->commit();
$ixNet->setMultiAttribute($lte_device, 
    '-multiplier', '1', 
    '-name', 'LTE Device Group');
$ixNet->commit();


print "Add Ethernet to LTE ...";
my $ethernet1 = $ixNet->add($lte_device, 'ethernet');
$ixNet->commit();

print "\nAdd ipv4 to LTE device\n";
my $ip1 = $ixNet->add($ethernet1, 'ipv4');
$ixNet->commit();

print "\nconfiguring ipv4 addresses for LTE device ...";
$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-address').'/counter', '-start', '1.1.1.1', '-step', '0.0.0.1');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip1, '-gatewayIp').'/counter', '-start', '1.1.1.101', '-step', '0.0.0.1');
$ixNet->commit();

print "\nAdd GREoIPV4 in LTE device ...";
my $greoipv4 = $ixNet->add($ip1, 'greoipv4');
$ixNet->setMultiAttribute($greoipv4, '-name', 'GREoIPv4 2');
$ixNet->commit();

print "\nAdd DHCPv4 Client ...";
my $dhcpv4client = $ixNet->add($greoipv4, 'dhcpv4client');
$ixNet->setMultiAttribute($dhcpv4client, '-name', 'DHCPv4 Client 1');
$ixNet->commit();

print "\nAdd Bonded GRE in  LTE device ...";
my $dhcpv4client_bgre = $ixNet->getList($greoipv4, 'dhcpv4client');
my $bonded_gre_lte = $ixNet->add($greoipv4, 'bondedGRE');
$ixNet->setMultiAttribute($bonded_gre_lte, '-name', 'LTE Bonded GRE');
$ixNet->commit();

# Adding Bonded GRE DSL
print "\n.........Adding Bonded GRE DSL ...............";

my $dsl_device = $ixNet->add($hg_topology, 'deviceGroup');
$ixNet->commit();
$ixNet->setMultiAttribute($dsl_device, 
    '-multiplier', '1', 
    '-name', 'DSL Device Group');
$ixNet->commit();

print "\nAdd Ethernet to DSL device group...";
my $ethernet1 = $ixNet->add($dsl_device, 'ethernet');
$ixNet->commit();

print "\nAdd ipv4 to DSL device group ...";
my $ip2 = $ixNet->add($ethernet1, 'ipv4');
$ixNet->commit();

print "\n Configuring ipv4 addresses for  DSL device group ...";
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-address').'/counter', '-start', '1.1.1.2', '-step', '0.0.0.1');
$ixNet->setMultiAttribute($ixNet->getAttribute($ip2, '-gatewayIp').'/counter', '-start', '1.1.1.101', '-step', '0.0.0.1');
$ixNet->commit();

print "\nAdd GREoIPV4 in DSL device group...";
my $greoipv4_dsl = $ixNet->add($ip2, 'greoipv4');
$ixNet->setMultiAttribute($greoipv4_dsl, '-name', 'GREoIPv4 2');
$ixNet->commit();

print "\n Add BOnded GRE in DSL device group...";
my $bonded_gre_dsl = $ixNet->add($greoipv4_dsl, 'bondedGRE');
$ixNet->setMultiAttribute($bonded_gre_dsl, '-name', 'DSL Bonded GRE');
$ixNet->commit();

print "\n Modify tunnel type of DSL device group to DSL value";

$ixNet->setMultiAttribute($bonded_gre_dsl, 
'-tunnelType', 'dsl', 
'-stackedLayers', [], 
'-name', 'DSL Bonded GRE');

# Fetching HAAP device group details
my @top = $ixNet->getList($root, 'topology');
my $haap_topo = @top[0];
my @dg2 = $ixNet->getList($haap_topo, 'deviceGroup');
print "\n Check Device group list : @dg2 \n ";
my $deviceGroup_haap = @dg2[0];
my @mac = $ixNet->getList($deviceGroup_haap, 'ethernet');
my $ethernet_haap = @mac[0];
my @ipv4 = $ixNet->getList($ethernet_haap, 'ipv4');
my $ipv4_haap = @ipv4[0];
my @gre = $ixNet->getList($ipv4_haap, 'greoipv4');
my $greoipv4_haap = @gre[0];
my @ipdhcp = $ixNet->getList($greoipv4_haap, 'ipv4');
my $dhcpip = @ipdhcp[0];
my @dhcp = $ixNet->getList($dhcpip, 'dhcpv4server');
my $dhcpv4server = @dhcp[0];

print "\n Bonded GRE LTE handle is : $bonded_gre_lte \n";
print "\n  Bonded GRE DSL handle is : $bonded_gre_dsl \n";
print "\n GRE Home gateway handle is: $greoipv4 \n";
print "\n GRE HAAP handle is: $greoipv4_haap \n";
print "\n HomeGateway DHCP client handle  is: $dhcpv4client \n";
print "\n HAAP DHCP server handle  is : $dhcpv4server \n";
print "\n HAAP DHCPv4 Server IP handle is: $dhcpip \n";


print "\n Get Global templates ...";
my @global = $ixNet->getList($root, 'globals');
my $global_config = @global[0];
my @global_topology = $ixNet->getList($global_config, 'topology');
my $global_top = @global_topology[0];
my @glob_bgre = $ixNet->getList($global_top, 'bondedGRE');
my $global_bgre = @glob_bgre[0];
my @glob_tlv = $ixNet->getList($global_bgre, 'tlvEditor');
my $global_tlv_editor = @glob_tlv[0];
my @global_default_tlv = $ixNet->getList($global_tlv_editor, 'defaults');
my $global_tlv_default = @global_default_tlv[0];
my @glob_temp = $ixNet->getList($global_tlv_default, 'template');
my $global_template = @glob_temp[0];

print "\n Global templates : $global_template...";

print "########################################################################";
print "\n\n Add Link and custom TLV in LTE \n\n";
print "########################################################################";

print "\n 1. Creating Link TLV";

my $link_value = '[77] Link Type';
my @tlv_profile_1 = $ixNet->getList($bonded_gre_lte, 'tlvProfile');
my $tlv_profile = @tlv_profile_1[0];

#Get Link Type TLV from many default templates
my @tlv_list_1 = $ixNet->getFilteredList($global_template, 'tlv', '-name', $link_value);
my $tlv_list = @tlv_list_1[0];
$ixNet->commit();

#Copy Link Type TLV template to tlv profile
my $link_type_tlv = $ixNet->execute('copyTlv', $tlv_profile, $tlv_list);
$ixNet->commit();

print "\n Creating custom TLV with Type , Length and Value";
my $custom_tlv = '[xx] Bonded GRE Custom TLV';
#Get Custom Type TLV from many default templates
my @tlv_list_2 = $ixNet->getFilteredList($global_template, 'tlv', '-name', $custom_tlv);
my $tlv_list_custom = @tlv_list_2[0];
$ixNet->commit();
#Copy Custom Type TLV template to tlv profile
my $custom_type_tlv = $ixNet->execute('copyTlv', $tlv_profile, $tlv_list_custom);
$ixNet->commit();

#Get Custom type field value
my @tlv_val_1 = $ixNet->getList($custom_type_tlv, 'type');
my $tlv_val = @tlv_val_1[0];

my @tlv_obj_val1 = $ixNet->getList($tlv_val, 'object');
my $tlv_obj_val = @tlv_obj_val1[0];

my @obj_field_val_1 = $ixNet->getList($tlv_obj_val, 'field');
my $obj_field_val = @obj_field_val_1[0];

print "\n Change the Type Value for $custom_tlv to value aabbccdd";
#Modify field value for sub-tlv
my $obj_value = $ixNet->getAttribute($obj_field_val, '-value');
my $obj_counter = $ixNet->add($obj_value, 'counter');
$ixNet->setMultiAttribute($obj_counter, '-start', '12', '-step', '1');
$ixNet->commit();

print "\n Change the Value for $custom_tlv to value aabbccdd";
#Get Custom value
my @tlv_val_2 = $ixNet->getList($custom_type_tlv, 'value');
my $tlv_val = @tlv_val_2[0];
#Get Custom value object
my @tlv_obj_val2 = $ixNet->getList($tlv_val, 'object');
my $tlv_obj_val = @tlv_obj_val2[0];

#Get Custom value field
my @obj_field_val_2 = $ixNet->getList($tlv_obj_val, 'field');
my $obj_field_val = @obj_field_val_2[0];

#Modify field value for custom-tlv value
my $obj_value = $ixNet->getAttribute($obj_field_val, '-value');
my $obj_counter = $ixNet->add($obj_value, 'counter');
$ixNet->setMultiAttribute($obj_counter, '-start', 'aabbccdd', '-step', '1');
$ixNet->commit();

print("Starting Protocols \n");

print("1.  Starting LTE Bonded GRE protocols \n");
$ixNet->execute('start', $bonded_gre_lte);

print("2. Starting DSL Bonded GRE protocols \n");
$ixNet->execute('start', $bonded_gre_dsl);

print("3. Starting HAAP GRE \n");
$ixNet->execute('start', $greoipv4_haap);

print("Running the protocol for 30 seconds ..\n");
sleep(30);

print("\n Making LTE tunnel up by sending traffic for LTE setup accept message \n");

my $lte_setup_accept = "LTE setup Accept - All attributes";
traffitem_enable_regenerate($ixNet, $lte_setup_accept);
print("Applying and running traffic for LTE \n");
my @traffic1 = $ixNet->getList($root, 'traffic');
print("Apply traffic...'\n");
my $traffic = @traffic1[0];
$ixNet->execute('apply', $traffic);
print("Starting traffic...'\n");
$ixNet->execute('start', $traffic);
sleep(5);

print("Disable LTE setup accept traffic items\n");
traffitem_disable($ixNet, $lte_setup_accept);

my $dsl_setup_accept = "DSL Setup Accept - All attributes";
traffitem_enable_regenerate($ixNet, $dsl_setup_accept);
print("Applying and running traffic for DSL setup Accept message..\n");
my @traffic1 = $ixNet->getList($root, 'traffic');
print("Apply traffic...'\n");
my $traffic = @traffic1[0];
$ixNet->execute('apply', $traffic);
print("Starting traffic...'\n");
$ixNet->execute('start', $traffic);
sleep(5);

print("Disable DSL setup accept traffic items\n");
traffitem_disable($ixNet, $dsl_setup_accept);


print("Fetching all BondedGRE per port Stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"BondedGRE Per Port"/page';
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
sleep(1);


print("4. Starting Home Gateway dhcp Server\n");
$ixNet->execute('start', $dhcpv4server);

print("5. Starting Home Gateway dhcp client\n");
$ixNet->execute('start', $dhcpv4client);
sleep(5);

print("Creating Traffic from Home Gateway DHCP client to DHCP Server IPV4\n");
$ixNet->add(($ixNet->getRoot()).'/traffic', 'trafficItem');
$ixNet->commit();

my @ti1 = $ixNet->getList(($ixNet->getRoot()).'/traffic', 'trafficItem');

my $trafficItem1 = @ti1[4];

$ixNet->setMultiAttribute($trafficItem1, '-name', 'LTE-DHCP-HG-HAAP',
    '-trafficType', 'ipv4');
$ixNet->commit();

my $endpointSet1 = $ixNet->add($trafficItem1, 'endpointSet');

$ixNet->setMultiAttribute($endpointSet1,
    '-name',                  'EndpointSet-1',
    '-multicastDestinations', [[]],
    '-scalableSources',       [],
    '-multicastReceivers',    [[]],
    '-scalableDestinations',  [],
    '-ngpfFilters',           [],
    '-trafficGroups',         [],
    '-sources',               $dhcpv4client,
    '-destinations',          $dhcpip);
$ixNet->commit();

$ixNet->setMultiAttribute($trafficItem1.'/tracking', 
'-trackBy', ['ethernetIiSourceaddress0','trackingenabled0','ipv4DestIp0',
             'ipv4SourceIp0','ethernetIiDestinationaddress0'], 
'-values', [], 
'-fieldWidth', 'thirtyTwoBits', 
'-protocolOffset', 'Root.0');
$ixNet->commit();

print("Apply traffic...'\n");
my $traffic = @traffic1[0];
$ixNet->execute('apply', $traffic);

print("Starting traffic...'\n");
$ixNet->execute('start', $traffic);
sleep(5);

print("Fetching Flow Statistics Stats\n");
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
sleep(1);

print("Stop traffic...'\n");
$ixNet->execute('stop', $traffic);
sleep(2);

my $lte_traffic_home_gateway_haap = "LTE-DHCP-HG-HAAP";
traffitem_disable($ixNet, $lte_traffic_home_gateway_haap);

print("\n Applying and running traffic for active hello state \n");

my $lte_active_hello = "LTE - Notify-active_hello";
traffitem_enable_regenerate($ixNet, $lte_active_hello);
print("Applying and running traffic for active hello \n");
my @traffic1 = $ixNet->getList($root, 'traffic');
print("Apply traffic...'\n");
my $traffic = @traffic1[0];
$ixNet->execute('apply', $traffic);
print("Starting traffic...'\n");
$ixNet->execute('start', $traffic);
sleep(5);

print("Disable LTE setup accept traffic items\n");
traffitem_disable($ixNet, $lte_active_hello);


print "########################################################################";
print "Send right click actions for Overflow lte, Stop Hello and resume hello";
print "########################################################################";
#Similar command can be used for all right click actions like:
#Diag:Bonding tunnel start, Diag:DSL tunnel start, Diag:LTE tunnel Start, Diag: End Diagnostics
#Switch To DSL tunnel, DSL link failure, LTE link failure
print("Sending Stop hello\n");
$ixNet->execute('stophello', $bonded_gre_lte, 1);
sleep(2);
my @stop_hello_info = $ixNet->getAttribute($bonded_gre_lte, '-bSessionInfo');

print "\n Bonded GRE info after stop hello is : @stop_hello_info \n";

print("Resume Stop hello\n");
$ixNet->execute('resumehello', $bonded_gre_lte, 1);
sleep(2);
my @resume_hello_info = $ixNet->getAttribute($bonded_gre_lte, '-bSessionInfo');

print "\n Bonded GRE info after resume hello is : @resume_hello_info \n";

print("Sending overflowLte\n");
$ixNet->execute('overflowLte', $bonded_gre_lte, 1);
sleep(5);
my @hgateway_info = $ixNet->getAttribute($bonded_gre_lte, '-bSessionInfo');

print "\n Home Gateway info after sending right click action for overflowLte is : @hgateway_info \n";

print "########################################################################";
print "\n Verify the behavior when tear down is received by Home Gateway from HAAP\n";
print "########################################################################";

print "\n Enabling traffic for  LTE tear down with error code 01 \n";
my $lte_teardown_error = "LTE-Teardowncode01";
traffitem_enable_regenerate($ixNet, $lte_teardown_error);
print("Apply traffic...'\n");
my $traffic = @traffic1[0];
$ixNet->execute('apply', $traffic);

print("Starting traffic...'\n");
$ixNet->execute('start', $traffic);
sleep(10);

# Get Bonded GRE session Info for tear down
my @bgre_session_info = $ixNet->getAttribute($bonded_gre_lte, '-bSessionInfo');
print "\n Bonded GRE session Info for tear down is : @bgre_session_info \n";

# Get Error Code for tear down
my @error_code = $ixNet->getAttribute($bonded_gre_lte, '-errorCode');
print "\n Error Code for tear down is : @error_code \n";
traffitem_disable($ixNet, $lte_teardown_error);

print "\n Stop LTE Bonded GRE protocols and start again \n";
$ixNet->execute('stop', $bonded_gre_lte);
sleep(2);
$ixNet->execute('start', $bonded_gre_lte);
sleep(2);

print("\n Making LTE tunnel up by sending traffic for LTE setup accept message \n");
my $lte_setup_accept = "LTE setup Accept - All attributes";
traffitem_enable_regenerate($ixNet, $lte_setup_accept);
print("Applying and running traffic for LTE \n");
my @traffic1 = $ixNet->getList($root, 'traffic');
print("Apply traffic...'\n");
my $traffic = @traffic1[0];
$ixNet->execute('apply', $traffic);
print("Starting traffic...'\n");
$ixNet->execute('start', $traffic);
sleep(5);

print "########################################################################";
print "Send LTE tear down traffic from Homegateway to HAAP";
print "########################################################################";
$ixNet->execute('teardown', $bonded_gre_lte, 11, 1);
sleep(2);
my @teardown_info = $ixNet->getAttribute($bonded_gre_lte, '-bSessionInfo');
print "\n Bonded GRE info after Tear down from Homegateway to HAAP is : @teardown_info \n";

# Get Error Code for tear down
my @error_code = $ixNet->getAttribute($bonded_gre_lte, '-errorCode');
print "\n Error Code for tear down by homegateway is : @error_code \n";

$ixNet->execute('stopAllProtocols');
time.sleep(10);

print "###############################";
print " \n Disable Link and custom TLV\n";
print "##############################";

# Get TLV profile list
my @tlv_profile_list1 = $ixNet->getList($bonded_gre_lte, 'tlvProfile');
print "\n tlv_profile_list1 is : @tlv_profile_list1 \n";
my $tlv_profile_list = @tlv_profile_list1[0];
print "\n tlv_profile_list is : $tlv_profile_list \n";
my @tlv = $ixNet->getList($tlv_profile_list, 'tlv');
print "\n tlv is : @tlv \n";
foreach my $tlv_l (@tlv) {
    $ixNet->setMultiAttribute($tlv_l, '-isEnabled', 'false');
    $ixNet->commit();
}

print "\n Disconnect IxNetwork";
$ixNet->disconnect();

print("!!! \n Test Script Ends !!!");