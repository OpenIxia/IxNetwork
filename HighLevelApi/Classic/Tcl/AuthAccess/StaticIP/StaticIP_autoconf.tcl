################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Adrian Enache $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-29-2013 Adrian Enache
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
#    This sample configures one static ipv6 with autoconfiguration enabled     #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a 10/100/1000 STXS4-256Mb module.                #
#                                                                              #
################################################################################

# dut config

# conf t
# ipv6 unicast-routing
# int g7/13
# ipv6 address 2001:1212::/64 eui-64
# ipv6 nd prefix 2001:1212::/64
# no ipv6 nd suppress-ra
# no sh

package req Ixia

set chassis {10.205.16.26}
set tcl_server 10.205.16.26
set master_chassis {none}
set port_list {{1/3}}
set aggregation_mode {{not_supported not_supported}}
set aggregation_resource_mode {{normal normal}}
set guard_rail statistics
# 
#  this should match up w/ your port_list above
# 
set ixnHLT(path_list) {{//vport:<1>}}
# 
# 
set _result_ [::ixia::connect  \
    -reset 1 \
    -device $chassis \
    -master_device $master_chassis \
    -aggregation_mode $aggregation_mode \
    -aggregation_resource_mode $aggregation_resource_mode \
    -port_list $port_list \
    -ixnetwork_tcl_server localhost \
    -tcl_server $tcl_server \
    -guard_rail $guard_rail \
]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
  $::ixnHLT_errorHandler [info script] $_result_
}
foreach {port_list_elem} $port_list {path_list_elem} $ixnHLT(path_list) {chassis_elem} $chassis {
    foreach {port} $port_list_elem {path} $path_list_elem {
        if {[catch {keylget _result_ port_handle.$chassis_elem.$port} _port_handle]} {
            error "connection status: $_result_: $_port_handle"
        }
        set ixnHLT(PORT-HANDLE,$path) $_port_handle
    }
}

set _result_ [::ixia::interface_config  \
    -mode modify \
    -port_handle $ixnHLT(PORT-HANDLE,//vport:<1>) \
    -connected_count 1 \
	-ipv6_intf_addr ::0 \
    -mss 1460 \
    -l23_config_type static_endpoint \
    -mtu 1500 \
]

set static_ip_handle [keylget _result_ interface_handle]

set _result_ [::ixia::interface_config  \
    -mode config \
    -port_handle $ixnHLT(PORT-HANDLE,//vport:<1>) \
    -l23_config_type static_endpoint \
    -ipv6_addr_mode autoconfig \
]

set _result_ [::ixia::test_control \
    -action start_protocol \
    -handle $static_ip_handle \
]

return "SUCCESS - $test_name - [clock format [clock seconds]]"