#-----------------------------------------------------------------------------#
# Source Individual file from a directory                                     #
#-----------------------------------------------------------------------------#
proc executeTestCaseFile {} {
    if {[catch {set tclFiles [glob test.*.tcl]} result]} {
        # no test.*.tcl in this directory
        set tclFiles {}
    }

    foreach executableTcl $tclFiles {
        global env argv0
        array set env [array get env]
        set argv0 ""
        puts "sourcing $executableTcl"
        if {[catch {source ./$executableTcl} errorMsg]} {
            puts "error in executing $executableTcl"
            puts "$errorMsg"
        }
    }
}

#-----------------------------------------------------------------------------#
# Drill down through directory                                                #
#-----------------------------------------------------------------------------#
proc Run { } {

    if {[catch {set files [lsort [glob -type d *]]} result]} {
        # This directory is empty!
        set files {}
    }

    foreach dir $files {
        cd $dir
        Run
        cd ".."
        puts "PWD == [join [lrange [split [pwd] /] 3 end] /]"
    }

    # source test.*.tcl files
    executeTestCaseFile
}

#----------------------------------------------------------------------------#
# Store the present working directory                                        #
#----------------------------------------------------------------------------#
set current_working_directory [pwd]

#----------------------------------------------------------------------------#
# $env(IX_NETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork is the root of all the        #
# test cases. So go to the root first                                        #
#----------------------------------------------------------------------------#
global env
cd "$env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork"

#----------------------------------------------------------------------------#
# Run all the test cases in batch                                            #
#----------------------------------------------------------------------------#
Run

#----------------------------------------------------------------------------#
# return back to old working directory again                                 #
#----------------------------------------------------------------------------#
cd $current_working_directory
