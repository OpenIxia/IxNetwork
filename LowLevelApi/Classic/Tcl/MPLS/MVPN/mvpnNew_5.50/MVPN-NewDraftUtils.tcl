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
# PROCEDURE  : checkBGPLearnedInfo
# PARAMETERS : neighborRange    - BGP neighborRange object
#              checkLearntInfoList - The list of expected info
#              filterList - The filter for leart info display
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
#-------------------------------------------------------------------------------
proc checkBGPLearnedInfo {neighborRange checkLearntInfoList {filterList {}}} {
    set isError 1

    # set filter following filterlist
    array set filterListArray $filterList

    log "Setting BGP Learnt Info filter ... \n [parray filterListArray]"
    set learnedFilter $neighborRange/learnedFilter
    set capabilities $learnedFilter/capabilities

    foreach {attr attrVal} $filterList {
        if {[setAndCheckAttributeValue $capabilities $attr [list $attrVal y]] \
            == 1} {
            return $isError
        }
    }
    after 2000

    log "Refreshing for learnt information on BGP neighbor: $neighborRange\n"
    set a [ixNet exec refreshLearnedInfo $neighborRange]

    set count 0
    set isComplete false
    while {$isComplete != true} {
        set isComplete [ixNet getAttr $neighborRange -isLearnedInfoRefreshed]
        log "isComplete = $isComplete"
        after 1000
        incr count
        if {$count > 40} {
            log "Could not retrieve learnt info on bgp neighbor: \
                 $neighborRange, timeout"
            break
        }
    }
    log "BGP Learnt Info refreshed for BGP Neighbor : $neighborRange !!!"

    # Get ALL Learned Info List
    set learnedInformation $neighborRange/learnedInformation

    foreach {learntInfoType db expectedCheckList} $checkLearntInfoList {
        # Get Learned Info List
        set learnedInfoList [ixNet getList $learnedInformation $learntInfoType]
        if {[llength $learnedInfoList] == 0} {
            log "No BGP learnt info present for $learntInfoType !!!"
            return $isError
        }

        log "[llength $learnedInfoList] BGP learnt info present for \
             $learntInfoType !!!"

        # Loop through expected list & search in learntinfo list
        set numInfoInCheckList 0
        set isFound 0
        foreach checkList $expectedCheckList {
            foreach $db $checkList {
                incr numInfoInCheckList
                log " -----------------------------"
                log "Browsing BGP $learntInfoType learntinfo list ..."

                foreach learntInfo $learnedInfoList {
                    set misMatch 0
                    foreach attr $db {
                        set attrVal [set [set attr]]
                        if {[matchAttributeValue $learntInfo $attr $attrVal] \
                             == 1} {
                             set misMatch 1
                             break
                        }
                    }

                    if {$misMatch == 0} {
                        # Reached here -> all field match found in learnt info
                        log "Expected learntinfo present in BGP $learntInfoType \
                             learntinfo list"
                        log " ----------------------------- "
                        incr isFound
                        break
                    }
                }
            }
        }

        log "Among all $numInfoInCheckList info $isFound are present in \
             BGP $learntInfoType Learnt Info List"

        if {$numInfoInCheckList != $isFound} {
            return $isError
        }
    }

    set isError 0
    return $isError
}


#-------------------------------------------------------------------------------
# PROCEDURE  : switchToSpmsi
# PURPOSE    :
# PARAMETERS : vport
#              numOfMcastSenderSiteToBeSwitched
#              l3SiteList
#              addressFamilyType: addressFamilyIpv4/addressFamilyIpv6
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
# USES       :
#-------------------------------------------------------------------------------

proc switchToSpmsi {neighborRangeList {addressFamilyType Both} \
                    {numOfMcastSenderSiteToBeSwitched All}} {
    set error 1

    set index 0
    foreach neighborRange $neighborRangeList {
        set l3SiteList1 [ixNet getList $neighborRange l3Site]

        foreach l3Site $l3SiteList1 {
            set multicastSenderSiteList [ixNet getList $l3Site \
                                                       multicastSenderSite]

            foreach multicastSenderSite $multicastSenderSiteList {
                set addressFamilyType1 \
                    [ixNet getAttr $multicastSenderSite -addressFamilyType]

                if {($addressFamilyType == "Both") || \
                     ($addressFamilyType == $addressFamilyType1)} {
                    incr index

                    if {$index > $numOfMcastSenderSiteToBeSwitched} {
                        break
                    }

                    if {[ixNet exec switchToSpmsi $multicastSenderSite] != \
                        "::ixNet::OK-{kBool,true}"} {
                        log "Not able to Switch To S-PMSI the Multicast Sender \
                             Site $index: $multicastSenderSite !!!"
                        return $error
                    }

                    log "Successfully Switch To S-PMSI the Multicast Sender \
                         Site $index: $multicastSenderSite !!!"
                    after 2000
                }
            }
        }
    }

    set error 0
    return $error
}