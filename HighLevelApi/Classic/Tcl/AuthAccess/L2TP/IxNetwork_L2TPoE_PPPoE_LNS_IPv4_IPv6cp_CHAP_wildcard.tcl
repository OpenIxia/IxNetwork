################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Matei-Eugen Vasile $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    7-6-2007 Matei-Eugen Vasile
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
###############################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample configures 150 PPPoE sessions, between the first Ixia port    #
#    and DUT, and 3 L2TP tunnels, each with 50 sessions, between DUT and the   #
#    other Ixia port.                                                          #
#    The topology is the following:                                            #
#                                                                              #
#      Access      PPPoE               L2TPoE                                  #
#      Network   -------- LAC (DUT)  ---------- LNS                            #
#    (Ixia Port1)        (Cisco 7200)       (Ixia Port2)                       #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################

################################################################################
# DUT config:                                                                  #
################################################################################
# conf t
# !
# vpdn enable
# vpdn search-order domain
# !
# vpdn-group gigel1.org
#  request-dialin
#   protocol l2tp
#   domain gigel1.org
#  initiate-to ip 12.70.0.1
#  local name dut
#  l2tp tunnel password ixia
# !
# vpdn-group gigel2.org
#  request-dialin
#   protocol l2tp
#   domain gigel2.org
#  initiate-to ip 12.70.0.1
#  local name dut
#  l2tp tunnel password ixia
# !
# vpdn-group gigel3.org
#  request-dialin
#   protocol l2tp
#   domain gigel3.org
#  initiate-to ip 12.70.0.1
#  local name dut
#  l2tp tunnel password ixia
# !
# bba-group pppoe LAC_GROUP
#  virtual-template 1
# !
# interface FastEthernet5/0
#  no ip address
#  pppoe enable group LAC_GROUP
#  no shutdown
# !
# interface FastEthernet6/0
#  ip address 12.70.0.2 255.255.255.0
#  no shutdown
# !
# interface Virtual-Template1
#  no ip address
#  ppp authentication chap
# !
# end
################################################################################

package require Ixia

set test_name           [info script]

set chassisIP           sylvester
set port_list           [list 2/3 2/4]

set tunnel_count        3
set sessions_per_tunnel 50

################################################################################
# Connect to the chassis, reset to factory defaults and take ownership         #
################################################################################
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                             \
        -reset                                                                  \
        -ixnetwork_tcl_server       localhost                                   \
        -device                     $chassisIP                                  \
        -port_list                  $port_list                                  \
        ]
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
set access_port  [lindex $port_handle 0]
set network_port [lindex $port_handle 1]

################################################################################
# Initialize the parameters for the access interface(s) in the test            #
################################################################################
set port_handle_list        [list]
set speed_list              [list]
set duplex_list             [list]
set auto_list               [list]
set phy_mode_list           [list]

################################################################################
# Configure the parameters for the access interface(s) in the test             #
################################################################################
for {set i 2} {$i <= [expr $tunnel_count + 1]} {incr i} {
    lappend port_handle_list    $access_port
    lappend speed_list          ether100
    lappend duplex_list         half
    lappend phy_mode_list       copper
    lappend auto_list           1
}

################################################################################
# Configure the parameters for the network interface(s) in the test            #
################################################################################
lappend port_handle_list    $network_port
lappend speed_list          ether100
lappend duplex_list         half
lappend phy_mode_list       copper
lappend auto_list           1

################################################################################
# Configure the interfaces                                                     #
################################################################################
set interface_status [::ixia::interface_config                                  \
        -port_handle                $port_handle_list                           \
        -mode                       config                                      \
        -speed                      $speed_list                                 \
        -duplex                     $duplex_list                                \
        -phy_mode                   $phy_mode_list                              \
        -autonegotiation            $auto_list                                  \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Configure PPPoE on access port                                               #
################################################################################
set config_status [::ixia::pppox_config                                     \
        -port_handle                $access_port                                \
        -mode                       add                                         \
        -protocol                   pppoe                                       \
        -port_role                  access                                      \
        -encap                      ethernet_ii                                 \
        -num_sessions               [expr $tunnel_count * $sessions_per_tunnel] \
        -redial                     1                                           \
        -redial_max                 10                                          \
        -redial_timeout             20                                          \
        -ip_cp                      ipv6_cp                                     \
        -auth_req_timeout           10                                          \
        -auth_mode                  chap                                        \
        -username                   "user@gigel#.org"                           \
        -password                   pass                                        \
        -username_wildcard          1                                           \
        -wildcard_pound_start       1                                           \
        -wildcard_pound_end         $tunnel_count                               \
        ]
if {[keylget config_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget config_status log]"
}
set access_pppox_handle [keylget config_status handle]

################################################################################
# Configure L2TP on the network port                                           #
################################################################################
set l2tp_status [::ixia::l2tp_config                                            \
        -port_handle                $network_port                               \
        -mode                       lns                                         \
        -l2_encap                   ethernet_ii                                 \
        -num_tunnels                $tunnel_count                               \
        -sessions_per_tunnel        $sessions_per_tunnel                        \
        -l2tp_src_addr              12.70.0.1                                   \
        -l2tp_dst_addr              12.70.0.2                                   \
        -l2tp_src_count             1                                           \
        -l2tp_src_step              0.0.0.0                                     \
        -l2tp_dst_step              0.0.0.0                                     \
        -tun_auth                                                               \
        -hostname                   dut                                         \
        -secret                     ixia                                        \
        -auth_mode                  chap                                        \
        -username                   "user@gigel#.org"                           \
        -password                   pass                                        \
        -username_wc                1                                           \
        -wildcard_pound_start       1                                           \
        -wildcard_pound_end         $tunnel_count                               \
        -ip_cp                      ipv6_cp                                     \
        -ppp_client_ip              BEEF::2                                     \
        -ppp_client_step            0::17                                       \
        -ppp_server_ip              BEEF::1                                     \
        -ipv6_pool_addr_prefix_len  48                                          \
        -ipv6_pool_prefix           BEEF::0                                     \
        -ipv6_pool_prefix_len       32                                          \
        ]
if {[keylget l2tp_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget l2tp_status log]"
}

set network_l2tp_handle [keylget l2tp_status handle]

################################################################################
# Connect sessions                                                             #
################################################################################
set control_status [::ixia::l2tp_control                                        \
        -handle     [list                                                       \
                            $network_l2tp_handle                                \
                    ]                                                           \
        -action     connect                                                     \
        ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}

set control_status [::ixia::pppox_control                                       \
        -handle     [list                                                       \
                            $access_pppox_handle                                \
                    ]                                                           \
        -action     connect                                                     \
        ]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}

################################################################################
# Get L2TP aggregate statistics                                                #
################################################################################
after 10000
set l2tp_status [::ixia::l2tp_stats                                             \
        -port_handle    [list                                                   \
                                $network_port                                   \
                        ]                                                       \
        -mode           aggregate                                               \
        ]
if {[keylget l2tp_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget l2tp_status log]"
}

set port_list [keylkeys l2tp_status]
foreach port $port_list {
    if {$port != "status"} {
        puts "port: $port"
        puts "\ttunnels up: [keylget l2tp_status $port.aggregate.tunnels_up]"
        puts "\tsessions up: [keylget l2tp_status $port.aggregate.sessions_up]"
    }
}
