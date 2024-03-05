# coding=utf-8

################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################
################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use OVSDB Protocol API#
#    It will create following :
#1.    Add topology for ovsdb controller
#2.    Configure ipv4, ovsdb controller in TLS and cluster data.
#3.    Add device group for hypervisor and VM.
#4.    Associate connection between Hypervisor VxLAN and ovsdb controller.
#5.    Add Replicator as another device group, configure its ip address, BFD 
#      interface.
#6.    Associate replicator VXLAN and BFD interface to ovsdb controller.
#7.    Start each device group separately.
#8.    Wait for some time
#9.    Check Stats
#10.   Stop each device group separately.
#
################################################################################
import sys
import time

################################################################################
# Either feed the ixNetwork library path in the sys.path as below, or put the  #
# IxNetwork.py file somewhere else where we python can autoload it             #
# "IxNetwork.py" is available in <IxNetwork_installer_path>\API\Python         #
################################################################################
sys.path.append('C:\Program Files (x86)\Ixia\IxNetwork\8.10-EA\API\Python')
from src import IxNetwork

print("loaded successfully")


class ovsdb(object):
    ################################################################################
    # Connecting to IxTCl server and cretaing new config                           #
    ################################################################################
    
    #Procedure to connect to IxTclNetwork Server
    def __init__(self, ix_tcl_server, ix_tcl_port, ix_version="8.20"):
        ixNet = IxNetwork.IxNet()
        print("connecting to IxNetwork client")
        ixNet.connect(ix_tcl_server, '-port', ix_tcl_port, '-version', ix_version,
                      '-setAttribute', 'strict')

        # cleaning up the old configfile, and creating an empty config
        print("cleaning up the old configfile, and creating an empty config")
        ixNet.execute('newConfig')
        self.ixNet = ixNet
        self.root = ixNet.getRoot()
    
    # Procedure for assigning ports to ixNetTclServer    
    def assignPorts(self, realPort1):
        chassis1 = realPort1[0]
        card1 = realPort1[1]
        port1 = realPort1[2]
        root = self.ixNet.getRoot()
        vport1 = self.ixNet.add(root, 'vport')
        self.ixNet.commit()
        vport1 = self.ixNet.remapIds(vport1)[0]
        chassisObj1 = self.ixNet.add(root + '/availableHardware', 'chassis')
        self.ixNet.setAttribute(chassisObj1, '-hostname', chassis1)
        self.ixNet.commit()
        chassisObj1 = self.ixNet.remapIds(chassisObj1)[0]

        cardPortRef1 = chassisObj1 + '/card:%s/port:%s' % (card1, port1)
        self.ixNet.setMultiAttribute(vport1, '-connectedTo', cardPortRef1,
                                     '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 001')
        self.ixNet.commit()

    # Procedure to Disable resolve gateway if require
    def resolve_gateway_disable(self, value):
        resolve_gateway = self.ixNet.getAttribute(value, '-resolveGateway')
        self.ixNet.setMultiAttribute(resolve_gateway, '-clearOverlays', 'false')
        self.ixNet.commit()
        resolve_gateway_val = self.ixNet.add(resolve_gateway, 'singleValue')
        self.ixNet.setMultiAttribute(resolve_gateway_val, '-value', 'false')
        self.ixNet.commit()

    #Procedure to configure ip address and gateway ip for ovsdb controller and replicator
    def assign_ip(self, ovsdb_ip, ip_address, gateway):
        mvAdd1 = self.ixNet.getAttribute(ovsdb_ip, '-address')
        mvGw1 = self.ixNet.getAttribute(ovsdb_ip, '-gatewayIp')
        print("configuring ipv4 addresses")
        self.ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', ip_address)
        self.ixNet.commit()
        self.ixNet.setAttribute(mvGw1 + '/singleValue', '-value', gateway)
        self.ixNet.commit()
        self.ixNet.setAttribute(self.ixNet.getAttribute(ovsdb_ip, '-prefix') + '/singleValue', '-value', '24')
        self.ixNet.commit()
        self.ixNet.setMultiAttribute(self.ixNet.getAttribute(ovsdb_ip, '-resolveGateway') + '/singleValue', '-value', 'true')
        self.ixNet.commit()
        time.sleep(5)

    ################################################################################
    # Start protocol                                                               #
    ################################################################################
    def start_protocol(self, startDeviceGroup):
        print("Starting protocols and waiting for 45 seconds for protocols to come up")
        self.ixNet.execute("start", startDeviceGroup)
        time.sleep(20)
    
    #Procedure to stop protocol
    def stop_protocol(self, stopDeviceGroup):
        print("stopping protocols")
        self.ixNet.execute("stop", stopDeviceGroup)
        time.sleep(20)
    
    #Procedure to get vport list connected to IxTclNetwork

    def get_vport(self):
        root = self.ixNet.getRoot()
        return self.ixNet.getList(root, 'vport')[0]
    
    #Procedure to add and get topology list

    def add_and_get_topology(self, vportTx):
        print("adding topologies")
        root = self.ixNet.getRoot()
        self.ixNet.add(root, 'topology', '-vports', vportTx)
        self.ixNet.commit()
        topologies = self.ixNet.getList(self.ixNet.getRoot(), 'topology')
        return topologies[0]

    #procedure to add and get device groups if its OVSDB controller, Hypervisor, Replicator    
    def add_and_get_device_group(self, topology, device_index=0):
        print("Adding  device group  ovsdb controller")
        device_group_controller = self.ixNet.add(topology, 'deviceGroup')
        self.ixNet.commit()
        t1devices = self.ixNet.getList(topology, 'deviceGroup')
        return device_group_controller, t1devices[device_index]

    #Procedure to set multiplier for each OVSDB controller, Hypervisor, Replicator
    def set_multiplier(self, device_group_controller, name_attribute, val):
        print("Configuring the multipliers (number of sessions)")
        self.ixNet.setMultiAttribute(device_group_controller, '-multiplier', val, '-name', name_attribute)
        self.ixNet.commit()
    
    # Procedure to add and get ethernet    
    def add_and_get_ethernet(self, device, device_group):
        print("Adding ethernet/mac endpoints in ovsdb controller")
        self.ixNet.add(device, 'ethernet')
        self.ixNet.commit()
        return self.ixNet.getList(device_group, 'ethernet')[0]
    
    #Procedure to get and add ipv4
    def add_and_get_ipv4(self, ethernet):
        print("Adding ipv4")
        ipv4_controller = self.ixNet.add(ethernet, 'ipv4')
        self.ixNet.commit()
        return ipv4_controller, self.ixNet.getList(ethernet, 'ipv4')[0]
    
    # procedure to Call assign_ip function 
    def configure_ipv4_and_gateway_address(self, ovsdb_controller_ip, controller_ip_address, gateway_ip_address):
        print("Configuring Ipv4 and gateway address in OVSDB Controller!!")
        self.assign_ip(ovsdb_controller_ip, controller_ip_address, gateway_ip_address)

    # Procedure to add ovsdb controller    
    def add_ovsdb_controller(self, ovsdb_controller_ip):
        print("Adding  controller IP4 stacks")
        ovsdb_controller = self.ixNet.add(ovsdb_controller_ip, 'ovsdbcontroller')
        self.ixNet.commit()
        return ovsdb_controller

    #Procedure to add TLS connection and set its certificate files    
    def add_tls_and_certs(self, ovsdb_controller):
        print("Adding tls Connection and its related certificate files!!")
        connection_type = self.ixNet.getAttribute(ovsdb_controller, '-connectionType')
        self.ixNet.setMultiAttribute(connection_type,
                                      '-clearOverlays', 'false')
        self.ixNet.commit()

        connection_type_val = self.ixNet.add(connection_type, 'singleValue')
        self.ixNet.setMultiAttribute(connection_type_val,
                                      '-value', 'tls')
        self.ixNet.commit()

        controller_directory = self.ixNet.getAttribute(ovsdb_controller, '-directoryName')
        self.ixNet.setMultiAttribute(controller_directory,
                                      '-clearOverlays', 'false')
        self.ixNet.commit()

        controller_file_name = self.ixNet.add(controller_directory, 'singleValue')
        self.ixNet.setMultiAttribute(controller_file_name,
                                      '-value', 'C:\\cert_files_original')
        self.ixNet.commit()

        file_ca_cert = self.ixNet.getAttribute(ovsdb_controller, '-fileCaCertificate')
        self.ixNet.setMultiAttribute(file_ca_cert,
                                      '-clearOverlays', 'false')
        self.ixNet.commit()

        file_ca_cert_value = self.ixNet.add(file_ca_cert, 'singleValue')
        self.ixNet.setMultiAttribute(file_ca_cert_value,
                                      '-value', 'cacert.pem')
        self.ixNet.commit()

        file_private_key = self.ixNet.getAttribute(ovsdb_controller, '-filePrivKey')
        self.ixNet.setMultiAttribute(file_private_key,
                                      '-clearOverlays', 'false')
        self.ixNet.commit()

        file_private_key_val = self.ixNet.add(file_private_key, 'string')
        self.ixNet.setMultiAttribute(file_private_key_val,
                                      '-pattern', 'controller-key.pem')
        self.ixNet.commit()

        file_cert_key = self.ixNet.getAttribute(ovsdb_controller, '-fileCertificate')
        self.ixNet.setMultiAttribute(file_cert_key,
                                      '-clearOverlays', 'false')

        self.ixNet.commit()

        file_cert_key_value = self.ixNet.add(file_cert_key, 'string')
        self.ixNet.setMultiAttribute(file_cert_key_value,
                                      '-pattern', 'controller-cert.pem')
        self.ixNet.commit()
    
    
    # Procedure to get and set physical port name
    def get_and_set_physical_port_name(self, ovsdb_controller):
        print("Modifying Physical Port name !!!")
        physical_port_name = self.ixNet.getAttribute(ovsdb_controller + '/clusterData', '-physicalPortName')
        self.ixNet.setMultiAttribute(physical_port_name,
                                     '-clearOverlays', 'false')
        self.ixNet.commit()
        physical_port_name_values = self.ixNet.add(physical_port_name, 'singleValue')
        self.ixNet.setMultiAttribute(physical_port_name_values, '-value', 'ens256')
        self.ixNet.commit()
        physical_port_name_index2 = self.ixNet.add(physical_port_name, 'overlay')
        self.ixNet.setMultiAttribute(physical_port_name_index2,
                                      '-count', '1',
                                      '-index', '2',
                                      '-indexStep', '0',
                                      '-valueStep', 'ens256',
                                      '-value', 'ens256')
        self.ixNet.commit()

    # Procedure to get and set Physical switch name     
    def get_and_set_physical_switch_name(self, ovsdb_controller):
        print("Modifying Physical Switch name !!!")
        physical_switch_name = self.ixNet.getAttribute(ovsdb_controller + '/clusterData', '-physicalSwitchName')
        self.ixNet.setMultiAttribute(physical_switch_name,
                                     '-clearOverlays', 'false')
        self.ixNet.commit()
        physical_switch_name_values = self.ixNet.add(physical_switch_name, 'singleValue')
        self.ixNet.setMultiAttribute(physical_switch_name_values, '-value', 'br0')
        self.ixNet.commit()

    #Procedure to get and set logical switch name    
    def get_and_set_logical_switch_name(self, ovsdb_controller):
        print("Modifying Logical Switch name !!!")
        logical_switch_name = self.ixNet.getAttribute(ovsdb_controller + '/clusterData', '-logicalSwitchName')
        self.ixNet.setMultiAttribute(logical_switch_name,
                                     '-clearOverlays', 'false')
        self.ixNet.commit()
        logical_sw_name = self.ixNet.add(logical_switch_name, 'string')
        self.ixNet.setMultiAttribute(logical_sw_name,
                                      '-pattern', 'LS_{Inc:5000,1}')
        self.ixNet.commit()
    
    #Procedure to get and set ovsdb_vni
    def get_and_set_ovsdb_vni(self, ovsdb_controller):
        ovsdb_vni = self.ixNet.getAttribute(ovsdb_controller + '/clusterData', '-vni')
        self.ixNet.setMultiAttribute(ovsdb_vni,
                                      '-clearOverlays', 'false')
        self.ixNet.commit()
        ovsdb_vni_value = self.ixNet.add(ovsdb_vni, 'counter')
        self.ixNet.setMultiAttribute(ovsdb_vni_value,
                                      '-step', '1',
                                      '-start', '5000',
                                      '-direction', 'increment')
        self.ixNet.commit()

    def attach_at_start(self, ovsdb_controller):
        ovsdb_attach_at_start = self.ixNet.getAttribute(ovsdb_controller + '/clusterData', '-attachAtStart')
        self.ixNet.setMultiAttribute(ovsdb_attach_at_start, '-clearOverlays', 'false')
        self.ixNet.commit()
        attach_at_start_val = self.ixNet.add(ovsdb_attach_at_start, 'singleValue')
        self.ixNet.setMultiAttribute(attach_at_start_val, '-value', 'false')
        self.ixNet.commit()
    
    #Procedure to add and get hypervisor as device group
    def add_and_get_hypervisor_device_group(self, topology):
        print("Adding  device group 2  as Hypervisor")
        device_group_hypervisor = self.ixNet.add(topology, 'deviceGroup')
        self.ixNet.commit()
        t2devices = self.ixNet.getList(topology, 'deviceGroup')
        return device_group_hypervisor, t2devices[1]

    #Procedure to add and get VxLan    
    def add_and_get_vxlan(self, hypervisor_ip, ovsdb_controller):
        print("Adding VXLAN over IP4 stacks")
        vxlan_hypervisor = self.ixNet.add(hypervisor_ip, 'vxlan')
        self.ixNet.commit()

        print("Ädding connector for Ovsdb Controller to Hypervisor VxLAN")
        self.ixNet.setMultiAttribute(vxlan_hypervisor, '-externalLearning', 'true', \
        '-runningMode', 'ovsdbStack', '-ovsdbConnectorMultiplier', '10', '-multiplier', '10',  '-stackedLayers', [], '-name', 'VXLAN 1')
        self.ixNet.commit()

        print("Associating hypervisor with ovsdb controller")
        self.ixNet.setMultiAttribute(ovsdb_controller,
                                     '-vxlan', vxlan_hypervisor)
        self.ixNet.setMultiAttribute(ovsdb_controller,
                                 '-pseudoConnectedTo', vxlan_hypervisor)
        self.ixNet.commit()
        return vxlan_hypervisor

    # Procedure to attach bindings
    def attach_bindings_in_range(self, ovsdb_controller, startIndex, LastIndex):
        cluster_data = self.ixNet.getList(ovsdb_controller, 'clusterData')[0]
        self.cluster_data = cluster_data
        print ("attaching  %s index to %s  bindings " % (startIndex, LastIndex))
        index_list = []
        for x in range(startIndex, (LastIndex + 1)):
            index_list.append(x)
        print (index_list)
        self.ixNet.execute('attach', cluster_data, index_list)
        return

    # Procedure to find master controller for dump db execution
    def find_master_controllerIndex(self, ovsdb_controller):
        RoleList = self.ixNet.getAttribute(ovsdb_controller, '-role')
        try:
            # adding 1 to make it start with 1 instead of 0
            masterIndex = (RoleList.index('master') + 1)
        except ValueError:
            masterIndex = -1
        return masterIndex

    ################################################################################
    # protocol configuration section                                               #
    ################################################################################
    def main(self):
        self.assignPorts(ports[0])
        root = self.ixNet.getRoot()
        #vportTx = self.ixNet.getList(root, 'vport')[0]
        vportTx = self.get_vport()
        print ('''
    #---------------------------------------------------------------------------
    # Adding topology and adding device group (OVSDB Controller)
    #---------------------------------------------------------------------------
    ''')
        topo1 = self.add_and_get_topology(vportTx)
        device_group_controller, t1dev1 = self.add_and_get_device_group(topo1)
        print ('''
    #---------------------------------------------------------------------------
    # Configuring OVSDB Controller and its cluster data 
    #---------------------------------------------------------------------------
    ''')
        #self.set_multiplier(device_group_controller, 'OVSDB Controller')
        self.set_multiplier(device_group_controller, 'OVSDB Controller', 1)
        mac_controller = self.add_and_get_ethernet(t1dev1, t1dev1)
        ipv4_controller, ovsdb_controller_ip = self.add_and_get_ipv4(mac_controller)
        self.configure_ipv4_and_gateway_address(ovsdb_controller_ip, '70.101.1.1', '70.101.1.101')
        ovsdb_controller = self.add_ovsdb_controller(ovsdb_controller_ip)
        #self.add_tls_and_certs(ovsdb_controller)
        print("Set OVSDB connector to replicator , hypervisor vxlan and BFD interface")
        self.ixNet.setMultiAttribute(ovsdb_controller,
                                      '-vxlan', r'::ixNet::OBJ-null',
                                      '-vxlanReplicator', r'::ixNet::OBJ-null',
                                      '-pseudoConnectedTo', r'::ixNet::OBJ-null',
                                      '-pseudoConnectedToVxlanReplicator', r'::ixNet::OBJ-null',
                                      '-pseudoConnectedToBfd', r'::ixNet::OBJ-null',
                                      '-stackedLayers', [],
                                      '-name', 'OVSDB Controller 1')
        self.ixNet.commit()

        cluster_data = self.ixNet.getList(ovsdb_controller, 'clusterData')[0]
        print (self.ixNet.help(cluster_data))
        print("cluster_data")
        bindingCount = self.ixNet.getAttribute(cluster_data, '-bindingsCount')
        print("Change Binding Count to 2")
        self.ixNet.setMultiAttribute(ovsdb_controller + '/clusterData',
                                     '-bindingsCount', '10',
                                     '-name', 'Cluster Configuration 1')
        self.get_and_set_physical_port_name(ovsdb_controller)
        self.get_and_set_physical_switch_name(ovsdb_controller)
        self.get_and_set_logical_switch_name(ovsdb_controller)
        self.get_and_set_ovsdb_vni(ovsdb_controller)
        self.attach_at_start(ovsdb_controller)

        print ('''
    #---------------------------------------------------------------------------
    # Adding Hypervisor and VM's behind hypervisor
    #---------------------------------------------------------------------------
    ''')
        device_group_hypervisor, t2dev1 = self.add_and_get_hypervisor_device_group(topo1)
        self.set_multiplier(device_group_hypervisor, 'Hypervisor', 1)
        mac_hypervisor = self.add_and_get_ethernet(t2dev1, t2dev1)
        ipv4_hypervisor, ip2 = self.add_and_get_ipv4(mac_hypervisor)
        self.configure_ipv4_and_gateway_address(ip2, '50.101.1.11', '50.101.1.101')
        vxlan_hypervisor = self.add_and_get_vxlan(ip2, ovsdb_controller)
        device_group_vm, t3dev1 = self.add_and_get_device_group(t2dev1, 0)

        # self.set_multiplier(device_group_vm, 'VM')
        self.set_multiplier(device_group_vm, 'VM', 1)

        mac3 = self.add_and_get_ethernet(device_group_vm, device_group_vm)
        ipv4_vm, ipv4_list = self.add_and_get_ipv4(mac3)

        ethernt2_vxlan1_connector = self.ixNet.add(mac3, 'connector')
        self.ixNet.setMultiAttribute(ethernt2_vxlan1_connector,
                                      '-connectedTo', vxlan_hypervisor)
        self.ixNet.commit()
        print ('''
    #---------------------------------------------------------------------------
    # Adding Replicator and BFD interface inside replicator
    #---------------------------------------------------------------------------
    ''')
        print("Adding Replicator!!!")
        device_group_replicator, t4dev1 = self.add_and_get_device_group(topo1, 2)
        self.set_multiplier(device_group_replicator, 'Replicator', 1)
        mac_replicator = self.add_and_get_ethernet(t4dev1, device_group_replicator)
        print("Add ipv4 in replicator")
        ipv4_replicator, replicator_ip = self.add_and_get_ipv4(mac_replicator)
        self.configure_ipv4_and_gateway_address(replicator_ip, '50.101.1.1', '50.101.1.101')
        print("Associate VXLAN Replicator to ovsdb controller")
        vxlan_replicator = self.ixNet.add(ipv4_replicator, 'vxlan')
        self.ixNet.setMultiAttribute(vxlan_replicator,
                                      '-externalLearning', 'true',
                                      '-runningMode', 'ovsdbControllerBfdStack',
                                      '-ovsdbConnectorMultiplier', '55',
                                      '-multiplier', '11',
                                      '-stackedLayers', [],
                                      '-name', 'VXLAN 2')
        self.ixNet.commit()
        self.ixNet.setMultiAttribute(ovsdb_controller,
                                      '-pseudoConnectedToVxlanReplicator', vxlan_replicator)
        self.ixNet.setMultiAttribute(ovsdb_controller,
                                      '-vxlanReplicator', vxlan_replicator)
        self.ixNet.commit()
        print("Adding VNI in replicator vxlan")
        replicator_vxlan_vni = self.ixNet.getAttribute(vxlan_replicator, '-vni')
        self.ixNet.setMultiAttribute(replicator_vxlan_vni,
                                      '-clearOverlays', 'false')

        self.ixNet.commit()
        replicator_vxlan_vni_value = self.ixNet.add(replicator_vxlan_vni, 'custom')
        self.ixNet.setMultiAttribute(replicator_vxlan_vni_value,
                                      '-step', '0',
                                      '-start', '0')
        self.ixNet.commit()
        replicator_vni = self.ixNet.add(replicator_vxlan_vni_value, 'increment')
        self.ixNet.setMultiAttribute(replicator_vni,
                                      '-count', '2',
                                      '-value', '5000')
        self.ixNet.commit()
        replicator_vni_incr = self.ixNet.add(replicator_vxlan_vni_value, 'increment')
        self.ixNet.setMultiAttribute(replicator_vni_incr,
                                      '-count', '9',
                                      '-value', '1')
        self.ixNet.commit()
        self.ixNet.setMultiAttribute(replicator_vxlan_vni + '/nest:1',
                                      '-enabled', 'false',
                                      '-step', '1')

        print("Adding BFD interface over replicator vxlan")

        bfdv4_interface = self.ixNet.add(vxlan_replicator, 'bfdv4Interface')
        self.ixNet.setMultiAttribute(bfdv4_interface,
                                      '-noOfSessions', '1',
                                      '-stackedLayers', [],
                                      '-name', 'BFDv4 IF 1')
        self.ixNet.commit()
        print ('''
    #---------------------------------------------------------------------------
    #Associate BFD interface to ovsdb controller and configure BFD interface
    #---------------------------------------------------------------------------
    ''')
        self.ixNet.setMultiAttribute(ovsdb_controller,
                                      '-pseudoConnectedToBfd', bfdv4_interface)

        bfd_active_multiVal = self.ixNet.getAttribute(bfdv4_interface, '-active')
        self.ixNet.setMultiAttribute(bfd_active_multiVal, '-clearOverlays', 'false')
        self.ixNet.commit()
        bfd_active_value = self.ixNet.add(bfd_active_multiVal, 'alternate')
        self.ixNet.setMultiAttribute(bfd_active_value,
                                      '-value', 'true')
        self.ixNet.commit()

        print("Enabling one BFD Session")
        bfd_session = self.ixNet.getAttribute(bfdv4_interface + '/bfdv4Session', '-active')
        self.ixNet.setMultiAttribute(bfd_session,
                                      '-clearOverlays', 'false')

        self.ixNet.commit()
        bfd_Session_value = self.ixNet.add(bfd_session, 'alternate')
        self.ixNet.setMultiAttribute(bfd_Session_value,
                                      '-value', 'true')
        self.ixNet.commit()
        print("Seeting BFD discriminator value to 1")
        bfd_discriminator = self.ixNet.getAttribute(bfdv4_interface + '/bfdv4Session', '-myDiscriminator')
        self.ixNet.setMultiAttribute(bfd_discriminator,
                                      '-clearOverlays', 'false')

        self.ixNet.commit()
        bfd_discriminator_value = self.ixNet.add(bfd_discriminator, 'singleValue')
        self.ixNet.setMultiAttribute(bfd_discriminator_value,
                                      '-value', '1')
        self.ixNet.commit()

        #api for disabling resolve gateway
        print("Disabling Resolve gateway for all ip")
        self.resolve_gateway_disable(ipv4_controller)
        self.resolve_gateway_disable(ipv4_hypervisor)
        self.resolve_gateway_disable(ipv4_vm)
        self.resolve_gateway_disable(ipv4_replicator)
        print ('''
    #---------------------------------------------------------------------------
    #Start Protocols one by one 
    ''')
        print("Start Replicator")
        self.start_protocol(device_group_replicator)

        print("Start VM")
        self.start_protocol(device_group_vm)

        print("Start ovsdb controller")
        self.start_protocol(device_group_controller)
        time.sleep(30)
        print ('''
    #---------------------------------------------------------------------------
    #Attaching bindings from 1 - 10
    #---------------------------------------------------------------------------
            ''')
        self.attach_bindings_in_range(ovsdb_controller, 1, 10)
        print ("Waiting for 45 seconds before attaching!!!")
        time.sleep(45)
        print ('''
    #---------------------------------------------------------------------------
    #Execute dump db action
    #---------------------------------------------------------------------------
                ''')
        self.ixNet.execute('dumpDB', ovsdb_controller, self.find_master_controllerIndex(ovsdb_controller))

        print ('''
            #---------------------------------------------------------------------------
            #Fetching all Protocol Summary Stats\n
            #---------------------------------------------------------------------------
            ''')
        # print ("Fetching all Protocol Summary Stats\n")
        viewPage = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
        statcap = self.ixNet.getAttribute(viewPage, '-columnCaptions')
        for statValList in self.ixNet.getAttribute(viewPage, '-rowValues'):
            for statVal in statValList:
                print("***************************************************")
                index = 0
                for satIndv in statVal:
                    print("%-30s:%s" % (statcap[index], satIndv))
                    index = index + 1
                    # end for
                    # end for
        # end for
        print("***************************************************")

        print ("Fetching OVSDB  Protocol per port stats Stats\n")
        viewPage = '::ixNet::OBJ-/statistics/view:"OVSDB Controller Per Port"/page'
        statcap = self.ixNet.getAttribute(viewPage, '-columnCaptions')
        for statValList in self.ixNet.getAttribute(viewPage, '-rowValues'):
            for statVal in statValList:
                print("***************************************************")
                index = 0
                for satIndv in statVal:
                    print("%-30s:%s" % (statcap[index], satIndv))
                    index = index + 1
                    # end for
                    # end for
        # end for
        print("***************************************************")

        print ('''
    #---------------------------------------------------------------------------
    #Stopping all Protocols 
    #---------------------------------------------------------------------------
    ''')
        print("Stop Replicator")
        self.stop_protocol(device_group_replicator)
        print("Stop Hypervisor")
        self.stop_protocol(device_group_hypervisor)
        print("Stop ovsdb controller")
        self.stop_protocol(device_group_controller)

        print ('!!! Test Script Ends !!!')

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information   #
# below                                                                         #
#################################################################################
if __name__ == "__main__":
    ixTclServer = '10.214.100.2'
    ixTclPort = '6767'
    ports = [('10.214.100.77', '2', '1',)]
    version = '8.40'
    controller = ovsdb(ixTclServer, ixTclPort, version)
    controller.main()
