################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mircea Hasegan $
#
#    Copyright © 1997 - 2007 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    9-12-2008 Mircea Hasegan
#    3-17-2009 Adrian Iliesiu
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
#    This sample creates a BACK-TO-BACK setup.                                 #
#                                                                              #
#    It configures two IPv4 Ethernet interfaces and configures Ethernet OAM    #
#    using sequence_id and sequence_id_step parameters                         #
# Module:                                                                      #
#    The sample was tested on a TXS4 module.                                   #
#                                                                              #
################################################################################

package require Ixia

set test_name [info script]

set chassisIP sylvester
set port_list [list 1/1 1/2]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect                         \
        -reset                                              \
        -ixnetwork_tcl_server   localhost                   \
        -device                 $chassisIP                  \
        -port_list              $port_list                  ]
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
set port_1 [lindex $port_handle 1]

puts "Ixia port handles are $port_handle "

########################################
# L1 configurations                    #
########################################
set interface_status [::ixia::interface_config \
        -port_handle      $port_0     \
        -mode             config               \
        -speed            auto                 \
        -duplex           auto                 \
        -phy_mode         copper               \
        -autonegotiation  1                    ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

set interface_status [::ixia::interface_config \
        -port_handle      $port_1     \
        -mode             config               \
        -speed            auto                 \
        -duplex           auto                 \
        -phy_mode         copper               \
        -autonegotiation  1                    ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}

##########################################################################
# Configure Ethernet OAM port, Information and Event Notification OAMPDU #
##########################################################################

puts "\nConfiguring Ethernet OAM"
set efm_status [::ixia::emulation_efm_config    \
        -port_handle $port_0                    \
        -oam_mode                       active  \
        -link_events                            \
        -variable_retrieval                     \
        -error_frame_count              5       \
        -error_frame_period_count       6       \
        -error_frame_period_threshold   66      \
        -error_frame_period_window      660     \
        -error_frame_threshold          55      \
        -error_frame_window             550     \
        -error_frame_summary_count      7       \
        -error_frame_summary_threshold  77      \
        -error_frame_summary_window     770     \
        -error_symbol_period_count      8       \
        -error_symbol_period_threshold  88      \
        -error_symbol_period_window     880     \
        -size                           512     \
    ]
if {[keylget efm_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget efm_status log]"
    return
}

set efm_status [::ixia::emulation_efm_config    \
        -port_handle $port_0                    \
        -oam_mode                       active  \
        -link_events                            \
        -variable_retrieval                     \
        -error_frame_count              5       \
        -error_frame_period_count       6       \
        -error_frame_period_threshold   66      \
        -error_frame_period_window      660     \
        -error_frame_threshold          55      \
        -error_frame_window             550     \
        -error_frame_summary_count      7       \
        -error_frame_summary_threshold  77      \
        -error_frame_summary_window     770     \
        -error_symbol_period_count      8       \
        -error_symbol_period_threshold  88      \
        -error_symbol_period_window     880     \
        -size                           512     \
        -sequence_id                    15      \
        -sequence_id_step               10      \
    ]
if {[keylget efm_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget efm_status log]"
    return
}

set efm_status [::ixia::emulation_efm_config    \
        -port_handle $port_0                    \
        -oam_mode                       active  \
        -link_events                            \
        -variable_retrieval                     \
        -error_frame_count              5       \
        -error_frame_period_count       6       \
        -error_frame_period_threshold   66      \
        -error_frame_period_window      660     \
        -error_frame_threshold          55      \
        -error_frame_window             550     \
        -error_frame_summary_count      7       \
        -error_frame_summary_threshold  77      \
        -error_frame_summary_window     770     \
        -error_symbol_period_count      8       \
        -error_symbol_period_threshold  88      \
        -error_symbol_period_window     880     \
        -size                           512     \
        -sequence_id                    50      \
    ]
if {[keylget efm_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget efm_status log]"
    return
}

set efm_status [::ixia::emulation_efm_config    \
        -port_handle $port_1                    \
        -oam_mode                       passive \
        -link_events                            \
        -variable_retrieval                     \
        -error_frame_count              5       \
        -error_frame_period_count       6       \
        -error_frame_period_threshold   66      \
        -error_frame_period_window      660     \
        -error_frame_threshold          55      \
        -error_frame_window             550     \
        -error_frame_summary_count      7       \
        -error_frame_summary_threshold  77      \
        -error_frame_summary_window     770     \
        -error_symbol_period_count      8       \
        -error_symbol_period_threshold  88      \
        -error_symbol_period_window     880     \
        -size                           512     \
        ]
if {[keylget efm_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget efm_status log]"
    return
}

set efm_status [::ixia::emulation_efm_config    \
        -port_handle $port_1                    \
        -oam_mode                       passive \
        -link_events                            \
        -variable_retrieval                     \
        -error_frame_count              5       \
        -error_frame_period_count       6       \
        -error_frame_period_threshold   66      \
        -error_frame_period_window      660     \
        -error_frame_threshold          55      \
        -error_frame_window             550     \
        -error_frame_summary_count      7       \
        -error_frame_summary_threshold  77      \
        -error_frame_summary_window     770     \
        -error_symbol_period_count      8       \
        -error_symbol_period_threshold  88      \
        -error_symbol_period_window     880     \
        -sequence_id                    13      \
        -sequence_id_step               10      \
        -size                           512     \
        ]
if {[keylget efm_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget efm_status log]"
    return
}

set efm_status [::ixia::emulation_efm_config    \
        -port_handle $port_1                    \
        -oam_mode                       passive \
        -link_events                            \
        -variable_retrieval                     \
        -error_frame_count              5       \
        -error_frame_period_count       6       \
        -error_frame_period_threshold   66      \
        -error_frame_period_window      660     \
        -error_frame_threshold          55      \
        -error_frame_window             550     \
        -error_frame_summary_count      7       \
        -error_frame_summary_threshold  77      \
        -error_frame_summary_window     770     \
        -error_symbol_period_count      8       \
        -error_symbol_period_threshold  88      \
        -error_symbol_period_window     880     \
        -sequence_id                    100     \
        -size                           512     \
        ]
if {[keylget efm_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget efm_status log]"
    return
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"
