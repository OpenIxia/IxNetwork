#!/usr/bin/perl
################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################
################################################################################
#                                                                              
# Description:                                                                 
#    This script intends to demonstrate how to use OVSDB Protocol API#
#    It will create following :
#1.    Add topology for ovsdb controller
#2.    Configure ipv4, ovsdb controller in TCP and cluster data.
#3.    Add device group for hypervisor and VM.
#4.    Associate connection between Hypervisor VxLAN and ovsdb controller.
#5.    Add Replicator as another device group, configure its ip address, BFD 
#      interface.
#6.    Associate replicator VXLAN and BFD interface to ovsdb controller.
#7.    Start each device group separately.
#8.    Wait for some time
#9.    Check Stats
#10.   Execute dump db
#11.   Stop each device group separately.
#
################################################################################
use IxNetwork

# Script Starts
print("!!! Test Script Starts !!!\n");

# Edit this variables values to match your setup
my $ixTclServer = '10.214.100.11';
my $ixTclPort   = '8348';
my @ports       = (('10.214.100.71', '8', '1'));
# Spawn a new instance of IxNetwork object. 
my $ixNet = new IxNetwork();

###############################################################################
# Connecting to IxTCl server and creating new config                          #
###############################################################################

print("Connect to IxNetwork Tcl server\n");
$ixNet->connect($ixTclServer, '-port', $ixTclPort, '-version', '8.40',
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


print("Adding  topologies\n");
$ixNet->add($ixNet->getRoot(), 'topology', '-vports', $vportTx);
$ixNet->commit();

my @topologies = $ixNet->getList($ixNet->getRoot(), 'topology');
my $topo1 = $topologies[0];

################################################################################
# Adding Controller Device Group                         #
###############################################################################
print("Adding Controller device groups\n");
$ixNet->add($topo1, 'deviceGroup');
$ixNet->commit();

my @t1devices = ($ixNet->getList($topo1, 'deviceGroup'));
my $t1devices = ($ixNet->getList($topo1, 'deviceGroup'));
my $ovsdb_controller = $t1devices[0];

print("Configuring the multipliers (number of sessions)\n");
$ixNet->setAttribute($ovsdb_controller, 
                    '-multiplier', '1',
                    '-name', 'OVSDB Controller');
$ixNet->commit();
################################################################################
# Adding Hypervisor Device Group                         #
###############################################################################
print("Adding Hypervisor device groups\n");
$ixNet->add($topo1, 'deviceGroup');
$ixNet->commit();

my @t1devices = ($ixNet->getList($topo1, 'deviceGroup'));
my $t1devices = ($ixNet->getList($topo1, 'deviceGroup'));
my $hypervisor_device_group = $t1devices[1];

print("Configuring the multipliers (number of sessions)\n");
$ixNet->setAttribute($hypervisor_device_group, 
                    '-multiplier', '1',
                    '-name', 'Hypervisor');
$ixNet->commit();

# print "Adding Hypervisor device group"
# set hypervisor_dg [ixNet add $topo1 deviceGroup]
# ixNet commit
# set dg_list [ixNet getList $topo1 deviceGroup]
# set hypervisor_device_group [lindex $dg_list 1]

# print "Configuring the multipliers (number of sessions)"
# ixNet setAttr $hypervisor_device_group -multiplier 1
# ixNet setAttr $hypervisor_device_group -name "Hypervisor"
# ixNet commit


################################################################################
# Adding VM Device Group behinf Hypervisor DG               #
###############################################################################

my $vm_dg  = $ixNet->add($hypervisor_device_group, 'deviceGroup');
$ixNet->setMultiAttribute($vm_dg,
    '-multiplier', '1',
    '-name', 'VM');
$ixNet->commit();

################################################################################
# Adding Replicator Device Group                     #
###############################################################################

print "Adding Replicator device group\n";
my $replicator_dg = $ixNet->add($topo1, 'deviceGroup');
$ixNet->commit();
my @dg_list = ($ixNet->getList($topo1, 'deviceGroup'));
my $dg_list = ($ixNet->getList($topo1, 'deviceGroup'));
my $replicator_device_group = $dg_list[2];
print "Configuring the multipliers (number of sessions)\n";
$ixNet->setMultiAttribute($replicator_device_group, '-multiplier', '5');
$ixNet->setMultiAttribute($replicator_device_group, '-name', 'Hypervisor');
$ixNet->commit();


################################################################################
# Configure  Controller and its cluster data                     #
###############################################################################
print("Add ethernet to controller \n");
my $controller_ethernet = $ixNet->add($ovsdb_controller, 'ethernet');
$ixNet->setMultiAttribute($controller_ethernet, 
    '-stackedLayers', [], 
    '-name', 'Ethernet 1');
$ixNet->commit();

print("Add ipv4\n");
my $controller_ipv4 = $ixNet->add($controller_ethernet, 'ipv4');;
$ixNet->setMultiAttribute($controller_ipv4, 
    '-stackedLayers', [], 
    '-name', 'IPv4 1');
$ixNet->commit();


my $ipv4_gateway = $ixNet->getAttribute($controller_ipv4, '-gatewayIp');
my $ipv4_gateway_value = $ixNet->add($ipv4_gateway, 'singleValue');;
$ixNet->setMultiAttribute($ipv4_gateway_value, 
    '-value', '70.101.1.101');
$ixNet->commit();    


my $ipv4_address = $ixNet->getAttribute($controller_ipv4, '-address');
$ixNet->commit();
my $ipv4_address_val = $ixNet->add($ipv4_address, 'singleValue');;
$ixNet->setMultiAttribute($ipv4_address_val, 
    '-value', '70.101.1.1');
$ixNet->commit();

my $ovsdb_controller = $ixNet->add($controller_ipv4, 'ovsdbcontroller');
$ixNet->setMultiAttribute($ovsdb_controller,
    '-name', 'OVSDB Controller 1');
$ixNet->commit();

print("Start configuring cluster data for ovsdb controller\n");

$ixNet->setMultiAttribute($ovsdb_controller.'/clusterData',
        '-bindingsCount', '10');
$ixNet->commit();

print("Set vlan value for cluster data from range 1000-1009\n");
my $ovsdb_vlan = $ixNet->getAttribute($ovsdb_controller.'/clusterData', '-vlan');
my $ovsdb_vlan_counter = $ixNet->add($ovsdb_vlan, 'counter');
$ixNet->setMultiAttribute($ovsdb_vlan_counter,
		'-step', '1', 
		'-start', '1000', 
		'-direction', 'increment');
$ixNet->commit();

print "Set Physical port name for cluster data to value ens256\n";
my $controller_physical_port = $ixNet->getAttribute($ovsdb_controller.'/clusterData', '-physicalPortName');
my $controller_physical_port_single_val = $ixNet->add($controller_physical_port, 'singleValue');
$ixNet->setMultiAttribute($controller_physical_port_single_val,
    '-value', 'ens256');
$ixNet->commit();

print "Set Physical switch name for cluster data to value br0\n";
my $controller_ps_name = $ixNet->getAttribute($ovsdb_controller.'/clusterData', '-physicalSwitchName');
my $controller_ps_name_single_val = $ixNet->add($controller_ps_name, 'singleValue');
$ixNet->setMultiAttribute($controller_ps_name_single_val,
    '-value', 'br0');
$ixNet->commit();

print "Set vni value for cluster data to 5000-5009\n";
my $ovsdb_controller_vni = $ixNet->getAttribute($ovsdb_controller.'/clusterData', '-vni');
my $ovsdb_controller_vni_counter = $ixNet->add($ovsdb_controller_vni, 'counter');
$ixNet->setMultiAttribute($ovsdb_controller_vni_counter,
		'-step', '1', 
		'-start', '5000', 
		'-direction', 'increment');
$ixNet->commit();

print "Set logical switch name for cluster data to value LS_5000 to LS_5009\n";
my $ovsdb_controller_ls_name = $ixNet->getAttribute($ovsdb_controller.'/clusterData', '-logicalSwitchName');
my $ovsdb_controller_ls_string = $ixNet->add($ovsdb_controller_ls_name, 'string');
$ixNet->setMultiAttribute($ovsdb_controller_ls_string,
   '-pattern', 'LS_{Inc:5000,1}');
$ixNet->commit();

print "Enabling attach at start and setting its value to True\n";
my $attach_at_start = $ixNet->getAttribute($ovsdb_controller.'/clusterData', '-attachAtStart');
my $attach_at_start_val = $ixNet->add($attach_at_start, 'singleValue');
$ixNet->setMultiAttribute($attach_at_start_val,
    '-value', 'true');
$ixNet->commit();

print "Set error log directory name to C:\\temp";
my $ovsdb_controller_error_log = $ixNet->getAttribute($ovsdb_controller, '-errorLogDirectoryName');
my $ovsdb_controller_error_log_val = $ixNet->add($ovsdb_controller_error_log, "singleValue");
$ixNet->setMultiAttribute($ovsdb_controller_error_log_val,
    '-value', 'C:\temp');
$ixNet->commit();

print "Enable clear dump db file\n";
my $ovsdb_controller_clear_dump_db_file = $ixNet->getAttribute($ovsdb_controller, '-clearDumpDbFiles');
my $ovsdb_controller_clear_dump_db_file_val = $ixNet->add($ovsdb_controller_clear_dump_db_file, 'singleValue');
$ixNet->setMultiAttribute($ovsdb_controller_clear_dump_db_file_val,
    '-value', 'true');
$ixNet->commit();

print "Set all OVSDB table names here\n";
my $ovsdb_controller_table_name = $ixNet->getAttribute($ovsdb_controller, '-tableNames');
my $ovsdb_controller_table_name_single_val = $ixNet->add($ovsdb_controller_table_name, 'singleValue');
$ixNet->setMultiAttribute($ovsdb_controller_table_name_single_val,
   '-value', 'all global manager physical_switch physical_port physical_locator physical_locator_set tunnel logical_switch ucast_mac_local ucast_mac_remote mcast_mac_local mcast_mac_remote');
$ixNet->commit();

print "Set Dumpo DB directory name to C:\temp";
my $ovsdb_controller_dump_db = $ixNet->getAttribute($ovsdb_controller, '-dumpdbDirectoryName');
my $ovsdb_controller_dump_db_val = $ixNet->add($ovsdb_controller_dump_db, 'singleValue');
$ixNet->setMultiAttribute($ovsdb_controller_dump_db_val,
    '-value', 'C:\temp');
$ixNet->commit();

print "Set file name directory here if connection type is TLS...\n";
my $ovsdb_controller_file_cacert = $ixNet->getAttribute($ovsdb_controller, '-fileCaCertificate');
my $ovsdb_controller_file_cacert_val = $ixNet->add($ovsdb_controller_file_cacert, 'string');
$ixNet->setMultiAttribute($ovsdb_controller_file_cacert_val,
    '-pattern', 'CA_Certificate.pem');
$ixNet->commit();

my $ovsdb_controller_verify_peer = $ixNet->getAttribute($ovsdb_controller, '-verifyPeerCertificate');
my $ovsdb_controller_verify_peer_val = $ixNet->add($ovsdb_controller_verify_peer, 'singleValue');
$ixNet->setMultiAttribute($ovsdb_controller_verify_peer_val,
   '-value', 'false');
$ixNet->commit();

my $ovsdb_controller_file_cert = $ixNet->getAttribute($ovsdb_controller, '-fileCertificate');
my $ovsdb_controller_file_cert_val = $ixNet->add($ovsdb_controller_file_cert, 'string');
$ixNet->setMultiAttribute($ovsdb_controller_file_cert_val,
    '-pattern', 'Certificate.pem');
$ixNet->commit();

my $ovsdb_controller_file_prv_key = $ixNet->getAttribute($ovsdb_controller, '-filePrivKey');
my $ovsdb_controller_file_prv_key_val = $ixNet->add($ovsdb_controller_file_prv_key, 'string');
$ixNet->setMultiAttribute($ovsdb_controller_file_prv_key_val,
    '-pattern', 'Private_Key.pem');
$ixNet->commit();

my $ovsdb_controller_dir_name = $ixNet->getAttribute($ovsdb_controller, '-directoryName');
my $ovsdb_controller_dir_name_val = $ixNet->add($ovsdb_controller_dir_name, 'string');
$ixNet->setMultiAttribute($ovsdb_controller_dir_name_val,
   '-pattern', 'C:\Program Files (x86)\Ixia\authfiles');
$ixNet->commit();

my $ovsdb_controller_tcp_port = $ixNet->getAttribute($ovsdb_controller, '-controllerTcpPort');
my $ovsdb_controller_tcp_port_val = $ixNet->add($ovsdb_controller_tcp_port, 'singleValue');
$ixNet->setMultiAttribute($ovsdb_controller_tcp_port_val,
    '-value', '6640');
$ixNet->commit();
print "Set TCP connection here.\n";
my $ovsdb_controller_conn_type = $ixNet->getAttribute($ovsdb_controller, '-connectionType');
my $ovsdb_controller_conn_type_val = $ixNet->add($ovsdb_controller_conn_type, 'singleValue');
$ixNet->setMultiAttribute($ovsdb_controller_conn_type_val,
    '-value', 'tcp');
$ixNet->commit();


################################################################################
# Configure  Hypervisor                    #
###############################################################################

print "Configure Hypervisor layer by layer\n";
my $ethernet_hypervisor = $ixNet->add($hypervisor_device_group, 'ethernet');
$ixNet->setMultiAttribute($ethernet_hypervisor,
    '-name', 'Ethernet 2');
$ixNet->commit();

my $ipv4_hypervisor = $ixNet->add($ethernet_hypervisor, 'ipv4');
$ixNet->setMultiAttribute($ipv4_hypervisor,
    '-name', 'IPv4 2');
$ixNet->commit();

my $gateway_ip_hypervisor = $ixNet->getAttribute($ipv4_hypervisor, '-gatewayIp');
my $gateway_ip_hypervisor_val = $ixNet-> add($gateway_ip_hypervisor, 'singleValue');
$ixNet->setMultiAttribute($gateway_ip_hypervisor_val,
    '-value', '50.101.1.101');
$ixNet->commit();

my $hypervisor_ipv4_address = $ixNet->getAttribute($ipv4_hypervisor, '-address');
my $hypervisor_ipv4_address_val = $ixNet->add($hypervisor_ipv4_address, "singleValue");
$ixNet->setMultiAttribute($hypervisor_ipv4_address_val,
    '-value', '50.101.1.11');
$ixNet->commit();
my $hypervisor = $ixNet->add($ipv4_hypervisor, 'vxlan');

print "Connecting link of hypervisor to ovsdb controllert via pseudoConnectedTo\n ";
$ixNet->setMultiAttribute($hypervisor,
		'-externalLearning', 'true', 
		'-runningMode', 'ovsdbStack', 
		'-ovsdbConnectorMultiplier', '10', 
		'-multiplier', '10', 
		'-stackedLayers', [], 
		'-name', 'VXLAN 1');
$ixNet->commit();
$ixNet->setMultiAttribute($ovsdb_controller,
    '-pseudoConnectedTo', $hypervisor); 
$ixNet->setMultiAttribute($ovsdb_controller,
    '-vxlan', $hypervisor); 
$ixNet->setMultiAttribute($ethernet_hypervisor.'/vlan:1',
    '-name', 'VLAN 2');
$ixNet->commit();    
print("Set hypervisor VNI to increment from 5000 to 5009\n");
print $hypervisor;
my $hypervisor_vni = $ixNet->getAttribute($hypervisor, '-vni');
print $hypervisor_vni; 
my $hypervisor_vni_val = $ixNet->add($hypervisor_vni, 'counter');
print $hypervisor_vni_val;
$ixNet->setMultiAttribute($hypervisor_vni_val,
     '-step', '1',
     '-start', '5000',
     '-direction', 'increment');
$ixNet->commit();

    
################################################################################
# Configure  VM                    #
###############################################################################    
print("configure VM\n");
print $vm_dg;
# print    
my $ethernet_vm = $ixNet->add($vm_dg, 'ethernet');
$ixNet->commit();
$ixNet->setMultiAttribute($ethernet_vm,
    '-name', 'Ethernet 3');
$ixNet->commit();

print "adding ipv4";
my $ipv4_vm = $ixNet->add($ethernet_vm, 'ipv4');
$ixNet->setMultiAttribute($ipv4_vm,
        '-name', 'IPv4 3');
$ixNet->commit();

my $gateway_ip_vm = $ixNet->getAttribute($ipv4_vm, '-gatewayIp');
my $gateway_ip_val = $ixNet->add($gateway_ip_vm, 'counter');
$ixNet->setMultiAttribute($gateway_ip_val,
		'-step', '0.0.1.0', 
		'-start', '100.1.0.1', 
		'-direction', 'increment');
$ixNet->commit();

my $ipv4_address_vm = $ixNet->getAttribute($ipv4_vm, '-address');
my $ipv4_address_val = $ixNet->add($ipv4_address_vm, 'counter');
$ixNet->setMultiAttribute($ipv4_address_val,
		'-step', '0.0.1.0', 
		'-start', '100.1.0.2', 
		'-direction', 'increment');
$ixNet->commit();        
print "Connecting link of VM to hypervisor via ConnectedTo\n ";        
my $vm_dg_connector = $ixNet-> add($ethernet_vm, 'connector');
$ixNet->setMultiAttribute($vm_dg_connector,
    '-connectedTo', $hypervisor);
$ixNet->commit();
   
################################################################################
# Configure  Replicator                #
###############################################################################  
my $ethernet_replicator = $ixNet->add($replicator_device_group, 'ethernet');
$ixNet->setMultiAttribute($ethernet_replicator,
    '-name', 'Ethernet 4');
$ixNet->commit();

my $ipv4_replicator = $ixNet->add($ethernet_replicator, 'ipv4');
$ixNet->setMultiAttribute($ipv4_replicator,
    '-name', 'IPv4 4');
$ixNet->commit();

my $gateway_ip_replicator = $ixNet->getAttribute($ipv4_replicator, '-gatewayIp');
my $gateway_ip_hypervisor_val = $ixNet->add($gateway_ip_replicator, 'singleValue');
$ixNet-> setMultiAttribute($gateway_ip_hypervisor_val,
    '-value', '50.101.1.101');
$ixNet->commit();

my $replicator_ipv4_address = $ixNet->getAttribute($ipv4_replicator, '-address');
my $replicator_ipv4_address_val = $ixNet->add($replicator_ipv4_address, 'singleValue');
$ixNet->setMultiAttribute($replicator_ipv4_address_val,
    '-value', '50.101.1.1');
$ixNet->commit();
my $replicator_vxlan = $ixNet->add($ipv4_replicator, 'vxlan');
$ixNet->setMultiAttribute($replicator_vxlan,
		'-externalLearning', 'true', 
		'-runningMode', 'ovsdbControllerBfdStack', 
		'-ovsdbConnectorMultiplier', '55', 
		'-multiplier', '11', 
		'-stackedLayers', [], 
		'-name', 'VXLAN 2');
$ixNet->commit();

my $replicator_vxlan_vni = $ixNet->getAttribute($replicator_vxlan, '-vni');
print "Set hypervisor VNI to increment from 0 to 5009\n";
my $replicator_vxlan_vni_custom = $ixNet->add($replicator_vxlan_vni, 'custom');
$ixNet->setMultiAttribute($replicator_vxlan_vni_custom,
    '-step', '0',
    '-start', '0');
$ixNet->commit();

my $replicator_vxlan_vni_incr = $ixNet->add($replicator_vxlan_vni_custom, 'increment');
$ixNet->setMultiAttribute($replicator_vxlan_vni_incr,
    '-count', '2',
    '-value', '5000');
$ixNet->commit();

my $replicator_vxlan_vni_val = $ixNet->add($replicator_vxlan_vni_custom, 'increment');
$ixNet->setMultiAttribute($replicator_vxlan_vni_val,
    '-count', '9',
    '-value', '1');
$ixNet->commit();        

print "Set connector from controller to replicator\n";  
$ixNet->setMultiAttribute($ovsdb_controller,
    '-pseudoConnectedToVxlanReplicator', $replicator_vxlan);
$ixNet->setMultiAttribute($ovsdb_controller,
    '-vxlanReplicator', $replicator_vxlan);
$ixNet->commit();        
print "setting BFD interface";
my $replicator_bfd = $ixNet->add($replicator_vxlan, 'bfdv4Interface');
$ixNet->setMultiAttribute($replicator_bfd,
		'-noOfSessions', '1', 
		'-stackedLayers', [], 
		'-name', 'BFDv4 IF 1');
$ixNet->commit();
$ixNet->setMultiAttribute($replicator_bfd.'/bfdv4Session',
    '-name', 'BFDv4 Session 1');

$ixNet->commit();

$ixNet->setMultiAttribute($ovsdb_controller,
    '-pseudoConnectedToBfd', $replicator_bfd);
$ixNet->setMultiAttribute($ethernet_replicator.'/vlan:1',
    '-name', 'VLAN 4');
$ixNet->commit();

print "Setting BFD interface parameters here\n";
my $bfd_active_multiVal = $ixNet->getAttribute($replicator_bfd, '-active');
my $bfd_active_value = $ixNet->add($bfd_active_multiVal, 'alternate');
$ixNet->setMultiAttribute($bfd_active_value, '-value', 'true');
$ixNet->commit();

print "Enabling one BFD Session\n";
my $bfd_session = $ixNet->getAttribute($replicator_bfd.'/bfdv4Session', '-active');
my $bfd_Session_value = $ixNet-> add($bfd_session, 'alternate');
$ixNet->setMultiAttribute($bfd_Session_value, '-value', 'true');
$ixNet->commit();
print "Setting BFD discriminator value to 1\n";
my $bfd_discriminator = $ixNet->getAttribute($replicator_bfd.'/bfdv4Session', '-myDiscriminator');
$ixNet->setMultiAttribute($bfd_discriminator, '-clearOverlays', 'false');
$ixNet->commit();
my $bfd_discriminator_value = $ixNet->add($bfd_discriminator, 'singleValue');
$ixNet->setMultiAttribute($bfd_discriminator_value, '-value', '1');
$ixNet->commit();

################################################################################
# Starting Protocols DG one by one as start all is not supported                                                     #
############################################################################### 
#$ixNet->execute(startAllProtocols);
#sleep(45);
print "Starting Replicator DG\n";
$ixNet->execute('start', $replicator_device_group);
# $ixNet-> exec start $replicator_device_group
sleep(10);

print "Starting VM DG\n";
$ixNet->execute('start', $vm_dg);
# $ixNet-> exec start $vm_dg
sleep(10); 

print "Starting Controller DG\n";
$ixNet->execute('start', $ovsdb_controller);
#$ixNet-> exec start $controller_device_group1
sleep(30); 

################################################################################
# Check Stats                                                  #
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

print("Verifying OpenFlow Controller Per Port stats\n");
my $viewPage = '::ixNet::OBJ-/statistics/view:"OVSDB Controller Per Port"/page';
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
# Execute dump db                                                 #
############################################################################### 
print "Execute Dump DB\n";
# $ixNet-> exec dumpDB $ovsdb_controller 1
$ixNet->execute('dumpDB', $ovsdb_controller, '1');

################################################################################
# Stopping Protocols DG one by one as start all is not supported                                                     #
############################################################################### 
print "Stopping Replicator DG\n";
$ixNet->execute('stop', $replicator_device_group);
# $ixNet-> exec stop $replicator_device_group
sleep(10); 

print "Stopping Hypervisor DG\n";
$ixNet->execute('stop', $hypervisor_device_group);
# $ixNet-> exec stop $hypervisor_device_group
sleep(10); 

print "Stopping Controller DG\n";
$ixNet->execute('stop', $ovsdb_controller);
# $ixNet-> exec stop $controller_device_group1
sleep(10); 

print "************TEST CASE ENDS HERE*********************"





