#################################################################################
# Version 1    $Revision: 3 $
# $Author: MChakravarthy $
#
#    Copyright © 1997 - 2013 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    07-20-2007 Mchakravarthy - created sample
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
#   This sample Configures interfaces on the ports and modifies the values 	   #
#	of arp and ndp in the configured interface and verifies it				   #
#                                                                              #
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
set cfgError									0
set chassis_ip									10.205.16.54
set port_list									[list 2/5 2/6]
set ixnetwork_tcl_server						127.0.0.1
set port_count									2
################################################################################
# START - Connect to the chassis
################################################################################
# Connect to the chassis, reset to factory defaults and take ownership
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect

set connect_status [::ixia::connect                 \
        -reset                                      \
        -device               $chassis_ip           \
        -port_list            $port_list            \
        -username             ixiaApiUser           \
        -tcl_server           $tcl_server           \
        -ixnetwork_tcl_server $ixnetwork_tcl_server \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
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
update idletasks

catch {unset interface_hanles}

########################################
# Configure interface port_0		   #
########################################

set _result_ [::ixia::interface_config                          \
    -mode                               config                  \
    -port_handle                        $port_0                 \
    -transmit_clock_source              external                \
    -internal_ppm_adjust                0                       \
    -enable_data_center_shared_stats    0                       \
    -additional_fcoe_stat_1             fcoe_invalid_delimiter  \
    -additional_fcoe_stat_2             fcoe_invalid_frames     \
    -data_integrity                     1                       \
    -intf_mode                          ethernet                \
    -speed                              ether100                \
    -duplex                             full                    \
    -autonegotiation                    1                       \
    -phy_mode                           copper                  \
    -tx_gap_control_mode                average                 \
    -transmit_mode                      advanced                \
    -port_rx_mode                       packet_group            \
    ]

#Check status
if {[keylget _result_ status] != $::SUCCESS}     {
  puts "Fail - Interface Config failed"
  return 0 
}

########################################
# Configure interface port_1		   #
########################################

set _result_ [::ixia::interface_config                          \
    -mode                               config                  \
    -port_handle                        $port_1                 \
    -transmit_clock_source              external                \
    -internal_ppm_adjust                0                       \
    -enable_data_center_shared_stats    0                       \
    -additional_fcoe_stat_1             fcoe_invalid_delimiter  \
    -additional_fcoe_stat_2             fcoe_invalid_frames     \
    -data_integrity                     1                       \
    -intf_mode                          ethernet                \
    -speed                              ether100                \
    -duplex                             full                    \
    -autonegotiation                    1                       \
    -phy_mode                           copper                  \
    -tx_gap_control_mode                average                 \
    -transmit_mode                      advanced                \
    -port_rx_mode                       packet_group            \
    ]   
    
#Check status
if {[keylget _result_ status] != $::SUCCESS}     {
  puts "Fail - Interface Config failed"
  return 0 
}
    
# -enable_ndp 1
# enables neighbor discovery, default 1
# -arp 1
# enables arp requests, default 1
# -arp_send_req 1
# sends arp requests after ports are up
# -ndp_send_req 1
# sends neighbor discovery/solicitation after ports are up

########################################
# Modify interface port_0    		   #
########################################

set _result_ [::ixia::interface_config                  \
    -mode                           modify              \
    -port_handle                    $port_0             \
    -mtu                            1500                \
    -vlan                           0                   \
    -l23_config_type                protocol_interface  \
    -gateway                        8.0.0.1             \
    -intf_ip_addr                   8.0.0.2             \
    -netmask                        255.255.255.0       \
    -check_opposite_ip_version      0                   \
    -src_mac_addr                   0000.2ce1.01ba      \
    -arp_on_linkup                  1                   \
    -ns_on_linkup                   0                   \
    -single_arp_per_gateway         1                   \
    -single_ns_per_gateway          1                   \
]
#Check status
if {[keylget _result_ status] != $::SUCCESS}     {
    puts "Fail - Interface Config failed"
    return 0 
}

########################################
# Modify interface port_1    		   #
########################################


set _result_ [::ixia::interface_config                  \
    -mode                           modify              \
    -port_handle                    $port_1             \
    -mtu                            1500                \
    -vlan                           0                   \
    -l23_config_type                protocol_interface  \
    -gateway                        8.0.0.2             \
    -intf_ip_addr                   8.0.0.1             \
    -netmask                        255.255.255.0       \
    -check_opposite_ip_version      0                   \
    -src_mac_addr                   0000.2ce1.01bb      \
    -arp_on_linkup                  1                   \
    -ns_on_linkup                   0                   \
    -single_arp_per_gateway         1                   \
    -single_ns_per_gateway          1                   \
]

#Check status
if {[keylget _result_ status] != $::SUCCESS}     {
    puts "Fail - Interface Config failed"
    return 0 
}

after 30000

########################################
# Modify interface port_0 and port_1   #
########################################

set interface_status [::ixia::interface_config											\
        -mode						modify												\
        -port_handle				[list $port_0 $port_1]								\
	 	-arp						1													\
		-arp_send_req				1 													\
		-enable_ndp 				1													\
		-ndp_send_req 				1													\
		]
if {[keylget interface_status status] != $SUCCESS} {
    puts "FAIL - $test_name - [keylget interface_status log]"
    return
}


set failed_count 0
foreach port [list $port_0 $port_1] {
	if {[catch {set failed_arp [keylget interface_status \
			$port.arp_request_success]}] || $failed_arp == 0} {
			
		
		if {![catch {set intf_list [keylget \
			interface_status $port.arp_ipv4_interfaces_failed]}]} {
			puts  "ARP failed on interfaces: $intf_list."
		}
		incr failed_count
	}
}
if { $failed_count } {
	puts "FAIL - $test_name arp send request failed. "
	return 0
}

puts "SUCCESS - $test_name - [clock format [clock seconds]]"
return 1


