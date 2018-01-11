#################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    02-21-2013 Mchakravarthy - created sample
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
#    This sample connects to IxNetwork Tcl Proxy Server and displays the       #
#    proxy connection information                                              #
# Module:                                                                      #
#    The sample was tested on a LM1000TXS4 module.                             #
#                                                                              #
################################################################################

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}
################################################################################
# General script variables
################################################################################
set test_name                                   [info script]

################################################################################
# START - Connect to the chassis
################################################################################
puts "Starting - $test_name - [clock format [clock seconds]]"
puts "Start connecting to chassis ..."
set chassis_ip              10.205.16.54
set port_list               [list 2/5 2/6]
set break_locks             1
set tcl_server              127.0.0.1
set ixnetwork_tcl_server    10.205.16.127; # IP Address of the machine in which TCL Proxy server is running
set port_count              2
set username                cmgruser1
set cfgErrors               0

set connect_status [::ixia::connect                                 \
            -reset                                                  \
            -device               $chassis_ip                       \
            -port_list            $port_list                        \
            -break_locks          $break_locks                      \
            -tcl_server           $tcl_server                       \
            -ixnetwork_tcl_server $ixnetwork_tcl_server             \
            -interactive          1                                 \
            -tcl_proxy_username   $username                         ]
            
#puts  "Connect Status: $connect_status"
if {[keylget connect_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget connect_status log]"
    return 0
} else {
    array set truth [list  1 true 0 false]
    set connection_keys [list    using_tcl_proxy process_id session_id tcl_proxy_username server_version \
                                port rdp state start_time hostname username close_server_on_disconnect]
    foreach key $connection_keys {
        if {[catch {keylget connect_status connection.$key} key_value]} {
            puts "FAIL - $key not present in ::ixia::connect return values"
            incr cfgErrors
        } else {
            puts "$key:$key_value"
        }
    }
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
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
# END - Connect to the chassis
################################################################################
################################################################################
# START - DisConnect to the chassis
################################################################################
set cleanup_status [::ixia::cleanup_session -reset -port_handle [list $port_0 $port_1]]
if {[keylget cleanup_status status] != $::SUCCESS} {
    puts "FAIL - $test_name - [keylget cleanup_status log]"
    return 0
}
################################################################################
# END - DisConnect to the chassis
################################################################################
############################### SUCCESS or FAILURE #############################
if {$cfgErrors > 0} {
    puts "FAIL - $test_name  $cfgErrors Errors- [clock format [clock seconds]]"
    return 0
}
puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1

################################################################################


