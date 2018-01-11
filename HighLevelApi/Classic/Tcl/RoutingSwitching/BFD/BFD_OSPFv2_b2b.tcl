################################################################################
# Version 1.0    $Revision: 3 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-20-2007 LRaicea - created sample
#    10-16-2007 MVasile - updated the session status checking
#    11-28-2007 LRaicea - updated statistics retrieval
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
#    This sample creates BFD and OSPF emulation on two Ixia ports connected to #
#    each other.                                                               #
#    One BFD router is created on each port.                                   #
#    Each BFD router will have 1 router interfaces.                            #
#    The BFD router interface will be configured as a GRE tunnel.              #
#    For each BFD router interface we add one IPv4 BFD session.                #
#    2 OSPF routers are created on each port.                                  #
#    The protocols are started and statistics are being retrieved.             #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET27.                                      #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 2/1 2/2]

set intf_connected_0 20.0.0.1
set intf_connected_1 20.0.0.2

set loop_count       2
set intf_loop_0      5.0.0.1
set intf_loop_step_0 0.0.1.0
set intf_loop_1      7.0.0.1
set intf_loop_step_1 0.0.1.0

set gre_count        1
set intf_gre_0       2.0.0.1
set intf_gre_step_0  0.0.1.0
set intf_gre_1       3.0.0.1
set intf_gre_step_1  0.0.1.0

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                            \
        -reset                                                                 \
        -ixnetwork_tcl_server           localhost                              \
        -device                         $chassisIP                             \
        -port_list                      $port_list                             \
        -username                       ixiaApiUser                            \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
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

puts "Ixia port handles are: $port_0, $port_1 ... \n\n"
update idletasks

################################################################################
# Configure interface in the test
################################################################################
set interface_status [::ixia::interface_config                                 \
        -port_handle                    [list $port_0 $port_1]                 \
        -intf_mode                      ethernet                               \
        -autonegotiation                1                                      \
        -speed                          auto                                   \
        -duplex                         auto                                   \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

puts "Ixia port configuration returned: [keylget interface_status status] ...\n\n"
update idletasks
################################################################################
# Configure BFD routers
################################################################################
# Connected IP    Loopback IP   GRE IP      GRE DST
#                 = GRE SRC
# -------------------------------------------------
# 20.0.0.1        5.0.0.1       2.0.0.1     7.0.0.1
#                 5.0.1.1       2.0.4.1     7.0.1.1
set bfd_router_status [::ixia::emulation_bfd_config                            \
        -mode                           create                                 \
        -reset                                                                 \
        -port_handle                    $port_0                                \
        -mac_address_init               0ab0.0026.0001                         \
        -count                          1                                      \
        -intf_count                     1                                      \
        -intf_ip_addr                   $intf_connected_0                      \
        -intf_ip_prefix_length          24                                     \
        -intf_gw_ip_addr                $intf_connected_1                      \
        -router_id                      $intf_connected_0                      \
        -loopback_count                 $loop_count                            \
        -loopback_ip_addr               $intf_loop_0                           \
        -loopback_ip_addr_step          $intf_loop_step_0                      \
        -loopback_ip_prefix_length      24                                     \
        -gre_count                      $gre_count                             \
        -gre_ip_addr                    $intf_gre_0                            \
        -gre_ip_addr_step               $intf_gre_step_0                       \
        -gre_ip_prefix_length           24                                     \
        -gre_dst_ip_addr                $intf_loop_1                           \
        -gre_dst_ip_addr_step           0.0.0.0                                \
        -gre_dst_ip_addr_lstep          $intf_loop_step_1                      \
        -gre_dst_ip_addr_cstep          0.0.0.0                                \
        -gre_src_ip_addr_mode           routed                                 \
        ]
if {[keylget bfd_router_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bfd_router_status log]"
    return
}
set bfd_router_0     [keylget bfd_router_status router_handles]
set gre_interfaces_0 [keylget bfd_router_status interface_handles.${bfd_router_0}]

################################################################################
# Connected IP    Loopback IP   GRE IP      GRE DST
#                 = GRE SRC
# -------------------------------------------------
# 20.0.0.2        7.0.0.1       3.0.0.1     5.0.0.1
#                 7.0.1.1       3.0.4.1     5.0.1.1
set bfd_router_status [::ixia::emulation_bfd_config                            \
        -mode                           create                                 \
        -reset                                                                 \
        -port_handle                    $port_1                                \
        -mac_address_init               0ab0.0026.0002                         \
        -count                          1                                      \
        -intf_count                     1                                      \
        -intf_ip_addr                   $intf_connected_1                      \
        -intf_ip_prefix_length          24                                     \
        -intf_gw_ip_addr                $intf_connected_0                      \
        -router_id                      $intf_connected_1                      \
        -loopback_count                 $loop_count                            \
        -loopback_ip_addr               $intf_loop_1                           \
        -loopback_ip_addr_step          $intf_loop_step_1                      \
        -loopback_ip_prefix_length      24                                     \
        -gre_count                      $gre_count                             \
        -gre_ip_addr                    $intf_gre_1                            \
        -gre_ip_addr_step               $intf_gre_step_1                       \
        -gre_ip_prefix_length           24                                     \
        -gre_dst_ip_addr                $intf_loop_0                           \
        -gre_dst_ip_addr_step           0.0.0.0                                \
        -gre_dst_ip_addr_lstep          $intf_loop_step_0                      \
        -gre_dst_ip_addr_cstep          0.0.0.0                                \
        -gre_src_ip_addr_mode           routed                                 \
        ]
if {[keylget bfd_router_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bfd_router_status log]"
    return
}
set bfd_router_1     [keylget bfd_router_status router_handles]
set gre_interfaces_1 [keylget bfd_router_status interface_handles.${bfd_router_1}]

puts "Ixia BFD routers are: $bfd_router_0, $bfd_router_1 ... \n\n"
update idletasks

################################################################################
# Configure BFD sessions
################################################################################
set bfd_session_status [::ixia::emulation_bfd_session_config                   \
        -mode                           create                                 \
        -handle                         $bfd_router_0                          \
        -count                          1                                      \
        -ip_version                     4                                      \
        -enable_auto_choose_source      1                                      \
        -local_disc                     3                                      \
        -enable_learned_remote_disc     1                                      \
        -remote_ip_addr                 $intf_gre_1                            \
        -remote_ip_addr_step            $intf_gre_step_1                       \
        -session_type                   single_hop                             \
        ]
if {[keylget bfd_session_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bfd_session_status log]"
    return
}
set bfd_sessions_0 [keylget bfd_session_status session_handles]

set bfd_session_status [::ixia::emulation_bfd_session_config                   \
        -mode                           create                                 \
        -handle                         $bfd_router_1                          \
        -count                          1                                      \
        -ip_version                     4                                      \
        -enable_auto_choose_source      1                                      \
        -local_disc                     3                                      \
        -enable_learned_remote_disc     1                                      \
        -remote_ip_addr                 $intf_gre_0                            \
        -remote_ip_addr_step            $intf_gre_step_0                       \
        -session_type                   single_hop                             \
        ]
if {[keylget bfd_session_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bfd_session_status log]"
    return
}
set bfd_sessions_1 [keylget bfd_session_status session_handles]

puts "Ixia BFD IPv4 sessions are: ${bfd_sessions_0}, ${bfd_sessions_1} ... \n\n"
update idletasks

################################################################################
# Create OSPF routers
################################################################################
set ospf_neighbor_status [::ixia::emulation_ospf_config                        \
        -mode                           create                                 \
        -reset                                                                 \
        -port_handle                    $port_0                                \
        -session_type                   ospfv2                                 \
        -count                          [expr $loop_count * $gre_count]        \
        -interface_handle               $gre_interfaces_0                      \
        -router_id                      $intf_gre_0                            \
        -router_id_step                 $intf_gre_step_0                       \
        -network_type                   ptop                                   \
        -bfd_registration               1                                      \
        ]
if {[keylget ospf_neighbor_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospf_neighbor_status log]"
    return
}
set ospf_neighbor_0 [keylget ospf_neighbor_status handle]

set ospf_neighbor_status [::ixia::emulation_ospf_config                        \
        -mode                           create                                 \
        -reset                                                                 \
        -port_handle                    $port_1                                \
        -session_type                   ospfv2                                 \
        -count                          [expr $loop_count * $gre_count]        \
        -interface_handle               $gre_interfaces_1                      \
        -router_id                      $intf_gre_1                            \
        -router_id_step                 $intf_gre_step_1                       \
        -network_type                   ptop                                   \
        -bfd_registration               1                                      \
        ]
if {[keylget ospf_neighbor_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospf_neighbor_status log]"
    return
}
set ospf_neighbor_1 [keylget ospf_neighbor_status handle]

puts "Ixia OSPF neighbors are: $ospf_neighbor_0, $ospf_neighbor_1 ... \n\n"
update idletasks

################################################################################
# Start protocols
################################################################################
set ospf_emulation_status [::ixia::emulation_ospf_control                      \
        -port_handle                    [list $port_0 $port_1]                 \
        -mode                           start                                  \
        ]
if {[keylget ospf_emulation_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ospf_emulation_status log]"
    return
}

puts "Started OSPF protocol ... \n\n"
update idletasks

after 5000

set bfd_emulation_status [::ixia::emulation_bfd_control                        \
        -port_handle                    [list $port_0 $port_1]                 \
        -mode                           start                                  \
        ]
if {[keylget bfd_emulation_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bfd_emulation_status log]"
    return
}

puts "Started BFD protocol ... \n\n"
update idletasks

################################################################################
# Retrieve learned BFD information
################################################################################
# There are ($gre_count * $loop_count) interfaces per router, each BFD interface
# has one session configured
set sessions_configured     [expr 2 * $gre_count * $loop_count]
# There are ($gre_count * $loop_count) interfaces per router, each BFD interface
# has one session configured and for each session connected through the same 
# loopback there are ($gre_count - 1) sessions auto configured
set sessions_autoconfigured [expr 2 * ($gre_count * $loop_count) * ($gre_count - 1)]
set sessions_all            [expr $sessions_autoconfigured + $sessions_configured]
set retries                 20
set sessions_learned        0
set sessions_up             0
set learned_sessions_0      ""
set learned_sessions_1      ""
while {($sessions_up < $sessions_all) && ($retries > 0)} {
    set sessions_learned        0
    set sessions_up             0
    set learned_sessions_0      ""
    set learned_sessions_1      ""
    set bfd_emulation_status [::ixia::emulation_bfd_info                       \
            -port_handle                    [list $port_0 $port_1]             \
            -mode                           learned_info                       \
            ]
    if {[keylget bfd_emulation_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget bfd_emulation_status log]"
        return
    }
    puts "Retrieving learned BFD information, number of retries left:\
            [expr $retries - 1] ..."
    update idletasks
    if {![catch {set learned_sessions_0 [keylkeys bfd_emulation_status \
            ${port_0}.${bfd_router_0}.session]}]} {
        incr sessions_learned [llength $learned_sessions_0]
        foreach session $learned_sessions_0 {
            if {![catch {set session_state [keylget bfd_emulation_status \
                    ${port_0}.${bfd_router_0}.session.${session}.session_state]}] && \
                    $session_state == "UP"} {
                incr sessions_up
            }
        }
    }
    if {![catch {set learned_sessions_1 [keylkeys bfd_emulation_status \
            ${port_1}.${bfd_router_1}.session]}]} {
        incr sessions_learned [llength $learned_sessions_1]
        foreach session $learned_sessions_1 {
            if {![catch {set session_state [keylget bfd_emulation_status \
                    ${port_1}.${bfd_router_1}.session.${session}.session_state]}] && \
                    $session_state == "UP"} {
                incr sessions_up
            }
        }
    }
    incr retries -1
    if {$sessions_up < $sessions_all} {
        after 1000
    }
}
if {$sessions_learned == 0} {
    puts "FAIL - $test_name - There are no BFD sessions learned."
    return
}
################################################################################
# Print learned BFD information
################################################################################
set stats_list {
    "Desired Min. Transmit Interval"   desired_min_tx_interval
    "Local Discriminator"              local_disc
    "Local IP Address"                 local_ip_addr
    "Remote Discriminator"             remote_disc
    "Remote Flags"                     remote_flags
    "Remote IP Address"                remote_ip_addr
    "Remote Router State"              remote_state
    "Remote Router Up Time"            remote_up_time
    "Protocol Using Session"           protocol_using_session
    "Required Min. Echo Interval"      req_min_echo_interval
    "Required Min. Receive Interval"   req_min_rx_interval
    "Session State"                    session_state
    "Session Type"                     session_type
}
foreach {session_key} $learned_sessions_0 {
    puts [string repeat "-" 80]
    puts "BFD - Port $port_0, Router $bfd_router_0, Session ${session_key}"
    puts [string repeat "-" 80]
    foreach {stat_output stat_name} $stats_list {
        puts "[format %-35s $stat_output] [keylget bfd_emulation_status \
                ${port_0}.${bfd_router_0}.session.${session_key}.${stat_name}]"
    }
}

foreach {session_key} $learned_sessions_1 {
    puts [string repeat "-" 80]
    puts "BFD - Port $port_1, Router $bfd_router_1, Session ${session_key}"
    puts [string repeat "-" 80]
    foreach {stat_output stat_name} $stats_list {
        puts "[format %-35s $stat_output] [keylget bfd_emulation_status \
                ${port_1}.${bfd_router_1}.session.${session_key}.${stat_name}]"
    }
}

set bfd_emulation_status [::ixia::emulation_bfd_info                           \
        -port_handle                    [list $port_0 $port_1]                 \
        -mode                           aggregate_stats                        \
        ]
if {[keylget bfd_emulation_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget bfd_emulation_status log]"
    return
}

foreach port [list $port_0 $port_1] {
    puts [string repeat "-" 50]
    puts "BFD - Port $port"
    puts [string repeat "-" 50]
    foreach {stat_name} [keylkeys bfd_emulation_status \
            ${port}.aggregate] {
        puts "[format %-35s [string totitle [split $stat_name _]]]\
                [keylget bfd_emulation_status ${port}.aggregate.${stat_name}]"
    }
}

if {$sessions_up < $sessions_all} {
    puts "FAIL - $test_name - Only $sessions_up out of the\
            $sessions_all BFD sessions(configured and autoconfigured) are up."
    return
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return
