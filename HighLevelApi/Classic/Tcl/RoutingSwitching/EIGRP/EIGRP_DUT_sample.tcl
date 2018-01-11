################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10-16-2007 LRaicea - created sample
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
# DUT configuration:
#
# conf t
# !
# ip subnet-zero
# !
# ip cef
# !
# interface GigabitEthernet0/3
#  no ip address
#  no shutdown
# !
# interface GigabitEthernet0/3.25
#  encapsulation dot1Q 25
#  ip address 25.0.0.1 255.255.255.0
# !
# interface GigabitEthernet0/3.26
#  encapsulation dot1Q 26
#  ip address 26.0.0.1 255.255.255.0
# !
# interface GigabitEthernet0/3.27
#  encapsulation dot1Q 27
#  ip address 27.0.0.1 255.255.255.0
# !
# interface Loopback35
#  ip address 35.0.0.1 255.255.255.0
# !
# interface Loopback36
#  ip address 36.0.0.1 255.255.255.0
# !
# interface Loopback37
#  ip address 37.0.0.1 255.255.255.0
# !
# interface Loopback45
#  ip address 45.0.0.1 255.255.255.0
# !
# interface Loopback46
#  ip address 46.0.0.1 255.255.255.0
# !
# interface Loopback47
#  ip address 47.0.0.1 255.255.255.0
# !
# router eigrp 25
#  network 25.0.0.0 0.0.0.255
#  network 35.0.0.0 0.0.0.255
#  network 45.0.0.0 0.0.0.255
#  no auto-summary
# !
# router eigrp 26
#  network 26.0.0.0 0.0.0.255
#  network 36.0.0.0 0.0.0.255
#  network 46.0.0.0 0.0.0.255
#  no auto-summary
# !
# router eigrp 27
#  network 27.0.0.0 0.0.0.255
#  network 37.0.0.0 0.0.0.255
#  network 47.0.0.0 0.0.0.255
#  no auto-summary
# 
# end
#
# Description:                                                                 #
#    This sample creates 3 EIGRP routers with directly connected IPv4          #
#    interfaces.                                                               #
#    For each EIGRP router, it creates 2 EIGRP route ranges, each route        #
#    range having 10 prefixes.                                                 #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET27.                                      #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set start_time [clock clicks -milliseconds]
set totalTime 0

set chassisIP sylvester
set port_list [list 2/4]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_list       \
        -username  ixiaApiUser      ]

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
################################################################################
# Configure interface in the test
################################################################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_0               \
        -autonegotiation 1                     \
        -duplex          auto 	               \
        -speed 	         auto                  ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}
################################################################################
# Configure EIGRP routers
################################################################################
set eigrp_router_status [::ixia::emulation_eigrp_config \
        -mode                           create          \
        -reset             			                    \
        -port_handle                    $port_0         \
        -count      		            3               \
        -intf_ip_addr                   25.0.0.2        \
        -intf_ip_addr_step              1.0.0.0         \
        -intf_ip_prefix_length          24              \
        -intf_gw_ip_addr                25.0.0.1        \
        -intf_gw_ip_addr_step           1.0.0.0         \
        -vlan                           1               \
        -vlan_id                        25              \
        -vlan_id_step                   1               \
        -mac_address_init               0000.0000.0001  \
        -router_id                      25.0.0.2        \
        -router_id_step                 1.0.0.0         \
        -enable_piggyback               1               \
        -bfd_registration               1               \
        -discard_learned_routes         0               \
        -as_number                      25              \
        -as_number_step                 1               \
        ]
if {[keylget eigrp_router_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget eigrp_router_status log]"
    return
}
set eigrp_router_handles [keylget eigrp_router_status router_handles]
################################################################################
# Configure EIGRP routes
################################################################################
set eigrp_router_status [::ixia::emulation_eigrp_route_config \
        -mode                           create                \
        -handle                         $eigrp_router_handles \
        -prefix_start                   50.0.0.1              \
        -count                          2                     \
        -num_prefixes                   10                    \
        ]
if {[keylget eigrp_router_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget eigrp_router_status log]"
    return
}

################################################################################
# Start EIGRP protocol
################################################################################
set eigrp_control_status [ixia::emulation_eigrp_control   \
        -port_handle   $port_0                            \
        -mode          start                              ]
if {[keylget eigrp_control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget eigrp_control_status log]"
    return
}

after 20000
################################################################################
# Retrieve learned EIGRP information
################################################################################
set num_learned_routes 6
set learned_routes     0
set retries            10
while {($learned_routes < $num_learned_routes) && ($retries >= 0)} {
    set eigrp_learned_status [ixia::emulation_eigrp_info \
            -port_handle $port_0                         \
            -mode        learned_info                    ]

    if {[keylget eigrp_learned_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget eigrp_learned_status log]"
        return
    }
    puts "Retrieving learned EIGRP information, number of retries left: $retries ..."
    update idletasks
    foreach {eigrp_router_handle} $eigrp_router_handles {
        if {![catch {set port_learned_routes [keylkeys eigrp_learned_status \
                ${port_0}.${eigrp_router_handle}.route]}]} {
            incr learned_routes [llength $port_learned_routes]
        }
    }
    incr retries -1
    
    if {$learned_routes < $num_learned_routes} {
        after 1000
        set learned_routes 0
    }
}
if {$learned_routes < $num_learned_routes} {
    puts "FAIL - $test_name - Not all EIGRP routes have been learned."
    return
}
################################################################################
# Print learned EIGRP information
################################################################################
set stats_list {
    "Route Prefix"        prefix
    "Route Prefix Length" prefix_length
    "Route Type"          type
    "Feasible Distance"   FD
    "Neighbor Router"     neighbor
    "Reported Distance"   RD
    "Hop Count"           hop_count
    "Next Hop"            next_hop
}
foreach {eigrp_router_handle} $eigrp_router_handles {
    set port_learned_routes [keylkeys eigrp_learned_status \
                ${port_0}.${eigrp_router_handle}.route]
    foreach {route_key} $port_learned_routes {
        puts [string repeat "-" 80]
        puts "EIGRP - Port $port_0, Router $eigrp_router_handle, Route ${route_key}"
        puts [string repeat "-" 80]
        foreach {stat_output stat_name} $stats_list {
            puts "[format %-35s $stat_output] [keylget eigrp_learned_status \
                    ${port_0}.${eigrp_router_handle}.route.${route_key}.${stat_name}]"
        }
    }
}

################################################################################
# Retrieve EIGRP aggregate information
################################################################################
set routers_running 0
set retries         10
while {($routers_running == 0) && ($retries > 0)} {
    set eigrp_aggregate_status [ixia::emulation_eigrp_info \
        -port_handle $port_0                           \
        -mode        aggregate_stats                   ]

    if {[keylget eigrp_aggregate_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget eigrp_aggregate_status log]"
        return
    }
    set routers_running [keylget eigrp_aggregate_status \
            ${port_0}.aggregate.routers_running]
    incr retries -1
    puts "Retrieving aggregate EIGRP information, number of retries left: $retries ..."
    update idletasks
    if {$routers_running == 0} {
        after 1000
    }
}


puts [string repeat "-" 50]
puts "EIGRP - Port $port_0"
puts [string repeat "-" 50]
foreach {stat_name} [keylkeys eigrp_aggregate_status ${port_0}.aggregate] {
    puts "[format %-35s [string totitle [split $stat_name _]]]\
            [keylget eigrp_aggregate_status ${port_0}.aggregate.${stat_name}]"
}

set total_time [expr [clock clicks -milliseconds] - $start_time]
puts   "SUCCESS - $total_time - $totalTime"
return "SUCCESS - $test_name - Time to complete: $total_time ms"
