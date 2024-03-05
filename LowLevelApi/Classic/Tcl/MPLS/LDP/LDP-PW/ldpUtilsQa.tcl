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

###############################################################################
#   Procedure : getChassisCardPort
#
#   Description: Gets chassis name card and port from portData in Action.
#
#   Argument(s):
#   prt -   Port(refernce) to which router is added.
#       rtrId   -   Router Id of the router to be added.
#
###############################################################################
proc getChassisCardPort {port1Info {port2Info ""}} {
    set chassis1 [lindex $port1Info 0]
    set card1    [lindex $port1Info 2]
    set port1    [lindex $port1Info 3]
    puts "This is the details $chassis1 $card1 and $port1"
    if {$port2Info != ""} {
        set chassis2 [lindex $port2Info 0]
        set card2    [lindex $port2Info 2]
        set port2    [lindex $port2Info 3]
        set portLists [list [list $chassis1 $card1 $port1] \
                [list $chassis2 $card2 $port2]]
        return $portLists
    } else {
        set portLists [list [list $chassis1 $card1 $port1]]
        return $portLists
    }
}


###############################################################################
#   Procedure : checkLDPSessionUp
#
#   Description: This procedure checks the number of LDP sessions up on the
#                   port pecified.
#
#   Argument(s):
#       port        -   Port/Interface on which the number of sessions are to
#                       be checked.
#       sessions    -   Number of expectd sessions.
#
#   NOTES: This is a open proc as of now. Will be complete once the stats are
#           available.
#
###############################################################################
proc checkLDPSessionUp {portList sessions} {
    set sessFoundFlag 0
    set userViewList [ixNet getList [ixNet getRoot]/statistics userStatView]
    foreach view $userViewList {
        ixNet remove $view
        ixNet commit
    }

    set userStatView [SetupUserStats $portList "LDP" "*"]
    set timeout 5
    set doneList $portList

    puts "Checking the LDP stats.."
    set contFlag 0
    while {$timeout > 0} {
        GetStatValue "UserStatView LDP" "LDP Basic Sessions Up" statValueArray1
        PrintArray statValueArray1

        foreach portItem $doneList {
            scan [join [split $portItem]] "%s %s %s" ch card port
            puts "This is the chassis card port $ch $card $port"
            set sessFoundFlag 0
            puts "This is the number of sessions got from statistics \
                 $statValueArray1($ch,$card,$port)"
            if {([llength [array get statValueArray1]] > 0)} {
                if {$statValueArray1($ch,$card,$port) == $sessions} {
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

    if {$contFlag == 0} {
        logMsg "Error in establishing LDP sessions... Check the configuration"
        return 1
    }

    if {$sessFoundFlag == 1} {
        return 0
    } else {
        return 1
    }
    after 2000
}

###############################################################################
#   Procedure : checkLDPTragetSessionUp
#
#   Description: This procedure checks the number of LDP Targeted sessions up
#       on the port specified.
#
#   Argument(s):
#       portList    -   Port/Interface on which the number of sessions are to
#                       be checked.
#       sessions    -   Number of expectd sessions.
#
#
###############################################################################
proc checkLDPTargetedSessionUp {portList sessions} {
    puts "This is the ports $portList ################"
    set sessFoundFlag 0
    set userViewList [ixNet getList [ixNet getRoot]/statistics userStatView]
    foreach view $userViewList {
        ixNet remove $view
        ixNet commit
    }
    set userStatView [ixTclNet::SetupUserStats $portList "LDP" "*"]
    set timeout 3
    set doneList $portList

    #Checking the stats.."
    set contFlag 0
    while {$timeout > 0} {
        ixTclNet::GetStatValue "UserStatView LDP" "LDP Targeted Sessions Up" \
                      statValueArray1
        PrintArray statValueArray1

        foreach portItem $doneList {
            scan [join [split $portItem]] "%s %s %s" ch card port
            puts "This is the chassis card port $ch $card $port"
            set sessFoundFlag 0

            if {([llength [array get statValueArray1]] > 0)} {
                if {$statValueArray1($ch,$card,$port) == $sessions} {
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
    } ;# end while ($timeout)

    if {$contFlag == 0} {
        logMsg "Error in establishing LDP sessions... Check the configuration"
        return 1
    }
    if {$sessFoundFlag == 1} {
        return 0
    } else {
        return 1
    }
    after 2000

}


proc checkAllLdpStats { portList stat } {
    set sessFoundFlag 0
    set userViewList [ixNet getList [ixNet getRoot]/statistics userStatView]
    foreach view $userViewList {
        ixNet remove $view
        ixNet commit
    }

    set userStatView [SetupUserStats $portList "LDP" "*"]
    set timeout 20
    set doneList $portList

    array set statToVerify $stat
    set statNames [array names statToVerify]

    set returnFlag 1
    #Checking the stats.."
    set contFlag 0
    foreach eachStat $statNames {
        while {$timeout > 0} {
            GetStatValue "UserStatView LDP" "$eachStat" statValueArray1
            if {[lindex [array get statValueArray1] 1] >= $statToVerify($eachStat)} {
                PrintArray statValueArray1
                puts "For stat $eachStat expected is $statToVerify($eachStat)"
                puts "obtained: [lindex [array get statValueArray1] 1] "
            } else {
                PrintArray statValueArray1
                puts "For stat $eachStat expected is $statToVerify($eachStat)"
                puts "obtained: [lindex [array get statValueArray1] 1] --> MIS Match"
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
        logMsg "Error in establishing LDP sessions... Check the configuration"
        return 1
    }

    if {$returnFlag == 1} {
        return 0
    } else {
        return 1
    }
    after 2000
}

