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
