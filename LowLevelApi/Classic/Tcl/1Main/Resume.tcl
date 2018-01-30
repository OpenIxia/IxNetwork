#!/usr/bin/tclsh

# Description:
# 
#    Assuming that all ports are configured.
#    

package req Ixia
#package req IxTclNetwork

set ixiaChassisIp 10.219.117.101
set ixNetworkTclServerIp 10.219.117.103

set userName hgee

#source /home/hgee/Dropbox/MyIxiaWork/Insieme_Saravana/pythonScripts/ixpy-0.0.9/ixpy/ixiaHltLib.tcl
#source /home/hgee/Dropbox/MyIxiaWork/IxNet_tclApi.tcl

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
set status [::ixiangpf::connect \
		-ixnetwork_tcl_server $ixNetworkTclServerIp \
		-tcl_server $ixiaChassisIp \
		-username $userName \
		-session_resume_keys 1 \
	       ]

#puts \n[KeylPrint status]
}

proc GetStatView { {getStatsBy trafficItem} } {
    set viewList [ixNet getList [ixNet getRoot]/statistics view]
    puts "\nviewList: $viewList\n"

    set statViewSelection "Flow Statistics"

    set flowStatsViewIndex [lsearch -regexp $viewList $statViewSelection]
    if {$flowStatsViewIndex == -1} {
	puts "\nGetStatView: No \"$statViewSelection\" found"
	return 1
    }

    # $view: ::ixNet::OBJ-/statistics/view:"Flow Statistics"
    set view [lindex $viewList $flowStatsViewIndex]

    ixNet setAttribute $view -enabled true
    ixNet commit

    set columnList [ixNet getAttribute ${view}/page -columnCaptions]
    puts "\n$columnList\n"

    set startTime 1
    set stopTime 30
    while {$startTime < $stopTime} {
	set totalPages [ixNet getAttribute $view/page -totalPages]
	if {[regexp -nocase "null" $totalPages]} {
	    puts "\nGetStatView: Getting total pages for $view is not ready. $startTime/$stopTime"
	    after 2000
	} else {
	    break
	}
    }
    
    # Iterrate through each page 
    set row 0
    for {set currPage 1} {$currPage <= $totalPages} {incr currPage} {
	puts "\nGetStatView: Getting statistics on page: $currPage/$totalPages"

	catch {ixNet setAttribute $view/page -currentPage $currPage} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nGetStatView: Failed to get statistic for current page.\n"
	    return 1
	}
	ixNet commit
	
	# Wait for statistics to populate on current page
	set whileLoopStopCounter 0
	while {[ixNet getAttribute $view/page -isReady] != "true"} {
	    if {$whileLoopStopCounter == "5"} {
		puts "\nGetStatView: Could not get stats"
		return 1
	    }
	    if {$whileLoopStopCounter < 5} {
		puts "\nGetStatView: Not ready yet.  Waiting $whileLoopStopCounter/5 seconds ..."
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
		# Increment the row number
		incr row

		# cellList: 1/1/1 1/1/2 TI0-Flow_1 1.1.1.1-1.1.2.1 4000 4000 0 0 0 0 256000 0 0 0 0 0 0 0 0 0 0 0 00:00:00.684 00:00:00.700
		set cellList [lindex $rowList $rowIndex] ;# third list of cell values
		
		puts "\n--- cellList $pageListIndex: $cellList ---\n"

		# Get the Traffic Item name
		set trafficItemIndex [lsearch $columnList "Traffic Item"]
		if {$trafficItemIndex == -1} {
		    set trafficItem "UnknownTrafficItem $pageListIndex"
		} else {
		    set trafficItem [lindex $cellList $trafficItemIndex]
		}

		set rxPortIndex [lsearch $columnList "Rx Port"]
		set rxPort [lindex $cellList $rxPortIndex]
		
		foreach column $columnList item $cellList {
		    if {[regexp "VLAN:VLAN Priority" $column]} {
			set column "Vlan_Priority"
		    }
		    if {[regexp "VLAN:VLAN-ID.*1" $column]} {
			set column "Inner_Vlan_ID"
		    }
		    if {[regexp "VLAN:VLAN-ID" $column]} {
			# This is also Outer VlanID
			set column "Vlan_ID"
		    }
		    if {[regexp "IPv4 :Source Address" $column]} {
			set column "IPv4_Src_Address"
		    }
		    if {[regexp "IPv4 :Destination Address" $column]} {
			set column "IPv4_Dst_Address"
		    }
		    if {[regexp "Ethernet II:Destination MAC Address" $column]} {
			set column "Dest_Mac_Address"
		    }
		    if {[regexp "Ethernet II:Source MAC Address" $column]} {
			set column "Src_Mac_Address"
		    }
		    if {$getStatsBy == "trafficItem"} {
			if {[regexp "Traffic Item" $column] == 0} {
			    keylset getStats trafficItem.[join $trafficItem _].flow.$row.[join $column _] $item
			}
		    }
		    if {$getStatsBy == "port"} {
			if {[regexp "Rx Port" $column] == 0} {
			    keylset getStats rxPort.$rxPort.trafficItem.[join $trafficItem _].[join $column _] $item
			}
		    }
		    keylset getStats totalFlows $row
		}
	    }
	}
    }

    return $getStats
}

ixNet connect $ixNetworkTclServerIp -version 8.0

GetStatView "Flow View"
