#!/opt/ActiveTcl-8.5/bin/tclsh

# Written by: Hubert Gee
# 
# For this script, it was tested with Guang_mmrp3.ixncfg config file
#
# NOTE!  This script assumes that there is a duplicate RAW 
#        Traffic Item with flow groups copied from Traffic Item #1.
#        Therefore, this script will be modifying the second
#        RAW Traffic Item of flow groups.
#
#        The user must create an accurate amount of flow groups.
#        For example:
#           If user created Traffic Item #1 with 50 Flow Groups,
#           and user set the follwoing variable values with:
#               bMacRepeat 10
#               bMacCount 5
#               isidCount 3
#           This means the script will create a total of 150 flow groups.
#           For each of the original flow group, the script will create
#           addtional [expr $isidCount - 1]. In this example, 2 more created.
#           bMacRepeat is the pseudo wire, with the same bMac-src-mac address.
#           bMacCount is total PE's.
#           isidCount is the total amount of isid for each pseudo wire.
#

package req IxTclNetwork

set ixNetworkTclServer localhost
set ixNetworkVersion 7.12

ixNet connect $ixNetworkTclServer -version $ixNetworkVersion

# User's input
set isidStartingValue "000001"
set isidCount 3 
set isidStep 1
set isidInstantSkip 1 ;# Ex: 01 02 03 <skip 1> 05 06 07 <skip 1> 09 0a 0b

#set startingPayloadPrefix "0002062001011e83"
set startingPayloadPrefix "0002060001011e83"
set endingPayloadPrefix "2400000000"

set bMacStartingValue "00:aa:bb:cc:dd:00"
set bMacRepeat 10 ;# Corresponds to the number of PW per PE
set bMacStep "00:00:00:00:00:01" ;# Incrementing by one, but this isn't working.
set bMacCount 5 ;# Corresponds to the number of emulated PEs

set srcMacLastByteStartingValue [lindex [split $bMacStartingValue :] end]
set srcMacFirstFiveBytes        [join [lrange [split $bMacStartingValue :] 0 4] :]

set bMacDstMac 01:80:c2:00:00:20

set flag 0
set srcMacList {}
# We have 10 pseudo wires for each bmac.
# Each pseudo wire in a bMac will have the same src mac addr
# But each packet will have a unique isid payload pattern
for {set peCount 1} {$peCount <= $bMacCount} {incr peCount} {
    if {$flag == 0} {
	# Convert hex to decimal
	set startingMacValue [expr 0x$srcMacLastByteStartingValue]
	set flag 1
    } 
    if {$flag == 1} {
	set startingMacValue [incr startingMacValue]
    }
    
    for {set repeat 1} {$repeat <= [expr $bMacRepeat * $isidCount]} {incr repeat} {
	lappend srcMacList $srcMacFirstFiveBytes:[format "%02x" $startingMacValue]
    }
}

# Build the isid payload pattern

set isidList {}
set convertIsidHexToDecimal [expr 0x$isidStartingValue]
for {set times 1} {$times <= [expr $bMacRepeat * $bMacCount]} {incr times} {
    for {set isid 1} {$isid <= $isidCount} {incr isid} {
	lappend isidList $startingPayloadPrefix[format "%06x" $convertIsidHexToDecimal]$endingPayloadPrefix
	incr convertIsidHexToDecimal
    }
    incr convertIsidHexToDecimal $isidInstantSkip
}

puts \n
set num 0
foreach mac $srcMacList {
    puts "[incr num]: $mac"
}

puts \n
set numb 0
foreach isid $isidList {
    puts "[incr numb]: $isid"
}

set trafficItem [lindex [ixNet getList [ixNet getRoot]traffic trafficItem] 1]

# Get total flow groups for the Raw Traffic Item
set totalFlowGroups 0
foreach highLevelStream [ixNet getList $trafficItem highLevelStream] {
    incr totalFlowGroups
}

if {$totalFlowGroups != [expr $bMacCount * $bMacRepeat]} {
    puts "\nUser inputs: bMacCount = $bMacCount : bMacRepeat = $bMacRepeat"
    puts "Total expected Flow Groups on Traffic Item: [expr $bMacCount * $bMacRepeat]"
    puts "ERROR:  Traffic Item name [ixNet getAttribute $trafficItem -name]"
    puts "        has total flow groups: $totalFlowGroups"
    
    puts "\nExiting test!\n\n\n"
    return
    exit
}


#::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ethernet-1"
#::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"mpls-2"
#::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"mpls-3"
#::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"ethernet-4"
#::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"fcs-5"
#::ixNet::OBJ-/traffic/trafficItem:1/configElement:1/stack:"fcs-6"

# Get the current Traffic Item's EndpointSet srcPort and dstPorts
# in order to create new endpointSet
set currentEndpointSet [lindex [ixNet getList $trafficItem endpointSet] 0]
set srcVport [ixNet getAttribute $currentEndpointSet -sources]
set dstVport [ixNet getAttribute $currentEndpointSet -destinations]

set allHighLevelStreams [ixNet getList $trafficItem highLevelStream]

set mplsValueList1 {}
set mplsValueList2 {}

# Going to get the MPLS labels and other packet info and build a list.
# Then delete the flow group because there seems to be a bug that 
# the payload cannot get modified. We are going to recreate all 
# the flow groups after removing the existing ones.
foreach highLevelStream $allHighLevelStreams {
    puts "\nFlow Group: $highLevelStream"

    #regexp "highLevelStream:(\[0-9]+)" $highLevelStream - flowGroupNum

    set ethernetSrc    [ixNet getAttribute $highLevelStream/stack:\"ethernet-1\"/field:\"ethernet.header.sourceAddress-2\" -singleValue]
    set ethernetDst    [ixNet getAttribute $highLevelStream/stack:\"ethernet-1\"/field:\"ethernet.header.destinationAddress-1\" -singleValue]
    #set mpls1 [ixNet getAttribute $highLevelStream/stack:\"mpls-2\"/field:\"mpls.label.value-1\" -singleValue]
    set mpls2 [ixNet getAttribute $highLevelStream/stack:\"mpls-3\"/field:\"mpls.label.value-1\" -singleValue]

    #foreach lable $mpls1 {
    #	append mplsValueList1 "\"$lable\" "
    #}

    foreach lable2 $mpls2 {
	append mplsValueList "\"$lable2\" "
    }
    
    set frameSize     [ixNet getAttribute $highLevelStream/frameSize -fixedSize]
    set frameRateType [ixNet getAttribute $highLevelStream/frameRate -type]
    set frameRate     [ixNet getAttribute $highLevelStream/frameRate -rate]

    set currentHlEndpointSetId [ixNet getAttribute $highLevelStream -endpointSetId]
    puts "$highLevelStream endpointSeId: $currentHlEndpointSetId"

    puts "\nRemoving current flow group: $trafficItem/endpointSetId:$currentHlEndpointSetId  ..."
    catch {ixNet remove $trafficItem/endpointSet:$currentHlEndpointSetId} errMsg
    puts "\tRemove flow group: $errMsg"
}
catch {ixNet commit} errMsg
puts "\tixNet commit removeflow group: $errMsg"

puts "\nmplsValueList: $mplsValueList"

# Go through each highLevelStream to configure bMac and isid
set payloadIndexNumber 0 ;# This is for getting the next srcMac and next isid
set mplsIndexCounter 0
for {set totalFlowGroups 1} {$totalFlowGroups <= [llength $allHighLevelStreams]} {incr totalFlowGroups} {
    for {set newFlowGroup 1} {$newFlowGroup <= $isidCount} {incr newFlowGroup} {
	set tiEndpointSetObj [ixNet add $trafficItem endpointSet]
	ixNet setMultiAttrs $tiEndpointSetObj \
	    -sources $srcVport \
	    -destinations $dstVport
	ixNet commit
	set tiEndpointSetObj [lindex [ixNet remapIds $tiEndpointSetObj] 0]
	puts "\nCreated new Flow Group: $newFlowGroup/$isidCount"
	
	# Get the endpointSet-Id
	regexp "endpointSet:(\[0-9]+)" $tiEndpointSetObj - newEndpointSetId
	
	# Must search all created flow groups to see which flow group has the
	# endpointSetId that is just created.
	foreach newHighLevelStream [ixNet getList $trafficItem highLevelStream] {
	    if {[ixNet getAttribute $newHighLevelStream -endpointSetId] == $newEndpointSetId} {
		
		catch {ixNet setAttribute $newHighLevelStream/stack:\"ethernet-1\"/field:\"ethernet.header.sourceAddress-2\" \
			   -singleValue $ethernetSrc \
		       } errMsg
		puts "\tConfiguring ethernetSrcAddr: $errMsg"
		
		catch {ixNet setAttribute $newHighLevelStream/stack:\"ethernet-1\"/field:\"ethernet.header.destinationAddress-1\" \
			   -singleValue $ethernetDst \
		       } errMsg
		puts "\tConfiguring ethernetDstAddr: $errMsg"
		
		set mplsIndex [lsearch -regexp [ixNet getList [ixNet getRoot]/traffic protocolTemplate] mpls]
		set mplsStack [lindex [ixNet getList [ixNet getRoot]/traffic protocolTemplate] $mplsIndex]
		
		puts "\tAdding MPLS-1 stack ..."
		set addToStackLevel [lindex [ixNet getList $newHighLevelStream stack] 0]
		ixNet exec append $addToStackLevel $mplsStack

		catch {ixNet setMultiAttribute $newHighLevelStream/stack:\"mpls-2\"/field:\"mpls.label.value-1\" \
			   -valueType singleValue \
			   -singleValue \"[lindex $mplsValueList $mplsIndexCounter]\"} errMsg
		puts "\t\tsetAttrib mpls-1 \"[lindex $mplsValueList`< $mplsIndexCounter]\": $errMsg"
		
		set ethernetNoFcsIndex [lsearch -regexp [ixNet getList [ixNet getRoot]/traffic protocolTemplate] ethernetNoFCS]
		set ethernetNoFcsStack [lindex [ixNet getList [ixNet getRoot]/traffic protocolTemplate] $ethernetNoFcsIndex]
		
		puts "\tAdding EthernetNoFCS stack ..."
		set addToStackLevel [lindex [ixNet getList $newHighLevelStream stack] 1]
		ixNet exec append $addToStackLevel $ethernetNoFcsStack
		
		catch {ixNet setMultiAttribute $newHighLevelStream/stack:\"ethernetNoFCS-3\"/field:\"ethernetNoFCS.header.destinationAddress-1\" \
			   -valueType valueList \
			   -valueList $bMacDstMac} errMsg
		puts "\t\tsetAttrib bMacDestAddr: $errMsg"
		
		catch {ixNet setMultiAttribute $newHighLevelStream/stack:\"ethernetNoFCS-3\"/field:\"ethernetNoFCS.header.sourceAddress-2\" \
			   -valueType valueList \
			   -valueList [lindex $srcMacList $payloadIndexNumber]} errMsg
		puts "\t\tsetAttrib bMacSrcAddr: $errMsg"
		
		puts "\tConfiguring Ethernet Type 0x88f6 on new flow group"
		catch {ixNet setMultiAttribute $newHighLevelStream/stack:\"ethernetNoFCS-3\"/field:\"ethernetNoFCS.header.etherType-3\" \
			   -auto false \
			   -singleValue 88f6 \
			   -seed 1 \
			   -optionalEnabled true \
			   -valueList [list 0xFFFF] \
			   -stepValue 0xFFFF \
			   -fixedBits 0xFFFF \
			   -fieldValue 88f6 \
			   -randomMask 0xFFFF \
			   -startValue 0xFFFF \
		       } errMsg
		puts "\t\tsetMultiAttr 88f6: $errMsg"
		
		puts "\tConfiguring custom payload: $newHighLevelStream\n\t[lindex $isidList $payloadIndexNumber] ..."
		catch {ixNet setMultiAttribute $newHighLevelStream/framePayload \
			   -customPattern [list [lindex $isidList $payloadIndexNumber]] \
			   -type custom \
			   -customRepeat false} errMsg
		puts "\t\tsetMultiAttr: $errMsg"
		
		catch {ixNet setMultiAttribute $newHighLevelStream/frameSize \
			   -fixedSize $frameSize} errMsg
		puts "\t\tsetMultiAttr frameSize: $errMsg"		
		
		catch {ixNet setMultiAttribute $newHighLevelStream/frameRate \
			   -type $frameRateType \
			   -rate $frameRate} errMsg
		puts "\t\tsetMultiAttr frameRate: $errMsg"		
		
		catch {ixNet commit} errMsg
		puts "\t\tPushing config to hardware: $errMsg"
		
		incr payloadIndexNumber
	    }
	}
    }
    incr mplsIndexCounter
}

puts "\n----  Done -----\n\n"
