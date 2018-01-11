
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright 1997 - 2015 by IXIA                                             #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    06/04/2015 - Sumit Deb - created sample                                   #
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
#    This script intends to demonstrate how to use NGPF StaticLag API.         #
#    Script uses four ports to demonstrate LAG properties                      #
#                                                                              #
#    1. It will create 2 StaticLag topologies, each having two ports which are #
#       LAG members. It will then modify the Lag Id for both the LAG systems   #
#    2. Start the StaticLag protocol.                                          #
#    3. Retrieve protocol statistics and StaticLag per port statistics         #
#    4. Perform Simulate Link Down on port1 in System1-StaticLag-LHS           #
#    5. Retrieve protocol statistics and StaticLag per port statistics         #
#    6. Perform Simulate Link Up on port1 in System1-StaticLag-LHS             #
#    7. Retrieve protocol statistics and StaticLag per port statistics         #
#    8. Stop All protocols                                                     #
#   Ixia Software:                                                             #
#    IxOS      6.90EA                                                          #
#    IxNetwork 7.50EA                                                          #
#                                                                              #
################################################################################

# Import other procedures used in the script, that do not use HL API
# configuration/control procedures
from pprint import pprint
import sys, os
import time, re

# Import packages that are required by  Ixia HL API.
from ixiatcl   import IxiaTcl
from ixiahlt   import IxiaHlt
from ixiangpf  import IxiaNgpf
from ixiaerror import IxiaError

ixiatcl  = IxiaTcl()
ixiahlt  = IxiaHlt(ixiatcl)
ixiangpf = IxiaNgpf(ixiahlt)

################################################################################
# Utilities                                                                    #
################################################################################

try:
    ErrorHandler('', {})
except (NameError,):
    def ErrorHandler(cmd, retval):
        global ixiatcl
        err = ixiatcl.tcl_error_info()
        log = retval['log']
        additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
        raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)
    # end  def ErrorHandler
# end try/except

################################################################################
# Connection to the chassis, IxNetwork Tcl Server                              #
################################################################################
chassis_ip           = ['10.205.28.173']
tcl_server           = '10.205.28.173'
port_list            = [['1/1', '1/2', '1/3', '1/4']]
ixnetwork_tcl_server = '10.205.28.41:5555';
cfgErrors            = 0

print("------------------------------------------------")
print("Printing connection variables ... ")
print("chassis_ip =  %s" % chassis_ip)
print("tcl_server = %s " % tcl_server)
print("ixnetwork_tcl_server = %s" % ixnetwork_tcl_server)
print("port_list = %s " % port_list)
print("------------------------------------------------")

print("Connecting to chassis and client")
connect_result = ixiangpf.connect(
    ixnetwork_tcl_server = ixnetwork_tcl_server,
    tcl_server           = tcl_server,
    device               = chassis_ip,
    port_list            = port_list,
    break_locks          = 1,
    reset                = 1,
)

if connect_result['status'] != '1':
    ErrorHandler('connect', connect_result)
# end if

print(" Printing connection result")
pprint(connect_result)

#Retrieving the port handles, in a list
ports = connect_result['vport_list'].split()

################################################################################
# Configure Topology, Device Group                                             #
################################################################################

#  Creating a topology on 1st and 3rd port
print("Adding topology 1 on port 1 and port 3")
_result_ = ixiangpf.topology_config(
    topology_name = 'LAG1-LHS',
    port_handle   = [ ports[0], ports[2] ],
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
# end if
topology_1_handle = _result_['topology_handle']

# Creating a device group in topology
print("Creating device group 1 in topology 1")
_result_ = ixiangpf.topology_config(
    topology_handle         = topology_1_handle,
    device_group_name       = 'SYSTEM1-StaticLag-LHS',
    device_group_multiplier = '1',
    device_group_enabled    = '1',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
#end if
deviceGroup_1_handle = _result_['device_group_handle']

# Creating a topology on 2nd and 4th port
print("Adding topology 2 on port 2 and port 4")
_result_ = ixiangpf.topology_config(
    topology_name = 'LAG1-RHS',
    port_handle   = [ ports[1], ports[3] ],
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
# end if
topology_2_handle = _result_['topology_handle']

# Creating a device group in topology
print("Creating device group 2 in topology 2")
_result_ = ixiangpf.topology_config(
    topology_handle         = topology_2_handle,
    device_group_name       = 'SYSTEM1-StaticLag-LHS',
    device_group_multiplier = '1',
    device_group_enabled    = '1',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', _result_)
# end if
deviceGroup_2_handle = _result_['device_group_handle']

################################################################################
# Configure staticLag                                                          #
################################################################################
# Creating ethernet stack for the first Device Group
print("Creating ethernet stack for the first Device Group")
_result_ = ixiangpf.interface_config(
    protocol_name     = 'Ethernet 1',
    protocol_handle   = deviceGroup_1_handle,
    mtu               = '1500',
    src_mac_addr      = '00.11.01.00.00.01',
    src_mac_addr_step = '00.00.01.00.00.00',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)
# end if
ethernet_1_handle = _result_['ethernet_handle']

# Creating ethernet stack for the second Device Group
print("Creating ethernet for the second Device Group")
_result_ = ixiangpf.interface_config(
    protocol_name                = 'Ethernet 2',
    protocol_handle              = deviceGroup_2_handle,
    mtu                          = '1500',
    src_mac_addr                 = '00.12.01.00.00.01',
    src_mac_addr_step            = '00.00.01.00.00.00',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', _result_)
# end if
ethernet_2_handle = _result_['ethernet_handle']

# Creating Static LAG on top of Ethernet Stack for the first Device Group LAG with id 666
print("\nCreating Static LAG on top of Ethernet Stack for the first Device Group with LAG id 666")
_result_ = ixiangpf.multivalue_config(
        pattern                 = "single_value",
        single_value            = "1",
        nest_step               = "1",
        nest_owner              = '%s' % (topology_1_handle),
        nest_enabled            = "0",
        overlay_value           = "666,666",
        overlay_value_step      = "666,666",
        overlay_index           = "1,2",
        overlay_index_step      = "0,0",
        overlay_count           = "1,1",
    )
if _result_['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('multivalue_config', _result_)

sys1_lhs_lagId_multivalue_handle = _result_['multivalue_handle']

_result_ = ixiangpf.emulation_lacp_link_config(
    mode              = "create",
    handle            = ethernet_1_handle,
    active            = "1",
    session_type      = "staticLag",
    lag_id            = sys1_lhs_lagId_multivalue_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('emulation_lacp_link_config', _result_)
staticLag_1_handle = _result_['staticLag_handle']

# Creating Static LAG on top of Ethernet Stack for the second Device Group with LAG id 777
print("\nCreating Static LAG on top of Ethernet Stack for the second Device Group with LAG id 777")
_result_ = ixiangpf.multivalue_config(
        pattern                 = "single_value",
        single_value            = "1",
        nest_step               = "1",
        nest_owner              = '%s' % (topology_2_handle),
        nest_enabled            = "0",
        overlay_value           = "777,777",
        overlay_value_step      = "777,777",
        overlay_index           = "1,2",
        overlay_index_step      = "0,0",
        overlay_count           = "1,1",
    )
if _result_['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('multivalue_config', _result_)

sys1_rhs_lagId_multivalue_handle = _result_['multivalue_handle']

_result_ = ixiangpf.emulation_lacp_link_config(
    mode              = "create",
    handle            = ethernet_2_handle,
    active            = "1",
    session_type      = "staticLag",
    lag_id            = sys1_rhs_lagId_multivalue_handle,
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('emulation_lacp_link_config', _result_)
staticLag_2_handle = _result_['staticLag_handle']

print("Waiting 5 seconds before starting protocol(s) ...")
time.sleep(5)

################################################################################
# Start protocol                                                               #
################################################################################
print("Starting StaticLAG on topology1")
_result_ = ixiahlt.test_control(action='start_all_protocols')

print("Waiting for 30 seconds")
time.sleep(30)

################################################################################
# Get Static LAG learned_info   stats                                          #
################################################################################
print("Fetching SYSTEM1-StaticLag-LHS learned_info")

staticLag1_stats = ixiangpf.emulation_lacp_info(
    handle = staticLag_1_handle,
    mode   = 'global_learned_info',
    session_type = "staticLag",
)
if staticLag1_stats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_lacp_info', staticLag1_stats)
# end if
print("\n\nPrinting SYSTEM1-StaticLag-LHS learned_info")
pprint(staticLag1_stats)

print("\n\nFetching SYSTEM1-StaticLag-RHS per port stats")
staticLag2_stats = ixiangpf.emulation_lacp_info(
    handle = staticLag_2_handle,
    mode   = 'per_port',
    session_type = "staticLag",
)
if staticLag2_stats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_lacp_info', staticLag2_stats)
# end if
print("\n\nPrinting SYSTEM1-StaticLag-RHS per port stats")
pprint(staticLag2_stats)

time.sleep(5)

################################################################################
# Perform Simulate Link Down on port1 in System1-StaticLag-LHS                 #
################################################################################
print("\n\nPerform Simulate Link Down on port1 in System1-StaticLag-LHS ")

_result_ = ixiangpf.interface_config(
    port_handle     =  ports[0],
    op_mode     = 'sim_disconnect',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('interface_config', _result_)
time.sleep(5)
################################################################################
# Get Static LAG learned_info and per-port stats                               #
################################################################################
print("Fetching SYSTEM1-StaticLag-LHS learned_info")

staticLag1_stats = ixiangpf.emulation_lacp_info(
    handle = staticLag_1_handle,
    mode   = 'global_learned_info',
    session_type = "staticLag",
)
if staticLag1_stats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_lacp_info', staticLag1_stats)
# end if
print("\n\nPrinting SYSTEM1-StaticLag-LHS learned_info")
pprint(staticLag1_stats)

print("\n\nFetching SYSTEM1-StaticLag-RHS per port stats")
staticLag2_stats = ixiangpf.emulation_lacp_info(
    handle = staticLag_2_handle,
    mode   = 'per_port',
    session_type = "staticLag",
)
if staticLag2_stats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_lacp_info', staticLag2_stats)
# end if
print("\n\nPrinting SYSTEM1-StaticLag-RHS per port stats")
pprint(staticLag2_stats)

time.sleep(5)
################################################################################
# Perform Simulate Link Up on port1 in System1-StaticLag-LHS                   #
################################################################################
print("\n\nPerform Simulate Link Up on port1 in System1-StaticLag-LHS ")

_result_ = ixiangpf.interface_config(
    port_handle     =  ports[0],
    op_mode     = 'normal',
)
if _result_['status'] != IxiaHlt.SUCCESS:
    ixnHLT_errorHandler('interface_config', _result_)
time.sleep(5)
################################################################################
# Get Static LAG learned_info and per-port stats                               #
################################################################################
print("Fetching SYSTEM1-StaticLag-LHS learned_info")

staticLag1_stats = ixiangpf.emulation_lacp_info(
    handle = staticLag_1_handle,
    mode   = 'global_learned_info',
    session_type = "staticLag",
)
if staticLag1_stats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_lacp_info', staticLag1_stats)
# end if
print("\n\nPrinting SYSTEM1-StaticLag-LHS learned_info")
pprint(staticLag1_stats)

print("\n\nFetching SYSTEM1-StaticLag-RHS per port stats")
staticLag2_stats = ixiangpf.emulation_lacp_info(
    handle = staticLag_2_handle,
    mode   = 'per_port',
    session_type = "staticLag",
)
if staticLag2_stats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('emulation_lacp_info', staticLag2_stats)
# end if
print("\n\nPrinting SYSTEM1-StaticLag-RHS per port stats")
pprint(staticLag2_stats)

time.sleep(5)

###############################################################################
# Stop all protocols                                                          #
###############################################################################
print "Stopping all protocol(s) ..."
stop = ixiangpf.test_control(action='stop_all_protocols')
if stop['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', stop)
# end if

time.sleep(2)
print "!!! Test Script Ends !!!"
