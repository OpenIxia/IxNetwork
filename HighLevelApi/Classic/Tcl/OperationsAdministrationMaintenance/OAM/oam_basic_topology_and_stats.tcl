################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mircea Hasegan $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    02-23-2009 Mircea Hasegan
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
#    This sample creates a BACK-TO-BACK setup using the IxNetwork              #
#    implementation of Ethernet OAM.                                           #
#                                                                              #
#    It configures two Ethernet OAM Bridges, one on each Ixia port.            #
#    Each OAM Bridge will have 20 Maintenance Points configured on Maintenance #
#    Domain Level 7.                                                           #
#    The protocol is started and statistics are gathered.                      #
#                                                                              #
#    Topology:                                                                 #
#                                                                              #
#    MEP1  ___                                                    _____MEP21  #
#    MEP2  _  \                                                  / _____Mep22  #
#    .      \  \                                                / /       .    #
#    .       -----OAMBridge1--IxiaPort1--IxiaPort2--OAMBridge2----        .    #
#    MEP20  __/                                                  \______Mep41  #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################


proc printStats {keyedList} {
    set statsList {
        aggregate.topology_stats.total_maintenance_points
        aggregate.topology_stats.operational_maintenance_points
        aggregate.topology_stats.total_entries
        aggregate.topology_stats.start_entries
        aggregate.topology_stats.ok_entries
        aggregate.topology_stats.fail_entries
        aggregate.topology_stats.ma_configured
        aggregate.topology_stats.ma_running
        aggregate.topology_stats.remote_meps
        aggregate.topology_stats.rmeps_defective
        aggregate.topology_stats.rmep_error_no_defect
        aggregate.topology_stats.mep_fng_reset
        aggregate.topology_stats.mep_fng_defect
        aggregate.topology_stats.mep_fng_defect_reported
        aggregate.topology_stats.mep_fng_defect_clearing
    }
    
    puts "Statistics for Port Handle [keylget keyedList port_handle]:"
    foreach statKey $statsList {
        set stat_value [keylget keyedList $statKey]
        puts "\t[format {%-65s%-40s} $statKey $stat_value]"
        
        if {$stat_value == "" || $stat_value == "N/A"} {
            puts "Statistics issue: $statKey is $stat_value"
        }
    }
    puts "\n\n"
}

set env(IXIA_VERSION) HLTSET47

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 2/3 2/4]


# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                 \
        -reset                                      \
        -ixnetwork_tcl_server       localhost       \
        -device                     $chassisIP      \
        -port_list                  $port_list      \
        -username  ixiaApiUser                      ]
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

set port_0 [lindex $port_handle 0]
set port_1 [lindex $port_handle 1]

puts "Ixia port handles are $port_handle "

set interface_status [::ixia::interface_config \
        -port_handle      $port_0     \
        -mode             config               \
        -speed            auto                 \
        -duplex           auto                 \
        -phy_mode         copper               \
        -autonegotiation  1                    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
    
}


set interface_status [::ixia::interface_config \
        -port_handle      $port_1     \
        -mode             config               \
        -speed            auto                 \
        -duplex           auto                 \
        -phy_mode         copper               \
        -autonegotiation  1                    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
    
}

#
# Reset any OAM topology that may exist on port_0
#
set oam_topology_status [::ixia::emulation_oam_config_topology                  \
         -mode                        reset                                     \
         -port_handle                 $port_0                                   \
    ]
if {[keylget oam_topology_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget oam_topology_status log]"
    
}

#
# Create HUB and Spoke topology on port_0
#
set oam_topology_status [::ixia::emulation_oam_config_topology                  \
         -mode                        create                                    \
         -port_handle                 $port_0                                   \
         -count                       1                                         \
         -encap                       ethernet_ii                               \
         -mac_local                   00:00:00:10:00:0A                         \
         -mac_local_incr_mode         increment                                 \
         -vlan_id                     10                                        \
         -vlan_id_step                1                                         \
         -continuity_check                                                      \
         -fault_alarm_signal                                                    \
         -domain_level                level0                                    \
         -md_level                    2                                         \
         -short_ma_name_format        integer                                   \
         -short_ma_name_value         0                                         \
         -short_ma_name_step          0                                         \
         -mip_count                   0                                         \
         -mep_count                   20                                        \
         -mep_id                      1                                         \
         -mep_id_incr_mode            increment                                 \
    ]
if {[keylget oam_topology_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget oam_topology_status log]"
    
}

#
# Reset any OAM topology that may exist on port_1
#
set oam_topology_status [::ixia::emulation_oam_config_topology                  \
         -mode                        reset                                     \
         -port_handle                 $port_1                                   \
    ]
if {[keylget oam_topology_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget oam_topology_status log]"
    
}

#
# Create HUB and Spoke topology on port_1
#
set oam_topology_status [::ixia::emulation_oam_config_topology                  \
         -mode                        create                                    \
         -port_handle                 $port_1                                   \
         -count                       1                                         \
         -encap                       ethernet_ii                               \
         -mac_local                   00:00:10:10:00:0A                         \
         -mac_local_incr_mode         increment                                 \
         -vlan_id                     10                                        \
         -vlan_id_step                1                                         \
         -continuity_check                                                      \
         -fault_alarm_signal                                                    \
         -domain_level                level0                                    \
         -md_level                    2                                         \
         -short_ma_name_format        integer                                   \
         -short_ma_name_value         0                                         \
         -short_ma_name_step          0                                         \
         -mip_count                   0                                         \
         -mep_count                   20                                        \
         -mep_id                      21                                        \
         -mep_id_incr_mode            increment                                 \
    ]
if {[keylget oam_topology_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget oam_topology_status log]"
    
}

#
# Reset all OAM messages from all Maintenance Points on port_0
#
set retCode [::ixia::emulation_oam_config_msg                                   \
	 -mode                        reset                                         \
     -handle                      $port_0                                       \
    ]

if {[keylget retCode status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retCode log]"
    
}

#
# Reset all OAM messages from all Maintenance Points on port_1
#
set retCode [::ixia::emulation_oam_config_msg                                   \
	 -mode                        reset                                         \
     -handle                      $port_1                                       \
    ]

if {[keylget retCode status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retCode log]"
    
}


#
# Configure Linktrace messages on port_0
#
set retCode [::ixia::emulation_oam_config_msg                                   \
	 -mode                        create                                        \
     -port_handle                 $port_0                                       \
     -msg_type                    linktrace                                     \
     -mep_id                      1                                             \
     -mep_id_incr_mode            list                                          \
     -mep_id_list                 "all"                                         \
     -renew_test_msgs                                                           \
    ]

if {[keylget retCode status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retCode log]"
    
}

#
# Configure Loopback messages on port_1
#
set retCode [::ixia::emulation_oam_config_msg                                   \
	 -mode                        create                                        \
     -port_handle                 $port_1                                       \
     -msg_type                    loopback                                      \
     -mep_id                      1                                             \
     -mep_id_incr_mode            list                                          \
     -mep_id_list                 "all"                                         \
     -mac_remote_incr_mode        list                                          \
     -mac_remote_list             "all"                                         \
     -renew_test_msgs                                                           \
    ]

if {[keylget retCode status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retCode log]"
    
}

#
# Start OAM protocol on both ports
#
set oam_ctrl_status [::ixia::emulation_oam_control                              \
        -action                         start                                   \
        -port_handle                    [list $port_0 $port_1]                  \
    ]
if {[keylget oam_ctrl_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget oam_ctrl_status log]"
    
}

#
# Get Aggregate Topology statistics
#
set retCode [::ixia::emulation_oam_info \
        -mode aggregate                 \
        -action get_topology_stats      \
        -port_handle $port_0            ]
if {[keylget retCode status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retCode log]"
    
}

puts "Aggregate Topology stats on port $port_0"
keylset retCode port_handle $port_0
printStats $retCode

#
# Get Aggregate Topology statistics
#
set retCode [::ixia::emulation_oam_info \
        -mode aggregate                 \
        -action get_topology_stats      \
        -port_handle $port_1            ]
if {[keylget retCode status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retCode log]"
    
}
puts "Aggregate Topology stats on port $port_1"
keylset retCode port_handle $port_1
printStats $retCode


#
# Get Aggregate Message statistics
#
set retCode [::ixia::emulation_oam_info \
        -mode aggregate                 \
        -action get_message_stats      \
        -port_handle $port_0            ]
if {[keylget retCode status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retCode log]"
    
}

# printStats $retCode
puts "Aggregate Message stats on port $port_0"
puts "\tRX:"
foreach key [keylkeys retCode aggregate.rx] {
    puts [format {%-8s%-16s%s} "" $key [keylget retCode aggregate.rx.$key]]
}

puts "\tTX:"
foreach key [keylkeys retCode aggregate.tx] {
    puts [format {%-8s%-16s%s} "" $key [keylget retCode aggregate.tx.$key]]
}


#
# Get Aggregate Message statistics
#
set retCode [::ixia::emulation_oam_info \
        -mode aggregate                 \
        -action get_message_stats      \
        -port_handle $port_1            ]
if {[keylget retCode status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retCode log]"
    
}

puts "Aggregate Message stats on port $port_1"
puts "\tRX:"
foreach key [keylkeys retCode aggregate.rx] {
    puts [format {%-8s%-16s%s} "" $key [keylget retCode aggregate.rx.$key]]
}

puts "\tTX:"
foreach key [keylkeys retCode aggregate.tx] {
    puts [format {%-8s%-16s%s} "" $key [keylget retCode aggregate.tx.$key]]
}


#
# Get Session Topology statistics
#
set retCode [::ixia::emulation_oam_info \
        -mode session                 \
        -action get_topology_stats      \
        -port_handle $port_0            ]
if {[keylget retCode status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retCode log]"
    
}

puts "Session Topology stats on port $port_0"
# md_level.$md_level.mac.$mac
foreach md_level [keylkeys retCode md_level] {
    puts "\tMD Level $md_level"
    foreach mac_addr [keylkeys retCode md_level.$md_level.mac] {
        puts "\t\tMAC Address $mac_addr"
        foreach key [keylkeys retCode md_level.$md_level.mac.$mac_addr] {
            puts [format {%-24s%-16s%s} "" "$key " [keylget retCode md_level.$md_level.mac.$mac_addr.$key]]
        }
    }
}

#
# Get Session Topology statistics
#
set retCode [::ixia::emulation_oam_info \
        -mode session                 \
        -action get_topology_stats      \
        -port_handle $port_1            ]
if {[keylget retCode status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retCode log]"
    
}

puts "Session Topology stats on port $port_1"
# md_level.$md_level.mac.$mac
foreach md_level [keylkeys retCode md_level] {
    puts "\tMD Level $md_level"
    foreach mac_addr [keylkeys retCode md_level.$md_level.mac] {
        puts "\t\tMAC Address $mac_addr"
        foreach key [keylkeys retCode md_level.$md_level.mac.$mac_addr] {
            puts [format {%-24s%-16s%s} "" "$key " [keylget retCode md_level.$md_level.mac.$mac_addr.$key]]
        }
    }
}


#
# Get Session Message statistics
#
set retCode [::ixia::emulation_oam_info \
        -mode session                 \
        -action get_message_stats      \
        -port_handle $port_0            ]
if {[keylget retCode status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retCode log]"
    
}

puts "Session Message stats on port $port_0"
puts "\tLinktrace statistics:"
# md_level.$md_level.mac.$mac
foreach stat_key [keylkeys retCode linktrace] {
    puts [format {%-16s%-16s%s} "" "$stat_key " [keylget retCode linktrace.$stat_key]]
}
puts "\tLoopback statistics:"
# md_level.$md_level.mac.$mac
foreach stat_key [keylkeys retCode loopback] {
    puts [format {%-16s%-16s%s} "" "$stat_key " [keylget retCode loopback.$stat_key]]
}

#
# Get Session Message statistics
#
set retCode [::ixia::emulation_oam_info \
        -mode session                 \
        -action get_message_stats      \
        -port_handle $port_1            ]
if {[keylget retCode status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget retCode log]"
    
}

puts "Session Message stats on port $port_1"
puts "\tLinktrace statistics:"
# md_level.$md_level.mac.$mac
foreach stat_key [keylkeys retCode linktrace] {
    puts [format {%-16s%-16s%s} "" "$stat_key " [keylget retCode linktrace.$stat_key]]
}
puts "\tLoopback statistics:"
# md_level.$md_level.mac.$mac
foreach stat_key [keylkeys retCode loopback] {
    puts [format {%-16s%-16s%s} "" "$stat_key " [keylget retCode loopback.$stat_key]]
}

#
# Stop OAM Protocol
#
set oam_ctrl_status [::ixia::emulation_oam_control                              \
        -action                         stop                                    \
        -port_handle                    [list $port_0 $port_1]                  \
    ]
if {[keylget oam_ctrl_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget oam_ctrl_status log]"
    
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"