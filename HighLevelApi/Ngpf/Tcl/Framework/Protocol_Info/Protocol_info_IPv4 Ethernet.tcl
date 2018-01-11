################################################################################
# Version 1.0
# $Author: Laura - Adriana Savu$
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#
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
#    This sample creates one topology with one device group containing one     #
# IPv4 stack and uses protocol_info command to retrive information about the   #
# Ethernet and IPv4 protocols sessions.                                        #
#                                                                              #
################################################################################


################################################################################
# Package require Ixia                                                         #
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

################################################################################
#  chassis, card, port configuration                                           #
################################################################################
set chassis_ip 10.215.180.121
set ixnetwork_tcl_server localhost
set port_list [list 2/1 2/2]
set test_name                   [info script]

################################################################################################
# START - Connect to the chassis                                                               #
# Connect to the IxNetwork Tcl Server & chassis, reset to factory defaults and take ownership  #
################################################################################################

set connect_status [::ixiangpf::connect             \
    -reset                                          \
    -device $chassis_ip                             \
    -port_list $port_list                           \
    -ixnetwork_tcl_server $ixnetwork_tcl_server     \
]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}
puts "End connecting to chassis ..."

set port_handle1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port_handle2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]

################################################################################
# Configure Topology, Device Group                                             #
################################################################################
puts "Creating topology"
set topology_status [::ixiangpf::topology_config             \
    -topology_name      {Topology 1}                         \
    -port_handle        [list $port_handle1 $port_handle2]   \
    ]
if {[keylget topology_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_status log]"
    return 0
}
set topology_handle [keylget topology_status topology_handle]

puts "Creating device group"
set device_group_status [::ixiangpf::topology_config      \
    -topology_handle              $topology_handle        \
    -device_group_name            {Device Group 1}        \
    -device_group_multiplier      10                      \
    -device_group_enabled         1                       \
    ]
if {[keylget device_group_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_status log]"
    return 0
}
set deviceGroup_handle [keylget device_group_status device_group_handle]

###############################################################################
# Create Ethernet Stack for the Device Group                                  #
###############################################################################
puts "Creating ethernet stack"
set ethernet_status [::ixiangpf::interface_config            \
    -protocol_name                {Ethernet 1}               \
    -protocol_handle              $deviceGroup_handle        \
    -mtu                          1500                       \
    -src_mac_addr                 00.aa.bb.cc.00.01          \
    -src_mac_addr_step            00.00.00.00.00.01          \
    -vlan                         1                          \
    -vlan_id                      1                          \
    -vlan_id_step                 1                          \
    -vlan_id_count                1                          \
    -vlan_tpid                    0x8100                     \
    -vlan_user_priority           0                          \
    -vlan_user_priority_step      0                          \
    -use_vpn_parameters           0                          \
    -site_id                      0                          \
]
if {[keylget ethernet_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_status log]"
    return 0
}
set ethernet_handle [keylget ethernet_status ethernet_handle]
    
################################################################################
# Create IPv4 Stack on top of Ethernet Stack                                   #
################################################################################
puts "Creating IPv4 stack"
set ipv4_status [::ixiangpf::interface_config                  \
    -protocol_name                     {IPv4 1}                \
    -protocol_handle                   $ethernet_handle        \
    -ipv4_resolve_gateway              0                       \
    -ipv4_manual_gateway_mac           00.00.00.00.00.01       \
    -ipv4_manual_gateway_mac_step      00.00.00.00.00.00       \
    -gateway                           100.1.0.1               \
    -gateway_step                      0.0.1.0                 \
    -intf_ip_addr                      100.1.0.2               \
    -intf_ip_addr_step                 0.0.1.0                 \
    -netmask                           255.255.255.0           \
]

if {[keylget ipv4_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ipv4_status log]"
    return 0
}
set ipv4_handle [keylget ipv4_status ipv4_handle]

################################################################################
# Start protocols                                                              #
################################################################################
puts "Starting protocols"
set start_status [::ixiangpf::test_control  \
    -action         start_all_protocols     \
]
if {[keylget start_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget start_status log]"
    return 0
}

puts "Waiting for protocols to start"
after 10000
update idletasks
#############################################################################################################
# Retrieve information about the number of Ethernet sessions that are in each state : up, down, not_started #
#############################################################################################################
puts "Retrieving aggregate statistics for ethernet sessions"
set protocol_status [::ixiangpf::protocol_info  \
    -mode           aggregate                   \
    -handle         $ethernet_handle            \
]
if {[keylget protocol_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_status log]"
    return 0
}


puts "_________________________________________"
puts "Statistics about ethernet sessions state"

puts "   Sessions down: [keylget protocol_status $ethernet_handle.aggregate.sessions_down]"
puts "   Sessions up: [keylget protocol_status $ethernet_handle.aggregate.sessions_up]"
puts "   Sessions not started: [keylget protocol_status $ethernet_handle.aggregate.sessions_not_started]"
puts "   Sessions total: [keylget protocol_status $ethernet_handle.aggregate.sessions_total]"


#################################################################################################################
# Retrieve information about the number of Ethernet sessions that are in each state : up, down, not_started     #
# Due to the use of port_filter information will be returned only for the sesions configured on the first port  #
#################################################################################################################
puts "Retrieving aggregate statistics for ethernet session configured on the first port"
set protocol_status [::ixiangpf::protocol_info  \
    -mode           aggregate                   \
    -handle         $ethernet_handle            \
    -port_filter    $port_handle1               \

]
if {[keylget protocol_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_status log]"
    return 0
}

puts "______________________________________________________"
puts "Statistics about ethernet sessions state on first port"

puts "   Sessions down: [keylget protocol_status $ethernet_handle.aggregate.$port_handle1.sessions_down]"
puts "   Sessions up: [keylget protocol_status $ethernet_handle.aggregate.$port_handle1.sessions_up]"
puts "   Sessions not started: [keylget protocol_status $ethernet_handle.aggregate.$port_handle1.sessions_not_started]"
puts "   Sessions total: [keylget protocol_status $ethernet_handle.aggregate.$port_handle1.sessions_total]"

###########################################################################################################
# Retrieve the handles of IPv4 sessions that are in each state : up, down, not_started                    #
###########################################################################################################
puts "Retriving handles of IPv4 sessions"
set protocol_status [::ixiangpf::protocol_info  \
    -mode           handles                     \
    -handle         $ipv4_handle                \
]
if {[keylget protocol_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_status log]"
    return 0
}


puts "_________________________"
puts "Handles of IPv4 sessions "

puts "   Sessions up handles: "
foreach item [keylget protocol_status $ipv4_handle.handles.sessions_up] {
    puts "    $item"
}
puts "   Sessions total handles: "
foreach item [keylget protocol_status $ipv4_handle.handles.sessions_total] {
    puts "    $item"
}

###########################################################################################################
# Retrieve the handles of IPv4 sessions that are in each state : up, down, not_started                    #
# Due to the use of port_filter, only the handles of the sessions on the second port will be returned     #
###########################################################################################################
puts "Retriving handles of IPv4 sessions configured on port 2"
set protocol_status [::ixiangpf::protocol_info  \
    -mode           handles                     \
    -handle         $ipv4_handle                \
    -port_filter    $port_handle2               \
]
if {[keylget protocol_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget protocol_status log]"
    return 0
}

puts "______________________________________"
puts "Handles of IPv4 sessions, second port "

puts "   Sessions up handles: "
foreach item [keylget protocol_status $ipv4_handle.handles.$port_handle2.sessions_up] {
    puts "       $item"
}
puts "   Sessions total handles: "
foreach item [keylget protocol_status $ipv4_handle.handles.$port_handle2.sessions_total] {
    puts "       $item"
}

return 1