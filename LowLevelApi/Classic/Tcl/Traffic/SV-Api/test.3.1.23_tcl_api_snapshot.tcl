#-------------------------------------------------------------------------------
# Name     : test.3.1.23_tcl_api_snapshot.tcl
# Author   : Pradeep Kumar MS
# Config   : config.10.1.25_10.1.26_tcl_api.ixncfg
# Purpose  : Configure 250 traffic items in a back to back scenario set page
#            size to 50 so that there is at least 5 pages of the traffic stats.
#            1) Tracking on IPv4 Source/Destination is on
#            2) Create Drill Down View by ""IPv4"" source address
#            3) Create Flow Detective View
#            Tcl View: change the default value of
#            "Snapshot.View.Csv.GeneratingMode"
#            and take a snapshot using the  API :ixTclNet::TakeViewCSVSnapshot
#            with value kNewCSVFile take snapshot for current page
#-------------------------------------------------------------------------------

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

proc Action {portData1 portData2} {
    # initialize return value
    set FAILED 1
    set PASSED 0

    # Get real card1/port1 from portData
    set chassisIp1 [getChassisIp $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    # Get real card2/port2 from portData
    set chassisIp2 [getChassisIp $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    # Hostname, where IxNetwork TCL-Server client runs
    set connection_Result [connectToClient $portData1 $portData2 "5.40"]
    log "Connection Result: $connection_Result"

   if {[string equal $connection_Result "::ixNet::OK"] != 1} {
        log "connection to client unsuccessful"
        return $FAILED
    }
    log "connectToClient Successful"

    # Clean up all the existing configurations from client
    log "cleaning up the client"
    ixNetCleanUp

    after 2000
    set configFileName config.[getTestId].ixncfg

    # load config files
    log "loading ixncfg file ..."
    if  {[ixNet exec loadConfig [ixNet readFrom $::pwd/$configFileName]] \
         != "::ixNet::OK"} {
        log "Loading IxNetwork config file FAILED "
        ixNetCleanUp
        return $FAILED
    }
    log "Loading IxNetwork config file : PASSED"

    # Getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2]]

    # Assign real ports to virtual ports
    log "getting virtual ports ...."
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]
    log "Virtual ports are = $vPorts"

    # Assign virtual ports to real ports
    log "Assign virtual ports to real ports ..."
    set force true
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    if {[string equal [lindex $status 0]  $vPort1] != 1 || \
        [string equal [lindex $status 1]  $vPort2] != 1} {
        ixNetCleanUp
        return $FAILED
    }
    ixTclNet::CheckLinkState $vPorts doneList

    # Start Protocol
    log "Stoping the Protocols ... "
    ixNet exec startAllProtocols

    log "Waiting for 20 Sec to check stats"
    after 20000

    # Check for Protocol Session UP
    log "Verify protocol stats.."
    set completeStats { "IPv4 Routers Configured" 1 \
                        "IPv4 Routers Running" 1}

    if {[checkAllProtocolStats $realPortsList \
        "EIGRP Aggregated Statistics" $completeStats]} {
        log "Failure: Did not get the expected value for the all stats"
        ixNetCleanUp
        return $FAILED
    }
    log "Control Plane UP and Runing ..."

    # Traffic Apply and Start
    set traffic [ixNet getRoot]/traffic
    if [generateApplyTraffic] {
        log "Failed to start traffic"
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic applyed successfully"

    if {[startTraffic $traffic] == 1} {
        log "Failed to start the traffic"
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic started successfully"

    log "Waiting for 20 seconds..."
    after 20000

    # Traffic Stop
    if {[stopTraffic $traffic] == 1} {
        log "Failed to stop traffic"
        ixNetCleanUp
        return $FAILED
    }

    log "Stoping the Protocols ... "
    ixNet exec stopAllProtocols
    after 4000

    # Check stats from TI Agregated view
    # Checking from Default 'Traffic Item Statistics' View
    log "Check Traffic Item Statistics..."
    if {[checkAllTrafficStats "Traffic Item Statistics"] == 1} {
        log "Not able to retrieve Traffic Item Statistics"
        ixNetCleanUp
        return $FAILED
    }

    set li1 {"Port Statistics"}
    set li2 [list {Snapshot.View.Csv.Name: "Port Statistics"}     \
                  {Snapshot.View.Csv.Location: "C:\Snapshot CSV"} \
                  {Snapshot.View.Csv.GeneratingMode: "kOverwriteCSVFile"}]

    if { [catch { ixTclNet::TakeViewCSVSnapshot $li1 $li2 } err] == 1} {
        puts "Error is $err"
        ixNetCleanUp
        return $FAILED
    }

    log "wait for 10 sec let sanp shot view get created"
    after 10000

    set files ""
    catch {set files [glob "/Snapshot CSV/*.csv"]}
    set len [llength $files]
    if {[llength $files] == 0} {
        log "No snap shot csv file created"
        ixNetCleanUp
        return $FAILED
    }

    set  fileName [lindex $files [expr $len-1]]
    log  "*** $fileName ***"

    if {[catch {readCsvSnapShotDataFromFile $fileName fileContents {Stat Name} \
                    [list {"Duplex Mode"} \
                          {"Frames Tx."} \
                          {"Valid Frames Rx."} \
                          {"Frames Tx. Rate"} \
                          {"Valid Frames Rx. Rate"} \
                          {"Data Integrity Frames Rx."}]} err] == 1} {
        log "Error in reading contents due to $err"
    }

    after 50000

    set matchString1 \
        "$chassisIp1/Card[format "%02d" $card1]/Port[format "%02d" $port1]"

    set matchString2 \
        "$chassisIp2/Card[format "%02d" $card2]/Port[format "%02d" $port2]"

    set row1 $fileContents($matchString1)
    set row2 $fileContents($matchString2)

    parray fileContents

    lappend checkValues [lindex $row1 0]
    lappend checkValues [lindex $row1 1]
    lappend checkValues [lindex $row1 2]
    lappend checkValues [lindex $row1 3]
    lappend checkValues [lindex $row1 4]
    lappend checkValues [lindex $row1 5]

    lappend checkValues [lindex $row2 0]
    lappend checkValues [lindex $row2 1]
    lappend checkValues [lindex $row2 2]
    lappend checkValues [lindex $row2 3]
    lappend checkValues [lindex $row2 4]
    lappend checkValues [lindex $row2 5]

    puts "checkValues is $checkValues"

    for {set count 0} {$count <= 6} {incr count 6} {
        lappend matchStatListPerRow [subst \
           {"Duplex Mode" [lindex $checkValues $count] 0 \
            "Frames Tx." [lindex $checkValues [expr $count+1]] 0 \
            "Valid Frames Rx." [lindex $checkValues [expr $count+2]] 0 \
            "Frames Tx. Rate" [lindex $checkValues [expr $count+3]] 0 \
            "Valid Frames Rx. Rate" [lindex $checkValues [expr $count+4]] 0}]
    }

    puts $matchStatListPerRow

    if {[checkAllStats "Port Statistics" $matchStatListPerRow] == 1} {
        log "Not able to retrieve statistics values for Port Statistics"
        ixNetCleanUp
        return $FAILED
    }

    set file2 "Port Statistics.csv"

    if {[file exists "$file2"] == 1} {
        log "Delete the file $file2"
        file delete -force "$file2"
    }

    # Cleanup
    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
