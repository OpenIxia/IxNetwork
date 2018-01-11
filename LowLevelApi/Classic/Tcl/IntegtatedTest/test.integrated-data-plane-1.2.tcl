#------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
# Shows how to run a integrated data plane test case and verify the stats and
# .csv file
#
# Sequence of events being carried out by the script
#    1) source the config file
#    2) Apply and start the traffic
#    3) Start test configuration
#    4) Stop test configuration
#    5) Read the generated .csv file
#    6) Verify the statistics
#
# SCRIPT-GEN USED : Yes
# IXNCFG USED     : No
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

#------------------------------------------------------------------------------
# PROCEDURE    : printStatFromCsv
# PURPOSE      : printing an analysing the CSV contents
# RETURN VALUE : -1 if failed 0 when passed.
#------------------------------------------------------------------------------
proc printStatFromCsv {path} {
    puts "opening file: $path"

    if {[catch {set fd [open $path "r"]} error]} {
        puts "unable to open: $path"
        puts "$error"
        cd $path
        return -1
    }

    if {[catch {set stream [read $fd]} error]} {
        puts "unable to read: $path"
        puts "$error"
        cd $path
        return -1
    }

    set lines [split $stream "\n"]
    foreach ln $lines {
        puts "$ln"
        flush stdout
    }

    # no error so return 0
    cd $path
    return 0
}


#------------------------------------------------------------------------------
# PROCEDURE    : returnCsvPath
# PURPOSE      : To return the path where CSV file is created as well as the
#                .CSV file name.
# INPUT        : current working directory
# OUTPUT       : string == "<Absolute-path>/<CSV filename>"
# ASSUMPTIONS  : Each time csv file created follows a definite rule:
#                (1)  First a Directory is created under
#                     "C:/Program Files/Ixia/IxNetwork/<username>//data/logs/"
#                (2)  Each time This Directory is created it is named a
#                     Test<num>-<TimeStamp>. So it is catchable with a regular
#                     expression
#                (3)  Inside that directory desired CSV file matches the
#                     regular expression "Traffic Statistics -*"
#------------------------------------------------------------------------------
proc returnCsvPath {home} {

    # take the help of system defined global env variable
    # to get the current USER NAAME
    global env
    set userName $env(USERNAME)

    set constPortion1 "C:/Program Files/Ixia/IxNetwork/"
    set constPortion2 "/data/logs/"

    set failed [catch {cd  $constPortion1$userName$constPortion2} error]
    if {$failed} {
        puts "unable to cd: $constPortion1$userName$constPortion2"
        puts "$error"
        return ""
    }

    set allDir ""
    catch {set allDir [glob "Test*"]}
    set lastCreated [lindex [lsort $allDir] end]
    puts "$constPortion1$userName$constPortion2$lastCreated"
    set path "$constPortion1$userName$constPortion2$lastCreated"

    set isDone [catch {cd $path} error]
    if {$failed} {
        puts "unable to cd: $path"
        puts "$error"
        cd $home
        return ""
    }

    set fileList ""
    catch {set fileList [glob "Traffic Statistics -*"]}
    set fileName [lindex  $fileList end]
    set pathAndFile "$path/$fileName"
    puts "CSV: $path/$fileName"

    cd $home
    return $pathAndFile
}


#------------------------------------------------------------------------------
# PROCEDURE    : portStats
# PURPOSE      : Returning port statistics values.
# INPUT        : Chassis card port and the stats want to check
# OUTPUT       : Corresponding port stat values
# RETURN VALUE : integer value
#------------------------------------------------------------------------------
proc portStats {hname crd prt statWanted} {
    set statViewObjRef ""
    set statViewList [ixNet getList [ixNet getRoot]/statistics statViewBrowser]
    foreach statView $statViewList {
        if {[ixNet getAttribute $statView -name] == "Port Statistics"} {
            if {[ixNet getAttribute $statView -enabled] == "false"} {
                ixNet setAttribute $statView -enabled true
                ixNet commit
            }
            set statViewObjRef $statView
            break
        }
    }

    if {$statViewObjRef == ""} {
        puts "no object view ref found"
        return -1
    }

    set continueFlag "true"
    set timeout 5

    while {$continueFlag == "true"} {
        if {[ixNet getAttribute $statViewObjRef -isReady] == true} {
            set rowList [ixNet getList $statViewObjRef row]
            foreach row $rowList {
                set cellList [ixNet getList $row cell]
                foreach cell $cellList {
                    set statName [ixNet getAttribute $cell -catalogStatName]
                    if {$statName == $statWanted}  {
                        set rowName [ixNet getAttribute $cell -rowName]
                        set statValue [ixNet getAttribute $cell -statValue]
                        set splitString [split $rowName /]
                        set hostName [lindex $splitString 0]
                        set card [string trimleft [lindex $splitString 1] "Card"]
                        set port [string trimleft [lindex $splitString 2] "Port"]
                        set card [string trimleft $card 0]
                        set port [string trimleft $port 0]
                        puts "here ........."
                        if {($hostName == $hname) && ($card == $crd) \
                            && ($port == $prt) } {
                            puts "comming here $hostName $card $port"
                            puts "$statName"
                            return $statValue
                        }

                        set statValueArray($hostName,$card,$port) $statValue
                        puts "\t$statName = $statValue"
                    }
                }
           }
           break
        } else {
            if {$timeout ==0} {
               set continueFlag false
            } else {
                after 1000
                incr timeout -1
            }
        }
    } ;# end while {$continueFlag == "true"}
    return 0
}


#------------------------------------------------------------------------------
# PROCEDURE    : Action
# PURPOSE      : Encapsulating all of your testing actions
# INPUT        : (1) [list $chassis1 $card1 $port1 $client1 $tcpPort1]
#                (2) [list $chassis2 $card2 $port2 $client2 $tcpPort2]
#                (3) home; (the current directory)
# RETURN VALUE : FAILED (1) or PASSED (0)
#------------------------------------------------------------------------------
proc Action {portData1 portData2} {

    # initialize return value
    set FAILED 1
    set PASSED 0

    # get port info 1
    set chassisIp1 [lindex $portData1 0]
    set card1      [lindex $portData1 1]
    set port1      [lindex $portData1 2]
    set client1    [lindex $portData1 3]
    set tcpPort1   [lindex $portData1 4]

    # get port info 2
    set chassisIp2 [lindex $portData2 0]
    set card2      [lindex $portData2 1]
    set port2      [lindex $portData2 2]
    set client2    [lindex $portData2 3]
    set tcpPort2   [lindex $portData2 4]

    if {$client1 == $client2} {
        set status ""
        puts "Connecting to client $client1"
        if {[catch {set status [ixNet connect $client1 -port \
            $tcpPort1]} error]} {
            puts "Unable to connect to ixNetwork"
            return $FAILED
        }

        if {[string equal $status "::ixNet::OK"] != 1} {
            puts "connection to client unsuccessfill"
            return $FAILED
        }

    } else {
        puts "Try to use the same client"
        return $FAILED
    }

    # clean up all the existing configurations from client
    puts "cleaning up the client"
    ixNetCleanUp
    puts "Executing from [pwd]"

    # Now we configure the first Ixia port
    puts "Now we configure the first Ixia port from the script-gen file"
    if {[catch {source "$::pwd/config.integrated-data-plane-1.2.tcl"} \
         error] } {
         puts "Error in sourcing the file .config.integrated-data-plane-1.2.tcl"
         puts "$error"
         return $FAILED
    }

    # get the virtual port list
    puts "getting virtual ports ...."
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]
    puts "Virtual ports are = $vPorts"

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
        [list $chassisIp2 $card2 $port2] ]

    # Assign virtual ports to real ports
    puts "Assign virtual ports to real ports ..."
    set force true
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    puts "Assigned: $status"
    ixNet commit
    if {[string equal [lindex $status 0] $vPort1] != 1 || \
        [string equal [lindex $status 1] $vPort2] != 1} {
        ixNetCleanUp
        return $FAILED
    }
    ixTclNet::CheckLinkState $vPorts doneList

    set root [ixNet getRoot]
    set trafficWizard $root/traffic/wizard
    set traffic $root/traffic
    set trafficItem [ixNet getList $traffic trafficItem]

    #enable CSV logging
    set stats $root/statistics
    ixNet setAttr $stats -enableCsvLogging True
    ixNet setAttr $stats -pollInterval 1
    ixNet commit

    puts "Generating the traffic item..."
    set genTraffic [ixNet setAtt [ixNet getRoot]/traffic \
                    -refreshLearnedInfoBeforeApply  true]

    if {$genTraffic != "::ixNet::OK"} {
    puts "Not able to start the traffic"
        ixNetCleanUp
        return $FAILED
    }
    puts "Generated the traffic successfully.."

    puts "Appling the traffic...."
    set applyTraffic [::ixNet exec apply $traffic]
    if {$applyTraffic != "::ixNet::OK"} {
        puts "Not able to apply the traffic"
        ixNetCleanUp
        return $FAILED
    }
    after 2000
    puts "Applied the traffic successfully.."

    puts "Start Test configuration..."
    ixNet exec startTestConfiguration

    puts "Wait for 120 second"
    after 120000

    puts "Stoping the test configuration...."
    ixNet exec stopTestConfiguration

    after 2000
    while { [regexp [ixNet getAtt [ixNet getRoot]/testConfiguration \
        -testRunning] true ] } {
        after 2000
    }
    puts "Test configuration stopped"

    puts "Stopping the traffic"
    if {[catch {ixNet exec stop $traffic} error]} {
        puts "Error in Stopping the traffic $error"
        ixNetCleanUp
        return $FAILED
    }

    puts "Stopping traffic ....."
    after 15000

    scan [ixNet getVersion] "%d.%d.%d.%d" magor minor x x
    set version $magor.$minor
    if {$version > 5.30} {
        puts "version is $version"
        return 0
    }

    if {[printStatFromCsv [returnCsvPath $::pwd]]} {
        puts "problem in parsing the .CSV file"
        cd $::pwd
        puts "cd $::pwd"
        ixNetCleanUp
        return $FAILED
    }

    set frameSent [portStats $chassisIp2 $card1 $port1 \
                   "Scheduled Frames Sent"]
    puts "Number of frame sent from port 1 : $frameSent"

    set frameReceived [portStats $chassisIp2 $card1 $port1 \
                       "Data Integrity Frames"]
    puts "Number of Data Integrity Frames received on port 2 : $frameReceived"

    # Need to remove assigned ports after test
    ixNetCleanUp
    return $PASSED
}


#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
