################################################################################
# Version 1.0    $Revision: 1 $
# $Author:  cnicutar$
#
#    Copyright © 1997 - 2009 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    4-25-2009
#
# Description:
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
# This sample creates a traffic item using circuit_type quick_flows and udf    #
# parameters and the runs traffic between the 2 ports and prints flow stats    #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET55.                                      #
#                                                                              #
################################################################################

package require Ixia

proc print_flow_stats {flow_traffic_status} {
    set flow_results [list                                                  \
        "Tx Frames"                     tx.total_pkts                       \
        "Rx Frames"                     rx.total_pkts                       \
        "Tx pkt_rate"                   tx.total_pkt_rate                   \
        "Loss %"                        rx.loss_percent                     \
    ]

    set flows [keylget flow_traffic_status flow]
    foreach flow [keylkeys flows] {
        set flow_key [keylget flow_traffic_status flow.$flow]
        puts "\tFlow $flow"
        foreach {name key} [subst $[subst flow_results]] {
            puts "\t\t$name: [keylget flow_traffic_status flow.$flow.$key]"
        }
    }
}

set test_name [info script]

set chassisIP sylvester

########
# IpV4 #
########
set ipV4_port_list    "7/1            7/2"
set ipV4_ixia_list    "1.1.1.2        1.1.1.1"
set ipV4_gateway_list "1.1.1.1        1.1.1.2"
set ipV4_netmask_list "255.255.255.0  255.255.255.0"
set ipV4_mac_list     "0000.0000.0001 0000.0000.0002"
set ipV4_version_list "4              4"
set ipV4_autoneg_list "0              0"
set ipV4_duplex_list  "full           full"
set ipV4_speed_list   "ether100       ether100"

set file_name "ip_flows_test_results.txt"

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                 \
        -reset                                      \
        -ixnetwork_tcl_server       localhost       \
        -device                     $chassisIP      \
        -port_list                  $ipV4_port_list \
        -username                   ixiaApiUser     ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle_tx [keylget connect_status \
        port_handle.$chassisIP.[lindex $ipV4_port_list 0]]
set port_handle_rx [keylget connect_status \
        port_handle.$chassisIP.[lindex $ipV4_port_list 1]]
set port_handle_list [list $port_handle_tx $port_handle_rx]

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle_list   \
        -intf_ip_addr    $ipV4_ixia_list     \
        -gateway         $ipV4_gateway_list  \
        -netmask         $ipV4_netmask_list  \
        -autonegotiation $ipV4_autoneg_list  \
        -duplex          $ipV4_duplex_list   \
        -src_mac_addr    $ipV4_mac_list      \
        -speed           $ipV4_speed_list    ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

##################################
#  Configure streams on TX port  #
##################################
set flow_count 10

# Configure the streams on the first IpV4 port
set traffic_status1 [::ixia::traffic_config        \
        -traffic_generator         ixnetwork_540   \
        -mode                      create          \
        -circuit_type              quick_flows     \
        -port_handle               $port_handle_tx \
        -port_handle2              $port_handle_rx \
        -l3_protocol               ipv4            \
        -ip_src_addr               1.1.1.1         \
        -ip_src_mode               fixed           \
        -ip_dst_addr               1.1.1.2         \
        -ip_dst_mode               increment       \
        -ip_dst_step               0.0.0.1         \
        -ip_dst_count              $flow_count     \
        -l3_length                 46              \
        -rate_percent              100             \
        -mac_dst_mode              discovery       \
        -enable_udf4               1               \
        -udf4_mode                 nested          \
        -udf4_offset               26              \
        -udf4_counter_type         32              \
        -udf4_counter_init_value   12.1.1.1        \
        -udf4_counter_step         1               \
        -udf4_counter_mode         count           \
        -udf4_counter_repeat_count $flow_count     \
        -udf4_inner_repeat_value   $flow_count     \
        -udf4_inner_repeat_count   $flow_count     \
        -udf4_inner_step           1               \
        -enable_udf3               1               \
        -udf3_mode                 counter         \
        -udf3_offset               52              \
        -udf3_counter_type         16              \
        -udf3_counter_init_value   1               \
        -udf3_counter_repeat_count [mpexpr $flow_count * $flow_count] \
        -udf3_counter_step         1               \
        -udf3_counter_mode         count           \
        -track_by                  dest_endpoint]
if {[keylget traffic_status1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status1 log]"
}


#########################
# Start traffic on port #
#########################
# Clear stats before sending traffic
set clear_stats_status [::ixia::traffic_control \
        -traffic_generator         ixnetwork_540   \
        -port_handle $port_handle_list        \
        -action      clear_stats              ]
if {[keylget clear_stats_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget clear_stats_status log]"
}

set traffic_control_status [::ixia::traffic_control \
        -traffic_generator         ixnetwork_540   \
        -port_handle $port_handle_tx              \
        -action      run                          ]
if {[keylget traffic_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_control_status log]"
}


ixia_sleep 10000

############################################
# Get traffic statistics for all the PGIDs #
############################################
set flow_statistics_list [::ixia::traffic_stats     \
        -traffic_generator         ixnetwork_540    \
        -mode               flow                    \
    ]
if {[keylget flow_statistics_list status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget flow_statistics_list log]"
}

########################
# Stop traffic on port #
########################
set traffic_control_status [::ixia::traffic_control \
        -traffic_generator         ixnetwork_540   \
        -port_handle $port_handle_tx              \
        -action      stop                         ]
if {[keylget traffic_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_control_status log]"
}

print_flow_stats $flow_statistics_list
update idletasks

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1