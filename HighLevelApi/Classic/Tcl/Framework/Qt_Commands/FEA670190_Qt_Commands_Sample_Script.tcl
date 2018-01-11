#################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    02-27-2013 Mchakravarthy - created sample
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
# This is sample script is created for the feature implementation QT commands  #
# Support in HLTAPI                                                            #
# The following are the new commands (actions for ::ixia::test_control) added  #
# in HLTAPI                                                                    #
# 1.    get_all_qt_handles                                                     #
# 2.    get_available_qt_types                                                 #
# 3.    get_qt_handles_for_type                                                #
#                                                                              #
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

#############################################################################
# General script variables
#############################################################################
set test_name               [info script]
set test_name_folder        [file dirname $test_name]
set ixn_cfg                 "$test_name_folder/qt_sample_config.ixncfg"
set chassis_ip              10.205.16.54
set ixnetwork_tcl_server    127.0.0.1
set tcl_server              127.0.0.1
set port_list               [list 2/5 2/6]
set start_time              [clock seconds]

puts "Script Start Time    : [clock format $start_time] ($start_time)"

#############################################################################
# START - Connect to the chassis
#############################################################################

set connect_status [::ixia::connect                 \
    -device                 $chassis_ip             \
    -config_file            $ixn_cfg                \
    -ixnetwork_tcl_server   $ixnetwork_tcl_server   \
    -interactive            1                       \
    -tcl_server             $tcl_server             \
    -port_list              $port_list              \
     ]

if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
        return 0
}

#############################################################################
# END - Connect to the chassis
#############################################################################
#############################################################################
#   ACTION - get_available_qt_types                                         #
#############################################################################

puts "get_available_qt_types ......"
set test_control_status [::ixia::test_control       \
        -action             get_available_qt_types  \
        ]
if {[keylget test_control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget test_control_status log]"
    return 0
}
set qt_types [keylget test_control_status qt_types]
puts "qt_types=$qt_types"

#############################################################################
#   ACTION - get_qt_handles_for_type                                        #
#############################################################################

foreach qt_type $qt_types {
    puts "List of all test handles for qt type $qt_type"
    set test_control_status [::ixia::test_control       \
            -action             get_qt_handles_for_type \
            -qt_type            $qt_type                \
            ]
    if {[keylget test_control_status status] != $::SUCCESS} {
        puts "FAIL - $test_name - [keylget test_control_status log]"
        return 0
    }
    set qt_handle [keylget test_control_status qt_handle]
    puts "Test Handles: - $qt_handle"
}

#############################################################################
#   ACTION - get_all_qt_handles                                             #
#############################################################################
puts "get_all_qt_handles ......"
set test_control_status [::ixia::test_control   \
        -action         get_all_qt_handles      ]
    
if {[keylget test_control_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget test_control_status log]"
    return 0
}

set qt_handles [keylget test_control_status qt_handle]

puts "Handles Retrieved:- "
foreach qt_handle $qt_handles {
    puts $qt_handle
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1

