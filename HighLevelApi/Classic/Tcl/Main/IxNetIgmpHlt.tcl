#!/opt/ActiveTcl-8.5/bin/tclsh

################################################################################
#                                                                            
# Description:                                                               
#    This script creates an IGMP v2 host and adds multicast group pool to the host.
#    Starts IGMP protocol emulation.  Streams are generated using ixnetwork 
#    traffic_generator. Traffic statistics are collected for each flow.  
#
################################################################################
#
# interface GigabitEthernet 1/0/19
#  switchport
#  switchport trunk encapsulation dot1q
#  switch mode trunk
#  no shut
# !

# interface GigabitEthernet 1/0/20
#  no switchport
#  ip address 21.0.0.1 255.255.255.0
#  no shutdown

# interface vlan 101
# ip address 1.1.101.1 255.255.255.0
# ip pim dense-mode
# no shut
# exit

# interface vlan 102
# ip address 1.1.102.1 255.255.255.0
# ip pim dense-mode
# no shut
# exit
################################################################################


package require Ixia

set network_tcl_server_ip 10.205.1.42
set chassisIP 10.205.4.172
set port_list "1/1 1/2"

proc keylprint {keylist {space ""}} {
    upvar $keylist kl
    set result ""
    foreach key [keylkeys kl] {
	set value [keylget kl $key]
	if {[catch {keylkeys value}]} {
	    append result "$space$key: $value\n"
	} else {
	    set newspace "$space "
	    append result "$space$key:\n[keylprint value $newspace]"
	}
    }
    return $result
}

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
			-reset \
			-device                         $chassisIP      \
			-ixnetwork_tcl_server $network_tcl_server_ip    \
			-port_list                      $port_list      \
			-username                       user             \
			-tcl_server $chassisIP \
        ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "\Error: Failed to connect:\n[keylget connect_status log]"
    exit
}
set port_tx [keylget connect_status port_handle.$chassisIP.[lindex $port_list 0]]
set port_rx [keylget connect_status port_handle.$chassisIP.[lindex $port_list 1]]
set port_handle [list $port_rx $port_tx]

puts "\nport_tx: $port_tx\n"
puts "port_rx: $port_rx\n"
puts "port_handle: $port_handle\n"

set interface_status [::ixia::interface_config \
			  -port_handle $port_rx  \
			  -autonegotiation 1 \
			  -duplex full \
			  -speed auto \
			 ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "\nError: Interface config:\n[keylget interface_status log]"
    exit
}

###################################################################
# Configure port properties and Protocol Interface on the TX port
###################################################################
set interface_status [::ixia::interface_config \
        -port_handle      $port_tx \
        -autonegotiation 1 \
        -duplex          full \
        -speed           auto \
        -intf_ip_addr    1.0.101.7 \
        -gateway         1.0.101.254 \
        -netmask         255.255.255.0 \
        -vlan            1 \
        -vlan_id         101 \
        ]
if {[keylget interface_status status] != $::SUCCESS} {
    puts "\nError: Interface config:\n[keylget interface_status log]"
    exit
}
set int_handle [keylget interface_status interface_handle]

##################################################
#  Configure interfaces and create IGMP sessions #
##################################################
set session_handle_list {}
set igmp_status [::ixia::emulation_igmp_config          \
        -port_handle                    $port_rx        \
        -reset                                          \
        -mode                           create          \
        -msg_interval                   0               \
        -igmp_version                   v2              \
        -ip_router_alert                0               \
        -general_query                  0               \
        -group_query                    0               \
        -count                          1               \
        -intf_ip_addr                   1.0.101.8       \
        -neighbor_intf_ip_addr          1.0.101.254       \
        -intf_prefix_len                24              \
        -vlan                           1               \
        -vlan_id                        101             \
        ]
if {[keylget igmp_status status] != $::SUCCESS} {
    puts "Error: igmp emulation config:\n[keylget igmp_status log]"
    exit
}

lappend session_handle_list [keylget igmp_status handle]

##################################################
#  Configure interfaces and create IGMP sessions #
##################################################
set igmp_status [::ixia::emulation_igmp_config          \
        -port_handle                    $port_rx        \
        -mode                           create          \
        -msg_interval                   0               \
        -igmp_version                   v2              \
        -ip_router_alert                0               \
        -general_query                  0               \
        -group_query                    0               \
        -count                          1               \
        -intf_ip_addr                   1.0.102.8       \
        -neighbor_intf_ip_addr          1.0.102.254       \
        -intf_prefix_len                24              \
        -vlan                           1               \
        -vlan_id                        102             \
        ]
if {[keylget igmp_status status] != $::SUCCESS} {
    puts "Error: Creating igmp config:\n[keylget igmp_status log]"
    exit
}
lappend session_handle_list [keylget igmp_status handle]

##################################################
# Create multicast group pool
##################################################
set mcast [::ixia::emulation_multicast_group_config     \
        -mode create                                    \
        -num_groups                     10               \
        -ip_addr_start                  225.0.0.1       \
        -ip_addr_step                   0.0.0.1         \
        -ip_prefix_len                  24              \
        ]
if {[keylget mcast status] != $::SUCCESS} {
    puts "Error: Multicast group config:\n[keylget mcast log]"
    exit
}
set group_handle_1 [keylget mcast handle]


set mcast [::ixia::emulation_multicast_group_config     \
        -mode create                                    \
        -num_groups                     10              \
        -ip_addr_start                  235.0.0.1       \
        -ip_addr_step                   0.0.0.1         \
        -ip_prefix_len                  24              \
        ]
if {[keylget mcast status] != $::SUCCESS} {
    puts "Error: Multicast group config:\n[keylget mcast log]"
    exit
}

set group_handle_2 [keylget mcast handle]

puts "\nsession_handle_list: $session_handle_list\n"

############################################################################
# Create IGMP group member by asociating a multicast group pool to a session
############################################################################
set gr_status [::ixia::emulation_igmp_group_config      \
        -mode                           create          \
        -session_handle                 [lindex $session_handle_list 0] \
        -group_pool_handle              $group_handle_1   \
        ]

if {[keylget gr_status status] != $::SUCCESS} {
    puts "Error: Configuring igmp group: \n[keylget gr_status log]"
    exit
}

set igmp_group_handles_host1 [keylget gr_status handle]

set gr_status [::ixia::emulation_igmp_group_config      \
        -mode                           create          \
        -session_handle                 [lindex $session_handle_list 0] \
        -group_pool_handle              $group_handle_2   \
        ]

if {[keylget gr_status status] != $::SUCCESS} {
    puts "Error: Configuring igmp group:\n[keylget gr_status log]"
    exit
}

lappend igmp_group_handles_host1 [keylget gr_status handle]

set gr_status [::ixia::emulation_igmp_group_config      \
        -mode                           create          \
        -session_handle                 [lindex $session_handle_list 1] \
        -group_pool_handle              $group_handle_1   \
        ]

if {[keylget gr_status status] != $::SUCCESS} {
    puts "Error: Configuring igmp groups:\n[keylget gr_status log]"
    exit
}

set igmp_group_handles_host2 [keylget gr_status handle]

# session_handle_list: ::ixNet::OBJ-/vport:2/protocols/igmp/host:1 ::ixNet::OBJ-/vport:2/protocols/igmp/host:2

#igmp_group_handles_host1: ::ixNet::OBJ-/vport:2/protocols/igmp/host:1/group:1 ::ixNet::OBJ-/vport:2/protocols/igmp/host:1/group:2

#igmp_group_handles_host2: ::ixNet::OBJ-/vport:2/protocols/igmp/host:2/group:1

#group_handle_1: group1
#group_handle_2: group2

puts "\nigmp_group_handles_host1: $igmp_group_handles_host1\n"
puts "igmp_group_handles_host2: $igmp_group_handles_host2\n"
puts "group_handle_1: $group_handle_1\n"
puts "group_handle_2: $group_handle_2\n"

set gr_status [::ixia::emulation_igmp_group_config      \
        -mode                           create          \
        -session_handle                 [lindex $session_handle_list 1] \
        -group_pool_handle              $group_handle_2   \
        ]

if {[keylget gr_status status] != $::SUCCESS} {
    puts "Error: Config igmp groups:\n[keylget gr_status log]"
    exit
}

lappend igmp_group_handles_host2 [keylget gr_status handle]


######################################
# Start the IGMP protocol emulation  #
######################################
set igmp_emulation_status [::ixia::emulation_igmp_control \
        -handle                    $session_handle_list   \
        -mode                      start           \
        ]
if {[keylget igmp_emulation_status status] != $::SUCCESS} {
    puts "Error: Starting igmp protocol:\n[keylget igmp_emulation_status log]"
    exit
}




######################################
# Gather statistics IGMP statistics  #
######################################
after 10000
set igmp_routers_info [::ixia::emulation_igmp_info      \
			   -port_handle                    $port_rx        \
			   -mode                           aggregate       \
			  ]
if {[keylget igmp_routers_info status] != $::SUCCESS} {
    puts "Error: Getting igmp aggregate stats:\n[keylget igmp_routers_info log]"
}


set igmp_stats [list                                    \
		    "Host v1 Membership Rpts. Rx"                   \
		    $port_rx.igmp.aggregate.rprt_v1_rx      \
		    "Host v2 Membership Rpts. Rx"                   \
		    $port_rx.igmp.aggregate.rprt_v2_rx      \
		    "v1 Membership Rpts. Tx"                        \
		    $port_rx.igmp.aggregate.rprt_v1_tx      \
		    "v2 Membership Rpts. Tx"                        \
		    $port_rx.igmp.aggregate.rprt_v2_tx      \
		    "v3 Membership Rpts. Tx"                        \
		    $port_rx.igmp.aggregate.rprt_v3_tx      \
		    "v2 Leave Tx"                                   \
		    $port_rx.igmp.aggregate.leave_v2_tx     \
		    "Host Total Frames Tx"                          \
		    $port_rx.igmp.aggregate.total_tx        \
		    "Host Total Frames Rx"                          \
		    $port_rx.igmp.aggregate.total_rx        \
		    "Host Invalid Packets Rx"                       \
		    $port_rx.igmp.aggregate.invalid_rx      \
		    "General Queries Rx"                            \
		    $port_rx.igmp.aggregate.gen_query_rx    \
		    "Grp. Specific Queries Rx"                      \
		    $port_rx.igmp.aggregate.grp_query_rx    \
		   ]
puts "Port $port_rx:"
foreach {name key} $igmp_stats {
    puts "\t$name: [keylget igmp_routers_info $key]"
}

puts "src_emulation_handle: $int_handle"
puts "dest_emulation_handle: $igmp_group_handles_host2"

#########################################
#  Configure traffic                    #
#########################################
set traffic_status [::ixia::traffic_config \
			-mode                 create \
			-traffic_generator    ixnetwork \
			-emulation_src_handle $int_handle \
			-emulation_dst_handle $igmp_group_handles_host2 \
			-src_dest_mesh        one_to_one \
			-track_by             endpoint_pair \
			-circuit_type           none \
			-circuit_endpoint_type ipv4 \
			-egress_tracking        outer_vlan_id_12 \
			-stream_packing       one_stream_per_endpoint_pair \
			-transmit_mode        continuous \
			-length_mode          fixed \
			-frame_size           256 \
			-burst_loop_count       1 \
			-pkts_per_burst         9999 \
			-rate_pps               1000 \
		       ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "Error: traffic_config:\n[keylget traffic_status log]"
    exit
}


################################################################################
# Start the traffic                                                            #
################################################################################
set traffic_status [::ixia::traffic_control \
			-action run \
			-max_wait_timer         120 \
			-packet_loss_duration_enable 1 \
		       ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "Error: Starting traffic:\n[keylget traffic_status log]"
    exit
}

if {[keylget traffic_status stopped] == 1} {
    puts "Traffic is not started yet.  Waiting for another 2 seconds"
}


################################################################################
# The traffic must flow!                                                       #
################################################################################
after 5000

################################################################################
# Stop the traffic                                                             #
################################################################################
set traffic_status [::ixia::traffic_control \
			-action                 stop \
			-max_wait_timer         120 \
		       ]
if {[keylget traffic_status status] != $::SUCCESS} {
    puts "Error: Stopping traffic:\n[keylget traffic_status log]"
    exit
}



################################################################################
# Wait for the traffic to stop - the recommended wait is 30 second before issuing
# next command
################################################################################
puts "Wait 15 seconds ..."
after 15000

################################################################################
# Gather and display aggregate traffic statistics                              #
################################################################################
set aggregated_traffic_status [::ixia::traffic_stats \
				   -mode                   all \
				   -traffic_generator      ixnetwork \
				  ]
if {[keylget aggregated_traffic_status status] != $::SUCCESS} {
    puts "Error: Getting all stats:\n[keylget aggregated_traffic_status log]"
    exit
}

ixPuts "Aggregate Traffic Stats"
ixPuts "[keylprint aggregated_traffic_status]"

################################################################################
# Gather and display flow traffic statistics                                   #
################################################################################
set flow_traffic_status [::ixia::traffic_stats \
			     -mode flow \
			    ]
if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "Error: Getting flow stats:\n[keylget flow_traffic_status log]"
    exit

}

ixPuts "Flow Traffic Stats"
ixPuts "[keylprint flow_traffic_status]"

set flow_traffic_status [::ixia::traffic_stats \
			     -mode egress_by_flow \
			     -port_handle $port_rx \
			    ]

if {[keylget flow_traffic_status status] != $::SUCCESS} {
    puts "Error: Getting egress stats:\n[keylget flow_traffic_status log]"
    exit
}

puts "Finished retrieving stats per flow ..."

update idletasks
set flow_results [list                                                  \
            "Rx Frames"                     rx.total_pkts               \
            "Rx Frame Rate"                 rx.total_pkt_rate           \
            "Rx Bytes"                      rx.total_pkts_bytes         \
            "Rx Rate (Bps)"                 rx.total_pkt_byte_rate      \
            "Rx Rate (bps)"                 rx.total_pkt_bit_rate       \
            "Rx Rate (Kbps)"                rx.total_pkt_kbit_rate      \
            "Rx Rate (Mbps)"                rx.total_pkt_mbit_rate      \
            "First TimeStamp"               rx.first_tstamp             \
            "Last TimeStamp"                rx.last_tstamp              \
        ]

##set fid [open ${test_name}_[clock seconds].log w+]

set flow 1
### TK debug - changed $port_0 to $port_1
while {![catch {set flow_key [keylget flow_traffic_status $port_rx.egress.$flow]}]} {
    puts  "\tFlow $flow - [keylget flow_traffic_status $port_rx.egress.$flow.flow_name] - [keylget flow_traffic_status $port_rx.egress.$flow.flow_print]"

    ###  TK debug
    ###    [subst $[subst $flow_results]]

    foreach {name key} $flow_results {
        puts  "\t\t$name: [keylget flow_traffic_status $port_rx.egress.$flow.$key]"
    }
    incr flow
}

puts " ----- Flows = [expr $flow - 1] -----"


##close $fid

################################################################################
# Gather and display stream traffic statistics                                  #
################################################################################
set stream_traffic_status [::ixia::traffic_stats                        \
        -mode                   stream                                \
        -traffic_generator      ixnetwork                             \
        ]
if {[keylget stream_traffic_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget stream_traffic_status log]"
}
ixPuts "Stream Traffic Stats"
ixPuts "[keylprint stream_traffic_status]"

################################################################################
### Example of retrieving the Packet Loss Duration
################################################################################
set streamList [keylget stream_traffic_status $port_rx.stream]
set streamKeyList [keylkeys streamList]

ixPuts "------ Packet Loss Duration --------"
foreach streamKey $streamKeyList {
    ixPuts "$streamKey: [keylget stream_traffic_status $port_rx.stream.$streamKey.rx.pkt_loss_duration] msec"
}



return
#################################################################################
# Clean up the connection
#################################################################################
set cleanup_status [::ixia::cleanup_session \
			-port_handle $port_handle     ]
if {[keylget cleanup_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget cleanup_status log]"
}
