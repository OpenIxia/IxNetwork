#-------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
#       PBBTE periodic learned info check and Protocol Stat and Packet structure
#       Varification.
#
# SCRIPT-GEN USED : Yes
#                   config.sample_script.pbbte.tcl
#                   Configure 1 Bridge in each port with 1 Trunk.
#                   Periodic LinkTrace , LoopBack,Delay Measurement is enabled
#                   with 2 iteration with interval of 5 sec.
#
#
# IXNCFG USED     : No
#
#
# Sequence of events being carried out by the script
#   1) Load the config file
#   2) Start the capture in the second port
#   3) Start PBBTE protocol & Wait for some time
#   4) Varify the periodic learned information
#   5) Check the Stats of the PBBTE Protocol
#   6) Start The Traffic and wait for some time
#   7) Stop The Traffic
#   8) Check the hex format of the received Packet
#   9) Start The Traffic and wait for some time
#   10) Stop The Traffic
#   11) Varify wheather traffic is received in the second Port
#
#
#-------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Standard package to include all IxNetwork APIs
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

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

    source $::pwd/pbbteCommonUtils.tcl
    source $::pwd/pbbteTrfficUtils.tcl
    source $::pwd/Stat.tcl

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
        if {[catch {set status [ixNet connect $client1 -port $tcpPort1]} error]} {
            puts "Unable to connect to ixNetwork"
            return $FAILED
        }

        if {[string equal $status "::ixNet::OK"] != 1} {
            puts "connection to client unsuccessful"
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


    # load config files
    if  {[catch {source "$::pwd/config.sample_script.pbbte.tcl"} err]} {
        puts $err
        puts "Loading Scriptgen config file : FAILED "
        ixNetCleanUp
        return $FAILED
    }
    puts "Loading Scriptgen config file : passed"


    # get the virtual port list
    puts "getting virtual ports ...."
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]
    puts "Virtual ports are = $vPorts"

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
        [list $chassisIp2 $card2 $port2] ]
    puts "realPortsList = $realPortsList"

    # Assign virtual ports to real ports
    puts "Assign virtual ports to real ports ..."
    set force true
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    ixNet commit
    puts "Assigned: $status"

    if {[string equal [lindex $status 0] $vPort1] != 1 || \
        [string equal [lindex $status 1] $vPort2] != 1} {
        ixNetCleanUp
        return $FAILED
    }
    ixTclNet::CheckLinkState $vPorts doneList

    puts "Waiting for 30 sec before starting ..."
    after 30000

    # capture cleanup
    if {[catch {ixNet exec closeAllTabs} err] == 1} {
        puts "Failed to close existing analyser tabs "
    }
    after 2000

    #Start the capture
    puts "Start Capturing packets"
    if {[catch {ixNet exec startCapture} err] == 1} {
        puts "Failed to start packet capture "
        ixNetCleanUp
        return $FAILED
    }


    puts "Starting Pbbte on both the ports.."
    ixNet exec start $vPort1/protocols/cfm
    ixNet exec start $vPort2/protocols/cfm

    # Expecting 2 LTM/LBM/DM  having 5 sec interval (10 Sec)
    puts "Waiting for 15 Sec..."
    after 15000

    set brobj [lindex [ixNet getList $vPort1/protocols/cfm bridge] 0]

    # First checking the periodic-LTM Learned information
    set checkInLearntInfoList {{"1" "VLANID 1 TPID 0x8100 Priority 0" "2" \
                                "00:00:00:00:00:02" "2" "0" "0" "0" "1" \
                                "00 00 00 00 00 02" "Complete Reply" "00:00:00:00:00:01"}}



    if {[checkPbbtePeriodicOAMLTLearnedInfo $brobj $checkInLearntInfoList]==1} {
        puts "All the attributes did not matched"
        return $FAILED
    }

    # Second checking the periodic-LBM Learned information
    set checkInLearntInfoList {{"VLANID 1 TPID 0x8100 Priority 0" "00:00:00:00:00:02" \
                               "2" "0" "0" "true" "00:00:00:00:00:01"}}
    if {[checkPbbtePeriodicOAMLBLearnedInfo $brobj $checkInLearntInfoList] == 1} {
        puts "All the attributes did not matched"
        return $FAILED
    }

    #Third checking the periodic-DM Learned information
    set checkInLearntInfoList {{"VLANID 1 TPID 0x8100 Priority 0" "2" "00:00:00:00:00:02" \
                                 "0" "0" "00:00:00:00:00:01"}}

    if {[checkPbbtePeriodicOAMDMLearnedInfo  $brobj $checkInLearntInfoList]==1} {
        puts "All the attributes did not matched"
        return $FAILED
    }

    #Checking the PBBTE Stats




 puts "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"


    set completeStats { "CFM Number Of Bridges Configured" 1 \
                        "CFM Number Of Bridges Running"    1 \
                        "MEPs Configured"                  0 \
                        "MEPs Running"                     0 \
                        "MAs Configured"                   1 \
                        "MAs Running"                      1 \
                        "Remote MEPs"                      1 \
                        "Trunks Configured"                1 \
                        "Trunks Running"                   1 \
                        "CFM LTM Tx"                       2 \
                        "CFM LTM Rx"                       2 \
                        "CFM LTR Tx"                       2 \
                        "CFM LTR Rx"                       2 \
                        "CFM LBM Tx"                       2 \
                        "CFM LBM Rx"                       2 \
                        "CFM LBR Tx"                       2 \
                        "CFM LBR Rx"                       2 \
                        "CFM AIS Tx"                       0 \
                        "CFM AIS Rx"                       0 \
                        "CFM DMM Tx"                       2 \
                        "CFM DMM Rx"                       2 \
                        "CFM DMR Tx"                       2 \
                        "CFM DMR Rx"                       2 \
                        "Invalid CCM Rx"                   0 \
                        "Invalid LBM Rx"                   0 \
                        "Invalid LBR Rx"                   0 \
                        "Invalid LTM Rx"                   0 \
                        "Invalid LTR Rx"                   0 \
                        "Defective RMEPS"                  0 \
                        "CCM Unexpected Period"            0 \
                        "Out of Sequence CCM Rx"           0 \
                        "RMEP Ok"                          1 \
                        "RMEP Error NoDefect"              1 \
                        "RMEP Error Defect"                0 \
                        "MEP FNG Reset"                    1 \
                        "MEP FNG DefectReported"           0 \
                        "MEP FNG DefectClearing"           0 \
                        "LR Respond"                       2}

    # Varifying the stat for the first Port
    set portList [list $portData1]
    if {[checkAllCfmStats $portList $completeStats 1]} {
        puts "Failure: Did not get the expected value for the all stats"
        ixNetCleanUp
        return $FAILED
    }
    puts "Success: Got expected values for all the stats"


    # Traffic Start
    if [generateApplyTraffic] {
        puts "Failed to start traffic"
        ixNetCleanUp
        return $FAILED
    }
    puts "Traffic applied successfully"

    if [startTraffic] {
        puts "Failed to start the traffic"
        ixNetCleanUp
        return $FAILED
    }
    puts "Traffic started successfully"

    puts "Waiting for 10 seconds for running the traffic"
    after 10000

    # Traffic Stop
    if [stopTraffic] {
        puts "Failed to stop traffic"
        ixNetCleanUp
        return $FAILED
    }


    puts "Stoping PBBTE ... "
    ixNet exec stop $vPort1/protocols/cfm
    ixNet exec stop $vPort2/protocols/cfm
    after 5000

    # Stop the capture
    puts "Stopping the capture"
    if {[catch {ixNet exec stopCapture} err] == 1} {
        puts "Failed to stop packet capture "
        ixNetCleanUp
        return $FAILED
    }

    # Packet structure
    #    0               1               2               3
    #  0+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #   |               Destination MAC Address                         |
    #  4+                               +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #   |                               |                               |
    #  8+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                               +
    #   |                      Source MAC Address                       |
    # 12+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #   |        Ether Type             |         S-Vlan                |
    # 16+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #   |      CFM Ether Type           |MD l | Version | Op Code = 1   |
    # 20+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #   |  Flags        | 1st TLV Octet |  Transaction Identifier (e.g.-|
    # 24+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #   |  - Sequence Number)           |                               |
    # 28+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                               +
    #   |              Maintenance Association Identifier               |
    #   +                                                               +
    #   |                                                               |
    # 74+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #   |                         RESERVED Y.1731                       |
    # 90+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #   |                          RESERVED                             |
    #   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #   |                          Optional TLV                         |
    #   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #   |                                FCS                            |
    #   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #
    # t.
    set matchFieldList {19  19  "03" \
                        26  32   "03 00 04 44 61 74 61" \
                        33  39  "1F 00 04 10 00 00 00"}

    if {[verifyCapturedPackets $chassisIp2 $card2 $port2 $matchFieldList] == 1} {
        puts "Expected field value match not found in capture buffer \
              for the port  $chassisIp2 $card2 $port2"
        ixNetCleanUp
        return $FAILED
    }

    puts "Wait for 10 sec"
    after 10000

    #Disabling Capture on ports
    ixNet setAttribute $vPort1 -rxMode measure
    ixNet setAttribute $vPort1/capture -hardwareEnabled False
    ixNet setAttribute $vPort1/capture -softwareEnabled False
    ixNet setAttribute $vPort2 -rxMode measure
    ixNet setAttribute $vPort2/capture -hardwareEnabled False
    ixNet setAttribute $vPort2/capture -softwareEnabled False
    ixNet commit

    # Changing the port to Measure Mode
    puts "Changing the port to Measure Mode ..."
    if {[ixNet setAttribute $vPort2 -rxMode measure]!= "::ixNet::OK"} {
        puts "Failed to change the rxMode of the port to measure flow"
        ixNetCleanUp
        return $FAILED
    }

    ixNet commit
    after 5000

    # Increase line rate to 100% from traffic api
    puts "Changing line rate to 100... "
    set traffic [ixNet getRoot]/traffic
    set lineRate [ixNet setAtt [lindex [ixNet getList \
                $traffic trafficItem] 0]/rateOptions -lineRate 100]
    if {$lineRate != "::ixNet::OK"} {
        puts "Not able to change the line rate to 100..."
        ixNetCleanUp
        return $FAILED
    }
    ixNet commit
    after 3000

    puts "Starting PBBTE ... "
    ixNet exec start $vPort1/protocols/cfm
    ixNet exec start $vPort2/protocols/cfm
    after 2000

    # Traffic Start
    if [generateApplyTraffic] {
        puts "Failed to start traffic"
        ixNetCleanUp
        return $FAILED
    }

    if [startTraffic] {
        puts "Failed to start traffic"
        ixNetCleanUp
        return $FAILED
    }
    puts "Traffic started successfully"

    puts "Waiting for 5 seconds..."
    after 5000

    # Traffic Stop
    if [stopTraffic] {
        puts "Failed to stop traffic"
        ixNetCleanUp
        return $FAILED
    }

    ixNet commit
    after 10000
    #---------------------------------------------------------------------------
    # First we are checking at least traffic statistics is comming in traffic
    # statistics view. What we will do to verify this is: Select a row from
    # the traffic statistics; and confirm that there is some non-zero stats.
    #---------------------------------------------------------------------------


    puts "Checking traffic statistics"
    set statistic    [ixNet getRoot]/statistics
    set statViewList [ixNet getList [ixNet getRoot]/statistics \
                         trafficStatViewBrowser]

    set indexOftraffStats [lsearch -regexp $statViewList "Traffic Statistics"]
    set trafficStats [lindex $statViewList $indexOftraffStats]

    ixNet setAttr $trafficStats -enabled true
    ixNet commit

    set rows  [ixNet getList $trafficStats row]
    set row1  [lindex $rows 0]
    set stats [ixNet getList $row1 cell]

    set rxFrames [ixNet getAttr [lindex $stats [lsearch -regexp $stats \
                      {Rx Frames}]] -statValue]

    set txFrames [ixNet getAttr [lindex $stats [lsearch -regexp $stats \
                      {Tx Frames}]] -statValue]

    set txframes     [expr ($txFrames / 20)]
    set txFrames     $txFrames
    set txFramesLess [expr ($txFrames - $txframes)]
    set txFramesMore [expr ($txFrames + $txframes)]

    if {$rxFrames <= $txFramesMore && $rxFrames >= $txFramesLess} {
        puts "Trafffic is getting received on the other end"
    } else {
        puts "Traffic is not getting recieved on the other end"
        ixNetCleanUp
        return $FAILED
    }
    puts "Traffic stats checking successfull"

    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
