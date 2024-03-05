################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################


#------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
# Showcase Flow Aggregation Custom Views


proc displayView {viewRef {pageNum 1}} {
    set totalPages [ixNet getA $viewRef/page -totalPages]
    if {$pageNum > $totalPages} {set pageNum $totalPages}

    ixNet setA $viewRef/page -currentPage $pageNum
    ixNet commit

    set cap [ixNet getA $viewRef -caption]
    puts $cap
    puts [string repeat * [string length $cap]]
    foreach row [ixNet getA $viewRef/page -rowValues] {
	puts {}
	set row [lindex $row 0]
	foreach {col} [ixNet getA $viewRef/page -columnCaptions] {val} $row {
	    puts [format "%-30s: %s" $col $val]
	}
	flush stdout
	puts "[string repeat = 70]\n"
    }
}


proc configIxNetwork {} {
    # START CONFIG
    # Traffic over dhcpServer ends no supported use Static IP
    ixNet exec newConfig

    set r [ixNet getRoot]
    set vPortList []
    foreach p {1 2} {
	set vPort$p [ixNet add $r vport]
	ixNet setA [set vPort$p] -name Port$p
	ixNet commit
	set vPort$p [ixNet remapIds [set vPort$p]]
	lappend vPortList [set vPort$p]
    }

    # Static IP config start
    ixNet setA $vPort1 -name {Port#1}
    ixNet setA $vPort2 -name {Port#2}

    foreach p {1 2} {
	set eth$p [ixNet add [set vPort$p]/protocolStack ethernet]
    }
    ixNet commit

    foreach p {1 2} {
	set ipEnd$p [ixNet add [set eth$p] ipEndpoint]
	ixNet commit
	set ipEnd$p [ixNet remapIds [set ipEnd$p]]
    }

    foreach p {1 2} {
	set ipRange$p [ixNet add [set ipEnd$p] range]
	ixNet commit
	set ipRange$p [ixNet remapIds [set ipRange$p]]

	ixNet setM [set ipRange$p]/ipRange	\
	    -count 100			\
	    -ipType	IPv4			\
	    -ipAddress 11.11.[set p].1	\
	    -prefix 16
	ixNet setM [set ipRange$p]/vlanRange    \
	    -enabled true			    \
	    -uniqueCount 8			    \
	    -firstId 0
	ixNet commit


	set ip6Range$p [ixNet add [set ipEnd$p] range]
	ixNet commit
	set ip6Range$p [ixNet remapIds [set ip6Range$p]]

	ixNet setM [set ip6Range$p]/ipRange	\
	    -count 100			\
	    -ipType	IPv6			\
	    -ipAddress 2001:[set p]::1	\
	    -prefix 64

	ixNet setM [set ip6Range$p]/vlanRange   \
	    -enabled true			    \
	    -uniqueCount 8			    \
	    -firstId 8
	ixNet commit
    }
    ixNet commit
    # Static IP config end

    # Traffic config start

    set tr [ixNet add $r/traffic trafficItem]
    ixNet setM $tr			\
	-name {IPv4 Traffic Item}	\
	-biDirectional  true	\
	-srcDestMesh    manyToMany	\
	-trafficType    ipv4	\
	-transmitMode   sequential
    ixNet commit
    set tr [ixNet remapIds $tr]

    set e [ixNet add $tr endpointSet]
    ixNet setM $e \
	-sources $vPort1/protocolStack \
	-destinations $vPort2/protocolStack
    ixNet commit
    set e [ixNet remapIds $e]

    set ce [ixNet getL $tr configElement]
    ixNet setA $ce/frameSize -fixedSize 66
    ixNet commit

    #puts [ixNet getA $tr/tracking -availableTrackBy]
    ixNet setM $tr/tracking \
	-trackBy {ipv4SourceIp0}
    ixNet setM $tr/tracking/egress	\
	-enabled true		\
	-offset {Outer VLAN ID (4 bits)}
    ixNet commit

    #v6
    set tr6 [ixNet add $r/traffic trafficItem]
    ixNet setM $tr6			\
	-name {IPv6 Traffic Item}	\
	-biDirectional  true	\
	-srcDestMesh    manyToMany	\
	-trafficType    ipv6	\
	-transmitMode   sequential
    ixNet commit
    set tr6 [ixNet remapIds $tr6]

    set e6 [ixNet add $tr6 endpointSet]
    ixNet setM $e6 \
	-sources $vPort1/protocolStack \
	-destinations $vPort2/protocolStack
    ixNet commit
    set e6 [ixNet remapIds $e6]

    set ce6 [ixNet getL $tr6 configElement]
    ixNet setA $ce6/frameSize -fixedSize 86
    ixNet commit

    #puts [ixNet getA $tr6/tracking -availableTrackBy]
    ixNet setM $tr6/tracking \
	-trackBy {ipv6SourceIp0}
    ixNet setM $tr6/tracking/egress	\
	-enabled true		\
	-offset {Outer VLAN ID (4 bits)}
    ixNet commit
    # Traffic L23 end
    # END CONFIG
}

proc Action {ports} {
    # Start the test
    set r [ixNet getRoot]			;# root of Data Model
    set vPortList [ixNet getL $r vport]		;# virtual ports in the configuration

    puts "Assigning ports..."
    ::ixTclNet::AssignPorts $ports {} $vPortList
    foreach vp $vPortList {ixNet setA $vp -txMode sequential}
    ixNet commit
    puts "DONE"

    ixNet exec clearStats
    puts -nonewline "Starting protocols"
    set job [ixNet -async exec startAllProtocols]
    while {![ixNet isDone $job]} {after 1000; puts -nonewline .; flush stdout}
    puts "DONE [ixNet getResult $job]"

    foreach {tr tr6} [ixNet getL $r/traffic trafficItem] {}

    puts "Tracking: [ixNet getA $tr/tracking -trackBy]"
    puts "Tracking: [ixNet getA $tr6/tracking -trackBy]"

    puts "Applying traffic..."
    ::ixTclNet::ApplyTraffic
    puts "Starting traffic..."
    ::ixTclNet::StartTraffic
    puts "DONE"

    # IPv4 View
    set mv [ixNet add $r/statistics view]
    ixNet setM $mv \
	-caption {IPv4 Flow Aggregation} \
	-visible true \
	-type layer23TrafficFlow
    ixNet commit
    set mv [lindex [ixNet remapIds $mv] 0]

    set portFil [ixNet getL $mv availablePortFilter]
    set ti4Fil [lindex [ixNet getL $mv availableTrafficItemFilter] 0]
    set trkFil [ixNet getL $mv availableTrackingFilter]
    set trk4Fil [lrange $trkFil 0 1]


    ixNet setM $mv/layer23TrafficFlowFilter	\
	-aggregatedAcrossPorts false	\
	-portFilterIds $portFil		\
	-trafficItemFilterId $ti4Fil
    ixNet commit

    foreach tk $trk4Fil {
	set fil [ixNet add $mv/layer23TrafficFlowFilter enumerationFilter]
	ixNet setM $fil \
	    -trackingFilterId $tk \
	    -sortDirection ascending
    }
    ixNet commit

    foreach st [ixNet getL $mv statistic] {
	ixNet setA $st -enabled true
    }
    ixNet commit

    ixNet setA $mv -enabled true
    ixNet commit

    displayView $mv

    # IPv6 View
    set mv [ixNet add $r/statistics view]
    ixNet setM $mv \
	-caption {IPv6 Flow Aggregation} \
	-visible true \
	-type layer23TrafficFlow
    ixNet commit
    set mv [lindex [ixNet remapIds $mv] 0]

    set portFil [ixNet getL $mv availablePortFilter]
    set ti6Fil [lindex [ixNet getL $mv availableTrafficItemFilter] 1]
    set trkFil [ixNet getL $mv availableTrackingFilter]
    set trk6Fil [lrange $trkFil 1 2]


    ixNet setM $mv/layer23TrafficFlowFilter	\
	-aggregatedAcrossPorts false	\
	-portFilterIds $portFil		\
	-trafficItemFilterId $ti6Fil
    ixNet commit

    foreach tk $trk6Fil {
	set fil [ixNet add $mv/layer23TrafficFlowFilter enumerationFilter]
	ixNet setM $fil \
	    -trackingFilterId $tk \
	    -sortDirection ascending
    }
    ixNet commit

    foreach st [ixNet getL $mv statistic] {
	ixNet setA $st -enabled true
    }
    ixNet commit

    ixNet setA $mv -enabled true
    ixNet commit

    displayView $mv
}


set ports  {{10.205.17.97 1 3} {10.205.17.97 1 4}}

puts [string toupper [info script]]

package require IxTclNetwork
ixNet connect localhost -version 5.40

configIxNetwork
Action $ports
