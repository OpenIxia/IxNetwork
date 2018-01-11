################################################################################
# Version 1.0    $Revision: 1 $
# $Author: AEnache $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-18-2006 AEnache
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
#    This sample configures two ipv4 ports and a traffic item with tcp         #
#    as a L4 protocol.                                                         #
#    This is an advanced config showing all possible params related to tcp.    #
#    The traffic is routed through a DUT with the configuration below.         #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10/100/1000 STXS4-256Mb module.                #
#    Using HLTSET76                                                            #
#                                                                              #
################################################################################

################################################################################
#  DUT configuration example:
#    default interface fa5/0
#    int fa5/0
#    ip address 12.1.1.1 255.255.255.0
#    no shutdown
#    exit
#    default interface fa6/0
#    int fa6/0
#    ip address 12.1.2.1 255.255.255.0
#    no shutdown
#    exit
################################################################################  

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 10/3 10/4]

################################################################################
# Connect to the chassis
################################################################################
puts "Start connecting to chassis ..."

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
        -reset                                  \
        -ixnetwork_tcl_server   localhost       \
        -device                 $chassisIP      \
        -port_list              $port_list      \
        -username               ixiaApiUser     ]
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

set i 0
puts "Ixia port handles are:"
foreach port $port_handle {
    set port_$i $port
    puts $port

    incr i
}
puts "End connecting to chassis ..."

################################################################################
# Interface configuration - L1
################################################################################
puts "Start interface configuration L1 ..."

foreach port $port_handle {
    set interface_status [::ixia::interface_config                             \
            -port_handle      $port                                            \
            -mode             config                                           \
            -intf_mode        ethernet                                         \
            -autonegotiation  1                                                \
            -speed            auto                                             \
            -duplex           auto                                             \
            -phy_mode         copper                                           \
            ]
    if {[keylget interface_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget interface_status log]"
        return 0
    }
}

puts "End interface configuration L1 ..."

################################################################################
# Interface configuration L2/3
################################################################################

set interface_status [::ixia::interface_config \
        -port_handle        $port_0     \
        -mode               modify          \
        -intf_ip_addr       12.1.1.2         \
        -gateway            12.1.1.1         \
        -netmask            255.255.255.0    \
        -src_mac_addr       0000.0005.0001   \
        -op_mode            normal           \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}
set intf0 [keylget interface_status interface_handle]
puts "OK - Interface $intf0 created"
set interface_status [::ixia::interface_config \
        -port_handle        $port_1     \
        -mode               modify           \
        -intf_ip_addr       12.1.2.2         \
        -gateway            12.1.2.1         \
        -netmask            255.255.255.0    \
        -src_mac_addr       0000.0005.0001   \
        -op_mode            normal           \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return 0
}
set intf1 [keylget interface_status interface_handle]
puts "OK - Interface $intf1 created"

################################################################################
# Configure traffic item               
################################################################################

# Delete all the streams first
foreach port $port_handle {
    set traffic_status [::ixia::traffic_config \
            -traffic_generator ixnetwork_540   \
            -mode        reset               \
            -port_handle $port        ]
    if {[keylget traffic_status status] != $::SUCCESS} {
        return "FAIL - $test_name - [keylget traffic_status log]"
    }
}

puts "\nCreating traffic streams..."

set tcp_ack_flag_list                [list 0 1 1]
set tcp_ack_flag_mode_list           [list fixed fixed fixed]
set tcp_ack_flag_tracking_list       [list 0 1 1]

set tcp_ack_num_list                 [list 1 4 65534]
set tcp_ack_num_count_list           [list 3 4 10]
set tcp_ack_num_mode_list            [list fixed incr decr]
set tcp_ack_num_step_list            [list 1 4 65534]
set tcp_ack_num_tracking_list        [list 0 1 0]

set tcp_checksum_list                [list 1 a1 11]
set tcp_checksum_count_list          [list 2 3 10]
set tcp_checksum_mode_list           [list fixed incr decr]
set tcp_checksum_step_list           [list 11 a d3]
set tcp_checksum_tracking_list       [list 0 1 1]

set tcp_cwr_flag_list                [list 0 1 1]
set tcp_cwr_flag_mode_list           [list fixed fixed fixed]
set tcp_cwr_flag_tracking_list       [list 0 1 1]

set tcp_data_offset_list             [list 0 4 15]
set tcp_data_offset_count_list       [list 3 1 2]
set tcp_data_offset_mode_list        [list fixed incr decr]
set tcp_data_offset_step_list        [list 1 3 4]
set tcp_data_offset_tracking_list    [list 0 1 1]

set tcp_dst_port_list                [list 20 80 65534]
set tcp_dst_port_count_list          [list 2 8 5]
set tcp_dst_port_mode_list           [list fixed incr decr]
set tcp_dst_port_step_list           [list 1 2 3]
set tcp_dst_port_tracking_list       [list 0 1 0]

set tcp_ecn_echo_flag_list           [list 0 1 1]
set tcp_ecn_echo_flag_mode_list      [list fixed fixed fixed]
set tcp_ecn_echo_flag_tracking_list  [list 0 1 1]

set tcp_fin_flag_list                [list 0 1 1]
set tcp_fin_flag_mode_list           [list fixed fixed fixed]
set tcp_fin_flag_tracking_list       [list 0 1 1]

set tcp_ns_flag_list                 [list 0 1 1]
set tcp_ns_flag_mode_list            [list fixed fixed fixed]
set tcp_ns_flag_tracking_list        [list 0 1 1]

set tcp_psh_flag_list                [list 0 1 1]
set tcp_psh_flag_mode_list           [list fixed fixed fixed]
set tcp_psh_flag_tracking_list       [list 0 1 1]

set tcp_reserved_list                [list 1 4 2]
set tcp_reserved_count_list          [list 1 5 6]
set tcp_reserved_mode_list           [list fixed incr decr]
set tcp_reserved_step_list           [list 0 3 6]
set tcp_reserved_tracking_list       [list 0 0 1]

set tcp_rst_flag_list                [list 0 1 1]
set tcp_rst_flag_mode_list           [list fixed fixed fixed]
set tcp_rst_flag_tracking_list       [list 0 1 1]

set tcp_seq_num_list                 [list 10 33 66]
set tcp_seq_num_count_list           [list 7 3 6]
set tcp_seq_num_mode_list            [list fixed incr decr]
set tcp_seq_num_step_list            [list 163 21 31]
set tcp_seq_num_tracking_list        [list 0 1 0]

set tcp_src_port_list                [list 20 80 65534]
set tcp_src_port_count_list          [list 0 3 5]
set tcp_src_port_mode_list           [list fixed incr decr]
set tcp_src_port_step_list           [list 10 13 15]
set tcp_src_port_tracking_list       [list 0 1 0]

set tcp_syn_flag_list                [list 0 1 1]
set tcp_syn_flag_mode_list           [list fixed fixed fixed]
set tcp_syn_flag_tracking_list       [list 0 1 1]

set tcp_urg_flag_list                [list 0 1 1]
set tcp_urg_flag_mode_list           [list fixed fixed fixed]
set tcp_urg_flag_tracking_list       [list 0 1 1]

set tcp_urgent_ptr_list              [list 7 77 777]
set tcp_urgent_ptr_count_list        [list 14 11 1111]
set tcp_urgent_ptr_mode_list         [list fixed incr decr]
set tcp_urgent_ptr_step_list         [list 20 80 65534]
set tcp_urgent_ptr_tracking_list     [list 0 1 1]

set tcp_window_list                  [list 2 8 35]
set tcp_window_count_list            [list 6 10 1]
set tcp_window_mode_list             [list fixed incr decr]
set tcp_window_step_list             [list 15 12 5]
set tcp_window_tracking_list         [list 0 1 1]

foreach tcp_ack_flag                $tcp_ack_flag_list                  \
        tcp_ack_flag_mode           $tcp_ack_flag_mode_list             \
        tcp_ack_flag_tracking       $tcp_ack_flag_tracking_list         \
        tcp_ack_num                 $tcp_ack_num_list                   \
        tcp_ack_num_count           $tcp_ack_num_count_list             \
        tcp_ack_num_mode            $tcp_ack_num_mode_list              \
        tcp_ack_num_step            $tcp_ack_num_step_list              \
        tcp_ack_num_tracking        $tcp_ack_num_tracking_list          \
        tcp_checksum                $tcp_checksum_list                  \
        tcp_checksum_count          $tcp_checksum_count_list            \
        tcp_checksum_mode           $tcp_checksum_mode_list             \
        tcp_checksum_step           $tcp_checksum_step_list             \
        tcp_checksum_tracking       $tcp_checksum_tracking_list         \
        tcp_cwr_flag                $tcp_cwr_flag_list                  \
        tcp_cwr_flag_mode           $tcp_cwr_flag_mode_list             \
        tcp_cwr_flag_tracking       $tcp_cwr_flag_tracking_list         \
        tcp_data_offset             $tcp_data_offset_list               \
        tcp_data_offset_count       $tcp_data_offset_count_list         \
        tcp_data_offset_mode        $tcp_data_offset_mode_list          \
        tcp_data_offset_step        $tcp_data_offset_step_list          \
        tcp_data_offset_tracking    $tcp_data_offset_tracking_list      \
        tcp_dst_port                $tcp_dst_port_list                  \
        tcp_dst_port_count          $tcp_dst_port_count_list            \
        tcp_dst_port_mode           $tcp_dst_port_mode_list             \
        tcp_dst_port_step           $tcp_dst_port_step_list             \
        tcp_dst_port_tracking       $tcp_dst_port_tracking_list         \
        tcp_ecn_echo_flag           $tcp_ecn_echo_flag_list             \
        tcp_ecn_echo_flag_mode      $tcp_ecn_echo_flag_mode_list        \
        tcp_ecn_echo_flag_tracking  $tcp_ecn_echo_flag_tracking_list    \
        tcp_fin_flag                $tcp_fin_flag_list                  \
        tcp_fin_flag_mode           $tcp_fin_flag_mode_list             \
        tcp_fin_flag_tracking       $tcp_fin_flag_tracking_list         \
        tcp_ns_flag                 $tcp_ns_flag_list                   \
        tcp_ns_flag_mode            $tcp_ns_flag_mode_list              \
        tcp_ns_flag_tracking        $tcp_ns_flag_tracking_list          \
        tcp_psh_flag                $tcp_psh_flag_list                  \
        tcp_psh_flag_mode           $tcp_psh_flag_mode_list             \
        tcp_psh_flag_tracking       $tcp_psh_flag_tracking_list         \
        tcp_reserved                $tcp_reserved_list                  \
        tcp_reserved_count          $tcp_reserved_count_list            \
        tcp_reserved_mode           $tcp_reserved_mode_list             \
        tcp_reserved_step           $tcp_reserved_step_list             \
        tcp_reserved_tracking       $tcp_reserved_tracking_list         \
        tcp_rst_flag                $tcp_rst_flag_list                  \
        tcp_rst_flag_mode           $tcp_rst_flag_mode_list             \
        tcp_rst_flag_tracking       $tcp_rst_flag_tracking_list         \
        tcp_seq_num                 $tcp_seq_num_list                   \
        tcp_seq_num_count           $tcp_seq_num_count_list             \
        tcp_seq_num_mode            $tcp_seq_num_mode_list              \
        tcp_seq_num_step            $tcp_seq_num_step_list              \
        tcp_seq_num_tracking        $tcp_seq_num_tracking_list          \
        tcp_src_port                $tcp_src_port_list                  \
        tcp_src_port_count          $tcp_src_port_count_list            \
        tcp_src_port_mode           $tcp_src_port_mode_list             \
        tcp_src_port_step           $tcp_src_port_step_list             \
        tcp_src_port_tracking       $tcp_src_port_tracking_list         \
        tcp_syn_flag                $tcp_syn_flag_list                  \
        tcp_syn_flag_mode           $tcp_syn_flag_mode_list             \
        tcp_syn_flag_tracking       $tcp_syn_flag_tracking_list         \
        tcp_urg_flag                $tcp_urg_flag_list                  \
        tcp_urg_flag_mode           $tcp_urg_flag_mode_list             \
        tcp_urg_flag_tracking       $tcp_urg_flag_tracking_list         \
        tcp_urgent_ptr              $tcp_urgent_ptr_list                \
        tcp_urgent_ptr_count        $tcp_urgent_ptr_count_list          \
        tcp_urgent_ptr_mode         $tcp_urgent_ptr_mode_list           \
        tcp_urgent_ptr_step         $tcp_urgent_ptr_step_list           \
        tcp_urgent_ptr_tracking     $tcp_urgent_ptr_tracking_list       \
        tcp_window                  $tcp_window_list                    \
        tcp_window_count            $tcp_window_count_list              \
        tcp_window_mode             $tcp_window_mode_list               \
        tcp_window_step             $tcp_window_step_list               \
        tcp_window_tracking         $tcp_window_tracking_list           \
{
    set traffic_status [::ixia::traffic_config      \
            -mode                    create         \
            -emulation_src_handle    $intf0         \
            -emulation_dst_handle    $intf1         \
            -traffic_generator       ixnetwork_540  \
            -l3_protocol             ipv4           \
            -l4_protocol             tcp            \
            -tcp_ack_flag                $tcp_ack_flag                  \
            -tcp_ack_flag_mode           $tcp_ack_flag_mode             \
            -tcp_ack_flag_tracking       $tcp_ack_flag_tracking         \
            -tcp_ack_num                 $tcp_ack_num                   \
            -tcp_ack_num_count           $tcp_ack_num_count             \
            -tcp_ack_num_mode            $tcp_ack_num_mode              \
            -tcp_ack_num_step            $tcp_ack_num_step              \
            -tcp_ack_num_tracking        $tcp_ack_num_tracking          \
            -tcp_checksum                $tcp_checksum                  \
            -tcp_checksum_count          $tcp_checksum_count            \
            -tcp_checksum_mode           $tcp_checksum_mode             \
            -tcp_checksum_step           $tcp_checksum_step             \
            -tcp_checksum_tracking       $tcp_checksum_tracking         \
            -tcp_cwr_flag                $tcp_cwr_flag                  \
            -tcp_cwr_flag_mode           $tcp_cwr_flag_mode             \
            -tcp_cwr_flag_tracking       $tcp_cwr_flag_tracking         \
            -tcp_data_offset             $tcp_data_offset               \
            -tcp_data_offset_count       $tcp_data_offset_count         \
            -tcp_data_offset_mode        $tcp_data_offset_mode          \
            -tcp_data_offset_step        $tcp_data_offset_step          \
            -tcp_data_offset_tracking    $tcp_data_offset_tracking      \
            -tcp_dst_port                $tcp_dst_port                  \
            -tcp_dst_port_count          $tcp_dst_port_count            \
            -tcp_dst_port_mode           $tcp_dst_port_mode             \
            -tcp_dst_port_step           $tcp_dst_port_step             \
            -tcp_dst_port_tracking       $tcp_dst_port_tracking         \
            -tcp_ecn_echo_flag           $tcp_ecn_echo_flag             \
            -tcp_ecn_echo_flag_mode      $tcp_ecn_echo_flag_mode        \
            -tcp_ecn_echo_flag_tracking  $tcp_ecn_echo_flag_tracking    \
            -tcp_fin_flag                $tcp_fin_flag                  \
            -tcp_fin_flag_mode           $tcp_fin_flag_mode             \
            -tcp_fin_flag_tracking       $tcp_fin_flag_tracking         \
            -tcp_ns_flag                 $tcp_ns_flag                   \
            -tcp_ns_flag_mode            $tcp_ns_flag_mode              \
            -tcp_ns_flag_tracking        $tcp_ns_flag_tracking          \
            -tcp_psh_flag                $tcp_psh_flag                  \
            -tcp_psh_flag_mode           $tcp_psh_flag_mode             \
            -tcp_psh_flag_tracking       $tcp_psh_flag_tracking         \
            -tcp_reserved                $tcp_reserved                  \
            -tcp_reserved_count          $tcp_reserved_count            \
            -tcp_reserved_mode           $tcp_reserved_mode             \
            -tcp_reserved_step           $tcp_reserved_step             \
            -tcp_reserved_tracking       $tcp_reserved_tracking         \
            -tcp_rst_flag                $tcp_rst_flag                  \
            -tcp_rst_flag_mode           $tcp_rst_flag_mode             \
            -tcp_rst_flag_tracking       $tcp_rst_flag_tracking         \
            -tcp_seq_num                 $tcp_seq_num                   \
            -tcp_seq_num_count           $tcp_seq_num_count             \
            -tcp_seq_num_mode            $tcp_seq_num_mode              \
            -tcp_seq_num_step            $tcp_seq_num_step              \
            -tcp_seq_num_tracking        $tcp_seq_num_tracking          \
            -tcp_src_port                $tcp_src_port                  \
            -tcp_src_port_count          $tcp_src_port_count            \
            -tcp_src_port_mode           $tcp_src_port_mode             \
            -tcp_src_port_step           $tcp_src_port_step             \
            -tcp_src_port_tracking       $tcp_src_port_tracking         \
            -tcp_syn_flag                $tcp_syn_flag                  \
            -tcp_syn_flag_mode           $tcp_syn_flag_mode             \
            -tcp_syn_flag_tracking       $tcp_syn_flag_tracking         \
            -tcp_urg_flag                $tcp_urg_flag                  \
            -tcp_urg_flag_mode           $tcp_urg_flag_mode             \
            -tcp_urg_flag_tracking       $tcp_urg_flag_tracking         \
            -tcp_urgent_ptr              $tcp_urgent_ptr                \
            -tcp_urgent_ptr_count        $tcp_urgent_ptr_count          \
            -tcp_urgent_ptr_mode         $tcp_urgent_ptr_mode           \
            -tcp_urgent_ptr_step         $tcp_urgent_ptr_step           \
            -tcp_urgent_ptr_tracking     $tcp_urgent_ptr_tracking       \
            -tcp_window                  $tcp_window                    \
            -tcp_window_count            $tcp_window_count              \
            -tcp_window_mode             $tcp_window_mode               \
            -tcp_window_step             $tcp_window_step               \
            -tcp_window_tracking         $tcp_window_tracking           \
    ]
    if {[keylget traffic_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget traffic_status log]"
        return 0
    } else { puts "\nTraffic item [keylget traffic_status traffic_item] stream  is created." }
}

# Add up all params and make lists

set rename_params {
    tcp_ack_flag
    tcp_ack_num
    tcp_checksum
    tcp_cwr_flag
    tcp_data_offset
    tcp_dst_port
    tcp_ecn_echo_flag
    tcp_fin_flag
    tcp_ns_flag
    tcp_psh_flag
    tcp_reserved
    tcp_rst_flag
    tcp_seq_num
    tcp_src_port
    tcp_syn_flag
    tcp_urg_flag
    tcp_urgent_ptr
    tcp_window
}

# set up new vars for the list TI
foreach rename_p $rename_params {
    # make values lists
    set $rename_p [set [subst $rename_p]_list]
    set ${rename_p}_mode "list"
    # make tracking flags lists
    set ${rename_p}_tracking [set [subst $rename_p]_tracking]
}

set traffic_status [::ixia::traffic_config      \
        -mode                   create          \
        -emulation_src_handle   $intf0          \
        -emulation_dst_handle   $intf1          \
        -traffic_generator      ixnetwork_540   \
        -l3_protocol            ipv4            \
        -l4_protocol            tcp             \
        -tcp_ack_flag               $tcp_ack_flag_list          \
        -tcp_ack_flag_mode          $tcp_ack_flag_mode          \
        -tcp_ack_flag_tracking      $tcp_ack_flag_tracking      \
        -tcp_ack_num                $tcp_ack_num_list           \
        -tcp_ack_num_mode           $tcp_ack_num_mode           \
        -tcp_ack_num_tracking       $tcp_ack_num_tracking       \
        -tcp_checksum               $tcp_checksum_list          \
        -tcp_checksum_count         $tcp_checksum_count         \
        -tcp_checksum_mode          $tcp_checksum_mode          \
        -tcp_checksum_step          $tcp_checksum_step          \
        -tcp_checksum_tracking      $tcp_checksum_tracking      \
        -tcp_cwr_flag               $tcp_cwr_flag_list          \
        -tcp_cwr_flag_mode          $tcp_cwr_flag_mode          \
        -tcp_cwr_flag_tracking      $tcp_cwr_flag_tracking      \
        -tcp_data_offset            $tcp_data_offset_list       \
        -tcp_data_offset_mode       $tcp_data_offset_mode       \
        -tcp_data_offset_tracking   $tcp_data_offset_tracking   \
        -tcp_dst_port               $tcp_dst_port_list          \
        -tcp_dst_port_mode          $tcp_dst_port_mode          \
        -tcp_dst_port_tracking      $tcp_dst_port_tracking      \
        -tcp_ecn_echo_flag          $tcp_ecn_echo_flag_list     \
        -tcp_ecn_echo_flag_mode     $tcp_ecn_echo_flag_mode     \
        -tcp_ecn_echo_flag_tracking $tcp_ecn_echo_flag_tracking \
        -tcp_fin_flag               $tcp_fin_flag_list          \
        -tcp_fin_flag_mode          $tcp_fin_flag_mode          \
        -tcp_fin_flag_tracking      $tcp_fin_flag_tracking      \
        -tcp_ns_flag                $tcp_ns_flag_list           \
        -tcp_ns_flag_mode           $tcp_ns_flag_mode           \
        -tcp_ns_flag_tracking       $tcp_ns_flag_tracking       \
        -tcp_psh_flag               $tcp_psh_flag_list          \
        -tcp_psh_flag_mode          $tcp_psh_flag_mode          \
        -tcp_psh_flag_tracking      $tcp_psh_flag_tracking      \
        -tcp_reserved               $tcp_reserved_list          \
        -tcp_reserved_mode          $tcp_reserved_mode          \
        -tcp_reserved_tracking      $tcp_reserved_tracking      \
        -tcp_rst_flag               $tcp_rst_flag_list          \
        -tcp_rst_flag_mode          $tcp_rst_flag_mode          \
        -tcp_rst_flag_tracking      $tcp_rst_flag_tracking      \
        -tcp_seq_num                $tcp_seq_num_list           \
        -tcp_seq_num_mode           $tcp_seq_num_mode           \
        -tcp_seq_num_tracking       $tcp_seq_num_tracking       \
        -tcp_src_port               $tcp_src_port_list          \
        -tcp_src_port_mode          $tcp_src_port_mode          \
        -tcp_src_port_tracking      $tcp_src_port_tracking      \
        -tcp_syn_flag               $tcp_syn_flag_list          \
        -tcp_syn_flag_mode          $tcp_syn_flag_mode          \
        -tcp_syn_flag_tracking      $tcp_syn_flag_tracking      \
        -tcp_urg_flag               $tcp_urg_flag_list          \
        -tcp_urg_flag_mode          $tcp_urg_flag_mode          \
        -tcp_urg_flag_tracking      $tcp_urg_flag_tracking      \
        -tcp_urgent_ptr             $tcp_urgent_ptr_list        \
        -tcp_urgent_ptr_mode        $tcp_urgent_ptr_mode        \
        -tcp_urgent_ptr_tracking    $tcp_urgent_ptr_tracking    \
        -tcp_window                 $tcp_window_list            \
        -tcp_window_mode            $tcp_window_mode            \
        -tcp_window_tracking        $tcp_window_tracking        \
]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
} else { 
    puts "\nTraffic item [keylget traffic_status traffic_item] stream  is created." 
}

################################################################################
# Run traffic and print stats           
################################################################################

puts "Running Traffic..."
set traffic_status [::ixia::traffic_control -action run -traffic_generator ixnetwork_540]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

after 10000

puts "Stopping Traffic..."
set traffic_status [::ixia::traffic_control -action stop -traffic_generator ixnetwork_540]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

after 5000

puts "Traffic stats"
set traffic_status [::ixia::traffic_stats -mode aggregate -traffic_generator ixnetwork_540]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget traffic_status log]"
    return 0
}

foreach {port_handle} $port_handle {
    puts ""
    puts "port $port_handle"
    puts "-----------------------------------"
    puts "TX"
    set statlist [keylkeys traffic_status $port_handle.aggregate.tx]
    foreach {stat} $statlist {
        set v [keylget traffic_status $port_handle.aggregate.tx.$stat]
        puts [format {%40s = %s} $stat $v]
    }
    puts "RX"
    set statlist [keylkeys traffic_status $port_handle.aggregate.rx]
    foreach {stat} $statlist {
        set v [keylget traffic_status $port_handle.aggregate.rx.$stat]
        puts [format {%40s = %s} $stat $v]
    }
    puts ""
}


puts "\nSUCCESS - $test_name - [clock format [clock seconds]]"

