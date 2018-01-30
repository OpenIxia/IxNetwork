#source "trafficItemCheckChassi.tcl"

global startEventName endEventName
set j 0
set b 25
for {set i 1} {$i<6} {incr i} {
    set startEventName(ospfEnableRR$i) "(OSPF) Router 187.119.0.1: Route Range $b.$b.$b.1/24/1000 - Enable"
    set startEventName(ospfV3EnableRR$i) "(OSPFv3) Router 187.119.0.1: Route Range $b:0:0:0:0:0:0:1/64/1000 - Enable"
    set startEventName(bgpEnableRR$i) "(BGP) Peer 21.21.21.2: Route Range $b.$b.$b.$b/32/1000 - Enable"
    set startEventName(bgpVpnEnableRR$i) "(BGP) Peer 1.1.1.1: Route Range $b.$b.$b.1/24/1000 - Enable"
    set startEventName(bgpMplsEnableRR$i) "(BGP) Peer 21.21.21.2: Route Range $b.$b.$b.$b/32/1 - Enable"
    set startEventName(isisEnableRR$i) "(ISIS) System ID BB 77 00 01 00 00 : Route Range $b.$b.$b.1/32/1 - Enable"
    set startEventName(isisv6EnableRR$i) "(ISIS) System ID BB 77 00 01 00 00 : Route Range $b:0:0:0:0:0:0:1/64/1 - Enable"
    set startEventName(eigrpEnableRR$i) "(EIGRP) Host 128.226.0.1: Route Range $b.$b.$b.1/24/1 - Enable"
    set startEventName(eigrpv6EnableRR$i) "(EIGRP) Host 218.150.0.1: Route Range $b:0:0:0:0:0:0:1/64/1 - Enable"
    set startEventName(pimv4EnableGR$i) "(PIM-SM/SSM) Router 218.150.0.1: Group Range 2$b.0.1.0/32/1000 - Enable"
    set startEventName(pimv6EnableGR$i) "(PIM-SM/SSM) Router 17.130.0.1: Group Range FF03:0:0:$j:0:0:0:1/128/1000 - Enable"
    set startEventName(igmpEnableGR$i) "(IGMP) Host 1.1.1.2: Group Range 224.0.0.$j/32/5 - Enable"
    set startEventName(MldEnableGR$i) "(MLD) Host 100:02 - 2: Group Range FF03:0:0:$j:0:0:0:0/128/1000 - Enable"
    set startEventName(oamEnable$i) "(OSPF) Router 187.119.0.1: Route Range $b.$b.$b.1/24/100 - Link Down"
    set startEventName(MstpTopologyChng$i) "protocols.2.BGP.BGP Peers.1.0.RouteRanges.$i: Topology Change"
    set startEventName(ospfDisableRR$i) "(OSPF) Router 187.119.0.1: Route Range $b.$b.$b.1/24/1000 - Disable"
    set startEventName(ospfV3DisableRR$i) "(OSPFv3) Router 187.119.0.1: Route Range $b:0:0:0:0:0:0:1/64/1000 - Disable"
    set startEventName(bgpDisableRR$i) "(BGP) Peer 21.21.21.2: Route Range $b.$b.$b.$b/32/1000 - Disable"
    set startEventName(bgpVpnDisableRR$i) "(BGP) Peer 1.1.1.1: Route Range $b.$b.$b.1/24/1000 - Disable"
    set startEventName(bgpMplsDisableRR$i) "(BGP) Peer 21.21.21.2: Route Range $b.$b.$b.$b/32/1 - Disable"
    set startEventName(isisDisableRR$i) "(ISIS) System ID BB 77 00 01 00 00 : Route Range $b.$b.$b.1/32/1 - Disable"
    set startEventName(isisv6DisableRR$i) "(ISIS) System ID BB 77 00 01 00 00 : Route Range $b:0:0:0:0:0:0:1/64/1 - Disable"
    set startEventName(eigrpDisableRR$i) "(EIGRP) Host 128.226.0.1: Route Range $b.$b.$b.1/24/1 - Disable"
    set startEventName(eigrpv6DisableRR$i) "(EIGRP) Host 218.150.0.1: Route Range $b:0:0:0:0:0:0:1/64/1 - Disable"
    set startEventName(pimv4DisableGR$i) "(PIM-SM/SSM) Router 218.150.0.1: Group Range 2$b.0.1.0/32/1000 - Disable"
    set startEventName(pimv6DisableGR$i) "(PIM-SM/SSM) Router 17.130.0.1: Group Range FF03:0:0:$j:0:0:0:1/128/1000 - Disable"
    set startEventName(igmpDisableGR$i) "(IGMP) Host 1.1.1.2: Group Range 224.0.0.$j/32/5 - Disable"
    set startEventName(MldDisableGR$i) "(MLD) Host 100:02 - 2: Group Range FF03:0:0:$j:0:0:0:0/128/1000 - Disable"
    set startEventName(oamDisable$i) "(OSPF) Router 187.119.0.1: Route Range $b.$b.$b.1/24/100 - Link Up"
    set startEventName(linkUpDown) "Port Link Up/Down"
    incr j
    incr b
}



# Must FIX BUGs ***
set ::BUG508119  0

#############################################################################
# Common procs to be used for set & get attr
#############################################################################

proc matchAttributeValue {object attr expectedVal} {
     set noMatch 1
     set val [ixNet getAtt $object -$attr]
     #log "\t (-$attr)$val : $expectedVal (expected)"
     if {[string tolower $val] != [string tolower $expectedVal]} {
          log "\t -$attr : $val (expected $expectedVal) ---> No Match"
          return $noMatch
     }
     set noMatch 0
     log "\t -$attr : $val (expected $expectedVal) --->Match"
    return $noMatch
}

proc checkAttributeValue {object arr} {
    set isError 1
    array set expectProp $arr

    # parray expectProp
    foreach attr [array names expectProp] {
        set attVal [ixNet getAttr $object -$attr]
        set val $expectProp($attr)
        log "\t attVal = $attVal (-$attr) expectProp = $val"

        # The attr value can be of two types
        # 1) single value 2) list
        set isAttrTypeArray [regexp {Array} [ixNet help $object -$attr]]
        if {!$isAttrTypeArray} {
            # for single value do a string match
            log "-$attr is a single value"
            if {[string tolower $attVal] != [string tolower $val]} {
                log "\t -$attr : $attVal (expected $val) --> did not match!"
                return $isError
            }
        } else {
            # for list value take each value from retrived list
            # and search it in the expected list.
            log "-$attr is list"
            foreach value $attVal {
               if {[lsearch $val $value] < 0} {
                   return $isError
               }
            };# foreach value $attVal
        };# endif {!$isAttrTypeArray}
     } ;# end foreach attr

    set isError 0
    return $isError
}

proc setAndCheckAttributeValue {object attr arr} {
    set isError 1
    array set expectProp $arr
    #parray expectProp
    log "Verifying  $attr ..."
    foreach attrVal [array names expectProp] {
        set retVal $expectProp($attrVal)
        catch {ixNet setAttribute $object -$attr $attrVal}
        catch {ixNet commit}
        set retAttrVal [ixNet getAttr $object -$attr]
        log "\t $attr = $retAttrVal ($attrVal :: $retVal)"
        if {(([string tolower $retAttrVal] != [string tolower $attrVal]) && ($retVal == "y")) || \
            (([string tolower $retAttrVal] == [string tolower $attrVal]) && ($retVal == "n"))} {
            log "\t $attr = $retAttrVal ($attrVal :: $retVal) --> Unexpected"
            return $isError
        }
    }
    set isError 0
    return $isError
}

proc addObjectInConfig {parentObj objName {objConfigList {}}} {
    set isError 1

    set prevLength [llength [ixNet getList $parentObj $objName]]

    set newObject [ixNet add $parentObj $objName]

    foreach {attr attrVal} $objConfigList {
        ixNet setAttr $newObject -$attr $attrVal
    }
    ixNet commit
    set newObject [lindex [ixNet remapIds $newObject] 0]

    set curLength [llength [ixNet getList $parentObj $objName]]
    log "Prev #$objName = $prevLength ~ Current #$objName = $curLength"
    if {$curLength != [expr $prevLength + 1]} {
        return $isError
    }
    set isError 0
    return $isError
}

proc removeObjectInConfig {parentObj objName {objMatchList {}}} {
    set isError 1

    set gotTheObjToRemove 0
    set getObjList [ixNet getList $parentObj $objName]
    set prevLength [llength $getObjList]

    if {$prevLength == 0} {
        log "No $objName to remove.."
        return $isError
    }

    foreach getObject $getObjList {
        if {[checkAttributeValue $getObject $objMatchList] == 0} {
            log "Got the $objName in configuration to remove.."
            set gotTheObjToRemove 1
            break
        }
    }

    if {($gotTheObjToRemove == 1) || ($objMatchList == {})} {
        ixNet remove $getObject
        ixNet commit
    } else {
        log "No mathing $objName found in configuration..."
        return $isError
    }

    set curLength [llength [ixNet getList $parentObj $objName]]
    log "Prev #$objName = $prevLength ~ Current #$objName = $curLength"
    if {$curLength != [expr $prevLength - 1]} {
        return $isError
    }
    set isError 0
    return $isError
}


################################################################################
# General Procs using IxTclHal
################################################################################


#-------------------------------------------------------------------------------
# PROCEDURE  : ixExplorerCheckAttributeValue
# PURPOSE    : To check the IxExplorer Attributes
# PARAMETERS : object, array of attr and expectedVal
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc ixExplorerCheckAttributeValue {object arr} {
    set isError 1
    array set expectProp $arr
    #parray expectProp

    foreach attr [array names expectProp] {
       set attVal [$object cget -$attr]
       set val $expectProp($attr)

       log "\t attVal = $attVal (-$attr) expectProp = $val"
       if {[string tolower $attVal] != [string tolower $val]} {
           log "\t -$attr : $attVal (expected $val) --> did not match!"
           return $isError
       }
    }

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : connectChassis
# PURPOSE    : To connect to the Chassis and reserve ports
# PARAMETERS : chassisIp, card and port
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc ixExplorerConnectChassis {chassisIp card port} {

    set error 1

    if {[ixInitialize $chassisIp]} {
        log "Could not connect to Chassis $chassisIp !!!"
        return $error
    }
    log "Connect to the Chassis $chassisIp successfully !!!"

    chassis get $chassisIp
    set chassisId [chassis cget -id]
    port get $chassisId $card $port
    set loginName [port cget -owner]

    if {[ixLogin $loginName]} {
        log "Could not login in the Chassis $chassisIp !!!"
        return $error
    }
    log "Log in successfully with user: $loginName !!!"

    if {[chassis refresh $chassisId]} {
        log "Could not refresh Chassis $chassisIp"
        return $error
    }
    log "Refreshed the Chassis $chassisIp !!!"

    set error 0
    return $error
}

#-------------------------------------------------------------------------------
# PROCEDURE  : disconnectChassis
# PURPOSE    : Disconnect from the Chassis
# PARAMETERS : chassisIp
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc ixExplorerDisconnectChassis {chassisIp} {

   set error 1

   if {[ixDisconnectFromChassis $chassisIp]} {
      log "Could not disconnect from Chassis $chassisIp"
      return $error
   }
   log "Successfully disconnected from the Chassis $chassisIp !!!"

   set error 0
   return $error
}

################################################################################

proc checkHighLevelSteamCountForAllTrafficItem {expectedTIcount hlsCountList} {
    set isError 1
    set traffic [ixNet getRoot]/traffic
    set trafficItemList [ixNet getList $traffic trafficItem]
    set obtainedTICount [llength $trafficItemList]

    log "Traffic Item Count $obtainedTICount (Expected : $expectedTIcount)"
    if {$obtainedTICount != $expectedTIcount} {
        log "------> MISMATCH"
        return $isError
    }

    foreach {trafficItemIndex expectedHLSteamCount} $hlsCountList {
        set trafficItem [lindex $trafficItemList $trafficItemIndex]
        set HLStreamList [ixNet getList $trafficItem highLevelStream]
        set obtainedHLSteamCount [llength $HLStreamList]

        log "TI[expr ($trafficItemIndex +1)] :: High Level Stream Item Count \
            $obtainedHLSteamCount (Expected : $expectedHLSteamCount)"
        if {$obtainedHLSteamCount != $expectedHLSteamCount} {
            log "------> MISMATCH"
            return $isError
        }
    }
    set isError 0
    return $isError
}



################################################################################
# Procedure : generateApplyTraffic
# Purpose   : To Generate and Apply Traffic
# Parameters    : None
# Return    : (Bool) 0 - Applied Traffic 1 - Failed to Apply Traffic
################################################################################
proc generateApplyTraffic {} {
    set flag 1
    set traffic [ixNet getRoot]/traffic
    # Enable refreshLearnedInfoBeforeApply for MPLS Traffic
    if {[setAndCheckAttributeValue $traffic refreshLearnedInfoBeforeApply {"true" y}] == 1} {
        ixNetCleanUp
        return $FAILED
    }

    # Apply Traffic
    log "Applying the traffic ...."
    set applyTraffic [catch {::ixNet exec apply $traffic} errMsg]
    if {[::ixNet exec apply $traffic] != "::ixNet::OK"} {
        log "Not able to apply the traffic.."
        log "[ixNet getAttr $traffic -errors]"
        return $flag
    }

    set count 0
    log "Checking Traffic State ..."
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
proc startTraffic {traffic} {
    set flag 1
    log "Starting the traffic..."


    set startTraffic [catch {::ixNet exec startStatelessTraffic $traffic} \
                                errMsg]
    if {$startTraffic} {
        # catch returned 1 error in starting traffic.
        log "$errMsg"
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

proc stopTraffic {traffic} {
    set flag 1
    log "Stopping the traffic...."

    set stopTraffic [catch {::ixNet exec stopStatelessTraffic $traffic} errMsg]

    if {$stopTraffic} {
        log "$errMsg"
        return $flag
    }
    after 10000

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

################################################################################
#Procedure  : disableTracking
#Purpose    : To disable all tracking option viz. Ingress/Egress/Latency Bin
#Parameters : trafficItemName
#Return     : (Bool) 0 - Pass 1 - Fail
################################################################################
proc disableTracking {trafficItemName} {
    set error 1

    set top [ixNet getRoot]
    set traffic $top/traffic
    set trafficItemList [ixNet getList $traffic trafficItem]
    set numTrafficItems [llength $trafficItemList]

    for {set index 0} {$index < $numTrafficItems} {incr index} {
        set trafficItem [lindex $trafficItemList $index]
        if {[ixNet getAttr $trafficItem -name] == $trafficItemName} {
            if {[setAndCheckAttributeValue $trafficItem/tracking trackBy {"" y}] == 1} {
                log "Not able to disable Ingress Tracking !!!"
                return $error
            }

            if {[setAndCheckAttributeValue $trafficItem/tracking/egress enabled {"False" y}] == 1} {
                log "Not able to disable Egress Tracking !!!"
                return $error
            }

            if {[setAndCheckAttributeValue $trafficItem/tracking/latencyBin enabled {"False" y}] == 1} {
                log "Not able to disable Latency Bin Tracking !!!"
                return $error
            }

            break
        }
    }

    set error 0
    return $error
}

################################################################################
# START :: DO NOT USE FOLLOWING PROCs DIRECTLY
################################################################################

proc createView {caption type} {
   set view [ixNet add [ixNet getRoot]statistics view]
   ixNet setAttribute $view -caption $caption
   ixNet setAttribute $view -type $type
   ixNet commit
   set view [lindex [ixNet remapIds $view] end]
   return $view
}

proc enableView {view} {
    ixNet setAttribute $view -enabled true
    ixNet commit
    ixNet setAttr $view -visible true
    ixNet commit
}

proc enableAllStatistics {view {usrStatsList "All"}} {

    # Reset All Stats First
    foreach {statistic} [ixNet getList $view statistic] {
        ixNet setAttribute $statistic -enabled false
    }

    foreach {statistic} [ixNet getList $view statistic] {
        if {$usrStatsList == "All"} {
            #log "Enabling stat :: [ixNet getAttribute $statistic -caption]"
            ixNet setAttribute $statistic -enabled true
        }
        foreach stat $usrStatsList {
            if {[ixNet getAttribute $statistic -caption] == $stat} {
                #log "Enabling stat :: [ixNet getAttribute $statistic -caption]"
                ixNet setAttribute $statistic -enabled true
            }
        }
    }
    ixNet commit
}


proc enableAllFilters {view availableFilters setupFilter setupFilterId {usrFilterSetList "All"}} {
    set isError 1
    set filters [ixNet getList ${view} $availableFilters]
    log $filters
    set filters2set {}
    # Enable All Filter (default)
    if {$usrFilterSetList == "All"} {
        ixNet setAttribute ${view}/$setupFilter -$setupFilterId $filters
    } else {
        # Enable selected Filters (Usr Specification)
        foreach usrFilterSet $usrFilterSetList {
          log "enableAllFilters usrFilterSet == $usrFilterSet"
            foreach filter $filters {
               log "enableAllFilters filter == $filter"
                set matchListLen 0
                set matchFound 0
                foreach {attr attrVal} $usrFilterSet {
                    log "enableAllFilters attr = $attr attrVal == $attrVal"
                    incr matchListLen
                    if {[ixNet getAttr $filter -$attr] == $attrVal} {
                        incr matchFound
                    }
                }
                if {$matchFound > 0} {
                    if {$setupFilterId == "trafficItemFilterId"} {
                         switch $setupFilter {
                              "layer23TrafficFlowFilter" -
                              "layer23TrafficFlowDetectiveFilter" {
                                   set filters2set $filter
                                   log "setting single filter $filters2set"
                              }
                              default {
                                   lappend filters2set $filter
                                   log "setting filter list $filters2set"
                              }
                         }
                    } else {
                         lappend filters2set $filter
                    }
                }
            }
        }

        if {$filters2set == {}} {
            log "filters2set $filters2set is empty, No filter selected to associate $setupFilterId for ${view}/$setupFilter"
            return $isError
        }

        #log "${view}/$setupFilter/$setupFilterId set to $filters2set"
        ixNet setAttribute ${view}/$setupFilter -$setupFilterId $filters2set
    }
    ixNet commit

    #log "${view}/$setupFilter/$setupFilterId set to [ixNet getAttribute ${view}/$setupFilter -$setupFilterId]"

    set isError 0
    return $isError
}

proc resetAdditionalFilter {view setupFilter filterTypeList} {
    set isError 1
    foreach filterType $filterTypeList {
        if {[removeObjectInConfig ${view}/$setupFilter $filterType ] == 1} {
            log "Failed to remove $filterType "
        }
    }
    set isError 0
    return $isError
}

proc enableAdditionalFilter {view filterType availableFilters setupFilter additionalFilterSetList} {
    set isError 1

    foreach additionalFilterSet $additionalFilterSetList {
        set isObjRefFoundForId 0
        set configList {}

        foreach {attr attrVal} $additionalFilterSet {
            if {($attr == "trackingFilterId") || ($attr == "statisticFilterId") || ($attr == "sortByStatisticId")} {
                foreach {filter} [ixNet getList ${view} $availableFilters] {
                    log "---- $filter"
                    if {(($filterType == "trackingFilter") || ($filterType == "enumerationFilter")) \
                            && ($attr == "trackingFilterId") && (([ixNet getAttr $filter -name] == $attrVal))} {
                        log "Adding Tracking filter -*- $filter"
                        incr isObjRefFoundForId
                        append configList $attr " " [list $filter] " "
                        break
                    }

                    if {(($filterType == "allFlowsFilter") || ($filterType == "liveFlowsFilter")) \
                            && ($attr == "sortByStatisticId") && ([ixNet getAttr $filter -caption] == $attrVal)} {
                        log "Adding Flow Detective filter -*- $filter"
                        incr isObjRefFoundForId
                        append configList $attr " " [list $filter] " "
                        break
                    }

                    if {($filterType == "statisticFilter") && ($attr == "statisticFilterId") \
                                && ([ixNet getAttr $filter -caption] == $attrVal)} {
                        log "Adding Statistics filter -*- $filter"
                        incr isObjRefFoundForId
                        append configList $attr " " [list $filter] " "
                        break
                    }
                }
            } else {
                append configList $attr " " $attrVal " "
            }
        }

        log "=============== $configList"
        if {(($filterType == "allFlowsFilter") || ($filterType == "liveFlowsFilter") || \
                    ($filterType == "deadFlowsFilter"))} {
            foreach {attr attrVal} $configList {
                log "attr = $attr attrVal = $attrVal"
                log "setAndCheckAttributeValue ${view}/$setupFilter/$filterType $attr [subst {$attrVal "y"}]"
                if {[setAndCheckAttributeValue ${view}/$setupFilter/$filterType \
                                               $attr                            \
                                               [list $attrVal "y"]] == 1} {
                    return $isError
                }
            }
        } else {
            if {[addObjectInConfig ${view}/$setupFilter $filterType $configList] == 1} {
                log "Failed to set Additional $filterType :: $additionalFilterSet"
                return $isError
            }
        }
        log "Additional $filterType set :: $additionalFilterSet"
    }

    log "All additional filter specifications are set successfully"
    set isError 0
    return $isError
}


################################################################################
# STOP :: DO NOT USE ABOVE PROCs DIRECTLY
################################################################################

################################################################################
# Design Statistics View Procedures
################################################################################


#-------------------------------------------------------------------------------
# PROCEDURE  : designL23ProtocolPortStatisticView
# PURPOSE    : Design Custom View of type L23TrafficPortStatistic
# PARAMETERS :  -
#               -
#               -
#               - list of {}
#
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
#       set viewCaption "CustomTCLView-layer23TrafficPort-100"
#       set usrStatsList {"AAA" "BBB" "CCC"}
#       designL23ProtocolPortStatisticView "PP-allFilters" "All" $usrStatsList
#       ----
#       set usrFilterSetList {{portFilterIds {{name "xm2-8/Card2/Port12"}}}}
#       designL23ProtocolPortStatisticView "PP-allTIseclectedPorts" $usrFilterSetList $usrStatsList
#-------------------------------------------------------------------------------

proc designL23ProtocolPortStatisticView {viewCaption {usrFilterSetList "All"} \
                            {usrStatsList "All"} {viewConfigList {}} {reUseSV 0}} {
    set isError 1

    if {$reUseSV == 0} {
        set view [createView $viewCaption layer23ProtocolPort]
    } else {
        set viewList [ixNet getList [ixNet getRoot]/statistics view]
        set indexOfSV [lsearch -regexp $viewList $viewCaption]
        set view [lindex $viewList $indexOfSV]
    }


    # Configure attributes/parameters directly under this view
    foreach {attr attrVal} $viewConfigList {
        if {[setAndCheckAttributeValue $view $attr [subst {$attrVal "y"}]] == 1} {
            return $isError
        }
    }

    # Enable All Filters
    if {$usrFilterSetList == "All"} {
        enableAllFilters $view availablePortFilter layer23ProtocolPortFilter portFilterIds
    } else {
        # Enable User Specified Filters
        set portFilterIdsConfigured 0
        foreach usrFilterSet $usrFilterSetList {
            foreach {filterIdType filterSetList} $usrFilterSet {
                if {$filterIdType == "portFilterIds"} {
                    set portFilterIdsConfigured 1
                    enableAllFilters $view availablePortFilter layer23ProtocolPortFilter portFilterIds $filterSetList
                }
            }
        }

        if {$portFilterIdsConfigured == 0} {
            log "Incorrect User Filter Specification !!!"
            return $isError
        }
    }


    if {$usrStatsList == "All"} {
        # Enable All Statistics
        enableAllStatistics $view
    } else {
        # Enable User Specified Statistics
        enableAllStatistics $view $usrStatsList
    }

    # Enable
    enableView $view

    after 2000

    # Refresh View
    ixNet exec refresh $view

    set isError 0
    return $isError
}

#-------------------------------------------------------------------------------
# PROCEDURE  : designL23TrafficPortStatisticView
# PURPOSE    : Design Custom View of type L23TrafficPortStatistic
# PARAMETERS :  -
#               -
#               -
#               - list of {}
#
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
#       set viewCaption "CustomTCLView-layer23TrafficPort-100"
#       set usrStatsList {"Tx Frames" "Rx Frames" "Loss %"}
#       designL23TrafficPortStatisticView "TP-allFilters" "All" $usrStatsList
#       ----
#       set usrFilterSetList {{portFilterIds {{name "xm2-8/Card2/Port12"}}}}
#       designL23TrafficPortStatisticView "TP-allTIseclectedPorts" $usrFilterSetList $usrStatsList
#-------------------------------------------------------------------------------

proc designL23TrafficPortStatisticView {viewCaption {usrFilterSetList "All"} \
                                {usrStatsList "all"} {viewConfigList {}} {reUseSV 0}} {
    set isError 1

    if {$reUseSV == 0} {
        set view [createView $viewCaption layer23TrafficPort]
    } else {
        set viewList [ixNet getList [ixNet getRoot]/statistics view]
        set indexOfSV [lsearch -regexp $viewList $viewCaption]
        set view [lindex $viewList $indexOfSV]
    }


    # Configure attributes/parameters directly under this view
    foreach {attr attrVal} $viewConfigList {
        if {[setAndCheckAttributeValue $view $attr [subst {$attrVal "y"}]] == 1} {
            return $isError
        }
    }

    # Enable All Filters
    if {$usrFilterSetList == "All"} {
        enableAllFilters $view availablePortFilter layer23TrafficPortFilter portFilterIds
    } else {
        # Enable User Specified Filters
        set portFilterIdsConfigured 0
        foreach usrFilterSet $usrFilterSetList {
            foreach {filterIdType filterSetList} $usrFilterSet {
                if {$filterIdType == "portFilterIds"} {
                    set portFilterIdsConfigured 1
                    enableAllFilters $view availablePortFilter layer23TrafficPortFilter portFilterIds $filterSetList
                }
            }
        }

        if {$portFilterIdsConfigured == 0} {
            log "Incorrect User Filter Specification !!!"
            return $isError
        }
    }

    if {$usrStatsList == "all"} {
        # Enable All Statistics
        enableAllStatistics $view
    } else {
        # Enable User Specified Statistics
        enableAllStatistics $view $usrStatsList
    }

    # Enable
    enableView $view

    after 2000

    # Refresh View
    ixNet exec refresh $view

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : designL23TrafficItemStatisticView
# PURPOSE    : Design Custom View of type layer23TrafficItem
# PARAMETERS :  -
#               -
#               -
#               - list of {}
#
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
#              designL23TrafficItemStatisticView "AllTI-AllStats"
#              -------
#              set usrFilterSetList {{trafficItemFilterIds {{name "ingressTracking-2"}}}}
#              designL23TrafficItemStatisticView "selectedTI-AllStats" $usrFilterSetList
#              -------
#              set usrFilterSetList {{trafficItemFilterIds {{name "ingressTracking-2"}}}}
#              set usrStatsList {"Tx Frames" "Rx Frames"}
#              designL23TrafficItemStatisticView "selectedTI-selectedStats" $usrFilterSetList $usrStatsList
#-------------------------------------------------------------------------------

proc designL23TrafficItemStatisticView {viewCaption {usrFilterSetList "All"} \
                                {usrStatsList "All"} {viewConfigList {}} {reUseSV 0}} {
    set isError 1

    if {$reUseSV == 0} {
        set view [createView $viewCaption layer23TrafficItem]
    } else {
        set viewList [ixNet getList [ixNet getRoot]/statistics view]
        set indexOfSV [lsearch -regexp $viewList $viewCaption]
        set view [lindex $viewList $indexOfSV]
    }

    # Configure attributes/parameters directly under this view
    foreach {attr attrVal} $viewConfigList {
        if {[setAndCheckAttributeValue $view $attr [subst {$attrVal "y"}]] == 1} {
            return $isError
        }
    }

    log "Enable Filters..."
    # Enable All Filters
    if {$usrFilterSetList == "All"} {
        enableAllFilters $view availableTrafficItemFilter layer23TrafficItemFilter trafficItemFilterIds
    } else {
        # Enable User Specified Filters
        set trafficItemFilterIdConfigured 0
        foreach usrFilterSet $usrFilterSetList {
            foreach {filterIdType filterSetList} $usrFilterSet {
                if {$filterIdType == "trafficItemFilterIds"} {
                    set trafficItemFilterIdConfigured 1
                    enableAllFilters $view availableTrafficItemFilter layer23TrafficItemFilter trafficItemFilterIds $filterSetList
                }
            }
        }

        if {$trafficItemFilterIdConfigured == 0} {
            log "Incorrect User Filter Specification !!!"
            return $isError
        }
    }

    log "Enable Stats..."
    if {$usrStatsList == "All"} {
        # Enable All Statistics
        enableAllStatistics $view
    } else {
        # Enable User Specified Statistics
        enableAllStatistics $view $usrStatsList
    }

    # Enable
    enableView $view

    after 2000

    # Refresh View
    ixNet exec refresh $view

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : designL23TrafficFlowStatisticView
# PURPOSE    : Design Custom View of type layer23TrafficFlow
# PARAMETERS :  -
#               -
#               -
#               - list of {}
#
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
# set chassisIp2 "xm2-8"
# set card2 2
# set port2 12
# set caption "FirstLevelDrilldown_13"
# set ingressTracking "Source/Dest Value Pair"
# set usrFilterSetList [subst {{trafficItemFilterId {{name "ingressTrackingRaw1"}}}\
#                             {portFilterIds {{name "$chassisIp2/Card$card2/Port$port2"}}}}]
# set addFilterList [subst {{enumerationFilter { \
#             {trackingFilterId "Source/Dest Value Pair" sortDirection "ascending"}}}}]
# set usrStatsList {"Tx Frames" "Rx Frames" "Loss %"}
# designL23TrafficFlowStatisticView $caption {} $usrFilterSetList $addFilterList $usrStatsList
#-------------------------------------------------------------------------------

proc designL23TrafficFlowStatisticView {viewCaption fvConfigList usrFilterSetList \
                    additionalFilterSetList {usrStatsList "All"} {viewConfigList {}} {reUseSV 0}} {

    set isError 1
    log "Designing SV with caption :: $viewCaption"
    if {$reUseSV == 0} {
        set view [createView $viewCaption layer23TrafficFlow]
    } else {
        set viewList [ixNet getList [ixNet getRoot]/statistics view]
        set indexOfSV [lsearch -regexp $viewList $viewCaption]
        set view [lindex $viewList $indexOfSV]
    }

    # Configure attributes/parameters directly under this view
    foreach {attr attrVal} $viewConfigList {
        if {[setAndCheckAttributeValue $view $attr [subst {$attrVal "y"}]] == 1} {
            return $isError
        }
    }

    # Configure Attributes/Filters of layer23TrafficFlowFilter
    foreach {attr attrVal} $fvConfigList {
        log "Setting $attr to $attrVal"
        if {[setAndCheckAttributeValue ${view}/layer23TrafficFlowFilter $attr [subst {$attrVal "y"}]] == 1} {
            return $isError
        }
    }

    log "Enable Filters..."
    # Enable User Specified Filters
    set trafficItemFilterIdConfigured 0
    set portFilterIdsConfigured 0
    set sortFilterIdsConfigured 0
    foreach usrFilterSet $usrFilterSetList {
        foreach {filterIdType filterSetList} $usrFilterSet {
            if {$filterIdType == "trafficItemFilterId"} {
                set trafficItemFilterIdConfigured 1
                enableAllFilters $view availableTrafficItemFilter layer23TrafficFlowFilter trafficItemFilterId $filterSetList
            }
            if {$filterIdType == "portFilterIds"} {
                set portFilterIdsConfigured 1
                enableAllFilters $view availablePortFilter layer23TrafficFlowFilter portFilterIds $filterSetList
            }
        }
    }

    if {$trafficItemFilterIdConfigured == 0} {
        log "Incorrect User Filter Specification !!!"
        return $isError
    }

    if {$portFilterIdsConfigured == 0} {
        log "Incorrect User Filter Specification !!!"
        return $isError
    }

    if {$reUseSV == 1} {
        # Reset All Additinal Filters
        resetAdditionalFilter $view layer23TrafficFlowFilter {"trackingFilter" "enumerationFilter"}
    }

    # Setup AdditionalFilters (optional)
    foreach additionalFilterSet $additionalFilterSetList {
        log "Enable Additional Filters..."
        foreach {filterType additionalFilterList} $additionalFilterSet {
            # Both trackingFilter & enumerationFilter selected from availableTrackingFilter List
            if {[enableAdditionalFilter $view $filterType availableTrackingFilter \
                        layer23TrafficFlowFilter $additionalFilterList] == 1} {
                log "Failed to set Additional $filterType :: $additionalFilterList"
                return $isError
            }
        }
    }

    log "Enable Stats..."
    if {$usrStatsList == "All"} {
        # Enable All Statistics
        enableAllStatistics $view
    } else {
        # Enable User Specified Statistics
        enableAllStatistics $view $usrStatsList
    }

    # Enable
    log "Enabling View..."
    enableView $view

    after 2000

    # Refresh View
    ixNet exec refresh $view

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : designL23TrafficFlowDetectiveStatisticView
# PURPOSE    : Design Custom View of type layer23TrafficFlow
# PARAMETERS :  -
#               -
#               -
#               - list of {}
#
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
# set chassisIp2 "xm2-8"
# set card2 2
# set port2 12
# set caption "FlowdetectiveView_1"
# set fdConfigList {deadFlowsThreshold 5 \
#                   flowFilterType allFlows} ; # allFlows, deadFlows, liveFlows
# set usrFilterSetList [subst {{trafficItemFilterId {{name "ingressTrackingRaw1"}}} \
#                       {portFilterIds {{name "$chassisIp2/Card$card2/Port$port2"}}}}]
# AllDeadFlowFilter:
# set addFilterList [subst {{deadFlowsFilter { \
#                     {sortByStatisticId "TotalFrames" numberOfResults "3" sortingCondition "bestPerformers"}}}}]
# AllLiveFlowFilter:
# set addFilterList [subst {{liveFlowsFilter { \
#                     {sortByStatisticId "TotalFrames" numberOfResults "3" sortingCondition "bestPerformers"}}}}]
# AllFlowFilter:
# set addFilterList [subst {{allFlowsFilter { \
#                     {sortByStatisticId "TotalFrames" numberOfResults "3" sortingCondition "bestPerformers"}}}}]
# designL23TrafficFlowDetectiveStatisticView $caption $fdConfigList $usrFilterSetList $addFilterList
#-------------------------------------------------------------------------------

proc designL23TrafficFlowDetectiveStatisticView {viewCaption fdConfigList usrFilterSetList \
                    additionalFilterSetList {usrStatsList "All"} {viewConfigList {}} {reUseSV 0}} {

    set isError 1

    if {$reUseSV == 0} {
        set view [createView $viewCaption layer23TrafficFlowDetective]
    } else {
        set viewList [ixNet getList [ixNet getRoot]/statistics view]
        set indexOfSV [lsearch -regexp $viewList $viewCaption]
        set view [lindex $viewList $indexOfSV]
    }

    # Configure attributes/parameters directly under this view
    foreach {attr attrVal} $viewConfigList {
        if {[setAndCheckAttributeValue $view $attr [subst {$attrVal "y"}]] == 1} {
            return $isError
        }
    }

    # Configure Attributes/Filters of layer23TrafficFlowDetectiveFilter
    foreach {attr attrVal} $fdConfigList {
        log "Setting $attr to $attrVal"
        if {[setAndCheckAttributeValue ${view}/layer23TrafficFlowDetectiveFilter $attr [subst {$attrVal "y"}]] == 1} {
            return $isError
        }

    }

    log "Enable Filters..."
    # Enable User Specified Filters
    set trafficItemFilterIdConfigured 0
    set portFilterIdsConfigured 0
    foreach usrFilterSet $usrFilterSetList {
        foreach {filterIdType filterSetList} $usrFilterSet {
            if {$filterIdType == "trafficItemFilterId"} {
                set trafficItemFilterIdConfigured 1
                enableAllFilters $view availableTrafficItemFilter layer23TrafficFlowDetectiveFilter trafficItemFilterId $filterSetList
            }
            if {$filterIdType == "portFilterIds"} {
                set portFilterIdsConfigured 1
                enableAllFilters $view availablePortFilter layer23TrafficFlowDetectiveFilter portFilterIds $filterSetList
            }
        }
    }

    if {$trafficItemFilterIdConfigured == 0} {
        log "Incorrect User Filter Specification !!!"
        return $isError
    }

    if {$portFilterIdsConfigured == 0} {
        log "Incorrect User Filter Specification !!!"
        return $isError
    }

    # Setup AdditionalFilters (optional)
    foreach additionalFilterSet $additionalFilterSetList {
        log "Enable Additional Filters..."
        foreach {filterType additionalFilterList} $additionalFilterSet {

            if {($filterType == "allFlowsFilter") || ($filterType == "deadFlowsFilter") \
                        || ($filterType == "liveFlowsFilter")} {
                if {[enableAdditionalFilter $view $filterType availableStatisticFilter \
                            layer23TrafficFlowDetectiveFilter $additionalFilterList] == 1} {
                    log "Failed to set Additional $filterType :: $additionalFilterList"
                    return $isError
                }
            }
            if {$filterType == "trackingFilter"} {
                if {[enableAdditionalFilter $view $filterType availableTrackingFilter \
                            layer23TrafficFlowDetectiveFilter $additionalFilterList] == 1} {
                    log "Failed to set Additional $filterType :: $additionalFilterList"
                    return $isError
                }
            }
            if {$filterType == "statisticFilter"} {
                if {[enableAdditionalFilter $view $filterType availableStatisticFilter \
                            layer23TrafficFlowDetectiveFilter $additionalFilterList] == 1} {
                    log "Failed to set Additional $filterType :: $additionalFilterList"
                    return $isError
                }
            }
        }
    }

    log "Enable Stats..."
    if {$usrStatsList == "All"} {
        # Enable All Statistics
        enableAllStatistics $view
    } else {
        # Enable User Specified Statistics
        enableAllStatistics $view $usrStatsList
    }

    # Enable
    enableView $view

    after 2000

    # Refresh View
    ixNet exec refresh $view

    set isError 0
    return $isError
}

#-------------------------------------------------------------------------------
# PROCEDURE  : verifyDesignedStatisticView
# PURPOSE    : Verify Designed Custom View per User Specification
# PARAMETERS :  -
#               - list of {{pageAtribute {{pageAtributeVal1} {pageAtributeVal2}}}}
#
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
# set usrSpecLists {{columnCaptions {{Rx Frames} {Tx Frames} {Loss %} {Tx Port} {Rx Port} {Source/Dest Value Pair}}} \
#                 {matchRowValues {{4.1.1.1-4.1.6.1} \
#                     {4.1.2.1-4.1.7.1} {4.1.3.1-4.1.8.1} \
#                     {4.1.4.1-4.1.9.1} {4.1.5.1-4.1.10.1}}}}
# set caption "My Stat View"
# verifyDesignedStatisticView $caption $usrSpecLists
#-------------------------------------------------------------------------------

proc verifyDesignedStatisticView {viewCaption usrSpecLists} {
    set flag 1
    set statsViewList [ixNet getList [ixNet getRoot]/statistics view]
    set indexOfStats [lsearch -regexp $statsViewList $viewCaption]
    set view [lindex $statsViewList $indexOfStats]
    set viewPage ${view}/page

    # Check the designed View as per specification
    set columnCaptionsChecked 0
    set rowLabelsChecked 0
    foreach usrSpecList $usrSpecLists {
        foreach {attr expcAttrValList} $usrSpecList {
            # Check Column Captions
            if {$attr == "columnCaptions"} {
                if {[llength $expcAttrValList] != [ixNet getAttr $viewPage -columnCount]} {
                    log "Column Captions in Created SV Not Per User Specification!!!"
                    #return $flag
                }
                # Check User Specified Stats are set here
                foreach stats $expcAttrValList {
                    set statFound 0
                    #log "[ixNet getAttr $viewPage -$attr]"
                    foreach columnCaption [ixNet getAttr $viewPage -$attr] {
                        #log "------- $columnCaption ~ $stats"
                        if {$columnCaption == $stats} {
                            set statFound 1
                            break
                        }
                    }
                    if {$statFound == 0} {
                        log "$stats not present as column Captions in Created SV!!!"
                        return $flag
                    }
                }
                set columnCaptionsChecked 1
            }

            # Check Row Levels
            if {$attr == "matchRowValues"} {
                if {[llength $expcAttrValList] != [ixNet getAttr $viewPage -rowCount]} {
                    log "$expcAttrValList "
                    log "Row Labels in Created SV Not Per User Specification!!!"
                    return $flag
                }

                # Check if egress Tracking
                set colCaptions [ixNet getAttribute $viewPage -columnCaptions]
                set eBucketIndex [lsearch -regexp $colCaptions {Egress Tracking}]

                # Check User Specified Stats are set here
                foreach stats $expcAttrValList {
                    set statFound 0
                    #log "[ixNet getAttr $viewPage -rowValues]"
                    foreach rowValue [ixNet getAttr $viewPage -rowValues] {
                        for {set rowIndex 0} {$rowIndex < [llength $rowValue]} {incr rowIndex} {
                            foreach rowLabel [lindex $rowValue $rowIndex] {
                                set stats2match $stats
                                if {$eBucketIndex != -1} {
                                    set stats2match [lindex $stats $rowIndex]
                                }
                                #log "--- $rowLabel ~  $stats2match"
                                if {$rowLabel == $stats2match} {
                                    set statFound 1
                                    break
                                }
                            }
                        }
                    }
                    if {$statFound == 0} {
                        log "$stats not present as row Labels in Created SV!!!"
                        return $flag
                    }
                }
                set rowLabelsChecked 1
            }
        }
    }

    log "columnCaptionsChecked == $columnCaptionsChecked \
        rowValuesChecked == $rowLabelsChecked "

    if {($columnCaptionsChecked == 0) || ($rowLabelsChecked == 0)} {
        log "Created SV not Per User Specification!!!"
        return $flag
    }

    log "Created SV Per User Specification!!!"
    set flag 0
    return $flag
}



################################################################################
# Verify Statistics Procedures
################################################################################

#-------------------------------------------------------------------------------
# PROCEDURE  : TrafficStats
# PURPOSE    : Check Data Plane Port Statistics
# PARAMETERS :  -
#               -
#               -
#               - list of {}
#
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
#               set txPortList [subst {{[ixNet getAttr $vPort1 -name]}}]
#               set rxPortList [subst {{[ixNet getAttr $vPort2 -name]}}]
#               checkAllPortTrafficStats "Data Plane Port Statistics" $txPortList $rxPortList
#-------------------------------------------------------------------------------

proc checkAllPortTrafficStats {viewCaption txPortList rxPortList {tolerance 5} {mcastMultiplier 1}} {

    set flag 1
    set statNames {{Rx Frames} {Tx Frames}}
    set statsViewList [ixNet getList [ixNet getRoot]/statistics view]
    set indexOftrafficStats [lsearch -regexp $statsViewList $viewCaption]
    set trafficStatsView [lindex $statsViewList $indexOftrafficStats]

    log "Refreshing Statistics View ..."
    set isRefreshed [ixNet exec refresh $trafficStatsView]
    after 2000

    log "Checking Statistics View isReady ..."
    set count 0
    while { [ixNet getAttr $trafficStatsView/page -isReady] != true } {
        log "isReady --> [ixNet getAttr $trafficStatsView -isReady]"
        after 1000
        incr count
        if { $count > 60 } {
            log "Waited for 1 min, Statistics View still not ready.. "
            return $flag
        }
    }
    log "Statistics View Ready ..."

    set page ${trafficStatsView}/page
    set pageList [ixNet getAttribute $page -rowValues] ;# first list of all rows in the page
    if {[llength $pageList] <= 0} {
        log "Traffic Stats are not retrievable... "
        return $flag
    }

    foreach stat $statNames {
        set statIndex [lsearch -regexp [ixNet getAttribute $page -columnCaptions] $stat]
        set statName [lindex [ixNet getAttribute $page -columnCaptions] $statIndex]
        for {set pageListIndex 0} {$pageListIndex < [llength $pageList]} {incr pageListIndex} {
            set rowList [lindex $pageList $pageListIndex] ;# second list of 1 ingress and x egress rows
            set cellList [lindex $rowList 0] ;# third list of cell values
            set statValue [lindex $cellList $statIndex]
            set portName [lindex $cellList 0]
            set statValueArray($portName,"$statName") $statValue
        }
    }

    parray statValueArray

    set TxFrames 0
    foreach portList $txPortList {
        set TxFrames [incr TxFrames $statValueArray($portList,"Tx Frames")]
    }

    if {$mcastMultiplier > 1} {
        set TxFrames [expr $TxFrames * $mcastMultiplier]
    }

    set RxFrames 0
    foreach portList $rxPortList {
        set RxFrames [incr RxFrames $statValueArray($portList,"Rx Frames")]
    }

    set minRxFrames [expr ($TxFrames - ($TxFrames * $tolerance)/100)]
    set maxRxFrames [expr ($TxFrames + ($TxFrames * $tolerance)/100)]

    log "(Total Tx: $TxFrames Total Rx: $RxFrames)"
    if {($TxFrames <= 0) || ($RxFrames <= 0) || ($RxFrames < $minRxFrames) || ($RxFrames > $maxRxFrames)} {
        log "Port Stats are not proper... "
        return $flag
    }

    set flag 0
    return $flag
}


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


#-------------------------------------------------------------------------------
# PROCEDURE  : checkAllRowLabels
# PURPOSE    : Check Row label values in SV
# PARAMETERS :  -
#               -
#               -
#               - list of {}
#
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
#               set matchStatListPerRow {{"IPv4 :Source Address" "4.1.1.1" \
#                                       "IPv4 :Destination Address" "4.1.6.1" }}
#               checkAllRowLabels "Flow Statistics" $matchStatListPerRow
#-------------------------------------------------------------------------------

proc checkAllRowLabels {viewCaption matchStatListPerRowList {rowPerPage 50} {pageList "all"}} {

    set flag 1
    set statsViewList [ixNet getList [ixNet getRoot]/statistics view]
    set indexOftrafficStats [lsearch -regexp $statsViewList $viewCaption]
    set trafficStats [lindex $statsViewList $indexOftrafficStats]
    set statsPageView ${trafficStats}/page

if {$::BUG508119 == 0} {
    log "Setting the page size for SV $statsPageView "
    ixNet setAttr $statsPageView -pageSize $rowPerPage
    ixNet commit
    after 2000
}

    log "Refreshing Statistics View ..."
    set isRefreshed [ixNet exec refresh $trafficStats]
    after 2000

    set count 0
    log "Checking Statistics View isReady ..."
    while { [ixNet getAttr $statsPageView -isReady] != true } {
        log "isReady --> [ixNet getAttr $statsPageView -isReady]"
        after 1000
        incr count
        if { $count > 60 } {
            log "Waited for 1 min, Statistics View still not ready.. "
            return $flag
        }
    }
    log "Statistics View Ready ..."

    set pageMax [ixNet getAttr $statsPageView -totalPages]
    log "Actual Number of pages available: $pageMax"

    set pagesToBrowse {}
    for {set page 1} {$page <= $pageMax} {incr page} {
        lappend pagesToBrowse $page
    }

    if {$pageList != "all"} {
        set pagesToBrowse $pageList
    }

    # Verify stats for all the flows
    foreach matchStatListPerRow $matchStatListPerRowList {
        #log "matchStatListPerRow -------- $matchStatListPerRow"
        set alllStatsMatched 0
        set numStatsToBeVerified [expr [llength $matchStatListPerRow] / 2]
        foreach page $pagesToBrowse {
            if {$page > $pageMax} {
                log "Can't browse for $page, max Page available is $pageMax"
                return $flag
            }
            ixNet setAttr $statsPageView -currentPage $page
            ixNet commit
            after 3000

            # check if Stats are ready before verifying them
            set isRefreshed [ixNet exec refresh $trafficStats]
            if {[string equal $isRefreshed "::ixNet::OK"] != 1} {
                log "Traffic Stats are not ready ..."
                return $flag
            }
            log "Traffic Stats are ready ..."

            set indexMax [ixNet getAttribute $statsPageView -rowCount]
            if {$indexMax <= 0} {
                log "Traffic Stats are not retrievable... "
                return $flag
            }
            log "Page [ixNet getAttr $statsPageView -currentPage] :: Number of rows $indexMax"

            for {set index 0} {$index < $indexMax} {incr index} {
                set numStatsMatchedInRow 0
                foreach {statName expectedStatValue} $matchStatListPerRow {
                    set statIndex [lsearch -regexp [ixNet getAttribute $statsPageView -columnCaptions] $statName]

                    if {$statIndex == -1} {
                        log "$statName column not present in stat view [ixNet getAttribute $trafficStats -caption]"
                        return $flag
                    }

                    set thisRowVal [lindex [ixNet getAttribute $statsPageView -rowValues] $index]
                    set statVal [lindex [lindex $thisRowVal 0] $statIndex]

                    log "Page: [ixNet getAttr $statsPageView -currentPage] : Row: $index  -- \
                        $statName: $statVal (expected $expectedStatValue)"

                    if {$statVal != $expectedStatValue} {
                        log "Stats are not proper for Page: [ixNet getAttr $statsPageView -currentPage] \
                            Row: $index "
                        break
                    }
                    incr numStatsMatchedInRow
                    log "Page: [ixNet getAttr $statsPageView -currentPage] : Row: $index  -- \
                        $statName: $statVal (expected $expectedStatValue) Traffic Stats correct..."
                }

                if {$numStatsMatchedInRow == $numStatsToBeVerified} {
                    log "check equality -- $numStatsMatchedInRow == $numStatsToBeVerified"
                    set alllStatsMatched 1
                    break
                }
            }

            if {$alllStatsMatched == 1} {
                break
            }
            log "Page: [ixNet getAttr $statsPageView -currentPage] completed...."
        }

        if {$alllStatsMatched == 0} {
            log "Not All Stats Matched...."
            return $flag
        }
    }

    log "All Stats Matched...."
    set flag 0
    return $flag
}


###############################################################################
# Procedure : checkAllStats
#
# Description: Checks all the Protocol Stats.
#
# Argument(s):
#         viewCaption -
#         matchStatListPerRow     -  List of Stats to be checked.{statName statValue tolerance}
#
###############################################################################

proc checkAllStats {viewCaption matchStatListPerRowList {rowPerPage 50} {pageList "all"}} {

    set flag 1
    set statsViewList [ixNet getList [ixNet getRoot]/statistics view]
    set indexOftrafficStats [lsearch -regexp $statsViewList $viewCaption]
    set trafficStats [lindex $statsViewList $indexOftrafficStats]
    set statsPageView ${trafficStats}/page

if {$::BUG508119 == 0} {
    log "Setting the page size for SV $statsPageView "
    ixNet setAttr $statsPageView -pageSize $rowPerPage
    ixNet commit
    after 2000
}

    log "Refreshing Statistics View ..."
    set isRefreshed [ixNet exec refresh $trafficStats]
    after 2000

    set count 0
    log "Checking Statistics View isReady ..."
    while { [ixNet getAttr $statsPageView -isReady] != true } {
        log "isReady --> [ixNet getAttr $statsPageView -isReady]"
        after 1000
        incr count
        if { $count > 60 } {
            log "Waited for 1 min, Statistics View still not ready.. "
            return $flag
        }
    }
    log "Statistics View Ready ..."

    set pageMax [ixNet getAttr $statsPageView -totalPages]
    log "Actual Number of pages available: $pageMax"

    set pagesToBrowse {}
    for {set page 1} {$page <= $pageMax} {incr page} {
        lappend pagesToBrowse $page
    }

    if {$pageList != "all"} {
        set pagesToBrowse $pageList
    }

    # Verify stats for all the flows
    foreach matchStatListPerRow $matchStatListPerRowList {
        #log "matchStatListPerRow -------- $matchStatListPerRow"
        set alllStatsMatched 0
        set numStatsToBeVerified [expr [llength $matchStatListPerRow] / 3]
        foreach page $pagesToBrowse {
            if {$page > $pageMax} {
                log "Can't browse for $page, max Page available is $pageMax"
                return $flag
            }
            ixNet setAttr $statsPageView -currentPage $page
            ixNet commit
            after 3000

            # check if Stats are ready before verifying them
            set isRefreshed [ixNet exec refresh $trafficStats]
            if {[string equal $isRefreshed "::ixNet::OK"] != 1} {
                log "Traffic Stats are not ready ..."
                return $flag
            }
            log "Traffic Stats are ready ..."

            set indexMax [ixNet getAttribute $statsPageView -rowCount]
            if {$indexMax <= 0} {
                log "Traffic Stats are not retrievable... "
                return $flag
            }
            log "Page [ixNet getAttr $statsPageView -currentPage] :: Number of rows $indexMax"

            for {set index 0} {$index < $indexMax} {incr index} {
                set numStatsMatchedInRow 0
                foreach {statName expectedStatValue tolerance} $matchStatListPerRow {
                    #log "[ixNet getAttribute $statsPageView -columnCaptions]"
                    set statIndex [lsearch -regexp [ixNet getAttribute $statsPageView -columnCaptions] $statName]
                    if {$statIndex == -1} {
                        log "$statName column not present in stat view [ixNet getAttribute $trafficStats -caption]"
                        return $flag
                    }

                    set thisRowVal [lindex [ixNet getAttribute $statsPageView -rowValues] $index]
                    set statVal [lindex [lindex $thisRowVal 0] $statIndex]
                    if {$statVal != ""} {
                       if {[string is double $statVal]} {
                          set statVal [expr int ($statVal)]
                       }
                    }
                    if {$tolerance == 0} {
                        if {$statVal != $expectedStatValue} {
                            log "Stats are not proper for Page: [ixNet getAttr $statsPageView -currentPage] \
                                Row: $index "
                            break
                        }
                    } else {
                        set minStatVal [expr ($expectedStatValue - ($expectedStatValue * $tolerance)/100)]
                        set maxStatVal [expr ($expectedStatValue + ($expectedStatValue * $tolerance)/100)]

                        log "$statName - $minStatVal < $statVal < $maxStatVal"
                        if {($statVal <= 0) || ($statVal < $minStatVal) || ($statVal > $maxStatVal) } {
                            log "Stats values crossing tolerance limit.."
                            # Introducing loose binding here as line rate varies over LM
                            if {($statVal <= 0)} {
                                log "Stats are not proper for Page: [ixNet getAttr $statsPageView -currentPage] \
                                    Row: $index "
                                break
                            }
                        }
                    }
                    incr numStatsMatchedInRow
                    log "Page: [ixNet getAttr $statsPageView -currentPage] : Row: $index  -- \
                        $statName: $statVal (expected $expectedStatValue) Traffic Stats correct..."
                }

                if {$numStatsMatchedInRow == $numStatsToBeVerified} {
                    log "check equality -- $numStatsMatchedInRow == $numStatsToBeVerified"
                    set alllStatsMatched 1
                    break
                }
            }

            if {$alllStatsMatched == 1} {
                break
            }
            log "Page: [ixNet getAttr $statsPageView -currentPage] completed...."
        }

        if {$alllStatsMatched == 0} {
            log "Not All Stats Matched...."
            return $flag
        }
    }

    log "All Stats Matched...."
    set flag 0
    return $flag
}
###############################################################################
#       Procedure : checkAllProtocolStats
#
#       Description: Checks all the Protocol Stats.
#
#       Argument(s):
#               portLIst -      Ports on which the sessions has to be checked.
#               stat     -  List of Stats to be checked.
#
###############################################################################
proc checkAllProtocolStats {portLists viewCaption stat {exactMatch 0}} {

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

#-------------------------------------------------------------------------------
# PROCEDURE  : checkEgressViewStats
# PURPOSE    : Check Egress stats in SV
# PARAMETERS :  -
#               -
#               -
#               - list of {}
#
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
#                set caption "EgressTracking"
#                set matchBucketList {{2 629407 15} {5 629407 15}}
#                checkEgressViewStats $caption 15 $matchBucketList
#-------------------------------------------------------------------------------

proc checkEgressViewStats {viewCaption {tolerance 5} {matchEgressBucketList {}}} {
    set flag 1
    set statsViewList [ixNet getList [ixNet getRoot]/statistics view]
    set indexOftrafficStats [lsearch -regexp $statsViewList $viewCaption]
    set trafficStats [lindex $statsViewList $indexOftrafficStats]
    set trafficStatsView ${trafficStats}/page

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

    set pageList [ixNet getAttribute $trafficStatsView -rowValues] ;# first list of all rows in the page
    if {[llength $pageList] <= 0} {
        log "Traffic Stats are not retrievable... "
        return $flag
    }

    set statNames {{Rx Frames} {Tx Frames}}
    set colCaptions [ixNet getAttribute $trafficStatsView -columnCaptions]
    log "colCaptions = $colCaptions"
    foreach stat $statNames {
        set RxIndex [lsearch -regexp $colCaptions {Rx Frames}]
        set TxIndex [lsearch -regexp $colCaptions {Tx Frames}]
        set eBucketIndex [lsearch -regexp $colCaptions {Egress Tracking}]

        for {set pageListIndex 0} {$pageListIndex < [llength $pageList]} {incr pageListIndex} {
            set rowList [lindex $pageList $pageListIndex] ;# second list of 1 ingress and x egress rows
            for {set rowIndex 0} {$rowIndex < [llength $rowList]} {incr rowIndex} {
                set cellList [lindex $rowList $rowIndex] ;# third list of cell values
                if {$rowIndex == 0} {
                    log "Ingress([expr $pageListIndex + 1]) $cellList"
                    set TxFrames [lindex $cellList $TxIndex]
                    set RxFrames [lindex $cellList $RxIndex]
                    set RxFramesList {}
                    set egressBucketList {}
                } else {
                    log "Egress([expr $rowIndex + 1]) $cellList"
                    lappend RxFramesList [lindex $cellList $RxIndex]
                    lappend egressBucketList [lindex $cellList $eBucketIndex]
                }
            }

            log "RxFrames $RxFrames TxFrames $TxFrames "
            set minRxFrames [expr ($TxFrames - ($TxFrames * $tolerance)/100)]
            set maxRxFrames [expr ($TxFrames + ($TxFrames * $tolerance)/100)]
            if {($TxFrames <= 0) || ($RxFrames <= 0) || ($RxFrames < $minRxFrames) || ($RxFrames > $maxRxFrames)} {
                log "Stats are not proper for Page: [ixNet getAttr $trafficStatsView -currentPage] Row: 0"
                return $flag
            }
            log "Page: [ixNet getAttr $trafficStatsView -currentPage] : \
                    Row: 0  (Tx: $TxFrames Rx: $RxFrames) Traffic Stats correct..."

            # Rx main should be sum of the components
            log "RxFramesList = $RxFramesList"
            set sumComponentRx 0
            foreach componentRx $RxFramesList {
                incr sumComponentRx $componentRx
            }

            log "Total RxFrames $RxFrames ~ sumComponentRx $sumComponentRx"
            if {$RxFrames != $sumComponentRx} {
                log "Total RxFrames must equal sumComponentRx"
                return $flag
            }

            # Match Egress Bucket List
            log "egressBucketList = $egressBucketList"
            if {[llength $egressBucketList] != [llength $RxFramesList]} {
                log "#rows under Egress Tracking must equal #rows under RxFrames"
                return $flag
            }

            foreach matchEgressBucket $matchEgressBucketList {
                foreach {bucket expectedStatValue tol} $matchEgressBucket {
                    set isBucketFound 0
                    for {set i 0} {$i < [llength $egressBucketList]} {incr i} {
                        if {[lindex $egressBucketList $i] == $bucket} {
                            set isBucketFound 1
                            set statVal [lindex $RxFramesList $i]
                            if {$tol == 0} {
                                log "Egress bucket $bucket :: $statVal (expected $expectedStatValue)"
                                if {$statVal != $expectedStatValue} {
                                    return $flag
                                }
                            } else {
                                set minStatVal [expr ($expectedStatValue - ($expectedStatValue * $tol)/100)]
                                set maxStatVal [expr ($expectedStatValue + ($expectedStatValue * $tol)/100)]
                                log "Egress bucket $bucket Obtained: $statVal Expected: <$minStatVal, $maxStatVal>"
                                if {($statVal <= 0) || ($statVal < $minStatVal) || ($statVal > $maxStatVal)} {
                                    log "Stats values crossing tolerance limit.."
                                    # Introducing loose binding here as line rate varies over LM
                                    if {($statVal <= 0)} {
                                        return $flag
                                    }
                                }
                            }
                        }
                    }
                    if {$isBucketFound == 0} {
                        log "Egress bucket $bucket not found in created SV"
                        return $flag
                    }
                }
            }
        }
    }

    log "Page: [ixNet getAttr $trafficStatsView -currentPage] Traffic Stats Verification completed...."
    set flag 0
    return $flag
}

#-------------------------------------------------------------------------------
# PROCEDURE   : checkStatisticsSortingOrder
# PURPOSE     : To check if the stats values are comming in the sorted order
#               for a given view
# PARAMETERS  : viewName      - View Caption/view name
#               usrStatsList  - name of the user stat for which values is being
#               isAssending   - isAssending == 0 meaning check assending order,
#                               decending otherwise
#                                          pass the statistics name here
# RETURN VALUE: (boolean) 0 pass 1 fail
#-------------------------------------------------------------------------------
proc checkStatisticsSortingOrder {viewName usrStatsName {isAssending 0}} {

    set flag 1
    set viewList [ixNet getList [ixNet getRoot]/statistics view]
    set view ""

    foreach viewRef $viewList {
        set captionName [ixNet getAttr $viewRef -caption]
        if {[string equal $captionName $viewName]} {
           set view $viewRef
           break
        }
    }

    if {![llength $view]} {
        log "User defined TCL view $viewName do not exists in the view list"
        return $flag
    }

    # Verify designed view as per specification & stats getting fetched
    set statsPageView ${view}/page
    set pageMax [ixNet getAttr $statsPageView -totalPages]
    log "Actual Number of pages available: $pageMax"

    set allRequiredStatval {}
    for {set page 1} {$page <= $pageMax} {incr page} {
        ixNet setAttr $statsPageView -currentPage $page
        ixNet commit
        after 3000

        set isRefreshed [ixNet exec refresh $view]
        if {[string equal $isRefreshed "::ixNet::OK"] != 1} {
            log "[ixNet getAttribute $view -caption] Stats not refreshed ..."
            return $flag
        }
        log "[ixNet getAttribute $view -caption] Stats refreshed ..."

        # Check stats are retrievable from created statistics view
        set indexMax [ixNet getAttribute $statsPageView -rowCount]
        if {$indexMax <= 0} {
            log "[ixNet getAttribute $view -caption] Stats are not retrievable... "
            return $flag
        }

        set allRowValues [ixNet getAttribute $statsPageView -rowValues]
        for {set index 0} {$index < $indexMax} {incr index} {
            set stat [lindex $usrStatsName 0]
            set statIndex [lsearch -regexp [ixNet getAttribute \
                $statsPageView -columnCaptions] $stat]

            if {$statIndex == -1} {
                log "$stat column not present in designed stat view \
                     [ixNet getAttribute $view -caption]"
                return $flag
            }

            set row     [lindex [lindex $allRowValues $index] 0]
            set statVal [lindex $row $statIndex]

            if {($statVal < 0) || ($statVal == " ")} {
                log "[ixNet getAttribute $view -caption] Stats
                     \are not retrievable..."
                return $flag
            }
            lappend allRequiredStatval $statVal
        } ;# for {set index 0} {$index < $indexMax} {incr index}
    } ;#for {set page 1} {$page <= $pageMax} {incr page}

    log "$allRequiredStatval"
    # check assending or decending
    expr {$isAssending ? [set operator "<"] : [set operator ">"]}
    set searchLength [expr [llength $allRequiredStatval] - 1]
    for {set ctr 0} {$ctr < $searchLength} {incr ctr} {
        set val1 [lindex $allRequiredStatval $ctr]
        set val2 [lindex $allRequiredStatval [expr $ctr + 1]]
        log "$val2   ${operator}=      $val1"
        if {[expr $val1 $operator $val2]} {
            log "Rows are not in the sorted order"
            return $flag
        }
    }

    log "Rows are in the sorted order"
    set flag 0
    return $flag
}


################################################################################
# PACKET STRUCTURE VERIFICATION
################################################################################
#-------------------------------------------------------------------------------
# PROCEDURE  : enableAndStartCapture
# PURPOSE    : Enable and Start capture on given ports in argument.
# PARAMETERS : vPorts - List of Vitrual ports on which we have to start capture.
#              args-List of other ports on which we wan to start capture.
#Author      :Darshan T
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail.
#-------------------------------------------------------------------------------


proc enableAndStartCapture {vPorts} {
    # initialize return value
    set PASSED 0
    set FAILED 1

    foreach vPort $vPorts {
        ixNet setAttribute $vPort -rxMode capture
        ixNet setAttribute $vPort/capture -softwareEnabled true
        ixNet setAttribute $vPort/capture -hardwareEnabled true
        ixNet commit
        after 2000
    }

    # capture cleanup
    if {[catch {ixNet exec closeAllTabs} err] == 1} {
        log "Failed to close existing analyser tabs "
    }
    after 2000

    #Start the capture
    log "Start Capturing packets"
    if {[catch {ixNet exec startCapture} err] == 1} {
        log "Failed to start packet capture "
        return $FAILED
    }
    log "Enable and Start Capture Complete Successfully"
    return $PASSED
}



#-------------------------------------------------------------------------------
# PROCEDURE  : verifyCapturedPackets
# PURPOSE    : Verifying expected field value in Captured Packets
# PARAMETERS : chassis -
#              card -
#              port -
#              matchFieldList - list of {startIndex endIndex expectedVal}
#              expPktCnt - {default value 1}
#              packetLengthList - expected packet length (length will be
#              matched). If one has to match between max size and min size
#              this should be [list $min $max]
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc verifyCapturedPackets {chassis card port matchFieldList {expPktCnt 1} \
         {packetLengthList {}}} {

    set isError 1

    log "Initializing through IxTclHal...."
    ixInitialize $chassis
    chassis get  $chassis

    set chassisId [chassis cget -id]
    port get $chassisId $card $port

    set loginName [port cget -owner]
    ixLogin $loginName

    log "Logging in using the $loginName"

    # Retrive captured packets
    captureBuffer get $chassisId $card $port
    set numCapturedPkts [captureBuffer cget -numFrames]

    log "Captured $numCapturedPkts pkts (expected: $expPktCnt)"
    if {$numCapturedPkts < $expPktCnt} {
        return $isError
    }

    set isLengthToBeMatched [llength $packetLengthList]
    captureBuffer get $chassisId $card $port 1 $numCapturedPkts
    for {set f 1} {$f <= $numCapturedPkts} {incr f} {

        after 50
        set a [captureBuffer getframe $f]
        after 50

        set capframe  [captureBuffer cget -frame]
        set frameSize [captureBuffer cget -length]

        set mismatch     0
        set sizeMismatch 0

        if {$isLengthToBeMatched} {
            set expectedMinPktLength [lindex $packetLengthList 0]
            set expectedMaxPktLength [lindex $packetLengthList end]
            if {($frameSize >= $expectedMinPktLength) && \
                ($frameSize <= $expectedMaxPktLength)} {
                set sizeMismatch 0
             } else {
                set sizeMismatch 1
             }
        }


        if {$sizeMismatch == 0} {
            foreach {startIndex endIndex expectedVal} $matchFieldList {
                log "Obtained: [lrange $capframe $startIndex $endIndex] \
                        Expected: $expectedVal"
                if {[lrange $capframe $startIndex $endIndex] != $expectedVal} {
                    set mismatch 1
                    log "Obtained: [lrange $capframe $startIndex $endIndex] \
                        Expected: $expectedVal ---> No Match"
                    break
                }
            }
        } ;# endif sizeMismatch

         if {$mismatch == 0} {
            log "All Field Patterns Matched !!!"
            set isError 0
            return $isError
        }
    } ;# end of swarching in buffer

    if {$mismatch == 1} {
        log "Not all Field Patterns Matched !!!"
        return $isError
    }
}



#--------------------------------------------------------------------------------
# PROCEDURE  : ifUnassignedConnectAgain
# PURPOSE    : check if any port connection got released, if so connects it
#              again
#--------------------------------------------------------------------------------
proc ifUnassignedConnectAgain {} {
    set root [ixNet getRoot]
    set vPorts [ixNet getList $root vport]
    foreach port $vPorts {
        set conn_Info [ixNet getAttr $port  -connectionInfo]
        if [string equal $conn_Info ""] {
            set conn_Status [ixNet exec connectPort $port]
            if {[string equal $conn_Status "::ixNet::OK"] != 1} {
               log "Cannot connect to port"
               ixNetCleanUp
               set flag 1
               return $flag
            }
            ixNet commit
        }
    }
}


#-------------------------------------------------------------------------------
# PROCEDURE   : numberOfPacketCapturedInBuffer
# PURPOSE     : To count the number of the packets in the buffer
# PARAMETERS  : chassis -
#               card    -
#               port    -
# MODEL SCENARIO WHERE IT CAN BE USED:
#              : 1) You expect exactly some number of packets in the buffer
#                2) It is ensured that only those packets are on the buffer and
#                   no other packets are present except those
# RETURN VALUE : number of captured packet
#-------------------------------------------------------------------------------
proc numberOfPacketCapturedInBuffer {chassis card port} {
    log "Initilizing thorugh IxTclHal...."
    ixInitialize $chassis
    chassis get $chassis
    set chassisId [chassis cget -id]

    port get $chassisId $card $port
    set loginName [port cget -owner]
    ixLogin $loginName
    log "Logging in using the $loginName"

    # Retrive captured packets
    captureBuffer get $chassisId $card $port

    set numCapturedPkts [captureBuffer cget -numFrames]
    log "Captured $numCapturedPkts pkts"
    return $numCapturedPkts
}

#--------------------------------------------------------------------------------
# PROCEDURE  : enableCaptureMode
# PURPOSE    : enabling capture mode in the port
# PARAMETERS : vPorts - list of vitual ports
#--------------------------------------------------------------------------------
proc enableCaptureMode {vPorts} {
    set isError 1

    foreach vPort $vPorts {
        ixNet setAttribute $vPort -rxMode capture
        ixNet commit
        if {([ixNet getAttribute $vPort -rxMode] != "captureAndMeasure") && \
            ([ixNet getAttribute $vPort -rxMode] != "capture")} {
            return $isError
        }

        if {[setAndCheckAttributeValue $vPort/capture softwareEnabled {"true" y}] == 1} {
            return $isError
        }
        if {[setAndCheckAttributeValue $vPort/capture hardwareEnabled {"true" y}] == 1} {
            return $isError
        }

        ixNet commit
        after 2000
    }

    # capture cleanup
    if {[catch {ixNet exec closeAllTabs} err] == 1} {
        log "Failed to close existing analyser tabs"
    }

    set isError 0
    return $isError
}

#--------------------------------------------------------------------------------
# PROCEDURE  : enableMeasureMode
# PURPOSE    : enabling Measure mode in the port
# PARAMETERS : vPorts - list of vitual ports
#--------------------------------------------------------------------------------
proc enableMeasureMode {vPorts} {
    set isError 1

    foreach vPort $vPorts {
        ixNet setAttribute $vPort -rxMode measure
        ixNet commit
        if {([ixNet getAttribute $vPort -rxMode] != "captureAndMeasure") && \
            ([ixNet getAttribute $vPort -rxMode] != "measure")} {
            return $isError
        }

        if {[setAndCheckAttributeValue $vPort/capture softwareEnabled {"false" y}] == 1} {
            return $isError
        }
        if {[setAndCheckAttributeValue $vPort/capture hardwareEnabled {"false" y}] == 1} {
            return $isError
        }

        ixNet commit
        after 2000
    }

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : ReturnTimestamp
# PURPOSE    : returns the timestamp of the captured packets
# PARAMETERS : chassis -
#              card -
#              port -
#              matchFieldList - list of {startIndex endIndex expectedVal}
#              expPktCnt - {default value 1}
# RETURN     : timeStamp
#-------------------------------------------------------------------------------

proc ReturnTimestamp {chassis card port matchFieldList {expPktCnt 1}} {
    set isError 1

    log "Initializing through IxTclHal...."
    ixInitialize $chassis
    chassis get $chassis
    set chassisId [chassis cget -id]

    port get $chassisId $card $port
    set loginName [port cget -owner]
    ixLogin $loginName
    log "Logging in using the $loginName"

    # Retrieve captured packets
    captureBuffer get $chassisId $card $port

    set numCapturedPkts [captureBuffer cget -numFrames]
    log "Captured $numCapturedPkts pkts (expected: $expPktCnt)"
    if {$numCapturedPkts < $expPktCnt} {
        return $isError
    }
    captureBuffer get $chassisId $card $port 1 $numCapturedPkts
    for {set f 1} {$f <= $numCapturedPkts} {incr f} {
        after 50
        set a [captureBuffer getframe $f]
        after 50
        set capframe [captureBuffer cget -frame]
        log "capframe = $capframe"
        set mismatch 0
        foreach {startIndex endIndex expectedVal} $matchFieldList {
            log "Obtained: [lrange $capframe $startIndex $endIndex] \
                        Expected: $expectedVal"
            if {[lrange $capframe $startIndex $endIndex] != $expectedVal} {
                set mismatch 1
                log "Obtained: [lrange $capframe $startIndex $endIndex] \
                        Expected: $expectedVal ---> No Match"
                break
            }
        }
        if {$mismatch == 0} {
            log "All Field Patterns Matched !!!"
            set timeStamp [captureBuffer cget -timestamp]
            return $timeStamp

        }
    }
    if {$mismatch == 1} {
        log "Not all Field Patterns Matched !!!"
        return $isError
    }
}



###############################################################################
# Read data from csv file
###############################################################################

#------------------------------------------------------------------------------
# PROCEDURE  : readCsvSnapShotDataFromFile
# PURPOSE    : read the stats from any csv file and return the read fields
#              inform of an array
# PARAMETERS : snapShotCsvPath - entire path to the csv snap shot file
#              outputStatArray - the output array
#              indexField - the field which you want to be the index of the
#                           array
#              statFields - list of stats fields that you want. This is optional
#              When you dont specify this argument it will list all the stats
#              in the array
#-------------------------------------------------------------------------------
proc readCsvSnapShotDataFromFile {snapShotCsvPath outputStatArray \
         {indexField ""} {statFields ""}} {
    set isError 1
    upvar $outputStatArray o_StatArray

    # open the file
    set isFileOpenError [catch {set fp [open $snapShotCsvPath "r"]} errorMsg]
    if {$isFileOpenError} {
        return $isError
    }

    # read the CSV header line
    gets $fp line

    # header line is a comma seperated string. put each header field in a list
    set fieldIndexList {}
    set listOfstatHeaders [split $line ","]

    foreach statName $listOfstatHeaders {
        lappend statHeaders [string trim $statName]
    }

    # get the index of the header fields to pick
    if {[llength $statFields] > 0} {
        foreach stat $statFields {
            set index 0
            foreach hdr $statHeaders {
               if {[string equal $hdr $stat] == 1} {
                   lappend fieldIndexList $index
               }
               incr index
            }
        }
    } else {
        set statHeadersLength [llength $statHeaders]
        for {set j 0} {$j < $statHeadersLength} {incr j} {
            lappend fieldIndexList $j
        }
    }

    # check for the key Index
    set keyIndex -1
    set index 0
    foreach hdr $statHeaders {
        if {[string equal [lindex $hdr 0] $indexField] == 1} {
           set keyIndex $index
           break
        }
        incr index
    }

    if {$keyIndex < 0} {
        set keyIndex 0
    }

    gets $fp line
    while {$line != {}} {
        set myStats ""
        set spaceSeperatedTuple ""

        set elements [split $line ","]
        foreach element $elements {
            append spaceSeperatedTuple [string trim $element]
            append spaceSeperatedTuple " "
        }

        foreach fieldIndex $fieldIndexList {
            append myStats [lindex $spaceSeperatedTuple $fieldIndex]
            append myStats " "
        }

        set o_StatArrayIndex [lindex $spaceSeperatedTuple $keyIndex]
        set o_StatArrayValue $myStats
        set o_StatArray($o_StatArrayIndex) $o_StatArrayValue

        gets $fp line

        unset myStats
        unset spaceSeperatedTuple
    }
    close $fp

    set isError 0
    return $isError
}


#------------------------------------------------------------------------------
# PROCEDURE : copyFileFromIxNetworkClient
# PURPOSE   : copy a file from a remote machine to a local machine
# PARAMETES : remotePathAndFile - absolute path in IxNetwork client side
#             localPathAndFile  - local path in your linux box
# ASSUMPTION: In normal case it will overwrite the file if the file
#             permission is not read only
#------------------------------------------------------------------------------
proc copyFileFromIxNetworkClient {remotePathAndFile localPathAndFile} {
    set isError 0
    set errorMsg {}

    set cmdList {{catch {ixNet exec copyFile                           \
                    [ixNet readFrom $remotePathAndFile -ixNetRelative] \
                    [ixNet writeTo $localPathAndFile] -overwrite}      \
                    errorMsg}
                 {catch {glob $localPathAndFile} errorMsg}}

    foreach cmd $cmdList {
        set isError [eval $cmd]
        if {$isError} {
            log "$errorMsg"
            return $isError
        }
    }
    return $isError
}


proc setAndCheckAttributeValue_Pkt {object attr arr valueType} {
    set isError 1
    array set expectProp $arr

    # parray expectProp
    log "Verifying  $attr ..."

    set DEBUG 1
    if {$DEBUG} {
        set fileId [open "[getTestId].csv" "a+"]
        seek $fileId 0 end
    }

    foreach attrVal [array names expectProp] {
        set retVal $expectProp($attrVal)
        catch {ixNet setAttribute $object -$attr $attrVal}
        catch {ixNet commit}
        set valueFormatIs [ixNet getAttr $object -valueFormat]

        if {[string tolower $valueFormatIs] == "hex"} {
            set retAttrValOb [ixNet getAttr $object -$attr]
            if {[llength  $retAttrValOb] == 0} {
               set fileId1 [open "[getTestId].null.txt" "a+"]
               log $fileId1 "--NULL-- BEGIN --NULL--"
               log $fileId1 "--NULL-- ixNet getAttr $object -$attr --NULL-"
               log $fileId1 "--NULL-- valueType   =  [ixNet getAttr $object -valueType]"
               log $fileId1 "--NULL-- valueFormat =  [ixNet getAttr $object -valueFormat]"
               log $fileId1 "--NULL-- END  --NULL-"
               close $fileId1
            }

            for {set count 0} {$count < [llength $retAttrValOb]} {incr count} {
                set values [lindex $retAttrValOb $count]
                if {$values != 0} {
                    set values [string trimleft $values 0]
                } else {
                    set values 0
                }
                set retAttrVal [lappend retAttrVal $values]
            }
        } else {
            set retAttrVal [ixNet getAttr $object -$attr]
        }



        log "\t $attr = $retAttrVal ($attrVal :: $retVal)"
        if {(([string tolower $retAttrVal] != [string tolower $attrVal])  && \
             ($retVal == "y"))                                            || \
             (([string tolower $retAttrVal] == [string tolower $attrVal]) && \
             ($retVal == "n"))} {
            log "\t $attr = $retAttrVal ($attrVal :: $retVal) --> Unexpected"

            if {$DEBUG} {
                set objName $object
                set type [ixNet getAttr $object -valueFormat]
                set valueType [ixNet getAttr $object -valueType]
                set length    [ixNet getAttr $object -length]
                set attrName $attr
                set attrVal $attrVal
                set attrExpd $retAttrVal
                if {$retVal == "n"} {
                    set reason "should not accept the value but accepted"
                } else {
                    set reason "should accept the value but did not accept"
                }
                log $fileId "$objName,$type,$valueType,$length,$attrName,$attrVal,$attrExpd,Failed,$reason"
                close $fileId
            }
            return [expr 1 - $DEBUG]
        }

        set attributeToChck $attr
        set valueObtainedAftrGet $retAttrVal
        set valueTypeFetch [ixNet getAttr $object -valueType]
        set stepValueFetch [ixNet getAttr $object -stepValue]
        if {($valueType != $valueTypeFetch)} {
            if {($stepValueFetch == "0"                       ||
                 $stepValueFetch == "00:00:00:00:00:00:00:00" ||
                 $stepValueFetch == "00:00:00:00:00:00"       ||
                 $stepValueFetch == "0.0.0.0")                &&
                 ($valueTypeFetch != "increment")} {
                log "Mismatch in valueType"
                if {$DEBUG} {
                    set objName $object
                    set type [ixNet getAttr $object -valueFormat]
                    set valueType [ixNet getAttr $object -valueType]
                    set length    [ixNet getAttr $object -length]
                    set attrName "$attr"
                    set attrVal $attrVal
                    set attrExpd $retAttrVal
                    if {$retVal == "n"} {
                        set reason "should not accept the value but accepted"
                    } else {
                        set reason "should accept the value but did not accept"
                    }
                    log $fileId "$objName,$type,$valueType,$length,$attrName,$attrVal,$attrExpd,Failed,$reason"
                    close $fileId
                } ;# endif $DEBUG
                return [expr 1 - $DEBUG]
            } ;# endif stepValueFetc
        } ;# endif $valueType != $valueTypeFetch
        unset retAttrVal
    } ;# endif foreach

    if {$DEBUG} {
       close $fileId
    }
    set isError 0
    return $isError
}


proc setValue {fieldObj valueType singleValue startValue stepValue \
countValue valueList} {
    ixNet setAttr $fieldObj -valueType $valueType
    ixNet setAttr $fieldObj -singleValue $singleValue
    ixNet setAttr $fieldObj -startValue $startValue
    ixNet setAttr $fieldObj -stepValue $stepValue
    ixNet setAttr $fieldObj -countValue $countValue
    ixNet setAttr $fieldObj -valueList $valueList
    log "valTy: $valueType :: sing: $singleValue :: star: $startValue \
    :: step: $stepValue :: count: $countValue :: valueL: $valueList"
    if { [catch {ixNet commit} err] == 1} {
        return 1
    }
    set valueTypeFetch [ixNet getAttr $fieldObj -valueType]
    set stepValueFetch [ixNet getAttr $fieldObj -stepValue]
    if {($valueType != $valueTypeFetch)} {
        if {($stepValueFetch == "0" || $stepValueFetch == "00:00:00:00:00:00:00:00" || \
        $stepValueFetch == "00:00:00:00:00:00" || $stepValueFetch == "0.0.0.0") && \
        ($valueTypeFetch != "increment")} {
            log "Mismatch in valueType"
            return 1
        }
    }
    return 0
}

proc setAndCheckAttributeValueBool {object attr arr} {
    set isError 1
    array set expectProp $arr
    #parray expectProp
    log "Verifying  $attr ..."
    foreach attrVal [array names expectProp] {
        set retVal $expectProp($attrVal)
        catch {ixNet setAttribute $object -$attr $attrVal}
        catch {ixNet commit}
        set retAttrVal [ixNet getAttr $object -$attr]
        log "\t $attr = $retAttrVal ($attrVal :: $retVal)"
        if {(([string tolower $retAttrVal] != [string tolower $attrVal]) && \
        ($retVal == "y")) || (([string tolower $retAttrVal] == \
        [string tolower $attrVal]) && ($retVal == "n"))} {
            log "\t $attr = $retAttrVal ($attrVal :: $retVal) --> Unexpected"
            return 1
        }
    }
    set isError 0
    return $isError
}

proc checkBooleanAttrFullAndTracking {fieldOneByOne} {
    log "***$fieldOneByOne***"
    if {[setAndCheckAttributeValueBool $fieldOneByOne "trackingEnabled" {"True" y "False" y "23" n "$11" n "hi" n}] == 1} {
        log "Error while setting and checking trackingEnabled field"
        return 1
    }
    log "+++$fieldOneByOne+++"
    if {[setAndCheckAttributeValueBool $fieldOneByOne "fullMesh" {"True" y "False" y "011" n "(8" n "ixia" n}] == 1} {
        log "Error while setting and checking fullMesh field"
        return 1
    }
}

proc checkBooleanAttributes {fieldOneByOne} {
    set autoFieldCheck [ixNet getAttr $fieldOneByOne -auto]
    set readOnlyCheck [ixNet getAttr $fieldOneByOne -readOnly]
    set fieldChoiceCheck [ixNet getAttr $fieldOneByOne -fieldChoice]
    set activeFieldChoiceCheck [ixNet getAttr $fieldOneByOne -activeFieldChoice]
    log "autoFieldCheck = $autoFieldCheck"
    log "readOnlyCheck = $readOnlyCheck"
    log "fieldChoiceCheck = $fieldChoiceCheck"
    log "activeFieldChoiceCheck = $activeFieldChoiceCheck"
    if {[string tolower $fieldChoiceCheck] != true} {
        if {[string tolower $autoFieldCheck] == true && [string tolower \
        $readOnlyCheck] != true} {
            log "####$fieldOneByOne###"
            if {[setAndCheckAttributeValueBool $fieldOneByOne "auto" {"True" y "False" y "1" n "-0" n "aa" n}] == 1} {
                log "Error while setting and checking auto field"
                return 1
            }
            if {[checkBooleanAttrFullAndTracking $fieldOneByOne] == 1} {
                log "Error in setting and checking tracking enabled or fullMesh attribute"
                return 1
            }
        } elseif {[string tolower $autoFieldCheck] != true && [string tolower \
        $readOnlyCheck] != true} {
            if {[checkBooleanAttrFullAndTracking $fieldOneByOne] == 1} {
                log "Error in setting and checking tracking enabled or fullMesh attribute"
                return 1
            }
        } elseif {[string tolower $readOnlyCheck] == true} {
            log "---$fieldOneByOne---"
            if {[setAndCheckAttributeValueBool $fieldOneByOne "trackingEnabled" {"True" y "False" y "$21" n "hihi" n}] == 1} {
                log "Error while setting and checking trackingEnabled field"
                return 1
            }
        }
    } elseif {[string tolower $fieldChoiceCheck] == true} {
        if {[string tolower $autoFieldCheck] == true && [string tolower \
        $readOnlyCheck] != true} {
            log "@@@$fieldOneByOne@@@"
            if {[setAndCheckAttributeValueBool $fieldOneByOne "activeFieldChoice" {"True" y "False" n "23" n "$11" n "hi" n}] == 1} {
                log "Error while setting and checking trackingEnabled field"
                return 1
            }
            log "###$fieldOneByOne###"
            if {[setAndCheckAttributeValueBool $fieldOneByOne "auto" {"True" y "False" y "1" n "-0" n "aa" n}] == 1} {
                log "Error while setting and checking auto field"
                return 1
            }
            if {[checkBooleanAttrFullAndTracking $fieldOneByOne] == 1} {
                log "Error in setting and checking tracking enabled or fullMesh attribute"
                return 1
            }
        } elseif {[string tolower $autoFieldCheck] != true && [string tolower \
        $readOnlyCheck] != true} {
            log "@@@$fieldOneByOne@@@"
            if {[setAndCheckAttributeValueBool $fieldOneByOne "activeFieldChoice" {"True" y "False" n "23" n "$11" n "hi" n}] == 1} {
                log "Error while setting and checking trackingEnabled field"
                return 1
            }
            if {[checkBooleanAttrFullAndTracking $fieldOneByOne] == 1} {
                log "Error in setting and checking tracking enabled or fullMesh attribute"
                return 1
            }
        } elseif {[string tolower $readOnlyCheck] == true} {
            log "---$fieldOneByOne---"
            log "---$fieldOneByOne---"
            if {[setAndCheckAttributeValueBool $fieldOneByOne "activeFieldChoice" {"True" y "False" n "23" n "$11" n "hi" n}] == 1} {
                log "Error while setting and checking trackingEnabled field"
                return 1
          }
            if {[setAndCheckAttributeValueBool $fieldOneByOne "trackingEnabled" {"True" y "False" y "$21" n "hihi" n}] == 1} {
                log "Error while setting and checking trackingEnabled field"
                return 1
            }
        }
    }
}

proc checkReadOnlyField {fieldObj singleValue} {
    ixNet setAttr $fieldObj -valueType singleValue
    ixNet setAttr $fieldObj -singleValue $singleValue
    if { [catch {ixNet commit} err] == 1} {
        return 1
    }
    return 0
}

proc getOutOfBoundaryValue {fieldOneByOne} {
    set fieldOneByOneLength [ixNet getAttr $fieldOneByOne -length]
    set fieldOneByOneFormat [ixNet getAttr $fieldOneByOne -valueFormat]
    log "length is $fieldOneByOneLength"
    log "format is $fieldOneByOneFormat"
    if {$fieldOneByOneLength > 31} {
        set outOfBOundaryValue 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
        return $outOfBOundaryValue
    } elseif {$fieldOneByOneFormat == "decimal"} {
        set resultOf2Power [expr pow(2,$fieldOneByOneLength)]
        set result [regexp {([0-9]+)} $resultOf2Power match \
        outOfBOundaryValue]
        set outOfBOundaryValue [expr $outOfBOundaryValue + 1]
        return $outOfBOundaryValue
    } elseif {$fieldOneByOneFormat == "hex"} {
        set resultOf2Power [expr pow(2,$fieldOneByOneLength)]
        set result [regexp {([0-9]+)} $resultOf2Power match \
        outOfBOundaryValue]
        set outOfBOundaryValue [expr $outOfBOundaryValue + 1]
        set outOfBOundaryValue [format "%0.1x" $outOfBOundaryValue]
        return $outOfBOundaryValue
    }
}


#-------------------------------------------------------------------------------
# PROCEDURE  : startEventScheduler
# PURPOSE    : To run Event Scheduler(ES)
# PARAMETERS : Program Index, Max Time
#              Normally no need to call maxTime arg. This arg doesn't affect
#              your Event Scheduler(ES) time. Your Event Sceduler will run for
#              the duration depending on your no. of iterations and wait
#              time you have given in the config file. If this duration exceeds
#              maxTime = 30 min, this proc will forcefully stop Event Scheduler.
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc startEventScheduler {{progIndex 1} {maxTime 30}} {
    set error 1
    set top [ixNet getRoot]
    set programList [ixNet getList $top/eventScheduler program]
    set program [lindex $programList [expr $progIndex-1]]

    log "Starting Event Scheduler ....."
    if {[ixNet exec start $program] != "::ixNet::OK"} {
        log "Could not start Event Scheduler : Program $progIndex"
        return $error
    }
    log "Successfully started Event Scheduler : Program $progIndex !!!"

    after 5000

    set i 1
    while {[checkAttributeValue $program {running true}] != 1} {
        after 60000
        log "Event Scheduler : Program $progIndex is still running ....."
        log "Time Elapsed: $i min. ..... I will again check the status after 1 min. !!!"
        if {($i == $maxTime) && ([checkAttributeValue $program {running true}] != 1)} {
           if {[ixNet exec stop $program] != "::ixNet::OK"} {
              log "Could not stop Event Scheduler : Program $progIndex"
              return $error
           }
            break
        }
        incr i
    }
    log "Event Scheduler : Program $progIndex is stopped ....."

    set error 0
    return $error
}


##########################################################################################
##########################################################################################






#-------------------------------------------------------------------------------
#PROC for getting CP-DP stats data from traffic/Flow statistics
#-------------------------------------------------------------------------------



proc GetCpDpStats {viewCaption {rowPerPage 50} {columnPerPage 30} {pageList "all"}} {

    set flag 1
    set statNames {{tEvent Name} {tEvent Start Timestamp} {tEvent End Timestamp} \
                   {tDP-above Threshold} {tDP-below Threshold} {Ramp-down Convergence} \
               {Ramp-up Convergence} {Link Up/Down Timestamp} {First TimeStamp} \
               {Last TimeStamp}}

    set statsViewList [ixNet getList [ixNet getRoot]/statistics view]
    set indexOftrafficStats [lsearch -regexp $statsViewList $viewCaption]
    set trafficStats [lindex $statsViewList $indexOftrafficStats]
    set trafficStatsView ${trafficStats}/page
#    ixNet setAttr $trafficStatsView -enabled "True"
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
    set statsdata {}
    # Verify TxFrames and RxFrames for all the flows
    foreach page $pagesToBrowse {
        if {$page > $pageMax} {
            log "Can't browse for $page, max Page available is $pageMax"
            return $flag
        }
        ixNet setAttr $trafficStatsView -currentPage $page
        ixNet commit
        after 10000

        # check if Stats are ready before verifying them
        log "check if Traffic Stats are ready..."
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
        foreach stat $statNames {
            set statIndex [lsearch -regexp [ixNet getAttribute $trafficStatsView -columnCaptions] $stat]
            set statName [lindex [ixNet getAttribute $trafficStatsView -columnCaptions] $statIndex]
            set statValue [lindex [lindex [ixNet getAttribute $trafficStatsView -rowValues] $index] $statIndex]
            set portName [lindex [lindex [ixNet getAttribute $trafficStatsView -rowValues] $index] 0]
            set statValueArray("$portName","$statName") $statValue
        }
    }
  }
  parray statValueArray
  return $statValueArray
 }

#--------------------------------------------------------------------------
# PROC for Clearing and Verifying CP DP stats
#--------------------------------------------------------------------------

proc ClearAndVerifyCpDpStats {viewCaption {TotalFlowCount 50}} {
   set PASSED 0
   set FAILED 1
   log "Clearing CP-DP stats"
   set traffic [ixNet getRoot]/traffic

   if {[ixNet exec clearCPDPStats] != "::ixNet::OK"} {
       log "FAILURE : Error in Clearing CP-DP stats"
       stopTraffic $traffic
       after 10000
       ixNetCleanUp
       return $FAILED
   }
   ixNet commit
   log "Waiting for 5 seconds"
   after 5000
   set expectedStats {}
   #set CPStatsColumnName {{"Event Name" "" 0 "Event Start Timestamp" "" 0 \
   #               "Event End Timestamp" "" 0 "Link Up/Down Timestamp" "" 0}}
   set CPStatsColumnName {{"Event Name" "" 0 "Event Start Timestamp" "" 0 \
               "Event End Timestamp" "" 0}}
   set StartflowCount 0
   while {$StartflowCount < $TotalFlowCount} {
         set expectedStats $CPStatsColumnName
         incr StartflowCount
   }
log "expectedStats-----------------> $expectedStats"
   log "Checking $viewCaption statistics ..."
        if {[checkAllStats $viewCaption $expectedStats] == 1} {
            log "FAILED : Clearing CP DP stats failed"
            ixNetCleanUp
            return $FAILED
        }
    log "SUCCESS :  Clearing CP DP stats"
   return $PASSED
  }








#---------------------------------------------------------------------------
# PROC for Verify CP stats
#---------------------------------------------------------------------------

   proc verifyCpStats {DrillDownStatsName DestEPList expDiffStartEndCpTS ProtocolUsed {flag 0} {FlowStartFrom 1} {Event  ""}} {
       global startEventName endEventName
       set PASSED 0
       set FAILED 1
       set statNameList {{Event Name} {Event Start Timestamp} {Event End Timestamp} \
                         {First TimeStamp} {Last TimeStamp}}
       set statValue [getStatValue $DrillDownStatsName $DestEPList $statNameList]
       log "statValue :: $statValue"

       #-----------------------------------------------------------------------
       # Verification for all the flows
       #-----------------------------------------------------------------------
       set flowCnt [llength $DestEPList]
       set flowStatsOffset 0
       if {$FlowStartFrom > 1} {
          set count1 2
          while {$count1 <= $FlowStartFrom} {
                set flowStatsOffset [expr $flowStatsOffset + 5]
                incr count1
          }
       }

       for {set loop $FlowStartFrom} {$loop<=$flowCnt} {incr loop} {
           set cpEventName [lindex $statValue [expr 0+$flowStatsOffset]]
           set cpStartTS($loop) [lindex $statValue [expr 1+$flowStatsOffset]]
           set cpEndTS($loop) [lindex $statValue [expr 2+$flowStatsOffset]]
           #set cpLinkUpDownTS($loop) [lindex $statValue [expr 3+$flowStatsOffset]]

           if {$ProtocolUsed != "PortLinkUp" && $ProtocolUsed != "PortLinkDown"} {
            log "Start Verifying CP stats for FLOW$loop"
                log "**********************************"
               if {$cpEventName == "" || $cpStartTS($loop) == "" || $cpEndTS($loop) == ""} {
                   log "CP stats are not available"
                   return $FAILED
               }
               log "CP Start TS of Flow$loop : $cpStartTS($loop)"
               log "CP End TS of Flow$loop : $cpEndTS($loop)"
           if {$cpEndTS($loop) >= $cpStartTS($loop)} {
              log "cp End TS of Flow$loop is greater or equal to CP Start TS of Flow$loop"
               } else {
                  log "cp End TS of Flow$loop is lesser than CP Start TS of Flow$loop"
                  return $FAILED
           }
               set obsDiffStartEndTS($loop) [expr $cpEndTS($loop)-$cpStartTS($loop)]
           if {$obsDiffStartEndTS($loop) > $expDiffStartEndCpTS} {
                 log "Difference of CP-Start-TS and CP-End-TS for FLOW$loop is not within limit"
             log "Expected : <$expDiffStartEndCpTS>, Observed : <$obsDiffStartEndTS($loop)>"
                 return $FAILED
            }
                log "Difference of CP-Start-TS and CP-End-TS is within limit for FLOW$loop"

           }
           switch $ProtocolUsed {
                  STPToplogyChangeVlan1 {
                                if {$cpEventName == "(OSPF) Router 192.193.0.1: Route Range 25.25.25.1/24/1 - Topology Change"} {
                                    log "CP Event Name for Changing Bridge Parameter is proper for FLOW$loop"
                                } else {
                                    log "CP Event Name for Changing Bridge Parameter is not proper for FLOW$loop"
                                    log "Expected CP Event Name : <(OSPF) Router 192.193.0.1: Route Range \
                          25.25.25.1/24/1 - Topology Change>, Observed : <$cpEventName>"
                                    return $FAILED
                                }
                  }
                  STPToplogyChangeVlan2 {
                                if {$cpEventName == "(OSPF) Router 192.193.0.2: Route Range 26.26.26.1/24/1 - Topology Change"} {
                                    log "CP Event Name for Changing Bridge Parameter is proper for FLOW$loop"
                                } else {
                                    log "CP Event Name for Changing Bridge Parameter is not proper for FLOW$loop"
                                    log "Expected CP Event Name : <(OSPF) Router 192.193.0.2: Route Range \
                                          26.26.26.1/24/1 - Topology Change>, Observed : <$cpEventName>"
                                    return $FAILED
                                }
                  }
                  STPBgpToplogyChangeMSTDID1 {
                if {$cpEventName == "(BGP) Peer 21.21.21.2: Route Range 25.25.25.1/24/1 - Topology Change"} {
                                    log "CP Event Name for Changing Bridge Parameter is proper for FLOW$loop"
                                } else {
                                    log "CP Event Name for Changing Bridge Parameter is not proper for FLOW$loop"
                                    log "Expected CP Event Name : <(BGP) Peer 21.21.21.2: Route Range \
                      25.25.25.1/24/1 - Topology Change>, Observed : <$cpEventName>"
                                    return $FAILED
                                }
                  }
                  STPBgpToplogyChangeMSTDID2 {
                                if {$cpEventName == "(BGP) Peer 21.21.22.2: Route Range 26.26.26.1/24/1 - Topology Change"} {
                                    log "CP Event Name for Changing Bridge Parameter is proper for FLOW$loop"
                                } else {
                                    log "CP Event Name for Changing Bridge Parameter is not proper for FLOW$loop"
                                    log "Expected CP Event Name : <(BGP) Peer 21.21.22.2: Route Range \
                                          26.26.26.1/24/1 - Topology Change>, Observed : <$cpEventName>"
                                    return $FAILED
                                }
                  }
                  ospfDisableRR {
                                if {$cpEventName == $startEventName(ospfDisableRR$loop)} {
                            log "CP Event Name for Disabling OSPFv2 RR is proper for FLOW$loop"
                        } else {
                            log "CP Event Name for Disabling OSPFv2 RR is not proper for FLOW$loop"
                            log "Expected CP Event Name : <$startEventName(ospfDisableRR$loop)>, Observed : <$cpEventName>"
                            return $FAILED
                    }
                 }
                 ospfEnableRR {
                              if {$cpEventName == $startEventName(ospfEnableRR$loop)} {
                                 log "CP Event Name for Enabling OSPFv2 RR is proper for FLOW$loop"
                              } else {
                                 log "CP Event Name for Enabling OSPFv2 RR is not proper for FLOW$loop"
                                 log "Expected CP Event Name : <$startEventName(ospfEnableRR$loop)>, Observed : <$cpEventName>"
                                 return $FAILED
                              }
                 }
                 ospfV3DisableRR {
                                if {$cpEventName == $startEventName(ospfV3DisableRR$loop)} {
                                    log "CP Event Name for Disabling OSPFv3 RR is proper for FLOW$loop"
                                } else {
                                    log "CP Event Name for Disabling OSPFv3 RR is not proper for FLOW$loop"
                                    log "Expected CP Event Name : <$startEventName(ospfV3DisableRR$loop)>, Observed : <$cpEventName>"
                                    return $FAILED
                                }
                 }
                 ospfV3EnableRR {
                              if {$cpEventName == $startEventName(ospfV3EnableRR$loop)} {
                                 log "CP Event Name for Enabling OSPFv3 RR is proper for FLOW$loop"
                              } else {
                                 log "CP Event Name for Enabling OSPFv3 RR is not proper for FLOW$loop"
                                 log "Expected CP Event Name : <$startEventName(ospfV3EnableRR$loop)>, Observed : <$cpEventName>"
                                 return $FAILED
                              }
                 }
                 bgpDisableRR {
                                if {$cpEventName == $startEventName(bgpDisableRR$loop)} {
                                    log "CP Event Name for Disabling BGP RR is proper for FLOW$loop"
                                } else {
                                    log "CP Event Name for Disabling BGP RR is not proper for FLOW$loop"
                                    log "Expected Start Event Name : <$startEventName(bgpDisableRR$loop)>, Observed : <$cpEventName>"
                                    return $FAILED
                                }
                 }
                 bgpEnableRR {
                              if {$cpEventName == $startEventName(bgpEnableRR$loop)} {
                                 log "CP Event Name for Enabling BGP RR is proper for FLOW$loop"
                              } else {
                                 log "CP End Event Name for Enabling BGP RR is not proper for FLOW$loop"
                                 log "Expected Start Event Name : <$startEventName(bgpEnableRR$loop)>, Observed : <$cpEventName>"
                                 return $FAILED
                              }
                 }
                 bgpVpnDisableRR {
                                if {$cpEventName == $startEventName(bgpVpnDisableRR$loop)} {
                                    log "CP Event Name for Disabling BGP VPN RR is proper for FLOW$loop"
                                } else {
                                    log "CP Event Name for Disabling BGP VPN RR is not proper for FLOW$loop"
                                    log "Expected Start Event Name : <$startEventName(bgpVpnDisableRR$loop)>, Observed : <$cpEventName>"
                                    return $FAILED
                                }
                 }
                 bgpVpnEnableRR {
                              if {$cpEventName == $startEventName(bgpVpnEnableRR$loop)} {
                                 log "CP Event Name for Enabling BGP VPN RR is proper for FLOW$loop"
                              } else {
                                 log "CP Event Name for Enabling BGP VPN RR is not proper for FLOW$loop"
                                 log "Expected Start Event Name : <$startEventName(bgpVpnEnableRR$loop)>, Observed : <$cpEventName>"
                                 return $FAILED
                              }
                 }
                 bgpMplsDisableRR {
                                if {$cpEventName == $startEventName(bgpMplsDisableRR$loop)} {
                                    log "CP Event Name for Disabling BGP MPLS RR is proper for FLOW$loop"
                                } else {
                                    log "CP Event Name for Disabling BGP MPLS RR is not proper for FLOW$loop"
                                    log "Expected CP Event Name : <$startEventName(bgpMplsDisableRR$loop)>, Observed : <$cpEventName>"
                                    return $FAILED
                                }
                 }
                 bgpMplsEnableRR {
                              if {$cpEventName == $startEventName(bgpMplsEnableRR$loop)} {
                                 log "CP Event Name for Enabling BGP MPLS RR is proper for FLOW$loop"
                              } else {
                                 log "CP Event Name for Enabling BGP MPLS RR is not proper for FLOW$loop"
                                 log "Expected Start Event Name : <$startEventName(bgpMplsEnableRR$loop)>, Observed : <$cpEventName>"
                                 return $FAILED
                              }
                 }
                 oamDisable {
                                if {$cpEventName == $startEventName(oamDisable$loop)} {
                                    log "CP Event Name for $Event is proper for FLOW$loop"
                                } else {
                                    log "CP Event Name for $Event is not proper for FLOW$loop"
                                    log "Expected CP Event Name : <$startEventName(oamDisable$loop)>, Observed : <$cpEventName>"
                                   return $FAILED
                                }
                 }
                 oamEnable {
                              if {$cpEventName == $startEventName(oamEnable$loop)} {
                                 log "CP Event Name for $Event is proper for FLOW$loop"
                              } else {
                                 log "CP Event Name for $Event is not proper for FLOW$loop"
                                 log "Expected CP Event Name : <$startEventName(oamEnable$loop)>, Observed : <$cpEventName>"
                                 return $FAILED
                              }
                 }

                 MldDisableGR {
                                if {$cpEventName == $startEventName(MldDisableGR$loop)} {
                                    log "CP Event Name for Disabling Group Range is proper for FLOW$loop"
                                } else {
                                    log "CP Event Name for Disabling Group Range is not proper for FLOW$loop"
                                    log "Expected CP Event Name : <$startEventName(MldDisableGR$loop)>, Observed : <$cpEventName>"
                                    return $FAILED
                                }
                 }
                 MldEnableGR {
                              if {$cpEventName == $startEventName(MldEnableGR$loop)} {
                                 log "CP Event Name for Enabling Group Range is proper for FLOW$loop"
                              } else {
                                 log "CP Event Name for Enabling Group Range is not proper for FLOW$loop"
                                 log "Expected CP Event Name : <$startEventName(MldEnableGR$loop)>, Observed : <$cpEventName>"
                                 return $FAILED
                              }
                 }

                 isisDisableRR {
                                if {$cpEventName == $startEventName(isisDisableRR$loop)} {
                                    log "CP Event Name for Disabling ISIS Route Range is proper for FLOW$loop"
                                } else {
                                    log "CP Event Name for Disabling ISIS Route Range is not proper for FLOW$loop"
                                    log "Expected CP Event Name : <$startEventName(isisDisableRR$loop)>, Observed : <$cpEventName>"
                                    return $FAILED
                                }
                 }
                 isisEnableRR {
                              if {$cpEventName == $startEventName(isisEnableRR$loop)} {
                                 log "CP Event Name for Enabling ISIS Route Range is proper for FLOW$loop"
                              } else {
                                 log "CP Event Name for Enabling ISIS Route Range is not proper for FLOW$loop"
                                 log "Expected CP Event Name : <$startEventName(isisEnableRR$loop)>, Observed : <$cpStartName>"
                                 return $FAILED
                              }
                 }
                 isisv6DisableRR {
                                if {$cpEventName == $startEventName(isisv6DisableRR$loop)} {
                                    log "CP Event Name for Disabling ISIS Route Range is proper for FLOW$loop"
                                } else {
                                    log "CP Event Name for Disabling ISIS Route Range is not proper for FLOW$loop"
                                    log "Expected CP Event Name : <$startEventName(isisv6DisableRR$loop)>, Observed : <$cpEventName>"
                                    return $FAILED
                                }
                 }
                 isisv6EnableRR {
                              if {$cpEventName == $startEventName(isisv6EnableRR$loop)} {
                                 log "CP Event Name for Enabling ISIS Route Range is proper for FLOW$loop"
                              } else {
                                 log "CP Event Name for Enabling ISIS Route Range is not proper for FLOW$loop"
                                 log "Expected CP Event Name : <$startEventName(isisv6EnableRR$loop)>, Observed : <$cpStartName>"
                                 return $FAILED
                              }
                 }

         eigrpDisableRR {
                               if {$cpEventName == $startEventName(eigrpDisableRR$loop)} {
                             log "CP Event Name for Disabling EIGRPv4 RR is proper for FLOW$loop"
                  } else {
                 log "CP Event Name for Disabling EIGRPv4 RR is not proper for FLOW$loop"
                 log "Expected CP Event Name : <$startEventName(eigrpDisableRR$loop)>, Observed : <$cpEventName>"
                 return $FAILED
                      }
         }
         eigrpEnableRR {
                if {$cpEventName == $startEventName(eigrpEnableRR$loop)} {
                 log "CP Event Name for Enabling EIGRPv4 RR is proper for FLOW$loop"
                  } else {
                 log "CP Event Name for Enabling EIGRPv4 RR is not proper for FLOW$loop"
                 log "Expected CP Event Name : <$startEventName(eigrpEnableRR$loop)>, Observed : <$cpEventName>"
                 return $FAILED
                      }
                 }
                 eigrpv6DisableRR {
                               if {$cpEventName == $startEventName(eigrpv6DisableRR$loop)} {
                                 log "CP Event Name for Disabling EIGRPv6 RR is proper for FLOW$loop"
                              } else {
                                 log "CP Event Name for Disabling EIGRPv6 RR is not proper for FLOW$loop"
                                 log "Expected CP Event Name : <$startEventName(eigrpv6DisableRR$loop)>, Observed : <$cpEventName>"
                                 return $FAILED
                              }
                 }
                 eigrpv6EnableRR {
                                if {$cpEventName == $startEventName(eigrpv6EnableRR$loop)} {
                                 log "CP Event Name for Enabling EIGRPv6 RR is proper for FLOW$loop"
                              } else {
                                 log "CP Event Name for Enabling EIGRPv6 RR is not proper for FLOW$loop"
                                 log "Expected CP Event Name : <$startEventName(eigrpv6EnableRR$loop)>, Observed : <$cpEventName>"
                                 return $FAILED
                              }
                 }
                 pimv4DisableGR {
                        if {$cpEventName == $startEventName(pimv4DisableGR$loop)} {
                         log "CP Event Name for Disabling PIMv4 GR is proper for FLOW$loop"
                     } else {
                         log "CP Event Name for Disabling PIMv4 GR is not proper for FLOW$loop"
                         log "Expected CP Event Name : <$startEventName(pimv4DisableGR$loop)>, Observed : <$cpEventName>"
                         return $FAILED
                      }
         }
         pimv4EnableGR {
                        if {$cpEventName == $startEventName(pimv4EnableGR$loop)} {
                         log "CP Event Name for Enabling PIMv4 GR is proper for FLOW$loop"
                     } else {
                         log "CP Event Name for Enabling PIMv4 GR is not proper for FLOW$loop"
                         log "Expected CP Event Name : <$startEventName(pimv4EnableGR$loop)>, Observed : <$cpEventName>"
                         return $FAILED
                         }
                 }
                 pimv6DisableGR {
                                if {$cpEventName == $startEventName(pimv6DisableGR$loop)} {
                                 log "CP Event Name for Disabling PIMv6 GR is proper for FLOW$loop"
                             } else {
                                 log "CP Event Name for Disabling PIMv6 GR is not proper for FLOW$loop"
                                 log "Expected CP Event Name : <$startEventName(pimv6DisableGR$loop)>, Observed : <$cpEventName>"
                                 return $FAILED
                              }
                 }
                 pimv6EnableGR {
                                if {$cpEventName == $startEventName(pimv6EnableGR$loop)} {
                                 log "CP Event Name for Enabling PIMv6 GR is proper for FLOW$loop"
                             } else {
                                 log "CP Event Name for Enabling PIMv6 GR is not proper for FLOW$loop"
                                 log "Expected CP Event Name : <$startEventName(pimv6EnableGR$loop)>, Observed : <$cpEventName>"
                                 return $FAILED
                             }
                 }
                 igmpDisableGR {
                if {$cpEventName == $startEventName(igmpDisableGR$loop)} {
                         log "CP Event Name for Disabling IGMP GR is proper for FLOW$loop"
                     } else {
                         log "CP Event Name for Disabling IGMP GR is not proper for FLOW$loop"
                         log "Expected CP Event Name : <$startEventName(igmpDisableGR$loop)>, Observed : <$cpEventName>"
                         return $FAILED
                      }
         }
         igmpEnableGR {
                        if {$cpEventName == $startEventName(igmpEnableGR$loop)} {
                         log "CP Event Name for Enabling IGMP GR is proper for FLOW$loop"
                     } else {
                         log "CP Event Name for Enabling IGMP GR is not proper for FLOW$loop"
                         log "Expected CP Event Name : <$startEventName(igmpEnableGR$loop)>, Observed : <$cpEventName>"
                         return $FAILED                                   }

         }
                 linkUpDown {
                     if {$cpEventName == $startEventName(linkUpDown)} {
                 log "CP Event Name for link up/down is proper for FLOW$loop"
             } else {
                 log "CP Event Name for link up/down is not proper for FLOW$loop"
                 log "Expected CP Event Name : <$startEventName(ospfDisableRR$loop)>, Observed : <$cpEventName>"
                 return $FAILED
                 }
                 }
                 PortLinkUp {
                lappend retList "tDP-above Threshold" $DpAboveTS($loop) "tDP-below Threshold" \
                                            $DpBelowTS($loop) "Link Up/Down Timestamp" $cpLinkUpDownTS($loop)"
                            return $retList
                 }

                 PortLinkDown {
                             lappend retList "tDP-above Threshold" $DpAboveTS($loop) "tDP-below Threshold" \
                         $DpBelowTS($loop) "Link Up/Down Timestamp" $cpLinkUpDownTS($loop)"
                             return $retList
                 }
         default {
            log "$ProtocolUsed is not match with any case"
            return $FAILED
                 }
           }

           log "End Verifying CP stats for FLOW$loop"
           #Move the offset to read the next flow stats
       incr flowStatsOffset 5
       }
           after 1000
           set lastflow [expr $loop -1]
           if {$flag == "StartTSFirstFlow"} {
               return $cpStartTS(1)
           } else {
               if {$flag == "EndTSLastFlow"} {
                   return $cpEndTS($lastflow)
               } else {
                   if {$flag == 0} {
                       return $PASSED
                   }
               }
           }
   }

#-----------------------------------------------------------------------------------
# PROC for Stopping traffic and Clean up of config
#-----------------------------------------------------------------------------------
proc ixNetStopTrafficAndCleanup {traffic} {
       set PASSED 0
       stopTraffic $traffic
       after 15000
       ixNetCleanUp
       return $PASSED

}

proc verifyChangeInCpStats {ViewCaption DestEPList AllflowCnt {FlowStartFrom 1} {FlowEnd true} {flag 0}} {

       set PASSED 0
       set FAILED 1
       set statNameList {{Event Name} {Event Start Timestamp} {Event End Timestamp}}
       if {$FlowEnd == "true"} {
           set FlowEnd $AllflowCnt
       }
       set statValue1 [getStatValue $ViewCaption $DestEPList $statNameList]

       #-----------------------------------------------------------------------
       # Verification for all the flows
       #-----------------------------------------------------------------------

       set flowStatsOffset 0
       if {$FlowStartFrom > 1} {
          set count1 1
          while {$count1 != $FlowStartFrom} {
                set flowStatsOffset [expr $flowStatsOffset + 10]
                incr count1
          }
       }
       set count2 0
       set count3 0
       for {set loop $FlowStartFrom} {$loop <=$FlowEnd} {incr loop} {
           set count2 0
       set count3 0
           set cpEventNameIn($loop) [lindex $statValue1 [expr 0+$flowStatsOffset]]
           set cpStartTSIn($loop) [lindex $statValue1 [expr 1+$flowStatsOffset]]
           set cpEndTSIn($loop) [lindex $statValue1 [expr 2+$flowStatsOffset]]
           if {$flag == "CheckForBlankStats" } {
               if {$cpEventNameIn($loop) != "{}" || $cpStartTSIn($loop) != "{}" || \
                   $cpEndTSIn($loop) != "{}"} {
                   incr count2
        } else {
           log "SUCCESS : CP stats not available for FLOW$loop without any Event Action"
                   incr count3
                }
        }
           incr flowStatsOffset 3
         }
         if {$count2 > 0} {
             return $FAILED
         }
         if {$count3 > 0} {
             return $PASSED
         }

       log "Waiting for 120 seconds without any Enabling/Disabling of Event"
       after 120000

       set statValue2 [getStatValue $ViewCaption $DestEPList $statNameList]

       #-----------------------------------------------------------------------
       # Verification for all the flows
       #-----------------------------------------------------------------------
       set flowStatsOffset 0
       for {set loop 1} {$loop<=$AllflowCnt} {incr loop} {
           set cpEventNameFinal($loop) [lindex $statValue2 [expr 0+$flowStatsOffset]]
           set cpStartTSFinal($loop) [lindex $statValue2 [expr 1+$flowStatsOffset]]
           set cpEndTSFinal($loop) [lindex $statValue2 [expr 2+$flowStatsOffset]]
           incr flowStatsOffset 3
      }

      for {set loop 1} {$loop<=$AllflowCnt} {incr loop} {
          log "Verifying Change in CP stats for FLOW$loop without any Enabling/Disabling of Event"
          if {$flag == "DpAboveThreshold"} {
          } else {
               if {$flag == 0} {
              if {$cpEventNameIn($loop) != $cpEventNameFinal($loop) || $cpStartTSIn($loop)!= $cpStartTSFinal($loop)\
                 || $cpEndTSIn($loop) != $cpEndTSFinal($loop)} {
                  log "FAILED : Variation found in CP stats without any Event action for Flow$loop"
                  return $FAILED
              }
               }
          }
      }
    log "SUCCESS : No Variation in CP stats without any Event action"
    return $PASSED
}



#---------------------------------------------------------------------------------

proc DesignAndVerifyCPDrillDownStats {trafficItem chassisIp Card Port DestinationIPList {usrStatsList ""} {usrSpecLists ""} {caption ""}} {
    # Traffic Item "Traffic Item 1" having Destination Endpoint tracking in traffic item and
    # Emulating 1st level drill down
    set DestinationEP [list $DestinationIPList]
    set ingressTracking "Dest Endpoint"
    set PASSED 0
    set FAILED 1

    set usrFilterSetList [subst {{trafficItemFilterId {{name "$trafficItem"}}}\
                                {portFilterIds {{name "$chassisIp/$Card/$Port"}}}}]


    set addFilterList [subst {{enumerationFilter { \
                      {trackingFilterId "Dest Endpoint" sortDirection "ascending"}}}}]
    if {$caption == ""} {
        set caption "FirstLevelDrilldown"
    }
    if {$usrStatsList == ""} {
        set usrStatsList {"Tx Frames" "Rx Frames" "Loss %" "Event Name" "Event Start Timestamp" \
                          "Event End Timestamp" "First TimeStamp" "Last TimeStamp" "Dest Endpoint"}
    }
    # Design View
    if {[designL23TrafficFlowStatisticView $caption {} $usrFilterSetList $addFilterList $usrStatsList] == 1} {
        log "Not able to emulate $caption Statistics View..."
        ixNetCleanUp
        return $FAILED
    }
    log "$caption Statistics View Successfully Emulated..."
    # Verify view creation as per user specification
    if {$usrSpecLists == ""} {
        set usrSpecLists [subst {{columnCaptions {{Rx Frames} {Tx Frames} {Loss %} \
                             {Dest Endpoint} {Event Name} {Event Start Timestamp} {Event End Timestamp} \
                 {First TimeStamp} {Last TimeStamp}}} \
                       {matchRowValues $DestinationEP}}]
    }
    log "Verify designed Stats View as per user specification..."
    if {[verifyDesignedStatisticView $caption $usrSpecLists] == 1} {
        log "Not able to emulate $caption Statistics View as per user spec."
        ixNetCleanUp
       return $FAILED
    }
    return $PASSED
}



#############################################################################################


###############################################################################
# Procedure : getStatValue
#
# Description: Get all the Traffic Stats based on caption passed to proc.
#
# Argument(s):
#         viewCaption -
#         matchStatListPerRow     -  List of Stats to be checked.{matchStatName matchStatValue}
#
###############################################################################

proc getStatValue {viewCaption matchStatListPerRow statNameList {rowPerPage 50} {pageList "all"}} {

    set flag 1
    set statsViewList [ixNet getList [ixNet getRoot]/statistics view]
    set indexOftrafficStats [lsearch -regexp $statsViewList $viewCaption]
    set trafficStats [lindex $statsViewList $indexOftrafficStats]
    set statsPageView ${trafficStats}/page

#    ixNet setAttr $statsPageView -enabled "True"
    ixNet setAttr $statsPageView -pageSize $rowPerPage
    ixNet commit

    set pageMax [ixNet getAttr $statsPageView -totalPages]
    log "Actual Number of pages available: $pageMax"

    set pagesToBrowse {}
    for {set page 1} {$page <= $pageMax} {incr page} {
        lappend pagesToBrowse $page
    }

    if {$pageList != "all"} {
        set pagesToBrowse $pageList
    }

    # Verify stats for all the flows
    #log "matchStatListPerRow -------- $matchStatListPerRow"
    set alllStatsFound 0
    set numStatsToBeVerified [expr [llength $matchStatListPerRow] / 3]
    foreach page $pagesToBrowse {
        if {$page > $pageMax} {
            log "Can't browse for $page, max Page available is $pageMax"
            return $flag
        }
        ixNet setAttr $statsPageView -currentPage $page
        ixNet commit
        after 3000

        # check if Stats are ready before verifying them
        set isRefreshed [ixNet exec refresh $trafficStats]
        if {[string equal $isRefreshed "::ixNet::OK"] != 1} {
            log "Traffic Stats are not ready ..."
            return $flag
        }
        log "Traffic Stats are ready ..."

        set indexMax [ixNet getAttribute $statsPageView -rowCount]
        if {$indexMax <= 0} {
            log "Traffic Stats are not retrievable... "
            return $flag
        }
        log "Page [ixNet getAttr $statsPageView -currentPage] :: Number of rows $indexMax"
            foreach {DestinationEndpoint} $matchStatListPerRow {
            #   log "[ixNet getAttribute $statsPageView -columnCaptions]"
                set DestnEndPointIndex [lsearch -regexp [ixNet getAttribute $statsPageView -rowValues] $DestinationEndpoint]
                if {$DestnEndPointIndex == -1} {
                    log "$DestinationEndpoint not present in stat view"
                    return $flag
                }
                set statvalueOfMatchedEPALL [lindex [ixNet getAttribute $statsPageView -rowValues] $DestnEndPointIndex]
                                set statvalueOfMatchedEP [lindex $statvalueOfMatchedEPALL 0]

                        foreach {statName} $statNameList {
                                set statIndex [lsearch -regexp [ixNet getAttribute $statsPageView -columnCaptions] $statName]
                set statval [lindex $statvalueOfMatchedEP $statIndex]
                                lappend returnlist $statval
                                lappend CPDPStatsValueList [subst {$statName $statval}]
                        }

                 }

        }
         # Printing CP-DP stats Value List
         log "CP-DP Stats Per End Point Destination :: $CPDPStatsValueList"
         return $returnlist
    }




#############################################################################################

###############################################################################
# Procedure : getFlowStatValueperPort
#
# Description: Get Specific Flow Stats value based on Rx Port.
#
# Argument(s):
#         viewCaption -
#         matchStatListPerRow     -  List of Stats to be checked.{matchStatName matchStatValue}
#
###############################################################################

proc getFlowStatValueperPort {viewCaption matchStatListPerRow statNameList {rowPerPage 50} {pageList "all"}} {

    set flag 1
    set statsViewList [ixNet getList [ixNet getRoot]/statistics view]
    set indexOftrafficStats [lsearch -regexp $statsViewList $viewCaption]
    set trafficStats [lindex $statsViewList $indexOftrafficStats]
    set statsPageView ${trafficStats}/page

#    ixNet setAttr $statsPageView -enabled "True"
    ixNet setAttr $statsPageView -pageSize $rowPerPage
    ixNet commit

    set pageMax [ixNet getAttr $statsPageView -totalPages]
    log "Actual Number of pages available: $pageMax"

    set pagesToBrowse {}
    for {set page 1} {$page <= $pageMax} {incr page} {
        lappend pagesToBrowse $page
    }

    if {$pageList != "all"} {
        set pagesToBrowse $pageList
    }

    # Verify stats for all the flows
        #log "matchStatListPerRow -------- $matchStatListPerRow"
        set alllStatsFound 0
        set numStatsToBeVerified [expr [llength $matchStatListPerRow] / 3]
        foreach page $pagesToBrowse {
                if {$page > $pageMax} {
                        log "Can't browse for $page, max Page available is $pageMax"
                        return $flag
                }
                ixNet setAttr $statsPageView -currentPage $page
                ixNet commit
                after 3000

                # check if Stats are ready before verifying them
                set isRefreshed [ixNet exec refresh $trafficStats]
                if {[string equal $isRefreshed "::ixNet::OK"] != 1} {
                        log "Traffic Stats are not ready ..."
                        return $flag
                }
                log "Traffic Stats are ready ..."
                set indexMax [ixNet getAttribute $statsPageView -rowCount]
                if {$indexMax <= 0} {
                        log "Traffic Stats are not retrievable... "
                        return $flag
                }
                log "Page [ixNet getAttr $statsPageView -currentPage] :: Number of rows $indexMax"
                set rowValuesperpage [ixNet getAttribute $statsPageView -rowValues]
                lappend tempFlowStatsValuelist $rowValuesperpage
                set FlowStatsValuelist [lindex $tempFlowStatsValuelist 0]
                set lengthFlowStatsList [llength $FlowStatsValuelist]
                set count 0
                while {$count < $lengthFlowStatsList} {
                      set checkingList [lindex $FlowStatsValuelist $count]
                      if {[lsearch -regexp $checkingList $matchStatListPerRow] != -1} {
                           lappend FlowStatslistperRxPort $checkingList
                      }
                incr count
                }

          }
          set lengthFlowStatsPerPortList [llength $FlowStatslistperRxPort]
          set count 0
          while {$count < $lengthFlowStatsPerPortList} {
                foreach {statName} $statNameList {
                    set statIndex [lsearch -regexp [ixNet getAttribute $statsPageView -columnCaptions] $statName]
                    set statval [lindex [lindex [lindex $FlowStatslistperRxPort $count] 0] $statIndex]
                    lappend FlowStatsperRxPortlist $statval
                }
          lappend returnFlowStatsperRxPortlist $FlowStatsperRxPortlist
          set FlowStatsperRxPortlist {}
          incr count
          }
          return $returnFlowStatsperRxPortlist
}


############################################################################################




#################################################################################
# Procedure : MaxMinThresholdTimeStamps
#
# Description: To Return Maximum or Minimum value of "DP Above Threshold TS"
#          or "DP Below Threshold TS" based on the flag and StatsName passed
#          as argument while calling this proc.
#
# Argument(s):
#         FlowstatValuePerRxPort -  List of selected stats value from "Flow
#                                   Statistic View".
#         StatsName     -  Its value can be either "DP Above Threshold TimeStamp"
#              or "DP Below Threshold TimeStamp" whose max or min
#              value is to return.
#         flag          -  Its value can either be "Max" or "Min",which decides
#                          either Max or Min of value is to return.
#
###############################################################################

proc MaxMinThresholdTimeStamps {FlowstatValuePerRxPort StatsName flag} {
         set count 0
         set totalFlowcount [llength $FlowstatValuePerRxPort]
         if {$StatsName == "Event Start Timestamp"} {
             while {$count < $totalFlowcount} {
                    set EventStartTs [lindex [lindex $FlowstatValuePerRxPort $count] 2]
                    lappend EventStartTsList $EventStartTs
                    incr count
             }
             set sortedEventStartTs [lsort $EventStartTsList]
             if {$flag == "Max"} {
                 return [lindex $EventStartTsList end]
             }
             if {$flag == "Min"} {
                return [lindex $EventStartTsList 0]
             }
         }
         if {$StatsName == "DP Above Threshold TimeStamp"} {
             while {$count < $totalFlowcount} {
                    set DpATT [lindex [lindex $FlowstatValuePerRxPort $count] 4]
                    lappend DpAttList $DpATT
                    incr count
             }
             set sortedDpAttList [lsort $DpAttList]
             if {$flag == "Max"} {
                 return [lindex $sortedDpAttList end]
             }
             if {$flag == "Min"} {
                return [lindex $sortedDpAttList 0]
             }
         }
         if {$StatsName == "DP Below Threshold TimeStamp"} {
             while {$count < $totalFlowcount} {
                    set DpBTT [lindex [lindex $FlowstatValuePerRxPort $count] 5]
                    lappend DpBttList $DpBTT
                    incr count
             }
             set sortedDpBttList [lsort $DpBttList]
             if {$flag == "Max"} {
                 return [lindex $sortedDpBttList end]
             }
             if {$flag == "Min"} {
                return [lindex $sortedDpBttList 0]
             }
          }
         if {$StatsName == "First TimeStamp"} {
             while {$count < $totalFlowcount} {
                    set FirstTS [lindex [lindex $FlowstatValuePerRxPort $count] 6]
                    lappend FirstTSList $FirstTS
                    incr count
             }
             set sortedFirstTSList [lsort $FirstTSList]
             if {$flag == "Max"} {
                 return [lindex $sortedFirstTSList end]
             }
             if {$flag == "Min"} {
                return [lindex $sortedFirstTSList 0]
             }
          }
         if {$StatsName == "Last TimeStamp"} {
             while {$count < $totalFlowcount} {
                    set LastTS [lindex [lindex $FlowstatValuePerRxPort $count] 7]
                    lappend LastTSList $LastTS
                    incr count
             }
             set sortedLastTSList [lsort $LastTSList]
             if {$flag == "Max"} {
                 return [lindex $sortedLastTSList end]
             }
             if {$flag == "Min"} {
                return [lindex $sortedLastTSList 0]
             }
          }
}




#######################################################


