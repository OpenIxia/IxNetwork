################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-20-2007 Mchakravarthy - created sample
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
#   This sample Configures 5000 IGMP groups and measures the performance 	   #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

################################################################################
# General script variables
################################################################################
set test_name                                   [info script]
set cfgError									0
set chassis_ip									10.205.16.54
set port_list									[list 2/5 2/6]
set ixnetwork_tcl_server						127.0.0.1
set port_count									2
################################################################################
# START - Connect to the chassis
################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect

set connect_status [::ixia::connect                     \
        -reset                                          \
        -device                $chassis_ip              \
        -port_list             $port_list               \
        -username              ixiaApiUser              \
        -ixnetwork_tcl_server  $ixnetwork_tcl_server    \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
	return 0
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
                temp_port]} {
        lappend port_handle $temp_port
    }
}

set i 0
puts "Ixia port handles are:"
foreach port $port_handle {
    set port_$i $port
    puts $port
    incr i
}

puts "End connecting to chassis ..."
update idletasks

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status_0 [::ixia::interface_config        \
        -port_handle                    $port_0		    \
        -autonegotiation                1               \
        -duplex                         full            \
        -speed                          ether1000       \
        ]
if {[keylget interface_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status_0 log]"
	return 0
}

set interface_status_1 [::ixia::interface_config        \
        -port_handle                    $port_1		    \
        -autonegotiation                1               \
        -duplex                         full            \
        -speed                          ether1000       \
        ]
if {[keylget interface_status_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status_1 log]"
	return 0
}
puts "End Interface Config"

##################################################
#  Configure interfaces and create IGMP sessions #
##################################################

set ip_router_alert         1
set intf_ip_addr            100.0.1.2
set neighbor_intf_ip_addr   100.0.1.1
set vlan_id                 10
set vlan_id_step            1
set vlan_user_priority      4

set igmp_status_0 [::ixia::emulation_igmp_config        \
        -port_handle           $port_0		            \
        -mode                  create                   \
        -reset                                          \
        -msg_interval          167                      \
        -igmp_version          v3                       \
        -ip_router_alert       $ip_router_alert         \
        -general_query         0                        \
        -group_query           0                        \
        -filter_mode           exclude                  \
        -count                 1                        \
        -intf_ip_addr          $intf_ip_addr            \
        -neighbor_intf_ip_addr $neighbor_intf_ip_addr   \
        -intf_prefix_len       24                       \
        -vlan_id_mode          increment                \
        -vlan_id               $vlan_id                 \
        -vlan_id_step          $vlan_id_step            \
        -vlan_user_priority    $vlan_user_priority      \
        -no_write                                       \
        ]
if {[keylget igmp_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status_0 log]"
	return 0
}
set session_handle_0 [keylget igmp_status_0 handle]

set igmp_status_1 [::ixia::emulation_igmp_config        \
        -port_handle           $port_1		            \
        -mode                  create                   \
        -reset                                          \
        -msg_interval          167                      \
        -igmp_version          v3                       \
        -ip_router_alert       $ip_router_alert         \
        -general_query         0                        \
        -group_query           0                        \
        -filter_mode           exclude                  \
        -count                 1                        \
        -intf_ip_addr          $neighbor_intf_ip_addr	\
        -neighbor_intf_ip_addr $intf_ip_addr			\
        -intf_prefix_len       24                       \
        -vlan_id_mode          increment                \
        -vlan_id               $vlan_id                 \
        -vlan_id_step          $vlan_id_step            \
        -vlan_user_priority    $vlan_user_priority      \
        -no_write                                       \
        ]
if {[keylget igmp_status_1 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget igmp_status_1 log]"
	return 0
}
set session_handle_1 [keylget igmp_status_1 handle]

############################################################################
# Create multiple IGMP group members and sources and retrieve the timing
############################################################################

proc generate_igmp_groups {gr_ip_add gr_count} {
    set group_list ""
    for {set i 1} {$i<=$gr_count} {incr i} {
        set count [expr $i % 5]
        if {$count==0} {incr count}
        set step [expr $i % 4]
        if {$step==0} {incr step}
        lappend group_list $gr_ip_add/0.0.0.$step/$count
        set gr_ip_add [::ixia::increment_ipv4_address $gr_ip_add]
    }
    return $group_list
}

proc generate_igmp_sources {sr_ip_add gr_count} {
    set source_list ""
    for {set i 1} {$i<=$gr_count} {incr i} {
        set count [expr $i % 5]
        if {$count==0} {incr count}
        set step [expr $i % 4]
        if {$step==0} {incr step}
        set sources_on_group $sr_ip_add/0.0.0.$step/$count
        set num_sources [expr [abs $count-$step]]
        if {$num_sources>0} {
            for {set j 0} {$j<$num_sources} {incr j} {
                set sr_ip_add [::ixia::increment_ipv4_address $sr_ip_add]
                append sources_on_group ",$sr_ip_add/0.0.0.$step/[expr $count+1]"
            }
            set sr_ip_add [::ixia::increment_ipv4_address $sr_ip_add 4 $num_sources]
        } else {
            set sr_ip_add [::ixia::increment_ipv4_address $sr_ip_add]
        }
        lappend source_list $sources_on_group
    }
    return $source_list
}


# Generate IGMP group member params
set gr_count  3000       ;# number of IGMP groups
set gr_ip_add 226.0.1.1 ;# start address for the IGMP groups
set group_list [generate_igmp_groups $gr_ip_add $gr_count]

# Generate IGMP sources params
set sr_ip_add 20.0.1.1 ;# start address for the IGMP sources
set source_list [generate_igmp_sources $sr_ip_add $gr_count]

set ct 0
foreach item $source_list {
    set l [llength [split $item ,]]
    set ct [expr $ct+$l]
}

##################################################
#  Configure IGMP Groups						 #
##################################################

set group_status_0 [::ixia::emulation_igmp_group_config \
        -mode                 create                    \
        -session_handle       $session_handle_0         \
        -group_pool_handle    $group_list               \
        -source_pool_handle   $source_list              \
        -no_write                                       \
        ]
if {[keylget group_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget group_status_0 log]"
	return 0
}


# Get all the Group Handles
set group_handles [keylget group_status_0 handle]

##################################################
# Enable 5000 Groups							 #
##################################################

set start_time_enable [clock clicks -milliseconds]
set group_status_1 [::ixia::emulation_igmp_group_config \
	-mode                     enable					\
	-handle                   $group_handles			\
	]
if {[keylget group_status_1 status] != $::SUCCESS} {
	puts  "FAIL - $test_name - [keylget group_status_1 log]"
	return 0
}
set end_time_enable [clock clicks -milliseconds]
set time_taken_enable  [expr $end_time_enable - $start_time_enable]


puts "Time Taken for enabling 5000 Groups  :  $time_taken_enable"


# Average time taken to enable IGMP groups after 5 runs
set baseLineTime_enable 12000

if {$time_taken_enable > $baseLineTime_enable} {
    puts  "FAIL - Enabling  of IGMP groups took too long"
	return 0
}


##################################################
# disable 5000 Groups							 #
##################################################

set start_time_disable [clock clicks -milliseconds]
set group_status_1 [::ixia::emulation_igmp_group_config \
	-mode                     disable					\
	-handle                   $group_handles			\
	]
if {[keylget group_status_1 status] != $::SUCCESS} {
	puts  "FAIL - $test_name - [keylget group_status_1 log]"
	return 0
}

set end_time_disable [clock clicks -milliseconds]
set time_taken_disable  [expr $end_time_disable - $start_time_disable]

puts "Time Taken for disabling 5000 Groups :  $time_taken_disable"

# Average time taken to enable IGMP groups after 5 runs
set baseLineTime_disable 12000

if {$time_taken_disable > $baseLineTime_disable} {
    puts  "FAIL - Disabling  of IGMP groups took too long"
	return 0
}


puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1