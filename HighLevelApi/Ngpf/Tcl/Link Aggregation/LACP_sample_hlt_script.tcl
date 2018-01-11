################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright 1997 - 2015 by IXIA                                             #
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
#    This script intends to demonstrate how to use NGPF OSPFv2 API.            #
#    Script uses four ports to demonstrate LAG properties                      #
#                                                                              #
#    1. It will create 2 LACP topologies, each having an two port which are    #
#       LAG members. It will then modify the ActorSystemId and ActorKey for    #
#       both the LAG systems.                                                  #
#    2. Start the LACP protocol.                                               #
#    3. Retrieve protocol statistics and LACP per port statistics              #
#    4. Disable Synchronization flag on port1 in System1-LACP-LHS              #
#    5. Retrieve protocol statistics and LACP per port statistics              #
#    6. Re-enable Synchronization flag on port1 in System1-LACP-LHS            #
#    7. Retrieve protocol statistics and LACP per port statistics              #
#    8. Perform Simulate Link Down on port1 in System1-LACP-LHS                #
#    9. Retrieve protocol statistics and LACP per port statistics              #
#    10. Perform Simulate Link Up on port1 in System1-LACP-LHS                 #
#    11. Retrieve protocol statistics and LACP per port statistics             #
#    12. Stop All protocols                                                    #
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
# 1. Creating topology and device group                                        #
################################################################################
# Creating a topology on 1st and 3rd port
puts "Adding topology 1 on port 1 and port 3"
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
puts "Creating device group in topology 1"
set device_group_1_status [::ixiangpf::topology_config\
    -topology_handle              $topology_1_handle  \
    -device_group_name            {SYSTEM1-lacp-LHS}    \
    -device_group_multiplier      1                   \
    -device_group_enabled         1                   \
]
if {[keylget device_group_1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_1_status log]"
    return 0
}
set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]

# Creating a topology on 2nd and 4th port
puts "Adding topology 2 on port 2 and port 4"
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
puts "Creating device group in topology 2"
set device_group_2_status [::ixiangpf::topology_config\
    -topology_handle              $topology_2_handle  \
    -device_group_name            {SYSTEM1-lacp-LHS}    \
    -device_group_multiplier      1                   \
    -device_group_enabled         1                   \
]
if {[keylget device_group_2_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget device_group_2_status log]"
    return 0
}
set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]

################################################################################
# Configure protocol interfaces                                                #
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

# Creating LACP on top of Ethernet Stack for the first Device Group

# Creating multivalue for Actor key = 666
puts "Creating multivalue for Actor key = 666"
set multivalue_1_status [::ixiangpf::multivalue_config \
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
if {[keylget multivalue_1_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $multivalue_1_status
}
set multivalue_1_handle [keylget multivalue_1_status multivalue_handle]
# Creating multivalue for System Id = 00:00:00:00:06:66
puts "Creating multivalue for System Id = 00:00:00:00:06:66"
set multivalue_2_status [::ixiangpf::multivalue_config \
    -pattern                 counter                                  \
    -counter_start           00:00:00:00:00:01                        \
    -counter_step            00:00:00:00:00:00                        \
    -counter_direction       increment                                \
    -nest_step               00:00:00:00:00:01                        \
    -nest_owner              $topology_1_handle                       \
    -nest_enabled            0                                        \
    -overlay_value           00:00:00:00:06:66,00:00:00:00:06:66      \
    -overlay_value_step      00:00:00:00:06:66,00:00:00:00:06:66      \
    -overlay_index           1,2                                      \
    -overlay_index_step      0,0                                      \
    -overlay_count           1,1                                      \
]
if {[keylget multivalue_2_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $multivalue_2_status
}
set multivalue_2_handle [keylget multivalue_2_status multivalue_handle]

# Configuring SYSTEM1-lacp-LHS with Actor Key, System Id and flags
puts "Configuring SYSTEM1-lacp-LHS with Actor Key, System Id and flags"
set lacp_1_status [::ixiangpf::emulation_lacp_link_config \
    -mode                                   create                    \
    -handle                                 $ethernet_1_handle        \
    -active                                 1                         \
    -session_type                           lacp                      \
    -actor_key                              $multivalue_1_handle      \
    -actor_port_num                         1                         \
    -actor_port_num_step                    0                         \
    -actor_port_pri                         1                         \
    -actor_port_pri_step                    0                         \
    -actor_system_id                        $multivalue_2_handle      \
    -administrative_key                     1                         \
    -collecting_flag                        1                         \
    -distributing_flag                      1                         \
    -sync_flag                              1                         \
    -aggregation_flag                       1                         \
]
if {[keylget lacp_1_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $lacp_1_status
}
set lacp_1_handle [keylget lacp_1_status lacp_handle]

# Creating multivalue for Actor key = 777
puts "Creating multivalue for Actor key = 777"
# Creating LACP on top of Ethernet Stack for the second Device Group
set multivalue_3_status [::ixiangpf::multivalue_config \
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
if {[keylget multivalue_3_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $multivalue_3_status
}
set multivalue_3_handle [keylget multivalue_3_status multivalue_handle]

# Creating multivalue for System Id = 00:00:00:00:07:77
puts "Creating multivalue for System Id = 00:00:00:00:07:77"
set multivalue_4_status [::ixiangpf::multivalue_config \
    -pattern                 counter                                  \
    -counter_start           00:00:00:00:00:02                        \
    -counter_step            00:00:00:00:00:00                        \
    -counter_direction       increment                                \
    -nest_step               00:00:00:00:00:01                        \
    -nest_owner              $topology_2_handle                       \
    -nest_enabled            0                                        \
    -overlay_value           00:00:00:00:07:77,00:00:00:00:07:77      \
    -overlay_value_step      00:00:00:00:07:77,00:00:00:00:07:77      \
    -overlay_index           1,2                                      \
    -overlay_index_step      0,0                                      \
    -overlay_count           1,1                                      \
]
if {[keylget multivalue_4_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $multivalue_4_status
}
set multivalue_4_handle [keylget multivalue_4_status multivalue_handle]
# Configuring SYSTEM1-lacp-RHS with Actor Key, System Id and flags
puts "Configuring SYSTEM1-lacp-LHS with Actor Key, System Id and flags"
set lacp_2_status [::ixiangpf::emulation_lacp_link_config \
    -mode                                   create                    \
    -handle                                 $ethernet_2_handle        \
    -active                                 1                         \
    -session_type                           lacp                      \
    -actor_key                              $multivalue_3_handle      \
    -actor_port_num                         1                         \
    -actor_port_num_step                    0                         \
    -actor_port_pri                         1                         \
    -actor_port_pri_step                    0                         \
    -actor_system_id                        $multivalue_4_handle      \
    -administrative_key                     1                         \
    -collecting_flag                        1                         \
    -distributing_flag                      1                         \
    -sync_flag                              1                         \
    -aggregation_flag                       1                         \
]
if {[keylget lacp_2_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $lacp_2_status
}
set lacp_2_handle [keylget lacp_2_status lacp_handle]

# Configuration Ends
puts "Waiting 5 seconds before starting protocol..."
after 5000
################################################################################
# Start all protocols                                                          #
################################################################################
puts "Starting all protocol(s) ..."
::ixiangpf::test_control -action start_all_protocols

puts "Waiting for 30 seconds"
after 30000

################################################################################
# Get LACP learned_info stats                                                  #
################################################################################

puts "Fetching SYSTEM1-lacp-LHS learned_info "
set lacp1_stats [::ixiangpf::emulation_lacp_info\
   -handle $lacp_1_handle                 \
   -mode global_learned_info                    \
   -session_type lacp                  \
]
if {[keylget lacp1_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-lacp-LHS learned_info "
puts "------------------------------------------------------------------------"
puts $lacp1_stats
puts "------------------------------------------------------------------------"

################################################################################
# Get LACP per-port stats                                                      #
################################################################################
puts "Fetching SYSTEM1-lacp-RHS per port stats "
set lacp2_stats [::ixiangpf::emulation_lacp_info\
   -handle $deviceGroup_2_handle                 \
   -mode per_port                     \
   -session_type lacp                  \
]
if {[keylget lacp2_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-lacp-RHS per port stats"
puts "------------------------------------------------------------------------"
puts $lacp2_stats
puts "------------------------------------------------------------------------"

after 5000
################################################################################
# 4. Disable Synchronization flag on port1 in System1-LACP-LHS
################################################################################
set multivalue_p1_status [::ixiangpf::multivalue_config \
    -pattern                 single_value      \
    -single_value            1                 \
    -overlay_value           0                 \
    -overlay_value_step      0                 \
    -overlay_index           1                 \
    -overlay_index_step      0                 \
    -overlay_count           1                 \
]
if {[keylget multivalue_3_status status] != $::SUCCESS} {
    $::ixnHLT_errorHandler [info script] $multivalue_3_status
}
set disable_syncPort1_handle [keylget multivalue_3_status multivalue_handle]

puts "\n\nDisable Synchronization flag on port1 in System1-LACP-LHS"
set disable_syncPort1_status [::ixiangpf::emulation_lacp_link_config \
    -handle                 $lacp_1_handle                          \
    -session_type                           lacp                      \
    -mode                   modify                                         \
    -sync_flag              0              \

]
if {[keylget disable_syncPort1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget disable_syncPort1_status log]"
    return 0
}
################################################################################
# Applying changes one the fly                                                 #
################################################################################
puts "Applying changes on the fly"
set applyChanges [::ixiangpf::test_control\
   -action apply_on_the_fly_changes       \
]
if {[keylget applyChanges status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget applyChanges log]"
    return 0
}
after 5000
################################################################################
# Get LACP learned_info stats                                                  #
################################################################################

puts "Fetching SYSTEM1-lacp-LHS learned_info "
set lacp1_stats [::ixiangpf::emulation_lacp_info\
   -handle $lacp_1_handle                 \
   -mode global_learned_info                    \
   -session_type lacp                  \
]
if {[keylget lacp1_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-lacp-LHS learned_info "
puts "------------------------------------------------------------------------"
puts $lacp1_stats
puts "------------------------------------------------------------------------"

################################################################################
# Get LACP per-port stats                                                      #
################################################################################
puts "Fetching SYSTEM1-lacp-RHS per port stats "
set lacp2_stats [::ixiangpf::emulation_lacp_info\
   -handle $deviceGroup_2_handle                 \
   -mode per_port                     \
   -session_type lacp                  \
]
if {[keylget lacp2_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-lacp-RHS per port stats"
puts "------------------------------------------------------------------------"
puts $lacp2_stats
puts "------------------------------------------------------------------------"

after 5000
################################################################################
# Re-enable Synchronization flag on port1 in System1-LACP-LHS                  #
################################################################################
puts "\n\nRe-enable Synchronization flag on port1 in System1-LACP-LHS"
set enable_syncPort1_status [::ixiangpf::emulation_lacp_link_config \
    -handle                 $lacp_1_handle                          \
    -mode                   modify                                         \
    -sync_flag               1              \
]
if {[keylget enable_syncPort1_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget enable_syncPort1_status log]"
    return 0
}
################################################################################
# Applying changes one the fly                                                 #
################################################################################
puts "Applying changes on the fly"
set applyChanges [::ixiangpf::test_control\
   -action apply_on_the_fly_changes       \
]
if {[keylget applyChanges status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget applyChanges log]"
    return 0
}
after 5000
################################################################################
# Get LACP learned_info stats                                                  #
################################################################################

puts "Fetching SYSTEM1-lacp-LHS learned_info "
set lacp1_stats [::ixiangpf::emulation_lacp_info\
   -handle $lacp_1_handle                 \
   -mode global_learned_info                    \
   -session_type lacp                  \
]
if {[keylget lacp1_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-lacp-LHS learned_info "
puts "------------------------------------------------------------------------"
puts $lacp1_stats
puts "------------------------------------------------------------------------"

################################################################################
# Get LACP per-port stats                                                      #
################################################################################
puts "Fetching SYSTEM1-lacp-RHS per port stats "
set lacp2_stats [::ixiangpf::emulation_lacp_info\
   -handle $deviceGroup_2_handle                 \
   -mode per_port                     \
   -session_type lacp                  \
]
if {[keylget lacp2_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-lacp-RHS per port stats"
puts "------------------------------------------------------------------------"
puts $lacp2_stats
puts "------------------------------------------------------------------------"

after 5000

################################################################################
# Perform Simulate Link Down on port1 in System1-LACP-LHS                      #
################################################################################
puts "\n\nPerform Simulate Link Down on port1 in System1-LACP-LHS "

set interface_status [::ixia::interface_config \
        -port_handle        $port1     \
        -op_mode            sim_disconnect   \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
after 5000
################################################################################
# Get LACP learned_info   stats                                                #
################################################################################

puts "Fetching SYSTEM1-lacp-LHS learned_info "
set lacp1_stats [::ixiangpf::emulation_lacp_info\
   -handle $lacp_1_handle                 \
   -mode global_learned_info                    \
   -session_type lacp                  \
]
if {[keylget lacp1_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-lacp-LHS learned_info "
puts "------------------------------------------------------------------------"
puts $lacp1_stats
puts "------------------------------------------------------------------------"

################################################################################
# Get LACP per-port stats                                                      #
################################################################################
puts "Fetching SYSTEM1-lacp-RHS per port stats "
set lacp2_stats [::ixiangpf::emulation_lacp_info\
   -handle $deviceGroup_2_handle                 \
   -mode per_port                     \
   -session_type lacp                  \
]
if {[keylget lacp2_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-lacp-RHS per port stats"
puts "------------------------------------------------------------------------"
puts $lacp2_stats
puts "------------------------------------------------------------------------"

after 5000
################################################################################
# Perform Simulate Link Up on port1 in System1-LACP-LHS                        #
################################################################################
puts "\n\nPerform Simulate Link Up on port1 in System1-LACP-LHS "

set interface_status [::ixia::interface_config \
        -port_handle        $port1     \
        -op_mode            normal   \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
after 5000
################################################################################
# Get LACP learned_info   stats                                                #
################################################################################

puts "Fetching SYSTEM1-lacp-LHS learned_info "
set lacp1_stats [::ixiangpf::emulation_lacp_info\
   -handle $lacp_1_handle                 \
   -mode global_learned_info                    \
   -session_type lacp                  \
]
if {[keylget lacp1_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-lacp-LHS learned_info "
puts "------------------------------------------------------------------------"
puts $lacp1_stats
puts "------------------------------------------------------------------------"

################################################################################
# Get LACP per-port   stats                                                    #
################################################################################
puts "Fetching SYSTEM1-lacp-RHS per port stats "
set lacp2_stats [::ixiangpf::emulation_lacp_info\
   -handle $deviceGroup_2_handle                 \
   -mode per_port                     \
   -session_type lacp                  \
]
if {[keylget lacp2_stats status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget lacp1_stats log]"
    return 0
}
puts "\n\nPrinting SYSTEM1-lacp-RHS per port stats"
puts "------------------------------------------------------------------------"
puts $lacp2_stats
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
