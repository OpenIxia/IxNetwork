################################################################################
# Version 1.2    $Revision: 3 $
# $Author: Lavinia Raicea $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    04/05/2005 Lavinia Raicea
#    07/20/2007 Matei-Eugen Vasile
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
#    This sample performs various operation. It creates, modifies and deletes  #
#    IGMP hosts. Creates group pools and source pools. Adds, modifies and      #
#    deletes group and source pools to IGMP hosts.                             #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP 10.205.19.96
set port_list [list 2/1 2/2]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                           \
        -reset                                              \
        -device                         $chassisIP          \
        -port_list                      $port_list          \
        -username                       ixiaApiUser         \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}
set port_handle1 [keylget connect_status port_handle.$chassisIP.[lindex $port_list 0]]
set port_handle2 [keylget connect_status port_handle.$chassisIP.[lindex $port_list 1]]

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config                \
        -port_handle    [list $port_handle1 $port_handle2]  \
        -autonegotiation                1                   \
        -duplex                         full                \
        -speed                          ether100            \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}


# Create session1
set igmp_status_1 [::ixia::emulation_igmp_config              \
        -port_handle                    $port_handle1       \
        -mode                           create              \
        -reset                                              \
        -msg_interval                   167                 \
        -igmp_version                   v3                  \
        -ip_router_alert                1                   \
        -general_query                  1                   \
        -group_query                    1                   \
        -unsolicited_report_interval    200                 \
        -suppress_report                0                   \
        -max_response_control           1                   \
        -max_response_time              50                  \
        -intf_ip_addr                   100.41.1.2          \
        -neighbor_intf_ip_addr          100.41.1.1          \
        -vlan_id_mode                   increment           \
        -vlan_id                        10                  \
        -vlan_id_step                   1                   \
        -vlan_user_priority             7                   \
        ]
if {[keylget igmp_status_1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmp_status_1 log]"
}
puts "Create:     $igmp_status_1"
set session1 [keylget igmp_status_1 handle]

# Create session2
set igmp_status_2 [::ixia::emulation_igmp_config              \
        -port_handle                    $port_handle1       \
        -mode                           create              \
        -igmp_version                   v3                  \
        -intf_ip_addr                   100.41.1.3          \
        -neighbor_intf_ip_addr          100.41.1.1          \
        ]

if {[keylget igmp_status_2 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmp_status_2 log]"
}
puts "Create:     $igmp_status_2"
set session2 [keylget igmp_status_2 handle]

# Create group pools 1 - 5
for {set i 0} {$i < 5} {incr i} {
    set retGroup [::ixia::emulation_multicast_group_config  \
            -mode create                                    \
            -num_groups                 5                   \
            -ip_addr_start                                  \
                    [mpexpr 225 + $i].0.1.1                 \
            -ip_addr_step               0.0.1.0             \
            -ip_prefix_len              24                  \
            ]
    
    if {[keylget retGroup status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget retGroup log]"
    }
    puts "Create:     $retGroup"
    set temp_group group_pool
    set temp_group [append temp_group [mpexpr $i + 1]]
    set $temp_group [keylget retGroup handle]
}

# Create group pools 1 - 6
for {set i 0} {$i < 5} {incr i} {
    set mcast [::ixia::emulation_multicast_source_config    \
            -mode create                                    \
            -num_sources                5                   \
            -ip_addr_start                                  \
                    100.[mpexpr 35 + $i].1.1                \
            -ip_addr_step               0.0.1.0             \
            -ip_prefix_len              24                  \
            ]
    if {[keylget mcast status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget mcast log]"
    }
    puts "Create:     $mcast"
    set temp_source source_pool
    set temp_source [append temp_source [mpexpr $i + 1]]
    set $temp_source [keylget mcast handle]
}
set source_pool6 "wrong_source_pool"

# Create session1 group_member1
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session1           \
        -group_pool_handle              $group_pool1        \
        -source_pool_handle                                 \
                [list $source_pool1 $source_pool2]          \
        ]
        
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member1 [keylget retMember handle]

# Create session1 group_member2
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session1           \
        -group_pool_handle              $group_pool2        \
        -source_pool_handle                                 \
                [list $source_pool2 $source_pool3]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member2 [keylget retMember handle]

# Create session1 group_member3
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session1           \
        -group_pool_handle              $group_pool3        \
        -source_pool_handle                                 \
                [list $source_pool3 $source_pool4]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member3 [keylget retMember handle]

# Create session2 group_member4
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session2           \
        -group_pool_handle              $group_pool1        \
        -source_pool_handle                                 \
            [list $source_pool1 $source_pool3 $source_pool5]\
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member4 [keylget retMember handle]

# Create session2 group_member5
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session2           \
        -group_pool_handle              $group_pool1        \
        -source_pool_handle                                 \
                [list $source_pool2 $source_pool4]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member5 [keylget retMember handle]

# Modify group_member5
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           modify              \
        -handle                         $group_member5      \
        -group_pool_handle              $group_pool2        \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Modify:     $retMember"

# Modify group_member2
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           modify              \
        -handle                         $group_member2      \
        -source_pool_handle                                 \
                [list $source_pool3 $source_pool4]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Modify:     $retMember"

# Modify group_member3
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           modify              \
        -handle                         $group_member3      \
        -source_pool_handle                                 \
                [list $source_pool5 $source_pool1]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Modify:     $retMember"

# Create session3,4
set igmp_status_3 [::ixia::emulation_igmp_config              \
        -port_handle                    $port_handle1       \
        -mode                           create              \
        -msg_interval                   167                 \
        -igmp_version                   v3                  \
        -ip_router_alert                0                   \
        -general_query                  0                   \
        -group_query                    0                   \
        -unsolicited_report_interval    200                 \
        -suppress_report                0                   \
        -max_response_control           1                   \
        -max_response_time              0                   \
        -intf_ip_addr                   100.41.1.4          \
        -neighbor_intf_ip_addr          100.41.1.1          \
        -count                          2                   \
        ]
if {[keylget igmp_status_3 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmp_status_3 log]"
}
puts "Create:     $igmp_status_3"
set session3 [lindex [keylget igmp_status_3 handle] 0]
set session4 [lindex [keylget igmp_status_3 handle] 1]

# Create session3 group_member6
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session3           \
        -group_pool_handle              $group_pool3        \
        -source_pool_handle                                 \
                [list $source_pool3 $source_pool4]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member6 [keylget retMember handle]

# ERROR - Create session3 group_member7 - source6 is not valid
# Returned status 0 
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session4           \
        -group_pool_handle              $group_pool2        \
        -source_pool_handle                                 \
                [list $source_pool5 $source_pool6]          \
        ]
puts "NOT Create: $retMember"

# Create session3 group_member7
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session4           \
        -group_pool_handle              $group_pool2        \
        -source_pool_handle                                 \
                [list $source_pool5 $source_pool1]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member7 [keylget retMember handle]

# Disable session3
set igmpConf [::ixia::emulation_igmp_config                   \
        -handle                         $session3           \
        -mode                           disable             \
        ]
if {[keylget igmpConf status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmpConf log]"
}
puts "Disable:    $igmpConf"

# Enable session3
set igmpConf [::ixia::emulation_igmp_config                   \
        -handle                         $session3           \
        -mode                           enable              \
        ]
if {[keylget igmpConf status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmpConf log]"
}
puts "Enable:     $igmpConf"



# Create session5,6,7
set igmp_status_4 [::ixia::emulation_igmp_config              \
        -port_handle                    $port_handle2       \
        -mode                           create              \
        -reset                                              \
        -igmp_version                   v3                  \
        -ip_router_alert                0                   \
        -general_query                  0                   \
        -group_query                    0                   \
        -unsolicited_report_interval    100                 \
        -suppress_report                0                   \
        -max_response_control           1                   \
        -max_response_time              0                   \
        -intf_ip_addr                   100.42.1.4          \
        -neighbor_intf_ip_addr          100.42.1.1          \
        -count                          3                   \
        ]
if {[keylget igmp_status_4 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmp_status_4 log]"
}
puts "Create:     $igmp_status_4"
set session5 [lindex [keylget igmp_status_4 handle] 0]
set session6 [lindex [keylget igmp_status_4 handle] 1]
set session7 [lindex [keylget igmp_status_4 handle] 2]

# Create session5 group_member8
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session5           \
        -group_pool_handle              $group_pool1        \
        -source_pool_handle                                 \
                [list $source_pool1 $source_pool2]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member8 [keylget retMember handle]

# ERROR - Create session5 group_member9 - source6 is not valid
# Returned status 0
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session5           \
        -group_pool_handle              $group_pool2        \
        -source_pool_handle                                 \
                [list $source_pool5 $source_pool6]          \
        ]
puts "NOT Create: $retMember"

# Create session6 group_member9
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session6           \
        -group_pool_handle              $group_pool3        \
        -source_pool_handle                                 \
                [list $source_pool3 $source_pool4]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member9 [keylget retMember handle]

# Create session6 group_member10
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session6           \
        -group_pool_handle              $group_pool4        \
        -source_pool_handle                                 \
                [list $source_pool1 $source_pool2]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member10 [keylget retMember handle]

# Create session5 group_member11
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session5           \
        -group_pool_handle              $group_pool2        \
        -source_pool_handle                                 \
                [list $source_pool5 $source_pool2]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member11 [keylget retMember handle]

# Disable sessions on different ports
set retMember [::ixia::emulation_igmp_config                \
        -mode                           disable             \
        -handle                                             \
                [list $session1 $session5 $session6]        \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Disable:    $retMember"

# Enable sessions on different ports
set retMember [::ixia::emulation_igmp_config                \
        -mode                           enable              \
        -handle                                             \
                [list $session1 $session5 $session6]        \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Enable:     $retMember"

# Modify session6 group_member10
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           modify              \
        -handle                         $group_member10     \
        -group_pool_handle              $group_pool5        \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Modify:     $retMember"

# Disable all sessions on port 1
set igmpConf [::ixia::emulation_igmp_config                   \
        -port_handle                    $port_handle1       \
        -mode                           disable_all         \
        ]
if {[keylget igmpConf status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmpConf log]"
}
puts "Disable_all:$igmpConf"

# Disable sessions 2 and 4
set igmpConf [::ixia::emulation_igmp_config                   \
        -handle                                             \
                [list $session2  $session4]                 \
        -mode                           disable             \
        ]
if {[keylget igmpConf status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmpConf log]"
}
puts "Disable:    $igmpConf"

# Modify session1 and session7
set igmpConf [::ixia::emulation_igmp_config                   \
        -handle                                             \
                [list $session1 $session7]                  \
        -mode                           modify              \
        -suppress_report                1                   \
        -max_response_control           0                   \
        -filter_mode                    include             \
        -intf_ip_addr                                       \
                [list 172.17.2.1 172.17.2.7]                \
        -mac_address_init                                   \
                [list 0011.2233.4455 0011.2233.4455]        \
        ]
if {[keylget igmpConf status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmpConf log]"
}
puts "Modify:     $igmpConf"

# Enable all sessions on ports
set igmpConf [::ixia::emulation_igmp_config                   \
        -port_handle                                        \
                [list $port_handle1 $port_handle2]          \
        -mode                           enable_all          \
        ]
if {[keylget igmpConf status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmpConf log]"
}
puts "Enable_all: $igmpConf"

# Disable all sessions on ports
set igmpConf [::ixia::emulation_igmp_config                   \
        -port_handle                                        \
                [list $port_handle1 $port_handle2]          \
        -mode                           disable_all         \
        ]
if {[keylget igmpConf status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmpConf log]"
}
puts "Disable_all:$igmpConf"


# Enable all sessions on ports
set igmpConf [::ixia::emulation_igmp_config                   \
        -port_handle                    $port_handle1       \
        -mode                           enable_all          \
        ]
if {[keylget igmpConf status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmpConf log]"
}
puts "Enable_all: $igmpConf"

# Enable all sessions on ports
set igmpConf [::ixia::emulation_igmp_config                   \
        -port_handle                    $port_handle2       \
        -mode                           enable_all          \
        ]
if {[keylget igmpConf status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget igmpConf log]"
}
puts "Enable_all: $igmpConf"

# Delete group_member11
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           delete              \
        -handle                         $group_member11     \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Delete:     $retMember"

# Create session5 group_member11
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session5           \
        -group_pool_handle              $group_pool3        \
        -source_pool_handle                                 \
                [list $source_pool3 $source_pool2]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member11 [keylget retMember handle]

# Create session5 group_member12
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session5           \
        -group_pool_handle              $group_pool5        \
        -source_pool_handle                                 \
                [list $source_pool1 $source_pool2]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member12 [keylget retMember handle]

# Create session7 group_member13
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session7           \
        -group_pool_handle              $group_pool5        \
        -source_pool_handle                                 \
                [list $source_pool1 $source_pool2]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member13 [keylget retMember handle]

# Remove all groups from session5
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           clear_all           \
        -session_handle                 $session5           \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Clear_all:  $retMember"

# ERROR - Delete one group from session5 - the group does not exist anymore
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           delete              \
        -handle                         $group_member11     \
        ]
puts "NOT Delete: $retMember"

# Create session5 group_member8
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session5           \
        -group_pool_handle              $group_pool1        \
        -source_pool_handle                                 \
                [list $source_pool1 $source_pool2]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member8 [keylget retMember handle]

# Create session5 group_member11
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           create              \
        -session_handle                 $session5           \
        -group_pool_handle              $group_pool2        \
        -source_pool_handle                                 \
                [list $source_pool4 $source_pool2]          \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Create:     $retMember"
set group_member11 [keylget retMember handle]

# Delete one groups from session1 and session6
set retMember [::ixia::emulation_igmp_group_config          \
        -mode                           delete              \
        -handle                                             \
                [list $group_member2 $group_member10]       \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Delete:     $retMember"


# Delete session2 and session6
set retMember [::ixia::emulation_igmp_config                \
        -mode                           delete              \
        -handle                                             \
                [list $session2 $session6]                  \
        ]
if {[keylget retMember status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retMember log]"
}
puts "Delete:     $retMember"

return "SUCCESS - $test_name - [clock format [clock seconds]]"
