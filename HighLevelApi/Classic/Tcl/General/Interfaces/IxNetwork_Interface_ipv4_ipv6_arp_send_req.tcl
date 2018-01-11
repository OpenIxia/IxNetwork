################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Stefan Popi $
#
#    Copyright © 1997 - 2011 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    32-09-2011 Stefan Popi
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
###############################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample configures Dual Stack Protocol Interfaces, and sends arp      #
#    requests for IPv4 interfaces and Router Solicitation for IPv6 interfaces. #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on ... module                                       #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]
set chassisIP 10.205.16.91
set port_list [list 5/7 5/8]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect     \
        -reset                          \
        -device         $chassisIP      \
        -port_list      $port_list      \
        -ixnetwork_tcl_server localhost \
        ]
        
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}

set port_src_handle [lindex $port_handle 0]
set port_dst_handle [lindex $port_handle 1]

puts "Ixia port handles are $port_handle ..."
################################################################################
# Configure Dual Stack Interfaces on both ports                                #
################################################################################

for {set i 1} {$i<10} {incr i} {
    set interface_status [::ixia::interface_config      \
            -port_handle        $port_src_handle        \
            -mode               config                  \
            -speed              ether100                \
            -phy_mode           copper                  \
            -intf_ip_addr       20.0.0.10$i             \
            -gateway            20.0.0.$i               \
            -netmask            255.255.255.0           \
            -autonegotiation    1                       \
            -ipv6_intf_addr     20:0:0:0:0:0:0:$i       \
            -ipv6_gateway       20:0:0:0:0:0:0:10$i     \
            -ipv6_prefix_length 112                     \
            ]
    if {[keylget interface_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget interface_status log]"
    }
}
for {set i 1} {$i<10} {incr i} {
    set interface_status [::ixia::interface_config      \
            -port_handle        $port_dst_handle        \
            -mode               config                  \
            -speed              ether100                \
            -phy_mode           copper                  \
            -intf_ip_addr       20.0.0.$i               \
            -gateway            20.0.0.10$i             \
            -netmask            255.255.255.0           \
            -autonegotiation    1                       \
            -ipv6_intf_addr     20:0:0:0:0:0:0:10$i     \
            -ipv6_gateway       20:0:0:0:0:0:0:$i       \
            -ipv6_prefix_length 112                     \
            ]
    if {[keylget interface_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget interface_status log]"
    }
}
################################################################################
# Send ARP request and Router Solicitations
################################################################################
after 5000
set start [clock seconds]
set start_time [clock clicks -milliseconds]
set interface_status [::ixia::interface_config                      \
        -port_handle     [list $port_src_handle $port_dst_handle]   \
        -send_router_solicitation       [list 1 1]                  \
        -arp_send_req       [list 1 1]                              \
        ]
set stop [clock seconds]
puts "Total time [expr $stop - $start]"
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
after 5000
foreach port $port_handle {
    puts "\nPort $port:"
    if {[keylget interface_status $port.arp_request_success] == 1} {
        puts "\tARP resolved for all interfaces"
    } else {
        if {![catch {keylget interface_status $port.arp_ipv4_interfaces_failed} out]} {
            puts "\tIPv4 Interfaces that failed to resolve ARP: $out"
        }
        if {![catch {keylget interface_status $port.arp_ipv6_interfaces_failed} out]} {
            puts "\tIPv6 Interfaces that didn't receive a response to router \
                    solicitation: $out"
        }
    }
}

if {[keylget interface_status $port_src_handle.arp_request_success] != 1} {
    set int_arp_failed [keylget interface_status $port_src_handle.arp_ipv4_interfaces_failed]
    puts "Interfaces '$int_arp_failed' failed to resolve ARP on port $port_src_handle"
} else {
    puts "ARP was successful on port $port_src_handle"
}

if {[keylget interface_status $port_dst_handle.arp_request_success] != 1} {
    set int_arp_failed [keylget interface_status $port_dst_handle.arp_ipv4_interfaces_failed]
    puts "Interfaces '$int_arp_failed' failed to resolve ARP on port $port_dst_handle"
} else {
    puts "ARP was successful on port $port_dst_handle"
}

set control_status [::ixia::cleanup_session -port_handle $port_handle]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
