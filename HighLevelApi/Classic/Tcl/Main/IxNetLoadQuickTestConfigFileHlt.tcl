# This script will load a saved Quick Test config file.
# Users could passed in a list of ports so this config
# can run on any testbed.
#
#    - Connect to an existing configuration or load a saved
#      Quick Test config file and optionally, reassign ports.
#    - Verify user defined list of Quick Test names to run.
#    - Verify port state.
#    - Loop through each Quick Test name.
#    - Retrieve a copy of the csv saved results to local Linux.
#

set ixNetworkPort 8008
set ixNetworkTclServerIp 172.27.143.178
set ixiaChassisIp [list 172.27.143.172] 

# Set the value to {} if you want to use the existing configuration's port.
# Otherwise, if you provide a list of ports, they will be used.
set portList {1/5 1/6}

set userName willui

# The path to the saved config file on the IxNetwork Window's client PC.
# Leave this variable blank if you don't want to load a config file.
set ixncfgFile {}

# set value to "all" to run all the configured Quick Tests.
set userSelectQuickTestList "google-LSR-NDR google-LSR-v6-NDR"

# The local Linux machine's path to store the result files.
set copyResultFileToLocalLinuxPath /auto/wswillui-sjc/bemr/quicktest/results/

# The Quick Test result file to get
set quickTestCsvResultFile AggregateResults.csv

proc Help {} {
    exec clear >@ stdout
    puts "\nIxNetLoadQuickTestConfigFileHlt.tcl help:"
    puts "\t-ixNetworkTclServerIp:   The IxNetwork Windows PC"
    puts "\t-ixNetworkPort:          The IxNetwork socket port number"
    puts "\t-ixiaChassisIp:          The IP address of the Ixia chassis"
    puts "\t                         If you have multiple chassis's, then pass in a list like this:"
    puts "\t                              -ixiaChassisIP \"{1.1.1.1 1.1.1.2}\""
    puts "\t-portList:               The ports to use for this test wrapped inside double quotes"
    puts "\t                         If you have multiple chassis's, then pass in a list aligning to the ixiaChassis"
    puts "\t                         the ixiaChassis index list like this:"
    puts "\t                              -portList \"{1/1 1/3} {2/4 2/5}\""
    puts "\t-userName:               The username to use for logging in"
    puts "\t-ixncfgFile:             The full path to the Quick Test saved config file to load"
    puts "\t-quickTestListToRun:     All the Quick Test names to run wrapped inside double quotes"
    puts "\t                         Example: \"rfc2544_cat6k {rfc2544 cat3k} throughputTest\""
    puts "\t-copyResultsToLinuxPath: The full path and file name to save the Quick Test results on"
    puts "\t                         your local Linux."
    puts "\t                         Example: /automation/resultFolder"
    puts \n
    exit
}

proc GetTime {} {
    #return [clock format [clock seconds] -format "%H:%M:%S"]
    return [clock milliseconds]
}

proc Connect { {type reassignPorts} } {
    # Connect options are only: 
    #    - Resume to existing config.
    #    - Load a saved config and optionally, you could reassign ports also
    #
    # Parameter:
    #    type = reassignPorts or resume

    # Reassign ports
    if {$type == "reassignPorts"} {
	if {$::portList == ""} {
	    puts "\nError: You want to reassign ports, but the variable portList is not set with any ports"
	    exit
	}
	puts "\nConnect: Reassigning ports: $::ixiaChassisIp : $::portList\n"
	set hltParams { \
			    -device $::ixiaChassisIp \
			    -tcl_server $::ixiaChassisIp \
			    -port_list $::portList \
			    -ixnetwork_tcl_server $::ixNetworkTclServerIp\:$::ixNetworkPort \
			    -username $::userName \
			    -break_locks 1 \
			    -session_resume_keys 1
	}
	
	# Include loading a config file if the variable is set with a config file.
	if {$::ixncfgFile != ""} {
	    if {[file exists $::ixncfgFile] == 0} {
		puts "\n\n** ixNet config file does not exists: $::ixncfgFile\n\n"
		exit
	    } else {
		puts "\nLoading config file: $::ixncfgFile ..."
		append hltParams " -config_file $::ixncfgFile"
	    }
	}
    }

    # (Resume) Connect and use existing configuration
    if {$type != "reassignPorts"} {
	puts "\nConnect: Connecting to existing ports ...\n"
	set hltParams { \
			    -tcl_server $::ixiaChassisIp \
			    -ixnetwork_tcl_server $::ixNetworkTclServerIp\:$ixNetworkPort \
			    -username $::userName \
			    -break_locks 1 \
			    -session_resume_keys 1
	}
    }
    
    set connectStatus [eval ::ixia::connect $hltParams]
    if {[keylget connectStatus status] != $::SUCCESS} {
	puts "Connecting to IxNetwork Tcl server failed\n\n$connectStatus\n"
	puts "\nconnectStatus: [KeylPrint connectStatus]"
	exit
    } else {
	puts "Successfully connected to IxNetwork Tcl server"
    }
    
    puts "\n[KeylPrint connectStatus]\n"
    return $connectStatus
}

proc VerifyPortState { {portList all} {expectedPortState up} } {
    # portList format = 1/2.  Not 1/1/2

    puts "\nVerifyPortState ...\n"
    set allVports [ixNet getList [ixNet getRoot] vport]

    if {$portList == "all"} {
	set vPortList $allVports
    }

    if {$portList != "all"} {
	# Search out the user defined $portList
	set vPortList {}
	foreach vport $allVports {
	    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
	    set connectedTo [ixNet getAttribute $vport -connectedTo]
	    set connectedTo [lrange [split $connectedTo /] 3 4]
	    set card [lindex [split [lindex $connectedTo 0] :] end]
	    set port [lindex [split [lindex $connectedTo 1] :] end]
	    set port $card/$port

	    if {[lsearch $portList $port] != -1} { 
		lappend vPortList $vport
	    }
	}
    }

    set portsAllUpFlag 0

    foreach vport $vPortList {
	for {set timer 0} {$timer <= 60} {incr timer 2} {
	    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
	    set connectedTo [ixNet getAttribute $vport -connectedTo]
	    set connectedTo [lrange [split $connectedTo /] 3 4]
	    set card [lindex [split [lindex $connectedTo 0] :] end]
	    set port [lindex [split [lindex $connectedTo 1] :] end]
	    set port $card/$port
	    
	    set portState [ixNet getAttribute $vport -state]

	    # Expecting port state = UP
	    if {$expectedPortState == "up"} {
		if {$portState != "up" && $timer != "60"} {
		    puts "VerifyPortState: $port is still $portState. Expecting port up. $timer/60 seconds."
		    after 2000
		    continue
		}
		
		if {$portState != "up" && $timer == "60"} {
		    puts "\nError VerifyPortState: $port seem to be stuck on $portState state. Expecting port up.\n"
		    set portsAllUpFlag 1
		}
		
		if {$portState == "up"} {
		    puts "\nVerifyPortState: $port state is $portState"
		    break
		}
	    }

	    # Expecting port state = Down
	    if {$expectedPortState == "down"} {
		if {$portState != "down" && $timer != "60"} {
		    puts "\nVerifyPortState: $port is still $portState. Expecting port down. $timer/60 seconds."
		    after 2000
		    continue
		}
		
		if {$portState == "up" && $timer == "60"} {
		    puts "\nError VerifyPortState: $port seem to be stuck on the $portState state. Expecting port down."
		    set portsAllUpFlag 1
		}
		
		if {$portState == "down"} {
		    puts "\nVerifyPortState: $port state is $portState as expected"
		    break
		}
	    }
	}
    }

    if {$portsAllUpFlag == 1} {
	return 1
    } else {
	after 3000
	return 0
    }
}

proc KeylPrint {keylist {space ""}} {
    upvar $keylist kl
    set result ""
    foreach key [keylkeys kl] {
	set value [keylget kl $key]
	if {[catch {keylkeys value}]} {
	    append result "$space$key: $value\n"
	} else {
	    set newspace "$space "
	    append result "$space$key:\n[KeylPrint value $newspace]"
	}
    }
    return $result
}

proc GetAllQuickTestHandlesHlt {} {
    puts "Get All Quick Test handles ..."
    set testControlStatus [::ixia::test_control \
			       -action get_all_qt_handles \
			      ]
    
    if {[keylget testControlStatus status] != $::SUCCESS} {
	puts "GetAllQuickTestHandlesHlt Error: [keylget testControlStatus log]"
	return 0
    }
    set qtHandles [keylget testControlStatus qt_handle]
    return $qtHandles
}

proc ApplyQuickTestHandleHlt { quickTestHandle } {
    puts "\nApplying QA handle $quickTestHandle"
    set testControlStatus [::ixia::test_control \
			       -action         qt_apply_config \
			       -action_mode    async \
			       -qt_handle      $quickTestHandle \
			      ]
    if {[keylget testControlStatus status] != $::SUCCESS} {
	puts "ApplyQuickTestHandleHlt: [keylget testControlStatus log]"
	return 1
    }
 
    # ::ixNet::RESULT-3
    set resultHandle [keylget testControlStatus $quickTestHandle.result_handle]    
    #return $resultHandle
}

proc VerifyQuickTestApply { quickTestHandle } {
    set currentAction [string trim [GetQuickTestCurrentAction $quickTestHandle]]
    puts "\nVerifyQuickTestApply currentAction: $currentAction"
    if {$currentAction == "TestEnded" || $currentAction == "None"} {
	for {set timer 1} {$timer <= 20} {incr timer} {
	    set currentAction [string trim [GetQuickTestCurrentAction $quickTestHandle]]
	    if {$currentAction == "TestEnded" || $currentAction == "None"} {
		puts "\nCurrent State = $currentAction : Waiting $timer/20 seconds to change states"
		after 1000
		continue
	    } else {
		break
	    }
	}
    }

    set ixNetworkVersion [ixNet getAttribute [ixNet getRoot]/globals -buildNumberExtended]
    regexp "^\[^ ]+ *(\[0-9]+)\.\[^ ]+ *" $ixNetworkVersion - ixNetworkVersionNumber

    set applyQuickTestCounter 300
    for {set counter 1} {$counter <= $applyQuickTestCounter} {incr counter} {
	set quickTestApplyStates "InitializingTest ApplyFlowGroups SetupStatisticsCollection"
	set currentAction [string trim [GetQuickTestCurrentAction $quickTestHandle]]
	if {$currentAction == ""} {
	    # If using IxNetwork version < 8, expect blank and expect whitespaces
	    set currentAction "ApplyingAndInitializing"
	}

	# Version < 8, status = Trial when transmitting frames
	# Verrsion >= 8, status = TransmittingFrames 

	puts "VerifyQuickTestApply: $currentAction : Waiting $counter/$applyQuickTestCounter seconds"

	if {$ixNetworkVersionNumber >= 8} { 
	    if {$counter < $applyQuickTestCounter && $currentAction != "TransmittingFrames"} {
		after 1000
		continue
	    }
	}
	if {$ixNetworkVersionNumber < 8} { 
	    if {$counter < $applyQuickTestCounter && $currentAction == "ApplyingAndInitializing"} {
		continue
	    }
	}
	
	if {$ixNetworkVersionNumber >= 8} {
	    if {$counter < $applyQuickTestCounter && $currentAction == "TransmittingFrames"} {
		puts "\nVerifyQuickTestApply is done applying configuration and has started transmitting frames"
		break
	    }
	    break
	}

	if {$ixNetworkVersionNumber < 8} {
	    if {$counter < $applyQuickTestCounter && $currentAction == "ApplyingAndInitializing"} {
		puts "\nVerifyQuickTestApply is done applying configuration and has started transmitting frames"
		break
	    }
	    break
	}

	if {$counter == $applyQuickTestCounter} {
	    if {$ixNetworkVersionNumber >= 8 && $currentAction != "TransmittingFrames"} {
		puts "\nVerifyQuickTestApply is stuck on $currentAction. Waited $counter/$applyQuickTestCounter seconds"
		return 1
	    }
	    if {$ixNetworkVersionNumber < 8 && $currentAction != "Trial"} {
		puts "\nVerifyQuickTestApply is stuck on $currentAction. Waited $counter/$applyQuickTestCounter seconds"
		return 1
	    }
	}
    }
    
    return 0
}

proc StartQuickTestHlt { quickTestHandle } {
    puts "\nStartQuickTestHlt: $quickTestHandle"
    set testControlStatus [::ixia::test_control \
			       -action         qt_run \
			       -action_mode    async \
			       -qt_handle      $quickTestHandle \
			      ]
    if {[keylget testControlStatus status] != $::SUCCESS} {
	puts "StartQuickTestHlt Error: [keylget testControlStatus log]"
	return 1
    }
    return 0
}

proc GetQuickTestFlowViewHlt { quickTestHandle } {
    puts "\nGetQuickTestFlowViewHlt: $quickTestHandle"
    set testStats [::ixia::test_stats \
			       -mode qt_flow_view \
			       -qt_handle $quickTestHandle \
			    ]
    if {[keylget testStats status] != $::SUCCESS} {
	puts "Error: [keylget testStats log]"
	return 0
    }
    #puts "\n--- GetQuickTestFlowViewHlt keylPrint: [KeylPrint testStats]"
    #puts "Tx Frames --> [keylget testStats 1.tx_frames]"
    #puts "Rx Frames --> [keylget testStats 1.rx_frames]"
}

proc GetConfiguredQuickTests {} {
    set allConfiguredQuickTestNames {}
    set allConfiguredQuickTestHandles [ixNet getAttribute [ixNet getRoot]/quickTest -testIds]
    foreach qtHandle $allConfiguredQuickTestHandles {
	lappend allConfiguredQuickTestNames [ixNet getAttribute $qtHandle -name]
    }
    return $allConfiguredQuickTestNames
}

proc VerifyAllQuickTestNames { quickTestNameList } {
    # 1> Get a list of all the configured Quick Test objects
    # 2> From the above list, get a list of all the configured Quick Test names.
    # 3> Verify all the user defined Quick Test names with the actual configured list.

    set noSuchQuickTestName {}
    set allConfiguredQuickTestNames {}
    set allConfiguredQuickTestHandles [ixNet getAttribute [ixNet getRoot]/quickTest -testIds]

    foreach qtHandle $allConfiguredQuickTestHandles {
	lappend allConfiguredQuickTestNames [ixNet getAttribute $qtHandle -name]
    }

    puts "\nAll QT test names: $allConfiguredQuickTestNames\n"

    foreach userDefinedQuickTestName $quickTestNameList {
	if {[lsearch $allConfiguredQuickTestNames $userDefinedQuickTestName] == -1} {
	    lappend noSuchQuickTestName $userDefinedQuickTestName
	}
    }

    if {$noSuchQuickTestName != ""} {
	foreach noSuchTestName $noSuchQuickTestName {
	    puts "Error: No such QuickTest name: $noSuchTestName"
	}
    } else {
	return 0
    }
    return 1
}

proc GetQuickTestHandleByName { quickTestName } {
    foreach quickTestHandle [GetAllQuickTestHandlesHlt] {
	set currentQtName [ixNet getAttribute $quickTestHandle -name] 
	if {[regexp -nocase $quickTestName $currentQtName]} {
	    return $quickTestHandle
	}
    }
    return 0
}

proc GetQuickTestDuration { quickTestHandle } {
    return [ixNet getAttribute $quickTestHandle/testConfig -duration]
}

proc GetQuickTestTotalFrameSizesToTest { quickTestHandle } {
    return [llength [ixNet getAttribute $quickTestHandle/testConfig -framesizeList]]
}

proc GetQuickTestCurrentAction { quickTestHandle } {
    # NOTE:
    #   IxNetwork version 7.30 doesn't have the -currentAction support. This feature 
    #   is supported starting with 8.0 I believe.

    # IxNetwork 8.00.1027.17 EA
    set ixNetworkVersion [ixNet getAttribute [ixNet getRoot]/globals -buildNumberExtended]
    regexp "^\[^ ]+ *(\[0-9]+)\.\[^ ]+ *" $ixNetworkVersion - ixNetworkVersionNumber

    if {$ixNetworkVersionNumber >= 8} {
	# # InitializingTest, ApplyFlowGroups, SetupStatisticsCollection, TransmittingFrames, TestEnded
	return [ixNet getAttribute $quickTestHandle/results -currentAction]
    } else {
	# progress = " "  (white spaces) for version < 8
	set progressStatus [ixNet getAttribute $quickTestHandle/results -progress]
	return $progressStatus
    }
}

proc CopyFileWindowsToLocalLinux { windowsPath localPath } {
    # windowsPath = The path and file name on the Windows drive.
    # localPath   = The path and file name on the local Linux machine.

    puts "\nCopyFileWindowsToLocalLinux: From: $windowsPath To: $localPath"
    catch {ixNet exec copyFile [ixNet readFrom $windowsPath -ixNetRelative] [ixNet writeTo $localPath -overwrite]} errMsg
}

proc MonitorQuickTestRunProgress { quickTestHandle } {
    set counter 1
    while {1} {
	set isRunning [ixNet getAttribute $quickTestHandle/results -isRunning]
	if {$isRunning == "true"} {
	    set currentRunningProgress [ixNet getAttribute $quickTestHandle/results -progress]
	    puts "\n$counter seconds: $currentRunningProgress"
	    incr counter
	    after 1000
	    continue
	} else {
	    break
	}
    }	

    after 2000
}

proc GetVportMapping { Port } {
    # Search all vport for the port number.
    # Port format = 1/1.  Not 1/1/1.

    set vportList [ixNet getList [ixNet getRoot] vport]
    if {$vportList == ""} {
	return 0
    }
    
    foreach vport $vportList {
	set connectedTo [ixNet getAttribute $vport -connectedTo]
	set card [lindex [split [lindex [split $connectedTo /] 3] :] end]
	set portNum [lindex [split [lindex [split $connectedTo /] 4] :] end]
	set port $card/$portNum
	if {$port == $Port} {
	    return $vport
	}
    }
    return 0
}

set argIndex 0
while {$argIndex < [llength $argv]} {
    set currentArg [lindex $argv $argIndex]
    switch -exact -- $currentArg { 
	-ixiaChassisIp {
	    set ixiaChassisIp [lindex $argv [expr $argIndex + 1]]
	    incr argIndex 2
	}
	-tclServer {
	    set tclServer [lindex $argv [expr $argIndex + 1]]
	    incr argIndex 2
	}
	-ixNetworkTclServerIp {
	    set ixNetworkTclServerIp [lindex $argv [expr $argIndex + 1]]
	    incr argIndex 2
	}
	-ixNetworkPort {
	    set ixNetworkPort [lindex $argv [expr $argIndex + 1]]
	    incr argIndex 2
	}
	-portList {
	    set portList [lindex $argv [expr $argIndex + 1]]
	    incr argIndex 2
	}
	-userName {
	    set userName [lindex $argv [expr $argIndex + 1]]
	    incr argIndex 2
	}
	-ixncfgFile {
	    set ixncfgFile [lindex $argv [expr $argIndex + 1]]
	    incr argIndex 2
	}
	-quickTestListToRun {
	    set userSelectQuickTestList [lindex $argv [expr $argIndex + 1]]
	    incr argIndex 2
	}
	-copyResultsToLinuxPath {
	    set copyResultFileToLocalLinux [lindex $argv [expr $argIndex + 1]]
	    incr argIndex 2
	}
	help {
	    Help
	}
	default {
	    puts "\nError: No such parameter: $currentArg"
	    exit
	}
    }
}

package req Ixia

set connectStatus [Connect resume]

if {$userSelectQuickTestList == "all"} {
    set configuredQuickTestList [GetConfiguredQuickTests]
    if {$configuredQuickTestList != ""} {
	set quickTestNameList $configuredQuickTestList
    } else {
	puts "\nError: No Quick Test found on config file: $ixncfgFile"
	exit
    }
} else {
    # Verify user selected Quick Test to run. 
    if {[VerifyAllQuickTestNames $userSelectQuickTestList] == 1} {
	exit
    }
    set quickTestNameList $userSelectQuickTestList
}

puts "\nList of Quick Test to run ..."
foreach quickTestToRun $quickTestNameList {
    puts "\t$quickTestToRun"

}

#if {[VerifyPortState]} {
#    exit
#}

foreach quickTestName $quickTestNameList {
    set quickTestHandle [GetQuickTestHandleByName $quickTestName]
    set currentQuickTestName [ixNet getAttribute $quickTestHandle -name]

    puts "\nStarting QuickTest name: $currentQuickTestName" 

    # Get test duration
    set testDuration [GetQuickTestDuration $quickTestHandle]
    set totalFrameSizesToTest [GetQuickTestTotalFrameSizesToTest $quickTestHandle]

    ApplyQuickTestHandleHlt $quickTestHandle

    # Must wait 8000 for applying to sync before moving forward
    puts "\nWait 8 seconds for Quick Test to apply to hardware ..."
    after 8000

    if {[StartQuickTestHlt $quickTestHandle]} {
	exit
    }

    if {[VerifyQuickTestApply $quickTestHandle]} {
	exit
    }

    MonitorQuickTestRunProgress $quickTestHandle

    # resultPath = C:\Users\hgee\AppData\Local\Ixia\IxNetwork\data\result\DP.Rfc2889BroadcastRate\c3f7f1ee-9810-4c45-be49-7dd961aed060\Run0001
    set resultPath [ixNet getAttribute $quickTestHandle/results -resultPath]
    append resultPath \\$quickTestCsvResultFile

    # In case users included a slash at the end of the provided path, get rid of it.
    if {[string index $copyResultFileToLocalLinuxPath end] == "/"} {
	set copyResultFileToLocalLinuxPath [string replace $copyResultFileToLocalLinuxPath end end]
    }

    # Replace all blank spaces with an underscore for the result filename
    set currentQuickTestName [string map {" " _} $currentQuickTestName]

    # Result files to get options: iteration.csv, AggregateResults.csv, logfile.txt, results.csv 
    # The final result file name is: /path/AggregateResults_<quick test name>.csv    
    CopyFileWindowsToLocalLinux $resultPath $copyResultFileToLocalLinuxPath\/[lindex [split $quickTestCsvResultFile .] 0]\_$currentQuickTestName\_[GetTime]\.csv
}
