proc bgpImportFunctionality {importRouteOptions fileName {changeList ""}} {
   
    set isError 0
    set FAILED 1
   
    if {$changeList == 1} {
        ixNet setAttr $importRouteOptions -routeFileType "Ixia Format"
        log "IXIA Format importing"
     }

     if {$changeList == 2} {
        ixNet setAttr $importRouteOptions -routeFileType "Cisco IOS"
        log "CISCO Format importing"
     }

     if {$changeList == 3} {
        ixNet setAttr $importRouteOptions -routeFileType "Juniper JUNOS"
        log "JUNIPER Format importing"
     }
     ixNet commit
   
     if {[ixNet exec importOpaqueRouteRangeFromFile $importRouteOptions \
         [ixNet readFrom $fileName]] != "::ixNet::OK"} {
         log "FAILURE : Could not import file to neighbor"
         return $FAILED
     } else {
         puts "SUCCESS : Successfully imported file to neighbor"
     }
   
    set isError 0
    return $isError
}
 

proc learnedInfoFetchForRouteImport {bgpNeighbor expectedList} {
    set noMatch 1
    ixNet exec refreshLearnedInfo $bgpNeighbor
    after 5000

    set db {asPath                 \
            multiExitDiscriminator \
            neighbor               \
            ipPrefix}
       
    set learnedInformationList    [ixNet getList $bgpNeighbor learnedInformation]
    set BGPlearnedInformationList [ixNet getList $learnedInformationList ipv4Unicast]
    
    set matchList {}
    foreach BGPInfo $BGPlearnedInformationList  {
        set temp {}
        foreach attr $db {
            set attrVal [ixNet getAttr $BGPInfo -$attr]
            lappend temp $attrVal
        }
        lappend matchList $temp
    }

    puts "$matchList" 
    foreach expectedRoute $expectedList {
        set matchIndex [lsearch $matchList $expectedRoute]
        log "<Expected> : $expectedRoute"
        log "<received> : [lindex $matchList $matchIndex]"
        if {$matchIndex < 0} {
            puts "###############################################################################"
            return 0
        }
    }

   return 1 
}
