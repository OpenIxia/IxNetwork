#####################################################################################
################################## L2 - L3 TRAFFIC ##################################
#####################################################################################
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
        log "Not able to generate  the traffic.."
        return $flag
    }
    after 10000

    log "Appling the traffic...."
    set appTraffic [::ixNet exec apply $traffic]
    if {$appTraffic != "::ixNet::OK"} {
        log "Not able to apply the traffic.."
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
    log "Starting the traffic..."
    set startTraffic [::ixNet exec start $traffic]
    if {$startTraffic != "::ixNet::OK"} {
        log "Not able to start the traffic.."
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
    log "Stopping the traffic...."
    set stopTraffic [::ixNet exec stop $traffic]
    if {$stopTraffic != "::ixNet::OK"} {
        log "Not able to stop the traffic.."
        return $flag
    }
    after 10000

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
    log "Actual Number of pages available: $pageMax"

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
            log "Can't browse for $page, max Page available is $pageMax"
            return $flag
        }
        ixNet setAttr $trafficStatsView -currentPageNumber $page
        ixNet commit
        after 3000

        # check if Stats are ready before verifying them
        set count 0
        set isComplete false
        log "check if Traffic Stats are ready..."
        while { $isComplete != true } {
            set isComplete [ixNet getAttr $trafficStatsView -isReady]
            log "isComplete --> $isComplete"
            after 1000
            incr count
            if { $count > 30 } {
                log "Traffic Stats are still not ready ..."
                return $flag
            }
        }
        log "Traffic Stats are ready ..."

        set indexMax [llength [ixNet getList $trafficStatsView row]]
        log "Page $page :: Number of rows $indexMax"
        for {set index 0} {$index < $indexMax} {incr index} {
            set row [lindex [ixNet getList $trafficStatsView row] $index]
            set stats [ixNet getList $row cell]
            set RxFrames [ixNet getAttr [lindex $stats [lsearch -regexp $stats {Rx Frames}]] -statValue]
            set TxFrames [ixNet getAttr [lindex $stats [lsearch -regexp $stats {Tx Frames}]] -statValue]
            set minRxFrames [expr ($TxFrames - ($TxFrames * $tolerance)/100)]
            set maxRxFrames [expr ($TxFrames + ($TxFrames * $tolerance)/100)]

            if {($TxFrames <= 0) || ($RxFrames <= 0) || ($RxFrames < $minRxFrames) || ($RxFrames > $maxRxFrames)} {
                log "Stats are not proper for Page $page and Row $index "
                return $flag
            }
            log "Page No=$page : Row No=$index Traffic Stats correct"

        }
        log "Page: $page Traffic Stats Verification completed...."
    }

    set flag 0
    return $flag
}

###############################################################################
# LOR STATS VERIFICATION
###############################################################################

proc GetIxLoadStatValue {viewCaption statName} {

    set statValue 0
    set statViewList [ixNet getList [ixNet getRoot]/statistics statViewBrowser]
    set statViewObjRef ""
    foreach statView $statViewList {
        if {[ixNet getAttribute $statView -name] == $viewCaption} {
            if {[ixNet getAttribute $statView -enabled] == "false"} {
                ixNet setAttribute $statView -enabled true
                ixNet commit
            }
            set statViewObjRef $statView
            break
        }
    }
    if {[info exists statValueArray]} {
        unset statValueArray
    }
    after 1000

    set timeout 10
    while {$timeout > 0} {
        if {[ixNet getAttribute $statViewObjRef -isReady] == true} {
            break
        }
        after 500
        incr timeout -1
    }

    if {[ixNet getAttribute $statViewObjRef -isReady] != true} {
        logMsg "Error: Data is not available."
        return 0
    }

    if {[ixNet getAttribute $statViewObjRef -isReady] != true} {
        logMsg "Error: Data is not available."
        return 0
    }

    set rowList [ixNet getList $statViewObjRef row]
    foreach row $rowList {
        set cellList [ixNet getList $row cell]
        foreach cell $cellList {
            if {[ixNet getAttribute $cell -catalogStatName] == $statName} {
                set statValue [ixNet getAttribute $cell -statValue]
                break
            }
        }
    }
    log " GetIxLoadStatValue value = ($statValue)"
    return $statValue
}

###############################################################################
# Procedure     : CheckAndValidateStats
# Purpose       : To Check and Validate Stats
# Return        : Returns the Obtained IxLoadValue for the specified
###############################################################################

proc CheckAndValidateStats {option1 option2 expValue {per 0} } {
    log "Inside the CheckAndValidateStats procedure."
    for {set i 0} {$i < 5} {incr i } {
        after 20000
        log "Try No : $i"
        set retValue [GetIxLoadStatValue $option1 $option2]
        set temp [expr $retValue * [expr $per.0 / 100 ] ]
        if {$expValue >= [expr $retValue - $temp ] && $expValue <= [expr $retValue + $temp ]} {
            return $retValue
        } else {
            continue
        }
    }
    return $retValue
}



