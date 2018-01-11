################################################################################
# Version 1.0    $Revision: 1 $
# $Author: MHasegan $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    11-23-2008 Mircea Hasegan
#
# Description:
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
#    This sample RSVP P2MP Back2Back. Statistics are collected.                #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a STXS4 module.                                  #
#                                                                              #
################################################################################



package require Ixia

set test_name               [info script]

################################################################################
# START - Connect to the chassis
################################################################################
set chassis_ip              sylvester
set port_list               [list 2/3 2/4]

# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                        \
        -reset                                                             \
        -device               $chassis_ip                                  \
        -port_list            $port_list                                   \
        -break_locks          1                                            \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}

set i 0
puts "Ixia port handles are:"
foreach port $port_handle {
    set port_$i $port
    puts $port
    incr i
}

################################################################################
# END - Connect to the chassis
################################################################################

set interface_status [::ixia::interface_config                             \
        -port_handle      $port_0                                          \
        -mode             config                                           \
        -intf_mode        ethernet                                         \
        -autonegotiation  1                                                \
        -speed            ether100                                         \
        -duplex           auto                                             \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set interface_status [::ixia::interface_config                             \
        -port_handle      $port_1                                          \
        -mode             config                                           \
        -intf_mode        ethernet                                         \
        -autonegotiation  1                                                \
        -speed            ether100                                         \
        -duplex           auto                                             \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# START - RSVP configuration
################################################################################
puts "\nRSVP configuration $port_0 - Ingress..."

################################################################################
# RSVP Call - port_0 - Ingress
################################################################################

set rsvp_config_status [::ixia::emulation_rsvp_config  \
        -mode                            create        \
        -count                           1             \
        -intf_ip_addr                    1.1.1.1       \
        -intf_prefix_length              24            \
        -ip_version                      4             \
        -neighbor_intf_ip_addr           1.1.1.2       \
        -port_handle                     $port_0       \
        -reset                                         \
    ]
if {[keylget rsvp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_config_status log]"
}

set rsvpHandleList_ingress [keylget rsvp_config_status handles]


################################################################################
# RSVP configuration $port_1 - Egress
################################################################################
puts "\nRSVP configuration $port_1 - Egress..."

set rsvp_config_status [::ixia::emulation_rsvp_config                           \
        -mode                            create        \
        -count                           1             \
        -intf_ip_addr                    1.1.1.2       \
        -intf_prefix_length              24            \
        -ip_version                      4             \
        -neighbor_intf_ip_addr           1.1.1.1       \
        -port_handle                     $port_1       \
        -reset                                         \
    ]
if {[keylget rsvp_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_config_status log]"
}

set rsvpHandleList_egress [keylget rsvp_config_status handles]

################################################################################
# RSVP Tunnel configuration - Ingress
################################################################################
puts "\nRSVP Tunnel configuration - Ingress"

set rsvp_tunnel_config_status [::ixia::emulation_rsvp_tunnel_config        \
        -count                                    1                        \
        -emulation_type                           rsvptep2mp               \
        -handle                                   $rsvpHandleList_ingress  \
        -mode                                     create                   \
        -port_handle                              $port_0                  \
        -rsvp_behavior                            rsvpIngress              \
        -egress_ip_addr                           5.5.5.1                  \
        -egress_ip_step                           0.0.1.0                  \
        -egress_leaf_ip_count                     5                        \
        -egress_leaf_range_count                  3                        \
        -egress_leaf_range_step                   0.0.1.0                  \
        -p2mp_id                                  1                        \
        -ingress_ip_addr                          4.4.4.4                  \
        -lsp_id_start                             0                        \
        -tunnel_id_start                          1                        \
        -head_traffic_start_ip                    100.100.100.100          \
        -tail_traffic_start_ip                    224.0.0.20               \
    ]

if {[keylget rsvp_tunnel_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_tunnel_config_status log]"
}

set rsvp_ingress_handle [keylget rsvp_tunnel_config_status tunnel_handle]


################################################################################
# RSVP Tunnel configuration - Egress
################################################################################
puts "\nRSVP Tunnel configuration - Egress"

set rsvp_tunnel_config_status [::ixia::emulation_rsvp_tunnel_config      \
        -count                                    1                      \
        -emulation_type                           rsvptep2mp             \
        -handle                                   $rsvpHandleList_egress \
        -mode                                     create                 \
        -port_handle                              $port_1                \
        -rsvp_behavior                            rsvpEgress             \
        -egress_ip_addr                           5.5.5.1                \
        -egress_ip_step                           0.0.1.0                \
        -egress_leaf_ip_count                     5                      \
        -egress_leaf_range_count                  3                      \
        -egress_leaf_range_step                   0.0.1.0                \
        -p2mp_id                                  1                      \
        -tail_traffic_start_ip                    224.0.0.20             \
    ]
if {[keylget rsvp_tunnel_config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_tunnel_config_status log]"
}

set rsvpTunnelHandleList [keylget rsvp_tunnel_config_status tunnel_handle]
set rsvp_egress_handle $rsvpTunnelHandleList


################################################################################
# Start - RSVP emulation - Egress
################################################################################
puts "\nStart - RSVP emulation - Egress"
set rsvp_control_status [::ixia::emulation_rsvp_control\
        -mode           start                    \
        -handle         $rsvp_egress_handle      \
        ]

if {[keylget rsvp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_control_status log]"
}


################################################################################
# Start - RSVP emulation - Ingress
################################################################################
puts "\nStart - RSVP emulation - Ingress"
set rsvp_control_status [::ixia::emulation_rsvp_control\
        -mode           start                    \
        -handle         $rsvp_ingress_handle     \
        ]

if {[keylget rsvp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_control_status log]"
}

################################################################################
# RSVP info - Ingress - mode stats
################################################################################
# Wait for stats to accumulate
after 10000

puts "\nRSVP info - Ingress - mode stats"
set rsvp_info_status [::ixia::emulation_rsvp_info \
        -mode        stats                        \
        -port_handle $port_0                      \
    ]
if {[keylget rsvp_info_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_info_status log]"
}

puts "\nPort - $port_0"
foreach stat [keylkeys rsvp_info_status] {
    if {$stat == "status"} {
        continue
    }
    puts [format {%-10s%-40s%s} "" $stat [keylget rsvp_info_status $stat]]
}


if {[keylget rsvp_info_status ingress_lsp_up_count] != 1} {
    return "FAIL - $test_name - Not all lsps configured. Requested 1; Actual \
            [keylget rsvp_info_status ingress_lsp_up_count]"
}

if {[keylget rsvp_info_status ingress_sub_lsp_configured_count] != 15} {
    return "FAIL - $test_name - Not all sub lsps configured. Requested 15; Actual \
            [keylget rsvp_info_status ingress_sub_lsp_configured_count]"
}

################################################################################
# RSVP info - Egress - mode stats
################################################################################
puts "\nRSVP info - Egress - mode stats"
set rsvp_info_status [::ixia::emulation_rsvp_info                               \
        -mode        stats                                                      \
        -port_handle $port_1                                                    \
    ]
if {[keylget rsvp_info_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_info_status log]"
}


puts "\nPort - $port_1"
foreach stat [keylkeys rsvp_info_status] {
    if {$stat == "status"} {
        continue
    }
    puts [format {%-10s%-40s%s} "" $stat [keylget rsvp_info_status $stat]]
}


if {[keylget rsvp_info_status lsp_count] != 1} {
    return "FAIL - $test_name - Not all lsps configured. Requested 1; Actual \
            [keylget rsvp_info_status num_lsp_setup]"
}

if {[keylget rsvp_info_status egress_sub_lsp_up_count] != 15} {
    return "FAIL - $test_name - Not all sub lsps configured. Requested 15; Actual \
            [keylget rsvp_info_status egress_sub_lsp_up_count]"
}

################################################################################
# RSVP info - Ingress - mode settings
################################################################################

puts "\nRSVP info - Ingress - mode settings"
set rsvp_info_status [::ixia::emulation_rsvp_info                               \
        -mode        settings                                                   \
        -port_handle $port_0                                                    \
    ]
if {[keylget rsvp_info_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_info_status log]"
}

puts "\nPort - $port_0"
foreach stat [keylkeys rsvp_info_status] {
    if {$stat == "status"} {
        continue
    }
    puts [format {%-10s%-40s%s} "" $stat [keylget rsvp_info_status $stat]]
}


if {[keylget rsvp_info_status intf_ip_addr] != "1.1.1.1"} {
    return "FAIL - $test_name - Settings not configured. Requested 1.1.1.1; Actual \
            [keylget rsvp_info_status intf_ip_addr]"
}

if {[keylget rsvp_info_status neighbor_intf_ip_addr] != "1.1.1.2"} {
    return "FAIL - $test_name - Settings not configured. Requested 1.1.1.2; Actual \
            [keylget rsvp_info_status neighbor_intf_ip_addr]"
}


################################################################################
# RSVP info - Egress - mode settings
################################################################################

puts "\nRSVP info - Egress - mode settings"
set rsvp_info_status [::ixia::emulation_rsvp_info                               \
        -mode        settings                                                   \
        -port_handle $port_1                                                    \
    ]
if {[keylget rsvp_info_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_info_status log]"
}

puts "\nPort - $port_1"
foreach stat [keylkeys rsvp_info_status] {
    if {$stat == "status"} {
        continue
    }
    puts [format {%-10s%-40s%s} "" $stat [keylget rsvp_info_status $stat]]
}


if {[keylget rsvp_info_status intf_ip_addr] != "1.1.1.2"} {
    return "FAIL - $test_name - Settings not configured. Requested 1.1.1.2; Actual \
            [keylget rsvp_info_status intf_ip_addr]"
}

if {[keylget rsvp_info_status neighbor_intf_ip_addr] != "1.1.1.1"} {
    return "FAIL - $test_name - Settings not configured. Requested 1.1.1.1; Actual \
            [keylget rsvp_info_status neighbor_intf_ip_addr]"
}

################################################################################
# RSVP info - Ingress - mode neighbors
################################################################################

puts "\nRSVP info - Ingress - mode neighbors"
set rsvp_info_status [::ixia::emulation_rsvp_info                               \
        -mode        neighbors                                                  \
        -port_handle $port_0                                                    \
    ]
if {[keylget rsvp_info_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_info_status log]"
}

puts "\nPort - $port_0"
foreach neighbor [keylget rsvp_info_status neighbors] {
    puts "\t$neighbor"
}


if {[llength [keylget rsvp_info_status neighbors]] != 15} {
    return "FAIL - $test_name - Not all tunnels were established. Expected: 15; \
        Actual [llength [keylget rsvp_info_status neighbors]]"
}

################################################################################
# RSVP info - Egress - mode neighbors
################################################################################

puts "\nRSVP info - Egress - mode neighbors"
set rsvp_info_status [::ixia::emulation_rsvp_info                               \
        -mode        neighbors                                                  \
        -port_handle $port_1                                                    \
    ]
if {[keylget rsvp_info_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_info_status log]"
}

puts "\nPort - $port_1"
foreach neighbor [keylget rsvp_info_status neighbors] {
    puts "\t$neighbor"
}


if {[llength [keylget rsvp_info_status neighbors]] != 15} {
    return "FAIL - $test_name - Not all tunnels were established. Expected: 15; \
        Actual [llength [keylget rsvp_info_status neighbors]]"
}

################################################################################
# RSVP info - Ingress - mode labels
################################################################################

puts "\nRSVP info - Ingress - mode labels"
set rsvp_info_status [::ixia::emulation_rsvp_info                               \
        -mode        labels                                                  \
        -port_handle $port_0                                                    \
    ]
if {[keylget rsvp_info_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_info_status log]"
}

puts "\nPort - $port_0"
foreach tunnel [keylkeys rsvp_info_status labels] {
    puts "\tTunnel $tunnel - label [keylget rsvp_info_status labels.$tunnel]"
}


################################################################################
# RSVP info - Egress - mode labels
################################################################################

puts "\nRSVP info - Egress - mode labels"
set rsvp_info_status [::ixia::emulation_rsvp_info                               \
        -mode        labels                                                  \
        -port_handle $port_1                                                    \
    ]
if {[keylget rsvp_info_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_info_status log]"
}

puts "\nPort - $port_1"
foreach tunnel [keylkeys rsvp_info_status labels] {
    puts "\tTunnel $tunnel - label [keylget rsvp_info_status labels.$tunnel]"
}

################################################################################
# Stop - RSVP emulation - Ingress
################################################################################
puts "\nStop - RSVP emulation - Ingress"
set rsvp_control_status [::ixia::emulation_rsvp_control\
        -mode           stop                    \
        -handle         $rsvp_ingress_handle     \
        ]

if {[keylget rsvp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_control_status log]"
}


################################################################################
# Stop - RSVP emulation - Egress
################################################################################
puts "\nStop - RSVP emulation - Egress"
set rsvp_control_status [::ixia::emulation_rsvp_control\
        -mode           stop                    \
        -handle         $rsvp_egress_handle      \
        ]

if {[keylget rsvp_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget rsvp_control_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
