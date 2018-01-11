################################################################################
# Version 1.0    $Revision: 1 $
# $Author: M Ridichie $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    6-02-2006 MRidichie
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
#    This sample collects the ATM stats.                                       #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM622MR module.                                #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester

########
# IpV4 #
########

set port_list "3/1 3/2"

#################################################################################
#                                START TEST                                     #
#################################################################################

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect  \
        -reset                     \
        -device    $chassisIP      \
        -port_list $port_list \
        -username  ixiaApiUser     ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_one [keylget connect_status \
        port_handle.$chassisIP.[lindex $port_list 0]]
set port_two [keylget connect_status \
        port_handle.$chassisIP.[lindex $port_list 1]]

set port_handle [list $port_one $port_two]
########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_one        \
        -intf_ip_addr    1.1.1.1     \
        -gateway         1.1.1.2  \
        -netmask         255.255.255.0  \
        -atm_enable_coset 1 \
    -atm_enable_pattern_matching 1 \
    -atm_filler_cell idle \
    -atm_interface_type nni \
    -atm_packet_decode_mode cell \
    -atm_reassembly_timeout 111]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set interface_status [::ixia::interface_config \
        -port_handle     $port_two        \
        -intf_ip_addr    1.1.1.2     \
        -gateway         1.1.1.1  \
        -netmask         255.255.255.0  \
        -atm_enable_coset 1 \
    -atm_enable_pattern_matching 1 \
    -atm_filler_cell idle \
    -atm_interface_type nni \
    -atm_packet_decode_mode cell \
    -atm_reassembly_timeout 111]

if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

########################################
# Stream configuration                 #
# IPv4                                 #
########################################
# Delete all the streams first
set traffic_status [::ixia::traffic_config \
        -mode        reset               \
        -port_handle $port_one        ]


set traffic_status [::ixia::traffic_config \
        -mode        reset               \
        -port_handle $port_two        ]


set stream_index_list ""

# Configure first stream on the IpV4 port
set traffic_status [::ixia::traffic_config         \
        -mode         create                     \
        -port_handle  $port_one                  \
        -l3_protocol  ipv4                       \
        -ip_src_addr  1.1.1.1 \
        -ip_dst_addr  1.1.1.2 \
    -rate_percent 50.0                         \
        -l3_length    100                         \
        -vpi          10            \
    -vci          20            \
    -atm_header_aal5error no_error        \
    -atm_header_cell_loss_priority  1    \
    -atm_header_enable_cpcs_length 1    \
    -atm_header_cpcs_length  100  \
    -atm_header_enable_auto_vpi_vci  0    \
    -atm_header_enable_cl  1        \
    -atm_header_encapsulation  llc_routed_clip \
    -atm_header_generic_flow_ctrl  14    \
    -atm_header_hec_errors  0        \
    -atm_counter_vpi_type  fixed        \
    -atm_counter_vci_type  fixed        ]

if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

set traffic_status [::ixia::traffic_config         \
        -mode         create                     \
        -port_handle  $port_two                  \
        -l3_protocol  ipv4                       \
        -ip_src_addr  1.1.1.2 \
        -ip_dst_addr  1.1.1.1 \
    -rate_percent 50.0                         \
        -l3_length    100                         \
        -vpi          10            \
    -vci          20            \
    -atm_header_aal5error no_error        \
    -atm_header_cell_loss_priority  1    \
    -atm_header_enable_cpcs_length 1    \
    -atm_header_cpcs_length  100  \
    -atm_header_enable_auto_vpi_vci  0    \
    -atm_header_enable_cl  1        \
    -atm_header_encapsulation  llc_routed_clip \
    -atm_header_generic_flow_ctrl  14    \
    -atm_header_hec_errors  0        \
    -atm_counter_vpi_type  fixed        \
    -atm_counter_vci_type  fixed        ]

if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

# Clear stats before sending traffic
set clear_stats_status [::ixia::traffic_control \
        -port_handle $port_handle             \
        -action      clear_stats              ]
if {[keylget clear_stats_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget clear_stats_status log]"
}

set traffic_start_status [::ixia::traffic_stats    \
        -port_handle $port_one                  \
        -mode       add_atm_stats               \
    -vpi          10            \
    -vci          20            \
    -atm_counter_vpi_type  fixed        \
    -atm_counter_vci_type  fixed            \
    -atm_reassembly_enable_iptcpudp_checksum  0 \
    -atm_reassembly_enable_ip_qos  0  \
    -atm_reassembly_encapsulation  llc_routed_clip  ]

if {[keylget traffic_start_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_start_status log]"
}

set traffic_start_status [::ixia::traffic_stats    \
        -port_handle $port_two                  \
        -mode       add_atm_stats               \
    -vpi          10            \
    -vci          20            \
    -atm_counter_vpi_type  fixed        \
    -atm_counter_vci_type  fixed            \
    -atm_reassembly_enable_iptcpudp_checksum  0 \
    -atm_reassembly_enable_ip_qos  0  \
    -atm_reassembly_encapsulation  llc_routed_clip  ]

if {[keylget traffic_start_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_start_status log]"
}

# Start the traffic on TX port
set traffic_start_status [::ixia::traffic_control    \
        -port_handle $port_one                  \
        -action      run                        ]
if {[keylget traffic_start_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_start_status log]"
}

set traffic_start_status [::ixia::traffic_control    \
        -port_handle $port_two                  \
        -action      run                        ]
if {[keylget traffic_start_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_start_status log]"
}

# Sleep 5 seconds
ixia_sleep 5000

set traffic_start_status [::ixia::traffic_control    \
        -port_handle $port_one                  \
        -action      stop                        ]
if {[keylget traffic_start_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_start_status log]"
}

set traffic_start_status [::ixia::traffic_control    \
        -port_handle $port_two                  \
        -action      stop                        ]
if {[keylget traffic_start_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_start_status log]"
}

set vpi 10
set vci 20

set aggregate_stats [::ixia::traffic_stats -port_handle $port_one]

if {[keylget aggregate_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggregate_stats log]"
}

puts ""
puts "*************************Port $port_one*************************"
puts ""
puts "Aggregate TX stats on ATM port $port_one: (vpi,vci) = $vpi/$vci"
puts "--------------------------------------------------"
foreach statName [keylkeys aggregate_stats ${port_one}.aggregate.tx.${vpi}.${vci}] {
    puts [format "%31s        %-20s" "$statName" [keylget aggregate_stats ${port_one}.aggregate.tx.${vpi}.${vci}.${statName}]]
}

puts ""
puts "Aggregate RX stats on ATM port $port_one: (vpi,vci) = $vpi/$vci"
puts "--------------------------------------------------"
foreach statName [keylkeys aggregate_stats ${port_one}.aggregate.rx.${vpi}.${vci}] {
    puts [format "%31s        %-20s" "$statName" [keylget aggregate_stats ${port_one}.aggregate.rx.${vpi}.${vci}.${statName}]]
}


set aggregate_stats [::ixia::traffic_stats -port_handle $port_two]

if {[keylget aggregate_stats status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget aggregate_stats log]"
}

puts ""
puts "*************************Port $port_two*************************"
puts ""
puts "Aggregate RX stats on ATM port $port_two: (vpi,vci) = $vpi/$vci"
puts "--------------------------------------------------"
foreach statName [keylkeys aggregate_stats ${port_two}.aggregate.rx.${vpi}.${vci}] {
    puts [format "%31s        %-20s" "$statName" [keylget aggregate_stats ${port_two}.aggregate.rx.${vpi}.${vci}.${statName}]]
}

puts ""
puts "Aggregate TX stats on ATM port $port_two: (vpi,vci) = $vpi/$vci"
puts "--------------------------------------------------"
foreach statName [keylkeys aggregate_stats ${port_two}.aggregate.tx.${vpi}.${vci}] {
    puts [format "%31s        %-20s" "$statName" [keylget aggregate_stats ${port_two}.aggregate.tx.${vpi}.${vci}.${statName}]]
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"


