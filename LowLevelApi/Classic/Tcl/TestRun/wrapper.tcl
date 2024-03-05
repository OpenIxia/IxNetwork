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

#-----------------------------------------------------------------------------#
# PROCEDURE : Execute_Action                                                  #
# PURPOSE   : Creates a wrapper for the proc action which executes the sample #
#             test cases                                                      #
# INPUT     : none                                                            #
# OUTPUT    : writes the result of teh test case pass/fail in results.csv     #
#-----------------------------------------------------------------------------#
proc Execute_Action {} {
    global env
    set PASSED 0
    set FAILED 1

    #-------------------------------------------------------------------------#
    # create a .csv file to record the result                                 #
    #-------------------------------------------------------------------------#
    set resultFileId {NULL}
    set resultFilePath "$env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork"
    if {[catch {set resultFileId [open $resultFilePath/results.csv "a+"]}]} {
        puts "can't open result file: Pass/Fail result will not be recorded"
    }

    #-------------------------------------------------------------------------#
    # place file pointer to end of the file                                   #
    #-------------------------------------------------------------------------#
    if {$resultFileId != {NULL}} {
        seek $resultFileId 0 end
    }

    #-------------------------------------------------------------------------#
    # Procedure Action must be defined before invoking this function          #
    #-------------------------------------------------------------------------#
    if {[info proc Action] == {}} {
        error "Action proc not defined in this file"
    }

    #-------------------------------------------------------------------------#
    # Check if the script is being run from wish console or tclsh console     #
    #-------------------------------------------------------------------------#
    if {[regexp -nocase wish* $::argv0] || $::argv0 == ""} {
        # script invoked from wish console
        set testName [info script]
        set ::pwd    [file dirname $testName]
        set testName [file tail $testName]
        puts "wish: name of the script is $testName"
    } else {
        # script invoked from tclsh prompt
        set testName $::argv0
        puts "tclsh: name of the script is $testName"
    }

    setTestId $testName

    set portDataList1 [list $::chassis $::card1 $::port1 $::client $::tcpPort]
    set portDataList2 [list $::chassis $::card2 $::port2 $::client $::tcpPort]
    set home [pwd]

    set csvStr [join "$testName $::chassis $::card1 $::port1 $::card2 \
                      $::port2 $::client $::tcpPort" ","]

    #-------------------------------------------------------------------------#
    # Call the Action procedure:                                              #
    # ASSUMPTION : 1) Action returns 0 if test criteria is matched (PASSED)   #
    #              2) Action returns any non-zero value when test criteria    #
    #                 does not match (FAILED)                                 #
    #-------------------------------------------------------------------------#
    if {[catch {set result [Action $portDataList1 $portDataList2]} err]} {
        catch {unset ::pwd}
        puts "$testName\t\t: FAILED"
        puts "$err"
    } else {
        catch {unset ::pwd}

        # action is not needed any more release it
        rename Action {}

        if {$result == 0} {
             # your test cases passed
             puts "$testName\t\t: PASSED"
             puts "disconnecting from the client ..."

             # record the test result
             if {$resultFileId != {NULL}} {
                 puts $resultFileId "$csvStr,Passed"
                 close $resultFileId
             }

             catch  {ixNet disconnect}
             puts "Disconnected from the client."
             unsetTestId
             update

             return $PASSED
        } else {
             # your test caes failed
             puts "$testName\t\t: FAILED"
             puts "disconnecting from the client ..."

             # record the test result
             if {$resultFileId != {NULL}} {
                 puts $resultFileId "$csvStr,Failed"
                 close $resultFileId
             }

             catch {ixNet disconnect}
             puts "Disconnected from the client."
             unsetTestId
             update

             return $FAILED
        }
    }

    rename Action {}

    #-------------------------------------------------------------------------#
    # one should not reach here only when call to action has failed           #
    #-------------------------------------------------------------------------#
    if {$resultFileId != {NULL}} {
        puts $resultFileId "$csvStr,Failed"
        close $resultFileId
    }

    catch {ixNet disconnect}
    puts "Disconnected from the client."
    unsetTestId
    update

    return $FAILED
}
