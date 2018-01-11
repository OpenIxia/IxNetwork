################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    06/04/2015 - Sumit Deb - created sample                                   #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF StaticLag API.         #
#    Script uses four ports to demonstrate LAG properties                      #
#                                                                              #
#    1. It will create 2 StaticLag topologies, each having two ports which are #
#       LAG members. It will then modify the Lag Id for both the LAG systems   #
#    2. Start the StaticLag protocol.                                          #
#    3. Retrieve protocol statistics and StaticLag per port statistics         #
#    4. Perform Simulate Link Down on port1 in System1-StaticLag-LHS           #
#    5. Retrieve protocol statistics and StaticLag per port statistics         #
#    6. Perform Simulate Link Up on port1 in System1-StaticLag-LHS             #
#    7. Retrieve protocol statistics and StaticLag per port statistics         #
#    8. Stop All protocols                                                     #
#   Ixia Software:                                                             #
#    IxOS      6.90EA                                                          #
#    IxNetwork 7.50EA                                                          #
#                                                                              #
################################################################################

################################################################################
# Utilities                                                                    #
################################################################################
if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}
# End Utilities ################################################################

# Script Starts
puts "!!! Test Script Starts !!!"
################################################################################
# Connection to the chassis, IxNetwork Tcl Server                              #
################################################################################
set chassis_ip        {10.205.28.173}
set tcl_server        10.205.28.173
set port_list         {1/1 1/2 1/3 1/4}
set ixNetwork_client  "10.205.28.41:5555"
set test_name         [info script]

# Connecting to Chassis
puts "Connecting to chassis and client..."
set connect_status [::ixiangpf::connect       \
    -reset                   1                \
    -device                  $chassis_ip      \
    -port_list               $port_list       \
    -ixnetwork_tcl_server    $ixNetwork_client\
    -tcl_server              $tcl_server      \
]

if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
}
# End Connecting to Chassis
puts "End connecting to chassis ..."

# Retrieving port handles, for later use
set port1 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 0]]
set port2 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 1]]
set port3 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 2]]
set port4 [keylget connect_status port_handle.$chassis_ip.[lindex $port_list 3]]

################################################################################
# Creating topology and device group                                           #
################################################################################
# Creating a topology on first port
puts "Adding topology 1 on port 1"
set topology_1_status [::ixiangpf::topology_config\
    -topology_name      {LAG1-LHS}                \
    -port_handle        "$port1 $port3"                  \
]
if {[keylget topology_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_1_status log]"
    return 0
}
set topology_1_handle [keylget topology_1_status topology_handle]

# Creating a device group in topology 1
puts "Creating device group in first port"
set device_group_1_status [::ixiangpf::topology_config\
    -topology_handle              $topology_1_handle  \
    -device_group_name            {SYSTEM1-StaticLag-LHS}    \
    -device_group_multiplier      1                   \
    -device_group_enabled         1                   \
]
if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_1_status log]"
    return 0
}
set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

# Creating a topology on 2nd port
puts "Adding topology 1 on port 1"
set topology_2_status [::ixiangpf::topology_config\
    -topology_name      {LAG1-RHS}                \
    -port_handle        "$port2 $port4"                  \
]
if {[keylget topology_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget topology_2_status log]"
    return 0
}
set topology_2_handle [keylget topology_2_status topology_handle]

# Creating a device group in topology 2
puts "Creating device group in second port"
set device_group_2_status [::ixiangpf::topology_config\
    -topology_handle              $topology_2_handle  \
    -device_group_name            {SYSTEM1-StaticLag-LHS}    \
    -device_group_multiplier      1                   \
    -device_group_enabled         1                   \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_2_status log]"
    return 0
}
set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]

################################################################################
#  Configure protocol interfaces                                               #
################################################################################
# Creating ethernet stack for the first Device Group
puts "Creating ethernet stack within Device Group 1"
set ethernet_1_status [::ixiangpf::interface_config    \
    -protocol_name                {Ethernet 1}         \
    -protocol_handle              $deviceGroup_1_handle\
    -mtu                          1500                 \
    -src_mac_addr                 "00.11.01.00.00.01"    \
]

if {[keylget ethernet_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_1_status log]"
    return 0
}

set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]

# Creating ethernet stack for the second Device Group
puts "Creating ethernet stack within Device Group 2"
set ethernet_2_status [::ixiangpf::interface_config    \
    -protocol_name                {Ethernet 2}         \
    -protocol_handle              $deviceGroup_2_handle\
    -mtu                          1500                 \
    -src_mac_addr                 "00.12.01.00.00.01"  \
]

if {[keylget ethernet_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ethernet_2_status log]"
    return 0
}
set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]

# Creating Static LAG on top of Ethernet Stack for the first Device Group with LAG id 666"
puts "Creating Static LAG on top of Ethernet Stack for the first Device Group with LAG id 666"
set sys1_lhs_lagId_multivalue_2_status [::ixiangpf::multivalue_config \
    -pattern                 single_value            \
    -single_value            1                       \
    -nest_step               1                       \
    -nest_owner              $topology_1_handle      \
    -nest_enabled            0                       \
    -overlay_value           666,666                 \
    -overlay_value_step      666,666                 \
    -overlay_index           1,2                     \
    -overlay_index_step      0,0                     \
    -overlay_count           1,1                     \
]
if {[keylget sys1_lhs_lagId_multivalue_2_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $sys1_lhs_lagId_multivalue_2_status
}
set sys1_lhs_lagId_multivalue_2_handle [keylget sys1_lhs_lagId_multivalue_2_status multivalue_handle]
set static_lag_1_status [::ixiangpf::emulation_lacp_link_config \
    -mode              create                    \
    -handle            $ethernet_1_handle        \
    -active            1                         \
    -session_type      staticLag                 \
    -lag_id            $sys1_lhs_lagId_multivalue_2_handle      \
]
if {[keylget static_lag_1_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $static_lag_1_status
}
set staticLag_1_handle [keylget static_lag_1_status staticLag_handle]

# Creating Static LAG on top of Ethernet Stack for the second Device Group with LAG id 777"
puts "Creating Static LAG on top of Ethernet Stack for the second Device Group with LAG id 777"
set sys1_rhs_lagId_multivalue_2_status [::ixiangpf::multivalue_config \
    -pattern                 single_value            \
    -single_value            1                       \
    -nest_step               1                       \
    -nest_owner              $topology_2_handle      \
    -nest_enabled            0                       \
    -overlay_value           777,777                 \
    -overlay_value_step      777,777                 \
    -overlay_index           1,2                     \
    -overlay_index_step      0,0                     \
    -overlay_count           1,1                     \
]
if {[keylget sys1_rhs_lagId_multivalue_2_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $sys1_rhs_lagId_multivalue_2_status
}
set sys1_rhs_lagId_multivalue_2_handle [keylget sys1_rhs_lagId_multivalue_2_status multivalue_handle]
set static_lag_2_status [::ixiangpf::emulation_lacp_link_config \
    -mode              create                    \
    -handle            $ethernet_2_handle        \
    -active            1                         \
    -session_type      staticLag                 \
    -lag_id            $sys1_rhs_lagId_multivalue_2_handle      \
]
if {[keylget static_lag_2_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $static_lag_2_status
}
set staticLag_2_handle [keylget static_lag_2_status staticLag_handle]

# Configuration Ends

puts "Waiting 5 seconds before starting protocol..."
after 5000
################################################################################
# Start all protocols                                                          #
################################################################################
puts "Starting all protocol(s) ..."
set r [::ixiangpf::test_control -action start_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "Waiting for 30 seconds"
after 30000

################################################################################
# Get Static LAG learned_info   stats                                          #
################################################################################

puts "Fetching SYSTEM1-StaticLag-LHS learned_info "
set staticLag1_stats [::ixiangpf::emulation_lacp_info\
   -handle $staticLag_1_handle                 \
   -mode global_learned_info                    \
   -session_type staticLag                  \
]
if {[keylget staticLag1_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget staticLag1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-StaticLag-LHS learned_info "
puts "------------------------------------------------------------------------"
puts $staticLag1_stats
puts "------------------------------------------------------------------------"

puts "Fetching SYSTEM1-StaticLag-RHS learned_info "
set staticLag2_stats [::ixiangpf::emulation_lacp_info\
   -handle $deviceGroup_2_handle                 \
   -mode per_port                     \
   -session_type staticLag                  \
]
if {[keylget staticLag2_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget staticLag1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-StaticLag-RHS stats"
puts "------------------------------------------------------------------------"
puts $staticLag2_stats
puts "------------------------------------------------------------------------"

after 5000

################################################################################
# Perform Simulate Link Down on port1 in SYSTEM1-StaticLag-LHS                 #
################################################################################
puts "\n\nPerform Simulate Link Down on port1 in SYSTEM1-StaticLag-LHS "

set interface_status [::ixia::interface_config \
        -port_handle        $port1     \
        -op_mode            sim_disconnect   \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
after 5000

################################################################################
# Get Static LAG learned_info & per-port stats                                 #
################################################################################

puts "Fetching SYSTEM1-StaticLag-LHS learned_info "
set staticLag1_stats [::ixiangpf::emulation_lacp_info\
   -handle $staticLag_1_handle                 \
   -mode global_learned_info                    \
   -session_type staticLag                  \
]
if {[keylget staticLag1_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget staticLag1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-StaticLag-LHS learned_info "
puts "------------------------------------------------------------------------"
puts $staticLag1_stats
puts "------------------------------------------------------------------------"

puts "Fetching SYSTEM1-StaticLag-RHS learned_info "
set staticLag2_stats [::ixiangpf::emulation_lacp_info\
   -handle $deviceGroup_2_handle                 \
   -mode per_port                     \
   -session_type staticLag                  \
]
if {[keylget staticLag2_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget staticLag1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-StaticLag-RHS stats"
puts "------------------------------------------------------------------------"
puts $staticLag2_stats
puts "------------------------------------------------------------------------"

after 5000

################################################################################
# Perform Simulate Link Down on port1 in SYSTEM1-StaticLag-LHS                 #
################################################################################
puts "\n\nPerform Simulate Link Down on port1 in SYSTEM1-StaticLag-LHS "

set interface_status [::ixia::interface_config \
        -port_handle        $port1     \
        -op_mode            normal   \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
after 5000

################################################################################
# Get Static LAG learned_info & per-port  stats                                #
################################################################################

puts "Fetching SYSTEM1-StaticLag-LHS learned_info "
set staticLag1_stats [::ixiangpf::emulation_lacp_info\
   -handle $staticLag_1_handle                 \
   -mode global_learned_info                    \
   -session_type staticLag                  \
]
if {[keylget staticLag1_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget staticLag1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-StaticLag-LHS learned_info "
puts "------------------------------------------------------------------------"
puts $staticLag1_stats
puts "------------------------------------------------------------------------"

puts "Fetching SYSTEM1-StaticLag-RHS per port stats "
set staticLag2_stats [::ixiangpf::emulation_lacp_info\
   -handle $deviceGroup_2_handle                 \
   -mode per_port                     \
   -session_type staticLag                  \
]
if {[keylget staticLag2_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget staticLag1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-StaticLag-RHS stats"
puts "------------------------------------------------------------------------"
puts $staticLag2_stats
puts "------------------------------------------------------------------------"

after 5000

###############################################################################
# Stop all protocols                                                          #
###############################################################################
puts "Stopping all protocol(s) ..."
set r [::ixiangpf::test_control -action stop_all_protocols]
if {[keylget r status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget r log]"
    return 0
}
puts "!!! Test Script Ends !!!"

