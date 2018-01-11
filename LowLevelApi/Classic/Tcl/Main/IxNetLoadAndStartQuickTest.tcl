#!/usr/bin/tclsh

# Description:
#    - This script is written using IxNetwork low level api
#      because HLT currently isn't supporting Quick Test RFC's yet.
#
# Note:
#      The QuickTest configuration must configure the port protocol interface and
#      Traffic Items first and then configure the QuickTest.
#      In the QuickTest Traffic Selection, select "Existing Config" to use the
#      Traffic Item because this allows back-to-back ports with ip gateways
#      pointing to the back-to-back ports.
#
# Note that if you want to run your configuration dynamically without having any hardware 
# dependency, you can save your configuration file without chassis and port assignment.
# Then, you can load the configuration and add the chassis and ports as shown below.
package req Ixia
package req IxTclNetwork

set ixiaChassisIp 10.205.4.172
set ixNetworkTclServer 10.205.1.42
set ixNetworkVersion 7.12

proc SendIxNetCmd { commandLine } {
    catch {eval $commandLine} errMsg
    if {$errMsg != "::ixNet::OK"} {
	puts "Error: $errMsg --> $commandLine"
	exit
    } else {
	puts "Info: $errMsg --> $commandLine"
	return $errMsg
    }
}

proc ApplyTraffic {} {
    puts "\nApplying configuration to hardware ..."
    set traffic [ixNet getRoot]traffic

    set stopCounter 10
    for {set startCounter 1} {$startCounter <= $stopCounter} {incr startCounter} {
	catch {ixNet exec apply $traffic} errMsg
	if {$errMsg != "::ixNet::OK" && $startCounter < $stopCounter} {
	    puts "ApplyTraffic warning: Attempting to apply traffic: $startCounter/$stopCounter tries"
	    after 1000
	    continue
	}
	if {$errMsg != "::ixNet::OK" && $startCounter == $stopCounter} {
	    puts "ApplyTraffic error: $errMsg"
	    exit
	}
	if {$errMsg == "::ixNet::OK" && $startCounter < $stopCounter} {
	    puts "Successfully applied traffic to hardware"
	    break
	}
    }
    after 2000
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
		puts "Info: VerifyPortState: $port is up"
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
	exit
    }
    puts "VerifyPortState: All ports are up"
}

proc GetVportConnectedToPort { vport } {
    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
    set connectedTo [ixNet getAttribute $vport -connectedTo]
    set connectedTo [lrange [split $connectedTo /] 3 4]
    set card [lindex [split [lindex $connectedTo 0] :] end]
    set port [lindex [split [lindex $connectedTo 1] :] end]
    return $card/$port    
}

proc SendArp { vPort } {
    set port [GetVportConnectedToPort $vPort]
    foreach interface [ixNet getList $vPort interface] {

	# Don't send arps on Unconnected (Routed) and GRE interfaces
	set interfaceType [ixNet getAttribute $interface -type]

	if {[regexp "default" $interfaceType]} {
	    set isIntEnabled [ixNet getAttribute $interface -enabled]
	    if {$isIntEnabled == "true" || $isIntEnabled == "True"} {
		puts "SendArp on: $interface"
		
		catch {ixNet exec sendArp $interface} ipv4ErrMsg
		catch {ixNet exec sendNs $interface} ipv6ErrMsg2
		if {$ipv4ErrMsg != "::ixNet::OK" || $ipv6ErrMsg2 != "::ixNet::OK" } {
		    set message "SendArp error on port $port"
		    return [list 0 $message]
		}
	    }
	}
    }
    return [list 1 "Sent arp on $port"]
}

proc SendArpOnAllPorts {} {
    puts \n
    foreach vp [ixNet getList [ixNet getRoot] vport] {
	set arpResult [SendArp $vp]
	if {[lindex $arpResult 0] != 1} {
	    exit
	    #return [list 0 "SendArpOnAllPorts failed"]
	}
    }
    after 2000
    return [list 1 "SendArponAllPorts passed"]
}

proc VerifyArpDiscoveries { {ExitTest doNotExitTest} } {
    # First, get a list of all the expected Gateway IP addresses for this vPort.
    # Get only if the interface is enabled. We don't care about gateways if the
    # interface isn't enable.
    # Then get a list of all the discovered arps.
    # At the end, compare the two list. Any left overs are unresolved arps.
    
    set resolvedArp {}
    set allIpGateways {}

    foreach vP [ixNet getList [ixNet getRoot] vport] {
	# Refresh the arp table on this vport first
	ixNet execute refreshUnresolvedNeighbors $vP

	set currentVportInterfaceList [ixNet getList $vP interface]

	foreach int $currentVportInterfaceList {

	    # Ignore the Unconnected (Routed), and GRE interfaces
	    set interfaceType [ixNet getAttribute $int -type]

	    if {[regexp "default" $interfaceType]} {
		# Only lappend the Gateway if the Interface is enabled.
		set isIntEnabled [ixNet getAttribute $int -enabled]
		if {$isIntEnabled == "true" || $isIntEnabled == "True"} {
		    catch {ixNet getAttribute $int/ipv4 -gateway} ipv4GatewayReturn
		    
		    if {[regexp "null" $ipv4GatewayReturn] != 1} {
			if {[lsearch $allIpGateways $ipv4GatewayReturn] == -1} {
			    lappend allIpGateways $ipv4GatewayReturn
			}
		    }
		    
		    catch {ixNet getList $int ipv6} ipv6GatewayList
		    if {$ipv6GatewayList != ""} {
			foreach ipv6Gateway $ipv6GatewayList {
			    set ipv6 [ixNet getAttribute $ipv6Gateway -gateway]
			    
			    if {$ipv6 != "0:0:0:0:0:0:0:0"} {
				if {[lsearch $allIpGateways $ipv6] == -1} {
				    lappend allIpGateways $ipv6
				}
			    }
			}
		    }
		}
	    }
	}
    }

    puts "Expected ARPs to be resolved:\n"
    foreach arp $allIpGateways {
	puts "\t$arp"
    }
    puts \n

    foreach vP [ixNet getList [ixNet getRoot] vport] {
	# Get all the discovered ARPs for the current vPort
	set vPortInterfaceList [ixNet getList $vP discoveredNeighbor]
	
	if {$vPortInterfaceList != ""} {
	    set currentPort [GetVportConnectedToPort $vP]

	    # vPortInt = ::ixNet::OBJ-/vport:1/discoveredNeighbor:1
	    foreach vPortInt $vPortInterfaceList {
		set currentVp [join [lrange [split $vPortInt /] 0 1] /]
		
		set discoveredIp [ixNet getAttribute $vPortInt -neighborIp]
		set discoveredMac [ixNet getAttribute $vPortInt -neighborMac]
		
		puts "Discovered arp on $currentPort: $discoveredIp : $discoveredMac"
		
		if {$discoveredMac != "" || $discoveredMac != "00:00:00:00:00:00"} {
		    if {[lsearch $allIpGateways $discoveredIp] != -1} {
			lappend resolvedArp $discoveredIp
		    }
		}
	    }
	}
    }

    # Now compare the expected list of arps with what is resolved.
    # Any left overs are unresovled arps.
    foreach resolvedGateway $resolvedArp {
	if {[lsearch $allIpGateways $resolvedGateway] != -1} {
	    set index [lsearch $allIpGateways $resolvedGateway]
	    set allIpGateways [lreplace $allIpGateways $index $index]
	}
    }

    if {$allIpGateways != ""} {
	foreach unresolvedArp $allIpGateways {
	    puts "\tError: Unresolved Arp: $unresolvedArp"
	}
	exit
    } else {
	puts "All arps are resolved"
    }
}

proc GetStatView { statType {getStatsBy trafficItem} } {
    # $statType is one of the following statistics
    # $viewList: 
    # {::ixNet::OBJ-/statistics/view:"Port Statistics"} 
    # {::ixNet::OBJ-/statistics/view:"Tx-Rx Frame Rate Statistics"} 
    # {::ixNet::OBJ-/statistics/view:"Port CPU Statistics"} 
    # {::ixNet::OBJ-/statistics/view:"Global Protocol Statistics"}
    # {::ixNet::OBJ-/statistics/view:"Flow Statistics"} 
    # {::ixNet::OBJ-/statistics/view:"Flow Detective"}  
    # {::ixNet::OBJ-/statistics/view:"Data Plane Port Statistics"} 
    # {::ixNet::OBJ-/statistics/view:"User Defined Statistics"} 
    # {::ixNet::OBJ-/statistics/view:"Traffic Item Statistics"}
    set viewList [ixNet getList [ixNet getRoot]/statistics view]
    #puts "\nviewList: $viewList\n"

    set statViewSelection $statType

    set flowStatsViewIndex [lsearch -regexp $viewList $statViewSelection]
    if {$flowStatsViewIndex == -1} {
	puts "ViewStats: No \"$statViewSelection\" found"
	exit
    }

    # $view: ::ixNet::OBJ-/statistics/view:"Flow Statistics"
    set view [lindex $viewList $flowStatsViewIndex]

    # New way of getting stats. Andy thinks he implemented this in 6.30.
    # If not 6.30, then 7.0
    # ixNet -strip exec getValue $statView "10.205.4.35/Card01/Port01" "Stat Name"
    #   10.205.4.35/Card01/Port01

    ixNet setAttribute $view -enabled true
    ixNet commit

    # $columnList:
    # {Tx Port} {Rx Port} {Traffic Item} {Ethernet II:Destination MAC Address} {Ethernet II:Source MAC Address} {Ethernet II:Ethernet-Type} {Ethernet II:PFC Queue} {IPv4 :Precedence} {IPv4 :Source Address} {IPv4 :Destination Address} {Custom Tracking: Byte Offset 0} {Source/Dest Endpoint Pair} {Source/Dest Value Pair} {Source/Dest Port Pair} {Source Endpoint} {Source Port} {Dest Endpoint} {Frame Size} {Flow Group} {Traffic Group ID} {Tx Frames} {Rx Frames} {Frames Delta} {Loss %} {Tx Frame Rate} {Rx Frame Rate} {Rx Bytes} {Tx Rate (Bps)} {Rx Rate (Bps)} {Tx Rate (bps)} {Rx Rate (bps)} {Tx Rate (Kbps)} {Rx Rate (Kbps)} {Tx Rate (Mbps)} {Rx Rate (Mbps)} {Store-Forward Avg Latency (ns)} {Store-Forward Min Latency (ns)} {Store-Forward Max Latency (ns)} {First TimeStamp} {Last TimeStamp}
    
    set columnList [ixNet getAttribute ${view}/page -columnCaptions]
    #puts "\nColumnList: $columnList\n"

    set startTime 1
    set stopTime 30
    while {$startTime < $stopTime} {
	set totalPages [ixNet getAttribute $view/page -totalPages]
	if {[regexp -nocase "null" $totalPages]} {
	    puts "Getting total pages for $view is not ready. $startTime/$stopTime"
	    after 2000
	} else {
	    break
	}
    }
    
    # Iterrate through each page 
    for {set currPage 1} {$currPage <= $totalPages} {incr currPage} {
	catch {ixNet setAttribute $view/page -currentPage $currPage} errMsg
	if {$errMsg != "::ixNet::OK"} {
	    puts "GetResults: Failed to get statistic for current page."
	    exit
	}
	ixNet commit
	
	# Wait for statistics to populate on current page
	set whileLoopStopCounter 0
	while {[ixNet getAttribute $view/page -isReady] != "true"} {
	    if {$whileLoopStopCounter == "5"} {
		puts "ViewStats: Could not get stats"
		exit
	    }
	    if {$whileLoopStopCounter < 5} {
		puts "\nViewStats: Not ready yet.  Waiting $whileLoopStopCounter/5 seconds ..."
		after 1000
	    }
	    incr whileLoopStopCounter
	}
	
	set pageList [ixNet getAttribute $view/page -rowValues] ;# first list of all rows in the page
	set totalFlowStatistics [llength $pageList]

	# totalPageList == The total amount of flow statistics
	for {set pageListIndex 0} {$pageListIndex <= $totalFlowStatistics} {incr pageListIndex} {
	    set rowList [lindex $pageList $pageListIndex] ;# second list of 1 ingress and x egress rows
	    #puts "\nrowList: $rowList\n"

	    for {set rowIndex 0} {$rowIndex < [llength $rowList]} {incr rowIndex} {
		# cellList: 1/1/1 1/1/2 TI0-Flow_1 1.1.1.1-1.1.2.1 4000 4000 0 0 0 0 256000 0 0 0 0 0 0 0 0 0 0 0 00:00:00.684 00:00:00.700
		set cellList [lindex $rowList $rowIndex] ;# third list of cell values
		
		#puts "\n--- cellList $pageListIndex: $cellList ---\n"

		if {$statViewSelection == "Port Statistics"} {
		    # 10.205.4.35/Card01/Port01
		    set portIndex [lsearch  $columnList "Stat Name"]
		    set port [lindex $cellList $portIndex]
		    set cardNum [string range [lindex [split $port /] 1] 4 end]
		    set portNum [string range [lindex [split $port /] 2] 4 end]

		    foreach column $columnList item $cellList {
			if {[regexp "Link State" $column]} {
			    keylset getStats port.$cardNum/$portNum.linkState $item
			}
			if {[regexp "Misdirected" $column]} {
			    keylset getStats port.$cardNum/$portNum.misdirectedPktCount $item
			}
			if {[regexp "CRC" $column]} {
			    keylset getStats port.$cardNum/$portNum.crcError $item
			}
		    }
		}

		if {$statViewSelection == "Flow Statistics" || $statViewSelection == "Traffic Item Statistics" || $statViewSelection == "Flow Detective"} {
		    # Get the Traffic Item name
		    set trafficItemIndex [lsearch $columnList "Traffic Item"]
		    if {$trafficItemIndex == -1} {
			set trafficItem "UnknownTrafficItem $pageListIndex"
		    } else {
			set trafficItem [lindex $cellList $trafficItemIndex]
		    }
		    
		    # Get the Flow Group
		    set flowGroupIndex [lsearch $columnList "Flow Group"]
		    if {$flowGroupIndex == -1} {
			set flowGroup "$pageListIndex"
		    } else {
			# Flow Group 0008
			set flowGroup [lindex [lindex $cellList $flowGroupIndex] end]
		    }
		    
		    set rxPortIndex [lsearch $columnList "Rx Port"]
		    set rxPort [lindex $cellList $rxPortIndex]
		    
		    foreach column $columnList item $cellList {
			if {[regexp "VLAN:VLAN Priority" $column]} {
			    set column "Vlan Priority"
			}
			
			if {[regexp "VLAN:VLAN-ID" $column]} {
			    set column "Vlan ID"
			}
			
			if {$getStatsBy == "trafficItem"} {
			    if {[regexp "Traffic Item" $column] == 0} {
				keylset getStats trafficItem.[join $trafficItem _].flowGroup.Flow_Group_$flowGroup.[join $column _] $item
			    }
			}
			
			if {$getStatsBy == "port"} {
			    if {[regexp "Rx Port" $column] == 0} {
				keylset getStats rxPort.$rxPort.trafficItem.[join $trafficItem _].[join $column _] $item
			    }
			}
		    }
		}
	    }
	}
    }

    return $getStats
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

# The full path to the config file/configFileName.ixncfg if it is not in the same folder
#set ixnConfigFile  /home/hgee/MyIxiaWork/Temp/QuickTest.ixncfg
set ixnConfigFile  /home/hgee/MyIxiaWork/Temp/QuickTest_7.12.ixncfg

SendIxNetCmd "ixNet connect $ixNetworkTclServer -version $ixNetworkVersion"

# This will clear the old configs
SendIxNetCmd "ixNet rollback"
SendIxNetCmd "ixNet execute newConfig"
set root [ixNet getRoot]

# Load previously saved configuration, make sure to provide the full path to the
# IxNetwork config file, if the file is not in the same folder as this script
SendIxNetCmd "ixNet exec loadConfig [ixNet readFrom $ixnConfigFile]"

ApplyTraffic
VerifyPortState

# ::ixNet::OBJ-/quickTest
set quickTest [ixNet getList $root quickTest]
if {[regexp "::ixNet::OBJ-/quickTest" $quickTest] == 0} {
    puts "Error: quickTest"
    exit
}

# ::ixNet::OBJ-/quickTest/rfc2544throughput:1
set throughputList [ixNet getList $quickTest rfc2544throughput]
if {[regexp "::ixNet::OBJ-/quickTest/rfc2544throughput:\[0-9]+" $throughputList] == 0} {
    puts "Error: throughputList"
    exit
}

set test1 [lindex $throughputList 0]

# ixNet exec apply ::ixNet::OBJ-/quickTest/rfc2544throughput:1
SendIxNetCmd "ixNet exec apply $test1"

SendArpOnAllPorts
VerifyArpDiscoveries

puts "\n==== RFC test: $test1 ====\n"

# ixNet exec start ::ixNet::OBJ-/quickTest/rfc2544throughput:1
SendIxNetCmd "ixNet exec start $test1"

# ixNet getAttribute $test1/results ...
#   Attributes:
#     -duration (readOnly=True, type=kString)
#     -isRunning (readOnly=True, type=kBool)
#     -progress (readOnly=True, type=kString)
#     -result (readOnly=True, type=kString)
#     -resultPath (readOnly=True, type=kString)
#     -startTime (readOnly=True, type=kString)
#     -status (readOnly=True, type=kString)
#
# Right after exec start
#   -duration 
#   -isRunning true
#   -progress -progress Trial 1/1 Iteration 1, Size 64, Rate 10 % 
#   -result 
#   -resultPath C:\Users\hgee\AppData\Local\Ixia\IxNetwork\data\result\DP.Rfc2544Tput\eb2465e5-b0ca-4160-81fc-1fda223554f4\Run0001
#   -startTime 06/06/13 15:05:11
#   -status none
#
# When QT is complete
#    -duration 00:04:54
#    -isRunning false
#    -progress 
#    -result pass
#    -resultPath C:\Users\hgee\AppData\Local\Ixia\IxNetwork\data\result\DP.Rfc2544Tput\eb2465e5-b0ca-4160-81fc-1fda223554f4\Run0001
#    -startTime 06/06/13 15:05:11
#    -status none



# Remove all the previous QuickTest results
foreach quickTestResultFiles {QuickTest_iteration.csv QuickTest_results.csv QuickTest_logFile.txt} {
    catch {exec rm $quickTestResultFiles} errMsg
}

for {set i 0} {$i <= 180} {incr i} {
    if {$i == "180"} {
	puts "Waited for 3 minutes and $test1 can't seem to come up. Exiting."
	exit
    }
    set progress [ixNet getAttribute $test1/results -progress]
    # When we see "Iteration", means the QT has started
    if {[regexp "Iteration" $progress] == 0} {
	puts "Quick Test is not ready yet .... $i/180"
	after 1000
    } else {
	break
    }
}

set resultPath [ixNet getAttribute $test1/results -resultPath]
puts "\nReading results from: $resultPath\n"

set attributeList {-duration -isRunning -progress -result -resultPath -startTime -status}
foreach attrib $attributeList {
    puts "$attrib [ixNet getAttribute $test1/results $attrib]"
}

set isThereQtLogFileFlag 0
# Progress: complete
#           Trial 1/1 Iteration 7, Size 64, Rate 98.594 % Transmitting frames for 10 seconds
#           Trial 1/1 Iteration 7, Size 64, Rate 98.594 % Wait for 8 seconds Wait 35.0770073%complete
#           Trial 1/1 Iteration 7, Size 64, Rate 98.594 %
# 
while {1}  {
    set progress [ixNet getAttribute $test1/results -progress]
    set status [ixNet getAttribute $test1/results -status]
    puts "Progress: $progress ; Status: $status"
    
    #catch {ixNet exec copyFile [ixNet readFrom $resultPath\\iteration.csv -ixNetRelative] [ixNet writeTo QuickTest_iteration.csv -overwrite]} errMsg
    
    #catch {ixNet exec copyFile [ixNet readFrom $resultPath\\results.csv -ixNetRelative] [ixNet writeTo QuickTest_results.csv -overwrite]} errMsg
    
    # Sometimes the QT logFile takes a little longer to get generated.
    # Must wait until the first iteration is done so there is a logFile result
    if {$isThereQtLogFileFlag == 0} {
	set timeStop 180
	for {set timer 0} {$timer <= $timeStop} {incr timer 2} {
	    set progress [ixNet getAttribute $test1/results -progress]
	    set status [ixNet getAttribute $test1/results -status]

	    catch {ixNet exec copyFile [ixNet readFrom $resultPath\\logFile.txt -ixNetRelative] [ixNet writeTo QuickTest_logFile.txt -overwrite]} errMsg
	    
	    catch {exec ls QuickTest_logFile.txt} isThereQtLogFile
	    
	    if {[regexp "No such file" $isThereQtLogFile]} {
		puts "No QuickTest logFile generated yet. Waiting $timer/$timeStop seconds"
		after 2000
	    }
	    if {[regexp "No such file" $isThereQtLogFile] == 0} {
		puts "QuickTest logFile is generated on the IxNet Tcl server"
		set isThereQtLogFileFlag 1
		break
	    }
	    if {$timer == $timeStop && $isThereQtLogFileFlag == 0} {
		puts "IxNet Tcl Server failed to generate the QT logFile on..."
		puts "$resultPath.  Exiting test"
		exit
	    }	    
	}
    }

    catch {ixNet exec copyFile [ixNet readFrom $resultPath\\iteration.csv -ixNetRelative] [ixNet writeTo QuickTest_iteration.csv -overwrite]} iterationCsvFileMsg
    
    catch {ixNet exec copyFile [ixNet readFrom $resultPath\\logFile.txt -ixNetRelative] [ixNet writeTo QuickTest_logFile.txt -overwrite]} errMsg

    # Uncomment this if you want iteration stats.
    # These are the same thing as keylget
    if 0 {
	if {$iterationCsvFileMsg == "::ixNet::OK"} {
	    set iterationStats [exec cat QuickTest_iteration.csv]
	    set fileId [open QuickTest_logFile.txt]
	    set fileContents [read $fileId]
	    close $fileId
	    foreach iterationLine [split $iterationStats \n] {
		# I could get any of the following stats from the iteration file
		# Trial,Framesize,Iteration,Tx Port,Rx Port,Traffic Item,IPv4 :Precedence,Flow Group,Tx Rate (% Line Rate),Rx Throughput (% Line Rate),Rx Throughput (fps),Rx Throughput (Mbps),Tx Count (frames),Rx Count (frames),Frame Loss (frames),Frame Loss (%),Min Latency (ns),Max Latency (n),Avg Latency (ns)
	    }
	}
    }

    set currentLogFile [exec cat QuickTest_logFile.txt]
    #puts \n$currentLogFile\n
    set statView [GetStatView "Port Statistics"]
    puts \n[KeylPrint statView]\n
    set statView [GetStatView "Flow Statistics"]
    puts \n[KeylPrint statView]\n

    set fileId [open QuickTest_logFile.txt]
    set fileContents [read $fileId]
    close $fileId

    foreach line [split $fileContents \n] {
	# BINARY iteration 1, Trial 1, Frame Size 64,  Rate  10 % RFC 2544 Throughput test, Started 4:48:15 PM
	# BINARY iteration 2, Trial 1, Frame Size 64,  Rate  55 % RFC 2544 Throughput test, Started 4:48:45 PM
	# BINARY iteration 3, Trial 1, Frame Size 64,  Rate  77.5 % RFC 2544 Throughput test, Started 4:49:16 PM
	# BINARY iteration 4, Trial 1, Frame Size 64,  Rate  88.75 % RFC 2544 Throughput test, Started 4:49:46 PM
	# BINARY iteration 5, Trial 1, Frame Size 64,  Rate  94.375 % RFC 2544 Throughput test, Started 4:50:16 PM
	# BINARY iteration 6, Trial 1, Frame Size 64,  Rate  97.188 % RFC 2544 Throughput test, Started 4:50:45 PM
	# BINARY iteration 7, Trial 1, Frame Size 64,  Rate  98.594 % RFC 2544 Throughput test, Started 4:51:15 PM
	# BINARY iteration 8, Trial 1, Frame Size 64,  Rate  99.297 % RFC 2544 Throughput test, Started 4:51:45 PM
	# BINARY iteration 9, Trial 1, Frame Size 64,  Rate  100 % RFC 2544 Throughput test, Started 4:52:15 PM
	# 06/06/2013 16:52:44: Ethernet - 001 :  Total frames transmitted: 14880952
	# 06/06/2013 16:52:44: 
	# 06/06/2013 16:52:44: Collecting receive statistics ...
	# 06/06/2013 16:52:44: Ethernet - 002 :  Total frames received: 14880952
	
	# 06/06/2013 16:52:44: Tx Port   Rx Port  Traffic Item  Flow Group  Tx Rate (% Line Rate) Rx Throughput (% Line Rate)  Rx Throughput (fps)  Rx Throughput (Mbps)  Tx Count (frames)  Rx Count (frames)  Frame Loss (frames)  Frame Loss (%)  Min Latency (ns)  Max Latency (ns)  Avg Latency (ns)  
	#06/06/2013 16:52:44: ********************************************************************************************************************************************************************************************************************************************************************************************************************************
	#06/06/2013 16:52:44: Ethernet - 001  Ethernet - 002  Traffic Item 1  Traffic Item 1-EndpointSet-1 - Flow Group 0001  100.000                100.000                      1488095.213          761.905               14880952           14880952           0                    0.000           640               680               652  

	if {[regexp "BINARY *iteration *(\[0-9]+), *Trial *(\[0-9]+), *Frame *Size *(\[0-9]+), *Rate *(\[0-9]+).*Started *(\[0-9]+.*)" $line - iteration trial frameSize rate startTime]} {
	    puts "\nIteration $iteration, Trial $trial, FrameSize $frameSize, Rate $rate%, StartTime $startTime"
	}
	
	if 0 {
	    # 06/06/2013 16:52:44: Ethernet - 001 :  Total frames transmitted: 14880952
	    if {[regexp "\[0-9]+/\[0-9]+/\[0-9]+ *(\[0-9:]+) *(.*) : *Total *frames *transmitted: *(\[0-9]+)" $line - startTime portName totalTx]} {
		puts "\t$startTime $portName TotalTx: $totalTx"
	    }
	    # 06/06/2013 16:52:44: Ethernet - 002 :  Total frames received: 14880952
	    if {[regexp "\[0-9]+/\[0-9]+/\[0-9]+ *(\[0-9:]+) *(.*) : *Total *frames *received: *(\[0-9]+)" $line - startTime portName totalRx]} {
		puts "\t$startTime $portName TotalRx: $totalRx"
	    }
	}
    }

    set progress [ixNet getAttribute $test1/results -progress]
    puts "\n--- Current progress: $progress ---\n"
    if {[regexp "Trial" $progress] == 0 || [regexp "^complete" $progress]} {
	puts "Progress: Quick Test has stopped."
	break
    } else {
	puts "Sleeping 20 seconds ..."
	after 20000
    }
}


ixNet exec copyFile [ixNet readFrom $resultPath\\iteration.csv -ixNetRelative] [ixNet writeTo QuickTest_iteration.csv -overwrite]

ixNet exec copyFile [ixNet readFrom $resultPath\\results.csv -ixNetRelative] [ixNet writeTo QuickTest_results.csv -overwrite]

ixNet exec copyFile [ixNet readFrom $resultPath\\logFile.txt -ixNetRelative] [ixNet writeTo QuickTest_logFile.txt -overwrite]


if 0 {
    set waitForTest [ixNet exec waitForTest $test1]
}


# TODO:  VerifyTrafficStatus

# You need to call this in the loop to get the status when the test is complete 
# or stopped before you run the next test
# ::ixNet::OK-{kArray,{{kString,isRunning},{kString,False},{kString,status},{kString,The execution was aborted.},{kString,result},{kString,fail},{kString,resultPath},{kString,C:\Users\hgee\AppData\Local\Ixia\IxNetwork\data\result\DP.Rfc2544Tput\c5f38e39-17a8-47f2-a3c8-9a82ebf4d274\Run0001}}}

#catch {ixNet exec waitForTest $test1} errMsg
#puts "\nInfo: waitForTest: $errMsg"


# or if you want to run all the rfc2544throughput tests, do as follows

#foreach test $throughputList {

#    ixNet exec apply $test
#     after 5000
#    ixNet exec waitForTest $test1
#}


