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
#    This sample configures two ipv4 ports and a traffic item with udp         #
#    as a L4 protocol.                                                         #
#    This is an advanced config showing all possible params related to udp.    #
#    The traffic is routed through a DUT with the configuration below.         #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10/100/1000 STXS4-256Mb module.                #
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

set udp_dst_port_mode                       "list"
set udp_dst_port                            [list 12 20 50]
set udp_dst_port_tracking                   1

set udp_length_mode                         "list"
set udp_length                              [list 50 80 55]
set udp_length_tracking                     0

set udp_src_port_mode                       "list"
set udp_src_port                            [list 80 123 65535]
set udp_src_port_tracking                   0

set udp_checksum                            0
set udp_checksum_value                      "a1"
set udp_checksum_value_tracking             1

set traffic_status [::ixia::traffic_config                             \
        -mode                             create                       \
        -emulation_src_handle             $intf0                       \
        -emulation_dst_handle             $intf1                       \
        -traffic_generator                ixnetwork_540                \
        -l3_protocol                      ipv4                         \
        -l4_protocol                      udp                          \
        -udp_checksum                     $udp_checksum                \
        -udp_checksum_value               $udp_checksum_value          \
        -udp_checksum_value_tracking      $udp_checksum_value_tracking \
        -udp_dst_port                     $udp_dst_port                \
        -udp_dst_port_mode                $udp_dst_port_mode           \
        -udp_dst_port_tracking            $udp_dst_port_tracking       \
        -udp_length                       $udp_length                  \
        -udp_length_mode                  $udp_length_mode             \
        -udp_length_tracking              $udp_length_tracking         \
        -udp_src_port                     $udp_src_port                \
        -udp_src_port_mode                $udp_src_port_mode           \
        -udp_src_port_tracking            $udp_src_port_tracking       \
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
    
