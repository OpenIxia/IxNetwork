#!/opt/ActiveTcl-8.5/bin/tclsh

# This sample script only works for IxExplorer.
# Because IxNetwork only supports CSV format.
# 
# This script will log into the chassis without resetting
# any ports and configure the receiving port for capturing
# packets. Starts Traffic and capture packets.
#
# Note: 
#    Use 
#        -format txt 
#        -filename packetCapture.txt
#    to put all the packet captures into a txt file.
#    There will be many files 3.27MB size files though.
#
#    Use 
#        -format var 
#    to put the first 20 packets into a keyed list 
#
# 100:00:09.11952566000 01 01 04 00 0100 01 01 03 00 0108
# 045 00 00 4E 00 00 00 00 4F 3D 67 6F 01 01 01 01 01 01 01 02 CA CC 86 6C 26
# D8 9C C8 49 78 69 60 00 0D 0E 0F 00 00 00 00 A9 78 0F 12 00 1E 1A 1B 1C 1D 1E 1F 
# 0 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F 30 31 32 33 34 35 36 37 74 E0 81 8
# C2 7096Good Packet


package req Ixia

set ixiaChassisIp 10.219.117.101
set ixNetworkTclServerIp 10.219.117.103
set userName hgee
set portList "1/1 1/2"
set port1 1/1/1
set port2 1/1/2
set rxCapturePort $port2

proc KeylPrint {keylist {space ""}} {
    upvar $keylist kl
    set result ""
    foreach key [keylkeys kl] {
	set value [keylget kl $key]
	if {[catch {keylkeys value}]} {
	    append result "$space$key: $value\n"
	} else {
	    set newspace "$space "
	    append result "$space$key:\n[KeylPrint value $newspace]"
	}
    }
    return $result
}

puts "\nConnecting to $ixNetworkTclServerIp ..."

if 0 {
set connectStatus [::ixia::connect \
		       -ixnetwork_tcl_server $ixNetworkTclServerIp \
		       -tcl_server $ixiaChassisIp \
		       -username $userName \
		       -session_resume_keys 1 \
		  ]

if {[keylget connectStatus status] != $::SUCCESS} {
    puts "Connecting to ixNetwork Tcl server failed\n\n$connectStatus\n"
    exit
} 
after 5000
}


set connectStatus [::ixiangpf::connect \
		-ixnetwork_tcl_server $ixNetworkTclServerIp \
		-tcl_server $ixiaChassisIp \
		-username $userName \
		-session_resume_keys 1 \
	       ]

puts \n$connectStatus\n
puts [KeylPrint connectStatus]

#--------------- Below codes are for including filtering ---------------
set captureBuffer [::ixia::packet_config_buffers  \
		       -port_handle $port2 \
		       -data_plane_capture_enable 1 \
		       -control_plane_capture_enable 0 \
		       -slice_size 0 \
		       -trigger_position 1 \
		       -capture_mode trigger \
		       -after_trigger_filter filter \
		       -before_trigger_filter none \
		       -continuous_filter filter \
		      ]

puts "\ncaptureBuffer: [KeylPrint captureBuffer]\n"

set captureFilter [::ixia::packet_config_filter  \
		       -port_handle $port2 \
		       -pattern_offset_type1 startOfFrame \
		       -pattern_offset_type2 startOfFrame \
		       -DA1 {00 00 00 00 00 00} \
		       -DA2 {00 00 00 00 00 00} \
		       -DA_mask1 {00 00 00 00 00 00} \
		       -DA_mask2 {00 00 00 00 00 00} \
		       -pattern1 22 \
		       -pattern2 00 \
		       -pattern_mask1 00 \
		       -pattern_mask2 00 \
		       -pattern_offset1 42 \
		       -pattern_offset2 0 \
		       -SA1 {00 00 00 00 00 00} \
		       -SA2 {00 00 00 00 00 00} \
		       -SA_mask1 {00 00 00 00 00 00} \
		       -SA_mask2 {00 00 00 00 00 00} \
		      ]

# status = 1
puts "\ncaptureFilter: [KeylPrint captureFilter]\n"
# ----------------- Filtering done ------------------

puts "Starting capture.."
# Choices: data, control or both
set start_status [::ixia::packet_control \
		      -port_handle $port2    \
		      -packet_type data \
		      -action start \
    ]
if {[keylget start_status status] != $::SUCCESS} {
    puts "FAIL - $start_status"
    return 0
} else {
    puts "Config $port2 capture mode: $start_status"
}

ixNet exec saveCapture c:\\Results\\packetCapture
ixNet exec startCapture

::ixiangpf::test_control -action start_all_protocols

after 15000
::ixiangpf::test_control -action stop_all_protocols

if 0 {

set traffic_control_status [::ixia::traffic_control \
				-port_handle $port1 \
				-action      run \
			       ]
if {[keylget traffic_control_status status] != $::SUCCESS} {
    puts "FAIL - $traffic_control_status"
    return 0
}

after 15000

set traffic_control_status [::ixia::traffic_control \
				-port_handle $port1 \
				-action      stop \
				]
if {[keylget traffic_control_status status] != $::SUCCESS} {
    puts "FAIL - $traffic_control_status"
    return 0
}

puts "waiting traffic to stop"
puts "traffic stopped"
}

puts "Stopping capture..."

set stop_status [::ixia::packet_control \
        -port_handle $port2  \
        -action      stop  \
    ]
if {[keylget stop_status status] != $::SUCCESS} {
    puts "FAIL - $stop_status"
    return 0
}

#############################################
# Get capture and statistics to keyed list  #
#############################################
if 0 {
set stats_status [::ixia::packet_stats   \
		      -port_handle    $rxCapturePort  \
		      -format csv \
		      -filename packetCapture \
		      -dirname /home/hgee \
		     ]
}


set stats_status [::ixia::packet_stats   \
		      -port_handle    $rxCapturePort  \
		      -format txt \
		      -dirname /home/hgee \
		     ]
if {[keylget stats_status status] != $::SUCCESS} {
    puts "FAIL: $stats_status"
}


puts "\n$stats_status\n"

if 0 {
set stats_status [::ixia::packet_stats   \
		      -port_handle    $rxCapturePort  \
		      -format var \
		     ]

if {[keylget stats_status status] != $::SUCCESS} {
    puts "FAIL: $stats_status"
}
}

puts \n[KeylPrint stats_status]\n


