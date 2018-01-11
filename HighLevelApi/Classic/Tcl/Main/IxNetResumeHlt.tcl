#!/opt/ActiveTcl-8.5/bin/tclsh

# Connect to an existing IxNetwork configuration.
#
 
package req Ixia

set ixiaChassisIp 10.219.117.x
set ixNetworkTclServerIp 10.219.117.x
set userName hgee
set portList "1/1 1/2"
set port1 1/1/1
set port2 1/1/2

proc GetTime {} {
    return [clock format [clock seconds] -format "%H:%M:%S"]
}

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

proc StartAllProtocolsHlt {} {
    puts "\nStartAllProtocolsHlt"
    set startProtocolStatus [::ixiangpf::test_control -action start_all_protocols]
    if {[keylget startProtocolStatus status] != $::SUCCESS} {
	puts "\nError: StartAllProtocolsHlt failed:  $startProtocolStatus\n"
	return 1
    }

    after 3000
    return 0
}

proc StartTrafficHlt {} {
    puts "\nStarting IxNetwork traffic ..."
    set status [ixia::traffic_control -action run]
    
    if {[keylget status status] != $::SUCCESS} {
	puts "\nIxia traffic failed to start: $status"
    } else {
	puts "\nTraffic started ..."
    }

    after 10000
}

proc GetStatsHlt { {type flow} } {
    puts "\nGetStatsHlt"
    set flowStats [::ixia::traffic_stats -mode $type]
    
    if {[keylget flowStats status] != $::SUCCESS} {
	puts "GetStatsHlt failed: $status"
	return 0
    }
    return $flowStats
}

puts "\nConnecting to $ixNetworkTclServerIp ..."

set status [::ixia::connect \
		-ixnetwork_tcl_server $ixNetworkTclServerIp \
		-tcl_server $ixiaChassisIp \
		-username $userName \
		-session_resume_keys 1 \
	       ]

set flowStats [GetStatsHlt flow]

StartTrafficHlt

# Example on how to get certain statistics.
puts "\n[KeylPrint flowStats]\n"

puts \n
puts "\t[format %-10s Flow][format %10s TxPktBitRate][format %15s RxPktBitRate][format %15s Result]"
puts "------------------------------------------------------------------------"

set belowThreshold 490422270

for {set flowNumber 1} {$flowNumber <= [llength [keylget flowStats flow]]} {incr flowNumber} {
    set txRate [keylget flowStats flow.$flowNumber.tx.total_pkt_bit_rate]
    set rxRate [keylget flowStats flow.$flowNumber.rx.total_pkt_bit_rate]
    if {$rxRate < $belowThreshold} {
	set result FAILED
    } else {
	set result Passed
    }
    puts "\t[format %-10s $flowNumber][format %10s $txRate][format %15s $rxRate][format %15s $result]"
}
