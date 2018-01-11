#################################################################################
# Version 1.0    $Revision: 1 $
# $Author: MHasegan $
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10-17-2006 MHasegan
#
#################################################################################

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
#    This sample creates one IPv4 stream with increasing frame length, varying #
#    the destination and source IP addresses.                                  #
#    The trigger is set on an IP source address and the filter is set to a     #
#    framesize range and a range of IP source and destination addresses.       #
#    The trigger position is set to 10%, the before_trigger_filter is set to   #
#    record all frames in the capture buffer and the after_trigger_filter is   #
#    set to record in the capture buffer only the frames that match the        #
#    filter.                                                                   #
#    Starts the capture then it starts the streams, collects statistics and    #
#    returns the capture buffer in the default filename.                       #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET26.                                      #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester

########
# IpV4 #
########

set ipV4_port_list    "3/1            3/2"
set ipV4_ixia_list    "1.1.1.2        1.1.1.1"
set ipV4_gateway_list "1.1.1.1        1.1.1.2"
set ipV4_netmask_list "255.255.255.0  255.255.255.0"
set ipV4_mac_list     "0000.debb.0001 0000.debb.0002"
set ipV4_version_list "4              4"
set ipV4_autoneg_list "1              1"
set ipV4_duplex_list  "full           full"
set ipV4_speed_list   "ether100       ether100"
set ipV4_port_rx_mode "capture        capture"

#################################################################################
#                              START TEST                                       #
#################################################################################

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect  \
        -reset                     \
        -device    $chassisIP      \
        -port_list $ipV4_port_list \
        -username  ixiaApiUser     ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle_tx [keylget connect_status \
        port_handle.$chassisIP.[lindex $ipV4_port_list 0]]
set port_handle_rx [keylget connect_status \
        port_handle.$chassisIP.[lindex $ipV4_port_list 1]]
set port_handle [list $port_handle_tx $port_handle_rx]

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_handle        \
        -intf_ip_addr    $ipV4_ixia_list     \
        -gateway         $ipV4_gateway_list  \
        -netmask         $ipV4_netmask_list  \
        -autonegotiation $ipV4_autoneg_list  \
        -duplex          $ipV4_duplex_list   \
        -src_mac_addr    $ipV4_mac_list      \
        -speed           $ipV4_speed_list    \
        -port_rx_mode    $ipV4_port_rx_mode  \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

##################################
#  Configure streams on TX port  #
##################################

# Configure the streams on the first IpV4 port
set traffic_status  [::ixia::traffic_config          \
        -mode                      create          \
        -port_handle               $port_handle_tx \
        -l3_protocol               ipv4            \
        -ip_src_addr               12.1.1.1        \
        -ip_src_mode               increment       \
        -ip_src_step               0.0.0.1         \
        -ip_src_count              512             \
        -ip_dst_addr               13.1.1.1        \
        -ip_dst_mode               increment       \
        -ip_dst_step               0.0.0.1         \
        -ip_dst_count              512             \
        -l3_length                 42              \
        -rate_percent              100             \
        -mac_dst_mode              discovery       \
        -length_mode           increment       \
        -frame_size_min           20              \
        -frame_size_max           10000           \
        -frame_size_step       1                  \
        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

set interface_status [::ixia::interface_config  \
        -port_handle     $port_handle_tx        \
        -arp_send_req    1                      ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
if {[catch {set failed_arp [keylget interface_status \
        $port_handle_tx.arp_request_success]}] || $failed_arp == 0} {
        set returnLog "FAIL - $test_name arp send request failed. "
        if {![catch {set intf_list [keylget \
            interface_status $port_handle_tx.arp_ipv4_interfaces_failed]}]} {
            append returnLog "ARP failed on interfaces: $intf_list."
        }
}

# Clear stats before sending traffic
set clear_stats_status [::ixia::traffic_control \
        -port_handle    $port_handle          \
        -action         clear_stats           \
        ]
if {[keylget clear_stats_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget clear_stats_status log]"
}

####################################
#  Configure triggers and filters  #
####################################

set config_status [::ixia::packet_config_buffers \
    -port_handle           $port_handle_rx   \
    -capture_mode          trigger           \
    -before_trigger_filter all               \
    -after_trigger_filter  filter            \
    -trigger_position      10                \
    ]
if {[keylget config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget config_status log]"
}

# Pattern 1 will match the IP source address of a packet.
# The source address is specified with the -pattern1 parameter
# in hex format.
# Since it has no mask, it trigger the capture on the address
# 12.1.1.100

# Pattern2 will match the IP source and destination address of
# a packet.
# The addresses are specified with the use of the -pattern2
# parameter (IpSA is 12.1.2.1 and IpDA is 13.1.2.1).
# The use of pattern mask2 will extend the capture filter to a
# IP source address range {0C 01 02 0*} and destination address
# range {0D 01 02 0*}.
# The filter will capture packets having an IP source address
# from 12.1.2.0 to 12.1.2.15 AND IP destinatino address from
# 13.1.2.0 to 13.1.2.15

set config_status [::ixia::packet_config_filter  \
    -port_handle   $port_handle_rx           \
    -match_type1   IpSAEthernetII            \
    -pattern1      {0C 01 01 64}             \
    -match_type2   IpSADAEthernetII          \
    -pattern2      {0C 01 02 01 0D 01 02 01} \
    -pattern_mask2 {00 00 00 0F 00 00 00 0F} \
    ]
if {[keylget config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget config_status log]"
}

set config_status [::ixia::packet_config_triggers      \
        -port_handle                   $port_handle_rx \
        -capture_trigger           1           \
        -capture_trigger_pattern       pattern1        \
        -capture_filter               1           \
        -capture_filter_pattern        pattern2        \
        -capture_filter_framesize      1               \
        -capture_filter_framesize_from 1300            \
        -capture_filter_framesize_to   1900            \
        ]
if {[keylget config_status status] == $::FAILURE} {
    return "FAIL - $test_name - [keylget config_status log]"
}

#########################
# Start capture on port #
#########################

puts "Starting capture.."

set start_status [::ixia::packet_control \
        -port_handle $port_handle_rx     \
    -action      start               \
    ]
if {[keylget start_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget start_status log]"
}

puts "Capturing...."

#########################
# Start traffic on port #
#########################

set traffic_control_status [::ixia::traffic_control \
        -port_handle $port_handle_tx              \
        -action      run                          ]
if {[keylget traffic_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_control_status log]"
}

after 3000

#########################
# Stop traffic on port  #
#########################
puts "Stopped"

set traffic_control_status [::ixia::traffic_control \
        -port_handle $port_handle_tx              \
        -action      stop                         ]
if {[keylget traffic_control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_control_status log]"
}

set portz [list [list 1 3 1] [list 1 3 2]]
puts "waiting traffic to stop"
ixCheckTransmitDone portz
puts "traffic stopped"

#########################
# Stop capture on port  #
#########################

puts "Stopping capture..."

set stop_status [::ixia::packet_control \
        -port_handle $port_handle_tx    \
    -action      stop            \
    ]
if {[keylget stop_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget stop_status log]"
}

#############################################
# Get capture and statistics to keyed list  #
#############################################
set path [pwd]
set filename test_capture
set absolute_path $path/$filename

set stats_status [::ixia::packet_stats   \
        -port_handle    $port_handle_rx  \
        -format            cap              \
        -filename       $absolute_path   \
    ]
if {[keylget stats_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget stats_status log]"
}

puts "Filepath of exported file: $path"

set frames_no [keylget stats_status $port_handle_rx.aggregate.num_frames]
puts "Captured frames: $frames_no"

return "SUCCESS - $test_name - [clock format [clock seconds]]"
