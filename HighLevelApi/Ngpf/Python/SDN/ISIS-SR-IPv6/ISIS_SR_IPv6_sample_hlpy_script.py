################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997 - 2017 by IXIA                                            #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    09/05/2017 - Shilpam Sinha - created sample                               #
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
#                                                                              #        
# This is a sample script written in HLPy to describe ISIS SR IPv6.It          #
# configures two ISIS router back to back. One of them has                     #
# simulated topology (type linear) configured behind it. The script does       #
# the following operations.                                                    #  
# 1. Starts all the topologies.                                                #
# 2. Check protocol statistics.                                                #
# 3. Checks for learned info.                                                  # 
# 4. OTF change flag bits and weight value in Simulated Interface.             #
# 5. Checks for learned info.                                                  #
# 6. Stops all protocols.                                                      #
#                                                                              #
# Ixia Software:                                                               #
#     IxOS : 8.30 EA                                                           #
#     IxNetwork : 8.30 EA                                                      # 
################################################################################

from pprint import pprint
import sys, os
import time, re

from ixiatcl   import IxiaTcl
from ixiahlt   import IxiaHlt
from ixiangpf  import IxiaNgpf
from ixiaerror import IxiaError

if os.name == 'nt':
    # If the Python version is greater than 3.4 call IxiaTcl with
    # the Tcl 8.6 path.
    # Example: tcl_dependencies = ['/path/to/tcl8.6'];
    # ixiatcl = IxiaTcl(tcl_autopath=tcl_dependencies)
    ixiatcl = IxiaTcl()
else:
    # unix dependencies this may change accoring to your system. This is
    # required to make following packages available to ixiatcl object.
    # 1. Tclx   --> mandatory
    # 2. msgcat --> mandatory
    # 3. mpexpr --> optional
    tcl_dependencies = [
         '/usr/local/lib/',
         '/usr/lib/',
         '/usr/share/tcl8.5',
         '/usr/lib/tcl8.5',
         '/usr/lib/tk8.5',
         '/usr/share/tk8.5',
    ]
    ixiatcl = IxiaTcl(tcl_autopath=tcl_dependencies)
# endif

ixiahlt = IxiaHlt(ixiatcl)
ixiangpf = IxiaNgpf(ixiahlt)
            
try:
    ErrorHandler('', {})
except (NameError,):
    def ErrorHandler(cmd, retval):
        global ixiatcl
        err = ixiatcl.tcl_error_info()
        log = retval['log']
        additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
        raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)

###############################################################################
# Specify your chassis/card port and IxNetwork client here
###############################################################################
chassis_ip           = "10.216.108.99"
tcl_server           = "10.216.108.99"
ixnetwork_tcl_server = "10.216.108.27:8676"
port_list            = "6/3 6/4"
cfgErrors            = 0

print("Printing connection variables ... ")
print('chassis_ip =  %s' % chassis_ip)
print("tcl_server = %s " % tcl_server)
print("ixnetwork_tcl_server = %s" % ixnetwork_tcl_server)
print("port_list = %s " % port_list)

print("Connect to chassis ...")
connect_result = ixiangpf.connect(
        ixnetwork_tcl_server = ixnetwork_tcl_server,
        tcl_server = tcl_server,
        device = chassis_ip,
        port_list = port_list,
        break_locks = 1,
        reset = 1,
    )

if connect_result['status'] != '1':
    ErrorHandler('connect', connect_result)

print(" Printing connection result")
pprint(connect_result)

#Retrieving the port handles, in a list
ports = connect_result['vport_list'].split()

#-------------------------------------------------------------------------------
# Add topology1
#-------------------------------------------------------------------------------
print ('Adding topology1')    
topology_1_status = ixiangpf.topology_config(
        topology_name      = """ISIS Topology 1""",
        port_handle        = ports[0],
)
if topology_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', topology_1_status)
    
topology_1_handle = topology_1_status['topology_handle']

#-------------------------------------------------------------------------------
# Add device group1
#-------------------------------------------------------------------------------
print("Adding device group1\n")
device_group_1_status = ixiangpf.topology_config(
        topology_handle              = topology_1_handle,
        device_group_name            = """Device Group 1""",
        device_group_multiplier      = "1",
        device_group_enabled         = "1",
)
if device_group_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', device_group_1_status)
    
deviceGroup_1_handle = device_group_1_status['device_group_handle']
   
#-------------------------------------------------------------------------------
# Add ethernet stack1
#-------------------------------------------------------------------------------
print("Adding ethernet stack1")
ethernet_1_status = ixiangpf.interface_config(
        protocol_name                = """Ethernet 1""",
        protocol_handle              = deviceGroup_1_handle,
        mtu                          = "1500",
        src_mac_addr                 = "00.11.01.00.00.01",
)
if ethernet_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ethernet_1_status)

ethernet_1_handle = ethernet_1_status['ethernet_handle']
 
#--------------------------------------------------------------------------
# Add IPv6 Stack1
#--------------------------------------------------------------------------
print("Creating IPv6 Stack on top of Ethernet Stack for the first Device Group")
ipv6_1_status = ixiangpf.interface_config(
        protocol_name                     = """IPv6 1""",
        protocol_handle                   = ethernet_1_handle,
        ipv6_multiplier                   = "1",
        ipv6_resolve_gateway              = "1",
        ipv6_manual_gateway_mac           = "00.00.00.00.00.01",
        ipv6_manual_gateway_mac_step      = "00.00.00.00.00.00",
        ipv6_gateway                      = "2000:0:0:1:0:0:0:1",
        ipv6_intf_addr                    = "2000:0:0:1:0:0:0:2",
        ipv6_prefix_length                = "64",
)
if ipv6_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ipv6_1_status)

ipv6_1_handle = ipv6_1_status['ipv6_handle']

#-------------------------------------------------------------------------------
# Add ISIS router1
#-------------------------------------------------------------------------------
print ("Adding ISIS router1")
isis_l3_1_status = ixiangpf.emulation_isis_config(
        mode                                 = "create",
        discard_lsp                          = "0",
        handle                               = ethernet_1_handle,
        intf_type                            = "ptop",
        routing_level                        = "L2",
        area_id                              = "490001",
        system_id                            = "64:01:00:01:00:00 ",
        protocol_name                        = """ISIS-L3 IF 1""",
        active                               = "1",
        if_active                            = "1",
        ipv4_flag                            = "0",
        ipv6_flag                            = "0",
        enable_sr                            = "1",
        interface_enable_adj_sid             = "1",                        
        ipv6_srh_flag_emulated_router        = "1",
        ipv6_node_prefix                     = "7895:0:0:1:0:0:0:1",
        prefix_length_v6                     = "128",
        ipv6_adjacency_sid_value             = "abcd:1:0:1:0:0:0:2",
)
if isis_l3_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_isis_config', isis_l3_1_status)

isisL3_1_handle = isis_l3_1_status['isis_l3_handle']

#--------------------------------------------------------------------------------
# Configure simulated topology1 type == linear
#--------------------------------------------------------------------------------
print("Adding simulated topology1 linear")
network_group_1_status = ixiangpf.network_group_config(
    protocol_handle             = deviceGroup_1_handle,
    protocol_name               = """Network Group 1""",
    multiplier                  = "1",                          
    enable_device               = "1",
    type                        = "linear",
    linear_nodes                = "5",
    linear_link_multiplier      = "1",
)

if network_group_1_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_isis_config', network_group_1_status)

networkGroup_1_handle = network_group_1_status['network_group_handle']

#--------------------------------------------------------------------------------
# Configure ISIS and ISIS-SR related parameters in the simulated topology1
#--------------------------------------------------------------------------------
print("Configuring ISIS route parameter in the simulated topology")
network_isis_grp_status = ixiangpf.emulation_isis_network_group_config(
    handle                                          = networkGroup_1_handle,
    mode                                            = "modify",
    connected_to_handle                             = ethernet_1_handle,    
    router_system_id                                = "a1:01:00:00:00:01",
    enable_ip                                       = "1",
    sim_topo_active                                 = "1",
    grid_router_active                              = "1",
    link_type                                       = "pttopt",
    si_enable_adj_sid                               = "1",
    si_adj_sid                                      = "8001",
    pseudo_node_enable_sr                           = "1",
    ipv6_adjacency_sid_value                        = "55fe:1:0:1:0:0:0:2",
    ipv6_node_prefix                                = "7878:0:0:1:0:0:0:1",
    prefix_length_v6                                = "128",
    ipv6_srh_flag_pseudonode_routes_v6              = "1",
    ipv6_srh_flag_pseudo_router                     = "1",
)

if network_isis_grp_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_isis_config', network_isis_grp_status)

simtopo_1_handle = network_isis_grp_status['network_group_handle']

#-------------------------------------------------------------------------------
# Add topology2
#-------------------------------------------------------------------------------
print ('Adding topology2')    
topology_2_status = ixiangpf.topology_config(
        topology_name      = """ISIS Topology 2""",
        port_handle        = ports[1],
)
if topology_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', topology_2_status)
    
topology_2_handle = topology_2_status['topology_handle']

#-------------------------------------------------------------------------------
# Add device group1
#-------------------------------------------------------------------------------
print("Adding device group2\n")
device_group_2_status = ixiangpf.topology_config(
        topology_handle              = topology_2_handle,
        device_group_name            = """Device Group 2""",
        device_group_multiplier      = "1",
        device_group_enabled         = "1",
)
if device_group_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', device_group_2_status)
    
deviceGroup_2_handle = device_group_2_status['device_group_handle']
   
#-------------------------------------------------------------------------------
# Add ethernet stack2
#-------------------------------------------------------------------------------
print("Adding ethernet stack2")
ethernet_2_status = ixiangpf.interface_config(
        protocol_name                = """Ethernet 2""",
        protocol_handle              = deviceGroup_2_handle,
        mtu                          = "1500",
        src_mac_addr                 = "00.12.01.00.00.01",
)
if ethernet_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ethernet_2_status)

ethernet_2_handle = ethernet_2_status['ethernet_handle']
 
#--------------------------------------------------------------------------
# Add IPv6 Stack2
#--------------------------------------------------------------------------
print("Creating IPv6 Stack on top of Ethernet Stack for the second Device Group")
ipv6_2_status = ixiangpf.interface_config(
        protocol_name                     = """IPv6 2""",
        protocol_handle                   = ethernet_2_handle,
        ipv6_multiplier                   = "1",
        ipv6_resolve_gateway              = "1",
        ipv6_manual_gateway_mac           = "00.00.00.00.00.01",
        ipv6_manual_gateway_mac_step      = "00.00.00.00.00.00",
        ipv6_gateway                      = "2000:0:0:1:0:0:0:2",
        ipv6_intf_addr                    = "2000:0:0:1:0:0:0:1",
        ipv6_prefix_length                = "64",
)
if ipv6_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', ipv6_2_status)

ipv6_2_handle = ipv6_2_status['ipv6_handle']

#-------------------------------------------------------------------------------
# Add ISIS router2
#-------------------------------------------------------------------------------
print ("Adding ISIS router1")
isis_l3_2_status = ixiangpf.emulation_isis_config(
        mode                                 = "create",
        discard_lsp                          = "0",
        handle                               = ethernet_2_handle,
        intf_type                            = "ptop",
        routing_level                        = "L2",
        area_id                              = "500001",
        system_id                            = "65:01:00:01:00:00 ",
        protocol_name                        = """ISIS-L3 IF 2""",
        active                               = "1",
        if_active                            = "1",
        ipv4_flag                            = "0",
        ipv6_flag                            = "0",
        enable_sr                            = "1",
        interface_enable_adj_sid             = "1",                        
        ipv6_srh_flag_emulated_router        = "1",
        ipv6_node_prefix                     = "9087:0:0:1:0:0:0:1",
        prefix_length_v6                     = "128",
        ipv6_adjacency_sid_value             = "3214:1:0:1:0:0:0:2",
)
if isis_l3_2_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_isis_config', isis_l3_2_status)

isisL3_2_handle = isis_l3_2_status['isis_l3_handle']

#--------------------------------------------------------------------------
# Start all the protocols                                                    
#--------------------------------------------------------------------------
print ('Starting all protocol !!!')
	
status = ixiangpf.test_control(action='start_all_protocols')
if status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('ixiangpf.test_control', status)

print ('Waiting for 120 seconds')
time.sleep(120)

#-------------------------------------------------------------------------------
# Fetching ISIS statistics
#-------------------------------------------------------------------------------

print ('Fetching statistics on ISIS router1')               
status = ixiangpf.emulation_isis_info(\
        handle = isisL3_1_handle,
        mode   = 'stats')
if status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_info', status)

#-------------------------------------------------------------------------------
# printing stat values
#-------------------------------------------------------------------------------


print('===================================================================================')
pprint(status)
print('===================================================================================')

#-------------------------------------------------------------------------------
# Fetching ISIS statistics
#-------------------------------------------------------------------------------

print ('Fetching statistics on ISIS router2')
status = ixiangpf.emulation_isis_info(\
        handle = isisL3_2_handle,
        mode   = 'stats')
if status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_info', status)

#-------------------------------------------------------------------------------
# printing stat values
#-------------------------------------------------------------------------------

print('==================================================================================')
pprint(status)
print('==================================================================================')

#-------------------------------------------------------------------------------
# Fetching learned info
#-------------------------------------------------------------------------------

print ('Fetching Learned Info on ISIS router2')
status = ixiangpf.emulation_isis_info(\
        handle = isisL3_2_handle,
        mode   = 'learned_info')
if status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_info', status)

#-------------------------------------------------------------------------------
# printing stat values
#-------------------------------------------------------------------------------

print('===================================================================================')
pprint(status)
print('===================================================================================')

#----------------------------------------------------------------------------
# OTF changing the valye of BGPLS ID & Instance ID                         
#----------------------------------------------------------------------------
print('Changing Attribute Values in Simulated Interfaces OTF')
isis_ng = ixiangpf.emulation_isis_network_group_config(
    handle                                          = simtopo_1_handle,
    mode                                            = "modify",
    si_b_flag                                       = "1",
    si_v_flag                                       = "0",
    si_l_flag                                       = "0",
    si_s_flag                                       = "1",
    si_weight                                       = "0",
)

if isis_ng['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_isis_config', isis_ng)


print ("Applying changes on the fly")
try :
    ixiangpf.test_control( action = 'apply_on_the_fly_changes')
except :
    print("error in applying on the fly change")

time.sleep(10)

#-------------------------------------------------------------------------------
# Fetching learned info
#-------------------------------------------------------------------------------

print ('Fetching Learned Info on ISIS router2')
status = ixiangpf.emulation_isis_info(\
        handle = isisL3_2_handle,
        mode   = 'learned_info')
if status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_igmp_info', status)

#-------------------------------------------------------------------------------
# printing stat values
#-------------------------------------------------------------------------------

print('===================================================================================')
pprint(status)
print('===================================================================================')

#-------------------------------------------------------------------------------
# Stopping all protocols
#-------------------------------------------------------------------------------
print ('Stopping all protocol(s) ...')
stop = ixiangpf.test_control(action='stop_all_protocols')
                  
if stop['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', stop)

#-------------------------------------------------------------------------------
# Test Ends
#-------------------------------------------------------------------------------
print ('!!! Test Script Ends !!!')


