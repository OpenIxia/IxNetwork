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

#############################################################################
# Common procs to be used for set & get attr
#############################################################################
proc matchAttributeValue {object attr expectedVal} {
    set noMatch 1
    set val [ixNet getAtt $object -$attr]
    #puts "\t (-$attr)$val : $expectedVal (expected)"
    if {[string tolower $val] != [string tolower $expectedVal]} {
        puts "\t -$attr : $val (expected $expectedVal) ---> No Match"
        return $noMatch
    }
    puts "\t -$attr : $val (expected $expectedVal) ---> Match"
    set noMatch 0
    return $noMatch
}


proc setAndCheckAttributeValue {object attr arr} {
    set isError 1
    array set expectProp $arr
    #parray expectProp
    foreach attrVal [array names expectProp] {
        set retVal $expectProp($attrVal)
        catch {ixNet setAttr $object -$attr $attrVal}
        ixNet commit
        set retAttrVal [ixNet getAttr $object -$attr]
        puts "\t $attr = $retAttrVal ($attrVal :: $retVal)"
        if {(([string tolower $retAttrVal] != [string tolower $attrVal])  && \
             ($retVal == "y"))                                            || \
             (([string tolower $retAttrVal] == [string tolower $attrVal]) && \
             ($retVal == "n"))} {
            puts "\t $attr = $retAttrVal ($attrVal :: $retVal) --> Unexpected"
            return $isError
        }
    }
    set isError 0
    return $isError
}


proc checkAttributeValue {object arr} {
    set isError 1
    array set expectProp $arr
    #parray expectProp
    foreach attr [array names expectProp] {
       set attVal [ixNet getAttr $object -$attr]
       set val $expectProp($attr)
       puts "\t attVal = $attVal (-$attr) expectProp = $val"
       if {[string tolower $attVal] != [string tolower $val]} {
           puts "\t -$attr : $attVal (expected $val) --> did not match!"
           return $isError
       }
    }
    set isError 0
    return $isError
}


################################################################################
# LEARNED INFO VERIFICATION
################################################################################
#-------------------------------------------------------------------------------
#       Procedure : getBSRRPInfo
#
#       Description: Prints the Learnt Info
#
#       Argument(s):
#               interface - Interface on which RP has to be added.
#-------------------------------------------------------------------------------
proc getBSRInfo {interface checkLearnedBSRList {exactMatch 1}} {
    set isError 1
    set ref [ixNet exec refreshCrpBsrLearnedInfo $interface]

    puts "Refreshing for learnt BSR information on PIMSM interface : \
          $interface...\n"

    set count 0
    set isComplete false
    while {$isComplete != true} {
        set isComplete [ixNet getAttr $interface -isRefreshRpSetComplete]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if {$count > 40} {
            puts "Failed to retrieve learnt BSR info on pimsm interface : \
                  $interface, timeout"
            return $isError
        }
    }
    puts "RP learnt information refreshed ..."

    # Get RP Learned Info List
    set bsrLearnedInfoList [ixNet getList $interface learnedBsrInfo]
    if {[llength $bsrLearnedInfoList] == 0} {
        puts "No BSR learnt info present ... "
        return $isError
    }

    # Search in learntinfo list
    set bsrInfo [lindex $bsrLearnedInfoList 0]
    puts "Browsing BSR learnt Info list ..."
    puts "---------------------------------"
    foreach {attr attrVal} $checkLearnedBSRList {
        #puts "Expected val for $attr is $attrVal"
        if {[matchAttributeValue $bsrInfo $attr $attrVal] == 1} {
            # Handle not exactMatch cases hare ....
            puts "All infos not present in BSR Learnt Info List"
            return $isError
        }
    }

    puts "\t Time elapsed since last BSM send/recv : \
            [ixNet getAtt $bsrInfo -lastBsmSendRecv]"
            
    puts "All info are present in BSR Learnt Info List"
    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
#  Procedure  : GetLearntRPInfo
#
#  Description: Prints the Learnt Info
#
#  Argument(s): interface - Interface on which RP has to be added.
#-------------------------------------------------------------------------------
proc getRPInfo {interface checkLearnedRPList {exactMatch 1}} {
    set isError 1
    set ref [ixNet exec refreshCrpBsrLearnedInfo $interface]

    puts "Refreshing for learnt RP information on PIMSM interface : \
            $interface...\n"

    set count 0
    set isComplete false
    while {$isComplete != true} {
        set isComplete [ixNet getAttr $interface -isRefreshRpSetComplete]
        puts "isComplete --> $isComplete"
        after 1000
        incr count
        if {$count > 40} {
            puts "Failed to retrieve learnt RP info on pimsm interface : \
                  $interface, timeout"
            return $isError
        }
    }
    puts "RP learnt information refreshed ..."

    # Get RP Learned Info List
    set rpLearnedInfoList [ixNet getList $interface learnedCrpInfo]
    if {[llength $rpLearnedInfoList] == 0} {
        puts "No RP learnt info present ... "
        return $isError
    }

    # Loop through expected list & search in learntinfo list
    set i 0
    foreach rpInfo $rpLearnedInfoList {
        incr i
        set isFound 0
        set mismatch 0
        set numAttrToBeMatched 0
        puts "Browsing RP learnt Info list (entry $i)..."
        puts "------------------------------------------"
        foreach {attr attrVal} $checkLearnedRPList {
            incr numAttrToBeMatched
            #puts "Expected val for $attr is $attrVal"
            if {[matchAttributeValue $rpInfo $attr $attrVal] == 1} {
                # Handle not exactMatch cases hare ....
                incr mismatch
            }
        }

        if {$mismatch == 0} {
            # Reached here -> field match found in learnt info
            incr isFound
            puts "\t Learnt Info Expiry Timer : [ixNet getAtt $rpInfo -expiryTimer]"
            break
        }
    }

    puts "$isFound info present in RP Learnt Info List"
    if {$mismatch != 0} {
        puts "Not all expected info present in RP Learnt Info List"
        return $isError
    }

    set expectedNumLearntInfo [expr [llength $checkLearnedRPList] / \
            ($numAttrToBeMatched * 2)]
    
    puts "All $isFound info (Expected $expectedNumLearntInfo)present \
            in RP Learnt Info List"
    
    set isError 0
    return $isError
}


###############################################################################
# STATS VERIFICATION
###############################################################################
#-------------------------------------------------------------------------------
#   Procedure : checkAllPIMStats
#
#   Description: Checks all the PIM Stats.
#
#   Argument(s):
#       portLIst -  Ports on which the sessions has to be checked.
#       statList -  List of Stats to be checked.
#
#   NOTE: This is a dummy proc as of now. Once the stat APIs are available
#       body will be completed.
#-------------------------------------------------------------------------------
proc checkAllPIMStats { portList stat } {

    set sessFoundFlag 0
    set userViewList [ixNet getList [ixNet getRoot]/statistics userStatView]
    foreach view $userViewList {
        ixNet remove $view
        ixNet commit
    }

    set userStatView [SetupUserStats $portList "PIMSM" "*"]
    set timeout 20
    set doneList $portList

    array set statToVerify $stat

    set statNames [array names statToVerify]

    set returnFlag 1
    #Checking the stats.."
    set contFlag 0
    foreach eachStat $statNames {
        while {$timeout > 0} {
            GetStatValue "UserStatView PIMSM" "$eachStat" statValueArray1
            if {[lindex [array get statValueArray1] 1] >= $statToVerify($eachStat)} {
                PrintArray statValueArray1
                puts "For stat $eachStat expected is $statToVerify($eachStat) \
                    obtained: [lindex [array get statValueArray1] 1]"
            } else {
                PrintArray statValueArray1
                puts "For stat $eachStat expected is $statToVerify($eachStat) \
                      obtained: [lindex [array get statValueArray1] 1] --> MIS Match"
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
        logMsg "Error in establishing PIM sessions... Check the configuration"
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
proc verifyCapturedPackets {chassis card port matchFieldList {expPktCnt 1} \
           {expMaxPktCnt 1} } {
    set isError 1

    puts "Initializing through IxTclHal...."
    ixInitialize $chassis
    chassis get $chassis
    set chassisId [chassis cget -id]

    port get $chassisId $card $port
    set loginName [port cget -owner]
    ixLogin $loginName
    puts "Logging in using the $loginName"

    # Retrive captured packets
    captureBuffer get $chassisId $card $port
    set numCapturedPkts [captureBuffer cget -numFrames]
    puts "Captured $numCapturedPkts pkts (expected: $expPktCnt)"
    if {$numCapturedPkts < $expPktCnt} {
        return $isError
    }
    
    captureBuffer get $chassisId $card $port 1 $numCapturedPkts
    set cnt 0
    set matchedCapFrame 0
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
            incr cnt
            set matchedCapFrame $capframe
            puts "Matching Packet No. $cnt found"
        }
    }

    puts "The number of matched packets is $cnt"
    if {$cnt < $expPktCnt} {
        return $isError
    } elseif {($expMaxPktCnt > $expPktCnt) && ($cnt > $expMaxPktCnt)} {
        return $isError
    } else {
        return $matchedCapFrame
    }
}

