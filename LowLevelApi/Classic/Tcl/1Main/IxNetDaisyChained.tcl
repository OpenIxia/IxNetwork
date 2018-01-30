#!/opt/ActiveTcl-8.5/bin/tclsh

# This script creates a new traffic item and 
# creates the total number of endpoints based on the 
# total number of the array entries on "endpoint".
#
# For each endpoint, create a mpls and ipv4 header
# mpls value = 0
# source IP is the primary link.
#     Primary link means for each source IP address, it
#     will send to every destination hosts. Then it 
#     goes to the next src IP and send to every destination
#     host and round robins until it is done with all the 
#     src ip addresses.
#
# About daisy chaining Ixia chassis's:
# 
# There's nothing that needs to be done. IxNetwork and IxExplorer 
# will recognize which are the Master and Slave (and actually, they don't care).
# Turn on the Master chassis first, and bring up IxServer. Once IxServer says it's 
# master, you can turn up the Slave chassis and bring up IxServer on that chassis. 
# Make sure IxServer on that chassis recognizes it's a slave.

# Add the chassis and  ports to the IxNetwork config (slave or master doesn't matter). 
# In IxExplorer, just connect to both the chassis. Again master or slave doesn't matter.


package req IxTclNetwork

set ixNetworkTclServerIp 10.205.1.42
set ixNetworkVersion 7.3
set ixChassisIp1 10.205.4.172

set portList(1.1.1.2) "1/1 1/2 1/3 1/4 1/5 1/6 1/7 1/8 1/9 1/10 1/11 1/12 1/13 1/14 1/15 1/16 2/1 2/2 2/3 2/4 2/5 2/6 2/7 2/8 2/9 2/10 2/11 2/12 2/13 2/14 2/15 2/16 3/1 3/2 3/3 3/4 3/5 3/6 3/7 3/8 3/9 3/10 3/11 3/12 3/13 3/14 3/15 3/16 4/1 4/2 4/3 4/4 4/5 4/6 4/7 4/8 4/9 4/10 4/11 4/12 4/13 4/14 4/15 4/16 5/1 5/2 5/3 5/4 5/5 5/6 5/7 5/8 5/9 5/10 5/11 5/12 5/13 5/14 5/15 5/16 6/1 6/2 6/3 6/4 6/5 6/6 6/7 6/8 6/9 6/10 6/11 6/12 6/13 6/14 6/15 6/16 7/1 7/2 7/3 7/4 7/5 7/6 7/7 7/8 7/9 7/10 7/11 7/12 7/13 7/14 7/15 7/16 8/1 8/2 8/3 8/4 8/5 8/6 8/7 8/8 8/9 8/10 8/11 8/12 8/13 8/14 8/15 8/16 9/1 9/2 9/3 9/4 9/5 9/6 9/7 9/8 9/9 9/10 9/11 9/12 9/13 9/14 9/15 9/16 10/1 10/2 10/3 10/4 10/5 10/6 10/7 10/8 10/9 10/10 10/11 10/12 10/13 10/14 10/15 10/16 11/1 11/2 11/3 11/4 11/5 11/6 11/7 11/8 11/9 11/10 11/11 11/12 11/13 11/14 11/15 11/16 12/1 12/2 12/3 12/4 12/5 12/6 12/7 12/8 12/9 12/10 12/11 12/12 12/13 12/14 12/15 12/16"

set portList(1.1.1.3) "3/1 3/2 3/3 3/4 3/5 3/6 3/7 3/8 3/9 3/10 3/11 3/12 3/13 3/14 3/15 3/16 3/17 3/18 3/19 3/20 3/21 3/22 3/23 3/24 3/25 3/26 3/27 3/28 3/29 3/30 3/31 3/32 4/1 4/2 4/3 4/4 4/5 4/6 4/7 4/8 4/9 4/10 4/11 4/12 4/13 4/14 4/15 4/16 4/17 4/18 4/19 4/20 4/21 4/22 4/23 4/24 4/25 4/26 4/27 4/28 4/29 4/30 4/31 4/32"

set dstEndpoint1 "$ixChassisIp1:1/2 $ixChassisIp1:1/3"
set dstEndpoint2 "$ixChassisIp1:1/1 $ixChassisIp1:1/3"
set dstEndpoint3 "$ixChassisIp1:1/1 $ixChassisIp1:1/2"

#             StartingSrcIp  TotalSrcIpCount  StartingDstIp  TotalDstIpCount
set endpoint(1.1.1.2:1/2,[list $dstEndpoint1]) "1.1.1.1 101 200.1.1.1 10"

catch {ixNet connect $ixNetworkTclServerIp -version $ixNetworkVersion} errMsg
if {$errMsg != "::ixNet::OK"} {
    puts "\nFailed to connect to the IxNetwork Tcl server. Exiting.\n"
    exit
}


set root [ixNet getRoot]

ixNet execute newConfig

foreach {ixChassisIp ports} [array get portList *] {
    set ixChassis [ixNet add [ixNet getRoot]/availableHardware chassis]
    ixNet setAttribue $ixChassis -hostname $ixChassisIp
    set ixChassis [lindex [ixNet remapIds $ixChassis] 0]

    foreach port $ports {
	set port [split $port /]
	set cardNumber [lindex $port 0]
	set portNumber [lindex $port 1]
	puts "Clearing port state on $ixChassisIp: $cardNumber/$portNumber ..."
	
	# ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:2
	catch {ixNet execute clearOwnership "::ixNet::OBJ-/availableHardware/chassis:\"$ixChassisIp\"/card:$cardNumber/port:$portNumber"} errMsg
	if {[regexp "Unable" $errMsg]} {
	    puts "Failed to clear port ownership"
	    exit
	}
	
	set vPort [ixNet add [ixNet getRoot] vport]
	ixNet commit
	set vPort [lindex [ixNet remapIds $vPort] 0]
	lappend vPortList $vPort
	
	set getVport($ixChassisIp:$cardNumber/$portNumber) $vPort
	set getPort($vPort) $ixChassisIp:$cardNumber/$portNumber
    }
}

puts \n
parray endpoint
parray getVport
parray getPort
puts \n

foreach vPort $vPortList {
    set port $getPort($vPort) ;# 10.205.4.155:1/1
    set ixiaChassisIp [lindex [split $port :] 0]
    set cardNumber [lindex [split [lindex [split $port :] 1] /] 0]
    set portNumber [lindex [split [lindex [split $port :] 1] /] 1]

    # /availableHardware/chassis:\"$ixChassisIp\"/card:$cardNumber/port:$portNumber
    puts "Connecting to: $ixiaChassisIp:$cardNumber/$portNumber : Rebooting ..."
    ixNet setAttribute $vPort \
	-connectedTo ::ixNet::OBJ-/availableHardware/chassis:\"$ixiaChassisIp\"/card:$cardNumber/port:$portNumber \
	-assignedTo $ixiaChassisIp:$cardNumber:$portNumber \
	-name "$ixiaChassisIp:$cardNumber/$portNumber"
}
ixNet commit

puts "\nCreating a new Traffic Item ..."
set trafficItemObj [ixNet add $root/traffic trafficItem]
    ixNet setMultAttrs $trafficItemObj\
	-enabled True \
	-name TrafficItem_1 \
	-routeMesh oneToOne \
	-srcDestmesh oneToOne \
	-transmitMode interleaved \
	-trafficType raw
    ixNet commit

set trafficItem [lindex [ixNet remapIds $trafficItemObj] 0]

# set endpoint($ixChassisIp1:1/1,$ixChassisIp1:1/2 $ixChassisIp1:1/3) "1.1.1.1 100 200.1.1.1 100"
foreach {srcDstEndpoints properties} [array get endpoint *] {
    set srcPortInfo [lindex [split $srcDstEndpoints ,] 0] ;# $ixChassisIp1:1/1
    set srcPortIxChassisIp [lindex [split $srcPortInfo :] 0]
    set srcPort [lindex [split $srcPortInfo :] 1]
    set srcPortVport $getVport($srcPortIxChassisIp:$srcPort)

    puts "\nforeach srcDstEndpoints: $srcDstEndpoints\n"

    # Build a list of all the dstPorts in vport format
    set dstPortList [lrange [split $srcDstEndpoints ,] 1 end]
    set dstPortList [string map {\{ ""} $dstPortList]
    set dstPortList [string map {\} ""} $dstPortList]

    set listOfDstPorts {}
    foreach port $dstPortList {
	lappend listOfDstPorts $port
    }

    puts "\nlistOfDstPorts: $listOfDstPorts"

    regexp "::ixNet::OBJ-(.*)" $$getVport($srcPortIxChassisIp:$srcPort) - srcVportProtocol
    set srcVportProtocol $srcVportProtocol/protocols

    set dstPortVportList {}
    set listOfPhyDstPorts {}
    foreach dstPortInfo $listOfDstPorts {
	set dstPortIxChassisIp [lindex [split $dstPortInfo :] 0]
	# dstPort: 1/2 10.205.4.155
	set dstPort [lindex [split $dstPortInfo :] 1]
	puts "\ndstPortIxChassisIp: $dstPortIxChassisIp"

	set dstPortVport $getVport($dstPortIxChassisIp:$dstPort)
	puts "\ndstPortVport: $dstPortVport"

	# ::ixNet::OBJ-/vport:2/protocols <-- Need to trim off ::ixNet::OBJ-
	lappend listOfPhyDstPorts $dstPort
	regexp "::ixNet::OBJ-(.*)" $getVport($dstPortIxChassisIp:$dstPort)/protocols - dstVportProtocol
	lappend dstPortVportList $dstVportProtocol 
    }	

    puts "\nsrcVportProtocol: [list $srcVportProtocol]"
    puts "\ndstPortVportList: [list $dstPortVportList]"

    set endPointObject [ixNet add $trafficItem endpointSet]

    puts "Creating an endpoint: srcPort=$srcPort : dstPort=$listOfPhyDstPorts"
    ixNet setMultiAttrs $endPointObject \
	-destinations $dstPortVportList \
	-sources $srcVportProtocol
    ixNet commit

    set endpointObject [lindex [ixNet remapIds $endPointObject] 0]
}

if 0 {
    foreach {srcDstEndpoints properties} [array get endpoint *] {
	set srcPortInfo [lindex [split $srcDstEndpoints ,] 0] ;# $ixChassisIp1:1/1
	set dstPortInfo [lindex [split $srcDstEndpoints ,] 1] ;# $ixChassisIp1:1/2
	
	set srcPortIxChassisIp [lindex [split $srcPortInfo :] 0]
	set srcPort [lindex [split $srcPortInfo :] 1]
	set srcPortVport $getVport($srcPortIxChassisIp:$srcPort)
	
	set dstPortIxChassisIp [lindex [split $dstPortInfo :] 0]
	set dstPort [lindex [split $dstPortInfo :] 1]
	set dstPortVport $getVport($dstPortIxChassisIp:$dstPort)
	
	set endPointObject [ixNet add $trafficItem endpointSet]
	
	puts "Creating an endpoint: srcPort=$srcPort : dstPort=$dstPort"
	ixNet setMultiAttrs $endPointObject \
	    -destinations $dstPortVport/protocols \
	    -sources $getVport($srcPortIxChassisIp:$srcPort)/protocols
	ixNet commit
	
	set endpointObject [lindex [ixNet remapIds $endPointObject] 0]
    }
}

set protocolTemplate [ixNet getList [ixNet getRoot]/traffic protocolTemplate]

# Uncomment this foreach loop for viewing all protocol templates only.
#foreach proto $protocolTemplate {
#    puts "\t$proto"
#}

set mplsIndex [lsearch -regexp $protocolTemplate mpls]
set mplsProtocolTemplate [lindex $protocolTemplate $mplsIndex]

set ipv4Index [lsearch -regexp $protocolTemplate ipv4]
set ipv4ProtocolTemplate [lindex $protocolTemplate $ipv4Index]

#puts "---- mpls: $mplsProtocolTemplate ----"
#puts "---- ipv4: $ipv4ProtocolTemplate ----"

set trafficItem [lindex [ixNet getList $root/traffic trafficItem] 0]
# :OBJ-/traffic/trafficItem:1/configElement:1/stack:"ethernet-1"

foreach configElement [ixNet getList $trafficItem configElement] {
    set dstPortList {}
    puts "\nconfigElement: $configElement"

    set endpointId [ixNet getAttribute $configElement -endpointSetId]
    puts "\tendpointId: $endpointId"

    set srcEndpointVport [ixNet getAttribute $trafficItem/endpointSet:$endpointId -sources]
    set dstEndpointVport [ixNet getAttribute $trafficItem/endpointSet:$endpointId -destinations]

    puts "\tsrcEndpointVport=$srcEndpointVport : dstEndpointVport=$dstEndpointVport"

    # Convert each $dstEndpointVport into $ixChassisIp:1/1 and build a list

    foreach dstEp $dstEndpointVport {
	# ::ixNet::OBJ-/vport:3/protocols
	regexp "(::ixNet::OBJ-/vport:\[0-9]+).*" $dstEp - dstVport
	lappend dstPortList $getPort($dstVport)
    }

    puts "\ndstPortList: $dstPortList"

    # Example: /vport:1/protocols
    set srcVport [split $srcEndpointVport /]
    set srcVport [join [lrange $srcVport 0 1] /]
    set srcPort $getPort($srcVport)
    set srcPort [lindex [split $srcPort :] 1]
    set srcPortIxChassisIp [lindex [split $getPort($srcVport) :] 0]

#    set dstVport [split $dstEndpointVport /]
#    set dstVport [join [lrange $dstVport 0 1] /]
#    set dstPort $getPort($dstVport)
#    set dstPort [lindex [split $dstPort :] 1]
#    set dstPortIxChassisIp [lindex [split $getPort($dstVport) :] 0]

    # Example: set endpoint($ixChassisIp1:1/1,{$ixChassisIp1:1/2 $ixChassisIp1:1/2}) "1.1.1.1 100 200.1.1.1 100"
    set endpointProperties $endpoint($srcPortIxChassisIp:$srcPort,[list $dstPortList])

    set srcIp [lindex $endpointProperties 0]
    set srcTotalIpCount [lindex $endpointProperties 1]

    set dstIp [lindex $endpointProperties 2]
    set dstTotalIpCount [lindex $endpointProperties 3]

    set ethernetStack [lindex [ixNet getList $configElement stack] 0]	
    ixNet exec append $ethernetStack $mplsProtocolTemplate
    
    puts "\tConfiguring MPLS value to 0 ..."
    ixNet setAttribute $configElement/stack:\"mpls-2\"/field:\"mpls.label.value-1\" \
	-fieldValue 0 \
	-valueList [list 16] \
	-stepValue 16 \
	-startValue 16 \
	-singleValue 0 \
	-optionalEnabled true \
	-seed 1 \
	-fixedBits 16 \
	-randomMask 16
    ixNet commit

    set mplsProtocolStack [lindex [ixNet getList $configElement stack] 1]
    ixNet exec append $mplsProtocolStack $ipv4ProtocolTemplate

    puts "\tConfiguring starting srcIP: $srcIp : TotalCount= $srcTotalIpCount"
    ixNet setAttribute $configElement/stack:\"ipv4-3\"/field:\"ipv4.header.srcIp-27\" \
	-fieldValue 0.0.0.0 \
	-countValue $srcTotalIpCount \
	-valueList [list 0.0.0.0] \
	-stepValue 0.0.0.1 \
	-startValue $srcIp \
	-valueType increment \
	-singleValue 0.0.0.0 \
	-optionalEnabled true \
	-seed 1 \
	-fixedBits 0.0.0.0 \
	-randomMask 0.0.0.0

    ixNet commit
    
    puts "\tConfiguring starting destIp: $dstIp : TotalCount= $dstTotalIpCount"
    ixNet setAttribute $configElement/stack:\"ipv4-3\"/field:\"ipv4.header.dstIp-28\" \
	-fieldValue 0.0.0.0 \
	-countValue $dstTotalIpCount \
	-valueList [list 0.0.0.0] \
	-stepValue 0.0.0.1 \
	-startValue $dstIp \
	-valueType increment \
	-singleValue 0.0.0.0 \
	-optionalEnabled true \
	-seed 1 \
	-fixedBits 0.0.0.0 \
	-randomMask 0.0.0.0
    ixNet commit

    puts "\tSelecting the source IP as primary link"
    ixNet setAttribute $configElement/stackLink:\"ipv4-3-srcIp-27\" \
	-linkedTo $configElement/stackLink:\"ipv4-3-dstIp-28\"

    ixNet setMultiAttribute $configElement/stackLink:"ipv4-3-dstIp-28" \
	-linkedTo ::ixNet::OBJ-null
    ixNet commit
}

