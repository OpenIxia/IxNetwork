################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    06-28-2007 LRaicea - created sample
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
#    This sample creates uses 2 Ixia port connected back to back.              #
#    One EIGRP router with directly connected IPv4 interfaces is created on    #
#    each port2.                                                               #
#    Each router has 2 route ranges. Each route range advertises 5 prefixes.   #
#    The protocol is started.                                                  #
#    EIGRP learned information is retrieved.                                   #
#    EIGRP aggregated stats are also retrieved.                                #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET27.                                      #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set start_time [clock clicks -milliseconds]
set totalTime  0

set chassisIP sylvester
set port_list [list 1/1 1/2]

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
set port_1 [lindex $port_handle 1]
################################################################################
# Configure interface in the test
################################################################################
set interface_status [::ixia::interface_config  \
        -port_handle     [list $port_0 $port_1] \
        -autonegotiation 1                      \
        -duplex          auto 	                \
        -speed 	         auto                   ]
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
        -count      		            1               \
        -intf_ip_addr                   25.0.0.1        \
        -intf_ip_prefix_length          24              \
        -intf_gw_ip_addr                25.0.0.2        \
        -router_id                      25.0.0.1        \
        -enable_piggyback               1               \
        -bfd_registration               1               \
        -discard_learned_routes         0               \
        ]
if {[keylget eigrp_router_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget eigrp_router_status log]"
    return
}
set eigrp_router0 [keylget eigrp_router_status router_handles]

set eigrp_router_status [::ixia::emulation_eigrp_config \
        -mode                           create          \
        -reset             			                    \
        -port_handle                    $port_1         \
        -count      		            1               \
        -intf_ip_addr                   25.0.0.2        \
        -intf_ip_prefix_length          24              \
        -intf_gw_ip_addr                25.0.0.1        \
        -router_id                      25.0.0.2        \
        -enable_piggyback               1               \
        -bfd_registration               1               \
        -discard_learned_routes         0               \
        ]
if {[keylget eigrp_router_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget eigrp_router_status log]"
    return
}
set eigrp_router1 [keylget eigrp_router_status router_handles]

################################################################################
# Configure EIGRP routes
################################################################################
set eigrp_route0_status [::ixia::emulation_eigrp_route_config \
        -mode                           create                \
        -handle                         $eigrp_router0        \
        -prefix_start                   50.0.0.1              \
        -count                          2                     \
        -num_prefixes                   5                     \
        ]
if {[keylget eigrp_route0_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget eigrp_route0_status log]"
    return
}

set eigrp_route1_status [::ixia::emulation_eigrp_route_config \
        -mode                           create                \
        -handle                         $eigrp_router1        \
        -prefix_start                   60.0.0.1              \
        -count                          2                     \
        -num_prefixes                   5                     \
        ]
if {[keylget eigrp_route1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget eigrp_route1_status log]"
    return
}

################################################################################
# Start EIGRP protocol
################################################################################
set eigrp_control_status [ixia::emulation_eigrp_control   \
        -port_handle   [list $port_0 $port_1]             \
        -mode          start                              ]
if {[keylget eigrp_control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget eigrp_control_status log]"
    return
}

after 20000
################################################################################
# Retrieve learned EIGRP information
################################################################################
set routes_up       0
set retries         10
set learned_routes0 ""
set learned_routes1 ""
while {($routes_up == 0) && ($retries >= 0)} {
    set eigrp_learned_status [ixia::emulation_eigrp_info \
            -port_handle [list $port_0 $port_1]          \
            -mode        learned_info                    ]

    if {[keylget eigrp_learned_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget eigrp_learned_status log]"
        return
    }
    puts "Retrieving learned EIGRP information, number of retries left: $retries ..."
    update idletasks
    if {![catch {set learned_routes0 [keylkeys eigrp_learned_status \
            ${port_0}.${eigrp_router0}.route]}]} {
        incr routes_up [llength $learned_routes0]
    }
    if {![catch {set learned_routes1 [keylkeys eigrp_learned_status \
            ${port_1}.${eigrp_router1}.route]}]} {
        incr routes_up [llength $learned_routes1]
    }
    incr retries -1
    if {$routes_up == 0} {
        after 1000
    }
}
if {$routes_up == 0} {
    puts "FAIL - $test_name - There are no EIGRP routes UP."
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
foreach {route_key} $learned_routes0 {
    puts [string repeat "-" 80]
    puts "EIGRP - Port $port_0, Router $eigrp_router0, Route ${route_key}"
    puts [string repeat "-" 80]
    foreach {stat_output stat_name} $stats_list {
        puts "[format %-35s $stat_output] [keylget eigrp_learned_status \
                ${port_0}.${eigrp_router0}.route.${route_key}.${stat_name}]"
    }
}

foreach {route_key} $learned_routes1 {
    puts [string repeat "-" 80]
    puts "EIGRP - Port $port_1, Router $eigrp_router1, Route ${route_key}"
    puts [string repeat "-" 80]
    foreach {stat_output stat_name} $stats_list {
        puts "[format %-35s $stat_output] [keylget eigrp_learned_status \
                ${port_1}.${eigrp_router1}.route.${route_key}.${stat_name}]"
    }
}

################################################################################
# Retrieve EIGRP aggregate information
################################################################################
set eigrp_aggregate_status [ixia::emulation_eigrp_info \
        -port_handle [list $port_0 $port_1]            \
        -mode        aggregate_stats                   ]

if {[keylget eigrp_aggregate_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget eigrp_aggregate_status log]"
    return
}

foreach port [list $port_0 $port_1] {
    puts [string repeat "-" 50]
    puts "EIGRP - Port $port"
    puts [string repeat "-" 50]
    foreach {stat_name} [keylkeys eigrp_aggregate_status ${port}.aggregate] {
        puts "[format %-35s [string totitle [split $stat_name _]]]\
                [keylget eigrp_aggregate_status ${port}.aggregate.${stat_name}]"
    }
}

set total_time [expr [clock clicks -milliseconds] - $start_time]
puts   "SUCCESS - $total_time - $totalTime"
return "SUCCESS - $test_name - Time to complete: $total_time ms"
