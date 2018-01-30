#!/usr/local/python2.7.6/bin/python2.7

# By Hubert Gee
#
# Description:
#   A sample script using Tkinter to call TCL APIs.
#   This script sources an API file and the APIs are a combination
#   of low level and high level APIs.
#   
#   This script can load a saved config file or resume from an existing
#   configuration.
#   
#   This script was created to test ModifyProtocolInterfaces and IGMP host
#   and Source Mode filtering. 

import Tkinter
import sys
import time

tcl = Tkinter.Tcl()
tcl.eval('package req Ixia')
tcl.eval('source tclApi2.tcl')


tcl.eval('set connect(-tcl_server) "10.219.117.101"')
tcl.eval('set connect(-ixnetwork_tcl_server) "10.219.117.103"')
tcl.eval('set connect(-username) "hgee"')
tcl.eval('set connect(-session_resume_keys) 1')

tcl.eval('set ixiaChassisIp "10.219.117.101"')
tcl.eval('set ixNetworkTclServerIp "10.219.117.103"')
tcl.eval('set userName) "hgee"')
tcl.eval('set portList "1/1 1/2"')
tcl.eval('set port1 "1/1/1"')
tcl.eval('set port2 "1/1/2"')
tcl.eval('set ixncfgFile "/home/hgee/Dropbox/MyIxiaWork/Temp/l2l3_8.10.ixncfg"')


# Uncomment this to load a saved config file
#if tcl.eval('LoadConfigFile') == 1:
#    sys.exit()

# Uncomment this to connect to an existing configuration
status = tcl.eval('ResumeHlt ::connect')

# --------------- IGMP Configurations with Source Mode Filtering ---------------#
# Step 1/3: Create new IGMP Host 
tcl.eval('set igmpHost($port1,-mode) create')
tcl.eval('set igmpHost($port1,-port_handle) $port1')
tcl.eval('set igmpHost($port1,-reset) 1')
tcl.eval('set igmpHost($port1,-msg_interval) 0')
tcl.eval('set igmpHost($port1,-igmp_version) v3')
tcl.eval('set igmpHost($port1,-ip_router_alert) 0')
tcl.eval('set igmpHost($port1,-general_query) 0')
tcl.eval('set igmpHost($port1,-group_query) 0')
tcl.eval('set igmpHost($port1,-filter_mode) exclude')
tcl.eval('set igmpHost($port1,-count) 1')
tcl.eval('set igmpHost($port1,-intf_ip_addr) 1.1.1.1')
tcl.eval('set igmpHost($port1,-neighbor_intf_ip_addr) 11.1.1.1')
tcl.eval('set igmpHost($port1,-intf_prefix_len) 24')
tcl.eval('set igmpHost($port1,-vlan) 1')
tcl.eval('set igmpHost($port1,-vlan_id) 101')
igmpHostHandle = tcl.eval('set igmpHostHandle1($port1) [ConfigIgmpHostHlt ::igmpHost]')

# Create 2/3: Create IGMP Group 1
tcl.eval('set igmpGroup(-mode) create')
tcl.eval('set igmpGroup(-num_groups) 10')
tcl.eval('set igmpGroup(-ip_addr_start) 235.0.0.1')
tcl.eval('set igmpGroup(-ip_addr_step) 0.0.0.1')
tcl.eval('set igmpGroup(-ip_prefix_len) 24')
igmpHostGroupHandle = tcl.eval('set igmpGroupHandle1($port1) [CreateIgmpGroupHlt ::igmpGroup]')

#             Create IGMP Group 2
tcl.eval('set igmpGroup(-mode) create')
tcl.eval('set igmpGroup(-num_groups) 10')
tcl.eval('set igmpGroup(-ip_addr_start) 236.0.0.1')
tcl.eval('set igmpGroup(-ip_addr_step) 0.0.0.1')
tcl.eval('set igmpGroup(-ip_prefix_len) 24')
igmpHostGroupHandle = tcl.eval('set igmpGroupHandle2($port1) [CreateIgmpGroupHlt ::igmpGroup]')

#             Create IGMP Group 3
tcl.eval('set igmpGroup(-mode) create')
tcl.eval('set igmpGroup(-num_groups) 10')
tcl.eval('set igmpGroup(-ip_addr_start) 237.0.0.1')
tcl.eval('set igmpGroup(-ip_addr_step) 0.0.0.1')
tcl.eval('set igmpGroup(-ip_prefix_len) 24')
igmpHostGroupHandle = tcl.eval('set igmpGroupHandle3($port1) [CreateIgmpGroupHlt ::igmpGroup]')


# Create 3/3: Bind IGMP Host to a group 1
tcl.eval('set igmpHostToGroup(-mode) create')
tcl.eval('set igmpHostToGroup(-session_handle) $igmpHostHandle1($port1)')
tcl.eval('set igmpHostToGroup(-group_pool_handle) $igmpGroupHandle1($port1)')
igmpEndpointHandle = tcl.eval('set igmpHostToGroupHandle1($port1) [ConfigIgmpGroupHlt ::igmpHostToGroup]')
# ::ixNet::OBJ-/vport:1/protocols/igmp/host:2/group:1

# Create 3/3: Bind IGMP Host to a group 2
tcl.eval('set igmpHostToGroup(-mode) create')
tcl.eval('set igmpHostToGroup(-session_handle) $igmpHostHandle1($port1)')
tcl.eval('set igmpHostToGroup(-group_pool_handle) $igmpGroupHandle2($port1)')
igmpEndpointHandle = tcl.eval('set igmpHostToGroupHandle2($port1) [ConfigIgmpGroupHlt ::igmpHostToGroup]')


# Create IGMP Source 1
tcl.eval('set igmpSource(-mode) create')
tcl.eval('set igmpSource(-num_sources) 3')
tcl.eval('set igmpSource(-ip_addr_start) 1.1.1.11')
tcl.eval('set igmpSource(-ip_addr_step) 0.0.0.1')
tcl.eval('set igmpSource(-ip_prefix_len) 24')
tcl.eval('set igmpSourceHandle1($port1) [ConfigIgmpSourceHlt ::igmpSource]')

# Create IGMP Source 2
tcl.eval('set igmpSource2(-mode) create')
tcl.eval('set igmpSource2(-num_sources) 3')
tcl.eval('set igmpSource2(-ip_addr_start) 10.1.1.11')
tcl.eval('set igmpSource2(-ip_addr_step) 0.0.0.1')
tcl.eval('set igmpSource2(-ip_prefix_len) 24')
tcl.eval('set igmpSourceHandle2($port1) [ConfigIgmpSourceHlt ::igmpSource2]')


# Config IGMP Source Include
tcl.eval('set igmpSourceInclude(-mode) create')
tcl.eval('set igmpSourceInclude(-session_handle) $igmpHostHandle1($port1)')
tcl.eval('set igmpSourceInclude(-group_pool_handle) $igmpGroupHandle3($port1)')
tcl.eval('set igmpSourceInclude(-source_pool_handle) [list $igmpSourceHandle1($port1) $igmpSourceHandle2($port1)]') 
tcl.eval('set igmpSourceHandle($port1) [ConfigIgmpGroupHlt ::igmpSourceInclude]')


# Modify source mode to include or exclude
# ::ixNet::OBJ-/vport:1/protocols/igmp/host:3/group:3
tcl.eval('ConfigIgmpSourceMode $igmpSourceHandle($port1) include')

# Enable/Disable IGMP Group
#tcl.eval('EnableIgmpGroup $port1 "235.0.0.1 236.0.0.1"')
#tcl.eval('DisableIgmpGroup $port1 "235.0.0.1 236.0.0.1"')
