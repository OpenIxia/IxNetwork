################################################################################
# Version 1.0    $Revision: 1 $
# $Author: MHasegan $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-18-2006 MHasegan
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
#    This sample configures one ancp sessions                                  ##                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10/100/1000 STXS4-256Mb module.                #
#                                                                              #
################################################################################


#DUT CONFIGURATOIN
#conf t
#
#no ip dhcp pool ancp_scalability
#ip dhcp pool ancp_scalability
#   network 175.71.0.0 255.255.0.0
#   default-router 175.71.0.1
#   lease 3
#
#no ipv6 dhcp pool ancp_scalability
#ipv6 dhcp pool ancp_scalability
# prefix-delegation pool ancp_scalability lifetime infinite infinite
#
#no bba-group pppoe monprofileipv4_1
#bba-group pppoe monprofileipv4_1
# virtual-template 3
# sessions per-vc limit 4000
# sessions per-mac limit 65530
# sessions per-vlan limit 65530 inner 65530
#
#no interface GigabitEthernet7/0/0.1
#interface GigabitEthernet7/0/0.1
# encapsulation dot1Q 71 second-dot1q 701
# ip address 175.71.0.1 255.255.0.0
# pppoe enable group monprofileipv4_1
# ipv6 address 2002:175:71:0:1::1/64
# ipv6 enable
# ipv6 ospf 2 area 0
# ipv6 dhcp server ancp_scalability
#
#!
#no interface GigabitEthernet7/0/0.2
#interface GigabitEthernet7/0/0.2
# encapsulation dot1Q 72 second-dot1q 702
# ip address 175.72.0.1 255.255.0.0
# pppoe enable group monprofileipv4_1
# ancp enable
# !
# ipv6 address 2002:175:72:0:1::1/64
#
#
#no interface Virtual-Template3
#interface Virtual-Template3
# ip unnumbered Loopback1
# peer default ip address pool monpoolipv4_1
# peer default ipv6 pool monpoolipv6_1
# ppp authentication pap
#
#no ip local pool monpoolipv4_1
#ip local pool monpoolipv4_1 137.1.1.1 137.1.11.250
#no ipv6 local pool monpoolipv6_1
#ipv6 local pool monpoolipv6_1 2002:ABCD::/48 64
#
#end
#
#tclsh
#
#conf t
#
#for { set i 0 } { $i<=253 } { incr i } {
#    set an [expr 1+$i]    ;# the AN variable
#    for { set y 1 } { $y<=100 } { incr y } {
#	set id [expr $i*100+$y]    ;# the client-ID variable
#	set anip [expr 1+$an]    ;# the access node ip variable
#	set dslid [expr 100000+$id]    ;# the dsl ID variable
#
#	"no ancp neighbor name AN_$an id 175.72.0.$anip"
#	"ancp neighbor name AN_$an id 175.72.0.$anip"
#	"dot1q 72 second-dot1q 702 interface Gi7/0/0.2 client-ID DL$dslid"
#    }
#}
# 
#for { set i 254 } { $i<=319 } { incr i } {
#    set an [expr 1+$i]    ;# the AN variable
#    for { set y 1 } { $y<=100 } { incr y } {
#	set id [expr $i*100+$y]    ;# the client-ID variable
#	set anip [expr $an-255]    ;# the access node ip variable
#	set dslid [expr 100000+$id]    ;# the dsl ID variable
#
#	"no ancp neighbor name AN_$an id 175.72.1.$anip"
#	"ancp neighbor name AN_$an id 175.72.1.$anip"
#	"dot1q 72 second-dot1q 702 interface Gi7/0/0.2 client-ID DL$dslid"
#    }
#}



package require Ixia

set test_name [info script]

set chassis_ip 10.205.17.97
set port_list [list 1/5]

# Connect to the chassis.
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect             \
        -reset                                  \
        -ixnetwork_tcl_server   localhost       \
        -device                 $chassis_ip     \
        -port_list              $port_list      \
        -username               ixiaApiUser     ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}
set port_handle [keylget connect_status port_handle.$chassis_ip.$port_list]

# Configure physical port attributes
set interface_status [::ixia::interface_config \
        -port_handle       $port_handle        \
        -intf_mode          ethernet           \
        -phy_mode           copper             \
        -autonegotiation    1                  \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}



################################################################################
# START - Interface configuration - L2, L3
################################################################################



set intf_cfg_port_handle        $port_handle
set chassis                     [format %02x [lindex [split $port_handle "/"] 0]]
set card                        [format %02x [lindex [split $port_handle "/"] 1]]
set port                        [format %02x [lindex [split $port_handle "/"] 2]]

set src_mac_addr                00${chassis}.00${card}.${port}01    ;# MAC
set vlan                        1                                 ;# CHOICES 0 1 DEFAULT 0
set vlan_id                     701,71                              ;# RANGE 0-4096
set vci                         32                                  ;# RANGE 32-65535 DEFAULT 32
set vpi                         0                                   ;# RANGE 0-255 DEFAULT 0
set ip_type                     ipv4                                ;# CHOICES ipv4 ipv6 ipv46
set intf_ip_addr                175.71.0.2                          ;# IPV4
set gateway                     175.71.0.1                          ;# IPV4
set netmask                     255.255.0.0                         ;# IPV4
set ipv6_intf_addr              200::1                              ;# IPV6
set ipv6_prefix_length          64                                  ;# RANGE 1-128
set l23_config_type             static_endpoint                     ;# CHOICES protocol_interface static_endpoint DEFAULT protocol_interface
set mtu                         1500
set mss                         1460	
set qinq_incr_mode              both      

    set interface_status [::ixia::interface_config                             \
            -port_handle            $intf_cfg_port_handle                      \
            -mode                   modify                                     \
            -src_mac_addr           $src_mac_addr                              \
	    -vlan                   $vlan                                      \
	    -vlan_id                $vlan_id                                   \
            -intf_ip_addr           $intf_ip_addr                              \
            -gateway                $gateway                                   \
            -netmask                $netmask                                   \
            -l23_config_type        $l23_config_type                           \
	    -mtu                    $mtu                                       \
	    -mss                    $mss                                       \
	    -qinq_incr_mode         $qinq_incr_mode                            \
            ]
    if {[keylget interface_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget interface_status log]"
        return
    }
set interface_config_handle_0_list   [keylget interface_status interface_handle]

puts "Interface config complete."

################################################################################
# END - Interface configuration - L2, L3
################################################################################
################################################################################
# START - ANCP configuration - First port
################################################################################
puts "Start ANCP configuration ..."
update idletasks

################################################################################
# ANCP - GENERAL
################################################################################
set device_count                                   10                                 ;# NUMERIC DEFAULT 1
set handle                                         $interface_config_handle_0_list    ;# ANY 
set mode                                           create                             ;# CHOICES create modify delete enable disable enable_all disable_all DEFAULT create
set ancp_cfg_port_handle                           $port_handle                            ;# ANY 

################################################################################
# ANCP - GLOBAL and PORT
################################################################################
set ancp_standard                                  ietf-ancp-protocol2                ;# Only the default value is supported - CHOICES ietf-ancp-protocol2 gsmp-l2control-config2 DEFAULT ietf-ancp-protocol2
set events_per_interval                            10                                 ;# RANGE 1-300 DEFAULT 10
set global_port_down_rate                          50                                 ;# RANGE 1-300 DEFAULT 50
set global_port_up_rate                            10                                 ;# RANGE 1-300 DEFAULT 10
set global_resync_rate                             50                                 ;# RANGE 1-300 DEFAULT 50
set gsmp_standard                                  gsmp-v3-base                       ;# Only the default value is supported - CHOICES RFC-3292 gsmp-v3-base DEFAULT gsmp-v3-base
set interval                                       1                                  ;# RANGE 1-100 DEFAULT 1
set line_config                                    0                                  ;# Only the default value is supported - CHOICES 0 1 DEFAULT 0
set port_down_rate                                 50                                 ;# RANGE 1-300 DEFAULT 50
set port_resync_rate                               50                                 ;# RANGE 1-300 DEFAULT 50
set port_up_rate                                   50                                 ;# RANGE 1-300 DEFAULT 50
set port_override_globals                          1                                  ;# CHOICES 0 1 DEFAULT 1
set topology_discovery                             1                                  ;# CHOICES 0 1 DEFAULT 1

################################################################################
# ANCP - Access Loop
################################################################################
set access_aggregation                             0                                  ;# CHOICES 0 1 DEFAULT 0
set access_aggregation_dsl_inner_vlan              1                                  ;# RANGE 1-4094 DEFAULT 1
set access_aggregation_dsl_inner_vlan_type         actual_dsl_subscriber_vlan         ;# CHOICES actual_dsl_subscriber_vlan custom DEFAULT actual_dsl_subscriber_vlan
set access_aggregation_dsl_outer_vlan              1                                  ;# RANGE 1-4094 DEFAULT 1
set access_aggregation_dsl_outer_vlan_type         actual_dsl_subscriber_vlan         ;# CHOICES actual_dsl_subscriber_vlan custom DEFAULT actual_dsl_subscriber_vlan

################################################################################
# ANCP - NAS
################################################################################
set keep_alive                                     10000                              ;# RANGE 1000-25000 DEFAULT 10000
set keep_alive_retries                             3                                  ;# RANGE 1-10 DEFAULT 3
set sut_ip_addr                                    175.72.0.1                         ;# IPV4 DEFAULT 20.20.0.1
set sut_service_port                               6068                               ;# RANGE 1-65535 DEFAULT 6068

################################################################################
# ANCP - ACCESS NODE IP
################################################################################
set gateway_incr_mode                              every_subnet                       ;# CHOICES every_subnet every_interface DEFAULT every_subnet
set gateway_ip_addr                                175.72.0.1                         ;# IPV4 DEFAULT 0.0.0.0
set gateway_ip_prefix_len                          16                                 ;# RANGE 0-32 DEFAULT 16
set gateway_ip_step                                0.0.0.1                            ;# IPV4 DEFAULT 0.0.0.0
set intf_ip_addr                                   175.72.0.12                        ;# IPV4 DEFAULT 10.10.10.2
set intf_ip_prefix_len                             16                                 ;# RANGE 0-32 DEFAULT 16
set intf_ip_step                                   0.0.0.1                            ;# IPV4 DEFAULT 0.0.0.1
set local_mss                                      1460                               ;# RANGE 28-9460 DEFAULT 1460

################################################################################
# ANCP - ACCESS NODE MAC
################################################################################
set encap_type                                     ETHERNETII                         ;# CHOICES ETHERNETII SAF SNAP DEFAULT ETHERNETII
set local_mac_addr                                 000a.0abc.0200                     ;# MAC DEFAULT 000a.0a00.0200
set local_mac_step                                 0000.0000.0001                     ;# MAC DEFAULT 0000.0000.0001
set local_mac_addr_auto                            0                                  ;# CHOICES 0 1 DEFAULT 1
set local_mtu                                      1500                               ;# RANGE 500-9500 DEFAULT 1500

################################################################################
# ANCP - ACCESS NODE VLAN
################################################################################
set qinq_incr_mode                                 both                               ;# CHOICES inner outer both DEFAULT both
set vlan_id                                        72                                 ;# RANGE 0-4095 DEFAULT 1
set vlan_id_count                                  1                                  ;# RANGE 0-4095 DEFAULT 1
set vlan_id_count_inner                            1                                  ;# RANGE 0-4095 DEFAULT 1
set vlan_id_inner                                  702                                ;# RANGE 0-4095 DEFAULT 1
set vlan_id_repeat                                 1                                  ;# NUMERIC DEFAULT 1
set vlan_id_repeat_inner                           1                                  ;# NUMERIC DEFAULT 1
set vlan_id_step                                   1                                  ;# RANGE 0-4095 DEFAULT 1
set vlan_id_step_inner                             1                                  ;# RANGE 0-4095 DEFAULT 1
set vlan_user_priority                             1                                  ;# RANGE 0-7 DEFAULT 0
set vlan_user_priority_inner                       1                                  ;# RANGE 0-7 DEFAULT 0



################################################################################
# Start ANCP Call
################################################################################
set ANCP_config_status [::ixia::emulation_ancp_config                                                   \
        -device_count                                   $device_count                                   \
        -handle                                         $handle                                         \
        -mode                                           $mode                                           \
        -port_handle                                    $ancp_cfg_port_handle                           \
        -ancp_standard                                  $ancp_standard                                  \
        -events_per_interval                            $events_per_interval                            \
        -global_port_down_rate                          $global_port_down_rate                          \
        -global_port_up_rate                            $global_port_up_rate                            \
        -global_resync_rate                             $global_resync_rate                             \
        -gsmp_standard                                  $gsmp_standard                                  \
        -interval                                       $interval                                       \
        -line_config                                    $line_config                                    \
        -port_down_rate                                 $port_down_rate                                 \
        -port_resync_rate                               $port_resync_rate                               \
        -port_up_rate                                   $port_up_rate                                   \
        -port_override_globals                          $port_override_globals                          \
        -topology_discovery                             $topology_discovery                             \
        -access_aggregation                             $access_aggregation                             \
        -access_aggregation_dsl_inner_vlan              $access_aggregation_dsl_inner_vlan              \
        -access_aggregation_dsl_inner_vlan_type         $access_aggregation_dsl_inner_vlan_type         \
        -access_aggregation_dsl_outer_vlan              $access_aggregation_dsl_outer_vlan              \
        -access_aggregation_dsl_outer_vlan_type         $access_aggregation_dsl_outer_vlan_type         \
        -keep_alive                                     $keep_alive                                     \
        -keep_alive_retries                             $keep_alive_retries                             \
        -sut_ip_addr                                    $sut_ip_addr                                    \
        -sut_service_port                               $sut_service_port                               \
        -gateway_incr_mode                              $gateway_incr_mode                              \
        -gateway_ip_addr                                $gateway_ip_addr                                \
        -gateway_ip_prefix_len                          $gateway_ip_prefix_len                          \
        -gateway_ip_step                                $gateway_ip_step                                \
        -intf_ip_addr                                   $intf_ip_addr                                   \
        -intf_ip_prefix_len                             $intf_ip_prefix_len                             \
        -intf_ip_step                                   $intf_ip_step                                   \
        -local_mss                                      $local_mss                                      \
        -encap_type                                     $encap_type                                     \
        -local_mac_addr                                 $local_mac_addr                                 \
        -local_mac_step                                 $local_mac_step                                 \
        -local_mac_addr_auto                            $local_mac_addr_auto                            \
        -local_mtu                                      $local_mtu                                      \
        -qinq_incr_mode                                 $qinq_incr_mode                                 \
	-vlan_id                                        $vlan_id                                        \
        -vlan_id_count                                  $vlan_id_count                                  \
        -vlan_id_count_inner                            $vlan_id_count_inner                            \
	-vlan_id_inner                                  $vlan_id_inner                                  \
        -vlan_id_repeat                                 $vlan_id_repeat                                 \
        -vlan_id_repeat_inner                           $vlan_id_repeat_inner                           \
        -vlan_id_step                                   $vlan_id_step                                   \
        -vlan_id_step_inner                             $vlan_id_step_inner                             \
        -vlan_user_priority                             $vlan_user_priority                             \
        -vlan_user_priority_inner                       $vlan_user_priority_inner                       \
        ]
if {[keylget ANCP_config_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget ANCP_config_status log]"
    return
}
set ANCP_handles [keylget ANCP_config_status handle]
puts "Ixia ANCP handles are: "
update idletasks
foreach ANCP_handle $ANCP_handles {
    puts $ANCP_handle
    update idletasks
}
################################################################################
# End ANCP Call
################################################################################


puts "End ANCP configuration ..."
update idletasks
################################################################################
# END - ANCP configuration - First Port
################################################################################

set sbsc_out [::ixia::emulation_ancp_subscriber_lines_config        \
       -mode                               create                   \
       -ancp_client_handle                 $ANCP_handles            \
       -circuit_id                         DL                       \
       -circuit_id_suffix                  116300                   \
       -circuit_id_suffix_repeat           1                        \
       -circuit_id_suffix_step             1                        \
       -actual_rate_downstream             13                       \
       -actual_rate_upstream               14                       \
       -data_link                          ethernet                 \
       -downstream_act_interleaving_delay  22                       \
       -downstream_attainable_rate         23                       \
       -downstream_max_interleaving_delay  54                       \
       -downstream_max_rate                25                       \
       -downstream_min_low_power_rate      26                       \
       -downstream_min_rate                27                       \
       -dsl_type                           vdsl2                    \
       -encap1                             single_tagged_ethernet   \
       -encap2                             aal5_null_wo_fcs         \
       -include_encap                      1                        \
       -remote_id                          50                       \
       -upstream_act_interleaving_delay    76                       \
       -upstream_attainable_rate           88                       \
       -upstream_max_interleaving_delay    99                       \
       -upstream_max_rate                  76                       \
       -upstream_min_low_power_rate        66                       \
       -upstream_min_rate                  55                       \
       -percentage                         80                       \
    ]

if {[keylget sbsc_out status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget sbsc_out log]"
    return 0
}

################################################################################
# End ANCP Call
################################################################################
puts "End ANCP Profile configuration ..."
update idletasks
################################################################################
# END - ANCP Profile configuration - First port
################################################################################

after 1000

puts "starting ANCP protocol"

##################################################
# Start ANCP                                   #
##################################################

set control_status_0 [::ixia::emulation_ancp_control \
        -ancp_handle $ANCP_handle                    \
        -action            enable                    \
	-action_control    start                     \
        ]
if {[keylget control_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status_0 log]"
    return 0
}

after 10000

##################################################
#           GET ANCP STATISTICS                #
##################################################

set ancp_stats_0 [::ixia::emulation_ancp_stats      \
        -port_handle   $port_handle                      \
        ]
if {[keylget ancp_stats_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name -[keylget ancp_stats_0 log]"
    return 0
}

after 5000


##################################################
#            PRINT ANCP STATISTICS               #
##################################################


proc show_stats var {
    set level [expr [info level] - 1]
    foreach key [keylkeys var] {
            if {$key == "status"} {continue}
            set indent [string repeat "    " $level] 
            puts -nonewline $indent 
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


puts "These are the statistics after starting the protocol"

puts "####################################################"
show_stats $ancp_stats_0
puts "####################################################"


after 2000

##################################################
# Stop reset ANCP                                #
##################################################

set control_status_0 [::ixia::emulation_ancp_control \
        -ancp_handle $ANCP_handle                    \
        -action            enable                    \
	-action_control    stop                      \
        ]
if {[keylget control_status_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget control_status_0 log]"
    return 0
}

##################################################
#           GET ANCP STATISTICS                #
##################################################

set ancp_stats_0 [::ixia::emulation_ancp_stats      \
        -port_handle   $port_handle                      \
        ]
if {[keylget ancp_stats_0 status] != $::SUCCESS} {
    puts "FAIL - $test_name -[keylget ancp_stats_0 log]"
    return 0
}


puts "These are the statistics after stoping the protocol"

puts "####################################################"
show_stats $ancp_stats_0
puts "####################################################"


return "SUCCESS - $test_name - [clock format [clock seconds]]"
