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
# CSV Snapshot on default and custom statistics views


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


    # PPP config start
    foreach p {1 2} {
	set e$p [ixNet add [set vPort$p]/protocolStack ethernet]
	set ppp$p [ixNet add [set e$p] pppoxEndpoint]
	ixNet commit
	set ppp$p [ixNet remapIds [set ppp$p]]
	unset e$p
    }

    foreach p {1 2} {
	set pppRange$p [ixNet add [set ppp$p] range]
	ixNet setM [set pppRange$p]/pppoxRange \
	    -numSessions 20 \
	    -authType chap
	ixNet commit
	set pppRange$p [ixNet remapIds [set pppRange$p]]
    }
    unset p

    set po [ixNet add $vPort1/protocolStack pppoxOptions]
    ixNet setA $po -role server
    ixNet setA $vPort1 -name {PPPoE Server}
    ixNet commit

    set po [ixNet add $vPort2/protocolStack pppoxOptions]
    ixNet setA $po -role client
    ixNet setA $vPort2 -name {PPPoE Client}
    ixNet setA $po -associates $vPort1/protocolStack
    ixNet commit
    unset po
    # PPP config end

    # Traffic L23 config start
    set tr [ixNet add $r/traffic trafficItem]
    ixNet setM $tr \
	-biDirectional  true \
	-srcDestMesh    manyToMany \
	-trafficType    ipv4 \
	-transmitMode   sequential
    ixNet commit
    set tr [ixNet remapIds $tr]

    set e [ixNet add $tr endpointSet]
    ixNet setM $e \
	-sources $vPort1/protocolStack \
	-destinations $vPort2/protocolStack
    ixNet commit
    set e [ixNet remapIds $e]

    set cfgEl [ixNet getL $tr configElement]
    ixNet setA $cfgEl/frameSize -fixedSize 128
    ixNet commit

    #puts [ixNet getA $tr/tracking -availableTrackBy]
    ixNet setM $tr/tracking \
	-trackBy {ipv4SourceIp0 ipv4DestIp0}
    ixNet commit

    # Traffic L23 config end
    # END CONFIG
}

proc Action {ports} {
    # Start the test
    set r [ixNet getRoot]			;# root of Data Model
    set vPortList [ixNet getL $r vport]		;# virtual ports in the configuration

    puts "Assigning ports..."
    ::ixTclNet::AssignPorts $ports {} $vPortList
    foreach p $vPortList {ixNet setA $p -txMode sequential}
    ixNet commit
    puts "DONE"
    after 1000

    ixNet exec clearStats
    puts "Starting protocols..."
    ixNet exec startAllProtocols
    puts "DONE"

    after 10000

    puts "Applying traffic..."
    ::ixTclNet::ApplyTraffic

    puts "Starting traffic..."
    ::ixTclNet::StartTraffic
    puts "DONE"

    after 10000

    # layer23TrafficFlow
    set mv [ixNet add $r/statistics view]
    ixNet setM $mv \
	-caption layer23TrafficFlow \
	-type layer23TrafficFlow \
	-visible true
    ixNet commit
    set mv [lindex [ixNet remapIds $mv] 0]

    set portFil [ixNet getL $mv availablePortFilter]
    set tiFil [lindex [ixNet getL $mv availableTrafficItemFilter] 0]

    set fil [ixNet getL $mv layer23TrafficFlowFilter]
    ixNet setM $fil \
	-portFilterIds $portFil \
	-trafficItemFilterId $tiFil
    ixNet commit

    foreach atk [ixNet getL $mv availableTrackingFilter] {
	set ef [ixNet add $fil enumerationFilter]
	ixNet setM $ef \
	    -sortDirection ascending \
	    -trackingFilterId $atk
	ixNet commit
    }

    foreach s [ixNet getL $mv statistic] {ixNet setA $s -enabled true}
    ixNet commit

    ixNet setA $mv -enabled true
    ixNet commit

    displayView $mv

    # layer23ProtocolPort
    set mv [ixNet add $r/statistics view]
    ixNet setM $mv \
	-caption layer23ProtocolPort \
	-type layer23ProtocolPort \
	-visible true
    ixNet commit
    set mv [lindex [ixNet remapIds $mv] 0]

    set fil [ixNet getL $mv layer23ProtocolPortFilter]
    ixNet setA $fil -portFilterIds \
	[ixNet getL $mv availablePortFilter]
    ixNet commit

    foreach s [ixNet getL $mv statistic] {ixNet setA $s -enabled true}
    ixNet commit

    ixNet setA $mv -enabled true
    ixNet commit

    displayView $mv

    # layer23TrafficItem
    set mv [ixNet add $r/statistics view]
    ixNet setM $mv \
	-caption layer23TrafficItem \
	-type layer23TrafficItem \
	-visible true
    ixNet commit
    set mv [lindex [ixNet remapIds $mv] 0]

    set tiFil [ixNet getL $mv availableTrafficItemFilter]

    set fil [ixNet getL $mv layer23TrafficItemFilter]
    ixNet setM $fil \
	-trafficItemFilterIds $tiFil
    ixNet commit

    foreach s [ixNet getL $mv statistic] {ixNet setA $s -enabled true}
    ixNet commit

    ixNet setA $mv -enabled true
    ixNet commit

    displayView $mv


    # layer23TrafficFlowDetective
    set mv [ixNet add $r/statistics view]
    ixNet setM $mv \
	-caption layer23TrafficFlowDetective \
	-type layer23TrafficFlowDetective \
	-visible true
    ixNet commit
    set mv [lindex [ixNet remapIds $mv] 0]

    set portFil [ixNet getL $mv availablePortFilter]
    set tiFil [lindex [ixNet getL $mv availableTrafficItemFilter] 0]
    set srtFil [ixNet getF $mv availableStatisticFilter -caption {Rx Frames}]

    set fil [ixNet getL $mv layer23TrafficFlowDetectiveFilter]
    ixNet setM $fil \
	-portFilterIds $portFil \
	-trafficItemFilterId $tiFil \
	-flowFilterType allFlows
    ixNet setM $fil/allFlowsFilter \
	-sortByStatisticId $srtFil
    ixNet commit

    foreach s [ixNet getL $mv statistic] {ixNet setA $s -enabled true}
    ixNet commit

    ixNet setA $mv -enabled true
    ixNet commit

    displayView $mv


    # layer23ProtocolStack
    set mv [ixNet add $r/statistics view]
    ixNet setM $mv \
	-caption layer23ProtocolStack \
	-type layer23ProtocolStack \
	-visible true
    ixNet commit
    set mv [lindex [ixNet remapIds $mv] 0]

    set afil [ixNet getL $mv availableProtocolStackFilter]
    set fil [ixNet getL $mv layer23ProtocolStackFilter]
    set srtStat [lindex [ixNet getF $mv statistic -caption {Interface Identifier}] 0]

    ixNet setM $fil \
	-protocolStackFilterId $afil    \
	-sortingStatistic $srtStat	    \
	-sortAscending true
    ixNet commit

    foreach s [ixNet getL $mv statistic] {ixNet setA $s -enabled true}
    ixNet commit

    ixNet setA $mv -enabled true
    ixNet commit

    displayView $mv


    # layer23TrafficPort
    set mv [ixNet add $r/statistics view]
    ixNet setM $mv \
	-caption layer23TrafficPort	\
	-type layer23TrafficPort \
	-visible true
    ixNet commit
    set mv [lindex [ixNet remapIds $mv] 0]

    set pFil [ixNet getL $mv availablePortFilter]
    set fil [ixNet getL $mv layer23TrafficPortFilter]

    ixNet setM $fil \
	-portFilterIds $pFil
    ixNet commit

    foreach s [ixNet getL $mv statistic] {ixNet setA $s -enabled true}
    ixNet commit

    ixNet setA $mv -enabled true
    ixNet commit

    displayView $mv

    puts "Saving CSV Snapshots..."
    # Save views snapshots in CSVs
    set opts [::ixTclNet::GetDefaultSnapshotSettings]	    ;# default Snapshot opts to customize
    set idx [lsearch $opts *Template*]
    set opts [lreplace $opts $idx $idx]			    ;# removing Template related key

    set loc [file join [pwd] SnapshotCSV]		    ;# directory to save CSVs
    lset opts [lsearch $opts *Location*] [subst {Snapshot.View.Csv.Location: $loc}]
    lset opts [lsearch $opts *GeneratingMode*] {Snapshot.View.Csv.GeneratingMode: kOverwriteCSVFile}
    lset opts [lsearch $opts *Settings.Name*] {Snapshot.Settings.Name: "MySnapshot"}

    lset opts [lsearch $opts *Name*] {Snapshot.View.Csv.Name: "TrafficItemStats"}
    ::ixTclNet::TakeViewCSVSnapshot [list {Traffic Item Statistics}] $opts
    after 5000
    lset opts [lsearch $opts *Name*] {Snapshot.View.Csv.Name: "FlowStats"}
    ::ixTclNet::TakeViewCSVSnapshot [list {Flow Statistics}] $opts
    after 10000
    lset opts [lsearch $opts *Name*] {Snapshot.View.Csv.Name: "PPP_General_Statistics"}
    ::ixTclNet::TakeViewCSVSnapshot [list {PPP General Statistics}] $opts
    after 10000

    lset opts [lsearch $opts *Name*] {Snapshot.View.Csv.Name: "layer23TrafficFlow"}
    ::ixTclNet::TakeViewCSVSnapshot [list {layer23TrafficFlow}] $opts
    after 10000

    lset opts [lsearch $opts *Name*] {Snapshot.View.Csv.Name: "layer23ProtocolPort"}
    ::ixTclNet::TakeViewCSVSnapshot [list {layer23ProtocolPort}] $opts
    after 10000

    lset opts [lsearch $opts *Name*] {Snapshot.View.Csv.Name: "layer23TrafficItem"}
    ::ixTclNet::TakeViewCSVSnapshot [list {layer23TrafficItem}] $opts
    after 10000

    lset opts [lsearch $opts *Name*] {Snapshot.View.Csv.Name: "layer23TrafficFlowDetective"}
    ::ixTclNet::TakeViewCSVSnapshot [list {layer23TrafficFlowDetective}] $opts
    after 10000

    lset opts [lsearch $opts *Name*] {Snapshot.View.Csv.Name: "layer23ProtocolStack"}
    ::ixTclNet::TakeViewCSVSnapshot [list {layer23ProtocolStack}] $opts
    after 10000

    lset opts [lsearch $opts *Name*] {Snapshot.View.Csv.Name: "layer23TrafficPort"}
    ::ixTclNet::TakeViewCSVSnapshot [list {layer23TrafficPort}] $opts
    after 10000

    puts "DONE"
}


set ports  {{10.205.17.97 1 3} {10.205.17.97 1 4}}

puts [string toupper [info script]]

package require IxTclNetwork
ixNet connect localhost -version 5.40

configIxNetwork
Action $ports
