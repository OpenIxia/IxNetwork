################################################################################
# Version 1.0    $Revision: 1 $
# $Author:  CNICUTAR$
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
# This sample creates a traffic config by sequentially adding headers (using   #
# protocol templates), runs traffic between the 2 ports and gets flow stats    #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET55.                                      #
#                                                                              #
################################################################################

package require Ixia
set test_name [info script]

set chassisIP sylvester
set port_list [list 7/1 7/2]


proc show_stats var {
    set level [expr [info level] - 1]
    foreach key [keylkeys var] {
	if {$key == "status"} {continue}
	set indent [string repeat "    " $level] 
	puts -nonewline $indent 
    if { [regexp field_singleValue $key] == 0 } {
        continue
    }
	if {[catch {keylkeys var $key}]} {
	    puts "$key: [keylget var $key]"
	    continue
	} else {
	    puts $key
	    puts "$indent[string repeat "-" [string length $key]]"
	}
	show_stats [keylget var $key]
    }
}

# Connect to chassis
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
        -reset                                  \
        -ixnetwork_tcl_server   localhost       \
        -device                 $chassisIP      \
        -port_list              $port_list      \
        -username               ixiaApiUser     \
]

set port_handle_tx [keylget connect_status \
        port_handle.$chassisIP.[lindex $port_list 0]]
set port_handle_rx [keylget connect_status \
        port_handle.$chassisIP.[lindex $port_list 1]]
set port_handle [list $port_handle_tx $port_handle_rx]

# Create two b2b interfaces. The ports have to be b2b

set interface_status [::ixia::interface_config           \
        -port_handle            $port_handle_tx          \
        -intf_ip_addr           172.16.31.1              \
        -netmask                255.255.0.0              \
        -src_mac_addr           0000.0000.0001           \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

set interface_status [::ixia::interface_config           \
        -port_handle            $port_handle_rx          \
        -intf_ip_addr           172.16.31.2              \
        -netmask                255.255.0.0              \
        -src_mac_addr           0000.0000.0002           \
]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}


set traffic_status  [::ixia::traffic_config                     \
        -traffic_generator              ixnetwork_540           \
        -mode                           create                  \
        -circuit_type                   raw                     \
        -port_handle                    $port_handle_tx         \
        -port_handle2                   $port_handle_rx         \
        -mac_src                        0000.0000.0001          \
        -mac_dst                        0000.0000.0002          \
        -track_by                       endpoint_pair           \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

set traffic_item [keylget traffic_status traffic_item]
set config_element [keylget traffic_status $traffic_item]
set stream_ids [keylget config_element stream_ids]

set headers [keylget config_element [lindex $stream_ids 0]]
set headers [keylget headers headers]

set eth_header [lindex $headers 0 ]


set available_templates  [::ixia::traffic_config             \
    -traffic_generator      ixnetwork_540                    \
    -mode                   get_available_protocol_templates \
]
if {[keylget available_templates status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget available_templates log]"
    return 0
}

# foreach template [keylget available_templates pt_handle] {
#     puts "$template"
# }

if { [lsearch [keylget available_templates pt_handle] ipv4] == -1 } {
    puts "FAIL - $test_name - ipv4 is not available. Available templates: \
    [keylget available_templates pt_handle]"
}

set traffic_status [::ixia::traffic_config             \
    -mode                   append_header                \
    -traffic_generator      ixnetwork_540                \
    -stream_id              $eth_header                  \
    -pt_handle              ipv4                         \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

set ipv4_header [keylget traffic_status handle]


set available_fields [::ixia::traffic_config             \
    -mode                   get_available_fields         \
    -traffic_generator      ixnetwork_540                \
    -header_handle          $ipv4_header                 \
]
if {[keylget available_fields status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget available_fields log]"
    return 0
}

set src_ip [lindex [keylget available_fields handle] \
           [lsearch -regexp [keylget available_fields handle] "srcIp"]]
set dst_ip [lindex [keylget available_fields handle] \
           [lsearch -regexp [keylget available_fields handle] "dstIp"]]
           

#Get current destination IP
puts "\nGetting current IP configuration"

set get_src_val  [::ixia::traffic_config                     \
        -traffic_generator              ixnetwork_540           \
        -mode                           get_field_values        \
        -header_handle                  $ipv4_header            \
        -field_handle                   $src_ip                 \
]
if {[keylget get_src_val status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget get_src_val log]"
    return 0
}

set get_dst_val  [::ixia::traffic_config                     \
        -traffic_generator              ixnetwork_540           \
        -mode                           get_field_values        \
        -header_handle                  $ipv4_header            \
        -field_handle                   $dst_ip                 \
]
if {[keylget get_dst_val status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget get_dst_val log]"
    return 0
}

puts "Source ip: [keylget get_src_val field_fieldValue]"
puts "Destination ip: [keylget get_dst_val field_fieldValue]"

puts "\nSetting new source IP "

update idletasks

set set_src_val  [::ixia::traffic_config                     \
        -traffic_generator              ixnetwork_540           \
        -mode                           set_field_values        \
        -header_handle                  $ipv4_header            \
        -field_handle                   $src_ip                 \
        -field_singleValue              "172.16.31.1"           \
]
if {[keylget set_src_val status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget set_src_val log]"
    return 0
}

puts "Setting new destination IP "
update idletasks

set set_dst_val  [::ixia::traffic_config                     \
        -traffic_generator              ixnetwork_540           \
        -mode                           set_field_values        \
        -header_handle                  $ipv4_header            \
        -field_handle                   $dst_ip                 \
        -field_singleValue              "172.16.31.2"           \
]
if {[keylget set_dst_val status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget set_dst_val log]"
    return 0
}

puts "\nGetting current IP configuration"

set get_src_val  [::ixia::traffic_config                     \
        -traffic_generator              ixnetwork_540           \
        -mode                           get_field_values        \
        -header_handle                  $ipv4_header            \
        -field_handle                   $src_ip                 \
]
if {[keylget get_src_val status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget get_src_val log]"
    return 0
}

set get_dst_val  [::ixia::traffic_config                     \
        -traffic_generator              ixnetwork_540           \
        -mode                           get_field_values        \
        -header_handle                  $ipv4_header            \
        -field_handle                   $dst_ip                 \
]
if {[keylget get_dst_val status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget get_dst_val log]"
    return 0
}

puts "Source ip: [keylget get_src_val field_fieldValue]"
puts "Destination ip: [keylget get_dst_val field_fieldValue]"
update idletasks


puts "Running traffic.."

################################################################################
# Start the traffic                                                            #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 run                                         \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

#Wait 10 seconds
after 10000


#Get flow stats
set flow_traffic_status [::ixia::traffic_stats                        \
        -mode                   flow                                        \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget flow_traffic_status log]"
    return 0
}

################################################################################
# Stop the traffic                                                             #
################################################################################
set traffic_status [::ixia::traffic_control                                 \
        -action                 stop                                        \
        -traffic_generator      ixnetwork_540                               \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

################################################################################
# Wait for the traffic to stop                                                 #
################################################################################

after 5000

set flow_results [list                                                      \
        "Tx Port"                       tx.port                             \
        "Rx Port"                       rx.port                             \
        "Tx Frames"                     tx.total_pkts                       \
        "Tx Frame Rate"                 tx.total_pkt_rate                   \
        "Rx Frames"                     rx.total_pkts                       \
        "Frames Delta"                  rx.loss_pkts                        \
        "Rx Frame Rate"                 rx.total_pkt_rate                   \
        "Loss %"                        rx.loss_percent                     \
        "Rx Bytes"                      rx.total_pkts_bytes                 \
        "Rx Rate (Bps)"                 rx.total_pkt_byte_rate              \
        "Rx Rate (bps)"                 rx.total_pkt_bit_rate               \
        "Rx Rate (Kbps)"                rx.total_pkt_kbit_rate              \
        "Rx Rate (Mbps)"                rx.total_pkt_mbit_rate              \
        "Avg Latency (ns)"              rx.avg_delay                        \
        "Min Latency (ns)"              rx.min_delay                        \
        "Max Latency (ns)"              rx.max_delay                        \
        "First Timestamp"               rx.first_tstamp                     \
        "Last Timestamp"                rx.last_tstamp                      \
]

set flows [keylget flow_traffic_status flow]
foreach flow [keylkeys flows] {
    set flow_key [keylget flow_traffic_status flow.$flow]
    puts "\tFlow $flow: [keylget flow_traffic_status flow.$flow.flow_name]"
    foreach {name key} [subst $[subst flow_results]] {
        puts "\t\t$name: [keylget flow_traffic_status flow.$flow.$key]"
    }
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1