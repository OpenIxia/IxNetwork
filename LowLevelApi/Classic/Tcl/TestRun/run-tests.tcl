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
