################################################################################
# Version 1.0 $
# $Author: cnicutar $
#
#    Copyright © 1997 - 2009 by IXIA
#    All Rights Reserved.
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
#    This sample creates two IPv4 VLAN streams, starts the streams and         #
#    displays latency statistics.                                              #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester

########
# IpV4 #
########
set ipV4_port_list    "3/3            3/4"
set ipV4_autoneg_list "1              1"
set ipV4_duplex_list  "auto           auto"
set ipV4_speed_list   "auto           auto"
set ipV4_mac_list     "0000.debb.0001 0000.debb.0002"
set ipV4_vlan_list    "1              1"
set ipV4_vlan_id_list "100            100"
set ipV4_version_list "4              4"
set ipV4_ixia_list    "1.1.1.2        1.1.1.1"
set ipV4_gateway_list "1.1.1.1        1.1.1.2"
set ipV4_netmask_list "255.255.255.0  255.255.255.0"


#################################################################################
#                              START TEST                                       #
#################################################################################

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
        -reset                                  \
        -ixnetwork_tcl_server   localhost       \
        -device                 $chassisIP      \
        -port_list              $ipV4_port_list \
        -username               ixiaApiUser     ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_array [keylget connect_status port_handle.$chassisIP]

set port_0 [keylget port_array [lindex $ipV4_port_list 0]]
set port_1 [keylget port_array [lindex $ipV4_port_list 1]]

set port_handle [list $port_0 $port_1]

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -autonegotiation $ipV4_autoneg_list  \
        -duplex          $ipV4_duplex_list   \
        -speed           $ipV4_speed_list    \
        -src_mac_addr    $ipV4_mac_list      \
        -vlan            $ipV4_vlan_list     \
        -vlan_id         $ipV4_vlan_id_list  \
        -intf_ip_addr    $ipV4_ixia_list     \
        -gateway         $ipV4_gateway_list  \
        -netmask         $ipV4_netmask_list  \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set vlan_number       1

# Configure the streams on the first IpV4 port

set traffic_status  [::ixia::traffic_config          \
        -traffic_generator         ixnetwork_540   \
        -mode                      create          \
        -port_handle               $port_0         \
        -port_handle2              $port_1         \
        -l3_protocol               ipv4            \
        -ip_src_addr               1.1.1.2         \
        -ip_src_mode               increment       \
        -ip_src_step               0.0.0.1         \
        -ip_src_count              $vlan_number    \
        -ip_dst_addr               1.1.1.1         \
        -ip_dst_mode               increment       \
        -ip_dst_step               0.0.0.1         \
        -ip_dst_count              $vlan_number    \
        -rate_percent              25              \
        -mac_src                   0000.debb.0001  \
        -mac_dst                   0000.debb.0002  \
        -vlan                      enable          \
        -vlan_id_mode              increment       \
        -vlan_id                   100             \
        -vlan_id_count             $vlan_number    \
        -vlan_id_step              2               \
        -track_by                  endpoint_pair   \
        ]

if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

set stream_id_list [keylget traffic_status stream_id]


set traffic_status  [::ixia::traffic_config          \
        -traffic_generator         ixnetwork_540   \
        -mode                      create          \
        -port_handle               $port_0         \
        -port_handle2              $port_1         \
        -l3_protocol               ipv4            \
        -ip_src_addr               1.1.1.1         \
        -ip_src_mode               increment       \
        -ip_src_step               0.0.0.1         \
        -ip_src_count              $vlan_number    \
        -ip_dst_addr               1.1.1.2         \
        -ip_dst_mode               increment       \
        -ip_dst_step               0.0.0.1         \
        -ip_dst_count              $vlan_number    \
        -rate_percent              25              \
        -mac_src                   0000.debb.0002  \
        -mac_dst                   0000.debb.0001  \
        -vlan                      enable          \
        -vlan_id_mode              increment       \
        -vlan_id                   100             \
        -vlan_id_count             $vlan_number    \
        -vlan_id_step              2               \
        -track_by                  endpoint_pair   \
        ]

if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}


lappend stream_id_list [keylget traffic_status stream_id]
set number_of_streams [llength $stream_id_list]
set number_of_bins  3

set clear_stats_status [::ixia::traffic_control  \
        -port_handle    $port_handle             \
        -action         clear_stats              \
        -traffic_generator      ixnetwork_540    \
        -latency_bins   $number_of_bins          \
        -latency_values 2 3.45 ]
if {[keylget clear_stats_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget clear_stats_status log]"
}


set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork_540                               \
]

if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_control_status log]"
}

after 10000



set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_control_status log]"
}

after 5000
set pgid_statistics_list [::ixia::traffic_stats          \
        -traffic_generator         ixnetwork_540    \
        -mode                      stream           \
]
if {[keylget pgid_statistics_list status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget pgid_statistics_list log]"
}

puts  "\n"
puts  "+---------------------------------------------------------------+"
puts  "+                       Statistic Results                       +"
puts  "+---------------------------------------------------------------+"
puts  "+ Time                   : [clock format [clock seconds]]"
puts  "+ Number of Streams      : $number_of_streams"
puts  "+ Number of Latency Bins : $number_of_bins"
puts  "+ Note                   : Latency values are in nsec"
puts  "+---------------------------------------------------------------+"
puts  [format "%20s  %8s  %16s  %16s  %9s  %8s  %8s" \
        Stream Bin# FirstTS LastTS MaxLat MinLat TotalPackets]

 
for {set stream_index 0} {$stream_index < $number_of_streams} {incr stream_index} { 
    set stream_id [lindex $stream_id_list $stream_index]
    for {set l 1} {$l <= $number_of_bins} {incr l} {

        puts  [format "%20s  %8d  %15s  %15s  %8.1f  %8.1f  %8d" $stream_id   $l    \
            [keylget pgid_statistics_list \
       $port_1.stream.$stream_id.rx.latency_bin.$l.first_tstamp] \
            [keylget pgid_statistics_list \
       $port_1.stream.$stream_id.rx.latency_bin.$l.last_tstamp] \
            [keylget pgid_statistics_list \
       $port_1.stream.$stream_id.rx.latency_bin.$l.max] \
            [keylget pgid_statistics_list \
       $port_1.stream.$stream_id.rx.latency_bin.$l.min] \
            [keylget pgid_statistics_list \
       $port_1.stream.$stream_id.rx.latency_bin.$l.total_pkts] \
            [keylget pgid_statistics_list ]]
    }
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
