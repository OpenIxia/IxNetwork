################################################################################
# Version 1.0    $Revision: 0 $
# $Author: Radu Antonescu $
#
#    Copyright © 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    2-25-2008 Radu Antonescu
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
#    This sample create 20 emulated L2TP clients setting number of             #
#    addresses used for one vpi/vci.                                           #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on a ATM/POS622-MultiRate-256Mb module.             #
#                                                                              #
################################################################################

package require Ixia

set test_name           [info script]

set chassisIP           10.205.19.229
set port_list           [list 2/1]

set tunnel_count        3
set sessions_per_tunnel 50

################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
################################################################################
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixia::connect                                         \
        -reset                                                              \
        -ixnetwork_tcl_server       localhost                               \
        -device                     $chassisIP                              \
        -port_list                  $port_list                              \
        ]
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
# Configure the interfaces
################################################################################
set interface_status [::ixia::interface_config                              \
        -port_handle                $port_0                                 \
        -mode                       config                                  \
        -speed                      oc3                                     \
        -intf_mode                  atm                                     \
        -tx_c2                      13                                      \
        -rx_c2                      13                                      \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

################################################################################
# Configure L2TP on the access port
################################################################################
set l2tp_status [::ixia::l2tp_config                                        \
        -port_handle                $port_0                                 \
        -mode                       lac                                     \
        -l2_encap                   atm_snap                                \
        -num_tunnels                $tunnel_count                           \
        -sessions_per_tunnel        $sessions_per_tunnel                    \
        -l2tp_src_addr              12.70.0.2                               \
        -l2tp_dst_addr              12.70.0.1                               \
        -l2tp_src_count             $tunnel_count                           \
        -l2tp_src_step              0.0.0.1                                 \
        -l2tp_dst_step              0.0.0.0                                 \
        -vci                        32                                      \
        -vpi                        1                                       \
        -tun_distribution           next_tunnelfill_tunnel                  \
        -attempt_rate               100                                     \
        -tun_auth                                                           \
        -hostname                   b2b                                     \
        -secret                     ixia                                    \
        -auth_mode                  chap                                    \
        -username                   user                                    \
        -password                   pass                                    \
        -vpi_step                   2                                       \
        -vci_step                   2                                       \
        -addr_count_per_vci         4                                       \
        -addr_count_per_vpi         5                                       \
        ]
if {[keylget l2tp_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget l2tp_status log]"
    return
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
