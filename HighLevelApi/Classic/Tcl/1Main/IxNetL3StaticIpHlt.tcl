#!/usr/bin/tclsh

package req Ixia

# Description:
#
#         Any packets destination address to 10.1.1.1, forwards to 2.2.2.2
#
#                       |----------------------------------|
#    IxPort1 1.1.1.1 -->|1.1.1.2    DUT/10.1.1.1    2.2.2.1|--> IxPort2 2.2.2.2
#                       |----------------------------------|
# 
# Solution:
#
#       -Create a static ip address on IxRxPort2 of 10.1.1.1.
#           - We are faking Ixia to let it think the static ip 10.1.1.1 is behind 2.2.2.2.
#             In reality, it is actually in front.
#           - The packets egressing the DUT will have:
#                srcIp = 1.1.1.1 dstIp = 10.1.1.1.  We could track destIp this way.
#
#       -On TrafficItem edit, srcPort selects interface, dstPort selects static.
#       -Flow Tracking select dest_ip.
#
#    .ixncfg file
#    
#       - scenario_1.ixncfg
#
# 

set ixiaChassisIp 10.205.4.35
set ixNetworkTclServerIp 10.205.1.42
set userName hgee
set portList "1/1 1/2"
set port1 1/1/1
set port2 1/1/2

puts "\nConnecting to $ixNetworkTclServerIp ..."
puts "Rebooting ports $portList ..."

set connectStatus [::ixia::connect \
 		       -reset \
		       -device $ixiaChassisIp \
		       -port_list $portList \
		       -ixnetwork_tcl_server $ixNetworkTclServerIp \
		       -tcl_server $ixiaChassisIp \
		       -username $userName \
		  ]

if {[keylget connectStatus status] != $::SUCCESS} {
    puts "Connecting to ixNetwork Tcl server failed\n\n$connectStatus\n"
    exit
} 

set port1Status [::ixia::interface_config \
		     -mode config \
		     -port_handle $port1 \
		     -intf_ip_addr 1.1.1.1 \
		     -gateway 1.1.1.2 \
		     -netmask 255.255.255.0 \
		     -src_mac_addr 00:01:01:01:00:01 \
		    ]
set port1Interface [keylget port1Status interface_handle]


set port2Status [::ixia::interface_config \
		     -mode config \
		     -port_handle $port2 \
		     -intf_ip_addr 2.1.1.2 \
		     -intf_ip_addr_step 0.0.0.1 \
		     -connected_count 5 \
		     -gateway 2.1.1.1 \
		     -gateway_step 0.0.0.0 \
		     -netmask 255.255.255.0 \
		     -src_mac_addr 00:01:01:02:00:01 \
		     -src_mac_addr_step 0000.0000.0001 \
		    ]

set port2Interface [keylget port2Status interface_handle]


# Configure the static IP address to 10.1.1.1 on the DUT
set port2StaticIp [::ixia::interface_config  \
		  -mode modify \
		  -port_handle $port2 \
		  -static_ip_dst_count 1 \
		  -static_ip_dst_addr 10.1.1.1 \
		  -static_l3_protocol ipv4 \
		  -static_ip_dst_prefix_len 32 \
		  -static_enable 1 \
		  -static_ip_dst_increment 0.0.0.1 \
		  -static_intf_handle $port2Interface \
		 ]
if {[keylget port2StaticIp status] != $::SUCCESS} {
    puts "Error: Failed to configure static IP on $port2 $port2Interface"
}
set port2StaticInterface [keylget port2StaticIp interface_handle]

puts "\nport2StaticInterface: $port2StaticInterface\n"

# port1Interface = ::ixNet::OBJ-/vport:1/interface:1
# port2Interfaces = ::ixNet::OBJ-/vport:2/interface:1 

# transmit_mode options: single_burst or continuous
# -transmit_distribution options:
# frameSize0 ethernetIiDestinationaddress0 srcDestEndpointPair0 rxPort0 ipv4DestIp0 ipv4Precedence0 ethernetIiEtherType0 ethernetIiPfcQueue0 ethernetIiSourceaddress0 ipv4SourceIp0
set trafficItem1 [::ixia::traffic_config \
		      -mode create \
		      -emulation_src_handle $port1Interface \
		      -emulation_dst_handle $port2StaticInterface \
		      -track_by  "sourceDestValuePair0 flowGroup0 ipv4_dest_ip" \
		      -name "TrafficItem_1" \
		      -bidirectional 0 \
		      -rate_percent 10 \
		      -pkts_per_burst 10000 \
		      -transmit_mode single_burst \
		      -frame_size 100 \
		      -transmit_distribution {frameSize0 ethernetIiDestinationaddress0 srcDestEndpointPair0 rxPort0 ipv4DestIp0 ipv4Precedence0 ethernetIiEtherType0 ethernetIiPfcQueue0 ethernetIiSourceaddress0 ipv4SourceIp0} \
		     ]

puts "\nStarting IxNetwork traffic ..."
set trafficControlStatus [ixia::traffic_control \
			      -port_handle $port1 \
			      -action run \
			     ]
if {[keylget trafficControlStatus status] != $::SUCCESS} {
    puts "\nIxia traffic failed to start on port $portList"
} else {
    puts "\nTraffic started on port $portList"
}

# Wait 10 seconds and collect stats
after 10000

set flowStats [::ixia::traffic_stats \
		   -mode flow \
	      ]
if {[keylget flowStats status] != $::SUCCESS} {
    puts "Failed to get statistics"
    exit
}

puts \n
puts "[format %-10s FlowGroup][format %10s TxPort][format %10s RxPort][format %14s TxFrames][format %14s RxFrames][format %14s destIp]"
puts "------------------------------------------------------------------------"

for {set flowNumber 1} {$flowNumber <= [llength [keylget flowStats flow]]} {incr flowNumber} {
    set txPort [keylget flowStats flow.$flowNumber.tx.port]
    set rxPort [keylget flowStats flow.$flowNumber.rx.port]
    set txFrames [keylget flowStats flow.$flowNumber.tx.total_pkts]
    set rxFrames [keylget flowStats flow.$flowNumber.rx.total_pkts]
    
    # flow_name: 1/1/2 TI0-TrafficItem_1 1.1.1.6 TI0-TrafficItem_1-EndpointSet-1 - Flow Group 0001
    set flowName [keylget flowStats flow.$flowNumber.flow_name]
    regexp "TrafficItem_\[0-9]+ *(\[0-9]+\.\[0-9]+\.\[0-9]+\.\[0-9]+)" $flowName - destIp
  
    puts "[format %5s $flowNumber][format %15s $txPort][format %10s $rxPort][format %14s $txFrames][format %14s $rxFrames][format %14s $destIp]"
}
