# coding=utf-8

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
################################################################################
namespace eval ::py {
    set ixTclServer 10.214.100.11
    set ixTclPort   8345
    set ports       {{10.214.100.71 8 1} { 10.214.100.71 7 1}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::py::ixTclServer -port $::py::ixTclPort -version 8.40\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# Connecting to IxTCl server and cretaing new config                           #
###############################################################################
puts "Adding 1 vports"
ixNet add [ixNet getRoot] vport
ixNet commit
set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]

puts "Assigning the ports"
::ixTclNet::AssignPorts $py::ports {} $vPorts force

puts "Adding topology"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet commit
set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
################################################################################
# Adding Controller Device Group                         #
###############################################################################
puts "Adding Controller device group"
set controller_dg [ixNet add $topo1 deviceGroup]
ixNet commit
set controller_device_group [ixNet getList $topo1 deviceGroup]
set controller_device_group1 [lindex $controller_device_group 0]

puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $controller_device_group1 -multiplier 1
ixNet setAttr $controller_device_group1 -name "controller"
ixNet commit

################################################################################
# Adding Hypervisor Device Group                         #
###############################################################################
puts "Adding Hypervisor device group"
set hypervisor_dg [ixNet add $topo1 deviceGroup]
ixNet commit
set dg_list [ixNet getList $topo1 deviceGroup]
set hypervisor_device_group [lindex $dg_list 1]

puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $hypervisor_device_group -multiplier 1
ixNet setAttr $hypervisor_device_group -name "Hypervisor"
ixNet commit


################################################################################
# Adding VM Device Group behinf Hypervisor DG               #
###############################################################################

set vm_dg [ixNet add $hypervisor_device_group "deviceGroup"]
ixNet setMultiAttribute $vm_dg \
    -multiplier 1 \
    -name VM
ixNet commit

################################################################################
# Adding Replicator Device Group                     #
###############################################################################

puts "Adding Replicator device group"
set replicator_dg [ixNet add $topo1 deviceGroup]
ixNet commit
set dg_list [ixNet getList $topo1 deviceGroup]
set replicator_device_group [lindex $dg_list 2]
puts "Configuring the multipliers (number of sessions)"
ixNet setAttr $replicator_device_group -multiplier 5
ixNet setAttr $replicator_device_group -name "Hypervisor"
ixNet commit


################################################################################
# Configure  Controller and its cluster data                     #
###############################################################################

puts "Configure Controller layer by layer"
set ethernet [ixNet add $controller_device_group1 "ethernet"]
ixNet setMultiAttribute $ethernet \
    -name "Ethernet"
ixNet commit

set ipv4 [ixNet add $ethernet "ipv4"]
ixNet setMultiAttribute $ipv4 \
    -name "IPv4"
ixNet commit

set gateway_ip [ixNet getAttribute $ipv4 -gatewayIp]
set gateway_ip_single_val [ixNet add $gateway_ip "singleValue"]
ixNet setMultiAttribute $gateway_ip_single_val \
    -value 70.101.1.101
ixNet commit

set ipv4_address [ixNet getAttribute $ipv4 -address]
set ipv4_address_val [ixNet add $ipv4_address "singleValue"]
ixNet setMultiAttribute $ipv4_address_val \
    -value 70.101.1.1
ixNet commit
set ovsdb_controller [ixNet add $ipv4 "ovsdbcontroller"]
ixNet setMultiAttribute $ovsdb_controller \
    -name "OVSDB\ Controller\ 1"
ixNet commit

puts "Start configuring cluster data for ovsdb controller"

ixNet setMultiAttribute $ovsdb_controller/clusterData \
        -bindingsCount 10 
ixNet commit

puts "Set vlan value for cluster data from range 1000-1009"
set ovsdb_vlan [ixNet getAttribute $ovsdb_controller/clusterData -vlan]
set ovsdb_vlan_counter [ixNet add $ovsdb_vlan "counter"]
ixNet setMultiAttribute $ovsdb_vlan_counter \
    -step 1 \
    -start 1000 \
    -direction increment
ixNet commit

puts "Set Physical port name for cluster data to value ens256"
set controller_physical_port [ixNet getAttribute $ovsdb_controller/clusterData -physicalPortName]
set controller_physical_port_single_val [ixNet add $controller_physical_port "singleValue"]
ixNet setMultiAttribute $controller_physical_port_single_val \
    -value ens256
ixNet commit

puts "Set Physical switch name for cluster data to value br0"
set controller_ps_name [ixNet getAttribute $ovsdb_controller/clusterData -physicalSwitchName]
set controller_ps_name_single_val [ixNet add $controller_ps_name "singleValue"]
ixNet setMultiAttribute $controller_ps_name_single_val \
    -value br0
ixNet commit

puts "Set vni value for cluster data to 5000-5009"
set ovsdb_controller_vni [ixNet getAttribute $ovsdb_controller/clusterData -vni]
set ovsdb_controller_vni_counter [ixNet add $ovsdb_controller_vni "counter"]
ixNet setMultiAttribute $ovsdb_controller_vni_counter \
    -step 1 \
    -start 5000 \
    -direction increment
ixNet commit

puts "Set logical switch name for cluster data to value LS_5000 to LS_5009"
set ovsdb_controller_ls_name [ixNet getAttribute $ovsdb_controller/clusterData -logicalSwitchName]
set ovsdb_controller_ls_string [ixNet add $ovsdb_controller_ls_name "string"]
ixNet setMultiAttribute $ovsdb_controller_ls_string \
    -pattern "LS_\{Inc:5000,1\}"
ixNet commit

puts "Enabling attach at start and setting its value to True"
set attach_at_start [ixNet getAttribute $ovsdb_controller/clusterData -attachAtStart]
set attach_at_start_val [ixNet add $attach_at_start "singleValue"]
ixNet setMultiAttribute $attach_at_start_val \
    -value true
ixNet commit

puts "Set error log directory name to C:\\temp"
set ovsdb_controller_error_log [ixNet getAttribute $ovsdb_controller -errorLogDirectoryName]
set ovsdb_controller_error_log_val [ixNet add $ovsdb_controller_error_log "singleValue"]
ixNet setMultiAttribute $ovsdb_controller_error_log_val \
    -value "C:\\temp"
ixNet commit

puts "Enable clear dump db file"
set ovsdb_controller_clear_dump_db_file [ixNet getAttribute $ovsdb_controller -clearDumpDbFiles]
set ovsdb_controller_clear_dump_db_file_val [ixNet add $ovsdb_controller_clear_dump_db_file "singleValue"]
ixNet setMultiAttribute $ovsdb_controller_clear_dump_db_file_val \
    -value true
ixNet commit

puts "Set all OVSDB table names here"
set ovsdb_controller_table_name [ixNet getAttribute $ovsdb_controller -tableNames]
set ovsdb_controller_table_name_single_val [ixNet add $ovsdb_controller_table_name "singleValue"]
ixNet setMultiAttribute $ovsdb_controller_table_name_single_val \
    -value "all\ global\ manager\ physical_switch\ physical_port\ physical_locator\ physical_locator_set\ tunnel\ logical_switch\ ucast_mac_local\ ucast_mac_remote\ mcast_mac_local\ mcast_mac_remote"
ixNet commit

puts "Set Dumpo DB directory name to C:\\temp"
set ovsdb_controller_dump_db [ixNet getAttribute $ovsdb_controller -dumpdbDirectoryName]
set ovsdb_controller_dump_db_val [ixNet add $ovsdb_controller_dump_db "singleValue"]
ixNet setMultiAttribute $ovsdb_controller_dump_db_val \
    -value "C:\\temp"
ixNet commit

puts "Set file name directory here if connection type is TLS..."
set ovsdb_controller_file_cacert [ixNet getAttribute $ovsdb_controller -fileCaCertificate]
set ovsdb_controller_file_cacert_val [ixNet add $ovsdb_controller_file_cacert "string"]
ixNet setMultiAttribute $ovsdb_controller_file_cacert_val \
    -pattern CA_Certificate.pem
ixNet commit

set ovsdb_controller_verify_peer [ixNet getAttribute $ovsdb_controller -verifyPeerCertificate]
set ovsdb_controller_verify_peer_val [ixNet add $ovsdb_controller_verify_peer "singleValue"]
ixNet setMultiAttribute $ovsdb_controller_verify_peer_val \
    -value false
ixNet commit

set ovsdb_controller_file_cert [ixNet getAttribute $ovsdb_controller -fileCertificate]
set ovsdb_controller_file_cert_val [ixNet add $ovsdb_controller_file_cert "string"]
ixNet setMultiAttribute $ovsdb_controller_file_cert_val \
    -pattern Certificate.pem
ixNet commit

set ovsdb_controller_file_prv_key [ixNet getAttribute $ovsdb_controller -filePrivKey]
set ovsdb_controller_file_prv_key_val [ixNet add $ovsdb_controller_file_prv_key "string"]
ixNet setMultiAttribute $ovsdb_controller_file_prv_key_val \
    -pattern Private_Key.pem
ixNet commit

set ovsdb_controller_dir_name [ixNet getAttribute $ovsdb_controller -directoryName]
set ovsdb_controller_dir_name_val [ixNet add $ovsdb_controller_dir_name "string"]
ixNet setMultiAttribute $ovsdb_controller_dir_name_val \
    -pattern "C:\\Program\ Files\ (x86)\\Ixia\\authfiles"
ixNet commit

set ovsdb_controller_tcp_port [ixNet getAttribute $ovsdb_controller -controllerTcpPort]
set ovsdb_controller_tcp_port_val [ixNet add $ovsdb_controller_tcp_port "singleValue"]
ixNet setMultiAttribute $ovsdb_controller_tcp_port_val \
    -value 6640
ixNet commit
puts "Set TCP connection here."
set ovsdb_controller_conn_type [ixNet getAttribute $ovsdb_controller -connectionType]
set ovsdb_controller_conn_type_val [ixNet add $ovsdb_controller_conn_type "singleValue"]
ixNet setMultiAttribute $ovsdb_controller_conn_type_val \
    -value tcp
ixNet commit


################################################################################
# Configure  Hypervisor                    #
###############################################################################

puts "Configure Hypervisor layer by layer"
set ethernet_hypervisor [ixNet add $hypervisor_device_group "ethernet"]
ixNet setMultiAttribute $ethernet_hypervisor \
    -name "Ethernet\ 2"
ixNet commit

set ipv4_hypervisor [ixNet add $ethernet_hypervisor "ipv4"]
ixNet setMultiAttribute $ipv4_hypervisor \
    -name "IPv4\ 2"
ixNet commit

set gateway_ip_hypervisor [ixNet getAttribute $ipv4_hypervisor -gatewayIp]
set gateway_ip_hypervisor_val [ixNet add $gateway_ip_hypervisor "singleValue"]
ixNet setMultiAttribute $gateway_ip_hypervisor_val \
    -value 50.101.1.101
ixNet commit

set hypervisor_ipv4_address [ixNet getAttribute $ipv4_hypervisor -address]
set hypervisor_ipv4_address_val [ixNet add $hypervisor_ipv4_address "singleValue"]
ixNet setMultiAttribute $hypervisor_ipv4_address_val \
    -value 50.101.1.11
ixNet commit
set hypervisor [ixNet add $ipv4_hypervisor "vxlan"]

puts "Connecting link of hypervisor to ovsdb controllert via pseudoConnectedTo "
ixNet setMultiAttribute $hypervisor \
        -externalLearning true \
        -runningMode ovsdbStack \
        -ovsdbConnectorMultiplier 10 \
        -multiplier 10 \
        -stackedLayers [list ] \
        -name "VXLAN\ 1"
ixNet commit
ixNet setMultiAttribute $ovsdb_controller \
    -pseudoConnectedTo $hypervisor
ixNet setMultiAttribute $ovsdb_controller \
    -vxlan $hypervisor
ixNet setMultiAttribute $hypervisor_device_group/vlan:1 \
    -name "VLAN\ 2"

puts "Set hypervisor VNI to increment from 5000 to 5009"
set hypervisor_vni [ixNet getAttribute $hypervisor -vni]
set hypervisor_vni_val [ixNet add $hypervisor_vni "counter"]
ixNet setMultiAttribute $hypervisor_vni_val \
    -step 1 \
    -start 5000 \
    -direction increment
ixNet commit

    
################################################################################
# Configure  VM                    #
###############################################################################    
    
set ethernet_vm [ixNet add $vm_dg "ethernet"]
ixNet setMultiAttribute $ethernet_vm \
    -name "Ethernet\ 3"
ixNet commit

set ipv4_vm [ixNet add $ethernet_vm "ipv4"]
ixNet setMultiAttribute $ipv4_vm \
    -name "IPv4\ 3"
ixNet commit

set gateway_ip_vm [ixNet getAttribute $ipv4_vm -gatewayIp]
set gateway_ip_val [ixNet add $gateway_ip_vm "counter"]
ixNet setMultiAttribute $gateway_ip_val \
        -step 0.0.1.0 \
        -start 100.1.0.1 \
        -direction increment
ixNet commit

set ipv4_address_vm [ixNet getAttribute $ipv4_vm -address]
set ipv4_address_val [ixNet add $ipv4_address_vm "counter"]
ixNet setMultiAttribute $ipv4_address_val \
        -step 0.0.1.0 \
        -start 100.1.0.2 \
        -direction increment
ixNet commit        
puts "Connecting link of VM to hypervisor via ConnectedTo "        
set vm_dg_connector [ixNet add $ethernet_vm "connector"]
ixNet setMultiAttribute $vm_dg_connector \
    -connectedTo $hypervisor
ixNet commit
   
################################################################################
# Configure  Replicator                #
###############################################################################  
set ethernet_replicator [ixNet add $replicator_device_group "ethernet"]
ixNet setMultiAttribute $ethernet_replicator \
    -name "Ethernet\ 4"
ixNet commit

set ipv4_replicator [ixNet add $ethernet_replicator "ipv4"]
ixNet setMultiAttribute $ipv4_replicator \
    -name "IPv4\ 4"
ixNet commit

set gateway_ip_replicator [ixNet getAttribute $ipv4_replicator -gatewayIp]
set gateway_ip_hypervisor_val [ixNet add $gateway_ip_replicator "singleValue"]
ixNet setMultiAttribute $gateway_ip_hypervisor_val \
    -value 50.101.1.101
ixNet commit

set replicator_ipv4_address [ixNet getAttribute $ipv4_replicator -address]
set replicator_ipv4_address_val [ixNet add $replicator_ipv4_address "singleValue"]
ixNet setMultiAttribute $replicator_ipv4_address_val \
    -value 50.101.1.1
ixNet commit
set replicator_vxlan [ixNet add $ipv4_replicator "vxlan"]
ixNet setMultiAttribute $replicator_vxlan \
        -externalLearning true \
        -runningMode ovsdbControllerBfdStack \
        -ovsdbConnectorMultiplier 55 \
        -multiplier 11 \
        -stackedLayers [list ] \
        -name "VXLAN\ 2"
ixNet commit

set replicator_vxlan_vni [ixNet getAttribute $replicator_vxlan -vni]
ixNet setMultiAttribute $replicator_vxlan_vni \
    -clearOverlays false
ixNet commit

puts "Set hypervisor VNI to increment from 0 to 5009"
set replicator_vxlan_vni_custom [ixNet add $replicator_vxlan_vni "custom"]
ixNet setMultiAttribute $replicator_vxlan_vni_custom \
    -step 0 \
    -start 0
ixNet commit

set replicator_vxlan_vni_incr [ixNet add $replicator_vxlan_vni_custom "increment"]
ixNet setMultiAttribute $replicator_vxlan_vni_incr \
    -count 2 \
    -value 5000
ixNet commit

set replicator_vxlan_vni_val [ixNet add $replicator_vxlan_vni_custom "increment"]
ixNet setMultiAttribute $replicator_vxlan_vni_val \
    -count 9 \
    -value 1
ixNet commit        

puts "Set connector from controller to replicator"  
ixNet setMultiAttribute $ovsdb_controller \
    -pseudoConnectedToVxlanReplicator $replicator_vxlan
ixNet setMultiAttribute $ovsdb_controller \
    -vxlanReplicator $replicator_vxlan
ixNet commit        

set replicator_bfd [ixNet add $replicator_vxlan "bfdv4Interface"]
ixNet setMultiAttribute $replicator_bfd \
    -noOfSessions 1 \
    -stackedLayers [list ] \
    -name "BFDv4\ IF\ 1"
ixNet commit
ixNet setMultiAttribute $replicator_bfd/bfdv4Session \
    -name "BFDv4\ Session\ 1"

ixNet commit
ixNet setMultiAttribute $ovsdb_controller \
    -pseudoConnectedToBfd $replicator_bfd
ixNet setMultiAttribute $replicator_device_group/vlan:1 \
    -name "VLAN\ 4"
ixNet commit

puts "Setting BFD interface parameters here"
set bfd_active_multiVal [ixNet getAttribute $replicator_bfd -active]
ixNet setMultiAttribute $bfd_active_multiVal -clearOverlays false
ixNet commit
set bfd_active_value [ixNet add $bfd_active_multiVal alternate]
ixNet setMultiAttribute $bfd_active_value -value true
ixNet commit

puts "Enabling one BFD Session"
set bfd_session [ixNet getAttribute $replicator_bfd/bfdv4Session -active]
ixNet setMultiAttribute $bfd_session -clearOverlay false
ixNet commit

set bfd_Session_value [ixNet add $bfd_session alternate]
ixNet setMultiAttribute $bfd_Session_value -value true
ixNet commit
puts "Seeting BFD discriminator value to 1"
set bfd_discriminator [ixNet getAttribute $replicator_bfd/bfdv4Session -myDiscriminator]
ixNet setMultiAttribute $bfd_discriminator -clearOverlays false
ixNet commit
set bfd_discriminator_value [ixNet add $bfd_discriminator singleValue]
ixNet setMultiAttribute $bfd_discriminator_value -value 1
ixNet commit

################################################################################
# Starting Protocols DG one by one as start all is not supported                                                     #
############################################################################### 
puts "Starting Replicator DG"
ixNet exec start $replicator_device_group
after 10000

puts "Starting VM DG"
ixNet exec start $vm_dg
after 10000

puts "Starting Controller DG"
ixNet exec start $controller_device_group1
after 30000

################################################################################
# Check Stats                                                  #
############################################################################### 

puts "Verifying all the stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Protocols Summary"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

puts "Verifying OVSDB Controller per port stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"OVSDB Controller Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

################################################################################
# Execute dump db                                                 #
############################################################################### 

ixNet exec dumpDB $ovsdb_controller 1

################################################################################
# Stopping Protocols DG one by one as start all is not supported                                                     #
############################################################################### 
puts "Stopping Replicator DG"
ixNet exec stop $replicator_device_group
after 10000

puts "Stopping Hypervisor DG"
ixNet exec stop $hypervisor_device_group
after 10000

puts "Stopping Controller DG"
ixNet exec stop $controller_device_group1
after 10000

puts "************TEST CASE ENDS HERE*********************"





