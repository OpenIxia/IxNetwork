#
# CFM Traffic Utils to be used in the Traffic test cases
#


################################################################################
# Procedure : generateApplyTraffic
# Purpose   : To Generate and Apply Traffic
# Parameters    : None
# Return    : (Bool) 0 - Applied Traffic 1 - Failed to Apply Traffic
################################################################################
proc generateApplyTraffic {} {

    set flag 1
    set traffic [ixNet getRoot]/traffic
    # Generate Traffic
    set genTraffic [ixNet setAtt $traffic -refreshLearnedInfoBeforeApply  true]
    if {$genTraffic != "::ixNet::OK"} {
        puts "Not able to generate  the traffic.."
        return $flag
    }
    after 10000

    puts "Appling the traffic...."
    set appTraffic [::ixNet exec apply $traffic]
    if {$appTraffic != "::ixNet::OK"} {
        puts "Not able to apply the traffic.."
        return $flag
    }
    after 10000
    set flag 0
    return $flag
}

################################################################################
#Procedure  : startTraffic
#Purpose    : To Start the Traffic
#Parameters     : None
#Return     : (Bool) 0 - Started Traffic Successfully 1 - Failed to Start the Traffic
################################################################################
proc startTraffic {} {
    set flag 1
    set traffic [ixNet getRoot]/traffic
    puts "Starting the traffic..."
    set startTraffic [::ixNet exec start $traffic]
    if {$startTraffic != "::ixNet::OK"} {
        puts "Not able to start the traffic.."
    return $flag
    }
    set flag 0
    return $flag
}

################################################################################
#Procedure  :stopTraffic
#Purpose    : To Stop the Traffic
#Parameters : None
#Return     : (Bool) 0 - Stopped Traffic Successfully 1 - Failed to Stop the Traffic
################################################################################

proc stopTraffic {} {
    set flag 1
    set traffic [ixNet getRoot]/traffic
    puts "Stopping the traffic...."
    set stopTraffic [::ixNet exec stop $traffic]
    if {$stopTraffic != "::ixNet::OK"} {
        puts "Not able to stop the traffic.."
        return $flag
    }
    after 10000

    set flag 0
    return $flag
}

################################################################################
#Procedure  : captureMode
#Purpose    : To change the mode of the Port p2 to Capture Mode
#Parameters : port (port)
#Return     : None
################################################################################

proc captureMode {port} {
    ixNet setAttribute $port -rxMode capture
    ixNet setAttribute $port/capture -hardwareEnabled true
    ixNet commit
    after 5000
}

################################################################################
#Procedure  : measureMode
#Purpose    : To change the mode of the port p2 to measure flow mode
#Parameters : port (port )
#Return     : None
################################################################################

proc measureMode {port} {
    ixNet setAttribute $port -rxMode measure
    ixNet setAttribute $port/capture -hardwareEnabled false
    ixNet commit
    after 5000
}
################################################################################
#Procedure  : TxRxCalculation
#Purpose    : To calculate the Tx - Rx Rate and to check if the Rx rate is equal to expected Rx Rate
#Parameters : TxFrame Value RxFrame Value
#Return     : (Bool) 0 - If the Rx Frame is greater than or equal to delta percentage  the value of Tx Frame
################################################################################

proc TxRxCalculation {TxFrame RxFrame {tolerance 15} } {
    set flag 1
    set minRxFrame [expr ($TxFrame - ($TxFrame * $tolerance)/100)]
    puts "Frames Received: $RxFrame Frames Transmitted: $TxFrame (considering 15%% tolerence $minRxFrame)"
    if {$RxFrame < $minRxFrame} {
        puts "Frames Received is less than Frames Transmitted (considering 15%% tolerence)"
        return $flag
    }

    set flag 0
    return $flag
}

################################################################################
#Procedure  : checkAllTrafficStats
#Purpose    : To verify Traffic Stats for specified tolerance
#Parameters : pageMax, rowPerPage, tolerance
#Return     : (Bool) 0 - If the no. of Rx Frames is less than or equal to no. of Tx Frames within tolerance.
################################################################################

proc checkAllTrafficStats {{tolerance 0} {rowPerPage 50} {pageList "all"}} {
    set flag 1
    set statistic [ixNet getRoot]/statistics
    set statsViewList [ixNet getList $statistic trafficStatViewBrowser]
    set indexOftrafficStats [lsearch -regexp $statsViewList "Traffic Statistics"]
    set trafficStatsView [lindex $statsViewList $indexOftrafficStats]
    ixNet setAttr $trafficStatsView -enabled true
    ixNet setAttr $trafficStatsView -pageSize $rowPerPage
    ixNet commit

    set pageMax [ixNet getAttr $trafficStatsView -totalPages]
    puts "Actual Number of pages available: $pageMax"

    set pagesToBrowse {}
    for {set page 1} {$page <= $pageMax} {incr page} {
        lappend pagesToBrowse $page
    }

    if {$pageList != "all"} {
        set pagesToBrowse $pageList
    }

    # Verify TxFrames and RxFrames for all the flows
    foreach page $pagesToBrowse {
        if {$page > $pageMax} {
            puts "Can't browse for $page, max Page available is $pageMax"
            return $flag
        }
        ixNet setAttr $trafficStatsView -currentPageNumber $page
        ixNet commit
        after 3000

        # check if Stats are ready before verifying them
        set count 0
        set isComplete false
        puts "check if Traffic Stats are ready..."
        while { $isComplete != true } {
            set isComplete [ixNet getAttr $trafficStatsView -isReady]
            puts "isComplete --> $isComplete"
            after 1000
            incr count
            if { $count > 30 } {
                puts "Traffic Stats are still not ready ..."
                return $flag
            }
        }
        puts "Traffic Stats are ready ..."

        set indexMax [llength [ixNet getList $trafficStatsView row]]
        puts "Page $page :: Number of rows $indexMax"
        for {set index 0} {$index < $indexMax} {incr index} {
            set row [lindex [ixNet getList $trafficStatsView row] $index]
            set stats [ixNet getList $row cell]
            set RxFrames [ixNet getAttr [lindex $stats [lsearch -regexp $stats {Rx Frames}]] -statValue]
            set TxFrames [ixNet getAttr [lindex $stats [lsearch -regexp $stats {Tx Frames}]] -statValue]
            set minRxFrames [expr ($TxFrames - ($TxFrames * $tolerance)/100)]

            if {($TxFrames <= 0) || ($RxFrames <= 0) || ($RxFrames < $minRxFrames) || ($RxFrames > $TxFrames)} {
                puts "Stats are not proper for Page $page and Row $index "
                return $flag
            }
            puts "Page No=$page : Row No=$index Traffic Stats correct"

        }
        puts "Page: $page Traffic Stats Verification completed...."
    }

    set flag 0
    return $flag
}


################################################################################
#Procedure  : checkConditionalTrafficStats
#Purpose    : To verify Conditional Traffic Stats
#Parameters : sortStatName needCols maxResults performerType showBestPerformers deadFlowTimeout tolerance
#Return     : (Bool) 0 - If the conditional stats are fine
################################################################################

proc checkConditionalTrafficStats {sortStatName needCols {maxResults 50} {performerType showBestPerformers} {deadFlowTimeout 5} {tolerance 0}} {
    set flag 1

    puts "Creating conditional flows"

    set viewCaption [ixTclNet::CreateConditionalFlowDetectiveView $maxResults $performerType $sortStatName $deadFlowTimeout]
    puts "\nviewCaption = $viewCaption"

    ixTclNet::GetFilteredSnapshotData $viewCaption $needCols StatValueArray 20 1
    parray StatValueArray

    puts "Entering flowDetective to fetch information"
    set flowDetective [ixNet getRoot]/statistics/drilldown/flowDetective

    # There will be always one view that's why we consider index always 0 in the lindex command
    set conditionalTrafficStatsView [ixNet getList $flowDetective view]
    set conditionalTrafficStatsView1  [lindex $conditionalTrafficStatsView 0]
    ixNet setAttribute $conditionalTrafficStatsView1 -enabled True
    ixNet commit

    # Check if Conditional Traffic Stats is ready
    set count 0
    set isComplete false
    puts "Check if Conditional Traffic Stats are ready..."
    while {$isComplete != true} {
        set isComplete [ixNet getAttr $conditionalTrafficStatsView1 -isReady]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if { $count > 30 } {
            puts "Conditional Traffic Stats are still not ready ..."
            return $flag
        }
    }
    puts "Conditional Traffic Stats are ready ..."

    for {set index 0} {$index < $maxResults} {incr index} {
        set row [lindex [ixNet getList $conditionalTrafficStatsView1 row] $index]
        set stats [ixNet getList $row cell]
        set RxFrames [ixNet getAttr [lindex $stats [lsearch -regexp $stats {"Rx Frames"}]] -statValue]
        set TxFrames [ixNet getAttr [lindex $stats [lsearch -regexp $stats {"Tx Frames"}]] -statValue]
        set minRxFrames [expr ($TxFrames - ($TxFrames * $tolerance)/100)]

        if {($TxFrames <= 0) || ($RxFrames <= 0) || ($RxFrames < $minRxFrames) || ($RxFrames > $TxFrames)} {
            puts "Stats are not proper for Row $index "
            return $flag
        }
        puts "Row No=$index Conditional Traffic Stats correct"

    }
    puts "Conditional Traffic Stats verified sucessfully"

    set flag 0
    return $flag

}


