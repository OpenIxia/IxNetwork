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
# PROCEDURE  : verifyLacpLearnedInfo
# PURPOSE    :
# PARAMETERS : portList -
#              stat - {name value} Stat list to verify
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc verifyLacpLearnedInfo {linkProtoId checkLinkLearntInfoList \
                            {ckeckNumLAGsList {}}} {
    set isError 1

    # Request LearnedInfo
    set retVal [ixNet exec refreshLacpPortLearnedInfo $linkProtoId]

    set isComplete false
    set count 0
    while {$isComplete != true} {
        flush stdout
        set isComplete \
            [ixNet getAttr $linkProtoId -isLacpPortLearnedInfoRefreshed]

        puts "isComplete = $isComplete"
        after 5000
        incr count
        if {$count > 10} {
            puts "Could not retrieve learnt info on LACP link :\
                 <$linkProtoId> , ... timeout"
            return ""
        }
    }

    # Get Learned Info List
    set learnedInfoList [ixNet getList $linkProtoId learnedInfo]
    if {[llength $learnedInfoList] == 0} {
        log "No LACP learnt info present  ... "
        return $isError
    }
    log "[llength $learnedInfoList] LACP learnt info present... "

    foreach {db expectedCheckList} $checkLinkLearntInfoList {
        # Loop through expected list & search in learntinfo list
        set numInfoInCheckList 0
        set isFound 0
        foreach checkList $expectedCheckList {
            #puts "db $db --- checkList $checkList ... "
            foreach $db $checkList {
                incr numInfoInCheckList
                log " -----------------------------"
                log "Browsing LACP learntinfo list ..."
                foreach learntInfo $learnedInfoList {
                    set misMatch 0
                    foreach attr $db {
                        set attrVal [set [set attr]]
                        #puts "[ixNet help $learntInfo]"
                        log "$attr >> [ixNet getAttr $learntInfo -$attr]"
                        if {[matchAttributeValue $learntInfo $attr $attrVal] \
                             == 1} {
                             set misMatch 1
                             break
                        }
                    }

                    if {$misMatch == 0} {
                        # Reached here -> all field match found in learnt info
                        log "Expected learntinfo present in LACP learntinfo"
                        log " ----------------------------- "
                        incr isFound
                        break
                    }
                }
            } ;# learntInfo $learnedInfoList
        } ;# checkList $expectedCheckList

        log "Among all $numInfoInCheckList info $isFound are \
             present in LACP Learnt Info List"
        if {$numInfoInCheckList != $isFound} {
            return $isError
        }
    }

    set isError 0
    return $isError
}


