#!/opt/ActiveTcl-8.5/bin/tclsh

package req Ixia

set ixiaChassisIp 10.205.4.155
set ixNetworkTclServerIp 10.205.4.160
set userName hgee

source /home/hgee/IxiaScripts/IxNet/HLT/NGPF/ixiaHltLib.tcl

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

set status [::ixia::connect \
		-ixnetwork_tcl_server $ixNetworkTclServerIp \
		-tcl_server $ixiaChassisIp \
		-username $userName \
		-session_resume_keys 1 \
	       ]

set saveStatus [::ixia::connect \
		    -mode save \
		    -ixnetwork_tcl_server $ixNetworkTclServerIp \
		    -config_file mySavedConfig.ixncfg \
		    ]

puts "\n[KeylPrint saveStatus]"

