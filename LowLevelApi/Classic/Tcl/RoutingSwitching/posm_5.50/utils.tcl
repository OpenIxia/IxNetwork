#-------------------------------------------------------------------------------
# PROCEDURE  : checkAllProtocolStatsDefaultView
# PURPOSE    :
# PARAMETERS : portList -
#              stat - {name value} Stat list to verify
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# SUPPORT    : Available for Tcl Publisher Version 5.40 only
#-------------------------------------------------------------------------------
proc checkAllProtocolStatsDefaultView {portLists viewCaption stat {exactMatch 0} {tclPublisherVersion 0}} {
    set error 1

    # For Tcl Pu8blisher version 5.40 & 5.50 no change in SV API
    if {$tclPublisherVersion == "5.50"} {
        set tclPublisherVersion "5.40"
    }
    set procName checkAllProtocolStatsDefaultView_$tclPublisherVersion

    if {[$procName $portLists $viewCaption $stat $exactMatch] == 1} {
        log "Failed to verify Protocol stats from default view for TCL Publisher Version $tclPublisherVersion"
        return $error
    }

    set error 0
    return $error
}

proc checkAllProtocolStatsDefaultView_5.40 {portLists viewCaption stat {exactMatch 0}} {

    set flag 1
    array set statToVerify $stat
    set statNames [array names statToVerify]

    set statsViewList [ixNet getList [ixNet getRoot]/statistics view]
    set indexOfProtocolStats [lsearch -regexp $statsViewList $viewCaption]
    set protocolStatsView [lindex $statsViewList $indexOfProtocolStats]
    set page ${protocolStatsView}/page

    log "Refreshing Statistics View ..."
    set isRefreshed [ixNet exec refresh $protocolStatsView]
    after 2000

    set count 0
    log "Checking Statistics View isReady ..."
    while { [ixNet getAttr $page -isReady] != true } {
        log "isReady --> [ixNet getAttr $page -isReady]"
        after 1000
        incr count
        if { $count > 60 } {
            log "Waited for 1 min, Statistics View still not ready.. "
            return $flag
        }
    }
    log "Statistics View Ready ..."

    # Get Stats
    set pageList [ixNet getAttribute $page -rowValues] ;# first list of all rows in the page
    if {[llength $pageList] <= 0} {
        log "Traffic Stats are not retrievable... "
        return $flag
    }

    foreach stat $statNames {
        puts "[ixNet getAttribute $page -columnCaptions]"
        set statIndex [lsearch -regexp [ixNet getAttribute $page -columnCaptions] $stat]
        set statName [lindex [ixNet getAttribute $page -columnCaptions] $statIndex]
        for {set pageListIndex 0} {$pageListIndex < [llength $pageList]} {incr pageListIndex} {
            set rowList [lindex $pageList $pageListIndex] ;# second list of 1 ingress and x egress rows
            set cellList [lindex $rowList 0] ;# third list of cell values
            set statValue [lindex $cellList $statIndex]
            set portName [lindex $cellList 0]
            set splitString [split $portName /]
            set chassis [lindex $splitString 0]
            set card [string trimleft [string trimleft [lindex $splitString 1] "Card"] 0]
            set port [string trimleft [string trimleft [lindex $splitString 2] "Port"] 0]
            set statValueArray($chassis,$card,$port,$statName) $statValue
        }
    }

    parray statValueArray

    foreach portList $portLists {
        set chassis [lindex $portList 0]
        set card [lindex $portList 1]
        set port [lindex $portList 2]
        foreach statName $statNames {
            log "$statName : $statValueArray($chassis,$card,$port,$statName) (Expected:$statToVerify($statName))"
            if {$statValueArray($chassis,$card,$port,$statName) >= $statToVerify($statName)} {
                if {($exactMatch == 1) && \
                    ($statValueArray($chassis,$card,$port,$statName) != $statToVerify($statName))} {
                    return $flag
                }
            } else {
                log "Stat Mismatched..."
                return $flag
            }
        }
    }

    set flag 0
    return $flag
}
################################################################################
# Procedure : generateApplyTraffic
# Purpose   : To Generate and Apply Traffic
# Parameters    : None
# Return    : (Bool) 0 - Applied Traffic 1 - Failed to Apply Traffic
################################################################################
proc generateApplyTraffic {{refreshBeforeApply true} {lor 0}} {
    set flag 1
    set traffic [ixNet getRoot]/traffic
    # Enable refreshLearnedInfoBeforeApply for MPLS Traffic
    if {[setAndCheckAttributeValue $traffic refreshLearnedInfoBeforeApply [subst {"$refreshBeforeApply" y}]] == 1} {
        ixNetCleanUp
        return $FAILED
    }

    # Apply Traffic
    log "Applying the traffic ...."
    if {$lor == 0} {
        if {[::ixNet exec apply $traffic] != "::ixNet::OK"} {
            log "Not able to apply the traffic.."
            log "[ixNet getAttr $traffic -errors]"
            return $flag
        }
    } else {
        if {[::ixNet exec applyApplicationTraffic $traffic] != "::ixNet::OK"} {
            log "Not able to apply the traffic.."
            log "[ixNet getAttr $traffic -errors]"
            return $flag
        }
        # BUG546874: LoR :: TCL API :: Traffic state not associated with LoR Traffic
        set flag 0
        return $flag
    }
    set count 0
    log "Checking Traffic State ..."
    log "isApplied --> [ixNet getAttr $traffic -state]"
    while { [ixNet getAttr $traffic -state] == "unapplied" } {
        log "isApplied --> [ixNet getAttr $traffic -state]"
        after 1000
        incr count
        if { $count > 60 } {
            log "Waited for 1 min, Traffic still not applied.. "
            foreach trafficItem [ixNet getList $traffic trafficItem] {
                log "[ixNet getAttr $trafficItem -errors]"
                log "[ixNet getAttr $trafficItem -warnings]"

            }
            return $flag
        }
    }
    log "Traffic applied successfully ..."
    foreach trafficItem [ixNet getList $traffic trafficItem] {
        log "[ixNet getAttr $trafficItem -errors]"
        log "[ixNet getAttr $trafficItem -warnings]"
    }

    set flag 0
    return $flag
}



################################################################################
#Procedure  : startTraffic
#Purpose    : To Start the Traffic
#Parameters     : None
#Return     : (Bool) 0 - Started Traffic Successfully 1 - Failed to Start the Traffic
################################################################################
proc startTraffic {traffic {lor 0}} {
    set flag 1
    log "Starting the traffic..."
    set startTraffic 0

    if {$lor == 0} {
        set startTraffic [catch {::ixNet exec startStatelessTraffic $traffic} errMsg]
    } else {
        set startTraffic [catch {::ixNet exec startApplicationTraffic $traffic} errMsg]
    }
    if {$startTraffic} {
        # catch returned 1 error in starting traffic.
        log "$errMsg"
        return $flag
    }

    # BUG546874: LoR :: TCL API :: Traffic state not associated with LoR Traffic
    if {$lor} {
        set flag 0
        return $flag
    }

    set count 0
    log "Checking Traffic State ..."
    while { [ixNet getAttr $traffic -state] != "started" } {
        log "isStarted --> [ixNet getAttr $traffic -state]"
        after 1000
        incr count
        if { $count > 60 } {
            log "Waited for 1 min, Traffic still not started.. "
            foreach trafficItem [ixNet getList $traffic trafficItem] {
                log "[ixNet getAttr $trafficItem -errors]"
                log "[ixNet getAttr $trafficItem -warnings]"

            }
            return $flag
        }
    }
    log "Traffic started successfully ..."
    foreach trafficItem [ixNet getList $traffic trafficItem] {
        log "[ixNet getAttr $trafficItem -errors]"
        log "[ixNet getAttr $trafficItem -warnings]"
    }

    set flag 0
    return $flag
}

################################################################################
#Procedure  :stopTraffic
#Purpose    : To Stop the Traffic
#Parameters : None
#Return     : (Bool) 0 - Stopped Traffic Successfully 1 - Failed to Stop the
#             Traffic
################################################################################

proc stopTraffic {traffic {lor 0}} {
    set flag 1
    log "Stopping the traffic...."

    if {$lor == 0} {
        set stopTraffic [catch {::ixNet exec stopStatelessTraffic $traffic} errMsg]
    } else {
        set stopTraffic [catch {::ixNet exec stopApplicationTraffic $traffic} errMsg]
    }

    if {$stopTraffic} {
        log "$errMsg"
        return $flag
    }

    # BUG546874: LoR :: TCL API :: Traffic state not associated with LoR Traffic
    if {$lor} {
        set flag 0
        return $flag
    }


    set count 0
    log "Checking Traffic State ..."
    while { [ixNet getAttr $traffic -state] != "stopped" } {
        log "isStopped --> [ixNet getAttr $traffic -state]"
        after 1000
        incr count
        if { $count > 60 } {
            log "Waited for 1 min, Traffic still not stopped.. "
            foreach trafficItem [ixNet getList $traffic trafficItem] {
                log "[ixNet getAttr $trafficItem -errors]"
                log "[ixNet getAttr $trafficItem -warnings]"
            }
            return $flag
        }
    }
    log "Traffic stopped successfully ..."
    foreach trafficItem [ixNet getList $traffic trafficItem] {
        log "[ixNet getAttr $trafficItem -errors]"
        log "[ixNet getAttr $trafficItem -warnings]"
    }

    set flag 0
    return $flag
}
set ::BUG508119  0

proc checkAllTrafficStats {viewCaption {tolerance 5} {rowPerPage 50} {pageList "all"} {mcastMultiplier 1}} {

    set flag 1
    set statsViewList [ixNet getList [ixNet getRoot]/statistics view]
    set indexOftrafficStats [lsearch -regexp $statsViewList $viewCaption]
    set trafficStats [lindex $statsViewList $indexOftrafficStats]
    set trafficStatsView ${trafficStats}/page

if {$::BUG508119 == 0} {
    log "Setting the page size for SV $trafficStatsView "
    ixNet setAttr $trafficStatsView -pageSize $rowPerPage
    ixNet commit
    after 2000
}

    log "Refreshing Statistics View ..."
    set isRefreshed [ixNet exec refresh $trafficStats]
    after 2000

    set count 0
    log "Checking Statistics View isReady ..."
    while { [ixNet getAttr $trafficStatsView -isReady] != true } {
        log "isReady --> [ixNet getAttr $trafficStatsView -isReady]"
        after 1000
        incr count
        if { $count > 60 } {
            log "Waited for 1 min, Statistics View still not ready.. "
            return $flag
        }
    }
    log "Statistics View Ready ..."

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
        ixNet setAttr $trafficStatsView -currentPage $page
        ixNet commit
        after 20000

        # check if Stats are ready before verifying them
        set isRefreshed [ixNet exec refresh $trafficStats]
        if {[string equal $isRefreshed "::ixNet::OK"] != 1} {
            log "Traffic Stats are not ready ..."
            return $flag
        }
        log "Traffic Stats are ready ..."

        set indexMax [ixNet getAttribute $trafficStatsView -rowCount]
        if {$indexMax <= 0} {
            log "Traffic Stats are not retrievable... "
            return $flag
        }
        log "Page [ixNet getAttr $trafficStatsView -currentPage] :: Number of rows $indexMax"

        for {set index 0} {$index < $indexMax} {incr index} {
            set thisRowValues [lindex [ixNet getAttribute $trafficStatsView -rowValues] $index]
            set columnCaptions [ixNet getAttribute $trafficStatsView -columnCaptions]
            set RxFrames [lindex [lindex $thisRowValues 0] [lsearch -regexp $columnCaptions {Rx Frames}]]
            set TxFrames [lindex [lindex $thisRowValues 0] [lsearch -regexp $columnCaptions {Tx Frames}]]
            if {$RxFrames == "" || $TxFrames == ""} {
                log "Error while checking TxFrames, RxFrames: blank stats received"
                return 1
            }

            if {$mcastMultiplier > 1} {
                set TxFrames [expr $TxFrames * $mcastMultiplier]
            }

            set minRxFrames [expr ($TxFrames - ($TxFrames * $tolerance)/100)]
            set maxRxFrames [expr ($TxFrames + ($TxFrames * $tolerance)/100)]

            if {($TxFrames <= 0) || ($RxFrames <= 0) || ($RxFrames < $minRxFrames) || ($RxFrames > $maxRxFrames)} {
                log "Stats are not proper for Page: [ixNet getAttr $trafficStatsView -currentPage] Row: $index "
                return $flag
            }
            log "Page: [ixNet getAttr $trafficStatsView -currentPage] : \
                    Row: $index  (Tx: $TxFrames Rx: $RxFrames) Traffic Stats correct..."
        }
        log "Page: [ixNet getAttr $trafficStatsView -currentPage] Traffic Stats Verification completed...."
    }

    set flag 0
    return $flag
}
