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

#-------------------------------------------------------------------------------
# PROCEDURE  : checkAllIsisStats
# PURPOSE    :
# PARAMETERS : portList -
#              stat - {name value} Stat list to verify
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------

proc checkAllIsisStats {portLists stat {exactMatch 0}} {
    return [checkAllProtocolStats $portLists "ISIS" $stat $exactMatch]
}


#-------------------------------------------------------------------------------
# PROCEDURE  : checkISISLearnedInfo
# PURPOSE    :
# PARAMETERS : router    - ISIS router object
#              checkList - The list of expected info to be checked in \
#                          learntInfoList
#              filterList - The filter for leart info display
#                   filterIpv4MulticastTlvs         Bool
#                   filterIpv6MulticastTlvs         Bool
#                   filterLearnedIpv4Prefixes       Bool
#                   filterLearnedIpv6Prefixes       Bool
#                   filterLearnedRbridges           Bool
#                   filterMacMulticastTlvs          Bool
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
#-------------------------------------------------------------------------------

proc checkISISLearnedInfo {router checkLearntInfoList {filterList {}}} {

    set isError 1

    # Below veriable is for debug log only
    array set filterListArray $filterList
    log "Setting ISIS Learnt Info filter ... \n [parray filterListArray]"

    # set filter following filterlist
    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $router $attr [list $attrVal y]] == 1} {
            return $isError
        }
    }
    after 2000

    # Refresh ISIS learnt Info
    set status [ixNet exec refreshLearnedInformation $router]
    after 10000
    set status [ixNet exec refreshLearnedInformation $router]

    if {[string first "::ixNet::OK" $status] == -1} {
        log "Failed to refresh ISIS Learnt info..."
        return $isError
    }
    after 30000
    log "ISIS learnt info refreshed ..."

    # Get ALL Learned Info List
    set routerLearnedInfoList [ixNet getList $router learnedInformation]
    log "Lenght of ALL Leant Info List :: [llength $routerLearnedInfoList]"

    foreach {leartInfoType db expectedCheckList} $checkLearntInfoList {
        # Get Learned Info List
        catch {ixNet help $routerLearnedInfoList} result
        puts $result

        set learnedInfoList [ixNet getList $routerLearnedInfoList $leartInfoType]
        puts "---------------> $learnedInfoList"

        if {[llength $learnedInfoList] == 0} {
            log "No ISIS learnt info present for $leartInfoType ... "
            return $isError
        }
        log "[llength $learnedInfoList] ISIS learnt info present for \
             $leartInfoType"

        # Loop through expected list & search in learntinfo list
        set numInfoInCheckList 0
        set isFound 0
        foreach checkList $expectedCheckList {
            foreach $db $checkList {
                incr numInfoInCheckList
                log " -----------------------------"
                log "Browsing ISIS $leartInfoType learntinfo list ..."
                foreach learntInfo $learnedInfoList {
                    set misMatch 0
                    foreach attr $db {
                        set attrVal [set [set attr]]
                        #log "$attr >> [ixNet getAttr $learntInfo -$attr]"
                        if {($attr == "age") || ($attr == "sequenceNumber")} {
                            log "$attr :: [ixNet getAttr $learntInfo -$attr] \
                               (expected $attrVal) - Not going for exact Match"
                            continue
                        }
                        if {[matchAttributeValue $learntInfo $attr $attrVal] \
                             == 1} {
                             set misMatch 1
                             break
                        }
                    }
                    if {$misMatch == 0} {
                        # Reached here -> all field match found in learnt info
                        log "Expected learntinfo present in ISIS $leartInfoType \
                             learntinfo list ..."
                        log " ----------------------------- "
                        incr isFound
                        break
                    }
                }
            }
        }
        log "Among all $numInfoInCheckList info $isFound are present \
             in ISIS $leartInfoType Learnt Info List"
        if {$numInfoInCheckList != $isFound} {
            return $isError
        }
    }
    set isError 0
    return $isError
}
