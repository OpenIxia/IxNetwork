################################################################################
# Version 1.1    $Revision: 2 $
# $Author: Matei-Eugen Vasile $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    3-29-2007 initial version - Matei-Eugen Vasile
#    5-4-2007 added statistics result display code - Matei-Eugen Vasile
#	 7-3-2013 revised and optimized for HLT 4.71.95.15 - Marian-Octavian Preda
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
#    This sample creates 2 IS-IS routers on 2 different Ixia ports, adds       #
#    route ranges to be advertised on both routers, starts the routing         #
#    protocol and, finally, gathers the IS-IS statistics from both routers.    #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module in a back-to-back configuration.   #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP ixro-hlt-xm2-02
set port_list [list 1/3 1/4]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect 					  \
        -reset                    						\
        -device    $chassisIP     						\
        -port_list $port_list     						\
        -username  ixiaApiUser  						\
		]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle1 [keylget connect_status port_handle.$chassisIP.[lindex $port_list 0]]
set port_handle2 [keylget connect_status port_handle.$chassisIP.[lindex $port_list 1]]

##########################################
# Configure interface in the test (IPv4) #
##########################################
set interface_status [::ixia::interface_config                \
        -port_handle     [list $port_handle1 $port_handle2] \
        -autonegotiation 1                                  \
        -duplex          full                               \
        -speed           ether100                           \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

#########################################
# Configure the first IS-IS L1L2 router #
#########################################
set isis_router_status [::ixia::emulation_isis_config     \
        -mode                           create          \
        -reset                                          \
        -port_handle                    $port_handle1   \
        -intf_ip_addr                   22.1.1.2        \
        -gateway_ip_addr                22.1.1.1        \
        -intf_ip_prefix_length          24              \
        -mac_address_init               0000.0000.0001  \
        -count                          1               \
        -wide_metrics                   1               \
        -discard_lsp                    1               \
        -attach_bit                     1               \
        -partition_repair               1               \
        -overloaded                     1               \
        -lsp_refresh_interval           888             \
        -lsp_life_time                  777             \
        -max_packet_size                1492            \
        -intf_metric                    0               \
        -routing_level                  L1L2            \
        -te_enable                      1               \
        -te_max_bw                      10              \
        -te_max_resv_bw                 20              \
        -te_unresv_bw_priority0         10              \
        -te_unresv_bw_priority2         20              \
        -te_unresv_bw_priority3         30              \
        -te_unresv_bw_priority4         40              \
        -te_unresv_bw_priority5         50              \
        -te_unresv_bw_priority6         60              \
        -te_unresv_bw_priority7         70              \
        -te_metric                      10              \
        ]
if {[keylget isis_router_status status] != $::SUCCESS} {
    return "FAIL - [keylget isis_router_status log]"
}

set router_handle1 [keylget isis_router_status handle]

#####################################################
# Add a stub route range for the first IS-IS router #
#####################################################
set route_config_status [::ixia::emulation_isis_topology_route_config \
        -mode                   create                              \
        -handle                 $router_handle1                     \
        -type                   stub                                \
        -ip_version             4                                   \
        -stub_ip_start          44.0.0.1                            \
        -stub_ip_pfx_len        20                                  \
        -stub_count             5                                   \
        -stub_metric            22                                  \
        -stub_up_down_bit       1                                   \
        ]
if {[keylget route_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget route_config_status log]"
}

##########################################
# Configure the second IS-IS L1L2 router #
##########################################
set isis_router_status [::ixia::emulation_isis_config     \
        -mode                           create          \
        -reset                                          \
        -port_handle                    $port_handle2   \
        -intf_ip_addr                   22.1.1.1        \
        -gateway_ip_addr                22.1.1.2        \
        -intf_ip_prefix_length          24              \
        -mac_address_init               0000.0000.0002  \
        -count                          1               \
        -wide_metrics                   1               \
        -discard_lsp                    1               \
        -attach_bit                     1               \
        -partition_repair               1               \
        -overloaded                     1               \
        -lsp_refresh_interval           888             \
        -lsp_life_time                  777             \
        -max_packet_size                1492            \
        -intf_metric                    0               \
        -routing_level                  L1L2            \
        -te_enable                      1               \
        -te_max_bw                      10              \
        -te_max_resv_bw                 20              \
        -te_unresv_bw_priority0         10              \
        -te_unresv_bw_priority2         20              \
        -te_unresv_bw_priority3         30              \
        -te_unresv_bw_priority4         40              \
        -te_unresv_bw_priority5         50              \
        -te_unresv_bw_priority6         60              \
        -te_unresv_bw_priority7         70              \
        -te_metric                      10              \
        ]
if {[keylget isis_router_status status] != $::SUCCESS} {
    return "FAIL - [keylget isis_router_status log]"
}

set router_handle2 [keylget isis_router_status handle]

######################################################
# Add a stub route range for the second IS-IS router #
######################################################
set route_config_status [::ixia::emulation_isis_topology_route_config \
        -mode                   create                              \
        -handle                 $router_handle2                     \
        -type                   stub                                \
        -ip_version             4                                   \
        -stub_ip_start          55.0.0.3                            \
        -stub_ip_pfx_len        14                                  \
        -stub_count             3                                   \
        -stub_metric            20                                  \
        -stub_up_down_bit       1                                   \
        ]
if {[keylget route_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget route_config_status log]"
}

######################################
# Start the IS-IS protocol emulation #
######################################
set isis_emulation_status [::ixia::emulation_isis_control \
        -port_handle $port_handle1                      \
        -mode        start                              ]
if {[keylget isis_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_emulation_status log]"
}

set isis_emulation_status [::ixia::emulation_isis_control \
        -port_handle $port_handle2                      \
        -mode        start                              ]
if {[keylget isis_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_emulation_status log]"
}

######################################
# Gather statistics IS-IS statistics #
######################################
after 25000
set isis_routers_info [::ixia::emulation_isis_info    \
        -handle $router_handle1                     \
        -mode   stats                               \
        ]
if {[keylget isis_routers_info status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_routers_info log]"
}
set isis_stats [list                                \
        "L1 Sessions Configured"                    \
                 l1_sessions_configured             \
        "L1 Sessions Up"                            \
                 l1_sessions_up                     \
        "Number of Full L1 Neighbors"               \
                 full_l1_neighbors                  \
        "L2 Sessions Configured"                    \
                 l2_sessions_configured             \
        "L2 Sessions Up"                            \
                 l2_sessions_up                     \
        "Number of Full L2 Neighbors"               \
                 full_l2_neighbors                  \
        ]
		
		
set isis_stats_aggregated [list                     \
		"Aggregated L1 Hellos Tx"                   \
                 aggregated_l1_hellos_tx            \
        "Aggregated L1 Point-to-Point Hellos Tx"    \
                 aggregated_l1_p2p_hellos_tx        \
        "Aggregated L1 LSP Tx"                      \
                 aggregated_l1_lsp_tx               \
        "Aggregated L1 CSNP Tx"                     \
                 aggregated_l1_csnp_tx              \
        "Aggregated L1 PSNP Tx"                     \
                 aggregated_l1_psnp_tx              \
        "Aggregated L1 Database Size"               \
                 aggregated_l1_db_size              \
        "Aggregated L2 Hellos Tx"                   \
                 aggregated_l2_hellos_tx            \
        "Aggregated L2 Point-to-Point Hellos Tx"    \
                 aggregated_l2_p2p_hellos_tx        \
        "Aggregated L2 LSP Tx"                      \
                 aggregated_l2_lsp_tx               \
        "Aggregated L2 CSNP Tx"                     \
                 aggregated_l2_csnp_tx              \
        "Aggregated L2 PSNP Tx"                     \
                 aggregated_l2_psnp_tx              \
        "Aggregated L2 Database Size"               \
                 aggregated_l2_db_size              \
        "Aggregated L1 Hellos Rx"                   \
                 aggregated_l1_hellos_rx            \
        "Aggregated L1 Point-to-Point Hellos Rx"    \
                 aggregated_l1_p2p_hellos_rx        \
        "Aggregated L1 LSP Rx"                      \
                 aggregated_l1_lsp_rx               \
        "Aggregated L1 CSNP Rx"                     \
                 aggregated_l1_csnp_rx              \
        "Aggregated L1 PSNP Rx"                     \
                 aggregated_l1_psnp_rx              \
        "Aggregated L2 Hellos Rx"                   \
                 aggregated_l2_hellos_rx            \
        "Aggregated L2 Point-to-Point Hellos Rx"    \
                 aggregated_l2_p2p_hellos_rx        \
        "Aggregated L2 LSP Rx"                      \
                 aggregated_l2_lsp_rx               \
        "Aggregated L2 CSNP Rx"                     \
                 aggregated_l2_csnp_rx              \
        "Aggregated L2 PSNP Rx"                     \
                 aggregated_l2_psnp_rx              \
        "Aggregated L1 Init Count"                  \
                 aggregated_l1_init_count           \
        "Aggregated L1 Full Count"                  \
                 aggregated_l1_full_count           \
        "Aggregated L2 Init Count"                  \
                 aggregated_l2_init_count           \
        "Aggregated L2 Full Count"                  \
                 aggregated_l2_full_count           \
        ]
puts "First router:"
foreach {name key} $isis_stats {
    puts "\t$name: [keylget isis_routers_info $port_handle1.$key]"
}

if {[keylget connect_status connection {}]} {
	foreach {name key} $isis_stats_aggregated {
		puts "\t$name: [keylget isis_routers_info $port_handle1.$key]"
	}
}

set isis_routers_info [::ixia::emulation_isis_info    \
        -handle $router_handle2                     \
        -mode   stats                               \
        ]
if {[keylget isis_routers_info status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget isis_routers_info log]"
}

puts "Second router:"
foreach {name key} $isis_stats {
    puts "\t$name: [keylget isis_routers_info $port_handle2.$key]"
}

if {[keylget connect_status connection {}]} {
	foreach {name key} $isis_stats_aggregated {
		puts "\t$name: [keylget isis_routers_info $port_handle2.$key]"
	}
}


return "SUCCESS - $test_name - [clock format [clock seconds]]"
