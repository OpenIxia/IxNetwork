################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Radu Antonescu
#
#    Copyright © 1997 - 2005 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    4-27-2005 T.Kong - added the latency bin stats.
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
#    This sample creates two IPv4 streams. Packet group ids are 10 for first   #
#    stream and 20 for second. Statistics for PGID 10,15 and 20 are retrived.  #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#    The sample was tested with HLTSET26.                                      #
#                                                                              #
################################################################################

package req Ixia
set test_name [info script]

set chassisIP 127.0.0.1
set port_list [list 2/1 2/2]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                    \
        -device    $chassisIP     \
        -port_list $port_list     \
        -username  ixiaApiUser    ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_handle_list [keylget connect_status port_handle.$chassisIP]

set port_tx [lindex $port_handle_list 0 1]
set port_rx [lindex $port_handle_list 1 1]

########################################
# Configure interface in the test      #
# IPv4                                 #
########################################
set interface_status [::ixia::interface_config \
        -port_handle     [list $port_tx $port_tx] \
        -intf_ip_addr    [list 12.1.1.1 11.1.1.1] \
        -gateway         [list 12.1.1.2 11.1.1.2] \
        -netmask         [list 255.255.255.0 255.255.255.0] \
        -autonegotiation [list 1 1 ] \
        -src_mac_addr    [list 0000.0005.0001 0000.0005.0002] \
        -port_rx_mode    [list wide_packet_group wide_packet_group]   ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

# Delete all the streams first
set traffic_status [::ixia::traffic_config \
        -mode        reset               \
        -port_handle $port_tx        ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

# Configure first stream
set traffic_status1 [::ixia::traffic_config \
        -mode         create              \
        -port_handle  $port_tx            \
        -l3_protocol  ipv4                \
        -ip_src_addr  12.1.1.1            \
        -ip_dst_addr  12.1.1.2            \
        -l3_length    128                 \
        -rate_percent 20                  \
        -mac_dst_mode discovery           \
        -enable_pgid  1                   \
        -frame_size   541                 \
        -signature    "AB AC BC DE"       \
        -signature_offset 52              \
        -pgid_value    10                 \
             ]
if {[keylget traffic_status1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status1 log]"
}

# Configure second stream
set traffic_status2 [::ixia::traffic_config \
        -mode         create              \
        -port_handle  $port_tx            \
        -l3_protocol  ipv4                \
        -ip_src_addr  11.1.1.1            \
        -ip_dst_addr  11.1.1.2            \
        -l3_length    128                 \
        -rate_percent 25                  \
        -mac_dst_mode discovery           \
        -enable_pgid  1                   \
        -frame_size   541                 \
        -signature    "AB AC BC DE"       \
        -signature_offset 52              \
        -pgid_value    20                 \
             ]
if {[keylget traffic_status1 status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status1 log]"
}

# Prepare second port for statistics
set interface_status [::ixia::interface_config \
        -port_handle   $port_rx $port_rx \
        -mode           config            \
        -autonegotiation  1               \
        -src_mac_addr   00:01:02:03:04:05 \
        -pgid_mask      0000 \
        -pgid_offset    56 \
        -port_rx_mode   wide_packet_group \
        -signature      AB:AC:BC:DE \
        -intf_ip_addr    [list 12.1.1.2 11.1.1.2] \
        -gateway         [list 12.1.1.1 11.1.1.1] \
        -netmask         [list 255.255.255.0 255.255.255.0] \
        -signature_offset 52 ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status1 log]"
}

set interface_status [::ixia::interface_config  \
        -port_handle     $port_tx               \
        -arp_send_req    1                      ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
if {[catch {set failed_arp [keylget interface_status \
        $port_tx.arp_request_success]}] || $failed_arp == 0} {
    set returnLog "FAIL - $test_name arp send request failed. "
    if {![catch {set intf_list [keylget interface_status \
            $port_tx.arp_ipv4_interfaces_failed]}]} {
        append returnLog "ARP failed on interfaces: $intf_list."
    }
    return $returnLog
}

# Clear statistics on second port
set traffic_status [::ixia::traffic_control \
        -action         clear_stats \
        -port_handle    $port_rx]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status1 log]"
}

# Start traffic on first port
set traffic_status [::ixia::traffic_control \
        -action         run \
        -port_handle    $port_tx]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status1 log]"
}

# Retrive statistics for PGID between 0 and 20
set traffic_stats_status [::ixia::traffic_stats \
        -port_handle $port_rx \
        -packet_group_id 20 \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status1 log]"
}

# Display results
set pgid10_frame_rate [keylget traffic_stats_status $port_rx.pgid.rx.frame_rate.10]
set pgid20_frame_rate [keylget traffic_stats_status $port_rx.pgid.rx.frame_rate.20]
set pgid15_frame_rate [keylget traffic_stats_status $port_rx.pgid.rx.frame_rate.15]

puts "frame rate for pgid 10 = $pgid10_frame_rate"
puts "frame rate for pgid 15 = $pgid15_frame_rate - this should be 0"
puts "frame rate for pgid 20 = $pgid20_frame_rate"

return "SUCCESS - $test_name - [clock format [clock seconds]]"
