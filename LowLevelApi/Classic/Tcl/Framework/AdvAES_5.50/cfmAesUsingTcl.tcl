source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#-----------------------------------------------------------------------------#
# PURPOSE : Example test cases demonstrating the AES execution Tcl            #
#-----------------------------------------------------------------------------#

proc Action {portData1 portData2} {

    set FAILED 1
    set PASSED 0

    # get port info 1
    set chassisIp1 [getChassisIp $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    # get port info 2
    set chassisIp2 [getChassisIp  $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    # Hostname, where IxNetwork TCL-Server client runs
    set hostName [lindex [getHostName $portData1] 0]

    # Version Number (IxNetwork Major version No i.e. 5.50)
    set version "5.50"

    # connect to client
    if {[ixNet connect $hostName -version 5.50] != "::ixNet::OK"} {
        puts "Test case failed unable to connect to IxNetwork"
        return $FAILED
    }

    # clean up config
    ixNet exec newConfig

    # Configure IxNetwork GUI
    ixNet exec loadConfig [ixNet readFrom $::pwd/cfm1Config.ixncfg]

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2]]

    # get root object
    set root [ixNet getRoot]

    # Assign real ports to virtual ports
    puts "getting virtual ports ...."
    set vPorts [ixNet getList $root vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]


    # Assign virtual ports to real ports
    puts "Assign virtual ports to real ports ..."
    if {[catch {ixTclNet::AssignPorts $realPortsList {} $vPorts}]} {
        puts "Error in assigning ports"
        ixNet exec newConfig
    }

    # Check if the ports are assigned; if un-assigned re-assign them
    if {[ifUnassignedConnectAgain] == 1} {
        puts "Not able to re-assign the ports !!!"
        ixNetCleanUp
        return $FAILED
    }
    puts "Ports are in assigned state !!!"
    after 5000

    ixNet exec startTestConfiguration
    puts "integrated test running ...."

    puts "wait for 30 sec"
    after 30000

    set itest [ixNet getRoot]/testConfiguration
    while {[ixNet getAttr $itest -testRunning] == "true"} {
        after 1000
    }

    # Cleanup
    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action