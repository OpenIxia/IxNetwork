#!/opt/ActiveTcl-8.5/bin/tclsh

# Description
#  
#    - This script will load a saved config file.
#
#    - To modify the Traffic Item, call the following APIs and provide the
#      exact spelling of the Traffic Item's name (Case sensitive).
#          - ModifyStreamFrameSizeHlt ospf-1 256
#          - ModifyStreamLineRateHlt  ospf-2 18
#          - ModifyStreamIpPrecedenceHlt ospf-2 4
# 
#    - Saving stats into csv file: Use the variable csvStatisticFile to state
#      the path and filename.
# 

package req Ixia

set ixiaChassisIp 10.219.117.102
set ixNetworkTclServerIp 10.219.16.219
set csvStatisticFile /home/hgee/Dropbox/MyIxiaWork/HLT/IxN_LoadConfigModifyStream.csv
set ixncfgFile /home/hgee/Dropbox/MyIxiaWork/Temp/ospf_ngpf_7.40.ixncfg
set totalIterations 3

set params {
    {
	{trafficItemName ospf frameSize 128 ipPrecedence 1 lineRate 10}
	{trafficItemName bgp  frameSize 256 ipPrecedence 3 lineRate 20}
    }
    
    {
	{trafficItemName ospf frameSize 128 ipPrecedence 5 lineRate 30}
	{trafficItemName bgp  frameSize 256 ipPrecedence 7 lineRate 40}
    }
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

proc Connect {} {
    if {[file exists $::ixncfgFile] == 0} {
	puts "\n\n** ixNet config file does not exists: $::ixncfgFile\n\n"
	exit
    }

    puts "\nLoading config file: $::ixncfgFile ..."
    set connectStatus [::ixiangpf::connect \
			   -config_file $::ixncfgFile \
			   -ixnetwork_tcl_server $::ixNetworkTclServerIp \
			   -tcl_server $::ixiaChassisIp \
			   -session_resume_keys 1 \
			   -connect_timeout 120 \
			   -break_locks 1 
		      ]
    
    if {[keylget connectStatus status] != $::SUCCESS} {
	puts "Connecting to IxNetwork Tcl server failed\n\n$connectStatus\n"
	exit
    } else {
	puts "Successfully connected to IxNetwork Tcl server"
    }
    
    puts "\n[KeylPrint connectStatus]\n"
    return $connectStatus
}

proc GetTrafficItemByName { trafficItemName } {
    # Search for the exact Traffic Item name and return the Traffic Item object"

    foreach trafficItem [ixNet getList [ixNet getRoot]traffic trafficItem] {
	set currentTiName [ixNet getAttribute $trafficItem -name]

	if {[regexp "(TI\[0-9]+)?$trafficItemName$" $currentTiName]} {
	    return $trafficItem
	}
    }
    # Retuning 0 if not found
    return 0
}

proc ModifyStreamLineRateHlt { trafficItemName ratePercentage } {
    # streamId format = ::ixNet::OBJ-/traffic/trafficItem:1

    set trafficItem [GetTrafficItemByName $trafficItemName]
    if {$trafficItem == "" || $trafficItem == "0"} {
	puts "\nError ModifyStreamTransmitModeHlt: No such Traffic Item name: $trafficItemName"
	return 1
    }

    puts "\nModifyStreamLineRateHlt: $streamId : $ratePercentage\%"
    set trafficItemStatus [eval ::ixia::traffic_config \
			       -mode modify \
			       -stream_id $trafficItem \
			       -rate_percent $ratePercentage \
			      ]
    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError ModifyStreamLineRateHlt: $trafficItemStatus\n"
	return 1
    }
    return 0
}

proc ModifyStreamFrameSizeHlt { trafficItemName framesize } {
    # trafficItemName = The Traffic Item name in exact spelling.
    # framesize = The framesize value to modify.

    # Note: The stream_id format = ::ixNet::OBJ-/traffic/trafficItem:1

    set trafficItem [GetTrafficItemByName $trafficItemName]
    if {$trafficItem == "" || $trafficItem == "0"} {
	puts "\nError ModifyStreamTransmitModeHlt: No such Traffic Item name: $trafficItemName"
	return 1
    }

    set trafficItem [GetTrafficItemByName $trafficItemName]
    if {$trafficItem == "" || $trafficItem == "0"} {
	puts "\nError ModifyStreamTransmitModeHlt: No such Traffic Item name: $trafficItemName"
	return 1
    }

    puts "\nModifyFrameSizeHlt: $trafficItem : $framesize"
    set trafficItemStatus [::ixia::traffic_config \
			      -mode modify \
			      -stream_id $trafficItem \
			      -frame_size $framesize \
			      ]

    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError ModifyFrameSizeHlt: $trafficItemStatus\n"
	return 1
    }
    return 0
}

proc ModifyStreamIpPrecedenceHlt { trafficItemName ipPrecedenceValue } {
    # streamId format = ::ixNet::OBJ-/traffic/trafficItem:1

    set trafficItem [GetTrafficItemByName $trafficItemName]
    if {$trafficItem == "" || $trafficItem == "0"} {
	puts "\nError ModifyStreamTransmitModeHlt: No such Traffic Item name: $trafficItemName"
	return 1
    }

    puts "\nModifyStreamIpPrecedenceHlt: $streamId : $ipPrecedenceValue"
    set trafficItemStatus [eval ::ixia::traffic_config \
			       -mode modify \
			       -stream_id $trafficItem \
			       -ip_precedence $ipPrecedenceValue \
			      ]
    if {[keylget trafficItemStatus status] != $::SUCCESS} {
	puts "\nError ModifyStreamIpPrecedenceHlt: $trafficItemStatus\n"
	return 1
    }
    return 0
}

proc VerifyPortState { {StopTimer 60} } {
    set portDownList {}
    set stopTime $StopTimer
    puts \n
    foreach vPort [ixNet getList [ixNet getRoot] vport] {
	set port [GetVportConnectedToPort $vPort]
	for {set timer 1} {$timer <= $stopTime} {incr timer} {
	    if {$timer == $stopTime} {
		lappend portDownList $port
	    }

	    if {[ixNet getAttribute $vPort -state] == "up"} {
		puts "VerifyPortState: $port is up"
		break
	    } else {
		puts "VerifyPortState: $port is still not up. Waited $timer/$stopTime seconds"
		after 1000
		continue
	    }
	}
    }

    if {$portDownList != ""} {
	puts "VerifyPortState: Ports can't come up: $portDownList\n"
	return 1
    }
    after 5000
    return 0
}

proc GetVportConnectedToPort { vport } {
    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
    set connectedTo [ixNet getAttribute $vport -connectedTo]
    set connectedTo [lrange [split $connectedTo /] 3 4]
    set card [lindex [split [lindex $connectedTo 0] :] end]
    set port [lindex [split [lindex $connectedTo 1] :] end]
    return $card/$port    
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
    
    set flag 0
    if {[keylget status status] != $::SUCCESS} {
	puts "\nIxia traffic failed to start: $status"
	set flag 1
    } else {
	puts "\nTraffic started ..."
    }

    after 10000
    return $flag
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

proc GetStatViewOnCsv { csvFileName {typeOfStats "Flow Statistics"}} {
    # This API will create and overwrite the existing
    # $csvFileName.
    # 
    # All Statistics will be written to $csvFileName
    # in csv format.
    #
    # typeOfStats options:
    #    "Flow Statistics"  (Default)
    #    "Port Statistics"
    #    "Tx-Rx Frame Rate Statistics"
    #    "Port CPU Statistics"
    #    "Global Protocol Statistics"
    #    "L2-L3 Test Summary Statistics"
    #    "Flow Detective"
    #    "Data Plane Port Statistics"
    #    "User Defined Statistics"
    #    "Traffic Item Statistics"
    # 

    exec echo "" > $csvFileName

    set viewList [ixNet getList [ixNet getRoot]/statistics view]
    puts "$viewList"
    set statViewSelection $typeOfStats

    set flowStatsViewIndex [lsearch -regexp $viewList $statViewSelection]
    if {$flowStatsViewIndex == -1} {
	puts "GetStatViewOnCsv: No \"$statViewSelection\" found"
	return 1
    }

    # $view: ::ixNet::OBJ-/statistics/view:"Flow Statistics"
    set view [lindex $viewList $flowStatsViewIndex]

    ixNet setAttribute $view -enabled true
    ixNet commit

    set columnList [ixNet getAttribute ${view}/page -columnCaptions]

    # Using a foreach loop to add a comma in between each item for csv.
    set newColumnList {}
    set needComma false
    foreach item $columnList {
	if {$needComma} {
	    # Don't put a comma in front.
	    # And don't put a comma at the end.
	    append newColumnList ,
	} else {
	    set needComma true
	}
	append newColumnList $item
    }
    #puts "\n$newColumnList"
    exec echo $newColumnList >> $csvFileName

    set startTime 1
    set stopTime 30
    while {$startTime < $stopTime} {
	set totalPages [ixNet getAttribute $view/page -totalPages]
	if {[regexp -nocase "null" $totalPages]} {
	    puts "\nGetStatViewOnCsv: Getting total pages for $view is not ready. $startTime/$stopTime"
	    after 2000
	} else {
	    break
	}
    }
    
    # Iterrate through each page 
    for {set currPage 1} {$currPage <= $totalPages} {incr currPage} {
	puts "\nGetStatViewOnCsv: Getting statistics on page: $currPage/$totalPages"

	catch {ixNet setAttribute $view/page -currentPage $currPage} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nGetStatViewOnCsv: Failed to get statistic for current page."
	    return 1
	}
	ixNet commit
	
	# Wait for statistics to populate on current page
	set whileLoopStopCounter 0
	while {[ixNet getAttribute $view/page -isReady] != "true"} {
	    if {$whileLoopStopCounter == "5"} {
		puts "\nGetStatViewOnCsv: Could not get stats"
		return 1
	    }
	    if {$whileLoopStopCounter < 5} {
		puts "GetStatViewOnCsv: Not ready yet.  Waiting $whileLoopStopCounter/5 seconds ..."
		after 1000
	    }
	    incr whileLoopStopCounter
	}
	
	set pageList [ixNet getAttribute $view/page -rowValues] ;# first list of all rows in the page
	set totalFlowStatistics [llength $pageList]
	
	# totalPageList == The total amount of flow statistics
	for {set pageListIndex 0} {$pageListIndex <= $totalFlowStatistics} {incr pageListIndex} {
	    set rowList [lindex $pageList $pageListIndex] ;# second list of 1 ingress and x egress rows
	    for {set rowIndex 0} {$rowIndex < [llength $rowList]} {incr rowIndex} {
		# cellList: 1/1/1 1/1/2 TI0-Flow_1 1.1.1.1-1.1.2.1 4000 4000 0 0 0 0 256000 0 0 0 0 0 0 0 0 0 0 0 00:00:00.684 00:00:00.700
		set cellList [lindex $rowList $rowIndex]
		
		regsub -all " " $cellList "," newCellList
		exec echo $newCellList >> $csvFileName
	    }
	}
    }
}

Connect

if {[VerifyPortState]} {
    exit
}

if {[StartAllProtocolsHlt]} {
    exit
}

# User should remove this hard coded value and verify on the DUT 
# for all protocols establishment in a loop.
puts "\nSleeping 30 seconds for protocols to establish ..."
after 30000

for {set iteration 1} {$iteration <= $totalIterations} {incr iteration} {
    foreach eachTrafficSet $params {
	foreach trafficItem $eachTrafficSet {
	    set trafficItemName  [lindex $trafficItem 1]
	    set frameSize        [lindex $trafficItem 3]
	    set ipPrecedence     [lindex $trafficItem 5]
	    set lineRate         [lindex $trafficItem 7]
	    
	    ModifyStreamFrameSizeHlt $trafficItemName $frameSize
	    ModifyStreamLineRateHlt $trafficItemName $lineRate
	    ModifyStreamIpPrecedenceHlt $trafficItemName $ipPrecedence
	}

	if {[StartTrafficHlt]} {
	    exit
	}
	
	GetStatViewOnCsv $csvStatisticFile\_$iteration "Traffic Item Statistics"
    }
}
