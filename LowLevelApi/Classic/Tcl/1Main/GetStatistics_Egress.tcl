#!/opt/ActiveTcl-8.5/bin/tclsh

# Need to use Ixia package because we need Tclx
package req Ixia

# Script written by:  Hubert Gee
#
# 10/26/2013
#
# Description
#  
#    This script assumes that traffic is running already.
#    This script will get egressing stats based on what the user wants
#    to track.  For example. The following assumes that you want to 
#    track two packet fields: udp and vlan.
#
#    You can get the exact packet field wording by using the following API: 
#
#          [ixNet getList ${view} availableTrafficItemFilter]
#             Returns:
#             ::ixNet::OBJ-/statistics/view:"EgressView"/availableTrafficItemFilter:"vlan"
#             ::ixNet::OBJ-/statistics/view:"EgressView"/availableTrafficItemFilter:"udp
#
#        TODO: Eventually, I will make this script get these entries automatically.
#        For now, This is my way to customize a script for users by having them provide
#        the informations.  Users can use other techniques as well, but this is something
#        that is working.
#        This serves as a template too ...

#        array set egressTrackings {
#            udp {
#    	         {port "$ixChassisIp/Card1/Port4"}
#	         {field "UDP:UDP-Source-Port"}
#	         {offset {Custom:\ (16\ bits\ at\ offset\ 272)}}
#            }
#            vlan {
#	          {port "$ixChassisIp/Card1/Port2"}
#	          {field "VLAN:VLAN-ID"}
# 	          {offset {Custom:\ (12\ bits\ at\ offset\ 116)}}
#            }
#        }
#
#    port    = The Rx port to analyze for egress tracking.
#
#    field   = The packet field to track. When you select this in Flow Tracking,
#              the Traffic Item in the GUI will display the exact name for you 
#              to use.  You can also get this by scriptgen.
#
#    offset  = This is the offset on where to track. To understand how to get 
#              the offset:
#              - Go to IxNet Packet Editor, go to the exact packet field 
#              you want to track and just highlight it.  Then look at the bottom,
#              above the "Finish" button, and get the offset number and bytes.
#              The number of bits to used must cover value that you expect.
#
#              For example: 4096 2048 1024 256 128 64 32 16 8 4 2 1 = 12 bits
#                           For tracking vlanID, we don't know what the DUT will
#                           forward out. So we must use 12 bits to cover the 
#                           entire vlan range of 4096.
#
#              ALSO: You must go to Flow Tracking and enable the packet field. 
#                    Otherwise, it won't show up on the Traffic Item line.
#
#
#  Please go all the way to the bottom to see how the stats will show.
#
#  This script also uses an API that I created for this script called 
#  GetAssignedPort to convert the interface name to the physical port 
#  number for readability.
#
#  IMPORTANT TO KNOW for egress tracking
#
#  - The rxPort can ONLY track ONE egress tracking. You will need multiple
#    rxPorts to simultaneously track multiple egress trackings.
#
#  - Because the rxPort is extremely intense processing the stats before they are shown.
# 
#  - Therefore, egress stats take at least one minute to show up.
#
#

set ixNetworkTclServer 10.205.1.42
set ixChassisIp 10.205.4.172
set ixNetVersion 7.10

# 0 = Do not remove the created statView tab after the script finishes.
# 1 = Remove the created statView tab after the script finishes.
set removeTclViewStats 1 

# Get these API values from scriptgen

# DO NOT INCLUDE WHAT IS NOT BEING TRACKED
# If UDP is not being tracked, don't included.
# ALSO!  The udp and vlan is the actual Traffic Item name that
#        one of the egress API looks for.

array set egressTrackings {
    udp {
	{port "$ixChassisIp/Card1/Port4"}
	{field "UDP:UDP-Source-Port"}
	{offset {Custom:\ (16\ bits\ at\ offset\ 272)}}
    }
    vlan {
	{port "$ixChassisIp/Card1/Port2"}
	{field "VLAN:VLAN-ID"}
	{offset {Custom:\ (12\ bits\ at\ offset\ 116)}}
    }
}

proc GetTime {} {
    return [clock format [clock seconds] -format "%H:%M:%S"]
}

proc GetAssignedPort { name } {
    foreach vport [ixNet getList [ixNet getRoot] vport] {
	set currentName [ixNet getAttribute $vport -name]
	if {$currentName == $name} {
	    set assignedPort [ixNet getAttribute $vport -assignedTo]
	    set assignedPort [split $assignedPort :]
	    set card [lindex $assignedPort 1]
	    set port [lindex $assignedPort 2]
	    return $card/$port
	}
    }
    return unknownPort
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


proc GetEgressStats {} {
    # Remove all existing TCL Views first.
    ixNet execute removeAllTclViews

    foreach {packetField values} [array get ::egressTrackings *] {
	foreach fieldValue $values {
	    if {[lindex $fieldValue 0] == "port"} {
		# 10.205.4.155/Card1/Port2
		set port [lindex $fieldValue 1]
		regexp "\\\$(.*)(/.*/.*)" $port - ixiaChassisIp portNumber
		set port \"[set ::$ixiaChassisIp]$portNumber\"
	    }
	    if {[lindex $fieldValue 0] == "field"} {
		# VLAN:VLAN-ID
		set field [lindex $fieldValue 1]
	    }
	    if {[lindex $fieldValue 0] == "offset"} {
		# Custom:\ (12\ bits\ at\ offset\ 116)
		set offset [lindex $fieldValue 1]
	    }
	}

	set view [ixNet add [ixNet getRoot]statistics "view"]

	#ixNet setMultiAttribute $view -caption "EgressView" -treeViewNodeName "Egress\\Custom\ Views" -type layer23TrafficFlow -visible true
	ixNet setMultiAttribute $view -caption "$packetField\View" -type layer23TrafficFlow -visible true
	ixNet commit
	set view [lindex [ixNet remapIds $view] 0]
	
	set trafficFlowFilter [ixNet add $view "layer23TrafficFlowFilter"]
	ixNet setMultiAttribute $trafficFlowFilter -egressLatencyBinDisplayOption showEgressRows
	ixNet commit
	set trafficFlowFilter [lindex [ixNet remapIds $trafficFlowFilter] 0]
	
	# ::ixNet::OBJ-/statistics/view:"EgressView"/layer23TrafficFlowFilter/enumerationFilter:L81
	set enumerationFilter [ixNet add $trafficFlowFilter "enumerationFilter"]
	ixNet setMultiAttribute $enumerationFilter -sortDirection ascending
	ixNet commit
	set enumerationFilter [lindex [ixNet remapIds $enumerationFilter] 0]
	
	# ::ixNet::OBJ-/statistics/view:"EgressView"/layer23TrafficFlowFilter/enumerationFilter:L81
	set enumerationFilter2 [ixNet add $trafficFlowFilter "enumerationFilter"]
	ixNet setMultiAttribute $enumerationFilter2 -sortDirection ascending
	ixNet commit
	set enumerationFilter2 [lindex [ixNet remapIds $enumerationFilter2] 0]

	ixNet setMultiAttribute $trafficFlowFilter -portFilterIds [list $view/availablePortFilter:"$port"]

	ixNet setMultiAttribute $enumerationFilter2 -trackingFilterId $view/availableTrackingFilter:"$offset"

	ixNet setMultiAttribute $enumerationFilter -trackingFilterId $view/availableTrackingFilter:"$field"
	catch {ixNet commit} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "\nError: $field must be selected in Flow Tracking for tracking:\n$errMsg\n"
	    exit
	}
	
	ixNet setMultiAttribute $trafficFlowFilter -trafficItemFilterIds [list $view/availableTrafficItemFilter:"$packetField"]

	puts "--- packetField: $packetField ; field: $field ---"

	# Enable all the statistic counters
	foreach {statistic} [ixNet getList $view statistic] {
	    ixNet setAttribute $statistic -enabled true
	}
	ixNet commit 

	puts "\nCreated and enabling: $view"
	puts "\nRetrieving egress stats is intense processing."
	puts "Please wait ~1.5 minutes ..."

	catch {ixNet setMultiAttribute $view -enabled true} errMsg
	puts "\n---- $errMsg ---\n"
	catch {ixNet commit} errMsg
	puts "\n---- $errMsg ---\n"

puts "\n--- view: $view ----\n"

	# These are all the stat counters on the page
	set columnList [ixNet getAttribute ${view}/page -columnCaptions]
	puts "\n$columnList"

	set totalPages [ixNet getAttribute $view/page -totalPages]
	
	for {set currPage 1} {$currPage <= $totalPages} {incr currPage} {
	    ixNet setAttribute $view/page -currentPage $currPage
	    ixNet commit

	    set rowValues [ixNet getAttribute ${view}/page -rowValues]
	    set totalRowsOfStatistics [llength $rowValues]
	    
	    puts "\n---- rowValues: $rowValues ----\n"
	    
	    for {set pageListIndex 0} {$pageListIndex <= $totalRowsOfStatistics} {incr pageListIndex} {
		set rowList [lindex $rowValues $pageListIndex]

		for {set rowIndex 0} {$rowIndex < [llength $rowList]} {incr rowIndex} {
		    #cellList: {Ethernet - 002} 102 {Custom: (12 bits at offset 116)} 42602 42602 0 0 10 10 9600 9600 4260200 1000 1000 8000 8000 8 8 0.008 0.008 0 0 0 00:00:00.614 01:11:00.700

		    #cellList: {} {} 102 {} 42602 {} {} {} 10 {} 9600 4260200 {} 1000 {} 8000 {} 8 {} 0.008 0 0 0 00:00:00.614 01:11:00.700

		    #puts "\ncellList: $cellList"

		    #columnCaptions: {Rx Port} UDP:UDP-Source-Port {Egress Tracking} {Tx Frames} {Rx Frames} {Frames Delta} {Loss %} {Tx Frame Rate} {Rx Frame Rate} {Tx L1 Rate (bps)} {Rx L1 Rate (bps)} {Rx Bytes} {Tx Rate (Bps)} {Rx Rate (Bps)} {Tx Rate (bps)} {Rx Rate (bps)} {Tx Rate (Kbps)} {Rx Rate (Kbps)} {Tx Rate (Mbps)} {Rx Rate (Mbps)} {Store-Forward Avg Latency (ns)} {Store-Forward Min Latency (ns)} {Store-Forward Max Latency (ns)} {First TimeStamp} {Last TimeStamp}

		    set cellLineFlag 0
		    set getOneTimeOnlyFlag 0
		    foreach row $rowList {
			puts "\n---- foreach row: $row ----\n"
			foreach column $columnList item $row {
			    # Using cellLineFlag to control only getting stats on the 
			    # first line. Ignore the second line.
			    # Already parsed out the egress tracking.
			    if {$cellLineFlag == 0} {
				if {$getOneTimeOnlyFlag == 0} {
				    set ingressTracking [lindex $row 1]
				    #puts "\nIngressTracking: $ingressTracking"
				    
				    if {$column == "Rx Port"} {
					set port [GetAssignedPort $item]
					#puts "\nport: $port"
				    }
				    set getOneTimeOnlyFlag 1
				}

				set column [join $column _]
				set item   [join $item _]

				#puts "--- $column : $item ----"
				keylset egressStats rxPort.$port.$packetField.ingress.$ingressTracking.$column $item
			    }			
			}

			# We just want the egressing value. That is it.
			if {$cellLineFlag == 1} {
			    set egressTrackingIndex [lsearch $columnList "Egress Tracking"]
			    set egressTracking      [lindex $row $egressTrackingIndex]
			    #puts "\negressTrackingIndex: $egressTrackingIndex ; egressTracking: $egressTracking"
			    keylset egressStats rxPort.$port.$packetField.ingress.$ingressTracking.Egressing-As $egressTracking
			}
			set cellLineFlag 1
		    }
		}
	    }
	}
	
	if {[info exists ::removeTclViewStats] == 1 && $::removeTclViewStats == 1} {
	    ixNet remove $view
	    ixNet commit
	}
    }

    return $egressStats
}


ixNet connect $ixNetworkTclServer -version $ixNetVersion

set startTime [GetTime]
set egressStats [GetEgressStats]
set stopTime [GetTime]
puts [KeylPrint egressStats]

puts "\nStartTime: $startTime : StopTime: $stopTime\n"

# This is an example of a statistic snapshot.
# NOTE: Egress tracking statistics takes like a minute due to 
#       intense processing.
#
# keylist egressStats rxPort.1/2.vlan.ingress.102.$statCounters $statistics
#
#    For egress tracking, we only care about the Rx port only.
#    vlan = the packet field that you want to track.
#    ingress.102 = getting the ingressing value.
#    Egressing-As = The egressing value.

if 0 {
rxPort:
 1/2:
  vlan:
   ingress:
    102:
     Rx_Port: Ethernet_-_002
     VLAN:VLAN-ID: 102
     Egress_Tracking: Custom:_(12_bits_at_offset_116)
     Tx_Frames: 1002
     Rx_Frames: 1002
     Frames_Delta: 0
     Loss_%: 0
     Tx_Frame_Rate: 10
     Rx_Frame_Rate: 10
     Tx_L1_Rate_(bps): 9600
     Rx_L1_Rate_(bps): 9600
     Rx_Bytes: 100200
     Tx_Rate_(Bps): 1000
     Rx_Rate_(Bps): 1000
     Tx_Rate_(bps): 8000
     Rx_Rate_(bps): 8000
     Tx_Rate_(Kbps): 8
     Rx_Rate_(Kbps): 8
     Tx_Rate_(Mbps): 0.008
     Rx_Rate_(Mbps): 0.008
     Store-Forward_Avg_Latency_(ns): 0
     Store-Forward_Min_Latency_(ns): 0
     Store-Forward_Max_Latency_(ns): 0
     First_TimeStamp: 00:00:00.617
     Last_TimeStamp: 00:01:40.715
     Egressing-As: 102
}