#################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mircea Hasegan $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-25-2007 Mircea Hasegan
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
#    This sample configures IPv4 and IPv6 interfaces on two ixia ports         #
#    connected to a cisco dut.                                                 #
#    ARP and router solicitation is sent from all interfaces of both ixia      #
#    ports.                                                                    #
#    The following IPv4 interfaces should fail to resolve gateway ARP:         #
#       Port1: Interface 3, Interface 4                                        #
#       Port2: Interface 9                                                     #
#    The following IPv6 interfaces should fail to resolve router solicitation: #
#       Port2: Interface 6, Interface 8                                        #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#                                                                              #
################################################################################

################################################################################
# DUT configuration:
#
# conf t
#
#  ipv6 unicast-routing
#  ipv6 cef
#
# int gi 0/2
#   ip address 101.101.101.1 255.255.255.0
#   no ip route-cache cef
#   no ip route-cache
#   no ip mroute-cache
#   duplex full
#   ipv6 address 2002:5678:5678::1/64
#   ipv6 enable
#   no shutdown
#
# int gi 0/3
#   ip address 100.100.100.1 255.255.255.0
#   no ip route-cache cef
#   no ip route-cache
#   no ip mroute-cache
#   duplex full
#   no shutdown
#
# end
#
###########################################################################

set env(IXIA_VERSION) HLTSET26

package require Ixia

set test_name [info script]
set chassisIP sylvester
set port_list [list 3/3 3/4]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_list       \
        -username  ixiaApiUser      \
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

set port1 [lindex $port_handle 0]
set port2 [lindex $port_handle 1]

puts "Ixia port handles are $port_handle ..."

################################################################################
# Configure Interface 1
################################################################################

set interface_status [::ixia::interface_config \
        -port_handle      $port1     \
        -mode             config               \
        -speed            ether100             \
        -phy_mode         copper               \
        -autonegotiation  1                    \
        -intf_ip_addr     101.101.101.110      \
        -gateway          101.101.101.1        \
        -netmask          255.255.255.0        \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Configure Interface 2
################################################################################

set interface_status [::ixia::interface_config \
        -port_handle      $port1     \
        -mode             config               \
        -speed            ether100             \
        -phy_mode         copper               \
        -autonegotiation  1                    \
        -intf_ip_addr     101.101.101.111      \
        -gateway          101.101.101.1        \
        -netmask          255.255.255.0        \
        -ipv6_intf_addr     2002:5678:5678::100\
        -ipv6_prefix_length 64                 \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Configure Interface 3
################################################################################

set interface_status [::ixia::interface_config \
        -port_handle      $port1     \
        -mode             config               \
        -speed            ether100             \
        -phy_mode         copper               \
        -autonegotiation  1                    \
        -intf_ip_addr     101.101.101.112      \
        -gateway          101.101.101.2        \
        -netmask          255.255.255.0        \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Configure Interface 4
################################################################################

set interface_status [::ixia::interface_config \
        -port_handle      $port1     \
        -mode             config               \
        -speed            ether100             \
        -phy_mode         copper               \
        -autonegotiation  1                    \
        -intf_ip_addr     101.101.101.113      \
        -gateway          101.101.101.3        \
        -netmask          255.255.255.0        \
        -ipv6_intf_addr   2002:5678:5678::101  \
        -ipv6_prefix_length 64                 \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Configure Interface 5
################################################################################

set interface_status [::ixia::interface_config \
        -port_handle      $port1     \
        -mode             config               \
        -speed            ether100             \
        -phy_mode         copper               \
        -autonegotiation  1                    \
        -ipv6_intf_addr   2002:5678:5678::102  \
        -ipv6_prefix_length 64                 \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Configure Interface 6
################################################################################

set interface_status [::ixia::interface_config \
        -port_handle      $port2     \
        -mode             config               \
        -speed            ether100             \
        -phy_mode         copper               \
        -autonegotiation  1                    \
        -intf_ip_addr     100.100.100.50       \
        -gateway          100.100.100.1        \
        -netmask          255.255.255.0        \
        -ipv6_intf_addr     2001::4            \
        -ipv6_prefix_length 64                 \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Configure Interface 7
################################################################################

set interface_status [::ixia::interface_config \
        -port_handle      $port2     \
        -mode             config               \
        -speed            ether100             \
        -phy_mode         copper               \
        -autonegotiation  1                    \
        -intf_ip_addr     100.100.100.51       \
        -gateway          100.100.100.1        \
        -netmask          255.255.255.0        \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Configure Interface 8
################################################################################

set interface_status [::ixia::interface_config \
        -port_handle      $port2     \
        -mode             config               \
        -speed            ether100             \
        -phy_mode         copper               \
        -autonegotiation  1                    \
        -ipv6_intf_addr     2001::5            \
        -ipv6_prefix_length 64                 \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Configure Interface 9
################################################################################

set interface_status [::ixia::interface_config \
        -port_handle      $port2               \
        -mode             config               \
        -speed            ether100             \
        -phy_mode         copper               \
        -autonegotiation  1                    \
        -intf_ip_addr     100.100.100.52       \
        -gateway          100.100.100.2        \
        -netmask          255.255.255.0        \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

################################################################################
# Send ARP request
################################################################################
set interface_status [::ixia::interface_config \
        -port_handle     [list $port1 $port2]      \
        -arp_send_req    1                     \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}

foreach port $port_handle {
    puts "\nPort $port:"
    if {[keylget interface_status $port.arp_request_success] == 1} {
        puts "\tARP resolved for all interfaces"
    } else {
        if {![catch {keylget interface_status $port.arp_ipv4_interfaces_failed} out]} {
            puts "\tIPv4 Interfaces that failed to resolve ARP: $out"
        }
        if {![catch {keylget interface_status $port.arp_ipv6_interfaces_failed} out]} {
            puts "\tIPv6 Interfaces that didn't receive a response to router \
                    solicitation: $out"
        }
    }
}


set control_status [::ixia::cleanup_session -port_handle $port_handle]
if {[keylget control_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget control_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"

