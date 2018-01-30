

#############################################################################
# Common procs to be used for set & get attr
#############################################################################

#------------------------------------------------------------------------------
# PROCEDURE    : removePortList
# PURPOSR      : To clean up all the virtual ports from the IxNetwork GUI
# INPUT        : The list of virtual ports to be removed
# OUTPUT       : Removes all the virtual ports from the IxNetwork GUI
# RETURN VALUE : void
#------------------------------------------------------------------------------
proc removePortList {portList} {
    set len [llength $portList]
    set i 0
    while { $i < $len } {
        set port [lindex $portList $i]
        ixNet remove $port
        ixNet commit
        incr i
    }
}


#------------------------------------------------------------------------------
# PROCEDURE    : ixNetCleanUp
# PURPOSR      : Cleaning up, stop all protocols if running, close alnalyzer
#                tabs if open, stop test configuration etc.
# INPUT        : void
# OUTPUT       : Cleans up all configurations from IxNetwork GUI
# RETURN VALUE : void
# ASSUMPTION   : we are in the "connected" with the IxNetwork GUI
#------------------------------------------------------------------------------
proc ixNetCleanUp {} {

    # if protocols are not stopped handle it from here
    catch {ixNet exec stopAllProtocols}

    # Clean all tabs
    catch {ixNet exec closeAllTabs}

    # Stop integrated if running
    catch {
         #stop test configuration if it is running
         catch {ixNet exec stopTestConfiguration}

         while { [regexp [ixNet getAtt [ixNet getRoot]/testConfiguration \
               -testRunning] true ] } {
               after 20000
          }
    };  # stopp !!!!

    # Remove port
    ixTclNet::UnassignPorts [ixNet getList [::ixNet getRoot] vport]
    removePortList [ixNet getList [::ixNet getRoot] vport]

    # clean
    catch {ixNet execute newConfig}
}


#------------------------------------------------------------------------------
# PROCEDURE    : getPortList
# PURPOSR      : connecting to IxNetworl client
# INPUT        : [list $chassis1 $card1 $port1 $client1 $tcpPort1] and
#                [list $chassis2 $card2 $port2 $client2 $tcpPort2]
# OUTPUT       : Connects to IxNetwork Tcl server and chassis
# RETURN VALUE : list of virtual ports
#------------------------------------------------------------------------------
proc getPortList {portData1 portData2} {

    # get port info 1
    set chassisIp1 [lindex $portData1 0]
    set card1      [lindex $portData1 1]
    set port1      [lindex $portData1 2]
    set hostName1  [lindex $portData1 3]
    set tcpPort1   [lindex $portData1 4]

    # get port info 2
    set chassisIp2 [lindex $portData2 0]
    set card2      [lindex $portData2 1]
    set port2      [lindex $portData2 2]
    set hostName2  [lindex $portData2 3]
    set tcpPort2   [lindex $portData2 4]

    set portList [list [list $chassisIp1 $card1 $port1] \
                       [list $chassisIp2 $card2 $port2] ]

    if {[catch {ixNet connect $hostName1 -port $tcpPort1} result]} {
        puts "error in connect: $result"
        set iter 1
        while {$iter <= 3} {
            after 1000
            if {[catch {ixNet connect $hostName1 -port $tcpPort1} \
                result]} {
                puts "error on connect retry $iter: $result"
            } else {
                puts "successful connect on retry $iter"
                break
            }
            incr iter
        }
    }

    # after connecting cleaning up the network
    ixNetCleanUp

    ixTclNet::AssignPorts $portList
    set vPortList [ixNet getList [::ixNet getRoot] vport]
    return $vPortList
}

proc matchAttributeValue {object attr expectedVal} {
     set noMatch 1
     set val [ixNet getAtt $object -$attr]
     #puts "\t (-$attr)$val : $expectedVal (expected)"
     if {[string tolower $val] != [string tolower $expectedVal]} {
          #puts "\t -$attr : $val (expected $expectedVal) ---> No Match"
          return $noMatch
     }
     set noMatch 0
     return $noMatch
}

proc checkAttributeValue {object arr} {
    set isError 1
    array set expectProp $arr
    #parray expectProp
    foreach attr [array names expectProp] {
       set attVal [ixNet getAttr $object -$attr]
       set val $expectProp($attr)
       #puts "\t attVal = $attVal (-$attr) expectProp = $val"
       if {[string tolower $attVal] != [string tolower $val]} {
           #puts "\t -$attr : $attVal (expected $val) --> did not match!"
           return $isError
       }
    }
    set isError 0
    return $isError
}

proc setAndCheckAttributeValue {object attr arr} {
    set isError 1
    array set expectProp $arr
    #parray expectProp
    #puts "Verifying  $attr ..."
    foreach attrVal [array names expectProp] {
        set retVal $expectProp($attrVal)
        catch {ixNet setAttr $object -$attr $attrVal}
        ixNet commit
        set retAttrVal [ixNet getAttr $object -$attr]
        #puts "\t $attr = $retAttrVal ($attrVal :: $retVal)"
        if {(([string tolower $retAttrVal] != [string tolower $attrVal]) && ($retVal == "y")) || \
            (([string tolower $retAttrVal] == [string tolower $attrVal]) && ($retVal == "n"))} {
            #puts "\t $attr = $retAttrVal ($attrVal :: $retVal) --> Unexpected"
            return $isError
        }
    }
    set isError 0
    return $isError
}

proc getCciInmSec {cci} {
    if {$cci == "100msec"} {
        return 100
    }
    if {$cci == "10min"} {
        return 600000
    }
    if {$cci == "10msec"} {
        return 10
    }
    if {$cci == "10sec"} {
        return 10000
    }
    if {$cci == "1min"} {
        return 60000
    }
    if {$cci == "3.33msec"} {
        return 4
    }
    if {$cci == "1sec"} {
        return 1000
    }
    return -1
}



#############################################################################
# CFM Operations
#############################################################################


#-------------------------------------------------------------------------------
# PROCEDURE  : checkCfmCcmLearnedInfo
# PURPOSE    :
# PARAMETERS : bridge    - CFM/PBT bridge object
#              checkList - The list of expected info to be checked in learntInfoList
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc checkCfmCcmLearnedInfo {bridge filterList checkCcmList} {

    set isError 1

    # Below veriable is for debug puts only
    array set filterListArray $filterList
    puts "Setting Cfm Ccm Advanced filter ... \n [parray filterListArray]"

    # set filter following filterlist
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $bridge $attr [list $attrVal y]] == 1} {
            return $isError
        }
    }
    after 5000

    # Refresh CFM CCM learnt Info
    set status [ixNet exec refreshCcmLearnedInfo $bridge]

    set count 0
    set isComplete false
    puts "Retrieving Cfm Ccm learnt info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isCcmLearnedInfoRefreshed]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if { $count > 60 } {
            puts "Failed to retrieve Cfm Ccm learnt info ..."
            return $isError
        }
    }
    puts "Cfm Ccm learnt info refreshed ..."
    # CFM CCM Info Db
    set db {sVlan \
                cVlan \
                mdLevel \
                mepMacAddress \
                mepId \
                receivedRdi \
                someRmepDefect \
                allRmepDead \
                receivedPortTlvDefect \
                receivedIfaceTlvDefect \
                errCcmDefect \
                rmepCcmDefect \
                outOfSequenceCcmCount \
                receivedAis \
                cciInterval \
                shortMaNameFormat \
                shortMaName \
                mdNameFormat \
                mdName}

    # Get CCM Learned Info List
    set ccmLearnedInfoList [ixNet getList $bridge ccmLearnedInfo]
    if {[llength $ccmLearnedInfoList] == 0} {
        puts "No Cfm CCM learnt info present in database ... "
        return $isError
    }

    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0
    foreach checkList $checkCcmList {
        foreach $db $checkList {
            incr numInfoInCheckList
            puts " -----------------------------"
            puts "Browsing Cfm CCM learntinfo list ..."
            foreach ccmInfo $ccmLearnedInfoList {
                set misMatch 0
                foreach attr $db {
                    set attrVal [set [set attr]]
                    if {[matchAttributeValue $ccmInfo $attr $attrVal] == 1} {
                         set misMatch 1
                         break
                    }
                }
                if {$misMatch == 0} {
                    # Reached here -> all field match found in learnt info
                    puts "Expected learntinfo present in Cfm CCM learntinfo list ..."
                    puts " ----------------------------- "
                    incr isFound
                    break
                }
            }
        }
    }
    puts "Among all $numInfoInCheckList info $isFound are present in Cfm CCM Learnt Info List"
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}

#-------------------------------------------------------------------------------
# PROCEDURE  : checkCfmLtLearnedInfo
# PURPOSE    :
# PARAMETERS : bridge    - CFM/PBT bridge object
#              checkList - The list of expected info to be checked in learntInfoList
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc verifyLtHopInfo {ltHopInfo checkList} {
    set isError 1
    set db {ingressMac \
            egressMac \
            replyTtl \
            self}
    set numInfoInCheckList 0
    set isFound 0
    foreach $db $checkList {
        incr numInfoInCheckList
        puts " -----------------------------"
        puts "Browsing Link Trace Learned Hop list ..."
        foreach ltInfo $ltHopInfo {
            set misMatch 0
            foreach attr $db {
                set attrVal [set [set attr]]
                if {[matchAttributeValue $ltInfo $attr $attrVal] == 1} {
                     set misMatch 1
                     break
                }
            }
            if {$misMatch == 0} {
                # Reached here -> all field match found in learnt info
                puts "Expected learntinfo present in Cfm LT learnt Hop info list ..."
                puts " ----------------------------- "
                incr isFound
                break
            }
        }
    }

    puts "Among all $numInfoInCheckList info $isFound are present in Cfm LT Learnt Hop Info List"
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}

proc checkCfmLtLearnedInfo {bridge filterList checkList ltLearnedHopList \
                        {configMep "true"} {transactionId 0} {timeout 5000} {ttl 64}} {

    set isError 1

    # Below veriable is for debug puts only
    array set filterListArray $filterList
    puts "Setting Cfm Lt Advanced filter ... \n [parray filterListArray]"

    # set filter following filterlist
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $bridge $attr [list $attrVal y]] == 1} {
            return $isError
        }
    }

    # set userLearnedInfoTimeOut
    if {[setAndCheckAttributeValue $bridge "userLearnedInfoTimeOut" [list $timeout y]] == 1} {
        return $isError
    }

    # set userTtlInterval
    if {[setAndCheckAttributeValue $bridge "userTtlInterval" [list $ttl y]] == 1} {
        return $isError
    }

    # Check case with unconfigured MEP
    if {([string tolower $configMep] == "false") && ($transactionId != 0)} {
        if {[setAndCheckAttributeValue $bridge "userTransactionId" [list $transactionId y]] == 1} {
            return $isError
        }
    }

    after 5000

    # Refresh CFM LT learnt Info
    set status [ixNet exec startLinkTrace $bridge]

    set count 0
    set isComplete false
    puts "Retrieving Cfm Lt learnt info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isLinkTraceLearnedInfoRefreshed]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if { $count > 60 } {
            puts "Failed to retrieve Cfm Lt learnt info, [ixNet getAttr $bridge -ltLearnedErrorString]"
            return $isError
        }
    }
    puts "Cfm Lt learnt info refreshed ..."

    # Check CFM LT pkt sent
    if {[matchAttributeValue $bridge "isLtLearnedPacketSent" "True"] == 1} {
        puts "No Cfm Lt pkt sent, [ixNet getAttr $bridge -ltLearnedErrorString]"
        return $isError
    }
    puts "Cfm Link Trace pkt sent ? [ixNet getAttr $bridge -isLtLearnedPacketSent]"

    # CFM LT Db
    set db {sVlan \
            cVlan \
            mdLevel \
            srcMacAddress \
            dstMacAddress \
            hopCount \
            replyStatus}

    # Get LT Learned Info List
    set ltLearnedInfoList [ixNet getList $bridge ltLearnedInfo]

    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0
    foreach $db $checkList {
        incr numInfoInCheckList
        puts " -----------------------------"
        puts "Browsing Cfm Lt learntinfo list ..."
        foreach ltInfo $ltLearnedInfoList {
            set misMatch 0
            foreach attr $db {
                set attrVal [set [set attr]]
                if {[matchAttributeValue $ltInfo $attr $attrVal] == 1} {
                     set misMatch 1
                     break
                }
            }
            if {$misMatch == 0} {
        # Check Lt Learned HopList
                set ltHopInfo [ixNet getList $ltInfo ltLearnedHop]
                if [verifyLtHopInfo $ltHopInfo $ltLearnedHopList] {
            set misMatch 1
                    continue
                }
                # Check case with unconfigured MEP
                if {([string tolower $configMep] == "false") && ($transactionId != 0)} {
                    if {[matchAttributeValue $lbInfo "transactionId" $transactionId] == 1} {
                        continue
                    }
                }
                puts "Cfm Lt Learned ConfigMep ? : [ixNet getAttr $bridge -isLtLearnedConfigMep] \
                    (replyStatus : [ixNet getAttr $ltInfo -replyStatus], hops : [ixNet getAttr $ltInfo -hops])"

                # Reached here -> all field match found in learnt info
                puts "Expected learntinfo present in CFM Link Trace learntinfo list ..."
                puts " ----------------------------- "
                incr isFound
                break
            }
        }
    }

    puts "Among all $numInfoInCheckList info $isFound are present in Link Trace Learnt Info List"
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : checkCfmLbLearnedInfo
# PURPOSE    : Check CFM Loopback Info following specification
# PARAMETERS :
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc checkCfmLbLearnedInfo {bridge filterList checkList {configMep "true"} {transactionId 0} {timeout 5000}} {

    set isError 1

    # Below veriable is for debug puts only
    array set filterListArray $filterList
    puts "Setting Cfm Loopback Advanced filter ... \n [parray filterListArray]"

    # set filter following filterlist
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $bridge $attr [list $attrVal y]] == 1} {
            return $isError
        }
    }

    # set userLearnedInfoTimeOut
    if {[setAndCheckAttributeValue $bridge "userLearnedInfoTimeOut" [list $timeout y]] == 1} {
        return $isError
    }

    # Check case with unconfigured MEP
    if {([string tolower $configMep] == "false") && ($transactionId != 0)} {
        if {[setAndCheckAttributeValue $bridge "userTransactionId" [list $transactionId y]] == 1} {
            return $isError
        }
    }

    after 5000

    # Refresh CFM Loopback learnt Info
    set status [ixNet exec startLoopback $bridge]

    set count 0
    set isComplete false
    puts "Retrieving CFM Loopback learnt info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isLoopbackLearnedInfoRefreshed]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if { $count > 60 } {
            puts "Failed to retrieve CFM Loopback learnt info, [ixNet getAttr $bridge -lbLearnedErrorString]"
            return $isError
        }
    }
    puts "Cfm Loopback learnt info refreshed ..."

    # Check CFM LT pkt sent
    if {[matchAttributeValue $bridge "isLbLearnedPacketSent" "True"] == 1} {
        puts "No CFM LB pkt sent, [ixNet getAttr $bridge -lbLearnedErrorString]"
        return $isError
    }

    # CFM LB Db
    set db {sVlan \
            cVlan \
            mdLevel \
            srcMacAddress \
            dstMacAddress \
            reachability}

    # Get LB Learned Info List
    set lbLearnedInfoList [ixNet getList $bridge lbLearnedInfo]

    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0
    foreach $db $checkList {
        incr numInfoInCheckList
        puts " -----------------------------"
        puts "Browsing CFM Loopback learntinfo list ..."
        foreach lbInfo $lbLearnedInfoList {
            set misMatch 0
            foreach attr $db {
                set attrVal [set [set attr]]
                if {[matchAttributeValue $lbInfo $attr $attrVal] == 1} {
                     set misMatch 1
                     break
                }
            }
            if {$misMatch == 0} {
                # Check case with unconfigured MEP
                if {([string tolower $configMep] == "false") && ($transactionId != 0)} {
                    if {[matchAttributeValue $lbInfo "transactionId" $transactionId] == 1} {
                        continue
                    }
                }
                puts "Pbt LB Learned ConfigMep ? : [ixNet getAttr $bridge -isLbLearnedConfigMep] \
                    (reachability : [ixNet getAttr $lbInfo -reachability] \
                    transactionId : [ixNet getAttr $lbInfo -transactionId])"

                # Reached here -> all field match found in learnt info
                puts "Expected learntinfo present in CFM Loopback learntinfo list ..."
                puts " ----------------------------- "
                incr isFound
                break
            }
        }
    }

    puts "Among all $numInfoInCheckList info $isFound are present in Loopback Learnt Info List"

    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}

#-------------------------------------------------------------------------------
# PROCEDURE  : checkItuDelayLearnedInfo
# PURPOSE    : Check ITU Delay Learnt info getting populated correctly
# PARAMETERS : bridge    - CFM/PBT bridge object
#              checkList - The list of expected info to be checked in learntInfoList
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkItuDelayLearnedInfo {bridge filterList checkList {timeout 5000}} {

    set isError 1

    # Below veriable is for debug puts only
    array set filterListArray $filterList
    puts "Setting ITU Delay filter ... \n [parray filterListArray]"

    # set filter following filterlist
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $bridge $attr [list $attrVal y]] == 1} {
            return $isError
        }
    }

    # set userLearnedInfoTimeOut
    if {[setAndCheckAttributeValue $bridge "userLearnedInfoTimeOut" [list $timeout y]] == 1} {
        return $isError
    }

    after 5000

    # Refresh Itu Delay learnt Info
    set status [ixNet exec startDelayMeasurement $bridge]

    set count 0
    set maxCount [expr [expr $timeout / 1000] + 10] ;# timeout + 10 sec
    set isComplete false
    puts "Retrieving ITU Delay info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isDelayMeasurementLearnedInfoRefreshed]
        puts "isComplete ---> $isComplete"
        after 1000
        incr count
        if { $count > $maxCount } {
            puts "Failed to retrieve ITU Delay info, [ixNet getAttr $bridge -delayLearnedErrorString]"
            return $isError
        }
    }
    puts "ITU Delay info refreshed ..."

    # Check Itu Delay pkt sent
    if {[matchAttributeValue $bridge "isDelayLearnedPacketSent" "True"] == 1} {
        puts "No Itu Delay pkt sent, [ixNet getAttr $bridge -delayLearnedErrorString]"
        return $isError
    }
    puts "ITU Delay pkt sent ... "

    set delayInfo [lindex [ixNet getList $bridge delayLearnedInfo] 0]
    set delayInSec [ixNet getAttr $delayInfo -valueInSec]
    set delayInNanoSec [ixNet getAttr $delayInfo -valueInNanoSec]
    puts "ITU Learned ConfigMep ? : [ixNet getAttr $bridge -isDelayLearnedConfigMep] \
                                 (valueInSec : $delayInSec, valueInNanoSec : $delayInNanoSec)"

    # CheckList Map (reference only veriable)
    set checkListMap {isDelayLearnedConfigMep \
                       tolerence \
                       valueInSec \
                       valueInNanoSec}

    set configMep [lindex $checkList 0]
    if {[matchAttributeValue $bridge "isDelayLearnedConfigMep" $configMep] == 1} {
         return $isError
    }

    # Check case with unconfigured MEP
    if {[string tolower $configMep] == "false"} {
        if {($delayInSec != 0) || ($delayInNanoSec != 0)} {
            return $isError
        }
        set isError 0
        return $isError
    } else {
      if {($delayInSec != 0) && ($delayInNanoSec != 0)} {
            return $isError
        }
        set isError 0
        return $isError
    }

    # Now only configured MEP case left
    set matchTol [lindex $checkList 1]
    if {($matchTol > 100) || ($matchTol < -1)} {
         # Wrong user input, setting it to -1
         set matchTol -1
    }
    # Match tolerence -1, Just check for delay > 0 no specific value
    if {($matchTol == -1) && ($delayInSec == 0) && ($delayInNanoSec == 0)} {
        return $isError
    }
    # Match tolerence <0 - 100>
    if {($matchTol >= 0) && ($matchTol <= 100)} {
        set expectedDelayInSec [lindex $checkList 2]
        set min [expr $expectedDelayInSec - [expr [expr double($matchTol) / 100] * $expectedDelayInSec]]
        set max [expr $expectedDelayInSec + [expr [expr double($matchTol) / 100] * $expectedDelayInSec]]

        puts "expectedDelayInSec : $expectedDelayInSec , delayInSec : $delayInSec"
        if {($delayInSec < $min) || ($delayInSec > $max)} {
            return $isError
        }

        set expectedDelayInNanoSec [lindex $checkList 3]
        set min [expr $expectedDelayInNanoSec - [expr [expr double($matchTol) / 100] * $expectedDelayInNanoSec]]
        set max [expr $expectedDelayInNanoSec + [expr [expr double($matchTol) / 100] * $expectedDelayInNanoSec]]

        puts "< $min - $max >"
        puts "expectedDelayInNanoSec : $expectedDelayInNanoSec , delayInNanoSec : $delayInNanoSec]"
        if {($delayInNanoSec < $min) || ($delayInNanoSec > $max)} {
            return $isError
        }
    }
    set isError 0
    return $isError
}


#############################################################################
# PBT operations
#############################################################################

#-------------------------------------------------------------------------------
# PROCEDURE  : enableDisablePbtTrunk
# PURPOSE    : Enable/Disable Pbt Trunk following specification
# PARAMETERS :
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc enableDisablePbtTrunk {bridge en_disen conditionList} {
    set isError 1
    set trunkList [ixNet getList $bridge trunk]
    set numTrunks [llength $trunkList]
    for {set x 0} {$x < $numTrunks} {incr x} {
        set trunk [lindex $trunkList $x]
        if {[checkAttributeValue $trunk $conditionList] == 0} {
            # enable/disable the trunk
            if {[setAndCheckAttributeValue $trunk "enabled" [list $en_disen y]] == 1} {
                return $isError
            }
            set isError 0
            return $isError
        }
    }
    return $isError
}

#-------------------------------------------------------------------------------
# PROCEDURE  : getCciForPbtTrunk
# PURPOSE    : returns configured CCI for Pbt Trunk following specification
# PARAMETERS :
# RETURN     : string - configured CCI
#-------------------------------------------------------------------------------
proc getCciForPbtTrunk {bridge conditionList} {
    set cci 0
    set trunkList [ixNet getList $bridge trunk]
    set numTrunks [llength $trunkList]
    for {set x 0} {$x < $numTrunks} {incr x} {
        set trunk [lindex $trunkList $x]
        if {[checkAttributeValue $trunk $conditionList] == 0} {
            set cci [getCciInmSec [ixNet getAttr $trunk -cciInterval]]
            return $cci
        }
    }
    return $cci
}

#-------------------------------------------------------------------------------
# PROCEDURE  : checkPbtDelayLearnedInfo
# PURPOSE    :
# PARAMETERS : bridge    - CFM/PBT bridge object
#              checkList - The list of expected info to be checked in learntInfoList
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkPbtDelayLearnedInfo {bridge filterList checkList {timeout 5000}} {

    set isError 1

    # Below veriable is for debug puts only
    array set filterListArray $filterList
    puts "Setting Pbt Delay filter ... \n [parray filterListArray]"

    # set filter following filterlist
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $bridge $attr [list $attrVal y]] == 1} {
            return $isError
        }
    }

    # set userLearnedInfoTimeOut
    if {[setAndCheckAttributeValue $bridge "userLearnedInfoTimeOut" [list $timeout y]] == 1} {
        return $isError
    }

    after 5000

    # Refresh Pbt LB learnt Info
    set status [ixNet exec startDelayMeasurement $bridge]

    set count 0
    set maxCount [expr [expr $timeout / 1000] + 10] ;# timeout + 10 sec
    set isComplete false
    puts "Retrieving Pbt Delay info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isPbbTeDelayLearnedInfoRefreshed]
        puts "isComplete ---> $isComplete"
        after 1000
        incr count
        if { $count > $maxCount } {
            puts "Failed to retrieve Pbt Delay info, [ixNet getAttr $bridge -pbbTeDelayLearnedErrorString]"
            return $isError
        }
    }
    puts "Pbt Delay info refreshed ..."

    # Check Pbt Delay pkt sent
    if {[matchAttributeValue $bridge "isPbbTeDelayLearnedPacketSent" "True"] == 1} {
        puts "No Pbt Delay pkt sent, [ixNet getAttr $bridge -pbbTeDelayLearnedErrorString]"
        return $isError
    }
    puts "PbbTe Delay pkt sent ... "

    set delayInfo [lindex [ixNet getList $bridge pbbTeDelayLearnedInfo] 0]
    set delayInSec [ixNet getAttr $delayInfo -valueInSec]
    set delayInNanoSec [ixNet getAttr $delayInfo -valueInNanoSec]
    puts "Pbt LB Learned ConfigMep ? : [ixNet getAttr $bridge -isPbbTeDelayLearnedConfigMep] \
                                 (valueInSec : $delayInSec, valueInNanoSec : $delayInNanoSec)"

    # CheckList Map (reference only veriable)
    set checkListMap {isPbbTeDelayLearnedConfigMep \
                       tolerence \
                       valueInSec \
                       valueInNanoSec}

    set configMep [lindex $checkList 0]
    if {[matchAttributeValue $bridge "isPbbTeDelayLearnedConfigMep" $configMep] == 1} {
         return $isError
    }

    # Check case with unconfigured MEP
    if {[string tolower $configMep] == "false"} {
        if {($delayInSec != 0) || ($delayInNanoSec != 0)} {
            return $isError
        }
        set isError 0
        return $isError
    } else {
      if {($delayInSec != 0) && ($delayInNanoSec != 0)} {
            return $isError
        }
        set isError 0
        return $isError
    }

    # Now only configured MEP case left
    set matchTol [lindex $checkList 1]
    if {($matchTol > 100) || ($matchTol < -1)} {
         # Wrong user input, setting it to -1
         set matchTol -1
    }
    # Match tolerence -1, Just check for delay > 0 no specific value
    if {($matchTol == -1) && ($delayInSec == 0) && ($delayInNanoSec == 0)} {
        return $isError
    }
    # Match tolerence <0 - 100>
    if {($matchTol >= 0) && ($matchTol <= 100)} {
        set expectedDelayInSec [lindex $checkList 2]
        set min [expr $expectedDelayInSec - [expr [expr double($matchTol) / 100] * $expectedDelayInSec]]
        set max [expr $expectedDelayInSec + [expr [expr double($matchTol) / 100] * $expectedDelayInSec]]

        puts "expectedDelayInSec : $expectedDelayInSec , delayInSec : $delayInSec"
        if {($delayInSec < $min) || ($delayInSec > $max)} {
            return $isError
        }

        set expectedDelayInNanoSec [lindex $checkList 3]
        set min [expr $expectedDelayInNanoSec - [expr [expr double($matchTol) / 100] * $expectedDelayInNanoSec]]
        set max [expr $expectedDelayInNanoSec + [expr [expr double($matchTol) / 100] * $expectedDelayInNanoSec]]

        puts "< $min - $max >"
        puts "expectedDelayInNanoSec : $expectedDelayInNanoSec , delayInNanoSec : $delayInNanoSec]"
        if {($delayInNanoSec < $min) || ($delayInNanoSec > $max)} {
            return $isError
        }
    }
    set isError 0
    return $isError
}

#-------------------------------------------------------------------------------
# PROCEDURE  : checkPbtLbLearnedInfo
# PURPOSE    :
# PARAMETERS : bridge    - CFM/PBT bridge object
#              checkList - The list of expected info to be checked in learntInfoList
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc checkPbtLbLearnedInfo {bridge filterList checkList {configMep "true"} \
                {transactionId 0} {timeout 5000} } {

    set isError 1

    # Below veriable is for debug puts only
    array set filterListArray $filterList
    puts "Setting Pbt LB filter ... \n [parray filterListArray]"

    # set filter following filterlist
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $bridge $attr [list $attrVal y]] == 1} {
            return $isError
        }
    }

    # set userLearnedInfoTimeOut
    if {[setAndCheckAttributeValue $bridge "userLearnedInfoTimeOut" [list $timeout y]] == 1} {
        return $isError
    }

    # Check case with unconfigured MEP
    if {([string tolower $configMep] == "false") && ($transactionId != 0)} {
        if {[setAndCheckAttributeValue $bridge "userTransactionId" [list $transactionId y]] == 1} {
            return $isError
        }
    }

    after 5000

    # Refresh Pbt LB learnt Info
    set status [ixNet exec startLoopback $bridge]

    set count 0
    set maxCount [expr [expr $timeout / 1000] + 10] ;# timeout + 10 sec
    set isComplete false
    puts "Retrieving Pbt LB learnt info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isPbbTeLbLearnedInfoRefreshed]
        puts "isComplete ---> $isComplete"
        after 1000
        incr count
        if { $count > $maxCount } {
            puts "Failed to retrieve Pbt LB learnt info, [ixNet getAttr $bridge -pbbTeLbLearnedErrorString]"
            return $isError
        }
    }
    puts "Pbt Lb learnt info refreshed ..."

    # Attr list to match
    set db {bVlan \
        mdLevel \
        srcMacAddress \
        dstMacAddress \
        reachability}

    # Check Pbt LB pkt sent
    if {[matchAttributeValue $bridge "isPbbTeLbLearnedPacketSent" "True"] == 1} {
        puts "No Pbt LB pkt sent, [ixNet getAttr $bridge -pbbTeLbLearnedErrorString]"
        return $isError
    }

    set lbLearnedInfoList [ixNet getList $bridge pbbTeLbLearnedInfo]

    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0
    foreach $db $checkList {
        incr numInfoInCheckList
        foreach lbInfo $lbLearnedInfoList {
            set misMatch 0
            foreach attr $db {
                set attrVal [set [set attr]]
                if {[matchAttributeValue $lbInfo $attr $attrVal] == 1} {
                     set misMatch 1
                     break
                }
            }
            if {$misMatch == 0} {
                # Check case with unconfigured MEP
                if {([string tolower $configMep] == "false") && ($transactionId != 0)} {
                    if {[matchAttributeValue $lbInfo "transactionId" $transactionId] == 1} {
                        continue
                    }
                }
                puts "Pbt LB Learned ConfigMep ? : [ixNet getAttr $bridge -isPbbTeLbLearnedConfigMep] \
                    (reachability : [ixNet getAttr $lbInfo -reachability], rtt : [ixNet getAttr $lbInfo -rtt])"
                # Reached here -> all field match found in learnt info
                incr isFound
                break
            }
        }
    }
    puts "Among all $numInfoInCheckList info $isFound are present in PBT LB Learnt Info List"
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : checkCfmPbtCcmLearnedInfo
# PURPOSE    :
# PARAMETERS : bridge    - CFM/PBT bridge object
#              checkList - The list of expected info to be checked in learntInfoList
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc checkCfmPbtCcmLearnedInfo {bridge checkCcmList} {

    set isError 1
    set status [ixNet exec refreshCcmLearnedInfo $bridge]

    set count 0
    set isComplete false
    puts "Retrieving Pbt Ccm learnt info ..."
    while { $isComplete != true } {
        set isComplete [ixNet getAttr $bridge -isPbbTeCcmLearnedInfoRefreshed]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if { $count > 60 } {
            puts "Failed to retrieve Pbt Ccm learnt info ..."
            return $isError
        }
    }

    puts "Pbt Ccm learnt info refreshed ..."

    # PBT CCM Db
    set db {bVlan \
        remoteMacAddress \
        srcMacAddress \
        shortMaNameFormat \
        shortMaName \
        remoteMepId \
        srcMepId \
        mdLevel \
        mdNameFormat \
        mdName \
        receivedRdi \
        receivedPortTlvDefect \
        receivedIfaceTlvDefect \
        errCcmDefect \
        rmepCcmDefect \
        outOfSequenceCcmCount \
        cciInterval \
        errCcmDefectCount \
        portTlvDefectCount \
        ifaceTlvDefectCount \
        remoteMepDefectCount }

    # Get CCM Learned Info List
    set ccmLearnedInfoList [ixNet getList $bridge pbbTeCcmLearnedInfo]
    puts " length of ccmLearnedInfoList [llength $ccmLearnedInfoList]"
    if {[llength $ccmLearnedInfoList] == 0} {
        puts "No CCM learnt info present in database ... "
        return $isError
    }
    # Loop through expected list & search in learntinfo list
    set numInfoInCheckList 0
    set isFound 0
    foreach checkList $checkCcmList {
        foreach $db $checkList {
            incr numInfoInCheckList
            puts " -----------------------------"
            puts "Browsing CCM learntinfo list ..."
            foreach ccmInfo $ccmLearnedInfoList {
                set misMatch 0
                foreach attr $db {
                    set attrVal [set [set attr]]
                    if {[matchAttributeValue $ccmInfo $attr $attrVal] == 1} {
                        set misMatch 1
                        break
                    }
                }
                if {$misMatch == 0} {
                    # Reached here -> all field match found in learnt info
                    puts "Expected learntinfo present in CCM learntinfo list ..."
                    puts " ----------------------------- "
                    incr isFound
                    break
                }
            }
        }
    }

    puts "Among all $numInfoInCheckList info $isFound are present in CCM Learnt Info List"
    if {$numInfoInCheckList != $isFound} {
        return $isError
    }

    set isError 0
    return $isError
}

################################################################################
# STATISTICS VERIFICATION
################################################################################

#-------------------------------------------------------------------------------
# PROCEDURE  : checkAllCfmStats
# PURPOSE    :
# PARAMETERS : portList -
#              stat - {name value} Stat list to verify
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc checkAllCfmStats {portList stat {exactMatch 0}} {
    set sessFoundFlag 0
    set userViewList [ixNet getList [ixNet getRoot]/statistics userStatView]
    foreach view $userViewList {
        ixNet remove $view
        ixNet commit
    }

    set userStatView [SetupUserStats $portList "CFM" "*"]
    set timeout 20
    set doneList $portList

    array set statToVerify $stat
    set statNames [array names statToVerify]


    set returnFlag 1
    #Checking the stats.."
    set contFlag 0
    puts [format "%-32s %10s\t%10s" "STAT NAME" "EXPECTED" "OBTAINED"]
    foreach eachStat $statNames {
        while {$timeout > 0} {
            GetStatValue "UserStatView CFM" "$eachStat" statValueArray1
            if {[lindex [array get statValueArray1] 1] >= $statToVerify($eachStat)} {
                PrintArray statValueArray1
                #puts "$eachStat : $statToVerify($eachStat) (Expected) [lindex [array get statValueArray1] 1] (Obtained)"
                puts [format "%-32s %10d\t%10d" $eachStat $statToVerify($eachStat) [lindex [array get statValueArray1] 1]]
                if {($exactMatch == 1) && [lindex [array get statValueArray1] 1] != $statToVerify($eachStat)} {
                    return 1
            }
            } else {
                PrintArray statValueArray1
                #puts "$eachStat : $statToVerify($eachStat) (Expected) \
        #       [lindex [array get statValueArray1] 1] (Obtained) --> MIS Match"
                puts [format "%-32s %10d\t%10d --> MIS Match" $eachStat $statToVerify($eachStat) [lindex [array get statValueArray1] 1]]
                set returnFlag 0
                return 1
            }

            foreach portItem $doneList {
                scan [join [split $portItem]] "%s %s %s" ch card port
                set sessFoundFlag 0
                if {([llength [array get statValueArray1]] > 0)} {
                    if {$statValueArray1($ch,$card,$port) >= 0} {
                        set sessFoundFlag 1
                        set index [lsearch $doneList [list $ch $card $port]]
                        if {$index != -1} {
                            set doneList [lreplace $doneList $index $index]
                        }
                    }
                }
            }

            if {[llength $doneList] == 0} {
                set contFlag 1
                break
            } else {
                incr timeout -1
                after 1000
            }
        }
    }


    if {$contFlag == 0} {
        putsMsg "Error... Check the configuration"
        return 1
    }

    if {$returnFlag == 1} {
        return 0
    } else {
        return 1
    }
    after 2000
}

################################################################################
# PACKET STRUCTURE VERIFICATION
################################################################################

#-------------------------------------------------------------------------------
# PROCEDURE  : verifyCapturedPackets
# PURPOSE    : Verifying expected field value in Captured Packets
# PARAMETERS : chassis -
#              card -
#              port -
#              matchFieldList - list of {startIndex endIndex expectedVal}
#              expPktCnt - {default value 1}
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc verifyCapturedPackets {chassis card port matchFieldList {expPktCnt 1}} {
    set isError 1

    puts "Initilizing thorugh IxTclHal...."
    ixInitialize $chassis
    chassis get $chassis
    set chassisId [chassis cget -id]

    port get $chassisId $card $port
    set putsinName [port cget -owner]
    ixLogin $putsinName
    puts "Logging in using the $putsinName"

    # Retrive captured packets
    captureBuffer get $chassisId $card $port
    set numCapturedPkts [captureBuffer cget -numFrames]
    puts "Captured $numCapturedPkts pkts (expected: $expPktCnt)"
    if {$numCapturedPkts < $expPktCnt} {
        return $isError
    }
    captureBuffer get $chassisId $card $port 1 $numCapturedPkts
    for {set f 1} {$f <= $numCapturedPkts} {incr f} {
        after 50
        captureBuffer getframe $f
        after 50
        set capframe [captureBuffer cget -frame]
        set mismatch 0
        foreach {startIndex endIndex expectedVal} $matchFieldList {
            puts "Obtained: [lrange $capframe $startIndex $endIndex] \
                        Expected: $expectedVal"
            if {[lrange $capframe $startIndex $endIndex] != $expectedVal} {
                set mismatch 1
                puts "Obtained: [lrange $capframe $startIndex $endIndex] \
                        Expected: $expectedVal ---> No Match"
                break
            }
        }
        if {$mismatch == 0} {
            puts "All Field Patterns Matched !!!"
            set isError 0
            return $isError
        }
    }
    if {$mismatch == 1} {
        puts "Not all Field Patterns Matched !!!"
        return $isError
    }
}

########################################################################################
#                UTIL FOR MAC RANGE CONFIGURATION
########################################################################################

proc getNextMacAddress {lastMacAddressUsed {incrStep 1} {maxBytePosToIncrement 1}} {
    set splitAnMacAddress [split $lastMacAddressUsed ":"]
    for {set i 0} {$i < 6} {incr i} {
        set position [expr $i +1]
        set MacDigit$position [format "%i" 0x[lindex $splitAnMacAddress $i]]
    }

    set posToIncr -1
    incr MacDigit6 +$incrStep
    if {$MacDigit6 > 255} {
        set MacDigit6 $incrStep
        for {set j 5} {$j >= $maxBytePosToIncrement } {incr j -1} {
            set MacDigit [set MacDigit$j]
            if {$MacDigit < 255} {
                set posToIncr $j
                incr MacDigit
                set MacDigit$j $MacDigit
                break
            } else {
                set MacDigit$j 0
            }
        }
    } else {
        set posToIncr 6
    }

    if {$posToIncr == -1} {
        error "Crossing the configurable MAC range Limit from this Harness. \
              Reduce configuration & Try !!!"
    }

    for {set j 1} {$j <= 6} {incr j} {
        set MacDigit [set MacDigit$j]
        set MacDigit$j [format "%0.2x" $MacDigit]
    }
    lappend macAddr $MacDigit1:$MacDigit2:$MacDigit3:$MacDigit4:$MacDigit5:$MacDigit6
    return $macAddr
}

