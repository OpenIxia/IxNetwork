#-------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
#      To check the Traffic Statistics for ITU-Implementation.
#
# SCRIPT-GEN USED : No
# IXNCFG USED     : config.ituTrafficStats.ixncfg
#                 : configure 1 Bridge, 2 MEP, 2 MIP, single MD level, 2 MAC
#                   ranges, 5 mac count using Single VLAN (TPID 0x8100, default
#                   priority ) on each port and send traffic from Mac ranges.Use
#                   Different MA names.
#
# Sequence of events being carried out by the script
#   1) Load the config file
#   2) Start CFM protocol
#   3) Start Traffic
#   4) Wait for some time for traffic flow
#   5) Stop traffic
#   6) Check Transmitted and Received Frames
#   7) Stop CFM protocol
#
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

    # Source CFM common utility files
    source $::pwd/cfmCommonUtils.tcl
    source $::pwd/cfmTrafficUtil.tcl

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

    # Now we configure the first Ixia port
    puts "loading ixncfg file ..."
    # load config files
    if  {[ixNet exec loadConfig [ixNet readFrom "$::pwd/config.ituTrafficStats.ixncfg"]] != "::ixNet::OK"} {
        puts "Error in sourcing the file config.ituTrafficStats.ixncfg"
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
        [list $chassisIp2 $card2 $port2]]
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
        return $flag
    }
    ixTclNet::CheckLinkState $vPorts doneList

    puts "Waiting for 30 sec before starting ..."
    after 30000

    # Increase line rate to 100% from traffic api
    puts "Changing line rate to 100... "
    set traffic [ixNet getRoot]/traffic
    set lineRate [ixNet setAtt [lindex [ixNet getList $traffic trafficItem] 0]/rateOptions -lineRate 100]
    if {$lineRate != "::ixNet::OK"} {
        puts "Not able to change the line rate to 100..."
        ixNetCleanUp
        return $FAILED
    }
    ixNet commit
    after 3000
	
	


    puts "Starting CFM ... "
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
    puts "Waiting for 20 seconds..."
    after 10000

    #Traffic Stop
    if [stopTraffic] {
        puts "Failed to stop traffic"
        ixNetCleanUp
        return $FAILED
    }

    #Tx Frames
    set trafStat [lindex [ixNet getList [ixNet getRoot]/statistics trafficStatViewBrowser] 0]
    set TrafStatAttr [ixNet setAttr $trafStat -enabled true]
    if {$TrafStatAttr != "::ixNet::OK"} {
        puts "Not able to enable the Traffic Statistics Attribute..."
        ixNetCleanUp
        return $FAILED
    }
    ixNet commit
    after 3000
    set TxColumn [lindex [ixNet getList $trafStat column]  0]
    set TxCell [lindex [ixNet getList $TxColumn cell] 0]
    set TxFrame [ixNet getAttr $TxCell -statValue]

    #Rx Frames
    set trafStat [lindex [ixNet getList [ixNet getRoot]/statistics trafficStatViewBrowser] 0]
    set TrafStatAttr [ixNet setAttr $trafStat -enabled true]
    if {$TrafStatAttr != "::ixNet::OK"} {
        puts "Not able to enable the Traffic Statistics Attribute..."
        ixNetCleanUp
        return $FAILED
    }
    ixNet commit
    after 3000
	
	set AttributeList [ixNet getList $trafStat column]
    
    foreach x $AttributeList {
        set ColumnName [ixNet getAttr $x -name]
    }
    set index 0
    
    foreach y $ColumnName {
            if {[string compare $y "Rx Frame"]==0} {
                set index [expr $index+1]
            } else {
                break
            }
    }
	
    set RxColumn [lindex [ixNet getList $trafStat column]  $index]
    set RxCell [lindex [ixNet getList $RxColumn cell] 0]
    set RxFrame [ixNet getAttr $RxCell -statValue]

    #Comparing the Transmitted and Received Frames
    if [TxRxCalculation $TxFrame $RxFrame] {
        ixNetCleanUp
        return $FAILED
    }

    puts "Stoping CFM ... "
    ixNet exec stop $vPort1/protocols/cfm
    ixNet exec stop $vPort2/protocols/cfm
    after 2000

    ixNetCleanUp
    return $PASSED
}


#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action

