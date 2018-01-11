################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Karim $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    4-25-2003 Karim
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
#    This sample configures two external BGP neighbors and on each neighbor    #
#    configures two IPv4 route ranges an two IPv6 route ranges.                #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM100TXS8 module.                              #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 127.0.0.1
set port_list [list 10/1]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect \
        -reset                \
        -device    $chassisIP \
        -port_list $port_list \
        -username  ixiaApiUser]

if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [::ixia::get_port_list_from_connect $connect_status $chassisIP \
        $port_list]

########################################
# Configure interface in the test      #
#                                      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle \
        -autonegotiation 1            \
        -duplex          auto         \
        -speed           auto]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

#################################################
#                                               #
#  Configure 2 BGP neighbors on interface 1/10/1 #
#  1) Neighbor #1 - external                    #
#  2) Neighbor #2 - external                    #
#################################################
set bgp_routers_status [::ixia::emulation_bgp_config \
        -mode                   reset          \
        -port_handle            $port_handle   \
        -local_ip_addr          10.1.1.1       \
        -remote_ip_addr         10.1.1.2       \
        -count                  2              \
        -mac_address_start      0000.0000.0001 \
        -netmask                24             \
        -neighbor_type          external       \
        -ip_version             4              \
        -next_hop_enable                       \
        -next_hop_ip            10.10.160.1    \
        -local_as               111            \
        -local_as_mode          fixed          \
        -tcp_window_size        6666           \
        -updates_per_iteration  5              \
        -retries                11             \
        -retry_time             22             \
        -active_connect_enable                 \
        -staggered_start_enable                \
        -staggered_start_time   77             ]

if {[keylget bgp_routers_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_routers_status log]"
}

#########################################################
#                                                       #
#  Configure 2 BGP IPv4 Route Range on each BGP router  #
#  1/10/1                                               #
#                                                        #
#########################################################
#Get the list of BGP router handle form the keye list returned
set bgp_router_handle_list [keylget bgp_routers_status handles]

set bgp_route_ip_addr 22.1.1.1

set bgp_ipv4_route_handle_list ""

foreach bgp_router_handle $bgp_router_handle_list {

    set bgp_ipv4_route_handle [::ixia::emulation_bgp_route_config  \
            -mode                          add                \
            -handle                        $bgp_router_handle \
            -ip_version                    4                  \
            -prefix                        $bgp_route_ip_addr \
            -prefix_from                   24                 \
            -prefix_to                     24                 \
            -num_routes                    1000               \
            -origin                        igp                \
            -enable_generate_unique_routes                    \
            -enable_traditional_nlri       1                  \
            -max_route_ranges              2                  ]

    if {[keylget bgp_ipv4_route_handle status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget bgp_ipv4_route_handle log]"
    }

    # Increment the IPv4 address for the BGP route range
    set bgp_route_ip_addr [::ixia::increment_ipv4_address $bgp_route_ip_addr]

    lappend bgp_ipv4_route_handle_list $bgp_ipv4_route_handle
}

#########################################################
#                                                       #
#  Configure 2 BGP IPv6 Route Range on each BGP router  #
#  1/10/1                                               #
#                                                       #
#########################################################
#Get the list of BGP router handle form the keye list returned
set bgp_router_handle_list [keylget bgp_routers_status handles]

set bgp_route_ip_addr "0030:1::31"

set bgp_ipv4_route_handle_list ""

foreach bgp_router_handle $bgp_router_handle_list {

    set bgp_ipv6_route_handle [::ixia::emulation_bgp_route_config  \
            -mode                                add                \
            -handle                              $bgp_router_handle \
            -ip_version                          6                  \
            -prefix                              $bgp_route_ip_addr \
            -prefix_from                         64                 \
            -prefix_to                           64                 \
            -num_routes                          1000               \
            -enable_route_flap                                      \
            -flap_up_time                        20                 \
            -flap_down_time                      30                 \
            -origin                              igp                \
            -enable_partial_route_flap                              \
            -partial_route_flap_from_route_index 1                  \
            -partial_route_flap_to_route_index   50                 \
            -enable_generate_unique_routes                          \
            -enable_traditional_nlri             1                  \
            -max_route_ranges                    2                  ]

    if {[keylget bgp_ipv6_route_handle status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget bgp_ipv6_route_handle log]"
    }

    # Increment the IPv4 address for the BGP route range
    set bgp_route_ip_addr [::ixia::increment_ipv6_address $bgp_route_ip_addr 1]

    lappend bgp_ipv6_route_handle_list $bgp_ipv6_route_handle
}

######################
# START BGP on       #
######################
set bgp_emulation_status [::ixia::emulation_bgp_control   \
        -port_handle $port_handle \
        -mode        start ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}

# Set up the statistics for bgp once the protocol is running
set handle [lindex $bgp_router_handle_list 0]
set bgp_emulation_status [::ixia::emulation_bgp_control   \
        -handle $handle \
        -mode   statistic ]
if {[keylget bgp_emulation_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget bgp_emulation_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
