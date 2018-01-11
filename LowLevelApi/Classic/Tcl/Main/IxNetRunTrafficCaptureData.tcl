#!/usr/bin/tclsh

# Usage:
#       The configuration must be ready already.
#
#       This script will:
#             Apply traffic
#             Start capture
#             Start traffic
#             Stop traffic
#             Stop capture
#             Display each packets field name and value
#
#       You can use regexp to parse out the field and value.
#       Use $pktStack as your identifier to locate the packet header field
#       that matters to you.
#       All the fields/values are on the same packet number
#       before moving on.
       
      
package req IxTclNetwork

set ixiaChassisIp 10.219.117.101
set ixNetworkTclServer 10.219.117.103
set ixNetworkVersion 8.01
set captureRxPort 1/2

proc GetVport { port } {
    # port = 1/2 format.  Not 1/1/2
    foreach vport [ixNet getList [ixNet getRoot] vport] {
	set connectedTo [ixNet getAttribute $vport -connectedTo]
	set card [lindex [split [lindex [split $connectedTo /] 3] :] end]
	set portNum [lindex [split [lindex [split $connectedTo /] 4] :] end]
	set currentPort $card/$portNum
	
	if {$port == $currentPort} {
	    return $vport
	} 
    }
    puts "Error: $port is connect part of configuration."
    return 0
}

proc ApplyTraffic {} {
    puts "\nApplying configuration to hardware ..."
    set traffic [ixNet getRoot]traffic

    set stopCounter 10
    for {set startCounter 1} {$startCounter <= $stopCounter} {incr startCounter} {
	catch {ixNet exec apply $traffic} errMsg
	if {$errMsg != "::ixNet::OK" && $startCounter < $stopCounter} {
	    puts "ApplyTraffic: Attempting to apply traffic: $startCounter/$stopCounter tries"
	    after 1000
	    continue
	}
	if {$errMsg != "::ixNet::OK" && $startCounter == $stopCounter} {
	    puts "ApplyTraffic: $errMsg"
	    return 0
	}
	if {$errMsg == "::ixNet::OK" && $startCounter < $stopCounter} {
	    puts "Successfully applied traffic to hardware"
	    break
	}
    }
    after 5000
}

proc ConfigPortModeCapture { vPort software hardware } {
    # Values are true or false
    # -softwareEnabled == Control Plane
    # -hardwareEnabled == Data Plane

    ixNet setAttribute $vPort -rxMode capture
    ixNet setAttribute $vPort/capture -softwareEnabled $software
    ixNet setAttribute $vPort/capture -hardwareEnabled $hardware
    ixNet commit
    after 2000
}

catch {ixNet connect $ixNetworkTclServer -version $ixNetworkVersion} errMsg
if {$errMsg != "::ixNet::OK"} {
    puts "Error: Failed to connect to IxNet Tcl Server"
    exit
}

set vPort [GetVport $captureRxPort]
ApplyTraffic

puts "Enabling capture"
ConfigPortModeCapture $vPort false true

puts "\nClose all current captured tabs"
catch {ixNet exec closeAllTabs} errMsg
puts "\nCloseAllTabs: $errMsg"

puts "Starting capture"
catch {ixNet exec startCapture} errMsg
puts "\nstartCapture: $errMsg"
after 10000

puts "Starting traffic"
catch {ixNet exec start [ixNet getRoot]traffic} errMsg
puts "\nStartTraffic: $errMsg"
after 20000

puts "Stopping capture"
ixNet exec stopCapture

puts "Stopping traffic"
ixNet exec stop [ixNet getRoot]traffic
after 5000

puts "Getting all the packets ..."
set currentPkt [lindex [ixNet getList $vPort/capture currentPacket] 0]
puts "Data PacketCounter:[ixNet getAttr $vPort/capture -dataPacketCounter]"

set numPackets 10
for {set i 1} {$i <= $numPackets} {incr i} {
    set status [ixNet exec getPacketFromDataCapture $currentPkt $i]
    puts "\nStatus: $status\n"

    foreach pktStack [ixNet getList $currentPkt stack] {
	# Use pktStack to pin down the fields/values that is relevent to your parsing.
	set pktStackName [lindex [split $pktStack /] end]
	#puts "\nPacket Header: $pktStackName"
	puts "\npktStack: $pktStack\n"

	foreach pktStackField [ixNet getList $pktStack field] {
	    set fieldName [ixNet getAttr $pktStackField -displayName]
	    set fieldValue [ixNet getAttr $pktStackField -fieldValue]

            puts "\nPacket $i  header: $pktStackName"
	    puts "\tField Name: $fieldName : Value: $fieldValue"
	}
    }
}

puts "\nDisabling port mode capture\n"
ConfigPortModeCapture $vPort false false
