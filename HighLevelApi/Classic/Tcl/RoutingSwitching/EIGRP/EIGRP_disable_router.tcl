################################################################################
# Version 1.0    $Revision: 1 $
# $Author: LRaicea $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    10-16-2007 LRaicea - created sample
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
#    This sample creates 3 EIGRP routers with directly connected IPv4          #
#    interfaces and then, one router is disabled.                              #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000STXS4 module.                            #
#    The sample was tested with HLTSET27.                                      #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set start_time [clock clicks -milliseconds]
set totalTime 0

set chassisIP 127.0.0.1
set port_list [list 1/1]

# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect \
        -reset                      \
        -device    $chassisIP       \
        -port_list $port_list       \
        -username  ixiaApiUser      ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassisIP.$port} \
            temp_port]} {
        lappend port_handle $temp_port
    }
}
set port_0 [lindex $port_handle 0]
################################################################################
# Configure interface in the test
################################################################################
set interface_status [::ixia::interface_config \
        -port_handle     $port_0               \
        -autonegotiation 1                     \
        -duplex          auto 	               \
        -speed 	         auto                  ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}
################################################################################
# Configure EIGRP routers
################################################################################
set eigrp_create_status [::ixia::emulation_eigrp_config  \
        -mode                           create         \
        -reset             			                   \
        -port_handle                    $port_0        \
        -count      		            3              \
        -intf_ip_addr                   25.0.0.2       \
        -intf_ip_addr_step              1.0.0.0        \
        -intf_ip_prefix_length          24             \
        -intf_gw_ip_addr                25.0.0.1       \
        -intf_gw_ip_addr_step           1.0.0.0        \
        -vlan                           1              \
        -vlan_id                        25             \
        -vlan_id_step                   1              \
        -mac_address_init               0000.0000.0001 \
        -router_id                      25.0.0.2       \
        -router_id_step                 1.0.0.0        \
        -enable_piggyback               1              \
        -bfd_registration               1              \
        ]
if {[keylget eigrp_create_status status] != $::SUCCESS} {
    puts "FAIL - [keylget eigrp_router_status log]"
    return
}
set eigrp_router_1 [lindex [keylget eigrp_create_status router_handles] 1]

################################################################################
# Modify EIGRP routers
################################################################################
set eigrp_modify_status [::ixia::emulation_eigrp_config  \
        -mode                           disable          \
        -handle             			$eigrp_router_1  \
        ]
if {[keylget eigrp_modify_status status] != $::SUCCESS} {
    puts "FAIL - [keylget eigrp_modify_status log]"
    return
}

set total_time [expr [clock clicks -milliseconds] - $start_time]
puts   "SUCCESS - $total_time - $totalTime"
return "SUCCESS - $test_name - Time to complete: $total_time ms"
