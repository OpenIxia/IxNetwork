################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Eduard Tutescu $
#
#    Copyright © 1997 - 2011 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    02-09-2013 Eduard Tutescu
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
#    This sample configures a traffic item and uses -mode replace_header to    #
#    replace one of the layer 4 headers.                                       #
#                                                                              #
# Module:                                                                      #
#    The sample was tested on STXS4 module                                     #
#                                                                              #
################################################################################
package require Ixia

set test_name [info script]

set chassisIP 10.215.180.134
set port_list "6/1 6/2"

### points to where ixNetwork Tcl Server is running
set network_tcl_server_ip 127.0.0.1

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect                     \
        -reset                                          \
        -device                         $chassisIP      \
        -ixnetwork_tcl_server $network_tcl_server_ip    \
        -port_list                      $port_list      \
        -username                       ixiaApiUser     \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}
set port_rx [keylget connect_status port_handle.$chassisIP.[lindex $port_list 0]]
set port_tx [keylget connect_status port_handle.$chassisIP.[lindex $port_list 1]]
set port_handle [list $port_rx $port_tx]

############################################################
# Configure port properites like speed and autonegogiation #
############################################################
set interface_status [::ixia::interface_config  \
        -port_handle      $port_rx        		\
        -autonegotiation  1               		\
        -duplex           full            		\
        -speed            auto            		\
		-intf_ip_addr     140.0.0.1            	\
        -gateway          140.0.0.2            	\
        -netmask          255.255.255.0        	\
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}


###################################################################
# Configure port properties and Protocol Interface on the TX port
###################################################################
set interface_status [::ixia::interface_config \
        -port_handle      $port_tx             \
        -autonegotiation  1                    \
        -duplex           full                 \
        -speed            auto                 \
        -intf_ip_addr     140.0.0.2            \
        -gateway          140.0.0.1            \
        -netmask          255.255.255.0        \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget interface_status log]"
}
set int_handle [keylget interface_status interface_handle]

#########################################
#  Configure traffic                    #
#########################################
set traffic_status [::ixia::traffic_config                  			\
            -mode                 		create                        	\
            -port_handle          		$port_tx						\
			-port_handle2	      		$port_rx 						\
            -traffic_generator    		ixnetwork                     	\
            -ip_src_addr   				198.0.0.1						\
            -circuit_type  	      		raw								\
            -circuit_endpoint_type   	ipv4							\
            -src_dest_mesh        		one_to_one                    	\
            -track_by             		endpoint_pair                 	\
            -transmit_mode        		continuous                    	\
            -length_mode          		increment                     	\
            -frame_size_step      		1                             	\
            -frame_size_min       		800                           	\
            -frame_size_max       		1500                          	\
            -rate_percent         		4.5                           	\
               ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}


set trafficItem [keylget traffic_status traffic_item]
set headers [keylget traffic_status $trafficItem.headers]
set streamId [lindex $headers 1]

set traffic_status [::ixia::traffic_config                  \
            -mode 			append_header 					\
            -stream_id 		$streamId						\
            -l4_protocol 	udp								\
            -udp_src_port 	1064							\
            -udp_dst_port 	1064							\
            ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}
set traffic_status [::ixia::traffic_config                  \
            -mode 			append_header 					\
            -stream_id 		$streamId						\
            -l4_protocol 	tcp								\
            -tcp_src_port 	1063							\
            -tcp_dst_port 	1063							\
            ]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}			
set trafficItem [keylget traffic_status traffic_item]
set headers [keylget traffic_status $trafficItem.headers]
set handle [lindex $headers 2]

set traffic_status [::ixia::traffic_config 	\
	-mode 				replace_header 		\
	-stream_id 			$handle 			\
	-traffic_generator 	ixnetwork_540 		\
	-l4_protocol 		udp 				\
	-udp_src_port 		1064 				\
	-udp_dst_port 		1064 				\
	]
if {[keylget traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget traffic_status log]"
}

return "SUCCESS - $test_name - [clock format [clock seconds]]"