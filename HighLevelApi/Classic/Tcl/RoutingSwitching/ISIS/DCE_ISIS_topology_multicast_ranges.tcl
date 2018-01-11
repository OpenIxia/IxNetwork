################################################################################
# Version 1.0    $Revision: 1 $
# $Author: B. Danciu $
#
# $Workfile: DCE_ISIS_topology_multicast_ranges.tcl $
#
#    Copyright © 1997 - 2009 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    4-10-2009 create.
#
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample creates 3 DCE ISIS router bridges in Ixia back to back setup  #
# and adds a multicast mac range on first bridge, a multicast ipv4 group range #
# on second bridge and a multicast ipv6 group range on third bridge. The       #
# configuration is similar on second port. Then it starts the router bridges   #
# and get the protocol stats from port handles and retrieve the protocol       #
# learned info from bridge handles.                                            #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module using HLTSET 48             #
#                                                                              #
################################################################################

set hltset "HLTSET48"
set env(IXIA_VERSION) $hltset

package require Ixia

set test_name [info script]

set chassisIP 10.205.19.121
set port_list [list 6/1 6/2]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                            \
        -reset                                                                 \
        -device                         $chassisIP                             \
        -port_list                      $port_list                             \
        -username                       ixiaApiUser                            \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
            temp_port]} {
        lappend port_handle $temp_port
    }
}
set port_0 [lindex $port_handle 0]
set port_1 [lindex $port_handle 1]

puts "Ixia port handles are: $port_0, $port_1 ..."
update idletasks

################################################################################
# Configure interface in the test
################################################################################
set interface_status [::ixia::interface_config                                 \
        -port_handle                    [list $port_0 $port_1]                 \
        -intf_mode                      ethernet                               \
        -autonegotiation                1                                      \
        -speed                          auto                                   \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}
puts "Ixia port configuration returned: [keylget interface_status status] ..."
update idletasks

################################################################################
# Create protocol interface for the second port
################################################################################
set interface_status [::ixia::interface_config                                     \
        -mode               modify                                                 \
        -port_handle        [list $port_1           $port_1         $port_1]       \
        -intf_ip_addr       [list 121.1.1.2         122.1.1.2       123.1.1.2]     \
        -gateway            [list 121.1.1.1         122.1.1.1       123.1.1.1]     \
        -netmask            [list 255.255.255.0     255.255.255.0   255.255.255.0] \
        -ipv6_intf_addr     [list 121::2            122::2          123::2]        \
        -ipv6_prefix_length [list 64                64              64]            \
        -vlan               1                                                      \
        -vlan_id            [list 2 3 4]                                           \
        -src_mac_addr       [list 0cd0.0021.0001    0cd0.0022.0002  0cd0.0023.0003]\
        ]
if {[keylget interface_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}
set interface_handle [keylget interface_status interface_handle]
set interface_3 [lindex $interface_handle 0]
set interface_4 [lindex $interface_handle 1]
set interface_5 [lindex $interface_handle 2]
puts "Ixia interface configuration returned: $interface_handle ..."
update idletasks

################################################################################
# Create DCE ISIS bridges on first port
################################################################################
set isis_router_status [::ixia::emulation_isis_config                          \
        -mode                           create                                 \
        -reset                                                                 \
        -port_handle                    $port_0                                \
        -type                           dce_isis_draft_ward_l2_isis_04         \
        -ip_version                     4_6                                    \
        -intf_ip_addr                   121.1.1.1                              \
        -intf_ip_addr_step              1.0.0.0                                \
        -gateway_ip_addr                121.1.1.2                              \
        -gateway_ip_addr_step           1.0.0.0                                \
        -intf_ip_prefix_length          24                                     \
        -intf_ipv6_addr                 121:0:0:0:0:0:0:1                      \
        -intf_ipv6_addr_step            1:0:0:0:0:0:0:0                        \
        -intf_ipv6_prefix_length        64                                     \
        -count                          3                                      \
        -dce_capability_router_id       121.1.1.1                              \
        -dce_bcast_root_priority        65535                                  \
        -dce_num_mcast_dst_trees        2                                      \
        -dce_device_id                  10                                     \
        -dce_device_pri                 255                                    \
        -dce_ftag_enable                1                                      \
        -dce_ftag                       65535                                  \
        -wide_metrics                   1                                      \
        -discard_lsp                    0                                      \
        -attach_bit                     1                                      \
        -vlan                           1                                      \
        -vlan_id                        2                                      \
        -vlan_id_mode                   increment                              \
        -vlan_id_step                   1                                      \
        -vlan_user_priority             0                                      \
        -mac_address_init               0ab0.0021.0001                         \
        -mac_address_step               0000.0001.0001                         \
        ]
if {[keylget isis_router_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget isis_router_status log]"
    return 0
}

#Get the list of ISIS router handle form the keye list returned
set isis_router_handle_list_0 [keylget isis_router_status handle]
set isis_router_handle_0 [lindex $isis_router_handle_list_0 0]
set isis_router_handle_1 [lindex $isis_router_handle_list_0 1]
set isis_router_handle_2 [lindex $isis_router_handle_list_0 2]
################################################################################
# Create DCE ISIS bridges on second port
################################################################################
set isis_router_status [::ixia::emulation_isis_config                          \
        -mode                           create                                 \
        -reset                                                                 \
        -port_handle                    $port_1                                \
        -type                           dce_isis_draft_ward_l2_isis_04         \
        -interface_handle               [list $interface_3 $interface_4 $interface_5] \
        -count                          3                                      \
        -dce_capability_router_id       121.1.1.2                              \
        -dce_bcast_root_priority        0                                      \
        -dce_num_mcast_dst_trees        1                                      \
        -dce_device_id                  0                                      \
        -dce_device_pri                 0                                      \
        -dce_ftag_enable                1                                      \
        -dce_ftag                       0                                      \
        -wide_metrics                   0                                      \
        -discard_lsp                    0                                      \
        -attach_bit                     0                                      \
        ]
if {[keylget isis_router_status status] != $::SUCCESS} {
    return 0 "FAIL - $test_name - [keylget isis_router_status log]"
}
set isis_router_handle_list_1 [keylget isis_router_status handle]
set isis_router_handle_3 [lindex $isis_router_handle_list_1 0]
set isis_router_handle_4 [lindex $isis_router_handle_list_1 1]
set isis_router_handle_5 [lindex $isis_router_handle_list_1 2]

################################################################################
# Create DCE ISIS ranges
################################################################################
set route_config_status_0 [::ixia::emulation_isis_topology_route_config        \
        -mode                               create                             \
        -handle                             $isis_router_handle_0              \
        -type                               dce_mcast_mac_range                \
        -dce_vlan_id                        2                                  \
        -dce_mcast_start_addr               A201.0000.0200                     \
        -dce_mcast_addr_count               2                                  \
        -dce_mcast_addr_step                0000.0000.0200                     \
        -dce_ucast_sources_per_mcast_addr   2                                  \
        -dce_ucast_src_addr                 B200.0000.B200                     \
        -dce_intra_grp_ucast_step           0000.0000.0020                     \
        -dce_inter_grp_ucast_step           0000.0000.0002                     \
        -dce_src_grp_mapping                manual_mapping                     \
        ]

if {[keylget route_config_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget route_config_status_0 log]"
    return 0
}

set route_config_status_1 [::ixia::emulation_isis_topology_route_config        \
        -mode                               create                             \
        -handle                             $isis_router_handle_1              \
        -type                               dce_mcast_ipv4_group_range         \
        -dce_vlan_id                        3                                  \
        -dce_mcast_start_addr               230.0.0.1                          \
        -dce_mcast_addr_count               3                                  \
        -dce_mcast_addr_step                0.30.0.0                           \
        -dce_ucast_sources_per_mcast_addr   3                                  \
        -dce_ucast_src_addr                 30.0.0.1                           \
        -dce_intra_grp_ucast_step           0.0.0.30                           \
        -dce_inter_grp_ucast_step           0.0.30.0                           \
        -dce_src_grp_mapping                manual_mapping                     \
        ]

if {[keylget route_config_status_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget route_config_status_1 log]"
    return 0
}

set route_config_status_2 [::ixia::emulation_isis_topology_route_config        \
        -mode                               create                             \
        -handle                             $isis_router_handle_2              \
        -type                               dce_mcast_ipv6_group_range         \
        -dce_vlan_id                        4                                  \
        -dce_mcast_start_addr               FF00::1                            \
        -dce_mcast_addr_count               4                                  \
        -dce_mcast_addr_step                0::40:0:0                          \
        -dce_ucast_sources_per_mcast_addr   4                                  \
        -dce_ucast_src_addr                 40::1                              \
        -dce_intra_grp_ucast_step           0::40                              \
        -dce_inter_grp_ucast_step           0::40:0                            \
        -dce_src_grp_mapping                manual_mapping                     \
        ]

if {[keylget route_config_status_2 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget route_config_status_2 log]"
    return 0
}

set route_config_status_3 [::ixia::emulation_isis_topology_route_config        \
        -mode                               create                             \
        -handle                             $isis_router_handle_3              \
        -type                               dce_mcast_mac_range                \
        -dce_vlan_id                        2                                  \
        -dce_mcast_start_addr               C301.0000.0300                     \
        -dce_mcast_addr_count               2                                  \
        -dce_mcast_addr_step                0000.0000.0300                     \
        -dce_ucast_sources_per_mcast_addr   2                                  \
        -dce_ucast_src_addr                 D300.0000.D300                     \
        -dce_intra_grp_ucast_step           0000.0000.0003                     \
        -dce_inter_grp_ucast_step           0000.0000.0030                     \
        -dce_src_grp_mapping                manual_mapping                     \
        ]

if {[keylget route_config_status_3 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget route_config_status_3 log]"
    return 0
}

set route_config_status_4 [::ixia::emulation_isis_topology_route_config        \
        -mode                               create                             \
        -handle                             $isis_router_handle_4              \
        -type                               dce_mcast_ipv4_group_range         \
        -dce_vlan_id                        3                                  \
        -dce_mcast_start_addr               231.0.0.1                          \
        -dce_mcast_addr_count               3                                  \
        -dce_mcast_addr_step                0.30.0.0                           \
        -dce_ucast_sources_per_mcast_addr   3                                  \
        -dce_ucast_src_addr                 31.0.0.1                           \
        -dce_intra_grp_ucast_step           0.0.0.30                           \
        -dce_inter_grp_ucast_step           0.0.30.0                           \
        -dce_src_grp_mapping                manual_mapping                     \
        ]

if {[keylget route_config_status_4 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget route_config_status_4 log]"
    return 0
}

set route_config_status_5 [::ixia::emulation_isis_topology_route_config        \
        -mode                               create                             \
        -handle                             $isis_router_handle_5              \
        -type                               dce_mcast_ipv6_group_range         \
        -dce_vlan_id                        4                                  \
        -dce_mcast_start_addr               FF01::1                            \
        -dce_mcast_addr_count               4                                  \
        -dce_mcast_addr_step                0::40:0:0                          \
        -dce_ucast_sources_per_mcast_addr   4                                  \
        -dce_ucast_src_addr                 41::1                              \
        -dce_intra_grp_ucast_step           0::40                              \
        -dce_inter_grp_ucast_step           0::40:0                            \
        -dce_src_grp_mapping                manual_mapping                     \
        ]

if {[keylget route_config_status_5 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget route_config_status_5 log]"
    return 0
}
################################################################################
# Start protocol
################################################################################
set isis_info_handle_0 [::ixia::emulation_isis_control                         \
        -mode                               start                              \
        -port_handle                        [list $port_0 $port_1 ]            \
        ]

if {[keylget isis_info_handle_0 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_info_handle_0 log]"
}

# wait 30sec to start the protocol and learn stats
after 30000

##############################################
#SHOW STATS PROCEDURE - printing statistics  #
##############################################

proc show_stats var {
    set level [expr [info level] - 1]
    foreach key [keylkeys var] {
	if {$key == "status"} {continue}
	set indent [string repeat "    " $level] 
	puts -nonewline $indent 
	if {[catch {keylkeys var $key}]} {
	    puts "$key: [keylget var $key]"
	    continue
	} else {
	    puts $key
	    puts "$indent[string repeat "-" [string length $key]]"
	}
	show_stats [keylget var $key]
    }
}

################################################################################
# Retrieve protocol stats 
################################################################################
set isis_stats_0 [::ixia::emulation_isis_info                                  \
        -mode                               stats                              \
        -port_handle                        $port_0                            \
        ]

if {[keylget isis_stats_0 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_stats_0 log]"
}
puts "isis_stats_0 stats: -----------------------------------"
show_stats $isis_stats_0

set isis_stats_1 [::ixia::emulation_isis_info                                  \
        -mode                               stats                              \
        -port_handle                        $port_1                            \
        ]

if {[keylget isis_stats_1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_stats_1 log]"
}
puts "isis_stats_1 stats: -----------------------------------"
show_stats $isis_stats_1

################################################################################
# Retrieve protocol learned info 
################################################################################

set isis_learned_info_0 [::ixia::emulation_isis_info                           \
        -mode                               learned_info                       \
        -handle                             $isis_router_handle_3              \
        ]

if {[keylget isis_learned_info_0 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_learned_info_0 log]"
}
puts "isis_learned_info_0 learned_info: -----------------------------------"
show_stats $isis_learned_info_0

set isis_learned_info_1 [::ixia::emulation_isis_info                           \
        -mode                               learned_info                       \
        -handle                             $isis_router_handle_4              \
        ]

if {[keylget isis_learned_info_1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_learned_info_1 log]"
}
puts "isis_learned_info_1 learned_info: -----------------------------------"
show_stats $isis_learned_info_1

set isis_learned_info_2 [::ixia::emulation_isis_info                           \
       -mode                               learned_info                        \
       -handle                             $isis_router_handle_5               \
       ]

if {[keylget isis_learned_info_2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_learned_info_2 log]"
}
puts "isis_learned_info_2 learned_info: -----------------------------------"
show_stats $isis_learned_info_2

#::ixia::cleanup_session -reset -port_handle $port_handle

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1
